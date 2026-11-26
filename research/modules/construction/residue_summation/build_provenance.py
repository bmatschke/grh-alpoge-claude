"""Rebuild the RS source ledger from byte-identical pinned Lean source files."""
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
 'frames':GB+'SegRing.lean',
 'data':SD+'NonemptyDvrSettingOfStandard.lean',
 'coarse':SD+'Coarse.lean',
 'count':SD+'RestCountOf.lean',
 'occ':SD+'TopOccursInAtMostTwoSegments.lean',
 'cost':SD+'TopCountLowerBoundsOfOccurrence.lean',
 'num':SD+'ReflectionMemGlevCastSucc.lean',
 'scales':SD+'FrameZeroStrictMono.lean',
 'geo':SD+'SumPosOfPer.lean',
 'pad':SD+'DivMulSubLeDivSubDiv.lean',
 'digits':SD+'FactorialMulChooseEqProdRange.lean',
 'family':SD+'FamilyDegreesAdmissible.lean',
 'labels':SD+'SumMemLaSet.lean',
 'total':SD+'SumTotalLoss.lean',
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


claims=[]
def claim(id,title,statement,groups,depends=(),remaining=()):
    claims.append({'id':id,'title':title,'status':'proved_human_reconstruction_with_stated_source_hypotheses',
      'statement':statement,'assumptions':['Literal Dat.Hyp; CLa,Ck>=1088. Full frame and numerical supply is a separate existence problem.'],
      'depends_on':list(depends),'remaining_inputs':list(remaining),
      'sources':sum((refs(key,names,role) for key,names,role in groups),[]),
      'proof_location':{'file':'residue_summation/residue_summation_section.tex','expanded':'residue_summation/report.txt','section':id}})
claim('RS1','Actual periodic tiling and two-occurrence bound',
 'Late intervals tile TT exactly, split into LL and current frame, and give J<=N. Every residue occurs at most twice in the full segment-letter sets. Basic Hyp consequences are Ns>=1,k>=5,r<=k,Q>=1,a>=32.',[
 ('frames','Frames letters IsW LLset dist Valid','literal_frame_data'),
 ('data','Dat Hyp k La d','literal_source_hypotheses'),
 ('geo','fr_add_mul_period fr_lt_fr_of_lt_of_valid sum_fr_le mem_late_iff exists_shift_of_posOf_eq_of_mem_late prod_tiling sum_LLsub sum_frlate sum_split J_le_card_TT_of_valid','periodic_geometry'),
 ('occ','occ_Ioc top_occurs_in_at_most_two_segments','two_occurrence_bound'),
 ('num','frame_zero_le reflection_mem_Glev_castSucc mem_letters_bounds Basics basics','elementary_parameter_consequences')])
claim('RS2','Actual determinant degree cost and positive remaining degrees',
 'Et<=4Ns*a/(k^2Y), Et<=a/40 and E0<=a/32 prove aprime=deg-Eprime-Et>=.9deg on TT, Et<=d everywhere and Et=0 off TT. Also Eprime+Et<=5deg/(kY). All natural subtractions are justified.',[
 ('data','sg d Hyp','literal_definitions'),('coarse','row Et a\'','literal_degree_cost'),
 ('cost','LeadingLetterInAtMostTwoSegments oldest_le_row sg_mul_le late_index_map_mem_letters late_index_map_injective Et_le a_ge k_sq_mul_Y_ge_Ns top_count_lower_bounds_of_occurrence','degree_cost_and_margin'),
 ('scales','sum_compA','Y_dependent_loss_calculation')],['RS1'])
claim('RS3','Exact coarse scales and numerical margins',
 'Tj>=4p(E0+mStar+1), p^R<=Tj<p^(R+1), p^R>mStar and a/P>=8Yk^2Ns give a\'/P>=(36/5)Yk^2Ns. A_j=max(z_j,H+s_j) gives P_jQ_j=P_(j+1), product Q_j=p^nprime, consistency and periodicity. At current-frame letters a\'/(P_jQ_j)>=k+r+1; a>=32Y.',[
 ('coarse','Rj Qc Bw','literal_scale_definitions'),('count','Pz','literal_scale_definition'),
 ('num','Tj den_pos Tj_ge pow_Rj_le lt_pow_Rj power_exceeds_max_multiplicity l42b','actual_scale_bounds'),
 ('scales','Rj_add_first_frame_gap_le_last_frame_gap_add_Rj_succ frame_zero_strict_mono sum_PzQc sum_prodQ thirty_two_Y_le_a sum_aP sum_kP','source_scale_proof_shortened_by_common_cutoff'),
 ('geo','sum_Rj_per sum_Pz_per sum_Qc_per sum_uniqP sum_perW','periodicity_and_equal_residue_consistency')],['RS1','RS2'])
claim('RS4','Actual degree padding and cancellation of natural subtraction',
 'Admissible labels give a\'/P-k<nz<=a\'/P. A short successive-floor bound gives old-frame degree>=Bw, proving RestPad 1088. RS3 also gives e<nz and hence exact e+Q*((nz-e)/Q)=nz for actual EE.',[
 ('count','laSet LA nz EE eZ bfam setTau AdmLL RestPad','literal_degree_families'),
 ('pad','div_mul_sub_le_div_sub_div eZ_lt_mul_Qc sum_la_lt restPad','source_floor_and_padding_proof'),
 ('family','sum_eZ_val family_degrees_admissible','exact_degree_admissibility')],['RS3'])
claim('RS5','Exact digit partitions and complete label factorization',
 'Unique coordinate decomposition w=lambda+Pv yields the exact composition-count identity. For kP<=n the number of bounded labels with sum congruent n is P^(k-1). Applied to source label sets, this proves all sumSt lower bounds and sum_LA.',[
 ('digits','sum_card_tuples sum_digit_count sum_label_count','digit_partition_source'),
 ('family','sumBin sum_one_le_bin sum_one_le_prod sum_single_le_prod sumhT sumSt','label_factor_definitions'),
 ('labels','sum_one_le_hT sum_mem_laSet sum_St_nontop sum_St_nonneg Pz_pos sum_St_LL sum_St_fr sum_LA','actual_label_set_application')],['RS1','RS3'])
claim('RS6','Actual binomial comparisons with loss 5/Y and 1/Y',
 'The product formula and Bernoulli prove B(a\')>=(1-5/Y)B(deg), and (PQ)^(k-1)B((Bw_next-m0)_+)>=(1-1/Y)B(a\'), using RS2/RS3. These discharge SumFacts.compA and compW.',[
 ('coarse','m0 Bw','literal_old_frame_parameters'),
 ('digits','factorial_mul_choose_eq_prod_range choose_add_mul_one_sub_le_pow_mul_choose_add','elementary_product_comparison'),
 ('scales','sumBin_eq sum_M_le sum_compA sum_compW','actual_parameter_comparisons')],['RS2','RS3'])
claim('RS7','Full residue-family product and sum assembly',
 'For arbitrary G satisfying the literal nonnegative late-degree and residue-sum conditions, independent EE choices and the product LA set give total>=alpha^J product W_j*T_j product S_t. Periodic shift and product Q=p^nprime complete frame factors and yield q^(rK) total>=alpha^J eta^N product B(deg) when the final target is positive.',[
 ('count','SegOK RestSeg RestSum','exact_function_hypotheses'),
 ('family','sumTset sumhT sumSt firstSumFactor sumWf sumTf sum_segBound_eq SumFacts sum_bfam_late','actual_summation_definitions'),
 ('labels','sum_LA','label_factorization'),('digits','prod_range_shift_of_periodic','cyclic_frame_reindexing'),
 ('total','sumEta sum_fac_LL sum_fac_fr restSum_of','exact_residue_family_assembly')],['RS1','RS3','RS4','RS5','RS6'])
claim('RS8','RestSum 1088 1 with all actual numerical inputs discharged',
 'A nonpositive target is immediate from nonnegative rank sums. For positive target, a>=32Y and J<=N meet SD7 hypotheses and alpha^J eta^N>=1-Nr^2k/Y. Thus RestSum 1088 1 and RestPad 1088 are reconstructed. Combining with actual RestLam and RestSeg gives RestCount; CG and SD3 then transfer the rank to actual symbols.',[
 ('family','first_sum_factor_bounds SumFacts','actual_loss_inputs'),
 ('total','sum_total_loss restSum_of','final_positive_target_loss'),
 ('scales','sum_facts restSum','source_closed_sum_theorem'),
 ('pad','restPad','source_closed_padding_theorem'),
 ('count','RestLam RestSeg RestPad RestSum restCount_of','conditional_dimension_assembly'),
 ('coarse','RestCount restRank_of','conditional_rank_transfer')],['RS7','SD7'],['For final selected-symbol rank (not RestSum itself): actual RestLam, RestSeg and GeneratorModuloUniformiser, treated in companion LA, GP and CG components.'])
ledger={'component':'residue_summation','artifact_version':'0.7','repository':URL,'commit':PIN,'claims':claims,
 'source_files':[{k:v for k,v in files[key].items() if not k.startswith('_')} for key in PATHS],
 'validation':{'lean_sources_modified':False,'full_lean_build_or_kernel_replay':False,'all_files_equal_pinned_git_blobs':True}}
(HERE/'provenance.json').write_text(json.dumps(ledger,ensure_ascii=False,indent=2)+'\n')
with (HERE/'source_locators.txt').open('w') as out:
 for c in claims:
  out.write(c['id']+': '+c['title']+'\n')
  for r in c['sources']:out.write('  '+r['declaration']+'\n  '+r['url']+'\n')
  out.write('\n')
print(json.dumps({'claims':len(claims),'sources':sum(len(c['sources']) for c in claims),'files':len(files),'main_words':len((HERE/'residue_summation_section.tex').read_text().split())}))
