#!/usr/bin/env python3
"""Refine the selected sufficient audit, preserving every original logical edge."""
from pathlib import Path
import collections,copy,hashlib,json
ROOT=Path(__file__).resolve().parent
AUD=ROOT/"dependency_audit_v0_36";OLD=ROOT/"dependency_audit_v0_35"
read=lambda p:json.loads(p.read_text())
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
def write(p,d):p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+"\n")
cfg=read(ROOT/"increment_v0_36.json");g=copy.deepcopy(read(OLD/"obligation_map.json"))
g["artifact_version"]="0.36"
g["predecessor_graph"]={"file":"dependency_audit_v0_35/obligation_map.json","sha256":sha(OLD/"obligation_map.json")}
nodes={n["id"]:n for n in g["nodes"]}
def evidence(c):return {"component":c,"claims":cfg["component_claims"][c],"ledger":c+"/provenance.json",
 "ledger_sha256":sha(ROOT/c/"provenance.json"),"proof_file":c+"/main.tex","proof_sha256":sha(ROOT/c/"main.tex")}
def refine(k,contract,ev):
    n=nodes[k];n["previous_interface"]=copy.deepcopy(n)
    n.update(contract=contract,introduced_or_refined_in="0.36")
    n.setdefault("evidence",[]).extend(ev)
theta=["coefficient_fock_bridge","joint_harmonic_io","regular_quotient"]
evtheta=[evidence(c) for c in theta];evcount=[evidence("count_choice")]
thclaims=sum((cfg["component_claims"][c] for c in theta),[]);cch=cfg["component_claims"]["count_choice"]
refine("BASE_THETA_CUSPIDAL_EXTENSION",
 "On the SAME selected Bundle and SAME reading as BASE_THETA_READINGS, extend the exact lowest-type theta integral for each finite basis vector of HV(i,t0) to the original full Wall_i, with one family threshold before i and basis vectors. Inherited BTH/FIA/CTC/TAE/HCU supply convergence, finite cancellation, genuine cusp, actual-action derivatives and uniform growth of the initial integral, full original LowSm/LowIrr, holomorphic uniqueness and the exact Hilbert coefficient stage. CFB and JIO now construct the complete original simultaneous ioP: same c0L/cV/BV and exact VV range, original integer weights, unit-vector Delta normalization, actual real Weil character and substitution, one io_i before EVERY t, and activation of the stored weak choice. RQC now constructs IsReg from the SAME supplied FinPair on literal nuQ, proves full Hilbert smoothness and every ordered derivative word, the actual closed-orbit cusp-preservation supplier and original Gelfand scalar action. Remaining C subcontracts: initial boundedness of the extremal holomorphic cusp function; actual target FinPair; actual continuous smooth representatives with every pointwise/global-AE derivative identity on the same quotient; the fixed-order Sobolev estimate (one exponent and finite word list before x,F,psi), continuous evaluation and uniform moderate growth, completing the literal IsMultMap and exact restriction on all original lowest tensors. Post-Hilbert scalar action cannot supply earlier boundedness. Preserve the same model, quotient, frames, metrics, finite level, adjoints and common choices. Separate readings, rational tests and actual base rows remain outside this analytic packet.",evtheta)
refine("CERT_BASE_THETA_REDUCTION",nodes["CERT_BASE_THETA_REDUCTION"]["contract"]+
 " Version 0.36 supplies the original simultaneous ioP and stored-choice activation, actual same-FinPair IsReg, all Hilbert derivative words, complete original cusp-closure and Gelfand scalar suppliers. Initial boundedness/target FinPair and actual smooth representatives with Sobolev evaluation/growth remain, so the full pointwise MMap is still a producer.",evtheta)
refine("COUNT_II_SUPPORT",
 "For each of the TWO original QX rank-four Links, at fixed iota choose ONE common coefficient threshold before every later coefficient DVR and actual universal B,Lambda; produce one ideal J carrying ring,dense,pt,end1,end2,twist AND P1core. Inherited JSP/CIP/CAP supply the exact common ideal consumer, every-map reciprocity and required universal NiceI Norm, full ArPl under unchanged CohP and IsRes values for any supplied integral type. CCH now supplies the entire required h=0,a=n=4 Choice, including the actual full cyclotomic-kernel trace detector, twisted polarization, finite-list selection, one common finite local coefficient extension and every NP/N3/N4/full-determinant/point-kernel transport. The SAME constructed Kap has g=0 and satisfies literal B2 with C=0 before every m and every N, for every later actual T. Consume Choice and B2 as ONE coupled witness; the universal arbitrary-Kap obstruction theorem is not claimed. Remaining C producers: original ordinary/control/separating arithmetic fibers and type/neatU/TThetaEx; four further Hida endpoints on the same J; all-level same-J HasAut; the exact first-order B1 with D=4[L+:Q]+4T.q; and h=0 Raw on that same point, Kap, pair/J and TWAut, retaining CohP, N4, LocCFT, nontrivial residual cyclotomic character and all original side conditions. In particular g=0 does not make the Sel1 group in B1 vanish. Both Links, ell=3, fixed iota, threshold order and original rings/ideals remain; no ordinary or automorphic producer follows from coefficient extension.",evcount)
g["nodes"]=list(nodes.values())
g["selected_interface_cuts"]["theta_v036"]={
 "completed":"Complete original simultaneous ioP and stored-choice activation; literal IsReg from FinPair; smooth_map/all Hilbert words; actual cusp-closure and gelfRep_scalar",
 "nested_closed":["HCU_COMMON_IO","HCU_REGULAR_REPRESENTATION_EXISTENCE","SmoothMultilinear.smooth_map","ZClosed.zcusp_of_mem_closure","GelfScalar.gelfRep_scalar"],
 "remaining":["BASE_THETA_READINGS","BASE_THETA_CUSPIDAL_EXTENSION","BASE_THETA_RATIONAL_TESTS","SLR_BASE_ROWS_PRODUCER"],
 "residual":"Initial boundedness and actual target FinPair; actual smooth representatives with all derivative identities; fixed-order Sobolev evaluation and uniform growth; final original IsMultMap assembly.",
 "binding":"Same R, c0L/cV/BV, model at sg0, exists io_i forall t, exact Delta; same nuQ normalization and global AE; one finite level and ordered words. No pre-Hilbert boundedness inferred from later scalar action."}
g["selected_interface_cuts"]["count_ii_v036"]={
 "completed":"Coupled original h=0 full-block Choice and literal B2 for that SAME chosen g=0 Kap",
 "remaining":["COUNT_II_SUPPORT"],
 "nested_closed":["JSP_SINGLE_POINT_CHOICE","JSP_OBSTRUCTION_BOUND_ON_CCH15_CHOSEN_KAP"],
 "coupled_rule":copy.deepcopy(read(ROOT/"count_choice/closure.json")["sufficient_rules"][0]),
 "remaining_nested":["JSP_ORIGINAL_ORDINARY_DATA","JSP_FOUR_HIDA_ENDPOINTS","JSP_SAME_IDEAL_HASAUT","JSP_FIRST_ORDER_BOUND","JSP_SINGLE_POINT_RAW"],
 "binding":"Same xprime and kprime from CCH15 for B2 in CCH16, same original point/J and later T/TWPl. No arbitrary-Kap obstruction closure. Both Links, ell=3, fixed iota and one common threshold remain."}
for n in g["work_refinement_nodes"]:
    if n["id"]=="GLOBAL_LOCAL_THETA_BINDINGS":
        n["version_0_36_update"]="The complete original all-parameter ioP and exact regular/smooth/central/cusp-closure suppliers are reconstructed. Original common R/tie/models/Weil inputs, geometric readings/rational tests, initial boundedness/target FinPair and actual pointwise Sobolev realization remain."
    if n["id"] in ["HIDA_FIELDS","P1_CORE_MATCH","P1_CORE_ARITHMETIC_PRODUCER"]:
        n["version_0_36_update"]="CCH supplies h=0 Choice and B2 together on the same chosen g=0 Kap. Original ordinary/control/type, four Hida endpoints, same-J HasAut, B1, Raw and all exact side conditions remain; g=0 does not kill Sel1."
g["source_inputs"]={"predecessor_graph":g["predecessor_graph"]}
for c in cfg["components"]:
    for f in ["provenance.json","closure.json"]:
        g["source_inputs"][c+"_"+f.split(".")[0]]={"file":c+"/"+f,"sha256":sha(ROOT/c/f)}
if (AUD/"main.tex").exists():
    g["source_inputs"]["current_narrative"]={"file":"dependency_audit_v0_36/main.tex","sha256":sha(AUD/"main.tex")}
changes={
 "GLOBAL_SMALL_RANK":{"claims":thclaims,"closed":"Original simultaneous ioP, same-FinPair IsReg, all Hilbert smooth words, exact cusp-closure and Gelfand-scalar suppliers.",
  "retained":"Actual initial boundedness, target FinPair, smooth representatives and Sobolev evaluation/growth; common readings, rational tests and base rows."},
 "GLOBAL_LOCAL_THETA_BINDINGS":{"claims":thclaims,"closed":"Exact coefficient range/action, weights and normalization; same stored ioP activation before all t; exact quotient and derivative/cusp/central bindings.",
  "retained":"Original compatible R, tie, model and Weil production; remaining geometric and pointwise analytic producers."},
 "RANK4_JOINT_ORDINARY_SUPPORT":{"claims":cch,"closed":"Coupled original h=0 Choice and selected same-Kap B2 with C=0 for all m,N.",
  "retained":"Ordinary/control/type/neatU, four Hida endpoints, same-J HasAut, exact B1, Raw and CohP/side conditions."},
 "COUNT_II_SUPPORT":{"claims":cch,"closed":"JSP_SINGLE_POINT_CHOICE and only the chosen g=0 instance of JSP_OBSTRUCTION_BOUND, consumed together.",
  "retained":"Whole original same-J rank-four producer on both Links; no universal arbitrary-Kap obstruction theorem."}}
disp=copy.deepcopy(read(OLD/"target_disposition.json"));disp["version"]="0.36"
disp["predecessor_disposition"]={"file":"dependency_audit_v0_35/target_disposition.json","sha256":sha(OLD/"target_disposition.json")}
prior=read(ROOT/"history/version_0_35/next_source_targets.json")["targets"]
assert len(prior)==len(disp["records"])==245
for t,r in zip(prior,disp["records"]):
    assert t.get("id")==r["original_id"]
    r["predecessor_record_sha256"]=hashlib.sha256(json.dumps(t,ensure_ascii=False,sort_keys=True,separators=(",",":")).encode()).hexdigest()
    r["version_0_36_scope_updates"]=[dict(frontier=k,**v) for k,v in changes.items() if k in r.get("frontier_ids",[])]
    r["version_0_36_disposition_policy"]="Every inherited compound scope retained; theta and CountII original producers are strictly narrowed with explicit coupled witnesses."
disp["current_selected_frontier"]="dependency_audit_v0_36/obligation_map.json"
disp["category_count_policy"]="Historical compound categories are navigation; current sufficient leaves retain exact coupled contracts and are not completion percentages."
disp["coverage"]["records_with_v036_scope_updates"]=sum(bool(r["version_0_36_scope_updates"]) for r in disp["records"])
write(AUD/"target_disposition.json",disp)
g["backlog_crosswalk"]={"file":"dependency_audit_v0_36/target_disposition.json","sha256":sha(AUD/"target_disposition.json"),
 "records":245,"scope_groups":107,"meaning":"Every predecessor compound scope retained with additive exact producer reductions."}
active=set();done=set()
def visit(k):
    assert k in nodes and k not in active
    if k in done:return
    active.add(k)
    for j in nodes[k]["requires"]:visit(j)
    active.remove(k);done.add(k)
for k in nodes:visit(k)
def reach(k):
    seen=set();todo=[k]
    while todo:
        v=todo.pop()
        if v in seen:continue
        seen.add(v);todo+=nodes[v]["requires"]
    return seen
rh=reach("ORDINARY_RH");grh=reach("DIRICHLET_GRH");full=reach("GLOBAL_FULL_RANK")
assert rh|grh==set(nodes)
assert "COUNT_III_PRODUCER" not in rh and "COUNT_III_PRODUCER" in grh
assert {"COUNT_I_PRODUCER","COUNT_II_SUPPORT","COUNT_V_PRODUCER"}<=rh&grh
assert not any(k.startswith("TASK_GL4") for k in full) and "TASK_GL_FINAL_ASSEMBLY" not in full
leaves=[n for n in nodes.values() if n["gate"]=="LEAF" and n["status"] not in ["proved_in_stated_scope","published_application_checked"]]
assert len(leaves)==34 and collections.Counter(n["category"] for n in leaves)=={"C":23,"B":9,"D":2}
g["validation"].update(selected_node_count=len(nodes),rh_reachable_count=len(rh),dirichlet_grh_reachable_count=len(grh),
 open_leaf_count=34,open_leaf_categories={"C":23,"B":9,"D":2},logical_graph_acyclic=True,
 all_selected_nodes_reachable_from_roots=True,original_simultaneous_ioP_complete=True,
 original_IsReg_complete_from_same_FinPair=True,original_smooth_map_and_all_Hilbert_words_complete=True,
 original_cusp_closure_complete=True,original_gelfRep_scalar_complete=True,
 original_h0_full_block_Choice_complete=True,chosen_same_g0_Kap_B2_complete=True,
 Choice_and_B2_same_witness_coupling_explicit=True,arbitrary_Kap_B2_not_claimed=True,
 base_extension_not_claimed_complete=True,same_ideal_support_producer_not_claimed_complete=True,
 additional_selected_whole_leaves_closed=0,new_Lean_build_performed=False)
write(AUD/"obligation_map.json",g)
write(AUD/"remaining_leaf_register.json",{"artifact_version":"0.36","source_commit":g["source_commit"],
 "category_key":g["categories"],"scope":g["scope"],"records":leaves,
 "warning":"Selected sufficient obligations, often coupled; not a completion percentage or an absolute minimality theorem."})
write(AUD/"closure_delta.json",{"artifact_version":"0.36","source_commit":g["source_commit"],"changes":changes,
 "closed_selected_leaves":[],"nested_coupled_rule":g["selected_interface_cuts"]["count_ii_v036"]["coupled_rule"],
 "retained_historical_correction":"RF16 governed by DEX11; historical bytes unchanged."})
write(AUD/"published_applications.json",{"artifact_version":"0.36","source_commit":g["source_commit"],
 "freshly_checked_applications":[],
 "inherited_registry":{"file":"dependency_audit_v0_35/published_applications.json","sha256":sha(OLD/"published_applications.json")},
 "note":"No new published theorem is imported. All new arguments are reconstructed independently with the listed inherited human proofs. Prior checked applications, including CAP finite-Galois Chebotarev, retain their original exact scopes."})
print(json.dumps(g["validation"],indent=2))

