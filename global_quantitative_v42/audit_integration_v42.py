#!/usr/bin/env python3
"""Independent read-only audit of the v0.42 integration against the frozen v0.41 baseline."""
import argparse
import collections
import hashlib
import json
from pathlib import Path
import re
import subprocess

ROOT=Path(__file__).resolve().parents[1]
OLD=ROOT/'history/version_0_41'
PIN='7cbf7a0c32fca1badf05931879a37c3f8a2b03b4'
ap=argparse.ArgumentParser()
ap.add_argument('--source',type=Path,required=True)
ap.add_argument('--output',type=Path,default=ROOT/'reviews_v0_42/integration_global_estimates.json')
args=ap.parse_args(); source=args.source.resolve()
sha=lambda b:hashlib.sha256(b).hexdigest()
read=lambda p:json.loads(p.read_text())
errors=[]; checks=[]; bindings={}

def require(condition,label,detail=None):
    if condition:
        checks.append(label)
    else:
        errors.append(dict(check=label,detail=detail))

def bind(path):
    raw=path.read_bytes();bindings[str(path.relative_to(ROOT))]=sha(raw)
    return json.loads(raw)

def acyclic(graph):
    done,active=set(),set()
    def go(n):
        if n in active: raise AssertionError(('cycle',n))
        if n not in graph: raise AssertionError(('unknown node',n))
        if n in done:return
        active.add(n)
        for d in graph[n]:go(d)
        active.remove(n);done.add(n)
    for n in graph:go(n)
    return len(done)

require(subprocess.check_output(['git','-C',str(source),'rev-parse','HEAD'],text=True).strip()==PIN,'exact source pin')
cfg=bind(ROOT/'increment_v0_42.json')
old=bind(OLD/'provenance.json'); now=bind(ROOT/'provenance.json')
old_index=bind(OLD/'source_index.json'); index=bind(ROOT/'source_index.json')
baseclaims=old['claims']; claims=now['claims']; count=len(baseclaims)
require(count==2209,'baseline has 2209 claims',count)
require(claims[:count]==baseclaims,'all baseline claim records, source arrays, proof metadata and scope fields preserved exactly')
require(now['source_files'][:len(old['source_files'])]==old['source_files'],'baseline provenance source inventory preserved exactly')
require(index['source_files'][:len(old_index['source_files'])]==old_index['source_files'],'baseline source index preserved exactly')
old_manifest=OLD/'SHA256SUMS'; preserved_artifacts=0;historically_archived=0
if old_manifest.is_file():
    for line in old_manifest.read_text().splitlines():
        if not line.strip():continue
        expected,rel=line.split('  ',1);current=ROOT/rel; archived=OLD/rel
        if current.is_file() and sha(current.read_bytes())==expected:
            preserved_artifacts+=1
        elif archived.is_file() and sha(archived.read_bytes())==expected:
            preserved_artifacts+=1;historically_archived+=1
        else:
            errors.append(dict(check='baseline artifact preserved',detail=rel))
    require(preserved_artifacts==len([x for x in old_manifest.read_text().splitlines() if x.strip()]),'every baseline manifest artifact survives at original bytes in current tree or history')
ids=[c['id'] for c in claims]; byid={c['id']:c for c in claims}
require(len(ids)==len(set(ids)),'claim IDs unique')
graph=now['mathematical_dependency_graph']
require(all(graph.get(k)==v for k,v in old['mathematical_dependency_graph'].items()),'all baseline mathematical dependency edges preserved exactly')
require(set(graph)==set(ids),'claim graph has exactly the ledger claim IDs')
try: require(acyclic(graph)==len(claims),'complete mathematical claim graph is acyclic')
except AssertionError as e:require(False,'complete mathematical claim graph is acyclic',str(e))
order=now.get('dependency_topological_order',[]);pos={k:i for i,k in enumerate(order)}
require(set(order)==set(ids) and len(order)==len(ids),'topological order covers all claims once')
require(all(pos.get(d,len(ids))<pos.get(n,-1) for n,ds in graph.items() for d in ds),'topological order respects every recorded edge')
for claim,dep in [('HSR3','NR19'),('OST23','OST22'),('OST25','OST24'),('RRT6','RRT4')]:
    require(dep in graph.get(claim,[]),f'explicit reviewed proof dependency {claim} -> {dep} is recorded')

incoming=[]; component_bindings={}
for component in cfg['components']:
    ledger=bind(ROOT/component/'provenance.json')
    incoming.extend(ledger['claims'])
    component_bindings[component]=dict(claims=len(ledger['claims']),ledger_sha256=bindings[component+'/provenance.json'])
require([c['id'] for c in claims[count:]]==[c['id'] for c in incoming],'new claim inventory and order equal the configured component ledgers')
source_bytes={};source_ranges=set();new_proof_files={}
for c in incoming:
    integrated=byid.get(c['id'],{})
    require(integrated.get('depends_on',[])==c.get('depends_on',[])==graph.get(c['id']),f'{c["id"]}: dependencies imported literally')
    for k,v in c.items():
        if k not in {'proof_location','sources'}:
            require(integrated.get(k)==v,f'{c["id"]}: original component field {k} preserved')
    loc=integrated.get('proof_location',{});p=ROOT/loc['file'];raw=p.read_bytes()
    part=b''.join(raw.splitlines(keepends=True)[loc['line_start']-1:loc['line_end']])
    require(sha(part)==loc['sha256']==loc['range_sha256'],f'{c["id"]}: exact proof block bytes')
    require(sha(raw)==loc['file_sha256'],f'{c["id"]}: exact proof file bytes')
    new_proof_files[loc['file']]=sha(raw)
    require(len(c.get('sources',[]))==len(integrated.get('sources',[])),f'{c["id"]}: source array length preserved')
    for original_ref,imported_ref in zip(c.get('sources',[]),integrated.get('sources',[])):
        require(all(imported_ref.get(k)==v for k,v in original_ref.items() if k!='range_sha256'),f'{c["id"]}: original source annotations retained')
    for r in integrated.get('sources',[]):
        if 'path' not in r or 'line_start' not in r:continue
        path=r['path']
        if path not in source_bytes:
            data=(source/path).read_bytes()
            git=subprocess.check_output(['git','-C',str(source),'show',f'{PIN}:{path}'])
            require(data==git,'source equals pinned git blob: '+path)
            source_bytes[path]=data
            snap=ROOT/'source_snapshot_v0_42'/path
            require(snap.is_file() and snap.read_bytes()==data,'source snapshot bytes: '+path)
        data=source_bytes[path];lines=data.splitlines(keepends=True)
        require(sha(data)==r.get('file_sha256',r.get('sha256')),f'{c["id"]}: source file '+path)
        a,b=r['line_start'],r['line_end'];segment=b''.join(lines[a-1:b])
        require(1<=a<=b<=len(lines) and sha(segment)==r['range_sha256'],f'{c["id"]}: source range {path}:{a}-{b}')
        source_ranges.add((path,a,b))
prov_sources={s['path']:s for s in now['source_files']};index_sources={s['path']:s for s in index['source_files']}
require(len(prov_sources)==len(now['source_files']) and len(index_sources)==len(index['source_files']),'source inventories have no duplicate paths')
for path,data in source_bytes.items():
    require(path in prov_sources and prov_sources[path].get('sha256',prov_sources[path].get('file_sha256'))==sha(data),'new cited source appears with exact hash in cumulative provenance: '+path)
    require(path in index_sources and index_sources[path].get('sha256',index_sources[path].get('file_sha256'))==sha(data),'new cited source appears with exact hash in cumulative source index: '+path)

oldmap=bind(ROOT/'dependency_audit_v0_41/obligation_map.json')
sel=bind(ROOT/'dependency_audit_v0_42/obligation_map.json')
oldnodes={n['id']:n for n in oldmap['nodes']};nodes={n['id']:n for n in sel['nodes']}
require(len(nodes)==len(sel['nodes'])==121 and set(nodes)==set(oldnodes),'selected graph preserves all 121 original nodes')
require(all(nodes[k]['gate']==v['gate'] and nodes[k]['requires']==v['requires'] for k,v in oldnodes.items()),'selected graph preserves every original gate and dependency list')
logical={k:n['requires'] for k,n in nodes.items()}
require(sum(map(len,logical.values()))==161,'selected graph preserves 161 logical edges')
try:require(acyclic(logical)==121,'selected graph is acyclic')
except AssertionError as e:require(False,'selected graph is acyclic',str(e))
closed={'AD_VANISH_K_MATCH','HOST_RIGID_S'}
require(set(cfg['closed_selected_leaves'])==closed,'only the two reviewed original whole leaves are retired')
require({k for k in nodes if nodes[k]['status']!=oldnodes[k]['status']}==closed,'selected status changes are exactly the two reviewed closures')
for k,n in nodes.items():
    if k not in closed:
        require(n['category']==oldnodes[k]['category'],k+': unchanged selected classification')
    else:
        require(n['status']=='proved_in_stated_scope' and n['kind']=='proved_certificate',k+': current complete certificate status')
        require(n['version_0_42_discharge']==cfg['closed_selected_leaves'][k],k+': closure description equals reviewed configuration')
        require(all(q in byid for q in cfg['closed_selected_leaves'][k]['claims']),k+': closure claim IDs exist')
    for field in ['evidence','bindings','joint_witness_constraint']:
        if field in oldnodes[k]:require(n[field]==oldnodes[k][field],k+': original '+field+' preserved')

closed_status={'proved_in_stated_scope','published_application_checked','complete','closed'}
opens={k for k,n in nodes.items() if n['gate']=='LEAF' and n['status'] not in closed_status}
categories=dict(collections.Counter(nodes[k]['category'] for k in opens))
require(len(opens)==31 and categories=={'C':22,'B':9},'remaining frontier is 31 leaves: 22 C and 9 B',categories)
oldreg=bind(ROOT/'dependency_audit_v0_41/remaining_leaf_register.json')
reg=bind(ROOT/'dependency_audit_v0_42/remaining_leaf_register.json')
require(opens=={x['id'] for x in oldreg['records']}-closed,'no other original open leaf was dropped')
require({x['id'] for x in reg['records']}==opens and all(x==nodes[x['id']] for x in reg['records']),'remaining register is exactly the current open selected nodes')

def reachable(start):
    reached=set(); todo=[start]
    while todo:
        k=todo.pop()
        if k in reached:continue
        reached.add(k);todo.extend(logical[k])
    return reached
rh=reachable('ORDINARY_RH');grh=reachable('DIRICHLET_GRH')
require(len(opens&rh&grh)==24 and len((opens&grh)-rh)==7 and not ((opens&rh)-grh),'route frontier is 24 shared and 7 GRH-only; no RH-only leaves')
require('COUNT_III_PRODUCER' not in rh and 'COUNT_III_PRODUCER' in grh,'Count III remains GRH-only')
require({'COUNT_I_PRODUCER','COUNT_II_SUPPORT','COUNT_V_PRODUCER'}<=rh&grh,'Count I/II/V remain on both routes')
require({'GLOBAL_DENOMINATOR','GLOBAL_RETAINED_DEFECT','GLOBAL_PERIOD_HEIGHT','GLOBAL_LOCAL_GAIN','GLOBAL_SPECTRAL','COUNT_II_SUPPORT','RIG_II'}<=opens,'all original quantitative, actual Hida-support and Type-II rigidity producers remain open')
require(all(sel['source_inputs'].get(k)==v for k,v in oldmap['source_inputs'].items()),'selected baseline source-input records are preserved')
for name,r in sel['source_inputs'].items():
    require(sha((ROOT/r['file']).read_bytes())==r['sha256'],'selected source-input byte binding: '+name)

targets=bind(ROOT/'next_source_targets.json');oldtargets=bind(OLD/'next_source_targets.json')
require(targets['targets']==oldtargets['targets'] and len(targets['targets'])==245,'all 245 historical source targets are preserved literally')
disp=bind(ROOT/'dependency_audit_v0_42/target_disposition.json')
olddisp=bind(ROOT/'dependency_audit_v0_41/target_disposition.json')
require(len(disp['records'])==len(olddisp['records'])==245 and len(disp['scope_groups'])==107,'target disposition retains 245 records and 107 scope groups')
require(all(all(b.get(k)==v for k,v in a.items()) for a,b in zip(olddisp['records'],disp['records'])),'historical target dispositions preserved with additive current notes')
require(disp['scope_groups']==olddisp['scope_groups'],'historical target scope grouping unchanged')
checkpoint=bind(ROOT/'continuation_checkpoint.json')
require(checkpoint['remaining_major_inputs']==cfg['remaining_major_inputs'] and checkpoint['next_targets']==cfg['next_targets'],'continuation checkpoint contains the current remaining inputs and priorities')
require(targets['next_local_priority']==cfg['next_targets'],'target file contains the current priorities')
for k,progress in cfg.get('selected_node_progress',{}).items():
    require(nodes[k].get('version_0_42_progress')==progress,k+': selected nested progress matches the configuration')
countii=nodes['COUNT_II_SUPPORT']
if countii['contract']!=oldnodes['COUNT_II_SUPPORT']['contract']:
    require(countii.get('historical_contract_narrative_v0_41')==oldnodes['COUNT_II_SUPPORT']['contract'],'Count-II historical contract narrative preserved separately')
require('The near-term bounded target is finU followed by ordStruct/ordFree and ordBC' not in countii['contract'],'current Count-II narrative no longer labels completed ordinary entrance as its next target')

def claim_ancestors(cid):
    seen=set(); todo=list(graph[cid])
    while todo:
        other=todo.pop()
        if other not in seen:
            seen.add(other);todo.extend(graph[other])
    return seen

named_reference_exceptions={
    ('SMP2','OCT19'):'The text states that the hypotheses of OCT1--OCT19 hold; OCT19 is the endpoint of this scope range. The proof actually invokes OCT3, OCT6, OCT7, OCT10 and OCT15, all recorded ancestors.',
    ('SMP5','SMP9'):'The text explicitly says that this fact is needed in SMP9. This is a downstream consumer reference; adding a proof dependency in this direction would be incorrect.'
}
named_reference_scan=[];observed_exceptions=set()
for c in incoming:
    if not re.fullmatch(r'(SMP|ASP)\d+',c['id']):continue
    loc=byid[c['id']]['proof_location'];raw=(ROOT/loc['file']).read_bytes()
    segment=b''.join(raw.splitlines(keepends=True)[loc['line_start']-1:loc['line_end']])
    refs=set(re.findall(r'\b[A-Z]{2,}\d+\b',segment.decode()))&set(graph)
    refs.discard(c['id'])
    outside=refs-claim_ancestors(c['id'])
    explained={other:named_reference_exceptions[(c['id'],other)] for other in outside if (c['id'],other) in named_reference_exceptions}
    unresolved=outside-set(explained)
    observed_exceptions.update((c['id'],other) for other in explained)
    require(not unresolved,c['id']+': no substantive named-proof reference missing from recorded dependency ancestry',sorted(unresolved))
    named_reference_scan.append(dict(claim=c['id'],proof_file=loc['file'],proof_file_sha256=sha(raw),proof_range_sha256=sha(segment),
        named_claims=sorted(refs),named_claims_outside_ancestry=sorted(outside),reviewed_nondependency_references=explained,
        substantive_missing_dependencies=sorted(unresolved)))
require(len(named_reference_scan)==23 and observed_exceptions==set(named_reference_exceptions),'final SMP1--SMP10 and ASP1--ASP13 named-proof scan has exactly the two independently reviewed narrative exceptions')

stats=bind(ROOT/'integration_stats_v0_42.json')
computed=dict(new_claims=len(incoming),cumulative_claims=len(claims),selected_nodes=121,selected_edges=161,
              open_count=31,open_categories=categories,shared_open=24,extra_grh_open=7,
              new_source_files_checked=len(source_bytes),new_unique_source_ranges_checked=len(source_ranges))
require(stats==computed,'reported integration statistics equal independent computation',dict(reported=stats,computed=computed))
for p,h in bindings.items():
    require(sha((ROOT/p).read_bytes())==h,'audit input remained stable: '+p)

result=dict(schema='rh-independent-integration-review/1',reviewer='global_estimates',date='2026-11-23',
    source_commit=PIN,status='PASS' if not errors else 'FAIL',scope='Independent baseline-preservation, source/proof-byte, dependency, selected-route, closure and current-scope metadata audit; no Lean replay.',
    statistics=computed,baseline_claims_preserved=count,baseline_source_files_preserved=len(old['source_files']),
    baseline_manifest_artifacts_preserved=preserved_artifacts,baseline_artifacts_retained_in_history=historically_archived,
    claims_and_sources_checked=len(incoming),passed_check_count=len(checks),errors=errors,
    input_bindings=bindings,new_proof_files=new_proof_files,component_ledgers=component_bindings,
    final_specialization_named_reference_scan=named_reference_scan,
    current_remaining_scopes={k:n.get('version_0_42_progress',{}) for k,n in nodes.items() if 'version_0_42_progress' in n},
    semantic_scope_review=[
     'The five original global quantitative producer contracts remain open. The three-test retained-defect theorem and polynomial spectral rate are sufficient conditional simplifications, not replacement claims that retire the original whole leaves.',
     'RRT closes four finite terms of Wg and the exact LocalEstimateIII/IV substatements. Its original two character laws, LocalEstimateII, normalized label bridge, adelic row construction and cylinder counts remain inputs. Finite RowsLab enumeration does not construct the automorphic spectrum.',
     'The actual rank comparison f<=k<=r together with x^2<=f, rather than abstract SizesAt alone, justifies the eventual LocalEstimateV threshold.',
     'Current Count-II progress is distinguished from its preserved historical narrative. Full finite-level, ordinary, weight/control and Hecke-algebra nested producers do not by themselves give the same ideal on both original rank-four Links; the exact current residual assembly is recorded in current_remaining_scopes.',
     'The only whole selected closures are the independently reviewed full AdVanishK match and full HostRigid_s. Type-II rigidity and quantitative host/congruence producers remain distinct open contracts.',
     'An explicit-reference scan was reviewed for dependency direction. Four genuine omitted uses were added to component metadata before integration. References RRT11->GQT5, RRT16->RRT11 and GQT6->GFI15 describe downstream consumers; inserting them as proof dependencies would be incorrect. Other retained cross-references are explanatory ranges or repeat a displayed independent argument.'
    ],
    exact_whole_closures=sorted(closed),limitations=[
     'Claim-dependency completeness is checked against the reviewed component ledgers and all graph references. This does not assert a mechanically extracted Lean transitive dependency graph.',
     'Whole leaf closure is limited to AD_VANISH_K_MATCH and HOST_RIGID_S. Newly proved nested local inputs do not retire the global quantitative or same-ideal Hida support contracts.',
     'No formal correctness, Lean compilation or kernel replay assertion is made.'])
args.output.parent.mkdir(parents=True,exist_ok=True)
args.output.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
print(json.dumps(dict(status=result['status'],statistics=computed,passed_checks=len(checks),errors=errors,output=str(args.output)),ensure_ascii=False,indent=2))
raise SystemExit(bool(errors))
