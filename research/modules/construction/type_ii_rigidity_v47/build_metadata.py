#!/usr/bin/env python3
"""Rebuild the exact Kato/type-II component; no common or frozen files are edited."""
from pathlib import Path
import argparse,hashlib,json,re,subprocess
HERE=Path(__file__).resolve().parent; ROOT=HERE.parent
PIN='7cbf7a0c32fca1badf05931879a37c3f8a2b03b4'; VERSION='0.47'; PREFIX='KTR'; COMPONENT=HERE.name
ap=argparse.ArgumentParser();ap.add_argument('--repo',type=Path,required=True);repo=ap.parse_args().repo.resolve()
sha=lambda b:hashlib.sha256(b).hexdigest()
AV='src/Development/AutomorphicArithmetic/AutomorphicVarieties/'
U=AV+'UnitaryThreeGroups/'; Z=AV+'ModularityArgument/KatoQuadraticCharacters/'; P=AV+'PadicHodgeTheory/'; AF=AV+'AutomorphicForms/'
specs={
 'kato_original':(Z+'KatoTwoOfUseN.lean',11,53,'Full Used, KatoTwo and literal RigII original contracts'),
 'inpz':(Z+'KatoTwoOfUseN.lean',55,61,'Separate InpZ record; not assembled in this packet'),
 'kato_use':(U+'KatoUse.lean',13,18,'Original full finite-cyclotomic-character KatoUse'),
 'cohinp':(U+'KatoUse.lean',20,34,'Original cohomological and literature input scope'),
 'onechar':(U+'KatoUse.lean',54,64,'Separate original OneChar endpoint remains outside this closure'),
 'newform':(AF+'Newform.lean',12,48,'Exact normalized newform, polynomial and semisimple all-prolongations attachment'),
 'level':(AF+'BlochKatoSelmerVanishes.lean',65,116,'Source KillsMu, geometric algebraic Satake and continuous Level'),
 'selmer':(AF+'BlochKatoSelmerVanishes.lean',117,144,'Graph decomposition group and full actual cocycle/primitive Selmer definition'),
 'gd':(AV+'HeightAndVanishing/Counts.lean',9,26,'Original arithmetic GD fields and exact small-prime guards'),
 'datum':(U+'RhoKApply.lean',16,59,'Original Dat and local Dat3 coefficients/characters/embedding'),
 'point':(U+'RhoKApply.lean',61,92,'Kill, actual local point, IsExt and IsModular'),
 'shape':(U+'BaseRepGL3NormalisedOfPsiEqOne.lean',11,34,'TypeII, corner representation and original Wfun'),
 'marks':(U+'BaseRepGL3NormalisedOfPsiEqOne.lean',68,73,'Original marked complex conjugation and residual generic element'),
 'ad_action':(U+'UnitaryThreeReflectionRight.lean',1,227,'Disconnected GG action and full adRep with inverse transpose'),
 'normalised':(U+'UnitaryThreeReflectionRight.lean',272,292,'Actual Normalised predicate, including matrix at complex conjugation'),
 'local_ideals':(P+'IsInertiaInfiniteCyclotomic.lean',87,138,'Ordered ordinary ideal, saturation, radical and It intersection'),
 'local_data':(P+'IsInertiaInfiniteCyclotomic.lean',1,85,'Dat3 and local HL kernel guards'),
 'matrix_flag':(P+'CommutingUpperTriangularDistinct.lean',15,83,'Explicit distinct-diagonal and ordered-three-product linear algebra'),
 'completion':(U+'DatLoc.lean',1,None,'Actual embedding gives local decomposition/inertia and cyclotomic compatibility'),
 'point_facts':(U+'DatFacts.lean',1,None,'Residual point, local and character facts behind exact original producer'),
 'middle':(U+'ClsEqOne.lean',1,None,'Original middle/determinant class-group triviality target'),
 'cyclotomic':(U+'TypeIIrrCyc.lean',1,None,'Original infinite-cyclotomic irreducibility target'),
 'extension':(U+'ReducibleThreeDim.lean',1,None,'Original actual TypeII rank-two extension consumer'),
 'primitive_maps':(Z+'ReducibleThreeDim.lean',17,55,'Continuous equivariant maps preserve every IsBK witness'),
 'decomposition':(Z+'ReducibleThreeDim.lean',57,264,'Exact original pA,sA,pB,sB,pC and nine-coordinate action'),
 'rigidity_producer':(Z+'ReducibleThreeDim.lean',265,None,'Original rigII_of producer and its four vanishing inputs'),
 'scalar':(U+'BlochKatoNonpositiveWeight.lean',1,None,'Original scalar finite-character nonpositive-weight vanishing route'),
 'autq':(AF+'Hypotheses2.lean',1,None,'Original named classical/period literature foundation boundary'),
}
relations={
 1:(['ADK1','ADK5','BX1','DX1'],['selmer','primitive_maps','cohinp']),
 2:([1,'CAP6','RNC2'],['newform','kato_original','kato_use']),
 3:([1,2],['kato_original','kato_use','level']),
 4:([],['gd','datum','point','local_data','local_ideals','matrix_flag','completion']),
 5:([4],['gd','point','point_facts','middle']),
 6:([5],['datum','point','shape','marks','normalised','ad_action','extension']),
 7:([],['cyclotomic']),
 8:([4,5,6,7,'ADK2'],['cyclotomic','shape','point','completion']),
 9:([6,'RNC2','CAP6','ADK3'],['newform','point','autq']),
 10:([1,6,8,9,'ADK3','ADK4','ADK5','ADK6'],['ad_action','rigidity_producer','autq']),
 11:([1,3,'BX7'],['scalar','selmer']),
 12:([6,10],['ad_action','decomposition']),
 13:([1,2,3,4,5,6,8,9,10,11,12],['kato_original','point','rigidity_producer','onechar']),
}
ext_uses={1:['KTR_COHOMOLOGY','KTR_PERIOD'],2:['KTR_KATO','KTR_NEWFORM'],3:['KTR_STANDARD'],4:['KTR_LOCAL_GALOIS','KTR_STANDARD'],5:['KTR_CFT','KTR_STANDARD'],6:['KTR_STANDARD'],7:['KTR_STANDARD'],8:['KTR_LOCAL_GALOIS','KTR_STANDARD'],9:['KTR_BASECHANGE','KTR_BLGGT_THORNE','KTR_CFT','KTR_NEWFORM'],10:['KTR_BLGGT_THORNE','KTR_PERIOD'],11:['KTR_CFT','KTR_COHOMOLOGY','KTR_PERIOD'],12:['KTR_STANDARD'],13:['KTR_STANDARD']}
config={
 'component':COMPONENT,'prefix':PREFIX,'endpoint_claim':'KTR13','original_endpoint':'UpperTheory.V.Z.Kato.RigII','additional_original_endpoints':['UpperTheory.V.Z.Kato.KatoTwo','UpperTheory.V.U3.KatoUse'],
 'subcontracts':[{'id':'finite_coefficient_and_local_condition_comparison','claim':'KTR1'},{'id':'noncentral_critical_Kato_application','claim':'KTR2'},{'id':'literal_KatoUse_and_KatoTwo','claim':'KTR3'},{'id':'actual_It_ordered_inertia_flag','claim':'KTR4'},{'id':'middle_and_determinant_characters_trivial','claim':'KTR5'},{'id':'actual_original_rank_two_extension','claim':'KTR6'},{'id':'two_dimensional_abelian_quotient_selftwist','claim':'KTR7'},{'id':'full_infinite_cyclotomic_irreducibility','claim':'KTR8'},{'id':'actual_cuspidal_quadratic_base_change','claim':'KTR9'},{'id':'complete_polarized_corner_adjoint_vanishing','claim':'KTR10'},{'id':'quadratic_scalar_Selmer_vanishing','claim':'KTR11'},{'id':'actual_nine_dimensional_equivariant_decomposition','claim':'KTR12'},{'id':'literal_RigII','claim':'KTR13'}],
 'hypotheses':['For KatoUse: every original odd ell, closure, fixed iota, e>=1, normalized f of weight2e+1, continuous W with original f.Att(W*epsilon^-e), every M>=1 and every KillsMu(M,phi).','For KatoTwo: every original Used record in full, then every fixed iota/newform attachment; no extra condition is imposed.','For RigII: original Dat with full GD, ULoc, marked g1, actual IsPt and TypeII, and exact universal IsExt=>IsModular premise. No automorphy conclusion is inferred without that original premise.'],
 'quantifier_order':['original ell and algebraic closure/coefficient data','original imaginary quadratic K, all GD data/e/N/psi/Dat/ULoc/marked g1','the actual IsPt r','the fixed iota and original TypeII/modularity implication','every continuous full-adjoint IsBK cocycle','an actual algebraic-closure-valued global primitive'],
 'normalizations':{'Frobenius':'geometric F_p = inverse of source arithmetic Frobenius; epsilon(F_p)=p^-1','Kato':'V_f has polynomial X^2-a_p X+chi(p)p^(2e); W=V_f(e), r=e,k=2e+1','local_subgroup':'J=I_ell intersect ker(tau), where tau^2=1; ordIdeal subset It; ordered diagonal(epsilon^e,1,epsilon^-e)','extension':'W(g)=corner(R(g))*diag(-1,1)^((1-eta(g))/2); W(c)=diag(-1,1),detW=eta','automorphic':'pi=unitary newform adelization*|det|^(1/2); algSat2=q^(1/2)*Satake; full quadratic base change at split/inert places','polarization':'J2 symmetric; W(h)^t J2 W(chc^-1)=J2; adjoint(c)X=-J2 X^t J2','decomposition':'ad(r)=A+W+(W*eta)+eta, dimensions4+2+2+1; primitive uses1/2 on each off-diagonal section'},
 'not_claimed':['the full local crystalline-component theorem from the stronger original route','OneChar length producer','AutUnramCoef actual automorphy producer','full InpZ assembly','completion of RH or GRH'],
 'report':'KTR1-KTR13 prove full original KatoUse, KatoTwo and RigII. Kato Theorem14.2(1) is matched at r=e,k=2e+1, with exact source Frobenius and local conditions. A smaller local argument uses ordIdeal subset It directly on I intersect ker(tau), then residual prime-to-ell and class-number hypotheses to trivialize actual middle/determinant characters. The actual W extension is constructed and proved irreducible on the full infinite cyclotomic kernel. Its given modularity supplies a newform; precisely matched quadratic GL2 base change and Thorne give the complete corner adjoint. Explicit projections/sections split all nine source adjoint coordinates into A,W,W*eta,eta and recombine actual Selmer primitives. No Kato, AdVanishQ or NewformAut producer is left opaque. Original modularity, tied period, finite-cohomology and named classical foundations remain explicit. OneChar and AutUnramCoef are not closed.'}

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
  if r['id'] in lookup or r['id'] not in {'CAP6','BX1','BX7','DX1'}:continue
  loc=r['proof_location'];f=ROOT/loc['file'];data=f.read_bytes();block=b''.join(data.splitlines(keepends=True)[loc['line_start']-1:loc['line_end']]);assert sha(block)==loc['sha256'],r['id']
  lookup[r['id']]={'claim':r['id'],'file':loc['file'],'file_sha256':sha(data),'claim_sha256':sha(block),'line_start':loc['line_start'],'line_end':loc['line_end']}
 local={PREFIX+str(i) for i in relations};claims=[];inherited={}
 for i,(deps,ss) in relations.items():
  cid=PREFIX+str(i);m=re.search(r'% BEGIN '+cid+r'\n.*?% END '+cid+r'\n',txt,re.S);assert m,cid
  ds=[PREFIX+str(d) if isinstance(d,int) else d for d in deps];assert set(ds)<=set(lookup),(cid,set(ds)-set(lookup))
  for dep in set(ds)-local:inherited[dep]={**lookup[dep],'kind':'immutable_inherited_human_proof','newly_modified_by_this_component':False}
  start=txt[:m.start()].count('\n')+1
  claims.append({'id':cid,'title':re.search(r'\\paragraph\{'+cid+r'\. (.*?)\}\n',m.group(),re.S).group(1),'introduced_in':VERSION,'classification':'A' if i in (2,9) else 'B','depends_on':ds,'external_input_ids':ext_uses.get(i,[]),'proof_location':{'file':COMPONENT+'/main.tex','label':'claim:'+cid,'line_start':start,'line_end':start+m.group().count('\n')-1,'sha256':sha(m.group().encode()),'bytes':len(m.group().encode())},'sources':[sources[k] for k in ss],'source_proof_is_not_human_proof':True})
 refs={}
 for c in claims:
  if c['id'] in refs:c['non_premise_reference_explanations']=refs[c['id']]
 external=json.loads((HERE/'classical_inputs.json').read_text())['inputs'];all_ext={e['id'] for e in external};assert all(set(c['external_input_ids'])<=all_ext for c in claims)
 for e in external:e['kind']='retained_named_classical_foundation';e['newly_reconstructed']=False;e['original_source_scope']=[sources['kato_original']]
 reviews=[];paths=list(HERE.glob('review_*.json'));rp=ROOT/'reviews_v0_47'/f'{COMPONENT}_root_review.json'
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
 closure={'schema':'rh-human-component-closure/1','component':COMPONENT,'artifact_version':VERSION,'source_commit':PIN,'proof_file_sha256':main_sha,'status':status,'closed_subcontracts':config['subcontracts'],'proposed_global_frontier_leaf_closures':[{'id':'RIG_II','claim':'KTR13','scope':'Complete original RigII implication, retaining its universal IsExt-to-IsModular hypothesis exactly; all four vanishing producers and the actual extension are supplied. Root alone records selected-frontier closure.'}],'new_global_frontier_leaf_closures':[],'foundation_retention_explicit':True,'independent_reviews':reviews,'validation':'Two-pass standalone draft TeX; no Lean replay; hash-bound independent mathematical/source reviews as listed.','pending':sorted(local-reviewed),'OneChar_and_AutUnramCoef_remain_separate':True}
 manifest={'schema':'rh-source-manifest/1','component':COMPONENT,'source_commit':PIN,'files':list(files.values()),'ranges':list(sources.values())}
 for name,obj in [('contracts.json',contracts),('original_contracts.json',contracts),('provenance.json',prov),('closure.json',closure),('source_manifest.json',manifest),('retained_foundations.json',external)]: (HERE/name).write_text(json.dumps(obj,indent=2)+'\n')
 (HERE/'source_excerpts.txt').write_text('\n\n'.join(excerpts))
 (HERE/'report.txt').write_text(COMPONENT+' v'+VERSION+'\n\n'+config['report']+'\n\nTwo checked published applications A (KTR2,KTR9), eleven explicit human claims B. External classical foundations are separate from the numbered mathematical DAG. The actual OneChar length argument and AutUnramCoef remain separate. No historical proof or common metadata was edited.\n\nRebuild: python build_metadata.py --repo /path/to/formal_source\nValidate: python validate_tex.py --format /path/to/pdflatex.fmt\n\n'+f'Pin: {PIN}\nMain SHA256: {main_sha}\nStatus: {status}\nClaims: {len(claims)}; source files: {len(files)}; ranges: {len(sources)}\n')
 hashes={p.name:sha(p.read_bytes()) for p in sorted(HERE.iterdir()) if p.is_file() and p.name!='hashes.json'};(HERE/'hashes.json').write_text(json.dumps({'component':COMPONENT,'artifact_version':VERSION,'hashes':hashes},indent=2)+'\n')
 print(json.dumps({'component':COMPONENT,'claims':len(claims),'source_files':len(files),'source_ranges':len(sources),'inherited_bindings':len(inherited),'main_sha256':main_sha,'status':status},indent=2))
build()
