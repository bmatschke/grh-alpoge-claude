#!/usr/bin/env python3
"""Write the readable current progress report from reviewed scope records."""
from pathlib import Path
import json

ROOT=Path(__file__).resolve().parent
def read(name):return json.loads((ROOT/name).read_text())
cfg=read('increment_v0_50.json');st=read('integration_stats_v0_50.json')
coverage=read('dependency_audit_v0_50/route_coverage.json')
reg=read('dependency_audit_v0_50/remaining_leaf_register.json')

out=['RH AND DIRICHLET GRH — HUMAN RECONSTRUCTION, VERSION 0.50',
 'Frames, Bessel periods and denominator bounds','23 November 2026','',
 '1. THE RESULT OF THIS CONTINUATION','',
 cfg['status'],'',
 'This is a continuation of the attached v0.49 archive and its matching roadmap and parallel plan. '
 'The formal proof is accepted as correct, as requested. The work concerns the ordinary mathematical exposition and the exact connections between its results. '
 'It does not reopen the formal verification question. The new version is a full cumulative checkpoint, with all prior material preserved and a separate edition containing only the current audit and new proofs.','',
 'Seven chapters were written in parallel, then checked by a different author or the coordinating reviewer. '
 'They contain 98 new numbered claims: TDR1–TDR13, NFR1–NFR13, CAF1–CAF11, MFC1–MFC14, BNV1–BNV23, BSP1–BSP10 and DNE1–DNE14. '
 'Together with the 3014 unchanged predecessor claims, the cumulative inventory is 3112. '
 'The independent reviews check the mathematics and original hypotheses; source and text hashes separately identify exactly what was reviewed.','',
 '2. WHERE TO READ','',
 'RH_new_proofs_v0_50.tex contains the new seven chapters and the current whole-obligation audit. '
 'RH_readable_reconstruction_v0_50.tex is the complete cumulative manuscript, including the earlier conditional terminal deduction CMP1–CMP6. '
 'Individual chapters are also available in their component directories. The updated roadmap identifies remaining mathematics; the parallel plan assigns bounded tasks with explicit interfaces. '
 'RH_dependency_audit_v0_50.txt and the JSON registers retain the full selected contracts, shared objects and source evidence.','',
 'Suggested mathematical reading order:','']
for comp in cfg['components']:
    d=read(comp+'/provenance.json');ids=[c['id'] for c in d['claims']]
    out.append('  '+ids[0]+'–'+ids[-1]+': '+comp+'/main.tex')
out+=['','3. WHAT IS NOW PROVED','']
titles=['Arbitrary coefficient algebras and literal test rings',
 'The actual normalized theta frame and its mean',
 'Character seeds with the correct order of choices',
 'Construction of the common linked arithmetic frame',
 'Large-parameter Bessel nonvanishing and the original integral',
 'The analytic final step of weight propagation',
 'The whole denominator export from its original local family']
for i,(title,paragraph) in enumerate(zip(titles,cfg['local_conclusions']),1):
    out += [f'3.{i}. {title}','',paragraph,'']

out+=['4. WHY THE SIMPLIFICATIONS HELP','',
 'Finite descent through actual frame bundles. A framed point consists of finite algebraic data in vector-bundle frames and a theta-section frame. '
 'Once those objects represent the literal source functor, descent to a finitely generated subalgebra becomes a finite-presentation argument. '
 'A second direct local construction makes the same descent explicit. The proof does not smuggle a flatness or Noetherian hypothesis onto the coefficient algebra; '
 'it uses the original section-base-change statement only where its hypotheses hold. This separation is essential for the full reduced-test conclusion.','',
 'A Fourier calculation for the complex section line. The theta transformation law gives a recurrence among Fourier coefficients. '
 'Every coefficient is determined by one initial coefficient, and the classical theta series supplies a nonzero solution. '
 'This proves the required complex-fiber section space is one-dimensional directly. It avoids introducing a stronger general section-twisting premise into the normalized-frame construction. '
 'It does not remove the separate SecBaseChangeSt used to descend arbitrary coefficient-algebra frames.','',
 'Normalization is calculated rather than hidden in a positive scalar. The theta integral over the actual fundamental domain is 1/sqrt(2^g det(Im tau)). '
 'The normalized-period identity gives det(H) det(Im tau)=|det h|^2. Unit-minor frames fix det(H) as the source product over the CM type, and the normConst multiplier contributes the reciprocal factor required for cancellation. '
 'Consequently the final Gaussian mean is exactly 1, for either sign of the chosen square root. This verifies the literal normalization field needed later.','',
 'Elementary auxiliary arithmetic. The character-seed argument needs primes in the residue class 1 for an explicit modulus; a Euclid-cyclotomic construction supplies precisely that. '
 'The auxiliary real quadratic field needs congruence and nonsquare conditions, rather than a new prime in a prescribed progression. '
 'CRT imposes n congruent to -1 modulo 4M and valuation one at a fresh odd prime. This makes n nonsquare while retaining the desired local conditions. '
 'These simplifications are proved only at their actual source scope; the later automorphic representations are still separate.','',
 'A single product majorant for the last Bessel interchange. Let A=rho(y), B=rho(y^-1g), G0=rho(g), with rho the Frobenius norm. '
 'On the unitary group, A and B are at least 1 and G0<=AB. Therefore A^(-beta)B^(-beta)<=G0^(-beta/4)A^(-beta/2). '
 'The first factor is integrable over the compact/unipotent period variables and the second over the full group at the original StepGap thresholds. '
 'This establishes the required absolute Bochner integrability with a shorter estimate, preserving the actual character, measures and both free translates.','',
 'Asymptotic comparisons in the denominator bound. The source conclusion is eventual and uniform in the specified order, so its explicit numerical Large threshold can be replaced by proved uniform scale comparisons. '
 'The rapidly growing scale b=exp(x^epsilon) dominates the smaller exponential and polynomial factors; the remaining band scale has an additional exp(-(x^epsilon)^(1/3)) factor. '
 'The argument still chooses K=2000(|Ca|+1)^3 before the family, and later chooses the threshold only from the allowed fixed parameters and family cutoffs. '
 'It proves the entire original export conclusion, with no claim to the upstream existence of ConclF.','',
 '5. WHAT IS STILL MISSING FROM THE COMPLETE HUMAN PROOF','',
 'The seven new chapters finish complete original subtheorems, but none by itself constructs every input of one of the remaining whole selected obligations. '
 'The number of such obligations therefore remains 24. The most immediate mathematical targets are the following.','']
for i,item in enumerate(cfg['remaining_major_inputs'],1):out += [f'{i}. {item}','']
out+=['The distinction between a complete implication and its input producer is maintained throughout. '
 'For example, DNE proves ConclF implies LinkN in full; it does not assert the common ConclF family exists. '
 'BSP proves FinStatement with the original quotient and period-injectivity premises; it does not manufacture that shifted quotient. '
 'MFC constructs the actual linked marked frame under the original full entry assumptions and completes 21 Ok fields; it does not silently supply the seven other fields or GdEnd. '
 'These statements record the progress without weakening the final theorem that must eventually be reconstructed.','',
 '6. COMPLETE INVENTORY OF THE OPEN SELECTED OBLIGATIONS','',
 'Shared by ordinary RH and Dirichlet GRH (17):','']
byid={r['id']:r for r in reg['records']}
for cid in coverage['shared_open_leaf_ids']:
    r=byid[cid];out.append('  '+cid+' — '+r['category']+' — '+r['title'])
out+=['','Additional unrestricted Dirichlet-GRH inputs (7):','']
for cid in coverage['dirichlet_grh_only_open_leaf_ids']:
    r=byid[cid];out.append('  '+cid+' — '+r['category']+' — '+r['title'])
out+=['','There are no RH-only open leaves in this selected route. '
 'The graph remains 121 nodes and 161 edges, with 17 class-C and 7 class-B open leaves. '
 'Classification and reachability describe this sufficient route, not a minimal theorem dependency set. '
 'GLOBAL_LOCAL_GAIN remains closed from v0.49 and is not included in the open list.','',
 '7. ORIGINAL-DATA AND SCOPE CHECKS','',
 'The main points checked during independent review were the same-object and choice-order issues that can be lost in a streamlined exposition. '
 'The geometry uses the actual moduli point, line-bundle section, tangent eigenbasis and frame maps. '
 'The arithmetic uses the actual fixed field inside the original closure, one marked g1, both prescribed characters and one fixed coefficient embedding. '
 'The Bessel arguments use the actual kernel, character, group, Haar pair, Cayley data and original endomorphism integral. '
 'The denominator proof uses the original weights, table branches, summability and family quantifiers.','',
 'The Bessel review explicitly checked one uniform eventual majorant before all integration variables, almost-everywhere strong measurability, the allowed arbitrary ambient second measure in Schur averaging, '
 'and the relation between independently supplied Cayley matrices. The normalized-frame review checked first-linear Hermitian signs and every determinant/mean factor. '
 'The arithmetic review checked the CountV ell=3 scope, the minimal ramified set and the precise missing Ok fields. '
 'The denominator review checked the prime-three branch, the literal branch conditions and the dyadic cutoff range. '
 'All resulting corrections are incorporated in the reviewed files.','',
 '8. PRESERVATION, SOURCE EVIDENCE AND REPRODUCTION','',
 'Source repository: https://github.com/CocoSgt/riemann-hypothesis-lean',
 'Pinned commit: '+cfg['source_commit'],'',
 f"The aggregate new claim ledger cites {st['new_source_files_checked']} distinct pinned source files and {st['new_unique_source_ranges_checked']} distinct exact ranges. "
 'The individual component manifests also retain supporting source files consulted for contracts and neighboring interfaces. '
 'Each included source snapshot was compared with the pinned Git blob. The 98 new claim blocks have exact source locations, proof hashes, stated input boundaries and independent mathematical reviews. '
 'These checks document the human reconstruction; they are not a new Lean build or kernel replay.','',
 'Every predecessor claim record is unchanged. The historical cumulative proof body is unchanged, and displaced v0.49 root metadata is retained in history/version_0_49. '
 'The two attached v0.49 plans are preserved there as the starting point. The current complete plans are the v0.50 files at the archive root. '
 'The release includes its integration, assembly, draft-TeX validation and packaging scripts, plus a full SHA256SUMS manifest.','',
 'The final release record validation_v0_50.json and the independent integration review record the actual completed checks. '
 'Draft TeX compilation checks syntax and cross-references for the new and cumulative manuscripts. '
 'This release follows the inherited TeX-first workflow: no PDF or visual PDF certification is asserted. '
 'The next continuation should start from this complete v0.50 checkpoint and its current roadmap, retaining the exact original premises.','']
(ROOT/'RH_reconstruction_progress_v0_50.txt').write_text('\n'.join(out))
print(json.dumps({'report':'RH_reconstruction_progress_v0_50.txt','bytes':(ROOT/'RH_reconstruction_progress_v0_50.txt').stat().st_size,'new_claims':st['new_claims']}))
