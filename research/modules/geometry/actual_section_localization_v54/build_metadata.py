#!/usr/bin/env python3
"""Bind the ASL proof, accepted sources and inherited human proofs.
Only files within this component are written. No Lean replay is performed.
"""
from pathlib import Path
import argparse
import hashlib
import json
import re
import subprocess
HERE = Path(__file__).resolve().parent
WORK = HERE.parent
COMP = HERE.name
PIN = '7cbf7a0c32fca1badf05931879a37c3f8a2b03b4'
REPO = 'https://github.com/CocoSgt/riemann-hypothesis-lean'
A = 'src/Development/AbelianVarietyTheory/'
C = A + 'Proofs/CoherentCohomologyProofs/'
P = A + 'Proofs/AbelianSchemeLawProofs/'
D = A + 'Definitions/AbelianSchemeLaws/'
Q = A + 'Definitions/QuasicoherentCohomology/'
parser = argparse.ArgumentParser()
parser.add_argument('--source-root', type=Path, default=Path('/workspace/scratch/249d32c24541/formal_source'))
args = parser.parse_args()
def sha(data): return hashlib.sha256(data).hexdigest()
def write(name, data):
    (HERE/name).write_text(json.dumps(data, indent=2, ensure_ascii=False)+'\n')
proof = (HERE/'main.tex').read_bytes()
base = dict(artifact_version='0.54', component=COMP, source_commit=PIN,
            proof_file_sha256=sha(proof), status='written_pending_independent_review')
rows=[]
def src(key,file,lo,hi,declaration,prefix=C):
    rows.append((key,prefix+file,lo,hi,declaration))
src('scalar_localization','ExistsTwExtendPowMul.lean',15,37,'basicOpen_rs_eq; fun_extend; fun_kill')
src('finite_chart_cover','ExistsTwExtendPowMul.lean',39,78,'exists_fin_cover; unit_shift; pw_rel')
src('neighborhood_killing','ExistsNhdsPowMulTwCoordEqZero.lean',13,46,'exists_nhds_pow_mul_twCoord_eq_zero')
src('global_killing','ExistsNhdsPowMulTwCoordEqZero.lean',48,62,'exists_pow_mul_twCoord_eq_zero')
src('twisted_extension','ExistsTwExtendPowMul.lean',80,171,'exists_tw_extend_pow_mul')
src('coordinate_polynomial_action','ExistsSmulOfTwCoord.lean',13,49,'GrSum.apply_eq_eval₂Hom_mul; AbLaw.exists_smul_of_twCoord')
src('product_locus','MemNonzeroLocusIffMemBasicOpenChart.lean',13,59,'chart basic-open, finite product locus and prodSec')
src('qcqs_affine_intersections','VeryAmpleCompactQuasiSeparatedAffineCharts.lean',17,50,'compact_quasiSeparated_isAffineOpen and its retrocompactness/affine-intersection lemmas')
src('twisted_localization','TwistedSectionsLocaliseToCharts.lean',24,50,'twisted_sections_localise')
src('homogeneous_fraction_map','ExistsHomLocBijectiveGrSum.lean',45,110,'exists_homLoc_bijective; exists_homLoc_bijective_grSum')
src('homogeneous_cube_naturality','ExistsHomLocBijectiveGrSum.lean',113,162,'homLoc comparison naturality; exists_grCube_bijective_grSum')
src('actual_twisted_cube','ExistsTwistedSectionsCubeBijective.lean',21,63,'twistedSumRestrict; exists_grCube_twistedSections_hom_secCube_bijective')
src('actual_twisted_cube_theorem','ExistsTwistedSectionsCubeBijective.lean',45,63,'exists_grCube_twistedSections_hom_secCube_bijective')
src('dehom_units','ExistsDehomogenisationTwistedChart.lean',20,84,'secUnit; divPow; divPow_mulSec')
src('dehom_semilinear','ExistsDehomogenisationTwistedChart.lean',86,175,'dehom; ratio_self; exists_dehom_top')
src('dehom_chart','ExistsDehomogenisationTwistedChart.lean',179,189,'exists_dehom_chart')
src('ordinary_localization','SecOnBasicOpenLocalization.lean',14,21,'secOn_basicOpen_localization')
src('affine_projectivity','SecOnFinitePresentationProjective.lean',16,65,'chartBasicOpen localization; secOn_finitePresentation_projective')
src('affine_projectivity_theorem','SecOnFinitePresentationProjective.lean',44,65,'secOn_finitePresentation_projective')
src('affine_basechange','IsLocalizedModuleResBasicOpenOfQcqs.lean',92,115,'SecOn.isBaseChange_pullLE',P)
src('actual_scalar_basechange','IsLocalizedModuleResBasicOpenOfQcqs.lean',187,261,'SecOnR.isBaseChange_pull; baseChangeHom_restrict; baseChangeHom_bijective',P)
src('actual_cech_basechange','IsLocalizedModuleResBasicOpenOfQcqs.lean',294,375,'secCubeBaseChange; cechLBBaseChange and actual isomorphism',P)
src('smooth_flat_scalar','CstSmoothAndFlat.lean',12,20,'cst_smooth_and_flat')
src('actual_finite_complex','ExistsFiniteProjectiveCechComplexLineBundle.lean',19,43,'exists_finite_projective_complex_cechLB')
src('full_perf','NonemptyPerfectSectionsComplexOfSmoothProj.lean',15,22,'nonempty_perf_of_smooth_isProjBy',P)
src('literal_projectivity','FirstCohomologyVanishesSpecOfIsLocalRing.lean',13,42,'rs; cst; pw; tw; VeryAmpleBy; IsProjBy; FirstCohomologyVanishes',D)
src('literal_perf','FirstCohomologyVanishesSpecOfIsLocalRing.lean',44,81,'le_pull and all fields of Perf',D)
src('actual_sections','IsScalarTowerOfAlgebraMapEq.lean',14,130,'SecOn; coordinate compatibility; restriction; gluing; chart',D)
src('actual_twist_operations','IsScalarTowerOfAlgebraMapEq.lean',199,364,'twCoord; twMk; mulSec; invertibility; twZeroEquiv',D)
src('scalar_sections','IsScalarTowerOfAlgebraMapEq.lean',367,550,'cstAlgebra; SecOnR; actual scalar, restriction and pullback maps',D)
src('actual_section_cube','IsScalarTowerOfAlgebraMapEq.lean',559,643,'secCube; cechLB; exact restriction differential; secCubePull',D)
src('homloc_definition','ExistsAwayFracOfMemHomLoc.lean',197,328,'homLoc and exact homogeneous fraction representatives',Q)
src('grcube_definition','ExistsAwayFracOfMemHomLoc.lean',577,617,'grCube; grCubeMap; scalar-extension conventions',Q)
src('inherited_noetherian_model','DehomogenisingCompOfSaturating.lean',44,114,'FCD18: exists_noetherian_model_grCube')
src('inherited_projective_complex','ExistsFiniteProjectiveComplexOfNoetherianModel.lean',9,60,'GSL8: original universal finite-projective complex from cube model')
src('inherited_perf_construction','ThreeTermComplexOfProjectiveCechModel.lean',106,156,'GSL10: perf_of_projective_model')

previous_contracts=json.loads((WORK/'global_section_laws_v52/contracts.json').read_text())
removed={'GSL_STANDARD','GSL_PERF_GEOMETRY','GSL_NOETH_CUBE_DATA','GSL_CECH_MODEL_DATA'}
retained=[dict(x) for x in previous_contracts['external_inputs'] if x['id'] not in removed]
for inp in retained:
    for j,s in enumerate(inp.get('sources',[])):
        src('retained_'+inp['id'].lower()+'_'+str(j),s['path'],s['line_start'],s['line_end'],s['declaration'],'')
files={}; sources={}
for key,path,lo,hi,declaration in rows:
    if path not in files:
        blob=subprocess.check_output(['git','-C',str(args.source_root),'show',PIN+':'+path])
        assert (args.source_root/path).read_bytes()==blob, 'Source differs from pin: '+path
        dest=HERE/'source_snapshot'/path
        dest.parent.mkdir(parents=True,exist_ok=True);dest.write_bytes(blob)
        files[path]=dict(path=path,snapshot_file=str(dest.relative_to(WORK)),bytes=len(blob),
            line_count=len(blob.splitlines()),sha256=sha(blob),file_sha256=sha(blob),source_commit=PIN,
            verified_equal_to_pinned_git_blob=True,url=REPO+'/blob/'+PIN+'/'+path)
    rec=files[path];ls=(WORK/rec['snapshot_file']).read_bytes().splitlines(keepends=True)
    assert 1<=lo<=hi<=len(ls),(key,lo,hi,len(ls))
    body=b''.join(ls[lo-1:hi])
    sources[key]=dict(id='ASL_SRC_'+key.upper(),path=path,declaration=declaration,
        line_start=lo,line_end=hi,source_commit=PIN,file_sha256=rec['sha256'],full_file_sha256=rec['sha256'],
        range_sha256=sha(body),range_bytes=len(body),snapshot_file=rec['snapshot_file'],
        verified_equal_to_pinned_git_blob=True,url=rec['url']+f'#L{lo}-L{hi}')
for inp in retained:
    inp['sources']=[sources['retained_'+inp['id'].lower()+'_'+str(j)] for j in range(len(inp.get('sources',[])))]
    inp['globally_discharged_by_this_component']=False
    inp['boundary_inherited_from']='global_section_laws_v52/contracts.json'

specs=[
 ('ASL1',[],['scalar_localization'],'Scalar localization and power killing on quasi-compact opens.','Arbitrary rings, including zero divisors and nilpotents; one power on a quasi-compact open.'),
 ('ASL2',[],['product_locus','actual_twist_operations','literal_projectivity'],'Integer twists and invertibility on the original nonzero locus.','Every integer t,d; original transition functions and actual M to M(0) comparison.'),
 ('ASL3',[],['finite_chart_cover'],'A finite affine cover subordinate to both original line bundles.','Quasi-compact Y; overlap quasi-compactness only requires the original quasi-separatedness.'),
 ('ASL4',['ASL1','ASL2'],['neighborhood_killing'],'One neighborhood and exponent for all original chart indices.','After choosing a point, the same neighborhood and exponent work for every p,l and every open in their intersection; no global quasi-compactness premise is used.'),
 ('ASL5',['ASL4'],['global_killing'],'One global power kills the actual twisted section.','Quasi-compact Y; all integer twists; no quasi-separatedness needed for this killing statement.'),
 ('ASL6',['ASL1','ASL3'],['twisted_extension'],'First denominator clearing on finitely many affine charts.','A first exponent N extends coordinates but need not yet make them agree on full overlaps.'),
 ('ASL7',['ASL1','ASL2','ASL3','ASL6'],['twisted_extension'],'Full extension after a power of the actual section.','Quasi-compact quasi-separated Y; a separate common K kills overlap discrepancies; original all-chart formula.'),
 ('ASL8',['ASL2'],['coordinate_polynomial_action','product_locus','scalar_sections'],'Actual graded section action and product sections.','All integer degrees, finite supports, actual X_i multiplication and empty product equal to one.'),
 ('ASL9',['ASL2'],['qcqs_affine_intersections','literal_projectivity'],'The given projective presentation supplies quasi-compactness and affine intersections.','The literal VeryAmpleBy data imply quasi-separatedness and affine D_I for every nonempty I over arbitrary R.'),
 ('ASL10',['ASL5','ASL7','ASL8','ASL9'],['twisted_localization'],'Both original twisted-section localization clauses.','All finite I and all integer t, including empty I; element-dependent powers with actual restriction.'),
 ('ASL11',['ASL2','ASL10'],['homogeneous_fraction_map','homloc_definition'],'The canonical homogeneous fraction-to-section isomorphism.','Every homogeneous degree t; explicit a/X_I^k goes to sigma_I^(-k) times the actual restriction.'),
 ('ASL12',['ASL8','ASL11'],['homogeneous_cube_naturality','actual_twisted_cube','grcube_definition','actual_section_cube'],'The full actual graded-section cube comparison.','All vertices and every restriction; pullback naturality is preserved without asserting global sections commute with arbitrary base change.'),
 ('ASL13',['ASL2','ASL8'],['dehom_units','dehom_semilinear'],'Division by the original section in every integer degree.','Arbitrary V contained in D(s_i), actual ratios, coefficient-ring linearity and exact semilinear polynomial evaluation.'),
 ('ASL14',['ASL10','ASL13','FCD13'],['dehom_chart','dehom_semilinear'],'The full original chart dehomogenization.','Every family satisfying the original coordinate-ratio identities agrees with the very-ample ratios; original actual chart module, surjective epsilon, pi(X_i)=1, homogeneous power-kernel and degree-zero restriction; inherited quotient identification.'),
 ('ASL15',['ASL5','ASL7'],['ordinary_localization'],'Ordinary section localization on any quasi-compact quasi-separated open.','The actual module map P_f to sections on D(f); no finite-generation, reducedness or Noetherianity assumption.'),
 ('ASL16',['ASL1','ASL15'],['affine_projectivity'],'An explicit finite dual basis for the actual affine section module.','Every affine V and actual line bundle M; extra powers correct local evaluation identities globally, yielding projectivity and finite presentation over O(V).'),
 ('ASL17',['ASL15','ASL16'],['affine_basechange','actual_scalar_basechange','actual_cech_basechange'],'Actual affine sections under arbitrary scalar extension.','Any ring map B to B-prime and any specified Cartesian pullback; exact canonical map and restriction naturality; no flatness.'),
 ('ASL18',[],['smooth_flat_scalar'],'Smoothness and flatness for the original chart scalar map.','Any affine source open of the given smooth or flat morphism to Spec R; the original cst map, not a substitute algebra structure.'),
 ('ASL19',['ASL2','ASL12','ASL14','ASL16','ASL18','FCD18'],['actual_finite_complex','inherited_noetherian_model'],'One Noetherian model for the actual section cube.','One fixed R0,C0,Theta for the actual Y,H,M,s_i before any later coefficient ring; all three original nonempty-vertex model outputs.'),
 ('ASL20',['ASL17','ASL19','GSL8'],['actual_finite_complex','inherited_projective_complex'],'Full universally valid finite-projective section complex.','The original alternating Cech differential; finite projectives and original upper bound; every later ring map, without flatness.'),
 ('ASL21',['ASL9','ASL12','ASL17','ASL20','GSL9','GSL10'],['full_perf','literal_perf','inherited_perf_construction'],'The full original smooth-projective Perf producer.','Every arbitrary R, smooth IsProjBy f and actual M; fixed matrices, chart functions and every specified pullback square; the exact field retains only its own FirstCohomologyVanishes antecedent.')
]
lines=proof.splitlines(keepends=True);claims=[]
for ident,deps,groups,title,scope in specs:
    start=next(i for i,l in enumerate(lines) if l.strip()==('% BEGIN '+ident).encode())
    end=next(i for i,l in enumerate(lines) if l.strip()==('% END '+ident).encode())
    block=b''.join(lines[start:end+1])
    claims.append(dict(id=ident,title=title,introduced_in='0.54',classification='B',depends_on=deps,
        external_input_ids=['ASL_STANDARD'],scope_note=scope,source_groups=groups,sources=[sources[g] for g in groups],
        proof_location=dict(file=COMP+'/main.tex',label='claim:'+ident,line_start=start+1,line_end=end+1,sha256=sha(block),bytes=len(block)),
        proof_status='complete at the stated original mathematical hypotheses',status='complete human proof; pending independent review',
        scope_class='complete_at_original_mathematical_hypotheses',source_proof_is_not_human_proof=True))
inherited=[]
for comp,ident,use in [
 ('flat_chart_descent_v53','FCD13','Actual homogeneous dehomogenization kernel and quotient identification in ASL14.'),
 ('flat_chart_descent_v53','FCD18','The complete original Noetherian model theorem, now applied to actual geometric chart data in ASL19.'),
 ('global_section_laws_v52','GSL8','The unchanged arbitrary-base projective-complex construction from the original cube model in ASL20.'),
 ('global_section_laws_v52','GSL9','The actual section-Cech comparison and FirstCohomologyVanishes-to-degree-one exactness in ASL21.'),
 ('global_section_laws_v52','GSL10','The original finite-matrix and every-field Perf construction in ASL21.')]:
    pp=WORK/comp/'provenance.json';prev=json.loads(pp.read_text());q=next(x for x in prev['claims'] if x['id']==ident)
    loc=q['proof_location'];data=(WORK/loc['file']).read_bytes();ls=data.splitlines(keepends=True)
    assert sha(data)==prev['proof_file_sha256']
    assert sha(b''.join(ls[loc['line_start']-1:loc['line_end']]))==loc['sha256']
    inherited.append(dict(id=ident,component=comp,title=q['title'],proof_file=loc['file'],proof_file_sha256=prev['proof_file_sha256'],
        proof_block_sha256=loc['sha256'],proof_location=loc,source_commit=PIN,use=use,all_original_premises_retained=True,
        provenance_file=str(pp.relative_to(WORK)),provenance_sha256=sha(pp.read_bytes())))

def declaration(key):
    s=sources[key];ls=(WORK/s['snapshot_file']).read_bytes().splitlines(keepends=True)
    return b''.join(ls[s['line_start']-1:s['line_end']]).decode().split(':= by',1)[0].strip()
endpoints=[]
for ident,key,output in [
 ('ASL4','neighborhood_killing','One neighborhood and exponent, before every original chart index and subopen.'),
 ('ASL5','global_killing','One global power kills every original coordinate of the actual twisted section.'),
 ('ASL7','twisted_extension','Every actual section on the original nonzero locus extends after one power, with the exact coordinate equation.'),
 ('ASL10','twisted_localization','Both original localization clauses for every finite chart set and integer degree.'),
 ('ASL12','actual_twisted_cube_theorem','The full original graded-section cube comparison, with actual restrictions.'),
 ('ASL14','dehom_chart','For every family satisfying the original coordinate-ratio identities, the original chart polynomial evaluation and actual semilinear dehomogenization with all five required properties.'),
 ('ASL15','ordinary_localization','The original actual section-module localization statement on a quasi-compact quasi-separated open.'),
 ('ASL16','affine_projectivity_theorem','Finite presentation and projectivity of the actual section module over the actual affine coordinate ring.'),
 ('ASL18','smooth_flat_scalar','Smoothness or flatness of the original affine chart scalar map from the corresponding property of f.'),
 ('ASL20','actual_finite_complex','The complete original universally valid finite-projective Cech model.'),
 ('ASL21','full_perf','Nonempty Perf for every arbitrary-R smooth IsProjBy morphism and actual line bundle, in its full original scope.')]:
    header=declaration(key)
    endpoints.append(dict(claim_id=ident,source=sources[key],exact_source_declaration_header=header,
        declaration_header_sha256=sha(header.encode()),output=output,status='complete at all original hypotheses; no newly assumed opaque producer'))
standard=dict(id='ASL_STANDARD',name='Ordinary scheme, sheaf and module foundations',kind='standard_background_not_a_selected_project_gap',
    scope_note=('The structure sheaf of Spec B on a principal open is B_f; sheaf existence/uniqueness and stalks; principal opens form an affine basis; '
    'elementary localization, tensor products and finite direct sums; affine-local definitions/dictionaries for smooth and flat morphisms; '
    'finite-projective modules as retracts of finite free modules. All particular twisted power-killing, extension, affine dual bases and actual comparison maps are proved here.'),
    sources=[sources['actual_sections'],sources['literal_projectivity']],globally_discharged_by_this_component=False)
discharged=[
 dict(id='FCD_ACTUAL_AFFINE_SECTIONS',supplied_by=['ASL15','ASL16'],scope='Full original affine actual-section module statement.'),
 dict(id='FCD_ACTUAL_SMOOTH_CHARTS',supplied_by=['ASL18'],scope='Full original cst_smooth_and_flat.'),
 dict(id='FCD_ACTUAL_GEOMETRIC_DEHOM',supplied_by=['ASL4','ASL5','ASL7','ASL10','ASL13','ASL14'],scope='Full original all-integer-twist power extension, localization and actual dehomogenization.'),
 dict(id='FCD_ACTUAL_GEOMETRIC_CUBE',supplied_by=['ASL11','ASL12','ASL19'],scope='Actual full cube and exact common Noetherian geometric model.'),
 dict(id='GSL_PERF_GEOMETRY',supplied_by=['ASL20','ASL21'],scope='Full original universal arbitrary-R smooth IsProjBy Perf producer.'),
 dict(id='GSL_NOETH_CUBE_DATA',supplied_by=['ASL19'],scope='Supplied for every actual smooth-projective section cube needed here; no claim about an arbitrary abstract cube.'),
 dict(id='GSL_CECH_MODEL_DATA',supplied_by=['ASL20'],scope='Supplied for every actual smooth-projective M and its chosen original projective cover.')]
guards=[
 'R is arbitrary, including zero, nilpotent and non-Noetherian rings; no reducedness or flat coefficient change is imposed.',
 'The twisted power-killing and extension theorems hold for every integer d and t; the original Y,H,M and sigma are fixed throughout.',
 'ASL4 chooses one neighborhood and one exponent before all original p,l and every smaller open; ASL5 chooses one exponent for the whole quasi-compact space.',
 'ASL7 first chooses N to clear local denominators, then K to kill the finitely many overlap discrepancies; equality on D(sigma) alone is never cancelled on the ambient overlap.',
 'ASL10--12 include the empty chart set; every restriction and every homogeneous degree is the original one.',
 'ASL12 pullback naturality is not a global H0 base-change isomorphism; ASL17 supplies such an isomorphism only on the relevant affine opens.',
 'ASL14 quantifies every ratio family satisfying the original coordinate identities; division by the unit coordinates of s_i forces equality with the prescribed very-ample family, preserving its surjective polynomial evaluation.',
 'ASL16 constructs a finite dual basis for the actual module over O(V), correcting evaluation identities by additional powers; no Noetherianity of O(V) is used.',
 'ASL19 chooses one R0,C0,Theta before every later base change, with no flatness of R0 to R; the model requires flatness and bijectivity only at nonempty vertices.',
 'ASL20 fixes K and phi once, then proves the original quasi-isomorphism assertion for every later R-algebra and every specified geometric pullback.',
 'ASL21 fixes all matrices, opens, chart indices and coordinate functions before R-prime, g, Y-prime, pi and f-prime; arbitrary specified Cartesian squares are retained.',
 'Perf.exact retains its own FirstCohomologyVanishes antecedent. Such vanishing is not required for existence of Perf and is not proved by this packet.',
 'Global SecBaseChangeSt, SecBaseChangeAnySt, SecTwistSt and Moduli are not declared unconditionally supplied; the independent GSL geometric inputs remain.']
write('provenance.json',dict(schema='rh-proof-provenance/1',**base,source_repository=REPO,claims=claims,new_claim_count=len(claims),original_endpoints=endpoints,independent_reviews=[]))
write('source_manifest.json',dict(schema='rh-source-manifest/1',**base,repository=REPO,snapshot_root=COMP+'/source_snapshot',files=list(files.values()),ranges=list(sources.values()),file_count=len(files),range_count=len(sources),total_bytes=sum(x['bytes'] for x in files.values()),all_files_verified_equal_to_pinned_git_blobs=True))
write('contracts.json',dict(schema='rh-component-contracts/1',**base,claim_ids=[x['id'] for x in claims],completed_original_suppliers=endpoints,quantifier_guards=guards,inherited_inputs=inherited,external_inputs=[standard],formerly_retained_producers_now_supplied=discharged,remaining_global_producers=retained,global_perf_producer_supplied=True,global_section_laws_unconditionally_supplied=False,selected_whole_obligations_closed=[],independent_reviews=[]))
write('inherited_inputs.json',dict(schema='rh-inherited-inputs/1',**base,inputs=inherited))
write('retained_foundations.json',dict(schema='rh-retained-foundations/1',**base,inputs=[standard],remaining_global_producers=retained,scope_note='None of these remaining geometric producers is a hidden hypothesis of ASL21. They are separate inputs of the downstream global section-law theorems.'))
write('explicit_inputs.json',dict(schema='rh-explicit-inputs/1',**base,inputs=[standard],inherited_human_proofs=inherited,original_pointwise_interfaces=endpoints,remaining_global_producers=retained,scope_note='Full original Perf geometry is proved, not assumed. Separate cohomological, rank, polarized base-change and translation producers are retained for the next section-law join.'))
write('closure.json',dict(schema='rh-component-closure/1',**base,new_claim_count=len(claims),completed=[
 'Full original actual twisted power-killing and extension for all integer twists.',
 'Full original localization, dehomogenization and actual graded-section cube comparisons.',
 'Explicit finite dual-basis projectivity and finite presentation of actual affine line-bundle sections.',
 'Actual affine section base-change comparisons for arbitrary coefficient maps and specified Cartesian squares.',
 'The original affine scalar smoothness/flatness theorem.',
 'One actual geometric Noetherian model and the full universal finite-projective Cech model.',
 'Full original nonempty_perf_of_smooth_isProjBy for arbitrary R and every actual line bundle.'],completed_original_endpoint_claim_ids=[x['claim_id'] for x in endpoints],formerly_retained_producers_now_supplied=discharged,pending_actual_geometric_producers=[x['id'] for x in retained],globally_supplied_laws=[],global_perf_producer_supplied=True,global_section_laws_unconditionally_supplied=False,selected_whole_obligations_closed=[],selected_obligation_statuses_unchanged=True,earlier_proof_components_modified=[],graph_nodes_added=0,graph_edges_added=0,independent_reviews=[]))
write('hashes.json',dict(schema='rh-component-hashes/1',**base,proof_blocks={x['id']:x['proof_location']['sha256'] for x in claims},primary_source_files={x['path']:x['sha256'] for x in files.values()},inherited_proof_blocks={x['id']:x['proof_block_sha256'] for x in inherited}))
print(json.dumps(dict(component=COMP,proof_sha256=sha(proof),claims=len(claims),primary_files=len(files),source_ranges=len(sources),inherited_claims=len(inherited)),indent=2))
