#!/usr/bin/env python3
"""Read-only local verification of source/proof hashes and the claim DAG."""
from pathlib import Path
import hashlib
import json

HERE = Path(__file__).resolve().parent
WORK = HERE.parent
def sha(b): return hashlib.sha256(b).hexdigest()
def read(n): return json.loads((HERE/n).read_text())
proof=(HERE/'main.tex').read_bytes()
prov=read('provenance.json')
assert sha(proof)==prov['proof_file_sha256']
lines=proof.splitlines(keepends=True)
ids={c['id'] for c in prov['claims']}
assert len(ids)==len(prov['claims'])==prov['new_claim_count']
for c in prov['claims']:
    p=c['proof_location']; b=b''.join(lines[p['line_start']-1:p['line_end']])
    assert sha(b)==p['sha256'] and len(b)==p['bytes'], c['id']
    assert b.splitlines()[0]==('% BEGIN '+c['id']).encode()
    assert b.splitlines()[-1]==('% END '+c['id']).encode()
    assert set(c['depends_on'])<=ids
edges={c['id']:c['depends_on'] for c in prov['claims']}
seen=set(); active=set()
def visit(i):
    assert i not in active, 'cycle at '+i
    if i in seen:return
    active.add(i)
    for j in edges[i]:visit(j)
    active.remove(i);seen.add(i)
for i in ids:visit(i)
manifest=read('source_manifest.json')
for f in manifest['files']+manifest['dependency_files']:
    b=(WORK/f['snapshot_file']).read_bytes()
    assert sha(b)==f['sha256'] and len(b)==f['bytes'], f['path']
for r in manifest['ranges']:
    b=(WORK/r['snapshot_file']).read_bytes()
    assert sha(b)==r['file_sha256']
    ls=b.splitlines(keepends=True)
    sl=b''.join(ls[r['line_start']-1:r['line_end']])
    assert sha(sl)==r['range_sha256'] and len(sl)==r['range_bytes'], r['id']
for x in read('inherited_inputs.json')['inputs']:
    b=(WORK/x['proof_file']).read_bytes();p=x['proof_location']
    assert sha(b)==x['proof_file_sha256']
    sl=b''.join(b.splitlines(keepends=True)[p['line_start']-1:p['line_end']])
    assert sha(sl)==x['proof_block_sha256']
for n in ['source_manifest.json','contracts.json','closure.json','retained_foundations.json',
          'inherited_inputs.json','explicit_inputs.json','hashes.json','tex_validation.json']:
    assert read(n)['proof_file_sha256']==sha(proof),n
assert read('tex_validation.json')['status']=='PASS'
review=HERE/'independent_review.json'
if review.exists():
    q=json.loads(review.read_text())
    if 'proof_file_sha256' in q:assert q['proof_file_sha256']==sha(proof)
    if 'proof_hashes' in q:
        for c in prov['claims']:assert q['proof_hashes'][c['id']]==c['proof_location']['sha256']
print(json.dumps(dict(status='PASS',claims=len(ids),primary_files=len(manifest['files']),
    dependency_files=len(manifest['dependency_files']),source_ranges=len(manifest['ranges']),
    inherited_bindings=len(read('inherited_inputs.json')['inputs']),proof_sha256=sha(proof)),indent=2))
