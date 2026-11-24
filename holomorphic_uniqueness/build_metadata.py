#!/usr/bin/env python3
"""Rebuild HCU source and human-proof certificates without running Lean.

Portable usage:
  python3 build_metadata.py --source /path/to/pinned/checkout --human-root /path/to/reconstruction

Ranges are inclusive and their hashes include the original line endings.
The inherited TAE packet is recorded only as a downstream application context;
all HCU1--HCU20 proofs are independent apart from their listed HCU edges.
"""
from pathlib import Path
import argparse
import hashlib
import json
import re
import subprocess

HERE = Path(__file__).resolve().parent
DEFAULT_HUMAN = HERE.parent if (HERE.parent / "theta_extension").exists() else HERE.parent.parent / "reconstruction_v034"
parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument("--source", type=Path, default=HERE.parent.parent / "lean_source")
parser.add_argument("--human-root", type=Path, default=DEFAULT_HUMAN)
args = parser.parse_args()
SOURCE = args.source.resolve()
HUMAN = args.human_root.resolve()
PIN = "7cbf7a0c32fca1badf05931879a37c3f8a2b03b4"
REPO = "https://github.com/CocoSgt/riemann-hypothesis-lean"
sha = lambda b: hashlib.sha256(b).hexdigest()
assert subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=SOURCE, text=True).strip() == PIN
decl = re.compile(r"^(?:(?:private|protected|noncomputable|unsafe)\s+)*(?:def|abbrev|theorem|lemma|structure|class|instance)\s+")
cache = {}
sources = {}


def add(sid, path, anchor, stop=None, role="Exact original definition, contract, or source argument reconstructed independently"):
    path = "src/" + path
    if path not in cache:
        b = (SOURCE / path).read_bytes()
        assert b == subprocess.check_output(["git", "show", PIN + ":" + path], cwd=SOURCE), path
        cache[path] = b, b.decode().splitlines(keepends=True)
    b, lines = cache[path]
    hits = [i for i, line in enumerate(lines) if anchor in line]
    assert len(hits) == 1, (sid, path, anchor, hits)
    a = hits[0]
    if stop:
        z = next(i for i in range(a + 1, len(lines)) if stop in lines[i])
    else:
        z = next((i for i in range(a + 1, len(lines)) if decl.match(lines[i])), len(lines))
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
DP = D + "Proofs/DivisorProofs/"
IW = D + "Proofs/IwasawaDecomposition/"
IR = "Formalism/LocalToGlobal/IndefiniteReal/"
BT = "Formalism/LocalToGlobal/BesselHermitianTheta/"
HDS = D + "BlockTheory/TwistedDiscreteSeries/"
DEF = D + "Definitions/Divisors/IsSmoothVector.lean"
UPQ = "Formalism/PeriodIntegrals/UpqRep.lean"
RESIDUAL = "Retained producer or consumer boundary; this component does not claim its independent production"

for sid, anchor in [
    ("frame_domain", "def frDom "), ("upper_group", "def UpT "),
    ("original_frame", "def OrthFr "), ("product_unitary", "def UG "),
    ("product_domain", "def frDoms "), ("holomorphic_section", "def HolSec "),
    ("holomorphic_type", "def HolFn "), ("real_lie", "def lieH "),
    ("smooth_function", "def SmFn "), ("real_derivative", "def der "),
    ("real_involution", "def conjH "), ("complex_derivative", "def derC "),
    ("borel_killed", "def KilledFn "), ("original_torus", "def torEl "),
    ("torus_character", "def torCh "), ("complex_derived_action", "def dRepC "),
    ("holomorphic_shape", "def HolShape "), ("integer_weight", "def WtIs "),
    ("adelic_holomorphic", "def HolAd "), ("bounded_holomorphic_form", "structure HolForm "),
    ("finite_pair", "structure FinPair "), ("quotient_measure", "def nuQ "),
    ("original_representative", "def Repr "), ("regular_representation", "structure IsReg "),
    ("central_cuspidality", "def ZCusp "),
]:
    add(sid, DEF, anchor)
for sid, anchor in [("leading_minor", "def lminor "), ("signature_sign", "def sgn "), ("partial_signature", "def psgn ")]:
    add(sid, "ReciprocityTheory/ReductiveGroups/ArithmeticGeometry/FundamentalDomains/Signature.lean", anchor)

GS = DP + "SmoothGramSchmidtIndefiniteHermitianFrames.lean"
for sid, anchor in [
    ("gram_diagonalization", "theorem Lm_conj_diag "), ("pivot_ratio", "theorem lminor_succ "),
    ("pivot_sign", "theorem diag_pos "), ("source_factor", "def fac "),
    ("factor_spec", "theorem fac_spec "), ("factor_smooth", "theorem contDiffOn_fac "),
    ("smooth_frame_factor", "theorem smooth_gramSchmidt "),
]:
    add(sid, GS, anchor)
DOM = DP + "NegativeFrameDomainProductOpenPreconnectedStable.lean"
for sid, anchor in [
    ("triangular_domain_stability", "theorem mul_upT_mem "),
    ("unitary_domain_stability", "theorem unitary_mul_mem "),
    ("domain_open", "theorem isOpen_frDom "),
    ("domain_connected", "theorem isPreconnected_frDom "),
    ("domain_contract", "theorem GlobalTheory.HolDict.frDoms_open_preconnected_stable "),
]:
    add(sid, DOM, anchor)
UNIQ = DP + "HolomorphicTypeEqZeroOfTorusLawAtOne.lean"
for sid, anchor in [
    ("lower_disc", "def loP "), ("lu_map", "def luMap "),
    ("lu_derivative", "lemma luMap_strict "), ("local_zero", "lemma local_zero "),
    ("global_zero", "theorem eq_zero_of_torus_law "),
]:
    add(sid, UNIQ, anchor)
add("borel_tangent_split", DP + "HolomorphicTypeOfSmoothBorelKilled.lean", "lemma decomp ")
add("borel_holomorphic_core", DP + "HolomorphicTypeOfSmoothBorelKilled.lean", "lemma core ")
add("holomorphic_of_borel", DP + "HolomorphicTypeOfSmoothBorelKilled.lean", "theorem holFn_of_killed ")
add("borel_of_holomorphic", DP + "SmFnAndKilledFnOfHolFn.lean", "theorem GlobalTheory.HolDict.smFn_and_killedFn_of_holFn ")
add("integrated_torus", DP + "TorusLawOfKilled.lean", "theorem torus_law_of_killed ")
add("bounded_holomorphic_integral", DP + "IntegralHolomorphicTypeFamilyHolomorphicType.lean", "theorem holFn_integral ")

for sid, anchor in [
    ("compact_half_sum", "def rhoC "), ("noncompact_half_sum", "def rhoN "),
    ("hc_parameter", "def IsHCParam "), ("lowest_weight", "def lowK "),
    ("unitary_representation", "def IsURepOn "), ("irreducibility", "def IsIrredOn "),
    ("torus_weight", "def IsWtOn "), ("compact_dominance", "def CDom "),
    ("compact_stability", "def IsKStableOn "), ("compact_type", "def IsKTypeOf "),
    ("vogan_norm", "def vNormSq "), ("discrete_series", "def IsDS "),
    ("full_lowest_supremum", "def lowKSub "),
]:
    add(sid, UPQ, anchor)
add("smooth_vector", BT + "TiedType.lean", "def SmoothVec ")
add("real_derived_action", BT + "TiedType.lean", "def dRep ")
add("sobolev_two_contract", BT + "TiedType.lean", "def Sobolev₂ ", role=RESIDUAL)
add("model", IR + "ScalarOnPartsFull.lean", "structure DSModel ")
add("model_action", IR + "ScalarOnPartsFull.lean", "def DSModel.rep ")
add("model_smooth_span", IR + "ScalarOnPartsFull.lean", "def DSModel.sm ")
add("multiplicity_map_contract", IR + "ScalarOnPartsFull.lean", "structure IsMultMap ", role=RESIDUAL)
for sid, anchor in [
    ("negative_count", "def nNeg "), ("reverse_negative", "def revNeg "),
    ("negative_first_arrangement", "def arr "), ("negative_count_shape", "theorem nNeg_shape "),
    ("reverse_negative_shape", "theorem revNeg_shape "), ("reverse_arrangement", "theorem revNeg_arr "),
    ("extremal_weight", "def extWt "), ("extremal_vector", "def IsExtVec "),
    ("full_lowest_smooth", "def LowSm "), ("actual_base_frame", "def x0Mat "),
]:
    add(sid, IR + "ExistsChosenExtremalVector.lean", anchor)
add("full_lowest_irreducible", HDS + "HolomorphicLowestType.lean", "def LowIrr ")
add("rank_signature_sum", HDS + "HolomorphicLowestType.lean", "theorem pW_add_qW ")
add("actual_basis", IR + "LinksDefs.lean", "def onb ")
add("actual_lowest_intersection", IR + "LinksDefs.lean", "def lowT ")

LOW = IW + "HolomorphicDiscreteSeriesLowestKTypeSmoothIrredu.lean"
for sid, anchor in [
    ("coefficient_smooth", "theorem smFn_coef "), ("coefficient_derivative", "theorem derC_coef "),
    ("orthogonal_uniqueness", "theorem eq_zero_of_orth "), ("weight_integrality", "theorem wt_int "),
    ("compact_extremal_existence", "theorem exists_ext_mem "), ("actual_torus_weight", "theorem torus_wt "),
    ("whole_lowest_producer", "theorem lowSm_and_lowIrr "),
]:
    add(sid, LOW, anchor)
SEED = IW + "ExistsLowestKTypeLeSmoothVectors.lean"
for sid, anchor in [
    ("compact_bump", "theorem exists_bump "), ("garding_smooth", "theorem garding_smooth "),
    ("smooth_compact_copy", "theorem exists_smooth_ktype "), ("smooth_lowest_seed", "theorem exists_lowK_le_sm "),
]:
    add(sid, SEED, anchor)
add("smooth_subspace", DP + "SmoothVectorsSubspaceStableSobolevFormDeriv.lean", "theorem smoothVec_basic ")
DER = DP + "ComplexifiedDerivedActionIsLieAction.lean"
for sid, anchor in [
    ("complex_action_linearity", "theorem dRepC_lin "), ("complex_action_bracket", "theorem dRepC_bracket "),
    ("derived_covariance", "theorem rep_dRepC "), ("derived_adjoint", "theorem inner_dRepC "),
    ("complex_action_contract", "theorem main "),
]:
    add(sid, DER, anchor)
COMPACT = DP + "ExistsCompactTypeInCompactStableSubmodule.lean"
for sid, anchor in [
    ("compact_highest_extraction", "theorem exists_highest "),
    ("compact_minimal_subspace", "theorem exists_minimal "),
    ("compact_projection", "theorem proj_comm "),
    ("compact_type_extraction", "theorem exists_kType "),
]:
    add(sid, COMPACT, anchor)
CROOT = DP + "ExtremalLowestKtypeKilledByCompactRoots.lean"
for sid, anchor in [
    ("weight_projection", "theorem isWtOn_proj "), ("compact_weight_orthogonality", "theorem orth_of_not_cdom "),
    ("diagonal_derived_weight", "theorem dRepC_diag "), ("derived_root_weight", "theorem isWtOn_root "),
    ("compact_extremal_killed", "theorem extremal_killed "),
]:
    add(sid, CROOT, anchor)
NROOT = DP + "LowestKtypeHolomorphicKilledByLoweringRoots.lean"
for sid, anchor in [
    ("vogan_strict_inequality", "lemma vNormSq_lt "), ("compact_dominant", "lemma dominant_of_isKTypeOf "),
    ("finite_stable_supremum", "lemma exists_fin_stable "), ("full_supremum_weight", "lemma cdom_of_inner_ne "),
    ("noncompact_lowest_killed", "theorem lowK_killed "),
]:
    add(sid, NROOT, anchor)
add("source_borel_extremal", DP + "BaseFrameBorelActsExtremalVectorByWeight.lean", "theorem borel_extVec ")
add("frame_smoothness", DP + "BaseFrameBorelActsExtremalVectorByWeight.lean", "theorem smooth_conj ")
add("actual_model_representation", DP + "DiscreteSeriesModelUnitaryIrreducibleOrthonormal.lean", "theorem model_rep ")

add("infinite_embedding", "Formalism/SharpRestriction/GlobalSchurBounds/StandardLattice.lean", "def IsInfEmb ")
for sid, anchor in [
    ("finite_subgroup", "def GfC "), ("infinite_subgroup", "def GinfC "),
    ("infinite_family", "def IsInfFam "), ("one_place_contract", "def IsAtTau "),
    ("automorphic_contract", "structure IsAutFun "), ("right_translate", "def rTr "),
]:
    add(sid, BT + "IsAutFunDef.lean", anchor)
REAL = D + "Proofs/HeightProofs/AdelicUnitaryRealPointsStructureRealPlaces.lean"
for sid, anchor in [
    ("infinite_embedding_unique", "theorem infEmb_unique "),
    ("original_cm_type", "theorem tauE_cm "), ("original_real_points", "theorem realPoints "),
    ("evaluated_gram_hermitian", "theorem gramAt_herm "),
    ("evaluated_gram_nonsingular", "theorem gramAt_unit "),
]:
    add(sid, REAL, anchor)
TENSOR = D + "Proofs/UnitaryExistence/InfAdeleTensorBijective.lean"
for sid, anchor in [
    ("infinite_tensor_values", "theorem hom_tmul "), ("imaginary_generator", "theorem exists_delta "),
    ("cm_tensor_bijection", "theorem infAdele_tensor_bijective "),
]:
    add(sid, TENSOR, anchor)
add("original_archimedean_lift", DP + "ExistsArchimedeanLiftUnitaryGroupProduct.lean", "theorem exists_real_lift ")
add("actual_coefficient_holomorphic", DP + "ExtremalVectorMatrixCoeffHolomorphicType.lean", "theorem holFn_coef_extVec ")
add("representative_null_transfer", DP + "BoundedAutomorphicHasRepresentative.lean", "theorem ae_up ")
add("representative_properties", DP + "BoundedAutomorphicHasRepresentative.lean", "theorem repr_properties ")
add("two_coefficient_proportionality", DP + "L2MatrixCoeffBoundedHolomorphicFormEqExtremalVec.lean", "lemma eq_const_mul ")
add("original_l2_coefficient", DP + "L2MatrixCoeffBoundedHolomorphicFormEqExtremalVec.lean", "theorem GlobalTheory.HolDict.inner_reg_eq_coef_extremal ")
GRAM = DP + "ExistsEquivariantMultilinearOfMatrixCoeffEqUnita.lean"
add("gram_vector", GRAM, "theorem exists_vector_of_inner_eq_prod ")
add("gram_multilinear", GRAM, "theorem exists_continuousMultilinearMap_of_inner_eq_prod ")
add("gram_equivariant", GRAM, "theorem exists_equivariant_multilinear_of_matrixCoeff_eq ")
BACK = DP + "BoundedHolomorphicFormEqMultiplicitySpaceValue.lean"
add("actual_hilbert_map_abstract", BACK, "theorem exists_map_abs ")
add("finite_eigenclass", BACK, "theorem eig_class ")
add("actual_hilbert_map", BACK, "theorem exists_map ")
add("full_multiplicity_extension", BACK, "theorem exists_multMap ", role=RESIDUAL)
add("point_evaluation_continuity", BACK, "theorem cont_value ", role=RESIDUAL)
PACKET = HDS + "UniformModerateGrowthLevel.lean"
for sid, anchor in [
    ("negative_lie_block", "def pMinus "), ("lowest_multilinear", "abbrev KMap "),
    ("adelic_smoothness", "def IsSmoothFn "), ("original_cusp_packet", "structure IsHolCuspKMap "),
]:
    add(sid, PACKET, anchor)
add("full_holomorphic_extension_contract", PACKET, "def HolExtend ", role=RESIDUAL)
AD = IW + "HolomorphicTypeAtExtremalOfKEquivariantLoweringK.lean"
add("compact_evaluation_form", AD, "theorem exists_form ")
add("compact_differentiation", AD, "theorem rder_eq ")
add("packet_to_holomorphic", AD, "theorem holAd_of_kEquiv ")

add("base_infinite_choice", IR + "LinksDefs.lean", "def sgAt ")
add("base_infinite_choice_identity", IR + "LinksDefs.lean", "theorem sgAt_mk ")
add("base_coefficient_embedding", IR + "LinksDefs.lean", "abbrev sg0 ")
add("original_label_embedding", IR + "LinksDefs.lean", "def labE ")
add("original_label", IR + "LinksDefs.lean", "def lab ")
add("original_weight_at", IR + "LinksDefs.lean", "def kapAt ")
add("original_parameter_at", IR + "LinksDefs.lean", "def parAt ")
add("actual_ordered_models", IR + "LinksChar.lean", "abbrev models_order ")
add("original_models_contract", IR + "LinksChar.lean", "structure IsModels ")
add("signed_parameter_enumeration", BT + "DefsReal.lean", "def IsEnum ")
ENT = "Formalism/LocalToGlobal/HeckeThetaElements/IsHeckeElt.lean"
add("holomorphic_parameter_entry", ENT, "def holEnt ")
add("holomorphic_parameter_set", ENT, "def holPar ")
add("original_integral_weight", "Formalism/LocalToGlobal/HeckeThetaElements/DefsWt.lean", "def wtOf ")
add("fixed_parameter_identity", D + "Counterexamples/RotationExamples/OneLeAPlLast.lean", "theorem parAt_fixed ")
add("fixed_label_identity", D + "Counterexamples/RotationExamples/OneLeAPlLast.lean", "theorem labE_fixed ")
add("lowest_weight_count_identity", "Formalism/FormalDegreeBessel/FormalDegreeRatio/DSLowK.lean", "lemma dslowk_lowK_eq ")
add("lowest_weight_integral", "Formalism/FormalDegreeBessel/FormalDegreeRatio/DSLowK.lean", "theorem low_k_integrable_holds ")
add("actual_base_shape", IW + "FormsModelHolomorphicIntegralExtremalWeight.lean", "theorem holShape_fixed ")

add("remaining_boundedness", IW + "BoundedOfSmoothCuspidalUniformModerate.lean", "theorem bounded_of_smooth_unifModGrowth ", role=RESIDUAL)
add("published_predicate_not_certificate", D + "PublishedTheorems/AutomorphicForms₂/ExistsNormLeHeightPow.lean", "def CuspRapidDecay ", role=RESIDUAL)
add("remaining_target_volume", IW + "FiniteVolumeAdelicUnitaryQuotient.lean", "theorem finVol ", role=RESIDUAL)
add("remaining_regular_existence", DP + "RegularRepresentationOfFinitePair.lean", "theorem exists_isReg ", role=RESIDUAL)
add("remaining_smooth_representative", DP + "SmoothVectorAutomorphicDerivatives.lean", "theorem exists_smooth_repr ", role=RESIDUAL)
add("remaining_sobolev_growth", DP + "SobolevBoundForSmoothVectors.lean", "theorem pointwise_growth ", role=RESIDUAL)
add("remaining_central_finiteness", DP + "GelfandInvariantsActByScalarsHighestWeight.lean", "theorem gelfRep_scalar ", role=RESIDUAL)
add("remaining_cusp_closure", DP + "CuspidalityPreservedInClosure.lean", "theorem zcusp_of_mem_closure ", role=RESIDUAL)
add("original_io_contract", IR + "LinksChar.lean", "def IsIoW ", role=RESIDUAL)
add("simultaneous_io", IR + "LinksW.lean", "def PIoP ", role=RESIDUAL)
add("remaining_io_poly", IW + "ExistsLowestKTypeFockMapThetaVectors.lean", "theorem exists_io_poly ", role=RESIDUAL)
add("remaining_io_all_parameters", IW + "ExistsLowestKTypeFockMapThetaVectors.lean", "theorem exists_ioP ", role=RESIDUAL)
EXT = IW + "ExistsThetaLiftLinearMapCuspFormMultiplicity.lean"
add("remaining_full_extension", EXT, "theorem exists_extension ", role=RESIDUAL)
add("remaining_fires_at", EXT, "theorem firesAt ", role=RESIDUAL)

titles = {
    "HCU1": "Smooth triangular factor on the original negative-frame domain",
    "HCU2": "Openness, stability and path connectedness of the actual domain",
    "HCU3": "The literal local zero lemma",
    "HCU4": "Global coefficient uniqueness from the original torus law",
    "HCU5": "Both directions of the full smooth Borel--holomorphic dictionary",
    "HCU6": "Holomorphic type is preserved by bounded finite-measure integration",
    "HCU7": "Coefficient proportionality and the exact orthogonal-vector uniqueness",
    "HCU8": "Smooth derived calculus and a smooth copy of the original compact type",
    "HCU9": "Compact weight extraction, dominance and raising annihilation",
    "HCU10": "The strict Vogan-norm inequality with the required compact cone",
    "HCU11": "Noncompact lowering kills the full original lowest supremum",
    "HCU12": "Actual negative-first frames and full extremal Borel equations",
    "HCU13": "Full original LowSm and LowIrr with multiplicity one",
    "HCU14": "Original archimedean lift with the given IsInfFam coordinates",
    "HCU15": "Actual extremal model matrix coefficient has the required HolFn",
    "HCU16": "Original finite-quotient L2 representatives and translation identities",
    "HCU17": "Complete original extremal regular matrix-coefficient identity",
    "HCU18": "Exact Hilbert multilinear realization and original finite eigenlaws",
    "HCU19": "The original compact-equivariant lowering packet is holomorphic",
    "HCU20": "Same original base-model HolShape, integer weight, LowSm and LowIrr",
}
maps = {
    "HCU1": ["frame_domain", "original_frame", "upper_group", "leading_minor", "signature_sign", "partial_signature", "gram_diagonalization", "pivot_ratio", "pivot_sign", "source_factor", "factor_spec", "factor_smooth", "smooth_frame_factor"],
    "HCU2": ["product_domain", "product_unitary", "triangular_domain_stability", "unitary_domain_stability", "domain_open", "domain_connected", "domain_contract"],
    "HCU3": ["local_zero", "lower_disc", "lu_map", "lu_derivative", "upper_group"],
    "HCU4": ["global_zero", "holomorphic_section", "holomorphic_type", "original_torus", "torus_character"],
    "HCU5": ["smooth_function", "borel_killed", "real_lie", "real_derivative", "real_involution", "complex_derivative", "borel_tangent_split", "borel_holomorphic_core", "holomorphic_of_borel", "borel_of_holomorphic", "integrated_torus"],
    "HCU6": ["bounded_holomorphic_integral", "holomorphic_section", "holomorphic_type"],
    "HCU7": ["orthogonal_uniqueness", "two_coefficient_proportionality", "coefficient_smooth", "coefficient_derivative", "irreducibility"],
    "HCU8": ["smooth_vector", "real_derived_action", "smooth_subspace", "complex_action_linearity", "complex_action_bracket", "derived_covariance", "derived_adjoint", "complex_action_contract", "compact_bump", "garding_smooth", "smooth_compact_copy", "smooth_lowest_seed", "model_smooth_span"],
    "HCU9": ["torus_weight", "compact_dominance", "compact_stability", "compact_type", "full_lowest_supremum", "compact_highest_extraction", "compact_minimal_subspace", "compact_projection", "compact_type_extraction", "weight_projection", "compact_weight_orthogonality", "diagonal_derived_weight", "derived_root_weight", "compact_extremal_killed", "weight_integrality", "compact_dominant", "finite_stable_supremum", "full_supremum_weight"],
    "HCU10": ["compact_half_sum", "noncompact_half_sum", "hc_parameter", "lowest_weight", "vogan_norm", "vogan_strict_inequality"],
    "HCU11": ["discrete_series", "full_lowest_supremum", "noncompact_lowest_killed", "derived_adjoint", "finite_stable_supremum", "full_supremum_weight"],
    "HCU12": ["model", "model_action", "holomorphic_shape", "integer_weight", "actual_basis", "negative_count", "reverse_negative", "negative_first_arrangement", "negative_count_shape", "reverse_negative_shape", "reverse_arrangement", "extremal_weight", "extremal_vector", "actual_base_frame", "source_borel_extremal", "frame_smoothness", "actual_model_representation", "compact_extremal_existence", "actual_torus_weight"],
    "HCU13": ["whole_lowest_producer", "full_lowest_smooth", "full_lowest_irreducible", "full_lowest_supremum", "model_smooth_span", "compact_type", "actual_model_representation"],
    "HCU14": ["infinite_embedding", "infinite_family", "one_place_contract", "finite_subgroup", "infinite_subgroup", "infinite_embedding_unique", "original_cm_type", "original_real_points", "evaluated_gram_hermitian", "evaluated_gram_nonsingular", "infinite_tensor_values", "imaginary_generator", "cm_tensor_bijection", "original_archimedean_lift"],
    "HCU15": ["actual_coefficient_holomorphic", "extremal_vector", "integer_weight", "complex_derived_action", "actual_torus_weight"],
    "HCU16": ["finite_pair", "regular_representation", "quotient_measure", "original_representative", "right_translate", "representative_null_transfer", "representative_properties", "finite_eigenclass"],
    "HCU17": ["original_l2_coefficient", "bounded_holomorphic_form", "adelic_holomorphic", "representative_properties", "two_coefficient_proportionality"],
    "HCU18": ["gram_vector", "gram_multilinear", "gram_equivariant", "actual_hilbert_map_abstract", "actual_hilbert_map", "finite_eigenclass"],
    "HCU19": ["lowest_multilinear", "actual_lowest_intersection", "negative_lie_block", "adelic_smoothness", "original_cusp_packet", "compact_evaluation_form", "compact_differentiation", "packet_to_holomorphic"],
    "HCU20": ["actual_base_shape", "base_infinite_choice", "base_infinite_choice_identity", "base_coefficient_embedding", "original_label_embedding", "original_label", "original_weight_at", "original_parameter_at", "actual_ordered_models", "original_models_contract", "signed_parameter_enumeration", "holomorphic_parameter_entry", "holomorphic_parameter_set", "original_integral_weight", "fixed_parameter_identity", "fixed_label_identity", "rank_signature_sum", "lowest_weight_count_identity", "lowest_weight_integral"],
}
deps = {
    "HCU1": [], "HCU2": ["HCU1"], "HCU3": [],
    "HCU4": ["HCU1", "HCU2", "HCU3"],
    "HCU5": ["HCU1", "HCU2"], "HCU6": ["HCU1", "HCU2"],
    "HCU7": ["HCU4", "HCU5"], "HCU8": ["HCU5"],
    "HCU9": ["HCU8"], "HCU10": [],
    "HCU11": ["HCU8", "HCU9", "HCU10"],
    "HCU12": ["HCU8", "HCU9", "HCU11"],
    "HCU13": ["HCU7", "HCU8", "HCU12"],
    "HCU14": [],
    "HCU15": ["HCU5", "HCU8", "HCU12"],
    "HCU16": [],
    "HCU17": ["HCU6", "HCU7", "HCU14", "HCU15", "HCU16"],
    "HCU18": ["HCU14", "HCU16", "HCU17"],
    "HCU19": ["HCU5", "HCU12", "HCU13", "HCU14"],
    "HCU20": ["HCU8", "HCU12", "HCU13", "HCU14"],
}
scopes = {
    "HCU1": "Every supplied OrthFr on the actual frDom, including n=0; exists a real-smooth upper factor with original unitary factorization. The source asks for an existential factor, not equality to its auxiliary fac definition.",
    "HCU2": "Every finite product of the actual frame domains under OrthFr; same H, x0 and q; open, nonempty, path connected and stable under the original left unitary and right upper actions.",
    "HCU3": "Exactly local_zero: ambient Q differentiable on a neighborhood of 1, its stated upper-stable zero set, the original diagonal conjugation equality on the neighborhood, and Q(1)=0.",
    "HCU4": "Every original HolFn under OrthFr with separate exact left torus character and value zero at 1; conclusion on the entire original UG.",
    "HCU5": "Under OrthFr and integer w, original SmFn plus original KilledFn iff original HolFn; the proof differentiates on the actual real Lie group and descends through the exact diagonal-unitary intersection.",
    "HCU6": "Every finite measure, every family of original HolFn, one uniform bound on all UG, and pointwise AE strong measurability; includes negative integer characters.",
    "HCU7": "Proportionality for same exact HolFn and torus law; for the vector consequence the original unitary irreducible action, smooth nonzero Borel eigenvector and possibly nonsmooth orthogonal torus eigenvector are the exact inputs.",
    "HCU8": "Complete unitary strongly continuous representation of the nondegenerate Hermitian unitary group; original exponential-word SmoothVec. Any finite compact irreducible subspace gives an isomorphic smooth compact subspace, without claiming the entire lowest supremum is already smooth.",
    "HCU9": "Finite compact-stable subspaces and the actual algebraic supremum of all IsKTypeOf subspaces; no multiplicity-one or full-lowest finite-dimensionality assumption.",
    "HCU10": "Ordered sign blocks, strictly decreasing HC parameter, compact-dominant Lambda and mu, and Lambda-mu equal to one cross-block root plus a nonnegative integral compact-root cone.",
    "HCU11": "Literal IsDS and ordered IsHCParam, every smooth vector in the full lowKSub, every negative-row/positive-column root; lower action vanishes before multiplicity one is used.",
    "HCU12": "The same DSModel with HolShape; original frame inverse, arr and revNeg; each supplied IsExtVec has all required Borel equations, and a smooth unit extremal tuple exists.",
    "HCU13": "Every DSModel satisfying its actual HolShape: all original lowest compact subspaces coincide with one smooth subspace. This closes full LowSm and LowIrr, not merely a selected copy.",
    "HCU14": "Original D, V and supplied IsInfFam theta; all exists_real_lift fields: exact real evaluation inverse and continuity, atTau, archM in UG for every adele, finite/infinite decomposition and commutation, and Hermitian nonsingular gramAt. No replacement theta is chosen.",
    "HCU15": "Same M, HolShape, WtIs and IsExtVec; original product coefficient has HolFn, the exact left torus law and value 1.",
    "HCU16": "Same given FinPair and IsReg on the original quotient; existence for continuous bounded rational-invariant functions and exact globally AE Repr identities. FinPair and IsReg existence remain inputs.",
    "HCU17": "Literal inner_reg_eq_coef_extremal for original D, theta, V, S, M, w, v, mu, fundamental domain, rho, HolForm and Repr. Boundedness and target finite volume remain explicitly supplied.",
    "HCU18": "Complete unitary irreducible factor spaces with unit vectors, a complete unitary target and the exact Gram coefficient; obtains the full continuous Hilbert multilinear map. Original finite eigenlaws and actual atTau are preserved. No pointwise automorphic MMap is inferred.",
    "HCU19": "Same model and infinite family, original lowest KMap, all-values smoothness, literal KEquiv and all-values original pMinus annihilation; concludes actual HolAd at every supplied unit extremal tuple.",
    "HCU20": "Every original RealDat R with its models_order field, every i, and only sg0 identified with embLL using R.hv0; actual enumeration formulas yield HolShape, integral WtIs and full LowSm/LowIrr before any parameter t.",
}
assert set(titles) == set(maps) == set(deps) == set(scopes)

inherited = []
for rel, ids, role in [
    ("theta_extension/main.tex", ["TAE12", "TAE13"],
     "Downstream application context only: HCU20 discharges the retained LowSm/LowIrr inputs, and HCU19 consumes its original lowering packet; not an incoming proof dependency of an HCU claim."),
]:
    b = (HUMAN / rel).read_bytes()
    slines = b.splitlines(keepends=True)
    blocks = []
    for cid in ids:
        a = next(i for i, line in enumerate(slines) if line.strip() == ("% BEGIN " + cid).encode())
        z = next(i for i, line in enumerate(slines) if line.strip() == ("% END " + cid).encode()) + 1
        block = b"".join(slines[a:z])
        blocks.append({"id": cid, "line_start": a + 1, "line_end": z, "sha256": sha(block), "bytes": len(block)})
    inherited.append({"file": rel, "sha256": sha(b), "file_sha256": sha(b), "role": role, "claims": blocks})

tex = (HERE / "main.tex").read_bytes()
lines = tex.splitlines(keepends=True)
claims = []
for cid, title in titles.items():
    a = next(i for i, line in enumerate(lines) if line.strip() == ("% BEGIN " + cid).encode())
    z = next(i for i, line in enumerate(lines) if line.strip() == ("% END " + cid).encode()) + 1
    block = b"".join(lines[a:z])
    claims.append({
        "id": cid, "title": title, "introduced_in": "0.35", "classification": "B",
        "status": "complete independent human proof of the explicitly stated implication",
        "depends_on": deps[cid], "quantifier_scope": scopes[cid],
        "proof_location": {"file": "holomorphic_uniqueness/main.tex", "label": "claim:" + cid,
                           "line_start": a + 1, "line_end": z, "sha256": sha(block), "bytes": len(block)},
        "source_ids": maps[cid], "sources": [sources[s] for s in maps[cid]],
    })

remaining = [
    {"id": "HCU_COMMON_IO", "classification": "C", "status": "retained simultaneous original producer",
     "contract": "For each original i, exists one io_i, forall t, IsIoW on the same R.theta, MW(i,sg0), cV(i), omegaP(i,t), ptP(i,t), Delta(i). The same polynomial normalization and two intertwining laws must activate the stored OrZero PIoP. HCU does not construct io.",
     "source_ids": ["original_io_contract", "simultaneous_io", "remaining_io_poly", "remaining_io_all_parameters"],
     "not_new_independent_top_level_obligation": True},
    {"id": "HCU_BOUNDEDNESS_AND_TARGET_VOLUME", "classification": "C", "status": "retained actual analytic producer, not a checked published application",
     "contract": "The original smooth cuspidal uniformly moderate extremal function must be bounded, and a finite target FinPair must be produced. CuspRapidDecay is only a source predicate here; no primary published theorem and full hypothesis match are claimed.",
     "source_ids": ["remaining_boundedness", "published_predicate_not_certificate", "remaining_target_volume", "finite_pair"],
     "not_new_independent_top_level_obligation": True},
    {"id": "HCU_REGULAR_REPRESENTATION_EXISTENCE", "classification": "B", "status": "retained moderate measure-theoretic construction",
     "contract": "From the given target FinPair construct IsReg on the same L2 quotient, including the globally AE value law, unitarity and strong continuity. HCU16--18 use supplied IsReg; they do not assert this separate source producer.",
     "source_ids": ["remaining_regular_existence", "regular_representation"],
     "not_new_independent_top_level_obligation": True},
    {"id": "HCU_POINTWISE_AUTOMORPHIC_REALIZATION", "classification": "C", "status": "retained global analytic completion after the proved Hilbert map",
     "contract": "Convert the same Hilbert multilinear image into pointwise smooth automorphic representatives with every derivative identity, Sobolev-continuous evaluation, uniform growth, central finiteness and preserved genuine cusp integrals in the closed orbit span. Then prove IsMultMap and exact RestrictsTo on all original lowest tensors. HCU18 only gives the Hilbert-valued map.",
     "source_ids": ["remaining_smooth_representative", "remaining_sobolev_growth", "remaining_central_finiteness", "remaining_cusp_closure", "point_evaluation_continuity", "full_multiplicity_extension", "multiplicity_map_contract", "full_holomorphic_extension_contract", "remaining_full_extension", "remaining_fires_at"],
     "not_new_independent_top_level_obligation": True},
]
provenance = {
    "schema": "rh-human-component-provenance/1", "artifact_version": "0.35", "date": "2026-11-22",
    "component": "holomorphic_uniqueness", "source_commit": PIN, "main_tex_sha256": sha(tex),
    "metadata_builder": {"file": "build_metadata.py", "sha256": sha(Path(__file__).read_bytes()),
                         "portable_invocation": "python3 build_metadata.py --source /path/to/pinned/checkout --human-root /path/to/reconstruction"},
    "claims": claims, "source_inventory": list(sources.values()), "baseline_dependencies": inherited,
    "remaining_producer_contracts": remaining,
    "validation": {"source_commit_verified": True, "pinned_blob_verified_files": len(cache),
                   "source_ranges": len(sources), "claim_source_occurrences": sum(len(v) for v in maps.values()),
                   "all_source_ranges_exact": True, "new_lean_build": False,
                   "tex_validation": "See validation/validation.json; draft compilation is syntax validation only."},
    "scope_note": "Formal correctness is assumed. The entire local/global uniqueness, full original LowSm/LowIrr, exact coefficient identity and conditional Hilbert realization are reconstructed. Original weak-data existence, simultaneous io, target boundedness/volume and pointwise MMap completion remain separate.",
}
(HERE / "provenance.json").write_text(json.dumps(provenance, indent=2, ensure_ascii=False) + "\n")

closure = {
    "schema": "rh-component-closure/1", "version": "0.35", "component": "holomorphic_uniqueness",
    "source_commit": PIN, "main_tex_sha256": sha(tex),
    "provenance_sha256": sha((HERE / "provenance.json").read_bytes()),
    "new_claims": list(titles), "claim_count": len(titles),
    "class_counts": {"A": 0, "B": len(titles), "C": 0, "D": 0},
    "all_new_claims_are_conditional_implications": True,
    "closed_subtargets": [
        {"source_declaration": "smooth_gramSchmidt and frDoms_open_preconnected_stable", "proof": ["HCU1", "HCU2"]},
        {"source_declaration": "HolDict.Uniq.local_zero and eq_zero_of_torus_law", "proof": ["HCU3", "HCU4"]},
        {"source_declaration": "holFn_of_killed and smFn_and_killedFn_of_holFn", "proof": ["HCU5"]},
        {"source_declaration": "holFn_integral", "proof": ["HCU6"]},
        {"source_declaration": "eq_zero_of_orth", "proof": ["HCU7"]},
        {"source_declaration": "exists_lowK_le_sm, compact-type extraction, lowK_killed and borel_extVec", "proof": ["HCU8", "HCU9", "HCU10", "HCU11", "HCU12"]},
        {"source_declaration": "lowSm_and_lowIrr", "scope": "the entire original algebraic supremum, under actual HolShape", "proof": ["HCU13"]},
        {"source_declaration": "exists_real_lift", "scope": "all original fields, including finite/infinite decomposition, archM in UG for every adele and Hermitian nonsingular gramAt", "proof": ["HCU14"]},
        {"source_declaration": "holFn_coef_extVec", "proof": ["HCU15"]},
        {"source_declaration": "repr_properties", "scope": "same supplied FinPair and IsReg", "proof": ["HCU16"]},
        {"source_declaration": "inner_reg_eq_coef_extremal", "scope": "same bounded HolForm, FinPair, IsReg and Repr", "proof": ["HCU17"]},
        {"source_declaration": "exists_equivariant_multilinear_of_matrixCoeff_eq and BackForm.exists_map", "scope": "Hilbert map with full original finite eigenlaws; no pointwise MMap asserted", "proof": ["HCU18"]},
        {"source_declaration": "holAd_of_kEquiv", "proof": ["HCU19"]},
        {"source_declaration": "holShape_fixed", "scope": "only same R.MW(i,sg0), under original models_order", "proof": ["HCU20"]},
    ],
    "closed_prior_residues": [
        {"id": "TAE_FULL_LOWEST_TYPE", "proof": ["HCU13", "HCU20"], "scope": "same original base models on every supplied R with IsModels.order; no model replacement"},
        {"id": "TAE_HILBERT_REALIZATION", "status": "strict partial refinement",
         "closed": "exact coefficient identity and conditional continuous Hilbert multilinear map",
         "remaining": "same target boundedness, FinPair/IsReg existence and pointwise Sobolev-continuous automorphic MMap completion",
         "proof": ["HCU17", "HCU18"]},
    ],
    "sufficient_rules": [
        {"id": "HCU_ACTUAL_BASE_LOWEST", "kind": "same-object implication",
         "requires": ["one original RealDat R", "R.models_order"],
         "concludes": "forall i, HolShape(MW(i,sg0)), exists integral w_i with WtIs, and full LowSm/LowIrr on the same original model",
         "proof": ["HCU20"]},
        {"id": "HCU_ORIGINAL_HOLOMORPHIC_PACKET", "kind": "AND on one original R and one simultaneous io_i per i",
         "requires": ["all original TAE13 weak-data inputs on the same R", "forall i, exists one io_i, forall t, original IsIoW"],
         "concludes": "forall i,t,x, the literal original integral has the TAE13 IsHolCuspKMap packet and is HolAd at every chosen original unit extremal; no independent LowSm/LowIrr producer remains",
         "proof": ["TAE13", "HCU19", "HCU20"]},
        {"id": "HCU_BOUNDED_HILBERT_REALIZATION", "kind": "AND on the same target quotient, model, form and representative",
         "requires": ["original IsInfFam, HolShape, WtIs and IsExtVec", "original bounded HolForm", "same FinPair", "same IsReg"],
         "concludes": "exists original Repr and a continuous Hilbert multilinear map with its exact coefficient, atTau equivariance, closed orbit containment and every original finite eigenlaw",
         "proof": ["HCU14", "HCU15", "HCU16", "HCU17", "HCU18"]},
    ],
    "quantifiers": {
        "base_model": "forall i, same M_i=R.MW(i,sg0); sg0=embLL is proved, not chosen",
        "other_embeddings": "HolShape is not asserted for arbitrary coefficient embeddings",
        "io": "exists io_i, forall t; never weakened to forall t, exists io_(i,t)",
        "target_measure": "FinPair, IsReg and Repr use the same mu and fundamental domain",
        "family_threshold": "none introduced; all implications are pointwise on the original supplied data",
    },
    "remaining_producers": remaining, "new_unresolved_internal_suppliers": [], "new_D_obligations": [],
    "not_closed": ["original same-Bundle weak-data existence", "simultaneous ioP",
                   "actual target boundedness and finite volume", "IsReg existence",
                   "pointwise Sobolev-continuous IsMultMap on the full smooth spaces",
                   "full exists_extension, firesAt or exists_thetaMap",
                   "geometric reading, rational tests and RowsHold0_3", "complete human RH/GRH proof"],
    "new_lean_replay": False, "no_new_A_certificate": True,
}
(HERE / "closure.json").write_text(json.dumps(closure, indent=2, ensure_ascii=False) + "\n")
(HERE / "source_locators.txt").write_text("\n".join(
    [f"Source pin: {PIN}", f"Main TeX SHA256: {sha(tex)}", ""]
    + [f"{s['id']} | {s['declaration_anchor']}\n{s['path']}:{s['line_start']}-{s['line_end']}\n"
       f"file_sha256={s['file_sha256']}\nrange_sha256={s['range_sha256']}\nrole={s['role']}\n{s['url']}\n"
       for s in sources.values()]
))
print(json.dumps({"claims": len(claims), "source_files": len(cache), "source_ranges": len(sources),
                  "claim_source_occurrences": sum(len(v) for v in maps.values()),
                  "main_tex_sha256": sha(tex), "provenance_sha256": sha((HERE / "provenance.json").read_bytes()),
                  "closure_sha256": sha((HERE / "closure.json").read_bytes()),
                  "proof_hashes": {c["id"]: c["proof_location"]["sha256"] for c in claims}}, indent=2))
