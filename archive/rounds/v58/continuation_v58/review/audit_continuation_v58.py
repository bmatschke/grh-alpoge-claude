#!/usr/bin/env python3
"""Independent preservation and offline-continuation audit for release v0.58.

This packaging release has no new mathematics.  Its primary baseline is the
actually delivered v0.57 ZIP.  No v0.56 audit or Lean build is replayed here.
Run only after root announces that the payload, helpers and handoff are frozen.
"""
from pathlib import Path, PurePosixPath
import argparse
import collections
import hashlib
import json
import os
import re
import shlex
import shutil
import stat
import subprocess
import sys
import tarfile
import tempfile
import zipfile

PIN = "7cbf7a0c32fca1badf05931879a37c3f8a2b03b4"
TREE = "02cfa4b3810fc22f6d43b317409071f380a5f1b4"
BASELINE_SHA = "b326cc620d0064eda3126cce27f3dafd31e83d8516741aaf2ffcac450788bd33"
BASELINE_BYTES = 535525399
BASELINE_MEMBERS = 9551
SOURCE_FILES = 175192
SOURCE_BYTES = 1030545459
CAP = 536870912

ap = argparse.ArgumentParser(description=__doc__)
ap.add_argument("--package-root", type=Path, required=True)
ap.add_argument("--baseline", type=Path, required=True)
ap.add_argument("--original-source", type=Path, required=True)
ap.add_argument("--payload", default="continuation_v58/reconstruction_snapshot.tar.xz")
ap.add_argument("--unpack-command", required=True,
                help="JSON argv using {python}, {package}, {reconstruction} placeholders")
ap.add_argument("--restore-command",
                help="JSON argv using {python}, {package}, {source} placeholders")
ap.add_argument("--restored-source", type=Path,
                help="Reuse the one already executed full independent source restore")
ap.add_argument("--restore-execution-record", default="continuation_v58/review/source_restore_execution.json")
ap.add_argument("--archive", type=Path, help="Optional finished outer ZIP; checked without modifying it")
ap.add_argument("--output", type=Path,
                help="Defaults to continuation_v58/review/handoff_audit.json")
args = ap.parse_args()
if not args.restore_command and not args.restored_source:
    ap.error("supply --restore-command or --restored-source")
ROOT = args.package_root.resolve()
BASELINE = args.baseline.resolve()
ORIGINAL = args.original_source.resolve()
OUTPUT = args.output or ROOT / "continuation_v58/review/handoff_audit.json"
errors, checks, bindings = [], [], {}
baseline_members = {}


def phase(name, **details):
    print(json.dumps({"phase": name, **details}, ensure_ascii=False), flush=True)


def need(ok, label, detail=None):
    if ok:
        checks.append(label)
    else:
        errors.append({"check": label, "detail": detail})


def digest_stream(stream):
    h, count = hashlib.sha256(), 0
    for part in iter(lambda: stream.read(1024 * 1024), b""):
        h.update(part)
        count += len(part)
    return h.hexdigest(), count


def file_hash(path):
    with path.open("rb") as stream:
        return digest_stream(stream)[0]


def raw(rel):
    data = (ROOT / rel).read_bytes()
    bindings[rel] = hashlib.sha256(data).hexdigest()
    return data


def bind_file(rel):
    bindings[rel] = file_hash(ROOT / rel)
    return bindings[rel]


def read(rel):
    return json.loads(raw(rel))


def safe_member(name):
    path = PurePosixPath(name)
    return bool(name) and not path.is_absolute() and ".." not in path.parts and "\\" not in name


def git(repo, *argv, input=None):
    return subprocess.check_output(["git", "-C", str(repo), *argv], input=input)


def tree_rows(repo):
    rows = []
    for record in git(repo, "ls-tree", "-r", "-l", "-z", PIN).split(b"\0"):
        if not record:
            continue
        header, path = record.split(b"\t", 1)
        mode, kind, oid, size = header.decode().split()
        rows.append({"path": path.decode(), "mode": mode, "type": kind,
                     "oid": oid, "bytes": int(size)})
    return rows


phase("checking_primary_baseline")
need(BASELINE.stat().st_size == BASELINE_BYTES, "delivered v57 archive byte length")
need(file_hash(BASELINE) == BASELINE_SHA, "delivered v57 archive SHA256")
with zipfile.ZipFile(BASELINE) as old:
    old_names = old.namelist()
    need(len(old_names) == len(set(old_names)) == BASELINE_MEMBERS,
         "delivered v57 has exactly 9551 distinct members")
    need(all(safe_member(n) and not n.endswith("/") for n in old_names),
         "baseline member names are canonical relative file paths")
    manifest_bytes = old.read("SHA256SUMS")
    for line in manifest_bytes.decode().splitlines():
        expected, name = line.split("  ", 1)
        need(name not in baseline_members, "unique baseline manifest path: " + name)
        baseline_members[name] = {"sha256": expected, "bytes": old.getinfo(name).file_size}
    baseline_members["SHA256SUMS"] = {
        "sha256": hashlib.sha256(manifest_bytes).hexdigest(), "bytes": len(manifest_bytes)}
    need(set(baseline_members) == set(old_names), "baseline manifest covers every delivered member")
    prior_audit = json.loads(old.read("reviews_v0_57/integration_arithmetic_common_frame.json"))
    old_stats = json.loads(old.read("integration_stats_v0_57.json"))
    old_graph = json.loads(old.read("dependency_audit_v0_57/obligation_map.json"))
    old_routes = json.loads(old.read("dependency_audit_v0_57/route_coverage.json"))

phase("stream_verifying_reconstruction_payload")
payload = ROOT / args.payload
payload_hash = bind_file(args.payload)
seen_payload, payload_bytes = set(), 0
with tarfile.open(payload, "r|*") as archive:
    for member in archive:
        if member.isdir():
            need(safe_member(member.name), "safe reconstruction directory")
            continue
        name = member.name
        need(safe_member(name) and member.isfile(), "ordinary safe reconstruction member: " + name)
        need(name in baseline_members and name not in seen_payload,
             "payload has one original baseline member: " + name)
        if not member.isfile():
            continue
        stream = archive.extractfile(member)
        actual, size = digest_stream(stream)
        stream.close()
        expected = baseline_members.get(name, {})
        need(actual == expected.get("sha256") and size == expected.get("bytes"),
             "exact delivered member bytes in solid payload: " + name)
        seen_payload.add(name)
        payload_bytes += size
need(seen_payload == set(baseline_members), "solid payload preserves all 9551 original members")
bundle = read("continuation_v58/reconstruction_bundle.json")
inventory = read("continuation_v58/reconstruction_inventory.json")
need(bundle["baseline_archive_sha256"] == inventory["baseline_archive_sha256"] == BASELINE_SHA,
     "reconstruction metadata identifies the delivered v57 baseline")
need(bundle["member_count"] == inventory["member_count"] == BASELINE_MEMBERS and
     bundle["uncompressed_bytes"] == inventory["uncompressed_bytes"] == payload_bytes,
     "reconstruction metadata has exact restored inventory totals")
need({r["path"]: {"sha256": r["sha256"], "bytes": r["bytes"]} for r in inventory["members"]} == baseline_members,
     "reconstruction inventory records each exact delivered byte string")
for key in ["archive", "inventory"]:
    entry = bundle[key]
    rel = "continuation_v58/" + entry["file"]
    need(bind_file(rel) == entry["sha256"] and (ROOT / rel).stat().st_size == entry["bytes"],
         "reconstruction bundle binds its exact " + key)

# The accepted expanded author workspace must also remain unchanged. These
# work-relative bindings are directly consumable by the new release packager.
for name, expected in baseline_members.items():
    need((ROOT / name).is_file(), "unchanged expanded v57 member exists: " + name)
    if (ROOT / name).is_file():
        need(bind_file(name) == expected["sha256"], "unchanged expanded v57 member bytes: " + name)

phase("checking_inherited_mathematical_state")
need(prior_audit["status"] == "PASS" and prior_audit["errors"] == [], "final inherited v57 audit passes")
need(len(prior_audit["input_bindings"]) == 450, "all 450 inherited input bindings are declared")
for name, expected in prior_audit["input_bindings"].items():
    need(baseline_members.get(name, {}).get("sha256") == expected,
         "delivered payload retains the exact independently audited input: " + name)
need(old_stats == {"new_claims": 101, "cumulative_claims": 3746,
                   "selected_nodes": 121, "selected_edges": 161, "open_count": 24,
                   "open_categories": {"C": 17, "B": 7}, "shared_open": 17,
                   "extra_grh_open": 7, "new_source_files_checked": 118,
                   "new_unique_source_ranges_checked": 205}, "exact inherited v57 mathematics inventory")
nodes = {n["id"]: n for n in old_graph["nodes"]}
closed_statuses = {"proved_in_stated_scope", "published_application_checked", "complete", "closed"}
open_ids = {k for k, n in nodes.items() if n["gate"] == "LEAF" and n["status"] not in closed_statuses}
need(len(nodes) == 121 and sum(len(n["requires"]) for n in nodes.values()) == 161,
     "selected 121-node/161-edge graph is retained")
need(len(open_ids) == 24 and collections.Counter(nodes[k]["category"] for k in open_ids) == {"C": 17, "B": 7},
     "same 24 whole open obligations and categories")
need(len(old_routes["shared_open_leaf_ids"]) == 17 and len(old_routes["dirichlet_grh_only_open_leaf_ids"]) == 7,
     "separate shared and additional-GRH partition retained")
need(set(old_routes["shared_open_leaf_ids"]) | set(old_routes["dirichlet_grh_only_open_leaf_ids"]) == open_ids,
     "route partition covers precisely the open register")
need(nodes["GLOBAL_LOCAL_GAIN"]["status"] == "proved_in_stated_scope", "GLOBAL_LOCAL_GAIN remains closed")

phase("checking_complete_source_manifest")
need(git(ORIGINAL, "rev-parse", "HEAD").decode().strip() == PIN, "accepted original source checkout pin")
manifest = read("continuation_v58/source/tree_manifest.json")
raw_commit = raw("continuation_v58/source/accepted_commit.raw")
source_archive_hash = bind_file("continuation_v58/source/formal_source.tar.xz")
source_bundle = read("continuation_v58/source/source_bundle.json")
need(source_bundle["source_commit"] == PIN and source_bundle["source_tree"] == TREE,
     "source bundle declares the original identifiers")
for key in ["archive", "tree_manifest", "raw_commit"]:
    entry = source_bundle[key]
    rel = "continuation_v58/source/" + entry["file"]
    need(bind_file(rel) == entry["sha256"] and (ROOT / rel).stat().st_size == entry["bytes"],
         "source bundle binds its exact " + key)
expected_rows = tree_rows(ORIGINAL)
need(manifest["commit"] == PIN and manifest["tree"] == TREE, "source manifest has exact accepted commit/tree")
need(manifest["files"] == expected_rows, "complete source manifest matches every original Git tree entry")
need(manifest["tracked_file_count"] == len(expected_rows) == SOURCE_FILES and
     manifest["tracked_bytes"] == sum(r["bytes"] for r in expected_rows) == SOURCE_BYTES,
     "complete source file and byte counts")
need(all(r["type"] == "blob" for r in expected_rows), "no omitted source submodule prerequisite")
need(raw_commit == git(ORIGINAL, "cat-file", "commit", PIN), "raw original commit is preserved exactly")
commit_id = hashlib.sha1(b"commit " + str(len(raw_commit)).encode() + b"\0" + raw_commit).hexdigest()
need(commit_id == PIN and hashlib.sha256(raw_commit).hexdigest() == manifest["raw_commit_sha256"],
     "raw commit independently reconstructs the original Git identifier")

# This source index is navigation, not a new mathematical producer or closure.
index = read("continuation_v58/next_tasks_source_index.json")
raw("continuation_v58/next_tasks_source_index.txt")
need(index["artifact_version"] == "0.58" and index["handoff_only"] is True and
     index["new_mathematical_claims"] == 0 and index["closure_changes"] == [],
     "next-task index adds no proof claim or closure")
need(index["source_commit"] == PIN and "v0.57" in index["current_human_checkpoint"]["baseline"],
     "next-task index starts from delivered v57 at the accepted source pin")
need(index["current_human_checkpoint"]["cumulative_claims"] == 3746 and
     index["current_human_checkpoint"]["whole_open_obligations"] == 24,
     "next-task index records the current unchanged mathematical inventory")
need({t["id"] for t in index["tasks"]} == {"LOCAL", "RANK3", "CARTIER", "PERIOD"},
     "source-index task cards cover the four actual next producer lanes")
for item in index["planning_inputs"]:
    need(baseline_members.get(item["path"], {}).get("sha256") == item["sha256"],
         "next-task index uses a current preserved planning input: " + item["path"])
source_by_path = {r["path"]: r for r in expected_rows}

restoration_results = {}
with tempfile.TemporaryDirectory(prefix="rh_v58_independent_restore_", dir=ROOT.parent) as temporary:
    temporary = Path(temporary)
    reconstruction = temporary / "reconstruction"
    source = args.restored_source.resolve() if args.restored_source else temporary / "formal_source"
    substitutions = {"python": sys.executable, "package": str(ROOT),
                     "reconstruction": str(reconstruction), "source": str(source)}

    # The outer ZIP makes these six unchanged v57 readers directly available.
    # Reproduce that real restart state before the single full restore.
    reconstruction.mkdir()
    direct_readers = read("CURRENT_CHECKPOINT_v0_58.json")["direct_reading_files"]
    need(len(direct_readers) == len({r["path"] for r in direct_readers}) == 6,
         "fresh reconstruction test starts with the six direct outer readers")
    for row in direct_readers:
        need(safe_member(row["path"]) and baseline_members.get(row["path"]) ==
             {"sha256": row["sha256"], "bytes": row["bytes"]},
             "seeded direct reader is an exact delivered baseline member: " + row["path"])
        target = reconstruction / row["path"]
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(ROOT / row["path"], target)

    def run_helper(label, command_json):
        command = [part.format(**substitutions) for part in json.loads(command_json)]
        need(command[0] == sys.executable and str(ROOT) in command[1], label + ": supplied local Python helper")
        phase(label, command=command)
        result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
        log_rel = "continuation_v58/review/" + label + ".log"
        (ROOT / log_rel).write_text(result.stdout)
        bindings[log_rel] = file_hash(ROOT / log_rel)
        need(result.returncode == 0, label + ": offline helper succeeds", result.stdout[-4000:])
        if result.returncode:
            raise RuntimeError(label + " failed; no continuation PASS can be issued")
        restoration_results[label] = {"returncode": 0, "command": command,
                                      "log": log_rel, "log_sha256": bindings[log_rel]}
        if label == "unpack_test":
            helper_result = json.loads(result.stdout[result.stdout.index("{"):])
            need(helper_result["status"] == "PASS" and
                 helper_result["members_verified"] == BASELINE_MEMBERS and
                 helper_result["new_files_restored"] == BASELINE_MEMBERS - 6 and
                 helper_result["existing_identical_files_retained"] == 6 and
                 not helper_result["network_used"] and
                 helper_result["new_mathematical_claims"] == 0,
                 "single full restore accepts the six existing readers and restores the other 9545")
            restoration_results[label].update({"full_restore_executions": 1,
                                               "helper_result": helper_result})

    run_helper("unpack_test", args.unpack_command)
    phase("checking_fresh_reconstruction")
    for name, expected in baseline_members.items():
        path = reconstruction / name
        need(path.is_file(), "fresh restored member exists: " + name)
        if path.is_file():
            need(path.stat().st_size == expected["bytes"] and file_hash(path) == expected["sha256"],
                 "fresh restored member equals delivered bytes: " + name)
    restored_names = {p.relative_to(reconstruction).as_posix() for p in reconstruction.rglob("*") if p.is_file()}
    need(restored_names == set(baseline_members), "fresh reconstruction has exactly the delivered member inventory")
    restored_prior_audit = json.loads((reconstruction / "reviews_v0_57/integration_arithmetic_common_frame.json").read_text())
    need(restored_prior_audit == prior_audit, "fresh reconstruction retains the complete accepted audit")

    if args.restored_source:
        execution = read(args.restore_execution_record)
        need(execution["status"] == "PASS" and execution["returncode"] == 0,
             "the single separately executed full source restore passed")
        need(execution["destination"] == str(source), "the source execution record names this exact fresh tree")
        for rel, expected in execution["input_bindings"].items():
            need(bind_file(rel) == expected, "source restore used this exact frozen bundle/helper input: " + rel)
        need(bind_file(execution["log"]) == execution["log_sha256"], "exact full source-restoration execution log")
        result = execution["helper_result"]
        need(result["status"] == "ok" and result["source_commit"] == PIN and
             result["source_tree"] == TREE and result["tracked_files_verified"] == SOURCE_FILES and
             result["tracked_bytes_verified"] == SOURCE_BYTES and not result["network_used"] and
             not result["lean_build_run"], "full offline source restore has the required exact output")
        restoration_results["source_restore_test"] = {
            "execution_record": args.restore_execution_record,
            "execution_record_sha256": bindings[args.restore_execution_record],
            "full_restore_executions": 1,
            "result": "PASS",
        }
    else:
        run_helper("source_restore_test", args.restore_command)
    phase("checking_fresh_source_repository")
    need(git(source, "rev-parse", "HEAD").decode().strip() == PIN, "offline restored source has original HEAD")
    need(git(source, "rev-parse", "HEAD^{tree}").decode().strip() == TREE, "offline restored source has original tree")
    need(tree_rows(source) == expected_rows, "every restored source path, mode, size and object identifier matches")
    need(git(source, "cat-file", "commit", PIN) == raw_commit, "offline source retains exact original commit bytes")
    need(not (source / ".git/objects/info/alternates").exists(), "restored source has no old-checkout object dependency")
    check = subprocess.run(["git", "-C", str(source), "fsck", "--full", "--no-reflogs"],
                           stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
    need(check.returncode == 0, "fresh shallow repository has complete required Git objects", check.stdout[-3000:])

    regular = [r for r in expected_rows if r["mode"] != "120000"]
    need(all("\n" not in r["path"] and not r["path"].startswith('"') for r in regular),
         "source file paths are unambiguous for batched raw hashing")
    path_input = "".join(r["path"] + "\n" for r in regular).encode()
    actual_ids = git(source, "hash-object", "--no-filters", "--stdin-paths", input=path_input).decode().splitlines()
    need(actual_ids == [r["oid"] for r in regular], "every restored working-tree file has exact original raw bytes")
    for row in expected_rows:
        path = source / row["path"]
        if row["mode"] == "120000":
            need(path.is_symlink(), "restored source symbolic link mode: " + row["path"])
            target = os.readlink(path).encode()
            oid = hashlib.sha1(b"blob " + str(len(target)).encode() + b"\0" + target).hexdigest()
            need(oid == row["oid"], "restored source symbolic link content: " + row["path"])
        else:
            need(bool(path.stat().st_mode & stat.S_IXUSR) == (row["mode"] == "100755"),
                 "restored source executable mode: " + row["path"])

    phase("checking_next_task_sources_and_ranges")
    checked_sources, checked_ranges, checked_imports = set(), set(), set()
    source_cache = {}
    def source_bytes(path):
        if path not in source_cache:
            source_cache[path] = (source / path).read_bytes()
        return source_cache[path]
    for item in index["indexed_sources"]:
        path = item["path"]
        data = source_bytes(path)
        need(item["source_commit"] == PIN and hashlib.sha256(data).hexdigest() == item["file_sha256"] and
             len(data) == item["bytes"], "next-task exact primary source: " + path)
        checked_sources.add(path)
        lines = data.splitlines(keepends=True)
        need(len(lines) == item["line_count"], "next-task primary source line count: " + path)
        for row in item["declarations"] + item["reading_ranges"]:
            a, b = row["line_start"], row["line_end"]
            need(1 <= a <= b <= len(lines), "next-task source range lies in its actual file")
            part = b"".join(lines[a-1:b])
            need(hashlib.sha256(part).hexdigest() == row["range_sha256"],
                 "next-task exact declaration/reading range: " + path + ":" + str(a) + "-" + str(b))
            if row.get("header"):
                need(row["header"] in part.decode(), "next-task declaration header is literal: " + row["name"])
            checked_ranges.add((path, a, b))
        for row in item["immediate_imports"]:
            need(row["module"] in lines[row["line"]-1].decode(), "next-task import is at its recorded source line")
            if row["kind"] == "project":
                data_i = source_bytes(row["path"])
                need(row["source_commit"] == PIN and hashlib.sha256(data_i).hexdigest() == row["sha256"],
                     "next-task exact immediate project import: " + row["path"])
                checked_imports.add(row["path"])
            else:
                need(row.get("source_commit") != PIN, "external dependency stays distinct from accepted RH source")
    for row in index["immediate_project_import_files"]:
        data = source_bytes(row["path"])
        need(row["path"] in checked_imports and hashlib.sha256(data).hexdigest() == row["sha256"] and
             len(data) == row["bytes"], "next-task aggregate imported-source binding: " + row["path"])
    need(len(checked_sources) == len(index["indexed_sources"]), "next-task primary file inventory has no duplicate")
    need(checked_imports == {r["path"] for r in index["immediate_project_import_files"]},
         "next-task import inventory is exact")
    need(index["source_availability"]["missing_requested_project_sources"] == [] and
         index["source_availability"]["unresolved_selectors_or_imports"] == [],
         "next-task index has no missing project source or unresolved selector")
    lake_bytes = source_bytes("lake-manifest.json")
    packages = {r["name"]: r for r in json.loads(lake_bytes)["packages"]}
    for name, dependency in index["source_availability"]["external_dependencies"].items():
        need(packages[name]["rev"] == dependency["commit"] != PIN and
             hashlib.sha256(lake_bytes).hexdigest() == dependency["manifest_sha256"],
             "external dependency retains its actual original separate revision: " + name)
        for supporting in dependency.get("already_preserved_supporting_sources", []):
            rel = supporting["snapshot_path"]
            data = (reconstruction / rel).read_bytes()
            a, b = supporting["line_start"], supporting["line_end"]
            part = b"".join(data.splitlines(keepends=True)[a-1:b])
            need(hashlib.sha256(data).hexdigest() == supporting["sha256"] and
                 hashlib.sha256(part).hexdigest() == supporting["range_sha256"] and
                 supporting["source_commit"] == dependency["commit"],
                 "already preserved external definition and range: " + supporting["path"])

phase("checking_frozen_handoff_and_scope")
checkpoint = read("CURRENT_CHECKPOINT_v0_58.json")
state = checkpoint["mathematical_state"]
need(checkpoint["package_version"] == "0.58" and checkpoint["mathematical_edition"] == "0.57",
     "package version is distinguished from the unchanged mathematical edition")
need(checkpoint["primary_baseline"] == {"archive": "RH_reconstruction_v0_57.zip", "sha256": BASELINE_SHA,
                                      "bytes": BASELINE_BYTES, "members": BASELINE_MEMBERS},
     "portable checkpoint starts from the exact delivered v57 archive")
for key, expected in {"commit": PIN, "tree": TREE, "tracked_files": SOURCE_FILES,
                      "tracked_bytes": SOURCE_BYTES, "complete_tracked_project_source": True,
                      "offline_exact_shallow_git_restore": True}.items():
    need(checkpoint["original_source"][key] == expected, "checkpoint accurately describes the tested source: " + key)
need(checkpoint["restore_commands"] == ["python3 continuation_v58/unpack_reconstruction.py",
      "python3 continuation_v58/restore_source.py --destination formal_source"],
     "checkpoint commands match the supplied tested offline helpers")
need(checkpoint["independent_handoff_audit"] == "continuation_v58/review/handoff_audit.json",
     "checkpoint names the actual independent handoff audit")
for key, expected in {"new_claims_in_this_package": 0, "cumulative_claims": 3746,
                      "whole_open_obligations": 24, "selected_graph_nodes": 121,
                      "selected_graph_edges": 161, "shared_rh_grh_open": 17,
                      "additional_unrestricted_dirichlet_grh_open": 7,
                      "new_whole_obligation_closures": []}.items():
    need(state[key] == expected, "unchanged mathematical state: " + key)
need(set(checkpoint["shared_open_ids"]) == set(old_routes["shared_open_leaf_ids"]) and
     set(checkpoint["additional_grh_open_ids"]) == set(old_routes["dirichlet_grh_only_open_leaf_ids"]),
     "portable checkpoint has the exact whole-obligation route partition")
for row in checkpoint["direct_reading_files"]:
    need(baseline_members.get(row["path"]) == {"sha256": row["sha256"], "bytes": row["bytes"]},
         "direct reader is an unchanged delivered v57 member: " + row["path"])
    need(bind_file(row["path"]) == row["sha256"], "direct reader current bytes: " + row["path"])
for outer, inner in [("RH_START_HERE_v0_58.txt", "continuation_v58/START_HERE.txt"),
                     ("RH_NEW_CHAT_PROMPT_v0_58.txt", "continuation_v58/NEW_CHAT_PROMPT.txt")]:
    need(raw(outer) == raw(inner), "outer entry point equals the complete handoff text: " + outer)
for key, rel in checkpoint["entry_points"].items():
    need((ROOT / rel).is_file() and (rel in baseline_members or rel in bindings or rel.startswith("continuation_v58/")),
         "portable entry point is available directly or after the documented unpack: " + key)
    bind_file(rel)
start = raw("continuation_v58/START_HERE.txt").decode()
prompt = raw("continuation_v58/NEW_CHAT_PROMPT.txt").decode()
source_access = raw("continuation_v58/SOURCE_ACCESS.txt").decode()
need(all(cid in start for cid in open_ids), "START_HERE contains the complete exact 24-ID register")
need(all(cid in prompt for cid in old_routes["dirichlet_grh_only_open_leaf_ids"]),
     "new-chat prompt preserves all seven extra unrestricted-GRH obligations")
for label, text in [("START_HERE", start), ("new-chat prompt", prompt)]:
    need(PIN in text and "v0.57" in text and "3,746" in text and "24" in text,
         label + ": exact original source and inherited mathematical inventory")
    need("unpack_reconstruction.py" in text and "restore_source.py" in text,
         label + ": complete two-stage offline restart instructions")
    need("FinLam" in text and "SeedIn" in text and "ell=3" in text and "AbsConv" in text,
         label + ": original arithmetic and analytic retained premises are visible")
need("every file TRACKED BY THE ORIGINAL PROJECT COMMIT" in source_access and
     "not a preinstalled Lean build environment" in source_access,
     "source access precisely distinguishes full project source from external build dependencies")

# Every added control is frozen and bound, excluding this output to avoid a
# self-reference. The outer SHA256SUMS_v0_58 is necessarily generated later.
for path in sorted((ROOT / "continuation_v58").rglob("*")):
    if not path.is_file() or "__pycache__" in path.parts or path.resolve() == OUTPUT.resolve():
        continue
    if path.suffix in {".tmp", ".partial"}:
        continue
    bind_file(path.relative_to(ROOT).as_posix())

archive_check = {"status": "NOT_YET_PACKAGED", "scope": "The packager consumes these frozen exact input bindings."}
if args.archive:
    archive_path = args.archive.resolve()
    phase("checking_finished_outer_archive")
    need(archive_path.stat().st_size <= CAP, "finished outer ZIP fits the observed delivery limit")
    with zipfile.ZipFile(archive_path) as archive:
        names = archive.namelist()
        need(len(names) == len(set(names)) and all(safe_member(n) for n in names),
             "finished outer archive has unique safe member paths")
        manifest_data = archive.read("SHA256SUMS_v0_58")
        outer_entries = dict(line.split("  ", 1)[::-1] for line in manifest_data.decode().splitlines())
        need(set(outer_entries) | {"SHA256SUMS_v0_58"} == set(names), "outer manifest covers every member")
        for name, expected in outer_entries.items():
            with archive.open(name) as stream:
                actual, size = digest_stream(stream)
            need(actual == expected == file_hash(ROOT / name), "exact outer archive member: " + name)
        archive_check = {"status": "PASS" if not errors else "FAIL", "sha256": file_hash(archive_path),
                         "bytes": archive_path.stat().st_size, "members": len(names)}

result = {
    "schema": "rh-independent-portable-continuation-audit/1", "package_version": "0.58",
    "mathematical_edition": "0.57", "date": "2026-11-24", "reviewer": "/root/arithmetic_common_frame",
    "status": "PASS" if not errors else "FAIL", "errors": errors, "source_commit": PIN,
    "scope": "Exact delivered-v57 preservation, unchanged mathematical scope, complete accepted-source inclusion, one fresh offline reconstruction test and one fresh offline source restoration, with actual restored-file and source-range checks. No Lean replay or new mathematical proof claims.",
    "primary_baseline": checkpoint["primary_baseline"], "preserved_reconstruction_members": len(seen_payload),
    "preserved_reconstruction_bytes": payload_bytes, "reconstruction_payload_sha256": payload_hash,
    "inherited_audit_input_bindings_checked": len(prior_audit["input_bindings"]),
    "inherited_mathematics_statistics": old_stats, "new_mathematical_claims": 0,
    "cumulative_claims": 3746, "exact_whole_closures": {}, "whole_open_obligations": 24,
    "original_source": {"commit": PIN, "tree": TREE, "tracked_files": SOURCE_FILES,
                        "tracked_bytes": SOURCE_BYTES, "archive_sha256": source_archive_hash,
                        "full_working_tree_raw_bytes_verified": True,
                        "no_external_object_alternates": True},
    "offline_restoration_tests": restoration_results,
    "next_task_source_index": {"primary_files_checked": len(checked_sources),
                               "unique_ranges_checked": len(checked_ranges),
                               "immediate_project_import_files_checked": len(checked_imports),
                               "all_project_sources_present": True,
                               "source_inclusion_is_not_a_new_proof": True},
    "narrative_scope_review": {"status": "PASS" if not errors else "FAIL", "unresolved_findings": [],
        "notes": [
            "Delivered v57 is the primary baseline. The 3645-through-v56 plus 101-in-v57 statement is historical claim-count lineage, not a restart from v56.",
            "The five v57 mathematical packets and all original retained premises are preserved. Rank-two propagation does not supply rank-three parity/thick/corner or automorphic seeds; the period identity does not supply its convergence/family or spectral inputs; the determinant window retains actual normal-form existence; section growth is separate from other section laws; FET retains the original records, Herr/comparison and common-family joins.",
            "All 24 whole identifiers remain, with class/category and route partitions kept distinct. GLOBAL_LOCAL_GAIN stays closed. No specialized input, source index, restoration success or packaging work is counted as a mathematical closure.",
            "The detailed proof-note style, intermediate constructions, unchanged coefficient rings/maps and order of common choices are explicit in both entry documents. The next tasks start at genuine missing producer bodies.",
            "The two bundled offline helpers recover the exact original reconstruction and accepted project source. The new source is a genuine shallow snapshot of the original commit, not a replacement commit. External dependency pins remain explicit; no complete offline Lean environment is claimed.",
        ]},
    "outer_archive_check": archive_check, "passed_check_count": len(checks),
    "input_bindings": dict(sorted(bindings.items())), "lean_build_run": False, "kernel_replay": False,
}
OUTPUT.parent.mkdir(parents=True, exist_ok=True)
OUTPUT.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n")
phase("completed", status=result["status"], errors=errors, passed_checks=len(checks),
      preserved_members=len(seen_payload), source_files=SOURCE_FILES, input_bindings=len(bindings),
      output=str(OUTPUT))
raise SystemExit(bool(errors))
