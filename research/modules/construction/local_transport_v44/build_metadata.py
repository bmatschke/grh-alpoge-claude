#!/usr/bin/env python3
"""Bind the complete written local-transport packet to the unchanged source pin."""
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
ap.add_argument('--repo', required=True, type=Path)
repo = ap.parse_args().repo.resolve()
sha = lambda data: hashlib.sha256(data).hexdigest()
B = 'src/Development/AutomorphicArithmetic/AutomorphicVarieties/'
H = B+'HeckeAlgebras/'
O = H+'OrdinaryHeckeCharacters/'
D = B+'ModularityArgument/ThresholdArguments/DenseThresholdCases/'
C = B+'BuildingsResidueChars/'
A = 'src/Development/AbelianVarietyTheory/'
I = A+'Proofs/IwasawaDecomposition/'
specs = {
 'scalar_definitions':(H+'IsTheta.lean',191,208,'infRep, toForm, IsBasis and literal YOf'),
 'group_levels':(H+'IsTheta.lean',67,145,'cmp, Ub, toKT, locA, sec, QData, UQ and actual hset'),
 'big_and_actions':(H+'CoefficientRepTrivialOnUnramified.lean',179,189,'tauC, Big, atV and atW'),
 'isotypic_definition':(H+'CoefficientRepTrivialOnUnramified.lean',71,74,'literal IsoSum'),
 'automorphic_definitions':(A+'PublishedTheorems/GaloisCohomology₂/BaseChangeDefiniteUnitary.lean',90,141,'infU/locU/embU/RU/IsAutFormU/IsAutRepU/IsCompAlong/IsUnramU/HasWeightAt'),
 'membership':(O+'PartUR2MemSpan.lean',11,48,'partUR2Mem_span and full partUR2Mem'),
 'local_section':(I+'SplitPlaceUnitaryLocalPointsEquivGL.lean',1,None,'actual split coordinate equivalence; reused through FNL5'),
 'restriction_isotypic':(C+'IsoSumRestrictionOfLocalComponentUnitary.lean',11,None,'isoSum_restriction_of_local_component_unitary'),
 'family_isotypic':(C+'IsoSumOfInjectiveEquivariantFamily.lean',10,None,'isoSum_of_injective_equivariant_family'),
 'opposite_compact':(C+'MemMaximalCompactOfUnderEq.lean',11,None,'mem_maximalCompact_of_under_eq; exact opposite-place inverse conjugate transpose'),
 'double_coset_definition':(H+'ContinuousTorusCharacter.lean',14,18,'fixd and representation-independent chosen representatives in dc'),
 'spherical_definition':(H+'Distinct.lean',41,43,'sphOp as original unnormalized dc at al(n,j)'),
 'abstract_local':(O+'MemCongruenceSubgroupIff.lean',17,107,'congruence compactness and all four partUR2Abs clauses'),
 'at_l':(O+'InfRepFin.lean',12,71,'actual coordinates, infRep_fin and full partUR2AtV'),
 'iso_l':(O+'PartUR2IsoL.lean',17,92,'stability, finite family, and full partUR2IsoL'),
 'at_away':(O+'PartUR2AtW.lean',13,123,'sec_eq/toKT_sec and full partUR2AtW'),
 'iso_q':(O+'PartUR2IsoQ.lean',17,78,'raF_big, big_atW and full partUR2IsoQ'),
 'base_fix':(O+'PartUR2Fix.lean',16,86,'actual away projection and full matrix-valued partUR2Fix'),
 'spherical_transport':(O+'PartUR2Sph.lean',17,75,'finite-sum push and full partUR2Sph'),
 'unramified':(O+'PartUR2Unr.lean',16,56,'full original partUR2Unr, with no split-place hypothesis'),
 'infinite_emb':(C+'InjectiveInfinitePlaceOfEmbAtSplitPlaces.lean',12,None,'actual-prime recovery and injective infinitePlace of Emb'),
 'tensor_factor':(C+'ExistsFactorDualEmbeddingOfNeZeroTensor.lean',4,None,'exists_factor_dual_embedding_of_ne_zero_tensor'),
 'dual_weight_definition':('src/Formalism/LocalRingCardinality/DataCoeff.lean',12,32,'DomWeight and literal reversed-negative dual'),
 'weight_intertwiner':(C+'HasWeightAtOfTensorDualIntertwiner.lean',14,None,'hasWeightAt_of_tensor_dual_intertwiner'),
 'weight_transport':(O+'WtOfForm.lean',15,72,'wt_of_form and full original partUR2Wt'),
 'v0_transport':(O+'LNotMemBasePrime.lean',16,72,'l_not_mem_base_prime and full original partUR2V0'),
 'type_product':(D+'AutomorphicTensorInductionOfLocalPlaces.lean',16,75,'neu_comm, ne_J and exact type invariant-vector consumer'),
 'type_transport':(D+'AutomorphicTensorInductionOfLocalPlaces.lean',76,114,'full original partUR2Type_alt'),
 'type_definitions':(D+'UnitaryHeckeData.lean',19,44,'IsTypeAlt, TypeForAlt and exact pushed Teichmuller characters'),
 'point_aut_record':(D+'UnitaryHeckeData.lean',45,59,'UnitaryPointProperties including exact local family/weight/unramified/v0 fields'),
 'local_component':(I+'ExistsLocCompSplit.lean',15,75,'full exists_locComp_split with admissibility and unramified iff spherical'),
 'local_component_producer':(I+'ExistsAdmissibleLocalComponentDefiniteUnitary.lean',95,162,'source admissible-local-component producer; alternate actual multiplicity-space proof in LTP19'),
 'smooth_admissible':(A+'Definitions/Foundations/SmoothPartStable.lean',73,76,'literal IsSmooth and IsAdmissible'),
 'part_u_caller':(D+'PartU.lean',43,155,'actual PartU use of all seven suppliers and simultaneous local choice'),
}
cache = {}
source_files = {}
sources = {}
for key,(rel,lo,hi,decl) in specs.items():
    if rel not in cache:
        data=(repo/rel).read_bytes()
        pinned=subprocess.run(['git','show',PIN+':'+rel],cwd=repo,check=True,stdout=subprocess.PIPE).stdout
        assert data==pinned,rel
        cache[rel]=data
    data=cache[rel]
    lines=data.splitlines(keepends=True); hi=hi or len(lines)
    assert 1<=lo<=hi<=len(lines),(key,lo,hi,len(lines))
    block=b''.join(lines[lo-1:hi])
    url=f'https://github.com/CocoSgt/riemann-hypothesis-lean/blob/{PIN}/{rel}'
    source_files[rel]={'path':rel,'sha256':sha(data),'bytes':len(data),'line_count':len(lines),
                      'verified_equal_to_pinned_git_blob':True,'url':url}
    sources[key]={'id':'LTP_SRC_'+key.upper(),'path':rel,'declaration':decl,
        'line_start':lo,'line_end':hi,'sha256':sha(data),'full_file_sha256':sha(data),
        'range_sha256':sha(block),'range_bytes':len(block),'source_commit':PIN,
        'verified_equal_to_pinned_git_blob':True,'url':url+f'#L{lo}-L{hi}'}

relations = {
 1:(['ADP7'],['scalar_definitions','membership']),
 2:(['FNL2','FNL4','FNL5','FNL6'],['local_section','opposite_compact','automorphic_definitions']),
 3:([2],['restriction_isotypic','automorphic_definitions','isotypic_definition']),
 4:(['ITA10'],['family_isotypic','isotypic_definition']),
 5:(['OHA1'],['abstract_local','double_coset_definition','spherical_definition']),
 6:([1,2,'ADP6','ADP7'],['at_l','big_and_actions']),
 7:([1,3,4,6],['iso_l']),
 8:([1,2,'ADP7','FNL5','FNL6','FNL16'],['at_away','iso_q','big_and_actions','group_levels']),
 9:([1,2,3,4,8,'FNL4'],['iso_q']),
 10:(['ADP6','ADP7'],['base_fix','group_levels','big_and_actions']),
 11:([1,3,5,8,'FNL16'],['spherical_transport','abstract_local','spherical_definition']),
 12:([1,2,10],['unramified','opposite_compact','automorphic_definitions']),
 13:(['FNL4','WRP1','HP1','HP2','HP4'],['infinite_emb','tensor_factor','dual_weight_definition','weight_intertwiner']),
 14:([1,13,'ADP7','HP2'],['weight_transport','weight_intertwiner','automorphic_definitions']),
 15:([1,2,3,5,10,'FNL4'],['v0_transport','abstract_local']),
 16:([2,10,'FNL4'],['type_product','group_levels']),
 17:([1,3,16],['type_product','type_transport','type_definitions']),
 18:([17,'ITA12'],['type_definitions','type_transport','point_aut_record']),
 19:([2,'ADP1','ADP2','PKT5','PKT6'],['local_component','local_component_producer','smooth_admissible','automorphic_definitions']),
 20:([2,3,5,19],['local_component','automorphic_definitions']),
 21:([7,9,11,12,14,15,17,18,19,20,'FNL16'],['part_u_caller','point_aut_record','local_component']),
}
tex=(HERE/'main.tex').read_text()
main_hash=sha(tex.encode())
claims=[]
for number,(deps,groups) in relations.items():
    cid=f'LTP{number}'
    m=re.search(r'^% BEGIN '+cid+r'\n.*?^% END '+cid+r'\n',tex,re.M|re.S)
    assert m,cid
    block=m.group()
    title=re.search(r'\\paragraph\{'+cid+r'\. (.*?)\}\n',block,re.S).group(1)
    start=tex[:m.start()].count('\n')+1
    retained=[]
    if number in [8,9,11]:retained.append('Original H.Ax where the source endpoint quantifies it; supplied on the actual H by FNL16.')
    if number in [12,14,15,17,18,21]:retained.append('The original YOf is nonzero; no production of nonvanishing for an arbitrary residual block.')
    if number==17:retained.append('Original supplied IsTypeAlt, for arbitrary chi; its entire every-IsRecT detecting equivalence is retained.')
    if number==18:retained.append('Original supplied TypeForAlt; ITA12 supplies it only on its explicitly retained source/classical foundations.')
    claims.append({'id':cid,'title':title,'introduced_in':'0.44','classification':'B',
       'status':'complete written proof at the full stated original scope',
       'depends_on':[f'LTP{x}' if isinstance(x,int) else x for x in deps],
       'external_input_ids':[],
       'scope':'shared RH and unrestricted Dirichlet GRH; actual unitary automorphic part and original local actions',
       'proof_location':{'file':'local_transport_v44/main.tex','label':'claim:'+cid,
          'line_start':start,'line_end':start+block.count('\n')-1,'sha256':sha(block.encode()),'bytes':len(block.encode())},
       'source_groups':groups,'sources':[sources[x] for x in groups],
       'retained_hypotheses':retained,
       'dependency_scope':'Numbered human proofs only; supplied source predicates remain explicit hypotheses. Formal acceptance is not used as a substitute for the written argument.'})

component_for={'ADP':'automorphic_decomposition_v43','FNL':'finite_levels_v42',
  'ITA':'integral_type_v43','OHA':'ordinary_hecke_algebra_v42','WRP':'weight_representation_v42',
  'HP':'chain_closure_core','PKT':'comparison_packet'}
inherited=[]
for cid in sorted({d for ds,_ in relations.values() for d in ds if isinstance(d,str)}):
    component=component_for[re.match(r'[A-Z]+',cid).group()]
    p=ROOT/component/'main.tex';t=p.read_text()
    m=re.search(r'^% BEGIN '+cid+r'\n.*?^% END '+cid+r'\n',t,re.M|re.S)
    if not m:m=re.search(r'\\paragraph\{'+cid+r':.*?(?=\n\\paragraph\{|\Z)',t,re.S)
    assert m,cid
    inherited.append({'claim':cid,'file':component+'/main.tex','file_sha256':sha(p.read_bytes()),
       'claim_sha256':sha(m.group().encode()),'line_start':t[:m.start()].count('\n')+1,
       'line_end':t[:m.end()].count('\n')+int(not m.group().endswith('\n')),
       'kind':'immutable_inherited_human_proof','newly_modified':False,
       'scope':'Only the printed scope is used. ITA12 retains its original type/correspondence foundations; FNL3/ADP2 retain the checked finite-class application.'})

completed=[
 {'endpoint':'UpperTheory.V.Hi.partUR2Mem','claim':'LTP1','scope':'Literal YOf intersection/span equals the complete scalarization predicate; no nonzero requirement.'},
 {'endpoint':'UpperTheory.isoSum_restriction_of_local_component_unitary','claim':'LTP3','scope':'Every supplied local component at a split place, by actual centralizer factorization and global irreducibility.'},
 {'endpoint':'UpperTheory.isoSum_of_injective_equivariant_family','claim':'LTP4','scope':'Arbitrary representations, a finite separating equivariant family, and literal IsoSum.'},
 {'endpoint':'UpperTheory.V.Hi.partUR2Abs','claim':'LTP5','scope':'All compact fixed-vector transfers, all spherical j, additive naturality on the full ambient representation, and compactness of every Kc(c).'},
 {'endpoint':'UpperTheory.V.Hi.partUR2AtV','claim':'LTP6','scope':'Original selected ell place, every coefficient function and functional, actual right-translation order.'},
 {'endpoint':'UpperTheory.V.Hi.partUR2IsoL','claim':'LTP7','scope':'Every supplied smooth irreducible local component at every original ell place; includes Y=0.'},
 {'endpoint':'UpperTheory.V.Hi.partUR2AtW','claim':'LTP8','scope':'Every split place outside s.S, actual conditional sec, coefficient action becomes identity exactly there.'},
 {'endpoint':'UpperTheory.V.Hi.partUR2IsoQ','claim':'LTP9','scope':'Every original auxiliary place and supplied local component, original H.Ax retained; includes Y=0.'},
 {'endpoint':'UpperTheory.V.Hi.partUR2Fix','claim':'LTP10','scope':'Every finite x satisfying all original coordinate tests; unchanged coefficient matrix and every column/functional.'},
 {'endpoint':'UpperTheory.V.Hi.partUR2Sph','claim':'LTP11','scope':'Every original split outside place, local component, j>=0, complex scalar and vector in Y; original H.Ax retained.'},
 {'endpoint':'UpperTheory.V.Hi.partUR2Unr','claim':'LTP12','scope':'Every finite place outside V.S prime, including nonsplit places, when actual Y is nonzero.'},
 {'endpoint':'UpperTheory.V.Hi.partUR2Wt','claim':'LTP14','scope':'Every original local embedding index and exact reversed-negative dual weight at fixed iota, when Y is nonzero.'},
 {'endpoint':'UpperTheory.V.Hi.partUR2V0','claim':'LTP15','scope':'Every local component at original distinguished place, exact Kc(1), when Y is nonzero.'},
 {'endpoint':'UpperTheory.V.Hi.partUR2Type_alt','claim':'LTP17','scope':'Every original chi with supplied IsTypeAlt, every local-component family and every original IsRecT map, when Y is nonzero.'},
 {'endpoint':'GlobalTheory.DefU.exists_locComp_split','claim':'LTP20','construction_claim':'LTP19','scope':'Every CM field, all n>=0, every original automorphic representation and split place; admissibility, actual component map, and exact unramified iff spherical.'},
]
boundaries=[
 'A global Galois representation attached to the automorphic constituent, and its local/global/Frobenius comparisons.',
 'Quotient descent through the original V.pr, polarization and the complete UnitaryPointProperties record.',
 'The complete PartAltAlt, AutomorphicHeckeSet and subsequent same-J Hida installation; root/peer packets may separately supply these.',
 'Nonvanishing of an arbitrary residual Hecke block; only the printed hypotheses Y!=0 are used.',
 'No new proof of the inherited crystalline type theorem, full classical LLC, RecTExists or trace-formula foundations.',
 'No whole RH/GRH or COUNT_II_SUPPORT obligation is closed by this component alone.'
]
foundation_retention=[
 {'name':'ITA12 original type/correspondence foundations','used_through':'ITA12 in LTP18',
  'introduced_here':False,'source_component':'integral_type_v43',
  'retained_external_ids':['ITA_ORIGINAL_HLIT','ITA_CLASSICAL_CRYSTALLINE_TYPE','ITA_CLASSICAL_LLC_SINGLETONS','ITA_FOUNDATION_RECT_EXISTS'],
  'scope':'The original HypothesesH/litN local package and matched classical type inputs retain their printed scope. LTP17 merely consumes the full supplied IsTypeAlt predicate.'},
 {'name':'Actual finite-class theorem already matched in FNL3/FV9','used_through':'ADP1-ADP2 in LTP19',
  'introduced_here':False,'source_component':'finite_levels_v42',
  'scope':'The inherited checked Borel finite-class application is reused, not replaced by an inference from finite volume. No new base-change/trace-formula input is asserted.'}
]
contract={'schema':'rh-local-transport-contract/1','artifact_version':'0.44','component':'local_transport_v44',
 'source_commit':PIN,'proof_file_sha256':main_hash,'claim_count':21,'claims':'LTP1-LTP21',
 'completed_source_endpoints':completed,
 'original_data':'Original ell,L,Omega,s,n>=1,V,Q,c,iota,m,tau0,lambda,d,E,xi and IsBasis; actual IsAutRepU sigma and original YOf.',
 'coefficient_scope':'The original arbitrary coefficient DVR O and integral tau0 are unchanged; all transport maps are the specified complex scalarizations. No flatness, field extension or continuity assumption on iota is introduced.',
 'zero_nonzero_scope':{'no_Y_nonzero_required':['LTP7','LTP9','LTP11'],'Y_nonzero_required':['LTP12','LTP14','LTP15','LTP17','LTP18','LTP21'],'local_component_existence':'LTP19-LTP20 require only original IsAutRepU, not nonzero Y.'},
 'right_action':'R_x(phi)(g)=phi(g*x), R_x R_y=R_(x*y); R((g*x)^-1)=R(x^-1)R(g^-1).',
 'infinity_weight':'At every original Emb index a, the weight is exactly lambda(a.res).dual, with ith entry -lambda(a.res)(n-1-i).',
 'distinguished_level':'The source subgroup Kc(L_(s.w(v0)),n,1), with no deeper-level substitution.',
 'type_quantifiers':'Arbitrary supplied IsTypeAlt chi, every family of local components, every IsRecT. Through the same TypeForAlt tau0, every original IsTeich family before every local map.',
 'spherical_normalization':'Original unnormalized dc at al(n,j), all j>=0 and representation-independent chosen right-coset representatives.',
 'choice_order':'One split component family of one sigma is chosen once; the same family supplies ell, Q, unramified, v0 and type fields. For Type_alt choose one nonzero scalarization functional before all compact k and all local correspondences.',
 'prime_rank_edge_cases':['original prime 3','every original admitted residue prime','n=1','no prime-to-rank restriction','m=0 or d=0 in the zero-space endpoints','empty St and empty embedding indices','n=0 additionally for full exists_locComp_split'],
 'inherited_foundation_retention':foundation_retention,
 'new_external_foundations':[],
 'not_supplied':boundaries}

review_candidates=list(HERE.glob('review_*.json'))
root_review=ROOT/'reviews_v0_44/local_transport_v44_root_review.json'
if root_review.exists():review_candidates.append(root_review)
reviews=[]
for p in review_candidates:
    rd=json.loads(p.read_text())
    bound=rd.get('proof_file_sha256',rd.get('proof_sha256',rd.get('main_tex_sha256',rd.get('main_sha256'))))
    if bound!=main_hash:continue
    expected={c['id']:c['proof_location']['sha256'] for c in claims}
    assert all(expected.get(k)==v for k,v in rd.get('proof_hashes',{}).items()),p
    reviews.append({'file':str(p.relative_to(ROOT)),'sha256':sha(p.read_bytes()),'record':rd})
status='complete_at_stated_scope_independently_reviewed' if reviews else 'complete_written_proof_pending_independent_review'
provenance={'schema':'rh-human-component-provenance/1','artifact_version':'0.44','date':'2026-11-23',
 'component':'local_transport_v44','source_commit':PIN,'main_tex_sha256':main_hash,'proof_file_sha256':main_hash,
 'status':status,'claims':claims,'source_groups':sources,'source_files':list(source_files.values()),
 'inherited_human_inputs':inherited,'classical_and_foundational_inputs':[],
 'inherited_foundation_retention':foundation_retention,'independent_reviews':reviews,
 'dependency_convention':'depends_on contains only numbered human claims. No foundation label is inserted as a fake DAG claim. Inherited foundation records are named separately above.',
 'source_proof_is_not_human_proof':True,'root_ledger_modified':False,'frozen_v43_modified':False}
closure={'schema':'rh-human-component-closure/1','artifact_version':'0.44','component':'local_transport_v44',
 'proof_file_sha256':main_hash,'status':status,'completed_source_endpoints':completed,
 'whole_obligations_closed':[],'remaining':boundaries,'foundation_retention_explicit':True,
 'one_original_component_family':True,'exact_depth_one':True,'every_IsRecT_and_IsTeich_retained':True,
 'validation':'Written endpoint/source matching and two-pass standalone draft TeX; no Lean replay or visual PDF certification.',
 'independent_reviews':reviews}
manifest={'schema':'rh-source-manifest/1','artifact_version':'0.44','source_commit':PIN,
 'files':list(source_files.values()),'ranges':list(sources.values()),'all_files_equal_pinned_git_blobs':True,
 'file_count':len(source_files),'range_count':len(sources)}
for fn,data in [('provenance.json',provenance),('source_manifest.json',manifest),('contract.json',contract),('closure.json',closure)]:
    (HERE/fn).write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n')
summary=[
 'LOCAL TRANSPORT ON THE ACTUAL AUTOMORPHIC PART — v0.44',
 'Source pin: '+PIN,'Proof SHA256: '+main_hash,
 f'Written claims:21. Pinned source files:{len(source_files)}. Exact source ranges:{len(sources)}.',
 'Status: '+status,'',
 'Complete exact suppliers:',
 '  LTP7 IsoL; LTP9 IsoQ; LTP11 Sph; LTP12 Unr at every outside place, including nonsplit;',
 '  LTP14 exact dual infinity weight; LTP15 distinguished Kc(1); LTP17 Type_alt for every IsRecT;',
 '  LTP18 every original Teich family through unchanged TypeForAlt.',
 '  LTP19-20 actual admissible local component and unramified iff spherical for all CM fields/ranks;',
 '  LTP21 one simultaneous local family for all original PartU fields.',
 '  Helpers include full partUR2Mem, partUR2AtV/AtW, partUR2Fix and partUR2Abs.','',
 'Proof methods:',
 '  Exact scalarization and its right-translation order, finite separating dual coordinates,',
 '  actual split local factors and centralizers, algebraic isotypic descent, finite compact averaging,',
 '  original unnormalized Hecke sums, the complete matrix-valued base-level equation,',
 '  actual prime recovery and fixed-iota dual weights, one product section at the type places,',
 '  and a new local-component construction inside the actual positive finite-multiplicity space.',
 '',
 'Scope retained:',
 '  Original O,tau0,iota,E,xi and Y; original ranks/primes including3; no continuity of iota.',
 '  Nonzero Y only at endpoints that require it; no arbitrary residual-block nonvanishing.',
 '  Exact original H.Ax where required and its actual FNL16 installation.',
 '  IsTypeAlt/TypeForAlt retain all every-map/every-Teich quantifiers and ITA foundations.',
 '',
 'Remaining beyond this packet:']+['  '+x for x in boundaries]+[
 '',
 'Metadata builder verifies each cited source file against git show at the exact pin,',
 'hashes every source range and every written claim block, and records only actual',
 'numbered human claims in depends_on. No common ledger, history or source was modified.',
 'TeX validator is reproducible with --format pointing to the workspace pdflatex format.']
(HERE/'report.txt').write_text('\n'.join(summary)+'\n')
print(json.dumps({'component':'local_transport_v44','claims':len(claims),'files':len(source_files),
 'ranges':len(sources),'proof_sha256':main_hash,'status':status},ensure_ascii=False))
