"""Merge v0.9 proof ledgers without rewriting any earlier source array.

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
OUT = BASE / "output/RH_reconstruction_v0_9"
OLD_PATH = BASE / "output/RH_reconstruction_v0_8/provenance.json"
MAIN_PATH = BASE / "output/pdf/RH_readable_reconstruction_v0_9.tex"
PIN = "7cbf7a0c32fca1badf05931879a37c3f8a2b03b4"
URL = "https://github.com/CocoSgt/riemann-hypothesis-lean/blob/" + PIN + "/"
COMPONENTS = [
    ("graded_gram", "GG", 1, 8, "graded_gram_section.tex"),
    ("tie_partners", "TP", 1, 11, "main.tex"),
    ("segment_weighted", "SW", 1, 11, "segment_weighted_section.tex"),
    ("segment_numerics", "SW", 12, 12, "main.tex"),
    ("paired_lifts", "RL", 1, 11, "paired_lifts_section.tex"),
]

def digest(raw):
    return hashlib.sha256(raw).hexdigest()

old_bytes = OLD_PATH.read_bytes()
old = json.loads(old_bytes)
assert old["commit"] == PIN
assert old["artifact_version"] == "0.8"
assert len(old["claims"]) == 273
assert len(old["source_files"]) == 598
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

# Keep historical claims verbatim; append only current boundary annotations.
REMAINS = [
    "Actual coarse rank-on-digits upper and lower bounds; harmonic-model dimensions and the KeyIneq application.",
    "The full admissible Type-I numerical package, its quantifier order, t0<=tI, and the final exceptional-function application.",
    "Global arithmetic/orbit abundance, simultaneous prime/host selection, cohomological windows, and the remaining theta/spectral/metric comparisons.",
]
UPDATES = {
    "TI2": ("actual_paired_lift_input_now_constructed_under_literal_Std", "The original Smith and block-lattice proof is unchanged. RL11 now constructs the actual PairLiftAt maps into CCe and CCe' at height floor(t0), using SW12 and explicit standard hypotheses. This does not supply the remaining rank/density or uniform parameter comparisons.", ["RL11", "SW12"]),
    "TI4": ("sharper_source_GamIntC_now_proved", "The original valid GamInt bound is preserved. TP2 proves the sharper exact GamIntC exponent ((K+4)r+6) floor(log_p(S+o+r)); the final weighted mean uses this sharper proof.", ["TP2"]),
    "TI6": ("restricted_graded_Gram_input_discharged_and_exact_mean_proved", "GG7 proves the actual coefficient-image lattice Gram determinant bound; GG8 supplies the exact segment constant. TP3 proves the source's sharpened one-tie mean with rounding included. TI6's original conditional estimate remains unchanged as a historical result.", ["GG7", "GG8", "TP3"]),
    "TI7": ("local_form_and_lift_inputs_advanced_density_inputs_still_explicit", "GG/TP/SW supply the actual form and weighted-mean mechanisms and RL the cleaned paired lifts under their stated inputs. The actual coarse rank comparison, harmonic-model dimension identification, KeyIneq application and uniform density/volume conditions are still required before applying this unchanged translation lemma.", ["TP11", "SW8", "RL11"]),
    "TI8": ("final_translation_unchanged_remaining_inputs_narrowed", "The elementary final kappa translation is unchanged. The earlier Gram, partner and cleaned-lift constructions are now supplied by GG/TP/RL, while the enlarged-box density and numerical boundary/height conditions still remain.", ["TP11", "SW8", "RL11"]),
    "TI9": ("Type_I_frontier_narrowed_to_density_and_full_numeric_assembly", "Actual graded Gram, simultaneous integral partners, exact multiple-tie mean, harmonic block comparison and cleaned paired lifts are reconstructed. SW8 still retains the actual coarse rank inequality, and RL's endpoint is floor(t0) under literal Std. Coarse rank/density, harmonic-model identification, the full numerical package and t0<=tI remain; full Conclusion2 is not asserted.", ["GG7", "GG8", "TP11", "SW8", "SW9", "SW10", "SW12", "RL11"]),
    "JR10": ("rank_one_local_form_and_cleaned_lifts_reconstructed_full_density_remaining", "The Type-I branch now has the actual restricted Gram bound, simultaneous partners and exact mean, harmonic block conversion and cleaned paired maps. The full exceptional-function/density theorem still needs the precise remaining TI9/SW11 inputs. The completed Type-II theorem is unchanged.", ["GG7", "TP11", "SW8", "SW12", "RL11"]),
}
for c in claims:
    if c["id"] not in UPDATES:
        continue
    prior = {k: deepcopy(v) for k, v in c.items()
             if k not in {"sources", "version_history"} and not k.startswith("version_")}
    c.setdefault("version_history", []).append({"version": "0.8", **prior})
    status, explanation, discharged = UPDATES[c["id"]]
    c["version_0_9_update"] = {
        "status": status, "explanation": explanation,
        "discharged_by": discharged, "separate_remaining_work": REMAINS,
        "scope": "Human reconstruction under the stated local hypotheses; no complete Type-I, global parameter-existence or RH/GRH proof assertion.",
    }

component_inputs, artifact_inputs = [], []
new_counts, new_scopes = {}, {}
for component, prefix, first, last, texname in COMPONENTS:
    relative = component + "/provenance.json"
    directory = BASE / "v0_9" / component
    raw = (directory / "provenance.json").read_bytes()
    data = json.loads(raw)
    repository = data.get("repository")
    pin = data.get("commit", data.get("source_commit"))
    if pin is None and isinstance(repository, dict):
        pin = repository.get("commit")
    assert pin == PIN, (component, "source pin")
    assert data.get("artifact_version", "0.9") == "0.9"
    expected_ids = {f"{prefix}{i}" for i in range(first, last+1)}
    assert {c["id"] for c in data["claims"]} == expected_ids, component
    count = last-first+1
    component_inputs.append({"path": "v0_9/" + relative, "sha256": digest(raw), "claims": count})
    new_counts[prefix] = new_counts.get(prefix, 0) + count
    new_scopes[component] = {key: deepcopy(data[key]) for key in
        ["outside_scope", "scope_note", "shared_companions", "reused_completed_inputs", "independent_reviews"] if key in data}
    for record in data.get("source_files", data.get("files", [])):
        path = source_path(record)
        expected = record.get("sha256", record.get("full_file_sha256", record.get("source_sha256")))
        assert expected
        content, _ = file_record(path, expected)
        if "bytes" in record:
            assert len(content) == record["bytes"]
        if "lines" in record or "line_count" in record:
            assert len(content.decode().splitlines()) == record.get("lines", record.get("line_count"))
        if "url" in record:
            assert record["url"] == URL + path
    records = list(data.get("artifacts", [])) + [
        {"path": name, "sha256": sha} for name, sha in data.get("artifact_sha256", {}).items()
    ]
    for record in records:
        artifact = directory / record["path"]
        content = artifact.read_bytes()
        assert digest(content) == record["sha256"], (component, record["path"], "artifact hash")
        if "bytes" in record:
            assert len(content) == record["bytes"]
        artifact_inputs.append({"path": str(artifact.relative_to(BASE)), "sha256": digest(content)})
    for name in [texname, "report.txt", "build_provenance.py"]:
        artifact = directory / name
        artifact_inputs.append({"path": str(artifact.relative_to(BASE)), "sha256": digest(artifact.read_bytes())})
    for c in data["claims"]:
        n = deepcopy({k: v for k, v in c.items() if k != "sources"})
        if "title" not in n:
            n["title"] = n.pop("result")
        n["introduced_in"] = "0.9"
        n["component_ledger"] = relative
        refs = c.get("sources")
        if refs is None:
            refs = [record for record in data["source_entries"] if record["claim_id"] == c["id"]]
        assert refs
        n["sources"] = [reference(record) for record in refs]
        n.setdefault("proof_location", {"file": texname, "expanded": "report.txt", "section": c["id"]})
        for field in ["proof_location", "expanded_notes"]:
            location = n.get(field)
            if isinstance(location, dict):
                for key in ["file", "expanded"]:
                    value = location.get(key)
                    if isinstance(value, str):
                        if not value.startswith(component + "/"):
                            value = component + "/" + value
                            location[key] = value
                        assert (BASE / "v0_9" / value).is_file(), (c["id"], value)
        claims.append(n)

ids = [c["id"] for c in claims]
assert len(ids) == len(set(ids)) == 315
assert sum(new_counts.values()) == 42
by_id = {c["id"]: c for c in claims}

def stable_ids(value):
    if isinstance(value, str):
        return [value] if re.fullmatch(r"[A-Z]+[0-9]*", value) else []
    if isinstance(value, list):
        return [x for item in value for x in stable_ids(item)]
    if isinstance(value, dict):
        return [x for item in value.values() for x in stable_ids(item)]
    return []

for c in claims:
    if c["id"] in old_claims:
        prior = old_claims[c["id"]]
        assert c["sources"] == prior["sources"]
        for key, value in prior.items():
            if key == "version_history":
                assert c.get(key, [])[:len(value)] == value
            else:
                assert c[key] == value, (c["id"], key, "historical field changed")
        assert set(c) - set(prior) <= {"version_0_9_update", "version_history"}
    for key in ["depends_on", "dependencies", "discharged_by", "resolved_companion_inputs"]:
        for cid in stable_ids(c.get(key, [])):
            assert cid in by_id, (c["id"], key, cid)
    for cid in stable_ids(c.get("version_0_9_update", {}).get("discharged_by", [])):
        assert cid in by_id

graph = {c["id"]: list(dict.fromkeys(stable_ids(c.get("depends_on", c.get("dependencies", []))))) for c in claims}
graph["EA9"] = list(dict.fromkeys(graph["EA9"] + ["CP8"]))
assert {"EA1", "EA2"} <= set(graph["CP6"])
assert "OR8" in graph["CP7"]
state, trail, topo = {}, [], []
def visit(cid):
    if state.get(cid) == 2:
        return
    assert state.get(cid) != 1, ("proof dependency cycle", trail + [cid])
    state[cid] = 1
    trail.append(cid)
    for dep in graph[cid]:
        assert dep in by_id, (cid, dep)
        visit(dep)
    trail.pop()
    state[cid] = 2
    topo.append(cid)
for cid in ids:
    visit(cid)

main_raw = MAIN_PATH.read_bytes()
bibliography = {"src/" + x for x in re.findall(r"\\src\{([^{}]+)\}", main_raw.decode())}
for path in bibliography:
    file_record(path, role="Additional bibliography source in the integrated v0.9 document.")
for path, record in old_files.items():
    assert files[path] == record
assert OLD_PATH.read_bytes() == old_bytes
for item in component_inputs + artifact_inputs:
    assert digest((BASE / item["path"]).read_bytes()) == item["sha256"], (item["path"], "input changed during merge")

boundaries = deepcopy(old["component_input_boundaries"])
boundaries.update({
    "TI": "TI polynomial and transfer lemmas are preserved. GG discharges the actual graded Gram input; TP proves exact sharp integrality and the simultaneous weighted mean; SW proves form and finite-sum mechanisms with its rank input explicit; RL constructs actual cleaned lifts at floor(t0). Coarse rank/density, harmonic-model dimensions and full numerical supply remain.",
    "JR": "The full local Type-II theorem is unchanged. The separate Type-I actual form, partner and lift constructions are now reconstructed, while its coarse rank/density and uniform numerical application remain explicit.",
    "GG": "Actual restricted graded Gram, prefix projections and highest-vector generation are proved via IW and an explicit integral auxiliary action, including the image-lattice saturation cost. No additional local integral representation premise is retained.",
    "TP": "Sharp GamIntC, compatible simultaneous partners and exact TheoremMV7 are reconstructed under the stated admissible signed-chain and size hypotheses, using GG; CM=1.",
    "SW": "Actual SS saturation, harmonic level comparison, ramified good block lattices and terminal Gram averages are proved. Weighted digit-class summation retains coarse rank and the displayed numerical inputs. Literal Std gives the coarse gap, BLk(0), OPlus and order<=t0; universal numerical supply remains separate.",
    "RL": "Actual factorial correction, raw generators, quotient/remainder reblocking, finite cleanup and CCe/CCe' transport are reconstructed under literal Std with CE1,CE2,Cm>=17,Ct>=30. PairLiftAt is proved at floor(t0), not yet at the final tI envelope.",
})
counts = {
    "claims": len(claims), "new_claims": 42, "new_claims_by_prefix": new_counts,
    "source_links": sum(len(c["sources"]) for c in claims),
    "old_source_links_preserved": sum(len(c["sources"]) for c in old["claims"]),
    "new_source_links": sum(len(c["sources"]) for c in claims if c["id"] not in old_claims),
    "source_files": len(files), "old_source_files_preserved": len(old_files),
    "new_source_files": len(files)-len(old_files), "unique_source_ranges": len(validated_ranges),
    "main_bibliography_paths": len(bibliography), "explicit_dependency_edges": sum(map(len, graph.values())),
    "historical_claim_status_updates": len(UPDATES),
}
validation = {
    **counts, "all_file_and_range_hashes_validated": True,
    "all_named_or_focus_anchors_validated": True, "anchor_validation_methods_per_link": anchor_methods,
    "all_source_bytes_equal_pinned_git_blobs": True, "all_prior_source_arrays_exactly_preserved": True,
    "all_prior_source_file_records_exactly_preserved": True,
    "all_prior_claim_fields_preserved_except_appended_version_annotations": True,
    "all_prior_ids_preserved": True, "all_main_bibliography_paths_in_source_index": True,
    "all_explicit_dependency_ids_resolve": True, "explicit_mathematical_dependency_graph_acyclic": True,
    "component_artifact_hashes_validated_when_supplied": True, "no_lean_build_or_kernel_replay": True,
}
ledger = {
    **{k: deepcopy(v) for k,v in old.items() if k not in ["claims", "source_files", "component_input_boundaries"]},
    "artifact_version": "0.9", "predecessor_version": "0.8", "date": "2026-11-21",
    "scope": "Partial human RH/Dirichlet-GRH reconstruction: local Type II complete under literal hypotheses; actual Type-I form, partner and lift mechanisms reconstructed, with density and full numerical supply still explicit.",
    "claims": claims, "source_files": [files[k] for k in sorted(files)],
    "new_component_ledgers": [name+"/provenance.json" for name, *_ in COMPONENTS],
    "component_input_boundaries": boundaries,
    "component_input_boundaries_history": deepcopy(old.get("component_input_boundaries_history", [])) + [{"version": "0.8", "boundaries": old["component_input_boundaries"]}],
    "component_scope_metadata_as_received": new_scopes,
    "dependency_convention": "Edges record explicit mathematical premises, including EA9's application of CP8. Version-update/discharged_by fields are historical closure annotations, not reverse proof edges. This is not a Lean transitive dependency audit.",
    "mathematical_dependency_graph": graph, "dependency_topological_order": topo,
    "version_0_9_local_conclusions": {
        "exact_multitie_mean": "TP11: literal TheoremMV7 with CM=1 under its explicit admissible signed-chain and size bounds.",
        "paired_lift": "RL11: actual PairLiftAt at floor(t0), scalar valuation<=4kappa0, under literal Std and CE1,CE2,Cm>=17,Ct>=30; SW12 supplies block legality and order bound.",
        "weighted_segment": "SW8--SW9: finite weighted-sum and depth bounds, retaining actual coarse rank and explicitly displayed numerical inputs.",
        "remaining_inputs": REMAINS,
    },
    "merge_inputs_history": deepcopy(old.get("merge_inputs_history", [])) + [{"version": "0.8", "inputs": old.get("merge_inputs", {})}],
    "merge_inputs": {
        "predecessor": {"path": str(OLD_PATH.relative_to(BASE)), "sha256": digest(old_bytes)},
        "components": component_inputs, "component_artifacts": artifact_inputs,
        "integrated_main": {"path": str(MAIN_PATH.relative_to(BASE)), "sha256": digest(main_raw)},
        "merger": {"path": str(Path(__file__).resolve().relative_to(BASE)), "sha256": digest(Path(__file__).read_bytes())},
    },
    "validation": validation,
}
lines = [
    "RH AND DIRICHLET-GRH READABLE RECONSTRUCTION — SOURCE LEDGER v0.9", "Pinned commit: "+PIN,
    "All earlier claim fields and source arrays are preserved; read version_0_9_update for the new boundary.",
    f"{counts['claims']} stable claims; {counts['source_links']} source links; {counts['source_files']} primary source files.",
    "42 new claims: GG8 + TP11 + SW12 + RL11.",
    "Actual Type-I Gram, partner, harmonic-block and cleaned-lift mechanisms are proved under their stated inputs.",
    "Coarse rank/density, full numerical supply and global arithmetic remain. No Lean build or kernel replay is claimed.", "",
]
fields = ["statement", "claims", "hypotheses", "assumptions", "supplied_data_scope", "remaining_inputs",
          "separate_remaining_work", "actual_application", "discharged_by", "depends_on", "dependencies", "source_relation",
          "proof_location", "expanded_notes", "merged_application"]
fields += [f"version_0_{i}_update" for i in range(3,10)]
for c in claims:
    lines += [c["id"]+" — "+c["title"], "Historical/component status: "+c["status"]]
    for key in fields:
        if key in c:
            value = c[key] if isinstance(c[key],str) else json.dumps(c[key], ensure_ascii=False)
            lines.append(key.replace("_"," ").capitalize()+": "+value)
    for index, ref in enumerate(c["sources"], 1):
        lines += [f"  [{index}] {ref['path']}:{ref['line_start']}–{ref['line_end']}",
                  "      "+ref["declaration"], "      "+ref["url"],
                  "      File SHA-256 "+ref["sha256"], "      Range SHA-256 "+ref["range_sha256"]]
    lines.append("")
OUT.mkdir(parents=True, exist_ok=True)
(OUT/"provenance.json").write_text(json.dumps(ledger, indent=2, ensure_ascii=False)+"\n")
(OUT/"provenance.txt").write_text("\n".join(lines)+"\n")
(OUT/"source_index.json").write_text(json.dumps({"commit":PIN,"artifact_version":"0.9","source_files":ledger["source_files"]},indent=2,ensure_ascii=False)+"\n")
print(json.dumps(validation, indent=2))

