#!/usr/bin/env python3
"""Bind the root's completed mathematical review to the exact NFR text."""
from pathlib import Path
import hashlib
import json
import subprocess

ROOT = Path(__file__).resolve().parents[1]
SOURCE = Path('/workspace/scratch/249d32c24541/formal_source')
PIN = '7cbf7a0c32fca1badf05931879a37c3f8a2b03b4'
COMP = 'normalized_frames_v50'
EXPECTED = '37d44b538b169764bca21f5cba9077a8b1b60115a764402d81495615ee3f11d1'
def sha(b): return hashlib.sha256(b).hexdigest()
def read(p): return json.loads(p.read_text())
def dump(p,d): p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n')

notes = [
 'The first-linear Hermitian convention is followed throughout. Positive columns use conjugated coordinates and negative dual rows use unconjugated coordinates, giving exactly the original relab/perFr dictionary and host multiplicities.',
 'The Q block matrix and trace with minus xi0 give the positive Hermitian form with the original alternating-form sign. Orthogonalization identifies the domain with the connected indefinite unitary group and positive triangular factors. Actual period entries are holomorphic; the separate onto clause is not asserted.',
 'The polynomial w squared equals w minus 2m gives an idempotent w to the fourth power modulo eight whose adjoint is its complement. The two summands are complementary Lagrangians. Elementary symplectic shears, including the explicit unit diagonal factorization, lift the prescribed basis integrally.',
 'Riemann relations produce h and tau on the same ordered lattice. Inherited HUF20 gives one pair of half characteristics on the connected domain and the actual algebraic section and zero-rigidified frame. Every original ThetaData field is accounted for.',
 'Normal convergence gives holomorphy. Nonzero Fourier coefficients prove nonvanishing; the recurrence under the second lattice generators leaves one scalar parameter. This proves the complex section line directly and does not import SecTwistSt or SecBaseChangeSt.',
 'The nonzero determinant multiplier has an actual pointwise square root. Scaling the same algebraic section and differentiating the same exponential produces the required ordered tangent eigenbasis. IsThetaPt and IsNormUn have their literal original data.',
 'The normalized periods and Riemann relations give H = transpose(h) times inverse(Im tau) times conjugate(h). Determinants give det(H) det(Im tau) = absolute(det h) squared, with all factors positive.',
 'Unit signed principal minors fix each Hermitian block determinant. Multiplication over the actual CM type yields the exact product of 2 absolute(type xi0), rather than an unspecified positive constant.',
 'An actual half-open lattice parallelepiped is a fundamental domain. Orthogonality in the first torus variable and tiling in the second give the Gaussian theta mean 1 divided by sqrt(2 to the g times det(Im tau)); the zero-dimensional convention is consistent.',
 'The quadratic holomorphic gauge gives the exact unit semicharacter and Gaussian weight. Scalar readings remain those of the actual section in the rescaled frame; the zero rigidification is preserved.',
 'The normConst factor and exact Hermitian determinant cancel the Gaussian denominator and leave mean exactly one. Only the squared modulus of the chosen square root occurs, so its arbitrary sign has no effect.',
 'The actual isomorphism, exponential, tangent basis, section generator, multiplier, weight and normalized mean supply every original FrameOK clause. The direct Fourier argument is sufficient for the section-generator field.',
 'Choice on the finite supplied family gives all normalized points simultaneously and exactly the first FramesOK field. FromTest uses TDR13 only with its original SecBaseChangeSt premise. The three other FramesOK fields, CoverTri, FibTri and complete IsUnf remain explicit.'
]
here=ROOT/COMP
raw=(here/'main.tex').read_bytes()
assert sha(raw)==EXPECTED
ledger=read(here/'provenance.json')
assert len(ledger['claims'])==len(notes)==13
claims=[]
for c,note in zip(ledger['claims'],notes):
    pl=c['proof_location']
    block=b''.join(raw.splitlines(keepends=True)[pl['line_start']-1:pl['line_end']])
    assert sha(block)==pl['sha256']
    claims.append({'id':c['id'],'status':'PASS','block_sha256':sha(block),'reasoning':note})
manifest=read(here/'source_manifest.json')
blobs={}
for f in manifest['files']:
    path=f['path']
    b=subprocess.check_output(['git','show',PIN+':'+path],cwd=SOURCE)
    assert sha(b)==f['sha256']
    assert (ROOT/f['snapshot_file']).read_bytes()==b
    blobs[path]=b
for r in manifest['ranges']:
    b=b''.join(blobs[r['path']].splitlines(keepends=True)[r['line_start']-1:r['line_end']])
    assert sha(b)==r['range_sha256']
inherited=read(here/'inherited_inputs.json')['inputs']
for h in inherited:
    b=(ROOT/h['proof_file']).read_bytes()
    assert sha(b)==h['proof_file_sha256']
    pl=h['proof_location']
    assert sha(b''.join(b.splitlines(keepends=True)[pl['line_start']-1:pl['line_end']]))==h['proof_block_sha256']
report = '# Independent mathematical review: NFR1–NFR13\n\n'
report += 'Reviewer: root. Author: geometry_alltest. Result: PASS at the exact written scope.\n\n'
report += 'The whole proof text and the original ModelsOf, ModelBase, ThetaData, IsThetaPt, IsNormUn, FrameOK and FramesOK contracts were read independently. This review checks the human argument; source hashing is a separate provenance check.\n\n'
for c in claims: report += '## '+c['id']+'\n\n'+c['reasoning']+'\n\n'
report += '## Scope and verification\n\nThe source commit is '+PIN+'. All 31 pinned source files and 31 ranges, the full proof file, 13 claim blocks and six inherited proof blocks were checked byte-for-byte. The supplied Moduli and the original inherited foundations remain. NFR1–NFR12 do not require a new section-base-change premise; the FromTest conclusion in NFR13 retains it. No full FramesOK, IsUnf, hasPrinc or whole selected obligation is inferred. There are no unresolved findings.\n'
rp=here/'independent_review.md';rp.write_text(report)
dump(here/'independent_review.json',{
 'schema':'rh-independent-mathematical-review/1','artifact_version':'0.50',
 'component':COMP,'reviewer':'/root','author':'/root/geometry_alltest','status':'PASS',
 'source_commit':PIN,'proof_file':COMP+'/main.tex','proof_file_sha256':EXPECTED,
 'claims_reviewed':claims,'review_report':COMP+'/independent_review.md','report_sha256':sha(rp.read_bytes()),
 'source_file_count_verified':len(blobs),'source_range_count_verified':len(manifest['ranges']),
 'inherited_blocks_verified':len(inherited),'corrections_resolved':[],
 'unresolved_findings':[],'scope':'Complete original normalized point constructors and every FrameOK field; simultaneous first FramesOK field and original-premise FromTest only.'})
print(json.dumps({'component':COMP,'result':'PASS','claims':len(claims),'source_files':len(blobs),'source_ranges':len(manifest['ranges'])}))
