#!/usr/bin/env python3
"""Bind the actual measure constructions to the exact pinned source contracts.

This is a provenance builder, not a Lean/kernel replay or a mathematical proof
checker. Every numbered claim has a human proof in the corresponding TeX.
"""
from pathlib import Path
import hashlib
import json
import re
import subprocess

ROOT = Path(__file__).resolve().parent
SRC = ROOT.parent / 'formal_source'
PIN = '7cbf7a0c32fca1badf05931879a37c3f8a2b03b4'
assert subprocess.check_output(['git','-C',str(SRC),'rev-parse','HEAD'],text=True).strip()==PIN
sha=lambda x:hashlib.sha256(x).hexdigest()
S='src/Formalism/LocalToGlobal/SiegelLatticeTheory/'
H=S+'HaarTransversals/'
U=H+'UnitaryHaarProducts/'
F='src/Development/AbelianVarietyTheory/Proofs/FlagMeasures/'
P='src/Formalism/PeriodIntegrals/'

DATA={
 'adelic_measures_v48':{
  'prefix':'AMD','count':17,'A':[],
  'groups':{
   'bridge_contract':[(S+'FundamentalEquivalence/AdBridge.lean',13,118,'Literal scalar maps, IsBridge, rational/compact sets and all three AdelicIsomorphism predicates'),(S+'ClosedVolumeStatements/AdelicIsomorphismStatement.lean',1,None,'Full original bridge producer')],
   'original_instance':[('src/Formalism/SharpRestriction/CuspSpanNormBounds/GlobAut.lean',16,118,'Original CM instance, nondegenerate form, real coordinates, lattice congruence topology and rational points')],
   'standard_groups':[(S+'FundamentalEquivalence/LevelIntersectParabolic.lean',149,178,'Original Frame, IsStd, Ssub and Hsub'),(S+'FundamentalEquivalence/LevelIntersectParabolic.lean',225,255,'Literal Nsub; includes all of U-perp, rather than only the chosen frame vectors')],
   'measure_records':[(S+'CokernelGLCounts/Measures.lean',65,None,'Literal splitA, ambient pushforward, five/eight measure entries, six/eleven normalization clauses, ratOf and choice-based covolume')],
   'weak_infinity':[(H+'HidaSetting.lean',24,65,'Actual real flag and unipotent subgroups and coordinate maps'),(H+'HidaSetting.lean',136,160,'Four-clause IsHaarOnSet and exact Hset'),(U+'MeasInfCut.lean',1,None,'Full original InfTransfer with arbitrary supplied bridge and arbitrary weak source measures')],
   'group_measure':[(U+'MExistsCut.lean',52,64,'Full original MGExists and its three exact equalities'),(U+'MultiplicityGExists.lean',471,611,'Original local/tuple Haar constructors and full MGExists implementation')],
   'frame_measure':[(U+'MeasCore.lean',17,26,'Full original MWCore guarded by actual IsStd'),(P+'UnitaryGroupMassFormula/WeightedMeasureSplitting/HermitianMeasureSplitting.lean',1,None,'Original frame split and measure-core producer')],
   'actual_measured_block':[(U+'SettingBlocks.lean',209,215,'All original MBlk fields'),(U+'SettingBlocks.lean',358,363,'Entire MExists contract'),(U+'MExistsCut.lean',11,47,'Exact MeasTieCore, MExistsCore and original specialization'),(U+'MultiplicityGExists.lean',638,699,'Actual word frame standardness, MWExistsStd and all-input MExists assembly'),(H+'HidaSetting.lean',364,380,'Actual toInf/toFin and full MeasTie')],
   'prescribed_measure':[(F+'ExistsHaarMapProdEq.lean',1,None,'Arbitrary prescribed product/global Haar theorem'),(F+'ExistsMeasWPrescribed.lean',1,None,'Full prescribed MeasW statement with all five unchanged entries')],
   'unipotent_covolume':[(F+'NsubCocompact.lean',1,None,'Exact standard-frame Nsub cocompactness and rational subgroup'),(F+'FundamentalDomainCovol.lean',1,None,'Original covolume choice independence and finite positive scalar law'),(F+'ExistsHaarMeasureUnipotentRadicalCovolumeOne.lean',1,None,'Actual Haar measure of covolume one'),(F+'ExistsHaarMeasureUnipotentRadicalCovolumeOneStatement.lean',1,None,'Whole original universally quantified covolume-one contract')],
   'rescaling_consumer':[(F+'RescaleStep3.lean',1,None,'Same-infinity prescribed measure replacement inside original Siegel–Weil rescaling'),(F+'ExistsGlobalSetting.lean',1,None,'Actual full setting, transport and spectral endpoint with distinct remaining producers')]
  },
  'claim_groups':{
   1:['bridge_contract','measure_records'],2:['bridge_contract','original_instance'],3:['bridge_contract','original_instance'],
   4:['standard_groups','measure_records'],5:['standard_groups','frame_measure'],6:['standard_groups','frame_measure'],7:['standard_groups','measure_records','frame_measure'],
   8:['weak_infinity'],9:['weak_infinity','bridge_contract','standard_groups'],10:['group_measure','measure_records','bridge_contract'],
   11:['frame_measure','measure_records'],12:['actual_measured_block','weak_infinity','group_measure','frame_measure'],
   13:['prescribed_measure'],14:['prescribed_measure','measure_records'],15:['unipotent_covolume','standard_groups','measure_records'],
   16:['unipotent_covolume','measure_records'],17:['rescaling_consumer','prescribed_measure','unipotent_covolume']
  },
  'deps':{
   1:[],2:['AMD1','FV4'],3:['AMD1','AMD2'],4:['AMD1'],5:['AMD4'],6:['AMD4','AMD5'],7:['AMD5','AMD6'],
   8:[],9:['AMD2','AMD4','AMD6','AMD8'],10:['AMD2','AMD4'],11:['AMD4','AMD7'],
   12:['AMD9','AMD10','AMD11'],13:[],14:['AMD4','AMD7','AMD11','AMD13'],15:['AMD6'],16:['AMD15'],17:['AMD9','AMD14','AMD16']
  },
  'scopes':[
   'Canonical topological tensor splitting, original theta_v/tau_F formulas, involution and exact ambient group splitA, including rank zero.',
   'Full AdBridgeIso on every actual AutInst, exact original finite congruence topology, uniqueness under IsBridge and arbitrary-witness infinity/finite maps.',
   'Entire original AdBridgeGF and AdBridgeK for every supplied bridge, same rational matrix and exact original majorant/local lattice conditions; hence full AdelicIsomorphism.',
   'Exact original Nsub/Hsub/Ssub, closed lcsc group properties and global-to-infinite/finite topological splitting for every standard frame; arbitrary tuple stabilizers included.',
   'Actual S=N semidirect H with H=U(W), explicit algebraic inverse and no real definiteness restriction.',
   'Unimodularity and H-action modulus one at every finite and infinite place and on restricted adelic products; explicit Lie blocks and Norm(det h)^(-r)=1.',
   'Every prescribed N/H Haar pair gives the literal S Haar product and ambient identity, without an unspecified scalar.',
   'Source sigma-finite nonzero supported invariant measure becomes actual Haar on the specified closed unimodular subgroup, by explicit Tonelli identities and scalar comparison.',
   'Full InfTransfer for all original instances, arbitrary supplied bridge witnesses, standard frames and weak measures, preserving both exact ambient pushforward identities.',
   'Whole MGExists with all five Haar entries, arbitrary degenerate tuple stabilizers, full split equality and all three specified original-measure ties.',
   'Whole generic MWCore with all eight entries and eleven normalization clauses, retaining the two prescribed infinity measures exactly.',
   'Whole MExistsCore and MExists for every D and every original antecedent block, one bridge for every word, exact actual frame and all five MeasTie equalities; no added gap or Bessel/Siegel–Weil premise.',
   'Whole general exists_haar_map_prod_eq, prescribing the first factor and the global measure by scaling only the second factor.',
   'Whole exists_measW_prescribed, retaining both infinity measures, both global measures and the whole local S-measure family with all original normalization clauses.',
   'Full nsub_cocompact for the exact rational subgroup; explicit central-coordinate compact representative construction, including r=0.',
   'Full original universal unipotent covolume-one measure theorem, with explicit Borel transversal, positivity, finiteness and choice-independent source covolume.',
   'Simultaneous prescribed infinity/global-H/local-S measures and unipotent covolume one on one MeasW, with exact existing infinity ties preserved for every word; remaining orbital/fiber identities explicit.'
  ],
  'foundations':[
   {'id':'AMD_HAAR_ANALYSIS','kind':'standard_mathematical_background','statement':'Existence and finite-positive-scalar uniqueness of Haar measure on locally compact groups, Haar products and pushforwards under topological group isomorphisms, Tonelli integration, and the local analytic derivative formula for the modulus of an automorphism. The weak source predicate, relevant unimodularity/action moduli, exact subgroups, product normalizations and covolume are proved explicitly in AMD4–17.'},
   {'id':'AMD_ALGEBRA_BACKGROUND','kind':'standard_mathematical_background','statement':'Finite-dimensional tensor algebra, finite projective number-field lattices and their completions, polynomial matrix exponential/logarithm in characteristic zero, nilpotent Lie-algebra central flags, and the additive Chinese remainder theorem. The actual adelic splitting, coordinate topology, group structure and compact representative induction are given in the numbered proofs.'},
   {'id':'AMD_ORIGINAL_INPUTS','kind':'original_contract_inputs','statement':'Exactly the original AutInst/CM/Hermitian/standard-frame data and the given Haar or IsHaarOnSet measures where the source quantifies them. AMD12 takes the original antecedent blocks of MExists; it does not require independently producing their Bessel block.'},
   {'id':'AMD_RESCALING_BOUNDARY','kind':'retained_original_consumer_premises','statement':'Only the final rescaling interpretation retains the original compatible orbital measures, normalized local fiber measures and Siegel–Weil premise. These are not hypotheses added to MGExists, MWCore, InfTransfer, MExists, prescribed extension or unipotent covolume one.'}
  ],
  'external':{1:['AMD_ALGEBRA_BACKGROUND','AMD_ORIGINAL_INPUTS'],2:['AMD_ALGEBRA_BACKGROUND','AMD_ORIGINAL_INPUTS'],3:['AMD_ALGEBRA_BACKGROUND','AMD_ORIGINAL_INPUTS'],8:['AMD_HAAR_ANALYSIS'],13:['AMD_HAAR_ANALYSIS'],17:['AMD_HAAR_ANALYSIS','AMD_ORIGINAL_INPUTS','AMD_RESCALING_BOUNDARY']},
  'default_external':['AMD_HAAR_ANALYSIS','AMD_ALGEBRA_BACKGROUND','AMD_ORIGINAL_INPUTS'],
  'completed':[
   'Full original AdelicIsomorphism: actual bridge, rational points and original compact conditions',
   'Full original MGExists, MWCore, InfTransfer and guarded MWExistsStd',
   'Full original MExistsCore and MExists with every literal same-bridge MeasTie equality',
   'Full original exists_haar_map_prod_eq and exists_measW_prescribed',
   'Full original nsub_cocompact and unipotent covolume-one Haar theorem',
   'Simultaneous covolume-one and prescribed infinity/global-H/local-S normalization portion of original RescaleStep3'
  ],
  'not_claimed':[
   'Original nonzero normalized Bessel W block or its decay/nonvanishing/uniqueness producers',
   'Remaining Siegel–Weil compatible orbital/stabilizer and normalized local fiber comparisons',
   'Witt/genus/level/representation transport to the arithmetic columns',
   'Full common spectral family, actual CountIdempotentsClass or any whole global leaf closure',
   'Complete RH or GRH'
  ],
  'endpoint':'AMD12'
 }
}

baseline=json.loads((ROOT/'history/version_0_47/provenance.json').read_text())
known={c['id']:c for c in baseline['claims']}
for name,cfg in DATA.items():
 here=ROOT/name
 raw=(here/'main.tex').read_bytes(); txt=raw.decode()
 groups={}; inventory={}; excerpts=[]
 for group,specs in cfg['groups'].items():
  records=[]
  for j,(path,start,end,desc) in enumerate(specs,1):
   data=(SRC/path).read_bytes()
   assert data==subprocess.check_output(['git','-C',str(SRC),'show',PIN+':'+path])
   lines=data.splitlines(keepends=True);end=end or len(lines)
   assert 1<=start<=end<=len(lines),(path,start,end,len(lines))
   part=b''.join(lines[start-1:end])
   rec={'id':f'{cfg["prefix"]}_{group}_{j:02}','path':path,'line_start':start,'line_end':end,'declaration':desc,'file_sha256':sha(data),'range_sha256':sha(part),'range_bytes':len(part),'source_commit':PIN,'verified_equal_to_pinned_git_blob':True,'url':f'https://github.com/CocoSgt/riemann-hypothesis-lean/blob/{PIN}/{path}#L{start}-L{end}'}
   records.append(rec);inventory[path]={'path':path,'sha256':sha(data),'bytes':len(data),'line_count':len(lines),'verified_equal_to_pinned_git_blob':True}
   excerpts.append(f'[{rec["id"]}] {path}:{start}-{end}\nRange SHA256 {sha(part)}\n{part.decode()}\n')
  groups[group]=records
 claims=[]
 for n in range(1,cfg['count']+1):
  cid=cfg['prefix']+str(n)
  match=re.search(r'% BEGIN '+cid+r'\n.*?% END '+cid+r'\n',txt,re.S);assert match,cid
  title=re.search(r'\\paragraph\{'+cid+r'\. (.*?)\}\n',match.group(),re.S).group(1)
  block=match.group().encode(); ext=cfg['external'].get(n,cfg['default_external'])
  claims.append({'id':cid,'title':title,'introduced_in':'0.48','classification':'A' if n in cfg['A'] else 'B','status':'complete human proof at the explicitly stated original scope','depends_on':cfg['deps'][n],'external_input_ids':ext,'published_input_ids':[x for x in ext if x in {'RFD_HARISH_CHANDRA','ASG_CLASS_FIELD_CHEBOTAREV'}],'scope_note':cfg['scopes'][n-1],'source_groups':cfg['claim_groups'][n],'sources':[s for g in cfg['claim_groups'][n] for s in groups[g]],'proof_location':{'file':name+'/main.tex','label':'claim:'+cid,'line_start':txt[:match.start()].count('\n')+1,'line_end':txt[:match.end()].count('\n'),'sha256':sha(block),'bytes':len(block)},'source_proof_is_not_human_proof':True})
 inherited=[]
 for cid in sorted({d for c in claims for d in c['depends_on'] if not d.startswith(cfg['prefix'])}):
  c=known[cid];loc=c['proof_location'];data=(ROOT/loc['file']).read_bytes();part=b''.join(data.splitlines(keepends=True)[loc['line_start']-1:loc['line_end']]);h=loc.get('sha256',loc.get('paragraph_sha256'))
  assert h in {sha(part),sha(part.rstrip(b'\r\n'))},(cid,'inherited proof hash')
  inherited.append({'id':cid,'file':loc['file'],'main_tex_sha256':sha(data),'block_sha256':sha(part),'recorded_baseline_hash':h,'line_start':loc['line_start'],'line_end':loc['line_end'],'kind':'numbered_human_proof_dependency','not_an_external_foundation':True,'introduced_in':c.get('introduced_in')})
 known.update({c['id']:c for c in claims})
 reviews=[{'file':str(p.relative_to(ROOT)),'sha256':sha(p.read_bytes())} for p in sorted(here.glob('review_*.json'))]
 prov={'schema':'rh-human-component-provenance/1','artifact_version':'0.48','date':'2026-11-23','component':name,'source_commit':PIN,'main_tex_sha256':sha(raw),'proof_file_sha256':sha(raw),'claims':claims,'source_groups':groups,'source_inventory':list(inventory.values()),'source_files':list(inventory),'retained_foundations':cfg['foundations'],'inherited_human_inputs':inherited,'independent_reviews':reviews,'builder':{'file':'../build_root_components_v0_48.py','sha256':sha(Path(__file__).read_bytes())},'validation':{'source_checkout_pin_verified':True,'all_source_bytes_compared_to_pinned_git_blobs':True,'claim_blocks':len(claims),'external_foundations_separate_from_claim_DAG':True,'inherited_human_proof_hashes_checked':True,'no_lean_replay':True}}
 contracts={'schema':'rh-root-producer-contracts/1','artifact_version':'0.48','component':name,'source_commit':PIN,'proof_file_sha256':sha(raw),'endpoint_claim':cfg['endpoint'],'completed_original_substatements':cfg['completed'],'not_claimed':cfg['not_claimed'],'proposed_whole_obligation_closures':[],'whole_obligation_closures':[],'no_lean_replay':True}
 for fn,obj in [('provenance.json',prov),('contracts.json',contracts),('classical_inputs.json',{'component':name,'artifact_version':'0.48','foundations':cfg['foundations']})]:
  (here/fn).write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n')
 (here/'source_excerpt.txt').write_text('\n'.join(excerpts))
 (here/'README.txt').write_text(name+' — version0.48\n\n'+str(len(claims))+' numbered human proofs.\n\nCOMPLETED ORIGINAL SUBSTATEMENTS\n'+'\n'.join('- '+x for x in cfg['completed'])+'\n\nEXACT BOUNDARY\n'+'\n'.join('- '+x for x in cfg['not_claimed'])+'\n\nNo Lean build or kernel replay. Source bytes and inherited human proofs are hash-bound.\n')
 report=[name+' — mathematical scope and source report','Version0.48; 23 November2026','',
  'The complete human proofs are in main.tex. This report records their exact scope, retained foundations and independent review bindings.','',
  'PROVED CLAIMS']
 for c in claims:report += [c['id']+' ['+c['classification']+']: '+c['scope_note']]
 report+=['','RETAINED FOUNDATIONS AND ORIGINAL PREMISES']
 for f in cfg['foundations']:report += [f['id']+' ('+f['kind']+'): '+f['statement']]
 report+=['','COMPLETED ORIGINAL ENDPOINTS']+cfg['completed']+['','BOUNDARY']+cfg['not_claimed']
 report+=['','PROVENANCE',f'{len(inventory)} pinned source files; {sum(len(x) for x in groups.values())} exact source ranges; {len(inherited)} inherited human proof bindings.',
  'Source commit: '+PIN,'Proof SHA256: '+sha(raw),'','INDEPENDENT REVIEWS']
 report += [x['file']+' — SHA256 '+x['sha256'] for x in reviews]
 report += ['','The hash bindings record the exact inspected text. They are not a formal replay or a substitute for the mathematical arguments.']
 (here/'report.txt').write_text('\n'.join(report)+'\n')
 print(json.dumps({'component':name,'claims':len(claims),'A':len(cfg['A']),'proof_sha256':sha(raw),'source_files':len(inventory),'source_ranges':sum(len(x) for x in groups.values()),'inherited_inputs':len(inherited)}))
