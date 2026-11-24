#!/usr/bin/env python3
"""Bind all new proof paragraphs to independent reviews and record v0.20 scope.

This is reproducible review-coverage bookkeeping, not a mathematical proof
checker. The separately authored reviews supply the substantive scrutiny.
"""
from pathlib import Path
import hashlib
import json
import re

ROOT = Path(__file__).resolve().parent
REV = ROOT / 'reviews_v0_20'
OLD = ROOT / 'history/version_0_19'
COMPONENTS = {
    'adic_realization': ('GA', 23, '/root/class_rank'),
    'finite_weil_arithmetic': ('WA', 19, '/root/comparison_span'),
    'mass_formula': ('MF', 20, '/root/global_frame'),
    'ray_prime_estimates': ('QR', 25, '/root'),
}


def read(path):
    return json.loads(path.read_text())


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def ids(prefix, start, stop):
    return [f'{prefix}{i}' for i in range(start, stop + 1)]


def paragraph_hash(claim):
    direct = claim.get('proof_paragraph_sha256')
    location = claim.get('proof_location', {})
    values = [value for value in (
        direct, location.get('sha256'), location.get('paragraph_sha256')
    ) if value is not None]
    assert values and len(set(values)) == 1, ('missing/inconsistent paragraph hash', claim['id'])
    return values[0]


ledger = read(ROOT / 'provenance.json')
prior = read(OLD / 'provenance.json')
targets = read(ROOT / 'next_source_targets.json')
cfg = read(ROOT / 'increment_v0_20.json')
tex = read(ROOT / 'tex_validation.json')
assert ledger['commit'] == prior['commit'] == '7cbf7a0c32fca1badf05931879a37c3f8a2b03b4'
assert tex['syntax_compile_succeeded'] and not tex['pdf_generated']
assert not tex['pdf_visual_review_performed'] and not tex['page_count_asserted']
assert not tex['undefined_references_or_citations']
assert tex['missing_character_warnings'] == 0
assert tex['tex_filename'] == 'RH_readable_reconstruction_v0_20.tex'
assert tex['tex_sha256'] == sha(ROOT / tex['tex_filename'])
assert len(targets['global_branches_unchanged']) == 4
assert targets['global_branches_unchanged'] == read(OLD / 'next_source_targets.json')['global_branches_unchanged']
assert set(cfg['components']) == set(COMPONENTS)

claims = {claim['id']: claim for claim in ledger['claims']}
prior_ids = {claim['id'] for claim in prior['claims']}
expected = {
    f'{prefix}{i}'
    for prefix, count, _ in COMPONENTS.values()
    for i in range(1, count + 1)
}
assert len(prior_ids) == 896 and len(expected) == 87
assert len(claims) == len(ledger['claims']) == 983
assert not prior_ids & expected
assert set(claims) == prior_ids | expected

coverage = [
    ('adic_realization_GA1_12_review.txt', '/root/global_frame', 'adic_realization', ids('GA', 1, 12)),
    ('adic_realization_GA13_23_review.txt', '/root', 'adic_realization', ids('GA', 13, 23)),
    ('adic_reviews_finite_weil_arithmetic.txt', '/root/class_rank', 'finite_weil_arithmetic', ids('WA', 1, 19)),
    ('mass_formula_MF1_10_review.txt', '/root/comparison_span', 'mass_formula', ids('MF', 1, 10)),
    ('mass_formula_MF11_20_review.txt', '/root', 'mass_formula', ids('MF', 11, 20)),
    ('ray_prime_estimates_QR1_9_review.txt', '/root/global_frame', 'ray_prime_estimates', ids('QR', 1, 9)),
    ('ray_prime_estimates_QR10_14_review.txt', '/root/class_rank', 'ray_prime_estimates', ids('QR', 10, 14)),
    ('ray_prime_estimates_QR15_25_review.txt', '/root/comparison_span', 'ray_prime_estimates', ids('QR', 15, 25)),
]

component_claims = {}
actual_hashes = {}
for component, (prefix, count, _) in COMPONENTS.items():
    component_ledger = read(ROOT / component / 'provenance.json')
    component_claims[component] = {claim['id']: claim for claim in component_ledger['claims']}
    assert set(component_claims[component]) == set(ids(prefix, 1, count))
    source = (ROOT / component / 'main.tex').read_bytes()
    markers = list(re.finditer(rb'(?m)^\\paragraph\{([A-Z]+\d+):', source))
    hashes = {}
    for i, marker in enumerate(markers):
        cid = marker[1].decode()
        assert cid not in hashes, ('duplicate paragraph marker', component, cid)
        stop = markers[i + 1].start() if i + 1 < len(markers) else len(source)
        hashes[cid] = hashlib.sha256(source[marker.start():stop]).hexdigest()
    assert set(hashes) == set(ids(prefix, 1, count)), component
    for cid, value in hashes.items():
        assert paragraph_hash(component_claims[component][cid]) == value, ('component paragraph mismatch', cid)
        assert paragraph_hash(claims[cid]) == value, ('cumulative paragraph mismatch', cid)
    actual_hashes[component] = hashes

seen = set()
records = []
for filename, reviewer, component, scope in coverage:
    path = REV / filename
    assert path.is_file(), filename
    review_text = path.read_text()
    assert re.search(r'(?m)^(?:Result|Verdict):\s+PASS\b', review_text), filename
    assert re.search(r'(?m)^Reviewer:\s+' + re.escape(reviewer) + r'(?:\s|$)', review_text), ('wrong reviewer', filename)
    assert reviewer != COMPONENTS[component][2], ('self-review', filename)
    assert not seen & set(scope), ('duplicate coverage', filename)
    seen.update(scope)
    hashes = {cid: actual_hashes[component][cid] for cid in scope}
    for cid, value in hashes.items():
        # Bind the identifier and its exact current hash on the same review line.
        pattern = r'(?m)^' + re.escape(cid) + r'\b[^\n]*\b' + value + r'\b'
        assert re.search(pattern, review_text), ('stale or unbound review', filename, cid, value)
    records.append({
        'review': str(path.relative_to(ROOT)),
        'reviewer': reviewer,
        'component_author': COMPONENTS[component][2],
        'component': component,
        'claims': scope,
        'review_sha256': sha(path),
        'current_main_sha256': sha(ROOT / component / 'main.tex'),
        'current_report_sha256': sha(ROOT / component / 'report.txt'),
        'current_component_provenance_sha256': sha(ROOT / component / 'provenance.json'),
        'current_claim_paragraph_sha256': hashes,
    })
assert seen == expected, seen ^ expected
assert len(records) == 8

coverage_output = {
    'artifact_version': '0.20',
    'result': 'PASS',
    'new_claims': len(expected),
    'covered_new_claims': len(seen),
    'review_count': len(records),
    'method': 'Eight independently authored scoped mathematical/source reviews are bound to exact current proof-paragraph hashes in both component and cumulative ledgers. This bookkeeping is not an automated mathematical proof checker.',
    'paragraph_hash_convention': 'Raw UTF-8 bytes from a line-start \\paragraph{ID: marker to the next such marker, or EOF for the last paragraph, including intervening whitespace.',
    'cumulative_provenance_sha256': sha(ROOT / 'provenance.json'),
    'review_records': records,
    'no_lean_build_or_kernel_replay': True,
}
REV.mkdir(exist_ok=True)
coverage_path = REV / 'mathematical_review_coverage_v0_20.json'
coverage_path.write_text(json.dumps(coverage_output, ensure_ascii=False, indent=2) + '\n')

paths = {entry['path'] for entry in ledger['source_files']} | {entry['path'] for entry in targets['targets']}
report = f'''FINAL SCOPE AND MATHEMATICAL JOIN REVIEW: VERSION 0.20
Result: PASS within the explicit reconstruction scope
Date: {cfg['date']}
Pinned source: {ledger['commit']}
Method: write_final_scope_review_v0_20.py plus the eight named independent reviews

The cumulative note is a partial human-readable reconstruction with exact
source provenance. It is not a complete self-contained RH/Dirichlet-GRH
proof. Mathematical reviews, source hashes and TeX syntax validation are
distinct checks; no Lean build or kernel replay was performed.

All {len(expected)} new claims have independent reviews bound to their current
proof-paragraph hashes, also checked against the component and cumulative
ledgers. Coverage is exactly GA1--GA23, WA1--WA19, MF1--MF20 and QR1--QR25,
with no duplicate or omitted claim. Every reviewer differs from the
component's author. The continuity audit separately verifies all 896
predecessor claims, 1972 source-file records, 928 package files, previous
dependency lists and the four unchanged global branch records.

NORMALIZED ADIC REALIZATION
GA constructs the actual algebraic Hecke-to-adic character from the
stipulated GlobalArtin map. It proves finite-DVR integral-unit descent,
closedness and topology, finite coefficient-field containment, and
compatibility with the chosen embeddings. The complex-to-adic field
isomorphism is not assumed continuous: open kernels and the local
algebraic formula supply the required continuity. Local complex
characters have open kernel on units by the no-small-subgroups argument.
The inverse-arithmetic-Frobenius convention and inertia reciprocity sign
are preserved.

The actual shift and block characters are obtained on the stated datum.
Uniqueness from the unramified Frobenius values proves reading independence
and identifies the first installed twist character only after its exact
normalization and Reading record are supplied. The five host character
laws, auxiliary order-fifteen behavior and local IsGalOf/DeltaRead
consequences use the actual characters and embeddings. Arbitrary complex
finite-order characters are not substituted for normalized adic ones.

Global Artin reciprocity remains a named established input. Nonempty
twist/local indices, all-place SideB.cover, field containments, coefficient
readings and compatible representation/weight/form data remain separate.
Replacing characters on a bare empty-Loc skeleton does not construct that
nonempty arithmetic realization, RankTie, MuIsW or a full Core.

FINITE WEIL ARITHMETIC AND SUPPLIED BOTTOM PERIODS
WA uses the actual host ideal in the completed lattice and its absolute
codifferent trace-duality identity. The dyadic split-half clauses account
for the lattice sign. Finite Heisenberg eigenspaces and orthogonal
projectors produce algebraic expansion coefficients; finite pairings,
split normalization, positive-power closure and actual local unitary
generation remove the phase ambiguity and prove moved_translate_algComb.
This proof precedes the conditional theta-test consumers it supplies.

The result supplies NFJet and, for a literal supplied bottom triangle,
the normalized integral field assertion SumsIn. The comparison scalar
between fixed period-normalized entire models is nonzero; it is not
asserted to have absolute value one. Its value remains in the common
period factor, with both sides' normalizations respected.

Standard bottom geometry, ranks, parity, lattices and conductor joins are
constructed conditional on the two required new full Weil data. Local
Hilbert-90 sections and integral roots away from finitely many places
justify continuity of the determinant character on the restricted
product. Character twisting reduces arbitrary splitting characters to
the canonical eta case. The canonical full oriented adelic Weil datum,
its rational automorphy, the stronger quantitative DictAt dictionary,
critical ratio fields and the same Choice.FieldOK embedding join remain
explicit. Qualitative algebraicity does not give those stronger inputs.

HERMITIAN LOCAL DENSITIES AND THE ACTUAL MASS LAW
MF proves the unramified local Hermitian diagonalization/representation
statements and finite matrix/vector densities, including dyadic places.
Weighted local orbit counting gives the literal LIStat normalization.
Rank-one mass independence, finite global fiber patching and the weighted
singular-series average then give the rank induction and exact
SiegelMassRatioCM law with its factorial, discriminant and Euler factors.
Hasse--Minkowski is the explicitly retained classical theorem in the
global representation step; a mass formula is not assumed as that input.

MF19 supplies the previously conditional QW9 mass premise, and MF20 joins
them without rewriting the predecessor's conditional proof or graph.
The resulting numerical window keeps the actual size, host, word and
same-object ChOK/du/Ds hypotheses. This definite genus mass law does not
identify the geometric VolumeEqMass2/VolTie or indefinite volume factors,
and does not construct compatible recursive data or a full Core.

ACTUAL RAY FAMILY AND UNIFORM PRIME ESTIMATES
QR constructs every field of the literal ray-class LFam with conductor
4dM^2 and the same-family NormOne support. The arithmetic construction
precedes the analytic estimates, which are first proved for a supplied
family. Mellin continuation and the logarithmic derivative retain the
actual residue, theta and character-orthogonality normalizations.

The heat/Bessel positivity argument yields a uniform real-character value
bound of order B^(-45), and a Cauchy estimate gives the B^(-46) real-zero
separation. The subsequent argument controls the single possible simple
family exception, proves the uniform explicit formula and gives the
B^(-47) weighted short-interval lower bound. No inference of RH, a full
complex zero-free strip or the independent cohomological windows is made.

QR25 joins the actual family with this abstract-family estimate, closing
both previously retained QW11 suppliers. The exact prime-power removal
and weighted-to-unweighted transports give ShortNorm with exponent 47,
the source level-prime window and the nine-tenths dyadic norm-prime count.
The original geometric and interval hypotheses of those applications
remain in force. These particular arithmetic prime theorems do not
supply simultaneous PairEx choices or the final centered-prime-sum chain.

CURRENT REMAINING WORK
''' + ''.join(f'{i + 1}. {item}\n' for i, item in enumerate(cfg['remaining_major_inputs'])) + f'''
VERIFICATION AND LIMITS
The cumulative ledger contains {len(ledger['claims'])} claims and
{sum(len(claim['sources']) for claim in ledger['claims'])} claim-source links.
It indexes {len(ledger['source_files'])} pinned source files. The current map
has {len(targets['targets'])} target ranges; the claim/target union contains
{len(paths)} distinct source paths. The preserved human dependency graph
and the new supplier/consumer guards are audited separately. Hashes bind
files and reviews to exact bytes; they do not prove the mathematical
content of imported theorems or replace the independent reviews.

Historical target records remain archived. Newly retired generic targets
are conditional completions at their stated interfaces. The narrower
nonempty arithmetic, full Core, canonical bottom-Weil, same-field theta,
quantitative dictionary and four global branch requirements remain.

Draft-mode TeX validation took {tex['passes']} passes, with no undefined
references/citations or missing characters. It retained
{tex['overfull_box_warnings']} overfull-box warnings for a future rendering.
No PDF was generated; no current page count or visual layout certification
is asserted.

Provenance SHA256: {sha(ROOT / 'provenance.json')}
TeX SHA256: {sha(ROOT / tex['tex_filename'])}
Next-target SHA256: {sha(ROOT / 'next_source_targets.json')}
Increment configuration SHA256: {sha(ROOT / 'increment_v0_20.json')}
Review coverage SHA256: {sha(coverage_path)}
TeX validation SHA256: {sha(ROOT / 'tex_validation.json')}
Scope-review script SHA256: {sha(Path(__file__))}
'''
(REV / 'final_scope_review.txt').write_text(report)
print(json.dumps({
    'result': 'PASS',
    'new_claims': len(expected),
    'independently_reviewed': len(seen),
    'review_records': len(records),
    'total_claims': len(claims),
    'tex_hash_matches': True,
    'overfull_box_warnings': tex['overfull_box_warnings'],
    'pdf_generated': False,
}))
