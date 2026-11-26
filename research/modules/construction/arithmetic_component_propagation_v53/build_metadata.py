#!/usr/bin/env python3
"""Bind the ACP human proofs to exact pinned contracts; never replay Lean."""
from pathlib import Path
import argparse
import hashlib
import json
import re
import subprocess

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
PIN = "7cbf7a0c32fca1badf05931879a37c3f8a2b03b4"
VERSION = "0.53"
V = "src/Development/AutomorphicArithmetic/AutomorphicVarieties/"
C = V + "CurveDVRSpecialization/"
F = V + "FrobeniusSmoothVectors/"
D = V + "ModularityArgument/ThresholdArguments/DenseThresholdCases/"
L = V + "ModularityArgument/AutomorphyLifting/"

# A missing final line means the complete file.  Files needed only to identify
# the next consumer are retained too, but are not represented as proved inputs.
SPECS = {
 "cd": (C+"IsUnitOrIsUnitOfAddOne.lean",107,110,"Full original IsCD, including finite residue field"),
 "co": (V+"CommutativeAlgebra/ResMapBijective.lean",9,75,"Original IsCO, automatic residue preservation and adic continuity"),
 "clsub": (V+"CommutativeAlgebraHeight/ClSub.lean",1,None,"General residue-constant subring construction; ACP1 proves the exact DVR/scalar-tower specialization directly"),
 "space": (F+"LeAdicClosure.lean",9,221,"NRep, exact ordered products, IsLift, supplied Space, weight-zero algebra, FinLam and core"),
 "frame": (F+"ContinuousCoboundaries2.lean",1,216,"Original frame and all Ok fields, including gen and cl"),
 "flag": (F+"FlagLoc.lean",1,None,"Full original flag_loc"),
 "lagrange": (V+"AlgebraTools/LagTriangular.lean",1,None,"Ordered-product projector calculation underlying flag_loc"),
 "o1": (F+"CharpolyFlag.lean",1,None,"Full original o1 local characteristic-polynomial identity"),
 "torsion": (C+"SelfTwistEigenvalues/OneUnitTF.lean",1,None,"Full original oneUnitTF"),
 "cycle": (C+"FinPtOf.lean",13,28,"charpoly_of_cyc over an arbitrary commutative ring"),
 "char": (C+"FinPtOf.lean",29,108,"Full finite-character rigidity argument char_eq"),
 "diag": (C+"FinPtOf.lean",109,182,"Frame gen/cl diagonal rigidity diag_eq"),
 "finpt": (C+"FinPtOf.lean",183,344,"Full original finPtOf, both triangular branches and all IsCD tests"),
 "pointloc": (F+"PointLoc.lean",1,None,"Broader triangular-residual point_loc; explicitly not imported by ACP2"),
 "pointdefs": (C+"PropagationTheoremGL2.lean",31,84,"Literal P1', P23', SeedIn, AllGood, OffFin, IsLiftA, FinPt and FinPtOf"),
 "nice_defs": (C+"FlipTwoThree.lean",7,14,"Full original NicePrimeEx contract"),
 "local_defs": (C+"FlipTwoThree.lean",15,59,"All ten LocData.Ok fields and full LocProp"),
 "global_defs": (C+"FlipTwoThree.lean",61,87,"All eight GlobData.Ok fields and full GlobProp"),
 "chart_defs": (C+"FlipTwoThree.lean",89,108,"Full Chart, ChartOfFlat and GlobOfCharts contracts"),
 "nice": (C+"NicePrimeEx.lean",1,None,"One-dimensional specialization and full nicePrimeEx"),
 "local": (C+"LocProp.lean",1,None,"Full original locProp"),
 "global": (C+"GlobProp.lean",1,None,"Full original globProp"),
 "chart": (C+"ChartOfFlat.lean",1,None,"Full original chartOfFlat, without Noetherian assumptions"),
 "charts": (C+"GlobOfCharts.lean",1,None,"Full original globOfCharts with all three conclusions"),
 "finend": (C+"FinEndOfFinPt.lean",1,None,"Already reconstructed AFE20: same-frame FinPt to FinEnd transport"),
 "ends": (C+"RatTorsionFree.lean",20,68,"Original OrdPt, FinEnd, AutEnd2/3, HostEnd and GdEnd"),
 "alt": (D+"AutEnd3AltAlt.lean",20,40,"Original Alt endpoints and identical marking/FinEnd fields"),
 "alt3": (L+"IsAutCsdA.lean",1,16,"IsAutCsdA is AutCsd0 and conditional WitA"),
 "aut3": (V+"AutomorphicForms/BlochKatoSelmerVanishes.lean",77,86,"Original IsAutCsd is precisely AutCsd0"),
 "alt2": (L+"AutomorphyDescent/AutEnd2Ao.lean",1,None,"Original Alt rank-two conclusion retains attached newform and WitAQ"),
 "abs": (C+"AbsMain.lean",1,None,"Actual common-frame call: rank two, rank three, then FinPtOf"),
 "gl2": (C+"ComponentsGoodRankTwo.lean",1,None,"Actual rank-two application; geometric suppliers remain explicit"),
 "gl3": (C+"PropagationTheoremGL3.lean",1,None,"Actual rank-three application and final intersection of the two finite ideals"),
 "nice_app": (C+"ExistsNicePrimeAboveOfLargeDim.lean",1,None,"Exact next consumer of NicePrimeEx with triangular/coincident-locus bounds"),
 "locflat": (F+"LocFlat.lean",1,None,"Retained arithmetic deformation-chart flatness supplier"),
 "locrho": (F+"LocRho.lean",1,None,"Retained arithmetic local chart and representation dictionary"),
 "loccpl": (F+"LocCpl.lean",162,188,"Retained actual arithmetic completion from the local universal property"),
 "graded": (F+"IsInternalCongr.lean",81,None,"Retained generic gr_A; UCE13 with its FinA antecedent cannot replace this upstream theorem"),
 "sharp2": (F+"ChainedBot.lean",1,None,"Retained rank-two sharp component-chain supplier"),
 "sharp3": (F+"ChainedOfComap.lean",1,None,"Retained rank-three sharp component-chain supplier"),
 "dim": (F+"KrullDimLtOfNotLeTriangular.lean",1,None,"Retained triangular and coincident-character dimension bounds"),
 "conn": (F+"PreconnectedRankTwo.lean",1,None,"Retained preconnected core supplier"),
 "seedpt": (F+"Seedpt.lean",1,None,"Retained passage from the seed to a large local prime"),
 "corner": (F+"QuotientHomNonvanishingBound.lean",1,None,"Retained actual rank-two corner and finite exceptional-type ideal l53"),
 "tworuns": (D+"TwoRuns.lean",80,109,"Actual same-frame two-rank and two-place call, with separate rings and ideals"),
 "finptdown": (C+"FinPtDown.lean",113,None,"Retained finPtDown: descent from the extended coefficient frame to the original frame"),
 "linkedend": (D+"LinkedEndE.lean",18,67,"Actual common linked endpoint applies finPtDown at line 67"),
}

# New dependencies, exact source keys, inherited human proofs.
REL = {
 1:([],["cd","co","clsub"],[]),
 2:([1],["cd","co","space","pointdefs","pointloc"],[]),
 3:([],["flag","lagrange"],[]),
 4:([3],["o1","frame","space"],[]),
 5:([],["torsion"],[]),
 6:([5],["char"],[]),
 7:([6],["diag","frame","space"],[]),
 8:([],["cycle"],[]),
 9:([2],["finpt","pointdefs","space"],[]),
10:([4,7],["finpt","pointdefs","space"],[]),
11:([1,2,8,9,10],["finpt","pointdefs","finend","abs"],["AFE15","AFE16","AFE20"]),
12:([],["nice"],[]),
13:([12],["nice","nice_defs"],[]),
14:([],["local","local_defs"],[]),
15:([],["global","global_defs"],[]),
16:([],["chart","chart_defs"],[]),
17:([14,16],["charts","chart_defs"],[]),
18:([],["gl3","space","pointdefs"],[]),
19:([],["ends","alt","alt3","aut3","alt2"],[]),
}

EXT = {
 "ACP_LOCAL_ALGEBRA": {"kind":"named_classical_commutative_algebra", "statement":"DVR structure and adic completeness; finite generation of submodules over a Noetherian ring; Krull intersection for Noetherian local rings; principal and generalized principal ideal theorems; finite prime avoidance and systems of parameters. ACP1 and ACP12–13 give the needed subring and prime constructions rather than importing their source conclusions.","source_keys":["clsub","nice","char"]},
 "ACP_SUPPLIED_FRAME_SPACE": {"kind":"original_theorem_antecedent", "statement":"Original coefficient DVR with IsCoef, F.Ok(C0), and a supplied Space on that exact frame. ACP11 retains the literal OffFin antecedent. No Big, characteristic-zero test-ring, or automorphic premise is introduced for FinPtOf. The existence of a suitable Space and production of OffFin remain separate.","source_keys":["space","pointdefs","frame"]},
 "ACP_LOCAL_PROPAGATION_DATA": {"kind":"original_theorem_antecedent", "statement":"Exactly the ten LocData.Ok conditions, explicitly listed before ACP14; in particular P1 and flipTwoThree are retained original inputs. R is Noetherian but need not be local. No disjointness of the type sets is assumed.","source_keys":["local_defs"]},
 "ACP_GLOBAL_PROPAGATION_DATA": {"kind":"original_theorem_antecedent", "statement":"Exactly the eight GlobData.Ok conditions, explicitly listed before ACP15; X is Noetherian. Neither openness of TI nor closedness of Good is needed for this abstract theorem.","source_keys":["global_defs"]},
 "ACP_FLAT_CHART_FOUNDATIONS": {"kind":"standard_commutative_algebra_and_spectrum_topology", "statement":"Elementary spectrum/localization dictionary, existence of minimal primes, closed irreducible subsets of an affine spectrum, flat base change and localization. ACP16 includes the faithful-flatness/going-down argument needed for the chart; no Noetherian hypothesis is added to ChartOfFlat.","source_keys":["chart"]},
 "ACP_GENERAL_CHART_INPUT": {"kind":"original_theorem_antecedent", "statement":"For ACP17, the arbitrary supplied Chart, local Noetherian ring, openness of TI, closedness of Good, their exact pullback identifications, and the original local Concl. ACP17 proves all three original outputs; it does not assume the chart is one obtained from a flat map.","source_keys":["chart_defs"]},
 "ACP_ALT_INPUT": {"kind":"original_theorem_antecedent", "statement":"For ACP19 only, the complete Alt endpoint at its original quantifiers. Projection preserves the same g1, Marks and FinEnd. Actual WitA and WitAQ producers remain required by the terminal Alt route; no converse and no Alt producer are asserted.","source_keys":["ends","alt","alt3","alt2"]},
}
USES = {i:[] for i in REL}
for i in [1,2,5,6,7,12,13]: USES[i].append("ACP_LOCAL_ALGEBRA")
for i in [2,4,7,9,10,11]: USES[i].append("ACP_SUPPLIED_FRAME_SPACE")
USES[14] = ["ACP_LOCAL_PROPAGATION_DATA"]
USES[15] = ["ACP_GLOBAL_PROPAGATION_DATA"]
USES[16] = ["ACP_FLAT_CHART_FOUNDATIONS"]
USES[17] = ["ACP_GENERAL_CHART_INPUT"]
USES[19] = ["ACP_ALT_INPUT"]

def sha(b): return hashlib.sha256(b).hexdigest()
def dump(name,value): (HERE/name).write_text(json.dumps(value,indent=2,ensure_ascii=False)+"\n")

def inherited(cid):
    comp = "arithmetic_frame_entries_v52" if cid.startswith("AFE") else "linked_frame_completion_v51"
    p = ROOT/comp/"provenance.json"
    raw = p.read_bytes()
    old = next(c for c in json.loads(raw)["claims"] if c["id"]==cid)
    loc = old["proof_location"]
    main = (ROOT/loc["file"]).read_bytes()
    piece = b"".join(main.splitlines(keepends=True)[loc["line_start"]-1:loc["line_end"]])
    if sha(piece)!=loc.get("sha256",loc.get("proof_range_sha256")): raise ValueError(("inherited range",cid))
    return {"id":cid,"component":comp,"file":loc["file"],"label":"claim:"+cid,
        "file_sha256":sha(main),"line_start":loc["line_start"],"line_end":loc["line_end"],
        "proof_range_sha256":sha(piece),"parent_provenance_file":str(p.relative_to(ROOT)),
        "exact_parent_provenance_sha256":sha(raw),
        "scope":"Exact reviewed scope, including retained original P for AFE15/16. LFC3/6 identify the already constructed frame fields; generic ACP7 uses the literal Ok antecedent."}

def main():
    ap=argparse.ArgumentParser(); ap.add_argument("--repo",type=Path,required=True); args=ap.parse_args()
    repo=args.repo.resolve()
    if subprocess.check_output(["git","-C",str(repo),"rev-parse","HEAD"],text=True).strip()!=PIN: raise ValueError("wrong pin")
    sources,files,texts,excerpts={},{},{},[]
    for key,(rel,first,last,decl) in SPECS.items():
        blob=subprocess.check_output(["git","-C",str(repo),"show",PIN+":"+rel])
        if (repo/rel).read_bytes()!=blob: raise ValueError(("checkout differs from pin",rel))
        lines=blob.splitlines(keepends=True); last=last or len(lines)
        if not 1<=first<=last<=len(lines): raise ValueError(("bad range",key,first,last,len(lines)))
        dst=HERE/"source_snapshot"/rel; dst.parent.mkdir(parents=True,exist_ok=True); dst.write_bytes(blob)
        piece=b"".join(lines[first-1:last]); url="https://github.com/CocoSgt/riemann-hypothesis-lean/blob/"+PIN+"/"+rel
        files[rel]={"path":rel,"snapshot_file":str(dst.relative_to(ROOT)),"sha256":sha(blob),"bytes":len(blob),"line_count":len(lines),"source_commit":PIN,"url":url,"verified_equal_to_pinned_git_blob":True}
        sources[key]={"id":"ACP_SRC_"+key.upper(),"path":rel,"declaration":decl,"line_start":first,"line_end":last,"source_commit":PIN,"file_sha256":sha(blob),"full_file_sha256":sha(blob),"range_sha256":sha(piece),"range_bytes":len(piece),"snapshot_file":str(dst.relative_to(ROOT)),"verified_equal_to_pinned_git_blob":True,"url":url+f"#L{first}-L{last}"}
        texts[key]=piece.decode(); excerpts.append("["+sources[key]["id"]+"] "+decl+"\n"+sources[key]["url"]+"\n"+piece.decode())
    text=(HERE/"main.tex").read_text(); mainsha=sha(text.encode())
    blocks={m.group(1):m for m in re.finditer(r"% BEGIN (ACP\d+)\n.*?% END \1\n",text,re.S)}
    expected={"ACP"+str(i) for i in REL}
    if set(blocks)!=expected: raise ValueError("claim set mismatch")
    hashes={cid:sha(m.group().encode()) for cid,m in blocks.items()}
    reviews=[]
    for p in sorted(HERE.glob("independent_review*.json")):
        r=json.loads(p.read_text())
        if r.get("result",r.get("status"))!="PASS": continue
        bound=r.get("proof_file_sha256",r.get("main_sha256",r.get("main_tex_sha256")))
        if bound!=mainsha: raise ValueError(("stale review main",p))
        ids=r.get("claims_reviewed",r.get("reviewed_claims",[]))
        ids=[x if isinstance(x,str) else x.get("id",x.get("claim")) for x in ids]
        for cid in ids:
            if cid not in hashes or r.get("proof_hashes",{}).get(cid)!=hashes[cid]: raise ValueError(("review block",cid))
        reviews.append({"file":str(p.relative_to(ROOT)),"sha256":sha(p.read_bytes()),"reviewer":r.get("reviewer"),"result":"PASS","proof_file_sha256":mainsha,"claims":ids})
    reviewed={cid for r in reviews for cid in r["claims"]}
    status="complete_at_stated_scope_independently_reviewed" if expected<=reviewed else "complete_at_stated_scope_pending_independent_review"
    common={"artifact_version":VERSION,"component":HERE.name,"source_commit":PIN,"proof_file_sha256":mainsha,"status":status}
    human={cid:inherited(cid) for cid in ["AFE15","AFE16","AFE20","LFC3","LFC6"]}
    claims=[]
    for i,(deps,keys,ids) in REL.items():
        cid="ACP"+str(i); m=blocks[cid]; start=text[:m.start()].count("\n")+1
        claims.append({"id":cid,"title":m.group().split("\n")[1],"introduced_in":VERSION,"classification":"B","depends_on":["ACP"+str(d) for d in deps]+ids,"external_input_ids":USES[i],"sources":[sources[k] for k in keys],"proof_location":{"file":HERE.name+"/main.tex","label":"claim:"+cid,"line_start":start,"line_end":start+m.group().count("\n")-1,"sha256":hashes[cid],"bytes":len(m.group().encode())},"status":"complete_at_stated_scope_independently_reviewed" if cid in reviewed else "complete_at_stated_scope_pending_independent_review","independent_review_files":[r["file"] for r in reviews if cid in r["claims"]],"source_proof_is_not_human_proof":True})
    ext=[{"id":eid,**e,"source_bindings":[sources[k] for k in e["source_keys"]]} for eid,e in EXT.items()]
    endpoints=[
      {"id":"full_original_FinPtOf","claim":"ACP11","scope":"Every original IsCD test ring and specified O→k→A scalar tower; supplied Space and literal OffFin; no Big or automorphy premise","same_frame":True,"point_loc_imported":False},
      {"id":"exact_IsLiftA_point_realization","claim":"ACP2","scope":"Every original IsCD finite-point test on the supplied Space; literal diagonal reduction retained","general_point_loc_claimed":False},
      {"id":"full_original_flag_loc","claim":"ACP3","scope":"Arbitrary commutative local ring, group, rank and original separator/ordered-product assumptions"},
      {"id":"full_original_o1","claim":"ACP4","scope":"Original rank two or three supplied space and Ok; every subsequent algebra map"},
      {"id":"full_original_oneUnitTF","claim":"ACP5","scope":"Every positive prime characteristic and original local-domain assumptions"},
      {"id":"full_original_NicePrimeEx","claim":"ACP13","scope":"Original arbitrary Noetherian local ring, N≥1, finite family, ideal I and element varpi in maximal ideal"},
      {"id":"full_original_LocProp","claim":"ACP14","scope":"All ten literal Ok fields; arbitrary Noetherian ring, not necessarily local"},
      {"id":"full_original_GlobProp","claim":"ACP15","scope":"All eight literal Ok fields; Noetherian topological space"},
      {"id":"full_original_ChartOfFlat","claim":"ACP16","scope":"Arbitrary open affine chart and local flat algebra; no Noetherian hypothesis"},
      {"id":"full_original_GlobOfCharts","claim":"ACP17","scope":"Arbitrary supplied Chart and all three original outputs"},
      {"id":"rank_three_final_ideal_intersection","claim":"ACP18","scope":"Same supplied type-I and exceptional-type ideals and common lambda"},
      {"id":"full_Alt_to_original_endpoint_projection","claim":"ACP19","scope":"GdEndAlt→GdEnd and HostEndAlt→HostEnd, identical g1/Marks/FinEnd; no converse and no Alt producer"},
    ]
    retained=[
      {"id":"ACP_ARITHMETIC_CHART_GEOMETRY","statement":"Actual arithmetic local charts, flatness, generic gr_A, completion loc_cpl and representation dictionary; generic ChartOfFlat does not construct them. UCE13 assumes FinA and cannot replace generic gr_A upstream of FinPt/FinEnd without circularity.","source_keys":["locflat","locrho","loccpl","graded"]},
      {"id":"ACP_SHARP_AND_DIMENSION_BOUNDS","statement":"Rank-two/rank-three sharp component chains and dimensions, triangular and coincident-character dimension bounds, and their NicePrimeEx application.","source_keys":["sharp2","sharp3","dim","nice_app"]},
      {"id":"ACP_CORE_AND_SEED_GEOMETRY","statement":"Preconnected core, closed-point density and generic-component incidence, plus passage of the seed to a large local prime.","source_keys":["conn","seedpt","gl2","gl3"]},
      {"id":"ACP_RANK_TWO_CORNER_IDEAL","statement":"Actual rank-two corner on the odd-weight quotient and its map between the two distinct weight-zero algebras, producing FinLam and exceptional-type containment (l53).","source_keys":["corner"]},
      {"id":"ACP_AUTOMORPHIC_AND_PATCHING_PRODUCERS","statement":"The two actual automorphic seeds, suitable supplied spaces, finite modularity ideals, P1'/P23'/SeedIn, arithmetic-point classicality and Alt WitA/WitAQ. These are not produced by the abstract propagation principles or elementary projection.","source_keys":["pointdefs","abs","tworuns","alt","alt2"]},
      {"id":"ACP_FINPT_COEFFICIENT_DESCENT","statement":"Actual TwoRuns returns FinPt c1.O (Phi.ext f) 3. The original finPtDown, called in LinkedEndE line 67, must descend this to FinPt c.O Phi 3 before AFE20. ACP11 works at either frame but does not reconstruct this transport or identify the two coefficient frames.","source_keys":["tworuns","finptdown","linkedend"]},
    ]
    retained=[{**r,"source_bindings":[sources[k] for k in r["source_keys"]]} for r in retained]
    contract={"schema":"rh-human-component-contract/1",**common,"closed_subcontracts":endpoints,
      "entry_premises":["Literal supplied original F.Ok and Space for FinPtOf","Literal original OffFin on that same Space","All original local/global propagation data, explicitly listed in the chapter","Original arithmetic P retained when applying AFE15/16","Actual Alt endpoint only as antecedent of the elementary projection"],
      "full_original_FinPtOf_closed":True,"full_original_FinPt_producer_supplied":False,
      "full_original_finPtDown_supplied":False,"extended_and_original_coefficient_frames_kept_distinct":True,
      "full_PropagationTheoremGL2_closed":False,"full_PropagationTheoremGL3_closed":False,
      "full_general_point_loc_closed":False,"source_point_loc_used_as_axiom":False,
      "all_original_IsCD_tests_preserved":True,"finite_residue_degree_supplied_by_IsCD":True,
      "specified_scalar_tower_preserved":True,"ordinary_character_values_and_inverses_in_C":True,
      "full_Alt_to_original_projection_closed":True,"actual_Alt_producer_supplied":False,
      "WitA_and_WitAQ_retained_on_terminal_route":True,"full_GdEnd_closed":False,"full_HostEnd_closed":False,
      "full_GdEndAlt_closed":False,"full_HostEndAlt_closed":False,
      "original_P_retained":True,"host_ell_3_allowed":True,"same_g1":True,
      "choice_order":["Original AFE Dat or Host frame, retaining original P and specified place","Same extended coefficient frame and marking g1 before rank-two/rank-three realizations","Separate S2/M2 and S3/M3 on that same extended frame","Rank-two AllGood before rank-three exceptional ideal and OffFin","One OffFin ideal before every IsCD ring and IsLiftA point","Retained finPtDown transports extended-frame FinPt to original-frame FinPt","AFE20 chooses G_L before all later ordinary points"],
      "retained_suppliers":retained,"exact_whole_closures":{},"new_global_frontier_leaf_closures":[],
      "selected_producer_closed":False,"root_ledger_modified":False,"no_lean_replay":True}
    dump("contracts.json",contract)
    dump("original_contracts.json",{"schema":"rh-original-contracts/1",**common,"contract_keys":["cd","co","space","pointdefs","nice_defs","local_defs","global_defs","chart_defs","ends","alt","alt3","aut3","alt2"],"verbatim_source_contracts":{k:texts[k] for k in ["cd","co","space","pointdefs","nice_defs","local_defs","global_defs","chart_defs","ends","alt","alt3","aut3","alt2"]}})
    dump("provenance.json",{"schema":"rh-human-component-provenance/1",**common,"claims":claims,"inherited_human_inputs":list(human.values()),"classical_and_foundational_inputs":ext,"independent_reviews":reviews,"source_proof_is_not_human_proof":True,"root_ledger_modified":False})
    dump("source_manifest.json",{"schema":"rh-pinned-source-manifest/1",**common,"source_repository":"https://github.com/CocoSgt/riemann-hypothesis-lean","files":list(files.values()),"ranges":list(sources.values()),"file_count":len(files),"range_count":len(sources)})
    dump("inherited_inputs.json",{"schema":"rh-inherited-proof-bindings/1",**common,"inputs":list(human.values())})
    dump("retained_foundations.json",{"schema":"rh-retained-foundations/1",**common,"inputs":ext,"still_unsupplied_producers":retained})
    dump("classical_inputs.json",{"schema":"rh-classical-input-registry/1",**common,"inputs":[e for e in ext if e["kind"] in ["named_classical_commutative_algebra","standard_commutative_algebra_and_spectrum_topology"]]})
    dump("published_inputs.json",[])
    dump("claim_dag.json",{"schema":"rh-human-claim-dag/1",**common,"claims":[{"id":c["id"],"depends_on":c["depends_on"]} for c in claims]})
    dump("closure.json",{"schema":"rh-human-component-closure/1",**common,"closed_subcontracts":endpoints,"independent_reviews":reviews,"pending_review_claims":sorted(expected-reviewed,key=lambda x:int(x[3:])),"exact_whole_closures":{},"new_global_frontier_leaf_closures":[],"proposed_global_frontier_leaf_closures":[],"full_original_FinPtOf_closed":True,"actual_FinPt_producer_remains_open":True,"full_original_finPtDown_remains_open":True,"full_PropagationTheoremGL2_remains_open":True,"full_PropagationTheoremGL3_remains_open":True,"full_GdEnd_remains_open":True,"full_GdEndAlt_remains_open":True,"original_P_retained":True,"all_IsCD_tests_preserved":True})
    (HERE/"source_excerpts.txt").write_text("\n\n".join(excerpts))
    report="""ARITHMETIC COMPONENT PROPAGATION — v0.53

ACP1–ACP19 contain detailed human proofs of the full original FinPtOf
and of complete original subtheorems used by rank-two/rank-three
component propagation.  The finite-point proof handles every original
IsCD test ring and the specified O→k→A scalar tower.  It uses the
explicit subring C=k+m_A; finite residue degree follows from IsCD's
finite residue field, and completeness and Noetherianity are proved.
All full ordinary-character values and inverses belong to C.  Literal
diagonal reduction is available at the actual FinPt consumer; the
broader triangular-residual point_loc is neither assumed nor claimed.

The ordered-product projector argument proves full flag_loc over every
commutative local ring and every rank.  It gives the actual local
characteristic polynomial o1, after every coefficient map.  The two
finite-point branches are both proved: off-triangular points collapse
the weight-zero algebra using the single FinLam ideal; triangular
points have exact characters by local detectors, the uniform class
exponent, finite principal-unit quotients and Krull intersection.
An explicit determinant calculation completes full FinPtOf.

The geometric subtheorems proved in full are NicePrimeEx, LocProp,
GlobProp, ChartOfFlat and GlobOfCharts, with all their original scopes
and fields.  Their proofs include the one-dimensional prime avoiding
every bad ideal, the two-state local component induction, the finite
closed-union/preconnectedness argument, flat going down, and all three
global-chart conclusions.  The actual final rank-three ideal operation
is also proved.  GdEndAlt→GdEnd and HostEndAlt→HostEnd follow by literal
projections, retaining the same marking; this does not construct Alt.

EXACT BOUNDARY
FinPtOf retains its original OffFin antecedent on a supplied Space.
The specific deformation dimensions, sharp component chains, core
connectedness/density, seed-prime dimensions and rank-two corner ideal
are still unsupplied arithmetic geometry.  Thus full rank-two and
rank-three propagation, the actual FinPt producer, automorphic seeds,
patching/classicality and Alt WitA/WitAQ remain separate.  No complete
GdEnd, HostEnd, Alt endpoint, selected whole frontier leaf or human
RH/Dirichlet GRH proof is claimed closed.  AFE20 is the exact downstream
FinEnd consumer, on the same frame and g1, choosing G_L before points.

The actual TwoRuns call first gives FinPt over the extended coefficient
frame.  The separate original finPtDown transport, used in LinkedEndE
at line 67, remains required before applying AFE20 on the original
frame.  The two coefficient frames are not identified.  The upstream
arithmetic charts also require generic gr_A and loc_cpl: UCE13 assumes
the downstream FinA conclusion and cannot replace generic gr_A here.

The original arithmetic P premise and Host ell=3 are retained.
All v52 and earlier artifacts are unchanged.  No Lean replay or PDF.
"""
    (HERE/"report.txt").write_text(report+f"\nPin: {PIN}\nMain SHA256: {mainsha}\nStatus: {status}\nClaims: {len(claims)}; source files/ranges: {len(files)}/{len(sources)}\n")
    dump("hashes.json",{"component":HERE.name,"artifact_version":VERSION,"hashes":{p.name:sha(p.read_bytes()) for p in sorted(HERE.iterdir()) if p.is_file() and p.name!="hashes.json"}})
    print(json.dumps({"component":HERE.name,"claims":len(claims),"source_files":len(files),"source_ranges":len(sources),"main_sha256":mainsha,"status":status},indent=2))

if __name__=="__main__": main()
