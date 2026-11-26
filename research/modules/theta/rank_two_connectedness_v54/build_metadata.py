#!/usr/bin/env python3
"""Bind RTC human proofs and their exact original scopes; never replay Lean."""
from pathlib import Path
import argparse
import hashlib
import json
import re
import subprocess

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
PIN = "7cbf7a0c32fca1badf05931879a37c3f8a2b03b4"
VERSION = "0.54"
V = "src/Development/AutomorphicArithmetic/AutomorphicVarieties/"
F = V + "FrobeniusSmoothVectors/"
C = V + "CurveDVRSpecialization/"
A = V + "CommutativeAlgebra/"
D = V + "ModularityArgument/ThresholdArguments/DenseThresholdCases/"

SPECS = {
 "co": (A+"ResMapBijective.lean",9,75,"Original IsCO, residue preservation and adic continuity"),
 "weights": (A+"ResMapBijective.lean",77,196,"Formal weight parts, homogeneous kernel, WPres and its actual graded algebra"),
 "space": (F+"LeAdicClosure.lean",9,259,"Original NRep, IsBar, Space, B/A/gr, maximal ideal and BB core"),
 "frame": (F+"ContinuousCoboundaries2.lean",124,214,"Original frame and all Ok fields; no Big is added to core connectedness"),
 "cone": (F+"ContinuousCoboundaries2.lean",11,63,"Literal strict Z1C, continuous boundaries and H1C quotient"),
 "strict": (F+"StrYMap.lean",33,71,"Original strS and linear transport"),
 "fpt": (F+"StrSMul.lean",70,91,"Original scalar multiplication, FPt and arbitrary-map composition"),
 "co_span": (A+"CoSpan.lean",15,108,"Relative cotangent-space generation from maps determined by coordinates"),
 "co_surj": (A+"CoSurj.lean",6,32,"Formal coefficient-algebra surjectivity"),
 "co_mvps": (A+"CoMvps.lean",21,40,"Finite-variable power-series coefficient algebras"),
 "coord": (A+"CoordGrading.lean",29,93,"Weighted coordinates from uniqueness and diagonal-torus stability"),
 "twist": (F+"AlgTwist.lean",54,72,"Actual normalized-representation diagonal twist"),
 "coordinate_entries": (F+"ContMap.lean",117,297,"Universal twists, coordinate uniqueness and selected centered entries"),
 "wpres": (F+"ContMap.lean",307,402,"Full original wpres for both allowed ranks"),
 "homog": (A+"HomogOfStable.lean",136,194,"Kernel homogeneity; RTC gives direct integer-weight formal-unit argument"),
 "eigen": (A+"EigenMem.lean",55,111,"Actual eigenvectors in the homogeneous parts"),
 "part_closed": (A+"PartClosed.lean",74,134,"Closedness of homogeneous parts"),
 "part_span": (A+"PartSpan.lean",5,51,"Finite homogeneous monomial spanning"),
 "part_filt": (A+"PartFilt.lean",54,175,"Fixed-weight cofinality of the ideal filtrations"),
 "zero_co": (A+"WPresGrZeroIsCOOfMemMaximalIdeal.lean",71,107,"Degree-zero complete Noetherian coefficient ring"),
 "gr_noeth": (A+"GrNoeth.lean",8,74,"Finite homogeneous pieces and Noetherian graded algebra"),
 "cob": (F+"CoB.lean",8,26,"Full original co_B"),
 "gra": (F+"IsInternalCongr.lean",81,86,"Full original gr_A, upstream of FinPt/FinEnd/FinA"),
 "contu": (F+"MemPowSmulLe.lean",14,110,"Full original cont_u, including every graded-piece filtration clause"),
 "smooth_char": (F+"SmoothCharacterExtendsToOpenSubgroup.lean",7,52,"Full original automatic local constancy, IsBar and uniqueness for FPt"),
 "normalize": (F+"SmoothVectorFixedByOpenSubgroup.lean",6,90,"Full original normalized nonzero strict cocycle; no continuity of arbitrary chi required"),
 "nonzero": (F+"ExistsMemStrSNeZeroOfFrameOk.lean",12,61,"Full original nonzero strS supplier from f4'"),
 "rep": (F+"PreconnectedRankTwo.lean",12,131,"Actual lower-triangular normalized rank-two representation"),
 "fiber": (F+"FramePointFiberNonempty.lean",6,64,"Full original extraction of a strict cocycle from a triangular rank-two representation"),
 "smooth_hom": (F+"SmoothHomWeightSumNeg.lean",53,115,"Original realization theorem; RTC supplies its rank-two case only"),
 "pt_ex": (F+"PreconnectedRankTwo.lean",139,152,"Original rank-two pt_ex; RTC constructs it directly over arbitrary target k-algebras"),
 "pt_uniq": (F+"PreconnectedRankTwo.lean",153,172,"Original rank-two pt_uniq"),
 "pt_mem": (F+"PreconnectedRankTwo.lean",173,184,"Original rank-two pt_mem"),
 "dual": (F+"SmoothDualExact.lean",7,31,"Original core residue-field point supplier; RTC supplies its rank-two case"),
 "line": (F+"PreconnectedRankTwo.lean",185,204,"Original polynomial-line generic prime and all later evaluation maps"),
 "preconnected": (F+"PreconnectedRankTwo.lean",206,264,"Full original preconnected_rank_two"),
 "gl2": (C+"ComponentsGoodRankTwo.lean",31,163,"Actual rank-two consumer; other local/global data remain explicit"),
 "prop_defs": (C+"PropagationTheoremGL2.lean",31,84,"Original propagation and finite-point predicates"),
 "cd": (C+"IsUnitOrIsUnitOfAddOne.lean",107,110,"Full original IsCD, including finite residue field"),
 "fpd_ext": (C+"FinPtDown.lean",53,102,"Actual common test-DVR extension supplier; RTC constructs finite residue fields directly"),
 "fpd_cont": (C+"FinPtDown.lean",103,112,"Original continuity transport under a local map"),
 "fpd": (C+"FinPtDown.lean",113,155,"Full original finPtDown at arbitrary rank"),
 "fpd_contract": (C+"EveryPointSatisfiesFrameCondition.lean",133,137,"Literal original FinPtDown contract and prescribed coefficient maps"),
 "finend": (C+"FinEndOfFinPt.lean",9,48,"Inherited AFE20 original-frame FinPt-to-FinEnd consumer"),
 "tworuns": (D+"TwoRuns.lean",80,109,"Actual extended-frame finite-point output, with separate spaces and ideals"),
 "linked": (D+"LinkedEndE.lean",18,67,"Actual linked endpoint uses finPtDown at line 67"),
 "loccpl": (F+"LocCpl.lean",100,188,"Retained actual local completion from its universal property"),
 "locflat": (F+"LocFlat.lean",37,69,"Retained actual arithmetic local chart flatness"),
 "locrho": (F+"LocRho.lean",40,66,"Retained actual local representation and ideal dictionary"),
 "sharp2": (F+"ChainedBot.lean",51,86,"Retained rank-two sharp component chains and dimensions"),
 "dim": (F+"KrullDimLtOfNotLeTriangular.lean",36,58,"Retained triangular/coincident-character dimension bounds"),
 "seed": (F+"Seedpt.lean",9,30,"Retained actual seed-prime incidence and dimension comparison"),
 "corner": (F+"QuotientHomNonvanishingBound.lean",221,236,"Retained rank-two-to-rank-three corner and exceptional ideal"),
 "gl3": (C+"PropagationTheoremGL3.lean",213,229,"Retained full rank-three propagation and OffFin producer"),
 "pointloc": (F+"PointLoc.lean",1,None,"Broader general point_loc remains separate; it is not imported in RTC15"),
}

# Numbered dependencies, exact source keys and inherited mathematical inputs.
REL = {
 1:([],["co","space","coordinate_entries"],[]),
 2:([1],["co_span","co_surj","co_mvps","coord","coordinate_entries"],[]),
 3:([1,2],["twist","coordinate_entries","homog","coord"],[]),
 4:([2,3],["weights","eigen","part_closed"],[]),
 5:([],["part_span","gr_noeth","zero_co"],[]),
 6:([2,5],["zero_co","co_mvps","cob"],[]),
 7:([2,3,4,5,6],["wpres","cob","gra","gr_noeth","space"],[]),
 8:([2,4,5,6,7],["part_filt","contu"],[]),
 9:([7,8],["contu","space"],[]),
10:([7,9],["smooth_char","fpt"],[]),
11:([],["cone","normalize","frame"],[]),
12:([11],["nonzero","strict","frame"],[]),
13:([],["strict","frame"],[]),
14:([13],["rep","fiber","space","strict"],[]),
15:([1,13,14],["pt_ex","smooth_hom","space","co_mvps"],[]),
16:([10,14,15],["pt_mem","pt_uniq","fpt"],[]),
17:([10,14],["dual","space"],[]),
18:([15,16],["line"],[]),
19:([12,15,16,17,18],["preconnected","gl2"],[]),
20:([7,19],["gl2","prop_defs"],[]),
21:([],["fpd_ext","cd"],[]),
22:([21],["fpd_ext","cd"],[]),
23:([22],["fpd_cont","fpd","cd","fpd_contract"],[]),
24:([22,23],["fpd","fpd_contract","prop_defs"],[]),
25:([24],["tworuns","linked","finend","prop_defs"],["ACP11","AFE20"]),
}

EXT = {
 "RTC_UNIVERSAL_SPACE": {
  "kind":"original_theorem_antecedent",
  "statement":"Original complete coefficient DVR with IsCoef, full F.Ok(C0), and the supplied universal Space in rank two or three. RTC proves the actual upstream algebra and connectedness on this Space; existence of the automorphic/modularity realization remains a separate producer. Original P is retained at the inherited AFE/LFC frame entry.",
  "source_keys":["space","frame"]
 },
 "RTC_CLASSICAL_LOCAL_ALGEBRA": {
  "kind":"named_classical_commutative_algebra",
  "statement":"Nakayama's lemma for finite modules; the formal power-series Hilbert basis theorem; Krull intersection for Noetherian local rings; completeness of finite-variable power-series rings and their local quotients. The required coordinate generation, homogeneous projections, monomial finite spanning and topology comparisons are proved in RTC1–9 rather than imported as source conclusions.",
  "source_keys":["co_span","co_surj","co_mvps","zero_co","part_closed","part_filt"]
 },
 "RTC_ORIGINAL_STRICT_FRAME_FIELDS": {
  "kind":"original_theorem_antecedent",
  "statement":"The literal odd-characteristic, c^2, del(c), Psi(c), open kernels, f3 and nonzero strict H1C f4' fields of F.Ok. RTC11 normalizes an arbitrary original character without adding its continuity, and RTC12 constructs the actual nonzero strS element from these fields.",
  "source_keys":["frame","cone","normalize","nonzero"]
 },
 "RTC_CLASSICAL_FIELDS_AND_DVR": {
  "kind":"named_classical_algebra",
  "statement":"A nonfield DVR has a principal maximal ideal and its nonzero elements have finite uniformizer order; finite field extensions embed in an algebraic closure over a specified common subfield. RTC21 proves the finite-residue coefficient section and digit expansion, RTC22 constructs the actual common test DVR, and RTC24 proves the full original transport.",
  "source_keys":["fpd_ext","cd"]
 },
 "RTC_SUPPLIED_EXTENDED_FINPT_DATA": {
  "kind":"original_theorem_antecedent",
  "statement":"In RTC25, the actual extended-frame rank-three Space and OffFin are supplied, exactly as ACP11 requires. The actual common frame/link needed by inherited AFE20 remains fixed. No rank-specific propagation, modularity, seed, classicality or Alt witness producer is manufactured by this conditional join.",
  "source_keys":["prop_defs","tworuns","linked","finend"]
 },
}
USES={i:[] for i in REL}
for i in range(1,11): USES[i]=["RTC_UNIVERSAL_SPACE","RTC_CLASSICAL_LOCAL_ALGEBRA"]
for i in [11,12,13,14]: USES[i]=["RTC_ORIGINAL_STRICT_FRAME_FIELDS"]
for i in [15,16,17,18,19,20]: USES[i]=["RTC_UNIVERSAL_SPACE","RTC_ORIGINAL_STRICT_FRAME_FIELDS"]
for i in [21,22,23,24]: USES[i]=["RTC_CLASSICAL_FIELDS_AND_DVR"]
USES[25]=["RTC_SUPPLIED_EXTENDED_FINPT_DATA"]

def sha(data): return hashlib.sha256(data).hexdigest()
def dump(name,data): (HERE/name).write_text(json.dumps(data,indent=2,ensure_ascii=False)+"\n")
def inherited(cid):
    comp="arithmetic_component_propagation_v53" if cid.startswith("ACP") else "arithmetic_frame_entries_v52"
    path=ROOT/comp/"provenance.json"; body=path.read_bytes()
    old=next(x for x in json.loads(body)["claims"] if x["id"]==cid)
    loc=old["proof_location"]; main=(ROOT/loc["file"]).read_bytes()
    block=b"".join(main.splitlines(keepends=True)[loc["line_start"]-1:loc["line_end"]])
    if sha(block)!=loc.get("sha256",loc.get("proof_range_sha256")): raise ValueError(("inherited block",cid))
    return {"id":cid,"component":comp,"file":loc["file"],"label":"claim:"+cid,
      "file_sha256":sha(main),"line_start":loc["line_start"],"line_end":loc["line_end"],
      "proof_range_sha256":sha(block),"parent_provenance_file":str(path.relative_to(ROOT)),
      "exact_parent_provenance_sha256":sha(body),
      "scope":"Exact independently reviewed original scope. ACP11 retains a supplied Space and OffFin; AFE20 consumes original-frame FinPt and fixes G_L before all later ordinary points."}

def main():
    ap=argparse.ArgumentParser();ap.add_argument("--repo",type=Path,required=True);args=ap.parse_args()
    repo=args.repo.resolve()
    if subprocess.check_output(["git","-C",str(repo),"rev-parse","HEAD"],text=True).strip()!=PIN:
        raise ValueError("wrong accepted source pin")
    files,sources,texts,excerpts={},{},{},[]
    for key,(rel,first,last,decl) in SPECS.items():
        body=subprocess.check_output(["git","-C",str(repo),"show",PIN+":"+rel])
        if body!=(repo/rel).read_bytes(): raise ValueError(("checkout differs from pin",rel))
        lines=body.splitlines(keepends=True);last=last or len(lines)
        if not 1<=first<=last<=len(lines): raise ValueError(("range",key,first,last,len(lines)))
        piece=b"".join(lines[first-1:last]);dst=HERE/"source_snapshot"/rel
        dst.parent.mkdir(parents=True,exist_ok=True);dst.write_bytes(body)
        url="https://github.com/CocoSgt/riemann-hypothesis-lean/blob/"+PIN+"/"+rel
        files[rel]={"path":rel,"snapshot_file":str(dst.relative_to(ROOT)),"sha256":sha(body),
          "bytes":len(body),"line_count":len(lines),"source_commit":PIN,"url":url,
          "verified_equal_to_pinned_git_blob":True}
        sources[key]={"id":"RTC_SRC_"+key.upper(),"path":rel,"declaration":decl,
          "line_start":first,"line_end":last,"source_commit":PIN,"file_sha256":sha(body),
          "full_file_sha256":sha(body),"range_sha256":sha(piece),"range_bytes":len(piece),
          "snapshot_file":str(dst.relative_to(ROOT)),"verified_equal_to_pinned_git_blob":True,
          "url":url+f"#L{first}-L{last}"}
        texts[key]=piece.decode()
        excerpts.append("["+sources[key]["id"]+"] "+decl+"\n"+sources[key]["url"]+"\n"+piece.decode())
    text=(HERE/"main.tex").read_text();mainsha=sha(text.encode())
    blocks={m.group(1):m for m in re.finditer(r"% BEGIN (RTC\d+)\n.*?% END \1\n",text,re.S)}
    expected={"RTC"+str(i) for i in REL}
    if set(blocks)!=expected: raise ValueError("numbered block set mismatch")
    proofhash={cid:sha(m.group().encode()) for cid,m in blocks.items()}
    reviews=[]
    for p in sorted(HERE.glob("independent_review*.json")):
        r=json.loads(p.read_text())
        if r.get("result",r.get("status"))!="PASS": continue
        if r.get("proof_file_sha256",r.get("main_sha256",r.get("main_tex_sha256")))!=mainsha:
            raise ValueError(("reviewed main differs",p))
        ids=r.get("claims_reviewed",r.get("reviewed_claims",r.get("claims",[])))
        ids=[x if isinstance(x,str) else x.get("id",x.get("claim")) for x in ids]
        hashes=dict(r.get("proof_hashes",{}))
        for x in r.get("claims_reviewed",[]):
            if isinstance(x,dict): hashes[x.get("id",x.get("claim"))]=x.get("block_sha256",x.get("proof_range_sha256",x.get("sha256")))
        for cid in ids:
            if hashes.get(cid)!=proofhash[cid]: raise ValueError(("review block",cid))
        reviews.append({"file":str(p.relative_to(ROOT)),"sha256":sha(p.read_bytes()),
          "reviewer":r.get("reviewer"),"result":"PASS","proof_file_sha256":mainsha,"claims":ids})
    reviewed={cid for r in reviews for cid in r["claims"]}
    status="complete_at_stated_scope_independently_reviewed" if expected<=reviewed else "complete_at_stated_scope_pending_independent_review"
    common={"artifact_version":VERSION,"component":HERE.name,"source_commit":PIN,
      "proof_file_sha256":mainsha,"status":status}
    claims=[]
    for i,(deps,keys,parents) in REL.items():
        cid="RTC"+str(i);m=blocks[cid];first=text[:m.start()].count("\n")+1
        claims.append({"id":cid,"title":m.group().split("\n")[1],"introduced_in":VERSION,
          "classification":"B","depends_on":["RTC"+str(j) for j in deps]+parents,
          "external_input_ids":USES[i],"sources":[sources[k] for k in keys],
          "proof_location":{"file":HERE.name+"/main.tex","label":"claim:"+cid,
            "line_start":first,"line_end":first+m.group().count("\n")-1,
            "sha256":proofhash[cid],"bytes":len(m.group().encode())},
          "status":"complete_at_stated_scope_independently_reviewed" if cid in reviewed else "complete_at_stated_scope_pending_independent_review",
          "independent_review_files":[r["file"] for r in reviews if cid in r["claims"]],
          "source_proof_is_not_human_proof":True})
    human=[inherited(cid) for cid in ["ACP11","AFE20"]]
    ext=[{"id":eid,**record,"source_bindings":[sources[k] for k in record["source_keys"]]} for eid,record in EXT.items()]
    endpoints=[
      {"id":"full_original_wpres","claim":"RTC7","scope":"Every original supplied Space at rank two or three, same actual B/A/gr; integer weights and coefficient DVR as in the source endpoint"},
      {"id":"full_original_co_B","claim":"RTC7","scope":"All original IsCO clauses on the actual B, maximal ideal exactly S.mB"},
      {"id":"full_original_gr_A","claim":"RTC7","scope":"All seven original fields at both allowed ranks; no FinA or finite-point hypothesis"},
      {"id":"full_original_cont_u","claim":"RTC9","scope":"All matrix/character/diagonal continuity clauses and every fixed-weight/N cofinality clause, both allowed ranks"},
      {"id":"full_original_smoothCharacter_extends_to_open_subgroup","claim":"RTC10","scope":"Every original target commutative k-algebra, including zero/nonreduced targets; exact IsBar and uniqueness"},
      {"id":"full_original_smooth_vector_fixed_by_open_subgroup","claim":"RTC11","scope":"Any field k of characteristic ell and frame F.Ok, with no chosen O/Space, every original chi without an added continuity assumption, and literal strict H1C input"},
      {"id":"full_original_exists_mem_strS_ne_zero_of_frameOk","claim":"RTC12","scope":"Any field k of characteristic ell and frame F.Ok, with no chosen O/Space; the nonzero strict cocycle is constructed from its f4' field"},
      {"id":"full_original_framePoint_fiber_nonempty","claim":"RTC14","scope":"Any field k of characteristic ell and frame F.Ok, with no chosen O/Space; every original triangular normalized rank-two representation and target k-algebra"},
      {"id":"rank_two_smoothHom_weight_sum_neg","claim":"RTC15","scope":"Full rank-two specialization of the original arbitrary-target realization; rank-three realization not claimed"},
      {"id":"full_rank_two_pt_ex_uniq_mem","claim":"RTC16","scope":"Original PreconnectedRankTwo private supplier contracts, with all target k-algebras and arbitrary subsequent maps"},
      {"id":"rank_two_smoothDual_exact","claim":"RTC17","scope":"Every prime of the actual rank-two core, with its actual possibly infinite residue field; higher-rank case not claimed"},
      {"id":"full_original_rank_two_line","claim":"RTC18","scope":"One prime for every supplied polynomial strict family, before every later evaluation and point map"},
      {"id":"full_original_preconnected_rank_two","claim":"RTC19","scope":"Every original coefficient DVR/IsCoef, F.Ok and supplied rank-two Space; no Big/modularity/finite-point antecedent added"},
      {"id":"full_original_FinPtDown","claim":"RTC24","scope":"Original c,c1,f/inclusion/residue compatibility, every frame and arbitrary rank, every prime including two; every IsCD test and exact scalar tower"},
      {"id":"exact_extended_to_original_finite_end_join","claim":"RTC25","scope":"Supplied actual extended-frame Space/OffFin, ACP11 then RTC24 then inherited AFE20, same original link/g1; other producer fields retained"},
    ]
    retained=[
      {"id":"RTC_ACTUAL_SPACE_AND_MODULARITY_REALIZATION","statement":"The actual modularity spaces, ideals, CReal and patching construction remain original producers. The universal Space is the original antecedent of wpres, gr_A, cont_u and preconnected_rank_two; these full implications are now proved.","source_keys":["space","tworuns","linked","prop_defs"]},
      {"id":"RTC_ACTUAL_LOCAL_COMPLETION_AND_FLATNESS","statement":"The actual local completion loc_cpl, local chart flatness loc_flat and local representation/ideal dictionary loc_rho remain. RTC7 and RTC9 now provide their upstream generic graded algebra and continuity inputs; UCE13's FinA-dependent analogue is not used.","source_keys":["loccpl","locflat","locrho"]},
      {"id":"RTC_DIMENSION_DENSITY_AND_SEED_INCIDENCE","statement":"Sharp component chains and dimensions, triangular/coincident-locus bounds, closed-point density/generic-component incidence and seed-prime comparison remain. Core preconnectedness and the actual graded Noetherian algebra are no longer retained gaps.","source_keys":["sharp2","dim","seed","gl2"]},
      {"id":"RTC_RANK_THREE_CORNER_AND_PROPAGATION","statement":"The actual rank-two-to-three corner and exceptional ideal, full rank-two AllGood, full rank-three propagation and OffFin remain. The ranks have separate rings and modularity ideals on the same extended frame.","source_keys":["corner","gl2","gl3","tworuns"]},
      {"id":"RTC_AUTOMORPHIC_AND_ALT_WITNESSES","statement":"Actual seeds, P1'/P23'/SeedIn, arithmetic-point classicality and the stronger terminal Alt WitA/WitAQ producers remain. RTC25 is only the exact finite-end join at its supplied original data.","source_keys":["prop_defs","tworuns","linked"]},
      {"id":"RTC_BROADER_POINT_REALIZATION","statement":"The full generic point_loc and the rank-three smoothHom_weight_sum_neg/smoothDual_exact remain outside this packet. RTC15 proves the entire rank-two triangular realization needed by the actual preconnectedness consumer and makes no claim at those larger scopes.","source_keys":["pointloc","smooth_hom","dual"]},
    ]
    retained=[{**r,"source_bindings":[sources[k] for k in r["source_keys"]]} for r in retained]
    contracts={"schema":"rh-human-component-contract/1",**common,"closed_subcontracts":endpoints,
      "full_original_wpres_supplied":True,"full_original_co_B_supplied":True,
      "full_original_gr_A_supplied":True,"full_original_cont_u_supplied":True,
      "generic_graded_algebra_both_allowed_ranks":True,"upstream_FinA_not_assumed":True,
      "full_original_preconnected_rank_two_supplied":True,
      "arbitrary_target_k_algebras_preserved":True,"arbitrary_core_residue_fields_preserved":True,
      "formal_series_evaluated_only_at_topologically_nilpotent_coordinates":True,
      "only_polynomial_image_evaluated_in_arbitrary_target":True,
      "broader_IsBar_scope_preserved":True,"general_point_loc_imported":False,
      "full_general_point_loc_supplied":False,"rank_three_triangular_realization_supplied":False,
      "full_original_finPtDown_supplied":True,"finPtDown_arbitrary_rank_and_all_primes":True,
      "all_original_IsCD_tests_and_scalar_towers_preserved":True,
      "extended_and_original_coefficient_frames_kept_distinct":True,
      "full_loc_cpl_supplied":False,"full_loc_flat_supplied":False,"full_loc_rho_supplied":False,
      "full_PropagationTheoremGL2_supplied":False,"full_PropagationTheoremGL3_supplied":False,
      "actual_OffFin_producer_supplied":False,"actual_automorphic_or_Alt_producer_supplied":False,
      "full_GdEnd_supplied":False,"full_HostEnd_supplied":False,
      "original_P_retained_at_arithmetic_entry":True,"host_ell_3_allowed":True,"same_g1":True,
      "choice_order":["Fix original frame and supplied Space before all weighted coordinates",
        "Choose one nonzero strict cocycle and base core point before every other core prime",
        "For each original core prime use its actual residue field, then the polynomial line",
        "For finite-point descent retain original c,c1,f and scalar tower, then extend each permitted test DVR compatibly",
        "Extended-frame OffFin implies extended-frame FinPt, then FinPtDown returns original-frame FinPt before AFE20",
        "AFE20 fixes G_L before every later ordinary point; rank-two/rank-three rings and ideals remain separate"],
      "retained_suppliers":retained,"exact_whole_closures":{},"new_global_frontier_leaf_closures":[],
      "selected_producer_closed":False,"root_ledger_modified":False,"no_lean_replay":True}
    dump("contracts.json",contracts)
    keys=["co","weights","space","frame","cone","strict","fpt","wpres","cob","gra","contu","smooth_char","normalize","nonzero","fiber","pt_ex","pt_uniq","pt_mem","line","preconnected","cd","fpd_contract","prop_defs"]
    dump("original_contracts.json",{"schema":"rh-original-contracts/1",**common,
      "contract_keys":keys,"verbatim_source_contracts":{k:texts[k] for k in keys},
      "scope_note":"Generic auxiliary commutative-algebra source files are used in the integer-weight DVR specialization needed for the full original wpres/co_B/gr_A/cont_u endpoints. No full arbitrary-weight-group CoordGrading or general point_loc closure is asserted."})
    dump("provenance.json",{"schema":"rh-human-component-provenance/1",**common,"claims":claims,
      "inherited_human_inputs":human,"classical_and_foundational_inputs":ext,
      "independent_reviews":reviews,"source_proof_is_not_human_proof":True,"root_ledger_modified":False})
    dump("source_manifest.json",{"schema":"rh-pinned-source-manifest/1",**common,
      "source_repository":"https://github.com/CocoSgt/riemann-hypothesis-lean",
      "files":list(files.values()),"ranges":list(sources.values()),"file_count":len(files),"range_count":len(sources)})
    dump("inherited_inputs.json",{"schema":"rh-inherited-proof-bindings/1",**common,"inputs":human})
    dump("retained_foundations.json",{"schema":"rh-retained-foundations/1",**common,
      "inputs":ext,"still_unsupplied_producers":retained})
    dump("classical_inputs.json",{"schema":"rh-classical-input-registry/1",**common,
      "inputs":[e for e in ext if e["kind"].startswith("named_classical")]})
    dump("published_inputs.json",[])
    dump("claim_dag.json",{"schema":"rh-human-claim-dag/1",**common,
      "claims":[{"id":c["id"],"depends_on":c["depends_on"]} for c in claims]})
    dump("closure.json",{"schema":"rh-human-component-closure/1",**common,
      "closed_subcontracts":endpoints,"independent_reviews":reviews,
      "pending_review_claims":sorted(expected-reviewed,key=lambda s:int(s[3:])),
      "exact_whole_closures":{},"new_global_frontier_leaf_closures":[],
      "proposed_global_frontier_leaf_closures":[],
      "full_original_generic_weighted_algebra_and_continuity_closed":True,
      "full_original_preconnected_rank_two_closed":True,"full_original_finPtDown_closed":True,
      "actual_local_completion_flatness_dimensions_and_seed_incidence_remain_open":True,
      "full_PropagationTheoremGL2_remains_open":True,"full_PropagationTheoremGL3_remains_open":True,
      "actual_OffFin_producer_remains_open":True,"full_GdEnd_remains_open":True,
      "full_HostEnd_remains_open":True,"actual_Alt_producers_remain_open":True,
      "original_P_retained":True,"all_IsCD_tests_preserved":True})
    (HERE/"source_excerpts.txt").write_text("\n\n".join(excerpts))
    report="""RANK-TWO CONNECTEDNESS AND FINITE-POINT DESCENT — v0.54

RTC1–RTC25 provide detailed human proofs of the actual rank-two
preconnected core and full original FinPtDown, together with the
upstream generic weighted algebra needed for all original core points.

RTC1–RTC9 prove full original wpres, co_B, gr_A and cont_u for both
allowed ranks. Finite centered-entry coordinates follow from the
universal property and relative cotangent maps. Diagonal twists over
(R/m^N)[[Z]] separate integer weights by the injective Laurent
substitution Y=1+Z, even over nilpotent quotients. Dickson monomial
factorizations prove finite zero-weight generators, finite weight
pieces and the exact fixed-weight filtration comparison. The actual
B, A and gr pieces are identified throughout. No FinA is used.

RTC10–RTC19 prove the original automatic-continuity and strict-cocycle
suppliers, build lower-triangular normalized representations on
arbitrary k-algebras, and realize them by formal-variable deformations.
Only their polynomial entry-algebra image is evaluated in the target.
Arbitrary core residue fields are retained. One nonzero strict cocycle
is chosen first; the generic prime and both specified endpoints of
each polynomial line lie in the actual core. This proves the full
original preconnected_rank_two, without adding Big or modularity.

RTC21–RTC24 construct finite-residue coefficient sections by convergent
Frobenius powers, identify a nonfield equal-characteristic test DVR
with its residue-field power-series ring, and construct a common test
DVR respecting the prescribed embeddings. Exact local continuity,
residual matrices and ordinary characters transport. Injectivity then
descends the characteristic-polynomial identity. Full FinPtDown holds
at every original rank and prime, with every IsCD test/scalar tower.

RTC25 joins ACP11 to FinPtDown and AFE20 on the same original marking.
The extended and original coefficient frames are distinguished and
connected by the proved transport; G_L is chosen before later points.

EXACT BOUNDARY
Actual Space/modularity existence, local completion and chart flatness,
the local representation dictionary, sharp dimensions, closed-point
and seed incidence, the rank-three corner/exceptional ideal, full
rank-specific propagation, OffFin, seeds/classicality and Alt WitA/
WitAQ remain separate. General point_loc and rank-three triangular
realization are not claimed. Original arithmetic P and Host ell=3
are retained. No whole selected obligation or complete human RH/GRH
proof is closed. All v53 and earlier artifacts remain unchanged.
"""
    (HERE/"report.txt").write_text(report+f"\nPin: {PIN}\nMain SHA256: {mainsha}\nStatus: {status}\nClaims: {len(claims)}; source files/ranges: {len(files)}/{len(sources)}\n")
    dump("hashes.json",{"component":HERE.name,"artifact_version":VERSION,
      "hashes":{p.name:sha(p.read_bytes()) for p in sorted(HERE.iterdir()) if p.is_file() and p.name!="hashes.json"}})
    print(json.dumps({"component":HERE.name,"claims":len(claims),"source_files":len(files),
      "source_ranges":len(sources),"main_sha256":mainsha,"status":status},indent=2))

if __name__=="__main__": main()
