#!/usr/bin/env python3
"""Write the current producer roadmap and a concrete four-slot next-wave plan."""
from pathlib import Path
import json
ROOT=Path(__file__).resolve().parent
cfg=json.loads((ROOT/'increment_v0_55.json').read_text())
st=json.loads((ROOT/'integration_stats_v0_55.json').read_text())
reg=json.loads((ROOT/'dependency_audit_v0_55/remaining_leaf_register.json').read_text())
parts=[
 'RH AND UNRESTRICTED DIRICHLET GRH — RECONSTRUCTION ROADMAP v0.55',
 '23 November 2026','',
 'Purpose: continue the full human reconstruction of the accepted Alpoge–Claude formal proof, keeping the detailed proof-note style. This roadmap is based on RH_reconstruction_v0_55.zip and supersedes the v0.54 task frontier. It assigns future research; it does not add proof claims.','',
 'Repository: https://github.com/CocoSgt/riemann-hypothesis-lean',
 'Accepted source pin: '+cfg['source_commit'],'',
 '1. CURRENT STATE','',cfg['status'],'',
 'Read RH_reconstruction_progress_v0_55.txt for the mathematical explanation, RH_new_proofs_v0_55.tex for every new proof, and RH_readable_reconstruction_v0_55.tex for the cumulative manuscript. RH_dependency_audit_v0_55.txt contains every open whole contract. The graph remains 121 nodes and 161 edges, with 24 whole obligations. A named nested producer can now be complete even while other independent inputs to its whole obligation remain.','',
 'Do not reassign the original Serre H1 theorem, high-power homogeneous polynomial theorem, actual arithmetic loc_cpl/LocFlat/types/LocRho/loc_ex, conditional stabilizer-volume theorem, actual InVolumes join, or invariant Frobenius-matrix descent as missing. SHV, ALC, SVW and IFD supply them. ASL Perf, RTC upstream coefficient rings/preconnectedness/FinPtDown, AOS orbital scalar, WIS inclusion/completeness and the full v0.49 GLOBAL_LOCAL_GAIN closure remain available at their original scopes.','',
 '2. READ THE NEXT CONSUMER BEFORE EXPANDING ITS PRODUCERS','',
 'For each task, print the exact original output, all antecedents, the common objects and the order of choices. Read the producer and its next use together. Give every common construction one owner; workers may prove independent properties of that construction or independent suppliers on the same original data. Do not make unrelated choices of frames, coefficient fields, measures or thresholds and assume they match later.','',
 'A simplification is useful when its precise implication to the original consumer is proved. In v0.55 the actual universal maps fix the arithmetic completion; one finite graded model fixes the degree bound before all sections; determining admissible tests identify every supplied Gram measure; and exact fixed sharp-root coordinates reuse the completed fixed-field theorem. These changes remove proof work without adding a substitute hypothesis.','',
 'Use substantial original producers as units of progress. A wrapper with unproved antecedents is a consumer map, not a newly completed mathematical construction. Keep the supplied-data boundary visible and retire current-frontier flags when a supplier is genuinely completed. Preserve old proof records as historical statements.','',
 '3. GEOMETRY: POLARIZED BASE CHANGE AND THE REMAINING SECTION LAWS','',
 (ROOT/'serre_h1_v55/next_source_handoff.txt').read_text(),'',
 'Recommended next assignment: the full arbitrary-base local-to-global relatively ample construction, followed by every field of PolBaseChange. This can run independently of the local period prism, arithmetic dimensions and reference-volume work. It must preserve the actual Cartesian group-scheme square, the same line bundle, rigidification, symmetry and relative dimension. The Noetherian condition used by the later Serre theorem must not be added to this arbitrary-base producer.','',
 'A second geometry worker, if a slot becomes free, may take the exact finite polynomial-image growth theorem and the smooth transcendence-degree identification. Join them only through the original SecM evaluation, same scalar maps and same dimension g. Neither monomial counting in the number of projective coordinates nor the complex Fourier rank on a selected family proves the original all-characteristic principal rank theorem.','',
 'Finite-level systems remain a later independent task at Proofs/SiegelThetaTransformation/HermitianThetaLevelDataFormsSystem.lean. Preserve one X,bas,idx,D,M,v0,mu through all nine fields and then through Gaussian/reproduction, ramified jets, simultaneous dictionaries, class sums and phase-sensitive uniqueness. The completed Perf and Serre statements do not themselves construct these family systems.','',
 '4. ARITHMETIC: COMPONENT BOUNDS, DIMENSIONS, DENSITY AND PROPAGATION','',
 (ROOT/'arithmetic_local_charts_v55/next_source_handoff.txt').read_text(),'',
 'The current arithmetic entry includes the full RTC pre-FinA coefficient/graded-ring inputs and full ALC actual local objects. Work should now begin at the exact component/dimension or seed producer still required by ComponentsGoodRankTwo and its rank-three return. Preserve the original chosen A, coefficient ideal, closed point and map A to the constructed local ring. The component charts are available; numerical lower bounds and global incidence are independent statements.','',
 'The rank-two and rank-three coefficient extensions need not be the same. Each construction returns to the original common marked frame through its proved maps. Preserve arbitrary target fields and arbitrary ring maps A to K in the type theorem, the original arithmetic P premise where used and the allowed Host prime 3. Full FinPtDown is complete and must be used in the eventual return, not left as an opaque coefficient-descent premise. Existence of universal spaces, actual automorphic seeds, patching/modularity and classicality remain distinct.','',
 '5. ANALYSIS: REALBRACKET AFTER THE ACTUAL VOLUME JOIN','',
 (ROOT/'stabilizer_volume_v55/next_source_handoff.txt').read_text(),'',
 'The default analytic assignment is the reference unipotent covolume and discriminant calculation, followed by its literal CovolRef return. This is independent of the geometry, arithmetic and prism work. A second analytic worker can prove the broad local Jacobian/PlaceSplit or the full ProdExact theorem. Keep one GMR19 output, one character, both words, both infinity-domain witnesses and the original auxiliary tuple common to all joins.','',
 'The arithmetic InVolumes record has all its measure inputs on the existing GMR19 output. Do not normalize the unipotent measure again for that join. Its reference archimedean covolume in RealBracket is a different prescribed quantity and still needs its determinant calculation. The original smooth Siegel–Weil density premise is retained; completing its volume consequence does not prove the premise itself.','',
 '6. DENOMINATORS: THE ACTUAL PRISM, THEN COMPARISON AND ONE FAMILY','',
 (ROOT/'invariant_frobenius_descent_v55/next_source_handoff.txt').read_text(),'',
 'Write I=src/Development/AbelianVarietyTheory/Proofs/InertiaEigenvalues/ and N=src/Development/AbelianVarietyTheory/Definitions/NonGaloisDescent/. The next local producer is I/ExistsWachPrismOverIntegers.lean, exists_prism, and the corresponding full exported exists_wach_prism_over_integers interface. Read both the construction and I/WachLatticesExistAllLayersOfBhattScholze.lean before choosing auxiliary coordinates.','',
 'Prism acceptance scope: construct the original local prism, its specialization kernel and Frobenius ideal generator, the map to LetA, Galois maps, finite-free power-series coordinates and both coefficient decompositions. Prove the equality of the composite scalar map with the original zlA. Keep the original local data, cyclotomic parameter, coefficient extension and prescribed ring maps. A generic prism of the same rank does not supply these fields.','',
 'IFD25 already proves the full inhomogeneous fixed-matrix descent; its Y=0 specialization supplies precisely the homogeneous input of WLD26. WIS18 already supplies inclusion and unit reflection. Thus the actual prism is the one remaining period-ring supplier before IFD26/WLD26 returns full WachEx for every original layer and every supplied etale module. The return still retains LocTied/IsStd and the original crystalline-lattice realization premise.','',
 'After WachEx, take separate substantial producers for FaithH, EtBasis, Herr class maps and quantitative de Rham comparison. They must provide one complete HW/Fon/Cmp triple with the original maps. N/ExistsOfLayers chooses a complete dependent record at each original Good index; do not invent a separate transition system between different outer indices. The later constructor needs the full record at each index, not a loose collection of equivalent objects.','',
 'Then assemble the original quantitative family using SSC17 and DFD. Keep one SignatureChoice, complements, NChoice and exceptional set. The fifteen Concl fields are pos, pass, mult, rank, kill, num, mid, bb, large, exc, two, ram, typ, par and small. Fix C and x0 before every later x and index. Retain ShaFinOdd and summability. RowNum, StarAD, BB and the actual large/exceptional/ramified/type estimates remain. Apply DNE only after ConclF exists, with K=2000(|Ca|+1)^3 fixed before the family.','']
old=(ROOT/'RH_GRH_reconstruction_roadmap_v0_54.txt').read_text()
tail=old[old.index('7. THE SEPARATE COUNTV HOST AND SUPPORT LANE'):old.index('11. COMPLETE CURRENT WHOLE-OBLIGATION REGISTER')]
tail=tail.replace('RTC core/coefficient descent and completed conditional marked frame help this lane,','RTC core/coefficient descent, ALC actual local charts and completed conditional marked frame help this lane,')
parts += [tail,'11. COMPLETE CURRENT WHOLE-OBLIGATION REGISTER','']
for i,r in enumerate(reg['records'],1):
    parts.append(f"{i:02d}. {r['id']} [{r['category']}] — {r['title']}")
parts+=['',
 'All 24 remain open at their whole original contracts. The current register and route coverage are in dependency_audit_v0_55. There are 17 shared RH/GRH leaves and 7 additional unrestricted Dirichlet-GRH leaves, with 17 class C and 7 class B. Counts are an inventory, not a completion estimate.','',
 '12. ACCEPTANCE AND CONTINUATION','',
 'An accepted packet contains a readable theorem and proof, its exact original target and next use, every retained input, exact proof/source bindings, mathematical dependencies and an independent review. The reviewer must check the argument, its quantifier scope and its common-object return. Source snapshots establish provenance and target scope; they do not replace the human proof.','',
 'When a simpler proof supplies the original statement, explain the simplification and its exact return. When a packet stops at a missing producer, state that producer’s mathematical content and call site. Do not promote a new omnibus assumption into a proof. Keep all predecessor claim objects and source pins intact; update the current frontier separately. Continue toward the complete human proof of RH and unrestricted Dirichlet GRH in the same detailed style.','']
road=ROOT/'RH_GRH_reconstruction_roadmap_v0_55.txt'
road.write_text('\n'.join(parts))

plan="""RH AND UNRESTRICTED DIRICHLET GRH — PARALLEL EXECUTION PLAN v0.55
23 November 2026

This plan is based on RH_reconstruction_v0_55.zip and its current roadmap.
Accepted source pin: 7cbf7a0c32fca1badf05931879a37c3f8a2b03b4.
The goal is the complete human reconstruction in the detailed proof-note
style. This plan assigns future work and makes no additional proof claims.

CURRENT INVENTORY

87 new claims; 3538 cumulative claims; all 3451 predecessor claim records
preserved. The selected sufficient graph has 121 nodes and 161 edges.
24 whole obligations remain: 17 class C and 7 class B; 17 shared RH/GRH
and 7 additional unrestricted Dirichlet-GRH inputs, with none RH-only.
GLOBAL_LOCAL_GAIN remains fully closed from v0.49.

1. FOUR ACTIVE SLOTS AND COMMON-OBJECT OWNERSHIP

Use one coordinator and three workers. The coordinator owns a mathematical
task as well as integration. Assign one owner to every common construction.
Other workers can prove independent suppliers or independent properties
of that same original object. Do not choose unrelated coefficient rings,
frames, measures, periods or thresholds and hope to identify them later.

Read the substantial original producer and its next consumer before
expanding proof dependencies. A short wrapper is not an adequate task
completion when its main mathematical antecedents remain unproved.
Prefer a full named endpoint; a sufficient specialization needs a written
implication to the exact original next use.

2. DEFAULT NEXT WAVE

Coordinator — actual Wach prism.

  Start with Proofs/InertiaEigenvalues/ExistsWachPrismOverIntegers.lean
  in src/Development/AbelianVarietyTheory/, and read its consumer
  WachLatticesExistAllLayersOfBhattScholze.lean.
  Target the full original exists_wach_prism_over_integers interface:
  the local prism, specialization kernel, Frobenius ideal generator,
  Galois actions, actual map into LetA, scalar identity and both finite
  coefficient-coordinate decompositions.
  Preserve the supplied P,AI,K,s,LL,Gamma,R,I, parameter and embeddings.
  WIS inclusion/completeness and IFD full invariant matrix descent are
  already proved. Do not recreate them as new missing obligations.
  Acceptance: every original prism field and the exact IFD26/WLD26
  return to all-layer WachEx, retaining original LocTied/IsStd and
  crystalline realization. Later FaithH/EtBasis/Herr/Cmp remain distinct.

Worker G — full polarized base change over arbitrary base schemes.

  Read Proofs/AbelianSchemeLawProofs/RelAmpleOfLocallyOnBase.lean,
  especially glue_pack, exists_sv and relAmple_of_locally, then
  PolBaseChangeOfRelAmpleLocal.lean, polBaseChange_of_relAmple_local.
  Prove the actual finite principal-cover construction of an ample pack,
  synchronize its powers and glue its sections, then return all original
  coordinate-surjectivity and generated-bundle fields.
  Keep the specified Cartesian group-scheme square, actual line bundle,
  rigidification, symmetry, KTriv and the same relative dimension.
  Acceptance: the complete original arbitrary-S and arbitrary-S-prime
  PolBaseChange producer, without adding Noetherianity or smoothness
  beyond its original hypotheses.
  SHV both Serre conjuncts and ASL Perf are complete inputs. GSL17 still
  needs its independent multiplication and invariant-function descent.

Worker A — sharp component and dimension inputs on the actual charts.

  The preferred first target is FrobeniusSmoothVectors/HasObs.lean,
  pres: construct the original local deformation presentation, with
  a surjection O'[[X_1,...,X_N]] onto the actual L.R, its N' specified
  kernel generators, and the exact relation N=N'+n*d+1.
  Independent alternatives are EnnrealVolumeRatioStepCancel.lean,
  c1ch, with its actual ClComp/ClChain bodies, and the l51/l52 dimension
  bounds in CharpolyCoeffsInSubalgebra.lean and TameInertiaCondition.lean.
  Read their next joins in ChainedBot.lean and KrullDimLtOfNotLeTriangular
  before expanding dependencies. The ALC handoff gives exact paths.
  Reuse RTC upstream wpres/co_B/gr_A/cont_u and preconnected core,
  plus ALC actual loc_ex, completion, flatness, types and LocRho.
  Work on the original A,B, coefficient ideal, closed point and map to
  its actual local coefficient ring. Establish the precise chain or
  dimension bound required by that propagation consumer.
  Acceptance: the original numerical and prime-component quantifiers,
  with no finite-point conclusion imported upstream.
  Keep global density and seed incidence explicit if their producers
  are independent. Preserve rank-specific coefficient rings and ideals,
  the common marked frame, original arithmetic P and Host prime 3.
  A local chart theorem by itself is not full propagation or OffFin.

Worker V — prescribed reference unipotent covolume and discriminant.

  Write N=src/Formalism/LocalToGlobal/SiegelLatticeTheory/
  CokernelGLCounts/RankPointCounts/DualFamilyCounting/.
  Start with NcRealXPS.lean, CovolRef, and NcRealXCR.lean.
  Read N/RefNBoxOf.lean, N/CovolNOfSteps.lean, the parent
  RankPointCounts/CoordCovolOf.lean, and N/CovolBR/b/c.
  Target the exact reference-box factor
      Tw(w)^(-r*d) * 2^(d*(r*k+r^2))
  and the original discriminant exponent, on every permitted domain.
  Preserve the independent reference word u and lattice word w; a
  proof only at u=w is weaker than the consumer.
  Acceptance: full CovolRef with the original Haar/coordinate-lattice
  data, then its exact RealBracket input.
  AOS exact orbital scalar and SVW actual InVolumes join are complete.
  Existing unipotent covolume-one normalization on GMR19 is not the
  reference archimedean determinant calculation asked for here.

3. READY ALTERNATIVES WHEN A WORKER FINISHES

Geometry: FinrankTotalDegreeImageGrowth and the smooth transcendence-
degree theorem, followed by their actual SecM consumer. Keep both
growth bounds and exponent equal to the actual relative dimension,
not the number of projective coordinates. Other independent packets
are geometric integrality, principal rank one, multiplication/invariant
descent and square/translation generators.

Analysis: the broad JacGauge and actual moving-ball limiting integral,
then PlaceSplit; or the full ProdExact theorem at arbitrary supplied
sigma-finite factor measures and all permitted sections. Fix the
GMR19 setting, common character, both words and original infinity
measures. Do not restrict ProdExact to one convenient factorization.

Arithmetic: once the component bounds are available, supply the exact
global density/seed incidence, complete rank-two propagation, and then
the rank-three corner, exceptional ideal and propagation. Full FinPtDown
is already available for return to the original marked coefficient frame.
Actual automorphic seeds, patching/modularity, classicality and the
stronger Alt witness outputs remain separate.

Periods: after the actual prism, choose a complete original FaithH,
EtBasis, Herr-map or quantitative-comparison producer. Only then
assemble HW/Fon/Cmp and the common ConclF family. Do not invent
an extra compatibility system between outer Good indices.

4. CROSS-REVIEW AND JOIN ORDER

When a mathematical chapter is frozen, send the final manuscript and
its target contract to another worker. Use the cycle:
  A reviews G; V reviews A; coordinator reviews V; G reviews coordinator.
Every reviewer checks each numbered proof, its original quantifier
scope, retained premises and the maps to the actual next use.
Bind the review to the final file and each numbered proof block.
The author's own validation is useful but is not independent review.

An idle worker may instead perform the independent integration audit.
It must preserve the current source pin and all predecessor claim
objects, check exact source/proof ranges, acyclicity of the human
dependency graph and the whole-obligation register, and verify that
current remaining-input flags no longer list newly completed producers.
Historical conditional proofs and frontiers remain unchanged.

Keep joins mathematical. The new prism should feed IFD26/WLD26
directly. Polarized base change should feed the actual GSL framework.
Component bounds should feed the supplied actual local charts.
Reference volumes and place splitting should feed RealBracket on
the same GMR19 output that already has AOS and SVW conclusions.

5. COMMON FAMILY AND UNRESTRICTED GRH STAY IN THE QUEUE

The 24 whole obligations remain the work inventory. Do not spend
successive waves only on a terminal specialization and lose the common
family or the seven additional GRH inputs. A bounded host dictionary,
coefficient transport or finite-field seed task may be assigned as a
worker becomes free, with its exact original common data.

For CountV keep the actual host/frame/local conditions and normalized
Selmer length. Preserve the ordinary-RH specialization with e=1,
ell in {3,7}, and unbounded dyadic conductors. The selected rank-four
support theorem is not the general rank-three host theorem.

For the common family, construct one DesignChoices/Bundle and the
original compatible selection before invoking row and local-specialization
consumers. Keep both rational-test levels, whole coefficient fields,
Fits, eta agreements, metrics, measures, phases and thresholds.
Do not add this stronger family-existence condition as a new premise
to the already fully closed GLOBAL_LOCAL_GAIN estimate.

6. REQUIRED HANDOFF

Each component supplies:
  - the readable full theorem and proof, numbered for stable citation;
  - the exact original producer and next consumer, with all assumptions;
  - source pin, full-file and range hashes, proof-block hashes;
  - mathematical dependencies on prior human proofs;
  - completed outputs, retained inputs and exact next-source tasks;
  - independent review at the final proof hash;
  - draft TeX syntax/reference checks if the manuscript changes.

The release preserves the cumulative manuscript and produces the new
proof edition, progress report, roadmap, parallel plan, complete audit,
archive manifest and delivery record. No Lean replay or PDF claim is
needed. Claim counts are inventories and no whole closure is inferred
from completion of a proper subtheorem.

COMPLETE CURRENT WHOLE-OBLIGATION INVENTORY

"""
for i,r in enumerate(reg['records'],1):
    plan+=f"{i:02d}. {r['id']} [{r['category']}] — {r['title']}\n"
plan+='\nAll remain open at their full registered scopes. The roadmap and audit give their contracts and the exact common objects.\n'
dest=ROOT/'RH_GRH_parallel_execution_plan_v0_55.txt'
dest.write_text(plan)
print(json.dumps({'roadmap_words':len(road.read_text().split()),
 'parallel_plan_words':len(plan.split()),'roadmap':road.name,'plan':dest.name}))
