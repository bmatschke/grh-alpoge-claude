#!/usr/bin/env python3
"""Refine the selected sufficient proof audit without erasing historical scopes."""
from pathlib import Path
import copy,hashlib,json,collections
ROOT=Path(__file__).resolve().parent
AUDIT=ROOT/'dependency_audit_v0_32';OLD=ROOT/'dependency_audit_v0_31'
PIN='7cbf7a0c32fca1badf05931879a37c3f8a2b03b4'
def read(p):return json.loads(p.read_text())
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def write(p,d):p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n')
cfg=read(ROOT/'increment_v0_32.json')
g=copy.deepcopy(read(OLD/'obligation_map.json'))
g['artifact_version']='0.32'
g['predecessor_graph']={'file':'dependency_audit_v0_31/obligation_map.json','sha256':sha(OLD/'obligation_map.json')}
nodes={n['id']:n for n in g['nodes']}
def evidence(component,claims):
 return dict(component=component,claims=claims,ledger=component+'/provenance.json',ledger_sha256=sha(ROOT/component/'provenance.json'),proof_file=component+'/main.tex',proof_sha256=sha(ROOT/component/'main.tex'))
def add(ident,title,cat,contract,requires=(),status=None,kind=None,proofs=()):
 n=dict(id=ident,title=title,category=cat,kind=kind or ('implication_certificate' if status=='proved_in_stated_scope' else 'proof_obligation'),status=status or ('proved_implication_with_open_inputs' if requires else 'open_original_producer'),contract=contract,gate='AND' if requires else 'LEAF',requires=list(requires),evidence=list(proofs),introduced_or_refined_in='0.32')
 if ident in nodes:n['previous_interface']=copy.deepcopy(nodes[ident])
 nodes[ident]=n
 return n
def closed(ident,title,contract,comp,ids):return add(ident,title,'B',contract,status='proved_in_stated_scope',proofs=[evidence(comp,ids)])

closed('TASK_GL3_GAP_DEGREE','Original formal-degree h3 is installed',
 'DSZ1–DSZ3 prove the actual SigmaDegreeTwoSidedBoundOfGap on every supplied FamP, using the literal cdScaleTie/dsigTie. The source gap exceeds the general DC1–DC12 construction/rigidity threshold, and HC-Deg retains its exact DC18 compact-dual normalization. Closed may use epsilon1=1,K=0. This certificate does not construct an unrelated or new family.',
 'degree_prime_size',['DSZ1','DSZ2','DSZ3'])
closed('DESIGN_TUSIZE_CLOSED','Original construction-class TuSize implication',
 'DSZ4–DSZ10 prove Closed(Cdes,cTmin(CYL)<=CTu -> TuSize) for the actual construction class A=cls(Q,Lk,E), Bd=Bundle, and its target/WithChN/WithSm/WithTw subclasses. Membership supplies Built, hence RealTied and the previously proved exact volume identity. The same result is a universal Row.of_sel from actual IsSel, with extra predicate True. cT(eps,y)=max(11,16+3 max(5,y+1)), epsilon1=1,K=0; eventual thresholds may depend on the supplied family. A common compatible class member is not constructed.',
 'degree_prime_size',['DSZ'+str(i) for i in range(4,11)])
closed('DESIGN_RANKM_CLOSED','Original construction-class RankM implication',
 'RMP1–RMP11 prove the actual ClassNumberFormula₂, Mu0Tie and RankM. On A=cls(Q,Lk,E), Bd=Bundle, Link.pos/QOf gives cls_at/pick and the same Bundle.R columns. For Cprime=WithChN(A intersect target class) and Cdes=WithTw(WithSm Cprime), Closed eventual RankM uses epsilon1=1,K=0 and the inner threshold Fm.x1+1 (or max(as,Fm.x1+1) for a separately supplied original TSel). There is no independent rank-selector obligation in this construction-class scope. Actual common class-member existence remains DESIGN_CHOICES_COMMON.',
 'rank_producer',['RMP'+str(i) for i in range(1,12)])
add('DESIGN_CHOICES_COMMON','Construct the original common design family and bundle','C',
 'For the one target HostExW, construct the original compatible DesignChoices on Cdes=WithTw(WithSm Cprime), where Cprime=WithChN(A intersect target class), A is the one Built construction class, and cT(eps,y)=cTmin(y). Retain every original field, tuple, word, metric and common bundle duty. DSZ10 and RMP11 prove the size/rank properties of members of this class; they do not produce a member. The RecExP/RecAtG and common object/row route remains a coupled construction.',
 proofs=[evidence('degree_prime_size',['DSZ10']),evidence('rank_producer',['RMP11']),evidence('design_existence',['DEX7','DEX8','DEX9','DEX10','DEX11'])])
add('GLOBAL_DESIGN','Exact compatible design after its common family producer','B',
 'Literal DesignExists follows on the one original construction class with cT=cTmin. The DEX three-input assembly remains unchanged; the two size/rank inputs are now proved on exactly that class. Actual compatible DesignChoices is the sole remaining selected design producer.',
 ['DESIGN_CHOICES_COMMON','DESIGN_TUSIZE_CLOSED','DESIGN_RANKM_CLOSED','CERT_DESIGN_REDUCTION'])

gle=[
 ('TASK_GL6_SIZE_SETTING','Every original late member satisfies HidaSetting',
  'GLE1–GLE2: the actual ParameterChoice windows and lower TuSize bound give lambda in [-2b,2xb], b>=24x, b>=3N, amax<=2xb, bTop>=0 and eventually T>=b^2. These verify every strict original HidaSetting clause, uniformly before i,u. No full NumsL, upper logT or DlSize supplier is required.',['GLE1','GLE2']),
 ('TASK_GL6_INTEGRAL','Original up/down integrality on the actual lattices',
  'GLE3–GLE5: the same original Forms0, finite K-valued level character and admS give exact rational polynomial coordinates, original S/B lattice equalities, U(B) subset S and D(S) subset B. Original local moves, all coefficient-place embeddings, determinant shifts and character units are retained. In a family, apply only after the same original second-layer supplier threshold.',['GLE3','GLE4','GLE5','GLE12']),
 ('TASK_GL6_RAMIFIED','Original ramified stability and inverse composite',
  'GLE7–GLE9: original lattice/functional moves, exact character-one comparison and finite DU fibers prove the literal DU formula, diamond commutations, preservation of Mram and UD=T^(k-1) on it. The same supplied Forms0/character/admS are used. This is the pointwise source implication, uniformly installed by GLE12; it does not produce those compatible forms.',['GLE7','GLE8','GLE9','GLE12']),
 ('TASK_GL6_SECOND_BRANCH','Original second-branch inclusion and exact length',
  'GLE3–GLE6: with the same original Forms0/admS and b_v>=0, T^b_v S subset B and length(B/T^b_v S)=e_w d_S (|lambda|+k b_v)/k. The actual neighbor kernel has colength one; integral row-degree bases and determinant shifts give the exact elementary divisors. Here |lambda| is the signed sum of weights and d_S the full original dimension.',['GLE3','GLE4','GLE6','GLE12']),
 ('TASK_GL6_CONGRUENCE_LENGTH','Original ordered composite and congruence length',
  'GLE10–GLE11: on the same supplied forms and HidaSetting, the one-operator DVR exact sequences, original ordered product and its mth power identify Nlam as an actual submodule of Sram with finite cokernel and the complete source length bound. The unseen-place empty product is identity. No commutativity of differently ordered factors is assumed. GLE12 retains all upstream selector and Closed thresholds.',['GLE10','GLE11','GLE12'])]
for ident,title,contract,ids in gle:closed(ident,title,contract,'global_local_estimates',ids)
add('GLOBAL_RAMIFIED_INCLUSION','Original ramified inclusion after the shared second layer','B',
 'The actual eventual original second-layer conditions supply the same forms and finite character, RSL7 supplies admS, and D3 membership supplies TuSize. The completed GLE size/integral/ramified/second-branch implications then prove Nlam subset Sram with one maximum threshold. The shared second-layer producer remains explicit; no independent inclusion producer or GL4 estimate is required.',
 ['GLOBAL_REAL_SECOND_LAYER','TASK_GL6_SIZE_SETTING','TASK_GL6_INTEGRAL','TASK_GL6_RAMIFIED','TASK_GL6_SECOND_BRANCH','CERT_RSL_OPERATOR_INCLUSION'],
 proofs=[evidence('global_local_estimates',['GLE12'])])
nodes['CERT_RSL_OPERATOR_INCLUSION']['previous_interface']=copy.deepcopy(nodes['CERT_RSL_OPERATOR_INCLUSION'])
nodes['CERT_RSL_OPERATOR_INCLUSION']['contract']='The RSL7–RSL10 same-form operator consumer is retained. GLE1–GLE2 now supply its original eventual size-setting condition, and GLE3–GLE11 supply the integral, ramified, second-branch and composite-length implications on those exact original forms. Their common second-layer producer is explicit in GLOBAL_RAMIFIED_INCLUSION; no class member is inferred.'
nodes['CERT_RSL_OPERATOR_INCLUSION']['version_0_32_evidence']=[evidence('global_local_estimates',['GLE1','GLE2','GLE12'])]
add('TASK_LINK_GL_INSTALL','Remaining original global-slope reconstruction tasks','B',
 'The h3 and five GL6 implication tasks below are now complete on their exact original supplied inputs. Finish the three actual GL4 slots and the final global numerical/lattice assembly. This AND rule retains all original slots and the mass/second-layer context supplied to GLOBAL_GL_PAIR; completed certificates do not create that context.',
 ['CERT_RSL_RAMIFIED_MODEL','TASK_GL3_GAP_DEGREE','TASK_GL4_SLOPE_LOWER','TASK_GL4_SLOPE_MAX','TASK_GL4_COLUMN_VALUES']+[a[0] for a in gle]+['TASK_GL_FINAL_ASSEMBLY'],
 status='human_proof_still_required',kind='implication_reconstruction_task',proofs=[evidence('global_local_estimates',['GLE12']),evidence('degree_prime_size',['DSZ3'])])

closed('CERT_BASE_THETA_REDUCTION','Convergence and the original base theta square from a smaller producer',
 'BTH1–BTH15: smooth-topology lowest-type uniqueness, absolute convergence on the original definite quotient, finite-basis extension assembly, original weak-choice activation, finite character/equivariance/unitarity, explicit geometric theta witness, rational adjoint image, idempotent kernel argument and actual rational relation matrix yield the original base thTheta. BTH13–BTH15 prove adelic character rigidity, uniqueness on the original theta space and the exact finite lattice-stabilizer character of the actual action. Retain one common original reading, basis extensions and simultaneous rational tests; no full ExAt, nonbase tests, PLevW/LUnif/H5 or positive theta-norm theorem is an additional input to this base consumer.',
 'base_theta',['BTH'+str(i) for i in range(1,16)])
theta=[
 ('BASE_THETA_READINGS','Actual base reading on the common bundle',
  'For every family in the original class, eventually on the SAME selected Bundle and for each i<m, supply the actual R,F,Read,ReadL, weak models/Weil data and phase-one pins. Identify their LiftTie.theta, mtRead, mjRead and ThDef3 basis with that Bundle.P.A3, P.Zs, P.S0 and its stored maps. Exact field, embeddings, metrics, measures, row family and weak choices are retained. This is one part of the coupled BTH12 producer, not a freely replaceable isomorphic model.'),
 ('BASE_THETA_CUSPIDAL_EXTENSION','Extend the original convergent base integrals',
  'On the SAME selected Bundle and the SAME reading as BASE_THETA_READINGS, for each i<m extend the exact lowest-type theta integral for every vector of one finite basis of HV(i,t0) to the original Wall_i. Absolute convergence is already BTH3. The remaining assertion includes smoothness, equivariance, cuspidality, prescribed finite level and Sobolev-continuous multiplicity realization. Supply these with one family threshold before i and the basis vectors.'),
 ('BASE_THETA_RATIONAL_TESTS','Simultaneous original base rational tests',
  'On the SAME original Bundle/reading/theta map, for every i<m supply one finite separating complex-linear test family. Its values must lie in the fixed embedded coefficient field on theta of EVERY original rational source vector and on EVERY stored target-coordinate basis vector. BTH8 and BTH11 use this one base LiftTestB family for rational adjoint image and matrix coordinates. Finite dimensionality alone does not supply these rationality identities.'),
 ('SLR_BASE_ROWS_PRODUCER','Actual base row identities on that same bundle',
  'For the SAME selected Bundle, common original fields and readings used by the other three BTH12 inputs, supply actual RowsHold0_3 uniformly eventually for every family. Its original primitive row realization, spectrum/type and basis identifications must be retained. BTH supplies a theta consumer only; it does not construct the base row identity. No separate witness may be chosen merely to satisfy this row requirement.')]
for ident,title,contract in theta:add(ident,title,'C',contract,proofs=[evidence('base_theta',['BTH12'])])
add('SLR_SAME_BUNDLE_BASE_PRODUCER','Coupled base rows and theta through the refined producer cut','B',
 'BTH12 plus the existing SLR consumer: the four exact inputs below are jointly supplied on one common Bundle and reading, with a common eventual threshold. The first three give its original base theta square; the fourth supplies RowsHold0_3. These are coupled predicates on the selected object, not four independent existential models. If supplied only in a weaker Closed form, retain each original epsilon/K bound before taking the inner maximum threshold.',
 [t[0] for t in theta]+['CERT_BASE_THETA_REDUCTION'],proofs=[evidence('base_theta',['BTH12'])])
g['nodes']=list(nodes.values())
g['selected_interface_cuts']['design_v032']=dict(inputs=['DESIGN_CHOICES_COMMON'],proved_inputs=['DESIGN_TUSIZE_CLOSED','DESIGN_RANKM_CLOSED'],certificate='CERT_DESIGN_REDUCTION',binding='Exact Built construction class, cT=cTmin, target intersection, and one common original Bundle; no nonemptiness inferred.')
g['selected_interface_cuts']['base_theta_v032']=dict(inputs=[t[0] for t in theta],certificate='CERT_BASE_THETA_REDUCTION',binding='Joint predicates on the same selected Bundle and original R/F/Read/ReadL. Three theta inputs plus base rows; same family threshold or retained Closed bounds.')
g['selected_interface_cuts']['global_v032']=dict(completed=['TASK_GL3_GAP_DEGREE']+[t[0] for t in gle],remaining=['TASK_GL4_SLOPE_LOWER','TASK_GL4_SLOPE_MAX','TASK_GL4_COLUMN_VALUES','TASK_GL_FINAL_ASSEMBLY'],binding='Compatible actual second-layer forms/character remain upstream; every completed local implication uses those same objects.')
g['selected_interface_cuts']['fullness_v032']=dict(inputs=['GLOBAL_REAL_SECOND_LAYER'],completed_rule='GLOBAL_RAMIFIED_INCLUSION and RSL fullness',binding='D3 supplies TuSize; GLE supplies its setting and actual local inclusion on the same forms. The common second-layer producer remains C.')
for n in g['work_refinement_nodes']:
 if n['id']=='DESIGN_RECURSIVE_CORE':n['version_0_32_update']='Actual RecAtG/common object/Bundle construction remains. DSZ10 and RMP11 remove independent size/rank tasks on its class.'
 if n['id']=='GLOBAL_LOCAL_THETA_BINDINGS':n['version_0_32_update']='BTH supplies exact base convergence, finite Hilbert/adjoint/rational-matrix consumer and a three-part coupled theta cut. The actual common reading, smooth cuspidal extension and rational tests remain C.'
 if n['id']=='GLOBAL_ACTUAL_ROW_SPECTRUM':n['version_0_32_update']='Base RowsHold0_3 remains a separate C predicate on the same Bundle. BTH does not claim its primitive realization or spectral/rationality producer.'
for leaf in [t[0] for t in theta]:
 g['work_refinement_links'].append(dict(consumer=leaf,dependency='GLOBAL_LOCAL_THETA_BINDINGS',logical=False,relation='work_refinement',rationale='Shared same-object geometric/analytic reading; not an additional sufficient logical proof rule.'))

g['source_inputs']={'predecessor_graph':g['predecessor_graph']}
for comp in cfg['components']:
 for file in ['provenance.json','closure.json']:
  p=ROOT/comp/file
  if p.exists():g['source_inputs'][comp+'_'+file.split('.')[0]]={'file':comp+'/'+file,'sha256':sha(p)}
if (AUDIT/'main.tex').exists():g['source_inputs']['current_narrative']={'file':'dependency_audit_v0_32/main.tex','sha256':sha(AUDIT/'main.tex')}
changes={
 'GLOBAL_DESIGN':dict(claims=['DSZ10','RMP11'],closed='Original construction-class Closed TuSize and RankM, literal class number and exact level-prime size.',retained='Actual compatible DesignChoices/common class-member construction and shared Bundle duties.'),
 'GLOBAL_SMALL_RANK':dict(claims=cfg['component_claims']['base_theta'],closed='Base integral convergence, smooth-vector uniqueness, finite Hilbert/adjoint/level and rational theta-matrix implication.',retained='Same-Bundle actual reading, smooth cuspidal extension, simultaneous rational tests and RowsHold0_3.'),
 'GLOBAL_LOCAL_THETA_BINDINGS':dict(claims=cfg['component_claims']['base_theta'],closed='The exact base theta sufficient reduction and original stored-map identifications under its displayed common reading.',retained='Actual geometric/analytic reading and extensions/tests; nonbase period and row requirements keep their distinct scopes.'),
 'GLOBAL_ACTUAL_ROW_SPECTRUM':dict(claims=['BTH12'],closed='Exact separation of base row producer from the now reduced theta consumer.',retained='Actual RowsHold0_3, rational row spectra and original common row realization.'),
 'GLOBAL_FULL_RANK':dict(claims=['GLE2','GLE5','GLE6','GLE9','GLE11','GLE12'],closed='Original local inclusion and complete operator/length implications from the same second-layer forms; RSL fullness then applies.',retained='Actual compatible second-layer selector/real witness; unrelated fullness components of historical compound scopes remain.'),
 'GLOBAL_SLOPE':dict(claims=['DSZ3']+cfg['component_claims']['global_local_estimates'],closed='Original h3, size-to-setting, both integral Hecke maps, ramified inverse, exact second-branch and composite length.',retained='Three original GL4 slots, actual same-selector input producer and final numerical/lattice assembly.'),
 'GLOBAL_SECOND_LAYER_MATCH':dict(claims=['RMP11','GLE12'],closed='Same-Bundle rank and local operator consumers need no fresh selector.',retained='The existing actual second-layer/common family and class-duty producer remains; its scopes are not replaced by a new independent witness.')}
disp=copy.deepcopy(read(OLD/'target_disposition.json'));disp['version']='0.32'
disp['predecessor_disposition']={'file':'dependency_audit_v0_31/target_disposition.json','sha256':sha(OLD/'target_disposition.json')}
oldtargets=read(ROOT/'history/version_0_31/next_source_targets.json')['targets']
assert len(oldtargets)==len(disp['records'])==245
for t,rec in zip(oldtargets,disp['records']):
 assert t.get('id')==rec['original_id'],('predecessor record identity',t.get('id'),rec['original_id'])
 rec['predecessor_record_sha256']=hashlib.sha256(json.dumps(t,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()).hexdigest()
 rec['version_0_32_scope_updates']=[dict(frontier=k,**v) for k,v in changes.items() if k in rec.get('frontier_ids',[])]
 rec['version_0_32_disposition_policy']='Retain every original compound scope and category; update only the stated subclaims. No whole record is erased because one consumer is proved.'
disp['current_selected_frontier']='dependency_audit_v0_32/obligation_map.json'
disp['category_count_policy']='Historical compound categories are navigation. Current selected leaves have their own A/B/C/D category and exact coupled contract; their count is not a completion percentage.'
disp['coverage']['records_with_v032_scope_updates']=sum(bool(r['version_0_32_scope_updates']) for r in disp['records'])
write(AUDIT/'target_disposition.json',disp)
g['backlog_crosswalk']=dict(file='dependency_audit_v0_32/target_disposition.json',sha256=sha(AUDIT/'target_disposition.json'),records=245,scope_groups=107,meaning='All inherited compound scopes retained, with precise current subclaim reductions.')
def reachable(root):
 seen=set();todo=[root]
 while todo:
  k=todo.pop();assert k in nodes,('missing node',k)
  if k in seen:continue
  seen.add(k);todo+=nodes[k]['requires']
 return seen
active=set();done=set()
def visit(k):
 assert k not in active,('cycle',k)
 if k in done:return
 active.add(k)
 for dep in nodes[k]['requires']:visit(dep)
 active.remove(k);done.add(k)
for k in nodes:visit(k)
rh=reachable('ORDINARY_RH');grh=reachable('DIRICHLET_GRH');full=reachable('GLOBAL_FULL_RANK')
assert rh|grh==set(nodes)
assert 'COUNT_III_PRODUCER' not in rh and 'COUNT_III_PRODUCER' in grh
assert {'COUNT_I_PRODUCER','COUNT_II_SUPPORT','COUNT_V_PRODUCER'}<=rh&grh
assert not any(k.startswith('TASK_GL4') for k in full) and 'TASK_GL_FINAL_ASSEMBLY' not in full
openleaves=[n for n in nodes.values() if n['gate']=='LEAF' and n['status'] not in ['proved_in_stated_scope','published_application_checked']]
g['validation']=dict(logical_graph_acyclic=True,all_selected_nodes_reachable_from_roots=True,selected_node_count=len(nodes),work_refinement_node_count=len(g['work_refinement_nodes']),optional_node_count=len(g['optional_routes']),rh_reachable_count=len(rh),dirichlet_grh_reachable_count=len(grh),rh_excludes_every_case_III_producer=True,unrestricted_grh_includes_case_III=True,both_roots_reach_I_II_V=True,ten_exact_topDesWin_arguments_retained=True,same_ideal_count_II_coupling_retained=True,full_rank_excludes_GL4_and_final_slope_assembly=True,design_thresholds_before_one_family=True,construction_class_size_rank_closed_without_nonemptiness=True,base_theta_four_inputs_coupled_on_same_bundle=True,GL6_retains_original_second_layer_supplier=True,all_selected_open_leaves_classified=True,open_leaf_categories=dict(collections.Counter(n['category'] for n in openleaves)),predecessor_claim_graph_preservation_is_separate=True,new_Lean_build_performed=False)
write(AUDIT/'obligation_map.json',g)
write(AUDIT/'remaining_leaf_register.json',dict(artifact_version='0.32',source_commit=PIN,category_key=g['categories'],scope=g['scope'],records=openleaves,warning='Selected sufficient proof-task contracts, often coupled and overlapping; no completion percentage or absolute minimality claim.'))
write(AUDIT/'closure_delta.json',dict(artifact_version='0.32',source_commit=PIN,changes=changes,retained_historical_correction='RF16 is governed by DEX11 as recorded in v0.31; no historical proof bytes changed.'))
write(AUDIT/'published_applications.json',dict(artifact_version='0.32',source_commit=PIN,freshly_checked_applications=read(ROOT/'degree_prime_size/published_applications.json'),inherited_registry=dict(file='dependency_audit_v0_31/published_applications.json',sha256=sha(OLD/'published_applications.json')),note='The HC-Deg entry records the checked exact application retained from DC18 and used by DSZ; it is not a new classical assumption. Other prior applications retain their existing scopes.'))
print(json.dumps(g['validation'],indent=2))
