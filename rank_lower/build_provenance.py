"""Rebuild RD1–RD15 provenance from the pinned, byte-identical Lean checkout.

Writes only this component's provenance.json and source_locators.txt.
No network, Lean edits, compilation or kernel replay. Inclusive ranges
retain their original bytes and line endings. Requires Python 3.11+.
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
GB = "src/Formalism/SharpRestriction/GrowthBounds/"
PATHS = {
    "STD": GB+"BinomialRatio/Transported.lean",
    "OBJ": GB+"ObjSeg.lean",
    "NUM": GB+"BinomialRatio/CoarseDegreeAlternative.lean",
    "GEOM": GB+"BinomialRatio/SegmentStatementHolds.lean",
    "CD": GB+"BinomialRatio/CountDefs.lean",
    "CU": GB+"BinomialRatio/CountUp.lean",
    "CL": GB+"BinomialRatio/CountLow.lean",
    "TAIL": GB+"BinomialRatio/ThresholdStandardLarge.lean",
    "PC": GB+"BinomialRatio/PairCount.lean",
    "WD": GB+"BinomialRatio/WdimUp.lean",
    "WT": GB+"BinomialRatio/WtBound.lean",
    "NK": GB+"BinomialRatio/NotKept.lean",
    "EXP": GB+"BinomialRatio/NkExponent.lean",
    "BR": GB+"BinomialRatio/Bracket.lean",
    "LARGED": GB+"BinomialRatio/CoarseDegreesLargeBeyond.lean",
    "LARGE": GB+"BinomialRatio/CoarseDegreesLargeOfStd.lean",
    "CR": GB+"BinomialRatio/CoarseThresholdRatioConsecutive.lean",
    "AR": GB+"BinomialRatio/CoarseDegreeRatioConsecutive.lean",
    "PF": GB+"BinomialRatio/PairFacts.lean",
    "KS": GB+"BinomialRatio/KeptBlocksHolds.lean",
    "KU": GB+"BinomialRatio/KeptBlocksOfSLine.lean",
    "KX": GB+"BinomialRatio/KeptBlocksOfUSLines.lean",
    "RANK": GB+"BinomialRatio/RankDefs.lean",
    "CAST": GB+"BinomialRatio/RankOnDigitsCast.lean",
    "HALF": GB+"BinomialRatio/LeAndHalfLeProdOneSubExpNegOfBounds.lean",
    "SIZE": "src/Formalism/PolynomialDimension/DigitClassSize.lean",
    "SER": "src/Formalism/PolynomialDimension/MultinomialDepth/BinomialSeriesBound.lean",
    "FINAL": GB+"ColumnSpanDensity/ThresholdFinalFacts.lean",
    "DENS": GB+"ColumnSpanDensity/DensityNumericalFacts.lean",
    "DABS": GB+"ColumnSpanDensity/DensAbs.lean",
    "TDENS": GB+"ColumnSpanDensity/ThresholdDensityFacts.lean",
    "COL": GB+"ColumnSpanDensity/ColumnSpanNumericalFacts.lean",
    "MD": GB+"ColumnSpanDensity/MeanDefs.lean",
    "BASE": GB+"ColumnSpanDensity/NumBase.lean",
    "LOC": GB+"ColumnSpanDensity/LocalHypothesisOfGlobal.lean",
    "ROOT": GB+"ColumnSpanDensity/RhoLowerBoundLargeConductor.lean",
    "HYP": GB+"ProjectionLemmaBaseLevel.lean",
    "MID": GB+"ColumnSpanDensity/MidMeanOf.lean",
    "SG": GB+"ColumnSpanDensity/SgSegUnique.lean",
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
                                 "qualified": f"{namespace}.{name}" if namespace else name})
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
        "id": "RD1", "title": "Literal standard data give the exact coarse scale and geometric prefix bounds",
        "status": "proved_under_literal_Std_H4", "dependencies": ["SW10"],
        "statement": "For compatible actual segment digits and A0(1-epsilon)<=A<=A0, all A,Ai,Ci>=k^3; p>=k^2, k>=10, 4lambda<=k; both consecutive coarse degree ratios are at least p^2/2 and preceding sums are <=4/p^2 times the current degree. The exact early/late alternative is SW10.",
        "sources": many("STD", ["Std"], "literal_hypotheses")
            +many("OBJ", ["SegData.P","SegData.Qj","SegData.A0","coarseA","coarseC","DigitsOK"], "literal_coarse_data")
            +many("NUM", ["coarse_bounds","Std.kQ","Std.levels","coarse_degree_alternative"])
            +many("GEOM", ["dist_odd","dist_strictMono","segG_even","sigma_iff"])
            +many("LARGE", ["coarse_degree_gt_quotient","coarse_degrees_large_of_std"])
            +many("AR", ["coarse_degree_ratio_consecutive","coarse_degree_prefix_sum"])
            +many("CR", ["coarse_threshold_ratio_consecutive","coarse_threshold_prefix_sum"])
            +many("HALF", ["Std.half_ratio_le_segment_base_of_std","Std.La_ge"]),
    },
    {
        "id": "RD2", "title": "Actual weighted pairs, their sparse tail shape and coordinate bounds",
        "status": "proved_using_RU2_RU3_dimension_identities", "dependencies": ["RD1","RU2","RU3"],
        "statement": "The exact total pair weight is dimMM, and horizontal-strip propagation proves all PairFactsAt inequalities, including the signed lower-tail bound n_i<=Ci(1+4/p^2).",
        "sources": many("CD", ["Strip","wdim","IsChain","ChainDimAt","NumBranchAt"], "literal_shared_dimension_interfaces")
            +many("CU", ["Inter","kLetters"], "literal_pair_word_and_branching")
            +many("CL", ["IsPair","pairC","pairTail","pairRho","pairO","pairW","pairSg","pairN","pairD"], "literal_pair_statistics")
            +many("TAIL", ["pairSet","pairSet_finite","pair_sum"])
            +many("AR", ["strip_tail","inter_strip","chain_first_tail","pair_top","pairC_zero"])
            +many("WT", ["wb_vstep","wb_cstep","wb_one","wb_shape","wb_follow"])
            +many("PF", ["pfMass","pfMass_up","pfMass_down","pf_mass","pf_prev_le","pf_rho_le","pf_u_ge","pf_rho_le_c"])
            +many("LARGE", ["pfa_rho_nonneg","pfa_c_nonneg","pfa_rho_up","pfa_u_low","pair_first_weight_bounds","pfa_n_nonneg","restPairFacts_of"])
            +many("CR", ["nu_follow","nu_le_last","last_ge_mass","nUp_of_std"])
            +many("LARGED", ["PairFactsAt"], "exact_source_endpoint"),
    },
    {
        "id": "RD3", "title": "An explicit finite encoding bounds the actual number of pairs",
        "status": "proved_by_integer_coordinate_encoding", "dependencies": ["RD1","RD2"],
        "statement": "The actual pair set has cardinality at most (8a)^(4(N1+1)^2), by encoding only its first s+1 and last s coordinates at each state.",
        "sources": many("PC", ["pc_strip_le","pcU","pcL","pc_shape","pcPosition","pcEnc","pcEnc_inj","pcEnc_abs","pc_count","pairCount_of_std","restPairCount"])
            +many("TAIL", ["PairCountAt"], "literal_target"),
    },
    {
        "id": "RD4", "title": "The regularized quadratic identity proves the complete bad-pair bracket",
        "status": "proved_by_quadratic_deficit_and_telescoping", "dependencies": ["RD1","RD2"],
        "statement": "Every non-kept pair has a product bracket theta with theta^(r-1)<=exp(2-lambda/5). Either failed literal kept inequality contributes exp(-lambda/(4k)); zero factors require no division.",
        "sources": many("CL", ["KeptPair"], "literal_bad_event")
            +many("NK", ["BracketAt"], "exact_target")
            +many("EXP", ["nk_iv","nk_vi","nk_tele","nk_bracket","nk_exponent"])
            +many("BR", ["brk_hat","brk_core","bracket_of","restBracket_of"]),
    },
    {
        "id": "RD5", "title": "Weighted bad mass is at most exp(-lambda/8) with the exact source threshold",
        "status": "proved_for_C0_ge_880", "dependencies": ["RD2","RD3","RD4","RU2"],
        "statement": "A signed-strip path bounds wdim by a product of symmetric-power dimensions. Combined with RD4 and the explicit pair count, this proves the exact TailAt lower mass (1-exp(-lambda/8))*dimMM. The human bound before the final polynomial envelope is stronger than the source statement.",
        "sources": many("WD", ["wuLam","wuDeg","wuLL","wuSt","wu_step","wu_chain","wu_prod","wdimUp_of"])
            +many("WT", ["wtBound_of"])
            +many("NK", ["nk_b_up","nk_b_low","nk_core","nk_prod_le_dimMM","notKeptWt_of"])
            +many("TAIL", ["kept_sum","tail_core","tail_num","NotKeptWtAt","threshold_standard_large","tail_of","restTail_of"])
            +many("CL", ["keptPairSum","TailAt"], "literal_endpoint"),
    },
    {
        "id": "RD6", "title": "The actual early, late and terminal kept-block inequalities",
        "status": "proved_from_the_literal_kept_pair_and_Std", "dependencies": ["RD1","RD2","SW10"],
        "statement": "PairUAt, PairSAt and PairXAt hold with the exact source bounds, including early sg<=2lambda*A0/k and the terminal negative-mass correction.",
        "sources": many("AR", ["PairUAt","PairSAt","PairXAt"], "literal_three_line_interfaces")
            +many("KU", ["pairC_le_sum","pairU_at"])
            +many("KS", ["pairS_at","restPairS"])
            +many("PF", ["pf_tele","pf_d_le","pf_X"])
            +many("KX", ["restPairX"]),
    },
    {
        "id": "RD7", "title": "The literal kept-block map preserves weights, levels and every prefix cutoff",
        "status": "proved_by_explicit_map_and_trace_recovery", "dependencies": ["RD2","RD6"],
        "statement": "pairMap constructs actual kept blocks with the original digits, legal levels, and the exact margin cutoffs; cap_l=M+c_l. It is injective because the degree sums recover omitted first coordinates, and gives MatchAt by a finite weighted sum. Target finiteness is proved directly, independently of the source's use of MatchUp.",
        "sources": many("OBJ", ["oEff","cap","Oplus","Kept"], "literal_kept_block_constraints")
            +many("CU", ["FinalTheorems","SrcOK","Fs","chainCount_eq"], "literal_source_weight_and_count")
            +many("CL", ["TgtOK","pairChain","pairBlock","pairLevel","pairMap","KeptBlockAt","cl_chain_total","cl_chain_ext","matchLow_of","match_of"], "explicit_source_map_and_weighted_assembly")
            +many("CL", ["cl_Fs_finite"], "parallel_finiteness_target; human_proof_uses_direct_degree_bounds")
            +many("AR", ["jE_pair","pair_chain","pair_level","oEff_pair","cap_pair","pair_thr","kept_pair_of_three_lines","kept_block_at_of_pair_level_chain_threshold"])
            +many("KS", ["kept_blocks_holds"], "completed_archival_endpoint"),
    },
    {
        "id": "RD8", "title": "The terminal hockey-stick loss and the rounded initial-degree loss",
        "status": "proved_by_binomial_products_and_Bernoulli", "dependencies": [],
        "statement": "The terminal sum is at least (1-exp(-lambda/3))*binom(B+r,r), and binom(A0-M+r,r)>=(1-rM/A0)binom(A0+r,r), including a negative final factor.",
        "sources": many("CL", ["cl_sd_step","cl_sd_ratio_le","cl_hockey","cl_hockey_low","one_sub_div_pow_mul_sd_le_sd_sub","cl_sd_margin"]),
    },
    {
        "id": "RD9", "title": "The exact lower rank on each compatible digit class",
        "status": "proved_pointwise_under_Std_H4_and_uniformly_with_NP2", "dependencies": ["RD5","RD7","RD8","RU1","RU2","NP2"],
        "statement": "For h>=0 and ceil(h)<=A0*N1*lambda/k, rankOnDigits>=lowFac*mmB with lowFac=(1-exp(-lambda/8))(1-exp(-lambda/3))(1-r*ceil(h)/A0). This is the actual LowAt/RestLow with all original ring and digit conventions.",
        "sources": many("RANK", ["mmB","lowFac","LowAt","RestLow"], "literal_rank_endpoint")
            +many("CD", ["CountLowAt","RestCountLow"], "literal_combinatorial_endpoint")
            +many("CL", ["countLow_of","restCountLow_of","restCountLow_of''"])
            +many("CAST", ["blockRank_cast","rankOnDigits_cast","restLow_of"]),
    },
    {
        "id": "RD10", "title": "The two-sided half-density window with its exact ceiling",
        "status": "proved_using_actual_upper_RU8_and_lower_RD9", "dependencies": ["RD1","RD9","RU8"],
        "statement": "For 0<=h<=b'/(kQY), the lower factor is at least 29/45>1/2, giving mmB/2<=rankOnDigits<=mmB. This is the pointwise content of RootMultiplicityTwoBeyond and its uniform form follows with NP2.",
        "sources": many("HALF", ["le_and_half_le_prod_one_sub_exp_neg_of_bounds","one_segment_of_upper_lower"])
            +many("RANK", ["UpAt","LowAt","lowFac"], "exact_two_sided_bounds"),
    },
    {
        "id": "RD11", "title": "A finite telescoping proof strengthens the actual harmonic diagonal density",
        "status": "proved_by_new_finite_telescoping_argument", "dependencies": ["HM1"],
        "statement": "For P(t)=binom(t+r,r), H=P(alpha)P(beta)-P(alpha-1)P(beta-1), the actual P1 term is >=R_j-R_(j+1). Consequently its finite sum is >=1-exp(-lambda'/3) under the literal window bound, removing the source's extra initial-degree loss and infinite-series detour.",
        "sources": many("SIZE", ["dimPol","dimHar","DensityLower"], "literal_dimensions_and_archival_weaker_statement")
            +many("DENS", ["P1","DensityNumericalFacts"], "actual_dimension_weight_and_target")
            +many("SER", ["dimPol_succ_mul_real","dimPol_succ_eq_real","binomial_ratio_bound","binomSeries_gen","tail_q_bound","binomial_tail_bound","dimHar_ratio_ge","density_lower_bound"], "archival_parallel_route; replaced_by_finite_Rj_telescoping"),
    },
    {
        "id": "RD12", "title": "All harmonic density fields hold uniformly at max(TLP,400)",
        "status": "proved_with_stronger_density_and_literal_source_threshold", "dependencies": ["RD11","NP4"],
        "statement": "Under literal Dat.Hyp and K.Pos, C_H>=max(TLP,400) supplies DensityNumericalFacts with d=1-exp(-lambda'/3), exact enlarged-cardinality factor2, and the original coordinate windows. The auxiliary threshold is1.",
        "sources": many("HYP", ["HypI"], "literal_final_numerical_hypotheses")
            +many("ROOT", ["Dat","a","Hyp","J0","Jn","TransportedAlt"], "actual_data_and_quantifier_order")
            +many("BASE", ["Cst.TLP","Base","base_of"], "NP4_reused_base_interface")
            +many("MD", ["ua","lb","ub","Wa","Wb","WaP","WbP"], "literal_boxes")
            +many("FINAL", ["WinFacts","card_first_window","card_second_window","winFacts_of"], "window_fields_reconstructed_in_report")
            +many("DENS", ["DensityNumericalFacts","card_Wa","card_Wb"], "exact_target")
            +many("DABS", ["dens_abs","Nexp_le"], "archival_scalar_route; report_uses_stronger_finite_density_and_rational_Bernoulli_bounds")
            +many("TDENS", ["Cst.TM2","threshold_density_facts"], "same_uniform_threshold_and_exact_record"),
    },
    {
        "id": "RD13", "title": "The actual column-box boundary loss and conductor correction",
        "status": "proved_uniformly_at_TLP", "dependencies": ["NP4"],
        "statement": "Under literal final Hyp with C_H>=TLP, the unshifted windows are positive, wa,wb>=2YNc, the removed product-box fraction is <=1/Y, and 12Nkc/b'<=1/Y. These are all fields of ColumnSpanNumericalFacts, with auxiliary threshold1.",
        "sources": many("COL", ["ColumnSpanNumericalFacts"], "literal_record")
            +many("FINAL", ["WinFacts","winFacts_of","below_abs","threshold_final_facts"])
            +many("HYP", ["HypI"], "literal_final_size_clause")
            +many("BASE", ["Cst.TLP","Base"], "NP4_reused_base_bounds"),
    },
    {
        "id": "RD14", "title": "Exact segment marginalization proves the enlarged-window MeanX",
        "status": "proved_using_completed_local_mean_and_margin_bounds", "dependencies": ["SW8","SW9","TP11","RU8","NP3","NP6","NP9"],
        "statement": "For CA>=max{56,2(31e^3+5)e^3,1} and Cs>=Ckap(Cm+4CE1+CE2+15), the actual segment means and kapPI bound imply mean kx<=(CA+Cs)NN1/Y. Each segment restriction fiber has exactly waP^(N-s_j-1) elements; no independence is assumed.",
        "sources": many("LOC", ["card_fiber_restriction_pi","sum_pi_marginal_injective","sum_pi_option_split","MeanKappaNumericalFacts","locOf","local_hypothesis_of_global","instOf","instance_window_eq","kapSeg","segment_mean_kappa_bound","segment_sum_kappa_bound","meanX_of"])
            +many("ROOT", ["kx","Cst.admitted"], "actual_kx_and_archival_packaged_inputs_resolved_by_named_dependencies")
            +many("MD", ["meanN","MeanX"], "actual_normalized_average")
            +many("SG", ["sgTop","sgTop_inj","sg_count"], "actual_segment_coordinate_map_and_count"),
    },
    {
        "id": "RD15", "title": "The actual final exceptional mean with Cmean=6(CA+Cs)+8",
        "status": "proved_using_HM7_and_completed_numerical_records", "dependencies": ["RD12","RD13","RD14","HM7"],
        "statement": "The literal kText on the signed final weight box has mean at most [6(CA+Cs)+8]NN1/Y. The proof tracks subtraction on the inside box, the boundary fraction, bijective positive shift and exact conductor correction.",
        "sources": many("ROOT", ["kF","Inside","kText","Cst.Cmean"], "actual_exceptional_function")
            +many("COL", ["sum_pi_cast","card_Icc_cast","ceil_cast","floor_cast","kText_cast","sum_of_meanN","sum_first","sum_piFinset_Icc_shift_eq","mean_of"])
            +many("DENS", ["avg_of"], "conditional_Avg_already_proved_by_HM7")
            +many("MID", ["FM","midMean_of"], "completed_mean_assembly"),
    },
]

ids = {c["id"] for c in CLAIMS}
assert ids == {f"RD{i}" for i in range(1,16)}
external = sorted({d for c in CLAIMS for d in c["dependencies"] if d not in ids})
def visit(name, path=()):
    if name in path:
        raise RuntimeError("dependency cycle: "+" -> ".join(path+(name,)))
    for child in next(c for c in CLAIMS if c["id"]==name)["dependencies"]:
        if child in ids: visit(child,path+(name,))
for name in ids: visit(name)

artifacts=[]
for name in ["main.tex","report.txt","build_provenance.py"]:
    raw=(HERE/name).read_bytes()
    artifacts.append({"path":name,"sha256":sha256(raw).hexdigest(),"bytes":len(raw)})
payload={
    "artifact_version":"0.10", "component":"rank_lower",
    "repository":BASE_URL, "commit":COMMIT, "head_verified":actual_head,
    "line_range_convention":"inclusive, one-indexed, original bytes including line endings",
    "claims":CLAIMS,
    "source_files":[{k:v for k,v in f.items() if not k.startswith('_')} for f in FILES.values()],
    "artifacts":artifacts,
    "explicit_external_dependencies":external,
    "derived_simplifications":[
        "The lower source support is finite directly from kept order bounds; MatchUp is not needed merely to justify summation.",
        "The single bad-pair weight bound is stronger than its source polynomial envelope; C0>=880 is retained.",
        "P1>=Rj-R(j+1) proves the harmonic density by finite telescoping and removes the initial-degree loss in the archival infinite-series route.",
        "Cubing gives N exp(-lambda'/3)<=1/3; rational Bernoulli bounds prove the same factor2 enlarged-window inequality at the unchanged threshold400.",
    ],
    "outside_scope":[
        "Digit-class summation and aggregate HH rank are RU9–RU11, not duplicated here.",
        "Actual harmonic maps/dimensions and KeyIneq/Avg are HM1/HM6/HM7, with exact dependencies preserved.",
        "Uniform parameter supply and kapPI are NP2–NP9; pointwise lower-rank proofs do not silently identify Std with bare HIext.",
        "General cloud transfer, coefficient-ring transport and global arithmetic/spectral/cohomological RH/GRH branches are separate.",
    ],
    "scope_note":"Complete human proofs of the named local count, density-record and mean interfaces under their literal hypotheses and listed completed dependencies. Source-byte validation is not a Lean build or kernel replay.",
}
(HERE/'provenance.json').write_text(json.dumps(payload,indent=2,ensure_ascii=False)+'\n')
out=[f"RD1–RD15 exact source locators at {COMMIT}",""]
for c in CLAIMS:
    out.extend([c['id']+': '+c['title'],'Dependencies: '+', '.join(c['dependencies'])])
    for s in c['sources']:
        out.extend([f"  {s['declaration']} | {s['path']}:{s['line_start']}-{s['line_end']} | {s['role']}",
                    '    '+s['pinned_url'],
                    f"    file sha256 {s['full_file_sha256']} ; range sha256 {s['range_sha256']}"])
    out.append('')
(HERE/'source_locators.txt').write_text('\n'.join(out)+'\n')
print(json.dumps({"claims":len(CLAIMS),"source_files":len(FILES),"locators":sum(len(c['sources']) for c in CLAIMS),
                  "external_dependencies":external,"artifacts":artifacts},indent=2))
