#!/usr/bin/env python3
"""Merge reviewed claims additively; retain every predecessor claim/source/edge."""
from pathlib import Path
import argparse, collections, copy, hashlib, json, subprocess
ROOT=Path(__file__).resolve().parent
OLD=ROOT/'history/version_0_38'
PIN='7cbf7a0c32fca1badf05931879a37c3f8a2b03b4'
URL='https://github.com/CocoSgt/riemann-hypothesis-lean/blob/'+PIN+'/'
p=argparse.ArgumentParser(description=__doc__)
p.add_argument('--repo',type=Path,required=True)
args=p.parse_args();repo=args.repo.resolve()
assert subprocess.check_output(['git','-C',str(repo),'rev-parse','HEAD']).decode().strip()==PIN
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def read(p):return json.loads(p.read_text())
def write(p,d):p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n')
cfg=read(ROOT/'increment_v0_39.json')
old=read(OLD/'provenance.json');d=copy.deepcopy(old)
d.update(artifact_version='0.39',date=cfg['date'],predecessor_version='0.38',scope=cfg['scope'])
d.setdefault('merge_inputs_history',[]).append(dict(version='0.38',inputs=copy.deepcopy(old['merge_inputs'])))
d['merge_inputs']={}
d['new_component_ledgers']=[c+'/provenance.json' for c in cfg['components']]
new=[]
for name in cfg['components']:
    path=ROOT/name/'provenance.json';comp=read(path)
    d['merge_inputs'][name]=dict(ledger=name+'/provenance.json',sha256=sha(path))
    d['component_scope_metadata_as_received'][name]={k:v for k,v in comp.items() if k not in ['claims','source_files']}
    for item in comp['claims']:
        c=copy.deepcopy(item);c['component_ledger']=name+'/provenance.json'
        c.setdefault('classification','B');c.setdefault('introduced_in','0.39');new.append(c)
    d['component_input_boundaries'][name]=dict(
      status='Human implications complete in their explicitly retained supplied-data scope; producer existence is not inferred.',
      source_ledger=name+'/provenance.json',closure_file=name+'/closure.json',
      arithmetic_premises=[dict(claim=c['id'],inputs=c.get('remaining_inputs',c.get('remaining_arithmetic_input',[]))) for c in comp['claims']])
ids={c['id'] for c in old['claims']}
assert len(new)==cfg['expected_new_claims']
assert len({c['id'] for c in new})==cfg['expected_new_claims'] and not ids.intersection(c['id'] for c in new)
assert set(cfg['claim_updates'])<=ids
for c in d['claims']:
    if c['id'] in cfg['claim_updates']:c['version_0_39_update']=copy.deepcopy(cfg['claim_updates'][c['id']])
d['claims']+=new
graph=d['mathematical_dependency_graph']
for c in new:graph[c['id']]=c.get('depends_on',[])
assert set(graph)=={c['id'] for c in d['claims']}
active=set();done=set();order=[]
def visit(k):
    assert k in graph,('unknown claim dependency',k)
    assert k not in active,('claim cycle',k)
    if k in done:return
    active.add(k)
    for nxt in graph[k]:visit(nxt)
    active.remove(k);done.add(k);order.append(k)
for k in graph:visit(k)
d['dependency_topological_order']=order
filemap={r['path']:copy.deepcopy(r) for r in old['source_files']}
for c in new:
    for r in c['sources']:
        path=r['path'];digest=r.get('sha256',r.get('file_sha256',r.get('source_full_file_sha256')))
        if path in filemap:
            assert filemap[path]['sha256']==digest,path
            continue
        raw=(repo/path).read_bytes()
        assert hashlib.sha256(raw).hexdigest()==digest,path
        assert subprocess.check_output(['git','-C',str(repo),'show',PIN+':'+path])==raw,path
        filemap[path]=dict(path=path,sha256=digest,bytes=len(raw),line_count=len(raw.splitlines()),
          lines=len(raw.splitlines()),verified_equal_to_pinned_git_blob=True,
          worktree_source_present=True,worktree_bytes_compared_to_git_blob=True,
          url=URL+path,first_indexed_in='0.39')
d['source_files']=[filemap[k] for k in sorted(filemap)]
d['semantic_dependency_audit']=dict(artifact_version='0.39',
 file='dependency_audit_v0_39/obligation_map.json',explanatory_chapter='dependency_audit_v0_39/main.tex',
 complete_backlog_disposition='dependency_audit_v0_39/target_disposition.json',
 remaining_leaf_register='dependency_audit_v0_39/remaining_leaf_register.json',
 route_coverage='dependency_audit_v0_39/route_coverage.json',
 scope='Selected sufficient interfaces with completed consumers distinct from open producers and shared work.')
d['version_0_39_local_conclusions']=dict(local_conclusions=cfg['new_in_this_version'],
 remaining_major_inputs=cfg['remaining_major_inputs'],next_priority=cfg['next_local_priority'],
 published_applications='dependency_audit_v0_39/published_applications.json',
 historical_correction='RF16 remains governed by the preserved DEX11 correction; no new correction is introduced.')
d['validation']=dict(previous_claims_preserved=len(old['claims']),new_claims=len(new),
 claim_count=len(d['claims']),source_link_count=sum(len(c['sources']) for c in d['claims']),
 source_file_count=len(filemap),dependency_graph_acyclic=True,dependency_graph_is_lean_transitive_audit=False,
 lean_build=False,kernel_replay=False,detailed_validation_file='validation_v0_39.json')
write(ROOT/'provenance.json',d)
write(ROOT/'source_index.json',dict(commit=PIN,artifact_version='0.39',source_files=d['source_files']))

targets=read(OLD/'next_source_targets.json')
disp=read(ROOT/'dependency_audit_v0_39/target_disposition.json')
assert len(targets['targets'])==len(disp['records'])==245
for t,r in zip(targets['targets'],disp['records']):
    digest=hashlib.sha256(json.dumps(t,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()).hexdigest()
    assert digest==r['predecessor_record_sha256']
    t['version_0_39_disposition']=copy.deepcopy(r)
targets.update(version='0.39',
 status='All 245 original compound records retained, with additive v0.39 reductions. Current open tasks are in the selected leaf register; no whole scope is silently closed by a subclaim.',
 next_local_priority=cfg['next_local_priority'],completed_previous_frontier=cfg['new_in_this_version'],
 count_policy=disp['category_count_policy'])
targets['version_0_39_precision_notes']=cfg['precision_notes']
targets['version_0_39_selected_frontier_files']=['dependency_audit_v0_39/remaining_leaf_register.json','dependency_audit_v0_39/obligation_map.json']
targets['version_0_39_disposition_coverage']=disp['coverage']
targets['validation']=dict(all_inherited_records_preserved=True,all_inherited_records_dispositioned=True,
 original_record_hashes_checked=True,detailed_validation='validation_v0_39.json')
write(ROOT/'next_source_targets.json',targets)
cp=read(OLD/'continuation_checkpoint.json')
cp.update(artifact_version='0.39',date=cfg['date'],predecessor_version='0.38',status=cfg['scope'],
 new_in_this_version=cfg['new_in_this_version'],remaining_major_inputs=cfg['remaining_major_inputs'],
 next_targets=[cfg['next_local_priority']]+cfg['remaining_major_inputs'],
 previous_source_targets_file='history/version_0_38/next_source_targets.json',
 current_dependency_audit=d['semantic_dependency_audit'],
 current_deliverable=dict(main='RH_readable_reconstruction_v0_39.tex',archive='RH_reconstruction_v0_39.zip',
 audit='RH_dependency_audit_v0_39.txt',pdf_generated=False),
 main_note_pages=None,new_section_start_pages={},validation=d['validation'])
cp.setdefault('retained_prior_results',[]).extend(read(ROOT/'increment_v0_38.json')['new_in_this_version'])
cp['retained_prior_results_note']='Every predecessor file remains at its unchanged path or as exact bytes in history/version_0_38. Original claim fields, source arrays and claim edges are unchanged. RF16 carries an explicit current correction and a replacement proof, with its historical bytes retained.'
cp.setdefault('precision_constraints',[]).extend(cfg['precision_notes'])
cp['version_0_39_update']=d['version_0_39_local_conclusions']
cp['next_step_notes']=[dict(file='continuation_notes_v0_39/'+name,
 sha256=sha(ROOT/'continuation_notes_v0_39'/name),status='Source-anchored work plan; no new proof or closure claim.')
 for name in ['next_analytic_and_common.txt','next_count_ii.txt','next_division_and_readings.txt']
 if (ROOT/'continuation_notes_v0_39'/name).is_file()]
cp['logical_component_page_map']={}
for comp in cfg['components']:
    cs=[c for c in new if c['component_ledger'].split('/')[0]==comp]
    prefix=''.join(t for t in cs[0]['id'] if not t.isdigit())
    cp['logical_component_page_map'][prefix]=dict(component=comp,claims=[c['id'] for c in cs],
      fragment=comp+'/main.tex',page_numbers=None)
write(ROOT/'continuation_checkpoint.json',cp)
lines=['RH/Dirichlet-GRH reconstruction v0.39 — claim provenance','Pinned source: '+PIN,cfg['scope'],
 'Current audit: dependency_audit_v0_39/obligation_map.json',
 'RF16 correction: use DEX11 and its preserved scope correction; original bytes retained.','']
for c in d['claims']:
    lines += [c['id']+' — '+c['title'],'Status: '+c.get('status','See original record.')]
    if c.get('proof_location'):lines.append('Proof: '+json.dumps(c['proof_location'],ensure_ascii=False))
    for tag in sorted(k for k in c if k.startswith('version_') and k.endswith('_update')):
        if c.get(tag):
            value=c[tag]
            message=value['statement'] if isinstance(value,dict) and 'statement' in value else json.dumps(value,ensure_ascii=False,sort_keys=True)
            lines.append(tag+': '+message)
    for s in c['sources']:
        lines.append('  '+s['path']+':'+str(s['line_start'])+'-'+str(s['line_end'])+' | '+s.get('declaration','')+' | '+s['sha256']+' | '+s['range_sha256'])
    lines.append('')
(ROOT/'provenance.txt').write_text('\n'.join(lines)+'\n')
(ROOT/'README.txt').write_text('RH / DIRICHLET-GRH HUMAN RECONSTRUCTION — VERSION 0.39\n22 November 2026\n\nSTART HERE\nRH_dependency_audit_v0_39.txt: self-contained current audit and all remaining contracts.\nRH_readable_reconstruction_v0_39.tex: all historical chapters and the new proofs.\ncontinuation_checkpoint.json: precise scope, validation and next priorities.\n\nSTATUS\n'+cfg['scope']+'\n\nNEW WORK\n'+'\n\n'.join(cfg['new_in_this_version'])+'\n\nCURRENT AUDIT\ndependency_audit_v0_39/obligation_map.json: selected sufficient interfaces.\nremaining_leaf_register.json: all open A/B/C/D contracts.\ntarget_disposition.json: every inherited compound target retained.\npublished_applications.json: new checked Milne, Miller–Schmid and Chenevier applications, with predecessor registries retained.\nreviews_v0_39/: independent mathematical reviews bound to released proof bytes.\n\nNEXT PRIORITY\n'+cfg['next_local_priority']+'\n\nCONTINUATION NOTES\ncontinuation_notes_v0_39/next_analytic_and_common.txt\ncontinuation_notes_v0_39/next_count_ii.txt\ncontinuation_notes_v0_39/next_division_and_readings.txt\n\nCONTINUITY\nEvery predecessor file is retained at its old path or in history/version_0_38.\nOriginal claim fields, source arrays and mathematical edges are unchanged.\nThe RF16 correction remains governed by DEX11.\n\nREPRODUCTION\npython configure_v0_39.py\npython build_audit_v0_39.py\npython write_readable_audit_v0_39.py\npython build_audit_v0_39.py\npython assemble_v0_39.py\npython audit_route_coverage_v0_39.py\npython merge_v0_39.py --repo /path/to/pinned/checkout\npython backtrack.py --repo /path/to/pinned/checkout --check-all\npython validate_tex_v0_39.py\npython validate_v0_39.py --repo /path/to/pinned/checkout\npython package_v0_39.py\n\nOPTIONAL COMPONENT-LEDGER REBUILD\nrestore_predecessor_v0_38.py DESTINATION reconstructs exact v0.38 bytes from this archive alone. Use that destination for the inherited-proof argument (--human-root or --baseline as specified by the component builder); use the current reconstruction as --peer-root where requested. When rebuilding a v0.39 component ledger, the pinned Lean checkout is a separate --source input.\n\nSource pin: '+PIN+'\nNo Lean build or kernel replay. Draft TeX checks syntax and references; no PDF.\n')
print(json.dumps(d['validation'],indent=2))
