#!/usr/bin/env python3
"""Close the selected analytic leaf and refine nested suppliers without changing edges."""
from pathlib import Path
import collections,copy,hashlib,json
ROOT=Path(__file__).resolve().parent;AUD=ROOT/'dependency_audit_v0_38';OLD=ROOT/'dependency_audit_v0_37'
read=lambda p:json.loads(p.read_text());sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
def write(p,d):p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n')
cfg=read(ROOT/'increment_v0_38.json');g=copy.deepcopy(read(OLD/'obligation_map.json'))
g['artifact_version']='0.38';g['predecessor_graph']={'file':'dependency_audit_v0_37/obligation_map.json','sha256':sha(OLD/'obligation_map.json')}
nodes={n['id']:n for n in g['nodes']}
def evidence(c):return {'component':c,'claims':cfg['component_claims'][c],'ledger':c+'/provenance.json',
 'ledger_sha256':sha(ROOT/c/'provenance.json'),'proof_file':c+'/main.tex','proof_sha256':sha(ROOT/c/'main.tex')}
def refine(k,contract,components):
 n=nodes[k];n['previous_interface']=copy.deepcopy(n);n.update(contract=contract,introduced_or_refined_in='0.38')
 n.setdefault('evidence',[]).extend(evidence(c) for c in components)
ana=['finite_volume','seed_boundedness'];cnt=['count_raw'];com=['division_identity']
anac=sum((cfg['component_claims'][c] for c in ana),[]);cntc=cfg['component_claims']['count_raw'];comc=cfg['component_claims']['division_identity']
refine('BASE_THETA_CUSPIDAL_EXTENSION',
 'On the SAME selected Bundle and SAME reading as BASE_THETA_READINGS, the exact lowest-type theta integral now extends to the original full Wall_i for all original i,t, and hence for every finite base-parameter basis vector, with no additional family threshold. FV proves the entire original FiniteVolume2 and supplies actual target FinPair before all t,x, preserving every original Haar and fundamental-domain normalization. SBD proves full-center finiteness directly from the initial highest-weight equations, exact original ZI/additive-adele and rational-parabolic cusp descent, and the initial seed bound by checked Miller–Schmid rapid decay plus a finite Siegel cover. The initial bound has forall i,t,x exists C forall g, as required; no uniformity in t,x is invented. Inherited HCU/RQC/ASB/SPR then give the complete same-quotient pointwise IsMultMap, exact lowest-type restriction, linear theta assembly and stored-choice activation on the same R. The full selected analytic obligation is complete on the original common-data premises. Common geometric readings, rational tests and actual base rows remain separate selected producers. This does not assert the stronger universal CuspRapidDecay/global-height predicate for arbitrary multiplicity-space forms.',ana)
nodes['BASE_THETA_CUSPIDAL_EXTENSION'].update(category='B',status='proved_in_stated_scope',
 closure={'version':'0.38','claim':'SBD16','joint_claims':anac,'scope':'Entire selected analytic leaf on the same original common data; no extra threshold.'})
refine('CERT_BASE_THETA_REDUCTION',nodes['CERT_BASE_THETA_REDUCTION']['contract']+
 ' Version 0.38 supplies both initial target FinPair and actual seed bound and thereby the full selected cuspidal-extension leaf. Its separate common geometric readings, rational tests and base-row contracts remain.',ana)
refine('COUNT_II_SUPPORT',
 'For each of the TWO original QX rank-four Links, at fixed iota choose ONE common coefficient threshold before every later coefficient DVR and actual universal B,Lambda; produce one ideal J carrying ring,dense,pt,end1,end2,twist AND P1core. Inherited JSP/CIP/CAP/CCH/CFO supply the same-J consumer, every-map reciprocity/universal NiceI Norm, ArPl under unchanged CohP, supplied-type IsRes, the full selected h=0,a=n=4,g=0 Choice and its coupled B1/B2, with D=4[L+:Q]+4T.q and B2 constant zero. The selected dualN bound has one C before every m and an eventual N threshold uniform over every original admissible rep-prime satisfying its finiteness premise, on the actual TWPl and unchanged CohP. CRW now supplies the original full-block completed S6 representation and exact coefficient DVR OO/rF on normalized data with O onto K, bounded first-order derivatives and cotangent-to-Selmer injection, selected CohLim on its supplied Lim, actual D-generator power-series presentation, presOut0/GalOut comparison and h=0 ChainAbs consumer. It keeps the same point, Kap, T, TWPl, TWAut, paired ideal J and actual completion; no n! inversion excludes ell=3. Remaining C producers: original ordinary/control/separating arithmetic fibers and type/neatU/TThetaEx; four Hida endpoints on this same J; all-level same-J HasAut; and the residual original h=0 Raw packet, namely actual S4, patched ring/maps/modules with S5 support and the coefficient normalization/added Unit parameter and pro-ell descent back to the same J. The published Cayley–Hamilton input and elementary cotangent comparison do not produce patching support. Preserve full CohP, LocCFT, N4, exact determinant/pro-ell conditions, nontrivial residual cyclotomic character, both Links, ell=3, fixed iota, every local guard and the common coefficient threshold. No arbitrary-Kap B1/B2 theorem or Sel1=0 inference is claimed.',cnt)
refine('DESIGN_CHOICES_COMMON',
 'For the one target HostExW, construct the original compatible DesignChoices on Cdes=WithTw(WithSm Cprime), where Cprime=WithChN(A intersect target class), A is the one Built construction class, and cT(eps,y)=cTmin(y). Retain every original field, tuple, word, metric and common bundle duty. DSZ10 and RMP11 give size/rank properties of class members, not member existence. The original RecExP/RecAtG and common object/row route remains coupled. Construct ONE original common design family R with its recursive/geometric half, q/RXs and Read/ReadL, and compatible selected realization. Inherited CSR supplies finite columns, one ReadC before later twists, exact period/evaluation and scalar/error transports, RowSideDetermined and same-R Bundle/BTw/BWit/BunU consumers. DI now proves the first literal DivDef3 at that exact updated R,F,Y,Z,C,sEE, including StepLev, TopLev, RowProj, both composite identities and first theta li/span/lat, on the original Pins/Holds, stored nonzero IsItW chain, the full original five-predicate real-group input DI.2 (DiscreteSeriesCover, HarishChandraModules, CasselmanWallach, HarishChandraFinite, CuspRapidDecay), and group-tie premises, PLUS explicitly additional RowPairInt for all actual b,t,w,c,v,v-prime and required finite residual translates with the exact mu_b/fd0. This is a conditional sufficient refinement, not a proof of the original theorem from its original premises alone. Remaining construction packets are actual common geometry and readings; host/frame fields; MultEq nonzero-part support; the stated original nonzero chain, group tie and required generic multiplicity-pair integrability; eigensystem/carrier/parts and all-embedding logLam; HD with original d3b; and NEb. Retain every original simultaneous hypothesis and eventual threshold, rational test and actual base row. The stronger second DivRows3 theta square remains separate. The initial highest-weight seed bound does not supply universal CuspRapidDecay for arbitrary multiplicity forms, and record or identity consumers do not construct this common datum.',com)
refine('BASE_THETA_READINGS',
 'For every family in the original class, eventually on the SAME selected Bundle and for each i<m, supply the actual R,F,Read,ReadL, weak models/Weil data and phase-one pins. Identify their LiftTie.theta, mtRead, mjRead and ThDef3 basis with that Bundle.P.A3, P.Zs, P.S0 and its stored maps. Exact field, embeddings, metrics, measures, row family and weak choices are retained. This remains one part of the coupled BTH12 producer, not a freely replaceable isomorphic model. Construct its actual geometric half, reFace and rational-test compatibility. Inherited CSR supplies actual finite columns once those witnesses are present, fixes one ReadC before every later TwArgs, transports both level metrics and all thirteen reading maps under the exact scalar/error update, and places the actual period/evaluation with kappa=(c*nP)^(-1/2). DI supplies the first updated DivDef3 on this same realization under the original Pins/Holds, stored nonzero chain, the full original five-predicate real-group input DI.2 (DiscreteSeriesCover, HarishChandraModules, CasselmanWallach, HarishChandraFinite, CuspRapidDecay), and group-tie inputs, PLUS the additional RowPairInt supplier on the actual pairs and finite translates, including exact nP^(-1) row metrics. Initial theta extension is now complete by FV/SBD, but does not construct these readings. Actual geometric/readings and MultEq support, the just-listed original DI inputs, all rational tests, and any required stronger DivRows3 theta square remain. No independent compatible reading or replacement Haar normalization may be substituted.',com+ana)
refine('SECOND_LAYER_COMPATIBLE_SELECTION',nodes['SECOND_LAYER_COMPATIBLE_SELECTION']['contract']+
 ' Version 0.38 closes the selected analytic extension and reconstructs the first updated DivDef3 consumer; it leaves the original common selection, geometric readings, rational tests, base rows, host/parts/NEb and exact retained DI premises upstream, with unchanged EvP/ParEv thresholds.',com+ana)
g['nodes']=list(nodes.values())
g['selected_interface_cuts']['theta_v038']={
 'completed':'Entire selected cuspidal theta-extension obligation on the original common datum, including initial target FinPair and actual highest-weight seed bound.',
 'whole_selected_closed':['BASE_THETA_CUSPIDAL_EXTENSION'],
 'nested_closed':['FiniteVolume2','actual_target_FinPair','initial_extremal_theta_bound','ThetaMap.exists_extension','ThetaMap.exists_thetaMap'],
 'remaining':['BASE_THETA_READINGS','BASE_THETA_RATIONAL_TESTS','SLR_BASE_ROWS_PRODUCER'],
 'binding':'Same R/Wall/model/io/measure/level; target finite pairs before t,x; pre-Hilbert full center; forall i,t,x exists C forall g; all-parameter construction adds no family threshold.',
 'outside_scope':'Universal quotient-height CuspRapidDecay for arbitrary IsAutFunSm/IsCuspFun is not asserted; generic DI pairing inputs remain in common realization.'}
g['selected_interface_cuts']['count_ii_v038']={
 'completed':'Original selected full-block S6 and OO/rF; cotangent injection, selected CohLim on supplied Lim, D-generator presentation and h=0 ChainAbs comparison.',
 'nested_closed_claims':cntc,'remaining':['COUNT_II_SUPPORT'],
 'remaining_nested':['JSP_ORIGINAL_ORDINARY_DATA','JSP_FOUR_HIDA_ENDPOINTS','JSP_SAME_IDEAL_HASAUT','CRW_ACTUAL_S4','CRW_PATCHED_MAPS_MODULES_S5','CRW_COEFFICIENT_PROELL_DESCENT'],
 'binding':'Same CCH/CFO Choice/B1/B2, h=0,a=n=4,g=0, point/Kap/T/TWPl/TWAut/J; ell=3, fixed iota and common threshold. No universal arbitrary-Kap theorem or Raw completion.',
 'component_closure':{'file':'count_raw/closure.json','sha256':sha(ROOT/'count_raw/closure.json')}}
g['selected_interface_cuts']['common_realization_v038']={
 'completed':'Conditional first literal updated DivDef3 on original CSR selected realization, with original premises PLUS RowPairInt; level, projector/composite identities and first theta li/span/lat.',
 'nested_closed_claims':comc,
 'remaining_packets':['common_geometry_and_Read_ReadL','host_frames','MultEq_support','original_nonzero_chain_and_group_tie','generic_multiplicity_pair_integrability','eigensystems_parts_all_embedding_logLam','HD_d3b','NEb','rational_tests_and_base_rows'],
 'binding':'Same R,F,Y,Z,C,sEE, both original finite-group levels and exact nP inverse measure; original Pins/Holds and full five-predicate real-group input DI.2 (DiscreteSeriesCover, HarishChandraModules, CasselmanWallach, HarishChandraFinite, CuspRapidDecay) retained; explicitly additional RowPairInt is not derived from the unproved original per-coset-to-global-height reduction.',
 'outside_scope':'Stronger second DivRows3 theta square and actual common datum are not supplied.',
 'component_closure':{'file':'division_identity/closure.json','sha256':sha(ROOT/'division_identity/closure.json')}}
g['source_inputs']={'predecessor_graph':copy.deepcopy(g['predecessor_graph'])}
for c in cfg['components']:
 for stem in ['provenance','closure','published_applications']:
  p=ROOT/c/(stem+'.json')
  if p.is_file():g['source_inputs'][c+'_'+stem]={'file':p.relative_to(ROOT).as_posix(),'sha256':sha(p)}
if (AUD/'main.tex').exists():g['source_inputs']['current_narrative']={'file':'dependency_audit_v0_38/main.tex','sha256':sha(AUD/'main.tex')}
changes={
 'GLOBAL_SMALL_RANK':{'claims':anac+comc,'closed':'Whole selected analytic extension; first DivDef3 consumer on original inputs.','retained':'Common readings/rational tests/base rows and stated DI producer premises.'},
 'GLOBAL_LOCAL_THETA_BINDINGS':{'claims':anac,'closed':'Actual target finite pairs and initial theta bounds, all original all-parameter extension consumers.','retained':'Original common geometry and separate generic cusp/row-pairing producer.'},
 'RANK4_JOINT_ORDINARY_SUPPORT':{'claims':cntc,'closed':'Selected original S6 and cotangent/presentation/ChainAbs comparison.','retained':'Raw S4/patching/S5/descent and ordinary/control/type/Hida/HasAut on same J.'},
 'COUNT_II_SUPPORT':{'claims':cntc,'closed':'Nested original completed-point and first-order comparison suppliers.','retained':'Whole two-Link same-J producer with patching and arithmetic/automorphic existence.'},
 'GLOBAL_DESIGN':{'claims':comc+anac,'closed':'First exact updated DivDef3 consumer and complete original theta extension.','retained':'Actual common geometry/readings, generic pairing/nonzero-chain inputs, rational tests, parts and NEb.'}}
disp=copy.deepcopy(read(OLD/'target_disposition.json'));disp['version']='0.38'
disp['predecessor_disposition']={'file':'dependency_audit_v0_37/target_disposition.json','sha256':sha(OLD/'target_disposition.json')}
prior=read(ROOT/'history/version_0_37/next_source_targets.json')['targets'];assert len(prior)==len(disp['records'])==245
for t,r in zip(prior,disp['records']):
 assert t.get('id')==r['original_id']
 r['predecessor_record_sha256']=hashlib.sha256(json.dumps(t,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()).hexdigest()
 r['version_0_38_scope_updates']=[dict(frontier=k,**v) for k,v in changes.items() if k in r.get('frontier_ids',[])]
 r['version_0_38_disposition_policy']='Every inherited compound scope retained; one selected analytic leaf closes, other changes are exact nested reductions.'
disp['current_selected_frontier']='dependency_audit_v0_38/obligation_map.json'
disp['coverage']['records_with_v038_scope_updates']=sum(bool(r['version_0_38_scope_updates']) for r in disp['records'])
write(AUD/'target_disposition.json',disp)
g['backlog_crosswalk']={'file':'dependency_audit_v0_38/target_disposition.json','sha256':sha(AUD/'target_disposition.json'),'records':245,'scope_groups':107,'meaning':'Every inherited compound target retained with additive exact producer reductions.'}
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
g['validation'].update(selected_node_count=len(nodes),rh_reachable_count=len(rh),dirichlet_grh_reachable_count=len(grh),
 open_leaf_count=33,open_leaf_categories={'C':22,'B':9,'D':2},logical_graph_acyclic=True,all_selected_nodes_reachable_from_roots=True,
 full_original_finite_volume_and_target_FinPair_complete=True,pre_Hilbert_full_center_and_initial_seed_bound_complete=True,
 base_extension_not_claimed_complete=False,base_extension_complete_on_same_common_data=True,
 generic_universal_CuspRapidDecay_not_claimed=True,first_updated_DivDef3_complete_on_exact_inputs=True,
 original_full_block_S6_and_selected_ChainAbs_comparison_complete=True,Raw_patching_support_descent_remain=True,
 actual_common_construction_not_claimed=True,same_ideal_support_producer_not_claimed_complete=True,
 additional_selected_whole_leaves_closed=1,new_Lean_build_performed=False)
write(AUD/'obligation_map.json',g)
write(AUD/'remaining_leaf_register.json',{'artifact_version':'0.38','source_commit':g['source_commit'],'category_key':g['categories'],'scope':g['scope'],'records':leaves,'warning':'Selected sufficient coupled obligations, not a completion percentage or absolute minimality theorem.'})
write(AUD/'closure_delta.json',{'artifact_version':'0.38','source_commit':g['source_commit'],'changes':changes,'closed_selected_leaves':['BASE_THETA_CUSPIDAL_EXTENSION'],
 'prior_open_leaf_count':34,'current_open_leaf_count':33,'retained_historical_correction':'RF16 governed by DEX11; historical bytes unchanged.'})
apps=[]
for c in cfg['components']:
 p=ROOT/c/'published_applications.json'
 if not p.exists():continue
 data=read(p)
 if isinstance(data,list):items=data
 else:items=data.get('applications',data.get('freshly_checked_applications',[]))
 assert isinstance(items,list),(c,'unsupported publication registry schema')
 apps.extend(dict(component=c,**a) for a in items)
assert len({a['id'] for a in apps})==len(apps)
write(AUD/'published_applications.json',{'artifact_version':'0.38','source_commit':g['source_commit'],
 'freshly_checked_applications':apps,
 'inherited_registry':{'file':'dependency_audit_v0_37/published_applications.json','sha256':sha(OLD/'published_applications.json')},
 'note':'Exact hypotheses and conclusions are in each component certificate. These imports do not supply original patching support, ordinary/automorphic existence, common geometry or universal generic cusp decay.'})
print(json.dumps({k:g['validation'][k] for k in ['selected_node_count','rh_reachable_count','dirichlet_grh_reachable_count','open_leaf_count','open_leaf_categories','additional_selected_whole_leaves_closed']},indent=2))
