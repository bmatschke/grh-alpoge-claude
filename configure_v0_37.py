#!/usr/bin/env python3
"""Define v0.37 exact producer closures and their retained original inputs."""
from pathlib import Path
import json
ROOT=Path(__file__).resolve().parent
components=['adelic_sobolev','smooth_representatives','count_first_order','common_selected']
claims={n:[c['id'] for c in json.loads((ROOT/n/'provenance.json').read_text())['claims']] for n in components}
allnew=sum(claims.values(),[]);analytic=claims['adelic_sobolev']+claims['smooth_representatives']
def span(n):return claims[n][0]+'–'+claims[n][-1]
new=[
 span('adelic_sobolev')+': complete original adelic chart and cube/Haar comparison, local Sobolev inequality, finite-tensor denominator and polynomial rational-point count, and fixed-level pointwise_growth. One exponent and one finite derivative list precede x,F,psi,u; the actual normInf and quotient measure are retained.',
 span('smooth_representatives')+': complete original smooth representatives with every pointwise/global-AE derivative identity on the same finite level; full bounded-holomorphic multiplicity map with all five IsMultMap fields; exact lowest-type restriction and generic linear theta assembly. On the same R, the analytic theta consumer now retains only the original target FinPair and initial extremal-function boundedness, besides its already explicit datum and seed cusp inputs.',
 span('count_first_order')+': the full selected dualN estimate and original ArSys/Counts yield literal B1 with D=4[L+:Q]+4q on the SAME CCH-selected h=0,a=n=4,g=0 Kap already satisfying B2. The constant precedes m, the eventual threshold in N is uniform in the entire admissible rep-prime class, and all original CohP/local-arithmetic guards remain.',
 span('common_selected')+': the complete original cols_of_witnesses, one ReadC before later TwArgs, exact period/evaluation placement and same-R realization/Bundle assembly consumers. Actual reFace/readings, geometry, eigensystem/multiplicity, PartsRow/NEb and division-compatibility suppliers remain explicit; no unrelated compatible witness is substituted.',
 f'There are {1770+len(allnew)} cumulative human claims, with {len(allnew)} added in this version. The selected graph retains 34 open coupled leaves: 23 C, 9 B and 2 D. Several whole nested source producers are completed, but no additional whole selected leaf is closed. The human RH/Dirichlet-GRH reconstruction remains incomplete.'
]
remaining=[
 'Produce the original common recursive/geometric member and compatible selected realization. The finite columns, common ReadC and same-R Bundle/BWit assembly consumers are reconstructed; original reFace and Read/ReadL, geometric half, spectral/eigensystem multiplicities, NEb/PartsRow, division compatibility, rational tests and base rows still require their exact producers.',
 'Supply the initial boundedness of the original extremal theta function and the actual target FinPair. After these inputs the original smooth-representative/Sobolev and bounded-holomorphic IsMultMap producers, lowest-type restriction and all-parameter linear theta consumer are complete. Earlier seed boundedness cannot be inferred from the later Hilbert realization.',
 'Produce actual NBuilt/NdSpec and the original local projection square on the common installation, with unchanged spectra, maximal ideals, coefficient embeddings and metrics.',
 'Supply the original denominator, retained-defect, period-height, local-gain and spectral estimates on the same family.',
 'Construct the compatible second-layer selector and duties. The eleven-field FamGLmin and same-family ChainTied/Closed consumers remain complete; their compatible upstream family is still required.',
 'For RH and two-primary targets finish original Cases I/II/V. CountII now has the same selected h=0 Choice/B1/B2 package, in addition to universal NiceI Norm, ArPl and supplied-type IsRes. It retains ordinary/control/arithmetic fibers, type/neatU/TThetaEx, four Hida endpoints, all-level same-J HasAut, h=0 Raw, CohP/LocCFT/N4 and original side guards. Both rank-four Links retain ell=3, fixed iota and one common coefficient threshold.',
 'Unrestricted Dirichlet targets additionally retain CaseIII, SeedIV and original chain propagation/descent. The two-primary route supplies no universal CountIII.',
 'The optional AQ positive-part route and separate arithmetic envelope remain optional. Historical RF16 remains governed by DEX11.'
]
priority=(
 'Prioritize the exact initial seed-bound and target-FinPair suppliers: they now dominate the remaining analytic theta route, because the complete downstream representative/Sobolev/MMap chain is reconstructed. '
 'Read the published CuspRapidDecay contract together with BoundedOfSmoothCuspidalUniformModerate and the original quotient-volume/fundamental-domain suppliers; check the precise cusp, center, normalization and uniform-derivative hypotheses before treating any result as a published application. '
 'In parallel advance the original common realization through its remaining original readings and first DivDef3 at the exact updated packet, retaining the actual geometry, eigensystems, PartsRow and NEb. The same-R Bundle/BWit assembly is a completed consumer, so do not reconstruct it again. '
 'On CountII, pursue the exact h=0 Raw propagation on the same point/J/Kap and TWAut, while ordinary/control, type/neatU and all-level same-J HasAut remain the principal arithmetic production tasks. '
 'Use the selected Choice/B1/B2 conclusions together on the same full-block g=0 witness; do not reopen the universal arbitrary-Kap B1 or B2 branches for this route. '
 'Keep all selected graph edges, common fields, thresholds, metrics and finite levels unchanged.'
)
updates={
 'CTC13':(analytic,'Actual smooth representatives, every derivative, fixed-level growth/evaluation and the full original bounded-holomorphic MMap are now reconstructed after target FinPair and the initial seed bound. Separate seed ZCusp remains explicit.'),
 'TAE13':(analytic,'The all-parameter original lowest-type integral extends by SPR23–25 once the original target FinPair and initial extremal bound are supplied. No smooth-representative, Sobolev or MMap-field producer remains after those inputs.'),
 'HCU18':(analytic,'The same Hilbert map now has one pointwise smooth multilinear realization with every IsMultMap field, on the unchanged finite pair and finite level. Original initial boundedness and target volume remain upstream.'),
 'RQC22':(analytic,'The retained smooth-representative and Sobolev residue is fully closed by ASB and SPR. Initial target FinPair and seed boundedness remain explicit, with no circular use of post-Hilbert central finiteness.'),
 'BTH12':(allnew,'The theta analytic consumer is complete after the two initial analytic gates. CSR reconstructs the finite original columns/common reading and same-R realization/Bundle assembly consumers; original geometric readings, rational tests and actual base rows remain.'),
 'JSP11':(claims['count_first_order'],'Literal selected B1 is supplied on the same CCH full-block g=0 Kap already satisfying Choice/B2. The exponent is 4[L+:Q]+4q with one C before m and eventual N; ordinary/type, Hida, same-J HasAut and Raw remain.'),
 'CIP12':(claims['count_first_order'],'The exact selected first-order bound now joins the coupled h=0 Choice/B2, retaining full dualN uniformity, ArSys/Counts and CohP/local guards; no ordinary or automorphic module existence is inferred.'),
 'QX10':(claims['count_first_order'],'Both original rank-four Links may use the same selected Choice/B1/B2 route, with ell=3, fixed iota and common coefficient threshold. Raw and original ordinary/automorphic support remain.'),
 'DA1':(allnew,'The ten-input final interface is unchanged. Exact analytic, selected first-order and common-record consumers are now closed on their stated inputs; 34 whole selected leaves remain open.'),
 'GH7':(allnew,'RH retains Cases I/II/V; unrestricted Dirichlet GRH also retains III. Shared analytic and first-order producers are narrowed, but the complete human proof is still unfinished.')
}
cfg=dict(artifact_version='0.37',date='2026-11-22',predecessor_version='0.36',components=components,
 expected_new_claims=len(allnew),component_claims=claims,
 scope='Partial human reconstruction of RH and Dirichlet GRH, accepting the underlying Alpoge–Claude Lean proof as fully checked and correct. Version 0.37 completes original smooth-representative/Sobolev/MMap producers, exact selected CountII B1, and common selected-record/Bundle assembly consumers. Initial target boundedness/volume, actual common construction, local/spectral and ordinary/automorphic producers remain. No Lean replay is claimed.',
 new_in_this_version=new,remaining_major_inputs=remaining,next_local_priority=priority,
 claim_updates={k:dict(supplied_by=v[0],statement=v[1],scope='Additive update; every predecessor field, source and edge retained.') for k,v in updates.items()},
 precision_notes=[
 'A is a checked published application; B independent elementary/moderate reconstruction; C substantial reconstruction; D unresolved human source understanding, not an alleged formal error.',
 'ASB3/4 precede SPR13; SPR13 alone enters ASB14; later SPR14–25 consume ASB14. The joint claim graph is acyclic.',
 'The same original FinPair, literal nuQ and global Haar-AE Repr convention are preserved; no target volume is manufactured by normalization.',
 'The single representative has every original ordered derivative word; the same open level is retained throughout.',
 'One exponent and finite word list precede x,F,psi,u; every model derivative retains that exponent. No unjustified cross-level uniformity is asserted.',
 'SPR21 is the full BackForm.exists_multMap on bounded HolForm, original FinPair and separate ZCusp. SPR25 is conditional on the two remaining upstream analytic gates.',
 'CFO closes B1 only on the SAME CCH-selected full-block g=0 Kap. No universal arbitrary-Kap FirstOrderDualArithmeticBound or obstruction theorem is claimed.',
 'The selected B1 count retains one C before m and eventual N, uniform in every original admissible rep-prime satisfying its finiteness premise. g=0 does not imply Sel1=0.',
 'The only new published import is the finite decomposition/inertia theorem from Milne, with its finite-field/completion/Galois hypotheses checked; the infinite quotient passage is proved independently.',
 'CSR preserves one ReadC before TwArgs and transports the actual later period object; an initial zero period creates no nonzero period witness.',
 'The selected evaluation normalization is exactly kappa=(c*nP)^(-1/2) and nP||sEE(v)||^2=||v||^2 on the original guarded level subspace.',
 'Original geometric readings, multiplicity/eigensystem and PartsRow/NEb/division-compatible inputs remain producers; record assembly does not supply them.',
 'All 245 historical compound targets/107 groups and all selected graph edges remain. The 34 open leaves are not a completion percentage or an absolute minimality theorem.',
 'No PDF production or Lean replay. Draft TeX checks syntax and references only.'
 ])
(ROOT/'increment_v0_37.json').write_text(json.dumps(cfg,ensure_ascii=False,indent=2)+'\n')
print('Configured',len(allnew),'new claims,',1770+len(allnew),'cumulative.')
