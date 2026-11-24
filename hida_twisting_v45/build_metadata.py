#!/usr/bin/env python3
"""Rebuild the exact finite-order twisting component; no shared output is edited."""
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
 'target':(AV+'WeilGroupCharacters/ArithmeticPointClassicality.lean',103,109,'Complete original TwistOk'),
 'producer':(DT+'WJTwist.lean',1,None,'Actual all-rank finite twist and same-ideal return producer'),
 'wrapper':(DT+'JTwistA.lean',1,None,'Original final TwistOk wrapper'),
 'finitechar':(AB+'PublishedTheorems/AutomorphicForms₂/ExistsUniqueHcharOfFiniteOrder.lean',50,65,'Literal IsLAdicOf equality and algebraic normalizations'),
 'finitecharproof':(AB+'PublishedTheorems/AutomorphicForms₂/ExistsUniqueHcharOfFiniteOrder.lean',372,426,'Continuous finite character, global Artin construction and uniqueness'),
 'conj':(BR+'ThetaCharEqSelfOfConjugateDual.lean',1,None,'Conjugate-dual finite Hecke character on all ideles'),
 'detglobal':(BR+'DetCharacterKerOpenTrivialRationalArchimedean.lean',1,None,'Open determinant kernel and rational/infinity triviality'),
 'detlocal':(BR+'DetCharacterEqLocalDetSplitNonsplit.lean',1,None,'Actual split square and nonsplit determinant character'),
 'auttwist':(BR+'ExistsAutomorphicRepTwistByCharacter.lean',1,None,'Actual multiplication map and two-direction local component transport'),
 'typegd':(CD+'SphericalTwists/UnramifiedTwists/TypeGd.lean',1,None,'Original type-to-Good-and-Gd consumer'),
 'gdcontract':(CD+'SphericalTwists/HodgeTateFromSandwich.lean',15,27,'Exact TypeGd and full TwAway statement'),
 'abconv':('src/Development/AutomorphicArithmetic/Foundations/LocalLanglands/LocalCentralUnits/AbConv.lean',1,None,'Abelian inertia type forces rank-one support'),
 'sphuntw':(CD+'SphericalTwists/UnramifiedTwists/SphUntw.lean',1,None,'Spherical untwist supplies exact Good/Gd guards'),
 'twaway':(DT+'TTwAway.lean',1,None,'Original every-IsRecT away twist producer'),
 'localcontracts':(DT+'SphUntw.lean',15,37,'Literal TwAwayAlt, SphUntwAlt and PsFullAlt'),
 'pfull':(DT+'TPsFull.lean',1,None,'Good finite parts make exact full principal series'),
 'ordtwist':(CD+'SphericalTwists/UnramifiedTwists/PrinTw.lean',1,None,'Exact inducing-function twist and OrdChar transformation'),
 'orddefs':(DT+'OrdDefs.lean',43,70,'PartPtAlt/CoreOrdAlt/AutUOAlt exact arbitrary predicate scope'),
 'return':(DT+'UpUW.lean',80,None,'Exact all-rank original UpUW return'),
 'hecke':(DT+'UnitaryHeckeData.lean',38,74,'Actual integral type and same IsJ data'),
 'literature':(DT+'LitAut.lean',12,63,'Original retained local/global foundational scope'),
}
relations={
 1:(['CAP6'],['finitechar','finitecharproof','conj','detglobal','detlocal','producer']),
 2:([1],['auttwist','detlocal','producer']),
 3:(['GUA12'],['typegd','gdcontract','abconv','sphuntw']),
 4:([1,'ADK1','OFL1'],['twaway','localcontracts']),
 5:(['HPT3'],['pfull','ordtwist','localcontracts']),
 6:(['ADP12','UPA16','ITA12','HED1','HED2','AFS8','HAW10','LTP12','LTP14','LTP15','LTP17','LTP18'],['producer','orddefs','hecke']),
 7:([1,2,3,4,5,6,'HED5','GUA14','LTP17','LTP18'],['producer','target']),
 8:([1,2,3,4,5,6,7,'HPT17'],['target','producer','wrapper','return']),
}
external=[
 {'id':'HTS_ORIGINAL_ARTIN','kind':'retained_original_foundation','classification':'inherited','source_keys':['literature','finitechar','finitecharproof'],
  'statement_used':'The original global Artin quotient with its stated kernel and local Artin reciprocity; HTS1 proves the needed finite-character construction, and HTS4/5 use the exact weight-zero local equality. Cofinite Frobenius identification uses already reconstructed CAP6.','newly_reconstructed':False},
 {'id':'HTS_ORIGINAL_LOCAL','kind':'retained_original_foundation','classification':'inherited','source_keys':['literature','typegd','twaway','localcontracts'],
  'statement_used':'Original local support/multisegment, rank-one parameter and every-IsRecT twist laws under their original Good guards; original away monodromy and finite-coefficient foundations already retained in GUA/OFL. HTS3/4 prove the bounded guarded consumers and do not assert PlainTor for arbitrary nongeneric components.','newly_reconstructed':False},
]
ext_uses={1:['HTS_ORIGINAL_ARTIN'],3:['HTS_ORIGINAL_LOCAL'],4:['HTS_ORIGINAL_ARTIN','HTS_ORIGINAL_LOCAL'],5:['HTS_ORIGINAL_ARTIN','HTS_ORIGINAL_LOCAL']}
config={
 'component':'hida_twisting_v45','prefix':'HTS','endpoint_claim':'HTS8',
 'original_endpoint':'B.TwistOk J','original_producer':'UpperTheory.V.Z.Desc.W.jTwist_of_alt / JTwistA',
 'subcontracts':[{'id':'actual_odd_order_unitary_character','claim':'HTS1'},{'id':'actual_automorphic_twist','claim':'HTS2'},{'id':'TypeGd_and_spherical_untwist_guards','claim':'HTS3'},{'id':'finite_order_away_IsWDOf_twist','claim':'HTS4'},{'id':'PsFull_and_OrdTw','claim':'HTS5'},{'id':'actual_PartOfAlt_extraction','claim':'HTS6'},{'id':'all_UpUW_inputs_for_twisted_point','claim':'HTS7'},{'id':'TwistOk','claim':'HTS8'}],
 'hypotheses':['All original Hida/IsJ data, V.Sprime=s.S, n>=1, ell odd including3, unchanged coefficient O and fixed iota','J<=ker x, x.Good h; beta:G0->Qbar_ell units has open kernel and ell-power order','beta conjugate-dual and trivial on all original Iu and I0','x.D.IsTwist beta xprime.D as full polynomial laws; exact ordered psi twist for xprime'],
 'normalizations':{'odd_power':'ell^k=2N+1, delta=mu^(N+1), delta^2=mu','unitary_character':'chi=nu(det); split local character kappa=nu^2; nonsplit local character nu','weights':'finite twist preserves h and lambda dual','PS':'omega_i becomes omega_i*kappa_w','finite_part':'phi_i becomes phi_i*mu_on_inertia^-1','v0_depth':'same Kc1'},
 'not_claimed':['new DescWeak application or unrestricted automorphy lifting','general arbitrary-infinite-character TwAway proof; HTS4 is the finite-order case sufficient for exact TwistOk','new global selected-frontier closure','completion of RH or GRH'],
 'report':'HTS1-HTS8 prove the exact original TwistOk endpoint for all positive ranks, including prime3. The actual odd-order square-root Hecke character twists the actual unitary automorphic space, with the split-local square checked explicitly. Every local Good/Gd guard, principal-series normalization, full polynomial-law twist, all-Teich type and unchanged v0 depth is verified. HAW10 supplies an actual part at the original Good point, and HPT17 returns the constructed twisted point to the same ideal. The low-rank DescWeak input is not used.'}

# Component-local metadata engine.

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
