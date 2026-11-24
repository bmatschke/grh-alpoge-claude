#!/usr/bin/env python3
"""Refine exact original producer cuts; preserve every selected logical edge."""
from pathlib import Path
import collections,copy,hashlib,json
ROOT=Path(__file__).resolve().parent;AUD=ROOT/'dependency_audit_v0_41';OLD=ROOT/'dependency_audit_v0_40'
read=lambda p:json.loads(p.read_text());sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
def write(p,d):p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n')
cfg=read(ROOT/'increment_v0_41.json');g=copy.deepcopy(read(OLD/'obligation_map.json'))
g['artifact_version']='0.41';g['predecessor_graph']={'file':'dependency_audit_v0_40/obligation_map.json','sha256':sha(OLD/'obligation_map.json')}
nodes={n['id']:n for n in g['nodes']}
def evidence(c):return dict(component=c,claims=cfg['component_claims'][c],ledger=c+'/provenance.json',ledger_sha256=sha(ROOT/c/'provenance.json'),proof_file=c+'/main.tex',proof_sha256=sha(ROOT/c/'main.tex'))
def refine(k,contract,comps):
 n=nodes[k];n['previous_interface']=copy.deepcopy(n);n.update(contract=contract,introduced_or_refined_in='0.41');n.setdefault('evidence',[]).extend(evidence(c) for c in comps)
ordcom=['neat_levels','ordinary_theta_weight'];ratcom=['rational_theta'];loccom=['local_hecke_projection']
ordc=sum((cfg['component_claims'][c] for c in ordcom),[]);ratc=cfg['component_claims']['rational_theta'];locc=cfg['component_claims']['local_hecke_projection']
oldcount=nodes['COUNT_II_SUPPORT']['contract']
old_sentence='Current C producers are earlier: original ordinary/control/separating arithmetic fibers and type/neatU/TThetaEx; four Hida endpoints on this same J; all-level same-J TWAut/HasAut on both Links.'
assert old_sentence in oldcount
new_sentence=('Full original neatU is now reconstructed for every QData, arbitrary integral tau0 and every compact-open K, using the same stored odd unramified auxiliary prime. Full original TThetaEx now constructs one theta in the entire complete coefficient ring before every K, through the actual artOf and the exact inverse cyclotomic adjustment; neatU gives IsWt. OTW13 assembles every UnitaryHeckeData field using inherited CAP17 IsRes once the complete original TypeForAlt is supplied. Current C producers are therefore the original integral TypeForAlt and remaining HSet.Ax, ordinary/control/separating arithmetic fibers; the four Hida endpoints on this same J; and all-level same-J TWAut/HasAut on both Links. Neither neatU nor TThetaEx nor the supplied-type HdEx record assembly remains an unspecified producer. The complete integral-type antecedent, including every required Teichmuller lift and IsRecT, has not been weakened.')
proposal=read(ROOT/'continuation_notes_v0_41/count_ii_contract_replacements.json')
assert proposal['canonical_node']['old_contract']==oldcount
refine('COUNT_II_SUPPORT',proposal['canonical_node']['replacement_contract'],ordcom)
# These are current work-planning annotations, not new selected logical nodes.
# The frozen component contracts and all older interface cuts stay unchanged.
g['current_count_subcontracts_v0_41']=copy.deepcopy(proposal['current_subcontracts'])
refinement_index={n['id']:n for n in g['work_refinement_nodes']}
for change in proposal['current_work_refinement_replacements']:
 n=refinement_index[change['id']]
 assert n['contract']==change['old_contract'],change['id']
 n['previous_interface_v0_40']=copy.deepcopy(n)
 n.update(contract=change['replacement_contract'],status=change['status'],introduced_or_refined_in='0.41')
 n['version_0_41_source_proposal']='continuation_notes_v0_41/count_ii_contract_replacements.json'
 for k in ['no_new_logical_gate','no_whole_count_ii_closure']:
  if k in change:n[k]=change[k]
refine('BASE_THETA_RATIONAL_TESTS',
 'On the SAME original Bundle/reading/theta map, for every i<m supply one finite separating complex-linear test family whose values lie in the fixed embedded coefficient field on theta of EVERY original rational source vector and on EVERY stored target-coordinate basis vector. BTH8/BTH11 use this same LiftTestB for rational adjoint image and matrix coordinates. RTG now reconstructs prescribed-field coefficient extension, original split class representatives/RepsOK, the self-dual split-lattice square law and finite residue PhiIs; every Pins field follows from the actual CoversAt. With the base coefficient record literally fixed, exact class-sum existence/uniqueness including phase-rescaled O, PointIdentCore with common lambda,z before every O, and base ClassSumsSpan imply all-tuple finite lift span and OneMapOverL. The phase is exactly cj(twAt embLL A3.A.v0)(R.phs i). RatG uses the actual good projector eOp(y), and full LiftTestB follows at BOTH original levels. These finite implication proofs are complete. Remaining original producers are the prescribed higher covers, those actual class sums/uniqueness, PointIdentCore, base ClassSumsSpan and the base/common geometric datum; exact MLat is supplied only from original LatFull, whose geometric production remains separate. Finite dimension or an unrelated rational theta model cannot replace these same-object identities. Original outer eventual-family/Bundle quantifiers remain.',ratcom)
refine('LOCAL_NBUILT_COMMON',
 'Construct, with the required closed-class property on the same Des(C,3), one eventual family of actual NBuilt certificates for the original Fm.D(x,i), retaining the certificate before forgetting to TSel. HLP now reconstructs full HeckeLift0, all-index commutation, HeckeStd0 and HeckeIntTw from the original MtInput and complex Hecke facts, in the full ambient GenAt range k<=nV. Every maximal ideal is an actual supported residual character class; literal MtSub is the O-span of projections of the original MtLat generators, is finite free, and localizes onto the exact NCov.part. Literal Psi has its exact range and off-space projection error, both original span assertions hold, and ActEx/ActHK are constructed on the same lattice under original semisimplicity. Original MjLat relation quotients, universal coefficient-map relation fields, selected tame generators, coefficient embeddings and all identity transports give the complete nonempty_spec constructor on its full printed input list. A single compositum combines the four original coefficient requirements with big fixed beforehand. Whole ndSpec_exists still needs actual common geometric/choice MtInput, complex HeckeStdPlain and the no-Jordan producer, original F3 bridges with valuation/GoodCoef/iq, original F4 common-overfield reading of the entire coefficient field, and exact arithmetic character/reciprocity/admissibility suppliers. Original AutSpec, Galois specialization and the remaining NBuilt fields on that same installation also remain. Do not replace the actual projected lattice or maps by abstract objects with the same dimensions.',loccom)
rat_append=(' Version 0.41 supplies the finite phase-correct rational theta route: exact coefficient extension, split representatives, square-law/PhiIs, Pins from CoversAt, class-sum/point-identity transfer to OneMapOverL, actual-good-projector RatG and both-level LiftTestB. Its original higher covers, all-tuple class-sum uniqueness including phase rescaling, one PointIdentCore before O, base ClassSumsSpan and geometric LatFull remain explicit producers. MLat is available from the original LatFull input. This sharpens the rational-test work without claiming actual common geometry, Fits or eta agreement.')
for k in ['DESIGN_CHOICES_COMMON','BASE_THETA_READINGS','CERT_BASE_THETA_REDUCTION','SECOND_LAYER_COMPATIBLE_SELECTION']:
 refine(k,nodes[k]['contract']+rat_append,ratcom)
g['nodes']=list(nodes.values())
def closure(c):return {'file':c+'/closure.json','sha256':sha(ROOT/c/'closure.json')}
neword=['FULL_ORIGINAL_NEATU','FULL_ORIGINAL_TTHETAEX','HDEx_ASSEMBLY_GIVEN_TYPEFORALT']
newrat=['PRESCRIBED_FIELD_COEFF_EXTENSION','ORIGINAL_SPLIT_REPS_AND_SQUARELAW','ORIGINAL_PHIIS','PINS_FROM_ORIGINAL_COVERS','PHASE_CORRECT_ONEMAPOVERL_TRANSFER','ORIGINAL_RATG_GOOD_PROJECTOR','BOTH_LEVEL_LIFTTESTB','MLAT_FROM_ORIGINAL_LATFULL']
newloc=['ORIGINAL_HECKELIFT0_STD_INT','ALL_MAXIMAL_IDEAL_SUPPORT','ORIGINAL_MTSUB_MTLOC_PSI_PROJECTION','ORIGINAL_ACTEX_ACTHK','ORIGINAL_MJLAT_RELATION_QUOTIENT','FULL_NONEMPTY_SPEC_CONSTRUCTOR','ONE_FOUR_REQUIREMENT_COEFFICIENT_COMPOSITUM']
g['selected_interface_cuts']['count_ii_v041']=dict(
 completed='Full original neatU and full TThetaEx; exact HdEx assembly after the original complete TypeForAlt. Selected Raw remains complete from v0.40.',
 nested_closed_claims=ordc,newly_closed_nested=neword,remaining=['COUNT_II_SUPPORT'],
 remaining_nested=['ORIGINAL_INTEGRAL_TYPEFORALT','REMAINING_HSET_AX_ORDINARY_CONTROL_SEPARATING_FIBERS','JSP_FOUR_HIDA_ENDPOINTS','JSP_SAME_IDEAL_HASAUT'],
 binding='Both original rank-four Links, ell=3, fixed iota, one common coefficient threshold before every later DVR and original same B,J. One theta before every original compact-open K, actual artOf, arbitrary integral tau0 and original QData. Complete TypeForAlt quantifiers retained.',
 scope='No whole Count-II closure or unconditional integral-type production. No alternate Artin map, ell>n assumption or replacement ideal. The selected h=0,a=n=4,k.g=0 Raw theorem remains available.',component_closures=[closure(c) for c in ordcom])
g['selected_interface_cuts']['count_ii_v041']['canonical_subcontracts']=[x['id'] for x in proposal['current_subcontracts']]
g['selected_interface_cuts']['rational_theta_v041']=dict(
 completed='Exact finite prescribed-field, class-representative, square-law, PhiIs, Pins, phase-normalized OneMapOverL, good-projector RatG and both-level LiftTestB constructions; MLat on the original LatFull input.',
 nested_closed_claims=ratc,newly_closed_nested=newrat,remaining=['BASE_THETA_RATIONAL_TESTS','DESIGN_CHOICES_COMMON'],
 remaining_packets=['PRESCRIBED_HIGHER_COVERS','CLS_EX_AND_UNIQUENESS_FOR_ALL_AND_RESCALED_O','POINT_IDENT_CORE_ONE_LAMBDA_Z_BEFORE_O','BASE_CLASS_SUMS_SPAN','ACTUAL_GEOMETRIC_LATFULL','ACTUAL_BASE_COMMON_DATA_AND_OUTER_FAMILY'],
 phase='cj(twAt embLL A3.A.v0)(R.phs i)',
 binding='Same T,R,F,kappa,v0,O, actual coefficient record, fieldRange embLL, measures and metrics; actual eOp projection; one lambda,z before O and both original levels.',
 outside_scope='No geometric CoversAt/ClsEx/PointIdentCore/ClassSumsSpan/LatFull producer inferred from a finite algebra wrapper; whole common construction and second DivRows3 remain open.',component_closures=[closure(c) for c in ratcom])
g['selected_interface_cuts']['local_hecke_v041']=dict(
 completed='Full finite Hecke localization and exact nonempty_spec constructor under its printed original input list.',nested_closed_claims=locc,newly_closed_nested=newloc,
 remaining=['LOCAL_NBUILT_COMMON'],remaining_packets=['ACTUAL_COMMON_MtInput_AND_CHOICE_DATA','COMPLEX_HECKESTDPLAIN_AND_NO_JORDAN','ORIGINAL_F3_BRIDGES_GOODCOEF_IQ','ORIGINAL_F4_FULL_COMMON_READING','ARITHMETIC_CHARACTER_RECIPROCITY_ADMISSIBILITY','ORIGINAL_AUTSPEC_AND_OTHER_NBUILT_FIELDS'],
 binding='Full ambient GenAt k<=nV; same complex embedding, actual iV/MtSub/Psi/prMt, all original maximal ideals and exact action; MjLat relation module distinct from MtLat; big before output and one four-field compositum.',
 scope='Does not assert unconditional ndSpec_exists or NBuilt. Semisimple transfer retains original complex no-Jordan input; F3/F4 and arithmetic character suppliers remain explicit.',component_closures=[closure(c) for c in loccom])
g['selected_interface_cuts']['theta_v041']=dict(previous_complete_leaf='BASE_THETA_CUSPIDAL_EXTENSION remains complete.',
 new_progress='Exact finite phase-correct rational-test construction and actual local finite projection/action constructor are reconstructed under their respective original suppliers.',remaining=['BASE_THETA_READINGS','BASE_THETA_RATIONAL_TESTS','SLR_BASE_ROWS_PRODUCER'],
 guard='Original common geometry, higher covers/class sums/point identity/spanning/LatFull, actual arithmetic local coefficient/character suppliers, Fits, eta and outer family quantifiers remain.')
g['source_inputs']={'predecessor_graph':copy.deepcopy(g['predecessor_graph'])}
g['source_inputs']['count_ii_current_contract_proposal']={'file':'continuation_notes_v0_41/count_ii_contract_replacements.json','sha256':sha(ROOT/'continuation_notes_v0_41/count_ii_contract_replacements.json')}
for c in cfg['components']:
 for stem in ['provenance','closure','published_applications']:
  p=ROOT/c/(stem+'.json')
  if p.is_file():g['source_inputs'][c+'_'+stem]={'file':p.relative_to(ROOT).as_posix(),'sha256':sha(p)}
if (AUD/'main.tex').exists():g['source_inputs']['current_narrative']={'file':'dependency_audit_v0_41/main.tex','sha256':sha(AUD/'main.tex')}
changes={
 'COUNT_II_SUPPORT':dict(claims=ordc,closed='Full neatU/TThetaEx and original HdEx assembly after TypeForAlt.',retained='Integral TypeForAlt, remaining ordinary/control/separating fibers, four Hida endpoints and all-level same-J HasAut on both Links.'),
 'RANK4_JOINT_ORDINARY_SUPPORT':dict(claims=ordc,closed='The all-level neatness and theta/weight producers now precede the already completed selected Raw.',retained='Complete integral type and original ordinary/Hida/same-J automorphic inputs; ell=3, fixed iota and common coefficient threshold.'),
 'GLOBAL_DESIGN':dict(claims=ratc,closed='Phase-correct finite rational theta/test algorithms with actual good projector.',retained='Same original geometric CoversAt/ClsEx/PointIdentCore/ClassSumsSpan/LatFull, Fits, eta and other common inputs.'),
 'GLOBAL_LOCAL_THETA_BINDINGS':dict(claims=ratc+locc,closed='Full finite rational theta tests and exact local projection/action/nonempty_spec constructors.',retained='Actual common geometry and local coefficient/character/automorphic suppliers; no full NBuilt or common-family installation.'),
 'GLOBAL_LOCAL_COVERAGE':dict(claims=locc,closed='All actual maximal ideals, finite free projected lattice, Psi/ActEx/ActHK and full original nonempty_spec assembly.',retained='Full ndSpec_exists arithmetic inputs, AutSpec and other NBuilt fields on the same original realization.'),
 'GLOBAL_SMALL_RANK':dict(claims=ratc,closed='Both-level exact LiftTestB and rational image from the original phase-correct RatG construction.',retained='Geometric source suppliers, base rows, original chain/group and common-family inputs.'),
 'GLOBAL_ACTUAL_ROW_SPECTRUM':dict(claims=locc,closed='Finite local Hecke algebra, literal action and supported points supplied on exact original form and arithmetic inputs.',retained='Actual ambient MtInput, complex Hecke standard/normality, coefficient and automorphic producers; no numerical spectrum inferred from abstract points.')}
disp=copy.deepcopy(read(OLD/'target_disposition.json'));disp['version']='0.41';disp['predecessor_disposition']={'file':'dependency_audit_v0_40/target_disposition.json','sha256':sha(OLD/'target_disposition.json')}
prior=read(ROOT/'history/version_0_40/next_source_targets.json')['targets'];assert len(prior)==len(disp['records'])==245
for t,r in zip(prior,disp['records']):
 assert t.get('id')==r['original_id']
 r['predecessor_record_sha256']=hashlib.sha256(json.dumps(t,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()).hexdigest()
 r['version_0_41_scope_updates']=[dict(frontier=k,**v) for k,v in changes.items() if k in r.get('frontier_ids',[]) or k in r.get('canonical_count_node_ids',[])]
 r['version_0_41_disposition_policy']='Every inherited compound scope retained; neatU/TThetaEx and exact finite constructors close inside it. No whole selected-leaf closure.'
for change in proposal['active_target_replacements']:
 r=disp['records'][change['original_index_one_based']-1]
 assert r['id']==change['id'] and r['original_id']==change['original_id']
 existing=[x for x in r['version_0_41_scope_updates'] if x['frontier']!='COUNT_II_SUPPORT']
 r['version_0_41_scope_updates']=existing+[copy.deepcopy(change['append_annotation'])]
 r['version_0_41_count_contract_reference']='COUNT_II_SUPPORT'
 r['version_0_41_count_subcontract_references']=[x['id'] for x in proposal['current_subcontracts']]
assert len(proposal['active_target_replacements'])==17
disp['current_selected_frontier']='dependency_audit_v0_41/obligation_map.json';disp['coverage']['records_with_v041_scope_updates']=sum(bool(r['version_0_41_scope_updates']) for r in disp['records'])
write(AUD/'target_disposition.json',disp)
g['backlog_crosswalk']={'file':'dependency_audit_v0_41/target_disposition.json','sha256':sha(AUD/'target_disposition.json'),'records':245,'scope_groups':107,'meaning':'Every inherited compound target retained with explicit current inner-producer boundaries.'}
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
  if v not in seen:seen.add(v);todo+=nodes[v]['requires']
 return seen
rh=reach('ORDINARY_RH');grh=reach('DIRICHLET_GRH');assert rh|grh==set(nodes)
leaves=[n for n in nodes.values() if n['gate']=='LEAF' and n['status'] not in ['proved_in_stated_scope','published_application_checked']]
assert len(nodes)==121 and len(rh)==101 and len(grh)==110 and len(leaves)==33
assert collections.Counter(n['category'] for n in leaves)=={'C':22,'B':9,'D':2}
oldnodes={n['id']:n for n in read(OLD/'obligation_map.json')['nodes']}
assert all(n['gate']==oldnodes[k]['gate'] and n['requires']==oldnodes[k]['requires'] for k,n in nodes.items())
g['validation'].update(full_original_neatU_complete=True,full_original_TThetaEx_complete=True,
 HdEx_assembly_complete_with_original_TypeForAlt_retained=True,original_integral_type_producer_not_claimed=True,
 phase_correct_rational_theta_finite_transfer_complete=True,both_original_LiftTestB_levels_complete_on_inputs=True,
 geometric_rational_test_suppliers_retained=True,actual_local_Hecke_projection_action_complete_on_inputs=True,
 full_original_nonempty_spec_complete_on_original_inputs=True,unconditional_ndSpec_exists_and_NBuilt_not_claimed=True,
 additional_selected_whole_leaves_closed=0,new_Lean_build_performed=False)
write(AUD/'obligation_map.json',g)
write(AUD/'remaining_leaf_register.json',dict(artifact_version='0.41',source_commit=g['source_commit'],category_key=g['categories'],scope=g['scope'],records=leaves,warning='Selected sufficient coupled obligations, not a completion percentage or absolute minimality theorem.'))
write(AUD/'closure_delta.json',dict(artifact_version='0.41',source_commit=g['source_commit'],changes=changes,closed_selected_leaves=[],closed_nested_producers=neword+newrat+newloc,prior_open_leaf_count=33,current_open_leaf_count=33,retained_historical_correction='RF16 governed by DEX11; historical bytes unchanged.'))
apps=[]
for c in cfg['components']:
 data=read(ROOT/c/'published_applications.json');items=data if isinstance(data,list) else data.get('applications',data.get('freshly_checked_applications',[]));apps.extend(dict(component=c,**a) for a in items)
assert len({a['id'] for a in apps})==len(apps)
write(AUD/'published_applications.json',dict(artifact_version='0.41',source_commit=g['source_commit'],freshly_checked_applications=apps,inherited_registry={'file':'dependency_audit_v0_40/published_applications.json','sha256':sha(OLD/'published_applications.json')},note='No new published theorem is required by this increment. Exact inherited CIP reciprocity and other certified inputs retain their original hypotheses.'))
print(json.dumps(dict(nodes=121,edges=sum(len(n['requires']) for n in nodes.values()),open=33,scope_updates=disp['coverage']['records_with_v041_scope_updates'],new_published_applications=len(apps)),indent=2))
