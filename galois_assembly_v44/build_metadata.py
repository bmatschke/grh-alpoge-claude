#!/usr/bin/env python3
"""Rebuild only the GUA component's source-pinned reconstruction metadata."""
from pathlib import Path
import argparse
import hashlib
import json
import re
import subprocess

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
PIN = '7cbf7a0c32fca1badf05931879a37c3f8a2b03b4'
ap = argparse.ArgumentParser()
ap.add_argument('--repo', type=Path, required=True)
repo = ap.parse_args().repo.resolve()
sha = lambda b: hashlib.sha256(b).hexdigest()
AV = 'src/Development/AutomorphicArithmetic/AutomorphicVarieties/'
FR = 'src/Development/AutomorphicArithmetic/Foundations/'
AL = AV+'ModularityArgument/AutomorphyLifting/'
UG = AL+'UnitaryGaloisFamilies/'
DT = AV+'ModularityArgument/ThresholdArguments/DenseThresholdCases/'
BR = AV+'BuildingsResidueChars/'
AB = 'src/Development/AbelianVarietyTheory/'
IP = AB+'Proofs/InertiaEigenvalues/'
specs = {
 'target': (AL+'GalUnitaryT.lean',18,93,'Gd/WDT/CmpT/ParAtT/LocGlobT/HasHTAt and the complete GalUnitaryT'),
 'interfaces': (UG+'IrrCaseT.lean',19,None,'CompatG, GdLaws, PlainGd, SumHTAt, SumTwoG, SumFamG, PolG, HalfG, ProdT, SpehT, RecTotT, FrobTotT, IrrCaseT'),
 'literature': (DT+'LitAut.lean',12,63,'Original LitLocAlt and LiteratureRankNHypothesis, including aut.gal=RowT and aut.bc'),
 'row_alias': (AL+'WeakOfAtt.lean',47,47,'RowT is Row0b applied to the full IsRecT predicate'),
 'row_fields': (FR+'GaloisRepresentations/TypeConditions/WeightsConjBis.lean',17,88,'IsQpBig, AwayB, AboveB, PropsB, Row0b: full retained attachment hypothesis'),
 'tor': (FR+'GaloisRepresentations/TypeConditions/WeightsConjAlt.lean',23,29,'Tor is the original commutator characteristic-polynomial condition'),
 'rect': (FR+'LocalLanglands/IsRecTOfIsRec.lean',20,87,'Good/Toral/LawsT/IsRecT; every original correspondence and its Artin map'),
 'rect_exists': (FR+'LocalLanglands/LocalCentralUnits/RecTExists.lean',20,None,'Retained full IsRecT existence/nonvacuity foundation'),
 'artin': (AB+'PublishedTheorems/AutomorphicForms₂/HasExponentZeroIff.lean',145,156,'IsLocalArtin and ord(a(g))=-deg(g)'),
 'alg_norm': (AB+'PublishedTheorems/GaloisCohomology₂/GaloisRepOfPolarizedCuspidal.lean',24,26,'algNorm = nu((1-n)/2)'),
 'totals': (AV+'AutomorphicForms/GuDefs.lean',22,158,'Actual Par, cl, ex, totPar, satTot and original assembly interfaces'),
 'frob_att': (AV+'AutomorphicForms/BlochKatoSelmerVanishes.lean',69,82,'FrobEig/algSat/AttachedSys/AttC; geometric inverse of every arithmetic Frobenius'),
 'pairing': (AV+'AutomorphicForms/IsAlgChar.lean',41,54,'IsConjEl and literal IsPairing matrix identity'),
 'cusp_pair': (AB+'Definitions/GaloisGeometry/DualIsConjByOne.lean',27,55,'Paired finite/compact/Lie identities, DualIsConj and PolarizedPair'),
 'half_polarization': (AB+'Proofs/IwasawaDecomposition/IsPolarizedTwistAbsPow.lean',195,236,'resReal, norm pullback identity and exact quadratic-sign polarization of an absolute-value twist'),
 'polg': (DT+'GuPolG.lean',20,None,'Original RowT toral-branch consumer polG_of_printsH_of_rT'),
 'half': (UG+'HalfG.lean',12,None,'Original HalfG producer and s=(e+a-1)/2 calculation'),
 'plain_def': (AB+'Definitions/GaloisGeometry/CyclicStrongAtCusp.lean',18,31,'Unlinked and PlainTor literal support definition'),
 'plain': (UG+'PlainGd.lean',14,None,'Original plainGd and its singleton principal-series proof'),
 'prod': (IP+'IsLanglandsClassificationAddOfIrreducibleProduct.lean',1,None,'Original multisegment union argument for irreducible products'),
 'speh': (DT+'GuSpehT.lean',1,None,'Original generic-unitary ordered-segment proof of SpehT'),
 'precedence': (IP+'UnitarisableSegmentTwistPrecedesAddOneLe.lean',24,None,'Central-character norm identity and x+1<=y precedence bound'),
 'rec_total': (UG+'RecTotT.lean',1,None,'Original RecTotT and exact exponent ex/2'),
 'weight_def': (AB+'PublishedTheorems/GaloisCohomology₂/BaseChangeDefiniteUnitary.lean',125,144,'IsUnramU, HasWeightAt, infOfWeight with the actual cEmb map'),
 'weight_existence': (AB+'Proofs/IwasawaDecomposition/ExistsUniqueWeightDefiniteUnitaryAt.lean',29,103,'Actual finite infinity-orbit construction and evaluation-continuity argument'),
 'strings': (BR+'SpehParameterStrings.lean',1,None,'Exact Strings producer; integral exponents and multiset identity'),
 'period_models': (AB+'Definitions/AutomorphicMembership/FiniteDimensionalWdSpace.lean',181,244,'IsModel, IsdRAt, IsPstAt, IsInduced, IsJumpsAt and wdAt'),
 'tied_period': (AV+'PadicHodgeTheory/FiniteCohomology.lean',74,84,'Original chosen Loc.PP/AIP and tiedP witness'),
 'wd_monodromy': (AB+'Definitions/AutomorphicMembership/WeilDeligneParamMonodromyEqZeroIff.lean',340,382,'Actual IsWDOfWith/IsWDOf/wdOf and its monodromy/Frobenius semisimplification'),
 'monodromy_open': (AB+'Definitions/AutomorphicMembership/WeilDeligneParamMonodromyEqZeroIff.lean',78,82,'IsMonodromy includes equality with exp(tN) on an open inertia subgroup'),
 'frob_ss': (AB+'Definitions/AutomorphicMembership/CharpolyEqOfIsNilpotentSub.lean',92,104,'Literal IsFrobSS commuting nilpotent difference and equality on semisimple inertia matrices'),
 'sum': (DT+'GuSumTwoG.lean',17,None,'Original common-coefficient, split-period and sumTwoG producer'),
 'sum_ht': (UG+'SumHTAt.lean',1,None,'Original all-bridge/all-embedding sumHTAt producer'),
 'spherical_singletons': (IP+'SphericalSatakeEqLanglandsQuotientUnramified.lean',24,None,'Langlands exhaustion, spherical segment factors, singleton support identification'),
 'spherical_segment': (IP+'SphericalSegmentRepLengthOneUnramified.lean',43,None,'Actual proof that a spherical segment is length1 and an unramified character'),
 'spherical_cusp': (IP+'IsUnramifiedCharOfCuspidalSpherical.lean',23,None,'Spherical supercuspidal has unramified rank-one support'),
 'determinant_quotient': (IP+'IsLanglandsClassificationDetCharacter.lean',25,None,'Embedding of determinant character and dual quotient of descending singleton induction'),
 'satake_law': (AL+'PolarizedLinkage/ExtraV.lean',59,111,'Universal IsRecT product and spherical laws from original local foundations'),
 'sat_local': (DT+'TSatLoc.lean',11,None,'Local/global Satake transfer on an isotypic actual representation'),
 'frob_total': (DT+'GuFrobTotT.lean',25,None,'Exact total-parameter Frobenius eigenvalues and all-valuation inertia statement'),
 'component_unique': (BR+'BuildingComponentUniqueness.lean',12,None,'Split local inclusion, centralizer factor and original component uniqueness'),
 'sat_conj': (BR+'SatakeParametersComplexConjugate.lean',11,None,'CSD Satake inversion and k -> d-1-k'),
 'pol_frob': (BR+'TwistedDualFrobeniusCompatibility.lean',1,None,'Original cyclotomic exponent1-n and matrix-pairing assembly'),
 'chebotarev': (DT+'TIsoOfFrob.lean',11,None,'Density of degree-one Frobenius classes and continuous coefficient/Brauer-Nesbitt consumer'),
 'irr_case': (DT+'GuIrrCaseT.lean',15,None,'All six cuspidal output fields, including every unramified and split local place'),
 'assembly': (DT+'Assemble.lean',20,None,'Original complete assembly_s, including strong all-unramified spherical input'),
 'gal_wrapper': (DT+'GalUnitaryT.lean',18,43,'Original half/recTotal wrappers and GalUnitaryT assembly'),
 'guwrap': (DT+'GuWrap.lean',18,24,'Original spehOf_alt, galUnitaryT_of_printsH and separately retained endShape endpoint'),
 'row_identity': (FR+'GaloisRepresentations/RankTwoPatching/GaloisRepExistsTotallyRealGL2.lean',60,60,"rowOf' is the identity on RowT"),
}
files, sources, excerpts = {}, {}, []
for sid,(rel,start,end,decl) in specs.items():
    data = (repo/rel).read_bytes()
    pinned = subprocess.run(['git','show',PIN+':'+rel],cwd=repo,check=True,
                            stdout=subprocess.PIPE).stdout
    assert data == pinned, rel
    lines = data.splitlines(keepends=True)
    end = end or len(lines)
    assert 1 <= start <= end <= len(lines), (sid,start,end,len(lines))
    block = b''.join(lines[start-1:end])
    url = f'https://github.com/CocoSgt/riemann-hypothesis-lean/blob/{PIN}/{rel}'
    files[rel] = {'path':rel,'sha256':sha(data),'bytes':len(data),
                 'line_count':len(lines),'verified_equal_to_pinned_git_blob':True,'url':url}
    sources[sid] = {'id':'GUA_SRC_'+sid.upper(),'path':rel,'declaration':decl,
        'line_start':start,'line_end':end,'source_commit':PIN,
        'full_file_sha256':sha(data),'range_sha256':sha(block),'range_bytes':len(block),
        'verified_equal_to_pinned_git_blob':True,'url':url+f'#L{start}-L{end}'}
    excerpts.append(f'[{sources[sid]["id"]}] {decl}\n{url}#L{start}-L{end}\n'+block.decode())

external = [
 {'id':'GUA_ORIGINAL_LITERATURE','kind':'inherited_original_hypothesis','classification':'inherited',
  'source':sources['literature'],
  'statement_used':'Original HypothesesH prime -> litN. Local Bernstein-Zelevinsky finiteness/admissibility, normalized induction and duality, support and multisegment uniqueness/exhaustion, geometric lemma, standard cosocle and square-integrable segment theorems remain the literal classical local foundations. Global Gelfand-Kazhdan duality is retained.',
  'newly_reconstructed':False},
 {'id':'GUA_ORIGINAL_ROWT','kind':'inherited_original_hypothesis','classification':'inherited',
  'source':sources['row_fields'],'alias_source':sources['row_alias'],
  'statement_used':'For every CM E, algebraic closure, prime ell, iota, a>=1, regular algebraic original cusp and Hecke character of E+ satisfying the literal PolarizedPair, Row0b(IsRecT) produces continuous semisimple r, integer wt and HT with every PropsB field. AboveB quantifies every tied local period model, valuation, ring, bridge and induced embedding. Only its Tor-and-mono0 branch is used.',
  'unused_branch':'The IsQpBig/tame/squarefree alternative and its rank-dependent prime bound are not used.',
  'newly_reconstructed':False},
 {'id':'GUA_RECT_NONVACUITY','kind':'inherited_source_foundation','classification':'inherited',
  'source':sources['rect_exists'],
  'statement_used':'For every original E/Omega/A/w/h there exists an rc satisfying the full original IsRecT, not a weakened unramified-only predicate.',
  'newly_reconstructed':False},
 {'id':'GUA_PERIOD_AND_MONODROMY','kind':'inherited_source_foundation','classification':'inherited',
  'sources':[sources['tied_period'],sources['period_models'],sources['wd_monodromy']],
  'statement_used':'The original tied Loc.PP period model and its field-valued de Rham/semistable modules; the away-ell local monodromy theorem and IsWDOf construction. GUA10 proves the direct-sum and coefficient-enlargement consequences actually used, without claiming production of these entire foundations.',
  'newly_reconstructed':False},
 {'id':'GUA_CLASSICAL_CHEBOTAREV','kind':'retained_classical_input','classification':'A',
  'source':sources['chebotarev'],
  'statement_used':'For a number field, arithmetic Frobenius conjugacy classes outside any fixed finite set are dense in its absolute Galois group; the original stronger degree-one version suffices.',
  'application_checked':'GUA16 applies this to continuous characteristic-polynomial coefficient functions on the same profinite G_E and then to finite-dimensional semisimple representations.',
  'newly_reconstructed':False},
 {'id':'GUA_ELEMENTARY_COMPACT_ANALYSIS','kind':'retained_general_foundation','classification':'A',
  'statement_used':'Haar averaging on compact groups, Stone-Weierstrass for a self-conjugate separating algebra of continuous functions, and elementary compact-induction/Hecke adjunction. GUA9 proves the needed compact U(n) highest-weight consequence from these and HP4; GUA12 proves spherical uniqueness from the actual Hecke idempotent.',
  'newly_reconstructed':False},
]
relations = {
 1:([],['target','tor','interfaces']),
 2:([1],['plain_def','plain','rect','alg_norm']),
 3:([],['prod','rect','interfaces']),
 4:(['BCS8'],['precedence','speh']),
 5:([3,4,'BCS5'],['speh','rect','interfaces']),
 6:([3,5],['rec_total','totals','alg_norm']),
 7:([],['row_alias','row_fields','polg','cusp_pair','target']),
 8:([7],['half','half_polarization','rect','alg_norm']),
 9:(['HP4'],['weight_def','weight_existence','strings']),
 10:([1,'ADK1'],['sum','sum_ht','period_models','wd_monodromy','interfaces']),
 11:([8,9,10,'BCS18'],['assembly','strings','totals']),
 12:(['BCS14','BCS15'],['spherical_singletons','spherical_segment','spherical_cusp','determinant_quotient','satake_law','rect','artin']),
 13:(['ITA10','BCS15','BCS19'],['sat_local','assembly']),
 14:([1,11,12,13],['frob_total','frob_att','totals','wd_monodromy','monodromy_open','frob_ss']),
 15:([2,6,11,'ITA10','BCS18'],['component_unique','target','assembly']),
 16:([11,13,14],['sat_conj','pol_frob','chebotarev','pairing']),
 17:([7,9,11,13,14,15,'BCS18'],['irr_case','frob_att','cusp_pair','target']),
 18:([11,14,15,16,17,'BCS18','BCS19'],['target','assembly','gal_wrapper','guwrap','row_identity','literature']),
}
ext_uses = {
 2:['GUA_ORIGINAL_LITERATURE'],3:['GUA_ORIGINAL_LITERATURE'],
 4:['GUA_ORIGINAL_LITERATURE'],5:['GUA_ORIGINAL_LITERATURE'],
 7:['GUA_ORIGINAL_LITERATURE','GUA_ORIGINAL_ROWT','GUA_RECT_NONVACUITY','GUA_PERIOD_AND_MONODROMY'],
 8:['GUA_ORIGINAL_LITERATURE'],9:['GUA_ELEMENTARY_COMPACT_ANALYSIS'],
 10:['GUA_PERIOD_AND_MONODROMY'],
 12:['GUA_ORIGINAL_LITERATURE','GUA_ELEMENTARY_COMPACT_ANALYSIS'],
 14:['GUA_RECT_NONVACUITY','GUA_PERIOD_AND_MONODROMY'],
 16:['GUA_CLASSICAL_CHEBOTAREV'],17:['GUA_ORIGINAL_LITERATURE'],
 18:['GUA_ORIGINAL_LITERATURE','GUA_ORIGINAL_ROWT'],
}
text = (HERE/'main.tex').read_text()
main_sha = sha(text.encode())
claims = []
local_ids = {'GUA'+str(n) for n in relations}
root_ids = set(json.loads((ROOT/'provenance.json').read_text())['mathematical_dependency_graph'])
peer_ids = set(re.findall(r'% BEGIN (BCS\d+)\n',(ROOT/'base_change_v44/main.tex').read_text()))
ext_ids = {x['id'] for x in external}
for n,(deps,groups) in relations.items():
    cid = 'GUA'+str(n)
    m = re.search(r'% BEGIN '+cid+r'\n.*?% END '+cid+r'\n',text,re.S)
    assert m,cid
    block = m.group()
    title = re.search(r'\\paragraph\{'+cid+r'\. (.*?)\}\n',block).group(1)
    dep_ids = ['GUA'+str(d) if isinstance(d,int) else d for d in deps]
    assert set(dep_ids) <= root_ids | peer_ids | local_ids, (cid,dep_ids)
    assert not set(dep_ids) & ext_ids,(cid,dep_ids)
    assert set(ext_uses.get(n,[])) <= ext_ids,cid
    start = text[:m.start()].count('\n')+1
    claims.append({'id':cid,'title':title,'introduced_in':'0.44','classification':'B',
       'status':'complete_at_stated_scope_pending_independent_review',
       'depends_on':dep_ids,'external_input_ids':ext_uses.get(n,[]),
       'proof_location':{'file':'galois_assembly_v44/main.tex','label':'claim:'+cid,
         'line_start':start,'line_end':start+block.count('\n')-1,
         'sha256':sha(block.encode()),'bytes':len(block.encode())},
       'sources':[sources[g] for g in groups],
       'scope':'Exact original objects, normalizations and universal quantifiers; GUA18 retains the original RowT/base-change/local foundations and allows every n>=1 and ell=3.',
       'source_proof_is_not_human_proof':True})

inputs=[]
for component,filename,ids,kind in [
 ('chain_closure_core','main.tex',['HP4'],'immutable_inherited_human_proof'),
 ('conditional_main_v42','adjoint_matching.tex',['ADK1'],'immutable_inherited_human_proof'),
 ('integral_type_v43','main.tex',['ITA10'],'immutable_inherited_human_proof'),
 ('base_change_v44','main.tex',['BCS5','BCS8','BCS14','BCS15','BCS18','BCS19'],'same_version_human_proof')]:
    p=ROOT/component/filename;t=p.read_text()
    for cid in ids:
        m=re.search(r'% BEGIN '+cid+r'\n.*?% END '+cid+r'\n',t,re.S)
        if not m:m=re.search(r'\\paragraph\{'+cid+r':.*?(?=\n\\paragraph\{|\Z)',t,re.S)
        assert m,(component,cid)
        inputs.append({'claim':cid,'file':component+'/'+filename,
             'file_sha256':sha(p.read_bytes()),'claim_sha256':sha(m.group().encode()),
             'kind':kind,'newly_modified_by_this_component':False})

reviews=[]
paths=list(HERE.glob('review_GUA*.json'))
rp=ROOT/'reviews_v0_44/galois_assembly_v44_root_review.json'
if rp.exists():paths.append(rp)
for p in paths:
    v=json.loads(p.read_text())
    assert v.get('result',v.get('status'))=='PASS',str(p)
    assert v.get('proof_sha256',v.get('proof_file_sha256'))==main_sha,str(p)
    original_entries=v.get('claims_reviewed',v.get('reviewed_claims',[]))
    entries=[]
    for e in original_entries:
        cid=e if isinstance(e,str) else e.get('id',e.get('claim'))
        expected=(v.get('proof_hashes',{}).get(cid) if isinstance(e,str)
                  else e.get('proof_range_sha256',e.get('block_sha256')))
        m=re.search(r'% BEGIN '+cid+r'\n.*?% END '+cid+r'\n',text,re.S)
        assert m and expected==sha(m.group().encode()),(p,cid)
        entries.append({'id':cid,'proof_range_sha256':expected})
    reviews.append({'file':str(p.relative_to(ROOT)),'sha256':sha(p.read_bytes()),
      'reviewer':v.get('reviewer'),'result':'PASS','proof_file_sha256':main_sha,
      'claims':[x['id'] for x in entries],'scope':v.get('scope')})
reviewed={c for r in reviews for c in r['claims']}
complete_review=local_ids <= reviewed
status='complete_at_stated_scope_independently_reviewed' if complete_review else 'complete_at_stated_scope_pending_independent_review'
for c in claims:
    c['status']='complete_at_stated_scope_independently_reviewed' if c['id'] in reviewed else status
    c['independent_review_files']=[r['file'] for r in reviews if c['id'] in r['claims']]
contracts={
 'schema':'rh-galois-assembly-contract/1','component':'galois_assembly_v44','artifact_version':'0.44',
 'source_commit':PIN,'proof_file_sha256':main_sha,'endpoint_claim':'GUA18',
 'original_endpoint':'UpperTheory.V.Z.Win.GalUnitaryT',
 'original_producer':'UpperTheory.V.Z.Win.Gu.galUnitaryT_of_printsH',
 'inputs':{'base_change':'BCS18 and BCS19: one set of witnesses and its all-IsUnramU consequence',
   'attachment':'Full original RowT/PropsB, separately retained as GUA_ORIGINAL_ROWT',
   'local_generic_unitary':'BCS8 is the one shared checked published application; GUA4 proves its needed ordering consequence'},
 'hypotheses':['E is CM and finite-unramified over E+','same specified algebraic closure Omega',
   'ell is prime and ell !=2, including3','given iota:Qbar_ell~=C with no complex continuity premise',
   'n>=1, unrestricted relative to ell or local primes','actual original IsAutRepU subspace sigma'],
 'actual_output':'One R:G_E->GL_n(Qbar_ell) and one integer multiset H_tau, constructed as ordered blocks r_ik and transported by sum_i d_i*a_i=n.',
 'normalizations':{'algNorm':'tau nu^((1-rank tau)/2)',
   'Speh_local':'sum_k rc(rho_i)((d_i-1)/2-k)',
   'total_exponent':'e_ik/2=(d_i-2k-n)/2',
   'HalfG_twist':'s=(e+a-1)/2 on the actual automorphic cusp; no Galois square root is selected',
   'HT':'-z-e_ik/2 and total (n-1)/2-infOfWeight',
   'geometric_Frobenius':'q_w^((n-1)/2)*alpha*q_w^(k-(d_i-1)/2)',
   'pairing_multiplier':'epsilon^(1-n)'},
 'universal_quantifiers':['every IsUnramU place away ell, every valuation above it, every inertia element',
   'every infinity weight witness','every split place and every actual local component',
   'every A,h and rc satisfying the full IsRecT','every original coefficient ring, LocBridge and Induces witness',
   'every finite coefficient extension and inducing embedding in HasHTAt',
   'every complex conjugation with literal IsConjEl',
   'all six irreducible-to-cuspidal fields, including Satake at all IsUnramU places even over ell'],
 'conditional_local_scope':'CmpT compares actual WD only when Gd=Tor and mono0; HasHTAt follows under original PlainTor. These guards are preserved.',
 'subcontracts':[{'id':k,'claim':c} for k,c in [('PlainGd','GUA2'),('ProdT','GUA3'),('SpehT','GUA5'),
   ('RecTotT','GUA6'),('PolG','GUA7'),('HalfG','GUA8'),('Strings','GUA9'),('SumFamG','GUA10'),
   ('spherical_IsRecT','GUA12'),('FrobTotT','GUA14'),('all_split_LocGlobT','GUA15'),
   ('PolOfFrob_consumer','GUA16'),('IrrCaseT','GUA17'),('GalUnitaryT_GuWrap','GUA18')]],
 'retained_foundations':[x['id'] for x in external],
 'not_claimed':['production of original RowT','production of BaseChangeIsobaricN',
   'production of RecTExists or the entire tied period model','unconditional all-rank automorphy lifting',
   'purity','all Speh lengths1 without irreducibility','the separate cofinite strict-ratio endShape endpoint',
   'full RH/GRH reconstruction']}
provenance={'schema':'rh-human-component-provenance/1','component':'galois_assembly_v44',
 'artifact_version':'0.44','source_commit':PIN,'date':'2026-11-23','proof_file_sha256':main_sha,
 'status':status,'claims':claims,'inherited_human_inputs':inputs,
 'classical_and_foundational_inputs':external,'independent_reviews':reviews,
 'dependency_convention':'depends_on contains only numbered human claims. External foundations are in external_input_ids; peer BCS inputs carry exact block hashes.',
 'source_proof_is_not_human_proof':True,'root_ledger_modified':False,'v42_v43_artifacts_modified':False}
closure={'schema':'rh-human-component-closure/1','component':'galois_assembly_v44',
 'artifact_version':'0.44','source_commit':PIN,'proof_file_sha256':main_sha,'status':status,
 'closed_subcontracts':contracts['subcontracts'],'new_global_frontier_leaf_closures':[],
 'foundation_retention_explicit':True,'independent_reviews':reviews,
 'validation':'Two-pass draft TeX on the full chapter; no Lean replay. Independent mathematical/source review is separately hash-bound.',
 'pending':[] if complete_review else ['independent mathematical/source review of all GUA1-GUA18']}
manifest={'schema':'rh-source-manifest/1','component':'galois_assembly_v44','source_commit':PIN,
 'files':list(files.values()),'ranges':list(sources.values())}
for name,value in [('contracts.json',contracts),('provenance.json',provenance),('closure.json',closure),
                   ('source_manifest.json',manifest),('retained_foundations.json',external)]:
    (HERE/name).write_text(json.dumps(value,ensure_ascii=False,indent=2)+'\n')
(HERE/'source_excerpts.txt').write_text('\n\n'.join(excerpts))
(HERE/'report.txt').write_text('''GALOIS ASSEMBLY v0.44

Outcome: GUA1-GUA18 reconstruct the literal GalUnitaryT and GuWrap producer
at the original retained foundations. One actual representation and one HT
family satisfy every field, with every IsRecT and LocBridge quantifier.
The packet includes HalfG, finite period sums, RecTotT, FrobTotT, plainGd,
all original unramified places, pairing epsilon^(1-n), and all cuspidal fields.

Substantive new proof: local parameter identities; direct-sum period and
monodromy comparisons; exact half-normalization and infinity arithmetic;
spherical singleton Langlands deduction; actual block construction; dense
Frobenius pairing; irreducible-to-actual-cusp recovery. The written compact
U(n) argument derives the needed highest-weight occurrence from HP4.

Shared published input: BCS8 matches only the local generic unitary
decomposition of Moeglin-Waldspurger I.10-I.11. GUA4 uses that same numbered
claim, so there is no second hidden classification foundation.

Retained inputs: full original RowT/PropsB, BCS18-19 and its retained original
BaseChangeIsobaricN, classical local foundations, full RecTExists, the original
tied period and local monodromy foundations, and Chebotarev. Their exact
source pin/ranges/hashes and used statements are in retained_foundations.json.
No production of these foundations, purity, unrestricted automorphy lifting,
separate endShape, or completion of RH/GRH is claimed.

Validation: run validate_tex.py with the project pdflatex format; rebuild
metadata with build_metadata.py --repo /path/to/pinned/formal_source.
No frozen v0.42/v0.43 files, source files, or common ledgers were modified.
'''+f'\nSource pin: {PIN}\nMain SHA256: {main_sha}\nStatus: {status}\n')
hashes={p.name:sha(p.read_bytes()) for p in sorted(HERE.iterdir()) if p.is_file() and p.name!='hashes.json'}
(HERE/'hashes.json').write_text(json.dumps({'component':'galois_assembly_v44','artifact_version':'0.44','hashes':hashes},indent=2)+'\n')
print(json.dumps({'component':'galois_assembly_v44','claims':len(claims),
 'source_files':len(files),'source_ranges':len(sources),'status':status,'main_sha256':main_sha},indent=2))
