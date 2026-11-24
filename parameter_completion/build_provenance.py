#!/usr/bin/env python3
"""Rebuild PN ledgers from exact pinned Git blobs; never modify the checkout."""
from pathlib import Path
import argparse
import hashlib
import json
import re
import subprocess

ROOT = Path(__file__).resolve().parent
parser = argparse.ArgumentParser()
parser.add_argument('--repo', type=Path, default=ROOT.parents[1] / 'lean-source')
args = parser.parse_args()
REPO = args.repo.resolve()
COMMIT = '7cbf7a0c32fca1badf05931879a37c3f8a2b03b4'
URL = 'https://github.com/CocoSgt/riemann-hypothesis-lean'
GP = 'src/Development/AbelianVarietyTheory/Proofs/GlobalInterpolation/'
DP = 'src/Development/AbelianVarietyTheory/Definitions/GlobalTwisting/'
LC = 'src/Formalism/LocalRingCardinality/'
SR = 'src/Formalism/SharpRestriction/'
WC = 'src/Development/AutomorphicArithmetic/WeightCongruences/'
PAIR = DP + 'PairRowIffQdRows.lean'
IFACE = SR + 'InertJacobiLevels/AsmIface.lean'
PARAMS = LC + 'DataParams.lean'
SIZEDATA = LC + 'DataParams₂.lean'
cache = {}


def sha(data):
    return hashlib.sha256(data).hexdigest()


def blob(path):
    if path not in cache:
        data = subprocess.check_output(
            ['git', '-C', str(REPO), 'show', f'{COMMIT}:{path}'])
        local = REPO / path
        if local.is_file():
            assert local.read_bytes() == data, ('changed source checkout', path)
        cache[path] = data
    return cache[path]


def source(path, spelling, namespace='', role='source theorem or definition'):
    raw = blob(path)
    lines = raw.splitlines(keepends=True)
    text = [s.decode('utf-8').rstrip('\r\n') for s in lines]
    pattern = re.compile(
        r'^(?:@\[[^\n]*?\]\s*)?(?:(?:private|protected|noncomputable)\s+)?'
        r'(?:theorem|lemma|def|abbrev|structure)\s+'
        + re.escape(spelling) + r'(?=\s|\{|\(|:)')
    starts = [i for i, line in enumerate(text) if pattern.search(line)]
    assert len(starts) == 1, (path, spelling, starts)
    a = starts[0]
    b = a + 1
    boundary = re.compile(
        r'^(?:(?:private|protected|noncomputable)\s+)?'
        r'(?:theorem|lemma|def|abbrev|structure|instance|variable|namespace|end|open|section|set_option)\b|^@\[')
    while b < len(lines) and not boundary.match(text[b]):
        b += 1
    while b > a + 1 and not text[b - 1].strip():
        b -= 1
    selected = b''.join(lines[a:b])
    declaration = namespace + '.' + spelling if namespace else spelling
    declaration = declaration.removeprefix('_root_.')
    return dict(
        path=path, declaration=declaration, source_spelling=spelling,
        line_start=a + 1, line_end=b, full_file_sha256=sha(raw), sha256=sha(raw),
        range_sha256=sha(selected), range_bytes=len(selected),
        first_line=text[a], declaration_lines_within_range=[a + 1],
        url=f'{URL}/blob/{COMMIT}/{path}#L{a+1}-L{b}',
        pinned_url=f'{URL}/blob/{COMMIT}/{path}#L{a+1}-L{b}',
        role=role, verified_equal_to_pinned_git_blob=True)


def many(path, names, namespace='', role='source theorem or definition'):
    return [source(path, n, namespace, role) for n in names]


def gp(file, *names):
    return many(GP + file + '.lean', names, 'GlobalTheory.EX')


def definitions(path, names, namespace='Formalism.BasicNotions'):
    return many(path, names, namespace, 'literal definition or supplied record interface')


family_specs = {
    1: ('SzRowPrimesConductorStatement', '_root_.GlobalTheory.T.sizes_host_degree_and_log_q_and_conductor_bounds', ''),
    2: ('ExplicitChoiceRankKLowerUpperBounds', 'explicitChoice_rankK_lower_upper_bounds', 'GlobalTheory.EX'),
    3: ('RankRowsOfCrudeBounds', 'szRow_rank_lower_bounds', 'GlobalTheory.EX'),
    4: ('LogfSqLeRS', 'szRow_logf', 'GlobalTheory.EX'),
    5: ('SzRowEtaBoundsStatement', '_root_.GlobalTheory.T.sizes_etaSz_le_b_div_and_log_etaSz_le_and_t_le', ''),
    6: ('SzRowEtaLeWStatement', '_root_.GlobalTheory.T.sizes_m_mul_Sc_add_etaSz_le_w_mul_L_and_bounds', ''),
    7: ('SzRowTopsBandBottomsStatement', '_root_.GlobalTheory.T.sizes_card_TT_le_Nstar_and_rhoP_le_and_bT_le', ''),
    8: ('SzRowCloudLe', 'szRow_cloud_le', 'GlobalTheory.EX'),
    9: ('SzRowWindowLength', 'szRow_windowLength', 'GlobalTheory.EX'),
    10: ('SzRowExact', 'szRow_exact', 'GlobalTheory.EX'),
    11: ('HalfLeAbsNodeSubMid', 'szRow_lowsFar', 'GlobalTheory.EX'),
    12: ('ExplicitChoiceRowWeightRatioAndLastCloudLeTwiceFStatement', '_root_.GlobalTheory.T.explicitChoice_rowWeight_ratio_and_lastCloud_le_twice_first', ''),
    13: ('SzRowThinSizeGe', 'szRow_thinSize_ge', 'GlobalTheory.EX'),
    14: ('SzRowCloudUnitLowerStatement', '_root_.GlobalTheory.T.sizes_del_ge_cloudUnit_and_count_bounds', ''),
    15: ('SzRowNodeGapStatement', '_root_.GlobalTheory.T.sizes_node_bounds_le_h0', ''),
    16: ('SzRowGapFunFNStatement', '_root_.GlobalTheory.T.sizes_t_add_cube_le_h0_and_f_mul_N_pow_le_h0', ''),
    17: ('SzRowSigGaps', 'szRow_sig_gaps', 'GlobalTheory.EX'),
    18: ('RbSNumeric', 'szRow_rbS', 'GlobalTheory.EX'),
    19: ('SzRowLStarStatement', '_root_.GlobalTheory.T.sizes_b_add_Sc_add_etaSz_add_div_lt_lStar', ''),
    20: ('SzRowCardWordsLe', 'szRow_card_words_le', 'GlobalTheory.EX'),
    21: ('SzRowTypePrimesStatement', '_root_.GlobalTheory.T.sizes_exists_Y_bounds_host_g_mem_Icc_Y_two_mul_Y', ''),
}
family_claim = {
    1: 'PN2', 2: 'RF12', 3: 'RF12', 4: 'PN3', 5: 'PN4', 6: 'PN5',
    7: 'RF14', 8: 'PN6', 9: 'PN7', 10: 'PN8', 11: 'PN9', 12: 'PN10',
    13: 'RF13', 14: 'PN11', 15: 'PN12', 16: 'PN13', 17: 'RF13',
    18: 'PN14', 19: 'PN15', 20: 'RF16', 21: 'RF14',
}
family_fields = {
    1: ['qd_pow', 'logq_ge', 'logDerivative_le_power', 'condE_le', 'pde_log'],
    2: ['k_low', 'k_up', 'radius_ge_sqrt_ratio'],
    3: ['k_ge_m2L', 'k_ge_mx', 'klogk', 'flogk'],
    4: ['logf_le', 'log_sq_conductor_le', 'loglogb', 'nW_ge'],
    5: ['eta_le', 'logeta', 't_le_eta', 'teta', 'mteta'],
    6: ['mSeta', 'Neta', 'eta2', 'kS_le'],
    7: ['TT_card_le', 'rho_le', 'bT_le'],
    8: ['S_le', 'Del_le', 'logDel'],
    9: ['Lw_j', 'Lw_le', 'jetIndex_le_log'],
    10: ['topPlace_first_bound', 'cloud_place_bound', 'uk_extreme', 'em_win',
         'nodes_gap', 'e_centred', 'e_mu', 'etaF_eq', 'pde_mod', 'pde_ne',
         'ccK_log', 'ccK_le'],
    11: ['lows_far'], 12: ["X''_ratio", 'bm_le'], 13: ["w''_ge"],
    14: ['Del_ge', 'Del_count'], 15: ['h0_ge'],
    16: ['heightBound_ge_rank_cubic', 'heightBound_ge_degree_power'],
    17: ['sig_gaps'], 18: ['rbS'], 19: ['lstar1', 'lstar2'],
    20: ['words_le'], 21: ['g_Y'],
}
families = {}
for number, (file, spelling, namespace) in family_specs.items():
    families[number] = source(GP + file + '.lean', spelling, namespace,
                              'literal complete ParameterChoice supplier family')


def family(number):
    return [families[number]]


claims = []
COMMON = [
    'The same actual D7 and SizeData₂ D satisfy Val C cD ch L; epsilon is in (0,1/52) and C is standard.',
    'Thresholds have the literal SzRow order and precede D,L; J is allowed to vary but HostConst bounds it by the fixed Cpde.',
    'RF11, RF12 and RF14 are reused only for their proved comparison, rank and band estimates under the same supplied data.',
    'Host/column/initial-size existence is not inferred from numerical inequalities; the initial SizeData weight windows and HCVal character data are supplied.',
]


def claim(cid, title, statement, deps, sources, extra=()):
    unique = []
    seen = set()
    for s in sources:
        key = (s['path'], s['declaration'], s['line_start'], s['line_end'])
        if key not in seen:
            seen.add(key)
            unique.append(s)
    claims.append(dict(
        id=cid, title=title, statement=statement, depends_on=list(deps),
        status='derived_simplification',
        mathematical_status='proved_under_explicit_hypotheses',
        introduced_in='0.15',
        proof_location=dict(file='parameter_completion/main.tex',
                            expanded='parameter_completion/report.txt', section=cid),
        assumptions=COMMON + list(extra), sources=unique))


claim('PN1', 'Common literal scales and uniform numerical hypotheses',
      'The source SzRow quantifier order, rank/scale identities and the uniform polynomial envelope are made explicit, including actual lStar=m*b/Astar, lA, d2 and the ceiling bounds.',
      ['RF11', 'RF12', 'RF14'],
      definitions(PAIR, ['Std', 'RankVal', 'HostVal', 'HostArith', 'HCVal', 'Val', 'SzRow'], 'GlobalTheory.EX')
      + definitions(SIZEDATA, ['Scale', 'wj', 'SizeData₂'])
      + definitions(SIZEDATA, ['ez', 'L', 'b', 'a', "X'", "b'", "w''", "X''", 'delta1'], 'Formalism.BasicNotions.Scale')
      + definitions(LC+'Params.lean', ['Ranks'])
      + definitions(LC+'Params.lean', ['n', 'f', 'r', 'N', 'rS'], 'Formalism.BasicNotions.Ranks')
      + definitions(PARAMS, ['condE', 'lA', 'lStar', 'h0', 'qSig', 'Mrt', 'nW'], 'Formalism.BasicNotions.LevelStarExponents')
      + gp('SzRowAndImp', 'SzRow.and', 'SzRow.imp'))

claim('PN2', 'Both host-prime lower bounds and the exact conductor-product tuple',
      'Family1 is proved from PairWin/PairRow and J<=Cpde: q,d exceed x^(2Ct+5), log q>=x^(ez/6), (QSqd)^36*t^150<=sqrt(b), and both auxiliary-prime logs are <=Lpow; Val.dlog is copied explicitly.',
      ['PN1'], family(1)
      + gp('SzRowPrimesConductor', 'szRow_primes_conductor')
      + gp('HostBoundsTwoMulRpowLogSqLe', 'hostBounds_log_of_sqrt_exp_lt', 'hostBounds_ez', 'hostBounds_win')
      + definitions(PAIR, ['PairWin', 'PairRow', 'HostConst'], 'GlobalTheory.EX')
      + definitions(SR+'GlobalSchurBounds/GeneralLinearActions/FiltrationCocycleLiftCriterion.lean', ['X1', 'X2'], 'GlobalTheoryTheory'))

claim('PN3', 'Four logarithmic and block-window bounds',
      'Family4 is proved: log f<=sqrt(rS), (log f)^2<=m^2*Lpow, loglog b<=cLL*r*f*log r, and (4f+10)r<=nW(L,10), preserving the actual fixed constant cLL.',
      ['PN1'], family(4)+gp('LogfSqLeRS', 'logf_sq_le_rS')
      + definitions(PARAMS, ['nW'], 'Formalism.BasicNotions.LevelStarExponents')
      + definitions(LC+'Params.lean', ['rS'], 'Formalism.BasicNotions.Ranks'))

claim('PN4', 'Five complete eta scale inequalities',
      'Family5 is proved with eta<=x^(ch+3), ch>=401 and the explicit exponent ch+1224, including both relative w bounds and the literal logarithmic bound.',
      ['PN1'], family(5)+gp('SzRowEtaBounds', 'szRow_eta_bounds'))

claim('PN5', 'Four coupled eta and cloud inequalities',
      'Family6 is proved with Q=x^(cD+ch+402), S,eta<=Q^3, d2*Q>=1 and w>=Q^10; all four literal product inequalities follow.',
      ['PN1'], family(6)+gp('SzRowEtaLeW', 'eta_rows_of_pow_bounds', 'szRow_eta_le_w'))

claim('PN6', 'Complete cloud upper-bound family',
      'Family8 is proved with 4S<=lambda*bprime/k, 4CDelG*k^2*Delta_cl<=lambda*bprime and log Delta_cl<=x^(epsilon/4)/2, with its exact half factor.',
      ['PN1'], family(8))

claim('PN7', 'Integer window witnesses and exact logarithmic depth',
      'Family9 is proved with the actual witness j=ceil(7log x), every l>=11, the literal Lw ceiling formula and j0=ceil(log_5(nN/m)), giving the fixed constants CLw=4455 and Cj0=405.',
      ['PN1'], family(9)+gp('SzRowWindowLength', 'lA_le_pow_seven', 'nN_div_m_le'))

claim('PN8', 'All twelve exact column and arithmetic assertions',
      'Family10 follows from the supplied actual HC identities, with zero centering error and exact node gaps; MUQ is converted to the literal numerator root-of-unity character condition, and prime/ideal fields are copied from their precise supplied interfaces.',
      ['PN1'], family(10)
      + definitions(PAIR, ['HCVal', 'Val', 'HostVal'], 'GlobalTheory.EX')
      + definitions(LC+'DataHost.lean', ['Host'])
      + definitions(LC+'DataHost.lean', ['MuCond'], 'Formalism.BasicNotions.Host')
      + definitions(WC+'ProdNegOneZpow.lean', ['MU', 'MUQ'], 'UpperTheory')
      + many(WC+'IffNum.lean', ['num'], 'UpperTheory.MUQ'),
      ['The full HCVal.MUQ premise is retained; its parity consequence alone would not supply e_mu.'])

claim('PN9', 'Quantitative separation of every node from every midpoint',
      'Family11 is proved for cD>=402 and ch>=7cD by bounding the denominator polynomial by 12Q^6 and using the exact half-integer grid separation |b_i-e_j|>=H/2.',
      ['PN1'], family(11)+gp('HalfLeAbsNodeSubMid', 'lowsFar_poly', 'half_le_abs_node_sub_mid'))

claim('PN10', 'Every cross-weight ratio and final-bottom bound',
      'Family12 is proved by placing all actual weight windows inside [w,2b], using Xpp*w=xb, and using HCVal to show b_last<=2b_first. The supplied initial SizeData windows remain explicit.',
      ['PN1'], family(12)
      + gp('ExplicitChoiceRowWeightRatioAndLastCloudLeTwiceF', "rpow_mul_X'_le_b", 'szRow_size_ratio')
      + definitions(SIZEDATA, ['wj', 'SizeData₂'])
      + definitions(LC+'DataHost.lean', ['topPlaces', 'thickPlaces', 'IsThin'], 'Formalism.BasicNotions.Host'))

claim('PN11', 'All five cloud-unit and counting lower bounds',
      'Family14 is proved using cD>=5c+Fc+406K+412; the exact five exponent bounds are 5c+6+Fc,404,5c+24,412,406K, preserving etaF=6x^-CF and all real exponents.',
      ['PN1'], family(14)+gp('SzRowCloudUnitLower', 'cloudUnit_poly_bounds', 'szRow_cloudUnit_lower'))

claim('PN12', 'Ten node-height bounds with a variable-coefficient strengthening',
      'Family15 is proved for ch>=max(1300+cD,406CCount), including stronger 12Astar+2t+8<=h0 and the literal 12b/lStar=12Astar/m. The two coefficient rows hold uniformly for arbitrary Ar,Ak in [0,x], allowing x^(epsilon/100) in SizeNodes.',
      ['PN1'], family(15)+gp('SzRowNodeGap', 'nodeGap_poly', 'szRow_nodeGap')
      + definitions(PARAMS, ['lStar', 'h0', 'qSig', 'Mrt'], 'Formalism.BasicNotions.LevelStarExponents')
      + definitions(SR+'ElevenLe.lean', ['szlStar', 'SizeNodes'], 'Formalism.MainNotions'))

claim('PN13', 'The two additional cubic-rank and degree-power height bounds',
      'Family16 is proved with the literal rank expression t+2(k+m(t+r+7))^3+1<=x^1210 and f*N^Ch0N<=x^(3+402Ch0N); these are separate from the four ParamsT height fields.',
      ['PN1'], family(16)+gp('SzRowGapFunFN', 'gap_cube_bound', 'szRow_gap_fun_fN'))

claim('PN14', 'The complete rank-bottom-cloud product inequality',
      'Family18 is proved by bprime,S<=b/x^14 and r*log(x)*lA<=x^13, giving rbS<=2b/x<=d2*m*b with exact normalizations.',
      ['PN1'], family(18)+gp('RbSNumeric', 'rbS_numeric')
      + definitions(SR+'ElevenLe.lean', ['szlA', 'SizeEta'], 'Formalism.MainNotions'))

claim('PN15', 'Both strict lower-scale inequalities',
      'Family19 is proved using Q=x^(cD+ch+402), P=Q^7, Astar,S,eta,t<=P, P^2<=bprime and bprime*P^2<=b; lStar>=100bprime preserves both strict inequalities.',
      ['PN1'], family(19)+gp('SzRowLStar', 'lstar_ineqs_of_le', 'lstar_den_le', 'szRow_lStar')
      + definitions(SR+'ElevenLe.lean', ['szlStar', 'SizeLstar'], 'Formalism.MainNotions'))

claim('PN16', 'All 111 fields of the actual compatible ParameterChoice record',
      'All21 families hold at one correctly ordered uniform threshold. Copying23 constants, proving23 positivity fields, assigning61 family fields and the four exact HostArith fields constructs P for the same D,L with parConsts P=C.PK and P.CnW=C.P.CnW.',
      [f'PN{i}' for i in range(2, 16)]+['RF12', 'RF13', 'RF14', 'RF16'],
      gp('ExplicitConstantsParameterConditionsLarge', 'Std.parConsts_pos', 'explicitConstants_parameterConditions_large')
      + definitions(PARAMS, ["ParameterChoice'"])
      + definitions(PAIR, ['Std', 'HostArith', 'Val', 'SzRow'], 'GlobalTheory.EX')
      + definitions(IFACE, ['PC', 'PC.list', 'FC.PK', 'FC.cMid', 'FC.cLast', 'FC.Fixed'], 'Formalism.MainNotions.Inhab')
      + definitions(SR+'ParConsts.lean', ['parConsts'], 'Formalism.MainNotions')
      + [families[i] for i in range(1, 22)],
      ['HostArith for the same supplied host is an explicit premise only at the final record join.'])

# Exhaustively verify the constant and assertion fields of the actual record.
param_source = source(PARAMS, "ParameterChoice'", 'Formalism.BasicNotions')
param_raw = b''.join(blob(PARAMS).splitlines(keepends=True)[
    param_source['line_start']-1:param_source['line_end']]).decode('utf-8')
fields = re.findall(r"^  ([A-Za-z0-9_']+)\s*:", param_raw, re.M)
assert len(fields) == len(set(fields)) == 111, len(fields)
constants = ['CkLow', 'Ck6', 'CfL', 'cLL', 'CnW', 'Crho', 'CDelG', 'CLw',
             'Cj0', 'Cw', 'cw', 'CDel', 'CCount', 'Ch0r', 'Ch0k', 'Ch0N',
             'Cgap', 'CetaF', 'CY', 'CYL', 'Cpde', 'CccK', 'CF']
assert len(constants) == 23
field_map = {}
for name in constants:
    field_map[name] = dict(role='copied real constant', claim='PN16', from_expression='C.P.'+name)
    field_map[name+'_pos'] = dict(role='positivity from Std', claim='PN16')
numerical_names = [f for i in range(1,22) for f in family_fields[i]]
assert len(numerical_names) == len(set(numerical_names)) == 61
for i in range(1,22):
    for f in family_fields[i]:
        assert f not in field_map
        field_map[f] = dict(role='proved supplier field', claim=family_claim[i], supplier_family=i,
                            source_declaration=families[i]['declaration'])
for name in ['g_norm', 'g_mod', 'pde_split', 'level_split']:
    assert name not in field_map
    field_map[name] = dict(role='explicit same-host HostArith premise', claim='PN16',
                           source_declaration='GlobalTheory.EX.HostArith')
assert set(field_map) == set(fields), (set(fields)-set(field_map), set(field_map)-set(fields))

# Check the exact constant order, including CF in the last position.
pc_source = source(IFACE, 'PC.list', 'Formalism.MainNotions.Inhab')
pc_text = b''.join(blob(IFACE).splitlines(keepends=True)[pc_source['line_start']-1:pc_source['line_end']]).decode()
assert re.findall(r'P\.([A-Za-z0-9_]+)', pc_text) == constants
parc_source = source(SR+'ParConsts.lean', 'parConsts', 'Formalism.MainNotions')
parc_text = b''.join(blob(parc_source['path']).splitlines(keepends=True)[parc_source['line_start']-1:parc_source['line_end']]).decode()
assert re.findall(r'P\.([A-Za-z0-9_]+)', parc_text) == constants

# Check the source constructor's literal order of all21 supplier families.
aggregate = source(GP+'ExplicitConstantsParameterConditionsLarge.lean',
                   'explicitConstants_parameterConditions_large', 'GlobalTheory.EX')
aggregate_text = b''.join(blob(aggregate['path']).splitlines(keepends=True)[aggregate['line_start']-1:aggregate['line_end']]).decode()
join_text = aggregate_text.split('refine SzRow.imp (',1)[1].split(') ?_',1)[0]
source_order = re.findall(r'GlobalTheory\.[A-Za-z0-9_.]+', join_text)
assert source_order == [families[i]['declaration'] for i in range(1,22)]
new_families = [i for i in range(1,22) if family_claim[i].startswith('PN')]
reused_families = [i for i in range(1,22) if family_claim[i].startswith('RF')]
assert new_families == [1,4,5,6,8,9,10,11,12,14,15,16,18,19]
assert reused_families == [2,3,7,13,17,20,21]

retained = [
    source(SIZEDATA, 'SizeData₂', 'Formalism.BasicNotions', 'actual supplied initial size record; separate SZ construction'),
    source(PAIR, 'Val', 'GlobalTheory.EX', 'supplied RankVal/HostVal/HCVal and exact scalar identities'),
    source(PAIR, 'HostArith', 'GlobalTheory.EX', 'explicit norm/congruence/splitting premise at PN16'),
    source(PAIR, 'Std', 'GlobalTheory.EX', 'fixed compatible constant hypothesis'),
]


def file_record(path):
    data = blob(path)
    return dict(path=path, sha256=sha(data), bytes=len(data), lines=len(data.splitlines()),
                commit=COMMIT, url=f'{URL}/blob/{COMMIT}/{path}',
                verified_equal_to_pinned_git_blob=True)


all_claim_sources = [s for c in claims for s in c['sources']]
claim_paths = sorted({s['path'] for s in all_claim_sources})
family_table = [dict(number=i, proved_by=family_claim[i], fields=family_fields[i],
                     newly_proved_in_0_15=i in new_families, source=families[i])
                for i in range(1,22)]
frontier = dict(
    parameter_choice=dict(total_families=21, completed_families=list(range(1,22)),
                          newly_completed_families=new_families, reused_rf_families=reused_families,
                          retained_families=[], full_package='proved_by_PN16_under_Val_and_HostArith'),
    record_fields=dict(total=111, copied_constants=23, positivity_fields=23,
                       family_assertion_fields=61, explicit_HostArith_fields=4),
    paramsT='RF15 already proved; applies to the actual P supplied by PN16',
    sizesAt_numAt='separate SZ component; no independent claim made by PN',
    initial_size_construction='separate SZ component; PN requires the actual same D,L',
    host_and_column_existence='retained primitive construction boundary',
)
proof_hashes = {fn:sha((ROOT/fn).read_bytes()) for fn in ['main.tex','report.txt']}
payload = dict(
    schema='readable-rh-claim-provenance', artifact_version='0.15',
    repository=URL, commit=COMMIT,
    scope='Complete actual ParameterChoice from supplied same-data Val and HostArith; all14 residual families proved, all21 families accounted for. No host, column or initial-size existence inferred.',
    claims=claims, source_files=[file_record(p) for p in claim_paths],
    input_boundaries=[
        'Every claim is conditional on the actual supplied D7 and SizeData₂ D, with Std C and Val C cD ch L in the literal SzRow quantifier order.',
        'HostArith is required explicitly at PN16 for g_norm, g_mod, pde_split and level_split.',
        'The full HCVal.MUQ character relation, host prime conditions and existing three SizeData windows remain explicit; no parity-only substitute or circular initial-size construction is used.',
        'condE means the literal product QS*q*d; Val.dlog is supplied, not established analytically here.',
        'lStar=szlStar=m*b/Astar; PN12 separately proves the stronger numerator bound 12Astar+2t+8<=h0.',
        'Variable coefficients x^(epsilon/100) are permitted in PN12 by its uniform [0,x] coefficient version. Other SizesAt strengthenings belong to SZ.',
        'No residual ParameterChoice family remains. Host/CM/column existence and the four independent global branches are not inferred from numerical completion.',
        'Scalar Delta_cl, integral Weyl Delta and dual nabla remain distinct.',
    ],
    numerical_frontier=frontier, parameter_family_table=family_table,
    parameter_record_field_map=[dict(field=f, **field_map[f]) for f in fields],
    retained_input_interfaces=retained, proof_file_sha256=proof_hashes,
    validation=dict(claims=len(claims),source_links=len(all_claim_sources),source_files=len(claim_paths),
                    exact_inclusive_ranges=True,pinned_bytes_verified=True,
                    record_fields_checked=len(fields),source_family_order_checked=True,
                    constant_list_order_checked=True,lean_build=False,pdf_compiled=False,
                    source_files_modified=False))
completed_targets = []
for i in new_families:
    s = dict(families[i])
    s.update(completed_by=family_claim[i], supplier_family=i,
             human_status='proved_under_explicit_hypotheses', remaining_human_scope='none within the literal supplier family')
    completed_targets.append(s)
s=dict(aggregate)
s.update(completed_by='PN16',human_status='proved_under_Val_and_HostArith',remaining_human_scope='none within the literal compatible ParameterChoice constructor')
completed_targets.append(s)
next_data=dict(
    artifact_version='0.15',repository=URL,commit=COMMIT,
    status='all residual ParameterChoice families and their actual record constructor are complete under the stated supplied inputs',
    targets=[],completed_targets=completed_targets,retained_input_interfaces=retained,
    numerical_frontier=frontier,
    cross_component_scope='SZ owns initial SizeData, SizesAt and NumAt joins. Primitive host/column/analytic suppliers remain in the shared frontier; PN adds no duplicate target.',
    source_files=[file_record(p) for p in sorted({s['path'] for s in completed_targets+retained})],
    validation=dict(target_count=0,completed_target_count=len(completed_targets),
                    retained_parameter_family_count=0,pinned_bytes_verified=True))

for name,data in [('provenance.json',payload),('next_targets.json',next_data)]:
    (ROOT/name).write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n')
(ROOT/'source_locators.txt').write_text('\n\n'.join(
    f"{c['id']} {s['declaration']} [{s['role']}]\n"
    f"{s['path']}:{s['line_start']}-{s['line_end']}\n{s['url']}\n"
    f"full_sha256={s['full_file_sha256']}\nrange_sha256={s['range_sha256']}"
    for c in claims for s in c['sources'])+'\n')
print(json.dumps(payload['validation']))
print(json.dumps(next_data['validation']))
