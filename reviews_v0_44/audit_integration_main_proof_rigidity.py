#!/usr/bin/env python3
"""Independent, read-only audit of the v0.44 integration and unchanged v0.43 baseline."""
from pathlib import Path
import argparse
import collections
import hashlib
import json
import re
import subprocess

ROOT=Path(__file__).resolve().parents[1]
OLD=ROOT/'history/version_0_43'
PIN='7cbf7a0c32fca1badf05931879a37c3f8a2b03b4'
ap=argparse.ArgumentParser()
ap.add_argument('--source',type=Path,required=True)
ap.add_argument('--output',type=Path,default=ROOT/'reviews_v0_44/integration_main_proof_rigidity.json')
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
cfg=read(ROOT/'increment_v0_44.json')
old=read(OLD/'provenance.json');now=read(ROOT/'provenance.json')
oi=read(OLD/'source_index.json');ni=read(ROOT/'source_index.json')
bc=old['claims'];cs=now['claims'];oldcount=len(bc)
need(oldcount==2441,'baseline has exactly 2441 claims',oldcount)
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
    need(now['component_scope_metadata_as_received_v0_44'].get(component)=={k:v for k,v in ledger.items() if k not in {'claims','source_files','source_inventory','source_groups'}},component+': complete component scope metadata preserved')
    component_bindings[component]=dict(claims=len(ledger['claims']),ledger_sha256=bindings[component+'/provenance.json'])
    external={r['id']:r for key in ['published_applications','classical_and_foundational_inputs','retained_foundations']
              for r in ledger.get(key,[]) if isinstance(r,dict) and 'id' in r}
    for c in ledger['claims']:
        names=c.get('external_input_ids',[])+c.get('published_input_ids',[])
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
            snapshot=ROOT/'source_snapshot_v0_44'/path
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

oldmap=read(ROOT/'dependency_audit_v0_43/obligation_map.json')
newmap=read(ROOT/'dependency_audit_v0_44/obligation_map.json')
oldnodes={n['id']:n for n in oldmap['nodes']};nodes={n['id']:n for n in newmap['nodes']}
need(len(nodes)==len(newmap['nodes'])==121 and set(nodes)==set(oldnodes),'selected sufficient-route graph preserves all 121 nodes')
need(all(nodes[k]['gate']==v['gate'] and nodes[k]['requires']==v['requires'] for k,v in oldnodes.items()),'every selected gate and dependency list preserved')
logical={k:n['requires'] for k,n in nodes.items()}
need(sum(map(len,logical.values()))==161,'selected sufficient-route graph preserves 161 edges')
try:need(dag(logical)==121,'selected sufficient-route graph acyclic')
except AssertionError as e:need(False,'selected sufficient-route graph acyclic',str(e))
need(cfg['closed_selected_leaves']=={},'no new whole selected leaf closure is claimed')
for k,n in nodes.items():
    for field in ['status','category','kind','gate','requires','evidence','bindings','joint_witness_constraint']:
        if field in oldnodes[k]:need(n.get(field)==oldnodes[k][field],k+': baseline selected '+field+' preserved')
for cid,previous in oldnodes.items():
    for key,value in previous.items():
        if key=='contract' and cid in cfg.get('updated_contracts',{}):continue
        need(nodes[cid].get(key)==value,cid+': prior selected node field retained: '+key)
need(all(nodes[k]['status']=='proved_in_stated_scope' for k in ['AD_VANISH_K_MATCH','HOST_RIGID_S']),'two inherited v0.42 whole closures remain closed')
closed_status={'proved_in_stated_scope','published_application_checked','complete','closed'}
opens={k for k,n in nodes.items() if n['gate']=='LEAF' and n['status'] not in closed_status}
cats=dict(collections.Counter(nodes[k]['category'] for k in opens))
need(len(opens)==31 and cats=={'C':22,'B':9},'remaining frontier stays 31 whole leaves: 22 C and 9 B',cats)
oldreg=read(ROOT/'dependency_audit_v0_43/remaining_leaf_register.json')
reg=read(ROOT/'dependency_audit_v0_44/remaining_leaf_register.json')
need(opens=={n['id'] for n in oldreg['records']},'all original open whole contracts remain open')
need({n['id'] for n in reg['records']}==opens and all(n==nodes[n['id']] for n in reg['records']),'remaining register exactly matches current selected nodes')
def reachable(start):
    seen=set();todo=[start]
    while todo:
        k=todo.pop()
        if k not in seen:seen.add(k);todo.extend(logical[k])
    return seen
rh=reachable('ORDINARY_RH');grh=reachable('DIRICHLET_GRH')
need(len(opens&rh&grh)==24 and len((opens&grh)-rh)==7 and not((opens&rh)-grh),'24 shared and 7 GRH-only open obligations; none RH-only')
need('COUNT_III_PRODUCER' not in rh and 'COUNT_III_PRODUCER' in grh,'Count III remains GRH-only')
need({'GLOBAL_DENOMINATOR','GLOBAL_RETAINED_DEFECT','GLOBAL_PERIOD_HEIGHT','GLOBAL_LOCAL_GAIN','GLOBAL_SPECTRAL','COUNT_II_SUPPORT','RIG_II'}<=opens,'all full global quantitative and same-ideal/support producer obligations remain open')
need(all(newmap['source_inputs'].get(k)==v for k,v in oldmap['source_inputs'].items()),'selected baseline source inputs preserved')
for k,r in newmap['source_inputs'].items():need(sha((ROOT/r['file']).read_bytes())==r['sha256'],'selected source-input byte binding: '+k)
for k,progress in cfg.get('selected_node_progress',{}).items():
    need(nodes[k].get('version_0_44_progress')==progress,k+': current nested progress matches configuration')
for k,contract in cfg.get('updated_contracts',{}).items():
    need(nodes[k]['contract']==contract,k+': current contract narrative matches configuration')
    need(nodes[k].get('historical_contract_narrative_v0_43')==oldnodes[k]['contract'],k+': prior exact contract narrative retained separately')

targets=read(ROOT/'next_source_targets.json');oldtargets=read(OLD/'next_source_targets.json')
need(targets['targets']==oldtargets['targets'] and len(targets['targets'])==245,'all 245 historical source targets preserved literally')
disp=read(ROOT/'dependency_audit_v0_44/target_disposition.json');od=read(ROOT/'dependency_audit_v0_43/target_disposition.json')
need(len(disp['records'])==len(od['records'])==245 and len(disp['scope_groups'])==107,'245 dispositions and 107 scope groups preserved')
need(all(all(b.get(k)==v for k,v in a.items()) for a,b in zip(od['records'],disp['records'])),'historical target disposition fields retained with additive current notes')
need(disp['scope_groups']==od['scope_groups'],'historical target grouping unchanged')
checkpoint=read(ROOT/'continuation_checkpoint.json')
need(checkpoint['remaining_major_inputs']==cfg['remaining_major_inputs'] and checkpoint['next_targets']==cfg['next_targets'],'continuation checkpoint contains current frontier and priorities')
need(targets['next_local_priority']==cfg['next_targets'],'next source priorities are current')
need(now['scope']==cfg['status'],'active provenance scope is the current v0.44 status')
expected_active_audit={
    'artifact_version':'0.44',
    'file':'dependency_audit_v0_44/obligation_map.json',
    'explanatory_chapter':'dependency_audit_v0_44/main.tex',
    'complete_backlog_disposition':'dependency_audit_v0_44/target_disposition.json',
    'remaining_leaf_register':'dependency_audit_v0_44/remaining_leaf_register.json',
    'route_coverage':'dependency_audit_v0_44/route_coverage.json',
    'scope':'Selected sufficient interfaces with completed consumers distinct from open producers and shared work.'}
need(checkpoint['current_dependency_audit']==expected_active_audit,'active checkpoint audit references are the exact v0.44 records')
for key,file in expected_active_audit.items():
    if key in {'artifact_version','scope'}:continue
    need((ROOT/file).is_file(),'active audit destination exists: '+key)
integration_script=(ROOT/'integrate_v0_44.py').read_bytes()
bindings['integrate_v0_44.py']=sha(integration_script)
need(sha(integration_script)=='72feb7b5e331a97144b3cf9c9f6f6d21f5a96f7fc1a74e79d6ec8a72e2e3de9a','integration generator includes the reviewed current-scope and current-audit corrections')


# Exact component boundaries remain separate from the whole selected contracts.
component_closures={}
closure_keys=['whole_obligations_closed','whole_obligation_closures',
              'new_global_frontier_leaf_closures','whole_selected_leaf_closed']
for component in cfg['components']:
    closure=read(ROOT/component/'closure.json');component_closures[component]=closure
    present=[k for k in closure_keys if k in closure]
    need(bool(present),component+': whole-closure scope explicitly recorded')
    need(all(closure[k] in ([],False,{}) for k in present),component+': no whole selected leaf closure claimed')
    expected=closure.get('proof_file_sha256',closure.get('main_tex_sha256'))
    need(expected==proofs[component+'/main.tex'],component+': closure binds exact frozen main proof')
bcs=component_closures['base_change_v44'];gua=component_closures['galois_assembly_v44']
hep=component_closures['hecke_eigenpoints_v44'];jrp=component_closures['ring_properties_v44']
need(bcs['original_named_base_change_input_preserved'] and bcs['all_positive_speh_lengths_preserved'] and bcs['all_original_rank_and_local_and_infinity_scopes_preserved'],'BCS retains exact original base-change foundation, ranks, places and every positive Speh length')
need(gua['foundation_retention_explicit'],'GUA keeps original RowT, correspondence and period foundations explicit')
need(hep['arithmetic_pt_before_good_guard'] and hep['full_laws_after_every_scalar_extension'] and hep['prime_3_retained'],'HEP preserves all-point existence, exact Good flag guard, all scalar extensions and prime 3')
need(jrp['original_ideal_and_coefficient_ring_preserved'] and jrp['top_ideal_included'] and jrp['V0ok_guard_preserved'] and jrp['universal_polynomial_law_scope_preserved'],'JRP preserves the same ideal and ring, top ideal, auxiliary guard and full polynomial-law scope')
need(byid['BCS8']['classification']=='A' and byid['BCS8'].get('published_input_ids')==['BCS_MW_GENERIC_UNITARY'],'generic-unitary classification is a named checked published application')
need('BCS_MW_GENERIC_UNITARY' not in graph and 'BCS8' in graph['GUA4'],'shared generic-unitary application is an actual claim dependency; published identifier is separate')
need(not newmap['validation'].get('all_original_finite_local_character_laws_complete',False),'current metadata does not claim the unused fourth admLq character law')
for flag in ['actual_Galois_decorated_automorphic_parts_complete','bare_original_same_J_density_complete','full_original_ordinary_Hecke_point_record_complete','full_original_same_J_RingProps_complete']:
    need(newmap['validation'].get(flag) is True,'current completed nested endpoint recorded: '+flag)
need(newmap['validation'].get('actual_global_estimate_producers_not_claimed') is True,'full global quantitative producers remain explicitly unclaimed')
need(now['validation'].get('lean_build') is False and now['validation'].get('kernel_replay') is False and now['validation'].get('dependency_graph_is_lean_transitive_audit') is False,'human/source integration is not presented as Lean replay or formal transitive dependency extraction')
need(len(incoming)==119 and len(cs)==2560,'exact new and cumulative claim counts: 119 and 2560')
new_categories=dict(collections.Counter(c['classification'] for c in incoming))
need(new_categories=={'B':117,'A':2},'new proof classification is exactly 117 B and 2 A',new_categories)
# Baseline source snapshots, newly added snapshots, and indexes have different scopes;
# the new manifest must enumerate precisely the sources actually cited this increment.
sm=read(ROOT/'source_snapshot_v0_44/manifest.json')
need(sm['commit']==PIN,'new source snapshot records exact pin')
need(len(sm['files'])==len(sources) and {r['path'] for r in sm['files']}==set(sources),'new source manifest has exactly all cited source files')
for record in sm['files']:
    data=sources.get(record['path'],b'')
    need(record['sha256']==sha(data) and record['bytes']==len(data) and record['line_count']==len(data.splitlines()),'new source snapshot record exact: '+record['path'])
coverage=read(ROOT/'dependency_audit_v0_44/route_coverage.json')
need(coverage['graph_sha256']==sha((ROOT/'dependency_audit_v0_44/obligation_map.json').read_bytes()),'selected route coverage bound to current graph')
need(coverage['ordinary_rh_open_leaf_count']==24 and coverage['dirichlet_grh_open_leaf_count']==31 and coverage['shared_open_leaf_count']==24,'route coverage counts are exact')
need(coverage['shared_open_leaf_ids']==sorted(opens&rh&grh) and coverage['dirichlet_grh_only_open_leaf_ids']==sorted((opens&grh)-rh) and coverage['ordinary_rh_only_open_leaf_ids']==[],'route coverage IDs match independent reachability')
delta=read(ROOT/'dependency_audit_v0_44/closure_delta.json')
need(delta['closed_selected_leaves']=={} and delta['closed_nested_producers']==cfg['closed_nested_producers'] and delta['prior_open_leaf_count']==delta['current_open_leaf_count']==31 and delta['new_proof_claims']==119,'closure delta separates nested producer completion from unchanged whole obligations')
apps=read(ROOT/'dependency_audit_v0_44/published_applications.json')
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
 ('LTP15','LTP12'):'LTP15 repeats only the choice of a nonzero scalarization described at the start of LTP12. That choice follows directly from the LTP1 separating-family theorem, already a recorded premise of LTP15. The LTP12 unramifiedness conclusion is not used.',
 ('BCS9','BCS6'):'BCS9 identifies the descending product by the expression displayed in BCS6. Its cosocle proof uses BCS8 and the recorded segment/order foundations; it does not use BCS6 Hermitian duality or its quotient conclusion.',
 ('BCS12','BCS10'):'BCS12 restates the hypotheses of BCS10: positive-rank discrete V, AscEmb(V,P,d), and normalized P. Its infinity-character proof uses BCS4, BCS7 and BCS11, all recorded. It does not use the local IsSpeh conclusion of BCS10.',
 ('UPA5','GUA12'):'The final sentence identifies the HasSatGL normalization derived from the directly matched Gross theorem with the parameter notation used in GUA12. No GUA12 theorem conclusion is used to prove the Satake application.',
 ('OFL15','OFL5'):'OFL15 names OFL5--OFL14 as consumers of its inertia-distinctness conclusion. Its independent proof uses original local Artin surjectivity and the original valuation/degree sign, not a conclusion of OFL5.',
 ('OFL15','OFL14'):'OFL15 names OFL5--OFL14 as consumers of its inertia-distinctness conclusion. Its independent proof uses original local Artin surjectivity and the original valuation/degree sign, not a conclusion of OFL14.'
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
        entries=record.get('reviewed_claims',record.get('claims_reviewed',record.get('claims',[])))
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
    entries=review.get('reviewed_claims',review.get('claims_reviewed',review.get('claims',[])))
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
need(reviewed==new_ids,'all and only 119 new claims have matching independent mathematical review coverage',sorted(new_ids-reviewed))
# Explicitly test the two frozen reader artifacts without binding progress reports
# and README, which are produced only after independent validation completes.
reader_files={
 'RH_new_proofs_v0_44.tex':'3f9caec5a3c5b50e57162dfd6a6b5a250501a6cf99ee285fc587f292cfebcd27',
 'RH_readable_reconstruction_v0_44.tex':'30331f6f4ba2295b3e429421dea10fe8733025ed44535f374afb190352d3b67a'}
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

stats=read(ROOT/'integration_stats_v0_44.json')
computed=dict(new_claims=len(incoming),cumulative_claims=len(cs),selected_nodes=121,selected_edges=161,
    open_count=31,open_categories=cats,shared_open=24,extra_grh_open=7,
    new_source_files_checked=len(sources),new_unique_source_ranges_checked=len(ranges))
need(stats==computed,'reported integration statistics equal independent computation',dict(reported=stats,computed=computed))
bindings[str(Path(__file__).resolve().relative_to(ROOT))]=sha(Path(__file__).read_bytes())
for p,h in proofs.items():need(sha((ROOT/p).read_bytes())==h,'proof file stable during audit: '+p)
for p,data in sources.items():need((source/p).read_bytes()==data and (ROOT/'source_snapshot_v0_44'/p).read_bytes()==data,'source and snapshot stable during audit: '+p)
for p,h in bindings.items():need(sha((ROOT/p).read_bytes())==h,'audit input stable during review: '+p)
result=dict(schema='rh-independent-integration-review/1',reviewer='main_proof_rigidity',date='2026-11-23',
    source_commit=PIN,status='PASS' if not errors else 'FAIL',
    scope='Independent preservation, source/proof bytes, dependency, selected-route, closure and current-scope audit; no Lean replay.',
    statistics=computed,new_claim_categories=new_categories,baseline_claims_preserved=oldcount,baseline_source_files_preserved=len(old['source_files']),
    baseline_manifest_artifacts_preserved=preserved,baseline_artifacts_retained_in_history=archived,
    claims_and_sources_checked=len(incoming),passed_check_count=len(checks),errors=errors,input_bindings=bindings,
    new_proof_files=proofs,component_ledgers=component_bindings,named_proof_reference_scan=reference_scan,
    named_external_input_bindings=external_bindings,independent_mathematical_review_coverage=review_coverage,
    exact_whole_closures=[],current_remaining_scopes={k:n.get('version_0_44_progress') for k,n in nodes.items() if 'version_0_44_progress' in n},
    semantic_scope_review=[
        'BCS consumes the exact original BaseChangeIsobaricN input; GUA consumes the original RowT/PropsB attachment and local/period foundations. The generic-unitary theorem is one checked published application shared through BCS8.',
        'All positive Speh lengths remain in the construction. A length-one cuspidal conclusion is obtained only under the original irreducibility premise. No purity theorem, universal temperedness or optional endShape endpoint is claimed.',
        'The same actual local maps, global representation and quotient descent fill PartAltAlt and UnitaryPointProperties. AuTeichEx supplies the earlier AFS same-ideal separation consumer and yields bare TJDense on the original ideal.',
        'OFL uses raw Weil action before Frobenius semisimplification, all original period bridges and exact ordinary ordering. Its local Artin injectivity argument retains the original Chevalley-units input. HEP provides an arithmetic-point representation before imposing Good on its ordinary-flag and potential-crystallinity conclusions.',
        'JRP gives the entire RingProps record for that same IsJ ideal, including the top ideal. It preserves determinant polynomial laws after all scalar extensions and retains the original auxiliary V0ok condition.',
        'The four later Hida endpoints, both original rank-four Links, all-level same-ideal automorphy, common geometric/arithmetic families and global quantitative production remain in the continuation frontier.',
        'No new whole sufficient-route obligation is closed. The two earlier AdVanishK and HostRigid_s closures persist, and the 31-entry register retains every remaining original whole contract.'
    ],limitations=['Recorded graph is the human-proof dependency graph, not a mechanically extracted Lean transitive graph.',
        'Independent mathematical component reviews remain separately bound; this integration audit does not reprove every component theorem.',
        'No Lean compilation, kernel replay, formal correctness challenge or completed unconditional human proof of RH/GRH is asserted.'])
args.output.parent.mkdir(parents=True,exist_ok=True)
args.output.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
print(json.dumps(dict(status=result['status'],statistics=computed,passed_checks=len(checks),errors=errors,output=str(args.output)),ensure_ascii=False,indent=2))
raise SystemExit(bool(errors))
