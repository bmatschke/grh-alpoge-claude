#!/usr/bin/env python3
"""Verify the 0.85 manuscript and its source, dependencies, and obligation graph."""
import argparse
from collections import Counter
from graphlib import TopologicalSorter
import json
from pathlib import Path
import subprocess
import sys
from types import ModuleType


ROOT = Path(__file__).resolve().parents[1]
BASE = "92dcfff5f0524e8fa05dfd27392cf2e23744d6a4"
GRAPH = "continuation_v84/obligations.json"
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
    for edition in range(60, 85):
        rows = json.loads(archived(f"continuation_v{edition}/claims.json"))["claims"]
        ids.extend(row["id"] for row in rows)
    known = core.distinct(ids, "historical claim IDs")
    core.check(len(known) == previous["mathematical_state"]["cumulative_claims"]
               == current["predecessor"]["cumulative_claims"] == 4720, "incorrect historical claim total")
    return known


def verify_endpoints(core, claims):
    chapters = {'realization': ['R85P1', 'R85P2', 'R85P3'], 'connection': ['E85C1', 'E85C2', 'E85C3', 'E85C4'], 'kernel': ['K85F1', 'K85F2', 'K85F3', 'K85F4'], 'monodromy': ['M85N1', 'M85N2', 'M85N3', 'M85N4', 'M85N5', 'M85N6'], 'period': ['P85C1', 'P85C2', 'P85C3', 'P85C4', 'P85C5', 'P85C6'], 'assembly': ['A85D1', 'A85D2', 'A85D3'], 'memberfield': ['W85M1'], 'basechange': ['B85U1', 'B85U2'], 'member': ['G85M1', 'G85M2', 'G85M3'], 'depth': ['D85G1']}
    expected = {cid: f"continuation_v85/{chapter}.tex" for chapter, ids in chapters.items() for cid in ids}
    core.check({c["id"]: c["manuscript"] for c in claims} == expected, "reviewed chapter or claim mismatch")
    edges = {c["id"]: c["dependencies"] for c in claims}
    endpoints = {'A85D3': ['A85D2', 'P84B3', 'T84L5', 'K84P4'], 'B85U2': ['B85U1', 'A72F6', 'V72L1', 'V72L3'], 'D85G1': ['M84T7', 'M84T9', 'B85U1'], 'G85M3': ['P84C1', 'G85M1', 'G85M2'], 'W85M1': ['M84T7'], 'A85D2': ['R85P1', 'R85P2', 'R85P3', 'E85C4', 'K85F2', 'K85F3', 'K85F4', 'M85N2', 'M85N6', 'P85C2', 'P85C5', 'P85C6', 'A85D1', 'Q84T1', 'Q84T2']}
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
    previous = json.loads(archived("CURRENT_CHECKPOINT_v0_84.json"))
    current = json.loads(core.local_file("CURRENT_CHECKPOINT_v0_85.json"))
    manifest = json.loads(core.local_file("continuation_v85/claims.json"))
    graph = json.loads(core.local_file("continuation_v85/obligations.json"))
    core.check(current["predecessor"]["reconstruction_commit"] == manifest["base_commit"] == BASE, "wrong base revision")
    pin = manifest["formal_pin"]
    core.check(current["original_source"] == previous["original_source"] and pin == current["original_source"]["commit"],
               "original source pin changed")
    core.check(current["mathematical_edition"] == manifest["edition"] == graph["edition"] == "0.85"
               and previous["mathematical_edition"] == current["predecessor"]["mathematical_edition"] == "0.84",
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
    validation = json.loads(core.local_file("continuation_v85/validation.json"))
    core.check((validation["new_claims"], validation["source_ranges"], validation["distinct_pinned_files"])
               == (added, ranges, files), "validation totals disagree with the checked ledger")
    pdf = validation["short_reader"]
    core.check(pdf["path"] == current["entry_points"]["new_proofs_pdf"] == "RH_new_proofs_v0_85.pdf",
               "wrong typeset supplement")
    core.digest(core.local_file(pdf["path"]), pdf["sha256"], pdf["path"])
    covered = {"pos", "pass", "mult", "rank", "kill", "num", "bb", "exc", "typ", "par", "small", "large", "ram", "two"}
    covered.add("mid")
    remaining = set()
    receipt = current["denominator_family"]
    core.check(core.distinct(receipt["together_on_one_hub"], "proved family fields") == covered
               and core.distinct(receipt["remaining_fields"], "remaining family fields") == remaining
               and receipt["witness"] == "A83G2" and receipt["alternate_witness"] == "V84A5"
               and receipt["good_cut_witness"] == "P84B1" and receipt["type_prime_lifting_witness"] == "A85D2"
               and receipt["conditional_original_family_witness"] == "A85D3", "family conclusion accounting changed")
    mode = "verified against Git" if formal else "indexed; supply --formal-git to check original bytes"
    print(f"Verified {added} new claims, {state['cumulative_claims']} cumulative claims, {state['whole_open_obligations']} "
          f"open obligations ({state['shared_rh_grh_open']} shared, {state['additional_unrestricted_dirichlet_grh_open']} additional).")
    print(f"{ranges} source ranges in {files} pinned files ({mode}).")


if __name__ == "__main__":
    try:
        main()
    except (OSError, ValueError, TypeError, KeyError, subprocess.CalledProcessError) as error:
        sys.exit(f"Verification failed: {error}")
