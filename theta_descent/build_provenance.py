#!/usr/bin/env python3
"""Build the TD ledger from immutable pinned Git blobs; no checkout mutations."""
from pathlib import Path
import argparse, hashlib, json, re, subprocess

ROOT=Path(__file__).resolve().parent
ap=argparse.ArgumentParser();ap.add_argument('--repo',type=Path,default=ROOT.parents[1]/'lean-source')
REPO=ap.parse_args().repo.resolve()
PIN='7cbf7a0c32fca1badf05931879a37c3f8a2b03b4'
URL='https://github.com/CocoSgt/riemann-hypothesis-lean'
AB='src/Development/AbelianVarietyTheory/'
IR='src/Formalism/LocalToGlobal/IndefiniteReal/'
IP=AB+'Proofs/IwasawaDecomposition/'
TW=AB+'Proofs/TwistedOperators/'
DR='src/Formalism/LocalToGlobal/Divisibility/'
P={
 'coord':IR+'RationalAdjoints/CoordRat.lean',
 'range':IR+'RationalAdjoints/RangeAdjointRat.lean',
 'tests':IR+'RationalAdjoints/RatZOfTests.lean',
 'mu':IR+'RationalAdjoints/RatMuOfRowTest.lean',
 'th':IR+'RationalAdjoints/RatThOfLiftTest.lean',
 'stable':IR+'MemRangeAdjointOfKerStable.lean',
 'level':IR+'LiftGoodPartComplexEqRange.lean',
 'rows':IR+'EqZeroOfMemRangeAdjoint.lean',
 'lifts':IR+'EqZeroOfRangeAdjoint.lean',
 'parts':IR+'PartsOrth.lean','cuts':IR+'CutTuples2.lean',
 'cx':IR+'CxLemmas.lean','principal':IR+'PrincipalLevelLattice.lean',
 'rowlat':DR+'RowLat.lean','rowlem':DR+'RowLatLemmas.lean',
 'ortho':IR+'EquivFunOM.lean','sep':IR+'MajAtEqZeroOfMemQpOfNe.lean',
 'base':IP+'BaseLevelLiftMatrixSolvesRelationExtendedData.lean',
 'holds':AB+'Definitions/AutomorphicMembership/NonzeroPlacesOverPrimesLifts.lean',
 'normal':TW+'RowTestHilbertModelsOfChoiceClaims.lean',
 'realis':TW+'RowTestAtRealisationOfHilbertModels.lean',
 'cxmodel':TW+'RowTestComplexSideOfHilbertModels.lean',
 'kernel':AB+'BlockTheory/TwistedDiscreteSeries/RationalRowTestKernel.lean',
 'formula':AB+'Statements/HeckeThetaIntegrals/FormulaAt.lean',
 'sums':TW+'RowTestRationalSumsOfFiniteSumsMeaningful.lean',
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
def explicit_range(key,name,a,b,role):
 path=P[key];raw=blob(path);ls=raw.splitlines(keepends=True);part=b''.join(ls[a-1:b]);url=f'{URL}/blob/{PIN}/{path}#L{a}-L{b}'
 return dict(path=path,declaration=name,source_spelling='example',line_start=a,line_end=b,sha256=sha(raw),full_file_sha256=sha(raw),range_sha256=sha(part),range_bytes=len(part),first_line=ls[a-1].decode().rstrip('\r\n'),declaration_lines_within_range=[a],url=url,pinned_url=url,role=role,verified_equal_to_pinned_git_blob=True)
main=(ROOT/'main.tex').read_bytes();mt=main.decode();report=(ROOT/'report.txt').read_bytes()
markers=list(re.finditer(r'(?m)^\\paragraph\{(TD\d+):',mt));assert[m[1]for m in markers]==[f'TD{i}'for i in range(1,17)]
claims=[]
def claim(i,title,statement,deps,sources,assumptions):
 a=markers[i-1].start();b=markers[i].start()if i<len(markers)else len(mt);part=mt[a:b].encode()
 claims.append(dict(id=f'TD{i}',title=title,statement=statement,status='derived_simplification',mathematical_status='proved_under_explicit_hypotheses',introduced_in='0.18',depends_on=deps,assumptions=assumptions,proof_location=dict(file='theta_descent/main.tex',expanded='theta_descent/report.txt',section=f'TD{i}',sha256=sha(part),line_start=mt[:a].count('\n')+1,line_end=mt[:b].count('\n'),bytes=len(part)),sources=sources))

claim(1,'Finite tests recover coordinates over the prescribed field','An injective finite basis map with one separating test family rational on its columns has rational coordinates for every vector with rational test values.',[],ss('coord','coord_rat'),['Literal field embedding; common finite separating complex-linear tests; injective basis map.'])
claim(2,'The tested theta kernel descends','A coefficient form whose theta columns have rational values under separating tests has kernel equal to the complex span of its rational kernel, by Gaussian elimination.',[],ss('kernel','RowTest','FormsSpan','KerRational','KerRationalOfRowTest'),['The chosen K-basis maps to a complex basis; the fixed-field RowTest is supplied.'])
claim(3,'Rationality of the actual adjoint image','The metric identity implies star compatibility; Riesz vectors and the invertible rational Gram matrix prove the literal RatZ for rows and single lifts.',['TD1'],ss('range','star_compat','range_adjoint_rat','ratZOfTests')+ss('tests','RowTest','LiftTest','perpR','perpL','RatZOfTests')+ss('parts','RatZ'),['Exact coefficient-basis and K-valued metric identities; supplied row/lift tests on the same theta maps.'])
claim(4,'The adjoint cut is operator-stable','Adjoint closure and theta-kernel invariance preserve the actual adjoint image and its K-preimage; theta is injective on that image.',[],ss('stable','mem_range_adjoint_of_ker_stable','semilin_comp_eq_constr','jR_opR','jL_opL','cutStable')+ss('rows','eq_zero_of_mem_range_adjoint')+ss('cuts','KerStabR','KerStabL','AdjClosedR','AdjClosedL','CutStable'),['Finite-dimensional positive Hermitian spaces; actual coefficient forms, operator and adjoint-closure identities.'])
claim(5,'Exact finite group and adjoint equivariance','The finite group representation extends unitarily and intertwines theta and its adjoint; finite sums prove the literal group-algebra identities.',[],ss('level','opF','opV','opF_mul','opV_sum_single','j_opF','opV_mul','rho_mul','rho_one','rho_unitary','theta_rho','rho_adj','theta_opV','opV_adj','Hyp'),['Spanning coefficient form, rational invariant metric, group action and exact theta equivariance; target action unitary.'])
claim(6,'Rational idempotent level descent','For the actual rational idempotent, the level/adjoint intersection is the complex span of its rational preimage, and every level vector has an adjoint-image representative with the same theta image.',['TD3','TD5'],ss('level','opV_idem','mem_R','ker','range_opV','fix_of_idem','ratLev','dn')+ss('cuts','RatLev','DnLev','RatLevL','DnLevL'),['The same idempotent, theta equivariance and RatZ; self-adjointness of the level idempotent is unnecessary.'])
claim(7,'Character projector, upward level, and inverse convention','The character projector is explicitly idempotent and selects the stated character; central block intersection gives the actual upward and type conditions, retaining psi on rows and inverse psi on lifts.',['TD5'],ss('level','opV_lvlIdem','type','fixE','up','goodAt_idem','opF_goodAt_idem','opF_goodAt_type','goodAt_bot')+ss('rowlat','lvl','lvlA')+ss('cuts','UpLev','UpLevL'),['Characteristic zero and finite group; literal central block idempotent. Standard finite-character orthogonality is explicit background.'])
claim(8,'Common theta image and exact row Gram identity','The actual level/adjoint coordinate image and positive theta operator scalar on spanning spectral parts prove all H2 common-image clauses and the exact H4 identity.',['TD4','TD6','TD7'],ss('rows','uQ','iC_eq_comp','lin_uQ_cpt','gram_uQ','lin_uQ_injective','cutRows')+ss('cuts','IsoR','CrdZ','CoordinatesInGoodPart','ThmBop','PartsE','CutRows')+ss('parts','H2','H4pos','H4'),['Actual positive Gram n_P H_Q, exact RatLev/DnLev/UpLev, supplied ThmBop and PartsE, positive kappa and lambdas on the same realization.'])
claim(9,'The common row matrices are rational and coherent','One common RowTest yields the literal rowMat with I_base sigma(M_t)=I_t; it is bijective, is identity at the base, and gives exact coherent comparisons.',['TD1','TD2','TD8'],ss('mu','solve_spec','lin_single','ratMuOfRowTest')+ss('parts','kOf','kMat','solve','relMat','rowMatC','rowMat','RATmu')+ss('cx','relMat_bij','key_row','rowMat_bij','rowMat_base'),['The supplied common RowTest tests all actual theta columns; TD8 common image is used, not dimension equality.'])
claim(10,'Single lifts descend through the chosen principal basis','CutLifts gives exact H5 and ThmA; LiftTestB on both moving columns and chosen principal basis gives the literal rational bijective liftMat.',['TD1','TD4','TD8'],ss('lifts','uL','tC_eq','gram_uL','lin_uL_injective','cutLifts')+ss('th','lin_injective','ratThOfLiftTest')+ss('tests','LiftTestB')+ss('parts','w0C','liftMat','H5','ThmA','EWnorm')+ss('cuts','ThmAop','PartsW','CutLifts')+ss('cx','eW_inj','principal_form_injective','key_lift','liftMat_bij'),['Actual lift level and Gram identities, positive ThmAop and PartsW, principal complex basis with EWnorm, and LiftTestB including that basis.'])
claim(11,'Exact base-lift relation from containment','Containment of the actual base lift columns in the principal image plus principal injectivity and LiftTestB proves the extendedData matrix relation; the local containment follows from principal adjoint replacement and the supplied PLevW identity.',['TD1','TD3','TD5','TD6','TD7'],ss('base','dnLevL_of_ratZL','tC_single_mem','liftMatC_isRat','liftMatrix_computes_lift_rational','baseLevelLiftMatrix_solves_relation_extendedData')+ss('holds','Pre2','HoldsL'),['The same WeakCharacterisation.base.models and HoldsL realization; actual PLevW and test identities remain supplied. No full lift surjectivity needed for this endpoint.'])
claim(12,'Spectral orthogonality in the actual quotient metric','Commuting adjoint-closed operators are normal at every infinite place; spectral-label disjointness gives orthogonality in the actual quotient via unique orthogonal lifts.',['TD4'],ss('ortho','OkOp','oM_comm','oM_adj','eig_ratG','vE_tVg','Pq_tVg','adjCg','part_orthg')+ss('sep','okOp_opAll','majAt_eq_zero_of_mem_Qp_of_ne')+ss('rowlem','Pq_surj','XQ_quot')+ss('parts','PartsOrth'),['Actual positive class metric and maximal-CM matrix identities; exact Hecke/inertia adjoint closure, stable cut and disjoint source residue labels.'])
claim(13,'The weighted target metric is literal and positive','The weighted part-projection sum and distinguished-place Gram splice construct the exact source metric; orthogonality yields its part identities and min-weight lower bound.',['TD8','TD9','TD12'],ss('rowlat','partPr','rowXE')+ss('rowlem','sum_partPr','rowXE_spec')+ss('cx','partPr_eq','partPr_mem','partPr_self','partPr_other','sum_partPr_mulVec','rowXE_part','gramE_unit','XE_spec')+ss('principal','majAt_off','majAt_off_part')+ss('parts','H3'),['Actual rational direct sum, positive weights, TD12 at other places, and actual H3 at the distinguished place; no minimum for an empty part index and no quantitative lambda estimate.'])
claim(14,'The literal principal Hermitian lattice','The actual rowMat images of the full row lattices are the prescribed local lattices; PL9 glues them, and exact theta-image membership identifies the literal principal Hermitian lattice.',['TD9','TD13','PL9'],ss('principal','principalHermitianLattice','RR_lattice','principal_hermitian_lattice_good','mem_matLat_iff','RR_mem','RR_mem_span'),['Actual full projected lattices, finite twist support and base identity; no integral isometry or period-divisibility inference from rational bijectivity.'])
claim(15,'One normalization produces all fixed-field row tests','The same finite period formula, rational ratios and rational finite sums give one nonzero common test normalization when kappa is nonzero; when kappa=0 the unscaled tests already have zero rational theta values.',['TD5','TD7'],ss('normal','sum_gE','rat_of_formula','exists_good','exists_linearMap_eq_psiK','rowTestModel_of_scaled_values_rational','exists_embLL_mul_psiK_eq_vK_of_formulaAt','rowTest_of_choice')+ss('formula','LinK','InjK','ConstK','FormulaAt','Formula2K','SumRatK','RatioK'),['Compatible test choice/FieldOK, LinK and InjK, actual Formula2K, SumRatK, RatioK and ConstK on the same realization; these analytic and arithmetic suppliers remain.'])
claim(16,'Conjugation transport, uniform quantifiers and exact test boundary','Boolean conjugation transports separating tests to the exact embedding. Maxima taken in the source order prove the conditional rowTest_realisation; algebraicity alone is insufficient for fixed-field common tests.',['TD15'],ss('kernel','HasRationalTest','RowTestModel','twFun','untwFun','test_tw_iff','rowTest_toCx_iff')+[explicit_range('kernel','GlobalTheory.IndefiniteRowSideFullHecke.RationalRowTestKernel.example_not_HasRationalTest_one_I',25,37,'literal unnamed counterexample; descriptive locator name, not a Lean declaration name')]+ss('cxmodel','rowTest_toCx3')+ss('normal','rowTestModel_of_claims')+ss('realis','GlobalTheory.RowTest.rowTest_realisation')+ss('formula','HidaSetting','Big','Big.and','SumOKK'),['The source Boolean twist and emb0 identities; same-data Big hypotheses with thresholds in their literal order. Actual convergent tests, period/ratio/coefficient suppliers and positive theta identities remain.'])

remaining=[
 dict(interface='Actual common tests',scope='Same-data compatible choice/FieldOK, LinK/InjK, Formula2K, SumRatK and RatioK remain substantive. Algebraic VI/CA jets do not imply RowTest over the specified fixed field.'),
 dict(interface='Positive theta identities and types',scope='ThmBop/ThmAop, PartsE/PartsW and actual HoldsL/model suppliers remain; TD derives the exact common image and metric from them.'),
 dict(interface='Quantitative and global branches',scope='Positive eigenvalues do not provide quantitative lower/logarithmic estimates, GalD/dimension balance, congruence denominators, cohomological or prime-sum bounds.'),
]
targets=[]
for key,name,scope in [
 ('formula','LinK','Prove convergence and linearity of the actual period integrals for the same compatible choice; TD15 only uses the resulting linear functionals.'),
 ('formula','InjK','Prove the actual finite test family separates the Hilbert target with the specified uniform thresholds.'),
 ('formula','Formula2K','Reconstruct the unfolded finite period formula for the exact tuple, block projection, constants and test arguments.'),
 ('formula','RatioK','Prove the actual common normalization ratios lie in the prescribed coefficient field.'),
 ('sums','vK_mem','Reconstruct actual arithmetic coefficient suppliers used by the finite rational sum; finite field closure is only the last step.'),
 ('cuts','ThmBop','Supply the actual multi-theta theta-adjoint scalar identity on the specified type parts, with its positive factors. TD8 proves the downstream common-image/metric conclusion.'),
 ('cuts','ThmAop','Supply the actual single-lift theta-adjoint scalar identity on the same principal type parts.'),
 ('cuts','PartsE','Construct and identify the actual orthogonal type parts spanning the common row target.'),
 ('cuts','PartsW','Construct and identify the actual orthogonal type parts spanning every principal lift target.'),
 ('parts','GalD','Prove actual dimension balance and conjugate compatibility, independent of rational common-image construction.'),
]:
 t=src(key,name,'retained source target');t.update(id='TD-next-'+str(len(targets)+1),priority=3,scope=scope,remaining_human_scope=scope);targets.append(t)
completed=[]
for key,name,ids in [
 ('range','ratZOfTests',['TD3']),('mu','ratMuOfRowTest',['TD9']),('th','ratThOfLiftTest',['TD10']),
 ('stable','cutStable',['TD4']),('level','ratLev',['TD6']),('level','dn',['TD6']),('level','up',['TD7']),
 ('rows','cutRows',['TD8']),('lifts','cutLifts',['TD10']),
 ('base','baseLevelLiftMatrix_solves_relation_extendedData',['TD11']),
 ('sep','majAt_eq_zero_of_mem_Qp_of_ne',['TD12']),
 ('principal','principal_hermitian_lattice_good',['TD14']),
 ('normal','rowTest_of_choice',['TD15']),('normal','rowTestModel_of_claims',['TD16']),
 ('realis','GlobalTheory.RowTest.rowTest_realisation',['TD16']),
]:
 s=src(key,name);completed.append(dict(path=s['path'],declaration=s['declaration'],claims=ids,reason='Literal conditional endpoint reconstructed with exact upstream test, operator, type and realization assumptions retained.'))

hs=src('level','Hyp','literal five-field record audit')
audits=[dict(record=hs['declaration'],source=hs,field_count=5,fields=[dict(name=n,supplied_by='TD5',scope='Given the literal coefficient form, representation, invariant metric and target equivariance.')for n in ['sp','jr','iso','eq','u']])]
files=[dict(path=p,sha256=sha(b),bytes=len(b),lines=len(b.splitlines()),commit=PIN,url=f'{URL}/blob/{PIN}/{p}',verified_equal_to_pinned_git_blob=True)for p,b in sorted(cache.items())]
artifacts={n:dict(sha256=sha((ROOT/n).read_bytes()),bytes=(ROOT/n).stat().st_size)for n in ['main.tex','report.txt','build_provenance.py']}
links=sum(len(c['sources'])for c in claims);ranges={(s['path'],s['line_start'],s['line_end'],s['range_sha256'])for c in claims for s in c['sources']}
data=dict(artifact_version='0.18',component='theta_descent',repository=URL,commit=PIN,scope='Finite rational tests, actual adjoint/level cuts, common theta image and exact metric, literal rational row/lift comparisons and principal lattice, conditional common row-test normalization. Actual test/period/type/operator suppliers and quantitative bounds remain.',claim_count=len(claims),source_link_count=links,unique_claim_source_range_count=len(ranges),source_file_count=len(files),claims=claims,source_files=files,proof_artifacts=artifacts,record_audits=audits,retained_inputs=remaining,completed_targets=completed,independent_reviews=[],validation=dict(read_only_source_access=True,source_range_hashes_regenerated=True,lean_build_performed=False,pdf_build_performed=False))
for filename,reviewer,nums in [('theta_descent_TD1_8_review.txt','/root/class_rank',range(1,9)),('theta_descent_TD9_16_review.txt','/root/global_frame',range(9,17))]:
 rp=ROOT.parent/'reviews_v0_18'/filename
 if not rp.exists():continue
 raw=rp.read_bytes();content=raw.decode();chosen={c['id']:c['proof_location']['sha256']for c in claims if int(c['id'][2:])in nums}
 assert 'PASS'in content
 for cid,h in chosen.items():assert h in content,('review paragraph changed',filename,cid)
 data['independent_reviews'].append(dict(reviewer=reviewer,result='PASS',claim_ids=list(chosen),review_record='../reviews_v0_18/'+filename,review_record_sha256=sha(raw),paragraph_sha256=chosen,lean_replay=False))
for n,obj in [('provenance.json',data),('source_manifest.json',dict(artifact_version='0.18',component='theta_descent',repository=URL,commit=PIN,source_files=files,proof_artifacts=artifacts)),('next_targets.json',dict(artifact_version='0.18',repository=URL,commit=PIN,targets=targets,completed_targets=completed,retained_inputs=remaining))]:
 (ROOT/n).write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n')
out=['THETA DESCENT TD1–TD16',f'Repository {URL}',f'Commit {PIN}',f'{len(claims)} claims, {links} source links, {len(files)} pinned files.','']
for c in claims:
 out += [c['id']+': '+c['title'],'Proof paragraph SHA256 '+c['proof_location']['sha256']]
 for s in c['sources']:out += [f"  {s['declaration']} | {s['path']}:{s['line_start']}-{s['line_end']}",'  '+s['url'],f"  File {s['full_file_sha256']}; range {s['range_sha256']}"]
 out+=['']
(ROOT/'source_locators.txt').write_text('\n'.join(out)+'\n')
(ROOT/'next_targets.txt').write_text('\n'.join(['THETA DESCENT — RETAINED TARGETS','']+[f"{t['declaration']}\n{t['pinned_url']}\n{t['remaining_human_scope']}\n"for t in targets])+'\n')
print(json.dumps(dict(claims=len(claims),source_links=links,unique_ranges=len(ranges),source_files=len(files),next_targets=len(targets)),indent=2))
