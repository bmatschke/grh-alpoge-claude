#!/usr/bin/env python3
"""Record the v0.39 original-input closures and the remaining coupled producers."""
from pathlib import Path
import json
ROOT=Path(__file__).resolve().parent
components=['row_integrability','common_readings','limit_system','proell_descent']
read=lambda p:json.loads(p.read_text())
claims={n:[c['id'] for c in read(ROOT/n/'provenance.json')['claims']] for n in components}
allnew=sum(claims.values(),[])
old_count=len(read(ROOT/'history/version_0_38/provenance.json')['claims'])
def span(n):return claims[n][0]+'–'+claims[n][-1]
new=[
 span('row_integrability')+': uniform smooth growth from the original IsAutFunSm and exact original IsCuspFun imply boundedness of each actual multiplicity-space function. An independently proved mean-zero derivative/contraction argument supplies the exact RowPairInt for all required pairs and finite translates with the original scaled Haar measure and domain. The first DivDef3 is thereby proved from its original premises alone; its extra RowPairInt premise is discharged. The stronger universal quotient-height CuspRapidDecay and second DivRows3 are not asserted.',
 span('common_readings')+': the full original exists_side_reading_level_zero and read_of_moved constructors, and their common ReadPk/pin consequence, are reconstructed on the original given geometric/comparison data. One actual Side0 is chosen before every later reader; every original map, frame, metric, representative and period tie is retained. Full ReadL is supplied with the original eta agreement on every required row/place; the two named endpoints themselves add no hypothesis. Actual common geometry and comparison/test suppliers remain.',
 span('limit_system')+': the entire original S4 is reconstructed: every original pro-ell TWGrp has its actual full Lim record. The same ultrafilter, stabilized finite presentation, finite quotients, local maps and compatibility data are used simultaneously; uniformity in all local elements is proved. This is the limit-group producer, not a construction of the limiting patched modules or the S5 support theorem.',
 span('proell_descent')+': the full original TWQuot and CoreBC-to-Raw pro-ell descent are reconstructed. Full determinant laws, their closed Cayley–Hamilton ideals, Selmer B1/B2, point, Kap and supplied TWAut descend with the same B, J, K, f and modules. Closed-ideal inclusion gives the required one-way NonSS implication. This works at ell=3 without inverting 4!. Coefficient normalization/Unit and the limiting patched support producer remain.',
 f'There are {old_count+len(allnew)} cumulative human proof claims, with {len(allnew)} new claims. No additional whole selected leaf closes: all 33 open compound leaves remain, classified as 22 C, 9 B and 2 D. Their current nested dependencies are substantially smaller. The human RH/Dirichlet-GRH reconstruction remains incomplete.'
]
remaining=[
 'Produce the actual common recursive/geometric member and original comparison/test packets: q/o/Moved/Fits, ChT/LfT/Reps, primitive Holds and eta agreement for full ReadL. The original reader constructors are now reconstructed on these given inputs. Retain the one HostExW, original class, same R/F, frames, maps, metrics, measures, periods and simultaneous family thresholds.',
 'Complete common host/frame and MultEq nonzero-part support, original stored nonzero chain and group tie, eigensystem/carrier/parts and all-embedding logLam, HD/d3b and NEb; construct original RatG/LiftTestB rational tests, base rows and any required second DivRows3 theta square. The exact generic RowPairInt and first DivDef3 implication are now closed on original premises; do not reintroduce the discharged analytic premise.',
 'Construct actual NBuilt/NdSpec and the original local projection square on the common installation, with unchanged spectra, maximal ideals, coefficient embeddings and metrics; supply denominator, retained-defect, period-height, local-gain and normalized spectral estimates on the same family.',
 'Construct the compatible second-layer selector and duties. All common family, Bundle/BWit/BunU, FamGLmin and final assembly consumers retain their exact upstream inputs.',
 'For the selected h=0 Raw route, construct the actual limiting patched rings, maps and modules and prove S5 support on normalized Core data; supply Core-to-CoreBC coefficient normalization and the added Unit parameter. Original S4 and full CoreBC-to-Raw pro-ell descent are now reconstructed and must no longer be listed as current open producers. Keep the same point/Kap/T/TWAut and paired ideal J.',
 'Complete original Cases I/II/V for RH and two-primary targets. CountII still retains ordinary/control/separating arithmetic fibers, type/neatU/TThetaEx, four Hida endpoints and all-level same-J HasAut. Preserve full CohP/LocCFT/N4, both rank-four Links, ell=3, fixed iota and one common coefficient threshold. Unrestricted Dirichlet targets additionally retain CaseIII, SeedIV and original chain propagation/descent.',
 'The optional AQ positive-part route and separate arithmetic envelope remain optional. Historical RF16 remains governed by DEX11.'
]
priority=(
 'Prioritize the remaining normalized Core patching producer: actual limiting rings/maps/modules and S5 support, with Core-to-CoreBC coefficient normalization/Unit as its adjacent branch. '
 'S4 and full TWQuot/CoreBC-to-Raw pro-ell descent are closed in the current human reconstruction and should be reused directly. '
 'In parallel construct the original common geometric/comparison packet and primitive rational tests on one R/F, including exact eta agreement for ReadL; the original reader constructors and exact RowPairInt/first DivDef3 implication are now available. '
 'Ordinary/control, type/neatU, four Hida endpoints and all-level same-J HasAut remain major arithmetic producers. Actual local installation, common estimates and second-layer selection remain shared by both final targets. '
 'Retain every original shared object, metric, measure, quantifier order, fixed iota, prime 3 and common coefficient threshold.'
)
updates={
 'DI1':(claims['row_integrability'],'RPI14 supplies the formerly additional exact RowPairInt under original predicates; RPI15 yields the first original DivDef3 from its original inputs alone.'),
 'DI11':(claims['row_integrability'],'Exact actual multiplicity-pair and finite-translate integrability is supplied by RPI14 with the unchanged mu_b/fd0; no scalar-witness existence is needed.'),
 'DI12':(claims['row_integrability'],'The retained RowPairInt input is now supplied; the original empty/nonempty ipM witness-set argument and exact measure remain unchanged.'),
 'DI20':(claims['row_integrability'],'First DivDef3 now follows from its original geometric, Pins/Holds, chain, five real-group predicates and group-tie premises, without the extra RowPairInt premise.'),
 'DI21':(claims['row_integrability']+claims['common_readings'],'The first division identity has its exact analytic supplier, and the named original reader constructors are reconstructed on their actual given data. Common geometry/comparisons/tests, chain, group tie and second DivRows3 remain upstream.'),
 'CSR15':(claims['row_integrability']+claims['common_readings'],'Exact RowPairInt and the original reader constructors are now supplied in their original scopes. One common geometric/comparison/test member and its exact eta agreement, nonzero chain and group tie are still required.'),
 'BTH12':(claims['row_integrability']+claims['common_readings'],'The analytic extension remains closed. Original side/read constructors and guarded full ReadL are reconstructed; common geometry, comparison packets, rational tests and actual base rows remain.'),
 'JSP11':(claims['limit_system']+claims['proell_descent'],'Entire original S4 and full CoreBC-to-Raw pro-ell descent are now reconstructed. The selected Raw route retains normalized Core limiting patching/S5 and coefficient normalization/Unit, plus ordinary/type/Hida/HasAut on the same J.'),
 'CRW12':(claims['limit_system'],'The originally supplied actual Lim may now be constructed by full S4; no limiting patched module or support conclusion is inferred from this group-level producer.'),
 'CRW21':(claims['limit_system']+claims['proell_descent'],'Reuse full original S4 and full matched pro-ell descent. Remaining selected Raw work is normalized Core limiting patched rings/maps/modules/S5 and Core-to-CoreBC normalization/Unit.'),
 'CFO21':(claims['limit_system']+claims['proell_descent'],'The selected coupled B1/B2 packet descends with one C before m and the same eventual N sets; actual S4 is constructed. These do not construct normalized limiting patching support.'),
 'QX10':(claims['limit_system']+claims['proell_descent'],'Both original Links keep ell=3, fixed iota and common coefficient threshold. Full limit-group/pro-ell producers close, while normalized patching/S5 and ordinary/automorphic existence remain.'),
 'DA1':(allnew,'All selected logical edges and ten final input interfaces are retained. Four nested branches advance; the 33 whole open selected obligations remain.'),
 'GH7':(allnew,'RH retains I/II/V and unrestricted Dirichlet GRH additionally III. Current scope incorporates actual S4/descent and exact original-input first division/read constructors; global completion is not claimed.')
}
old_ids={c['id'] for c in read(ROOT/'history/version_0_38/provenance.json')['claims']}
assert set(updates)<=old_ids,sorted(set(updates)-old_ids)
cfg=dict(artifact_version='0.39',date='2026-11-22',predecessor_version='0.38',predecessor_claim_count=old_count,
 components=components,expected_new_claims=len(allnew),component_claims=claims,
 scope='Partial human reconstruction of RH and Dirichlet GRH, accepting the underlying Alpoge–Claude Lean proof as fully checked and correct. Version 0.39 reconstructs exact original-input row integrability/first division, original given-data reader constructors with the full ReadL guard, entire S4 and full CoreBC-to-Raw pro-ell descent. Actual common producers, normalized limiting patching/S5 and coefficient normalization/Unit, local/spectral and ordinary/automorphic producers remain. No Lean replay is claimed.',
 new_in_this_version=new,remaining_major_inputs=remaining,next_local_priority=priority,
 claim_updates={k:dict(supplied_by=v[0],statement=v[1],scope='Additive scope update; every predecessor field, source array and claim edge remains.') for k,v in updates.items()},
 precision_notes=[
 'A: checked published application; B: independent elementary/moderate argument; C: substantial reconstruction; D: unresolved human source understanding, not an alleged formal error.',
 'RPI uses the source uniform exponent before every derivative word. Its own compact mean-zero/contraction proof requires no full-center finiteness and does not import Miller–Schmid Theorem A.',
 'Exact source NI is identified with the appropriate unitary parabolic radical; every proper rational parabolic cusp and every right derivative is checked. Only the qualitative finite Siegel cover and stated algebraic root/parabolic facts are published inputs.',
 'RPI14 retains every b,t,w,c,v,v-prime,g, the same MY0, mu_b=ofReal(nP^(-1)) nu0 and fd0. RPI15 discharges the extra RowPairInt, while retaining all original first-DivDef3 predicates, readings, Pins/Holds, stored nonzero chain and group tie.',
 'No universal quotient-height CuspRapidDecay or stronger second DivRows3 is claimed. The direct integrability proof closes precisely the missing extra supplier.',
 'RDR chooses one Side0 before every later Read. The two original named constructors and ReadPk/pins add no premises beyond their original source. Full ReadL additionally retains the original eta agreement at every required row/place; arbitrary Over does not imply it.',
 'Read constructors consume actual ChT/LfT/Reps, Fits/Moved, original geometry and tests. They do not construct a common family or add a threshold.',
 'LIM proves forall original T:TWGrp, T.ProL implies Nonempty(Lim T), including every record field and uniform local maps. The same finite quotient system and ultrafilter are used throughout.',
 'PQL proves full original TWQuot and CoreBC implies Raw with the same B,J,K,f, maps and supplied modules. Original coefficient normalization/Unit and limiting patching/S5 remain distinct.',
 'PQL uses the full polynomial determinant law and its closed kernel. Chenevier kernel, Cayley–Hamilton and finite-quotient facts are checked over discrete quotients with no irreducibility, reducedness or n! inversion required; ell=3 is retained.',
 'PQL preserves Selmer B1/B2 quantifier order and exact closed augmented Cayley–Hamilton ideals. NonSS transport is the needed one-way implication from the descended algebra surjecting onto the original algebra, not an asserted equivalence.',
 'All 245 historical compound targets in 107 groups and all 121 selected nodes/edges remain. No new whole selected leaf closes; 33=22C+9B+2D is a scope register, not a completion percentage.',
 'No PDF production or Lean replay. Draft TeX verifies syntax and references; independent mathematical reviews are bound separately to the released proof bytes.'
 ])
(ROOT/'increment_v0_39.json').write_text(json.dumps(cfg,ensure_ascii=False,indent=2)+'\n')
print('Configured',len(allnew),'new claims;',old_count+len(allnew),'cumulative.')
