#!/usr/bin/env python3
"""Independent pinned-Git byte/range audit of the merged v0.22 ledger."""
from pathlib import Path
from collections import Counter
import hashlib
import json
import argparse
from datetime import date
import subprocess
import sys
sys.dont_write_bytecode = True
from source_audit_locations_v0_22 import audit_locations_and_continuity

ART = Path(__file__).resolve().parent.parent
parser = argparse.ArgumentParser(
    description='Independently verify the packaged v0.22 source ledger against pinned Git blobs. '
                'Outputs go to new/empty directories; historical packaged evidence is never overwritten.')
parser.add_argument('--repo', type=Path, default=ART.parent / 'lean-source',
                    help='Git repository at the pinned commit (default: sibling lean-source)')
parser.add_argument('--verification-dir', type=Path,
                    default=ART.parent / 'source_verification_v0_22',
                    help='new/empty directory for exact pinned source copies')
parser.add_argument('--output-dir', type=Path,
                    help='new/empty directory for the new report, JSON and log '
                         '(default: verification directory name plus _results)')
args = parser.parse_args()
REPO = args.repo.expanduser().resolve()
VERIFY = args.verification_dir.expanduser().resolve()
OUT = (args.output_dir.expanduser().resolve() if args.output_dir else
       VERIFY.parent / (VERIFY.name + '_results'))
PIN = '7cbf7a0c32fca1badf05931879a37c3f8a2b03b4'

def within(path, root):
    return path == root or root in path.parents

for destination in [VERIFY, OUT]:
    if any(within(destination, root) or within(root, destination) for root in [ART, REPO]):
        parser.error('output directories must be outside, and must not contain, the artifact or Git repository')
    if destination.exists() and (not destination.is_dir() or any(destination.iterdir())):
        parser.error(str(destination) + ' must be new or empty; no deletion or overwrite performed')
if within(VERIFY, OUT) or within(OUT, VERIFY):
    parser.error('verification and output directories must be separate, with neither containing the other')
OUT.mkdir(parents=True, exist_ok=True)
REPORT = OUT / 'source_verification.txt'
AUDIT_JSON = OUT / 'source_verification_v0_22_audit.json'
LOG = OUT / 'source_verification_v0_22_backtrack.log'


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def ranges(value):
    if isinstance(value, dict):
        if {'path','sha256','line_start','line_end','range_sha256'} <= value.keys():
            yield value
        else:
            for child in value.values():
                yield from ranges(child)
    elif isinstance(value, list):
        for child in value:
            yield from ranges(child)


def git(*args):
    return subprocess.check_output(['git','-C',str(REPO),*args])


def check_path(path):
    rel = Path(path)
    assert not rel.is_absolute() and '..' not in rel.parts, ('unsafe path',path)
    assert rel.parts and rel.parts[0] == 'src', ('non-source path',path)
    return rel


initial = {name:(ART/name).read_bytes() for name in
           ['provenance.json','source_index.json','next_source_targets.json','backtrack.py']}
input_sha = {name:sha(raw) for name,raw in initial.items()}
ledger = json.loads(initial['provenance.json'])
index = json.loads(initial['source_index.json'])
targets = json.loads(initial['next_source_targets.json'])
assert ledger['commit'] == index['commit'] == targets['commit'] == PIN
assert git('rev-parse','HEAD').decode().strip() == PIN
before_status = git('status','--porcelain=v1','--untracked-files=no')
assert not before_status, 'Lean tracked worktree was not clean before read-only audit'
claims = ledger['claims']
ids = [c['id'] for c in claims]
navigation_audit, artifact_snapshots = audit_locations_and_continuity(ART, ledger)
for code_file in ['reviews_v0_22/source_verification_v0_22_audit_portable.py',
                  'reviews_v0_22/source_audit_locations_v0_22.py']:
    artifact_snapshots[code_file] = (ART/code_file).read_bytes()
print('Continuity and proof-file navigation checks passed; reading pinned Git blobs.', flush=True)
assert len(ids) == len(set(ids)), 'duplicate stable claim IDs'
assert index['source_files'] == ledger['source_files'], 'source-index records differ from merged ledger'
claim_sources = [(c['id'],i,s) for c in claims for i,s in enumerate(c['sources'],1)]
target_sources = list(ranges(targets))
all_ranges = [s for _,_,s in claim_sources]+target_sources
file_records = [*ledger['source_files'],*index['source_files'],*targets.get('source_files',[])]
needed = sorted({s['path'] for s in [*file_records,*all_ranges]})
for path in needed:
    check_path(path)
if VERIFY.exists():
    assert not any(VERIFY.iterdir()), 'verification directory must be new or empty; no deletion performed'
else:
    VERIFY.mkdir(parents=True)

# One process reads all unique commit:path objects; no checkout or worktree read
# is used as the authoritative source. No git checkout/add/reset/build is run.
proc = subprocess.Popen(['git','-C',str(REPO),'cat-file','--batch'],
                        stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
assert proc.stdin is not None and proc.stdout is not None
blobs, lines, blob_oids = {}, {}, {}
for path in needed:
    spec=f'{PIN}:{path}'.encode('utf-8')
    proc.stdin.write(spec+b'\n')
    proc.stdin.flush()
    header=proc.stdout.readline().rstrip(b'\n').split()
    assert len(header)==3 and header[1]==b'blob', ('missing/nonblob pinned object',path,header)
    oid=header[0].decode('ascii')
    size=int(header[2])
    raw=proc.stdout.read(size)
    assert len(raw)==size and proc.stdout.read(1)==b'\n', ('truncated cat-file stream',path)
    actual_oid=hashlib.sha1(b'blob '+str(size).encode()+b'\0'+raw).hexdigest()
    assert oid==actual_oid, ('Git blob object-ID mismatch',path,oid,actual_oid)
    blobs[path]=raw
    lines[path]=raw.splitlines(keepends=True)
    blob_oids[path]=oid
    dest=VERIFY/check_path(path)
    dest.parent.mkdir(parents=True,exist_ok=True)
    dest.write_bytes(raw)
proc.stdin.close()
stderr=proc.stderr.read() if proc.stderr else b''
code=proc.wait(timeout=30)
assert code==0, ('cat-file failed',code,stderr.decode(errors='replace'))

stats=Counter()
for r in file_records:
    raw=blobs[r['path']]
    assert sha(raw)==r['sha256'], ('indexed full-file SHA mismatch',r['path'])
    stats['indexed_full_file_checks']+=1
    for key in ['bytes','size_bytes']:
        if key in r:
            assert r[key]==len(raw), ('indexed byte count mismatch',r['path'],key,r[key],len(raw))
            stats['file_size_checks']+=1
    for key in ['line_count','lines']:
        if key in r:
            assert r[key]==len(lines[r['path']]), ('indexed line count mismatch',r['path'],key)
            stats['file_line_count_checks']+=1

distinct_ranges=set()
for r in all_ranges:
    path=r['path']; raw=blobs[path]; ls=lines[path]
    assert sha(raw)==r['sha256'], ('range full-file SHA mismatch',path,r['declaration'])
    first,last=r['line_start'],r['line_end']
    assert type(first) is int and type(last) is int and 1<=first<=last<=len(ls), ('invalid inclusive bounds',path,first,last)
    rr=b''.join(ls[first-1:last])
    assert sha(rr)==r['range_sha256'], ('range SHA mismatch',path,first,last,r['declaration'])
    stats['inclusive_range_sha_checks']+=1
    distinct_ranges.add((path,first,last,r['range_sha256']))
    if 'full_file_sha256' in r:
        assert r['full_file_sha256']==sha(raw), ('duplicate full-file SHA mismatch',path)
        stats['explicit_full_file_sha_checks']+=1
    if 'range_bytes' in r:
        assert r['range_bytes']==len(rr), ('range byte count mismatch',path,first,last)
        stats['range_byte_count_checks']+=1
    if 'first_line' in r:
        assert r['first_line']==ls[first-1].decode('utf-8').rstrip('\r\n'), ('first-line mismatch',path,first,r['first_line'])
        stats['first_line_checks']+=1
    for number in r.get('declaration_lines_within_range',[]):
        assert type(number) is int and first<=number<=last, ('declaration-line bounds mismatch',path,number,first,last)
        stats['declaration_line_bounds_checks']+=1

actual_paths={p.relative_to(VERIFY).as_posix() for p in VERIFY.rglob('*') if p.is_file()}
assert actual_paths==set(needed), 'verification tree contains missing or extra files'
for path,raw in blobs.items():
    assert (VERIFY/path).read_bytes()==raw, ('verification copy mismatch',path)

def run_backtrack(arguments):
    command=[sys.executable,str(ART/'backtrack.py'),*arguments]
    result=subprocess.run(command,capture_output=True,text=True,timeout=55)
    assert result.returncode==0, ('unchanged backtrack failed',arguments,result.stdout,result.stderr)
    return dict(arguments=arguments,exit_code=result.returncode,stdout=result.stdout,stderr=result.stderr)

check=run_backtrack(['--repo',str(VERIFY),'--check-all'])
listing=run_backtrack(['--list'])
listed=[line.split()[0] for line in listing['stdout'].splitlines() if line.strip()]
assert listed==ids, 'backtrack --list differs from stable claim order'
lookups=[]
for claim_id,entry in [('AN1',1),('SF7',1),('FC19',1),('DR3',6),('CV9',1),('NB8',1),('VE11',1),('RF16',1),
                       ('TL13',1),('TL21',1),('TG12',1),('PN16',1),
                       ('SZ11',1),('SZ13',1),('AC7',1),('AC10',1),
                       ('PA15',1),('TA10',1),('TA12',1),('TA14',1),('AH16',1),
                       ('CI13',1),('CI19',1),('TX5',1),('TX10',1),('TX16',1),('VI3',1),('VI7',1),('VI9',1),('VI11',1),
                       ('CA2',1),('CA9',1),('CA11',1),('CA13',1),
                       ('NC4',1),('NC8',1),('NC12',1),('NC16',1),('NC17',1),
                       ('SE6',1),('SE9',1),('SE11',1),('SE12',1),('SE14',1),('SE16',1),
                       ('IG1',1),('IG3',1),('IG9',1),('IG10',1),('IG12',1),('IG14',1),
                       ('RC2',1),('RC6',1),('RC11',1),('RC13',1),('RC19',1),('RC20',1),('RC21',1),
                       ('LS1',1),('LS6',1),('LS7',1),('LS13',1),('LS16',1),('LS17',1),('LS21',1),('LS22',1),
                       ('TD3',1),('TD8',1),('TD13',1),('TD16',1),
                       ('QW1',1),('QW6',1),('QW9',1),('QW11',1),('QW12',1),('QW15',1),
                       ('AR5',1),('AR8',1),('AR11',1),('AR14',1),('AR18',1),('AR22',1),
                       ('HF4',1),('HF13',1),('HF16',1),('HF18',1),('HF19',1),('HF20',1),
                       ('TT3',1),('TT6',1),('TT8',1),('TT10',1),('TT11',1),('TT12',1),
                       ('TT13',1),('TT15',1),('TT16',1),('TT17',1),('TT18',1),('TT19',1),
                       ('GA1',1),('GA6',1),('GA8',1),('GA15',1),('GA23',1),
                       ('WA3',1),('WA8',1),('WA11',1),('WA16',1),('WA19',1),
                       ('MF4',1),('MF5',1),('MF9',1),('MF16',1),('MF19',1),('MF20',1),
                       ('QR5',1),('QR9',1),('QR13',1),('QR14',1),('QR24',1),('QR25',1),
                       ('NR1',1),('NR7',1),('NR11',1),('NR15',1),('NR18',1),('NR20',1),('NR24',1),
                       ('CW4',1),('CW9',1),('CW13',1),('CW16',1),('CW21',1),('CW24',1),('CW25',1),
                       ('GV5',1),('GV7',1),('GV10',1),('GV13',1),('GV19',1),('GV21',1),
                       ('CC1',1),('CC8',1),('CC14',1),('CC16',1),('CC19',1),('CC20',1)] + [
                       (f'{prefix}{i}',1) for prefix,n in [('MR',26),('QD',22),('DC',22),('QP',25)] for i in range(1,n+1)]:
    record=run_backtrack([claim_id,'--repo',str(VERIFY),'--entry',str(entry),'--max-lines','3'])
    claim=next(c for c in claims if c['id']==claim_id)
    s=claim['sources'][entry-1]
    assert record['stdout'].startswith(claim_id+' — ')
    assert f"[{entry}] {s['declaration']}" in record['stdout']
    assert s['path'] in record['stdout'] and s['range_sha256'] in record['stdout']
    first=s['line_start']
    assert f'{first:6}  ' in record['stdout']
    lookups.append(record)

for name,raw in initial.items():
    assert (ART/name).read_bytes()==raw, ('merged input changed during audit',name)
for name, raw in artifact_snapshots.items():
    assert (ART/name).read_bytes() == raw, ('audited artifact evidence changed during audit', name)
after_status=git('status','--porcelain=v1','--untracked-files=no')
assert after_status==before_status==b'', 'Lean tracked worktree changed during audit'
assert git('rev-parse','HEAD').decode().strip()==PIN

log_parts=['UNCHANGED BACKTRACK --CHECK-ALL\n'+check['stdout'],
           'UNCHANGED BACKTRACK --LIST\n'+listing['stdout']]
for r in lookups:
    log_parts += ['LOOKUP '+' '.join(r['arguments'])+'\n'+r['stdout']]
LOG.write_text('\n\n'.join(log_parts),encoding='utf-8')
summary=dict(result='PASS',reviewer_executor='/root/class_rank',commit=PIN,input_sha256=input_sha,
    counts=dict(claims=len(claims),claim_source_ranges=len(claim_sources),next_target_ranges=len(target_sources),
        indexed_source_files=len(ledger['source_files']),next_target_source_files=len(targets.get('source_files',[])),
        distinct_pinned_source_blobs=len(needed),distinct_range_tuples=len(distinct_ranges),
        target_only_source_files=len(set(needed)-{r['path'] for r in ledger['source_files']}),
        total_pinned_source_bytes=sum(map(len,blobs.values())),lookup_tests=len(lookups)),
    checks=dict(stats),backtrack_check_all=check['stdout'].strip(),
    lookup_arguments=[r['arguments'] for r in lookups],
    method='git cat-file --batch with pinned commit:path requests; verify raw blob object IDs, SHA256s, and raw inclusive slices',
    verification_directory=str(VERIFY),verification_tree_extra_files=0,
    unchanged_merged_inputs=True,unchanged_clean_lean_tracked_worktree=True,
    source_file_object_ids=blob_oids,
    preserved_claim_fields=navigation_audit['old_claim_fields_preserved'],
    preserved_old_claims=navigation_audit['old_claims_preserved'],
    preserved_old_source_records=navigation_audit['old_source_file_records_preserved'],
    predecessor_manifest_files_verified=navigation_audit['predecessor_manifest_files_verified'],
    predecessor_package_files_verified=navigation_audit['predecessor_package_files_verified'],
    archived_predecessor_root_files=navigation_audit['archived_predecessor_root_files'],
    legacy_navigation_counts=navigation_audit['legacy_navigation_counts'],
    proof_navigation_counts=navigation_audit['proof_navigation_counts'],
    archival_corpus_fallback_without_claim_id_text=navigation_audit['archival_corpus_fallback_without_claim_id_text'],
    historical_anchor_text_not_found=navigation_audit['historical_anchor_text_not_found'],
    audited_artifact_file_sha256={name:sha(raw) for name,raw in sorted(artifact_snapshots.items())},
    formal_verification=dict(lean_compilation=False,kernel_replay=False,mathematical_proof_verification=False))
AUDIT_JSON.write_text(json.dumps(summary,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')

NAVIGATION_JSON = OUT / 'proof_location_audit_v0_22.json'
NAVIGATION_JSON.write_text(json.dumps(navigation_audit, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')


report = f"""PINNED-SOURCE, CONTINUITY AND PROOF-NAVIGATION AUDIT — v0.22
Result: PASS
Executor: /root/class_rank
Date: {date.today().isoformat()}
Pin: {PIN}

This read-only checker obtains every source from git cat-file --batch at
the exact commit:path. It does not treat sparse worktree presence as source
authority. Full Git object IDs, SHA256s, byte/line counts and inclusive
range hashes are verified. Declaration spellings and pinned URLs are
checked under their recorded conventions.

Counts:
{json.dumps(summary['counts'],ensure_ascii=False,indent=2)}

Checks:
{json.dumps(summary['checks'],ensure_ascii=False,indent=2)}

The unchanged backtrack.py passes --check-all and --list. Retained historical
lookups and every one of the 95 new claim IDs are exercised with source
excerpts. The log preserves the actual commands and outputs.

All {navigation_audit['old_claims_preserved']} predecessor claims, every old
source record/dependency list/conclusion object, all 1064 v0.21 manifest
entries plus the manifest itself, and all four global branch records are
preserved. Nineteen previous root files are archived under
history/version_0_21/. New components and the audit code are snapshotted
and confirmed unchanged throughout execution.

Every new paragraph marker, raw paragraph SHA256 and inclusive proof range
is checked. Explicit historical file references resolve. Legacy evidence
is faithfully disclosed: 75 component-corpus fallbacks, GF3 without a
literal ID occurrence, and the five retained absent textual anchors
WT8, PG4, PG10, FG3 and OR4. No exact pointers are invented for them.

Navigation counts:
{json.dumps(navigation_audit['proof_navigation_counts'],indent=2)}

All old construction-before-join guards remain; new MR/QD/DC/QP boundaries
are checked. This verifies the recorded human graph, not the transitive
Lean graph. Named classical premises and stronger remaining same-object
joins are not converted to proofs by hashes or source matches.

The repository HEAD stayed pinned, its tracked worktree stayed clean,
and no reviewed artifact or cumulative source input changed. No Lean
build, kernel replay, automated mathematical proof checking, current PDF
render or visual layout review is claimed.

Inputs:
{json.dumps(input_sha,indent=2)}

Portable checker: reviews_v0_22/source_verification_v0_22_audit_portable.py
Navigation helper: reviews_v0_22/source_audit_locations_v0_22.py
Explicit aliases: reviews_v0_22/proof_location_aliases_v0_22.json
Machine record: source_verification_v0_22_audit.json
Navigation record: proof_location_audit_v0_22.json
Backtrack log: source_verification_v0_22_backtrack.log
"""
REPORT.write_text(report,encoding='utf-8')
print(json.dumps({'result':'PASS','counts':summary['counts'],'output_dir':str(OUT)},indent=2))
