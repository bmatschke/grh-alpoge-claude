#!/usr/bin/env python3
"""Bind the classical section-growth replacement to its exact original consumer."""
from pathlib import Path
import argparse
import hashlib
import json
import subprocess

HERE=Path(__file__).resolve().parent
WORK=HERE.parent
COMP=HERE.name
PIN='7cbf7a0c32fca1badf05931879a37c3f8a2b03b4'
REPO='https://github.com/CocoSgt/riemann-hypothesis-lean'
A='src/Development/AbelianVarietyTheory/Proofs/AbelianSchemeLawProofs/'
D='src/Development/AbelianVarietyTheory/Definitions/AbelianSchemeLaws/'
R='src/ReciprocityTheory/ReductiveGroups/ArithmeticGeometry/'
ap=argparse.ArgumentParser()
ap.add_argument('--source-root',type=Path,default=Path('/workspace/scratch/249d32c24541/formal_source'))
args=ap.parse_args()
sha=lambda b:hashlib.sha256(b).hexdigest()
def write(name,obj):
    (HERE/name).write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n')

proof=(HERE/'main.tex').read_bytes()
base=dict(artifact_version='0.57',component=COMP,source_commit=PIN,
          proof_file_sha256=sha(proof),status='written_pending_independent_review')
rows=[]
def src(key,path,lo,hi,decl,prefix=A):
    rows.append((key,prefix+path,lo,hi,decl))

src('polav','ExtensionDescent/NonzeroLocus.lean',59,73,'The original PolAV record',R)
src('abelian','SemiabelianSchemes/AbelianSchemeQuotients/IsAbelianScheme.lean',13,17,
    'IsAbelianScheme: commutative group, smoothness, properness, geometric connectedness',R)
src('bundle','SemiabelianSchemes/CubicalStructures/CubeSymmetricSwapFirst.lean',17,78,
    'LB, IsLB, actual Sec, LinComb and pull',R)
src('lpow','ExtensionDescent/ThetaPt.lean',53,57,'LPow and liftFun',R)
src('secm','ExtensionDescent/ThetaVV.lean',18,60,
    'liftHom, scalar action, actual SecM, toSec and ofSec',R)
src('veryample','FirstCohomologyVanishesSpecOfIsLocalRing.lean',18,29,
    'pw and exact VeryAmpleBy chart data',D)
src('ample_producer','VeryAmpleByOfRelAmple.lean',113,121,'polAV_veryAmpleBy (completed by PBC26)')
src('finite_producer','AbelianVarietyLineBundleSectionsFinite.lean',78,100,
    'sections_finite_of_perf (completed by PBC27)')
src('finite_secm','FiniteOfNotLinearIndependent.lean',242,278,
    'finite_secM for all original integer powers and the literal identity product')
src('power_maps','FiniteOfNotLinearIndependent.lean',280,312,
    'wchart comparison, lcg power identities and actual toPw/ofPw')
src('growth_target','FiniteOfNotLinearIndependent.lean',316,350,
    'secM_finite_and_growth; this packet supplies its entire terminal output by a classical alternative')
src('growth_export','CubeTheoremAndSectionsFiniteGrowthAbelianVariety.lean',38,43,
    'CubeAssembly.sections_growth')
src('rank_consumer','FinrankSectionsLineBundlePowEqPow.lean',223,260,
    'coefficient field and the exact hgrow input of finrank_sections_lineBundlePow_eq_pow')
src('later_join','LawsOfH0EqOneClosedFields.lean',64,93,
    'laws_of_h0_eq_one: separate rank-one, decomposition, vanishing and section-law inputs')

old_contracts=json.loads((WORK/'polarized_base_change_v56/contracts.json').read_text())
completed_input=next(dict(x) for x in old_contracts['remaining_global_producers'] if x['id']=='GSL_FINITE_GROWTH')
retained=[dict(x) for x in old_contracts['remaining_global_producers'] if x['id']!='GSL_FINITE_GROWTH']
for inp in retained:
    for j,s in enumerate(inp.get('sources',[])):
        src('retained_'+inp['id'].lower()+'_'+str(j),s['path'],s['line_start'],s['line_end'],s['declaration'],'')

files,sources={},{}
for key,path,lo,hi,decl in rows:
    if path not in files:
        blob=subprocess.check_output(['git','-C',str(args.source_root),'show',PIN+':'+path])
        assert (args.source_root/path).read_bytes()==blob,path
        dest=HERE/'source_snapshot'/path
        dest.parent.mkdir(parents=True,exist_ok=True)
        dest.write_bytes(blob)
        files[path]=dict(path=path,snapshot_file=str(dest.relative_to(WORK)),bytes=len(blob),
            line_count=len(blob.splitlines()),sha256=sha(blob),file_sha256=sha(blob),source_commit=PIN,
            verified_equal_to_pinned_git_blob=True,url=REPO+'/blob/'+PIN+'/'+path)
    f=files[path]
    ls=(WORK/f['snapshot_file']).read_bytes().splitlines(keepends=True)
    assert 1<=lo<=hi<=len(ls),(key,lo,hi,len(ls))
    part=b''.join(ls[lo-1:hi])
    sources[key]=dict(id='SGV_SRC_'+key.upper(),path=path,declaration=decl,
        line_start=lo,line_end=hi,source_commit=PIN,file_sha256=f['sha256'],
        full_file_sha256=f['sha256'],range_sha256=sha(part),range_bytes=len(part),
        snapshot_file=f['snapshot_file'],verified_equal_to_pinned_git_blob=True,
        url=f['url']+f'#L{lo}-L{hi}')
for inp in retained:
    inp['sources']=[sources['retained_'+inp['id'].lower()+'_'+str(j)]
                    for j in range(len(inp.get('sources',[])))]
    inp['globally_discharged_by_this_component']=False
    inp['boundary_inherited_from']='polarized_base_change_v56/contracts.json'
    if inp['id']=='GSL_GEOM_INTEGRAL':
        inp['completed_subproducer_claim_ids']=['SGV1']
        inp['completed_subproducer']='The actual original P/K identity fiber is geometrically integral, with exact dimension g.'
        inp['remaining_subproducer']='The broader universal arbitrary-base source implication is not asserted as a new endpoint here.'

milne_base=dict(kind='explicit_published_classical_theorem',author='J. S. Milne',
    title='Abelian Varieties',edition='Corrected 2022 version of the 1986 Storrs article',
    url='https://www.jmilne.org/math/xnotes/AVs.pdf',
    field_scope='Arbitrary base fields, including positive characteristic; used here over the original algebraically closed K.',
    attribution='Published input retained explicitly; not newly proved and not attributed to a post-proof exposition.')
published=[dict(milne_base,id='SGV_MILNE_9_1',theorem='Proposition 9.1',printed_page=15,pdf_page_index=14,
    exact_used_statement='An ample invertible sheaf with a nonzero section on an abelian variety has a translation stabilizer of dimension zero.'),
 dict(milne_base,id='SGV_MILNE_13_3_C',theorem='Theorem 13.3(c)',printed_page=25,pdf_page_index=24,
    exact_used_statement='If the translation stabilizer has dimension zero, the invertible sheaf has nonzero cohomology in exactly one degree.'),
 dict(milne_base,id='SGV_MILNE_13_3_B',theorem='Theorem 13.3(b)',printed_page=25,pdf_page_index=24,
    exact_used_statement='For a Cartier divisor D on an abelian variety of dimension g, chi(O(D))=(D^g)/g!, as an equality in Q of integer-valued numerical invariants.')]
background=dict(id='SGV_SCHEME_BACKGROUND',kind='standard_scheme_background',
    scope_note='Smoothness over a field gives regular local rings; regular local rings are domains; smooth relative dimension equals fiber dimension. Also the ordinary sheaf gluing, affine closed-immersion criterion, Veronese embedding and Zariski lemma.',
    primary_references=['https://stacks.math.columbia.edu/tag/04QM',
      'https://stacks.math.columbia.edu/tag/00NN','https://stacks.math.columbia.edu/tag/01V4'])

specs=[
 ('SGV1',[],['polav','abelian'],['SGV_SCHEME_BACKGROUND'],
  'The actual identity product is an abelian variety of dimension g.',
  'Original algebraically closed field, actual Cartesian projections, geometric integrality after every field extension, exact P.g.'),
 ('SGV2',[],['bundle','lpow','secm','power_maps'],['SGV_SCHEME_BACKGROUND'],
  'The literal SecM module and its actual scalar field.',
  'Every integer j; coordinate-preserving section bijection and scalar transport through K=Gamma(Spec K,O), including negative powers.'),
 ('SGV3',['PBC26','SGV2'],['veryample','ample_producer','power_maps'],['SGV_SCHEME_BACKGROUND'],
  'One very ample power, with nonzero sections in every positive power.',
  'N is chosen before t; exact VeryAmpleBy ratios imply a closed immersion; one original section remains nonzero at the identity in every power.'),
 ('SGV4',['SGV1','SGV3'],['polav','growth_target'],['SGV_MILNE_9_1','SGV_MILNE_13_3_C'],
  'Degree-zero concentration for every positive power of the chosen H.',
  'No assumption prime to the characteristic; no identification of original KTriv with a Picard-scheme kernel.'),
 ('SGV5',['SGV1','SGV3','SGV4'],['growth_target'],['SGV_MILNE_13_3_B'],
  'Exact section growth in positive dimension.',
  'All t>=1; Cartier divisor from the actual nonzero section; factorial interpreted in Q, not inverted in K.'),
 ('SGV6',['SGV1'],['polav','growth_target'],['SGV_SCHEME_BACKGROUND'],
  'The zero-dimensional case.',
  'Original algebraic closedness used explicitly; every invertible sheaf on Spec K has one-dimensional sections.'),
 ('SGV7',['PBC27','SGV2','SGV3','SGV5','SGV6'],['finite_secm','growth_target','growth_export','rank_consumer'],[],
  'Full original section-finiteness and two-sided growth output.',
  'Finiteness for every integer j and one N,d>=1 before all t>=1; exact equality with d*t^g, then original c=1,C=d bounds.')]
ls=proof.splitlines(keepends=True)
claims=[]
for ident,deps,groups,external,title,scope in specs:
    lo=next(i for i,l in enumerate(ls) if l.strip()==('% BEGIN '+ident).encode())
    hi=next(i for i,l in enumerate(ls) if l.strip()==('% END '+ident).encode())
    block=b''.join(ls[lo:hi+1])
    claims.append(dict(id=ident,title=title,introduced_in='0.57',classification='B',depends_on=deps,
        external_input_ids=external,scope_note=scope,source_groups=groups,sources=[sources[g] for g in groups],
        proof_location=dict(file=COMP+'/main.tex',label='claim:'+ident,line_start=lo+1,line_end=hi+1,
            sha256=sha(block),bytes=len(block)),proof_status='complete with the explicitly stated inherited and published inputs',
        status='complete human proof; pending independent review',
        scope_class='complete_original_output_by_classical_alternative',source_proof_is_not_human_proof=True))

inherited=[]
for comp,ident,role,use in [
 ('polarized_base_change_v56','PBC26','dependency','The complete actual affine-test very-ample power producer, applied only to the identity test over K.'),
 ('polarized_base_change_v56','PBC27','dependency','The actual all-integer SecM finiteness conclusion over the original algebraically closed K.'),
 ('global_section_laws_v52','GSL19','next_consumer','Its geometric-fiber integrality and fourth (growth/finiteness) input are supplied; rank one and actual section equivalences remain.'),
 ('serre_h1_v55','SHV17','completed_context','The completed full all-cover eventual Serre H1 theorem remains supplied and is not reopened.'),
 ('serre_h1_v55','SHV21','completed_context','The completed homogeneous-polynomial section theorem remains supplied and is not reopened.')]:
    pp=WORK/comp/'provenance.json'
    prev=json.loads(pp.read_text())
    c=next(x for x in prev['claims'] if x['id']==ident)
    loc=c['proof_location'];data=(WORK/loc['file']).read_bytes()
    part=b''.join(data.splitlines(keepends=True)[loc['line_start']-1:loc['line_end']])
    assert sha(data)==prev['proof_file_sha256'] and sha(part)==loc['sha256']
    inherited.append(dict(id=ident,component=comp,role=role,title=c['title'],use=use,
        proof_file=loc['file'],proof_file_sha256=sha(data),proof_block_sha256=sha(part),
        proof_location=loc,source_commit=PIN,all_original_premises_retained=True,
        provenance_file=str(pp.relative_to(WORK)),provenance_sha256=sha(pp.read_bytes())))

completed_input.update(supplied_by=['SGV7'],status='complete original terminal output by the stated classical alternative',
    globally_discharged_by_this_component=True,
    sources=[sources['growth_target'],sources['growth_export'],sources['rank_consumer']],
    completed_subproducer_claim_ids=['PBC27','SGV7'],
    completed_subproducer='Actual all-integer section finiteness and exact dim(V_Nt)=d*t^g with N,d>=1 fixed first.')
completed_input.pop('remaining_subproducer',None)
endpoints=[dict(claim_id='SGV7',source=sources[key],output=out,
    status='complete original terminal conclusion by explicitly attributed classical replacement') for key,out in [
      ('growth_target','The complete secM_finite_and_growth output for every original P over every algebraically closed field.'),
      ('growth_export','The complete CubeAssembly.sections_growth output.'),
      ('rank_consumer','The exact hgrow input, together with the actual P/K integrality input, of the next rank theorem.')]]
scope=dict(full_original_secM_finite_and_growth_output_supplied=True,
    full_original_sections_growth_supplied=True,all_integer_SecM_finiteness_reused=True,
    exact_positive_power_growth_supplied=True,actual_identity_product_and_scalars_retained=True,
    completed_nested_frontier_ids=['GSL_FINITE_GROWTH'],
    general_filtered_polynomial_growth_supplied=False,
    original_rank_one_supplied=False,original_torsion_section_decomposition_supplied=False,
    full_GlobalSectionsRankAlgClosed_supplied=False,
    full_original_all_cover_positive_power_H1_supplier_supplied=False,
    full_SecBaseChangeSt_supplied=False,full_SecBaseChangeAnySt_supplied=False,
    full_SecTwistSt_supplied=False,global_Moduli_supplied=False,
    selected_whole_obligations_closed=[])
guards=[
 'The terminal consumer has algebraically closed K; there is no characteristic-zero, separability or prime-to-characteristic restriction on N or t.',
 'The actual identity product, its two projections and the original scalar action are preserved in the section dictionary.',
 'One N and d are chosen before every t>=1; no uniformity across different P or K is asserted.',
 'The original g is the supplied smooth relative dimension, not a new transcendence-degree parameter.',
 'The zero-dimensional case and t=1 are included explicitly.',
 'PBC27 is used at its actual algebraically closed endpoint, not its broader conditional arbitrary-field implication.',
 'Only Milne9.1 and13.3(b,c) are used; no principal-polarization degree formula or KTriv-to-Picard-kernel identification is assumed.',
 'Vanishing for the selected H powers is classical sheaf cohomology; the original all-cover positive-power law for L is not declared supplied.',
 'The broader filtered-polynomial growth theorem is bypassed for this exact consumer only.',
 'GSL19 still requires rank one and the actual torsion-indexed section equivalences; no whole obligation closes.'
]
comparison=WORK.parent/'comparison_20261124/section_growth_alternative.tex'
adaptation=dict(source_file=str(comparison),sha256=sha(comparison.read_bytes()),
    role='Previously independently reviewed classical replacement, now installed with seven numbered human proofs and exact source bindings.',
    attribution='The mathematical input is Milne; the comparison exercise motivated this consumer-specific route.')

write('provenance.json',dict(schema='rh-proof-provenance/1',**base,source_repository=REPO,
    claims=claims,new_claim_count=len(claims),original_endpoints=endpoints,adaptation=adaptation,independent_reviews=[]))
write('source_manifest.json',dict(schema='rh-source-manifest/1',**base,repository=REPO,
    snapshot_root=COMP+'/source_snapshot',files=list(files.values()),ranges=list(sources.values()),
    file_count=len(files),range_count=len(sources),total_bytes=sum(x['bytes'] for x in files.values()),
    all_files_verified_equal_to_pinned_git_blobs=True,published_inputs=published,background_references=[background]))
write('contracts.json',dict(schema='rh-component-contracts/1',**base,**scope,
    claim_ids=[c['id'] for c in claims],completed_original_suppliers=endpoints,
    completed_input=completed_input,quantifier_guards=guards,inherited_inputs=inherited,
    external_inputs=published+[background],remaining_global_producers=retained,independent_reviews=[]))
write('inherited_inputs.json',dict(schema='rh-inherited-inputs/1',**base,inputs=inherited,adaptation=adaptation))
write('retained_foundations.json',dict(schema='rh-retained-foundations/1',**base,
    inputs=published+[background],remaining_global_producers=retained))
write('explicit_inputs.json',dict(schema='rh-explicit-inputs/1',**base,inputs=published+[background],
    inherited_human_proofs=inherited,original_pointwise_interfaces=endpoints,remaining_global_producers=retained))
write('closure.json',dict(schema='rh-component-closure/1',**base,**scope,new_claim_count=len(claims),
    completed=[x['output'] for x in endpoints],completed_input=completed_input,
    pending_actual_geometric_producers=[x['id'] for x in retained],
    selected_obligation_statuses_unchanged=True,earlier_proof_components_modified=[],
    graph_nodes_added=0,graph_edges_added=0,independent_reviews=[]))
write('hashes.json',dict(schema='rh-component-hashes/1',**base,
    proof_blocks={c['id']:c['proof_location']['sha256'] for c in claims},
    primary_source_files={f['path']:f['sha256'] for f in files.values()},
    inherited_proof_blocks={x['id']:x['proof_block_sha256'] for x in inherited}))
write('status.json',dict(schema='rh-component-status/1',**base,**scope,new_claim_count=len(claims),
    formal_proof_correctness_accepted=True,lean_replay_performed=False,
    proof_style='Detailed same-object classical theorem application, with explicit published inputs and original section coordinates.'))
write('source_mapping.json',dict(schema='rh-source-mapping/1',**base,original_endpoints=endpoints,
    claims=[dict(id=c['id'],sources=c['sources'],scope_note=c['scope_note']) for c in claims]))
write('proof_bindings.json',dict(schema='rh-proof-bindings/1',**base,
    blocks={c['id']:c['proof_location'] for c in claims}))
print(json.dumps(dict(component=COMP,proof_sha256=sha(proof),claims=len(claims),
    primary_files=len(files),source_ranges=len(sources),inherited_bindings=len(inherited)),indent=2))
