#!/usr/bin/env python3
"""Verify edition 0.59's new manuscript, source bindings and inventory with Git and Python 3.9+."""
import argparse
from functools import lru_cache
from graphlib import TopologicalSorter
from hashlib import sha1, sha256
import json
from pathlib import Path
import re
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
OLD_CHECKPOINT = "CURRENT_CHECKPOINT_v0_58.json"


def require(condition, message):
    if not condition:
        raise ValueError(message)


def read_json(path):
    return json.loads(path.read_bytes())


def git(repository, *args):
    cmd = ["git", "-C", str(repository), *args]
    result = subprocess.run(cmd, capture_output=True)
    if result.returncode:
        raise ValueError(result.stderr.decode(errors="replace").strip() or f"Git failed: {args}")
    return result.stdout


def historical_file(path):
    local = ROOT / path
    return local.read_bytes() if local.is_file() else git(ROOT, "show", "HEAD:" + path)


def unique(items, context):
    result = set(items)
    require(len(result) == len(items), f"{context}: duplicate IDs")
    return result


def line_slice(lines, bounds, where):
    first, last = bounds
    require(1 <= first <= last <= len(lines), f"{where}: invalid inclusive range {bounds}")
    return b"".join(lines[first - 1:last])


def git_blob_id(data):
    return sha1(b"blob " + str(len(data)).encode() + b"\0" + data).hexdigest()


def check_hash(data, digest, where):
    require(sha256(data).hexdigest() == digest, f"{where}: SHA-256 mismatch")


def objects(value):
    """Walk all source bindings, including non-claim consumer and handoff records."""
    if isinstance(value, dict):
        yield value
        for child in value.values():
            yield from objects(child)
    elif isinstance(value, list):
        for child in value:
            yield from objects(child)


def check_source_bindings(provenance, source_file, pin):
    require(provenance["source_commit"] == pin, "component source commit differs from v0.58")
    blobs = provenance.get("source_blobs", {})
    for path, oid in blobs.items():
        require(source_file(path)[1] == oid, f"{path}: source_blobs Git ID mismatch")
    count = 0
    for binding in objects(provenance):
        if "path" not in binding:
            continue
        path = binding["path"]
        data, oid, lines = source_file(path)
        bounds = binding["lines"] if "lines" in binding else [binding["first"], binding["last"]]
        excerpt = line_slice(lines, bounds, path)
        for name in ("git_blob", "git_blob_oid"):
            if name in binding:
                require(binding[name] == oid, f"{path}: {name} mismatch")
        require(path in blobs or any(k in binding for k in ("git_blob", "git_blob_oid", "file_sha256")),
                f"{path}: no file identity supplied")
        if "file_sha256" in binding:
            check_hash(data, binding["file_sha256"], path)
        if "range_sha256" in binding:
            check_hash(excerpt, binding["range_sha256"], f"{path}:{bounds}")
        if "url" in binding:
            url = f"https://github.com/CocoSgt/riemann-hypothesis-lean/blob/{pin}/{path}#L{bounds[0]}-L{bounds[1]}"
            require(binding["url"] == url, f"{path}: permalink disagrees with pinned range")
        count += 1
    return count


def verify_component(component, source_file, pin, dependencies):
    directory = ROOT / component["directory"]
    manuscript = (directory / "main.tex").read_bytes()
    lines = manuscript.splitlines(keepends=True)
    check_hash(manuscript, component["manuscript_sha256"], directory)
    check_hash((directory / "review.md").read_bytes(), component["review_sha256"], directory / "review.md")
    provenance_path = directory / "provenance.json"
    require(ROOT / component["source_provenance"] == provenance_path, f"{directory}: wrong provenance path")
    provenance_bytes = provenance_path.read_bytes()
    check_hash(provenance_bytes, component["source_provenance_sha256"], provenance_path)
    provenance = json.loads(provenance_bytes)
    for key in ("proof_sha256", "manuscript_sha256"):
        if key in provenance:
            check_hash(manuscript, provenance[key], directory)
    source_claims = provenance["claims"]
    if isinstance(source_claims, list):
        unique([c["id"] for c in source_claims], directory)
        source_claims = {c["id"]: c for c in source_claims}
    ids = unique([c["id"] for c in component["claims"]], directory)
    require(ids == set(source_claims), f"{directory}: inventory and local ledger disagree")
    for marker in ("BEGIN", "END"):
        found = re.findall(rb"^% " + marker.encode() + rb" ([A-Z0-9]+)\r?$", manuscript, re.M)
        require(unique([s.decode() for s in found], directory) == ids, f"{directory}: {marker} markers disagree")
    for claim in component["claims"]:
        name, bounds = claim["id"], claim["lines"]
        require(name not in dependencies, f"{name}: ID already present")
        dependencies[name] = unique(claim["dependencies"], name + " dependencies")
        local = source_claims[name]
        block = line_slice(lines, bounds, name)
        first, last = bounds
        require(lines[first - 1].rstrip(b"\r\n") == f"% BEGIN {name}".encode()
                and lines[last - 1].rstrip(b"\r\n") == f"% END {name}".encode()
                and lines[last - 1].endswith(b"\n"), f"{name}: mismatched block delimiters")
        check_hash(block, claim["sha256"], name)
        for key in ("block_sha256", "proof_block_sha256"):
            if key in local:
                check_hash(block, local[key], name)
        if "tex_anchor" in local:
            anchor = ("\\label{" + local["tex_anchor"] + "}").encode()
            require(anchor in block, f"{name}: missing TeX label")
        if "tex_lines" in local:
            require(local["tex_lines"] == bounds, f"{name}: local manuscript range mismatch")
        required = local.get("proof_dependencies", local.get("prior_claims_used", []))
        require(set(required) <= set(dependencies[name]), f"{name}: missing a component dependency")
    return check_source_bindings(provenance, source_file, pin)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", type=Path, default=ROOT / "formal_source",
                        help="bare or ordinary Git repository containing the pinned formal-source commit")
    args = parser.parse_args()
    old = json.loads(historical_file(OLD_CHECKPOINT))
    pin = old["original_source"]["commit"]
    git(args.source, "cat-file", "-e", pin + "^{commit}")

    @lru_cache(maxsize=None)
    def source_file(path):
        data = git(args.source, "cat-file", "blob", f"{pin}:{path}")
        return data, git_blob_id(data), data.splitlines(keepends=True)

    manifest = read_json(ROOT / "continuation_v59/claims.json")
    current = read_json(ROOT / "CURRENT_CHECKPOINT_v0_59.json")
    require(pin == manifest["source_commit"] == current["original_source"]["commit"], "formal source pin mismatch")
    tree = git(args.source, "rev-parse", pin + "^{tree}").decode().strip()
    require(tree == old["original_source"]["tree"] == current["original_source"]["tree"], "formal tree mismatch")
    require(manifest["predecessor_ledger"] == "provenance.json", "unexpected predecessor ledger")
    historical = historical_file(manifest["predecessor_ledger"])
    require(git_blob_id(historical) == manifest["predecessor_ledger_git_blob"], "predecessor Git blob mismatch")
    inventory = json.loads(historical_file("continuation_v58/reconstruction_inventory.json"))
    old_file = next(f for f in inventory["members"] if f["path"] == "provenance.json")
    check_hash(historical, old_file["sha256"], "preserved predecessor ledger")
    old_claims = json.loads(historical)["claims"]
    previous = unique([c["id"] for c in old_claims], "predecessor ledger")
    require(len(previous) == old["mathematical_state"]["cumulative_claims"], "predecessor count mismatch")
    del historical, old_claims
    require(current["predecessor"]["cumulative_claims"] == len(previous), "checkpoint predecessor count mismatch")
    dependencies = {}
    source_ranges = sum(verify_component(c, source_file, pin, dependencies) for c in manifest["components"])
    new_ids = set(dependencies)
    require(not previous.intersection(new_ids), "new IDs collide with the predecessor ledger")
    for name, edges in dependencies.items():
        require(set(edges) <= previous | new_ids, f"{name}: unknown dependency IDs")
    list(TopologicalSorter(dependencies).static_order())
    state = current["mathematical_state"]
    baseline = old["mathematical_state"]
    require(state["new_claims_in_this_package"] == len(new_ids), "new claim count mismatch")
    require(state["cumulative_claims"] == len(previous) + len(new_ids), "cumulative count mismatch")
    for key in ("new_whole_obligation_closures", "global_local_gain", "selected_graph_nodes", "selected_graph_edges",
                "whole_open_obligations", "shared_rh_grh_open", "additional_unrestricted_dirichlet_grh_open"):
        require(state[key] == baseline[key], f"checkpoint {key} differs from v0.58")
    groups = []
    for key, count in (("shared_open_ids", "shared_rh_grh_open"),
                       ("additional_grh_open_ids", "additional_unrestricted_dirichlet_grh_open")):
        group = unique(current[key], key)
        require(group == set(old[key]) and len(group) == state[count], f"checkpoint {key} mismatch")
        groups.append(group)
    require(len(groups[0] | groups[1]) == state["whole_open_obligations"], "whole open ID count mismatch")
    register = json.loads(historical_file("dependency_audit_v0_57/remaining_leaf_register.json"))
    require(current["whole_open_by_class"] == register["category_counts"], "whole open class counts mismatch")
    print(f"Verified {len(new_ids)} new claims, {len(previous) + len(new_ids)} cumulative claims, "
          f"{state['whole_open_obligations']} open obligations, {source_ranges} source ranges "
          f"in {source_file.cache_info().currsize} pinned files.")


if __name__ == "__main__":
    try:
        main()
    except (ValueError, KeyError, OSError, StopIteration) as exc:
        sys.exit(f"Verification failed: {exc}")
