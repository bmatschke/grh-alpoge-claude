#!/usr/bin/env python3
"""Read-only verification of the already-built RCV component and its dependencies."""
from pathlib import Path
import hashlib
import json

HERE = Path(__file__).resolve().parent
WORK = HERE.parent

def sha(data):
    return hashlib.sha256(data).hexdigest()

def read_json(path):
    return json.loads(path.read_text())

provenance = read_json(HERE / "provenance.json")
main = (HERE / "main.tex").read_bytes()
main_hash = sha(main)
assert provenance["proof_file_sha256"] == main_hash
assert provenance["main_tex_sha256"] == main_hash
assert len(provenance["claims"]) == 25
assert [c["id"] for c in provenance["claims"]] == [f"RCV{i}" for i in range(1, 26)]
proofs = {}
for claim in provenance["claims"]:
    loc = claim["proof_location"]
    assert loc["file"] == HERE.name + "/main.tex"
    data = (WORK / loc["file"]).read_bytes().splitlines(keepends=True)
    selected = b"".join(data[loc["line_start"] - 1:loc["line_end"]])
    assert loc["sha256"] == sha(selected), claim["id"]
    assert loc["bytes"] == len(selected), claim["id"]
    assert selected.startswith(("% BEGIN " + claim["id"]).encode())
    assert selected.rstrip().endswith(("% END " + claim["id"]).encode())
    proofs[claim["id"]] = loc["sha256"]
manifest = read_json(HERE / "source_manifest.json")
assert manifest["source_commit"] == provenance["source_commit"]
file_index = {f["path"]: f for f in manifest["source_files"]}
for file in file_index.values():
    data = (WORK / file["snapshot_path"]).read_bytes()
    assert file["sha256"] == sha(data), file["path"]
    assert file["bytes"] == len(data), file["path"]
    assert file["line_count"] == len(data.splitlines(keepends=True)), file["path"]
ranges = set()
for entries in provenance["source_groups"].values():
    for entry in entries:
        file = file_index[entry["path"]]
        lines = (WORK / file["snapshot_path"]).read_bytes().splitlines(keepends=True)
        selected = b"".join(lines[entry["line_start"] - 1:entry["line_end"]])
        assert entry["file_sha256"] == file["sha256"], entry["id"]
        assert entry["range_sha256"] == sha(selected), entry["id"]
        assert entry["range_bytes"] == len(selected), entry["id"]
        ranges.add((entry["path"], entry["line_start"], entry["line_end"]))
assert manifest["total_files"] == len(file_index)
assert manifest["total_bytes"] == sum(f["bytes"] for f in file_index.values())
assert manifest["distinct_source_ranges"] == len(ranges)
inherited_ids = set()
inherited = read_json(HERE / "inherited_inputs.json")
for component in inherited["components"]:
    data = (WORK / component["file"]).read_bytes()
    assert sha(data) == component["sha256"], component["component"]
    lines = data.splitlines(keepends=True)
    for binding in component["claim_bindings"]:
        selected = b"".join(lines[binding["line_start"] - 1:binding["line_end"]])
        assert sha(selected) == binding["sha256"], binding["id"]
        assert len(selected) == binding["bytes"], binding["id"]
        inherited_ids.add(binding["id"])
known = set(proofs) | inherited_ids
index = {c["id"]: c for c in provenance["claims"]}
for claim in index.values():
    assert all(dep in known for dep in claim["depends_on"]), claim["id"]
done = set(inherited_ids)
visiting = set()
def visit(identifier):
    if identifier in done:
        return
    assert identifier not in visiting, ("cycle", identifier)
    visiting.add(identifier)
    for dependency in index[identifier]["depends_on"]:
        visit(dependency)
    visiting.remove(identifier)
    done.add(identifier)
for identifier in index:
    visit(identifier)
for name in ["contracts.json", "closure.json", "claim_dag.json", "tex_validation.json", "inherited_inputs.json"]:
    assert read_json(HERE / name)["proof_file_sha256"] == main_hash, name
assert read_json(HERE / "tex_validation.json")["status"] == "PASS"
reviews = []
for path in HERE.glob("independent_review*.json"):
    review = read_json(path)
    bound = review.get("proof_file_sha256", review.get("main_tex_sha256"))
    if bound:
        assert bound == main_hash, path.name
    for identifier, value in review.get("proof_hashes", {}).items():
        assert value == proofs[identifier], (path.name, identifier)
    reviews.append(path.name)
print(json.dumps({
    "status": "PASS", "component": HERE.name, "main_sha256": main_hash,
    "claims": len(proofs), "source_files": len(file_index),
    "source_ranges": len(ranges), "inherited_claim_bindings": len(inherited_ids),
    "all_dependency_ids_resolve": True, "local_dag_acyclic": True,
    "independent_review_files_checked": reviews,
    "no_mutation": True, "no_lean_replay": True,
}, indent=2))
