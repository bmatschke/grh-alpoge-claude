#!/usr/bin/env python3
"""Write the readable progress report and concrete next parallel tasks."""
from pathlib import Path
import json

ROOT=Path(__file__).resolve().parent
cfg=json.loads((ROOT/'increment_v0_57.json').read_text())
counts=cfg['component_claim_counts']; new=sum(counts.values()); total=3645+new
date='24 November 2026'

progress=f'''RH AND UNRESTRICTED DIRICHLET GRH — HUMAN RECONSTRUCTION v0.57
{date}

THE RESULT OF THIS CONTINUATION

{cfg['status']}

This continues the detailed proof-note edition. The new-proof TeX contains the complete new arguments and current obligation register. The cumulative TeX preserves the historical proof body and adds this edition ahead of it. No replacement condensed PDF is introduced.

NEW CHAPTERS

'''
for i,s in enumerate(cfg['local_conclusions'],1):progress+=f'{i}. {s}\n\n'
progress+='''WHY THESE ARE THE NEXT USEFUL STEPS

1. Local coefficients: linear descent and nonlinear conjugacy are different tasks.

Earlier IFD25 shows that appropriate invariant solutions of a Frobenius equation have coefficients in the original coefficient ring. That does not, by itself, choose a basis in which an arbitrary fixed invertible Frobenius matrix has coefficients there. FET fills this construction. A parameter filtration first makes the error small modulo p; its Frobenius contraction constructs a near-identity correction. Then the earlier additive surjectivity supplies one correction at each p-adic precision. Their limits give the actual conjugacy. Applying linear descent afterwards places the Galois action and all lattice morphisms over the same ring. This removes an actual construction from the denominator route.

2. Rank two: the connectedness argument now has its actual local input.

The APD presentation has N=N'+n*d+1. Its regular complete source has dimension N+1. Cutting by the N' relations gives components of dimension at least n*d+2 and a chain whose successive intersections have dimension at least n*d+1. At rank two, the explicit bounds on the triangular and coincident-character loci allow a characteristic-prime curve through every sufficiently large good ideal while avoiding those bad loci. The original P1-prime propagates goodness down from those curves. One actual seed starts propagation, and the previously established connected core carries it across all type-I components. The seed and P1-prime are exactly the original theorem's inputs; the chapter does not manufacture them from topology.

3. Determinant tests: the numerical estimate now reaches the original germs.

The local jet is normalized by its main determinant factorial. Its Newton coefficients have constant coefficient one and eventually positive valuation. The integer matrix of binomial evaluations on any consecutive interval has determinant one. If every value in the prescribed interval had positive valuation, its inverse would force the constant coefficient to have positive valuation, a contradiction. This gives a test order in every original window. The second half is equally necessary: integral row completion and the original Cartier coordinates identify these jets with values on the actual integral germs, up to a determinant factor of valuation zero. The row normal form must still be constructed by its original producer.

4. Sections: a classical replacement now supplies the full growth contract.

On the actual identity-base product, SGV identifies SecM with global sections of the literal power of the pulled line bundle, preserving the coefficient action. Choose one very ample power N. Its positive powers have nonzero sections. Milne's stated index theorem puts their cohomology in degree zero; abelian Riemann–Roch then gives

    dim SecM(N*t) = d*t^g   for every integer t>=1,
    d = dim SecM(N) >= 1.

Thus c=1 and C=d give the original two-sided bounds. The constants are chosen before t and may depend on the original variety, exactly as the source permits. The argument includes all characteristics and g=0. It does not require proving the source's more general filtered-polynomial machinery for this particular endpoint.

5. Periods: the exact Gram identity is separated from the spectral estimate.

PGR proves the original period expansion for every supplied setting satisfying the printed analytic inputs. The absolute-integrability argument occurs before orbit unfolding. The rational-return dictionary, local phases and integral splitting identify the resulting terms with the prescribed operators. The literal normalizing scalar is preserved, including the source's total inverse convention. This supplies the operator identity used by the subsequent estimates; those uniform estimates and the family supplying the analytic data remain their own tasks.

EXPLICIT CLASSICAL INPUTS AND RECENT READING EDITIONS

ACC: Grothendieck connectedness (Stacks 0ECR), complete-local universal catenarity (032C), and the finite-type dimension formula (02JU).
DJW: the ordinary Cayley identity, Caracciolo–Sokal–Sportiello, Theorem 2.1. The adjoint-functor reader, revision 94107d5f1a355a4ae0bd521123dba9ffd62e00f5, suggested the shorter window organization; the coefficient estimates and original-row application are printed here.
SGV: Milne, Abelian Varieties, corrected 2022 Storrs article, Proposition 9.1 and Theorem 13.3(b),(c), with the full original-object dictionary supplied.
FET: Scholze, Perfectoid spaces, Theorem 3.7(i), for finite extensions of the explicitly constructed cyclotomic perfectoid field. The sharp-coordinate recovery needed for faithfulness is proved here.
PGR: Brox's reading edition, revision fd38313e5c7018c3c988ba20510e6b0b3bca0519, suggested the support/return/antilinear-column organization. This chapter proves the original universal analytic contract without adding that edition's installed arithmetic gap.

The reading editions supply useful ideas and organization. Completion is recorded only after the resulting argument has been checked on the pinned original statement.

CURRENT LIMITS AND NEXT PRODUCERS

'''
for i,s in enumerate(cfg['remaining_major_inputs'],1):progress+=f'{i}. {s}\n\n'
progress+=f'''INVENTORY AND VALIDATION

Baseline claims preserved: 3,645.
New claims: {new}.
Cumulative claims: {total}.
Component counts: {json.dumps(counts,ensure_ascii=False)}.
Whole selected graph: 121 nodes, 161 edges.
Whole open obligations: 24 = 17 C + 7 B; separately 17 shared RH/GRH + 7 additional GRH.
New whole closures: none. GLOBAL_LOCAL_GAIN remains closed at the full v0.49 scope.

Every new proof block has an independent mathematical/source-contract review bound to its final bytes. The original proof claims and historical manuscript body are preserved. Source file and range hashes are checked against the pinned original commit. The integration audit checks the exact current boundary, review coverage, acyclicity, preservation, and counts. Draft TeX checks both reading editions for syntax and references. The delivered validation files record the actual outcomes; none of these checks is represented as a new Lean replay.

READING ORDER

Start with this report, then RH_new_proofs_v0_57.tex. Use RH_readable_reconstruction_v0_57.tex for inherited claims. The roadmap names the next actual producer bodies; the parallel plan separates tasks which can proceed independently. The archive contains every component, review, source snapshot, dependency ledger, validation record and continuation script.
'''
(ROOT/'RH_reconstruction_progress_v0_57.txt').write_text(progress)

roadmap=f'''RH / UNRESTRICTED DIRICHLET GRH — NEXT MATHEMATICAL ROADMAP v0.57
{date}

GOAL AND RULE OF CONTINUATION

Produce the full human-readable proof of both RH and unrestricted Dirichlet GRH. Accept the formal source as correct. Continue the detailed proof-note edition and use standard published replacements where they supply the exact original contract. Keep the concrete mathematical construction visible; a source identifier or an assumed compatibility predicate is not a human proof.

Use the current checkpoint and v0.57 dependency register as the frontier authority. Historical remaining-input descriptions are preserved records and can be superseded by later chapters.

FIRST: FINISH THE LOCAL WACH CONSUMER ON ITS ACTUAL INPUTS

Completed: FET FaithH, fixed integral basis, nonlinear Frobenius decompletion, EtBasis and WEt; WPR original conditional WachEx; WIS/IFD period-ring inputs and linear descent.

Read src/Development/AbelianVarietyTheory/Proofs/InertiaEigenvalues/ExistsLocalWachFunctor.lean, especially its actual assembly. The group, series and inclusion records are constructed in NormCoeAlgebraMap.lean (GroupLayer.nonempty_gamS), OneAddXMulDerivativeBinomial.lean (Ser.nonempty_wSer) and TeichPow.lean (IoLayer.main). The current downstream WIS/WPR/FET theorems retain these records as supplied data; reuse the completed generic action, tensor and inclusion arguments while assembling the missing original record constructors. Then reconstruct HerrClassMaps.exists_classMaps in ExistsUniqueFits.lean and Cmp.nonempty_cmpS through ChiGamPowNeOne.lean and its imports. Expand every output field of the original structures.

The quantitative return must retain full inverse-image finite local conditions, including torsion; coefficient-normalized length; both cyclic orders of the signed clusters; and the same comparison maps. After that, build the original ConclF table on one common family, preserving ShaFinOdd, the exceptional sets, summability and eventual thresholds. Do not infer the common family from isolated local estimates or introduce an extra transition-system requirement between outer indices.

SECOND: COMPLETE THE DISTINCT RANK-THREE COMPONENT ROUTE

Completed: full rank-two PropagationTheoremGL2; c1ch, ordinary local chains, loc_dim, fibre, l52 and several incidence suppliers at both ranks. The original automorphic finite-weight, P1-prime and seed producers remain their own inputs.

Read the actual dependencies of PropagationTheoremGL3.lean and AbsMain.lean under src/Development/AutomorphicArithmetic/AutomorphicVarieties/CurveDVRSpecialization. Begin at rank three's EPres parity equations and Sharp record, then its triangular locus, FrobeniusCornerLiftTwoToThree.lean, seedpt, exceptional ideal and thick chains. Preserve the separate rank-two and rank-three determinant maps and ideals. Use ACC's full rank-two return as the exact supplied AllGood input; do not assume it for a different ideal.

The target is full rank-three propagation plus OffFin at the original premises. The automorphic ModIn/ModU and seed producers, patching/modularity/classicality and stronger Alt witnesses remain subsequent arithmetic tasks. Host ell=3 must remain in scope.

THIRD: CONSTRUCT THE ORIGINAL CARTIER NORMAL FORM

Completed: DJW full ThmP, arbitrary-index BiValue, BiContent/BiWindow, all MtoHM fields, actual standard coordinates, integral row completion and full block_of_normal_form. The exact integral row window is proved from MConcl. Do not re-prove the scalar window while this existence step remains.

Read RowDataMainTermNormalFormAndLevelOne.lean and its imports under src/Development/AbelianVarietyTheory/Proofs/UnramifiedDepth. Reconstruct the adapted Cartier-chain construction, residue rank estimates, pairing-kernel estimate and weighted gauge remainder which produce RowData.LemmaM on the original RowData. Preserve its rank deficiency and level-one strengthening. Then apply DJW on the same form, flags, gauges, coefficient valuation and chosen coordinates to install the literal flag versions of BiSupply.

FOURTH: FINISH THE POSITIVE-POWER SECTION-LAW INPUTS

Completed: arbitrary-base Perf, both Serre conclusions, PolBaseChangeSt, actual very-ampleness, section finiteness and SGV full section growth. GSL_FINITE_GROWTH is supplied; do not leave it in the active frontier.

Use the remaining input list at GSL17 and GSL26. Prove multiplication-pullback generated comparison and the actual finite/flat/surjective and etale multiplication geometry; invariant-function descent on every relevant open; the required arbitrary-test integrality and principal rank one; torsion-indexed section decomposition; and square/translation generators. Keep the original covers, tuple coordinates, section actions and both levels. The identity-base geometric-integrality dictionary in SGV is not automatically every other test-space integrality statement.

FIFTH: COMPLETE THE REAL AND FINITE NORMALIZATIONS, THEN THE SPECTRAL ESTIMATE

Completed: RCV full original CovolRef; AOS exact infinity scalar; PGR full original conditional KExpansionC and its literal period/operator consumer; BQS BesselNVGap; conditional SVW and original InVolumes join at their premises.

The next bounded analytic card is full InHHC. PGR already supplies the general folding, L2 and mixed-inner arguments. Identify the original Hilbert convolution operators with their scalar integral representatives on the actual quotient, then prove the final automorphic-range equation. Use InHHCut.lean, InHHLeaf.lean and InHHClosed.lean under HaarTransversals/UnitaryHaarProducts. The exact consumer is KExpTied in FlagStabilizerTensors/ThmSOwn.lean. Its FoldOKC, InHHC, FundExistsC, OOIntAllC, OOFundIndepC, AmpWellDefC and AbsConvC suppliers must be installed on the same setting and words. The full AbsConv contract includes operator-norm and auxiliary-vector-norm summability and positive Gam1; scalar integrated convergence alone is insufficient. The PGR handoff states the exact source scopes and a finite-measure testing argument for the operator dictionary.

In parallel, prove broad JacGauge, PlaceSplit and ProdExact on the same setting and domains, giving RealBracket with unchanged measures. Supply the retained density/compatibility and finite-place mass/index/column/form data. The full family must supply Forms0, the level/genus/intertwiner transport, Bessel uniqueness and simultaneous arithmetic cylinder counts. Prove the normalized GLOBAL_SPECTRAL estimate on the actual operator now identified by PGR. An exact Gram identity does not bound its norm uniformly by itself.

SIXTH: CONSTRUCT THE COMMON GLOBAL OBJECTS AND THE EXTRA GRH ROUTE

Complete F3 coefficient bridges and F4 common-overfield readings, with the entire fields and fixed embeddings. Construct the actual Hecke and arithmetic character data, base rows, frame lengths, nonzero chains and group ties, carrier/parts, all-embedding logLam and the remaining row estimates. Then join denominator, retained defect, period height and spectral estimates on one common family with Fits/eta agreement and simultaneous eventual thresholds.

Keep the seven extra unrestricted-GRH obligations distinct: SEED_IV_ALT, TENSOR_FACTOR_TOWER, CHAIN_RANK_FOUR, CHAIN_DESC4, RANK4_CHAIN_REDUCTION, TASK_CASE3_PROMOD_JOIN and TASK_CASE3_AUT_JOIN. Neither a selected Hida support nor a conditional CaseIII implication supplies the full automorphy/promodularity producer. CMP1–CMP6 remain the completed conditional terminal deduction.

EFFICIENT WAY TO DISCHARGE AN OBLIGATION

1. State the exact original theorem, including every quantifier, coefficient map and shared object.
2. Read its actual producer body and list its immediate inputs.
3. Match each input to the current human ledger; do not repeat a completed producer because an older roadmap still lists it.
4. For the first missing input, either reconstruct its source construction or use a stated classical theorem and prove the exact object dictionary.
5. Prove the consumer join on the original objects, then record the exact smaller remaining boundary.
6. Have a different agent review the complete argument and full scope before changing any closure status.

The point is to reduce the frontier to concrete constructions. A new independently chosen object is useful only if the theorem permits that choice and the necessary maps and simultaneous conditions are proved.
'''
(ROOT/'RH_GRH_reconstruction_roadmap_v0_57.txt').write_text(roadmap)

plan=f'''RH / UNRESTRICTED DIRICHLET GRH — PARALLEL EXECUTION PLAN v0.57
{date}

STATE

{new} new claims; {total} cumulative. Twenty-four whole obligations remain. The current new proofs and their independent reviews are authoritative. Parallel work should begin at the first missing producer named below, keeping the detailed human-readable style.

AVAILABLE CONCURRENCY

Use three mathematical agents plus the coordinating root. Keep file ownership disjoint. Each author must provide a complete mathematical chapter, exact original contracts and source ranges, inherited inputs, retained foundations, and a precise continuation boundary. Another agent must review the final proof text; an author may not certify their own chapter.

INITIAL WAVE

Agent 1 — local period rings and denominator comparison.
Input: FET/WPR/WIS/IFD/WLD and ExistsLocalWachFunctor assembly.
Task: assemble the actual group, series and inclusion records through NormCoeAlgebraMap.lean, OneAddXMulDerivativeBinomial.lean and TeichPow.lean, reusing the completed generic maps; then construct the Herr class maps and actual comparison records. Begin the quantitative lifting bounds only after their maps are installed.
Target: full actual local functor consumer and then original quantitative comparison; retain torsion, normalized length and both signed orders.
Do not repeat FaithH, the integral fixed basis, nonlinear conjugacy, EtBasis or WEt.

Agent 2 — rank-three arithmetic components.
Input: APD/ACC/RTC/ALC/ACP and exact PropagationTheoremGL3 inputs.
Task: EPres and Sharp, remaining triangular bound, rank-two-to-three corner, exceptional/thick chains and seed incidence, in the source dependency order.
Target: full rank-three propagation and OffFin at their original hypotheses.
Keep ModIn/ModU and actual automorphic seeds separate. Do not infer rank-three parity data from ordinary pres.

Agent 3 — original Cartier normal form.
Input: DJW, original RowData and RowDataMainTermNormalFormAndLevelOne.
Task: adapted chains, residue ranks, pairing-kernel and weighted remainder; construct the exact MConcl/MPlusConcl, then join to the already proved actual integral-row window.
Target: full original LemmaM and original flag BiSupply at their retained geometric inputs.
Do not replace actual gauges with arbitrary formal series or rebuild the scalar window.

Root — source-frontier audit, joins and review.
Confirm the three source scopes and their inherited inputs, maintain the common-object map, and review finished chapters. While mathematical agents run, reconstruct the bounded InHHC automorphic-range producer from the PGR handoff, or prepare a geometric multiplication/descent or JacGauge source packet when that is more independent. Do not mutate another author's chapter without communicating the finding.

SECOND WAVE WHEN A SLOT OPENS

Geometric section laws: multiplication geometry, invariant descent, rank one, torsion decomposition, square/translation laws. SGV already supplies full growth.
Period installation: full InHHC and the KExpTied supplier join on the same setting; preserve all three AbsConv clauses. Independently, complete JacGauge, PlaceSplit/ProdExact and RealBracket; retained finite-place and family data; then uniform spectral norm estimates. PGR already supplies the exact original conditional expansion.
Automorphic realization: actual seed/ModIn/ModU producers on the unchanged frames; extra GRH rank-four and CaseIII producers remain distinct.

CROSS-REVIEW

Rotate reviewers after a chapter freezes. Review the mathematics, not just source references: all degenerate cases and primes, ordering of choices, coefficient actions, directions of maps, phases, normalizations, integrability before interchanging sums/integrals, and the exact conclusion of each classical input. Record corrections and bind the final review to whole-file and per-claim hashes. Keep conditional inputs explicitly printed.

INTEGRATION GATES

Preserve all existing claims and the historical manuscript body. Verify the new source bytes against the pinned original commit. Keep the proof graph acyclic and every dependency resolvable. Never close a whole selected obligation from a proper subtheorem. Never reopen GLOBAL_LOCAL_GAIN. Keep all seven extra unrestricted-GRH obligations. Update all current frontier records so completed subtheorems are not reassigned. Validate both TeX reading editions and package the full continuation state with the established eight deliverables.
'''
(ROOT/'RH_GRH_parallel_execution_plan_v0_57.txt').write_text(plan)
register=json.loads((ROOT/'dependency_audit_v0_57/remaining_leaf_register.json').read_text())
coverage=json.loads((ROOT/'dependency_audit_v0_57/route_coverage.json').read_text())
by_id={r['id']:r for r in register['records']}
footer=f'''\nFROZEN SOURCE AND COMPLETE CURRENT REGISTER

Accepted original source commit: {cfg['source_commit']}.
This checkpoint preserves 3645 prior claims and adds {new}, for {total} cumulative claims.
The selected graph has 121 nodes and 161 edges. Its 24 open whole obligations
split into 17 class C and 7 class B; separately, 17 are shared by RH and
Dirichlet GRH and 7 are additional Dirichlet-GRH obligations. These are
different partitions. No whole obligation is newly closed in v0.57.
GLOBAL_LOCAL_GAIN remains closed at its full v0.49 scope.

Shared RH / unrestricted Dirichlet-GRH obligations:
'''
for cid in coverage['shared_open_leaf_ids']:
    footer+=f"  {cid} — class {by_id[cid]['category']}.\n"
footer+='\nAdditional unrestricted Dirichlet-GRH obligations:\n'
for cid in coverage['dirichlet_grh_only_open_leaf_ids']:
    footer+=f"  {cid} — class {by_id[cid]['category']}.\n"
footer+='\nRH_dependency_audit_v0_57.txt states each complete original contract and its current remaining producers.\n'
for name in ['RH_reconstruction_progress_v0_57.txt',
             'RH_GRH_reconstruction_roadmap_v0_57.txt',
             'RH_GRH_parallel_execution_plan_v0_57.txt']:
    p=ROOT/name
    p.write_text(p.read_text()+footer)
print(json.dumps({'progress_bytes':len(progress.encode()),'roadmap_bytes':len(roadmap.encode()),'parallel_plan_bytes':len(plan.encode())}))
