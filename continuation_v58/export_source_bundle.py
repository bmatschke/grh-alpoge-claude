#!/usr/bin/env python3
"""Reproduce the two v0.58 offline source files from the pinned Git submodule."""

import argparse
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile


HERE = Path(__file__).resolve().parent
ASSETS = {
    "tree_manifest": "tree_manifest.json",
    "archive": "formal_source.tar.xz",
}


def git_command(source, *args):
    return ["git", "-C", str(source), "-c", "tar.umask=0002", *args]


def git_output(source, env, *args):
    return subprocess.check_output(git_command(source, *args), env=env)


def verify_file(path, record):
    if path.is_symlink() or not path.is_file() or path.stat().st_size != record["bytes"]:
        raise ValueError(f"Unexpected file or size: {path}")
    digest = hashlib.sha256()
    with path.open("rb") as source:
        for block in iter(lambda: source.read(4 * 1024 * 1024), b""):
            digest.update(block)
    if digest.hexdigest() != record["sha256"]:
        raise ValueError(f"SHA-256 mismatch: {path}")


def write_manifest(path, source, bundle, env):
    listing = git_output(source, env, "ls-tree", "-rlz", bundle["source_commit"])
    files = []
    for entry in listing.rstrip(b"\0").split(b"\0"):
        header, name = entry.split(b"\t", 1)
        mode, kind, oid, size = header.decode("ascii").split()
        files.append({"path": name.decode("utf-8"), "mode": mode, "type": kind,
                      "oid": oid, "bytes": int(size)})
    size = sum(f["bytes"] for f in files)
    if len(files) != bundle["tracked_files"] or size != bundle["tracked_bytes"]:
        raise ValueError("Git tree inventory differs from the v0.58 source bundle")
    manifest = {
        "schema": "rh-pinned-source-tree/1",
        "commit": bundle["source_commit"],
        "tree": bundle["source_tree"],
        "source_repository": bundle["source_repository"],
        "shallow_snapshot": True,
        "files": files,
        "tracked_file_count": len(files),
        "tracked_bytes": size,
        "raw_commit_sha256": bundle["raw_commit"]["sha256"],
    }
    with path.open("w", encoding="utf-8", newline="\n") as out:
        json.dump(manifest, out, ensure_ascii=False, separators=(",", ":"))
        out.write("\n")


def write_archive(path, source, bundle, env):
    git = git_command(source, "archive", "--format=tar", bundle["source_commit"])
    with path.open("wb") as out, subprocess.Popen(git, stdout=subprocess.PIPE, env=env) as archive:
        try:
            subprocess.run(["xz", "-T4", "-3", "--check=sha256", "-c"],
                           stdin=archive.stdout, stdout=out, check=True, env=env)
        finally:
            archive.stdout.close()
        if archive.wait():
            raise ValueError("git archive failed to export the pinned source")


def export(source, bundle_path, output):
    bundle = json.loads(bundle_path.read_text(encoding="utf-8"))
    if bundle["schema"] != "rh-offline-source-bundle/1":
        raise ValueError("Unknown source bundle format")
    env = os.environ.copy()
    for name in ("XZ_OPT", "XZ_DEFAULTS", "GIT_DIR", "GIT_WORK_TREE",
                 "GIT_INDEX_FILE", "GIT_COMMON_DIR"):
        env.pop(name, None)
    env.update({"GIT_NO_REPLACE_OBJECTS": "1", "GIT_NO_LAZY_FETCH": "1",
                "GIT_ALLOW_PROTOCOL": "", "GIT_CONFIG_NOSYSTEM": "1",
                "GIT_CONFIG_GLOBAL": os.devnull, "GIT_ATTR_NOSYSTEM": "1"})
    for ref, key in (("HEAD", "source_commit"), ("HEAD^{tree}", "source_tree")):
        if git_output(source, env, "rev-parse", ref).decode("ascii").strip() != bundle[key]:
            raise ValueError(f"Source {ref} differs from {key} in {bundle_path}")
    raw = git_output(source, env, "cat-file", "commit", "HEAD")
    if len(raw) != bundle["raw_commit"]["bytes"] or hashlib.sha256(raw).hexdigest() != bundle["raw_commit"]["sha256"]:
        raise ValueError("Original Git commit bytes differ from the recorded v0.58 commit")
    output.mkdir(parents=True, exist_ok=True)
    generators = {"tree_manifest": write_manifest, "archive": write_archive}
    with tempfile.TemporaryDirectory(prefix=".v58-export-", dir=output) as temp:
        staged = []
        for key, filename in ASSETS.items():
            if filename != bundle[key]["file"]:
                raise ValueError(f"Unexpected asset name in {bundle_path}")
            destination = output / filename
            if destination.exists() or destination.is_symlink():
                verify_file(destination, bundle[key])
                continue
            candidate = Path(temp) / filename
            generators[key](candidate, source, bundle, env)
            verify_file(candidate, bundle[key])
            staged.append((candidate, destination))
        for candidate, destination in staged:
            # A concurrent process cannot cause an existing file to be overwritten.
            os.link(candidate, destination)
    for key, filename in ASSETS.items():
        print(f"{bundle[key]['sha256']}  {output / filename}")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", type=Path, default=HERE.parent / "formal_source")
    parser.add_argument("--bundle", type=Path, default=HERE / "source" / "source_bundle.json")
    parser.add_argument("--output-dir", type=Path, help="defaults to the metadata file's directory")
    args = parser.parse_args()
    export(args.source, args.bundle, args.output_dir or args.bundle.parent)


if __name__ == "__main__":
    try:
        main()
    except (OSError, ValueError, KeyError, subprocess.CalledProcessError) as exc:
        sys.exit(f"Source export failed: {exc}")
