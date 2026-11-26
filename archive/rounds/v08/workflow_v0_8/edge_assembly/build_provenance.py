"""Regenerate EA's exact pinned-source ledger; no Lean invocation or edits."""
from pathlib import Path
import hashlib
import json
import re
import subprocess

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[1] / 'alpoge-rh'
PIN = '7cbf7a0c32fca1badf05931879a37c3f8a2b03b4'
URL = 'https://github.com/CocoSgt/riemann-hypothesis-lean'
GB = 'src/Formalism/SharpRestriction/GrowthBounds/'
SE = GB + 'ScaleEdges/'
PATHS = {
 'setting':GB+'UnramifiedQuadraticSetting.lean',
 'bridge':GB+'ObjBridge.lean',
 'pol':GB+'ObjPol.lean',
 'statement':GB+'TableLineDegreeFive.lean',
 'source':GB+'SourceCleaning.lean',
 'rank_statement':GB+'ValuationLowestDegreeRename.lean',
 'frames':SE+'FramesOf.lean',
 'gain':SE+'GainBoundAt.lean',
 'degree':SE+'MultidegreeBoundLeA.lean',
 'det_degree':SE+'EDelApply.lean',
 'twist':SE+'EvensBeforePairwise.lean',
 'real':SE+'SymbolRealisableBound.lean',
 'realproof':SE+'SymbolRealisableIffGeneralRank.lean',
 'rank':SE+'RankMulConductorDivLeOne.lean',
 'edgeplane':SE+'EdgePlane.lean',
 'flat':SE+'FlatSrc.lean',
 'multiply':SE+'EdgeLatticeMulOfWeightSum.lean',
 'family':SE+'EdgeFamOf.lean',
 'familyproof':SE+'ScaleZpowMono.lean',
 'edge':SE+'InitialLevelMonoWeights.lean',
 'defs':SE+'ManyEdges.lean',
 'num':SE+'NumericProductInequality.lean',
 'many':SE+'ColSpanMap.lean',
 'asm':SE+'ScaleNegMono.lean',
 'smith':SE+'DvdOfAdd.lean',
 'prim':SE+'GoodRankOfPrim.lean',
 'constants':SE+'TheoremIIOfEdgeBoundConstants.lean',
 'main':GB+'ScaleEdges.lean',
 'cloudx':SE+'RestCloudOfX.lean',
 'cloudy':SE+'RestCloudXOfY.lean',
 'split':SE+'SourcePrimitiveIntegrality.lean',
 'witt':GB+'WittIdentPI.lean',
 'witt_statement':'src/Formalism/PeriodIntegrals/WittUnram.lean',
 'witt_main':'src/Formalism/PeriodIntegrals/OrbitalBoundsConclusion/WittUnram.lean',
}
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
 {'id':'EA1','title':'Verify the exact frame and numerical data supplied to RK',
  'status':'proved_human_parameter_bridge_using_FG_and_RK',
  'statement':'Literal Hyps and FG FramesOK give all Conclusion2 premises other than its final size inequality: Ns=min(N1,2N), segment cardinality and p-distance bounds, flat degrees in [a,2a], Ns+r<=K, the logarithmic k bound, and the factor128 depth bound. Basic positivity and monotonicity in C are proved explicitly.',
  'depends_on':['FG7','FG8','RK3'],
  'sources':refs('defs','Hyps')+refs('statement','OrbitHyp WeightHyp La')+refs('frames','FramesOK frames_of')+refs('gain','one_le_orbitWindowCount rank_le_orbitWindowCount Basic hyps_basic hyps_mono flatDeg flatDeg_bounds fr_mono Qj_le alphaMax_le letters_card_le dist_le GainBoundAt symbol_space_at')+refs('rank_statement','Conclusion2')},
 {'id':'EA2','title':'The 3040 size estimate and C>=30 actual source realisation',
  'status':'proved_actual_numerical_compatibility_using_SY_and_IP',
  'statement':'With actual E0=15cPrime(N1+rk)Q^2 and mStar, prove 32pk^2NsQ^2(E0+mStar+1)<=3040k^3r^2NQ^5cPrime. Thus RK applies for C>=3041+|Ck|, in particular4129 for Ck1088. Prove eSP<=E0<=a and eSP=0 off TT, making the existing SY/IP construction the actual SourcesRealisable for C>=30.',
  'depends_on':['EA1','SY6','SY7','IP6','IP11','RK3'],
  'sources':refs('source','alphaMax cPrime mStar')+refs('gain','alphaMax_le E0 symbol_space_at')+refs('degree','num_E multidegree_bound_le_a spdeg')+refs('det_degree','eSP_off eSP_le')+refs('twist','twist_of')+refs('real','G2d dT castV toK SPtrue symB SymbolRealisableAt SymbolRealisableBound SourcesRealisable')+refs('realproof','oHyp_of castVK SymbolRealisableGeneralRank symbol_realisable_iff_general_rank symbol_realisable_general_rank sources_realisable_holds')},
 {'id':'EA3','title':'Finite actual basis, normal-degree floor and exact inverse-transpose edge coordinate',
  'status':'proved_human_transport_with_precise_classical_Witt_background',
  'statement':'The RK direct summand lies in a fixed finite multidegree, hence has a finite actual-generator basis. The normal-degree floor is <=t0(C,max(A,10)). Edges at a fixed source have bases H*g^(-T), and their rational planes are the first r rows of g^(-1). Specify the strict-p-ring uniqueness theorem giving the Frobenius-compatible Witt identification from HidaSetting.',
  'depends_on':['EA1','EA2','RK3'],
  'sources':refs('rank','basis_fin flW_dom restW_dom lambda_zero_eq_product level_lower_bound_terms')+refs('setting','HidaSetting UnramifiedQuadraticSetting IsLattice IsEdge IsEdgeBasis')+refs('bridge','IsWittIdent WittIdent matQ EdgePlane dvrOfStd dvrOfStd_sq')+refs('witt','wittIdent_of wittIdentity_holds','classical_background_source_interface')+refs('witt_statement','IsWittIdent WittUnram','classical_background_source_interface')+refs('witt_main','witt_unramified','classical_background_source_interface')+refs('pol','ratPlane')+refs('edgeplane','Ng Ngi Ng_unit src_eq mem_plane edgePlane')+refs('edge','initial_level_nonneg initial_level_mono_weights edgeStep_of')},
 {'id':'EA4','title':'Transport the integral raw realisations to the actual flat edge lattices',
  'status':'proved_conditional_on_actual_CloudAt_flat_identification',
  'statement':'For each realised summand of level o, divide its integral raw lift by w^o using IsFlatIdent, obtaining source height o, own-edge error w^cPrime, and vanishing at every different outgoing edge. Sum o<=T0; substituted integrality proves the ideal flat family belongs to its own Re. No integrality of rational preimages or power-substitution equivariance is asserted.',
  'depends_on':['EA2','EA3'],
  'sources':refs('flat','vecE flW isFlat_flW LLT_eq scale_shift IsFlatIdent flatSrc')+refs('real','SymbolRealisableAt CloudAt CloudStep')+refs('edge','edgeStep_of')},
 {'id':'EA5','title':'Actual lattice multiplication and primitive-test stability under realisation error',
  'status':'proved_human_edge_family_assembly',
  'statement':'CB/EL give actual Hten, HL and normalized Re multiplication. Multiplying complementary height oS costs exactly oS in off-edge depth cPrime, leaving at least cStar. The own-edge error pairs into w^cPrime O subset p^(D1+1)O; a value a dividing p^D1 is changed only to a(1+p*b*z), preserving the bound for every primitive coefficient array.',
  'depends_on':['EA4','CB6','CB7','EL6','EL7'],
  'sources':refs('statement','LevelPrimesProviso')+refs('setting','lamAt H0 Hten HL HLe Ar Re Re\' be')+refs('bridge','DualHeightInclusion BePerfect')+refs('multiply','lamAt_add Ar_add isDominant_add nuOf_add dualWeyl_mul tensorLat_mul V_mul mulV toV_mul HL_mul Re_mul edge_lattice_mul_of_weight_sum')+refs('family','EdgeFamOf')+refs('familyproof','scale_zpow_mono scale_mono be_add_left be_smulK_left edgeFamOf')+refs('smith','dvd_of_add')+refs('prim','p_nonunit')},
 {'id':'EA6','title':'Controlled EdgeStep with exact rank and height constants',
  'status':'proved_conditional_on_uniform_actual_CloudStep',
  'statement':'Combine RK rank and the cloud complementary count without multiplying by a negative loss factor. Produce n=b*n2>=q^(-rK)(1-Nr^2k/Y)(1-kc0/a)^N dimV, source height<=t0(C,max(A,10))+ell, target height<=that+Nc0, denominator D1<=B*N*k^2*log_p(a)<=Dp. The actual uniform threshold is the maximum in EA.0g.',
  'depends_on':['EA1','EA2','EA3','EA4','EA5','RK3','CL2'],
  'sources':refs('defs','t0 om EdgeStep RestEdge')+refs('real','CloudAt CloudStep SourcesRealisable RestCloud')+refs('rank','norm_index_count_bound rank_mul_conductor_div_le_one mul_mul_add_le_of_abs_le level_lower_bound_terms')+refs('edge','initial_level_nonneg initial_level_mono_weights edgeStep_of restEdge_of')},
 {'id':'EA7','title':'Absorb all level and dimension losses and sum an exact graph chart',
  'status':'proved_human_numerical_and_finite_field_assembly',
  'statement':'The size bound implies Nk*c0*Y<=a. Prove the tBound comparison, D1<=Dp and 1-Cx<=(1-Cr*x)(1-kc0/a)^N for C>=Cr+1, including negative-target cases. Kernels of (u,v)->u+A*v give q^(rK) edges into W^k and cancel the per-edge denominator after summation.',
  'depends_on':['EA6'],
  'sources':refs('num','numeric_product_inequality num_size level_bound_numeric num_count num')+refs('defs','ManyEdges Num')+refs('many','incl incl_inj colSpan_one lattice_of card_quot psi psi_surj psi_ker_inj manyEdges')+refs('constants','prvE_of_gl_operators_form_representation')+refs('statement','tBound aux₃')},
 {'id':'EA8','title':'Global primitive detection, literal GoodRankK and transport to every target',
  'status':'proved_human_primitive_to_GoodRank_and_equivariance_argument',
  'statement':'Increasing the heights identifies the actual Nsrc and Ntgt intersections. An edge containing a unit coefficient detects every primitive combined array; other edges contribute only p^(Dp+1)O. Smith normal form gives p^Dp O^M inside the evaluation image and explicit preimages supply GoodRankK with identity matrix. Tensor covariance and the contragredient action preserve the exact p^Ar-normalized pairing and prove LPOneEvery.',
  'depends_on':['EA5','EA7','EL6','EL8'],
  'sources':refs('setting','extO H0 Hten Vsp HL IsEdge LeAt Ar Re Re\' be Nsrc Ntgt GoodRankK LPprimeAt LPprime LPprimeOne')+refs('defs','ValLe SrcTests EdgeFam S7 Asm')+refs('asm','scale_neg_mono scale_pos_le ValLe.mono asm')+refs('prim','p_nonunit goodRank_of_prim be_sum_left s7')+refs('smith','smith_mem dvd_of_add')+refs('bridge','LPOneEvery')},
 {'id':'EA9','title':'Uniform ConclusionE from the actual cloud input, with threshold4129 bridge',
  'status':'proved_conditional_uniform_implication_not_an_independent_cloud_proof',
  'statement':'For fixed RK1088,1,10 and CloudStep(C,A,B,1088) for every C>=Ccloud, ConclusionE follows for C>=max(4129,Ccloud,A,B). SourcesRealisable uses threshold30. General constants use the exact source maxima EA.0g. RestCloudX/Y and the split-cloud variants feed the same implication only after their actual premises have been proved; no full TypeII or RH/GRH claim is made from a conditional cloud input.',
  'depends_on':['EA1','EA2','EA3','EA4','EA5','EA6','EA7','EA8'],
  'sources':refs('edge','edgeStep_of restEdge_of')+refs('constants','prvE_of_gl_operators_form_representation theorem_II_of_edge_bound_constants')+refs('main','theorem_II_of_edge_bound prvE_degree_five_of_adm_sources_realisable theorem_II_of_cloud_bound theorem_II_of_cloud_bound_X theorem_II_of_cloud_bound_Y theorem_II_of_split_cloud_bounds')+refs('cloudx','CloudStepX RestCloudX restCloud_of_X','explicit_upstream_cloud_interface')+refs('cloudy','CloudStepY RestCloudY restCloudX_of_Y','explicit_upstream_cloud_interface')+refs('split','SourcePrimitiveIntegrality RemainingInputsAfter restCloudY_of','explicit_upstream_cloud_interface')+refs('statement','admitted Stmt ConclusionE ClosedFormOfAdmitted aux₃')},
]
for c in claims:
    c['assumptions']=[
      'Literal local coefficient/Hyps/OrbitHyp/WeightHyp setting; all parameter dependencies and quantifier order retained.',
      'Earlier proved FG, RK, SY/IP, CB and EL results only at the precise interfaces identified in the report.',
    ]
    c['proof_location']={'file':'edge_assembly/edge_assembly_section.tex',
                         'expanded':'edge_assembly/report.txt','section':c['id']}
    c['remaining_inputs']=[]
    if c['id'] in ['EA4','EA6','EA9']:
        c['remaining_inputs']=['The explicit actual CloudAt/CloudStep input, owned by the concurrent cloud-compatibility and outgoing-realisation components.']
    if c['id']=='EA3':
        c['classical_background']=['Uniqueness of the strict p-ring with a given perfect residue field; the report explains Teichmuller expansions and Frobenius compatibility, but does not rederive every defining Witt addition polynomial.']
    c['separate_remaining_work']=['Separate r=1 Type-I construction','Global arithmetic/theta/metric/cohomological windows and simultaneous prime selection']

ledger={
 'component':'edge_assembly','artifact_version':'0.8','repository':URL,'commit':PIN,
 'range_convention':'Inclusive one-based raw-line bytes, including their existing line endings.',
 'claims':claims,
 'source_files':[{k:v for k,v in f.items() if not k.startswith('_')} for f in files.values()],
 'shared_companions':{'FG':'Literal full FramesOK, not bare PathPairCorrespondence.',
   'CP_OR':'Uniform actual CloudStep and its separate outgoing-realisation premise; not inferred from EA.'},
 'artifact_sha256':{name:hashlib.sha256((HERE/name).read_bytes()).hexdigest()
                   for name in ['report.txt','edge_assembly_section.tex','build_provenance.py']},
 'validation':{'lean_sources_modified':False,'full_lean_build_or_kernel_replay':False,
               'all_files_equal_pinned_git_blobs':True,'all_declarations_anchored':True},
}
(HERE/'provenance.json').write_text(json.dumps(ledger,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'claims':len(claims),'sources':sum(len(c['sources']) for c in claims),
                  'files':len(files),'all_files_equal_pinned_git_blobs':True}))
