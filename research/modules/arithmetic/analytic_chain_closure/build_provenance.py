#!/usr/bin/env python3
"""Rebuild source locators for the v0.23 cohomological-window closure."""
from pathlib import Path
import argparse, hashlib, json, re, subprocess
ROOT=Path(__file__).resolve().parent
p=argparse.ArgumentParser();p.add_argument('--repo',type=Path,default=ROOT.parents[1]/'lean-source');a=p.parse_args();REPO=a.repo.resolve()
PIN='7cbf7a0c32fca1badf05931879a37c3f8a2b03b4'
BASE='https://github.com/CocoSgt/riemann-hypothesis-lean/blob/'+PIN+'/'
def sha(x):return hashlib.sha256(x).hexdigest()
D='src/Development/AutomorphicArithmetic/'
V=D+'AutomorphicVarieties/'
W=V+'CMFieldExponentialBounds/'
P=V+'PrimeSetBoundDataOfPrimitiveChar.lean'
F=V+'StmtFields.lean'
E=D+'CharacterBoxes/ExistsPageN.lean'
source_specs={
 'VW1':[
 ('src/Formalism/GaloisCohomology/Statement.lean','qzTw'),
 ('src/Formalism/GaloisCohomology/Statement.lean','Sha'),
 (V+'PartsConj.lean','h1TwistConjByLift'),
 (V+'PartsConj.lean','h1TwistConjByLift_eq_self_of_forall_apply_eq'),
 (V+'PartsConj.lean','h1TwistConjByLift_eq_of_isLift_of_isLift'),
 (V+'PartsConj.lean','h1TwistConjByLift_mem_sha_of_mem_sha'),
 (V+'PartsConj.lean','galoisActionOnCohomology'),
 (V+'PartsConj.lean','galois_action_cohomology_mul'),
 (V+'PartsConj.lean','galois_action_preserves_sha'),
 (V+'LengthEqAddEigen.lean','length_eq_add_eigen'),
 (V+'LengthEqAddEigen.lean','ShaPlus'),
 (V+'LengthEqAddEigen.lean','ShaMinus'),
 (V+'LengthEqAddEigen.lean','shaLen_eq_add'),
 (V+'LengthEqAddEigen.lean','VVat'),
 (V+'LengthEqAddEigen.lean','VVminusLe'),
 (V+'LengthEqAddEigen.lean','VVplusLe'),
 (V+'LengthEqAddEigen.lean','vvle_of_parts'),
 (E,'VVle')],
 'VW2':[(E,'IsChiField'),(E,'WinPair'),(E,'PageN'),(E,'exists_pageN'),
 (F,'IsCompField'),(F,'condF'),(F,'isCompField_ofChar'),
 (W+'ConductorBoundsOfIsChiField.lean','UpperTheory.V.conductor_bounds_of_isChiField'),
 (W+'IsCMFieldOfIsChiField.lean','UpperTheory.V.isCMField_of_isChiField'),
 (V+'HeightAndVanishing/HostCond.lean','UpperTheory.V.HV.hostCond'),
 (W+'AdmissibleOfPageN.lean','admissible_of_pageN'),
 (W+'logpair.lean','UpperTheory.V.log_mul_le_rpow_of_winPair'),
 (W+'bigpair.lean','UpperTheory.V.eventually_winPair_gt_power'),
 (W+'LogConductorMulHeightLeOfPageN.lean','UpperTheory.V.log_conductor_mul_height_le_of_pageN'),
 (F,'minusBound'),
 (W+'minusle.lean','UpperTheory.V.minusBound_le_exp_of_log_le'),
 (W+'ErrorTermsLeSqrtExpRpow.lean','UpperTheory.V.error_terms_le_sqrt_exp_rpow')],
 'VW3':[(P,'admitted'),(P,'PrimePair'),(P,'BaAt'),(P,'HVAt'),(P,'JointWin'),(P,'ThmBc'),
 (E,'VAt'),(E,'VWinAt'),(E,'VWin'),
 (W+'AdmissibleOfPageN.lean','vwinAt_of_joint'),
 (W+'AdmissibleOfPageN.lean','vwin_of_joint')],
 'VW4':[(P,'BConst'),(P,'BConst.R'),(P,'BConst.J'),(P,'BbAt'),(P,'IsBWindow'),(P,'BShape'),(P,'ThmBab'),(P,'ThmHV'),
 (P,'ThmBcFree'),(P,'thmBc_iff'),(P,'primeSetBoundData_of_primitiveChar'),(P,'jointWin_of'),
 (F,'pK'),(F,'hStar'),(F,'pOne'),(F,'Bchi'),(F,'prime_of_mem_Bchi'),
 (V+'HeightAndVanishing/LayerLe.lean','LayerLe'),
 (V+'HeightAndVanishing/LayerLe.lean','PointHV'),
 (V+'HeightAndVanishing/ThmHV.lean','UpperTheory.V.HV.thmHV'),
 (V+'HeightAndVanishing/HostCond.lean','UpperTheory.V.HV.hostCond'),
 (D+'CharacterBoxes/PairGood.lean','PairGood'),
 (D+'CharacterBoxes/PairGood.lean','PairEx'),
 (D+'CharacterBoxes/WinPairs.lean','UpperTheory.Top.winPairs'),
 (E,'VVle.mono')]
}
DECL=re.compile(r'^(?:(?:private|protected|noncomputable)\s+)*(?:def|theorem|lemma|structure|abbrev)\s+([^\s({:]+)')
cache={}; files={}
def source(path,name):
 if path not in cache:
  data=(REPO/path).read_bytes();lines=data.splitlines(keepends=True)
  pin=subprocess.run(['git','-C',str(REPO),'show',PIN+':'+path],check=True,capture_output=True).stdout
  if data!=pin:raise ValueError('source differs from pin: '+path)
  ds=[]
  for i,l in enumerate(lines,1):
   m=DECL.match(l.decode())
   if m:ds.append((i,m.group(1)))
  cache[path]=(data,lines,ds)
  files[path]={'path':path,'sha256':sha(data),'bytes':len(data),'lines':len(lines),'url':BASE+path,'verified_equal_to_pinned_git_blob':True}
 data,lines,ds=cache[path];matches=[(i,n) for i,n in ds if n==name]
 if len(matches)!=1:raise ValueError((path,name,matches))
 first=matches[0][0];last=next((i-1 for i,n in ds if i>first),len(lines))
 chunk=b''.join(lines[first-1:last]);return {'path':path,'declaration':name,'line_start':first,'line_end':last,'sha256':sha(data),'range_sha256':sha(chunk),'range_bytes':len(chunk),'first_line':lines[first-1].decode().rstrip(),'declaration_lines_within_range':[first],'url':BASE+path+f'#L{first}-L{last}','verified_equal_to_pinned_git_blob':True}
text=(ROOT/'main.tex').read_text();markers=[r'\section{Closing the cohomological window assembly}',r'\subsection{The actual field and the uniform numerical budget}',r'\subsection{Two precise input interfaces and their closed consequence}',r'\subsection{The minimal supplier boundary and the fixed-pair endpoint}'];starts=[text.index(x) for x in markers]+[len(text)]
info={
 'VW1':('Exact two-primary and odd-eigenspace cohomological assembly',[],[], 'Complete elementary construction and proof. Standard continuous cocycle definitions and finite module-length additivity are used; no cohomological finiteness theorem, duality or automorphy supplier is asserted.'),
 'VW2':('Same-field CM/conductor identification and uniform window budget',[],[], 'Complete field and numerical lemmas. The exact host conductor is proved using its finite character group; the supplied IsChiField and prime/page hypotheses remain the theorem premises.'),
 'VW3':('Complete JointWin plus ThmBc to literal VWinAt chain',['VW1','VW2'],['JointWin(Ct): the simultaneous two-primary and odd-plus cohomological square-window theorem, with its original quantifiers.', 'ThmBc(Ct): the uniform odd-minus length bound; only its fixed-target specialization is used.'], 'Complete conditional theorem, with the two deep supplier interfaces explicitly retained. Does not prove unconditional VWinAt.'),
 'VW4':('Structural cohomological suppliers to one fixed good pair on the whole window',['VW2','VW3','QP22'],['ThmBab(K,Ct) on the specified Bchi and cyclotomic layers, with one common K.', 'PointHV for the specified layer-index function and original hosts.', 'ThmBcFree for the same abelian base and original CM fields.', 'CN, BD and HD, the named unconditional classical inputs retained in QP22.'], 'Complete conditional supplier and fixed-pair assembly. Every remaining cohomological supplier and QP22 classical input stays explicit; all fields and pairs are the original ones.')
}
claims=[]
for i,cid in enumerate(source_specs):
 title,deps,remain,status=info[cid];part=text[starts[i]:starts[i+1]].encode()
 claims.append({'id':cid,'title':title,'status':status,'remaining_inputs':remain,'mathematical_dependencies':deps,'component_ledger':'analytic_chain_closure/provenance.json','sources':[source(*x) for x in source_specs[cid]],'introduced_in':'0.23','human_proof':{'file':'analytic_chain_closure/main.tex','start_marker':markers[i],'end_marker':markers[i+1] if i+1<len(markers) else 'EOF','sha256':sha(part),'bytes':len(part)}})
ledger={'schema':'rh-human-reconstruction-provenance/1','artifact_version':'0.23','date':'2026-11-22','repository':'https://github.com/CocoSgt/riemann-hypothesis-lean','commit':PIN,'scope':'Complete downstream cohomological-window assembly, conditional on explicit deep cohomological suppliers. No unconditional VWinAt or global RH/GRH claim.','range_convention':'One-based inclusive source lines; all byte hashes checked against the pinned git blob.','claims':claims,'source_files':list(files.values()),'mathematical_dependency_graph':{c['id']:c['mathematical_dependencies'] for c in claims},'component_input_boundary':{'coarse':['JointWin(Ct)','ThmBc(Ct)'],'structural':['ThmBab(K,Ct)','PointHV','ThmBcFree'],'classical_pair_leaves':['CN','BD','HD'],'not_supplied':['LinkN','LinkV','cohomological counting statements','Iwasawa layer bounds','actual odd-minus bound','geometric lattice-gain inequality']},'validation':{'main_tex_sha256':sha(text.encode()),'source_files':len(files),'source_links':sum(len(c['sources']) for c in claims),'all_sources_equal_pinned_git_blobs':True,'full_lean_build':False,'kernel_replay':False}}
(ROOT/'provenance.json').write_text(json.dumps(ledger,indent=2,ensure_ascii=False)+'\n')
(ROOT/'source_manifest.json').write_text(json.dumps({'commit':PIN,'source_files':list(files.values())},indent=2)+'\n')
(ROOT/'source_locators.txt').write_text('\n\n'.join(c['id']+' — '+c['title']+'\n'+'\n'.join(f"{s['path']}:{s['line_start']}-{s['line_end']} {s['declaration']}\n{s['url']}\nfile_sha256={s['sha256']} range_sha256={s['range_sha256']}" for s in c['sources']) for c in claims)+'\n')
print(json.dumps(ledger['validation'],indent=2))
