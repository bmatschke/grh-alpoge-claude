#!/usr/bin/env python3
"""Rebuild JIO source/proof certificates without running Lean.

Portable invocation:
  python3 build_metadata.py --source /path/to/pinned/checkout \
      --human-root /path/to/reconstruction --peer-root /path/to/reconstruction

In a release both human-root and peer-root are its root.  During drafting,
human-root is reconstruction_v035 and peer-root is work_v036.
All line ranges are inclusive and retain the original newline bytes.
"""
from pathlib import Path
import argparse
import hashlib
import json
import re
import subprocess

HERE = Path(__file__).resolve().parent
DEFAULT_HUMAN = HERE.parent if (HERE.parent / "canonical_weil").exists() else HERE.parent.parent / "reconstruction_v035"
p = argparse.ArgumentParser(description=__doc__)
p.add_argument("--source", type=Path, default=HERE.parent.parent / "lean_source")
p.add_argument("--human-root", type=Path, default=DEFAULT_HUMAN)
p.add_argument("--peer-root", type=Path, default=HERE.parent)
args = p.parse_args()
SOURCE, HUMAN, PEER = args.source.resolve(), args.human_root.resolve(), args.peer_root.resolve()
PIN = "7cbf7a0c32fca1badf05931879a37c3f8a2b03b4"
REPO = "https://github.com/CocoSgt/riemann-hypothesis-lean"
sha = lambda b: hashlib.sha256(b).hexdigest()
assert subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=SOURCE, text=True).strip() == PIN
decl = re.compile(r"^(?:(?:private|protected|noncomputable|unsafe)\s+)*(?:def|abbrev|theorem|lemma|structure|class|instance)\s+")
cache, sources = {}, {}


def add(sid, path, anchor, stop=None, role="Exact original definition, contract or proof independently reconstructed in the stated scope"):
    anchor = anchor.rstrip()
    path = "src/" + path
    if path not in cache:
        b = (SOURCE / path).read_bytes()
        assert b == subprocess.check_output(["git", "show", PIN + ":" + path], cwd=SOURCE), path
        cache[path] = b, b.decode().splitlines(keepends=True)
    b, lines = cache[path]
    anchor_re = re.compile(re.escape(anchor) + r"(?=$|[\s:({])")
    hits = [i for i, line in enumerate(lines) if anchor_re.search(line)]
    assert len(hits) == 1, (sid, path, anchor, hits)
    a = hits[0]
    z = next((i for i in range(a + 1, len(lines)) if (stop in lines[i] if stop else decl.match(lines[i]))), len(lines))
    while z > a and not lines[z - 1].strip():
        z -= 1
    block = "".join(lines[a:z]).encode()
    sources[sid] = {
        "id": sid, "path": path, "declaration": anchor, "declaration_anchor": anchor,
        "line_start": a + 1, "line_end": z, "sha256": sha(b), "file_sha256": sha(b),
        "range_sha256": sha(block), "range_bytes": len(block), "first_line": lines[a].rstrip(),
        "role": role, "verified_equal_to_pinned_git_blob": True,
        "url": f"{REPO}/blob/{PIN}/{path}#L{a + 1}-L{z}",
    }


D = "Development/AbelianVarietyTheory/"
IW = D + "Proofs/IwasawaDecomposition/"
DP = D + "Proofs/DivisorProofs/"
FM = D + "Proofs/FlagMeasures/"
TW = D + "Proofs/TwistedOperators/"
IR = "Formalism/LocalToGlobal/IndefiniteReal/"
BT = "Formalism/LocalToGlobal/BesselHermitianTheta/"
JH = IW + "IsHolRepOfIsTau.lean"
ORIG = IW + "ExistsLowestKTypeFockMapThetaVectors.lean"
LF = IR + "LocalNewformFunction.lean"
REST = "Retained original producer or downstream consumer boundary; no production asserted by JIO"

for sid, anchor in [
    ("hol_rep", "def IsHolRep "), ("bottom", "def IsBottom "),
    ("hol_family", "def IsHolFam "), ("bottom_family", "def IsBotFam "),
    ("fock_substitution", "def fsub "), ("positive_det", "def detP "),
    ("negative_det", "def detM "), ("fock_character", "def fchar "),
    ("fock_action", "def fact "), ("fock_K_action", "def factK "),
    ("fock_U_action", "def factU "), ("target_weight", "def wtK "),
    ("source_weight", "def wtU "), ("coefficient_action", "def vact "),
]:
    add(sid, JH, anchor)
for sid, anchor in [("factorial", "def mfact "), ("fock_form", "def fockS "), ("fock_linear_form", "def fockL ")]:
    add(sid, "Formalism/LocalToGlobal/Divisibility/CoefMod.lean", anchor)

FAD = IW + "FockPolynomialActionOneMulAdjoint.lean"
for sid, anchor in [
    ("linear_substitution", "def lsub "), ("linear_substitution_product", "theorem lsub_mul "),
    ("substitution_derivative", "theorem pderiv_lsub "), ("substitution_adjoint", "theorem fockL_lsub_adj "),
    ("sign_off_block_zero", "theorem entry_eq_zero "), ("linear_action_matrix", "def fmat "),
    ("action_matrix_product", "theorem fmat_mul "), ("action_matrix_adjoint", "theorem fmat_conj "),
    ("substitution_is_linear_action", "theorem fsub_eq_lsub "),
    ("fock_character_product", "theorem fchar_mul "), ("fock_character_adjoint", "theorem fchar_conj "),
    ("fock_one_product_adjoint", "theorem fact_one_mul_adj "),
]:
    add(sid, FAD, anchor)
FHF = IW + "FockActionsIsHolomorphicProductKRepFamily.lean"
for sid, anchor in [
    ("fock_anisotropy", "theorem fockL_aniso "), ("two_det_product", "theorem detPlus_mul_detMinus "),
    ("fock_differentiability", "theorem fact_diff "), ("fock_hol_families", "theorem main "),
]:
    add(sid, FHF, anchor)
for sid, anchor in [
    ("minor_plus", "def minorPlus "), ("minor_minus", "def minorMinus "),
    ("delta_one_place", "def deltaAt "), ("delta_product", "def delta "),
]:
    add(sid, LF, anchor)
FMIN = IW + "FsubMinorMinus.lean"
for sid, anchor in [
    ("minor_telescope", "theorem telescope "), ("source_weight_regroup", "theorem regroup "),
    ("minor_plus_eigen", "theorem fsub_minorPlus "), ("minor_minus_eigen", "theorem fsub_minorMinus "),
    ("original_delta_eigen", "theorem fsub_delta "),
]:
    add(sid, FMIN, anchor)
JB = IW + "ExistsMinorProductTranslateJointLowestWeight.lean"
for sid, anchor in [
    ("negative_tail_reversal", "def revTail "), ("reversal_involution", "theorem revTail_mul_self "),
    ("reversed_minor_eigen", "theorem eigen "), ("joint_bottom", "theorem exists_joint_bottom "),
]:
    add(sid, JB, anchor)

for sid, anchor in [
    ("peak", "def peak "), ("peak_positive", "theorem peak_pos "),
    ("peak_unique_maximum", "theorem peak_lt "),
    ("compact_holomorphic_extension", "theorem exists_holomorphic_extension "),
]:
    add(sid, FM + "HolomorphicExtensionCompactRep.lean", anchor)
add("complex_block_identity", FM + "EqZeroOnKCOfEqZeroOnKset.lean", "theorem eq_zero_on_KC_of_eq_zero_on_Kset ")
for sid, anchor in [
    ("extension_multiplicativity", "theorem mul_on_KC "),
    ("extension_adjoint", "theorem adj_on_KC "),
    ("conjugated_compact_type", "theorem tauExists "),
]:
    add(sid, FM + "KTypeExtendsHolomorphicComplexifiedK.lean", anchor)
for sid, anchor in [
    ("compact_dominance", "def CDom "), ("compact_type", "def IsKTypeOf "),
    ("original_lowest_supremum", "def lowKSub "),
]:
    add(sid, "Formalism/PeriodIntegrals/UpqRep.lean", anchor)
for sid, anchor in [
    ("lower_root_dominance_contradiction", "lemma not_cdom "),
    ("lower_root_weight", "lemma wt_single "),
    ("lower_unipotent_fixes_bottom", "theorem lowest_fixed "),
]:
    add(sid, FM + "LowestWeightVectorFixedByLowerUnitriangular.lean", anchor)
for sid, anchor in [
    ("positive_torus_bottom", "theorem real_torus "),
    ("lower_borel_bottom", "theorem borel "),
    ("universal_gram_scalar", "theorem gram "),
    ("bottom_coefficient_identity", "theorem coeff_eq "),
]:
    add(sid, IW + "LowestWeightMatrixCoefficientDependsOnWeight.lean", anchor)
for sid, anchor in [
    ("product_adjoint", "theorem adj_fam "), ("other_place_bottom", "theorem bottom_move "),
    ("product_bottom_coefficient", "theorem coef_fam "), ("product_gram", "theorem gram_fam "),
    ("linear_map_from_gram", "theorem exists_map_of_gram "), ("orbit_map", "theorem exists_orbit_map "),
]:
    add(sid, IW + "LowestWeightVectorTransfer.lean", anchor)
for sid, anchor in [
    ("universal_operator", "theorem exists_op_of_isTau "),
    ("original_compact_operator", "theorem exists_op "),
]:
    add(sid, IW + "ExistsOperatorLowestWeightHolomorphicKType.lean", anchor)
for sid, anchor in [
    ("tensor_commuting_operators", "theorem exists_multi "),
    ("tensor_operator_core", "theorem core "), ("original_lowest_family_operator", "theorem lowest_types_act "),
]:
    add(sid, IW + "HolomorphicFamilyLowLieAction.lean", anchor)
add("smooth_compact_seed", IW + "ExistsLowestKTypeLeSmoothVectors.lean", "theorem exists_lowK_le_sm ")
for sid, anchor in [
    ("stored_cartan", "def cart "), ("stored_orthonormal_frame", "def onb "),
    ("original_lowest_intersection", "def lowT "), ("original_lowest_tensor", "abbrev LowT "),
]:
    add(sid, IR + "LinksDefs.lean", anchor)
add("original_DSModel", IR + "ScalarOnPartsFull.lean", "structure DSModel ")
add("original_smooth_span", IR + "ScalarOnPartsFull.lean", "def DSModel.sm ")

for sid, anchor in [
    ("dominant_weight", "structure DomWeight "), ("determinant_shift", "def detShift "),
    ("natural_weight", "def natW "), ("square_coefficient_space", "def nablaSq "),
    ("literal_extremal", "def extremal "),
]:
    add(sid, "Formalism/LocalRingCardinality/DataCoeff.lean", anchor)
for sid, anchor in [
    ("column_definition_dual_weyl", "def dualWeyl "),
    ("leading_minor", "def lpMinor "), ("highest_minor_product", "def hw "),
]:
    add(sid, "Formalism/GradedWeylDivisibility/StatementA.lean", anchor)
for sid, anchor in [
    ("coefficient_action_adjoint", "theorem vhol_adj "),
    ("coefficient_holomorphic_bottom", "theorem vact_isHolFam_isBotFam "),
]:
    add(sid, IW + "FrameFunctionActionHolomorphicExtremalLowest.lean", anchor)
add("coefficient_compact_cyclicity", IW + "CoefficientSpaceLeSpanUnitaryOrbitExtremal.lean", "theorem VV_le_span_vact_extremal ", role="Exact original interface supplied by companion CFB6")
add("original_coefficient_bridge", IW + "ExistsPolynomialModelCoefficientSpaceRealPoints.lean", "theorem exists_poly_model ", role="Exact original interface supplied by companion CFB5")
add("coefficient_tie", IR + "BridgeTie.lean", "def CoefMapTie ")
add("source_coefficient_module", IR + "LinksDefs.lean", "structure CoefA ")
add("source_coefficient_Is", IR + "LinksDefs.lean", "def Is : Prop")
for sid, anchor in [
    ("actual_theta_activation", "theorem isThetaFunO_of_isThetaAt "),
    ("compact_inverse_transpose", "theorem invT_conj "),
    ("two_fock_actions_commute", "theorem commute_factU_factK "),
    ("parameter_free_io", "theorem exists_io_poly "),
    ("simultaneous_io_producer", "theorem exists_ioP "),
]:
    add(sid, ORIG, anchor)

for sid, anchor in [
    ("theta_function", "structure IsThetaFunO "),
    ("actual_weil_datum", "structure IsWeilDatumO "),
    ("original_place_model", "structure IsPlaceModel "),
    ("original_all_place_models", "def IsThetaAt "),
    ("real_Heisenberg_derivative", "def dRho "),
    ("cartan_complex_structure", "def cplxO "),
    ("original_creator", "def crea "), ("fock_scale", "def fockScale "),
    ("scaled_creator", "def aPlus "), ("fock_vacuum", "def IsFockVacAt "),
    ("actual_unit_direction", "def unitMap "),
    ("original_polynomial_evaluation", "def pureTensorL "),
    ("all_original_creators", "def aPlusAll "),
]:
    add(sid, LF, anchor)
add("original_stored_vacuum", IR + "DatumVec.lean", "def IsThPVecOf ")
add("vacuum_from_AllSome", TW + "IsFockVacAtOfIsThetaAt.lean", "theorem isFockVacAt_of_isThetaAt ")
add("stored_fock_vacuum", TW + "IsFockVacAtOfIsThetaAt.lean", "theorem isFockVacAt_thPVec ")
for sid, anchor in [
    ("idele_character_comparison", "def ChrEq "),
    ("original_level_characters", "structure LevCh "),
    ("actual_twisted_character", "def mu (t : T)"),
    ("level_character_Is", "structure Is (μ0 : T)"),
]:
    add(sid, IR + "LinksDefs.lean", anchor)
for sid, anchor in [
    ("actual_Delta", "def Delta "), ("actual_ptP", "def ptP "),
    ("actual_family_Is", "structure IsFam "), ("actual_models_Is", "structure IsModels "),
    ("actual_weil_family", "abbrev thP_ωP "), ("actual_vacuum_family", "abbrev thP_vP "),
    ("polynomial_theta_family", "abbrev thP_pt_theta "), ("strong_io_family", "abbrev thP_ioP "),
    ("original_IsIoW", "def IsIoW "),
]:
    add(sid, IR + "LinksChar.lean", anchor)
for sid, anchor in [
    ("parameter_twist", "def tup "), ("actual_pair_characters", "def chrTh "),
]:
    add(sid, IR + "HasInfExpF.lean", anchor)
for sid, anchor in [
    ("actual_Hecke_character", "def IsHeckeChar "),
    ("actual_infinity_exponent", "def HasInfExp "), ("actual_quadratic_restriction", "def ResEta "),
]:
    add(sid, BT + "DefsReal.lean", anchor)
add("finite_tensor_components", D + "Proofs/FoundationProofs/ExistsBaseChangeFiniteAdeleRingEquiv.lean", "theorem exists_finiteAdele_equiv ", role="Same finite restricted-product coordinate interface; JIO14 proves only the part needed for the character transport")
for sid, anchor in [
    ("local_principal_net", "theorem tendsto_inf_mul_prod "),
    ("principal_real_character_comparison", "theorem eq_inf "),
    ("infinity_exponent_transport", "theorem hasInfExp_of_chrEq "),
]:
    add(sid, TW + "TendstoInfMulProd.lean", anchor)
add("archimedean_density_character", D + "Proofs/FoundationProofs/HeckeCharEqOneOfTrivialFinitePartOne.lean", "theorem eq_one_of_trivial_on_finite ")
for sid, anchor in [
    ("infinity_exponent_product", "theorem hasInfExp_mul "),
    ("infinity_exponent_inverse", "theorem hasInfExp_inv "),
]:
    add(sid, IW + "HeckeCharacterInfinityExponentGroupLaws.lean", anchor)
add("all_parameter_infinity_types", IW + "ThetaLiftInfinityTypesAtRealPlace.lean", "theorem infTypesAt ")
add("original_infinity_types_contract", D + "BlockTheory/TwistedDiscreteSeries/InfinityTypes.lean", "structure InfTypesAt ")

add("actual_determinant_root", BT + "TiedWeil.lean", "def IsDetRoot ")
for sid, anchor in [
    ("real_one_place_idele", "theorem exists_idele_at "),
    ("real_determinant_root_values", "theorem exists_root "),
    ("positive_Hom_determinant", "theorem detPlus_one "),
    ("twisted_infinity_exponent", "theorem hasInfExp_twist "),
]:
    add(sid, DP + "ExistsIdeleAt.lean", anchor)
add("general_real_vacuum_character", DP + "WeilDatumRealPlacesFockVacuumCharacter.lean", "theorem vacuum_character ", role="Original scalar interface; JIO16 uses CW24's already constructed eta0 route without adding the source's universal auxiliary IsEtaTilde existence as a premise")
add("positive_source_vacuum_character", DP + "VacuumCharacterPositiveDefiniteSource.lean", "theorem vacuum_character ")
FB = IW + "FockPolynomialVectorChangeOrthonormalBasesSubst.lean"
for sid, anchor in [
    ("unit_direction_change", "theorem unitMap_mul "),
    ("creator_complex_or_conjugate_linear", "theorem aPlus_smul_dir "),
    ("creator_frame_change", "theorem aPlus_unitMap_mul "),
    ("polynomial_substitution_induction", "theorem pure_subst "),
    ("original_Fock_basis_change", "theorem pureTensorO_basis "),
]:
    add(sid, FB, anchor)
FC = IW + "WeilMaximalCompactFockSubstitutionCharacter.lean"
for sid, anchor in [
    ("source_frame_positive_cartan", "theorem isCartanInv_one "),
    ("source_real_conjugate_unitary", "theorem conj_unitary "),
    ("target_frame_determinants", "theorem det_conj "),
    ("polynomial_vacuum_scaling", "theorem pureTensorO_smul "),
    ("actual_compact_Weil_Fock_action", "theorem om_pureTensorO_eq_fact "),
]:
    add(sid, FC, anchor)
add("original_polynomial_Weil_covariance", D + "Proofs/AdelicLatticeProofs/PureTensorLIntertwine.lean", "theorem om_pureTensorO ")
for sid, anchor in [
    ("weak_choice", "def OrZero "), ("all_parameter_io_predicate", "def PIoP "),
    ("stored_io_weak_law", "abbrev tw_ioP "), ("existential_io", "abbrev ex_ioP "),
    ("stored_full_theta_activation", "theorem thP_of_weak "),
]:
    add(sid, IR + "LinksW.lean", anchor)
add("full_analytic_extension", IW + "ExistsThetaLiftLinearMapCuspFormMultiplicity.lean", "theorem exists_extension ", role=REST)
add("base_theta_firing", IW + "ExistsThetaLiftLinearMapCuspFormMultiplicity.lean", "theorem firesAt ", role=REST)
add("remaining_boundedness", IW + "BoundedOfSmoothCuspidalUniformModerate.lean", "theorem bounded_of_smooth_unifModGrowth ", role=REST)
add("remaining_actual_volume", IW + "FiniteVolumeAdelicUnitaryQuotient.lean", "theorem finVol ", role=REST)
add("remaining_pointwise_representative", DP + "SmoothVectorAutomorphicDerivatives.lean", "theorem exists_smooth_repr ", role=REST)
add("remaining_pointwise_Sobolev", DP + "SobolevBoundForSmoothVectors.lean", "theorem pointwise_growth ", role=REST)

titles = {
 "JIO1": "Linear polynomial substitution and the exact factorial adjoint",
 "JIO2": "Both original twisted Fock actions are holomorphic product representations",
 "JIO3": "Literal minor product, nonvanishing and triangular eigenvalues",
 "JIO4": "Negative-tail reversal and the exact joint bottom vector",
 "JIO5": "Explicit peaked-Haar holomorphic extension of a compact representation",
 "JIO6": "Conjugated original compact type and its full bottom-vector laws",
 "JIO7": "Bottom matrix coefficients depend only on the specified weight",
 "JIO8": "Product-family orbit transfer from complete Gram relations",
 "JIO9": "One universal finite-type operator with compact operator-span control",
 "JIO10": "Full original LowT operator construction by smooth seed and projection",
 "JIO11": "Literal coefficient polynomial action and nonzero bottom extremal",
 "JIO12": "Complete parameter-free io_poly with exact unit-vector Delta normalization",
 "JIO13": "Actual stored theta and Fock-vacuum activation, all polynomial theta values",
 "JIO14": "Exact original infinity types uniformly for every parameter",
 "JIO15": "Real determinant roots and their simultaneous integral character evaluation",
 "JIO16": "Exact actual real vacuum character via the constructed full Weil comparison",
 "JIO17": "Original orthonormal-frame change and precise Fock substitution",
 "JIO18": "Actual compact Weil substitution character for every polynomial",
 "JIO19": "Full original exists_ioP with one io_i for all t and stored weak activation",
}
maps = {
 "JIO1": ["factorial","fock_form","fock_linear_form","linear_substitution","linear_substitution_product","substitution_derivative","substitution_adjoint"],
 "JIO2": ["hol_rep","hol_family","fock_substitution","positive_det","negative_det","fock_character","fock_action","fock_K_action","fock_U_action","sign_off_block_zero","linear_action_matrix","action_matrix_product","action_matrix_adjoint","substitution_is_linear_action","fock_character_product","fock_character_adjoint","fock_one_product_adjoint","fock_anisotropy","two_det_product","fock_differentiability","fock_hol_families","two_fock_actions_commute"],
 "JIO3": ["minor_plus","minor_minus","delta_one_place","delta_product","minor_telescope","source_weight_regroup","minor_plus_eigen","minor_minus_eigen","original_delta_eigen"],
 "JIO4": ["bottom","bottom_family","target_weight","source_weight","negative_tail_reversal","reversal_involution","reversed_minor_eigen","joint_bottom"],
 "JIO5": ["peak","peak_positive","peak_unique_maximum","compact_holomorphic_extension","complex_block_identity","extension_multiplicativity","extension_adjoint","hol_rep"],
 "JIO6": ["compact_dominance","compact_type","conjugated_compact_type","lower_root_dominance_contradiction","lower_root_weight","lower_unipotent_fixes_bottom","bottom"],
 "JIO7": ["hol_rep","bottom","positive_torus_bottom","lower_borel_bottom","universal_gram_scalar","bottom_coefficient_identity"],
 "JIO8": ["hol_family","bottom_family","product_adjoint","other_place_bottom","product_bottom_coefficient","product_gram","linear_map_from_gram","orbit_map"],
 "JIO9": ["universal_operator","original_compact_operator","compact_type","bottom_coefficient_identity"],
 "JIO10": ["original_lowest_supremum","original_DSModel","original_smooth_span","smooth_compact_seed","original_lowest_intersection","original_lowest_tensor","tensor_commuting_operators","tensor_operator_core","original_lowest_family_operator"],
 "JIO11": ["dominant_weight","determinant_shift","natural_weight","square_coefficient_space","literal_extremal","column_definition_dual_weyl","leading_minor","highest_minor_product","coefficient_action","coefficient_action_adjoint","coefficient_holomorphic_bottom"],
 "JIO12": ["parameter_free_io","coefficient_tie","source_coefficient_module","source_coefficient_Is","original_coefficient_bridge","coefficient_compact_cyclicity","compact_inverse_transpose","two_fock_actions_commute","joint_bottom","original_lowest_family_operator"],
 "JIO13": ["actual_theta_activation","theta_function","original_place_model","original_all_place_models","original_stored_vacuum","vacuum_from_AllSome","stored_fock_vacuum","real_Heisenberg_derivative","original_creator","scaled_creator","original_polynomial_evaluation","actual_vacuum_family","polynomial_theta_family","actual_ptP"],
 "JIO14": ["idele_character_comparison","actual_Hecke_character","actual_infinity_exponent","original_level_characters","level_character_Is","actual_twisted_character","parameter_twist","actual_pair_characters","finite_tensor_components","local_principal_net","principal_real_character_comparison","infinity_exponent_transport","archimedean_density_character","infinity_exponent_product","infinity_exponent_inverse","all_parameter_infinity_types","original_infinity_types_contract"],
 "JIO15": ["actual_determinant_root","actual_infinity_exponent","real_one_place_idele","real_determinant_root_values"],
 "JIO16": ["actual_weil_datum","actual_quadratic_restriction","actual_infinity_exponent","fock_vacuum","cartan_complex_structure","positive_Hom_determinant","twisted_infinity_exponent","general_real_vacuum_character","positive_source_vacuum_character"],
 "JIO17": ["stored_cartan","stored_orthonormal_frame","actual_unit_direction","fock_scale","scaled_creator","original_polynomial_evaluation","all_original_creators","unit_direction_change","creator_complex_or_conjugate_linear","creator_frame_change","polynomial_substitution_induction","original_Fock_basis_change"],
 "JIO18": ["actual_weil_datum","original_polynomial_Weil_covariance","source_frame_positive_cartan","source_real_conjugate_unitary","target_frame_determinants","polynomial_vacuum_scaling","actual_compact_Weil_Fock_action"],
 "JIO19": ["simultaneous_io_producer","parameter_free_io","original_IsIoW","actual_Delta","actual_ptP","actual_family_Is","actual_models_Is","level_character_Is","actual_weil_family","actual_vacuum_family","polynomial_theta_family","strong_io_family","all_parameter_io_predicate","weak_choice","stored_io_weak_law","existential_io","stored_full_theta_activation"],
}
deps = {
 "JIO1": [], "JIO2": ["JIO1"], "JIO3": [], "JIO4": ["JIO2","JIO3"],
 "JIO5": [], "JIO6": ["JIO5"], "JIO7": [], "JIO8": ["JIO7"],
 "JIO9": ["JIO6","JIO7"], "JIO10": ["JIO9","HCU8"],
 "JIO11": ["JIO1","JIO2","JIO3"],
 "JIO12": ["JIO2","JIO4","JIO8","JIO10","JIO11","CFB5","CFB6"],
 "JIO13": ["CW12","TAE3","TAE9"], "JIO14": ["HCU14"], "JIO15": ["HCU14"],
 "JIO16": ["JIO15","CW11","CW13","CW24","BTH14","HF9","HF11"],
 "JIO17": ["JIO13","CW12","TAE3"], "JIO18": ["JIO16","JIO17","CW12","TAE3"],
 "JIO19": ["JIO12","JIO13","JIO14","JIO18","CFB13","HCU14"],
}
scopes = {
 "JIO1": "Any finite variable set; all complex polynomials and all complex matrices. Original conjugate-first factorial form and substitution X_e -> sum_f A_fe X_f.",
 "JIO2": "All original D,m,n,signs and integer twists; k in the complex sign centralizer, u invertible. Includes negative determinant powers, all one-place scalar holomorphy and exact F_U/F_K commutation.",
 "JIO3": "Original m<=n, p+q=m, ordered sign blocks, nonnegative antitone ap/am only on their actual finite ranges. Uses literal natural exponent subtraction; no exponent/phase discarded.",
 "JIO4": "Same original Delta and twists as JIO3; explicit real unitary negative-tail reversal; full IsBotFam with target weight MINUS wtK and source weight wtU; fact(kappa,1)Delta'=Delta exactly.",
 "JIO5": "Any continuous finite-dimensional unitary compact block representation; explicit function holomorphic on GL_m and representation/adjoint only on the complex block centralizer. Does not assert multiplication on all GL_m.",
 "JIO6": "Exact original IsKTypeOf and unitary compact action; same finite subspace, sigma(bar k) action, unit highest vector becomes a bottom vector of negative original weight.",
 "JIO7": "Any two original IsHolRep spaces with anisotropic sesquilinear forms and four bottom vectors of the same real weight; no finite-dimensionality of the compared ambient spaces and no nonzero cross coefficient assumption.",
 "JIO8": "Finite product of same sign groups, original IsHolFam/IsBotFam, only source bottom x' nonzero; linear map on whole source polynomial space is an algebraic extension, with intertwining only on the explicitly controlled orbit span.",
 "JIO9": "Original finite compact IsKTypeOf and arbitrary IsHolRep target. A SINGLE right inverse/operator T is chosen before EVERY bottom vector y; every T(s) stays in span of actual compact operators.",
 "JIO10": "Every original DSModel, not only HolShape, and any supplied IsHolFam. Actual lowT is the smooth intersection of the full lowKSub supremum; finite seed is used only via equivariant projection, not as a substitute source space.",
 "JIO11": "Every finite family of integral dominant weights including n=0; literal determinant shift/natural weight, VV polynomial definition, actual extremal, conjugate-first Fock form, and weight -lambda.",
 "JIO12": "Exactly original exists_io_poly premises including SAME CoefMapTie, actual c0, all invertible BS, both weight identities and all rank/order/antitone hypotheses. One map before any t; exact Delta at unit original vectors and both polynomial covariances.",
 "JIO13": "Any original IsThetaAt with original theta initial vacuum; AllSome perturbation proves its output is theta. On thP_vP, same stored vP is Fock vacuum and every original ptP polynomial is theta. No arbitrary choice of a different theta vector.",
 "JIO14": "Every original LevCh with Is(mu0); all i,t,tau with no threshold. ChrEq comparison is on original one-place principal finite ideles; continuity and actual real coordinates give the literal AllSome HasInfExp, including exponent factor two.",
 "JIO15": "Original nondegenerate Hermitian real-supported g; one real determinant root before every character of integral infinity exponents. Root value formula uses phase exponent 2c and is unchanged under square-root sign.",
 "JIO16": "Original full oriented Weil datum, standard sign-minus-one character, actual S/T SigOK, positive source Cartan, target Cartan, all-place vacuum and three specified INTEGER exponents. CW24 eta0 is auxiliary, not identified with stored eta and not promoted to universal IsEtaTilde.",
 "JIO17": "Original source orthonormal BS, target onb=M.fr^-1, exact cart M, actual fockScale, any theta initial function and all polynomials. Compact changes k,u only; positive/negative complex-conjugate scalar distinction retained.",
 "JIO18": "Exact original compact Fock character theorem: supplied full omega, same frames/Cartans/infinity exponents, real-supported g,h, target compact conjugate. Actual action on theta functions is differentiated through L2 isometry, not unproved continuity on all functions.",
 "JIO19": "ONE arbitrary original R with toLevCh.Is(mu0), IsFam, IsModels, thP_omegaP, thP_vP. Proves thP_pt_theta and forall i exists io_i forall t IsIoW; then actual stored OrZero PIoP gives strong ioP. No family threshold, replacement model, or io_(i,t) introduced.",
}
assert set(titles) == set(maps) == set(deps) == set(scopes)
assert all(s in sources for ss in maps.values() for s in ss)


def human_blocks(root, rel, ids, role):
    b = (root / rel).read_bytes()
    lines = b.splitlines(keepends=True)
    out = []
    for cid in ids:
        begin, end = ("% BEGIN " + cid).encode(), ("% END " + cid).encode()
        hits = [i for i, line in enumerate(lines) if line.strip() == begin]
        if hits:
            assert len(hits) == 1
            a = hits[0]
            z = next(i for i in range(a + 1, len(lines)) if lines[i].strip() == end) + 1
        else:
            pat = ("\\paragraph{" + cid + ":").encode()
            hits = [i for i, line in enumerate(lines) if line.startswith(pat)]
            assert len(hits) == 1, (rel, cid, hits)
            a = hits[0]
            z = next((i for i in range(a + 1, len(lines)) if lines[i].startswith(b"\\paragraph{")), len(lines))
            while z > a and not lines[z - 1].strip():
                z -= 1
        block = b"".join(lines[a:z])
        out.append({"id": cid, "line_start": a + 1, "line_end": z,
                    "sha256": sha(block), "range_sha256": sha(block), "bytes": len(block)})
    return {"file": rel, "sha256": sha(b), "file_sha256": sha(b), "role": role, "claims": out}


inherited = [
    human_blocks(HUMAN, "holomorphic_uniqueness/main.tex", ["HCU8","HCU14"], "Incoming human proofs: actual smooth compact seed and exact original archimedean coordinate/lift identities."),
    human_blocks(HUMAN, "canonical_weil/main.tex", ["CW11","CW12","CW13","CW24"], "Incoming human proofs: actual real oscillator vacuum determinant, genuine theta Banach smoothness, oriented Hom action, and auxiliary eta0 prescribed-character construction."),
    human_blocks(HUMAN, "base_theta/main.tex", ["BTH14"], "Incoming human proof: two full Weil data with same original characters agree on the same theta space."),
    human_blocks(HUMAN, "host_character_frame/main.tex", ["HF9","HF11"], "Incoming explicit auxiliary quadratic character and its Hecke extension, as used in CW24; not an IsEtaTilde universal uniqueness assertion."),
    human_blocks(HUMAN, "theta_extension/main.tex", ["TAE3","TAE9"], "Incoming actual Heisenberg/Weil derivative calculus and stored-vacuum AllSome transfer, with their original inputs preserved."),
    human_blocks(PEER, "coefficient_fock_bridge/main.tex", ["CFB5","CFB6","CFB13"], "Same-iteration incoming proofs: exact original coefficient j, literal compact extremal cyclicity, and all original same-R/i weight/tie/frame installation BEFORE t."),
]
downstream = [
    human_blocks(HUMAN, "holomorphic_uniqueness/main.tex", ["HCU20"], "Downstream context only; same base LowSm/LowIrr already proved. Not an incoming proof premise of the simultaneous io construction."),
    human_blocks(HUMAN, "theta_extension/main.tex", ["TAE13"], "Downstream context only; the io supplier of its analytic/cuspidal packet is now discharged on the same original inputs. No full MMap is inferred."),
]
incoming_ids = {b["id"] for r in inherited for b in r["claims"]}
assert all(d in titles or d in incoming_ids for ds in deps.values() for d in ds)
tex = (HERE / "main.tex").read_bytes()
lines = tex.splitlines(keepends=True)
claims = []
for cid, title in titles.items():
    a = next(i for i, line in enumerate(lines) if line.strip() == ("% BEGIN " + cid).encode())
    z = next(i for i, line in enumerate(lines) if line.strip() == ("% END " + cid).encode()) + 1
    block = b"".join(lines[a:z])
    claims.append({
        "id": cid, "title": title, "introduced_in": "0.36", "classification": "B",
        "status": "complete independent human proof of the explicitly stated original-data implication",
        "depends_on": deps[cid], "quantifier_scope": scopes[cid],
        "proof_location": {"file": "joint_harmonic_io/main.tex", "label": "claim:" + cid,
                           "line_start": a + 1, "line_end": z, "sha256": sha(block), "bytes": len(block)},
        "source_ids": maps[cid], "sources": [sources[s] for s in maps[cid]],
    })

remaining = [
    {"id": "JIO_ORIGINAL_COMMON_DATA", "classification": "C", "status": "retained upstream original producer",
     "contract": "Produce the same selected Bundle/RealDat R with the actual toLevCh.Is(mu0), IsFam including the literal coefficient tie, IsModels, thP_omegaP and thP_vP, together with the original weak stored choice if its strong stored ioP is desired. JIO19 is universal on those supplied predicates and does not construct R or replace its fields.",
     "source_ids": ["actual_family_Is","actual_models_Is","level_character_Is","actual_weil_family","actual_vacuum_family","stored_io_weak_law"],
     "not_new_independent_top_level_obligation": True},
    {"id": "JIO_ACTUAL_BOUNDEDNESS_TARGET_VOLUME", "classification": "C", "status": "retained analytic producer outside simultaneous io",
     "contract": "For the SAME original target and actual extremal theta integral prove bounded HolForm and construct the actual finite target FinPair. No CuspRapidDecay published application is certified by this component.",
     "source_ids": ["remaining_boundedness","remaining_actual_volume","full_analytic_extension"],
     "not_new_independent_top_level_obligation": True},
    {"id": "JIO_POINTWISE_SOBOLEV_COMPLETION", "classification": "C", "status": "retained analytic producer outside simultaneous io",
     "contract": "For the same Hilbert image construct actual pointwise smooth automorphic representatives and all derivative identities, with original Sobolev-continuous point evaluation and required uniform growth, then install full IsMultMap/RestrictsTo. Companion regular-representation, central-scalar or cusp-closure implications do not by themselves construct these representatives.",
     "source_ids": ["remaining_pointwise_representative","remaining_pointwise_Sobolev","full_analytic_extension","base_theta_firing"],
     "not_new_independent_top_level_obligation": True},
]
prov = {
    "schema": "rh-human-component-provenance/1", "artifact_version": "0.36", "date": "2026-11-22",
    "component": "joint_harmonic_io", "source_commit": PIN, "main_tex_sha256": sha(tex),
    "metadata_builder": {"file": "build_metadata.py", "sha256": sha(Path(__file__).read_bytes()),
        "portable_invocation": "python3 build_metadata.py --source /path/to/pinned/checkout --human-root /path/to/reconstruction --peer-root /path/to/reconstruction"},
    "claims": claims, "source_inventory": list(sources.values()), "baseline_dependencies": inherited,
    "downstream_application_context": downstream, "remaining_producer_contracts": remaining,
    "validation": {"source_commit_verified": True, "pinned_blob_verified_files": len(cache),
        "source_ranges": len(sources), "claim_source_occurrences": sum(map(len, maps.values())),
        "all_source_ranges_exact": True, "all_inherited_claim_edges_explicit": True,
        "new_lean_build": False, "tex_validation": "See validation/validation.json; draft syntax/layout only."},
    "scope_note": "The full simultaneous original ioP producer and all polynomial theta values are reconstructed on exactly the source predicates. Common R existence, boundedness/actual target volume and pointwise Sobolev realization remain separate. Formal correctness is accepted; no new Lean replay.",
}
(HERE / "provenance.json").write_text(json.dumps(prov, indent=2, ensure_ascii=False) + "\n")
closure = {
    "schema": "rh-component-closure/1", "version": "0.36", "component": "joint_harmonic_io",
    "source_commit": PIN, "main_tex_sha256": sha(tex),
    "provenance_sha256": sha((HERE / "provenance.json").read_bytes()),
    "new_claims": list(titles), "claim_count": len(titles),
    "class_counts": {"A": 0, "B": len(titles), "C": 0, "D": 0},
    "all_new_claims_are_conditional_implications": True,
    "closed_subtargets": [
        {"id": "JIO_POLYNOMIAL_SUPPLIERS", "claims": list(titles)[:11],
         "contract": "Original factorial actions, minor signs, joint bottom, finite compact holomorphic extension, weight-only Gram transfer and full original LowT operators; no unnamed Fock or intertwiner producer retained."},
        {"id": "JIO_PARAMETER_FREE_IO", "claims": ["JIO12"], "incoming_peer_claims": ["CFB5","CFB6"],
         "contract": "Entire original exists_io_poly on exact CoefMapTie and weight/rank hypotheses, both polynomial covariances, literal Delta at original unit inputs."},
        {"id": "JIO_ACTUAL_COMPACT_ACTION", "claims": ["JIO13","JIO14","JIO15","JIO16","JIO17","JIO18"],
         "contract": "Stored theta/Fock vacuum; original infinity exponents for all t; actual compact Weil action with exact determinant scalar and every polynomial. No extra IsEtaTilde universal uniqueness premise."},
        {"id": "JIO_SIMULTANEOUS_ORIGINAL_IO", "claims": ["JIO19"], "incoming_peer_claims": ["CFB13"],
         "contract": "ONE R satisfying hLev,hFam,hModels,thP_omegaP,thP_vP implies thP_pt_theta AND forall i exists ONE io_i forall t IsIoW on the same original objects. Existing OrZero PIoP activates the stored map."},
    ],
    "selected_route_effect": {
        "original_parent_node": "BASE_THETA_CUSPIDAL_EXTENSION",
        "closed_residue": "One original io_i satisfying IsIoW for EVERY parameter t, plus original thP_pt_theta.",
        "parent_status_after_this_component": "remains C on explicit remaining analytic producers and common-data inputs",
        "new_threshold": False, "new_independent_original_datum": False,
        "one_io_before_all_parameters": True, "source_fully_checked_assumed": True,
    },
    "same_object_sufficient_rule": {
        "universals": "For every original D,A,Ks and every original R:RealDat D A Ks.",
        "inputs": ["R.toLevCh.Is(A.mu0)","R.IsFam","R.IsModels","R.thP_omegaP","R.thP_vP"],
        "outputs": ["R.thP_pt_theta","forall i exists io_i forall t IsIoW(R.theta,R.MW(i,sg0),R.cV(i),R.omegaP(i,t),R.ptP(i,t),Delta(i),io_i)"],
        "stored_activation": "Add only the already stored R.tw_ioP; OrZero's first implication yields R.thP_ioP. No equality of the newly constructed map and the stored map is claimed.",
        "no_extra_producers_inside_rule": True,
    },
    "retained_producers": remaining,
    "not_claimed": ["Unconditional existence of the selected Bundle/RealDat or its coefficient/model/Weil packet",
        "Full smooth cuspidal extension to Wall or actual Sobolev-continuous MMap",
        "Actual boundedness or target FinPair construction",
        "Global field/rational test/readings production",
        "A primary-source published rapid-decay certificate",
        "A new Lean build or RH/GRH conclusion"],
}
(HERE / "closure.json").write_text(json.dumps(closure, indent=2, ensure_ascii=False) + "\n")
loc = [
    "JIO source locators — v0.36", "Pin: " + PIN,
    "Inclusive ranges; file and range SHA256 are checked against pinned git blobs.",
    "No Lean replay. Source theorem names are locators, not substitutes for human proofs.", "",
]
for cid in titles:
    loc.append(cid + ": " + titles[cid])
    loc.append("  Proof dependencies: " + (", ".join(deps[cid]) or "none beyond the stated ordinary background and inputs"))
    for sid in maps[cid]:
        s = sources[sid]
        loc += [f"  {sid}: {s['path']}:{s['line_start']}–{s['line_end']} [{s['declaration'].strip()}]",
                "    file_sha256=" + s["file_sha256"] + " range_sha256=" + s["range_sha256"],
                "    " + s["url"]]
    loc.append("")
(HERE / "source_locators.txt").write_text("\n".join(loc) + "\n")
print(json.dumps({"claims": len(claims), "source_ranges": len(sources), "pinned_files": len(cache),
                  "claim_source_occurrences": sum(map(len, maps.values())),
                  "main_sha256": sha(tex), "provenance_sha256": sha((HERE / "provenance.json").read_bytes()),
                  "closure_sha256": sha((HERE / "closure.json").read_bytes())}, indent=2))
