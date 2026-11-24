#!/usr/bin/env python3
"""Independent, read-only audit of the v0.46 integration and unchanged v0.45 baseline."""
from pathlib import Path
import argparse
import collections
import hashlib
import json
import re
import subprocess

ROOT=Path(__file__).resolve().parents[1]
OLD=ROOT/'history/version_0_45'
PIN='7cbf7a0c32fca1badf05931879a37c3f8a2b03b4'
ap=argparse.ArgumentParser()
ap.add_argument('--source',type=Path,required=True)
ap.add_argument('--new-reader-sha256',required=True)
ap.add_argument('--cumulative-reader-sha256',required=True)
ap.add_argument('--integration-script-sha256',required=True)
ap.add_argument('--expected-source-files',type=int)
ap.add_argument('--expected-source-ranges',type=int)
ap.add_argument('--output',type=Path,default=ROOT/'reviews_v0_46/integration_main_proof_rigidity.json')
args=ap.parse_args(); source=args.source.resolve()
sha=lambda b:hashlib.sha256(b).hexdigest()
checks=[];errors=[];bindings={}
def need(ok,label,detail=None):
    if ok:checks.append(label)
    else:errors.append(dict(check=label,detail=detail))
def read(path):
    raw=path.read_bytes();bindings[str(path.relative_to(ROOT))]=sha(raw)
    return json.loads(raw)
def dag(graph):
    done,active=set(),set()
    def visit(n):
        if n not in graph:raise AssertionError(('unknown dependency',n))
        if n in active:raise AssertionError(('dependency cycle',n))
        if n in done:return
        active.add(n)
        for d in graph[n]:visit(d)
        active.remove(n);done.add(n)
    for n in graph:visit(n)
    return len(done)

need(subprocess.check_output(['git','-C',str(source),'rev-parse','HEAD'],text=True).strip()==PIN,'exact pinned source HEAD')
cfg=read(ROOT/'increment_v0_46.json')
old=read(OLD/'provenance.json');now=read(ROOT/'provenance.json')
oi=read(OLD/'source_index.json');ni=read(ROOT/'source_index.json')
bc=old['claims'];cs=now['claims'];oldcount=len(bc)
need(oldcount==2677,'baseline has exactly 2677 claims',oldcount)
need(cs[:oldcount]==bc,'all baseline claim objects, sources, proof locations and scopes preserved literally')
need(now['source_files'][:len(old['source_files'])]==old['source_files'],'baseline provenance source inventory preserved literally')
need(ni['source_files'][:len(oi['source_files'])]==oi['source_files'],'baseline source index preserved literally')
preserved=archived=0
manifest=OLD/'SHA256SUMS'
need(manifest.is_file(),'baseline SHA256SUMS exists')
if manifest.is_file():
    nonempty=[x for x in manifest.read_text().splitlines() if x.strip()]
    for line in nonempty:
        expected,rel=line.split('  ',1)
        current,history=ROOT/rel,OLD/rel
        if current.is_file() and sha(current.read_bytes())==expected:preserved+=1
        elif history.is_file() and sha(history.read_bytes())==expected:preserved+=1;archived+=1
        else:errors.append(dict(check='baseline artifact preserved at original bytes',detail=rel))
    need(preserved==len(nonempty),'every baseline artifact preserved in current tree or exact history')
ids=[c['id'] for c in cs];byid={c['id']:c for c in cs}
graph=now['mathematical_dependency_graph']
need(len(ids)==len(set(ids)),'cumulative claim IDs unique')
need(all(graph.get(k)==v for k,v in old['mathematical_dependency_graph'].items()),'all baseline dependency edges preserved literally')
need(set(graph)==set(ids),'dependency graph has exactly cumulative numbered claims')
try:need(dag(graph)==len(cs),'cumulative mathematical dependency graph acyclic')
except AssertionError as e:need(False,'cumulative mathematical dependency graph acyclic',str(e))
order=now['dependency_topological_order'];pos={k:i for i,k in enumerate(order)}
need(len(order)==len(ids) and set(order)==set(ids),'topological order covers all claims exactly once')
need(all(pos.get(d,len(ids))<pos.get(n,-1) for n,ds in graph.items() for d in ds),'topological order respects every edge')

incoming=[];component_bindings={};external_bindings=[]
for component in cfg['components']:
    ledger=read(ROOT/component/'provenance.json')
    incoming.extend(ledger['claims'])
    need(ledger.get('source_commit',PIN)==PIN,component+': component source pin unchanged')
    need(now['component_scope_metadata_as_received_v0_46'].get(component)=={k:v for k,v in ledger.items() if k not in {'claims','source_files','source_inventory','source_groups'}},component+': complete component scope metadata preserved')
    component_bindings[component]=dict(claims=len(ledger['claims']),ledger_sha256=bindings[component+'/provenance.json'])
    external={r['id']:r for key in ['published_applications','classical_and_foundational_inputs','retained_foundations','conditional_inputs']
              for r in ledger.get(key,[]) if isinstance(r,dict) and 'id' in r}
    for c in ledger['claims']:
        names=c.get('external_input_ids',[])+c.get('published_input_ids',[])+c.get('foundation_input_ids',[])+c.get('conditional_input_ids',[])
        for name in names:
            need(name in external,c['id']+': published/foundational identifier has an explicit component record',name)
            need(name not in graph,c['id']+': published/foundational identifier is separate from numbered claim DAG',name)
        if names:external_bindings.append(dict(claim=c['id'],external_input_ids=names))
need([c['id'] for c in cs[oldcount:]]==[c['id'] for c in incoming],'new claim inventory and order match configured component ledgers')
sources={};ranges=set();proofs={}
for c in incoming:
    integrated=byid[c['id']]
    need(integrated['depends_on']==c.get('depends_on',[])==graph[c['id']],c['id']+': literal proof dependencies preserved')
    for key,value in c.items():
        if key not in {'proof_location','sources'}:need(integrated.get(key)==value,c['id']+': component field '+key+' preserved')
    pl=integrated['proof_location'];raw=(ROOT/pl['file']).read_bytes()
    part=b''.join(raw.splitlines(keepends=True)[pl['line_start']-1:pl['line_end']])
    need(sha(part)==pl['sha256']==pl['range_sha256'],c['id']+': exact proof-block bytes')
    need(sha(raw)==pl['file_sha256'],c['id']+': exact proof-file bytes')
    need(re.search(rb'^% BEGIN '+re.escape(c['id'].encode())+rb'\s*$',part,re.M) is not None and re.search(rb'^% END '+re.escape(c['id'].encode())+rb'\s*$',part,re.M) is not None,c['id']+': proof range contains its exact numbered block markers')
    need(len(re.findall(rb'^% BEGIN '+re.escape(c['id'].encode())+rb'\s*$',raw,re.M))==1,c['id']+': proof marker unique in its component')
    proofs[pl['file']]=sha(raw)
    need(len(c.get('sources',[]))==len(integrated.get('sources',[])),c['id']+': source array length retained')
    for original,added in zip(c.get('sources',[]),integrated.get('sources',[])):
        need(all(added.get(k)==v for k,v in original.items() if k!='range_sha256'),c['id']+': source annotations retained')
    for s in integrated.get('sources',[]):
        if 'path' not in s or 'line_start' not in s:continue
        path=s['path']
        if path not in sources:
            data=(source/path).read_bytes()
            need(data==subprocess.check_output(['git','-C',str(source),'show',f'{PIN}:{path}']),'source equals pinned Git blob: '+path)
            sources[path]=data
            snapshot=ROOT/'source_snapshot_v0_46'/path
            need(snapshot.is_file() and snapshot.read_bytes()==data,'source snapshot exact bytes: '+path)
        data=sources[path];lines=data.splitlines(keepends=True);a,b=s['line_start'],s['line_end']
        need(sha(data)==s.get('file_sha256',s.get('full_file_sha256',s.get('sha256'))),c['id']+': source-file hash '+path)
        need(1<=a<=b<=len(lines) and sha(b''.join(lines[a-1:b]))==s['range_sha256'],c['id']+f': source-range hash {path}:{a}-{b}')
        ranges.add((path,a,b))
for label,items in [('provenance',now['source_files']),('index',ni['source_files'])]:
    mapping={s['path']:s for s in items}
    need(len(mapping)==len(items),label+' source paths unique')
    for path,data in sources.items():
        need(path in mapping and mapping[path].get('sha256',mapping[path].get('file_sha256'))==sha(data),label+' source inventory exact hash: '+path)

oldmap=read(ROOT/'dependency_audit_v0_45/obligation_map.json')
newmap=read(ROOT/'dependency_audit_v0_46/obligation_map.json')
oldnodes={n['id']:n for n in oldmap['nodes']};nodes={n['id']:n for n in newmap['nodes']}
need(len(nodes)==len(newmap['nodes'])==121 and set(nodes)==set(oldnodes),'selected sufficient-route graph preserves all 121 nodes')
need(all(nodes[k]['gate']==v['gate'] and nodes[k]['requires']==v['requires'] for k,v in oldnodes.items()),'every selected gate and dependency list preserved')
logical={k:n['requires'] for k,n in nodes.items()}
need(sum(map(len,logical.values()))==161,'selected sufficient-route graph preserves 161 edges')
try:need(dag(logical)==121,'selected sufficient-route graph acyclic')
except AssertionError as e:need(False,'selected sufficient-route graph acyclic',str(e))
closed=set(cfg['closed_selected_leaves'])
need(closed=={'CNR3','TASK_PROP_GK_INSTALL'},'exactly CNR3 and the finite PropGK implication task are newly discharged',sorted(closed))
for cid,previous in oldnodes.items():
    allowed={'category','kind','status','opaque_frontier'} if cid in closed else set()
    for key,value in previous.items():
        if key=='contract' and cid in cfg.get('updated_contracts',{}):continue
        if key in allowed:continue
        need(nodes[cid].get(key)==value,cid+': prior selected node field retained: '+key)
    if cid in closed:
        need(nodes[cid]['predecessor_status_v0_45']=={k:previous[k] for k in ['category','kind','status']},cid+': exact predecessor status retained')
        need(nodes[cid]['status']=='proved_in_stated_scope' and nodes[cid]['kind']=='proved_certificate' and nodes[cid]['category']==cfg['closed_selected_leaves'][cid]['category'] and nodes[cid]['opaque_frontier'] is False,cid+': only reviewed status transition installed')
        need(nodes[cid]['version_0_46_discharge']==cfg['closed_selected_leaves'][cid],cid+': exact reviewed discharge record installed')
need(all(nodes[k]['status']=='proved_in_stated_scope' for k in ['AD_VANISH_K_MATCH','HOST_RIGID_S']),'two inherited v0.42 whole closures remain closed')
closed_status={'proved_in_stated_scope','published_application_checked','complete','closed'}
opens={k for k,n in nodes.items() if n['gate']=='LEAF' and n['status'] not in closed_status}
cats=dict(collections.Counter(nodes[k]['category'] for k in opens))
need(len(opens)==28 and cats=={'C':20,'B':8},'remaining frontier is 28 whole leaves: 20 C and 8 B',cats)
oldreg=read(ROOT/'dependency_audit_v0_45/remaining_leaf_register.json')
reg=read(ROOT/'dependency_audit_v0_46/remaining_leaf_register.json')
need(opens=={n['id'] for n in oldreg['records']}-closed,'all other original open whole contracts remain open')
need({n['id'] for n in reg['records']}==opens and all(n==nodes[n['id']] for n in reg['records']),'remaining register exactly matches current selected nodes')
def reachable(start):
    seen=set();todo=[start]
    while todo:
        k=todo.pop()
        if k not in seen:seen.add(k);todo.extend(logical[k])
    return seen
rh=reachable('ORDINARY_RH');grh=reachable('DIRICHLET_GRH')
need(len(opens&rh&grh)==21 and len((opens&grh)-rh)==7 and not((opens&rh)-grh),'21 shared and 7 GRH-only open obligations; none RH-only')
need('COUNT_III_PRODUCER' not in rh and 'COUNT_III_PRODUCER' in grh,'Count III remains GRH-only')
need({'GLOBAL_DENOMINATOR','GLOBAL_RETAINED_DEFECT','GLOBAL_PERIOD_HEIGHT','GLOBAL_LOCAL_GAIN','GLOBAL_SPECTRAL','RIG_II'}<=opens,'all other full global quantitative and global assembly producer obligations remain open')
need(all(newmap['source_inputs'].get(k)==v for k,v in oldmap['source_inputs'].items()),'selected baseline source inputs preserved')
for k,r in newmap['source_inputs'].items():need(sha((ROOT/r['file']).read_bytes())==r['sha256'],'selected source-input byte binding: '+k)
for k,progress in cfg.get('selected_node_progress',{}).items():
    need(nodes[k].get('version_0_46_progress')==progress,k+': current nested progress matches configuration')
for k,contract in cfg.get('updated_contracts',{}).items():
    need(nodes[k]['contract']==contract,k+': current contract narrative matches configuration')
    need(nodes[k].get('historical_contract_narrative_v0_45')==oldnodes[k]['contract'],k+': prior exact contract narrative retained separately')

targets=read(ROOT/'next_source_targets.json');oldtargets=read(OLD/'next_source_targets.json')
need(targets['targets']==oldtargets['targets'] and len(targets['targets'])==245,'all 245 historical source targets preserved literally')
disp=read(ROOT/'dependency_audit_v0_46/target_disposition.json');od=read(ROOT/'dependency_audit_v0_45/target_disposition.json')
need(len(disp['records'])==len(od['records'])==245 and len(disp['scope_groups'])==107,'245 dispositions and 107 scope groups preserved')
need(all(all(b.get(k)==v for k,v in a.items()) for a,b in zip(od['records'],disp['records'])),'historical target disposition fields retained with additive current notes')
need(disp['scope_groups']==od['scope_groups'],'historical target grouping unchanged')
checkpoint=read(ROOT/'continuation_checkpoint.json')
need(checkpoint['remaining_major_inputs']==cfg['remaining_major_inputs'] and checkpoint['next_targets']==cfg['next_targets'],'continuation checkpoint contains current frontier and priorities')
need(targets['next_local_priority']==cfg['next_targets'],'next source priorities are current')
need(now['scope']==cfg['status'],'active provenance scope is the current v0.46 status')
expected_active_audit={
    'artifact_version':'0.46',
    'file':'dependency_audit_v0_46/obligation_map.json',
    'explanatory_chapter':'dependency_audit_v0_46/main.tex',
    'complete_backlog_disposition':'dependency_audit_v0_46/target_disposition.json',
    'remaining_leaf_register':'dependency_audit_v0_46/remaining_leaf_register.json',
    'route_coverage':'dependency_audit_v0_46/route_coverage.json',
    'scope':'Selected sufficient interfaces with completed consumers distinct from open producers and shared work.'}
need(checkpoint['current_dependency_audit']==expected_active_audit,'active checkpoint audit references are the exact v0.46 records')
for key,file in expected_active_audit.items():
    if key in {'artifact_version','scope'}:continue
    need((ROOT/file).is_file(),'active audit destination exists: '+key)
integration_script=(ROOT/'integrate_v0_46.py').read_bytes()
bindings['integrate_v0_46.py']=sha(integration_script)
need(sha(integration_script)==args.integration_script_sha256,'integration generator matches the announced frozen version')


# Exact completed implications remain separate from their producer premises.
component_closures={}
closure_keys=['whole_obligations_closed','whole_obligation_closures',
              'new_global_frontier_leaf_closures','whole_selected_leaf_closed']
for component in cfg['components']:
    # ARO records the same explicit closure boundary in its contracts record.
    path=ROOT/component/('contracts.json' if component=='arithmetic_rows_v46' else 'closure.json')
    need(path.is_file(),component+': explicit component closure record exists')
    if not path.is_file():continue
    closure=read(path);component_closures[component]=closure
    present=[k for k in closure_keys if k in closure]
    need(bool(present),component+': whole-closure scope explicitly recorded')
    need(all(closure[k] in ([],False,{}) for k in present),component+': root integration alone installs the reviewed whole selected transitions')
    expected=closure.get('proof_file_sha256',closure.get('main_tex_sha256'))
    need(expected==proofs[component+'/main.tex'],component+': closure binds exact frozen main proof')
need(set(cfg['components'])=={'rank_three_congruence_v46','prop_gk_installation_v46','arithmetic_rows_v46','integral_cusp_lattices_v46','global_local_gain_v46'},'exact five reviewed continuation components')
for cid,component in [('CNR3','rank_three_congruence_v46'),('TASK_PROP_GK_INSTALL','prop_gk_installation_v46')]:
    review_file=component+('/review_RNC1_RNC16_root.json' if cid=='CNR3' else '/review_PGK1_PGK6_root.json')
    review=read(ROOT/review_file);whole=review['selected_whole_contract_reviewed']
    need(review['result']=='PASS' and whole['id']==cid and whole['full_original_contract_closed_in_stated_scope'] is True and whole['no_weaker_replacement'] is True,cid+': independent review accepts exactly the whole original selected contract')
    need(whole['baseline_version']=='0.45' and whole['baseline_contract_sha256']==sha(oldnodes[cid]['contract'].encode()),cid+': whole-contract review binds the literal baseline contract')
    need(review['proof_sha256']==proofs[component+'/main.tex'],cid+': whole-contract review binds final proof bytes')
    need(set(cfg['closed_selected_leaves'][cid]['claims'])=={x['id'] for x in review['claims_reviewed']},cid+': exact full reviewed claim range supplies closure')
rnc=component_closures.get('rank_three_congruence_v46',{})
pgk=component_closures.get('prop_gk_installation_v46',{})
need(rnc.get('foundation_retention_explicit') is True and rnc.get('OneChar_and_unconditional_PropGK_remain_separate') is True,'CNR3 retains named classical foundations and separate OneChar producer')
need(rnc.get('status')=='complete_at_stated_scope_independently_reviewed','RNC1-16 complete with independent review')
need(pgk.get('status')=='complete_implication_independently_reviewed' and pgk.get('OneChar_is_not_newly_assumed_as_a_closed_foundation') is True,'PGK closes only the finite implication with explicit OneChar antecedent')
need({'ONE_CHAR','TASK_ONE_CHAR_PROOF','RIG_II'}<=set(pgk.get('retained_open_producers',[])),'PGK explicitly retains the original arithmetic producers')
pgkp=read(ROOT/'prop_gk_installation_v46/provenance.json')
onechar=next(x for x in pgkp['conditional_inputs'] if x['id']=='PGK_ONE_CHAR')
need(onechar['kind']=='explicit_original_conditional_premise' and onechar['newly_proved'] is False,'original OneChar remains an unproved logical antecedent')
need(all('PGK_ONE_CHAR' in byid[c]['conditional_input_ids'] for c in ['PGK5','PGK6']),'both PropGK length consumers explicitly carry OneChar')
need('PGK_ONE_CHAR' not in graph and nodes['ONE_CHAR']['status']=='open_producer' and 'RIG_II' in opens,'no conditional premise is promoted to a proved DAG node or closed producer')
icl=component_closures.get('integral_cusp_lattices_v46',{})
need(icl.get('full_LatFull_unconditional_supplier_closed') is False,'ICL does not claim unconditional full-lattice spanning')
for key in ['foundation_retention_explicit','all_original_tests_retained','all_positive_weights_retained','both_Boolean_MLat_levels_retained']:
    need(icl.get(key) is True,'ICL exact retained scope: '+key)
needed_icl={'ICL_PRINCIPAL_CHART_INPUT','ICL_LEVEL_SYSTEM_INPUT','ICL_RAW_GAUSSIAN_INPUT','ICL_SHORT_DICTIONARY_INPUT','ICL_RAMIFIED_JET_INPUT','ICL_CANONICAL_NAB_INPUT'}
need(all(set(x['remaining_input_ids'])==needed_icl for x in icl.get('conditional_original_endpoints',[])) and len(icl.get('conditional_original_endpoints',[]))==3,'all three ICL spanning/transport endpoints retain the same six exact producer inputs')
glg=component_closures.get('global_local_gain_v46',{})
for key in ['exact_error_and_constants_preserved','all_five_LinkG_fields','full_admission_and_actual_compatibility_retained','mean_hypothesis_explicit','both_original_integral_models','actual_rank_and_DVR_preserved']:
    need(glg.get(key) is True,'GLG exact original conditional scope: '+key)
aro=component_closures.get('arithmetic_rows_v46',{})
need({'ARO_ORIGINAL_SETTING','ARO_ROWS_FIN_DIM','ARO_ORIGINAL_TIES','ARO_COUNT_THEOREM_ANTECEDENT'}<=set(aro.get('external_input_ids',[])),'ARO retains the original common setting, row finiteness, ties and arithmetic count antecedents')
need(aro.get('endpoint_claim')=='ARO24' and aro.get('count_endpoint_claim')=='ARO28' and aro.get('family_consumer_claim')=='ARO30','ARO distinguishes structure, conditional count installation and common-family consumption')
need({'GLOBAL_DENOMINATOR','GLOBAL_RETAINED_DEFECT','GLOBAL_PERIOD_HEIGHT','GLOBAL_LOCAL_GAIN','GLOBAL_SPECTRAL'}<=opens,'all five actual global quantitative producer contracts remain open')
need(not newmap['validation'].get('all_original_finite_local_character_laws_complete',False),'unused fourth local character law not claimed')
need(now['validation'].get('lean_build') is False and now['validation'].get('kernel_replay') is False and now['validation'].get('dependency_graph_is_lean_transitive_audit') is False,'human/source integration is not presented as Lean replay or formal transitive dependency extraction')
need(len(incoming)==91 and len(cs)==2768,'exact new and cumulative claim counts: 91 and 2768')
new_categories=dict(collections.Counter(c['classification'] for c in incoming))
need(new_categories=={'B':90,'A':1},'new proof classification is exactly 90 B and 1 A',new_categories)
# Baseline source snapshots, newly added snapshots, and indexes have different scopes;
# the new manifest must enumerate precisely the sources actually cited this increment.
sm=read(ROOT/'source_snapshot_v0_46/manifest.json')
need(sm['commit']==PIN,'new source snapshot records exact pin')
need(len(sm['files'])==len(sources) and {r['path'] for r in sm['files']}==set(sources),'new source manifest has exactly all cited source files')
for record in sm['files']:
    data=sources.get(record['path'],b'')
    need(record['sha256']==sha(data) and record['bytes']==len(data) and record['line_count']==len(data.splitlines()),'new source snapshot record exact: '+record['path'])
coverage=read(ROOT/'dependency_audit_v0_46/route_coverage.json')
need(coverage['graph_sha256']==sha((ROOT/'dependency_audit_v0_46/obligation_map.json').read_bytes()),'selected route coverage bound to current graph')
need(coverage['ordinary_rh_open_leaf_count']==21 and coverage['dirichlet_grh_open_leaf_count']==28 and coverage['shared_open_leaf_count']==21,'route coverage counts are exact')
need(coverage['shared_open_leaf_ids']==sorted(opens&rh&grh) and coverage['dirichlet_grh_only_open_leaf_ids']==sorted((opens&grh)-rh) and coverage['ordinary_rh_only_open_leaf_ids']==[],'route coverage IDs match independent reachability')
delta=read(ROOT/'dependency_audit_v0_46/closure_delta.json')
need(delta['closed_selected_leaves']==cfg['closed_selected_leaves'] and delta['closed_nested_producers']==cfg['closed_nested_producers'] and delta['prior_open_leaf_count']==30 and delta['current_open_leaf_count']==28 and delta['new_proof_claims']==91,'closure delta separates producer progress from exactly two reviewed whole-leaf discharges')
apps=read(ROOT/'dependency_audit_v0_46/published_applications.json')
need(apps['freshly_checked_applications']==cfg['published_applications'],'published-application scope preserved literally')
need(apps['inherited_registry']['sha256']==sha((ROOT/apps['inherited_registry']['file']).read_bytes()),'inherited published registry remains byte-bound')

def ancestors(cid):
    seen=set();todo=list(graph[cid])
    while todo:
        k=todo.pop()
        if k not in seen:seen.add(k);todo.extend(graph[k])
    return seen
# An out-of-ancestry reference is an error unless its complete proof block has
# been read and an explicit non-premise reason is recorded here.
exceptions={
 ('RNC1','RNC2'):'RNC1 is the abstract general RA polarized published application. Its RNC2 reference identifies a later application check for rank-two essential self-duality; RNC2 is not used to prove the abstract statement.',
 ('RNC2','RNC1'):'RNC2 constructs the actual rank-two adelization and verifies that it meets RNC1 hypotheses. It does not use the Galois representation conclusion of RNC1 in constructing the cusp.',
 ('RNC6','CX1'):'RNC6 compares its finite-cell method to the earlier rank-four argument, then proves the complete bounded-rank coefficient and cell count directly. It does not use the rank-four CX1 conclusion.'
}


reference_scan=[]
for c in incoming:
    pl=byid[c['id']]['proof_location'];raw=(ROOT/pl['file']).read_bytes()
    block=b''.join(raw.splitlines(keepends=True)[pl['line_start']-1:pl['line_end']])
    named=set(re.findall(r'\b[A-Z]{2,}\d+\b',block.decode()))&set(graph)
    named.discard(c['id']);outside=named-ancestors(c['id'])
    explained={k:exceptions[(c['id'],k)] for k in outside if (c['id'],k) in exceptions}
    missing=outside-set(explained)
    need(not missing,c['id']+': named proof uses represented in dependency ancestry',sorted(missing))
    reference_scan.append(dict(claim=c['id'],proof_range_sha256=sha(block),named_claims=sorted(named),
        named_claims_outside_ancestry=sorted(outside),reviewed_nondependency_references=explained,
        substantive_missing_dependencies=sorted(missing)))

# Component review schemas differ only in bookkeeping; normalize them while
# checking every whole-file hash and every claimed mathematical block separately.
review_paths=[]
for component in cfg['components']:
    for path in sorted((ROOT/component).glob('*review*.json')):
        record=json.loads(path.read_bytes())
        entries=record.get('reviewed_claims',record.get('claims_reviewed',record.get('claims',list(record.get('proof_hashes',{})))))
        if entries and record.get('reviewer'):
            review_paths.append(str(path.relative_to(ROOT)))
reviewed=set();review_coverage=[];new_ids={c['id'] for c in incoming}
need(bool(review_paths),'independent mathematical review files found')
for rel in review_paths:
    review=read(ROOT/rel)
    result=review.get('status',review.get('result'))
    need(result=='PASS',rel+': independent mathematical review PASS')
    file=review.get('proof_file',str(Path(rel).parent/'main.tex'));data=(ROOT/file).read_bytes()
    expected=[review[k] for k in ['proof_file_sha256','proof_sha256','main_tex_sha256'] if k in review]
    need(bool(expected) and all(h==sha(data) for h in expected),rel+': every reviewed whole-file hash is current')
    need(review.get('source_commit',PIN)==PIN,rel+': review uses exact source pin')
    entries=review.get('reviewed_claims',review.get('claims_reviewed',review.get('claims',list(review.get('proof_hashes',{})))))
    found=[]
    for entry in entries:
        if isinstance(entry,str):
            cid=entry;h=review.get('proof_hashes',{}).get(cid);entry_status=result
        else:
            cid=entry.get('id',entry.get('claim'))
            h=entry.get('proof_range_sha256',entry.get('block_sha256'))
            entry_status=entry.get('status',entry.get('result',result))
        need(cid in new_ids,rel+': reviewed claim is a new numbered claim '+str(cid))
        need(entry_status=='PASS',rel+': reviewed claim passed '+str(cid))
        if cid not in byid:continue
        pl=byid[cid]['proof_location']
        need(pl['file']==file,rel+': reviewed claim is in the bound proof file '+cid)
        block=b''.join(data.splitlines(keepends=True)[pl['line_start']-1:pl['line_end']])
        need(h in {sha(block),sha(block.rstrip(b'\r\n'))},rel+': current claim block matches reviewed bytes '+cid)
        if isinstance(entry,dict) and 'line_start' in entry:
            need((entry['line_start'],entry['line_end'])==(pl['line_start'],pl['line_end']),rel+': reviewed block positions match '+cid)
        reviewed.add(cid);found.append(cid)
    need(len(found)==len(set(found)),rel+': reviewed claim inventory has no duplicate')
    review_coverage.append(dict(file=rel,reviewer=review['reviewer'],claims=len(found),claim_ids=found,proof_file=file,proof_file_sha256=sha(data)))
need(reviewed==new_ids,'all and only 91 new claims have matching independent mathematical review coverage',sorted(new_ids-reviewed))
# Explicitly test the two frozen reader artifacts without binding progress reports
# and README, which are produced only after independent validation completes.
reader_files={'RH_new_proofs_v0_46.tex':args.new_reader_sha256,'RH_readable_reconstruction_v0_46.tex':args.cumulative_reader_sha256}

def reader_wrap(text):
    # The assembly adds only discretionary line-breaking commands to monospaced
    # identifiers and escaped underscores. Check the entire expanded chapter.
    def mono(match):
        t=re.sub(r'(?<=[a-z])(?=[A-Z])',lambda _:r'\allowbreak ',match[1])
        t=re.sub(r'\.(?!\\allowbreak)',lambda _:r'.\allowbreak ',t)
        t=re.sub(r'([/:])(?!\\allowbreak)',lambda m:m[1]+r'\allowbreak ',t)
        t=re.sub(r'\\_(?!\\allowbreak)',lambda _:r'\_\allowbreak ',t)
        return r'\texttt{'+t+'}'
    text=re.sub(r'\\texttt\{([^{}]*)\}',mono,text)
    return re.sub(r'\\_(?!\\allowbreak)',lambda _:r'\_\allowbreak ',text)
for file,h in reader_files.items():
    raw=(ROOT/file).read_bytes();bindings[file]=sha(raw)
    need(sha(raw)==h,file+': exact frozen reader bytes')
    for component in cfg['components']:
        need(reader_wrap((ROOT/component/'main.tex').read_text()).encode() in raw,file+': includes entire exact component modulo specified discretionary breaks: '+component)

stats=read(ROOT/'integration_stats_v0_46.json')
computed=dict(new_claims=len(incoming),cumulative_claims=len(cs),selected_nodes=121,selected_edges=161,
    open_count=28,open_categories=cats,shared_open=21,extra_grh_open=7,
    new_source_files_checked=len(sources),new_unique_source_ranges_checked=len(ranges))
if args.expected_source_files is not None:need(len(sources)==args.expected_source_files,'exact announced source-file count',len(sources))
if args.expected_source_ranges is not None:need(len(ranges)==args.expected_source_ranges,'exact announced source-range count',len(ranges))
need(stats==computed,'reported integration statistics equal independent computation',dict(reported=stats,computed=computed))
bindings[str(Path(__file__).resolve().relative_to(ROOT))]=sha(Path(__file__).read_bytes())
for p,h in proofs.items():need(sha((ROOT/p).read_bytes())==h,'proof file stable during audit: '+p)
for p,data in sources.items():need((source/p).read_bytes()==data and (ROOT/'source_snapshot_v0_46'/p).read_bytes()==data,'source and snapshot stable during audit: '+p)
for p,h in bindings.items():need(sha((ROOT/p).read_bytes())==h,'audit input stable during review: '+p)
result=dict(schema='rh-independent-integration-review/1',reviewer='main_proof_rigidity',date='2026-11-23',
    source_commit=PIN,status='PASS' if not errors else 'FAIL',
    scope='Independent preservation, source/proof bytes, dependency, selected-route, closure and current-scope audit; no Lean replay.',
    statistics=computed,new_claim_categories=new_categories,baseline_claims_preserved=oldcount,baseline_source_files_preserved=len(old['source_files']),
    baseline_manifest_artifacts_preserved=preserved,baseline_artifacts_retained_in_history=archived,
    claims_and_sources_checked=len(incoming),passed_check_count=len(checks),errors=errors,input_bindings=bindings,
    new_proof_files=proofs,component_ledgers=component_bindings,named_proof_reference_scan=reference_scan,
    named_external_input_bindings=external_bindings,independent_mathematical_review_coverage=review_coverage,
    exact_whole_closures=cfg['closed_selected_leaves'],current_remaining_scopes={k:n.get('version_0_46_progress') for k,n in nodes.items() if 'version_0_46_progress' in n},
    semantic_scope_review=[
        'RNC1 applies the exact published Galois/compatibility results only after matching their polarized and Shin-regular weight hypotheses. RNC2-16 preserve the actual original representations and flags, build bounded-rank full cusp labels, and choose the whole orbit product integer before every later coefficient datum. The whole original CNR3 closure has an independently bound exact-contract review.',
        'PGK1-6 prove the full finite CNR3 and OneChar to PropGK implication, including all original GD fields, exact same-kernel coefficient realization, inverse-Frobenius scalar, and normalized valuation sum. ONE_CHAR and RIG_II remain open; only the separate finite B installation task closes.',
        'ARO constructs the structural reduction, Haar-fiber, idempotent and row objects on the original supplied setting. Actual common setting, form ties, finite-dimensional rows and arithmetic count inputs are retained rather than silently produced by a finite-algebra argument.',
        'ICL proves finite generation of the whole original integral cusp lattice. Its identity-cover and spanning/transport implications preserve the original IsNab connection and five supplied producer groups. No unconditional spanning, arbitrary higher-cover or common-geometric-family theorem is inferred.',
        'GLG proves the full original logarithmic counting theorem and exact local-lattice and LinkG consumers. Their actual compatibility, admitted-family, local first-growth and mean-deficit producers remain separate. The five original global quantitative obligations remain open.',
        'All 121 selected sufficient-route nodes and 161 edges are retained. Exactly CNR3 and TASK_PROP_GK_INSTALL move to proved status; the remaining 28 whole obligations have categories 20 C and 8 B, with 21 shared plus 7 extra GRH obligations. All 2677 predecessor claims and their source arrays are preserved literally.'
    ],limitations=['Recorded graph is the human-proof dependency graph, not a mechanically extracted Lean transitive graph.',
        'Independent mathematical component reviews remain separately bound; this integration audit does not reprove every component theorem.',
        'No Lean compilation, kernel replay, formal correctness challenge or completed unconditional human proof of RH/GRH is asserted.'])
args.output.parent.mkdir(parents=True,exist_ok=True)
args.output.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
print(json.dumps(dict(status=result['status'],statistics=computed,passed_checks=len(checks),errors=errors,output=str(args.output)),ensure_ascii=False,indent=2))
raise SystemExit(bool(errors))
