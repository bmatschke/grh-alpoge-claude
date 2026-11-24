#!/usr/bin/env python3
"""Current exact scope and additive claim updates for the v0.32 continuation."""
from pathlib import Path
import json
ROOT=Path(__file__).resolve().parent
components=['degree_prime_size','rank_producer','base_theta','global_local_estimates']
claims={c:[x['id'] for x in json.loads((ROOT/c/'provenance.json').read_text())['claims']] for c in components}
new=[
 'DSZ1–DSZ10: exact original formal degree and h3, source gap versus the actual DC existence threshold, actual family coordinate bounds, harmonic Vandermonde upper comparison, exact factorial cancellation and the original TuSize with cTmin. Built membership supplies RealTied and the earlier volume theorem on the same construction class.',
 'RMP1–RMP11: original discriminant modules, self-dual enlargement, exact T^k−1 functional-stabilizer index, auxiliary and global indices, genus mass, trivial level stabilizers, literal ClassNumberFormula₂, Mu0Tie and RankM. The construction-class pick supplies the same Bundle.R, so no independent rank-selector premise remains.',
 'The base-theta chapter gives the original base square through a smaller exact set of supplied analytic, realization and rational-test inputs. Actual integral convergence and the finite Hilbert/idempotent/matrix arguments are proved; the residual smooth cuspidal extension and compatible readings remain explicit.',
 'The global-local chapter gives the original eventual HidaSetting from the lower TuSize inequality and reconstructs the integral, ramified, second-branch and finite composite-length arguments on the actual supplied forms and lattices. Compatible original forms/characters remain upstream.',
 'The complete-proof audit retains every inherited obligation, closes the design size/rank and completed global slots in their exact construction-class or supplied-form scopes, and exposes the smaller same-Bundle theta producer cut. Closed consumers do not assert independent existence of the common family.'
]
remaining=[
 'Construct the original common recursive/geometric class member and actual compatible Bundle. The separate design TuSize and RankM consumers are now complete on that construction class; DesignChoices/RecAtG and the shared common object duties remain.',
 'Supply actual base rows and the residual base-theta analytic extension, exact same-Bundle readings and rational test identities. The new convergence and finite theta arguments do not produce those deep geometric/analytic data.',
 'Produce actual NBuilt/NdSpec on the original local installation, including all original maps, spectra, maximal ideals and exact projection square. The finite local coverage consumer remains complete.',
 'Prove the original local denominator, retained defect, period-height, local gain and spectral estimates on the common family, with prescribed coefficient-field readings. Existing transport arguments do not imply these producers.',
 'Produce the common second-layer selector and class duties, complete the three original GL4 slots (actual ColVal dictionary, lower slope and class-map upper slope), and write the final global numerical/lattice assembly. The h3 and GL6 implication tasks reconstructed in this version no longer remain separate unwritten steps.',
 'For RH and power-of-two-order targets finish I/II/V: the same-ideal rank-four ordinary support/Hida/P1 producer, original one-character/adjoint/congruence inputs, and original Case-V support/catalogue/rigidity transports. CountI and CountV have different fixed fields and prime scopes.',
 'For unrestricted Dirichlet targets additionally reconstruct actual Case III, SeedIV and chain propagation/descent on the original records. The specialization removing III for 2-power-order targets is not a universal CountIII theorem.',
 'The AQ positive-part endpoint is an alternative conditional route with its own unproduced arithmetic envelope; it does not shorten the selected source route without that supplier.'
]
priority=(
 'Prioritize the common actual row/theta reading and smooth cuspidal extension producer, with its base rational tests, because it is shared with small rank, local specialization and the period/spectral constructions. '
 'The next bounded global branch is the actual ColVal dictionary and its two GL4 slope estimates, then the final FamGLmin assembly; h3, TuSize, RankM and the completed GL6 calculations should not be reconstructed again. '
 'In parallel retain the same-ideal rank-four ordinary Hecke/support producer as the principal independent count branch. '
 'Construct all required inputs on the same Bundle before claiming a complete family or final theorem.'
)
updates={
 'DEX7':(['DSZ10','RMP11'],'On the exact Built construction class with cT=cTmin, the Closed TuSize and RankM inputs are now proved. The original compatible DesignChoices/common class-member construction remains. The two projections use the same class and bundle; no independent witness is selected.'),
 'DEX11':(['DSZ10','RMP11'],'The conditional RecExP-to-DesignChoices route is unchanged. Its separate size/rank obligations are now discharged on the construction class; actual RecAtG, common object/bundle duties and nonemptiness remain.'),
 'DC20':(['DSZ1','DSZ2','DSZ3'],'The exact original-row h3 finite bounds and source gap-to-DC existence comparison are written out. The already named HC-Deg and exact compact-dual normalization retain their checked scopes.'),
 'QW9':(['DSZ4','DSZ5','DSZ6','DSZ7','DSZ8','DSZ9','DSZ10'],'The earlier QW lower window combines with a new harmonic upper comparison on the actual family cloud to prove literal TuSize. No full Vandermonde variation or count package is claimed.'),
 'CR6':(['RMP1','RMP2','RMP3','RMP4','RMP5','RMP6','RMP7','RMP8','RMP9','RMP10','RMP11'],'The actual class number, original level indices and original Mu0Tie/RankM are now supplied. The proof retains the original cls0 and proves a stronger class-count assertion without GBig.'),
 'RSL13':(claims['global_local_estimates']+['DSZ3'],'The actual h3 and completed GL6 implication proofs are supplied by the new chapters. Original GL4 slots, compatible selector production and final numerical/lattice assembly remain.'),
 'SLR9':(claims['base_theta'],'The base theta consumer now has a smaller explicit coupled producer cut. The exact new theta proofs and their residual analytic/read/test inputs govern this scope; actual RowsHold0_3 remains a separate same-Bundle producer.'),
 'DA1':(['DSZ10','RMP11']+claims['base_theta']+claims['global_local_estimates'],'The exact ten-argument final interface is preserved. The current graph separates newly proved size/rank/global/theta implications from the surviving common family and arithmetic count producers.'),
 'GH7':(['DSZ10','RMP11']+claims['base_theta']+claims['global_local_estimates'],'These reductions apply to both selected roots. RH still requires I/II/V and all same-family producers; unrestricted Dirichlet targets still additionally require Case III. No complete human theorem is asserted.')
}
cfg=dict(artifact_version='0.32',date='2026-11-22',predecessor_version='0.31',components=components,
 expected_new_claims=sum(map(len,claims.values())),component_claims=claims,
 scope='Partial human reconstruction of RH and Dirichlet GRH, accepting the underlying Lean proof as fully checked and correct. Version 0.32 supplies actual original degree/size and class-number/rank proofs, reconstructs the global local calculations and refines the base-theta producer cut. Common geometric/analytic/arithmetic producers and the original counts remain. No new Lean build or kernel replay is claimed.',
 new_in_this_version=new,remaining_major_inputs=remaining,next_local_priority=priority,
 claim_updates={k:dict(supplied_by=v[0],statement=v[1],scope='Additive current-scope update; all original fields, sources and claim edges retained.') for k,v in updates.items()},
 precision_notes=[
 'The formal Lean proof is assumed fully checked and correct. Category D refers only to incomplete human source understanding.',
 'A matched published application is category A; a completed conditional implication can be category B while its producer remains C. Category and proof completion are distinct.',
 'The exact construction class cls(Q,Lk,E) supplies Built/pick as part of membership. Its nonempty compatible family must still be constructed; this is not inferred from the new Closed size or rank implications.',
 'Retain Cprime=WithChN(A intersect target class), Cdes=WithTw(WithSm Cprime), and top-level C=WithChN A. All thresholds are joined before one family is selected.',
 'The TuSize upper proof replaces only the needed upper estimate. It does not assert the source full Vandermonde variation/counting theorem.',
 'The original local Hecke calculations consume the same Forms0, character, stabilizer and metric records. They do not construct a new compatible selector.',
 'Every inherited compound continuation record remains. Current selected sufficient leaves are the exact proof-task register, not a completion percentage or a proof of absolute mathematical minimality.',
 'No new Lean build or kernel replay. Draft-mode TeX verifies syntax and references, produces no PDF and makes no visual-layout certification.'])
(ROOT/'increment_v0_32.json').write_text(json.dumps(cfg,ensure_ascii=False,indent=2)+'\n')
print('Configured v0.32:',cfg['expected_new_claims'],'new claims in',len(components),'components.')
