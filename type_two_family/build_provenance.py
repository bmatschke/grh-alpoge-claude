"""Regenerate GII pinned-source correspondence; no Lean execution or edits."""
from pathlib import Path
import hashlib
import json
import re
import subprocess

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[1] / 'alpoge-rh'
PIN = '7cbf7a0c32fca1badf05931879a37c3f8a2b03b4'
URL = 'https://github.com/CocoSgt/riemann-hypothesis-lean'
SR = 'src/Formalism/SharpRestriction/'
GB = SR+'GrowthBounds/'
LC = 'src/Formalism/LocalRingCardinality/'
GI = 'src/Development/AbelianVarietyTheory/Proofs/GlobalInterpolation/'
PATHS = {
    'top':GB+'TopChoiceBounds.lean',
    'cyclic':'src/Formalism/GrowthSums/FactorialBaseGrowth/NextEvenTopHolds.lean',
    'growth_stmt':'src/Formalism/GrowthSums/StatementB.lean',
    'good':'src/Formalism/SubspaceCounting/GoodOrbitIntervalTileCondition.lean',
    'corner':GB+'CornerGLContinuity.lean',
    'setting':GB+'UnramifiedQuadraticSetting.lean',
    'obj':GB+'ObjSeg.lean',
    'params':GB+'IsResidueClassZero.lean',
    'sizes':GB+'SizesAtRecord.lean',
    'small':GB+'SmallOrderPrimes.lean',
    'joints':GB+'Joints.lean',
    'aux':GB+'TableLineDegreeFive.lean',
    'scale':LC+'DataParams₂.lean',
    'host':LC+'DataHost.lean',
    'size_defs':SR+'ElevenLe.lean',
    'family_core':SR+'FamCore.lean',
    'family':SR+'ParConsts.lean',
    'prob_join':SR+'AdmissibleParameterJoins/GandSa.lean',
    'prob_select':SR+'GlobalSchurBounds/CMFieldLemmas.lean',
    'chosen':SR+'GlobalSchurBounds/Chosen.lean',
    'mertens':GB+'JointsLit.lean',
    'host_join':GI+'BadCharacterBound.lean',
    'host_num':GI+'SzRowNumAt.lean',
    'host_band':GI+'BandWidthLeInvSqOfRankBounds.lean',
    'host_design':'src/Development/AutomorphicArithmetic/CharacterBoxes/DesignS.lean',
}
PREFIX = r'(?:@\[[^\n]*\]\s*)?(?:(?:private|protected|noncomputable)\s+)*'
DECL = re.compile(r'^'+PREFIX+r'(?:def|abbrev|theorem|lemma|structure|class|instance)\s+(\S+)')
BOUND = re.compile(r'^'+PREFIX+r'(?:def|abbrev|theorem|lemma|structure|class|instance|namespace|section|end|variable|open|include|omit|attribute|set_option)\b')
files = {}
for key, path in PATHS.items():
    raw = (REPO/path).read_bytes()
    assert raw == subprocess.check_output(['git','-C',str(REPO),'show',f'{PIN}:{path}']), ('unpinned bytes',path)
    lines = raw.splitlines(keepends=True)
    stack, declarations = [], []
    for i, raw_line in enumerate(lines):
        line = raw_line.decode().rstrip('\r\n')
        if m := re.match(r'^namespace\s+(\S+)',line):
            stack.append(('namespace',m[1]))
        elif m := re.match(r'^(?:noncomputable\s+)?section(?:\s+(\S+))?\s*$',line):
            stack.append(('section',m[1]))
        elif m := re.match(r'^end(?:\s+(\S+))?\s*$',line):
            assert stack, (path,i+1,'end without opening')
            kind,label = stack.pop()
            assert not m[1] or m[1] == label, (path,i+1,label,m[1])
        elif m := DECL.match(line):
            ns = '.'.join(label for kind,label in stack if kind == 'namespace')
            declarations.append((m[1],i,ns+'.'+m[1] if ns else m[1]))
    assert all(kind == 'section' and label is None for kind,label in stack), (path,'unclosed namespace')
    files[key] = {'path':path,'sha256':hashlib.sha256(raw).hexdigest(),'bytes':len(raw),
                  'lines':len(lines),'verified_equal_to_pinned_git_blob':True,
                  '_lines':lines,'_decls':declarations}

def refs(key, names, role='exact_source_interface_or_parallel_proof'):
    f = files[key]
    out = []
    for name in names.split():
        hits = [d for d in f['_decls'] if d[0] == name or d[2] == name]
        assert len(hits) == 1, (key,name,hits)
        spelling,start,qualified = hits[0]
        end = start+1
        while end < f['lines'] and not BOUND.match(f['_lines'][end].decode()):
            end += 1
        while end > start+1 and not f['_lines'][end-1].strip():
            end -= 1
        selected = b''.join(f['_lines'][start:end])
        out.append({'path':f['path'],'declaration':qualified,'source_spelling':spelling,
                    'line_start':start+1,'line_end':end,'full_file_sha256':f['sha256'],
                    'range_sha256':hashlib.sha256(selected).hexdigest(),'range_bytes':len(selected),
                    'first_line':f['_lines'][start].decode().rstrip('\r\n'),
                    'role':role,'url':f'{URL}/blob/{PIN}/{f["path"]}#L{start+1}-L{end}'})
    return out

claims = [
 {'id':'GII1','title':'Actual cyclic good-orbit counts, predecessor bounds and segments',
  'status':'proved_human_finite_cyclic_count_and_actual_segment_identification',
  'statement':'Under the literal good-orbit conditions and 3G<=n-prime, periodic marked starts give a selected even successor within G. The incidence count gives n-prime<=NG<=n-prime*N1, strengthening the source upper count. The least even successor and the short-window cap give the actual positional clauses, numSeg>=2, segG<=G and segS<=N1.',
  'depends_on':[],
  'assumptions':['Finite cyclic orbit; r,u>=1; G=(M+5)(6r+1)u; literal short-window, tile-run and G-window conditions; 3G<=n-prime.','For predecessor clauses, cap=r-1 and L1<=L2<u.'],
  'sources':refs('good','cell Marked CondTiles CondIntervals GoodOrbitIntervalTileCondition')+
   refs('growth_stmt','SegmentBound OldestFar NextEvenTop TopCount')+
   refs('cyclic','next_even_top_holds top_count_holds')+
   refs('corner','fwd OrbitRaw SegmentCountBounds OrbitPositions OrbitSizeBounds')+
   refs('top','bc_next bc_old bc_gap bc_tile_end bc_tile bc_seg bc_size_real bs_numSeg bs_start_mem bs_min bs_segs orbit_segments')+
   refs('obj','cdist evenTops numSeg segStart segNext segG segDists segS')+
   refs('joints','OrbitSegs'),
  'new_human_argument':'Periodic marked starts keep the incomplete cyclic remainder; summing all cyclic windows gives the stronger upper bound NG<=n-prime*N1.'},
 {'id':'GII2','title':'Exact ceilings and one epsilon-dependent logarithmic count constant',
  'status':'proved_human_explicit_uniform_ceiling_estimates',
  'statement':'For Ce=40(6r+1)((h+3)10^(6r+1)+6), prove G<=Ce log(x)/delta, N1<=Ce log(x), and n-prime*delta/(Ce log(x))<=N<=40n-prime*delta. At actual rG,hG the constant depends only on epsilon, and eventually 3G<=x^(epsilon/4).',
  'depends_on':['GII1'],
  'assumptions':['x>=3, 0<delta<=1, r>=1, h>=0 and the exact displayed ceilings.','For the top count use GII1; for eventual scale estimates use 0<epsilon<1/52 and delta=x^(-epsilon/8).'],
  'sources':refs('setting',"goodU goodEll orbitSmallMultiplicity goodG' orbitWindowCount IsGoodOrbit")+
   refs('params','hG KG rG N1 Gp')+
   refs('top','logBoundConstant logBoundConstant_pos bc_goodU_pos bc_size segment_count_log_bounds period_ge_three_gap_eventually master_orbit_sizes_hold')},
 {'id':'GII3','title':'Actual orbit transport, family adm1 and logarithmic-window quantifiers',
  'status':'proved_human_literal_orbit_bijection_and_uniform_family_bounds',
  'statement':'The actual representative map identifies topsPos with topsOn and preserves index parity and modular distances. This proves AuxBlock8.adm1 for C31>=Ce and FamilyWindowLogBound for CN>=Ce, uniformly over every current family member. Nonnegative substitution gives rho<=rhoB<=x^-2 from the actual family field.',
  'depends_on':['GII1','GII2'],
  'assumptions':['Literal Inst representative identities and inert-prime step identification.','For a supplied FamP use its fixed valid epsilon, fixed J, scale identities, nonnegative constant tuple and rhoB bound; do not assume current Ix(x) is nonempty.'],
  'sources':refs('params','HH hP Inst stepP nP reps topsOn Nv topsPos wPos IsV Good CbLarge rho rhoB rho_le_rhoB')+
   refs('small','adm1')+
   refs('top','base_point_add_smul base_point_idempotent base_point_of_representative orbit_index_injective mem_tops_positions_iff mem_tops_on_orbit_iff isV_iff_even_index vertex_count_eq_card_tops forward_back_index_eq back_smul_eq_sub first_length_le_window uniform_constant_of_master uniform_constant_at_instance family_uniform_constant_of_master family_log_bound_threshold')+
   refs('corner','WindowLogBound FamilyOrbitPositionsAndSizeBounds FamilyWindowLogBound')+
   refs('family_core','FamCore FamCore.one_le_J FamCore.ez FamCore.L_ez')+
   refs('family','FamP')},
 {'id':'GII4','title':'Actual levels, inert-prime lower bound and shifted integer weight windows',
  'status':'proved_human_all_scale_window_and_floor_comparisons',
  'statement':'Literal SizesAt gives k<=x^5, n<=x^3 and c<=4b-prime/x. Prove L2<=514log(x)<u, 3G<=x^(epsilon/4), inert p>x^(zeta/5), p>=13 eventually, and L2<=2ceil(620/zeta). Actual ParametersFill and rho<=1/7 give the exact winA/winB and all shifted floor-weight clauses, including c>=0 and a-c>=1.',
  'depends_on':['GII2','GII3'],
  'assumptions':['Actual SizeN, SizeK, SizeLa, SizeBot, sixth SizeDel clause, parameter equality Lambda=LaG, rho<=1/7 and host split-small property.','0<epsilon<1/52, fixed zeta>0, and one sufficiently large x threshold.'],
  'sources':refs('scale',"Scale ez a X' b' A p0 delta1 SizeData₂")+
   refs('host','primeClass Host')+
   refs('size_defs','szTh SizeN SizeK SizeLa SizeBot SizeDel SizesAt')+
   refs('params','cG L1 L2 Nstar La Qp c0num winA winB ParametersFill')+
   refs('sizes','localLength_le_ceil_log_mul two_mul_localLength_le_maxLength thirteen_le Sc_le Ib_le windows_at')+
   refs('top','inert_primes_lower_bound two_mul_first_length_le_window window_length_le_ceil_at_scale window_length_lt_tile_length window_length_le_ceil')},
 {'id':'GII5','title':'Lower top count supplies every polynomial Type-II rank margin',
  'status':'proved_human_first_six_NumII_fields_uniformly',
  'statement':'For arbitrary actual data with SizesAt, p<p0, x^(epsilon/4)<=n-prime<=n, N<=n-prime and the actual lower top count, one threshold gives N1^2<=N<=rN, r<=x^26, N1+3r<=k, Ck-prime*N1^2 log(a)<=k, p^(L1-1)>=k^2 x^78, and 256k^2N x^52<=k^2x^78.',
  'depends_on':['GII2','GII4'],
  'assumptions':['epsilon and the nonnegative constant tuple and C31>0 are fixed before x.','The displayed literal size, prime, orbit-order and lower-count hypotheses; goodness itself is not used after the count is supplied.'],
  'sources':refs('params','Consts Consts.Nonneg L1 N1 rG')+
   refs('sizes','NumII numII_ev')+
   refs('size_defs','SizeN SizeK')},
 {'id':'GII6','title':'Full Type-II Q^5 size bound with unchanged source exponents',
  'status':'proved_human_actual_ceiling_and_exponential_budget',
  'statement':'Uniformly under GII5 hypotheses, prove Q^5<=exp(5x^(7epsilon/48)), DII<=x^18*b-prime including its ceiling, and the exact last NumII expression<=x^69*exp(5x^(7epsilon/48))*b-prime<=a-c. All threshold constants precede the member, prime and orbit.',
  'depends_on':['GII4','GII5'],
  'assumptions':['The GII5 hypotheses; fixed nonnegative denominator/size constants.','One threshold also enforces x>=max(500,480CD,Cs) and the explicit logarithm-versus-power comparisons.'],
  'sources':refs('params','NplusF DIIf Qp c0num')+
   refs('sizes','DII_arith SzII_arith NumII numII_ev')+
   refs('scale',"a X' b' A p0")},
 {'id':'GII7','title':'Literal HypIIAt supplied uniformly to every member of a given family',
  'status':'proved_human_actual_family_TypeII_hypothesis_supply',
  'statement':'For a supplied FamP epsilon with CN>=Ce(epsilon), choose one x0 after all fixed family constants and J; for every x>=x0 and every i in Ix(x), prove actual HypIIAt. The proof includes candidate prime size, all weight clauses, all NumII fields and the correct quantifier order; empty current index or good-representative sets are harmless.',
  'depends_on':['GII3','GII4','GII5','GII6'],
  'assumptions':['A supplied literal FamP, its SizesAt and ParametersFill records and rhoB bound.','CN>=Ce(epsilon); no construction of FamP or abundance of its good representatives is assumed proved by this claim.'],
  'sources':refs('params','Cand goodReps ParametersFill')+
   refs('joints','HypIIAt')+
   refs('sizes',"hypIIAt_ev exists_place' hypIIAt_fam_of hypIIAt_fam")+
   refs('family','FamP')},
 {'id':'GII8','title':'Exact local Type-II witness at the global depth, height and loss',
  'status':'proved_human_actual_local_to_global_parameter_substitution',
  'statement':'At the supplied standard coefficient setting, apply reconstructed local Type II with m=k-1, a0=a-c, Y=x^26, floor(c), floor(c0), Dp=DII and cStar=8(DII+1). Every local hypothesis follows from literal adm6 premises and GII7. Termwise monotonicity gives ceil(tIIf), actual DIIf and min(1,kapIIf raw), proving the exact AuxBlock8.adm6.',
  'depends_on':['EA9','CP8','OR8','GII7'],
  'assumptions':['c>=0 and a-c>=1; one local C>=4129 dominated by all six displayed global Type-II constants.','The supplied standard coefficient setting and the literal adm6 orbit/count/weight/numerical premises.'],
  'sources':refs('small','adm6')+
   refs('aux','OrbitHyp WeightHyp La tBound aux₃ ConclusionE')+
   refs('params','DIIf tIIf kapIIf')+
   refs('joints','type_two_hypothesis_of_counts'),
  'separate_remaining_work':['Scalar extension to the actual place is BC/GJ; this implication alone does not construct a global family.']},
 {'id':'GII9','title':'Actual bad-orbit probability with one selected point conditioned',
  'status':'proved_human_full_conditional_probability_and_uniform_family_bound',
  'statement':'With Lb=2ceil(620/zeta) and Cb=(Lb+1)2^Lb+2, prove conditional bad-orbit probability<=Cb*x^-2. Separate short windows containing the forced point, discard the affected marked tile, and bound long-window tails. Removing conditioning gives the literal BadProb and FamilyBadPrimeBound uniformly over all large-order steps and points.',
  'depends_on':['GII2','GII4'],
  'assumptions':['Finite ambient group, independent Bernoulli(delta) subset, delta=x^(-epsilon/8)<=1/10, L2<=Lb, 3G<=n-prime, and n-prime<=n<=x^(h+epsilon/8).','For the actual family use SizesAt, fixed epsilon,zeta and the inert-prime lower-bound supplier; the supplied host subset is not assumed random.'],
  'sources':refs('good','condProbAt binUpper markedBound')+
   refs('prob_join','posOn BadOrb BadProb')+
   refs('prob_select','bern')+
   refs('top','bernoulli_weight_union_eq bernoulli_marginal_sum_eq orbit_positions_map_val bad_orbit_prob_eq_conditional window_condition_failure_prob_le good_orbit_failure_prob_le binomial_tail_le_choose_mul_pow binomial_tail_le_exp_bound one_quarter_le_one_sub_pow_ceil marked_probability_bounds delta_pow_le_rpow marked_tile_failure_le_rpow binomial_tail_le_rpow sharp_tops_inequality_of_bounds tops_choice_holds window_length_le_ceil family_tops_choice_of_master family_tops_choice_holds')+
   refs('corner','BadPrimeBound FamilyBadPrimeBound FamilyBadPrimeBoundOfInertPrimesLarge')},
 {'id':'GII10','title':'Finite top-set selection and simultaneous weighted bad-orbit mass',
  'status':'proved_human_actual_TopsOK_existence_and_conditional_adm2',
  'statement':'For delta|H|>=16, Chebyshev and Markov select one subset of size between delta|H|/2 and 2delta|H| with exactly the source TopsOK weighted cost, including zero cost. An elementary factorial bound gives sum_(p<y)log(p)/p<=2log(y); consequently the selected subset has simultaneous bad mass<=|T|x^(-2+epsilon) eventually. If this same subset is the arithmetic host subset, it gives actual adm2.',
  'depends_on':['GII9'],
  'assumptions':['Nonnegative finite prime weights and the GII9 pointwise BadProb bound.','For actual adm2, the chosen subset and steps must be identified with the arithmetic host; that transport is explicitly separate.'],
  'sources':refs('prob_select','Conclusion6')+
   refs('prob_join','TopsOK badOrb_congr tops_exist_of frobenius_step_large_order badOrb_TT primes_eq tops_share_bound')+
   refs('chosen','ChTT_at largeOrderResiduePrimes badTops ChBad_at ChosenTT ChosenBad')+
   refs('small','BTT adm2')+
   refs('corner','MertensBound SegmentEndpointChoiceExists FamilyMaximaSpacing FamilyMaximaChoiceWithConstant FamilyMaximaChoice')+
   refs('top','stmtTTc_proved bm_sum_le stmtTT_proved tops_share_bound family_tops_statement_of_mertens')+
   refs('mertens','mertens_bound mertens_bound_family'),
  'new_human_argument':'Direct finite Chebyshev/Markov selection and an elementary factorial prime-weight estimate replace longer wrappers while preserving their exact interfaces.',
  'separate_remaining_work':['Realize the same selected subset, rank, q,d, prime classification and Frobenius steps in the actual host and family.']},
]

for claim in claims:
    claim['proof_location']={'file':'type_two_family/main.tex','expanded':'type_two_family/report.txt','section':claim['id']}
    claim['remaining_inputs']=[]
    claim.setdefault('separate_remaining_work',[])

navigation = refs('host_join','badOK_iff_badOfBase chBad_iff_badOfBase badOfBase_of_host chBad_of_from','explicit_unreconstructed_host_choice_join')+refs('host_num','szRow_numAt','explicit_unreconstructed_host_choice_join')+refs('host_band','bandWidth_le_inv_sq_of_rank_bounds szRow_band_lambda_primes','explicit_unreconstructed_host_choice_join')+refs('host_design','designS','explicit_unreconstructed_family_construction')

records=[source for claim in claims for source in claim['sources']]+navigation
unique={(s['path'],s['line_start'],s['line_end'],s['range_sha256']) for s in records}
for s in records:
    raw=(REPO/s['path']).read_bytes().splitlines(keepends=True)
    part=b''.join(raw[s['line_start']-1:s['line_end']])
    assert hashlib.sha256(part).hexdigest()==s['range_sha256']
    assert raw[s['line_start']-1].decode().rstrip('\r\n')==s['first_line']
    assert len(part)==s['range_bytes']
ledger={
 'component':'type_two_family','artifact_version':'0.11','repository':URL,'commit':PIN,
 'range_convention':'Inclusive one-based raw-line bytes, including original line endings.',
 'claims':claims,'next_host_join_sources':navigation,
 'source_files':[{k:v for k,v in f.items() if not k.startswith('_')} for f in files.values()],
 'review_scope':{
  'remarks_math':'Independently reviewed GII5-GII6 and GII9-GII10 against NumII, BadProb, TopsOK and conditional-event definitions; passed. The stronger SizeK consequence k<=x^5 was made explicit for the 620/zeta bound.',
  'scope':'Human reconstruction and exact source correspondence only; no full Lean build or kernel replay.'},
 'artifact_sha256':{name:hashlib.sha256((HERE/name).read_bytes()).hexdigest() for name in ['main.tex','report.txt','build_provenance.py']},
 'validation':{'lean_sources_modified':False,'full_lean_build_or_kernel_replay':False,
  'all_files_equal_pinned_git_blobs':True,'all_declarations_anchored':True,
  'all_range_hashes_rechecked':True,'source_records':len(records),'unique_ranges':len(unique)}
}
(HERE/'provenance.json').write_text(json.dumps(ledger,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'claims':len(claims),'source_records':len(records),'unique_ranges':len(unique),'files':len(files),'all_files_equal_pinned_git_blobs':True}))
