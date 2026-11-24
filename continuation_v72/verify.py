#!/usr/bin/env python3
"""Verify the 0.72 manuscript and its two whole arithmetic closures and derived host conclusions."""
import argparse
from collections import Counter
from graphlib import TopologicalSorter
import json
from pathlib import Path
import subprocess
import sys
from types import ModuleType


ROOT = Path(__file__).resolve().parents[1]
BASE = "1cea200af6bb614a18f176dfe585b716d64d6f13"
GRAPH = "continuation_v71/obligations.json"
CLOSURES = {'THM_S6_S': 'M72S3', 'AUT_UNRAM_COEF': 'T72W1'}
DERIVED = {'COUNT_V_PRODUCER': 'M72S4', 'INP_Z': 'KIZ2', 'ONE_CHAR': 'T72W2', 'PROP_GK': 'T72W2', 'COUNT_I_PRODUCER': 'T72W2', 'COUNT_I': 'T72W2', 'PMEX_ALT': 'QX10', 'COUNT_II': 'YX2', 'CASE3_PROMOD': 'CJP3', 'COUNT_III_PRODUCER': 'CJA2', 'COUNT_III_GENERAL': 'T72W3', 'VWIN_RH': 'T72W3', 'VWIN_GRH': 'T72W3', 'HOST_RH': 'T72W3', 'HOST_GRH': 'T72W3'}
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
    for edition in range(60, 72):
        rows = json.loads(archived(f"continuation_v{edition}/claims.json"))["claims"]
        ids.extend(row["id"] for row in rows)
    known = core.distinct(ids, "historical claim IDs")
    core.check(len(known) == previous["mathematical_state"]["cumulative_claims"]
               == current["predecessor"]["cumulative_claims"] == 4064, "incorrect historical claim total")
    return known


def verify_endpoints(core, claims):
    chapters = [("V72L", 8, "local"), ("D72P", 3, "crystal"), ("C72M", 11, "cm"),
                ("A72F", 9, "aut"), ("O72H", 6, "outer"), ("M72S", 4, "assembly"),
                ("E72G", 2, "datum"), ("R72Q", 3, "corner"), ("T72W", 3, "return")]
    expected = {f"{prefix}{i}": f"continuation_v72/{chapter}.tex" for prefix, count, chapter in chapters
                for i in range(1, count + 1)}
    by_id = {row["id"]: row["manuscript"] for row in claims}
    core.check(by_id == expected, "new claims or their manuscripts differ from the reviewed chapters")
    dependencies = {c["id"]: c["dependencies"] for c in claims}
    support = {"T72W3"}
    for cid in reversed(tuple(TopologicalSorter(dependencies).static_order())):
        if cid in support:
            support.update(dependencies.get(cid, []))
    essential = set(expected) | {"AFE15", "AFE16", "HIA2", "HIA3", "A71M1", "A71M2", "F71A3",
                                 "D70W1", "D70W2", "D70W5", "L69D3", "UCE19", "HVJ2",
                                 "VUN6", "OCH30", "KIZ2", "QX10", "YX2", "CJA2", "HX4"}
    core.check(essential <= support, "the two arithmetic closures or the host installation lack a required argument")


def verify_graph(core, previous, current, changes):
    check, distinct = core.check, core.distinct
    check(changes["base_commit"] == BASE and changes["base_graph_path"] == GRAPH, "wrong graph predecessor")
    data = archived(GRAPH)
    core.digest(data, changes["base_graph_sha256"], GRAPH)
    before = json.loads(data)
    contracts = {r["id"]: r for r in before["remaining_contracts"]}
    groups = changes["closure_groups"]
    check(distinct([g["id"] for g in groups], "closure groups") == set(CLOSURES)
          and changes["derived_nodes"] == [{"id": k, "proof_claims": [v]} for k, v in DERIVED.items()], "unexpected obligation closures or derived status changes")
    for group in groups:
        oid = group["id"]
        check(group == {"id": oid, "contract": contracts[oid]["contract"], "proof_claims": [CLOSURES[oid]]},
              f"{oid}: original closure contract or witness changed")
    old_nodes = {n["id"]: n for n in before["nodes"]}
    nodes = changes["nodes"]
    check(distinct([n["id"] for n in nodes], "graph IDs") == set(old_nodes), "selected graph IDs changed")
    installed = {n["id"] for n in old_nodes.values() if n["status"] == PROVED} | set(CLOSURES)
    for oid in DERIVED:
        n = old_nodes[oid]
        check(n["gate"] == "AND" and n["requires"] and set(n["requires"]) <= installed,
              f"{oid}: required input missing at installation")
        installed.add(oid)
    for node in nodes:
        oid = node["id"]
        expected = dict(old_nodes[oid])
        if oid in CLOSURES:
            check(expected["gate"] == "LEAF" and not expected["requires"] and expected["status"] != PROVED,
                  f"{oid}: expected an open predecessor leaf")
            expected["status"] = PROVED
        elif oid in DERIVED:
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
    previous = json.loads(archived("CURRENT_CHECKPOINT_v0_71.json"))
    current = json.loads(core.local_file("CURRENT_CHECKPOINT_v0_72.json"))
    manifest = json.loads(core.local_file("continuation_v72/claims.json"))
    graph = json.loads(core.local_file("continuation_v72/obligations.json"))
    core.check(current["predecessor"]["reconstruction_commit"] == manifest["base_commit"] == BASE, "wrong base revision")
    pin = manifest["formal_pin"]
    core.check(current["original_source"] == previous["original_source"] and pin == current["original_source"]["commit"],
               "original source pin changed")
    core.check(current["mathematical_edition"] == manifest["edition"] == graph["edition"] == "0.72"
               and previous["mathematical_edition"] == current["predecessor"]["mathematical_edition"] == "0.71",
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
    all_ids = known | {c["id"] for c in manifest["claims"]}
    core.check(set(DERIVED.values()) <= all_ids and set(CLOSURES.values()) <= all_ids, "unknown closure witness")
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
