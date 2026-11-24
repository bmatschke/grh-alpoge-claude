#!/usr/bin/env python3
"""Check the v0.63 proof ledger and the installation of host vanishing."""
import argparse
from collections import Counter
from graphlib import TopologicalSorter
import json
from pathlib import Path
import subprocess
import sys
from types import ModuleType


ROOT = Path(__file__).resolve().parents[1]
BASE = "7e11ae44637b52a2b6b962fd6a4f51b5624c3f3a"
GRAPH = "continuation_v62/obligations.json"
LEAF = "TASK_HOST_VAN_E_INSTALL"
DERIVED = "HOST_VAN_E"
ENDPOINT = "VHZ4"
PROVED = "proved_in_stated_scope"


def archived(path):
    return subprocess.check_output(["git", "-C", str(ROOT), "show", f"{BASE}:{path}"])


def previous_checks():
    """Use the byte-range and historical-ledger checks from the immutable release."""
    path = "continuation_v62/verify.py"
    module = ModuleType("v62_checks")
    module.__file__ = str(ROOT / path)
    exec(compile(archived(path), module.__file__, "exec"), module.__dict__)
    return module, module.predecessor_verifier()


def verify_graph(core, previous, current, changes, claims):
    check, distinct = core.check, core.distinct
    check(changes["base_commit"] == BASE and changes["base_graph_path"] == GRAPH, "wrong graph predecessor")
    data = archived(GRAPH)
    core.digest(data, changes["base_graph_sha256"], GRAPH)
    before = json.loads(data)
    contracts = {row["id"]: row for row in before["remaining_contracts"]}
    closure = {"id": LEAF, "contract": contracts[LEAF]["contract"], "proof_claims": [ENDPOINT]}
    check(changes["closure_groups"] == [closure] and changes["derived_nodes"] == [DERIVED],
          "wrong closure witnesses, contract or derived node")
    by_claim = {c["id"]: c for c in claims}
    check(by_claim[ENDPOINT]["manuscript"] == "hostvan_v63/assembly.tex", "wrong host closure proof")
    evidence = {cid: c["dependencies"] for cid, c in by_claim.items()}
    supporting = {ENDPOINT}
    for cid in reversed(tuple(TopologicalSorter(evidence).static_order())):
        if cid in supporting:
            supporting.update(evidence.get(cid, []))
    check({"VHZ1", "VHZ2", "VHZ3", "VHN1", "VHN2", "VHN3", "RV6"} <= supporting,
          "host closure does not depend on both scalar line proofs and their matrix assembly")
    old_nodes = {n["id"]: n for n in before["nodes"]}
    nodes = changes["nodes"]
    check(distinct([n["id"] for n in nodes], "graph IDs") == set(old_nodes), "selected graph IDs changed")
    check(old_nodes[LEAF]["gate"] == "LEAF" and not old_nodes[LEAF]["requires"]
          and old_nodes[DERIVED]["gate"] == "AND" and old_nodes[DERIVED]["requires"] == ["CERT_COHOMOLOGY_NATIVE", LEAF]
          and old_nodes["CERT_COHOMOLOGY_NATIVE"]["status"] == PROVED
          and all(old_nodes[oid]["status"] != PROVED for oid in (LEAF, DERIVED)), "wrong predecessor vanishing interface")
    for node in nodes:
        expected = dict(old_nodes[node["id"]])
        if node["id"] in (LEAF, DERIVED):
            expected["status"] = PROVED
        check(node == expected, f"{node['id']}: unexpected graph change")

    old, new = previous["mathematical_state"], current["mathematical_state"]
    check(new["selected_graph_nodes"] == old["selected_graph_nodes"] == len(nodes) == 121
          and new["selected_graph_edges"] == old["selected_graph_edges"] == sum(len(n["requires"]) for n in nodes) == 161,
          "incorrect graph totals")
    check(new["new_whole_obligation_closures"] == [LEAF] and new["global_local_gain"] == old["global_local_gain"],
          "incorrect checkpoint closure transition")
    opened = set()
    for key, count in (("shared_open_ids", "shared_rh_grh_open"),
                       ("additional_grh_open_ids", "additional_unrestricted_dirichlet_grh_open")):
        was = distinct(previous[key], key)
        now = distinct(current[key], key)
        check(was == set(before[key]) and len(was) == old[count] and now == was - {LEAF}
              and now == distinct(changes[key], key) and len(now) == new[count], f"{key}: wrong obligations")
        check(not opened.intersection(now), "open ID lists overlap")
        opened.update(now)
    check(opened == distinct(changes["remaining"], "remaining IDs")
          and len(opened) == new["whole_open_obligations"] == old["whole_open_obligations"] - 1,
          "wrong whole-obligation count")
    rows = changes["remaining_contracts"]
    check(distinct([r["id"] for r in rows], "remaining contracts") == opened
          and all(r == contracts[r["id"]] for r in rows), "original remaining contracts changed")
    check(current["whole_open_by_class"] == dict(Counter(contracts[oid]["category"] for oid in opened)),
          "wrong remaining counts by class")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--formal-git", type=Path, metavar="PATH", help="check exact source bytes at the original formal pin")
    formal = parser.parse_args().formal_git
    prior, core = previous_checks()
    previous = json.loads(archived("CURRENT_CHECKPOINT_v0_62.json"))
    current = json.loads(core.local_file("CURRENT_CHECKPOINT_v0_63.json"))
    manifest = json.loads(core.local_file("continuation_v63/claims.json"))
    graph = json.loads(core.local_file("continuation_v63/obligations.json"))
    core.check(current["predecessor"]["reconstruction_commit"] == manifest["base_commit"] == BASE, "incorrect base revision")
    pin = manifest["formal_pin"]
    core.check(current["original_source"] == previous["original_source"] and pin == current["original_source"]["commit"],
               "original source pin changed")
    if formal:
        if formal.is_file() and formal.name == ".git":
            formal = formal.parent
        core.check(core.git(formal, "rev-parse", pin + "^{tree}").decode().strip() == current["original_source"]["tree"],
                   "formal source tree mismatch")
    known = prior.predecessor_ids(core, json.loads(archived("CURRENT_CHECKPOINT_v0_61.json")), previous)
    known = core.distinct([*known, *(c["id"] for c in json.loads(archived("continuation_v62/claims.json"))["claims"])],
                          "historical claim IDs")
    core.check(len(known) == previous["mathematical_state"]["cumulative_claims"] == current["predecessor"]["cumulative_claims"]
               == 3858, "incorrect historical claim total")
    added, ranges, files = core.verify_claims(manifest, known, pin, formal)
    for review in manifest["reviews"]:
        core.check(review["manuscript_sha256"].encode() in core.local_file(review["path"]),
                   f"{review['path']}: review omits the exact manuscript hash")
    state = current["mathematical_state"]
    core.check(added == state["new_claims_in_this_package"] and len(known) + added == state["cumulative_claims"],
               "wrong new or cumulative claim count")
    verify_graph(core, previous, current, graph, manifest["claims"])
    mode = "verified against Git" if formal else "indexed; use --formal-git to verify source bytes"
    print(f"Verified {added} new claims, {state['cumulative_claims']} cumulative claims, {state['whole_open_obligations']} "
          f"open obligations ({state['shared_rh_grh_open']} shared, {state['additional_unrestricted_dirichlet_grh_open']} additional).")
    print(f"{ranges} source ranges in {files} pinned files ({mode}).")


if __name__ == "__main__":
    try:
        main()
    except (OSError, ValueError, TypeError, KeyError, subprocess.CalledProcessError) as exc:
        sys.exit(f"Verification failed: {exc}")
