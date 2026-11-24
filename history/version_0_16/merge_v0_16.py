#!/usr/bin/env python3
"""Merge v0.16 proofs, preserving every original v0.15 claim field."""
from pathlib import Path
import argparse
import copy
import hashlib
import json
import subprocess

ROOT=Path(__file__).resolve().parent
OLD=ROOT/'history/version_0_15'
parser=argparse.ArgumentParser()
parser.add_argument('--repo',type=Path,default=ROOT.parent/'lean-source')
args=parser.parse_args()
REPO=args.repo.resolve()
COMMIT='7cbf7a0c32fca1badf05931879a37c3f8a2b03b4'
URL='https://github.com/CocoSgt/riemann-hypothesis-lean'

def read(p):return json.loads(p.read_text())
def write(p,o):p.write_text(json.dumps(o,ensure_ascii=False,indent=2)+'\n')
def digest(b):return hashlib.sha256(b).hexdigest()

config=read(ROOT/'increment_v0_16.json')
components=config['components']
prior=read(OLD/'provenance.json')
result=copy.deepcopy(prior)
result.update(artifact_version='0.16',date=config['date'],predecessor_version='0.15',scope=config['scope'])
files={f['path']:copy.deepcopy(f)for f in prior['source_files']}
graph=copy.deepcopy(prior['mathematical_dependency_graph'])
new=[]
component_scope={}
for component in components:
    ledger=read(ROOT/component/'provenance.json')
    repository_metadata=ledger.get('repository')
    nested_commit=repository_metadata.get('commit')if isinstance(repository_metadata,dict)else None
    assert ledger.get('commit',ledger.get('source_commit',nested_commit))==COMMIT,component
    component_scope[component]={k:v for k,v in ledger.items()if k not in ['claims','files','source_files']}
    for original in ledger['claims']:
        c=copy.deepcopy(original)
        c['introduced_in']='0.16'
        c['component_ledger']=component+'/provenance.json'
        c['depends_on']=c.get('depends_on',c.get('dependencies',[]))
        if 'proof_location' not in c:
            c['proof_location']={'file':component+'/main.tex','expanded':component+'/report.txt','section':c['id']}
        for field in ['proof_location','expanded_notes']:
            if isinstance(c.get(field),dict):
                for key in ['file','expanded']:
                    if isinstance(c[field].get(key),str)and'/'not in c[field][key]:
                        c[field][key]=component+'/'+c[field][key]
        new.append(c)
        graph[c['id']]=list(c['depends_on'])
    for f0 in ledger.get('source_files',ledger.get('files',[])):
        if f0['path']in files:
            assert f0['sha256']==files[f0['path']]['sha256'],f0['path']
        else:
            f=copy.deepcopy(f0)
            if'line_count'in f and'lines'not in f:f['lines']=f['line_count']
            f.setdefault('url',f"{URL}/blob/{COMMIT}/{f['path']}")
            files[f['path']]=f
result['claims'].extend(new)
ids={c['id']for c in result['claims']}
assert len(ids)==len(result['claims'])
for cid,deps in graph.items():assert set(deps)<=ids,(cid,sorted(set(deps)-ids))
for c in result['claims']:
    if c['id']in config['claim_updates']:
        c['version_0_16_update']=copy.deepcopy(config['claim_updates'][c['id']])
order=[];visited=set();active=set()
def visit(k):
    if k in visited:return
    assert k not in active,('dependency cycle',k)
    active.add(k)
    for d in graph[k]:visit(d)
    active.remove(k);visited.add(k);order.append(k)
for k in graph:visit(k)
result['mathematical_dependency_graph']=graph
result['dependency_topological_order']=order
result['source_files']=sorted(files.values(),key=lambda f:f['path'])
result.setdefault('merge_inputs_history',[]).append(copy.deepcopy(prior.get('merge_inputs',{})))
result['merge_inputs']={c:{'ledger':c+'/provenance.json','sha256':digest((ROOT/c/'provenance.json').read_bytes())}for c in components}
result['new_component_ledgers']=[c+'/provenance.json'for c in components]
result['version_0_16_local_conclusions']=copy.deepcopy(config['local_conclusions'])
result.setdefault('component_scope_metadata_as_received',{}).update(component_scope)
result.setdefault('component_input_boundaries',{}).update({c:component_scope[c].get('retained_inputs',component_scope[c].get('input_boundaries',[]))for c in components})
for original,c in zip(prior['claims'],result['claims']):
    assert all(c[k]==v for k,v in original.items()),original['id']
for k,v in prior.items():
    if k.startswith('version_')and'conclusion'in k:assert result[k]==v,k
for k,v in prior['mathematical_dependency_graph'].items():assert graph[k]==v,k
result['validation']={
    'previous_claims_preserved':len(prior['claims']),'new_claims':len(new),'claim_count':len(ids),
    'source_link_count':sum(len(c['sources'])for c in result['claims']),'source_file_count':len(files),
    'dependency_graph_acyclic':True,'dependency_graph_is_lean_transitive_audit':False,
    'lean_build':False,'kernel_replay':False,
}
write(ROOT/'provenance.json',result)
write(ROOT/'source_index.json',{'commit':COMMIT,'artifact_version':'0.16','source_files':result['source_files']})

text=['RH / DIRICHLET-GRH RECONSTRUCTION v0.16 -- CLAIM AND SOURCE LEDGER',
      'Pinned source '+COMMIT,'All v0.15 claim fields/source arrays are preserved; v0.16 annotations are additive.',
      'Current scope: '+config['scope'],'']
for c in result['claims']:
    text += [c['id']+' -- '+c['title'],'Status: '+c['status']]
    for field in ['statement','assumptions','depends_on','dependencies','proof_location','version_0_16_update']:
        if field in c:text.append(field+': '+(c[field]if isinstance(c[field],str)else json.dumps(c[field],ensure_ascii=False)))
    for i,f in enumerate(c['sources'],1):
        text += [f"  {i}. {f['declaration']}",f"     {f['path']}:{f['line_start']}-{f['line_end']}",
                 '     '+f['url'],'     File SHA256 '+f['sha256'],'     Range SHA256 '+f['range_sha256']]
    text.append('')
(ROOT/'provenance.txt').write_text('\n'.join(text)+'\n')

nt=read(OLD/'next_source_targets.json')
nt.update(version='0.16',completed_previous_frontier=config['completed_previous_frontier'],next_local_priority=config['next_local_priority'])
nt['priority_groups']=config['priority_groups']
nt['previous_version_precision_notes']=copy.deepcopy(nt['precision_notes'])
nt['precision_notes']=config['precision_notes']
def key(t):return t['path']+':'+t['declaration'].split('.')[-1]
removed=[]
retained=[]
for t0 in nt['targets']:
    t=copy.deepcopy(t0)
    if key(t)in config['replaced_target_keys']:
        removed.append(t)
        continue
    if key(t)in config['target_scope_updates']:
        t['remaining_human_scope']=config['target_scope_updates'][key(t)]
    retained.append(t)
new_targets=[]
def flatten_targets(data):
    raw=data if isinstance(data,list) else data.get('targets',[])
    out=[]
    for item in raw:
        if 'path' in item:
            out.append(item)
        else:
            for index,source in enumerate(item.get('sources',[]),1):
                t=copy.deepcopy(source)
                t.update({k:copy.deepcopy(v) for k,v in item.items() if k!='sources' and k not in t})
                t['id']=str(item.get('id','target'))+'-'+str(index)
                t['remaining_human_scope']=item.get('scope',item.get('remaining_scope',item.get('title','')))
                out.append(t)
    return out
for component in components:
    p=ROOT/component/'next_targets.json'
    if not p.is_file():continue
    target_data=read(p)
    target_records=flatten_targets(target_data)
    for t0 in target_records:
        t=copy.deepcopy(t0)
        if key(t)in config['replaced_target_keys']:
            removed.append(t)
            continue
        # Component priority numbers rank that component's own targets.
        # Normalize them to the cumulative map's four subject groups.
        t['component_priority_group']=t.get('priority_group')
        t['priority_group']=3 if component == 'arithmetic_hosts' else 1
        t['human_status']='continuation_target_only; no new proof asserted by this target record'
        t.setdefault('remaining_human_scope',t.get('remaining_scope',t.get('role','Remaining supplied-data construction.')))
        if key(t)in config['target_scope_updates']:t['remaining_human_scope']=config['target_scope_updates'][key(t)]
        new_targets.append(t)
seen=set();dedup=[]
for t in new_targets+retained:
    k=(t['path'],t['line_start'],t['line_end'])
    if k in seen:continue
    seen.add(k);dedup.append(t)
target_files={}
cache={}
for t in dedup:
    path=t['path']
    if path not in cache:cache[path]=subprocess.check_output(['git','-C',str(REPO),'show',COMMIT+':'+path])
    raw=cache[path]
    assert digest(raw)==t['sha256'],path
    assert digest(b''.join(raw.splitlines(keepends=True)[t['line_start']-1:t['line_end']]))==t['range_sha256'],(path,t['line_start'])
    target_files[path]={'path':path,'sha256':digest(raw),'bytes':len(raw),'lines':len(raw.splitlines()),'url':f'{URL}/blob/{COMMIT}/{path}'}
nt['targets']=dedup
nt['target_count']=len(dedup)
nt['source_files']=list(target_files.values())
nt['source_file_count']=len(target_files)
nt['priority_group_counts']={str(i):sum(t['priority_group']==i for t in dedup)for i in range(1,5)}
removed_unique={key(t):t for t in removed}
nt['version_0_16_replaced_targets']=[{'path':t['path'],'declaration':t['declaration'],'reason':config['replaced_target_keys'][key(t)]}for t in removed_unique.values()]
nt['validation']={'all_target_file_and_range_hashes_verified':True,'target_count':len(dedup),
                  'global_branches_preserved':nt['global_branches_unchanged']==read(OLD/'next_source_targets.json')['global_branches_unchanged']}
write(ROOT/'next_source_targets.json',nt)
print(json.dumps(result['validation']))
print(json.dumps({'next_targets':len(dedup),'target_groups':nt['priority_group_counts']}))
