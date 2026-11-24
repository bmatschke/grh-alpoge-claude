#!/usr/bin/env python3
"""Rebuild TAE source/proof certificates without running Lean.

Portable usage:
  python3 build_metadata.py --source /path/to/pinned/checkout --human-root /path/to/reconstruction

The human root contains canonical_weil/, base_theta/, finite_isotropic_average/
and constant_terms/.  Source files are checked byte-for-byte against pinned git
objects.  Line ranges are inclusive; range hashes include the exact line endings.
"""
from pathlib import Path
import argparse
import hashlib
import json
import re
import subprocess

HERE = Path(__file__).resolve().parent
DEFAULT_HUMAN = HERE.parent if (HERE.parent / "canonical_weil").exists() else HERE.parent.parent / "reconstruction_v033"
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
IW = D + "Proofs/IwasawaDecomposition/"
TO = D + "Proofs/TwistedOperators/"
DP = D + "Proofs/DivisorProofs/"
BT = "Formalism/LocalToGlobal/BesselHermitianTheta/"
IR = "Formalism/LocalToGlobal/IndefiniteReal/"
HDS = D + "BlockTheory/TwistedDiscreteSeries/"
LOCAL = IR + "LocalNewformFunction.lean"
LOWER = IW + "FockVectorMixedLaplacianKilledLoweringKilled.lean"
GROW = TO + "LintegralCompactLe.lean"
VAC = TO + "IsFockVacAtOfIsThetaAt.lean"
PACKET = HDS + "UniformModerateGrowthLevel.lean"
GEN = IW + "ExistsWeilDatumGeneratorRealOneParamGroup.lean"
EXT = IW + "ExistsThetaLiftLinearMapCuspFormMultiplicity.lean"
RESIDUAL = "Retained supplier or consumer boundary; not claimed independently closed by this component"

add("theta_contract", LOCAL, "structure IsThetaFunO ")
add("weil_contract", LOCAL, "structure IsWeilDatumO ")
add("heisenberg", LOCAL, "def heisO ")
add("hom_action", LOCAL, "def actO ")
add("kernel", LOCAL, "def thetaKO ")
add("oriented_pairing", LOCAL, "def hO ")
add("symplectic_form", LOCAL, "def symplO ")
add("half_phase", LOCAL, "def symplOH ")
add("real_line_contract", LOCAL, "def IsLineAt ")
add("real_line", LOCAL, "def lineAt ")
add("derivative", LOCAL, "def dRho ")
add("cartan_contract", LOCAL, "def IsCartanInv ")
add("complex_structure", LOCAL, "def cplxO ")
add("annihilation", LOCAL, "def annih ")
add("creation", LOCAL, "def crea ")
add("fock_scale", LOCAL, "def fockScale ")
add("scaled_creation", LOCAL, "def aPlus ")
add("vacuum_contract", LOCAL, "def IsFockVacAt ")
add("unit_map", LOCAL, "def unitMap ")
add("ordered_word", LOCAL, "def opPow ")
add("pure_tensor_linear", LOCAL, "def pureTensorL ")
add("all_creation", LOCAL, "def aPlusAll ")
add("polynomial_variable", LOCAL, "def varF ")
add("positive_minor", LOCAL, "def minorPlus ")
add("negative_minor", LOCAL, "def minorMinus ")
add("delta_place", LOCAL, "def deltaAt ")
add("delta_product", LOCAL, "def delta ")
add("place_model", LOCAL, "structure IsPlaceModel ")
add("theta_at", LOCAL, "def IsThetaAt ")
add("original_vector", IR + "DatumVec.lean", "def IsThPVecOf ")
add("pure_tensor_oriented", IR + "DatumVec.lean", "def pureTensorO ")
add("std_character", BT + "TiedWeil.lean", "def IsStdChar ")
add("inf_family", BT + "IsAutFunDef.lean", "def IsInfFam ")
add("lie_at", BT + "TiedSmooth.lean", "def lieAt ")
add("one_parameter", BT + "TiedSmooth.lean", "def oneP ")
add("right_derivative", BT + "TiedSmooth.lean", "def Rder ")
add("complex_parts", BT + "TiedSmooth.lean", "def conjAt ")
add("complex_derivative", BT + "TiedSmooth.lean", "def RderC ")
add("original_height", BT + "TiedSmooth.lean", "def normInf ")

add("oscillator_integral", IW + "ExistsOscillatorActionUnitaryPolynomialBound.lean", "theorem osc_eq ")
add("oscillator_derivative_source", IW + "ExistsOscillatorActionUnitaryPolynomialBound.lean", "theorem hasDerivAt_osc ",
    role="Source oscillator derivative route; TAE1 proves smoothness directly from the inherited Gaussian formula, without claiming the extra nOp+lambda normal form")
add("oscillator_bound_derivative_source", IW + "ExistsOscillatorActionUnitaryPolynomialBound.lean", "theorem exists_osc_bound_deriv ",
    role="Source upstream normal-form route, bypassed by the direct smooth-domain argument; not an exact closed contract")
add("continuous_character_derivative", IW + "WeilRepresentationOneParameterGenerator.lean", "theorem exists_hasDerivAt_char ")
add("translated_derivative_L2", IW + "HasDerivAtWeilRepRealOneParamAdelicPoint.lean", "theorem deriv_eq_of_norm ")
add("translated_derivative", IW + "HasDerivAtWeilRepRealOneParamAdelicPoint.lean", "theorem deriv_om ")
add("generator_ambient_extension", GEN, "theorem exists_extension ")
add("generator_commutator", GEN, "theorem comm_dRho ")
add("generator_exact", GEN, "theorem exists_generator ")
add("generator_contract", LOWER, "def IsGen ")

for sid, anchor in [
    ("sobolev_iter", "theorem sobolev_iter "),
    ("compact_integral_bound", "theorem lintegral_compact_le "),
    ("real_slice_measure", "theorem lintegral_real_le "),
    ("word_bound", "theorem words_bound "),
    ("derivative_preserves_theta", "theorem theta_dv "),
    ("derivative_preserves_level", "theorem dv_level "),
    ("sobolev_step", "theorem sobolev_step "),
    ("real_hom_action", "def mov "),
    ("covariant_derivative", "theorem dv_om "),
    ("height_comparison", "theorem norm_mov_le "),
    ("height_lower", "theorem one_le_normInf "),
    ("common_finite_level", "theorem uniform_level "),
    ("word_level", "theorem words_level "),
    ("cube_bound", "theorem cube_bound "),
    ("kernel_growth", "theorem thetaKO_growth "),
]:
    add(sid, GROW, anchor)
add("integral_domination", IW + "DefiniteThetaLiftContinuousInvariantHasDerivAt.lean", "theorem hasDerivAt_integral_of_cocompact ")
add("kernel_continuity_invariance", IW + "DefiniteThetaLiftContinuousInvariantHasDerivAt.lean", "theorem kernel_continuous_invariant ")
add("integral_derivative", IW + "DefiniteThetaLiftContinuousInvariantHasDerivAt.lean", "theorem lift_continuous_invariant_hasDerivAt ")
add("integral_growth", IW + "ThetaLiftDefiniteSmoothModerateGrowthAnnihilated.lean", "theorem lift_growth ")
add("integral_smooth_growth_killed", IW + "ThetaLiftDefiniteSmoothModerateGrowthAnnihilated.lean", "theorem lift_smooth_growth_killed ")
add("closed_derivatives_smooth", IW + "MemSmoothFunctionsOfClosedRightDerivatives.lean", "theorem mem_smFun_of_closed ")
add("source_measure", IR + "LinksDefs.lean", "def IsMeasDef ")
add("source_class_representatives", IR + "Bridge.lean", "structure ClassPres ")
add("coefficient_representation", IR + "LinksDefs.lean", "structure CoefA ")
add("coefficient_extension", IR + "LinksDefs.lean", "def ext ")
add("coefficient_contract", IR + "LinksDefs.lean", "def Is : Prop :=")

for sid, anchor in [
    ("quadratic_polynomial_identity", "theorem quad_pure "),
    ("frame_trace", "theorem trace_unitMap "),
    ("skew_entries", "theorem skew_entry "),
    ("opposite_sign_entries", "theorem zero_entry "),
    ("lowering_real_parts", "theorem parts "),
    ("generator_cartan_anti", "theorem gen_anti "),
    ("generator_preserves_vacuum", "theorem gen_vac "),
    ("vacuum_lowering", "theorem gen_kill_vac "),
    ("lowering_block", "theorem pMinus_laws "),
    ("mixed_coefficients", "theorem exists_coef "),
    ("mixed_laplacian_operator", "theorem gen_kill "),
    ("kernel_lowering", "theorem rderC_theta_eq_zero "),
]:
    add(sid, LOWER, anchor)
add("CCR_original", IW + "EqZeroOfPderivStable.lean", "theorem dRho_comm ")
add("original_pairing_coordinates", IW + "EqZeroOfPderivStable.lean", "def omDir ")
add("creation_commutation", IW + "EqZeroOfPderivStable.lean", "theorem aPlus_comm' ")
add("annihilation_creation_commutation", IW + "EqZeroOfPderivStable.lean", "theorem annih_aPlus ")
add("scale_nonzero", TO + "ExistsFockPolynomialOperatorHeisenbergDerivative.lean", "theorem fockScale_ne_zero ")
add("derivative_functional_extension", VAC, "theorem exists_derivForm ")
add("derivative_finite_commutation", VAC, "theorem alongLine_heisO ")
add("ambient_annihilator", VAC, "theorem exists_annihLin ")
add("finite_half", VAC, "theorem infPart_of_isHalf ")
add("theta_at_vacuum", VAC, "theorem isFockVacAt_of_isThetaAt ")
add("stored_vector_vacuum", VAC, "theorem isFockVacAt_thPVec ")
add("partial_commutation", IW + "MixedLaplacianKillsProductOfMinors.lean", "theorem pderiv_comm ")
add("delta_independence", IW + "MixedLaplacianKillsProductOfMinors.lean", "theorem delta_mem ")
add("delta_harmonic", IW + "MixedLaplacianKillsProductOfMinors.lean", "theorem laplacian_delta ")
add("target_cartan", IR + "LinksDefs.lean", "def cart ")
add("target_basis", IR + "LinksDefs.lean", "def onb ")
add("smooth_lowest_type", IR + "LinksDefs.lean", "def lowT ")
add("target_model", IR + "ScalarOnPartsFull.lean", "structure DSModel ")
add("target_smooth_space", IR + "ScalarOnPartsFull.lean", "def DSModel.sm ")
add("actual_lowest_tensor", IR + "LinksDefs.lean", "abbrev LowT ")
add("actual_multiplicity_contract", IR + "ScalarOnPartsFull.lean", "structure IsMultMap ", role=RESIDUAL)
add("discrete_series_contract", "Formalism/PeriodIntegrals/UpqRep.lean", "def IsDS ")
add("full_lowest_subspace", "Formalism/PeriodIntegrals/UpqRep.lean", "def lowKSub ")
add("lowest_smooth_contract", IR + "ExistsChosenExtremalVector.lean", "def LowSm ")
add("lowest_irreducible_contract", HDS + "HolomorphicLowestType.lean", "def LowIrr ")
add("original_io_contract", IR + "LinksChar.lean", "def IsIoW ")
add("lowering_adjoint_stability", IW + "LowestKTypeValuesKilledByLoweringPart.lean", "theorem adAt_mem_pMinus ")
add("all_coefficient_lowering", IW + "LowestKTypeValuesKilledByLoweringPart.lean", "theorem values_killed ")
add("negative_lie_block", PACKET, "def pMinus ")
add("smoothness_contract", PACKET, "def IsSmoothFn ")
add("uniform_growth_contract", PACKET, "def IsUnifModGrowth ")
add("holomorphic_cusp_packet", PACKET, "structure IsHolCuspKMap ")
add("full_extension_contract", PACKET, "def HolExtend ", role=RESIDUAL)
add("original_models", IR + "LinksChar.lean", "structure IsModels ")
add("original_weil_field", IR + "LinksChar.lean", "abbrev thP_ωP ")
add("original_vacuum_field", IR + "LinksChar.lean", "abbrev thP_vP ")
add("original_polynomial_field", IR + "LinksChar.lean", "abbrev thP_pt_theta ")
add("original_polynomial_map", IR + "LinksChar.lean", "def ptP ")
add("simultaneous_io", IR + "LinksW.lean", "def PIoP ")
add("or_zero", IR + "LinksW.lean", "def OrZero ")
add("source_identity_lift", IW + "WeilFiniteVectorFixedPrincipalLevelCoeffSpace.lean", "theorem isLift_one_V ")
add("finite_vacuum_fixing", IW + "WeilFiniteVectorFixedPrincipalLevelCoeffSpace.lean", "theorem om_level_vP ")
add("principal_target_character", HDS + "VectorLevelCharacters.lean", "theorem principalLevelCharacter_eq_one ")
add("source_rank", IR + "LinksDefs.lean", "theorem r_le_V ")
add("literal_firesAt_consumer", EXT, "theorem firesAt ", role=RESIDUAL)
add("literal_extension_consumer", EXT, "theorem exists_extension ", role=RESIDUAL)
add("literal_member_consumer", EXT, "theorem exists_member ", role=RESIDUAL)
add("literal_thetaMap_consumer", EXT, "theorem exists_thetaMap ", role=RESIDUAL)
add("remaining_io_poly", IW + "ExistsLowestKTypeFockMapThetaVectors.lean", "theorem exists_io_poly ", role=RESIDUAL)
add("remaining_io_all_parameters", IW + "ExistsLowestKTypeFockMapThetaVectors.lean", "theorem exists_ioP ", role=RESIDUAL)
add("remaining_lowest_multiplicity", IW + "HolomorphicDiscreteSeriesLowestKTypeSmoothIrredu.lean", "theorem lowSm_and_lowIrr ", role=RESIDUAL)
add("remaining_boundedness", IW + "BoundedOfSmoothCuspidalUniformModerate.lean", "theorem bounded_of_smooth_unifModGrowth ", role=RESIDUAL)
add("published_predicate_not_certificate", D + "PublishedTheorems/AutomorphicForms₂/ExistsNormLeHeightPow.lean", "def CuspRapidDecay ", role=RESIDUAL)
add("remaining_coefficient_identity", DP + "L2MatrixCoeffBoundedHolomorphicFormEqExtremalVec.lean", "theorem GlobalTheory.HolDict.inner_reg_eq_coef_extremal ", role=RESIDUAL)
add("remaining_Hilbert_realization", DP + "BoundedHolomorphicFormEqMultiplicitySpaceValue.lean", "theorem exists_multMap ", role=RESIDUAL)
add("remaining_Sobolev_realization", DP + "BoundedHolomorphicFormEqMultiplicitySpaceValue.lean", "theorem cont_value ", role=RESIDUAL)

titles = {
    "TAE1": "The explicit Gaussian oscillator action is smooth in every real parameter and Heisenberg seminorm",
    "TAE2": "The continuous scalar twists have genuine smooth real derivatives",
    "TAE3": "The actual original action has the generator, commutators, and every translated point derivative",
    "TAE4": "A common finite level gives a uniform real-cube integral bound",
    "TAE5": "The actual theta kernel has the unchanged exponent dim_R RW(T,S)",
    "TAE6": "Compact source representatives justify dominated differentiation of the literal integral",
    "TAE7": "Every derivative word of the original lift has one uniform growth exponent",
    "TAE8": "Quadratic commutators determine the entire polynomial action",
    "TAE9": "The actual vacuum is killed by lowering, including the stored IsThPVecOf transfer",
    "TAE10": "The original lowering derivative is the exact mixed Laplacian with its original scale and sign",
    "TAE11": "The literal product of minors satisfies every required mixed equation",
    "TAE12": "Lowering propagates to all coefficient values under explicit LowSm and LowIrr",
    "TAE13": "The same original lowest-type integral has the full IsHolCuspKMap packet under the retained producers",
}
maps = {
    "TAE1": ["theta_contract", "heisenberg", "inf_family", "oscillator_integral", "oscillator_derivative_source", "oscillator_bound_derivative_source"],
    "TAE2": ["continuous_character_derivative"],
    "TAE3": ["weil_contract", "lie_at", "one_parameter", "derivative", "real_line_contract", "real_line", "generator_exact", "generator_contract", "generator_ambient_extension", "generator_commutator", "translated_derivative_L2", "translated_derivative"],
    "TAE4": ["theta_contract", "weil_contract", "hom_action", "common_finite_level", "compact_integral_bound", "real_slice_measure", "cube_bound", "derivative_preserves_level", "word_level"],
    "TAE5": ["original_height", "real_hom_action", "covariant_derivative", "height_comparison", "height_lower", "word_bound", "sobolev_step", "sobolev_iter", "kernel_growth"],
    "TAE6": ["kernel", "weil_contract", "coefficient_representation", "coefficient_extension", "source_measure", "source_class_representatives", "kernel_continuity_invariance", "integral_domination", "integral_derivative"],
    "TAE7": ["right_derivative", "complex_parts", "complex_derivative", "smoothness_contract", "uniform_growth_contract", "closed_derivatives_smooth", "integral_growth", "integral_smooth_growth_killed"],
    "TAE8": ["quadratic_polynomial_identity", "pure_tensor_linear", "ordered_word"],
    "TAE9": ["generator_contract", "generator_cartan_anti", "generator_preserves_vacuum", "vacuum_lowering", "complex_structure", "annihilation", "vacuum_contract", "original_vector", "place_model", "theta_at", "derivative_functional_extension", "derivative_finite_commutation", "ambient_annihilator", "finite_half", "theta_at_vacuum", "stored_vector_vacuum"],
    "TAE10": ["oriented_pairing", "symplectic_form", "half_phase", "std_character", "original_pairing_coordinates", "CCR_original", "scaled_creation", "fock_scale", "scale_nonzero", "unit_map", "target_cartan", "target_basis", "target_model", "negative_lie_block", "lowering_real_parts", "lowering_block", "frame_trace", "skew_entries", "opposite_sign_entries", "creation_commutation", "annihilation_creation_commutation", "all_creation", "pure_tensor_oriented", "mixed_coefficients", "mixed_laplacian_operator", "kernel_lowering"],
    "TAE11": ["polynomial_variable", "positive_minor", "negative_minor", "delta_place", "delta_product", "partial_commutation", "delta_independence", "delta_harmonic", "source_rank"],
    "TAE12": ["coefficient_contract", "original_io_contract", "lowest_smooth_contract", "lowest_irreducible_contract", "smooth_lowest_type", "actual_lowest_tensor", "discrete_series_contract", "full_lowest_subspace", "lowering_adjoint_stability", "all_coefficient_lowering"],
    "TAE13": ["original_models", "original_weil_field", "original_vacuum_field", "original_polynomial_field", "original_polynomial_map", "simultaneous_io", "or_zero", "source_identity_lift", "finite_vacuum_fixing", "principal_target_character", "holomorphic_cusp_packet", "literal_firesAt_consumer", "actual_multiplicity_contract"],
}
deps = {
    "TAE1": ["CW8", "CW9", "CW10", "CW11", "CW12"],
    "TAE2": ["CW24"],
    "TAE3": ["TAE1", "TAE2", "CW12", "CW24", "BTH14"],
    "TAE4": ["TAE3", "CW12"],
    "TAE5": ["TAE3", "TAE4", "CW12"],
    "TAE6": ["TAE3", "BTH3"],
    "TAE7": ["TAE5", "TAE6", "BTH3"], "TAE8": [],
    "TAE9": ["TAE3", "CW11", "CW24", "BTH14"],
    "TAE10": ["TAE3", "TAE8", "TAE9"], "TAE11": [],
    "TAE12": ["TAE3", "TAE7", "TAE10", "TAE11"],
    "TAE13": ["TAE6", "TAE7", "TAE9", "TAE10", "TAE11", "TAE12",
              "BTH3", "BTH5", "BTH15", "FIA8", "CTC9", "CTC10", "CTC11", "CTC12", "CTC13"],
}
scopes = {
    "TAE1": "Inherited CW8-CW12 actual oscillator formula on the genuine smooth Heisenberg domain; compact parameter sets; every Heisenberg seminorm; preservation of any fixed finite Heisenberg level.",
    "TAE2": "Every continuous complex nonzero-valued character of a finite-dimensional matrix Lie group; applies to the exact inherited CW24 determinant-root twists.",
    "TAE3": "Every supplied original full IsWeilDatumO, IsInfFam, real place and real Lie direction; exists one linear generator; forall theta f, arbitrary adelic left pair p and original evaluation point w; exact IsGen commutators.",
    "TAE4": "Fix one finite level U, real basis, target point x and compact source C; exists b0; forall original theta vectors at U, all h in C and all target real g. Real derivatives keep U.",
    "TAE5": "One N=finrank_R RW(T,S) is chosen before f,x,C; forall f theta,x,C compact, exists c, forall h in C,g real, norm(thetaKO)<=c*normInf(g)^N; includes N=0.",
    "TAE6": "One original full datum and compact source representatives, original Haar measure/fundamental domain, continuous rational-invariant finite-dimensional coefficient-valued F and linear L into theta; literal integral is absolutely convergent and derivative is integral of G compose L.",
    "TAE7": "One N depending only on the real Hom dimension; forall original real derivative words in their foldr order and adelic x, exists C, forall real g, derivative norm<=C*normInf(g)^N; pointwise complex lowering passes through the original integral.",
    "TAE8": "Common invariant complex vector space, commuting creation operators, explicit quadratic commutators, b_j f=Gf=0; all polynomials; no injectivity or completion assumption.",
    "TAE9": "Actual full Weil action and actual all-place Fock vacuum; every anti-Cartan real Lie X with Y=i*s*X. Stored IsThPVecOf theta values are shown to satisfy these vacuum equations by their literal AllSome place-model contract.",
    "TAE10": "Actual positive source frame and target DS frame with ordered signs, same original theta vacuum and Fock scale; every mixed-harmonic P, place, negative-block Z and source h. Exact coefficient is -4*pi*i/fockScale(tau)^2 with nu as in TAE.62.",
    "TAE11": "Literal source delta polynomial with natural truncated exponents; only p_tau+q_tau<=rS is needed. Each mixed derivative vanishes termwise using disjoint column support.",
    "TAE12": "One supplied original c.Is and same-model LowSm, LowIrr and IsIoW; normalized delta lowering implies lowering for every coefficient value and every lowest-type pure tensor; these representation-theoretic producers are not supplied here.",
    "TAE13": "On one original R retain toLevCh.Is A.mu0, IsModels, thP_omegaP, thP_vP, thP_pt_theta; for each i retain one io_i with forall t IsIoW and LowSm/LowIrr of the same MW(i,sg0). Then forall t,x the literal integral has the original eight-field IsHolCuspKMap packet with N_i chosen before t,x,v and every derivative word. No MMap extension is asserted.",
}

human_specs = [
    ("canonical_weil/main.tex", ["CW8", "CW9", "CW10", "CW11", "CW12", "CW24"], "Exact oscillator formula, smooth-domain identification, vacuum scalar and full prescribed-character action"),
    ("base_theta/main.tex", ["BTH3", "BTH5", "BTH14", "BTH15"], "Compact original source representatives; actual finite covariance and full-action uniqueness"),
    ("finite_isotropic_average/main.tex", ["FIA8"], "Universal original polynomial/translated-kernel finite isotropic average"),
    ("constant_terms/main.tex", ["CTC2", "CTC9", "CTC10", "CTC11", "CTC12", "CTC13"], "Real-cube infrastructure and original finite averages to genuine cuspidality"),
]
inherited = []
for rel, ids, role in human_specs:
    b = (HUMAN / rel).read_bytes()
    slines = b.splitlines(keepends=True)
    blocks = []
    for cid in ids:
        pat = ("\\paragraph{" + cid + ":").encode()
        a = next(i for i, line in enumerate(slines) if pat in line)
        z = next((i for i in range(a + 1, len(slines)) if slines[i].startswith(b"\\paragraph{") or slines[i].startswith(b"\\subsection")), len(slines))
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
        "id": cid, "title": title, "introduced_in": "0.34", "classification": "B",
        "status": "complete independent human proof of the explicitly stated implication",
        "depends_on": deps[cid], "quantifier_scope": scopes[cid],
        "proof_location": {"file": "theta_extension/main.tex", "label": "claim:" + cid, "line_start": a + 1,
                           "line_end": z, "sha256": sha(block), "bytes": len(block)},
        "source_ids": maps[cid], "sources": [sources[s] for s in maps[cid]],
    })

remaining = [
    {"id": "TAE_COMMON_IO", "classification": "C", "status": "retained original coupled producer, not proved here",
     "contract": "For each original i, produce one io_i with forall t IsIoW for the same R.theta, MW(i,sg0), cV(i), omegaP(i,t), ptP(i,t), Delta(i); activate the stored OrZero choice only after this simultaneous witness exists.",
     "source_ids": ["remaining_io_poly", "remaining_io_all_parameters", "simultaneous_io"],
     "not_new_independent_top_level_obligation": True},
    {"id": "TAE_FULL_LOWEST_TYPE", "classification": "C", "status": "retained representation-theoretic producer, not proved here",
     "contract": "LowSm and LowIrr for each actual full lowKSub of the target model, including multiplicity one of the supremum of all compact subspaces of the specified type; a nonzero smooth cyclic vector does not alone prove this.",
     "source_ids": ["remaining_lowest_multiplicity", "lowest_smooth_contract", "lowest_irreducible_contract", "discrete_series_contract", "full_lowest_subspace"],
     "not_new_independent_top_level_obligation": True},
    {"id": "TAE_BOUNDEDNESS_AND_TARGET_VOLUME", "classification": "C", "status": "retained analytic/literature producer; not a checked category-A application",
     "contract": "Bound the actual smooth cuspidal uniformly moderate lowest-type form and supply a genuine finite-volume target quotient for the same target group/measure data. CuspRapidDecay is only a source predicate here, not a published theorem certificate with matched hypotheses.",
     "source_ids": ["remaining_boundedness", "published_predicate_not_certificate", "literal_extension_consumer"],
     "not_new_independent_top_level_obligation": True},
    {"id": "TAE_HILBERT_REALIZATION", "classification": "C", "status": "retained exact original realization producer, not proved here",
     "contract": "Prove inner_reg_eq_coef_extremal on the same target model and regular representation, then realize the bounded holomorphic form by an actual MMap with IsMultMap, Sobolev evaluation continuity, full smooth equivariance and exact restriction to the original lowest-type integral.",
     "source_ids": ["remaining_coefficient_identity", "remaining_Hilbert_realization", "remaining_Sobolev_realization", "actual_multiplicity_contract"],
     "not_new_independent_top_level_obligation": True},
]
provenance = {
    "schema": "rh-human-component-provenance/1", "artifact_version": "0.34", "date": "2026-11-22",
    "component": "theta_extension", "source_commit": PIN, "main_tex_sha256": sha(tex),
    "metadata_builder": {"file": "build_metadata.py", "sha256": sha(Path(__file__).read_bytes()),
                         "portable_invocation": "python3 build_metadata.py --source /path/to/pinned/checkout --human-root /path/to/reconstruction"},
    "claims": claims, "source_inventory": list(sources.values()), "baseline_dependencies": inherited,
    "remaining_producer_contracts": remaining,
    "validation": {"source_commit_verified": True, "pinned_blob_verified_files": len(cache),
                   "source_ranges": len(sources), "claim_source_occurrences": sum(len(v) for v in maps.values()),
                   "all_source_ranges_exact": True, "new_lean_build": False,
                   "tex_validation": "See validation/validation.json; draft compilation is syntax validation only."},
    "scope_note": "Formal correctness is assumed. TAE proofs reconstruct the analytic/growth/lowering block independently; no category-A certificate, full extension, simultaneous io existence, or original-data existence is asserted.",
}
(HERE / "provenance.json").write_text(json.dumps(provenance, indent=2, ensure_ascii=False) + "\n")

exact_inputs = ["one original R on the selected same Bundle",
                "R.toLevCh.Is A.mu0", "R.IsModels", "R.thP_omegaP", "R.thP_vP", "R.thP_pt_theta"]
packet_inputs = exact_inputs + ["for each i, exists one io_i, forall t, IsIoW on the literal same R fields",
                              "LowSm and LowIrr for the same MW(i,sg0) model"]
closure = {
    "schema": "rh-component-closure/1", "version": "0.34", "component": "theta_extension",
    "source_commit": PIN, "main_tex_sha256": sha(tex),
    "provenance_sha256": sha((HERE / "provenance.json").read_bytes()),
    "new_claims": list(titles), "claim_count": len(titles),
    "class_counts": {"A": 0, "B": len(titles), "C": 0, "D": 0},
    "all_new_claims_are_conditional_implications": True,
    "exact_original_inputs": exact_inputs,
    "closed_subtargets": [
        {"contract": "actual smooth oscillator action on the genuine theta domain", "proof": ["TAE1", "TAE2"]},
        {"source_declaration": "exists_generator", "scope": "literal source generator/IsGen consumer; no nOp+lambda normal-form statement is claimed", "proof": ["TAE3"]},
        {"source_declaration": "thetaKO_growth", "scope": "original normInf and exponent finrank_R RW(T,S)", "proof": ["TAE4", "TAE5"]},
        {"source_declaration": "lift_continuous_invariant_hasDerivAt", "proof": ["TAE6"]},
        {"source_declaration": "lift_smooth_growth_killed", "proof": ["TAE7"]},
        {"source_declaration": "quad_pure", "proof": ["TAE8"]},
        {"source_declaration": "isFockVacAt_thPVec and gen_kill_vac", "proof": ["TAE9"]},
        {"source_declaration": "rderC_theta_eq_zero", "proof": ["TAE8", "TAE9", "TAE10"]},
        {"source_declaration": "laplacian_delta", "proof": ["TAE11"]},
        {"source_declaration": "values_killed", "scope": "explicit same-model LowSm and LowIrr remain inputs", "proof": ["TAE12"]},
        {"contract": "literal IsHolCuspKMap packet of the original lowest-type integral", "scope": "the simultaneous io and same-model LowSm/LowIrr are supplied", "proof": ["TAE13"], "inherited": ["FIA8", "CTC9-CTC13", "BTH3", "BTH5", "BTH14", "BTH15"]},
    ],
    "sufficient_rules": [
        {"id": "TAE_ORIGINAL_ANALYTIC_LOWERING", "kind": "AND on the same supplied original R",
         "requires": exact_inputs, "concludes": "Actual theta integral absolute convergence, all-word smoothness and growth with unchanged exponent, original delta kernel lowering and finite-average cuspidality; no common io or lowest-type realization is supplied.",
         "proof": ["TAE1", "TAE2", "TAE3", "TAE4", "TAE5", "TAE6", "TAE7", "TAE8", "TAE9", "TAE10", "TAE11"]},
        {"id": "TAE_ORIGINAL_CUSP_PACKET", "kind": "AND on one R and one simultaneous io_i per i",
         "requires": packet_inputs, "concludes": scopes["TAE13"], "proof": list(titles)},
    ],
    "quantifiers": {"growth_exponent": "N_i=2*rank(Vc_i)*rank(Wc_i)*card(Tau), selected before t,x,v,derivative word,adelic x0",
                    "bounding_constant": "may depend on the vector, derivative word, adelic left translate and compact source representatives",
                    "io": "exists io_i, forall t; never weakened to forall t, exists io_(i,t)",
                    "base_tuple": "same t0=A3.A.mu0 as BTH12 and SLR8",
                    "family_threshold": "no new eventual threshold; all implications are pointwise on the same supplied data"},
    "remaining_producers": remaining,
    "new_unresolved_internal_suppliers": [],
    "new_D_obligations": [],
    "not_closed": ["existence of original weak data on the selected Bundle",
                   "simultaneous original ioP producer",
                   "full-lowest-type smoothness and multiplicity one",
                   "boundedness/target finite-volume input and Hilbert realization",
                   "full exists_extension, firesAt or exists_thetaMap",
                   "same-Bundle geometric reading, rational tests and RowsHold0_3",
                   "complete human RH/GRH proof"],
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
