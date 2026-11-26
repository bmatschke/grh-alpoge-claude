#!/usr/bin/env python3
"""Check preserved claims, exact proof/source hashes and the complete v0.30 audit."""
from pathlib import Path
import argparse
import collections
import hashlib
import json
import subprocess

ROOT=Path(__file__).resolve().parent
OLD=ROOT/'history/version_0_29'
PIN='7cbf7a0c32fca1badf05931879a37c3f8a2b03b4'
parser=argparse.ArgumentParser(description=__doc__)
parser.add_argument('--repo',type=Path,required=True)
args=parser.parse_args()
args.repo=args.repo.resolve()

def sha(b):return hashlib.sha256(b).hexdigest()
def read(p):return json.loads(p.read_text())
def write(p,d):p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n')

assert subprocess.check_output(['git','-C',str(args.repo),'rev-parse','HEAD']).decode().strip()==PIN
old=read(OLD/'provenance.json');now=read(ROOT/'provenance.json')
oldclaims={c['id']:c for c in old['claims']};claims={c['id']:c for c in now['claims']}
assert len(claims)==len(now['claims'])==1438
for key,c in oldclaims.items():
    assert key in claims
    for field,value in c.items():assert claims[key][field]==value,('changed predecessor claim',key,field)
for key,edges in old['mathematical_dependency_graph'].items():
    assert now['mathematical_dependency_graph'][key]==edges,('changed predecessor edge',key)

prior_files=0;archived_files=0;file_cache={}
def filehash(p):
    if p not in file_cache:file_cache[p]=sha(p.read_bytes())
    return file_cache[p]
for line in (OLD/'SHA256SUMS').read_text().splitlines():
    if not line.strip():continue
    digest,rel=line.split('  ',1);prior_files+=1
    direct=ROOT/rel;archive=OLD/rel
    if direct.is_file() and filehash(direct)==digest:continue
    assert archive.is_file() and filehash(archive)==digest,('predecessor file not preserved',rel)
    archived_files+=1

newclaims=[c for c in now['claims'] if c['id'] not in oldclaims]
for c in newclaims:
    p=c['proof_location'];raw=(ROOT/p['file']).read_bytes()
    span=b''.join(raw.splitlines(keepends=True)[p['line_start']-1:p['line_end']])
    assert sha(span)==p['sha256'],('proof range hash',c['id'])
    if 'bytes' in p:assert len(span)==p['bytes'],('proof bytes',c['id'])

expected_reviewed={
 'host_window_installation/main.tex':'37c561051ae31c618455e73bf558530e2545cbb1e8808da26018fc91a3dafaeb',
 'metric_transport/main.tex':'55ac8034b4312f450ceb7be32320e2039cc6a063c89db454159b2fa5bb4142a3',
 'count_i_aggregation/main.tex':'39a8a5b5483fe5e59de6fb461e03317cf2b4934964da533402c3ea6863d61ea1',
 'tied_window_completion/main.tex':'3e102f1a3e4ddced78b5cd3e92378a3ebdfa68a52b7de5fb69e2ac997eddc7b1',
 'analytic_envelope/analytic_envelope.tex':'71df803d44f5fc658f81d6a414c88ea9d94bac8c89f43434de650f3dcf0fdb5c'}
for rel,digest in expected_reviewed.items():assert filehash(ROOT/rel)==digest,('reviewed chapter changed',rel)

graph=now['mathematical_dependency_graph'];active=set();done=set()
def visit(k):
    assert k in graph,('unknown dependency',k)
    assert k not in active,('claim dependency cycle',k)
    if k in done:return
    active.add(k)
    for nxt in graph[k]:visit(nxt)
    active.remove(k);done.add(k)
for k in graph:visit(k)
assert len(done)==1438

source_cache={};range_count=0;unique_ranges=set()
def check_source(r):
    global range_count
    path=r['path']
    expected=r.get('sha256',r.get('file_sha256',r.get('source_full_file_sha256')))
    if path not in source_cache:
        raw=(args.repo/path).read_bytes();source_cache[path]=(sha(raw),raw.splitlines(keepends=True))
    digest,lines=source_cache[path]
    assert digest==expected,('source file hash mismatch',path)
    first,last=r.get('line_start'),r.get('line_end')
    target=r.get('range_sha256',r.get('source_range_sha256'))
    if first is not None and last is not None and target:
        assert 1<=first<=last<=len(lines),('source range out of bounds',path,first,last)
        assert sha(b''.join(lines[first-1:last]))==target,('source range hash mismatch',path,first,last)
        range_count+=1;unique_ranges.add((path,first,last,target))

def records(v):
    if isinstance(v,dict):
        if isinstance(v.get('path'),str) and v['path'].startswith('src/') and any(k in v for k in ['sha256','file_sha256','source_full_file_sha256']):yield v
        for x in v.values():yield from records(x)
    elif isinstance(v,list):
        for x in v:yield from records(x)

for r in now['source_files']:check_source(r)
for c in now['claims']:
    for r in c['sources']:check_source(r)
auditdir=ROOT/'dependency_audit_v0_30'
for p in sorted(auditdir.glob('*.json')):
    for r in records(read(p)):check_source(r)

previous_targets=read(OLD/'next_source_targets.json')['targets']
targets=read(ROOT/'next_source_targets.json')['targets']
disp=read(auditdir/'target_disposition.json')
assert len(previous_targets)==len(targets)==len(disp['records'])==245
for i,(oldtarget,target,rec) in enumerate(zip(previous_targets,targets,disp['records']),1):
    for k,v in oldtarget.items():assert target[k]==v,('changed inherited target',i,k)
    assert rec['original_index_one_based']==i
    assert rec['original_record_sha256']==sha(json.dumps(oldtarget,sort_keys=True,ensure_ascii=False,separators=(',',':')).encode())
    assert target['version_0_30_disposition']==rec
    check_source(oldtarget)
categories=dict(collections.Counter(r['primary_category'] for r in disp['records']))
assert categories=={'A':3,'B':10,'C':118,'D':114},categories
assert len(disp['scope_groups'])==107
assert len({r['id'] for r in disp['records']})==245
registry=read(auditdir/'published_applications.json')
assert len(registry['freshly_checked_applications'])==8
assert len(registry['inherited_registries'])==22
assert sum(r['entry_count'] for r in registry['inherited_registries'])==101

selected=read(auditdir/'obligation_map.json')
assert selected.get('source_commit',selected.get('commit'))==PIN
selected_nodes={n['id']:n for n in selected['nodes']}
assert len(selected_nodes)==len(selected['nodes'])
selected_active=set();selected_done=set()
def selected_visit(k):
    assert k in selected_nodes,('missing selected node',k)
    assert k not in selected_active,('selected graph cycle',k)
    if k in selected_done:return
    selected_active.add(k)
    node=selected_nodes[k]
    assert node['category'] in ['A','B','C','D']
    assert node['gate'] in ['AND','LEAF']
    if node['gate']=='LEAF':assert not node['requires']
    for dep in node['requires']:selected_visit(dep)
    selected_active.remove(k);selected_done.add(k)
for root in selected['roots']:selected_visit(root)
assert selected_done==set(selected_nodes),'Detached selected logical nodes'
def reachable(root):
    seen=set();todo=[root]
    while todo:
        k=todo.pop()
        if k in seen:continue
        seen.add(k);todo+=selected_nodes[k]['requires']
    return seen
rh=reachable('ORDINARY_RH');grh=reachable('DIRICHLET_GRH')
case3={'COUNT_III_PRODUCER','COUNT_III_GENERAL','CASE3_PROMOD','SEED_IV_ALT',
       'TENSOR_FACTOR_TOWER','CHAIN_RANK_FOUR','CHAIN_DESC4','RANK4_CHAIN_REDUCTION'}
assert not case3.intersection(rh)
assert case3<=grh
assert {'COUNT_I_PRODUCER','COUNT_II_SUPPORT','COUNT_V_PRODUCER'}<=rh&grh
assert not {n['id'] for n in selected['optional_routes']}.intersection(selected_nodes)
assert selected['selected_interface_cuts']['common_family']['source_argument_count']==10
assert len(selected['selected_interface_cuts']['common_family']['ten_contracts'])==10
for name,entry in selected['source_inputs'].items():
    p=Path(entry['file']);assert not p.is_absolute(),('nonportable graph input',name)
    assert filehash(ROOT/p)==entry['sha256'],('graph input hash',name)
assert (ROOT/'reviews_v0_30/connected_graph_review.json').is_file(),'Missing independent selected-graph review'
tex=read(ROOT/'tex_validation.json')
assert tex['syntax_compile_succeeded'] and not tex['undefined_references_or_citations']
assert not tex['pdf_generated']
assert tex['tex_sha256']==filehash(ROOT/'RH_readable_reconstruction_v0_30.tex')
assert (ROOT/'RH_dependency_audit_v0_30.txt').is_file()

result=dict(artifact_version='0.30',result='PASS',source_commit=PIN,
    predecessor_claims_preserved=len(oldclaims),new_claims=len(newclaims),claims=len(claims),
    predecessor_manifest_files_preserved=prior_files,predecessor_files_resolved_through_archive=archived_files,
    original_claim_fields_preserved=True,original_source_arrays_preserved=True,original_claim_edges_preserved=True,
    new_proof_ranges_checked=len(newclaims),reviewed_component_hashes=expected_reviewed,
    indexed_source_files=len(now['source_files']),distinct_source_files_checked=len(source_cache),
    claim_source_ranges=sum(len(c['sources']) for c in now['claims']),
    source_range_records_checked_including_audit=range_count,unique_source_ranges_checked=len(unique_ranges),
    inherited_targets_preserved_and_dispositioned=245,scope_groups=107,backlog_primary_categories=categories,
    freshly_checked_published_applications=8,inherited_registry_entries=101,inherited_registry_files=22,
    claim_graph_acyclic=True,selected_graph='dependency_audit_v0_30/obligation_map.json',
    independently_checked_selected_nodes=len(selected_nodes),all_selected_nodes_root_reachable=True,
    rh_reachable_nodes=len(rh),dirichlet_grh_reachable_nodes=len(grh),
    rh_excludes_case_III_and_grh_includes_it=True,selected_graph_inputs_hash_checked=True,
    selected_graph_sha256=filehash(auditdir/'obligation_map.json'),
    selected_graph_validation=selected.get('validation'),
    independent_graph_review_file='reviews_v0_30/connected_graph_review.json',
    independent_graph_review_sha256=filehash(ROOT/'reviews_v0_30/connected_graph_review.json'),
    tex_validation=tex,lean_build=False,kernel_replay=False,
    scope='Checks source/proof provenance, continuity, audit coverage and TeX syntax. Mathematical review is recorded separately; formal correctness is an accepted premise, not reverified here.')
write(ROOT/'validation_v0_30.json',result)
cp=read(ROOT/'continuation_checkpoint.json');cp['validation']=result;write(ROOT/'continuation_checkpoint.json',cp)
print(json.dumps({k:v for k,v in result.items() if k not in ['reviewed_component_hashes','selected_graph_validation','tex_validation','scope']},indent=2))
