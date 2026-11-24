#!/usr/bin/env python3
"""Bind the human normalized-frame laws to the exact accepted source pin."""
from pathlib import Path
import argparse
import hashlib
import json
import re
import subprocess

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
PIN = '7cbf7a0c32fca1badf05931879a37c3f8a2b03b4'
VERSION = '0.51'
COMPONENT = HERE.name
SNAP = ROOT / 'source_snapshot_v0_51' / 'geometry'
parser = argparse.ArgumentParser()
parser.add_argument('--repo', type=Path, required=True)
args = parser.parse_args()
repo = args.repo.resolve()
U = 'src/Development/AbelianVarietyTheory/Proofs/UnitaryExistence/'
HI = 'src/Development/AbelianVarietyTheory/Proofs/HomogeneousIdeals/'
FO = 'src/Development/AbelianVarietyTheory/Proofs/FoundationProofs/'
DE = 'src/Development/AbelianVarietyTheory/Definitions/ExistenceOfLattices/'
PJ = 'src/Formalism/LocalToGlobal/ProjectiveLattices/'
EXT = 'src/ReciprocityTheory/ReductiveGroups/ArithmeticGeometry/ExtensionDescent/'
TOR = 'src/ReciprocityTheory/ReductiveGroups/ArithmeticGeometry/BirationalGeometry/ToroidalCompactification/'
FD = 'src/ReciprocityTheory/ReductiveGroups/ArithmeticGeometry/FundamentalDomains/'

# Full files preserve all namespace, variable, typeclass and notation context.
# Exact endpoint declarations are additionally extracted below.
SOURCES = {
 'contracts': (DE+'NormConst.lean','Literal ModelsOf, ModelBase, FrameOK, FramesOK, CoverTri, FibTri, ThetaData and IsNormUn'),
 'frame_ring': (DE+'UnivFrame.lean','Literal SecBC, FrChg, FrameRing, universal frames and open charts'),
 'frame_literal': (PJ+'IsCombAt.lean','Original dual-number framed points, FrMap, FrBor, Rul, sec and evR'),
 'rules': (PJ+'AlgebraMapCAt.lean','TRing, FromTest, natural and weighted rules, evaluation and EvalWD'),
 'weights': (PJ+'EmbKCoe.lean','Original Dom, exponent function ex and coefficient embedding'),
 'unf': (PJ+'UnFree.lean','Original Unf, rdU, laU, perFr and every field of IsUnf'),
 'principal': ('src/Development/AbelianVarietyTheory/Definitions/RegularCharts/BaseNorm.lean','Literal HasPrinc at the original integer modulus'),
 'domain': (FD+'Signature.lean','First-linear Hermitian convention, signed leading minors, frame domain and Borel action'),
 'family': (TOR+'IsHolPeriods.lean','Literal IsPeriod, FamilyUnif, exponential, derivative and actual theta-family interfaces'),
 'section_bc': (EXT+'GlobalSectionsRankAlgClosed.lean','Retained exact SecBaseChangeSt: locally Noetherian original base and arbitrary affine target'),
 'section_twist': (EXT+'SecBaseChangeAnySt.lean','Retained exact SecTwistSt: all local rings, twisted bases and residue-section lifts'),
 'finite_gauss': (FO+'ExistsRepresentativesQuotientRangeMulVecLin.lean','Finite quotient quadratic form, nondegeneracy and sq_sum_exp_pair, reconstructed by odd primary diagonalization'),
 'gaussian': (HI+'ExistsEqTransposeMulDiagonalMul.lean','Gaussian Fourier integral, exact squared determinant and Poisson inversion'),
 'theta_transform': (HI+'FromBlocksMapIntCastMemSymplecticGroup.lean','Coset completion, exact theta multiplier and theta_halfVec_sq_transform'),
 'theta_zero': (U+'ThetaSqTransformLevelEight.lean','Whole theta_sq_transform_level_eight'),
 'unit_characteristic': (U+'TwoDvdMultiplierOfThetaZActEqUnitMul.lean','Full-lattice periodic unit forces half-characteristic parity invariance'),
 'half_shift': (U+'ThetaSqLawOfZero.lean','Reduction of half-characteristic squares to the zero-characteristic square law'),
 'theta_ratio': (U+'RatioSqEqDetJAut.lean','Rigidified nonvanishing ratio forces kappa squared equal to det jAut, even at a theta zero'),
 'adapted_det': (U+'CmUnitPowFourIdempotentModEight.lean','Host idempotent, determinant interpolation and blocks_det_mod_eight'),
 'integral_det': (U+'IsIntegralDetSubOne.lean','Integral determinant coefficient under a full lattice congruence'),
 'normal_change': (U+'ChangeOfNormalisation.lean','Exact swapped-transposed symplectic blocks and period_change'),
 'frame_ratio': (U+'ExistsSecGeneratorFibre.lean','Actual rigidified line-frame quotient and thetaFrame_ratio'),
 'theta_frame': (U+'ThetaFrameDetMulSqInvariant.lean','Actual family determinant identity, not an abstract bundle replacement'),
 'theta_point': (U+'ThetaPointsChangeLevelIsometryLinearMap.lean','Full thetaPt_change, original derivative and SecBC scalar equation'),
 'period_borel': (U+'TriangularFrameMovesPeriodBlockTriangular.lean','Original period change, triangular support, determinants and all-even-weight character formula'),
 'norm_borel': (U+'NormalisedFramedPointTriangularFrameWeightRule.lean','Whole normUn_bor, one witness before all allowed weights'),
 'period_gamma': (U+'PerFrLact.lean','Literal lattice isometry induced by the original arithmetic group and per_gam'),
 'norm_gamma': (U+'NormalisedFramedPointArithmeticGroupInvariantSig.lean','Whole normUn_gamma, same actual points and section scalar squared one'),
 'algebraic_laws': (U+'FramedModuliAlgebraicLawsChartWeightIntegrality.lean','EvalWD and reduced-algebra weight-law portion; integral/unit-independence clauses are not newly claimed'),
 'frame_charts': (PJ+'FrameCharts.lean','Exact universal chart classifiers, local refinements and triangular relation charts'),
 'chart_wd': (PJ+'ChartWD.lean','Full EvalWD over arbitrary rings and weight transport for test-presented points'),
 'chart_cover': (U+'ChartCoverFOfSectionBaseChange.lean','Original universal-frame chart cover under exact SecBaseChangeSt'),
 'local_coordinates': (U+'ExistsChartHolomorphicCoordinatesNearFrame.lean','Actual finite-type coefficient chart with holomorphic evaluations'),
 'hol_matrix': (U+'DifferentiableOnExponentialFrameMatrix.lean','Arbitrary coefficient algebra and holomorphic eigenframe change'),
 'hol_generator': (U+'DifferentiableOnThetaAlgebraicGeneratorFactor.lean','Arbitrary coefficient algebra and actual theta-section generator factor'),
 'hol_rule': (U+'DifferentiableOnNaturalRuleHolomorphicFrames.lean','All normed complex V and all subsets B; universal full-frame specialization'),
 'hol_reading': (U+'DifferentiableOnReadingsNormalisedThetaPoints.lean','Whole differentiableOn_rdU, including pointwise square roots and all allowed weights'),
 'all_frames': (U+'ExistsFramedPointsAllNormalisationsFamilyUnif.lean','Whole exists_framesOK at exact SecBC and SecTwist premises'),
 'period_onto': (U+'ExistsFrameOfIsPeriod.lean','Actual inverse block construction from every original IsPeriod'),
 'periods': (U+'ExistsFramePeriods.lean','Whole original exists_framePeriods; NFR2 supplies forward/holomorphic fields and NFL18 supplies onto'),
 'period_linear': (U+'FrameOfPeriodLinear.lean','Exact block comparison between two literal frame period maps'),
 'cover': (U+'ExistsInverseBlock.lean','Whole CoverTri and literal derivative equality for every supplied framed point'),
 'fiber': (U+'BlockTriangularOfMulEqOne.lean','Whole FibTri with original lattice isometry, group, Borel and dependent-component equality'),
 'period_rigidity': (U+'UniformizationPeriodLatticeChange.lean','Exact exponential and point identity under level-preserving lattice/linear changes'),
 'derivative_chain': (U+'IsDerivAt0CompLinear.lean','Actual dual-number derivative chain rule for exponential changes'),
 'derivative_comb': (U+'IsCombAtIffIsDerivAt0.lean','Exact tangent combination and derivative-coordinate equivalence'),
 'unf_join': (U+'FamilyUniformisationIsComplexUniformisation.lean','Whole isUnf_built and its covering/fiber/IsSec clauses'),
 'prescribed_conditional': (U+'ExistsFrameUniformisationPrescribedSpaceStatement.lean','Original conditional prescribed-space interface, with N1c, HasseNorm, SecBC and SecTwist exposed'),
 'principal_return': (U+'CongrOfDvdModulus.lean','Original actual exists_unf_hasPrinc return; its global law suppliers remain retained here'),
 'models_interface': (U+'ExistsFlagDomainModelsOfFamilyUniformisation.lean','Prescribed original Hermitian model and exact ModelBase, inherited through PUN11'),
}

CLAIMS = [
 ('NFL1',[],['finite_gauss','theta_transform'],['NFL_STANDARD_ALGEBRA'],
  'Complete finite quadratic Gauss square in the symplectic even-block odd-determinant setting used here, including negative determinant and empty dimension.'),
 ('NFL2',['NFL1'],['gaussian','theta_transform','theta_zero','half_shift'],['NFL_STANDARD_ANALYSIS'],
  'Whole exact theta_halfVec_sq_transform at B,C divisible by four, and whole level-eight zero-characteristic law; multiplier square derived by finite sums and Gaussian Poisson summation.'),
 ('NFL3',['NFL2'],['unit_characteristic','theta_ratio'],['NFL_STANDARD_ANALYSIS'],
  'Entire rigidified unit comparison forces parity invariance and multiplier square; no division at a zero of theta.'),
 ('NFL4',[],['adapted_det','integral_det','contracts'],['NFL_INHERITED_NFR','NFL_INHERITED_PUN','NFL_STANDARD_ALGEBRA'],
  'Original actual level-isometry setting; full off-diagonal divisibility and determinant sign modulo eight on the prescribed adapted lattice.'),
 ('NFL5',['NFL4'],['normal_change','family'],[],
  'Exact period change including transposes, inverse lattice isometry and determinant; linear-map invertibility follows from the period relation.'),
 ('NFL6',['NFL3','NFL4','NFL5'],['frame_ratio','theta_frame','period_rigidity','section_twist'],['NFL_INHERITED_HUF','NFL_INHERITED_NFR','NFL_SECTION_TWIST'],
  'Full determinant identity on the original ThetaData family, with actual line frames and rigidification; no extra theta transformation premise.'),
 ('NFL7',['NFL6'],['theta_point','derivative_chain','frame_ring'],['NFL_INHERITED_HUF','NFL_INHERITED_TDR','NFL_SECTION_TWIST'],
  'Complete original thetaPt_change with the actual base point, original dual-number derivatives and literal SecBC scalar identity.'),
 ('NFL8',[],['period_borel','weights','unf'],['NFL_INHERITED_NFR'],
  'Exact original period/Borel character computation for every allowed weight; the proof uses only evenness of n and retains all eigenblocks.'),
 ('NFL9',['NFL7','NFL8'],['norm_borel','contracts','weights','frame_literal'],['NFL_SECTION_TWIST'],
  'Whole normUn_bor: each original triangular move has one literal FrBor witness before every allowed weight.'),
 ('NFL10',['NFL7'],['period_gamma','norm_gamma','contracts','frame_literal'],['NFL_SECTION_TWIST'],
  'Whole normUn_gamma for the actual arithmetic group, with all original level conditions and one witness for every allowed weight.'),
 ('NFL11',[],['algebraic_laws','frame_charts','chart_wd','chart_cover','frame_ring','rules','frame_literal','section_bc'],['NFL_INHERITED_TDR','NFL_SECTION_BC'],
  'Full EvalWD over arbitrary coefficient rings and full weight law on all reduced coefficient algebras; no restriction on a,n. No claim to the separate integral-lattice/unit-independence conjuncts.'),
 ('NFL12',[],['local_coordinates','family','frame_ring','section_bc'],['NFL_INHERITED_HUF','NFL_INHERITED_TDR','NFL_SECTION_BC'],
  'Actual local test-ring coordinates for every original theta-period family point, with all scalar evaluations holomorphic; GoodEmb/ModelBase/NegXi unnecessary.'),
 ('NFL13',[],['hol_matrix','derivative_comb','derivative_chain'],['NFL_INHERITED_HUF','NFL_INHERITED_TDR','NFL_STANDARD_ANALYSIS','NFL_STANDARD_AG'],
  'Whole original eigenframe holomorphy for arbitrary commutative coefficient R; finite local expressions avoid analytification of Spec R.'),
 ('NFL14',['NFL13'],['hol_generator','section_twist','frame_ring'],['NFL_SECTION_TWIST','NFL_INHERITED_NFR','NFL_STANDARD_AG'],
  'Whole original generator-factor holomorphy for arbitrary R and holomorphic kappa, using actual chart section evaluation at a nonzero point.'),
 ('NFL15',['NFL11'],['hol_rule','frame_ring','rules'],['NFL_INHERITED_TDR','NFL_SECTION_BC'],
  'Whole original differentiableOn_evR scope, strengthened from weighted sections to natural rules; arbitrary normed complex V and arbitrary B, with within-set differentiability.'),
 ('NFL16',['NFL11','NFL12','NFL13','NFL14','NFL15'],['hol_reading','contracts','weights','unf'],['NFL_SECTION_BC','NFL_SECTION_TWIST','NFL_INHERITED_NFR'],
  'Whole original differentiableOn_rdU under IsNormUn, without GoodEmb/ModelBase/NegXi; n=2m replaces pointwise kappa by (C det h)^m.'),
 ('NFL17',['NFL9','NFL10','NFL16'],['all_frames','contracts','section_bc','section_twist'],['NFL_INHERITED_NFR','NFL_INHERITED_TDR','NFL_SECTION_BC','NFL_SECTION_TWIST'],
  'Whole exists_framesOK and simultaneous FromTest on one actual chosen family, before frames, moves, weights and sections.'),
 ('NFL18',[],['period_onto','periods','family','domain'],['NFL_INHERITED_NFR','NFL_STANDARD_ALGEBRA'],
  'Complete reverse-period producer by explicit signed block matrix; together with NFR2 closes all original exists_framePeriods fields including onto.'),
 ('NFL19',['NFL18'],['cover','period_rigidity','derivative_comb','derivative_chain','contracts'],['NFL_INHERITED_HUF','NFL_INHERITED_TDR','NFL_INHERITED_PUN'],
  'Whole CoverTri, in fact exact eigenframe equality, and for every derivative realization in the original quantifier order.'),
 ('NFL20',[],['fiber','period_linear','period_gamma','period_rigidity','derivative_comb','contracts'],['NFL_INHERITED_HUF','NFL_INHERITED_NFR','NFL_INHERITED_PUN'],
  'Whole FibTri with arbitrary original derivative families, exact level-preserving gamma and actual Borel b in the dependent component equality; the proof uses NFL10 only for its period calculation and no section-law premise is necessary.'),
 ('NFL21',['NFL11','NFL19','NFL20'],['unf_join','unf','contracts','domain'],['NFL_SECTION_BC','NFL_INHERITED_NFR'],
  'Whole original isUnf_built for any supplied FramesOK; no additional SecTwist premise is introduced into this join.'),
 ('NFL22',['NFL17','NFL21'],['principal_return','prescribed_conditional','principal','models_interface','section_bc','section_twist'],['NFL_INHERITED_HUF','NFL_INHERITED_PUN','NFL_INHERITED_TDR','NFL_SECTION_BC','NFL_SECTION_TWIST'],
  'Complete actual prescribed-space principal/cusp return conditional on exact retained section laws and supplied Moduli; the source unconditional global-law suppliers are not claimed.'),
]

def sha(x): return hashlib.sha256(x).hexdigest()
def dump(name,obj): (HERE/name).write_text(json.dumps(obj,indent=2,ensure_ascii=False)+'\n')

source_bytes={}
files={}
sources={}
for key,(path,description) in SOURCES.items():
    blob=subprocess.check_output(['git','show',PIN+':'+path],cwd=repo)
    if (repo/path).read_bytes()!=blob:
        raise SystemExit('Working tree differs from pin: '+path)
    source_bytes[key]=blob
    dest=SNAP/path
    dest.parent.mkdir(parents=True,exist_ok=True)
    dest.write_bytes(blob)
    n=len(blob.splitlines())
    url='https://github.com/CocoSgt/riemann-hypothesis-lean/blob/'+PIN+'/'+path
    f={'path':path,'snapshot_file':str(dest.relative_to(ROOT)),
       'bytes':len(blob),'sha256':sha(blob),'file_sha256':sha(blob),
       'source_commit':PIN,'verified_equal_to_pinned_git_blob':True,'url':url}
    files[path]=f
    sources[key]={'id':'NFL_SRC_'+key.upper(),'path':path,'declaration':description,
      'line_start':1,'line_end':n,'source_commit':PIN,'file_sha256':sha(blob),
      'full_file_sha256':sha(blob),'range_sha256':sha(blob),'range_bytes':len(blob),
      'snapshot_file':f['snapshot_file'],'verified_equal_to_pinned_git_blob':True,
      'url':url+f'#L1-L{n}'}

tex=(HERE/'main.tex').read_bytes()
text=tex.decode()
claims=[]
for ident,deps,groups,external,scope in CLAIMS:
    a=text.index('% BEGIN '+ident+'\n')
    b=text.index('% END '+ident+'\n',a)+len('% END '+ident+'\n')
    block=text[a:b].encode()
    title=re.search(r'\\paragraph\{'+ident+r': ([^\n]+)\}',text[a:b]).group(1)
    claims.append({'id':ident,'title':title,'introduced_in':VERSION,'classification':'B',
      'depends_on':deps,'external_input_ids':external,'scope_note':scope,
      'source_groups':groups,'sources':[sources[g] for g in groups],
      'proof_location':{'file':COMPONENT+'/main.tex','label':'claim:'+ident,
        'line_start':text.count('\n',0,a)+1,'line_end':text.count('\n',0,b),
        'sha256':sha(block),'bytes':len(block)},
      'source_proof_is_not_human_proof':True,'status':'written_pending_independent_review',
      'independent_review_files':[]})
common={'artifact_version':VERSION,'component':COMPONENT,'source_commit':PIN,
        'proof_file_sha256':sha(tex),'status':'written_pending_independent_review'}

inherited=[]
for component,idents,use in [
 ('normalized_frames_v50',[f'NFR{i}' for i in range(1,14)],'The actual period dictionary, adapted basis, ThetaData, theta section, arbitrary normalized square roots, all FrameOK fields and the same simultaneous point family.'),
 ('holomorphic_uniformization_v49',['HUF1','HUF21'],'Actual analytic/dual-number dictionary and full FamilyUnif; all original supplied Moduli and classical-foundation scope retained.'),
 ('test_ring_descent_v50',['TDR1','TDR3','TDR5','TDR6','TDR8','TDR12','TDR13'],'Actual eigenframes, arbitrary-ring base change, affine charts, universal frame rings, finite localization capture and reduced-algebra AllTest; exact SecBC scope retained.'),
 ('principal_uniformization_v48',['PUN6','PUN8']+[f'PUN{i}' for i in range(11,20)],'Original half/full level equivalence, rigidity, prescribed Hermitian models, every actual cusp-center lattice and exact A=1 exponent match.'),
]:
    p=ROOT/component
    body=(p/'main.tex').read_bytes()
    t=body.decode()
    prov=json.loads((p/'provenance.json').read_text())
    if prov['proof_file_sha256']!=sha(body):
        raise SystemExit('Inherited full proof mismatch: '+component)
    for ident in idents:
        claim=next(c for c in prov['claims'] if c['id']==ident)
        a=t.index('% BEGIN '+ident+'\n')
        b=t.index('% END '+ident+'\n',a)+len('% END '+ident+'\n')
        block=t[a:b].encode()
        if claim['proof_location']['sha256']!=sha(block):
            raise SystemExit('Inherited block mismatch: '+ident)
        inherited.append({'id':ident,'component':component,'proof_file':component+'/main.tex',
          'proof_file_sha256':sha(body),'proof_block_sha256':sha(block),
          'proof_location':claim['proof_location'],'source_commit':prov['source_commit'],
          'title':claim['title'],'scope_note':claim['scope_note'],'used_for':use,
          'exact_parent_provenance_sha256':sha((p/'provenance.json').read_bytes()),
          'retain_parent_premises_and_classical_foundations':True})

def declaration(group,name):
    s=source_bytes[group].decode()
    m=re.search(r'^theorem\s+'+re.escape(name)+r'(?=\s|\{|\()',s,re.M)
    if not m: raise SystemExit('Declaration missing: '+group+' / '+name)
    end=s.index(':= by',m.start())
    st=s[m.start():end].rstrip()
    return {'source_group':group,'source_path':SOURCES[group][0],
      'declaration_text':st,'line_start':s.count('\n',0,m.start())+1,
      'line_end':s.count('\n',0,end)+1,'source_commit':PIN,
      'declaration_sha256':sha(st.encode()),
      'context':'All earlier variables, namespace and typeclass parameters in the full pinned source file are retained.'}

ENDPOINTS=[
 ('theta_halfVec_sq_transform','NFL2','theta_transform','theta_halfVec_sq_transform','whole_original_endpoint_written','Original B,C divisible by four, all integer half-characteristics with the required parity and every Siegel matrix/argument.'),
 ('theta_sq_transform_level_eight','NFL2','theta_zero','theta_sq_transform_level_eight','whole_original_endpoint_written','Entire original zero-characteristic level-eight law, with exact chi4(det D) factor.'),
 ('thetaPt_change','NFL7','theta_point','thetaPt_change','whole_original_endpoint_written','Original actual ThetaData, SecTwist and level-preserving isometry; invertibility of the arbitrary input matrix follows from its period relation.'),
 ('normUn_bor','NFL9','norm_borel','normUn_bor','whole_original_endpoint_written','SecTwist retained; one actual FrBor witness before all Dom(a,n).'),
 ('normUn_gamma','NFL10','norm_gamma','normUn_gamma','whole_original_endpoint_written','SecTwist retained; actual original Gamma and all Dom(a,n).'),
 ('differentiableOn_frameMatrix','NFL13','hol_matrix','differentiableOn_frameMatrix','whole_original_endpoint_written','Arbitrary commutative coefficient algebra R, exact original open B and actual FrMap/FrChg/IsThetaPt; no GoodEmb/ModelBase/NegXi needed.'),
 ('differentiableOn_generator_factor','NFL14','hol_generator','differentiableOn_generator_factor','whole_original_endpoint_written','Arbitrary R, holomorphic scalar kappa and exact SecTwist retained; actual local section values.'),
 ('differentiableOn_evR','NFL15','hol_rule','differentiableOn_evR','whole_original_endpoint_written','Original arbitrary normed complex V and any subset B; proof strengthens weighted-section input to naturality alone.'),
 ('differentiableOn_rdU','NFL16','hol_reading','differentiableOn_rdU','whole_original_endpoint_written','Exact SecBC/SecTwist and IsNormUn; no GoodEmb/ModelBase/NegXi and no holomorphic square-root hypothesis.'),
 ('exists_framesOK','NFL17','all_frames','exists_framesOK','whole_original_endpoint_written','One original family satisfying all four fields, with exact supplied F/M and two retained section laws.'),
 ('exists_framePeriods','NFL18','periods','exists_framePeriods','whole_original_endpoint_written_with_inherited_NFR2','NFR2 supplies unique literal forward periods and holomorphy; NFL18 proves every original admissible period is realized by an actual frame.'),
 ('CoverFrame.coverTri','NFL19','cover','coverTri','whole_original_endpoint_written','All actual framed points and every derivative realization; proof gives identity triangular coefficients.'),
 ('FibreFlag.fibTri','NFL20','fiber','fibTri','whole_original_endpoint_written','All original component/frame/period/tangent data and the actual level group; no new section law premise is used.'),
 ('isUnf_built','NFL21','unf_join','isUnf_built','whole_original_endpoint_written','Exact original SecBC + FramesOK join; every literal IsUnf field and all Gaussian/section data preserved.'),
 ('exists_frameUniformisation_prescribedSpace','NFL22','prescribed_conditional','_root_.GlobalTheory.T.exists_frameUniformisation_prescribedSpace','whole_original_conditional_endpoint_written','N1c and model/HasseNorm inputs supplied by inherited HUF/PUN in their explicit foundation scope; SecBC and SecTwist retained.'),
 ('exists_unf_hasPrinc','NFL22','principal_return','exists_unf_hasPrinc','conditional_return_complete_global_law_suppliers_retained','Actual complete original output, strengthened conditional interface adding HasPrinc; source global SecBC/SecTwist suppliers are not reconstructed and its unconditional wrapper is not claimed.'),
]
endpoints=[{'endpoint':name,'claim':claim,'status':status,'qualification':note,
            'exact_source_contract':declaration(group,decl)}
           for name,claim,group,decl,status,note in ENDPOINTS]

law_inputs=[]
for ident,group,name,scope in [
 ('NFL_SECTION_BC','section_bc','SecBaseChangeSt','Exact retained original law. Locally Noetherian original scheme; n>=1; basis on a neighborhood; every arbitrary commutative affine target R. Uses actual Moduli.toPolAV at n=1. No flatness, reducedness or Noetherianity restriction on R.'),
 ('NFL_SECTION_TWIST','section_twist','SecTwistSt','Exact retained original law for arbitrary original S/P, q>=1, all local coefficient rings, translated line, q^g basis and every residue-section lift. The proof only consumes its actual complex-fiber instances, but does not claim the global supplier.'),
]:
    s=source_bytes[group].decode()
    a=s.index('def '+name+' : Prop :=')
    match=re.search(r'\n(?:def|theorem|lemma) ',s[a+1:])
    b=a+1+match.start() if match else len(s)
    st=s[a:b].rstrip()
    law_inputs.append({'id':ident,'name':name,'status':'retained_premise_not_discharged',
      'scope_note':scope,'source':sources[group],
      'exact_definition_text':st,'definition_sha256':sha(st.encode())})

foundations=[
 {'id':'NFL_STANDARD_ALGEBRA','status':'ordinary_named_foundations','scope_note':'Finite abelian primary decomposition; integer lattice index equals absolute determinant; finite projective determinants and trace-pairing nondegeneracy. The odd Gauss-sum sign and cyclic recurrence are proved explicitly in NFL1.'},
 {'id':'NFL_STANDARD_ANALYSIS','status':'ordinary_named_foundations','scope_note':'Real Gaussian integration, Poisson summation for Schwartz functions, holomorphic continuation, Cauchy derivative formula, Liouville and the identity theorem. Exact determinant and phase factors are derived in NFL2–NFL3. No theta transformation law is assumed.'},
 {'id':'NFL_STANDARD_AG','status':'ordinary_named_foundations','scope_note':'Smooth finite-presentation algebraic charts, cotangent bases, regular-function holomorphy on complex charts, and local section evaluation. NFL13–NFL14 explain finite expressions for arbitrary R; no analytic structure on Spec R is postulated.'},
]
input_ids=[{'id':'NFL_ORIGINAL_DATA','status':'original_input','scope_note':'Original CM field, host, datum, level, supplied Moduli, coefficient field and embedding. F/M/GoodEmb/ModelBase/NegXi are original hypotheses only where their exact source endpoint requires them.'},
 {'id':'NFL_INHERITED_NFR','status':'inherited_human_proof','claims':[f'NFR{i}' for i in range(1,14)]},
 {'id':'NFL_INHERITED_HUF','status':'inherited_human_proof','claims':['HUF1','HUF21']},
 {'id':'NFL_INHERITED_TDR','status':'inherited_human_proof','claims':['TDR1','TDR3','TDR5','TDR6','TDR8','TDR12','TDR13']},
 {'id':'NFL_INHERITED_PUN','status':'inherited_human_proof','claims':['PUN6','PUN8']+[f'PUN{i}' for i in range(11,20)]}]

dump('source_manifest.json',{'schema':'rh-pinned-source-manifest/1',**common,
 'source_repository':'https://github.com/CocoSgt/riemann-hypothesis-lean',
 'files':list(files.values()),'ranges':list(sources.values()),
 'file_count':len(files),'range_count':len(sources)})
dump('inherited_inputs.json',{'schema':'rh-inherited-human-inputs/1',**common,'inputs':inherited})
dump('retained_foundations.json',{'schema':'rh-retained-foundations/1',**common,
 'original_inputs':input_ids,'section_laws':law_inputs,'ordinary_foundations':foundations,
 'all_inherited_classical_foundations_retained':True,
 'formal_correctness':'The verified Lean proof is accepted as correct. No Lean replay or attempt to diagnose the formal proof is performed.'})
dump('published_inputs.json',{'schema':'rh-human-published-inputs/1',**common,
 'inputs':foundations,'note':'These are named ordinary mathematical foundations; no external theta multiplier, no Hasse/Moduli/section global supplier, and no whole selected obligation is newly asserted.'})
dump('provenance.json',{'schema':'rh-human-claim-provenance/1',**common,
 'source_repository':'https://github.com/CocoSgt/riemann-hypothesis-lean',
 'claims':claims,'claim_count':len(claims),'inherited_inputs':inherited,
 'formal_proof_accepted_correct':True,'lean_replay_performed':False})
dump('contracts.json',{'schema':'rh-human-component-contracts/1',**common,
 'entry_premises':['NFL_ORIGINAL_DATA','NFL_INHERITED_NFR','NFL_INHERITED_HUF','NFL_INHERITED_TDR','NFL_INHERITED_PUN'],
 'retained_laws':law_inputs,'inherited_inputs':inherited,
 'ordinary_foundations':foundations,'completed_source_endpoints':endpoints,
 'supplementary_completed_results':[
  {'claim':'NFL11','result':'Full EvalWD and every reduced-algebra weight law','source_group':'algebraic_laws','limitation':'Separate IntDiagUnit/UnitIndep clauses not newly reconstructed.'},
  {'claim':'NFL17','result':'FromTest at every chosen complex framed point','input':'TDR13','limitation':'Exact SecBaseChangeSt retained.'}],
 'quantifier_guards':[
  'The actual Moduli Xo is supplied throughout; it is never replaced by an abstract period quotient.',
  'One F, M, theta datum per component and point family u are fixed before all points, moves, weights, natural rules and cusps.',
  'Borel and arithmetic witnesses t are selected before every allowed a,n; no bounded-weight replacement.',
  'Dom(a,n) retains antitone embedding weights and even n. Holomorphic readings use n=2m and (C det h)^m, with no regularity of the selected roots.',
  'EvalWD allows arbitrary target rings. The all-point weight law uses reduced target S precisely because TDR13 supplies FromTest there.',
  'Frame/generator holomorphy allows arbitrary possibly nonreduced, non-Noetherian coefficient R; it uses finitely many local coefficient expressions.',
  'HolEval allows arbitrary normed complex V and arbitrary subset B with DifferentiableOn, matching the original helper scope.',
  'CoverTri and FibTri quantify over every supplied derivative realization and retain exact original period maps and dependent component equalities.',
  'HasPrinc uses l.M prime = lcm(l.M,l.A); the ExpoMatch statement assumes l.A=1 and retains the original level l.M.',
  'The complete geometric return remains conditional on exact SecBaseChangeSt/SecTwistSt and inherited named foundations; no global supplier is silently inserted.'],
 'whole_selected_obligations_closed':[],
 'not_claimed':['unconditional global Moduli producer','global SecBaseChangeSt supplier','global SecTwistSt supplier','unconditional source exists_unf_hasPrinc wrapper','selected whole common-family obligation','RH theorem closure','Dirichlet GRH theorem closure']})
dump('closure.json',{'schema':'rh-human-component-closure/1',**common,
 'new_claim_count':22,'completed_source_endpoints':endpoints,
 'complete_internal_results':['theta multiplier square','normUn_bor','normUn_gamma','differentiableOn_rdU','FramesOK','CoverTri','FibTri','IsUnf at original inputs','HasPrinc/LatZ/ExpoMatch/FromTest simultaneous return at retained section laws'],
 'retained_premise_ids':['NFL_ORIGINAL_DATA','NFL_SECTION_BC','NFL_SECTION_TWIST'],
 'all_inherited_foundation_scope_retained':True,'whole_selected_obligations_closed':[],
 'selected_closure_delta':0,
 'scope_boundary':'The final source global-law packages are not reconstructed. Complete original conditional geometry is proved on actual data; no selected whole closure is inferred from internal IsUnf or principal returns.',
 'next_mathematical_work':'Supply the global exact section laws and original Moduli where the later common-family entry demands them; join this actual U to the remaining common-family and reading/normalization producers without choosing new G/xi0 or new coefficient fields.'})

report=f'''NORMALIZED FRAME LAWS v0.51 — NFL1–NFL22
Source pin: {PIN}
Proof SHA256: {sha(tex)}

The verified formal proof is accepted correct. This packet contains actual
human proofs; it does not replay Lean or treat source declarations as proofs.

Completed mathematics
---------------------
1. Exact finite odd quadratic Gauss square and Gaussian/Poisson theta-square
   transformation, including the chi4(det D) sign, half-characteristics and
   zero-dimensional convention. A periodic-unit argument fixes characteristic
   parity; dense-set cancellation permits theta to vanish at zero.
2. Actual host-adapted congruence, period normalization and rigidified theta
   frame comparison. The original SectionBC scalar satisfies the exact
   determinant equation, on the same universal line and exponential.
3. Full normUn_bor and normUn_gamma, with one FrBor witness before all allowed
   weights. The field, model, lattice, levels and section are unchanged.
4. Full EvalWD over arbitrary coefficient rings and the complete weight law
   on all reduced coefficient rings, at exact SecBaseChangeSt. Local original
   charts, holomorphic Lie-frame changes and generator factors work with any
   coefficient algebra. Full natural-rule differentiability allows any normed
   complex V and any subset B, exactly as the source helper requires.
5. All normalized readings are holomorphic: n=2m replaces the arbitrary
   pointwise square root kappa by (C det h)^m. No holomorphic-root hypothesis.
6. Every original admissible period is the literal period of an actual frame,
   by an explicit signed block construction. Full CoverTri and FibTri follow
   with the original tangent families, lattice isometry and arithmetic group.
7. One actual NFR family now satisfies all FramesOK and every IsUnf clause.
   On the prescribed Hermitian space the same U has original HasPrinc at
   l.M'=lcm(l.M,l.A), nonempty components, all characters one, FromTest at all
   points, LatZ at every cusp, and exact ExpoMatch at l.A=1.

Retained scope
--------------
The original Moduli is supplied. Exact SecBaseChangeSt and SecTwistSt remain
retained premises; their full quantified definitions are reproduced in the
contracts. All inherited HUF/PUN/TDR/NFR classical-foundation scope remains.
The source's unconditional final wrapper obtains the section laws from global
packages; these global suppliers are not reconstructed here. No whole selected
RH/GRH obligation is closed. The proof does not alter original coefficient
fields, frames, sections, level, Hermitian G/xi0 or quantifier order.

Evidence
--------
{len(files)} complete source files / {sum(f['bytes'] for f in files.values())} bytes
are verified byte-for-byte against the exact pinned git blobs. {len(inherited)}
inherited proof blocks and all 22 new blocks are SHA256 bound. Draft TeX
validation is separate in tex_validation.json. No PDF or Lean replay.

Independent mathematical review is pending in this generated author packet;
review files, when present, bind the final proof and source hashes separately.
'''
(HERE/'report.txt').write_text(report)
dump('hashes.json',{'schema':'rh-human-component-hashes/1',**common,
 'files':{name:sha((HERE/name).read_bytes()) for name in [
   'main.tex','provenance.json','source_manifest.json','contracts.json','closure.json',
   'inherited_inputs.json','retained_foundations.json','published_inputs.json','report.txt']},
 'proof_blocks':{c['id']:c['proof_location']['sha256'] for c in claims}})
print(json.dumps({'component':COMPONENT,'proof_sha256':sha(tex),'claims':len(claims),
 'source_files':len(files),'source_bytes':sum(f['bytes'] for f in files.values()),
 'inherited_blocks':len(inherited),'whole_selected_closure_delta':0},indent=2))
