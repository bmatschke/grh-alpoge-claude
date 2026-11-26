#!/usr/bin/env python3
"""Pin written arithmetic-fiber proofs and distinguish the remaining installer."""
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
G = H + 'CoefficientRepTrivialOnUnramified.lean'
P = 'src/Development/AbelianVarietyTheory/PublishedTheorems/'

specs = {
 'dense_box': (B+'AlgebraTools/HidaCompleteRings/DenseBox.lean',146,149,'denseBox; elementary alternate proof in AFS1'),
 'torsion_boxes': (D+'TDenseU.lean',94,146,'du_near and du_sets; prime-to-ell common exponent simplification'),
 'local_finiteness': (D+'TDenseU.lean',149,245,'du_pow, du_ker, du_fin, du_cont; actual-local specialization via inherited KX3'),
 'algebraic_character': (D+'TDenseU.lean',249,345,'du_Uc, du_unit, du_alg, du_arith and positive local rank'),
 'weight_density': (D+'TDenseU.lean',346,457,'du_box and full isDomain_and_denseWt_of_isTheta'),
 'local_abelian_fields': (B+'WeilGroupCharacters/Inertia.lean',9,24,'muG and all LocAb fields'),
 'universal_weight': (B+'WeilGroupCharacters/LamFree.lean',150,None,'lam_ex_free; inherited exact universal-object construction KX4-KX5'),
 'good_definitions': (G,149,176,'op, IsWt, finPart, Arith, Good, DenseWt'),
 'weight_consistency': (D+'TWtBridge.lean',100,166,'emb_lt, emb_place, emb_inj, wt_ex'),
 'local_weight_bridge': (D+'TWtBridge.lean',16,99,'stored Artin uniqueness, unit surjectivity, IsFin, part_val, locAlg_iff'),
 'weight_bridge': (D+'TWtBridge.lean',168,239,'arith_good_iff_hset_of_theta_incr_weight'),
 'point_eigenvector': (B+'AlgebraTools/HidaCompleteRings/PointEig.lean',8,None,'pointEig for arbitrary faithful finite module and arbitrary field map'),
 'fiber_nonvanishing': (B+'AlgebraTools/HidaCompleteRings/FibreNe.lean',1,None,'fibreNe; faithful support and Nakayama'),
 'jacquet_kernel': (O+'PropCker.lean',1,None,'propCker averaging and kernel characterization; concrete glIwa proof here'),
 'jacquet_sum': (O+'PropCp.lean',4,None,'propCp exact integer quotient index'),
 'local_definitions': (H+'Distinct.lean',22,45,'glIwa, piIwa, PS, psEig, IsInvOn, Distinct, invPart'),
 'local_ps_endpoint': (D+'ExistsForm.lean',272,391,'exists_principal_series_of_distinct_inv_ne_bot'),
 'local_ps_helpers': (D+'ExistsForm.lean',175,268,'eig_le, inv_stab, inv_inj and normalized eigenvalue computation'),
 'principal_irreducibility': (D+'TPsIrr.lean',13,92,'singleton induction in stages and totally-disjoint irreducibility'),
 'jacquet_multiplicities': (B+'AlgebraTools/IwJqMult.lean',1,None,'one-dimensional Bruhat-cell filtration and multiplicity bound'),
 'retained_literature_fields': (D+'LitAut.lean',10,29,'LitLocAlt: original bz, geo, disj fields among the retained literature hypotheses'),
 'bz_clause': (P+'TwistedTraceFormula/HasFiniteLengthOfIsIrreducible.lean',19,53,'irreducible admissibility; Jacquet finite length; original BZ hypothesis definition'),
 'geometric_clause': (P+'TwistedTraceFormula/ExistsCellOfIsSubquotient.lean',146,208,'JacquetOfInducedFiltration and GeometricLemma definitions'),
 'disjoint_clause': (P+'GaloisGeometry₂/TotallyDisjointProductIrreducible.lean',10,18,'literal totally-disjoint irreducibility hypothesis, twists -1,0,1'),
 'isotypic_definition': (G,71,74,'IsoSum as sum of original intertwining images'),
 'isotypic_separation': (O+'IsoSep.lean',10,None,'isoSep exact separation-map endpoint'),
 'scalar_helpers': (D+'CharOfScalar.lean',13,229,'onto_inf, kill_poly, unit_eig, char_of_scalar, local/product operator factorization, local_step'),
 'good_scalar': (D+'CharOfScalar.lean',230,307,'full original goodScalB_alt'),
 'classical_definitions': (G,216,251,'original lowVal/opC/uzC/ClAt/OrdAt and every IsSpec field'),
 'part_definition': (D+'UnitaryPointProperties.lean',29,53,'PartAltAlt and exact AutomorphicHeckeSet predicate'),
 'fiber_action_helpers': (D+'HeckeOperatorPreservesPart.lean',20,273,'pa_rho, pa_eig, pa_chr, pa_inst, pa_main, pa_fin and exact tensor maps'),
 'part_preservation': (D+'HeckeOperatorPreservesPart.lean',274,306,'hecke_operator_preserves_part and its isotypic/product stability helpers'),
 'part_action': (D+'HeckeOperatorPreservesPart.lean',308,336,'full original partAct0_alt'),
 'core_separation': (D+'TCoreSep.lean',13,67,'coreSep_coord, coreSep_kill and eq_zero_of_vanish_at_good_points_dense_weight'),
 'out_definition': (G,275,285,'Out.sep and separate Out.pt fields'),
 'same_kernel_lemma': (D+'TJDense.lean',23,36,'dense_arithmetic_points exact abstract implication'),
 'density_installation': (D+'TJDense.lean',37,50,'dense_of_is_j_unitary_hecke_data; actual automorphic supplier remains explicit'),
 'same_ideal_definition': (H+'IsTheta.lean',39,53,'HSet.IsMap and the literal two-case HSet.IsJ'),
 'unitary_record': (D+'UnitaryHeckeData.lean',38,None,'TypeForAlt, UnitaryPointProperties, UnitaryHeckeData and IsJ abbreviation'),
 'point_and_dense': (B+'WeilGroupCharacters/ArithmeticPointClassicality.lean',49,80,'Hida weights, original Pt/Arith/Good and full Dense quantifiers'),
}

files, sources = {}, {}
for key, (rel, first, last, decl) in specs.items():
    data = (repo/rel).read_bytes()
    pinned = subprocess.run(['git','show',PIN+':'+rel],cwd=repo,
                            check=True,stdout=subprocess.PIPE).stdout
    assert data == pinned, rel
    lines = data.splitlines(keepends=True)
    last = last or len(lines)
    assert 1 <= first <= last <= len(lines), (key,first,last,len(lines))
    block = b''.join(lines[first-1:last])
    url = f'https://github.com/CocoSgt/riemann-hypothesis-lean/blob/{PIN}/{rel}'
    files[rel] = {'path':rel,'sha256':sha(data),'bytes':len(data),
                  'line_count':len(lines),'url':url,
                  'verified_equal_to_pinned_git_blob':True}
    sources[key] = {'id':'AFS_SRC_'+key.upper(),'path':rel,'declaration':decl,
       'line_start':first,'line_end':last,'sha256':sha(data),
       'full_file_sha256':sha(data),'range_sha256':sha(block),'range_bytes':len(block),
       'source_commit':PIN,'verified_equal_to_pinned_git_blob':True,
       'url':url+f'#L{first}-L{last}'}

relations = {
 1: (['WRP2'],['dense_box']),
 2: ([1],['torsion_boxes','weight_density']),
 3: (['KX3','CIP4'],['local_finiteness','algebraic_character','local_abelian_fields']),
 4: (['KX3','CIP4','WRP1','ASP2'],['algebraic_character','good_definitions','weight_density']),
 5: ([2,3,4,'KX4','KX5'],['weight_density','universal_weight','good_definitions']),
 6: (['WRP1'],['weight_consistency']),
 7: (['CIP4'],['local_weight_bridge']),
 8: ([6,7,'CIP4','CIP5','KX3'],['weight_bridge','point_and_dense']),
 9: ([],['point_eigenvector','fiber_nonvanishing','fiber_action_helpers']),
 10: ([9,'OHA6','OHA7','ASP11'],['point_eigenvector','fiber_nonvanishing','part_action']),
 11: (['OST5','OST6','OST26'],['jacquet_kernel','jacquet_sum','local_definitions','local_ps_helpers','bz_clause']),
 12: ([9,11],['local_ps_endpoint','local_ps_helpers','principal_irreducibility','jacquet_multiplicities','retained_literature_fields','bz_clause','geometric_clause','disjoint_clause']),
 13: ([],['isotypic_definition','isotypic_separation']),
 14: ([12,13,'OST5'],['scalar_helpers','local_ps_endpoint']),
 15: ([],['scalar_helpers']),
 16: ([13,'OST5','OST27'],['part_preservation','scalar_helpers','part_definition']),
 17: ([14,15,16,'ASP2','OST25'],['good_scalar','classical_definitions']),
 18: ([],['fiber_action_helpers']),
 19: ([9,16,17,18,'OHA6','OHA7','ASP11','CFD12'],['part_action','part_definition','classical_definitions']),
 20: ([19,'ASP13','OHA7'],['core_separation','out_definition']),
 21: ([],['same_kernel_lemma']),
 22: ([5,6,8,20,21,'FNL16'],['density_installation','same_ideal_definition','unitary_record','point_and_dense']),
}

tex = (HERE/'main.tex').read_text()
claims = []
for number,(deps,groups) in relations.items():
    cid=f'AFS{number}'
    match=re.search(r'% BEGIN '+cid+r'\n.*?% END '+cid+r'\n',tex,re.S)
    assert match,cid
    block=match.group()
    title=re.search(r'\\paragraph\{'+cid+r'\. (.*?)\}\n',block).group(1)
    start=tex[:match.start()].count('\n')+1
    claims.append({'id':cid,'title':title,'introduced_in':'0.43','classification':'B',
      'status':'complete written implication at the stated original or explicitly conditional scope',
      'depends_on':[f'AFS{x}' if isinstance(x,int) else x for x in deps],
      'scope':'shared RH and unrestricted Dirichlet GRH; original arithmetic points and ordinary Hecke algebra',
      'proof_location':{'file':'arithmetic_fibers_v43/main.tex','label':'claim:'+cid,
       'line_start':start,'line_end':start+block.count('\n')-1,
       'sha256':sha(block.encode()),'bytes':len(block.encode())},
      'source_groups':groups,'sources':[sources[g] for g in groups],
      'retained_hypotheses':(['literal hLit.loc.bz, hLit.loc.geo, hLit.loc.disj'] if number in [11,12,14,17,19,20,22] else [])+
          (['original supplied H.AutomorphicHeckeSet(iota,P)'] if number in [19,20] else [])+
          (['actual H.AutomorphicHeckeSet(iota,UnitaryPointProperties r iota), still an unconstructed installation input'] if number==22 else []),
      'classical_inputs':[],
      'dependency_scope':'Written proof, not an inference from formal acceptance. AFS22 does not retire the bare TJDense source endpoint.'})

component_for = {'KX':'symplectic_universal_arithmetic','CIP':'count_ii_producer',
 'WRP':'weight_representation_v42','ASP':'arithmetic_specialization_v42',
 'OST':'ordinary_structure_v42','OHA':'ordinary_hecke_algebra_v42',
 'CFD':'classical_parts_v43','FNL':'finite_levels_v42'}
inputs=[]
ids=sorted({x for deps,_ in relations.values() for x in deps if isinstance(x,str)})
for cid in ids:
    pref=re.match(r'[A-Z]+',cid).group()
    component=component_for[pref]
    contents=(ROOT/component/'main.tex').read_text()
    match=re.search(r'% BEGIN '+cid+r'\n.*?% END '+cid+r'\n',contents,re.S)
    assert match,cid
    inputs.append({'claim':cid,'file':component+'/main.tex',
      'claim_sha256':sha(match.group().encode()),'file_sha256':sha(contents.encode()),
      'classification':'B','kind':'inherited' if pref in ['KX','CIP'] else 'peer',
      'scope':'Only the printed exact proof scope is used; CFD12 retains its original supplied AutomorphicHeckeSet.'})

remaining = [
 'Actual AutomorphicHeckeSet(iota,UnitaryPointProperties r iota) supplier from the original type and automorphic-part/Galois-attachment constructions (partX_alt/GuWrap); compact automorphic decomposition alone does not supply its Galois and local compatibility fields.',
 'Bare TJDense installation without the explicitly retained actual AutomorphicHeckeSet supplier.',
 'The other original Out.pt, same-J Hida ring, automorphy, purity and auxiliary control conditions not stated as conclusions here.',
 'Nonvanishing of an arbitrary chosen residual block when its actual module has not been shown nonzero.',
 'No whole COUNT_II_SUPPORT or RH/GRH obligation is closed by this packet.'
]
completed = [
 {'endpoint':'UpperTheory.V.Hi.isDomain_and_denseWt_of_isTheta','proof_claim':'AFS5','scope':'Every original supplied LamObj and every dominant weight, all primes, every original coefficient-algebra point; KX3-KX5 identify the actual universal object.'},
 {'endpoint':'UpperTheory.V.Hi.arith_good_iff_hset_of_theta_incr_weight','proof_claim':'AFS8','scope':'Original increasing Hida weights and every original B point, exact toPair map, stored Artin map and finite parts.'},
 {'endpoint':'UpperTheory.V.AlgebraTools.AnnihilatorQuotientFinite.denseBox','proof_claim':'AFS1','scope':'Infinite Cartesian sets throughout the open unit disk; no interior accumulation premise.'},
 {'endpoint':'UpperTheory.V.AlgebraTools.AnnihilatorQuotientFinite.pointEig','proof_claim':'AFS9','scope':'Arbitrary finite faithful module, commutative acting algebra and field point; the faithful action identifies its algebra with its actual endomorphism image; no flatness.'},
 {'endpoint':'UpperTheory.V.Hi.exists_principal_series_of_distinct_inv_ne_bot','proof_claim':'AFS12','scope':'All original nonarchimedean local fields and n>=0; original hLit retained, including explicitly unpacked bz/geo/disj clauses; exact PS/psEig and stable ordinary subspace.'},
 {'endpoint':'UpperTheory.V.Hi.isoSep','proof_claim':'AFS13','scope':'Every literal IsoSum; a map on the whole ambient vector space intertwining only on the given Y, exactly as stated.'},
 {'endpoint':'hecke_operator_preserves_part','proof_claim':'AFS16','scope':'Every original PartAltAlt and generator, with original factor/coset normalization.'},
 {'endpoint':'UpperTheory.V.Hi.goodScalB_alt','proof_claim':'AFS17','scope':'Every supplied original IsSpec and Good datum, every level and e>=c0, arbitrary original IsCO A, fixed iota, all original positive generators j+1.'},
 {'endpoint':'UpperTheory.V.Hi.partAct0_alt','proof_claim':'AFS19','scope':'All original hypotheses including supplied AutomorphicHeckeSet; one action before all points and parts; nonzero eigenvectors for every specified point and scalar points for every nonzero part at Good x.'},
 {'endpoint':'UpperTheory.V.Hi.eq_zero_of_vanish_at_good_points_dense_weight','proof_claim':'AFS20','scope':'Full literal TCoreSep endpoint / Out.sep on the original T, with original supplied AutomorphicHeckeSet and DenseWt.'},
 {'endpoint':'UpperTheory.V.Hi.dense_arithmetic_points','proof_claim':'AFS21','scope':'Exact abstract all-rings same-kernel implication; even surjectivity is unnecessary.'},
]
contract = {
 'main_claims':'AFS1-AFS22','claim_count':22,
 'completed_source_endpoints':completed,
 'conditional_installation':{'claim':'AFS22','source_endpoint':'UpperTheory.V.Hi.dense_of_is_j_unitary_hecke_data',
   'complete_at_printed_scope':True,'bare_source_endpoint_closed':False,
   'retained_additional_supplier':'H.AutomorphicHeckeSet(iota,UnitaryPointProperties r iota)',
   'conclusion':'For every original J, R.IsJ B K J implies B.Dense J; every increasing weight and every b; exactly the original J=ker f.'},
 'arithmetic_density':'Actual LamObj from KX5; independent disjoint torsion boxes, evaluated within finite algebraic extensions; all original point maps.',
 'nonvanishing':'Every nonzero original finite-free MK has every nonzero field fiber and admits an extension of each given coefficient point; every specified Hecke-algebra point occurs as an eigenvector. This does not prove MK nonzero for an arbitrary label.',
 'coefficient_scope':'Original arbitrary IsCO A, including nonreduced rings; point maps are allowed to be noninjective and nonflat. Tensor injections use the actual idempotent splitting.',
 'fixed_embedding':'The specified iota:Qbar_ell≃C is unchanged, and is never assumed continuous.',
 'prime_scope':'Weight density allows every prime. HSet applications retain ell!=2 and include ell=3. No substitution ell>=5.',
 'local_normalization':'Original uniformizer; U_a is the integral finite quotient sum. PS(omega)=normalized Ind(omega_i |.|^((n-1)/2)); psEig(omega,j)=product_{i<j} omega_i(pi) q^(-i). Global local generators use j+1 and lowVal(v,j+1)^(-1).',
 'retained_literature':'Only the source-supplied hLit and its exact bz/geo/disj clauses are used for the local principal-series step. No unconditional production of these hypotheses and no new class-A imports are asserted.',
 'automorphic_scope':'CFD12 and AFS19-AFS20 retain the source-supplied AutomorphicHeckeSet. The actual UnitaryPointProperties Galois attachment remains an installation frontier in AFS22.',
 'choice_order':'Fix original datum, rings, iota and lambda before torsion boxes; use the given x and one original sp; construct one action before all Hecke points and all parts; the scalar point of a nonzero part is chosen once before t and F; J remains the supplied kernel.',
 'not_supplied':remaining,
}
provenance = {
 'schema':'rh-human-component-provenance/1','artifact_version':'0.43','date':'2026-11-23',
 'component':'arithmetic_fibers_v43','source_commit':PIN,
 'main_tex_sha256':sha(tex.encode()),'proof_file_sha256':sha(tex.encode()),
 'claims':claims,'source_groups':sources,'source_files':list(files.values()),
 'inherited_proof_inputs':[x for x in inputs if x['kind']=='inherited'],
 'peer_proof_inputs':[x for x in inputs if x['kind']=='peer'],
 'published_applications':[],
 'retained_original_hypotheses':['hLit.loc.bz','hLit.loc.geo','hLit.loc.disj','original H.AutomorphicHeckeSet where printed'],
 'endpoint_contract':contract,
 'validation':{'source_files_equal_to_pinned_git_blobs':True,
  'source_file_count':len(files),'source_range_count':len(sources),'claim_count':len(claims),
  'no_lean_kernel_replay':True,'mathematical_claim_count_is_not_a_completion_percentage':True},
 'builder':{'file':'arithmetic_fibers_v43/build_metadata.py','sha256':sha(Path(__file__).read_bytes())}}
def save(name,obj):
    (HERE/name).write_text(json.dumps(obj,indent=2,ensure_ascii=False)+'\n')
save('provenance.json',provenance)
save('source_manifest.json',{'source_commit':PIN,'source_files':list(files.values()),'ranges':sources})
save('contract.json',contract)
save('closure.json',{'schema':'rh-exact-endpoint-closure/1','artifact_version':'0.43',
 'main_tex_sha256':sha(tex.encode()),'completed':completed,
 'conditional_installation':contract['conditional_installation'],
 'whole_obligations_closed':[],'remaining':remaining,'choice_order':contract['choice_order']})
(HERE/'report.txt').write_text(
 'ARITHMETIC FIBERS AND SEPARATION — v0.43\n\n'
 'AFS1–AFS22 give 22 complete written B implications at their printed scopes. The exact original weight-domain/density and arithmetic/good-point bridge are now supplied. The disjoint torsion-box argument uses an elementary integral-series root bound, so it does not assume accumulation inside the open disk. KX3–KX5 identify every original supplied LamObj.\n\n'
 'The finite algebra argument realizes every specified Hecke point by a nonzero eigenvector in the actual module fiber without flatness. Nonzero original finite-free blocks have nonzero fibers at every given coefficient point. The local Jacquet argument explicitly derives the distinct-character principal series and its original normalized scalar from the retained literal bz/geo/disj literature hypotheses.\n\n'
 'The complete original goodScalB_alt, hecke_operator_preserves_part, partAct0_alt and TCoreSep/Out.sep endpoints are proved, retaining their original automorphic-part hypothesis. The one action and scalar points use the original specialization map, levels, embedding, uniformizers, positive generators and indices. All CNL/nonflat scope and prime 3 are preserved.\n\n'
 'AFS22 gives every increasing-weight Dense assertion on the SAME original IsJ kernel, conditional only on the explicitly identified actual AutomorphicHeckeSet installation input in addition to original TJDense data. The bare TJDense endpoint is NOT marked closed: the partX_alt/GuWrap automorphic Galois attachment and its complete dictionaries remain a producer, even if compact automorphic decomposition is available. No Out.pt or whole Hida/RH/GRH closure is claimed.\n\n'
 f'Pinned source: {PIN}. Verified {len(files)} full file blobs and {len(sources)} exact ranges. Main SHA256 {sha(tex.encode())}. No Lean replay; no new class-A imports.\n')
print(json.dumps({'component':'arithmetic_fibers_v43','claims':len(claims),
 'source_files':len(files),'source_ranges':len(sources),'main_sha256':sha(tex.encode()),
 'status':'PASS','bare_TJDense_closed':False}))
