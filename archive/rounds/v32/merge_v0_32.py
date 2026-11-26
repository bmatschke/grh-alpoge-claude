#!/usr/bin/env python3
"""Merge reviewed claims additively; retain every predecessor claim/source/edge."""
from pathlib import Path
import argparse, collections, copy, hashlib, json, subprocess
ROOT=Path(__file__).resolve().parent
OLD=ROOT/'history/version_0_31'
PIN='7cbf7a0c32fca1badf05931879a37c3f8a2b03b4'
URL='https://github.com/CocoSgt/riemann-hypothesis-lean/blob/'+PIN+'/'
p=argparse.ArgumentParser(description=__doc__)
p.add_argument('--repo',type=Path,required=True)
args=p.parse_args();repo=args.repo.resolve()
assert subprocess.check_output(['git','-C',str(repo),'rev-parse','HEAD']).decode().strip()==PIN
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def read(p):return json.loads(p.read_text())
def write(p,d):p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n')
cfg=read(ROOT/'increment_v0_32.json')
old=read(OLD/'provenance.json');d=copy.deepcopy(old)
d.update(artifact_version='0.32',date=cfg['date'],predecessor_version='0.31',scope=cfg['scope'])
d.setdefault('merge_inputs_history',[]).append(dict(version='0.31',inputs=copy.deepcopy(old['merge_inputs'])))
d['merge_inputs']={}
d['new_component_ledgers']=[c+'/provenance.json' for c in cfg['components']]
new=[]
for name in cfg['components']:
    path=ROOT/name/'provenance.json';comp=read(path)
    d['merge_inputs'][name]=dict(ledger=name+'/provenance.json',sha256=sha(path))
    d['component_scope_metadata_as_received'][name]={k:v for k,v in comp.items() if k not in ['claims','source_files']}
    for item in comp['claims']:
        c=copy.deepcopy(item);c['component_ledger']=name+'/provenance.json'
        c.setdefault('classification','B');c.setdefault('introduced_in','0.32');new.append(c)
    d['component_input_boundaries'][name]=dict(
      status='Human implications complete in their explicitly retained supplied-data scope; producer existence is not inferred.',
      source_ledger=name+'/provenance.json',closure_file=name+'/closure.json',
      arithmetic_premises=[dict(claim=c['id'],inputs=c.get('remaining_inputs',c.get('remaining_arithmetic_input',[]))) for c in comp['claims']])
ids={c['id'] for c in old['claims']}
assert len(new)==cfg['expected_new_claims']
assert len({c['id'] for c in new})==cfg['expected_new_claims'] and not ids.intersection(c['id'] for c in new)
assert set(cfg['claim_updates'])<=ids
for c in d['claims']:
    if c['id'] in cfg['claim_updates']:c['version_0_32_update']=copy.deepcopy(cfg['claim_updates'][c['id']])
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
          url=URL+path,first_indexed_in='0.32')
d['source_files']=[filemap[k] for k in sorted(filemap)]
d['semantic_dependency_audit']=dict(artifact_version='0.32',
 file='dependency_audit_v0_32/obligation_map.json',explanatory_chapter='dependency_audit_v0_32/main.tex',
 complete_backlog_disposition='dependency_audit_v0_32/target_disposition.json',
 remaining_leaf_register='dependency_audit_v0_32/remaining_leaf_register.json',
 scope='Selected sufficient interfaces with completed consumers distinct from open producers and shared work.')
d['version_0_32_local_conclusions']=dict(local_conclusions=cfg['new_in_this_version'],
 remaining_major_inputs=cfg['remaining_major_inputs'],next_priority=cfg['next_local_priority'],
 published_applications='dependency_audit_v0_32/published_applications.json',
 historical_correction='RF16 remains governed by the preserved DEX11 correction; no new correction is introduced.')
d['validation']=dict(previous_claims_preserved=len(old['claims']),new_claims=len(new),
 claim_count=len(d['claims']),source_link_count=sum(len(c['sources']) for c in d['claims']),
 source_file_count=len(filemap),dependency_graph_acyclic=True,dependency_graph_is_lean_transitive_audit=False,
 lean_build=False,kernel_replay=False,detailed_validation_file='validation_v0_32.json')
write(ROOT/'provenance.json',d)
write(ROOT/'source_index.json',dict(commit=PIN,artifact_version='0.32',source_files=d['source_files']))

targets=read(OLD/'next_source_targets.json')
disp=read(ROOT/'dependency_audit_v0_32/target_disposition.json')
assert len(targets['targets'])==len(disp['records'])==245
for t,r in zip(targets['targets'],disp['records']):
    digest=hashlib.sha256(json.dumps(t,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()).hexdigest()
    assert digest==r['predecessor_record_sha256']
    t['version_0_32_disposition']=copy.deepcopy(r)
targets.update(version='0.32',
 status='All 245 original compound records retained, with additive v0.32 reductions. Current open tasks are in the selected leaf register; no whole scope is silently closed by a subclaim.',
 next_local_priority=cfg['next_local_priority'],completed_previous_frontier=cfg['new_in_this_version'],
 count_policy=disp['category_count_policy'])
targets['version_0_32_precision_notes']=cfg['precision_notes']
targets['version_0_32_selected_frontier_files']=['dependency_audit_v0_32/remaining_leaf_register.json','dependency_audit_v0_32/obligation_map.json']
targets['version_0_32_disposition_coverage']=disp['coverage']
targets['validation']=dict(all_inherited_records_preserved=True,all_inherited_records_dispositioned=True,
 original_record_hashes_checked=True,detailed_validation='validation_v0_32.json')
write(ROOT/'next_source_targets.json',targets)
cp=read(OLD/'continuation_checkpoint.json')
cp.update(artifact_version='0.32',date=cfg['date'],predecessor_version='0.31',status=cfg['scope'],
 new_in_this_version=cfg['new_in_this_version'],remaining_major_inputs=cfg['remaining_major_inputs'],
 next_targets=[cfg['next_local_priority']]+cfg['remaining_major_inputs'],
 previous_source_targets_file='history/version_0_31/next_source_targets.json',
 current_dependency_audit=d['semantic_dependency_audit'],
 current_deliverable=dict(main='RH_readable_reconstruction_v0_32.tex',archive='RH_reconstruction_v0_32.zip',
 audit='RH_dependency_audit_v0_32.txt',pdf_generated=False),
 main_note_pages=None,new_section_start_pages={},validation=d['validation'])
cp.setdefault('retained_prior_results',[]).extend(read(OLD/'increment_v0_31.json')['new_in_this_version'])
cp['retained_prior_results_note']='Every predecessor file remains at its unchanged path or as exact bytes in history/version_0_31. Original claim fields, source arrays and claim edges are unchanged. RF16 carries an explicit current correction and a replacement proof, with its historical bytes retained.'
cp.setdefault('precision_constraints',[]).extend(cfg['precision_notes'])
cp['version_0_32_update']=d['version_0_32_local_conclusions']
cp['next_step_notes']=[dict(file='continuation_notes_v0_32/'+name,
 sha256=sha(ROOT/'continuation_notes_v0_32'/name),status='Source-anchored work plan; no new proof or closure claim.')
 for name in ['next_base_extension.txt','next_count_ii.txt']]
cp['logical_component_page_map']={}
for comp in cfg['components']:
    cs=[c for c in new if c['component_ledger'].split('/')[0]==comp]
    prefix=''.join(t for t in cs[0]['id'] if not t.isdigit())
    cp['logical_component_page_map'][prefix]=dict(component=comp,claims=[c['id'] for c in cs],
      fragment=comp+'/main.tex',page_numbers=None)
write(ROOT/'continuation_checkpoint.json',cp)
lines=['RH/Dirichlet-GRH reconstruction v0.32 — claim provenance','Pinned source: '+PIN,cfg['scope'],
 'Current audit: dependency_audit_v0_32/obligation_map.json',
 'RF16 correction: use DEX11 and the version_0_32_update; original bytes retained.','']
for c in d['claims']:
    lines += [c['id']+' — '+c['title'],'Status: '+c.get('status','See original record.')]
    if c.get('proof_location'):lines.append('Proof: '+json.dumps(c['proof_location'],ensure_ascii=False))
    for tag in ['version_0_30_update','version_0_31_update','version_0_32_update']:
        if c.get(tag):lines.append(tag+': '+c[tag]['statement'])
    for s in c['sources']:
        lines.append('  '+s['path']+':'+str(s['line_start'])+'-'+str(s['line_end'])+' | '+s.get('declaration','')+' | '+s['sha256']+' | '+s['range_sha256'])
    lines.append('')
(ROOT/'provenance.txt').write_text('\n'.join(lines)+'\n')
(ROOT/'README.txt').write_text('''RH / DIRICHLET-GRH HUMAN RECONSTRUCTION — VERSION 0.32
22 November 2026

START HERE
RH_dependency_audit_v0_32.txt is the self-contained current audit.
RH_readable_reconstruction_v0_32.tex contains every historical mathematical
chapter and the new version-0.32 proof claims, with the current audit first.
continuation_checkpoint.json records precise remaining producers and priority.

STATUS
'''+cfg['scope']+'''

NEW WORK
'''+''.join(str(i)+'. '+v+'\n' for i,v in enumerate(cfg['new_in_this_version'],1))+'''
CURRENT AUDIT
dependency_audit_v0_32/obligation_map.json: connected selected sufficient
interfaces, with open producers, completed conditional proofs, B proof tasks
and shared refinements distinguished.
dependency_audit_v0_32/remaining_leaf_register.json: every selected open leaf
with A/B/C/D category and exact contract.
dependency_audit_v0_32/target_disposition.json: all245 inherited compound
scopes and precise current subclaim reductions; no completion percentage.
dependency_audit_v0_32/published_applications.json: retained checked HC-Deg application and exact pointer to inherited classical registries.
reviews_v0_32/: independent mathematical reviews and graph review bound to
finalized proof bytes. The release registry supersedes any component's older
pending-review annotation without rewriting reviewed metadata.

NEXT PRIORITY
'''+cfg['next_local_priority']+'''

CONCRETE CONTINUATION NOTES
continuation_notes_v0_32/next_base_extension.txt ranks the exact analytic
subtargets, beginning with the actual finite isotropic Heisenberg average
and zero constant terms. It records the simultaneous ioP choice and uniform
derivative-growth quantifiers that must be preserved.
continuation_notes_v0_32/next_count_ii.txt traces the original same-ideal
rank-four Hida/HasAut and P1-only support producer on both original Links.
These notes identify work to do; they assert no additional closure.

CONTINUITY
Every predecessor file is retained at its old path or in history/version_0_31.
Original claim/source fields and mathematical claim edges remain unchanged.
Current scope corrections are additive. RF16's omitted epsilon/100 term is
explicitly repaired in DEX11, which reproves the original conclusion.

REPRODUCING THIS INCREMENT (run from this directory)
python configure_v0_32.py
python build_audit_v0_32.py
python write_readable_audit_v0_32.py
python build_audit_v0_32.py
python assemble_v0_32.py
python merge_v0_32.py --repo /path/to/pinned/checkout
python backtrack.py --repo /path/to/pinned/checkout --check-all
python validate_tex_v0_32.py
python validate_v0_32.py --repo /path/to/pinned/checkout
python package_v0_32.py

The component ledgers and reviews are preserved as reviewed inputs.
The source pin is '''+PIN+'''.
No Lean build or kernel replay is claimed. Draft-mode TeX checks syntax and
references; no PDF is generated and visual layout is not certified.
Historical scripts retain their original historical assumptions and outputs.
''')
print(json.dumps(d['validation'],indent=2))
