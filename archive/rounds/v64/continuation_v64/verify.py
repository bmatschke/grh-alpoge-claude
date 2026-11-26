#!/usr/bin/env python3
"""Check the v0.64 manuscripts, source bindings, and changes to the selected obligation graph."""
import argparse
from collections import Counter
from graphlib import TopologicalSorter
import hashlib
import json
from pathlib import Path
import subprocess
import sys
from types import ModuleType


ROOT = Path(__file__).resolve().parents[1]
BASE = "da57716c0570e25a544072197e73462b40346a7b"
GRAPH = "continuation_v63/obligations.json"
PROVED = "proved_in_stated_scope"
CHAPTERS = {
    "VUN": ("hostnumber_v64/main.tex", 6),
    "TFT": ("tensortower_v64/main.tex", 5),
    "RFCR": ("rankchain_v64/main.tex", 4),
    "VMA": ("markedaut_v64/main.tex", 6),
}
CLOSURES = {
    "HOST_NUMBER_S": "VUN6",
    "TENSOR_FACTOR_TOWER": "TFT5",
    "RANK4_CHAIN_REDUCTION": "RFCR4",
}


def archived(path):
    return subprocess.check_output(["git", "-C", str(ROOT), "show", f"{BASE}:{path}"])


def previous_checks():
    """Load the byte-range and ledger checks from their immutable Git versions."""
    path = "continuation_v63/verify.py"
    module = ModuleType("v63_checks")
    module.__file__ = str(ROOT / path)
    exec(compile(archived(path), module.__file__, "exec"), module.__dict__)
    return module.previous_checks()


def historical_ids(v62, core, previous, current):
    def checkpoint(edition):
        return json.loads(archived(f"CURRENT_CHECKPOINT_v0_{edition}.json"))

    ids = list(v62.predecessor_ids(core, checkpoint(61), checkpoint(62)))
    for edition in (62, 63):
        rows = json.loads(archived(f"continuation_v{edition}/claims.json"))["claims"]
        ids.extend(c["id"] for c in rows)
    known = core.distinct(ids, "historical claim IDs")
    core.check(len(known) == previous["mathematical_state"]["cumulative_claims"]
               == current["predecessor"]["cumulative_claims"] == 3865, "incorrect historical claim total")
    return known


def verify_reviewed_manifests(core, manifest):
    """Match the two source manifests explicitly identified by checksum in their reviews."""
    reviews = {r["manuscript"]: r for r in manifest["reviews"]}
    for prefix in ("VUN", "VMA"):
        manuscript, _ = CHAPTERS[prefix]
        raw_path = str(Path(manuscript).with_name("provenance.json"))
        data = core.local_file(raw_path)
        review = reviews[manuscript]
        checksum = hashlib.sha256(data).hexdigest().encode()
        core.check(checksum in core.local_file(review["path"]), f"{raw_path}: checksum missing from its review")
        raw = json.loads(data)
        core.check(raw["source_commit"] == manifest["formal_pin"] and raw["component"] == Path(manuscript).name
                   and raw["sha256"] == review["manuscript_sha256"], f"{raw_path}: wrong source or manuscript")
        rows = [c for c in manifest["claims"] if c["manuscript"] == manuscript]
        core.check([c["id"] for c in rows] == [c["id"] for c in raw["claims"]],
                   f"{raw_path}: claim IDs differ from the release ledger")
        for claim, source in zip(rows, raw["claims"]):
            bindings = [{"path": b["path"], "lines": b["lines"], "git_blob": b["git_blob"], "sha256": b["range_sha256"]}
                        for b in source["source_ranges"]]
            core.check(claim["lines"] == source["lines"] and claim["sha256"] == source["proof_block_sha256"]
                       and claim["dependencies"] == source["proof_dependencies"] and claim["source_ranges"] == bindings,
                       f"{source['id']}: reviewed source manifest differs from release ledger")


def verify_endpoints(core, claims):
    expected = {f"{prefix}{i}": path for prefix, (path, count) in CHAPTERS.items()
                for i in range(1, count + 1)}
    core.check({c["id"]: c["manuscript"] for c in claims} == expected,
               "new claim IDs or source manuscripts differ from the four reviewed chapters")
    evidence = {c["id"]: c["dependencies"] for c in claims}
    dependency_order = tuple(TopologicalSorter(evidence).static_order())
    for endpoint in CLOSURES.values():
        supporting = {endpoint}
        for cid in reversed(dependency_order):
            if cid in supporting:
                supporting.update(evidence.get(cid, []))
        chapter = {cid for cid, path in expected.items() if path == expected[endpoint]}
        core.check(chapter <= supporting, f"{endpoint}: incomplete proof dependencies for the closed obligation")


def verify_graph(core, previous, current, changes):
    check, distinct = core.check, core.distinct
    check(changes["base_commit"] == BASE and changes["base_graph_path"] == GRAPH, "wrong graph predecessor")
    data = archived(GRAPH)
    core.digest(data, changes["base_graph_sha256"], GRAPH)
    before = json.loads(data)
    contracts = {r["id"]: r for r in before["remaining_contracts"]}
    groups = changes["closure_groups"]
    check(distinct([g["id"] for g in groups], "closure groups") == set(CLOSURES)
          and changes["derived_nodes"] == [], "unexpected obligation closures or derived status changes")
    for group in groups:
        oid = group["id"]
        check(group == {"id": oid, "contract": contracts[oid]["contract"], "proof_claims": [CLOSURES[oid]]},
              f"{oid}: original closure contract or witness changed")
    old_nodes = {n["id"]: n for n in before["nodes"]}
    nodes = changes["nodes"]
    check(distinct([n["id"] for n in nodes], "graph IDs") == set(old_nodes), "selected graph IDs changed")
    for node in nodes:
        oid = node["id"]
        expected = dict(old_nodes[oid])
        if oid in CLOSURES:
            check(expected["gate"] == "LEAF" and not expected["requires"] and expected["status"] != PROVED,
                  f"{oid}: expected an open predecessor leaf")
            expected["status"] = PROVED
        check(node == expected, f"{oid}: unexpected graph change")

    old, new = previous["mathematical_state"], current["mathematical_state"]
    check(new["selected_graph_nodes"] == old["selected_graph_nodes"] == len(nodes) == 121
          and new["selected_graph_edges"] == old["selected_graph_edges"] == sum(len(n["requires"]) for n in nodes) == 161,
          "incorrect graph totals")
    check(distinct(new["new_whole_obligation_closures"], "checkpoint closures") == set(CLOSURES)
          and new["global_local_gain"] == old["global_local_gain"], "incorrect checkpoint transition")
    opened = set()
    for key, count in (("shared_open_ids", "shared_rh_grh_open"),
                       ("additional_grh_open_ids", "additional_unrestricted_dirichlet_grh_open")):
        was = distinct(previous[key], key)
        now = distinct(current[key], key)
        check(was == set(before[key]) and len(was) == old[count] and now == was - CLOSURES.keys()
              and now == distinct(changes[key], key) and len(now) == new[count], f"{key}: wrong obligations")
        check(not opened.intersection(now), "open IDs listed in both classes")
        opened.update(now)
    check(opened == distinct(changes["remaining"], "remaining IDs") and len(opened) == new["whole_open_obligations"]
          == old["whole_open_obligations"] - len(CLOSURES), "wrong whole-obligation count")
    rows = changes["remaining_contracts"]
    check(distinct([r["id"] for r in rows], "remaining contracts") == opened
          and all(r == contracts[r["id"]] for r in rows), "original remaining contracts changed")
    check(current["whole_open_by_class"] == dict(Counter(contracts[oid]["category"] for oid in opened)),
          "wrong counts by obligation class")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--formal-git", type=Path, metavar="PATH", help="check source bytes against the original Lean Git tree")
    formal = parser.parse_args().formal_git
    v62, core = previous_checks()
    previous = json.loads(archived("CURRENT_CHECKPOINT_v0_63.json"))
    current = json.loads(core.local_file("CURRENT_CHECKPOINT_v0_64.json"))
    manifest = json.loads(core.local_file("continuation_v64/claims.json"))
    graph = json.loads(core.local_file("continuation_v64/obligations.json"))
    core.check(current["predecessor"]["reconstruction_commit"] == manifest["base_commit"] == BASE, "wrong base revision")
    pin = manifest["formal_pin"]
    core.check(current["original_source"] == previous["original_source"] and pin == current["original_source"]["commit"],
               "original source pin changed")
    if formal:
        if formal.is_file() and formal.name == ".git":
            formal = formal.parent
        core.check(core.git(formal, "rev-parse", pin + "^{tree}").decode().strip() == current["original_source"]["tree"],
                   "formal source tree mismatch")
    known = historical_ids(v62, core, previous, current)
    added, ranges, files = core.verify_claims(manifest, known, pin, formal)
    for review in manifest["reviews"]:
        core.check(review["manuscript_sha256"].encode() in core.local_file(review["path"]),
                   f"{review['path']}: review omits the exact manuscript hash")
    verify_reviewed_manifests(core, manifest)
    verify_endpoints(core, manifest["claims"])
    verify_graph(core, previous, current, graph)
    state = current["mathematical_state"]
    core.check(added == state["new_claims_in_this_package"] and len(known) + added == state["cumulative_claims"],
               "wrong new or cumulative claim count")
    mode = "verified against Git" if formal else "indexed; supply --formal-git to check original bytes"
    print(f"Verified {added} new claims, {state['cumulative_claims']} cumulative claims, {state['whole_open_obligations']} "
          f"open obligations ({state['shared_rh_grh_open']} shared, {state['additional_unrestricted_dirichlet_grh_open']} additional).")
    print(f"{ranges} source ranges in {files} pinned files ({mode}).")


if __name__ == "__main__":
    try:
        main()
    except (OSError, ValueError, TypeError, KeyError, subprocess.CalledProcessError) as error:
        sys.exit(f"Verification failed: {error}")
