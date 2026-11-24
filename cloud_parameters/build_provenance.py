"""Regenerate CP's exact pinned-source ledger; does not modify Lean sources."""
from pathlib import Path
import hashlib
import json
import re
import subprocess

HERE=Path(__file__).resolve().parent
REPO=HERE.parents[1]/'alpoge-rh'
PIN='7cbf7a0c32fca1badf05931879a37c3f8a2b03b4'
URL='https://github.com/CocoSgt/riemann-hypothesis-lean'
GB='src/Formalism/SharpRestriction/GrowthBounds/'
DS=GB+'DiagonalSupport/'
DF=GB+'DualFockLinear/'
SE=GB+'ScaleEdges/'
PATHS={
 'hyps':SE+'ManyEdges.lean',
 'sl':GB+'SourceCleaning.lean',
 'data':GB+'TwistedSubstitution/Proposition5Gram.lean',
 'Dt':GB+'Lemma5aAt.lean',
 'plane':GB+'TwistedSubstitution/PlaneCoeff.lean',
 'num':DS+'LeOfOneLeMul.lean',
 'geometry':DS+'SlackBoundJoint.lean',
 'size':DS+'SlackBoundReal.lean',
 'tri':DS+'TriangularCountLeSq.lean',
 'cube':DS+'LeCubeMul.lean',
 'sizeStep':DS+'SizeStep.lean',
 'mfhd':DS+'ExistsMapOfCoefGe.lean',
 'mfh':DS+'MembTop.lean',
 'gram':DS+'GramExponentArithmetic.lean',
 'pick':DS+'PickCore.lean',
 'pickdefs':DS+'PickDefs.lean',
 'decomp':DS+'DecompositionOfThreeParts.lean',
 'three':DS+'Proposition5OfThreeParts.lean',
 'NS':DF+'RestXiPOfNS.lean',
 'XI':DF+'XiStepNOfP.lean',
 'ND':DF+'RestNDOfAdm.lean',
 'zero':DF+'NormalDegreeZeroMul.lean',
 'ndops':DF+'NormDegUniv.lean',
 'truncate':DF+'Lemma4ElementZero.lean',
 'real':DF+'ScaleZeroIff.lean',
 'pair':DF+'PairFormula.lean',
 'one':DF+'OneSidedLemma4Realisable.lean',
 'flat':DF+'FockSumRight.lean',
 'cloud':DF+'TestSideExplicitIdentification.lean',
 'cloud3':DF+'RestCloudBOfThree.lean',
 'logsize':DF+'LogSizeBoundLe.lean',
 'prim':DF+'TheoremIIClosedOfTestBound.lean',
 'prim1':DF+'PrimStep.lean',
 'theta':SE+'SourcePrimitiveIntegrality.lean',
 'cloudY':SE+'RestCloudXOfY.lean',
 'cloudX':SE+'RestCloudOfX.lean',
 'cloudStep':SE+'SymbolRealisableBound.lean',
}
PREFIX=r'(?:@\[[^\n]*\]\s*)?(?:(?:private|protected|noncomputable)\s+)*'
DECL=re.compile(r'^'+PREFIX+r'(?:def|abbrev|theorem|lemma|structure|class|instance)\s+(\S+)')
BOUND=re.compile(r'^'+PREFIX+r'(?:def|abbrev|theorem|lemma|structure|class|instance|namespace|section|end|variable|open|include|omit|attribute)\b')
files={}
for key,path in PATHS.items():
 raw=(REPO/path).read_bytes()
 assert raw==subprocess.check_output(['git','-C',str(REPO),'show',f'{PIN}:{path}']),path
 lines=raw.splitlines(keepends=True)
 stack=[]; decls=[]
 for i,bline in enumerate(lines):
  line=bline.decode().rstrip('\r\n')
  if m:=re.match(r'^namespace\s+(\S+)',line): stack.append(('namespace',m[1]))
  elif m:=re.match(r'^(?:noncomputable\s+)?section(?:\s+(\S+))?\s*$',line): stack.append(('section',m[1]))
  elif m:=re.match(r'^end(?:\s+(\S+))?\s*$',line):
   assert stack,(path,i+1,'end')
   kind,label=stack.pop()
   assert not m[1] or m[1]==label,(path,i+1,label,m[1])
  elif m:=DECL.match(line):
   ns='.'.join(label for kind,label in stack if kind=='namespace')
   decls.append((m[1],i,ns+'.'+m[1] if ns else m[1]))
 files[key]={'path':path,'sha256':hashlib.sha256(raw).hexdigest(),'bytes':len(raw),'lines':len(lines),
             '_lines':lines,'_decls':decls,'verified_equal_to_pinned_git_blob':True}

def refs(key,names,role='exact_interface_and_parallel_source_route'):
 item=files[key]; out=[]
 for name in names.split():
  hits=[d for d in item['_decls'] if d[0]==name]
  assert len(hits)==1,(key,name,hits)
  _,start,qualified=hits[0]
  end=start+1
  while end<item['lines'] and not BOUND.match(item['_lines'][end].decode()):end+=1
  while end>start+1 and not item['_lines'][end-1].strip():end-=1
  raw=b''.join(item['_lines'][start:end])
  out.append({'path':item['path'],'declaration':qualified,'source_spelling':name,
              'line_start':start+1,'line_end':end,'full_file_sha256':item['sha256'],
              'range_sha256':hashlib.sha256(raw).hexdigest(),'role':role,
              'url':f'{URL}/blob/{PIN}/{item["path"]}#L{start+1}-L{end}'})
 return out

claims=[
 {'id':'CP1','title':'Direct floor-correct Type-II numerical slack',
  'status':'proved_human_simplification_for_actual_hypotheses',
  'statement':'Under actual Hyps and C>=100, B>=a/Q² gives floor(B/(Yk²))>=B/(2Yk²) and 3r p^(-L1-1)B<=sl/8. B>=a/Q gives sl>=100r²cP. This supplies hII5 and hII0 without retaining the general parameter lemmas.',
  'depends_on':['FG7'],
  'sources':refs('hyps','Hyps')+refs('sl','levDeg Bo sl cPrime mStar')+refs('num','NB nb_of numAt_of numStep_of')},
 {'id':'CP2','title':'Actual Hyp26 and MFH from frame geometry',
  'status':'proved_human_actual_data_compatibility',
  'statement':'The stronger L2 gaps and full segment span give dLL<=3a p^(-D-L1-1), Bo>=a/p^(D+g)>=a/Q, including the periodic wrap. CP1 yields r dLL/P+26r cP<=3sl/8 and sl>=128cP. Hence literal Hyp26 and every MFH clause hold.',
  'depends_on':['CP1','FG5','FG6','FG7'],
  'sources':refs('Dt','Hyp')+refs('geometry','LL_gap Bo_ge seg_shift dLL_le slack_bound_joint')+refs('mfhd','MFH')+refs('mfh','margin_real mfh_of')},
 {'id':'CP3','title':'Actual chain and projector size budgets 20 and 9',
  'status':'proved_human_actual_data_estimate',
  'statement':'Actual one-period late letters number<=N, chains<=N, counted links<=N, normal cuts<=2N. Degree bounds and Legendre imply Dm+Dl+3kp<=20L, kappa_fl<=20L and SizeAt9. In particular cP>80L>4MD; no additional local numerical budget is assumed.',
  'depends_on':['CP1','FG8','LA2'],
  'sources':refs('Dt','eP Dm Dl kp')+refs('size','posTL_win posTL_inj card_TL_le card_TL_eq lg_le_four sizes_le')+
    refs('num','kapFl_le numAt_of')+refs('tri','sl_lt_real mult_level mult_level_real card_idx J_le_card DnoOf_le')+
    refs('cube','k_le_a sl_lt_Bo sizeAt_of')+refs('pickdefs','DnoOf SizeAt')},
 {'id':'CP4','title':'Constructing the literal selected signed-chain object',
  'status':'proved_human_actual_constructor',
  'statement':'The unit coefficient, exact digit class, plane/normal degrees, actual signs and carries, finite prefix chains, T_u-sl/8 thresholds and positive T_u-3sl/8 link thresholds construct mkDt. Select the joint projector first at zero normal weights, then update thresholds without changing its operators. DT/IW provide digit units and coefficient selection; IN/WT supply actual incoming membership.',
  'depends_on':['CP2','CP3','DT6','DT7','DT8','IW4','IN9','WT9'],
  'sources':refs('Dt','SignedChainData trueLet modelLet XX')+refs('plane','thStar slU Tied MemAt')+
    refs('gram','mkDt JPOK\' updTh upd_trueLet jpok_upd exists_unit_coeff pickAt_of pickStep_all')+
    refs('pick','thL_arith pick_core')+refs('data','DataII MemStep')},
 {'id':'CP5','title':'Actual constrained test with normalized exponent 50L',
  'status':'proved_human_component_assembly',
  'statement':'On the constructed data PG26,2,24,60, DT selection cost9L, MD<=20L and kappa_fl<=20L give normalized integral value dividing p^ceil(49L), with ceil(49L)<=50L. Actual MFH makes DT outgoing membership applicable. This supplies Proposition5At and NSStep without extra local budget assumptions.',
  'depends_on':['CP2','CP3','CP4','PG11','DT8','DT9','DT10','CL8','CL9'],
  'sources':refs('pick','gram_exponent_arithmetic pick_core')+refs('decomp','leQ_add_of_lt geQ_expFact geQ_fock')+
    refs('three','asm_coefGe ph_coefGe ph_mem_pol value_core proposition5_at_of_three_parts proposition5_of_three_parts')+
    refs('data','Proposition5At nsStep_of')+refs('NS','NSAt xiAtP_of_NS NSStep restXiP_of_NS')},
 {'id':'CP6','title':'Uniform normal-degree height with constant 10',
  'status':'proved_human_actual_height_bound',
  'statement':'RK and EA bound the actual source normal degree by X. The fixed multiplier has normal degree zero; conjugated elementary operators raise it by<=1, with at most Nc0 operators. All one-sided tests of order above floor(X)+Nc0 pair to zero and may be discarded, proving Ct0=10 uniformly in the primitive input.',
  'depends_on':['RK3','EA1','EA2','CP5'],
  'sources':refs('hyps','t0')+refs('zero','fixed_symbol_normal_degree_zero Nsub NsubInv subst_eq_Lin Nsub_mul')+
    refs('ndops','nd_move nd_op Lin_pderiv nd_Lin_op nd_word word_length nd_OpCl')+
    refs('ND','restND_of_adm')+refs('truncate','lemma4_element_normal_degree lemma4_element_zero NDAt xiAt_of')+
    refs('XI','symP xiStepN_of_P')},
 {'id':'CP7','title':'Actual realization-to-dual map and integral pairing error',
  'status':'proved_human_component_assembly_using_completed_OR',
  'statement':'For the actual OR-realizable one-sided symbols, normalized opposite-edge Fock duality gives T with target height tF, own-edge integrality, other-edge order cP and beta_fl=y+w^cP z. Since cP>2DX, the new value still divides p^DX. This proves actual FlatAt; OR is separately proved, not inferred from regular source-symbol realization.',
  'depends_on':['CP5','CP6','IW7','EL6','CL10','OR8'],
  'sources':refs('theta','IsTrueTheta theta_exists')+refs('pair','Aa_dual2 subst_Lin pair_formula exists_gv')+
    refs('real','realAt_gen realStep')+refs('one','OneSidedLemma4Element RealAt one_sided_lemma4_realisable')+
    refs('flat','valLe_perturb restFlat_of')+refs('cloud','FlatAt')},
 {'id':'CP8','title':'Uniform primitive cloud with constants 10 and 54',
  'status':'proved_human_actual_cloud_theorem',
  'statement':'CB/CL primitive-array detection, IW/CL contraction cost4L and CP7 flat cost50L yield actual cloud witnesses Ct0=10,CD1=54, other-edge order c* and the literal height bound. The integral scalar in the contraction need not be a unit: x(cb)=p^(kappa+DX). Thresholds are chosen before all local data. OR proves its actual threshold100, so CloudStep(C,10,54,1088) holds for every C>=4129 under the literal Type-II hypotheses.',
  'depends_on':['CP7','CB6','CB7','CL3','CL4','CL5','CL6','CL11','IW7','RK3','EA2'],
  'sources':refs('cloud','OpCl SgOp CloudBAt CloudBStep FlatStep test_bound_of_two_halves')+
    refs('cloud3','TSOpAt OntoAt pairAt_of_tsop restPairTop_of restCloudB_of_three')+
    refs('logsize','log_size_bound_le sizeStep restSize restCloudB_of_op')+
    refs('prim','primStep_of source_integrality_of_substitution')+refs('prim1','rest6a')+
    refs('theta','PrimAt restCloudY_of')+refs('cloudY','CloudStepY restCloudX_of_Y')+
    refs('cloudX','CloudStepX restCloud_of_X')+refs('cloudStep','CloudStep')},
]
for c in claims:
 c['assumptions']=['Literal actual Type-II setting, orbit and weight hypotheses; the threshold and auxiliary choices specified in the report.']
 c['remaining_inputs']=[]
 c['proof_location']={'file':'cloud_parameters/cloud_parameters_section.tex','expanded':'cloud_parameters/report.txt','section':c['id']}
ledger={'component':'cloud_parameters','artifact_version':'0.8','repository':URL,'commit':PIN,'claims':claims,
 'source_files':[{k:v for k,v in files[key].items() if not k.startswith('_')} for key in PATHS],
 'validation':{'lean_sources_modified':False,'full_lean_build_or_kernel_replay':False,'all_files_equal_pinned_git_blobs':True}}
(HERE/'provenance.json').write_text(json.dumps(ledger,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'claims':len(claims),'sources':sum(len(c['sources']) for c in claims),'files':len(files)}))
