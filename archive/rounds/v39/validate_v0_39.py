#!/usr/bin/env python3
"""Check exact continuity, source/proof/review bindings and current audit integrity."""
from pathlib import Path
import argparse,collections,hashlib,json,re,subprocess
ROOT=Path(__file__).resolve().parent
OLD=ROOT/'history/version_0_38'
PIN='7cbf7a0c32fca1badf05931879a37c3f8a2b03b4'
p=argparse.ArgumentParser(description=__doc__)
p.add_argument('--repo',type=Path,required=True)
args=p.parse_args();repo=args.repo.resolve()
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def digest(b):return hashlib.sha256(b).hexdigest()
def read(p):return json.loads(p.read_text())
def write(p,d):p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n')
assert subprocess.check_output(['git','-C',str(repo),'rev-parse','HEAD']).decode().strip()==PIN
cfg=read(ROOT/'increment_v0_39.json');old=read(OLD/'provenance.json');now=read(ROOT/'provenance.json')
oldclaims={c['id']:c for c in old['claims']};claims={c['id']:c for c in now['claims']}
assert len(claims)==len(now['claims'])==len(old['claims'])+cfg['expected_new_claims']
for cid,c in oldclaims.items():
    for k,v in c.items():assert claims[cid][k]==v,('changed predecessor claim',cid,k)
for cid,edges in old['mathematical_dependency_graph'].items():
    assert now['mathematical_dependency_graph'][cid]==edges,('changed old claim edges',cid)
new=[c for c in now['claims'] if c['id'] not in oldclaims]
assert len(new)==cfg['expected_new_claims']
for c in new:
    loc=c['proof_location'];raw=(ROOT/loc['file']).read_bytes()
    part=b''.join(raw.splitlines(keepends=True)[loc['line_start']-1:loc['line_end']])
    assert digest(part)==loc['sha256'],('proof range',c['id'])
    if 'bytes' in loc:assert len(part)==loc['bytes']

manifest_total=0;archived=0;cache={}
def fsha(p):
    if p not in cache:cache[p]=sha(p)
    return cache[p]
for line in (OLD/'SHA256SUMS').read_text().splitlines():
    if not line.strip():continue
    value,rel=line.split('  ',1);manifest_total+=1
    if (ROOT/rel).is_file() and fsha(ROOT/rel)==value:continue
    assert (OLD/rel).is_file() and fsha(OLD/rel)==value,('predecessor file lost',rel)
    archived+=1
graph=now['mathematical_dependency_graph'];active=set();done=set()
def visit(k):
    assert k in graph and k not in active,('claim dependency error',k)
    if k in done:return
    active.add(k)
    for nxt in graph[k]:visit(nxt)
    active.remove(k);done.add(k)
for k in graph:visit(k)
assert set(claims)==set(graph)==done

source_cache={};ranges=0;unique=set()
def source(r):
    global ranges
    path=r['path'];expected=r.get('sha256',r.get('file_sha256',r.get('source_full_file_sha256',r.get('full_file_sha256'))))
    if path not in source_cache:
        raw=(repo/path).read_bytes();source_cache[path]=(digest(raw),raw.splitlines(keepends=True))
    filehash,lines=source_cache[path]
    assert filehash==expected,('source file',path)
    a,b=r.get('line_start'),r.get('line_end')
    rh=r.get('range_sha256',r.get('source_range_sha256'))
    if a is not None and b is not None and rh:
        assert 1<=a<=b<=len(lines),('range bounds',path,a,b)
        assert digest(b''.join(lines[a-1:b]))==rh,('source range',path,a,b)
        ranges+=1;unique.add((path,a,b,rh))
for r in now['source_files']:source(r)
for c in now['claims']:
    for r in c['sources']:source(r)

targets=read(ROOT/'next_source_targets.json')['targets'];prior=read(OLD/'next_source_targets.json')['targets']
disp=read(ROOT/'dependency_audit_v0_39/target_disposition.json')
assert len(prior)==len(targets)==len(disp['records'])==245
for i,(a,b,r) in enumerate(zip(prior,targets,disp['records']),1):
    for k,v in a.items():assert b[k]==v,('changed inherited target',i,k)
    assert r['original_index_one_based']==i
    assert r['predecessor_record_sha256']==digest(json.dumps(a,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode())
    assert b['version_0_39_disposition']==r
    source(a)
assert len(disp['scope_groups'])==107

aud=ROOT/'dependency_audit_v0_39'
g=read(aud/'obligation_map.json');nodes={n['id']:n for n in g['nodes']}
assert len(nodes)==len(g['nodes'])==121
prior_selected=read(ROOT/'dependency_audit_v0_38/obligation_map.json')
prior_nodes={n['id']:n for n in prior_selected['nodes']}
assert set(nodes)==set(prior_nodes), 'Selected node inventory changed'
for ident,n in nodes.items():
    assert n['gate']==prior_nodes[ident]['gate'] and n['requires']==prior_nodes[ident]['requires'],('Selected logical edge changed',ident)
assert nodes['TASK_GL_FINAL_ASSEMBLY']['status']=='proved_in_stated_scope'
assert nodes['TASK_LINK_GL_INSTALL']['status']=='proved_implication_with_open_inputs'
assert nodes['GLOBAL_GL_PAIR']['status']=='proved_conditional_join_with_open_producers'
selected_active=set();selected_done=set()
def sel(k):
    assert k in nodes and k not in selected_active,('selected graph error',k)
    if k in selected_done:return
    selected_active.add(k);n=nodes[k]
    assert n['category'] in ['A','B','C','D']
    assert n['gate'] in ['AND','LEAF']
    if n['gate']=='LEAF':assert not n['requires']
    for v in n['requires']:sel(v)
    selected_active.remove(k);selected_done.add(k)
for k in g['roots']:sel(k)
assert selected_done==set(nodes),'Detached selected node'
def reachable(k):
    seen=set();todo=[k]
    while todo:
        q=todo.pop()
        if q in seen:continue
        seen.add(q);todo+=nodes[q]['requires']
    return seen
rh=reachable('ORDINARY_RH');grh=reachable('DIRICHLET_GRH');full=reachable('GLOBAL_FULL_RANK')
assert 'COUNT_III_PRODUCER' not in rh and 'COUNT_III_PRODUCER' in grh
assert {'COUNT_I_PRODUCER','COUNT_II_SUPPORT','COUNT_V_PRODUCER'}<=rh&grh
assert not any(k.startswith('TASK_GL4') for k in full)
assert 'TASK_GL_FINAL_ASSEMBLY' not in full
assert 'TASK_GL6_SIZE_SETTING' in nodes['GLOBAL_RAMIFIED_INCLUSION']['requires']
assert 'TASK_GL6_SIZE_SETTING' in nodes['TASK_LINK_GL_INSTALL']['requires']
assert nodes['CERT_RSL_FULLNESS']['requires']==[]
assert 'SECOND_LAYER_COMPATIBLE_SELECTION' in nodes['GLOBAL_SECOND_LAYER_MATCH']['requires']
assert g['selected_interface_cuts']['common_family']['source_argument_count']==10
refids={n['id'] for n in g['work_refinement_nodes']}
optids={n['id'] for n in g['optional_routes']}
assert not set(nodes).intersection(refids|optids)
for label,item in g['source_inputs'].items():
    q=Path(item['file']);assert not q.is_absolute()
    assert sha(ROOT/q)==item['sha256'],('graph input',label)
assert sha(ROOT/g['backlog_crosswalk']['file'])==g['backlog_crosswalk']['sha256']

# Independent review evidence is bound to the exact released proof bytes.
review_specs=[(comp+'_review.json',comp,list(range(1,len(cfg['component_claims'][comp])+1))) for comp in cfg['components']]
registry=[];reviewed_new_claims=set()
def review_status(r):return str(r.get('verdict',r.get('result',r.get('status',''))))
def review_hash(r,kind):
    nested={'proof':'main_tex','provenance':'provenance','closure':'closure'}[kind]
    rf=r.get('reviewed_files',{})
    fallback=rf.get(nested,{}).get('sha256') if isinstance(rf,dict) else None
    return r.get(kind+'_file_sha256',r.get(kind+'_sha256',fallback))
for name,comp,ids in review_specs:
    q=ROOT/'reviews_v0_39'/name;r=read(q)
    assert review_status(r).startswith('PASS'),name
    for key in ['required_fixes','required_corrections','required_changes_remaining','outstanding_required_corrections','unresolved_issues','unresolved_review_issues','open_findings']:
        assert not r.get(key,[]),(name,key)
    assert r.get('all_required_corrections_resolved',True),(name,'unresolved correction flag')
    prefix=re.sub(r'\d+$','',cfg['component_claims'][comp][0])
    expected_review={prefix+str(i) for i in ids}
    actual_review=set(r.get('claims_reviewed',r.get('reviewed_claims',[b['id'] for b in r.get('proof_blocks',[])])))
    assert actual_review==expected_review,('review claim coverage',name,actual_review,expected_review)
    reviewed_new_claims.update(actual_review)
    h=review_hash(r,'proof')
    assert h==sha(ROOT/comp/'main.tex'),('review proof binding',name)
    assert review_hash(r,'provenance')==sha(ROOT/comp/'provenance.json'),('review provenance',name)
    assert review_hash(r,'closure')==sha(ROOT/comp/'closure.json'),('review closure',name)
    if r.get('published_applications_file_sha256'):
        assert r['published_applications_file_sha256']==sha(ROOT/comp/'published_applications.json'),('review published input',name)
    registry.append(dict(review_file='reviews_v0_39/'+name,review_sha256=sha(q),
       component=comp,claim_indices_reviewed=ids,proof_file=comp+'/main.tex',proof_sha256=h,result='PASS'))
assert reviewed_new_claims=={c['id'] for c in new},'Incomplete new mathematical review coverage'
q=ROOT/'reviews_v0_39/selected_route_graph_review.json';r=read(q)
assert review_status(r).startswith('PASS')
graph_review_hash=r.get('graph_file_sha256',r.get('graph_sha256',r.get('graph',{}).get('sha256')))
assert graph_review_hash==sha(aud/'obligation_map.json'),'Graph review hash stale'
for key in ['required_corrections','unresolved_review_issues']:
    assert not r.get(key,[]),('graph review issue',key)
for key in ['narrative','standalone_audit']:
    if key in r:assert sha(ROOT/r[key]['file'])==r[key]['sha256'],('graph review text binding',key)
if r.get('narrative_file_sha256'):
    assert r['narrative_file_sha256']==sha(aud/'main.tex'),'Graph narrative review stale'
if r.get('readable_audit_file_sha256'):
    assert r['readable_audit_file_sha256']==sha(ROOT/'RH_dependency_audit_v0_39.txt'),'Graph TXT review stale'
for item in r.get('reviewed_files',[]):
    if isinstance(item,dict) and 'file' in item and 'sha256' in item:
        assert sha(ROOT/item['file'])==item['sha256'],('reviewed graph input',item['file'])
registry.append(dict(review_file='reviews_v0_39/'+q.name,review_sha256=sha(q),
 graph_file='dependency_audit_v0_39/obligation_map.json',graph_sha256=graph_review_hash,result='PASS'))
write(ROOT/'reviews_v0_39/release_review_registry.json',dict(artifact_version='0.39',
 status='Final released bytes independently reviewed in the scopes below.',
 supersedes='Older pending-review annotations inside preserved component metadata.',
 records=registry))

tex=read(ROOT/'tex_validation.json')
assert tex['syntax_compile_succeeded'] and not tex['undefined_references_or_citations']
assert not tex['pdf_generated'] and tex['missing_character_warnings']==0
assert tex['tex_sha256']==sha(ROOT/'RH_readable_reconstruction_v0_39.tex')
assert (ROOT/'RH_dependency_audit_v0_39.txt').is_file()
notes=read(ROOT/'continuation_checkpoint.json')['next_step_notes']
assert {Path(n['file']).name for n in notes}=={'next_analytic_and_common.txt','next_count_ii.txt','next_division_and_readings.txt'}
for n in notes:assert sha(ROOT/n['file'])==n['sha256'],('continuation note',n['file'])
note_sources_checked=0
for p in (ROOT/'continuation_notes_v0_39').glob('*_sources.json'):
    n=read(p);assert n['source_commit']==PIN
    main=p.with_name(p.name.replace('_sources.json','.txt'))
    assert sha(main)==n['note_sha256'],('continuation source-note binding',p.name)
    for item in n.get('source_ranges',n.get('source_anchors',[])):
        source(item);note_sources_checked+=1
    for item in n.get('component_bindings',[]):
        assert sha(ROOT/item['file'])==item['sha256'],('continuation component binding',p.name,item['file'])
reg=read(aud/'remaining_leaf_register.json')
expected={n['id'] for n in nodes.values() if n['gate']=='LEAF' and n['status'] not in ['proved_in_stated_scope','published_application_checked']}
assert {n['id'] for n in reg['records']}==expected
assert len(expected)==33
assert collections.Counter(n['category'] for n in reg['records'])=={'C':22,'B':9,'D':2}
prior_open={n['id'] for n in prior_nodes.values() if n['gate']=='LEAF' and n['status'] not in ['proved_in_stated_scope','published_application_checked']}
assert prior_open==expected,'Whole selected open-leaf inventory must remain unchanged'
assert not expected-prior_open,'Unexpected new selected leaf'
assert nodes['BASE_THETA_CUSPIDAL_EXTENSION']['status']=='proved_in_stated_scope'
assert nodes['BASE_THETA_CUSPIDAL_EXTENSION']['category']=='B'
audit_text=(ROOT/'RH_dependency_audit_v0_39.txt').read_text()
leaf_by_id={n['id']:n for n in reg['records']}
headings=list(re.finditer(r'^\d+\. ([A-Z][A-Z0-9_]+) — ([ABCD]) — .+$',audit_text,re.M))
assert len(headings)==len(expected) and {m[1] for m in headings}==expected
for m in headings:
    # Each contract is one paragraph; separate group headings are not part of it.
    body=audit_text[m.end():].strip().split('\n\n',1)[0]
    assert ' '.join(body.split())==' '.join(leaf_by_id[m[1]]['contract'].split()),('readable contract',m[1])
    assert m[2]==leaf_by_id[m[1]]['category']
fresh=read(aud/'published_applications.json')['freshly_checked_applications']
component_apps=[]
for comp in cfg['components']:
    p=ROOT/comp/'published_applications.json'
    if not p.exists():continue
    a=read(p)
    component_apps+=a if isinstance(a,list) else a.get('applications',a.get('freshly_checked_applications',[]))
assert {a['id'] for a in fresh}=={a['id'] for a in component_apps}
assert len(fresh)==len(component_apps)
assert {'RPI_COCHARACTER_PARABOLICS','RPI_RELATIVE_ROOT_SETUP','RPI_REAL_SIEGEL_COVER','PQL_CHEN_1','PQL_CHEN_2','PQL_CHEN_3'}<={a['id'] for a in fresh}
countcut=g['selected_interface_cuts']['count_ii_v037']
assert countcut['coupled_rule']['logic']=='AND'
assert countcut['coupled_rule']['conclusion']=='COUPLED_ORIGINAL_CHOICE_B1_B2'
assert 'same' in countcut['coupled_rule']['binding']
assert 'No arbitrary-Kap B1 or B2 closure' in countcut['binding']
assert set(countcut['remaining_nested'])=={'JSP_ORIGINAL_ORDINARY_DATA','JSP_FOUR_HIDA_ENDPOINTS','JSP_SAME_IDEAL_HASAUT','JSP_SINGLE_POINT_RAW'}
thetacut=g['selected_interface_cuts']['theta_v037']
for retained in ['Initial boundedness','FinPair','readings','rational tests','base rows']:
    assert retained in thetacut['residual'],('lost analytic producer',retained)
assert 'BackForm.exists_multMap' in thetacut['nested_closed']
assert 'SPR13' in now['mathematical_dependency_graph']['ASB14']
assert 'ASB14' not in now['mathematical_dependency_graph']['SPR13']
assert {'ASB3','ASB4'}<=set(now['mathematical_dependency_graph']['SPR13'])
assert len(g['selected_interface_cuts']['common_realization_v037']['remaining_packets'])==7
current_theta=g['selected_interface_cuts']['theta_v038']
assert current_theta['whole_selected_closed']==['BASE_THETA_CUSPIDAL_EXTENSION']
assert set(current_theta['remaining'])=={'BASE_THETA_READINGS','BASE_THETA_RATIONAL_TESTS','SLR_BASE_ROWS_PRODUCER'}
assert 'CuspRapidDecay' in current_theta['outside_scope']
current_count=g['selected_interface_cuts']['count_ii_v038']
assert {'CRW_ACTUAL_S4','CRW_PATCHED_MAPS_MODULES_S5','CRW_COEFFICIENT_PROELL_DESCENT'}<=set(current_count['remaining_nested'])
assert 'ell=3' in current_count['binding'] and 'No universal' in current_count['binding']
current_common=g['selected_interface_cuts']['common_realization_v038']
assert 'generic_multiplicity_pair_integrability' in current_common['remaining_packets']
assert 'original_nonzero_chain_and_group_tie' in current_common['remaining_packets']
assert 'DivRows3' in current_common['outside_scope']
for key in ['component_closure']:
    for item in [current_count,current_common]:assert sha(ROOT/item[key]['file'])==item[key]['sha256']
assert 'WithTw(WithSm Cprime)' in nodes['DESIGN_CHOICES_COMMON']['contract']
assert 'cT(eps,y)=cTmin(y)' in nodes['DESIGN_CHOICES_COMMON']['contract']
for word in ['For every family','eventually','LiftTie.theta','mtRead','mjRead','ThDef3','Bundle.P.A3','P.Zs','P.S0']:
    assert word in nodes['BASE_THETA_READINGS']['contract'],('lost original reading guard',word)
assert read(aud/'closure_delta.json')['closed_selected_leaves']==[]
# Current exact scopes; predecessor cuts above remain historical, unchanged.
for key,value in prior_selected['selected_interface_cuts'].items():
    assert g['selected_interface_cuts'][key]==value,('changed historical interface cut',key)
current_count39=g['selected_interface_cuts']['count_ii_v039']
assert set(current_count39['newly_closed_nested'])=={'ORIGINAL_S4','ORIGINAL_TWQUOT','ORIGINAL_COREBC_TO_RAW_PROELL_DESCENT'}
assert set(current_count39['remaining_nested'])=={'JSP_ORIGINAL_ORDINARY_DATA','JSP_FOUR_HIDA_ENDPOINTS','JSP_SAME_IDEAL_HASAUT','CORE_LIMITING_PATCHED_MAPS_MODULES_S5','CORE_TO_COREBC_COEFFICIENT_NORMALIZATION_UNIT'}
assert 'ell=3' in current_count39['binding'] and 'same' in current_count39['completed'].lower()
current_common39=g['selected_interface_cuts']['common_realization_v039']
assert 'EXACT_ROW_PAIR_INTEGRABILITY' in current_common39['newly_closed_nested']
assert 'FIRST_DIVDEF3_ORIGINAL_PREMISES' in current_common39['newly_closed_nested']
assert 'generic_multiplicity_pair_integrability' not in current_common39['remaining_packets']
assert {'common_geometric_Fits_Moved_realization','actual_ChT_LfT_Reps_and_primitive_tests','original_eta_agreement_for_ReadL','original_nonzero_chain_and_group_tie'}<=set(current_common39['remaining_packets'])
assert 'DivRows3' in current_common39['outside_scope'] and 'CuspRapidDecay' in current_common39['outside_scope']
for cut in [current_count39,current_common39]:
    for item in cut['component_closures']:assert sha(ROOT/item['file'])==item['sha256']
for text in ['ChT/LfT/Reps','eta','same']:
    assert text.lower() in nodes['BASE_THETA_READINGS']['contract'].lower(),('lost reading guard',text)
assert len(g['nodes'])==121 and sum(len(n['requires']) for n in g['nodes'])==161
assert g['validation']['original_entire_S4_complete']
assert g['validation']['original_full_CoreBC_to_Raw_proell_descent_complete']
assert g['validation']['first_DivDef3_extra_RowPairInt_discharged']
assert g['validation']['actual_common_construction_not_claimed']
coverage=read(aud/'route_coverage.json')
assert coverage['graph_sha256']==sha(aud/'obligation_map.json')
assert set(coverage['shared_open_leaf_ids'])==rh&grh&expected
assert set(coverage['ordinary_rh_only_open_leaf_ids'])==(rh&expected)-grh
assert set(coverage['dirichlet_grh_only_open_leaf_ids'])==(grh&expected)-rh
assert coverage['ordinary_rh_open_leaf_count']==len(rh&expected)==26
assert coverage['dirichlet_grh_open_leaf_count']==len(grh&expected)==33
assert coverage['shared_open_leaf_count']==len(rh&grh&expected)==26
assert coverage['shared_categories']=={'C':18,'B':6,'D':2}
result=dict(artifact_version='0.39',result='PASS',source_commit=PIN,
 predecessor_claims_preserved=len(oldclaims),new_claims=len(new),claims=len(claims),
 predecessor_manifest_files_preserved=manifest_total,predecessor_files_resolved_through_archive=archived,
 original_claim_fields_preserved=True,original_source_arrays_preserved=True,original_claim_edges_preserved=True,
 new_proof_ranges_checked=len(new),indexed_source_files=len(now['source_files']),
 distinct_source_files_checked=len(source_cache),claim_source_ranges=sum(len(c['sources']) for c in now['claims']),
 source_ranges_checked=ranges,unique_source_ranges_checked=len(unique),
 inherited_targets_preserved_and_dispositioned=245,scope_groups=107,
 claim_graph_acyclic=True,selected_graph='dependency_audit_v0_39/obligation_map.json',
 selected_graph_sha256=sha(aud/'obligation_map.json'),selected_graph_inputs_hash_checked=True,
 selected_node_count=len(nodes),rh_reachable_nodes=len(rh),dirichlet_grh_reachable_nodes=len(grh),
 all_selected_nodes_root_reachable=True,open_leaf_count=len(expected),
 ordinary_rh_open_leaf_count=26,dirichlet_grh_open_leaf_count=33,shared_open_leaf_count=26,
 additional_selected_whole_leaves_closed=0,
 additional_selected_whole_leaf_ids=[],
 coupled_original_Choice_B1_B2_scope_checked=True,
 original_pointwise_and_Sobolev_producers_complete_on_exact_inputs=True,
 initial_target_FinPair_and_seed_bound_complete=True,
 full_selected_theta_extension_complete_on_common_data=True,
 exact_original_row_pair_integrability_complete=True,
 universal_quotient_height_CuspRapidDecay_not_claimed=True,
 selected_full_block_completion_and_ChainAbs_comparison_complete=True,
 original_entire_S4_and_full_TWQuot_complete=True,
 full_CoreBC_to_Raw_proell_descent_complete=True,
 normalized_Core_limiting_patching_S5_and_coefficient_normalization_Unit_remain=True,
 first_DivDef3_extra_RowPairInt_discharged=True,
 original_given_data_side_and_reader_constructors_complete=True,
 full_ReadL_original_eta_guard_retained=True,
 second_DivRows3_separate=True,
 freshly_checked_published_applications=len(fresh),
 continuation_note_source_ranges_checked=note_sources_checked,
 common_Bundle_BWit_consumers_complete_with_original_inputs_retained=True,
 open_leaf_categories=dict(collections.Counter(n['category'] for n in reg['records'])),
 readable_audit_sha256=sha(ROOT/'RH_dependency_audit_v0_39.txt'),
 readable_audit_words=len(audit_text.split()),readable_exact_contracts_checked=len(headings),
 full_rank_excludes_GL4_and_final_assembly=True,guarded_FamU_size_task_explicit=True,
 independent_reviews=registry,historical_RF16_correction_explicit=True,
 all_new_claims_independently_reviewed=True,independently_reviewed_new_claims=len(reviewed_new_claims),
 tex_validation=tex,lean_build=False,kernel_replay=False,
 scope='Source/proof continuity, selected audit and TeX checks. Independent mathematical review is recorded separately; formal correctness is accepted, not reverified.')
write(ROOT/'validation_v0_39.json',result)
cp=read(ROOT/'continuation_checkpoint.json');cp['validation']=result;write(ROOT/'continuation_checkpoint.json',cp)
print(json.dumps({k:v for k,v in result.items() if k not in ['independent_reviews','tex_validation','scope']},indent=2))
