from pathlib import Path
import hashlib,json,subprocess,re
root=Path('/workspace/scratch/368c004c3aea')
out=root/'work_v032/rank_producer'; repo=root/'lean_source'
pin='7cbf7a0c32fca1badf05931879a37c3f8a2b03b4'
sha=lambda b: hashlib.sha256(b).hexdigest()
assert subprocess.check_output(['git','rev-parse','HEAD'],cwd=repo,text=True).strip()==pin
F='src/Formalism/'; D='src/Development/AbelianVarietyTheory/'
G=D+'Proofs/GlobalInterpolation/'; H=D+'BlockTheory/GlobalSignature/'
I=D+'Proofs/IwasawaDecomposition/'
S=F+'SharpRestriction/GlobalSchurBounds/'
specs=[
('R01',F+'LocalRingCardinality/DataLevel.lean',[(32,39,'upperUni; iwU'),(90,92,'dualSet'),(94,147,'ColLevel: lattice, local level and functional fields'),(149,182,'ColLevel: topology, original class and stabilizer maps')]),
('R01',F+'LocalRingCardinality/DataLevelD.lean',[(6,8,'LevelData')]),
('R01',F+'LocalRingCardinality/DataKernels.lean',[(14,23,'ColumnChain.cls, finite classes and stabilizers'),(203,204,'ColumnChain.StabZero')]),
('R02',F+'LocalRingCardinality/DataSpaces.lean',[(14,24,'CMData; sig'),(26,46,'HSpace including original self-dual L0'),(59,68,'SigOK; IsDefinite; IsPosDef'),(77,119,'Spaces: original base signatures and isometric inclusion')]),
('R02',F+'LocalRingCardinality/DataLevel.lean',[(48,75,'rank0; gram0; crd0; crdLat0; hermitianForm_base_coordinates')]),
('R03',S+'StandardLattice.lean',[(428,431,'SplitsF'),(443,472,'SmallOrderPrimeLogSumBound; ClassNumberFormula₂; Mu0Tie; Conclusion4f')]),
('R03',S+'TopDensityNGeSixteen.lean',[(95,103,'RankM; RankHyp; rank_formula_of_part_four')]),
('R04',F+'SharpRestriction/LevelLetterCocycles/DataN.lean',[(165,165,'NData.g_split')]),
('R04',F+'SharpRestriction/AdmissibleParameterJoins/SfromGLt.lean',[(68,102,'sum_ef; ef_one_of_card; ef_one_sub'),(129,143,'splits_sub')]),
('R04',F+'SharpRestriction/AdmissibleParameterJoins/SfromGLu.lean',[(12,18,'finrank_F_eq; splitsF_g')]),
('R05',F+'LocalRingCardinality/RhoDetPrimeEqMuTildeMulChiPow.lean',[(142,146,'D7.T_level; T_norm')]),
('R05',F+'LocalRingCardinality/IntCastDvdOfDvdIntegers.lean',[(49,98,'modT and T_mod_cond')]),
('R05',G+'MemLocLatOverLat.lean',[(687,715,'T_ne_g')]),
('R06',F+'LocalRingCardinality/SpanPowerMembership/PlacesOverNcardOfSplitInj.lean',[(548,565,'placesOver_ncard_of_frob: hypotheses and trivial Frobenius'),(641,662,'placesOver_ncard_of_art; placesOver_ncard_of_split')]),
('R06',F+'SharpRestriction/RamificationFrobenius/TotientGaloisClasses/HostFacts.lean',[(298,301,'HostRaw.frob_iff')]),
('R06',F+'SharpRestriction/AdmissibleParameterJoins/DIVfromGLz.lean',[(13,18,'level_prime_splits_totally_real')]),
('R07',F+'LocalRingCardinality/Params.lean',[(6,20,'Ranks bounds'),(28,44,'f; r; N; rS; rankY; sigY0')]),
('R07',F+'LocalRingCardinality/RankBoundMonotoneInDimension.lean',[(653,674,'baseSpace_posDef')]),
('R08',H+'SplittingProjection.lean',[(18,23,'IsSplitting'),(72,131,'dualLb; IsOverLattice; LocalAtT; HasOverLattice; IndexAtT'),(135,143,'SelfDualOverBase; IndexOverBase')]),
('R09',G+'MemLocLatOverLat.lean',[(106,160,'mem_of_count'),(404,437,'dual_loc; le_dualLb; nsmul_mem; finite_dualLb'),(442,511,'exists_local')]),
('R10',G+'MemLocLatOverLat.lean',[(535,577,'overLat; its completion and equality away from T'),(582,683,'exists_overLattice'),(717,722,'overLattice')]),
('R11',G+'MemLocLatOverLat.lean',[(250,391,'localAtT')]),
('R11',G+'SelfDualLatticeOverColumnBaseLattice.lean',[(8,9,'selfDualOverBase')]),
('R12',G+'LocalLevelRelIndexAtLevelPrimeSelfDual.lean',[(236,263,'local_level_relIndex_at_level_prime_selfDual')]),
('R12',G+'StabilizerIndex.lean',[(12,39,'index_field; index_stabRow and its finite-field orbit proof')]),
('R13',G+'LocalLevelRelIndexAtLevelPrimeSelfDual.lean',[(173,189,'relIndex_selfDual'),(195,234,'relIndex_at_g'),(265,335,'exists_glue; relIndex_level; indexKU_of_selfDualOverBase')]),
('R14',H+'SelfDualLatticeIndex.lean',[(11,43,'IsSelfDualLat; stabHat; levelU; IndexAt; StabiliserLevelIndexFormula'),(51,61,'factorT_pos; stabHat_le')]),
('R14',G+'RelIndexConjLevelVL.lean',[(14,49,'relIndex_conj_comm'),(192,216,'relIndex_conj_levelVL')]),
('R14',G+'ExistsFrameCm.lean',[(110,126,'exists_frame_cm statement and coordinate model'),(169,174,'exists_frame on original D')]),
('R14',G+'StabiliserSelfDualLatticeLevelIndexFormula.lean',[(11,14,'selfDualLatticeIndex_stabiliserLevelIndexFormula')]),
('R15',D+'Proofs/FoundationProofs/MassSelfDualLatticeFirstSpaceEq.lean',[(22,44,'card_eq_index_mul_mass'),(51,80,'exists_lattice'),(93,100,'mass_selfDualLattice_firstSpace_eq'),(102,135,'classNumber; classNumber_of_index')]),
('R16',D+'Proofs/FoundationProofs/GenusMassStdOfLandherrHasse.lean',[(9,14,'genusMassStd; genusMassStd_of_landherrHasse')]),
('R17',H+'ClassesDoubleCosets.lean',[(12,49,'CosetMass; stabHat; General; DefiniteSpaceClassStatement; ClassesAsDoubleCosets')]),
('R18',G+'DoubleCosetCount.lean',[(8,67,'card_fiber_mul_card_stab'),(69,89,'doubleCosetCount')]),
('R19',H+'ColumnStabiliser.lean',[(14,42,'colStab; mem_colStab; ColStabTrivialAt'),(47,63,'original stored stabilizer triviality'),(65,80,'map_colStab')]),
('R19',F+'LocalToGlobal/GlobalTheory/GL6/DiagonalSlopes/AdmissibleStabilisersOfCompatibleForms.lean',[(172,195,'triv; admS from compatible original forms')]),
('R20',D+'Proofs/FoundationProofs/ClassNumberAll.lean',[(11,12,'classNumber_all')]),
('R20',G+'LinkEx.lean',[(15,37,'GlobalTheory.Top.link_ex and its exact class-number/selector slots')]),
('R21',S+'TheoremThreeFamilyOfFormalDegreeInput.lean',[(29,34,'rankFormula_of_classNumber'),(60,74,'familyRankFormula_of_classNumber; chosenProviso_min')]),
('R22',F+'LocalToGlobal/GroupLattices/DownNaturalLevelZero.lean',[(12,31,'Forms0'),(71,92,'FormsTied.to0'),(94,100,'Joint0 and stronger same-carrier scope')]),
('R23',F+'LocalToGlobal/HermitianForms/TiedStep.lean',[(70,103,'ClsTied; ValTied.eY; ValTied.Fi')]),
('R23',F+'LocalToGlobal/HermitianForms/FormsTied.lean',[(128,132,'Mu0_iff')]),
('R24',S+'GlobalRankLatticeProofs/UnitTraceSumBounds/RankConditionsOfLayerTwo.lean',[(35,62,'cspan_eq; valCEquiv; finrank_valC'),(105,123,'fiC_eq_pi statement and trivial stabilizer setup'),(160,224,'extension of freely assigned original coefficient values'),(230,256,'finrank_lowest_forms_space')]),
('R25',S+'GlobalRankLatticeProofs/UnitTraceSumBounds/RankConditionsOfLayerTwo.lean',[(258,289,'card_ssIdx_eq; actual weight shift; mu0Tie_of_sym'),(295,297,'rank_conditions_of_layer_two')]),
('R26',S+'GeneralLinearActions/GapAtLeast.lean',[(10,30,'stdForm; stdLat; massI; vand; facProd; dimV'),(56,95,'IsUnitri; idxLoc; idxColLoc; idxPi; duStarP; uColR; duStarU')]),
('R26',F+'LocalToGlobal/HermitianForms/BothSym.lean',[(27,40,'ColsTiedSym and car0')]),
('R27',F+'LocalRingCardinality/RhoDetPrimeEqMuTildeMulChiPow.lean',[(342,346,'colsS; duS')]),
('R27',S+'StandardLattice.lean',[(652,660,'FactDuStar; FactDstar; exact original family extra fields')]),
('R27',F+'LocalRingCardinality/DataExtra.lean',[(40,43,'Extra.lev'),(87,90,'Extra.duStar_def; Dstar_def')]),
('R28',I+'ExistsStandardColumnComparisonsTrueColumns.lean',[(20,72,'colsTiedSym_std, inherited TG12 exact scope')]),
('R29',F+'LocalToGlobal/ThresholdSelection.lean',[(9,15,'TSelF; TSel; TSelF.tiedRec')]),
('R29',F+'LocalToGlobal/ClassRec.lean',[(21,31,'RecT.T')]),
('R29',F+'LocalToGlobal/ClassSK.lean',[(15,22,'TiedDataSK extends actual LinkedFamilyData')]),
('R29',F+'LocalToGlobal/ClassS.lean',[(27,35,'LinkedFamilyData.cols and original extra')]),
('R30',D+'Definitions/GlobalTwisting/ColumnCompatibleSelection.lean',[(63,86,'Bundle and same-record RawSel selectors')]),
('R31',F+'LocalToGlobal/ClassOfRecordOfChoice.lean',[(34,35,'WithChN'),(61,62,'tied_families_of_choice')]),
('R32',F+'SharpRestriction/ParamsHeightRankConstant.lean',[(159,178,'Closed; Closed.and; Closed.imp')]),
('R32',S+'GlobalRankLatticeProofs/UnitTraceSumBounds/ClosedRankTiesFC2S.lean',[(11,21,'rankTiesF_of_C2S; closed_rankTiesF_C2S')]),
('R33',D+'Definitions/GlobalTwisting/ValidForConstructedPointClassesEventuallyWorking.lean',[(108,109,'RawSel'),(222,238,'Link with positivity; clsP'),(250,257,'Built; QOf; cls'),(274,282,'cls_at; pick; pick_isSel')]),
('R33','src/Development/AutomorphicArithmetic/CharacterBoxes/ClassSel.lean',[(14,28,'classSel uses the literal cls and pick')]),
('R33','src/Development/AutomorphicArithmetic/CharacterBoxes/ShapeWin.lean',[(42,48,'target intersection; forgetful projection; same selector passed to link_ex')])
]
cache={};sources=[];groups={}
for group,path,ranges in specs:
    b=(repo/path).read_bytes()
    if path not in cache:
        blob=subprocess.check_output(['git','show',pin+':'+path],cwd=repo)
        assert b==blob,path
        cache[path]=b
    lines=b.splitlines(keepends=True)
    for a,z,decl in ranges:
        assert 1<=a<=z<=len(lines),(path,a,z,len(lines))
        chunk=b''.join(lines[a-1:z]);sid=f'{group}-{len(groups.get(group,[]))+1}'
        s={'id':sid,'group':group,'path':path,'declaration':decl,'line_start':a,'line_end':z,'full_file_sha256':sha(b),'sha256':sha(b),'range_sha256':sha(chunk),'range_bytes':len(chunk),'first_line':lines[a-1].decode().rstrip(),'verified_equal_to_pinned_git_blob':True,'url':f'https://github.com/CocoSgt/riemann-hypothesis-lean/blob/{pin}/{path}#L{a}-L{z}'}
        sources.append(s);groups.setdefault(group,[]).append(sid)
tex=(out/'main.tex').read_bytes();lines=tex.splitlines(keepends=True)
titles={
'RMP1':'Original base, prime splitting, positive signature and exact level fields',
'RMP2':'Actual local discriminant modules have two simple factors',
'RMP3':'Literal self-dual overLat and preservation by the original level',
'RMP4':'Exact T-local index from a nonzero functional stabilizer',
'RMP5':'Auxiliary, global and arbitrary-self-dual-base index formula',
'RMP6':'Exact first-space mass from the existing uniform mass proof',
'RMP7':'Actual genus/class dictionary and finite trivial original level stabilizers',
'RMP8':'Full original ClassNumberFormula₂ by finite double-coset fiber counting',
'RMP9':'Literal Mu0Tie from original Forms0 and exact weight shift',
'RMP10':'Pointwise original RankM and stored dstar compatibility',
'RMP11':'Original Closed RankM on the selected construction class and actual target intersection'}
source_groups={
'RMP1':['R01','R02','R03','R04','R05','R06','R07'],
'RMP2':['R01','R08','R09'],
'RMP3':['R01','R08','R09','R10','R11'],
'RMP4':['R11','R12'],
'RMP5':['R12','R13','R14','R26'],
'RMP6':['R02','R07','R15','R16','R26'],
'RMP7':['R01','R15','R17','R18','R19'],
'RMP8':['R03','R15','R18','R20','R21'],
'RMP9':['R22','R23','R24','R25','R26'],
'RMP10':['R03','R26','R27','R28'],
'RMP11':['R20','R21','R29','R30','R31','R32','R33']}
deps={
'RMP1':['MF1','DR1'],
'RMP2':['RMP1','MF1','DR1'],
'RMP3':['RMP2','LP1'],
'RMP4':['RMP3'],
'RMP5':['RMP1','RMP3','RMP4','DR1','GV1','GV12'],
'RMP6':['RMP1','RMP3','MF6','MF14','MF18','MF19'],
'RMP7':['RMP1','RMP3','RMP6','LP1','MF3','GV11','CR4','RSL7'],
'RMP8':['RMP5','RMP6','RMP7'],
'RMP9':['RMP7','CB2','CB3','IW3','CR1','CR2','CR5','CR6'],
'RMP10':['RMP8','RMP9'],
'RMP11':['RMP10']}
claims=[]
for cid in titles:
    a=next(i for i,l in enumerate(lines) if l.strip()==f'% BEGIN {cid}'.encode())
    z=next(i for i,l in enumerate(lines) if l.strip()==f'% END {cid}'.encode())
    chunk=b''.join(lines[a:z+1])
    claims.append({'id':cid,'title':titles[cid],'introduced_in':'0.32','classification':'B','status':'complete human proof on its stated original supplied data; no independent source-existence assertion','depends_on':deps[cid],'proof_location':{'file':'rank_producer/main.tex','label':'claim:'+cid,'line_start':a+1,'line_end':z+1,'sha256':sha(chunk),'bytes':len(chunk)},'source_groups':source_groups[cid],'sources':[s for s in sources if s['group'] in source_groups[cid]]})
inh=[
('class_rank/main.tex',['CR1','CR2','CR4','CR5','CR6']),
('geometric_volumes/main.tex',['GV1','GV11','GV12']),
('mass_formula/main.tex',['MF1','MF3','MF4','MF6','MF14','MF18','MF19']),
('lattice_patching/main.tex',['LP1']),
('decorated_realization/main.tex',['DR1']),
('terminal_geometry/main.tex',['TG12']),
('second_layer_global/main.tex',['RSL7']),
('design_existence/main.tex',['DEX5','DEX7']),
('integral_weyl/integral_weyl_section.tex',['IW3'])]
inherited=[]
for path,ids in inh:
    p=root/'reconstruction_v031'/path
    inherited.append({'path':'reconstruction_v031/'+path,'claim_ids':ids,'sha256':sha(p.read_bytes()),'role':'inherited human proof; no claim to reconstruct its complete upstream proof again'})
# CB2/CB3 are durably bound to the cumulative v0.31 proof if no standalone path is assumed.
cum=list((root/'reconstruction_v031').glob('*.tex'))
for p in cum:
    if b'CB2' in p.read_bytes() and b'CB3' in p.read_bytes():
        inherited.append({'path':str(p.relative_to(root)),'claim_ids':['CB2','CB3'],'sha256':sha(p.read_bytes()),'role':'durable cumulative human coefficient-basis/Weyl dimension text binding'})
        break
prov={'schema':'rh-human-component-provenance/1','artifact_version':'0.32','date':'2026-11-22','source_commit':pin,'component':'rank_producer','main_tex_sha256':sha(tex),'claims':claims,'source_groups':groups,'source_inventory':sources,'inherited_proof_inputs':inherited,'external_input_scope':'Inherited MF4 Hasse–Minkowski theorem at its already checked scope. No new external theorem certificate; no Tamagawa theorem used by RMP6.','validation':{'pinned_blob_verified_files':len(cache),'source_ranges':len(sources),'all_source_ranges_exact':True,'claim_proof_blocks':len(claims),'new_lean_build':False,'independent_human_mathematical_proof':True},'scope_note':'The Lean proof is assumed fully checked and correct. Open obligations refer only to human reconstruction. Construction-class membership supplies the literal Bundle selector; the shared construction of a common family in that class remains DESIGN_CHOICES_COMMON.'}
(out/'provenance.json').write_text(json.dumps(prov,indent=2,ensure_ascii=False)+'\n')
loc=[f'RMP1–RMP11 source provenance; pinned commit {pin}',f'main.tex SHA256 {sha(tex)}','']
for s in sources:loc.extend([f"{s['id']} | {s['declaration']}",f"{s['path']}:{s['line_start']}-{s['line_end']}",f"file_sha256={s['full_file_sha256']}",f"range_sha256={s['range_sha256']}",s['url'],''])
(out/'source_locators.txt').write_text('\n'.join(loc))
closure={
'schema':'rh-human-component-closure/1','artifact_version':'0.32','component':'rank_producer','source_commit':pin,'proof_sha256':sha(tex),'proof_claims':list(titles),
'closed':[
{'id':'ORIGINAL_SELF_DUAL_OVER_BASE','by':['RMP1','RMP2','RMP3'],'scope':'Every supplied original D7, LevelData and word, with the original local functional selecting the split factor; no new family-existence claim.'},
{'id':'ORIGINAL_STABILISER_LEVEL_INDEX','by':['RMP4','RMP5'],'scope':'Original index formula for the constructed self-dual overLat and every other supplied full self-dual lattice whose stabilizer contains the same U.'},
{'id':'ORIGINAL_CLASS_NUMBER_FORMULA_2','by':['RMP6','RMP7','RMP8'],'scope':'Every supplied D7 and LevelData; original cls 0 and normalization, including all hypotheses of ClassNumberFormula₂. The proof is stronger and does not need GBig.'},
{'id':'ORIGINAL_MU0TIE_CONSUMER','by':['RMP9'],'scope':'Original Forms0 on same D and word, with actual stored cls 0, stabilizers, Fi/eY and weights; no integral or metric equality claimed.'},
{'id':'DESIGN_RANKM_CLOSED','by':['RMP10','RMP11'],'scope':'Closed original RankM on Cdes=WithTw(WithSm(Cprime)), Cprime=WithChN(A intersect G.cls(lambda)), for A=cls(Q,Lk,Erow), Bd=Bundle. Membership supplies RawSel Bundle by cls_at/pick, hence the same TSel; there is no independent selector premise. epsilon1=1, all transported bound components zero, inner threshold Fm.x1+1. The existence of a common family in this class remains DESIGN_CHOICES_COMMON.'}],
'remaining':[
{'id':'DESIGN_CHOICES_COMMON','classification':'C','contract':'Construct the selected common arithmetic family satisfying cls(Q,Lk,Erow) and the other common conditions. Membership in this class already supplies its actual Bundle and selector; RMP11 proves the required rank property of every member without establishing nonemptiness.','relation':'shared upstream producer, not an additional independent RankM obligation'}],
'sufficient_rules':[
{'conclusion':'ORIGINAL_CLASS_NUMBER_FORMULA_2','requires':['SUPPLIED_D7','SUPPLIED_LEVEL_DATA','CERT_RMP1_RMP8'],'logic':'AND'},
{'conclusion':'ORIGINAL_RANKM_POINTWISE','requires':['SUPPLIED_D7','SUPPLIED_LEVEL_DATA','SAME_D_FORMS0_FOR_EVERY_WORD','CERT_RMP1_RMP10'],'logic':'AND'},
{'conclusion':'DESIGN_RANKM_CLOSED_IN_GENERAL_SELECTED_CONTEXT','requires':['SAME_SELECTED_TSEL_ON_A','CERT_RMP11'],'logic':'AND'},
{'conclusion':'DESIGN_RANKM_CLOSED','requires':['A_IS_ORIGINAL_CONSTRUCTION_CLASS_WITH_BD_BUNDLE','CERT_RMP11'],'logic':'AND','note':'Class membership implies cls_at and pick; class nonemptiness is not needed to prove Closed.'}],
'nonlogical_shared_links':[
{'from':'DESIGN_CHOICES_COMMON','to':'SECOND_LAYER_COMPATIBLE_SELECTION','reason':'May use same Bundle; no assertion that a separate existing second-layer witness can be exchanged for the selected Bundle.'},
{'from':'SAME_D_FORMS0_FOR_EVERY_WORD','to':'TG12','reason':'TG12 is a sufficient pointwise supplier on actual true-column inputs with Ok, Pins, Laws and Later. It does not create those arithmetic inputs.'}],
'quantifier_guards':[
'Class-number proof works at every x>Fm.x1 using the actual ex.lev; no outer epsilon restriction is needed.',
'TSel threshold is selected before x,i,u; only max with Fm.x1+1 is added.',
'RawSel Bundle selects exactly Bundle.R, with threshold Fm.x1, so Fm.x1+1 suffices.',
'For the actual A=cls(Q,Lk,Erow), Bd=Bundle, Link.pos discharges QOf positivity and cls_at/pick supplies RawSel on each class member; no independent selector existence is assumed.',
'The actual Cprime is WithChN(A intersect G.cls(lambda)); forgetting its literal conjunctions preserves the same family and selected records.',
'For a weaker Closed eventual Forms0 supplier retain its epsilon and transported bound instead of resetting them to zero.',
'No GBig, Duty, ChiFin0, theta square, TuSize, or metric comparison is required in this rank consumer.'],
'peer_review':'pending independent review; proof hashes and source ranges are stable unless corrections are requested'}
(out/'closure.json').write_text(json.dumps(closure,indent=2,ensure_ascii=False)+'\n')
report='''RMP1–RMP11: original rank producer, v0.32

Outcome
-------
The complete class-number formula is reconstructed on the original supplied D7/LevelData. Its self-dual enlargement is the literal overLat of Lb, its finite class set is the original cls 0 through Lv.y_bij, and its local index is exactly idxPi*(T^k-1)^f. RMP6 uses MF18–MF19 to identify the mass of the constructed self-dual lattice with massI; no new Tamagawa assertion is used.

The new local argument uses the original prime-order functional and total discriminant index. At each place over T, the two split discriminant components have equal length and both are nonzero. The total index T^(2f) and the f split places force each length to be one. Taking the selected dual component gives the actual self-dual enlargement, and fixing the nonzero row gives T^k-1 rather than a projective-line count. Two distinct upper-unitriangular auxiliary reductions kill every finite rational stabilizer. This avoids GBig in the stronger proof while satisfying the original conditional ClassNumberFormula₂.

RankM and exact remaining boundary
---------------------------------
RMP9 identifies the literal Mu0 with arbitrary Weyl values on the same stored cls 0 using Forms0.val0.Fi/eY and cls0.stabI_range. Its weight shift gives exactly the source Vandermonde quotient dimV. The product is duStarU, and the actual family extra record identifies it with stored A.duStar. No replacement integral lattice or metric comparison is asserted.

RMP11 first proves the implication from an original TSel, whose RecT.T.cols supplies the same-D Forms0 for every word. For the selected A=cls(Q,Lk,Erow), Bd=Bundle, membership gives Link.pos and the pointwise QOf witnesses. Thus cls_at/pick supplies RawSel Bundle and its sel uses exactly Bundle.R. No independent selector premise remains in DESIGN_RANKM_CLOSED. The actual target class is Cprime=WithChN(A intersect G.cls(lambda)), then Cdes=WithTw(WithSm Cprime). Literal forgetful projections preserve the same family. Choose epsilon1=1, K=0 and threshold Fm.x1+1. The shared DESIGN_CHOICES_COMMON producer still constructs a common family in this class; the universal Closed property does not assert class nonemptiness. A weaker Closed forms supplier must retain its own epsilon/K bounds.

All 11 claims are completed B arguments at their stated conditional scopes, not open B placeholders. Existing MF4 Hasse–Minkowski is inherited through MF18. No new A, C or D leaf is asserted by this component. Formal Lean correctness is assumed; this audit is exclusively about human reconstruction.
'''
(out/'report.txt').write_text(report+f'\nProof SHA256: {sha(tex)}\nSource files: {len(cache)}; exact source ranges: {len(sources)}; proof blocks: {len(claims)}.\n')
print(json.dumps({'main_sha256':sha(tex),'provenance_sha256':sha((out/'provenance.json').read_bytes()),'closure_sha256':sha((out/'closure.json').read_bytes()),'claims':len(claims),'source_files':len(cache),'source_ranges':len(sources)},indent=2))
