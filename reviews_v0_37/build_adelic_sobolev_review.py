#!/usr/bin/env python3
"""Bind root's independent mathematical review of ASB1--14 to final bytes."""
from pathlib import Path
import argparse,hashlib,json,subprocess
p=argparse.ArgumentParser();p.add_argument('--root',type=Path,default=Path(__file__).resolve().parent)
p.add_argument('--human-root',type=Path,default=Path(__file__).resolve().parent.parent/'reconstruction_v036')
p.add_argument('--source',type=Path,default=Path(__file__).resolve().parent.parent/'lean_source')
a=p.parse_args();root=a.root.resolve();comp=root/'adelic_sobolev';out=root/'reviews_v0_37';out.mkdir(exist_ok=True)
sha=lambda b:hashlib.sha256(b).hexdigest();pin='7cbf7a0c32fca1badf05931879a37c3f8a2b03b4'
raw=(comp/'main.tex').read_bytes();lines=raw.splitlines(keepends=True)
prov=json.loads((comp/'provenance.json').read_text());cl=json.loads((comp/'closure.json').read_text())
assert prov['main_tex_sha256']==cl['main_tex_sha256']==sha(raw)
assert cl['provenance_sha256']==sha((comp/'provenance.json').read_bytes())
notes=[
 'Actual tensor topology and real lift retain original atTau and oneP. The skew-Hermitian Lie spaces give a one-place basis and finite/real factors commute.',
 'Cayley coordinates and the inverse function theorem give the actual ordered-product chart. Compactness supplies uniform inverse-Lipschitz control before the shift; rank zero is explicit.',
 'The common neighborhood is ar inverse(V) intersect a inverse(U). The finite factor a_x is independent of t and belongs to exactly the supplied U intersect Gf.',
 'The inverse Lipschitz outer-measure bound is valid on subsets. Layer-cake integration and averaging over one compact positive-Haar neighborhood require only left Haar invariance.',
 'The one-dimensional endpoint inequality has constants 2/s and 2s. Induction integrates the last curve and prepends its derivative, without commuting noncommuting Lie letters.',
 'The complete list of words up to the real dimension precedes psi and y. Second-kind charts justify iterated differentiability and finite-level commutation gives the exact invariant integrands.',
 'Finite cover by integral-adele cosets gives one positive denominator. All local integrality implies global integrality through monic minimal-polynomial coefficients.',
 'Original tensor coordinates are continuous. One denominator clears all coefficient compact images and another clears the chosen field basis; the original module topology is retained.',
 'Trace discriminants give a finite free integral lattice. The inverse embedding matrix bounds coordinates by the actual maximum over all complex embeddings.',
 'Counting bounded integral coordinate arrays yields exponent [E:Q]n^2 before denominator/radius, including the empty matrix case.',
 'The literal sum of entries and inverse entries is continuous, inverse invariant and submultiplicative. The CM-type dictionary covers every complex embedding up to conjugation.',
 'The injection gamma -> gamma gamma0 inverse has the stated multiplication order. Its denominator is fixed from x and Omega before u,y; the height radius yields exponent 2[E:Q]n^2.',
 'Unfolding counts rational preimages on the unchanged fundamental domain. Integer k<=M implies k<=M^2 for nonnegative k; global AE and left Haar give the exact L2 comparison.',
 'ASB6 then ASB12 choose N,list before x,Cx before F,psi,u. SPR13 supplies the same-U representative; continuous uniqueness identifies every permitted psi. Taking square roots gives the literal full pointwise_growth contract without a circular edge.'
]
assert len(notes)==len(prov['claims'])==14
reviews=[];cache={};refs=0
for c,note in zip(prov['claims'],notes):
 loc=c['proof_location'];part=b''.join(lines[loc['line_start']-1:loc['line_end']])
 assert sha(part)==loc['sha256'];assert part.startswith(('% BEGIN '+c['id']).encode())
 reviews.append({'id':c['id'],'status':'PASS','proof_range':loc,'depends_on':c['depends_on'],'review':note})
for s in prov['source_inventory']:
 path=s['path']
 if path not in cache:
  b=(a.source/path).read_bytes();assert b==subprocess.check_output(['git','show',pin+':'+path],cwd=a.source);cache[path]=b
 b=cache[path];assert sha(b)==s.get('file_sha256',s.get('sha256'))
 assert sha(b''.join(b.splitlines(keepends=True)[s['line_start']-1:s['line_end']]))==s['range_sha256'];refs+=1
inherited=[]
for h in prov['baseline_dependencies']:
 path=(root/h['file']) if (root/h['file']).is_file() else a.human_root/h['file']
 b=path.read_bytes();assert sha(b)==h.get('file_sha256',h.get('sha256'))
 for c in h['claims']:
  assert sha(b''.join(b.splitlines(keepends=True)[c['line_start']-1:c['line_end']]))==c['sha256'];inherited.append(c['id'])
r={'schema':'rh-independent-mathematical-review/1','version':'0.37','date':'2026-11-22','component':'adelic_sobolev',
 'reviewer':'/root','author':'/root/audit_literature','status':'PASS','source_commit':pin,
 'proof_file':'adelic_sobolev/main.tex','proof_file_sha256':sha(raw),
 'provenance_file_sha256':sha((comp/'provenance.json').read_bytes()),'closure_file_sha256':sha((comp/'closure.json').read_bytes()),
 'claims_reviewed':[c['id'] for c in prov['claims']],'claim_reviews':reviews,'open_findings':[],
 'validation':{'pinned_source_files':len(cache),'source_inventory_ranges':refs,'inherited_claims':inherited,'new_lean_build':False},
 'boundary':'Complete original chart, scalar comparison, local Sobolev, rational count and fixed-level pointwise-growth suppliers. The original target FinPair and initial seed bound remain inputs. Only SPR13 enters ASB14; the joint proof DAG is acyclic.'}
(out/'adelic_sobolev_review.json').write_text(json.dumps(r,ensure_ascii=False,indent=2)+'\n')
(out/'adelic_sobolev_review.txt').write_text('INDEPENDENT MATHEMATICAL REVIEW — ASB1–14\nReviewer: /root\nResult: PASS\n\n'+r['boundary']+'\n\n'+'\n\n'.join(c['id']+': '+c['review'] for c in reviews)+'\n\nProof SHA256: '+r['proof_file_sha256']+'\nProvenance SHA256: '+r['provenance_file_sha256']+'\nClosure SHA256: '+r['closure_file_sha256']+'\n')
print(json.dumps({'status':'PASS','claims':14,'files':len(cache),'ranges':refs},indent=2))
