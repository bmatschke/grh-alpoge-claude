#!/usr/bin/env python3
"""Write the current roadmap and capacity-bounded parallel execution plan."""
from pathlib import Path
import json
ROOT=Path(__file__).resolve().parent
cfg=json.loads((ROOT/'increment_v0_52.json').read_text())
st=json.loads((ROOT/'integration_stats_v0_52.json').read_text())
reg=json.loads((ROOT/'dependency_audit_v0_52/remaining_leaf_register.json').read_text())
old=(ROOT/'RH_GRH_reconstruction_roadmap_v0_51.txt').read_text()
parts=[r'''RH AND UNRESTRICTED DIRICHLET GRH — RECONSTRUCTION ROADMAP v0.52
23 November 2026

Purpose: continue the human-readable reconstruction of the accepted
Alpoge–Claude formal proof, with proved simplifications allowed and all
original scopes retained. This roadmap supersedes the v0.51 frontier
notes. It is a work guide, not an additional proof claim.

Repository: https://github.com/CocoSgt/riemann-hypothesis-lean
Pinned commit: 7cbf7a0c32fca1badf05931879a37c3f8a2b03b4

Use RH_reconstruction_v0_52.zip as the complete checkpoint.
RH_new_proofs_v0_52.tex contains the current audit and four new chapters;
RH_readable_reconstruction_v0_52.tex is the cumulative edition.
RH_dependency_audit_v0_52.txt and the corresponding remaining_leaf_register
contain the full original whole contracts. The execution plan is separate.

Source prefixes used below, relative to the exact pinned repository:
 A = src/Development/AutomorphicArithmetic/AutomorphicVarieties/
 G = src/Development/AbelianVarietyTheory/Proofs/
 I = G/InertiaEigenvalues/
 N = src/Development/AbelianVarietyTheory/Definitions/NonGaloisDescent/
 L = src/ReciprocityTheory/ReductiveGroups/DiscreteSeries/LaplaceOperators/
 AG = src/ReciprocityTheory/ReductiveGroups/ArithmeticGeometry/

1. WHERE THE RECONSTRUCTION STANDS

The 87 new claims bring the inventory from 3192 to 3279. The selected
sufficient graph has 121 nodes and 161 edges. Exactly 24 whole obligations
remain: 17 class C and seven class B. Seventeen are shared by RH and
unrestricted Dirichlet GRH, seven are additional GRH inputs, and none
are RH-only. Counts describe the decomposition, not a completion
percentage or an estimate of the effort still required.

GLOBAL_LOCAL_GAIN remains fully closed from v0.49. Version 0.52 closes
substantial original subtheorems within the remaining whole obligations,
including both Bessel quotients, BesselNVGap, the arithmetic Gen entries,
the finite-end transport and the Selmer SignatureChoice. The global
section laws are complete conditional implications with their geometric
producers still explicit. The whole common-family estimates and remaining
producer records must still be supplied.

2. REUSE THE FOUR NEW CHAPTERS
''']
for i,t in enumerate(cfg['local_conclusions'],1): parts += [f'2.{i}. {t}\n']
parts += [r'''
Do not reopen QuotP/QuotM, K2/K3, the local Bessel shift/nonvanishing,
gen_gd/gen_host, P-to-GdFrameEx/HostFrameEx, exists_nrep3,
finEnd_of_finPt, Selmer scalar change, SignatureChoice, the universal
matrix-basis certificate or its conditional section-law installation.
Their original premises remain visible at the appropriate joins.

3. DENOMINATOR PRIORITY: THE ACTUAL WACH COMPARISON

SSC17 removes the Selmer-signature supplier from DFD15. Its remaining
comparison is precisely one HW/Fon/Cmp triple on the original canonical
D. Begin with I/ExistsWachFunctorComparisonOfBhattScholzeStatement.lean,
exists_wachFunctor_comparison_of_bhattScholze, and read the full types of
HWOf, FonOf and CmpOf before choosing a smaller lattice lemma.

The detailed map is selmer_signature_comparison_v52/wach_next_handoff.txt.
It separates four bounded directions: concrete group/series/embeddings;
faithful cyclotomic-kernel invariants and etale bases; the actual Wach
lattice from the original integral comparison input; and Herr classes
with the period comparison. DFD12 already proves coefficient extension
from BhattScholzeIntegral to BhattScholzeCrystallineLattices. That is an
input to, rather than a substitute for, the Wach lattice construction.

N/ExistsOfLayers.lean has the exact dependent record
Gamma,R,I,ioW,E,Mo,Cl,Cm. Its exists_of_layers theorem permits choosing
one complete such record at each Good(K,s,LL). Do not add an unspecified
extra inter-layer transition requirement. Preserve the actual internal
functoriality for all lattices and maps, the source Frobenius/Gamma
relations, the original trivial lattice, and the quantitative de Rham
filtration remainder. Arbitrary independently chosen models do not
supply one dependent record.

Useful producer entries are I/ExistsLocalWachFunctor.lean,
CyclotomicKernelTiltInvariantsFaithful.lean, ResEqOneIff.lean,
WachLatticesExistAllLayersOfBhattScholze.lean, IsUnitOfOneTmul.lean,
ExistsUniqueFits.lean and ChiGamPowNeOne.lean. WachEx quantifies over
every allowed Gamma/series/embedding/etale module, not just a convenient
model. Preserve that scope if proving the full source theorem.

3.1. Return to the original setup and local family

Once the coherent triple is supplied, SSC17 and DFD give the original
Setup and AdmJ with the same NChoice, complement family and exceptional
sets. The next target is one ConclF family, not another assumed omnibus
record. For fixed Fm, choose C and x0 before every x>=x0, every original
hx:Fm.x1<x and every i in Fm.Ix(x). Given the original ShaFinOdd member
premise, choose actual HubData X satisfying all fifteen Concl fields:
 pos, pass, mult, rank, kill, num, mid, bb, large, exc, two, ram,
 typ, par, small.

The actual points, support, dcOf and epJ choices remain fixed. The
representation-dependent e-prime and exceptional sets may be evaluated
only after the representations on which they depend have been chosen.
Reuse DFD's uniform admissibility and small-prime estimates, SSC's
signature and the exact 1/ell^2 oriented KillAt bound. Prove RowNum,
StarAD, BB and the remaining large/exceptional/type/ramified bounds on
that same Setup. ConclusionOfFamilyFacts, RowClosureLinking and the
original NormChoiceFacts/common-bundle construction identify the join.

Apply DNE14 only after ConclF is supplied. Its
K=2000(|Ca|+1)^3 is chosen before every family at fixed Ca; ConclF's Ca
may depend on the family. Preserve that distinction. Finally install
Closed(Des(C,3),LinkN) with the actual etaSum, dZ0 and same-host vvTerm,
retaining precisely the original ShaFinOdd and summability guards.

4. GEOMETRIC PRIORITY: ACTUAL SUPPLIERS OF THE CONDITIONAL LAWS

GSL3–GSL13 should now be used directly. They prove one matrix certificate
and actual basis valid after every permitted coefficient change, the
finite-projective-to-matrix reduction, the universal flat-complex model
from supplied Noetherian cube data, all literal Perf fields, naturality
and lifting of every residue section. GSL23–GSL26 give the complete
conditional global installation. Read
global_section_laws_v52/next_source_handoff.txt and explicit_inputs.json
for the exact remaining F,P,V,R,T interfaces.

4.1. Recommended first bounded packet: the geometric section cube

G/CoherentCohomologyProofs/ExistsFiniteProjectiveCechComplexLineBundle.lean
asks for one finite-projective complex and actual map to the section
Cech complex, valid after every coefficient extension. The original
ring may be arbitrary. Keep the smooth X->Spec R, actual very-ample
presentation H,s_i and actual line bundle M. GSL10 already proves that
the cover D_i=D(s_i) has affine nonempty finite intersections.

The central missing model is DehomogenisingCompOfSaturating.lean,
exists_noetherian_model_grCube. Supply one Noetherian R0, a cube C0
flat on every nonempty vertex with finite Cech cohomology, and the
actual bijective base-change maps to the original graded-localization
cube. GSL8 consumes exactly these outputs. Its substantial supporting
entries are ExistsGradedPresentationSaturating,
ExistsNoetherianSubringHomogeneousMatrixFlatChar, FiniteGrCechHomology,
ExistsDehomogenisationTwistedChart and ExistsTwistedSectionsCubeBijective.
The final return to Perf is NonemptyPerfectSectionsComplexOfSmoothProj.
A statement only for flat target rings or geometric fibers is insufficient.

4.2. Other geometric suppliers and their joins

The exact polarization base-change producer is
G/AbelianSchemeLawProofs/AbelianSchemeLawsWithoutCohomology.lean,
polBaseChange_holds. Preserve the Cartesian polarized record, dimension,
multiplication on every test scheme and the generated bundle isomorphism.
GSL15 and GSL20 already prove its needed projectivity and fiber returns.

The geometric-integrality input, Smooth plus GeometricallyConnected
implying GeometricallyIntegral, remains explicit in GSL19; it makes
multiplication by a nonzero section injective. The principal rank-one
input starts at FinrankSectionsPrincipalPolarisationEqOne
and its two suppliers FinrankPrincipalPolarisationSectionModuleLeOne and
OneLeFinrankSecM. The upper bound uses the actual Mumford bundle and
Kunneth. Preserve the source KTriv condition and all characteristics.
The complex theta classification alone is not this global theorem.
The actual torsion-indexed section decomposition and finite two-sided
growth then feed GSL18–GSL19, which already give the full n^g rank law.

For positive-power H1 vanishing, supply the original Serre statement,
multiplication-power generator, finite-flat-surjective multiplication
and every-open torsion-invariant function descent. For the geometric
twist, supply the square generator and multiplication geometry. GSL17
and GSL21 already prove the reductions from these inputs. GSL22 uses
the root only over an algebraically closed fiber; no root need lift to
the local coefficient ring. Once F,P,V,R,T exist, reuse GSL26 and NFL22
on the same supplied Moduli and normalized family.

4.3. Later geometry can proceed on supplied inputs

The actual Moduli and retained HUF/PUN foundations remain explicit.
The finite-level IsSystem is a useful independent bounded target:
G/SiegelThetaTransformation/HermitianThetaLevelDataFormsSystem.lean.
Its nine fields must use one fixed X,bas,idx,D,M,v0,mu. Subsequent
Gaussian/reproduction, simultaneous dictionaries, ramified jets,
all-tuple class sums and phase-sensitive uniqueness must retain both
levels, the whole coefficient field, Fits and eta agreement. A common
PointIdentCore must choose the same lambda and z for its consumers.
The base ClassSumsSpan and actual row installation remain separate.

5. ARITHMETIC PRIORITY: FinPt AND THE AUTOMORPHIC ENDPOINTS

AFE already supplies full gen_gd/gen_host, both original frame joins,
the auxiliary Host frame and local witnesses, all Marks fields,
exists_nrep3 and finEnd_of_finPt. The local Noetherian-domain scope
of NRep descent is preserved without extra flatness or completeness.
The Host branch includes ell=3; the CAF modulus is chosen before L,w;
the same C0,Phi,g1 and coefficient embedding remain fixed.

The next finite supplier is the actual FinPt on that Phi, defined in
A/CurveDVRSpecialization/PropagationTheoremGL2.lean. It is a universal
assertion for the source complete DVR coefficient points and their
original local inertia condition. Prove its producer from the actual
space and OffFin/patching hypotheses. AFE20 then gives FinEnd with
the single subgroup G_L chosen before all later algebras and points.
Do not count that completed transport as a proof of FinPt itself.

In parallel or after a finite packet, reconstruct the full AutPt-to-
AutEnd3/AutEnd2 transports, retaining the actual representation and
coefficient embeddings. RatTorsionFree.lean defines the exact endpoints;
OrthogonalPairingFromIntertwiner and AutEnd2OfAutPt are bounded starting
entries. The two actual automorphic seeds remain substantial:
A/IdeleGenerators/ShapeFacts.lean defines Seed2 and Seed3, including
arbitrarily high weights in the prescribed congruence class,
determinant/residual-sum conditions and rank-three open irreducibility.
These are representations, not CAF's already constructed character seed.

Then supply full PfromAut/ModUAlt, linked-end and local/automorphic
descent. Preserve the original P=GC.Hypotheses2 where it is used. The
same marked g1 must precede FinEnd, AutEnd3 and AutEnd2 in GdEnd.
LinkedEndEAlt/GdEndAlt retain their additional fields until proved at
their full source scope. UCE19 consumes one original GdEnd to give
the full joint FinA/AutB/LemW output at the fixed embedding.

6. ANALYTIC PRIORITY: THE ACTUAL GLOBAL SETTING AND COMPARISONS

BQS1–BQS23 now supply both full original QuotP/QuotM and the complete
StepStatement/BesselNVGap return. Their scopes include arbitrary input
tuples in the source Euler eigenspaces, every allowed incomplete
unitary target, actual compact-group stability and the simultaneous
kernel of all prescribed periods. These should not be new work cards.

ConcreteSettingExists retains the source Forms0 premise. The next
global source guide is bessel_quotient_suppliers_v52/next_source_handoff.txt.
Read the actual Forms0 and setting producers, orbital/fiber and
Siegel-Weil character/measure comparisons, Bessel uniqueness/local ties,
and full transport before deciding the next bounded proof endpoint.
Keep one representation, compact type, original Haar pair, character,
Cayley matrix, coefficient slots and all free translates.

The later AutTie/RowDictTie/LabTie and simultaneous arithmetic cylinder
counts for CountIdempotentsClass still require their literal common
family. Bessel nonvanishing is now available to these constructions;
it is not the global normalized spectral estimate. The latter still
requires exact Gamma normalization, off-diagonal Hilbert–Schmidt and
diagonal errors, and the Dall/Dstar bound at the original thresholds.
''']
tail=old[old.index('\n7. THE SEPARATE COUNTV'):old.index('\n11. COMPLETE OPEN WHOLE-OBLIGATION')]
tail=tail.replace('The completed conditional marked frame and the planned concrete Gen entries help this lane, but AUT_UNRAM_COEF alone',
 'The full AFE arithmetic entries and completed conditional marked frame help this lane, but AUT_UNRAM_COEF alone')
tail=tail.replace('The completed NFL uniformization and the remaining geometry tasks in section 4',
 'The completed conditional GSL section laws, NFL uniformization and remaining geometric suppliers in section 4')
tail=tail.replace('the denominator\nproducer of section 6','the denominator\nproducer of section 3')
parts.append(tail)
parts.append('\n11. COMPLETE OPEN WHOLE-OBLIGATION REGISTER AT v0.52\n')
for i,r in enumerate(reg['records'],1):parts.append(f"{i:02d}. {r['id']} [{r['category']}] — {r['title']}\n")
parts += [r'''
The full contracts and binding order remain in the dependency audit.
No newly completed local theorem changes this register by itself.
GLOBAL_LOCAL_GAIN is absent because its full closure is preserved.

12. NEXT ROUND AND ACCEPTANCE CRITERIA

Use at most four active agents including the coordinator. A useful
first wave assigns one bounded Wach layer/comparison theorem to the
coordinator, the actual geometric section-cube model to geometry,
FinPt or one original automorphic transport to arithmetic, and the
next actual global analytic setting/comparison to analysis. Decide
the bounded original endpoint before drafting. Later freed slots can
take independent Wach, principal-rank or finite-level suppliers.

Each packet must have a written ordinary proof, exact original source
scope, explicit retained inputs, common objects and order of choices,
source/proof hashes and review by another author. An existence wrapper
or an unrelated abstract object is insufficient. A shorter proof is
welcome when it proves the same needed interface. If it proves only
a sufficient instance, write the implication from that instance to
every affected consumer and update the route explicitly.

Freeze proof text before independent review. Integrate only complete
reviewed subtheorems, preserve all predecessor claims and proof body,
and update the original whole-contract register only when every field
and dependency is supplied. Draft TeX checks syntax and references;
it is not mathematical or formal verification. No Lean replay or PDF
is required. Save a cumulative checkpoint with updated roadmap,
parallel plan, exact source/proof ledger and continuation records.

13. CONTINUATION REFERENCES

increment_v0_52.json — current scopes and remaining producers.
continuation_checkpoint.json — exact status and next source targets.
global_section_laws_v52/next_source_handoff.txt — F/P/V/R/T producers.
selmer_signature_comparison_v52/wach_next_handoff.txt — dependent Wach layers.
bessel_quotient_suppliers_v52/next_source_handoff.txt — after local nonvanishing.
arithmetic_frame_entries_v52/contracts.json — original arithmetic scope.
arithmetic_frame_entries_v52/next_source_handoff.txt — finite and automorphic endpoints.
reviews_v0_52/review_registry.json — all new mathematical reviews.
validation_v0_52.json — preservation and independent release audit.
''']
road=ROOT/'RH_GRH_reconstruction_roadmap_v0_52.txt';road.write_text('\n'.join(parts))

plan=r'''RH / UNRESTRICTED DIRICHLET GRH: PARALLEL EXECUTION PLAN v0.52
23 November 2026

1. STARTING POINT

Continue the accepted reconstruction at pinned commit
7cbf7a0c32fca1badf05931879a37c3f8a2b03b4, using the full v0.52 archive.
The authoritative scopes are increment_v0_52.json, the component
contracts and RH_dependency_audit_v0_52.txt. This plan introduces no
new mathematical claim.

There are 3279 written claims after the 87 new v0.52 claims. The
selected graph remains 121 nodes and 161 edges, with 24 whole open
obligations: 17 shared RH/GRH and seven additional Dirichlet-GRH,
classified as 17 C and seven B. There are no RH-only open leaves.
Counts are inventories. GLOBAL_LOCAL_GAIN stays fully closed.

Reuse GSL's complete universal basis/section-model algebra and full
conditional section laws; AFE's full Gen entries, frame joins, NRep
descent and FinPt-to-FinEnd; BQS's full QuotP/QuotM, Step and BesselNVGap;
and SSC's full Selmer SignatureChoice. Preserve every printed premise.
In particular, the global geometric producers, P/FinPt and automorphic
seeds, Forms0/global analytic comparisons, and coherent Wach comparison
are still work. Do not assign the completed suppliers again.

2. CAPACITY AND INITIAL OWNERS

At most four active agents, including coordinator C. Initial workers
G, R and A own geometry, arithmetic and analysis. C owns a bounded
Wach packet and integration. Reviews occupy existing slots; do not
schedule a fifth worker or assume simultaneous drafting and review
capacity from the same author.

First wave:
 G — actual geometric section-cube/Noetherian model producer.
 R — actual FinPt producer or one full AutPt-to-AutEnd transport.
 A — one actual Forms0/setting or orbital/local-comparison producer.
 C — one original group/series, etale, lattice or comparison Wach packet.

These are independent at their exact inherited interfaces. Before
drafting, each owner names one complete source endpoint, its retained
inputs and its common objects. A deep packet may stop at a complete
conditional theorem with an explicit substantial producer remaining;
it must not label that producer closed.

After a packet freezes, review it before beginning a dependent join.
Freed slots can take additional Wach layers, principal rank one,
finite-level IsSystem, a second automorphic transport, or host-length
dictionaries. Do not synchronize unrelated packets unnecessarily.

3. G — ACTUAL GEOMETRIC SECTION MODEL

Start from global_section_laws_v52/next_source_handoff.txt. The target
ExistsFiniteProjectiveCechComplexLineBundle uses the original arbitrary
R, smooth X->Spec R, actual very-ample presentation H,s_i and actual M.
GSL10 already proves affine nonempty intersections for D(s_i).

Recommended bounded core: exists_noetherian_model_grCube in
CoherentCohomologyProofs/DehomogenisingCompOfSaturating. It must produce
one Noetherian R0, flat nonempty cube vertices, finite Cech cohomologies
and actual base-change bijections before any later R-algebra is chosen.
Trace the graded presentation, homogeneous-matrix flat descent,
finite graded Cech cohomology and dehomogenization suppliers. GSL8–10
then give the full finite-projective model and literal Perf record.

Do not replace arbitrary target algebras by flat or reduced targets.
Do not assert that a geometric-fiber rank calculation supplies Perf.
The return should identify the actual coordinate functions and
specified Cartesian maps used in every section comparison.

Independent later cards:
 G2 — full PolBaseChangeSt on the actual polarized record.
 G3 — geometric integrality and the principal rank-one theorem, then actual torsion section
      decomposition and growth; reuse GSL18–19 for n^g.
 G4 — original Serre/multiplication/invariant descent and square
      generator; reuse GSL17,21 for vanishing and twist reduction.
 G5 — finite-level IsSystem, all nine fields on one fixed record.

Only after F,P,V,R,T are supplied may GSL26 install the unconditional
laws for the actual family. Supplied Moduli and HUF/PUN foundations,
simultaneous dictionaries, class sums and rows remain separate.

4. R — FINITE POINTS AND THE AUTOMORPHIC ENDPOINTS (AUT_UNRAM_COEF)

AFE15–16 has already joined the original entries with the full LFC
frame and CAF seed. Fix that L,Phi,C0,g1 and coefficient embedding.
The Host route includes ell=3, and the modulus Q precedes L,w.

Choose one bounded endpoint before splitting effort:
 R1 — full FinPt on that Phi from its actual space/OffFin/patching
      producers. Read PropagationTheoremGL2's exact point scope.
      AFE20 already transports it to FinEnd on one G_L.
 R2 — full AutEnd3 transport, starting with the original orthogonal
      pairing/intertwiner and actual AutPt inputs.
 R3 — full AutEnd2OfAutPt, retaining the actual corner representation,
      trace-zero condition and coefficient embedding.

The source endpoint definitions are in CurveDVRSpecialization/
RatTorsionFree. The next seed work is IdeleGenerators/ShapeFacts,
Seed2/Seed3: representations of arbitrarily high congruent weights,
with the exact determinant/residual-sum and open-irreducibility fields.
CAF's character SeedClause does not supply those representations.

Later join full PfromAut/ModUAlt and actual local/automorphic descent
with one marked g1 before all outputs. Keep P and each unconstructed
seed explicit. The alternative LinkedEndEAlt/GdEndAlt fields are not
interchangeable with GdEnd without their original transport theorem.
UCE19 consumes a full GdEnd once it is supplied.

5. A — AFTER THE COMPLETE LOCAL BESSEL THEOREM

Start from bessel_quotient_suppliers_v52/next_source_handoff.txt.
Do not reopen Euler identities, K2/K3, QuotP/QuotM, the actual period
kernel quotient or Step/BesselNVGap. BQS keeps arbitrary original
eigenspace tuples and incomplete unitary targets, and supplies literal
smooth functions with both directions of their L2 image relation.

Choose the next exact global endpoint: actual Forms0 and setting,
one orbital/fiber or Siegel-Weil character/measure comparison, Bessel
uniqueness with local ties, or the full representation transport.
Read all original inputs before choosing a smaller calculation.
Keep the representation, compact type, coefficient slots, original
Haar pair, character, Cayley matrix and all allowed translates.

Later AutTie/RowDictTie/LabTie and CountIdempotentsClass require actual
simultaneous arithmetic cylinders and one compatible family. A local
nonzero vector does not prove their counts or GLOBAL_SPECTRAL.
The latter must retain exact Gamma normalization, off-diagonal
Hilbert–Schmidt and diagonal errors, Dall/Dstar and the original
exp(-x^(epsilon/8)) family bounds.

6. C — ONE BOUNDED WACH PRODUCER, THEN THE COMMON JOIN

SSC16 proves full SignatureChoice on the actual DFD family. SSC17
leaves coherent HW/Fon/Cmp at the setup step. Read
selmer_signature_comparison_v52/wach_next_handoff.txt and the full
dependent Layers record before selecting a core theorem.

The local assembly has four substantial supplier groups:
 W1 — actual Gamma, series and embeddings, including all level
      expansions and the source ell=2 branches.
 W2 — FaithH, actual invariant etale bases, then the full WEt functor.
 W3 — WachEx at every original Gamma/R/I/E, including projectivity,
      both Frobenius inclusions, all lattice maps, trivial object and
      the prescribed noncrystalline branch.
 W4 — Herr class maps and WCmp, including the literal representative
      identities and quantitative de Rham filtration remainder.

The initial coordinator should own one of W1–W4, not promise all
four at once while reviewing the other project lanes. The other cards
can use slots released by completed and reviewed packets. Generic
conditional constructions may be proved independently on supplied
records, then joined only when those exact records are available.

The source exists_of_layers permits one complete dependent record per
Good(K,s,LL). Do not add a nonexistent extra transition-system demand.
Internal compatibility of Gamma,R,I,E,Mo,Cl,Cm and all lattice maps is
mandatory. DFD12 already gives the full coefficient extension of the
original integral Bhatt-Scholze input; it does not give WN or WCmp.

After the full triple is produced on the original D, use SSC17 and
DFD to form Setup. Prove all fifteen Concl fields on that same family,
with one C,x0 before every x,hx,i. Preserve ShaFinOdd, actual exceptional
sets, the 1/ell^2 oriented budget and vvTerm summability. DNE14 already
supplies the complete export with K=2000(|Ca|+1)^3 before every family.

7. ROLLING QUEUE THAT MUST STAY VISIBLE

Host/CountV: THM_S6_S, HOST_NUMBER_S, HOST_FRAME_LENGTH,
TASK_HOST_VAN_E_INSTALL, TASK_HOST_XPP_INSTALL and TASK_COUNT_V_INSTALL.
The ordinary-RH specialization includes e=1 and ell in {3,7} with
unbounded dyadic conductor. AFE's full Host entries preserve this;
they do not yet install all count and normalized-length conclusions.

Common family: DESIGN_CHOICES_COMMON, LOCAL_NBUILT_COMMON,
SECOND_LAYER_COMPATIBLE_SELECTION, BASE_THETA_READINGS,
BASE_THETA_RATIONAL_TESTS and SLR_BASE_ROWS_PRODUCER. Preserve one
Bundle, both levels, whole coefficient field, actual lattice and maps,
Fits, eta agreements, metric/measure choices and common thresholds.

Global estimates: GLOBAL_DENOMINATOR, GLOBAL_RETAINED_DEFECT,
GLOBAL_PERIOD_HEIGHT and GLOBAL_SPECTRAL remain distinct. The full
GLOBAL_LOCAL_GAIN theorem stays closed at its original selected-member
scope; stronger common-family tasks do not become new premises for it.

Additional GRH: SEED_IV_ALT, TENSOR_FACTOR_TOWER, CHAIN_RANK_FOUR,
CHAIN_DESC4, RANK4_CHAIN_REDUCTION, TASK_CASE3_PROMOD_JOIN and
TASK_CASE3_AUT_JOIN. Preserve fixed iota, same-object support and the
original Case-III/rank-four interfaces. These can receive freed slots;
they should not disappear while shared RH tasks are pursued.

8. REVIEW, FREEZE AND RELEASE

Each author provides main.tex, claim/proof ranges, exact original
source ranges at the pin, dependency references, contracts, retained
inputs and a concise next-source handoff. Claims must contain ordinary
proofs; naming a formal producer is not its expository reconstruction.
Choose claims around mathematical results, not around desired counts.

Suggested review rotation uses existing workers: C reviews G and R;
G reviews A; R reviews C. Each review records all exact proof-block
hashes and the original quantified scope. An author may also perform
routine integrity checks, but that is not independent mathematical
review. A correction changes the frozen hash and must be rechecked.

After review, C integrates, preserving all 3192 predecessor claims
and, for the next round, all 3279 v0.52 claims without alteration.
For the next release the direct predecessor baseline is v0.52.
Check acyclicity, inherited proof/ledger bindings, source snapshots,
the unchanged historical proof body and the original whole register.
A separate worker audits the integrated release before packaging.

Draft TeX checks syntax and references with no new overfull boxes.
No Lean replay or PDF is needed. Do not broaden tests after the
identified release risks are resolved. Save the cumulative archive,
incremental and cumulative TeX, progress, current roadmap, parallel
plan, dependency audit and exact delivery record. An unresolved whole
producer remains open even when a substantial conditional theorem
inside it has been completed and reviewed.
'''
dest=ROOT/'RH_GRH_parallel_execution_plan_v0_52.txt';dest.write_text(plan)
print(json.dumps({'roadmap_words':len(road.read_text().split()),'parallel_plan_words':len(plan.split())}))
