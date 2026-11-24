"""Rebuild the SD source ledger from byte-identical pinned Lean source files."""
from pathlib import Path
import hashlib
import json
import re
import subprocess

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[1] / 'alpoge-rh'
PIN = '7cbf7a0c32fca1badf05931879a37c3f8a2b03b4'
URL = 'https://github.com/CocoSgt/riemann-hypothesis-lean'
GB = 'src/Formalism/SharpRestriction/GrowthBounds/'
SD = GB + 'SegmentDegree/'
PATHS = {
    'statement': GB + 'ValuationLowestDegreeRename.lean',
    'main': GB + 'SegmentDegree.lean',
    'data': SD + 'NonemptyDvrSettingOfStandard.lean',
    'sel': SD + 'SelIsComplRestrictSupport.lean',
    'coarse': SD + 'Coarse.lean',
    'sat': SD + 'LamSatRestrict.lean',
    'prod': SD + 'LamProdMonomial.lean',
    'img': SD + 'LamImgApply.lean',
    'lam': SD + 'RestLamOfRests.lean',
    'degree': SD + 'StrictMonoIntExists.lean',
    'distinct': SD + 'LateVectorsDistinctTops.lean',
    'det': SD + 'DiscriminantNonzeroOfInjectiveTops.lean',
    'gen': SD + 'DiscriminantNonzeroModUniformiser.lean',
    'genred': SD + 'DiscriminantNeZeroOfResidueNeZero.lean',
    'res': SD + 'DminusLeBeS.lean',
    'tau': SD + 'TauDegreeOnPathBound.lean',
    'loss': SD + 'SumTotalLoss.lean',
    'sum': SD + 'FrameZeroStrictMono.lean',
    'count': SD + 'RestCountOf.lean',
    'good': SD + 'GoodPathWeight.lean',
    'beta': SD + 'BetaRatioBound.lean',
    'pad': SD + 'DivMulSubLeDivSubDiv.lean',
    'digits': 'src/Formalism/ThetaLogCoordinates/ResidueClassEstimates/VandermondeRankEstimates/LDigits.lean',
}
PREFIX = r'(?:@\[[^\n]*\]\s*)?(?:(?:private|protected|noncomputable)\s+)*'
DECL = re.compile(r'^' + PREFIX + r'(?:def|abbrev|theorem|lemma|structure|class|instance)\s+(\S+)')
BOUND = re.compile(r'^' + PREFIX + r'(?:def|abbrev|theorem|lemma|structure|class|instance|namespace|section|end|variable|open|include|omit|attribute)\b')
files = {}
for key, path in PATHS.items():
    raw = (REPO / path).read_bytes()
    expected = subprocess.check_output(['git', '-C', str(REPO), 'show', f'{PIN}:{path}'])
    assert raw == expected, ('uncommitted source bytes', path)
    lines = raw.splitlines(keepends=True)
    stack = []
    decls = []
    for i, bline in enumerate(lines):
        line = bline.decode().rstrip('\r\n')
        if m := re.match(r'^namespace\s+(\S+)', line):
            stack.append(('namespace', m[1]))
        elif m := re.match(r'^(?:noncomputable\s+)?section(?:\s+(\S+))?\s*$', line):
            stack.append(('section', m[1]))
        elif m := re.match(r'^end(?:\s+(\S+))?\s*$', line):
            assert stack, (path, i + 1, 'end without namespace/section')
            kind, label = stack.pop()
            assert not m[1] or m[1] == label, (path, i + 1, label, m[1])
        elif m := DECL.match(line):
            ns = '.'.join(label for kind, label in stack if kind == 'namespace')
            decls.append((m[1], i, ns + '.' + m[1] if ns else m[1]))
    files[key] = {'path': path, 'sha256': hashlib.sha256(raw).hexdigest(), 'bytes': len(raw),
                  'lines': len(lines), '_lines': lines, '_decls': decls,
                  'verified_equal_to_pinned_git_blob': True}


def refs(key, names, role='parallel_source_proof'):
    item = files[key]
    output = []
    for name in names.split():
        hits = [d for d in item['_decls'] if d[0] == name]
        assert len(hits) == 1, (key, name, hits)
        _, start, qualified = hits[0]
        end = start + 1
        while end < item['lines'] and not BOUND.match(item['_lines'][end].decode()):
            end += 1
        while end > start + 1 and not item['_lines'][end - 1].strip():
            end -= 1
        raw = b''.join(item['_lines'][start:end])
        output.append({'path': item['path'], 'declaration': qualified, 'source_spelling': name,
                       'line_start': start + 1, 'line_end': end,
                       'full_file_sha256': item['sha256'], 'range_sha256': hashlib.sha256(raw).hexdigest(),
                       'role': role, 'url': f'{URL}/blob/{PIN}/{item["path"]}#L{start+1}-L{end}'})
    return output


claims = [
    {'id': 'SD1', 'title': 'Actual-generator direct summand by an invertible coefficient minor',
     'status': 'proved_shorter_alternative_to_source',
     'statement': 'For a finite monomial support and any generating set G over a DVR, select a residue-field basis from reduced G. A unit coefficient minor gives a retraction onto the lifts, an actual-generator basis and a direct summand of rank exactly dim(span of reduced G). This proves RestSel, without estimating that dimension.',
     'assumptions': ['DVR coefficient ring', 'finite common monomial support'],
     'remaining_inputs': [],
     'sources': refs('data', 'RestSel degSet_finite', 'definition_and_application_support') + refs('sel', 'sel_key sel_li sel_sat restSel', 'source_proof_replaced_by_unit_minor')},
    {'id': 'SD2', 'title': 'Saturated residue bases and injective monomial tensor assembly',
     'status': 'proved_conditional_assembly_lemma',
     'statement': 'A finite free saturated polynomial lattice has residue-independent basis reductions; support intersections preserve saturation. An injective map of labelled tuples of support monomials makes the associated direct sum of tensor-product spaces inject into the product polynomial module. Successive quotient/remainder in n=ell+P(u+Qv) explains the exact source exponent recovery.',
     'assumptions': ['Saturation of the given segment modules', 'Injectivity of the labelled support exponent map'],
     'remaining_inputs': ['For the actual RestLam application: full NestedTypeBound saturation identification, LamGeo verification and exact row-degree matching RestLamDeg.'],
     'sources': refs('sat', 'lam_sat_restrict lam_dvd_of_res restLamA_of') + refs('prod', 'lam_coeff lam_li_fixed lam_li_all') + refs('img', 'LamGeo lam_digit lam_eval restLamInj_of') + refs('lam', 'RestLamA RestLamInj RestLamDeg restLam_of_rests')},
    {'id': 'SD3', 'title': 'Periodic frame predecessors and nonvanishing of the determinant multiplier',
     'status': 'faithful_translation_with_shorter_geometric_proof',
     'statement': 'The last r even predecessors of a late letter span less than a period and have distinct residues. Each substituted determinant evaluates to 1 at its own diagonal assignment. Its reduction is nonzero; their finite product remains nonzero in the residue polynomial domain. This proves DiscriminantNonzeroModUniformiser pointwise for valid frames.',
     'assumptions': ['The exact periodic frame validity hypotheses', 'Positive substitution exponents and a domain residue ring'],
     'remaining_inputs': [],
     'sources': refs('coarse', 'row detPl DlSeg Dl DiscriminantNonzeroModUniformiser', 'literal_definitions') + refs('distinct', 'late_vectors_distinct_tops') + refs('det', 'ph_detPl_ne_zero discriminant_nonzero_of_injective_tops') + refs('gen', 'discriminant_nonzero_mod_uniformiser')},
    {'id': 'SD4', 'title': 'Normal-degree bound with Cdeg=10 and a sharper intermediate expression',
     'status': 'faithful_translation_with_sharper_intermediate_bound',
     'statement': 'Writing N=|TT|, A=La*a/(p*k), B=a*p^(-L1), every polynomial in the actual selected generator span has normal degree <=N*(A+10B+kQ), hence <=10N*(A+B+kQ). Old-frame variables have zero normal weight; late letters tile one period; digit labels contribute <=NkQ. This proves RestDeg and the degree clause of Conclusion2 under the supplied hypotheses.',
     'assumptions': ['Dat.Hyp, including even period and frame validity', 'CLa>=0'],
     'remaining_inputs': [],
     'sources': refs('data', 'Hyp o gen NN RestDeg', 'exact_data_and_target') + refs('degree', 'wtVS vsDeg_eq nonW_eq exists_nonW sum_card_nonW okVars XX\'_supported ordDeg_eq even_of_isW vs_img_le pow_mul_o_le seg_bound label_bound gen_bound restDeg')},
    {'id': 'SD5', 'title': 'Residue rank transfer through the actual nonzero determinant multiplier',
     'status': 'proved_conditional_rank_transfer',
     'statement': 'If each reduced Delta-times-coarse-generator is a reduced actual generator, multiplication by reduced Delta injects LamBar into NNbar. SD1 then yields an integral actual-generator summand of at least the coarse residue dimension. Graphs of linear maps give nPl>=q^(rK), including the correct handling of a nonpositive target bound.',
     'depends_on': ['SD1', 'SD3'],
     'remaining_inputs': ['GeneratorModuloUniformiser for the actual coarse and fine symbol families', 'The quantitative lower bound on dim(LamBar)'],
     'sources': refs('coarse', 'Rj Qc Mj lamGen LamBar GeneratorModuloUniformiser RestCount restRank_of') + refs('genred', 'SegmentReductionLiftsMultihomogeneous generator_of_segment_reductions', 'unexpanded_congruence_input') + refs('gen', 'generator_modulo_uniformiser_of_adm', 'unexpanded_congruence_source_route') + refs('data', 'second_estimate_of_rank_bound')},
    {'id': 'SD6', 'title': 'A union-bound digit count and the terminal-path degree estimate',
     'status': 'proved_shorter_residue_count_and_conditional_RestMon',
     'statement': 'For r>=2,Q>2b, a truncated cube has >=Q^(r-1)*(1-2rb/Q) solutions to any prescribed sum congruence, by deleting forbidden coordinates from Q^(r-1) full solutions. Interlacing telescopes to d<=mu_new,1-mu_old,k<=2b for terminal path degrees. Under 4Yb<=Q these prove the exact RestMon row factor, retaining the path and terminal index.',
     'remaining_inputs': ['BetaRatioBound 4Y*beS<=Qc for the actual parameters; the separate good-path abundance estimate.'],
     'sources': refs('tau', 'BetaRatioBound TauDegreeOnPathBound ResidueClassCount restMon_of') + refs('res', 'residue_class_count tele_le dminus_le_beS tau_degree_on_path_bound') + refs('digits', 'residueClassLowerBound', 'recursive_source_proof_replaced_by_union_bound') + refs('good', 'IsPATH Tset Idx RestMon', 'literal_path_and_counting_targets') + refs('beta', 'beta_ratio_bound', 'retained_parameter_bound')},
    {'id': 'SD7', 'title': 'Elementary compression of the rank losses to coefficient one',
     'status': 'proved_arithmetic_lemma_with_exact_positive_target_condition',
     'statement': 'For J<=N,r>=2,k>=5,Y>=1 and 1-1/(32Y)<=alpha<=1, a positive target 1-Nr^2k/Y is <=alpha^J*((1-5/Y)(1-1/Y)(1-r/(2Y)))^N. The proof uses product(1-x)>=1-sum x and Bernoulli. A nonpositive rank target is separately trivial. This explains Crk=1 without claiming the preceding source factor bounds proved.',
     'remaining_inputs': ['The actual SumFacts component bounds and residue-family product/sum identities.'],
     'sources': refs('loss', 'sumEta sum_total_loss') + refs('loss', 'sum_fac_LL sum_fac_fr restSum_of', 'remaining_factor_assembly') + refs('sum', 'sum_facts restSum', 'retained_source_parameter_verification')},
    {'id': 'SD8', 'title': 'Exact quantitative selected-symbol target and remaining density frontier',
     'status': 'precise_retained_source_theorem_and_conditional_dependency_map',
     'statement': 'The pinned route chooses C0=1088,Crk=1,Cdeg=10. SD closes RestSel, DiscriminantNonzeroModUniformiser and RestDeg. Full residue rank still requires the coarse-generator congruence, actual RestLam support/degree/saturation identifications, good-path RestSeg construction and abundance, and RestPad/RestSum numerical aggregation. Hence Conclusion2 rank is not yet claimed as a complete human proof.',
     'remaining_inputs': ['GeneratorModuloUniformiser including the NestedTypeBound lift', 'Actual RestLam geometry, degree matching and saturation identification', 'RestSeg: RestMem, RestInd, GoodPathWeight and BetaRatioBound', 'RestPad and complete RestSum identities and parameter estimates'],
     'sources': refs('statement', 'Conclusion2 NestedTypeBound AdmB SecondPartClosed', 'exact_source_interfaces') + refs('data', 'Hyp RestRank second_estimate_of_rank_bound') + refs('count', 'RestLam RestSeg RestPad RestSum restCount_of') + refs('good', 'RestMem RestInd GoodPathWeight restSeg_of') + refs('pad', 'restPad', 'retained_numeric_input') + refs('main', 'second_estimate_of_restrictions restMon restInd secondPartClosed', 'pinned_witness_constants_and_assembly')},
]
for claim in claims:
    claim['proof_location'] = {'file': 'selected_dimension/selected_dimension_section.tex',
                               'expanded': 'selected_dimension/report.txt', 'section': claim['id']}

ledger = {'component': 'selected_dimension', 'artifact_version': '0.6',
          'repository': URL, 'commit': PIN, 'claims': claims,
          'source_files': [{k: v for k, v in files[key].items() if not k.startswith('_')} for key in PATHS],
          'validation': {'lean_sources_modified': False, 'full_lean_build_or_kernel_replay': False,
                         'all_files_equal_pinned_git_blobs': True}}
(HERE / 'provenance.json').write_text(json.dumps(ledger, ensure_ascii=False, indent=2) + '\n')
with (HERE / 'source_locators.txt').open('w') as f:
    for claim in claims:
        f.write(f"{claim['id']}: {claim['title']}\nStatus: {claim['status']}\n")
        for s in claim['sources']:
            f.write(f"  {s['declaration']}\n  {s['url']}\n  file SHA-256 {s['full_file_sha256']}\n  range SHA-256 {s['range_sha256']}\n")
        f.write('\n')
print(json.dumps({'claims': len(claims), 'source_links': sum(len(c['sources']) for c in claims),
                  'source_files': len(files), 'main_words': len((HERE/'selected_dimension_section.tex').read_text().split())}))
