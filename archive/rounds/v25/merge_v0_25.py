#!/usr/bin/env python3
"""Merge the reviewed v0.25 chains; preserve original claim fields and edges."""
from pathlib import Path
import copy,hashlib,json

ROOT=Path(__file__).resolve().parent; OLD=ROOT/'history/version_0_24'
def read(p):return json.loads(p.read_text())
def write(p,v):p.write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n')
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
cfg=read(ROOT/'increment_v0_25.json');prior=read(OLD/'provenance.json')
out=copy.deepcopy(prior)
out.update(artifact_version='0.25',predecessor_version='0.24',date=cfg['date'],scope=cfg['scope'])
files={f['path']:copy.deepcopy(f) for f in prior['source_files']}
graph=copy.deepcopy(prior['mathematical_dependency_graph'])
new=[];scopes={}
for component in cfg['components']:
 data=read(ROOT/component/'provenance.json');assert data['commit']==prior['commit'],component
 scopes[component]={k:v for k,v in data.items() if k not in ['claims','source_files','files']}
 for original in data['claims']:
  c=copy.deepcopy(original);c['introduced_in']='0.25';c['component_ledger']=component+'/provenance.json'
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
 if c['id'] in cfg['claim_updates']:c['version_0_25_update']=copy.deepcopy(cfg['claim_updates'][c['id']])
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
out['version_0_25_local_conclusions']={'chains':cfg['new_in_this_version'],'semantic_audit':'dependency_audit_v0_25/obligation_map.json','premise_closures':cfg['claim_updates'],'closure_certificates':{c:{'path':c+'/closure.json','sha256':sha(ROOT/c/'closure.json')} for c in cfg['components']}}
out.setdefault('component_scope_metadata_as_received',{}).update(scopes)
out.setdefault('component_input_boundaries',{}).update({c:scopes[c].get('component_input_boundary',scopes[c].get('retained_inputs',scopes[c].get('input_ledger',scopes[c].get('input_boundaries',[])))) for c in cfg['components']})
out['semantic_dependency_audit']={'path':'dependency_audit_v0_25/obligation_map.json','kind':'Finite audited AND/OR sufficient-obligation map, with completed suppliers, explicit classical leaves and exact same-object/quantifier bindings','is_exhaustive_lean_dependency_graph':False,'empty_legacy_remaining_inputs_implies_closed':False}
for old,c in zip(prior['claims'],out['claims']):assert all(c[k]==v for k,v in old.items()),old['id']
for k,v in prior['mathematical_dependency_graph'].items():assert graph[k]==v,k
out['validation']={'previous_claims_preserved':len(prior['claims']),'new_claims':len(new),'claim_count':len(ids),'source_link_count':sum(len(c['sources']) for c in out['claims']),'source_file_count':len(files),'dependency_graph_acyclic':True,'dependency_graph_is_lean_transitive_audit':False,'lean_build':False,'kernel_replay':False}
write(ROOT/'provenance.json',out)
write(ROOT/'source_index.json',{'commit':prior['commit'],'artifact_version':'0.25','source_files':out['source_files']})
lines=['RH / DIRICHLET-GRH RECONSTRUCTION v0.25 -- CLAIM AND SOURCE LEDGER','Pinned source '+prior['commit'],'Every original v0.24 claim field and source array is preserved; current closure annotations are additive.','Scope: '+cfg['scope'],'Semantic frontier: dependency_audit_v0_25/obligation_map.json','']
for c in out['claims']:
 lines.extend([c['id']+' -- '+c['title'],'Status: '+c['status']])
 fields=['statement','assumptions','remaining_inputs','classical_inputs','depends_on','proof_location']+[k for k in c if k.startswith('version_') and k.endswith('_update')]
 for f in fields:
  if f in c:lines.append(f+': '+(c[f] if isinstance(c[f],str) else json.dumps(c[f],ensure_ascii=False)))
 for i,s in enumerate(c['sources'],1):lines.extend([f"  {i}. {s['declaration']}",f"     {s['path']}:{s['line_start']}-{s['line_end']}",'     '+s['url'],'     File SHA256 '+s['sha256'],'     Range SHA256 '+s['range_sha256']])
 lines.append('')
(ROOT/'provenance.txt').write_text('\n'.join(lines)+'\n')

nt=read(OLD/'next_source_targets.json')
nt.update(version='0.25',completed_previous_frontier=cfg['completed_previous_frontier'],next_local_priority=cfg['next_local_priority'])
nt['previous_version_precision_notes']=copy.deepcopy(nt['precision_notes']);nt['precision_notes']=cfg['precision_notes']
retirement=read(ROOT/'dependency_audit_v0_25/retirement_candidates.json')
closed={t['id']:t for t in retirement['targets']}
assert len(closed)==10
scopefile=ROOT/'dependency_audit_v0_25/target_scope_updates.json'
scopeupdates=read(scopefile) if scopefile.exists() else {}
if 'updates' in scopeupdates:scopeupdates=scopeupdates['updates']
if isinstance(scopeupdates,list):scopeupdates={r['id']:r for r in scopeupdates}
retired=[];kept=[]
for t0 in nt['targets']:
 t=copy.deepcopy(t0);cid=t.get('id')
 if cid in closed:
  u=closed[cid]
  assert (t['path'],t['line_start'],t['line_end'])==(u['path'],u['line_start'],u['line_end']),cid
  retired.append({'id':cid,'path':t['path'],'declaration':t['declaration'],'supplied_by':u['supplied_by'],'reason':u['closed_scope'],'original_record':'history/version_0_24/next_source_targets.json','original_target_snapshot':t0})
  continue
 if t['declaration'].split('.')[-1]=='VWinAt':
  t['version_0_25_supplied_inputs']={'ThmBab':'TW8: one BConst before every Ct>=1','ThmBcFree':'OB8: constant 240','PointHV_common_inputs':'LD3, LK2/LK3, KB8=LemmaK31, CZ6=CountZ0'}
  t['remaining_human_scope']='VW3–VW4 prove the exact conditional same-field and fixed-pair window assembly. TW8 now supplies the full ThmBab theorem and OB8 supplies ThmBcFree240. PointHV is the remaining major cohomological supplier: CountI/II/III/V and remaining original-field case/layer/sum assembly. Classical prime-pair inputs and actual host installation retain their original roles.'
  t['human_status']='PointHV remains at the major cohomological cut; simultaneous two-primary/reference-layer and odd-minus suppliers are closed'
 if cid in scopeupdates:
  u=scopeupdates[cid]
  t['version_0_25_audit_scope_update']=copy.deepcopy(u)
  for k in ['remaining_human_scope','retained_inputs','human_status','supplied_by','supplied_parts']:
   if k in u:t[k]=copy.deepcopy(u[k])
 kept.append(t)
assert {x['id'] for x in retired}==set(closed)
extra=read(ROOT/'dependency_audit_v0_25/next_targets.json')
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
nt['version_0_25_replaced_targets']=retired
nt['version_0_25_added_target_deduplication']=duplicates
nt['version_0_25_global_scope_update']={'preserved_global_branch_objects':True,'closed_suppliers':['LK1–LK4: exact native local-K interfaces','TB1–TB10: all-prime TorsBound49 and TorsBoundPow22','KB1–KB8: actual KBridge and LemmaK31','TW1–TW8: full simultaneous ThmBab','CZ1–CZ6: PropZ and CountZ0'],'conditional_chain_closures':['Earlier VW3/VW4 now retain PointHV as their only major cohomological supplier, plus their original prime-pair and actual-host requirements','Earlier LN1–LN10 retain actual local tables and type/theta/rank data for original-family LinkN'],'current_remaining_inputs':cfg['remaining_major_inputs'],'semantic_frontier':'dependency_audit_v0_25/obligation_map.json'}
nt['validation']={'target_count':len(dedup),'global_branches_preserved':nt['global_branches_unchanged']==read(OLD/'next_source_targets.json')['global_branches_unchanged'],'all_target_file_and_range_hashes_verified':False,'verification_note':'Filled by audit_v0_25.py after this merge.'}
write(ROOT/'next_source_targets.json',nt)
print(json.dumps({**out['validation'],'retired_targets':len(retired),'new_target_records':len(extra),'deduplicated_target_records':len(duplicates),'next_targets':len(dedup)},indent=2))
