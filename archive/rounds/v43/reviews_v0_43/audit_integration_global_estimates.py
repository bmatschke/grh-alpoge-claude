#!/usr/bin/env python3
"""Independent, read-only audit of the v0.43 integration and unchanged v0.42 baseline."""
from pathlib import Path
import argparse
import collections
import hashlib
import json
import re
import subprocess

ROOT=Path(__file__).resolve().parents[1]
OLD=ROOT/'history/version_0_42'
PIN='7cbf7a0c32fca1badf05931879a37c3f8a2b03b4'
ap=argparse.ArgumentParser()
ap.add_argument('--source',type=Path,required=True)
ap.add_argument('--output',type=Path,default=ROOT/'reviews_v0_43/integration_global_estimates.json')
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
cfg=read(ROOT/'increment_v0_43.json')
old=read(OLD/'provenance.json');now=read(ROOT/'provenance.json')
oi=read(OLD/'source_index.json');ni=read(ROOT/'source_index.json')
bc=old['claims'];cs=now['claims'];oldcount=len(bc)
need(oldcount==2363,'baseline has exactly 2363 claims',oldcount)
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
    component_bindings[component]=dict(claims=len(ledger['claims']),ledger_sha256=bindings[component+'/provenance.json'])
    external={r['id']:r for key in ['published_applications','classical_and_foundational_inputs']
              for r in ledger.get(key,[]) if 'id' in r}
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
            snapshot=ROOT/'source_snapshot_v0_43'/path
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

oldmap=read(ROOT/'dependency_audit_v0_42/obligation_map.json')
newmap=read(ROOT/'dependency_audit_v0_43/obligation_map.json')
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
need(all(nodes[k]['status']=='proved_in_stated_scope' for k in ['AD_VANISH_K_MATCH','HOST_RIGID_S']),'two v0.42 whole closures remain closed')
closed_status={'proved_in_stated_scope','published_application_checked','complete','closed'}
opens={k for k,n in nodes.items() if n['gate']=='LEAF' and n['status'] not in closed_status}
cats=dict(collections.Counter(nodes[k]['category'] for k in opens))
need(len(opens)==31 and cats=={'C':22,'B':9},'remaining frontier stays 31 whole leaves: 22 C and 9 B',cats)
oldreg=read(ROOT/'dependency_audit_v0_42/remaining_leaf_register.json')
reg=read(ROOT/'dependency_audit_v0_43/remaining_leaf_register.json')
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
    need(nodes[k].get('version_0_43_progress')==progress,k+': current nested progress matches configuration')
for k,contract in cfg.get('updated_contracts',{}).items():
    need(nodes[k]['contract']==contract,k+': current contract narrative matches configuration')
    need(nodes[k].get('historical_contract_narrative_v0_42')==oldnodes[k]['contract'],k+': prior exact contract narrative retained separately')

targets=read(ROOT/'next_source_targets.json');oldtargets=read(OLD/'next_source_targets.json')
need(targets['targets']==oldtargets['targets'] and len(targets['targets'])==245,'all 245 historical source targets preserved literally')
disp=read(ROOT/'dependency_audit_v0_43/target_disposition.json');od=read(ROOT/'dependency_audit_v0_42/target_disposition.json')
need(len(disp['records'])==len(od['records'])==245 and len(disp['scope_groups'])==107,'245 dispositions and 107 scope groups preserved')
need(all(all(b.get(k)==v for k,v in a.items()) for a,b in zip(od['records'],disp['records'])),'historical target disposition fields retained with additive current notes')
need(disp['scope_groups']==od['scope_groups'],'historical target grouping unchanged')
checkpoint=read(ROOT/'continuation_checkpoint.json')
need(checkpoint['remaining_major_inputs']==cfg['remaining_major_inputs'] and checkpoint['next_targets']==cfg['next_targets'],'continuation checkpoint contains current frontier and priorities')
need(targets['next_local_priority']==cfg['next_targets'],'next source priorities are current')

flc=read(ROOT/'finite_local_completion_v43/closure.json')
need(flc['whole_obligation_closures']==[] and flc['unused_upper_comparison_not_claimed'] and flc['small_rank_long_prime_not_claimed'] and flc['original_normalized_type_record_retained'],'FLC scope retains global inputs and exact eventual/unused-clause boundaries')
need(byid['FLC16']['classification']=='A' and byid['FLC16'].get('published_input_ids')==['FLC_GREEN_CLASSIFICATION'],'Green is a named checked published application, not an unresolved or newly proved theorem')
need('FLC_GREEN_CLASSIFICATION' not in graph,'published input is not a fictitious numbered claim')
need(not newmap['validation'].get('all_original_finite_local_character_laws_complete',False),'current metadata does not claim the unused fourth admLq character law')

def ancestors(cid):
    seen=set();todo=list(graph[cid])
    while todo:
        k=todo.pop()
        if k not in seen:seen.add(k);todo.extend(graph[k])
    return seen
# Each exception was read in its complete claim block and checked for direction/scope.
exceptions={
 ('ADP3','PKT4'):'ADP3 explicitly excludes the separate geometric multiplicity inputs of PKT4. Its finite reducibility argument uses PKT5-PKT6 with independently supplied ADP1-ADP2 hypotheses; both are recorded.',
 ('ADP9','ADP10'):'ADP9 points forward to where the openness condition enters. Its formU proof uses ADP6-ADP8; ADP10 is a later consumer, not a premise.',
 ('ADP12','CFD12'):'The final boundary paragraph describes a subsequent application of CFD12 after the separate Galois-decorated part supplier is produced. CFD12 is not used to prove decompU.',
 ('AFS17','AFS10'):'AFS17 refers to the full ordinary module N0 defined in AFS10. Its required automorphism is supplied directly by recorded OST25, and its IsSpec span field is an explicit hypothesis. It does not invoke AFS10 nonzero-fiber or extension assertions.',
 ('AFS19','AFS10'):'AFS19 imports only the notation N0,N,T from AFS10. Its proof obtains the summand and freeness from recorded OHA6-OHA7, tensor identification from recorded AFS18/ASP11, and specified-character existence from recorded AFS9. The separate AFS10 theorem is not used.'
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

review_paths=[
 'reviews_v0_43/integral_type_v43_root_review.json',
 'automorphic_decomposition_v43/review_ADP1_ADP12_main_proof_rigidity.json',
 'classical_parts_v43/review_CFD_global_estimates.json',
 'reviews_v0_43/arithmetic_fibers_v43_root_review.json',
 'reviews_v0_43/finite_local_completion_v43_root_review.json']
reviewed=set();review_coverage=[]
for rel in review_paths:
    review=read(ROOT/rel)
    need(review.get('status',review.get('result'))=='PASS',rel+': independent mathematical review PASS')
    file=review['proof_file'];data=(ROOT/file).read_bytes()
    expected=review.get('proof_file_sha256',review.get('proof_sha256'))
    need(sha(data)==expected,rel+': reviewed proof file is current exact file')
    entries=review.get('reviewed_claims',review.get('claims_reviewed',review.get('claims',[])))
    for entry in entries:
        cid=entry.get('id',entry.get('claim'))
        need(cid in byid,rel+': reviewed claim exists '+cid)
        need(entry.get('status',entry.get('result'))=='PASS',rel+': reviewed claim passed '+cid)
        pl=byid[cid]['proof_location']
        block=b''.join(data.splitlines(keepends=True)[pl['line_start']-1:pl['line_end']])
        h=entry.get('proof_range_sha256',entry.get('block_sha256'))
        need(h in {sha(block),sha(block.rstrip(b'\r\n'))},rel+': current claim block matches reviewed bytes '+cid)
        reviewed.add(cid)
    review_coverage.append(dict(file=rel,reviewer=review['reviewer'],claims=len(entries),proof_file=file,proof_file_sha256=sha(data)))
need(reviewed=={c['id'] for c in incoming},'all and only 78 new claims have matching independent mathematical review coverage')

stats=read(ROOT/'integration_stats_v0_43.json')
computed=dict(new_claims=len(incoming),cumulative_claims=len(cs),selected_nodes=121,selected_edges=161,
    open_count=31,open_categories=cats,shared_open=24,extra_grh_open=7,
    new_source_files_checked=len(sources),new_unique_source_ranges_checked=len(ranges))
need(stats==computed,'reported integration statistics equal independent computation',dict(reported=stats,computed=computed))
for p,h in bindings.items():need(sha((ROOT/p).read_bytes())==h,'audit input stable during review: '+p)
result=dict(schema='rh-independent-integration-review/1',reviewer='global_estimates',date='2026-11-23',
    source_commit=PIN,status='PASS' if not errors else 'FAIL',
    scope='Independent preservation, source/proof bytes, dependency, selected-route, closure and current-scope audit; no Lean replay.',
    statistics=computed,baseline_claims_preserved=oldcount,baseline_source_files_preserved=len(old['source_files']),
    baseline_manifest_artifacts_preserved=preserved,baseline_artifacts_retained_in_history=archived,
    claims_and_sources_checked=len(incoming),passed_check_count=len(checks),errors=errors,input_bindings=bindings,
    new_proof_files=proofs,component_ledgers=component_bindings,named_proof_reference_scan=reference_scan,
    named_external_input_bindings=external_bindings,independent_mathematical_review_coverage=review_coverage,
    exact_whole_closures=[],current_remaining_scopes={k:n.get('version_0_43_progress') for k,n in nodes.items() if 'version_0_43_progress' in n},
    semantic_scope_review=[
        'The integral type and Hecke-data constructor retain their explicitly matched classical type and inherited local-correspondence foundations. The output coefficient ring and all original universal quantifiers are preserved.',
        'Actual compact-unitary decompU is distinct from the still-required Galois-decorated PartAltAlt/AutomorphicHeckeSet producer. CFD and the AFS same-ideal installation retain that exact supplier.',
        'Dense arithmetic points, nonflat faithful fibers, good-part scalar action and separation do not assert nonzero blocks for arbitrary residual labels or replace the original ideal by its radical.',
        'FLC closes the three retained finite inputs of RRT11 and proves selected eventual WeightAllRows with the original Wg. Original normalized-type, adelic row and cylinder-count production remain separate.',
        'The final long-prime term has RRT10 threshold N0. Actual f<=k<=r and x^2<=f absorb it; SizesAt alone does not. The unused fourth admLq upper comparison remains unclaimed.',
        'No new whole sufficient-route obligation is closed. The v0.42 AdVanishK match and HostRigid_s closures persist, while every remaining original whole contract remains in the 31-entry register.'
    ],limitations=['Recorded graph is the human-proof dependency graph, not a mechanically extracted Lean transitive graph.',
        'Independent mathematical component reviews remain separately bound; this integration audit does not reprove every component theorem.',
        'No Lean compilation, kernel replay, formal correctness challenge or completed unconditional human proof of RH/GRH is asserted.'])
args.output.parent.mkdir(parents=True,exist_ok=True)
args.output.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
print(json.dumps(dict(status=result['status'],statistics=computed,passed_checks=len(checks),errors=errors,output=str(args.output)),ensure_ascii=False,indent=2))
raise SystemExit(bool(errors))
