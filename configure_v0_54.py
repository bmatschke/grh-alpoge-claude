#!/usr/bin/env python3
"""Describe v54 by its exact original producers and remaining consumer inputs."""
from pathlib import Path
import copy, json

ROOT = Path(__file__).resolve().parent
old = json.loads((ROOT / 'increment_v0_53.json').read_text())
components = ['actual_section_localization_v54', 'rank_two_connectedness_v54',
              'archimedean_orbital_scalar_v54', 'wach_inclusion_saturation_v54']
authors = ['geometry_alltest', 'arithmetic_common_frame', 'bessel_nonvanishing', 'root']
counts = [len(json.loads((ROOT / c / 'provenance.json').read_text())['claims']) for c in components]
n = sum(counts)
total = 3361 + n

geometry = (
 'ASL supplies the full original actual twisted-section power-killing and extension theorems, graded localization and dehomogenization, and all-vertex section-cube comparison. '
 'Affine line-bundle sections are finite projective over arbitrary rings and the actual chart algebras are smooth and flat. '
 'Joining these with FCD18 and GSL8–10 supplies the full original universal Perf producer, nonempty_perf_of_smooth_isProjBy, on the given scheme and line bundle over arbitrary R. '
 'One Noetherian model, one finite-projective complex and the actual section comparison precede every later coefficient algebra and pullback square. Do not reopen the algebraic or actual geometric perfect-complex model. '
 'The separate PolBaseChangeSt, Serre H1 with its all-cover conclusion, multiplication/invariant descent, geometric integrality, principal rank one, torsion section decomposition/growth and theorem-of-square generators remain. '
 'The next bounded geometry packet is the full original Serre H1 theorem: one finite homogeneous submodule for all degrees, a uniform large-degree Cech bound, and the reverse chosen-cover-to-all-cover argument. '
 'Supply the independent P,V,R,T producers before the relevant GSL26/NFL joins. Original Moduli and HUF/PUN foundations remain. '
 'Later finite-level systems, Gaussian/reproduction, simultaneous dictionaries, ramified jets, all-tuple class sums, phase-sensitive uniqueness, common PointIdentCore and base ClassSumsSpan remain, retaining both levels, whole fields, Fits and eta agreement.'
)
arithmetic = (
 'RTC supplies full original wpres/co_B/gr_A/cont_u upstream for both ranks two and three, without FinA. '
 'Formal-unit twists separate integral weights over nilpotent test rings; finite monomial decompositions and fixed-weight filtration cofinality identify the actual entry and graded coefficient rings. '
 'It supplies the complete rank-two arbitrary-k-algebra triangular point correspondence, the original smooth/nonzero strict-cocycle producers, and full preconnected_rank_two. '
 'It also supplies full original FinPtDown at arbitrary rank and all allowed primes, and the exact ACP11-to-FinPtDown-to-AFE20 return. '
 'Remaining are actual loc_cpl and LocFlat/LocRho charts, sharp component and dimension bounds, density/seed incidence, complete rank-two propagation, the rank-two-to-three corner and exceptional ideal, rank-three propagation and OffFin. '
 'Actual automorphic seeds, patching/modularity, classicality and the stronger Alt WitA/WitAQ outputs also remain. '
 'Keep rank-two and rank-three rings/ideals separate on the same AFE marked frame, with original P where used. '
 'ACP abstract propagation and FinPtOf are complete; completed generic gr_A must replace the former opaque upstream input, while loc_cpl and actual flatness are not inferred from it. '
 'The broad IsBar realization is proved directly; ACP’s diagonal IsLiftA shortcut is not silently enlarged. Host ell=3 and the original coefficient descent stay in scope.'
)
analytic = (
 'AOS supplies full original PlaceJac, universal GaugeDens, GaugeVolU, HinfCompact, PushInf and ConstTest with the literal gaugeU*volU(k)^d*Tw^(-kd) scalar. '
 'It also supplies ExInf, HtotInf, WeilInf, AinfValue/AinfClause, GinfTest and AprimeInf at every original witness and section, preserving the supplied bridge and all infinity measures. '
 'The prior GMR full RescaleStep3 and continuous Gram-fiber measures are reused; its one standard character remains fixed before all words, places and tuples. '
 'The immediate remaining RealBracket producers are the actual reference unipotent covolume/discriminant exponent, broad JacGauge/PlaceSplit and ProdExact. '
 'An independent next packet is full VolStabFromSWS and InVolumesAt from the exact original Siegel–Weil/compatibility premises, using one common admissible positive test and the same measures for unfolding and scalar cancellation. '
 'Arithmetic theta/quotient-volume equalities and finite-place factors are not supplied by the archimedean scalar. '
 'BQS already gives full BesselNVGap. Forms0, all-family Witt/genus/level/intertwiner Transport/LevelMatch, Bessel uniqueness, AutTie/RowDictTie/LabTie, simultaneous arithmetic cylinder counts and the normalized GLOBAL_SPECTRAL estimate remain.'
)
denominator = (
 'WIS supplies the full original four-clause ioE_injective_saturated_inter: actual injectivity, unit reflection, prime saturation and exact integral intersection. '
 'A finite multiplication determinant proves the needed Jacobson property without assuming stronger unused parameter-adic completeness. '
 'It also supplies full original padic_closed, fixed-subring prime-adic completeness, fixed lifts modulo p for arbitrary H, tilt parameter-separatedness/completeness, nearPi_sep_complete and fixSub_nearPi_complete. '
 'WLD26 now retains exactly two period-ring suppliers before full WachEx: the actual Wach prism and the remaining homogeneous cyclotomic-kernel-fixed Frobenius matrix descent. '
 'The latter still needs Frobenius-filtration, actual invariant approximation, near-closedness with const_dvd and matrix lifting; completed WIS inputs must be reused. '
 'Original LocTied/IsStd and Bhatt–Scholze realization premises remain explicit. Full all-layer WachEx is not yet unconditional. '
 'FaithH, EtBasis, Herr class maps and quantitative comparison remain for the complete HW/Fon/Cmp triple. No extra outer-layer transition system is introduced. '
 'Then every original local row/table bound must hold on one common ConclF family, retaining ShaFinOdd, exceptional sets, vvTerm summability and uniform thresholds. '
 'SSC, DFD12 and DNE remain available; DNE fixes K=2000(|Ca|+1)^3 before the family. Whole GLOBAL_DENOMINATOR remains open.'
)
rows, global_inputs, extra = old['remaining_major_inputs'][4:7]
local = [
 'ASL1–ASL21 complete the original actual smooth-projective perfect-complex producer. On a qcqs scheme a section which vanishes on a section’s nonvanishing locus is killed by one common power, and a section on that locus extends after one common power. Finite covers and a second common power kill the overlap discrepancies. These constructions preserve all integer twists and actual transition functions. They prove graded-section localization and every restriction in the section cube. Explicit extended local generators and duals give a finite dual basis for affine line-bundle sections; the actual chart algebra is smooth and flat. FCD’s one Noetherian model and the previously proved finite-projective-complex assembly then yield the full original Perf record over arbitrary R, with one comparison before all base changes. Independent polarization, all-cover H1, rank and square-law suppliers remain.',
 'RTC1–RTC25 complete the original rank-two preconnected core and coefficient descent. A formal diagonal-unit twist separates every integral weight over nilpotent rings, producing the genuine homogeneous presentation of the universal entry ring. Dickson’s lemma and fixed-weight filtrations give the original coefficient-ring and grading statements for ranks two and three before any FinA conclusion. Formal-variable deformations realize the rank-two triangular points from arbitrary coefficient-valued strict cocycles, evaluating only their polynomial part. A polynomial family gives every core point and one fixed nonzero cocycle a common generic prime inside the core; these three-point irreducible sets prove the complete original preconnected_rank_two. Other specializations may leave the core and are not used. The equal-characteristic coefficient-section construction gives full FinPtDown at arbitrary rank, and its original return to FinEnd. Local charts/flatness, dimension/seed incidence, complete rank-specific propagation, OffFin and automorphic producers remain separate.',
 'AOS1–AOS18 compute the exact archimedean orbital measure. The source pairings give tuple density 2^(nad) and Frobenius volume on Hermitian matrices. The block differential has absolute determinant 2^(-na)|det T|^k, so its fiber density is |det T|^k. The literal small-exponential-ball gauge is the density of the prescribed Haar measure relative to Frobenius volume. The last-column fibration of U(j) gives volU(k)=product_{j=1}^k (2*pi)^j/(j-1)!. Dividing orbit density by fiber density and multiplying over real places proves full PushInf, with no unspecified scalar. Compact-stabilizer unfolding proves the complete all-witness/all-section integration clause and uniqueness of its scalar. Original infinity measures and the bridge are preserved; RealBracket and arithmetic/finite-place volume identities remain.',
 'WIS1–WIS26 complete the actual Wach coefficient inclusion and its first invariant-completeness suppliers. In each power-series component, the first coefficient not divisible by the uniformizer determines a unit times a power of the parameter. The parameter lies in the Jacobson radical of the integral Witt tensor ring by a finite determinant argument. This forces divisibility reflection, then actual injectivity and unit reflection; successive integral digits and p-adic completeness give exact intersection. Witt zero-coordinate formulas give saturated fixed subrings, fixed lifts modulo p and explicit tilt/near-parameter sums for arbitrary sets of automorphisms. The full generic lattice construction therefore retains two period-ring suppliers rather than three. The actual prism and the remaining fixed Frobenius-matrix descent, and subsequently HW/Fon/Cmp and the common ConclF family, remain explicit.'
]
status = (
 f'Partial human reconstruction of RH and unrestricted Dirichlet GRH, accepting the pinned formal proof as correct. Version 0.54 continues the detailed proof-note approach with {n} independently reviewed numbered claims, bringing the inventory to {total}. '
 'It completes the original actual smooth-projective perfect-complex producer, rank-two preconnected core and coefficient descent, exact archimedean orbital/integration scalar, and full four-clause Wach coefficient inclusion with invariant-completeness inputs. '
 'No additional whole selected obligation is closed: 24 remain, comprising 17 class C and 7 class B, with 17 shared RH/GRH and 7 additional unrestricted Dirichlet-GRH obligations. '
 'The separate geometric H1/polarization/rank/square inputs, rank-specific local geometry and automorphic producers, two period-ring suppliers and later Wach comparison, and global volume/transport/counting/spectral producers remain. '
 'GLOBAL_LOCAL_GAIN remains fully closed from v0.49. Counts are inventories, not completion percentages. No Lean replay or PDF is claimed.'
)
progress = copy.deepcopy(old['selected_node_progress'])
def setp(key, first, remaining):
    prior = progress.get(key, {'completed': []})
    progress[key] = {'completed': first + prior['completed'], 'remaining': remaining}
setp('GLOBAL_DENOMINATOR', ['WIS1–WIS26 (full four-clause actual inclusion and fixed/near-parameter completeness; exact two-supplier Wach return)'], denominator)
setp('AUT_UNRAM_COEF', ['RTC1–RTC25 (upstream universal coefficient rings, full preconnected_rank_two and FinPtDown)'], arithmetic)
setp('GLOBAL_SPECTRAL', ['AOS1–AOS18 (full exact archimedean orbital scalar, gauge, compact volume and all-section integration clause)'], analytic)
for key in ['DESIGN_CHOICES_COMMON', 'BASE_THETA_READINGS', 'BASE_THETA_RATIONAL_TESTS']:
    setp(key, ['ASL1–ASL21 (actual section localization and full original arbitrary-base Perf producer)'], geometry + (' ' + rows if key == 'BASE_THETA_READINGS' else ''))
setp('TASK_COUNT_V_INSTALL', ['RTC full rank-two preconnected core and coefficient descent; actual propagation/counting inputs retained'], arithmetic + ' ' + rows)
setp('LOCAL_NBUILT_COMMON', ['ASL full actual perfect-complex model; RTC common-frame arithmetic inputs; AOS exact unchanged infinity normalization'], global_inputs + ' ' + geometry)
setp('SECOND_LAYER_COMPATIBLE_SELECTION', ['WIS actual inclusion and invariant completeness; AOS exact scalar; ASL/RTC full named nested producers'], global_inputs)

cfg = {
 'artifact_version': '0.54', 'date': '2026-11-23', 'source_commit': old['source_commit'],
 'title': 'Actual sections, connected cores, exact orbital measures and Wach inclusions',
 'components': components, 'component_authors': dict(zip(components, authors)),
 'closed_selected_leaves': {}, 'closure_reviews': {},
 'closed_nested_producers': [
  'Full original qcqs twisted-section power-killing and extension, for all integer twists',
  'Full original actual graded localization, dehomogenization and all-vertex section-cube comparison',
  'Full original affine line-bundle section projectivity and actual chart smoothness/flatness',
  'Full original nonempty_perf_of_smooth_isProjBy, arbitrary-base universal Perf',
  'Full upstream original wpres/co_B/gr_A/cont_u in ranks two and three without FinA',
  'Full original rank-two arbitrary-coefficient triangular point correspondence and strict-cocycle suppliers',
  'Full original preconnected_rank_two',
  'Full original FinPtDown at arbitrary rank and exact same-frame return to FinEnd',
  'Full original PlaceJac, universal GaugeDens and GaugeVolU with exact normalization',
  'Full original HinfCompact, PushInf and ConstTest for every original witness',
  'Full original ExInf, HtotInf, WeilInf, AinfValue/AinfClause, GinfTest and AprimeInf',
  'Full original four-clause ioE_injective_saturated_inter',
  'Full original padic_closed, fixed-subring completeness and fixed lifts modulo p',
  'Full original tilt separatedness/completeness, nearPi_sep_complete and fixSub_nearPi_complete',
  'Conditional full WachEx reduced to two exact period-ring suppliers, retaining original LocTied/IsStd and realization inputs'
 ],
 'status': status, 'local_conclusions': local,
 'remaining_major_inputs': [analytic, geometry, arithmetic, denominator, rows, global_inputs, extra],
 'next_targets': [geometry, arithmetic, denominator, analytic, rows, global_inputs, extra],
 'selected_node_progress': progress, 'updated_contracts': {}, 'published_applications': [],
 'publication_note': f'All {n} new numbered claims are written class-B deductions at their explicitly stated original scopes. Standard foundations and originally supplied data are separately recorded. Conditional outputs retain every original antecedent. No whole RH/GRH human proof or new formal replay is asserted.',
 'validation_scope_updates': {
  'full_original_actual_section_localization_and_cube_comparison_complete': True,
  'full_original_arbitrary_base_smooth_projective_Perf_complete': True,
  'actual_section_localization_gluing_and_affine_geometric_suppliers_remain_explicit': False,
  'actual_geometric_section_model_PolBaseChange_Serre_integrality_rank_square_suppliers_remain_explicit': False,
  'independent_PolBaseChange_Serre_all_cover_H1_integrality_rank_square_inputs_remain': True,
  'superseded_v53_actual_geometric_model_flag_explanation': 'The actual smooth-projective Perf producer is now complete; independent polarization, H1, rank and square suppliers remain.',
  'full_original_upstream_wpres_co_B_gr_A_cont_u_complete_without_FinA': True,
  'full_original_preconnected_rank_two_complete': True,
  'full_original_FinPtDown_complete_at_all_original_ranks_and_primes': True,
  'actual_LocFlat_LocRho_dimension_seed_propagation_OffFin_automorphic_inputs_remain': True,
  'full_original_PlaceJac_GaugeDens_GaugeVolU_complete': True,
  'full_original_PushInf_ConstTest_exact_scalar_complete': True,
  'full_original_ExInf_HtotInf_WeilInf_AinfValue_AprimeInf_complete': True,
  'all_original_selfdual_fiber_witnesses_and_all_sections_preserved': True,
  'original_setting_bridge_and_infinity_measures_preserved': True,
  'RealBracket_arithmetic_quotient_volumes_finite_place_and_transport_counting_remain': True,
  'full_original_four_clause_actual_Wach_inclusion_complete': True,
  'full_original_padic_fixed_subring_tilt_and_NearPi_completeness_inputs_complete': True,
  'two_exact_period_ring_suppliers_before_full_WachEx_remain_explicit': True,
  'three_exact_period_ring_suppliers_before_full_WachEx_remain_explicit': False,
  'superseded_v53_three_period_suppliers_explanation': 'Actual ioE injectivity and unit reflection are supplied by WIS18; the actual prism and remaining fixed Frobenius matrix descent remain.',
  'original_LocTied_IsStd_and_Bhatt_Scholze_inputs_retained': True,
  'all_layer_WachEx_claimed_unconditional': False,
  'coherent_Wach_HW_Fon_Cmp_and_common_ConclF_remain_explicit': True,
  'GLOBAL_LOCAL_GAIN_full_v49_closure_preserved': True,
  'no_new_whole_selected_obligation_closed': True
 }
}
(ROOT / 'increment_v0_54.json').write_text(json.dumps(cfg, ensure_ascii=False, indent=2) + '\n')
print(json.dumps({'components': dict(zip(components, counts)), 'new_claims': n, 'cumulative_claims': total}))
