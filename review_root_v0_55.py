#!/usr/bin/env python3
"""Record the coordinator's completed independent SVW mathematical reading."""
from pathlib import Path
import hashlib, json, subprocess

ROOT = Path(__file__).resolve().parent
REPO = Path('/workspace/scratch/249d32c24541/formal_source')
PIN = '7cbf7a0c32fca1badf05931879a37c3f8a2b03b4'
HERE = ROOT / 'stabilizer_volume_v55'
EXPECTED = '358b9ff25062d7b74218b154105b17dfbcd219ad930a6715318cb6bdb42dfebd'

def sha(b):
    return hashlib.sha256(b).hexdigest()

notes = ['The finite-coordinate restricted-product topology is locally compact and second countable. The rational diagonal is closed discrete by its integral lattice at infinity. The unitary equations define a closed subset with continuous inverse, and the stabilizer is closed; rational matrix subgroups are countable and discrete. Thus the actual Haar measures are Radon and sigma-finite.', 'An admissible pure test is supported in a product with only finitely many exceptional finite factors. That product lies in a clopen restricted-product chart, so extension by zero is continuous and support is compact. Arbitrary compact sets admit larger finite boxes and a smooth infinite cutoff. Compactness plus the rational closed-discrete set gives the full FinTheta scope, and a countable sum gives measurability.', 'Every supplied IsOmT includes actual integrability for every admissible test. Admissible cutoffs therefore prove local finiteness of that supplied measure before Radon uniqueness is used. Compact-open finite boxes times compact infinite tests determine the Borel measure. This proves uniqueness for every IsOmT and closes the universal supplied-measure requirement in ExStab; an existential compatible pair alone would not suffice.', 'A compact Hermitian cutoff supported in the invertible locus puts the tuple test inside the independent locus. The full fiber-family continuity then gives a continuous density near the specified T. Equality of compact-set integrals and positive Haar mass force pointwise equality of continuous complex densities. This preserves every supplied local witness and proves fixed-T equality rather than only an almost-everywhere statement.', 'Compact support implies the literal rapid-decay inequality for every exponent. The smooth compatibility premise is specialized using the same IsOmT self-dual witnesses, character, ambient Haar and domain. Pointwise local density identification and the stated convergent products give SWeqOm without rearranging a product or changing normalization.', 'The nondegenerate rational Gram spans are isometric. The displayed Hermitian rank-one map has denominator d=h(u-v,u), sends u to v and preserves the form because h(u-v,u-v)=d+conjugate(d). If d=0 the u,-v construction has denominator 2t, followed by negation on the current orthogonal complement. The construction fixes earlier lines and remains rational. Right cosets Gamma/Delta count each rational tuple exactly once.', 'The translates U x_j each intersect a left discrete-subgroup orbit at most once because UU^{-1} meets the subgroup only at identity. Selecting the first chart gives a Borel strict domain. No quotient mass assumption enters, so ExFDStab is proved before finite stabilizer mass.', 'Null-measurable source domains have measurable representatives; countability and invariant measure preserve all translated almost-everywhere identities. Inserting the translated indicator sum and using nonnegative Tonelli proves domain independence even at infinite mass. The analogous right-domain statement is legitimate once the measure is right invariant.', 'Local unitary unimodularity follows from the nondegenerate invariant trace pairing; at infinity its real form has determinant of absolute value one. Restricted-product cylinder checks then give a bi-invariant adelic Haar measure, and uniqueness transports to every supplied normalization. The nondegenerate pointwise stabilizer is the rational orthogonal-complement unitary group. Inversion invariance is fixed by a symmetric positive finite compact neighborhood.', 'The right-coset convention is correct: Gamma is the disjoint union of Delta gamma^{-1}, so the union of gamma^{-1}D is a left Delta domain and its inverse a right Delta domain. In each fiber s(y)H the set of h landing in that inverse domain is a right Delta domain. Its mass is the same stabilizer covolume, possibly infinite. Compatibility and nonnegative integrals prove unfolding before any finite-mass conversion.', 'The nonzero complex Bochner theta integral rules out its nonintegrable zero fallback. The nonnegative integral is therefore finite and strictly positive. IsOmT supplies finite integral I of the test; extended unfolding gives 0<L=mass(F_H)*I<infinity. Only then are I>0 and finite stabilizer mass deduced and real values taken. Thus no cancellation of the real value of an infinite measure occurs.', 'One rational scalar clears the finitely many denominators of X0 in a fixed E/F basis. The corresponding tuple lattice is open compact in the finite restricted product and contains X0 at all finite places. A smooth positive compact bump at infinity gives one admissible all-chart-smooth product. Its positivity pulls back to a genuine open identity neighborhood in G.', 'IsOmT gives finite integral. If its nonnegative integral vanished, compatibility applied to the identity-neighborhood indicator would force positive Haar mass of that neighborhood to vanish: every fiber with zero test value contributes zero. This proves positivity for every supplied compatible measure, with the same test used in the density and unfolding equations.', 'Character and IsOmT existence reuse the already proved GMR records. SVW3 identifies an arbitrary supplied IsOmT with the constructed positive Radon orbit measure, so GMR11 supplies a compatible Haar measure for that arbitrary witness. SVW7 gives every stabilizer domain stage. Ambient domains and finite mass use exactly SWa1. The six nested existence/universality stages are preserved.', 'The ambient domain has positive finite mass by SWa1 and countable translates. SWeqOm with the same positive test gives a nonzero theta integral; Unfold then gives finite stabilizer mass. Cancellation is now between positive finite real scalars, and the finite extended masses are equal. Original SWa1 and StabilizerFirstChernCompatibility remain premises, not renamed conclusions.', 'The rational stabilizer subgroups ratOf and ratIn agree by literal inverse-image membership. The chosen covolume domains exist, and the universal VolStabW equality applies to those precise choices. Equality of real values holds even for an arbitrary supplied VolStabW without finite-mass hypotheses; positivity is carefully limited to the stronger SWa1 specialization.', 'The source rank conditions include even m, m>=2, k>=m+3 and n=k+m-1, giving the stated strict size bounds for both tuple lengths. The original frame Gram determinant is (-1)^(r+1)Tw. All three stabilizer covolumes equal the same ambient c on the supplied setting. Substitution gives c*c=c*c, while both original unipotent covolume-one antecedents are preserved in the generic InVolumesAt statement.', 'The actual GMR19 MeasCompat-psi contains the compatible orbit measures for both words and every nondegenerate auxiliary X0, and already contains the unipotent covolume-one equations. The literal inVolumes_of_compat consumer therefore discharges every measure antecedent on that same rescaled setting with one character. Original bridge and infinity measures are unchanged; only the three InVolumes fields are claimed, not the remaining mass-data or spectral package.']

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
    assert c['id'] == 'SVW' + str(i + 1)
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
    'schema': 'rh-independent-mathematical-review/1', 'artifact_version': '0.55',
    'component': HERE.name, 'reviewer': 'root', 'author': 'bessel_nonvanishing',
    'source_commit': PIN, 'status': 'PASS', 'proof_file_sha256': sha(proof),
    'claims_reviewed': blocks, 'unresolved_findings': [],
    'scope': 'Independent mathematical reading of every new proof and the original consumer scopes; exact source/proof bytes separately checked. This is not formal verification or a Lean replay.',
    'source_files_verified': files, 'source_ranges_verified': list(ranges.values()),
    'review_refinements_in_final_text': [], 'whole_selected_obligation_closed': False}
(HERE / 'independent_review.json').write_text(json.dumps(review, ensure_ascii=False, indent=2) + '\n')
md = [
    '# Independent mathematical review: stabilizer volumes from the original smooth Siegel--Weil identity', '',
    'Reviewer: root. Author: bessel_nonvanishing.', '',
    '**Status: PASS at the explicitly stated original scopes.**', '',
    'Every numbered proof and its relevant original contract was read independently. The final proof file, every proof block and the pinned source ranges are bound below. This is a mathematical review, not a formal verification.', '',
    'Proof SHA-256: ' + sha(proof),
    f'Primary pinned source files: {len(files)}; distinct cited ranges: {len(ranges)}.', '']
for block in blocks:
    md += ['## ' + block['id'], '', block['review_note'], '']
md += ['## Boundary', '',
       'No unresolved findings remain in the reviewed text. No whole selected RH/GRH obligation is closed by this component. The original smooth Siegel--Weil premise, RealBracket, finite-place factors, remaining mass/counting fields, Forms0 and all-family transport/counting/spectral producers remain explicitly separate. The actual InVolumes join is complete at its retained premise scope.', '']
(HERE / 'independent_review.md').write_text('\n'.join(md))
print(json.dumps({'status': 'PASS', 'claims': len(blocks), 'files': len(files),
                  'ranges': len(ranges), 'main_sha256': sha(proof)}))
