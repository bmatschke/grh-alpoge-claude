#!/usr/bin/env python3
"""Merge the reviewed supplier chains, retaining every historical claim field."""
from pathlib import Path
import copy,hashlib,json

ROOT=Path(__file__).resolve().parent; OLD=ROOT/'history/version_0_23'
def read(p):return json.loads(p.read_text())
def write(p,v):p.write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n')
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
cfg=read(ROOT/'increment_v0_24.json');prior=read(OLD/'provenance.json')
out=copy.deepcopy(prior)
out.update(artifact_version='0.24',predecessor_version='0.23',date=cfg['date'],scope=cfg['scope'])
files={f['path']:copy.deepcopy(f) for f in prior['source_files']}
graph=copy.deepcopy(prior['mathematical_dependency_graph'])
new=[];scopes={}
for component in cfg['components']:
 data=read(ROOT/component/'provenance.json');assert data['commit']==prior['commit'],component
 scopes[component]={k:v for k,v in data.items() if k not in ['claims','source_files','files']}
 for original in data['claims']:
  c=copy.deepcopy(original);c['introduced_in']='0.24';c['component_ledger']=component+'/provenance.json'
  c['depends_on']=c.get('depends_on',c.get('mathematical_dependencies',c.get('dependencies',[])))
  if 'proof_location' not in c:
   c['proof_location']=copy.deepcopy(c.get('human_proof',{'file':component+'/main.tex','section':c['id']}))
   loc=c['proof_location']
   if 'file' not in loc and 'path' in loc:loc['file']=loc['path']
   if 'sha256' not in loc and 'range_sha256' in loc:loc['sha256']=loc['range_sha256']
  new.append(c);graph[c['id']]=list(c['depends_on'])
 for f in data.get('source_files',data.get('files',[])):
  if f['path'] in files:assert files[f['path']]['sha256']==f['sha256'],f['path']
  else:files[f['path']]=copy.deepcopy(f)
out['claims'].extend(new)
ids={c['id'] for c in out['claims']};assert len(ids)==len(out['claims'])
for cid,deps in graph.items():assert set(deps)<=ids,(cid,set(deps)-ids)
for c in out['claims']:
 if c['id'] in cfg['claim_updates']:c['version_0_24_update']=copy.deepcopy(cfg['claim_updates'][c['id']])
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
out['version_0_24_local_conclusions']={'chains':cfg['new_in_this_version'],'semantic_audit':'dependency_audit_v0_24/obligation_map.json','premise_closures':cfg['claim_updates'],'closure_certificates':{c:{'path':c+'/closure.json','sha256':sha(ROOT/c/'closure.json')} for c in cfg['components']}}
out.setdefault('component_scope_metadata_as_received',{}).update(scopes)
out.setdefault('component_input_boundaries',{}).update({c:scopes[c].get('component_input_boundary',scopes[c].get('retained_inputs',scopes[c].get('input_ledger',scopes[c].get('input_boundaries',[])))) for c in cfg['components']})
out['semantic_dependency_audit']={'path':'dependency_audit_v0_24/obligation_map.json','kind':'Finite audited AND/OR sufficient-obligation map, with completed suppliers, explicit classical leaves and exact same-object/quantifier bindings','is_exhaustive_lean_dependency_graph':False,'empty_legacy_remaining_inputs_implies_closed':False}
for old,c in zip(prior['claims'],out['claims']):assert all(c[k]==v for k,v in old.items()),old['id']
for k,v in prior['mathematical_dependency_graph'].items():assert graph[k]==v,k
out['validation']={'previous_claims_preserved':len(prior['claims']),'new_claims':len(new),'claim_count':len(ids),'source_link_count':sum(len(c['sources']) for c in out['claims']),'source_file_count':len(files),'dependency_graph_acyclic':True,'dependency_graph_is_lean_transitive_audit':False,'lean_build':False,'kernel_replay':False}
write(ROOT/'provenance.json',out)
write(ROOT/'source_index.json',{'commit':prior['commit'],'artifact_version':'0.24','source_files':out['source_files']})
lines=['RH / DIRICHLET-GRH RECONSTRUCTION v0.24 -- CLAIM AND SOURCE LEDGER','Pinned source '+prior['commit'],'Every original v0.23 claim field and source array is preserved; current closure annotations are additive.','Scope: '+cfg['scope'],'Semantic frontier: dependency_audit_v0_24/obligation_map.json','']
for c in out['claims']:
 lines.extend([c['id']+' -- '+c['title'],'Status: '+c['status']])
 fields=['statement','assumptions','remaining_inputs','classical_inputs','depends_on','proof_location']+[k for k in c if k.startswith('version_') and k.endswith('_update')]
 for f in fields:
  if f in c:lines.append(f+': '+(c[f] if isinstance(c[f],str) else json.dumps(c[f],ensure_ascii=False)))
 for i,s in enumerate(c['sources'],1):lines.extend([f"  {i}. {s['declaration']}",f"     {s['path']}:{s['line_start']}-{s['line_end']}",'     '+s['url'],'     File SHA256 '+s['sha256'],'     Range SHA256 '+s['range_sha256']])
 lines.append('')
(ROOT/'provenance.txt').write_text('\n'.join(lines)+'\n')

nt=read(OLD/'next_source_targets.json')
nt.update(version='0.24',completed_previous_frontier=cfg['completed_previous_frontier'],next_local_priority=cfg['next_local_priority'])
nt['previous_version_precision_notes']=copy.deepcopy(nt['precision_notes']);nt['precision_notes']=cfg['precision_notes']
closed={
 'DA-next-01-c':('OB8, with OS9 and OS1','The full literal quantitative ThmBcFree supplier is proved with constant 240, including all non-PsiBound ingredients.'),
 'DA-next-01-d':('OS9, through OS1–OS8 and LD2/LD4','The literal universal PsiBound interface is supplied on the original E/Omega/O and all local data.'),
 'DA-next-02-b':('LN1–LN7 and LN9','The stated conditional cut-to-original linkN_of_gd implication is proved, including the exact restoration cost and unchanged cohomological coefficient.')
}
lnupdates={r['id']:r for r in read(ROOT/'congruence_chain/closure.json')['partial_target_updates']}
scopefile=ROOT/'dependency_audit_v0_24/target_scope_updates.json'
scopeupdates=read(scopefile) if scopefile.exists() else {}
if 'updates' in scopeupdates:scopeupdates=scopeupdates['updates']
if isinstance(scopeupdates,list):scopeupdates={r['id']:r for r in scopeupdates}
retired=[];kept=[]
for t0 in nt['targets']:
 t=copy.deepcopy(t0);cid=t.get('id')
 if cid in closed:
  supplier,reason=closed[cid]
  retired.append({'id':cid,'path':t['path'],'declaration':t['declaration'],'supplied_by':supplier,'reason':reason,'original_record':'history/version_0_23/next_source_targets.json'})
  continue
 if cid in lnupdates:
  u=lnupdates[cid];t['version_0_24_scope_update']=copy.deepcopy(u)
  t['human_status']=u['status'];t['remaining_human_scope']=u['retained']
  t['retained_inputs']=u['retained']
 if cid in ['DA-next-01-a','DA-next-01-b']:
  t['version_0_24_supplied_inputs']={'PoitouTateDuality':'LD3, relative to precisely matched finite classical Poitou–Tate'}
  t['remaining_human_scope']=('LD3 supplies the literal finite PoitouTateDuality premise. LocalFinitenessK, LocalTateDualityK and the actual LemmaK/counting arithmetic remain separate interfaces; the simultaneous original-field and prescribed-layer window quantifiers are retained.')
  t['retained_inputs']=t['retained_inputs'].replace('PoitouTateDuality, ','')
 if t['declaration'].split('.')[-1]=='VWinAt':
  t['remaining_human_scope']='VW3–VW4 prove the exact conditional window assembly. OS/OB now supply ThmBcFree with constant 240. The bespoke cohomological cut is ThmBab plus PointHV, with the same original output field and every prescribed layer model on the same parameter window/fixed pair; actual host installation remains.'
  t['human_status']='two bespoke cohomological suppliers still open; odd-minus and downstream assembly closed'
 if cid in scopeupdates:
  u=scopeupdates[cid]
  t['version_0_24_audit_scope_update']=copy.deepcopy(u)
  for k in ['remaining_human_scope','retained_inputs','human_status','supplied_by']:
   if k in u:t[k]=copy.deepcopy(u[k])
 kept.append(t)
assert {x['id'] for x in retired}==set(closed)
extra=read(ROOT/'dependency_audit_v0_24/next_targets.json')
extra=extra if isinstance(extra,list) else extra['targets']
for t in extra:
 c=copy.deepcopy(t);c.setdefault('priority_group',4);c.setdefault('human_status','open substantive supplier; exact current scope is stated in this record');kept.append(c)
seen=set();dedup=[];duplicates=[]
for t in kept:
 key=(t['path'],t['line_start'],t['line_end'])
 if key in seen:duplicates.append({'id':t.get('id'),'source_key':list(key)});continue
 seen.add(key);dedup.append(t)
nt['targets']=dedup;nt['target_count']=len(dedup)
oldfiles={f['path']:copy.deepcopy(f) for f in nt['source_files']}
for component in cfg['components']:
 for f in read(ROOT/component/'provenance.json')['source_files']:oldfiles.setdefault(f['path'],copy.deepcopy(f))
for t in extra:
 if t['path'] not in oldfiles:
  p=ROOT.parent/'lean-source'/t['path'];b=p.read_bytes();assert hashlib.sha256(b).hexdigest()==t['sha256']
  oldfiles[t['path']]={'path':t['path'],'sha256':t['sha256'],'bytes':len(b),'lines':len(b.splitlines()),'url':t['url'].split('#')[0]}
targetpaths={t['path'] for t in dedup}
nt['source_files']=sorted([oldfiles[p] for p in targetpaths],key=lambda f:f['path']);nt['source_file_count']=len(targetpaths)
nt['priority_group_counts']={str(i):sum(t.get('priority_group')==i for t in dedup) for i in range(1,5)}
nt['version_0_24_replaced_targets']=retired
nt['version_0_24_added_target_deduplication']=duplicates
nt['version_0_24_global_scope_update']={'preserved_global_branch_objects':True,'closed_suppliers':['LD1–LD4 in their finite-duality scope','OS1–OS9: PsiBound','OB1–OB8: ThmBcFree(240)'],'conditional_chain_closures':['LN1–LN10: original-family LinkN from the precise actual local tables and type/theta/rank data'],'current_remaining_inputs':cfg['remaining_major_inputs'],'semantic_frontier':'dependency_audit_v0_24/obligation_map.json'}
nt['validation']={'target_count':len(dedup),'global_branches_preserved':nt['global_branches_unchanged']==read(OLD/'next_source_targets.json')['global_branches_unchanged'],'all_target_file_and_range_hashes_verified':False,'verification_note':'Filled by audit_v0_24.py after this merge.'}
write(ROOT/'next_source_targets.json',nt)
print(json.dumps({**out['validation'],'retired_targets':len(retired),'new_target_records':len(extra),'deduplicated_target_records':len(duplicates),'next_targets':len(dedup)},indent=2))
