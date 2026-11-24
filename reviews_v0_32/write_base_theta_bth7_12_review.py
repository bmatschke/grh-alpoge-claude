#!/usr/bin/env python3
"""Bind the root's completed BTH7–BTH12 mathematical review to final bytes."""
from pathlib import Path
import hashlib,json,subprocess
ROOT=Path(__file__).resolve().parents[2]
COMP=ROOT/'work_v032/base_theta'
REPO=ROOT/'lean_source'
PIN='7cbf7a0c32fca1badf05931879a37c3f8a2b03b4'
def digest(b):return hashlib.sha256(b).hexdigest()
def sha(p):return digest(p.read_bytes())
data=json.loads((COMP/'provenance.json').read_text())
ids=['BTH'+str(i) for i in range(7,13)]
claims={c['id']:c for c in data['claims']}
raw=(COMP/'main.tex').read_bytes().splitlines(keepends=True)
source_cache={};ranges=set();entries=0;proofs=[]
for ident in ids:
 c=claims[ident];p=c['proof_location']
 assert digest(b''.join(raw[p['line_start']-1:p['line_end']]))==p['sha256'],ident
 proofs.append(dict(claim=ident,proof_location=p))
 for s in c['sources']:
  path=s['path']
  if path not in source_cache:
   b=(REPO/path).read_bytes()
   assert b==subprocess.check_output(['git','-C',str(REPO),'show',PIN+':'+path]),path
   source_cache[path]=b
  b=source_cache[path]
  assert digest(b)==s.get('sha256',s.get('file_sha256')),path
  a,z=s['line_start'],s['line_end']
  assert digest(b''.join(b.splitlines(keepends=True)[a-1:z]))==s['range_sha256'],(path,a,z)
  ranges.add((path,a,z));entries+=1
checks=[
 ('BTH7','The explicit witness lift(U_i z), literal mtRead and mjRead equalities, injective extV/model maps, full finite-level membership, and original LiftTie.theta establish the Hilbert identity without assuming the desired base square. The actual geometric reading remains an explicit same-Bundle input.'),
 ('BTH8','An original K-basis is a complex basis after realization because its embedded Gram matrix is nonsingular and its image spans. Separating simultaneous tests give a K-defined theta kernel; the original Hermitian form and conjugation-compatible embedding give the rational adjoint image. The target test condition is reserved for BTH11; test existence is not inferred from dimension.'),
 ('BTH9','The invariant orthogonal complement gives P_Z commuting with the full finite action. Idempotence, rationality and Z-invariance suffice for Z intersect image(e)=eZ and its rational span even when e is not self-adjoint. The constructed u has Theta(u)=Theta(jf); its orthogonality and adjoint-image membership force its squared norm to vanish.'),
 ('BTH10','The original level uses psi_0 inverse; p_psi fixes precisely the supplied level forms. The good-cut range is the actual rational adjoint preimage intersect image(C p_psi). The source pairing is |P| times the normalized lH pairing, not its reciprocal. Original phase-one and twisted model identities transfer the kernel conclusion back to thG.'),
 ('BTH11','The stored ThDef3 basis and positive Mj norm factor make w0 injective. BTH7 places theta of each good-cut basis vector in its image, so no additional PLevW, LUnif or H5 producer is needed for containment. The same tests give a full-column-rank matrix over the fixed embedded field; a nonzero maximal minor proves rational coordinates, including zero dimension. Literal relMat/kMat definitions identify the stored matrix.'),
 ('BTH12','The exact normalized projection splits x into E Pi x plus an orthogonal remainder. BTH10 kills the remainder; BTH7 and BTH11 identify the two sides through the injective original target reading. Readings, extensions, simultaneous tests and RowsHold0_3 remain coupled on one Bundle. The family threshold is joined before i and vectors; weaker Closed epsilon/K hypotheses are preserved.')]
result=dict(schema='rh-human-proof-review/1',artifact_version='0.32',component='base_theta',reviewer='/root',
 verdict='PASS — independent BTH7–BTH12 mathematical and source-scope review',
 proof_file_sha256=sha(COMP/'main.tex'),provenance_file_sha256=sha(COMP/'provenance.json'),closure_file_sha256=sha(COMP/'closure.json'),
 claims_reviewed=ids,checks=[dict(claim=c,finding=f) for c,f in checks],required_fixes=[],
 changes_required_and_applied=['Added the nondegenerate Gram-matrix argument for the rational basis under complex realization.','Separated the original discrete-series tensor notation from the stored theta matrix and the good-cut dimension from the Hilbert reading.'],
 evidence=dict(proof_ranges_checked=len(ids),claim_source_entries=entries,distinct_source_ranges=len(ranges),pinned_source_files=len(source_cache),source_commit=PIN,proofs=proofs),
 limitations=['BTH1–BTH6 and BTH13–BTH15 are covered by their separate independent reviews.','The actual common reading, smooth cuspidal extension, simultaneous rational tests and base rows remain producer inputs.','The formal Lean proof is accepted; this is not a Lean build or kernel replay.'])
dest=Path(__file__).resolve().parent
(dest/'base_theta_bth7_12_review.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
(dest/'base_theta_bth7_12_review.txt').write_text('BTH7–BTH12 INDEPENDENT REVIEW — PASS\n\nProof SHA256: '+result['proof_file_sha256']+'\nProvenance SHA256: '+result['provenance_file_sha256']+'\nClosure SHA256: '+result['closure_file_sha256']+'\n\n'+'\n\n'.join(c+' — '+f for c,f in checks)+'\n\nNo required corrections remain. The original common producer is not asserted to exist. No Lean replay was performed.\n')
print(json.dumps({k:result[k] for k in ['verdict','proof_file_sha256','claims_reviewed']}))
