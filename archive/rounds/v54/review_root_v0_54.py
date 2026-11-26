#!/usr/bin/env python3
"""Record the coordinator's completed independent AOS mathematical reading."""
from pathlib import Path
import hashlib, json, subprocess

ROOT = Path(__file__).resolve().parent
REPO = Path('/workspace/scratch/249d32c24541/formal_source')
PIN = '7cbf7a0c32fca1badf05931879a37c3f8a2b03b4'
HERE = ROOT / 'archimedean_orbital_scalar_v54'
EXPECTED = '9b2ff7d9a81e7a29ee059086aa53bd6b1c69f5767a79d9d19e1ecd3374a06b40'

def sha(b):
    return hashlib.sha256(b).hexdigest()

notes = [
    'The literal BR trace pairing becomes twice the real Hermitian pairing on tuples, while the half-trace in pairHerm removes that factor on Hermitian matrices. Thus the tuple self-dual density is 2^(nad) and the Hermitian density is Frobenius volume. The supplied P and bridge are transported with the pairings; no determinant factor is omitted or counted twice. GMR2 supplies uniqueness for every source witness.',
    'The real determinant of a complex linear map is the squared modulus of its complex determinant. The singular-value computation for Hermitian congruence counts diagonal coordinates once and off-diagonal coordinates twice; the exponent -2a is correct, including zero dimensions.',
    'The orthogonal Lie block has off-diagonal coordinates scaled by sqrt(2). The upper block contributes 2^(-ka)|det B|^(2k); the lower Hermitian/skew-Hermitian block contributes 2^(-a^2). Since |det T|=|det B|^2, their product is 2^(-na)|det T|^k. Inverting this determinant gives the source pushforward factor. Arbitrary orthonormal coordinate spaces and arbitrary complement signs are preserved.',
    'The local square root (1+T^(-1)(Q-T))^(1/2) is T-self-adjoint by its real-coefficient power series, even for indefinite T. Its derivative gives the exact block map. Multiplying the Jacobian by the tuple self-dual density leaves |det T|^k at the base point. GMR5 upgrades fiber identification to every parameter and every permitted witness.',
    'The source lieE real span equals the skew-J-adjoint Lie algebra, and the literal realification is a Frobenius isometry. Cayley coordinates construct the smooth group. Left-translated Frobenius volume is Haar; the exponential derivative is the identity. Its average density on shrinking balls yields the literal ratioAt limit and positive limUnder value for all dimensions and signs. Dimension zero is handled directly.',
    'For U(j) to the last-column sphere, the horizontal Frobenius metric is 2|z|^2+t^2. The quotient volume factor is 2^(j-1), not its inverse. Sphere area 2*pi^j/(j-1)! gives successive compact-group volume (2*pi)^j/(j-1)!, matching the source volU recurrence and zero-dimensional case. muGauge is the comparison Frobenius measure by AOS5.',
    'The stabilizer is the actual U(k) block. In local section-times-stabilizer coordinates the density at (0,h) is g, since conjugation by the Euclidean-unitary block is a Frobenius isometry. Integration gives g*volU(k). Compact fibers and local sections establish properness and Radon pushforward; lifting invariant orbit measures to the group establishes the needed uniqueness.',
    'The same local coordinate gives orbit density g*volU(k) and fiber density |det T|^k, fixing their ratio. For a general positive complement, the conjugating unitary changes the orbit map by right translation. The invariant nondegenerate trace form proves absolute adjoint determinant one and hence unimodularity, so this right translation preserves the prescribed Haar measure.',
    'The original ordered frame has Gram blocks 0, I_r and -T_w; its determinant is (-1)^(r+1)T_w and its signature is (r,r+1). The ambient signature therefore leaves a positive complement of dimension k. This proves compactness of the actual stabilizer under every supplied setting, without inventing an alternate frame or assuming HypX to manufacture it.',
    'Independence over the finite product algebra is equivalent componentwise by the coordinate idempotents. Product submersion charts and finite compact-support covers give the complete fiber-family condition even at singular parameters. GMR5 identifies all original global witnesses pointwise, not only almost everywhere. The product is finite and all relevant measures are sigma finite.',
    'The exact completed bridge intertwines the action and the first original MeasTie fixes the ambient infinity measure. Multiplication over real places gives precisely gaugeU(X.B.I)*volU(k)^d*T_w^(-kd). Every original HypX, character, GaugeDens, symmetry and self-dual/fiber quantifier is retained; a different Hermitian proof changes no underlying matrix.',
    'A compactly supported bump inside the independent locus has a strictly positive finite fiber integral by the local positive density and Radon property. Applying the already established PushInf to that bump supplies the literal ConstTest equality. This order is noncircular and its existential PushHyp witnesses supply exactly the original endpoint antecedents.',
    'Existence is checked in the nested AllSome order: a self-dual tuple measure, a self-dual Hermitian measure for every tuple witness, and a fiber family for every pair. The Gram submersion construction covers the independent locus at all parameters, including singular ones; the original character/compatibility premises are retained.',
    'Compactness makes the supplied stabilizer Haar mass finite and positive. Evaluating the original ambient measure tie on the whole space identifies it with the unchanged X.muH mass. No probability or Frobenius renormalization is substituted for that source measure.',
    'A countable local-section cover yields a Borel section. Tonelli, left Haar invariance on H and right invariance on G prove the formula with the factor eta(H)^(-1). Any other section has exactly the same inner integral by a left change of variable in H. The ambient orbit is measurable and carries the outer measure, so arbitrary off-orbit values do not affect the lower integral.',
    'The actual infinity group is a finite product of the real models through the supplied bridge; it is unimodular. The nondegenerate Gram fiber is the full closed orbit, with local sections from the matrix chart and compact actual stabilizer. AOS15 therefore proves literal WeilInf for every source section and every nonnegative measurable test.',
    'Substituting PushInf into WeilInf and using the unchanged stabilizer mass gives the exact positive scalar K/m_H. ExInf supplies all existence clauses and the substitutions hold for every permitted self-dual pair, fiber family and section. The full AinfClause and AinfValue follow, with no division by zero or infinity.',
    'A compact identity neighborhood supplies the original GinfTest under HypX alone. Apply two integration clauses to its indicator using the same witnesses, section and stabilizer measure. The positive finite ambient mass forces the common inner integral positive and finite, so cancellation gives the literal AprimeInf/AprimeInfS scalar. RealBracket and arithmetic/finite-place volume inputs remain separate.'
]

ledger = json.loads((HERE / 'provenance.json').read_text())
manifest = json.loads((HERE / 'source_manifest.json').read_text())
proof = (HERE / 'main.tex').read_bytes()
assert sha(proof) == ledger['proof_file_sha256'] == EXPECTED
assert len(notes) == len(ledger['claims']) == 18
blobs, files = {}, []
for f in manifest.get('files', manifest.get('source_files', [])):
    path = f['path']
    b = (REPO / path).read_bytes()
    assert b == subprocess.check_output(['git', '-C', str(REPO), 'show', PIN + ':' + path])
    assert sha(b) == f.get('sha256', f.get('file_sha256'))
    snap = f.get('snapshot_file', f.get('snapshot_path'))
    if snap:
        assert (ROOT / snap).read_bytes() == b
    blobs[path] = b
    files.append({'path': path, 'sha256': sha(b), 'verified_equal_to_pinned_git_blob': True})
blocks, ranges = [], {}
for i, c in enumerate(ledger['claims']):
    assert c['id'] == 'AOS' + str(i + 1)
    pl = c['proof_location']
    b = b''.join((ROOT / pl['file']).read_bytes().splitlines(keepends=True)[pl['line_start'] - 1:pl['line_end']])
    assert sha(b) == pl['sha256']
    blocks.append({'id': c['id'], 'block_sha256': sha(b), 'status': 'PASS', 'review_note': notes[i]})
    for s in c['sources']:
        raw = blobs[s['path']]
        assert sha(raw) == s.get('file_sha256', s.get('full_file_sha256', s.get('sha256')))
        b = b''.join(raw.splitlines(keepends=True)[s['line_start'] - 1:s['line_end']])
        assert sha(b) == s['range_sha256']
        ranges[(s['path'], s['line_start'], s['line_end'])] = {
            'path': s['path'], 'line_start': s['line_start'], 'line_end': s['line_end'], 'range_sha256': sha(b)}

review = {
    'schema': 'rh-independent-mathematical-review/1', 'artifact_version': '0.54',
    'component': HERE.name, 'reviewer': 'root', 'author': 'bessel_nonvanishing',
    'source_commit': PIN, 'status': 'PASS', 'proof_file_sha256': sha(proof),
    'claims_reviewed': blocks, 'unresolved_findings': [],
    'scope': 'Independent mathematical reading of every new proof and the original consumer scopes; exact source/proof bytes separately checked. This is not formal verification or a Lean replay.',
    'source_files_verified': files, 'source_ranges_verified': list(ranges.values()),
    'review_refinements_in_final_text': [], 'whole_selected_obligation_closed': False}
(HERE / 'independent_review.json').write_text(json.dumps(review, ensure_ascii=False, indent=2) + '\n')
md = [
    '# Independent mathematical review: the exact archimedean orbital scalar', '',
    'Reviewer: root. Author: bessel_nonvanishing.', '',
    '**Status: PASS at the explicitly stated original scopes.**', '',
    'Every numbered proof and its relevant original contract was read independently. The final proof file, every proof block and the pinned source ranges are bound below. This is a mathematical review, not a formal verification.', '',
    'Proof SHA-256: ' + sha(proof),
    f'Primary pinned source files: {len(files)}; distinct cited ranges: {len(ranges)}.', '']
for block in blocks:
    md += ['## ' + block['id'], '', block['review_note'], '']
md += ['## Boundary', '',
       'No unresolved findings remain in the reviewed text. No whole selected RH/GRH obligation is closed by this component. RealBracket, finite-place and arithmetic quotient-volume comparisons, Forms0 and all-family transport/counting/spectral producers remain explicitly separate.', '']
(HERE / 'independent_review.md').write_text('\n'.join(md))
print(json.dumps({'status': 'PASS', 'claims': len(blocks), 'files': len(files),
                  'ranges': len(ranges), 'main_sha256': sha(proof)}))
