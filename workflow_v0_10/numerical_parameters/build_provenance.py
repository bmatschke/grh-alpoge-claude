"""Rebuild NP1-NP9 provenance from the pinned, byte-identical Lean checkout.

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
PATHS = {k: GB + v for k,v in {'STD': 'BinomialRatio/Transported.lean', 'LOW': 'BinomialRatio/ThresholdLowerBounds.lean', 'THR': 'BinomialRatio/ExtendedStatementOfParts.lean', 'LOC': 'ColumnSystems.lean', 'OBJ': 'ObjSeg.lean', 'FLIP': 'FlipOneThree.lean', 'HIF': 'CountingStatementReduction.lean', 'SEGF': 'MonomialFactorials/CoarseCLower.lean', 'WIN': 'MonomialFactorials/WindowEntryLeTwoMulA.lean', 'SIZE': 'MonomialFactorials/RestTMSizeOf.lean', 'N0': 'MonomialFactorials/LowerBoundInitialMultiplicity.lean', 'TMH': 'MonomialFactorials/RestTMHypOf.lean', 'TME': 'MonomialFactorials/EpsilonBoundMConstant.lean', 'TM': 'MonomialFactorials/RestTMExists.lean', 'SB': 'MonomialFactorials/UTopVal.lean', 'DIST': 'MonomialFactorials/SegDistsLtG.lean', 'RATIO': 'MonomialFactorials/RatioConditionOfSegFacts.lean', 'PROJ': 'ProjectionLemmaBaseLevel.lean', 'DAT': 'ColumnSpanDensity/RhoLowerBoundLargeConductor.lean', 'BASE': 'ColumnSpanDensity/NumBase.lean', 'ROUND': 'ColumnSpanDensity/TwoHundredLeRadius.lean', 'DEPTH': 'ColumnSpanDensity/FourDepthLtConductorOfBounds.lean', 'JF': 'ColumnSpanDensity/ThresholdFixedWeightFacts.lean', 'FACT': 'ColumnSpanDensity/FactorizationBoundMonoLattices.lean', 'MEAN': 'ColumnSpanDensity/LocalHypothesisOfGlobal.lean', 'HEIGHT': 'ColumnSpanDensity/InitialLevelFormula.lean', 'SEG': 'ColumnSpanDensity/SegStartSpec.lean', 'ODD': 'ColumnSpanDensity/OddTops.lean', 'LP': 'ColumnSpanDensity/ThrLPOf.lean', 'KAP': 'BinomialRatio/KapCore.lean', 'FAMILY': 'BinomialRatio/FamilyFourthBound.lean'}.items()}

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



DEFS = [{'id': 'NP1', 'title': 'Six-term error bound with explicit positive hypotheses', 'dependencies': [], 'statement': 'Each of the six unweighted summands in E0+Q is at most a*N1*lambda/k^2; hence (E0+Q)/a<=N1*lambda/k under the literal elementary hypotheses.', 'src': {'LOW': ['error_ratio_le_epsilon'], 'OBJ': ['errorTermBound']}}, {'id': 'NP2', 'title': 'Complete uniform D1num+HIext+CBound to Std, for every fixed H>=1', 'dependencies': ['NP1'], 'statement': 'All 29 Std fields follow for T2=1000(CE1+CE2+1)(Cc+1)H, with the exact three-stage TransportedAlt quantifier order preserved; H=4 supplies RD and implies H=1 for RL/SW.', 'src': {'STD': ['TransportedAlt', 'TransportedAlt.and', 'TransportedAlt.of_explicit', 'be', 'Std'], 'LOW': ['numSeg_le_card', 'T2', 'chordCoeffCubic_inversionDenom_inv', 'std_of'], 'LOC': ['Loc', 'k', 'N', 'Q', 'La', 'de', 'E0', 'D1num', 'CBound', 'Loc.J0', 'WindowHypotheses', 'InWin', 'HIext'], 'THR': ['thr_std'], 'OBJ': ['lambdaScale', 'errorTermBound']}}, {'id': 'NP3', 'title': 'Actual segment size, logarithmic degree and multiple-tie numerical supply', 'dependencies': ['NP2', 'SW5', 'SW6', 'SW7', 'SW12', 'TP11'], 'statement': 'Literal segment HI gives SegFacts; the actual maximum-tie model has all degrees<=2a, total degree<=4a<=8a and Si<=n0i. The source RestTMHyp, terminal window and SW5-9 numerical assumptions are supplied uniformly; CM=1.', 'src': {'FLIP': ['Inst', 'winA', 'HI'], 'HIF': ['HIFacts', 'hiFacts'], 'SEGF': ['SegFacts', 'segFacts', 'coarseC_lower', 'coarseA_upper'], 'WIN': ['window_entry_le_two_mul_a', 'r5', 'b_small', 'chain_wt', 'oplus_le', 'lLL_deg_le_chain', 'lLL_deg_le'], 'SIZE': ['RestSI', 'aTopPt_mem', 'setTies_top', 'restTMSize_of'], 'N0': ['cast_sub_ge', 'lower_bound_initial_multiplicity', 'restSI_proved', 'restTMSize_proved'], 'TMH': ['RestTMSize', 'lgA_ge_one', 'r_ge_two', 'p_ne_two', 'restTMHyp_of'], 'TME': ['EpsFacts', 'epsFacts', 'restTMEps_of', 'restTMEps_proved', 'restTM_closed'], 'TM': ['restTM_of', 'restTM_exists'], 'SB': ['S_bound'], 'DIST': ['p_le_P'], 'RATIO': ['ratio_num', 'ratioCondition_of_segFacts']}}, {'id': 'NP4', 'title': 'All base facts and exact integer-radius transfer including the odd-power exclusion', 'dependencies': [], 'statement': 'HypI with C_H>=TM yields Base and rounded HypI at radius ceil(ar), Yb/2 and constant K.CH. The forbidden interval is contained in the original interval; no new odd-power-gap premise is assumed.', 'src': {'PROJ': ['LaI', 'deI', 'HypI'], 'DAT': ['Cst', 'Cst.Pos', 'Dat', 'a', 'Hyp'], 'BASE': ['Cst.TLP', 'Base', 'base_of'], 'ROUND': ['Cst.TM', 'two_hundred_le_radius', 'log_round', 'La_round', 'r12', 'r15', 'r16', 'rde', 'rband', 'r19', 'r22', 'hyp_round'], 'DEPTH': ['logs_of']}}, {'id': 'NP5', 'title': 'Exact depths, conductor inequalities, floors and cleaning windows', 'dependencies': ['NP4'], 'statement': "The five explicit terms give 2D1+N*kappa1<=(6CA+84)NY^2k^3 log_p ar<=Dp, hence 4D1<c4; J>=3, J0<=b'/216 and every degree-window inequality are proved.", 'src': {'DAT': ['c4', 'u0c', 'kap1c', 'D0', 'D1', 'J0', 'Jn'], 'DEPTH': ['dle_abs', 'logs_of', 'D0_eq_numSeg_mul_add', 'D1nn_of', 'dle_of', 'four_depth_lt_conductor_of_bounds'], 'JF': ['JFacts', 'jFacts_of', 'D0nn_of', 'small_depth_le_large_depth', 'window_lower_bound_of_base', 'winA_of', 'winB_of', 'jA_of', 'jB_of', 'degree_sum_le_eight_mul']}}, {'id': 'NP6', 'title': 'Uniform fixed-weight and mean-kappa numerical records', 'dependencies': ['NP4', 'NP5'], 'statement': "For C_H>=TM every field of FixedWeightNumericalFacts and MeanKappaNumericalFacts follows, including CBoundI(4), both extended windows and m0<=b'/(kQY).", 'src': {'FACT': ['FixedWeightNumericalFacts'], 'MEAN': ['MeanKappaNumericalFacts', 'locOf', 'local_hypothesis_of_global', 'instOf'], 'JF': ['cb_of', 'logl_of', 'multiplicity_bound_nonneg', 'multiplicity_bound_abstract', 'multiplicity_bound_le_ratio', 'fixed_weight_facts_of_hyp', 'mean_kappa_facts_of_hyp', 'threshold_fixed_weight_facts', 'threshold_mean_kappa_facts'], 'OBJ': ['m1G4', 'm0G4'], 'PROJ': ['CBoundI']}}, {'id': 'NP7', 'title': 'Cyclic reindexing and the actual shifted final Type-I height', 'dependencies': ['NP4', 'SW12'], 'statement': "Every odd marked point has its unique preceding even endpoint, and shifting both degree families increases the principal sum by at most N*ccl. The exact ceiling height satisfies tStar(aw+ccl,bw+ccl)+2*n'*ccl<=tI for C>=4Ct+4.", 'src': {'PROJ': ['dPrev', 'yPrev', 'IaZ', 'IbZ', 'tI'], 'DAT': ['t0', 'tStar'], 'HEIGHT': ['RestOddTops', 'tle_abs', 'initial_level_formula'], 'SEG': ['segPos_spec', 'segStart_spec', 'ex_cast', 'min_shift', 'tle_of'], 'ODD': ['next_min', 'prev_segPos', 'odd_in_seg', 'restOddTops']}}, {'id': 'NP8', 'title': 'All FactsLP fields with uniform source thresholds', 'dependencies': ['NP4', 'NP5', 'NP7'], 'statement': 'The literal FactsLP is supplied for C_H>=TLP and C>=4Ct+4, including depth, conductors, small boundary fraction, lower degree bounds and actual shifted height.', 'src': {'DAT': ['TransportedAlt', 'FactsLP'], 'BASE': ['Cst.TLP'], 'DEPTH': ['k_le_G', 'Nccl_le', 'eps_of', 'ccl_le_b', 'b_le_a', 'second_moment_of_columns', 'lowa_of', 'lowb_of'], 'LP': ['TLP_pos', 'thrLP_of', 'thrLP']}}, {'id': 'NP9', 'title': 'Explicit uniform coarse-kappa margin bound', 'dependencies': ['NP2'], 'statement': 'The actual kappaP is at most Cs*N*N1/Y with Cs=Ckap*(Cm+4CE1+CE2+15), in exactly the source FamilyFourthBound quantifier order.', 'src': {'OBJ': ['kappaMarginBound', 'errorTermBound', 'm0G4'], 'KAP': ['kap_core', 'rest2'], 'LOC': ['kapP', 'ExtendedKappaBound'], 'FAMILY': ['FamilyFourthBound']}}]

CLAIMS=[]
for d in DEFS:
    c={k:v for k,v in d.items() if k!='src'}
    c['status']='proved_by_explicit_elementary_inequalities_and_literal_field_checks'
    c['sources']=[locator(key,name) for key,names in d['src'].items() for name in names]
    CLAIMS.append(c)
artifacts=[]
for name in ['main.tex','report.txt','build_provenance.py']:
    raw=(HERE/name).read_bytes()
    artifacts.append({'path':name,'sha256':sha256(raw).hexdigest(),'bytes':len(raw)})
payload={'artifact_version':'0.10','component':'numerical_parameters','repository':BASE_URL,'commit':COMMIT,
 'head_verified':actual_head,'line_range_convention':'inclusive, one-indexed, original bytes including line endings',
 'claims':CLAIMS,'source_files':[{k:v for k,v in f.items() if not k.startswith('_')} for f in FILES.values()],
 'artifacts':artifacts,'explicit_external_dependencies':['SW5','SW6','SW7','SW12','TP11'],
 'scope_note':'Uniform finite numerical records and exact shifted height. No global arithmetic existence, complete RH/GRH proof, Lean compilation or kernel replay is asserted.'}
(HERE/'provenance.json').write_text(json.dumps(payload,indent=2,ensure_ascii=False)+'\n')
lines=[f'NP1-NP9 source ledger at {COMMIT}','']
for c in CLAIMS:
    lines += [c['id']+': '+c['title'],'Dependencies: '+', '.join(c['dependencies'])]
    for x in c['sources']:
        lines += [x['declaration']+' | '+x['path']+':'+str(x['line_start'])+'-'+str(x['line_end']),
                  x['pinned_url'],'file '+x['full_file_sha256']+' ; range '+x['range_sha256']]
    lines.append('')
(HERE/'source_locators.txt').write_text('\n'.join(lines)+'\n')
print(json.dumps({'claims':len(CLAIMS),'files':len(FILES),'references':sum(len(c['sources']) for c in CLAIMS),'commit':COMMIT}))
