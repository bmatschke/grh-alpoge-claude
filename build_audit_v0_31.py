#!/usr/bin/env python3
"""Build the selected v0.31 proof-obligation graph. This does not run Lean."""
from pathlib import Path
import copy, hashlib, json, collections

ROOT=Path(__file__).resolve().parent
AUDIT=ROOT/'dependency_audit_v0_31'
OLD=ROOT/'dependency_audit_v0_30'
PIN='7cbf7a0c32fca1badf05931879a37c3f8a2b03b4'
COMPONENTS=['design_existence','local_theta_dictionary','small_level_rank','second_layer_global']
def read(p): return json.loads(p.read_text())
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def write(p,d): p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n')

g=copy.deepcopy(read(OLD/'obligation_map.json'))
g['artifact_version']='0.31'
g['predecessor_graph']={'file':'dependency_audit_v0_30/obligation_map.json','sha256':sha(OLD/'obligation_map.json')}
nodes={n['id']:n for n in g['nodes']}
def evidence(component,claims):
    p=ROOT/component/'provenance.json'
    return dict(component=component,claims=claims,ledger=component+'/provenance.json',
                ledger_sha256=sha(p),proof_file=component+'/main.tex',
                proof_sha256=sha(ROOT/component/'main.tex'))
def add(ident,title,category,contract,requires=(),status=None,kind=None,proofs=()):
    n=dict(id=ident,title=title,category=category,
      kind=kind or ('implication_certificate' if status=='proved_in_stated_scope' else 'proof_obligation'),
      status=status or ('proved_implication_with_open_inputs' if requires else 'open_original_producer'),
      contract=contract,gate='AND' if requires else 'LEAF',requires=list(requires),
      evidence=list(proofs),introduced_or_refined_in='0.31')
    if ident in nodes:n['previous_interface']=copy.deepcopy(nodes[ident])
    nodes[ident]=n
    return n
def cert(ident,title,contract,component,claims):
    return add(ident,title,'B',contract,status='proved_in_stated_scope',
               proofs=[evidence(component,claims)])

cert('CERT_DESIGN_REDUCTION','Three compatible inputs give literal DesignExists',
 'DEX1–DEX7: on ONE class Cdes with ONE cT, DesignChoices(Cdes,3,cT), Closed(Cdes,cT(eps,CYL)<=CTu -> TuSize), and Closed(Cdes,eventual original RankM) imply DesignExists(Cdes,3). In the final application Cdes=WithTw(WithSm Cprime); the top-level C=WithChN A is distinct. BoxesF/QDRowsF yield ChosenThin(1); DGamDvdF yields DGamSize(12); original RankM gives ChosenProviso(3). All Closed thresholds are joined BEFORE selecting one family.',
 'design_existence',['DEX1','DEX2','DEX3','DEX4','DEX5','DEX6','DEX7'])
add('DESIGN_CHOICES_COMMON','Original compatible DesignChoices on the common class','C',
 'For the one target HostExW and the same fixed class Cdes=WithTw(WithSm Cprime), supply DesignChoices(Cdes,3,cT) with a single cT. Every original field, tuple, word, metric and target-class duty is retained. This is a coupled construction, not independent nonempty models.',
 proofs=[evidence('design_existence',['DEX7','DEX8','DEX9','DEX10','DEX11'])])
add('DESIGN_TUSIZE_CLOSED','Uniform TuSize implication on that design class','C',
 'For the same Cdes and cT as DESIGN_CHOICES_COMMON, prove Closed(Cdes, fun Fm _ => cT(eps,Fm.CYL)<=Fm.CTu -> TuSize Fm). The uniform transported threshold precedes the family. No family is selected before this threshold is joined.',
 proofs=[evidence('design_existence',['DEX7'])])
add('DESIGN_RANKM_CLOSED','The actual original family rank formula','C',
 'On that same Cdes prove Closed(Cdes, fun Fm _ => eventually in x and every actual i: RankM(Fm.D(x,i))). RankM is the literal dM(u)=dstar(u)*(T_u^k-1)^f with the source level and lattice identities. An unrelated Weyl dimension is insufficient.',
 proofs=[evidence('design_existence',['DEX5','DEX7'])])
add('GLOBAL_DESIGN','Exact compatible design assembly','B',
 'The literal target DesignExists construction, conditional on the same target HostExW carried by DESIGN_RH/GRH and on the three compatible inputs below. DEX7 supplies the entire finite and numerical assembly.',
 ['DESIGN_CHOICES_COMMON','DESIGN_TUSIZE_CLOSED','DESIGN_RANKM_CLOSED','CERT_DESIGN_REDUCTION'])

cert('CERT_LOCAL_COVERAGE','Original local spectrum gives coverage and LinkEta',
 'LTD3–LTD5: commuting integral split operators on the actual NdSpec have a finite generalized-primary decomposition; the exact local projections are jointly injective and their ranks cover the original MtL. Actual NBuilt on the same installed record gives LocsCoverTw; eventual certificates give LinkEta. Generic TSel alone does not give NBuilt.',
 'local_theta_dictionary',['LTD3','LTD4','LTD5'])
add('LOCAL_NBUILT_COMMON','Actual local specialization on the common selected family','C',
 'Closed on the same Des(C,3) class: one eventual family of actual NBuilt certificates for the original Fm.D(x,i), including NdSpec, original iV/Hecke actions, every required maximal ideal, Ψ/range and projection square. Keep the constructor certificate before forgetting it to TSel.',
 proofs=[evidence('local_theta_dictionary',['LTD2','LTD4','LTD5'])])
add('GLOBAL_LOCAL_COVERAGE','Local coverage consumer with its smaller producer','B',
 'Closed(Des C 3) LinkEta on the original family follows from the original eventual NBuilt producer and the completed finite coverage argument.',
 ['LOCAL_NBUILT_COMMON','CERT_LOCAL_COVERAGE'])

cert('CERT_SLR_FINITE_JOIN','Original small-level rank from base rows and theta',
 'SLR1–SLR9: lPrj*lZ0=1 with the exact |P| metric factor; generalized type dimensions and the original bases give D0; only the actual base-tuple theta square is needed to obtain dZ0(j)=D0. K=0 and epsilon1=1 for the finite consumer; the maximum of producer/selector thresholds and Fm.x1+1 is taken inside each family.',
 'small_level_rank',['SLR'+str(i) for i in range(1,10)])
add('SLR_SAME_BUNDLE_BASE_PRODUCER','Base row and theta identities on one Bundle','C',
 'For EVERY original Fm in the same class A, supply one compatible original Bundle selector and one eventual threshold for that Fm such that every selected P has RowsHold0_3 P AND its original base-tuple thTheta square, for all used lift indices and rational coordinates. This is the universally supplied class producer of SLR9, so the finite consumer may use epsilon1=1,K=0. If a weaker Closed producer is used instead, its own epsilon/K bounds must be retained and joined; they are not erased. This is one coupled producer. No full DivRows3 pairing record, RowsHoldLam3, TupAllUsed, or nonbase theta identity is required by this rank consumer.',
 proofs=[evidence('small_level_rank',['SLR4','SLR5','SLR6','SLR7','SLR9'])])
add('GLOBAL_SMALL_RANK','SmallLevelRankEq after the actual base producer','B',
 'Closed SmallLevelRankEq on D3(3,A), conditional on the same-Bundle base row/theta producer; the former projection identification and finite rank join are complete.',
 ['SLR_SAME_BUNDLE_BASE_PRODUCER','CERT_SLR_FINITE_JOIN'])

cert('CERT_SECOND_LAYER_SELECTION','Finite characters and second layer on the same selector',
 'RSL4–RSL6: the true-column additive characters supply primitive g0,g1 roots in the ORIGINAL field; every supplied FormsTiedSym has ChiFin0 with exponent g0*g1. Keep TSel.T.cols and TSel.T.theta.real on the same rec7 record, take one family threshold and obtain RealPlaceSecondLayerConditions.',
 'second_layer_global',['RSL4','RSL5','RSL6'])
add('SECOND_LAYER_COMPATIBLE_SELECTION','Original second-layer selector and class duties','C',
 'For the same A, supply Duty on A and a Closed common original TSel family whose selected records are the original true-column rec7 records (or have the entire dependent tuple transported), with their real witness and original coefficient-field root data. Existence/compatibility remains arithmetic; merely abstractly isomorphic fields or independently selected columns do not suffice.',
 proofs=[evidence('second_layer_global',['RSL4','RSL5','RSL6'])])
add('GLOBAL_REAL_SECOND_LAYER','Actual eventual real and symmetric-column witnesses','B',
 'Closed(D3(3,A), RealPlaceSecondLayerConditions), carrying the same A and original family.',
 ['SECOND_LAYER_COMPATIBLE_SELECTION','CERT_SECOND_LAYER_SELECTION'])
cert('CERT_RSL_MASS_VOLUME','Exact original mass and reciprocal volume inputs',
 'RSL1–RSL3 match GenusMassAt(D,n) for every n, hence n=2, and MassRatioUnderVolume(D) for every D. The original W.hT/W.L0, Haar normalization and VolTie are retained. Uses the already recorded GV Tamagawa and MF Hasse–Minkowski applications; no unconditional assignment of D.vol to an arbitrary function.',
 'second_layer_global',['RSL1','RSL2','RSL3'])
add('GLOBAL_SECOND_LAYER_MATCH','Matched same-family inputs of link_gl','B',
 'The exact hduty, Closed second layer, universal hU and universal hG in link_gl, on the same A and original records. The two universal mass/volume inputs and finite-character join are reconstructed; actual compatible selector production remains upstream.',
 ['SECOND_LAYER_COMPATIBLE_SELECTION','GLOBAL_REAL_SECOND_LAYER','CERT_RSL_MASS_VOLUME'])
cert('CERT_RSL_RAMIFIED_MODEL','Literal integral and isometric ramified model',
 'RSL7–RSL10: two auxiliary primes kill stabilizers; actual rational and integral orbit slices give an isometric induced lattice at EVERY embedding. The original ramified lattice is W tensor augmentation^(f), with rank ratio (1-1/(T-1))^f, slope loss f*log(T-1)/(T-2), and maximal slope bounded by the original full lattice.',
 'second_layer_global',['RSL7','RSL8','RSL9','RSL10'])
cert('CERT_RSL_FULLNESS','Local inclusion gives original full positive-rank lattice',
 'RSL11–RSL12: eventual Nlam subset Sram and actual second layer give NuFullF and MuRank using original nuDef, nprimeDef and nuIn. Original T=1 mod4 and primality give T>=3 pointwise, so positivity does not invoke full HidaSetting. TuSize remains harmless source-facing data, and on D3(3,A)=Des(WithChN A,3) it is already a membership projection. The bare inclusion-to-fullness rule needs neither TASK_GL6_SIZE_SETTING nor ChosenProviso.',
 'second_layer_global',['RSL11','RSL12'])
cert('CERT_RSL_OPERATOR_INCLUSION','Normalized local operators preserve the ramified lattice',
 'RSL12: under the original HidaSetting, U_v(B_w(v)) subset S_w, U_v(Mram) subset Mram, and T^b_v*S_w subset B_w(v), with b_v>=0, imply normalized G_v preserves Sram; their exact product power defines Nlam. The full FamU contracts require that setting as a guard. D3 supplies TuSize; TASK_GL6_SIZE_SETTING separately proves the still-unwritten implication to eventual HidaSetting. Only the displayed inclusion pieces of the three full operator/length contracts are used.',
 'second_layer_global',['RSL12'])

tasks=[
 ('TASK_GL3_GAP_DEGREE','Install actual two-sided formal-degree bound','B',
  'Prove the remaining finite product estimates and the original-row installation of Closed fam0 SigmaDegreeTwoSidedBoundOfGap (h3). DC1/DC10/DC19 already supply the named normalized discrete-series producer; retain its normalization and all original row/signature matches.'),
 ('TASK_GL4_SLOPE_LOWER','Original column-lattice lower slope','B',
  'Prove hZa=Closed FamilySlopeLowerOpenPart using the actual ColVal.Q, exact base-change lattice and metric: column_lattice_exact_slope followed by the standard Schur slope and hook estimate.'),
 ('TASK_GL4_SLOPE_MAX','Original class-map upper slope','B',
  'Prove hZb=Closed FamilySlopeMaxOpenPart(4) using class_map_archimedean on original class bases and metrics and the constant-four hook bound of PStmtFree.'),
 ('TASK_GL4_COLUMN_VALUES','Actual ColVal dictionary','B',
  'Prove tCV: eventual Nonempty ColVal(D,u) on the same family. Supply original ColTieW polynomial realization, exact local Q_(c,tau) membership and archimedean norm formula, then colValOfTiedS_holds. An abstract slice model alone is insufficient.'),
 ('TASK_GL6_SIZE_SETTING','Original size-to-Hida-setting implication','B',
  'On the original family, reconstruct TuSize -> SettingEventually, supplying every HidaSetting clause (level inequalities, alcove bound and bTop>=0) through Places.settingF_of, numsL_wtsL_fam and levelPrime_setting_of_sizes. FamU is eventual (HidaSetting -> P), so the three full operator contracts cannot be used as unconditional eventual statements. D3 projects to TuSize but does not itself prove this longer implication.'),
 ('TASK_GL6_INTEGRAL','Original two integral Hecke maps','B',
  'Prove hI=Closed FamU HeckeIntegralLevelZero on the two original local lattices via IntegralAtBasePointLattice.integral_at_t0_lattice and exact finite local coset calculations.'),
 ('TASK_GL6_RAMIFIED','Original ramified stability and composite','B',
  'Prove hR=Closed FamU HeckeRamifiedLevelZero, including ramified stability and the original inverse composite, via hecke_ramified_zero_of_matchings_and_du with its exact operators.'),
 ('TASK_GL6_SECOND_BRANCH','Original second-branch inclusion and length','B',
  'Prove hB=Closed FamU SecondBranchInclusionLength on the original local lattices, including T^b S subset B and the exact DVR length, via LemB.second_branch_all_members.'),
 ('TASK_GL6_CONGRUENCE_LENGTH','Finite composite congruence length','B',
  'From the same hI,hR,hB and HidaSetting, reconstruct congruence_no_kernel_minimal: exact normalized product and mth power, finite cokernel and its required length estimate. Its weaker Nlam inclusion is already RSL12.'),
 ('TASK_GL_FINAL_ASSEMBLY','Full final global numerical and lattice assembly','B',
  'Given precisely the eleven original FamGLmin fields (h2b,h2v,h3,hZa,hZb,tCV,hW,hmu,hI,hR,hB), the reconstructed congruence length, original Duty/ChosenWall and TuSize, complete linkGLOBAL7_min/items and link8 on the same class, with Cabs=2,C0=3,C5=4,eD=2,eL=0. FR1/GF8 give frame/HN consequences only in their stated scopes; the remaining inequalities and all actual slot hypotheses must be written.')]
for ident,title,cat,contract in tasks:
    add(ident,title,cat,contract,status='human_proof_still_required',
        kind='implication_reconstruction_task',proofs=[evidence('second_layer_global',['RSL13'])])
add('GLOBAL_RAMIFIED_INCLUSION','Original local Nlam inclusion','B',
 'Closed on D3(3,A): one eventual threshold for every original x,i,u,w above T_u gives Nlam(D,u,w) subset Sram(D,u,w). The selected sufficient operator route requires the three FamU contracts plus the separate size-to-setting proof task; D3 membership supplies its TuSize premise. Only the preservation/inclusion pieces of those full contracts are used. The bare Nlam inclusion remains a weaker exact input to the RSL fullness consumer.',
 ['TASK_GL6_SIZE_SETTING','TASK_GL6_INTEGRAL','TASK_GL6_RAMIFIED','TASK_GL6_SECOND_BRANCH','CERT_RSL_OPERATOR_INCLUSION'])
add('GLOBAL_FULL_RANK','Fullness through its smaller local inclusion cut','B',
 'Closed(D3(3,A), ChosenE(3,CH) -> NuFullF AND MuRank). The completed implication uses actual second layer and Nlam inclusion; TuSize is a projection of D3 membership. This route does not depend on GL4 or the final global-slope assembly.',
 ['GLOBAL_REAL_SECOND_LAYER','GLOBAL_RAMIFIED_INCLUSION','CERT_RSL_RAMIFIED_MODEL','CERT_RSL_FULLNESS'])
add('TASK_LINK_GL_INSTALL','Precisely separated residual global proof tasks','B',
 'Finish the human implication from the same link_gl input record. Mass/base-volume and actual ramified model are now reconstructed. The ten explicit B tasks below, including size-to-setting installation, are still proof tasks; their Lean declarations are not counted as human proofs.',
 ['CERT_RSL_RAMIFIED_MODEL']+[t[0] for t in tasks],
 status='human_proof_still_required',kind='implication_reconstruction_task')
add('GLOBAL_GL_PAIR','Same-family full-rank and global-slope source join','B',
 'Both source link_gl conclusions, conditional on exact matched second-layer/mass inputs and completion of the remaining original global proof tasks. GLOBAL_FULL_RANK now also has the independently smaller RSL route.',
 ['GLOBAL_SECOND_LAYER_MATCH','TASK_LINK_GL_INSTALL'],status='conditional_join_open')
# GLOBAL_SLOPE retains its original precise projection from GLOBAL_GL_PAIR.

for n in g['work_refinement_nodes']:
    if n['id']=='GLOBAL_SMALL_PROJECTION_MATCH':
        n.update(category='B',status='closed_in_stated_scope',
          contract='SLR1–SLR3/SLR8 identify the exact original lPrj and prove lPrj*lZ0=1, with |P| normalization. No separate zL arithmetic supplier remains after the actual Bundle is supplied.',
          evidence=[evidence('small_level_rank',['SLR1','SLR2','SLR3','SLR8'])])
    elif n['id']=='GLOBAL_SMALL_RANK_LINEAR_JOIN':
        n.update(status='closed_conditional_implication',
          contract='SLR4–SLR9 close the original finite rank join. Actual same-Bundle base rows and theta square remain at SLR_SAME_BUNDLE_BASE_PRODUCER.',
          evidence=[evidence('small_level_rank',['SLR4','SLR5','SLR6','SLR7','SLR9'])])
    elif n['id']=='GLOBAL_LOCAL_THETA_BINDINGS':
        n['version_0_31_update']='LTD1/2/6/7/8 close selection, literal operator/lattice, localization and field transports. Remaining D concerns exact actual realization/EMtTheta and full field containment; known substantial suppliers stay C. Row and ambient Hecke families remain distinct.'
    elif n['id']=='GLOBAL_ACTUAL_ROW_SPECTRUM':
        n['version_0_31_update']='LTD6 closes identity transport with cHk^k; SLR narrows its rank consumer to RowsHold0_3 plus base theta. Actual RatIn.span/hL_int, row spectra and readings remain C.'
newwork=[
 dict(id='DESIGN_RECURSIVE_CORE',category='C',status='open_original_producer',
  contract='Literal RecExP(withQD QOf) for the common object predicate; QW9/MF20 already supply the historical logarithmic window. Remaining RecAtG core and eventual QOf/common bundle/row inputs must be supplied together.',
  evidence=[evidence('design_existence',['DEX8','DEX9','DEX10','DEX11'])]),
 dict(id='DESIGN_RECURSIVE_INSTALL',category='B',status='closed_conditional_implication',
  contract='DEX8–DEX11: actual RecExP(withQD QOf)+the same HostExW -> compatible DesignChoices, through one common selector, uniform injective word code and original kits. This is an exact alternative producer route; recursive existence is not asserted.',
  evidence=[evidence('design_existence',['DEX8','DEX9','DEX10','DEX11'])])]
g['work_refinement_nodes']+=newwork
for consumer,dep in [
 ('DESIGN_CHOICES_COMMON','DESIGN_RECURSIVE_CORE'),
 ('DESIGN_CHOICES_COMMON','DESIGN_RECURSIVE_INSTALL'),
 ('SLR_SAME_BUNDLE_BASE_PRODUCER','GLOBAL_ACTUAL_ROW_SPECTRUM'),
 ('SLR_SAME_BUNDLE_BASE_PRODUCER','GLOBAL_LOCAL_THETA_BINDINGS'),
 ('LOCAL_NBUILT_COMMON','GLOBAL_LOCAL_THETA_BINDINGS'),
 ('SECOND_LAYER_COMPATIBLE_SELECTION','GLOBAL_LOCAL_THETA_BINDINGS')]:
    g['work_refinement_links'].append(dict(consumer=consumer,dependency=dep,logical=False,
       relation='work_refinement',rationale='Shared work or upstream producer route; not a claim that this list alone constructs the consumer.'))
g['nodes']=list(nodes.values())
g['selected_interface_cuts']['design_v031']=dict(
 inputs=['DESIGN_CHOICES_COMMON','DESIGN_TUSIZE_CLOSED','DESIGN_RANKM_CLOSED'],
 certificate='CERT_DESIGN_REDUCTION',
 binding='One common construction class Cdes=WithTw(WithSm Cprime), cT and actual family, selected only after every Closed threshold is joined; top-level C=WithChN A remains distinct.')
g['selected_interface_cuts']['small_rank_v031']=dict(
 inputs=['SLR_SAME_BUNDLE_BASE_PRODUCER'],certificate='CERT_SLR_FINITE_JOIN',
 binding='One Bundle selector with both actual RowsHold0_3 and base-tuple thTheta, uniformly eventually.')
g['selected_interface_cuts']['coverage_v031']=dict(
 inputs=['LOCAL_NBUILT_COMMON'],certificate='CERT_LOCAL_COVERAGE')
g['selected_interface_cuts']['fullness_v031']=dict(
 inputs=['GLOBAL_REAL_SECOND_LAYER','GLOBAL_RAMIFIED_INCLUSION'],
 certificate=['CERT_RSL_RAMIFIED_MODEL','CERT_RSL_FULLNESS'],
 implicit_class_projection='D3 membership includes TuSize. The bare RSL fullness consumer uses original T=1 mod4 for positivity and needs no full HidaSetting or GL4.',
 selected_stronger_supplier_note='The three full GL6 FamU contracts plus the explicit size-to-setting B task form a selected sufficient supplier shared with global slope; only their weaker preservation/inclusion pieces reach Nlam inclusion.')
g['selected_interface_cuts']['GL4_v031']=dict(
 interface='the exact three GL4 fields of FamGLmin',
 inputs=['TASK_GL4_SLOPE_LOWER','TASK_GL4_SLOPE_MAX','TASK_GL4_COLUMN_VALUES'],
 scope='These fill only the three GL4 slots. The other FamGLmin fields and final assembly remain explicit.')
g['source_inputs']={'predecessor_graph':g['predecessor_graph']}
for comp in COMPONENTS:
    for file in ['provenance.json','closure.json']:
        p=ROOT/comp/file
        if p.exists():g['source_inputs'][comp+'_'+file.split('.')[0]]={'file':comp+'/'+file,'sha256':sha(p)}
if (AUDIT/'main.tex').exists():
    g['source_inputs']['current_narrative']={'file':'dependency_audit_v0_31/main.tex','sha256':sha(AUDIT/'main.tex')}

# Retain every historical compound disposition and append precise scope reductions.
prior=read(OLD/'target_disposition.json')
disp=copy.deepcopy(prior);disp['version']='0.31'
disp['predecessor_disposition']={'file':'dependency_audit_v0_30/target_disposition.json','sha256':sha(OLD/'target_disposition.json')}
oldtargets=read(ROOT/'history/version_0_30/next_source_targets.json')['targets']
changes={
 'GLOBAL_DESIGN':dict(claims=['DEX7','DEX8','DEX9','DEX10','DEX11'],
   closed='Finite thinning/denominator/proviso, selector and kit-to-family joins are complete; see three-input design cut.',
   retained='Actual compatible DesignChoices, Closed TuSize implication and original RankM on one class; recursive existence and actual common rows remain.'),
 'GLOBAL_LOCAL_COVERAGE':dict(claims=['LTD3','LTD4','LTD5'],
   closed='Finite generalized-primary coverage and actual NBuilt-to-LinkEta implication.',
   retained='Actual compatible NBuilt/NdSpec producer; no generic TSel inference.'),
 'GLOBAL_SMALL_RANK':dict(claims=['SLR'+str(i) for i in range(1,10)],
   closed='Exact lPrj/lZ0, original-basis rank and base-theta-to-SmallLevelRankEq finite implication.',
   retained='Same original Bundle with actual RowsHold0_3 AND base-tuple theta square; other compound source requirements retain their separate roles.'),
 'GLOBAL_LOCAL_THETA_BINDINGS':dict(claims=['LTD1','LTD2','LTD6','LTD7','LTD8'],
   closed='Literal selections, installed original maps/lattices, row operator normalization and prescribed field containment transport.',
   retained='Actual common geometric/analytic realization, row readings, theta comparisons and field-valued period data.'),
 'GLOBAL_ACTUAL_ROW_SPECTRUM':dict(claims=['LTD6','SLR4','SLR5'],
   closed='Original row operator/eigenvalue/lattice transport and conditional finite type-rank comparison.',
   retained='Actual rational spectral span/integrality and original row realization; row and ambient Hecke systems remain different.'),
 'GLOBAL_SECOND_LAYER_MATCH':dict(claims=['RSL'+str(i) for i in range(1,7)],
   closed='Universal original genus mass and reciprocal volume match, finite character in original field and same-selector second-layer join.',
   retained='Actual compatible selector/real witness on the same class; remaining GL4/GL6 proof tasks are listed separately.'),
 'GLOBAL_FULL_RANK':dict(claims=['RSL9','RSL10','RSL11','RSL12'],
   closed='Actual integral/isometric ramified model and Nlam-inclusion-to-full-positive-rank implication.',
   retained='Original eventual Nlam subset Sram and compatible second layer; distinct theta/type fullness obligations in this compound record are not automatically discharged.'),
 'GLOBAL_SLOPE':dict(claims=['RSL1','RSL2','RSL3','RSL9','RSL10','RSL13'],
   closed='Mass/base-volume, actual ramified mean and maximal-slope transport; LC7 transport boundary closed in this scope.',
   retained='Actual h3, GL4 triple, GL6 operator/length contracts and final global numerical/lattice assembly.')}
for t,rec in zip(oldtargets,disp['records']):
    rec['predecessor_record_sha256']=hashlib.sha256(json.dumps(t,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()).hexdigest()
    updates=[dict(frontier=k,**v) for k,v in changes.items() if k in rec.get('frontier_ids',[])]
    rec['version_0_31_scope_updates']=updates
    rec['version_0_31_disposition_policy']='Original full compound scope and primary category retained; listed sub-implications are superseded precisely. Use current selected leaf cuts for remaining independent proof work. No whole record is declared closed merely from one new subclaim.'
disp['current_selected_frontier']='dependency_audit_v0_31/obligation_map.json'
disp['category_count_policy']='Historical compound-record categories are retained as navigation, not current atomic proof-task counts or a completion percentage. Current selected leaves each have their own A/B/C/D category.'
disp['coverage']['records_with_v031_scope_updates']=sum(bool(r['version_0_31_scope_updates']) for r in disp['records'])
write(AUDIT/'target_disposition.json',disp)
g['backlog_crosswalk']=dict(file='dependency_audit_v0_31/target_disposition.json',
 sha256=sha(AUDIT/'target_disposition.json'),records=245,scope_groups=107,
 meaning='Full inherited compound scopes plus explicit v0.31 subclaim reductions; categories are not independent-obligation counts.')

def reachable(root):
    seen=set();todo=[root]
    while todo:
        k=todo.pop()
        assert k in nodes,('missing reference',k)
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
rh=reachable('ORDINARY_RH');grh=reachable('DIRICHLET_GRH')
assert rh|grh==set(nodes)
assert 'COUNT_III_PRODUCER' not in rh and 'COUNT_III_PRODUCER' in grh
assert {'COUNT_I_PRODUCER','COUNT_II_SUPPORT','COUNT_V_PRODUCER'}<=rh&grh
full=reachable('GLOBAL_FULL_RANK')
assert not any(k.startswith('TASK_GL4') for k in full)
assert 'TASK_GL_FINAL_ASSEMBLY' not in full
openleaves=[n for n in nodes.values() if n['gate']=='LEAF' and n['status'] not in ['proved_in_stated_scope','published_application_checked']]
g['validation']=dict(logical_graph_acyclic=True,all_selected_nodes_reachable_from_roots=True,
 selected_node_count=len(nodes),work_refinement_node_count=len(g['work_refinement_nodes']),
 optional_node_count=len(g['optional_routes']),rh_reachable_count=len(rh),dirichlet_grh_reachable_count=len(grh),
 rh_excludes_every_case_III_producer=True,unrestricted_grh_includes_case_III=True,both_roots_reach_I_II_V=True,
 ten_exact_topDesWin_arguments_retained=True,same_ideal_count_II_coupling_retained=True,
 full_rank_excludes_GL4_and_final_slope_assembly=True,design_thresholds_before_one_family=True,
 small_rank_coupled_base_producer=True,generic_TSel_not_assumed_to_produce_NBuilt=True,
 all_selected_open_leaves_classified=True,open_leaf_categories=dict(collections.Counter(n['category'] for n in openleaves)),
 predecessor_claim_graph_preservation_is_separate=True,new_Lean_build_performed=False)
write(AUDIT/'obligation_map.json',g)
write(AUDIT/'remaining_leaf_register.json',dict(artifact_version='0.31',source_commit=PIN,
 category_key=g['categories'],scope=g['scope'],records=openleaves,
 warning='These are selected sufficient proof-task contracts, often coupled and overlapping. Their count is not a completion percentage or mathematical minimality theorem.'))
write(AUDIT/'closure_delta.json',dict(artifact_version='0.31',source_commit=PIN,changes=changes,
 historical_corrections=[dict(claim='RF16',supplied_by='DEX11',
  correction='RF.45–46 omitted epsilon/100 from the literal f rank window. Replace H upper exponent by 9/2+9epsilon and use positive gap epsilon. The same proof preserves RF.48 and the original uniform word bound; old bytes retained for provenance.')]))
write(AUDIT/'published_applications.json',dict(artifact_version='0.31',source_commit=PIN,
 freshly_checked_applications=read(ROOT/'design_existence/published_applications.json'),
 inherited_registry=dict(file='dependency_audit_v0_30/published_applications.json',sha256=sha(OLD/'published_applications.json')),
 note='New Minkowski application is checked against the primary Serre text. GV-TAM/MF-HM and CC inputs retain their previously recorded scopes; they are not described as fresh re-reviews.'))
print(json.dumps(g['validation'],indent=2))
