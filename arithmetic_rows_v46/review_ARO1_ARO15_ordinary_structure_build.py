#!/usr/bin/env python3
"""Bind the independently read first half of the original arithmetic row packet."""
from pathlib import Path
import hashlib, json, re, subprocess

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
SRC = ROOT.parent / 'formal_source'
PIN = '7cbf7a0c32fca1badf05931879a37c3f8a2b03b4'
sha = lambda b: hashlib.sha256(b).hexdigest()
data = (HERE/'main.tex').read_bytes()
assert sha(data) == '1ed4d31d5fce6de4a7cf2d9b9164722a65a6928e7e88b72950a905301030d873'
text = data.decode()
blocks = {}
for n in range(1,16):
    cid = f'ARO{n}'
    m = re.search(r'^% BEGIN '+cid+r'\n.*?^% END '+cid+r'\n', text, re.M|re.S)
    assert m, cid
    blocks[cid] = sha(m.group().encode())
R = 'src/Formalism/LocalToGlobal/SiegelLatticeTheory/FlagStabilizerTensors/RootLatticeThresholds/'
H = 'src/Formalism/LocalToGlobal/SiegelLatticeTheory/HaarTransversals/'
S = 'src/Formalism/LocalToGlobal/SiegelLatticeTheory/FlagStabilizerTensors/'
specs = [
 (H+'HidaSetting.lean',60,135),
 (H+'HidaSetting.lean',179,265),
 (H+'HidaSetting.lean',340,361),
 (S+'RowDict.lean',42,90),
 (S+'AllRowsOf.lean',18,115),
 (S+'AllRowsOf.lean',660,701),
 (R+'AllRowsKpp.lean',15,135),
 (R+'KppIdx.lean',13,185),
 (R+'KppCharB.lean',15,154),
 (R+'KppLocC.lean',17,176),
 (R+'KppFrameW.lean',245,294),
 (R+'AllRowsRMul.lean',17,94),
 ('src/Formalism/SharpRestriction/LevelLetterCocycles/ArithmeticCylinders.lean',300,341),
 ('src/Formalism/SharpRestriction/CuspSpanNormBounds/GlobAut.lean',120,140),
]
sources = []
for rel,lo,hi in specs:
    b=(SRC/rel).read_bytes()
    assert b==subprocess.check_output(['git','-C',str(SRC),'show',PIN+':'+rel])
    lines=b.splitlines(keepends=True)
    hi=min(hi,len(lines))
    assert lo<=hi
    sources.append({'path':rel,'line_start':lo,'line_end':hi,'file_sha256':sha(b),
       'range_sha256':sha(b''.join(lines[lo-1:hi])),'source_commit':PIN,
       'verified_equal_to_pinned_git_blob':True})
review={
 'schema':'rh-independent-mathematical-review/1','artifact_version':'0.46',
 'reviewer':'/root/ordinary_structure','component':'arithmetic_rows_v46',
 'status':'PASS','result':'PASS','proof_file':'arithmetic_rows_v46/main.tex',
 'proof_file_sha256':sha(data),'proof_sha256':sha(data),'source_commit':PIN,
 'claims_reviewed':list(blocks),'proof_hashes':blocks,'source_ranges_inspected':sources,
 'scope':'Independent mathematical reading of ARO1-ARO15 only, with direct comparison to the literal original reduction, level-character, event and operator contracts. Later ARO16-ARO30 are not covered by this review.',
 'checks':[
  'Reduction uses the original full lattice; the selected and conjugate split primes exhaust the auxiliary-prime factors, and their perfect dual pairing gives the exact kernel on the completed lattice.',
  'Surjectivity is constructed adelically from local GL_n(O_v) lifts and inverse transposes; it does not invoke rational strong approximation.',
  'Every reduction fiber has original Haar volume V. Inflation divides by V, the hat transform multiplies by V, and convolution cancels precisely one such factor.',
  'Both ew orientations use the correct reversed middle/f blocks and the original diagonal sign correction. Direct inverse-matrix flags and CRT prove the full reverse membership implication.',
  'The CRT additive characters use the original rational/infinity character law. Complete splitting makes Tr(epsilon/q_other) mod q nonzero, so the new elementary nontriviality proof preserves the literal character normalization.',
  'The finite character idempotent uses inverse character coefficients, as in the original eDat/eJ. The diagonal character-shift exponents give all phiJ terms the same multiplier, including empty chains.',
  'The full EtOne cylinder identity retains the original e(1), measure and finite normalized type projectors; invalid labels vanish. Positivity is established for the identity coefficients rather than presumed real.',
  'The positive-type convolution identity is valid on the full group. The right regular action satisfies R(ab)=R(a)R(b), giving the displayed convolution order and adjoint convention.',
  'The original weak-integral IsRConvF field is satisfied with norm bound, uniqueness and exact adjoint. Consequently the chosen ReT branch is the actual operator and the entire infinity action commutes with each event projector.',
  'Original SG.HidaSetting and normalized-type data remain supplied; this review neither constructs a common geometric family nor closes an outer selected obligation.'
 ],
 'resolved_findings':[
  {'claim':'ARO8','kind':'literal-domain clarification','finding':'The statement should state x belongs to K, matching rho:K->G and original KppShape.',
   'resolution':'Final reviewed ARO8 now explicitly says for every x in K. No proof or scope enlargement was needed.'}
 ],
 'unresolved_findings':[],'material_corrections_required':[],
 'method':'Written mathematical/source-interface audit. No Lean replay; formal correctness was not substituted for the human argument.'
}
out=HERE/'review_ARO1_ARO15_ordinary_structure.json'
out.write_text(json.dumps(review,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'review':str(out),'sha256':sha(out.read_bytes()),'claims':len(blocks),'source_ranges':len(sources)}))
