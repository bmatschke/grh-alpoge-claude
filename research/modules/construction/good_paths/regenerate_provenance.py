"""Regenerate GP1--GP12 provenance from byte-identical pinned Lean sources.

Run with Python 3.11+ from any directory. No network or Lean build is used.
Ranges are inclusive, one-indexed lines, retaining original line endings.
Qualified names are lexical; private names can differ internally in Lean.
The report and TeX are human reconstructions, not new Lean formalizations.
"""
from pathlib import Path
from hashlib import sha256
import json
import re
import subprocess

WORK = Path(__file__).resolve().parent
REPO = WORK.parents[1] / "alpoge-rh"
COMMIT = "7cbf7a0c32fca1badf05931879a37c3f8a2b03b4"
URL = "https://github.com/CocoSgt/riemann-hypothesis-lean"
GB = "src/Formalism/SharpRestriction/GrowthBounds/"
PATHS = {
    "OBJ": GB + "ObjPol.lean",
    "SEG": GB + "SegRing.lean",
    "HYP": GB + "SegmentDegree/NonemptyDvrSettingOfStandard.lean",
    "COARSE": GB + "SegmentDegree/Coarse.lean",
    "RC": GB + "SegmentDegree/RestCountOf.lean",
    "GOOD": GB + "SegmentDegree/GoodPathWeight.lean",
    "ATYP": GB + "SegmentDegree/AtypicalPathSmallWeight.lean",
    "DICT": GB + "SegmentDegree/DistAddTwoLeOfSameVec.lean",
    "NUM": GB + "SegmentDegree/FourHundredSixteenLeA.lean",
    "GEO": GB + "SegmentDegree/CardFinRange.lean",
    "OLD": GB + "SegmentDegree/SortGetDSpec.lean",
    "TOTAL": GB + "SegmentDegree/ProdFromSelfEqOne.lean",
    "TAUC": GB + "SegmentDegree/DomOfStripDown.lean",
    "WIN": GB + "SegmentDegree/WindowSmall.lean",
    "LET": "src/Formalism/ThetaLogCoordinates/ResidueClassEstimates/Letters.lean",
    "STMT": "src/Formalism/ThetaLogCoordinates/ResidueClassEstimates/StatementT.lean",
    "TAIL": "src/Formalism/ThetaLogCoordinates/ResidueClassEstimates/VandermondeRankEstimates/N0LeNs.lean",
    "LOG": "src/Formalism/ThetaLogCoordinates/ResidueClassEstimates/VandermondeRankEstimates/LogBinomialProperties.lean",
    "WEYL": "src/Formalism/ThetaLogCoordinates/ResidueClassEstimates/VandermondeRankEstimates/LogWeylDimensionEstimate.lean",
    "ABAD": "src/Formalism/ThetaLogCoordinates/ResidueClassEstimates/VandermondeRankEstimates/AtypicalWeightBoundOf.lean",
    "FINAL": "src/Formalism/ThetaLogCoordinates/ResidueClassEstimates/FinalT.lean",
    "TRANS": GB + "SegmentDegree/TypOfTypical.lean",
    "ORD": GB + "SegmentDegree/TypicalPathOrdersSmall.lean",
    "GPARTS": GB + "SegmentDegree/GoodPathWeightOfParts.lean",
    "GTOP": GB + "SegmentDegree/GoodPathWeightOfTopCount.lean",
    "GALT": GB + "SegmentDegree/GoodPathWeightAlt.lean",
    "MEM": GB + "SegmentDegree/DiscPowerTimesMonomial.lean",
    "MEMA": GB + "SegmentDegree/DiscPowerMonomialMemSupported.lean",
    "MEMB": GB + "SegmentDegree/DiscPowerMonomialDegreeAtW.lean",
    "MEMCD": GB + "SegmentDegree/M0LeBwOfIsW.lean",
    "DPLUS": GB + "SegmentDegree/DplusLeBeS.lean",
    "DMIN": GB + "SegmentDegree/DminusLeBeS.lean",
    "KCOL": GB + "SegmentDegree/KillKcolTau.lean",
    "ICUT": GB + "SegmentDegree/MemColRangeOfLeEntry.lean",
    "CUT": GB + "SegmentDegree/CardIcutFilter.lean",
    "KEY": GB + "SegmentDegree/SumSingleApplyZero.lean",
    "LI": GB + "SegmentDegree/KillOfEmpty.lean",
    "IND": GB + "SegmentDegree/ScaleSCoeffZero.lean",
    "BETA": GB + "SegmentDegree/BetaRatioBound.lean",
    "MON": GB + "SegmentDegree/TauDegreeOnPathBound.lean",
    "FIN": GB + "SegmentDegree/FiniteRestrictSupport.lean",
    "CLOSED": GB + "SegmentDegree.lean",
}

PREFIX = r"(?:@\[[^\n]*\]\s*)?(?:(?:private|protected|noncomputable)\s+)*"
DECL = re.compile(r"^" + PREFIX + r"(?:def|theorem|lemma|abbrev|structure|inductive|instance)\s+(\S+)")
BOUNDARY = re.compile(r"^" + PREFIX + r"(?:def|theorem|lemma|abbrev|structure|inductive|instance|namespace|end|section|variable|attribute|open|include|set_option)\b")
NS = re.compile(r"^namespace\s+(\S+)")
SEC = re.compile(r"^(?:noncomputable\s+)?section(?:\s+(\S+))?\s*$")
END = re.compile(r"^end(?:\s+(\S+))?\s*$")
FILES = {}

for key, path in PATHS.items():
    raw = (REPO / path).read_bytes()
    pinned = subprocess.check_output(["git", "-C", str(REPO), "show", f"{COMMIT}:{path}"])
    if raw != pinned:
        raise ValueError(f"Working-tree bytes differ from pinned source: {path}")
    lines = raw.splitlines(keepends=True)
    stack = []
    declarations = []
    for i, rawline in enumerate(lines):
        line = rawline.decode("utf-8").rstrip("\r\n")
        if match := NS.match(line):
            stack.append(("namespace", match.group(1)))
        elif match := SEC.match(line):
            stack.append(("section", match.group(1)))
        elif match := END.match(line):
            if not stack:
                raise ValueError((path, i + 1, "unmatched end"))
            kind, label = stack.pop()
            if match.group(1) and match.group(1) != label:
                raise ValueError((path, i + 1, "end label mismatch", label, match.group(1)))
        elif match := DECL.match(line):
            name = match.group(1)
            ns = ".".join(label for kind, label in stack if kind == "namespace")
            declarations.append({"name": name, "line": i, "qualified": f"{ns}.{name}" if ns else name})
    FILES[key] = {
        "path": path,
        "sha256": sha256(raw).hexdigest(),
        "bytes": len(raw),
        "line_count": len(lines),
        "verified_equal_to_pinned_git_blob": True,
        "_lines": lines,
        "_declarations": declarations,
    }


def locator(key, name, role="parallel_source_proof", occurrence=0):
    item = FILES[key]
    hits = [decl for decl in item["_declarations"] if decl["name"] == name]
    if occurrence >= len(hits):
        raise ValueError((key, name, occurrence, "declaration not found"))
    decl = hits[occurrence]
    start = decl["line"]
    lines = item["_lines"]
    end = start + 1
    while end < len(lines) and not BOUNDARY.match(lines[end].decode("utf-8")):
        end += 1
    while end > start + 1 and not lines[end - 1].strip():
        end -= 1
    excerpt = b"".join(lines[start:end])
    if role == "parallel_source_proof" and re.match(r"^" + PREFIX + r"(?:def|abbrev|structure|inductive)\b", lines[start].decode("utf-8")):
        role = "definition_or_statement"
    return {
        "path": item["path"],
        "declaration": decl["qualified"],
        "source_spelling": name,
        "line_start": start + 1,
        "line_end": end,
        "role": role,
        "full_file_sha256": item["sha256"],
        "range_sha256": sha256(excerpt).hexdigest(),
        "range_bytes": len(excerpt),
        "pinned_url": f"{URL}/blob/{COMMIT}/{item['path']}#L{start+1}-L{end}",
    }


def many(key, names, role="parallel_source_proof"):
    return [locator(key, name, role) for name in names]


CLAIMS = [
    {
        "id": "GP1",
        "title": "Actual segment geometry and quantitative degree dictionary",
        "status": "proved_from_literal_Hyp_and_reconstructed_RS2_RS3",
        "statement": "The actual old/late/current-frame partition gives N>=3r, N<=Ns, oldest indices before n0, c_i-2kNs<=B_i<=c_i, k<=B_i<=2a/P_i, same-sign growth by p^2/5, earlier-degree bound B_l<=4(a/P_i)/p, h=K-2N>=k/2, and the exact logarithmic-size margins.",
        "sources": many("HYP", ["Dat", "Hyp", "k", "La"], "literal_hypotheses_and_constants")
          + many("SEG", ["Frames", "letters", "IsW", "LLset", "dist", "GapGt", "oldest", "Valid"], "literal_geometry")
          + many("COARSE", ["Rj", "Qc", "m0", "Bw", "thc", "oc"], "literal_constants")
          + many("GOOD", ["restr", "Bdeg", "beS", "BOK"], "literal_degree_family")
          + many("GEO", ["card_LLset", "two_r_le", "dict_lateV"])
          + many("OLD", ["exists_od"])
          + many("NUM", ["six_le_Ns", "a_big", "four_hundred_sixteen_le_a", "log_a_ge", "k_big", "c_bounds", "Bdeg_bounds"])
          + many("DICT", ["dist_cast", "dist_lt", "dist_add_two_le_of_same_vec", "beS_eq", "final_num", "letter_dictionary_bounds"]),
    },
    {
        "id": "GP2",
        "title": "Exact signed paths, endpoint weight, total count and finite path bound",
        "status": "proved_using_previously_reconstructed_Pieri_and_GT_counts",
        "statement": "For the literal IsPATH paths, the sum of standard-normal-array counts is the product R of the preterminal symmetric-power dimensions. Terminal head forcing becomes ordinary GT row interlacing. The number of paths is at most exp(2N^2 log(1+2aN)).",
        "sources": many("GOOD", ["IsPATH", "Tset"], "literal_actual_paths")
          + many("ATYP", ["IsPATHa", "rkA", "HypT", "SP", "SAll", "PathWeightEqRank", "PathCountFinite"], "generic_interface")
          + many("LET", ["HStrip", "Interl", "weylDim", "IsPATH", "stLen", "stage", "kaRows", "wt"], "generic_weight_definition")
          + many("TOTAL", ["pre_count", "path_weight_eq_rank"])
          + many("TAUC", ["tau_count"])
          + many("WIN", ["path_le_beA", "beA_le", "code", "path_count_finite"]),
    },
    {
        "id": "GP3",
        "title": "Complete tail-sum recursion and persistence of a deficit",
        "status": "complete_elementary_human_proof",
        "statement": "Positive and reversed-negative suffix sums are bounded by suffix sums of the corresponding reverse-chronological preterminal degree lists. Active steps shift the deficit index by one; opposite-sign and terminal interlacing steps preserve it without loss.",
        "sources": many("LET", ["tailPos", "tailNeg", "latestV", "latestC", "SPos", "SNeg"], "literal_tail_definitions")
          + many("STMT", ["PathTailBounds"], "exact_source_target")
          + many("TAIL", ["HStrip.tailPos_shift", "HStrip.tailPos_zero", "Interl.tailPos_le", "abs_bound", "deficit_persists_of_active_inactive_recursion", "frame_step", "vec_step", "cov_step", "pathTailBounds"]),
    },
    {
        "id": "GP4",
        "title": "Log-binomial suffix deficit by concavity and Abel summation",
        "status": "complete_elementary_human_proof",
        "statement": "For f_h(x)=sum_{t=1}^h log(1+x/t), every suffix deficit contributes a nonnegative derivative-difference coefficient, at least h/(4b_u) when b_u>=h and b_{u-1}>=4b_u. An X deficit costs Xh/(4b_u). Empty lists and zero padding are handled explicitly.",
        "sources": many("LET", ["fT", "fT'"], "literal_function_definition")
          + many("STMT", ["LogBinomialProperties", "LogBinomialDeficit"], "exact_source_targets")
          + many("LOG", ["fT_nat", "fT_hasDerivAt", "fT'_lower", "fT'_upper", "fT'_half", "fT_concave", "abel_tails", "logBinomialDeficit"])
          + many("ABAD", ["bracket", "key"]),
    },
    {
        "id": "GP5",
        "title": "Direct endpoint Weyl estimate with constant 6 instead of 9",
        "status": "new_elementary_strengthening_of_the_consumed_source_bound",
        "statement": "At the actual endpoint, separating zero/nonzero Weyl pairs proves log w<=sum f_h(positive parts)+sum f_h(negative parts)+6N^2 L. Two-nonzero pairs cost at most 2N^2 L and the extra zero distances at most 4N^2 L. Combined with log R>=sum f_h(B_i), a suffix deficit costs Xh/(4b).",
        "source_difference": "The 6N^2 endpoint bound is proved in the human report and is not asserted to be a verbatim Lean theorem. The source uses a general r,K,Ns,n log-Weyl estimate yielding 9N^2 in this application; its requested bound follows by weakening the human result.",
        "sources": many("LET", ["weylDim"], "literal_Weyl_normalization")
          + many("STMT", ["LogWeylDimensionEstimate", "LogRankEstimate"], "source_general_bounds")
          + many("WEYL", ["G", "G_split", "sum_pa_le", "logWeylDimensionEstimate"], "parallel_more_general_source_argument")
          + many("LOG", ["logRankEstimate"], "parallel_more_general_source_argument")
          + many("ABAD", ["pathWeightBound_of"], "source_endpoint_assembly_with_constant_9"),
    },
    {
        "id": "GP6",
        "title": "The three actual bad events and their complete weighted count",
        "status": "complete_human_reconstruction_with_stronger_intermediate_bound",
        "statement": "Mass-cancellation failures cost La*h/(16k), and failure of the oldest-plane-row threshold costs h/12. Finite path counting gives bad mass <=R exp(8N^2 L-min(La,k)/32), which implies the source's 11N^2 version and <=R/a^(Ns^2) under unchanged CLa,Ck>=1088.",
        "sources": many("ATYP", ["posS", "negS", "Xi", "Typ", "AtypicalPathSmallWeight", "LemT", "lemT_of"], "exact_typicality_and_assembly")
          + many("LET", ["Bo", "Typical"], "generic_source_typicality")
          + many("STMT", ["PathWeightBound", "AtypicalWeightBound"], "source_weight_bound_targets")
          + many("ABAD", ["a_fin", "pathWeightBound_of"])
          + many("TRANS", ["oldest_threshold_eq", "threshold_letter_eq_Xi", "typ_of_Typical", "atypical_path_small_weight"])
          + many("FINAL", ["lemma_t_one"], "source_closed_tail_export")
          + many("DICT", ["final_num"]),
    },
    {
        "id": "GP7",
        "title": "Typical paths satisfy literal good-path inequalities and are abundant",
        "status": "complete_human_reconstruction",
        "statement": "Interlacing and separated degrees bound mu_(i,r-1)<2B_old. Typical mass inequalities therefore bound normal vector-step degree and plane covector-step degree by the actual oc allowance and give the exact thc lower bound. Thus the finite set Tset has cardinal at least (1-a^{-Ns^2})R.",
        "sources": many("ATYP", ["GoodA", "TypicalPathOrdersSmall"], "generic_good_path_interface")
          + many("ORD", ["nu_last_le", "typical_path_orders_small"])
          + many("DICT", ["letter_dictionary_bounds"], "actual_threshold_and_order_translation")
          + many("GPARTS", ["LetterDictionaryBounds", "good_path_weight_of_parts"])
          + many("GTOP", ["lemT_of_adm", "good_path_weight_of_top_count"])
          + many("GALT", ["good_path_weight"], "closed_actual_abundance_export")
          + many("GOOD", ["IsGood", "GoodPathWeight"], "exact_actual_target"),
    },
    {
        "id": "GP8",
        "title": "The literal famEl family satisfies all four membership clauses",
        "status": "complete_human_proof_using_IP_prefix_bounds",
        "statement": "The actual determinant/old-monomial/current-monomial/plane-word/normal-word product lies in Mj(b): its split paths satisfy the crossing inequalities, determinant order supplies m0, ordinary degrees are the required normal/plane row degrees, total row degrees equal b, and each terminal plane-coordinate exponent is <Qc.",
        "sources": many("SEG", ["XX'", "ordDeg", "plEmb", "nmEmb"], "literal_selected_space")
          + many("COARSE", ["resSet", "segDegSet", "Mj"], "literal_selected_intersection")
          + many("GOOD", ["Idx", "Dw", "famEl", "RestMem"], "literal_family_and_target")
          + many("MEM", ["discPowerTimesMonomial", "memMu", "memPl", "memG", "memM", "famEl_eq", "RestMemA", "RestMemB", "RestMemC", "RestMemD", "restMem_of_rests"])
          + many("MEMA", ["exists_path_decomposition", "mem_tan_zero", "tangent_degree_zero_at_w", "mem_vg_A", "restMemA_of"])
          + many("MEMB", ["disc_power_monomial_degree_at_w", "mem_dMu_tau", "restMemB_of"])
          + many("MEMCD", ["m0_le_Bw_of_isW", "restMemC_of", "restMemD_of", "restMem_of"])
          + many("DMIN", ["tau_degree_on_path_bound"], "reused_SD6_terminal_degree_bound"),
    },
    {
        "id": "GP9",
        "title": "Antidiagonal specialization and integral independence",
        "status": "complete_human_proof_using_IP_integral_path_basis",
        "statement": "Killing off-antidiagonal terminal plane variables turns each actual plane path word into a unit times a frame monomial times its truncated-path word. Icut is standard and records every terminal column rise. The IP product basis gives specialized independence; taking the least auxiliary off-diagonal degree lifts it, and cancelling the nonzero common determinant-monomial gives RestInd.",
        "sources": many("IND", ["kill", "scaleS", "offDeg", "scaleS_coeff_zero", "li_of_kill", "offSet", "monTau", "wordEl", "RestKey", "restInd_of"])
          + many("DPLUS", ["cut_ppath", "plHyp_of"])
          + many("KCOL", ["offN", "riseA", "kill_Kcol_tau"])
          + many("ICUT", ["cutPath", "PlHyp", "Icut", "kill_Psi"])
          + many("CUT", ["Icut_eq", "card_Icut_filter", "isSt_cut", "path_eq_of_cut"])
          + many("LI", ["li_mono_words"])
          + many("KEY", ["kill_wordEl", "restKey_of"])
          + many("CLOSED", ["restInd"], "closed_actual_export"),
    },
    {
        "id": "GP10",
        "title": "Direct beta/Q bound using the actual adjacent coarse scale",
        "status": "new_short_elementary_proof_of_the_exact_source_target",
        "statement": "Distinct preterminal distances and the L1 gap give beta<=4a/p^(Rj+D+L1+1). The proven untruncated Q formula and adjacent lower p^R bound give beta/Q<32Yk^2Ns/p^L1<=1/(4pY), stronger than 4Y beta<=Q. No admissibleSmallRatio lemma is retained as an input.",
        "sources": many("MON", ["BetaRatioBound"], "exact_ratio_target")
          + many("BETA", ["beta_ratio_bound"], "parallel_source_proof")
          + many("COARSE", ["Rj", "Qc"], "literal_scale_definitions")
          + many("SEG", ["GapGt", "Valid"], "literal_gap_premise"),
    },
    {
        "id": "GP11",
        "title": "Actual terminal residue padding and RestMon",
        "status": "complete_application_of_reconstructed_SD6_with_GP10",
        "statement": "Each good path admits at least [Q^(r-1) max(0,1-r/(2Y))]^r auxiliary arrays with arbitrary specified terminal residues. The resulting actual degrees satisfy e_t<rQ, preserve IsPATH and IsGood, and give an injection into the precise Idx family summed in RestMon.",
        "sources": many("MON", ["TauDegreeOnPathBound", "ResidueClassCount", "restMon_of"])
          + many("DMIN", ["residue_class_count", "tau_degree_on_path_bound"], "reused_SD6_elementary_results")
          + many("GOOD", ["RestMon"], "exact_actual_summation_target")
          + many("CLOSED", ["restMon"], "closed_actual_export"),
    },
    {
        "id": "GP12",
        "title": "Construct the literal segment function G and close RestSeg",
        "status": "complete_human_reconstruction_conditional_on_literal_Hyp_and_prior_proved_results",
        "statement": "The function G_j(b)=|Idx(j,restr b)| is nonnegative, depends only on late degrees, is bounded by rank Mj(b) for every BOK b, and satisfies the exact SegOK residue sum. All RestMem, RestInd, GoodPathWeight and BetaRatio inputs are proved in this report; SD6, IP and RS are reused explicitly.",
        "sources": many("RC", ["segBound", "SegOK", "RestSeg"], "literal_final_target")
          + many("GOOD", ["RestFin", "restSeg_of"], "exact_final_assembly")
          + many("FIN", ["segDegSet_finite", "restFin"])
          + many("CLOSED", ["second_estimate_of_restrictions"], "source_consumer_of_the_reconstructed_branch"),
    },
]

artifacts = []
for filename in ["good_paths_section.tex", "report.txt"]:
    raw = (WORK / filename).read_bytes()
    artifacts.append({"filename": filename, "sha256": sha256(raw).hexdigest(), "bytes": len(raw)})

prior = [
    ("v0_5/path_generators/report.txt", "IP2--IP6: integral signed path basis, signed Pieri counts, prefix extremal bounds and splitting the joint path."),
    ("v0_6/complementary_basis/report.txt", "CB: exact standard-tableau/GT count and Weyl dimension formula, including the one-row branching identity used in GP2."),
    ("v0_6/selected_dimension/report.txt", "SD6: elementary residue congruence count and terminal strip degree <=2 beta."),
    ("v0_7/residue_summation/report.txt", "RS2--RS3: actual coarse a-prime and scale arithmetic, fully reconstructed in this version."),
]
prior_human_results = []
for path, use in prior:
    raw = (REPO.parent / path).read_bytes()
    prior_human_results.append({"path": path, "use": use, "sha256_at_generation": sha256(raw).hexdigest()})

ledger = {
    "title": "Good paths, actual segment generators and their rank: GP1--GP12",
    "version": "0.7",
    "repository": URL,
    "commit": COMMIT,
    "generated_by": "regenerate_provenance.py",
    "range_convention": "Inclusive one-indexed lines; SHA256 retains original bytes and line endings. Declaration names are lexical namespace qualifications.",
    "source_validation": "Every cited local file compared byte-for-byte with git show COMMIT:path before generation.",
    "verification_limits": [
        "No Lean build was run for this note.",
        "These human mathematical arguments are not new Lean formalizations.",
        "The whole claimed RH/GRH release is not certified by this segment result.",
        "Literal Dat.Hyp and CLa,Ck>=1088 remain explicit; the IP/SD/RS results are reused with their proved hypotheses.",
        "The improved endpoint constants 6 and 8 and the direct beta/Q shortcut are independently derived human arguments, not claimed as verbatim source declarations.",
    ],
    "prior_human_results": prior_human_results,
    "artifacts": artifacts,
    "files": [{k: v for k, v in item.items() if not k.startswith("_")} for item in FILES.values()],
    "claims": CLAIMS,
}

(WORK / "provenance.json").write_text(json.dumps(ledger, indent=2, ensure_ascii=False) + "\n")
lines = ["GP1--GP12 source locators", f"Pinned commit: {COMMIT}", ""]
seen = set()
for claim in CLAIMS:
    lines.extend([claim["id"] + ": " + claim["title"], claim["status"]])
    for source in claim["sources"]:
        key = (source["path"], source["line_start"], source["line_end"])
        seen.add(key)
        lines.append(f"  {source['declaration']} — {source['path']}:{source['line_start']}-{source['line_end']}")
        lines.append(f"  {source['pinned_url']}")
        lines.append(f"  range sha256: {source['range_sha256']}")
    lines.append("")
(WORK / "source_locators.txt").write_text("\n".join(lines) + "\n")
print(f"Generated {len(CLAIMS)} claims; {len(FILES)} pinned files; {len(seen)} unique declaration ranges.")


