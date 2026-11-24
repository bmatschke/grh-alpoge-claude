#!/usr/bin/env python3
"""Bind the independent v0.41 selected-route/scope review to current bytes."""
from pathlib import Path
import argparse, collections, hashlib, json, subprocess

PIN="7cbf7a0c32fca1badf05931879a37c3f8a2b03b4"
HERE=Path(__file__).resolve().parent
read=lambda p:json.loads(p.read_text())
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
digest=lambda b:hashlib.sha256(b).hexdigest()
def write(p,q):p.write_text(json.dumps(q,ensure_ascii=False,indent=2)+"\n")
def main():
 ap=argparse.ArgumentParser()
 ap.add_argument("--root",type=Path,default=HERE.parent.parent/"reconstruction_v041")
 ap.add_argument("--source-root",type=Path,default=HERE.parent.parent/"lean_source")
 args=ap.parse_args();R=args.root.resolve();S=args.source_root.resolve();A=R/"dependency_audit_v0_41"
 g=read(A/"obligation_map.json");old=read(R/"dependency_audit_v0_40/obligation_map.json")
 n={x["id"]:x for x in g["nodes"]};on={x["id"]:x for x in old["nodes"]}
 assert set(n)==set(on)
 for k in n:
  for f in ["category","gate","requires","status"]:assert n[k][f]==on[k][f],(k,f)
 for k,v in old["selected_interface_cuts"].items():assert g["selected_interface_cuts"][k]==v,k
 for k in ["optional_routes","roots","work_refinement_links"]:assert g[k]==old[k],k
 active=set();done=set()
 def visit(k):
  assert k in n and k not in active
  if k in done:return
  active.add(k)
  for j in n[k]["requires"]:visit(j)
  active.remove(k);done.add(k)
 for k in n:visit(k)
 def reach(k):
  seen=set();todo=[k]
  while todo:
   k=todo.pop()
   if k not in seen:seen.add(k);todo+=n[k]["requires"]
  return seen
 rh=reach("ORDINARY_RH");grh=reach("DIRICHLET_GRH")
 closed={"proved_in_stated_scope","published_application_checked"}
 leaves={k for k,x in n.items() if x["gate"]=="LEAF" and x["status"] not in closed}
 assert len(n)==121 and sum(len(x["requires"]) for x in n.values())==161
 assert len(rh)==101 and len(grh)==110 and rh|grh==set(n)
 shared=leaves&rh&grh;go=(leaves&grh)-rh;ro=(leaves&rh)-grh
 assert len(leaves)==33 and len(shared)==26 and len(go)==7 and not ro
 cats=lambda ids:dict(collections.Counter(n[k]["category"] for k in ids))
 assert cats(leaves)=={"C":22,"B":9,"D":2}
 assert cats(shared)=={"C":18,"B":6,"D":2} and cats(go)=={"C":4,"B":3}
 reg=read(A/"remaining_leaf_register.json")
 assert {x["id"] for x in reg["records"]}==leaves
 for x in reg["records"]:assert x==n[x["id"]]
 route=read(A/"route_coverage.json")
 assert route["graph_sha256"]==sha(A/"obligation_map.json")
 assert set(route["shared_open_leaf_ids"])==shared
 assert set(route["dirichlet_grh_only_open_leaf_ids"])==go
 assert route["shared_categories"]==cats(shared)
 assert route["ordinary_rh_open_leaf_count"]==26 and route["dirichlet_grh_open_leaf_count"]==33
 source_inputs=[]
 for k,s in g["source_inputs"].items():
  assert sha(R/s["file"])==s["sha256"],(k,s["file"])
  source_inputs.append(dict(name=k,**s))
 prop=read(R/"continuation_notes_v0_41/count_ii_contract_replacements.json")
 assert n["COUNT_II_SUPPORT"]["contract"]==prop["canonical_node"]["replacement_contract"]
 assert g["current_count_subcontracts_v0_41"]==prop["current_subcontracts"]
 w={x["id"]:x for x in g["work_refinement_nodes"]};ow={x["id"]:x for x in old["work_refinement_nodes"]}
 for x in prop["current_work_refinement_replacements"]:
  y=w[x["id"]]
  assert y["contract"]==x["replacement_contract"] and y["status"]==x["status"]
  assert y["category"]==x["category"] and y["previous_interface_v0_40"]==ow[x["id"]]
 d=read(A/"target_disposition.json");od=read(R/"dependency_audit_v0_40/target_disposition.json")
 assert len(d["records"])==len(od["records"])==245
 for x,y in zip(d["records"],od["records"]):
  for f in ["id","original_id","original_index_one_based","audit_scope_group","primary_category","applicability",
            "disposition","frontier_ids","canonical_count_node_ids","path","declaration","line_start","line_end",
            "source_full_file_sha256","source_range_sha256"]:
   assert x.get(f)==y.get(f),(x["id"],f)
 idx={x["id"]:x for x in d["records"]}
 want={x["id"] for x in prop["active_target_replacements"]}
 got={x["id"] for x in d["records"] if "COUNT_II_SUPPORT" in x.get("canonical_count_node_ids",[])}
 assert got==want and len(got)==17
 for p in prop["active_target_replacements"]:
  x=idx[p["id"]]
  assert x["version_0_41_count_contract_reference"]=="COUNT_II_SUPPORT"
  assert x["version_0_41_count_subcontract_references"]==p["append_annotation"]["canonical_subcontracts"]
  assert p["append_annotation"] in x["version_0_41_scope_updates"]
 assert len({x["audit_scope_group"] for x in d["records"]})==107
 assert sum(bool(x["version_0_41_scope_updates"]) for x in d["records"])==200
 assert sha(A/"target_disposition.json")==g["backlog_crosswalk"]["sha256"]
 assert sha(R/"dependency_audit_v0_40/obligation_map.json")==g["predecessor_graph"]["sha256"]
 txt=(R/"RH_dependency_audit_v0_41.txt").read_text()
 tex=(A/"main.tex").read_text()
 def esc(s):
  table={"\\":r"\textbackslash{}","_":r"\_\allowbreak{}","&":r"\&","%":r"\%","$":r"\$","#":r"\#",
    "{":r"\{","}":r"\}","~":r"\textasciitilde{}","^":r"\textasciicircum{}","≤":r"$\le$","≥":r"$\ge$",
    "→":r"$\to$","∩":r"$\cap$","κ":r"$\kappa$","λ":r"$\lambda$","χ":r"$\chi$","Ψ":r"$\Psi$",
    "ε":r"$\varepsilon$","𝒞":r"$\mathcal C$","−":"-","/":r"/\allowbreak{}"}
  return "".join(table.get(c,c) for c in s)
 for k in leaves:
  assert n[k]["contract"] in txt,k
  assert esc(n[k]["contract"]) in tex,k
 assert "Frame.Free stabilizer identity" in txt and "ordinary-module freeness remains the target of OrdFree" in txt
 assert "The all-level HasAut producer remains a separate obligation on that same J" in txt
 assert "Tc(c) iff Uc(c+1)" in (R/"configure_v0_41.py").read_text()
 cfg=read(R/"increment_v0_41.json")
 assert cfg["expected_new_claims"]==87 and cfg["predecessor_claim_count"]==2122
 assert len(read(R/"history/version_0_40/provenance.json")["claims"])==2122
 components=cfg["components"]
 pc=sum(len(read(R/c/"provenance.json")["claims"]) for c in components);assert pc==87
 # Verify all new proof blocks, their hash-bound peer reviews and the source
 # ranges cited in new claims plus selected-graph source evidence.
 sources=[];proofs=[];cb=[];peer=[]
 review_names={"neat_levels":"neat_levels_review.json","ordinary_theta_weight":"ordinary_theta_weight_review.json",
   "rational_theta":"rational_theta_review.json","local_hecke_projection":"local_hecke_projection_review.json"}
 for c in components:
  p=read(R/c/"provenance.json");main=R/c/"main.tex";lines=main.read_bytes().splitlines(keepends=True)
  reviewpath=R/"reviews_v0_41"/review_names[c];rv=read(reviewpath)
  assert (rv.get("status") or rv.get("verdict","")).startswith("PASS")
  assert rv["proof_file_sha256"]==sha(main)
  assert rv["provenance_file_sha256"]==sha(R/c/"provenance.json")
  assert rv["closure_file_sha256"]==sha(R/c/"closure.json")
  assert rv["published_applications_file_sha256"]==sha(R/c/"published_applications.json")
  assert set(rv["claims_reviewed"])=={x["id"] for x in p["claims"]}
  peer.append(dict(component=c,file=str(reviewpath.relative_to(R)),sha256=sha(reviewpath),status="PASS"))
  files=[]
  for fn in ["main.tex","provenance.json","closure.json","published_applications.json"]:
   files.append(dict(file=c+"/"+fn,sha256=sha(R/c/fn)))
  cb.append(dict(component=c,claims=[x["id"] for x in p["claims"]],files=files))
  for x in p["claims"]:
   q=x["proof_location"];a,b=q["line_start"],q["line_end"];h=digest(b"".join(lines[a-1:b]))
   assert h==(q.get("range_sha256") or q["sha256"]),(x["id"],h)
   proofs.append(dict(claim=x["id"],file=c+"/main.tex",line_start=a,line_end=b,range_sha256=h))
   sources+=x.get("sources",[])
 for x in n.values():
  for e in x.get("evidence",[]):
   if e.get("path","").startswith("src/") and "line_start" in e:sources.append(e)
   if e.get("component") in components:
    assert sha(R/e["ledger"])==e["ledger_sha256"]
    assert sha(R/e["proof_file"])==e["proof_sha256"]
 cache={};source_ranges=set();occ=0
 for s in sources:
  path=s.get("path")
  if not path or not path.startswith("src/") or "line_start" not in s:continue
  if path not in cache:
   data=(S/path).read_bytes()
   pinned=subprocess.check_output(["git","show",f"{PIN}:{path}"],cwd=S)
   assert data==pinned,path
   cache[path]=data
  data=cache[path];lines=data.splitlines(keepends=True)
  a,b=s["line_start"],s["line_end"]
  assert 1<=a<=b<=len(lines),(path,a,b)
  expected=s.get("file_sha256") or s.get("sha256")
  if expected:assert digest(data)==expected,(path,"file")
  if s.get("range_sha256"):assert digest(b"".join(lines[a-1:b]))==s["range_sha256"],(path,a,b)
  source_ranges.add((path,a,b));occ+=1
 apps=read(A/"published_applications.json")
 assert apps["freshly_checked_applications"]==[]
 delta=read(A/"closure_delta.json")
 assert delta["closed_selected_leaves"]==[]
 assert delta["prior_open_leaf_count"]==delta["current_open_leaf_count"]==33
 changed=[k for k in n if n[k]["contract"]!=on[k]["contract"]]
 semantic=[
 ("full_neatU","NTL17 matches every original QData, arbitrary integral tau0 and compact-open K. The fixed odd auxiliary prime, section fallback and same-coordinate torsion argument introduce no ell>n or type antecedent."),
 ("one_theta_all_levels","OTW12 produces one character in the entire complete coefficient ring before EVERY K; actual artOf, inverse cyclotomic adjustment and Tc(c)/Uc(c+1) are preserved. Frame.Free is distinguished from the still-unproved ordinary-module freeness."),
 ("conditional_HdEx","OTW13 assembles all eight original UnitaryHeckeData fields on the complete retained TypeForAlt and inherited CAP17. Every Teichmuller lift and allowed IsRecT remains quantified; no unconditional type or Hida producer is inferred."),
 ("canonical_CountII","The canonical COUNT_II_SUPPORT contract and all three active subcontracts equal the source-anchored proposal byte for byte. All 17 applicable target records reference that one contract and carry its exact same-object/threshold annotation."),
 ("same_ideal_and_four_Alt_fields","Both rank-four Links, fixed iota before one coefficient threshold, ell=3, actual B/J/K/f/Kap/T/TWPl, CohP/LocCFT/N4 and full determinant/pro-ell guards remain. The four Alt fields preserve the cofinite strict ratio bound, not a stronger exact-purity theorem. HasAut remains separate on the SAME J."),
 ("selected_support_stays_complete","SCI13 selected h=0,a=n=4,g=0 Raw is retained as complete under its original antecedents. The historical P1 literature-match refinement is bypassed only for that selected route; actual same-J HasAut and the compound Count-II leaf remain open."),
 ("rational_theta_same_record","RTG finite coefficient, representative, square-law, PhiIs and Pins transfers keep the literal base coefficient record. Higher CoversAt, all original and scaleXi class sums/uniqueness, common PointIdentCore lambda,z before O, base ClassSumsSpan and geometric LatFull remain explicit."),
 ("phase_projection_tests","RatG uses cj(twAt embLL A3.A.v0)(R.phs i) and the actual good projector eOp(y). Both Boolean-level LiftTestB consumers preserve the same rational basis and target coordinate tests. The zero-reference branch does not infer a scalar ratio."),
 ("rational_outer_duties","Original common R/F/T, Inputs/Pins/Holds/ExAt/InGeo, base OMPins/OneMapRow0, Fits, eta agreement, base rows and outer family/eventual/Bundle selection remain. First RowPairInt/DivDef3 remain closed in their stated scope; stronger second DivRows3 is separate."),
 ("local_literal_lattice_and_action","HLP keeps ambient indices 1<=k<=nV, literal MtLat-projection MtSub, Psi/range/off-space error, actual maximal ideals and faithful actions. Bj uses the distinct original MjLat generators and universal coefficient-map relation."),
 ("local_original_inputs","Full nonempty_spec is closed on its full original input list. Actual MtInput, complex HeckeStdPlain/no-Jordan, F3 norm/GoodCoef/iq bridges, F4 entire-field common reading, arithmetic characters, AutSpec and remaining NBuilt fields remain. HLP is explicitly distinct from ordinary Hida Frame/glIwa."),
 ("same_family_graph","No sufficient AND gate or logical edge changes. Shared refinements are not promoted to independent sufficient gates. All old historical cuts, optional AQ and root scopes remain; RF16 remains governed by DEX11."),
 ("classification_scope","All 33 whole leaves retain identity, category and status. The two D leaves concern human source understanding, not formal correctness. Counts are bookkeeping, not a completion percentage or globally minimality proof."),
 ]
 files=["dependency_audit_v0_41/obligation_map.json","dependency_audit_v0_41/main.tex",
   "RH_dependency_audit_v0_41.txt","dependency_audit_v0_41/remaining_leaf_register.json",
   "dependency_audit_v0_41/target_disposition.json","dependency_audit_v0_41/closure_delta.json",
   "dependency_audit_v0_41/route_coverage.json","dependency_audit_v0_41/published_applications.json",
   "increment_v0_41.json","configure_v0_41.py","build_audit_v0_41.py","write_readable_audit_v0_41.py",
   "assemble_v0_41.py","continuation_notes_v0_41/count_ii_contract_replacements.json",
   "continuation_notes_v0_41/next_count_ii.txt","continuation_notes_v0_41/next_count_ii_sources.json"]
 result=dict(schema="rh-selected-route-independent-review/1",artifact_version="0.41",date="2026-11-22",
  reviewer="/root/audit_literature",status="PASS",
  verdict="PASS — unchanged whole selected graph, exact ordinary/neatness scopes, same-J canonical Count-II updates, and retained rational/local producer boundaries",
  source_commit=PIN,formal_correctness_assumed=True,new_lean_build=False,
  review_scope="Independent structural and mathematical-scope review of the assembled graph/narrative and four component cuts. Individual proof reviews are separately hash-bound; this does not claim a second full mathematical review of every HLP/RTG proof.",
  graph_sha256=sha(A/"obligation_map.json"),graph_file_sha256=sha(A/"obligation_map.json"),
  narrative_file_sha256=sha(A/"main.tex"),readable_audit_file_sha256=sha(R/"RH_dependency_audit_v0_41.txt"),
  narrative=dict(file="dependency_audit_v0_41/main.tex",sha256=sha(A/"main.tex")),
  standalone_audit=dict(file="RH_dependency_audit_v0_41.txt",sha256=sha(R/"RH_dependency_audit_v0_41.txt")),
  reviewed_files=[dict(file=f,sha256=sha(R/f)) for f in files],
  verified_source_inputs=source_inputs,component_bindings=cb,verified_individual_proof_reviews=peer,
  summary=dict(selected_nodes=121,logical_edges=161,rh_reachable=101,dirichlet_grh_reachable=110,
    union_reachable=121,open_selected_leaves=33,open_categories=cats(leaves),
    shared_open_leaves=26,shared_categories=cats(shared),dirichlet_grh_only_open_leaves=7,
    dirichlet_grh_only_categories=cats(go),rh_only_open_leaves=0,new_whole_selected_leaves_closed=0,
    historical_target_records=245,historical_scope_groups=107,current_scope_update_records=200,
    current_count_ii_disposition_updates=17,source_inputs=len(source_inputs),
    distinct_pinned_source_files=len(cache),distinct_pinned_source_ranges=len(source_ranges),
    verified_source_occurrences=occ,new_proof_blocks=len(proofs),current_independently_reviewed_claims=87,
    predecessor_claim_count=2122,cumulative_claim_count_from_component_ledgers=2209),
  changed_interface_ids=changed,open_leaf_ids=sorted(leaves),shared_open_leaf_ids=sorted(shared),
  dirichlet_grh_only_open_leaf_ids=sorted(go),canonical_count_ii_target_ids=sorted(got),
  semantic_checks=[dict(id=k,status="PASS",detail=v) for k,v in semantic],
  proof_block_bindings=proofs,
  corrections_resolved=[
    dict(id="torus_depth",detail="Replaced ambiguous Tc(c+1) wording by exact Tc(c) iff Uc(c+1)."),
    dict(id="freeness_scope",detail="Explicitly distinguished Frame.Free stabilizer identity from ordinary-module freeness, which remains OrdFree's target."),
    dict(id="HasAut_scope",detail="Separated the four same-J Hida fields from the additional all-level same-J HasAut producer."),
    dict(id="current_P1_refinements",detail="Installed exact current refinements and all 17 target annotations without modifying immutable historical snapshots.")],
  required_corrections_remaining=[],
  limitations=["No fresh Lean verification is claimed.","This review verifies selected graph and semantic scope, not completion of its remaining suppliers.",
   "Cumulative claim total is independently checked from predecessor and new component ledgers; root's release validation separately checks the merged cumulative ledger."])
 out=HERE/"selected_route_graph_review.json";write(out,result)
 txtout=HERE/"selected_route_graph_review.txt"
 report=[
  "INDEPENDENT SELECTED-ROUTE REVIEW — VERSION 0.41","Reviewer: /root/audit_literature",
  "PASS. No required correction remains.","",
  "Source pin: "+PIN,"Graph SHA256: "+result["graph_sha256"],
  "Audit TeX SHA256: "+result["narrative_file_sha256"],
  "Readable audit SHA256: "+result["readable_audit_file_sha256"],"",
  "Structural result: all 121 nodes and 161 logical edges are retained. RH reaches 101 nodes; unrestricted Dirichlet GRH reaches 110. All 33 whole open leaves have exactly their predecessor identities, statuses and categories: 22 C, 9 B, 2 D.",
  "The 26 shared leaves are 18 C + 6 B + 2 D; the 7 additional GRH-only leaves are 4 C + 3 B. There are no RH-only open leaves. Every historical cut and optional route is unchanged.",
  "All 245 target records in 107 groups retain original source identity/category/disposition. There are 200 additive scope-update records. The 17 Count-II targets carry the exact canonical proposal and all three subcontract references; HIDA_FIELDS and both P1_* refinements preserve their prior snapshots.",
  "Four packet sizes: NTL17 + OTW13 + RTG25 + HLP32 = 87. Together with 2,122 predecessor claims this gives 2,209 cumulative claims at component-ledger level. All 87 new proof-block hashes and final independent review bindings were checked.",
  f"Source check: {len(cache)} pinned files, {len(source_ranges)} distinct inclusive ranges, {occ} occurrences from current component claims and selected-graph evidence. All 15 graph source-input bindings match current files.",
  ""]
 for k,v in semantic:report+=["PASS — "+k,v,""]
 report+=["Resolved precision edits: exact Tc(c)/Uc(c+1); Frame.Free versus module freeness; separate same-J HasAut; current P1 refinements and 17 target annotations.",
  "No new proof, selected-leaf closure, source-correctness challenge or Lean replay is asserted. The semantic review retains every original supplier described above. The root release validation separately checks cumulative merge and TeX delivery.",
  "", "Review JSON SHA256: "+sha(out)]
 txtout.write_text("\n".join(report)+"\n")
 print(json.dumps(dict(status="PASS",graph_sha256=result["graph_sha256"],
  narrative_sha256=result["narrative_file_sha256"],audit_sha256=result["readable_audit_file_sha256"],
  review_json_sha256=sha(out),review_txt_sha256=sha(txtout),sources=len(cache),
  ranges=len(source_ranges),source_occurrences=occ),indent=2))
if __name__=="__main__":main()
