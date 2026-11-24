#!/usr/bin/env python3
"""Write the v54 roadmap and four-slot plan from the frozen current packet."""
from pathlib import Path
import json

ROOT = Path(__file__).resolve().parent
cfg = json.loads((ROOT / 'increment_v0_54.json').read_text())
st = json.loads((ROOT / 'integration_stats_v0_54.json').read_text())
reg = json.loads((ROOT / 'dependency_audit_v0_54/remaining_leaf_register.json').read_text())
parts = [
'RH AND UNRESTRICTED DIRICHLET GRH — RECONSTRUCTION ROADMAP v0.54',
'23 November 2026', '',
'Purpose: continue the complete human reconstruction of the accepted Alpoge–Claude formal proof. Keep the detailed proof-note style. This roadmap is based on RH_reconstruction_v0_54.zip and supersedes the v0.53 task frontier. It is guidance for future work, not an additional proof.', '',
'Repository: https://github.com/CocoSgt/riemann-hypothesis-lean',
'Accepted source pin: ' + cfg['source_commit'], '',
'1. CURRENT STATE', '', cfg['status'], '',
'The new proof edition is RH_new_proofs_v0_54.tex; the cumulative edition is RH_readable_reconstruction_v0_54.tex. The progress report explains the constructions and their limits. RH_dependency_audit_v0_54.txt prints every remaining whole contract. The selected sufficient graph remains 121 nodes and 161 edges, with 24 whole open obligations. Completion of a nested producer does not imply completion of the whole obligation that consumes it.', '',
'The full original Perf producer, preconnected_rank_two, FinPtDown, exact archimedean scalar and four-clause Wach inclusion are now available. Do not assign them again as missing work. Original input records still have to be supplied where their existence is an independent obligation. All historical proofs, including the complete v0.49 GLOBAL_LOCAL_GAIN closure, retain their original scope.', '',
'2. WORK BACKWARD FROM THE ACTUAL NEXT CONSUMER', '',
'For each proposed task, state the exact output, all antecedents, the common objects and the order of choices before expanding a proof. Read both the producer body and its next use. A short wrapper identifies a join but does not substitute for its substantial inputs. A useful packet removes one named mathematical premise from the next consumer and supplies its human argument at the original scope.', '',
'Give each common construction one owner. Other workers can prove independent properties of that object or independent suppliers on the same original data. They should not make unrelated choices of frames, coefficient fields, periods, measures or thresholds and assume them compatible afterward. If a simpler construction is used, prove the precise transport or implication needed by the original next use.', '',
'The current examples are concrete: finite powers clear section denominators and overlap discrepancies; a formal polynomial family gives a common generic arithmetic prime; comparison of two local densities computes the prescribed orbital scalar; and a finite multiplication determinant supplies the Jacobson property needed by the actual period embedding. These are mathematical simplifications with explicit consumer joins.', '',
'3. GEOMETRY: SERRE H1 AND THE INDEPENDENT POLARIZATION/RANK INPUTS', '',
(ROOT / 'actual_section_localization_v54/next_source_handoff.txt').read_text(), '',
'The original global section-law F input is fully supplied. The next packet should not recreate its finite-projective model. The all-cover Serre H1 producer is a bounded route to a separate missing input, while PolBaseChangeSt and the principal rank-one arguments can be assigned independently when slots are available. The component handoff distinguishes the two directions of change-of-cover and records the original arbitrary-base scopes.', '',
'Finite-level IsSystem remains a later independent target at Proofs/SiegelThetaTransformation/HermitianThetaLevelDataFormsSystem.lean. Preserve one X,bas,idx,D,M,v0,mu through all nine fields and then through the Gaussian/reproduction, ramified jets, dictionaries, class sums and phase-sensitive uniqueness. Completion of Perf does not install those family systems.', '',
'4. ARITHMETIC: ACTUAL LOCAL CHARTS, DIMENSIONS AND PROPAGATION', '',
(ROOT / 'rank_two_connectedness_v54/next_source_handoff.txt').read_text(), '',
'The upstream guard has changed: wpres/co_B/gr_A/cont_u are now proved at their original pre-FinA scope. Reuse RTC, not the analogous UCE13 statement that assumes FinA. Actual loc_cpl and LocFlat/LocRho remain independent mathematical statements. Preconnectedness supplies the actual core field, not seed incidence or propagation through every component. FinPtDown is complete and must not remain an opaque assumption in the eventual return to the original marked frame.', '',
'5. ANALYSIS: REALBRACKET AND ARITHMETIC STABILIZER VOLUMES', '',
(ROOT / 'archimedean_orbital_scalar_v54/next_source_handoff.txt').read_text(), '',
'The exact infinity scalar and all-section integration clause are now complete. Use the same setting, bridge, character and prescribed infinity measures. The arithmetic volume card can run independently of the unipotent discriminant/JacGauge cards, at its stated original Siegel–Weil premises. Any finite fundamental-domain mass needed in a volume proof must be derived at the proper stage, not assumed as part of the normalization being proved.', '',
'6. DENOMINATORS: THE TWO PERIOD-RING SUPPLIERS AND LATER COMPARISON', '',
(ROOT / 'wach_inclusion_saturation_v54/next_source_handoff.txt').read_text(), '',
'Write I=src/Development/AbelianVarietyTheory/Proofs/InertiaEigenvalues/ and N=src/Development/AbelianVarietyTheory/Definitions/NonGaloisDescent/. The actual Wach prism and the homogeneous invariant-matrix descent are independent on the original supplied period data. Either can be assigned first; a free worker can take the other. WIS and WLD are completed inputs to both joins.', '',
'Prism card: I/ExistsWachPrismOverIntegers.lean, exists_prism. Construct the original local prism, specialization kernel, Frobenius ideal generator, map to LetA, Galois maps, finite-free power-series coordinates and both coefficient decompositions. The identity of the composite scalar map with the original zlA is part of the output. Keep the same original local data, parameter and coefficient extension; an abstract prism with a similar rank does not supply this theorem.', '',
'Invariant-matrix card: I/FixedByCyclotomicKernelEtalePhiSolutionMemWach.lean. WLD26 needs the homogeneous case for all original matrix ranks and layers. The completed WIS fixed/NearPi completeness inputs are available, but FrobeniusConstantsPiAdicFiltrationModEll, actual invariant approximation through TiltInvariantApproxByEpsilonRootsClosure, the near_closed argument with its const_dvd input, and the matrix lifting theorem still require their human proofs. Read how these inputs enter before choosing whether to prove the broader inhomogeneous source statement. A homogeneous specialization is acceptable only with its exact implication to the original WLD26 consumer.', '',
'The return retains original LocTied/IsStd and the Bhatt–Scholze crystalline-realization input. With both period-ring suppliers, WIS26/WLD26 gives full WachEx for every supplied original etale record. The subsequent FaithH, EtBasis, Herr class maps and quantitative de Rham comparison are still required for one complete HW/Fon/Cmp triple. N/ExistsOfLayers chooses a complete dependent record at each original Good index and adds no unspecified transition system between different outer indices.', '',
'After that comparison, SSC17 and DFD provide the original family setup with the same SignatureChoice, complements, NChoice and exceptional sets. The fifteen Concl fields must then hold on one common family: pos, pass, mult, rank, kill, num, mid, bb, large, exc, two, ram, typ, par, small. Fix C and x0 before all later x and indices. Retain ShaFinOdd and summability. RowNum, StarAD, BB and the actual large/exceptional/ramified/type estimates remain producers. Apply DNE only after ConclF exists, keeping K=2000(|Ca|+1)^3 fixed before the family.', '']
old = (ROOT / 'RH_GRH_reconstruction_roadmap_v0_53.txt').read_text()
tail = old[old.index('7. THE SEPARATE COUNTV HOST AND SUPPORT LANE'):old.index('11. COMPLETE CURRENT WHOLE-OBLIGATION REGISTER')]
tail = tail.replace('The full AFE arithmetic entries, ACP abstract implications and completed conditional marked frame help this lane,',
                    'The full AFE arithmetic entries, ACP abstract implications, RTC core/coefficient descent and completed conditional marked frame help this lane,')
parts += [tail, '11. COMPLETE CURRENT WHOLE-OBLIGATION REGISTER', '']
for i, r in enumerate(reg['records'], 1):
    parts.append(f"{i:02d}. {r['id']} [{r['category']}] — {r['title']}")
parts += ['',
'All 24 remain open at their whole original contracts. The current register and route coverage are in dependency_audit_v0_54. Counts do not estimate the work remaining.', '',
'12. ACCEPTANCE AND CONTINUATION', '',
'An accepted packet contains the readable theorem and proof, the original target and exact next use, all retained inputs, exact source/proof bindings, mathematical dependencies and a review by someone other than its author. Source declarations fix target scope; they do not replace the human proof. A full endpoint keeps its original quantifiers and common objects. A sufficient specialization needs its explicit implication to the actual consumer.', '',
'If a task reaches an unproved producer, state its mathematical content and where it enters. Do not hide it in a newly named omnibus hypothesis. Preserve old proof bytes and update the current scope separately. Retire obsolete current-frontier booleans when a formerly missing supplier is now complete; keep historical records unchanged. Continue toward the full human proof of RH and unrestricted Dirichlet GRH in the same readable style.', '']
road = ROOT / 'RH_GRH_reconstruction_roadmap_v0_54.txt'
road.write_text('\n'.join(parts))

plan = r'''RH AND UNRESTRICTED DIRICHLET GRH — PARALLEL EXECUTION PLAN v0.54
23 November 2026

This plan is based on RH_reconstruction_v0_54.zip and its current roadmap.
Accepted source pin: 7cbf7a0c32fca1badf05931879a37c3f8a2b03b4.
The objective is the complete human reconstruction in the detailed proof-note
style. This plan assigns future work and does not assert new proof closures.

1. CAPACITY AND COMMON-OBJECT OWNERSHIP

Use four active slots: one coordinator and three workers. The coordinator
owns a mathematical task and the integration. Each common construction has
one owner; independent properties and original suppliers may be proved in
parallel on that fixed object. A finished worker can review another chapter.
Do not count an author's self-check as independent mathematical review.

Use a named substantial original producer and its next consumer as the unit
of progress. Claim counts are an inventory. A wrapper with unproved premises
does not meet an assignment merely because its Lean declaration is short.

2. DEFAULT NEXT WAVE: FOUR INDEPENDENT PRODUCERS

Coordinator — remaining invariant Frobenius-matrix descent.
  Work on the actual supplied Gamma,R,I and coefficient maps.
  Target the homogeneous specialization of
  InertiaEigenvalues/FixedByCyclotomicKernelEtalePhiSolutionMemWach.lean
  required by WLD26, at every original rank and permitted layer.
  Reuse all WIS inclusion, fixed-mod-p lifting and NearPi completeness
  results. Read the Frobenius-filtration, actual invariant approximation,
  const_dvd/near_closed and matrix-lifting producers before expanding.
  Acceptance: return every original kernel-fixed homogeneous matrix solution
  to the actual ioE image, with no convenient-model restriction. If the
  packet stops earlier, complete one named substantial supplier and state
  the exact remaining matrix inputs. Full WachEx still needs the prism.

Worker G — full original Serre H1 vanishing.
  Target exists_h1Zero_tw_of_veryAmpleBy in
  Proofs/CoherentCohomologyProofs/SerreVanishingH1Twist.lean.
  Keep the original Noetherian R, actual VeryAmpleBy cover and arbitrary
  line bundle. No smoothness assumption may be added to this theorem.
  Use FCD10/13 and ASL12/14/16 to choose one finite homogeneous submodule
  before all degrees. Prove a uniform large-degree exactness bound, then
  the reverse chosen-cover-to-all-cover cocycle argument.
  Acceptance: the literal FirstCohomologyVanishes predicate for all integer
  twists t>=t0, with t0 chosen once. Exactness of one cover alone is weaker.
  Do not recreate Perf: ASL21 already supplies its full arbitrary-base scope.

Worker A — actual local arithmetic charts and flatness.
  Start from the exact ComponentsGoodRankTwo and LocFlat/LocRho consumers.
  Reuse full RTC wpres/co_B/gr_A/cont_u, now proved upstream without FinA.
  Reconstruct the actual loc_cpl identification and the local representation
  chart, preserving the original chosen entries, localization prime, residue
  field, coefficient map and topology. Then prove the original flatness
  conclusion and its representation-chart identification if one bounded
  packet permits both. FCD completion-flatness algebra may be reused only
  after its hypotheses are proved for this actual chart.
  Acceptance: the full original named local producer, not a flat substitute
  with the same dimension. RTC preconnectedness supplies its separate core
  field; dimensions, density, seed incidence and propagation remain explicit.
  An alternative bounded task is one complete dimension/seed-incidence
  producer if its dependency inspection is more favorable.

Worker M — arithmetic stabilizer-volume comparison from original SW inputs.
  Target VolStabFromSWS / VolStabFromSWOf under
  PeriodIntegrals/UnitaryGroupMassFormula/StabilizerVolume/.
  Keep exactly the original SWa1 and StabilizerFirstChernCompatibility
  premises, or their original upstream SiegelWeilUnitaryConvergent supplier.
  GMR supplies the continuous fibers, positive product and compatible Haar
  measures. Identify the theta density with the same IsOmT integral, unfold
  the rational tuple orbit and cancel using one common positive finite
  admissible test. Establish fundamental-domain existence and derive finite
  mass at the correct stage; do not assume the volume equality to prove it.
  Acceptance: full VolStabAt in its all-character/all-Haar/all-fiber and
  fundamental-domain witness order. Then make the literal InVolumesAt join,
  including both word frames and the supplied auxiliary tuple X0, if its
  independent unipotent-volume inputs have been supplied. Otherwise print
  those exact inputs. AOS's infinity scalar and measures remain unchanged.

These tasks are independent at their original supplied data. None needs
another wave to choose a new global setting or a new character.

3. FIRST AVAILABLE SWAPS AND SECOND WAVE

Independent period-ring slot — actual Wach prism.
  Target InertiaEigenvalues/ExistsWachPrismOverIntegers.lean, exists_prism.
  Construct its specialization kernel, Frobenius ideal generator, embedding
  into LetA, all Galois maps, finite-free coordinates, coefficient expansions
  and the original composite scalar-map identity. It is independent of the
  coordinator's invariant-matrix argument. With both in hand, use WIS26/WLD26
  for full WachEx, retaining LocTied/IsStd and the original realization input.
  FaithH/EtBasis, Herr maps and quantitative comparison remain after that.

Geometry slots after Serre H1.
  The separate PolBaseChangeSt producer keeps the actual Cartesian group
  scheme and original L, rigidification, symmetry and KTriv; its main work
  is local-to-global relative ampleness with synchronized powers.
  Principal rank one splits into the Kunneth/Mumford-bundle upper bound and
  the high-twist/torsion-decomposition/growth lower bound. Preserve every
  algebraically closed characteristic. Geometric integrality and the actual
  square generator remain separate. The complex Fourier model alone does
  not supply those all-characteristic original statements.

Arithmetic slots after local charts.
  Complete sharp component/dimension bounds, density and seed incidence
  before invoking ACP's abstract propagation. In parallel, the rank-three
  owner may prepare the exact two-by-two corner and exceptional ideal, but
  must retain the rank-two AllGood supplier it consumes.
  Keep the rank-two and rank-three rings/ideals distinct on one marked
  frame. Rank-three OffFin feeds ACP FinPtOf; RTC FinPtDown returns to the
  original coefficients; AFE then returns FinEnd. Actual automorphic seeds,
  modularity/classicality and Alt WitA/WitAQ remain independent producers.

Independent analytic slots — the two RealBracket cards.
  R1: full CovolRef through CoordCovol, RefNBox and the row-block trace
      determinant transfer. Derive the literal discriminant exponent for
      every original fundamental-domain witness, words and coordinate
      lattice. Do not declare the covolume a normalization.
  R2: broad JacGauge through its actual limiting-integral supplier; then
      PlaceSplit and ProdExact. The four local measure families must have
      products equal to the actual supplied global measures. The source
      distributes a global Haar scalar at one place; unrelated local
      normalizations do not provide the same identity.
  The AOS handoff records exact paths and scopes. RealBracket still needs
  these inputs even though AprimeInf is complete.

Independent counting/transport slots.
  On supplied Forms0, prove the all-family Transport/LevelMatch while
  preserving Witt/genus data, chosen intertwiners, phases and both levels.
  The VolumeStep→PointsLemma→CountTypedOfVolumeStep route may proceed at
  its original supplied spaces independently of Forms0 existence. Keep
  constants before all later tuples and cylinders. Neither route is
  completed by a local nonvanishing or a scalar measure computation.

4. QUEUE THAT MUST REMAIN VISIBLE

Preserve the separate CountV host/support lane, including ell=3, the exact
HostData dictionary and Selmer length, THM_S6_S, HOST_NUMBER_S and the four
installation/transport duties. AUT_UNRAM_COEF alone does not imply them.
The common DesignChoices/Bundle, actual NBuilt and second-layer records
must coexist with their fields, metrics, measures, phases and thresholds.
Retained-defect, period-height, denominator and spectral estimates remain
full quantitative producers on those same families. GLOBAL_LOCAL_GAIN
is already complete and must not acquire stronger new premises.

The seven extra unrestricted Dirichlet-GRH obligations also remain in the
queue: SeedIVAlt, tensor-factor tower, rank-four propagation, its finite
descent, seeded reduction, ProMod join and Case-III automorphy/count join.
Use the whole-contract register for their original quantifier order.

5. INDEPENDENT REVIEW AND INTEGRATION

After all original interfaces are printed, cross-review the mathematics:
arithmetic reviews geometry, analysis reviews arithmetic, coordinator
reviews analysis, and geometry reviews the coordinator's period argument.
A different allocation is allowed if it preserves author/reviewer
independence. Corrections require updated proof hashes and a final review
of those bytes. Do not bind a review to a superseded draft.

Check every new claim against its exact source contract and next use.
Record its proof block, dependencies and retained inputs. A conditional
theorem is complete at its conditional scope; its assumptions are not
therefore proved. Keep no additional whole-closure claim unless the full
original selected contract is supplied and independently reviewed.

Preserve all previous claim objects, source snapshots and historical proof
body. Freeze displaced current metadata in the next version's history.
Explicitly retire obsolete current-frontier flags while retaining their
historical versions. Validate both dependency DAGs and the current complete
open register. Draft TeX checks syntax and references; no PDF or formal
kernel replay is claimed. Bind the archive manifest and delivery record.

6. HUMAN READABILITY

Lead each chapter with the mathematical object being constructed and why
the next theorem needs it. State notation once and use it consistently.
Give the finite denominator, determinant, localization, specialization or
limit argument in ordinary mathematical prose. Explain how it returns to
the original common object. Keep source names and mechanical hashes in
the traceability apparatus. The goal is a complete human proof, and the
roadmap must make the remaining mathematics easier to find, not merely
increase the number of wrapper claims.
'''
inventory = (
    f"CURRENT INVENTORY\n\nThis checkpoint adds {st['new_claims']} reviewed claims, giving "
    f"{st['cumulative_claims']} cumulatively. The selected graph has "
    f"{st['selected_nodes']} nodes and {st['selected_edges']} edges. "
    f"{st['open_count']} whole obligations remain open: "
    f"{st['open_categories']['C']} class C and {st['open_categories']['B']} class B, "
    f"with {st['shared_open']} shared RH/GRH and {st['extra_grh_open']} additional "
    "Dirichlet-GRH obligations. No new whole selected closure is claimed. "
    "These counts are inventories, not completion percentages.\n\n")
plan = plan.replace('1. CAPACITY AND COMMON-OBJECT OWNERSHIP',
                    inventory + '1. CAPACITY AND COMMON-OBJECT OWNERSHIP', 1)
plan += '\n7. COMPLETE CURRENT OPEN-OBLIGATION REGISTER\n\n'
plan += 'These exact identifiers keep every original whole obligation visible in the\n'
plan += 'parallel queue. The detailed contracts and shared-object constraints are in\n'
plan += 'RH_dependency_audit_v0_54.txt and dependency_audit_v0_54.\n\n'
for i, r in enumerate(reg['records'], 1):
    plan += f"{i:02d}. {r['id']} [{r['category']}] — {r['title']}\n"
plan += '\nAll 24 remain open at their whole original contracts. Reuse the completed\n'
plan += 'GLOBAL_LOCAL_GAIN theorem at its unchanged v0.49 scope.\n'
dest = ROOT / 'RH_GRH_parallel_execution_plan_v0_54.txt'
dest.write_text(plan)
print(json.dumps({'roadmap_words': len(road.read_text().split()), 'plan_words': len(plan.split())}))
