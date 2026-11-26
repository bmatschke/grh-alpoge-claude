#!/usr/bin/env python3
"""Bind independent scoped reviews to current proof bytes and state v0.22 limits.

This is reproducible coverage bookkeeping, not an automated mathematical
proof checker. Substantive scrutiny is recorded in the named review files.
"""
from pathlib import Path
from collections import Counter
import hashlib
import json
import re

ROOT = Path(__file__).resolve().parent
REV = ROOT / 'reviews_v0_22'
OLD = ROOT / 'history/version_0_21'
COMPONENTS = {
    'automorphic_realization': ('MR', 26, '/root/class_rank'),
    'quantitative_weil_dictionary': ('QD', 22, '/root/comparison_span'),
    'discrete_series_core': ('DC', 22, '/root/global_frame'),
    'simultaneous_prime_pairs': ('QP', 25, '/root'),
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
cfg = read(ROOT / 'increment_v0_22.json')
tex = read(ROOT / 'tex_validation.json')
assert ledger['commit'] == prior['commit'] == '7cbf7a0c32fca1badf05931879a37c3f8a2b03b4'
assert tex['syntax_compile_succeeded'] and not tex['pdf_generated']
assert not tex['pdf_visual_review_performed'] and not tex['page_count_asserted']
assert not tex['undefined_references_or_citations']
assert tex['missing_character_warnings'] == 0
assert tex['tex_filename'] == 'RH_readable_reconstruction_v0_22.tex'
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
assert len(prior_ids) == 1073 and len(expected) == 95
assert len(claims) == len(ledger['claims']) == 1168
assert not prior_ids & expected and set(claims) == prior_ids | expected

# Four independent reviews partition all 95 newly authored claims.
coverage = [
    ('automorphic_realization_independent_review.json', '/root', 'automorphic_realization', ids('MR',1,26), False),
    ('quantitative_weil_dictionary_independent_review.json', '/root/class_rank', 'quantitative_weil_dictionary', ids('QD',1,22), False),
    ('discrete_series_core_independent_review.json', '/root/comparison_span', 'discrete_series_core', ids('DC',1,22), False),
    ('dc_reviews_qp.json', '/root/global_frame', 'simultaneous_prime_pairs', ids('QP',1,25), False),
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
    review_result=review.get('result', review.get('status'))
    assert review_result in {
        'PASS', 'PASS_UNDER_EXPLICIT_CLASSICAL_AND_INHERITED_PREMISES'
    }, filename
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
        'review_result_as_stated': review_result,
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
assert len(records) == 4
assert {cid for cid, count in coverage_counts.items() if count != 1} == set()
assert max(coverage_counts.values()) == 1
coverage_output = {
    'artifact_version': '0.22',
    'result': 'PASS',
    'new_claims': len(expected),
    'covered_new_claims': len(coverage_counts),
    'review_count': len(records),
    'primary_review_count': 4,
    'supplemental_review_count': 0,
    'claims_with_second_independent_review': [],
    'method': 'Four independently authored scoped mathematical/source reviews partition all 95 new claims. Each reviewer differs from the component author. All reviews are bound to exact current proof-paragraph hashes in both component and cumulative ledgers. This bookkeeping is not an automated mathematical proof checker.',
    'paragraph_hash_convention': 'Raw UTF-8 bytes from a line-start \\paragraph{ID: marker to the next such marker, or EOF for the last paragraph, including intervening whitespace.',
    'cumulative_provenance_sha256': sha(ROOT / 'provenance.json'),
    'review_records': records,
    'no_lean_build_or_kernel_replay': True,
}
REV.mkdir(exist_ok=True)
(REV / 'mathematical_review_coverage_v0_22.json').write_text(
    json.dumps(coverage_output, ensure_ascii=False, indent=2) + '\n')


paths={entry['path'] for entry in ledger['source_files']}|{entry['path'] for entry in targets['targets']}
report=f'''FINAL SCOPE AND MATHEMATICAL JOIN REVIEW: VERSION 0.22
Result: PASS within the displayed conditional reconstruction scope
Date: {cfg['date']}
Pinned source: {ledger['commit']}

This cumulative note is a partial human-readable reconstruction, not a
complete self-contained proof of RH or Dirichlet GRH. Source-byte checks,
mathematical scrutiny, record inventories and TeX syntax checks are separate.
No Lean build or independent kernel replay occurred.

All {len(expected)} new claims have an independent scoped mathematical review:
MR1–MR26 by /root, QD1–QD22 by /root/class_rank, DC1–DC22 by
/root/comparison_span and QP1–QP25 by /root/global_frame. Each reviewer
is different from the author. All exact current paragraph hashes match
both component and cumulative ledgers. Whole main/report hashes also match.
The four JSON records and their TXT companions state findings and limits.
Coverage bookkeeping does not turn the reviews into formal proof checking.

The continuity audit preserves all 1073 previous claims, 2221 previous
source-file records, all 1065 predecessor package files, old dependency
adjacency lists and all four global branch records. Historical proofs and
hypotheses remain unchanged; current scope annotations are additive.

NEW RECONSTRUCTED CONSTRUCTIONS
''' + '\n\n'.join(cfg['new_in_this_version']) + f'''

JOIN AND NORMALIZATION REVIEW
MR gives the whole TypeSp through the original tuple basis, not a map
inferred solely from equal dimension. Prime-local Hecke integrality is
proved on the actual nabla lattice with the exact residue-prime exclusion.
The additive K-reading need not be multiplicative, which keeps the
original coefficient DVR. Dedekind-flat finite-equation descent gives
stability of the actual good lattice. The initial SideB endpoint is
conditional on a subsequently supplied NTh; zero theta and empty toric
fields, including the otherwise unused Mt parameters, are explicitly
recorded. No nonempty genuine theta/local family is claimed from them.

QD proves actual arithmetic scalar normalization using finite Fourier
relations, real determinant characters, rational/split/stabilizer
factorization and entire jets. One kappa works at all standard primes.
The finite quotient denominator uses f=[F:Q], not the CM degree [E:Q].
Uncollected coefficients nu_i/n have nu_i^(2k^2)=1, n divides k^(fab),
and the all-conjugate l1 sum is one; collecting terms only reduces it.
These statements apply to the actual supplied original choices. Critical
toric ratios and the original-embedding Choice.FieldOK join remain.

DC constructs the sufficient actual large-gap range rather than claiming
all regular parameters. The full Capelli central polynomial and signs,
not only the Casimir, are identified. Haar normalization includes the
compact center and is calibrated by a direct Bergman beta integral.
Harish-Chandra's formal-degree theorem remains a named unreconstructed
input. The exact four RealTied fields and both restricted later-stage
uses are checked. GV's unitary Tamagawa theorem remains named for the
actual volume, and full same-X Core/layout/arithmetic fields are retained.
The weaker threshold in the literal isDS_props_of_gap source is not
silently claimed by the stronger DC.2 construction.

QP retains CN (quadratic analytic class-number formula), BD (Bombieri
log-free density with its exceptional-zero factor), and HD (Heath-Brown
1979 Theorem1). The signed pole-at-zero constant cancels low-zero
reciprocals before estimation. Relative error preserves the exceptional
small main term. The continuum maximal argument treats every real y,
not only sampled endpoints. High-T explicit formulas retain the left-edge
term; imprimitive deleted-Euler tails are explicitly bounded. The leading
one in Mertens' estimate preserves the exact final 4 log y coefficient.
Primitive conductor one is handled separately in the bad-box count.
Inducer uniqueness has a positive ambient modulus. Both primes satisfy
all prescribed clauses, yet RealBox/ThinH still require the same compatible
host, and winPairs retains VWinAt(psi,401) and its cohomological suppliers.

NAMED INPUTS, STRONGER INTERFACES AND REMAINING WORK
''' + ''.join('- '+x+'\n' for x in cfg['remaining_major_inputs']) + f'''

SOURCE AND DOCUMENT EVIDENCE
The cumulative ledger records {len(claims)} claims and
{sum(len(c['sources']) for c in ledger['claims'])} claim-source links,
with {len(ledger['source_files'])} indexed files. The target map has
{len(targets['targets'])} exact ranges; the total pin coverage is
{len(paths)} distinct source files. Target entries are remaining-scope
navigation, not additional proved claims. The recorded human graph is
acyclic and preserves every historical edge.

The complete cumulative TeX passed draft-mode compilation with resolved
references/citations and no missing characters. No PDF was generated.
There are {tex['overfull_box_warnings']} overfull-box warnings, disclosed for a
future visual-layout pass. This is no claim of current page count or
visual layout validation. Reviewed component bytes remain unchanged by
the cumulative assembly's permitted typography normalization.

Current provenance SHA256: {sha(ROOT/'provenance.json')}
Current TeX SHA256: {sha(ROOT/tex['tex_filename'])}
Current target SHA256: {sha(ROOT/'next_source_targets.json')}
Coverage SHA256: {sha(REV/'mathematical_review_coverage_v0_22.json')}
This script SHA256: {sha(Path(__file__))}
'''
(REV/'final_scope_review.txt').write_text(report)
print(json.dumps({'result':'PASS','new_claims':len(expected),'covered_claims':len(coverage_counts),
                  'reviews':len(records),'tex_syntax_valid':True,'pdf_generated':False}))
