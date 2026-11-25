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
    endpoints = update["reachable_open_contracts"]
    assert set(endpoints) == {"ORDINARY_RH", "DIRICHLET_GRH"}
    for endpoint, reported in endpoints.items():
        assert leaves(endpoint) & old_open == set(graph["shared_open_ids"])
        assert sorted(leaves(endpoint) & remaining) == reported
        assert "DESIGN_CHOICES_COMMON" in reported
        print(f"{endpoint} has {len(reported)} remaining contracts")
    difference = set(endpoints["DIRICHLET_GRH"]) - set(endpoints["ORDINARY_RH"])
    assert sorted(difference) == update["additional_dirichlet_grh_contracts"]
    print(f"Checked {len(deps)} nodes, {len(proved)} updated proof references and {len(roadmap_ids)} roadmap entries")


if __name__ == "__main__":
    main()
