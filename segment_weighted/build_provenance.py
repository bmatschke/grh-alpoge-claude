"""Rebuild SW1--SW11 provenance from the byte-identical pinned Lean checkout.

Run with Python 3.11+. This reads source and writes only this component's
provenance.json/source_locators.txt. It does not invoke Lean or use the network.
Line ranges are inclusive and preserve all original bytes and line endings.
Qualified declaration names are lexical; private Lean internals may differ.
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
PATHS = {'Y': 'src/Formalism/MahlerMeasure/GoodCount.lean',
 'TIEV': 'src/Formalism/MahlerMeasure/TieVars.lean',
 'LEVEL': 'src/Formalism/MahlerMeasure/LevelLattice.lean',
 'SSD': 'src/Formalism/MahlerMeasure/MahlerMeasureProofs/SSDirect.lean',
 'FOCK': 'src/Formalism/MahlerMeasure/MahlerMeasureProofs/FockBlocks.lean',
 'HARM': 'src/Formalism/ThetaLogCoordinates/BihomogeneousPairs/LetterChainEmbeddings/TieFPowMulFree.lean',
 'PST': 'src/Formalism/ThetaLogCoordinates/BihomogeneousPairs/LetterChainEmbeddings/PstScalMem.lean',
 'STEP': 'src/Formalism/ThetaLogCoordinates/BihomogeneousPairs/LetterChainEmbeddings/PairStep.lean',
 'LL': 'src/Formalism/ThetaLogCoordinates/BihomogeneousPairs/LetterChainEmbeddings/LevelLatticeOf.lean',
 'LVLDIM': 'src/Formalism/SharpRestriction/GrowthBounds/MonomialFactorials/LvlDimGen.lean',
 'DIMCOND': 'src/Formalism/SharpRestriction/GrowthBounds/MonomialFactorials/LvlDimCondition.lean',
 'SUMRANK': 'src/Formalism/SharpRestriction/GrowthBounds/MonomialFactorials/SumFinrankLeOfIndep.lean',
 'BASECHANGE': 'src/Formalism/SharpRestriction/GrowthBounds/MonomialFactorials/RestDimBCProved.lean',
 'DECOMP': 'src/Formalism/SharpRestriction/GrowthBounds/MonomialFactorials/RestDecompProved.lean',
 'DERIV': 'src/Formalism/SharpRestriction/GrowthBounds/MonomialFactorials/DegSubSingle.lean',
 'VALINPUT': 'src/Formalism/SharpRestriction/GrowthBounds/MonomialFactorials/BlockValuationZpOfValuationBound.lean',
 'VALGEN': 'src/Formalism/SharpRestriction/GrowthBounds/MonomialFactorials/DegFactNeZero.lean',
 'SUPPORT': 'src/Formalism/SharpRestriction/GrowthBounds/MonomialFactorials/SLetCastSucc.lean',
 'VALROW': 'src/Formalism/SharpRestriction/GrowthBounds/MonomialFactorials/FinPosEqCast.lean',
 'VALFINAL': 'src/Formalism/SharpRestriction/GrowthBounds/MonomialFactorials/BlockValuationOverZpHolds.lean',
 'BLOCKDUAL': 'src/Formalism/SharpRestriction/GrowthBounds/MonomialFactorials/BlockBoundOfDualFamilies.lean',
 'PLUSAW': 'src/Formalism/SharpRestriction/GrowthBounds/MonomialFactorials/PlusAWICondition.lean',
 'ORTHSPLIT': 'src/Formalism/SharpRestriction/GrowthBounds/MonomialFactorials/OrthSplitOfMin.lean',
 'ORTHCOUNT': 'src/Formalism/SharpRestriction/GrowthBounds/MonomialFactorials/OrthCountOf.lean',
 'COMM': 'src/Formalism/SharpRestriction/GrowthBounds/MonomialFactorials/CommCondition.lean',
 'PLUS': 'src/Formalism/SharpRestriction/GrowthBounds/MonomialFactorials/BejjSmulLeft.lean',
 'DIGITS': 'src/Formalism/SharpRestriction/GrowthBounds/MonomialFactorials/DigitsOKOfCompat.lean',
 'RATIO': 'src/Formalism/SharpRestriction/GrowthBounds/MonomialFactorials/RatioConditionOfSegFacts.lean',
 'SIZE': 'src/Formalism/SharpRestriction/GrowthBounds/MonomialFactorials/LowerBoundInitialMultiplicity.lean',
 'EPS': 'src/Formalism/SharpRestriction/GrowthBounds/MonomialFactorials/EpsilonBoundMConstant.lean',
 'TM': 'src/Formalism/SharpRestriction/GrowthBounds/MonomialFactorials/RestTMExists.lean',
 'SUM': 'src/Formalism/SharpRestriction/GrowthBounds/MonomialFactorials/Imports.lean',
 'WEIGHTED': 'src/Formalism/SharpRestriction/GrowthBounds/MonomialFactorials/SegmentWeightedCountingBoundOfAllRemainingBounds.lean',
 'DEPTH': 'src/Formalism/SharpRestriction/GrowthBounds/MonomialFactorials/KappaZeroNonneg.lean',
 'CLOSED': 'src/Formalism/SharpRestriction/GrowthBounds/MonomialFactorials/ClosedOfOpenConditions.lean',
 'PHIPAIR': 'src/Formalism/SharpRestriction/GrowthBounds/FockGramWindow/PhiPair.lean',
 'WINLVL': 'src/Formalism/SharpRestriction/GrowthBounds/FockGramWindow/WinLvl.lean',
 'NORM': 'src/Formalism/SharpRestriction/GrowthBounds/FockGramWindow/NormFockLe.lean',
 'LJJ': 'src/Formalism/SharpRestriction/GrowthBounds/FockGramWindow/LettersAtUPos.lean',
 'WINABS': 'src/Formalism/SharpRestriction/GrowthBounds/FockGramWindow/NeglogPowMul.lean',
 'WINNUM': 'src/Formalism/SharpRestriction/GrowthBounds/FockGramWindow/InitialPointNumericBound.lean',
 'RESTWIN': 'src/Formalism/SharpRestriction/GrowthBounds/FockGramWindow/RestWinOfLvl.lean',
 'LVLDEF': 'src/Formalism/SharpRestriction/GrowthBounds/FockGramWindow/LvlDef.lean',
 'COARSE': 'src/Formalism/SharpRestriction/GrowthBounds/BinomialRatio/CoarseDegreeAlternative.lean',
 'STD': 'src/Formalism/SharpRestriction/GrowthBounds/BinomialRatio/Transported.lean',
 'FLIP': 'src/Formalism/SharpRestriction/GrowthBounds/FlipOneThree.lean',
 'RANKDEF': 'src/Formalism/SharpRestriction/GrowthBounds/BinomialRatio/RankDefs.lean',
 'RANKDIG': 'src/Formalism/SharpRestriction/GrowthBounds/BinomialRatio/RankOnDigitsCast.lean',
 'RANKBOTH': 'src/Formalism/SharpRestriction/GrowthBounds/BinomialRatio/LeAndHalfLeProdOneSubExpNegOfBounds.lean',
 'TARGET': 'src/Formalism/SharpRestriction/GrowthBounds/ProjectionLemmaBaseLevel.lean',
 'OBJ': 'src/Formalism/SharpRestriction/GrowthBounds/ObjSeg.lean'}

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
        'id': 'SW1',
        'title': 'Actual level directness, saturation and scalar extension',
        'status': 'complete_human_proof_for_actual_SS_lattice',
        'statement': 'Lexicographically maximal scalar-variable degree proves the raw levels independent and saturated; each prefix condition is separately a stabilized finite kernel, so base change and the actual rank formula follow.',
        'dependencies': ['TI1'],
        "sources": many('Y', ['Y', 'YZ', 'YCond'])
                   + many('SSD', ['good_pre', 'ss_direct', 'ss_sat', 'semisimple_direct_sum'])
                   + many('LVLDIM', ['lvlDim_gen'])
                   + many('DIMCOND', ['lvlDimCondition'])
                   + many('SUMRANK', ['sum_gens_le', 'restSumSpan_proved'])
                   + many('BASECHANGE', ['restDimBC_proved'])
                   + many('DECOMP', ['restDecomp_proved']),
    },
    {
        'id': 'SW2',
        'title': 'Integral harmonic change of actual levels and exact Fock normalization',
        'status': 'complete_elementary_harmonic_expansion_with_explicit_logarithmic_loss',
        'statement': 'The harmonic projection and its telescoping inverse preserve the actual prefix lattices, with p^U inclusions both ways. Their orthogonal level pairing is c_j times the residual phi form, with every factorial and shift explicit.',
        'dependencies': ['TI1', 'SW1'],
        "sources": many('TIEV', ['tieP', 'RemoveS'])
                   + many('LEVEL', ['BlockData.BlockOK', 'BlockData.phiAll', 'SSDirect', 'LevelLattice', 'FockBlocks'])
                   + many('HARM', ['harmonicProjection_expand', 'decomp'])
                   + many('PST', ['pair_induction_holds'])
                   + many('STEP', ['HypJoin', 'HypU', 'PairStep'])
                   + many('LL', ['asm_num', 'asm_chain', 'LevelLattice_of'])
                   + many('DERIV', ['pderiv_ycond', 'tieF_ycond'])
                   + many('VALINPUT', ['hypU_proved', 'hypTie_proved', 'restLL_proved'])
                   + many('FOCK', ['chain_main', 'chain_orth', 'fock_blocks_of_weights', 'fock_block_decomposition']),
    },
    {
        'id': 'SW3',
        'title': 'Actual ramified block GoodSub from good level Smith factors',
        'status': 'complete_block_lattice_conversion_under_explicit_degree_bounds',
        'statement': 'The harmonic dual families, factorial row-carry bound and ramified rescaling give BlockBoundUniformiser at depth D+10(s+1)(r+1)Lambda+kappa0 with rank loss the sum of actual level bad counts.',
        'dependencies': ['TI1', 'TI2', 'SW1', 'SW2'],
        "sources": many('VALGEN', ['expU', 'expM', 'blkZ_gen'])
                   + many('SUPPORT', ['wL', 'dLvl', 'SSZ_support'])
                   + many('VALROW', ['dLvl_eq', 'val_gen'])
                   + many('VALFINAL', ['loss_num', 'restValNum_proved', 'block_valuation_over_Zp_holds'])
                   + many('BLOCKDUAL', ['block_dual_family_bound', 'block_bound_of_dual_families'])
                   + many('OBJ', ['GoodSub']),
    },
    {
        'id': 'SW4',
        'title': 'Normalized terminal tensor families and orthogonal integral basis',
        'status': 'complete_symmetric_rational_form_argument_over_odd_p',
        'statement': 'Multiplying terminal monomials by n!/alpha! gives integral normalized tensor dual families. A least-valuation pivot gives an orthogonal lattice basis even for a rational or degenerate form.',
        'dependencies': ['TI2', 'SW1'],
        "sources": many('PLUSAW', ['cf_mul', 'plusAW_of_blockOK', 'plusACondition'])
                   + many('ORTHSPLIT', ['orthSplit_of_min'])
                   + many('ORTHCOUNT', ['orthCount_of', 'orthLat_of'])
                   + many('COMM', ['commCondition', 'symmCondition'])
                   + many('PLUS', ['RestOrth']),
    },
    {
        'id': 'SW5',
        'title': 'Terminal Gram window as a single polynomial-matrix average',
        'status': 'complete_actual_terminal_average_under_listed_window_numeric_inputs',
        'statement': 'Multiplication by p^x0 binom(q+z,J) gives an integral binomial-polynomial Gram matrix whose leading matrix is the earlier diagonal Gram form. TI5 yields an explicit average and the actual RestPlus 5/Y bound under the displayed window assumptions.',
        'dependencies': ['TI5', 'SW4'],
        "sources": many('PHIPAIR', ['phi_pair', 'cW_sum', 'cW_top', 'cW_norm'])
                   + many('WINLVL', ['bnd_phisB', 'int_lvl', 'winLvl'])
                   + many('NORM', ['bnd_Xl', 'bnd_phi', 'norm_fock_le'])
                   + many('LJJ', ['Ljj_val'])
                   + many('WINABS', ['win_abs'])
                   + many('WINNUM', ['initial_point_numeric_bound', 'hx_inst', 'q_num', 'restWinNum_proved'])
                   + many('RESTWIN', ['restWin_of_lvl'])
                   + many('LVLDEF', ['x0N', 'lgN', 'JN', 'WinLvl'])
                   + many('PLUS', ['RestWin', 'restPlusB_of']),
    },
    {
        'id': 'SW6',
        'title': 'Fixed digit-class indices and endpoint mass ratio',
        'status': 'complete_under_explicit_digit_and_box_bounds',
        'statement': 'The actual kept block-level set is constant on a compatible degree box; replacing one coordinate by its endpoint changes its coarse monomial dimension by at most exp(3).',
        'dependencies': ['TI1'],
        "sources": many('DIGITS', ['mem_lv', 'idx_sub', 'restFree_proved'])
                   + many('RATIO', ['ratio_num', 'ratioCondition_of_segFacts']),
    },
    {
        'id': 'SW7',
        'title': 'Numerical specialization of the multiple-tie mean',
        'status': 'complete_epsilon_and_initial_size_checks_under_displayed_segment_bounds',
        'statement': 'The exact TP11 epsilon is at most 17/Y and hence (30+CM)/Y; the displayed coarse bounds also imply the required initial degree at least the prefix total. Other TP degree and log conditions remain explicit admissible inputs.',
        'dependencies': ['TP11'],
        "sources": many('SIZE', ['lower_bound_initial_multiplicity', 'restSI_proved', 'restTMSize_proved'])
                   + many('EPS', ['eps_num', 'epsilon_bound_M_constant', 'restTMEps_of', 'restTM_closed'])
                   + many('TM', ['restTM_of', 'restTM_exists']),
    },
    {
        'id': 'SW8',
        'title': 'Weighted digit-class summation with the coarse rank input retained',
        'status': 'complete_finite_sum_assembly_conditional_on_actual_upper_rank_and_matching_numeric_inputs',
        'statement': 'The terminal and multiple-tie averages, together with sum_z dim(Y)d_xi<=m(a), imply total bad count <=[(30+CM)t exp(3)+5]/Y times terminal-window size and ambient mass. The actual coarse rank inequality is not proved by summation.',
        'dependencies': ['TI2', 'SW1', 'SW3', 'SW5', 'SW6', 'SW7'],
        "sources": many('SUM', ['assemble'])
                   + many('WEIGHTED', ['rank_le', 'claim2', 'digit_class_dimension_comparison_of_remaining_estimates', 'RestAll', 'segment_weighted_counting_bound_of_all_remaining_bounds'])
                   + many('FLIP', ['adm11'], 'retained_actual_coarse_rank_input'),
    },
    {
        'id': 'SW9',
        'title': 'Final segment-depth arithmetic',
        'status': 'complete_arithmetic_under_SW_explicit_inputs',
        'statement': 'The depth is bounded by C Y^2 N1^2(r+1)^2 Lambda+kappa0 for C>=18(1+CM)+20; the additional fixed mass constant matches the source SegmentWeightedCountingBound.',
        'dependencies': ['SW3', 'SW5', 'SW8'],
        "sources": many('DEPTH', ['depth_num', 'restDepth_proved'])
                   + many('CLOSED', ['restAllE_of_open']),
    },
    {
        'id': 'SW10',
        'title': 'Exact coarse-degree alternative from literal Std',
        'status': 'complete_under_literal_standard_parameters_including_excluded_band',
        'statement': 'The odd-power gap and two elementary scalar inequalities give A(1+delta)<A0 before the split and A0<A(1-delta) after it, with the floor and digit errors retained.',
        'dependencies': ['TI1'],
        "sources": many('STD', ['Std'], 'literal_numeric_input')
                   + many('COARSE', ['coarse_bounds', 'poly_S', 'poly_U', 'dich_S', 'dich_U', 'eps', 'Std.eps_ge', 'Std.kQ', 'Std.kQeps', 'Std.levels', 'coarse_degree_alternative']),
    },
    {
        'id': 'SW11',
        'title': 'Type-I local frontier after form and weighted-sum reconstruction',
        'status': 'explicit_remaining_boundary_not_a_full_Type_I_or_RH_proof',
        'statement': 'Coarse rank-on-digits upper and lower estimates, full simultaneous numerical supply and the final t0<=tI comparison remain separate; RL and SW12 supply actual cleaned lifts under literal Std. Global RH/Dirichlet GRH obligations remain unchanged.',
        'dependencies': [],
        "sources": many('RANKDEF', ['UpAt', 'LowAt', 'RestUp', 'RestLow'], 'remaining_rank_target')
                   + many('RANKDIG', ['restUp_of'], 'remaining_rank_route')
                   + many('RANKBOTH', ['one_segment_of_upper_lower'], 'remaining_rank_route')
                   + many('TARGET', ['HypI', 'WeightI', 'tI', 'Conclusion2'], 'remaining_full_Type_I_target'),
    },
]

artifacts = []
for name in ("report.txt", "segment_weighted_section.tex", "build_provenance.py"):
    raw = (HERE / name).read_bytes()
    artifacts.append({"path": name, "sha256": sha256(raw).hexdigest(), "bytes": len(raw)})
payload = {
    "component": "v0.9 Type-I weighted segment construction", "claims": CLAIMS,
    "repository": BASE_URL, "commit": COMMIT,
    "head_verified": actual_head,
    "line_range_convention": "inclusive, one-indexed, original bytes including line endings",
    "source_files": [{k: v for k, v in info.items() if not k.startswith("_")} for info in FILES.values()],
    "artifacts": artifacts,
    "scope_note": "SW1--SW10 prove the actual local form mechanisms under the hypotheses written in the main text; SW8 retains the actual coarse-rank inequality. Literal Std is an input to SW10. No full Type-I or RH/GRH conclusion or Lean replay is asserted.",
}
(HERE / "provenance.json").write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n")
lines = [f"Weighted segment provenance at {COMMIT}", ""]
for claim in CLAIMS:
    lines.extend([f"{claim['id']}: {claim['title']}", f"Status: {claim['status']}"])
    for src in claim["sources"]:
        lines.append(f"  {src['declaration']} | {src['path']}:{src['line_start']}-{src['line_end']} | {src['role']}")
        lines.append(f"    {src['pinned_url']}")
        lines.append(f"    file sha256 {src['full_file_sha256']} ; range sha256 {src['range_sha256']}")
    lines.append("")
(HERE / "source_locators.txt").write_text("\n".join(lines) + "\n")
print(json.dumps({"claims": len(CLAIMS), "source_files": len(FILES),
                  "locators": sum(len(c['sources']) for c in CLAIMS),
                  "verified_commit": COMMIT, "artifacts": artifacts}, indent=2))
