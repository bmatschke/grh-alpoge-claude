#!/usr/bin/env python3
"""Audit source bytes, new proof locators, unchanged history and reference DAG."""
from pathlib import Path
import argparse,hashlib,json,subprocess

ROOT=Path(__file__).resolve().parent; OLD=ROOT/'history/version_0_26'; REVIEW=ROOT/'reviews_v0_27'
p=argparse.ArgumentParser();p.add_argument('--repo',type=Path,default=ROOT.parent/'lean-source');args=p.parse_args();REPO=args.repo.resolve()
def read(p):return json.loads(p.read_text())
def write(p,v):p.write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n')
def digest(b):return hashlib.sha256(b).hexdigest()
def sha(p):return digest(p.read_bytes())
ledger=read(ROOT/'provenance.json');prior=read(OLD/'provenance.json');targets=read(ROOT/'next_source_targets.json');cfg=read(ROOT/'increment_v0_27.json')
assert ledger['artifact_version']=='0.27'
pin=ledger['commit']
semantic=read(ROOT/'dependency_audit_v0_27/obligation_map.json')
semantic_sources=read(ROOT/'dependency_audit_v0_27/source_anchors.json')['sources']
for rec in read(ROOT/'dependency_audit_v0_27/input_manifest.json')['files']:
 assert sha(ROOT/rec['path'])==rec['sha256'],('stale semantic-audit input',rec['path'])
assert (ROOT/'dependency_audit_v0_27/previous_obligation_map.json').read_bytes()==(ROOT/'dependency_audit_v0_26/obligation_map.json').read_bytes()
scope_review=(REVIEW/'integration_scope_review.txt').read_text()
for name in ['configure_v0_27.py','increment_v0_27.json']:
 assert sha(ROOT/name) in scope_review,('stale integration-scope review',name)
semantic_review=(REVIEW/'semantic_scope_review.txt').read_text()
for name in ['obligation_map.json','source_anchors.json','retirement_candidates.json','target_scope_updates.json','global_branch_scope_updates.json']:
 assert sha(ROOT/'dependency_audit_v0_27'/name) in semantic_review,('stale semantic-scope review',name)
claims={c['id']:c for c in ledger['claims']};new=[c for c in ledger['claims'] if c.get('introduced_in')=='0.27']
assert len(claims)==len(ledger['claims'])
nodes={n['id']:n for n in semantic['nodes']};assert len(nodes)==len(semantic['nodes'])
assert semantic['validation']['node_count']==len(nodes),'stale semantic node count'
oldnodes={n['id']:n for n in read(ROOT/'dependency_audit_v0_26/obligation_map.json')['nodes']}
assert set(oldnodes)<=set(nodes)
semantic_edges={}
for nid,n in nodes.items():
 assert set(n.get('claims',[]))<=set(claims),('unknown semantic claim',nid)
 es=n.get('requires',[]) if n['gate']=='AND' else [x for a in n.get('alternatives',[]) for x in a] if n['gate']=='OR' else []
 assert set(es)<=set(nodes),('unknown semantic obligation',nid)
 semantic_edges[nid]=es
 if nid in oldnodes and n!=oldnodes[nid]:
  assert any(h.get('snapshot')==oldnodes[nid] for h in n.get('history',[])),('missing prior node snapshot',nid)
semantic_done=set();semantic_active=set()
def semantic_visit(nid):
 if nid in semantic_done:return
 assert nid not in semantic_active,('semantic cycle',nid)
 semantic_active.add(nid)
 for d in semantic_edges[nid]:semantic_visit(d)
 semantic_active.remove(nid);semantic_done.add(nid)
for nid in nodes:semantic_visit(nid)
for c in prior['claims']:assert all(claims[c['id']][k]==v for k,v in c.items()),('historical claim changed',c['id'])
files={f['path']:f for f in ledger['source_files']}
for f in prior['source_files']:assert files[f['path']]==f,('historical source record changed',f['path'])
graph=ledger['mathematical_dependency_graph'];positions={c:i for i,c in enumerate(ledger['dependency_topological_order'])}
assert set(positions)==set(graph)==set(claims)
for k,v in prior['mathematical_dependency_graph'].items():assert graph[k]==v,('historical edge changed',k)
for c,deps in graph.items():assert all(positions[d]<positions[c] for d in deps),('invalid order',c)
assert targets['global_branches_unchanged']==read(OLD/'next_source_targets.json')['global_branches_unchanged']
for k,v in prior.items():
 if k.startswith('version_') and 'conclusion' in k:assert ledger[k]==v,k

# Every byte of the predecessor package is retained at its original relative
# path, except predecessor root files, whose exact copies are in history.
oldroots={x.name for x in OLD.iterdir() if x.is_file()}
oldcount=0
for line in (OLD/'SHA256SUMS').read_text().splitlines():
 expected,rel=line.split('  ',1);path=OLD/rel if rel in oldroots else ROOT/rel
 assert path.is_file() and sha(path)==expected,('historical file changed',rel)
 oldcount+=1

# Verify every cited and next-target source against both recorded SHA256 and
# its pinned Git blob. One batch obtains the immutable blobs efficiently.
source_records=[s for c in ledger['claims'] for s in c['sources']]
all_paths=sorted(set(files)|{t['path'] for t in targets['targets']}|{t['path'] for t in semantic_sources})
batch=('\n'.join(pin+':'+path for path in all_paths)+'\n').encode()
proc=subprocess.run(['git','-C',str(REPO),'cat-file','--batch'],input=batch,capture_output=True,check=True)
data=proc.stdout;offset=0;cache={}
for path in all_paths:
 end=data.index(b'\n',offset);header=data[offset:end].split();assert len(header)==3 and header[1]==b'blob',(path,header)
 size=int(header[2]);start=end+1;blob=data[start:start+size];offset=start+size+1
 assert data[start+size:start+size+1]==b'\n'
 raw=(REPO/path).read_bytes();assert raw==blob,('checkout differs from pin',path)
 cache[path]=(digest(raw),raw.splitlines(keepends=True))
assert offset==len(data)
for f in [*ledger['source_files'],*targets['source_files']]:assert cache[f['path']][0]==f['sha256'],f['path']
for s in source_records+targets['targets']+semantic_sources:
 d,lines=cache[s['path']];assert d==s['sha256'],s['path']
 a,b=s['line_start'],s['line_end'];assert 1<=a<=b<=len(lines),(s['path'],a,b)
 piece=b''.join(lines[a-1:b]);assert digest(piece)==s['range_sha256'],(s['path'],a,b)
 if 'range_bytes' in s:assert len(piece)==s['range_bytes'],(s['path'],a,b)

proofchecks=[]
for c in new:
 loc=c['proof_location'];file=ROOT/loc['file'];raw=file.read_bytes()
 if 'line_start' in loc:
  lines=raw.splitlines(keepends=True);part=b''.join(lines[loc['line_start']-1:loc['line_end']])
 elif 'start_marker' in loc:
  text=raw.decode();a=text.index(loc['start_marker']);b=len(text) if loc.get('end_marker')=='EOF' else text.index(loc['end_marker'],a+1);part=text[a:b].encode()
 else:raise AssertionError(('no exact new proof pointer',c['id'],loc))
 assert digest(part)==loc['sha256'],('proof hash mismatch',c['id'])
 if 'bytes' in loc:assert len(part)==loc['bytes'],c['id']
 proofchecks.append({'id':c['id'],'file':loc['file'],'sha256':loc['sha256'],'bytes':len(part)})

# Reviews are human mathematical checks. Hash verification only binds a
# recorded review to the frozen text; it does not turn it into a formal proof.
coverage={c['id']:[] for c in new};review_records=[]
for p in sorted(REVIEW.glob('*review.json')):
 rec=read(p);verdict=str(rec.get('result',rec.get('status',''))).lower()
 if not (verdict=='pass' or verdict.startswith('pass for ')):continue
 if p.name=='integration_scope_review.json':
  assert rec['schema']=='rh-independent-integration-scope-review/1'
  assert rec['no_unresolved_scope_findings'] is True
  assert rec['configuration_equals_generated_json'] is True
  assert set(rec['bound_sha256'])=={'configure_v0_27.py','increment_v0_27.json'}
  assert not rec.get('unresolved_findings',[])
  for name,expected in rec['bound_sha256'].items():assert sha(ROOT/name)==expected,('stale integration review',name)
  continue
 if p.name=='integration_scope_core_review.json':
  assert rec['schema']=='rh-independent-release-scope-review-v1'
  assert {'finish_metadata_v0_27.py','assemble_v0_27.py'}<=set(rec['bound_sha256'])
  assert not rec.get('unresolved_findings',[])
  assert not any('source_verification_v0_27_audit' in name for name in rec['bound_sha256']), 'Release review must not create a circular audit-output hash dependency'
  for name,expected in rec['bound_sha256'].items():assert sha(ROOT/name)==expected,('stale release review',name)
  continue
 path=rec.get('reviewed_file',rec.get('reviewed_main_file',rec.get('component','')+'/main.tex'))
 expected=rec.get('sha256',rec.get('reviewed_main_sha256',rec.get('reviewed_sha256',rec.get('main_tex_sha256'))))
 assert path and expected,(p,'missing reviewed-file identity')
 assert sha(ROOT/path)==expected,('stale review',p.name)
 assert not rec.get('unresolved_findings',[]),('unresolved review finding',p.name)
 reviewed=rec.get('claim_ids',rec.get('reviewed_claims',rec.get('reviewed_claim_ids',rec.get('claims_reviewed',rec.get('claims',[])))))
 if 'no_unresolved_mathematical_findings' in rec:assert rec['no_unresolved_mathematical_findings'] is True
 if reviewed and isinstance(reviewed[0],dict):
  assert all(str(c.get('status',c.get('result',''))).lower().startswith('pass') for c in reviewed),(p,'claim review not passed')
  reviewed=[c['id'] for c in reviewed]
 for name,expected_metadata in rec.get('reviewed_metadata',{}).items():
  assert sha(ROOT/name)==expected_metadata,('stale reviewed metadata',p.name,name)
 if 'provenance_sha256' in rec:
  assert sha(ROOT/rec['component']/'provenance.json')==rec['provenance_sha256'],('stale review provenance',p.name)
 if 'source_validation_file' in rec:
  assert sha(ROOT/rec['source_validation_file'])==rec['source_validation_sha256'],('stale source validation',p.name)
 assert all(isinstance(cid,str) for cid in reviewed),(p,'review claim identities must be strings')
 for cid in reviewed:
  if cid in coverage:coverage[cid].append(str(p.relative_to(ROOT)))
 review_records.append({'review':str(p.relative_to(ROOT)),'sha256':sha(p),'reviewed_file':path,'reviewed_sha256':expected,'claims':reviewed})
assert all(coverage.values()),('unreviewed new claims',[k for k,v in coverage.items() if not v])
write(REVIEW/'mathematical_review_coverage_v0_27.json',{'version':'0.27','scope':'Independent human mathematical review, bound to frozen component text; not formal verification','coverage':coverage,'review_records':review_records})
write(REVIEW/'proof_location_audit_v0_27.json',{'result':'PASS','scope':'Exact byte locators for every new claim; unchanged historical pointers retained','proofs':proofchecks})
targets['validation'].update(all_target_file_and_range_hashes_verified=True,verification_note='All active target file and range hashes checked against the pinned Git blobs by audit_v0_27.py.')
write(ROOT/'next_source_targets.json',targets)
input_names=['provenance.json','source_index.json','next_source_targets.json','configure_v0_27.py','increment_v0_27.json','assemble_v0_27.py','merge_v0_27.py','finish_metadata_v0_27.py','dependency_audit_v0_27/obligation_map.json','dependency_audit_v0_27/audit.txt','dependency_audit_v0_27/source_anchors.json','dependency_audit_v0_27/target_scope_updates.json','dependency_audit_v0_27/global_branch_scope_updates.json','dependency_audit_v0_27/retirement_candidates.json','dependency_audit_v0_27/input_manifest.json','reviews_v0_27/integration_scope_review.txt','reviews_v0_27/integration_scope_review.json','reviews_v0_27/semantic_scope_review.txt']
input_names.extend(['reviews_v0_27/integration_scope_core_review.json','reviews_v0_27/integration_scope_core_review.txt'])
for component in cfg['components']:
 input_names.extend(component+'/'+name for name in ['main.tex','provenance.json','closure.json'])
report={'version':'0.27','result':'PASS','commit':pin,'prior_claims':len(prior['claims']),'claims':len(claims),'new_claims':len(new),'claim_source_ranges':len(source_records),'indexed_source_files':len(files),'source_files_checked_including_targets':len(all_paths),'active_target_ranges':len(targets['targets']),'semantic_audit_source_ranges':len(semantic_sources),'semantic_obligation_nodes':len(nodes),'all_prior_semantic_node_identities_preserved':True,'semantic_map_acyclic':True,'integration_scope_review_bound_to_configuration':True,'new_proof_ranges_checked':len(proofchecks),'all_source_bytes_match_pinned_git_blobs':True,'all_ranges_verified':True,'historical_claim_fields_and_source_arrays_preserved':True,'historical_source_file_records_preserved':True,'historical_reference_edges_preserved':True,'reference_graph_acyclic':True,'global_branch_objects_preserved':True,'previous_manifest_entries_checked':oldcount,'previous_total_files_preserved':oldcount+1,'previous_root_files_archived':len(oldroots),'no_lean_build_or_kernel_replay':True,'input_sha256':{n:sha(ROOT/n) for n in input_names}}
write(REVIEW/'source_verification_v0_27_audit.json',report)
(REVIEW/'source_verification.txt').write_text(f"PASS — version 0.27\nPinned source {pin}\n{len(all_paths)} complete source files match immutable Git blobs.\n{len(source_records)} claim-source ranges and {len(targets['targets'])} active continuation ranges match recorded SHA256.\n{len(proofchecks)} new proof ranges match their frozen text.\nThis is source/proof navigation verification, not Lean compilation, kernel replay or a proof of the remaining arithmetic inputs.\n")
(REVIEW/'continuity_audit.txt').write_text(f"PASS — version 0.27\nEvery original field of all {len(prior['claims'])} claims is unchanged; supersessions are additive.\nAll previous source-file records, reference adjacency lists and global-branch objects are unchanged.\nAll {oldcount+1} predecessor files are preserved; {len(oldroots)} predecessor root files are archived exactly in history/version_0_26.\nReference DAG has {len(graph)} vertices and {sum(map(len,graph.values()))} edges and is acyclic.\nSemantic obligations live separately in dependency_audit_v0_27/obligation_map.json; the reference DAG is not a completion certificate.\n")
print(json.dumps(report,indent=2))
