#!/usr/bin/env python3
"""Rebuild exact bindings for the integral cusp lattice packet; no common edits."""
from pathlib import Path
import argparse, hashlib, json, re, subprocess

HERE=Path(__file__).resolve().parent
ROOT=HERE.parent
PIN='7cbf7a0c32fca1badf05931879a37c3f8a2b03b4'
VERSION='0.46'
COMPONENT=HERE.name
ap=argparse.ArgumentParser()
ap.add_argument('--repo',type=Path,required=True)
repo=ap.parse_args().repo.resolve()
sha=lambda b:hashlib.sha256(b).hexdigest()
assert subprocess.check_output(['git','-C',str(repo),'rev-parse','HEAD'],text=True).strip()==PIN

A='src/Development/AbelianVarietyTheory/'
P=A+'Proofs/'
D=P+'DivisorProofs/'
C=P+'CubicalLineBundles/'
U=P+'UnitaryExistence/'
S=P+'SiegelThetaTransformation/'
J=P+'RingsOfIntegers/'
F='src/Formalism/LocalToGlobal/ProjectiveLattices/'
W='src/Formalism/LocalToGlobal/IndefiniteReal/FWExist.lean'
specs={
 'valuation_lattice':(A+'BlockTheory/DivisorBase/KappaLatticeEvaluation.lean',16,None,'Original latIn, supLat, FullAt and every-DVR mem_supLat'),
 'integral_frames':(F+'VAtVNeBot.lean',44,101,'Whole integral eigenspace bases, theta generator, rigidifications, IntFr and every finite-residue test'),
 'test_algebras':(F+'AlgebraMapCAt.lean',9,58,'Reduced finite-type TRing and the original FromTest/evaluation interface'),
 'valuation_normalization':(F+'OneLtAbsNormReal.lean',122,126,'Exact positive ramification-index OverLa condition'),
 'all_valuation_tests':(F+'NonnegIffOfLiesTotal.lean',15,30,'algCls and literal valSet range'),
 'finite_integral_functionals':(D+'FgIntOfForallIsIntegral.lean',1,None,'Original integral-functional finite-generation theorem; ICL2 gives finite separating-family proof'),
 'generic_power_and_fg':(D+'ExistsSmulNonnegOfPow.lean',25,70,'Original exists_smul_nonneg_of_pow and generic fg_latIn'),
 'rational_CM_flags':('src/ReciprocityTheory/ReductiveGroups/ArithmeticGeometry/FundamentalDomains/NonvanishingNearMaximum.lean',17,25,'Exact qualitative LamBasis fields; no quantitative radius is claimed'),
 'CM_point_at_frame':(C+'ExistsGoodCmPointAtCmBasisFrame.lean',21,43,'Original CM point construction at a rational Hermitian frame'),
 'CM_object':(C+'CmPointObjectExistsOfLaws.lean',105,192,'Original CM object, abelian model, action and polarized-frame interface'),
 'integral_CM_object':(C+'ExistsGoodCmPointOfIntegralCmObject.lean',30,58,'Integral CM object to original framed moduli point'),
 'CM_detection':(D+'ExistsGoodCmPtFrPolyNeZero.lean',70,111,'Original stronger quantitative nonzero CM evaluation; ICL3-7 replace only its qualitative role'),
 'CM_integral_frame':(C+'ExistsRankOneCuspLatticeDataOfPrincipal.lean',1,None,'Original integral CM frame/section construction used by source finite-generation branch'),
 'reading_independence':(U+'ReadingLinearIndependentAndInjective.lean',22,None,'Exact original complex reading and finite K-linear-independence preservation'),
 'finite_dimensional_cusps':(U+'CuspFormsDominantWeightFiniteDimensional.lean',24,None,'Fixed-weight finite-dimensionality from original reading and actual analytic cusp components'),
 'good_embedding_finite_dim':(U+'CuspFormsFiniteDimensionalOfGoodEmb.lean',11,None,'Literal good-embedding finite-dimensionality endpoint'),
 'cusp_product':(D+'ExistsSmulNonnegOfPow.lean',74,85,'Literal dominant cusp power with summed exponent'),
 'identity_cover_data':(F+'ThShort.lean',114,234,'DeltaDat, IsLev, UnitC, PhiPin, PsiTie and original half-quotient character conventions'),
 'short_rules':(F+'ThShort.lean',235,299,'harmL, exact shortGen, IsShortRule and ShortValTot'),
 'canonical_connection':(P+'CuspFormEvaluations/ExistsIsNab.lean',1,None,'Original canonical IsNab producer retained as input to the identity-cover construction'),
 'higher_cover_construction':(U+'ExistsDeltaDatumHigherLevel.lean',85,None,'Original higher-cover producer; not reconstructed by the identity-cover proof'),
 'principal_chart':(D+'ExistsSmulNonnegOfPow.lean',87,137,'Actual same-Gram/same-xi principal-chart construction retained explicitly'),
 'metric_comparison':(D+'IsMetricOfIsOrtho.lean',14,None,'Actual metric at orthogonal frames and boundedness transfer to the same principal charts'),
 'level_system':(A+'Definitions/SpanningFamilies/IsSystem.lean',99,147,'Original kernel, invariant families, slab, IsSystem and all IsForm fields'),
 'operator_coefficients':(S+'LatticeOperatorCoefficients.lean',15,None,'Original positive class weights, mass, covariance and class-sum coefficient estimates'),
 'kernel_identity':(S+'KernelIdentity.lean',181,None,'Original raw theta/Gaussian kernel identity and its exact normalizing scalar; retained producer'),
 'kernel_unfolding':(S+'HermitianThetaSeriesSpanBoundedForms.lean',22,None,'Source finite-rank unfolding, thin-slab integrability and bounded inverse/reproducer argument'),
 'stable_range':(S+'LevelThetaSpan.lean',1,None,'Exact original stable exponent threshold'),
 'integral_harmonic_span':(S+'HarmonicRowHighestEqSpanIntegralHarmonic.lean',1,None,'Original coefficient field and literal integral harmonic highest-weight lattice'),
 'lower_row_dictionary':(S+'StableFormsEqSumThetaSeriesFreeLowerRows.lean',1,None,'Original lower-row/lattice translation dictionary retained explicitly'),
 'short_reading':(S+'ShortSeriesReadingsEqClassicalThetaSeries.lean',88,None,'Original simultaneous short-rule reading with component-independent nonzero scalar'),
 'short_gluing':(P+'CuspFormEvaluations/ShortValTotOfPinned.lean',1,None,'Original short-rule gluing and chart independence retained explicitly'),
 'exact_short_span':(D+'BddMemSpanShortGen.lean',29,None,'Literal bounded-section shortGen span and identity-cover exists_datum_span consumer'),
 'reading_coefficient_descent':(S+'CuspFormsLeSpanShortThetaSeries.lean',22,66,'Original independence-based coefficient descent to the same K'),
 'short_value_on_cover':(J+'EvROfFrMapFromTest.lean',24,None,'Actual finite DVR extension and short_value_on_cover, including torsion and phase data'),
 'jet_class_bound':(D+'ExistsSmulShortNonneg.lean',217,269,'Original class_bound without beta in Xq; ramified integral-jet estimate retained'),
 'host_chart_bound':(J+'HarmonicValuationLowerBoundHostFieldAllPlaces.lean',39,None,'Actual chBound_host at all finite places and original half-discriminant term'),
 'average_and_scalar':(J+'ShortGeneratorPlaceValuationBoundProof.lean',71,124,'Normalized finite-average inequality and literal nrm_nat identity'),
 'nonnegative_degree':(F+'ThProps.lean',28,28,'DF is the natural sum of row degrees'),
 'host_discriminant_definition':('src/Development/AutomorphicArithmetic/PrimeDiscriminants/SlopeTestRemainingChoices.lean',28,32,'Literal vdH is ord_p(abs(disc E)) divided by the positive field degree'),
 'discriminant_bound':('src/Development/AutomorphicArithmetic/CyclotomicBounds/RamifiedDiscriminants/VdHLeNatAbs.lean',1,None,'Original host vdH nonnegativity and absolute discriminant upper bound'),
 'uniform_denominator':(D+'ExistsSmulShortNonneg.lean',275,None,'Source global clearing scalar and every-place cancellation, with normalized ramification'),
 'full_at':(D+'ExistsSmulNonnegOfPow.lean',142,None,'Whole literal positive-weight fullAt_of_pins target; only conditional span installation supplied here'),
 'full_lattice_definition':(W,222,239,'Original FullLat and exact transport through the existing source map'),
 'LatFull_definition':(W,723,727,'Original all-row LatFull predicate'),
 'literal_endpoints':(D+'IntegralCuspFormsFullLattice.lean',11,None,'Actual fullLat, canonical weight, LatFull and original FWTie/MKFull/both Boolean MLat endpoints'),
}

relations={
 1:([],['valuation_lattice','integral_frames','test_algebras','valuation_normalization','all_valuation_tests']),
 2:([],['finite_integral_functionals','generic_power_and_fg']),
 3:([],['rational_CM_flags','CM_detection']),
 4:([3],['CM_point_at_frame','CM_object','test_algebras','reading_independence']),
 5:([4],['CM_object','integral_CM_object','CM_integral_frame','integral_frames']),
 6:([5],['CM_integral_frame','integral_frames']),
 7:([1,4,5,6],['integral_frames','test_algebras','valuation_normalization','CM_detection','CM_integral_frame']),
 8:([2,7],['finite_dimensional_cusps','good_embedding_finite_dim','reading_independence','generic_power_and_fg','valuation_lattice']),
 9:([1],['generic_power_and_fg']),
 10:([],['cusp_product']),
 11:([],['identity_cover_data','canonical_connection','higher_cover_construction']),
 12:([],['level_system','operator_coefficients','kernel_unfolding']),
 13:([],['kernel_unfolding']),
 14:([12,13],['kernel_identity','kernel_unfolding','level_system']),
 15:([],['short_rules','integral_harmonic_span']),
 16:([8,11,14,15],['principal_chart','lower_row_dictionary','short_reading','short_gluing','exact_short_span','reading_coefficient_descent','stable_range']),
 17:([],['average_and_scalar']),
 18:([11,17],['short_value_on_cover','jet_class_bound','host_chart_bound','average_and_scalar','nonnegative_degree','host_discriminant_definition','discriminant_bound','uniform_denominator']),
 19:([1,8,9,10,11,16,18],['principal_chart','metric_comparison','full_at','full_lattice_definition','valuation_lattice']),
 20:([19],['LatFull_definition','literal_endpoints']),
 21:([20,'RTG22','RTG23'],['literal_endpoints','full_lattice_definition']),
}

foundations=[
 {'id':'ICL_ORIGINAL_MODULI_UNIFORMIZATION','kind':'retained_original_data_and_validity',
  'name':'Same original pinned moduli datum and valid uniformization',
  'not_reconstructed':True,'not_a_DAG_claim':True,
  'statement':'The fixed D,T,Q,c,l, row, good embedding, original moduli uniformization, its algebraic rule evaluation and naturality. The common-family existence is not asserted. The qualitative CM argument is applied to this supplied actual moduli object.',
  'source_groups':['valuation_lattice','integral_frames','test_algebras','reading_independence','good_embedding_finite_dim']},
 {'id':'ICL_CM_CLASSICAL','kind':'named_classical_foundation','name':'Riemann uniformization and algebraicity of CM abelian varieties',
  'not_reconstructed':True,'not_a_DAG_claim':True,
  'statement':'A polarized complex torus is algebraic, and a complex abelian variety with a commutative semisimple endomorphism algebra of dimension twice its dimension has a number-field model with its finite polarization/action/level data after finite extension. The chosen frame fibre is the actual finite-type algebraic fibre.',
  'application_checked':'ICL3 makes an orthogonal decomposition into E-lines; the lattice is commensurable with their sum, giving E^r in End^0 and precisely the CM dimension. ICL4 descends finite data and uses the same moduli fibre.',
  'references':[{'author':'J. S. Milne','title':'Complex Multiplication','location':'Chapters I-II','url':'https://www.jmilne.org/math/CourseNotes/CM.pdf','checked_online':True}],
  'source_groups':['CM_point_at_frame','CM_object','integral_CM_object']},
 {'id':'ICL_CM_POTENTIAL_GOOD_REDUCTION','kind':'named_primary_classical_foundation','name':'Serre-Tate potential good reduction for CM abelian varieties',
  'not_reconstructed':True,'not_a_DAG_claim':True,
  'statement':'At each finite place with finite residue field, a CM abelian variety acquires good reduction after finite extension.',
  'application_checked':'ICL5 applies it only at the finitely many bad finite places, then proves the global finite-extension/gluing step using weak approximation, Krasner and normal closure.',
  'references':[{'authors':'J.-P. Serre and J. Tate','title':'Good reduction of abelian varieties','journal':'Annals of Mathematics 88 (1968), 492-517','location':'Theorem 6(a)','url':'https://annals.math.princeton.edu/1968/88-3/p05','checked_online':True}],
  'source_groups':['CM_object','integral_CM_object','CM_integral_frame']},
 {'id':'ICL_ABELIAN_SCHEME_FOUNDATIONS','kind':'named_classical_foundation','name':'Abelian scheme extension, cube and coherent base change',
  'not_reconstructed':True,'not_a_DAG_claim':True,
  'statement':'Homomorphisms of abelian schemes extend uniquely over a normal Dedekind base; rigidified generic line bundles extend as the appropriate cubical line bundles; a principal ample line bundle has a rank-one relative section module commuting with base change. Flat base change and torsion-freeness are used for the integral Lie kernels; no ramified integral eigenspace direct-sum theorem is assumed.',
  'application_checked':'ICL5 keeps the original polarization and its inverse and rigidification, extends action maps, identifies whole saturated integral Lie eigenspace kernels, and ICL6 principalizes their projective modules after a finite field extension.',
  'references':[{'author':'L. Moret-Bailly','title':'Pinceaux de varietes abeliennes','publication':'Asterisque 129 (1985)','location':'Chapters I and VI','url':'https://www.numdam.org/item/AST_1985__129__1_0/','checked_online':True}],
  'source_groups':['integral_frames','CM_object','CM_integral_frame']},
 {'id':'ICL_FIXED_WEIGHT_FINITE_DIMENSION','kind':'named_primary_classical_foundation','name':'Harish-Chandra fixed-type automorphic finite-dimensionality',
  'not_reconstructed':True,'not_a_DAG_claim':True,
  'statement':'The holomorphic cusp forms of one fixed highest weight on each fixed arithmetic uniformization component form a finite-dimensional complex space.',
  'application_checked':'ICL8 uses only the given finite component family and fixed weight. It proves preservation of finite K-linear independence after the fixed complex scalar extension from reduced finite-type test rings, so it obtains the literal K-space dimension assertion.',
  'references':[{'author':'Harish-Chandra','title':'Automorphic forms on semisimple Lie groups','publication':'Lecture Notes in Mathematics 62 (1968)','location':'Theorem 1','url':'https://doi.org/10.1007/BFb0098434','checked_online':True},{'author':'A. Borel','title':'Automorphic forms on reductive groups','location':'Section 8.4','url':'https://homepages.math.uic.edu/~rtakloo/papers/borel/borel3.pdf','checked_online':True}],
  'source_groups':['finite_dimensional_cusps','good_embedding_finite_dim']},
 {'id':'ICL_CANONICAL_NAB_INPUT','kind':'retained_original_unreconstructed_producer','name':'Original canonical connection with all IsNab laws',
  'not_reconstructed':True,'not_a_DAG_claim':True,
  'statement':'An original canonical connection nab satisfying IsNab on the same moduli object is supplied to ICL11. The identity-cover construction does not reprove the connection laws.',
  'source_groups':['canonical_connection','identity_cover_data']},
 {'id':'ICL_PRINCIPAL_CHART_INPUT','kind':'retained_original_unreconstructed_producer','name':'Actual same-Gram principal charts and metric comparison',
  'not_reconstructed':True,'not_a_DAG_claim':True,
  'statement':'For every original row, the original SupFull.exists_unf construction on the same Q has common Gm and xi0, principal stabilizers, trivial scalar multipliers and the source lattice comparison. The original metric identifies the given bounded readings with these charts.',
  'source_groups':['principal_chart','metric_comparison']},
 {'id':'ICL_LEVEL_SYSTEM_INPUT','kind':'retained_original_unreconstructed_producer','name':'Actual level-system producer with quantitative norm bound',
  'not_reconstructed':True,'not_a_DAG_claim':True,
  'statement':'At every required stable exponent the original IsSystem supplies its actual lattice family, unit vacua, scalar cocycle, support/cusp/admissibility, finite class set and positive weights, and the summable off-diagonal majorant of mass strictly smaller than the diagonal. The chosen common family is not replaced.',
  'source_groups':['level_system','operator_coefficients','stable_range']},
 {'id':'ICL_RAW_GAUSSIAN_INPUT','kind':'retained_original_unreconstructed_producer','name':'Original kernel identity, thin-slab integrability and reproducer',
  'not_reconstructed':True,'not_a_DAG_claim':True,
  'statement':'The exact original Gaussian/theta identity, its nonzero kappa and positive rho, the permitted thin slab, absolute kernel integrability and uniform Borel-factor bounds hold. These are explicit original producer premises, not classified as published foundations.',
  'source_groups':['kernel_identity','kernel_unfolding']},
 {'id':'ICL_SHORT_DICTIONARY_INPUT','kind':'retained_original_unreconstructed_producer','name':'Actual global short-rule gluing and simultaneous finite-level dictionary',
  'not_reconstructed':True,'not_a_DAG_claim':True,
  'statement':'For every allowed row and stable weight, the original lattices in distinct orbits and their stabilizers match the principal charts; the lower-row and lattice-translation dictionary and global short rules exist with exact rd_U(g)_k=C_k u_(Lambda,N) Theta_(Lambda,P)(L_k,gamma_k x), u nonzero and independent of k.',
  'source_groups':['lower_row_dictionary','short_reading','short_gluing','exact_short_span']},
 {'id':'ICL_RAMIFIED_JET_INPUT','kind':'retained_original_unreconstructed_producer','name':'All-place integral jet and short-value-on-cover producer',
  'not_reconstructed':True,'not_a_DAG_claim':True,
  'statement':'For every allowed short rule and every original complete-DVR IntFr test, the actual finite extension, all-rational torsion chart, InZh, geometric injection, half-ideal killing, UU and finite-order phase data yield (ICL.13). The literal class_bound and HostChart.chBound_host give (ICL.14)-(ICL.15), including ramified places. No good-prime-only estimate is substituted.',
  'source_groups':['short_value_on_cover','jet_class_bound','host_chart_bound','uniform_denominator']},
]

E={x['id'] for x in foundations}
ext={
 1:['ICL_ORIGINAL_MODULI_UNIFORMIZATION'],
 3:['ICL_ORIGINAL_MODULI_UNIFORMIZATION'],
 4:['ICL_ORIGINAL_MODULI_UNIFORMIZATION','ICL_CM_CLASSICAL'],
 5:['ICL_CM_POTENTIAL_GOOD_REDUCTION','ICL_ABELIAN_SCHEME_FOUNDATIONS'],
 7:['ICL_ORIGINAL_MODULI_UNIFORMIZATION'],
 8:['ICL_FIXED_WEIGHT_FINITE_DIMENSION','ICL_ORIGINAL_MODULI_UNIFORMIZATION'],
 10:['ICL_ORIGINAL_MODULI_UNIFORMIZATION'],
 11:['ICL_ORIGINAL_MODULI_UNIFORMIZATION','ICL_CANONICAL_NAB_INPUT'],
 12:['ICL_LEVEL_SYSTEM_INPUT'],
 14:['ICL_LEVEL_SYSTEM_INPUT','ICL_RAW_GAUSSIAN_INPUT'],
 16:['ICL_PRINCIPAL_CHART_INPUT','ICL_SHORT_DICTIONARY_INPUT'],
 18:['ICL_RAMIFIED_JET_INPUT'],
 19:['ICL_PRINCIPAL_CHART_INPUT','ICL_LEVEL_SYSTEM_INPUT','ICL_RAW_GAUSSIAN_INPUT','ICL_SHORT_DICTIONARY_INPUT','ICL_RAMIFIED_JET_INPUT','ICL_CANONICAL_NAB_INPUT'],
 20:['ICL_PRINCIPAL_CHART_INPUT','ICL_LEVEL_SYSTEM_INPUT','ICL_RAW_GAUSSIAN_INPUT','ICL_SHORT_DICTIONARY_INPUT','ICL_RAMIFIED_JET_INPUT','ICL_CANONICAL_NAB_INPUT'],
 21:['ICL_PRINCIPAL_CHART_INPUT','ICL_LEVEL_SYSTEM_INPUT','ICL_RAW_GAUSSIAN_INPUT','ICL_SHORT_DICTIONARY_INPUT','ICL_RAMIFIED_JET_INPUT','ICL_CANONICAL_NAB_INPUT'],
}
scopes={
 1:'Every original complete DVR, finite residue field, integral frame and positive OverLa ramification index; literal full lattice.',
 2:'Any number-field vector space and arbitrary O_K-submodule; neither spanning nor saturation assumed.',
 3:'Qualitative rational Hermitian flags at every original signature; no uniform quantitative radius or CMPt.Good claimed.',
 4:'Actual moduli CM point and regular frame fibre; original K and embedding retained.',
 5:'One integral abelian model after finite extension, all original Lie eigenspace kernels including ramified primes and actual theta line.',
 6:'Exact whole integral modules, finite extensions only, Zariski-dense integral frames without replacing by bounded-denominator frames.',
 7:'For each nonzero section one K-linear nonzero evaluation integral on the entire L_w at every prime; no denominator depending on the section being evaluated.',
 8:'Actual finite generation of the entire original L_w at every dominant weight, including zero cusp spaces; no spanning premise.',
 9:'All normalized valuation tests simultaneously and every q>=1; one integral clearing scalar in the original K.',
 10:'Every positive original weight and exact original stable exponent q=4([E:Q]r)+4, preserving cusp multiplication.',
 11:'Literal identity DeltaDat, IsLev, UnitC, PsiTie and PhiPin for a supplied original IsNab; no higher cover.',
 12:'Same actual class weights and C operator; convergent Neumann inverse using exactly the supplied IsSystem strict norm bound.',
 13:'Free-a.e. measure-preserving orbit unfolding with finite rank, absolute summability and explicit coefficient integrability; original lattice/frame action verified free.',
 14:'Full theta span as an implication from the exact raw Gaussian/level-system inputs; no arbitrary substitute kernel.',
 15:'Original finite-degree harmonic highest-weight equations and literal harmL integral generators over the same K.',
 16:'Exact original shortGen K-span, conditional on gluing and simultaneous dictionary; coefficient descent uses full independence preservation.',
 17:'Finite nonarchimedean average, root-of-unity phase and explicit denominators, including zero values.',
 18:'One original scalar A_w beta_H before all complete-DVR tests, ramified primes and finite extensions; actual squarefree level and nonnegative DF.',
 19:'Every original positive weight/row FullAt and FullLat, retaining every named spanning producer uniformly over all needed exponents.',
 20:'Literal all-row LatFull and canonical-weight specialization, with the exact original remaining producer premises.',
 21:'Same original FWTie map, whole M_K and both Boolean MLat levels, same common field/metric/measure/phases; conditional LatFull input scope retained.',
}

files={};sources={};excerpts=[]
for key,(rel,lo,hi,title) in specs.items():
    data=(repo/rel).read_bytes()
    assert data==subprocess.check_output(['git','-C',str(repo),'show',PIN+':'+rel]),rel
    lines=data.splitlines(keepends=True);hi=hi or len(lines)
    assert 1<=lo<=hi<=len(lines),(key,rel,lo,hi,len(lines))
    block=b''.join(lines[lo-1:hi]);url=f'https://github.com/CocoSgt/riemann-hypothesis-lean/blob/{PIN}/{rel}'
    files[rel]={'path':rel,'sha256':sha(data),'bytes':len(data),'line_count':len(lines),'verified_equal_to_pinned_git_blob':True,'url':url}
    sources[key]={'id':'ICL_SRC_'+key.upper(),'path':rel,'declaration':title,'line_start':lo,'line_end':hi,'source_commit':PIN,'file_sha256':sha(data),'full_file_sha256':sha(data),'range_sha256':sha(block),'range_bytes':len(block),'verified_equal_to_pinned_git_blob':True,'url':url+f'#L{lo}-L{hi}'}
    excerpts.append(f'[{sources[key]["id"]}] {title}\n{sources[key]["url"]}\n'+block.decode())

text=(HERE/'main.tex').read_text()
assert not any(ord(c)<32 and c not in '\n\t' for c in text)
main_sha=sha(text.encode())
claims=[]
for i,(deps,ss) in relations.items():
    cid=f'ICL{i}';m=re.search(r'^% BEGIN '+cid+r'\n.*?^% END '+cid+r'\n',text,re.M|re.S)
    assert m,cid
    assert r'\label{claim:'+cid+'}' in m.group(),cid
    ds=[f'ICL{x}' if isinstance(x,int) else x for x in deps]
    assert all(not d.startswith('ICL') or int(d[3:])<i for d in ds)
    assert set(ext.get(i,[]))<=E
    lo=text[:m.start()].count('\n')+1
    claims.append({'id':cid,'title':re.search(r'\\paragraph\{'+cid+r'\. (.*?)\}\n',m.group(),re.S).group(1),
      'introduced_in':VERSION,'classification':'B','depends_on':ds,'external_input_ids':ext.get(i,[]),
      'scope_note':scopes[i],'source_groups':ss,'sources':[sources[k] for k in ss],
      'proof_location':{'file':COMPONENT+'/main.tex','label':'claim:'+cid,'line_start':lo,'line_end':lo+m.group().count('\n')-1,'sha256':sha(m.group().encode()),'bytes':len(m.group().encode())},
      'source_proof_is_not_human_proof':True})

inherited=[]
for cid in ['RTG22','RTG23']:
    p=ROOT/'rational_theta/main.tex';t=p.read_text();m=re.search(r'^% BEGIN '+cid+r'\n.*?^% END '+cid+r'\n',t,re.M|re.S)
    assert m,cid
    inherited.append({'claim':cid,'file':'rational_theta/main.tex','file_sha256':sha(p.read_bytes()),'claim_sha256':sha(m.group().encode()),'line_start':t[:m.start()].count('\n')+1,'line_end':t[:m.end()].count('\n'),'kind':'immutable_inherited_human_proof','newly_modified_by_this_component':False})

reviews=[];reviewed=set();lookup={c['id']:c['proof_location']['sha256'] for c in claims}
for p in sorted(HERE.glob('review_*.json')):
    r=json.loads(p.read_text());assert r.get('status',r.get('result'))=='PASS',p
    entries=r.get('claims_reviewed',r.get('reviewed_claims',[]));ids=[]
    stale=False
    for e in entries:
        cid=e if isinstance(e,str) else e.get('id',e.get('claim'))
        expected=r.get('proof_hashes',{}).get(cid) if isinstance(e,str) else e.get('proof_range_sha256',e.get('block_sha256'))
        assert cid in lookup,(p,cid)
        if expected!=lookup[cid]:stale=True
        ids.append(cid)
    if stale:continue
    reviewed.update(ids)
    reviews.append({'file':str(p.relative_to(ROOT)),'sha256':sha(p.read_bytes()),'reviewer':r.get('reviewer'),'result':'PASS','reviewed_proof_file_sha256':r.get('proof_file_sha256',r.get('proof_sha256')),'proof_file_sha256':main_sha,'reviewed_blocks_unchanged':True,'claims':ids})
status='complete_at_stated_scope_independently_reviewed' if set(lookup)<=reviewed else 'complete_at_stated_scope_pending_independent_review'
for c in claims:
    c['status']='complete_at_stated_scope_independently_reviewed' if c['id'] in reviewed else 'complete_at_stated_scope_pending_independent_review'
    c['independent_review_files']=[r['file'] for r in reviews if c['id'] in r['claims']]

completed=[
 {'endpoint':'Original supLat/latIn finite-generation conjunct at every dominant weight','claim':'ICL8','status':'actual_producer_supplied_under_named_classical_foundations','scope':'Same original valid uniformization and full family of integral tests; no short-theta producer, spanning or saturation premise.'},
 {'endpoint':'Identity DeltaDat IsLev/UnitC/PsiTie/PhiPin','claim':'ICL11','status':'actual_identity_cover_constructed_given_original_IsNab','scope':'pd=1, unchanged level/moduli/coefficient record, c_delta=phi_delta=1, zero half quotients; no higher CoversAt.'},
 {'endpoint':'SupFull.exists_smul_nonneg_of_pow','claim':'ICL9','status':'whole_generic_valuation_implication_proved','scope':'Every original valuation family and every positive power, scalar remains in K.'},
 {'endpoint':'Original analytic class-operator inversion and finite-rank kernel-to-theta-span implication','claims':['ICL12','ICL13','ICL14'],'status':'complete_conditional_implication','scope':'Original IsSystem and raw Gaussian producer inputs, actual measure and phases.'},
 {'endpoint':'Original integral harmonic lattice spans its harmonic highest-weight space','claim':'ICL15','status':'actual_linear_algebra_producer_supplied','scope':'Literal harmL, fixed coefficient field and finite homogeneous degree.'},
 {'endpoint':'Original global short-generator clearing scalar','claim':'ICL18','status':'complete_conditional_implication','scope':'Exact all-place ramified jet and short-value-on-cover premises, original squarefree level; explicit A_w beta_H.'},
]
conditional=[
 {'endpoint':'GlobalTheory.SupFull.fullAt_of_pins','claim':'ICL19','conclusion':'FullAt and FullLat at every original positive weight','remaining_input_ids':['ICL_PRINCIPAL_CHART_INPUT','ICL_LEVEL_SYSTEM_INPUT','ICL_RAW_GAUSSIAN_INPUT','ICL_SHORT_DICTIONARY_INPUT','ICL_RAMIFIED_JET_INPUT','ICL_CANONICAL_NAB_INPUT']},
 {'endpoint':'GlobalTheory.GoodLat.Obj.latFull and integralCuspFormsFullLattice','claim':'ICL20','conclusion':'Literal all-row LatFull and canonical weight specialization','remaining_input_ids':['ICL_PRINCIPAL_CHART_INPUT','ICL_LEVEL_SYSTEM_INPUT','ICL_RAW_GAUSSIAN_INPUT','ICL_SHORT_DICTIONARY_INPUT','ICL_RAMIFIED_JET_INPUT','ICL_CANONICAL_NAB_INPUT']},
 {'endpoint':'GlobalTheory.GoodLat.Obj.mkFull_of_tie and mLat_of_tie','claim':'ICL21','conclusion':'Original MKFull and every face/every Boolean MLat','remaining_input_ids':['ICL_PRINCIPAL_CHART_INPUT','ICL_LEVEL_SYSTEM_INPUT','ICL_RAW_GAUSSIAN_INPUT','ICL_SHORT_DICTIONARY_INPUT','ICL_RAMIFIED_JET_INPUT','ICL_CANONICAL_NAB_INPUT']},
]
boundaries=[
 'The full original LatFull producer is not unconditionally reconstructed: its spanning half still requires the six explicitly named original producer inputs, uniformly over every row and needed weight.',
 'The principal-chart, actual common IsSystem, raw Gaussian identity/reproducing estimates, short-rule gluing/dictionary and ramified jet/class-bound producers are not reclassified as published foundations.',
 'The constructed identity cover does not supply higher CoversAt, including arbitrary tuple cover and phase-rescaling laws.',
 'All-tuple ClsEx, one PointIdentCore chosen before every tuple record, and base ClassSumsSpan remain outside this packet.',
 'The original common field, embeddings, Hermitian forms, metric, measure and phase family are fixed; no outer common-family existence or GroupCompatibilityFamily is inferred.',
 'Eta agreement, stronger second division law, DESIGN_CHOICES_COMMON and BASE_THETA_RATIONAL_TESTS remain open.',
 'No quantitative CMPt.Good, uniform CM radius, global point-height estimate, RH or GRH is asserted.',
]
contract={
 'schema':'rh-human-component-contract/1','artifact_version':VERSION,'component':COMPONENT,'source_commit':PIN,'proof_file_sha256':main_sha,
 'claims':'ICL1-ICL21','claim_count':21,'completed_source_endpoints':completed,'conditional_original_endpoints':conditional,
 'main_outcome':'Actual finite generation of the entire original integral cusp lattice; exact remaining-input implications through literal LatFull and both Boolean MLat levels.',
 'quantifier_order':['Fix the original D,T,Q,c,l, embedding, metric, measure and phase family.','For each original row and each dominant weight, construct separating integral evaluations.','For each nonzero section choose one finite auxiliary number field and integral frame before varying every section in the lattice and every finite-place completion.','Choose a finite separating family before asserting finite generation of the whole lattice.','For the conditional spanning half require each original named producer at every row and needed stable exponent.','For each short generator choose its single scalar A_w beta_H before every original complete-DVR test.','Use the original FWTie map for every face and both Boolean levels.'],
 'finite_generation_scope':'All original dominant weights, even without spanning; full supLat rather than a finite-index sublattice. The CM point is qualitative and its frame is truly integral at every completion.',
 'ramified_integrality_scope':'Whole saturated Lie eigenspace kernels commute with flat extension. No direct-sum splitting of the total integral Lie lattice at ramified primes is assumed. Integral theta generator and original rigidifications are retained.',
 'field_scope':'The coefficient number field K and common field LL never change. Finite number fields used for evaluation are allowed by literal FromTest/IntFr/valSet and map through the given inclusion.',
 'identity_cover_scope':'pd=1, l2=l, X2=X, c2=c, r=m=id, c_delta=phi_delta=1, zero half quotients, root order1 and 3 not dividing pd.',
 'spanning_scope':'Only the complete conditional implication from original raw producers is claimed; their existence on the common family remains a frontier.',
 'source_normalizations':{'stable_power':'q=4([E:Q]r)+4','normalized_valuation':'ord_V/e, preserved as ord_Vprime/(b e)','operator':'C(L,M) with original positive class weights and unmodified Lebesgue measure','denominator':'rad(condN)^(abs(disc E)*DF) * M^DF * c0 * beta_H','degree':'DF=sum_tau sum_i a(tau,i), a natural number','transport':'literal original FWTie iota_i and both b=false,true'},
 'retained_input_ids':[x['id'] for x in foundations],'not_supplied':boundaries,'whole_obligations_closed':[],
 'non_premise_references':[{'location':'packet introduction and concluding scope paragraphs','references':['RTG'],'reason':'Historical geometric frontier description; only RTG22 and RTG23 are actual numbered proof premises.'}],
}
manifest={'schema':'rh-source-manifest/1','artifact_version':VERSION,'component':COMPONENT,'source_commit':PIN,'files':list(files.values()),'ranges':list(sources.values()),'all_files_equal_pinned_git_blobs':True,'file_count':len(files),'range_count':len(sources)}
prov={'schema':'rh-human-component-provenance/1','artifact_version':VERSION,'component':COMPONENT,'source_commit':PIN,'proof_file_sha256':main_sha,'main_tex_sha256':main_sha,'status':status,'claims':claims,'source_groups':sources,'inherited_human_inputs':inherited,'classical_and_foundational_inputs':foundations,'independent_reviews':reviews,'dependency_convention':'depends_on contains only numbered written human claims; all classical foundations, original data and unproved producer premises have separate external_input_ids with explicit kinds.','source_proof_is_not_human_proof':True,'root_ledger_modified':False,'frozen_artifacts_modified':False}
closure={'schema':'rh-human-component-closure/1','artifact_version':VERSION,'component':COMPONENT,'source_commit':PIN,'proof_file_sha256':main_sha,'status':status,'completed_source_endpoints':completed,'conditional_original_endpoints':conditional,'whole_obligations_closed':[],'proposed_global_frontier_leaf_closures':[],'remaining':boundaries,'foundation_retention_explicit':True,'all_original_tests_retained':True,'all_positive_weights_retained':True,'both_Boolean_MLat_levels_retained':True,'full_LatFull_unconditional_supplier_closed':False,'independent_reviews':reviews,'pending_independent_review':sorted(set(lookup)-reviewed),'validation':'Two-pass standalone draft TeX; no PDF and no Lean replay; hash-bound mathematical reviews as listed.'}
for name,obj in [('provenance.json',prov),('source_manifest.json',manifest),('contracts.json',contract),('original_contracts.json',contract),('closure.json',closure),('retained_foundations.json',foundations)]:
    (HERE/name).write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n')
(HERE/'source_excerpts.txt').write_text('\n\n'.join(excerpts))
report=[
 'INTEGRAL CUSP LATTICES ON THE ORIGINAL GEOMETRIC FAMILY — v0.46',
 'Source pin: '+PIN,'Proof SHA256: '+main_sha,
 f'Claims:21; source files:{len(files)}; exact source ranges:{len(sources)}.',
 'Status: '+status,'',
 'Actual new producer: ICL8 proves finite generation of the whole original supLat at',
 'every dominant weight. Qualitative rational CM flags, one globally good-reduction',
 'abelian model after finite extension, saturated integral Lie eigenspaces, principalized',
 'section/eigenspace modules and dense integral frames give genuine integral separating',
 'evaluations. A finite descending-kernel argument proves finiteness without assuming',
 'spanning or saturation. No denominator depends on the section being evaluated.',
 '',
 'ICL11 constructs the literal identity cover. ICL12-18 write the full Neumann-inverse,',
 'free orbit unfolding, coefficient descent and explicit global denominator implications',
 'with the original class weights, field, measures, phases and all finite-place tests.',
 'ICL19-21 then prove the exact positive-weight FullAt/FullLat, all-row LatFull, canonical',
 'weight and original FWTie -> MKFull -> both Boolean MLat consequences.',
 '',
 'The full spanning producer remains conditional on the named original principal-chart,',
 'canonical connection, level-system, raw Gaussian, short-rule dictionary/gluing and',
 'ramified jet producers. Those premises are quantified over every original row/weight',
 'needed by the power argument and are explicitly NOT relabelled as published inputs.',
 '',
 'No whole selected RH/GRH obligation is closed. In particular DESIGN_CHOICES_COMMON,',
 'BASE_THETA_RATIONAL_TESTS, higher CoversAt, all-tuple ClsEx, PointIdentCore and',
 'base ClassSumsSpan remain. Neither eta agreement nor the stronger second division',
 'law nor the outer common-family choice order is inferred.',
 '',
 'Rebuild: python build_metadata.py --repo /path/to/formal_source',
 'Validate: python validate_tex.py --format /path/to/project/pdflatex.fmt',
 'The builder verifies every source file against the pinned git blob, hashes every',
 'source range and human claim, and binds the immutable RTG22/RTG23 proof blocks.',
 'No common metadata, frozen proof or formal source was changed.',
]
(HERE/'report.txt').write_text('\n'.join(report)+'\n')
hashes={p.name:sha(p.read_bytes()) for p in sorted(HERE.iterdir()) if p.is_file() and p.name!='hashes.json'}
(HERE/'hashes.json').write_text(json.dumps({'artifact_version':VERSION,'component':COMPONENT,'hashes':hashes},indent=2)+'\n')
print(json.dumps({'component':COMPONENT,'claims':len(claims),'source_files':len(files),'source_ranges':len(sources),'proof_file_sha256':main_sha,'status':status},indent=2))
