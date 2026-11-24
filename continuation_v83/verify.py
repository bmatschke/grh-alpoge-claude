#!/usr/bin/env python3
"""Verify the 0.83 manuscript and its source, dependencies, and obligation graph."""
import argparse
from collections import Counter
from graphlib import TopologicalSorter
import json
from pathlib import Path
import subprocess
import sys
from types import ModuleType


ROOT = Path(__file__).resolve().parents[1]
BASE = "682a3b0bdf07b3a95566cee72d0eb4388814b438"
GRAPH = "continuation_v82/obligations.json"
CLOSURES = {}
PROVED = "proved_in_stated_scope"


def archived(path):
    return subprocess.check_output(["git", "-C", str(ROOT), "show", f"{BASE}:{path}"])


def previous_checks():
    """Use the byte-range verifier as archived in the public parent commit."""
    path = "continuation_v60/verify.py"
    module = ModuleType("archived_manuscript_checks")
    module.__file__ = str(ROOT / path)
    exec(compile(archived(path), module.__file__, "exec"), module.__dict__)
    return module


def historical_ids(core, previous, current):
    """Reconstruct every prior ID from files in the single public base tree."""
    first = json.loads(archived("continuation_v59/claims.json"))
    ledger = archived(first["predecessor_ledger"])
    core.check(core.blob_id(ledger) == first["predecessor_ledger_git_blob"], "wrong first proof ledger")
    ids = [row["id"] for row in json.loads(ledger)["claims"]]
    ids.extend(row["id"] for component in first["components"] for row in component["claims"])
    for edition in range(60, 83):
        rows = json.loads(archived(f"continuation_v{edition}/claims.json"))["claims"]
        ids.extend(row["id"] for row in rows)
    known = core.distinct(ids, "historical claim IDs")
    core.check(len(known) == previous["mathematical_state"]["cumulative_claims"]
               == current["predecessor"]["cumulative_claims"] == 4614, "incorrect historical claim total")
    return known


def verify_endpoints(core, claims):
    chapters = {'mixed': ['U83M1', 'U83M2', 'U83M3', 'U83M4', 'U83M5', 'U83M6'], 'thick': ['T83A1', 'T83A2', 'T83A3', 'T83A4', 'T83A5', 'T83A6'], 'separation': ['S83M1', 'S83M2'], 'single': ['S83L1', 'S83L2', 'S83L3', 'S83L4'], 'twodown': ['D83L1', 'D83L2'], 'threejet': ['K83J1', 'K83J2', 'K83J3'], 'threevector': ['K83V1', 'K83V2'], 'far3': ['F83S1', 'F83S2'], 'upthree': ['A83U1', 'A83U2', 'A83U3'], 'excess': ['E83D1', 'E83D2', 'E83D3'], 'doublehits': ['H83F1', 'H83F2', 'H83F3'], 'assembly': ['A83G1', 'A83G2', 'A83G3', 'A83G4'], 'tiecut': ['T83C1', 'T83C2', 'T83C3'], 'cylinder': ['C83N1', 'C83N2', 'C83N3', 'C83N4'], 'nearflag': ['C83N5', 'C83N6']}
    expected = {cid: f"continuation_v83/{chapter}.tex" for chapter, ids in chapters.items() for cid in ids}
    core.check({c["id"]: c["manuscript"] for c in claims} == expected, "reviewed chapter or claim mismatch")
    edges = {c["id"]: c["dependencies"] for c in claims}
    endpoints = {'A83G4': ['A83G1', 'A83G2', 'A83G3', 'A83U3', 'B82R3', 'D83L2', 'DNE14', 'F78D2', 'F83S2', 'G82C5', 'G82F4', 'G82I2', 'I82W5', 'K83V2', 'LN10', 'N82I1', 'S83L4', 'S83M2', 'T83A6', 'U83M6'], 'C83N4': ['C83N3'], 'C83N6': ['C83N2', 'C83N3', 'C83N5'], 'E83D3': ['A78P3', 'E83D2', 'X78A1', 'X78A2', 'X78A3'], 'H83F3': ['C82S1', 'E83D1', 'E83D2', 'H83F2'], 'T83C3': ['T83C1', 'T83C2'], 'U83M5': ['A78P2', 'G82I2', 'I82W1', 'I82W3', 'I82W5', 'M82R1', 'M82R2', 'N82I1', 'N82I2']}
    covered = set()
    for point, required in endpoints.items():
        supporting = {point}
        for cid in reversed(tuple(TopologicalSorter(edges).static_order())):
            if cid in supporting:
                supporting.update(edges.get(cid, []))
        core.check(set(required) <= supporting, f"{point}: missing a required dependency")
        covered.update(supporting)
    core.check(set(expected) <= covered, "reviewed claim is disconnected from the edition endpoints")


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
    core = previous_checks()
    previous = json.loads(archived("CURRENT_CHECKPOINT_v0_82.json"))
    current = json.loads(core.local_file("CURRENT_CHECKPOINT_v0_83.json"))
    manifest = json.loads(core.local_file("continuation_v83/claims.json"))
    graph = json.loads(core.local_file("continuation_v83/obligations.json"))
    core.check(current["predecessor"]["reconstruction_commit"] == manifest["base_commit"] == BASE, "wrong base revision")
    pin = manifest["formal_pin"]
    core.check(current["original_source"] == previous["original_source"] and pin == current["original_source"]["commit"],
               "original source pin changed")
    core.check(current["mathematical_edition"] == manifest["edition"] == graph["edition"] == "0.83"
               and previous["mathematical_edition"] == current["predecessor"]["mathematical_edition"] == "0.82",
               "wrong edition or predecessor")
    if formal:
        if formal.is_file() and formal.name == ".git":
            formal = formal.parent
        core.check(core.git(formal, "rev-parse", pin + "^{tree}").decode().strip() == current["original_source"]["tree"],
                   "formal source tree mismatch")
    known = historical_ids(core, previous, current)
    added, ranges, files = core.verify_claims(manifest, known, pin, formal)
    for review in manifest["reviews"]:
        core.check(review["manuscript_sha256"].encode() in core.local_file(review["path"]),
                   f"{review['path']}: review omits the exact manuscript hash")
    verify_endpoints(core, manifest["claims"])
    verify_graph(core, previous, current, graph)
    state = current["mathematical_state"]
    core.check(added == state["new_claims_in_this_package"] and len(known) + added == state["cumulative_claims"],
               "wrong new or cumulative claim count")
    validation = json.loads(core.local_file("continuation_v83/validation.json"))
    core.check((validation["new_claims"], validation["source_ranges"], validation["distinct_pinned_files"])
               == (added, ranges, files), "validation totals disagree with the checked ledger")
    pdf = validation["short_reader"]
    core.check(pdf["path"] == current["entry_points"]["new_proofs_pdf"] == "RH_new_proofs_v0_83.pdf",
               "wrong typeset supplement")
    core.digest(core.local_file(pdf["path"]), pdf["sha256"], pdf["path"])
    covered = {"pos", "pass", "mult", "rank", "kill", "num", "bb", "exc", "typ", "par", "small", "large", "ram", "two"}
    covered.add("mid")
    remaining = set()
    receipt = current["denominator_family"]
    core.check(core.distinct(receipt["together_on_one_hub"], "proved family fields") == covered
               and core.distinct(receipt["remaining_fields"], "remaining family fields") == remaining
               and receipt["witness"] == "A83G2", "family conclusion accounting changed")
    mode = "verified against Git" if formal else "indexed; supply --formal-git to check original bytes"
    print(f"Verified {added} new claims, {state['cumulative_claims']} cumulative claims, {state['whole_open_obligations']} "
          f"open obligations ({state['shared_rh_grh_open']} shared, {state['additional_unrestricted_dirichlet_grh_open']} additional).")
    print(f"{ranges} source ranges in {files} pinned files ({mode}).")


if __name__ == "__main__":
    try:
        main()
    except (OSError, ValueError, TypeError, KeyError, subprocess.CalledProcessError) as error:
        sys.exit(f"Verification failed: {error}")
