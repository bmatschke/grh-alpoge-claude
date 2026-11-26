#!/usr/bin/env python3
"""Restore the complete v0.57 reconstruction layout from the v0.58 snapshot.

Existing identical files are retained. Conflicting files, links, unsafe paths,
unlisted members and checksum mismatches stop extraction; no files are deleted.
"""
from pathlib import Path
import argparse
import hashlib
import json
import os
import stat
import sys
import tarfile

HERE=Path(__file__).resolve().parent
BASELINE_SHA='b326cc620d0064eda3126cce27f3dafd31e83d8516741aaf2ffcac450788bd33'

def require(value,message):
    if not value:raise ValueError(message)

def sha(path):
    h=hashlib.sha256()
    with path.open('rb') as f:
        for block in iter(lambda:f.read(4194304),b''):h.update(block)
    return h.hexdigest()

def safe_parts(name):
    require(isinstance(name,str) and name and '\\' not in name and '\0' not in name,'Unsafe member path')
    parts=tuple(name.split('/'))
    require(all(p not in ('','.','..') for p in parts),'Noncanonical member path: '+name)
    require(all(p.casefold()!='.git' for p in parts),'Git-control path refused: '+name)
    return parts

def read_json(path):
    def unique(pairs):
        d={}
        for k,v in pairs:
            require(k not in d,'Duplicate JSON key');d[k]=v
        return d
    return json.loads(path.read_text(),object_pairs_hook=unique)

def verify_asset(parent,item):
    parts=safe_parts(item['file']);require(len(parts)==1,'Bundle asset must be beside metadata')
    p=parent/item['file'];require(not p.is_symlink() and p.is_file(),'Bundle asset is not a regular file')
    require(p.stat().st_size==item['bytes'] and sha(p)==item['sha256'],'Bundle asset differs: '+p.name)
    return p

def safe_target(root,parts,create=False):
    current=root
    for part in parts[:-1]:
        current=current/part
        if current.exists() or current.is_symlink():
            require(not current.is_symlink() and current.is_dir(),'Non-directory or link in target path: '+str(current))
        elif create:current.mkdir()
    return root.joinpath(*parts)

def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--bundle',type=Path,default=HERE/'reconstruction_bundle.json')
    ap.add_argument('--destination',type=Path,default=HERE.parent)
    ap.add_argument('--quiet',action='store_true')
    args=ap.parse_args();meta=read_json(args.bundle)
    require(meta['schema']=='rh-preserved-reconstruction-bundle/1','Unknown bundle schema')
    require(meta['baseline_archive_sha256']==BASELINE_SHA,'Wrong v0.57 baseline')
    inv_path=verify_asset(args.bundle.parent,meta['inventory']);inv=read_json(inv_path)
    require(inv['baseline_archive_sha256']==BASELINE_SHA,'Wrong inventory baseline')
    records=inv['members'];byname={r['path']:r for r in records}
    require(len(byname)==len(records)==meta['member_count']==inv['member_count']==9551,'Member count mismatch')
    require(sum(r['bytes'] for r in records)==meta['uncompressed_bytes']==inv['uncompressed_bytes'],'Byte total mismatch')
    for r in records:
        safe_parts(r['path']);require(type(r['bytes']) is int and r['bytes']>=0,'Invalid member size')
        require(len(r['sha256'])==64 and all(c in '0123456789abcdef' for c in r['sha256']),'Invalid digest')
        require(type(r['mode']) is int and 0<=r['mode']<=0o777,'Invalid mode')
    require(not args.destination.is_symlink(),'Destination must not be a symlink')
    args.destination.mkdir(parents=True,exist_ok=True);root=args.destination.resolve()
    require(root.is_dir(),'Destination must be a directory')
    existing=set()
    for r in records:
        p=safe_target(root,safe_parts(r['path']))
        if p.exists() or p.is_symlink():
            require(not p.is_symlink() and p.is_file(),'Existing target is not a regular file: '+r['path'])
            require(p.stat().st_size==r['bytes'] and sha(p)==r['sha256'],'Conflicting existing file: '+r['path'])
            existing.add(r['path'])
    archive=verify_asset(args.bundle.parent,meta['archive'])
    if not args.quiet:print('Restoring and checking every original v0.57 member.',file=sys.stderr,flush=True)
    seen=set();created=0
    with tarfile.open(archive,mode='r|xz') as tar:
        for member in tar:
            name=member.name;parts=safe_parts(name)
            require(member.isfile() and not member.issparse(),'Only ordinary files are permitted')
            require(name in byname and name not in seen,'Unexpected or duplicate snapshot member: '+name)
            r=byname[name];require(member.size==r['bytes'] and member.mode==r['mode'],'Member size/mode mismatch: '+name)
            source=tar.extractfile(member);require(source is not None,'Missing member stream')
            target=safe_target(root,parts,create=True);output=None;checksum=hashlib.sha256();total=0
            try:
                if name not in existing:
                    fd=os.open(target,os.O_WRONLY|os.O_CREAT|os.O_EXCL|getattr(os,'O_NOFOLLOW',0),0o600)
                    output=os.fdopen(fd,'wb')
                while block:=source.read(4194304):
                    checksum.update(block);total+=len(block)
                    if output is not None:output.write(block)
                require(total==r['bytes'] and checksum.hexdigest()==r['sha256'],'Member checksum mismatch: '+name)
            finally:
                source.close()
                if output is not None:output.close()
            if name not in existing:
                os.chmod(target,r['mode']);created+=1
            seen.add(name)
    require(seen==set(byname),'Snapshot omitted original members')
    print(json.dumps({'status':'PASS','baseline_version':'0.57','baseline_archive_sha256':BASELINE_SHA,
      'destination':str(root),'members_verified':len(seen),'new_files_restored':created,
      'existing_identical_files_retained':len(existing),'uncompressed_bytes':inv['uncompressed_bytes'],
      'network_used':False,'new_mathematical_claims':0},indent=2))

if __name__=='__main__':
    try:main()
    except (OSError,ValueError,KeyError,tarfile.TarError) as error:
        print('Reconstruction restore failed: '+str(error),file=sys.stderr);raise SystemExit(1)
