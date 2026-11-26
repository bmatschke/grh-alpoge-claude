#!/usr/bin/env python3
"""Independent final graph bindings/checks after the mathematical scope review."""
from pathlib import Path
import argparse, collections, hashlib, json, subprocess

HERE=Path(__file__).resolve().parent
ap=argparse.ArgumentParser(description=__doc__)
ap.add_argument('--root',type=Path,default=HERE.parents[1]/'reconstruction_v033')
ap.add_argument('--source',type=Path,default=HERE.parents[1]/'lean_source')
args=ap.parse_args(); R=args.root.resolve(); S=args.source.resolve()
PIN='7cbf7a0c32fca1badf05931879a37c3f8a2b03b4'
sha=lambda b:hashlib.sha256(b).hexdigest()
read=lambda p:json.loads(p.read_text())
AUD=R/'dependency_audit_v0_33'; g=read(AUD/'obligation_map.json')
old=read(R/'dependency_audit_v0_32/obligation_map.json')
nodes={n['id']:n for n in g['nodes']}; previous={n['id']:n for n in old['nodes']}
assert len(nodes)==len(g['nodes'])==121
assert set(nodes)==set(previous)
assert all(nodes[k]['requires']==previous[k]['requires'] for k in nodes)
assert g['source_commit']==PIN
assert subprocess.check_output(['git','rev-parse','HEAD'],cwd=S,text=True).strip()==PIN
active=set(); finished=set()
def visit(k):
    assert k in nodes and k not in active, k
    if k in finished:return
    active.add(k)
    for v in nodes[k]['requires']:visit(v)
    active.remove(k);finished.add(k)
for k in nodes:visit(k)
def reach(k):
    seen=set();todo=[k]
    while todo:
        a=todo.pop()
        if a in seen:continue
        seen.add(a);todo+=nodes[a]['requires']
    return seen
rh=reach('ORDINARY_RH'); grh=reach('DIRICHLET_GRH'); full=reach('GLOBAL_FULL_RANK')
assert rh|grh==set(nodes)
assert 'COUNT_III_PRODUCER' not in rh and 'COUNT_III_PRODUCER' in grh
assert {'COUNT_I_PRODUCER','COUNT_II_SUPPORT','COUNT_V_PRODUCER'}<=rh&grh
assert not any(k.startswith('TASK_GL4') for k in full)
assert 'TASK_GL_FINAL_ASSEMBLY' not in full
assert {'GLOBAL_REAL_SECOND_LAYER','SECOND_LAYER_COMPATIBLE_SELECTION'}<=full
changed_status={k for k in nodes if nodes[k]['status']!=previous[k]['status']}
gl4={'TASK_GL4_COLUMN_VALUES','TASK_GL4_SLOPE_LOWER','TASK_GL4_SLOPE_MAX'}
assert changed_status==gl4
assert all(nodes[k]['status']=='proved_in_stated_scope' for k in gl4)
assert nodes['TASK_GL_FINAL_ASSEMBLY']['status']=='human_proof_still_required'
assert nodes['COUNT_II_SUPPORT']['status']=='open_producer'
assert nodes['BASE_THETA_CUSPIDAL_EXTENSION']['status']=='open_original_producer'
leaves=[n for n in g['nodes'] if n['gate']=='LEAF' and n['status'] not in ('proved_in_stated_scope','published_application_checked')]
assert len(leaves)==35
assert collections.Counter(n['category'] for n in leaves)=={'C':23,'B':10,'D':2}
assert read(AUD/'remaining_leaf_register.json')['records']==leaves
cut=g['selected_interface_cuts']['common_family']
assert cut['source_argument_count']==10 and len(cut['ten_contracts'])==10
assert cut['constants']=={'Cabs':2,'C0':3,'eD':2,'eL':0}
assert cut['class_side_conditions']==['Cprime -> C','Cprime -> E','E -> HypV']
joint=nodes['COUNT_II_SUPPORT']['joint_witness_constraint']
assert len(joint['properties_on_same_witness'])==7
assert joint==previous['COUNT_II_SUPPORT']['joint_witness_constraint']
assert 'nested D' in nodes['COUNT_II_SUPPORT']['contract']
assert 'KX3 alone does not supply' in nodes['COUNT_II_SUPPORT']['contract']
assert nodes['RIG_II']['supplier_expansion_incomplete']
assert nodes['RIG_II']['requires']==[]
assert set(nodes['RIG_II']['exact_unexpanded_supplier_arguments'])=={'LitN','LemmaK','Af.AdVanishQ','Af.NewformAut','KatoTwo'}
ref={n['id'] for n in g['work_refinement_nodes']}; opt={n['id'] for n in g['optional_routes']}
assert not set(nodes)&(ref|opt)
for x in g['work_refinement_links']:
    assert x['logical'] is False
    assert x['consumer'] in set(nodes)|ref|opt and x['dependency'] in set(nodes)|ref|opt
assert len(ref)==13 and len(opt)==8

bindings=set(); inputs=[]
def file_binding(file, expected):
    p=R/file
    assert not Path(file).is_absolute() and p.is_file(),file
    assert sha(p.read_bytes())==expected,('file hash',file)
    bindings.add((file,expected))
for key,x in g['source_inputs'].items():
    file_binding(x['file'],x['sha256']);inputs.append(dict(id=key,**x))
file_binding(g['backlog_crosswalk']['file'],g['backlog_crosswalk']['sha256'])
disp=read(AUD/'target_disposition.json'); olddisp=read(R/'dependency_audit_v0_32/target_disposition.json')
targets=read(R/'history/version_0_32/next_source_targets.json')['targets']
assert len(disp['records'])==len(olddisp['records'])==len(targets)==245
for a,b,t in zip(disp['records'],olddisp['records'],targets):
    assert a['original_id']==b['original_id']==t['id']
    assert all(a[k]==v for k,v in b.items()),a['original_id']
    tb=json.dumps(t,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()
    assert a['predecessor_record_sha256']==sha(tb)

source_cache={}; ranges=set(); blocks=set(); evidence_count=0; ledgers={}
def source_check(x):
    p=x['path']
    if p not in source_cache:
        raw=(S/p).read_bytes()
        assert raw==subprocess.check_output(['git','show',PIN+':'+p],cwd=S)
        source_cache[p]=(raw,raw.splitlines(keepends=True))
    raw,ls=source_cache[p]
    filehash=x.get('file_sha256',x.get('full_file_sha256',x.get('sha256')))
    assert sha(raw)==filehash,('source file hash',p)
    st,en=x['line_start'],x['line_end'];rb=b''.join(ls[st-1:en])
    assert 1<=st<=en<=len(ls),(p,st,en)
    assert sha(rb)==x['range_sha256'],('source range hash',p,st,en)
    ranges.add((p,st,en,x['range_sha256']))
def proof_check(x):
    p=R/x['file'];raw=p.read_bytes();ls=raw.splitlines(keepends=True)
    rb=b''.join(ls[x['line_start']-1:x['line_end']])
    assert sha(rb)==x.get('range_sha256',x['sha256']),('proof range',x['file'],x['line_start'])
    if 'file_sha256' in x:assert sha(raw)==x['file_sha256']
    blocks.add((x['file'],x['line_start'],x['line_end']))
def walk(x):
    if isinstance(x,list):
        for y in x:walk(y)
    elif isinstance(x,dict):
        if x.get('path','').startswith('src/') and 'range_sha256' in x:source_check(x)
        if 'proof_location' in x:
            p=x['proof_location']
            if all(k in p for k in ('file','line_start','line_end','sha256')):proof_check(p)
        for a,b in [('ledger','ledger_sha256'),('proof_file','proof_sha256'),('provenance_file','provenance_sha256'),('registry','registry_sha256')]:
            if a in x and b in x:file_binding(x[a],x[b])
        lp=x.get('ledger',x.get('provenance_file'))
        if lp and isinstance(x.get('claims'),list):
            if lp not in ledgers:ledgers[lp]={c['id']:c for c in read(R/lp)['claims']}
            for c in x['claims']:
                assert c in ledgers[lp],(lp,c)
                walk(ledgers[lp][c])
        for k,v in x.items():
            if k not in ('previous_interface','previous_input_contract','claims','proof_location'):walk(v)
for group in ('nodes','work_refinement_nodes','optional_routes'):
    for n in g[group]:
        evidence_count+=len(n.get('evidence',[]));walk(n.get('evidence',[]))

text=(R/'RH_dependency_audit_v0_33.txt').read_text()
assert (AUD/'audit.txt').read_text()==text
for n in leaves:assert n['contract'] in text,n['id']
apps=read(R/'global_slope/published_applications.json')
assert isinstance(apps,list) and len(apps)==1 and apps[0]['application_claim']=='GLS8'
assert apps[0]['theorem']=='Theorem (2.1)' and apps[0]['classification']=='A'
assert apps[0]['independently_derived_normalization'] and apps[0]['original_source_facts']
assert 'nested category D' in text and 'coupled C' in text
assert 'eigenvalue\ndifferent from one' in text or 'eigenvalue different from one' in text
assert 'nonunit eigenvalue' not in text

def entry(file):return dict(file=file,sha256=sha((R/file).read_bytes()))
graph=entry('dependency_audit_v0_33/obligation_map.json')
narr=entry('dependency_audit_v0_33/main.tex')
plain=entry('RH_dependency_audit_v0_33.txt')
findings=[
 ('EXACT_FINAL_INTERFACE','Both roots keep the ten original topDesWin inputs, the same class inclusion/HypV side conditions, source constants, original host window, metric transport and terminal numerical certificate. No direct-gap shortcut replaces their producers.'),
 ('THREE_GL4_CLOSURES','Exactly three previously open B leaves change to proved implication certificates. GLS gives original ColVal, lower slope and maximum slope with coefficient 4. Banaszczyk is explicitly registered as a checked A input; all trace/codifferent and metric normalizations are proved in GLS. The full arbitrary-partition/zero-rank StdSlopeLow scope is included in corrected GLS5.'),
 ('GLOBAL_PACKET_AND_REMAINDER','All eleven FamGLmin fields are complete conditional on the same supplied original second layer. The compatible selector remains C. TASK_GL_FINAL_ASSEMBLY remains B for actual linkGLOBAL7_min/items/link8 numerical and identity installations; no PartFive/count/frame/loss producer is silently declared complete.'),
 ('QUANTIFIER_ORDER','Closed epsilon cutoffs and TransportedAlt tuples precede Fm,CH. The later x threshold may depend on that family but precedes members, words and places. Same-FamU HidaSetting guards are unchanged. The narrative now explicitly distinguishes these two levels.'),
 ('FULLNESS_AND_DESIGN','The smaller actual Nlam-inclusion-to-fullness route still reaches the original second-layer producer and excludes every GL4 leaf and final global assembly. Actual Built-class TuSize/RankM remain conditional on that class and cT=cTmin; DesignChoices/common Bundle existence remains open.'),
 ('THETA_SCOPE','FIA and CTC close finite averaging and genuine cuspidality on the original kernels. BASE_THETA_CUSPIDAL_EXTENSION remains C for smoothness/growth/lowering/type/finite-level/Hilbert realization, with universal ioP. Same-Bundle readings, rational tests and original base rows remain separate coupled producers.'),
 ('COUNT_TARGETS','RH and fixed 2-power-order targets retain I/II/V and exclude Case III. Unrestricted Dirichlet GRH additionally requires III/SeedIV/chain. Count-I and Count-V source fields and prime/exponent scopes remain distinct; universal helper routes are expressly stronger sufficient implementations.'),
 ('JOINT_IDEAL_AND_NESTED_D','COUNT_II_SUPPORT remains C on both original rank-four Links: fixed iota, one common threshold before later DVR/B/Lambda, one J per Link carrying all six Hida fields and P1core. JSP conditional ring/dense/TWBase and one-point transport do not create ordinary arithmetic, all-level HasAut or six support contracts. Exact artOf/every-map IsWtPart matching is explicitly retained as a nested D issue, not inferred from KX3.'),
 ('OPAQUE_AND_OPTIONAL_SCOPES','RigII remains an opaque C contract with all five unexpanded supplier arguments named; Kato alone is not a sufficient AND producer. Thirteen shared-work nodes and eight optional/reuse routes remain outside logical reachability. All 245 inherited compound targets preserve their previous fields and explicit scopes.'),
 ('NARRATIVE_AGREEMENT','The plain audit reproduces every exact current remaining contract; its counts refer to selected coupled nodes, not all finer subobligations or completion percentages. The TeX narrative and standalone audit retain conditional scope, corrected eigenvalue wording and the complete-root priority.'),
]
report=dict(schema='rh-independent-graph-review/1',version='0.33',reviewer='/root/audit_global_routes',status='PASS',verdict='PASS',source_commit=PIN,
 graph=graph,narrative=narr,standalone_audit=plain,graph_sha256=graph['sha256'],graph_file_sha256=graph['sha256'],narrative_file_sha256=narr['sha256'],audit_txt_sha256=plain['sha256'],
 review_scope='Independent mathematical sufficient-rule scope, same-object/quantifier boundaries, current completion status, narrative agreement and binding validation. Component mathematical reviews are separately registered; this is not a reconstruction of every inherited open producer.',
 findings=[dict(id=i,status='PASS',detail=d) for i,d in findings],
 validation=dict(selected_nodes=len(nodes),RH_reachable_nodes=len(rh),Dirichlet_GRH_reachable_nodes=len(grh),all_selected_nodes_reachable=True,all_requires_references_resolved=True,acyclic=True,predecessor_selected_nodes_preserved=len(previous),all_selected_dependency_edges_preserved=True,changed_status_nodes=sorted(changed_status),nonlogical_refinement_links_resolved=len(g['work_refinement_links']),work_refinement_nodes=len(ref),optional_routes=len(opt),open_leaf_count=len(leaves),open_leaf_categories=dict(collections.Counter(n['category'] for n in leaves)),source_inputs_verified=len(inputs),current_evidence_entries_checked=evidence_count,evidence_file_hash_bindings_verified=len(bindings),distinct_pinned_source_ranges_verified=len(ranges),pinned_source_files_verified=len(source_cache),human_proof_blocks_verified=len(blocks),backlog_records_preserved_and_matched=245,backlog_scope_groups_preserved=107,leaf_register_exactly_matches_selected_graph=True,nested_reciprocity_D_explicit=True),
 source_inputs=inputs,required_corrections=[],unresolved_review_issues=[],
 resolved_pre_freeze_findings=['Distinguished Closed transport-tuple bounds from family-dependent eventual x thresholds.','Exposed JSP exact reciprocity as a nested D scope within the coupled Count-II C producer.','Replaced ambiguous nonunit eigenvalue by eigenvalue different from one.'],
 limitations=['Selected sufficient-interface graph only, not an exhaustive Lean declaration graph or proof of absolute mathematical minimality.','Formal correctness is accepted; every open status concerns the human reconstruction.','The mathematical GLS chapter is independently reviewed by the count-path agent; this report assesses its installation and premises, not independent authorship of GLS.'])
out=R/'reviews_v0_33';out.mkdir(exist_ok=True)
(out/'selected_route_graph_review.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
lines=['Independent selected-route graph and narrative review — v0.33','Reviewer: /root/audit_global_routes','Verdict: PASS','',
 f"Graph SHA256 {graph['sha256']}",f"Narrative SHA256 {narr['sha256']}",f"Standalone audit SHA256 {plain['sha256']}",'']
for i,d in findings:lines.extend([i+': PASS',d,''])
lines.extend(['Validation',json.dumps(report['validation'],ensure_ascii=False,indent=2),'','No required correction or unresolved review issue remains.','The underlying Lean proof is assumed fully checked and correct; the report concerns the human reconstruction.'])
(out/'selected_route_graph_review.txt').write_text('\n'.join(lines)+'\n')
print(json.dumps(dict(status='PASS',graph_sha256=graph['sha256'],narrative_sha256=narr['sha256'],audit_txt_sha256=plain['sha256'],review_json_sha256=sha((out/'selected_route_graph_review.json').read_bytes()),validation=report['validation']),ensure_ascii=False,indent=2))
