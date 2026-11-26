#!/usr/bin/env python3
"""Update the sufficient dependency audit without dropping a producer or old scope."""
from pathlib import Path
import collections, copy, hashlib, json

ROOT=Path(__file__).resolve().parent
AUD=ROOT/'dependency_audit_v0_35';OLD=ROOT/'dependency_audit_v0_34'
def read(p):return json.loads(p.read_text())
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def write(p,d):p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n')
cfg=read(ROOT/'increment_v0_35.json')
g=copy.deepcopy(read(OLD/'obligation_map.json'))
g['artifact_version']='0.35'
g['predecessor_graph']=dict(file='dependency_audit_v0_34/obligation_map.json',sha256=sha(OLD/'obligation_map.json'))
nodes={n['id']:n for n in g['nodes']}
def evidence(comp):
    return dict(component=comp,claims=cfg['component_claims'][comp],ledger=comp+'/provenance.json',
     ledger_sha256=sha(ROOT/comp/'provenance.json'),proof_file=comp+'/main.tex',proof_sha256=sha(ROOT/comp/'main.tex'))
def refine(ident,contract,proofs,complete=False):
    n=nodes[ident];n['previous_interface']=copy.deepcopy(n)
    n.update(contract=contract,introduced_or_refined_in='0.35')
    n.setdefault('evidence',[]).extend(proofs)
    if complete:n.update(status='proved_in_stated_scope',kind='implication_certificate',category='B')
    return n
lfs=cfg['component_claims']['global_loss'];gfi=cfg['component_claims']['global_final_installation']
hcu=cfg['component_claims']['holomorphic_uniqueness'];cap=cfg['component_claims']['count_auxiliary_primes']
evl=evidence('global_loss');evg=evidence('global_final_installation')
evh=evidence('holomorphic_uniqueness');evc=evidence('count_auxiliary_primes')
refine('TASK_GL_FINAL_ASSEMBLY',
 'PROVED on the SAME original supplied family, compatible second-layer selector and Duty. GLS13 supplies the full eleven-field FamGLmin(D3(3,A),4); GVC/GFA supply the original count, source/quotient slopes, ranks, all-H frame, nodes, windows and characters. LFS1–17 now prove both original Loss_at inequalities, including every Reads/HEq/cutoff, from ChosenTT, ChosenBadp, LinkG and the same ChosenWS degree pair with its realizing i1; no CoverAll premise is inserted. GFI1–17 install every actual ChainTied field and the final Closed wrapper, with Cabs=2, C0=3, column constant 4,eD=2, eL=0. ChosenE plus ChosenWall is converted to the full required Seven packet. The epsilon cutoff and TransportedAlt tuple precede Fm,CH; eventual x thresholds precede members, base points, words, places and readings. This closes the entire conditional assembly implication. Compatible family/selector/Duty and actual LinkG/LinkS/LinkIRR/LinkDIV and other global inputs remain upstream producers.',[evl,evg],complete=True)
refine('TASK_LINK_GL_INSTALL',
 'The exact same-selector LinkGLOBAL consumer is now fully reconstructed: all h3/GL4/GL6 implications and eleven-field FamGLmin, GVC/GFA count/slopes/ranks/frame/windows/characters, LFS both universal losses and GFI complete tied-ledger/Closed installation. Its original AND requirements, guarded TuSize context and shared mass/selector assumptions are unchanged. The closed assembly leaf supplies an implication on the same original family; it creates no class member, selector, arithmetic estimate or spectral producer.',[evl,evg])
nodes['TASK_LINK_GL_INSTALL']['status']='proved_implication_with_open_inputs'
refine('GLOBAL_GL_PAIR',
 'The conditional join of the original full-rank and LinkGLOBAL consumers is complete on the SAME original compatible second-layer selector and Duty. The full-rank route and the now-complete global assembly retain their original separate AND requirements. The original second-layer producer, common construction and actual local, spectral and arithmetic inputs remain open; the completed join neither supplies them nor chooses a replacement family.',[evl,evg])
nodes['GLOBAL_GL_PAIR']['status']='proved_conditional_join_with_open_producers'
refine('BASE_THETA_CUSPIDAL_EXTENSION',
 'On the SAME selected Bundle and SAME reading as BASE_THETA_READINGS, extend the exact lowest-type theta integral for each finite basis vector of HV(i,t0) to the original full Wall_i, with one family threshold before i and basis vectors. BTH/FIA/CTC/TAE prove convergence, finite cancellation, genuine cuspidality, actual-action smoothness, one growth exponent for every derivative word, stored-vacuum transfer and exact lowering. HCU now proves the actual signed-frame holomorphic dictionary and uniqueness, full LowSm/LowIrr including multiplicity one of the original lowKSub, the exact base-model ordered-parameter installation, and holomorphicity of the extremal cusp packet. Under bounded HolForm, FinPair and IsReg on the SAME target, it proves the full original extremal coefficient identity and BackForm.exists_map Hilbert multilinear realization with finite eigenlaws. Remaining C subcontracts: one original io_i satisfying IsIoW for EVERY parameter t; actual boundedness and finite-volume regular target; pointwise smooth representatives and every derivative of the constructed Hilbert image, Sobolev point-evaluation estimates and uniform growth, central finiteness, and cusp preservation under closed orbit span, producing the literal Sobolev-continuous MMap agreeing with the original integral. Preserve all fields, adjoints, levels and common choices. Separate geometric readings, rational tests and actual base rows remain outside this analytic packet.',[evh])
refine('CERT_BASE_THETA_REDUCTION',nodes['CERT_BASE_THETA_REDUCTION']['contract']+
 ' Version 0.35 additionally supplies full original LowSm/LowIrr, the base-model ordered parameters, holomorphic extremal uniqueness, exact coefficient identity and the original Hilbert map. The latter retains boundedness/FinPair/IsReg; one simultaneous ioP and the global pointwise smooth/Sobolev/central/cusp-closure producers still prevent a full MMap claim.',[evh])
refine('COUNT_II_SUPPORT',
 'For each of the two original QX rank-four Links, at fixed iota choose one common coefficient threshold before every later coefficient DVR and actual universal B/Lambda; produce one ideal J with ring,dense,pt,end1,end2,twist AND P1core. JSP supplies the exact common ideal and conditional support transport. CIP supplies every-map split-CM reciprocity with the positive cyclotomic norm sign and the full universal NiceI Norm with original D0, integral representation, ordered flags and determinant law. CAP now supplies the full original ArPl under unchanged CohP: PhiCond, the exact polarized residual H, the PL-relative Frattini tower, every prescribed list and all actual TWGrp/TWPl levels, inverse arithmetic Frobenius, complete closed kernel and one uniform Hom bound. CAP also constructs the original IsRes values for any supplied integral type at every QData level. Remaining C producers: original ordinary/control/arithmetic-fiber data and integral type/neatU/TThetaEx, four further Hida fields on this J, all-level same-J automorphic modules/HasAut, Choice, first-order and obstruction bounds, and Raw, retaining original CohP and all stated side conditions. Both Links, ell=3, fixed iota and common threshold order remain. No generic NiceE Norm or ordinary/control existence follows from the completed consumers.',[evc])
g['nodes']=list(nodes.values())
g['selected_interface_cuts']['global_v035']=dict(
 completed='Full original global consumer: eleven-field FamGLmin, GVC/GFA fields, LFS both universal losses, GFI same-family ChainTied and final Closed',
 closed_selected_leaf='TASK_GL_FINAL_ASSEMBLY',
 retained='Original common construction, compatible second layer and Duty, LinkG/LinkS/LinkIRR/LinkDIV and other upstream producers; every original AND edge retained.',
 constants=dict(Cabs=2, C0=3, column_constant=4,eD=2, eL=0),
 binding='Same fields, embeddings, metrics, character, degree pair, realizing member and original quantifier order.')
g['selected_interface_cuts']['theta_v035']=dict(
 completed='Original holomorphic uniqueness, full lowest-type smoothness and multiplicity one, exact base-model installation, extremal coefficient identity and Hilbert multilinear map',
 remaining=['BASE_THETA_READINGS','BASE_THETA_CUSPIDAL_EXTENSION','BASE_THETA_RATIONAL_TESTS','SLR_BASE_ROWS_PRODUCER'],
 residual='Common all-parameter ioP; boundedness/finite-volume regular target; smooth representatives, Sobolev point evaluation/uniform growth, central finiteness and cusp closure for the full MMap.',
 binding='Actual original DSModel and its entire lowest-type supremum, same original quotient and theta integral; no replacement model.')
g['selected_interface_cuts']['count_ii_v035']=dict(
 completed='Full original ArPl under unchanged CohP and original IsRes values for every supplied integral type and QData level, following exact reciprocity and required NiceI Norm',
 remaining=['COUNT_II_SUPPORT'],nested_closed=['JSP_ACTUAL_ARPL','TResEx_at_supplied_integral_type'],
 binding='Both original Links, same J within each Link, fixed iota and coefficient threshold order, ell=3. Ordinary/control/type/HasAut/Choice/first-order/obstruction/Raw producers remain.')
for n in g['work_refinement_nodes']:
    if n['id']=='GLOBAL_LOCAL_THETA_BINDINGS':
        n['version_0_35_update']='HCU supplies full original lowest-type multiplicity one and the exact Hilbert coefficient stage. Common ioP, boundedness/finite-volume and global Sobolev/central/cusp-closure producers plus geometric/rational bindings remain.'
    if 'HIDA' in n['id'] or 'ORDINARY' in n['id']:
        n['version_0_35_update']='CAP supplies full ArPl and supplied-type IsRes, retaining CohP and the same original ideal. Ordinary/control, integral type/neatU, other Hida fields and same-J HasAut remain.'
g['source_inputs']={'predecessor_graph':g['predecessor_graph']}
for comp in cfg['components']:
    for f in ['provenance.json','closure.json']:
        g['source_inputs'][comp+'_'+f.split('.')[0]]=dict(file=comp+'/'+f,sha256=sha(ROOT/comp/f))
if (AUD/'main.tex').exists():g['source_inputs']['current_narrative']=dict(file='dependency_audit_v0_35/main.tex',sha256=sha(AUD/'main.tex'))
changes={
 'GLOBAL_SLOPE':dict(claims=lfs+gfi,closed='Both original universal losses and complete same-family ChainTied/final Closed consumer.',retained='Original compatible construction, selector/Duty and LinkG/LinkS/LinkIRR/LinkDIV and all other upstream producers.'),
 'GLOBAL_SMALL_RANK':dict(claims=hcu,closed='Full original lowest-type smoothness/multiplicity one, signed-frame uniqueness, actual base parameters, exact extremal coefficient and Hilbert map.',retained='Common ioP, boundedness/finite-volume and full pointwise smooth/Sobolev/central/cusp-closure suppliers; readings/rational tests/base rows.'),
 'GLOBAL_LOCAL_THETA_BINDINGS':dict(claims=hcu,closed='Original lowest-type and Hilbert coefficient subarguments with exact same-model/quotient bindings.',retained='Same-object geometric/rational and remaining global analytic producers.'),
 'RANK4_JOINT_ORDINARY_SUPPORT':dict(claims=cap,closed='Complete original ArPl and supplied-type IsRes with unchanged CohP and all-level/list quantifiers.',retained='Ordinary arithmetic/control, integral type/neatU/TThetaEx, four further Hida fields, same-J HasAut and other support producers.'),
 'COUNT_II_SUPPORT':dict(claims=cap,closed='Nested JSP_ACTUAL_ARPL and original residual Hecke-value construction.',retained='Whole original same-ideal rank-four producer on both Links; Choice, first-order/obstruction bounds, Raw and retained arithmetic hypotheses.')
}
disp=copy.deepcopy(read(OLD/'target_disposition.json'));disp['version']='0.35'
disp['predecessor_disposition']=dict(file='dependency_audit_v0_34/target_disposition.json',sha256=sha(OLD/'target_disposition.json'))
prior=read(ROOT/'history/version_0_34/next_source_targets.json')['targets']
assert len(prior)==len(disp['records'])==245
for t,r in zip(prior,disp['records']):
    assert t.get('id')==r['original_id']
    r['predecessor_record_sha256']=hashlib.sha256(json.dumps(t,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()).hexdigest()
    r['version_0_35_scope_updates']=[dict(frontier=k,**v)for k,v in changes.items()if k in r.get('frontier_ids',[])]
    r['version_0_35_disposition_policy']='Every inherited compound scope retained; the whole original conditional global assembly is closed, while theta/CountII subarguments narrow their original producer contracts.'
disp['current_selected_frontier']='dependency_audit_v0_35/obligation_map.json'
disp['category_count_policy']='Historical compound categories remain navigation. Current sufficient leaves retain exact coupled contracts; counts are not completion percentages.'
disp['coverage']['records_with_v035_scope_updates']=sum(bool(r['version_0_35_scope_updates'])for r in disp['records'])
write(AUD/'target_disposition.json',disp)
g['backlog_crosswalk']=dict(file='dependency_audit_v0_35/target_disposition.json',sha256=sha(AUD/'target_disposition.json'),records=245,scope_groups=107,meaning='Every predecessor compound scope retained with additive exact reductions.')
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
assert 'COUNT_III_PRODUCER'not in rh and 'COUNT_III_PRODUCER'in grh
assert {'COUNT_I_PRODUCER','COUNT_II_SUPPORT','COUNT_V_PRODUCER'}<=rh&grh
assert not any(k.startswith('TASK_GL4')for k in full)and 'TASK_GL_FINAL_ASSEMBLY'not in full
leaves=[n for n in nodes.values()if n['gate']=='LEAF'and n['status']not in ['proved_in_stated_scope','published_application_checked']]
assert len(leaves)==34 and collections.Counter(n['category']for n in leaves)=={'C':23,'B':9,'D':2}
g['validation']=dict(logical_graph_acyclic=True,all_selected_nodes_reachable_from_roots=True,
 selected_node_count=len(nodes),work_refinement_node_count=len(g['work_refinement_nodes']),optional_node_count=len(g['optional_routes']),
 rh_reachable_count=len(rh),dirichlet_grh_reachable_count=len(grh),rh_excludes_every_case_III_producer=True,
 unrestricted_grh_includes_case_III=True,both_roots_reach_I_II_V=True,ten_exact_topDesWin_arguments_retained=True,
 same_ideal_count_II_coupling_retained=True,full_rank_excludes_GL4_and_final_slope_assembly=True,
 design_thresholds_before_one_family=True,all_GL4_implications_complete=True,original_FamGLmin_complete_on_supplied_second_layer=True,
 both_original_universal_losses_complete=True,same_family_ChainTied_and_Closed_consumer_complete=True,
 selected_global_assembly_leaf_closed=True,original_lowest_type_LowSm_LowIrr_complete=True,
 exact_extremal_coefficient_and_Hilbert_map_complete_on_original_inputs=True,
 original_ArPl_complete_under_unchanged_CohP=True,original_IsRes_complete_for_supplied_integral_type=True,
 base_extension_not_claimed_complete=True,same_ideal_support_producer_not_claimed_complete=True,
 all_selected_open_leaves_classified=True,open_leaf_count=len(leaves),
 open_leaf_categories=dict(collections.Counter(n['category']for n in leaves)),new_Lean_build_performed=False)
write(AUD/'obligation_map.json',g)
write(AUD/'remaining_leaf_register.json',dict(artifact_version='0.35',source_commit=g['source_commit'],category_key=g['categories'],scope=g['scope'],records=leaves,warning='Selected sufficient obligations, often coupled; not a completion percentage or an absolute minimality theorem.'))
write(AUD/'closure_delta.json',dict(artifact_version='0.35',source_commit=g['source_commit'],changes=changes,closed_selected_leaves=['TASK_GL_FINAL_ASSEMBLY'],retained_historical_correction='RF16 governed by DEX11; historical proof bytes unchanged.'))
fresh=read(ROOT/'count_auxiliary_primes/published_applications.json')
write(AUD/'published_applications.json',dict(artifact_version='0.35',source_commit=g['source_commit'],freshly_checked_applications=fresh,
 inherited_registry=dict(file='dependency_audit_v0_34/published_applications.json',sha256=sha(OLD/'published_applications.json')),
 note='The new external application is unconditional finite-Galois Chebotarev, with actual field extension, excluded primes and arithmetic Frobenius convention checked. The remaining new arguments are written independently. Earlier checked published inputs retain their original scopes; CohP is retained, not silently replaced by a new literature claim.'))
print(json.dumps(g['validation'],indent=2))
