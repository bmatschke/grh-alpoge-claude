"""Regenerate IN1--IN9 provenance from byte-identical pinned Lean sources.

Run with Python 3.11+ from any directory. This script needs no network and
does not run Lean or edit the source checkout. Hash ranges are inclusive,
one-indexed lines, retaining their original line endings. Declaration names
are the literal lexical namespace qualification (private declarations may
have a different compiler-generated internal name).
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
    "SC": GB + "SourceCleaning.lean",
    "L5": GB + "Lemma5aAt.lean",
    "PC": GB + "TwistedSubstitution/PlaneCoeff.lean",
    "ML": GB + "TwistedSubstitution/MemLin.lean",
    "MR": GB + "TwistedSubstitution/MemRed.lean",
    "MONO": GB + "TwistedSubstitution/Lemma5aMonomial.lean",
    "GP": GB + "TwistedSubstitution/Lemma5aGeneratorProducts.lean",
    "BLOCK": GB + "PlaneCoefficients/PlanePairsOnBlocksAt.lean",
    "TENS": GB + "PlaneCoefficients/PlaneCoeffOneTTens.lean",
    "RG": GB + "PlaneCoefficients/RenameMemSupported.lean",
    "PMAT": GB + "PlaneCoefficients/PmatDetMem.lean",
    "SP": GB + "DualFockLinear/SubstSPtrue.lean",
    "SYM": GB + "DualFockLinear/XiStepNOfP.lean",
    "SS": GB + "ScaleEdges/SymbolRealisableBound.lean",
    "HYP": GB + "ScaleEdges/ManyEdges.lean",
    "FRAME": GB + "ScaleEdges/FramesOf.lean",
    "DATA": GB + "TwistedSubstitution/Proposition5Gram.lean",
    "NPJ": GB + "TwistedSubstitution/JointEIntList.lean",
    "NT": GB + "TwistedSubstitution/TypeBound.lean",
    "NB": GB + "PlaneCoefficients/TypeBd.lean",
    "NE": GB + "PlaneCoefficients/CompDEqHomComp.lean",
    "NSPAN": GB + "PolynomialLevels/MemSpanList.lean",
    "NLEV": GB + "PolynomialLevels/LevNMonomial.lean",
    "NPR": GB + "PolynomialLevels/LowestWeightNonposOffSet.lean",
    "TH": GB + "PlaneCoefficients/ValSCongrSupp.lean",
    "AVS": GB + "AevalValuation/RestSpec.lean",
    "AVD": GB + "AevalValuation/PlDefs.lean",
    "AVG": GB + "AevalValuation/ValGen.lean",
    "AVC": GB + "AevalValuation/MemSupportedOf.lean",
    "TR": GB + "PlaneCoefficients/ProdRangeZmod.lean",
    "PH": GB + "MonomialSupport/PhMonomialMul.lean",
    "LD": GB + "PlaneCoefficients/RestPlOf.lean",
    "LL": GB + "PlaneCoefficients/MemTSetIff.lean",
    "LDEG": GB + "PlaneCoefficients/MultidegSingle.lean",
    "LSUP": GB + "PlaneCoefficients/SupportedOfSupport.lean",
    "LW": GB + "PlaneCoefficients/SumFiberMultideg.lean",
    "UNTW": GB + "TwistedSubstitution/TwistedMonomialFiltration/TwistSubXMemSupported.lean",
    "OLD": GB + "PlaneCoefficients/OldestFar.lean",
    "AR": GB + "PlaneCoefficients/FortyEightBoundArith.lean",
    "ENTRY": GB + "PlaneCoefficients.lean",
    "AV": GB + "AevalValuation.lean",
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
        "id": "IN1",
        "title": "Exact initial membership endpoint, source letters and threshold indexing",
        "status": "faithful_translation",
        "statement": "Under DataII and C>=1, every actual symP(B_b) satisfies MemAtG(0,1/8): all plane coefficients after all compatible physical digit/degree blocks and selected normal joint projectors satisfy source XX with chain theta=thStar and link theta=thStar-slU/8. Frame indices are reversed, and the odd-predecessor normal index is u-1.",
        "sources": many("DATA", ["DataII"], "literal_hypotheses")
          + many("HYP", ["Hyps"], "literal_hypotheses")
          + many("FRAME", ["FramesOK"], "literal_hypotheses")
          + many("SEG", ["Frames", "letters", "IsW", "LLset", "dist", "oldest", "Valid", "LZ"], "literal_definition")
          + many("OBJ", ["twistMat", "twistSub", "sDegs", "valS", "lam1S"], "literal_definition")
          + many("PC", ["jIso", "IsJProj", "posU", "posTL", "lowP", "NSet", "thStar", "slU", "normE"], "literal_definition")
          + many("L5", ["TL", "ML", "SignedChainData", "trueLet", "modelLet", "chainML", "TSet", "XX"], "literal_definition")
          + many("ML", ["TwistedSubstitutionGrowthBound", "MemAtG"], "exact_endpoint")
          + many("MR", ["Lemma5aAt"], "exact_endpoint")
          + many("SC", ["Bo", "sl", "alphaMax", "cPrime", "mStar"], "literal_constant_definition"),
    },
    {
        "id": "IN2",
        "title": "Actual pair span, retained degree blocks and exact tensor factorization",
        "status": "faithful_translation_with_elementary_exponent_proof",
        "statement": "The actual localizer is supported on plane vector variables. The proof holds on BlockDeg-compatible blocks of each pair-product summand, extends by multilinearity to actual symbol-space factors, and then uses physical homogeneity to eliminate incompatible blocks. A compatible low-digit block factors as A_* tensor G_*, and normal coefficient extraction after the projector is a scalar multiple of A_*.",
        "sources": many("SEG", ["XX'", "phSeg", "IsLabel", "RRdeg", "Gen"], "literal_definition")
          + many("SS", ["symbolSpaces", "G2d"], "literal_actual_family")
          + many("GP", ["pairSet", "symG", "symG_span", "g2mg", "g2th", "symbol_spaces_le_pair_span"])
          + many("GP", ["Lemma5aGeneratorProductsAt"], "stronger_unused_statement_not_claimed")
          + many("SP", ["SPR"], "literal_actual_localizer")
          + many("SYM", ["symP"], "literal_actual_symbol")
          + many("PMAT", ["pmat_det_mem", "restSP"])
          + many("PC", ["plMon", "noMon", "InLow", "InBlock", "levImg", "oneT", "planeCoeff"], "literal_definition")
          + many("BLOCK", ["BlockDeg", "blockDeg_of", "MemAtB", "memSubB", "memAtG_of_B", "PlanePairsOnBlocksAt", "rest5aMonoStep_of_B"])
          + many("TENS", ["tens", "planeCoeff_oneT_tens", "compD", "compD_mem_Pol", "levP", "levN", "zPl", "zNo", "PlaneEven", "RestT"])
          + many("RG", ["symG_eq_mul", "restT_of", "restT"])
          + many("NLEV", ["levN_zNo"]),
    },
    {
        "id": "IN3",
        "title": "All selected normal prefix types inherit the original maximum-weight cutoffs",
        "status": "proved_specialization_of_characteristic_zero_representation_theory",
        "statement": "Canonical isotypic projectors for nested/disjoint prefixes commute. Joint-isotypic vectors span each finite-degree space, so the literal IsJProj condition determines the product projector uniquely. A nonzero selected normal vector therefore has each selected type present; its largest coordinate is bounded by the original segment normal-prefix maximum. No integral direct sum or projector-denominator estimate is used.",
        "background": "Ordinary characteristic-zero complete reducibility and highest-weight extremal-weight facts, already used in v0_5 PG/IW. The report supplies the precise commutation, uniqueness, homogeneous-filtering and prefix identification argument.",
        "sources": many("NPJ", ["NSet_mono", "NSet_disj", "eeN", "eeN_spec", "eeN_mul_comm_of_val_le", "eeN_mul_comm_of_ne_index", "eeN_comm", "eeN_pol", "jointN_props"])
          + many("NSPAN", ["ee_pres", "mem_span_list", "jproj_eq", "jproj_ne"])
          + many("NT", ["TypeBound"], "exact_type_cutoff_statement")
          + many("NB", ["typeBound_proved"], "archival_binding_to_weight_theory")
          + many("NPR", ["NSet_lt", "NSet_le", "trueLet_vec", "lam_Rn_le", "lam_prod_le"])
          + many("NE", ["restN"], "exact_assembled_source_estimate"),
    },
    {
        "id": "IN4",
        "title": "Recover every thStar term, including the odd predecessor",
        "status": "faithful_translation",
        "statement": "The pair inequalities and IN3 imply v_<x(A_j)>=thStar(j,u). At an odd predecessor the supported plane prefix <=previous equals <current, while the even predecessor set and hence Bo/sl are unchanged. The selected normal index is exactly u-1.",
        "sources": many("TENS", ["RestTh"], "exact_source_target")
          + many("TH", ["valS_congr_supp", "sl_le_g2mg", "le_pred_iff", "oldest_pred", "restTh"]),
    },
    {
        "id": "IN5",
        "title": "Model-variable renaming and homogeneous filters before the power substitution",
        "status": "faithful_translation_with_direct_twist_calculus",
        "statement": "The model product Pi has the original chain order. Its exact plane level image is X^b phi(Pi), and extracting dP is a filter on model letter degrees before phi. This filter cannot lower generic order. No characteristic-zero equivariance is asserted for phi's positive-power substitutions.",
        "sources": many("AVS", ["mlOf", "chi", "MlSpec", "RestTr"], "literal_model_interface")
          + many("AVD", ["filtQ", "ValFilt", "ValAeval", "phDeg", "phExp", "CompPh"], "literal_calculus_interface")
          + many("AVG", ["filtQ_eq_sum", "valFilt", "twist_aeval", "thetaG_mem", "valAeval"])
          + many("AVC", ["chain_mem", "geo_chain", "chi_out", "val_chi"])
          + many("TR", ["seg_PsiP", "restTr"])
          + many("PH", ["phMon", "multideg_phExp", "compPh"]),
    },
    {
        "id": "IN6",
        "title": "Exact frame-digit identity and zero chain loss",
        "status": "faithful_translation_with_explicit_monomial_proof",
        "statement": "After expanding the independent lab variables, exact quotient/remainder arithmetic gives Fdig_sigma(X^beta phi Q)=0 or X^lift(floor(beta/P))Q for Q supported on ll,wc. The extra monomial contains only vector letters in each chain. Thus every frame-digit extraction retains the complete thStar chain bound.",
        "sources": many("L5", ["P", "ph", "digOK", "liftVar", "liftExp", "Fdig"], "literal_digit_definition")
          + many("AVD", ["IsLW", "PhMon", "FdigPh", "FdigSum"], "exact_digit_interface")
          + many("PH", ["fdigSum", "digOK_phExp", "liftMon_phExp", "fdig_monomial", "fdigPh"])
          + many("AVC", ["chain_core", "restChain_of"])
          + many("AV", ["restChain"], "archival_export"),
    },
    {
        "id": "IN7",
        "title": "Deleting a preceding vector frame costs only its surviving degree",
        "status": "faithful_translation_with_direct_untwisting_proof",
        "statement": "Inverse vector twisting on a degree-d_W preceding frame lowers Laurent order by at most d_W. Remaining coefficients rename into the true link. Decomposing by source letter degrees and retaining only pieces that can survive dP bounds d_W by exact dwB=Delta_j, giving link order >=thStar-Delta_j.",
        "sources": many("LD", ["PhiJ", "wSet", "LinkL", "LkDeg", "LkVars", "RestLink"], "exact_link_interface")
          + many("TENS", ["dwB", "RestPl"], "literal_loss_and_target")
          + many("UNTW", ["untw", "untw_comp", "valS_wCoeff_ge"])
          + many("LL", ["PhiJ_nonW", "PhiJ_w", "mem_TSet_iff", "linkL"])
          + many("LDEG", ["PhiJ_X_mon", "PhiJ_monomial", "lkDeg", "lkVars"])
          + many("LW", ["lkW"])
          + many("LSUP", ["restLink_of"])
          + many("ENTRY", ["level_link_of_degree_letters", "restLink"], "archival_export"),
    },
    {
        "id": "IN8",
        "title": "Exact degree cancellation and numerical bound Delta_j<=slU/8",
        "status": "faithful_translation_with_unrolled_arithmetic",
        "statement": "BlockDeg plus the base-monomial residues cancels the localizer degree and gives q_x(dP-deg b)_+<=G2d<=2a. Distinct previous-frame distances produce Delta_j<=3a/p^g with no factor r. The oldest-vector separation and actual size hypotheses give D+L1+1<=g, 48Yk^2<=p^(L1+1), and 1<=Bo/(Yk^2)<=2 floor(Bo/(Yk^2)); hence Delta_j<=slU/8. C>=1 suffices; J>=2 is also derived.",
        "sources": many("OLD", ["first_gap", "oldest_far", "deg_le"])
          + many("AR", ["arith1", "size_le_monomial_product", "forty_eight_bound_arith", "arithCondition_of_one_le", "restArith_all"])
          + many("HYP", ["Hyps"], "exact_numerical_assumptions")
          + many("FRAME", ["FramesOK"], "exact_frame_assumptions")
          + many("TENS", ["RestArithStep"], "exact_quantified_arithmetic_target"),
    },
    {
        "id": "IN9",
        "title": "Assemble the actual symbols into Lemma5aAt and expose the WT interface",
        "status": "complete_human_reconstruction_conditional_on_literal_DataII",
        "statement": "Combine IN2--IN8 on compatible blocks, extend over the defining pair spans, eliminate incompatible blocks using actual physical homogeneity, and sum the actual SPR monomials. Every symP(B_b) and their Kf-linear span satisfy MemAtG(0,1/8). WT then supplies MemAtG(1/8,3/8)=MemAt. No stronger arbitrary unblocked generator-product theorem is claimed.",
        "sources": many("TENS", ["rest5aPairBStep_of", "rest5aMono_of_cut"], "exact_source_assembly")
          + many("BLOCK", ["rest5aMonoStep_of_B", "rest5aMono_of_B"], "degree_preserving_source_assembly")
          + many("MONO", ["symP_eq_sum", "conclusionAt_of_monomialAt", "lemma5a_of_monomial"], "localizer_sum_assembly")
          + many("ML", ["tied_iff", "memAt_iff"], "interface_normalization")
          + many("MR", ["Lemma5aAt", "WordConditionAt", "memAt_of_wordConditionAt"], "interface_to_separate_WT_proof")
          + many("ENTRY", ["restMEM_of_last", "stmtE_of_pl"], "actual_closed_source_route"),
    },
]

artifacts = []
for filename in ["initial_membership_section.tex", "report.txt"]:
    raw = (WORK / filename).read_bytes()
    artifacts.append({"filename": filename, "sha256": sha256(raw).hexdigest(), "bytes": len(raw)})

ledger = {
    "title": "Initial-symbol incoming membership: IN1--IN9",
    "version": "0.6",
    "repository": URL,
    "commit": COMMIT,
    "generated_by": "regenerate_provenance.py",
    "range_convention": "Inclusive one-indexed lines; SHA256 retains original bytes and line endings. Declarations use lexical namespace qualification.",
    "source_validation": "Every cited local file compared byte-for-byte with git show COMMIT:path before generation.",
    "verification_limits": [
        "No Lean build was run for this note.",
        "The human proofs are reconstructed mathematical arguments, not new Lean formalizations.",
        "The whole claimed RH/GRH release is not certified by this local result.",
        "The actual DataII family/arithmetic/frame inputs remain explicit hypotheses; no new specialized initial-membership estimate is assumed.",
        "The stronger unused Lemma5aGeneratorProductsAt statement is not claimed; the actual blocked route is proved.",
    ],
    "prior_human_results": [
        {"path": "v0_5/local_gram/report.txt", "use": "The generic extremal-weight and nested/disjoint projector principles already used in PG; specialized again in IN3 without a new integral estimate."},
        {"path": "v0_5/integral_weyl/report.txt", "use": "Characteristic-zero highest-weight background; IW4's quantitative denominator bound is not needed for this initial membership step."},
    ],
    "artifacts": artifacts,
    "files": [{k: v for k, v in item.items() if not k.startswith("_")} for item in FILES.values()],
    "claims": CLAIMS,
}

(WORK / "provenance.json").write_text(json.dumps(ledger, indent=2, ensure_ascii=False) + "\n")
lines = ["IN1--IN9 source locators", f"Pinned commit: {COMMIT}", ""]
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
