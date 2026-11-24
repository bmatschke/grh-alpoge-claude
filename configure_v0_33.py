#!/usr/bin/env python3
"""Define the additive v0.33 continuation and its exact scope."""
from pathlib import Path
import json
ROOT=Path(__file__).resolve().parent
components=['finite_isotropic_average','constant_terms','global_slope','joint_support']
claims={c:[x['id'] for x in json.loads((ROOT/c/'provenance.json').read_text())['claims']] for c in components}
new=[
 'FIA1–FIA8: the original finite isotropic Heisenberg average, including character nondegeneracy, split/residue chart, weighted half-datum guard and exact phase, with one positive period for the datum and an averaging list independent of the polynomial. The stored original vector and action are used.',
 'CTC1–CTC13: compact transvection quotients, uniform compact Weil-orbit bounds, local character duality, split-half functional separation, positivity on along coinvariants, the full Fourier constant-term argument, finite-average-to-ZCusp, and genuine full cuspidality of the original base theta integral. Explicit Witt coordinates prove ordinary convergence of all unipotent constant terms.',
 'GLS1–GLS13: original ColVal dictionary at every place, exact column slope, finite hook/Fock and normalized integral Weyl estimates, checked Euclidean transference on the original trace lattice, and both GL4 slope inequalities with constant 4. All eleven FamGLmin fields are assembled on the same supplied second layer; linkGLOBAL7_min/items/link8 remains to be written.',
 'JSP1–JSP12: the actual joint Hecke-kernel ideal, explicit surjectivity on all original generators, equality with the original module annihilator, full RingProps and Dense under their stated arithmetic inputs, the same-ideal TWBase, and the single-point NiceI-to-P1 implication under explicit support contracts. Ordinary arithmetic and all-level patched-support producers remain.',
 'The selected complete-proof audit closes the three GL4 implication tasks and narrows the actual theta and Count-II producer interfaces without removing their common-object constraints. Every inherited claim, source range, compound target and original proof dependency remains available.'
]
remaining=[
 'Construct the original common recursive/geometric class member and compatible Bundle. The construction-class TuSize and RankM consumers are already complete; DesignChoices/RecAtG and common object duties remain.',
 'Finish the original base theta extension after the now proved finite cancellation and genuine cuspidality: smoothness, uniform derivative growth, lowering and prescribed type, and bounded holomorphic/Hilbert multiplicity realization, with simultaneous original ioP quantifiers. Supply same-Bundle readings, rational tests and actual RowsHold0_3.',
 'Produce actual NBuilt/NdSpec on the original local installation, including original spectra, maximal ideals and exact projection square. Retain the same family, fields, embeddings and chosen maps.',
 'Prove the original local denominator, retained defect, period-height, local gain and spectral estimates on the common family.',
 'Construct the compatible second-layer selector and class duties. The eleven FamGLmin fields and all GL4/GL6 implication calculations now have human proofs on those exact supplied inputs. Finish the numerical/lattice linkGLOBAL7_min/items/link8 assembly with Cabs=2,C0=3,C5=4,eD=2,eL=0.',
 'For RH and power-of-two-order targets finish original I/II/V. In Count II produce the original rank-four ordinary Hecke arithmetic fibers, the four remaining Hida endpoints, all-level automorphic modules and the retained single-point arithmetic/patching support inputs on the kernel ideal constructed here, on both original Links after one threshold at fixed iota.',
 'For unrestricted Dirichlet targets additionally reconstruct actual Case III, SeedIV and chain propagation/descent on the original records. The two-primary specialization does not supply universal Count III.',
 'The AQ positive-part endpoint remains an alternative conditional route with its own unproduced arithmetic envelope.'
]
priority=(
 'The next bounded global task is the residual linkGLOBAL7_min/items/link8 assembly from the now complete same-selector FamGLmin package. '
 'The principal common analytic producer is the original smooth-growth/lowering/Hilbert realization after the now proved finite averaging and cuspidality; do not reconstruct those completed arguments again. '
 'In parallel prioritize the original rank-four ordinary arithmetic/control and all-level same-ideal support producers, using JSP to avoid repeating the kernel and single-point transport. '
 'Retain one common Bundle, actual coefficient embeddings and original quantifier order throughout; no complete final theorem is asserted before all root dependencies are supplied.'
)
updates={
 'BTH3':(['CTC10','CTC13'],'The original convergent base integral now also has a complete genuine cuspidality proof, using FIA8 and the CTC compact-quotient/Fourier arguments. Its full smooth Hilbert extension is still separate.'),
 'BTH12':(claims['finite_isotropic_average']+claims['constant_terms'],'The finite isotropic average and the full original constant-term/cuspidality subarguments are supplied. The remaining coupled base producer retains same-Bundle readings, smoothness/uniform derivative growth, lowering/type and original Hilbert realization, rational tests and actual base rows.'),
 'RSL13':(claims['global_slope'],'The three original GL4 implications and the same-selector FamGLmin assembly are supplied, including exact column slope and constant4. The compatible second layer and residual linkGLOBAL7_min/items/link8 numerical/lattice join remain.'),
 'QX10':(claims['joint_support'],'JSP supplies the original kernel ideal, RingProps/Dense and same-ideal TWBase, plus the one-point P1 implication under displayed original arithmetic/support inputs. Both original Links, ell=3, fixed iota and one coefficient threshold are retained. COUNT_II_SUPPORT remains a genuine producer.'),
 'DA1':(sum(claims.values(),[]),'The selected final ten-input interface is unchanged. Three GL4 implication leaves are closed; theta and Count-II producer obligations are narrowed precisely. No unproduced common family or support theorem is inferred.'),
 'GH7':(sum(claims.values(),[]),'These reductions apply on both roots. RH still uses original I/II/V; unrestricted Dirichlet GRH also uses III. The original formal proof is accepted as correct, while the human reconstruction remains partial.')
}
cfg=dict(artifact_version='0.33',date='2026-11-22',predecessor_version='0.32',components=components,
 expected_new_claims=sum(map(len,claims.values())),component_claims=claims,
 scope='Partial human reconstruction of RH and Dirichlet GRH, accepting the underlying Lean proof as fully checked and correct. Version 0.33 proves original finite averaging and genuine theta cuspidality, the three GL4 implications and FamGLmin assembly, and same-ideal Hecke/support transports. Original common geometric, analytic, ordinary arithmetic and patched-support producers and the final global join remain. No Lean build or kernel replay is claimed.',
 new_in_this_version=new,remaining_major_inputs=remaining,next_local_priority=priority,
 claim_updates={k:dict(supplied_by=v[0],statement=v[1],scope='Additive scope update; every predecessor field, source and dependency edge retained.') for k,v in updates.items()},
 precision_notes=[
 'Formal correctness is accepted. Category D means incomplete human source understanding only.',
 'A is a checked direct published application; B is an independently reconstructible argument; C is a substantial remaining reconstruction; D is a human source-understanding issue. Category and proof completion are separate.',
 'The same original datum supplies all finite-average objects. A fixed positive period works across indices/parameters/translates; its list is independent of the polynomial, not of the other parameters.',
 'CTC proves ordinary unipotent integral convergence; the formal integral_undef convention does not replace human cuspidality.',
 'The Closed epsilon cutoff and transport tuple precede the supplied family/class witness. Eventual x thresholds may depend on that family/class witness, but precede the indices, places and other uniformly bounded variables.',
 'All eleven FamGLmin fields are now proved on the original supplied compatible second layer. Its existence and final numerical/lattice assembly remain explicit.',
 'RingProps, Dense and TWBase use the exact Hecke-kernel ideal. They do not construct the ordinary arithmetic inputs or HasAut; the one-point P1 proof retains the six named arithmetic/patching contracts.',
 'All selected obligations retain original fields, embeddings, metrics, same-object bindings and threshold order. Leaf counts are not completion percentages or mathematical minimality claims.',
 'No Lean replay or PDF production. Draft TeX checks syntax and references; historical overfull warnings remain recorded.'
 ])
(ROOT/'increment_v0_33.json').write_text(json.dumps(cfg,ensure_ascii=False,indent=2)+'\n')
print('Configured',cfg['expected_new_claims'],'new claims.')
