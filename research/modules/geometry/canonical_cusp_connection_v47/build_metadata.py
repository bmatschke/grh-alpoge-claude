#!/usr/bin/env python3
"""Rebuild only the CNC component's exact proof/source bindings; no Lean replay."""
from pathlib import Path
import argparse
import hashlib
import json
import re
import subprocess

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
PIN = '7cbf7a0c32fca1badf05931879a37c3f8a2b03b4'
VERSION = '0.47'
COMPONENT = HERE.name
parser = argparse.ArgumentParser()
parser.add_argument('--repo', type=Path, required=True)
repo = parser.parse_args().repo.resolve()
sha = lambda data: hashlib.sha256(data).hexdigest()
assert subprocess.check_output(['git', '-C', str(repo), 'rev-parse', 'HEAD'], text=True).strip() == PIN

A = 'src/Development/AbelianVarietyTheory/'
P = A + 'Proofs/'
C = P + 'CuspFormEvaluations/'
G = P + 'FormalGroupCharts/'
F = 'src/Formalism/LocalToGlobal/ProjectiveLattices/'
J = 'src/Formalism/SharpRestriction/Divisibility/GeneratorPowers/'
T = 'src/ReciprocityTheory/ReductiveGroups/ArithmeticGeometry/BirationalGeometry/ToroidalCompactification/'
E = 'src/ReciprocityTheory/ReductiveGroups/ArithmeticGeometry/ExtensionDescent/'
Y = 'src/ReciprocityTheory/ReductiveGroups/ArithmeticGeometry/TaylorDiscriminants/'

specs = {
    'abelian_scheme_definition': (A + 'BlockTheory/AbelianSchemeLaw/SemiAbelianSchemes.lean', 1, 43, 'Original IsAbelianScheme and semiabelian geometric fields'),
    'host_and_SAB': (T + 'TwoWeightEqOneAddRoot.lean', 14, 84, 'Original host involution, w0, datum, level and all SAB line data'),
    'proper_original_object': (T + 'TwoWeightEqOneAddRoot.lean', 144, 162, 'Original Obj properness and actual universal object'),
    'moduli_and_coefficient_field': (T + 'PushInvertible.lean', 29, 46, 'Literal Moduli and Coeff with every conjugate inside c.F'),
    'actual_abelian_family': (P + 'ModuliProofs/ObjIsAbelianSchemeDimRigidifiedSym.lean', 232, 239, 'Original ObjDim.isAbelianScheme, rigidified and symmetric line'),
    'universal_polarized_object': (C + 'IsLocallyNoetherian.lean', 21, None, 'Original universal polarized abelian object; reducedness of X is not imposed on S'),
    'global_functions_contract': (E + 'GlobalSectionsRankAlgClosed.lean', 150, 153, 'Literal GlobalFnsSt for arbitrary schemes'),
    'global_functions_producer': (P + 'AbelianSchemeLawProofs/GlobalFnsHolds.lean', 19, 22, 'Original globalFns_holds endpoint replaced by the matched classical foundation'),
    'framed_point': (F + 'IsCombAt.lean', 67, 77, 'Original FrPt full tangent eigenbasis and section generator'),
    'tangent_decomposition': (C + 'GlobalBasisAlgebra.lean', 22, 184, 'Exact global eigenbasis algebra over arbitrary coefficient ring'),
    'framed_tangent_basis': (C + 'GlobalBasisAlgebra.lean', 512, None, 'Original frame_tangent_basis on every FrPt'),
    'framed_formal_chart': (G + 'ExistsIsUnivChartOfIsLieBasis.lean', 1, None, 'Original universal formal chart with prescribed Lie basis'),
    'actual_chart_producer': (C + 'ExistsIsChartGOfBasis.lean', 1, None, 'Exact chart from the entire original tangent basis'),
    'chart_and_frame_contract': (F + 'ThGerm.lean', 43, 152, 'All IsChart and IsFrame fields, exact partial law order and adjoint direction'),
    'primitive_and_germ_contract': (F + 'ThGerm.lean', 153, 187, 'Original PrimTy, IsPrim, eL and all IsGerm truncation witnesses'),
    'ChartAt_and_IsNab': (F + 'ThGerm.lean', 189, None, 'Literal ChartAt and IsNab including every coefficient algebra and every germ'),
    'compatible_frame_generators': (C + 'ExistsFramesCubeDefectAlongChartOverRing.lean', 1, None, 'Actual nilpotent generator lifts and normalized cube-defect frame'),
    'normalized_primitive_and_adjoint': (J + 'GermBPrim.lean', 130, None, 'Actual global wP and wL from original SAB.prim and SAB.adj'),
    'complete_frame_producer': (C + 'ExistsFramesOfFormalChart.lean', 23, None, 'Original exists_frames_of_chart over every S, including FrTrunc and axes'),
    'frame_ratios': (C + 'FrameBiextDictionarySecondPartialLaw.lean', 191, 257, 'Exact first/second partial, symmetry and adjoint scalar dictionaries'),
    'formal_frame_identities': (C + 'FrameBiextDictionarySecondPartialLaw.lean', 315, None, 'Actual fbId including every adjoint law'),
    'formal_FB_contract': (T + 'CocycleRightZeroThd.lean', 12, 163, 'Formal group, O action, invariant operators and every FB field'),
    'gauge_and_value_contract': (T + 'CocycleRightZeroThd.lean', 164, 197, 'Literal IsCanonGauge, hL and nabVal with original signs'),
    'formal_logarithm': (G + 'PderivSecondEvFirstPointEqZero.lean', 51, 118, 'Original logarithm from closed invariant one-forms'),
    'formal_action_linear': (G + 'FormalGroupLogEndomorphismLinear.lean', 64, None, 'Original endomorphisms become linear in logarithmic coordinates'),
    'first_cocycle_gauge': (G + 'ExistsGaugeFirstLaw.lean', 42, None, 'Source first partial cocycle gauge'),
    'regauge_contract': (G + 'GermEvRegaugedSecondLawFamily.lean', 154, 164, 'Original regauge signs for all four units'),
    'regauge_endpoint': (G + 'GermEvRegaugedSecondLawFamily.lean', 342, None, 'Exact original exists_regauge conclusion'),
    'inner_derivation': (G + 'DerivationInnerOfSeparabilityElement.lean', 10, None, 'Exact separability inner derivation for reduced finite orders'),
    'adjoint_gauge': (G + 'ExistsActionGauge.lean', 241, None, 'Source logarithmic bilinear adjoint cocycle and simultaneous gauge'),
    'symmetry_gauge': (G + 'ExistsGaugeOfSymmetry.lean', 30, None, 'Exact antisymmetric half correction'),
    'full_gauge_contract': (Y + 'ConnectionKillsSeries.lean', 63, 67, 'Full original CanonGaugeSt including arbitrary source ring and rational coefficient algebra'),
    'gauge_assembly': (G + 'CanonGaugeOfLog.lean', 21, None, 'Source four-step canonical-gauge assembly'),
    'full_gauge_endpoint': (G + 'CanonGaugeExists.lean', 1, None, 'Literal canonGauge_exists endpoint'),
    'germ_producer': (J + 'GermDPf.lean', 111, None, 'Compatible eL jets and all-section germ producer'),
    'germ_uniqueness': (J + 'GermFunPf.lean', 195, None, 'Exact isGermFun_holds uniqueness by every truncation'),
    'complete_chart_endpoint': (C + 'ExistsBiextensionChartWithGermsFramedPoint.lean', 26, None, 'Actual ChartAt with compatible frames and all section germs'),
    'NabV_definition': (F + 'IsThRule.lean', 20, 28, 'Original all-integer NabV on every coefficient algebra'),
    'IsNab_endpoint': (C + 'ExistsIsNab.lean', 19, None, 'Original exists_isNab construction, negative integers zero and every-germ equality'),
    'unconditional_IsNab_endpoint': (G + 'ExistsIsNabUncond.lean', 19, None, 'Literal exists_isNab_uncond for every original moduli object'),
    'lattice_route_source': (P + 'DivisorProofs/BddMemSpanShortGen.lean', 1, None, 'Original spanning route requiring same connection, geometric charts and short-rule inputs'),
    'literal_lattice_endpoints': (P + 'DivisorProofs/IntegralCuspFormsFullLattice.lean', 11, None, 'Actual all-row LatFull and both Boolean MLat endpoints; no whole closure inferred'),
}

relations = {
    1: ([], ['abelian_scheme_definition','host_and_SAB','proper_original_object','actual_abelian_family','global_functions_contract','global_functions_producer']),
    2: ([], ['host_and_SAB','moduli_and_coefficient_field','framed_point','tangent_decomposition','framed_tangent_basis']),
    3: ([1,2], ['framed_formal_chart','actual_chart_producer','chart_and_frame_contract']),
    4: ([1], ['host_and_SAB','normalized_primitive_and_adjoint','primitive_and_germ_contract']),
    5: ([3,4], ['compatible_frame_generators','complete_frame_producer','frame_ratios','chart_and_frame_contract']),
    6: ([1,3,4,5], ['formal_frame_identities','frame_ratios','formal_FB_contract']),
    7: ([], ['formal_FB_contract','formal_logarithm','formal_action_linear']),
    8: ([], ['first_cocycle_gauge','gauge_assembly']),
    9: ([], ['formal_FB_contract','regauge_contract','regauge_endpoint']),
    10: ([7,8,9], ['first_cocycle_gauge','gauge_assembly','gauge_and_value_contract']),
    11: ([7,9,10], ['inner_derivation','adjoint_gauge','full_gauge_contract']),
    12: ([6,7,9,10,11], ['symmetry_gauge','gauge_assembly','full_gauge_contract','full_gauge_endpoint','gauge_and_value_contract']),
    13: ([3,4,5], ['primitive_and_germ_contract','germ_producer','germ_uniqueness']),
    14: ([2,3,4,5,6,12,13], ['ChartAt_and_IsNab','complete_chart_endpoint']),
    15: ([7,13,14], ['NabV_definition','gauge_and_value_contract','ChartAt_and_IsNab','IsNab_endpoint','unconditional_IsNab_endpoint']),
    16: ([15,'ICL11','ICL19','ICL20','ICL21'], ['lattice_route_source','literal_lattice_endpoints']),
}

foundations = [
    {
        'id':'CNC_ORIGINAL_MODULI_DATA',
        'kind':'original_quantified_input_data',
        'name':'The original supplied Host, Datum, Level, Moduli and Coeff records',
        'not_reconstructed':True, 'not_a_DAG_claim':True,
        'statement':'The exact theorem quantifies over original E,H,Dw,l,Xo,c. Xo.univ.t already includes its group, smooth geometrically connected semiabelian family, action, rigidified cubical line, adjoint identifications and primitive L=B_L(id,w0) identification; Xo.univ includes properness. The theorem does not construct a common Moduli family.',
        'application_checked':'CNC1 checks the abelian-scheme hypotheses from the original fields. CNC4 normalizes the actual prim/adj line isomorphisms rather than asserting them for an arbitrary symmetric line.',
        'source_groups':['host_and_SAB','proper_original_object','moduli_and_coefficient_field','actual_abelian_family'],
    },
    {
        'id':'CNC_PROPER_BASE_FUNCTIONS',
        'kind':'named_published_foundation',
        'name':'Universal base functions for proper flat connected reduced families',
        'not_reconstructed':True, 'not_a_DAG_claim':True,
        'statement':'If f is proper, flat and of finite presentation and all its geometric fibres are reduced and connected, then O_S -> f_*O_X is an isomorphism after every base change.',
        'application_checked':'CNC1 verifies these hypotheses for the original universal abelian scheme and all its finite powers, including after nonreduced/nonflat base change. Its normalized line-isomorphism consequence is a written human deduction, not a new retained theorem.',
        'references':[{'author':'The Stacks Project Authors','title':'The Stacks Project','location':'Lemma 36.32.6, tag 0E0L','url':'https://stacks.math.columbia.edu/tag/0E0L','checked_online':True}],
        'source_groups':['global_functions_contract','global_functions_producer'],
    },
    {
        'id':'CNC_SMOOTH_SECTION_COORDINATES',
        'kind':'named_published_foundation',
        'name':'Formal coordinates at a section of a smooth morphism',
        'not_reconstructed':True, 'not_a_DAG_claim':True,
        'statement':'A smooth morphism with section has locally a power-series completion along that section, with finite locally free conormal and symmetric conormal associated graded algebra. Nilpotent thickenings of affine schemes are affine.',
        'application_checked':'CNC3 uses the actual entire free tangent basis from CNC2, then proves the global affine compatible-coordinate construction using successive lifts and associated graded isomorphisms. No local/reduced/Noetherian hypothesis on the coefficient algebra is introduced.',
        'references':[{'author':'The Stacks Project Authors','title':'The Stacks Project','location':'Lemma 29.35.20, tag 05D9, and its smooth-section algebra proof','url':'https://stacks.math.columbia.edu/tag/05D9','checked_online':True}],
        'source_groups':['framed_formal_chart','actual_chart_producer'],
    },
    {
        'id':'CNC_REMAINING_ICL_SPANNING_PRODUCERS',
        'kind':'retained_original_unreconstructed_producer_bundle',
        'name':'The five remaining original geometric/integral spanning producer groups',
        'not_reconstructed':True, 'not_a_DAG_claim':True,
        'statement':'For the exact conditional CNC16 consumer retain ICL principal charts and metric, the actual finite theta IsSystem, raw Gaussian identity/integrability/reproducer, the global short-rule gluing and lower-row/reading dictionary, and the all-place ramified jet and short-value bounds, at every original required row and weight. The IsNab member of the old six-premise bundle alone is supplied by CNC15.',
        'inherited_external_input_ids':['ICL_PRINCIPAL_CHART_INPUT','ICL_LEVEL_SYSTEM_INPUT','ICL_RAW_GAUSSIAN_INPUT','ICL_SHORT_DICTIONARY_INPUT','ICL_RAMIFIED_JET_INPUT'],
        'application_checked':'CNC16 is solely the application of the universally quantified CNC15 to the unchanged conditional ICL11/19/20/21. No common-family or full LatFull producer is inferred.',
        'source_groups':['lattice_route_source','literal_lattice_endpoints'],
    },
]
external = {
    1:['CNC_ORIGINAL_MODULI_DATA','CNC_PROPER_BASE_FUNCTIONS'],
    2:['CNC_ORIGINAL_MODULI_DATA'],
    3:['CNC_SMOOTH_SECTION_COORDINATES'],
    4:['CNC_ORIGINAL_MODULI_DATA'],
    16:['CNC_REMAINING_ICL_SPANNING_PRODUCERS'],
}
scope = {
    1:'Original universal abelian scheme, every finite product and every base change, including nonreduced bases; proper normalized line-isomorphism uniqueness.',
    2:'Entire original framed tangent module over every c.F-algebra, via all CM embeddings; no ramified integral eigenspace splitting is claimed.',
    3:'One global compatible formal chart over each arbitrary coefficient algebra with exactly the given tangent frame and all six IsChart fields.',
    4:'Nilpotent lifting over arbitrary rings and normalization of the original global SAB.prim/SAB.adj data; no generic false primitive identity.',
    5:'Compatible actual cube-defect generators, both axes, and exact first/second partial, symmetry and adjoint ratios.',
    6:'Every original formal FB equation, proved from actual cube/normalized adjoint diagrams using universal base functions.',
    7:'Formal logarithm and endomorphism linearization over every commutative Q-algebra, nonreduced allowed.',
    8:'Coefficientwise primitive of a symmetric normalized additive two-cocycle, with all formal parameter variables.',
    9:'Original gauge signs; direct preservation of every FB field and addition of successive gauges.',
    10:'Two partial cocycles killed while preserving previous equations, no field or analytic assumption.',
    11:'One simultaneous adjoint gauge for every element of every reduced finite free Z-order, using its rational separability element.',
    12:'Literal full CanonGaugeSt: arbitrary source ring, dimension, reduced finite free order, and arbitrary rational coefficient algebra over the source.',
    13:'Actual eL based on original w0 and line; unique germ of every nonnegative tensor-power section by all jets, over arbitrary coefficients.',
    14:'All ChartAt data/proof fields plus compatible frames and all section germs, on each original framed point.',
    15:'Full exists_isNab_uncond on every original E/H/Dw/l/Xo/c, same star involution and nabVal; every algebra/section/multi-index/germ, negative NabV degrees set to zero.',
    16:'Only the original IsNab premise of ICL11/19/20/21 is discharged; all five remaining producer groups and common-family choice boundaries are retained.',
}

files, sources, excerpts = {}, {}, []
for key, (rel, lo, hi, title) in specs.items():
    data = (repo / rel).read_bytes()
    assert data == subprocess.check_output(['git','-C',str(repo),'show',PIN+':'+rel]), rel
    lines = data.splitlines(keepends=True)
    hi = hi or len(lines)
    assert 1 <= lo <= hi <= len(lines), (key,lo,hi,len(lines))
    block = b''.join(lines[lo-1:hi])
    url = f'https://github.com/CocoSgt/riemann-hypothesis-lean/blob/{PIN}/{rel}'
    files[rel] = {'path':rel,'sha256':sha(data),'bytes':len(data),'line_count':len(lines),'verified_equal_to_pinned_git_blob':True,'url':url}
    sources[key] = {'id':'CNC_SRC_'+key.upper(),'path':rel,'declaration':title,'line_start':lo,'line_end':hi,'source_commit':PIN,'file_sha256':sha(data),'full_file_sha256':sha(data),'range_sha256':sha(block),'range_bytes':len(block),'verified_equal_to_pinned_git_blob':True,'url':url+f'#L{lo}-L{hi}'}
    excerpts.append(f'[{sources[key]["id"]}] {title}\n{sources[key]["url"]}\n'+block.decode())

text = (HERE/'main.tex').read_text()
assert not any(ord(c)<32 and c not in '\n\t' for c in text)
main_sha = sha(text.encode())
claims = []
foundation_ids = {f['id'] for f in foundations}
for i, (deps, groups) in relations.items():
    cid = f'CNC{i}'
    match = re.search(r'^% BEGIN '+cid+r'\n.*?^% END '+cid+r'\n',text,re.M|re.S)
    assert match, cid
    assert r'\label{claim:'+cid+'}' in match.group(), cid
    ds = [f'CNC{x}' if isinstance(x,int) else x for x in deps]
    assert all(not d.startswith('CNC') or int(d[3:])<i for d in ds)
    assert set(external.get(i,[])) <= foundation_ids
    start = text[:match.start()].count('\n')+1
    claims.append({'id':cid,'title':re.search(r'\\paragraph\{'+cid+r'\. (.*?)\}\n',match.group(),re.S).group(1),'introduced_in':VERSION,'classification':'B','depends_on':ds,'external_input_ids':external.get(i,[]),'scope_note':scope[i],'source_groups':groups,'sources':[sources[k] for k in groups],'proof_location':{'file':COMPONENT+'/main.tex','label':'claim:'+cid,'line_start':start,'line_end':start+match.group().count('\n')-1,'sha256':sha(match.group().encode()),'bytes':len(match.group().encode())},'source_proof_is_not_human_proof':True})

inherited = []
for cid in ['ICL11','ICL19','ICL20','ICL21']:
    p = ROOT/'integral_cusp_lattices_v46/main.tex'
    body = p.read_text()
    match = re.search(r'^% BEGIN '+cid+r'\n.*?^% END '+cid+r'\n',body,re.M|re.S)
    assert match, cid
    inherited.append({'claim':cid,'file':'integral_cusp_lattices_v46/main.tex','file_sha256':sha(p.read_bytes()),'claim_sha256':sha(match.group().encode()),'line_start':body[:match.start()].count('\n')+1,'line_end':body[:match.end()].count('\n'),'kind':'immutable_inherited_human_proof','newly_modified_by_this_component':False})

reviews, reviewed = [], set()
lookup = {c['id']:c['proof_location']['sha256'] for c in claims}
for p in sorted(HERE.glob('review_*.json')):
    review = json.loads(p.read_text())
    assert review.get('status',review.get('result')) == 'PASS', p
    entries = review.get('claims_reviewed',review.get('reviewed_claims',[]))
    ids, stale = [], False
    for entry in entries:
        cid = entry if isinstance(entry,str) else entry.get('id',entry.get('claim'))
        expected = review.get('proof_hashes',{}).get(cid) if isinstance(entry,str) else entry.get('proof_range_sha256',entry.get('block_sha256'))
        assert cid in lookup, (p,cid)
        stale = stale or expected != lookup[cid]
        ids.append(cid)
    if stale:
        continue
    reviewed.update(ids)
    reviews.append({'file':str(p.relative_to(ROOT)),'sha256':sha(p.read_bytes()),'reviewer':review.get('reviewer'),'result':'PASS','reviewed_proof_file_sha256':review.get('proof_file_sha256',review.get('proof_sha256')),'proof_file_sha256':main_sha,'reviewed_blocks_unchanged':True,'claims':ids})
status = 'complete_at_stated_scope_independently_reviewed' if set(lookup)<=reviewed else 'complete_at_stated_scope_pending_independent_review'
for claim in claims:
    claim['status'] = 'complete_at_stated_scope_independently_reviewed' if claim['id'] in reviewed else 'complete_at_stated_scope_pending_independent_review'
    claim['independent_review_files'] = [r['file'] for r in reviews if claim['id'] in r['claims']]

completed = [
    {'endpoint':'GlobalTheory.canonGauge_exists / CanonGaugeSt','claim':'CNC12','status':'whole_literal_generic_producer_written','scope':'Every original R,d,O,k,B with O reduced finite free over Z and k an arbitrary Q-algebra and R-algebra. Both partial, all adjoint and symmetry gauges are proved.'},
    {'endpoint':'GlobalTheory.ChartRing.exists_chartAt_with_germs on the original moduli object','claim':'CNC14','status':'whole_literal_conclusion_supplied_under_two_named_classical_foundations','scope':'Every S and original framed point, all ChartAt fields, compatible frames and every section germ. The large source Laws package is not retained as an extra premise.'},
    {'endpoint':'GlobalTheory.CanonConn.exists_isNab_uncond','claim':'CNC15','status':'whole_literal_source_endpoint_supplied_under_two_named_classical_foundations','scope':'Every original E,H,Dw,l,Xo,c; all c.F coefficient algebras and every natural degree/section/germ/multi-index. Same original nabVal and w0.'},
    {'endpoint':'ICL connection-existence producer premise','claim':'CNC16','status':'one_original_producer_discharged','scope':'Applied to the unchanged original row family and both Boolean levels. Five other spanning producer groups remain.'},
]
boundaries = [
    'The original Host/Datum/Level/Moduli/Coeff objects are quantified inputs. No common-family construction or simultaneous Hermitian/metric/measure/phase choice is inferred.',
    'Two named published geometric foundations are retained separately: smooth-section formal coordinates and universal base functions for proper flat geometrically reduced connected families.',
    'The actual principal same-Gram charts and metric comparison, finite theta IsSystem, raw Gaussian identity and integrability/reproducer, global short-rule gluing/reading dictionary, and ramified integral short-value estimates remain original producer boundaries.',
    'CNC15 is precisely IsNab. It does not assert unproved integral valuation bounds or additional connection theorems absent from that predicate.',
    'Higher CoversAt, all-tuple ClsEx, PointIdentCore before every tuple, ClassSumsSpan, eta agreement and stronger second DivRows3 are not supplied.',
    'No whole DESIGN_CHOICES_COMMON or BASE_THETA_RATIONAL_TESTS obligation is closed; full unconditional LatFull is not inferred.',
]
contract = {
    'schema':'rh-human-component-contract/1','artifact_version':VERSION,'component':COMPONENT,'source_commit':PIN,'proof_file_sha256':main_sha,'claims':'CNC1-CNC16','claim_count':16,
    'main_outcome':'Actual original IsNab construction over every coefficient algebra, with complete formal gauge proof and all ChartAt/germ fields; removal of precisely ICL canonical-connection premise.',
    'completed_source_endpoints':completed,
    'conditional_original_endpoints':[{'endpoint':'ICL11/ICL19/ICL20/ICL21 with the IsNab premise removed','claim':'CNC16','remaining_input_ids':['CNC_REMAINING_ICL_SPANNING_PRODUCERS'],'scope':'All original remaining hypotheses of those immutable human implications are retained.'}],
    'quantifier_order':['Fix any original E,H,Dw,l,Xo,c.','For every commutative c.F-algebra S and every original framed point y, construct one chart C.','That chart serves every natural degree k and every original section F.','Its unique germ enforces the nabVal equality for every series satisfying IsGerm, not only the chosen representative.','Choose the NabV function simultaneously on the original coefficient-algebra data; rational structure maps are unique.','Apply the universal result separately to every original row and Boolean level, leaving all other common-family producers intact.'],
    'coefficient_scope':{'arbitrary_commutative_cF_algebra':True,'nonreduced_allowed':True,'nonlocal_allowed':True,'non_Noetherian_allowed':True,'domain_assumption':False,'flatness_assumption_on_S':False,'zero_ring_allowed':True},
    'generic_gauge_scope':'Arbitrary source commutative ring R0 and commutative rational R over R0; arbitrary dimension; any reduced finite free Z-order O with involution. The separability argument takes place in O tensor Q, not in the coefficient ring.',
    'literal_signs':{'ph1':'h(x,w)+h(z,w)-h(F(x,z),w)','ph2':'h(x,z)+h(x,w)-h(x,F(z,w))','sy':'h(z,x)-h(x,z)','ad_b':'h([b]x,z)-h(x,[star b]z)','last_correction':'minus log(sy)/2','value':'constantCoeff Dpoly(f*exp(k*h(x,[w0]x)))'},
    'negative_integer_values':'NabV is defined for all integers; the source and this proof assign zero at negative integers, while literal IsNab constrains natural degrees only.',
    'foundation_classification':'All CNC labels are numbered written deductions. The two published foundations have separate external_input_ids, full statements and checked hypothesis matching, and are not counted as proved human claims.',
    'retained_input_ids':[f['id'] for f in foundations],
    'not_supplied':boundaries,'whole_obligations_closed':[],
    'non_premise_references':[{'location':'introductory and concluding scope statements','references':['principal charts','IsSystem','Gaussian estimates','higher CoversAt','ClsEx','PointIdentCore','ClassSumsSpan'],'reason':'Explicitly retained or later-consumer boundaries, not outputs or hidden premises of the IsNab proof.'}],
}
manifest = {'schema':'rh-source-manifest/1','artifact_version':VERSION,'component':COMPONENT,'source_commit':PIN,'files':list(files.values()),'ranges':list(sources.values()),'all_files_equal_pinned_git_blobs':True,'file_count':len(files),'range_count':len(sources)}
provenance = {'schema':'rh-human-component-provenance/1','artifact_version':VERSION,'component':COMPONENT,'source_commit':PIN,'proof_file_sha256':main_sha,'main_tex_sha256':main_sha,'status':status,'claims':claims,'source_groups':sources,'inherited_human_inputs':inherited,'classical_and_foundational_inputs':foundations,'independent_reviews':reviews,'dependency_convention':'depends_on contains only numbered written human claims; original quantified records, named published foundations and retained producer boundaries use separate external_input_ids.','source_proof_is_not_human_proof':True,'root_ledger_modified':False,'frozen_artifacts_modified':False}
closure = {'schema':'rh-human-component-closure/1','artifact_version':VERSION,'component':COMPONENT,'source_commit':PIN,'proof_file_sha256':main_sha,'status':status,'completed_source_endpoints':completed,'conditional_original_endpoints':contract['conditional_original_endpoints'],'whole_obligations_closed':[],'proposed_global_frontier_leaf_closures':[],'remaining':boundaries,'foundation_retention_explicit':True,'full_literal_IsNab_supplied':True,'full_literal_CanonGaugeSt_supplied':True,'full_LatFull_unconditional_supplier_closed':False,'all_original_coefficient_algebras_retained':True,'all_original_germs_retained':True,'independent_reviews':reviews,'pending_independent_review':sorted(set(lookup)-reviewed),'validation':'Two-pass standalone draft TeX, no PDF and no Lean replay; review files are independently authored and hash-bound.'}

for name, value in [('provenance.json',provenance),('source_manifest.json',manifest),('contracts.json',contract),('original_contracts.json',contract),('closure.json',closure),('retained_foundations.json',foundations)]:
    (HERE/name).write_text(json.dumps(value,ensure_ascii=False,indent=2)+'\n')
(HERE/'source_excerpts.txt').write_text('\n\n'.join(excerpts))
report = [
    'CANONICAL CUSP CONNECTION ON THE ORIGINAL MODULI FAMILY — v0.47',
    'Source pin: '+PIN,'Proof SHA256: '+main_sha,
    f'Claims: 16; source files: {len(files)}; exact source ranges: {len(sources)}.',
    'Status: '+status,'',
    'CNC15 constructs the complete literal exists_isNab_uncond endpoint. Every original',
    'coefficient algebra is retained: nonreduced, nonlocal and non-Noetherian rings are',
    'allowed. A single chart at each original framed point serves every degree/section,',
    'and uniqueness of all compatible jets gives the equality for every valid germ.',
    '',
    'CNC1–6 construct the actual formal coordinates, normalized cube-defect generators',
    'and all original formal biextension identities. The primitive and adjoint line',
    'isomorphisms are fields of the supplied original SAB, normalized here at zero.',
    'CNC7–12 give a complete coefficientwise formal-gauge proof: logarithmic coordinates,',
    'two explicit symmetric-cocycle primitives, one separability-element correction for',
    'all adjoint units, and the final antisymmetric half correction.',
    'CNC12 retains the full generic CanonGaugeSt scope, beyond the needed O_E instance.',
    '',
    'The two separately named published foundations are smooth-section formal coordinates',
    '(Stacks05D9) and universal base functions for proper flat reduced connected families',
    '(Stacks0E0L). Their hypotheses are checked on the actual original family. They are',
    'not counted as numbered human deductions. No large source Laws package is assumed.',
    '',
    'CNC16 removes precisely the ICL canonical connection premise. Principal charts,',
    'finite theta system, raw Gaussian/reproducer estimates, short-rule gluing/dictionary',
    'and ramified integral valuation producers remain. No full LatFull, higher CoversAt,',
    'all-tuple ClsEx, PointIdentCore, ClassSumsSpan or compound common-family closure is',
    'inferred. The original fields, metrics, measures, embeddings and phases stay fixed.',
    '',
    'Rebuild: python build_metadata.py --repo /path/to/formal_source',
    'Validate: python validate_tex.py --format /path/to/pdflatex.fmt',
    'Every source file is compared with its exact pinned git blob; every range and',
    'human block is SHA256-bound. Frozen v46 proofs and root/shared files are untouched.',
]
(HERE/'report.txt').write_text('\n'.join(report)+'\n')
hashes = {p.name:sha(p.read_bytes()) for p in sorted(HERE.iterdir()) if p.is_file() and p.name!='hashes.json'}
(HERE/'hashes.json').write_text(json.dumps({'artifact_version':VERSION,'component':COMPONENT,'hashes':hashes},indent=2)+'\n')
print(json.dumps({'component':COMPONENT,'claims':len(claims),'source_files':len(files),'source_ranges':len(sources),'proof_file_sha256':main_sha,'status':status},indent=2))
