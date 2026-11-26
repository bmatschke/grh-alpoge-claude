#!/usr/bin/env python3
"""Read-only claim lookup and exact source verification for the RH reconstruction."""
from pathlib import Path
import argparse
import hashlib
import json
import re
import sys

ROOT = Path(__file__).resolve().parent
parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('claim', nargs='?', help='Claim ID, for example RU8, RD15, HM12, TC6, or SW8.')
parser.add_argument('--repo', type=Path, help='Local pinned source checkout, containing src/.')
parser.add_argument('--entry', type=int, help='Print only this numbered source entry (one-based).')
parser.add_argument('--max-lines', type=int, default=160, help='Maximum excerpt lines per entry; default 160.')
parser.add_argument('--list', action='store_true', help='List every stable claim ID and title.')
parser.add_argument('--check-all', action='store_true', help='Verify every source-file and inclusive-range hash, including next targets; requires --repo.')
args = parser.parse_args()
ledger = json.loads((ROOT / 'provenance.json').read_text(encoding='utf-8'))
claims = {c['id']: c for c in ledger['claims']}
cache = {}

def source_ranges(value):
    if isinstance(value, dict):
        if {'path', 'sha256', 'line_start', 'line_end', 'range_sha256'} <= value.keys():
            yield value
        else:
            for child in value.values():
                yield from source_ranges(child)
    elif isinstance(value, list):
        for child in value:
            yield from source_ranges(child)

def checked_source(record):
    rel = Path(record['path'])
    if rel.is_absolute() or '..' in rel.parts:
        raise ValueError(f'Non-relative source path: {rel}')
    path = args.repo / rel
    if record['path'] not in cache:
        try:
            raw = path.read_bytes()
        except OSError as exc:
            raise ValueError(f'{path}: {exc}') from exc
        cache[record['path']] = (hashlib.sha256(raw).hexdigest(), raw.splitlines(keepends=True))
    digest, lines = cache[record['path']]
    if digest != record['sha256']:
        raise ValueError(f'File hash mismatch: {path}\nexpected {record["sha256"]}\nobserved {digest}')
    if 'range_sha256' in record:
        first, last = record['line_start'], record['line_end']
        if not (isinstance(first, int) and isinstance(last, int) and 1 <= first <= last <= len(lines)):
            raise ValueError(f'Invalid inclusive source range: {path}:{first}-{last}')
        if hashlib.sha256(b''.join(lines[first - 1:last])).hexdigest() != record['range_sha256']:
            raise ValueError(f'Inclusive source-range hash mismatch: {path}:{first}-{last}')
    return [line.decode('utf-8').rstrip('\r\n') for line in lines]

def update_keys(claim):
    pairs = []
    for key in claim:
        match = re.fullmatch(r'version_(\d+)_(\d+)_update', key)
        if match:
            pairs.append((tuple(map(int, match.groups())), key))
    return [key for _, key in sorted(pairs)]

def show_field(key, value):
    shown = value if isinstance(value, str) else json.dumps(value, ensure_ascii=False)
    print(key.replace('_', ' ') + ': ' + shown)

def latest_proofs(claim):
    updates = update_keys(claim)
    if not updates:
        return
    update = claim[updates[-1]]
    linked = update.get('discharged_by', []) if isinstance(update, dict) else []
    if isinstance(linked, str):
        linked = re.findall(r'\b[A-Z]+[0-9]+\b', linked)
    linked = [cid for cid in dict.fromkeys(linked) if cid in claims]
    if linked:
        print('\nLatest linked proof locations (' + updates[-1] + '):')
        for cid in linked:
            proof = claims[cid].get('proof_location', {})
            print('  ' + cid + ': ' + json.dumps(proof, ensure_ascii=False))

if args.max_lines < 1:
    parser.error('--max-lines must be positive')
if args.check_all:
    if args.repo is None:
        parser.error('--check-all requires --repo')
    targets_path = ROOT / 'next_source_targets.json'
    target_records = list(source_ranges(json.loads(targets_path.read_text(encoding='utf-8')))) if targets_path.exists() else []
    source_records = [record for c in ledger['claims'] for record in c['sources']]
    errors = []
    for record in [*ledger['source_files'], *source_records, *target_records]:
        try:
            checked_source(record)
        except ValueError as exc:
            errors.append(str(exc))
    if errors:
        print('\n\n'.join(dict.fromkeys(errors)), file=sys.stderr)
        sys.exit(1)
    print(f'Verified {len(cache)} distinct source files, {len(source_records)} claim-source ranges, and {len(target_records)} next-target ranges against the SHA256 records for pinned commit {ledger["commit"]}.')
    print('This checks recorded source bytes and ranges; it does not compile Lean or replay its kernel.')
if args.list:
    for claim in ledger['claims']:
        print(f'{claim["id"]:5} {claim["title"]}')
if args.claim:
    claim = claims.get(args.claim.upper())
    if claim is None:
        parser.error(f'Unknown claim {args.claim!r}; use --list')
    print(f'{claim["id"]} — {claim["title"]}\nHistorical/recorded status: {claim["status"]}')
    fields = ['statement', 'claims', 'remaining_inputs', 'assumptions', 'source_relation',
              *update_keys(claim), 'proof_location', 'expanded_notes', 'depends_on',
              'dependencies', 'merged_application', 'merged_scope_classification',
              'resolved_companion_inputs', 'merge_scope_note']
    for key in fields:
        if key in claim:
            show_field(key, claim[key])
    latest_proofs(claim)
    if args.entry is not None and not 1 <= args.entry <= len(claim['sources']):
        parser.error(f'--entry must be between 1 and {len(claim["sources"])}')
    for number, record in enumerate(claim['sources'], 1):
        if args.entry is not None and args.entry != number:
            continue
        print(f'\n[{number}] {record["declaration"]}\n{record["path"]}:{record["line_start"]}–{record["line_end"]}\n{record["url"]}\nFile SHA256 {record["sha256"]}\nInclusive-range SHA256 {record["range_sha256"]}')
        if args.repo is not None:
            try:
                lines = checked_source(record)
            except ValueError as exc:
                print(str(exc), file=sys.stderr)
                sys.exit(1)
            stop = min(record['line_end'], record['line_start'] + args.max_lines - 1)
            for line_number in range(record['line_start'], stop + 1):
                print(f'{line_number:6}  {lines[line_number - 1]}')
            if stop < record['line_end']:
                print(f'... excerpt capped at {args.max_lines} lines; increase --max-lines to read the rest.')
if not (args.claim or args.list or args.check_all):
    parser.print_help()
