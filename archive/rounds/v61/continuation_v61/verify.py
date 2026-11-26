#!/usr/bin/env python3
"""Check edition 0.61, its claim ledger and the changes to the selected graph (Python 3.9+)."""
import argparse
from collections import Counter
from importlib.machinery import SourceFileLoader
import json
from pathlib import Path
import subprocess
import sys
from types import ModuleType

ROOT = Path(__file__).resolve().parents[1]
BASE = "0b9d14003be8869c18891ec5a4553b2dd8e59c03"
GRAPH = "continuation_v60/obligations.json"
ORIGINAL_GRAPH = "dependency_audit_v0_57/obligation_map.json"
CLOSED = "CHAIN_DESC4"
PROOF = ["RCD1", "RCD2", "RCD3"]


def archived(path):
    """Read the immutable predecessor even when this path is outside the sparse checkout."""
    return subprocess.check_output(["git", "-C", str(ROOT), "show", f"{BASE}:{path}"])


def predecessor_verifier():
    """Reuse v0.60's hash, ledger and dependency checks from the verified base revision."""
    name = "continuation_v60/verify.py"
    module = ModuleType("v60_checks")
    module.__file__ = str(ROOT / name)
    loader = SourceFileLoader(module.__name__, module.__file__)
    exec(loader.source_to_code(archived(name), module.__file__), module.__dict__)
    return module


def verify_graph(v60, current, previous, changes, claims):
    check, distinct = v60.check, v60.distinct
    check(changes["base_commit"] == BASE and changes["base_graph_path"] == GRAPH,
          "incorrect obligation predecessor")
    raw = archived(GRAPH)
    v60.digest(raw, changes["base_graph_sha256"], "v0.60 graph")
    before = json.loads(raw)
    old_nodes = {n["id"]: n for n in before["nodes"]}
    full_raw = archived(ORIGINAL_GRAPH)
    v60.digest(full_raw, before["base_graph_sha256"], "original graph contracts")
    contracts = {n["id"]: n for n in json.loads(full_raw)["nodes"]}
    check(before["base_graph_path"] == ORIGINAL_GRAPH and set(contracts) == set(old_nodes),
          "original obligation graph differs from predecessor")
    check(changes["closed_leaf"] == CLOSED and changes["derived_node"] is None
          and changes["closure_contract"] == contracts[CLOSED]["contract"], "incorrect closure or contract")
    check(changes["proof_claims"] == PROOF, "incorrect closure witnesses")
    by_id = {c["id"]: c for c in claims}
    for cid in PROOF:
        check(by_id[cid]["manuscript"] == "chain_v61/main.tex", f"{cid}: wrong proof path")
    check(set(by_id["RCD3"]["dependencies"]) == {"RCD1", "RCD2"}, "incorrect RCD3 proof dependencies")

    check(old_nodes[CLOSED]["status"].startswith("open_") and old_nodes[CLOSED]["gate"] == "LEAF",
          "expected an open chain descent leaf in the predecessor")
    check(all(old_nodes[i]["status"] == "proved_in_stated_scope" for i in ("TASK_HOST_XPP_INSTALL", "HOST_XPP")),
          "predecessor host closure missing")
    nodes = changes["nodes"]
    check(distinct([n["id"] for n in nodes], "selected graph IDs") == set(old_nodes),
          "selected graph IDs changed")
    for n in nodes:
        expected = dict(old_nodes[n["id"]])
        if n["id"] == CLOSED:
            expected["status"] = "proved_in_stated_scope"
        check(n == expected, f"{n['id']}: unexpected graph change")
    state, prior = current["mathematical_state"], previous["mathematical_state"]
    check(state["selected_graph_nodes"] == prior["selected_graph_nodes"] == len(nodes) == 121
          and state["selected_graph_edges"] == prior["selected_graph_edges"]
          == sum(len(n["requires"]) for n in nodes) == 161, "incorrect graph totals")
    check(state["new_whole_obligation_closures"] == [CLOSED] and state["global_local_gain"] == prior["global_local_gain"],
          "incorrect change in whole closures")
    groups = []
    for field, count, total in (("shared_open_ids", "shared_rh_grh_open", 16),
                                ("additional_grh_open_ids", "additional_unrestricted_dirichlet_grh_open", 6)):
        old = distinct(previous[field], f"predecessor {field}")
        new = distinct(current[field], field)
        check(new == distinct(changes[field], f"graph {field}") == old - {CLOSED}
              and len(new) == state[count] == total and len(old) == prior[count],
              f"incorrect open obligations in {field}")
        groups.append(new)
    opened = groups[0] | groups[1]
    check(groups[0].isdisjoint(groups[1]) and distinct(changes["remaining"], "remaining IDs") == opened
          and len(opened) == state["whole_open_obligations"] == prior["whole_open_obligations"] - 1 == 22,
          "incorrect list or total of remaining obligations")
    rows = changes["remaining_contracts"]
    check(distinct([r["id"] for r in rows], "remaining contract IDs") == opened, "incorrect remaining contracts")
    for row in rows:
        check(all(row[k] == contracts[row["id"]][k] for k in ("title", "category", "contract")),
              f"{row['id']}: original obligation contract changed")
    check(current["whole_open_by_class"] == dict(Counter(contracts[i]["category"] for i in opened)),
          "incorrect remaining counts by class")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--formal-git", type=Path, metavar="PATH",
                        help="also check every source excerpt against the pinned Git repository or submodule")
    args = parser.parse_args()
    v60 = predecessor_verifier()
    local = lambda path: json.loads(v60.local_file(path))
    previous = json.loads(archived("CURRENT_CHECKPOINT_v0_60.json"))
    current = local("CURRENT_CHECKPOINT_v0_61.json")
    manifest = local("continuation_v61/claims.json")
    v60.check(current["predecessor"]["reconstruction_commit"] == manifest["base_commit"] == BASE,
              "wrong base revision")
    v60.check(current["original_source"] == previous["original_source"]
              and manifest["formal_pin"] == previous["original_source"]["commit"], "wrong formal source")
    formal = args.formal_git
    if formal and formal.is_file() and formal.name == ".git":
        formal = formal.parent
    pin = manifest["formal_pin"]
    if formal:
        tree = v60.git(formal, "rev-parse", pin + "^{tree}").decode().strip()
        v60.check(tree == current["original_source"]["tree"], "formal tree mismatch")
    earlier = json.loads(v60.at_base("CURRENT_CHECKPOINT_v0_59.json"))
    known = v60.predecessor(earlier, previous["predecessor"])
    prev_claims = json.loads(archived("continuation_v60/claims.json"))["claims"]
    known = v60.distinct([*known, *(c["id"] for c in prev_claims)], "historical proof IDs")
    v60.check(len(known) == previous["mathematical_state"]["cumulative_claims"]
              == current["predecessor"]["cumulative_claims"] == 3801, "incorrect historical claim total")
    n, ranges, files = v60.verify_claims(manifest, known, pin, formal)
    state = current["mathematical_state"]
    v60.check(state["new_claims_in_this_package"] == n and state["cumulative_claims"] == len(known) + n,
              "incorrect new or cumulative claim count")
    verify_graph(v60, current, previous, local("continuation_v61/obligations.json"), manifest["claims"])
    mode = "verified against Git" if formal else "indexed; use --formal-git to verify source bytes"
    print(f"Verified {n} new claims, {len(known) + n} cumulative claims, 22 open obligations (16 shared, 6 additional).")
    print(f"{ranges} source ranges in {files} pinned files ({mode}).")


if __name__ == "__main__":
    try:
        main()
    except (OSError, ValueError, KeyError, TypeError, subprocess.CalledProcessError) as exc:
        sys.exit(f"Verification failed: {exc}")
