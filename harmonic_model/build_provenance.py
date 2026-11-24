"""Regenerate HM pinned-source correspondence; does not invoke or modify Lean."""
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
CS = GB + 'ColumnSpanDensity/'
HT = GB + 'HermitianTensor/'
PD = 'src/Formalism/PolynomialDimension/'
FM = 'src/Formalism/LocalToGlobal/GroupLattices/FockModels/'
PATHS = {
    'setting': GB+'UnramifiedQuadraticSetting.lean',
    'obj': GB+'ObjSeg.lean',
    'bridge': GB+'ObjBridge.lean',
    'delta': CS+'DeltaPsiH.lean',
    'single': CS+'SingleWeightLatticeComparison.lean',
    'model': CS+'ModelIdentificationOfExplicitMap.lean',
    'explicit': HT+'ExplicitMapOntoTwoLetterSpace.lean',
    'gauss_inverse': HT+'TwoLetterLatticeGaussInverse.lean',
    'nu': HT+'NuOfWtPQCast.lean',
    'letter': CS+'FinrankLetter.lean',
    'rank_tensor': CS+'FinrankTensor.lean',
    'mean': CS+'MeanDefs.lean',
    'factor': CS+'FactorizationBoundMonoLattices.lean',
    'har': PD+'StatementHar.lean',
    'har_final': PD+'FinalHar.lean',
    'har_zero': CS+'HarProjEqZeroIff.lean',
    'single_model': CS+'SingleWeightOfModelIdentification.lean',
    'functor': CS+'FunctorComparisonOfSingleWeight.lean',
    'functor_facts': CS+'FunctorComparisonOfSingleWeightFacts.lean',
    'lattice_maps': CS+'LatticeMapsOfFunctorComparison.lean',
    'rho_split': CS+'RhoSumBoundOfMapsSplitting.lean',
    'block': CS+'BlockSplit.lean',
    'edge_lat': CS+'EdgeLatRS.lean',
    'gl': CS+'InvariantSectionsTransportGL.lean',
    'edge': CS+'EdgeIndep.lean',
    'upper': CS+'RhoUpperBoundSmallDepth.lean',
    'upper_count': CS+'RhoUpperBoundOfEdgeCount.lean',
    'lower_count': CS+'RhoLowerBoundOfEdgeCount.lean',
    'rho': CS+'RhoLowerBoundLargeConductor.lean',
    'nled': CS+'NLeDAll.lean',
    'fixed': CS+'ThresholdFixedWeightFacts.lean',
    'tm': CS+'TwoHundredLeRadius.lean',
    'density': CS+'DensityNumericalFacts.lean',
    'ed_basis': FM+'ElementaryDivisorBasis.lean',
    'dual_inc': FM+'DualInclusionLattices.lean',
    'tensor': CS+'Tensor.lean',
    'tensor_defs': CS+'FactorsLEOfIndex.lean',
    'det_defs': HT+'DetFactsPAlt.lean',
    'tau': HT+'TauP.lean',
    'pb': HT+'PbSmithLam.lean',
    'det_nonzero': HT+'DetYNeZero.lean',
    'det': HT+'DetFactsP.lean',
    'coeff': HT+'CoeffSumMonomialLinear.lean',
    'contraction': HT+'ContractionOfPairingLemmas.lean',
    'cloud_a_def': HT+'CloudADef.lean',
    'cloud_defs': HT+'CloudDefs.lean',
    'cloud_a': HT+'CloudA.lean',
    'cloud_b': HT+'CloudB.lean',
    'cloud_c': HT+'CloudC.lean',
    'cloud_iso': HT+'CloudIso.lean',
    'cloud_iso_def': HT+'CloudIsoDef.lean',
    'cc_dual': HT+'CcDualWtAnti.lean',
    'cloud_maps': CS+'CloudPropOfMapsRetractionBasis.lean',
    'ring_defs': CS+'RestHLTransport.lean',
    'ring_poly': CS+'HLepolyTr.lean',
    'ring': CS+'LpRingIndepOf.lean',
    'oring': CS+'RestOIso.lean',
    'quad_defs': CS+'QuadraticBasis/StatementO.lean',
    'quad_roots': CS+'QuadraticBasis/QuadRoots.lean',
    'quad_basis': CS+'QuadraticBasis/QuadBasis.lean',
    'quad_iso': CS+'QuadraticBasis/PresIso.lean',
    'quad_final': CS+'QuadraticBasis/FinalO.lean',
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
            kind,label = stack.pop()
            assert not m[1] or m[1] == label, (path,i+1,label,m[1])
        elif m := DECL.match(line):
            ns = '.'.join(label for kind,label in stack if kind == 'namespace')
            declarations.append((m[1],i,ns+'.'+m[1] if ns else m[1]))
    assert all(kind == 'section' and label is None for kind,label in stack), (path,'unclosed namespace')
    files[key] = {'path':path,'sha256':hashlib.sha256(raw).hexdigest(),'bytes':len(raw),
                  'lines':len(lines),'verified_equal_to_pinned_git_blob':True,
                  '_lines':lines,'_decls':declarations}

def refs(key, names, role='exact_source_interface_or_parallel_proof'):
    f = files[key]
    out = []
    for name in names.split():
        hits = [d for d in f['_decls'] if d[0] == name or d[2] == name]
        assert len(hits) == 1, (key,name,hits)
        spelling,start,qualified = hits[0]
        end = start+1
        while end < f['lines'] and not BOUND.match(f['_lines'][end].decode()):
            end += 1
        while end > start+1 and not f['_lines'][end-1].strip():
            end -= 1
        selected = b''.join(f['_lines'][start:end])
        out.append({'path':f['path'],'declaration':qualified,'source_spelling':spelling,
                    'line_start':start+1,'line_end':end,'full_file_sha256':f['sha256'],
                    'range_sha256':hashlib.sha256(selected).hexdigest(),'range_bytes':len(selected),
                    'first_line':f['_lines'][start].decode().rstrip('\r\n'),
                    'role':role,'url':f'{URL}/blob/{PIN}/{f["path"]}#L{start+1}-L{end}'})
    return out

claims = [
 {'id':'HM1','title':'Actual two-letter model, integral transport, harmonic kernel and dimensions',
  'status':'proved_human_actual_polynomial_and_lattice_identification',
  'statement':'The cofactor/first-column map identifies the actual two-letter tensor and integral lattice. The diagonal quotient has kernel hP_(a-1,b-1) and dimension S_a S_b-S_(a-1)S_(b-1). Determinant-twisted basis change proves the actual model on every lattice; disjoint-block dimensions telescope exactly.',
  'depends_on':['CB2','CB3','CB6','CB7','EL2'],
  'sources':refs('delta','covY PsiXY deltaB sum_covY delta_Psi_h')+
   refs('single','wtPQ twoLat twoSp SingleWeightLatticeComparison')+
   refs('model','TiePsi model_identification_of_explicit_map')+
   refs('explicit','Psi_xs Psi_ys explicit_map_injective explicit_map_onto_two_letter_space')+
   refs('gauss_inverse','ta_vec_mem ta_cov_mem ta_vec_of ta_cov_of two_letter_lattice_gauss_inverse')+
   refs('nu','dPsi tie5b tie3 nuOf_wtPQ_cast weylDim_shift finrank_wtPQ tie4 tiePsi_of')+
   refs('letter','prod_tops flatW_dom lamAt_flat finrank_weyl finrank_letter restDims_of')+
   refs('rank_tensor','weylDim_hwt_eq weylDim_vec weylDim_cov finrank_tensor RS.charZeroO RS.charZero')+
   refs('mean','RestDims')+refs('setting','H0 Hten nuOf Vsp dimV HL')},
 {'id':'HM2','title':'Explicit harmonic projectors and bounded integral quotient maps',
  'status':'proved_human_commutator_and_divided_power_lattice_argument',
  'statement':'Construct pi and every level projector by the sl2 commutator, prove the harmonic direct sum and actual quotient maps, and bound their Gauss-lattice denominator by ceil((m+2)(log_p(8a+m)+1)) using Legendre binomial valuations. Equivariance gives the same bound for every ordinary lattice.',
  'depends_on':['HM1'],
  'sources':refs('har','hXY ctrF hDiv ctrDiv PolAB HarAB harProj levelProj glAct GaussLat FockLat latOf SlTwo SlTwoPower HarDecomp HarProj LevelProj BinomVal FockProj GaussProj GaussLemmaH LevelLattice HarQuot')+
   refs('har_final','slTwo harProj levelProj gaussProj gaussLemmaH levelLattice harQuot')+
   refs('har_zero','harProj_eq_zero_iff oneTop_abs')+
   refs('single_model','RS.Ov RS.pLocal TwoLetterModelIdentification expo_le single_weight_of_model_identification')},
 {'id':'HM3','title':'Actual tensor comparison, cleaned lattices and exact p^(3u) pairing',
  'status':'proved_human_all_edge_lattice_and_normalization_computation',
  'statement':'Tensor the harmonic maps over TT, rescale by w^(AHH-Ar), and prove all source, midpoint, target and competing-edge conditions at unchanged t,c. The actual paired images have normalized pairing p^(3u) times the corresponding HH component, before the source weakens the depth cost to 4u.',
  'depends_on':['HM2','EL5','EL6'],
  'sources':refs('functor','lamAt_flat_top lamAt_flat_off functor_comparison_of_single_weight')+
   refs('functor_facts',"exists_linearMap_prod_rename_eq existsIO' existsPR' regroupP functor_comparison_of_single_weight_facts")+
   refs('lattice_maps','LatticeFunctorComparison Ar_le_AHH scale_add_le lattice_maps_of_functor_comparison')+
   refs('rho_split','RhoSumLatticeMaps vO_eq vLEO_pow_mul rho_sum_bound_of_maps_splitting')+
   refs('obj',"AHH ReHH ReHH' beHH CCe CCe'")+
   refs('edge_lat','edgeLat_RS')},
 {'id':'HM4','title':'Small Smith factors split across the actual harmonic components',
  'status':'proved_human_primitive_kernel_and_Smith_argument',
  'statement':'If integral matrices sum to zI_n, the total number of their Smith factors of valuation<=v(z) is at least n. Integral row/column scalings yield actual component certificates whose ranks sum to the HH rank, at depth D+3u<=D+4u.',
  'depends_on':['HM3'],
  'sources':refs('rho_split','BlockSplit RhoSumLatticeMaps rho_sum_bound_of_maps_splitting')+
   refs('block','BlockSplit blockSplit blockSplitting_holds')+
   refs('obj','FactorsLE RhoGE vLEO')+refs('rho','RhoSumLowerBoundEdge')},
 {'id':'HM5','title':'Exact edge transport and the one-sided small-depth rank bound',
  'status':'proved_human_GL_transport_and_residue_pairing_matrix',
  'statement':'Actual determinant-twisted transport preserves CCL, CCL-prime, Re-prime and certificates. A single-edge certificate with primal CCL and dual only Re-prime, 2D<c, has rank<=dimV/gaussian(q,k); the proof counts residue lines and makes the joint normalized pairing matrix the identity modulo w.',
  'depends_on':['CB7','EL8','HM8'],
  'sources':refs('gl','fuT fu_nablaLTw invariant_sections_transport_GL fuG fu_twist fu_extO fu_LeAt fuTT fu_Hten restFunct')+
   refs('edge','mapE RestFunct restEdge_of')+
   refs('upper','det_updateCol_one famS restEdgeCountSrc restEdgeCount rho_upper_bound_small_depth')+
   refs('upper_count','RestEdgeCountSrc dvd_w_pow_of_vLEO be_scale_Re rho_upper_bound_of_edge_count')+
   refs('rho',"CCL CCL' FacL RhoL dL RestEdge RhoUpperBoundSmallDepth")+
   refs('nled','nLeD_all nEdge nLeD')},
 {'id':'HM6','title':'Literal KeyIneq from the actual HH certificate and fixed-weight numerics',
  'status':'proved_human_structural_implication_with_explicit_concurrent_inputs',
  'statement':'Under the displayed HH RhoGE certificate and literal FixedWeightNumericalFacts, split the rank, apply the one-sided edge bound, compare the shifted height, and use the exact dimension telescope to prove source KeyIneq for the literal kF and kx.',
  'depends_on':['HM1','HM4','HM5','RU11','NP6'],
  'sources':refs('factor','FixedWeightNumericalFacts factorization_bound_mono_lattices factorization_bound_mono_level infimum_kappa_le_of_rho_bound sum_dimensions_flattened_weights exponent_le_shifted_add initial_level_shift_bound keyIneq_of')+
   refs('rho','a c4 u0c D0 D1 J0 Jn t0 tStar kF kx')+
   refs('mean','ua lb ub WaP WbP KeyIneq')+
   refs('fixed','fixed_weight_facts_of_hyp','concurrent_NP_numerical_supplier')+
   refs('tm','Cst.TM','concurrent_NP_exact_uniform_threshold')},
 {'id':'HM7','title':'Finite harmonic telescoping and the exact translated-box average',
  'status':'proved_human_stronger_finite_density_and_conditional_Avg',
  'statement':'Prove sum_(j<=J) H_ab/(S_(a+j)S_(b+j))>=1-S_aS_b/(S_(a+J+1)S_(b+J+1)), and its exponential tail. Translation of the actual KeyIneq gives Avg whenever the stated density/cardinality comparison holds. RD12 supplies that comparison uniformly.',
  'depends_on':['HM1','HM6'],
  'sources':refs('density','P1 DensityNumericalFacts sum_map_le card_Wa card_Wb sum_kF_mul_prod_le_kx avg_abs avg_of')+
   refs('mean','meanN Avg'),
  'new_human_argument':'The finite R_j telescope and its stronger exponential bound are independently derived, not attributed to a named source declaration.'},
 {'id':'HM8','title':'Actual dual-height bases, perfect normalized pairing and disjoint tensor factorization',
  'status':'proved_human_tableau_edge_exponents_and_actual_product_bases',
  'statement':'Transport the integral row-homogeneous tableau basis to the source edge. With pi its target exponent and o=Ar-pi>=0, the two normalized edge bases pair by p^Ar w^(-2o)p^(-pi)=1. Disjoint letter blocks give literal RestTensor, including ordinary and midpoint lattice equalities, the dual evaluation formula, and dimension multiplication.',
  'depends_on':['CB2','CB7','EL5','EL6'],
  'sources':refs('bridge','DualHeightBasis DualHeightInclusion BePerfect HLSpans')+
   refs('ed_basis','elementary_divisor_basis dualHeightBasis')+
   refs('dual_inc','dualInclusionLattices hlSpans bePerfect')+
   refs('setting',"Hten HL LeAt HLe Ar Re Re' be order")+
   refs('tensor_defs','othW Pr RestTensor')+
   refs('tensor','invariant_sections_zero_weight_iff tn_Hten tn_Vsp tnMu tnDelta RestLeLat tn_dimV restTensor_of')},
 {'id':'HM9','title':'Integral complementary-middle pairing with bounded p-power diagonals',
  'status':'proved_human_Jacobi_complement_Fock_duality_and_Smith_rounding',
  'statement':'The explicit tau(f)=det(Y)^T f(Y^(-transpose)J) is an integral complementary-module isomorphism. Normalize the IW Fock form by p^kappa, perform Smith reduction and round half-integral valuations upward, obtaining every QPh clause with integer p-power diagonal exponents bounded by ceil(kappaOneExponent).',
  'depends_on':['CB2','CB3','IW3','IW5'],
  'sources':refs('det_defs','genY cofY TauP SmithP BilinP DetFactsP NumP')+
   refs('tau','adjugate_subst_mem_dualWeyl_of_mem transpose_act_comp_adjugate_subst_comp_act_eq_det antidiagonal_mul_self_eq_one detY_mul_adjugate_subst_adjugate_eq_X tauP')+
   refs('pb','pb_nabla_one pb_finrank pb_smith_lam smithP')+
   refs('det_nonzero','detY_ne_zero qPh_of')+
   refs('det','bilinP detFactsP numP')+refs('coeff','PhInv QPh')},
 {'id':'HM10','title':'Literal middle-column contraction, integral tableau lifts and CloudOne',
  'status':'proved_human_explicit_coefficient_map_and_highest_line_scalar',
  'statement':'Construct the source Lambda coefficientwise from v(Zdiag(1,Y,1)) and the complementary pairing. Adjoin row/column zero to middle minors to lift the actual diagonal families, prove their row degrees, and evaluate the unique highest line at I to obtain the exact scalar. Twisted changes of basis give every CloudOne lattice and primitivity clause for all nonzero xi.',
  'depends_on':['HM1','HM9','CB2','CB6','CB7'],
  'sources':refs('coeff','midI midOf subY sub2 lcoef lamOf resY RowA shapeC SubCoeffP SubMapP SubRowP LamCoeffP LamEquivP LamMulP LamEvalP LamMemP SubMuP TopLineP LiftP DetDivP IntCapP HwMulP')+
   refs('contraction','contraction_of_pairing_lemmas')+
   refs('cloud_a_def','intO Row0 ContractionStandardLattice')+
   refs('cloud_defs','dualWt dualW famD CloudOne')+refs('cloud_a','cloudOne_of')},
 {'id':'HM11','title':'Actual tensor cloud maps, primitive exact preimage and conductor loss 2Nc',
  'status':'proved_human_actual_RestCloudMaps_with_all_normalizations',
  'statement':'Tensor the explicit Lambda maps and primitive highest vectors. Prove exact preimage on every actual lattice by Gauss valuation; check midpoint exponents and source cleaning. The dual map is p^(Nc)(g composed with L_a), and its competing-target condition loses exactly 2Nc powers of w. This proves literal RestCloudMaps, with c2>=2Nc.',
  'depends_on':['HM8','HM10','CB2','CB7'],
  'sources':refs('cloud_defs','RestCloudLat')+refs('cloud_b','restCloudLat_of')+
   refs('cloud_c','cc_elem restCloudMaps_of')+
   refs('cloud_iso_def','CloudIsoP')+refs('cloud_iso','iso_one retract_one iso_ten cloudIso')+
   refs('cc_dual',"cc_Ar_add cc_Ar_of cc_Re cc_CCL cc_tgt_le cc_CCL'")+
   refs('cloud_maps','RestCloudMaps')},
 {'id':'HM12','title':'Compatible actual RS coefficient rings and LPprime transport',
  'status':'proved_human_Hensel_bases_Frobenius_compatibility_and_semilinear_transport',
  'statement':'Construct matching Z_p bases of the unramified rings and W bases 1,eta,w,eta w of the ramified rings by Hensel lifting and completeness. The resulting isomorphisms preserve w, embeddings and Frobenius. Coefficient transport preserves the actual invariant lattices, duals, normalized pairings and integral GoodRankK equations, proving literal LPRingIndep.',
  'depends_on':['CB2'],
  'sources':refs('setting','HidaSetting UnramifiedQuadraticSetting H0 Hten LeAt HLe GoodRankK LPprimeAt LPprime')+
   refs('rho','RS LPRingIndep')+
   refs('ring_defs','RSIso RestRSIso RestHLTransport dT')+
   refs('ring_poly',"PsiV HLpoly_tr HLepoly_tr restHLTransport lpRingIndep_of'")+
   refs('ring',"RestOIso restRSIso_of lpRingIndep_of''")+refs('oring','restOIso')+
   refs('quad_defs','IsQuadBasis PresIso QuadBasis QuadRoots')+
   refs('quad_roots','qr_hensel existsCompatibleRoots_holds')+
   refs('quad_basis','qb_indep qb_span basisCriterion_holds')+
   refs('quad_iso','presentationIso_holds')+refs('quad_final','oIso')},
]

for claim in claims:
    claim['proof_location'] = {'file':'harmonic_model/main.tex',
                               'expanded':'harmonic_model/report.txt',
                               'section':claim['id']}
    claim['assumptions'] = [
        'The literal source coefficient and dominant-weight hypotheses at the cited interface; characteristic zero and w^2=p where used.',
        'All dimensions, maps and lattices are the actual polynomial models, with source determinant and normalized pairing conventions.',
        'HM6 explicitly requires the displayed HH rank certificate and FixedWeightNumericalFacts; HM7 explicitly requires the displayed density/cardinality bound.',
    ]
    claim['remaining_inputs'] = []
    if claim['id'] == 'HM6':
        claim['explicit_external_interfaces'] = [
            {'interface':'Actual HH RhoGE at D0 and mass (1-kx)dimHH/Ne',
             'supplier':'RU11 with SW segment data and NP/RD numerical instantiation',
             'status':'supplied_by_concurrent_v0_10_components; not inferred from RL alone'},
            {'interface':'FixedWeightNumericalFacts','supplier':'NP6',
             'status':'proved_in_concurrent_v0_10_component'},
        ]
    if claim['id'] == 'HM7':
        claim['explicit_external_interfaces'] = [
            {'interface':'Uniform harmonic density and exact box-cardinality factor',
             'supplier':'RD11-RD12','status':'proved_in_concurrent_v0_10_component'},
        ]
    claim['separate_remaining_work'] = [
        'The final CloudCount/CloudWeightLowerBound/ResidueClassCount rank applications and MidLP/Type-I constant assembly are separate from the explicit maps.',
        'No global arithmetic window construction or analytic RH/Dirichlet-GRH completion is claimed by this component.',
    ]

records = [source for claim in claims for source in claim['sources']]
unique = {(s['path'],s['line_start'],s['line_end'],s['range_sha256']) for s in records}
for s in records:
    raw = (REPO/s['path']).read_bytes().splitlines(keepends=True)
    part = b''.join(raw[s['line_start']-1:s['line_end']])
    assert hashlib.sha256(part).hexdigest() == s['range_sha256']
    assert raw[s['line_start']-1].decode().rstrip('\r\n') == s['first_line']
    assert len(part) == s['range_bytes']
ledger = {
    'component':'harmonic_model','artifact_version':'0.10','repository':URL,'commit':PIN,
    'range_convention':'Inclusive one-based raw-line bytes, including original line endings.',
    'claims':claims,
    'source_files':[{k:v for k,v in f.items() if not k.startswith('_')} for f in files.values()],
    'review_scope':{
        'root':'HM8 and HM12 independently checked against the actual coefficient and lattice interfaces.',
        'lean_audit':'HM9-HM11 independently checked against literal QPh, ContractionStandardLattice, CloudOne and RestCloudMaps; no correction requested.',
        'own_external_reviews':'RU10-RU11 and RD11-RD13 independently checked; no correction requested.',
    },
    'artifact_sha256':{name:hashlib.sha256((HERE/name).read_bytes()).hexdigest()
                       for name in ['report.txt','main.tex','build_provenance.py']},
    'validation':{'lean_sources_modified':False,'full_lean_build_or_kernel_replay':False,
                  'all_files_equal_pinned_git_blobs':True,'all_declarations_anchored':True,
                  'all_range_hashes_rechecked':True,'source_records':len(records),
                  'unique_ranges':len(unique)},
}
(HERE/'provenance.json').write_text(json.dumps(ledger,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'claims':len(claims),'source_records':len(records),
                  'unique_ranges':len(unique),'files':len(files),
                  'all_files_equal_pinned_git_blobs':True}))
