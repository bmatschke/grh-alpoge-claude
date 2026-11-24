#!/usr/bin/env python3
"""Add the v0.23 chains and semantic closures, preserving all prior records."""
from pathlib import Path
import copy,hashlib,json

ROOT=Path(__file__).resolve().parent; OLD=ROOT/'history/version_0_22'
def read(p):return json.loads(p.read_text())
def write(p,v):p.write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n')
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
cfg=read(ROOT/'increment_v0_23.json');prior=read(OLD/'provenance.json')
out=copy.deepcopy(prior)
out.update(artifact_version='0.23',predecessor_version='0.22',date=cfg['date'],scope=cfg['scope'])
files={f['path']:copy.deepcopy(f) for f in prior['source_files']}
graph=copy.deepcopy(prior['mathematical_dependency_graph'])
new=[];scopes={}
for component in cfg['components']:
 data=read(ROOT/component/'provenance.json')
 assert data['commit']==prior['commit'],component
 scopes[component]={k:v for k,v in data.items() if k not in ['claims','source_files','files']}
 for original in data['claims']:
  c=copy.deepcopy(original); c['introduced_in']='0.23';c['component_ledger']=component+'/provenance.json'
  c['depends_on']=c.get('depends_on',c.get('mathematical_dependencies',c.get('dependencies',[])))
  if 'proof_location' not in c:
   c['proof_location']=copy.deepcopy(c.get('human_proof',{'file':component+'/main.tex','section':c['id']}))
   loc=c['proof_location']
   if 'file' not in loc and 'path' in loc:loc['file']=loc['path']
   if 'sha256' not in loc and 'range_sha256' in loc:loc['sha256']=loc['range_sha256']
  new.append(c);graph[c['id']]=list(c['depends_on'])
 for f in data.get('source_files',data.get('files',[])):
  if f['path'] in files: assert files[f['path']]['sha256']==f['sha256'],f['path']
  else: files[f['path']]=copy.deepcopy(f)
out['claims'].extend(new)
ids={c['id'] for c in out['claims']};assert len(ids)==len(out['claims'])
for cid,deps in graph.items():assert set(deps)<=ids,(cid,set(deps)-ids)
for c in out['claims']:
 if c['id'] in cfg['claim_updates']:c['version_0_23_update']=copy.deepcopy(cfg['claim_updates'][c['id']])
order=[];done=set();active=set()
def visit(k):
 if k in done:return
 assert k not in active,('cycle',k)
 active.add(k)
 for d in graph[k]:visit(d)
 active.remove(k);done.add(k);order.append(k)
for k in graph:visit(k)
out['mathematical_dependency_graph']=graph;out['dependency_topological_order']=order
out['source_files']=sorted(files.values(),key=lambda f:f['path'])
out.setdefault('merge_inputs_history',[]).append(copy.deepcopy(prior.get('merge_inputs',{})))
out['merge_inputs']={c:{'ledger':c+'/provenance.json','sha256':sha(ROOT/c/'provenance.json')} for c in cfg['components']}
out['new_component_ledgers']=[c+'/provenance.json' for c in cfg['components']]
out['version_0_23_local_conclusions']={'chains':cfg['new_in_this_version'],'semantic_audit':'dependency_audit_v0_23/obligation_map.json','premise_closures':cfg['claim_updates']}
out.setdefault('component_scope_metadata_as_received',{}).update(scopes)
out.setdefault('component_input_boundaries',{}).update({c:scopes[c].get('component_input_boundary',scopes[c].get('retained_inputs',scopes[c].get('input_boundaries',[]))) for c in cfg['components']})
out['semantic_dependency_audit']={'path':'dependency_audit_v0_23/obligation_map.json','kind':'Finite audited AND/OR sufficient-obligation map with explicit same-object and quantifier bindings','is_exhaustive_lean_dependency_graph':False,'empty_legacy_remaining_inputs_implies_closed':False}
for old,c in zip(prior['claims'],out['claims']):assert all(c[k]==v for k,v in old.items()),old['id']
for k,v in prior['mathematical_dependency_graph'].items():assert graph[k]==v,k
out['validation']={'previous_claims_preserved':len(prior['claims']),'new_claims':len(new),'claim_count':len(ids),'source_link_count':sum(len(c['sources']) for c in out['claims']),'source_file_count':len(files),'dependency_graph_acyclic':True,'dependency_graph_is_lean_transitive_audit':False,'lean_build':False,'kernel_replay':False}
write(ROOT/'provenance.json',out)
write(ROOT/'source_index.json',{'commit':prior['commit'],'artifact_version':'0.23','source_files':out['source_files']})
lines=['RH / DIRICHLET-GRH RECONSTRUCTION v0.23 -- CLAIM AND SOURCE LEDGER','Pinned source '+prior['commit'],'Every v0.22 claim field and source array is preserved; current closure annotations are additive.','Scope: '+cfg['scope'],'Semantic frontier: dependency_audit_v0_23/obligation_map.json','']
for c in out['claims']:
 lines.extend([c['id']+' -- '+c['title'],'Status: '+c['status']])
 for f in ['statement','assumptions','remaining_inputs','depends_on','proof_location','version_0_23_update']:
  if f in c:lines.append(f+': '+(c[f] if isinstance(c[f],str) else json.dumps(c[f],ensure_ascii=False)))
 for i,s in enumerate(c['sources'],1):lines.extend([f"  {i}. {s['declaration']}",f"     {s['path']}:{s['line_start']}-{s['line_end']}",'     '+s['url'],'     File SHA256 '+s['sha256'],'     Range SHA256 '+s['range_sha256']])
 lines.append('')
(ROOT/'provenance.txt').write_text('\n'.join(lines)+'\n')

nt=read(OLD/'next_source_targets.json')
nt.update(version='0.23',completed_previous_frontier=cfg['completed_previous_frontier'],next_local_priority=cfg['next_local_priority'])
nt['previous_version_precision_notes']=copy.deepcopy(nt['precision_notes']);nt['precision_notes']=cfg['precision_notes']
hp=read(ROOT/'chain_closure_core/closure.json')
closed_ids={t['id'] for t in hp['closed_source_target_keys']}
retired=[];kept=[]
for t0 in nt['targets']:
 t=copy.deepcopy(t0)
 short=t['declaration'].split('.')[-1]
 if t.get('id') in closed_ids or short in ['vwinAt_of_joint','winPairs']:
  reason='HP1–HP6 close the literal representation leaf.' if t.get('id') in closed_ids else 'VW3–VW4 now prove this exact conditional assembly; its substantive cohomological suppliers are separately retained.'
  retired.append({'id':t.get('id'),'path':t['path'],'declaration':t['declaration'],'reason':reason,'original_record':'history/version_0_22/next_source_targets.json'});continue
 if short=='VWinAt':
  t['version_0_23_inherited_scope']=t.get('remaining_human_scope',t.get('scope',''))
  t['remaining_human_scope']='The conditional JointWin + ThmBc -> VWinAt and fixed-pair assembly are proved in VW1–VW4. Retain only construction of the deep suppliers, with exact original fields and simultaneous windows; see ThmBab/PointHV/ThmBcFree targets and the obligation map.'
  t['human_status']='unconditional arithmetic supplier still open; downstream assembly closed'
 kept.append(t)
targetfile=ROOT/'dependency_audit_v0_23/next_targets.json'
extra=read(targetfile)
extra=extra if isinstance(extra,list) else extra['targets']
for t in extra:
 c=copy.deepcopy(t);c.setdefault('priority_group',4);c.setdefault('human_status','open substantive supplier; no proof asserted by this target record');kept.append(c)
seen=set();dedup=[]
for t in kept:
 key=(t['path'],t['line_start'],t['line_end'])
 if key in seen:continue
 seen.add(key);dedup.append(t)
nt['targets']=dedup;nt['target_count']=len(dedup)
old_target_files={f['path']:f for f in nt['source_files']}
for f in read(ROOT/'dependency_audit_v0_23/provenance.json')['source_files']:old_target_files.setdefault(f['path'],f)
targetpaths={t['path'] for t in dedup}
# Exact file metadata is supplied by either the unchanged target index or the
# current audited component; no file identity is inferred from a basename.
for f in extra:
 if f['path'] not in old_target_files:
  p=ROOT.parent/'lean-source'/f['path'];b=p.read_bytes()
  assert hashlib.sha256(b).hexdigest()==f['sha256']
  old_target_files[f['path']]={'path':f['path'],'sha256':f['sha256'],'bytes':len(b),'lines':len(b.splitlines()),'url':f['url'].split('#')[0]}
nt['source_files']=sorted([old_target_files[p] for p in targetpaths],key=lambda f:f['path']);nt['source_file_count']=len(targetpaths)
nt['priority_group_counts']={str(i):sum(t.get('priority_group')==i for t in dedup) for i in range(1,5)}
nt['version_0_23_replaced_targets']=retired
nt['version_0_23_global_scope_update']={'preserved_global_branch_objects':True,'downstream_closures':['HP1–HP6','VW1–VW4','WB1–WB8','DA1–DA2'],'current_remaining_inputs':cfg['remaining_major_inputs'],'semantic_frontier':'dependency_audit_v0_23/obligation_map.json'}
nt['validation']={'target_count':len(dedup),'global_branches_preserved':nt['global_branches_unchanged']==read(OLD/'next_source_targets.json')['global_branches_unchanged'],'all_target_file_and_range_hashes_verified':False,'verification_note':'Filled by audit_v0_23.py after this merge.'}
write(ROOT/'next_source_targets.json',nt)
print(json.dumps({**out['validation'],'retired_targets':len(retired),'next_targets':len(dedup)},indent=2))
