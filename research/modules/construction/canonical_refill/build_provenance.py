#!/usr/bin/env python3
"""Rebuild RF provenance from pinned Git blobs; never modify the checkout."""
from pathlib import Path
import argparse
import hashlib
import json
import re
import subprocess

ROOT = Path(__file__).resolve().parent
PARSER = argparse.ArgumentParser()
PARSER.add_argument('--repo', type=Path,
                    default=ROOT.parents[1] / 'lean-source')
ARGS = PARSER.parse_args()
REPO = ARGS.repo.resolve()
COMMIT = '7cbf7a0c32fca1badf05931879a37c3f8a2b03b4'
URL = 'https://github.com/CocoSgt/riemann-hypothesis-lean'
GP = 'src/Development/AbelianVarietyTheory/Proofs/GlobalInterpolation/'
DP = 'src/Development/AbelianVarietyTheory/Definitions/GlobalTwisting/'
LC = 'src/Formalism/LocalRingCardinality/'
GB = 'src/Formalism/SharpRestriction/GrowthBounds/'
ST = DP + 'SetUnipotentTranslate.lean'
GC = GB + 'IsResidueClassZero.lean'
cache = {}


def sha(data):
    return hashlib.sha256(data).hexdigest()


def blob(path):
    if path not in cache:
        raw = subprocess.check_output(
            ['git', '-C', str(REPO), 'show', f'{COMMIT}:{path}'])
        if (REPO / path).is_file():
            assert (REPO / path).read_bytes() == raw, path
        cache[path] = raw
    return cache[path]


def source(path, spelling, namespace='', role='proof'):
    raw = blob(path)
    lines = raw.splitlines(keepends=True)
    text = [line.decode('utf-8').rstrip('\r\n') for line in lines]
    pattern = re.compile(
        r'^(?:@\[[^\n]*?\]\s*)?(?:(?:private|protected|noncomputable)\s+)?'
        r'(?:theorem|lemma|def|abbrev|structure)\s+'
        + re.escape(spelling) + r'(?=\s|\{|\(|:)')
    starts = [i for i, line in enumerate(text) if pattern.search(line)]
    assert len(starts) == 1, (path, spelling, starts)
    start = starts[0]
    end = start + 1
    boundary = re.compile(
        r'^(?:(?:private|protected|noncomputable)\s+)?'
        r'(?:theorem|lemma|def|abbrev|structure|instance|variable|namespace|end|open|section|set_option)\b|^@\[')
    while end < len(lines) and not boundary.match(text[end]):
        end += 1
    while end > start + 1 and not text[end - 1].strip():
        end -= 1
    selected = b''.join(lines[start:end])
    qualified = namespace + '.' + spelling if namespace else spelling
    if qualified.startswith('_root_.'):
        qualified = qualified[len('_root_.'):]
    return dict(path=path, declaration=qualified, source_spelling=spelling,
                line_start=start + 1, line_end=end,
                sha256=sha(raw), full_file_sha256=sha(raw),
                range_sha256=sha(selected), range_bytes=len(selected),
                url=f'{URL}/blob/{COMMIT}/{path}#L{start+1}-L{end}',
                pinned_url=f'{URL}/blob/{COMMIT}/{path}#L{start+1}-L{end}',
                first_line=text[start], declaration_lines_within_range=[start+1],
                role=role, verified_equal_to_pinned_git_blob=True)


def many(path, names, namespace='', role='proof'):
    return [source(path, n, namespace, role) for n in names]


def refill(*names):
    return many(GP+'ExistsRefill.lean', names, 'GlobalTheory.Refill')


def led(*names):
    return many(GP+'ExistsLedPart.lean', names, 'GlobalTheory.EX.Led')


def growth(*names):
    return many(GC, names, 'Formalism.MainNotions.G', 'literal_definition_or_support')


def objdefs(*names, role='input_definition'):
    return many(ST, names, 'GlobalTheory.EX.OB', role)


def basic(file, *names, role='literal_definition_or_support'):
    return many(LC+file+'.lean', names, 'Formalism.BasicNotions', role)


def spec(ident, title, statement, deps, sources, status='faithful_translation'):
    return dict(id=ident, title=title, statement=statement, depends_on=deps,
                status=status, mathematical_status='proved_under_explicit_hypotheses',
                introduced_in='0.14',
                proof_location=dict(file='canonical_refill/main.tex',
                                    expanded='canonical_refill/report.txt', section=ident),
                assumptions=[
                    'The actual D7, number-field/host/frame and source scalar definitions are retained.',
                    'Geometric Lay/RecOK/LedOK and constructor inputs are supplied exactly where stated; no global model or metric existence is inferred.',
                    'Classical number-ring ideal factorization, localization and elementary finite-group/real analysis are declared background.',
                    'No Lean build or kernel replay was performed.'
                ], sources=sources)


claims = [
spec('RF1', 'Canonical orbit selector in the original labels',
     'The least-label representative bsH belongs to the h-orbit and is unchanged by t -> t+h.',
     [],
     many('src/Formalism/LocalToGlobal/GlobalTheory/IsResidueClassZero.lean', ['bsH'],
          'Formalism.L2.GlobalTheoryTheory.Arith', 'literal_definition')
     + refill('bsH_orb', 'bsH_step')),
spec('RF2', 'Exact canonical filling and defining numerical instance',
     'The piecewise offC fills the actual weights on 1..m, obeys every top/thick/thin window, has fill>=1 when w>=1, and constructs CanonInst, EpDef and KapIDef without assuming EpTie.',
     ['RF1', 'GJ1'],
     refill('plGG_inj', 'eTau_tauPl', 'top_iff', 'thick_iff', 'offC',
            'offC_top', 'offC_thick', 'offC_thin', 'inst', 'inst_canon',
            'inst_fill', 'one_le_fill')
     + growth('IsTopPl', 'IsThickPl', 'IsThinPl', 'Inst', 'fill', 'partner')
     + many(DP+'ThinScalesIffHostBound.lean', ['CanonInst'], 'GlobalTheory.EX', 'literal_definition')
     + many(GB+'DefsInst.lean', ['EpDef', 'kapISet', 'one_mem_kapISet', 'KapIDef', 'sInf_mem_kapISet'],
            'Formalism.MainNotions.G', 'retained_definition_and_GJ1_route')),
spec('RF3', 'One finite exceptional support for every word and index',
     'The explicit B_S and finite union of places p<=B_S with the finite twist set satisfies Big: outside it p>Xpp, no exceptional/type prime or DGam divisor occurs, and mu=mu0.',
     [], refill('finite_over', 'finite_le', 'Big', 'exists_big')),
spec('RF4', 'Literal gain, forcing, error and deficit values have common support',
     'The exact gainP/Fval/Eval/tauP/ioP formulas vanish outside RF3 support, preserve the own-type-prime priority and ramification divisions, and forcing is conjugation invariant. Installing these values asserts no new local estimate.',
     ['RF2', 'RF3'],
     growth('stepP', 'nP', 'reps', 'topsOn', 'Nv', 'IsV', 'Good', 'DIIf', 'DIf',
            'tIIf', 'kapIIf', 'tIf', 'kapLoc', 'al', 'capU', 'IsDist', 'Excl',
            'dl', 'g0', 'gU', 'Pr', 'Dp', 'tv', 'kapv', 'Cand', 'goodReps',
            'Sig', 'VV', 'Sv', 'tauP', 'ioP', 'gainP')
     + basic('DataParams₂', 'lpFeasible', 'lpF', 'wj')
     + basic('DataForced', 'tauPl', 'wPl', 'posPl', 'posPl_period', 'lpF_shift',
             'FOrb', 'FOrb_step', 'FInert', 'FRamD', 'fockDeg', 'FTypeG',
             'FvalP', 'Fval', 'sum_orbits', 'cls_ramD', 'FvalP_above',
             'resChar_conj', 'Fval_conj')
     + basic('DataErr', 'nuAbs', 'tauPib', 'vNN', 'EatG', 'Wtau', 'EatT',
             'ctD', 'EatD', 'EatC', 'kindA', 'kindBC', 'topsBC', 'EatX',
             'EatI', 'Eval', 'Eval_above')
     + many(DP+'PairRowIffQdRows.lean', ['HostArith'], 'GlobalTheory.EX', 'input_definition')),
spec('RF5', 'Complete canonical refill with exact parameter preservation',
     'Under the literal exists_refill inputs, the explicit refill preserves scale/aT/bT/Val and gives CanonInst, EpDef, KapIDef, FDef, EDef, support containments, all ParametersFill fields and the exact generally infinite drop set.',
     ['RF1', 'RF2', 'RF3', 'RF4'],
     refill('VV_empty', 'tau_eq_zero_of_not_candidate', 'ioP_eq_zero_of_not_cand',
            'TTP_subset', 'refill', 'exists_refill')
     + growth('TTP', 'aL', 'bL', 'ParametersFill')
     + basic('DataParams₂', 'SizeData₂')
     + basic('DataForced', 'SizeData₂.FDef')
     + basic('DataErr', 'SizeData₂.EDef')
     + many('src/Formalism/SharpRestriction/ParConsts.lean', ['NoGain'],
            'Formalism.MainNotions', 'literal_definition')
     + many(DP+'PairRowIffQdRows.lean', ['Val'], 'GlobalTheory.EX', 'preserved_input_definition')),
spec('RF6', 'Served primes cannot satisfy NoGain',
     'Nonempty VV forces the candidate and loss bounds and excludes every NoGain alternative. Odd Frobenius order divides the small index o, contradicting the required lower order. Dropped or non-inert/non-signal primes are unserved.',
     ['RF5'],
     led("X'_le_X''", 'cand_of_VV', 'not_noGain')
     + growth('InBand', 'HEv', 'IsCs', 'HEv.not_isCs')
     + many('src/Development/AutomorphicArithmetic/OrbitLabellings/EvenAddOrderOfHPOfPowLe.lean',
            ['UpperTheory.even_addOrderOf_hP_of_pow_le'])
     + many('src/Formalism/SharpRestriction/RamificationFrobenius/TotientGaloisClasses/FrameFacts.lean',
            ['index_A0_eq_o', 'eq_zero_of_mem_cyclic_of_projection',
             'addOrderOf_h_dvd', 'addOrderOf_h_dvd_two_pow',
             'o_smul_mem_A0', 'o_nsmul_of_h_eq_zero'], 'Formalism.HC.Frame')),
spec('RF7', 'Complete literal LedPart construction under supplied geometric conditions',
     'Apply LedOK first for untwisted Fval, refill, then apply LedOK to that same new datum. LP patches Mram-relative local modules; RF6 proves all NuDef dropped-place equalities and the quotient-zero argument gives lats0. All LedPart fields and scale/degree/Val/CanonInst conclusions follow.',
     ['RF5', 'RF6', 'LP4', 'LP5'],
     led('setLat', 'setInst', 'exists_ledPart')
     + objdefs('Lay', 'RecOK', 'WtEq', 'LedOK', 'LedPart')
     + many(LC+'DataDIVDefs.lean', ['NuDef', 'lenLoc', 'MramL'], 'Formalism.BasicNotions.DV', 'literal_definition')
     + basic('DataLatDefs', 'LatDefs')
     + basic('DataExtra', 'EpTie', 'NuUnserved')
     + basic('DataErr', 'ErrDefs')
     + many(LC+'Lemmas.lean', ['DV.lenLoc_eq_zero'], 'Formalism.BasicNotions')
     + many(LC+'Lemmas.lean', ['lenMN_unserved'], 'Formalism.BasicNotions.LatCmp')
     + many('src/Formalism/SharpRestriction/InertJacobiLevels/AsmIface.lean',
            ['TiesAt'], 'Formalism.MainNotions.Inhab', 'literal_definition')),
spec('RF8', 'Actual ideal-scaled lattice and height installation',
     'Set Nprime=I_u*NuLat with I_u=product P_w^(-floor(e_w*sg_u,w)); install hExpl6 and the max height allowance. The actual local numerical/maps/NP and auxiliary chain objects transport unchanged, yielding LedPart.pt with its exact identities, not new geometric or metric estimates.',
     ['RF7'],
     objdefs('setDiv', 'ledTr', 'instTr', 'downTo_tr', 'iota_tr', 'Qsp_tr',
             'RRset_tr', 'iiStar_tr', 'kapOf_tr', 'rrDef_tr', 'kapSharp_tr',
             'VV_tr', 'tau_translate', 'ioP_instTr', 'gainP_instTr', 'TTP_tr',
             'fills_tr', 'NP_tr', 'bk_tr', 'sLen_tr', 'twAt_tr', 'extraTr',
             'LedPart.extra', 'nPrime', role='construction_and_transport')
     + many(ST, ['ht', 'pt', 'pt_val', 'pt_wtEq', 'pt_canon', 'pt_has'],
            'GlobalTheory.EX.OB.LedPart')
     + many(LC+'DataDIVDefs.lean', ['ur', 'Iu', 'NprimeDef'], 'Formalism.BasicNotions.DV', 'literal_definition')
     + many(LC+'DataParams₂.lean', ['gainD', 'sg'], 'Formalism.BasicNotions.SizeData₂', 'literal_definition')
     + many(LC+'KernelPlaceMeanBound.lean', ['hExpl6'], 'Formalism.BasicNotions.DV', 'installed_expression')
     + many(DP+'DisjointExceptional.lean', ['Pt'], 'GlobalTheory.EX', 'literal_definition')),
spec('RF9', 'Elementary uniform scale thresholds',
     'Under RankVal, fixed epsilon>0 gives wpp>=1 at an explicit threshold; log T>=cs*m*x^epsilon gives Xprime<=T once x^(2epsilon/3)>=1/cs. These preserve the source threshold dependence.',
     [],
     many(DP+'ObjCOfRecExObjO.lean', ["scale_X'_le_of_log", "scale_one_le_w''"],
          'GlobalTheory.EX.OB.Bridge', 'source_conclusions_with_simpler_proof')
     + many(DP+'PairRowIffQdRows.lean', ['RankVal'], 'GlobalTheory.EX', 'input_definition')
     + many(LC+'DataParams₂.lean', ['b', 'a', "X'", "b'", "w''", "X''"],
            'Formalism.BasicNotions.Scale', 'literal_definition'), 'derived_simplification'),
spec('RF10', 'Uniform point join with explicit upstream construction premises',
     'With RecExP, LevelPrime and the retained chGood/level/initial-size constructors, construct the actual ObjCP point by RF7-RF8 with the exact nested threshold order and same host, labels and word code. This is a conditional join, not a proof of those suppliers or NumAt.',
     ['RF7', 'RF8', 'RF9'],
     many(GP+'ExistsObjectsOfAdmissibleTwistDatum.lean', ['objCP_and_of_recExP'], 'GlobalTheory.Fc', 'conditional_consumer')
     + many(DP+'ValidForConstructedPointClassesEventuallyWorking.lean', ['ParEv', 'RecExP', 'ObjCP'],
            'GlobalTheory.Fc', 'exact_quantifier_definition')
     + many(DP+'ObjCOfRecExObjO.lean', ['exists_T_of_over'], 'GlobalTheory.EX.OB.Bridge')
     + objdefs('chGood_of_host', role='retained_constructor_input')
     + many(GP+'ExistsLevChOfLevelPrime.lean', ['exists_levCh_of_levelPrime'], 'GlobalTheory.EX.OB', 'retained_constructor_input')
     + many(GP+'ExistsParametersOver.lean', ['exists_sizeData_over'], 'GlobalTheory.EX.OB', 'retained_constructor_input')
     + many(DP+'LogCondLeThree.lean', ['LevelPrime'], 'GlobalTheory.EX', 'retained_analytic_input_definition')),
spec('RF11', 'Elementary quantitative power and exponential comparison',
     'The exponential series gives explicit uniform thresholds for every fixed logarithmic-power comparison, proving the full scale_poly_comparison list, including its n-uniform thin-size and conductor-scale clauses.',
     [],
     many(GP+'ConstMulRpowMulLogPowLeRpow.lean', ['_root_.GlobalTheory.const_mul_rpow_mul_log_pow_le_rpow'], role='source_conclusion_reproved_by_exponential_series')
     + many(GP+'LogAddRpowMulLogPowLeRpow.lean', ['log_add_rpow_mul_log_pow_le_rpow'], 'GlobalTheory', 'source_conclusion_reproved_by_exponential_series')
     + many(GP+'ScalePolynomialQuantitiesComparison.lean', ['_root_.GlobalTheory.scale_poly_comparison'], role='full_source_conclusion_reproved')
     + many(DP+'PairRowIffQdRows.lean', ['SzRow'], 'GlobalTheory.EX', 'exact_quantifier_definition')
     + many(GP+'SzRowAndImp.lean', ['SzRow.and'], 'GlobalTheory.EX', 'finite_threshold_join')
     + many(LC+'DataParams₂.lean', ['L', 'b', 'a', "X'", "b'", "w''", "X''"], 'Formalism.BasicNotions.Scale', 'literal_definition'),
     'derived_simplification'),
spec('RF12', 'All seventeen rank bounds and seven rank-parameter inequalities',
     'The exact rational exponent table proves every rank_basic_bounds conclusion, including nW<=x^22.9, x^377<=t<=x^401 and N(m)<=x^402, and both complete rank-parameter supplier families under the literal RankVal windows.',
     ['RF11'],
     many(GP+'ExplicitRanksBasicBoundsLargeScale.lean', ['rank_const_absorb', 'rank_mul_le', 'rank_basic_bounds'], 'GlobalTheory.EX', 'full_source_bounds_reproved')
     + many(GP+'ExplicitRanksBasicBoundsLargeScaleStatement.lean', ['_root_.GlobalTheory.T.explicitRanks_basic_bounds_large_scale'], role='complete_source_conclusion')
     + many(GP+'ExplicitChoiceRankKLowerUpperBounds.lean', ['rank_k_ineqs_poly_wide', 'rank_k_ineqs_poly', 'explicitChoice_rankK_lower_upper_bounds'], 'GlobalTheory.EX', 'complete_parameter_family')
     + many(GP+'RankRowsOfCrudeBounds.lean', ['rank_rows_of_crude_bounds', 'szRow_rank_lower_bounds'], 'GlobalTheory.EX', 'complete_parameter_family')
     + many(DP+'PairRowIffQdRows.lean', ['TOv', 'nWv', 'RankVal'], 'GlobalTheory.EX', 'literal_input_and_definitions')
     + many(LC+'Params.lean', ['Ranks'], 'Formalism.BasicNotions', 'literal_input_definition')
     + many(LC+'Params.lean', ['n', 'f', 'r', 'N'], 'Formalism.BasicNotions.Ranks', 'literal_definition')
     + many(LC+'DataParams.lean', ['jG', 'R0'], 'Formalism.BasicNotions.LevelStarExponents', 'literal_definition'),
     'derived_simplification'),
spec('RF13', 'Thin-size domination and all actual signature gaps',
     'Prove both thin-size inequalities with cw=9/10 and every signature-gap clause from the actual HCVal columns, using scalar cloud spacing ceil(x^cD), cD,ch>=430 and the source gapS expression.',
     ['RF11', 'RF12'],
     many(GP+'SzRowThinSizeGe.lean', ['szRow_thinSize_ge'], 'GlobalTheory.EX', 'complete_parameter_family')
     + many(GP+'SzRowSigGaps.lean', ['rankVal_crude', 'gap_crude', 'base_sizes_ge', 'szRow_sig_gaps'], 'GlobalTheory.EX', 'complete_parameter_family_with_stronger_RF12_bounds')
     + many(DP+'PairRowIffQdRows.lean', ['Std', 'HCVal', 'h0v', 'Delv', 'Val'], 'GlobalTheory.EX', 'literal_input_and_definitions')
     + many(LC+'DataParams.lean', ['gapS'], 'Formalism.BasicNotions.LevelStarExponents', 'literal_definition')
     + basic('DataParams₂', 'SizeData₂', role='actual_top_bottom_and_window_inputs'),
     'derived_simplification'),
spec('RF14', 'Complete band/lambda/prime supplier and two parameter families',
     'Expand the rounded orbit count to prove N1<=BN log x, derive exact lambda and rhoB/rhoP bounds, prove auxiliary-prime and supplied-level-prime scales, ChTT and the lower ChCode count, and splitBound>=11. This completes the top/band/bottom and type-prime-scale parameter families; it chooses no new primes.',
     ['RF11', 'RF12'],
     many(GP+'GoodTopCountLeConstMulLog.lean', ['goodTopCount_le_const_mul_log', 'topCount_and_lambda_bounds'], 'GlobalTheory', 'rounded_count_and_lambda_proofs')
     + many(GB+'UnramifiedQuadraticSetting.lean', ['goodU', 'goodEll', 'orbitSmallMultiplicity', "goodG'", 'orbitWindowCount'], 'Formalism.MainNotions.G', 'literal_count_definitions')
     + growth('hG', 'KG', 'rG', 'N1', 'Nstar', 'La', 'rhoB')
     + many(GP+'BandWidthLeInvSqOfRankBounds.lean', ['bandWidth_le_inv_sq_of_rank_bounds', 'szRow_band_lambda_primes'], 'GlobalTheory.EX', 'full_source_supplier_reproved')
     + many(GP+'SzRowTopsBandBottomsStatement.lean', ['_root_.GlobalTheory.T.sizes_card_TT_le_Nstar_and_rhoP_le_and_bT_le'], role='complete_parameter_family')
     + many(GP+'SzRowTypePrimesStatement.lean', ['_root_.GlobalTheory.T.sizes_exists_Y_bounds_host_g_mem_Icc_Y_two_mul_Y'], role='complete_parameter_family')
     + many(GP+'SzRowElevenLeSplitBound.lean', ['szRow_eleven_le_splitBound'], 'GlobalTheory.EX', 'one_completed_SizesAt_clause')
     + many(DP+'PairRowIffQdRows.lean', ['PairWin', 'PairRow', 'HostConst', 'HostVal', 'Val'], 'GlobalTheory.EX', 'literal_input_definitions')
     + many(LC+'DataParams.lean', ['Nstar', 'condE', 'rhoP'], 'Formalism.BasicNotions.LevelStarExponents', 'literal_definition')
     + many('src/Formalism/SharpRestriction/GlobalSchurBounds/Chosen.lean', ['GamL', 'ChTT_at', 'ChCode_at'], 'Formalism.MainNotions', 'literal_definition'),
     'derived_simplification'),
spec('RF15', 'Every field of the actual ParamsT constructor',
     'For every supplied compatible ParameterChoice P, the exact TO/nW/nP/PP/Dp/s construction satisfies every ParamsT field. The critical order exponent is 371.768<377; cloud thresholds cD>=800 and height threshold ch>=1000 suffice after fixed constants and exponential comparisons. Consequently the remaining full NumAt supply is precisely compatible ParameterChoice plus SizesAt for the same D,L.',
     ['RF11', 'RF12', 'RF14'],
     many(GP+'SzRowNodeGapBlockLength.lean', ['nodeGap_blockLength_poly', 'szRow_nodeGap_blockLength', 'szRow_blockLengthParams'], 'GlobalTheory.EX', 'full_block_constructor_reproved')
     + many(LC+'DataParamsT.lean', ['zBase', 'ParamsT'], 'Formalism.BasicNotions', 'all_literal_fields_checked')
     + many(LC+'DataParams.lean', ['nW', 'h0'], 'Formalism.BasicNotions.LevelStarExponents', 'literal_definition')
     + many(LC+'DataParams.lean', ["ParameterChoice'"], 'Formalism.BasicNotions', 'retained_input_type')
     + many(DP+'PairRowIffQdRows.lean', ['Std', 'TOv', 'nWv', 'Delv', 'h0v', 'HostVal', 'HCVal', 'Val'], 'GlobalTheory.EX', 'actual_definitions_and_inputs')
     + many('src/Formalism/SharpRestriction/InertJacobiLevels/AsmIface.lean', ['FC.Fixed', 'NumAt'], 'Formalism.MainNotions.Inhab', 'exact_constants_and_conditional_output_type')
     + many(GP+'SzRowNumAt.lean', ['szRow_numAt'], 'GlobalTheory.EX', 'conditional_consumer_with_ParameterChoice_and_SizesAt_retained')
     + many('src/Formalism/SharpRestriction/ElevenLe.lean', ['SizesAt'], 'Formalism.MainNotions', 'retained_input_definition'),
     'derived_simplification'),
spec('RF16', 'The literal exponential word count is bounded by 2^(k-3)',
     'Keep GamL=exp(CGam*m^5*f*x^epsilon) and the exact ceiling formula. The rank windows give the positive gap 21epsilon/16 between m^5*f*x^epsilon and k, yielding log(card Word)<=k/4<=(k-3)log 2 and hence the literal natural upper bound with uniform SzRow thresholds.',
     ['RF11', 'RF12'],
     many(GP+'SzRowCardWordsLe.lean', ['words_real_bound', 'szRow_card_words_le'], 'GlobalTheory.EX', 'full_parameter_family_reproved_with_explicit_rank_gap')
     + many(DP+'PairRowIffQdRows.lean', ['Std', 'RankVal', 'Val', 'SzRow'], 'GlobalTheory.EX', 'exact_constant_rank_count_and_quantifier_inputs')
     + many('src/Formalism/SharpRestriction/GlobalSchurBounds/Chosen.lean', ['GamL'], 'Formalism.MainNotions', 'actual_exponential_definition'),
     'derived_simplification'),
]

claim_paths = {s['path'] for c in claims for s in c['sources']}


def target(path, name, ns, role, scope):
    s = source(path, name, ns, 'remaining_input')
    s.update(role=role, remaining_human_scope=scope,
             human_status='continuation_target_only; no additional theorem claimed')
    return s


targets = [
target(ST, 'chGood_of_host', 'GlobalTheory.EX.OB', 'Compatible actual host-column constructor',
       'Expand exists_hc_family and its exact HCVal/interlacing/parity/code construction; retain the same host and distinguished translate and uniform thresholds. RF10 only consumes this supplier.'),
target(GP+'ExistsLevChOfLevelPrime.lean', 'exists_levCh_of_levelPrime', 'GlobalTheory.EX.OB',
       'Actual level-prime record from the analytic LevelPrime input',
       'Prove the full norm/congruence element and type-window construction with the same du/Dstar and Gam, including exclusion of both pde primes; RF10 retains this constructor.'),
target(GP+'ExistsExplicitParameters.lean', 'exists_sizeData_explicit', 'GlobalTheory.EX',
       'Initial size datum before the now-proved refill',
       'Reconstruct the HC window, cloud and depth estimates and the explicit initial SizeData/Val fields. The old zero support and zero gains are placeholders replaced by RF5, not the final refill.'),
target(GP+'ExistsParametersOver.lean', 'exists_sizeData_over', 'GlobalTheory.EX.OB',
       'Same-host and code transport of the initial-size constructor',
       'Combine the preceding initial size theorem with Over and preserve every host/Frobenius/code identity, including positivity of Del in bit recovery; RF10 retains the substantive supplier.'),
target('src/Development/AbelianVarietyTheory/Proofs/IwasawaDecomposition/ExistsLayeredDataOfGoodScaleContexts.lean',
       'recExP_of_recAtG', 'GlobalTheory.Fc', 'Recursive geometric construction with the correct order of levels and lattice choices',
       'Supply actual RecAtG/FromCoreAt, the mass-ratio/window-lower inputs and du/Dstar identities, then the universal level and LedPart clauses. RF does not derive these geometric data from refill.'),
target(GP+'NormPrimesAndLevelPrimeUnconditional.lean', 'levelPrime_unconditional', 'GlobalTheory.EX',
       'Uniform analytic type-prime supplier',
       'Reconstruct the underlying norm-prime theorem and all interval/congruence dependences at the required scale. RF9 only proves the elementary scale comparison.'),
target(GP+'ExplicitConstantsParameterConditionsLarge.lean', 'explicitConstants_parameterConditions_large', 'GlobalTheory.EX',
       'Stronger actual parameter record',
       'RF12-RF14 and RF16 prove seven of the twenty-one families: rank-k, rank lower, top/band/bottom, thin-size, signature gaps, type-prime scale and the upper word count. Prove the fourteen residual families listed below and then the exact compatible constant record; conjunction assembly alone does not supply them.'),
target(GP+'SzRowNumAt.lean', 'szRow_numAt', 'GlobalTheory.EX',
       'Full NumAt, top-density and word-code numerical supplier',
       'RF15 proves full ParamsT for every compatible P and RF14 proves full band/lambda/prime/ChTT/ChCode. Remaining inputs are a complete compatible ParameterChoice and SizesAt for the same D,L; the numerical data do not supply the geometric model.'),
target(GP+'SzRowElevenLeSplitBound.lean', 'szRow_sizesAt', 'GlobalTheory.EX',
       'Complete independent SizesAt numerical conjunction',
       'Check all 23 named Size* conjunctions with their exact fields and uniform thresholds. RF14 separately proves splitBound>=11, and other RF bounds give ingredients, but the full SizesAt package is retained.'),
]

# The exact fourteen uncompleted families from the 21-family parameter supplier.
numerical_residuals = [
 (1, 'SzRowPrimesConductorStatement', '_root_.GlobalTheory.T.sizes_host_degree_and_log_q_and_conductor_bounds', '',
  'The full q/d growth, log q lower, dlog, conductor/t and auxiliary-prime logarithm family; RF14 already proves some ingredients but not this whole tuple.'),
 (4, 'LogfSqLeRS', 'szRow_logf', 'GlobalTheory.EX',
  'All log f, squared-log, loglog b and nW lower parameter conditions.'),
 (5, 'SzRowEtaBoundsStatement', '_root_.GlobalTheory.T.sizes_etaSz_le_b_div_and_log_etaSz_le_and_t_le', '',
  'Every eta-size bound, preserving dependence on cD and ch.'),
 (6, 'SzRowEtaLeWStatement', '_root_.GlobalTheory.T.sizes_m_mul_Sc_add_etaSz_le_w_mul_L_and_bounds', '',
  'All four coupled eta, cloud, thin-weight and de2 inequalities.'),
 (8, 'SzRowCloudLe', 'szRow_cloud_le', 'GlobalTheory.EX',
  'The three cloud/Delta/logarithm bounds with the actual supplied spacing.'),
 (9, 'SzRowWindowLength', 'szRow_windowLength', 'GlobalTheory.EX',
  'The integer j witness, word length and log-five depth bounds with fixed CLw and Cj0.'),
 (10, 'SzRowExact', 'szRow_exact', 'GlobalTheory.EX',
  'The complete HC identities, parity, etaF, pde congruence/distinctness and ideal-norm tuple.'),
 (11, 'HalfLeAbsNodeSubMid', 'szRow_lowsFar', 'GlobalTheory.EX',
  'All quantitative low-node to midpoint separation bounds.'),
 (12, 'ExplicitChoiceRowWeightRatioAndLastCloudLeTwiceFStatement', '_root_.GlobalTheory.T.explicitChoice_rowWeight_ratio_and_lastCloud_le_twice_first', '',
  'Every actual cross-weight ratio and final-to-first bottom comparison.'),
 (14, 'SzRowCloudUnitLowerStatement', '_root_.GlobalTheory.T.sizes_del_ge_cloudUnit_and_count_bounds', '',
  'All cloud-unit, rank and count lower bounds on the scalar spacing.'),
 (15, 'SzRowNodeGapStatement', '_root_.GlobalTheory.T.sizes_node_bounds_le_h0', '',
  'All ten specified node-height bounds, including lStar, real powers and rank products.'),
 (16, 'SzRowGapFunFNStatement', '_root_.GlobalTheory.T.sizes_t_add_cube_le_h0_and_f_mul_N_pow_le_h0', '',
  'The further cubic and degree-power height bounds.'),
 (18, 'RbSNumeric', 'szRow_rbS', 'GlobalTheory.EX',
  'The actual rank-bottom-cloud bound with lA and de2.'),
 (19, 'SzRowLStarStatement', '_root_.GlobalTheory.T.sizes_b_add_Sc_add_etaSz_add_div_lt_lStar', '',
  'Both strict lStar comparison inequalities for the actual sizes.')
]
for number, filename, name, namespace, scope in numerical_residuals:
    t = target(GP+filename+'.lean', name, namespace,
               f'Residual ParameterChoice supplier family {number}/21', scope)
    t['parameter_family_number'] = number
    targets.append(t)

numerical_frontier = dict(
    parameter_choice=dict(total_families=21, completed_families=[2, 3, 7, 13, 17, 20, 21],
                          completed_by=['RF12', 'RF13', 'RF14', 'RF16'],
                          retained_families=[t[0] for t in numerical_residuals],
                          complete_package='retained'),
    paramsT=dict(status='proved_uniformly_for_every_supplied_compatible_ParameterChoice', claim='RF15',
                 order_exponent='377', critical_upper_exponent='371.768',
                 cD_lower='800', ch_lower='1000', height_upper_exponents=['757', '882', '117', '891']),
    band_lambda_primes=dict(status='proved', claim='RF14'),
    sizesAt=dict(status='retained_as_complete_package', separately_proved_clause='splitBound>=11 by RF14'),
    numAt=dict(status='conditional_join', remaining_packages=['compatible complete ParameterChoice for the same D,L',
                                                           'complete SizesAt for the same D,L'],
               no_simultaneous_geometric_supply_inferred=True))


def file_record(path):
    raw = cache[path]
    return dict(path=path, sha256=sha(raw), bytes=len(raw), lines=len(raw.splitlines()),
                url=f'{URL}/blob/{COMMIT}/{path}', verified_equal_to_pinned_git_blob=True)


boundaries = [
    'Canonical refill requires the supplied D7/SizeData, HostArith, finite twist support, positive DGam and untwisted Fval condition; it proves no new gain/error estimate.',
    'RF7 proves the full exists_ledPart implication under the actual supplied Lay/RecOK/LedOK geometric and local conditions, preserving Mram, the type-prime exception and lenLoc.toNat/e_w.',
    'RF8 installs I_u*N_u and the prescribed height while transporting supplied structures; it does not construct the metric, theta, comparison or cohomological inputs stored in Lay.',
    'RF10 retains RecExP, LevelPrime and the named compatible host-column, level and initial-size constructor inputs. All threshold quantifiers are preserved.',
    'The drop set is generally infinite; common finite support is proved only for gain, forcing, error and the two deficit fields.',
    'RF11-RF16 prove seven complete ParameterChoice supplier families, full ParamsT for every compatible P, the full band/lambda/prime supplier and splitBound>=11. Full ParameterChoice and SizesAt remain the exact two inputs to the conditional NumAt join.',
    'The scalar cloud spacing Delta_cl is not the integral Weyl operator Delta or the dual operator nabla. The four independent global branches remain unchanged.'
]
payload = dict(schema='rh-component-provenance-v1', artifact_version='0.14',
               repository=URL, commit=COMMIT, claims=claims,
               source_files=[file_record(p) for p in sorted(claim_paths)],
               input_boundaries=boundaries,
               numerical_frontier=numerical_frontier,
               validation=dict(claims=len(claims), source_links=sum(len(c['sources']) for c in claims),
                               source_files=len(claim_paths), pinned_bytes_verified=True,
                               exact_inclusive_ranges=True, lean_build=False, source_files_modified=False))
next_data = dict(artifact_version='0.14', repository=URL, commit=COMMIT,
                 status='Exact remaining suppliers after RF; targets are not theorem proofs.',
                 targets=targets,
                 numerical_frontier=numerical_frontier,
                 source_files=[file_record(p) for p in sorted({s['path'] for s in targets})],
                 validation=dict(target_count=len(targets), pinned_bytes_verified=True))
(ROOT/'provenance.json').write_text(json.dumps(payload, ensure_ascii=False, indent=2)+'\n')
(ROOT/'next_targets.json').write_text(json.dumps(next_data, ensure_ascii=False, indent=2)+'\n')
(ROOT/'source_locators.txt').write_text('\n\n'.join(
    f"{c['id']} {s['declaration']} [{s['role']}]\n{s['path']}:{s['line_start']}-{s['line_end']}\n{s['url']}\nfull_sha256={s['sha256']}\nrange_sha256={s['range_sha256']}"
    for c in claims for s in c['sources'])+'\n')
print(json.dumps(payload['validation']))
print(json.dumps(next_data['validation']))
