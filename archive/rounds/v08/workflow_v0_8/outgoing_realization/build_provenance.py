#!/usr/bin/env python3
"""Rebuild source-exact v0.8 outgoing-realization provenance."""
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
GB = "src/Formalism/SharpRestriction/GrowthBounds/"
assert subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip() == COMMIT
files, cache = {}, {}
TOP = re.compile(r"^(?:(?:private\s+)?(?:noncomputable\s+)?(?:theorem|lemma|def|structure|abbrev|class|end|namespace|section|variable|include|omit|open|attribute|instance|set_option|local)\b|@\[\s*)")

def source(path):
    if path not in cache:
        raw = (ROOT / path).read_bytes()
        pinned = subprocess.check_output(["git", "show", COMMIT + ":" + path], cwd=ROOT)
        assert raw == pinned, ("source differs from pin", path)
        lines = raw.decode("utf-8").splitlines(keepends=True)
        cache[path] = (raw, lines)
        files[path] = dict(path=path, sha256=hashlib.sha256(raw).hexdigest(),
            bytes=len(raw), line_count=len(lines), verified_equal_to_pinned_git_blob=True,
            url=f"{REPO}/blob/{COMMIT}/{path}")
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

def ref(path, name, role="source_counterpart"):
    _, lines = source(path)
    pat = re.compile(r"^(?:private\s+)?(?:noncomputable\s+)?(?:theorem|lemma|def|structure|abbrev|class)\s+" + re.escape(name) + r"(?=[\s{(:])")
    hits = [i for i, line in enumerate(lines) if pat.match(line)]
    assert len(hits) == 1, (path, name, hits)
    first = hits[0] + 1
    last = next((i for i in range(first, len(lines)) if TOP.match(lines[i])), len(lines))
    while last > first and not lines[last - 1].strip():
        last -= 1
    ns = namespace_at(lines, first)
    qualified = name.removeprefix("_root_.") if name.startswith("_root_.") else (ns + "." if ns else "") + name
    excerpt = "".join(lines[first - 1:last]).encode("utf-8")
    return dict(path=path, declaration=qualified, source_spelling=name,
        line_start=first, line_end=last, role=role, sha256=files[path]["sha256"],
        range_sha256=hashlib.sha256(excerpt).hexdigest(), range_bytes=len(excerpt),
        url=f"{REPO}/blob/{COMMIT}/{path}#L{first}-L{last}")

def refs(file, names, role="source_counterpart"):
    return [ref(GB + file + ".lean", name, role) for name in names]

def w(names, role="source_counterpart"):
    return refs("WittFrameLocaliserOrders", names, role)

def pw(file, names, role="source_counterpart"):
    return refs("PathWeight/" + file, names, role)

def os(names, role="source_counterpart"):
    return refs("DualFockLinear/OneSidedLemma4OfAdmittedTheoremII", names, role)

claims = []
def claim(cid, title, statement, sources, dependencies=(), assumptions=(), status="faithful_translation", note=""):
    claims.append(dict(id=cid, title=title, status=status, statement=statement,
        depends_on=list(dependencies), assumptions=list(assumptions),
        proof_location=dict(file="outgoing_realization_section.tex", anchors=[cid]),
        expanded_notes=dict(file="report.txt", section=cid), source_relation=note,
        sources=sources))

claim("OR1", "A partial-prefix determinant twist is a rank-one update",
    "For r distinct selected vector rows and every prefix or arbitrary letter subset S′, the generic conjugate cocharacter changes the selected matrix by a rank-one update. Its determinant is affine in t with minimum exponent <=1. Hence val_S′(D_A^m H)<=val_S′(H)+m, including the zero case.",
    refs("ObjPol", ["Letters", "genMat", "GLCoord", "GLLaurent", "gL", "gLinv", "twistMat", "coefL", "twistSub", "sDegs", "lastIdx", "valS"], "exact_generic_substitution_definitions")
    + w(["letterDeterminant", "FieldMultidegreeDivisibility"], "exact_interface_proved"),
    assumptions=["Any coefficient field, r>0, distinct chosen vector letters; no characteristic-zero or infinite-field assumption."],
    status="derived_simplification",
    note="This supplies a direct proof of the second clause of FieldMultidegreeDivisibility. That interface is a conclusion here, not a hypothesis.")

claim("OR2", "Generic singular specialization forces all determinant powers integrally",
    "For a letter-multihomogeneous polynomial, minimum prefix weight theta exceeding the degree B in other selected vector letters forces D_A^(theta−B) divisibility over every field. The proof uses the generic determinant prime and a kernel-adapted cocharacter; quotient degree and OR1 permit iteration. Unit-leading-coefficient division descends the quotient to every integral domain, preserving all prefix bounds.",
    refs("ObjPol", ["Pol"], "exact_homogeneity_definition")
    + w(["otherVectorDegree", "FieldMultidegreeDivisibility", "IntegralToFieldBaseChange", "GaussQuotientIntegral"], "interfaces_reconstructed")
    + w(["determinant_coefficients_units", "gauss_of_det_coefficients", "gauss_quotient_integral",
         "laurent_coordinate_embedding_injective", "laurentRingMap_injective",
         "twist_substitution_natural", "valuation_fraction_field_extension"], "parallel_source_facts")
    + pw("DvDegOtherMono", ["dv_quot_hom", "dv_eA", "dv_detA_hom", "dv_detA_ne", "dv_div_one"], "exact_integral_extraction_target"),
    dependencies=["OR1"],
    assumptions=["Finite signed letter family over a field, or an integral domain after fraction-field extension.",
                 "All chosen determinant rows are distinct vectors lying in the division subset; F is letter-multihomogeneous."],
    status="derived_simplification",
    note="Proves the previously abstract hE input itself. The generic determinant irreducibility proof is included and works in every characteristic; the integral descent does not require the base domain to be a UFD.")

claim("OR3", "Overlapping tasks and the literal segment divisor",
    "A finite list of determinant tasks of total exponent T can be extracted if every initial task prefix has minimum at least its other-vector degree plus T. Each quotient has weakly smaller degrees and every prefix loses at most T. For actual segments the tasks are one recent-r-even determinant per late letter plus the preceding-frame determinant; their total cost is <=mStar, and their quotient satisfies exactly MGen0.",
    pw("DvDegOtherMono", ["dv_degOther_mono", "dv_div_list", "dv_eL_lt", "dv_eL_inj", "dv_eL_mem", "dv_eL_surj",
        "dv_ev_dec", "dv_ev_mem", "dv_len", "dv_Arow_get", "dv_Arow_anti", "dv_Arow_inj",
        "dv_Arow_newer", "dv_Arow_ge", "dv_mem_letters", "dv_mem_nonW", "dv_Arow_letter",
        "dv_frame_letter", "dv_last_nonW", "dv_W_frame", "dv_nonW_image", "dv_plnm_det",
        "dv_degOther_le", "dv_segment"], "literal_task_and_segment_proof")
    + pw("GeneratorImageIsSymbol", ["Mj", "eL", "LLs", "nonW", "plnm", "CondM", "MGen", "MGen0", "Dseg", "Wseg", "Dv", "Ctx.m1", "Ctx.m2"], "literal_family_definitions")
    + refs("SourceCleaning", ["evensBefore", "Arow", "mStar"], "exact_search_and_budget_definitions")
    + w(["divisions_le_total_budget", "segment_divisions_le_bound"], "exact_total_cost"),
    dependencies=["OR1", "OR2", "FG7"],
    assumptions=["The exact Valid frame, even positive n′, r,K>0, and a late letter.",
                 "The per-task strict-prefix valuation inequality; OR4–OR5 supply it in the actual application."],
    note="The old-frame task uses a prefix containing only those r rows and hence has other-vector degree zero. All selected rows lie inside the segment; no default Arow branch is used. This proves dv_segment rather than merely invoking its hE premise.")

claim("OR4", "The actual one-sided other-vector degree is at most Bo/80",
    "Every even predecessor outside the r nearest ones is before the oldest of them and lies in the old frame or intermediate letter set. Its even distance is 2h for a distinct h>=1. The one-sided total-degree upper bound gives other degree <=2.02 Bo/(p^2−1)<=Bo/80 for p>=13, with no lower approximation assumption.",
    pw("GeOldest", ["geN", "ge_N_lt", "ge_N_inj", "ge_Arow", "ge_oldest", "ge_frame", "ge_older"], "exact_order_geometry")
    + refs("SegRing", ["letters", "IsW", "LLset", "oldest"], "literal_segment_sets")
    + refs("SourceCleaning", ["levDeg", "Bo"], "exact_normalized_degrees")
    + os(["RestGeomU", "restGeomU"], "exact_one_sided_statement_and_proof"),
    dependencies=["FG7"],
    assumptions=["p>=13, even positive n′, r>=2, Valid frame; a<=deg_s<=2a on TT.",
                 "Only d_y<=1.01 levDeg(y) on old-frame and intermediate letters is assumed."],
    note="The finite sum is bounded by the full geometric series over distinct positive even distances. This proves the outgoing RestGeomU version, not just the absolute-error RestGeom statement.")

claim("OR5", "Explicit C>=100 extraction margin for the actual data",
    "From the exact mStar definition, alphaMax<=1+rkQ, N1<=k and r,k>=2, one has mStar<=8rk²QcP. The actual size bound a>=Ck³r²NQ⁵cPY and oldest degree Bo>=a/Q imply mStar<=Bo/100 for C>=100. The exact floor slack is <=Bo/8, so Bo/2−sl>=Bo/80+mStar. Thus every actual MGen factors through Dv and MGen0.",
    refs("SourceCleaning", ["alpha", "alphaMax", "cPrime", "mStar", "sl", "HypII"], "exact_budgets")
    + refs("ScaleEdges/ManyEdges", ["Hyps"], "actual_application_hypotheses")
    + pw("GeneratorImageIsSymbol", ["Ctx"], "actual_context")
    + w(["twist_alpha_le_bound", "alphaMax_le_bound"], "source_alpha_bound")
    + w(["numeric_symbol_bound_real"], "universal_existential_constant_route_replaced_in_actual_application")
    + os(["RestDivMU", "restDivMU"], "exact_one_sided_extraction_target"),
    dependencies=["OR3", "OR4", "FG7", "CP1"],
    assumptions=["r,k>=2, Y>=r, N>=1, Q>=1, cP>=1, N1<=k, alphaMax<=1+rkQ.",
                 "Valid frame span z_j−f_(j−1,0)<=G′ and Q=p^G′.",
                 "a>=Ck³r²NQ⁵cPY with C>=100 and a<=deg_s<=2a on TT."],
    status="derived_simplification",
    note="This supplies the exact actual application with an explicit constant and weaker needed margin. It does not claim an optimized universal OneSidedLemma4 constant triple. No mStar<=sl premise or dropped floor is used.")

claim("OR6", "Whole-letter projection gives RestModel and integral quotient symbols",
    "Projecting the defining XX′ product span to fixed whole-letter degrees gives a finite integral sum of exact MGen products: generic substitution preserves each letter degree and its prefix bounds. The final order-support intersection is only forgotten for this inclusion. OR5 and completed IP6/IP11 then give xi=Dv xi′ with phi(xi′) in the actual symbol algebra.",
    refs("SegRing", ["XX'", "geR", "phSeg"], "literal_constrained_space")
    + pw("GeneratorImageIsSymbol", ["RestModel", "GeneratorSpanInclusion", "GeneratorImageIsSymbol", "Sy", "SyS", "Ctx.SyS"], "exact_input_and_output_interfaces")
    + pw("MdWeightMapDomain", ["md_twist_rename", "md_sDegs_rename", "md_sDegs_comp", "md_val_comp", "md_lam_comp",
          "md_val_tr", "md_lam_tr", "GenM", "MGenM", "md_comp_gen", "restModel"], "projection_and_reindexing_proof")
    + pw("Lemma4OfRemainingStatements", ["SyS_of_span", "good_of_span"], "integral_linear_assembly")
    + pw("FixedSymbolFactorIntegral", ["Sy_mul", "Sy_IT", "SyS_of_Sy", "SyS_mul", "SyS_prod", "IT_C"], "closure_facts"),
    dependencies=["OR5", "IP3", "IP4", "IP6", "IP11"],
    assumptions=["The exact XX′ membership and whole-letter homogeneity of the outgoing xi family.",
                 "The already reconstructed integral path-generator spanning and image statements IP6/IP11."],
    note="No integral irreducible decomposition or termwise factorization of the final XX′ support intersection is asserted. The inclusion into MGen follows directly from homogeneous projection.")

claim("OR7", "The literal RestPh congruence and residual exponent arithmetic",
    "Universal Frobenius determinant congruence modulo p and the binomial split give phi(Dseg_x)^m1 divisible modulo p^c by D_barx^(m1−c), and similarly the old-frame factor. Late intervals cover each TT residue once; cyclic frame reindexing and m1−c=(2Q+3)c+kQ, m2−c=c(alphaMax+1) yield product phi(Dv)=fixedSymbolFactor(c) DkQ H+p^cY with H integral tangential and Y integral.",
    pw("GeneratorImageIsSymbol", ["Ctx.sb", "Ctx.fixedSymbolFactor", "Ctx.DkQ", "RestPh"], "exact_identity_target")
    + refs("SourceCleaning", ["Qj", "alpha", "R0", "DtopProd"], "exact_frame_and_fixed_factors")
    + w(["topPairingMatrix", "bc_IT", "bc_St"], "actual_tangential_objects")
    + pw("PhProdShift", ["ph_Arow_shift", "ph_z_step", "ph_z_mono", "ph_mem_nonW", "ph_prod_tops", "ph_prod_shift"], "period_and_product_reindexing")
    + pw("SymbolGeneratorData", ["ph_det_pow", "ph_det_pow_sub", "Spl", "Spl_pow", "Spl_one", "Spl_mul", "Spl_prod",
         "Ctx.SS", "Ctx.DsO", "Ctx.DlM", "Ctx.DlO", "ph_T_mem", "ph_DsO_mem", "ph_DsO_map",
         "ph_DlM_mem", "ph_DlO_mem", "ph_DlO_map", "ph_DlO_period", "ph_Dseg", "ph_Wseg", "restPh"], "complete_actual_congruence_proof"),
    dependencies=["FG7"],
    assumptions=["The exact Ctx frame/chart/coefficients, any nonnegative c, and m1/m2 as defined.",
                 "Frobenius is used as a ring endomorphism modulo p; no arbitrary coefficient is asserted fixed under it."],
    note="This proves the actual outgoing multiplier identity. It keeps the p^c error and nonnegative residual powers c(alphaMax−alpha_j); it is not replaced by the ordinary SPtrue multiplier assertion.")

claim("OR8", "Actual monPh symbols have the required integral separated realization",
    "Combining quotient symbols and RestPh gives monPh=Z fixedSymbolFactor(c)+p^cY′ with Z in the key-symbol algebra and Y′ integral. SY4 handles the fine-label factor. Normal-degree projection and completed SY5 finite correction give an integral F_o with own-chart error w^(o+c), order w^(o+c) on every other plane, and every prescribed position multidegree. Since p=w², the remaining error is w^(o+2c). This proves the actual outgoing OneSidedLemma4 application for C>=100.",
    refs("SourceCleaning", ["OHyp", "TwistBound", "CommonHypotheses", "monPh", "Realisable"], "exact_full_input_and_output")
    + refs("SegRing", ["IsLabel"], "actual_fine_digit_condition")
    + pw("GeneratorImageIsSymbol", ["RestMon"], "completed_SY4_input")
    + pw("FixedSymbolFactorIntegral", ["hom_iff", "SyS_comp", "inWj_compN", "fixed_symbol_factor_integral", "terms_of_agen", "core"], "actual_projection_and_cleaning_assembly")
    + os(["OneSidedLemma4", "one_sided_lemma4_of_interfaces", "lemma4_of_one_sided"], "exact_one_sided_target_and_assembly"),
    dependencies=["OR1", "OR2", "OR3", "OR4", "OR5", "OR6", "OR7", "SY4", "SY5", "IP6", "IP11", "CP1"],
    assumptions=["Exact actual Type-II frame, coefficients, chart and one-sided xi hypotheses, with the explicitly stated C>=100 inequalities.",
                 "Fine label supported on TT and normal-homogeneous monPh of degree o.",
                 "The previously reconstructed SY4 and SY5 key construction and finite correction."],
    note="The local application is complete without assuming LargePrimeLengthVanishing or OneSidedLemma4. It does not assert global abundance of the input Type-II data or a completed RH/GRH proof.")

out = dict(
    schema_version="1.2", artifact_version="0.8", date="2026-11-21",
    owner="/root/lean_audit", repository=dict(url=REPO, commit=COMMIT),
    range_convention="One-indexed inclusive declaration ranges. Full files are compared with pinned Git blobs and exact unnormalized range bytes are hashed.",
    verification=dict(full_file_bytes_compared_with_pinned_git_blob=True,
        range_bytes_hashed_without_normalization=True, human_mathematical_proofs_supplied=True,
        lean_source_files_edited=False, local_lean_compilation=False, lean_kernel_replay=False,
        replacement_arguments_formalized=False),
    status_definitions=dict(
        faithful_translation="Complete human proof of the exact source assertion in the stated actual setting.",
        derived_simplification="Directly proved replacement or sharper numerical argument, with its exact source counterpart and application scope identified.",
        remaining_input="Unexpanded specialized premise; no OR claim retains this status."),
    claims=claims, files=[files[path] for path in sorted(files)],
    reused_completed_inputs=[
        dict(ids=["FG7"], artifact="v0_8/frame_geometry/provenance.json", role="actual frame geometry"),
        dict(ids=["IP3", "IP4", "IP6", "IP11"], artifact="v0_5/path_generators/provenance.json", role="integral path basis and actual generator span/image"),
        dict(ids=["SY4", "SY5"], artifact="v0_4/symbols/provenance.json", role="label keys and finite correction"),
        dict(ids=["CP1"], artifact="v0_8/cloud_parameters/provenance.json", role="actual numerical input supply; OR5 independently proves the extraction comparison"),
    ],
    outside_scope=[
        "An optimized constant triple for the universal bare OneSidedLemma4 interface; the exact actual application has the proved threshold C>=100.",
        "Global orbit abundance and simultaneous global supply of the Type-II data.",
        "Separate Type-I and later global RH/Dirichlet-GRH inputs."
    ],
    independent_reviews=[
        dict(reviewer="/root/remarks_math", scope="OR1–OR3 generic determinant, integral descent and overlapping tasks",
             result="No mathematical correction found; generic specialization over every field, rank-one update, multidegree iteration, integral monic division and cumulative budget checked."),
        dict(reviewer="/root/readable_sources", scope="OR7–OR8 versus literal RestPh, restPh and one_sided_lemma4_of_interfaces",
             result="No mathematical correction found; exact Frobenius error, exponents, product coverage, normal projection and Realisable endpoint checked.")
    ]
)
(OUT / "provenance.json").write_text(json.dumps(out, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
(OUT / "source_manifest.json").write_text(json.dumps(dict(repository=out["repository"], files=out["files"]), ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
locators = []
for c in claims:
    locators += [c["id"] + ": " + c["title"], "Status: " + c["status"]]
    for s in c["sources"]:
        locators += ["  " + s["declaration"], "  " + s["url"],
                     "  full-file SHA256 " + s["sha256"],
                     "  inclusive-range SHA256 " + s["range_sha256"]]
    locators.append("")
(OUT / "source_locators.txt").write_text("\n".join(locators), encoding="utf-8")
print(json.dumps(dict(claims=len(claims), source_files=len(files),
    source_references=sum(len(c["sources"]) for c in claims),
    statuses={status:sum(c["status"]==status for c in claims) for status in out["status_definitions"]},
    every_source_byte_checked_against_pin=True)))
