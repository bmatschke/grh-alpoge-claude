#!/usr/bin/env python3
"""Update the mathematical roadmap, preserving still-current whole contracts."""
from pathlib import Path
import json
ROOT=Path(__file__).resolve().parent
cfg=json.loads((ROOT/'increment_v0_51.json').read_text())
old=(ROOT/'RH_GRH_reconstruction_roadmap_v0_50.txt').read_text()
parts=[r'''RH AND UNRESTRICTED DIRICHLET GRH — RECONSTRUCTION ROADMAP v0.51
23 November 2026

Purpose: continue the human-readable reconstruction of the accepted
Alpoge–Claude formal proof, allowing proved simplifications while keeping
the full original statements. This roadmap supersedes the v0.50 frontier
notes. It adds no proof claim by itself.

Source repository: https://github.com/CocoSgt/riemann-hypothesis-lean
Pinned commit: 7cbf7a0c32fca1badf05931879a37c3f8a2b03b4

Use the full RH_reconstruction_v0_51.zip checkpoint. The two companion
reading editions are RH_new_proofs_v0_51.tex and
RH_readable_reconstruction_v0_51.tex. The exact whole-contract register is
dependency_audit_v0_51/remaining_leaf_register.json, also printed in
RH_dependency_audit_v0_51.txt. The parallel plan is a separate execution
document; the present file explains the mathematics and the dependencies.

Source path prefixes used below:
  L = src/ReciprocityTheory/ReductiveGroups/DiscreteSeries/LaplaceOperators/
  A = src/Development/AutomorphicArithmetic/AutomorphicVarieties/
  U = src/Development/AbelianVarietyTheory/Proofs/UnitaryExistence/
  I = src/Development/AbelianVarietyTheory/Proofs/InertiaEigenvalues/
  D = src/Development/AbelianVarietyTheory/Definitions/
All paths refer to the exact source commit above. Claim labels refer to
the human manuscripts, not merely to names of source theorems.

1. WHERE THE RECONSTRUCTION STANDS

Version 0.51 adds 80 independently reviewed numbered claims to the 3112
unchanged predecessor claims. There are now 3192 claims. The selected
sufficient graph remains 121 nodes and 161 edges. Exactly 24 whole
obligations remain open: 17 class C and 7 class B. Seventeen are shared
by RH and unrestricted Dirichlet GRH; seven are additional GRH inputs.
There are no RH-only open leaves in this selected route. These counts
are an inventory, not a percentage or an estimate of remaining effort.

The complete GLOBAL_LOCAL_GAIN closure from v0.49 is preserved. None of
the five new chapters closes another whole selected obligation: each
finishes substantial original subtheorems inside those obligations.
The formal proof remains accepted as correct. The outstanding work is
its ordinary mathematical exposition and the construction of all
retained input records on the same objects.

2. WHAT THE FIVE NEW CHAPTERS SUPPLY
''']
for i,text in enumerate(cfg['local_conclusions'],1): parts += [f'2.{i}. {text}\n']
parts += [r'''
These results should be consumed rather than reconstructed again. In
particular, do not reopen all four FramesOK fields, CoverTri/FibTri, the
28 Ok fields, TMap/TMapD, Eig or EvalP/EvalM. Conditional premises remain
at the joins: the section laws, full Gen/P, both Quot statements and the
coherent arithmetic comparisons. The following sections isolate them.

3. FIRST ANALYTIC PRIORITY: THE TWO ACTUAL QUOTIENT SUPPLIERS

The exact remaining targets are QuotPStatement and QuotMStatement in
L/LaplaceEstimates/PsiDatumStatement.lean. Their actual producers are
QuotP.lean and QuotM.lean in that directory. Read the full definitions
before selecting a smaller algebraic subtask. The focused source map is
bessel_period_evaluation_v51/quotient_next_handoff.txt.

For the original generated module S=genSub(E,V), the two tensor actions
are tensV(E) and tensVd(E), with Euler operators eeV(E) and eeVd(E).
Their selected eigenspaces lie in S^n. The original input tuple is
arbitrary in the selected eigenspace, with a nonzero actual tensor period
at some allowed point. It need not be one of BSE's explicit minor tuples.
The shifted parameter lambda plus or minus e_s must retain the original
Harish–Chandra and gap conditions with the same h.

Each quotient theorem must construct W_f of literal matrix functions
and W-prime inside the actual smooth right-regular L2 space. Every
function in W_f must be a tensor coefficient from the specified
eigenspace. Membership in W-prime must be equivalent, in both
directions, to being the L2 class of such a function. W-prime must be
the exact shifted lowest compact type, have the prescribed Casimir,
and be stable under the actual compact group. If the prescribed period
of a member of W_f vanishes at every period point, the function must
vanish everywhere on the original unitary group. All clauses matter.

3.1. Euler polynomial and eigenspace projections

Start with L/KTypeLemma/ProdShiftEeVOfCapelli.lean and the standard and
dual Euler predicates in QuotientHighestWeightTensorStandard.lean.
BSP3 and BST8 give an economical route: the complementary expansion
has the form (Omega+tI)U(t)=p_lambda(t)I, with a monic operator
polynomial U of degree n-1. Comparing coefficients expresses its
coefficients recursively as scalar polynomials in Omega. The constant
identity then gives the characteristic polynomial of Omega. The dual
expansion has its own shifted parameter and must be tracked separately.
This is a proposed simplification to prove, not a new v0.51 result.

Strict ordering of lambda makes the roots distinct. Lagrange
polynomials then project to the original eigenspaces and commute with
the tensor action. The original Euler predicates are stated without
a chosen Psi coefficient identification. A proof using BSP3 must
therefore include the exact broader datum-to-coefficient link before
claiming the full original scope. Reuse established coefficient
identities; do not add a stronger hypothesis silently.

3.2. The weight cone, unique extremal line and trace transfer

The full K2 targets are EigenspaceWeightConeStandard and its dual in
the same source interface. The cone is the nonnegative integral cone
of all ordered gl_n positive roots, not only compact roots. Every
nonzero compact highest vector in the chosen eigenspace must have
weight in that cone above the shifted lowest weight. Highest vectors
at that exact lowest weight must be linearly dependent.

The VermaProductIdentity, VermaCone and its A/B/C files develop the
pure cyclic-module filtration. Separately, RightHolPowerDetDiag and
IndicatorRholMem identify the actual scalar model. The critical return
to the supplied representation is the trace-kernel implication in
LowestKTypeVectorExists.lean: on every compact-stable word subspace,
vanishing under the scalar model implies vanishing under the actual
module evaluation. Its proof uses the precise differentiated averaged
Psi coefficient and unitarity. Matching weights alone does not give
this implication. LiftHighestWeightVector, MemEigenTensorSpaceIff and
K2V then assemble the result. K2Vd and DualLowestKTypeOfStandard use
the actual conjugate Hilbert space and index reversal; a transpose of
the final formula is insufficient.

3.3. Minimal type in a nonzero unitary image

The K3 targets quantify over every intertwining map into an arbitrary
infinitesimally unitary inner-product module. The target need not be
complete or irreducible. ThreeAddLeGapBound.lean and
CasimirValueSubSingle.lean are the standard/dual entries. Their route
uses the finite compact hull, a highest vector of minimal integral
cone height, and the Schmid-Casimir identity. The upper partial-sum
bound and K2's lower cone bound force the extracted type to have the
exact shifted lowest weight. Retain the h-2 gap margin and all
integrality conditions. An equality of Casimir scalars alone does not
determine the required compact type.

3.4. The generic quotient and actual period kernel

ImageLeClosGen.lean proves a useful independent conditional theorem,
quot_generic. Its inputs include every-image lowest-type extraction,
one common highest-line vector valid for every intertwiner, finite
compact hulls, a stable kernel subspace Z, and the exact saturation
condition. Its conclusion gives a subspace avoiding Z whose smooth
image is the required lowest type and is stable under the compact
group. Reconstruct this full conditional theorem while K2/K3 are
being proved, keeping its original numerical and ambient-module scope.

For QuotP/M take Z to be the kernel of all actual periods for one fixed
Bessel datum, Cayley matrix, translates and coefficient vector. BST and
BSP provide the literal smooth maps, convergence and differentiation.
ToL2CongrOnUnitaryBis identifies equal smooth L2 classes with equal
functions on the unitary group, hence equal periods. This gives the
saturation condition. QuotPA/QuotMA provide the finite compact hulls
and common highest line. The final spaces must arise from this kernel,
not from an unrelated abstract irreducible quotient.

When both full quotient statements pass review, BSE9 supplies the full
StepStatement and BNV23 supplies BesselNVGap. The inherited setting
return still retains Forms0. Orbital/fiber comparisons, uniqueness,
normalizations, transport and the global spectral estimates are later
producers; local nonvanishing alone does not close GLOBAL_SPECTRAL.

4. FIRST GEOMETRIC PRIORITY: GLOBAL SECTION LAWS AND THEIR INSTALLATION

NFL22 now supplies the whole prescribed-space uniformization return at
the printed premises. The immediate missing geometry is upstream:
the actual supplied Moduli and the exact SecBaseChangeSt/SecTwistSt
laws, together with any retained global suppliers of the HUF/PUN
foundations. The file normalized_frame_laws_v51/next_source_handoff.txt
identifies their precise source entries and separates them from the
already completed construction.

SecBaseChangeSt begins with a locally Noetherian original scheme and
the actual polarized abelian scheme. Near every point it supplies the
specified number of sections forming a basis after every affine base
change. The target algebra may be nonreduced, non-Noetherian and
nonflat. A proof for geometric fibers, flat targets or only reduced
test rings does not supply this statement. The original interface is
in ReciprocityTheory/ReductiveGroups/ArithmeticGeometry/
ExtensionDescent/GlobalSectionsRankAlgClosed.lean.

SecTwistSt, in the adjacent SecBaseChangeAnySt.lean interface, concerns
the actual twisted line bundle L^(q-1) tensor t_c^*L over every local
coefficient ring and lifts every residue-field section. Preserve the
section bases, ranks and residue lifting. NFL uses its complex-fiber
instances, but replacing the whole law by an unnamed theta existence
assertion would conceal the remaining input. A shorter proof of exactly
the instances sufficient for the terminal route is allowed if the
replacement interface and its use in every consumer are proved.

Use the actual line bundle, rigidification, polarization and section
charts throughout. If general cohomology-and-base-change results are
used, state and check their hypotheses on the original abelian scheme
and establish the required vanishing and ranks. Do not conflate the
already proved direct Fourier classification of the complex theta line
with the global arbitrary-base-change theorem. The former is NFR6;
the latter remains an independent supplier.

The direct shared source entry is
Proofs/AbelianSchemeLawProofs/SecBaseChangeOfPerf.lean, with
FinrankOfIsSecBasis.lean for the twisted basis and residue lift.
The common finite-matrix argument starts at
ExistsMulEqSmulOneOfMulVecInjective.lean. Its actual perfect complex,
geometric H1 vanishing, exact n^g rank and translation suppliers must
be exposed. For Moduli, keep the literal universal, reduced-base
representability and dual-number unramifiedness record from
PushInvertible.lean. The construction spine is ModuliProofs/
ExistsModuliPrimePowerFullLevel, NonemptyModuliOfLevelDvd and
NonemptyCmModuliOfDeeperLevel, followed by the every-level join.

4.1. After the laws: finite levels, class sums and simultaneous readings

Reuse CNC, ICL, PCL, TDR, NFR, HUF, PUN and NFL. Complete the finite
IsSystem, Gaussian/integrability/reproduction, short-rule gluing,
simultaneous dictionary and ramified integral jet/value suppliers.
Obtain the actual LatFull, both Boolean MLat levels and exact FWTie
transport. A proof at only one level is insufficient for the selected
rational-test interface. A bounded first target is the full
HermitianThetaLevelDataFormsSystem theorem: all nine IsSystem fields
un, lat, stab, sb, norm, mu, supp, cusp and adm on the fixed data.
Its off-diagonal overlap bound must be the strict 0.65<1 estimate,
with the original even-weight threshold and relative-index exponent.

Then prove higher CoversAt for every original tuple, phase-rescaled
class-sum existence and uniqueness, one PointIdentCore with lambda
and z chosen before all tuple records, and baseClassSumsSpan. Tests
must separate the same theta map and take values in the fixed embedded
coefficient field on every rational source vector and every stored
target basis vector. Carry the entire coefficient field, not just a
smaller coefficient subfield chosen for a convenient point.

For readings and rows, supply the original initial geometry, Fits,
division and central conditions, reFace, MultEq support, chain/group
tie, carriers, eigensystems, all-embedding logLam, HD/d3b and NEb.
Match the stored LiftTie.theta, mtRead, mjRead and ThDef3 to the same
Bundle's P.A3, P.Zs and P.S0. Preserve the exact eta identity for all
1<=j<=m. The stronger DivRows3 is separate from the completed first
DivDef3 and row-pair integrability. These are later installations on
one common family, not additional fields of the now complete IsUnf.

5. FIRST ARITHMETIC PRIORITY: THE TWO FULL Gen ENTRIES

LFC completes every generic Ok field on the MFC frame. Do not rebuild
phi/gen/cl/ec/b1p/b1/h1 or enlarge C0. The immediate inputs now missing
from the frame route are the two full concrete Gen implications. Their
shared target is the 19-field structure in
A/FrobeniusSmoothVectors/FrobeniusSplitPrimeDatum.lean. The detailed
source map is linked_frame_completion_v51/next_source_handoff.txt.

5.1. Dat to Gen and GdFrameEx

The entry gen_gd is in A/FrobeniusSmoothVectors/SqrtDiscr.lean.
Its exact output has Hb=top and M=ell*N*|disc K|, with the original
Dat characters and conjugation. Use DatFacts and GdFacts at their
original scopes. A clean first lemma constructs the square root of
the negative quadratic discriminant, identifies its character and
its fixed field, and retains the discriminant factor in M.

The remaining fields require the actual residue cyclotomic comparison,
both character nondegeneracy conditions and the decomposition witness.
Away from ell, inertia fixes ell-power roots of unity; the residual
finite character has prime-to-ell order, so reduction is injective on
its roots of unity. This gives the exact Teichmuller condition. The
unit condition on Psi(s)^2-1 must be transported to the original
residue nonvanishing assertion. Hb=top simplifies its subgroup fields
only in this Dat branch.

5.2. HostData to Gen and HostFrameEx

The entry gen_host is in A/FrobeniusSmoothVectors/GenHost.lean.
Here eta=eta4, M=ell*N, and Hb=ker(dirG(kapB ell psi)); the subgroup
cannot be replaced by top. Prove that it is open, contains commutators,
has ell-power index and contains the required ell-inertia. The host
permits ell=3. Its prime restriction is ell different from 2, and its
dyadic conductor and parity assumptions must be retained literally.

The main separate host arguments are the conductor-at-2 kernel
obstruction gh_two/kernel_not_contained_eta and the actual local
nonquadratic decomposition witness. The latter enters through
UnitaryThreeInertia.exists_hostFrame/exists_sigma, with source
UnitaryThreeDeformations/HostEx.lean and its dyadic character supplier.
Transport the witness to the arbitrary specified place by conjugation.
Global nontriviality of a character is weaker than this local statement.

5.3. Join the entries to the completed frame, then construct automorphy

A/FrobeniusSmoothVectors/GdEx.lean and HostEx.lean join the entries
to GdFrameEx and HostFrameEx. Keep the original P=GC.Hypotheses2.
Choose the CAF modulus Q and seed function before L and w, apply
LFC22 at that Q, and join LFC23 on the resulting actual coefficient-DVR
frame. The general local-ring HasFrameW theorem and this coefficient-DVR
seed application have different scopes; preserve that distinction.

The ensuing automorphic work is still substantial. IdeleGenerators/
ShapeFacts.lean defines Seed2 and Seed3, including arbitrarily high
weights in the prescribed congruence class, determinant/residual-sum
conditions and rank-three open irreducibility. These are representations,
not the character SeedClause already constructed by CAF/LFC.

Next supply full PfromAut/ModUAlt, linked-end and local/automorphic
descent. CurveDVRSpecialization/RatTorsionFree.lean defines FinEnd,
AutEnd3, AutEnd2 and GdEnd, with one marked g1 chosen before all three
outputs. Bounded transports begin in FinEndOfFinPt,
OrthogonalPairingFromIntertwiner and AutEnd2OfAutPt. Alternative
LinkedEndEAlt/GdEndAlt fields remain distinct until the original
interface is proved. UCE19 then consumes one original GdEnd to give
the full joint FinA/AutB/LemW output with the fixed coefficient embedding.

6. FIRST DENOMINATOR PRIORITY: COHERENT COMPARISONS AND ACTUAL ConclF

The remaining work is more specific than at v0.50. DFD already gives
the continuous complements, original PtFam and canonical data, full
exists_hubData at its named inputs, the point-row implication, correct
oriented killing implication and uniform admissible/small-prime bounds.
DNE already gives the whole export. The next source work must construct
the two comparison suppliers still retained in DFD15 and then the actual
local row bounds on their common family.

6.1. The coherent all-layer Wach construction

DFD12 proves the whole coefficient-extension theorem from the original
BhattScholzeIntegral input to BhattScholzeCrystallineLattices, including
the original integral lattice and fully faithful morphism assertion.
It does not give the all-layer Wach modules, their bases, Frobenius and
Gamma matrices or compatibility under the original specialization maps.
Begin with I/WachLatticesExistAllLayersOfBhattScholzeStatement.lean,
ExistsLocalWachFunctor.lean and the WachCrystallineComparison interface
in BlockTheory/NonGaloisCusps. Trace the actual HW, Fon and CmpOf
requirements of I/ExistsHubData.lean and its family join before selecting
supporting lattice lemmas.

A bounded proof should identify one literal lattice at every required
layer, its saturation and exactness, its coefficient topology, its
filtration and Frobenius/Gamma relations, and the comparison maps used
later. Pointwise existence of isomorphic Wach modules is not enough
when the consumer asks for compatible maps and a single functor.
Keep the original integral comparison theorem as a named input unless
its own supplier is being reconstructed in that packet.

6.2. The actual Selmer signature comparison

The second supplier turns the original family facts and the chosen
PtFam into SignatureChoiceCondition for the actual canonical datum.
It must compare the literal finite and crystalline local conditions,
normalized lengths and signature entries; an abstract inequality for
an unrelated Selmer group is insufficient. Read the exact interface
in Formalism/SharpRestriction/LevelLetterCocycles/
JointConditionsZpowers/CommutingEndomorphismCondition.lean together
with its JointSix/local-global assembly producers.

DFD11 has already fixed the orientation: GoodTw and SignatureChoice
use the same character psiW=(psiAt(C.sd,C.psi')) composed with art,
then the same requested side. Their internally supplied Boolean sides
need not agree. Do not cancel characters from two different choices.
The exact budget in this join is 1/ell^2, for both the two Selmer
length errors and the tame term. DFD13–DFD14 supply the parameter and
small-prime room needed after these comparisons are installed.

6.3. Full original local family and the denominator exit

For a fixed Fm, ConclF asks for C and x0 before every x>=x0, every
original hx:Fm.x1<x and every i in Fm.Ix(x). Given the original
ShaFinOdd premise for that member, it then chooses actual HubData X
satisfying Concl(Fm.L(x,i),Fm.params(x,hx,i),X,C). That same X must
satisfy all fifteen fields:
  pos, pass, mult, rank, kill, num, mid, bb, large, exc, two, ram,
  typ, par, small.
The branch predicates and actual row points cannot be replaced by
separately favorable data. Preserve the original support and exact
dcOf/epJ choices in DFD's canonical construction.

DFD9 allows function-valued e-prime and exceptional sets depending on
the representations actually chosen. They are evaluated after those
families are selected; do not move those choices ahead of their inputs.
DFD15 gives the eight-field Setup and AdmJ only after its two common
comparison suppliers are available. The remaining RowNum, StarAD, BB,
large/exceptional/type, ramified and small-prime bounds must then be
proved on that exact Setup. Reuse DFD14's full small-family bound and
DFD13's admissible parameters without introducing new family thresholds
after a member has been selected.

The source ConclusionOfFamilyFacts, RowClosureLinking and the original
NormChoiceFacts/common-bundle construction identify the final assembly.
Retain their exact Hypotheses2, TwGood, FactsF and small-prime inputs
until their actual instances are written. The target remains the
original ConclF; a new assumed omnibus family record is not a closure.

Apply DNE14 once the family exists. Its constant
K=2000(|Ca|+1)^3 is chosen before every family at fixed Ca. ConclF's
own Ca may depend on the given family. Do not interchange these two
orders. Finally install Closed(Des(C,3),LinkN) with the actual etaSum,
dZ0, same-host vvTerm and only the original ShaFinOdd/summability
guards. That complete common-family installation closes
GLOBAL_DENOMINATOR.
''']

# The following four sections remain current. Retain their full contracts
# rather than replacing them by a shorter, weaker summary.
start=old.index('7. THE SEPARATE COUNTV HOST AND SUPPORT LANE')
end=old.index('11. COMPLETE OPEN WHOLE-OBLIGATION REGISTER AT V0.50')
inherited=old[start:end]
inherited=inherited.replace('The common marked-frame work helps this lane,',
 'The completed conditional marked frame and the planned concrete Gen entries help this lane,')
inherited=inherited.replace('The geometry tasks in section 4 must be installed',
 'The completed NFL uniformization and the remaining geometry tasks in section 4 must be installed')
parts.append(inherited)
reg=json.loads((ROOT/'dependency_audit_v0_51/remaining_leaf_register.json').read_text())
coverage=json.loads((ROOT/'dependency_audit_v0_51/route_coverage.json').read_text())
byid={r['id']:r for r in reg['records']}
parts.append('11. COMPLETE OPEN WHOLE-OBLIGATION REGISTER AT v0.51\n\nNo additional whole selected obligation was closed. The exact contracts\nremain in the current audit, with additive v0.51 progress records.\n\nSHARED RH/GRH — 17\n')
for cid in coverage['shared_open_leaf_ids']:
 r=byid[cid];parts.append(cid+' ['+r['category']+'] — '+r['title'])
parts.append('\nADDITIONAL DIRICHLET GRH — 7\n')
for cid in coverage['dirichlet_grh_only_open_leaf_ids']:
 r=byid[cid];parts.append(cid+' ['+r['category']+'] — '+r['title'])
parts += [r'''
Check: shared=13 C+4 B; additional=4 C+3 B; total=17 C+7 B=24.
GLOBAL_LOCAL_GAIN is absent because its complete v0.49 closure stands.

12. NEXT EXECUTION ROUND AND ACCEPTANCE CRITERIA

Use at most four active agents including the coordinator. A practical
first wave assigns the Bessel Euler/trace-transfer work, the global
section-law producer and the two concrete Gen entries to three agents,
while the coordinator develops one coherent denominator comparison.
The generic quotient theorem can be assigned as soon as a bounded
algebraic or arithmetic packet freezes. The companion parallel plan
gives the source inputs, disjoint file ownership and review rotation.

For every packet, start by copying the exact original input and output
contract into ordinary notation. Identify the actual shared objects and
the order of choices. Write the mathematical argument before recording
a closure. A theorem may be proved with original premises retained,
but its status must say so and its input producer must stay visible.
An accepted simplification must imply the original target used by the
terminal deduction; it cannot merely prove a similar weaker assertion.

The first review should ask whether the output can be passed directly
to its original consumer: same field and coefficient embedding, same
frame and lattice, same section and maps, same periods and measures,
same finite/local conditions, and the same uniformity. Then review the
mathematics, particularly boundary cases, signs, normalization constants
and any exchange of quantifiers. Record resolved findings and exact
proof hashes. Source hashes identify the target and evidence; they do
not replace the human proof.

Only after the full contract is written and independently checked
should the selected graph change status. Preserve all earlier claims
and the historical proof body. Update the current whole register,
roadmap and parallel plan together. Run the existing syntax/reference
and provenance checks; no new Lean replay is needed for this task.

13. DIRECT CONTINUATION REFERENCES

Current results and inputs:
  normalized_frame_laws_v51/main.tex — NFL1–NFL22.
  linked_frame_completion_v51/main.tex — LFC1–LFC23.
  bessel_shift_suppliers_v51/main.tex — BST1–BST11.
  bessel_period_evaluation_v51/main.tex — BSE1–BSE9.
  denominator_family_data_v51/main.tex — DFD1–DFD15.
Their provenance, contracts, closure and retained-foundation files bind
the exact original scopes and independently reviewed proofs.

Focused source guides:
  bessel_period_evaluation_v51/quotient_next_handoff.txt.
  linked_frame_completion_v51/next_source_handoff.txt.
  normalized_frame_laws_v51/next_source_handoff.txt.
These are task maps, not additional proof claims.

Whole frontier and preservation:
  dependency_audit_v0_51/remaining_leaf_register.json.
  dependency_audit_v0_51/route_coverage.json.
  continuation_checkpoint.json and next_source_targets.json.
  reviews_v0_51/review_registry.json and the independent integration audit.
  history/version_0_50 for displaced predecessor metadata and plans.

The final human exposition should follow the eventual mathematical
dependency order and explain why the constructions meet their consumer
contracts. The complete conditional terminal argument CMP1–CMP6 is
already available. The remaining work is to supply its original
producers, then state the unconditional human RH and unrestricted
Dirichlet-GRH deductions only when all those producers are present.
''']
dest=ROOT/'RH_GRH_reconstruction_roadmap_v0_51.txt'
dest.write_text('\n\n'.join(parts).rstrip()+'\n')
print(json.dumps({'file':dest.name,'words':len(dest.read_text().split()),'bytes':dest.stat().st_size}))
