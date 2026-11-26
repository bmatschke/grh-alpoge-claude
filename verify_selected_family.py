"""Check the selected-family update against the complete numbered dependency graph."""
from functools import cache
from graphlib import TopologicalSorter
from hashlib import sha256
import json
import re
from pathlib import Path


def main():
    root = Path(__file__).resolve().parent
    update = json.loads((root / "SELECTED_FAMILY_CHECKPOINT.json").read_text())
    raw = (root / update["base_graph"]).read_bytes()
    assert sha256(raw).hexdigest() == update["base_graph_sha256"]
    graph = json.loads(raw)
    deps = {row["id"]: row["requires"] for row in graph["nodes"]}
    assert len(deps) == len(graph["nodes"])
    assert all(node in deps for children in deps.values() for node in children)
    list(TopologicalSorter(deps).static_order())

    @cache
    def leaves(node):
        if not deps[node]:
            return {node}
        return set().union(*(leaves(child) for child in deps[node]))

    old_open = {row["id"] for row in graph["nodes"] if row["status"].startswith("open_")}
    assert old_open == set(graph["remaining"])
    proved = update["proved_on_the_original_selected_class"]
    assert proved.keys() <= old_open
    for node, proof in proved.items():
        assert not deps[node] and (root / proof).is_file()
    remaining = old_open - proved.keys()
    assert sorted(remaining) == update["remaining_contracts"]
    roadmap = (root / update["roadmap"]).read_text()
    roadmap_ids = re.findall(r"^\| `([A-Z][A-Z0-9_]+)` \|", roadmap, re.MULTILINE)
    assert sorted(roadmap_ids) == sorted(remaining), "Roadmap disagrees with the graph"
    endpoint_proofs = update["proved_endpoint_assertions_with_broader_work"]
    assert endpoint_proofs.keys() <= remaining
    for node, entry in endpoint_proofs.items():
        assert not deps[node] and (root / entry["proof"]).is_file()
        assert entry["endpoint_statement"] and entry["broader_work"]
        assert all((root / proof).is_file() for proof in entry.get("supporting_proofs", []))
    # Substitution of the selected base square is justified only at this use.
    theta_inputs = {"BASE_THETA_READINGS", "BASE_THETA_RATIONAL_TESTS"}
    base_producer = "SLR_SAME_BUNDLE_BASE_PRODUCER"
    assert theta_inputs <= endpoint_proofs.keys()
    for node in theta_inputs:
        assert {user for user, inputs in deps.items() if node in inputs} == {base_producer}
    assert {user for user, inputs in deps.items() if base_producer in inputs} == {"GLOBAL_SMALL_RANK"}
    missing_at_endpoint = remaining - endpoint_proofs.keys()
    progress = update["progress_within_remaining_inputs"]
    assert progress.keys() == missing_at_endpoint
    for entry in progress.values():
        assert entry["established"] and entry["needed"] and entry["proofs"]
        assert all((root / proof).is_file() for proof in entry["proofs"])
    heights = progress["GLOBAL_PERIOD_HEIGHT"]["height_entry_status"]
    height_groups = (
        heights["proved_on_the_existing_project_inputs"],
        heights["proved_on_selected_class_under_named_hypotheses"],
        heights["remaining"],
    )
    assert sorted(number for group in height_groups for number in group) == list(range(1, 10))
    conditional_proofs = heights["conditional_proofs"]
    assert {int(n) for n in conditional_proofs} == set(height_groups[1])
    assert all((root / proof).is_file() for proof in conditional_proofs.values())
    assert {int(number) for number in heights["partial"]} <= set(heights["remaining"])
    print("Remaining period-height entries:", ", ".join(map(str, heights["remaining"])))
    endpoint_roadmap, divider, _ = roadmap.partition("## Broader reconstruction")
    assert divider, "Roadmap must distinguish endpoint inputs from broader work"
    endpoint_ids = re.findall(r"^\| `([A-Z][A-Z0-9_]+)` \|", endpoint_roadmap, re.MULTILINE)
    assert sorted(endpoint_ids) == sorted(missing_at_endpoint)
    endpoints = update["reachable_open_contracts"]
    assert set(endpoints) == {"ORDINARY_RH", "DIRICHLET_GRH"}
    for endpoint, reported in endpoints.items():
        assert leaves(endpoint) & old_open == set(graph["shared_open_ids"])
        assert sorted(leaves(endpoint) & missing_at_endpoint) == reported
        assert "DESIGN_CHOICES_COMMON" in reported
        print(f"{endpoint} has {len(reported)} remaining endpoint inputs")
    difference = set(endpoints["DIRICHLET_GRH"]) - set(endpoints["ORDINARY_RH"])
    assert sorted(difference) == update["additional_dirichlet_grh_contracts"]
    print(
        f"Checked {len(deps)} nodes, {len(proved)} whole-entry proofs, "
        f"{len(endpoint_proofs)} selected-family endpoint substitution(s), "
        f"and {len(roadmap_ids)} open historical entries"
    )


if __name__ == "__main__":
    main()
