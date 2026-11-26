#!/usr/bin/env python3
"""Write the mathematical progress report and the precise continuation plan."""
from pathlib import Path
import collections
import hashlib
import json

ROOT=Path(__file__).resolve().parent
def read(name):
    return json.loads((ROOT/name).read_text())
cfg=read('increment_v0_46.json')
stats=read('integration_stats_v0_46.json')
tex=read('tex_validation.json')
assert tex['artifact_version']=='0.46'
for item in tex['documents']:
    assert item['tex_sha256']==hashlib.sha256((ROOT/item['tex_filename']).read_bytes()).hexdigest()
    assert item['syntax_compile_succeeded'] and not item['undefined_references_or_citations']
    assert not item['missing_character_warnings']
new=[c for component in cfg['components'] for c in read(component+'/provenance.json')['claims']]
categories=collections.Counter(c['classification'] for c in new)
head=[
 'RH AND UNRESTRICTED DIRICHLET GRH — HUMAN RECONSTRUCTION v0.46',
 '23 November 2026','','CURRENT RESULT','',cfg['status'],'',
 'Two whole selected obligations are completed: CNR3, the original rank-three '
 'congruence-number assertion; and TASK_PROP_GK_INSTALL, the exact finite '
 'implication from CNR3 and the original OneChar theorem to PropGK. The latter '
 'is an implication task. The separate arithmetic proof of OneChar remains '
 'open, as do RIG_II and the surrounding unconditional case producers.','',
 'The other new chapters prove the original arithmetic row structure on given '
 'data, finite generation of the whole integral cusp lattice, and the entire '
 'remaining logarithmic counting theorem. Exact conditional lattice-spanning '
 'and local-to-global gain arguments are also written out. The cumulative '
 'human-readable proof is still incomplete.','',
 'The complete ZIP includes all preceding work, five new proof chapters, '
 'source snapshots and exact ranges, claim/dependency ledgers, independent '
 'mathematical and integration reviews, validation records, and the current '
 'continuation plan. Both readers are TeX; a PDF is not required for this '
 'release.','','INVENTORY','',
 f"New claims: {stats['new_claims']} ({dict(sorted(categories.items()))}). Cumulative claims: {stats['cumulative_claims']}.",
 f"Predecessor claim records preserved: {stats['cumulative_claims']-stats['new_claims']}.",
 f"Selected graph: {stats['selected_nodes']} nodes and {stats['selected_edges']} edges.",
 f"Remaining whole obligations: {stats['open_count']} ({stats['open_categories']['C']} C and {stats['open_categories']['B']} B).",
 f"Shared RH/Dirichlet-GRH obligations: {stats['shared_open']}; additional Dirichlet-GRH obligations: {stats['extra_grh_open']}.",
 f"New increment source inventory: {stats['new_source_files_checked']} pinned files and {stats['new_unique_source_ranges_checked']} distinct ranges.",
 'Claim counts are an inventory, not a completion percentage. Class A marks '
 'a checked published application; class B marks a written proof in its stated '
 'scope. Conditional and eventual hypotheses remain explicit.','','THE FIVE NEW CHAPTERS','',
]
for i,(component,description) in enumerate(zip(cfg['components'],cfg['local_conclusions']),1):
    claims=read(component+'/provenance.json')['claims']
    head.extend([f"{i}. {claims[0]['id']}–{claims[-1]['id']} ({len(claims)} claims)",
                 'Proof: '+component+'/main.tex',description,''])

discussion='''THE RANK-THREE INTEGER: WHY A FINITE CATALOGUE IS ENOUGH

Fix the original imaginary quadratic field K. The source needs constants
depending only on K, then one nonzero integer for every weight e, level N,
prime p and finite indexed root-of-unity orbit. That integer must work for
every later coefficient prime, closure, embedding and admissible finite
collection. Choosing a new integer after choosing the coefficient prime
would not meet this contract.

The proof first builds two finite catalogues of full cuspidal representations.
The first comes from the original rank-three admissible representation rho
after the exact cyclotomic twist r=rho*epsilon^(-1). The second comes from
the actual newform in the rank-two alternative. The latter is adelized
directly over Q, and the twist |det|^(1/2) makes its geometric Satake roots
p^(-e) times the two roots of the original newform Hecke polynomial. This
avoids an unnecessary general-rank detour.

The local ordered flags identify the highest weights as

     lambda_3=(e-1,0,1-e),       lambda_2=(e-1,-e).

The use of the automorphic Galois theorem is staged carefully. General
regular-algebraic polarized existence first gives a representation that
is identified with the original one by cofinite Frobenius comparison.
The flag then identifies the weight. Only after this step is full
coefficient-prime compatibility invoked in its Shin-regular scope:
rank three is odd, and the rank-two difference is 2e-1>0. The proof does
not impose a new coefficient-prime lower bound or an Iwahori condition.

The original level contains a useful disjunction. Either no two flag
characters differ by a cyclotomic factor, or the representation is
potentially crystalline. A nonzero monodromy entry would force exactly
such a factor. In the other alternative, potential crystallinity and full
local compatibility give zero monodromy. Thus places outside the original
level do not acquire an extra coefficient-prime factor. The finite inertia
conductors and at most n-1 additional monodromy contribution give auxiliary
automorphic levels M^5 in rank three and M^3 in rank two. These auxiliary
levels bound the catalogues; they do not change the original Galois level.

A fixed torsion-free level-three arithmetic quotient has a finite cell
model. Passing to level3L multiplies the number of cells by at most a fixed
polynomial in L. The explicit highest-weight modules have polynomially
bounded ranks, obtained from polynomials in nine or four matrix coordinates.
Cuspidal cohomology then bounds the number of full cusp classes. The resulting
catalogue bounds have exponents90 and12 in N(e+1), with the original
discriminant factor in the rank-two alternative.

The catalogues are stable under every automorphism of C. The normalization
check is essential: if A_v=q_v^((n-1)/2) Sat_v is the geometric multiset,
then its j-th elementary symmetric function is

                    e_j(A_v)=q_v^(j(j-1)/2) T_(v,j).

The exponent is integral. Thus scalar conjugation of the rational Hecke
correspondence conjugates the algebraic roots without requiring an arbitrary
automorphism to fix a chosen square root of q_v. Full labels are retained,
even if two labels have the same trace at the chosen place.

Purity bounds each resulting rank-three comparison trace t by3. Integral
lattices at coefficient primes different from p, and both Newton/Hodge
endpoint bounds at p, show that q^e t is integral. For a root of unity z,
put

          E(q,e,z)=q^(-e)z+1+q^e z^(-1),
          F(t,z)=q^e(t-E(q,e,z)).

Since q>=7 and e>=1, |E|>=q^e-1-q^(-e)>3, so F is nonzero. Its expansion
q^e t-z-q^e-q^(2e)z^(-1) is integral, and log|F|<=2e log q+1.
The product of F over every indexed orbit member and every catalogue label
is fixed by every complex automorphism. It is consequently a nonzero
rational integer. Repeated orbit values are counted with their original
indices, and empty index sets give the integer1.

For any later coefficient prime ell!=p, each factor has ell-adic norm at
most1. The classifier is injective on each original pairwise-nonisomorphic
collection. Deleting unselected factors can only increase the product of
norms; the q^e multiplier is an ell-adic unit. This proves the exact
source product inequality with the already chosen integer. One permissible
uniform exponent is A=103; no optimization is needed for the reconstruction.

The PGK chapter then performs the entire finite consumer. Its length
estimate still comes from the original OneChar premise. Closing this
consumer is useful because the remaining OneChar theorem can now be
inserted into a fully written finite argument without revisiting the
catalogue, orbit or valuation construction.

ARITHMETIC ROWS: THE ORIGINAL NORMALIZATION AND ONE LABEL OBJECT

ARO works with the adelic SG.HidaSetting that carries the arithmetic rows.
This is a different record from the ordinary-Hecke Hida setting used in
the earlier support chapters. It keeps the original stabilizer K, level
N=K(g), both split primes, characters, measure and formal degrees.

The reduction map rho:K->G is constructed on the actual local lattices.
Its exact kernel is N, and its image is the entire finite product. With
V=mu(N), each fiber has volume V. If a finite group-algebra element a is
inflated as f(x)=a(rho(x))/V, then the transform is

                         hat f(gamma)=V f(x_gamma).

The convolution calculation contains two compensating V factors, one from
the fiber integral and one from the transform. Involution has the same
normalization. Keeping V here is what allows the later projector traces,
formal-degree expressions and cylinder counts to refer to one measure.

In a basis adapted to the original four-block frame, the concrete level
subgroup becomes the prescribed unipotent subgroup with its exact forbidden
entries. A direct reverse-flag argument and the Chinese remainder theorem
give both directions, including both conjugate orientations. The original
adelic additive character factors through nontrivial characters at the two
prime fields. Complete splitting makes the absolute trace calculation
especially simple; it proves nontriviality for the actual character rather
than selecting an unrelated one. This identifies the original projector
with the finite tensor of character idempotents.

The finite event idempotents therefore obey the full intersection, total
sum, self-adjointness and positivity laws. Invalid labels contribute zero,
so arbitrary subsets reduce to finite sums. The literal EtOne cylinder
identity follows with the same V. The integral operators are then bounded
on the original quotient Hilbert space, and the actual ReT specification
is realized with the correct convolution order.

At infinity, Schur orthogonality and the already reconstructed discrete
series input produce a rank-one compression. Evaluation at the original
unit vector identifies bounded intertwiner spaces with the exact projector
image. This gives finite-dimensional multiplicities under the original
RowsFinDim input and proves their additivity over finite events.

The actual good rows are kept as a distinguished subset. The original
semilinear row dictionary is handled with its conjugation convention, and
the label tie identifies the multiplicity of each good type. A single
finite completion then adds the missing nongood labels with their required
multiplicity. It preserves every original good index and allows repeated
labels. This one AllRows object is chosen before any event is selected.

The remaining count theorem is a genuine arithmetic input. The packet
checks every argument needed to apply it: the complementary unipotence
prime, the intersection volume, the common signature at every infinity
place, b and h, the gap and discriminant conditions, and the same formal
degrees. Under the literal CountIdempotentsClass theorem it obtains all
cylinder counts on the same object. The earlier finite local weight theorem
and retained-defect consumer then apply directly. Existence of the common
setting/ties and the counting theorem is not inferred from row algebra.

INTEGRAL CUSP LATTICES: FINITE GENERATION AND THE PRECISE SPANNING FRONTIER

The lattice is the whole set of original rational cusp rules that have
nonnegative normalized valuation at every permitted integral-frame test.
Showing that a convenient submodule is finite would be insufficient.

The finite-generation proof constructs a nonzero integral-frame evaluation
for every nonzero rational cusp rule. Rational Hermitian flags are dense,
so one may choose an actual CM point where the rule is nonzero. The named
CM and abelian-scheme foundations give a finite extension with an
everywhere-good model and the original rigidified line. The Lie eigenmodules
are full kernels, including at ramified primes. They are projective and
become free after principalizing finitely many ideals. No integral direct
sum decomposition at ramified primes is assumed.

Integral elementary changes of frame and root-of-unity diagonal changes
are Zariski dense in the frame group. One such frame therefore retains
the nonzero value. Every element of the entire lattice evaluates there
to an algebraic integer, because the same model supplies every finite-prime
test. A finite separating family of these evaluations embeds the lattice
in a finite product of rings of integers. Noetherianity gives finite
generation. Scalar-extension injectivity is proved on the original reduced
test rings, so finite-dimensionality is not borrowed from a theta spanning
statement. The zero cusp space is included.

Spanning requires more. The manuscript now gives a complete implication
from five precisely stated original inputs: principal charts; the actual
finite-level system; raw Gaussian kernel/reproduction estimates; short-rule
gluing and its simultaneous dictionary; and ramified integral jet bounds.
The identity cover is supplied directly given the original IsNab connection,
which remains an explicit input. It does not assert a higher cover.

For the analytic part, the class-sum operator is a scalar times1+Q with
norm(Q)<1, giving an explicit Neumann inverse. The raw kernel identity is
unfolded using the actual free lattice/frame action and the original
measure. Absolute summability is checked before interchanging sums and
integrals. A finite evaluation-matrix argument proves integrability of the
finite-rank coefficients, rather than assuming it term by term. Integral
harmonic polynomials span after clearing finitely many coefficients, and
the original-field reading argument descends the final coefficients back
to K. The same scalar works across all original components.

For the integral part, the retained jet bound and exact finite average
give one global scalar. If d_w is the original nonnegative degree, M the
squarefree level, c_0 the original finite averaging cardinality, and
Delta_E=|disc(E)|, a sufficient choice is

     A_w=(product_(p|condN) p)^(Delta_E*d_w) M^d_w c_0,
     s=A_w*betaH.

Its valuation cancels every permitted local denominator. The normalized
valuation is unchanged through the auxiliary extension, so this proves
the statement for the original test. The scalar is fixed before the place
and frame. Finally a positive power reaches the stable theta range. If
t f^q is integral everywhere with t integral, then tf is integral everywhere:
for a=ord(t)>=0 and x=v(f), a+q x>=0 implies a+x>=0. No root of t or change
of the original coefficient field is required.

This gives conditional FullAt/LatFull and exact transport through FWTie
to both original Boolean levels. The five producer inputs, higher covers,
all-tuple class sums/uniqueness, common PointIdentCore and base ClassSumsSpan
remain visible. Finite generation alone is not called a full lattice.

GLOBAL LOCAL GAIN: AN ACTUAL UNIFORM COUNT AND AN EXACT INSTALLER

GLG proves the original RemainingCountingStatement on every admitted
instance family. Its constant is selected before that family; its threshold
is uniform in all later members, primes, lifts and top functions. The top
weights b_s have their original lower bound and no new upper bound.

The finite argument uses positive-part and minimum sums over odd powers
of p. Their sum is the odd geometric series p/(p^2-1). On a candidate
cyclic orbit, each odd top with an even predecessor is assigned its nearest
such predecessor and the odd backward distance. This assignment is
injective into the actual even-top minimum sum. It cancels the potentially
large top term in the large-prime range; this is why no upper bound on b_s
is needed.

The two original prime ranges retain separate exact losses and ceiling
budgets. The common asymptotic estimate uses

      beta=23 epsilon/48 < epsilon/2,
      Z=exp(x^beta),
      b_o=b^(x^(-epsilon/2))=exp(x^(epsilon/2)).

Every remaining numerical budget is bounded by Z^13 after one threshold,
and Z^13<=b_o eventually. The proof retains the original coefficient1 of
b_o. A final increase of the chosen constant by1 pays for the exact
askP-to-askG shift. This proves the full source counting conclusion, not
only one window or one selected member.

The local-to-global chapter also supplies several exact structural pieces.
The integral local operators preserve both the dual-Weyl and Weyl models;
the latter is proved from homogeneous divided-power generators. Rational
coefficient evaluations and a K-linear retraction of the comparison field
give the original operator descent without assuming a Galois extension.
Faithful flatness over the original coefficient DVR then transports finite
sums, images and the precise intersections defining NPDesc.

The normalized length is checked on the actual lattices. If e_w is the
valuation of p in the original local field and a_w is the relative
ramification factor in the comparison DVR, then v_O(p)=a_w e_w. Each Smith
exponent scales by a_w, giving exactly

        length_O((M cap U_F)/P)=v_O(p)*lenMN(u,w).

This prevents an incorrect ramification factor from entering the global
inequality. Served-index coverage, the precise S_v bound, unserved zero
lengths and the selected-top admissibility implication are also supplied.

The five-conjunct LinkG installer now follows on the original common
objects, with constant4|C|+1 and the exact global loss comparison. At the
family level one can use delta_G(x)=x^(-epsilon/2). The common compatibility
record, the full admitted inputs, the local first-growth estimate and the
mean-deficit hypotheses still have to be realized on that same family.
They are explicit premises of this completed installation argument.

VALIDATION AND REPRODUCIBILITY

Each new claim has an independent mathematical/interface review by an
agent other than its author. Focused reviews cover disjoint portions of
some chapters; the final registry verifies coverage of every new claim,
whole-file hashes and exact block hashes. The two selected closures are
separately checked against the complete predecessor contracts.

The integration audit checks predecessor preservation, exact claim and
source records, acyclicity, literal selected-route changes, source snapshots,
and current continuation metadata. A separate semantic review checks that
completed implications are not presented as input-producing theorems,
including the OneChar, common-family, integral-spanning and local-growth
boundaries. All these records are included in the ZIP.

The complete preceding historical proof body and all predecessor claim records
are retained verbatim. Mutable root metadata from v0.45 is frozen in
history/version_0_45. Draft TeX compilation checks syntax, references and
missing characters. No PDF visual review or Lean/kernel replay is claimed.
The underlying formal proof is accepted as correct for this reconstruction.

NEXT WORK, ALREADY AUTHORIZED

Continue towards the full human-readable proof. The current whole-obligation
register supersedes historical frontier descriptions. Reuse completed
construction and implication chapters, while retaining their exact
antecedents until the corresponding producer is actually reconstructed.
'''
tail=[]
for i,target in enumerate(cfg['next_targets'],1):
    tail.extend([f'{i}. {target}',''])
tail.extend(['COMPLETE REMAINING MAJOR INPUTS',''])
for i,target in enumerate(cfg['remaining_major_inputs'],1):
    tail.extend([f'{i}. {target}',''])
tail.extend(['TEX CHECKS',''])
for item in tex['documents']:
    tail.extend([f"{item['tex_filename']}: {item['passes']} draft passes; {item['overfull_box_warnings']} overfull boxes; no undefined references or missing characters."])
tail.extend([
 'Inherited historical overfull boxes are recorded separately from the new '
 'increment. Draft compilation does not certify PDF layout; no PDF was generated.','',
 'READING FILES','',
 'RH_new_proofs_v0_46.tex — current audit and all new proof chapters.',
 'RH_readable_reconstruction_v0_46.tex — complete cumulative manuscript.',
 f"RH_dependency_audit_v0_46.txt — all {stats['open_count']} exact remaining selected contracts.",
 'continuation_checkpoint.json — current state and scope.',
 'next_source_targets.json — source-based continuation targets.',
 'provenance.json — all claims, proof/source ranges and dependencies.',
 'validation_v0_46.json — release checks and independent review registry.',
 'SHA256SUMS — hashes for the distributed files.','','SOURCE PIN',cfg['source_commit'],''])
text='\n'.join(head)+discussion+'\n'+'\n'.join(tail)
(ROOT/'RH_reconstruction_progress_v0_46.txt').write_text(text)
(ROOT/'README.txt').write_text('\n'.join(head[:head.index('THE FIVE NEW CHAPTERS')])+\
 '\nRead RH_reconstruction_progress_v0_46.txt for the mathematics, scope and next tasks. '
 'Both complete TeX readers, the exact audit, source snapshots and independent reviews are included.\n')
print(json.dumps({'progress_bytes':len(text.encode()),'new_claims':len(new),
                  'classification_counts':dict(categories),'open_count':stats['open_count']},indent=2))
