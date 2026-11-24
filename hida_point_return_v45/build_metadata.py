#!/usr/bin/env python3
"""Rebuild this component's pinned sources, contracts and human proof graph."""
from pathlib import Path
import argparse, hashlib, json, re, subprocess
HERE=Path(__file__).resolve().parent
ROOT=HERE.parent
PIN='7cbf7a0c32fca1badf05931879a37c3f8a2b03b4'
ap=argparse.ArgumentParser();ap.add_argument('--repo',type=Path,required=True)
repo=ap.parse_args().repo.resolve()
sha=lambda b:hashlib.sha256(b).hexdigest()
AV='src/Development/AutomorphicArithmetic/AutomorphicVarieties/'
DT=AV+'ModularityArgument/ThresholdArguments/DenseThresholdCases/'
CD=AV+'ModularityArgument/CuspidalDescent/'
AL=AV+'ModularityArgument/AutomorphyLifting/'
BR=AV+'BuildingsResidueChars/'
AB='src/Development/AbelianVarietyTheory/'
specs={
 'target':(DT+'PointTheoremBaseObject.lean',26,39,'PointTheoremBaseObject and HidaPropsAlt'),
 'final':(DT+'HeckePolyCoeffZero.lean',1,None,'Original complete point-property wrapper'),
 'row':(DT+'JPTRow.lean',1,None,'Original RowT to jPT assembly'),
 'point':(DT+'DualOfWeights.lean',1,None,'Norm, no-linkage, jumps, reverse comparison and literal jPT producer'),
 'desc':(CD+'DescWeak.lean',10,21,'Exact retained low-rank weak descent contract'),
 'universal':(AV+'WeilGroupCharacters/UniversalOrdinaryDeterminantRing.lean',125,163,'Residual Ip, Pair, Maps and universal property'),
 'isco':(AV+'CommutativeAlgebra/ResMapBijective.lean',1,19,'Exact coefficient category IsCO'),
 'typepoint':(AV+'HeckeAlgebras/UpOperatorEigenvalues/WdCharpoly.lean',119,None,'diag_pt full original trace/type producer'),
 'ordchar':(AV+'PadicHodgeTheory/OrdCharIff.lean',1,None,'OrdChar equivalence and inverse finite-part identity'),
 'flagwd':(DT+'LocFlagWD.lean',1,None,'Every-bridge FlagWD supplier and exact scope'),
 'ps':(DT+'PseudoLocalLanglandsDescent.lean',1,None,'Support-polynomial reverse principal-series comparison'),
 'psirr':(DT+'TPsIrr.lean',1,None,'Totally disjoint principal-series irreducibility'),
 'plain':(AL+'PolarizedLinkage/PlainRec.lean',1,None,'Window/plain support and every-IsRecT zero-monodromy consumer'),
 'win':(AV+'ModularityArgument/LeviSmoothLocalization/WinUpDown.lean',1,47,'Literal TorAt and WinAt'),
 'unram':(DT+'EqOneOfUnr.lean',1,None,'Actual reverse unramified spherical statement'),
 'aut':(AL+'IsAutCsdA.lean',1,None,'AutCsd0 and WitA in IsAutCsdA'),
 'guard':(AL+'WeakOfAtt.lean',1,53,'Unl1, PotUnl, WitA and retained RowT'),
 'same':(DT+'TSameOf.lean',1,None,'Original cofinite split-to-full Same producer'),
 'js':(AB+'PublishedTheorems/GaloisCohomology₂/StrongMultiplicityOne.lean',189,197,'Retained JacquetShalikaRigidity exact isobaric family scope'),
 'fixed':(BR+'ExistsNonzeroFormFixedByLevelOfUnramified.lean',1,None,'Original compact-level fixed-vector producer'),
 'fixedlocal':(BR+'ExistsFixedVectorInLocallyStableSubspace.lean',1,None,'Original local-stable-subspace fixed-vector transfer'),
 'embedding_exhaustion':(BR+'PlaceEmbeddingsBijectiveInfinitePlaces.lean',68,None,'Original actual infinity-embedding exhaustion used in nonzero tensor dual construction'),
 'nonzero':(DT+'AbsoluteIrreducibleRankFour.lean',1,None,'Actual nonempty_unitary_hecke_parts all-rank coefficient function construction'),
 'eigenline':(DT+'OrdA.lean',1,None,'Finite eigenfunctional and exact principal-series ordinary eigenline'),
 'coreup':(DT+'TCoreUp.lean',1,None,'Actual local intersections, z normalization and coreUp_alt'),
 'unif':(DT+'UnifVal.lean',1,None,'Exact finite-part, unit and residual ordinary-eigenvalue normalization'),
 'eigpoint':(AV+'HeckeAlgebras/UpOperatorEigenvalues/EigChar.lean',1,None,'Original residual-block eigenpoint supplier'),
 'return':(DT+'UpUW.lean',34,None,'StrongEquivalenceHida, exact type consumer and full upU_w_alt'),
 'hecke':(DT+'UnitaryHeckeData.lean',27,74,'TypeForAlt, actual UnitaryPointProperties and IsJ'),
 'normalization':(AV+'HeckeAlgebras/Distinct.lean',1,None,'Original PS, psEig, htW and local ordinary definitions'),
 'literature':(DT+'LitAut.lean',12,63,'Original local and global foundations retained by HypothesesHprime'),
}
relations={
 1:(['ASP2'],['universal','isco']),
 2:(['GUA14'],['universal','typepoint','return']),
 3:(['OFL1'],['ordchar','normalization']),
 4:([3],['point','normalization']),
 5:([3,'OFL4','OFL12'],['flagwd','point']),
 6:([4,'OFL1'],['ps','psirr','normalization']),
 7:(['BCS5','GUA2'],['plain','win','unram']),
 8:([3,4,5,6,7,'GUA7','GUA10','GUA12','HED8','ADK1'],['aut','guard','point']),
 9:([8,'BCS18','BCS19','GUA14','GUA18','HED6','HED7','LTP3'],['same','js','desc']),
 10:(['LTP5'],['fixed','fixedlocal']),
 11:([10,'ITA2','ITA9','ITA11','ITA12','LTP3','LTP13','LTP16','ADP7','ADP8','ADP9'],['nonzero','hecke','embedding_exhaustion']),
 12:([],['eigenline']),
 13:([12,'OST5','OST26'],['eigenline','normalization']),
 14:([13,'LTP3','OST26','OST27'],['coreup']),
 15:(['ASP2','HEP4','HEP5','HEP6'],['unif','return']),
 16:([14,'OHA4','OHA5','OHA6','OHA8','ASP2','ASP13'],['eigpoint','coreup']),
 17:([1,2,3,11,14,15,16,'AFS8','ASP13','UPA16','GUA14','HEP1','HEP2','HEP7'],['return','hecke']),
 18:([2,7,8,9,17,'AFS8','LTP20','LTP21','GUA14'],['point','target','final','row','desc']),
}
external=[
 {'id':'HPT_ORIGINAL_DESCWEAK','kind':'retained_original_foundation','classification':'inherited','source_keys':['desc'],
  'statement_used':'HypothesesHprime.descU: E is CM, unramified over E+ at every finite place; p prime; finite S, all places above S split, every place above p under S; ranks2<=n<=4; actual regular algebraic CSD cusp spherical outside S. Output actual sigma, nonsplit unramifiedness, cofinite split Satake matching only. HPT9 proves the stronger consumer needed later.','newly_reconstructed':False},
 {'id':'HPT_ORIGINAL_LOCAL','kind':'retained_original_foundation','classification':'inherited','source_keys':['literature','plain','ps'],
  'statement_used':'Original local finite-length/support/multisegment/exhaustion, GenericUnlinkedGL and TotallyDisjointProductIrreducible with their different hypotheses, local Artin laws, full RecTExists/IsRecT and original smooth-representation foundations. Exactly the scope already retained by GUA/OFL/ITA.','newly_reconstructed':False},
 {'id':'HPT_ORIGINAL_ROW_PERIOD','kind':'retained_original_foundation','classification':'inherited','source_keys':['literature','guard','flagwd'],
  'statement_used':'Original RowT/PropsB as used in GUA7; original tied period models, rank-one comparison, de Rham subobject/quotient and strict filtered exactness, potential semistability, every-bridge coefficient descent, and away local monodromy, at the scope already recorded in GUA/OFL. The bounded flag and given-rho consumers are proved here.','newly_reconstructed':False},
 {'id':'HPT_ORIGINAL_JS','kind':'retained_original_foundation','classification':'inherited','source_keys':['js','literature'],
  'statement_used':'Original litN.aut.js.1, JacquetShalikaRigidity for two finite families of positive-rank cusps over a totally complex number field, cofinite all-place equality of Satake unions implies a bijection matching actual cuspidal classes. Not newly literature-matched here.','newly_reconstructed':False},
 {'id':'HPT_GENERAL_ALGEBRA','kind':'retained_general_foundation','classification':'inherited','source_keys':['universal','typepoint'],
  'statement_used':'Finite semisimple algebra decomposition/Brauer-Nesbitt, finite character independence, Haar averaging on compact smooth complex representations, finite local module completeness and elementary coefficient-field facts. Their actual trace, fixed-vector and point-uniqueness consumers are proved in HPT1/2/10/12/16.','newly_reconstructed':False},
]
ext_uses={1:['HPT_GENERAL_ALGEBRA'],2:['HPT_GENERAL_ALGEBRA','HPT_ORIGINAL_ROW_PERIOD'],3:['HPT_ORIGINAL_LOCAL'],5:['HPT_ORIGINAL_ROW_PERIOD'],6:['HPT_ORIGINAL_LOCAL'],7:['HPT_ORIGINAL_LOCAL'],8:['HPT_ORIGINAL_ROW_PERIOD','HPT_GENERAL_ALGEBRA'],9:['HPT_ORIGINAL_JS'],10:['HPT_GENERAL_ALGEBRA'],11:['HPT_ORIGINAL_LOCAL'],13:['HPT_ORIGINAL_LOCAL'],18:['HPT_ORIGINAL_DESCWEAK']}
config={
 'component':'hida_point_return_v45','prefix':'HPT','endpoint_claim':'HPT18',
 'original_endpoint':'B.PointTheoremBaseObject iota J','original_producer':'hecke_ideal_point_properties / JPTwA / JPTRow / jPT_of_alt',
 'subcontracts':[{'id':'nonempty_unitary_hecke_parts','claim':'HPT11'},{'id':'local_ordinary_eigenline','claim':'HPT13'},{'id':'coreUp_alt','claim':'HPT16'},{'id':'upU_w_alt','claim':'HPT17'},{'id':'PointTheoremBaseObject','claim':'HPT18'}],
 'hypotheses':['Original HypothesesHprime, HidaSetting, V.Sprime=s.S, same IsJ ideal and actual integral type/coefficients/fixed iota','Original ell odd, including3; UpUW n>=1; final pt only2<=n<=4','pt: x arithmetic, x.IsRep rho, rho continuous and IsAutCsdA, full inertia trivial at v0, ordered flags and no cyclotomic ratio at every chosen ell-place','No J<=ker x premise in HPT17 or HPT18'],
 'normalizations':{'PS':'normalized induction of omega_i*abs^((n-1)/2)','algNorm':'tau*absdet^((1-n)/2)','weights':'h_i=lambda(n-1-i)+i','Artin':'ord(a(s))=-degree(s)','ordinary_generators':'j+1=1..n','ordinary_z':'j=0..n-1, with j0 factor1','v0_depth':'original Kc1'},
 'not_claimed':['production of DescWeak, RowT, full local correspondence or tied period foundations','unrestricted-rank version of pt','new global selected-frontier closure','completion of RH or GRH'],
 'report':'HPT1-HPT18 prove whole-point uniqueness, trace/type recovery, exact reverse flag/local comparison, weak-descent upgrade, actual nonzero integral-type/infinity coefficient part, ordinary eigenline and residual Hecke point, the all-rank UpUW return and literal pt in ranks2-4. DescWeak remains a precisely scoped original foundation. J<=ker x is concluded, not assumed.'}

# The remaining code is deliberately component-local and reproducible.
def build():
 files={};sources={};excerpts=[]
 for key,(rel,start,end,title) in specs.items():
  data=(repo/rel).read_bytes();pinned=subprocess.run(['git','show',PIN+':'+rel],cwd=repo,stdout=subprocess.PIPE,check=True).stdout
  assert data==pinned,rel
  lines=data.splitlines(keepends=True);end=end or len(lines);assert 1<=start<=end<=len(lines),(rel,start,end)
  block=b''.join(lines[start-1:end]);url=f'https://github.com/CocoSgt/riemann-hypothesis-lean/blob/{PIN}/{rel}'
  files[rel]={'path':rel,'sha256':sha(data),'bytes':len(data),'line_count':len(lines),'verified_equal_to_pinned_git_blob':True,'url':url}
  sources[key]={'id':config['prefix']+'_SRC_'+key.upper(),'path':rel,'declaration':title,'line_start':start,'line_end':end,'source_commit':PIN,'full_file_sha256':sha(data),'file_sha256':sha(data),'range_sha256':sha(block),'range_bytes':len(block),'verified_equal_to_pinned_git_blob':True,'url':url+f'#L{start}-L{end}'}
  excerpts.append(f'[{sources[key]["id"]}] {title}\n{sources[key]["url"]}\n'+block.decode())
 for e in external:e['sources']=[sources[k] for k in e.pop('source_keys')]
 text=(HERE/'main.tex').read_text();main_sha=sha(text.encode());prefix=config['prefix']
 lookup={}
 for f in list(ROOT.glob('*/main.tex'))+list(ROOT.glob('*/adjoint_matching.tex')):
  txt=f.read_text()
  for m in re.finditer(r'% BEGIN ([A-Z]+\d+)\n.*?% END \1\n',txt,re.S):
   cid=m.group(1)
   if cid in lookup:
    assert lookup[cid][2]==sha(m.group().encode()),(cid,f,'different duplicate blocks')
    continue
   lookup[cid]=(f,sha(f.read_bytes()),sha(m.group().encode()))
 local={prefix+str(i) for i in relations};claims=[];inherited={}
 for i,(deps,ss) in relations.items():
  cid=prefix+str(i);m=re.search(r'% BEGIN '+cid+r'\n.*?% END '+cid+r'\n',text,re.S);assert m,cid
  ds=[prefix+str(d) if isinstance(d,int) else d for d in deps];assert set(ds)<=set(lookup),(cid,set(ds)-set(lookup))
  for dep in set(ds)-local:
   f,fh,bh=lookup[dep];inherited[dep]={'claim':dep,'file':str(f.relative_to(ROOT)),'file_sha256':fh,'claim_sha256':bh,'kind':'same_version_human_proof' if '_v45/' in str(f) else 'immutable_inherited_human_proof','newly_modified_by_this_component':False}
  start=text[:m.start()].count('\n')+1
  claims.append({'id':cid,'title':re.search(r'\\paragraph\{'+cid+r'\. (.*?)\}\n',m.group(),re.S).group(1),'introduced_in':'0.45','classification':'B','depends_on':ds,'external_input_ids':ext_uses.get(i,[]),'proof_location':{'file':config['component']+'/main.tex','label':'claim:'+cid,'line_start':start,'line_end':start+m.group().count('\n')-1,'sha256':sha(m.group().encode()),'bytes':len(m.group().encode())},'sources':[sources[s] for s in ss],'source_proof_is_not_human_proof':True})
 reviews=[]
 paths=list(HERE.glob('review_*.json'));rp=ROOT/'reviews_v0_45'/f'{config["component"]}_root_review.json'
 if rp.exists():paths.append(rp)
 for p in paths:
  v=json.loads(p.read_text());assert v.get('result',v.get('status'))=='PASS',p
  entries=v.get('claims_reviewed',v.get('reviewed_claims',[]));ids=[]
  for e in entries:
   cid=e if isinstance(e,str) else e.get('id',e.get('claim'));assert cid in local,(p,cid)
   expected=v.get('proof_hashes',{}).get(cid) if isinstance(e,str) else e.get('proof_range_sha256',e.get('block_sha256'))
   assert expected==lookup[cid][2],(p,cid,'stale reviewed block')
   ids.append(cid)
  reviews.append({'file':str(p.relative_to(ROOT)),'sha256':sha(p.read_bytes()),'reviewer':v.get('reviewer'),'result':'PASS','reviewed_proof_file_sha256':v.get('proof_sha256',v.get('proof_file_sha256')),'proof_file_sha256':main_sha,'reviewed_blocks_unchanged':True,'claims':ids,'scope':v.get('scope')})
 reviewed={c for r in reviews for c in r['claims']};complete=local<=reviewed
 status='complete_at_stated_scope_independently_reviewed' if complete else 'complete_at_stated_scope_pending_independent_review'
 for c in claims:
  c['status']='complete_at_stated_scope_independently_reviewed' if c['id'] in reviewed else 'complete_at_stated_scope_pending_independent_review'
  c['independent_review_files']=[r['file'] for r in reviews if c['id'] in r['claims']]
 contracts={'schema':'rh-human-component-contract/1','artifact_version':'0.45','source_commit':PIN,'proof_file_sha256':main_sha,**config,'universal_quantifiers':['Every original point, coefficient datum and fixed algebraic iota','Every original local component, IsRecT, prolongation, period bridge and induced embedding wherever present','Every Teichmuller family and same integral type; unchanged original v0 depth'],'retained_foundations':[e['id'] for e in external]}
 prov={'schema':'rh-human-component-provenance/1','component':config['component'],'artifact_version':'0.45','source_commit':PIN,'proof_file_sha256':main_sha,'status':status,'claims':claims,'inherited_human_inputs':list(inherited.values()),'classical_and_foundational_inputs':external,'independent_reviews':reviews,'dependency_convention':'depends_on contains only numbered human claims; original foundations are separately named in external_input_ids.','source_proof_is_not_human_proof':True,'root_ledger_modified':False,'frozen_artifacts_modified':False}
 closure={'schema':'rh-human-component-closure/1','component':config['component'],'artifact_version':'0.45','source_commit':PIN,'proof_file_sha256':main_sha,'status':status,'closed_subcontracts':config['subcontracts'],'new_global_frontier_leaf_closures':[],'foundation_retention_explicit':True,'independent_reviews':reviews,'validation':'Two-pass standalone draft TeX, no Lean replay; independent hash-bound mathematical/source reviews as listed.','pending':sorted(local-reviewed)}
 manifest={'schema':'rh-source-manifest/1','component':config['component'],'source_commit':PIN,'files':list(files.values()),'ranges':list(sources.values())}
 for name,obj in [('contracts.json',contracts),('original_contracts.json',contracts),('provenance.json',prov),('closure.json',closure),('source_manifest.json',manifest),('retained_foundations.json',external)]:
  (HERE/name).write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n')
 (HERE/'source_excerpts.txt').write_text('\n\n'.join(excerpts))
 (HERE/'report.txt').write_text(config['component']+' v0.45\n\n'+config['report']+'\n\nOriginal foundations are explicitly retained in retained_foundations.json and outside the mathematical DAG. No source proof is substituted for a human proof. No frozen artifact or shared metadata was edited.\n\nRebuild: python build_metadata.py --repo /path/to/formal_source\nValidate: python validate_tex.py --format /path/to/project/pdflatex.fmt\n\n'+f'Pin: {PIN}\nMain SHA256: {main_sha}\nStatus: {status}\nClaims: {len(claims)}; source files: {len(files)}; ranges: {len(sources)}\n')
 hashes={p.name:sha(p.read_bytes()) for p in sorted(HERE.iterdir()) if p.is_file() and p.name!='hashes.json'}
 (HERE/'hashes.json').write_text(json.dumps({'component':config['component'],'artifact_version':'0.45','hashes':hashes},indent=2)+'\n')
 print(json.dumps({'component':config['component'],'claims':len(claims),'source_files':len(files),'source_ranges':len(sources),'inherited_bindings':len(inherited),'main_sha256':main_sha,'status':status},indent=2))
build()
