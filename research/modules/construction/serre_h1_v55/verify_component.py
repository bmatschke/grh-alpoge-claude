#!/usr/bin/env python3
"""Read-only verification of exact local proof/source/inherited bindings."""
from pathlib import Path
import hashlib,json
HERE=Path(__file__).resolve().parent
WORK=HERE.parent
def sha(b):return hashlib.sha256(b).hexdigest()
def read(name):return json.loads((HERE/name).read_text())
proof=(HERE/'main.tex').read_bytes();prov=read('provenance.json')
assert sha(proof)==prov['proof_file_sha256']
ls=proof.splitlines(keepends=True);ids={c['id'] for c in prov['claims']}
inh=read('inherited_inputs.json')['inputs'];inh_ids={x['id'] for x in inh}
assert len(ids)==len(prov['claims'])==prov['new_claim_count']
for c in prov['claims']:
 p=c['proof_location'];b=b''.join(ls[p['line_start']-1:p['line_end']])
 assert sha(b)==p['sha256'] and len(b)==p['bytes'],c['id']
 assert b.splitlines()[0]==('% BEGIN '+c['id']).encode()
 assert b.splitlines()[-1]==('% END '+c['id']).encode()
 assert set(c['depends_on'])<=ids|inh_ids,c['id']
edges={c['id']:[x for x in c['depends_on'] if x in ids] for c in prov['claims']}
seen=set();active=set()
def visit(i):
 assert i not in active,'cycle at '+i
 if i in seen:return
 active.add(i)
 for j in edges[i]:visit(j)
 active.remove(i);seen.add(i)
for i in ids:visit(i)
man=read('source_manifest.json')
for f in man['files']:
 b=(WORK/f['snapshot_file']).read_bytes()
 assert sha(b)==f['sha256'] and len(b)==f['bytes'],f['path']
for r in man['ranges']:
 b=(WORK/r['snapshot_file']).read_bytes();assert sha(b)==r['file_sha256']
 rs=b.splitlines(keepends=True);sl=b''.join(rs[r['line_start']-1:r['line_end']])
 assert sha(sl)==r['range_sha256'] and len(sl)==r['range_bytes'],r['id']
for x in inh:
 b=(WORK/x['proof_file']).read_bytes();p=x['proof_location']
 assert sha(b)==x['proof_file_sha256']
 sl=b''.join(b.splitlines(keepends=True)[p['line_start']-1:p['line_end']])
 assert sha(sl)==x['proof_block_sha256']
 assert sha((WORK/x['provenance_file']).read_bytes())==x['provenance_sha256']
for name in ['source_manifest.json','contracts.json','closure.json','retained_foundations.json','inherited_inputs.json','explicit_inputs.json','hashes.json','tex_validation.json']:
 assert read(name)['proof_file_sha256']==sha(proof),name
assert read('tex_validation.json')['status']=='PASS'
rp=HERE/'independent_review.json'
if rp.exists():
 r=json.loads(rp.read_text())
 if 'proof_file_sha256' in r:assert r['proof_file_sha256']==sha(proof)
 if 'proof_hashes' in r:
  for c in prov['claims']:assert r['proof_hashes'][c['id']]==c['proof_location']['sha256']
print(json.dumps(dict(status='PASS',proof_sha256=sha(proof),claims=len(ids),primary_files=len(man['files']),source_ranges=len(man['ranges']),inherited_bindings=len(inh)),indent=2))
