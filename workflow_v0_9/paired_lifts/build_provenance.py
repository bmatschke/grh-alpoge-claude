"""Regenerate RL exact pinned-source correspondence; no Lean invocation or edits."""
from pathlib import Path
import hashlib
import json
import re
import subprocess

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[1] / 'alpoge-rh'
PIN = '7cbf7a0c32fca1badf05931879a37c3f8a2b03b4'
URL = 'https://github.com/CocoSgt/riemann-hypothesis-lean'
PATHS = {'objseg': 'src/Formalism/SharpRestriction/GrowthBounds/ObjSeg.lean',
 'setting': 'src/Formalism/SharpRestriction/GrowthBounds/UnramifiedQuadraticSetting.lean',
 'bridge': 'src/Formalism/SharpRestriction/GrowthBounds/ObjBridge.lean',
 'std': 'src/Formalism/SharpRestriction/GrowthBounds/BinomialRatio/Transported.lean',
 'pair': 'src/Formalism/SharpRestriction/GrowthBounds/BinomialRatio/PairLift.lean',
 'block_form': 'src/Formalism/SharpRestriction/GrowthBounds/CoarseMultiplicity/RestBlockForm.lean',
 'bf': 'src/Formalism/SharpRestriction/GrowthBounds/CoarseMultiplicity/BFDefs.lean',
 'monomial': 'src/Formalism/SharpRestriction/GrowthBounds/CoarseMultiplicity/IoBlockMonomial.lean',
 'eig': 'src/Formalism/SharpRestriction/GrowthBounds/CoarseMultiplicity/TopOddNeEnd.lean',
 'balanced': 'src/Formalism/SharpRestriction/GrowthBounds/CoarseMultiplicity/DegSplit.lean',
 'fiber': 'src/Formalism/SharpRestriction/GrowthBounds/CoarseMultiplicity/SymVarInlFst.lean',
 'gtheta': 'src/Formalism/SharpRestriction/GrowthBounds/CoarseMultiplicity/GTheta.lean',
 'otherE': 'src/Formalism/SharpRestriction/GrowthBounds/CoarseMultiplicity/OtherEFree.lean',
 'chain': 'src/Formalism/SharpRestriction/GrowthBounds/CoarseMultiplicity/ChainEmbInj.lean',
 'sat': 'src/Formalism/SharpRestriction/GrowthBounds/CoarseMultiplicity/SatBlock.lean',
 'factorial': 'src/Formalism/SharpRestriction/GrowthBounds/CoarseMultiplicity/FactAbs.lean',
 'expfact': 'src/Formalism/SharpRestriction/GrowthBounds/CoarseMultiplicity/ExpFactIoExp.lean',
 'charzero': 'src/Formalism/SharpRestriction/GrowthBounds/CoarseMultiplicity/CharZeroOfW.lean',
 'leading': 'src/Formalism/SharpRestriction/GrowthBounds/CoarseMultiplicity/LeadingExponentHomogeneous.lean',
 'coarse': 'src/Formalism/SharpRestriction/GrowthBounds/CoarseMultiplicity/BFCoarse.lean',
 'mult': 'src/Formalism/SharpRestriction/GrowthBounds/CoarseMultiplicity/CoarseMultAt.lean',
 'true': 'src/Formalism/SharpRestriction/GrowthBounds/CoarseMultiplicity/BFTrueDeg.lean',
 'blockmaps': 'src/Formalism/SharpRestriction/GrowthBounds/CoarseMultiplicity/MemIntPolOfCoeff.lean',
 'orth': 'src/Formalism/SharpRestriction/GrowthBounds/CoarseMultiplicity/IoBlockEqSum.lean',
 'prod': 'src/Formalism/SharpRestriction/GrowthBounds/CoarseMultiplicity/IoBlockSupported.lean',
 'globalnorm': 'src/Formalism/SharpRestriction/GrowthBounds/CoarseMultiplicity/LogLeOfLeSq.lean',
 'form': 'src/Formalism/SharpRestriction/GrowthBounds/CoarseMultiplicity/FtFockZeroLeft.lean',
 'integral': 'src/Formalism/SharpRestriction/GrowthBounds/CoarseMultiplicity/FactorialExponentEqProd.lean',
 'colnum': 'src/Formalism/SharpRestriction/GrowthBounds/StandardPolynomials/ColNumDef.lean',
 'colnumproof': 'src/Formalism/SharpRestriction/GrowthBounds/StandardPolynomials/ColXNum.lean',
 'cols': 'src/Formalism/SharpRestriction/GrowthBounds/StandardPolynomials/ColsS.lean',
 'colmatch': 'src/Formalism/SharpRestriction/GrowthBounds/StandardPolynomials/ColXPH.lean',
 'colcount': 'src/Formalism/SharpRestriction/GrowthBounds/StandardPolynomials/ColXSum.lean',
 'coltop': 'src/Formalism/SharpRestriction/GrowthBounds/StandardPolynomials/ColTop.lean',
 'coldef': 'src/Formalism/SharpRestriction/GrowthBounds/StandardPolynomials/ColsDef.lean',
 'span': 'src/Formalism/SharpRestriction/GrowthBounds/StandardPolynomials/LatticeLeSpanPsiImage.lean',
 'rawdef': 'src/Formalism/SharpRestriction/GrowthBounds/CoarseMultiplicity/CoarseMultiplicityAtIdentity.lean',
 'rawasm': 'src/Formalism/SharpRestriction/GrowthBounds/CoarseMultiplicity/RestRawTail1Of.lean',
 'key': 'src/Formalism/SharpRestriction/GrowthBounds/CoarseMultiplicity/KeyMinorDvd.lean',
 'keyone': 'src/Formalism/SharpRestriction/GrowthBounds/CoarseMultiplicity/KeyOne.lean',
 'localres': 'src/Formalism/SharpRestriction/GrowthBounds/CoarseMultiplicity/Loc4ResOfLine.lean',
 'localdiv': 'src/Formalism/SharpRestriction/GrowthBounds/CoarseMultiplicity/Loc4DivOf.lean',
 'locallift': 'src/Formalism/SharpRestriction/GrowthBounds/CoarseMultiplicity/LiftSubstStart.lean',
 'multiplicities': 'src/Formalism/SharpRestriction/GrowthBounds/StandardPolynomials/MultMk.lean',
 'hook': 'src/Formalism/SharpRestriction/GrowthBounds/StandardPolynomials/TopKeyFormSelfSoft.lean',
 'rig': 'src/Formalism/SharpRestriction/GrowthBounds/StandardPolynomials/NdHomSingle.lean',
 'standard': 'src/Formalism/SharpRestriction/GrowthBounds/StandardPolynomials/StdPolyEq.lean',
 'head': 'src/Formalism/SharpRestriction/GrowthBounds/StandardPolynomials/SymFamilyWordEqHeadMulMonomial.lean',
 'totdeg': 'src/Formalism/SharpRestriction/GrowthBounds/StandardPolynomials/RigFactorWeightedHomogeneousLetter.lean',
 'pre': 'src/Formalism/SharpRestriction/GrowthBounds/StandardPolynomials/ColumnPolynomialCovectorZero.lean',
 'roomdef': 'src/Formalism/SharpRestriction/GrowthBounds/StandardPolynomials/RestRoom.lean',
 'room': 'src/Formalism/SharpRestriction/GrowthBounds/StandardPolynomials/ThresholdStandardSeventeen.lean',
 'factor': 'src/Formalism/SharpRestriction/GrowthBounds/StandardPolynomials/YcondFactor.lean',
 'reblock': 'src/Formalism/SharpRestriction/GrowthBounds/StandardPolynomials/SegmentBlockOfMonomial.lean',
 'quotients': 'src/Formalism/SharpRestriction/GrowthBounds/StandardPolynomials/BlockYZeroLeOfBound.lean',
 'binomial': 'src/Formalism/SharpRestriction/GrowthBounds/StandardPolynomials/DensitySumsAndDomination.lean',
 'rowinc': 'src/Formalism/SharpRestriction/GrowthBounds/StandardPolynomials/YcondCongr.lean',
 'rowproof': 'src/Formalism/SharpRestriction/GrowthBounds/StandardPolynomials/RecursionWithDensities.lean',
 'segcore': 'src/Formalism/SharpRestriction/GrowthBounds/StandardPolynomials/RestSegCoreOfNum.lean',
 'glue': 'src/Formalism/SharpRestriction/GrowthBounds/StandardPolynomials/TCGlue.lean',
 'coredef': 'src/Formalism/SharpRestriction/GrowthBounds/StandardPolynomials/TCoreDef.lean',
 'numdef': 'src/Formalism/SharpRestriction/GrowthBounds/StandardPolynomials/TCNumDef.lean',
 'num': 'src/Formalism/SharpRestriction/GrowthBounds/StandardPolynomials/TCXNum.lean',
 'factor_sys': 'src/Formalism/SharpRestriction/GrowthBounds/StandardPolynomials/MultidegAdd.lean',
 'core': 'src/Formalism/SharpRestriction/GrowthBounds/StandardPolynomials/ZeroOfMultideg.lean',
 'assembly': 'src/Formalism/SharpRestriction/GrowthBounds/StandardPolynomials/RestAssumptionsOfThreeInterfaces.lean',
 'cleanup': 'src/Formalism/SharpRestriction/GrowthBounds/CoarseMultiplicity/Lemma44IdentityOfRawTail.lean',
 'flat': 'src/Formalism/SharpRestriction/GrowthBounds/CoarseMultiplicity/MulMatQOne.lean',
 'flatpair': 'src/Formalism/SharpRestriction/GrowthBounds/CoarseMultiplicity/TestFlat.lean',
 'ximap': 'src/Formalism/SharpRestriction/GrowthBounds/CoarseMultiplicity/LaTwInvT.lean',
 'paired': 'src/Formalism/SharpRestriction/GrowthBounds/CoarseMultiplicity/PairedLiftAtOfIdentity.lean',
 'ord': 'src/Formalism/SharpRestriction/GrowthBounds/BinomialRatio/TopDegreeLeTwoB.lean',
 'gap': 'src/Formalism/SharpRestriction/GrowthBounds/BinomialRatio/CoarseDegreeAlternative.lean',
 'height': 'src/Formalism/SharpRestriction/GrowthBounds/ProjectionLemmaBaseLevel.lean'}
PREFIX = r'(?:@\[[^\n]*\]\s*)?(?:(?:private|protected|noncomputable)\s+)*'
DECL = re.compile(r'^'+PREFIX+r'(?:def|abbrev|theorem|lemma|structure|class|instance)\s+(\S+)')
BOUND = re.compile(r'^'+PREFIX+r'(?:def|abbrev|theorem|lemma|structure|class|instance|namespace|section|end|variable|open|include|omit|attribute|set_option)\b')
files = {}
for key, path in PATHS.items():
    raw = (REPO/path).read_bytes()
    assert raw == subprocess.check_output(['git','-C',str(REPO),'show',f'{PIN}:{path}']), ('unpinned bytes',path)
    lines = raw.splitlines(keepends=True)
    stack, declarations = [], []
    for i, raw_line in enumerate(lines):
        line = raw_line.decode().rstrip('\r\n')
        if m := re.match(r'^namespace\s+(\S+)',line):
            stack.append(('namespace',m[1]))
        elif m := re.match(r'^(?:noncomputable\s+)?section(?:\s+(\S+))?\s*$',line):
            stack.append(('section',m[1]))
        elif m := re.match(r'^end(?:\s+(\S+))?\s*$',line):
            assert stack, (path,i+1,'end without opening')
            kind,label=stack.pop()
            assert not m[1] or m[1]==label, (path,i+1,label,m[1])
        elif m := DECL.match(line):
            ns='.'.join(label for kind,label in stack if kind=='namespace')
            declarations.append((m[1],i,ns+'.'+m[1] if ns else m[1]))
    assert all(kind == 'section' and label is None for kind, label in stack), (path,'unclosed namespace')
    files[key]={'path':path,'sha256':hashlib.sha256(raw).hexdigest(),'bytes':len(raw),
                'lines':len(lines),'verified_equal_to_pinned_git_blob':True,
                '_lines':lines,'_decls':declarations}

def refs(key,names,role='exact_source_statement_or_parallel_proof'):
    f=files[key]
    out=[]
    for name in names.split():
        hits=[d for d in f['_decls'] if d[0]==name]
        assert len(hits)==1,(key,name,hits)
        _,start,qualified=hits[0]
        end=start+1
        while end<f['lines'] and not BOUND.match(f['_lines'][end].decode()):
            end+=1
        while end>start+1 and not f['_lines'][end-1].strip():
            end-=1
        selected=b''.join(f['_lines'][start:end])
        out.append({'path':f['path'],'declaration':qualified,'source_spelling':name,
                    'line_start':start+1,'line_end':end,'full_file_sha256':f['sha256'],
                    'range_sha256':hashlib.sha256(selected).hexdigest(),'range_bytes':len(selected),
                    'first_line':f['_lines'][start].decode().rstrip('\r\n'),
                    'role':role,'url':f'{URL}/blob/{PIN}/{f["path"]}#L{start+1}-L{end}'})
    return out

claims = [
 {'id':'RL1','title':'Actual physical monomial map and four-c Euler margin',
  'status':'proved_human_actual_symbol_and_margin_argument',
  'statement':'The source ioBlock monomial substitution is injective and preserves balanced gradings; nonterminal integral binomial Euler operators of total degree<=4c map SSZ(mu) into SSZ(mu-4c), with exact floor conventions.',
  'depends_on':['WT2','WT6','WT7','SW1'],
  'sources':refs('objseg','BlockData.gens BlockData.SSZ blockData')+
   refs('bf','baseExp ioExp gOp gEv Balanced HomExp GThetaAt')+
   refs('monomial','symVar_inj ioFockAt')+refs('balanced','OmB deg_split ssz_wh')+
   refs('fiber','homAt lam_balanced sum_fiber')+refs('eig','eigAt')+
   refs('gtheta','op_SSt thr_shift gThetaAt')+refs('otherE','cth_gen cth_SSt')+
   refs('chain','cth_rename Ehat_eq pairP nv_Ehat tail_chain')},
 {'id':'RL2','title':'Explicit factorial correction and block scalar valuation',
  'status':'proved_human_factorial_identity_and_sharp_source_bound',
  'statement':'Define Phi_b with all fixed factorials, the diagonal inverse factorial-unit polynomial, and kappa_b=z_j p^v_b Phi_b/specConst. Prove 0<=v_p(kappa_b)<=(k+1)L_j using the distinguished two-coordinate exponent and multinomial Legendre bounds.',
  'depends_on':['RL1','DT1','DT2','DT3','DT4','DT5','SW12'],
  'sources':refs('bf','cdeg Nblk IsOddVar DvdAt FactAt')+
   refs('fiber','dvdAt')+refs('factorial','fact_abs')+
   refs('expfact','Rblk expFact_ioExp baseExp_odd baseExp_end')+
   refs('leading','lev_balanced lev_const mu0F mu0 leading_exponent_homogeneous PhiB kap_transport kapAt_of')+
   refs('coarse','symbol_variable_first_columns card_supp_le cdeg_le_tdeg coarseMultAt_of')+
   refs('mult','val_digit kapNumAt_of')+refs('true','trueDegAt_of')+
   refs('charzero','oddVar_data endVar_data factAt_of')},
 {'id':'RL3','title':'Actual block maps and robust normalized product pairing',
  'status':'proved_human_block_maps_and_global_pairing_under_literal_local_bounds',
  'statement':'The maps w^v_b G_b and w^v_b produce integral SSZ outputs at margin m0(13) for Cm>=17. Distinct blocks have disjoint physical supports; products over disjoint segments give FormAt with v_p(kappa_beta)<=4kap0. The normalized form is integral on the full coefficient lattice, so arbitrary w^c perturbations preserve the congruence.',
  'depends_on':['RL1','RL2','SW1'],
  'sources':refs('objseg','bbSpec blockLat segForm kap0G4')+
   refs('blockmaps','bb_pair Nblk_ne ssz_antitone_of_le blockFormAt_of')+
   refs('orth','sep ioBlock_eq_sum orthAt')+
   refs('prod','fock_prod_disj segVars_disj ioBlock_supported prodAt')+
   refs('globalnorm','lgSeg_sum kapZ_sum zProdAt numAt')+
   refs('integral','fact_multinomial_le tensor_factorial_integral intAt')+
   refs('form','prod_add_mul segForm_single formAt_of restForm_of\'')+
   refs('block_form','kapZ zTen lgSeg facSeg zSeg BlockFormAt FormAt')},
 {'id':'RL4','title':'Literal column numerics and joined Frobenius column witnesses',
  'status':'proved_human_actual_ColumnNumericsAt_and_ColsAt_using_IP_and_SW10',
  'statement':'From literal Std derive the two floor inequalities of ColumnNumericsAt by epsilon A0 margins and the early coarse-degree alternative. Specify the rank-one plane path, its matching to the actual normal path, and the exact KK_c column witnesses and degree/order sums.',
  'depends_on':['SW10','IP3','IP4','IP7','IP8','IP9','IP10'],
  'sources':refs('std','Std')+refs('colnum','ColumnNumericsAt')+
   refs('colnumproof','column_first_coefficient_bound column_margin_bound column_lower_ratio column_first_goal column_second_goal three_level_le_eps_prime m1num_of_std')+
   refs('gap','coarse_degree_alternative','shared_SW10_exact_input')+
   refs('cols','zxS a0Z nuS PS colsS plS dKS oCS dgCS fCS')+
   refs('colmatch','ph_seg')+
   refs('colcount','change_count plSum_seg oSum_seg dKsum_seg Kprod_seg')+
   refs('coltop','colsAt_of')+refs('coldef','ColSys ColsAt')+
   refs('span','lattice_le_span_psi_image xiSpan genSet_le')},
 {'id':'RL5','title':'Explicit localizer, raw factor recipe and terminal room',
  'status':'proved_human_actual_PreSys_and_RoomAt_under_Std_CE1_CE2_ge_17',
  'statement':'Construct rank-one Frobenius minors, contractions and cyclic localizer. Specify all digit/level factor multiplicities and residual monomial. Prove usedX<=a-E0+(N1+c)kQ and the E0 margin, ensuring all exponents are nonnegative and giving the exact own symbol and off-plane order.',
  'depends_on':['RL4'],
  'sources':refs('rawasm','kSkey kWkey locC locR IsFac')+
   refs('key','kS_ord kW_ord key3At')+refs('keyone','key3One_S key_lift_identity_lower loc4One')+
   refs('localres','loc4Res_of loc4Res_of_line')+refs('localdiv','loc4Div_of')+
   refs('locallift','locR_lift loc4Ord_of')+
   refs('multiplicities','IM multMk fMk aMk oMk dgMk bMk')+
   refs('hook','hTop hTop_lift hpow_congr softHseg sgKS_pow')+
   refs('rig','rig0 rig std_eq wh_total')+
   refs('standard','rPl stdPoly_eq')+
   refs('head','l2sR word_head_formula sym_family_word_eq_head_mul_monomial')+
   refs('totdeg','order_sum_eq_order_family multidegree_sum_eq_target_degrees total_product_mem_polynomials cleaned_product_order_family_eq')+
   refs('pre','lemmaRData preAt_of')+refs('roomdef','usedX RoomAt')+
   refs('room','error_exponent_lower_bound room_of_std')},
 {'id':'RL6','title':'Actual quotient-remainder reblocking and integral tail-core membership',
  'status':'proved_human_actual_TCore_from_literal_numerical_bounds',
  'statement':'Reconstruct the new block from physical monomial quotients and remainders; prove the exact uTot expansion by Z^zS^y=Z^(z-y)(E-q)^y, the new degree/order bounds, column-deletion prefix cost N1e and subsequent prefix cost<=(N1+1)(k+Qe).',
  'depends_on':['RL4','RL5','RL7'],
  'sources':refs('factor','ycond_factor')+
   refs('reblock','mEps ezA eyA axA z0A y0A segmentBlockOfMonomial segMon_eq')+
   refs('quotients','nb_sum_mod_div nb_coarseA nb_coarseC nb_digits nb_oEff nb_ord nb_ez_le block_y_zero_le_of_bound block_y_zero_le_z_zero nb_coarseA_ge')+
   refs('binomial','pairU EhS EpS uTot uTot_mem')+
   refs('rowinc','ycond_mEps ycond_pairs pWt_sum_le rowInc_le thr_eq')+
   refs('rowproof','ycond_mul ycond_pair ycond_monomial')+
   refs('segcore','segCoreAt_of_num')+refs('glue','tcoreAt_of_seg')+
   refs('core','PreSys.core PreSys.toFacSys')+refs('coredef','TCoreAt')},
 {'id':'RL7','title':'All NumCoreAt inequalities derived directly from Std',
  'status':'proved_human_actual_numerical_core_without_black_box_restNumCore',
  'statement':'Prove delta A_i/4>=c(13kN1Q+2Q+3k)+4, transport BLk under the exact block growth bounds, and prove the cap/floor margin with total loss<=13e kN1Q. Natural subtraction is checked using e<n<=c.',
  'depends_on':[],
  'sources':refs('std','Std')+refs('rawdef','ka1 localOrderCap BLk')+
   refs('objseg','cap oEff coarseA DigitsOK')+refs('numdef','NumCoreAt RestNumCore')+
   refs('num','tcx_roomR tcx_room tcx_floor tcx_capdiff tcx_termU tcx_termS numCore_of_std')},
 {'id':'RL8','title':'Finite factor expansion proves the actual raw-tail congruence',
  'status':'proved_human_actual_RawTailBody_from_constructed_factors',
  'statement':'A tail coefficient has w-order at least max(1,normaldegree-order). For a product of removed tails this gives max(number removed,excess normaldegree), exactly matching the reblocking membership. Grouping the finite expansion proves RawTailBody, preserving true multidegree and off-edge order.',
  'depends_on':['RL4','RL5','RL6','RL7'],
  'sources':refs('factor_sys','TCls TCls.mul TCls.pow TCls.prod FacSys tail_cls FacSys.liftable')+
   refs('assembly','psi_facts facSysAt_of rest_assumptions_of_three_interfaces')+
   refs('span','asmRTAt_of_facSys')+refs('rawasm','AsmRTAt restRawTail1_of')+
   refs('rawdef','SSg IsCleanAwayFromPlane RawTailBody RawTailAt1 RestRawTail1')},
 {'id':'RL9','title':'Finite triangular cleanup preserves the original height',
  'status':'proved_human_actual_cleaning_induction',
  'statement':'Strong induction on precision subtracts w^h times a correction of height o+h, preserving height o and every other-plane w^c condition. At n=c and mm=12c this cleans the actual retained symbols and uses only the explicit SW12 order comparison for the final floor(t0) height.',
  'depends_on':['RL8','SW12'],
  'sources':refs('cleanup','clean_smul_pow symFam_span ssg_int t44 lemma44_at_body lemma44_at_of_raw_tail lemma44_identity_of_raw_tail')+
   refs('rawdef','CoarseMultiplicityAtIdentity KeptBLAt')+
   refs('ord','ord_all','shared_SW12_exact_height_input')+
   refs('objseg','m0G4 t0G4')},
 {'id':'RL10','title':'Exact actual source-dual chart pairing and CCe transport',
  'status':'proved_human_normalization_and_lattice_transport_using_prior_actual_models',
  'statement':'The reversed dual midpoint basis is inverse-transpose to the source midpoint; the product of the two chart factors w^AHH is exactly the multiplicative p^AHH in beHH(F,G)=p^AHH G(F). The normalized Fock map Xi carries the dual cleaned lattice into CCe-prime, and the flat pairing is exactly zTen times the identity-chart Fock pairing.',
  'depends_on':['RL3','RL9','EL1','EL2','EL5','EL6','EL8','IW5','IW6','EA3'],
  'sources':refs('bridge','IsWittIdent WittIdent EdgePlane')+
   refs('objseg','AHH ReHH ReHH\' beHH CCe CCe\'')+
   refs('flat','flatTheta mul_matQ_one Aa_dual\' lift_one')+
   refs('flatpair','Xi_CC kapR_zTen pairing testFlatAt')+
   refs('ximap','XiH')+refs('paired','TestFlatAt1 testFlatAt1 SrcHalfAt1 srcHalf1_of')},
 {'id':'RL11','title':'Literal PairLiftAt at Cm>=17, Ct>=30 with explicit scope',
  'status':'proved_human_actual_paired_lift_endpoint_under_recorded_Std_and_SW12_inputs',
  'statement':'Construct all source and dual lifts with height floor(t0), kappa valuations<=4kap0, and the exact block-diagonal product of segment forms modulo w^c. Nonretained or invalid branches are handled by zero lifts. This is the paired-lift component, not a digit-class rank bound, tI comparison, or global Type-I/RH theorem.',
  'depends_on':['RL1','RL2','RL3','RL4','RL5','RL6','RL7','RL8','RL9','RL10','SW1','SW10','SW12'],
  'sources':refs('pair','FamOK PairLiftAt RestPairLift')+
   refs('paired','paired_lift_at_of_identity paired_lifts_of_identity')+
   refs('block_form','FormAt RestForm')+refs('setting','UnramifiedQuadraticSetting')+
   refs('height','tI t0I','separate_downstream_height_not_claimed_here')},
]

for c in claims:
    c['assumptions']=[
      'Literal unramified quadratic coefficient/Frobenius setting, p>=5, w^2=p, and the fixed source data.',
      'Literal Std with H=1; CE1,CE2>=17 for residual room; Cm>=17 and Ct>=30 for the final paired endpoint.',
      'Named earlier IP/DT/WT/EL/IW and concurrent SW inputs only at the explicit interfaces in the report.',
    ]
    c['proof_location']={'file':'paired_lifts/paired_lifts_section.tex',
                         'expanded':'paired_lifts/report.txt','section':c['id']}
    c['remaining_inputs']=[]
    c['separate_remaining_work']=[
      'Uniform instantiation of Std and the kept/order premises uses the parent SW numerical component.',
      'The rankOnDigits/mCl digit-class estimate and subsequent t0<=tI comparison are not inferred from paired lifts.',
      'Full global arithmetic and simultaneous window/prime selection remain separate.',
    ]

records = [s for c in claims for s in c['sources']]
unique = {(s['path'],s['line_start'],s['line_end'],s['range_sha256']) for s in records}
for s in records:
    raw=(REPO/s['path']).read_bytes().splitlines(keepends=True)
    part=b''.join(raw[s['line_start']-1:s['line_end']])
    assert hashlib.sha256(part).hexdigest()==s['range_sha256']
    assert raw[s['line_start']-1].decode().rstrip('\r\n')==s['first_line']
    assert len(part)==s['range_bytes']
ledger={
 'component':'paired_lifts','artifact_version':'0.9','repository':URL,'commit':PIN,
 'range_convention':'Inclusive one-based raw-line bytes, including original line endings.',
 'claims':claims,
 'source_files':[{k:v for k,v in f.items() if not k.startswith('_')} for f in files.values()],
 'shared_companions':{
   'SW1':'Actual SSZ saturation; no integral semisimplicity.',
   'SW10':'Exact coarse-degree alternative from literal Std and odd-band exclusion.',
   'SW12':'Kept=>BLk(0), actual terminal oPlus legality and ord_all<=floor(t0).',
   'IP':'Matched normal/one-plane columns and actual Frobenius all-chart/own-chart witnesses.',
   'DT':'Integral Newton-polynomial factorial-unit approximation.',
   'EL_IW':'Actual tensor-polynomial and normalized dual-model identification.',
 },
 'artifact_sha256':{name:hashlib.sha256((HERE/name).read_bytes()).hexdigest()
                   for name in ['report.txt','paired_lifts_section.tex','build_provenance.py']},
 'validation':{'lean_sources_modified':False,'full_lean_build_or_kernel_replay':False,
               'all_files_equal_pinned_git_blobs':True,'all_declarations_anchored':True,
               'all_range_hashes_rechecked':True,
               'source_records':len(records),'unique_ranges':len(unique)},
}
(HERE/'provenance.json').write_text(json.dumps(ledger,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'claims':len(claims),'source_records':len(records),
                  'unique_ranges':len(unique),'files':len(files),
                  'all_files_equal_pinned_git_blobs':True}))

