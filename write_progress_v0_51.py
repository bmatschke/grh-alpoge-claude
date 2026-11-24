#!/usr/bin/env python3
"""Write current progress from the independently reviewed scope ledger."""
from pathlib import Path
import json
ROOT=Path(__file__).resolve().parent
def read(name): return json.loads((ROOT/name).read_text())
cfg=read('increment_v0_51.json'); st=read('integration_stats_v0_51.json')
coverage=read('dependency_audit_v0_51/route_coverage.json')
reg=read('dependency_audit_v0_51/remaining_leaf_register.json')
out=['RH AND UNRESTRICTED DIRICHLET GRH — HUMAN RECONSTRUCTION v0.51',cfg['title'],'23 November 2026','',
 '1. RESULT OF THIS CONTINUATION','',cfg['status'],'',
 'This continues v0.50. The formal proof is accepted as correct; the task is to write its ordinary mathematical proofs and preserve their exact connections. '
 'All 3112 predecessor claim records and the historical cumulative proof body are preserved. '
 'The five new chapters contain NFL1–NFL22, LFC1–LFC23, BST1–BST11, BSE1–BSE9 and DFD1–DFD15: 80 claims. '
 'Every claim has an independent mathematical review by someone other than its author, bound to its exact proof text and source scope. '
 'The inventory is now 3192 claims. These complete subtheorems inside the remaining whole obligations, so the whole open frontier remains 24.','',
 '2. READING ORDER','',
 'RH_new_proofs_v0_51.tex contains the current audit and all five new chapters. RH_readable_reconstruction_v0_51.tex contains the full cumulative manuscript, including the conditional terminal deduction CMP1–CMP6. '
 'The roadmap describes remaining mathematics; the parallel plan gives bounded assignments and review interfaces. Individual chapters in the archive are:','']
for comp in cfg['components']:
 p=read(comp+'/provenance.json'); ids=[c['id'] for c in p['claims']]
 out += ['  '+ids[0]+'–'+ids[-1]+': '+comp+'/main.tex']
out += ['','3. THE NEW MATHEMATICS','']
titles=['Full normalized-frame laws and conditional uniformization','All conditions on the common marked arithmetic frame',
 'Derivative decay, tensor maps and noncommutative minors','The two exact Bessel period evaluations','Continuous complementary representations and canonical family data']
for i,(title,t) in enumerate(zip(titles,cfg['local_conclusions']),1):out += [f'3.{i}. {title}','',t,'']
out += ['4. WHY THE SIMPLIFICATIONS HELP','',
 'Holomorphy without a continuous square root. The normalized theta scalar satisfies kappa_b^2=C det(h_b), with a separate choice at every frame. '
 'Every allowed section weight n is even: writing n=2m, its reading is (C det(h_b))^m times the reading with theta scalar one. '
 'The latter is holomorphic by the actual algebraic frame chart and the universal evaluation identity. '
 'Thus no continuous square-root choice is needed. For an arbitrary coefficient ring, locally only finitely many coefficients and nonvanishing denominators occur; their evaluated inverses are holomorphic after shrinking the neighborhood. '
 'This avoids analytifying an arbitrary Spec(R). NFL15 also retains the full arbitrary normed-space and within-set differentiability scope of the natural-rule theorem. See NFL13–NFL17.','',
 'The untwisted cohomology bound from CM units. LFC11–LFC12 use the appropriate Kummer eigenspace over F(mu_ell). '
 'The valuation contribution is separated integrally before reduction modulo ell. The CM-unit anti-invariants contribute only the root-of-unity term, and the class-group term uses the existing C0 through prime-to-ell restriction. '
 'This proves the required h1 bound without adding a Leopoldt premise. The subsequent Euler estimate keeps the actual local subspaces, continuous primitives and inflation defect before applying the exact retained P input. '
 'All 28 conditions are assembled on the same frame, with the same C0 and Big, in LFC21–LFC23.','',
 'Derivatives preserve the decay exponent. A compact conjugation-averaged smooth kernel acts by a nonzero scalar on the unique finite lowest compact type. '
 'Normalization makes it reproduce that type exactly. Right derivatives in the coefficient formula then move onto the compactly supported kernel, whose derivatives remain bounded on a fixed compact set. '
 'The original decay exponent survives every derivative word. This gives both literal tensor maps and their smooth L2 outputs. See BST1–BST5.','',
 'Ordered minors compute the actual periods. The Capelli entries do not commute. BST6–BST8 prove alternation using exterior variables and prove row-column equality by summing the commutator difference: each replacement minor occurs equally often with opposite signs. '
 'The resulting expansions keep the operator order. Ordinary determinant identities are used only for scalar change-of-frame matrices. '
 'For Q=g0^(-1) g P^(-1), d=2r+k, and j*=0 when r>0 or d when r=0, the witnesses are y=Q^(-1)e_j* and alpha=e_d^t Q. '
 'For r>0 the two periods equal kappa product_j(u_j-lambda_s-1/2) times the old period and kappa product_j(u_j-lambda_s+1/2) times the old period, where kappa=-T_z product_a |c_a|^2 / 4^r. '
 'For r=0 the corresponding prefactors are -sqrt(T_z) and +sqrt(T_z). '
 'All are nonzero under the original exclusions, with the original Haar pair, character and free translates unchanged. See BSE3–BSE8.','',
 'Build the integral complement after the rational splitting. DFD1–DFD7 first separate the prescribed character summands over the fraction field. '
 'For the complementary rational subspace W they take Lambda=W intersect O^N. This intersection is saturated, so over the original DVR both it and its quotient lattice are free. '
 'An integral basis b and retraction q give rho(g)=q R(g)b, providing integral continuous matrices. '
 'The construction does not assume an integral character splitting or continuity of a complex coefficient embedding. '
 'The exact Frobenius trace and Speh parity identities identify the desired complement; off the original parameter locus the prescribed trivial representation supplies the remaining family values.','',
 '5. THE REMAINING MATHEMATICS','',
 'A complete theorem with its stated premises is distinguished from the producer of those premises. The immediate targets are:','']
for i,t in enumerate(cfg['remaining_major_inputs'],1):out += [f'{i}. {t}','']
out += [
 'The quotient target is broader than the evaluated complementary-minor vectors. QuotP and QuotM allow any tuple in the specified Euler eigenspace whose actual period is nonzero somewhere. '
 'They require equality with the actual smooth L2 image, actual compact-group stability and injectivity of the prescribed period. '
 'The detailed source guide in bessel_period_evaluation_v51/quotient_next_handoff.txt separates Euler polynomial identities, the trace-kernel transfer and minimal-type extraction.','',
 'DFD9 is the complete canonical-data existence theorem at its named inputs. DFD15 is a conditional family setup theorem. '
 'Its coherent HW/Fon/Cmp and Selmer SignatureChoice suppliers remain. The latter must use the same oriented character as TwGood, with exact budget 1/ell^2. '
 'The crystalline-lattice coefficient theorem DFD12 does not supply the all-layer Wach comparison. Local row/table bounds must still establish ConclF before the completed DNE export can be used.','',
 '6. COMPLETE OPEN SELECTED REGISTER','', 'Shared by RH and unrestricted Dirichlet GRH (17):','']
byid={r['id']:r for r in reg['records']}
for cid in coverage['shared_open_leaf_ids']:
 r=byid[cid];out += ['  '+cid+' — '+r['category']+' — '+r['title']]
out += ['','Additional unrestricted Dirichlet-GRH inputs (7):','']
for cid in coverage['dirichlet_grh_only_open_leaf_ids']:
 r=byid[cid];out += ['  '+cid+' — '+r['category']+' — '+r['title']]
out += ['','There are no RH-only open leaves. The graph remains 121 nodes and 161 edges, with 17 class-C and 7 class-B open leaves. '
 'GLOBAL_LOCAL_GAIN remains fully closed from v0.49 and is excluded from this list. '
 'The full original contracts, common objects, current subresults and sources are in RH_dependency_audit_v0_51.txt.','',
 '7. INDEPENDENT REVIEW','',
 'Geometry review checked the theta determinant square and parity, arbitrary-ring charts, arbitrary within-set differentiability, and every covering/fiber quantifier. '
 'Arithmetic review checked the any-prime class-character statement using the narrow class group at ell=2, the full target topology in strict generation, local cochain corrections and unchanged C0. '
 'Analytic review checked compact-kernel smoothing, ordered-minor signs, both half-unit shifts, rank-zero cases and the unrestricted source period convention. '
 'Denominator review corrected the budget to 1/ell^2 and made the shared oriented character explicit. Both corrections are present in the frozen reviewed proof.','',
 'Every conditional boundary remains visible: NFL22 retains the exact section laws and supplied Moduli; LFC22 retains full Gen/P; LFC23 uses the original coefficient DVR for the seed join; '
 'BSE9 retains both quotient statements; DFD15 retains the coherent comparison suppliers. '
 'No source theorem name or existence of unrelated data was used to erase those premises.','',
 '8. SOURCE EVIDENCE AND PRESERVATION','',
 'Repository: https://github.com/CocoSgt/riemann-hypothesis-lean',
 'Source commit: '+cfg['source_commit'],'',
 f"The aggregate new claim ledger checks {st['new_source_files_checked']} distinct pinned source files and {st['new_unique_source_ranges_checked']} exact ranges. "
 'Every included source snapshot equals its pinned Git blob. Every new claim has an exact proof location, source ranges, dependencies and an independent review. '
 'The source specifies the intended contract; the ordinary proof is written in the chapter.','',
 'All 3112 predecessor claim records and the historical cumulative proof body are unchanged. Displaced v0.50 root metadata and predecessor plans are frozen in history/version_0_50. '
 'Current boundaries are governed by dependency_audit_v0_51 and the current plans; older frontier notes remain historical records.','',
 'Configuration, integration, assembly, review-finalization, draft-TeX validation and packaging scripts are included. '
 'validation_v0_51.json records the release checks and the separate independent integration audit. '
 'Draft TeX compilation checks syntax, references and new overflow diagnostics. No PDF, visual PDF certification or Lean replay is claimed. '
 'The archive-wide SHA256SUMS and external delivery record identify the complete checkpoint. '
 'Continue from this v0.51 archive, roadmap and parallel plan, preserving every original field, embedding, character, measure and order of choices.','']
dest=ROOT/'RH_reconstruction_progress_v0_51.txt';dest.write_text('\n'.join(out))
print(json.dumps({'report':dest.name,'words':len(dest.read_text().split()),'bytes':dest.stat().st_size}))
