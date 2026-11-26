#!/usr/bin/env python3
"""Merge the v0.13 mathematical ledgers without changing earlier claims."""
from pathlib import Path
import copy, hashlib, json, subprocess

ROOT=Path(__file__).resolve().parent
OLD=ROOT/'history/version_0_12'
REPO=ROOT.parent/'lean-source'
COMMIT='7cbf7a0c32fca1badf05931879a37c3f8a2b03b4'
URL='https://github.com/CocoSgt/riemann-hypothesis-lean'
COMPONENTS=['global_frame','class_rank','comparison_span','lattice_patching']
def read(p):return json.loads(p.read_text())
def write(p,o):p.write_text(json.dumps(o,ensure_ascii=False,indent=2)+'\n')
def digest(b):return hashlib.sha256(b).hexdigest()
prior=read(OLD/'provenance.json')
result=copy.deepcopy(prior)
result.update(artifact_version='0.13',date='2026-11-21',predecessor_version='0.12')
result['scope']='Partial human RH/Dirichlet-GRH reconstruction. The common global-frame/companion algebra, actual class-rank equality and exact integral comparison span are proved under the literal supplied compatible forms/value data; selected served/type-prime lattice patching and conditional normalized-length installation are also proved. Simultaneous standard forms/value/model construction, full refill/point/NumAt, host/field/analytic supply and the independent spectral, metric, cohomological and prime-window branches remain.'
new=[]
files={f['path']:copy.deepcopy(f) for f in prior['source_files']}
graph=copy.deepcopy(prior['mathematical_dependency_graph'])
component_scope={}
for component in COMPONENTS:
    j=read(ROOT/component/'provenance.json')
    component_scope[component]={k:v for k,v in j.items() if k not in ['claims','files','source_files']}
    for c0 in j['claims']:
        c=copy.deepcopy(c0)
        c['introduced_in']='0.13'
        c['component_ledger']=component+'/provenance.json'
        c['depends_on']=c.get('depends_on',c.get('dependencies',[]))
        for k in ['proof_location','expanded_notes']:
            if isinstance(c.get(k),dict):
                for f in ['file','expanded']:
                    if isinstance(c[k].get(f),str) and '/' not in c[k][f]:c[k][f]=component+'/'+c[k][f]
        if 'proof_location' not in c:c['proof_location']={'file':component+'/main.tex','expanded':component+'/report.txt','section':c['id']}
        new.append(c);graph[c['id']]=list(c['depends_on'])
    for f in j.get('source_files',j.get('files',[])):
        if f['path'] in files:assert f['sha256']==files[f['path']]['sha256'],f['path']
        else:
            f=copy.deepcopy(f)
            if 'line_count' in f and 'lines' not in f:f['lines']=f['line_count']
            f.setdefault('url',f"{URL}/blob/{COMMIT}/{f['path']}")
            files[f['path']]=f
result['claims'].extend(new)
ids={c['id']for c in result['claims']}
assert len(ids)==len(result['claims'])
for cid,deps in graph.items():assert set(deps)<=ids,(cid,set(deps)-ids)
updates={
 'LI5':(['SF1','SF5','SF6','SF7'],'Independent local frames are now replaced by base changes of a common global frame, under the exact standard-column/carrier premises.'),
 'LI8':(['SF7','CR6','CS9'],'The common-frame algebra, actual rank equality and integral comparison span are now proved under the supplied compatible forms/value construction. Joint0 and character rationality retain their stated uses; global model supply remains.'),
 'PL13':(['LP3','LP4','LP5'],'The actual exists_lat -> setLat route is proved for the supplied local predicates, including exact localizations and normalized lengths. The full refill and geometric RecOK/LedOK/point construction remain.'),
 'PL16':(['CR1','CR2','CR3','CR4','CR5','CR6'],'Weyl fiber ranks, actual class correspondence and stabilizer triviality now give the literal class-rank equality. This does not prove metric or automorphic model existence.'),
 'BC8':(['SF7','CR6','CS9'],'The former global frame/rank/comparison-algebra boundary is narrowed to the simultaneous compatible forms/value/model supply. Local coefficient-ring conclusions and all earlier parameter restrictions are unchanged.')
}
for c in result['claims']:
    if c['id']in updates:
        proved,note=updates[c['id']]
        c['version_0_13_update']={'discharged_by':proved,'scope':note}
result['mathematical_dependency_graph']=graph
visited=set();active=set();order=[]
def visit(k):
    if k in visited:return
    assert k not in active,('dependency cycle',k)
    active.add(k)
    for d in graph[k]:visit(d)
    active.remove(k);visited.add(k);order.append(k)
for k in graph:visit(k)
result['dependency_topological_order']=order
result['source_files']=sorted(files.values(),key=lambda f:f['path'])
result.setdefault('merge_inputs_history',[]).append(copy.deepcopy(prior.get('merge_inputs',{})))
result['merge_inputs']={c:{'ledger':c+'/provenance.json','sha256':digest((ROOT/c/'provenance.json').read_bytes())}for c in COMPONENTS}
result['new_component_ledgers']=[c+'/provenance.json'for c in COMPONENTS]
result['version_0_13_local_conclusions']={
 'common_frame':'SF1-SF7: common B, actual positive coordinates, diagonal companion and simultaneous local frame replacement under the supplied standard forms/carriers.',
 'rank':'CR1-CR6: literal locPack_d_eq/pack_d_eq; Joint0 is unused in this equality; Delta and nabla not identified integrally.',
 'integral_comparison':'CS1-CS9: ValIntRec and exact O-span(cmp(global lattice))=M under the same supplied compatible forms, ValEx, Joint0 and coefficient-field character data.',
 'patching':'LP1-LP5: exact finite-place patch for supplied served/type-prime predicates; conditional setLat length installation.',
 'remaining':'Simultaneous standard forms/value/model existence; full refill, point and NumAt supply; host/field/analytic suppliers; independent spectral, metric, cohomological and prime-window branches.'}
result.setdefault('component_scope_metadata_as_received',{}).update(component_scope)
result['component_input_boundaries'].update({c:component_scope[c].get('retained_inputs',component_scope[c].get('input_boundaries',[]))for c in COMPONENTS})
result['validation']={'previous_claims_preserved':len(prior['claims']),'new_claims':len(new),'claim_count':len(ids),
 'source_link_count':sum(len(c['sources'])for c in result['claims']),'source_file_count':len(files),'dependency_graph_acyclic':True,
 'dependency_graph_is_lean_transitive_audit':False,'lean_build':False,'kernel_replay':False}
write(ROOT/'provenance.json',result)
write(ROOT/'source_index.json',{'commit':COMMIT,'artifact_version':'0.13','source_files':result['source_files']})
for c0,c in zip(prior['claims'],result['claims']):
    assert all(c[k]==v for k,v in c0.items()),c0['id']
for k in ['version_0_10_local_conclusions','version_0_11_local_conclusions','version_0_12_local_conclusions']:
    assert result[k]==prior[k]

txt=['RH / DIRICHLET-GRH RECONSTRUCTION v0.13 -- CLAIM AND SOURCE LEDGER',
     'Pinned source '+COMMIT,'All v0.12 claim fields/source arrays are preserved; v0.13 annotations are additive.','']
for c in result['claims']:
    txt += [c['id']+' -- '+c['title'],'Status: '+c['status']]
    for field in ['statement','assumptions','depends_on','dependencies','proof_location','version_0_13_update']:
        if field in c:txt.append(field+': '+(c[field]if isinstance(c[field],str)else json.dumps(c[field],ensure_ascii=False)))
    for i,f in enumerate(c['sources'],1):
        txt += [f"  {i}. {f['declaration']}",f"     {f['path']}:{f['line_start']}-{f['line_end']}",
                '     '+f['url'],'     File SHA256 '+f['sha256'],'     Range SHA256 '+f['range_sha256']]
    txt += ['']
(ROOT/'provenance.txt').write_text('\n'.join(txt)+'\n')

nt=read(OLD/'next_source_targets.json')
old_targets=nt['targets']
nt['version']='0.13'
nt['completed_previous_frontier']='Common-frame and actual companion algebra, actual class-rank equality and exact integral comparison span are proved under the literal supplied compatible data; selected local lattice patching/installation is proved under its exact local conditions.'
nt['next_local_priority']='Construct the simultaneous standard global forms and polynomial values supplying the proved comparison; complete canonical refill/point/NumAt and underlying host arithmetic supply.'
nt['priority_groups']['1']='Simultaneous global standard forms, carrier and polynomial-value construction.'
targets=[copy.deepcopy(t)for t in old_targets if t['priority_group']!=1]
new_targets=[]
for component in COMPONENTS[:3]:
    for t0 in read(ROOT/component/'next_targets.json')['targets']:
        t=copy.deepcopy(t0);t['priority_group']=1
        t['human_status']='continuation_target_only; no new proof asserted by this target record'
        t.setdefault('remaining_human_scope',t.get('remaining_scope',t.get('role','Construct the simultaneous compatible global forms/value data.')))
        new_targets.append(t)
refill=next(s for c in new if c['id']=='LP5'for s in c['sources']if s.get('role')=='remaining_input')
refill=copy.deepcopy(refill);refill.update(priority_group=2,remaining_human_scope='Supply the complete canonical refill, including finite support and gain/error/deficit identities, from its literal size and untwisted hypotheses; LP supplies only the following lattice patch and length installation.',human_status='continuation_target_only')
new_targets.append(refill)
seen=set();dedup=[]
for t in new_targets+targets:
    key=(t['path'],t['declaration'].split('.')[-1],t['line_start'],t['line_end'])
    if key in seen:continue
    seen.add(key)
    if t['path'].endswith('/ExistsLedPart.lean'):
        t['remaining_human_scope']='LP1-LP5 prove exists_lat and setLat/length installation. Supply the complete canonical refill and exact RecOK/LedOK/Lay hypotheses, then finish the literal LedPart assembly without changing the selected local predicates.'
    dedup.append(t)
nt['targets']=dedup
nt['target_count']=len(dedup)
nt['priority_group_counts']={str(i):sum(t['priority_group']==i for t in dedup)for i in range(1,5)}
nt['removed_completed_targets'] += [t['path']+':'+t['declaration'] for t in old_targets if t['priority_group']==1]
nt['previous_version_precision_notes']=copy.deepcopy(nt['precision_notes'])
nt['precision_notes'] = [
 'Every reconstructed statement keeps its literal hypotheses. Completed conditional joins do not construct HostAx, ShortNorm, SmallOne, ThinH, PairEx or VWinAt.',
 'The biased TT set and separate integer shift set T2 are already constructed; this continuation does not reopen their probability/counting proofs.',
 'The active family-degree route remains HostWW/KitS/ChosenWall. CoverAll and IsRecCEv are optional interfaces, not imposed on the active route.',
 'Keep the same embRec, original orbit representatives, c^s parity and p-normalized valuations throughout all global/local comparisons.',
 'SF proves actual companion identities from supplied carriers; it does not construct all standard forms/values or justify them for unrelated hosts.',
 'CR compares dimensions via Delta Weyl fibers and the same class count. Delta is not identified with nabla as an integer lattice; Joint0 is unused only for rank.',
 'CS proves exact integral span. The rational-forms bridge uses emb_basis and Fi_zero in addition to CR6. Joint0 supplies SameUloc; SameUloc is not a separate open target under that premise.',
 'LP patches the actual retained Mram reference. Local-unit saturation does not imply primitive/global saturation, and type-prime local targets may enlarge Mram.',
 'LP does not complete exists_refill, all RecExP/ObjCP or the stronger NumAt parameter record.'
]
target_files={}
for t in dedup:
    raw=(REPO/t['path']).read_bytes();assert digest(raw)==t['sha256'],t['path']
    assert digest(b''.join(raw.splitlines(keepends=True)[t['line_start']-1:t['line_end']]))==t['range_sha256']
    target_files[t['path']]={'path':t['path'],'sha256':digest(raw),'bytes':len(raw),'lines':len(raw.splitlines()),'url':f"{URL}/blob/{COMMIT}/{t['path']}"}
nt['source_files']=list(target_files.values());nt['source_file_count']=len(target_files)
nt['validation']={'all_target_file_and_range_hashes_verified':True,'target_count':len(dedup),'global_branches_preserved':nt['global_branches_unchanged']==read(OLD/'next_source_targets.json')['global_branches_unchanged']}
write(ROOT/'next_source_targets.json',nt)
print(json.dumps(result['validation']))
print(json.dumps({'next_targets':len(dedup),'target_groups':nt['priority_group_counts']}))
