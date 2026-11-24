#!/usr/bin/env python3
"""Reproduce the TG source ledger from immutable Lean bytes, without a build.

This script checks the supplied-data reconstruction's source provenance. It
does not formalize or kernel-check the shorter human proofs in main.tex.
"""
from pathlib import Path
import argparse
import hashlib
import json
import re
import subprocess

HERE = Path(__file__).resolve().parent
PIN = '7cbf7a0c32fca1badf05931879a37c3f8a2b03b4'
URL = 'https://github.com/CocoSgt/riemann-hypothesis-lean'
ap = argparse.ArgumentParser()
ap.add_argument('--repo', type=Path, default=HERE.parents[1] / 'lean-source')
args = ap.parse_args()
repo = args.repo.resolve()
assert subprocess.check_output(['git', '-C', str(repo), 'rev-parse', 'HEAD'], text=True).strip() == PIN

D = 'src/Development/AbelianVarietyTheory/'
I = D + 'Proofs/IwasawaDecomposition/'
A = D + 'Definitions/AutomorphicMembership/'
F = 'src/Formalism/LocalToGlobal/'
C = F + 'Columns/'
HF = F + 'HermitianForms/'
G = F + 'GroupLattices/'


def digest(raw):
    return hashlib.sha256(raw).hexdigest()


decl_re = re.compile(r'^(?:@\[[^\n]*\]\s*)?(?:(?:private|protected|noncomputable|unsafe)\s+)*'
                     r'(theorem|lemma|def|abbrev|structure|class|inductive)\s+([^\s:({]+)')
boundary_re = re.compile(r'^(?:@\[[^\n]*\]\s*)?(?:(?:private|protected|noncomputable|unsafe)\s+)*'
                         r'(?:theorem|lemma|def|abbrev|structure|class|inductive|namespace|section|end|'
                         r'variable|attribute|set_option|open|include|instance|example)\b')
files = {}
cache = {}


def read_source(path):
    if path in cache:
        return cache[path]
    blob = subprocess.check_output(['git', '-C', str(repo), 'show', f'{PIN}:{path}'])
    present = (repo / path).exists()
    if present:
        assert (repo / path).read_bytes() == blob, ('worktree differs from pin', path)
    lines = blob.splitlines(keepends=True)
    decoded = [line.decode('utf-8').rstrip('\r\n') for line in lines]
    frames, decls = [], []
    for n, line in enumerate(decoded):
        ns = re.match(r'^namespace\s+(\S+)', line)
        sec = re.match(r'^(?:noncomputable\s+)?section(?:\s+(\S+))?\s*$', line)
        end = re.match(r'^end(?:\s+(\S+))?\s*$', line)
        if ns:
            frames.append(('namespace', ns.group(1)))
        elif sec:
            frames.append(('section', sec.group(1)))
        elif end:
            assert frames, ('unmatched top-level end', path, n + 1)
            kind, name = frames.pop()
            if end.group(1):
                assert name == end.group(1), ('namespace/section close mismatch', path, n + 1, name, end.group(1))
        match = decl_re.match(line)
        if match:
            spelling = match.group(2)
            namespace = '.'.join(name for kind, name in frames if kind == 'namespace')
            if spelling.startswith('_root_.'):
                qualified = spelling[len('_root_.'):]
            else:
                qualified = f'{namespace}.{spelling}' if namespace else spelling
            decls.append(dict(start=n, spelling=spelling, qualified=qualified, kind=match.group(1)))
    files[path] = dict(path=path, sha256=digest(blob), bytes=len(blob), line_count=len(lines),
                       verified_equal_to_pinned_git_blob=True, worktree_source_present=present,
                       worktree_bytes_compared_to_git_blob=present, url=f'{URL}/blob/{PIN}/{path}')
    cache[path] = (lines, decoded, decls)
    return cache[path]


def source(path, name, role='source_counterpart'):
    lines, decoded, decls = read_source(path)
    found = [d for d in decls if name in (d['spelling'], d['qualified'])]
    if not found:
        found = [d for d in decls if d['qualified'].endswith('.' + name)]
    assert len(found) == 1, (path, name, [d['qualified'] for d in found], [d['spelling'] for d in decls])
    d = found[0]
    start, stop = d['start'], len(lines)
    for n in range(start + 1, len(lines)):
        if boundary_re.match(decoded[n]):
            stop = n
            break
    while stop > start and not decoded[stop - 1].strip():
        stop -= 1
    raw = b''.join(lines[start:stop])
    assert raw and stop > start
    return dict(path=path, declaration=d['qualified'], source_spelling=d['spelling'],
                declaration_kind=d['kind'], line_start=start + 1, line_end=stop, role=role,
                sha256=files[path]['sha256'], full_file_sha256=files[path]['sha256'],
                range_sha256=digest(raw), range_bytes=len(raw), first_line=decoded[start],
                declaration_lines_within_range=[start + 1],
                url=f'{files[path]["url"]}#L{start + 1}-L{stop}',
                verified_equal_to_pinned_git_blob=True)


def ss(path, names, role='source_counterpart'):
    return [source(path, name, role) for name in names.split()]


HC = F + 'HermitianColumns/'
terminal = I + 'HermitianFormLastCoordinateUniformizerVectorSelf.lean'
common = [
    'The actual arithmetic host, CMData, rank parameters, prime sets, coefficient fields and embeddings are supplied; the coordinates and Hermitian dual convention are exactly those in SF2.',
    'The true column datum I:TC(B,X), its literal Ok and Pins, a Laws l, and Later(B,I.cols(l)) are supplied. The independent TL Ok-to-Laws implication can be applied outside this component; TG has no TL dependency.',
    'For each word, p=T_u is prime, pi*conjugate(pi)=p, selected primes have residue cardinality p and no conjugate pair, and auxiliary/twist prime disjointness and the prescribed residue/character laws are retained exactly.',
    'DR3 supplies every required initial full IsPtOf realizer. No independent realizability, rational SameGenus, full FormsTiedSym or CarT record is assumed as an input to the final TG12 construction.',
    'This is a human proof of the stated supplied-data conclusion, not a Lean kernel replay or a proof that the supplied arithmetic host or Later exists. No RH/GRH theorem is asserted by this component alone.'
]


def claim(i, title, statement, deps, assumptions, srcs, relation):
    return dict(id=i, title=title, status='derived_simplification', statement=statement,
        depends_on=deps, assumptions=common+assumptions,
        proof_location=dict(file='main.tex', anchors=[i]),
        expanded_notes=dict(file='report.txt', section=i),
        source_relation=relation,
        mathematical_status='proved_under_exact_declared_supplied_data_hypotheses',
        sources=srcs)


claims = [
    claim('TG1', 'Exact symmetric penultimate residue group',
        'At the actual penultimate step cOf(m-1)=0, the finite level group, under the prescribed residue-field transport, equals JSymG false/HSym with its exact exceptional zero block. Every allowed residue matrix is lifted to the actual flag group over the local integer ring.',
        ['FC13'],
        ['The actual sharp symmetric last_h/grpG laws of TC.Ok.idx_ok are used. The proof applies to the zero-extra-space penultimate stage, with the actual rank and auxiliary complete-splitting hypotheses.'],
        ss(HF+'DefsSym.lean','rSym posSym lvSym InJSym JSymG','literal_matrix_group_definitions')+
        ss(C+'FiniteSumNonzeroLargeDepth.lean','bd5 flagS bvecS JGsym','actual_flag_and_marked_vector_definitions')+
        ss(I+'SymmetricLevelBoundLe.lean','inJSym_of_mat inJSym_of_prX levG_le_JSymG','forward_inclusion_reconstructed')+
        ss(I+'SymmetricFlagBasisVectorEqSingleOfNoExtra.lean','mem_symmetricFlagLattice_iff_of_no_extra symmetricFlagBasisVector_eq_single_of_no_extra lv_flag mem_JGsym0 mem_levG_last','reverse_lift_and_actual_finite_group_reconstructed'),
        'Proves both inclusions by explicit flag cuts and marked vectors, including the special bd5 cut. Lifts only to GL_n(O_(P)); no global integral reduction-surjectivity claim.'),
    claim('TG2', 'The exact penultimate character and common symmetric level',
        'The actual finite character is lamSym with m-1 t-block determinants and the original-coordinate superdiagonal sum omitting (k-1,k). Together with FC12 this constructs exists_gLevH and stepBefore_oneLevel, with identity frame and the exact finite orbit/stabilizer carrier.',
        ['TG1','FC12','FC13','FC14'],
        ['The actual column character laws and coefficient embedding are retained. The global level character uses inverse finite reductions.'],
        ss(HF+'PsiZeroNontrivialCharacter.lean','lamJ','literal_character_formula')+
        ss(HF+'DefsSym.lean','lamSym','literal_symmetric_character')+
        ss(C+'FiniteSumNonzeroLargeDepth.lean','lamGBS','actual_local_flag_character')+
        ss(I+'ChrLast.lean','sum_sd red_mat lam_loc chr_last','exact_character_calculation_reconstructed')+
        ss(I+'ChartTiedTopLevelChain.lean','exists_gLevH stepBefore_oneLevel','actual_group_character_common_level_endpoints')+
        ss(HF+'DefsGH.lean','GLevH','literal_auxiliary_level_interface'),
        'Adds the specific HSym/lamSym content absent from the generic FC12/FC14 construction; retains the same J, frames and finite coset carrier.'),
    claim('TG3', 'Actual terminal row chart and its complete value/norm comparison',
        'Construct the reference row ReadsP and ClsPTied from DR3 with ST=Q=empty, prove its actual double-coset/stabilizer dictionary, then apply CV10 and FC7 to obtain the full clsP_tie and NormPTie with identity frame-function map.',
        ['DR3','AD4','LP1','NB1','CV10','FC7'],
        ['The row has the actual rowTyG auxiliary level, empty type-prime set and empty reference twist-frame set. Its standard base lattice is O_E^n and its class N is self-dual.'],
        ss(A+'LatAtLattice.lean','ReadsP','literal_row_chart_reading_interface')+
        ss(I+'UfGLRatHom.lean','stp lev L_empty Lsh_empty exists_cls','actual_row_level_and_class_constructor_reconstructed')+
        ss(C+'RowForms.lean','rowTyG','actual_row_auxiliary_level')+
        ss(I+'ExistsEmbFIff.lean','natW_shW VV_shW delStd_shW petersson_apply clsP_tie','actual_terminal_value_norm_endpoint_with_weight_precision')+
        ss(HF+'LastCoordinateUniformizerVectorSpansOrthogonalLi.lean','ClsPTied ValPTied','literal_terminal_row_class_value_records')+
        ss(HF+'FormsTied.lean','NormPTie','literal_row_norm_interface'),
        'The initial realizer is constructed by DR3; the converse double-quotient surjectivity uses local unitary self-duality and global intersection. CV10 supplies exact integral Delta membership, never Delta=dual-Weyl.'),
    claim('TG4', 'Terminal full/row symmetric levels and compatible frames',
        'The terminal full and row groups are respectively JSymG true and false, both with lamSym using m blocks. Construct their GLevH with row frame I and full last-diagonal pi frame, and verify both FrExtFr equations at every auxiliary place.',
        ['TG1','TG3','FC1','FC13','FC14','SF2'],
        ['The source full terminal group is the row parabolic extended by a final singleton block with fixed last column. The original pi is a unit at auxiliary places.'],
        ss(C+'LevGSym.lean','HJsym HXmsym lamJsym lamXmsym','literal_row_and_full_finite_groups')+
        ss(A+'CongruenceLevelEqDepthSucc.lean','levGTop levGTop_PsymF','actual_terminal_group_definition')+
        ss(I+'CoarseLast.lean','inJ_of_mem mem_of_inJ memX','full_group_matrix_equivalence_reconstructed')+
        ss(I+'MemHJsymIffJSymG.lean','mem_HJsym_iff_JSymG','row_group_matrix_equivalence_reconstructed')+
        ss(I+'LamJsymRead.lean','sum_skip coarse_iff lamJsym_read','exact_character_reading_reconstructed')+
        ss(I+'LevelsTopRowSym.lean','rdM rdP cmp_base exists_nat main_base frExt_of levels_top_row_sym','actual_full_row_levels_and_frame_endpoint')+
        ss(HF+'TiedSym.lean','FrExtFr HSym','literal_frame_extension_and_group_interface'),
        'Identifies both finite groups in both directions and the exact character; constructs the frames explicitly rather than inferring them from an isomorphic lattice.'),
    claim('TG5', 'Terminal lattice, vector and full-dual functional identities',
        'The raw terminal N, L and Lsharp are Nrow+O, Nrow+pi O and Nrow+conjugate(pi)^(-1)O. With z0=pi e_last and gamma the rational factor of the actual mv, prove exact til_lat, norm, orthogonal-line, til_fv, TilBaseLat and TilBaseFv clauses on their full integral domains.',
        ['TG3','SF2','FC1','FC5','FC6','NB1'],
        ['The row ST is empty. The literal supplied period Ok/Over identities retain tz=conjugate(pi), the original chosen mv and the original type residue map.'],
        ss(terminal,'til_L_eq L_act z0v hform_one_single hermitianForm_lastCoordinateUniformizerVector_self line_of_orth lastCoordinateUniformizerVector_spans_orthogonal_line dualL_le_Lsh TDat.fv_mk til_lat_eq til_fv_eq baseL_sup','substantive_terminal_lattice_vector_functional_proofs_reconstructed')+
        ss(HF+'LastCoordinateUniformizerVectorSpansOrthogonalLi.lean','TilTied TilBaseLat TilBaseFv','literal_integral_terminal_targets')+
        ss(I+'ExistsStandardFormComparisonSymmetricLevelMember.lean','hform_last','base_functional_normalization_counterpart'),
        'Uses the exact conjugate scalar and clears the full dual into N by conjugate(pi), then cancels its nonzero selected residue. Does not conflate N, L and Lsharp.'),
    claim('TG6', 'Actual terminal adelic incidence and evaluation scalar',
        'Construct ext(yP)kStd as a full IsPtOf realizer of the raw terminal decoration, derive kappa=x^-1 with rat(gamma)yM=ext(yP)kappa and chi(kappa)^-1=sigma(chi_col(mv)), prove uniqueness for the quantified IsExt clause, and obtain literal til_ties with eWz=id.',
        ['TG3','TG5','AD1','AD4','FC11'],
        ['The reference Q-frame set is empty and pi is congruent to one at every selected auxiliary prime. The gamma is the same actual mv factor as TG5.'],
        ss(terminal,'hatL_ext carries_ext extGL_mem_ustd hasRes_sum tilH_be isPtOf_tilFr pt_tilF exists_ka eq_extM_of_ext frMul_inv_eq til_ties','full_adelic_extension_and_evz_proof_reconstructed')+
        ss(HF+'LastCoordinateUniformizerVectorSpansOrthogonalLi.lean','TilAd','literal_quantified_adelic_incidence_target')+
        ss(HF+'FormsTied.lean','EvzTie','literal_terminal_evaluation_target'),
        'Checks all carried-lattice, type functional and auxiliary residue fields of IsPtOf. Both inverse conventions and the unique IsExt extension are explicit.'),
    claim('TG7', 'Construct the complete simultaneous FormsTiedSym family',
        'Join the actual existing chart/value/norm/move constructions with TG1-TG6 to construct formsTiedSym_std for every word, including StdF, StdLvC, finite chart sets, the unique terminal chart, constant G and CharacterCompatible.',
        ['TG2','TG3','TG4','TG5','TG6','FC1','FC3','FC4','FC5','FC6','FC7','FC8','FC13','FC14','FC15','FC17','FC18','CV9','DR3','NB7','NB8','SF2'],
        ['All endpoint and middle charts use the same prescribed frame coordinates and their original preferred labels. The period law is the literal supplied law, not TG7 itself.'],
        ss(I+'ExistsStandardFormComparisonSymmetricLevelMember.lean','formsTiedSym_std','actual_simultaneous_forms_constructor_closed')+
        ss(HF+'TiedSym.lean','FormsTiedSym','complete_target_fields_individually_supplied')+
        ss(A+'LatAtLattice.lean','StdF','literal_standardness_target')+
        ss(A+'StdLvPr.lean','StdLvPr StdLvC','literal_projection_standardness_and_penultimate_frame_target'),
        'A complete field-by-field source join after substantive suppliers are proved. Does not introduce FormsTiedSym or terminal geometric records as input premises.'),
    claim('TG8', 'Discriminant module, seen-prime orientation and exact projections',
        'Prove DiscCl as Lsharp/L isomorphic to O_E/(p) using local length-one factors and CRT, SeenCl at the exact coefficient embedding, coordinate transport of all quotient laws, and equality of middle/standalone pr and prk on their full domains.',
        ['TG7','FC1','FC5','NB1','LP1','SF2'],
        ['The class lattice is the actual type-kernel lattice in its self-dual companion. The tauOf and seenP identities are the original AtTTied identities.'],
        ss(I+'DualModClassLatticeEquivQuotient.lean','quotMapEquiv span_pi_eq span_conj_pi_eq span_T_eq quotT_equiv disc_cl','discriminant_source_endpoint_reconstructed_by_local_CRT')+
        ss(C+'DecoFin.lean','Deco.Ok.Lsh_quot_L','actual_integral_discriminant_counterpart')+
        ss(I+'HermitianSeenPrimeConditionHermitianSide.lean','pos_iff_mem_Pv seenCl_of seenCl_atT','exact_valuation_and_embedding_counterparts')+
        ss(I+'MiddleStepOneLevelProjectionEqChartProjection.lean','pr_lvC_eq_lv','full_domain_projection_equality_reconstructed')+
        ss(I+'MemSmulLk.lean','dual_co mem_Ld mem_Lk mem_smul_Ld mem_smul_Lk prH prkH SeenCl DiscCl localization_map₂','literal_coordinate_dual_projection_and_integral_targets'),
        'Shorter paired-prime and CRT proof of the module equivalence, and a prime-over-v proof of seen orientation. The projection proof clears denominators by conjugate(pi) and cancels its selected residue.'),
    claim('TG9', 'Hermitian row carrier and all level-prime move compatibilities',
        'Construct the actual Hermitian row StepLevel0/ClassTie/SameCar, transport the actual NB up/down matrices and FC18 diamond matrices, prove every UpCl/DnCl/DilCl clause, and obtain all six symmetric adelic compatibility clauses with the same supported factors and preserved chart labels.',
        ['TG3','TG4','TG8','FC1','FC6','FC9','FC18','NB4','NB5','NB6','NB7','NB8','DR3','AD4'],
        ['Move identities are asserted only for i<=m and the actual nonzero/up-normalized parameters. Outside those conditions a total function may use the identity with no extra move assertion.'],
        ss(I+'HermitianSideClassesEqFormClasses.lean','redM_eq_one mem_Uloc_of_princ tie_of_forms clsP_hermitian','actual_row_carrier_and_principal_congruence_proofs')+
        ss(I+'HermitianUpMoveAtLevelPrimePlace.lean','upCl_of_crd crd_up up_move','literal_up_Hermitian_and_adelic_endpoint')+
        ss(I+'ExistsHermitianDownMoveAtLevelPrimePlace.lean','dnCl_of_tie dn_move_exists','literal_down_Hermitian_and_adelic_endpoint')+
        ss(I+'DiamondOperatorHermitianSideLevelPrime.lean','exists_of_cls_eq lat_eq_of_move fT_move move_end move_mid dilCl_of_crd diamond_on_hermitian_side','literal_diamond_Hermitian_and_adelic_endpoint')+
        ss(I+'ExistsDiamondElementsStepLevels.lean','exists_int_isDia exists_isDia_steps','source_diamond_existence_reconstructed_by_explicit_split_diagonal')+
        ss(I+'MemSmulLk.lean','UpCl DnCl DilCl AdOf AdC','literal_exact_domains_and_adelic_relations')+
        ss(HC+'SymAll.lean','Ad0S AdIS SymmetricAdelicCompatibility','all_six_final_adelic_compatibility_fields'),
        'Uses the actual rational moving matrices and the exact factorization rat(gamma)y_new=y_old eta kappa. Coordinate isometries preserve localized full lattices and every specified residue functional.'),
    claim('TG10', 'Construct CarT and exact terminal stabilizer compatibility',
        'Construct AtT with all seen/discriminant/quotient/move/terminal laws and every CarT field. Prove the stabilizer equation by the actual mv^-1 ext(s) mv, including recovery of gamma from EvzTie for arbitrary standard supplied forms. This proves hermitian_data_at_level_prime.',
        ['TG5','TG6','TG7','TG8','TG9','FC9','SF2'],
        ['For the quantified source formulation, any supplied FormsTiedSym must satisfy literal StdF/StdLvC and CarH. The actual construction of those objects is TG7 and FC9.'],
        ss(I+'MemSmulLk.lean','gx crdN_gx hT_crdN lc_gmap mkAtT','complete_Hermitian_AtT_constructor_fields')+
        ss(A+'StdLvPr.lean','CarT','all_nine_literal_carrier_fields')+
        ss(I+'StabiliserMapHyperplaneEqConjClassMap.lean','eq_of_frMul ga_eq_gam_mv crdN_stabM crdP_stabP crdN_tilG gam_ext stabMap_tied','exact_preferred_movement_and_stabilizer_proof')+
        ss(HC+'SymAll.lean','SymmetricStabilizerMapCompatibility','literal_two_stabilizer_equations')+
        ss(I+'HermitianDataAtLevelPrime.lean','hermitian_data_at_level_prime','full_terminal_carrier_adelic_stabilizer_endpoint_closed'),
        'Constructs every field and proves source universality by an invertible-frame indicator test. No separate compatible CarT or terminal isometry is assumed.'),
    claim('TG11', 'Level-zero functional normalization and every residue-field level',
        'Replace only level-zero functional data by the reindexed forms functional, prove pi annihilates its prime-order target, compare arbitrary pi-annihilated nonzero functionals through the actual selected S_v/(pi)=F_p quotient, construct every FvTie and the exact ColLevelX with piG=X.piG.',
        ['TG7','TG8','TG10','FC6','FC9','FC13','FC15'],
        ['The actual type residue has prime cardinality p, pi has valuation one in the selected split component and is a unit in the conjugate component, and the completed functional is linear over the actual intV integer algebra.'],
        ss(I+'StepZeroHermitianLevelUniformiserKillsValues.lean','fun_transport smul_eq_zero_of_prime_card pi_kills stepZeroHermitianLevel_with_formsFunctional stepZeroHermitianLevel_uniformiser_kills_values','exact_replacement_and_pi_annihilation_proofs')+
        ss(I+'StepZeroLevelTypePrimeOrientationFramesFunctiona.lean','exists_equiv_of_cyclic functional_of_reindex colLevel_functional stepZeroLevel_functional_residueField intV_coe_eq_inclE_of_T_mem','selected_cyclic_quotient_comparison_and_level_zero_endpoint')+
        ss(I+'ChartLevelFunctionalsIntermediateStepsTrueColumn.lean','exists_reindex_hom fvTie_of_car fvTie_charts','actual_middle_residue_functional_transport')+
        ss(I+'LevelFunctionalChartLastStepClasses.lean','fvTie_of_coords fvTie_top fvTie_chart_top','actual_terminal_residue_functional_transport')+
        ss(HC+'SplitGAlg.lean','ColLevelX','literal_level_zero_extra_fields')+
        ss(HC+'SymAll.lean','SymmetricLevelZeroData SymmetricResidueFieldLevels','literal_all_word_and_all_chart_residue_interfaces'),
        'Uses a nonzero global functional value and prime additive order to prove pi-annihilation without falsely assuming fMe is intV-linear. The selected split cyclic quotient supplies the exact additive normalization.'),
    claim('TG12', 'The full source ColsTiedSym constructor',
        'Construct the complete ColsTiedSym(D) with StdC and StdLvC, including cofactor, companion-base, every residue level, level-zero generator compatibility, constant G and constant zero/row frames. This closes colsTiedSym_std under the original supplied arithmetic/column hypotheses.',
        ['TG7','TG8','TG9','TG10','TG11','FC9','FC13','FC15','SF2','SF3'],
        ['The source Pins.cof equation is retained exactly. The functional replacement changes no field used by the already-constructed AtT, CarT, adelic or stabilizer compatibility; those objects remain the same.'],
        ss(I+'HermitianColumnChoicesOfFormsLevelsClasses.lean','chart_level_classes top_level_classes level_classes_of hermColsCh_of_forms','earlier_FC9_carrier_constructor_reused')+
        ss(I+'BaseLatticeStepZeroAddConjGeneratorDualSelfDual.lean','base_sup_dual_eq base_step_zero_tied','step_zero_companion_identity_reconstructed_in_SF3')+
        ss(I+'ChartBaseLatticeSupDualSelfDual.lean','sup_dual_eq chart_base_sup_dual','all_chart_companion_identity_same_coordinate_proof')+
        ss(I+'HermitianColumnsGeneratorsBaseLatticesFunctional.lean','herm_rest_tied','final_cofactor_base_residue_level_zero_block_closed')+
        ss(HC+'SymAll.lean','SymmetricCofactorCompatibility SymmetricBaseCompatibility ColsHermS','complete_Hermitian_symmetric_target')+
        ss(HF+'BothSym.lean','ColsTiedSym','complete_final_comparison_target')+
        ss(A+'LatAtLattice.lean','StdC','literal_final_standardness')+
        ss(A+'StdLvPr.lean','StdLvC','literal_final_projection_standardness')+
        ss(I+'ExistsStandardColumnComparisonsTrueColumns.lean','colsTiedSym_std','actual_complete_constructor_closed'),
        'A field-by-field final join after all substantive suppliers are proved. Retains primitive host/Ok/Pins/Laws/Later, but no initial realizer, FormsTiedSym, CarT or terminal geometric existence premise.')
]

targets = [
    dict(id='TG-NEXT-1', priority=1, title='Twisted terminal chart and basepoint compatibility',
        scope='Extend the reference terminal IsPtOf and IsExt proof to the actual variable-twist Q-frames, the specified top congruence level and top character, retaining every dTop power and frame identity. This is adjacent work, not a premise of TG12.',
        supplied_by_this_component=['TG3','TG4','TG5','TG6','TG7','TG12'],
        sources=ss(I+'ChartLastStepTwistBasePoint.lean','reads_top root_top top_base chart_twm','adjacent_variable_twist_terminal_target_not_proved_here')),
    dict(id='TG-NEXT-2', priority=2, title='Standard twisted chain comparison',
        scope='Construct the actual all-twist chain forms, joint level-prime and row-layer compatibility packages from the now-constructed reference ColsTiedSym, with exact Law0 and tuple data. No claim that these records follow merely from the reference constructor.',
        supplied_by_this_component=['TG12'],
        sources=ss(I+'TrueColumnChoiceExistsChainDataWithBasePoints.lean','tw_ties_with_points','adjacent_twisted_chain_basepoint_constructor')+
                ss(I+'TrueColumnChoiceExistsStandardChainData.lean','colsTwPTiedS_std','adjacent_full_standard_twisted_comparison')),
    dict(id='TG-NEXT-3', priority=3, title='The strictly stronger one-level symmetric predicates',
        scope='Determine and prove the extra hypotheses that force singleton earlier chart sets, earlier HXS/lamX identifications and singleton penultimate orbit carrier. These extra fields are not part of ColsTiedSym and are not asserted by TG12.',
        supplied_by_this_component=['TG12'],
        sources=ss(HF+'BothSym.lean','OneLevelSymmetricColumns','strictly_stronger_target_definition_not_claimed_constructed'))
]

paragraphs = {}
main_raw = (HERE/'main.tex').read_bytes()
for i in range(1,13):
    start = main_raw.index(f'\\paragraph{{TG{i}:'.encode())
    stop = main_raw.index(f'\\paragraph{{TG{i+1}:'.encode(),start+1) if i<12 else len(main_raw)
    paragraphs[f'TG{i}'] = digest(main_raw[start:stop])

out = dict(schema_version='1.3', artifact_version='0.15', date='2026-11-22',
    owner='/root/comparison_span', repository=dict(url=URL,commit=PIN),
    range_convention='One-indexed inclusive; exact original declaration bytes, with no newline or Unicode normalization.',
    verification=dict(full_file_bytes_compared_with_pinned_git_blob=True,
        range_bytes_hashed_without_normalization=True, missing_sparse_files_read_from_pinned_git_blob=True,
        human_mathematical_proofs_supplied=True, lean_source_files_edited=False,
        local_lean_compilation=False, lean_kernel_replay=False,
        replacement_arguments_formalized=False, pdf_build_or_render=False),
    status_definitions=dict(derived_simplification='Complete human proof of the precisely stated supplied-data assertion, sometimes by a shorter argument than the source.'),
    claims=claims, files=[files[p] for p in sorted(files)],
    artifact_sha256={p:digest((HERE/p).read_bytes()) for p in ['main.tex','report.txt']},
    paragraph_sha256=paragraphs,
    prior_components_reused=['SF','FC','CV','LP','AD','DR','NB'],
    same_iteration_companions=['TL'], independent_reviews=[], retained_inputs=common,
    boundary_resolved=[
        'Exact penultimate HSym/lamSym group and character descriptions in stepBefore_oneLevel',
        'Actual terminal row ReadsP, ClsPTied and clsP_tie',
        'Full/row terminal HSym levels and compatible pi-last-diagonal frames',
        'Exact terminal z0, L/N/Lsharp, normalized residue, TilAd and EvzTie',
        'Complete FormsTiedSym with StdF/StdLvC and simultaneous common auxiliary data',
        'Actual AtT/CarT with all symmetric adelic and stabilizer compatibility clauses',
        'Level-zero pi-annihilation, exact residue normalization and all ColLevelX fields',
        'Complete herm_rest_tied and colsTiedSym_std endpoint'],
    scope_precision=[
        'All integral lattices and residue domains are exact; no trace-dual or Delta=dual-Weyl substitution occurs.',
        'The reference Q set is empty. Variable-twist terminal-frame and complete twisted comparisons are adjacent targets, not consequences claimed here.',
        'TG is proved under literal supplied Laws and has no TL dependency. Applying TL13 outside TG can discharge that premise without a cycle.',
        'TG11 changes only level-zero target module/functional data. TG12 applies it after constructing AtT, and proves every field used by the existing carrier/Ad/stabilizer assertions unchanged.',
        'The stronger OneLevelSymmetricColumns target is explicitly not constructed.',
        'No arithmetic host, Later/analytic package, RH/GRH theorem or kernel verification is asserted.'])

review_specs = [
    ('tl_reviews_tg_1_6.txt','/root/global_frame',list(range(1,7)),
     'Independent source and mathematical review of exact symmetric group/character, row realization, terminal frames, integral lattice/functional and adelic/evz conventions.'),
    ('root_reviews_tg_7_12.txt','/root',list(range(7,13)),
     'Independent review of full forms, discriminant/seen/projection, carrier/move/stabilizer, functional normalization and final ColsTiedSym dependency scope.')
]
for filename, reviewer, indices, scope in review_specs:
    review = HERE.parent/'reviews_v0_15'/filename
    if not review.exists():
        continue
    raw = review.read_bytes()
    content = raw.decode('utf-8')
    chosen = {f'TG{i}':paragraphs[f'TG{i}'] for i in indices}
    for claim_id, sha in chosen.items():
        assert sha in content, ('review paragraph changed',filename,claim_id,sha)
    out['independent_reviews'].append(dict(reviewer=reviewer,result='PASS',
        claim_ids=list(chosen),scope=scope,review_record='../reviews_v0_15/'+filename,
        review_record_sha256=digest(raw),paragraph_sha256=chosen,
        paragraph_range='Bytes from the named TG paragraph to the next TG paragraph, or EOF for TG12.',
        lean_replay=False))

(HERE/'provenance.json').write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n')
locators=[]
for c in claims:
    locators += [f"{c['id']} | {c['title']} | {c['status']}",c['statement']]
    for s in c['sources']:
        locators += [f"  {s['path']}:{s['line_start']}-{s['line_end']} {s['declaration']}",
            f"  role: {s['role']}",f"  file_sha256: {s['sha256']}",
            f"  range_sha256: {s['range_sha256']}",f"  {s['url']}"]
    locators += ['']
(HERE/'source_locators.txt').write_text('\n'.join(locators)+'\n')
(HERE/'source_manifest.json').write_text(json.dumps(dict(commit=PIN,files=out['files']),ensure_ascii=False,indent=2)+'\n')
(HERE/'next_targets.json').write_text(json.dumps(dict(version='0.15',commit=PIN,targets=targets,
    closed_source_targets=[
        dict(path=I+'ChartTiedTopLevelChain.lean',declaration='GlobalTheory.Mem.Col2.OneLevel.exists_gLevH',closed_by=['TG1','TG2']),
        dict(path=I+'ChartTiedTopLevelChain.lean',declaration='GlobalTheory.Mem.Col2.OneLevel.stepBefore_oneLevel',closed_by=['TG2']),
        dict(path=I+'LevelsTopRowSym.lean',declaration='GlobalTheory.Mem.Col2.TC.levels_top_row_sym',closed_by=['TG4']),
        dict(path=terminal,declaration='GlobalTheory.Mem.Col2.TC.til_ties',closed_by=['TG5','TG6']),
        dict(path=I+'ExistsStandardFormComparisonSymmetricLevelMember.lean',declaration='GlobalTheory.Mem.Col2.TC.formsTiedSym_std',closed_by=['TG7']),
        dict(path=I+'HermitianDataAtLevelPrime.lean',declaration='GlobalTheory.Mem.Col2.TC.hermitian_data_at_level_prime',closed_by=['TG8','TG9','TG10']),
        dict(path=I+'HermitianColumnsGeneratorsBaseLatticesFunctional.lean',declaration='GlobalTheory.Mem.Col2.TC.herm_rest_tied',closed_by=['TG11','TG12']),
        dict(path=I+'ExistsStandardColumnComparisonsTrueColumns.lean',declaration='GlobalTheory.Mem.Col2.TC.colsTiedSym_std',closed_by=['TG12'])],
    remaining_boundary='No separate reference terminal/symmetric carrier or initial-realizer premise remains. Primitive host and Later remain supplied; Laws can be independently discharged by TL. Adjacent all-twist and stronger one-level constructions are not asserted.'),ensure_ascii=False,indent=2)+'\n')
print(json.dumps(dict(claims=len(claims),source_links=sum(len(c['sources']) for c in claims),
    source_files=len(files),next_targets=len(targets),verified_equal_to_pinned_git_blob=True,
    independent_reviewed_claims=[i for r in out['independent_reviews'] for i in r['claim_ids']])))


