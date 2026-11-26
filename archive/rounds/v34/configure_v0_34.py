#!/usr/bin/env python3
"""Define the additive v0.34 continuation and exact retained producer scopes."""
from pathlib import Path
import json
ROOT=Path(__file__).resolve().parent
components=['global_count','global_assembly','theta_extension','count_ii_producer']
claims={name:[c['id'] for c in json.loads((ROOT/name/'provenance.json').read_text())['claims']] for name in components}
new=[
 'GVC1–GVC18: exact actual degree products and cross-word Vandermonde cancellation give CountF; all sixteen numerical and eight weight clauses give NumsL/WtsL; direct exact Conclusion5/6 and F5/F6 estimates give SlopesMF. The required logarithmic-derivative window is a projection from the original FamP size record. Stronger PartFive intermediate claims are not silently asserted.',
 'GFA1–GFA12: exact type-prime quotient cost 36, direct original correction bound Ta≤b², finite-place quotient slopes with the literal support and metrics, positive RR dual rank, exact arithmetic Gram-map dictionary, and the literal frame inequality for every admissible H, including zero spread. Original NodesF, all seventeen Win_at clauses and all four Char_at clauses are installed. The remaining final-global work is LossFS(Fm,0) and the same-family linkCore/ChainTied/Closed join.',
 'TAE1–TAE13: real Gaussian differentiation in every smooth seminorm, derivative transport for the original full action, one unchanged growth exponent for every derivative word, dominated differentiation of the actual integral, original-vacuum transfer, and the exact mixed-Laplacian lowering coefficient. Under explicit common ioP and LowSm/LowIrr premises these give the complete analytic/cuspidal lowest-type packet. Actual common ioP, lowest-type multiplicity one and Hilbert multiplicity realization remain producers.',
 'CIP1–CIP12: exact source reciprocity for every original IsLocalArtin at the split CM places, with the positive cyclotomic norm sign, and the full universal NiceI instance of Norm required by the original one-point support route. Integral symmetric-form diagonalization uses only a finite constant extension, preserves the original D0, ordered flags and all polynomial-law data, and includes coefficient characteristic3. Generic NiceE normalization and the other ordinary/patching producers are not claimed.',
 'Every inherited proof, source range, claim edge, compound target and optional route is retained. The selected graph still has 35 open coupled leaves (23 C,10 B,2 D), but the global, analytic and Count-II contracts are strictly narrowed. The nested Count-II reciprocity-understanding obligation is closed; no complete final theorem is claimed.'
]
remaining=[
 'Construct the original common recursive/geometric member and compatible Bundle; DesignChoices/RecAtG and common duties remain. Construction-class TuSize and RankM consumers are already complete.',
 'Finish the same-Bundle base extension after actual smoothness, uniform growth and lowering: construct one io_i satisfying IsIoW for every parameter t, prove LowSm/LowIrr for the full original lowest compact type, supply boundedness/target finite volume, and realize the exact integral in the original Hilbert multiplicity model. Same-Bundle readings, rational tests and actual RowsHold0_3 remain separate.',
 'Produce actual NBuilt/NdSpec on the original local installation, with original spectra, maximal ideals and projection square.',
 'Supply the original denominator, retained defect, period-height, local-gain and spectral estimates on that same family.',
 'Construct the compatible second-layer selector and duties. The eleven FamGLmin fields and now the count, source/quotient slopes, positive ranks, all-H frame, nodes, windows and characters are proved consumers. Finish the original LossFS(Fm,0) and exact same-family linkCore/ChainTied/Closed join, preserving Cabs=2,C0=3,C5=4,eD=2,eL=0.',
 'For RH and power-of-two-order targets finish original I/II/V. Count II still needs ordinary arithmetic/control and separating fibers, the four further Hida endpoints, same-J all-level HasAut, Choice, ArPl, first-order/obstruction bounds and Raw at the required NiceI route. Exact reciprocity and the required universal NiceI Norm are now supplied; original CohP and side conditions remain explicit. Both Links use one coefficient threshold at fixed iota.',
 'Unrestricted Dirichlet targets additionally retain Case III, SeedIV and original chain propagation/descent. The two-primary specialization does not imply universal Count III.',
 'The AQ positive-part endpoint remains an optional route with its own arithmetic envelope.'
]
priority=(
 'Finish the bounded shared global residual first: original LossFS(Fm,0), then the exact same-family linkCore/ChainTied installation and final Closed wrapper. '
 'In parallel reconstruct the original common ioP and lowest-type multiplicity-one/Hilbert realization, using the completed smooth-growth/lowering packet; prioritize the ordinary rank-four arithmetic/control and same-J HasAut producer for Count II. '
 'Do not repeat the completed count/frame/window/character consumers, finite-average/cuspidality, reciprocity, or NiceI normalization. '
 'Keep original common objects and threshold order explicit; completion of consumers does not create their producers.'
)
updates={
 'GLS13':(claims['global_count']+claims['global_assembly'],'The remaining final-global implication is narrowed to original LossFS(Fm,0) plus exact same-family linkCore/ChainTied/Closed installation; count, source and quotient slopes, positive ranks, all-H frame, nodes, windows and characters now have exact human proofs on the stated inputs.'),
 'RSL13':(claims['global_count']+claims['global_assembly'],'The original complete FamGLmin package now feeds reconstructed CountF, SlopesMF, PlacesF/SlopesNF, RRRankF/LatF/FrameF, NodesF/WinF/CharF consumers. Original selector/duties and the final loss/tied-ledger assembly remain.'),
 'CTC13':(claims['theta_extension'],'Actual original-action smoothness, all-word growth with unchanged exponent, dominated integral differentiation, original-vacuum passage and exact lowering are now supplied. Common all-parameter ioP, full-lowest-type smooth irreducibility, boundedness and Hilbert multiplicity realization remain explicit.'),
 'BTH12':(claims['theta_extension'],'The same-Bundle analytic/cuspidal lowest-type packet is supplied under common ioP and LowSm/LowIrr. Original geometric reading, rational tests and actual base rows remain; the packet is not yet an MMap.'),
 'JSP7':(claims['count_ii_producer'],'The nested JSP_EXACT_RECIPROCITY_MATCH obligation is closed in the entire required original split-CM scope, for every source IsLocalArtin and every admissible global Artin map, with positive cyclotomic norm sign. Arithmetic ordinary data remain.'),
 'JSP11':(claims['count_ii_producer'],'The entire universally quantified NiceI instance of Norm used here is now supplied, with finite constant extension, integral representation, ordered flags, N1–N4, original D0 and determinant law. General NiceE Norm is not claimed; five other named support inputs, HasAut, CohP and all stated side conditions remain.'),
 'QX10':(claims['count_ii_producer'],'Count II keeps both original Links, ell=3, fixed iota, one later-coefficient threshold and the same ideal for all seven properties. Exact reciprocity and required NiceI Norm are supplied; ordinary/control, remaining Hida and all-level/patching producers remain.'),
 'DA1':(sum(claims.values(),[]),'The exact final ten-input interface is unchanged. Three coupled leaves are narrowed by 55 reconstructed claims; no producer is inferred from a proved conditional consumer.'),
 'GH7':(sum(claims.values(),[]),'Both final roots benefit from the completed global, analytic and Count-II subarguments. RH still retains I/II/V and unrestricted Dirichlet GRH also retains III. The human proof remains incomplete.')
}
cfg=dict(artifact_version='0.34',date='2026-11-22',predecessor_version='0.33',components=components,
 expected_new_claims=sum(map(len,claims.values())),component_claims=claims,
 scope='Partial human reconstruction of RH and Dirichlet GRH, accepting the underlying Lean proof as fully checked and correct. Version0.34 completes exact global count/slope/frame/window/character consumers, real theta derivatives/growth/lowering, source reciprocity and the required NiceI normalization. Common geometric/analytic/arithmetic producers, final losses and tied-ledger assembly remain. No Lean build or kernel replay is claimed.',
 new_in_this_version=new,remaining_major_inputs=remaining,next_local_priority=priority,
 claim_updates={k:dict(supplied_by=v[0],statement=v[1],scope='Additive scope update; all predecessor fields, sources and dependency edges retained.') for k,v in updates.items()},
 precision_notes=[
 'Formal correctness is accepted. Category D means incomplete human source understanding only.',
 'A is a checked direct published application; B is an independently reconstructible argument; C is a substantial reconstruction; D is a human source-understanding issue. Category and completion are separate.',
 'GVC proves the required CountF/SlopesMF directly. It does not automatically prove every stronger PartFive or PropZ source intermediate.',
 'The original FamP.sizes already includes DlSize. Using that projection in these consumers does not construct the common family.',
 'GFA uses only the sufficient Ta<=b² bound. The stronger FamilyWeightSumBound is not silently closed.',
 'The frame proof holds for every H>0 satisfying the original height condition; u=0 is explicit and no H upper bound is inserted.',
 'TAE preserves one height exponent for every derivative word; actual LowSm/LowIrr and one ioP valid for every parameter remain premises.',
 'Exact reciprocity is proved in the required split-CM place scope, with every-map quantifiers; no generic local-idele injectivity is asserted.',
 'CIP closes full universal NiceI Norm with original D0 and ordered flags, including ell=3; it does not close general NiceE Norm or HasAut.',
 'The Closed cutoff and transport tuple precede the chosen family; eventual thresholds may depend on that family but precede every member, word and place.',
 'All selected obligations retain original fields, embeddings, metrics, same-object bindings and threshold order. Leaf counts are not completion percentages.',
 'No Lean replay or PDF production. Draft TeX checks syntax and references; historical overfull warnings remain recorded.'
 ])
assert cfg['expected_new_claims']==55
(ROOT/'increment_v0_34.json').write_text(json.dumps(cfg,ensure_ascii=False,indent=2)+'\n')
print('Configured',cfg['expected_new_claims'],'new claims.')
