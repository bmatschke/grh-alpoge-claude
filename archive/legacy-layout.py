#!/usr/bin/env python3
"""Make a writable historical-layout checkout and import reviewed edits into the live layout."""
import argparse
import csv
import hashlib
import json
import os
import posixpath
import re
import shutil
import stat
import subprocess
import sys
import tempfile
from pathlib import Path, PurePosixPath
from urllib.parse import urlsplit

ROOT = Path(__file__).resolve().parents[1]
STATE = ".git/legacy-layout.json"
EXTRA = "archive/legacy-additions.tsv"
SUBMODULE = "formal_source"
LINK = re.compile(r"(\]\(|^\s*\[[^\]\n]+\]:\s+)(<?)([^()<>\s]+)", re.M)

def git(root, *args, data=None, env=None):
    proc = subprocess.run(["git", "-C", str(root), *args], input=data, capture_output=True, env=env)
    if proc.returncode:
        raise ValueError(proc.stderr.decode(errors="replace").strip())
    return proc.stdout

def paths(raw):
    return [name for name in raw.decode().split("\0") if name]

def valid(name):
    p = PurePosixPath(name)
    if (not name or p.is_absolute() or str(p) != name or
            any(x in {".", "..", ".git"} for x in name.split("/")) or any(c in name for c in "\t\r\n\0")):
        raise ValueError("Invalid relative path: " + repr(name))
    return name

def guarded(root, name):
    p = root / valid(name)
    if p.resolve() != p:
        raise ValueError("A path crosses a symlink: " + str(p))
    return p

def load_map(root):
    forward = {}
    for name in ("archive/path-map.tsv", EXTRA):
        p = root / name
        if not p.exists() and name == EXTRA:
            continue
        with p.open() as fh:
            for row in csv.DictReader(fh, delimiter="\t"):
                key, dest = valid(row["former_root_entry"]), valid(row["current_path"])
                if key in forward or dest in forward.values():
                    raise ValueError("Duplicate layout mapping: " + key)
                forward[key] = dest
    return forward

def translate(name, mapping):
    candidate = name
    while candidate and candidate != ".":
        if candidate in mapping:
            return mapping[candidate] + name[len(candidate):]
        candidate = posixpath.dirname(candidate)
    return name

def project(data, old, modern, mapping, to_old):
    """Archive evidence retains its historical bytes. The live sources have relocated links."""
    before, after = (modern, old) if to_old else (old, modern)
    if old == "verify_selected_family.py":
        src = data.decode()
        variants = [("Path(__file__).resolve().parent", "Path(__file__).resolve().parents[2]"),
                    ('root / "SELECTED_FAMILY_CHECKPOINT.json"', 'root / "research/register/SELECTED_FAMILY_CHECKPOINT.json"')]
        for left, right in variants:
            src = src.replace(right, left) if to_old else src.replace(left, right)
        return src.encode()
    if old == "SELECTED_FAMILY_CHECKPOINT.json":
        def visit(x):
            if isinstance(x, str):
                if x in ("python3 verify_selected_family.py","python3 research/register/verify_selected_family.py"):
                    return "python3 " + ("verify_selected_family.py" if to_old else "research/register/verify_selected_family.py")
                return translate(x, mapping)
            if isinstance(x, list):
                return [visit(y) for y in x]
            if isinstance(x, dict):
                return {k: visit(y) for k, y in x.items()}
            return x
        return (json.dumps(visit(json.loads(data)), ensure_ascii=False, indent=2) + "\n").encode()
    if old == ".gitignore":
        early = "/continuation_v58/"
        late = "/archive/rounds/v58/continuation_v58/"
        return data.replace(late.encode(), early.encode()) if to_old else data.replace(early.encode(), late.encode())
    if not modern.endswith(".md") or (modern.startswith("archive/") and old != modern):
        return data
    def link(m):
        href = m[3]
        u = urlsplit(href)
        if u.scheme or u.netloc or not u.path or u.path.startswith("/"):
            return m[0]
        target = posixpath.normpath(posixpath.join(posixpath.dirname(before), u.path))
        # Leave unfamiliar escaped filenames alone unless a real named mapping changes their location.
        new = translate(target, mapping)
        if new == target and before == after:
            return m[0]
        rebased = posixpath.relpath(new, posixpath.dirname(after) or ".")
        return m[1] + m[2] + rebased + href[len(u.path):]
    return LINK.sub(link, data.decode()).encode()

def digest(data):
    return hashlib.sha256(data).hexdigest()

def mode(p):
    return 0o755 if p.stat().st_mode & stat.S_IXUSR else 0o644

def stamp(data, m):
    return f"{m:o} {digest(data)}"

def save_atomic(p, data, m=0o644):
    p.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.NamedTemporaryFile(dir=p.parent, delete=False) as h:
        tmp = Path(h.name)
        try:
            h.write(data)
            h.flush()
            os.fchmod(h.fileno(), m)
        except BaseException:
            tmp.unlink(missing_ok=True)
            raise
    try:
        os.replace(tmp, p)
    finally:
        tmp.unlink(missing_ok=True)

def state_save(dest, data):
    save_atomic(dest / STATE, (json.dumps(data, ensure_ascii=False, separators=(",", ":"))+"\n").encode())

def export_view(root, dest, omit_history):
    if dest.exists() or dest.is_relative_to(root) or root.is_relative_to(dest):
        raise ValueError("Choose a new directory outside the canonical checkout.")
    if not dest.parent.is_dir():
        raise ValueError("The destination parent does not exist.")
    layout = load_map(root)
    reverse = {v: k for k, v in layout.items()}
    # The current index and working tree suffice, including a depth-one checkout.
    listed = paths(git(root, "ls-files", "--cached", "--others", "--exclude-standard", "-z"))
    canonical = {n if (root / n).is_file() else translate(n, layout) for n in listed}
    revision = git(root, "rev-parse", "HEAD").decode().strip()
    sub = git(root, "ls-files", "--stage", "--", SUBMODULE).decode().split()
    if len(sub) != 4 or sub[0] != "160000" or sub[2] != "0":
        raise ValueError("Expected the recorded formal_source Git submodule in the current index.")
    # Independent working files and index; read-only access to available historical Git objects.
    objects = git(root, "rev-parse", "--path-format=absolute", "--git-path", "objects").decode().strip()
    shallow = Path(git(root, "rev-parse", "--path-format=absolute", "--git-path", "shallow").decode().strip())
    dest.mkdir()
    try:
        git(dest, "init", "--quiet")
        (dest / ".git/objects/info/alternates").write_text(objects + "\n")
        if shallow.is_file():
            shutil.copyfile(shallow, dest / ".git/shallow")
        state = {"root": str(root), "files": {}, "touched": []}
        for modern in sorted(canonical):
            old = translate(modern, reverse)
            if omit_history and old.split("/",1)[0] == "history":
                continue
            if old == SUBMODULE:
                continue
            src = guarded(root, modern)
            if not src.is_file():
                continue
            target = guarded(dest, old)
            data = src.read_bytes()
            projected = project(data, old, modern, reverse, True)
            perms = mode(src)
            save_atomic(target, projected, perms)
            state["files"][old] = [modern, stamp(data,perms), stamp(projected,perms)]
        (dest / SUBMODULE).mkdir(exist_ok=True)
        git(dest, "read-tree", "--empty")
        git(dest, "add", "-f", "--pathspec-from-file=-", "--pathspec-file-nul",
            data=b"".join(n.encode()+b"\0" for n in state["files"]),
            env={**os.environ, "GIT_LITERAL_PATHSPECS":"1"})
        git(dest,"update-index","--add","--cacheinfo","160000",sub[1],SUBMODULE)
        tree = git(dest, "write-tree").decode().strip()
        commit = git(dest, "-c","user.name=Legacy layout","-c","user.email=layout@localhost",
                     "commit-tree",tree,"-p",revision,"-m","Current manuscript projected into the historical research layout").decode().strip()
        git(dest,"update-ref","--no-deref","HEAD",commit)
        state["export_commit"] = commit
        state_save(dest,state)
        print(f"Created {dest} with {len(state['files'])} current files. Run old commands from that directory.")
    except BaseException:
        # The caller required a previously nonexistent directory and this process created it.
        shutil.rmtree(dest)
        raise

def added_paths(specs, dest, root, layout):
    new = {}; extra = {}
    for spec in specs:
        old,sep,modern=spec.partition("=")
        if not sep:raise ValueError("Use --add OLD_PATH=CANONICAL_PATH.")
        src=guarded(dest,old); guarded(root,modern)
        if not src.exists():raise ValueError("New source is absent: "+old)
        current=translate(old,layout)
        if old in layout and current!=modern:raise ValueError("Existing mapping: "+old+" -> "+current)
        if current!=modern:
            reverse={v:k for k,v in {**layout, **extra}.items()}
            inverse=translate(modern,reverse)
            if (inverse!=modern and inverse!=old) or (old in extra and extra[old]!=modern):
                raise ValueError("New destination collides with an existing mapping: "+modern)
            if any(k.startswith(old+"/") or v.startswith(modern+"/") for k,v in {**layout, **extra}.items()):
                raise ValueError("Map individual new files below an existing mapped path: "+old)
            extra[old]=modern
        members=[src] if src.is_file() else sorted(f for f in src.rglob("*") if f.is_file())
        for target in members:
            name=target.relative_to(dest).as_posix()
            canonical=modern+name[len(old):]
            guarded(dest,name);guarded(root,canonical)
            if name in new and new[name]!=canonical:raise ValueError("Conflicting additions: "+name)
            new[name]=canonical
    return new,extra

def import_view(root,dest,specs,write):
    s=json.loads((dest/STATE).read_text())
    if Path(s["root"])!=root:raise ValueError("This view was exported from a different checkout.")
    layout=load_map(root)
    add,extra=added_paths(specs,dest,root,layout)
    files=s["files"]
    own={v[0]:k for k,v in files.items()}
    for old,modern in add.items():
        if modern in own and own[modern]!=old:
            raise ValueError("New destination already belongs to "+own[modern])
        if modern in own and old not in files:
            raise ValueError("Duplicate import destination: "+modern)
        own[modern]=old
        if old in files and files[old][0]!=modern:raise ValueError("Cannot remap existing file "+old)
        if modern in (EXTRA,"archive/path-map.tsv"):raise ValueError("Reserved mapping file: "+modern)
    layout.update(extra)
    names=set(s["touched"])|set(add)|set(paths(git(dest,"diff","--name-only","--no-renames","-z",s["export_commit"],"--")))
    candidates=[];errors=[]
    for old in sorted(names):
        if old==SUBMODULE:continue
        if old not in files and old not in add:
            errors.append("New file needs --add: "+old);continue
        modern,base,before=files.get(old,[add.get(old),None,None])
        if modern in ("archive/path-map.tsv",EXTRA):
            errors.append("Edit the layout map in the canonical checkout: "+old);continue
        src=guarded(dest,old);target=guarded(root,modern)
        if not src.is_file():
            errors.append("Deletion requires a separate canonical edit: "+old);continue
        data=src.read_bytes();perms=mode(src);now=stamp(data,perms)
        if now==before:continue
        converted=project(data,old,modern,layout,False)
        resulting=stamp(converted,perms)
        if target.exists() and not target.is_file():
            errors.append("Canonical path is not a file: "+modern);continue
        current=stamp(target.read_bytes(),mode(target)) if target.exists() else None
        if current!=base and current!=resulting:
            errors.append("Conflicting canonical edit: "+modern);continue
        candidates.append((old,modern,current,resulting,now))
    if errors:raise ValueError("\n".join(errors))
    untracked=set(paths(git(dest,"ls-files","--others","--exclude-standard","-z")))-set(add)-set(files)
    for n in sorted(untracked):
        print("Unmapped, left in view:",n)
    for old,modern,_,_,_ in candidates:print(old+" -> "+modern)
    if not write:
        print(f"{len(candidates)} mapped changes. Add --apply to write them.");return
    # A retry recognises a previously completed file by its resulting digest.
    for old,modern,expected,resulting,now in candidates:
        src=guarded(dest,old);target=guarded(root,modern);data=src.read_bytes();perms=mode(src)
        if stamp(data,perms)!=now:raise ValueError("Concurrent edit in the legacy view: "+old)
        current=stamp(target.read_bytes(),mode(target)) if target.exists() else None
        if current!=resulting:
            if current!=expected:raise ValueError("Concurrent canonical edit: "+modern)
            save_atomic(target,project(data,old,modern,layout,False),perms)
        files[old]=[modern,resulting,now]
    if extra:
        p=root/EXTRA;previous=p.read_text() if p.exists() else "former_root_entry\tcurrent_path\n"
        save_atomic(p,(previous+"".join(k+"\t"+v+"\n" for k,v in sorted(extra.items()))).encode())
    s["touched"]=sorted(set(s["touched"])|{row[0] for row in candidates})
    state_save(dest,s);print(f"Imported {len(candidates)} mapped changes.")

def main():
    cli=argparse.ArgumentParser(description=__doc__)
    cli.add_argument("--root",type=Path,default=ROOT,help="canonical Git checkout")
    cmd=cli.add_subparsers(dest="task",required=True)
    export=cmd.add_parser("export",help="materialize current sources in a new, isolated checkout")
    export.add_argument("view",type=Path)
    export.add_argument("--omit-history",action="store_true",help="omit only old history/version_* snapshots to save disk space")
    imp=cmd.add_parser("import",help="show mapped changes, then apply explicitly")
    imp.add_argument("view",type=Path)
    imp.add_argument("--add",action="append",default=[],metavar="OLD=CANONICAL",help="map a new file or directory")
    imp.add_argument("--apply",action="store_true",help="write reviewed changes to the canonical checkout")
    opts=cli.parse_args();root=opts.root.resolve();dest=opts.view.resolve()
    if opts.task=="export":export_view(root,dest,opts.omit_history)
    elif opts.apply:
        # Serialize imports in this checkout, including updates to the supplemental path map.
        import fcntl
        gitdir=Path(git(root,"rev-parse","--absolute-git-dir").decode().strip())
        with (gitdir/"legacy-layout-import.lock").open("a") as lock:
            fcntl.flock(lock,fcntl.LOCK_EX)
            import_view(root,dest,opts.add,True)
    else:
        import_view(root,dest,opts.add,False)
if __name__=="__main__":
    try:main()
    except (OSError,ValueError) as error:
        print(error,file=sys.stderr);raise SystemExit(1)
