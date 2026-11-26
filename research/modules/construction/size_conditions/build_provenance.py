#!/usr/bin/env python3
"""Build SZ's exact source ledger from pinned Git objects; never build Lean."""
from pathlib import Path
import argparse
import hashlib
import json
import re
import subprocess

ROOT = Path(__file__).resolve().parent
parser = argparse.ArgumentParser()
parser.add_argument('--repo', type=Path, default=ROOT.parents[1] / 'lean-source')
REPO = parser.parse_args().repo.resolve()
COMMIT = '7cbf7a0c32fca1badf05931879a37c3f8a2b03b4'
URL = 'https://github.com/CocoSgt/riemann-hypothesis-lean'
GP = 'src/Development/AbelianVarietyTheory/Proofs/GlobalInterpolation/'
DP = 'src/Development/AbelianVarietyTheory/Definitions/GlobalTwisting/'
LC = 'src/Formalism/LocalRingCardinality/'
EL = 'src/Formalism/SharpRestriction/ElevenLe.lean'
AI = 'src/Formalism/SharpRestriction/InertJacobiLevels/AsmIface.lean'
PV = DP + 'PairRowIffQdRows.lean'
ST = DP + 'SetUnipotentTranslate.lean'
cache = {}


def sha(b):
    return hashlib.sha256(b).hexdigest()


def blob(path):
    if path not in cache:
        raw = subprocess.check_output(['git', '-C', str(REPO), 'show', f'{COMMIT}:{path}'])
        if (REPO / path).is_file():
            assert (REPO / path).read_bytes() == raw, path
        cache[path] = raw
    return cache[path]


def source(path, name, ns='', role='proof'):
    raw = blob(path)
    lines = raw.splitlines(keepends=True)
    txt = [l.decode().rstrip('\r\n') for l in lines]
    pattern = re.compile(r'^(?:@\[[^\n]*?\]\s*)?(?:(?:private|protected|noncomputable)\s+)?'
                         r'(?:theorem|lemma|def|abbrev|structure)\s+' + re.escape(name)
                         + r'(?=\s|\{|\(|:)')
    starts = [i for i, line in enumerate(txt) if pattern.search(line)]
    assert len(starts) == 1, (path, name, starts)
    lo = starts[0]
    hi = lo + 1
    boundary = re.compile(r'^(?:(?:private|protected|noncomputable)\s+)?'
                          r'(?:theorem|lemma|def|abbrev|structure|instance|variable|namespace|end|open|section|set_option)\b|^@\[')
    while hi < len(lines) and not boundary.match(txt[hi]):
        hi += 1
    while hi > lo + 1 and not txt[hi - 1].strip():
        hi -= 1
    selected = b''.join(lines[lo:hi])
    qualified = ((ns + '.') if ns else '') + name
    qualified = qualified.removeprefix('_root_.')
    url = f'{URL}/blob/{COMMIT}/{path}#L{lo+1}-L{hi}'
    return dict(path=path, declaration=qualified, source_spelling=name,
                line_start=lo+1, line_end=hi, sha256=sha(raw), full_file_sha256=sha(raw),
                range_sha256=sha(selected), range_bytes=len(selected),
                url=url, pinned_url=url, first_line=txt[lo], declaration_lines_within_range=[lo+1],
                role=role, verified_equal_to_pinned_git_blob=True)


def many(path, names, ns='', role='proof'):
    return [source(path, n, ns, role) for n in names]


def gp(file, *names):
    return many(GP+file+'.lean', names, 'GlobalTheory.EX', 'source_conclusion_reproved')


def defs(*names):
    return many(PV, names, 'GlobalTheory.EX', 'literal_input_or_quantifier_definition')


def sizes(*names):
    return many(EL, names, 'Formalism.MainNotions', 'literal_output_definition')


def scale(*names):
    return many(LC+'DataParams₂.lean', names, 'Formalism.BasicNotions.Scale', 'literal_definition')


def claim(ident, title, statement, deps, sources):
    return dict(id=ident, title=title, statement=statement, depends_on=deps,
                status='derived_simplification', mathematical_status='proved_under_explicit_hypotheses',
                introduced_in='0.15',
                proof_location=dict(file='size_conditions/main.tex', expanded='size_conditions/report.txt', section=ident),
                assumptions=[
                    'The literal rank, scale, host, column, Val and HostArith hypotheses are retained exactly where stated.',
                    'Uniform thresholds follow SzRow: epsilon,C then cD then ch then x0, before D,L and varying J.',
                    'SZ10-SZ11 construct the initial size record without assuming PN16, NumAt or an existing SizeData₂.',
                    'The actual ChOK, Over and RecOK data are inputs of SZ12; their geometric existence is not inferred.',
                    'Cyclotomic degree, finite multiplicative subgroup cyclicity and elementary real analysis are declared mathematical background.',
                    'No Lean build or kernel replay was performed.'
                ], sources=sources)


claims = [
claim('SZ1', 'All seven basic size clauses',
      'The literal RankVal and HostVal windows prove SizeN, SizeM, SizeK, SizeT, SizeTT, SizeDe2 and SizeLw uniformly, retaining the ceiling terms and the exact density identity.',
      ['RF11', 'RF12'],
      gp('SzRowRankSizes', 'szRow_rankSizes')
      + defs('Std', 'RankVal', 'HostVal', 'Lwv', 'Val', 'SzRow')
      + sizes('szTh', 'szNst', 'SizeN', 'SizeM', 'SizeK', 'SizeT', 'SizeTT', 'SizeDe2', 'SizeLw')
      + many(LC+'DataParams₂.lean', ['SizeData₂'], 'Formalism.BasicNotions', 'literal_supplied_size_fields')),
claim('SZ2', 'All fourteen coupled rank inequalities',
      'A sharp rational exponent table and the literal rS=m/2-1, f=2n and rankBudget=n*x^-epsilon prove every SizeKRel clause, using SZ3 for log root-discriminant <= L.',
      ['RF11', 'RF12', 'SZ3'],
      gp('SzRowSizeKRel', 'sizeKRel_of_rankVal', 'szRow_sizeKRel')
      + sizes('SizeKRel') + defs('RankVal')
      + many(LC+'Params.lean', ['Ranks'], 'Formalism.BasicNotions', 'rank_hypotheses')
      + many(LC+'Params.lean', ['n', 'f', 'r', 'rS'], 'Formalism.BasicNotions.Ranks', 'literal_definition')
      + many(LC+'DataArith.lean', ['rankBudget'], 'Formalism.BasicNotions', 'literal_definition')),
claim('SZ3', 'Complete conductor, prime and root-discriminant size clauses',
      'The supplied PairRow and bounded J give all eight SizeQD clauses, both auxiliary-prime logarithms and Q^36*t^150<=sqrt(b). The host-derived rd bounds are explicitly supplied by the actual Host; no prime or host is chosen.',
      ['RF11', 'RF12'],
      gp('HostBoundsTwoMulRpowLogSqLe', 'hostBounds_two_mul_rpow_log_sq_le', 'hostBounds_log_of_sqrt_exp_lt',
         'hostBounds_rd', 'hostBounds_ez', 'hostBounds_one_le_log_div', 'hostBounds_win', 'hostBounds')
      + gp('SzRowCondQdPde', 'szRow_cond_qd_pde')
      + defs('PairWin', 'PairRow', 'HostConst', 'HostVal', 'Val')
      + sizes('szCond', 'SizeCond', 'SizeQD', 'SizePde')
      + many(LC+'RankBoundMonotoneInDimension.lean', ['factRd'], 'Formalism.BasicNotions', 'actual_host_projection')
      + many(LC+'DataHost.lean', ['rdE'], 'Formalism.BasicNotions.Host', 'literal_definition')),
claim('SZ4', 'The exact lambda, rho and bottom size inequalities',
      'RF14 orbit-count control gives SizeLa; a separate exponent calculation handles the variable x^theta coefficient in SizeRho, and the literal Val bottom field gives SizeBot.',
      ['RF11', 'RF12', 'RF14'],
      gp('SzRowLaRhoBot', 'szRow_la_rho_bot') + sizes('SizeLa', 'SizeRho', 'SizeBot')
      + defs('Val')
      + many(GP+'GoodTopCountLeConstMulLog.lean', ['goodTopCount_le_const_mul_log', 'topCount_and_lambda_bounds'],
             'GlobalTheory', 'already_reconstructed_RF14_supplier')),
claim('SZ5', 'Every eta, node and strict-star size inequality',
      'The exact PN4/PN5/PN14 mapping supplies all nine SizeEta clauses; PN12 supplies all seven SizeNodes clauses including variable x^theta coefficients and the m divisor in lStar; PN15 supplies both strict SizeLstar clauses.',
      ['PN4', 'PN5', 'PN12', 'PN14', 'PN15'],
      gp('ExplicitChoiceSizeEta', 'szRow_sizeEta')
      + gp('ExplicitChoiceSizeNodes', 'szRow_sizeNodes')
      + gp('ExplicitChoiceSizeLstar', 'szRow_sizeLstar')
      + sizes('szlA', 'szlStar', 'SizeEta', 'SizeNodes', 'SizeLstar')),
claim('SZ6', 'All eight scalar spacing conditions',
      'cD>=412, exact ceiling bounds and exponential comparison give all eight SizeDel inequalities, with actual S=4kDelta and Host.v=rdE/2.',
      ['RF11', 'RF12', 'SZ3', 'SZ4'],
      gp('SzRowSizeDel', 'szRow_sizeDel') + sizes('SizeDel')
      + defs('Delv', 'Val')
      + many(LC+'DataHost.lean', ['v'], 'Formalism.BasicNotions.Host', 'literal_definition')),
claim('SZ7', 'Actual uniform weight envelopes, prime scales and word bounds',
      'The three supplied SizeData weight windows give wpp<=w_j<=2b, all cross-weight ratios and b_(m-1)<=2b_0. Host intervals supply all SizeG clauses, RF16 supplies SizeWords and RF14 the final splitting bound.',
      ['RF11', 'RF12', 'RF14', 'RF16', 'SZ4'],
      gp('SzRowSizeWSizeBmSizeXpp', 'window_scale_bounds', 'place_top_or_thick_or_thin', 'szRow_sizeW_sizeBm_sizeXpp')
      + gp('SzRowSizeGSizeWords', 'log_le_of_le_two_mul_pow_eight', 'szRow_sizeG', 'szRow_sizeG_sizeWords')
      + gp('SzRowElevenLeSplitBound', 'szRow_eleven_le_splitBound')
      + sizes('SizeW', 'SizeBm', 'SizeXpp', 'SizeG', 'SizeWords')
      + defs('HCVal', 'HostVal', 'Val') + scale('b', 'a', "b'", "w''", "X''")
      + many(LC+'DataParams₂.lean', ['wj', 'SizeData₂'], 'Formalism.BasicNotions', 'actual_weight_windows_and_definition')),
claim('SZ8', 'Complete literal SizesAt with the correct threshold order',
      'Assemble every one of the23 named Size* clauses and splitBound>=11 for the same D,L by nested finite maxima; SizeTu is separately defined and is not a conjunct of this output.',
      ['SZ1', 'SZ2', 'SZ3', 'SZ4', 'SZ5', 'SZ6', 'SZ7'],
      gp('SzRowElevenLeSplitBound', 'szRow_sizesAt') + sizes('SizesAt', 'SizeTu')
      + defs('SzRow') + gp('SzRowAndImp', 'SzRow.and')),
claim('SZ9', 'The full actual NumAt and density/code conjunction',
      'PN16 supplies the compatible ParameterChoice for the actual D,L; RF15 supplies ParamsT for that same P; SZ8 and RF14 supply all remaining fields. All21 NumAt fields and ChTT/ChCode are obtained under HostArith, with no numerical package retained.',
      ['PN16', 'RF14', 'RF15', 'SZ8'],
      gp('SzRowNumAt', 'szRow_numAt')
      + many(AI, ['NumAt', 'bTopOf', 'FC.Fixed'], 'Formalism.MainNotions.Inhab', 'literal_record_and_constants')
      + defs('Std', 'Val', 'HostArith', 'Lwv', 'HCVal')
      + many('src/Formalism/SharpRestriction/GlobalSchurBounds/Chosen.lean', ['ChTT_at', 'ChCode_at'],
             'Formalism.MainNotions', 'literal_output_definition')),
claim('SZ10', 'Torsion bound and all thirteen initial size windows',
      'The elementary inequality phi(a)^2>=a/2 gives torsionOrder(E)<=8f². With RankVal/HostVal/HCVal and bprime<=bT<=2bprime, the explicit arithmetic progressions prove all13 initial window/depth/density clauses without an existing size record.',
      ['RF11', 'RF12'],
      many('src/Formalism/LocalToGlobal/SiegelLatticeTheory/CokernelGLCounts/RankPointCounts/TorsionTotientBound.lean',
           ['le_mul_totient_sq', 'le_two_totient_sq', 'torsionOrder_le'],
           'Formalism.L2.SG.NGCut.TorsionTotientBound', 'cyclotomic_bound_reproved')
      + many('src/Development/AutomorphicArithmetic/CyclotomicBounds/RootsOfUnity/HostTorsionOrderLe.lean',
             ['host_torsionOrder_le'], 'UpperTheory.Mu', 'actual_host_degree_application')
      + gp('WindowsOfExplicitParameters', 'windows_scale_facts', 'ten_ceil_logb_le_Lwv',
           'torsionOrder_le_half_gap', 'windows_of_large_scale')
      + many(GP+'ParametersWindowsOfExplicitParametersStatement.lean',
             ['_root_.GlobalTheory.T.windows_of_explicitParameters'], role='literal_thirteen_clause_endpoint')
      + defs('h0v', 'Delv', 'Lwv', 'RankVal', 'HostVal', 'HCVal')
      + many(LC+'DataHost.lean', ['Host'], 'Formalism.BasicNotions', 'actual_second_set_range')
      + many(LC+'DataParams₂.lean', ['wj'], 'Formalism.BasicNotions', 'literal_weight_definition')),
claim('SZ11', 'Construct every field of the initial actual size datum',
      'An independent lambda/rank calculation permits SZ10. Install the initial zero-support/gain/error/lattice fields and exact scale/degree/cloud/depth/density fields; interlacing supplies middle cloud bounds. Every SizeData₂ and Val field follows from the literal supplied inputs.',
      ['RF11', 'RF12', 'RF14', 'SZ10'],
      gp('ExistsExplicitParameters', 'bottom_window_le', 'middle_between', 'exists_sizeData_explicit')
      + many(LC+'DataParams₂.lean', ['SizeData₂', 'dlogL'], 'Formalism.BasicNotions', 'complete_record_and_actual_derivative')
      + many(LC+'Params.lean', ['HCParam'], 'Formalism.BasicNotions', 'literal_interlacing_fields')
      + defs('Val', 'Std', 'HostVal')
      + many(GP+'GoodTopCountLeConstMulLog.lean', ['topCount_and_lambda_bounds'], 'GlobalTheory',
             'RF14_supplier_independent_of_initial_size_record')),
claim('SZ12', 'Exact initial-size transport through the actual Over construction',
      'Under supplied ChOK/Over/RecOK and Gam equality, SZ11 produces HostArith and the initial L with exact WtEq and Val; all rank/host/Frobenius labels and level-set containment are preserved, and positivity of Delta recovers every bit under the actual word equivalence.',
      ['SZ11'],
      many(GP+'ExistsParametersOver.lean', ['exists_sizeData_over'], 'GlobalTheory.EX.OB', 'full_source_conclusion_reconstructed')
      + many(ST, ['ChOK', 'Over', 'Over.host_heq', 'Over.field', 'RecOK', 'WtEq', 'GamS'],
             'GlobalTheory.EX.OB', 'literal_retained_input_and_transport_definitions')
      + defs('HostArith', 'Val')),
claim('SZ13', 'Construct the actual ranks over any prescribed frame and in the cyclic case',
      'For x>=16, even ceiling choices of k,m and the explicit t=(8f-1)r+4+8TOvW satisfy every Ranks field and literal RankVal while preserving the supplied frame. Least-power-of-two selection and the explicit j->[5^j] quotient isomorphism also give the exact cyclicFrame corollary, without constructing a number-field host.',
      [],
      gp('ExistsRanksRankValFrame', 'exists_even_between', 'exists_two_pow_between',
         'exists_ranks_of_frame', 'exists_ranks_rankVal_frame', 'exists_ranks_cyclic_frame')
      + defs('RankVal', 'TOv', 'nWv')
      + many(LC+'Params.lean', ['Ranks'], 'Formalism.BasicNotions', 'every_rank_field_checked')
      + many(LC+'Params.lean', ['n', 'f', 'r', 'N'], 'Formalism.BasicNotions.Ranks', 'literal_definition')
      + many('src/Formalism/SharpRestriction/RamificationFrobenius/TotientGaloisClasses/FrameCyclicGenerator.lean',
             ['cycIso', 'cycIso_one', 'cycHom', 'cycHom_bijective', 'idxZMod', 'frameCyc', 'cyclicFrame'],
             'Formalism.HC', 'actual_cyclic_frame_construction')
      + many('src/Formalism/SharpRestriction/RamificationFrobenius/TotientGaloisClasses/FrameCyclicGenerator.lean',
             ['ofEquiv'], 'Formalism.HC.Frame', 'transport_of_frame_axioms')
      + many('src/Formalism/FrobeniusOrbits/Statement.lean', ['HGrp'], 'Formalism.FrobeniusOrbits', 'literal_cyclic_quotient')
      + many('src/Formalism/FrobeniusOrbits/FrobeniusOrbitsProofs/CoprimeTwoPow.lean',
             ['hostGroup'], 'Formalism.FrobeniusOrbits', 'cyclic_quotient_reproved_in_restricted_scope')),
]


def file_rec(path):
    raw = blob(path)
    return dict(path=path, sha256=sha(raw), bytes=len(raw), lines=len(raw.splitlines()),
                url=f'{URL}/blob/{COMMIT}/{path}', verified_equal_to_pinned_git_blob=True)


paths = {s['path'] for c in claims for s in c['sources']}


def record_fields(path, name, ns):
    s = source(path, name, ns, 'literal_record_for_exhaustive_field_map')
    raw = b''.join(blob(path).splitlines(keepends=True)[s['line_start']-1:s['line_end']]).decode()
    names = re.findall(r'^  (\w+)\s*:', raw, re.M)
    assert len(names) == len(set(names)), name
    return names


size_fields = record_fields(LC+'DataParams₂.lean', 'SizeData₂', 'Formalism.BasicNotions')
num_fields = record_fields(AI, 'NumAt', 'Formalism.MainNotions.Inhab')
val_fields = record_fields(PV, 'Val', 'GlobalTheory.EX')
rank_fields = record_fields(LC+'Params.lean', 'Ranks', 'Formalism.BasicNotions')
assert len(size_fields) == 63 and len(num_fields) == 21 and len(val_fields) == 15 and len(rank_fields) == 13
size_map = {}
for names, supplier in [
    (['sc','aT','aT_win','bT','bT_ge','top_u'], 'SZ11: supplied scale, degree windows and top endpoints'),
    (['top_b','b_le','weightLength_ge_depth','win_thick','win_top','win_thin','cloud_gap','cloud_v','be_close','t_win'],
     'SZ10: the complete thirteen-window theorem, with Std Cc=2 and Ct=401'),
    (['supp','gain','F','E','tau','io','gain_supp','F_supp','E_supp','tau_supp','io_supp','gain_g',
      'not_inert','drop','drop_alt','F_conj','F_above','NuLat','lenMN'], 'SZ11: explicit empty sets, zero functions and bottom lattice'),
    (['untwisted'], 'SZ11: supplied untwisted Aj=0 and chosen F=0'),
    (['j0','logFiveDepth_le'], 'SZ11: exact natural log-five ceiling and its lower inequality'),
    (['logDerivativeAtOne','logDerivative_at_one_eq'], 'SZ11: actual dlogL D 1, definitionally the supplied host logarithmic derivative'),
    (['split_tie'], 'SZ11: literal HostVal split_tie'),
    (['o_tie','QS_tie'], 'SZ11: HostConst and Cpde<=x^theta'),
    (['de2','thickDensity_pos','thickDensity_le_one','typeDensity_eq_card_div'], 'SZ10-SZ11: 0<card(T2)<=n and exact quotient'),
    (['LaG','Sc','etaSz','Sc_pos','Sc_eq','Cc','etaSz_pos','Ct','CGam','CGam_pos'], 'SZ11: explicit formulas, supplied spacing equality and Std positivity'),
    (['cloud_u'], 'SZ11: actual word-column interlacing between the common adjacent v entries'),
    (['TTw','TTw_full'], 'SZ11: the full finite top set at every place'),
    (['Gam_eq'], 'SZ11: supplied exact logarithmic Gamma equality'),
    (['wPart','wPart_ge'], 'SZ11: constant one'),
]:
    for name in names:
        assert name not in size_map, name
        size_map[name] = supplier
assert set(size_map) == set(size_fields)
num_map = {}
for names, supplier in [
    (['params','params_K','CnW_eq'], 'PN16: same-data compatible ParameterChoice'),
    (['parT','parT_K','eP_eq'], 'RF15 applied to that same ParameterChoice'),
    (['sizes'], 'SZ8'),
    (['rho_le','LaG_ge','g_le','pde_lt'], 'RF14'),
    (['CGam_eq','Cc_eq','Ct_eq','secondConstant_eq','bT_le','logFiveDepth_eq','win'], 'literal Val fields on the same D,L'),
    (['ccK_top'], 'literal HostVal'),
    (['Lw_eq'], 'HostVal Lwv and Std Ct=401'),
    (['cloud1'], 'HCVal common v-column formula'),
]:
    for name in names:
        assert name not in num_map, name
        num_map[name] = supplier
assert set(num_map) == set(num_fields)
size_clause_map = {
    'SZ1':['SizeN','SizeM','SizeK','SizeT','SizeTT','SizeDe2','SizeLw'],
    'SZ2':['SizeKRel'], 'SZ3':['SizeCond','SizeQD','SizePde'],
    'SZ4':['SizeLa','SizeRho','SizeBot'], 'SZ5':['SizeEta','SizeNodes','SizeLstar'],
    'SZ6':['SizeDel'], 'SZ7':['SizeW','SizeBm','SizeXpp','SizeG','SizeWords']}
size_output = source(EL, 'SizesAt', 'Formalism.MainNotions')
size_raw = b''.join(blob(EL).splitlines(keepends=True)[size_output['line_start']-1:size_output['line_end']]).decode()
size_clauses = re.findall(r'\b(Size[A-Za-z0-9]+) L\b', size_raw)
assert len(size_clauses) == 23 and set(size_clauses) == {s for a in size_clause_map.values() for s in a}
record_audit = dict(
    method='Names and fields extracted from the exact pinned declaration ranges; proof suppliers are recorded separately. A coverage check is not itself a proof.',
    sizeData2=[dict(field=f, supplier=size_map[f]) for f in size_fields],
    numAt=[dict(field=f, supplier=num_map[f]) for f in num_fields],
    val=[dict(field=f, supplier='SZ11: literal supplied input or stated constructor equality') for f in val_fields],
    ranks=[dict(field=f, supplier='SZ13: explicit ceiling/t construction, preserving supplied frame') for f in rank_fields],
    sizesAt=[dict(clause=s, supplier=next(k for k,a in size_clause_map.items() if s in a)) for s in size_clauses],
    sizesAt_additional_clause=dict(clause='11 <= D.host.splitBound', supplier='RF14, reused in SZ7'),
    counts=dict(sizeData2=63, numAt=21, val=15, ranks=13, sizesAt_named_clauses=23))
boundaries = [
    'SizesAt and full NumAt are proved uniformly for the same supplied actual datum; arithmetic host existence and the Val/HostArith inputs are not produced by their numerical estimates.',
    'SZ10-SZ11 independently construct the initial SizeData₂ from their literal rank/host/HC/degree and untwisted inputs; no cycle through ParameterChoice, SizesAt or NumAt is used.',
    'SZ12 discharges RF10 initial-size constructor supplier, with ChOK, Over, RecOK and the same Gam equality still supplied. The host-column and level constructors are separate until their own reconstruction is supplied.',
    'The initial zero numerical fields are legal constructor choices, not final gain/forcing/error estimates. RF supplies the subsequent canonical refill and preserves Val.',
    'Actual geometric RecExP/Lay/RecOK/LedOK, arithmetic host and analytic LevelPrime existence and the four independent global branches retain their stated boundaries.',
    'SZ13 constructs the rank record over a supplied frame in its order window, and its exact cyclic-frame corollary. It supplies no host field, prime selection, or geometric model.',
]
numerical_frontier = dict(
    parameter_choice=dict(status='complete_under_Val_and_HostArith', supplied_by='PN16', families=21),
    paramsT=dict(status='complete_for_the_same_parameter_record', supplied_by='RF15', fields=54),
    sizesAt=dict(status='complete_uniformly', supplied_by='SZ8', named_size_clauses=23, additional_split_bound=True),
    numAt=dict(status='complete_under_Val_and_HostArith', supplied_by='SZ9', fields=21,
               additional_conclusions=['ChTT_at', 'ChCode_at(L,3,C.P.CF)']),
    initial_size=dict(status='constructed_under_literal_input_hypotheses', supplied_by=['SZ10','SZ11','SZ12'],
                      independent_of_numAt=True, window_clauses=13))
payload = dict(schema='rh-component-provenance-v1', artifact_version='0.15', repository=URL, commit=COMMIT,
               claims=claims, source_files=[file_rec(p) for p in sorted(paths)], input_boundaries=boundaries,
               numerical_frontier=numerical_frontier,
               record_field_audit=record_audit,
               validation=dict(claims=len(claims), source_links=sum(len(c['sources']) for c in claims),
                               source_files=len(paths), pinned_bytes_verified=True, exact_inclusive_ranges=True,
                               lean_build=False, source_files_modified=False))
targets = []
for path, name, ns, scope in [
    (ST, 'chGood_of_host', 'GlobalTheory.EX.OB', 'The actual compatible host-column constructor; SZ12 consumes its ChOK output. A separate AC reconstruction may discharge this target.'),
    (GP+'ExistsLevChOfLevelPrime.lean', 'exists_levCh_of_levelPrime', 'GlobalTheory.EX.OB', 'Actual level record with the given duStar/Dstar/Gam, norm/congruence elements and exclusions; analytic LevelPrime remains distinct.'),
    (GP+'NormPrimesAndLevelPrimeUnconditional.lean', 'levelPrime_unconditional', 'GlobalTheory.EX', 'The analytic uniform type-prime supplier, not supplied by any size estimate.'),
    ('src/Development/AbelianVarietyTheory/Proofs/IwasawaDecomposition/ExistsLayeredDataOfGoodScaleContexts.lean',
     'recExP_of_recAtG', 'GlobalTheory.Fc', 'Actual recursive geometric data, mass/window estimates and the complete Lay/RecOK/LedOK construction. Numerical and initial-size closure does not supply it.')
]:
    t = source(path, name, ns, 'remaining_input')
    t.update(remaining_human_scope=scope, human_status='continuation_target_only; no additional theorem claimed')
    targets.append(t)

(ROOT/'provenance.json').write_text(json.dumps(payload, ensure_ascii=False, indent=2)+'\n')
(ROOT/'source_manifest.json').write_text(json.dumps(payload['source_files'], ensure_ascii=False, indent=2)+'\n')
(ROOT/'record_field_audit.json').write_text(json.dumps(record_audit, ensure_ascii=False, indent=2)+'\n')
(ROOT/'next_targets.json').write_text(json.dumps(dict(artifact_version='0.15', repository=URL, commit=COMMIT,
    status='The complete numerical and initial-size packages are proved under their literal inputs; these are distinct upstream suppliers.',
    targets=targets, numerical_frontier=numerical_frontier,
    source_files=[file_rec(p) for p in sorted({s['path'] for s in targets})]), ensure_ascii=False, indent=2)+'\n')
(ROOT/'source_locators.txt').write_text('\n\n'.join(
    f"{c['id']} {s['declaration']} [{s['role']}]\n{s['path']}:{s['line_start']}-{s['line_end']}\n{s['url']}\nfull_sha256={s['sha256']}\nrange_sha256={s['range_sha256']}"
    for c in claims for s in c['sources'])+'\n')
print(json.dumps(payload['validation']))
