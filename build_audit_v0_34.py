#!/usr/bin/env python3
"""Update the complete selected audit while preserving predecessor scopes."""
from pathlib import Path
import copy,hashlib,json,collections
ROOT=Path(__file__).resolve().parent;AUD=ROOT/'dependency_audit_v0_34';OLD=ROOT/'dependency_audit_v0_33'
def read(p):return json.loads(p.read_text())
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def write(p,d):p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n')
cfg=read(ROOT/'increment_v0_34.json');g=copy.deepcopy(read(OLD/'obligation_map.json'))
g['artifact_version']='0.34';g['predecessor_graph']=dict(file='dependency_audit_v0_33/obligation_map.json',sha256=sha(OLD/'obligation_map.json'))
nodes={n['id']:n for n in g['nodes']}
def evidence(comp,ids):return dict(component=comp,claims=ids,ledger=comp+'/provenance.json',ledger_sha256=sha(ROOT/comp/'provenance.json'),proof_file=comp+'/main.tex',proof_sha256=sha(ROOT/comp/'main.tex'))
def refine(ident,contract,proofs,complete=False):
    n=nodes[ident];prev=copy.deepcopy(n);n['previous_interface']=prev
    n.update(contract=contract,introduced_or_refined_in='0.34')
    n.setdefault('evidence',[]).extend(proofs)
    if complete:n.update(status='proved_in_stated_scope',kind='implication_certificate',category='B')
    return n
gvc=cfg['component_claims']['global_count'];gfa=cfg['component_claims']['global_assembly'];tae=cfg['component_claims']['theta_extension'];cip=cfg['component_claims']['count_ii_producer']
evv=evidence('global_count',gvc);evg=evidence('global_assembly',gfa);evt=evidence('theta_extension',tae);evp=evidence('count_ii_producer',cip)
refine('TASK_GL_FINAL_ASSEMBLY',
 'On the SAME original supplied family, compatible second-layer selector and Duty, GLS13 gives the full eleven-field FamGLmin(D3(3,A),4). GVC now supplies literal CountF and SlopesMF, using the logarithmic-derivative size already projected from FamP.sizes; GFA supplies LevelTFamily with constant36, PlacesF/SlopesNF with original metrics/support, positive RRRankF/LatF, the literal all-H FrameF, NodesF, every Win_at clause and exact CharF. Remaining B work: prove original LossFS(Fm,0) from the chosen small shares and weights, then install the actual same-family linkCore/ChainTied ledger and final Closed wrapper with Cabs=2,C0=3,C5=4,eD=2,eL=0. Keep original top/bottom values, characters, all ledger fields and thresholds. The epsilon cutoff and TransportedAlt tuple precede Fm,CH; the eventual x threshold precedes i,u and places. Compatible family/selector existence and LinkG/LinkS/LinkIRR/LinkDIV remain upstream producers.',[evv,evg])
refine('TASK_LINK_GL_INSTALL',
 'All h3, GL4 and GL6 implications and the same-selector eleven-field FamGLmin packet remain complete. GVC/GFA now reconstruct the exact count, slopes, positive-rank, all-H frame, node, window and character consumers. Only original LossFS(Fm,0), the exact same-family linkCore/ChainTied installation and final Closed wrapper remain inside the global assembly leaf. The original AND requirements and shared mass/selector context are unchanged; no compatible class member or producer input is inferred.',[evv,evg])
refine('BASE_THETA_CUSPIDAL_EXTENSION',
 'On the SAME selected Bundle and SAME reading as BASE_THETA_READINGS, extend the exact lowest-type theta integral for each finite basis vector of HV(i,t0) to the original Wall_i, with one family threshold before i and basis vectors. BTH3/FIA/CTC prove convergence, finite cancellation and genuine cuspidality. TAE1–13 now prove actual-action smoothness, uniform growth with one exponent for every derivative word, dominated differentiation, stored-vacuum transfer, exact lowering, finite-level and compact-equivariance installation; given the following producer premises this gives the literal IsHolCuspKMap. Remaining C subcontracts: one original io_i satisfying IsIoW for EVERY parameter t; LowSm and LowIrr for the full original lowKSub (including multiplicity one); boundedness and finite-volume target input; the exact extremal coefficient identity and Sobolev-continuous Hilbert multiplicity-map realization agreeing with the given integral. Keep all original fields, adjoints, levels and common choices. Separate geometric readings, rational tests and actual base rows are not supplied by this analytic packet.',[evt])
refine('CERT_BASE_THETA_REDUCTION',nodes['CERT_BASE_THETA_REDUCTION']['contract']+
 ' Version0.34 supplies the original smooth-growth/lowering analytic packet in TAE1–13. One simultaneous ioP, full-lowest-type smooth irreducibility, boundedness and actual Hilbert multiplicity realization remain producer contracts; the completed packet is not itself an MMap.',[evt])
refine('COUNT_II_SUPPORT',
 'For each of the two original QX rank-four Links, at fixed iota choose one common coefficient threshold before every later coefficient DVR and actual universal B/Lambda; produce one ideal J with ring,dense,pt,end1,end2,twist AND P1core. JSP constructs the exact common Hecke-kernel/annihilator ideal and conditional RingProps/Dense/TWBase and the one-point NiceI transport. CIP now proves exact source reciprocity at the original split CM places for every IsLocalArtin and every admissible global map, with the positive cyclotomic norm sign, and the full universal NiceI instance of Norm used by that transport, preserving the original D0, integral representation, ordered flags and determinant law. Remaining C producers: original ordinary/control/arithmetic-fiber data, the four further Hida fields on this J, all-level same-J automorphic modules/HasAut, and Choice, ArPl, first-order and obstruction bounds, and Raw, with original CohP and stated side conditions. Both Links, ell=3 and common threshold order remain. Generic NiceE Norm is not claimed; the nested reciprocity-understanding obligation is closed in its full required scope.',[evp])
g['nodes']=list(nodes.values())
g['selected_interface_cuts']['global_v034']=dict(completed_package='GLS13 same-selector FamGLmin plus GVC CountF/SlopesMF and GFA quotient/rank/frame/node/window/character consumers',remaining=['TASK_GL_FINAL_ASSEMBLY'],residual='LossFS(Fm,0), same-family linkCore/ChainTied and final Closed wrapper',binding='Original common selector/Duty, LinkG/LinkS/LinkIRR/LinkDIV, fields, embeddings and metrics retained; no producer existence inferred.')
g['selected_interface_cuts']['theta_v034']=dict(completed='TAE1–13 actual-action smoothness, unchanged all-word growth exponent, dominated differentiation, stored-vacuum transfer and exact lowering; conditional IsHolCuspKMap',remaining=['BASE_THETA_READINGS','BASE_THETA_CUSPIDAL_EXTENSION','BASE_THETA_RATIONAL_TESTS','SLR_BASE_ROWS_PRODUCER'],residual='Common all-parameter ioP; full-lowest-type LowSm/LowIrr; boundedness/finite volume; original extremal coefficient/Hilbert multiplicity realization',binding='Same original R and every original theta vector/kernel/map retained.')
g['selected_interface_cuts']['count_ii_v034']=dict(completed='Exact every-map reciprocity in the original split-CM scope and full universal NiceI Norm with old D0',remaining=['COUNT_II_SUPPORT'],nested_closed=['JSP_EXACT_RECIPROCITY_MATCH','JSP_SINGLE_POINT_NORM_at_NiceI'],binding='Both original Links, fixed iota, same J and original threshold order, ell=3; other ordinary/control and patched-support producers remain.')
for n in g['work_refinement_nodes']:
 if n['id']=='GLOBAL_LOCAL_THETA_BINDINGS':n['version_0_34_update']='TAE closes actual smoothness, all-word uniform growth and lowering. Common ioP, LowSm/LowIrr, Hilbert realization, geometric readings and rational tests remain.'
 if 'HIDA' in n['id'] or 'ORDINARY' in n['id']:n['version_0_34_update']='CIP closes exact reciprocity and the full required NiceI normalization on the original same-ideal route. Ordinary arithmetic/control, other Hida fields, same-J HasAut and other support inputs remain.'
g['source_inputs']={'predecessor_graph':g['predecessor_graph']}
for comp in cfg['components']:
 for f in ['provenance.json','closure.json']:
  g['source_inputs'][comp+'_'+f.split('.')[0]]=dict(file=comp+'/'+f,sha256=sha(ROOT/comp/f))
if (AUD/'main.tex').exists():g['source_inputs']['current_narrative']=dict(file='dependency_audit_v0_34/main.tex',sha256=sha(AUD/'main.tex'))
changes={
 'GLOBAL_SLOPE':dict(claims=gvc+gfa,closed='Exact CountF, SlopesMF, LevelTFamily, PlacesF/SlopesNF, RRRankF/LatF, all-H FrameF, NodesF/WinF/CharF consumers.',retained='Original same-family producer inputs and residual LossFS(Fm,0), tied-ledger and Closed installation.'),
 'GLOBAL_SMALL_RANK':dict(claims=tae,closed='Original smoothness, all-word growth, dominated integral derivatives, vacuum transfer and exact lowering; conditional full analytic/cusp lowest-type packet.',retained='Common ioP, full-lowest-type LowSm/LowIrr, boundedness and Hilbert multiplicity realization; same-Bundle readings/tests and actual base rows.'),
 'GLOBAL_LOCAL_THETA_BINDINGS':dict(claims=tae,closed='Analytic and lowering subarguments on original theta kernels.',retained='Same-object analytic/geometric and rational producer identities.'),
 'RANK4_JOINT_ORDINARY_SUPPORT':dict(claims=cip,closed='Every-map exact reciprocity in required split-CM scope and full universal NiceI Norm with original D0.',retained='Ordinary arithmetic/control, four further Hida fields, same-J all-level HasAut and other support inputs.'),
 'COUNT_II_SUPPORT':dict(claims=cip,closed='Nested JSP exact reciprocity understanding task and required irreducible-point normalization.',retained='Whole original rank-four joint producer on both Links; no generic NiceE normalization claim.')
}
disp=copy.deepcopy(read(OLD/'target_disposition.json'));disp['version']='0.34'
disp['predecessor_disposition']=dict(file='dependency_audit_v0_33/target_disposition.json',sha256=sha(OLD/'target_disposition.json'))
prior=read(ROOT/'history/version_0_33/next_source_targets.json')['targets']
assert len(prior)==len(disp['records'])==245
for t,r in zip(prior,disp['records']):
 assert t.get('id')==r['original_id']
 r['predecessor_record_sha256']=hashlib.sha256(json.dumps(t,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()).hexdigest()
 r['version_0_34_scope_updates']=[dict(frontier=k,**v)for k,v in changes.items()if k in r.get('frontier_ids',[])]
 r['version_0_34_disposition_policy']='Every inherited compound scope retained; exact subarguments updated without claiming producer existence.'
disp['current_selected_frontier']='dependency_audit_v0_34/obligation_map.json'
disp['category_count_policy']='Historical compound categories remain navigation; current sufficient leaves have exact coupled contracts. No completion percentage.'
disp['coverage']['records_with_v034_scope_updates']=sum(bool(r['version_0_34_scope_updates']) for r in disp['records'])
write(AUD/'target_disposition.json',disp)
g['backlog_crosswalk']=dict(file='dependency_audit_v0_34/target_disposition.json',sha256=sha(AUD/'target_disposition.json'),records=245,scope_groups=107,meaning='Every predecessor compound scope retained with additive exact reductions.')
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
g['validation']=dict(logical_graph_acyclic=True,all_selected_nodes_reachable_from_roots=True,selected_node_count=len(nodes),work_refinement_node_count=len(g['work_refinement_nodes']),optional_node_count=len(g['optional_routes']),rh_reachable_count=len(rh),dirichlet_grh_reachable_count=len(grh),rh_excludes_every_case_III_producer=True,unrestricted_grh_includes_case_III=True,both_roots_reach_I_II_V=True,ten_exact_topDesWin_arguments_retained=True,same_ideal_count_II_coupling_retained=True,full_rank_excludes_GL4_and_final_slope_assembly=True,design_thresholds_before_one_family=True,all_GL4_implications_complete=True,original_FamGLmin_complete_on_supplied_second_layer=True,theta_cuspidality_complete_on_original_inputs=True,theta_smooth_growth_lowering_complete=True,global_count_frame_windows_characters_complete=True,exact_split_CM_reciprocity_match_complete=True,required_universal_NiceI_Norm_complete=True,base_extension_not_claimed_complete=True,same_ideal_support_producer_not_claimed_complete=True,all_selected_open_leaves_classified=True,open_leaf_count=len(leaves),open_leaf_categories=dict(collections.Counter(n['category']for n in leaves)),new_Lean_build_performed=False)
write(AUD/'obligation_map.json',g)
write(AUD/'remaining_leaf_register.json',dict(artifact_version='0.34',source_commit=g['source_commit'],category_key=g['categories'],scope=g['scope'],records=leaves,warning='Selected sufficient obligations, often coupled; not a completion percentage or an absolute minimality theorem.'))
write(AUD/'closure_delta.json',dict(artifact_version='0.34',source_commit=g['source_commit'],changes=changes,retained_historical_correction='RF16 governed by DEX11; historical proof bytes unchanged.'))
write(AUD/'published_applications.json',dict(artifact_version='0.34',source_commit=g['source_commit'],freshly_checked_applications=read(ROOT/'count_ii_producer/published_applications.json'),inherited_registry=dict(file='dependency_audit_v0_33/published_applications.json',sha256=sha(OLD/'published_applications.json')),note='Three explicit applications of classical local/global class field theory and norm compatibility in Milne version4.03. CIP independently proves every-map matching, split-CM unit injectivity and the exact cyclotomic sign. No new published theorem is imported in GVC/GFA/TAE. All earlier A applications remain available in their exact scopes.'))
print(json.dumps(g['validation'],indent=2))
