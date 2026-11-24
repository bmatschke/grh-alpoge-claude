#!/usr/bin/env python3
"""Record independent review coverage and the precise v0.17 joins."""
from pathlib import Path
import hashlib,json,re
ROOT=Path(__file__).resolve().parent;REV=ROOT/'reviews_v0_17'
def read(p):return json.loads(p.read_text())
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def ids(p,ns):return[p+str(i)for i in ns]
coverage=[
 ('root_reviews_vi.txt','/root','vacuum_identity',ids('VI',range(1,12))),
 ('root_reviews_ca.txt','/root','canonical_analytic',ids('CA',range(1,14))),
 ('ca_reviews_nc_1_4_10_13.txt','/root/global_frame','arithmetic_choice',ids('NC',list(range(1,5))+list(range(10,14)))),
 ('vi_reviews_nc_5_9_14_17.txt','/root/comparison_span','arithmetic_choice',ids('NC',list(range(5,10))+list(range(14,18)))),
 ('nc_reviews_se_1_8_13_16.txt','/root/class_rank','stage_existence',ids('SE',list(range(1,9))+list(range(13,17)))),
 ('vi_reviews_se_9_12.txt','/root/comparison_span','stage_existence',ids('SE',range(9,13))),
]
extra=[('nc_reviews_ca_3_8.txt','/root/class_rank','canonical_analytic',ids('CA',range(3,9))),
       ('ca_reviews_vi_2_7.txt','/root/global_frame','vacuum_identity',ids('VI',range(2,8)))]
ledger=read(ROOT/'provenance.json');targets=read(ROOT/'next_source_targets.json');cfg=read(ROOT/'increment_v0_17.json');tex=read(ROOT/'tex_validation.json')
assert tex['syntax_compile_succeeded']and not tex['pdf_generated']
assert not tex['undefined_references_or_citations']and tex['missing_character_warnings']==0
expected={c['id']for c in ledger['claims']if c.get('introduced_in')=='0.17'};seen=set();records=[]
for filename,reviewer,component,scope in coverage+extra:
 p=REV/filename;assert p.is_file()and'PASS'in p.read_text(),filename
 if (filename,reviewer,component,scope)in coverage:
  assert not seen&set(scope);seen.update(scope)
 source=(ROOT/component/'main.tex').read_bytes();marks=list(re.finditer(rb'\\paragraph\{([A-Z]+\d+):',source));ph={}
 for i,m in enumerate(marks):
  cid=m[1].decode()
  if cid in scope:
   stop=marks[i+1].start()if i+1<len(marks)else len(source);ph[cid]=hashlib.sha256(source[m.start():stop]).hexdigest()
 assert set(ph)==set(scope),filename
 for cid,h in ph.items():assert h in p.read_text(),('review stale',filename,cid,h)
 records.append(dict(review=str(p.relative_to(ROOT)),reviewer=reviewer,component=component,claims=scope,review_sha256=sha(p),current_main_sha256=sha(ROOT/component/'main.tex'),current_claim_paragraph_sha256=ph,additional_overlap_review=(filename,reviewer,component,scope)in extra))
assert seen==expected,(seen^expected)
out=dict(artifact_version='0.17',result='PASS',new_claims=len(expected),covered_new_claims=len(seen),method='Independently authored scoped mathematical/source reviews checked against current proof paragraph hashes. This bookkeeping is not an automated proof checker.',review_records=records,no_lean_build_or_kernel_replay=True)
(REV/'mathematical_review_coverage_v0_17.json').write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n')
paths={s['path']for s in ledger['source_files']}|{s['path']for s in targets['targets']}
report=f'''FINAL SCOPE AND MATHEMATICAL JOIN REVIEW: VERSION 0.17
Result: PASS within the exact conditional reconstruction scope
Date: {cfg['date']}
Pinned source: {ledger['commit']}

This deliverable is a cumulative human-readable reconstruction with a
source ledger. It does not claim that RH or Dirichlet GRH has been proved
here. Named classical background, supplied objects and quantifier order
remain explicit. Exact source hashes and independent human review are
distinct from a Lean build or kernel replay, neither of which was performed.

NEW COVERAGE
All {len(expected)} new claims are independently reviewed: VI1–VI11,
CA1–CA13, NC1–NC17 and SE1–SE16. The difficult covariance phase and
integral vacuum construction also received overlapping peer reviews.
The coverage JSON records each reviewer, exact claim scope and paragraph
hash. All690 predecessor claim records and original graph entries remain.

VACUUM AND GERM JOIN
VI proves the actual trace-dual full period lattices and quadratic
semicharacter, all ten StdData fields, finite Fourier inversion and the
positive-normalized mean isometry. The four-copy root is a scalar root
after theta-line factorization, never a pointwise analytic branch. The
actual thMM is the chosen element of the proved nonempty predicate.
Rational translations have algebraic phases. Applying the same derivative
in all four blocks gives its fourth power algebraic, including zero
constant terms without division. Rectangular products and both actual
moving intertwiners then give thZero/thMoved and the required germs.

INDICATOR, COVARIANCE AND CANONICAL JOIN
CA2 expands the actual normalized finite indicator and proves its support
and coefficient bounds independently of algebraic jets. VI11 uses this
finite identity; final FinAlg subsequently uses VI11. The dependency is
acyclic. CA3–CA5 account for the negative norm Gauss sum at conjugation-
fixed primes and the even opposite rank that cancels this sign for the
actual one-factor moves. Positive Iop is not declared path-independent on
arbitrary lattice triples. The Gaussian trace, finite Gauss positivity and
determinant identities compute the phase left open by theta-line uniqueness.
Both coordinate-action directions and both determinant exponents are kept.

The actual finite Taylor field follows from finitely many rational-unitary
lattice classes, finite denominator classes, algebraic representative jets,
and rational-unitary covariance. No entire theta function is made a
polynomial. The source allSet's FinAlg restriction is retained and checked
for the actual selected step. Host-level VacIn and literal restriction
identities bypass unused complete Stages fields; no NStage existence is
imported into FinAlg. The EvLg implication keeps its fixed/full finite field
sets, raw PreX and frame-inclusion antecedents and prescribed selector.
Its J=amb0, S, xi range, modulus and degree remain the same through canon.
Universal ValLL0 over later assemblies is not existence of those assemblies.

ARITHMETIC CHOICE JOIN
Finite complete-DVR extensions are constructed in the characteristic-zero
instance actually used. Prime alignment uses the prescribed coefficient
place, and the local/full integral lattice comparisons are semilinear with
the exact generator spans. All21 NChoice fields, all5 NChTie fields and
all12 TupTied fields are reconstructed at their literal conditional scope.
RankTie is retained and is necessary; arbitrary equal-rank lattice matching
does not produce Hecke or metric intertwining. The general tied-choice
construction does not acquire the stronger Galois-over-Q premise used only
in the optional conjugate-reading construction. Exact finite support,
conjugation, Q and the same descended character are retained in MuIsW and
LocsCarry. NC17 applies TX16 to those same objects.

STAGES, NORMALIZATION AND A CONCRETE COMPATIBILITY OBSTRUCTION
SE's common-kernel argument descends the actual operators via a linear
splitting. Positive Gram matrices give restricted Hermitian frames at every
infinite place. Noetherianity and denominator clearing make the actual
intersection lattice full, without global integral freeness. All14 DivStage
fields include the exact ramL image and norm equalities on the same W.

Actual class forms give Fits; the explicit RowsRest model checks all88
fields including25 typeclass fields. SStage uses the exact HasLetters and
class metric but may have zero spectral terms. Ordinary completions and
optional split data are distinct from Fontaine period rings. The compact-
dual Haar proof verifies all4 fields, including normalized product volume
and a common finite positive exponential-chart density. Bare GJStage uses
the explicit prescribed-rank constant module and may have empty situations
and constant positive volumes; it does not identify those with trueVol.

The five-stage join retains full NStage on the exact adapted rows. The
source's particular empty-Tw NStage model cannot supply NChoice.twI from
the nonempty coefficient-place set, even off the nonreference support.
This proves incompatibility of that particular auxiliary construction,
not nonexistence of other compatible stages. The zero projector on a
one-dimensional Mt also cannot give a positive projector-rank bound.
The shaLen.toNat assignment does not prove Sha finite. Both pins are
proved in normal form from existing sized/oriented data; their normalization
does not supply the initial geometry or prime/window hypotheses.

REMAINING WORK
'''+''.join(f'{i+1}. {x}\n'for i,x in enumerate(cfg['remaining_major_inputs']))+f'''

VERIFICATION SCOPE
The current ledger has {len(ledger['claims'])} claims and
{sum(len(c['sources'])for c in ledger['claims'])} claim-source links.
Its source index has {len(ledger['source_files'])} pinned files; including
the {len(targets['targets'])} next-target ranges gives {len(paths)} distinct
source files. The human graph is acyclic, with all historical edges retained.
Draft-mode TeX passed with {tex['passes']} passes, zero undefined references
or citations, and zero missing-character warnings. There are
{tex['overfull_box_warnings']} retained layout warnings for any future
rendering round. No PDF or visual-layout certification is claimed.

Provenance SHA256: {sha(ROOT/'provenance.json')}
TeX SHA256: {sha(ROOT/'RH_readable_reconstruction_v0_17.tex')}
Next-target SHA256: {sha(ROOT/'next_source_targets.json')}
'''
(REV/'final_scope_review.txt').write_text(report)
print(json.dumps(dict(result='PASS',new_claims=len(expected),independently_reviewed=len(seen),review_records=len(records))))
