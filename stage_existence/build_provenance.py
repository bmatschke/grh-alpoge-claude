#!/usr/bin/env python3
"""Build the SE ledger from immutable pinned Git blobs; no checkout mutations."""
from pathlib import Path
import argparse, hashlib, json, re, subprocess

ROOT=Path(__file__).resolve().parent
ap=argparse.ArgumentParser();ap.add_argument('--repo',type=Path,default=ROOT.parents[1]/'lean-source')
REPO=ap.parse_args().repo.resolve()
PIN='7cbf7a0c32fca1badf05931879a37c3f8a2b03b4'
URL='https://github.com/CocoSgt/riemann-hypothesis-lean'
AB='src/Development/AbelianVarietyTheory/'
IP=AB+'Proofs/IwasawaDecomposition/'
FP=AB+'Proofs/FoundationProofs/'
DF=AB+'Definitions/AutomorphicMembership/'
P={
 'lattice':IP+'LatticeEmbeddingMemUnitGroup.lean',
 'div':DF+'NuInRange.lean','rows':DF+'RowsRestWordColumnUnitBaseTuple.lean',
 'model':DF+'ModelLamPDef.lean','pins':DF+'LatAtLattice.lean',
 'ok':DF+'ExistsOkPins.lean','s':DF+'SCuIsom.lean',
 'inner':IP+'ExistsInnerProductSpace.lean','loc':FP+'ExistsContinuousPadic.lean',
 'split':FP+'ExistsIrreducible.lean','cd': 'src/Formalism/LocalRingCardinality/DataCD.lean',
 'reim':FP+'ReImMapSurjective.lean','haar':FP+'NonemptyCompactDualHaar.lean',
 'g':DF+'ResCharThetaJetPlaceDegOne.lean','lifts':DF+'ExistsAllLifts.lean',
 'const':FP+'ConstMapInjective.lean','inhab':IP+'InhabitedStage.lean',
 'zero':IP+'GoodTupleConditionOfIdempotentZero.lean',
 'localstage':DF+'NStageTrivialCharacterCoeffEq.lean',
 'fontaine':IP+'ExistsLocalPrimeAinf.lean','locinhab':IP+'LocStageInhabited.lean',
 'spaces':IP+'SpacesNormHasFrame.lean','coord':IP+'PinsCoordPre.lean',
 'sized':AB+'Proofs/GlobalInterpolation/ExistsHypJetsAll.lean',
 'choice':'src/Formalism/LocalRingCardinality/DataNChoice.lean',
}
cache={}
def sha(b):return hashlib.sha256(b).hexdigest()
def blob(path):
 if path not in cache:
  raw=subprocess.check_output(['git','-C',str(REPO),'show',PIN+':'+path])
  if (REPO/path).is_file():assert (REPO/path).read_bytes()==raw,('changed checkout',path)
  cache[path]=raw
 return cache[path]
PREFIX=r'^(?:@\[[^\n]*?\]\s*)?(?:(?:private|protected|noncomputable)\s+)*'
BOUND=re.compile(PREFIX+r'(?:theorem|lemma|def|abbrev|structure|instance|variable|namespace|end|open|section|set_option|attribute|include|omit)\b|^@\[[^\n]*\]')
def namespace(lines,i):
 stack=[]
 for l in lines[:i]:
  m=re.match(r'^namespace\s+(\S+)',l)
  if m:stack.append(('n',m[1]))
  elif re.match(r'^(?:noncomputable\s+)?section(?:\s|$)',l):stack.append(('s',None))
  elif re.match(r'^end(?:\s|$)',l) and stack:stack.pop()
 return '.'.join(v for k,v in stack if k=='n')
def src(key,name,role='literal endpoint or substantive supplier'):
 path=P.get(key,key);raw=blob(path);ls=raw.splitlines(keepends=True);ts=[l.decode().rstrip('\r\n')for l in ls]
 pat=re.compile(PREFIX+r'(?:theorem|lemma|def|abbrev|structure)\s+'+re.escape(name)+r'(?=\s|\{|\(|:|$)')
 hits=[i for i,l in enumerate(ts)if pat.match(l)];assert len(hits)==1,(path,name,hits)
 a=hits[0];b=a+1
 while b<len(ls)and not BOUND.match(ts[b]):b+=1
 while b>a+1 and not ts[b-1].strip():b-=1
 part=b''.join(ls[a:b]);ns=namespace(ts,a);full=((ns+'.')if ns else '')+name
 if full.startswith('_root_.'):full=full[7:]
 url=f'{URL}/blob/{PIN}/{path}#L{a+1}-L{b}'
 return dict(path=path,declaration=full,source_spelling=name,line_start=a+1,line_end=b,sha256=sha(raw),full_file_sha256=sha(raw),range_sha256=sha(part),range_bytes=len(part),first_line=ts[a],declaration_lines_within_range=[a+1],url=url,pinned_url=url,role=role,verified_equal_to_pinned_git_blob=True)
def ss(key,*names):return[src(key,n)for n in names]
main=(ROOT/'main.tex').read_bytes();mt=main.decode();report=(ROOT/'report.txt').read_bytes()
markers=list(re.finditer(r'(?m)^\\paragraph\{(SE\d+):',mt));assert[m[1]for m in markers]==[f'SE{i}'for i in range(1,17)]
claims=[]
def claim(i,title,statement,deps,sources,assumptions):
 a=markers[i-1].start();b=markers[i].start()if i<len(markers)else len(mt);part=mt[a:b].encode()
 claims.append(dict(id=f'SE{i}',title=title,statement=statement,status='derived_simplification',mathematical_status='proved_under_explicit_hypotheses',introduced_in='0.17',depends_on=deps,assumptions=assumptions,proof_location=dict(file='stage_existence/main.tex',expanded='stage_existence/report.txt',section=f'SE{i}',sha256=sha(part),line_start=mt[:a].count('\n')+1,line_end=mt[:b].count('\n'),bytes=len(part)),sources=sources))

claim(1,'Semilinear extension and independence','An embedded K-basis which is complex-independent permits every semilinear map to extend complex-linearly and sends every K-independent family to a complex-independent family.',[],ss('lattice','map_eq_sum','exists_extension','linearIndependent_map'),['Finite-dimensional K-space, field embedding sigma, complex-independent image of the stated basis.'])
claim(2,'Finite common-kernel descent','The common kernel of finitely many complex-linear operators preserving the actual coefficient-field form is exactly the complex span of the common K-kernel inside that form.',['SE1'],ss('lattice','mem_span_ker'),['Finite operator index set; preservation of e(V), not only of its complex span.'])
claim(3,'Restricted Hermitian frames','For every rational subspace, the positive Gram matrix (X^{-1}E)^*(X^{-1}E) constructs invertible frames giving exactly the restricted norm at each infinite place.',['SE1'],ss('lattice','exists_frame','cnorm_mulVec','vecMap','exists_frames_restrict'),['Invertible original frames; finite K-basis of the subspace.'])
claim(4,'Integral intersection is a full lattice','The pullback of L to U maps exactly to L intersect U, is finitely generated over O_K and spans U, without a freeness or principal-ideal assumption.',['SE3'],ss('lattice','subHLat','subHLat_map','subHLat_good','stdHLat_good'),['Number field K; good original Hermitian lattice.'])
claim(5,'The actual ramified coefficient-field form','Integral action preservation descends rhoT and Nm to the actual coefficient-field form. ramEmb sends every K-basis to a complex basis of the same Mram.',['SE1','SE2','SE4'],ss('lattice','rhoT_rat','Nm_rat','lattice_embedding_mem_unit_group','ramEmb','ramEmb_basis'),['Literal MemberForms fields, finite vT, actual Fi_zero and emb_basis.'])
claim(6,'All fourteen DivStage fields','For arbitrary RowsRest W, construct DivStage on W with AllGood and exact nuIn image equal to ramL, using actual restricted lattices and zero auxiliary Bk.',['SE3','SE4','SE5'],ss('div','DivStage')+ss('lattice','exists_divStage'),['The supplied B,C,W are identical throughout; no later bounds for independently specified maps are inferred.'])
claim(7,'Actual finite class forms supply Fits','Finite representative evaluation proves Mt finite-dimensional; actual word-independent period spaces and positive class sums supply all five Fits fields on I.cols(l).',['TL7'],ss('ok','mt_finite','ipC_herm','ipC_pos','fits')+ss('model','Fits'),['Actual TC I with Laws; original finite classes and representation/metric ties.'])
claim(8,'Explicit row model and exact existence criterion','RowsRest(B,C) is inhabited iff some d admits Fits(C,d). The model retains actual periods and Mram while choosing explicit coordinate auxiliary spaces, lattices and operators.',['SE1','SE7'],ss('rows','RowsRest')+ss('model','Fits','fits_of_rows','MuT','core','stdOLat','stdJ','stdJ_single','stdJ_basis','trunc','trunc_self','chain_lin','mdim','mdim_m','model','nonempty_iff'),['Fits(C,d) for the reverse implication; dimensions n,n0,a may be any natural numbers.'])
claim(9,'Ordinary completions with exactly marked split places','Completion and tensor-base-change construct LocAt at every finite place; full splitting marks the optional split datum exactly at the two selected residue characteristics. This is not LocStage.',['AH17'],ss('loc','exists_locAt')+ss('split','nonempty_splitAt')+ss('inner','ncard_primesOver_eq','conjF_ne_id','exists_locAt_split_iff'),['Supplied Base CM quadratic extension and full splitting at g0,g1; standard completion, local degree and CRT facts are explicit background.'])
claim(10,'All nine SStage fields','HasLetters, the actual positive class metric and Drows<=Dall give SStage with exact conjugate-linear isometric row inclusion, specified locals, singleton terms and zero spectral contributions.',['SE7','SE9'],ss('s','SStage')+ss('inner','nonempty_conj_embedding','exists_innerProductSpace','exists_sStage','nonempty_sStage'),['HasLetters with its exact gap/letter identities; class metric positive on Mu0; Drows<=Dall on the same W.'])
claim(11,'All four compact-dual Haar fields','The explicit real-form decomposition normalizes product Lebesgue measure. Exponential-chart density and positive scaling produce Haar measures with probability at compact signatures and equal finite nonzero Omega densities at compact dual signatures.',[],ss('cd','IsOmegaLeb','OmegaDensity','CDHaar')+ss('reim','reImMap','reImMap_injective','reImMap_surjective','exists_isOmegaLeb')+ss('haar','exists_density_of_chart','exp_mem','expU','image_expU','exists_omegaDensity','exists_haar_of_density','exists_prob_haar','nonempty_cdHaar'),['Finite-dimensional change of variables, matrix power-series logarithm/exponential, and ordinary Haar existence/uniqueness; no actual global mass/volume estimate.'])
claim(12,'GJStage with prescribed ranks and optional empty jets','The constant-function, no-variable-place GAtP model has every prescribed rank and finite classes. Given the jet compatibility fields it constructs GJStage; empty jets, constant positive volume and SE11 prove bare GJStage existence.',['SE11'],ss('g','GJStage')+ss('const','noPlaces','htupW_eq','finClasses','gat','constMap_injective','range_constMap','gat_d','GAtP₂')+ss('lifts','exists_place','tau_nonempty','exists_of_jet','gxOne','nonempty_iff')+ss('inhab','noJet','exists_noJet','nonempty_stage'),['The general jet construction retains adjacent-class nonemptiness and supplied positive volume; the bare model has empty situations and volume 1. The specific trueVol conclusion remains separate.'])
claim(13,'Zero good-tuple idempotents and exact adaptation','The unipotent delta family of central idempotents vanishes on squarefree good polynomials, so e0=0. Adaptation sets eOp,eMt,eta to zero and shaLen to the stated nonnegative toNat scalar, preserving RowsRest.',['SE8'],ss('zero','shaTrue','shaTrue_nonneg','unipSer','unipSer_sum','unipSer_of_squarefree','cenTriv','idempotent_good_tuples_eq_zero','good_tuple_condition_of_idempotent_zero','adapt'),['r>=2 and nonempty selected-prime family; adaptation uses the source defining Galois scalar. Does not prove full NStage or finiteness of Sha.'])
claim(14,'Five-stage join with NStage retained on the same W','Actual Laws and HasLetters, together with NStage on the exact adapted one-dimensional RowsRest model, imply Later via reconstructed RowsRest,DivStage,SStage,GJStage. The zero eMt model excludes automatic positive projector-rank conclusions; the particular empty-Tw NStage model cannot supply NChoice.twI on the nonempty coefficient-place set.',['SE6','SE7','SE8','SE10','SE11','SE12','SE13'],ss('pins','Later')+ss('ok','later')+ss('zero','nTw','exists_nStage_of_rows','exists_nStage_adapt')+ss('localstage','LocStage')+ss('choice','NChoice'),['NStage(B,C,adapt(model(fits(l),1,1,1))) remains a supplied input; LocStage/Fontaine and full Galois assembly not proved. The empty-Tw incompatibility concerns only this particular auxiliary model.'])
claim(15,'Diagonal spaces and exact coordinate frame inclusion','Explicit positive/negative diagonal coordinates give hyperbolic auxiliary frames, required signatures and norm T top line; extension by zero proves the literal Pins.iX equation.',[],ss('spaces','planeVec','planeVec_planeVec','ext_planeVec','single_planeVec','rankY_eq_N_add','pY_eq_N_add','top_line_norm','spacesNorm','spacesNorm_z_norm','spacesNorm_hasFrame','spacesNorm_coord','spacesNorm_T','spacesNorm_Vneg','spacesNorm_Y_sig')+ss('coord','PinsP','extTo_basis'),['Actual rank conditions and CM involution; prime T and supplied pz with conjugate(pz)*pz=T.'])
claim(16,'Both pins for an existing sized input','Replacing an existing input by the diagonal space model and setting c(u)=pi(u0)/pi(u) gives both frame and scalar pins, preserving its exact arithmetic/weight data.',['SE15'],ss('pins','Pins')+ss('ok','exists_pre','exists_ok_pins')+ss('sized','exists_pre_sized'),['Existing sized Pre/PreX, oriented frame and letter/duStar data; their existence and subsequent compatible Ok are retained.'])

def fields(key,name):
 s=src(key,name,'literal record field audit');ls=blob(s['path']).decode().splitlines()[s['line_start']-1:s['line_end']]
 out=[]
 for l in ls[1:]:
  m=re.match(r'^  \[?([A-Za-z_][A-Za-z0-9_\u0080-\uffff]*)\s*(?:\(|:|\{|\[)',l)
  if m:out.append(m[1])
 return s,out
audits=[]
for key,name,cid in [('div','DivStage','SE6'),('model','Fits','SE7'),('rows','RowsRest','SE8'),('s','SStage','SE10'),('cd','CDHaar','SE11'),('g','GJStage','SE12'),('pins','Later','SE14'),('pins','Pins','SE16')]:
 s,fs=fields(key,name);audits.append(dict(record=s['declaration'],source=s,field_count=len(fs),fields=[dict(name=f,supplied_by=cid,scope='N retained on the same W'if name=='Later'and f=='N'else'Exact conditional construction in cited claim')for f in fs]))
remaining=[
 dict(interface='NStage and LocStage',scope='Full exists_nStage_adapt, actual Fontaine period rings and comparison ties remain. SE13 proves only central-idempotent/adaptation steps; SE14 is conditional on N for the exact adapted W.'),
 dict(interface='Existing sized geometric input',scope='SE16 normalizes an existing PreX/oriented/HasLetters input. Analytic windows and actual geometric construction supplying it remain.'),
 dict(interface='Quantitative global branches',scope='Auxiliary zero operators, constant volumes and empty jets do not supply spectral, metric, cohomological or prime-window estimates or identify actual external realizations.'),
]
targets=[]
for key,name,scope in [
 ('zero','exists_nStage_of_rows','Reconstruct every NData/NAut/NBC/NTw/NExp/NTh/NTypes field and ties; retain the precise zero operators, shaTrue and empty Loc/Tw construction. SE13 only supplies idempotent/adaptation calculations.'),
 ('fontaine','exists_locPrime_tied','Construct the actual LocTheory/LocAinf/LocTied with Fontaine period rings, actions, filtration and comparison maps. Ordinary local completion SE9 does not supply this.'),
 ('sized','exists_pre_sized','Supply the original sized PreX, HasLetters and exact duStar/window/geometric data before SE15-SE16 coordinate normalization.'),
 ('inhab','exists_noJet','Bare GJStage existence is supplied by SE11-SE12. The stronger specific trueVol/baseVol conclusion retains its positivity and geometric volume identification.'),
]:
 t=src(key,name,'retained source target');t.update(id='SE-next-'+str(len(targets)+1),priority=1 if key in ['zero','fontaine']else 2,remaining_human_scope=scope,scope=scope);targets.append(t)
completed=[]
for key,name,ids in [('lattice','exists_divStage',['SE6']),('model','nonempty_iff',['SE8']),('inner','exists_sStage',['SE9','SE10']),('haar','nonempty_cdHaar',['SE11']),('lifts','nonempty_iff',['SE12']),('coord','extTo_basis',['SE15']),('spaces','spacesNorm_hasFrame',['SE15'])]:
 s=src(key,name);completed.append(dict(path=s['path'],declaration=s['declaration'],claims=ids,reason='Literal conditional endpoint reconstructed; retained inputs explicitly recorded.'))
files=[dict(path=p,sha256=sha(b),bytes=len(b),lines=len(b.splitlines()),commit=PIN,url=f'{URL}/blob/{PIN}/{p}',verified_equal_to_pinned_git_blob=True)for p,b in sorted(cache.items())]
artifacts={n:dict(sha256=sha((ROOT/n).read_bytes()),bytes=(ROOT/n).stat().st_size)for n in ['main.tex','report.txt','build_provenance.py']}
links=sum(len(c['sources'])for c in claims);ranges={(s['path'],s['line_start'],s['line_end'],s['range_sha256'])for c in claims for s in c['sources']}
data=dict(artifact_version='0.17',component='stage_existence',repository=URL,commit=PIN,scope='Actual restricted lattices and DivStage; Fits/RowsRest; ordinary local/SStage; CDHaar and bare GJStage; precise conditional Later and pins normal form. Full NStage/LocStage, prior geometric existence and quantitative branches retained.',claim_count=len(claims),source_link_count=links,unique_claim_source_range_count=len(ranges),source_file_count=len(files),claims=claims,source_files=files,proof_artifacts=artifacts,record_audits=audits,retained_inputs=remaining,completed_targets=completed,independent_reviews=[],validation=dict(read_only_source_access=True,source_range_hashes_regenerated=True,lean_build_performed=False,pdf_build_performed=False))
for filename,reviewer,nums in [('nc_reviews_se_1_8_13_16.txt','/root/class_rank',list(range(1,9))+list(range(13,17))),('vi_reviews_se_9_12.txt','/root/comparison_span',list(range(9,13)))]:
 rp=ROOT.parent/'reviews_v0_17'/filename
 if not rp.exists():continue
 raw=rp.read_bytes();content=raw.decode();chosen={c['id']:c['proof_location']['sha256']for c in claims if int(c['id'][2:])in nums}
 assert 'PASS'in content
 for cid,h in chosen.items():assert h in content,('review paragraph changed',filename,cid)
 data['independent_reviews'].append(dict(reviewer=reviewer,result='PASS',claim_ids=list(chosen),review_record='../reviews_v0_17/'+filename,review_record_sha256=sha(raw),paragraph_sha256=chosen,lean_replay=False))
for n,obj in [('provenance.json',data),('source_manifest.json',dict(artifact_version='0.17',component='stage_existence',repository=URL,commit=PIN,source_files=files,proof_artifacts=artifacts)),('next_targets.json',dict(artifact_version='0.17',repository=URL,commit=PIN,targets=targets,completed_targets=completed,retained_inputs=remaining))]:
 (ROOT/n).write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n')
out=['STAGE EXISTENCE SE1-SE16',f'Repository {URL}',f'Commit {PIN}',f'{len(claims)} claims, {links} source links, {len(files)} pinned files.','']
for c in claims:
 out += [c['id']+': '+c['title'],'Proof paragraph SHA256 '+c['proof_location']['sha256']]
 for s in c['sources']:out += [f"  {s['declaration']} | {s['path']}:{s['line_start']}-{s['line_end']}",'  '+s['url'],f"  File {s['full_file_sha256']}; range {s['range_sha256']}"]
 out+=['']
out+=['RETAINED TARGETS']+[f"{t['declaration']}: {t['remaining_human_scope']}"for t in targets]
(ROOT/'source_locators.txt').write_text('\n'.join(out)+'\n')
print(json.dumps(dict(claims=len(claims),source_links=links,unique_ranges=len(ranges),source_files=len(files),record_fields={a['record']:a['field_count']for a in audits},next_targets=len(targets)),indent=2))
