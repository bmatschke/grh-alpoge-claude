#!/usr/bin/env python3
"""Bind root's completed independent mathematical readings to exact files."""
from pathlib import Path
import hashlib, json, subprocess

ROOT=Path(__file__).resolve().parent
REPO=Path('/workspace/scratch/249d32c24541/formal_source')
PIN='7cbf7a0c32fca1badf05931879a37c3f8a2b03b4'
def sha(b): return hashlib.sha256(b).hexdigest()

NFL=[
 'Odd finite quadratic form and exact Gauss square, including negative determinant and dimension zero; pairing nondegeneracy and congruence sign checked.',
 'Poisson and finite-coset calculation retains exact squared multiplier, characteristic shifts and determinant; no unspecified theta multiplier input.',
 'Rigidified entire-unit ratio, half-characteristic parity and determinant square; no division by a theta value at zero.',
 'Whole original lattice level and mod-eight adapted blocks; determinant equals one by integral congruence and all complex absolute values, with exact original modulus.',
 'Swapped-transposed block convention and h-prime H0 equals J inverse-transpose h; H0 invertibility follows from full period lattices.',
 'Actual rigidified line frames and exact section-scalar equation; only square of pointwise root used.',
 'Literal SecBC equality and dual-number tangent derivative under level-preserving isometry, retaining section twist law.',
 'Early reversed column and late inverse block give precise Borel weight; section exponent even and no conjugation/sign loss.',
 'One actual triangular frame-change witness before every allowed weight and rule.',
 'Actual arithmetic lattice action, identity linear change and squared section ratio one; frame witness independent of weights.',
 'Full arbitrary-target EvalWD including nilpotents via reduced universal frame charts and localization; reduced-target weight law retains FromTest.',
 'One local finite-type test chart and actual holomorphic evaluation homomorphisms before moving the point or natural rule.',
 'Arbitrary coefficient ring handled by finitely many chart coefficients and nonvanishing denominators; derivative matrix recovered from actual exponential and dual numbers.',
 'Local nonzero evaluation of actual algebraic section gives holomorphic scalar ratio; finite chart proof avoids analytifying arbitrary Spec R or assuming theta at zero nonzero.',
 'Full normed-complex-space and arbitrary-subset DifferentiableOn scope; universal frame algebra and inverses prove natural-rule evaluation, without a weight hypothesis.',
 'Actual normalized readings for arbitrary pointwise roots: even n replaces root power by (C det h)^(n/2), so holomorphy needs no continuous root.',
 'All four FramesOK fields on exactly the inherited NFR family with one common choice and every FromTest return; SecBC/SecTwist retained.',
 'Full inverse construction from arbitrary IsPeriod; first-linear Hermitian signs, block forms and signed leading minors checked.',
 'Whole CoverTri for arbitrary actual framed point and arbitrary realizing derivatives, using equality of tangent vectors with unit diagonal.',
 'Whole FibTri recovers dependent component equality, actual lattice Gamma and Borel from triangular derivatives; only elementary per_gam calculation is used.',
 'Every literal IsUnf clause, covering and both fiber directions, IsSec transformations, same section, same lattice fundamental domain and exact mean one.',
 'Actual prescribed-space principal and all-cusp return, N=lcm(l.M,l.A), full FromTest and ExpoMatch at l.A=1; supplied Moduli and two global section laws remain explicit.'
]
BSE=[
 'Whole PerEquiv with arbitrary matrix function and source undefined-integral convention; compact conjugation modulus and nilpotent unimodularity preserve the given Haar pair.',
 'Original compact-type dominance yields highest vector; ordered determinant survives only identity permutation, centrality extends scalar to entire compact irreducible, including k=0.',
 'Full FrameLaw on actual generated module with Q=g0^-1 g P^-1; real derivatives, complexified character and exact paired-edge product -T(z) product |c_a|^2 / 4^r checked.',
 'Whole CapelliB and rank-zero WhittakerZero: last-column parameters decrease r times, first-row parameters stay fixed and final middle sign is (-1)^k; no nonzero kappa premise added.',
 'Whole CapelliCov over arbitrary associative complex algebra; two scalar Cauchy-Binet expansions justified by shifted-minor alternation, preserving ordered noncommuting products.',
 'Standard row and dual column are computed from the same Q and actual fixed Bessel vector; rank-zero signs and sqrt(T) factors checked.',
 'Whole EvalP with explicit y=Q^-1 e_j; complement parameter omega-1 gives precisely u_j-lambda_s-1/2, all original free translates and measures retained.',
 'Whole EvalM with explicit row e_d^t Q; complement parameter omega gives precisely u_j-lambda_s+1/2, same actual period and exact rank-zero factor.',
 'Full Step and Bessel return are conditional on both original QuotP/QuotM; Forms0 remains for ConcreteSettingExists and no whole selected global closure is inferred.'
]

for component,author,prefix,notes in [
 ('normalized_frame_laws_v51','geometry_alltest','NFL',NFL),
 ('bessel_period_evaluation_v51','bessel_nonvanishing','BSE',BSE)]:
 p=ROOT/component
 prov=json.loads((p/'provenance.json').read_text())
 manifest=json.loads((p/'source_manifest.json').read_text())
 proof=(p/'main.tex').read_bytes()
 assert sha(proof)==prov['proof_file_sha256']
 assert len(prov['claims'])==len(notes)
 blobs={}; files=[]
 for f in manifest.get('files',manifest.get('source_files',[])):
  path=f['path']; data=(REPO/path).read_bytes()
  blob=subprocess.check_output(['git','show',f'{PIN}:{path}'],cwd=REPO)
  assert data==blob and sha(data)==f.get('sha256',f.get('file_sha256'))
  snapshot=f.get('snapshot_file',f.get('snapshot_path'))
  if snapshot: assert (ROOT/snapshot).read_bytes()==blob
  blobs[path]=data
  files.append({'path':path,'sha256':sha(data),'verified_equal_to_pinned_git_blob':True})
 blocks=[]; ranges={}
 for i,c in enumerate(prov['claims']):
  assert c['id']==f'{prefix}{i+1}'
  q=c['proof_location']; data=b''.join((ROOT/q['file']).read_bytes().splitlines(keepends=True)[q['line_start']-1:q['line_end']])
  assert sha(data)==q['sha256'] and len(data)==q['bytes']
  blocks.append({'id':c['id'],'block_sha256':sha(data),'status':'PASS','review_note':notes[i]})
  for s in c['sources']:
   blob=blobs[s['path']]
   assert sha(blob)==s['file_sha256'] and s['source_commit']==PIN
   data=b''.join(blob.splitlines(keepends=True)[s['line_start']-1:s['line_end']])
   assert sha(data)==s['range_sha256'] and len(data)==s['range_bytes']
   ranges[(s['path'],s['line_start'],s['line_end'])]={'path':s['path'],'line_start':s['line_start'],'line_end':s['line_end'],'range_sha256':sha(data)}
 review={'schema':'rh-independent-mathematical-review/1','artifact_version':'0.51','component':component,
  'reviewer':'root','author':author,'source_commit':PIN,'status':'PASS','proof_file_sha256':sha(proof),
  'claims_reviewed':blocks,'unresolved_findings':[],
  'scope':'Independent reading of every human proof block and original endpoint scopes, with source and proof bytes separately verified. No Lean replay.',
  'source_files_verified':files,'source_ranges_verified':list(ranges.values()),
  'whole_selected_obligation_closed':False}
 (p/'independent_review.json').write_text(json.dumps(review,indent=2)+'\n')
 md=[f'# Independent mathematical review: {component}','','Reviewer: root. Author: '+author+'.','',
  '**Status: PASS.** All claims were read independently against their stated mathematics and original source interfaces. The notes below are the mathematical review; hashes identify the exact files.','',
  'Main proof SHA-256: `'+sha(proof)+'`.','',f'{len(blocks)} proof blocks, {len(files)} pinned source files and {len(ranges)} distinct cited ranges verified.','']
 for c in blocks: md += ['## '+c['id'],'',c['review_note'],'']
 md += ['## Scope boundary','',notes[-1],'','No unresolved review findings. This is an independent expository and mathematical review, not a new formal verification.','']
 (p/'independent_review.md').write_text('\n'.join(md))
 print(json.dumps({'component':component,'status':'PASS','claims':len(blocks),'files':len(files),'ranges':len(ranges),'main_sha256':sha(proof)}))
