#!/usr/bin/env python3
"""Rebuild the PCL component's pinned sources and human proof bindings; no Lean replay."""
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
F = 'src/Formalism/LocalToGlobal/ProjectiveLattices/'
H = 'src/Formalism/LocalRingCardinality/'
G = 'src/ReciprocityTheory/ReductiveGroups/ArithmeticGeometry/'

specs = {
    'original_datum_and_level': (G+'BirationalGeometry/ToroidalCompactification/TwoWeightEqOneAddRoot.lean',30,59,'Original perfect alternating Datum and Level.M >= 3'),
    'hermitian_coordinates': (P+'UnitaryExistence/ExistsHermCoordOfDatum.lean',11,None,'Literal exists_herm_coord_of_datum, trace nondegeneracy and original sign'),
    'original_Hermitian_Data': (G+'FundamentalDomains/Signature.lean',12,111,'Original left-linear Hermitian form, unitary stabilizer and complete Data'),
    'original_DataX': (G+'FundamentalDomains/FundamentalDomainPointBound.lean',12,41,'EFf sign, every DataX field and exact fdeg/rdE normalization'),
    'ideal_duality': (P+'HermitianTraceForms/TraceFormDualOneTraceFormDual.lean',14,257,'Fractional-ideal conjugation, ideal-valued dual, scalar-product cancellation and lattice fullness'),
    'trace_duality': (P+'HermitianTraceForms/TraceFormDualOneTraceFormDual.lean',258,None,'Actual traceFormDual, exact different factor and equivalence with integral perfection'),
    'complete_DataX_producer': (P+'CubicalLineBundles/ExistsPosNatMemFractionalIdeal.lean',10,None,'Literal exists_dataX_of_perfect_traceForm and positive integral denominators'),
    'original_IsUnf': (F+'UnFree.lean',15,95,'Original Unf, IsUnf, and same-component integral lattice/trace dictionary'),
    'trace_perfection_on_Unf': (P+'CubicalLineBundles/TraceFormIntegralPerfectOfIsUnf.lean',9,None,'Whole original traceForm_integral_perfect_of_isUnf endpoint'),
    'host_prime_congruence': ('src/Formalism/FrobeniusOrbits/Statement.lean',13,25,'Actual d prime and d congruent 7 modulo 16'),
    'actual_host_fields': (H+'DataHost.lean',40,95,'Actual host half-different, ccK and fixed embedding fields'),
    'actual_host_definitions': (H+'DataHost.lean',145,166,'Original xi0, ccE, AA, AAbar and absolute different'),
    'host_star_identification': (H+'RankBoundMonotoneInDimension.lean',507,513,'Host conjugation equals the CM involution by its embedding law'),
    'quadratic_different': ('src/Formalism/SharpRestriction/GlobalSchurBounds/GlobalRankLatticeProofs/EqOfLeOfAbsNormEq.lean',103,225,'Exact quadratic different and actual host DiffKH producer'),
    'quadratic_norm': ('src/Formalism/SharpRestriction/GlobalSchurBounds/GlobalRankLatticeProofs/EqOfLeOfAbsNormEq.lean',249,None,'Actual norm_K and NormKH ideal identity'),
    'principal_ideal_identity': (H+'RankBoundMonotoneInDimension.lean',1311,None,'Literal DiffKPrincipal/CcNorm and exact factPrincipalDatum product'),
    'original_principal_supplier': ('src/Formalism/LocalToGlobal/IndefiniteReal/FinitePlaces/FactPrincipalDatum.lean',10,27,'Original formal FactPrincipalDatum assembly, reconstructed in PCL7-PCL8'),
    'actual_scalar_norm': (G+'PullbackSections/HolomorphicFamilies/ModelDataX.lean',12,None,'Exact xiR=1/(Norm(ccK)*sqrt(d)) and numerical bound'),
    'half_different_norm': (G+'PullbackSections/HolomorphicFamilies/ModelLatIn.lean',12,91,'Exact HalfDiffNormSt and norm-square discriminant bound'),
    'quantitative_DataX_endpoint': (P+'CubicalLineBundles/ExistsRankOneCuspLatticeDataOfPrincipal.lean',14,None,'All exact fields of exists_dataX_of_hasPrinc, original NA/NC and scalar normalization'),
    'LawsCore_fields': (F+'CuspidalL2Subspace.lean',93,None,'Actual LawsM/LawsCore: every original row, good embedding and component; unf/xiAbs retained'),
    'HasPrinc': (A+'Definitions/RegularCharts/BaseNorm.lean',31,None,'Original principal-congruence inclusion on the same Unf'),
    'core_GamAt': (A+'Definitions/ThetaValues/GamAt.lean',10,17,'Literal core GamAt quantified over every original row and good embedding'),
    'model_GamAt_and_HalfDiff': (G+'PullbackSections/ModelLat.lean',10,23,'Original top GamAt and full HalfDiffNormSt'),
    'core_DataX_model_endpoint': (P+'CubicalLineBundles/DataXOfModelOfGamAt.lean',17,None,'Whole dataXOfModel_of_gamAt endpoint'),
    'page_size_predicate': (G+'PullbackSections/SupBoundPageRows.lean',9,18,'Full SupBoundPageRows with exact fourth ccK logarithmic bound'),
    'DataXOfModelSt': (F+'ArchimedeanQuadraticData/ArcWitnessExistence/DataXOfModel.lean',13,18,'Literal all-row model endpoint including both logarithmic bounds'),
    'principal_chart_boundary': (P+'UnitaryExistence/CongrOfDvdModulus.lean',36,None,'Stronger exists_unf_hasPrinc producer, explicitly not supplied by PCL'),
    'ICL_original_chart_use': (P+'DivisorProofs/ExistsSmulNonnegOfPow.lean',87,137,'Original existence of common-Gram principal charts and DataX use; full chart supplier not inferred'),
}

relations = {
    1:([],['original_datum_and_level','hermitian_coordinates','original_Hermitian_Data']),
    2:([],['ideal_duality']),
    3:([2],['ideal_duality','trace_duality','original_DataX']),
    4:([2,3],['trace_duality','complete_DataX_producer']),
    5:([2,4],['original_DataX','complete_DataX_producer']),
    6:([],['original_IsUnf','trace_perfection_on_Unf','original_datum_and_level']),
    7:([],['host_prime_congruence','actual_host_fields','host_star_identification','quadratic_different','quadratic_norm']),
    8:([7],['actual_host_definitions','principal_ideal_identity','original_principal_supplier','actual_scalar_norm']),
    9:([2,8],['actual_host_definitions','quantitative_DataX_endpoint']),
    10:([],['actual_host_fields','half_different_norm','original_DataX','model_GamAt_and_HalfDiff']),
    11:([5,6,8,9,10],['quantitative_DataX_endpoint','LawsCore_fields','HasPrinc','original_datum_and_level']),
    12:([10,11],['core_GamAt','model_GamAt_and_HalfDiff','core_DataX_model_endpoint','page_size_predicate','DataXOfModelSt','principal_chart_boundary','ICL_original_chart_use']),
}

foundations = [
    {'id':'PCL_STANDARD_NUMBER_FIELD_ALGEBRA','kind':'standard_algebraic_foundations','name':'Dedekind ideals, trace and different','not_a_DAG_claim':True,'not_reconstructed':True,
     'statement':'The ring of integers is a finite free Z-module and a Dedekind domain; nonzero fractional ideals are invertible and factor uniquely into primes. The number-field trace pairing is nondegenerate. The absolute different is the inverse trace-dual of O, has norm equal to the absolute discriminant, and obeys the tower identity. Finite torsion-free modules over Z are free. These general foundations are not counted as new numbered deductions.',
     'application_checked':'PCL1-PCL4 derive the particular coordinate, ideal-valued dual and exact lattice identities. PCL7 writes the quadratic integer-ring, trace-dual and norm arguments explicitly. PCL10 derives the actual quantitative half-different bound. No principal or free O-basis assumption is made on a supplied lattice.'},
    {'id':'PCL_ORIGINAL_DATUM','kind':'original_quantified_input_data','name':'Original perfect alternating Datum','not_a_DAG_claim':True,'not_reconstructed':True,
     'statement':'PCL1 takes the literal original Datum: its finite module, rank, perfect alternating pairing, and adjoint O_E action. It constructs coordinates without altering that module or pairing.'},
    {'id':'PCL_ORIGINAL_DATA_AND_CONGRUENCE','kind':'original_quantified_input_data','name':'Original Data and literal generic DataX hypotheses','not_a_DAG_claim':True,'not_reconstructed':True,
     'statement':'PCL5 quantifies over the original Data, conjugate fractional ideals satisfying the printed ideal equation, integral perfect trace pairing, constant absolute-value bound k<=1, and positive principal modulus with the exact subgroup inclusion. These are precisely the original generic constructor hypotheses. Its proof constructs all extra DataX fields.'},
    {'id':'PCL_SUPPLIED_UNIFORMIZATION','kind':'original_quantified_input_data','name':'The same supplied Unf and IsUnf witness','not_a_DAG_claim':True,'not_reconstructed':True,
     'statement':'PCL6 retains the actual Unf/IsUnf and uses its recorded equivalence from a perfect alternating Datum to each exact component lattice. It does not construct a uniformization, framed points, metric dictionary or N1c.'},
    {'id':'PCL_ORIGINAL_HOST','kind':'original_quantified_input_data','name':'The original host field and stored half-different data','not_a_DAG_claim':True,'not_reconstructed':True,
     'statement':'The actual host supplies E, K=Q(sqrt(-d)), the prime/congruence conditions, conjugation/embedding law, nonzero ccK and the half-different factorization. PCL7-PCL10 prove the required principal ideal, scalar and denominator consequences; they do not construct a new host.'},
    {'id':'PCL_CORE_LAWS_AND_PRINCIPAL','kind':'retained_original_hypotheses','name':'Actual LawsCore and HasPrinc/GamAt','not_a_DAG_claim':True,'not_reconstructed':True,
     'statement':'PCL11-PCL12 retain the original supplied Core/Top and LawsCore, hence the same IsUnf and xiAbs fields, and the original HasPrinc/GamAt principal-congruence inclusion at the exact level M. The output constructs DataX on those same charts, for every InR row and every good embedding.'},
    {'id':'PCL_PAGE_SIZE_HYPOTHESES','kind':'original_quantified_input_data','name':'Original SupBoundPageRows and size hypotheses','not_a_DAG_claim':True,'not_reconstructed':True,
     'statement':'The full original DataXOfModelSt size and weight hypotheses remain. Its ccK logarithmic inequality is the fourth actual SupBoundPageRows conjunct. The constructed L\u2032, NA and NC are independent of the later weight and size record.'},
]
external={1:['PCL_STANDARD_NUMBER_FIELD_ALGEBRA','PCL_ORIGINAL_DATUM'],2:['PCL_STANDARD_NUMBER_FIELD_ALGEBRA'],3:['PCL_STANDARD_NUMBER_FIELD_ALGEBRA'],5:['PCL_ORIGINAL_DATA_AND_CONGRUENCE'],6:['PCL_SUPPLIED_UNIFORMIZATION'],7:['PCL_STANDARD_NUMBER_FIELD_ALGEBRA','PCL_ORIGINAL_HOST'],8:['PCL_ORIGINAL_HOST'],9:['PCL_ORIGINAL_HOST'],10:['PCL_STANDARD_NUMBER_FIELD_ALGEBRA','PCL_ORIGINAL_HOST'],11:['PCL_CORE_LAWS_AND_PRINCIPAL'],12:['PCL_CORE_LAWS_AND_PRINCIPAL','PCL_PAGE_SIZE_HYPOTHESES']}
scopes={
1:'Every original Datum and nonzero anti-invariant xi, exact original rank including zero, same lattice and trace sign.',
2:'Every full O_E-lattice and nonzero fractional ideal, including nonprincipal ideals and nonfree lattices.',
3:'Exact left-linear Hermitian convention and absolute different; full original additive perfectness predicate.',
4:'The original untwisted lattice A^-1 Lambda itself is self-dual, not merely commensurable or saturated.',
5:'All extra fields of original DataX from precisely the literal generic hypotheses; same Data and g.',
6:'Each actual component of every supplied original IsUnf, using its recorded lattice equivalence.',
7:'Actual host K=Q(sqrt(-d)), actual conjugation, absolute different and norm ideal; no new arithmetic field choice.',
8:'Original xi0, AA, AAbar and constant xiR, including full principal ideal identity.',
9:'Exact NA=Norm(b) and NC=Norm(ccK), uniform in components and embeddings.',
10:'Full HalfDiffNormSt, norm square <= absolute discriminant, and exact half-log normalization.',
11:'Literal exists_dataX_of_hasPrinc: every InR row, good embedding and component, retaining LawsCore/HasPrinc.',
12:'Literal dataXOfModel_of_gamAt and full DataXOfModelSt, same modulus and every weight/size record; original charts/GamAt retained.',
}

files={}; sources={}; excerpts=[]
for key,(rel,lo,hi,title) in specs.items():
    data=(repo/rel).read_bytes()
    assert data==subprocess.check_output(['git','-C',str(repo),'show',PIN+':'+rel]),rel
    lines=data.splitlines(keepends=True); hi=hi or len(lines)
    assert 1<=lo<=hi<=len(lines),(key,lo,hi,len(lines))
    block=b''.join(lines[lo-1:hi]); url=f'https://github.com/CocoSgt/riemann-hypothesis-lean/blob/{PIN}/{rel}'
    files[rel]={'path':rel,'sha256':sha(data),'bytes':len(data),'line_count':len(lines),'verified_equal_to_pinned_git_blob':True,'url':url}
    sources[key]={'id':'PCL_SRC_'+key.upper(),'path':rel,'declaration':title,'line_start':lo,'line_end':hi,'source_commit':PIN,'file_sha256':sha(data),'full_file_sha256':sha(data),'range_sha256':sha(block),'range_bytes':len(block),'verified_equal_to_pinned_git_blob':True,'url':url+f'#L{lo}-L{hi}'}
    excerpts.append(f'[{sources[key]["id"]}] {title}\n{sources[key]["url"]}\n'+block.decode())

text=(HERE/'main.tex').read_text(); assert not any(ord(c)<32 and c not in '\n\t' for c in text)
main_sha=sha(text.encode()); claims=[]; foundation_ids={f['id'] for f in foundations}
for i,(deps,groups) in relations.items():
    cid=f'PCL{i}'; match=re.search(r'^% BEGIN '+cid+r'\n.*?^% END '+cid+r'\n',text,re.M|re.S)
    assert match and r'\label{claim:'+cid+'}' in match.group(),cid
    assert all(d<i for d in deps); assert set(external.get(i,[]))<=foundation_ids
    start=text[:match.start()].count('\n')+1
    claims.append({'id':cid,'title':re.search(r'\\paragraph\{'+cid+r'\. (.*?)\}\n',match.group(),re.S).group(1),'introduced_in':VERSION,'classification':'B','depends_on':[f'PCL{d}' for d in deps],'external_input_ids':external.get(i,[]),'scope_note':scopes[i],'source_groups':groups,'sources':[sources[k] for k in groups],'proof_location':{'file':COMPONENT+'/main.tex','label':'claim:'+cid,'line_start':start,'line_end':start+match.group().count('\n')-1,'sha256':sha(match.group().encode()),'bytes':len(match.group().encode())},'source_proof_is_not_human_proof':True})

reviews=[]; reviewed=set(); lookup={c['id']:c['proof_location']['sha256'] for c in claims}
for p in sorted(HERE.glob('review_*.json')):
    review=json.loads(p.read_text()); assert review.get('status',review.get('result'))=='PASS',p
    ids=[]; stale=False
    for entry in review.get('claims_reviewed',review.get('reviewed_claims',[])):
        cid=entry if isinstance(entry,str) else entry.get('id',entry.get('claim'))
        expected=review.get('proof_hashes',{}).get(cid) if isinstance(entry,str) else entry.get('proof_range_sha256',entry.get('block_sha256'))
        assert cid in lookup,(p,cid); stale=stale or expected!=lookup[cid]; ids.append(cid)
    if stale: continue
    reviewed.update(ids)
    reviews.append({'file':str(p.relative_to(ROOT)),'sha256':sha(p.read_bytes()),'reviewer':review.get('reviewer'),'result':'PASS','reviewed_proof_file_sha256':review.get('proof_file_sha256',review.get('proof_sha256')),'proof_file_sha256':main_sha,'reviewed_blocks_unchanged':True,'claims':ids})
status='complete_at_stated_scope_independently_reviewed' if set(lookup)<=reviewed else 'complete_at_stated_scope_pending_independent_review'
for claim in claims:
    claim['status']='complete_at_stated_scope_independently_reviewed' if claim['id'] in reviewed else 'complete_at_stated_scope_pending_independent_review'
    claim['independent_review_files']=[r['file'] for r in reviews if claim['id'] in r['claims']]

completed=[
{'endpoint':'GlobalTheory.exists_herm_coord_of_datum','claim':'PCL1','status':'whole_literal_constructor_written','scope':'Original finite perfect alternating datum, anti-invariant nonzero xi and r=p+q, including rank zero.'},
{'endpoint':'GlobalTheory.exists_dataX_of_perfect_traceForm','claim':'PCL5','status':'whole_literal_generic_constructor_written','scope':'Every original Data and all its printed ideal, trace, absolute-value and congruence hypotheses; every DataX field constructed.'},
{'endpoint':'GlobalTheory.traceForm_integral_perfect_of_isUnf','claim':'PCL6','status':'whole_literal_implication_written','scope':'Each component of the same supplied IsUnf.'},
{'endpoint':'Formalism.BasicNotions.DiffKPrincipal / CcNorm / FactPrincipalDatum','claim':'PCL8','status':'actual_host_producers_written','scope':'Original host field, half-different, ccK and xi0; PCL7 proves the quadratic arithmetic inputs.'},
{'endpoint':'ReciprocityTheory.ChartRestriction.G.PullbackSections.HalfDiffNormSt','claim':'PCL10','status':'whole_literal_host_bound_written','scope':'Original Norm(b)>0 and 2 log Norm(b)<=log|disc E|.'},
{'endpoint':'GlobalTheory.LatticeData.exists_dataX_of_hasPrinc','claim':'PCL11','status':'whole_literal_constructor_written_at_original_hypotheses','scope':'Same original Core, LawsCore, InR row, good embedding, supplied HasPrinc; exact NA/NC/g/k0 and original lattice.'},
{'endpoint':'GlobalTheory.LatticeData.dataXOfModel_of_gamAt','claim':'PCL12','status':'whole_literal_constructor_written_at_original_hypotheses','scope':'Actual LawsCore and GamAt, every original row and good embedding.'},
{'endpoint':'Formalism.L2.Pj.QAt.DataXOfModelSt','claim':'PCL12','status':'whole_literal_model_constructor_written_at_original_hypotheses','scope':'Original Top/GamAt/LawsCore, every row, page size and weight, same NA/NC/g and exact logarithmic bounds.'},
]
boundaries=[
'The common IsUnf family and its actual principal congruence inclusion HasPrinc/GamAt remain supplied original hypotheses. This packet does not prove exists_unf_hasPrinc.',
'The original LawsCore, framed-point normalization, global metric dictionary, and common-field/common-measure/common-phase construction are not produced.',
'PCL constructs the actual DataX lattice/normalization part of the ICL principal-chart group; it does not remove that entire producer group.',
'Finite IsSystem, raw Gaussian/integrability/reproduction, global short-rule gluing/reading, and ramified integral jet/value estimates remain separate.',
'No full unconditional LatFull, higher CoversAt, all-tuple ClsEx, PointIdentCore or ClassSumsSpan is inferred. No selected whole common-family obligation is closed.',
'The stronger ModelLatSt transvection/short-inverse package is not asserted merely from DataXOfModelSt.',
]
contract={'schema':'rh-human-component-contract/1','artifact_version':VERSION,'component':COMPONENT,'source_commit':PIN,'proof_file_sha256':main_sha,'claims':'PCL1-PCL12','claim_count':12,'main_outcome':'Original Hermitian-coordinate and DataX constructors, exact self-dual untwisting, host denominators and all-row logarithmic normalization on supplied principal charts.','completed_source_endpoints':completed,'quantifier_order':['Fix the original number field, datum or Data; no new common arithmetic family is chosen.','Construct the actual Hermitian coordinate map or L\u2032=A^-1 Lambda using the original forms and ideals.','For the host specialization fix the same Core/Top, LawsCore and HasPrinc/GamAt.','For every InR row, every good embedding and every component, construct DataX on exactly its existing Data.','Choose L\u2032, NA=Norm(b), NC=Norm(ccK), k0=2 xiR and g=M before every later row weight and page-size record.','Apply the exact SupBoundPageRows conjunct to the same NC; retain all other original size/weight hypotheses.'],'literal_normalizations':{'Hermitian':'h_G(x,y)=x^t G conjugate(y), linear in first variable','trace':'B_xi,G=Tr(-xi*h_G)','coordinate_theorem':'EF=Tr(xi*h_G), so use -xi0 for the chart convention','trace_dual':'Lambda^B=((xi)*D_E)^-1 Lambda^#','self_dual_lattice':'L\u2032=AA^-1 Lambda','NA':'Norm_E(b)','NC':'Norm_K(ccK)','g':'the original level M','k0':'2*xiR','log_NA':'<= (1/2)*log|disc(E)| = fdeg(E)*log(rdE(E))'},'complete_DataX_fields':['toData unchanged','k0','minWeight_pos','k0_le','xi0_abs','EF_int','EF_perf','L\u2032','L\u2032_fg','L\u2032_int','L\u2032_dual','NA','NC','NA_pos','NC_pos','NA_sub','NC_sub','g','g_pos','cong'],'rank_scope':'PCL1 generic rank includes zero; all host/range restrictions in the original consumers are retained.','no_principal_fractional_ideal_assumption':True,'no_free_O_lattice_assumption':True,'original_HasPrinc_retained':True,'original_LawsCore_retained':True,'retained_input_ids':[f['id'] for f in foundations],'not_supplied':boundaries,'whole_obligations_closed':[],'non_premise_references':[{'location':'introduction and final scope paragraph','references':['ICL','IsSystem','Gaussian','short-rule','higher CoversAt','ClsEx','PointIdentCore','ClassSumsSpan'],'reason':'Scope and later-consumer boundaries only; PCL has no inherited human-proof premise from those claims.'}]}
manifest={'schema':'rh-source-manifest/1','artifact_version':VERSION,'component':COMPONENT,'source_commit':PIN,'files':list(files.values()),'ranges':list(sources.values()),'all_files_equal_pinned_git_blobs':True,'file_count':len(files),'range_count':len(sources)}
provenance={'schema':'rh-human-component-provenance/1','artifact_version':VERSION,'component':COMPONENT,'source_commit':PIN,'proof_file_sha256':main_sha,'main_tex_sha256':main_sha,'status':status,'claims':claims,'source_groups':sources,'inherited_human_inputs':[],'classical_and_foundational_inputs':foundations,'independent_reviews':reviews,'dependency_convention':'depends_on contains only numbered written human claims; standard foundations and original quantified records use separate external_input_ids.','source_proof_is_not_human_proof':True,'root_ledger_modified':False,'frozen_artifacts_modified':False}
closure={'schema':'rh-human-component-closure/1','artifact_version':VERSION,'component':COMPONENT,'source_commit':PIN,'proof_file_sha256':main_sha,'status':status,'completed_source_endpoints':completed,'whole_obligations_closed':[],'proposed_global_frontier_leaf_closures':[],'remaining':boundaries,'full_literal_generic_DataX_supplied':True,'full_literal_DataXOfModelSt_supplied_at_original_hypotheses':True,'full_principal_chart_existence_supplied':False,'full_LatFull_unconditional_supplier_closed':False,'independent_reviews':reviews,'pending_independent_review':sorted(set(lookup)-reviewed),'validation':'Two-pass standalone draft TeX, no PDF, no Lean replay; independently authored hash-bound reviews.'}
for name,value in [('provenance.json',provenance),('source_manifest.json',manifest),('contracts.json',contract),('original_contracts.json',contract),('closure.json',closure),('retained_foundations.json',foundations)]:
    (HERE/name).write_text(json.dumps(value,indent=2,ensure_ascii=False)+'\n')
(HERE/'source_excerpts.txt').write_text('\n\n'.join(excerpts))
report=[
'PRINCIPAL CUSP LATTICES ON THE ORIGINAL CHARTS — v0.47',
'Source pin: '+PIN,'Proof SHA256: '+main_sha,
f'Claims: 12; source files: {len(files)}; exact source ranges: {len(sources)}.',
'Status: '+status,'',
'PCL1 constructs the original Hermitian coordinates from the exact perfect alternating',
'Datum. PCL2-PCL5 give a full human derivation of the literal DataX constructor.',
'The constructed lattice is exactly L\u2032=AA^-1 Lambda and is Hermitian self-dual by',
'the precise trace-dual/different calculation. No lattice saturation, commensurability',
'replacement, fractional-ideal principalization or free O-basis is used.',
'',
'PCL6 transports the original perfect pairing through each supplied IsUnf component.',
'PCL7-PCL10 prove the actual host quadratic different/norm identities, the original',
'principal ideal identity, the scalar xiR, and the exact denominators NA=Norm(b),',
'NC=Norm(ccK). They prove NA^2<=|disc E| and the exact half-log bound.',
'PCL11-PCL12 establish the entire original exists_dataX_of_hasPrinc,',
'dataXOfModel_of_gamAt, and DataXOfModelSt conclusions on every original row and',
'good embedding, with one construction before every later weight/size record.',
'',
'The original IsUnf, HasPrinc/GamAt and LawsCore remain supplied hypotheses.',
'Principal-chart existence, framed-point/metric normalization and the common family',
'are not inferred. Only the actual lattice/normalization subproducer in the ICL',
'principal-chart group has been constructed. The remaining level-system, Gaussian,',
'short-rule and ramified-jet producers stay explicit; no whole LatFull or common',
'DESIGN_CHOICES_COMMON / BASE_THETA_RATIONAL_TESTS closure is claimed.',
'',
'Foundations are separately named standard number-field/Dedekind algebra and the',
'literal quantified input records; no opaque specialized theorem is counted as proof.',
'Rebuild: python build_metadata.py --repo /path/to/formal_source',
'Validate: python validate_tex.py --format /path/to/pdflatex.fmt',
'Every source file is compared with its pinned git blob and every range/proof block',
'is SHA256-bound. Root/shared files and all frozen proof packets are untouched.',
]
(HERE/'report.txt').write_text('\n'.join(report)+'\n')
hashes={p.name:sha(p.read_bytes()) for p in sorted(HERE.iterdir()) if p.is_file() and p.name!='hashes.json'}
(HERE/'hashes.json').write_text(json.dumps({'artifact_version':VERSION,'component':COMPONENT,'hashes':hashes},indent=2)+'\n')
print(json.dumps({'component':COMPONENT,'claims':len(claims),'source_files':len(files),'source_ranges':len(sources),'proof_file_sha256':main_sha,'status':status},indent=2))
