#!/usr/bin/env python3
"""Rebuild the v0.12 local-identification source ledger at the immutable pin.

Only this component directory is written. All full source files are compared
byte for byte with their pinned Git blobs; all inclusive declaration excerpts
are hashed without normalization. No Lean compilation or replay is claimed.
"""
from pathlib import Path
import hashlib
import json
import re
import subprocess

WORK = Path(__file__).resolve().parents[2]
ROOT = WORK / "alpoge-rh"
OUT = Path(__file__).resolve().parent
COMMIT = "7cbf7a0c32fca1badf05931879a37c3f8a2b03b4"
REPO = "https://github.com/CocoSgt/riemann-hypothesis-lean"
IW = "src/Development/AbelianVarietyTheory/Proofs/IwasawaDecomposition/"
SA = "src/Development/AbelianVarietyTheory/Proofs/SatakeParameters/"
AM = "src/Development/AbelianVarietyTheory/Definitions/AutomorphicMembership/"
GL = "src/Formalism/LocalToGlobal/GroupLattices/"
HC = "src/Formalism/LocalToGlobal/HermitianColumns/"
LR = "src/Formalism/LocalRingCardinality/"
FR = "src/Formalism/SharpRestriction/RamificationFrobenius/TotientGaloisClasses/"
LG = "src/Formalism/SharpRestriction/GenusPolyhedralBounds/RelativeIndexClassSets/"
SW = "src/Formalism/SatakeDualWeyl/"

assert subprocess.check_output(
    ["git", "rev-parse", "HEAD"], cwd=ROOT, text=True
).strip() == COMMIT

files, cache = {}, {}
TOP = re.compile(
    r"^(?:(?:private\s+)?(?:noncomputable\s+)?"
    r"(?:theorem|lemma|def|structure|abbrev|class|inductive|end|namespace|section|variable|include|omit|open|attribute|instance|set_option|local)\b|@\[\s*)"
)


def source(path):
    if path not in cache:
        raw = (ROOT / path).read_bytes()
        pinned = subprocess.check_output(["git", "show", COMMIT + ":" + path], cwd=ROOT)
        assert raw == pinned, ("source differs from pin", path)
        lines = raw.decode("utf-8").splitlines(keepends=True)
        cache[path] = (raw, lines)
        files[path] = dict(
            path=path, sha256=hashlib.sha256(raw).hexdigest(),
            bytes=len(raw), line_count=len(lines),
            verified_equal_to_pinned_git_blob=True,
            url=f"{REPO}/blob/{COMMIT}/{path}",
        )
    return cache[path]


def namespace_at(lines, first):
    stack = []
    for line in lines[:first - 1]:
        ns = re.match(r"^namespace\s+(\S+)", line)
        sec = re.match(r"^(?:noncomputable\s+)?section(?:\s|$)", line)
        end = re.match(r"^end(?:\s|$)", line)
        if ns:
            stack.append(("namespace", ns.group(1)))
        elif sec:
            stack.append(("section", ""))
        elif end:
            assert stack, ("unmatched end", first, line)
            stack.pop()
    return ".".join(value for kind, value in stack if kind == "namespace")


def ref(path, name, role="proof"):
    _, lines = source(path)
    pat = re.compile(
        r"^(?:private\s+)?(?:noncomputable\s+)?"
        r"(?:theorem|lemma|def|structure|abbrev|class|instance|inductive)\s+"
        + re.escape(name) + r"(?=[\s{(:])"
    )
    hits = [i for i, line in enumerate(lines) if pat.match(line)]
    assert len(hits) == 1, (path, name, hits)
    first = hits[0] + 1
    last = next((i for i in range(first, len(lines)) if TOP.match(lines[i])), len(lines))
    while last > first and not lines[last - 1].strip():
        last -= 1
    namespace = namespace_at(lines, first)
    qualified = (
        name.removeprefix("_root_.") if name.startswith("_root_.")
        else (namespace + "." if namespace else "") + name
    )
    excerpt = "".join(lines[first - 1:last]).encode("utf-8")
    return dict(
        path=path, declaration=qualified, source_spelling=name,
        line_start=first, line_end=last, role=role,
        sha256=files[path]["sha256"], full_file_sha256=files[path]["sha256"],
        range_sha256=hashlib.sha256(excerpt).hexdigest(), range_bytes=len(excerpt),
        first_line=lines[first - 1].rstrip("\r\n"),
        declaration_lines_within_range=[first],
        url=f"{REPO}/blob/{COMMIT}/{path}#L{first}-L{last}",
    )


def group(base, file, names, role="proof"):
    return [ref(base + file + ".lean", n, role) for n in names]


def iw(file, names, role="proof"):
    return group(IW, file, names, role)


def gl(file, names, role="proof"):
    return group(GL, file, names, role)


def lr(file, names, role="proof"):
    return group(LR, file, names, role)


P = "ExistsLocIdOfCompletions"
W = "ExistsPlTieOfInertCore"
BASE = [
    "The host is supplied: E/Q is Galois CM with its stated abelian Galois group, conjugation, complex embedding, conductor and arithmetic Frobenius law. This component does not construct the host or prove abundance of suitable primes.",
    "Classical background is stated in report.txt: finite fields; the Witt rings and Teichmuller expansions already used in BC1; number-field integer rings finite over Z and Dedekind; DVR localization/completion; lying over; and the elementary inertia identity |I_P|=e_P.",
    "BC1-BC3 are prior proved results supplying the actual finite coefficient extension, its chosen-place embedding and the exact ramification scaling. Their proofs are reused, not reasserted as new LI claims.",
    "All local lattices and levels are the literal supplied ColLevel/LevelData objects. A frame for each completion does not by itself construct a common global matrix B.",
    "The global class-rank equality and comparison-lattice identification remain separate. No full IsLocalFamily, GroupCompatibilityAll, linked family, RH or GRH conclusion is asserted here.",
]
claims = []


def claim(cid, title, statement, sources, dependencies=(), status="faithful_translation", note="", extra=()):
    claims.append(dict(
        id=cid, title=title, status=status, statement=statement,
        depends_on=list(dependencies), assumptions=BASE + list(extra),
        proof_location=dict(file="main.tex", anchors=[cid]),
        expanded_notes=dict(file="report.txt", section=cid),
        source_relation=note,
        mathematical_status="proved_relative_to_declared_classical_background_and_named_proved_companion_results",
        sources=sources,
    ))


claim(
    "LI1", "Explicit unramified lifting and exact completion comparison",
    "For an unramified number-field prime P over p of residue degree m, construct a Good embedding into Q_m=Frac(W(F_(p^m))). Conversely, every such Good embedding identifies the actual completion with Q_m and its integer ring with W_m, compatibly with the original number field.",
    group(SA, W, ["intAlg", "exists_intHom", "eq_of_cong", "exists_wittHom", "Wn", "Qn", "Fr", "cc_eq_zero", "isUnit_of_cc", "Good", "exists_good", "Good.intAt", "Good.dense", "Good.pow_inj"], "source_lifting_and_Good_counterpart")
    + iw("ExistsCompletionEquiv", ["exists_hom_of_dense", "eq_of_forall_pow", "exists_equiv_of_dense", "exists_completion_equiv"])
    + iw(P, ["liesOver_of_mem", "mem_max", "p_mem", "plc", "p_mem_plc", "ov_plc", "mem_plc", "good_plc", "good_approx"]),
    dependencies=["BC1"], status="derived_simplification",
    note="A Newton/simple-root power-basis proof replaces the source formal-etale Witt lifting. The converse uses the exact local-integrality criterion and identical quotients at every p-power precision, not an unsupported density-to-isomorphism inference.",
    extra=["For the forward direction the prime is unramified; for the converse the three literal Good clauses are given. The converse itself implies unramifiedness."],
)

claim(
    "LI2", "Frobenius fixes the exact residue degree and classifies all E-primes",
    "Under the supplied arithmetic Frobenius f=((-1,-1),h) with even n=ord(h)>=2, every E-prime above p has residue degree n. For a fixed Good i:E->Q_n, P_g=ker(residue of i sigma_g) satisfies P_g'=P_g iff g'=g f^s, and every prime above p occurs.",
    group(SA, W, ["exists_frob_pow", "frob_pow_inj", "fr_pow", "Good.twist", "Ov", "Ov.eq", "Ov.conj", "ov_iff", "exists_ov", "exists_res", "Good.ov", "Good.exists_pow"])
    + iw(P, ["exists_aut", "plc_eq_of_pow", "good_aut", "isArithFrobAt_of", "sigmaOf_mul", "sigmaOf_inj", "sigmaOf_surj", "orderOf_frob", "mem_of_good", "fr_apply", "fr_pow_apply", "degree_eq", "good_tw", "exists_pow_of_plc_eq"]),
    dependencies=["LI1"],
    note="The proof expands finite-field Frobenius order, residue lifting uniqueness and normality of E/Q. Right multiplication g'=g f^s is checked with the source action convention. No decomposition-group classification is retained as an unexplained local input.",
)

claim(
    "LI3", "The literal Frobenius orbits label every real-subfield prime above p",
    "With c=((-1,-1),1), z=((1,1),h), Psi={(epsilon,1,a)}, n even implies c notin <f>. Every restriction i sigma_g|F is Good with residue degree n, and Psi/<z> is bijective with all primes v|p of F, using the literal orbRep/posG section and positions a_v z^s. Thus Q_n is exactly each F_v and E/F splits there.",
    group(FR, "ZsmulGeneratorEqZeroOfProjection", ["MA", "GG", "iota", "iotaInv", "cc", "chD", "Psi", "mem_Psi_iff"], "literal_host_group")
    + group(FR, "FrameFacts", ["index_Psi", "natCard_Psi", "cc_notMem_Psi", "cc_mul_cc", "orderOf_cc", "cc_mem_zpowers_iff"], "finite_group_counterparts")
    + iw(P, ["cc_mul_cc", "cc_pow", "cc_notMem", "frob_eq_mul", "tw", "tw_apply", "twF", "twF_cc_pow", "mem_plc_twF", "mem_plc_tw_cc", "conj_conj", "exists_real", "plc_ne_conj", "good_twF", "place_injective", "place_surjective"])
    + gl("LevelGatherings/SecPsiMulPow", ["OrbSec", "nOrb", "orbEquiv", "orbRep", "orbRep_mk", "orbRep_of_mk", "posG_bij", "posG", "posG_apply", "posG_step", "nOrb_mul_order", "zPsi", "zPsi_eq", "orderOf_zPsi"], "literal_orbit_enumeration"),
    dependencies=["LI1", "LI2"], status="derived_simplification",
    note="CRT produces b+c(b) with every required residue, without division by 2. The norm y c(y) and the two-ideal union argument prove equality of contractions directly. The target is ALL primes above p, and the source section is retained exactly.",
)

claim(
    "LI4", "Align the original coefficient embedding and prove the exact conjugation-parity position identity",
    "Embed the actual KfRec into C_p with ORec as its unit ball; extend its original embRec along the given complex number-field embedding to lambda on algebraic complex numbers. Adjust the Good E-embedding by one Galois automorphism before enumerating primes. Then i_K iota Fr^s(i_v x)=lambda(phi_(a_v z^s c^s)(x)) at every literal position, which is PosCompat and LocPack.posOK for every psi.",
    iw("LamV", ["exists_lam"])
    + iw(P, ["exists_locId_host", "exists_locId_of_emb", "exists_emb_norm", "exists_locId"], "exact_compatible_embedding_endpoints")
    + gl("LevelGatherings/PosCompatOfBase", ["emb_mul", "sigmaOf_pow", "PosCompat", "posCompat_of_base"])
    + gl("CloudFilling/FillInstRecEqWj", ["LocPack", "LocPack.posOK"], "literal_record_and_position_property")
    + gl("PerfectRings/ExtWRec", ["KfRec", "ORec", "embRec", "extRec", "embRec_int"], "prior_BC2_actual_coefficient_objects"),
    dependencies=["BC1", "BC2", "LI2", "LI3"], status="derived_simplification",
    note="The embedding extension is proved inside Qbar_p and then C_p; no map on transcendental complex numbers is used. The orbit enumeration is chosen after the permissible Galois adjustment. The c^s factor at odd positions and the original embRec are preserved exactly.",
)

claim(
    "LI5", "Explicit quadratic splitting and the frame for the actual localized lattice",
    "For j:E->F_v obtained from the Good embedding, Phi(x tensor t)=(j(x)t,j(c(x))t) is the required splitting with explicit inverse. The first projection of the literal locL is exactly O_v-span(j(Lc.Lb)), a full finite-free O_v lattice. Its basis supplies fr_lat, so all fields of LocId are constructed and its recovered iw is i_v.",
    gl("LevelGatherings/CompletionIntegersIff", ["LocId", "iw", "frQ"], "literal_required_record")
    + lr("DataLevel", ["intV", "ColLevel"], "literal_given_lattice_and_integral_ring")
    + group(HC, "InLocalDiscriminantKernel", ["locL"], "literal_localized_lattice")
    + group(SW, "Statement", ["sigR", "inclE", "swapR", "tensInt", "intOE"], "literal_tensor_maps_and_integral_subring")
    + group(SW, "StatementC", ["latS"], "literal_tensor_lattice_span")
    + group(LG, "LocIdFr", ["hom_int", "fst_int", "exists_spl", "fr_lat_of"], "source_splitting_and_frame_counterparts")
    + group(LG, "LevGapLoc", ["sc_exists_iso", "sc_emb_int", "sc_left_mem", "sc_right_mem"], "split_map_and_integrality_counterparts")
    + iw("ExistsCompletionEquiv", ["exists_first_frame"], "frame_endpoint_replaced_by_direct_DVR_basis_proof")
    + iw(P, ["exists_locId_of_completions"], "exact_reconstructed_local_record_endpoint"),
    dependencies=["LI1", "LI3"], status="derived_simplification",
    note="The equality pi_1(intV)=O_v proves both inclusions for the actual lattice projection, and finite generation/fullness are checked before applying DVR freeness. This replaces the longer dual-frame construction; it does not assert a common global frame B.",
)

claim(
    "LI6", "The actual positions induce the prescribed primes with the exact ramification scale",
    "For the actual theta_g=tauLL/Cmp.tEL satisfying e_C theta_g=phi_g, embRec(theta_(a_v z^s)(c^s x))=iota Fr^s(i_v x). Thus for nonzero x in F the normalized valuations nu_w(theta x)/nu_w(p) and v_p(i_v x) agree; for every integral x in F, including zero, membership in v is equivalent to strictly positive nu_w(theta x).",
    lr("DataErr", ["tauLL"], "literal_coefficient_field_embedding")
    + gl("TiedFamilies/TieIwLevTieOf", ["tieIw", "tieIw_levTieOf", "locAt_iw_C", "pos_C"], "actual_even_odd_embedding_dictionary")
    + iw("LocalIdentificationPlaceEqInducedRealPlace", ["iota_sigma_mem_range", "val_pos_iff", "mem_asIdeal_iff_inv", "inv_int_iff", "tie_mem_iff", "int_map_eq_zero_iff", "place_of_tie"])
    + iw("LocalIdentificationPlaceEqInducedRealPlaceStatement", ["_root_.GlobalTheory.T.mem_localPlace_asIdeal_iff_val_pos"], "actual_exported_prime_membership_statement")
    + gl("PerfectRings/ExtWRec", ["val_nonneg_iff", "resChar_mem", "embRec_int"], "prior_BC_prescribed_place_and_integrality_dictionary"),
    dependencies=["BC2", "BC3", "LI4"], status="derived_simplification",
    note="The source's integrality-of-inverse proof is spelled out, including x=0. The normalized equality is an explicitly proved strengthening via BC3; an unnormalized integer-valuation equality is not claimed. This does not identify the global comparison lattice.",
    extra=["The actual theta_g maps and their complex embedding identity are supplied as fields of the global datum. The normalized ratio is stated only for x!=0."],
)

claim(
    "LI7", "Discharge the literal exists_locId endpoint for every GIdx prime of supplied host data",
    "GIdx excludes the conductor; the supplied Host Frobenius law gives trivial inertia and Frobenius ((-1,-1),R.iota(hP)). HNeZero makes its finite order even and at least two, equal to frobOrder. LI1-LI6 then give the full exists_locId conclusion for the original D7/Lc/coefficient prime: all real primes, exact completion rings and lattice frames, aligned i_K/lambda and posOK for every away character.",
    lr("RhoDetPrimeEqMuTildeMulChiPow", ["GIdx", "D7"], "literal_supplied_global_datum_and_prime_condition")
    + lr("DataHost", ["Host", "sigmaOf", "emb", "cls", "sqrtMinusD", "HNeZero", "HNeZero.ne_one"], "literal_host_and_even_order_interfaces")
    + group(FR, "ConjEMemHostFIff", ["HostRaw", "condN", "small", "F", "galE", "conj", "psAt", "HostDer", "HostAx"], "explicit_supplied_global_host_input")
    + group(FR, "ConjEMemHostFIff", ["hostE_isGalois", "isCMField_hostE", "finrank_hostF", "galE_mul", "galE_bijective", "galE_injective", "exists_galE_eq", "galE_conjE", "conjE_apply", "conjE_mem_hostF_iff", "sqd_ne_zero"], "host_field_dictionary")
    + lr("HostCls", ["primeClass_eq_inert_iff", "dvd_condN_iff_primeClass", "not_dvd_conductor_of_inert", "jacobi_d_eq_one_or", "psAt_eq_one_or_neg_one", "primeClass_eq_inert_iff_symbols", "psAt_prime"], "specialization_of_supplied_host_Artin_and_quadratic_laws")
    + lr("SpanPowerMembership/GatTies", ["of_cls", "hOf", "hOf_of_coprime", "unit_eq_neg_one", "frob_val", "exists_frob", "hOf_even", "hOf_ne_one"], "actual_Frobenius_component_identification")
    + gl("CloudFilling/GatRecStepFrob", ["frob_eq"], "actual_hP_identification")
    + group(AM, "FrobOrderSpec", ["frobOrder", "frobOrder_spec", "pack", "pack_ψ"], "actual_order_and_pack")
    + iw(P, ["unramified_of_inertia", "exists_locId_of_completions", "exists_locId_host", "exists_locId_of_emb", "exists_emb_norm", "exists_locId"], "exact_reconstructed_endpoint"),
    dependencies=["LI1", "LI2", "LI3", "LI4", "LI5", "LI6"],
    note="The host Frobenius/Artin law is a stated global premise, not relabelled as a new proof here. Its local specialization and every remaining construction in exists_locId are expanded. The class name inertClass does not imply E/F is inert: the proved completion is split.",
)

claim(
    "LI8", "Construct the actual integral inverse away character and identify the remaining global joins",
    "Under literal Joint0 and LevelZeroCharacterRational, canonical finite-adelic truncation K sets components above p to one and preserves all others. Level-zero additive-character values and their inverses are algebraic integers. Their unique coefficient-field lifts map to units of ORec; psi(a)=embRec(r(K(a)))^(-1) is a homomorphism satisfying every quantifier in PsiTied. These choices are simultaneous with LI7, whose posOK holds for every psi.",
    iw("AddCharIsIntegral", ["adelic_ext", "exists_trivial_on", "finite_over", "exists_away_mem", "addChar_isIntegral", "chi_isIntegral", "exists_inv_char", "exists_psiTied", "exists_psi"])
    + gl("DownNaturalLevelZero", ["Forms0", "Joint0"], "literal_supplied_level_interfaces")
    + gl("ComparisonMaps/RecAct", ["gramN_zero"], "structural_Gram_identity_separate_from_Joint0")
    + gl("TiedFamilies/ChiMemSubfield", ["chi_mem_subfield", "LevelZeroCharacterRational", "chiRatAll_rec"], "literal_character_rationality_input_and_product_argument")
    + gl("TiedFamilies/TiePsi", ["PsiTied"], "exact_character_conclusion")
    + group(HC, "CompletionIntegersIff", ["awayFrom₂"], "literal_away_level_group")
    + gl("PerfectRings/ExtWRec", ["val_nonneg_iff", "embRec_int"], "prior_BC2_integrality_transport")
    + iw("ExistsConcrete", ["Companion", "stdBasis", "stdBasis_std", "placeId", "embK", "embAlg", "embK_embAlg", "awayChar", "gatOf", "gatOf_d", "posOK_placeId"], "consumer_and_explicit_common_frame_rank_boundary")
    + iw("IsRecGOfIsLocalFamily", ["IsLocalFamily", "exists_isLocalFamily", "isRecG_of_isLocalFamily"], "global_assembly_boundary_not_asserted_proved")
    + iw("CharZeroOfSetting", ["pack_d_eq"], "retained_class_rank_endpoint")
    + group(AM, "ExistsEmbeddingOfRingTie", ["comparison_statements"], "retained_global_comparison_lattice_assembly")
    + iw("ExistsGIs", ["nonempty_columnLocalData_of_standardConcreteFamily", "exists_trueVolume_stage_of_any_column_choice"], "later_linked_family_consumers"),
    dependencies=["BC2", "LI7"],
    note="Truncation uniqueness proves multiplicativity and the universal kappa quantifier. Integrality is strengthened to unit membership by also applying the argument to inverses. The consumer references record precise remaining premises and are not counted as discharged assertions.",
    extra=["Joint0 and LevelZeroCharacterRational are supplied; their construction from global automorphic data is not proved by the finite-character argument."],
)

claim_files = dict(files)
GW = "src/Formalism/SharpRestriction/GrowthBounds/IntegralWeylLatticeSpan/"
next_groups = [
    dict(
        id="global_standard_frame", priority=1,
        objective="Supply the actual common global frame from StdTied and the companion identity, then replace every local frame without changing iw or position compatibility.",
        mathematical_task="StdTied must come from the actual global model. Given its orthonormal integer basis and BaseTied, the local argument should be short: L is contained in the standard lattice, the latter is contained in L^dual, and T L^dual is contained in L. Since p does not divide T, their local projections agree. This is stronger than LI5's independently chosen local frames.",
        sources=group(HC, "ZeroPointScaledByCharacter", ["StdTied", "BaseTied"], "retained_actual_global_premises")
        + iw("TrueColumnSpacesStandardInFrameCoords", ["GlobalTheory.Mem.Col2.TC.spaces_in_coordinates"], "actual_StdTied_supplier_under_TC_Ok_Pins_Laws_Later")
        + gl("TiedFamilies/TieStd", ["stdB_core", "exists_stdB_of_tied"], "next_proof_target")
        + gl("TiedFamilies/CompanionOfBaseTied", ["T_smul_mem", "companion_le", "LocId.withFr", "locIdStd", "locIdStd_iw", "companion_of_baseTied"], "next_proof_target")
        + iw("ExistsGIs", ["companion_of_colsHermS"], "actual_ColsHermS_supplier"),
    ),
    dict(
        id="actual_class_rank", priority=2,
        objective="Prove pack_d_eq for the literal level/class representatives and automorphic forms, using the exact orbit bijection and stabilizer hypotheses.",
        mathematical_task="The local tableau/tensor basis part should reuse CB/BC/IP only after checking HtupW's integral Weyl convention. The genuine remaining join is the correspondence between global class labels and level-group orbits, plus trivial stabilizers and the level-zero forms dimension. A mere equality of abstract representation dimensions is insufficient.",
        sources=iw("CharZeroOfSetting", ["exists_basis_Dl0", "exists_basis_HtupW", "d_eq_of_classes", "locPack_d_eq", "pack_d_eq"], "next_proof_target")
        + gl("ComparisonMaps/ClsRec", ["clsR_iff", "clsR_surj"], "substantive_class_correspondence_supplier")
        + gl("TrivialTransfer/GramTotallyDefinite", ["trivStabU_rec", "stabZero_rec"], "substantive_stabilizer_supplier")
        + group("src/Formalism/LocalToGlobal/GlobalTheory/CoordinateLengths/", "DuCount", ["finrank_forms_level_zero"], "global_forms_dimension_supplier"),
    ),
    dict(
        id="actual_integral_comparison_criterion", priority=3,
        objective="Prove ValIntRec and the actual even/odd coefficient-lattice identification used in comparison_statements.",
        mathematical_task="The actual field, local basis and Gram data must match the global integral polynomial spans. Expand valIntAt_of; identify the exact Weyl descent statement with already proved integral models where possible. At odd positions the inverse-transpose matrix is corrected by the integral invertible Gram matrix, not identified with the original matrix without that correction. LI supplies the position identity and BC supplies the coefficient extension only.",
        sources=gl("ComparisonMaps/CmpCMemMIff", ["IntAtW", "ValIntRec", "LocWCrit"], "literal_target_definitions")
        + group(GW, "IntSpanGSmul", ["valIntAt_of", "valIntRec_of"], "substantive_integral_criterion_target")
        + group(GW, "WeylLatticeDescentHolds", ["oddFact_pf", "weylLatticeDescent_holds"], "exact_integral_Weyl_descent_supplier")
        + group(GW, "SelfDualCongr", ["latW_gen", "gramW_gen", "restLatW_of", "restGramW_of"], "actual_local_lattice_and_Gram_suppliers")
        + group(GW, "ColSpanMulUnit", ["latO_of", "restLatO_of", "restExB", "restChi_of"], "odd_position_and_global_basis_suppliers")
        + group(AM, "ExistsEmbeddingOfRingTie", ["block_rational", "comparison_statements"], "actual_assembly_and_remaining_rationality_supplier"),
    ),
    dict(
        id="comparison_lattice_span", priority=4,
        objective="Turn the proved integral criterion into equality of the full global comparison lattice with the actual local function lattice M.",
        mathematical_task="Expand rational-function surjectivity and the rational-span argument, including finite classes and weak approximation. LI proves distinct actual places and the completion-integrality dictionary needed by weakRec_pf, but does not by itself prove the entire span equality.",
        sources=gl("TiedFamilies/TieLat", ["cmpRec_lat_pf", "latM_pf", "mRatSpan_rec"], "substantive_lattice_comparison_targets")
        + gl("TiedFamilies/TieSurj", ["surjRat_pf"], "rational_surjectivity_target")
        + gl("TiedFamilies/TieWeak", ["weak_of_locAt", "weakRec_pf", "latM_rec'"], "weak_approximation_and_span_targets")
        + gl("TiedFamilies/TieLatFin", ["surjRat_rec", "comparison_lattice_span_eq"], "exact_exported_span_endpoint"),
    ),
    dict(
        id="simultaneous_family_assembly", priority=5,
        objective="After the preceding genuine inputs, assemble the supplied-data IsLocalFamily and GroupCompatibilityAll conclusions with the already reconstructed LI and BC maps.",
        mathematical_task="These endpoints are assembly targets, not substitutes for the common global frame, exact rank or comparison lattice. Preserve the original coefficient rings and embRec, the source orbRep positions, the c^s parity, and the same inverse away character.",
        sources=iw("IsRecGOfIsLocalFamily", ["IsLocalFamily", "exists_isLocalFamily", "isRecG_of_isLocalFamily"], "later_family_assembly_target")
        + iw("ExistsGIs", ["nonempty_columnLocalData_of_standardConcreteFamily", "exists_trueVolume_stage_of_any_column_choice"], "later_linked_family_consumers"),
    ),
]
next_paths = {s["path"] for g in next_groups for s in g["sources"]}
next_obj = dict(
    artifact_version="0.12", repository=dict(url=REPO, commit=COMMIT),
    status="continuation_targets_not_newly_proved_claims",
    prior_boundary_closed=["LI1-LI7 literal local places/completions/frames and position compatibility", "LI8 integral inverse away character under supplied Joint0 and rationality", "BC1-BC8 finite coefficient ring and exact base-change transport"],
    groups=next_groups, files=[files[p] for p in sorted(next_paths)],
)
(OUT / "next_targets.json").write_text(json.dumps(next_obj, ensure_ascii=False, indent=2) + "\n")
next_lines = ["LOCAL IDENTIFICATION FOLLOW-UP TARGETS — v0.12", "Pin: " + COMMIT,
              "These are remaining targets, not additional proved LI claims.", ""]
for g in next_groups:
    next_lines += [str(g["priority"]) + ". " + g["objective"], g["mathematical_task"]]
    for s in g["sources"]:
        next_lines += [f"  {s['declaration']} | {s['path']}:{s['line_start']}–{s['line_end']}", "    " + s["url"]]
    next_lines.append("")
(OUT / "next_targets.txt").write_text("\n".join(next_lines) + "\n")

reviews_path = OUT / "independent_reviews.json"
reviews = json.loads(reviews_path.read_text()) if reviews_path.exists() else []
unique_ranges = {(s["path"], s["line_start"], s["line_end"]) for c in claims for s in c["sources"]}
artifact_paths = [OUT / "main.tex", OUT / "report.txt", Path(__file__).resolve()]
if reviews_path.exists():
    artifact_paths.append(reviews_path)
for name in ["next_targets.txt", "next_targets.json"]:
    if (OUT / name).exists():
        artifact_paths.append(OUT / name)
out = dict(
    schema_version="1.2", artifact_version="0.12", date="2026-11-21", owner="/root/lean_audit",
    repository=dict(url=REPO, commit=COMMIT),
    range_convention="One-indexed inclusive declaration ranges; exact source bytes are compared with the pinned Git blob and hashed without normalization.",
    verification=dict(
        full_file_bytes_compared_with_pinned_git_blob=True, range_bytes_hashed_without_normalization=True,
        human_mathematical_proofs_supplied=True, lean_source_files_edited=False,
        local_lean_compilation=False, lean_kernel_replay=False, replacement_arguments_formalized=False,
    ),
    status_definitions=dict(
        faithful_translation="A complete human proof of the stated source assertion under explicitly supplied hypotheses and named prior proved results.",
        derived_simplification="A proved shorter argument or explicitly stated strengthening with exact source counterparts and unchanged application data.",
        remaining_input="A genuinely unexpanded hypothesis or downstream theorem. No LI local construction has this status; retained global premises are separately listed and marked in source roles.",
    ),
    independent_reviews=reviews,
    claims=claims,
    files=[claim_files[p] for p in sorted(claim_files)],
    artifact_sha256={p.name: hashlib.sha256(p.read_bytes()).hexdigest() for p in artifact_paths},
    prior_components_reused=[
        dict(ids=["BC1", "BC2", "BC3"], component="v0_11/base_change", role="Actual standard Witt/quadratic coefficient field, finite normalization, prescribed-place embedding, faithful integral transport and exact ramification normalization."),
    ],
    same_iteration_companions=[
        dict(component="v0_12/host_tops", role="Independent concrete host/point transport branch. LI consumes the stated Host laws; it does not infer that branch's global hypotheses from local identifications."),
    ],
    boundary_resolved=[
        dict(interface="GlobalTheory.PlaceOrbit.exists_locId_of_completions / exists_locId", discharged_by=["LI1", "LI2", "LI3", "LI4", "LI5", "LI7"], scope="Full literal local record, all primes above p, actual lattice frame, original coefficient embedding and every-position parity compatibility, for supplied D7/host/level data and GIdx."),
        dict(interface="GlobalTheory.TiePlace.place_of_tie", discharged_by=["LI4", "LI6", "BC2", "BC3"], scope="Actual local-prime membership and normalized valuations for the supplied theta_g coefficient embedding dictionary; no global comparison lattice inferred."),
        dict(interface="GlobalTheory.Mem.AwayChar.exists_psi", discharged_by=["LI8", "BC2"], scope="Actual ORec-unit character under supplied Joint0 and LevelZeroCharacterRational, simultaneous with the local-position construction."),
    ],
    scope_precision=[
        "The finite abelian group A is the actual R.MA; no cyclicity assumption is inserted.",
        "The arithmetic Frobenius convention is residue x->x^p; same-prime embeddings satisfy g'=g f^s with the source multiplication convention.",
        "The orbit quotient labels all F-primes above p. Even ord(h) excludes c from <f> and makes E/F split despite the name inertClass.",
        "Position compatibility includes c^s at odd positions and uses the original embRec. The Good embedding is adjusted before the prime enumeration is chosen.",
        "The projected lattice is the literal locL(Lc.Lb), not an abstract full lattice chosen independently. Its local frame need not descend to one global B.",
        "Only nu_w/nu_w(p) is identified with the Witt p-valuation; integral valuations may scale under ramification. The zero case is included separately in prime membership.",
        "PsiTied is proved for every compatible kappa by truncation uniqueness, and psi takes values in ORec units, using integrality also of inverses.",
        "The classical Hensel/completion construction is a human replacement argument, not a claimed formalized Lean replacement or kernel replay.",
    ],
    retained_inputs=[
        "The supplied Host/HostDer/HostAx fields, including their conductor and arithmetic Frobenius laws; their global construction and suitable-prime abundance.",
        "The supplied D7, ColLevel/LevelData and coefficient embedding dictionaries; LI does not construct the global arithmetic representation or host.",
        "Joint0 and LevelZeroCharacterRational for the level-zero forms in the away-character endpoint.",
        "StdTied plus Companion and the standard-frame supply, pack_d_eq, and the actual comparison_statements/ValIntRec/comparison_lattice_span_eq branch. LI constructs the individual LocId records only.",
        "All separate global theta/period, spectral, cohomological-window and analytic conclusions required for RH or GRH.",
    ],
    independent_review_targets=[
        "LI1-LI3 Hensel uniqueness, exact completion converse, Frobenius degree and every-prime CRT/ideal contraction classification",
        "LI4-LI6 original coefficient alignment, c^s parity, actual lattice projection, normalized valuation and zero branch",
        "LI7-LI8 exact GIdx specialization, character rationality/unit proof and simultaneous-family scope",
    ],
)
(OUT / "provenance.json").write_text(json.dumps(out, ensure_ascii=False, indent=2) + "\n")
(OUT / "source_manifest.json").write_text(json.dumps(dict(repository=out["repository"], files=out["files"]), ensure_ascii=False, indent=2) + "\n")
loc = []
for c in claims:
    loc.append(c["id"] + " — " + c["title"])
    for s in c["sources"]:
        loc.append(f"  {s['declaration']} | {s['path']}:{s['line_start']}–{s['line_end']} | {s['role']}")
        loc.append(f"    file={s['sha256']} range={s['range_sha256']}")
        loc.append("    " + s["url"])
(OUT / "source_locators.txt").write_text("\n".join(loc) + "\n")
print(json.dumps(dict(
    claims=len(claims), source_files=len(claim_files),
    references=sum(len(c["sources"]) for c in claims), unique_ranges=len(unique_ranges),
    output=str(OUT / "provenance.json"),
), indent=2))
