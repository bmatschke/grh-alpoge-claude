#!/usr/bin/env python3
"""Refine exact selected contracts while preserving every original logical edge."""
from pathlib import Path
import collections,copy,hashlib,json
ROOT=Path(__file__).resolve().parent;AUD=ROOT/'dependency_audit_v0_37';OLD=ROOT/'dependency_audit_v0_36'
read=lambda p:json.loads(p.read_text());sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
def write(p,d):p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n')
cfg=read(ROOT/'increment_v0_37.json');g=copy.deepcopy(read(OLD/'obligation_map.json'))
g['artifact_version']='0.37';g['predecessor_graph']={'file':'dependency_audit_v0_36/obligation_map.json','sha256':sha(OLD/'obligation_map.json')}
nodes={n['id']:n for n in g['nodes']}
def evidence(c):return {'component':c,'claims':cfg['component_claims'][c],'ledger':c+'/provenance.json',
 'ledger_sha256':sha(ROOT/c/'provenance.json'),'proof_file':c+'/main.tex','proof_sha256':sha(ROOT/c/'main.tex')}
def refine(k,contract,components):
 n=nodes[k];n['previous_interface']=copy.deepcopy(n);n.update(contract=contract,introduced_or_refined_in='0.37')
 n.setdefault('evidence',[]).extend(evidence(c) for c in components)
ana=['adelic_sobolev','smooth_representatives'];cnt=['count_first_order'];com=['common_selected']
anac=sum((cfg['component_claims'][c] for c in ana),[]);cntc=cfg['component_claims']['count_first_order'];comc=cfg['component_claims']['common_selected']
refine('BASE_THETA_CUSPIDAL_EXTENSION',
 'On the SAME selected Bundle and SAME reading as BASE_THETA_READINGS, extend the exact lowest-type theta integral for each finite basis vector of HV(i,t0) to the original full Wall_i, with one family threshold before i and basis vectors. Inherited BTH/FIA/CTC/TAE/HCU/CFB/JIO supply the actual integral, cusp/lowering/lowest-type data, simultaneous io_i before every t, exact Hilbert coefficient identity and stored-choice activation. RQC supplies the same-FinPair IsReg, Hilbert derivative words, full cusp closure and original central scalar action. ASB and SPR now supply the entire original smooth representative and every ordered pointwise/global-AE derivative on the SAME finite level; the fixed-order Sobolev estimate with one N and list before x,F,psi,u; continuous evaluation and uniform growth; all five original IsMultMap fields; exact lowest-type restriction; and all-parameter linear theta assembly on the same R. Remaining analytic C subcontracts are the INITIAL bound on the original extremal theta function and the actual TARGET FinPair, before this Hilbert construction. The initial seed ZCusp remains the separately checked inherited input. Preserve original models, measures, frames, adjoints, metrics, levels and common choices. Post-Hilbert growth/central finiteness cannot supply the earlier bound. Separate geometric readings, rational tests and actual base rows remain outside this analytic packet.',ana)
refine('CERT_BASE_THETA_REDUCTION',nodes['CERT_BASE_THETA_REDUCTION']['contract']+
 ' Version 0.37 completes the original same-quotient pointwise MMap and all theta-extension consumers after the initial target FinPair and seed bound. These two upstream suppliers, and separate common geometric readings/rational tests/base rows, remain.',ana)
refine('COUNT_II_SUPPORT',
 'For each of the TWO original QX rank-four Links, at fixed iota choose ONE common coefficient threshold before every later coefficient DVR and actual universal B,Lambda; produce one ideal J carrying ring,dense,pt,end1,end2,twist AND P1core. Inherited JSP/CIP/CAP supply the same-J consumer, every-map reciprocity/universal NiceI Norm, ArPl under unchanged CohP and IsRes for supplied integral type. CCH supplies the entire required h=0,a=n=4 Choice, full twisted polarized detector and common finite coefficient extension with all NP/N3/N4/determinant/point-kernel fields. CFO now proves the literal B1 with D=4[L+:Q]+4T.q on that SAME selected full-block g=0 Kap, together with its existing CCH B2 having C=0 for all m,N. Its selected dualN has one C before m, eventual N uniform in every original admissible rep-prime satisfying the finiteness premise; ArSys and Counts use the actual TWPl and unchanged CohP. Consume Choice/B1/B2 as ONE coupled witness; no arbitrary-Kap FirstOrderDualArithmeticBound or obstruction theorem is claimed, and g=0 does not imply Sel1=0. Remaining C producers: original ordinary/control/separating arithmetic fibers and type/neatU/TThetaEx; four further Hida endpoints on this same J; all-level same-J HasAut; and original h=0 Raw on that same point, Kap, pair/J and TWAut. Retain full CohP, N4, LocCFT, exact pro-ell kernel/determinant conditions, nontrivial residual cyclotomic character, both Links, ell=3, fixed iota and every original side condition.',cnt)
refine('DESIGN_CHOICES_COMMON',nodes['DESIGN_CHOICES_COMMON']['contract']+
 ' CSR now reconstructs all finite same-record cols_of_witnesses, selected TwArgs/RealIn/RealTB, RowSideDetermined, Bundle/BTw/BWit and same-R BunU consumers. One ReadC is fixed before later twists, and the exact period, metric and evaluation normalizations are transported. Remaining construction packets are the actual common q/RXs/geometric half and readings; host/frame fields; MultEq nonzero-part support; the exact updated DivDef3 output of divisionCompatible_at_readIdentifications; eigensystem/carrier/parts and all-embedding logLam; HD with original d3b; and NEb. Their original simultaneous hypotheses and eventual thresholds remain. Completing record constructors does not construct this shared geometric/arithmetic input.',com)
refine('BASE_THETA_READINGS',nodes['BASE_THETA_READINGS']['contract']+
 ' CSR9 supplies the actual finite columns once original reFace/readings and its listed witnesses are present, with one ReadC before every later TwArgs. CSR11–16 preserve both level metrics and all thirteen reading maps under the exact scalar/error update; selected periods and evaluation use the actual MMap and kappa=(c*nP)^(-1/2). These close transport/assembly consumers. Original Read/ReadL, geometric half, MultEq support and exact updated DivDef3 production remain, with all rational tests preserved only when supplied.',com)
refine('SECOND_LAYER_COMPATIBLE_SELECTION',nodes['SECOND_LAYER_COMPATIBLE_SELECTION']['contract']+
 ' CSR21–22 now construct the same-R Bundle/BTw/BWit/BunU outputs from the exact selected realization/row-side packet and NEb, with the original EvP/ParEv quantifier order. Actual common selection, the five stated realization packets and NEb remain upstream; none is replaced by an independently chosen compatible record.',com)
g['nodes']=list(nodes.values())
g['selected_interface_cuts']['theta_v037']={
 'completed':'Full original chart/local Sobolev/rational count/pointwise growth, smooth representatives/all derivatives, all five IsMultMap fields, exact restriction and generic linear theta assembly.',
 'nested_closed':['RQC_SMOOTH_REPRESENTATIVES_AND_SOBOLEV','HCU_POINTWISE_AUTOMORPHIC_REALIZATION','BackForm.exists_multMap','ThetaMap.restrictsTo_of_eq','ThetaFiresLinear.exists_linear_lift'],
 'remaining':['BASE_THETA_READINGS','BASE_THETA_CUSPIDAL_EXTENSION','BASE_THETA_RATIONAL_TESTS','SLR_BASE_ROWS_PRODUCER'],
 'residual':'Initial boundedness and actual target FinPair; common geometric readings, rational tests and original base rows remain separate.',
 'binding':'Same R/model/nuQ/finite level; one representative for all ordered words; N/list before x,F,psi,u; ASB3/4 -> SPR13 -> ASB14 -> SPR14–25; no circular initial bound.'}
ccl=read(ROOT/'count_first_order/closure.json')
coupled=next(r for r in ccl['sufficient_rules'] if r['conclusion']=='COUPLED_ORIGINAL_CHOICE_B1_B2')
g['selected_interface_cuts']['count_ii_v037']={
 'completed':'Exact selected B1 with exponent 4[L+:Q]+4q on the same CCH Choice/B2 witness.',
 'nested_closed':['JSP_FIRST_ORDER_BOUND_ON_SAME_CCH_SELECTED_KAP'], 'remaining':['COUNT_II_SUPPORT'],
 'coupled_rule':copy.deepcopy(coupled),
 'remaining_nested':['JSP_ORIGINAL_ORDINARY_DATA','JSP_FOUR_HIDA_ENDPOINTS','JSP_SAME_IDEAL_HASAUT','JSP_SINGLE_POINT_RAW'],
 'binding':'Same xprime,j,Kap,sg,al,T,TWPl and J; g=0 is selected, not a Sel1 vanishing argument. No arbitrary-Kap B1 or B2 closure. Both Links, ell=3, fixed iota and one common coefficient threshold remain.'}
g['selected_interface_cuts']['common_realization_v037']={
 'completed':'Original columns/one ReadC, exact evaluation-period placement, scalar/error transports, all selected RealIn/RealTB/row-side/Bundle/BWit/BunU consumers.',
 'remaining_packets':['common q/RXs and geometric half with original Read/ReadL','host/frame fields','MultEq nonzero-part support','exact updated DivDef3','eigensystem/carrier/parts and all-embedding logLam','HD with original d3b','NEb'],
 'binding':'Same R throughout; initial zero Sp is replaced by the actual later period; exact nP norm and both pde/pde-prime contractions; no producer inferred from record transport.'}
for n in g['work_refinement_nodes']:
 if n['id']=='GLOBAL_LOCAL_THETA_BINDINGS':n['version_0_37_update']=g['selected_interface_cuts']['theta_v037']['binding']+' '+g['selected_interface_cuts']['theta_v037']['residual']
 if n['id'] in ['HIDA_FIELDS','P1_CORE_MATCH','P1_CORE_ARITHMETIC_PRODUCER']:n['version_0_37_update']='Selected Choice/B1/B2 now supplied together. Original ordinary/type, Hida, same-J HasAut, Raw, CohP/LocCFT and side guards remain.'
g['source_inputs']={'predecessor_graph':g['predecessor_graph']}
for c in cfg['components']:
 for f in ['provenance.json','closure.json']:
  g['source_inputs'][c+'_'+f.split('.')[0]]={'file':c+'/'+f,'sha256':sha(ROOT/c/f)}
g['source_inputs']['count_published_application']={'file':'count_first_order/published_applications.json','sha256':sha(ROOT/'count_first_order/published_applications.json')}
if (AUD/'main.tex').exists():g['source_inputs']['current_narrative']={'file':'dependency_audit_v0_37/main.tex','sha256':sha(AUD/'main.tex')}
changes={
 'GLOBAL_SMALL_RANK':{'claims':anac,'closed':'All original downstream smooth/Sobolev/MMap and theta consumers.','retained':'Initial boundedness/target FinPair and same-object readings/rational tests/base rows.'},
 'GLOBAL_LOCAL_THETA_BINDINGS':{'claims':anac+comc,'closed':'Original analytic and finite same-R realization/Bundle assembly consumers.','retained':'Common geometry/readings, initial bound/volume, multiplicity/NEb/division and eigensystem packets.'},
 'RANK4_JOINT_ORDINARY_SUPPORT':{'claims':cntc,'closed':'Literal selected B1 with exact exponent on same Choice/B2 witness.','retained':'Ordinary/type/control, four Hida endpoints, same-J HasAut, Raw and original arithmetic guards.'},
 'COUNT_II_SUPPORT':{'claims':cntc,'closed':'Selected JSP_FIRST_ORDER_BOUND.','retained':'Whole two-Link same-J producer; no universal arbitrary-Kap theorem.'},
 'GLOBAL_DESIGN':{'claims':comc,'closed':'Exact selected record/Bundle consumers.','retained':'Common recursive geometry and five realization packets plus NEb.'}}
disp=copy.deepcopy(read(OLD/'target_disposition.json'));disp['version']='0.37'
disp['predecessor_disposition']={'file':'dependency_audit_v0_36/target_disposition.json','sha256':sha(OLD/'target_disposition.json')}
prior=read(ROOT/'history/version_0_36/next_source_targets.json')['targets'];assert len(prior)==len(disp['records'])==245
for t,r in zip(prior,disp['records']):
 assert t.get('id')==r['original_id']
 r['predecessor_record_sha256']=hashlib.sha256(json.dumps(t,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()).hexdigest()
 r['version_0_37_scope_updates']=[dict(frontier=k,**v) for k,v in changes.items() if k in r.get('frontier_ids',[])]
 r['version_0_37_disposition_policy']='Inherited compound scope retained; newly completed nested producers distinguished from remaining coupled inputs.'
disp['current_selected_frontier']='dependency_audit_v0_37/obligation_map.json'
disp['coverage']['records_with_v037_scope_updates']=sum(bool(r['version_0_37_scope_updates']) for r in disp['records'])
write(AUD/'target_disposition.json',disp)
g['backlog_crosswalk']={'file':'dependency_audit_v0_37/target_disposition.json','sha256':sha(AUD/'target_disposition.json'),'records':245,'scope_groups':107,'meaning':'Every original compound scope retained with additive producer reductions.'}
active=set();done=set()
def visit(k):
 assert k in nodes and k not in active
 if k in done:return
 active.add(k)
 for j in nodes[k]['requires']:visit(j)
 active.remove(k);done.add(k)
for k in nodes:visit(k)
def reach(k):
 seen=set();todo=[k]
 while todo:
  v=todo.pop()
  if v in seen:continue
  seen.add(v);todo+=nodes[v]['requires']
 return seen
rh=reach('ORDINARY_RH');grh=reach('DIRICHLET_GRH');assert rh|grh==set(nodes)
assert 'COUNT_III_PRODUCER' not in rh and 'COUNT_III_PRODUCER' in grh
leaves=[n for n in nodes.values() if n['gate']=='LEAF' and n['status'] not in ['proved_in_stated_scope','published_application_checked']]
assert len(leaves)==34 and collections.Counter(n['category'] for n in leaves)=={'C':23,'B':9,'D':2}
g['validation'].update(selected_node_count=len(nodes),rh_reachable_count=len(rh),dirichlet_grh_reachable_count=len(grh),
 open_leaf_count=34,open_leaf_categories={'C':23,'B':9,'D':2},logical_graph_acyclic=True,all_selected_nodes_reachable_from_roots=True,
 original_smooth_representatives_complete_on_same_FinPair=True,original_fixed_level_Sobolev_complete=True,
 original_MMap_complete_on_bounded_HolForm_FinPair_ZCusp=True,original_selected_B1_complete=True,
 Choice_B1_B2_same_witness_coupling_explicit=True,arbitrary_Kap_B1_not_claimed=True,
 original_Bundle_BWit_consumers_complete_on_exact_inputs=True,actual_common_construction_not_claimed=True,
 base_extension_not_claimed_complete=True,same_ideal_support_producer_not_claimed_complete=True,
 additional_selected_whole_leaves_closed=0,new_Lean_build_performed=False)
write(AUD/'obligation_map.json',g)
write(AUD/'remaining_leaf_register.json',{'artifact_version':'0.37','source_commit':g['source_commit'],'category_key':g['categories'],'scope':g['scope'],'records':leaves,'warning':'Selected sufficient coupled obligations; not a completion percentage or absolute minimality theorem.'})
write(AUD/'closure_delta.json',{'artifact_version':'0.37','source_commit':g['source_commit'],'changes':changes,'closed_selected_leaves':[],
 'nested_coupled_rule':coupled,'retained_historical_correction':'RF16 governed by DEX11; historical bytes unchanged.'})
write(AUD/'published_applications.json',{'artifact_version':'0.37','source_commit':g['source_commit'],
 'freshly_checked_applications':read(ROOT/'count_first_order/published_applications.json'),
 'inherited_registry':{'file':'dependency_audit_v0_36/published_applications.json','sha256':sha(OLD/'published_applications.json')},
 'note':'Only the finite Milne decomposition/inertia facts are imported; CFO proves the absolute passage. No ordinary/control, LocCFT, global-duality or initial analytic producer is silently imported.'})
print(json.dumps({k:g['validation'][k] for k in ['selected_node_count','rh_reachable_count','dirichlet_grh_reachable_count','open_leaf_count','open_leaf_categories','additional_selected_whole_leaves_closed']},indent=2))
