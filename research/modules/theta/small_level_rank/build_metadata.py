from pathlib import Path
import hashlib, json, subprocess, re
root=Path('/workspace/scratch/368c004c3aea')
out=root/'work_v031/small_level_rank'
repo=root/'lean_source'
pin='7cbf7a0c32fca1badf05931879a37c3f8a2b03b4'
assert subprocess.check_output(['git','rev-parse','HEAD'],cwd=repo,text=True).strip()==pin
sha=lambda b:hashlib.sha256(b).hexdigest()
F='src/Formalism/'
D='src/Development/AbelianVarietyTheory/'
I=D+'Proofs/IwasawaDecomposition/'
G=D+'Proofs/GlobalInterpolation/'
T=D+'Definitions/GlobalTwisting/'
# Each group is cited in the prose; its individual ranges remain separately hash-bound.
specs=[
('S01',F+'SharpRestriction/GlobalTheoremInputs.lean',[(52,54,'SmallLevelRankEq')]),
('S02',F+'LocalRingCardinality/DataParams₂.lean',[(194,197,'dZ0; zeroSpaceRankAtPlace'),(208,208,'lifts')]),
('S03',F+'LocalRingCardinality/DataRows.lean',[(73,78,'Data.EE0; D0; onb0'),(123,153,'Data.Mj; Mt; MtL; jMt; thetaP'),(201,204,'thetaT; Zj')]),
('S04',F+'LocalToGlobal/Divisibility/GoodPartHermitianSpec.lean',[(17,32,'IsAbsIrrChar; chiIdem; idemOf; lvlIdem; goodAt'),(43,63,'subDim; subBasis; subE; imE; orthPr'),(116,141,'lvlE; lvlPr; lvlH; V0E; goodPartProjection; goodPartHermitianForm')]),
('S05',F+'LocalToGlobal/Divisibility/RowLat.lean',[(83,90,'blockProd; ZH; HasRes; partF'),(103,168,'vE; vPr; HV; Z0; zE; Pq; fE; lPr; Tl; cutZ; delZ; toF'),(176,198,'BlockDat.Ok'),(246,277,'lvl; lvlA; side; DefFam.Ok')]),
('S06',F+'LocalToGlobal/Divisibility/LiftLat.lean',[(129,130,'BlockDat.lE'),(184,191,'BlockHyp')]),
('S07',I+'LPrjSurjective.lean',[(9,12,'GlobalTheory.Mem.LiftProjOnto.lPrj_surjective')]),
('S08',F+'LocalToGlobal/Divisibility/LiftLatLemmas.lean',[(162,217,'lf_lvl_mul_good; lf_lvl_vE; lf_lPr_lE; lf_l_proj'),(219,239,'lf_lE_form; lf_cutLat_mul; lf_cut_nab'),(281,305,'lf_lvlNab_isLattice; lf_lPr_surj; lf_Tl_isLattice; lf_cutZ_le')]),
('S09',F+'LocalToGlobal/Columns/HeckeSp.lean',[(16,26,'eigAt; Occurs; eigSum; PairComm; SplitOver'),(504,508,'heckePolyOf; blockPoly'),(574,578,'heckePoly; HasBlocks'),(660,661,'blockSum')]),
('S10',F+'LocalToGlobal/Divisibility/InertRationalAdjoint.lean',[(22,61,'Typ3; HasRes3; resSet3; ixFin3; part3; DiffAt; Ok3'),(77,77,'Stable3'),(97,156,'tr3; base3; amb3; side3; DefFam3.Ok3; TypesSep3')]),
('S11',F+'LocalToGlobal/Divisibility/InertPartitionLePartF.lean',[(90,113,'blockPoly_eval_zero; excl3'),(115,197,'resSet3_finite; diffAt_of_mem_ixFin3; inert_parts_independent'),(208,260,'inert_parts_span_top'),(262,323,'sameTypes_self3'),(366,413,'stable3_rows; sameTypes_base3; side_well_formed; side_Types3')]),
('S12',F+'LocalToGlobal/IndefiniteForms/IndefSide.lean',[(16,62,'DefBase; DefSide'),(76,108,'DefSide.WF; Types')]),
('S13',F+'LocalToGlobal/IndefiniteForms/IndefSide.lean',[(241,269,'IndefData'),(300,313,'BaseTypeSubspacesMapOntoBothSides; RowLatticeBoundForBasis; DimensionsOfPartsAgree'),(345,361,'IndefRows')]),
('S14',F+'LocalToGlobal/IndefiniteForms/IndefUse.lean',[(109,142,'IndefRows.dQ_eq; dZ_eq; dW_eq; rankZ')]),
('S15',F+'LocalToGlobal/HilbertRowConditions/ColumnsFunctionAtSubspaces.lean',[(43,66,'RowSideFamily'),(108,113,'RowsHold0_3')]),
('S16',F+'LocalToGlobal/BaseRankEqOfRealisation.lean',[(21,29,'base_rank_eq_of_tied_level')]),
('S17',F+'LocalRingCardinality/PrincipalHermitianLattice.lean',[(38,46,'RowSide.RR; jEE; jEE_basis; jEE_norm'),(139,140,'BaseLevelRowSide')]),
('S18',F+'LocalToGlobal/NormalizedHeckeFactors/BaseRowsEqRecordRows.lean',[(20,40,'finrank_Mj_eq_dW; wf0; dW_eq_D'),(50,71,'base_rows_eq_record_rows; finrank_Mj_of_pin'),(75,108,'thetaP_surj; adjoint_injective; finrank_Zj_of_pin')]),
('S19',F+'LocalToGlobal/Divisibility/DivisionCompatibleToSub2Indef2.lean',[(18,40,'FamIn3.indef2; indefDown'),(233,243,'ThDef3'),(261,306,'DivDef3; DivRows3')]),
('S20',F+'LocalToGlobal/Divisibility/TupUsed.lean',[(19,32,'TupAllUsed; tupAllUsed_iff_cover'),(56,64,'ThTheta; ThThetaG'),(112,145,'DivRows3G; DivRows3G.toRows')]),
('S21',F+'LocalToGlobal/IndefiniteReal/RecTie.lean',[(189,189,'Used0')]),
('S22',F+'LocalToGlobal/Divisibility/RowSideTie.lean',[(80,119,'lH; lNab; lZ0; lPrj; DivisionCompatibilityData.eRR0/eMt/jW')]),
('S23',I+'LiftCuspFormSpaceThetaMapEqData.lean',[(19,38,'eW_jW; eW_injective; li_span'),(128,172,'theta_of; thDef3_thTheta')]),
('S24',T+'ColumnCompatibleSelection.lean',[(63,86,'Bundle; sel; selS; selP; selC; selB')]),
('S25',T+'SquareIntegrableColumnsCompatible.lean',[(86,107,'SquareIntegrableColumnsCompatible; ok1')]),
('S26',T+'CountsIrreducibilityConstants.lean',[(163,174,'P_hPA; P_hLamP; P_hDivG'),(215,222,'H_zL; LZeroConditionAtBundlePoints')]),
('S27',G+'SmallLevelRankEqClosedOfLevelProjectionSurjective.lean',[(13,47,'GlobalTheory.Top.smallLevelRankEq_closed_of_levelProjection_surjective')]),
('S28',G+'LPrjSurjAt.lean',[(8,17,'lPrj_surj_at; row_zL')]),
('S29',F+'LocalToGlobal/TieTwRecOf.lean',[(32,36,'selKOf; selIOf')]),
('S30',I+'ThetaMapHilbertModelEqConcreteThetaMapFamilyThre.lean',[(39,86,'GlobalTheory.Mem.ThetaRead3.thetaP_read')]),
('S31',I+'LiftLevelFormOrthogonalKilledByThetaMap.lean',[(18,51,'theta_eq_zero_of_orth'),(76,152,'thG_eq_zero_of_orth')]),
('S32',I+'LiftMatrixComputesLiftRational.lean',[(163,180,'lin_cpt; liftMatrix_computes_lift_rational'),(290,306,'liftWeight_complexPoint_eq_twist; levelFormCoordinateMap_levelZero')]),
('S33',D+'Definitions/AutomorphicMembership/StableIffCarrierEq.lean',[(81,91,'Pins; Holds'),(105,110,'liftForm'),(116,156,'Read'),(200,220,'ReadL')]),
('S34',I+'DivisionCompatibleAtReadIdentifications.lean',[(22,46,'GlobalTheory.divTied3_read')]),
('S35',F+'SharpRestriction/ParamsHeightRankConstant.lean',[(159,178,'Closed; Closed.and; Closed.imp')]),
('S36',F+'LocalToGlobal/ClassOfRecordOfChoice.lean',[(34,35,'WithChN'),(48,59,'D3; d3_a; closed_eps_le_one; closed_of_mem')]),
('S37',F+'LocalToGlobal/NormalizedHeckeFactors/RankZeroOfLevelThree.lean',[(10,32,'rank_zero_of_row_conditions')]),
('S38', 'src/Development/AutomorphicArithmetic/CharacterBoxes/DesWin.lean',[(11,31,'UpperTheory.Top.topDesWin')]),
('S38', 'src/Development/AutomorphicArithmetic/CharacterBoxes/ShapeWin.lean',[(27,49,'UpperTheory.Top.shapeWin')]),
('S39', F+'LocalToGlobal/IndefiniteRealisationChoice.lean',[(86,103,'PrimAll; rowsHold0_of; RkOf')]),
('S39', F+'LocalToGlobal/IndefiniteReal/RealTP.lean',[(22,34,'rows_transport; rowsHold0')]),
('S39', F+'LocalToGlobal/IndefiniteReal/BaseLiftsPackageOfPrimitiveLinks.lean',[(199,222,'PrimRows3')])]
sources=[];groups={}; cache={}
for group,path,rs in specs:
 p=repo/path;b=p.read_bytes()
 if path not in cache:
  blob=subprocess.check_output(['git','show',pin+':'+path],cwd=repo)
  assert b==blob,path
  cache[path]=b
 lines=b.splitlines(keepends=True)
 for a,z,decl in rs:
  assert 1<=a<=z<=len(lines),(path,a,z,len(lines))
  chunk=b''.join(lines[a-1:z]);sid=group+'-'+str(len(groups.get(group,[]))+1)
  entry={'id':sid,'group':group,'path':path,'declaration':decl,'line_start':a,'line_end':z,'sha256':sha(b),'range_sha256':sha(chunk),'range_bytes':len(chunk),'first_line':lines[a-1].decode().rstrip(),'verified_equal_to_pinned_git_blob':True,'url':f'https://github.com/CocoSgt/riemann-hypothesis-lean/blob/{pin}/{path}#L{a}-L{z}'}
  sources.append(entry);groups.setdefault(group,[]).append(sid)
tex=(out/'main.tex').read_bytes();ls=tex.splitlines(keepends=True)
titles={
'SLR1':'Actual level and good spaces are nested',
'SLR2':'Explicit right inverse and exact normalized orthogonal projection',
'SLR3':'Image lattice, cut lattice and exact integral boundary',
'SLR4':'Finite generalized-primary type decompositions on original coefficient spaces',
'SLR5':'Original rational lift rank and direct D0 comparison',
'SLR6':'Base-tuple theta square implies surjectivity and actual adjoint-image rank',
'SLR7':'Base Used0 restriction and bounded theta-factorization implication',
'SLR8':'Pointwise Bundle projection certificate and Closed zL with zero bound',
'SLR9':'Same-selected-base-row/theta producer cut implies original Closed SmallLevelRankEq'}
source_groups={
'SLR1':['S04','S05','S07'],
'SLR2':['S04','S05','S06','S08'],
'SLR3':['S05','S08'],
'SLR4':['S09','S10','S11','S12','S13','S14','S15'],
'SLR5':['S13','S14','S15','S16','S17','S18','S19','S22','S03'],
'SLR6':['S01','S02','S03','S17','S18','S19','S20','S21','S22'],
'SLR7':['S19','S20','S21','S22','S23','S30','S31','S32','S33','S34'],
'SLR8':['S05','S06','S07','S24','S25','S26','S27','S28','S29','S35','S36'],
'SLR9':['S01','S15','S19','S20','S21','S24','S25','S26','S27','S28','S29','S35','S36','S37','S38','S39']}
deps={'SLR1':[],'SLR2':['SLR1'],'SLR3':['SLR2'],'SLR4':[],'SLR5':['SLR4'],'SLR6':['SLR2','SLR5'],'SLR7':['SLR2'],'SLR8':['SLR1','SLR2'],'SLR9':['SLR4','SLR5','SLR6','SLR7','SLR8']}
claims=[]
for cid in titles:
 start=next(i for i,l in enumerate(ls,1) if l.strip()==('% BEGIN '+cid).encode())
 end=next(i for i,l in enumerate(ls,1) if l.strip()==('% END '+cid).encode())
 chunk=b''.join(ls[start-1:end])
 claims.append({'id':cid,'title':titles[cid],'introduced_in':'0.31','classification':'B','status':'complete human proof of stated conditional implication; actual producers retained explicitly','depends_on':deps[cid],'proof_location':{'file':'small_level_rank/main.tex','label':'claim:'+cid,'paragraph':cid,'line_start':start,'line_end':end,'sha256':sha(chunk),'bytes':len(chunk)},'source_groups':source_groups[cid],'sources':[s for s in sources if s['group'] in source_groups[cid]],'open_input_warning':'Actual RowSideFamily/Bundle and, where used, original RowsHold0_3 and base-tuple thTheta remain supplied. SLR7 proves factorization conditional on its four actual reading identities; it does not reconstruct their analytic producers.'})
prov={'schema':'rh-human-component-provenance/1','artifact_version':'0.31','date':'2026-11-22','source_commit':pin,'component':'small_level_rank','main_tex_sha256':sha(tex),'claims':claims,'source_groups':groups,'source_inventory':sources,'validation':{'pinned_blob_verified_files':len(cache),'source_ranges':len(sources),'all_source_ranges_exact':True,'new_lean_build':False,'independent_human_mathematical_proof':True},'scope_note':'The Lean proof is assumed fully checked and correct. Open obligations refer only to the human reconstruction.'}
(out/'provenance.json').write_text(json.dumps(prov,indent=2,ensure_ascii=False)+'\n')
loc=[f'Pinned source: {pin}',f'Main TeX SHA256: {sha(tex)}','']
for s in sources:
 loc.extend([f"{s['id']} | {s['declaration']}",f"{s['path']}:{s['line_start']}-{s['line_end']}",f"file_sha256={s['sha256']}",f"range_sha256={s['range_sha256']}",s['url'],''])
(out/'source_locators.txt').write_text('\n'.join(loc))
(out/'source_excerpt_inventory.json').write_text(json.dumps({'source_commit':pin,'sources':sources},indent=2,ensure_ascii=False)+'\n')
print(json.dumps({'main_tex_sha256':sha(tex),'claims':len(claims),'files':len(cache),'ranges':len(sources),'proof_hashes':{c['id']:c['proof_location']['sha256'] for c in claims}},indent=2))
