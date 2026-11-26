#!/usr/bin/env python3
"""Restore exact v0.34 bytes from this additive archive, without an older ZIP.
Useful when rebuilding a new component ledger with --baseline. The destination
must not exist. This performs no network request and no Lean execution.
"""
from pathlib import Path
import argparse,hashlib,shutil
ROOT=Path(__file__).resolve().parent;OLD=ROOT/'history/version_0_34'
p=argparse.ArgumentParser(description=__doc__);p.add_argument('destination',type=Path);args=p.parse_args()
dest=args.destination.resolve()
if dest.exists():p.error('Destination already exists; choose an unused path.')
records=[]
for line in (OLD/'SHA256SUMS').read_text().splitlines():
 if not line.strip():continue
 digest,rel=line.split('  ',1);q=Path(rel)
 if q.is_absolute() or '..' in q.parts:raise ValueError('Unsafe predecessor path')
 candidates=[ROOT/q,OLD/q]
 source=next((v for v in candidates if v.is_file() and hashlib.sha256(v.read_bytes()).hexdigest()==digest),None)
 if source is None:raise ValueError('Missing exact predecessor bytes: '+rel)
 records.append((source,q))
dest.mkdir(parents=True)
for source,q in records:
 target=dest/q;target.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(source,target)
shutil.copy2(OLD/'SHA256SUMS',dest/'SHA256SUMS')
print('Restored',len(records)+1,'exact predecessor files to',dest)
