"""Merge v0.10 proof ledgers without rewriting any earlier source array.

Run from any directory. Source bytes, inclusive raw-line ranges, declaration
anchors, pinned Git blobs, prior-record preservation and component counts are
checked before the three output files are replaced. This is provenance
validation, not Lean elaboration or kernel replay.
"""
from copy import deepcopy
from pathlib import Path
import hashlib
import json
import re
import subprocess

BASE = Path(__file__).resolve().parents[1]
REPO = BASE / "alpoge-rh"
OUT = BASE / "output/RH_reconstruction_v0_10"
OLD_PATH = BASE / "output/RH_reconstruction_v0_9/provenance.json"
MAIN_PATH = BASE / "output/pdf/RH_readable_reconstruction_v0_10.tex"
PIN = "7cbf7a0c32fca1badf05931879a37c3f8a2b03b4"
URL = "https://github.com/CocoSgt/riemann-hypothesis-lean/blob/" + PIN + "/"
COMPONENTS = [
    ("rank_upper","RU",1,11,"main.tex"),
    ("rank_lower","RD",1,15,"main.tex"),
    ("harmonic_model","HM",1,12,"main.tex"),
    ("numerical_parameters","NP",1,9,"main.tex"),
    ("type_one_closure","TC",1,6,"main.tex"),
]


def digest(raw):
    return hashlib.sha256(raw).hexdigest()

old_bytes = OLD_PATH.read_bytes()
old = json.loads(old_bytes)
assert old["commit"] == PIN
assert old["artifact_version"] == "0.9"
assert len(old["claims"]) == 315
assert len(old["source_files"]) == 764
assert subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=REPO, text=True).strip() == PIN
# Compare the local bytes to the blob IDs in the pinned tree, independently
# of the hashes recorded in either old or new JSON.
tree = subprocess.check_output(["git", "ls-tree", "-r", "-z", PIN], cwd=REPO)
blob_ids = {}
for item in tree.split(b"\0"):
    if not item:
        continue
    metadata, path = item.split(b"\t", 1)
    _mode, kind, oid = metadata.split()
    if kind == b"blob":
        blob_ids[path.decode()] = oid.decode()

old_claims = {c["id"]: c for c in old["claims"]}
old_files = {s["path"]: s for s in old["source_files"]}
assert len(old_files) == len(old["source_files"])
files = deepcopy(old_files)
cache = {}
validated_ranges = set()
anchor_methods = {"declaration_line": 0, "named_occurrence": 0, "focus_range": 0}


def source_path(s):
    path = s.get("path", s.get("source_path"))
    assert isinstance(path, str) and path
    if not path.startswith("src/"):
        path = "src/" + path
    assert ".." not in Path(path).parts and not Path(path).is_absolute()
    return path


def rawfile(path):
    if path not in cache:
        raw = (REPO / path).read_bytes()
        assert path in blob_ids, (path, "absent from pinned tree")
        git_hash = hashlib.sha1(b"blob " + str(len(raw)).encode() + b"\0" + raw).hexdigest()
        assert git_hash == blob_ids[path], (path, "local bytes differ from pinned Git blob")
        cache[path] = raw
    return cache[path]


def file_record(path, expected=None, role=None):
    raw = rawfile(path)
    sha = digest(raw)
    if expected is not None:
        assert sha == expected, (path, "file SHA-256")
    if path in files:
        assert files[path]["sha256"] == sha, (path, "conflicting recorded hash")
    else:
        files[path] = {
            "path": path, "sha256": sha, "bytes": len(raw),
            "lines": len(raw.decode().splitlines()), "url": URL + path,
            "verified_equal_to_pinned_git_blob": True,
        }
        if role:
            files[path]["role"] = role
    return raw, sha


def reference(s):
    """Validate an input reference; normalize only new references with this result."""
    path = source_path(s)
    name = s.get("declaration", s.get("declaration_as_spelled"))
    assert isinstance(name, str) and name, (path, "missing declaration label")
    a, b = s["line_start"], s["line_end"]
    expected = s.get("sha256", s.get("source_sha256", s.get("full_file_sha256")))
    assert expected, (path, name, "missing full-file hash")
    raw, sha = file_record(path, expected)
    raw_lines = raw.splitlines(keepends=True)
    lines = raw.decode().splitlines()
    assert isinstance(a, int) and isinstance(b, int) and 1 <= a <= b <= len(lines), (path, name, "range")
    selected = b"".join(raw_lines[a-1:b])
    range_hash = digest(selected)
    expected_range = s.get("range_sha256", s.get("excerpt_sha256", s.get("declaration_sha256")))
    assert expected_range and expected_range == range_hash, (path, name, "inclusive raw-line SHA-256")
    if "range_bytes" in s:
        assert s["range_bytes"] == len(selected), (path, name, "range byte count")
    if "byte_start" in s:
        assert s["byte_start"] == sum(map(len, raw_lines[:a-1]))
    if "byte_end_exclusive" in s:
        assert s["byte_end_exclusive"] == sum(map(len, raw_lines[:b]))
    if "first_line" in s:
        assert s["first_line"] == lines[a-1], (path, name, "first-line anchor")
    short = name.rsplit(".", 1)[-1]
    spelling = s.get("source_spelling", short)
    focus = bool(s.get("focus_range") or s.get("entry_type") == "focus_range")
    excerpt = "\n".join(lines[a-1:b])
    # Older canonical arrays omitted source_spelling. A declaration may spell
    # a nontrivial lexical suffix such as HStrip.tailPos_shift, rather than
    # either its fully qualified name or its final component alone.
    suffixes = [".".join(name.split(".")[i:]) for i in range(len(name.split(".")))]
    candidates = list(dict.fromkeys([name, spelling, short] + suffixes))
    pattern = r"\b(?:def|abbrev|theorem|lemma|structure|class|inductive)\s+(?:" + "|".join(re.escape(x) for x in candidates) + r")(?=[\s(:{]|$)"
    declaration_lines = [i+1 for i in range(a-1, b) if re.search(pattern, lines[i])]
    assert focus or declaration_lines or name in excerpt or short in excerpt or spelling in excerpt, (path, name, "named anchor")
    if "declaration_lines_within_range" in s:
        # Earlier canonical fields are preserved verbatim. Validate every
        # stored line as a real named declaration without requiring the new
        # parser to produce an identical supplementary list.
        for line in s["declaration_lines_within_range"]:
            assert a <= line <= b and re.search(pattern, lines[line-1]), (path, name, "stored declaration-line anchor")
    expected_url = URL + path + f"#L{a}-L{b}"
    supplied_url = s.get("url", s.get("pinned_url"))
    assert supplied_url == expected_url, (path, name, "pinned URL")
    anchor_methods["focus_range" if focus else "declaration_line" if declaration_lines else "named_occurrence"] += 1
    validated_ranges.add((path, a, b, range_hash))
    out = {
        "path": path, "declaration": name, "line_start": a, "line_end": b,
        "sha256": sha, "range_sha256": range_hash, "url": expected_url,
        "first_line": lines[a-1], "declaration_lines_within_range": declaration_lines,
    }
    if focus:
        out["entry_type"] = "focus_range"
    if s.get("role"):
        out["role"] = s["role"]
    return out


# Validate old source records, but retain the original arrays exactly.
claims = deepcopy(old["claims"])
for c in claims:
    for s in c["sources"]:
        reference(s)
for path, s in old_files.items():
    raw, _sha = file_record(path, s["sha256"])
    assert s["bytes"] == len(raw)
    assert s["lines"] == len(raw.decode().splitlines())
    assert s["url"] == URL + path

# Append current scope without changing any earlier claim or source array.
REMAINS = [
    "Global abundance and compatibility of the literal Type-I and Type-II data, including orbit counts and all simultaneous arithmetic choices.",
    "Actual theta/common-image and spectral/arithmetic-kernel identities, metric transport and discarded target control.",
    "Congruence denominators, cohomological windows, PairEx prime selection and the final uniform centered prime-sum argument.",
]
UPDATES = {
    "TI7": ["RU8","RD15","HM6","NP8","TC6"],
    "TI8": ["RD15","NP7","TC5","TC6"],
    "TI9": ["RU11","RD15","HM12","NP8","TC6"],
    "JR10": ["TC6"],
    "SW8": ["RU8","NP3"],
    "SW9": ["NP3","RD14"],
    "SW11": ["RU11","RD15","HM12","NP8","TC6"],
    "SW12": ["NP2","NP7"],
    "RL11": ["NP2","NP7","RU11","TC6"],
}
for c in claims:
    if c["id"] in UPDATES:
        c["version_0_10_update"] = {
            "status": "local_Type_I_application_completed_under_literal_supplied_hypotheses",
            "explanation": "RU/RD supply both actual coarse ranks and density; HM supplies harmonic and cloud maps plus ring transport; NP supplies all uniform numerical fields and the shifted height. TC6 proves Conclusion2 directly, with C0>=880, CH>=2800001 and C=302114, without an unproved bundled AdmB/AdmT premise.",
            "discharged_by": UPDATES[c["id"]],
            "separate_remaining_work": REMAINS,
            "scope": "Complete supplied-data local Type I. No global parameter-existence or complete RH/Dirichlet-GRH proof assertion.",
        }

component_inputs, artifact_inputs, new_counts, new_scopes = [], [], {}, {}
for component,prefix,first,last,texname in COMPONENTS:
    directory=BASE/"v0_10"/component
    raw=(directory/"provenance.json").read_bytes()
    data=json.loads(raw)
    repository=data.get("repository")
    pin=data.get("commit",data.get("source_commit"))
    if pin is None and isinstance(repository,dict):pin=repository.get("commit")
    assert pin==PIN and data["artifact_version"]=="0.10"
    assert {c["id"] for c in data["claims"]}=={f"{prefix}{i}" for i in range(first,last+1)}
    component_inputs.append({"path":str((directory/"provenance.json").relative_to(BASE)),"sha256":digest(raw),"claims":last-first+1})
    new_counts[prefix]=last-first+1
    new_scopes[component]={k:deepcopy(data[k]) for k in ["scope_note","outside_scope","explicit_external_dependencies","independent_reviews"] if k in data}
    for record in data.get("source_files",data.get("files",[])):
        path=source_path(record)
        raw_file,_=file_record(path,record.get("sha256",record.get("full_file_sha256",record.get("source_sha256"))))
        if "bytes" in record: assert len(raw_file)==record["bytes"]
        if "line_count" in record: assert len(raw_file.splitlines())==record["line_count"]
    for rec in list(data.get("artifacts",[]))+[{"path":name,"sha256":sha} for name,sha in data.get("artifact_sha256",{}).items()]:
        content=(directory/rec["path"]).read_bytes()
        assert digest(content)==rec["sha256"],(component,rec["path"],"artifact hash")
        if "bytes" in rec: assert len(content)==rec["bytes"]
    for path in sorted(directory.glob("*")):
        if path.is_file() and path.suffix in {".tex",".txt",".json",".py"}:
            artifact_inputs.append({"path":str(path.relative_to(BASE)),"sha256":digest(path.read_bytes())})
    for c in data["claims"]:
        n=deepcopy({k:v for k,v in c.items() if k!="sources"})
        n["introduced_in"]="0.10"
        n["component_ledger"]=component+"/provenance.json"
        n["sources"]=[reference(x) for x in c["sources"]]
        n["proof_location"]={"file":component+"/"+texname,"expanded":component+"/report.txt","section":c["id"]}
        claims.append(n)

ids=[c["id"] for c in claims]
assert len(ids)==len(set(ids))==368
assert sum(new_counts.values())==53
by_id={c["id"]:c for c in claims}
def stable_ids(v):
    if isinstance(v,str): return [v] if re.fullmatch(r"[A-Z]+[0-9]*",v) else []
    if isinstance(v,list): return [x for e in v for x in stable_ids(e)]
    if isinstance(v,dict): return [x for e in v.values() for x in stable_ids(e)]
    return []
for c in claims:
    if c["id"] in old_claims:
        prior=old_claims[c["id"]]
        for key,value in prior.items(): assert c[key]==value,(c["id"],key,"historical field changed")
        assert set(c)-set(prior)<={"version_0_10_update"}
    for field in ["depends_on","dependencies"]:
        for cid in stable_ids(c.get(field,[])): assert cid in by_id,(c["id"],cid)
    for cid in c.get("version_0_10_update",{}).get("discharged_by",[]): assert cid in by_id

graph=deepcopy(old["mathematical_dependency_graph"])
for c in claims:
    if c["id"] not in old_claims:
        graph[c["id"]]=list(dict.fromkeys(stable_ids(c.get("depends_on",c.get("dependencies",[])))))
state,trail,topo={},[],[]
def visit(cid):
    if state.get(cid)==2:return
    assert state.get(cid)!=1,("proof dependency cycle",trail+[cid])
    state[cid]=1;trail.append(cid)
    for dep in graph[cid]:
        assert dep in by_id,(cid,dep)
        visit(dep)
    trail.pop();state[cid]=2;topo.append(cid)
for cid in ids:visit(cid)

main_raw=MAIN_PATH.read_bytes()
bibliography={"src/"+x for x in re.findall(r"\\src\{([^{}]+)\}",main_raw.decode())}
for path in bibliography:file_record(path,role="Additional bibliography source in the integrated v0.10 document.")
for path,record in old_files.items(): assert files[path]==record
assert OLD_PATH.read_bytes()==old_bytes
for record in component_inputs+artifact_inputs:
    assert digest((BASE/record["path"]).read_bytes())==record["sha256"],record["path"]

boundaries=deepcopy(old["component_input_boundaries"])
complete="The complete local Type-I Conclusion2 is reconstructed in TC6 under literal HypI, with C0>=880, CH>=2800001 and C=302114. Global existence/compatibility of these data remains separate."
for key in ["TI","JR","SW","RL"]:boundaries[key]=complete
boundaries.update({
    "RU":"Actual coarse upper rank, exact digit-to-HH mass, finite-free block lattices, Smith selection and paired assembly are proved.",
    "RD":"Actual coarse lower rank, all loss factors, finite harmonic density, boundary volumes and final exceptional mean are proved.",
    "HM":"Actual polynomial harmonic quotients and maps, normalized duality, one-sided edge bound, integral complementary contraction, full cloud maps and coefficient-ring transport are proved.",
    "NP":"All literal Std, rounded windows, depth, conductor, density-interface numerics and exact shifted tStar<=tI bounds are supplied with explicit thresholds.",
    "TC":complete,
})
counts={
    "claims":len(claims),"new_claims":53,"new_claims_by_prefix":new_counts,
    "source_links":sum(len(c["sources"]) for c in claims),
    "old_source_links_preserved":sum(len(c["sources"]) for c in old["claims"]),
    "new_source_links":sum(len(c["sources"]) for c in claims if c["id"] not in old_claims),
    "source_files":len(files),"old_source_files_preserved":len(old_files),
    "new_source_files":len(files)-len(old_files),"unique_source_ranges":len(validated_ranges),
    "main_bibliography_paths":len(bibliography),"explicit_dependency_edges":sum(map(len,graph.values())),
    "historical_claim_status_updates":len(UPDATES),
}
validation={
    **counts,"all_file_and_range_hashes_validated":True,"all_named_or_focus_anchors_validated":True,
    "anchor_validation_methods_per_link":anchor_methods,"all_source_bytes_equal_pinned_git_blobs":True,
    "all_prior_source_arrays_exactly_preserved":True,"all_prior_source_file_records_exactly_preserved":True,
    "all_prior_claim_fields_preserved_except_appended_version_annotations":True,"all_prior_ids_preserved":True,
    "all_main_bibliography_paths_in_source_index":True,"all_explicit_dependency_ids_resolve":True,
    "explicit_mathematical_dependency_graph_acyclic":True,"component_artifact_hashes_validated_when_supplied":True,
    "no_lean_build_or_kernel_replay":True,
}
conclusion={
    "local_Type_I":"TC6: literal HypI implies Conclusion2, with C0>=880, CH>=2800001 and C=302114.",
    "constants":{"C0_min":880,"CE1":17,"CE2":17,"Cm":17,"Ckap":3,"Ct":30,"Cc":4,"CA":50000,"Cs":351,"CH_inner":700000,"TLP":400093,"TM":2800001,"C":302114},
    "scope":"The local data are supplied. Quantifiers and ring uniformity are proved. The bundled AdmB/AdmT premises are bypassed by direct constructions.",
    "local_Type_II":"EA9 is unchanged: ConclusionE under literal Hyps for C>=4129, cloud tuple(10,54,1088).",
    "remaining_inputs":REMAINS,
}
ledger={
    **{k:deepcopy(v) for k,v in old.items() if k not in ["claims","source_files","component_input_boundaries"]},
    "artifact_version":"0.10","predecessor_version":"0.9","date":"2026-11-21",
    "scope":"Partial human RH/Dirichlet-GRH reconstruction. Both complete local Type-I and Type-II constructions are proved under literal supplied hypotheses; global arithmetic, spectral, metric and cohomological work remains.",
    "claims":claims,"source_files":[files[k] for k in sorted(files)],
    "new_component_ledgers":[c+"/provenance.json" for c,*_ in COMPONENTS],
    "component_input_boundaries":boundaries,
    "component_input_boundaries_history":deepcopy(old.get("component_input_boundaries_history",[]))+[{"version":"0.9","boundaries":old["component_input_boundaries"]}],
    "component_scope_metadata_as_received":new_scopes,
    "dependency_convention":"Explicit mathematical premises; historical closure annotations are not reverse proof edges. The historical graph, including EA9->CP8, is preserved. This is not a Lean transitive dependency audit.",
    "mathematical_dependency_graph":graph,"dependency_topological_order":topo,
    "version_0_10_local_conclusions":conclusion,
    "merge_inputs_history":deepcopy(old.get("merge_inputs_history",[]))+[{"version":"0.9","inputs":old.get("merge_inputs",{})}],
    "merge_inputs":{
        "predecessor":{"path":str(OLD_PATH.relative_to(BASE)),"sha256":digest(old_bytes)},
        "components":component_inputs,"component_artifacts":artifact_inputs,
        "integrated_main":{"path":str(MAIN_PATH.relative_to(BASE)),"sha256":digest(main_raw)},
        "merger":{"path":str(Path(__file__).resolve().relative_to(BASE)),"sha256":digest(Path(__file__).read_bytes())},
    },
    "validation":validation,
}
lines=[
    "RH AND DIRICHLET-GRH READABLE RECONSTRUCTION — SOURCE LEDGER v0.10","Pinned commit: "+PIN,
    "Read version_0_10_update for completed local Type-I applications; historical fields and source arrays are preserved.",
    f"{counts['claims']} stable claims; {counts['source_links']} source links; {counts['source_files']} primary files.",
    "53 new claims: RU11 + RD15 + HM12 + NP9 + TC6.",
    complete,"No full RH/Dirichlet-GRH proof, Lean build or kernel replay is asserted.","",
]
fields=["statement","claims","hypotheses","assumptions","supplied_data_scope","remaining_inputs","separate_remaining_work",
        "actual_application","discharged_by","depends_on","dependencies","source_relation","proof_location","expanded_notes","merged_application"]
fields += [f"version_0_{i}_update" for i in range(3,11)]
for c in claims:
    lines += [c["id"]+" — "+c["title"],"Historical/component status: "+c["status"]]
    for key in fields:
        if key in c:
            value=c[key] if isinstance(c[key],str) else json.dumps(c[key],ensure_ascii=False)
            lines.append(key.replace("_"," ").capitalize()+": "+value)
    for i,r in enumerate(c["sources"],1):
        lines += [f"  [{i}] {r['path']}:{r['line_start']}–{r['line_end']}","      "+r["declaration"],
                  "      "+r["url"],"      File SHA-256 "+r["sha256"],"      Range SHA-256 "+r["range_sha256"]]
    lines.append("")
OUT.mkdir(parents=True,exist_ok=True)
(OUT/"provenance.json").write_text(json.dumps(ledger,indent=2,ensure_ascii=False)+"\n")
(OUT/"provenance.txt").write_text("\n".join(lines)+"\n")
(OUT/"source_index.json").write_text(json.dumps({"commit":PIN,"artifact_version":"0.10","source_files":ledger["source_files"]},indent=2,ensure_ascii=False)+"\n")
print(json.dumps(validation,indent=2))

