#!/usr/bin/env python3
"""Current v0.45 scope, with the full selected closure gated by its review."""
from pathlib import Path
import hashlib
import json
ROOT=Path(__file__).resolve().parent
old=json.loads((ROOT/'increment_v0_44.json').read_text())
review=json.loads((ROOT/'hida_installation_v45/review_HIA1_HIA6_root.json').read_text())
assert review['result']=='PASS'
assert review['proof_sha256']==hashlib.sha256((ROOT/review['proof_file']).read_bytes()).hexdigest()
assert review['selected_whole_contract_reviewed']['full_original_contract_closed_in_stated_scope']
nodes={n['id']:n for n in json.loads((ROOT/'dependency_audit_v0_44/obligation_map.json').read_text())['nodes']}
contract=nodes['COUNT_II_SUPPORT']['contract']
assert review['selected_whole_contract_reviewed']['baseline_contract_sha256']==hashlib.sha256(contract.encode()).hexdigest()
a=contract.index('The remaining arithmetic producers are the four exact Hida endpoints')
b=contract.index('The selected Raw patching',a)
contract=contract[:a]+(
 'HPT18, HED16, HAW19 and HTS8 now prove the four exact remaining Hida fields on this same ideal. '
 'HLM26 constructs one original LevelAlt family, including its universal determinants and vector separation, with one base before all auxiliary levels. '
 'HTW24 constructs its full same-J HasAut with both trace relations, exact fEl and coefficient map, and the uniform exponent n!. '
 'HIA assembles all six fields and HasAut on the original empty-level IsJ; it applies the previously completed selected patching/P1 consumer at rank four and installs both actual QX Links above one common coefficient threshold. '
 'This completes the entire selected two-Link Hida/P1core contract. Full all-rank HidaUAlt is also assembled; arbitrary-chain P3core and full ModUAlt remain conditional on their original PfromAut supplier. '
 'The explicit published base-change, polarized attachment, local representation, DescWeak, cohomological and period foundations retain their original scope. '
)+contract[b:]
contract=contract.replace(
 'No arbitrary-Kap B1/B2 theorem, Sel1=0 assertion, arbitrary-chain Core or complete same-J arithmetic support producer is claimed.',
 'No arbitrary-Kap B1/B2 theorem, Sel1=0 assertion, arbitrary-chain Core or full P3core producer is claimed; the exact selected same-J arithmetic support producer is completed.')
components=['hida_decomposition_v45','hida_automorphy_away_v45','hida_point_return_v45',
 'hida_twisting_v45','hida_level_modules_v45','hida_taylor_wiles_v45','hida_installation_v45']
closed={'COUNT_II_SUPPORT':{
 'category':'B','claims':['HIA1','HIA2','HIA3','HIA4','HIA5','HIA6'],
 'conclusion':'Both original rank-four QX Links carry the full six-field HidaPropsAlt and selected P1core on one J for each permitted later universal datum, above one common prior coefficient threshold, with fixed iota and prime 3 retained.',
 'method':'Actual empty-level IsJ, all six completed Hida fields, one all-level LevelAlt/TWAut/HasAut base, the previously completed selected rank-four Raw/normalization/pro-ell/P1 consumer, and the original two-Link threshold installation.',
 'boundary':'Original named foundations remain explicit. This closes the selected rank-four contract and does not assert arbitrary-chain P3core or full ModUAlt.'}}
cfg={
 'artifact_version':'0.45','date':'2026-11-23','source_commit':old['source_commit'],
 'title':'The six Hida fields and both rank-four support installations',
 'components':components,'closed_selected_leaves':closed,
 'closed_nested_producers':[
  'Full hecke_ideal_end, frobTwT, endShapeT and ArithmeticPointDecomposition on the original IsJ ideal',
  'Full CoreOrdAlt, EndOrdAlt, OrdFlagJ, ConjUnl, ExpTor, BornJ and IrrArithPointsAutomorphicAway with the original conditional continuity and one global window',
  'Full all-positive-rank UpUW return and the literal PointTheoremBaseObject with its rank 2 through 4 antecedent',
  'Full all-positive-rank TwistOk on the same ideal, with the actual determinant twist and all original local guards',
  'Full coreDet and universal maps at every auxiliary level, actual smooth module union, vector-level classical separation and literal one-base LevelAlt',
  'Full local operator, OpMod/OpRel, completed TWRing/TWMaps, HasAutOfAlt and actual same-J HasAut, with exact fEl and uniform n!',
  'Full original HidaUAlt and selected rank-four same-J Hida/P1core installed on both QX Links above one common coefficient threshold'
 ],
 'status':(
  'Partial human reconstruction of RH and unrestricted Dirichlet GRH, accepting the pinned Alpoge-Claude formal source as fully checked and correct. '
  'Version 0.45 completes all six original Hida fields, the actual all-level same-ideal LevelAlt/TWAut/HasAut producer, and the entire selected rank-four Hida/P1core support contract on both original Links. '
  'The selected whole-obligation register decreases from 31 to 30 (21 C and 9 B). Full arbitrary-chain P3core/ModUAlt is not claimed. '
  'Original named local, automorphic, descent, cohomological and period foundations retain their recorded scopes. '
  'The common geometric/arithmetic families and remaining global quantitative and case producers still require reconstruction. No Lean build or kernel replay is claimed.'),
 'local_conclusions':[
  'HED1-HED16 prove the literal arithmetic-point decomposition/end1 on the given representation. Surjective quotient factorization keeps the original point and weight; full polynomial-law naturality keeps all scalar algebras. One HalfG seed is chosen for every original cusp and every positive Speh length, and the exact inverse cyclotomic strings are retained. Degree-one Chebotarev turns their Frobenius product into a global characteristic-polynomial identity. When all lengths equal one, the already matched generic-unitary classification gives the strict interval q^(-1/2)<|alpha|<q^(1/2), yielding the original cofinite strict ratio |z|<q|zprime| at all required places and for every supplied Frobenius multiset.',
  'HAW1-HAW19 prove the full original automorphy-away/end2 endpoint. They compare the arbitrary supplied representation with the actual automorphic part, extract ordinary principal-series data at every arithmetic point without a Good guard, and prove the ordered flag and conjugate-place transport. A single global unitarizing norm twist gives one real window center before all eligible places. The exact ordinary-character calculation shows that any positive-power cyclotomic ratio forces a forbidden factor q between the two complex character norms. This proves the full AutOffN predicate with conditional continuity precisely where the source places it.',
  'HPT1-HPT18 prove the all-positive-rank ordinary return UpUW and the entire PointTheoremBaseObject field with its original rank 2 through 4 antecedent. The proof reconstructs a nonzero actual automorphic part, its integral type and original residual block, then shows that the resulting Hecke point is the given point by the universal-ring property over a finite coefficient ring. Thus it concludes J is contained in the given point kernel; it does not assume this. The exact DescWeak foundation remains explicit only where the low-rank point theorem uses it.',
  'HTS1-HTS8 prove the original TwistOk in every positive rank on the same J. An odd-order conjugate-dual Galois character has a square-root power, which gives the actual adelic unitary determinant twist. Its split local character is the required square. Multiplication by this character preserves the original infinity weights, outside-place unramifiedness and depth-one vector. Full determinant laws and the guarded local comparisons give every input of HPT17 for the twisted point. The argument includes ell=3 and does not import the low-rank DescWeak premise into the all-rank twisting theorem.',
  'HLM1-HLM26 construct the full original LevelAlt with one base before every auxiliary level, including the empty set. An integral trace criterion gives projectivity without division by the quotient-group order. The actual directed union has exactly the required fixed modules and one coherent universal-ring action. At each level the determinant is first constructed over the integral Hecke algebra by compact interpolation and integral word identities; its full ordinary pair gives the surjective universal map. Classical points separate module vectors, and the old-level identification preserves the same support ideal and every original local correspondence quantifier.',
  'HTW1-HTW24 reconstruct the full level-to-Taylor-Wiles consumer. The tame Hecke relation retains its diagonal-unit terms, and a Jacquet dimension bound gives the uniform exponent n!. Explicit integral divided-difference dual families construct both comparison maps; their compositions are enlarged to exactly the original ordered-pair fEl. A canonical topologically nilpotent summand is projective, hence free, over the local diamond group algebra. Completed ordered-root and coefficient maps preserve both full trace relations and the exact theta_coefficientMap_eq. One base, one prior root lift, and one exponent then work for every auxiliary N, giving the same-J HasAut.',
  'HIA1-HIA6 assemble the complete original HidaUAlt and perform the selected rank-four support installation. The empty-level IsJ supplies one ideal carrying all six Hida fields and HasAut. The inherited selected patching, normalization, pro-ell and P1 consumers apply to that same ideal. The two actual QX Links are then handled above the same prior coefficient threshold with fixed iota, full CohP/LocCFT, original residual conditions and prime 3. This closes COUNT_II_SUPPORT as a whole selected contract. Full ModularAlt/ModUAlt is kept separate and conditional on the original PfromAut/P3core input.'
 ],
 'remaining_major_inputs':[s.replace('Cases I/II/V producers and installations for RH',
                                    'Cases I/V producers and installations for RH')
                          for s in old['remaining_major_inputs'][1:]],
 'next_targets':[
  'Construct the original EtOne, RowsAdd/RowsGood and one common AllRows arithmetic family, then all three sufficient cylinder counts. Reuse the completed finite local WeightAllRows and the newly completed same-J two-Link support producer.',
  'In parallel, complete the prescribed common geometric family: higher CoversAt, all-tuple ClsEx/uniqueness with phase rescalings, PointIdentCore, ClassSumsSpan, actual LatFull and exact F3/F4 coefficient bridges.',
  'Complete the remaining one-character, rank-three congruence, RIG_II and RH case producers; retain the extra Case III, Seed IV and rank-four chain propagation/descent branches for unrestricted Dirichlet GRH.',
  'Install the original denominator, period/height, local-gain and normalized spectral estimates on one common family, with simultaneous selector thresholds. Do not reopen the completed Hida fields, selected two-Link support, AD_VANISH_K_MATCH or HOST_RIGID_S.'
 ],
 'selected_node_progress':{'COUNT_II_SUPPORT':{
  'completed':['HED1-HED16','HAW1-HAW19','HPT1-HPT18','HTS1-HTS8','HLM1-HLM26','HTW1-HTW24','HIA1-HIA6'],
  'remaining':'None inside this exact selected rank-four two-Link Hida/P1core contract. Full arbitrary-chain P3core and ModUAlt are not inferred from this selected closure.'}},
 'updated_contracts':{'COUNT_II_SUPPORT':contract},
 'published_applications':[],
 'publication_note':'No new literature theorem is introduced as a separately classified application in this increment. Previously matched applications and the exact original retained foundations remain explicit.'
}
(ROOT/'increment_v0_45.json').write_text(json.dumps(cfg,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'components':components,'closed_selected_leaves':list(closed)},indent=2))
