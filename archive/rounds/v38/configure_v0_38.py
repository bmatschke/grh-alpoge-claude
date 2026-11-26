#!/usr/bin/env python3
"""Record exact v0.38 closures, original-object guards and remaining producers."""
from pathlib import Path
import json
ROOT=Path(__file__).resolve().parent
components=['finite_volume','seed_boundedness','count_raw','division_identity']
read=lambda p:json.loads(p.read_text())
claims={n:[c['id'] for c in read(ROOT/n/'provenance.json')['claims']] for n in components}
allnew=sum(claims.values(),[]);analytic=claims['finite_volume']+claims['seed_boundedness']
old_count=len(read(ROOT/'history/version_0_37/provenance.json')['claims'])
def span(n):return claims[n][0]+'–'+claims[n][-1]
new=[
 span('finite_volume')+': the complete original FiniteVolume2 for every original CM unitary group, every Haar measure and every supplied a.e. fundamental domain; actual FinPair for all stored targets before theta parameters; finite adelic classes and the exact real arithmetic-component dictionary. Borel applications have their reductivity, rational-character, adelic-topology and quotient-measure hypotheses checked.',
 span('seed_boundedness')+': pre-Hilbert full-center finiteness of the actual highest-weight seed; exact ZI/additive-adele and all-parabolic cusp descent; checked Miller–Schmid rapid decay and finite Siegel covering; the initial bound for every original i,t,x. Together with FV and inherited ASB/SPR, this completes the all-parameter original theta-extension construction and the whole selected BASE_THETA_CUSPIDAL_EXTENSION leaf on its common-data premises.',
 span('count_raw')+': the selected full-block completed representation and actual coefficient DVR, bounded cotangent derivatives and the exact first-order Selmer injection, selected limit cohomology on the supplied limit, actual finite power-series presentation, presOut0/GalOut dimension comparison and h=0 ChainAbs consumer. Original S4, patched maps/modules and S5 support, and coefficient/pro-ell descent remain producers; the whole Raw statement is not closed.',
 span('division_identity')+': the first literal DivDef3 on the same CSR selected realization, including inner/terminal level identities, exact row projector and composite identities, and the first theta subrecord. The proof retains original common readings, Pins/Holds, stored nonzero chain, full original five-predicate real-group input DI.2, including Harish–Chandra modules and generic cusp decay/integrability, and group tie, PLUS the explicitly additional RowPairInt producer for the actual pairs and finite translates. It is a conditional sufficient refinement, not the whole original theorem from its original premises alone. It does not construct the second DivRows3 theta square or the common datum.',
 f'There are {old_count+len(allnew)} cumulative human proof claims, with {len(allnew)} new claims. Exactly one whole selected leaf closes: BASE_THETA_CUSPIDAL_EXTENSION. The selected register now has 33 open coupled leaves: 22 C, 9 B and 2 D. The human RH/Dirichlet-GRH reconstruction remains incomplete.'
]
remaining=[
 'Produce the actual common recursive/geometric member, original Read/ReadL and rational tests, host/frames, MultEq support, eigensystem/carrier/parts and all-embedding logLam, HD/d3b and NEb. First DivDef3 is reconstructed on its explicit original premises plus additional RowPairInt; common construction, stored nonzero chain and group tie remain. Keep the second DivRows3 theta square separate.',
 'For the generic multiplicity-space row pairing, supply the exact required integrability (or the retained original universal CuspRapidDecay sufficient theorem). The initial highest-weight theta seed theorem does not prove universal decay for every IsAutFunSm/IsCuspFun. Determine whether the smaller pair-integrability contract can be supplied directly; the original nonzero IsItW chain is a separate input, and DI12 requires no scalar-witness existence theorem.',
 'Produce actual NBuilt/NdSpec and the original local projection square on the common installation, with unchanged spectra, maximal ideals, coefficient embeddings and metrics.',
 'Supply the original denominator, retained-defect, period-height, local-gain and normalized spectral estimates on the same family.',
 'Construct the compatible second-layer selector and duties. All common family, Bundle/BWit/BunU, FamGLmin and final assembly consumers retain their exact upstream inputs.',
 'For RH and two-primary targets finish original Cases I/II/V. CountII retains ordinary/control/separating arithmetic fibers and type/neatU/TThetaEx, four Hida endpoints and all-level same-J HasAut. Its selected Raw route now has the full-block representation, cotangent/presentation and ChainAbs comparison, but actual S4, patched maps/modules with S5 support and coefficient/pro-ell descent remain. Preserve full CohP/LocCFT/N4, both rank-four Links, ell=3, fixed iota and one common coefficient threshold.',
 'Unrestricted Dirichlet targets additionally retain CaseIII, SeedIV and original chain propagation/descent. The two-primary route supplies no universal CountIII.',
 'The optional AQ positive-part route and separate arithmetic envelope remain optional. Historical RF16 remains governed by DEX11.'
]
priority=(
 'With the initial finite volume and boundedness gates closed, prioritize actual common geometric readings and rational-test/base-row production, together with the exact nonzero chain and pairing inputs to the now reconstructed first DivDef3. '
 'The generic row proof needs integrability for its actual multiplicity-space pairs; first inspect that smaller contract before undertaking the stronger universal quotient-height CuspRapidDecay theorem. '
 'In parallel pursue the original h=0 patched support producer S4, its patched ring/maps/modules and S5 on the same point/J/Kap/TWAut, followed by coefficient/pro-ell descent. The selected full-block representation, cotangent bound and ChainAbs consumer should not be reconstructed again. '
 'Ordinary/control, type/neatU, four Hida endpoints and all-level same-J HasAut remain major arithmetic producers; local installation and spectral estimates remain common to both final targets. '
 'Keep all selected graph edges, original objects, common thresholds, Haar measures, metrics and levels unchanged.'
)
updates={
 'CTC13':(analytic,'The actual initial seed bound and target FinPair are now supplied by FV/SBD; the original all-parameter cuspidal theta extension is complete on the original common-data premises.'),
 'TAE13':(analytic,'SBD13–16 and FV8/FV11 close the two initial analytic gates and complete the all-parameter original theta map without asserting the stronger universal CuspRapidDecay predicate.'),
 'HCU18':(analytic,'The initial highest-weight seed has full enveloping-center finiteness before any Hilbert construction. FV/SBD supply its finite pair and bound; the inherited full pointwise MMap can now be applied.'),
 'RQC22':(analytic,'The initial target FinPair and seed bound are now reconstructed. All original quotient, representative, derivative and Sobolev conventions remain unchanged.'),
 'SPR25':(analytic,'Both initial analytic suppliers are closed on the actual common datum; SBD15 supplies all i,t theta maps and stored-choice activation without introducing a parameter threshold.'),
 'BTH12':(allnew,'The complete selected cuspidal-extension leaf is closed. The first DivDef3 consumer is reconstructed on its original selected inputs. Common geometric readings, rational tests and actual base rows remain open.'),
 'JSP11':(claims['count_raw'],'The selected Raw route has original full-block S6, OO/rF, cotangent/presentation and h=0 ChainAbs comparison; actual S4, patched maps/modules and S5 support, and coefficient/pro-ell descent remain. The same selected Choice/B1/B2 witness and same J are retained.'),
 'CIP12':(claims['count_raw'],'Selected first-order counting now feeds the original completed-point cotangent and dimension comparison. No all-level ordinary or automorphic module producer is inferred.'),
 'QX10':(claims['count_raw'],'Both original rank-four Links retain ell=3, fixed iota and the common coefficient threshold. The selected completed representation and one-point comparison are supplied; Raw support/descent and ordinary/automorphic production remain.'),
 'CSR15':(claims['division_identity'],'The first updated DivDef3 is reconstructed on the same selected realization and its explicit original predicates plus the additional RowPairInt supplier. This closes its record/identity consumer, not the common reading, stored-chain, group-tie or generic pairing producers.'),
 'DA1':(allnew,'The ten-input final interface and selected logical edges are unchanged. The analytic theta-extension leaf closes; 33 selected whole obligations remain.'),
 'GH7':(allnew,'RH retains Cases I/II/V and unrestricted Dirichlet GRH additionally III. The initial analytic branch is complete on common-data premises, while actual common, local/spectral and arithmetic producers remain.')
}
cfg=dict(artifact_version='0.38',date='2026-11-22',predecessor_version='0.37',predecessor_claim_count=old_count,
 components=components,expected_new_claims=len(allnew),component_claims=claims,
 scope='Partial human reconstruction of RH and Dirichlet GRH, accepting the underlying Alpoge–Claude Lean proof as fully checked and correct. Version 0.38 closes the full selected cuspidal theta-extension obligation, reconstructs selected completed-point/cotangent/dimension consumers and the first exact division identity. Common geometric/readings/rational-test, generic pairing, local/spectral, patching and ordinary/automorphic producers remain. No Lean replay is claimed.',
 new_in_this_version=new,remaining_major_inputs=remaining,next_local_priority=priority,
 claim_updates={k:dict(supplied_by=v[0],statement=v[1],scope='Additive scope update; every predecessor field, source array and claim edge remains.') for k,v in updates.items()},
 precision_notes=[
 'A denotes a checked published application; B an independently reconstructed elementary/moderate argument; C substantial reconstruction; D unresolved human source understanding, not an alleged formal error.',
 'FV proves the entire original finite-volume statement with every Haar measure and supplied a.e. fundamental domain. Actual target FinPair choices precede all t,x.',
 'SBD proves full enveloping-center finiteness directly from the initial highest-weight equations, before Hilbert realization. Post-Hilbert SPR central finiteness is not used to obtain the initial bound.',
 'Original ZI is identified exactly with the additive adele group. Every proper rational parabolic contains a central rational transvection constructed from a positive top cocharacter weight; no new cusp convention is substituted.',
 'Miller–Schmid Theorem A is applied only after checking smoothness, arithmetic subgroup, compact center, faithful-norm moderate growth, full-center finiteness and every proper rational-parabolic cusp. Finite rational Siegel translates are checked separately.',
 'SBD supplies all actual initial seeds and the selected analytic extension. It does not prove universal global quotient-height decay for arbitrary source IsAutFunSm/IsCuspFun, still retained in the generic DI row theorem.',
 'CRW keeps the same h=0 full block a=n=4, original point/Kap/T/TWPl/TWAut and ideal J. Odd N=0 is a property of this supplied full-block representation, not a universal Sel1 vanishing claim.',
 'Chenevier is applied to the full determinant law over the actual completed ring, with split absolutely irreducible residual law. No n! inversion occurs; ell=3 remains included.',
 'Actual S4, patched ring/maps/modules with S5 support and final coefficient/pro-ell descent remain in Raw. A cotangent or dimension comparison alone is not Raw.',
 'DI retains original Pins/Holds, nonzero IsItW chain, full original five-predicate real-group input DI.2 and group tie, plus explicitly additional RowPairInt. The original per-coset growth to global IsUnifModerate conversion through polynomial unitary reduction is not reconstructed. The exact nP inverse quotient measure and same CSR updated packet are retained.',
 'Only first DivDef3 is proved; the stronger second DivRows3 theta square is not silently supplied.',
 'All 245 historical compound targets in 107 groups and all 121 selected logical nodes/edges remain. Exactly BASE_THETA_CUSPIDAL_EXTENSION closes; open counts 33=22C+9B+2D are not completion percentages.',
 'No PDF production or Lean replay. Draft TeX checks syntax and references only; mathematical review is separately bound to released proof bytes.'
 ])
(ROOT/'increment_v0_38.json').write_text(json.dumps(cfg,ensure_ascii=False,indent=2)+'\n')
print('Configured',len(allnew),'new claims;',old_count+len(allnew),'cumulative.')
