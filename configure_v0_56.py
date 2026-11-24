#!/usr/bin/env python3
"""Record the new mathematical scope, preserving every original whole contract."""
from pathlib import Path
import json
ROOT=Path(__file__).resolve().parent
old=json.loads((ROOT/'increment_v0_55.json').read_text())
components=['polarized_base_change_v56','arithmetic_presentations_v56','reference_covolume_v56','wach_prism_v56']
new_count=sum(len(json.loads((ROOT/c/'provenance.json').read_text())['claims']) for c in components)
assert new_count==107
period=(
 'WPR supplies the full original Wach prism and the full original BS plus LocTied implication to WachEx. Its ring is the prescribed unramified integer ring W0[[T]], with the actual cyclotomic distinguished polynomial Q_s, Fontaine map, Frobenius and Galois actions. All sixteen output fields, the literal scalar identity and both coefficient-coordinate statements are proved; the second holds for every original coefficient basis. Generic division and tensor-factor arguments add no continuity or Noetherian premise. WIS18 and IFD25 now discharge the two other period-ring inputs isolated by WLD26, so no period-ring supplier remains in this original conditional WachEx theorem. The original LocTied/IsStd and Bhatt-Scholze crystalline-realization inputs remain its hypotheses. Next are FaithH, EtBasis, Herr class maps and quantitative de Rham comparison for full HW/Fon/Cmp. Then every original local row/table bound must hold in one common ConclF family, retaining ShaFinOdd, exceptional sets, vvTerm summability and uniform thresholds. No additional outer-layer transition-system hypothesis is introduced. SSC, DFD12 and DNE remain available, with DNE K=2000(|Ca|+1)^3 fixed before the family. Whole GLOBAL_DENOMINATOR remains open.')
geometry=(
 'PBC supplies full arbitrary-base RelAmpleOfLocallyOnBase and literal PolBaseChangeSt, including the actual Cartesian square, unchanged dimension, actual pulled line bundle, generated comparison, rigidification, symmetry, all-test group multiplication and all-affine-test KTriv. The finite determinant trick, extra-section affineness and two-exponent section extension give the synchronized positive-power glue_pack and exists_sv without a Noetherian or flatness restriction on base change. PBC26 now supplies full polAV_veryAmpleBy on every original affine test and specified Cartesian model; its power may depend on that test. PBC27 derives the finite-relation property from Perf over any field and proves original sections_finite_of_perf and every-integer-power SecM finiteness over the original algebraically closed field. Its separate arbitrary-field finite_secM implication retains the supplied finite-relation premise. GSL_POL_BASE_CHANGE is supplied, alongside the already complete GSL_SERRE and ASL Perf inputs. Remaining for GSL17 are multiplication-pullback generated comparison, finite/flat/surjective and etale multiplication geometry, and invariant-function descent on every relevant open. Geometric integrality, principal rank one, torsion-indexed section decomposition, two-sided growth, and square/translation generators remain for full P,V,R,T and the GSL26/NFL joins; section finiteness alone does not supply the growth half of GSL_FINITE_GROWTH. Original Moduli and HUF/PUN foundations remain. Later finite-level systems, Gaussian/reproduction, simultaneous dictionaries, ramified jets, all-tuple class sums, phase-sensitive uniqueness, common PointIdentCore and base ClassSumsSpan remain, retaining both levels, whole fields, Fits and eta agreement.')
arithmetic=(
 'APD supplies the full original local presentation pres for every supplied local object at both ranks: an O-prime power-series surjection onto the actual R with N variables and N-prime listed generators of its kernel, with N=N-prime+n*F.d+1. It constructs the broad point_loc, ext_A and def_iso/actual NRep.Univ using finite quotients of finitely generated graded Laurent vertex algebras and compact coefficient recovery. It proves actual small-extension obstruction and tangent maps, both normalization corrections, the weight-torus contribution to the tangent and invariant-space count, and the full cyclotomic-dual vanishing calculation; the original finite-module Euler field then gives the exact tangent excess. Neither F.Big nor a nontriangularity hypothesis is added to pres, and Host ell=3 remains allowed. The earlier ALC completion, LocFlat/LocRho and local charts over the coefficient maximal ideal remain complete. Remaining are c1ch with full ClComp/ClChain, triangular and coincident-character dimension suppliers, sharp2/sharp3, the distinct rank-three EPres data, nice-prime properties, closed-point density and seed incidence, full rank-two propagation, the rank-two-to-three corner and exceptional ideal, rank-three propagation and OffFin. Existence of originally supplied universal spaces, actual automorphic seeds, patching/modularity, classicality and stronger Alt WitA/WitAQ outputs remain separate. Preserve the common marked frame, original arithmetic P, rank-specific rings and ideals, all coefficient maps and both actual O-prime extensions. No upstream FinA conclusion is used.')
analytic=(
 'RCV supplies the full original reference unipotent CovolRef, on every supplied HidaSetting and bridge/HypX with both actual domains and independent reference and lattice words. It proves the exact trace Gram determinant for the original complement lattice, all four block covolumes, localized finite-level K2 membership without a character-identity premise, the full rational/lattice/fiber dictionary, triangular group multiplication and every-domain coordinate covolume. The literal Euclidean Lie volume contributes 2^(r^2+r*k); the exponential chart has determinant one. Independent-word FrameRow gives the exact determinant (Tw(w)/Tw(u))^r, and the product reference box has mass Tw(w)^(-r*d)*2^(d*(r*k+r^2)). Cancellation leaves the original discriminant exponent, with every mass finite and positive before cancellation. The reference covolume/discriminant producer is no longer open. Next are broad JacGauge and the original PlaceSplit/ProdExact consumers at every supplied factorization and section, giving RealBracket on the unchanged measures. SVW conditional VolStabFromSWS and actual InVolumes remain complete at their original SWa1 and StabilizerFirstChernCompatibility premises; those premises themselves, finite-place factors and other mass/index/column/form/counting fields remain. BQS full BesselNVGap is available; Forms0, all-family Witt/genus/level/intertwiner Transport/LevelMatch, Bessel uniqueness, AutTie/RowDictTie/LabTie, simultaneous arithmetic cylinder counts and normalized GLOBAL_SPECTRAL remain.')
replacements={old['selected_node_progress']['GLOBAL_DENOMINATOR']['remaining']:period,
 old['selected_node_progress']['DESIGN_CHOICES_COMMON']['remaining']:geometry,
 old['selected_node_progress']['AUT_UNRAM_COEF']['remaining']:arithmetic,
 old['selected_node_progress']['GLOBAL_SPECTRAL']['remaining']:analytic}
def replace(x):
 if isinstance(x,str):
  for before,after in sorted(replacements.items(),key=lambda item:len(item[0]),reverse=True):
   x=x.replace(before,after)
  return x
 if isinstance(x,list):return [replace(v) for v in x]
 if isinstance(x,dict):return {k:replace(v) for k,v in x.items()}
 return x
cfg=replace(old)
cfg.update(artifact_version='0.56',date='2026-11-24',
 title='Polarized base change, arithmetic presentations, reference covolumes and the Wach prism',
 components=components,
 component_authors=dict(zip(components,['geometry_alltest','arithmetic_common_frame','bessel_nonvanishing','root'])),
 closed_selected_leaves={},closure_reviews={})
cfg['closed_nested_producers']=[
 'Full original two-exponent Sc.extend, finite-module determinant trick and extra_section',
 'Full original glue_pack, exists_sv and arbitrary-base relAmple_of_locally',
 'Full original relAmple_pull when the base-map image lies in one affine open, and all-affine-test kTriv_pull',
 'Full original PolBaseChangeSt and actual polAV_veryAmpleBy',
 'Finite-relation property from Perf over any field; original sections_finite_of_perf and every-integer-power SecM finiteness over the original algebraically closed field; arbitrary-field finite_secM implication with its finite-relation premise',
 'Full original broad point_loc, ext_A and def_iso/actual NRep.Univ',
 'Full original minimal-presentation obstruction algebra and actual HasObs',
 'Full original tangent-surjectivity, weight-torus contribution to the tangent and invariant-space count, pr_dual and Euler/count excess',
 'Full original HasObs.pres with N=N-prime+n*F.d+1 at both ranks',
 'Full original TrDetUnimod, RowBlockCovol and BlockCovol',
 'Full original unipotent_conj_mem_level, NOratC, Dict and FibQ/FibOnto/NOfib',
 'Full original KapLaw, CoordCovol, CoordHaar and CovolN with every Haar/domain',
 'Full original Lie ConstStep/ShearStep/ExpChart, broad reference measure and independent-word FrameRow/RefNBox',
 'Full original CovolRef with its exact discriminant and all original witnesses',
 'Full original generic action, distinguished division, tensor factor and separated-coordinate theorems',
 'Full original Wach-prism existence with all sixteen output fields and both coordinate assertions',
 'Full original BS plus LocTied implies WachEx for every original layer and supplied etale module']
cfg['status']=(f'Partial human reconstruction of RH and unrestricted Dirichlet GRH, accepting the pinned formal proof as correct. Version 0.56 continues the detailed proof-note approach with {new_count} independently reviewed numbered claims, bringing the inventory to {3538+new_count}. It completes full arbitrary-base polarized pullback and actual section finiteness, the original arithmetic local presentation with its exact variable/relation count, the full reference unipotent covolume/discriminant calculation, and the prescribed Wach prism with the full original conditional Wach-existence return. No additional whole selected obligation is closed: 24 remain, comprising 17 class C and 7 class B, with 17 shared RH/GRH and 7 additional unrestricted Dirichlet-GRH obligations. Multiplication/invariant descent/rank/growth/square inputs, component chains/dimensions/seeds/propagation and automorphic producers, faithful invariants/etale bases/Herr/quantitative comparison, and JacGauge/RealBracket/finite-place/transport/counting/spectral producers remain. GLOBAL_LOCAL_GAIN remains fully closed from v0.49. Counts are inventories, not completion percentages. No Lean replay or PDF is claimed.')
cfg['local_conclusions']=[
 'PBC1–PBC27 prove full arbitrary-base polarized pullback. Two section-extension exponents separate local denominators from overlap compatibility. A finite determinant trick preserves affineness after an extra section is adjoined, and synchronized positive powers give the exact ratio-surjectivity needed by relative ampleness. The literal pulled group and line bundle retain all tests, including KTriv via the canonical iterated-fiber-product isomorphism. The original very-ample producer follows. Over the original algebraically closed field, a finite Perf coordinate space also gives actual section finiteness and every integer-power SecM finiteness; two-sided growth remains separate.',
 'APD1–APD25 prove full original pres on the actual local coefficient object in both ranks. Finite Laurent vertex quotients and compactness recover the broad point-realization and universality map without evaluating arbitrary completed Laurent series. Actual small-extension cocycles, normalization corrections and cone cohomology supply the obstruction and tangent maps. The nonzero weight matrix gives either a nonzero kernel vector for the tangent-to-cohomology map or a nonzero invariant in H0. Both cases give h1+1 at most dim(T)+h0, and the original Euler field gives dim(T)-dim(H2) at least n*F.d+1. Minimal-presentation algebra, with harmless zero padding of relations, yields the exact N=N-prime+n*F.d+1. Component-chain and sharp dimension results remain separate.',
 'RCV1–RCV25 prove the full original CovolRef. Trace-dual indices and the integral trace-one splitting compute every row, ideal and imaginary diagonal block. The actual finite-level subgroup is identified by localizing at one integer coprime to g, then descending the congruences. Triangular multiplication gives every-domain covolume. The prescribed Lie metric and exponential shear fix the reference measure exactly. Its independent-word box mass cancels the word and powers-of-two factors, leaving the required discriminant power for both actual HypX domains. JacGauge and RealBracket remain downstream.',
 'WPR1–WPR30 construct the actual W0[[T]] prism with its cyclotomic ideal, all bounded-prism fields, exact Fontaine/Frobenius/Galois maps, literal scalar identity and both unique-coordinate statements. A tail contraction proves distinguished division without continuity, and a normalized linear retraction descends the tensor map using separation alone. Unit-separated embeddings give an explicit invertible tensor coordinate map, preserving every coefficient basis. WIS18 and IFD25 then supply the two other inputs of WLD26, proving the full original BS plus LocTied implication to WachEx. Later FaithH/EtBasis/Herr/Cmp and the common family remain explicit.']
additions={
 'GLOBAL_DENOMINATOR':'WPR1–WPR30 (full prescribed prism and original BS plus LocTied implies WachEx; no period-ring supplier left)',
 'AUT_UNRAM_COEF':'APD1–APD25 (full broad point/universal maps, actual obstruction and tangent construction, exact original pres)',
 'GLOBAL_SPECTRAL':'RCV1–RCV25 (full original reference unipotent CovolRef with exact discriminant and independent words)',
 'DESIGN_CHOICES_COMMON':'PBC1–PBC27 (full arbitrary-base polarized pullback, actual very-ampleness and section finiteness)',
 'BASE_THETA_READINGS':'PBC1–PBC27 (full arbitrary-base polarized pullback, actual very-ampleness and section finiteness)',
 'BASE_THETA_RATIONAL_TESTS':'PBC1–PBC27 (full arbitrary-base polarized pullback, actual very-ampleness and section finiteness)',
 'TASK_COUNT_V_INSTALL':'APD full original presentation on the same arithmetic local objects; sharp chains/seeds/propagation retained',
 'LOCAL_NBUILT_COMMON':'PBC full polarized pullback; APD exact actual presentation; RCV reference covolume; WPR original conditional WachEx',
 'SECOND_LAYER_COMPATIBLE_SELECTION':'PBC/APD/RCV/WPR full named original producers on unchanged actual objects'}
for k,v in additions.items():cfg['selected_node_progress'][k]['completed'].insert(0,v)
cfg['publication_note']=f'All {new_count} new numbered claims are human class-B deductions at their explicitly stated original scopes. The original BS and LocTied hypotheses remain in the completed WachEx implication. Neither a complete human RH/GRH proof nor a new formal replay is asserted.'
cfg['validation_scope_updates'].update({
 'full_original_arbitrary_base_RelAmpleOfLocallyOnBase_complete':True,
 'full_original_PolBaseChangeSt_and_polAV_veryAmpleBy_complete':True,
 'full_original_sections_finite_of_perf_and_all_integer_power_SecM_finiteness_complete':True,
 'PolBaseChange_multiplication_invariant_descent_integrality_rank_square_inputs_remain':False,
 'multiplication_invariant_descent_integrality_rank_growth_square_inputs_remain':True,
 'superseded_v55_PolBaseChange_remaining_flag_explanation':'PBC25 supplies GSL_POL_BASE_CHANGE; PBC26 supplies the original very-ample producer. Multiplication, invariant descent, rank, two-sided growth and square inputs remain.',
 'full_original_point_loc_ext_A_def_iso_and_NRep_Univ_complete':True,
 'full_original_HasObs_and_pres_exact_variable_relation_count_complete':True,
 'component_chains_sharp_dimensions_EPres_seed_propagation_OffFin_remain':True,
 'full_original_CovolRef_all_words_domains_and_reference_measures_complete':True,
 'full_original_reference_Lie_normalization_and_FrameRow_complete':True,
 'JacGauge_PlaceSplit_ProdExact_RealBracket_remain':True,
 'reference_unipotent_covolume_discriminant_supplier_remains':False,
 'full_original_Wach_prism_all_sixteen_fields_complete':True,
 'full_original_conditional_WachEx_complete':True,
 'one_exact_period_ring_supplier_before_conditional_WachEx_remains_explicit':False,
 'remaining_period_ring_suppliers_before_original_conditional_WachEx':0,
 'superseded_v55_one_period_supplier_explanation':'WPR29 supplies the actual prism; WPR30 returns the full original WachEx implication with its original BS and LocTied hypotheses.',
 'FaithH_EtBasis_Herr_quantitative_comparison_common_ConclF_remain':True,
 'original_LocTied_IsStd_and_Bhatt_Scholze_inputs_retained':True,
 'all_layer_WachEx_claimed_unconditional':False,
 'GLOBAL_LOCAL_GAIN_full_v49_closure_preserved':True,
 'no_new_whole_selected_obligation_closed':True})
(ROOT/'increment_v0_56.json').write_text(json.dumps(cfg,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'new_claims':new_count,'total':3538+new_count,'whole_obligations_open':24},indent=2))
