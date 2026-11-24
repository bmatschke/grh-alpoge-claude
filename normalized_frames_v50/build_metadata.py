#!/usr/bin/env python3
"""Bind the normalized-frame proof to exact pinned Lean sources and inherited proofs."""
from pathlib import Path
import argparse
import hashlib
import json
import re
import subprocess

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
PIN = '7cbf7a0c32fca1badf05931879a37c3f8a2b03b4'
VERSION = '0.50'
COMPONENT = HERE.name
SNAP = ROOT / 'source_snapshot_v0_50' / 'normalized_frames'
parser = argparse.ArgumentParser()
parser.add_argument('--repo', type=Path, required=True)
args = parser.parse_args()
repo = args.repo.resolve()
BASE = 'src/Development/AbelianVarietyTheory/Proofs/UnitaryExistence/'
TOR = 'src/ReciprocityTheory/ReductiveGroups/ArithmeticGeometry/BirationalGeometry/ToroidalCompactification/'
FD = 'src/ReciprocityTheory/ReductiveGroups/ArithmeticGeometry/FundamentalDomains/'
EXT = 'src/ReciprocityTheory/ReductiveGroups/ArithmeticGeometry/ExtensionDescent/'
PJ = 'src/Formalism/LocalToGlobal/ProjectiveLattices/'
SOURCES = {
 'contracts': ('src/Development/AbelianVarietyTheory/Definitions/ExistenceOfLattices/NormConst.lean',14,None,'ModelsOf, ModelBase, FrameOK, FramesOK, NegXi, ThetaData, IsThetaPt, normConst, IsNormUn'),
 'period_family': (TOR+'IsHolPeriods.lean',12,None,'Literal IsPeriod, IsThetaFrame and FamilyUnif, including HUF21 theta and derivative interfaces'),
 'domain': (FD+'Signature.lean',12,111,'Actual first-linear Hermitian forms, signed-minor frame domain, upper triangular group and Data'),
 'per_fr': (PJ+'UnFree.lean',46,78,'Literal relab, GoodEmb and perFr with reversed early columns'),
 'relabel': (BASE+'RelabelEmbeddingsGoodBijectiveConjCompat.lean',17,None,'relab_good: bijection, CM conjugation and host-type preservation'),
 'dictionary': (BASE+'CmTypeLetterFrameColumnDictionary.lean',14,None,'Actual embedding, multiplicity and frame-column dictionary'),
 'period_form': (BASE+'HermFormConjDiag.lean',15,None,'Real period-coordinate isomorphism and complete isPeriod_frame'),
 'frame_periods': (BASE+'ExistsFramePeriods.lean',14,None,'Period and holomorphic-period portion of exists_framePeriods; source onto clause is not claimed here'),
 'orthonormal': (BASE+'UnitFrameEqOrthonormalMulTriangular.lean',14,None,'Hermitian elimination and unit-minor orthonormal times triangular factorization'),
 'period_change': (BASE+'TriangularFrameMovesPeriodBlockTriangular.lean',14,None,'Actual period change matrix and determinant; the final general character identity is not claimed by NFR'),
 'trace_sign': (BASE+'MemIffConjugateNotMem.lean',14,None,'CM trace pairing and first-q positive column sign convention'),
 'mod_eight': (BASE+'HostGeneratorPowFourTraceNormModEight.lean',14,None,'Host-generator congruences and exact exists_symplectic_basis_adapted_mod_eight'),
 'symplectic_lift': ('src/Development/AbelianVarietyTheory/Proofs/FoundationProofs/ExistsIsSymplecticBasisToMatrixOffDiagDvd.lean',190,None,'Integral symplectic lifting and adapted basis; NFR3 proves the required modulus-eight specialization'),
 'theta_data': (BASE+'NonemptyThetaDataFlagDomainModels.lean',21,None,'Complete nonempty_thetaData on the original family and models'),
 'theta_frame': ('src/Development/AbelianVarietyTheory/Proofs/ModuliProofs/ExistsThetaFrameFrames.lean',14,None,'Open frame domain and FamilyUnif.theta on that domain'),
 'connected_domain': ('src/Development/AbelianVarietyTheory/Proofs/CuspFormEvaluations/ContinuousRmulPair.lean',14,None,'frames_isConnected, replaced by the explicit indefinite-unitary graph proof'),
 'theta_half': (BASE+'ThetaCharHalfDifferentiableNeZeroFamilies.lean',19,None,'Half-characteristic theta holomorphy, nonvanishing and all holomorphic families'),
 'section_values': (BASE+'SecValuesComplexFibreAbelianScheme.lean',18,None,'Actual algebraic section values on the complex fiber; NFR5 supplies its rank-one conclusion directly for ThetaData'),
 'theta_point': (BASE+'ExistsThetaPt.lean',21,None,'Actual generating section and complete exists_thetaPt'),
 'norm_point': (BASE+'ExistsNormalisedFramedPointOnEachComponent.lean',17,None,'Positive normConst and complete exists_isNormUn'),
 'hermitian_identity': (BASE+'HermEqOfNormalised.lean',23,None,'Complete herm_eq_of_normalised for the supplied Hermitian form'),
 'determinant': (BASE+'EqOfImHermFormEq.lean',24,None,'Uniqueness from the lattice imaginary form and complete UnitDet.det_eq_prod'),
 'fundamental_mean': (BASE+'ExistsFundamentalDomainMeanNormSqThetaChar.lean',9,None,'Actual lattice fundamental domain and the exact normalized theta mean'),
 'theta_integral': ('src/Development/AbelianVarietyTheory/Proofs/ThetaLawProofs/LintegralLintegralNormSqRiemannTheta.lean',14,None,'Gaussian integral, Fourier orthogonality and exact integral_norm_sq_thetaChar'),
 'automorphy': (BASE+'ExpMulThetaCharAutomorphy.lean',25,None,'Exact translation factor, quadratic gauge and exp_mul_thetaChar_automorphy'),
 'frame_ok': (BASE+'NormalisedPointsSatisfySingleFrame.lean',22,None,'Dense-set cancellation, scalar normalization and complete frameOK_of_isNormUn'),
 'models_interface': (BASE+'ExistsFlagDomainModelsOfFamilyUniformisation.lean',66,None,'Exact original PUN11 model producer, preserving fixed Hermitian matrix and imaginary scalar'),
 'frame_record': (PJ+'IsCombAt.lean',44,124,'Actual tangent-combination predicate, SecGen, FrPt and FrMap inherited through TDR1'),
 'section_bc': (EXT+'GlobalSectionsRankAlgClosed.lean',32,44,'Exact retained SecBaseChangeSt used only for the NFR13 FromTest corollary'),
 'section_twist': (EXT+'SecBaseChangeAnySt.lean',49,58,'Original SecTwistSt antecedent in the source endpoints; neither assumed nor globally supplied by NFR'),
 'from_test': (PJ+'AlgebraMapCAt.lean',9,57,'Literal FromTest witness and reduced finite-presentation TRing'),
}

CLAIMS = [
 ('NFR1',[],['contracts','domain','per_fr','relabel','dictionary'],['NFR_ORIGINAL_DATA','NFR_INHERITED_MODELS'],
  'Exact CM embedding/multiplicity dictionary and literal period coordinates on the same model lattice.'),
 ('NFR2',['NFR1'],['period_form','frame_periods','orthonormal','period_change','trace_sign','connected_domain','period_family'],['NFR_STANDARD_ANALYSIS'],
  'Complete IsPeriod, holomorphic periods and open connected frame domain, with the correct first-linear sign convention; no claim to the separate onto clause.'),
 ('NFR3',[],['mod_eight','symplectic_lift'],['NFR_ORIGINAL_DATA','NFR_STANDARD_ALGEBRA'],
  'Whole original host-adapted integral symplectic basis at modulus eight, including a direct symplectic lifting proof.'),
 ('NFR4',['NFR1','NFR2','NFR3'],['contracts','theta_data','theta_frame','period_family'],['NFR_HUF_THETA'],
  'Complete original ThetaData, including a single fixed pair of half characteristics and the actual algebraic section/frame over the whole connected domain.'),
 ('NFR5',['NFR4'],['theta_half','automorphy','section_values','section_twist'],['NFR_STANDARD_ANALYSIS','NFR_STANDARD_AG'],
  'Theta convergence/nonvanishing and direct Fourier classification of the actual complex theta-section line. No new SecTwistSt or base-change premise.'),
 ('NFR6',['NFR4','NFR5'],['theta_point','norm_point','contracts','frame_record','period_family'],['NFR_HUF_DERIVATIVE','NFR_TDR_TANGENT'],
  'Complete actual IsThetaPt and IsNormUn constructors, with arbitrary pointwise square-root choices and the original FrPt section/tangent fields.'),
 ('NFR7',[],['hermitian_identity'],['NFR_STANDARD_ALGEBRA'],
  'Whole normalized Hermitian identity H=h^t(Im tau)^(-1)conj(h) and exact determinant relation.'),
 ('NFR8',['NFR1','NFR2'],['determinant','orthonormal','period_change','trace_sign'],[],
  'Whole original UnitDet.det_eq_prod at every unit-minor frame, for the actual supplied Hermitian form.'),
 ('NFR9',[],['fundamental_mean','theta_integral'],['NFR_STANDARD_ANALYSIS'],
  'Whole original exact theta mean on an actual lattice fundamental domain, with the original Lebesgue measure and empty-dimensional conventions.'),
 ('NFR10',['NFR5','NFR7'],['automorphy'],[],
  'Whole original quadratic-gauge automorphy and Gaussian weight identity, with the original first-linear Hermitian convention.'),
 ('NFR11',['NFR7','NFR8','NFR9','NFR10'],['frame_ok','contracts'],[],
  'Exact normConst and determinant normalization force mean exactly one, independently of the square-root sign.'),
 ('NFR12',['NFR5','NFR7','NFR8','NFR9','NFR10','NFR11'],['frame_ok','contracts','frame_record'],[],
  'Complete original frameOK_of_isNormUn for every allowed original ThetaData and normalized point family; all algebraic section values and rigidifications retained.'),
 ('NFR13',['NFR4','NFR6','NFR12'],['contracts','period_family','models_interface','from_test','section_bc'],['NFR_TDR_ALLTEST'],
  'One simultaneous actual family satisfying the first FramesOK field; pointwise literal FromTest under the exact already retained SecBaseChangeSt premise.'),
]

def sha(b): return hashlib.sha256(b).hexdigest()
def dump(name,value): (HERE/name).write_text(json.dumps(value,indent=2,ensure_ascii=False)+'\n')

files = {}
sources = {}
source_bytes = {}
for key,(path,a,b,declaration) in SOURCES.items():
    pinned=subprocess.check_output(['git','show',PIN+':'+path],cwd=repo)
    if (repo/path).read_bytes() != pinned:
        raise SystemExit('Working source differs from pin: '+path)
    source_bytes[key]=pinned
    dest=SNAP/path
    dest.parent.mkdir(parents=True,exist_ok=True)
    dest.write_bytes(pinned)
    lines=pinned.splitlines(keepends=True)
    b=len(lines) if b is None else b
    if not 1<=a<=b<=len(lines): raise SystemExit('Invalid source range: '+key)
    data=b''.join(lines[a-1:b])
    url='https://github.com/CocoSgt/riemann-hypothesis-lean/blob/'+PIN+'/'+path
    files[path]={'path':path,'snapshot_file':str(dest.relative_to(ROOT)),
      'bytes':len(pinned),'sha256':sha(pinned),'file_sha256':sha(pinned),
      'source_commit':PIN,'verified_equal_to_pinned_git_blob':True,'url':url}
    sources[key]={'id':'NFR_SRC_'+key.upper(),'path':path,'declaration':declaration,
      'line_start':a,'line_end':b,'source_commit':PIN,'file_sha256':sha(pinned),
      'full_file_sha256':sha(pinned),'range_sha256':sha(data),'range_bytes':len(data),
      'snapshot_file':str(dest.relative_to(ROOT)),'verified_equal_to_pinned_git_blob':True,
      'url':url+f'#L{a}-L{b}'}

tex=(HERE/'main.tex').read_bytes()
text=tex.decode()
claims=[]
for ident,deps,groups,external,scope in CLAIMS:
    start=text.index('% BEGIN '+ident+'\n')
    end=text.index('% END '+ident+'\n',start)+len('% END '+ident+'\n')
    block=text[start:end].encode()
    title=re.search(r'\\paragraph\{'+ident+r': ([^\n]+)\}',text[start:end]).group(1)
    claims.append({'id':ident,'title':title,'introduced_in':VERSION,'classification':'B',
      'depends_on':deps,'external_input_ids':external,'scope_note':scope,'source_groups':groups,
      'sources':[sources[g] for g in groups],
      'proof_location':{'file':COMPONENT+'/main.tex','label':'claim:'+ident,
        'line_start':text.count('\n',0,start)+1,'line_end':text.count('\n',0,end),
        'sha256':sha(block),'bytes':len(block)},
      'source_proof_is_not_human_proof':True,'status':'written_pending_independent_review',
      'independent_review_files':[]})
common={'artifact_version':VERSION,'component':COMPONENT,'source_commit':PIN,
        'proof_file_sha256':sha(tex),'status':'written_pending_independent_review'}

# Verify inherited blocks against their existing provenance, retaining exact scope.
inherited=[]
for component,idents,use in [
 ('holomorphic_uniformization_v49',['HUF1','HUF20','HUF21'],'Actual dual-number derivatives and the complete simultaneous FamilyUnif/theta constructor, at its original Moduli and classical-foundation scope.'),
 ('principal_uniformization_v48',['PUN11'],'ModelsOf, full ModelBase and NegXi for the same family and the original fixed Hermitian/arithmetic coordinates.'),
 ('test_ring_descent_v50',['TDR1','TDR13'],'TDR1 identifies actual tangent eigenframes without base-change assumptions. TDR13 is used only for FromTest and retains exact SecBaseChangeSt.'),
]:
    p=ROOT/component
    body=(p/'main.tex').read_bytes()
    t=body.decode()
    provenance=json.loads((p/'provenance.json').read_text())
    if provenance['proof_file_sha256'] != sha(body):
        raise SystemExit('Inherited proof hash mismatch: '+component)
    for ident in idents:
        cl=next(c for c in provenance['claims'] if c['id']==ident)
        a=t.index('% BEGIN '+ident+'\n')
        b=t.index('% END '+ident+'\n',a)+len('% END '+ident+'\n')
        block=t[a:b].encode()
        if cl['proof_location']['sha256'] != sha(block):
            raise SystemExit('Inherited block hash mismatch: '+ident)
        inherited.append({'id':ident,'component':component,'proof_file':component+'/main.tex',
          'proof_file_sha256':sha(body),'proof_block_sha256':sha(block),
          'proof_location':cl['proof_location'],'source_commit':provenance['source_commit'],
          'title':cl['title'],'scope_note':cl['scope_note'],'used_for':use,
          'exact_parent_provenance_sha256':sha((p/'provenance.json').read_bytes()),
          'retain_parent_premises_and_classical_foundations':True})

dump('source_manifest.json',{'schema':'rh-pinned-source-manifest/1',**common,
  'source_repository':'https://github.com/CocoSgt/riemann-hypothesis-lean',
  'files':list(files.values()),'ranges':list(sources.values()),
  'file_count':len(files),'range_count':len(sources)})
dump('inherited_inputs.json',{'schema':'rh-inherited-human-inputs/1',**common,'inputs':inherited,
  'comparison_only':'TDR2 is mentioned only to compare descriptions of the actual section line; NFR5 independently proves its required complex-fiber conclusion and does not import its base-change premise.'})
dump('provenance.json',{'schema':'rh-human-component-provenance/1',**common,
  'main_tex_sha256':sha(tex),'claims':claims,'inherited_human_inputs':inherited,
  'dependency_convention':'All claims retain the fixed original data and model inputs. Only NFR13 FromTest uses SecBaseChangeSt. Source SecTwistSt is not a new premise: NFR5 proves the required actual complex-fiber rank-one statement.'})

foundations=[
 {'id':'NFR_ORIGINAL_DATA','kind':'original_supplied_data',
  'statement':'Original E, CM Host, Datum, Level, Coeff, GoodEmb, ordered multiplicity equivalence and supplied Moduli record; no new existence theorem for the moduli scheme.'},
 {'id':'NFR_INHERITED_MODELS','kind':'inherited_human_proof',
  'statement':'HUF21 supplies the original FamilyUnif at its stated rank and foundation scope. PUN11 supplies ModelsOf, ModelBase and NegXi with the original fixed Hermitian coordinates and all original arithmetic premises preserved.',
  'claim_ids':['HUF21','PUN11']},
 {'id':'NFR_HUF_THETA','kind':'inherited_human_proof',
  'statement':'HUF20 and HUF21 supply the theta-frame law on every open preconnected base, for the prescribed integral symplectic basis and the same universal line.',
  'claim_ids':['HUF20','HUF21']},
 {'id':'NFR_HUF_DERIVATIVE','kind':'inherited_human_proof',
  'statement':'HUF1 identifies analytic derivatives with literal dual-number tangent maps; FamilyUnif.ex_diff and equivariance give the actual ordered eigenbasis.',
  'claim_ids':['HUF1','HUF21']},
 {'id':'NFR_TDR_TANGENT','kind':'inherited_human_proof',
  'statement':'TDR1 identifies the original tangent and IsCombAt predicates with the same Lie eigenbundle frames; it needs no section-base-change premise.',
  'claim_ids':['TDR1']},
 {'id':'NFR_TDR_ALLTEST','kind':'inherited_human_proof_with_retained_original_premise',
  'statement':'Only the NFR13 FromTest conclusion uses TDR13, with exact SecBaseChangeSt: original locally Noetherian base, arbitrary coefficient target. No stronger AnySt hypothesis.',
  'claim_ids':['TDR13'],'source':sources['section_bc']},
 {'id':'NFR_STANDARD_ALGEBRA','kind':'standard_foundational_algebra',
  'statement':'Finite free modules, duality of unimodular alternating forms, determinants and Hermitian linear algebra. The adapted modulus-eight basis and symplectic lifting required here are proved in NFR3.'},
 {'id':'NFR_STANDARD_ANALYSIS','kind':'standard_foundational_real_and_complex_analysis',
  'statement':'Normal convergence, Cauchy/Laurent expansion, identity theorem, elementary finite-dimensional inverse-function arguments, Fubini/Tonelli and linear changes of variables. Theta nonvanishing, coefficient classification, unitary connectedness and Gaussian constants are explicitly proved in NFR2/NFR5/NFR9.'},
 {'id':'NFR_STANDARD_AG','kind':'standard_foundational_algebraic_geometry',
  'statement':'An actual regular section is determined by its complex closed-point values on a reduced finite-type complex scheme; pullback of line bundles and the fiber-product universal property. The actual universal fibers are smooth. No GAGA or new rank-one section theorem is assumed here.'},
]
dump('retained_foundations.json',{'schema':'rh-retained-foundations/1',**common,'foundations':foundations,
  'no_new_published_theorem':True,'no_new_SecTwistSt_premise':True})

def theorem_contract(key,name):
    s=source_bytes[key].decode()
    pat=re.search(r'^theorem\s+(?:_root_\.)?'+re.escape(name)+r'\b',s,re.M)
    if not pat: raise SystemExit('Missing theorem contract '+name)
    a=pat.start()
    b=s.index(':= by',a)
    return {'source_group':key,'declaration_text':s[a:b].rstrip(),
      'line_start':s.count('\n',0,a)+1,'line_end':s.count('\n',0,b)+1,
      'source_commit':PIN,'declaration_sha256':sha(s[a:b].rstrip().encode()),
      'context':'All earlier variables and namespace/typeclass parameters in the pinned source file are retained.'}

endpoints=[]
for name,key,claim,qualification in [
 ('GlobalTheory.exists_symplectic_basis_adapted_mod_eight','mod_eight','NFR3','Complete original endpoint; the general arbitrary-modulus adapted-basis utility is used only at eight and proved there directly.'),
 ('nonempty_thetaData','theta_data','NFR4','Complete original endpoint for the supplied F/M with GoodEmb, ModelBase and NegXi.'),
 ('exists_thetaPt','theta_point','NFR6','Complete original implication, strengthened on actual ThetaData fibers by NFR5 so that SecTwistSt is unnecessary here; the global SecTwistSt statement is not claimed.'),
 ('exists_isNormUn','norm_point','NFR6','Complete original constructor and choice order. No holomorphic square root is assumed.'),
 ('herm_eq_of_normalised','hermitian_identity','NFR7','Complete original identity for the supplied normalized period data and Hermitian form.'),
 ('det_eq_prod','determinant','NFR8','Complete original exact determinant on every unit-minor frame.'),
 ('exists_fundamentalDomain_mean_norm_sq_thetaChar','fundamental_mean','NFR9','Complete original fundamental domain and exact mean, including finite positive volume.'),
 ('GlobalTheory.ThetaAH.exp_mul_thetaChar_automorphy','automorphy','NFR10','Complete original gauge automorphy and weight identity.'),
 ('frameOK_of_isNormUn','frame_ok','NFR12','Complete original FrameOK implication for every supplied original T/un; its source SecTwistSt antecedent is unused and not needed by the reconstruction.'),
]:
    endpoints.append({'endpoint':name,'claim':claim,'status':'whole_original_endpoint_written',
      'qualification':qualification,'exact_source_contract':theorem_contract(key,name)})

remaining=[
 'Original Moduli and the exact inherited HUF/PUN arithmetic and named classical foundations remain at their documented scope.',
 'Full FramesOK is not supplied: its triangular FrBor/character covariance, arithmetic-group FrBor/character invariance, and holomorphic readings are still adjoining producers.',
 'CoverTri, FibTri and the complete IsUnf/principal-uniformization assembly are not supplied.',
 'The global SecTwistSt predicate and its algebraic all-base supplier are not proved. NFR5 instead proves only the actual complex-fiber section-line statement needed for the original theta points.',
 'SecBaseChangeSt remains an exact original premise only for NFR13 FromTest, inherited from TDR13.',
 'No selected compound common-family obligation, full RH proof or full Dirichlet GRH proof is closed by this component.',
]
dump('contracts.json',{'schema':'rh-human-component-contracts/1',**common,
  'entry_premises':['NFR_ORIGINAL_DATA','NFR_INHERITED_MODELS'],
  'inherited_inputs':inherited,'completed_source_endpoints':endpoints,
  'extra_hypotheses_introduced':[],
  'choice_order':['Fix the actual original family F and models M.','Choose one ThetaData on each entire connected frame domain.','For each frame choose a nonzero square root and its actual framed point.','Choose these functions once before universally quantifying the frame; FrameOK holds for every choice.','Only for FromTest, apply TDR13 to each of these very framed points; its ring may depend on component and frame.'],
  'full_ThetaData_supplied':True,'full_original_IsNormUn_supplied':True,
  'full_original_FrameOK_supplied':True,'full_FramesOK_supplied':False,
  'FramesOK_fields_supplied':[1],'FramesOK_fields_remaining':[2,3,4],
  'same_actual_family_and_line':True,'mean_exactly_one':True,
  'SecTwistSt_required':False,'SecBaseChangeSt_only_for_FromTest':True,
  'original_definition_source':sources['contracts'],'remaining':remaining})
dump('closure.json',{'schema':'rh-human-component-closure/1',**common,
  'completed_source_endpoints':endpoints,'whole_obligations_closed':[],
  'proposed_global_frontier_leaf_closures':[],
  'full_ThetaData_supplied':True,'full_original_IsNormUn_supplied':True,
  'full_original_FrameOK_supplied':True,'full_FramesOK_supplied':False,
  'full_principal_uniformization_supplied':False,
  'independent_reviews':[],'remaining':remaining})
dump('published_inputs.json',[])
(HERE/'report.txt').write_text(
 'ACTUAL NORMALIZED THETA POINTS AND COMPLETE SINGLE-FRAME THEOREM — v0.50\n'
 f'Source pin: {PIN}\nProof SHA256: {sha(tex)}\n'
 f'Claims: {len(claims)}; source files: {len(files)}; exact source ranges: {len(sources)}.\n'
 'Status: complete human proofs at stated original scope; independent review pending.\n\n'
 'NFR1–NFR4 reconstruct the literal CM column dictionary, real period map,\n'
 'positive Hermitian form, open connected flag domain, exact modulus-eight\n'
 'adapted integral symplectic basis and complete original ThetaData.\n'
 'The fixed half characteristics and frame belong to the actual universal line.\n\n'
 'NFR5 classifies all sections of that actual complex theta line by Fourier\n'
 'coefficients and proves it is one-dimensional. This proves exactly the\n'
 'complex-fiber fact needed for the theta-point constructor without adding\n'
 'SecTwistSt. It does not purport to prove global SecTwistSt on all bases.\n'
 'NFR6 constructs the literal FrPt and IsNormUn with its original tangent\n'
 'eigenframes and algebraic generating section. Square roots are pointwise;\n'
 'no global or holomorphic square-root choice is used.\n\n'
 'NFR7–NFR11 prove the exact Hermitian determinant identity, unit-minor\n'
 'determinant product, real fundamental-domain theta integral, holomorphic\n'
 'gauge automorphy and mean-one scalar normalization. All signs and powers\n'
 'of two are checked against the first-linear source convention.\n\n'
 'NFR12 proves every clause of the full original FrameOK implication, for\n'
 'every allowed ThetaData and normalized point family. NFR13 chooses one\n'
 'actual simultaneous family and applies the already proved TDR13 to these\n'
 'very points, giving literal FromTest at the exact SecBaseChangeSt premise.\n\n'
 'Retained: supplied original Moduli, exact HUF/PUN foundations and arithmetic\n'
 'scope; SecBaseChangeSt only for FromTest. Remaining: three FramesOK fields,\n'
 'CoverTri, FibTri and IsUnf. No whole common-family/RH/GRH obligation closed.\n'
 'No new published theorem is assumed; no Lean replay or PDF is claimed.\n\n'
 'Rebuild: python build_metadata.py --repo /path/to/pinned/formal_source\n'
 'Validate: python validate_tex.py --format /path/to/pdflatex.fmt\n'
 'All snapshots were compared byte-for-byte against git show at the pin.\n')
dump('hashes.json',{p.name:sha(p.read_bytes()) for p in HERE.iterdir()
                    if p.is_file() and p.name!='hashes.json'})
print(json.dumps({'component':COMPONENT,'claims':len(claims),'files':len(files),
                  'ranges':len(sources),'proof_sha256':sha(tex),'inherited_claims':len(inherited)}))
