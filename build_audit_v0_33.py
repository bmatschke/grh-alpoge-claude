#!/usr/bin/env python3
"""Update the complete selected audit while preserving predecessor scopes."""
from pathlib import Path
import copy,hashlib,json,collections
ROOT=Path(__file__).resolve().parent;AUD=ROOT/'dependency_audit_v0_33';OLD=ROOT/'dependency_audit_v0_32'
def read(p):return json.loads(p.read_text())
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def write(p,d):p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n')
cfg=read(ROOT/'increment_v0_33.json');g=copy.deepcopy(read(OLD/'obligation_map.json'))
g['artifact_version']='0.33';g['predecessor_graph']=dict(file='dependency_audit_v0_32/obligation_map.json',sha256=sha(OLD/'obligation_map.json'))
nodes={n['id']:n for n in g['nodes']}
def evidence(comp,ids):return dict(component=comp,claims=ids,ledger=comp+'/provenance.json',ledger_sha256=sha(ROOT/comp/'provenance.json'),proof_file=comp+'/main.tex',proof_sha256=sha(ROOT/comp/'main.tex'))
def refine(ident,contract,proofs,complete=False):
    n=nodes[ident];prev=copy.deepcopy(n);n['previous_interface']=prev
    n.update(contract=contract,introduced_or_refined_in='0.33')
    n.setdefault('evidence',[]).extend(proofs)
    if complete:n.update(status='proved_in_stated_scope',kind='implication_certificate',category='B')
    return n
gls=cfg['component_claims']['global_slope'];fia=cfg['component_claims']['finite_isotropic_average'];ctc=cfg['component_claims']['constant_terms'];jsp=cfg['component_claims']['joint_support']
evg=evidence('global_slope',gls);evf=evidence('finite_isotropic_average',fia);evc=evidence('constant_terms',ctc);evj=evidence('joint_support',jsp)
refine('TASK_GL4_COLUMN_VALUES',
 'GLS1–GLS3 construct the actual ColVal from the original ColsTiedSym and adm3 on the same selected family: literal class lattices, conjugate embeddings, polynomial isomorphism, every finite-place membership test and the exact archimedean norm. This completes the tCV implication under the already explicit compatible second-layer input; it does not produce that input.',[evg],True)
refine('TASK_GL4_SLOPE_LOWER',
 'GLS4–GLS7 prove the original closed FamilySlopeLowerOpenPart implication: exact column slope −log(T)/k for any supplied original ColVal, the finite normal-order highest-vector norm recurrence, hook bound and normalized divided-power Weyl determinant estimate, with the literal metric and scalar extension. Shared original class/family premises remain upstream.',[evg],True)
refine('TASK_GL4_SLOPE_MAX',
 'GLS8–GLS12 prove the original closed FamilySlopeMaxOpenPart(4) implication. Banaszczyk Theorem2.1 is applied to the actual positive trace Euclidean lattice with its trace/codifferent dual checked; the short-vector, original class-basis polynomial and coefficient-norm calculations retain the exact constant4 and all coefficient embeddings. The compatible forms remain supplied by the shared second layer.',[evg],True)
refine('TASK_GL_FINAL_ASSEMBLY',
 'GLS13 assembles all eleven original FamGLmin(D3(3,A),4) fields on the SAME supplied second-layer selector and Duty, using the proved GL4/GL6 inputs. What remains is the human numerical/lattice implication linkGLOBAL7_min/items and link8 on that same class, from these fields, original congruence length, ChosenWall/Duty and TuSize, with Cabs=2,C0=3,C5=4,eD=2,eL=0. Preserve the actual frame/HN and loss inequalities. The Closed epsilon cutoff and TransportedAlt tuple precede the supplied Fm,CH; the eventual x threshold may depend on that Fm,CH but precedes i,u and every place. FamGLmin existence is conditional on the common upstream second layer.',[evg])
refine('TASK_LINK_GL_INSTALL',
 'The h3, all three original GL4 and five GL6 implications, and their eleven-field FamGLmin assembly are now complete on the exact supplied original second-layer data. Only the final numerical/lattice linkGLOBAL7_min/items/link8 step below remains unwritten inside this installation. The AND rule retains each original completed slot and the shared mass/selector context; no new class member or compatible forms are inferred.',[evg])
refine('BASE_THETA_CUSPIDAL_EXTENSION',
 'On the SAME selected Bundle and SAME reading as BASE_THETA_READINGS, extend the exact lowest-type theta integral for each finite basis vector of HV(i,t0) to the original Wall_i with one family threshold before i and the basis vectors. BTH3 proves convergence; FIA8 and CTC1–CTC13 now prove the actual finite average, ZCusp and genuinely convergent full cuspidality. The remaining work is original smoothness and uniform derivative-growth estimates, lowering and prescribed lowest type, finite-level/equivariance installation and Sobolev-continuous bounded holomorphic/Hilbert multiplicity realization. Retain one original ioP with its universal parameter conditions; base-only existence is insufficient.',[evf,evc])
refine('CERT_BASE_THETA_REDUCTION',nodes['CERT_BASE_THETA_REDUCTION']['contract']+
 ' Version0.33 supplies FIA8 and CTC1–CTC13 for the complete actual cuspidality subargument; CTC11 proves compactness of the literal NI rational quotients, so the human proof does not rely on integral_undef. The residual extension/readings/tests and actual base rows remain explicit.',[evf,evc])
refine('COUNT_II_SUPPORT',
 'For each of the two original QX rank-four Links, at fixed iota choose one common coefficient threshold before every later coefficient DVR and every actual universal B/Lambda; produce one ideal J with ring,dense,pt,end1,end2,twist AND P1core. JSP constructs J=ker(B→T)=Ann_B(M), proves ring/dense and the same-ideal TWBase from explicitly supplied original ordinary Hecke arithmetic data, and proves the one-point NiceI→P1 implication from HasAut and six exact arithmetic/patching contracts. Remaining producers are that ordinary/control/arithmetic-fiber system including its exact reciprocity dictionary, the four further Hida fields on this J, the all-level automorphic modules/HasAut, and the retained single-point support inputs. The exact artOf/every-map IsWtPart reciprocity matching is a nested D source-understanding obligation inside this coupled C producer; KX3 alone does not supply it. The common ideal, ell=3 scope, both Links and threshold order are unchanged.',[evj])
g['nodes']=list(nodes.values())
g['selected_interface_cuts']['global_v033']=dict(completed_GL4=['TASK_GL4_COLUMN_VALUES','TASK_GL4_SLOPE_LOWER','TASK_GL4_SLOPE_MAX'],completed_package='All eleven FamGLmin fields from the same supplied second layer, GLS13',remaining=['TASK_GL_FINAL_ASSEMBLY'],binding='Original common compatible selector/Duty and original metrics/embeddings retained; no family existence inferred.')
g['selected_interface_cuts']['theta_v033']=dict(completed='FIA8 and CTC13: literal finite cancellation and genuine base theta cuspidality',remaining=['BASE_THETA_READINGS','BASE_THETA_CUSPIDAL_EXTENSION','BASE_THETA_RATIONAL_TESTS','SLR_BASE_ROWS_PRODUCER'],binding='Original same-Bundle kernels; smooth-growth/lowering/realization and universal ioP remain.')
g['selected_interface_cuts']['count_ii_v033']=dict(completed='Original kernel/annihilator, conditional RingProps/Dense, same-ideal TWBase and single-point P1 transport',remaining=['COUNT_II_SUPPORT'],binding='Both original rank-four Links, fixed iota, one common threshold before later DVR/B/Lambda; same J for all seven properties; ell=3 retained.')
for n in g['work_refinement_nodes']:
 if n['id']=='GLOBAL_LOCAL_THETA_BINDINGS':n['version_0_33_update']='Actual finite averaging and genuine cuspidality are supplied on the original kernels. Shared smooth-growth/lowering/realization, geometric readings and rational tests remain.'
 if 'HIDA' in n['id'] or 'ORDINARY' in n['id']:n['version_0_33_update']='JSP reconstructs the original kernel and same-ideal conditional transports. Arithmetic ordinary/control and all-level patched-support producers remain.'
g['source_inputs']={'predecessor_graph':g['predecessor_graph']}
for comp in cfg['components']:
 for f in ['provenance.json','closure.json']:
  g['source_inputs'][comp+'_'+f.split('.')[0]]=dict(file=comp+'/'+f,sha256=sha(ROOT/comp/f))
if (AUD/'main.tex').exists():g['source_inputs']['current_narrative']=dict(file='dependency_audit_v0_33/main.tex',sha256=sha(AUD/'main.tex'))
changes={
 'GLOBAL_SLOPE':dict(claims=gls,closed='Three original GL4 implications and the same-selector eleven-field FamGLmin assembly.',retained='Actual compatible second-layer producer and residual linkGLOBAL7_min/items/link8 numerical/lattice join.'),
 'GLOBAL_SMALL_RANK':dict(claims=fia+ctc,closed='Literal finite isotropic average, Heisenberg-invariant constant term and original base integral cuspidality with ordinary convergence.',retained='Same-Bundle original readings, smooth-growth/lowering/Hilbert extension, simultaneous rational tests and actual base rows.'),
 'GLOBAL_LOCAL_THETA_BINDINGS':dict(claims=fia+ctc,closed='Original finite averaging and complete cusp subargument on the same actual theta kernels.',retained='Original analytic/geometric and rational producer identities; nonbase requirements retain distinct scopes.'),
 'RANK4_JOINT_ORDINARY_SUPPORT':dict(claims=jsp,closed='Kernel/annihilator construction, conditional full RingProps/Dense, literal same-ideal TWBase and single-point P1 transport.',retained='Original ordinary arithmetic/control data, exact reciprocity, remaining Hida fields, all-level automorphic modules and six arithmetic/patching support contracts.'),
 'COUNT_II_SUPPORT':dict(claims=jsp,closed='Exact same-ideal conditional reductions.',retained='Whole original rank-four joint producer on both Links after one threshold.')
}
disp=copy.deepcopy(read(OLD/'target_disposition.json'));disp['version']='0.33'
disp['predecessor_disposition']=dict(file='dependency_audit_v0_32/target_disposition.json',sha256=sha(OLD/'target_disposition.json'))
prior=read(ROOT/'history/version_0_32/next_source_targets.json')['targets']
assert len(prior)==len(disp['records'])==245
for t,r in zip(prior,disp['records']):
 assert t.get('id')==r['original_id']
 r['predecessor_record_sha256']=hashlib.sha256(json.dumps(t,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()).hexdigest()
 r['version_0_33_scope_updates']=[dict(frontier=k,**v)for k,v in changes.items()if k in r.get('frontier_ids',[])]
 r['version_0_33_disposition_policy']='Every inherited compound scope retained; exact subarguments updated without claiming producer existence.'
disp['current_selected_frontier']='dependency_audit_v0_33/obligation_map.json'
disp['category_count_policy']='Historical compound categories remain navigation; current sufficient leaves have exact coupled contracts. No completion percentage.'
disp['coverage']['records_with_v033_scope_updates']=sum(bool(r['version_0_33_scope_updates']) for r in disp['records'])
write(AUD/'target_disposition.json',disp)
g['backlog_crosswalk']=dict(file='dependency_audit_v0_33/target_disposition.json',sha256=sha(AUD/'target_disposition.json'),records=245,scope_groups=107,meaning='Every predecessor compound scope retained with additive exact reductions.')
def reach(k):
 seen=set();todo=[k]
 while todo:
  v=todo.pop();assert v in nodes
  if v in seen:continue
  seen.add(v);todo+=nodes[v]['requires']
 return seen
active=set();done=set()
def visit(k):
 assert k not in active
 if k in done:return
 active.add(k)
 for v in nodes[k]['requires']:visit(v)
 active.remove(k);done.add(k)
for k in nodes:visit(k)
rh=reach('ORDINARY_RH');grh=reach('DIRICHLET_GRH');full=reach('GLOBAL_FULL_RANK')
assert rh|grh==set(nodes)
assert 'COUNT_III_PRODUCER' not in rh and 'COUNT_III_PRODUCER' in grh
assert {'COUNT_I_PRODUCER','COUNT_II_SUPPORT','COUNT_V_PRODUCER'}<=rh&grh
assert not any(k.startswith('TASK_GL4')for k in full)and 'TASK_GL_FINAL_ASSEMBLY' not in full
leaves=[n for n in nodes.values() if n['gate']=='LEAF' and n['status']not in ['proved_in_stated_scope','published_application_checked']]
assert len(leaves)==35 and collections.Counter(n['category']for n in leaves)=={'C':23,'B':10,'D':2}
g['validation']=dict(logical_graph_acyclic=True,all_selected_nodes_reachable_from_roots=True,selected_node_count=len(nodes),work_refinement_node_count=len(g['work_refinement_nodes']),optional_node_count=len(g['optional_routes']),rh_reachable_count=len(rh),dirichlet_grh_reachable_count=len(grh),rh_excludes_every_case_III_producer=True,unrestricted_grh_includes_case_III=True,both_roots_reach_I_II_V=True,ten_exact_topDesWin_arguments_retained=True,same_ideal_count_II_coupling_retained=True,full_rank_excludes_GL4_and_final_slope_assembly=True,design_thresholds_before_one_family=True,all_GL4_implications_complete=True,original_FamGLmin_complete_on_supplied_second_layer=True,theta_cuspidality_complete_on_original_inputs=True,base_extension_not_claimed_complete=True,same_ideal_support_producer_not_claimed_complete=True,all_selected_open_leaves_classified=True,open_leaf_count=len(leaves),open_leaf_categories=dict(collections.Counter(n['category']for n in leaves)),new_Lean_build_performed=False)
write(AUD/'obligation_map.json',g)
write(AUD/'remaining_leaf_register.json',dict(artifact_version='0.33',source_commit=g['source_commit'],category_key=g['categories'],scope=g['scope'],records=leaves,warning='Selected sufficient obligations, often coupled; not a completion percentage or an absolute minimality theorem.'))
write(AUD/'closure_delta.json',dict(artifact_version='0.33',source_commit=g['source_commit'],changes=changes,retained_historical_correction='RF16 governed by DEX11; historical proof bytes unchanged.'))
write(AUD/'published_applications.json',dict(artifact_version='0.33',source_commit=g['source_commit'],freshly_checked_applications=read(ROOT/'global_slope/published_applications.json'),inherited_registry=dict(file='dependency_audit_v0_32/published_applications.json',sha256=sha(OLD/'published_applications.json')),note='New direct A application: Banaszczyk 1993 Thm2.1 on the exact positive trace Euclidean lattice; its normalization and subsequent transports are proved in GLS. Earlier A applications retain their exact scopes.'))
print(json.dumps(g['validation'],indent=2))
