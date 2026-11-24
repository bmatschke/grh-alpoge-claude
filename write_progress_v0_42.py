#!/usr/bin/env python3
"""Write the standalone mathematical progress and continuation guide."""
from pathlib import Path
import json

ROOT=Path(__file__).resolve().parent
cfg=json.loads((ROOT/'increment_v0_42.json').read_text())
stats=json.loads((ROOT/'integration_stats_v0_42.json').read_text())
spec='specialization_map_v42' in cfg['components']
arith='arithmetic_specialization_v42' in cfg['components']
text="""RH AND DIRICHLET GRH — RECONSTRUCTION v0.42
Mathematical progress, reading guide, and continuation record
23 November 2026

1. CURRENT RESULT AND BOUNDARY

This release advances the attached v0.41 reconstruction along the attached
roadmap. It contains actual written proofs, exact source correspondences,
independent mathematical reviews, and a revised dependency audit. It is
still a partial human reconstruction. The complete unconditional human
proof of RH and Dirichlet GRH is not yet present.

The underlying Alpoge–Claude Lean proof is accepted as fully checked and
correct. All remaining obligations concern the reconstruction into human
mathematics. GRH throughout means the unrestricted Dirichlet-L-function
generalization in the source. No claim about every automorphic L-function
is being made.

The two former class-D source-matching questions are now closed:

  AD_VANISH_K_MATCH — the full original AdVanishK, all ranks n >= 2,
  every allowed prime, exact polarized full matrix adjoint and local
  finite conditions. Proof: ADK1–ADK6.

  HOST_RIGID_S — the full original HostRigid_s, every original allowed
  point and deformation, all allowed odd primes including 3. Proof:
  HSR1–HSR9, using ADK6 and the inherited local crystalline calculation.

The selected route now has @OPEN@ whole open obligations: @C@ class C
and @B@ class B. There are @SHARED@ shared by RH and Dirichlet GRH,
@GRH@ additional for Dirichlet GRH, and none open only for RH.
The selected graph retains all 121 nodes and 161 logical edges.

The new inventory is @NEW@ claims, giving @TOTAL@ cumulative claims.
Four new numbered blocks (CMP1, CMP3, CMP4, CMP5) consolidate inherited
proofs into the main argument. They are expository progress, not new
arithmetic input theorems. None of these counts measures a percentage of
proof completion: several remaining C entries are large existence and
compatibility theorems.

2. WHAT TO READ

Start with RH_new_proofs_v0_42.tex. It contains the current audit and all
new chapters, without the historical accumulation. Read CMP1–CMP6 first
to see exactly how the arithmetic inputs imply the zero statements.
Then choose the supporting branch:

  Ordinary/arithmetic entrance: FNL, OST, WRP, OCT, OHA@SPEC_SHORT@.
  Adjoint and host rigidity: ADK, HSR.
  Finite row weights and global estimates: RRT, GQT.

RH_readable_reconstruction_v0_42.tex is the complete cumulative manuscript.
The new audit and chapters are at the front. The earlier proof body is
preserved verbatim, with explicit historical labels and the current
audit governing older statements of what remains open. Earlier named
lemmas cited by new proofs are available there and in their original
component folders.

RH_dependency_audit_v0_42.txt gives every current whole obligation,
its exact output, source references, common-object constraints and
updated remaining subfrontier. The archive contains all proof components,
the complete provenance ledger, the mathematical dependency graph,
independent review reports, continuation records and source snapshots.

3. ROADMAP MILESTONES

M0 — Complete as an explicitly conditional main proof.
The terminal derivation is now readable in one place. Its two arithmetic
input contracts name the objects, normalizations, inequalities and order
of choices. It is conditional until those input-producing theorems close.

M1 — Complete.
The actual finite-level representatives, all original HSet axioms, ordinary
projector, finite freeness and original coefficientwise base change are
proved. The completed theorem works over the source's complete local
rings, including nonreduced rings and nonflat local coefficient maps.

M2 — Substantially advanced; the same-ideal arithmetic theorem remains open.
The actual algebraic weight representation, full classical control and
the original local Hecke-algebra statements are proved.@SPEC_MILESTONE@
The full integral TypeForAlt, separating arithmetic fibers, four Hida
endpoints and all-level automorphy must still be assembled on the same
ideal in each of the two original rank-four constructions.

M3 — The common geometric/local existence theorem remains open.
This release retains the detailed F3/F4, higher-cover, class-sum,
point-identity, full-lattice and base-row contracts. It does not present
separate witnesses as a substitute for one simultaneous family.

M4 — Both D matching obligations complete; other arithmetic branches open.
The adjoint theorem and original host rigidity can now be used on their
printed hypotheses. RIG_II, one-character/congruence producers, host
existence/counting and the additional Dirichlet-GRH branches remain.

M5 — Exact reductions and several local estimates proved; five whole
global producers remain open.
Only three row-count tests suffice. A polynomial spectral rate suffices
for the selected final consumer. Actual finite local weights and four
of the five W_g terms have written local proofs. These do not yet produce
the global arithmetic counts or the other common-family estimates.

M6 — Final unconditional assembly remains open.
RH still uses Cases I, II and V; the additional Dirichlet-GRH route retains
Case III, Seed IV and rank-four chain propagation/descent. All original
character and conductor dependence is preserved.

M7 — Main exposition and reading structure advanced; final exposition
depends on mathematical closure.
The reader's edition separates the new argument from the cumulative
historical material, while the latter remains fully traceable.

4. THE COMPLETE CONDITIONAL MAIN ARGUMENT

For a primitive target character psi of order o, let C_psi be the distinct
primitive inducers of its powers. Define the smoothed centered prime sums

  G(x) = sum_{r<=x} Lambda(r)(x/r - 1) - x log x + (1+gamma)x,

  G_chi(x) = sum_{r<=x} Lambda(r)chi(r)(x/r - 1)
             + x L'/L(1,chi),                       chi nonprincipal,

and the fixed positive signal

  H_psi(x) = G(x) + (1/(3o+1))
                    sum_{chi in C_psi, chi != 1} Re G_chi(x).

The plus sign in the centering term removes the unwanted linear Mellin
pole. The character family and positive coefficients are fixed before
the late windows are chosen. The principal target gives the zeta signal.

The first arithmetic input constructs one compatible finite datum at
every x in arbitrarily late windows [Y,Y^(3/2)]. It includes the same
finite abelian quotient, original inertia and Frobenius classes, biased
character selector, thick/thin weights, exact logarithmic derivatives
and scalar size/cutoff conditions. The entire list is printed before
CMP1; it is not abbreviated to an unproved phrase such as 'compatible
automorphic data exist'.

The second input bounds one average arithmetic gap on those same data.
Writing Gamma_bar for the average over the original translate subgroup,
Q = |T| m b and D = Q d_2/2, the proved Fourier comparison is

  H_psi(x) <= Gamma_bar(x)/D(x)
               + (4+4o)x^(1/2+epsilon) + 4/(d_2 x).

Thus it is sufficient to bound the mean gap. Bounding every individual
translate is stronger than the terminal argument requires. The proof
checks the ramified prime terms as well as unramified orthogonality,
retaining the exceptional prime with its original coefficient.

The scalar parameter calculation then gives

  H_psi(x) << x^(1/2+(C+4)epsilon),

where C is the fixed exponent in the arithmetic gap estimate. The source
choice C=5 gives exponent 1/2+9epsilon. Constants may depend on the fixed
target and epsilon; their order of choice cannot depend on the later
family member in a way the original contract forbids.

CMP4 supplies the complete one-sided analytic criterion. The Mellin
transform of the centered signal has the relevant zero poles; its
positive weights prevent cancellation. A derivative/tail argument shows
that a pole to the right of the claimed exponent contradicts the upper
bound on arbitrarily late windows. Choose epsilon small enough for any
given exponent above 1/2. The functional equations and imprimitive Euler
factors then give RH and unrestricted Dirichlet GRH conditionally on the
two arithmetic inputs. CMP6 gives a further sufficient version using a
measurable positive averaged-gap envelope and a weighted integral bound.

This main proof organizes and, in two places, weakens the remaining
arithmetic task. It does not assert that the two input contracts have
already been constructed.

5. THE ORDINARY AND HECKE ENTRANCE

Finite levels and actual axioms — FNL1–FNL16.
The adelic class argument is specialized to the original identity-form
unitary group and its exact auxiliary and Iwahori level. Coordinate
patching proves the required order

  g = glob(gamma) s (u,b).

The proof checks the actual split local sections, their supports and
commutation, the level join, the original Artin map and dense inverse
Frobenius image. It supplies all eighteen HSet.Ax fields, not merely a
finite-dimensional replacement space. No rank-dependent restriction on
the original auxiliary prime is introduced.

Ordinary projector, freeness and base change — OST1–OST28.
Finite integral evaluation sections and repeated level lowering show
eventual periodicity modulo each adic precision. Factorial powers of the
same U_z then converge to one projector e, chosen before the function and
precision. Its convergence threshold may depend on them, as allowed.

Successive approximation and a split evaluation map prove finite
projectivity, hence freeness over the local ring. They also prove the
reverse inclusion in the exact value filtration; that equality is needed
for the later Nakayama argument. Every positive-monoid operator is
invertible on the actual ordinary submodule. Simultaneous evaluation
over A and B identifies the original coefficientwise map

  B tensor_A Ord_A  ->  Ord_B

as an isomorphism for every allowed local map A -> B. The proof adds no
flatness or reducedness premise and constructs the local and product
Iwahori axioms before installation on every actual level.

Actual algebraic weights — WRP1–WRP12.
The source needs an existential integral weight representation identified
with one specified complex tensor representation. A general integral
standard-monomial basis over arbitrary domains is unnecessary for that
endpoint. The construction instead takes one finite coefficient-field
compositum inside the original algebraic closure, its literal integer
DVR, and the saturated integral polynomial lattice in each original
factor.

The inherited polynomial-kernel and irreducibility theorems, together
with a dense Gaussian cell, give a weight basis with a unique reversed
lowest coordinate. The positive-root inequalities prove integral
positive normalization and strict contraction outside that coordinate.
Tensoring the bases gives an explicit intertwiner with the unchanged
algRep. Every one of the ten WtRep assertions is verified, and the torus
character is exactly the original lowW/algPow product. The given complex
field isomorphism is retained and is never assumed continuous. Every
prime, rank-zero and empty-index case remains allowed.

Classical control — OCT1–OCT19.
The same zeroth-coordinate map is shown to intertwine the normalized
classical T_a with the ordinary U_a. A finite free integral classical
lattice has its own factorial projector. Control is injective on its
ordinary part because its kernel is strictly contracted by T_z.
Deeper interpolation, level lowering, the exact ordinary filtration and
Nakayama give surjectivity. The resulting integral isomorphism yields
the original complex control statement, with the specified coefficient
embedding and its original domain hypothesis. Positive operators,
sufficiently deep levels and finite away sums have the required
compatibilities.

Local Hecke algebra — OHA1–OHA12.
Integral double-coset convolution gives the actual operators. Smith
factorization and transposition prove spherical commutativity. For the
finite commuting operator algebra T on the ordinary module, the literal
adic residual part equals the selected idempotent summand eY. The source
Hecke algebra is the corresponding finite complete local algebra with
the prescribed residue field. Positive operators are units in that
algebra, by a written inverse-polynomial argument. The domain hypothesis
is used only where the printed torsion-freeness conclusion requires it.

@SPEC_SECTION@

These theorems complete a substantial entrance to M2. They do not by
themselves prove that an arithmetic Hecke block is nonzero, that arithmetic
points separate the required algebra, or that all original Hida and
automorphy properties hold on one common ideal.

6. THE TWO RIGIDITY MATCHES

The global adjoint theorem — ADK1–ADK6.
The published input is Jack Thorne's Theorem 6.1 in 'On the vanishing of
adjoint Bloch–Kato Selmer groups of irreducible automorphic Galois
representations'. The reconstruction checks the actual regular algebraic
cuspidal polarized representation, normalized geometric Frobenius,
conjugate duality and finite coefficient scope. Irreducibility is on the
full infinite cyclotomic kernel. The action is on M_n, not a replacement
trace-zero subspace; complex conjugation acts by negative transpose
relative to the actual symmetric pairing. The scalar line is retained.

The comparison with the normalized Galois representation is checked using
the precise Barnet-Lamb–Gee–Geraghty–Taylor attachment and sign convention.
The local graph topology, diagonal crystalline action and coefficient
retractions are proved to match the literal source finite conditions.
No additional residual-image or large-prime hypothesis is introduced.
The application closes the full original rank-n contract for n>=2.

Original host rigidity — HSR1–HSR9.
An actual finite-DVR model gives continuity and finite coefficient capture
for an allowed deformation. A dyadic conductor calculation yields the
separating residue values. Correcting local arithmetic Frobenius by
inertia gives an element with cyclotomic character exactly one, stronger
than the original required closeness. Reducing the actual characteristic
polynomial proves eigenvalue separation in every allowed triangular basis.

The inherited ordinary crystalline calculation applies to the full
dual-number deformation, including unramified diagonal variations.
Explicit inertia primitives and finite-index averaging give precisely
the source Bloch–Kato conditions at every prime. The original automorphy
input is the twist epsilon^(-1) r_0 over Q(i); its pairing is the actual
antidiagonal matrix J and its multiplier is epsilon^(-2). Thus the full
adjoint is exactly the representation covered by ADK6. Quotient
surjectivity gives one global coboundary with the source's required sign.

The completed implication retains all original marked-point, parity,
valuation, automorphy and cyclotomic hypotheses. It does not construct
the points satisfying them. HostNumber_s and the separate Type-II
rigidity producer RIG_II therefore remain in the open register.

7. FINITE ROW ESTIMATES AND SUFFICIENT GLOBAL BOUNDS

RRT1–RRT16 start with the actual finite GL_N projectors and local weights.
The regular-representation coefficient trace proves nonnegativity and
normalization. Two character-theoretic identifications are isolated as
explicit remaining targets; neither is assumed merely because a source
declaration mentions Green's parametrization.

For the explicit squarefree polynomial weights, the proof gives factor
divisibility bounds and domination by random-permutation cycle types.
The elementary invariant-subset argument gives 7/8. An elementary
prime-count estimate gives the needed eventual long-cycle probability,
with the original constant and with rank growth checked on the actual
family, rather than inferred from an insufficient abstract size record.

The root-to-twist collision estimate is proved for its full original
range, including N=1. For the stated distinct odd primes p_1,p_2 and
divisibility assumptions on q-1, its bound is

  1/(4 min(p_1,p_2)) + (1+log N)/(q-1).

If a root has the same prime-to-ell component as a fixed twist, its
minimal polynomial divides X^(ell^v) - c^(ell^v). Counting these factors
by degree, and writing out the needed prime-power valuation calculation,
gives the exact constant. This supplies the complete LocalEstimateIII.
Together with the other finite arguments, four of the five W_g terms
have written local producers. The root-injectivity collision term and
the two exact local character laws remain to be proved.

The finite tensor identity preserves the original Haar comparison as a
separate input. An explicit disjoint-union construction supplies the
retained-row injection on the original multiplicity identities, allowing
repeated labels and zero multiplicities. It does not invent an automorphic
spectrum from a list of numbers.

GQT1–GQT5 show that the retained defect can be bounded using only three
count tests: a lower count for all rows and upper counts for two bad
label events. The finite union/probability argument uses no independence
assumption. With relative counting error alpha, its core inequality is

  defect <= ((1+alpha)/(1-alpha)) (p_0+p_1).

The actual row object and good-image identification are retained. A
uniform alpha<=1/2 suffices once the local bad-weight estimates are
available. The full stronger all-subset counting theorem is sufficient
but not required by this reduced final argument.

GQT6–GQT7 prove a sufficient spectral replacement. For a fixed C_H>0,
write sigma=x^(-C_H). On the same normalized operators and lattices, it
suffices to prove uniformly

  eta_0, eta_1, sqrt(e_0) <= sigma/16.

The existing Gram-to-slope proof then has error budget

  (83+4 sqrt(2))/16 < 6.

All positive-rank, Bessel-map, metric and normalization requirements are
checked. The original discarded fraction is absorbed using its existing
exponential bound. This proves sufficiency for the selected final
consumer. It does not prove the original stronger exponential LinkS
or supply the still-missing spectral-geometry estimates themselves.

8. WHAT IS STILL REQUIRED FOR A COMPLETE HUMAN PROOF

The remaining work should be organized around actual input-producing
theorems, rather than additional packaging of completed implications.

First: complete the same-ideal arithmetic package. Construct the full
integral TypeForAlt, the required arithmetic fibers and separation,
PointTheoremBaseObject, ArithmeticPointDecomposition (with the original
cofinite strict Frobenius-ratio bound), IrrArithPointsAutomorphicAway,
TwistOk and all-level HasAut. Preserve the same ideal J in each original
ring, both rank-four Links, fixed iota, prime 3 and the common coefficient
threshold. Do not strengthen the strict ratio statement to exact purity.

Second: construct one common geometric/local family. The higher covers,
class-sum cusp membership and uniqueness, phase rescalings, common point
identity, base class-sum generation and actual full lattice must agree
with the F3/F4 coefficient and local specialization data. The existing
finite transfer and local constructor theorems can then be used. Their
completed proofs are not substitutes for these input constructions.

Third: complete the one-character, congruence, host-counting and Type-II
arithmetic arguments. The two adjoint/host matching questions are now
resolved and should not consume reconstruction time again. Additional
Dirichlet-GRH seed/tensor/chain/promodularity work remains separately
identified; it contains substantial C arguments.

Fourth: prove the five global quantitative estimates on the same family.
For retained rows, the next precise local tasks are the two finite-group
character laws with exact normalized labels and the root-injectivity
collision estimate; the next global tasks are EtOne, RowsAdd/RowsGood,
the actual AllRows object and the three sufficient cylinder counts.
For the spectral branch, the proved polynomial alternative is available
with the exact stated uniformity. Denominator, period/height and local
gain still need their original arithmetic and geometric estimates.

All thresholds must be chosen in the source's permitted order. Separate
fields, ideals, metrics, measures or witness families satisfying separate
clauses do not establish their simultaneous conjunction.

9. REVIEW, PRESERVATION AND SOURCE CORRESPONDENCE

Each new proof component was reviewed by an agent other than its author;
the primary review and additional focused reviews are bound to the
actual released proof bytes. Review checks included small-prime scope,
nilpotent coefficient rings, nonflat base change, infinite cyclotomic
kernels, original local maps, entrywise weight assertions, all-level
compatibilities and the quantitative choice order.

The integration audit preserves all 2,209 baseline claim records, their
source arrays and mathematical dependency edges, every selected graph
node and edge, all 245 historical targets and their 107 scope groups.
All 3,475 baseline manifest artifacts survive either at their original
path or as byte-identical historical root files. New source ranges are
compared against exact git blobs at the same source pin. The complete
historical cumulative proof body is preserved verbatim.

The validation report distinguishes mathematical review, source/proof
integrity checks, dependency checks and TeX draft compilation. The latter
checks syntax and resolved cross-references; it is not a visual PDF
review. No PDF, Lean build or kernel replay is claimed. The claim graph
is the human mathematical dependency graph, not a mechanically extracted
Lean transitive audit.

The canonical source pin is
  7cbf7a0c32fca1badf05931879a37c3f8a2b03b4
  https://github.com/CocoSgt/riemann-hypothesis-lean/tree/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4

Checked published inputs used in the new chapters include:
  Thorne, Theorem 6.1:
    https://arxiv.org/html/2207.04925v1
  Barnet-Lamb–Gee–Geraghty–Taylor, Theorem 2.1.1 and sign conventions:
    https://annals.math.princeton.edu/wp-content/uploads/annals-v179-n2-p03-p.pdf
  Finite module completeness, Stacks Project Tag 00MA:
    https://stacks.math.columbia.edu/tag/00MA
  Finite algebra decomposition, Stacks Project Tag 0325:
    https://stacks.math.columbia.edu/tag/0325

The full proof files give the hypotheses and exact use of each published
input. The archive also preserves the original roadmap and the previous
continuation records. The current v0.42 audit governs completion status.
"""
repl={'@OPEN@':stats['open_count'],'@C@':stats['open_categories'].get('C',0),
      '@B@':stats['open_categories'].get('B',0),'@SHARED@':stats['shared_open'],
      '@GRH@':stats['extra_grh_open'],'@NEW@':stats['new_claims'],'@TOTAL@':stats['cumulative_claims'],
      '@SPEC_SHORT@':', SMP and ASP' if arith else (', and SMP' if spec else ''),
      '@SPEC_MILESTONE@':(' Both full Sp.absSpec and the original arithmetic\n'
        'SpecIntIff.spec are complete, including all eleven IsSpec fields.') if arith else
        (' The actual all-level specialization map is also reconstructed on its exact source hypotheses.' if spec else ''),
      '@SPEC_SECTION@':('\nOne all-level map — SMP1–SMP10.\n'
        'Exact ordinary base change and integral control give a unique good\n'
        'classical lift whenever it exists. Directed common refinements make\n'
        'that lift independent of the level. Defining the map on all ambient\n'
        'functions is essential: its full away-sum clause does not require\n'
        'the A-valued away-sum image to be ordinary. Finite O-modules of\n'
        'untwisted values and the determinant trick prove both eigenvalue\n'
        'integrality assertions. This proves the complete original Sp.absSpec.\n') if spec else ''}
if arith:
    repl['@SPEC_SECTION@'] += ('\nActual arithmetic specialization — ASP1–ASP13.\n'
        'The given arithmetic point x:A->Qbar_ell has image in one actual\n'
        'finite coefficient DVR. This follows from a strict norm bound on\n'
        'the maximal ideal, uniform decay of its powers, and finite-field\n'
        'capture of polynomial approximations. The induced coefficient map\n'
        'is local. The compact-torus character lifts into that same ring,\n'
        'and its quotient with the given character is exactly the original\n'
        'finite-part character with the required depth shift.\n\n'
        'The proof identifies the literal ClAt and OrdAt spaces, every local\n'
        'lowVal normalization, the original distinguished operator, integral\n'
        'spherical sums and auxiliary conjugated-level actions. The one SMP\n'
        'map then supplies all eleven original IsSpec fields for the specified\n'
        'point and fixed iota. This completes SpecIntIff.spec, while retaining\n'
        'its original Ax, IsWt and Arith hypotheses. Nonvanishing and separation\n'
        'of arithmetic Hecke blocks remain separate input-producing tasks.\n')
for a,b in repl.items():text=text.replace(a,str(b))
(ROOT/'RH_reconstruction_progress_v0_42.txt').write_text(text)
print('Wrote',len(text.encode()),'bytes of current mathematical progress and continuation guidance.')
