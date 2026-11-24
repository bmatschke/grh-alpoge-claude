#!/usr/bin/env python3
"""Write the v53 roadmap and four-slot parallel plan from the exact current packet."""
from pathlib import Path
import json
ROOT=Path(__file__).resolve().parent
cfg=json.loads((ROOT/'increment_v0_53.json').read_text())
st=json.loads((ROOT/'integration_stats_v0_53.json').read_text())
reg=json.loads((ROOT/'dependency_audit_v0_53/remaining_leaf_register.json').read_text())
parts=['RH AND UNRESTRICTED DIRICHLET GRH — RECONSTRUCTION ROADMAP v0.53',
'23 November 2026','',
'Purpose: continue the full human reconstruction of the accepted Alpoge–Claude formal proof. Keep the old detailed proof-note style. This roadmap is based on RH_reconstruction_v0_53.zip, preserves the accepted efficiency approach, and supersedes the v0.52 task frontier. It is guidance, not an additional proof.','',
'Repository: https://github.com/CocoSgt/riemann-hypothesis-lean',
'Accepted source pin: '+cfg['source_commit'],'',
'1. CURRENT STATE','',cfg['status'],'',
'The full new proof edition is RH_new_proofs_v0_53.tex. The cumulative edition is RH_readable_reconstruction_v0_53.tex. The progress report explains the actual constructions, and RH_dependency_audit_v0_53.txt prints every remaining whole contract. The selected graph remains 121 nodes and 161 edges. No whole closure is inferred from the completion of one conditional subtheorem.','',
'2. WORK BACKWARD FROM THE ACTUAL NEXT CONSUMER','',
'For a proposed task, write the exact output, all antecedents, and the choice order before developing a proof. Read the body of its actual producer and its next use. A short conjunction-projection or record assembly is useful for the map, but the main assignment should be the substantial producer it consumes. Aim to remove a specific nontrivial premise from that next use.','',
'Give one owner the common construction. Parallel workers can prove independent properties on that fixed object or independent exact suppliers. They should not choose separate frames, coefficient fields, lattices, measures or thresholds and assume those choices can later be identified. State and prove any transport actually needed.','',
'The present packet illustrates three legitimate simplifications: the smaller ring k+m_A realizes exactly the diagonal-residual finite points required by FinPtOf; local coarea and explicit good-place counts construct compatible measures without a theta-volume identity; and tensor normal forms prove the actual Wach base-change map without extra period-ring flatness. None silently reduces a consumer’s quantified class.','',
'Do not reopen the completed FCD algebraic model, ACP FinPtOf and abstract propagation, GMR RescaleStep3, or WLD generic constructors. Reuse the earlier GSL/AFE/BQS/SSC endpoints at their printed scopes. The inherited GLOBAL_LOCAL_GAIN closure remains complete.','',
'3. GEOMETRY: ACTUAL SECTION LOCALIZATION AND THE MODEL JOIN','',
(ROOT/'flat_chart_descent_v53/next_source_handoff.txt').read_text(),'',
'Independent geometry after that join','',
'The algebraic model is now supplied. The original global section laws still require the separate polarized base-change producer, geometric H1 vanishing, geometric integrality, principal rank one, the torsion-indexed section decomposition and growth, and the theorem-of-square generators. The detailed preserved GSL handoff is global_section_laws_v52/next_source_handoff.txt. Read its exact F,P,V,R,T input definitions; FCD discharges the algebraic grCube-model portion, not those independent geometric statements.','',
'Useful entries remain AbelianSchemeLawProofs/AbelianSchemeLawsWithoutCohomology.lean (polBaseChange_holds), FinrankSectionsPrincipalPolarisationEqOne and its two inequality suppliers, Serre and multiplication/invariant-descent producers, and the actual square-generator theorem. Once all original inputs are supplied, GSL26 and NFL22 install them on the same supplied Moduli and normalized family. Moduli and retained HUF/PUN foundations still have their own boundaries.','',
'The finite-level IsSystem at Proofs/SiegelThetaTransformation/HermitianThetaLevelDataFormsSystem.lean is an independent later target. Preserve one X,bas,idx,D,M,v0,mu through all nine fields, then the actual Gaussian/reproduction, ramified jets, simultaneous dictionaries, all-tuple class sums and phase-sensitive uniqueness. These do not follow from a model of the section complex alone.','',
'4. ARITHMETIC: SUPPLY THE RANK-SPECIFIC PROPAGATION DATA','',
(ROOT/'arithmetic_component_propagation_v53/next_source_handoff.txt').read_text(),'',
'An upstream-dependency guard: LocFlat uses the generic gr_A and loc_cpl (LocCpl.lean:162–188). The analogous UCE13 entry-algebra theorem assumes FinA and cannot replace that supplier here without a circular FinPt-to-FinEnd-to-FinA dependency. FCD5 supplies reusable completion-flatness algebra, while the actual arithmetic completion/universality and generic graded entry algebra remain to be proved at their upstream scopes.','',
'5. ANALYSIS: EXACT ORBITAL SCALARS, VOLUMES, TRANSPORT AND COUNTING','',
(ROOT/'global_measure_rescaling_v53/next_source_handoff.txt').read_text(),'',
'6. DENOMINATORS: THE THREE PERIOD-RING SUPPLIERS AND THE LATER COMPARISON','',
(ROOT/'wach_lattice_descent_v53/wach_descent_handoff.txt').read_text(),'',
'Use I=src/Development/AbelianVarietyTheory/Proofs/InertiaEigenvalues/ and N=src/Development/AbelianVarietyTheory/Definitions/NonGaloisDescent/. The precise bounded targets are:','',
'A. I/ExistsWachPrismOverIntegers.lean, exists_prism. Construct the original local prism, specialization kernel, Frobenius ideal generator, embedding into LetA, all Galois maps, finite-free power-series coordinates and both finite coefficient decompositions. The identity a composed with z equals the original zlA is part of the output, not a later arbitrary identification. WLD25 is now the full generic consumer.','',
'B. I/WachInclusionInjectiveSaturatedInter.lean, ioE_injective_saturated_inter. The Wach assembly needs injectivity and reflection of units for the actual ioE. Prove those at every original allowed layer/embedding. The stronger intersection clause may also serve later consumers; decide its scope from those consumers instead of assuming it is necessary for WLD26.','',
'C. I/FixedByCyclotomicKernelEtalePhiSolutionMemWach.lean. The original statement also handles an inhomogeneous term. WLD26 needs the homogeneous case: if F and U are invertible matrices over E, V has cyclotomic-kernel-fixed entries in B, and iota(F) phi(V)=V iota(U), then every V entry belongs to iota(E). Prove this at all original ranks and layers; WLD15 then returns every required fixed tuple to the supplied etale module. No convenient-model restriction is allowed.','',
'These three constructions can run independently on the original supplied WGam/WSer/WIo data. WLD1–25 are reusable, and DFD12 already gives the exact coefficient conversion from the original integral Bhatt–Scholze input. WLD26 joins the three outputs into full WachEx for every supplied WEt. Until that join the all-layer theorem remains conditional.','',
'Complete HW/Fon/Cmp requires more than WachEx. The exact chain in I/ExistsLocalWachFunctor.lean retains FaithH, EtBasis, Herr class maps and the quantitative de Rham comparison. N/ExistsOfLayers.lean allows a complete dependent Gamma,R,I,E,Mo,Cl,Cm record to be chosen at each Good(K,s,LL). Its internal functoriality and comparison identities must all hold; it does not ask for a new unspecified inter-layer transition system.','',
'After the comparison, SSC17 and DFD supply the original family setup with the same oriented SignatureChoice, complement family, NChoice and exceptional sets. Then obtain the fifteen Concl fields on one common family: pos, pass, mult, rank, kill, num, mid, bb, large, exc, two, ram, typ, par, small. For fixed Fm choose C,x0 before every later x and index; retain the original ShaFinOdd and summability conditions. RowNum, StarAD, BB and the actual large/exceptional/ramified/type estimates remain mathematical producers. Apply DNE only after ConclF exists, preserving its K=2000(|Ca|+1)^3 before the family.','']
old=(ROOT/'RH_GRH_reconstruction_roadmap_v0_52.txt').read_text()
tail=old[old.index('7. THE SEPARATE COUNTV HOST AND SUPPORT LANE'):old.index('11. COMPLETE OPEN WHOLE-OBLIGATION REGISTER')]
tail=tail.replace('remaining geometric suppliers in section 4','remaining geometric suppliers in section 3')
tail=tail.replace('denominator\nproducer of section 3','denominator\nproducer of section 6')
tail=tail.replace('The full AFE arithmetic entries and completed conditional marked frame help this lane,','The full AFE arithmetic entries, ACP abstract implications and completed conditional marked frame help this lane,')
parts += [tail,'11. COMPLETE CURRENT WHOLE-OBLIGATION REGISTER','']
for i,r in enumerate(reg['records'],1):parts += [f"{i:02d}. {r['id']} [{r['category']}] — {r['title']}"]
parts += ['','All 24 are still open at their whole original contracts. The detailed current register and route coverage are in dependency_audit_v0_53. Claim counts do not estimate the work remaining.','',
'12. ACCEPTANCE AND CONTINUATION','',
'An accepted packet contains the readable theorem and proof, the original target statement and exact next use, all explicitly retained inputs, exact source/proof ranges, a mathematical dependency list, and a review by someone other than its author. A source declaration is evidence for the intended target, not a replacement for the human proof. A full endpoint must keep its original quantifiers and common objects. A sufficient specialization is allowed only with its explicit implication to the actual consumer.','',
'If an assignment reaches an unproved producer, identify its exact mathematical statement and where it enters. Do not hide it in a newly named omnibus hypothesis or report it as discharged by an assembly. Preserve all previous proof bytes, and update the current scope separately. The parallel plan below this version uses the same archive and boundaries.','',
'Continue with the same full RH and unrestricted Dirichlet-GRH goal and the detailed human-readable exposition.','']
road=ROOT/'RH_GRH_reconstruction_roadmap_v0_53.txt';road.write_text('\n'.join(parts))
plan=r'''RH AND UNRESTRICTED DIRICHLET GRH — PARALLEL EXECUTION PLAN v0.53
23 November 2026

This plan is based on RH_reconstruction_v0_53.zip and the current roadmap.
Accepted source pin: 7cbf7a0c32fca1badf05931879a37c3f8a2b03b4.
The goal is the complete human reconstruction, preserving the detailed
proof-note style. This is a work plan, not a mathematical assertion.

1. CAPACITY AND OWNERSHIP

There are four active slots: one coordinator and three workers.
Keep one owner for every common construction. The coordinator handles
one mathematical task and the joins, while workers prove independent
exact suppliers. Reassign a finished worker to an independent review;
do not count the author's self-check as that review.

Choose bounded endpoints from the current roadmap. A completed original
subtheorem and its next use are the unit of progress. The number of
numbered claims is only an inventory. No current task should reconstruct
a wrapper while leaving its substantive antecedent unnamed.

2. DEFAULT NEXT WAVE: FOUR INDEPENDENT PRODUCERS

Coordinator — actual Wach coefficient embedding.
  Read ioE_injective_saturated_inter in
  InertiaEigenvalues/WachInclusionInjectiveSaturatedInter.lean.
  Supply actual injectivity and unit reflection at every original
  permitted layer. Reuse WLD's entire generic assembly and normal-form
  arguments. If proving the stronger intersection clause, name its
  downstream consumer. Keep the original Gamma,R,I throughout.
  Acceptance: the exact two clauses required by WLD26, with a full
  readable period-ring argument, not an abstract assumption called
  saturation. If an earlier ring construction is still required,
  reconstruct or name that precise supplier.

Worker G — actual twisted-section extension and localization.
  Fix the original arbitrary R, smooth projective Y, very ample H with
  sections s_i and line bundle M. Target the two literal section results:
  power-killing a section vanishing on D(sigma), and extending a section
  of D(sigma) after multiplication by a common power.
  Entries: ExistsNhdsPowMulTwCoordEqZero and ExistsTwExtendPowMul under
  Proofs/CoherentCohomologyProofs. Carry the finite cover, denominator
  exponent, overlap discrepancy exponent and transition units.
  Then obtain TwistedSectionsLocaliseToCharts and the actual cube
  comparison through ExistsDehomogenisationTwistedChart and
  ExistsTwistedSectionsCubeBijective.
  Acceptance: the actual semilinear maps and restrictions of the
  section cube, at arbitrary original R. FCD18 already supplies the
  algebraic Noetherian model; do not reopen it.

Worker A — one substantial rank-two geometry supplier.
  Start from the exact ComponentsGoodRankTwo consumer and identify its
  currently missing inputs. A good independent target is the actual
  PreconnectedRankTwo core construction: normalized extension
  representations, their realized points, uniqueness, membership and
  the polynomial lines joining them. Its original point-realization
  requirements must be read carefully; ACP's smaller diagonal-residual
  shortcut is not automatically a replacement for broader IsBar inputs.
  Alternative bounded targets are the actual LocFlat/LocRho chart pair
  or the ChainedBot plus triangular/coincident-locus dimension bounds.
  LocFlat uses generic gr_A/loc_cpl. Do not substitute the analogous
  UCE13 result here: it assumes FinA, which would create an upstream
  FinPt-to-FinEnd-to-FinA circle.
  Acceptance: a full original supplier of the arithmetic local/global
  propagation data. ACP13–17 already prove the general prime,
  propagation and flat-chart implications; do not redo them.

Worker M — exact archimedean orbital scalar on the measured setting.
  Use the actual rescaled X, its one character and unchanged infinity
  measures. Target ConstTest and PushInf at
  PeriodIntegrals/UnitaryGroupMassFormula/ArchimedeanOrbitMeasures/.
  Read the original KVal definition, PushCut and its actual positive
  test integral. Reuse GMR's invariant fiber measure, uniqueness and
  all-section quotient formula. Prove the exact determinant, compact
  volume and Tw-power factors.
  Acceptance: the literal PushInf equality for every original
  self-dual/fiber witness. An unspecified proportionality constant or
  a chosen new infinity measure does not meet the endpoint.
  The subsequent ExInf, WeilInf and HtotInf remain explicit unless
  their actual producer proofs are also completed.

These tasks are independent at their supplied original data and need not
wait for another wave to manufacture a common setting.

3. SECOND WAVE AND AVAILABLE SWAPS

After the actual section-localization proof:
  Affine line-bundle finite projectivity (SecOnFinitePresentationProjective)
  and chart smoothness (CstSmoothAndFlat) can run in parallel, both on
  the already fixed actual chart rings and modules. Join them with
  FCD18 and GSL8–10 to obtain the original smooth-projective Perf
  supplier. Then proceed to the separate polarization/H1/rank/square
  producers; do not announce global section laws before those inputs.

After one rank-two supplier:
  Complete the remaining rank-two geometry, seed incidence and
  dimensional bounds, then apply the already proved abstract
  propagation. In parallel on the same frame, the rank-three owner can
  reconstruct QuotientHomNonvanishingBound's actual two-by-two corner
  and exceptional ideal, and the ChainedOfComap dimension chain.
  Keep S2/M2 and S3/M3 separate. Rank-two AllGood feeds the corner;
  rank-three OffFin feeds ACP11; finPtDown descends the result from
  the extended coefficient frame to the original one before AFE20
  returns FinEnd. Actual
  automorphic seeds, modularity and Alt WitA/WitAQ are separate.

After the Wach embedding supplier:
  The actual Wach prism and the homogeneous fixed-Frobenius matrix
  descent are independent original targets. If the coordinator can
  release another worker, assign one to each.
  WLD26 then gives full WachEx on every supplied WEt.
  FaithH/EtBasis and Herr/quantitative comparison can begin at their
  supplied inputs in parallel; their final join is one complete
  HW/Fon/Cmp triple. Do not add an unspecified transition system
  between the outer layers.

After PushInf, or as an independent analytic swap:
  Reconstruct arithmetic volume comparison from the retained exact
  SiegelWeilUnitaryConvergent premise. Read InVolumesAt and its
  actual producer before unfolding. GMR has supplied compatible
  measures and their positive product, not the arithmetic quotient
  equality. The original all-family Transport/LevelMatch can be a
  separate task on supplied Forms0(u).
  The independent counting branch may start with VolumeStep in
  SameKindIsometric and its VolumeStepOfSiegelWeil producer, then
  PointsLemma and CountTypedOfVolumeStep. It does not need to wait
  for ambient Forms0 existence. Preserve constants before all later
  families and representation choices.

4. COMMON-OBJECT INTERFACES

Geometry:
  one Y,R,H,M,s_i and one graded section module; one R0,C0,theta;
  actual section restriction and every arbitrary coefficient change.

Arithmetic:
  one original frame, C0 and g1; separate rank-two/rank-three rings
  and modularity ideals; one OffFin ideal before every IsCD test;
  one G_L before all later ordinary points. Host ell=3 stays allowed.

Analysis:
  one actual setting X, one hb and one standard psi before all words,
  places and auxiliary tuples; literal global/infinity measures;
  actual S0,S and stabilizers. The original source does not add a
  hidden equality between a finite S-measure and a restricted product
  of local S-measures, so do not invent that additional obligation.

Wach/denominator:
  one supplied Gamma,R,I,E at a layer; one prismatic image and its
  inverse-image lattice; all original maps and Frobenius/Gamma laws;
  one complete dependent record at every allowed outer index.
  Later keep SSC's orientation, actual DFD complement family and
  exception sets, and all ConclF bounds on the same setup.

An isomorphism is usable only when its exact scalar, group, metric,
character, phase and measure compatibility is proved where required.

5. REVIEW ROTATION AND INTEGRATION

Suggested rotation:
  Arithmetic reviews geometry.
  Analytic worker reviews arithmetic.
  Geometry reviews the coordinator's Wach proof.
  Coordinator reviews analysis.

Review both the human proof and the full original endpoint. Inspect
zero-rank and empty-index branches, nonflat coefficient changes,
finite versus arbitrary residue extensions, singular Gram fibers,
all-section formulas, and the order of choices where those occur.
Do not widen a newly proved claim beyond its written hypotheses.

Each author supplies a self-contained main.tex, exact source snapshots
and ranges, proof-block hashes, a dependency list, retained-original-
input records, and an honest next-consumer handoff. The reviewer reads
the actual mathematics and records corrections before binding the final
bytes. A separate integration review checks all predecessor preservation,
sources, graph edges and status claims.

Retain every v0.52 and v0.53 proof unchanged in the next checkpoint.
Current frontier notes may supersede historical statuses without
rewriting the old proofs. Draft TeX verifies syntax and references;
no Lean replay or new compressed PDF is needed.

6. LONGER QUEUE WHICH MUST REMAIN VISIBLE

The denominator's actual common ConclF family; retained-row defect;
period/height comparison; normalized spectral estimates; one nonempty
design family; actual NBuilt specializations; second-layer compatible
selection; base readings, both rational-test levels and actual rows;
CountV host/support catalogue and length transports; the seven extra
Dirichlet-GRH seed/tensor/rank-four/descent/automorphy joins.

These are printed with full scopes in the current roadmap and audit.
Do not remove them because a shared local supplier has been completed.
The goal remains the full proof, with every required common object
and numerical estimate explained in human mathematics.
'''
plan+='\n7. CURRENT INVENTORY AND EXACT WHOLE-OBLIGATION REGISTER\n\n'
plan+=f"{st['new_claims']} new claims; {st['cumulative_claims']} cumulative claims. Selected graph: {st['selected_nodes']} nodes and {st['selected_edges']} edges. {st['open_count']} whole obligations remain ({st['open_categories']['C']} class C and {st['open_categories']['B']} class B): {st['shared_open']} shared RH/GRH and {st['extra_grh_open']} additional Dirichlet-GRH inputs. No RH-only open leaves. These counts are inventories, not completion percentages.\n\n"
for i,r in enumerate(reg['records'],1):plan+=f"{i:02d}. {r['id']} [{r['category']}] — {r['title']}\n"
plan+='\nGLOBAL_LOCAL_GAIN remains fully closed at its original v0.49 scope.\n'
dest=ROOT/'RH_GRH_parallel_execution_plan_v0_53.txt';dest.write_text(plan)
print(json.dumps({'roadmap_words':len(road.read_text().split()),'parallel_plan_words':len(plan.split())}))

