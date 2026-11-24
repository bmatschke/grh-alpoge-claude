#!/usr/bin/env python3
"""Refine producer boundaries without changing any selected logical edge."""
from pathlib import Path
import collections,copy,hashlib,json
ROOT=Path(__file__).resolve().parent
AUD=ROOT/"dependency_audit_v0_40";OLD=ROOT/"dependency_audit_v0_39"
read=lambda p:json.loads(p.read_text())
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
def write(p,d):p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+"\n")
cfg=read(ROOT/"increment_v0_40.json")
g=copy.deepcopy(read(OLD/"obligation_map.json"))
g["artifact_version"]="0.40"
g["predecessor_graph"]={"file":"dependency_audit_v0_39/obligation_map.json","sha256":sha(OLD/"obligation_map.json")}
nodes={n["id"]:n for n in g["nodes"]}
def evidence(c):
 return dict(component=c,claims=cfg["component_claims"][c],ledger=c+"/provenance.json",
  ledger_sha256=sha(ROOT/c/"provenance.json"),proof_file=c+"/main.tex",proof_sha256=sha(ROOT/c/"main.tex"))
def refine(k,contract,components):
 n=nodes[k];n["previous_interface"]=copy.deepcopy(n)
 n.update(contract=contract,introduced_or_refined_in="0.40")
 n.setdefault("evidence",[]).extend(evidence(c) for c in components)
cnt=["patched_ring","patched_support","coefficient_normalization","selected_core"]
com=["comparison_packet"]
cntc=sum((cfg["component_claims"][c] for c in cnt),[])
comc=cfg["component_claims"]["comparison_packet"]
refine("COUNT_II_SUPPORT",
 "For each of the TWO original QX rank-four Links, at fixed iota choose ONE common coefficient threshold before every later coefficient DVR and actual universal B,Lambda; produce one ideal J carrying ring,dense,pt,end1,end2,twist AND P1core. Inherited JSP/CIP/CAP/CCH/CFO supply the same-J consumer, every-map reciprocity/universal NiceI Norm, ArPl under unchanged CohP, supplied-type IsRes, and the full selected h=0,a=n=4,g=0 Choice with coupled B1/B2, D=4[L+:Q]+4T.q and B2 constant zero. The dualN bound retains one C before every m and an eventual N threshold uniform over each original admissible rep-prime under its finiteness premise, on actual TWPl. LIM constructs the full original S4. PRG now constructs the full original RRObj/RMaps, every finite-level map and actual ordered splitting target; PMS constructs the actual all-level PMod and full S5 with exact support, dimension, fiber and move fields, plus piKer/piSurj and the same-J annihilator equivalence. SCI constructs the actual quotient determinant, OoPair/ooMaps and point/OoPt on one splitting prime. The selected CRW full-block cotangent bound forces the support ideal to vanish, proving selected normalized Core. BCN supplies full Core=>CoreBC and its selected normalization/Unit consumer; PQL supplies full original TWQuot and matched pro-ell descent. Together SCI13 proves selected original Raw at h=0,a=n=4,k.g=0, with final B,J,K,f and every Selmer quantifier unchanged. Current C producers are earlier: original ordinary/control/separating arithmetic fibers and type/neatU/TThetaEx; four Hida endpoints on this same J; all-level same-J TWAut/HasAut on both Links. The selected Raw patching, normalization and descent are no longer open producers. Preserve full CohP, LocCFT, N4, exact determinant/pro-ell conditions, nontrivial residual cyclotomic character, ell=3, fixed iota and one common coefficient threshold. No arbitrary-Kap B1/B2 theorem, Sel1=0 assertion, arbitrary-chain Core or complete same-J arithmetic support producer is claimed.",cnt)
refine("DESIGN_CHOICES_COMMON",
 "For the one target HostExW, construct the original compatible DesignChoices on Cdes=WithTw(WithSm Cprime), where Cprime=WithChN(A intersect target class), A is the one Built construction class, and cT(eps,y)=cTmin(y). Retain every original field, tuple, word, metric and common bundle duty. DSZ10 and RMP11 give size/rank properties of class members, not member existence. The original RecExP/RecAtG and common object/row route remains coupled. Construct ONE original common design family R and its recursive/geometric half with original Inputs/Pins/Holds/ExAt/InGeo and required CoreP. PKT now reconstructs full exists_pkT, rowPk_nonempty and exists_moved with Copy/Coh on those original given inputs and a supplied fitting later stage: one catalogue, both ChT, complete LfT, actual integral lattices and all metric/measure/period constants are retained; one numerical record precedes every eta and V/S/N/G. RDR supplies one Side0 before all readers, ReadPk/pins and full ReadL with exact o.eta=q.eta. The initial actual geometry, Fits/division/central conditions, primitive rational tests and eta agreement must still be produced. Inherited CSR supplies finite columns, one ReadC before later twists, period/evaluation and scalar/error transports, RowSideDetermined and same-R Bundle/BTw/BWit/BunU consumers. RPI supplies exact RowPairInt for actual pairs and finite translates with original mu_b/fd0; first literal DivDef3 at the same updated R,F,Y,Z,C,sEE follows from its retained original readings, Pins/Holds, stored nonzero IsItW chain, five real-group predicates and group tie. Remaining common fields include host/frame, MultEq nonzero-part support, that original nonzero chain/group tie, eigensystem/carrier/parts and all-embedding logLam, HD/d3b, NEb, actual rational tests and base rows. Retain every simultaneous family hypothesis and eventual threshold. Stronger second DivRows3 remains separate; universal quotient-height CuspRapidDecay and actual common member existence are not inferred from the comparison constructors.",com)
refine("BASE_THETA_READINGS",
 "For every family in the original class, eventually on the SAME selected Bundle and for each i<m, supply the actual R,F,Read,ReadL, weak models/Weil data and phase-one pins. Identify their LiftTie.theta, mtRead, mjRead and ThDef3 basis with that Bundle.P.A3, P.Zs, P.S0 and its stored maps. Exact field, embeddings, metrics, measures, row family and weak choices are retained. This remains one part of the coupled BTH12 producer. PKT now supplies the complete original comparison packet, RowPk and fitting-stage Moved with Copy/Coh on original given geometry, Inputs/Pins/Holds/ExAt/InGeo and Fits. Its ChT/LfT/Reps, actual lattice carriers, original Haar and norm constants, period maps, representatives and all-place RrT are constructed together; its one numerical record precedes every eta/V/S/N/G. RDR gives the original level-zero side, moved-Read and ReadPk/pin constructors on those objects, with one Side0 before every reader and all twelve Read ties. Full ReadL retains the exact o.eta(j,v)=q.eta(j,v) guard for every 1<=j<=m and place v; arbitrary Over does not imply it. Inherited CSR fixes one ReadC before all TwArgs, transports both metrics and all thirteen reading maps, and gives actual period/evaluation with kappa=(c*nP)^(-1/2). RPI supplies exact row-pair integrability, so first updated DivDef3 follows from the retained original Pins/Holds, nonzero chain, five real-group predicates and group tie. Initial theta extension remains complete. Remaining work is actual initial common geometry and its original predicates, Fits/primitive rational tests, eta agreement and outer family/eventual/same-Bundle duties, reFace compatibility, MultEq support, original chain/group data, actual base rows and any stronger DivRows3 theta square. No new compatible reading, family threshold or Haar normalization is substituted.",com)
refine("CERT_BASE_THETA_REDUCTION",nodes["CERT_BASE_THETA_REDUCTION"]["contract"]+
 " Version 0.40 supplies full original comparison/RowPk/Moved constructors on given original geometry and Fits, with all maps and metrics fixed. Actual initial geometry, rational tests/Fits, eta agreement and base rows remain.",com)
refine("SECOND_LAYER_COMPATIBLE_SELECTION",nodes["SECOND_LAYER_COMPATIBLE_SELECTION"]["contract"]+
 " Version 0.40 also supplies original comparison/RowPk/fitting-stage Moved algorithms and exact common data transport. The actual initial geometric member, fitting tests, eta agreement and compatible second-layer selector with original eventual thresholds remain upstream.",com)
g["nodes"]=list(nodes.values())
def closure(c):return {"file":c+"/closure.json","sha256":sha(ROOT/c/"closure.json")}
new_count=["ORIGINAL_RROBJ","ORIGINAL_RMAPS","ACTUAL_PATCHED_MODULE","ORIGINAL_S5_SUPPORT_COMPLETION",
 "ACTUAL_QUOTIENT_PAIR_POINT","CORE_TO_COREBC_COEFFICIENT_NORMALIZATION_UNIT","SELECTED_NORMALIZED_CORE","SELECTED_RAW"]
new_common=["ORIGINAL_EXISTS_PKT","ORIGINAL_ROWPK_NONEMPTY","ORIGINAL_EXISTS_MOVED_COPY_COH"]
g["selected_interface_cuts"]["count_ii_v040"]={
 "completed":"Full original rrEx/rmapsEx, actual patched module and full S5, piKer/piSurj and exact same-J annihilator comparison; actual quotient pair and point; full coefficient normalization and selected Core/Raw.",
 "nested_closed_claims":cntc,"remaining":["COUNT_II_SUPPORT"],"newly_closed_nested":new_count,
 "remaining_nested":["JSP_ORIGINAL_ORDINARY_DATA","JSP_FOUR_HIDA_ENDPOINTS","JSP_SAME_IDEAL_HASAUT"],
 "binding":"Same original B,J,K,f,Kap,T,TWPl and all-level supplied TWAut; selected h=0,a=n=4,g=0, ell=3, fixed iota and one common coefficient threshold. One B1 C before every m and original eventual N sets. Both rank-four Links remain required.",
 "scope":"Selected original Raw is complete under its original TWAut and arithmetic antecedents. Generic S5 and full Core=>CoreBC are also proved. Arbitrary-chain Core, universal Kap bounds and original arithmetic TWAut/HasAut existence are not asserted.",
 "support_argument":"One splitting prime P carries both endpoint lifts and the exact point/completion. CRW18 plus PMS dimension forces the support ideal to vanish; same-J fiber equivalence gives J containment.",
 "component_closures":[closure(c) for c in cnt]}
g["selected_interface_cuts"]["common_realization_v040"]={
 "completed":"Full original exists_pkT, rowPk_nonempty and exists_moved with Copy/Coh, on original given geometric/analytic inputs and fitting later stages.",
 "nested_closed_claims":comc,"newly_closed_nested":new_common,
 "remaining_packets":["actual_initial_common_geometry_Inputs_Pins_Holds_ExAt_InGeo",
  "actual_Fits_division_central_and_primitive_rational_tests","original_eta_agreement_for_ReadL",
  "host_frames","MultEq_support","original_nonzero_chain_and_group_tie",
  "eigensystems_parts_all_embedding_logLam","HD_d3b","NEb","rational_tests_and_base_rows"],
 "binding":"Same R,F, finite group, coefficient embedding, lattice carriers, metrics, measures, periods and maps. One finite type catalogue for both ChT, full LfT, all-place RrT, and one Nums before every eta/V/S/N/G. Original conditional theta and exact ReadL eta guard retained.",
 "outside_scope":"Actual common member existence, primitive rational/Fits tests and eta agreement, stronger second DivRows3 and universal quotient-height CuspRapidDecay are not supplied.",
 "component_closures":[closure(c) for c in com]}
g["selected_interface_cuts"]["theta_v040"]={
 "previous_complete_leaf":"BASE_THETA_CUSPIDAL_EXTENSION remains complete.",
 "new_progress":"Original comparison, RowPk and fitting-stage copy producers are reconstructed; earlier RDR and RPI supply readers and exact first-division integrability.",
 "remaining":["BASE_THETA_READINGS","BASE_THETA_RATIONAL_TESTS","SLR_BASE_ROWS_PRODUCER"],
 "guard":"Actual initial geometry and original input predicates, Fits/rational tests, eta agreement and outer same-family/eventual/Bundle duties remain."}
g["source_inputs"]={"predecessor_graph":copy.deepcopy(g["predecessor_graph"])}
for c in cfg["components"]:
 for stem in ["provenance","closure","published_applications"]:
  p=ROOT/c/(stem+".json")
  if p.is_file():g["source_inputs"][c+"_"+stem]={"file":p.relative_to(ROOT).as_posix(),"sha256":sha(p)}
if (AUD/"main.tex").exists():
 g["source_inputs"]["current_narrative"]={"file":"dependency_audit_v0_40/main.tex","sha256":sha(AUD/"main.tex")}
changes={
 "GLOBAL_SMALL_RANK":{"claims":comc,"closed":"Full given-data PkT/RowPk/Moved with exact common maps.","retained":"Actual initial geometry/Fits/rational tests, eta agreement, base rows and original chain/group inputs."},
 "GLOBAL_LOCAL_THETA_BINDINGS":{"claims":comc,"closed":"Comparison and fitting-stage copy constructors, preserving all normalizations.","retained":"Actual initial geometry, primitive tests/Fits and eta agreement; stronger second DivRows3 remains."},
 "RANK4_JOINT_ORDINARY_SUPPORT":{"claims":cntc,"closed":"Actual patching/S5, coefficient normalization and selected original Core/Raw.","retained":"Original ordinary/control/type, four Hida endpoints and all-level same-J TWAut/HasAut."},
 "COUNT_II_SUPPORT":{"claims":cntc,"closed":"Entire selected Raw support producer under original antecedents.","retained":"Whole two-Link arithmetic/automorphic same-J support producer."},
 "GLOBAL_DESIGN":{"claims":comc,"closed":"Full original comparison/RowPk/Moved on given data, including one Nums before all later stages.","retained":"Actual common geometry/Fits/tests/eta, original chain/group inputs, parts/NEb and second DivRows3."}}
disp=copy.deepcopy(read(OLD/"target_disposition.json"));disp["version"]="0.40"
disp["predecessor_disposition"]={"file":"dependency_audit_v0_39/target_disposition.json","sha256":sha(OLD/"target_disposition.json")}
prior=read(ROOT/"history/version_0_39/next_source_targets.json")["targets"]
assert len(prior)==len(disp["records"])==245
for t,r in zip(prior,disp["records"]):
 assert t.get("id")==r["original_id"]
 r["predecessor_record_sha256"]=hashlib.sha256(json.dumps(t,ensure_ascii=False,sort_keys=True,separators=(",",":")).encode()).hexdigest()
 r["version_0_40_scope_updates"]=[
  dict(frontier=k,**v) for k,v in changes.items()
  if k in r.get("frontier_ids",[]) or k in r.get("canonical_count_node_ids",[])]
 r["version_0_40_disposition_policy"]="Every inherited compound scope retained. Selected Raw and comparison subproducers close; no new whole selected-leaf closure."
disp["current_selected_frontier"]="dependency_audit_v0_40/obligation_map.json"
disp["coverage"]["records_with_v040_scope_updates"]=sum(bool(r["version_0_40_scope_updates"]) for r in disp["records"])
write(AUD/"target_disposition.json",disp)
g["backlog_crosswalk"]={"file":"dependency_audit_v0_40/target_disposition.json","sha256":sha(AUD/"target_disposition.json"),
 "records":245,"scope_groups":107,"meaning":"All inherited compound targets retained with explicit nested producer closures."}
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
rh=reach("ORDINARY_RH");grh=reach("DIRICHLET_GRH")
assert rh|grh==set(nodes)
assert len(nodes)==121 and len(rh)==101 and len(grh)==110
assert "COUNT_III_PRODUCER" not in rh and "COUNT_III_PRODUCER" in grh
leaves=[n for n in nodes.values() if n["gate"]=="LEAF" and n["status"] not in ["proved_in_stated_scope","published_application_checked"]]
assert len(leaves)==33 and collections.Counter(n["category"] for n in leaves)=={"C":22,"B":9,"D":2}
oldnodes={n["id"]:n for n in read(OLD/"obligation_map.json")["nodes"]}
assert all(n["gate"]==oldnodes[k]["gate"] and n["requires"]==oldnodes[k]["requires"] for k,n in nodes.items())
g["validation"].update(selected_node_count=121,rh_reachable_count=101,dirichlet_grh_reachable_count=110,
 open_leaf_count=33,open_leaf_categories={"C":22,"B":9,"D":2},logical_graph_acyclic=True,
 all_selected_nodes_reachable_from_roots=True,original_RRObj_RMaps_complete=True,
 actual_PMod_and_full_S5_complete=True,full_Core_to_CoreBC_complete=True,
 selected_normalized_Core_complete=True,selected_original_Raw_complete=True,
 selected_Raw_original_TWAut_antecedent_retained=True,
 normalized_Core_limiting_patching_S5_and_coefficient_normalization_Unit_remain=False,
 original_exists_pkT_RowPk_Moved_complete=True,full_ReadL_eta_guard_retained=True,
 actual_common_construction_not_claimed=True,same_ideal_support_producer_not_claimed_complete=True,
 additional_selected_whole_leaves_closed=0,new_Lean_build_performed=False)
write(AUD/"obligation_map.json",g)
write(AUD/"remaining_leaf_register.json",dict(artifact_version="0.40",source_commit=g["source_commit"],
 category_key=g["categories"],scope=g["scope"],records=leaves,
 warning="Selected sufficient coupled obligations, not a completion percentage or absolute minimality theorem."))
write(AUD/"closure_delta.json",dict(artifact_version="0.40",source_commit=g["source_commit"],changes=changes,
 closed_selected_leaves=[],closed_nested_producers=new_count+new_common,prior_open_leaf_count=33,current_open_leaf_count=33,
 retained_historical_correction="RF16 governed by DEX11; historical bytes unchanged."))
apps=[]
for c in cfg["components"]:
 p=ROOT/c/"published_applications.json"
 if not p.exists():continue
 data=read(p);items=data if isinstance(data,list) else data.get("applications",data.get("freshly_checked_applications",[]))
 assert isinstance(items,list)
 apps.extend(dict(component=c,**a) for a in items)
assert len({a["id"] for a in apps})==len(apps)
write(AUD/"published_applications.json",dict(artifact_version="0.40",source_commit=g["source_commit"],
 freshly_checked_applications=apps,
 inherited_registry={"file":"dependency_audit_v0_39/published_applications.json","sha256":sha(OLD/"published_applications.json")},
 note="Exact hypotheses are checked in each certificate. These applications do not produce original arithmetic TWAut/Hida or actual common geometry."))
print(json.dumps({k:g["validation"][k] for k in ["selected_node_count","rh_reachable_count","dirichlet_grh_reachable_count","open_leaf_count","open_leaf_categories","selected_original_Raw_complete"]},indent=2))
