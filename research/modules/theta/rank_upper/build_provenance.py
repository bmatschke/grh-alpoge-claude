#!/usr/bin/env python3
"""Rebuild the exact pinned-source ledger for the v0.10 coarse upper-rank and HH-assembly proof.

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
GB = "src/Formalism/SharpRestriction/GrowthBounds/"
BR = GB + "BinomialRatio/"
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


def gb(file, names, role="proof"):
    return group(GB, file, names, role)

def br(file, names, role="proof"):
    return group(BR, file, names, role)


claims = []
BASE = [
    "The path-dimension calculations use a characteristic-zero fraction field K of a DVR O, r>=1 and k=r+1; the actual quadratic coefficient setting implies characteristic zero.",
    "Actual segments, compatible digits, kept blocks, levels and prefix cutoffs retain their literal definitions; all sets used in the counts have proved finite support.",
    "RU4-RU8 are pointwise under the literal Std(C0,Cde,CE1,CE2,H,X), H>=1. NP2 supplies this record uniformly; the numerical threshold theorem is not reproved here.",
    "The exact integral path basis and prefix adaptation are prior proved IP3-IP4; CB3 supplies the exact tableau dimension, and SW1/SW10 supply the named actual block and degree interfaces.",
    "Elementary field extension, polynomial coefficient algebra, finite-dimensional linear algebra and DVR/Smith normal form are declared classical background.",
]


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
    "RU1", "Actual SSZ block rank and its factorial-weighted lattice",
    "The actual block rank equals the sum over legal levels of dim(Y_level) h_r(B-j_plus). The factorial-weighted block lattice has exactly the same rational span and rank.",
    gb("ObjSeg", ["ChainLetters", "TieData", "BVar", "BlockData", "BlockData.lettersAt", "chainEmb", "xiVar", "scalZ", "scalS", "BlockData.Ehat", "BlockData.Eplus", "XiPolZ", "BlockData.LevelOK", "BlockData.gens", "BlockData.SSZ", "BlockData.withMargin", "blockData", "specConst", "bbSpec", "blockLat", "blockRank"], "literal_definition")
    + br("CountDefs", ["BlockRankAt", "sdXi"], "exact_interface")
    + br("BlockRank", ["pre", "ell", "Lv", "mem_Lv", "IF", "Ltot", "card_xi", "finrank_dom", "span_le_range", "range_le_span", "span_eq_range", "blockRankAt_of"])
    + br("BlockInj", ["tau", "rho", "rho_tau", "tau_inj", "base", "ell_eq_tau", "ppi", "eExp", "ppi_base", "eExp_inj", "ltot_inj", "blockRankAt"], "source_injectivity_counterpart")
    + br("TotalDegreeEplus", ["smul_mem_bbSpec", "finrank_lattice"], "weighted_rank_counterpart"),
    dependencies=["SW1"], status="derived_simplification",
    note="The lexicographically largest S-monomial proves the actual multiplication map injective directly, replacing the source's localization inverse. Weighted and ordinary coefficient lattices are not identified.",
)

claim(
    "RU2", "Literal prefix dimension and finite signed-chain mass",
    "DimYAt and ChainDimAt hold for the actual signed word and prefix space: dim Y is the finite sum of D_r(endpoint) over paths obeying all first-row cutoffs; without cutoffs it is the product of symmetric-power dimensions.",
    gb("ObjSeg", ["chPol", "chWt", "chStable", "YCond", "Yjt", "YjtZ"], "literal_prefix_space")
    + br("CountDefs", ["Strip", "wdim", "IsChain", "ChainOK", "chainSum", "DimYAt", "StWeylAt", "ChainDimAt", "chainCount"], "exact_count_definitions")
    + br("CardEqChainSum", ["strip_iff", "pathOf", "chain_of_path", "clear_den", "ycond_zero_top", "ycond_zero_bot", "psiR", "psiR_map", "psiK_li", "psiK_mem", "tx_finite", "exists_bound", "sK", "one_cond", "sAll", "map_span", "span_eq_Yjt", "fiber_card", "card_eq_chainSum", "dimY_of"], "source_path_and_prefix_counterparts")
    + br("ChainDim", ["card_tuples", "monoEquiv", "finrank_Pol", "chainDim_of"])
    + br("RankOnDigitsCast", ["segTies_J_le", "blockRank_cast", "rankOnDigits_cast"]),
    dependencies=["RU1", "IP3", "IP4", "CB3"],
    note="IP3-IP4 replace the source's admitted HyperplaneRank/DefiniteRankOne interface by the already reconstructed exact basis. The characteristic-zero Lie/group comparison is proved explicitly. Finiteness comes from coordinate bounds, not from a nonzero formal infinite sum.",
)

claim(
    "RU3", "Exact interlacing branching and terminal hockey-stick sum",
    "For every dominant integer weight nu of length r+1, D_(r+1)(nu)=sum_interlacing_lambda D_r(lambda), and sum_(j=0)^B h_r(B-j)=h_(r+1)(B).",
    br("CountDefs", ["NumBranchAt", "StWeylAt"], "exact_interfaces")
    + br("StWeyl", ["wdim_shift", "wdim_nat", "antitone_of_interlace", "numBranch_of", "stWeylAt"], "source_dimension_counterparts")
    + br("CountUp", ["hockey", "hockey_fin", "Inter", "inter_anti"]),
    dependencies=["CB3"], status="derived_simplification",
    note="The direct discrete-Vandermonde/tableau argument reuses proved CB3, bypassing the source's adm2/adm3 branching interfaces. A common determinant shift handles signed weights without changing dimensions.",
)

claim(
    "RU4", "Actual early partial widths lie below every neighboring cap",
    "Under Std(H>=1), for every early i and n<=i+1, sum_(l<=i) w_l<=cap_n. The proof retains the exact digit quotients and does not assume early cap monotonicity.",
    gb("ObjSeg", ["SegData", "SegBlock", "SegData.P", "SegData.Qj", "SegData.A0", "coarseA", "coarseC", "oEff", "cap", "DigitsOK", "Kept"], "literal_numeric_data")
    + br("Transported", ["be", "Std"], "literal_parameter_record")
    + br("CoarseDegreeAlternative", ["coarse_bounds", "eps", "Std.kQ", "coarse_degree_alternative"], "prior_SW10_and_digit_bounds")
    + br("AiAddMulLeA0", ["coarse_ratio_small", "Ai_add_mul_le_A0", "partial_width_le_cap", "top_rows_bound_holds"])
    + br("LeAndHalfLeProdOneSubExpNegOfBounds", ["Std.half_ratio_le_segment_base_of_std"], "head_degree_lower_bound")
    + br("ThresholdLowerBounds", ["one_le_level_alt", "k5", "Q1", "apos", "ba", "Hb1"], "literal_Std_consequences"),
    dependencies=["SW10"], status="derived_simplification",
    note="The report shortens the cap arithmetic using A_l<=2(A_i+k)/p, an available gap >34 epsilon A_* and added width <=3 epsilon A_*. It proves the exact source endpoint without changing constants.",
)

claim(
    "RU5", "All actual first-row conditions including early positions and endpoint",
    "Every actual residual chain satisfies kappa_(2i+1),0<=min(cap_i,cap_(i+1)) and kappa_(2s+1),0<=cap_s, including the literal floor(c-M) cutoffs for M>=0.",
    gb("ObjSeg", ["segChain", "uTop", "segmentCapacities", "segTies", "blockBase", "blockData"], "literal_chain_and_prefix_indices")
    + br("UpperCountOfTopRows", ["strip_first", "row_even", "row_odd", "SecondKernelAtLevel", "sTopRows_of", "LeadingRowsBeyondThreshold", "upper_count_of_top_rows"])
    + br("RestCountUpOfSTop", ["floor_sub_le", "thr_U", "thr_last", "STopRowsAt", "firstRows_of", "restFirstRows_of"])
    + br("SegmentChainDegreeEven", ["FirstRowsAt", "cap_zero", "cap_succ"]),
    dependencies=["RU4"],
    note="Late cap increments are nonnegative; early neighboring bounds use RU4. No unstated monotonicity or integer-floor replacement is used.",
)

claim(
    "RU6", "The explicit weight-preserving upper matching and full recovery",
    "Insert first entries c_i and c_i+A_i-d_(2i) into the residual path. The result is the unrestricted rank-(r+1) path for +A_*,+A_0,-C_0,...; retaining the endpoint and j_plus gives an injective matching of the actual block/level/path data.",
    br("CountUp", ["FinalTheorems", "BD", "SrcOK", "Fs", "mmLetters", "MatchUpAt"], "literal_source_and_target")
    + br("KLettersDegEven", ["strip_cons", "fstOf", "fstOf_odd", "fstOf_even", "muOf", "muOf_succ", "LevFacts", "kLetters_deg_odd", "kLetters_deg_even", "chain_of_facts", "LevFactsAt", "SrcInjAt", "muOf_inj", "matchUp_of"])
    + br("SegmentChainDegreeEven", ["jE", "tieSum", "lev_deg", "segment_chain_degree_even", "chain_deg_E", "chain_deg_U", "jE_S", "jE_top", "level_bounds", "cap_succ", "levW", "levE", "levU", "jE_at", "segBlock_ext", "srcInjAt", "levFactsAt_of", "restMatchUp_of"]),
    dependencies=["RU5"],
    note="The exact inverse recovers residual degrees, early w/sg, late j/o, terminal o_plus, fixed digits and zero fields. The terminal endpoint and level must remain in the target; omitting them would invalidate the count.",
)

claim(
    "RU7", "Evaluate the upper target weight with no multiplicity loss",
    "The sum of source path weights is at most h_(r+1)(A_*) product_i h_(r+1)(A_i)h_(r+1)(C_i) h_(r+1)(B), by the exact finite weighted injection and three successive counting identities.",
    br("CountDefs", ["CountUpAt", "RestCountUp"], "exact_count_endpoint")
    + br("CountUp", ["finsum_le_of_inj", "finsum_curry3", "wdim_pos", "Tgt", "Inter", "Gt", "Gt_nonneg", "chains_finite", "Gt_support_finite", "Gt_sum", "kLetters", "prod_kLetters", "chainCount_eq", "countUp_of", "restCountUp_of"]),
    dependencies=["RU2", "RU3", "RU6"],
    note="First sum terminal j_plus, then interlacing endpoints, then unrestricted chains. All weights are nonnegative and all contributing sets finite. The exact terminal factor is retained.",
)

claim(
    "RU8", "The actual UpAt and SW8 coarse upper rank are closed",
    "For every actual compatible digit class and every real M>=0, rankOnDigits<=mmB under literal Std(H>=1). With NP2's uniform supply, this is UpAt/RestUp in the original constant order; at M=0 it is ExtendedDigitRankBound, the upper premise of SW8.",
    gb("ColumnSystems", ["symDim", "dimMM", "digitBlock", "rankOnDigits", "ExtendedDigitRankBound"], "literal_target")
    + br("RankDefs", ["sd", "mmB", "UpAt", "RestUp"], "exact_upper_package")
    + br("RankOnDigitsCast", ["cast_finsum", "blockRank_cast", "rankOnDigits_cast", "restUp_of"])
    + br("FinrankTensor", ["charZeroAt"], "actual_characteristic_zero_check")
    + br("Transported", ["TransportedAlt", "TransportedAlt.of_explicit"], "ordered_uniform_quantifiers")
    + br("ThresholdLowerBounds", ["T2", "std_of"], "companion_NP2_numeric_supply")
    + gb("BinomialRatio", ["extended_fourth_of_upper_bound", "restUp_of_adm"], "source_export_counterparts"),
    dependencies=["RU1", "RU2", "RU7", "NP2"],
    note="T0=T1=1 and T2=1000(CE1+CE2+1)(Cc+1) apply to the source upper package; Cm is unused. The report explicitly delegates proof of uniform Std to NP2 rather than counting a wrapper as a new proof.",
)

claim(
    "RU9", "Exact digit summation, first-head recovery and full HH rank mass",
    "Using RD9, C0>=880 and Std(H=4), every M>=0 and Ckap>=3 satisfy (1-kappaMarginBound)dimHH<=gaussian(q,k) product_j segRank_j(M). The small-loss case supplies its own lower-margin condition; the other case has nonpositive target mass.",
    br("RankDefs", ["lowFac", "LowAt", "SegLowAt", "DimHHAt"], "exact_lower_and_dimension_interfaces")
    + br("SegLow", ["dset", "card_tuple", "digit_sum", "symDim_nat", "sum_prod_sd_digits_eq_prod_sd", "segLow_of", "restSegLow_of"])
    + br("FirstCoefficientFacts", ["choose_ratio", "Ne_ge", "four_fac", "symDim_toNat", "prod_letters", "seg_num", "ratio_num", "chain_num", "brk", "kap_eq", "first_coefficient_facts", "seg_step", "rank_alternative_lower", "restAlt2_of"])
    + br("OtherStart", ["rot", "rot_bij", "next_eq", "prod_next", "segG_eq", "sum_segG", "prod_starts", "pos_spec", "prod_pos", "odd_covered", "biUnion_odd", "prod_tops"], "literal_cyclic_partition")
    + br("SegmentStatementHolds", ["oddSet", "oddSet_disj"], "literal_segment_disjointness")
    + gb("ObjSeg", ["segStart", "segNext", "segG", "segDists", "segPos", "segData", "letterWt", "hhDeg", "hhWt", "VHH", "dimHH", "kappaMarginBound"], "literal_HH_and_margin_definitions")
    + br("FinrankTensor", ["prodUp", "prodDown", "wprod_vec", "wprod_cov", "finrank_letter", "finrank_tensor", "dimHH_of"], "exact_tensor_dimension_counterpart")
    + br("ThresholdLowerBounds", ["numSeg_le_card"], "segment_count")
    + gb("ColumnSystems", ["ExtendedModelRank"], "literal_endpoint"),
    dependencies=["RU1", "RU2", "CB3", "RD9", "NP2"], status="derived_simplification",
    note="Coordinatewise exponent division proves the exact digit identity. The shortened numeric proof retains the source loss 3*B and Ckap>=3. Actual VHH dimensions use the existing CB3 basis, with no replacement model or admitted Weyl dimension input.",
    extra=["The fully closed lower-count application uses C0>=880, Std(H=4), and RD9. The arithmetic conversion needs only Std(H>=1) once LowAt is supplied."],
)

claim(
    "RU10", "Actual finite free weighted lattices, rank equality and block Smith partners",
    "The actual segLat is finite free with rank=segRank. Every actual GoodSub of rank g at D>=0 yields g single-block-supported orthogonal pairs with nonzero integral diagonals of v_p<=D, proving RkAt and PartnersToFactorsAt.",
    gb("ObjSeg", ["bbSpec", "specConst", "blockLat", "segLat", "segForm", "SatIn", "PrimIn", "GoodSub", "GoodShare", "blockRank", "segRank"], "actual_lattices_and_partner_premise")
    + br("KeptFin", ["kf_coarseA_le", "kf_coarseC_le", "kf_cap_le", "kf_kept_finite"])
    + br("TotalDegreeEplus", ["degBound", "gens_totalDegree", "spanSSZ_le", "spanSSZ_finite", "Vb", "finrank_lattice", "finrank_segLat", "rkAt_all", "restRk"])
    + br("BlockFG", ["vK_wpow", "bb_coeff", "fg_inter", "blockFG_all", "smithAt_all", "partners_to_factors_holds"])
    + br("FockZeroRight", ["smith_block", "span_single", "smithData_seg"])
    + br("PartnersFactorsOfKernelSmith", ["SmithData", "scale_to_O", "blockDiag_of_smith", "CountSmithAt", "partners_factors_at_of_smith", "rank_le_of_ker", "prim_div", "ker_core", "segForm_bilin", "partners_factors_of_smith_bases"])
    + br("ExtendedStatementOfParts", ["RkAt", "BlockDiag", "PartnersToFactorsAt"], "exact_endpoints"),
    dependencies=["RU1"], status="derived_simplification",
    note="The direct coefficient valuation check proves the actual form integral on the weighted lattice, simplifying the source's fractional Smith normalization. The primitive-kernel contradiction uses the actual saturation clause and retains block support.",
    extra=["Actual quadratic setting with uniformizer w satisfying w^2=p and normalized valuation v_p(w)=1/2. GoodSub is supplied data; this claim does not assert arbitrary large good shares."],
)

claim(
    "RU11", "Actual paired lift assembly and the pre-transport HH RhoGE certificate",
    "For supplied GoodShare data D_j,kappa_j>=0 and c>4D*, D*=sum_j D_j+4kappa0, the actual CCe/CCe' at floor(t0) have RhoGE depth D* and mass (1-kappaP-sum_j kappa_j)dimHH/gaussian(q,k). This is HerrExtensionClass / aux3 before harmonic transport.",
    gb("ObjSeg", ["AHH", "beHH", "CCe", "CCe'", "vLEO", "FactorsLE", "RhoGE"], "literal_normalization_and_certificate")
    + gb("ColumnSystems", ["m0", "kap0", "kapP", "t0", "DjHyp", "aux₃", "HerrExtensionClass"], "actual_caller_and_mass")
    + br("PairLift", ["FamOK", "PairLiftAt", "vLEO_mul", "vLEO_prod", "liftVecAt_of", "restLiftVec_of"])
    + br("FactorsOfPerturb", ["nv_irr", "ramE_two", "vLEO_iff", "eq_unit_pow", "isUnit_one_add", "factors_of_perturb", "liftAt_of", "restLift_of"])
    + br("ExtendedStatementOfParts", ["LiftAt", "LiftVecAt", "kapP_nonneg", "Ne_pos", "extended_statement_of_parts", "restExt_of"]),
    dependencies=["RU9", "RU10", "RL11", "NP2"], status="derived_simplification",
    note="The proof checks both off-diagonal block-pattern cases, then explicitly inverts I+E over O and scales to one diagonal value. It retains p^AHH, w^2=p, source precision c>4D*, and all CCe/CCe' conditions. It gives a supplied-GoodShare theorem, not an unproved assertion of those data.",
    extra=["For the actual combined application: C0>=880, Std(H=4), CE1,CE2,Cm>=17, Ct>=30 and RL11's actual kept/order premises as supplied by NP/RL.",
           "Final depth D0 and loss kx require the separately proved numerical choices of GoodShare data; harmonic transport and global RH/GRH are outside RU."],
)

reviews_path = OUT / "independent_reviews.json"
reviews = json.loads(reviews_path.read_text()) if reviews_path.exists() else []
unique_ranges = {(s["path"], s["line_start"], s["line_end"]) for c in claims for s in c["sources"]}
artifact_files = {p.name: hashlib.sha256(p.read_bytes()).hexdigest()
                  for p in [OUT / "main.tex", OUT / "report.txt", Path(__file__).resolve()]}
out = dict(
    schema_version="1.2", artifact_version="0.10", date="2026-11-21", owner="/root/lean_audit",
    repository=dict(url=REPO, commit=COMMIT),
    range_convention="One-indexed inclusive declaration ranges; exact source bytes are compared with the pinned Git blob and range bytes are hashed without normalization.",
    verification=dict(full_file_bytes_compared_with_pinned_git_blob=True, range_bytes_hashed_without_normalization=True,
                      human_mathematical_proofs_supplied=True, lean_source_files_edited=False, local_lean_compilation=False,
                      lean_kernel_replay=False, replacement_arguments_formalized=False),
    status_definitions=dict(
        faithful_translation="A complete human proof of the precise cited source assertion, with named already-proved companion inputs.",
        derived_simplification="An explicitly proved shorter route or harmless strengthening with exact source counterpart and unchanged application constants.",
        remaining_input="A genuinely unexpanded input; no new RU local proof claim has this status. Supplied-data hypotheses are stated explicitly."),
    independent_reviews=reviews, claims=claims, files=[files[p] for p in sorted(files)],
    artifact_sha256=artifact_files,
    prior_components_reused=[
        dict(ids=["IP3", "IP4"], component="v0_5/path_generators", role="Literal integral signed-path basis and simultaneous prefix adaptation."),
        dict(ids=["CB3"], component="v0_6/complementary_basis", role="Exact standard-tableau / discrete-Vandermonde dimension and branching."),
        dict(ids=["SW1", "SW10"], component="v0_9/segment_weighted", role="Actual level multiplication and early/late degree alternative."),
        dict(ids=["RL11"], component="v0_9/paired_lifts", role="Actual CCe/CCe' paired lifts with p^AHH normalization and controlled scalar/error."),
    ],
    same_iteration_companions=[
        dict(ids=["NP2"], role="Uniform Std(H=4) and its weaker H=1 record in the original constant order."),
        dict(ids=["RD9"], role="Actual fixed-digit LowAt with exact exponential and terminal-margin factors."),
        dict(ids=["HM6"], role="Consumes the RU11 HH RhoGE certificate after companion depth/loss specialization."),
    ],
    historical_boundary_resolved=[
        dict(id="SW8", boundary="Actual coarse upper-rank premise only", discharged_by=[f"RU{i}" for i in range(1,9)]),
        dict(id="TI9", boundary="Coarse upper rank and actual segment-to-HH assembly; global and harmonic branches remain separately traced", discharged_by=[f"RU{i}" for i in range(1,12)]),
    ],
    scope_precision=[
        "RU1-RU8 do not infer a prefix-filtered dimension from an unrestricted ambient dimension; the literal lattice/path identification is proved.",
        "RU9 uses the independently proved RD9 lower count, not RU8 alone; its nontrivial case supplies the lower-margin condition.",
        "RU10 proves weighted finite generation and rational rank before Smith form, and selected pairs preserve individual block support.",
        "RU11 is the complete actual assembly for supplied GoodShare data; their final numerical choice is a separate companion theorem.",
        "No global RH or Dirichlet-GRH proof closure, formal replay, or source-code modification is asserted.",
    ],
    outside_scope=["Final numeric GoodShare depth/loss specialization and averaging (SW/RD/NP).",
                   "HH-to-harmonic transport and edge KeyIneq (HM).",
                   "Global orbit abundance, arithmetic windows and analytic completion of RH/Dirichlet-GRH."],
)
(OUT / "provenance.json").write_text(json.dumps(out, ensure_ascii=False, indent=2)+"\n")
(OUT / "source_manifest.json").write_text(json.dumps(dict(repository=out["repository"], files=out["files"]), ensure_ascii=False, indent=2)+"\n")
locators=[]
for c in claims:
    locators += [c["id"]+": "+c["title"], "Status: "+c["status"]]
    for s in c["sources"]:
        locators += ["  "+s["declaration"], "  "+s["url"], "  full-file SHA256 "+s["sha256"], "  inclusive-range SHA256 "+s["range_sha256"]]
    locators.append("")
(OUT / "source_locators.txt").write_text("\n".join(locators))
print(json.dumps(dict(claims=len(claims), source_files=len(files), source_references=sum(len(c["sources"]) for c in claims), unique_ranges=len(unique_ranges))))

