#!/usr/bin/env python3
"""Independent pinned-Git byte/range audit of the merged v0.14 ledger."""
from pathlib import Path
from collections import Counter
import hashlib
import json
import argparse
from datetime import date
import subprocess
import sys

ART = Path(__file__).resolve().parent.parent
parser = argparse.ArgumentParser(
    description='Independently verify the packaged v0.14 source ledger against pinned Git blobs. '
                'Outputs go to new/empty directories; historical packaged evidence is never overwritten.')
parser.add_argument('--repo', type=Path, default=ART.parent / 'lean-source',
                    help='Git repository at the pinned commit (default: sibling lean-source)')
parser.add_argument('--verification-dir', type=Path,
                    default=ART.parent / 'source_verification_v0_14_rerun',
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
AUDIT_JSON = OUT / 'source_verification_v0_14_audit.json'
LOG = OUT / 'source_verification_v0_14_backtrack.log'


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
for claim_id,entry in [('AN1',1),('SF7',1),('FC19',1),('DR3',6),('CV9',1),('NB8',1),('VE11',1),('RF16',1)]:
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
after_status=git('status','--porcelain=v1','--untracked-files=no')
assert after_status==before_status==b'', 'Lean tracked worktree changed during audit'
assert git('rev-parse','HEAD').decode().strip()==PIN

log_parts=['UNCHANGED BACKTRACK --CHECK-ALL\n'+check['stdout'],
           'UNCHANGED BACKTRACK --LIST\n'+listing['stdout']]
for r in lookups:
    log_parts += ['LOOKUP '+' '.join(r['arguments'])+'\n'+r['stdout']]
LOG.write_text('\n\n'.join(log_parts),encoding='utf-8')
summary=dict(result='PASS',commit=PIN,input_sha256=input_sha,
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
    formal_verification=dict(lean_compilation=False,kernel_replay=False,mathematical_proof_verification=False))
AUDIT_JSON.write_text(json.dumps(summary,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')

report='''INDEPENDENT PINNED-SOURCE BYTE AND RANGE AUDIT RERUN — v0.14
Audit implementation: packaged portable derivative of /root/global_frame historical audit
Date: '''+date.today().isoformat()+'''
Result: PASS

PINNED SOURCE AND INPUT SNAPSHOT

Repository: https://github.com/CocoSgt/riemann-hypothesis-lean
Commit: '''+PIN+'''
The source repository HEAD matched this commit before and after the audit.
Its tracked worktree was clean before and after; no checkout, reset, source
edit, build, or other worktree mutation was performed.

Exact audited merged-input SHA256 values:
'''+''.join('  '+name+': '+value+'\n' for name,value in input_sha.items())+'''
All four audited input files remained byte-identical throughout the audit.
The source_index.json source-file record array was exactly equal to the
merged provenance.json source_files array, including record order and fields.

ACTUAL COVERAGE

'''+''.join('  '+key.replace('_',' ')+': '+str(value)+'\n' for key,value in summary['counts'].items())+'''
The distinct source-file count exceeds the indexed count because the
continuation targets introduce additional paths. Every such target-only
path was read from the same pinned commit and fully checked.

METHOD

1. Loaded the current merged provenance.json, source_index.json and
   next_source_targets.json; checked their commit IDs and stable-claim-ID
   uniqueness. Collected every source-file record, all claim sources, and
   every recursively recorded next-target range. Every path was checked to
   be relative, under src/, and free of parent-directory traversal.
2. Read each distinct source blob once with a single git cat-file --batch
   process, requesting the exact <commit>:<path> object. The working tree
   was not used as the authoritative source. Checked the blob type, exact
   byte length, and Git blob object ID against the returned raw bytes.
3. Computed SHA256 on the original complete file bytes and each literal
   one-indexed inclusive line slice using splitlines(keepends=True). No
   Unicode, whitespace, line-ending, or newline normalization was applied.
   Checked every required hash and 1 <= first <= last <= file line count.
   Checked the additional full_file_sha256, range_bytes, first_line,
   declaration-line bounds, and indexed byte/line-count fields wherever
   present. All checks passed.
4. Wrote exactly the required pinned source files, and no extras, under
   '''+str(VERIFY)+'''. Re-read every copy and compared it with
   its original Git blob. This separate verification tree allowed the
   unchanged user backtrack.py to read all needed files without modifying
   the sparse Lean checkout.

Successful auxiliary metadata checks:
'''+''.join('  '+key.replace('_',' ')+': '+str(value)+'\n' for key,value in sorted(stats.items()))+'''
UNCHANGED USER BACKTRACK CHECK

Executed:
  '''+sys.executable+' '+str(ART/'backtrack.py')+' --repo '+str(VERIFY)+''' --check-all

Exit code: 0. Exact output:
'''+check['stdout']+'''
Also executed --list: all '''+str(len(ids))+''' stable claim IDs appeared in exactly the
merged-ledger order. Eight representative read-only source lookups passed:
'''+''.join('  '+r['arguments'][0]+' --entry '+r['arguments'][4]+' --max-lines 3\n' for r in lookups)+'''
Each lookup used --repo '''+str(VERIFY)+''', returned exit code 0,
and displayed the requested declaration, exact source path/range hash,
and correctly numbered initial source lines. The selections cover the
original RH endpoint, a prior common-frame claim, the new direct Forms0
assembly, full IsPtOf interface, chart values, down naturality, the final
realizability-based comparison join, and refill closure.

REPRODUCIBILITY AND LIMITS

The rerun script is '''+str(Path(__file__).resolve())+'''.
Machine-readable results: '''+str(AUDIT_JSON)+'''
Exact checker/list/lookup outputs: '''+str(LOG)+'''
The verification directory contains only the pinned source files necessary
for this audit. Historical packaged audit evidence was not overwritten.

This verifies source provenance, complete bytes, exact inclusive ranges,
recorded metadata, and the preserved backtracking interface. It does not
compile Lean, replay the Lean kernel, prove the mathematical statements,
or establish the wider RH/GRH conclusion. No PDF was built or rendered.
'''
REPORT.write_text(report,encoding='utf-8')
print(json.dumps({k:v for k,v in summary.items() if k not in ['source_file_object_ids','lookup_arguments']},ensure_ascii=False,indent=2))
print('Saved '+str(REPORT))
