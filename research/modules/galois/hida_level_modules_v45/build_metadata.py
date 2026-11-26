#!/usr/bin/env python3
"""Rebuild exact source and human-proof bindings for the all-level HLM packet."""
from pathlib import Path
import argparse
import hashlib
import json
import re
import subprocess

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
PIN = '7cbf7a0c32fca1badf05931879a37c3f8a2b03b4'
parser = argparse.ArgumentParser()
parser.add_argument('--repo', required=True, type=Path)
repo = parser.parse_args().repo.resolve()
sha = lambda b: hashlib.sha256(b).hexdigest()
B = 'src/Development/AutomorphicArithmetic/AutomorphicVarieties/'
H = B + 'HeckeAlgebras/'
O = H + 'OrdinaryHeckeCharacters/'
D = B + 'ModularityArgument/ThresholdArguments/DenseThresholdCases/'
C = B + 'BuildingsResidueChars/'
F = 'src/Development/AutomorphicArithmetic/Foundations/GaloisRepresentations/AdmissibleResidues/'
specs = {
 'ordinary_definitions': (H+'ContinuousTorusCharacter.lean',151,264,'actual ra, Sp, Ord, locPart and heckeAlg'),
 'hecke_definitions': (H+'CoefficientRepTrivialOnUnramified.lean',75,175,'HSet, Ax, lev, MK, IsWt'),
 'universal_definitions': (H+'CoefficientRepTrivialOnUnramified.lean',253,275,'TK and all five IsUniv fields'),
 'ideal_definition': (H+'IsTheta.lean',40,53,'IsMap and both branches of IsJ'),
 'ordinary_projectivity': (O+'OrdProj.lean',1,None,'full ordProj, exact Higman criterion, neat selector and ordinary projector'),
 'union_representation': (O+'PiBasic.lean',1,None,'full piBasic with actual union, fixed spaces, group quotients and projectivity'),
 'integral_law_extension': (B+'CommutativeAlgebraHeight/DGext.lean',1,None,'full group-coefficient determinant extension'),
 'integral_word_polynomials': (B+'CommutativeAlgebraHeight/DExtPoly.lean',1,None,'integral determinant word polynomial formulas'),
 'core_determinant_helpers': (D+'TCoreDet.lean',1,290,'compactness, local characters, extension and determinant gluing helpers'),
 'core_determinant': (D+'TCoreDet.lean',291,None,'full coreDet_alt'),
 'unique_pair': (D+'TCoreUniq.lean',1,None,'full core_unique_of_axioms_weight_char'),
 'action_compatibility': (D+'LevelUR2Compat.lean',1,None,'actual restriction algebra and unique-map action comparison'),
 'all_level_action': (D+'LevelUR2ActEx.lean',1,None,'full levelUR2ActEx_alt and directed action construction'),
 'ideal_existence': (D+'ExistsHeckeIdeal.lean',1,None,'full exists_hecke_ideal'),
 'determinant_reduction': (D+'HeckeDeterminantReductionEqResidual.lean',1,None,'actual residual determinant equality'),
 'ordinary_characters': (D+'ExistsOrdinaryCharactersHeckeAlgebra.lean',1,None,'all IsPsi fields and weight compatibility'),
 'deformation_relations': (D+'HeckeDeterminantSatisfiesDeformationRelations.lean',1,None,'original polar, ordered ordinary and type-inertia pair relations'),
 'point_separation': (D+'VLPiPts.lean',1,None,'full piPts_n_alt, global character projection and every-IsRecT local comparisons'),
 'isotypic_selection': (F+'IsoPick.lean',1,None,'actual isotypic component projection'),
 'isotypic_refinement': (F+'IsoRefine.lean',1,None,'finite product refinement with one nonzero vector'),
 'conjugacy_comparison': (D+'WoConj.lean',1,None,'WOT invariance under the original conjugacy'),
 'abstract_union_and_steps': (D+'UmodAbs.lean',1,None,'full umodAbs_alt, step1_alt and step2_alt'),
 'level_group_and_residual': (O+'LevelChangeBaseGroupHomApplyProjection.lean',1,None,'p0, rUp, rN, pairN, lamUp and original compatibility'),
 'up_data': (O+'FreeOfNeat.lean',1,None,'pairUp, opUp, kMax, freeness, Teich uniqueness, residual transport'),
 'type_for_up': (D+'TypeForUp.lean',1,None,'every-family and every-IsRecT type_for_r_up_of_type_for'),
 'unitary_data': (D+'UnitaryHeckeData.lean',19,70,'literal IsTypeAlt, TypeForAlt, UnitaryHeckeData and IsJ'),
 'level_membership': (C+'MemHeckeLevelOfLocalComponentsMem.lean',1,None,'converse coordinate membership by actual section deletion'),
 'level_coordinates': (O+'LevelUR2LevOut.lean',1,None,'forward original level-coordinate tests'),
 'level_equality': (O+'LevelUR2LevEq.lean',1,None,'literal old level equals new maximal-compact level'),
 'section_faithfulness': (O+'LevelUR2Faith.lean',1,None,'full every-section-product levelUR2Faith'),
 'ordinary_point': (D+'LevelUR2OrdPt.lean',1,None,'full ordinary eigencharacter occurs in an original part'),
 'residual_subselection': (O+'LevelUR2LocSub.lean',1,None,'finite algebra residual idempotent comparison'),
 'dense_frobenius_comparison': (D+'ModuleStructureOfCommuting.lean',1,None,'full levelUR2H3Abs_alt and residual congruence comparison'),
 'residual_level_equality': (D+'LevelUR2LocEq.lean',1,None,'full levelUR2LocEq_alt on original function modules'),
 'base_pair_equality': (D+'LevelUR2BaseEq.lean',1,None,'full levelUR2BaseEq_alt, determinant comap and unchanged characters'),
 'scalar_key': (D+'LevelUR2SmulKey.lean',1,None,'full levelUR2SmulKey_alt'),
 'weight_variables': (O+'WeightVariablesExist.lean',1,None,'all-rank levelUR2WtVars and exact coordinate enumeration'),
 'base_action': (O+'LevelUR2BaseAct.lean',1,None,'both IsJ branches, exact action kernel and weight scalar action'),
 'base_pack': (O+'LevelUR2BasePack.lean',1,None,'full original TWBase packing'),
 'iwahori_levels': (O+'LevelUR2IwLev.lean',1,None,'all compact-open iwC levels and original normal inclusion'),
 'iwahori_quotient': (B+'AlgebraTools/IwIwQuot.lean',1,None,'diagonal quotient of the original Iwahori by iwC'),
 'module_pack': (D+'NonemptyUnitaryHeckeParts.lean',1,None,'full levelUR2ModPack_alt, not the separate ordinary-return nonvanishing theorem'),
 'level_alt_definition': (D+'PaLevel.lean',24,57,'LevPtAlt, ClassicalAlt and complete LevelAlt quantifiers'),
 'level_module_definition': (B+'PatchingModules/Classical.lean',18,66,'ellC, UK, UIw, UIw1 and every LevMod field'),
 'base_definition': (B+'PatchingModules/ThetaCoefficientMapEq.lean',147,181,'WtVars and all TWBase fields'),
 'actual_producer': (D+'BaseObjectHomExt.lean',29,None,'full s3/s4 and level_of_isJ_unitaryHeckeData with one base before all levels'),
 'phi_supplier': (B+'WeilGroupCharacters/WeilCharactersModular/PhiAll.lean',1,None,'actual PhiAll from the original CohP'),
 'universal_ring_supplier': (B+'WeilGroupCharacters/WeilCharactersModular/ProModularRingExists.lean',1,None,'b0Ex with its actual nonempty-pair antecedent'),
 'original_hypotheses': (D+'AfDesc.lean',1,None,'original HypothesesH prime and retained literature package'),
}
cache = {}
source_files = {}
sources = {}
for key, (rel, lo, hi, description) in specs.items():
    if rel not in cache:
        data = (repo/rel).read_bytes()
        pinned = subprocess.run(['git','show',PIN+':'+rel], cwd=repo,check=True,stdout=subprocess.PIPE).stdout
        assert data == pinned, rel
        cache[rel] = data
    data = cache[rel]
    lines = data.splitlines(keepends=True)
    hi = hi or len(lines)
    assert 1 <= lo <= hi <= len(lines), (key,lo,hi,len(lines))
    block = b''.join(lines[lo-1:hi])
    url = 'https://github.com/CocoSgt/riemann-hypothesis-lean/blob/'+PIN+'/'+rel
    source_files[rel] = {'path':rel,'sha256':sha(data),'bytes':len(data),'line_count':len(lines),
                        'verified_equal_to_pinned_git_blob':True,'url':url}
    sources[key] = {'id':'HLM_SRC_'+key.upper(),'path':rel,'declaration':description,
      'line_start':lo,'line_end':hi,'sha256':sha(data),'full_file_sha256':sha(data),
      'range_sha256':sha(block),'range_bytes':len(block),'source_commit':PIN,
      'verified_equal_to_pinned_git_blob':True,'url':url+f'#L{lo}-L{hi}'}

relations = {
 1:([],['ordinary_projectivity']),
 2:([],['ordinary_projectivity','ordinary_definitions']),
 3:([1,2,'OST12','OST19'],['ordinary_projectivity','ordinary_definitions']),
 4:(['OHA5','OHA6'],['union_representation','ordinary_definitions']),
 5:([3,4,'OHA8'],['union_representation','hecke_definitions']),
 6:(['ASP2','JSP9'],['integral_law_extension','integral_word_polynomials','core_determinant_helpers']),
 7:([6,'OHA10','AFS20','ASP13','AFS19'],['core_determinant','core_determinant_helpers','universal_definitions']),
 8:([6,'KX1'],['unique_pair','action_compatibility','universal_definitions']),
 9:([6,7,'FNL16','UPA17','AFS5','OHA11','HEP11','JRP6','JRP7','JRP8','JRP9','JRP10','JRP11','JRP12','JSP2'],
    ['ideal_existence','determinant_reduction','ordinary_characters','deformation_relations','ideal_definition']),
 10:([5,8],['all_level_action','action_compatibility','ideal_definition']),
 11:([],['point_separation']),
 12:([],['isotypic_selection','isotypic_refinement','conjugacy_comparison']),
 13:([5,11,12,'ASP13','AFS19','HEP7','OHA11'],['point_separation','abstract_union_and_steps']),
 14:([5,10,13],['abstract_union_and_steps']),
 15:([],['level_group_and_residual','up_data']),
 16:([15,'NTL17'],['type_for_up','up_data','unitary_data']),
 17:(['LTP2'],['level_membership','level_coordinates','level_equality','section_faithfulness']),
 18:([11,'ASP13','AFS9','CFD12'],['ordinary_point']),
 19:([18,'OHA5','OHA6','ASP2'],['residual_subselection','dense_frobenius_comparison']),
 20:([15,16,17,19,'FNL16','AFS5','UPA17'],['residual_level_equality','abstract_union_and_steps']),
 21:([6,15,'KX1'],['base_pair_equality']),
 22:([5,10,20,21],['scalar_key','actual_producer']),
 23:(['KX3','KX4','KX5','OHA8'],['weight_variables','base_action','base_pack','base_definition']),
 24:([9,14,15,16,17,20,22,23,'KX3','KX4','KX6','KX7','KX8','KX9','FNL16','AFS5','UPA17','NTL17'],
     ['actual_producer','abstract_union_and_steps','phi_supplier','universal_ring_supplier','original_hypotheses']),
 25:([5,13,15,22,24],['module_pack','iwahori_levels','iwahori_quotient','level_module_definition','level_alt_definition']),
 26:([23,24,25],['actual_producer','level_alt_definition','original_hypotheses']),
}
foundations = [
 {'id':'HLM_ORIGINAL_H_PRIME','name':'Original HypothesesH prime and LiteratureRankNHypothesis',
  'introduced_here':False,'status':'retained original hypothesis',
  'scope':'Original unitary automorphic, local correspondence/type and reciprocity inputs, as already matched in UPA17, AFS and KX. HLM does not reprove these literature foundations.'},
 {'id':'HLM_FULL_LOCAL_RECIPROCITY','name':'Original full local Artin/LocCFT interface',
  'introduced_here':False,'status':'retained original local foundation through KX3 and the source Artin specification',
  'scope':'Weil density, reciprocity on all units and the original uniformizer, finite quotient character extension, actual local Dec/I = Zhat; no preferred IsRecT is selected.'},
 {'id':'HLM_ORIGINAL_COHOMOLOGY','name':'Original local/global cohomological finiteness and structural package',
  'introduced_here':False,'status':'retained input used through KX3 and KX6',
  'scope':'The supplied lf, lt, le, gf, ge, gw, pt and tame-from-duality package; only required fields are consumed. The auxiliary universal ring has the actual pulled-back Pair as its nonemptiness witness.'},
 {'id':'HLM_INHERITED_DETERMINANT_REPRESENTABILITY','name':'Chenevier continuous determinant representability in KX7',
  'introduced_here':False,'status':'retained primary literature foundation already matched in KX7',
  'scope':'Arbitrary original rank and coefficient prime, including ell <= n; no division by n! and no irreducibility requirement. This is used only for the new universal ordinary ring, not for HLM6 interpolation.'},
]
external_for = {7:['HLM_FULL_LOCAL_RECIPROCITY'],8:['HLM_FULL_LOCAL_RECIPROCITY'],
 9:['HLM_ORIGINAL_H_PRIME','HLM_FULL_LOCAL_RECIPROCITY'],
 13:['HLM_ORIGINAL_H_PRIME'],14:['HLM_ORIGINAL_H_PRIME'],
 21:['HLM_FULL_LOCAL_RECIPROCITY'],23:['HLM_FULL_LOCAL_RECIPROCITY'],
 24:[x['id'] for x in foundations],26:[x['id'] for x in foundations]}
tex = (HERE/'main.tex').read_text()
assert not any(ord(c)<32 and c not in '\n\t' for c in tex), 'ASCII control character in proof'
main_hash = sha(tex.encode())
claims = []
for number,(deps,groups) in relations.items():
    cid = f'HLM{number}'
    m = re.search(r'^% BEGIN '+cid+r'\n.*?^% END '+cid+r'\n',tex,re.M|re.S)
    assert m,cid
    block = m.group()
    title = re.search(r'\\paragraph\{'+cid+r'\. (.*?)\}\n',block,re.S).group(1)
    lo = tex[:m.start()].count('\n')+1
    retained = []
    if number in [5,7,13,14]:
        retained.append('Generic H.Ax/IsWt and supplied AutomorphicHeckeSet or all-level IsJ remain hypotheses exactly where stated; HLM24 installs them on the actual unitary data.')
    if number in [15,16,20,21,22,24,26]:
        retained.append('The original h and its absolute-quotient compatibility, same theta/type/residual data, and exact V.S prime conditions are retained.')
    if number in [9,23,24,25,26]:
        retained.append('Both original IsJ branches, including J=top for the zero old module; no same-ideal enlargement.')
    claims.append({'id':cid,'title':title,'introduced_in':'0.45','classification':'B',
      'status':'complete written proof at its stated original scope',
      'depends_on':[f'HLM{x}' if isinstance(x,int) else x for x in deps],
      'external_input_ids':external_for.get(number,[]),
      'scope':'shared RH and unrestricted Dirichlet GRH; original all-level ordinary module and fixed ideal',
      'proof_location':{'file':'hida_level_modules_v45/main.tex','label':'claim:'+cid,
         'line_start':lo,'line_end':lo+block.count('\n')-1,'sha256':sha(block.encode()),'bytes':len(block.encode())},
      'source_groups':groups,'sources':[sources[k] for k in groups],
      'retained_hypotheses':retained,
      'dependency_scope':'Only numbered written human claims occur in depends_on; external foundations are named separately. Formal correctness is not substituted for a written proof.'})

component_for = {'OST':'ordinary_structure_v42','OHA':'ordinary_hecke_algebra_v42',
 'ASP':'arithmetic_specialization_v42','AFS':'arithmetic_fibers_v43','FNL':'finite_levels_v42',
 'UPA':'automorphic_installation_v44','HEP':'hecke_eigenpoints_v44','JRP':'ring_properties_v44',
 'JSP':'joint_support','KX':'symplectic_universal_arithmetic','NTL':'neat_levels',
 'LTP':'local_transport_v44','CFD':'classical_parts_v43'}
inherited = []
for cid in sorted({d for ds,_ in relations.values() for d in ds if isinstance(d,str)}):
    component = component_for[re.match('[A-Z]+',cid).group()]
    path = ROOT/component/'main.tex'
    t = path.read_text()
    m = re.search(r'^% BEGIN '+cid+r'\n.*?^% END '+cid+r'\n',t,re.M|re.S)
    assert m,cid
    inherited.append({'claim':cid,'file':component+'/main.tex','file_sha256':sha(path.read_bytes()),
       'claim_sha256':sha(m.group().encode()),'line_start':t[:m.start()].count('\n')+1,
       'line_end':t[:m.end()].count('\n'),'kind':'immutable_inherited_human_proof',
       'newly_modified':False,'scope':'Only the printed scope and its retained foundations are used.'})

completed = [
 {'endpoint':'UpperTheory.V.Hi.ordProj','claim':'HLM3','scope':'All original finite/neat continuous-weight hypotheses; actual quotient action, projectivity, norm image and kernel, without group-order division.'},
 {'endpoint':'UpperTheory.V.Hi.piBasic','claim':'HLM5','scope':'Actual directed union, original right action, all compact fixed modules and all normal finite quotient actions, with the original neatness/faithfulness premises.'},
 {'endpoint':'UpperTheory.V.Hi.coreDet_alt','claim':'HLM7','scope':'Full IsUniv on the original nonzero CO Hecke algebra, including abstract rank zero; supplied original Ax, IsWt, automorphic parts and dense admitted weight.'},
 {'endpoint':'UpperTheory.V.Hi.core_unique_of_axioms_weight_char','claim':'HLM8','scope':'Equality of full determinant laws and every local character; integral coefficient argument.'},
 {'endpoint':'UpperTheory.V.Hi.exists_hecke_ideal','claim':'HLM9','scope':'Every original actual unitary level and rank n>=1 under original H prime, both zero/nonzero branches, actual surjective map and full IsJ.'},
 {'endpoint':'UpperTheory.V.Hi.levelUR2ActEx_alt','claim':'HLM10','scope':'One universal-ring action on the actual union, with original generic all-level IsJ premise and unique-map premise.'},
 {'endpoint':'UpperTheory.V.Hi.piPts_n_alt','claim':'HLM13','scope':'Every nonzero module vector, full polynomial determinant equality, fixed iota, all auxiliary factors, every prolongation and every IsRecT.'},
 {'endpoint':'UpperTheory.V.Hi.LvW.umodAbs_alt','claim':'HLM14','scope':'Complete generic directed union/action/finiteness/projectivity/map/vector-separation interface at the printed original hypotheses.'},
 {'endpoint':'UpperTheory.V.Hi.LvR.type_for_r_up_of_type_for','claim':'HLM16','scope':'Same integral type, every original Teichmuller family, every IsRecT; residual characters are pulled back through the actual p0.'},
 {'endpoint':'UpperTheory.V.Hi.levelUR2Faith','claim':'HLM17','scope':'Every original section-product homomorphism, every compact auxiliary level, including empty product.'},
 {'endpoint':'UpperTheory.V.Hi.levelUR2LevEq','claim':'HLM17','scope':'Literal subgroup equality when V0.S prime=s.S and all new selected factors are maximal compact.'},
 {'endpoint':'UpperTheory.V.Hi.levelUR2OrdPt_alt','claim':'HLM18','scope':'Every ordinary Hecke character over a supplied admitted arithmetic point occurs in an original part, before imposing residual block conditions.'},
 {'endpoint':'UpperTheory.V.Hi.levelUR2H3Abs_alt','claim':'HLM19','scope':'All retained ordinary indices and dense retained Frobenius images imply equality of full and selected residual parts; no specialization-flatness assumption.'},
 {'endpoint':'UpperTheory.V.Hi.LvW.step2_alt','claim':'HLM20','scope':'Actual operator identity and literal equality of original function modules, with exact theta and a composed with opUp.'},
 {'endpoint':'UpperTheory.V.Hi.levelUR2BaseEq_alt','claim':'HLM21','scope':'Exact determinant comap through p0 and equality of the unchanged local characters under the Hecke algebra map.'},
 {'endpoint':'UpperTheory.V.Hi.levelUR2SmulKey_alt','claim':'HLM22','scope':'Exact beta-equivariance on the same original old/new maximal-compact module, including zero module.'},
 {'endpoint':'UpperTheory.V.Hi.levelUR2WtVars and levelUR2BasePack','claim':'HLM23','scope':'Arbitrary original n>=1, D=n[L+:Q], Empty base variables, exact coordinate equations, annihilator=the same J.'},
 {'endpoint':'UpperTheory.V.Hi.LvW.step1_alt and BaseObjectHomExt.s3','claim':'HLM24','scope':'Actual all-level IsJ, same theta/type/residual data, auxiliary universal ring from actual Pair witness, and complete raw module package.'},
 {'endpoint':'UpperTheory.V.Hi.levelUR2ModPack_alt','claim':'HLM25','scope':'Every LevMod instance and non-instance field, exact Iwahori quotient action and full ClassicalAlt.'},
 {'endpoint':'UpperTheory.V.Hi.level_of_isJ_unitaryHeckeData','claim':'HLM26','scope':'Whole literal LevelAlt for n>=1, one base chosen before every V/h/q/v/w/Bq, q=0 included, original prime 3 and fixed iota.'},
]
boundaries = [
 'This packet proves LevelAlt and its actual suppliers. TWAut/HasAut is a separate consumer, not inferred from LevelAlt alone.',
 'The original HypothesesH prime, local Artin/LocCFT, automorphic/type/correspondence and cohomological foundations remain explicit inherited inputs.',
 'No new proof of continuous determinant representability, classical local correspondence or the trace-formula foundations is asserted.',
 'The literal final LevelAlt producer assumes n>=1; the abstract HasAutOfAlt statement with arbitrary n belongs to the separate consumer.',
 'No separate nonempty_unitary_hecke_parts ordinary-return vector producer is claimed by this file; NonemptyUnitaryHeckeParts in the mapped DenseThresholdCases path is the module-packing endpoint.',
 'No whole selected RH/GRH obligation is closed by this component alone; the old ideal J is never changed.'
]
non_premises = [
 {'claim':'HLM9','reference':'JSP3-JSP5','reason':'Comparison with the earlier rank-four application; the all-rank proof is supplied anew in HLM9.'},
 {'claim':'HLM23','reference':'JSP8','reason':'Identification of the earlier rank-four construction; HLM23 proves the all-rank construction directly from KX3-KX5 and the actual IsJ.'},
 {'claim':'HLM14','reference':'HLM24','reason':'Forward pointer identifying the later actual installation, not a premise of the generic theorem.'},
]
contract = {'schema':'rh-hida-level-modules-contract/1','artifact_version':'0.45','component':'hida_level_modules_v45',
 'source_commit':PIN,'proof_file_sha256':main_hash,'claim_count':26,'claims':'HLM1-HLM26',
 'completed_source_endpoints':completed,
 'main_endpoint':'UpperTheory.V.Hi.level_of_isJ_unitaryHeckeData',
 'original_data':'Same ell,L,Omega,s,n>=1,V0,Q0,c,r,iota,B,Lambda,UnitaryHeckeData,K0,J; V0.S prime=s.S.',
 'choice_order':'One b:TWBase(pairOf B.u,J,Empty,n[L+:Q]) is fixed before all V,h,q,v,w,Bq and their premises.',
 'auxiliary_scope':'Every original auxiliary level and quotient-compatible h; q may be zero; v injective outside s.S; V.S prime=s.S union range(v); every stated place-over and decomposition-group condition retained.',
 'coefficient_scope':'Original CO rings, including non-domains in generic ordinary/action/interpolation statements; the actual universal weight ring is the given A. No flatness of a field specialization or arbitrary coefficient map is assumed.',
 'module_identity':'Actual union of original MK submodules of one original function space; K-fixed module literally MK; maximal-compact module literally the original old MK.',
 'action_identity':'One R action agrees with every actual finite-level IsMap. Right translations retain source order rho(g)rho(h)=rho(gh), and commute with the R action.',
 'projectivity':'Integral Higman splitting using neat fundamental selector and the original ordinary projector; every normal compact-level quotient, without dividing by its order.',
 'determinant_scope':'Integral group-word polynomial interpolation gives full determinant laws on every scalar algebra, not just characteristic polynomials or pointwise traces; all-rank and small-prime compatible.',
 'type_and_local_scope':'Same tau0 and theta, a prime=a composed with opUp, every Teichmuller family, every prolongation and every IsRecT in every module-vector point.',
 'zero_scope':'Both IsJ branches retained. J=top gives a zero base; no assertion that every nonempty auxiliary union is then zero. q=0 is handled by the empty product.',
 'prime_rank_scope':['original prime 3','all original primes','every n>=1 for literal final producer','rank zero separately for abstract coreDet','empty auxiliary set','no ell>n condition','no inversion of n!'],
 'inherited_foundations':foundations,'non_premise_references':non_premises,'not_supplied':boundaries}

reviews = []
reviewed_claims = set()
for path in sorted(HERE.glob('review_*.json')):
    r = json.loads(path.read_text())
    bound = r.get('proof_file_sha256',r.get('proof_sha256',r.get('main_tex_sha256',r.get('main_sha256'))))
    if bound != main_hash:
        continue
    expected = {c['id']:c['proof_location']['sha256'] for c in claims}
    assert all(expected.get(k)==v for k,v in r.get('proof_hashes',{}).items()),path
    entries = r.get('claims_reviewed',r.get('reviewed_claims',list(r.get('proof_hashes',{}))))
    ids = [e if isinstance(e,str) else e.get('id',e.get('claim')) for e in entries]
    assert set(ids) <= set(expected), (path,ids)
    reviewed_claims.update(ids)
    reviews.append({'file':str(path.relative_to(ROOT)),'sha256':sha(path.read_bytes()),'claims':ids,'record':r})
status = 'complete_at_stated_scope_independently_reviewed' if {c['id'] for c in claims} <= reviewed_claims else 'complete_written_proof_pending_independent_review'
for claim in claims:
    claim['status'] = 'complete_at_stated_scope_independently_reviewed' if claim['id'] in reviewed_claims else 'complete_written_proof_pending_independent_review'
provenance = {'schema':'rh-human-component-provenance/1','artifact_version':'0.45','date':'2026-11-23',
 'component':'hida_level_modules_v45','source_commit':PIN,'status':status,
 'main_tex_sha256':main_hash,'proof_file_sha256':main_hash,'claims':claims,
 'source_groups':sources,'source_files':list(source_files.values()),'inherited_human_inputs':inherited,
 'classical_and_foundational_inputs':foundations,'inherited_foundation_retention':foundations,
 'independent_reviews':reviews,'non_premise_references':non_premises,
 'dependency_convention':'depends_on contains only numbered written human claims. Foundations and supplied interfaces are separate records, never fake DAG nodes.',
 'source_proof_is_not_human_proof':True,'root_ledger_modified':False,'frozen_v44_modified':False}
closure = {'schema':'rh-human-component-closure/1','artifact_version':'0.45','component':'hida_level_modules_v45',
 'proof_file_sha256':main_hash,'status':status,'completed_source_endpoints':completed,
 'whole_obligations_closed':[],'remaining':boundaries,'foundation_retention_explicit':True,
 'one_base_before_all_levels':True,'same_J':True,'q_zero_included':True,
 'all_module_vectors_separated':True,'every_IsRecT_and_IsTeich_retained':True,
 'validation':'Exact source and written proof matching; standalone draft TeX. No Lean replay or PDF visual certification.',
 'independent_reviews':reviews,'pending_independent_review':sorted({c['id'] for c in claims}-reviewed_claims)}
manifest = {'schema':'rh-source-manifest/1','artifact_version':'0.45','source_commit':PIN,
 'files':list(source_files.values()),'ranges':list(sources.values()),'all_files_equal_pinned_git_blobs':True,
 'file_count':len(source_files),'range_count':len(sources)}
for name,data in [('provenance.json',provenance),('source_manifest.json',manifest),
                  ('contract.json',contract),('original_contracts.json',contract),
                  ('closure.json',closure),('retained_foundations.json',foundations)]:
    (HERE/name).write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n')
summary = [
 'ACTUAL ALL-LEVEL ORDINARY MODULE FAMILY — v0.45',
 'Source pin: '+PIN,'Proof SHA256: '+main_hash,
 f'Written claims: 26. Pinned source files: {len(source_files)}. Exact source ranges: {len(sources)}.',
 'Status: '+status,'',
 'Completed:',
 '  HLM3 full ordProj; HLM5 actual smooth union and every compact fixed module;',
 '  HLM6 integral full-law interpolation; HLM7 actual coreDet including abstract n=0;',
 '  HLM8 uniqueness/action compatibility; HLM9 actual IsJ at every unitary level;',
 '  HLM10 one universal action; HLM13 full vector separation; HLM14 complete umodAbs;',
 '  HLM15-17 original residual/type/level/section transport;',
 '  HLM18-20 every ordinary eigencharacter, dense retained-Frobenius comparison, literal old module;',
 '  HLM21-22 exact pair/action comparison through beta;',
 '  HLM23 one same-J Taylor-Wiles base chosen first, with D=n[L+:Q];',
 '  HLM24 actual auxiliary ring and all hypotheses supplied; HLM25 every LevMod field;',
 '  HLM26 full original LevelAlt, all original n>=1/primes, q=0, fixed iota and every IsRecT.',
 '',
 'Key safeguards:',
 '  No Out record is used before its IsUniv pair exists. Integral determinant identities',
 '  use finite-degree truncated scalar algebras, not infinite-support group elements.',
 '  Projectivity is integral; the faithful-fiber argument uses a positive-rank free',
 '  direct summand before specializing, not an assumed flat or faithful base change.',
 '  Same theta, tau0, residual data and ideal J; every Teichmuller family descends',
 '  through the actual quotient by residue/root uniqueness.',
 '',
 'Remaining boundaries:'] + ['  '+x for x in boundaries] + [
 '',
 'The metadata builder compares every source file to git show at the exact pin,',
 'hashes source ranges and numbered human blocks, and binds inherited proof blocks.',
 'No common ledger, old proof bytes, historical file or formal source was edited.']
(HERE/'report.txt').write_text('\n'.join(summary)+'\n')
print(json.dumps({'component':'hida_level_modules_v45','claims':len(claims),'source_files':len(source_files),
 'source_ranges':len(sources),'proof_sha256':main_hash,'status':status}))
