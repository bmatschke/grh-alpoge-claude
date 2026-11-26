"""Independent graph/provenance checks; no Lean replay and no graph edits."""
from pathlib import Path
from collections import Counter
import hashlib
import json
import subprocess

BASE = Path("/workspace/scratch/368c004c3aea")
ROOT = BASE / "reconstruction_v031"
SOURCE = BASE / "lean_source"
GRAPH = ROOT / "dependency_audit_v0_31/obligation_map.json"
PIN = "7cbf7a0c32fca1badf05931879a37c3f8a2b03b4"
COMPONENTS = ["design_existence", "local_theta_dictionary", "small_level_rank", "second_layer_global"]

def sha(data):
    return hashlib.sha256(data).hexdigest()

g = json.loads(GRAPH.read_text())
assert g["source_commit"] == PIN
nodes = {n["id"]: n for n in g["nodes"]}
work = {n["id"]: n for n in g["work_refinement_nodes"]}
optional = {n["id"]: n for n in g["optional_routes"]}
assert len(nodes) == len(g["nodes"])
assert len(work) == len(g["work_refinement_nodes"])
assert len(optional) == len(g["optional_routes"])
assert not (set(nodes) & set(work) or set(nodes) & set(optional) or set(work) & set(optional))

for ident, node in nodes.items():
    assert node["category"] in "ABCD", ident
    assert node["gate"] in ["AND", "LEAF"], ident
    assert bool(node["requires"]) == (node["gate"] == "AND"), ident
    assert all(dep in nodes for dep in node["requires"]), ident

done, active = set(), set()
def visit(ident):
    assert ident not in active, ident
    if ident in done:
        return
    active.add(ident)
    for dep in nodes[ident]["requires"]:
        visit(dep)
    active.remove(ident)
    done.add(ident)
for ident in nodes:
    visit(ident)

def reachable(root):
    seen, todo = set(), [root]
    while todo:
        ident = todo.pop()
        if ident in seen:
            continue
        seen.add(ident)
        todo.extend(nodes[ident]["requires"])
    return seen

rh = reachable("ORDINARY_RH")
grh = reachable("DIRICHLET_GRH")
full = reachable("GLOBAL_FULL_RANK")
assert rh | grh == set(nodes)
assert "COUNT_III_PRODUCER" not in rh
assert "COUNT_III_PRODUCER" in grh
assert {"COUNT_I_PRODUCER", "COUNT_II_SUPPORT", "COUNT_V_PRODUCER"} <= rh & grh
assert not any(n.startswith("TASK_GL4") for n in full)
assert not {"TASK_GL_FINAL_ASSEMBLY", "TASK_LINK_GL_INSTALL", "GLOBAL_GL_PAIR"} & full

all_ids = set(nodes) | set(work) | set(optional)
for edge in g["work_refinement_links"]:
    assert edge["consumer"] in all_ids and edge["dependency"] in all_ids
    assert edge["logical"] is False

source_input_checks = []
for key, item in g["source_inputs"].items():
    p = ROOT / item["file"]
    actual = sha(p.read_bytes())
    assert actual == item["sha256"], key
    source_input_checks.append({"input": key, "file": item["file"], "sha256": actual})

files, ranges, claim_hashes, proof_files = {}, {}, {}, {}
for component in COMPONENTS:
    provenance = json.loads((ROOT / component / "provenance.json").read_text())
    assert provenance.get("commit", provenance.get("source_commit")) == PIN
    main = (ROOT / component / "main.tex").read_bytes()
    main_sha = sha(main)
    assert main_sha == provenance.get("main_tex_sha256", provenance.get("main_sha256")), component
    proof_files[component] = main_sha
    lines = main.splitlines(keepends=True)
    for claim in provenance["claims"]:
        loc = claim["proof_location"]
        text = b"".join(lines[loc["line_start"] - 1 : loc["line_end"]])
        assert sha(text) == loc["sha256"], claim["id"]
        claim_hashes[claim["id"]] = loc["sha256"]
        for s in claim.get("sources", []):
            if not s.get("path", "").startswith("src/"):
                continue
            path = s["path"]
            if path not in files:
                current = (SOURCE / path).read_bytes()
                pinned = subprocess.check_output(["git", "show", PIN + ":" + path], cwd=SOURCE)
                assert current == pinned, path
                files[path] = current
            current = files[path]
            if "range_sha256" not in s:
                continue
            expected = s.get("file_sha256", s.get("sha256"))
            assert sha(current) == expected, path
            excerpt = b"".join(current.splitlines(keepends=True)[s["line_start"] - 1 : s["line_end"]])
            assert sha(excerpt) == s["range_sha256"], (path, s["line_start"])
            ranges[(path, s["line_start"], s["line_end"], s["range_sha256"])] = True

evidence_count = 0
for node in list(nodes.values()) + list(work.values()):
    for ev in node.get("evidence", []):
        if ev.get("component") not in COMPONENTS:
            continue
        assert sha((ROOT / ev["ledger"]).read_bytes()) == ev["ledger_sha256"], node["id"]
        assert sha((ROOT / ev["proof_file"]).read_bytes()) == ev["proof_sha256"], node["id"]
        assert all(c in claim_hashes for c in ev["claims"]), node["id"]
        evidence_count += 1

open_leaves = [n for n in nodes.values() if n["gate"] == "LEAF" and
               n["status"] not in ["proved_in_stated_scope", "published_application_checked"]]
result = {
    "schema": "rh-independent-graph-validation/1",
    "date": "2026-11-22",
    "reviewer": "/root/audit_literature",
    "source_commit": PIN,
    "graph_file": str(GRAPH),
    "graph_sha256": sha(GRAPH.read_bytes()),
    "selected_node_count": len(nodes),
    "work_node_count": len(work),
    "optional_node_count": len(optional),
    "rh_reachable_count": len(rh),
    "grh_reachable_count": len(grh),
    "all_logical_references_valid": True,
    "logical_graph_acyclic": True,
    "all_selected_nodes_reachable": True,
    "refinement_links_explicitly_nonlogical": True,
    "optional_nodes_not_selected": True,
    "count_target_split_preserved": True,
    "full_rank_excludes_GL4_and_final_assembly": True,
    "full_rank_descendants": sorted(full),
    "source_inputs_checked": source_input_checks,
    "component_main_hashes": proof_files,
    "proof_block_hashes": claim_hashes,
    "new_component_evidence_entries_checked": evidence_count,
    "new_component_source_ranges_verified": len(ranges),
    "new_component_source_files_pin_verified": len(files),
    "open_leaf_categories": dict(Counter(n["category"] for n in open_leaves)),
    "new_lean_replay": False,
    "scope_note": "Mechanical and source-integrity checks; the separate signed review states the mathematical and quantifier assessment."
}
out = BASE / "work_v031/reviews/selected_route_graph_validation.json"
out.write_text(json.dumps(result, indent=2) + "\n")
print(json.dumps({k: result[k] for k in [
    "graph_sha256", "selected_node_count", "rh_reachable_count", "grh_reachable_count",
    "new_component_evidence_entries_checked", "new_component_source_ranges_verified",
    "new_component_source_files_pin_verified"
]}, indent=2))
