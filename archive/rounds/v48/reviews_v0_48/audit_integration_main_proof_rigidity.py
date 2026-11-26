#!/usr/bin/env python3
"""Independent, read-only audit of the v0.48 integration and unchanged v0.47 baseline."""
from pathlib import Path
import argparse
import collections
import hashlib
import json
import re
import subprocess

ROOT=Path(__file__).resolve().parents[1]
OLD=ROOT/'history/version_0_47'
PIN='7cbf7a0c32fca1badf05931879a37c3f8a2b03b4'
ap=argparse.ArgumentParser()
ap.add_argument('--source',type=Path,required=True)
ap.add_argument('--new-reader-sha256',required=True)
ap.add_argument('--cumulative-reader-sha256',required=True)
ap.add_argument('--integration-script-sha256',required=True)
ap.add_argument('--expected-source-files',type=int)
ap.add_argument('--expected-source-ranges',type=int)
ap.add_argument('--output',type=Path,default=ROOT/'reviews_v0_48/integration_main_proof_rigidity.json')
args=ap.parse_args(); source=args.source.resolve()
sha=lambda b:hashlib.sha256(b).hexdigest()
checks=[];errors=[];bindings={}
def need(ok,label,detail=None):
    if ok:checks.append(label)
    else:errors.append(dict(check=label,detail=detail))
def read(path):
    raw=path.read_bytes();bindings[str(path.relative_to(ROOT))]=sha(raw)
    return json.loads(raw)
def dag(graph):
    done,active=set(),set()
    def visit(n):
        if n not in graph:raise AssertionError(('unknown dependency',n))
        if n in active:raise AssertionError(('dependency cycle',n))
        if n in done:return
        active.add(n)
        for d in graph[n]:visit(d)
        active.remove(n);done.add(n)
    for n in graph:visit(n)
    return len(done)

need(subprocess.check_output(['git','-C',str(source),'rev-parse','HEAD'],text=True).strip()==PIN,'exact pinned source HEAD')
cfg=read(ROOT/'increment_v0_48.json')
old=read(OLD/'provenance.json');now=read(ROOT/'provenance.json')
oi=read(OLD/'source_index.json');ni=read(ROOT/'source_index.json')
bc=old['claims'];cs=now['claims'];oldcount=len(bc)
need(oldcount==2851,'baseline has exactly 2851 claims',oldcount)
need(cs[:oldcount]==bc,'all baseline claim objects, sources, proof locations and scopes preserved literally')
need(now['source_files'][:len(old['source_files'])]==old['source_files'],'baseline provenance source inventory preserved literally')
need(ni['source_files'][:len(oi['source_files'])]==oi['source_files'],'baseline source index preserved literally')
preserved=archived=0
manifest=OLD/'SHA256SUMS'
need(manifest.is_file(),'baseline SHA256SUMS exists')
if manifest.is_file():
    nonempty=[x for x in manifest.read_text().splitlines() if x.strip()]
    for line in nonempty:
        expected,rel=line.split('  ',1)
        current,history=ROOT/rel,OLD/rel
        if current.is_file() and sha(current.read_bytes())==expected:preserved+=1
        elif history.is_file() and sha(history.read_bytes())==expected:preserved+=1;archived+=1
        else:errors.append(dict(check='baseline artifact preserved at original bytes',detail=rel))
    need(preserved==len(nonempty),'every baseline artifact preserved in current tree or exact history')
ids=[c['id'] for c in cs];byid={c['id']:c for c in cs}
graph=now['mathematical_dependency_graph']
need(len(ids)==len(set(ids)),'cumulative claim IDs unique')
need(all(graph.get(k)==v for k,v in old['mathematical_dependency_graph'].items()),'all baseline dependency edges preserved literally')
need(set(graph)==set(ids),'dependency graph has exactly cumulative numbered claims')
try:need(dag(graph)==len(cs),'cumulative mathematical dependency graph acyclic')
except AssertionError as e:need(False,'cumulative mathematical dependency graph acyclic',str(e))
order=now['dependency_topological_order'];pos={k:i for i,k in enumerate(order)}
need(len(order)==len(ids) and set(order)==set(ids),'topological order covers all claims exactly once')
need(all(pos.get(d,len(ids))<pos.get(n,-1) for n,ds in graph.items() for d in ds),'topological order respects every edge')

incoming=[];component_bindings={};external_bindings=[]
for component in cfg['components']:
    ledger=read(ROOT/component/'provenance.json')
    incoming.extend(ledger['claims'])
    need(ledger.get('source_commit',PIN)==PIN,component+': component source pin unchanged')
    need(now['component_scope_metadata_as_received_v0_48'].get(component)=={k:v for k,v in ledger.items() if k not in {'claims','source_files','source_inventory','source_groups'}},component+': complete component scope metadata preserved')
    component_bindings[component]=dict(claims=len(ledger['claims']),ledger_sha256=bindings[component+'/provenance.json'])
    external={r['id']:r for key in ['published_applications','classical_and_foundational_inputs','retained_foundations','conditional_inputs','inherited_classical_and_foundational_inputs']
              for r in ledger.get(key,[]) if isinstance(r,dict) and 'id' in r}
    for c in ledger['claims']:
        names=c.get('external_input_ids',[])+c.get('published_input_ids',[])+c.get('foundation_input_ids',[])+c.get('conditional_input_ids',[])
        for name in names:
            need(name in external,c['id']+': published/foundational identifier has an explicit component record',name)
            need(name not in graph,c['id']+': published/foundational identifier is separate from numbered claim DAG',name)
        if names:external_bindings.append(dict(claim=c['id'],external_input_ids=names))
need([c['id'] for c in cs[oldcount:]]==[c['id'] for c in incoming],'new claim inventory and order match configured component ledgers')
sources={};ranges=set();proofs={}
for c in incoming:
    integrated=byid[c['id']]
    need(integrated['depends_on']==c.get('depends_on',[])==graph[c['id']],c['id']+': literal proof dependencies preserved')
    for key,value in c.items():
        if key not in {'proof_location','sources'}:need(integrated.get(key)==value,c['id']+': component field '+key+' preserved')
    pl=integrated['proof_location'];raw=(ROOT/pl['file']).read_bytes()
    part=b''.join(raw.splitlines(keepends=True)[pl['line_start']-1:pl['line_end']])
    need(sha(part)==pl['sha256']==pl['range_sha256'],c['id']+': exact proof-block bytes')
    need(sha(raw)==pl['file_sha256'],c['id']+': exact proof-file bytes')
    need(re.search(rb'^% BEGIN '+re.escape(c['id'].encode())+rb'\s*$',part,re.M) is not None and re.search(rb'^% END '+re.escape(c['id'].encode())+rb'\s*$',part,re.M) is not None,c['id']+': proof range contains its exact numbered block markers')
    need(len(re.findall(rb'^% BEGIN '+re.escape(c['id'].encode())+rb'\s*$',raw,re.M))==1,c['id']+': proof marker unique in its component')
    proofs[pl['file']]=sha(raw)
    need(len(c.get('sources',[]))==len(integrated.get('sources',[])),c['id']+': source array length retained')
    for original,added in zip(c.get('sources',[]),integrated.get('sources',[])):
        need(all(added.get(k)==v for k,v in original.items() if k!='range_sha256'),c['id']+': source annotations retained')
    for s in integrated.get('sources',[]):
        if 'path' not in s or 'line_start' not in s:continue
        path=s['path']
        if path not in sources:
            data=(source/path).read_bytes()
            need(data==subprocess.check_output(['git','-C',str(source),'show',f'{PIN}:{path}']),'source equals pinned Git blob: '+path)
            sources[path]=data
            snapshot=ROOT/'source_snapshot_v0_48'/path
            need(snapshot.is_file() and snapshot.read_bytes()==data,'source snapshot exact bytes: '+path)
        data=sources[path];lines=data.splitlines(keepends=True);a,b=s['line_start'],s['line_end']
        need(sha(data)==s.get('file_sha256',s.get('full_file_sha256',s.get('sha256'))),c['id']+': source-file hash '+path)
        need(1<=a<=b<=len(lines) and sha(b''.join(lines[a-1:b]))==s['range_sha256'],c['id']+f': source-range hash {path}:{a}-{b}')
        ranges.add((path,a,b))
for label,items in [('provenance',now['source_files']),('index',ni['source_files'])]:
    mapping={s['path']:s for s in items}
    need(len(mapping)==len(items),label+' source paths unique')
    for path,data in sources.items():
        need(path in mapping and mapping[path].get('sha256',mapping[path].get('file_sha256'))==sha(data),label+' source inventory exact hash: '+path)

oldmap=read(ROOT/'dependency_audit_v0_47/obligation_map.json')
newmap=read(ROOT/'dependency_audit_v0_48/obligation_map.json')
oldnodes={n['id']:n for n in oldmap['nodes']};nodes={n['id']:n for n in newmap['nodes']}
need(len(nodes)==len(newmap['nodes'])==121 and set(nodes)==set(oldnodes),'selected sufficient-route graph preserves all 121 nodes')
need(all(nodes[k]['gate']==v['gate'] and nodes[k]['requires']==v['requires'] for k,v in oldnodes.items()),'every selected gate and dependency list preserved')
logical={k:n['requires'] for k,n in nodes.items()}
need(sum(map(len,logical.values()))==161,'selected sufficient-route graph preserves 161 edges')
try:need(dag(logical)==121,'selected sufficient-route graph acyclic')
except AssertionError as e:need(False,'selected sufficient-route graph acyclic',str(e))
closed=set(cfg['closed_selected_leaves'])
need(closed=={'TASK_ONE_CHAR_PROOF'},'exactly the original OneChar implication task is newly discharged',sorted(closed))
for cid,previous in oldnodes.items():
    allowed={'category','kind','status','opaque_frontier'} if cid in closed else set()
    for key,value in previous.items():
        if key=='contract' and cid in cfg.get('updated_contracts',{}):continue
        if key in allowed:continue
        need(nodes[cid].get(key)==value,cid+': prior selected node field retained: '+key)
    if cid in closed:
        need(nodes[cid]['predecessor_status_v0_47']=={k:previous[k] for k in ['category','kind','status']},cid+': exact predecessor status retained')
        need(nodes[cid]['status']=='proved_in_stated_scope' and nodes[cid]['kind']=='proved_certificate' and nodes[cid]['category']==cfg['closed_selected_leaves'][cid]['category'] and nodes[cid]['opaque_frontier'] is False,cid+': only reviewed status transition installed')
        need(nodes[cid]['version_0_48_discharge']==cfg['closed_selected_leaves'][cid],cid+': exact reviewed discharge record installed')
need(all(nodes[k]['status']=='proved_in_stated_scope' for k in ['AD_VANISH_K_MATCH','HOST_RIGID_S']),'two inherited v0.42 whole closures remain closed')
closed_status={'proved_in_stated_scope','published_application_checked','complete','closed'}
opens={k for k,n in nodes.items() if n['gate']=='LEAF' and n['status'] not in closed_status}
cats=dict(collections.Counter(nodes[k]['category'] for k in opens))
need(len(opens)==25 and cats=={'C':18,'B':7},'remaining frontier is 25 whole leaves: 18 C and 7 B',cats)
oldreg=read(ROOT/'dependency_audit_v0_47/remaining_leaf_register.json')
reg=read(ROOT/'dependency_audit_v0_48/remaining_leaf_register.json')
need(opens=={n['id'] for n in oldreg['records']}-closed,'all other original open whole contracts remain open')
need({n['id'] for n in reg['records']}==opens and all(n==nodes[n['id']] for n in reg['records']),'remaining register exactly matches current selected nodes')
def reachable(start):
    seen=set();todo=[start]
    while todo:
        k=todo.pop()
        if k not in seen:seen.add(k);todo.extend(logical[k])
    return seen
rh=reachable('ORDINARY_RH');grh=reachable('DIRICHLET_GRH')
need(len(opens&rh&grh)==18 and len((opens&grh)-rh)==7 and not((opens&rh)-grh),'18 shared and 7 GRH-only open obligations; none RH-only')
need('COUNT_III_PRODUCER' not in rh and 'COUNT_III_PRODUCER' in grh,'Count III remains GRH-only')
need({'GLOBAL_DENOMINATOR','GLOBAL_RETAINED_DEFECT','GLOBAL_PERIOD_HEIGHT','GLOBAL_LOCAL_GAIN','GLOBAL_SPECTRAL','AUT_UNRAM_COEF'}<=opens,'all other full global quantitative and global assembly producer obligations remain open')
need(all(newmap['source_inputs'].get(k)==v for k,v in oldmap['source_inputs'].items()),'selected baseline source inputs preserved')
for k,r in newmap['source_inputs'].items():need(sha((ROOT/r['file']).read_bytes())==r['sha256'],'selected source-input byte binding: '+k)
for k,progress in cfg.get('selected_node_progress',{}).items():
    need(nodes[k].get('version_0_48_progress')==progress,k+': current nested progress matches configuration')
for k,contract in cfg.get('updated_contracts',{}).items():
    need(nodes[k]['contract']==contract,k+': current contract narrative matches configuration')
    need(nodes[k].get('historical_contract_narrative_v0_47')==oldnodes[k]['contract'],k+': prior exact contract narrative retained separately')

targets=read(ROOT/'next_source_targets.json');oldtargets=read(OLD/'next_source_targets.json')
need(targets['targets']==oldtargets['targets'] and len(targets['targets'])==245,'all 245 historical source targets preserved literally')
disp=read(ROOT/'dependency_audit_v0_48/target_disposition.json');od=read(ROOT/'dependency_audit_v0_47/target_disposition.json')
need(len(disp['records'])==len(od['records'])==245 and len(disp['scope_groups'])==107,'245 dispositions and 107 scope groups preserved')
need(all(all(b.get(k)==v for k,v in a.items()) for a,b in zip(od['records'],disp['records'])),'historical target disposition fields retained with additive current notes')
need(disp['scope_groups']==od['scope_groups'],'historical target grouping unchanged')
checkpoint=read(ROOT/'continuation_checkpoint.json')
need(checkpoint['remaining_major_inputs']==cfg['remaining_major_inputs'] and checkpoint['next_targets']==cfg['next_targets'],'continuation checkpoint contains current frontier and priorities')
need(targets['next_local_priority']==cfg['next_targets'],'next source priorities are current')
need(now['scope']==cfg['status'],'active provenance scope is the current v0.48 status')
expected_active_audit={
    'artifact_version':'0.48',
    'file':'dependency_audit_v0_48/obligation_map.json',
    'explanatory_chapter':'dependency_audit_v0_48/main.tex',
    'complete_backlog_disposition':'dependency_audit_v0_48/target_disposition.json',
    'remaining_leaf_register':'dependency_audit_v0_48/remaining_leaf_register.json',
    'route_coverage':'dependency_audit_v0_48/route_coverage.json',
    'scope':'Selected sufficient interfaces with completed consumers distinct from open producers and shared work.'}
need(checkpoint['current_dependency_audit']==expected_active_audit,'active checkpoint audit references are the exact v0.48 records')
for key,file in expected_active_audit.items():
    if key in {'artifact_version','scope'}:continue
    need((ROOT/file).is_file(),'active audit destination exists: '+key)
integration_script=(ROOT/'integrate_v0_48.py').read_bytes()
bindings['integrate_v0_48.py']=sha(integration_script)
need(sha(integration_script)==args.integration_script_sha256,'integration generator matches the announced frozen version')


# Exact completed implications remain separate from their producer premises.
component_closures={}
closure_keys=['whole_obligations_closed','whole_obligation_closures',
              'new_global_frontier_leaf_closures','whole_selected_leaf_closed']
for component in cfg['components']:
    path=ROOT/component/('contracts.json' if component=='adelic_measures_v48' else 'closure.json')
    need(path.is_file(),component+': explicit component closure record exists')
    if not path.is_file():continue
    closure=read(path);component_closures[component]=closure
    present=[k for k in closure_keys if k in closure]
    need(bool(present),component+': whole-closure scope explicitly recorded')
    need(all(closure[k] in ([],False,{}) for k in present),component+': root integration alone installs the reviewed whole selected transition')
    expected=closure.get('proof_file_sha256',closure.get('main_tex_sha256'))
    need(expected==proofs[component+'/main.tex'],component+': closure binds exact frozen main proof')
expected_components={'one_character_v48','adelic_measures_v48',
                     'principal_uniformization_v48','common_compatibility_v48'}
need(set(cfg['components'])==expected_components,'exact four independently reviewed continuation components')
cid='TASK_ONE_CHAR_PROOF';component='one_character_v48'
review_file=component+'/review_OCH1_OCH30_root.json'
need(cfg['closure_reviews'][cid]==review_file,cid+': configuration names the exact independent root closure gate')
review=read(ROOT/review_file);whole=review['selected_whole_contract_reviewed']
need(review['result']=='PASS' and review['reviewer']=='root' and whole['id']==cid and whole['full_original_contract_closed_in_stated_scope'] is True,cid+': independent root review accepts the whole original selected implication')
need(whole['baseline_contract_sha256']==sha(oldnodes[cid]['contract'].encode()),cid+': whole-contract review binds the literal v0.47 baseline contract')
need(nodes[cid]['contract']==oldnodes[cid]['contract'],cid+': the closed whole contract has not been weakened or replaced')
need(review['proof_sha256']==proofs[component+'/main.tex'],cid+': whole-contract review binds final proof bytes')
need(set(cfg['closed_selected_leaves'][cid]['claims'])=={'OCH'+str(i) for i in range(1,31)},cid+': exact thirty-claim producer supplies closure')
need({x['id'] for x in review['claims_reviewed']}=={'OCH'+str(i) for i in range(1,15)}|{'OCH30'},cid+': root review explicitly covers local/model construction and exact endpoint')
complementary=review.get('complementary_independent_review_files',[])
need(bool(complementary),cid+': closure gate requires complementary arithmetic and length review')
complementary_ids=set()
for rel in complementary:
    rr=read(ROOT/rel)
    need(rr.get('result',rr.get('status'))=='PASS' and rr['proof_sha256']==proofs[component+'/main.tex'],cid+': complementary review is current and passed')
    complementary_ids.update(x['id'] for x in rr['claims_reviewed'])
need({'OCH'+str(i) for i in range(15,31)}<=complementary_ids,cid+': complementary review covers every arithmetic/point/length/coefficient claim')
och=component_closures.get(component,{})
need(och.get('foundation_retention_explicit') is True and och.get('AUT_UNRAM_COEF_remains_separate') is True,'OCH retains the original named foundations and separate automorphy producer')
need(och.get('status')=='complete_at_stated_scope_independently_reviewed' and och.get('pending')==[],'OCH is complete with every claim independently reviewed')
och_contract=read(ROOT/component/'contracts.json')
need(och_contract['endpoint_claim']=='OCH30' and och_contract['original_endpoint']=='UpperTheory.V.Z.Kato.oneChar : InpZ -> AutomorphyUnramifiedCoefficients -> UpperTheory.V.U3.OneChar','OCH binds the literal original implication endpoint')
need(och_contract.get('selected_contract_is_implication') is True and och_contract.get('original_admissibility_not_weakened') is True,'OCH closure has exactly the original implication and admissibility scope')
need(och_contract['original_GD_fields']=={'ell_odd':'ell!=2','e_pos':'1<=e','N_even':'Even N','ord':'ell does not divide orderOf psi','ine':'comp ell psi squared is one','par':'PsiEven e psi','quad':'[K:Q]=2','imag':'K totally complex','ell_cop':'ell does not divide abs(disc K)*classNumber K','cop':'abs(disc K) coprime to N','eta':'ker(cycMod ell,1) intersect ker(dirG(chiP ell psi)) is not contained in G_K','gen':'ell-1 does not divide2e'},'OCH retains every literal GD field with no extra small-prime cutoff')
need('AUT_UNRAM_COEF' in opens and 'TASK_ONE_CHAR_PROOF' not in opens,'the actual automorphy premise remains open while its full OneChar implication is supplied')
need(nodes['ONE_CHAR']['status']==oldnodes['ONE_CHAR']['status'] and nodes['ONE_CHAR']['requires']==oldnodes['ONE_CHAR']['requires'],'the composite OneChar producer is not silently promoted past the retained automorphy premise')
need(all(nodes[k]['status']=='proved_in_stated_scope' for k in ['RIG_II','TASK_INP_Z_ASSEMBLY','CNR3','TASK_PROP_GK_INSTALL','COUNT_II_SUPPORT']),'all inherited arithmetic whole closures remain installed')
amd=component_closures.get('adelic_measures_v48',{})
need(amd.get('endpoint_claim')=='AMD12' and amd.get('whole_obligation_closures')==[],'AMD supplies the full measured constructor without a whole spectral/family closure')
need(any('Bessel' in x for x in amd.get('not_claimed',[])) and any('Siegel' in x for x in amd.get('not_claimed',[])),'AMD explicitly retains Bessel and Siegel--Weil/fiber measure ties')
pun=component_closures.get('principal_uniformization_v48',{})
for key in ['full_LatZ_supplied','full_A_equals_one_ExpoMatch_at_original_ModelBase_supplied','full_modelsOf_at_supplied_FamilyUnif_supplied','full_individual_point_and_equality_suppliers_written']:
    need(pun.get(key) is True,'PUN exact original completed scope: '+key)
for key in ['full_N1c_supplied','full_principal_uniformization_supplied','full_LatFull_unconditional_supplier_closed']:
    need(pun.get(key) is False,'PUN explicit unsupplied whole scope: '+key)
gcf=component_closures.get('common_compatibility_v48',{})
for key in ['full_original_GIs2','full_original_IsRecG','all_five_compatibility_fields_constructed_on_actual_stage','given_period_root_and_coefficient_field_unchanged','one_G_before_all_later_choices','arbitrary_division_lattice_transport','actual_comparison_equality_preserved','selected_D3_TopsF_produced','selected_D3_Adm2F_produced','original_common_family_realization_retained','original_geometric_chain_unchanged','exact_error_and_constants_preserved']:
    need(gcf.get(key) is True,'GCF exact original constructor/remaining-realization scope: '+key)
need('common_GroupCompatibilityFamily_and_Adm2F_remain_explicit' not in newmap['validation'],'ambiguous inherited common-family/admission flag is not active')
for key in ['selected_D3_TopsF_and_Adm2F_supplied_by_ChosenE','actual_eventual_common_WPt_TSel_realization_remains_explicit','full_original_OneChar_implication_complete','original_AutomorphyUnramifiedCoefficients_remains_explicit']:
    need(newmap['validation'].get(key) is True,'active scope flag separates completed constructor from retained producer: '+key)
need({'GLOBAL_DENOMINATOR','GLOBAL_RETAINED_DEFECT','GLOBAL_PERIOD_HEIGHT','GLOBAL_LOCAL_GAIN','GLOBAL_SPECTRAL'}<=opens,'all five full global quantitative contracts remain open')
need({'DESIGN_CHOICES_COMMON','BASE_THETA_RATIONAL_TESTS'}<=opens,'individual primitive points and conditional common stages do not close the common geometric whole obligations')
need(not newmap['validation'].get('all_original_finite_local_character_laws_complete',False),'unused fourth local character law not claimed')
need(now['validation'].get('lean_build') is False and now['validation'].get('kernel_replay') is False and now['validation'].get('dependency_graph_is_lean_transitive_audit') is False,'human/source integration is not presented as Lean replay or formal transitive dependency extraction')
need(len(incoming)==89 and len(cs)==2940,'exact new and cumulative claim counts: 89 and 2940')
new_categories=dict(collections.Counter(c['classification'] for c in incoming))
need(new_categories=={'B':89},'new proof classification is exactly 89 B and no new A',new_categories)
# Baseline source snapshots, newly added snapshots, and indexes have different scopes;
# the new manifest must enumerate precisely the sources actually cited this increment.
sm=read(ROOT/'source_snapshot_v0_48/manifest.json')
need(sm['commit']==PIN,'new source snapshot records exact pin')
need(len(sm['files'])==len(sources) and {r['path'] for r in sm['files']}==set(sources),'new source manifest has exactly all cited source files')
for record in sm['files']:
    data=sources.get(record['path'],b'')
    need(record['sha256']==sha(data) and record['bytes']==len(data) and record['line_count']==len(data.splitlines()),'new source snapshot record exact: '+record['path'])
coverage=read(ROOT/'dependency_audit_v0_48/route_coverage.json')
need(coverage['graph_sha256']==sha((ROOT/'dependency_audit_v0_48/obligation_map.json').read_bytes()),'selected route coverage bound to current graph')
need(coverage['ordinary_rh_open_leaf_count']==18 and coverage['dirichlet_grh_open_leaf_count']==25 and coverage['shared_open_leaf_count']==18,'route coverage counts are exact')
need(coverage['shared_open_leaf_ids']==sorted(opens&rh&grh) and coverage['dirichlet_grh_only_open_leaf_ids']==sorted((opens&grh)-rh) and coverage['ordinary_rh_only_open_leaf_ids']==[],'route coverage IDs match independent reachability')
delta=read(ROOT/'dependency_audit_v0_48/closure_delta.json')
need(delta['closed_selected_leaves']==cfg['closed_selected_leaves'] and delta['closed_nested_producers']==cfg['closed_nested_producers'] and delta['prior_open_leaf_count']==26 and delta['current_open_leaf_count']==25 and delta['new_proof_claims']==89,'closure delta separates producer progress from exactly one reviewed whole-leaf discharge')
apps=read(ROOT/'dependency_audit_v0_48/published_applications.json')
need(apps['freshly_checked_applications']==cfg['published_applications'],'published-application scope preserved literally')
need(apps['inherited_registry']['sha256']==sha((ROOT/apps['inherited_registry']['file']).read_bytes()),'inherited published registry remains byte-bound')

def ancestors(cid):
    seen=set();todo=list(graph[cid])
    while todo:
        k=todo.pop()
        if k not in seen:seen.add(k);todo.extend(graph[k])
    return seen
# An out-of-ancestry reference is an error unless its complete proof block has
# been read and an explicit non-premise reason is recorded here.
exceptions={
 ('OCH11','OCH12'):'OCH11 asserts and proves only the actual graded presentation, base point and numerical shape. Its statement and proof explicitly defer pts/der/lift to OCH12--OCH14. Those later conclusions are not premises in the construction of the partial structure.',
 ('OCH11','OCH14'):'This is the same explicit forward-completion reference. OCH14 subsequently assembles the full Model after constructing its last field; OCH11 does not claim that completed record.',
 ('OCH26','SP6'):'OCH26 identifies and proves the original M1--M5 antecedents appearing in SP6. It assumes its own stated FinA and PtHyp and does not use SP6 upper-bound conclusion. OCH27 then applies that theorem with an explicit SP6 dependency.'
}


reference_scan=[]
for c in incoming:
    pl=byid[c['id']]['proof_location'];raw=(ROOT/pl['file']).read_bytes()
    block=b''.join(raw.splitlines(keepends=True)[pl['line_start']-1:pl['line_end']])
    named=set(re.findall(r'\b[A-Z]{2,}\d+\b',block.decode()))&set(graph)
    named.discard(c['id']);outside=named-ancestors(c['id'])
    explained={k:exceptions[(c['id'],k)] for k in outside if (c['id'],k) in exceptions}
    missing=outside-set(explained)
    need(not missing,c['id']+': named proof uses represented in dependency ancestry',sorted(missing))
    reference_scan.append(dict(claim=c['id'],proof_range_sha256=sha(block),named_claims=sorted(named),
        named_claims_outside_ancestry=sorted(outside),reviewed_nondependency_references=explained,
        substantive_missing_dependencies=sorted(missing)))

# Component review schemas differ only in bookkeeping; normalize them while
# checking every whole-file hash and every claimed mathematical block separately.
review_paths=[]
for component in cfg['components']:
    for path in sorted((ROOT/component).glob('*review*.json')):
        record=json.loads(path.read_bytes())
        entries=record.get('reviewed_claims',record.get('claims_reviewed',record.get('claims',list(record.get('proof_hashes',{})))))
        if entries and record.get('reviewer'):
            review_paths.append(str(path.relative_to(ROOT)))
reviewed=set();review_coverage=[];new_ids={c['id'] for c in incoming}
need(bool(review_paths),'independent mathematical review files found')
for rel in review_paths:
    review=read(ROOT/rel)
    result=review.get('status',review.get('result'))
    need(result=='PASS',rel+': independent mathematical review PASS')
    file=review.get('proof_file',str(Path(rel).parent/'main.tex'));data=(ROOT/file).read_bytes()
    expected=[review[k] for k in ['proof_file_sha256','proof_sha256','main_tex_sha256'] if k in review]
    need(bool(expected) and all(h==sha(data) for h in expected),rel+': every reviewed whole-file hash is current')
    need(review.get('source_commit',PIN)==PIN,rel+': review uses exact source pin')
    entries=review.get('reviewed_claims',review.get('claims_reviewed',review.get('claims',list(review.get('proof_hashes',{})))))
    found=[]
    for entry in entries:
        if isinstance(entry,str):
            cid=entry;h=review.get('proof_hashes',{}).get(cid);entry_status=result
        else:
            cid=entry.get('id',entry.get('claim'))
            h=entry.get('proof_range_sha256',entry.get('block_sha256'))
            entry_status=entry.get('status',entry.get('result',result))
        need(cid in new_ids,rel+': reviewed claim is a new numbered claim '+str(cid))
        need(entry_status=='PASS',rel+': reviewed claim passed '+str(cid))
        if cid not in byid:continue
        pl=byid[cid]['proof_location']
        need(pl['file']==file,rel+': reviewed claim is in the bound proof file '+cid)
        block=b''.join(data.splitlines(keepends=True)[pl['line_start']-1:pl['line_end']])
        need(h in {sha(block),sha(block.rstrip(b'\r\n'))},rel+': current claim block matches reviewed bytes '+cid)
        if isinstance(entry,dict) and 'line_start' in entry:
            need((entry['line_start'],entry['line_end'])==(pl['line_start'],pl['line_end']),rel+': reviewed block positions match '+cid)
        reviewed.add(cid);found.append(cid)
    need(len(found)==len(set(found)),rel+': reviewed claim inventory has no duplicate')
    review_coverage.append(dict(file=rel,reviewer=review['reviewer'],claims=len(found),claim_ids=found,proof_file=file,proof_file_sha256=sha(data)))
need(reviewed==new_ids,'all and only 89 new claims have matching independent mathematical review coverage',sorted(new_ids-reviewed))
# Explicitly test the two frozen reader artifacts without binding progress reports
# and README, which are produced only after independent validation completes.
reader_files={'RH_new_proofs_v0_48.tex':args.new_reader_sha256,'RH_readable_reconstruction_v0_48.tex':args.cumulative_reader_sha256}

def reader_wrap(text):
    # The assembly adds only discretionary line-breaking commands to monospaced
    # identifiers and escaped underscores. Check the entire expanded chapter.
    def mono(match):
        t=re.sub(r'(?<=[a-z])(?=[A-Z])',lambda _:r'\allowbreak ',match[1])
        t=re.sub(r'\.(?!\\allowbreak)',lambda _:r'.\allowbreak ',t)
        t=re.sub(r'([/:])(?!\\allowbreak)',lambda m:m[1]+r'\allowbreak ',t)
        t=re.sub(r'\\_(?!\\allowbreak)',lambda _:r'\_\allowbreak ',t)
        return r'\texttt{'+t+'}'
    text=re.sub(r'\\texttt\{([^{}]*)\}',mono,text)
    return re.sub(r'\\_(?!\\allowbreak)',lambda _:r'\_\allowbreak ',text)
for file,h in reader_files.items():
    raw=(ROOT/file).read_bytes();bindings[file]=sha(raw)
    need(sha(raw)==h,file+': exact frozen reader bytes')
    for component in cfg['components']:
        need(reader_wrap((ROOT/component/'main.tex').read_text()).encode() in raw,file+': includes entire exact component modulo specified discretionary breaks: '+component)

old_reader_path=ROOT/'RH_readable_reconstruction_v0_47.tex'
old_reader=old_reader_path.read_bytes();bindings[str(old_reader_path.relative_to(ROOT))]=sha(old_reader)
old_audit=(ROOT/'dependency_audit_v0_47/main.tex').read_text()
old_marker=re.search(r'^\\section\{[^\n]+',old_audit,re.M)[0]
new_reader=(ROOT/'RH_readable_reconstruction_v0_48.tex').read_text()
need(old_reader.decode().count(old_marker)==1 and new_reader.count(old_marker)==1,'historical reader audit marker occurs exactly once in both cumulative editions')
def preserved_reader_body(txt):
    body=txt[txt.index(old_marker):]
    a=body.index(r'\section{The arithmetic still to be written out}')
    b=body.index(r'\section{Claim ledger and reading order}',a)
    body=body[:a]+'[CURRENT FRONTIER PROSE]\n'+body[b:]
    m=re.search(r'Start with the version-0\.\d+ audit in',body)
    assert m is not None,'historical reading-guide start missing'
    b=body.index('RF16 correction.',m.start())+len('RF16 correction.')
    return body[:m.start()]+'[CURRENT READING GUIDE]'+body[b:]
need(preserved_reader_body(old_reader.decode())==preserved_reader_body(new_reader),'complete historical cumulative reader body preserved except two documented current-scope prose replacements')

stats=read(ROOT/'integration_stats_v0_48.json')
computed=dict(new_claims=len(incoming),cumulative_claims=len(cs),selected_nodes=121,selected_edges=161,
    open_count=25,open_categories=cats,shared_open=18,extra_grh_open=7,
    new_source_files_checked=len(sources),new_unique_source_ranges_checked=len(ranges))
if args.expected_source_files is not None:need(len(sources)==args.expected_source_files,'exact announced source-file count',len(sources))
if args.expected_source_ranges is not None:need(len(ranges)==args.expected_source_ranges,'exact announced source-range count',len(ranges))
need(stats==computed,'reported integration statistics equal independent computation',dict(reported=stats,computed=computed))
bindings[str(Path(__file__).resolve().relative_to(ROOT))]=sha(Path(__file__).read_bytes())
for p,h in proofs.items():need(sha((ROOT/p).read_bytes())==h,'proof file stable during audit: '+p)
for p,data in sources.items():need((source/p).read_bytes()==data and (ROOT/'source_snapshot_v0_48'/p).read_bytes()==data,'source and snapshot stable during audit: '+p)
for p,h in bindings.items():need(sha((ROOT/p).read_bytes())==h,'audit input stable during review: '+p)
result=dict(schema='rh-independent-integration-review/1',reviewer='main_proof_rigidity',date='2026-11-23',
    source_commit=PIN,status='PASS' if not errors else 'FAIL',
    scope='Independent preservation, source/proof bytes, dependency, selected-route, closure and current-scope audit; no Lean replay.',
    statistics=computed,new_claim_categories=new_categories,baseline_claims_preserved=oldcount,baseline_source_files_preserved=len(old['source_files']),
    baseline_manifest_artifacts_preserved=preserved,baseline_artifacts_retained_in_history=archived,
    claims_and_sources_checked=len(incoming),passed_check_count=len(checks),errors=errors,input_bindings=bindings,
    new_proof_files=proofs,component_ledgers=component_bindings,named_proof_reference_scan=reference_scan,
    named_external_input_bindings=external_bindings,independent_mathematical_review_coverage=review_coverage,
    exact_whole_closures=cfg['closed_selected_leaves'],current_remaining_scopes={k:n.get('version_0_48_progress') for k,n in nodes.items() if 'version_0_48_progress' in n},
    semantic_scope_review=[
        'OCH reconstructs the complete original implication InpZ plus AutomorphyUnramifiedCoefficients implies OneChar. Every finite-Artin crystalline component, integral weighted model, actual point and derivative, normalized Selmer injection, finite irredundant orbit set, every-cover trace bound and original coefficient return is supplied. The exact root closure gate binds the original TASK_ONE_CHAR_PROOF contract and complementary independent review covers the full arithmetic half. AUT_UNRAM_COEF remains independently open, with one jointly marked g1 and the original fixed iota and all FinA/AutB/LemW quantifiers.',
        'AMD supplies the full original adelic measured-data constructor and prescribed-measure extension, including covolume-one normalization for the actual rational unipotent quotient. The given infinity/global/local measures and standard frame stay fixed as specified. The original Bessel vector, orbital/fiber and Siegel--Weil ties and full family realization remain separate.',
        'PUN supplies the fixed Hermitian-space arithmetic model, all original LatModel fields, ModelsOf conditional on the supplied FamilyUnif, the actual center lattice and exact A=1 exponent matching, and individual primitive points with full nonreduced KTriv and original Weil sign/markings. N1c, global holomorphic/principal uniformization, simultaneous normalized theta and full integral-cusp spanning remain open.',
        'GCF supplies the actual KDq determinant quotient, prescribed-column extension, the given period root over the same coefficient field, all five compatibility fields and one original GJStage before all later choices. Arbitrary division-lattice changes preserve the given comparison map. The selected D3 tops/admission follow from its ChosenE, while the common WPt/TSel realization on the actual comparison/kernel remains an explicit producer.',
        'All 121 selected sufficient-route nodes and 161 edges are retained. Exactly TASK_ONE_CHAR_PROOF moves from its old category-C frontier to proved status; the remaining 25 whole obligations are 18 C and 7 B, with 18 shared and 7 extra GRH. Every one of 2851 predecessor claim objects, source arrays and dependencies remains literally equal. The historical cumulative proof body is preserved except the two documented current-frontier and reading-guide prose replacements.'
    ],limitations=['Recorded graph is the human-proof dependency graph, not a mechanically extracted Lean transitive graph.',
        'Independent mathematical component reviews remain separately bound; this integration audit does not reprove every component theorem.',
        'No Lean compilation, kernel replay, formal correctness challenge or completed unconditional human proof of RH/GRH is asserted.'])
args.output.parent.mkdir(parents=True,exist_ok=True)
args.output.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
print(json.dumps(dict(status=result['status'],statistics=computed,passed_checks=len(checks),errors=errors,output=str(args.output)),ensure_ascii=False,indent=2))
raise SystemExit(bool(errors))
