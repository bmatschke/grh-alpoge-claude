#!/usr/bin/env python3
"""Rebuild the exact pinned-source ledger for the v0.9 graded Gram proof.

The builder only writes this component directory. Every cited source file is
byte-compared with its Git blob; declaration ranges are inclusive and hashed
without normalization. No Lean build or replacement formalization is claimed.
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
MM = "src/Formalism/MahlerMeasure/"
FR = "src/Formalism/ThetaLogCoordinates/FockResolutionOnto/"
FP = FR + "FockMonomialProofs/"
PW = "src/Formalism/ThetaLogCoordinates/TraceIsometryWeights/"
PM = "src/Formalism/ThetaLogCoordinates/PartnerMeanCoordinates/"
PD = "src/Formalism/PolynomialDimension/"
assert subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip() == COMMIT
files, cache = {}, {}
TOP = re.compile(
    r"^(?:(?:private\s+)?(?:noncomputable\s+)?"
    r"(?:theorem|lemma|def|structure|abbrev|class|end|namespace|section|variable|include|omit|open|attribute|instance|set_option|local)\b|@\[\s*)"
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
        r"(?:theorem|lemma|def|structure|abbrev|class)\s+"
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
        sha256=files[path]["sha256"], range_sha256=hashlib.sha256(excerpt).hexdigest(),
        range_bytes=len(excerpt), first_line=lines[first - 1].rstrip("\r\n"),
        declaration_lines_within_range=[first],
        url=f"{REPO}/blob/{COMMIT}/{path}#L{first}-L{last}",
    )


def group(base, file, names, role="proof"):
    return [ref(base + file + ".lean", n, role) for n in names]


def mm(file, names, role="proof"):
    return group(MM, file, names, role)


def fp(file, names, role="proof"):
    return group(FP, file, names, role)


def fr(file, names, role="proof"):
    return group(FR, file, names, role)


def pw(file, names, role="proof"):
    return group(PW, file, names, role)


def pm(file, names, role="proof"):
    return group(PM, file, names, role)


def pd(file, names, role="proof"):
    return group(PD, file, names, role)


claims = []
ASSUMPTIONS = [
    "p is prime, coefficients are Q_p with coefficient lattice Z_p, and v_p(p)=1.",
    "The signed word has K+1 letters, r>=2 coordinates, rho=r-1, and its final letter is a vector.",
    "Each letter has a fixed nonnegative integral degree; there are finitely many prefix constraints with thresholds in Z union {infinity}.",
    "Standard characteristic-zero split-GL highest-weight theory and elementary DVR/Smith theory are declared background. Integral denominator statements use the already proved IW1-IW4.",
]


def claim(cid, title, statement, sources, dependencies=(), status="faithful_translation", note="", extra=()):
    claims.append(dict(
        id=cid, title=title, status=status, statement=statement,
        depends_on=list(dependencies), assumptions=ASSUMPTIONS + list(extra),
        proof_location=dict(file="graded_gram_section.tex", anchors=[cid]),
        expanded_notes=dict(file="report.txt", section=cid),
        source_relation=note,
        mathematical_status="proved_relative_to_declared_classical_background_and_prior_proved_IW",
        sources=sources,
    ))


claim(
    "GG1", "Literal signed coefficient, highest-vector and graded initial lattices",
    "The actual grLat is the image in_e(F_e M_w), not its saturation. The form is Fock/prod_i(d_i!), so every monomial diagonal is a reciprocal product of integer multinomials.",
    mm("GoodCount", ["Letters", "MultiDeg", "Pol", "IntPol", "PolZ", "glAct", "wt", "GlStable", "gSpan", "FirstLE", "YCond", "Y", "YZ", "fock", "fockN"], "literal_definition")
    + mm("CsSaturated", ["WtSpC", "GlStableC", "HWC", "IsoC", "CsSaturated", "IsTypeProj", "WeylLat", "MMw", "MMwZ", "FilE", "grLat"], "literal_definition")
    + mm("HasOrder", ["HasOrder", "initPart"], "literal_order_definition")
    + mm("StatementT", ["GramDeterminantGradedHypothesis"], "exact_target"),
    note="The coefficient image retains the factor z^e. Saturation is not inserted into its definition.",
)

claim(
    "GG2", "Exact integral prefix projectors, highest projection and multiplicity-safe Weyl generation",
    "The signed prefix coordinate width is at most D, yielding HypP, HypE and HypW with e1=binom(r,2)Nat.log_p(D+r-1). HypE is the matching smaller-group type projector on a fixed full weight. Highest-vector generation works on an entire isotypic module with multiplicities and requires no integral irreducible splitting.",
    mm("StatementT", ["HypP", "HypW", "HypE"], "exact_interface")
    + pw("StatementC", ["kapC", "FockAdj", "ProjP", "CommP", "IntP", "WeylP", "ExtP"], "exact_denominator_interface")
    + pw("SchurTraceProofs/FischerAdjointnessHolds", ["fischerAdjointness_holds", "divided_integral_holds"])
    + pw("SchurTraceProofs/OrthogonalIsomorphismHolds", ["projection_lattice_holds"])
    + pw("SchurTraceProofs/CommProjectionHolds", ["typeProj_comm", "comm_projection_holds"])
    + pw("SchurTraceProofs/CompEqZeroOfNotDle", ["comp_eq_zero_of_not_dle", "isHW_of_mem_gSall", "comp_mem_lowIm", "lowC_le_perpV", "extP_of"])
    + pw("SchurTraceProofs/PolLeISupIsoW", ["intP_of"])
    + pw("SchurTraceProofs/ZpClosedToAddSubgroup", ["weylP_of"])
    + pw("SchurTraceProofs/TypeInt", ["typeInt_of"], "prior_IW4_source_counterpart")
    + pw("SchurTraceProofs/WeylInt", ["topC", "wl_key", "weylInt_of", "weyl_integral_holds"], "highest_generation_source_counterpart")
    + pw("SchurTraceProofs/InvInt", ["invariant_integral_holds"], "prior_IW1_source_counterpart")
    + pw("SchurTraceProofs/InvInv", ["invariant_inverse_holds"], "prior_IW2_source_counterpart")
    + pw("SchurTraceProofs/Discharge", ["kapC_mono", "pow_smul_mem_of_le", "dischargeP_of", "dischargeW_of", "dischargeE_of"])
    + pw("DischargeHeightBound", ["weylInt", "weylP", "extP", "dischargeW", "dischargeE"])
    + fp("GramBoundUnconditionalOfSat", ["hypPE_setLast"], "uniform_reduced_degree_application"),
    dependencies=["GG1", "IW1", "IW2", "IW3", "IW4"],
    note="The multiplicity-space extension of IW3 is proved explicitly. The Hom height is the difference of two weights at one coordinate, not a difference of coordinates within one weight.",
)

claim(
    "GG3", "Explicit auxiliary GL action, integral divided powers and finite weight width",
    "The literal XSp direct sum is stable under EX. A direct first-weight argument bypasses rational-surjectivity/Omega injectivity. Generic W-coordinate evaluation gives o<=c+D_early, and all auxiliary weight coordinates lie in [-D_early,c+2D_early], so the width is <=4D. The formal U-flow proves root divided-power integrality for every integer c.",
    fr("ShiftLastLetterThresholds", ["setLast", "FreeOf", "TypesLE", "XSp"], "literal_auxiliary_space")
    + fp("LatDefs", ["Wtot", "M2"], "literal_rational_and_image_lattices")
    + fr("StatementD", ["Wm", "dW", "eulW", "Uop", "UComm", "UKeepsLast", "UKeepsEarly", "UDeg", "ResU"], "literal_operator_and_stability_statements")
    + fr("StatementG", ["EX", "wtX", "GXExists", "UDivInt", "DWDivInt", "XVanish"], "literal_auxiliary_target")
    + fp("RaisingKeepsEarlyLetters", ["Uop_apply", "Uop_supp", "Uop_top", "raising_comm_holds", "raising_degree_holds", "restriction_raising_holds", "raising_keeps_early_letters", "raising_keeps_last_letter"], "first_weight_argument_counterpart")
    + fp("WmMulWmComm", ["U_U", "relX", "coeff_EX_diag", "GX", "GX_E", "coeff_GX_comp", "gl_action_exists"], "GL_relations_and_weights")
    + fp("DerivativeDividedIntegral", ["pderiv_div_int", "derivative_divided_integral", "Uop_eq", "DDop_last", "DDop_vec", "DDop_cov", "DDop_pair", "Uop_pow_one", "udiv_map", "raising_divided_integral"], "integral_flow_counterparts")
    + fp("Vanish", ["space_vanishing_holds"], "generic_evaluation_replacement_counterpart")
    + fp("DerivativeKillsDegreeZero", ["dEarly", "dEarly_nonneg", "dEarly_le_total", "wtot_stable", "x_vanish", "wtot_monomial", "wtot_fd", "wtX_range", "wtot_bound", "wtot_finW", "latData"], "actual_finite_representation_checks")
    + fp("DerivativeKillsDegreeZero", ["x_lift", "u_x"], "source_route_bypassed_not_assumed"),
    dependencies=["GG1", "GG2"], status="derived_simplification",
    note="The complete proof checks the actual XSp cutoffs directly. Neither x_lift nor Omega injectivity is a remaining input. The formal exponential is a new compact proof of the exact source divided-power assertion; it is not claimed formalized.",
)

claim(
    "GG4", "The actual restriction-image lattice lifts after precisely two IW losses",
    "For every integral x in the literal XSp at the original last degree, an integral h in the literal Y has h|_(z=0)=p^(2D4)x. M2 is divided-power stable and contains all integral auxiliary highest vectors, which have last degree zero. Type isolation and highest generation each cost D4, and extracting the original degree yields the actual lift.",
    fr("StatementG", ["ResSatL", "ResSatLThm"], "exact_integral_lift_target")
    + fp("LatDefs", ["Wtot", "M2"], "literal_image_not_saturated_replacement")
    + fp("DerivativeKeepsSpaceHolds", ["restriction_mem_space"], "restriction_into_actual_space")
    + fp("RestrictedLatticeDividedPower", ["mem_restrictedLattice_of_mem", "restrictedLattice_le", "restrictedLattice_map_le", "restrictedLattice_zpClosed", "restrictedLattice_divided_power", "glAct_y", "dW_y", "dW_pow_y", "uop_y", "uop_pow_y", "glAct_pow_y", "restrictedLattice_of_deg_zero", "compL_deg", "restrictedLattice_exists_lift", "restrictedLattice_divStable", "span_le_restrictedLattice"])
    + fp("DerivativeKillsDegreeZero", ["hw_deg_zero", "latData", "wtot_le_iso"], "actual_highest_and_weight_data")
    + fp("RestrictedSaturationHolds", ["sat_of_mem_y", "pol_le_ycond", "sat_main", "restricted_saturation_holds"], "exact_source_lifting_conclusion")
    + pw("HasLatBasis", ["DeltaLat", "LatData"], "actual_lattice_hypotheses")
    + pw("StatementB", ["TypeInt", "WeylInt"], "two_separate_denominator_losses"),
    dependencies=["GG1", "GG2", "GG3"],
    note="The source's c0=2D4 is retained exactly. This proves controlled lifting, not exact integral surjectivity or saturation of M2. No separate rational-surjectivity input is used.",
)

claim(
    "GG5", "Exact order stripping and saturation control for the actual graded image",
    "Multiplication by z^e shifts only the final degree, rho weight, and full-prefix thresholds. The rational graded span is z^e XH for the reduced data. Projecting the actual integral lift to full weight and smaller-group highest vectors proves p^(e1+2D4)(V_e intersect Z_p[X]) subset grLat.",
    fr("ShiftLastLetterThresholds", ["setLast", "shiftLastLetterThresholds", "shiftWt", "XH", "grSpan", "SatAt"], "exact_shift_and_saturation_definitions")
    + fp("MulEarlyLettersHolds", ["mul_early_letters_holds", "mul_last_letter_holds"], "generic_Laurent_degree_replacement_counterparts")
    + fp("FiltrationBotHolds", ["pow_mul_int_iff", "multiDeg_pow", "pol_pow", "wtSpC_pow", "hWC_pow", "yCond_pow", "mMw_pow", "mMwZ_pow", "filtration_eq_holds", "graded_eq_holds", "graded_bot_holds"])
    + fp("RestrictionMinMaxIntHolds", ["hypE_eproj", "eproj_fix", "eproj_comm", "eproj_Y", "eproj_res"], "actual_projection_naturality")
    + fp("GramBoundOfRestrictionOfProj", ["grSpan_eq"], "exact_rational_graded_identification")
    + fp("GramBoundUnconditionalOfSat", ["resSatL_mono", "resOntoK_of_resSatL", "resMMZL", "satAtL"]),
    dependencies=["GG1", "GG2", "GG4"], status="derived_simplification",
    note="Generic first-weight Laurent-degree additivity proves both directions of the cutoff shift. Initial coefficients retain z^e; actual saturation cost b=e1+2D4 is proved, not assumed.",
)

claim(
    "GG6", "Orthogonal graded projection with cost (K+1)e1 and exact zero-prefix handling",
    "For K>=1 there is a rational Fock-orthogonal projection onto V_e, integral after p^((K+1)e1). The K+2 type projections commute; prefix0 and prefix1 are identity or zero, leaving K paid projections and one highest projection. For K=0 the actual nonzero graded lattice is a monomial line with Gram entry 1/binom(d,e).",
    fr("StatementH", ["TrivProj", "HighestVectorProjectionPos", "GradedBoundOfSaturationPos", "ResSatLZero"], "exact_improved_projection_targets")
    + fr("ShiftLastLetterThresholds", ["ProjAt"], "exact_projection_on_graded_span")
    + fp("HighestVectorProjectionPos", ["trivial_projection_holds", "highest_vector_projection_holds"])
    + fp("GramBoundOfRestrictionOfProj", ["strip", "coeff_strip", "strip_monomial_ne", "strip_monomial_eq", "fock_pow_mul", "grSpan_eq"])
    + fp("GramBoundPosOfProjSat", ["projAt2_of", "restricted_saturation_zero"], "source_projection_and_zero_case_counterparts"),
    dependencies=["GG1", "GG2", "GG5"], status="derived_simplification",
    note="The positive-K cost is exactly the source's improved exponent. The direct K=0 monomial calculation is stronger than the generic source estimate and is not used to alter downstream constants.",
)

claim(
    "GG7", "Primitive integral partners and the actual initial-Gram determinant",
    "Every primitive u of grLat has a partner in that same actual lattice with normalized Fock valuation at most A+2b. Smith form yields v_p(det Gram)<=((K+3)e1+4D4)rank for K>=1, including nonintegral Gram matrices, zero rank, and all orders. No positive-form restriction or exact saturation claim is used.",
    mm("StatementT", ["GramDeterminantGradedHypothesis"], "literal_endpoint")
    + fr("StatementA", ["PartnerDet", "GradedPieceBound"], "primitive_partner_and_determinant_interfaces")
    + fp("PartnerDeterminantHolds", ["partner_determinant_holds", "grLat_le_int", "grLat_le_pol", "graded_piece_bound_holds"])
    + pd("MultinomialDepth/PartnerM", ["fockN_monomial_ge"], "exact_normalized_monomial_test")
    + fp("GramBoundPosOfProjSat", ["graded_bound_pos_of_proj"], "exact_A_plus_two_b_assembly")
    + fp("GramBoundUnconditionalOfSat", ["graded_bound_saturation_holds"], "general_source_cost_comparison")
    + pm("PartnerMeanProofs/GramHypothesisOfLogBound", ["gram_hypothesis_of_log_bound"], "actual_exported_Gram_target"),
    dependencies=["GG1", "GG5", "GG6"],
    note="The two saturation losses remain visible: c0=2D4, b=e1+c0 and A+2b=(K+3)e1+4D4. The normalized form divides by the factorials of the exact prefix word.",
)

claim(
    "GG8", "Exact segment kappa4 and full-word projector inputs to TheoremMV7",
    "Under literal SizeHypothesis for odd p, r>=2 and a>=1, every tied prefix has D_i with 2D_i+1<=8a+r. Therefore both logarithms are <=ell=1+log_p(8a+r), and K=pos_i<2s+1 gives GramDeterminantGradedHypothesis with kappa4=(s+4)r^2 ell. Full words satisfy HypP/HypW with floor(r^2 ell).",
    pd("DigitSumValuationBound", ["lgSeg", "kapSeg"], "literal_segment_constants")
    + pd("ChainOrderLetters", ["degreeAtPosition", "ChainOrderLetters", "ConditionShape", "SizeHypothesis", "TheoremMV7Of", "TheoremMV7"], "actual_caller_hypotheses_and_target")
    + mm("GoodCount", ["TieData", "TieData.Admissible", "TieData.S"], "actual_tie_data")
    + mm("StatementTM", ["Letters.takeD", "Letters.setTies", "TieData.thrUpTo"], "exact_prefix_word_and_thresholds")
    + mm("MahlerMeasureProofs/TheoremM", ["takeD_total_eq", "S_mono"], "prefix_total_comparison")
    + fp("GramBoundUnconditionalOfSat", ["grid_le", "takeD_vec_last"], "actual_grid_and_final_vector_checks")
    + pm("PartnerMeanProofs/GramHypothesisOfLogBound", ["natLog_le_lgSeg", "one_le_lgSeg", "natLog_floor_lgSeg", "choose_two_le", "gram_hypothesis_of_log_bound", "setTies_total_le", "theoremMV7"], "exact_numeric_discharge")
    + pm("TheoremMXB", ["MeanGamX", "TieOpsX"], "downstream_exact_Gram_and_projector_inputs"),
    dependencies=["GG1", "GG2", "GG7"],
    note="This supplies the Gram/projector hypotheses of the actual local theorem. Construction of SizeHypothesis from higher-level segment parameters, compatible partners, weighted rank/digit transfer and global RH/GRH are not inferred here.",
    extra=[
        "For the segment application: p is odd, a>=1, r>=2, word length=2s+1, literal T.Admissible and SizeHypothesis hold at the upper grid endpoint.",
    ],
)

reviews = [
    dict(
        reviewer="/root/remarks_math",
        scope="GG2 highest projection; GG3 direct cutoff stability, generic degree bound and signed U-flow; GG4 actual image-lattice lifting; GG6-GG7 costs",
        result="Passed: no substantive correction found. The omitted restriction term has a z factor; highest vectors lift at degree zero; original-degree extraction and A+2b bookkeeping were checked.",
    )
]
review_file = OUT / "independent_reviews.json"
if review_file.exists():
    reviews = json.loads(review_file.read_text(encoding="utf-8"))
out = dict(
    schema_version="1.2", artifact_version="0.9", date="2026-11-21", owner="/root/lean_audit",
    repository=dict(url=REPO, commit=COMMIT),
    range_convention="One-indexed inclusive declaration ranges; exact source bytes are compared with the pinned Git blob and range bytes are hashed without normalization.",
    verification=dict(
        full_file_bytes_compared_with_pinned_git_blob=True,
        range_bytes_hashed_without_normalization=True,
        human_mathematical_proofs_supplied=True,
        lean_source_files_edited=False,
        local_lean_compilation=False,
        lean_kernel_replay=False,
        replacement_arguments_formalized=False,
    ),
    status_definitions=dict(
        faithful_translation="A complete human proof of the precise cited source assertion, using only the stated data and prior proved IW results.",
        derived_simplification="An explicitly proved shorter route or harmless strengthening with exact source counterpart and unchanged application constants.",
        remaining_input="A genuinely unexpanded input. No new GG local proof claim has this status.",
    ),
    independent_reviews=reviews,
    claims=claims,
    files=[files[p] for p in sorted(files)],
    prior_components_reused=[
        dict(ids=["IW1", "IW2", "IW3", "IW4"], component="v0_5/integral_weyl",
             role="Proved invariant averaging, denominator and isotypic projector statements; exact Hom-coordinate width is rechecked."),
    ],
    bypassed_source_routes=[
        dict(path=FP+"DerivativeKillsDegreeZero.lean", declarations=["x_lift", "u_x"],
             replacement="GG3 proves XSp stability directly, so restriction_surjective/Omega injectivity is not a remaining input."),
    ],
    historical_boundary_resolved=[
        dict(id="TI6", boundary="Actual restricted graded initial-Gram premise", discharged_by=["GG1","GG2","GG3","GG4","GG5","GG6","GG7","GG8"]),
        dict(id="TI9", boundary="Restricted graded Gram and its integral highest/prefix lattice bridge only", discharged_by=["GG1","GG2","GG3","GG4","GG5","GG6","GG7","GG8"]),
    ],
    outside_scope=[
        "Construction of the caller's full SizeHypothesis and simultaneous numerical parameters from global segment data.",
        "Compatible multiple-tie partners, weighted digit-class rank/density transfer and paired edge lifts (companion TP, SW and RL components).",
        "Global orbit abundance, arithmetic windows, analytic completion and the final RH/Dirichlet-GRH implication.",
    ],
)
(OUT / "provenance.json").write_text(json.dumps(out, ensure_ascii=False, indent=2)+"\n", encoding="utf-8")
(OUT / "source_manifest.json").write_text(
    json.dumps(dict(repository=out["repository"], files=out["files"]), ensure_ascii=False, indent=2)+"\n",
    encoding="utf-8",
)
locators = []
for c in claims:
    locators += [c["id"]+": "+c["title"], "Status: "+c["status"]]
    for s in c["sources"]:
        locators += ["  "+s["declaration"], "  "+s["url"],
                     "  full-file SHA256 "+s["sha256"],
                     "  inclusive-range SHA256 "+s["range_sha256"]]
    locators.append("")
(OUT / "source_locators.txt").write_text("\n".join(locators), encoding="utf-8")
print(json.dumps(dict(
    claims=len(claims), source_files=len(files),
    source_references=sum(len(c["sources"]) for c in claims),
    unique_ranges=len({(s["path"],s["line_start"],s["line_end"]) for c in claims for s in c["sources"]}),
), ensure_ascii=False,
))
