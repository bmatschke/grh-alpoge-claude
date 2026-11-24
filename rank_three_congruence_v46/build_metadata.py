#!/usr/bin/env python3
"""Rebuild the bounded-rank CNR3 reconstruction; no common or frozen output is edited."""
from pathlib import Path
import argparse,hashlib,json,re,subprocess
HERE=Path(__file__).resolve().parent; ROOT=HERE.parent
PIN='7cbf7a0c32fca1badf05931879a37c3f8a2b03b4'; VERSION='0.46'; PREFIX='RNC'; COMPONENT=HERE.name
ap=argparse.ArgumentParser();ap.add_argument('--repo',type=Path,required=True);repo=ap.parse_args().repo.resolve()
sha=lambda b:hashlib.sha256(b).hexdigest()
AV='src/Development/AutomorphicArithmetic/AutomorphicVarieties/'
AF=AV+'AutomorphicForms/'; TL=AF+'TemperedLocalComponents/'; BR=AV+'BuildingsResidueChars/'
SL=AV+'ModularityArgument/SemisimpleLevels/'; AB='src/Development/AbelianVarietyTheory/'
specs={
 'target':(AF+'CongruenceNumberRankThree.lean',125,140,'Literal original CNR3 quantifiers and both output clauses'),
 'admissible':(AF+'CongruenceNumberRankThree.lean',107,121,'Exact Adm3, Adm2 and eis3'),
 'eigen':(AF+'CongruenceNumberRankThree.lean',56,92,'EigData and Classifies; original CountK/CountQ contracts, not assumed'),
 'level':(AF+'BlochKatoSelmerVanishes.lean',65,116,'KillsMu, FrobEig, algSat, IsAutCsd and literal LevelAt disjunction'),
 'newform':(AF+'Newform.lean',12,48,'Original newform, Hecke polynomial and weak attachment'),
 'newformrep':(AV+'PublishedTheorems/GelfandKazhdanReal.lean',159,164,'Original NewformRep contract; only j=e is used here'),
 'newformaut':(TL+'NewformAut.lean',37,113,'Exact twist/charpoly transport and actual NewformAutR producer'),
 'hyp':(AF+'Hypotheses2.lean',1,None,'Original named literature and period hypothesis bundle'),
 'galq':(AV+'ModularityArgument/BaseChangeUnits/GaloisRepRankTwoRealOf.lean',12,19,'Original rank-two totally real automorphic Galois input'),
 'ss':(SL+'CsdSsOfFull.lean',38,None,'Original semisimple coefficient-prime comparison scope'),
 'mono':(SL+'SsMonoOdd.lean',17,None,'Original odd-rank monodromy comparison scope'),
 'monoprod':(SL+'MonoOddOf.lean',29,None,'Finite-dimensional monodromy and comparison with actual supplied representation'),
 'levelko':(SL+'LevelKO.lean',89,None,'Exact odd-rank level producer and its LevelAt alternatives'),
 'flag':(SL+'FlagPol.lean',1,None,'Literal ordinary flag Weil character formula and cyclotomic ratio detection'),
 'levelcontracts':(SL+'CountRankThree.lean',86,126,'FlagPol, finite inertia, local fixed and no-ratio contracts'),
 'away':(TL+'WDAway.lean',1,None,'Away local inertia/WD comparison'),
 'above':(TL+'WDAbove.lean',1,None,'Coefficient-prime flag/WD comparison'),
 'jumps':(TL+'JumpsAbove.lean',1,None,'Original flag-to-Hodge weight computation'),
 'satfrob':(TL+'SatFrob.lean',1,None,'Full original prolongation/Frobenius normalization'),
 'countdef':(AF+'IsoOfFrob.lean',11,91,'Infinity/cusp label/count/conjugation/purity/slopes/actual level interfaces'),
 'countk':(TL+'CountK.lean',1,None,'Original full-system classifier construction'),
 'cells':(TL+'CohBoundFree.lean',65,99,'Fixed arithmetic cohomology and principal-level index bound'),
 'cardk':(TL+'KlevThree.lean',1,None,'Level-three cohomology counting consumer'),
 'conj':(TL+'EventuallyNotMem.lean',41,55,'Original automorphic conjugation catalogue consumer'),
 'pury':(TL+'PureK.lean',1,None,'Pure geometric roots under source normalization'),
 'intk':(TL+'IntK.lean',1,None,'Original all-coefficient-prime integral root producer'),
 'slopes':(AF+'Slopes.lean',62,None,'All-prime integral criterion and crystalline slope consumer'),
 'crys':(TL+'CrysSlopes.lean',1,None,'Crystalline interval-to-eigenvalue bounds'),
 'trace3':(BR+'FrobeniusTraceCountBoundOfCmEigensystemCount.lean',1,None,'Original rank-three cyclotomic shift and classifier'),
 't3':(BR+'TracesFromEigenvaluesRank3.lean',1,None,'Exact q-scaled inverse-root trace'),
 'trace2':(BR+'FrobeniusTraceCountBoundOfRatEigensystemCount.lean',1,None,'Original rank-two block/restriction classifier'),
 't2':(BR+'TracesFromEigenvaluesRank2.lean',1,None,'Exact residue-degree power trace plus1'),
 'classifies':(AF+'Classifies.lean',1,None,'Literal TrData, classifiers and disjoint-union construction'),
 'residue':(BR+'ExistsNormVEqPrimePowLeFinrank.lean',1,None,'Residue norm p^h with h bounded by degree'),
 'frobpower':(BR+'FrobeniusPowerCompatibility.lean',1,None,'Arithmetic Frobenius restriction and powers'),
 'sep':(BR+'EisensteinTraceDifferenceLogBound.lean',1,None,'Original nonzero integral factor and logarithmic bound'),
 'integer':(BR+'ExistsIntEqProdOfGaloisPermutedIntegral.lean',1,None,'Aut(C)-invariant integral product is a rational integer'),
 'select':(BR+'AdicNormProdLeProdOfInjectiveClasses.lean',1,None,'Injective finite-family norm-product selection'),
 'normprod':(BR+'FrobeniusTraceNormNonzeroLogBound.lean',1,None,'Exact whole indexed-orbit trace product consumer'),
 'producer':(TL+'CongruenceNumberRankThree.lean',14,None,'Original fixed c,A then all varying data CNR3 assembly'),
}
relations={
 1:([],['hyp','galq','ss','mono','level','countdef']),
 2:([],['newform','newformrep','newformaut','admissible']),
 3:([1,2,'ADK1','CAP6'],['level','admissible','jumps','levelko','satfrob']),
 4:([3,'ADK1'],['flag','levelcontracts','above']),
 5:([1,3,4],['level','levelko','away','above','monoprod']),
 6:(['HP1','HP2'],['cells','cardk','countdef']),
 7:([2,6],['conj','countdef','eigen','countk']),
 8:([1,7,'ADK1'],['pury','intk','slopes','crys','eigen']),
 9:([3,5,7,8,'CAP6'],['trace3','t3','satfrob','classifies']),
 10:([2,3,5,7,8,'CAP6'],['trace2','t2','frobpower','admissible']),
 11:([7,9,10],['classifies','residue','producer']),
 12:([],['sep','admissible']),
 13:([11,12],['integer','normprod']),
 14:([11,12,13],['select','normprod','target']),
 15:([6,11,13],['producer','residue','target']),
 16:([11,13,14,15],['target','admissible','producer']),
}
ext_uses={1:['RNC_BG','RNC_BGP','RNC_CFT'],2:['RNC_JL','RNC_SMO'],3:['RNC_BG','RNC_PH'],4:['RNC_PH'],5:['RNC_CFT','RNC_LL','RNC_NF','RNC_SMO'],6:['RNC_CL','RNC_BS','RNC_BLS','RNC_ANT'],7:['RNC_CL','RNC_SMO'],8:['RNC_BG','RNC_PH']}
config={
 'component':COMPONENT,'prefix':PREFIX,'endpoint_claim':'RNC16','original_endpoint':'UpperTheory.V.Af.CongruenceNumberRankThree','original_producer':'UpperTheory.V.Af.numberU3_of_admissible',
 'subcontracts':[{'id':'bounded_published_Galois_application','claim':'RNC1'},{'id':'actual_rank_two_newform_adelization','claim':'RNC2'},{'id':'same_actual_Galois_representation_and_weights','claim':'RNC3'},{'id':'exact_flag_norm_ratio_detection','claim':'RNC4'},{'id':'coefficient_independent_auxiliary_levels','claim':'RNC5'},{'id':'bounded_rank_uniform_cusp_counts','claim':'RNC6'},{'id':'AutC_stable_full_cusp_labels','claim':'RNC7'},{'id':'pure_and_integral_roots','claim':'RNC8'},{'id':'rank_three_trace_catalogue','claim':'RNC9'},{'id':'rank_two_restricted_block_trace_catalogue','claim':'RNC10'},{'id':'original_disjunctive_trace_catalogue','claim':'RNC11'},{'id':'nonzero_integral_Eisenstein_factors','claim':'RNC12'},{'id':'whole_indexed_orbit_integer','claim':'RNC13'},{'id':'all_later_coefficient_product_inequality','claim':'RNC14'},{'id':'fixed_uniform_constants','claim':'RNC15'},{'id':'literal_CNR3','claim':'RNC16'}],
 'hypotheses':['K is any original imaginary quadratic field; c,A depend only on K','e>=1,N>=1,p prime,p>=7,p does not divide N or discK; w above p','Any finite indexed family z of roots of unity with a permutation under every Aut(C), preserving multiplicity','After NN: every odd ell!=p including3, every original closure/scalar tower/iota/prolongation/arithmetic Frobenius','At each orbit index, a finite pairwise-nonisomorphic family satisfying original Adm3(e,N) OR Adm2(e,N*|discK|)'],
 'quantifier_order':['K','c,A','e,N,p,w,finite indexed roots-of-unity orbit','nonzero integer NN','ell,closures,scalar towers,iota,B,sigma','all families X(o)'],
 'normalizations':{'Frobenius':'sigma arithmetic; every trace is rho(sigma^-1)','algSat':'q^((n-1)/2)*normalized Satake is geometric; beta is its inverse','rank_three_twist':'r=rho*epsilon^-1; weights(e-1,-1,-e-1); r(geom)=q*rho(geom)','rank_three_trace':'sum_b (q*b)^-1','rank_two_trace':'1+sum_b b^-h, q=p^h, with original block positions0,2 and middle1','Eis':'q^-e*z+1+q^e*z^-1','factor':'q^e*(t-Eis)','auxiliary_levels':'N^5 and (N*|discK|)^3 only for the automorphic catalogues; Galois levels unchanged','constants':'A=103 and c=5*(c3+c2*|discK|^12), chosen with K'},
 'not_claimed':['all-rank CountK or CountQ','original OneChar producer or unconditional PropGK/CountI installation','uniform automorphy or monodromy beyond the two checked ranks/weights','completion of RH or GRH'],
 'report':'RNC1-RNC16 supply the literal original CNR3, with bounded-rank catalogue producers and the complete orbit integer argument. The proof replaces the source all-rank CountQ detour by the actual rank-two newform adelization over Q. The original LevelAt disjunction plus precisely matched Shin-regular local-global compatibility removes any coefficient-prime factor outside M. Finite cells and explicit polynomial coefficient ranks give catalogues at auxiliary levels M^5 and M^3. The same original Galois representations and levels are retained. Full cusp labels and all-Aut(C) conjugation precede the coefficient prime; the nonzero integer is the complete orbit-times-label product and works for every later pairwise-nonisomorphic family. The OneChar length producer remains separate.'}


def build():
 files={};sources={};excerpts=[]
 for key,(rel,start,end,title) in specs.items():
  data=(repo/rel).read_bytes();pinned=subprocess.check_output(['git','show',PIN+':'+rel],cwd=repo);assert data==pinned,rel
  ls=data.splitlines(keepends=True);end=end or len(ls);assert 1<=start<=end<=len(ls),(rel,start,end,len(ls));block=b''.join(ls[start-1:end]);url=f'https://github.com/CocoSgt/riemann-hypothesis-lean/blob/{PIN}/{rel}'
  files[rel]={'path':rel,'sha256':sha(data),'bytes':len(data),'line_count':len(ls),'verified_equal_to_pinned_git_blob':True,'url':url}
  sources[key]={'id':PREFIX+'_SRC_'+key.upper(),'path':rel,'declaration':title,'line_start':start,'line_end':end,'source_commit':PIN,'full_file_sha256':sha(data),'file_sha256':sha(data),'range_sha256':sha(block),'range_bytes':len(block),'verified_equal_to_pinned_git_blob':True,'url':url+f'#L{start}-L{end}'}
  excerpts.append(f'[{sources[key]["id"]}] {title}\n{sources[key]["url"]}\n'+block.decode())
 txt=(HERE/'main.tex').read_text();main_sha=sha(txt.encode());lookup={}
 for f in list(ROOT.glob('*/main.tex'))+list(ROOT.glob('*/adjoint_matching.tex')):
  text=f.read_text()
  for m in re.finditer(r'% BEGIN ([A-Z]+\d+)\n.*?% END \1\n',text,re.S):
   cid=m.group(1)
   if cid in lookup: assert lookup[cid]['claim_sha256']==sha(m.group().encode()),(cid,f)
   else: lookup[cid]={'claim':cid,'file':str(f.relative_to(ROOT)),'file_sha256':sha(f.read_bytes()),'claim_sha256':sha(m.group().encode()),'line_start':text[:m.start()].count('\n')+1,'line_end':text[:m.end()].count('\n')}
 # Immutable legacy claims do not all have BEGIN/END markers. Bind their exact recorded ranges.
 ledger=json.loads((ROOT/'provenance.json').read_text())
 for r in ledger['claims']:
  if r['id'] in lookup or r['id'] not in {'HP1','HP2','CAP6','ADK1'}:continue
  loc=r['proof_location'];f=ROOT/loc['file'];data=f.read_bytes();block=b''.join(data.splitlines(keepends=True)[loc['line_start']-1:loc['line_end']]);assert sha(block)==loc['sha256'],r['id']
  lookup[r['id']]={'claim':r['id'],'file':loc['file'],'file_sha256':sha(data),'claim_sha256':sha(block),'line_start':loc['line_start'],'line_end':loc['line_end']}
 local={PREFIX+str(i) for i in relations};claims=[];inherited={}
 for i,(deps,ss) in relations.items():
  cid=PREFIX+str(i);m=re.search(r'% BEGIN '+cid+r'\n.*?% END '+cid+r'\n',txt,re.S);assert m,cid
  ds=[PREFIX+str(d) if isinstance(d,int) else d for d in deps];assert set(ds)<=set(lookup),(cid,set(ds)-set(lookup))
  for dep in set(ds)-local:inherited[dep]={**lookup[dep],'kind':'immutable_inherited_human_proof','newly_modified_by_this_component':False}
  start=txt[:m.start()].count('\n')+1
  claims.append({'id':cid,'title':re.search(r'\\paragraph\{'+cid+r'\. (.*?)\}\n',m.group(),re.S).group(1),'introduced_in':VERSION,'classification':'A' if i==1 else 'B','depends_on':ds,'external_input_ids':ext_uses.get(i,[]),'proof_location':{'file':COMPONENT+'/main.tex','label':'claim:'+cid,'line_start':start,'line_end':start+m.group().count('\n')-1,'sha256':sha(m.group().encode()),'bytes':len(m.group().encode())},'sources':[sources[k] for k in ss],'source_proof_is_not_human_proof':True})
 refs={'RNC1':{'RNC2':'Later application check for rank-two essential self-duality; abstract RNC1 assumes the requisite polarized pair and does not use RNC2 conclusion.'},'RNC2':{'RNC1':'Consumer reference: the actual constructed cusp is verified to meet the RNC1 hypotheses; no RNC1 conclusion is used to construct it.'},'RNC6':{'CX1':'Method comparison only; the rank-four CX1 conclusion is not invoked for ranks2/3. The bounded finite-cell and coefficient proof is written here.'}}
 for c in claims:
  if c['id'] in refs:c['non_premise_reference_explanations']=refs[c['id']]
 external=json.loads((HERE/'classical_inputs.json').read_text())['inputs'];all_ext={e['id'] for e in external};assert all(set(c['external_input_ids'])<=all_ext for c in claims)
 for e in external:e['kind']='retained_named_classical_foundation';e['newly_reconstructed']=False;e['original_source_scope']=[sources['hyp']]
 reviews=[];paths=list(HERE.glob('review_*.json'));rp=ROOT/'reviews_v0_46'/f'{COMPONENT}_root_review.json'
 if rp.exists():paths.append(rp)
 for p in paths:
  v=json.loads(p.read_text());assert v.get('result',v.get('status'))=='PASS',p;ids=[]
  for e in v.get('claims_reviewed',v.get('reviewed_claims',[])):
   cid=e if isinstance(e,str) else e.get('id',e.get('claim'));assert cid in local,(p,cid)
   expected=v.get('proof_hashes',{}).get(cid) if isinstance(e,str) else e.get('proof_range_sha256',e.get('block_sha256'))
   assert expected==lookup[cid]['claim_sha256'],(p,cid,'stale reviewed block');ids.append(cid)
  reviews.append({'file':str(p.relative_to(ROOT)),'sha256':sha(p.read_bytes()),'reviewer':v.get('reviewer'),'result':'PASS','reviewed_proof_file_sha256':v.get('proof_sha256',v.get('proof_file_sha256')),'proof_file_sha256':main_sha,'reviewed_blocks_unchanged':True,'claims':ids,'scope':v.get('scope')})
 reviewed={c for r in reviews for c in r['claims']};status='complete_at_stated_scope_independently_reviewed' if local<=reviewed else 'complete_at_stated_scope_pending_independent_review'
 for c in claims:c['status']='complete_at_stated_scope_independently_reviewed' if c['id'] in reviewed else 'complete_at_stated_scope_pending_independent_review';c['independent_review_files']=[r['file'] for r in reviews if c['id'] in r['claims']]
 contracts={'schema':'rh-human-component-contract/1','artifact_version':VERSION,'source_commit':PIN,'proof_file_sha256':main_sha,**config,'retained_foundations':[e['id'] for e in external],'original_admissibility_not_weakened':True}
 prov={'schema':'rh-human-component-provenance/1','component':COMPONENT,'artifact_version':VERSION,'source_commit':PIN,'proof_file_sha256':main_sha,'status':status,'claims':claims,'inherited_human_inputs':list(inherited.values()),'classical_and_foundational_inputs':external,'independent_reviews':reviews,'dependency_convention':'depends_on contains numbered human claims only; classical foundations are named separately in external_input_ids. Non-premise references are explained explicitly.','source_proof_is_not_human_proof':True,'root_ledger_modified':False,'frozen_artifacts_modified':False}
 closure={'schema':'rh-human-component-closure/1','component':COMPONENT,'artifact_version':VERSION,'source_commit':PIN,'proof_file_sha256':main_sha,'status':status,'closed_subcontracts':config['subcontracts'],'proposed_global_frontier_leaf_closures':[{'id':'CNR3','claim':'RNC16','scope':'Complete original contract under its retained named classical and period foundations; subject to root integration review.'}],'new_global_frontier_leaf_closures':[],'foundation_retention_explicit':True,'independent_reviews':reviews,'validation':'Two-pass standalone draft TeX; no Lean replay; hash-bound independent mathematical/source reviews as listed.','pending':sorted(local-reviewed),'OneChar_and_unconditional_PropGK_remain_separate':True}
 manifest={'schema':'rh-source-manifest/1','component':COMPONENT,'source_commit':PIN,'files':list(files.values()),'ranges':list(sources.values())}
 for name,obj in [('contracts.json',contracts),('original_contracts.json',contracts),('provenance.json',prov),('closure.json',closure),('source_manifest.json',manifest),('retained_foundations.json',external)]: (HERE/name).write_text(json.dumps(obj,indent=2)+'\n')
 (HERE/'source_excerpts.txt').write_text('\n\n'.join(excerpts))
 (HERE/'report.txt').write_text(COMPONENT+' v'+VERSION+'\n\n'+config['report']+'\n\nThe mathematical classification is one checked published application A (RNC1), and fifteen explicit human-proof claims B. The original named classical foundations are separately registered and are not mathematical DAG nodes. No original source proof is used as the human proof. No old proof or shared metadata is edited. The CNR3 whole-leaf change is proposed here; only root integration records selected-frontier closure.\n\nRebuild: python build_metadata.py --repo /path/to/formal_source\nValidate: python validate_tex.py --format /path/to/project/pdflatex.fmt\n\n'+f'Pin: {PIN}\nMain SHA256: {main_sha}\nStatus: {status}\nClaims: {len(claims)}; source files: {len(files)}; ranges: {len(sources)}\n')
 hashes={p.name:sha(p.read_bytes()) for p in sorted(HERE.iterdir()) if p.is_file() and p.name!='hashes.json'};(HERE/'hashes.json').write_text(json.dumps({'component':COMPONENT,'artifact_version':VERSION,'hashes':hashes},indent=2)+'\n')
 print(json.dumps({'component':COMPONENT,'claims':len(claims),'source_files':len(files),'source_ranges':len(sources),'inherited_bindings':len(inherited),'main_sha256':main_sha,'status':status},indent=2))
build()
