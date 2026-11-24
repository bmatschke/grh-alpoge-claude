#!/usr/bin/env python3
"""Record independent review coverage and the precise v0.18 joins."""
from pathlib import Path
import hashlib,json,re
ROOT=Path(__file__).resolve().parent;REV=ROOT/'reviews_v0_18'
def read(p):return json.loads(p.read_text())
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def ids(p,ns):return[p+str(i)for i in ns]
coverage=[
 ('root_reviews_initial_geometry.txt','/root','initial_geometry',ids('IG',range(1,15))),
 ('root_reviews_arithmetic_compatibility.txt','/root','arithmetic_compatibility',ids('RC',range(1,22))),
 ('root_reviews_local_stages.txt','/root','local_stages',ids('LS',range(1,23))),
 ('theta_descent_TD1_8_review.txt','/root/class_rank','theta_descent',ids('TD',range(1,9))),
 ('theta_descent_TD9_16_review.txt','/root/global_frame','theta_descent',ids('TD',range(9,17))),
]
extra=[('ig_reviews_ls_1_8.txt','/root/comparison_span','local_stages',ids('LS',range(1,9)))]
ledger=read(ROOT/'provenance.json');targets=read(ROOT/'next_source_targets.json');cfg=read(ROOT/'increment_v0_18.json');tex=read(ROOT/'tex_validation.json')
assert tex['syntax_compile_succeeded']and not tex['pdf_generated']
assert not tex['undefined_references_or_citations']and tex['missing_character_warnings']==0
expected={c['id']for c in ledger['claims']if c.get('introduced_in')=='0.18'};seen=set();records=[]
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
out=dict(artifact_version='0.18',result='PASS',new_claims=len(expected),covered_new_claims=len(seen),method='Independently authored scoped mathematical/source reviews checked against current proof paragraph hashes. This bookkeeping is not an automated proof checker.',review_records=records,no_lean_build_or_kernel_replay=True)
(REV/'mathematical_review_coverage_v0_18.json').write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n')
paths={s['path']for s in ledger['source_files']}|{s['path']for s in targets['targets']}
report=f'''FINAL SCOPE AND MATHEMATICAL JOIN REVIEW: VERSION 0.18
Result: PASS within the explicit reconstruction scope
Date: {cfg['date']}
Pinned source: {ledger['commit']}

This is a cumulative human-readable reconstruction with exact source
provenance. It does not assert a complete proof of RH or Dirichlet GRH.
Background facts, conditional input objects and quantifier order remain
explicit. Independent mathematical review and source-range hashing are
distinct from a Lean build or kernel replay; neither was performed.

NEW COVERAGE
All {len(expected)} new claims are independently reviewed: RC1–RC21,
LS1–LS22, IG1–IG14 and TD1–TD16. The initial local period construction
LS1–LS8 also has an overlapping review. Coverage records bind reviews
to exact current paragraph hashes. All 747 predecessor claim records,
their original fields and old graph adjacency lists remain unchanged.

ARITHMETIC COMPATIBILITY
Finite evaluations justify the finite scalar-extension argument on the
actual form space, rather than assuming scalar extension commutes with
an infinite product. MtReal/NExpTied, exact weight matching and level
identification give RankTie. Global reciprocity and NTw.art_univ remain
named substantive inputs to the finite character construction. The
Frobenius detection proof uses precisely their uniformizer convention
and weak approximation; no Chebotarev premise is silently imported.
Exact ramification and decomposition triviality at ell are different
properties and are both checked. Primitive-root changes give the exact
normalized packet's prime-to-ell power relation, including side signs.

The local IsGalOf criterion yields equality of actual characters through
their injective coefficient maps, then equality of conductor sets.
Open kernels supply continuity of these finite-image character maps;
no continuity of a Qbar_ell-to-C isomorphism is assumed. Compatible
local index/side choices remain. The global choice theorem needs an
all-place reading; RC20's coverage selector supplies readings only at
twisted places. The empty-Tw stage cannot fill either missing input.

The local level comparison proves scalar-action parahoric rigidity,
orientation through opposite-parabolic indices, and additive character
rigidity through a prime-to-p quotient. The actual explicit integral
frame kills the rational stabilizer and supplies nonzero forms.
Joint and CellWt remain exact realization inputs. The MuW reset is a
bare row operation; it is not asserted to transport a geometric RowPk.
MuIsW is proved on the actual ColW/Pre2/St lift using its defining
equalities, and all ten fields and the same frame/Q/xi/psi join are kept.

RC21 first chooses finite integral subbases from the actual generating
theta vectors, then handles every forbidden set. Faithful flatness,
Noetherianity and the minimal-generator DVR argument are explicit.
Prime-support enlargement and finite induction give pairwise Apart.
The genuine aux3/GoodTw lattice-index bounds, FullRank, adm7 and setting
hypotheses remain; finite avoidance is not substituted for them.

ACTUAL PERIOD RINGS AND THE BARE STAGE
LS gives the orbit-halving Ax estimate, bounded cyclotomic projections
and all nonzero Tate-twist invariant vanishing, including p=2. It uses
the actual inverse limit and Witt ring, proves the theta kernel and
p-saturation, and constructs the de Rham DVR and algebraic coefficient
section. The actual divided-power completion embeds through a bounded
mod-xi construction whose injectivity is separately proved. Integral
logarithm estimates include the dyadic case. No topology of an arbitrary
coefficient-field embedding is invoked.

The Frobenius coefficient induction keeps its auxiliary coefficient,
all index inequalities and both ideal-power cases. Its consequence for
the completion is proved through the de Rham injection. The integral
fixed ring, simultaneous theta vanishing and eigenvector/filtration
induction give exactly Bcris^{{phi=1}} intersect BdR+ = Qp. The crystalline
invariant field follows from periodic Frobenius, interpolation on an
unramified root orbit and that fundamental intersection; it does not
assume a crystalline representation-comparison theorem.

All PeriodData, LocPrime, LocAinf and LocTied duties use the same rings,
maps, filtration, period and prime. The source's bare NStage is then
constructed with actual cyclotomic LData, prime labels, residue maps
and tame generators, but empty local and twist indices. Nonvacuous
fields are supplied before empty universal statements are used.
The zero good projector agrees with the exact adapted row operators.
Together with SE this closes bare Later on that same object.

The conclusion has a concrete limit: a coefficient number field has
a prime above 2, so NChoice.twI cannot map all coefficient primes into
the constructed empty twist type. This is an incompatibility of that
particular auxiliary construction, not nonexistence of other stages.
Zero projections do not supply positive projector ranks. The shaLen
toNat assignment does not prove Sha finite.

ORIGINAL GEOMETRY AND THE QUANTITATIVE BOUNDARY
IG constructs shifted-lattice partial ray zeta functions with common
positive residue and their value at −1. A hypothetical nontrivial zero
at 1 makes the full character product entire; its nonnegative Taylor
expansion contradicts the zero at −1. Euler logarithms and exclusion
of the convergent degree-two prime contribution yield qualitative
unbounded prime norms. This does not supply a prescribed short interval,
uniform error bound or quantitative LevelPrime theorem.

The actual cyclic host, integral norm factors, disjoint BB sets,
two explicit HC word columns, type prime and finite-adelic diagonal
spaces supply every original PreX field. The finite genus mass-index
and integral Vandermonde argument give positive integer duStarOf.
The source intentionally restricts to one word before resetting the
window scale; the lower endpoint is then exactly T. Orientation and
pins are on that same constructed datum, not an arbitrary fixed frame.

The literal positive-choice trueVol definition gives the specified
baseVol/noJet stage, including its fallback branch. It does not identify
that number with a geometric covolume without a VolIs witness.
The recursive-existence join preserves the order of its thresholds,
chooses du/Ds before every supplied level, and transports the dependent
pair equality before forming BPt. Quantitative window_lower, actual
full frame, V4.Core, volume/mass and all nine RecOK duties, as well as
LedOK integral NP comparisons, remain explicit.

RATIONAL THETA TARGET AND METRIC
TD recovers fixed-field coordinates from finite common tests, descends
the actual adjoint image through the exact Gram matrix, and proves
stability from adjoint closure. Finite group equivariance extends by
the stated coefficient embedding; the group-algebra adjoint identity
is summed from group-element identities. Rational idempotent cuts need
no unasserted self-adjointness. The row/lift characters retain their
inverse convention.

Positive theta theta* identities on spanning type parts construct a
common image explicitly. Exact rational row/lift matrices then follow
from one common test family, with the actual principal basis included
in LiftTestB. The nP Gram factor, distinguished-place metric splice and
literal principal lattice are retained. For orthogonality the actual
quotient metric is proved via orthogonal lifts; an arbitrary section
zE is not assumed isometric. Positive weights yield the precise metric
lower bound, but no quantitative estimate for those weights.

The common test normalization uses rational ratios and finite sums
from the same period formula. It separates the kappa=0 case instead
of dividing by a possibly zero scalar. Boolean conjugation acts on both
scalars and values, and the Big thresholds are combined in their
literal order. Algebraicity alone is insufficient for this fixed-field
condition, as the {{1,i}} over Q counterexample demonstrates. Primitive
convergence/separation/period/ratio and theta operator/type suppliers
remain the next inputs.

CURRENT REMAINING WORK
'''+''.join(f'{i+1}. {x}\n'for i,x in enumerate(cfg['remaining_major_inputs']))+f'''

VERIFICATION
The cumulative ledger contains {len(ledger['claims'])} claims and
{sum(len(c['sources'])for c in ledger['claims'])} exact claim-source links.
The index contains {len(ledger['source_files'])} pinned source files;
including {len(targets['targets'])} next-target ranges requires {len(paths)}
distinct source files. The human graph is acyclic and all historical
edges remain. This is not a transitive Lean dependency audit.

Draft-mode TeX validation completed in {tex['passes']} passes, with no
undefined references/citations or missing characters. It retained
{tex['overfull_box_warnings']} layout warnings for a future rendering
round. No new PDF or visual-layout certification is asserted.
Every predecessor package file is preserved and its manifest checked.
All old source records and claim fields are unchanged; additions have
explicit version_0_18 annotations.

Provenance SHA256: {sha(ROOT/'provenance.json')}
TeX SHA256: {sha(ROOT/'RH_readable_reconstruction_v0_18.tex')}
Next-target SHA256: {sha(ROOT/'next_source_targets.json')}
'''
(REV/'final_scope_review.txt').write_text(report)
print(json.dumps(dict(result='PASS',new_claims=len(expected),independently_reviewed=len(seen),review_records=len(records))))
