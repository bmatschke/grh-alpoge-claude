"""Merge v0.8 proof ledgers without rewriting any earlier source array.

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
OUT = BASE / "output/RH_reconstruction_v0_8"
OLD_PATH = BASE / "output/RH_reconstruction_v0_7/provenance.json"
MAIN_PATH = BASE / "output/pdf/RH_readable_reconstruction_v0_8.tex"
PIN = "7cbf7a0c32fca1badf05931879a37c3f8a2b03b4"
URL = "https://github.com/CocoSgt/riemann-hypothesis-lean/blob/" + PIN + "/"
COMPONENTS = [
    ("frame_geometry", "FG", 8),
    ("outgoing_realization", "OR", 8),
    ("cloud_parameters", "CP", 8),
    ("edge_assembly", "EA", 9),
    ("type_one", "TI", 9),
]

def digest(raw):
    return hashlib.sha256(raw).hexdigest()

old_bytes = OLD_PATH.read_bytes()
old = json.loads(old_bytes)
assert old["commit"] == PIN
assert old["artifact_version"] == "0.7"
assert len(old["claims"]) == 231
assert len(old["source_files"]) == 534
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

# Historical claim content remains unchanged. A current reader should apply
# version_0_8_update, while the original status and exact source array remain
# independently reviewable. Closure annotations are not proof-premise edges.
TYPE_II_CLOSURE = (
    "FG constructs the actual periodic frames from the literal supplied orbit data; "
    "OR proves the actual outgoing separated realization for C>=100; CP supplies "
    "the compatible local parameters and CloudStep(C,10,54,1088) for C>=4129; "
    "EA assembles the complete local Type-II ConclusionE under its literal hypotheses "
    "for C>=4129. This does not assert global abundance or simultaneous global "
    "supply of those arithmetic/orbit hypotheses."
)
GLOBAL_REMAINS = [
    "Global arithmetic/orbit abundance, simultaneous prime and host-field selection, and the full cohomological window inputs.",
    "The separately identified global theta/spectral, geometric and metric comparison inputs.",
    "Complete rank-one Type-I construction and averaged exceptional bound; TI1-TI5 reconstruct its polynomial/arithmetic mechanism, while TI6-TI8 retain explicit inputs and TI9 records the remaining bridges.",
]
UPDATES = {
    "SY8": ("local_Type_II_frontier_closed_under_literal_hypotheses", TYPE_II_CLOSURE + " The separate Type-I construction remains TI9."),
    "CL2": ("actual_application_inputs_now_supplied", "The original complementary ratio proof is unchanged. RK3 supplies selected-symbol density, EA1-EA2 supply exact numerical compatibility, and CP/EA now complete the full local Type-II application under literal hypotheses."),
    "CL3": ("actual_application_inputs_now_supplied", "The original primitive-array detector is unchanged. RK3 supplies its actual-generator summand; CB supplies the integral complementary model; FG/CP/EA supply the actual local data and complete the application."),
    "CL6": ("actual_application_inputs_now_supplied", "The original four-L comparison cost is unchanged. Its actual integral model and local parameter application are supplied by IW/CB and CP/EA; the contraction scalar is integral and need not be a unit."),
    "CL9": ("actual_application_inputs_now_supplied", "The 49L and 50L valuation conclusions are unchanged. CP1-CP5 now verify the numerical frame, spread, size and word/Gram hypotheses for the actual local family; OR closes the distinct outgoing realization used by CP7."),
    "CL10": ("actual_outgoing_realization_premise_now_discharged", "The conditional perturbation and scalar lemma is unchanged. Ordinary source-symbol realization did not by itself give the outgoing RealAt premise: OR1-OR8 now prove the actual one-sided integral lift, and CP7 supplies its normalized dual identification and quantitative error. Thus this distinct actual realization premise is now discharged under the literal local Type-II hypotheses."),
    "CL11": ("actual_cloud_and_local_Type_II_application_proved", "The denominator constant 54 is realized by CP8 in actual CloudStep(C,10,54,1088) for C>=4129; the extra four-L contraction cost is retained. EA then proves ConclusionE under literal local hypotheses."),
    "CL12": ("historical_complete_local_Type_II_frontier_discharged", TYPE_II_CLOSURE),
    "WT9": ("incoming_interface_and_local_parameter_application_closed", "IN9 supplies the actual initial-symbol membership and WT9 its exact word transport. CP1-CP5 now construct the compatible actual Type-II data and verify the numerical application; global arithmetic data supply remains separate."),
    "DT11": ("incoming_and_full_local_parameter_application_closed", "The IN/WT incoming proof and its C>=16 word threshold are unchanged. FG/CP/EA now close the actual local frame and parameter application, while OR proves the different outgoing one-sided construction. The full local Type-II threshold is 4129."),
    "SD8": ("selected_symbol_theorem_applied_to_actual_Type_II_data", "The earlier complete local selected-symbol theorem with witnesses 1088,1,10 is unchanged. FG and EA1-EA2 now match its literal Dat.Hyp to the actual Type-II inputs. CP8 and EA9 complete the local construction under those inputs; global orbit abundance and Type I remain separate."),
    "CG9": ("coarse_congruence_with_actual_Type_II_application_closed", "The reconstructed integral coarse-to-fine congruence is unchanged. FG, EA1-EA2 and CP now verify its actual local application; no global arithmetic/orbit-abundance conclusion is added."),
    "RK1": ("coarse_rank_with_actual_Type_II_application_closed", "The complete coarse residue-rank theorem is unchanged. FG/EA1-EA2/CP provide its compatible actual local Type-II data under the literal input hypotheses."),
    "RK2": ("rank_transfer_with_actual_Type_II_application_closed", "The actual-generator rank transfer is unchanged. The previously separate local parameter compatibility is now supplied by FG/EA1-EA2/CP."),
    "RK3": ("selected_symbol_theorem_with_actual_Type_II_application_closed", "All selected-symbol clauses with witnesses 1088,1,10 remain proved. EA1-EA2 verify their exact application under Type-II inputs, and CP8 plus EA9 establish full local ConclusionE for C>=4129. This is not global parameter existence."),
    "JR9": ("full_local_Type_II_ConclusionE_proved_under_literal_hypotheses", TYPE_II_CLOSURE),
    "JR10": ("Type_I_partial_mechanism_reconstructed_full_branch_remaining", "TI1-TI2 identify and prove the actual factorial block-lattice primitive-test mechanism; TI3-TI5 prove exact gamma degree/leading form, GamInt and p-adic polynomial-matrix averaging. TI6-TI8 prove conditional one-tie and final transfer steps with all missing inputs explicit. Restricted graded Gram, simultaneous partners, weighted block density, actual paired lifts and full Type-I parameter supply remain TI9."),
}
closure_ids = [f"{prefix}{i}" for _name, prefix, count in COMPONENTS[:4] for i in range(1, count+1)]
for c in claims:
    cid = c["id"]
    if cid not in UPDATES:
        continue
    prior = {k: deepcopy(v) for k, v in c.items()
             if k not in {"sources", "version_history"} and not k.startswith("version_")}
    c.setdefault("version_history", []).append({"version": "0.7", **prior})
    status, explanation = UPDATES[cid]
    discharged_by = closure_ids
    if cid == "JR10":
        discharged_by = [f"TI{i}" for i in range(1, 10)]
    elif cid == "CL10":
        discharged_by = [f"OR{i}" for i in range(1, 9)] + ["CP7"]
    c["version_0_8_update"] = {
        "status": status, "explanation": explanation,
        "discharged_by": discharged_by,
        "separate_remaining_work": GLOBAL_REMAINS,
        "scope": "Human reconstruction under the literal local hypotheses; no global abundance or full RH/GRH proof assertion.",
    }

component_inputs = []
artifact_inputs = []
new_counts = {}
new_component_scopes = {}
for component, prefix, expected_count in COMPONENTS:
    relative = component + "/provenance.json"
    ledger_path = BASE / "v0_8" / relative
    data_raw = ledger_path.read_bytes()
    data = json.loads(data_raw)
    repository = data.get("repository")
    pin = data.get("commit", data.get("source_commit"))
    if pin is None and isinstance(repository, dict):
        pin = repository.get("commit")
    assert pin == PIN, (component, "component pin")
    assert data.get("artifact_version", "0.8") == "0.8"
    expected_ids = {f"{prefix}{i}" for i in range(1, expected_count+1)}
    assert {c["id"] for c in data["claims"]} == expected_ids
    component_inputs.append({"path": "v0_8/" + relative, "sha256": digest(data_raw), "claims": expected_count})
    new_counts[prefix] = expected_count
    new_component_scopes[prefix] = {
        key: deepcopy(data[key]) for key in ["outside_scope", "scope_note", "shared_companions", "reused_completed_inputs"]
        if key in data
    }
    for s in data.get("source_files", data.get("files", [])):
        path = source_path(s)
        expected = s.get("sha256", s.get("full_file_sha256", s.get("source_sha256")))
        assert expected, (component, path, "missing source-file SHA")
        raw, _sha = file_record(path, expected)
        if "bytes" in s:
            assert s["bytes"] == len(raw), (component, path, "file bytes")
        if "line_count" in s or "lines" in s:
            assert s.get("line_count", s.get("lines")) == len(raw.decode().splitlines()), (component, path, "file lines")
        if "url" in s:
            assert s["url"] == URL + path, (component, path, "file URL")
    component_dir = BASE / "v0_8" / component
    for name, sha in data.get("artifact_sha256", {}).items():
        artifact = component_dir / name
        raw = artifact.read_bytes()
        assert digest(raw) == sha, (component, name, "artifact hash")
        artifact_inputs.append({"path": str(artifact.relative_to(BASE)), "sha256": sha})
    for record in data.get("artifacts", []):
        artifact = component_dir / record["path"]
        raw = artifact.read_bytes()
        assert digest(raw) == record["sha256"], (component, record["path"], "artifact hash")
        if "bytes" in record:
            assert len(raw) == record["bytes"]
        artifact_inputs.append({"path": str(artifact.relative_to(BASE)), "sha256": record["sha256"]})
    for c in data["claims"]:
        n = deepcopy({k: v for k, v in c.items() if k != "sources"})
        if "title" not in n:
            n["title"] = n.pop("result")
        n["introduced_in"] = "0.8"
        n["component_ledger"] = relative
        refs = c.get("sources")
        if refs is None:
            refs = [s for s in data["source_entries"] if s["claim_id"] == c["id"]]
        assert refs, (c["id"], "no source references")
        n["sources"] = [reference(s) for s in refs]
        n.setdefault("proof_location", {
            "file": component + "/" + component + "_section.tex",
            "expanded": component + "/report.txt", "section": c["id"],
        })
        for key in ["proof_location", "expanded_notes"]:
            location = n.get(key)
            if isinstance(location, dict):
                for file_key in ["file", "expanded"]:
                    value = location.get(file_key)
                    if isinstance(value, str):
                        if not value.startswith(component + "/"):
                            value = component + "/" + value
                            location[file_key] = value
                        assert (BASE / "v0_8" / value).is_file(), (c["id"], value)
        if n["id"] in {"CP7", "CP8"}:
            assert not n.get("remaining_inputs"), (n["id"], "outgoing input not yet resolved in component")
            n["resolved_companion_inputs"] = {"actual_outgoing_one_sided_realization": ["OR8"]}
            n["merge_scope_note"] = "OR8 is proved in the same version with threshold100; it is not an open input of the merged actual cloud theorem. CP8 therefore has threshold4129."
        if n["id"] == "EA9":
            n["merged_application"] = {
                "status": "proved_full_local_Type_II_ConclusionE_under_literal_hypotheses",
                "statement": "Apply the conditional EA9 theorem to the actual CP8 CloudStep(C,10,54,1088). Since C>=4129 dominates 10,54,1088 and OR's threshold100, the complete local ConclusionE follows for C>=4129 under the literal supplied orbit, weight, size and coefficient hypotheses.",
                "additional_depends_on": ["CP8"],
                "constants": {"C_lower_bound": 4129, "cloud_Ct0": 10, "cloud_CD1": 54, "cloud_CLa": 1088},
                "separate_remaining_work": GLOBAL_REMAINS,
            }
        if n["id"].startswith("TI"):
            number = int(n["id"][2:])
            n["merged_scope_classification"] = (
                "proved_actual_family_or_elementary_mechanism_with_stated_scope" if number <= 5
                else "proved_conditional_implication_with_explicit_missing_inputs" if number <= 8
                else "remaining_full_Type_I_input_boundary"
            )
            ti_dependencies = {1: [], 2: ["TI1"], 3: [], 4: ["TI3"], 5: [],
                               6: ["TI3", "TI4", "TI5"], 7: [], 8: ["TI7"], 9: []}
            n["depends_on"] = ti_dependencies[number]
            if number in {6, 7, 8, 9}:
                n["remaining_inputs"] = {
                    6: ["The actual restricted graded initial-Gram determinant bound; exact source lattice and basis hypotheses remain explicit."],
                    7: ["Actual KeyIneq and harmonic-model dimension identification, plus numerical density and enlarged-box volume hypotheses."],
                    8: ["Actual enlarged-box mean bound and the stated boundary/cleaning numerical bounds; TI7's inputs remain explicit."],
                    9: ["Restricted graded Gram and simultaneous integral partners.", "Weighted segment/digit-class and terminal-contraction comparison.", "Actual paired lifts into cleaned rank-one edge lattices.", "Harmonic-model passage and complete Type-I numerical parameter supply."],
                }[number]
        claims.append(n)

ids = [c["id"] for c in claims]
assert len(ids) == len(set(ids)) == 273
assert sum(new_counts.values()) == 42
assert set(old_claims) <= set(ids)
by_id = {c["id"]: c for c in claims}

def stable_ids(value):
    if isinstance(value, str):
        return [value] if re.fullmatch(r"[A-Z]+[0-9]+", value) else []
    if isinstance(value, list):
        return [x for item in value for x in stable_ids(item)]
    if isinstance(value, dict):
        return [x for item in value.values() for x in stable_ids(item)]
    return []

for c in claims:
    if c["id"] in old_claims:
        prior = old_claims[c["id"]]
        assert c["sources"] == prior["sources"], (c["id"], "historical source array changed")
        for key, value in prior.items():
            if key == "version_history":
                assert c.get(key, [])[:len(value)] == value, (c["id"], "historical status history changed")
            else:
                assert c[key] == value, (c["id"], key, "historical claim content changed")
        assert set(c) - set(prior) <= {"version_0_8_update", "version_history"}
    for key in ["depends_on", "dependencies", "discharged_by", "resolved_companion_inputs"]:
        for item in stable_ids(c.get(key, [])):
            assert item in by_id, (c["id"], key, item, "unknown stable ID")
    for item in stable_ids(c.get("merged_application", {}).get("additional_depends_on", [])):
        assert item in by_id, (c["id"], item, "unknown application dependency")

# Proof-premise edges and historical discharge annotations have distinct roles.
# In particular CL12 remains a historical boundary record, not a new theorem
# inserted upstream of the lemmas that the actual cloud construction uses.
graph = {c["id"]: list(dict.fromkeys(stable_ids(c.get("depends_on", c.get("dependencies", []))))) for c in claims}
graph["EA9"] = list(dict.fromkeys(graph["EA9"] + ["CP8"]))
assert {"EA1", "EA2"} <= set(graph["CP6"]), "CP6 must retain the actual RK-compatibility inputs"
assert "OR8" in graph["CP7"], "The actual outgoing realization must be a CP7 proof premise"
state, trail, topo = {}, [], []

def visit(cid):
    if state.get(cid) == 2:
        return
    assert state.get(cid) != 1, ("proof dependency cycle", trail[trail.index(cid):] + [cid])
    state[cid] = 1
    trail.append(cid)
    for dep in graph[cid]:
        assert dep in by_id, (cid, dep, "unknown graph node")
        visit(dep)
    trail.pop()
    state[cid] = 2
    topo.append(cid)

for cid in ids:
    visit(cid)

def ancestors(cid):
    found = set()
    todo = list(graph[cid])
    while todo:
        dep = todo.pop()
        if dep not in found:
            found.add(dep)
            todo.extend(graph[dep])
    return found

for cid in ["EA1", "EA2"]:
    assert not {"CP8", "EA9"} & ancestors(cid), (cid, "circular parameter compatibility")

main_raw = MAIN_PATH.read_bytes()
bibliography = {"src/" + x for x in re.findall(r"\\src\{([^{}]+)\}", main_raw.decode())}
assert bibliography, "No main bibliography source references found"
for path in bibliography:
    file_record(path, role="Additional bibliography source in the integrated v0.8 document.")
for path, source in old_files.items():
    assert files[path] == source, (path, "historical source-file record changed")
assert OLD_PATH.read_bytes() == old_bytes, "The predecessor ledger changed during the merge"
for item in component_inputs + artifact_inputs:
    assert digest((BASE / item["path"]).read_bytes()) == item["sha256"], (item["path"], "input changed during merge")
assert MAIN_PATH.read_bytes() == main_raw, "The integrated main changed during the merge"

boundaries = {
    **deepcopy(old.get("component_input_boundaries", {})),
    "SY": "Integral ordinary source realization and outgoing one-sided realization are now supplied by IP/SY and OR respectively. FG/CP/EA complete the actual local Type-II application. Separate Type I and global arithmetic supply remain.",
    "CL": "All actual Type-II frame, numerical, outgoing, incoming, primitive-cloud and denominator hypotheses are now supplied by FG/OR/CP with the prior IW/CB/IN/WT/PG/DT/RK results. EA completes local ConclusionE for C>=4129, under literal input hypotheses.",
    "DT": "The actual incoming construction and normal/Gram test were already proved; FG/CP now supply their numerical local data and OR supplies the separate outgoing one-sided realization. No full global arithmetic supply is asserted.",
    "WT": "IN/WT prove actual incoming membership, and CP supplies its compatible local Type-II data. Global simultaneous family supply remains separate.",
    "SD": "All selected-symbol density and degree clauses remain proved with witnesses1088,1,10. FG and EA1-EA2 now match the actual Type-II frame and numerical hypotheses; the full local application is closed by CP8/EA9.",
    "CG": "Actual coarse congruence is proved and its local Type-II parameter matching is now supplied by FG/EA/CP. It does not prove global orbit abundance.",
    "RK": "The selected-symbol theorem with constants1088,1,10 is applied to actual local Type-II data via FG/EA1-EA2. CP8 and EA9 give full local ConclusionE for C>=4129 under literal hypotheses. Separate Type I and global arithmetic windows remain.",
    "JR": "The complete local Type-II single-edge and many-edge assembly is now reconstructed under literal hypotheses by FG/OR/CP/EA, with threshold4129 and cloud constants10,54,1088. Type I and global arithmetic/analytic constructions remain distinct.",
    "PG": "The constrained Gram construction and actual incoming membership are proved; CP now supplies their numerical local Type-II data. This does not assert global abundance or the complete RH/GRH theorem.",
    "FG": "The literal good-orbit data produce the required periodic valid frames, chain geometry and cardinality bounds. CP/EA supply their downstream local parameter compatibility in this version. Abundance of suitable global orbit data remains separate.",
    "OR": "Generic determinant divisibility, integral quotient extraction, exact RestPh and finite correction give the actual outgoing one-sided realization for C>=100. It is a completed input to CP7 in this version.",
    "CP": "The actual local data, constrained tests, outgoing/incoming compatibility and primitive cloud are constructed under literal Type-II hypotheses; CloudStep(C,10,54,1088) holds for C>=4129. OR is fully resolved by OR8.",
    "EA": "The exact local rank, source realization, lattice comparison, finite-field edge count and primitive tests yield ConclusionE for C>=4129 after inserting CP8 into EA9. EA1-EA2 parameter compatibility is independent of CP8 and is used by CP6.",
    "TI": "TI1-TI5 prove the actual polynomial/lattice and p-adic averaging mechanism. TI6-TI8 are proved conditional implications with restricted graded Gram, weighted dimension, numerical and mean inputs explicit. TI9 records the still-incomplete full rank-one Type-I construction.",
}
counts = {
    "claims": len(claims), "new_claims": 42, "new_claims_by_prefix": new_counts,
    "source_links": sum(len(c["sources"]) for c in claims),
    "old_source_links_preserved": sum(len(c["sources"]) for c in old["claims"]),
    "new_source_links": sum(len(c["sources"]) for c in claims if c["id"] not in old_claims),
    "source_files": len(files), "old_source_files_preserved": len(old_files),
    "new_source_files": len(files) - len(old_files),
    "unique_source_ranges": len(validated_ranges), "main_bibliography_paths": len(bibliography),
    "explicit_dependency_edges": sum(map(len, graph.values())),
    "historical_claim_status_updates": len(UPDATES),
}
validation = {
    **counts,
    "all_file_and_range_hashes_validated": True,
    "all_named_or_focus_anchors_validated": True,
    "anchor_validation_methods_per_link": anchor_methods,
    "all_source_bytes_equal_pinned_git_blobs": True,
    "all_prior_source_arrays_exactly_preserved": True,
    "all_prior_source_file_records_exactly_preserved": True,
    "all_prior_claim_fields_preserved_except_appended_version_annotations": True,
    "all_prior_ids_preserved": True,
    "all_main_bibliography_paths_in_source_index": True,
    "all_explicit_dependency_ids_resolve": True,
    "explicit_mathematical_dependency_graph_acyclic": True,
    "EA1_EA2_independent_of_CP8_and_EA9": True,
    "CP6_keeps_EA1_EA2_dependencies": True,
    "CP7_outgoing_dependency_resolved_by_OR8": True,
    "EA9_merged_application_uses_CP8": True,
    "component_artifact_hashes_validated_when_supplied": True,
    "no_lean_build_or_kernel_replay": True,
}
ledger = {
    **{k: deepcopy(v) for k, v in old.items() if k not in ["claims", "source_files", "component_input_boundaries"]},
    "artifact_version": "0.8", "predecessor_version": "0.7", "date": "2026-11-21",
    "scope": "Human-readable partial RH/Dirichlet-GRH reconstruction; local Type II closed under literal hypotheses, Type I and global inputs still incomplete.",
    "claims": claims, "source_files": [files[k] for k in sorted(files)],
    "new_component_ledgers": [name + "/provenance.json" for name, _p, _n in COMPONENTS],
    "component_input_boundaries": boundaries,
    "component_input_boundaries_history": deepcopy(old.get("component_input_boundaries_history", [])) + [
        {"version": "0.7", "boundaries": deepcopy(old.get("component_input_boundaries", {}))}
    ],
    "component_scope_metadata_as_received": new_component_scopes,
    "dependency_convention": "Edges record explicit mathematical proof premises and the additional EA9 application of CP8. Historical discharged_by/version updates are closure annotations, not reverse proof-premise edges. Historical boundary records remain unchanged. This does not assert a Lean transitive dependency audit.",
    "mathematical_dependency_graph": graph,
    "dependency_topological_order": topo,
    "version_0_8_local_conclusion": {
        "claim": "EA9", "cloud_input": "CP8", "C_lower_bound": 4129,
        "cloud_constants": [10, 54, 1088], "outgoing_threshold": 100,
        "scope": "Complete local Type-II ConclusionE under its literal supplied hypotheses.",
        "remaining_global_and_Type_I_inputs": GLOBAL_REMAINS,
    },
    "merge_inputs_history": deepcopy(old.get("merge_inputs_history", [])) + [
        {"version": "0.7", "inputs": deepcopy(old.get("merge_inputs", {}))}
    ],
    "merge_inputs": {
        "predecessor": {"path": str(OLD_PATH.relative_to(BASE)), "sha256": digest(old_bytes)},
        "components": component_inputs,
        "component_artifacts": artifact_inputs,
        "integrated_main": {"path": str(MAIN_PATH.relative_to(BASE)), "sha256": digest(main_raw)},
        "merger": {"path": str(Path(__file__).resolve().relative_to(BASE)), "sha256": digest(Path(__file__).read_bytes())},
    },
    "validation": validation,
}
text_lines = [
    "RH AND DIRICHLET-GRH READABLE RECONSTRUCTION — SOURCE LEDGER v0.8",
    "Pinned commit: " + PIN,
    "Every historical claim field, source array and source-file record is preserved; only version-update/history annotations are appended.",
    "Read version_0_8_update for current historical-claim status. Earlier status fields remain verbatim historical records.",
    f"{counts['claims']} stable claims; {counts['source_links']} source links; {counts['source_files']} primary source files.",
    "42 new claims: FG8 + OR8 + CP8 + EA9 + TI9.",
    "Complete local Type-II ConclusionE is human-proved under literal hypotheses for C>=4129, using CloudStep constants10,54,1088.",
    "TI1-TI5 reconstruct actual polynomial/arithmetic mechanisms; TI6-TI8 retain explicit inputs; full Type I and global arithmetic windows remain.",
    "All source bytes match pinned Git blobs. Inclusive range hashes, anchors, stable-ID dependencies and acyclicity are validated.",
    "This is provenance validation, not Lean elaboration, kernel replay or a full formal dependency audit.", "",
]
fields = [
    "statement", "claims", "hypotheses", "assumptions", "supplied_data_scope", "remaining_inputs",
    "separate_remaining_work", "actual_application", "discharged_by", "depends_on", "source_relation",
    "proof_location", "expanded_notes", "component_scope_remaining_inputs", "resolved_companion_inputs",
    "merge_scope_note", "merged_scope_classification", "merged_application",
    "version_0_3_update", "version_0_4_update", "version_0_5_update", "version_0_6_update", "version_0_7_update", "version_0_8_update",
]
for c in claims:
    text_lines += [c["id"] + " — " + c["title"], "Historical/component status: " + c["status"]]
    for field in fields:
        if field in c:
            value = c[field] if isinstance(c[field], str) else json.dumps(c[field], ensure_ascii=False)
            text_lines.append(field.replace("_", " ").capitalize() + ": " + value)
    for i, source in enumerate(c["sources"], 1):
        text_lines.extend([
            f"  [{i}] {source['path']}:{source['line_start']}–{source['line_end']}",
            "      " + source["declaration"], "      " + source["url"],
            "      File SHA-256 " + source["sha256"],
            "      Range SHA-256 " + source["range_sha256"],
        ])
    text_lines.append("")
text_lines += ["VALIDATION", json.dumps(validation, ensure_ascii=False, indent=2), ""]
outputs = {
    "provenance.json": json.dumps(ledger, ensure_ascii=False, indent=2) + "\n",
    "source_index.json": json.dumps({"commit": PIN, "artifact_version": "0.8", "source_files": ledger["source_files"]}, ensure_ascii=False, indent=2) + "\n",
    "provenance.txt": "\n".join(text_lines) + "\n",
}
OUT.mkdir(parents=True, exist_ok=True)
for name, contents in outputs.items():
    temporary = OUT / (name + ".tmp")
    temporary.write_text(contents)
    temporary.replace(OUT / name)
written = json.loads((OUT / "provenance.json").read_text())
written_claims = {c["id"]: c for c in written["claims"]}
written_files = {s["path"]: s for s in written["source_files"]}
assert all(written_claims[cid]["sources"] == c["sources"] for cid, c in old_claims.items())
assert all(written_files[path] == record for path, record in old_files.items())
for cid, prior in old_claims.items():
    for key, value in prior.items():
        if key != "version_history":
            assert written_claims[cid][key] == value
        else:
            assert written_claims[cid].get(key, [])[:len(value)] == value
print(json.dumps(validation, ensure_ascii=False, indent=2))

