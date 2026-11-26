#!/usr/bin/env python3
"""Bind the independent QX4--QX10 mathematical review to frozen bytes."""
from pathlib import Path
import hashlib
import json
import subprocess

ROOT = Path(__file__).resolve().parents[1]
REPO = ROOT.parent / 'lean-source'
DIR = ROOT / 'symplectic_modular_support'
OUT = ROOT / 'reviews_v0_29'
PIN = '7cbf7a0c32fca1badf05931879a37c3f8a2b03b4'
EXPECTED = {
    'main.tex': '9e17c111d638dcd11242d421fe241ee3c0a976c34d1fb42088253aa952b3c5f8',
    'provenance.json': '4b4e1e563295dfd88b0e8ea942d29a47db6c7f36c535ecf619e90ac5b9cd8079',
    'closure.json': '98d07975562286229ece469e77a5fda710fd7032f965d239c64573fbb4327eda'}


def sha(b):
    return hashlib.sha256(b).hexdigest()


for f, h in EXPECTED.items():
    assert sha((DIR / f).read_bytes()) == h, f
p = json.loads((DIR / 'provenance.json').read_text())
claims = [c for c in p['claims'] if c['id'] in {f'QX{i}' for i in range(4, 11)}]
assert len(claims) == 7
blobs, anchors, proofs = {}, {}, []
source_links = 0
for c in claims:
    loc = c['proof_location']
    b = (ROOT / loc['file']).read_bytes()
    fragment = b''.join(b.splitlines(keepends=True)[loc['line_start']-1:loc['line_end']])
    assert sha(fragment) == loc['sha256'], c['id']
    proofs.append({'id': c['id'], 'proof_location': loc})
    for a in c['sources']:
        source_links += 1
        path = a['path']
        if path not in blobs:
            b = (REPO / path).read_bytes()
            assert b == subprocess.check_output(['git', '-C', str(REPO), 'show', PIN + ':' + path]), path
            blobs[path] = b
        b = blobs[path]
        fragment = b''.join(b.splitlines(keepends=True)[a['line_start']-1:a['line_end']])
        assert sha(b) == a['sha256'], path
        assert sha(fragment) == a['range_sha256'], (path, a['line_start'])
        assert PIN in a['url']
        anchors[(path, a['line_start'], a['line_end'])] = a

checks = {
 'QX4': [
  'Checked the ray-class construction of kappa0, the square-root cyclotomic gamma, the one-sided Z_ell character mu, beta and kappa; the conjugation, parity and local weight equations agree on the actual tower.',
  'The coefficient threshold includes all finite values and embeddings before every later ring and Space. The two distinct auxiliary degree-one places are chosen with compatible finite Frobenius conditions and finite exclusions.',
  'The use of Fit.g2 is for every integral root weight. It supplies the actual separating Frobenius/cyclotomic condition and does not silently replace the original residual character quotient.'
 ],
 'QX5': [
  'The actual IsPhi identities preserve every polynomial-law coefficient and all nonnegative exponents. Integral determinant descent does not divide by 4!, so ell=3 is included.',
  'The closed kernel is taken for the determinant in the separated universal ring; no unjustified closedness of an arbitrary adic matrix kernel is used.',
  'The weak Pair, ordinary and inertia relations are verified for the actual maps. Prime-to-ell torsion with characteristic polynomial reducing to (T-1)^4 is killed by a unit resultant. This supplies KX8 nonemptiness in its exact use.'
 ],
 'QX6': [
  'Twist invariance is an equality of integral ideals in the same B. Finite group algebras and all finite characters separate every coefficient before reduction modulo powers of the maximal ideal.',
  'Inverse twist and Krull separation give equality. The proof does not assume that finite-order characters pointwise approximate an arbitrary infinite-order twist.'
 ],
 'QX7': [
  'The seed weight parity and gaps give integral ordered exponents after the correcting twist. The central character and all local ordered flags remain those of the given seed.',
  'The algebraic rank-one character is matched through local class field theory. The Hecke twist preserves actual cuspidality and the CSD condition, and the source AllWin/PotUnl conditions are checked with the strict weight gaps.',
  'Continuity is established by a finite Burnside trace basis and the actual arithmetic-point continuity input. The given pt field, QX3 support implication and QX6 ideal equality return the original seed to the original ideal.'
 ],
 'QX8': [
  'Checked every NiceI clause: full-image irreducibility, index-two/cyclotomic restrictions, local character ratios and the exact open-coset quantifiers.',
  'The corrected proof uses H-degree-zero normal in the Zariski closure of Gamma0. A finite-index commuting subgroup gives a commutative connected component; regular eigenlines and the Fit.ord exclusion rule out the monomial alternative. It does not assume a finite-index normal core of an infinite-index subgroup.',
  'The generic regular-coset argument covers the 1+1+1+1 and 2+2 block patterns. Newton polygon edges and the block-swap polynomial give separability in every odd characteristic, including ell=3. The prescribed open coset is preserved by compatible powers.',
  'The auxiliary-place adjoint cyclotomic invariant vanishes from the actual residual characteristic polynomial and the nontrivial residual cyclotomic value.'
 ],
 'QX9': [
  'The end1 arithmetic decomposition gives actual continuous semisimple representations. Residual distinct characters and Fit.g2 force every string multiplicity to equal one. The inherited strict Frobenius-root ratio gives the exact PureW condition on the original representation.',
  'The end2 cusp is twisted on the exact coefficient field. Cyclic descent and HLTT resolve the finite-character ambiguity; auxiliary quadratic extensions are chosen to rule out self-twists and preserve cuspidality. The resulting attachments use the original fixed iota for every imaginary quadratic field.',
  'The corrected Hecke infinity-sign choice may multiply by eta_K. Its norm pullback and its G_K avatar remain unchanged; no corrected global-avatar equality or incorrect infinity-sign identification is asserted.',
  'Independently checked Caraiani 2012 Theorems1.1-1.2 and Caraiani 2014 Theorem1.1: CM, CSD, cohomological cusps of every rank n>=2, tempered at every finite place, with no Shin-regularity condition. The added Clozel Lemma3.14 paragraph explicitly matches the actual regular algebraic cuspidal hypothesis to cohomological, using the previously matched CX classical input.',
  'Independently checked HLTT TheoremA and the general semisimplified statement of local-global compatibility for l=p II TheoremA. The proof does not claim the stronger Shin-regular upgrade for a general descended polarized cusp.',
  'Original finite inertia, unramifiedness, ordered flags and finite-character Frobenius norms are transported back to the actual decomposition groups. Weak monodromy compatibility and the exact Unl1 ratio exclusion imply N=0; essential temperedness then gives all positive-power exclusions and the literal all-place window witness.'
 ],
 'QX10': [
  'Both pulled-back ideals live on the same original Space and use one coefficient threshold before the later coefficient ring and universal objects.',
  'The exact retained package is rank-four HidaPropsAlt plus P1core on those very same ideals. The fin clause uses the actual finite weight module and IX9; p1 uses QX8; seed uses QX7 for both summands; purity and automorphy use QX9.',
  'The full five-clause PMExAlt implication is written. The arithmetic ideal/support producer remains unproved here, and P3core, all-rank ModUAlt/HidaUAlt and the whole H-prime package are not silently promoted.'
 ]}
review = {
 'schema': 'rh-independent-mathematical-review/1', 'artifact_version': '0.29', 'date': '2026-11-22',
 'reviewer_role': 'Independent dependency_audit cross-review; not the QX component author',
 'component': 'symplectic_modular_support', 'reviewed_claim_ids': [c['id'] for c in claims],
 'result': 'PASS', 'review_kind': 'Full mathematical and exact-interface review of QX4--QX10; QX1--QX3 are incoming independently reviewed suppliers',
 'reviewed_main_sha256': EXPECTED['main.tex'], 'reviewed_provenance_sha256': EXPECTED['provenance.json'],
 'reviewed_closure_sha256': EXPECTED['closure.json'], 'pinned_lean_commit': PIN,
 'claims': [{'id': c['id'], 'result': 'PASS', 'reviewed_proof_location': c['proof_location'],
             'substantive_checks': checks[c['id']]} for c in claims],
 'resolved_findings': [
  {'id': 'QX8-NORMAL-01', 'status': 'resolved before freeze',
   'finding': 'An open finite-index subgroup of Gamma-prime need not have finite-index normal core in Gamma0.',
   'resolution': 'The proof now uses the connected Zariski component H-degree-zero, normal in Zcl(Gamma0), and its finite-index preimage in Gamma-prime.'},
  {'id': 'QX9-SIGN-01', 'status': 'resolved before freeze',
   'finding': 'The Hecke infinity sign does not follow by equating it to the uncorrected cyclotomic avatar at complex conjugation.',
   'resolution': 'The proof explicitly corrects by the quadratic Hecke character eta_K as needed, preserving only the required restriction to G_K and norm pullback.'}
 ],
 'primary_sources_independently_opened': [
  {'url': 'https://www.ma.imperial.ac.uk/~acaraian/papers/lgc1.pdf', 'locator': 'Theorems1.1-1.2, printed page2312', 'checked_scope': 'All finite places, CM CSD cohomological cusp, n>=2, no Shin regularity'},
  {'url': 'https://www.ma.imperial.ac.uk/~acaraian/papers/lgc2.pdf', 'locator': 'Theorem1.1', 'checked_scope': 'Full Frobenius-semisimplified l=p compatibility for the CSD cohomological cusp'},
  {'url': 'https://virtualmath1.stanford.edu/~rltaylor/lg2.pdf', 'locator': 'TheoremA', 'checked_scope': 'General semisimplified l=p compatibility; stronger Frobenius-semisimplification is not used without its hypotheses'},
  {'url': 'https://virtualmath1.stanford.edu/~rltaylor/rigcoh.pdf', 'locator': 'TheoremA and Corollary7.14', 'checked_scope': 'Continuous semisimple attachment to a regular algebraic cusp without requiring polarization'}
 ],
 'previous_primary_match_reused': ['Clozel Lemma3.14 via CX-CL; exact added cohomological-matching paragraph inspected', 'Cyclic base change/descent as the explicitly registered QX-AC classical leaf'],
 'unresolved_findings': [],
 'source_validation': {'selected_claim_source_links': source_links, 'unique_source_ranges': len(anchors),
                       'pinned_source_files': len(blobs), 'human_proof_ranges': len(proofs),
                       'all_match': True},
 'limits': 'Mathematical cross-review and pinned-source integrity checks; no Lean build or kernel replay. The retained actual Hecke/support producer is not supplied by this review.'}
validation = {'schema': 'rh-independent-selected-source-validation/1', 'artifact_version': '0.29',
 'component': 'symplectic_modular_support', 'source_commit': PIN, 'result': 'PASS',
 'reviewed_main_sha256': EXPECTED['main.tex'], 'reviewed_provenance_sha256': EXPECTED['provenance.json'],
 'reviewed_claim_ids': [c['id'] for c in claims], 'proofs': proofs,
 'source_links': source_links, 'unique_ranges': len(anchors), 'source_files': len(blobs),
 'all_full_files_equal_pinned_git_blobs': True, 'all_range_and_proof_hashes_match': True,
 'sources': sorted(anchors.values(), key=lambda a: (a['path'], a['line_start'], a['line_end']))}
for name, value in [('modular_support_audit_review.json', review), ('modular_support_audit_source_validation.json', validation)]:
    (OUT / name).write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n')
lines = ['Independent mathematical review: QX4--QX10', '', 'Result: PASS', '',
         'Main SHA256: ' + EXPECTED['main.tex'], 'Provenance SHA256: ' + EXPECTED['provenance.json'],
         'Closure SHA256: ' + EXPECTED['closure.json'], '',
         'Scope: exact arithmetic Links, IsPhi, integral twist/support transport, seed membership, NiceI, all-place purity/automorphy and the complete five-clause PMExAlt join. QX1--QX3 remain incoming independently reviewed suppliers.', '']
for cid, items in checks.items():
    lines += [cid, ''] + ['- ' + s for s in items] + ['']
lines += ['Resolved findings: QX8-NORMAL-01 and QX9-SIGN-01, both corrected before the frozen proof. No unresolved finding.', '',
          f'Independent integrity checks: {source_links} selected claim-source links, {len(anchors)} unique ranges, {len(blobs)} pinned files and {len(proofs)} human proof ranges all match.', '',
          'This is a human mathematical and source-interface review. It does not prove the retained actual rank-four Hecke ideal/P1core producer, and it is not a Lean build or kernel replay.']
(OUT / 'modular_support_audit_review.txt').write_text('\n'.join(lines) + '\n')
print(json.dumps({'result': 'PASS', 'links': source_links, 'ranges': len(anchors), 'files': len(blobs), 'proofs': len(proofs),
                  'review_sha256': sha((OUT / 'modular_support_audit_review.json').read_bytes())}, indent=2))
