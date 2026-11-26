"""Rebuild HC1–HC10 provenance from the immutable source checkout.

Writes only this component's provenance.json and source_locators.txt.
Uses original source bytes, inclusive one-indexed ranges, and exact
Git-blob comparison. No network, source edits or Lean compilation.
"""
from pathlib import Path
from hashlib import sha256
import json
import re
import subprocess

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[1] / "alpoge-rh"
COMMIT = "7cbf7a0c32fca1badf05931879a37c3f8a2b03b4"
BASE_URL = "https://github.com/CocoSgt/riemann-hypothesis-lean"
AA = "src/Development/AutomorphicArithmetic/"
GI = "src/Development/AbelianVarietyTheory/Proofs/GlobalInterpolation/"
GT = "src/Development/AbelianVarietyTheory/Definitions/GlobalTwisting/"
IF = "src/Development/AbelianVarietyTheory/Proofs/IwasawaDecomposition/"
FD = "src/Development/AbelianVarietyTheory/Proofs/FoundationProofs/"
HC = "src/Formalism/SharpRestriction/RamificationFrobenius/TotientGaloisClasses/"
PATHS = {
    "SCALE": "src/Formalism/LocalRingCardinality/DataParams₂.lean",
    "RANK": "src/Formalism/LocalRingCardinality/Params.lean",
    "DATAHOST": "src/Formalism/LocalRingCardinality/DataHost.lean",
    "ROWS": GT + "PairRowIffQdRows.lean",
    "BASE": "src/Formalism/LocalToGlobal/GlobalTheory/IsResidueClassZero.lean",
    "MARK": AA + "ThickFrames/MarkedLow.lean",
    "TOPBASE": AA + "ThickFrames/topsBase.lean",
    "TOPFRAME": AA + "ThickFrames/topsFrame.lean",
    "TOPCHOICE": AA + "ThickFrames/topsChoiceH.lean",
    "SHARES": HC + "ExplicitFormulaErrorOfHostConditions.lean",
    "FRAME": HC + "FrameFacts.lean",
    "NCARD": HC + "ZsmulGeneratorEqZeroOfProjection.lean",
    "AX": HC + "ConjEMemHostFIff.lean",
    "SEAM": AA + "CoprimeRanks/SecondSetNoRelation.lean",
    "IMPORTS": AA + "CharacterBoxes/Imports.lean",
    "THINDEF": GT + "ThinScalesIffHostBound.lean",
    "BAD": GI + "BadCharacterBound.lean",
    "CHOSEN": "src/Formalism/SharpRestriction/GlobalSchurBounds/Chosen.lean",
    "SUPPLY": AA + "CharacterBoxes/Supply.lean",
    "KIT": AA + "CharacterBoxes/KitS.lean",
    "DESIGN": AA + "CharacterBoxes/DesignS.lean",
    "SHORT": AA + "ShortNorms/ShortNorm.lean",
    "PRIMES": AA + "ShortNorms/Primes.lean",
    "NORMDEF": "src/Development/AbelianVarietyTheory/Definitions/Foundations/RayPrimes.lean",
    "NORM": AA + "ShortNorms/normPrimesN.lean",
    "TYPE": AA + "ShortNorms/typePrimesN.lean",
    "THREE": AA + "ShortNorms/ExistsThreePrimesOneModLeRpow.lean",
    "LEVEL": AA + "ShortNorms/levelData.lean",
    "BBDEF": "src/Formalism/CyclotomicNorms/StatementI.lean",
    "BBCOUNT": FD + "ExceptionalPrimesFiniteCardLe.lean",
    "BBCHOICE": FD + "DivLeRpowThreeQuarters.lean",
    "THICKDEF": "src/Formalism/FrobeniusOrbits/HostThickExists.lean",
    "THICK": "src/Formalism/FrobeniusOrbits/FrobeniusOrbitsProofs/ThickExists.lean",
    "THICK2": AA + "ThickFrames/ThickFrame2Large.lean",
    "HOST": AA + "ShortNorms/hostOfFieldOf.lean",
    "TRANK": AA + "CharacterBoxes/EventuallyRankLeRpowOfLtOneDivFiftytwo.lean",
    "QDBIG": AA + "ShortNorms/MulLogLeRpowEventually.lean",
    "PAIR": AA + "CharacterBoxes/PairGood.lean",
    "PAIRROWS": AA + "CharacterBoxes/PairRows.lean",
    "REAL": AA + "CharacterBoxes/RealSplit.lean",
    "REALBOX": AA + "CharacterBoxes/RealBox.lean",
    "NORMEL": IF + "NormOneIffOfSqrt.lean",
    "NORMMOD": IF + "NormOneModEqOneAndOfDvd.lean",
    "SPLIT": IF + "NcardPrimesOverOfStabilizer.lean",
    "THIN": AA + "MeanSquareBounds/GaussSumFunctionEq.lean",
    "TWIST": AA + "CharacterBoxes/TwistForm.lean",
    "PAGE": AA + "CharacterBoxes/ExistsPageN.lean",
    "FIELD": AA + "CharacterBoxes/FieldChi.lean",
    "BOUNDED": AA + "CharacterBoxes/BoundedTw.lean",
    "ISFIELD": AA + "CharacterBoxes/IsChiField.lean",
    "WIN": AA + "CharacterBoxes/WinPairs.lean",
    "SUPPLYADM": AA + "ShortNorms/supplyOfAdmOf.lean",
    "HOSTFIELD": AA + "CharacterBoxes/HostOfField.lean",
    "HOSTONE": AA + "ShortNorms/hostExOneOf.lean",
    "DIFF": HC + "InertiaGaloisSymmetry/KcDiff.lean",
    "RAW": HC + "InertiaGaloisSymmetry/OfRawToHostRaw.lean",
}

PREFIX = r"(?:@\[[^\n]*\]\s*)?(?:(?:private|protected|noncomputable)\s+)*"
DECL = re.compile(r"^" + PREFIX + r"(?:def|theorem|lemma|abbrev|structure|inductive|instance)\s+(\S+)")
BOUNDARY = re.compile(r"^" + PREFIX + r"(?:def|theorem|lemma|abbrev|structure|inductive|instance|namespace|end|section|variable|attribute|open|include|set_option)\b")
NS = re.compile(r"^namespace\s+(\S+)")
SEC = re.compile(r"^(?:noncomputable\s+)?section(?:\s+(\S+))?\s*$")
END = re.compile(r"^end(?:\s+(\S+))?\s*$")

actual_head = subprocess.check_output(["git", "-C", str(REPO), "rev-parse", "HEAD"], text=True).strip()
if actual_head != COMMIT:
    raise RuntimeError(f"Source checkout is {actual_head}, expected {COMMIT}")

FILES = {}
for key, path in PATHS.items():
    raw = (REPO / path).read_bytes()
    pinned = subprocess.check_output(["git", "-C", str(REPO), "show", f"{COMMIT}:{path}"])
    if raw != pinned:
        raise RuntimeError(f"Working tree differs from pinned bytes: {path}")
    lines = raw.splitlines(keepends=True)
    stack, declarations = [], []
    for i, rawline in enumerate(lines):
        line = rawline.decode("utf-8").rstrip("\r\n")
        if m := NS.match(line):
            stack.append(("namespace", m.group(1)))
        elif m := SEC.match(line):
            stack.append(("section", m.group(1)))
        elif m := END.match(line):
            if not stack:
                raise RuntimeError((path, i + 1, "unmatched end"))
            kind, label = stack.pop()
            if m.group(1) and m.group(1) != label:
                raise RuntimeError((path, i + 1, "end mismatch", label, m.group(1)))
        elif m := DECL.match(line):
            namespace = ".".join(label for kind, label in stack if kind == "namespace")
            name = m.group(1)
            declarations.append({"name": name, "line": i,
                                 "qualified": name.removeprefix("_root_.") if name.startswith("_root_.") else (f"{namespace}.{name}" if namespace else name)})
    # Lean permits an outer anonymous section to run to end of file.
    if any(kind == "namespace" or label is not None for kind, label in stack):
        raise RuntimeError((path, "unclosed named namespace or section", stack))
    FILES[key] = {
        "path": path, "full_file_sha256": sha256(raw).hexdigest(),
        "bytes": len(raw), "line_count": len(lines),
        "verified_equal_to_pinned_git_blob": True,
        "_lines": lines, "_declarations": declarations,
    }


def locator(key, name, role="parallel_source_proof", occurrence=0):
    info = FILES[key]
    hits = [d for d in info["_declarations"] if d["name"] == name]
    if occurrence >= len(hits):
        raise RuntimeError((key, name, occurrence, "declaration not found"))
    decl = hits[occurrence]
    start = decl["line"]
    lines = info["_lines"]
    end = start + 1
    while end < len(lines) and not BOUNDARY.match(lines[end].decode("utf-8")):
        end += 1
    while end > start + 1 and not lines[end - 1].strip():
        end -= 1
    excerpt = b"".join(lines[start:end])
    if role == "parallel_source_proof" and re.match(r"^" + PREFIX + r"(?:def|abbrev|structure)\b", lines[start].decode("utf-8")):
        role = "definition_or_statement"
    return {
        "path": info["path"], "declaration": decl["qualified"],
        "source_spelling": name, "line_start": start + 1, "line_end": end,
        "role": role, "full_file_sha256": info["full_file_sha256"],
        "range_sha256": sha256(excerpt).hexdigest(), "range_bytes": len(excerpt),
        "pinned_url": f"{BASE_URL}/blob/{COMMIT}/{info['path']}#L{start+1}-L{end}",
    }


def many(key, names, role="parallel_source_proof"):
    return [locator(key, name, role) for name in names]

CLAIMS = [
    {
        "id": "HC1", "title": "The literal host splitting row bounds the actual supremum Ltwo",
        "status": "proved_from_supplied_RankVal_PairWin_and_PairRow",
        "dependencies": [],
        "statement": "For fixed epsilon in (0,1/52), C0>=1 and Co=max(C0,2), the actual inert-class Ltwo is at most 2(620Co/epsilon+1), uniformly over the host data and including an empty defining set. No prime splitting or field existence is inferred without the supplied row.",
        "sources": many("SCALE", ["Scale", "ez", "L", "b", "X'", "delta1"], "literal_scale_normalizations")
            + many("RANK", ["Ranks", "n", "f", "r"], "literal_rank_dictionary")
            + many("ROWS", ["RankVal", "PairWin", "PairRow", "HostVal"], "literal_supplied_size_and_splitting_rows")
            + many("DATAHOST", ["primeClass", "cls"], "literal_inert_class_definition")
            + many("BASE", ["Base", "L1", "Ltwo"], "actual_natural_ceiling_and_supremum")
            + many("TOPBASE", ["logb_le'", "ltwo_le'"])
            + many("TOPCHOICE", ["lt_of_classC0'"]),
    },
    {
        "id": "HC2", "title": "The biased finite selection is the actual host TT and preserves HostAx",
        "status": "proved_using_BS5_with_exact_pointwise_orbit_selectors",
        "dependencies": ["HC1", "BS5"],
        "statement": "BS5 supplies the actual TT cardinality, Frame.Shares and BadOK with constants and scale threshold before all hosts. The actual step is h_p on inert candidates; the base may depend on the marked point and absolute parity is retained. Replacing TT leaves all selection inputs and HostAx unchanged.",
        "sources": many("MARK", ["hE", "KE", "rE", "dE"], "literal_K_and_rE_equals_K_plus_one")
            + many("BASE", ["IsResidueClassZero", "stepP", "nP", "topsPos", "Good", "bsH"], "literal_step_position_parity_and_pointwise_base")
            + many("TOPBASE", ["bsH_orb'", "UpperTheory.BernoulliSumsFrobeniusOrbits.topsBase"])
            + many("TOPFRAME", ["UpperTheory.BernoulliSumsFrobeniusOrbits.topsFrame"])
            + many("TOPCHOICE", ["UpperTheory.BernoulliSumsFrobeniusOrbits.topsChoiceH"])
            + many("NCARD", ["Frame", "A.val", "A.val_injective", "natCard_A", "A0", "n0", "o"], "actual_frame_and_coordinate_dictionary")
            + many("FRAME", ["natCard_A_eq_ord", "exponent_eq_index_mul_cyclic_order", "natCard_cyclic_subgroup", "index_A0_eq_o"])
            + many("SHARES", ["lam", "Shares"], "literal_biased_coset_share_endpoint")
            + many("THINDEF", ["hPH", "baseOf", "BadOK"], "literal_host_bad_sum")
            + many("DATAHOST", ["Host"], "only_TT_field_is_replaced")
            + many("HOST", ["UpperTheory.T3.hostOfFieldOf"], "actual_TT_installation_at_end_of_construction"),
    },
    {
        "id": "HC3", "title": "Exact point and family transport of shares, selected tops and bad mass",
        "status": "proved_for_supplied_actual_points_and_families",
        "dependencies": ["HC2", "BS6"],
        "statement": "Pt.From and the canonical selector identify candidate and bad sets term by term; no canonical-kappa fact is used. ChosenTT and ChosenBad follow for actually constructed families. The weighted bad mass is at most |TT|x^(-2+epsilon) after one explicit threshold.",
        "sources": many("THINDEF", ["Pt.From", "Pt.From.congr_field", "Pt.From.QS_eq", "Pt.From.cls_eq", "CanonInst"], "exact_preserved_host_data_and_selector")
            + many("BAD", ["BadOfBase", "badOK_iff_badOfBase", "chBad_iff_badOfBase", "badOfBase_of_host", "chBad_of_from"])
            + many("CHOSEN", ["ChTT_at", "largeOrderResiduePrimes", "badTops", "ChBad_at", "ChosenTT", "ChosenBad"], "literal_point_and_family_endpoints")
            + many("SUPPLY", ["FReq", "req", "At", "pt", "cls", "at_of_from"], "transport_of_scale_frame_HostAx_TT_predicates")
            + many("KIT", ["kitS"], "conditional_actual_point_constructor_join; ObjCP_remains_supplied")
            + many("DESIGN", ["designS"], "conditional_actual_family_join; NumAt_and_points_remain_supplied"),
    },
    {
        "id": "HC4", "title": "The entire source admitted witness follows from supplied HostAx and FieldRows",
        "status": "proved_from_supplied_field_data; no_Lean_placeholder_is_asserted",
        "dependencies": [],
        "statement": "The nonempty CM-type (cardinality 2ord), supplied half-different ideal and supplied sqrt(-q) give HostNF and Host with unchanged HostAx and choices. The unit ideal is a valid primitive ccK choice. Construction of the supplied HostAx and its half-different theorem remains separate.",
        "sources": many("AX", ["HostRaw", "HostDer", "HostAx"], "actual_supplied_field_CM_type_and_half_different_fields")
            + many("SEAM", ["FieldRows", "Choices", "HostNF", "HostNF.toHost", "HostNF.ofHost", "HostNF.toHost_ofHost", "HostNF.ofHost_toHost", "exists_cmType", "exists_hostNF", "exists_host", "span_natCast_ne_whole_of_one_lt", "nonempty_choices"])
            + many("IMPORTS", ["admitted"], "actual_predicate_discharged; name_is_not_a_Lean_placeholder")
            + many("DIFF", ["diffSupport", "principal"], "retained_substantive_supplier_of_HostDer_half_different")
            + many("RAW", ["HostRaw.der", "HostAx.ofRaw"], "retained_construction_of_HostAx_from_HostRaw")
            + many("HOST", ["hof_exists_host"], "actual_host_application"),
    },
    {
        "id": "HC5", "title": "The five auxiliary primes with exact norm, congruence and BB-disjointness conditions",
        "status": "proved_conditional_on_exact_ShortNorm_and_SmallOne_analytic_inputs",
        "dependencies": [],
        "statement": "ShortNorm gives >=Y^(9/10) actual NormOne primes at logY>=8x^epsilon. An elementary exceptional-root count excludes at most 20r^3Y^(3/4) candidates, yielding BB-disjoint norm primes at Y=(kb)^8. SmallOne gives three further distinct primes at most N^(2a^3+4a^2+a), eventually below b.",
        "sources": many("SHORT", ["ShortNorm", "SmallOne", "ModAt"], "exact_retained_analytic_inputs_and_modulus_premise")
            + many("PRIMES", ["UpperTheory.T3.shortNorm", "UpperTheory.T3.smallOne"], "named_analytic_suppliers_not_reconstructed_here")
            + many("NORMDEF", ["NormOne", "normPrimes"], "literal_integral_norm_equation_and_prime_set")
            + many("NORM", ["core_sqrt", "eventually_exp_decay_le", "ev_log_sq", "normPrimesN"])
            + many("BBDEF", ["Exc", "BB", "BBCount", "RootsOfUnityCount", "ChoiceCount"], "literal_exceptional_sets_and_count_targets")
            + many("BBCOUNT", ["exceptional_primes_finite_card_le", "exceptional_set_count"])
            + many("BBCHOICE", ["card_class_in_dyadic_le", "div_le_rpow_three_quarters", "card_exc_fixed_le", "card_mem_BB_fixed_le", "choiceCount_of", "choice_count"])
            + many("TYPE", ["excluded_lt", "exists_pair_disjoint", "poly_le_exp", "typePrimesN"])
            + many("THREE", ["mod_eq_one_of_mod_mul", "exists_three_primes_one_mod_le_rpow"])
            + many("LEVEL", ["mod_small", "UpperTheory.T3.levelData"]),
    },
    {
        "id": "HC6", "title": "The actual thick second set from a sphere and signed base expansion",
        "status": "proved_with_absolute_constants_32_and_64",
        "dependencies": [],
        "statement": "A finite sphere/base-expansion construction gives size >=n exp(-32sqrt(logn logL))/L with the exact signed NoRel predicate. Uniform logarithmic bounds and erasing zero give the actual T2 with CT2=64, |T2|>=x^-epsilon n and 4Lwv|T2|<=n0. This T2 is separate from the biased TT.",
        "sources": many("THICKDEF", ["NoRel", "HostThickExists"], "exact_signed_relation_and_cardinality_target")
            + many("THICK", ["coeff_zero", "map_lt", "sphere_rel", "cast_map", "sphere_mem_lemma", "noRel_image", "card_image", "hostThickExists"])
            + many("THICK2", ["UpperTheory.BernoulliSumsFrobeniusOrbits.thickFrame2_card", "UpperTheory.BernoulliSumsFrobeniusOrbits.thickFrame2_large", "UpperTheory.BernoulliSumsFrobeniusOrbits.thickFrame2"])
            + many("ROWS", ["TOv", "Lwv"], "actual_second_set_scale")
            + many("DATAHOST", ["secondSet_card_lower_bound"], "actual_host_lower_bound")
            + many("HOST", ["hof_Lwv_le", "hof_thick"], "actual_uniform_log_budget_and_application"),
    },
    {
        "id": "HC7", "title": "Actual rank, large-prime, pair-row and conductor numerical supply",
        "status": "proved_with_exact_rank_formula_and_source_constants",
        "dependencies": [],
        "statement": "RankVal gives r<=x5 and t<=x400 uniformly. PairWin/WinPair imply q,d>4tr+1 and d>=100; the explicit log budget gives log(Qqd)<=2Y^(epsilon/5)(logY)^2 and all PairRow clauses. The calculation uses raw data, avoiding a temporary arbitrary host.",
        "sources": many("ROWS", ["RankVal", "PairWin", "PairRow"], "actual_sizes_and_target_rows")
            + many("TRANK", ["UpperTheory.Top.eventually_rank_le_rpow_of_lt_one_div_fiftytwo"])
            + many("QDBIG", ["mul_log_le_rpow_eventually", "UpperTheory.T3.qdBig"])
            + many("PAGE", ["WinPair"], "actual_supplied_prime_congruences_and_intervals")
            + many("PAIR", ["PairGood"], "actual_pair_premise")
            + many("PAIRROWS", ["qdRows_kron_odd", "qdRows_kron_two", "qdRows_lo", "qdRows_up", "pairRow_of_pair", "mul_le_exp_of_le_div_sq", "UpperTheory.Top.pairRows"])
            + many("SHORT", ["ModAt"], "exact_norm_prime_modulus_endpoint"),
    },
    {
        "id": "HC8", "title": "Integral norm elements, full splitting and exact real-character boxes",
        "status": "proved_using_supplied_HostAx_Frobenius_law_and_PairGood",
        "dependencies": [],
        "statement": "The actual NormOne equation explicitly constructs pi=1+M(v+u(1+sqrt(-d))/2), with norm p and pi=1 mod M. Supplied trivial Frobenius and inertia imply full splitting. CRT and real-character conductor classification transfer PairGood to the actual QDq, Boxq, BoxH, RealBox and dlog bounds, retaining the full stated zero-box domain.",
        "sources": many("NORMEL", ["normOne_iff_of_sqrt", "normOne_iff_host"], "only_forward_NormOne_to_integral_element_direction_needed_and_proved")
            + many("NORMMOD", ["_root_.GlobalTheory.Mem.An.normOne_modEq_one_and_of_dvd"])
            + many("SPLIT", ["jacobiSym_neg_eq_one", "ncard_placesOver", "ncard_primesOver_of_stabilizer", "split_of_one_mod"])
            + many("AX", ["condN", "HostDer"], "supplied_Frobenius_inertia_and_Galois_laws; not_constructed")
            + many("PAIR", ["tw", "ZeroBox", "height", "PairGood", "RealBox"], "exact_supplied_analytic_twist_and_domain_data")
            + many("PAIRROWS", ["boxes_step", "boxes_core", "boxes_kron_odd", "boxes_kron_neg", "real_character_mod_eight", "boxq_of_pair", "qdq_core", "qdq_of_pair"])
            + many("REAL", ["UpperTheory.Top.realSplit_step", "UpperTheory.Top.realSplit_J", "exists_real_pchar_twist_decomposition", "UpperTheory.Top.realSplit"])
            + many("REALBOX", ["UpperTheory.Top.realBox_level", "UpperTheory.Top.realBox_main", "UpperTheory.Top.realBox"])
            + many("THINDEF", ["IsCharH", "isCharH_iff", "BoxH", "BoxW", "dlogH"], "literal_host_character_and_box_endpoints")
            + many("HOST", ["hof_quadraticChar_induces", "hof_abs_dlogH_le", "hof_log_le_rpow", "hof_coprime", "hof_odd", "hof_box"]),
    },
    {
        "id": "HC9", "title": "The complete elementary hostOfFieldOf join under its actual analytic and field inputs",
        "status": "proved_conditional_on_ShortNorm_SmallOne_ThinH_PairGood_and_supplied_HostAx_FieldRows_RankVal",
        "dependencies": ["HC2", "HC4", "HC5", "HC6", "HC7", "HC8"],
        "statement": "For epsilon,C0 fixed first, choose CT2=64, C8=max(C0,C1), C5=4 and uniform c6,Cb/threshold. Every actual input satisfying the report's field, rank, pair and modulus hypotheses gives HostGood plus Shares with unchanged HostAx. The source admitted premise has been discharged by HC4.",
        "sources": many("PAIR", ["ThinH"], "exact_retained_analytic_input")
            + many("THIN", ["thinH"], "named_analytic_supplier_not_reconstructed_here")
            + many("HOST", ["UpperTheory.T3.hostOfFieldOf"], "actual_constructor_and_quantifier_order")
            + many("HOSTFIELD", ["UpperTheory.Top.hostOfField"], "application_of_retained_analytic_suppliers")
            + many("THINDEF", ["ThinOK", "BadOK", "HostGood", "HostExW", "HostExP", "HostEx"], "literal_final_host_predicates")
            + many("ROWS", ["HostConst", "HostVal", "HostArith"], "all_actual_size_arithmetic_and_constant_fields")
            + many("SEAM", ["FieldRows", "Choices", "HostNF.toHost"], "literal_remaining_field_and_choice_interfaces"),
    },
    {
        "id": "HC10", "title": "Character windows and ordinary host specialization with exact existential scope",
        "status": "proved_conditional_on_actual_character_field_rank_PairEx_and_VWinAt_suppliers",
        "dependencies": ["HC3", "HC7", "HC8", "HC9"],
        "statement": "The exact dyadic rescaling with kappa=c^(1/h) turns supplied VWinAt(psi,401) and PairEx into exponent-3/2 host windows, preserves the selected field and yields EAtH and VVle(E,t,sqrt b). The host-only o=1 specialization uses M=J=1 and needs no VWinAt, but does not assert VVle or complete RH.",
        "sources": many("TWIST", ["KerChi", "TwistForm", "WinDatum"], "exact_character_field_and_window_interfaces")
            + many("PAGE", ["VVle", "IsChiField", "WinPair", "PageN", "VAt", "VWinAt", "VWin", "VVle.mono", "exists_pageN"], "retained_cohomological_window_input_and_elementary_monotonicity")
            + many("FIELD", ["conductor_divisor_bounds"], "elementary_conductor_field_rows")
            + many("FIELD", ["UpperTheory.Top.fieldChi"], "actual_character_field_supplier_retained; only_stated_elementary_rows_reconstructed")
            + many("BOUNDED", ["UpperTheory.Top.boundedTw_key", "UpperTheory.Top.boundedTw"])
            + many("ISFIELD", ["UpperTheory.Top.isChiField"])
            + many("WIN", ["UpperTheory.Top.winPairs"], "complete_conditional_window_rescaling_proof")
            + many("SUPPLYADM", ["UpperTheory.T3.supplyOfAdmOf"], "actual_uniform_host_window_assembly; admitted_discharged_by_HC4")
            + many("HOSTFIELD", ["UpperTheory.Top.supplyOfAdm"], "actual_endpoint_with_retained_field_rank_and_analytic_inputs")
            + many("HOSTONE", ["UpperTheory.T3.hostExOneOf"], "separate_ordinary_host_only_specialization")
            + many("SHARES", ["Level.cyc", "EAtH"], "literal_character_error_endpoint")
            + many("PAIR", ["PairEx", "PairGood.mono"], "analytic_prime_pair_existence_retained_and_monotonicity_used"),
    },
]

ids = {c["id"] for c in CLAIMS}
assert ids == {f"HC{i}" for i in range(1, 11)}
external = sorted({d for c in CLAIMS for d in c["dependencies"] if d not in ids})
def visit(name, path=()):
    if name in path:
        raise RuntimeError("dependency cycle: " + " -> ".join(path + (name,)))
    for child in next(c for c in CLAIMS if c["id"] == name)["dependencies"]:
        if child in ids:
            visit(child, path + (name,))
for name in ids:
    visit(name)

report = (HERE / "report.txt").read_text()
main = (HERE / "main.tex").read_text()
for name in ids:
    assert re.search(r"^" + name + r"\. ", report, re.M), name
assert main.count(r"\[") == main.count(r"\]"), "unbalanced display delimiters"
for claim in CLAIMS:
    for source in claim["sources"]:
        info = next(v for v in FILES.values() if v["path"] == source["path"])
        start, end = source["line_start"], source["line_end"]
        assert 1 <= start <= end <= info["line_count"]
        assert DECL.match(info["_lines"][start - 1].decode("utf-8"))
        assert source["pinned_url"].endswith(f"#L{start}-L{end}")

artifacts = []
for name in ["main.tex", "report.txt", "build_provenance.py"]:
    raw = (HERE / name).read_bytes()
    artifacts.append({"path": name, "sha256": sha256(raw).hexdigest(), "bytes": len(raw)})
payload = {
    "artifact_version": "0.12", "component": "host_tops",
    "repository": BASE_URL, "commit": COMMIT, "head_verified": actual_head,
    "line_range_convention": "inclusive, one-indexed, original bytes including line endings",
    "claims": CLAIMS,
    "source_files": [{k: v for k, v in f.items() if not k.startswith("_")} for f in FILES.values()],
    "artifacts": artifacts,
    "explicit_external_dependencies": external,
    "derived_simplifications": [
        "The literal admitted predicate is discharged directly from HostAx's CM-type and half-different fields, FieldRows and the choices; it is not left as an extra premise.",
        "The actual TT replacement preserves HostAx and all inputs of the finite selection, including point-dependent base selectors and absolute parity.",
        "The signed base-expansion sphere proof gives explicit second-set constants 32 and 64, independently of the biased TT.",
        "A raw rank/conductor calculation avoids creating an arbitrary temporary host solely to prove PairRow.",
        "Only the forward NormOne-to-integral-element implication is needed; the explicit element proves it without a full ring-of-integers basis theorem.",
        "The source prime selection consequences are reconstructed quantitatively, while ShortNorm and SmallOne themselves remain analytic inputs.",
        "The dyadic rescaling and character transport are complete under their literal field/rank/PairEx/VWinAt inputs; ordinary host-only specialization is kept separate.",
    ],
    "outside_scope": [
        "Analytic proofs of ShortNorm, SmallOne and ThinH, and PairEx supplying the actual PairGood.",
        "Construction of HostAx/HostDer and its Galois, Frobenius, CM-type and half-different fields, and the actual character-field/FieldRows supplier.",
        "The uniform rank constructor and cohomological VWinAt(psi,401) supplier.",
        "Actual ObjCP/RecExP point construction and NumAt/family existence; only their downstream exact transports are proved here.",
        "Local identifications are reconstructed in the concurrent LI component under supplied host data, not assumed globally absent.",
        "Archimedean trace/kernel estimates, global comparison-lattice span/dimension identities and the complete RH/GRH conclusion.",
    ],
    "review_records": [
        {"path": "v0_12/reviews/root_reviews_hc.txt", "scope": "HC1-HC5 and HC7-HC10 mathematical and source-join review"},
        {"path": "v0_12/reviews/bo_reviews_hc6.txt", "scope": "HC6 sphere, no-carry, cardinality, uniform erasure and main-fragment review"},
    ],
    "scope_note": "Actual finite, numerical, algebraic and conditional constructor proofs with all analytic/field/point suppliers explicitly retained. Exact pinned source-byte validation is not a Lean compilation or kernel replay.",
}
(HERE / "provenance.json").write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n")
out = [f"HC1-HC10 exact source locators at {COMMIT}", ""]
for claim in CLAIMS:
    out.extend([claim["id"] + ": " + claim["title"], "Dependencies: " + ", ".join(claim["dependencies"])])
    for source in claim["sources"]:
        out.extend([
            f"  {source['declaration']} | {source['path']}:{source['line_start']}-{source['line_end']} | {source['role']}",
            "    " + source["pinned_url"],
            f"    file sha256 {source['full_file_sha256']} ; range sha256 {source['range_sha256']}",
        ])
    out.append("")
(HERE / "source_locators.txt").write_text("\n".join(out) + "\n")
print(json.dumps({
    "claims": len(CLAIMS), "source_files": len(FILES),
    "locators": sum(len(c["sources"]) for c in CLAIMS),
    "external_dependencies": external, "artifacts": artifacts,
}, indent=2))

