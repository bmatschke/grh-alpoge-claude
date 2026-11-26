#!/usr/bin/env python3
"""Restore and verify the original accepted project snapshot, entirely offline.

No source is fetched and no Lean build is run. Only a new or empty destination
is accepted. Git's original commit object is imported verbatim, not recreated.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import stat
import subprocess
import sys
import tarfile
from typing import Any


ACCEPTED_COMMIT = "7cbf7a0c32fca1badf05931879a37c3f8a2b03b4"
ACCEPTED_TREE = "02cfa4b3810fc22f6d43b317409071f380a5f1b4"
CHUNK_SIZE = 4 * 1024 * 1024
HEX40 = re.compile(r"[0-9a-f]{40}\Z")
HEX64 = re.compile(r"[0-9a-f]{64}\Z")


class RestoreError(Exception):
    """A checked integrity, destination, or Git-reconstruction failure."""


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RestoreError(message)


def report(message: str, quiet: bool) -> None:
    if not quiet:
        print(message, file=sys.stderr, flush=True)


def integer(value: Any, label: str) -> int:
    require(type(value) is int and value >= 0, f"Invalid {label}.")
    return value


def digest_string(value: Any, pattern: re.Pattern[str], label: str) -> str:
    require(isinstance(value, str) and bool(pattern.fullmatch(value)),
            f"Invalid {label}.")
    return value


def safe_path_parts(value: Any) -> tuple[str, ...]:
    require(isinstance(value, str) and bool(value), "Empty or non-string path.")
    require("\x00" not in value and "\\" not in value,
            f"Unsafe path: {value!r}.")
    parts = tuple(value.split("/"))
    require(all(part not in ("", ".", "..") for part in parts),
            f"Noncanonical path: {value!r}.")
    require(all(part.casefold() != ".git" for part in parts),
            f"Git-control path is not a source member: {value!r}.")
    return parts


def read_json(path: Path) -> dict[str, Any]:
    def unique_object(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
        result: dict[str, Any] = {}
        for key, value in pairs:
            require(key not in result, f"Duplicate JSON key {key!r} in {path.name}.")
            result[key] = value
        return result

    with path.open("r", encoding="utf-8") as stream:
        result = json.load(stream, object_pairs_hook=unique_object)
    require(isinstance(result, dict), f"Expected a JSON object in {path.name}.")
    return result


def verify_asset(directory: Path, specification: Any, label: str) -> Path:
    require(isinstance(specification, dict), f"Missing {label} specification.")
    name = specification.get("file")
    parts = safe_path_parts(name)
    require(len(parts) == 1, f"{label} must be beside source_bundle.json.")
    expected_size = integer(specification.get("bytes"), f"{label} byte count")
    expected_hash = digest_string(specification.get("sha256"), HEX64,
                                  f"{label} SHA-256")
    path = directory / name
    information = path.lstat()
    require(stat.S_ISREG(information.st_mode), f"{label} is not a regular file.")
    require(information.st_size == expected_size, f"{label} byte count differs.")
    checksum = hashlib.sha256()
    total = 0
    with path.open("rb") as stream:
        while chunk := stream.read(CHUNK_SIZE):
            checksum.update(chunk)
            total += len(chunk)
    require(total == expected_size and checksum.hexdigest() == expected_hash,
            f"{label} SHA-256 or byte count differs.")
    after = path.lstat()
    require((information.st_dev, information.st_ino, information.st_size,
             information.st_mtime_ns) ==
            (after.st_dev, after.st_ino, after.st_size, after.st_mtime_ns),
            f"{label} changed while being verified.")
    return path


def git_object_id(kind: str, content: bytes) -> str:
    header = f"{kind} {len(content)}\0".encode("ascii")
    return hashlib.sha1(header + content).hexdigest()


def validate_manifest(manifest: dict[str, Any], bundle: dict[str, Any],
                      raw_commit: bytes) -> tuple[dict[str, dict[str, Any]], set[str]]:
    require(bundle.get("source_commit") == ACCEPTED_COMMIT,
            "Bundle is not for the accepted original commit.")
    require(bundle.get("source_tree") == ACCEPTED_TREE,
            "Bundle tree differs from the accepted original tree.")
    require(manifest.get("schema") == "rh-pinned-source-tree/1",
            "Unsupported tree-manifest schema.")
    require(manifest.get("commit") == ACCEPTED_COMMIT and
            manifest.get("tree") == ACCEPTED_TREE,
            "Tree manifest disagrees with the accepted commit/tree.")
    require(git_object_id("commit", raw_commit) == ACCEPTED_COMMIT,
            "Original raw commit does not hash to the accepted pin.")
    require(raw_commit.split(b"\n", 1)[0] ==
            b"tree " + ACCEPTED_TREE.encode("ascii"),
            "Original raw commit does not name the accepted tree.")
    require(manifest.get("raw_commit_sha256") == hashlib.sha256(raw_commit).hexdigest(),
            "Tree manifest's raw-commit SHA-256 differs.")

    records = manifest.get("files")
    require(isinstance(records, list) and bool(records), "Empty tree manifest.")
    files: dict[str, dict[str, Any]] = {}
    directories: set[str] = set()
    total_bytes = 0
    for record in records:
        require(isinstance(record, dict), "Invalid tree-manifest entry.")
        path = record.get("path")
        parts = safe_path_parts(path)
        require(path not in files, f"Duplicate manifest path: {path!r}.")
        require(record.get("type") == "blob", f"Non-blob source path: {path!r}.")
        require(record.get("mode") in ("100644", "100755"),
                f"Unsupported Git mode for {path!r}; links/submodules are refused.")
        digest_string(record.get("oid"), HEX40, f"blob object ID for {path!r}")
        total_bytes += integer(record.get("bytes"), f"size for {path!r}")
        files[path] = record
        for end in range(1, len(parts)):
            directories.add("/".join(parts[:end]))
    require(not directories.intersection(files), "A file is also a parent directory.")
    require(len(files) == integer(manifest.get("tracked_file_count"), "manifest count")
            == integer(bundle.get("tracked_files"), "bundle count"),
            "Tracked-file counts disagree.")
    require(total_bytes == integer(manifest.get("tracked_bytes"), "manifest bytes")
            == integer(bundle.get("tracked_bytes"), "bundle bytes"),
            "Tracked-byte totals disagree.")
    return files, directories


def prepare_destination(requested: Path) -> Path:
    requested = requested.expanduser()
    require(requested.name not in ("", ".", ".."), "Invalid destination.")
    # Resolve the parent only: never follow an existing destination symlink.
    parent = requested.parent.resolve(strict=True)
    destination = parent / requested.name
    try:
        information = destination.lstat()
    except FileNotFoundError:
        destination.mkdir(mode=0o700)
    else:
        require(stat.S_ISDIR(information.st_mode),
                "Destination must be a real directory, not a symlink or file.")
        require(next(destination.iterdir(), None) is None,
                "Destination is not empty; no files have been overwritten.")
    return destination


def directory_fd(root_fd: int, parts: tuple[str, ...]) -> int:
    """Open/create a relative directory without following any symlink."""
    current = os.dup(root_fd)
    try:
        for part in parts:
            try:
                os.mkdir(part, mode=0o755, dir_fd=current)
            except FileExistsError:
                pass
            following = os.open(part, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW,
                                dir_fd=current)
            os.close(current)
            current = following
        return current
    except BaseException:
        os.close(current)
        raise


def extract_source(archive: Path, destination: Path,
                   files: dict[str, dict[str, Any]], directories: set[str],
                   quiet: bool) -> int:
    seen_files: set[str] = set()
    seen_directories: set[str] = set()
    total_bytes = 0
    root_fd = os.open(destination, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW)
    try:
        # Deliberately avoid extract()/extractall(): every file is opened using
        # checked directory descriptors, O_EXCL, and O_NOFOLLOW.
        with tarfile.open(archive, mode="r|xz") as stream:
            for member in stream:
                path = member.name.rstrip("/") if member.isdir() else member.name
                parts = safe_path_parts(path)
                if member.isdir():
                    require(path in directories and path not in seen_directories,
                            f"Unexpected or duplicate directory: {path!r}.")
                    require(member.size == 0, f"Nonempty directory record: {path!r}.")
                    descriptor = directory_fd(root_fd, parts)
                    os.close(descriptor)
                    seen_directories.add(path)
                    continue

                require(member.type in (tarfile.REGTYPE, tarfile.AREGTYPE),
                        f"Non-regular archive member refused: {path!r}.")
                require(not member.issparse() and not member.linkname,
                        f"Sparse/link archive member refused: {path!r}.")
                require(path in files and path not in seen_files,
                        f"Unexpected or duplicate file: {path!r}.")
                record = files[path]
                require(member.size == record["bytes"],
                        f"Archive/manifest size differs for {path!r}.")
                executable = record["mode"] == "100755"
                require(bool(member.mode & 0o111) == executable,
                        f"Archive/manifest executable mode differs for {path!r}.")
                require(not (member.mode & 0o7000),
                        f"Special permission bits refused for {path!r}.")
                mode = 0o755 if executable else 0o644
                checksum = hashlib.sha1(f"blob {member.size}\0".encode("ascii"))
                count = 0
                parent_fd = directory_fd(root_fd, parts[:-1])
                try:
                    descriptor = os.open(parts[-1], os.O_WRONLY | os.O_CREAT |
                                         os.O_EXCL | os.O_NOFOLLOW,
                                         mode, dir_fd=parent_fd)
                    with os.fdopen(descriptor, "wb") as output:
                        os.fchmod(output.fileno(), mode)
                        source = stream.extractfile(member)
                        require(source is not None, f"Cannot read {path!r}.")
                        with source:
                            while chunk := source.read(CHUNK_SIZE):
                                count += len(chunk)
                                require(count <= record["bytes"],
                                        f"Oversized archive content for {path!r}.")
                                checksum.update(chunk)
                                output.write(chunk)
                        require(stat.S_IMODE(os.fstat(output.fileno()).st_mode) == mode,
                                f"Could not set the recorded mode for {path!r}.")
                finally:
                    os.close(parent_fd)
                require(count == record["bytes"] and checksum.hexdigest() == record["oid"],
                        f"Git blob hash or byte count differs for {path!r}.")
                seen_files.add(path)
                total_bytes += count
                if len(seen_files) % 50000 == 0:
                    report(f"Verified {len(seen_files):,}/{len(files):,} source files.", quiet)
    finally:
        os.close(root_fd)
    require(seen_files == files.keys(),
            f"Archive omitted {len(files.keys() - seen_files):,} expected files.")
    return total_bytes


def git_environment() -> dict[str, str]:
    # Exclude inherited Git directories/indexes/config injection, global/system
    # configuration and attributes. The helper never executes a network command.
    environment = {key: value for key, value in os.environ.items()
                   if not key.upper().startswith("GIT_")}
    environment.update({
        "GIT_CONFIG_NOSYSTEM": "1",
        "GIT_CONFIG_SYSTEM": os.devnull,
        "GIT_CONFIG_GLOBAL": os.devnull,
        "GIT_ATTR_NOSYSTEM": "1",
        "GIT_TERMINAL_PROMPT": "0",
    })
    return environment


def restore_git(destination: Path, raw_commit: bytes, quiet: bool) -> dict[str, str]:
    environment = git_environment()

    def git(*arguments: str, data: bytes | None = None) -> str:
        process = subprocess.run(["git", "-C", str(destination), *arguments],
                                 input=data, stdout=subprocess.PIPE,
                                 stderr=subprocess.PIPE, env=environment,
                                 check=False)
        if process.returncode:
            detail = process.stderr.decode("utf-8", errors="replace")[-4000:].strip()
            raise RestoreError(f"Git command {arguments[0]!r} failed: {detail}")
        return process.stdout.decode("utf-8", errors="strict").strip()

    git("init", "--quiet", "--template=", "--object-format=sha1")
    for key, value in {
        "core.autocrlf": "false",
        "core.eol": "lf",
        "core.safecrlf": "false",
        "core.attributesFile": os.devnull,
        "core.fileMode": "true",
        "core.ignoreCase": "false",
        "core.precomposeUnicode": "false",
        "core.fsmonitor": "false",
    }.items():
        git("config", "--local", key, value)
    # Highest-precedence attributes prevent any tracked/global attributes from
    # introducing clean filters, newline, ident or encoding transformations.
    information = destination / ".git" / "info"
    information.mkdir(exist_ok=True)
    (information / "attributes").write_text(
        "* -text -eol -ident -filter -working-tree-encoding\n", encoding="ascii")
    report("Writing Git blobs/index and checking the complete original tree.", quiet)
    git("add", "-f", "--all", "--", ".")
    tree = git("write-tree")
    require(tree == ACCEPTED_TREE,
            f"Restored Git tree differs: expected {ACCEPTED_TREE}, obtained {tree}.")
    commit = git("hash-object", "-t", "commit", "-w", "--stdin", data=raw_commit)
    require(commit == ACCEPTED_COMMIT, "Git did not preserve the original commit bytes.")

    # The original parent object is intentionally not fabricated. This exact
    # original commit is the boundary of a one-commit shallow snapshot.
    (destination / ".git" / "shallow").write_text(ACCEPTED_COMMIT + "\n", encoding="ascii")
    git("symbolic-ref", "HEAD", "refs/heads/accepted-source")
    git("update-ref", "refs/heads/accepted-source", ACCEPTED_COMMIT)
    require(git("rev-parse", "HEAD") == ACCEPTED_COMMIT, "Restored HEAD differs.")
    require(git("rev-parse", "HEAD^{tree}") == ACCEPTED_TREE, "Restored HEAD tree differs.")
    require(git("rev-parse", "--is-shallow-repository") == "true",
            "The accepted commit was not recorded as a shallow boundary.")
    require(git("status", "--porcelain", "--untracked-files=all") == "",
            "Restored working tree/index is not clean.")
    return {"commit": commit, "tree": tree}


def main() -> int:
    here = Path(__file__).resolve().parent
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--destination", type=Path, default=here.parent / "formal_source",
                        help="New or empty directory (default: archive-root/formal_source).")
    parser.add_argument("--bundle", type=Path,
                        default=here / "source" / "source_bundle.json",
                        help="Source-bundle JSON; its three artifacts must be beside it.")
    parser.add_argument("--quiet", action="store_true", help="Hide phase/progress messages.")
    arguments = parser.parse_args()
    destination: Path | None = None
    try:
        require(os.name == "posix" and hasattr(os, "O_NOFOLLOW") and
                os.open in os.supports_dir_fd and os.mkdir in os.supports_dir_fd,
                "Use a POSIX environment with safe directory-descriptor file operations.")
        require(shutil.which("git") is not None, "Git is not installed or is not on PATH.")
        bundle_path = arguments.bundle.expanduser().resolve(strict=True)
        bundle = read_json(bundle_path)
        report("Checking archive, manifest and original-commit SHA-256 hashes.", arguments.quiet)
        archive = verify_asset(bundle_path.parent, bundle.get("archive"), "source archive")
        manifest_path = verify_asset(bundle_path.parent, bundle.get("tree_manifest"), "tree manifest")
        raw_path = verify_asset(bundle_path.parent, bundle.get("raw_commit"), "original raw commit")
        manifest = read_json(manifest_path)
        raw_commit = raw_path.read_bytes()
        files, directories = validate_manifest(manifest, bundle, raw_commit)
        destination = prepare_destination(arguments.destination)
        report(f"Restoring {len(files):,} original files into {destination}.", arguments.quiet)
        restored_bytes = extract_source(archive, destination, files, directories, arguments.quiet)
        require(restored_bytes == bundle["tracked_bytes"], "Extracted byte total differs.")
        actual = restore_git(destination, raw_commit, arguments.quiet)
        print(json.dumps({
            "status": "ok",
            "destination": str(destination),
            "source_commit": actual["commit"],
            "source_tree": actual["tree"],
            "tracked_files_verified": len(files),
            "tracked_bytes_verified": restored_bytes,
            "artifact_sha256_checks": 3,
            "shallow": True,
            "working_tree_clean": True,
            "network_used": False,
            "lean_build_run": False,
        }, ensure_ascii=False))
        return 0
    except (RestoreError, OSError, ValueError, tarfile.TarError, EOFError) as error:
        result: dict[str, Any] = {"status": "error", "error": str(error)}
        if destination is not None:
            result["destination"] = str(destination)
            result["note"] = "Partial files were retained; use a new or empty destination for a retry."
        print(json.dumps(result, ensure_ascii=False), file=sys.stderr)
        return 1
    except KeyboardInterrupt:
        print("Restore interrupted. Any partial destination is retained; it will not be overwritten.",
              file=sys.stderr)
        return 130


if __name__ == "__main__":
    raise SystemExit(main())
