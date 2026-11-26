#!/usr/bin/env python3
"""Verify the 0.78 manuscript and its source, dependencies, and obligation graph."""
import argparse
from collections import Counter
from graphlib import TopologicalSorter
import json
from pathlib import Path
import subprocess
import sys
from types import ModuleType


ROOT = Path(__file__).resolve().parents[1]
BASE = "0ded7a5590d643f4efcbbd2b857aba7304605a17"
GRAPH = "continuation_v77/obligations.json"
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
    for edition in range(60, 78):
        rows = json.loads(archived(f"continuation_v{edition}/claims.json"))["claims"]
        ids.extend(row["id"] for row in rows)
    known = core.distinct(ids, "historical claim IDs")
    core.check(len(known) == previous["mathematical_state"]["cumulative_claims"]
               == current["predecessor"]["cumulative_claims"] == 4317, "incorrect historical claim total")
    return known


def verify_endpoints(core, claims):
    chapters = (
        ("H78K", 6, "hecke"), ("P78C", 14, "producer"), ("E78R", 6, "reading"),
        ("L78W", 13, "local"), ("N78T", 6, "table"), ("F78D", 3, "family"),
        ("A78P", 3, "parameters"), ("X78A", 3, "exceptional"), ("C78B", 5, "coarse"), ("J78H", 2, "assembly"),
    )
    expected = {f"{prefix}{i}": f"continuation_v78/{chapter}.tex"
                for prefix, count, chapter in chapters for i in range(1, count + 1)}
    core.check({c["id"]: c["manuscript"] for c in claims} == expected, "reviewed chapter or claim mismatch")
    edges = {c["id"]: c["dependencies"] for c in claims}
    endpoints = {
        "H78K6": {"H78K1", "H78K3", "H78K5", "B77R1", "F77W1"},
        "P78C14": {"P78C3", "P78C5", "P78C7", "P78C10", "P78C11", "P78C12", "P78C13"},
        "E78R6": {"E78R1", "E78R2", "E78R3", "E78R4", "E78R5", "PKT29", "RDR22"},
        "J78H1": {"A78P3", "X78A3", "LN5", "LN6", "DFD14"},
        "J78H2": {"F78D2", "F78D3"},
        "C78B5": {"F78D2", "C78B1", "C78B2", "C78B3", "C78B4"},
        "F78D3": {"CAP6", "SSC17", "L78W12", "L78W13", "FET25", "DFD12", "F78D1", "F78D2",
                  "N78T2", "N78T3", "N78T4", "N78T5", "N78T6"},
    }
    covered = set()
    for point, required in endpoints.items():
        supporting = {point}
        for cid in reversed(tuple(TopologicalSorter(edges).static_order())):
            if cid in supporting:
                supporting.update(edges.get(cid, []))
        core.check(required <= supporting, f"{point}: missing a required dependency")
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
    previous = json.loads(archived("CURRENT_CHECKPOINT_v0_77.json"))
    current = json.loads(core.local_file("CURRENT_CHECKPOINT_v0_78.json"))
    manifest = json.loads(core.local_file("continuation_v78/claims.json"))
    graph = json.loads(core.local_file("continuation_v78/obligations.json"))
    core.check(current["predecessor"]["reconstruction_commit"] == manifest["base_commit"] == BASE, "wrong base revision")
    pin = manifest["formal_pin"]
    core.check(current["original_source"] == previous["original_source"] and pin == current["original_source"]["commit"],
               "original source pin changed")
    core.check(current["mathematical_edition"] == manifest["edition"] == graph["edition"] == "0.78"
               and previous["mathematical_edition"] == current["predecessor"]["mathematical_edition"] == "0.77",
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
    validation = json.loads(core.local_file("continuation_v78/validation.json"))
    core.check((validation["new_claims"], validation["source_ranges"], validation["distinct_pinned_files"])
               == (added, ranges, files), "validation totals disagree with the checked ledger")
    pdf = validation["short_reader"]
    core.check(pdf["path"] == current["entry_points"]["new_proofs_pdf"] == "RH_new_proofs_v0_78.pdf",
               "wrong typeset supplement")
    core.digest(core.local_file(pdf["path"]), pdf["sha256"], pdf["path"])
    covered = {"pos", "pass", "mult", "rank", "kill", "num", "exc", "par", "small"}
    remaining = {"mid", "bb", "large", "two", "ram", "typ"}
    receipt = current["denominator_family"]
    core.check(core.distinct(receipt["together_on_one_hub"], "proved family fields") == covered
               and core.distinct(receipt["remaining_fields"], "remaining family fields") == remaining
               and receipt["witness"] == "J78H1", "family conclusion accounting changed")
    mode = "verified against Git" if formal else "indexed; supply --formal-git to check original bytes"
    print(f"Verified {added} new claims, {state['cumulative_claims']} cumulative claims, {state['whole_open_obligations']} "
          f"open obligations ({state['shared_rh_grh_open']} shared, {state['additional_unrestricted_dirichlet_grh_open']} additional).")
    print(f"{ranges} source ranges in {files} pinned files ({mode}).")


if __name__ == "__main__":
    try:
        main()
    except (OSError, ValueError, TypeError, KeyError, subprocess.CalledProcessError) as error:
        sys.exit(f"Verification failed: {error}")
