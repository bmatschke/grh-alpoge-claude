#!/usr/bin/env python3
"""Merge finalized v0.30 proofs additively into the immutable v0.29 ledger."""
from pathlib import Path
import argparse
import copy
import hashlib
import json
import subprocess

ROOT=Path(__file__).resolve().parent
OLD=ROOT/'history/version_0_29'
PIN='7cbf7a0c32fca1badf05931879a37c3f8a2b03b4'
URL='https://github.com/CocoSgt/riemann-hypothesis-lean/blob/'+PIN+'/'
parser=argparse.ArgumentParser(description=__doc__)
parser.add_argument('--repo',type=Path,required=True)
args=parser.parse_args()
args.repo=args.repo.resolve()
assert subprocess.check_output(['git','-C',str(args.repo),'rev-parse','HEAD']).decode().strip()==PIN

def sha(b):return hashlib.sha256(b).hexdigest()
def read(p):return json.loads(p.read_text())
def write(p,d):p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n')

cfg=read(ROOT/'increment_v0_30.json')
old=read(OLD/'provenance.json')
d=copy.deepcopy(old)
d.update(artifact_version='0.30',date=cfg['date'],predecessor_version='0.29',scope=cfg['scope'])
d['new_component_ledgers']=[c+'/provenance.json' for c in cfg['components']]
d.setdefault('merge_inputs_history',[]).append(dict(version='0.29',inputs=copy.deepcopy(old['merge_inputs'])))
d['merge_inputs']={}
newclaims=[]
for component in cfg['components']:
    path=ROOT/component/'provenance.json';comp=read(path)
    d['merge_inputs'][component]=dict(ledger=str(path.relative_to(ROOT)),sha256=sha(path.read_bytes()))
    d['component_scope_metadata_as_received'][component]={k:v for k,v in comp.items() if k not in ['claims','source_files']}
    for item in comp['claims']:
        c=copy.deepcopy(item)
        c['component_ledger']=str(path.relative_to(ROOT))
        c.setdefault('classification','A' if c['id']=='HX1' else 'B')
        c.setdefault('introduced_in','0.30')
        newclaims.append(c)
    d['component_input_boundaries'][component]=dict(
        status='Complete human implications in their explicitly retained conditional scopes.',
        source_ledger=str(path.relative_to(ROOT)),
        arithmetic_premises=[dict(claim=c['id'],inputs=c.get('remaining_inputs',c.get('remaining_arithmetic_input',[]))) for c in comp['claims']])
oldids={c['id'] for c in d['claims']}
assert not oldids.intersection(c['id'] for c in newclaims)
assert len(newclaims)==26 and len({c['id'] for c in newclaims})==26
for c in d['claims']:
    if c['id'] in cfg['claim_updates']:
        c['version_0_30_update']=copy.deepcopy(cfg['claim_updates'][c['id']])
d['claims']+=newclaims
graph=d['mathematical_dependency_graph']
for c in newclaims:graph[c['id']]=c.get('depends_on',[])
assert set(graph)=={c['id'] for c in d['claims']}
done=set();active=set();order=[]
def visit(k):
    assert k in graph,('unknown claim dependency',k)
    assert k not in active,('cycle',k)
    if k in done:return
    active.add(k)
    for v in graph[k]:visit(v)
    active.remove(k);done.add(k);order.append(k)
for k in graph:visit(k)
d['dependency_topological_order']=order

auditdir=ROOT/'dependency_audit_v0_30'
literature=read(auditdir/'literature_audit.json')
hx=read(ROOT/'host_window_installation/provenance.json')
xylouris=dict(
    id='HX-Xylouris-SmallOne',classification='A',consumer='HX1 / literal SmallOne',
    theorem='Xylouris, Acta Arithmetica 150 (2011), Theorem 1.1',
    url='https://www.impan.pl/shop/en/publication/transaction/download/product/83078',
    hypotheses_checked=['Integer modulus N>=2','Residue a=1, so gcd(a,N)=1','The uniform effective constant is fixed before N'],
    conclusion='Least prime p congruent to1 moduloN is at most C*N^5.18; C is absorbed uniformly into the SmallOne exponent using N>=2.',
    hypothesis_matching_explanation='Set Cstar=max(C,1) and exponent=max(1,5.18+log(Cstar)/log(2)); then C*N^5.18<=N^exponent for every N>=2.',
    proof_claim='HX1',source_anchors=hx['claims'][0]['sources'],
    primary_source_rechecked_this_round=True,
    not_supplied='Neither the independent cohomological window nor the geometric DesignExists producer.')
registry=dict(schema='rh-published-applications/1',artifact_version='0.30',source_commit=PIN,
    meaning='A means a named published result with the displayed consumer hypotheses checked. Inherited entries keep only their original documented scopes.',
    freshly_checked_applications=literature['rechecked_classical_applications']+[xylouris],
    inherited_registries=literature['inherited_registries'],
    counts=dict(freshly_checked_applications=8,inherited_registry_entries=101,inherited_registry_files=22),
    rejected_shortcuts=literature['rejected_shortcuts'])
write(auditdir/'published_applications.json',registry)

filemap={x['path']:copy.deepcopy(x) for x in old['source_files']}
checked={}
def source_records(v):
    if isinstance(v,dict):
        if isinstance(v.get('path'),str) and v['path'].startswith('src/') and any(k in v for k in ['sha256','file_sha256','source_full_file_sha256']):yield v
        for x in v.values():yield from source_records(x)
    elif isinstance(v,list):
        for x in v:yield from source_records(x)

def add_source(r):
    path=r['path'];expected=r.get('sha256',r.get('file_sha256',r.get('source_full_file_sha256')))
    if path in filemap:
        assert filemap[path]['sha256']==expected,('conflicting source hash',path)
        return
    raw=(args.repo/path).read_bytes()
    assert sha(raw)==expected,('source hash mismatch',path)
    if path not in checked:
        blob=subprocess.check_output(['git','-C',str(args.repo),'show',PIN+':'+path])
        assert blob==raw,('source differs from pin',path)
        checked[path]=True
    filemap[path]=dict(path=path,sha256=expected,bytes=len(raw),line_count=len(raw.splitlines()),
        lines=len(raw.splitlines()),verified_equal_to_pinned_git_blob=True,
        worktree_source_present=True,worktree_bytes_compared_to_git_blob=True,url=URL+path,
        first_indexed_in='0.30')

for c in newclaims:
    for r in c['sources']:add_source(r)
for p in sorted(auditdir.glob('*.json')):
    for r in source_records(read(p)):add_source(r)
d['source_files']=[filemap[k] for k in sorted(filemap)]
d['semantic_dependency_audit']=dict(artifact_version='0.30',file='dependency_audit_v0_30/obligation_map.json',
    explanatory_chapter='dependency_audit_v0_30/main.tex',complete_backlog_disposition='dependency_audit_v0_30/target_disposition.json',
    scope='Connected selected sufficient routes, not an exhaustive Lean graph or a claim of mathematical minimality; proof obligations and shared-work refinements are distinct.')
d['version_0_30_local_conclusions']=dict(local_conclusions=cfg['new_in_this_version'],
    remaining_major_inputs=cfg['remaining_major_inputs'],next_priority=cfg['next_local_priority'],
    published_applications='dependency_audit_v0_30/published_applications.json')
d['validation']=dict(previous_claims_preserved=len(old['claims']),new_claims=len(newclaims),
    claim_count=len(d['claims']),source_link_count=sum(len(c['sources']) for c in d['claims']),
    source_file_count=len(filemap),dependency_graph_acyclic=True,
    dependency_graph_is_lean_transitive_audit=False,lean_build=False,kernel_replay=False,
    detailed_validation_file='validation_v0_30.json')
write(ROOT/'provenance.json',d)
write(ROOT/'source_index.json',dict(commit=PIN,artifact_version='0.30',source_files=d['source_files']))

targets=read(OLD/'next_source_targets.json')
disposition=read(auditdir/'target_disposition.json')
records=disposition['records']
assert len(targets['targets'])==len(records)==245
for i,(target,rec) in enumerate(zip(targets['targets'],records),1):
    assert rec['original_index_one_based']==i
    digest=sha(json.dumps(target,sort_keys=True,ensure_ascii=False,separators=(',',':')).encode())
    assert rec['original_record_sha256']==digest,('inherited target changed before disposition',i)
    target['version_0_30_disposition']=copy.deepcopy(rec)
targets['version']='0.30'
targets['status']='All 245 inherited continuation records preserved and dispositioned. Current priority is the connected selected-route audit, not historical file order.'
targets['completed_previous_frontier']=cfg['completed_previous_frontier']
targets['next_local_priority']=cfg['next_local_priority']
targets['previous_version_precision_notes']=copy.deepcopy(targets.get('precision_notes',[]))
targets['precision_notes']=cfg['precision_notes']
targets['count_policy']='245 inherited records, all preserved;107 distinct scope groups. Counts are navigation bookkeeping, not independent obligations or completion percentages. See the selected audit for exact sufficient interfaces.'
targets['global_branches_unchanged']=False
targets['version_0_30_global_scope_update']=dict(
    conditional_closures=['HX host from VWinAt','MT metric transport','KA CountI aggregation','ZW tied-family numerical endpoint'],
    target_specialization='KA5–KA6 remove Case III only for power-of-two-order targets, including RH.',
    current_audit='dependency_audit_v0_30/obligation_map.json',
    complete_disposition='dependency_audit_v0_30/target_disposition.json')
targets['version_0_30_selected_frontier_files']=['dependency_audit_v0_30/global_frontier_inventory.json','dependency_audit_v0_30/count_frontier.json']
targets['version_0_30_disposition_coverage']=disposition['coverage']
targets['validation']=dict(all_inherited_records_preserved=True,all_inherited_records_dispositioned=True,
    original_record_hashes_checked=True,detailed_validation='validation_v0_30.json')
write(ROOT/'next_source_targets.json',targets)

cp=read(OLD/'continuation_checkpoint.json')
cp.update(artifact_version='0.30',date=cfg['date'],predecessor_version='0.29',status=cfg['scope'],
          user_instruction='Continue toward the complete human-readable proof, assuming the checked Lean proof is correct. Prioritize unresolved dependencies by contribution to the final theorem and deliver a minimal complete-proof dependency audit with A/B/C/D classifications.',
          new_in_this_version=cfg['new_in_this_version'],remaining_major_inputs=cfg['remaining_major_inputs'],
          next_targets=cfg['next_steps'],previous_source_targets_file='history/version_0_29/next_source_targets.json')
cp['retained_prior_results']+=read(OLD/'increment_v0_29.json')['new_in_this_version']
cp['retained_prior_results_note']='Every predecessor file is preserved either at its unchanged path or in history/version_0_29. Original claim/source fields and claim dependency edges are unchanged. Current scope updates are additive; historical frontier summaries are superseded by the connected v0.30 audit.'
cp['precision_constraints']+=cfg['precision_notes']
cp['version_0_30_update']=copy.deepcopy(d['version_0_30_local_conclusions'])
cp['current_deliverable']=dict(main='RH_readable_reconstruction_v0_30.tex',archive='RH_reconstruction_v0_30.zip',
    audit='RH_dependency_audit_v0_30.txt',pdf_generated=False,
    reason='Cumulative TeX, standalone audit and source-traceable continuation archive are the requested research deliverables.')
cp['new_section_headings']={}
cp['logical_component_page_map']={}
for component in cfg['components']:
    claims=[c for c in newclaims if c['component_ledger'].split('/')[0]==component]
    prefix=''.join(x for x in claims[0]['id'] if not x.isdigit())
    cp['logical_component_page_map'][prefix]=dict(component=component,claims=[c['id'] for c in claims],fragment=claims[0]['proof_location']['file'],page_numbers=None)
cp['validation']=copy.deepcopy(d['validation'])
cp['main_note_pages']=None
cp['new_section_start_pages']={}
write(ROOT/'continuation_checkpoint.json',cp)

lines=['RH/Dirichlet-GRH reconstruction v0.30 — claim provenance','Source pin: '+PIN,
       cfg['scope'],'','Current dependency audit: dependency_audit_v0_30/obligation_map.json',
       'All historical fields remain in provenance.json; current updates below are additive.','']
for c in d['claims']:
    lines += [c['id']+' — '+c['title'],'Status: '+c.get('status','See original ledger.')]
    if c.get('proof_location'):lines.append('Proof: '+json.dumps(c['proof_location'],ensure_ascii=False))
    if c.get('version_0_30_update'):lines.append('v0.30 scope: '+c['version_0_30_update']['statement'])
    for r in c['sources']:
        lines.append('  '+r['path']+':'+str(r['line_start'])+'-'+str(r['line_end'])+' | '+r.get('declaration','')+' | '+r['sha256']+' | '+r['range_sha256'])
    lines.append('')
(ROOT/'provenance.txt').write_text('\n'.join(lines)+'\n')

readme='''RH / DIRICHLET-GRH HUMAN RECONSTRUCTION — VERSION 0.30
22 November 2026

START HERE
RH_dependency_audit_v0_30.txt is the self-contained current audit.
RH_readable_reconstruction_v0_30.tex contains all earlier mathematical
chapters and the five new proof components, with the current audit first.
continuation_checkpoint.json records the exact next priority.

STATUS
'''+cfg['scope']+'''

WHAT CHANGED
'''+''.join(str(i)+'. '+x+'\n' for i,x in enumerate(cfg['new_in_this_version'],1))+'''
NEXT PRIORITY
'''+cfg['next_local_priority']+'''

AUDIT FILES
dependency_audit_v0_30/obligation_map.json: connected selected sufficient
routes, with exact logical gates distinct from open implication proofs and
shared-work refinements. RH and unrestricted Dirichlet-GRH roots differ.
dependency_audit_v0_30/target_disposition.json: every one of the 245 inherited
records, including complete compound scopes, closed pieces and optional routes.
dependency_audit_v0_30/global_frontier_inventory.json and count_frontier.json:
source-anchored detailed producer classifications.
dependency_audit_v0_30/published_applications.json: eight checked applications
this round and the exact inherited registry scopes.
reviews_v0_30/: independent reviews bound to the finalized chapter hashes.

BOUNDARIES
A/B/C/D classifies the kind of argument, separately from completion status.
D describes our human source understanding, not a problem in the checked proof.
This is a minimal sufficient-interface audit, not a theorem that no smaller
proof exists, not an exhaustive Lean dependency graph, and not a completion
percentage. The 245 records and 107 scope groups are navigation statistics.

CONTINUITY AND VALIDATION
All predecessor files remain at their old paths or have an exact copy in
history/version_0_29. Every original claim field, source list and dependency
edge is preserved; current conclusions are additive updates.
The source is pinned at '''+PIN+'''.
No Lean build or kernel replay is claimed. TeX validation uses draft mode,
resolves references and produces no PDF; it does not certify visual layout.

REPRODUCING THE INCREMENT (run from this directory)
python configure_v0_30.py
python build_parent_components_v0_30.py --repo /path/to/pinned/checkout
python assemble_v0_30.py
python merge_v0_30.py --repo /path/to/pinned/checkout
python backtrack.py --repo /path/to/pinned/checkout --check-all
python validate_tex_v0_30.py
python validate_v0_30.py --repo /path/to/pinned/checkout

The five component proof/source ledgers are preserved as reviewed inputs.
SHA256SUMS and validation_v0_30.json record the packaged final bytes.
Historical scripts retain their historical assumptions and outputs; use
the version-0.30 entry points for this snapshot.
'''
(ROOT/'README.txt').write_text(readme)
print(json.dumps(d['validation'],indent=2))
