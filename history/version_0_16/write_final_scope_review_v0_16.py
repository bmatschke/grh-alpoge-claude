#!/usr/bin/env python3
"""Record final proof scope, review coverage and remaining work for v0.16."""
from pathlib import Path
import hashlib
import json
import re

ROOT=Path(__file__).resolve().parent
REVIEW=ROOT/'reviews_v0_16'
def read(p):return json.loads(p.read_text())
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def ids(prefix,values):return [prefix+str(i)for i in values]
coverage=[
 ('root_reviews_ah_1_8_17_18.txt','/root','arithmetic_hosts',ids('AH',[1,2,3,4,5,6,7,8,17,18])),
 ('ci_reviews_ah9_16.txt','/root/global_frame','arithmetic_hosts',ids('AH',range(9,17))),
 ('ah_reviews_pa_1_4_11_15.txt','/root/class_rank','period_arithmetic',ids('PA',[1,2,3,4,11,12,13,14,15])),
 ('ah_reviews_pa_5_10.txt','/root/class_rank','period_arithmetic',ids('PA',range(5,11))),
 ('tx_reviews_ta.txt','/root/comparison_span','theta_arithmetic',ids('TA',range(1,15))),
 ('root_reviews_ci_1_9_15_19.txt','/root','canonical_indices',ids('CI',list(range(1,10))+list(range(15,20)))),
 ('tx_reviews_ci10_14.txt','/root/comparison_span','canonical_indices',ids('CI',range(10,15))),
 ('ci_reviews_tx1_5_8_9.txt','/root/global_frame','twisted_comparison',ids('TX',[1,2,3,4,5,8,9])),
 ('ah_reviews_tx6_7.txt','/root/class_rank','twisted_comparison',ids('TX',[6,7])),
 ('root_reviews_tx_10_16.txt','/root','twisted_comparison',ids('TX',range(10,17))),
]
ledger=read(ROOT/'provenance.json')
targets=read(ROOT/'next_source_targets.json')
config=read(ROOT/'increment_v0_16.json')
tex=read(ROOT/'tex_validation.json')
assert tex['syntax_compile_succeeded']and not tex['pdf_generated']
assert not tex['undefined_references_or_citations']and tex['missing_character_warnings']==0
expected={c['id']for c in ledger['claims']if c.get('introduced_in')=='0.16'}
seen=set();records=[]
for filename,reviewer,component,scope in coverage:
    p=REVIEW/filename
    assert p.is_file()and 'PASS'in p.read_text(),filename
    assert not (seen & set(scope)),filename
    seen.update(scope)
    source=(ROOT/component/'main.tex').read_bytes()
    pattern=rb'\\paragraph\{([A-Z]+\d+):'
    marks=list(re.finditer(pattern,source))
    paragraph_hashes={}
    for i,m in enumerate(marks):
        cid=m.group(1).decode()
        if cid in scope:
            stop=marks[i+1].start()if i+1<len(marks)else len(source)
            paragraph_hashes[cid]=hashlib.sha256(source[m.start():stop]).hexdigest()
    assert set(paragraph_hashes)==set(scope),filename
    records.append({'review':str(p.relative_to(ROOT)),'reviewer':reviewer,'component':component,
                    'claims':scope,'review_sha256':sha(p),'current_main_sha256':sha(ROOT/component/'main.tex'),
                    'current_claim_paragraph_sha256':paragraph_hashes})
assert seen==expected
review_record={
 'artifact_version':'0.16','result':'PASS','new_claims':len(expected),'covered_new_claims':len(seen),
 'method':'Record the independently authored scoped human reviews and current proof paragraph bytes. This bookkeeping is not an automated proof checker.',
 'review_records':records,'no_lean_build_or_kernel_replay':True,
}
(REVIEW/'mathematical_review_coverage_v0_16.json').write_text(json.dumps(review_record,ensure_ascii=False,indent=2)+'\n')
paths={s['path']for s in ledger['source_files']}|{s['path']for s in targets['targets']}
report=f'''FINAL SCOPE AND MATHEMATICAL JOIN REVIEW: VERSION 0.16
Result: PASS within the explicit conditional reconstruction scope
Date: {config['date']}
Pinned source: {ledger['commit']}

The deliverable is a cumulative human-readable proof reconstruction with a
source ledger, not a claim that RH or Dirichlet GRH has now been proved here.
All named ordinary classical background inputs remain visible. The new
proofs simplify the arguments where the exact source hypotheses permit it;
they do not replace a required constructor by an unspecified record.

NEW PROOF COVERAGE
There are {len(expected)} new claims: AH1--AH18, PA1--PA15, TA1--TA14,
CI1--CI19 and TX1--TX16. All are covered by independently authored scoped
human reviews. Mathematical_review_coverage_v0_16.json records those scopes
and current proof hashes. TA14 appears before TA1 in the readable note: it
is the analytic precursor added to prevent an arithmetic dependency cycle.

Arithmetic hosts. The conditional mixed-character cyclotomic construction
supplies the actual frame, character data and raw host. All thirty HostDer
fields are derived, including the chosen half-different, conjugated-trace
self-duality and the root-discriminant estimates. The eight FieldRows fields
are supplied with c0,e0 chosen before e,q,d,b. The label KcDiff.principal
asserts an ideal factorization; no principal generator is inferred. Analytic
selection of q,d in the required windows is still a separate input.

Ambient periods. The actual normalized period and unkilled half-point, the
rational four-copy trace isometry, its specified algebraic complex extension,
all local AtP corrections and all AmbIn.Ok fields are constructed. The local
Cayley approximation uses the opposite valuations at conjugate split primes;
it does not assume conjugation is continuous at one chosen prime. The finite
kappa product runs over the exact prime-and-SplitK subtype. The CM-j proof
retains the factor 1728, a unit leading coefficient and a nonsquare determinant.
The finite extension supplying FieldOK has the original universal containment
quantifier. Normalized torsion coordinates are algebraic; periods themselves
are not asserted algebraic.

One-dimensional theta arithmetic. The analytic normalized sigma laws are
proved separately. Formal differential-equation uniqueness, CM polynomial
descent and period comparison identify galSg. Exact division quotients and a
nonzero constant term fix the power-root ambiguity in gal1. Fixed-field
descent supplies all rational-translate coefficients, and the exact half-point
and 16-torsion transport supplies the even-theta conjugacy clauses. General
field embeddings are used only algebraically on countable generated fields;
no analytic continuity of an arbitrary embedding is assumed. TA10 supplies
the premise retained in PA15, without depending on PA15.

Local indices. Finite cosets, local normal forms, stabilized finite sums,
explicit finite-field positive counts and projected-kernel character rigidity
produce all 34 ChIdx.Ok fields and the actual initial/canonical index suppliers.
The nonzero sum proves character triviality independently of completed Laws
or column comparisons. Empty support and the operative one-coset range are
explicit. canon_ok retains its old-Ok and Deep premises.

Twisted comparison. The exact full scalar q_P^(c+1) differs from the row scalar
q_P; exponents are not identified with additive valuations without a
uniformizer hypothesis. The corrected coupling coset is z+q_P^M O^n with
center bound q_P^(-M)O^n. Deep character triviality uses ThetaOpen, not finite
order alone. The penultimate carrier has an explicit nonempty witness, giving
the required principal subgroup in its local stabilizer. The same integral
Delta lattice proves Law0; every permissible Law0 map is the same reindexing.
The local denominator is chosen outside the fixed prime. The exact movement
matrix, full-dual bar(pi)-unit cancellation and inverse character give the
terminal evaluation for the actual frame function. All ten standard twisted
column fields are assembled, retaining NChoice, TupTied and tp.xi=I.xi.

JOINS THAT REMAIN
1. The literal multidimensional StdOK/four-copy vacuum identity and normalized
   indicator/covariance, then the exact EvLg join. One-dimensional coefficient
   algebraicity does not identify that particular multivariable function.
2. Actual NChoice finite DVR extensions, valuation embeddings and Mt
   basis/integral-lattice comparison, plus TupTied for the same xi,psi,Q.
   Character readings alone are insufficient. Stronger one-level symmetric
   columns remain a distinct optional assertion.
3. Pins.iX and all five Later stages wherever their original interfaces occur.
4. Simultaneous analytic prime selection, top/logarithmic windows, LevelPrime,
   and the geometric Lay/RecOK/LedOK/RecExP mass/window suppliers.
5. The four independent global branches, unchanged: spectral/theta common
   images and quantitative norms; dimension and metric transport; congruence
   and cohomological windows; simultaneous PairEx and global prime-sum balance.

The exact current source-target map has {len(targets['targets'])} ranges in
{len({t['path']for t in targets['targets']})} files. Those entries are future
work, not additional proved claims. The completed local suppliers are removed
from the current frontier while all predecessor target records remain archived.

PRESERVATION AND VERIFICATION
The cumulative ledger has {len(ledger['claims'])} claims and
{sum(len(c['sources'])for c in ledger['claims'])} source-range links, indexing
{len(ledger['source_files'])} source files ({len(paths)} including next targets).
All 608 predecessor claims, source arrays, source-file records, dependency
adjacency lists and prior local-conclusion objects are preserved. All 651
predecessor package files retain their bytes, with its 20 root files archived.
The human dependency graph is acyclic; explicit checks cover the TA10/PA15,
CI13/Laws and TX10/final-join boundaries in addition to the earlier cycle checks.
Independent pinned-blob/range and navigation audits are recorded separately;
neither those checks nor these scoped reviews are a Lean build or kernel replay.

TeX passed {tex['passes']} draft-mode runs with no undefined cross-references
or citations and no missing-character warnings. No PDF was generated, no
current page count is asserted, and no visual layout review is claimed.
The {tex['overfull_box_warnings']} overfull-box warnings are retained in the
validation record for a later rendering round. The v0.13 PDF is historical
and does not contain the v0.14--v0.16 work.

Current TeX SHA256: {sha(ROOT/'RH_readable_reconstruction_v0_16.tex')}
Current provenance SHA256: {sha(ROOT/'provenance.json')}
Current target map SHA256: {sha(ROOT/'next_source_targets.json')}
Review coverage SHA256: {sha(REVIEW/'mathematical_review_coverage_v0_16.json')}
'''
report=report.replace('Mathematical_review_coverage','mathematical_review_coverage')
(REVIEW/'final_scope_review.txt').write_text(report)
print(json.dumps({'result':'PASS','new_claims':len(expected),'scoped_reviews':len(records),
                  'scope_review_sha256':sha(REVIEW/'final_scope_review.txt')}))
