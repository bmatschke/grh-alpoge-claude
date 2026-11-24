"""Build the v0.9 continuation map; this script adds no theorem claims.

Every selected declaration is checked against the pinned Git blob, with
full-file and inclusive-range hashes. The four v0.8 global-branch entries
are retained verbatim. Target counts are computed, never fixed in the
output schema. Run from the shared RH workspace with Python 3.11+.
"""
from copy import deepcopy
from pathlib import Path
from hashlib import sha256
import json
import re
import subprocess

HERE = Path(__file__).resolve().parent
BASE = HERE.parent
REPO = BASE / "alpoge-rh"
PIN = "7cbf7a0c32fca1badf05931879a37c3f8a2b03b4"
URL = "https://github.com/CocoSgt/riemann-hypothesis-lean"
GB = "src/Formalism/SharpRestriction/GrowthBounds/"
OLD_PATH = BASE / "v0_8/next_source_targets.json"
old_raw = OLD_PATH.read_text()
old = json.loads(old_raw)
if old["commit"] != PIN:
    raise RuntimeError("The previous target map has a different source pin")
head = subprocess.check_output(["git", "-C", str(REPO), "rev-parse", "HEAD"], text=True).strip()
if head != PIN:
    raise RuntimeError(f"Source checkout is {head}, expected {PIN}")

PREFIX = r"(?:@\[[^\n]*\]\s*)?(?:(?:private|protected|noncomputable)\s+)*"
DECL = re.compile(r"^" + PREFIX + r"(?:def|theorem|lemma|abbrev|structure|inductive|instance)\s+(\S+)")
BOUNDARY = re.compile(r"^" + PREFIX + r"(?:def|theorem|lemma|abbrev|structure|inductive|instance|namespace|end|section|variable|attribute|open|include|set_option)\b")
NS = re.compile(r"^namespace\s+(\S+)")
SEC = re.compile(r"^(?:noncomputable\s+)?section(?:\s+(\S+))?\s*$")
END = re.compile(r"^end(?:\s+(\S+))?\s*$")
files = {}


def source(path):
    path = GB + path
    if path in files:
        return files[path]
    raw = (REPO / path).read_bytes()
    pinned = subprocess.check_output(["git", "-C", str(REPO), "show", f"{PIN}:{path}"])
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
    info = {
        "path": path, "sha256": sha256(raw).hexdigest(),
        "full_file_sha256": sha256(raw).hexdigest(),
        "bytes": len(raw), "line_count": len(lines),
        "verified_equal_to_pinned_git_blob": True,
        "_lines": lines, "_declarations": declarations,
    }
    files[path] = info
    return info


targets = []


def add(stage, path, name, role, remaining, connections=()):
    info = source(path)
    hits = [d for d in info["_declarations"] if d["name"] == name]
    if len(hits) != 1:
        raise RuntimeError((path, name, "expected one declaration", len(hits)))
    decl = hits[0]
    start = decl["line"]
    lines = info["_lines"]
    end = start + 1
    while end < len(lines) and not BOUNDARY.match(lines[end].decode("utf-8")):
        end += 1
    while end > start + 1 and not lines[end - 1].strip():
        end -= 1
    excerpt = b"".join(lines[start:end])
    link = f"{URL}/blob/{PIN}/{info['path']}#L{start+1}-L{end}"
    targets.append({
        "priority_group": stage,
        "path": info["path"], "declaration": decl["qualified"],
        "source_spelling": name,
        "line_start": start + 1, "line_end": end,
        "sha256": info["sha256"],
        "full_file_sha256": info["full_file_sha256"],
        "range_sha256": sha256(excerpt).hexdigest(),
        "range_bytes": len(excerpt),
        "url": link, "pinned_url": link,
        "first_line": lines[start].decode("utf-8").rstrip("\r\n"),
        "declaration_lines_within_range": [start + 1],
        "verified_equal_to_pinned_git_blob": True,
        "role": role,
        "remaining_human_scope": remaining,
        "source_connections": list(connections),
        "human_status": "continuation_target_only; no additional theorem claim or proof by this map",
    })


# Priority 1: actual coarse rank-on-digits, including concrete counting inputs.
add(1, "BinomialRatio/RankDefs.lean", "UpAt",
    "Literal upper rank-on-digits inequality rankOnDigits<=mmB for every compatible digit class.",
    "Discharge the actual coarse upper bound retained by SW8, with the original block family, margin and coefficient rings.")
add(1, "BinomialRatio/RankDefs.lean", "LowAt",
    "Literal lower rank-on-digits inequality with the three-factor lowFac and the ceil(m) margin restriction.",
    "Prove the quantitative coarse lower count, including the exact exponential factors and initial-degree margin.")
add(1, "BinomialRatio/RankDefs.lean", "RestUp",
    "TransportedAlt quantifier package for the upper digit-class estimate.",
    "Make the upper proof uniform in the source's nested constant choices; a pointwise bound alone does not supply this package.")
add(1, "BinomialRatio/RankDefs.lean", "RestLow",
    "TransportedAlt quantifier package for the lower digit-class estimate.",
    "Make the lower proof uniform with the same literal parameters and margin constraints.")
add(1, "BinomialRatio/RankOnDigitsCast.lean", "restUp_of",
    "Converts the rational weighted chain upper count into the actual lattice rank upper count.",
    "Identify BlockRankAt and DimYAt with the completed SW/IP dimension decompositions, then supply RestCountUp; do not assume the chain count equals rank merely by notation.",
    ["RankOnDigitsCast.blockRank_cast", "RankOnDigitsCast.rankOnDigits_cast", "CountDefs.BlockRankAt", "CountDefs.DimYAt"])
add(1, "BinomialRatio/RankOnDigitsCast.lean", "restLow_of",
    "Converts the rational weighted chain lower count into the actual lattice rank lower count.",
    "Reuse the same exact dimension identification and supply RestCountLow, retaining the source real cast and lowFac.",
    ["RankOnDigitsCast.rankOnDigits_cast", "CountDefs.RestCountLow"])
add(1, "BinomialRatio/CountUp.lean", "countUp_of",
    "Concrete upper-count proof by a weight-preserving injection from kept block/level/path data into interlacing targets.",
    "Reconstruct MatchUpAt and the finite weighted sum; keep the actual terminal weight and terminal symmetric-power degree. ChainDimAt and NumBranchAt need explicit reuse of the established dimension formulas.",
    ["CountUp.MatchUpAt", "CountUp.Gt_sum", "SegmentChainDegreeEven.restMatchUp_of", "UpperCountOfTopRows.upper_count_of_top_rows"])
add(1, "BinomialRatio/AiAddMulLeA0.lean", "partial_width_le_cap",
    "Concrete upper-branch numerical predecessor: bounds partial early widths by the actual accumulated cap.",
    "Prove the partial-width inequality from literal Std and kept blocks, then follow top_rows_bound_holds and the first-row matching injection; SW10 and SW12 provide related but narrower cap consequences.",
    ["AiAddMulLeA0.top_rows_bound_holds", "UpperCountOfTopRows.sTopRows_of", "RestCountUpOfSTop.restCountUp_of_STop"])
add(1, "BinomialRatio/CountLow.lean", "countLow_of",
    "Concrete lower-count assembly: a large kept weighted pair set and its matching map give the exact lowFac times mmB.",
    "Prove the pair-to-block matching and its quantitative weighted lower sum, including the terminal hockey-stick estimate and ceil(m) loss.",
    ["CountLow.TailAt", "CountLow.MatchAt", "CountLow.match_of", "CountLow.restCountLow_of''"])
add(1, "BinomialRatio/ThresholdStandardLarge.lean", "tail_of",
    "Actual weighted tail estimate supplying TailAt, with C0>=880 and the literal polynomial-count and non-kept-weight bounds.",
    "Reconstruct the finite pair count and excluded-pair weight estimate, then verify the exponential budget; do not substitute the separate Type-II good-path tail theorem.",
    ["ThresholdStandardLarge.tail_core", "ThresholdStandardLarge.tail_num", "ThresholdStandardLarge.PairCountAt", "ThresholdStandardLarge.NotKeptWtAt", "ThresholdStandardLarge.restTail_of"])
add(1, "BinomialRatio/NotKept.lean", "notKeptWt_of",
    "Concrete non-kept-pair bound using a Weyl-weight product estimate and a strict bracket deficit.",
    "Supply WtBoundAt and BracketAt for the actual coarse pair geometry, retaining the exponential penalty and all dimension factors.",
    ["NotKept.nk_core", "NotKept.WtBoundAt", "NotKept.BracketAt", "NotKept.restNotKeptWt_of", "BinomialRatio.stmtEExt_of"])
add(1, "BinomialRatio/KeptBlocksHolds.lean", "pairS_at",
    "Concrete early-case estimate in the construction sending kept interlacing pairs to actual kept segment blocks.",
    "Prove PairSAt and the accompanying U/X line conditions, then check pairMap preserves digits, levels and all kept inequalities before using the lower injection.",
    ["KeptBlocksHolds.restPairS", "KeptBlocksOfSLine.kept_blocks_of_S_line", "KeptBlocksHolds.kept_blocks_holds", "CountLow.matchLow_of"])
add(1, "BinomialRatio/LeAndHalfLeProdOneSubExpNegOfBounds.lean", "one_segment_of_upper_lower",
    "Final coarse-count specialization combines RestUp and RestLow into the source half-density and upper bound.",
    "Check the exact ceil(m) margin and prove lowFac>=1/2 uniformly, then close the two rank-on-digits clauses used downstream.",
    ["LeAndHalfLeProdOneSubExpNegOfBounds.le_and_half_le_prod_one_sub_exp_neg_of_bounds", "LeAndHalfLeProdOneSubExpNegOfBounds.Std.half_ratio_le_segment_base_of_std", "FlipOneThree.adm11"])

# Priority 2: uniform numerical supply, distinct from already proved consequences.
add(2, "BinomialRatio/ThresholdLowerBounds.lean", "std_of",
    "Explicit parameter theorem D1num+HIext+CBound=>Std at T2=1000(CE1+CE2+1)(Cc+1)H.",
    "Check every literal Std clause and the full order of constant choices. SW10, SW12 and RL presently start from Std and do not prove this supply.",
    ["ThresholdLowerBounds.T2", "ThresholdLowerBounds.error_ratio_le_epsilon", "Transported.Std"])
add(2, "BinomialRatio/ExtendedStatementOfParts.lean", "thr_std",
    "Packages the explicit standard-hypothesis supply into the actual TransportedAlt quantifier order.",
    "Lift the proved pointwise parameter theorem uniformly, with CE1,CE2 and the later constants chosen in the permitted order; reuse the completed local numerical consequences.",
    ["ThresholdLowerBounds.std_of", "Transported.TransportedAlt"])
add(2, "MonomialFactorials/CoarseCLower.lean", "segFacts",
    "Actual segment numerical package from the literal flipOneThree.HI, including coarse scales, degree windows and cleaning displacement.",
    "Derive the required segment/window inequalities uniformly and match them to the explicit SW5--SW9 and TP11 inputs; do not read the name HI as automatic satisfaction.",
    ["CoarseCLower.SegFacts", "CountingStatementReduction.hiFacts", "RatioConditionOfSegFacts.ratioCondition_of_segFacts"])
add(2, "MonomialFactorials/ClosedOfOpenConditions.lean", "RestOpenE",
    "Exact uniform package of the block, terminal, multiple-tie and digit-transfer inputs before the segment theorem is closed.",
    "Supply the remaining numerical and coarse-rank premises uniformly while reusing the completed GG/TP/SW/RL constructions; the implication from this package is packaging, not a substitute for its hypotheses.",
    ["ClosedOfOpenConditions.RestOpen", "ClosedOfOpenConditions.restAllE_of_open", "SegmentWeightedCountingBoundOfAllRemainingBounds.RestAllE"])

# Priority 3: actual harmonic-model dimensions and the key weighted inequality.
add(3, "ColumnSpanDensity/MeanDefs.lean", "RestDims",
    "Exact harmonic and tensor-polynomial dimension identities used in the final Type-I average.",
    "Identify the actual Vsp(flatW) and HH spaces with the proved models and retain the rank m versus m+1 convention.")
add(3, "ColumnSpanDensity/FinrankLetter.lean", "restDims_of",
    "Source proof of RestDims from the Weyl representation model and letterwise dimension formulas.",
    "Audit the actual WeylV/model identification and tensor dimension application using earlier IW/CB results; no fresh abstract dimension axiom should be inserted.",
    ["FinrankLetter.finrank_weyl", "FinrankLetter.finrank_letter", "MeanDefs.RestDims"])
add(3, "ColumnSpanDensity/MeanDefs.lean", "KeyIneq",
    "Literal harmonic-weighted sum comparing shifted kF values with kx times dimHH divided by the Gaussian number.",
    "Prove the actual dimension-weighted inequality with the same shifted weight boxes and normalizing Gaussian factor; the already proved mean-transfer implication does not supply it.")
add(3, "ColumnSpanDensity/FactorizationBoundMonoLattices.lean", "keyIneq_of",
    "Concrete KeyIneq application from small-depth upper rank, large-conductor edge lower rank, lattice transport and dimensions.",
    "Match the actual RhoSumLowerBoundEdge, RhoUpperBoundSmallDepth, RestEdge and FixedWeightNumericalFacts hypotheses to reconstructed input theorems, preserving the harmonic shifts and multiplicities.",
    ["FactorizationBoundMonoLattices.sum_dimensions_flattened_weights", "DensityNumericalFacts.avg_of", "ColumnSpanDensity.MidMeanOf.midMean_of"])

# Priority 4: the full final height comparison and Type-I assembly.
add(4, "ColumnSpanDensity/SegStartSpec.lean", "tle_of",
    "Actual height comparison: shifted tStar plus 2*n'*ccl is bounded by tI for C>=4*Ct+4.",
    "Prove the minimum-term comparison, ceilings, cleaning allowance and odd-top count under the actual weight window. RL ends at t0, so this expanded tI comparison remains necessary.",
    ["SegStartSpec.min_shift", "InitialLevelFormula.RestOddTops", "RhoLowerBoundLargeConductor.Dat.tStar", "ThrLPOf.thrLP_of"])
add(4, "ProjectionLemmaBaseLevel.lean", "tI",
    "Literal expanded Type-I height bound, including its error envelope and weight-dependent minimum terms.",
    "Keep this exact expression as the target of the t0/tStar comparison; do not replace it by an asymptotically similar loss.",
    ["ProjectionLemmaBaseLevel.t0I", "ObjSeg.t0G4", "SegStartSpec.tle_of"])
add(4, "ColumnSpanDensity/TheoremIOfIntermediateBounds.lean", "theorem_I_of_intermediate_bounds",
    "Final source assembly from ring independence, LP, mean and both uniform numerical packages into Type-I closure.",
    "Discharge the literal MidLP, MidMean, FactsLP, FM and LPRingIndep interfaces, preserving the nested constants and the single exceptional function; local paired lifts alone are insufficient.",
    ["TheoremIOfLatticeFunctorComparison.theorem_I_of_lattice_functor_comparison", "ThrLPOf.thrLP", "RhoLowerBoundLargeConductor.LPRingIndep", "MeanDefs.MidMean"])
add(4, "ProjectionLemmaBaseLevel.lean", "Conclusion2",
    "Literal Type-I endpoint: one nonnegative exceptional function with the stated mean and LPprime conclusion.",
    "Check all final quantifiers, weight-box conditions, coefficient-ring independence and height hypotheses. Do not use the separate r>=2 Type-II theorem in place of this rank-one conclusion.",
    ["ProjectionLemmaBaseLevel.HypI", "ProjectionLemmaBaseLevel.WeightI", "ProjectionLemmaBaseLevel.tI"])

keys = [(t["path"], t["line_start"], t["line_end"]) for t in targets]
if len(keys) != len(set(keys)):
    raise RuntimeError("Duplicate exact target ranges")
forbidden = {"GramDeterminantGradedHypothesis", "gram_hypothesis_of_log_bound",
             "theoremMV7", "tieOpsX_main", "partnerMX_of_parts",
             "RestRawTail1", "RestForm", "paired_lifts_of_identity"}
if forbidden & {t["source_spelling"] for t in targets}:
    raise RuntimeError("A completed construction was incorrectly retained as a next target")

out = {
    "version": "0.9",
    "commit": PIN,
    "head_verified": head,
    "status": "Read-only continuation/source map; no additional theorem claim, human proof or Lean replay is asserted.",
    "target_count": len(targets),
    "source_file_count": len(files),
    "count_policy": "Consumers must use target_count or len(targets); no fixed historical target count is required.",
    "line_range_convention": "inclusive, one-indexed, original source bytes including line endings",
    "completed_previous_frontier": old["completed_previous_frontier"],
    "next_local_priority": "Actual coarse upper/lower rank-on-digits, then uniform Std and segment numerical supply, harmonic-model dimensions and KeyIneq, the full t0/tStar<=tI comparison, and final Type-I assembly.",
    "priority_groups": [
        {"priority": 1, "name": "Actual coarse upper and lower counts", "target_count": sum(t["priority_group"] == 1 for t in targets)},
        {"priority": 2, "name": "Uniform standard and segment parameters", "target_count": sum(t["priority_group"] == 2 for t in targets)},
        {"priority": 3, "name": "Harmonic dimensions and KeyIneq", "target_count": sum(t["priority_group"] == 3 for t in targets)},
        {"priority": 4, "name": "Final height and Type-I assembly", "target_count": sum(t["priority_group"] == 4 for t in targets)},
    ],
    "completed_Type_I_inputs": deepcopy(old["completed_Type_I_inputs"]) + [
        "GG1--GG8: actual restricted graded Gram estimate, auxiliary restriction lattice, projection and highest-vector bounds.",
        "TP1--TP11: exact GamIntC, compatible integral simultaneous partners, multiplicity identity, Cartan monotonicity and the literal TheoremMV7 under its explicit size/degree inputs.",
        "SW1--SW10: actual level forms and saturation, block/terminal estimates, exact weighted finite-sum transfer with its stated coarse-rank premise, depth arithmetic and the Std coarse-degree alternative.",
        "SW12: literal Std gives BLk(0), oPlus<=147a/250<=aPlus and sum blockOrd<=t0 for Ct>=30.",
        "RL1--RL11: actual factor recipes, reblocking, finite cleanup, source-dual chart pairing and PairLiftAt under literal Std, CE1,CE2,Cm>=17 and Ct>=30, at the t0 height.",
    ],
    "precision_notes": [
        "GG and TP close the previously retained restricted-Gram and simultaneous-partner inputs; they do not supply the arithmetic/segment size hypotheses uniformly.",
        "SW8 is a proved finite-sum implication conditional on the actual coarse upper rank-on-digits inequality and the matching explicit numerical premises; the lower half-density is also still to be supplied.",
        "RL proves the actual paired-lift construction under literal Std and its displayed constants, with SW12 giving t0. Uniform HIext=>Std and the later t0/tStar<=tI comparison remain separate.",
        "The numerical and dimension identifications should reuse completed IP/IW/CB/GG/TP/SW results where their literal hypotheses match; this map does not claim that any unmatched interface is automatic.",
        "No Type-II local theorem is substituted for the separate rank-one Type-I conclusion, and none of the four global branches below is changed.",
        "source_connections are lexical navigation hints; the targets themselves carry the exact checked ranges, URLs and hashes. They are not additional claims.",
    ],
    "targets": targets,
    "source_files": [{k: v for k, v in info.items() if not k.startswith("_")} for info in files.values()],
    "previous_global_branches_source": "v0_8/next_source_targets.json",
    "global_branches_unchanged": deepcopy(old["global_branches_unchanged"]),
}
if out["global_branches_unchanged"] != old["global_branches_unchanged"]:
    raise RuntimeError("Global branches changed")
rendered = json.dumps(out, ensure_ascii=False, indent=2) + "\n"
marker = '  "global_branches_unchanged":'
if old_raw[old_raw.index(marker):] != rendered[rendered.index(marker):]:
    raise RuntimeError("The four global branches were not preserved verbatim")
(HERE / "next_source_targets.json").write_text(rendered)
print(json.dumps({"exact_local_targets": len(targets), "source_files": len(files),
                  "global_branches": len(out["global_branches_unchanged"]),
                  "global_branch_suffix_preserved_verbatim": True,
                  "verified_commit": PIN,
                  "output_sha256": sha256(rendered.encode()).hexdigest()}, indent=2))
