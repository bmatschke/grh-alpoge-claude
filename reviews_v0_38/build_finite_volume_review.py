#!/usr/bin/env python3
"""Bind root's completed independent mathematical review of FV1–FV11.
These checks certify exact reviewed bytes and source provenance, not a machine proof.
"""
from pathlib import Path
import argparse,hashlib,json,subprocess
HERE=Path(__file__).resolve().parent
p=argparse.ArgumentParser(description=__doc__)
p.add_argument('--component',type=Path,default=HERE.parent/'finite_volume')
p.add_argument('--source',type=Path,default=HERE.parents[1]/'lean_source')
p.add_argument('--human-root',type=Path,default=HERE.parents[1]/'reconstruction_v037')
a=p.parse_args();COMP=a.component.resolve();SOURCE=a.source.resolve();HUMAN=a.human_root.resolve()
PIN='7cbf7a0c32fca1badf05931879a37c3f8a2b03b4'
EXPECTED='70df593f51261aaeb50396a02b9ca128f714e3d676d5e8150fb2ea646a8353ae'
sha=lambda b:hashlib.sha256(b).hexdigest()
main=(COMP/'main.tex').read_bytes();pb=(COMP/'provenance.json').read_bytes();cb=(COMP/'closure.json').read_bytes()
prov=json.loads(pb);closure=json.loads(cb)
assert sha(main)==EXPECTED,'Review the changed mathematics before updating this binding.'
assert prov['main_tex_sha256']==closure['main_tex_sha256']==sha(main)
assert closure['provenance_sha256']==sha(pb)
assert prov['source_commit']==closure['source_commit']==PIN
assert subprocess.check_output(['git','rev-parse','HEAD'],cwd=SOURCE,text=True).strip()==PIN
claims=prov['claims'];assert [c['id'] for c in claims]==[f'FV{i}' for i in range(1,12)]
for c in claims:
 q=c['proof_location'];r=b''.join(main.splitlines(keepends=True)[q['line_start']-1:q['line_end']])
 assert sha(r)==q['sha256'] and len(r)==q['bytes']
 assert r.splitlines()[0]==('% BEGIN '+c['id']).encode()
 assert r.splitlines()[-1]==('% END '+c['id']).encode()
files={};ranges={}
for s in prov['source_inventory']:
 path=s['path']
 if path not in files:
  b=(SOURCE/path).read_bytes();assert b==subprocess.check_output(['git','show',PIN+':'+path],cwd=SOURCE);files[path]=b
 b=files[path];assert sha(b)==s['file_sha256']==s['sha256']
 r=b''.join(b.splitlines(keepends=True)[s['line_start']-1:s['line_end']])
 assert sha(r)==s['range_sha256'] and len(r)==s['range_bytes'];ranges[s['id']]=s
for c in claims:
 assert c['source_ids']==[s['id'] for s in c['sources']]
 for s in c['sources']:assert s==ranges[s['id']]
inherited=[];incoming=set()
for d in prov['baseline_dependencies']:
 b=(HUMAN/d['file']).read_bytes();assert sha(b)==d['file_sha256']==d['sha256']
 for q in d['claims']:
  r=b''.join(b.splitlines(keepends=True)[q['line_start']-1:q['line_end']])
  assert sha(r)==q['sha256'] and len(r)==q['bytes'];incoming.add(q['id'])
 inherited.append({'file':d['file'],'sha256':sha(b),'claims':[q['id'] for q in d['claims']]})
graph={c['id']:c['depends_on'] for c in claims};active=set();done=set()
def visit(cid):
 if cid in incoming:return
 assert cid in graph and cid not in active,cid
 if cid in done:return
 active.add(cid)
 for x in graph[cid]:visit(x)
 active.remove(cid);done.add(cid)
for x in graph:visit(x)
pub=(COMP/'published_applications.json').read_bytes()
assert prov['published_applications']['sha256']==sha(pub)
assert all(not d.startswith('SBD') for c in claims for d in c['depends_on'])
notes={
 1:'Exact functor of points, fixed field, rank-zero case, polynomial inverse and closed faithful F-matrix representation are checked. No determinant condition or source tensor algebra is changed.',
 2:'E-tensor splitting and the J-transpose relation give geometric GL_n. The independent Jordan/transposed-Jordan trace argument rules out a nontrivial normal unipotent subgroup in characteristic zero.',
 3:'All geometric characters are determinant powers by diagonal/elementary generators; the CM descent involution negates the exponent. This proves the exact F-rational character condition, without conflating it with continuous characters.',
 4:'Finite-free module topology matches matrix coordinates; the inverse formula identifies both source matrix and inverse topology. Actual integral restricted-product conditions agree outside finitely many places. Rational subgroup, product decomposition, countability, discreteness and closedness are proved.',
 5:'Borel Lemma5.5 and Theorem5.6(i) were independently reopened in the primary text and matched to the exact F-group, identity component, rational characters, adeles and principal subgroup. Inversion correctly changes the quotient orientation and preserves finite invariant measure.',
 6:'Countable right-translated slices are each injective on left rational orbits; least-index selection gives an exact Borel section, not just an almost-everywhere chosen quotient representative.',
 7:'Orbit-sum lifting gives locally finite nonzero right Haar measure; compact intersection counting and Haar uniqueness identify its scale with any supplied measure. Exact-domain partition plus Tonelli proves equality for every original AE fundamental domain, including null-measurable ones.',
 8:'Full FiniteVolume₂ universal data/hypotheses are retained, including arbitrary Haar/FD. Original CM data and Gram nondegeneracy are explicitly matched. All four FinPair fields and positive volume are supplied on the literal target.',
 9:'Borel5.1 is separately matched; inversion and real-factor removal give the finite cover for standard K0. Compact finite-index refinement gives every original open finite K without requiring K compact or changing the left rational matrices.',
 10:'The rational restriction-of-scalars representation identifies the actual integral lattice subgroup. Compact-open intersections give arithmetic Gamma_s; discreteness uses compact finite slices. Actual real factors and compact scalar-circle center are checked, as are the orientation of phi_s and the full adelic factorization.',
 11:'Universal target finite pairs can be chosen once per i before t,x and all functions. Literal nuQ and downstream regular/representative measures are unchanged. The separate initial seed bound and common geometric data are not supplied by this chapter.'
}
record={'schema':'rh-independent-component-review/1','version':'0.38','component':'finite_volume','reviewer':'/root',
 'status':'PASS','source_commit':PIN,'claims_reviewed':[c['id'] for c in claims],
 'proof_file_sha256':sha(main),'provenance_file_sha256':sha(pb),'closure_file_sha256':sha(cb),
 'published_applications_file_sha256':sha(pub),'all_required_corrections_resolved':True,
 'per_claim_reviews':[{'claim':c['id'],'status':'PASS','proof_sha256':c['proof_location']['sha256'],'source_ids_reviewed':c['source_ids'],'assessment':notes[i]} for i,c in enumerate(claims,1)],
 'source_validation':{'pinned_files_verified':len(files),'distinct_ranges_verified':len(ranges),
 'claim_source_occurrences_verified':sum(len(c['sources']) for c in claims),'proof_blocks_verified':len(claims),
 'inherited_files_verified':len(inherited),'inherited_claim_blocks_verified':sum(len(d['claims']) for d in inherited),
 'all_files_equal_pinned_git_blobs':True,'all_proof_and_range_hashes_exact':True},
 'inherited_bindings':inherited,'dependency_graph':{'acyclic':True,'no_SBD_input_to_FV':True},
 'publication_review':'Primary Borel1963 Numdam PDF independently opened; Lemma5.5,Theorem5.6(i),Theorem5.1 and quotient/double-coset orientations checked.',
 'required_fixes':[],'unresolved_issues':[],'open_findings':[],
 'scope':'Independent human mathematical review plus exact source/proof binding. No Lean replay and no claim to reprove Borel reduction theory.'}
(HERE/'finite_volume_review.json').write_text(json.dumps(record,ensure_ascii=False,indent=2)+'\n')
(HERE/'finite_volume_review.txt').write_text('Independent mathematical review: FV1–FV11\nReviewer: /root\nVerdict: PASS\n\n'+
 '\n\n'.join(f'FV{i}: PASS. {notes[i]}' for i in notes)+
 f'\n\nExact bindings: {len(files)} pinned files; {len(ranges)} ranges; {sum(len(c["sources"]) for c in claims)} claim-source occurrences.\n'+
 f'Main SHA256: {sha(main)}\nProvenance SHA256: {sha(pb)}\nClosure SHA256: {sha(cb)}\n'+
 'No required corrections or unresolved findings. No Lean replay.\n')
print(json.dumps({'status':'PASS','claims':len(claims),'files':len(files),'ranges':len(ranges),
 'review_sha256':sha((HERE/'finite_volume_review.json').read_bytes())},indent=2))
