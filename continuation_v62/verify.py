#!/usr/bin/env python3
"""Verify the 0.62 manuscript, its pinned sources and the changes to the obligation graph."""
import argparse
from collections import Counter
import json
from pathlib import Path
import subprocess
import sys
from types import ModuleType


ROOT = Path(__file__).resolve().parents[1]
BASE = "f4081539e42aed1138b9c5a2b8c107eb4565f19b"
PREVIOUS_GRAPH = "continuation_v61/obligations.json"
ORIGINAL_GRAPH = "dependency_audit_v0_57/obligation_map.json"
CLOSURES = {
    "TASK_CASE3_PROMOD_JOIN": ("CJP1", "CJP2", "CJP3"),
    "TASK_CASE3_AUT_JOIN": ("CJA1", "CJA2"),
    "HOST_FRAME_LENGTH": ("HVJ1",),
    "TASK_COUNT_V_INSTALL": ("HVJ2",),
}


def archived(path):
    """Read a tracked object even when the working tree uses sparse checkout."""
    return subprocess.check_output(["git", "-C", str(ROOT), "show", f"{BASE}:{path}"])


def predecessor_verifier():
    """Load the existing ledger and byte-range checks from the fixed predecessor."""
    path = "continuation_v60/verify.py"
    module = ModuleType("v60_checks")
    module.__file__ = str(ROOT / path)
    exec(compile(archived(path), module.__file__, "exec"), module.__dict__)
    return module


def predecessor_ids(v60, previous, current):
    edition59 = json.loads(archived("continuation_v59/claims.json"))
    ledger = archived(edition59["predecessor_ledger"])
    v60.check(v60.blob_id(ledger) == edition59["predecessor_ledger_git_blob"], "historical ledger mismatch")
    ids = [row["id"] for row in json.loads(ledger)["claims"]]
    ids.extend(row["id"] for component in edition59["components"] for row in component["claims"])
    for epoch in (60, 61):
        chapter = json.loads(archived(f"continuation_v{epoch}/claims.json"))
        ids.extend(row["id"] for row in chapter["claims"])
    known = v60.distinct(ids, "historical proof IDs")
    v60.check(len(known) == previous["mathematical_state"]["cumulative_claims"]
              == current["predecessor"]["cumulative_claims"] == 3820, "incorrect historical claim total")
    return known


def verify_graph(v60, previous, current, changes, claims):
    check, distinct = v60.check, v60.distinct
    check(changes["base_commit"] == BASE and changes["base_graph_path"] == PREVIOUS_GRAPH,
          "incorrect obligation predecessor")
    old_bytes = archived(PREVIOUS_GRAPH)
    v60.digest(old_bytes, changes["base_graph_sha256"], "v0.61 selected graph")
    before = json.loads(old_bytes)
    original = json.loads(archived(ORIGINAL_GRAPH))["nodes"]
    contracts = {n["id"]: n for n in original}
    old_nodes = {n["id"]: n for n in before["nodes"]}
    check(set(contracts) == set(old_nodes), "original obligation IDs differ from the predecessor")
    check(changes["derived_nodes"] == [], "unexpected derived-node change")
    groups = changes["closure_groups"]
    closure_ids = distinct([group["id"] for group in groups], "closure groups")
    check(closure_ids == set(CLOSURES), "unexpected obligation closures")
    by_id = {row["id"]: row for row in claims}
    for group in groups:
        oid = group["id"]
        old = old_nodes[oid]
        check(old["gate"] == "LEAF" and old["requires"] == []
              and old["status"] != "proved_in_stated_scope", f"{oid}: expected an open predecessor leaf")
        check(group["contract"] == contracts[oid]["contract"], f"{oid}: original closure contract changed")
        proof_ids = distinct(group["proof_claims"], f"{oid} witnesses")
        check(proof_ids == set(CLOSURES[oid]) and proof_ids <= set(by_id), f"{oid}: wrong closure witnesses")
    for oid, proof_ids in CLOSURES.items():
        manuscript = "caseiii_v62/main.tex" if oid.startswith("TASK_CASE3_") else "hostjoin_v62/main.tex"
        for cid in proof_ids:
            check(by_id[cid]["manuscript"] == manuscript, f"{cid}: wrong closure proof path")

    nodes = changes["nodes"]
    check(distinct([n["id"] for n in nodes], "selected graph IDs") == set(old_nodes),
          "selected graph IDs changed")
    for n in nodes:
        oid = n["id"]
        expected = dict(old_nodes[oid])
        if oid in closure_ids:
            expected["status"] = "proved_in_stated_scope"
        check(n == expected, f"{oid}: unexpected graph change")
    state, prior = current["mathematical_state"], previous["mathematical_state"]
    check(state["selected_graph_nodes"] == prior["selected_graph_nodes"] == len(nodes) == 121
          and state["selected_graph_edges"] == prior["selected_graph_edges"]
          == sum(len(n["requires"]) for n in nodes) == 161, "incorrect graph totals")
    check(distinct(state["new_whole_obligation_closures"], "checkpoint closures") == closure_ids
          and state["global_local_gain"] == prior["global_local_gain"], "incorrect checkpoint closure transition")

    opened = set()
    removed = set()
    for field, count in (("shared_open_ids", "shared_rh_grh_open"),
                         ("additional_grh_open_ids", "additional_unrestricted_dirichlet_grh_open")):
        old = distinct(previous[field], f"predecessor {field}")
        new = distinct(current[field], field)
        check(old == set(before[field]) and len(old) == prior[count], f"{field}: inconsistent predecessor")
        check(new == distinct(changes[field], f"graph {field}") == old - closure_ids
              and len(new) == state[count], f"{field}: wrong remaining obligation IDs")
        check(opened.isdisjoint(new), "shared and additional open lists overlap")
        opened.update(new)
        removed.update(old - new)
    check(removed == closure_ids and distinct(changes["remaining"], "remaining IDs") == opened
          and len(opened) == state["whole_open_obligations"] == prior["whole_open_obligations"] - len(closure_ids),
          "incorrect list or count of open obligations")
    rows = changes["remaining_contracts"]
    check(distinct([r["id"] for r in rows], "remaining contract IDs") == opened,
          "incorrect remaining contracts")
    for row in rows:
        expected = contracts[row["id"]]
        check(all(row[key] == expected[key] for key in ("title", "category", "contract")),
              f"{row['id']}: original remaining contract changed")
    check(current["whole_open_by_class"] == dict(Counter(contracts[oid]["category"] for oid in opened)),
          "incorrect remaining counts by class")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--formal-git", type=Path, metavar="PATH",
                        help="also verify every Lean source range against the original pinned Git tree")
    args = parser.parse_args()
    v60 = predecessor_verifier()
    previous = json.loads(archived("CURRENT_CHECKPOINT_v0_61.json"))
    current = json.loads(v60.local_file("CURRENT_CHECKPOINT_v0_62.json"))
    manifest = json.loads(v60.local_file("continuation_v62/claims.json"))
    changes = json.loads(v60.local_file("continuation_v62/obligations.json"))
    v60.check(current["predecessor"]["reconstruction_commit"] == manifest["base_commit"] == BASE,
              "incorrect base revision")
    v60.check(current["original_source"] == previous["original_source"]
              and manifest["formal_pin"] == previous["original_source"]["commit"], "incorrect formal source pin")
    formal = args.formal_git
    if formal and formal.is_file() and formal.name == ".git":
        formal = formal.parent
    pin = manifest["formal_pin"]
    if formal:
        tree = v60.git(formal, "rev-parse", pin + "^{tree}").decode().strip()
        v60.check(tree == current["original_source"]["tree"], "formal source tree mismatch")
    known = predecessor_ids(v60, previous, current)
    n, ranges, files = v60.verify_claims(manifest, known, pin, formal)
    for review in manifest["reviews"]:
        v60.check(review["manuscript_sha256"].encode() in v60.local_file(review["path"]),
                  f"{review['path']}: review does not identify the exact manuscript it checks")
    state = current["mathematical_state"]
    v60.check(n == state["new_claims_in_this_package"] and len(known) + n == state["cumulative_claims"],
              "incorrect new or cumulative claim count")
    verify_graph(v60, previous, current, changes, manifest["claims"])
    mode = "verified against Git" if formal else "indexed; use --formal-git to verify source bytes"
    print(f"Verified {n} new claims, {state['cumulative_claims']} cumulative claims, "
          f"{state['whole_open_obligations']} open obligations "
          f"({state['shared_rh_grh_open']} shared, "
          f"{state['additional_unrestricted_dirichlet_grh_open']} additional).")
    print(f"{ranges} source ranges in {files} pinned files ({mode}).")


if __name__ == "__main__":
    try:
        main()
    except (OSError, ValueError, KeyError, TypeError, subprocess.CalledProcessError) as exc:
        sys.exit(f"Verification failed: {exc}")
