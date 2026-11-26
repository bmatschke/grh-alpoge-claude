#!/usr/bin/env python3
"""Bind independent scoped reviews to current proof bytes and state v0.21 limits.

This is reproducible coverage bookkeeping, not an automated mathematical
proof checker. Substantive scrutiny is recorded in the named review files.
"""
from pathlib import Path
from collections import Counter
import hashlib
import json
import re

ROOT = Path(__file__).resolve().parent
REV = ROOT / 'reviews_v0_21'
OLD = ROOT / 'history/version_0_20'
COMPONENTS = {
    'nonempty_realization': ('NR', 24, '/root/class_rank'),
    'canonical_weil': ('CW', 25, '/root/comparison_span'),
    'geometric_volumes': ('GV', 21, '/root/global_frame'),
    'centered_character_sums': ('CC', 20, '/root'),
}


def read(path):
    return json.loads(path.read_text())


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def ids(prefix, start, stop):
    return [f'{prefix}{i}' for i in range(start, stop + 1)]


def paragraph_hash(claim):
    location = claim.get('proof_location', {})
    values = [value for value in (
        claim.get('proof_paragraph_sha256'), location.get('sha256'),
        location.get('paragraph_sha256')
    ) if value is not None]
    assert values and len(set(values)) == 1, ('missing/inconsistent proof hash', claim['id'])
    return values[0]


ledger = read(ROOT / 'provenance.json')
prior = read(OLD / 'provenance.json')
targets = read(ROOT / 'next_source_targets.json')
cfg = read(ROOT / 'increment_v0_21.json')
tex = read(ROOT / 'tex_validation.json')
assert ledger['commit'] == prior['commit'] == '7cbf7a0c32fca1badf05931879a37c3f8a2b03b4'
assert tex['syntax_compile_succeeded'] and not tex['pdf_generated']
assert not tex['pdf_visual_review_performed'] and not tex['page_count_asserted']
assert not tex['undefined_references_or_citations']
assert tex['missing_character_warnings'] == 0
assert tex['tex_filename'] == 'RH_readable_reconstruction_v0_21.tex'
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
assert len(prior_ids) == 983 and len(expected) == 90
assert len(claims) == len(ledger['claims']) == 1073
assert not prior_ids & expected and set(claims) == prior_ids | expected

# The first eight reviews partition the increment. The last is an intentional
# second independent review of the rational Weil phase and its final joins.
coverage = [
    ('nonempty_realization_NR1_18_review.json', '/root', 'nonempty_realization', ids('NR', 1, 18), False),
    ('nonempty_realization_NR19_24_review.json', '/root', 'nonempty_realization', ids('NR', 19, 24), False),
    ('canonical_weil_CW1_13_review.json', '/root', 'canonical_weil', ids('CW', 1, 13), False),
    ('canonical_weil_CW14_end_review.json', '/root', 'canonical_weil', ids('CW', 14, 25), False),
    ('geometric_volumes_GV1_12_review.json', '/root', 'geometric_volumes', ids('GV', 1, 12), False),
    ('geometric_volumes_GV13_21_review.json', '/root', 'geometric_volumes', ids('GV', 13, 21), False),
    ('centered_character_sums_analytic_review.json', '/root/comparison_span', 'centered_character_sums', ids('CC', 1, 8), False),
    ('centered_character_sums_tail_review.json', '/root/class_rank', 'centered_character_sums', ids('CC', 9, 20), False),
    ('canonical_weil_rational_independent_review.json', '/root/global_frame', 'canonical_weil', ids('CW', 16, 25), True),
]
component_claims = {}
actual_hashes = {}
for component, (prefix, count, _) in COMPONENTS.items():
    data = read(ROOT / component / 'provenance.json')
    component_claims[component] = {claim['id']: claim for claim in data['claims']}
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
        assert paragraph_hash(component_claims[component][cid]) == value, ('component proof mismatch', cid)
        assert paragraph_hash(claims[cid]) == value, ('cumulative proof mismatch', cid)
    actual_hashes[component] = hashes

seen_primary = set()
coverage_counts = Counter()
records = []
for filename, reviewer, component, scope, supplemental in coverage:
    path = REV / filename
    review = read(path)
    assert review.get('result', review.get('status')) == 'PASS', filename
    assert review['reviewer'] == reviewer, ('wrong reviewer', filename)
    assert review['author'] == COMPONENTS[component][2], ('wrong author', filename)
    assert reviewer != COMPONENTS[component][2], ('self-review', filename)
    assert set(review['reviewed_claims']) == set(scope), ('scope mismatch', filename)
    assert not review.get('unresolved_findings', []), ('unresolved finding', filename)
    if not supplemental:
        assert not seen_primary & set(scope), ('duplicate primary coverage', filename)
        seen_primary.update(scope)
    hashes = {cid: actual_hashes[component][cid] for cid in scope}
    assert review['reviewed_claims'] == hashes, ('stale paragraph review', filename)
    artifacts = review.get('artifacts_reviewed', {})
    main_sha = review.get('main_sha256', artifacts.get('main_tex_sha256'))
    report_sha = review.get('report_sha256', artifacts.get('report_txt_sha256'))
    assert main_sha == sha(ROOT / component / 'main.tex'), ('stale main snapshot', filename)
    assert report_sha == sha(ROOT / component / 'report.txt'), ('stale report snapshot', filename)
    coverage_counts.update(scope)
    records.append({
        'review': str(path.relative_to(ROOT)),
        'reviewer': reviewer,
        'component_author': COMPONENTS[component][2],
        'component': component,
        'claims': scope,
        'supplemental_independent_review': supplemental,
        'review_sha256': sha(path),
        'current_main_sha256': main_sha,
        'current_report_sha256': report_sha,
        'current_component_provenance_sha256': sha(ROOT / component / 'provenance.json'),
        'current_claim_paragraph_sha256': hashes,
    })
assert seen_primary == set(coverage_counts) == expected
assert len(records) == 9
assert {cid for cid, count in coverage_counts.items() if count == 2} == set(ids('CW', 16, 25))
assert max(coverage_counts.values()) == 2
coverage_output = {
    'artifact_version': '0.21',
    'result': 'PASS',
    'new_claims': len(expected),
    'covered_new_claims': len(coverage_counts),
    'review_count': len(records),
    'primary_review_count': 8,
    'supplemental_review_count': 1,
    'claims_with_second_independent_review': ids('CW', 16, 25),
    'method': 'Eight independently authored scoped mathematical/source reviews partition all 90 new claims. A ninth independently reviews CW16-CW25 again. All reviews are bound to exact current proof-paragraph hashes in both component and cumulative ledgers. This bookkeeping is not an automated mathematical proof checker.',
    'paragraph_hash_convention': 'Raw UTF-8 bytes from a line-start \\paragraph{ID: marker to the next such marker, or EOF for the last paragraph, including intervening whitespace.',
    'cumulative_provenance_sha256': sha(ROOT / 'provenance.json'),
    'review_records': records,
    'no_lean_build_or_kernel_replay': True,
}
REV.mkdir(exist_ok=True)
(REV / 'mathematical_review_coverage_v0_21.json').write_text(
    json.dumps(coverage_output, ensure_ascii=False, indent=2) + '\n')

paths = {entry['path'] for entry in ledger['source_files']} | {entry['path'] for entry in targets['targets']}
report = f'''FINAL SCOPE AND MATHEMATICAL JOIN REVIEW: VERSION 0.21
Result: PASS within the explicit reconstruction scope
Date: {cfg['date']}
Pinned source: {ledger['commit']}
Method: write_final_scope_review_v0_21.py plus nine named scoped reviews

The cumulative note remains a partial human-readable reconstruction with
exact source provenance. It is not a complete self-contained RH or
Dirichlet-GRH proof. Mathematical review, source-byte checking and TeX
syntax validation are distinct. No Lean build or kernel replay occurred.

All {len(expected)} new claims have an independent review bound to the exact
current proof-paragraph bytes and checked against both ledgers. Eight
primary records partition NR1--NR24, CW1--CW25, GV1--GV21 and CC1--CC20.
The ninth record independently reviews CW16--CW25 a second time, including
the exact rational phase. Every reviewer differs from the component
author. Current whole-component and report snapshots also agree.

The continuity audit checks all 983 predecessor claims, 2106 source-file
records, 997 package files, every old dependency list and all four
unchanged global-branch records. Historical text is preserved. Current
scope annotations and target retirements are additive and explicit.

ACTUAL NONEMPTY COEFFICIENT FAMILIES AND CONDITIONAL ROW REPRESENTATIONS
NR constructs prime-compatible embeddings, complete unramified coefficient
DVRs, finite cyclotomic extensions, and actual universal finite
anticyclotomic quotients. The denominator-generation argument uses a
bounded coefficient right inverse and remains valid when a polynomial
degree drops after completion. The quotient universality has exactly the
source's restrictions at primes over ell; neither nontriviality nor full
ramification support is asserted.

On the original fixed global fields and D, Tw is every finite prime of
the coefficient integer ring. The actual TwR and RingSpec fields are
constructed, with normalized adic characters and the required Read
exponents. Exact coefficient-place coverage and Reading.Induces hold at
every prescribed place of the full coefficient field. The full-field
containment remains a supplied hypothesis; changing the global field
silently is not part of this construction.

The finite-field descent proof for compact continuous Qbar_ell
representations uses a countable cofinal family of finite local fields
from Krasner's lemma, Baire category, and finitely many compact-group
cosets. It does not claim the image is finite. A stable integral lattice
then follows from boundedness. The normalized row twist, universal
reading comparison and one coefficient-field bound give the literal
integral row-family supplier under GalEx, RowCusp, ChebSplit, SideA and
the named GlobalArtin input. Full SideB, genuine forms, Mt data,
residual/tame compatibility and a nonempty local stage remain.

FULL FINITE/REAL WEIL ACTION AND EXACT RATIONAL AUTOMORPHY
CW constructs the finite action on the actual theta space from signed
lattice intertwiners, finite character projectors and relations. The
host ideal, dyadic trace-one half, signed square-root function and
crossed determinant characters are retained. Norm, commutation and
continuity assertions apply on the stated theta domain; arbitrary
algebraic extensions outside that domain are not given analytic claims.

The real action is constructed by convergent Gaussian projectors on the
specified Banach smooth domain. Exact two- and three-projector
determinants fix the phase, and the transformed coherent-coefficient
identity establishes smoothness before closure is used. Norm preservation
is asserted with the actual bounded linear map hypothesis. The Cartan
vacuum determinant has the source orientation.

For rational elements, the combined action first differs from pullback
by a scalar of modulus one. An actual Gaussian theta series, a finite
Hermitian Gauss sum, paired lattice-index identities, the same eta
product formula and the real Gaussian determinant determine its phase.
The common Cartan/eta sign cancels using a generic norm-one scalar.
Only after this cancellation does positivity and modulus one imply the
scalar is exactly one. Quasi-reflection generation gives the full
rational pullback identity, hence the required automorphy at zero.

CW23 supplies all eleven canonical full-Weil fields and the two extra
vacuum clauses under a supplied IsEtaTilde. CW24 separately constructs
the actual prescribed-character full datum using the explicit HF11 eta0
readings and WA18 character twisting. It does not infer the separate
universal IsEtaTilde bridge or global norm-index uniqueness. The final
supplied characters furnish their own universal restrictions. CW25
therefore supplies the new bottom representations and bottom families;
WA16 supplies their common period field for finite twist index T.
Quantitative DictAt, critical toric ratios and the exact same-choice
coefficient-embedding join remain.

GEOMETRIC VOLUME WITH ITS EXPLICIT CLASSICAL INPUT
GV constructs the actual normalized Haar measure, rational fundamental
domain and direct definite quotient-to-genus-mass identity. It computes
the real compact-dual constant and the dyadic finite Lie-lattice factor,
then cancels auxiliary determinant and delta factors by the product
formula. The rank-one convergence factor is canceled locally before
forming Euler products, so no zeta(1) is introduced.

Writing f=[F:Q], a=n(n+1)/2 and
  A_n=(2*pi)^a / product_(j=0)^(n-1) j!,
the exact conversion is
  d tau = C_n d mu,
  C_n = |disc F|^(-n^2/2) A_n^f / product_(j=1)^n L_F(j,epsilon^j).
For positive rank, the named classical unitary Tamagawa-number theorem
tau(U)=2 gives M_n=2/C_n; rank zero is treated separately as M_0=1.
The Tamagawa theorem is an explicit unreconstructed input, with its
normalization recorded from the primary source:
  Harris--Li--Skinner, section 0.2,
  https://ems.press/content/book-chapter-files/27474
  https://doi.org/10.4171/DMS/4/12
GV11's direct definite mass identity and GV17's Haar scale comparison
are independent of this input.

The resulting signature-independent volumes give VolumeEqMass2,
trueVol and the same-stage VolTieG. The norm-sign UnitSplit step retains
classical Hasse--Minkowski. Quotient probability measures and the level
index direction are explicit. The RealTied/Core joins retain
DiscreteSeriesExist, FormalDegreeFormula2 and all other exact supplied
fields; dependent layouts and Core records are not automatically
transported by merely replacing a volume field.

EXACT CENTERINGS AND UNIFORM LATE-CUTOFF CHARACTER SUMS
CC derives the primitive Dirichlet functional equation, uniform growth,
height-radius-one zero windows, the zero-free strip with its possible
real exception, and the exact floor-endpoint explicit formula. The
closed-strip and logarithmic-denominator conventions are matched by a
fixed shrinkage, and the pointwise zero bound covers zeros at nonpositive
real part as well. The residue at zero and all low-zero reciprocal
terms remain in the explicit-formula estimate.

For psi0(chi,u)=sum_(n<=floor u) Lambda(n) chi(n)-delta_chi*u,
the exact centered function satisfies
  G0(chi,y) = -y integral_y^infinity psi0(chi,u)/u^2 du.
For nonprincipal chi the centering is +y L'_chi(1)/L_chi(1).
For the primitive principal character the subtracted term is
y(log y-1-gamma); its constant follows from the Laurent expansion and
is not replaced by -gamma alone. Primitive principal means conductor 1.

The uniform psi estimate chooses constants before the conductor,
character and height, retaining the real-zero exclusion. Above the
source's exponential cutoff the two strict exponent gaps
61/300>1/5 and 13/100>1/8 justify a uniform tail bound. CC16 supplies the
literal QH.thin. The quadratic conductor restriction and the finite
bounded-modulus zero exclusion then supply the actual same-host ThinH
under RealBox, the original conductor/odd-part bounds and
0<epsilon<1/52. CC20 adds a derivative and increment estimate on that
late-cutoff range. No polynomial-window square-root estimate, PairEx,
unconditional RealBox construction or relative progression theorem is
inferred from this conclusion.

CURRENT REMAINING WORK
''' + ''.join('- ' + item + '\n' for item in cfg['remaining_major_inputs']) + f'''
EVIDENCE AND LIMITS
The merged ledger contains {len(claims)} claims,
{sum(len(c['sources']) for c in ledger['claims'])} exact claim-source links,
and {len(ledger['source_files'])} indexed files. The current target map has
{len(targets['targets'])} ranges. Claim and target coverage together refer
to {len(paths)} distinct pinned files. Exact byte verification is
recorded separately in source_verification_v0_21_audit.json.

Draft-mode TeX compilation passed with no undefined references or
citations and no missing-character warnings. It generated no PDF.
There are {tex['overfull_box_warnings']} overfull-box warnings retained for a
future visual-layout pass. The assembly normalizes multi-column aligned
displays and line breaks without changing reviewed component proof bytes.
No current page count, visual review or complete proof certification is
claimed.

Current provenance SHA256: {sha(ROOT / 'provenance.json')}
Current TeX SHA256: {sha(ROOT / tex['tex_filename'])}
Current target map SHA256: {sha(ROOT / 'next_source_targets.json')}
Coverage record SHA256: {sha(REV / 'mathematical_review_coverage_v0_21.json')}
This script SHA256: {sha(Path(__file__))}
'''
(REV / 'final_scope_review.txt').write_text(report)
print(json.dumps({
    'result': 'PASS', 'new_claims': len(expected), 'covered_claims': len(coverage_counts),
    'reviews': len(records), 'claims_with_second_review': 10,
    'tex_syntax_valid': True, 'pdf_generated': False
}))
