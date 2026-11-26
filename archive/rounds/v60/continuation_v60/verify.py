#!/usr/bin/env python3
"""Check the 0.60 claims and the change in the selected obligation graph (Python 3.9+)."""
import argparse
from collections import Counter, defaultdict
from functools import lru_cache
from graphlib import TopologicalSorter
import hashlib
import json
from pathlib import Path
import re
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
CLOSED = "TASK_HOST_XPP_INSTALL"
DERIVED = "HOST_XPP"
BASE = "a0ab1f8786cd1487cdb43f9be686a676242c4e58"


def check(test, reason):
    if not test:
        raise ValueError(reason)


def git(directory, *args):
    run = subprocess.run(["git", "-C", str(directory), *args], capture_output=True)
    if run.returncode:
        raise ValueError(run.stderr.decode(errors="replace").strip() or f"Git failed for {args}")
    return run.stdout


def blob_id(data):
    return hashlib.sha1(b"blob " + str(len(data)).encode() + b"\0" + data).hexdigest()


def digest(data, expected, where):
    check(hashlib.sha256(data).hexdigest() == expected, f"{where}: SHA-256 mismatch")


def distinct(ids, where):
    unique = set(ids)
    check(len(unique) == len(ids), f"{where}: duplicate entries")
    return unique


def at_base(path):
    # Git object reads also work when these files are excluded from a sparse checkout.
    return git(ROOT, "show", f"{BASE}:{path}")


@lru_cache(maxsize=None)
def local_file(path):
    working_file = ROOT / path
    return working_file.read_bytes() if working_file.is_file() else git(ROOT, "show", f"HEAD:{path}")


def inclusive(lines, bounds, where):
    first, last = bounds
    check(type(first) is int and type(last) is int and 1 <= first <= last <= len(lines),
          f"{where}: invalid inclusive range {bounds}")
    return b"".join(lines[first - 1:last])


def predecessor(previous, record):
    old = json.loads(at_base("continuation_v59/claims.json"))
    data = at_base(old["predecessor_ledger"])
    check(blob_id(data) == old["predecessor_ledger_git_blob"], "v0.57 ledger Git blob mismatch")
    ids = [c["id"] for c in json.loads(data)["claims"]]
    ids.extend(c["id"] for d in old["components"] for c in d["claims"])
    known = distinct(ids, "predecessor editions")
    check(len(known) == previous["mathematical_state"]["cumulative_claims"] == record["cumulative_claims"],
          "wrong predecessor claim count")
    return known


def verify_claims(manifest, known, pin, formal_git):
    @lru_cache(maxsize=None)
    def formal_file(path):
        data = git(formal_git, "cat-file", "blob", f"{pin}:{path}")
        return blob_id(data), data.splitlines(keepends=True)

    claims = manifest["claims"]
    added = distinct([c["id"] for c in claims], "new claims")
    check(not added.intersection(known), "new claim ID collides with the predecessor")
    graph = {}
    by_manuscript = defaultdict(set)
    file_oids = {}
    source_ranges = 0
    for c in claims:
        cid, path = c["id"], c["manuscript"]
        lines = local_file(path).splitlines(keepends=True)
        first, last = c["lines"]
        block = inclusive(lines, (first, last), cid)
        check(lines[first - 1].rstrip(b"\r\n") == f"% BEGIN {cid}".encode()
              and lines[last - 1].rstrip(b"\r\n") == f"% END {cid}".encode()
              and block.endswith(b"\n"), f"{cid}: proof block does not match its markers")
        digest(block, c["sha256"], cid)
        by_manuscript[path].add(cid)
        graph[cid] = distinct(c["dependencies"], f"{cid} dependencies")
        check(graph[cid] <= known | added, f"{cid}: unknown claim dependency")

        check(c["source_ranges"], f"{cid}: missing formal source range")
        for binding in c["source_ranges"]:
            src, oid = binding["path"], binding["git_blob"]
            start, end = binding["lines"]
            check(isinstance(src, str) and src.startswith("src/") and src.endswith(".lean"),
                  f"{cid}: invalid formal source path")
            check(type(start) is int and type(end) is int and 1 <= start <= end
                  and re.fullmatch(r"[0-9a-f]{40}", oid) and re.fullmatch(r"[0-9a-f]{64}", binding["sha256"]),
                  f"{cid}: invalid source binding {src}")
            check(file_oids.setdefault(src, oid) == oid, f"{src}: conflicting Git blob IDs")
            if formal_git:
                actual, source_lines = formal_file(src)
                check(actual == oid, f"{src}: pinned source Git blob mismatch")
                excerpt = inclusive(source_lines, (start, end), src)
                digest(excerpt, binding["sha256"], f"{src}:{start}-{end}")
            source_ranges += 1
    list(TopologicalSorter(graph).static_order())
    for path, ids in by_manuscript.items():
        for marker in ("BEGIN", "END"):
            found = re.findall(rb"^% " + marker.encode() + rb" ([A-Z0-9]+)\r?$", local_file(path), re.M)
            check(distinct([x.decode() for x in found], f"{path} {marker}") == ids, f"{path}: unledgered markers")
    reviewed = set()
    for item in manifest["reviews"]:
        digest(local_file(item["path"]), item["sha256"], item["path"])
        path = item["manuscript"]
        digest(local_file(path), item["manuscript_sha256"], path)
        reviewed.add(path)
    check(reviewed == set(by_manuscript), "review coverage differs from the set of new manuscripts")
    return len(added), source_ranges, len(file_oids)


def verify_obligations(previous, current, changes, claims):
    check(changes["closed_leaf"] == CLOSED and changes["derived_node"] == DERIVED, "wrong obligation transition")
    check(changes["base_graph_path"] == "dependency_audit_v0_57/obligation_map.json", "wrong archived base graph")
    check(changes["base_commit"] == BASE, "obligation base commit mismatch")
    graph_bytes = at_base(changes["base_graph_path"])
    digest(graph_bytes, changes["base_graph_sha256"], "archived selected graph")
    old_graph = json.loads(graph_bytes)
    old_nodes = {n["id"]: n for n in old_graph["nodes"]}
    check(changes["closure_contract"] == old_nodes[CLOSED]["contract"], "closure contract changed")
    # Include prior-edition claims as leaves of this edition’s dependency chain.
    edges = {c["id"]: c["dependencies"] for c in claims}
    supporting = {"HXP4"}
    for node in reversed(list(TopologicalSorter(edges).static_order())):
        if node in supporting:
            supporting.update(edges.get(node, []))
    check(supporting == distinct(changes["proof_claims"], "closure claim IDs") and "BR7" in supporting,
          "declared closure witnesses differ from HXP4's dependency chain")
    nodes = changes["nodes"]
    check(distinct([n["id"] for n in nodes], "selected graph") == set(old_nodes), "selected graph IDs changed")
    check(old_nodes[DERIVED]["requires"] == ["CERT_COR_X", CLOSED] and old_nodes[CLOSED]["gate"] == "LEAF"
          and old_nodes["CERT_COR_X"]["status"] == "proved_in_stated_scope", "unexpected original host interface")
    for n in nodes:
        original = old_nodes[n["id"]]
        expected = "proved_in_stated_scope" if n["id"] in (CLOSED, DERIVED) else original["status"]
        check(n["requires"] == original["requires"] and n["status"] == expected
              and n["category"] == original["category"] and n["gate"] == original["gate"],
              f"{n['id']}: unexpected graph transition")
    state, old = current["mathematical_state"], previous["mathematical_state"]
    check(state["selected_graph_nodes"] == old["selected_graph_nodes"] == len(nodes)
          and state["selected_graph_edges"] == old["selected_graph_edges"] == sum(len(n["requires"]) for n in nodes),
          "wrong selected graph counts")
    check(state["global_local_gain"] == old["global_local_gain"], "previous local gain closure changed")
    check(state["new_whole_obligation_closures"] == [CLOSED], "unexpected list of whole closures")
    open_ids = set()
    for key, count in (("shared_open_ids", "shared_rh_grh_open"),
                       ("additional_grh_open_ids", "additional_unrestricted_dirichlet_grh_open")):
        group = distinct(current[key], key)
        original = distinct(previous[key], f"predecessor {key}")
        check(len(original) == old[count] and group == original - {CLOSED} and len(group) == state[count],
              f"{key}: incorrect remaining obligations")
        check(distinct(changes[key], f"graph {key}") == group, f"graph {key} disagrees with checkpoint")
        check(not open_ids.intersection(group), "overlap between the two open obligation lists")
        open_ids.update(group)
    check(distinct(changes["remaining"], "remaining obligation IDs") == open_ids, "remaining list disagrees")
    remaining = changes["remaining_contracts"]
    check(distinct([r["id"] for r in remaining], "remaining contracts") == open_ids,
          "remaining contract records differ from remaining IDs")
    for row in remaining:
        check(all(row[k] == old_nodes[row["id"]][k] for k in ("title", "category", "contract")),
              f"{row['id']}: remaining contract changed")
    check(state["whole_open_obligations"] == old["whole_open_obligations"] - 1 == len(open_ids),
          "wrong whole-open count")
    check(current["whole_open_by_class"] == dict(Counter(old_nodes[i]["category"] for i in open_ids)),
          "wrong counts by obligation class")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--formal-git", type=Path, metavar="PATH",
                        help="also verify every source excerpt against the pinned Git tree (worktree, bare repo, or .git)")
    args = parser.parse_args()
    formal = args.formal_git
    if formal and formal.is_file() and formal.name == ".git":
        formal = formal.parent
    manifest = json.loads(local_file("continuation_v60/claims.json"))
    current = json.loads(local_file("CURRENT_CHECKPOINT_v0_60.json"))
    previous = json.loads(at_base("CURRENT_CHECKPOINT_v0_59.json"))
    check(manifest["base_commit"] == BASE == current["predecessor"]["reconstruction_commit"], "base commit mismatch")
    pin = previous["original_source"]["commit"]
    check(manifest["formal_pin"] == pin == current["original_source"]["commit"], "formal source pin mismatch")
    if formal:
        tree = git(formal, "rev-parse", pin + "^{tree}").decode().strip()
        check(tree == previous["original_source"]["tree"] == current["original_source"]["tree"], "formal tree mismatch")
    known = predecessor(previous, current["predecessor"])
    n, ranges, files = verify_claims(manifest, known, pin, formal)
    state = current["mathematical_state"]
    check(state["new_claims_in_this_package"] == n and state["cumulative_claims"] == len(known) + n,
          "new or cumulative claim count mismatch")
    verify_obligations(previous, current, json.loads(local_file("continuation_v60/obligations.json")), manifest["claims"])
    mode = "verified against Git" if formal else "indexed; pass --formal-git to verify source bytes"
    print(f"Verified {n} new claims, {len(known) + n} cumulative claims, {state['whole_open_obligations']} open obligations.")
    print(f"{ranges} source ranges in {files} pinned files ({mode}).")


if __name__ == "__main__":
    try:
        main()
    except (OSError, ValueError, KeyError, TypeError) as exc:
        sys.exit(f"Verification failed: {exc}")
