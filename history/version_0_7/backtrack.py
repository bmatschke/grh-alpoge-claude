#!/usr/bin/env python3
"""Read-only source lookup for the RH reconstruction's stable claim IDs."""
from pathlib import Path
import argparse
import hashlib
import json
import sys

parser=argparse.ArgumentParser(description=__doc__)
parser.add_argument('claim',nargs='?',help='Claim ID, for example CG6, LA5, GP5, RS8, or RK3.')
parser.add_argument('--repo',type=Path,help='Root of a local checkout, containing src/.')
parser.add_argument('--entry',type=int,help='Print only this numbered source entry (one-based).')
parser.add_argument('--max-lines',type=int,default=160,help='Maximum excerpt lines per entry; default 160.')
parser.add_argument('--list',action='store_true',help='List all claim IDs and titles.')
parser.add_argument('--check-all',action='store_true',help='Verify all source-file hashes; requires --repo.')
args=parser.parse_args()
ledger=json.loads((Path(__file__).resolve().parent/'provenance.json').read_text())

def checked_source(record):
    path=args.repo/record['path']
    try:raw=path.read_bytes()
    except OSError as exc:raise ValueError(f'{path}: {exc}') from exc
    got=hashlib.sha256(raw).hexdigest()
    if got!=record['sha256']:
        raise ValueError(f'Hash mismatch: {path}\nexpected {record["sha256"]}\nobserved {got}')
    return raw.decode().splitlines()

if args.max_lines<1:parser.error('--max-lines must be positive')
if args.check_all:
    if args.repo is None:parser.error('--check-all requires --repo')
    errors=[]
    for rec in ledger['source_files']:
        try:checked_source(rec)
        except ValueError as exc:errors.append(str(exc))
    if errors:
        print('\n\n'.join(errors),file=sys.stderr);sys.exit(1)
    print(f'All {len(ledger["source_files"])} source hashes agree with commit {ledger["commit"]}.')
if args.list:
    for c in ledger['claims']:print(f'{c["id"]:5} {c["title"]}')
if args.claim:
    c=next((c for c in ledger['claims'] if c['id']==args.claim.upper()),None)
    if c is None:parser.error(f'Unknown claim {args.claim!r}; use --list')
    print(f'{c["id"]} — {c["title"]}\nStatus: {c["status"]}')
    for k in ['statement','claims','remaining_inputs','assumptions','source_relation','version_0_3_update','version_0_4_update','version_0_5_update','version_0_6_update','version_0_7_update']:
        if k in c:print(k.replace('_',' ')+': '+(c[k] if isinstance(c[k],str) else json.dumps(c[k],ensure_ascii=False)))
    if args.entry is not None and not 1<=args.entry<=len(c['sources']):
        parser.error(f'--entry must be between 1 and {len(c["sources"])}')
    for i,s in enumerate(c['sources'],1):
        if args.entry is not None and args.entry!=i:continue
        print(f'\n[{i}] {s["declaration"]}\n{s["path"]}:{s["line_start"]}–{s["line_end"]}\n{s["url"]}\nSHA-256 {s["sha256"]}')
        if args.repo is not None:
            try:lines=checked_source(s)
            except ValueError as exc:print(str(exc),file=sys.stderr);sys.exit(1)
            stop=min(s['line_end'],s['line_start']+args.max_lines-1)
            for n in range(s['line_start'],stop+1):print(f'{n:6}  {lines[n-1]}')
            if stop<s['line_end']:print(f'... excerpt capped at {args.max_lines} lines; increase --max-lines to read the rest.')
if not(args.claim or args.list or args.check_all):parser.print_help()
