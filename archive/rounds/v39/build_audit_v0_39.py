#!/usr/bin/env python3
"""Refine original nested producers while preserving every selected logical edge."""
from pathlib import Path
import collections,copy,hashlib,json
ROOT=Path(__file__).resolve().parent;AUD=ROOT/'dependency_audit_v0_39';OLD=ROOT/'dependency_audit_v0_38'
read=lambda p:json.loads(p.read_text());sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
def write(p,d):p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n')
cfg=read(ROOT/'increment_v0_39.json');g=copy.deepcopy(read(OLD/'obligation_map.json'))
g['artifact_version']='0.39';g['predecessor_graph']={'file':'dependency_audit_v0_38/obligation_map.json','sha256':sha(OLD/'obligation_map.json')}
nodes={n['id']:n for n in g['nodes']}
def evidence(c):return {'component':c,'claims':cfg['component_claims'][c],'ledger':c+'/provenance.json',
 'ledger_sha256':sha(ROOT/c/'provenance.json'),'proof_file':c+'/main.tex','proof_sha256':sha(ROOT/c/'main.tex')}
def refine(k,contract,components):
 n=nodes[k];n['previous_interface']=copy.deepcopy(n);n.update(contract=contract,introduced_or_refined_in='0.39')
 n.setdefault('evidence',[]).extend(evidence(c) for c in components)
cnt=['limit_system','proell_descent'];com=['row_integrability','common_readings']
cntc=sum((cfg['component_claims'][c] for c in cnt),[]);comc=sum((cfg['component_claims'][c] for c in com),[])
refine('COUNT_II_SUPPORT',
 'For each of the TWO original QX rank-four Links, at fixed iota choose ONE common coefficient threshold before every later coefficient DVR and actual universal B,Lambda; produce one ideal J carrying ring,dense,pt,end1,end2,twist AND P1core. Inherited JSP/CIP/CAP/CCH/CFO supply the same-J consumer, every-map reciprocity/universal NiceI Norm, ArPl under unchanged CohP, supplied-type IsRes, the full selected h=0,a=n=4,g=0 Choice and its coupled B1/B2, with D=4[L+:Q]+4T.q and B2 constant zero. The selected dualN bound has one C before every m and an eventual N threshold uniform over every original admissible rep-prime satisfying its finiteness premise, on the actual TWPl and unchanged CohP. CRW supplies the original full-block completed S6 representation and exact coefficient DVR OO/rF on normalized data with O onto K, cotangent-to-Selmer injection, selected CohLim, D-generator presentation, presOut0/GalOut comparison and h=0 ChainAbs. LIM now constructs the entire original S4, including the full actual Lim and uniform local-map convergence. PQL constructs the full original TWQuot and proves full CoreBC-to-Raw pro-ell descent, including Pair, Pt, Kap, B1/B2 and supplied TWAut on the same B,J,K,f and modules, with full determinant laws and exact closed ideals. Remaining C producers are original ordinary/control/separating arithmetic fibers and type/neatU/TThetaEx; four Hida endpoints on this same J; all-level same-J HasAut; and the residual selected h=0 Raw packet: normalized Core limiting patched rings/maps/modules and S5 support, plus Core-to-CoreBC coefficient normalization and the added Unit parameter. S4 and CoreBC-to-Raw pro-ell descent are no longer current open producers. Preserve full CohP, LocCFT, N4, exact determinant/pro-ell conditions, nontrivial residual cyclotomic character, both Links, ell=3, fixed iota, every local guard and the common coefficient threshold. No arbitrary-Kap B1/B2 theorem, Sel1=0 inference or complete same-J support producer is claimed.',cnt)
refine('DESIGN_CHOICES_COMMON',
 'For the one target HostExW, construct the original compatible DesignChoices on Cdes=WithTw(WithSm Cprime), where Cprime=WithChN(A intersect target class), A is the one Built construction class, and cT(eps,y)=cTmin(y). Retain every original field, tuple, word, metric and common bundle duty. DSZ10 and RMP11 give size/rank properties of class members, not member existence. The original RecExP/RecAtG and common object/row route remains coupled. Construct ONE original common design family R with its recursive/geometric half and q/o/Moved/Fits, actual ChT/LfT/Reps comparison packet, primitive Holds and eta agreement at every required row/place. RDR now reconstructs the full original level-zero side and moved-Read constructors, ReadPk and pins on those given data, choosing one Side0 before every later Read; full ReadL retains the original eta agreement. Inherited CSR supplies finite columns, one ReadC before later twists, period/evaluation and scalar/error transports, RowSideDetermined and same-R Bundle/BTw/BWit/BunU consumers. RPI supplies exact RowPairInt for every actual pair and finite translate with the original mu_b/fd0 and thereby discharges DI\'s extra analytic premise. First literal DivDef3 at the same updated R,F,Y,Z,C,sEE is now proved from its original readings, Pins/Holds, stored nonzero IsItW chain, full five-predicate real-group input DI.2 (DiscreteSeriesCover, HarishChandraModules, CasselmanWallach, HarishChandraFinite, CuspRapidDecay), and group-tie premises alone. Remaining construction packets are actual common geometry/comparisons/tests and eta agreement; host/frame fields; MultEq nonzero-part support; original nonzero chain and group tie; eigensystem/carrier/parts and all-embedding logLam; HD with d3b; NEb; rational tests and actual base rows. Retain all original simultaneous hypotheses and eventual thresholds. The stronger second DivRows3 theta square remains separate. The exact pair-integrability theorem does not assert universal quotient-height CuspRapidDecay, and the reader/identity constructors do not produce the common datum.',com)
refine('BASE_THETA_READINGS',
 'For every family in the original class, eventually on the SAME selected Bundle and for each i<m, supply the actual R,F,Read,ReadL, weak models/Weil data and phase-one pins. Identify their LiftTie.theta, mtRead, mjRead and ThDef3 basis with that Bundle.P.A3, P.Zs, P.S0 and its stored maps. Exact field, embeddings, metrics, measures, row family and weak choices are retained. This remains one part of the coupled BTH12 producer. RDR now proves the full original exists_side_reading_level_zero, read_of_moved and ReadPk/pin constructors on the actual given geometric/comparison inputs, with one Side0 before every reader and all twelve exact Read ties. Full ReadL is obtained with the original o.eta(j,v)=q.eta(j,v) guard for every 1<=j<=m and place v; arbitrary Over does not imply this equality. These constructors preserve original ChT/LfT/Reps, Fits/Moved, periods, representatives and coordinate data, but do not construct them. Inherited CSR supplies finite columns, fixes one ReadC before all TwArgs, transports both metrics and all thirteen reading maps, and gives the actual period/evaluation with kappa=(c*nP)^(-1/2). RPI now supplies the exact original row-pair integrability, so DI gives first updated DivDef3 from the retained original Pins/Holds, stored nonzero chain, five real-group predicates and group tie, without an extra RowPairInt premise. Initial theta extension remains complete by FV/SBD. Actual common geometric/comparison data, primitive Holds/rational tests and eta agreement, reFace compatibility, MultEq support, the original chain/group inputs, actual base rows and any stronger DivRows3 theta square remain. No independently chosen compatible reading, new family threshold or replacement Haar normalization is allowed.',com)
refine('CERT_BASE_THETA_REDUCTION',nodes['CERT_BASE_THETA_REDUCTION']['contract']+
 ' Version 0.39 additionally supplies exact original-input row integrability and first DivDef3, together with the original given-data side/read constructors and full ReadL under its eta guard. Actual common geometry/comparison/test packets and base-row construction remain.',com)
refine('SECOND_LAYER_COMPATIBLE_SELECTION',nodes['SECOND_LAYER_COMPATIBLE_SELECTION']['contract']+
 ' Version 0.39 supplies the original given-data reader constructors and exact RowPairInt/first DivDef3 on original premises. It leaves one actual common geometric/comparison/test member, eta agreement, compatible selection, rational tests, base rows, host/parts/NEb and original EvP/ParEv thresholds upstream.',com)
g['nodes']=list(nodes.values())
def closure(c):return {'file':c+'/closure.json','sha256':sha(ROOT/c/'closure.json')}
g['selected_interface_cuts']['count_ii_v039']={
 'completed':'Entire original S4; full original TWQuot; full CoreBC-to-Raw pro-ell descent, including same-point B1/B2 and supplied TWAut, exact full-law closed ideals and one-way NonSS.',
 'nested_closed_claims':cntc,'remaining':['COUNT_II_SUPPORT'],
 'newly_closed_nested':['ORIGINAL_S4','ORIGINAL_TWQUOT','ORIGINAL_COREBC_TO_RAW_PROELL_DESCENT'],
 'remaining_nested':['JSP_ORIGINAL_ORDINARY_DATA','JSP_FOUR_HIDA_ENDPOINTS','JSP_SAME_IDEAL_HASAUT','CORE_LIMITING_PATCHED_MAPS_MODULES_S5','CORE_TO_COREBC_COEFFICIENT_NORMALIZATION_UNIT'],
 'binding':'Same CCH/CFO Choice/B1/B2, selected h=0,a=n=4,g=0, point/Kap/T/TWPl/TWAut and B,J,K,f; ell=3, fixed iota and common threshold. One B1 C before m; original eventual N quantifiers. No universal arbitrary-Kap theorem or full Raw/support completion.',
 'component_closures':[closure(c) for c in cnt],
 'limit_record_scope':'Full original forall T, T.ProL implies Nonempty(Lim T); not a selected h=0 substitute.',
 'descent_scope':'Full original CoreBC implies Raw; independent from the unconstructed normalized Core patching and coefficient-normalization producers.'}
g['selected_interface_cuts']['common_realization_v039']={
 'completed':'Exact original-input RowPairInt; first original DivDef3 with the extra analytic premise discharged; full given-data level-zero and moved-Read constructors, ReadPk/pins and guarded full ReadL.',
 'nested_closed_claims':comc,
 'newly_closed_nested':['EXACT_ROW_PAIR_INTEGRABILITY','FIRST_DIVDEF3_ORIGINAL_PREMISES','LEVEL_ZERO_SIDE_READING_PRODUCER','MOVED_READ_PRODUCER','READPK_PIN_PRODUCER'],
 'remaining_packets':['common_geometric_Fits_Moved_realization','actual_ChT_LfT_Reps_and_primitive_tests','original_eta_agreement_for_ReadL','host_frames','MultEq_support','original_nonzero_chain_and_group_tie','eigensystems_parts_all_embedding_logLam','HD_d3b','NEb','rational_tests_and_base_rows'],
 'binding':'Same R,F,Y,Z,C,sEE, both original finite-group levels and exact nP inverse measure; all original Pins/Holds and five real-group predicates retained. One Side0 before every reader; full ReadL retains o.eta=q.eta for every required j,v. No extra analytic premise beyond the original inputs is needed for first DivDef3.',
 'outside_scope':'Stronger second DivRows3 theta square, universal quotient-height CuspRapidDecay and actual common datum are not supplied.',
 'component_closures':[closure(c) for c in com]}
g['selected_interface_cuts']['theta_v039']={
 'previous_complete_leaf':'BASE_THETA_CUSPIDAL_EXTENSION remains complete on original common data.',
 'new_progress':'Original given-data reader producers and exact first-division row integrability are supplied.',
 'remaining':['BASE_THETA_READINGS','BASE_THETA_RATIONAL_TESTS','SLR_BASE_ROWS_PRODUCER'],
 'guard':'The full selected reading leaf includes actual common geometric/comparison suppliers and exact eta agreement, plus outer family/eventual/same-Bundle duties. Pointwise constructor completion alone does not close it.'}
g['source_inputs']={'predecessor_graph':copy.deepcopy(g['predecessor_graph'])}
for c in cfg['components']:
 for stem in ['provenance','closure','published_applications']:
  p=ROOT/c/(stem+'.json')
  if p.is_file():g['source_inputs'][c+'_'+stem]={'file':p.relative_to(ROOT).as_posix(),'sha256':sha(p)}
if (AUD/'main.tex').exists():g['source_inputs']['current_narrative']={'file':'dependency_audit_v0_39/main.tex','sha256':sha(AUD/'main.tex')}
changes={
 'GLOBAL_SMALL_RANK':{'claims':comc,'closed':'Exact original-input RowPairInt and first DivDef3; given-data side/read constructors.','retained':'Actual common geometry/comparisons, eta agreement, rational tests/base rows and original chain/group inputs.'},
 'GLOBAL_LOCAL_THETA_BINDINGS':{'claims':comc,'closed':'Exact given-data reader constructors and row-pair integrability on original measures.','retained':'Actual shared geometric/comparison/test suppliers; universal quotient-height CuspRapidDecay is not asserted.'},
 'RANK4_JOINT_ORDINARY_SUPPORT':{'claims':cntc,'closed':'Entire S4 and full TWQuot/CoreBC-to-Raw pro-ell descent.','retained':'Normalized Core limiting patching/S5, coefficient normalization/Unit, ordinary/control/type/Hida/HasAut on same J.'},
 'COUNT_II_SUPPORT':{'claims':cntc,'closed':'Full original limit-group and matched pro-ell descent subproducers.','retained':'Whole two-Link same-J support producer with normalized patching and arithmetic/automorphic existence.'},
 'GLOBAL_DESIGN':{'claims':comc,'closed':'Exact RowPairInt and first original-input DivDef3; original given-data side/read/ReadPk constructors and guarded ReadL.','retained':'Actual common geometry/comparisons/tests and eta agreement, original chain/group inputs, parts, NEb and stronger second DivRows3.'}}
disp=copy.deepcopy(read(OLD/'target_disposition.json'));disp['version']='0.39'
disp['predecessor_disposition']={'file':'dependency_audit_v0_38/target_disposition.json','sha256':sha(OLD/'target_disposition.json')}
prior=read(ROOT/'history/version_0_38/next_source_targets.json')['targets'];assert len(prior)==len(disp['records'])==245
for t,r in zip(prior,disp['records']):
 assert t.get('id')==r['original_id']
 r['predecessor_record_sha256']=hashlib.sha256(json.dumps(t,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()).hexdigest()
 r['version_0_39_scope_updates']=[dict(frontier=k,**v) for k,v in changes.items() if k in r.get('frontier_ids',[])]
 r['version_0_39_disposition_policy']='Every inherited compound scope retained. Four nested branches advance, with no new whole selected-leaf closure.'
disp['current_selected_frontier']='dependency_audit_v0_39/obligation_map.json'
disp['coverage']['records_with_v039_scope_updates']=sum(bool(r['version_0_39_scope_updates']) for r in disp['records'])
write(AUD/'target_disposition.json',disp)
g['backlog_crosswalk']={'file':'dependency_audit_v0_39/target_disposition.json','sha256':sha(AUD/'target_disposition.json'),'records':245,'scope_groups':107,'meaning':'All inherited compound targets retained with exact additive nested producer reductions.'}
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
assert len(nodes)==121 and len(rh)==101 and len(grh)==110
assert 'COUNT_III_PRODUCER' not in rh and 'COUNT_III_PRODUCER' in grh
leaves=[n for n in nodes.values() if n['gate']=='LEAF' and n['status'] not in ['proved_in_stated_scope','published_application_checked']]
assert len(leaves)==33 and collections.Counter(n['category'] for n in leaves)=={'C':22,'B':9,'D':2}
oldnodes={n['id']:n for n in read(OLD/'obligation_map.json')['nodes']}
assert all(n['gate']==oldnodes[k]['gate'] and n['requires']==oldnodes[k]['requires'] for k,n in nodes.items())
g['validation'].update(selected_node_count=len(nodes),rh_reachable_count=len(rh),dirichlet_grh_reachable_count=len(grh),
 open_leaf_count=33,open_leaf_categories={'C':22,'B':9,'D':2},logical_graph_acyclic=True,all_selected_nodes_reachable_from_roots=True,
 generic_universal_CuspRapidDecay_not_claimed=True,exact_original_row_pair_integrability_complete=True,
 first_DivDef3_extra_RowPairInt_discharged=True,original_given_data_side_read_constructors_complete=True,
 full_ReadL_eta_guard_retained=True,original_entire_S4_complete=True,original_full_TWQuot_complete=True,
 original_full_CoreBC_to_Raw_proell_descent_complete=True,Raw_patching_support_descent_remain=False,
 normalized_Core_limiting_patching_S5_and_coefficient_normalization_Unit_remain=True,
 actual_common_construction_not_claimed=True,same_ideal_support_producer_not_claimed_complete=True,
 additional_selected_whole_leaves_closed=0,new_Lean_build_performed=False)
write(AUD/'obligation_map.json',g)
write(AUD/'remaining_leaf_register.json',{'artifact_version':'0.39','source_commit':g['source_commit'],'category_key':g['categories'],'scope':g['scope'],'records':leaves,'warning':'Selected sufficient coupled obligations, not a completion percentage or absolute minimality theorem.'})
write(AUD/'closure_delta.json',{'artifact_version':'0.39','source_commit':g['source_commit'],'changes':changes,'closed_selected_leaves':[],
 'closed_nested_producers':['ORIGINAL_S4','ORIGINAL_TWQUOT','ORIGINAL_COREBC_TO_RAW_PROELL_DESCENT','EXACT_ROW_PAIR_INTEGRABILITY','FIRST_DIVDEF3_ORIGINAL_PREMISES','LEVEL_ZERO_SIDE_READING_PRODUCER','MOVED_READ_PRODUCER','READPK_PIN_PRODUCER'],
 'prior_open_leaf_count':33,'current_open_leaf_count':33,'retained_historical_correction':'RF16 governed by DEX11; historical bytes unchanged.'})
apps=[]
for c in cfg['components']:
 p=ROOT/c/'published_applications.json'
 if not p.exists():continue
 data=read(p);items=data if isinstance(data,list) else data.get('applications',data.get('freshly_checked_applications',[]))
 assert isinstance(items,list),(c,'unsupported publication registry schema')
 apps.extend(dict(component=c,**a) for a in items)
assert len({a['id'] for a in apps})==len(apps)
write(AUD/'published_applications.json',{'artifact_version':'0.39','source_commit':g['source_commit'],
 'freshly_checked_applications':apps,
 'inherited_registry':{'file':'dependency_audit_v0_38/published_applications.json','sha256':sha(OLD/'published_applications.json')},
 'note':'Exact original hypotheses and scope in each component certificate. The imports do not provide normalized limiting patching/S5, coefficient normalization/Unit, ordinary/automorphic existence or common geometry.'})
print(json.dumps({k:g['validation'][k] for k in ['selected_node_count','rh_reachable_count','dirichlet_grh_reachable_count','open_leaf_count','open_leaf_categories','additional_selected_whole_leaves_closed']},indent=2))
