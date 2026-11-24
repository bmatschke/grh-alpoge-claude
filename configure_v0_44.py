#!/usr/bin/env python3
"""Exact v0.44 progress: original automorphic parts, points, and same-J ring."""
from pathlib import Path
import json
ROOT=Path(__file__).resolve().parent
old=json.loads((ROOT/'increment_v0_43.json').read_text())
nodes={n['id']:n for n in json.loads((ROOT/'dependency_audit_v0_43/obligation_map.json').read_text())['nodes']}
contract=nodes['COUNT_II_SUPPORT']['contract']
a=contract.index('OTW12 proves one original theta')
b=contract.index('The selected Raw patching',a)
contract=contract[:a]+(
 'OTW12, ITA1–ITA13 and CAP17 supply the original theta, integral TypeForAlt and UnitaryHeckeData over the unchanged O. '
 'FNL, OST, WRP, OCT, OHA, SMP and ASP supply the original finite-level/HSet, ordinary/freeness/base-change, weight, control, Hecke-algebra and specialization fields. '
 'ADP and CFD give the actual automorphic and classical decompositions; AFS gives the original domain, DenseWt, TWtBridge, faithful fibers, scalar action and separation. '
 'LTP now gives all original local transports, actual admissible split components and one simultaneous family. BCS proves BaseChangeIsobaricN to DefiniteN to full BcSpeh under the original bc foundation, with all Speh lengths. '
 'GUA constructs the literal GalUnitaryT from the original RowT/PropsB foundation, with full IsRecT and bridge quantifiers, exact half twists, all required unramified places, pairing and conditional cusp output. '
 'UPA fills all sixteen PartAltAlt fields and all four point properties on one representation descending through the actual V.pr; it proves full partX_alt/partU_alt, installs AuTeichEx AutomorphicHeckeSet and the bare same-J TJDense endpoint. '
 'OFL and HEP give the original ordered ordinary flags and complete Out point record, and JRP gives every original RingProps field for that same IsJ ideal. '
 'The remaining arithmetic producers are the four exact Hida endpoints PointTheoremBaseObject, ArithmeticPointDecomposition, IrrArithPointsAutomorphicAway and TwistOk, '
 'followed by all-level same-ideal LevelAlt/TWAut/HasAut on both original Links. The explicit published base-change, polarized attachment, local representation and period foundations retain their original scope. '
)+contract[b:]

cfg={
 'artifact_version':'0.44','date':'2026-11-23','source_commit':old['source_commit'],
 'components':['local_transport_v44','base_change_v44','galois_assembly_v44','automorphic_installation_v44','ordinary_flags_v44','hecke_eigenpoints_v44','ring_properties_v44'],
 'closed_selected_leaves':{},
 'closed_nested_producers':[
  'All seven original PartUR2 local transports, actual admissible split components and unramified/spherical equivalence, with one simultaneous component family',
  'Full DefiniteN, AscComp and BcSpeh consumers of the original BaseChangeIsobaricN foundation, including every positive Speh length and all-unramified cusp spherical factors',
  'Full PlainGd, ProdT, HalfG, SumFamG, RecTotT and FrobTotT consumers, and literal GalUnitaryT/GuWrap under the original RowT and local/period foundations',
  'Full original quotient descent, spherical Hecke/Frobenius reading, AtLT and exact global-character inertia comparison',
  'All sixteen PartAltAlt fields, all four UnitaryPointProperties, strengthened partX_alt and partU_alt on the same original representation',
  'Original AuTeichEx AutomorphicHeckeSet and bare TJDense for the same original IsJ ideal, without the previous extra hAut supplier',
  'Full original rank-one LocCharDR and ordFlag_alt, with ordered HasFlag, every-bridge PotCrys, original Artin convention and no added semisimplicity premise',
  'Full original TCoreEig and OrdCoreH Out.pt, completing the original Out record on its original automorphic-Hecke-set input',
  'Full original TJRing/RingProps for the same IsJ ideal, including the top ideal, exact type/ordinary/polarized determinant laws and auxiliary unramified condition'
 ],
 'status':(
  'Partial human reconstruction of RH and unrestricted Dirichlet GRH, accepting the pinned Alpoge–Claude formal proof as fully checked and correct. '
  'Version 0.44 reconstructs the original automorphic-part supplier, installs the same-J density theorem, proves the full ordinary Hecke-point record and the same-J ring-properties theorem. '
  'The base-change, polarized cuspidal attachment, local correspondence and period foundations are retained explicitly at their original scope. '
  'The four later Hida endpoints, all-level same-J automorphy on both rank-four Links, common geometric/arithmetic families and global quantitative producers remain. '
  'No new whole selected leaf is closed: the 31-entry register keeps its complete contracts. No Lean build or kernel replay is claimed.'),
 'local_conclusions':[
  'LTP1–LTP21 reconstruct every original PartUR2 local transport on the actual coefficient-valued function space. The full matrix type equation, dual infinity weight, exact spherical sums for every natural index and distinguished depth-one Kc(1) are preserved. The first six suppliers add no type-openness hypothesis, and the isotypy/spherical endpoints include the zero part. The chapter constructs actual admissible split components from the positive form and finite multiplicity, proves unramified/spherical equivalence for every component, and makes one family choice before all consumers. Outside-place unramifiedness also covers nonsplit places.',
  'BCS1–BCS19 prove the full BaseChangeIsobaricN→DefiniteN→BcSpeh bridge under the original named base-change input. Positivity makes the original discrete local factors unitary; irreducibility replaces the selected subquotient by the whole normalized product. The supplied ascending embedding is consumed directly, avoiding a new global residual-spectrum classification. Smooth Hermitian duality supplies the exact descending quotient, the matched generic-unitary classification and elementary segment bound give its unique cosocle, and the block Capelli and finite Satake calculations preserve all twists, all Speh lengths, split maps, inert clauses and every unramified place.',
  'GUA1–GUA18 construct one continuous semisimple GalUnitaryT representation from the full original RowT/PropsB cuspidal attachment. The half shifts are implemented by actual automorphic twists, so no square root of the cyclotomic character is presumed. Explicit finite period sums preserve all original bridges and embedding quantifiers. Every IsRecT map has the required product/Speh/spherical readings. The geometric Frobenius inverse and cyclotomic multiplier 1−n are checked. Chebotarev gives the same pairing for every complex conjugation. Irreducibility forces one positive block of length one and yields the actual regular algebraic cusp, with every required unramified Satake place and split component.',
  'UPA1–UPA18 descend that same representation through the actual level map V.pr, preserve semisimplicity and the same polarization matrix, and fill all sixteen PartAltAlt fields and all four UnitaryPointProperties. The exact source Hecke polynomial, every Frobenius lift, all local correspondences, every Teichmuller family and every period bridge are kept. Zero monodromy plus finite inertia gives the original diagonal inertia action over the unchanged coefficient field. The full partX_alt/partU_alt installs AuTeichEx AutomorphicHeckeSet. Substitution into the already written AFS separation argument proves bare TJDense for the same IsJ ideal, with no additional automorphic-Hecke-set supplier.',
  'OFL1–OFL16 prove the complete original ordinary-flag consumer. Local algebraic weights are globalized on an auxiliary CM field with exactly the same local completion; the original Hecke-character inputs give the precise rank-one DRat law. Distinct inertia characters yield one-dimensional character projectors and zero monodromy. Finite averaging, faithfulness of all Frobenius translates, and a Vandermonde period sum produce a nonzero fixed period. The fundamental crystalline intersection turns it into a Galois invariant when all weights are nonnegative. Twisting by the first ordinary character and induction on the quotient give the full ordered flag, together with potential crystallinity for every original bridge.',
  'HEP reconstructs the original Hecke-eigenpoint dictionary and completes OrdCoreH Out.pt. The exact normalized U-operator eigenvalues telescope to the individual ordinary characters, the original Artin and cyclotomic identities recover their full local formulas, and equality at the original dense Frobenius set gives equality of determinant laws. At every admitted arithmetic point, the actual nonzero part from AFS supplies one continuous semisimple representation, its full determinant law and the prescribed point properties. Under the original Good guard on that same point, OFL supplies its ordered flags and every-bridge potential crystallinity. The original point, weight, scalar and all-place quantifiers are retained.',
  'JRP proves the full original RingProps theorem for the very same IsJ ideal. It descends the polarized determinant relation, both kernel relations, ordinary characteristic polynomials and ordered products, and every Teichmuller inertia type through a jointly separating family of actual Hecke points. It retains the original auxiliary V0ok condition and proves its inertia-vanishing consumer. Finiteness and torsionfreeness are transported through the actual quotient isomorphism B/J≅T. The zero-module branch J=B is treated directly. This completes the ring and dense fields of the later six-field HidaPropsAlt record; its other four fields remain separate endpoints.'
 ],
 'remaining_major_inputs':[
  'Construct the four remaining exact Hida outputs: PointTheoremBaseObject, ArithmeticPointDecomposition with its cofinite strict Frobenius-norm ratio, IrrArithPointsAutomorphicAway and TwistOk. Then install all-level same-J LevelAlt/TWAut/HasAut on BOTH original rank-four Links, retaining the same ideal J, fixed iota, prime 3, full CohP/LocCFT and one common coefficient threshold. The original integral type, Hecke data, automorphic parts, complete Out point record, RingProps and bare same-J density are now available and should not be reconstructed again.',
  *old['remaining_major_inputs'][1:]
 ],
 'next_targets':[
  'Reconstruct endShapeT and ArithmeticPointDecomposition with the exact cofinite strict Frobenius-norm ratio, preserving all original Speh lengths until the appropriate dimension/irreducibility step. Reuse BCS/GUA/UPA and the same original point representations.',
  'In parallel, the exact remaining Hida fields PointTheoremBaseObject, IrrArithPointsAutomorphicAway and TwistOk; then full HidaPropsAlt/ModularAlt and all-level same-J HasAut on both original Links.',
  'Continue the independent original EtOne/RowsAdd/RowsGood/common AllRows arithmetic counts, common geometric/local family, one-character/congruence/RIG_II and original global estimate producers. The v0.43 finite local WeightAllRows and its unchanged Wg remain available.'
 ],
 'selected_node_progress':{
  'COUNT_II_SUPPORT':{'completed':['LTP1–LTP21','BCS1–BCS19','GUA1–GUA18','UPA1–UPA18','OFL1–OFL16','HEP full Out point endpoint','JRP full same-J RingProps'],
   'remaining':'The four exact Hida endpoints PointTheoremBaseObject, ArithmeticPointDecomposition, IrrArithPointsAutomorphicAway and TwistOk, followed by all-level same-J automorphy on both original Links. The original BaseChangeIsobaricN, RowT/PropsB, local representation and period foundations retain their explicit foundation scope.'}
 },
 'updated_contracts':{'COUNT_II_SUPPORT':contract},
 'published_applications':[
  {'title':'Spherical Satake at the exact source normalization','source':'B. H. Gross, On the Satake isomorphism, Proposition3.6, formula(3.14), Proposition6.4; Haar normalization(2.5)','url':'https://people.math.harvard.edu/~gross/preprints/sat.pdf','claims':['UPA5','UPA6','UPA7'],'hypotheses_checked':'Actual finite characteristic-zero local field, GL_n, maximal integral compact and volume1, smooth irreducible spherical representation, all fixed vectors and uniformizers; original Hecke polynomial and geometric Frobenius inverse are derived separately.'},
  {'title':'Generic unitary local representations as products of discrete-series twists','source':'C. Mœglin and J.-L. Waldspurger, Le spectre résiduel de GL(n), §§I.10–I.11, pp.639–640','url':'https://www.numdam.org/item/10.24033/asens.1595.pdf','claims':['BCS8','BCS9','GUA4','GUA5'],'hypotheses_checked':'Actual nonarchimedean characteristic-zero local field, positive rank, smooth irreducible generic unitarisable complex representation, original normalized upper-parabolic induction. The Whittaker condition eliminates longer local Speh factors and leaves real exponents in the strict interval(-1/2,1/2). No temperedness assumption or global residual-spectrum classification is imported.'}
 ]
}
(ROOT/'increment_v0_44.json').write_text(json.dumps(cfg,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'components':cfg['components'],'closed_selected_leaves':cfg['closed_selected_leaves']}))
