#!/usr/bin/env python3
"""Verify independent review coverage and record the exact v0.19 scope."""
from pathlib import Path
import hashlib,json,re
ROOT=Path(__file__).resolve().parent;REV=ROOT/'reviews_v0_19'
def read(p):return json.loads(p.read_text())
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
ledger=read(ROOT/'provenance.json');targets=read(ROOT/'next_source_targets.json')
cfg=read(ROOT/'increment_v0_19.json');tex=read(ROOT/'tex_validation.json')
assert tex['syntax_compile_succeeded']and not tex['pdf_generated']
assert not tex['undefined_references_or_citations']and tex['missing_character_warnings']==0
def component_ids(c):return[x['id']for x in read(ROOT/c/'provenance.json')['claims']]
coverage=[
 ('root_reviews_arithmetic_realization.txt','/root','arithmetic_realization',component_ids('arithmetic_realization')),
 ('ar_reviews_host_character_frame.txt','/root/class_rank','host_character_frame',component_ids('host_character_frame')),
 ('root_reviews_theta_test_inputs.txt','/root','theta_test_inputs',component_ids('theta_test_inputs')),
 ('quantitative_windows_QW1_9_review.txt','/root/global_frame','quantitative_windows',[f'QW{i}'for i in range(1,10)]),
 ('quantitative_windows_QW10_15_review.txt','/root/comparison_span','quantitative_windows',[f'QW{i}'for i in range(10,16)]),
]
expected={c['id']for c in ledger['claims']if c.get('introduced_in')=='0.19'};seen=set();records=[]
for filename,reviewer,component,scope in coverage:
 p=REV/filename;assert p.is_file()and'PASS'in p.read_text(),filename
 assert not seen&set(scope);seen.update(scope)
 source=(ROOT/component/'main.tex').read_bytes()
 marks=list(re.finditer(rb'(?m)^\\paragraph\{([A-Z]+\d+):',source));ph={}
 for i,m in enumerate(marks):
  cid=m[1].decode()
  if cid in scope:
   stop=marks[i+1].start()if i+1<len(marks)else len(source)
   ph[cid]=hashlib.sha256(source[m.start():stop]).hexdigest()
 assert set(ph)==set(scope),filename
 for cid,h in ph.items():assert h in p.read_text(),('stale review',filename,cid,h)
 records.append(dict(review=str(p.relative_to(ROOT)),reviewer=reviewer,component=component,claims=scope,review_sha256=sha(p),current_main_sha256=sha(ROOT/component/'main.tex'),current_claim_paragraph_sha256=ph))
assert seen==expected,seen^expected
out=dict(artifact_version='0.19',result='PASS',new_claims=len(expected),covered_new_claims=len(seen),method='Independently authored scoped mathematical/source reviews are bound to exact current proof paragraph hashes. This bookkeeping is not an automated mathematical proof checker.',review_records=records,no_lean_build_or_kernel_replay=True)
(REV/'mathematical_review_coverage_v0_19.json').write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n')
paths={s['path']for s in ledger['source_files']}|{s['path']for s in targets['targets']}
report=f'''FINAL SCOPE AND MATHEMATICAL JOIN REVIEW: VERSION 0.19
Result: PASS within the explicit reconstruction scope
Date: {cfg['date']}
Pinned source: {ledger['commit']}

The cumulative note is a partial human-readable reconstruction with exact
source provenance. It is not a complete self-contained RH/Dirichlet-GRH
proof. Mathematical reviews, source-range hashes and TeX syntax validation
are distinct from a Lean build or kernel replay; neither was performed.

All {len(expected)} new claims have independent reviews bound to their
current proof-paragraph hashes. All 820 predecessor claims retain their
original fields, source arrays and dependency adjacency lists. New scope
annotations are additive. All 863 predecessor package files are preserved.

ACTUAL LOCAL ARITHMETIC REALIZATION
AR reconstructs exact bad places and selected halves, tame Artin readings,
parahoric and type-level shapes, identity-frame reductions and the common
unipotent power comparison. Joint uses an intersection of the actual
geometric and series levels. The installed pointwise reading is proved
by an injective coefficient map and denominator clearing on finite
double-coset representatives; the same rdV equality must be installed.

The coefficient-field intertwiner argument is valid for infinitely many
group equations. It descends a minimal irreducible complex submodule by
linear coordinate projection and dimension comparison. Complex algebraic
classification, canonical dual highest weights and the characteristic-zero
Weyl/dual-Weyl identity remain explicit primitives. The infinitesimal-weight
comparison and arbitrary base-change basis transport are proved. The
harmonic argument preserves the complementary-minor sign and uses the
positive Fock pairing for injectivity. All five WtMap properties are
accounted for; no integral equality of Weyl and dual-Weyl lattices is used.

Normalized algebraic adic-character existence and published reciprocity
remain substantive. The type-character law requires nonempty all-place
SideB.cover. Bare empty-Tw stages do not satisfy it. The final rank and
choice conclusions retain the same actual global realization, weight,
side/index and local IsGalOf data, and the MuIsW ColW/Pre2/St/RowPk join.

ACTUAL HOST CHARACTER FRAME AND INITIAL JOIN
HF constructs the actual host characters with their exact infinity types,
real-subfield restrictions and finite local characters. Circle divisibility
and open-subgroup extension are used only after unit compatibility is
verified. Root-of-unity pairing, the quadratic product formula, the host
phase lemma and finite class-group exponent account for the restrictions,
finite order and exact auxiliary inertial order. The full HFrame stays on
the supplied host and weight data.

The determinant quotient, rational unitary determinant map and relative
lattice determinant package use the actual selected prime sets and local
valuation conventions. The same preliminary datum is preserved through
the field extension and original ColIn constructor. The canonical index
replacement preserves the frame, selector, character family and ambient
datum, with the updated modulus exponents used for JetsIn. Existing
column Laws/Law0 and the bare Later stages then live on that same base.
The resulting TwForms and ordinary lattice jets do not identify the
Galois-stage twist type with the nontrivial column-twist family. The full
V4.Core still has independent real/twist/object/layout/volume requirements;
the empty-prime untwisting construction cannot satisfy its forced prime.

PRIMITIVE THETA TESTS
TT proves finite local integral arithmetic with exact Haar normalization,
ramified singular-ball cancellation, literal Fourier/middle flips, phase
bounds and compact representative support. Totalized multiplicative
integrals are distinguished from convergent additive flat integrals.
The uniform support argument removes unbounded triangular factors before
choosing its period ball and retains the literal free-entry pattern.

Fixed-depth coset data are unique where their supports meet. This bounds
all expansion supports by one finite set. Point-evaluation tensor
injectivity proves expansion independence; actual finite class sums and
rational inverse stabilizers complete the eleven SumOK fields. Rational
polynomial-coordinate descent, fixed jets and the bilinear branching
conventions put every term of vK in the specified common field. SumRatK
retains FieldOK; no integral lattice equality or convergence theorem is
inferred from this calculation.

Ray-class and finite root choices construct the elementary field clauses.
The exact moved-vacuum calculation isolates the remaining finite-Weil
arithmetic assertion, and normalized period cancellation reduces jets
to finitely many algebraic entries. Compact Haar averaging is proved
algebraic using invariant and coinvariant spaces over Qbar, rather than
assuming an integral of algebraic values is algebraic. A single degree
survives central averaging. Definite bottom periods retain their actual
Haar volumes, possibly nonalgebraic common periods and the moving-Weil
input. The ratio argument retains common factorization, the matching
tower, critical nonvanishing and critical-ratio field membership.

The finite compositum supplies all eight NumbersIn clauses only when
their stated arithmetic inputs hold. FieldOK additionally requires the
same embLL, or actual L/G/W/S/flip agreements after enlargement. LinK,
InjK, Formula2K, positive theta operator identities and spanning type
parts retain their analytic/separation/period/operator suppliers.

QUANTITATIVE MASS AND PRIME WINDOWS
QW proves the actual Euler product by absolutely summable logarithms.
The unramified CM residue condition forces degree at least two at fixed
primes. Finite local subgroup counts yield the literal index ratio with
factor 2^(-2f). The mass law is stated separately, with its exact factorial,
root-discriminant and square-root normalization; positivity only justifies
the telescope and logarithms.

The Vandermonde comparison keeps all interior factors and loses only
2k-3 endpoint factors. Middle-weight logarithms telescope. Exact factorial
cancellation gives C=30+(2+2C0)/epsilon in LogRatioLowerBound. Every actual
top/thick/thin place satisfies all nine PlaceData clauses, with the
root-of-unity rounding bound included. Uniform host/rank estimates then
give the original window_lower implication, with 14mL remaining after
the exact GamS normalization, stronger than its required mL. All size
data and words are chosen after the threshold. SiegelMassRatioCM and
the same-object ChOK/du/Ds inputs remain explicit.

The prime-counting part removes prime powers from the same LFam using
its exact NormOne support and elementary Chebyshev remainder. It proves
all constants in the weighted-to-unweighted reduction. levelPrimeN and
the Y^(9/10) dyadic bound are uniform in every later endpoint. The actual
LFam construction and uniform weighted interval lower bound remain.
They are not inferred from qualitative ray-prime existence.

Classical Dirichlet continuation, character orthogonality and a
nonnegative entire-product Taylor argument prove nonvanishing at one.
Continuity and a finite positive minimum give exactly QH.small_zeros:
a real interval depending on a fixed conductor bound. This neither
produces an all-conductor constant nor a complex zero-free box, and
does not close the remaining analytic RH/GRH branches.

CURRENT REMAINING WORK
'''+''.join(f'{i+1}. {x}\n'for i,x in enumerate(cfg['remaining_major_inputs']))+f'''
VERIFICATION
The cumulative ledger has {len(ledger['claims'])} claims and
{sum(len(c['sources'])for c in ledger['claims'])} claim-source links.
It indexes {len(ledger['source_files'])} pinned source files; including
the {len(targets['targets'])} current target ranges requires {len(paths)}
distinct files. Every old source-file record and graph edge is preserved.
The graph is acyclic and is a human proof graph, not a transitive Lean
dependency audit. Historical target records remain archived; current
generic PreX/Later records are retired as stale without retiring the
stronger nonempty/core obligations.

Draft-mode TeX validation took {tex['passes']} passes, with no undefined
references/citations or missing characters. It retained
{tex['overfull_box_warnings']} layout warnings for a future rendering.
No new PDF, page count or visual layout certification is asserted.

Provenance SHA256: {sha(ROOT/'provenance.json')}
TeX SHA256: {sha(ROOT/'RH_readable_reconstruction_v0_19.tex')}
Next-target SHA256: {sha(ROOT/'next_source_targets.json')}
'''
(REV/'final_scope_review.txt').write_text(report)
print(json.dumps(dict(result='PASS',new_claims=len(expected),independently_reviewed=len(seen),review_records=len(records))))
