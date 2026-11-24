#!/usr/bin/env python3
"""Bind ALC human proofs to the accepted source and exact original scopes."""
from pathlib import Path
import argparse
import hashlib
import json
import re
import subprocess

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
PIN = "7cbf7a0c32fca1badf05931879a37c3f8a2b03b4"
VERSION = "0.55"
V = "src/Development/AutomorphicArithmetic/AutomorphicVarieties/"
F = V + "FrobeniusSmoothVectors/"
C = V + "CurveDVRSpecialization/"
A = V + "CommutativeAlgebra/"
H = V + "CommutativeAlgebraHeight/"
D = V + "ModularityArgument/ThresholdArguments/DenseThresholdCases/"

SPECS = {
 "co": (A+"ResMapBijective.lean",9,75,"Original IsCO, residue preservation and automatic adic continuity"),
 "space": (F+"LeAdicClosure.lean",9,219,"Original weights, NRep, Space, actual A/B, graded pieces and ideals"),
 "loc": (F+"LeAdicClosure.lean",220,259,"Full original Loc record, prescribed coefficient extension, lies, univ and local representation"),
 "frame": (F+"ContinuousCoboundaries2.lean",124,214,"Original Frame and full Ok fields, including odd characteristic and marked eigenvalue separation"),
 "integral": (F+"Integral.lean",11,103,"Original Integral, IsResMap, local contraction, Pres/EPres, Chained and Sharp"),
 "cpl_def": (H+"IsLocalHom.lean",31,57,"Literal localization-completion Cpl and all four IsCplAt fields"),
 "co_pow": (F+"LocCpl.lean",7,98,"Nilpotent completeness and finite quotient coefficient algebras"),
 "cpl_of_univ": (F+"LocCpl.lean",100,161,"Full original cpl_of_univ over an arbitrary local coefficient ring"),
 "loc_cpl": (F+"LocCpl.lean",162,188,"Full original loc_cpl on O' tensor A and the supplied original extension map"),
 "cpl_is": (H+"CplIs.lean",6,91,"Full original cpl_is for the completion of the localization at a maximal ideal"),
 "cpl_uniq": (H+"CplUniq.lean",9,81,"Full original cpl_uniq, including arbitrary complete target ideal, Cpl equivalence and maximal-ideal extension"),
 "c3a": (H+"HighestWeightSpaceFinite.lean",8,44,"Full original completion flatness and all prime/minimal-prime clauses"),
 "flat_dvr": (F+"LocFlat.lean",9,35,"Finite-residue maximal contraction and flatness of the original unramified DVR map"),
 "loc_flat": (F+"LocFlat.lean",37,69,"Full original loc_flat, including both maximality conclusions"),
 "idem": (F+"AddMulSelfEqOfOrthogonalIdempotents.lean",5,98,"Full original idem and the marked-matrix projector argument"),
 "graph": (F+"IrrOfConn.lean",8,102,"Invariant coordinate spaces and the actual rank-two/rank-three connectivity cases"),
 "types": (F+"IrrOfConn.lean",103,190,"Full original types for every field and every ring map from actual A"),
 "rho_helpers": (F+"LocRho.lean",8,38,"Continuity, entry-span contraction and residual coefficient comparison"),
 "loc_rho": (F+"LocRho.lean",40,66,"Full original loc_rho, every compatible residue map and every ideal"),
 "unr_ex": (F+"ResEqOf.lean",11,48,"Full original finite-residue unramified coefficient extension; ALC constructs the polynomial quotient directly"),
 "cpl_univ": (F+"ResEqOf.lean",50,100,"Full original cpl_univ with a supplied completion and coefficient scalar tower"),
 "cpl_ex": (F+"ResEqOf.lean",102,118,"Full original cpl_ex over an arbitrary local O"),
 "res_fin": (F+"ResEqOf.lean",120,130,"Original finite closed-residue supplier"),
 "loc_ex": (F+"ResEqOf.lean",132,178,"Full original loc_ex at every maximal x over mB in both allowed ranks"),
 "cob": (F+"CoB.lean",8,26,"Inherited RTC7 full co_B and exact maximal ideal"),
 "gra": (F+"IsInternalCongr.lean",81,86,"Inherited RTC7 full gr_A, independent of FinA"),
 "contu": (F+"MemPowSmulLe.lean",14,110,"Inherited RTC9 full cont_u and every adic filtration clause"),
 "chart": (C+"ChartOfFlat.lean",4,None,"Inherited ACP16 full chartOfFlat and its exact prime correspondence"),
 "gl2": (C+"ComponentsGoodRankTwo.lean",31,163,"Actual rank-two local/global consumer and retained sharp/dimension/seed premises"),
 "gl3_local": (C+"PropagationTheoremGL3.lean",30,161,"Actual rank-three local chart, ideal dictionary and existence calls"),
 "gl3_final": (C+"PropagationTheoremGL3.lean",162,229,"Retained rank-three global incidence and final propagation join"),
 "prop_defs": (C+"PropagationTheoremGL2.lean",31,84,"Original propagation, AllGood, OffFin and FinPt predicates"),
 "sharp2": (F+"ChainedBot.lean",51,86,"Retained actual rank-two sharp component-chain producer"),
 "sharp3": (F+"ChainedOfComap.lean",72,142,"Retained actual rank-three Sharp producer and parity branches"),
 "dim": (F+"KrullDimLtOfNotLeTriangular.lean",36,58,"Retained triangular and coincident-character dimension bounds"),
 "jac": (F+"FibreClosed.lean",10,None,"Retained closed-point density and original jac consumer"),
 "min_hom": (F+"MinHom.lean",7,None,"Retained homogeneous minimal-prime comparison"),
 "l41": (F+"MonMemPow.lean",8,None,"Retained nilpotence/power comparison in the actual graded algebra"),
 "seed": (F+"Seedpt.lean",9,30,"Retained seed-prime incidence and dimension comparison"),
 "corner": (F+"QuotientHomNonvanishingBound.lean",221,236,"Retained rank-two/rank-three corner and exceptional ideal"),
 "tworuns": (D+"TwoRuns.lean",80,109,"Actual same-frame two-rank application with separate rings and ideals"),
 "linked": (D+"LinkedEndE.lean",18,67,"Original terminal finite-end join; no Alt witness is supplied by ALC"),
}

# Numbered dependencies, exact source keys, and independently reviewed inputs.
REL = {
 1:([],["co","co_pow"],[]),
 2:([1],["cpl_of_univ","cpl_def"],[]),
 3:([2],["cpl_of_univ","cpl_def"],[]),
 4:([3],["loc","loc_cpl","gra"],["RTC7"]),
 5:([],["cpl_is","cpl_def"],[]),
 6:([],["c3a","cpl_is"],[]),
 7:([6],["c3a","cpl_is"],[]),
 8:([5,7],["c3a","cpl_uniq"],[]),
 9:([8],["c3a"],[]),
10:([],["flat_dvr"],[]),
11:([4,8,10],["loc_flat","loc","cob"],["RTC7"]),
12:([],["types","space","gra"],["RTC7"]),
13:([],["idem","integral","frame","space","cob"],["RTC7"]),
14:([13],["graph","space"],[]),
15:([12,13,14],["types","space"],[]),
16:([11],["rho_helpers","loc_rho","loc","integral","contu"],["RTC7","RTC9"]),
17:([15,16],["loc_rho"],[]),
18:([],["res_fin","gra","cob"],["RTC7"]),
19:([],["unr_ex"],[]),
20:([1,5],["cpl_univ","cpl_ex","cpl_uniq","cpl_def"],[]),
21:([18,19,20],["loc_ex","loc","gra"],["RTC7"]),
22:([9,11,15,16,17,21],["chart","gl2","gl3_local","prop_defs"],["ACP16"]),
}

EXT = {
 "ALC_ORIGINAL_UNIVERSAL_SPACE": {
  "kind":"original_theorem_antecedent",
  "statement":"For the arithmetic statements, the original complete coefficient DVR O with IsCoef, full F.Ok(C0), rank n=2 or n=3, and supplied original universal Space S are fixed. Actual A, B, u, the marking, all ordinary characters and all inclusion maps are preserved. No automorphic existence or modularity supplier is added to these original implications.",
  "source_keys":["space","frame","loc"]},
 "ALC_GENERAL_LOCAL_COEFFICIENT_DATA": {
  "kind":"original_theorem_antecedent",
  "statement":"The general cpl_of_univ/cpl_univ/cpl_ex arguments allow every commutative local O, Noetherian O-algebra D and the exact original IsCO targets and scalar towers. cpl_is/cpl_uniq/c3a are coefficient-independent and retain every original complete ideal-adic target. The arithmetic DVR and finite-residue assumptions are not imposed on these broader statements.",
  "source_keys":["co","cpl_of_univ","cpl_is","cpl_uniq","cpl_univ","cpl_ex","c3a"]},
 "ALC_CLASSICAL_NOETHERIAN_ALGEBRA": {
  "kind":"named_classical_commutative_algebra",
  "statement":"Hilbert's basis theorem and the finite-variable formal power-series Hilbert basis theorem; the finite-ideal flatness criterion and elementary localization/tensor constructions; existence of a prime of a nonzero commutative ring. ALC5 constructs completion, ALC6 proves Artin–Rees from the Rees algebra, ALC7 proves exactness and the tensor comparison, and ALC8–9 prove flatness, prime lifting and all minimal-prime conclusions rather than importing these target suppliers.",
  "source_keys":["cpl_is","cpl_uniq","c3a"]},
 "ALC_CLASSICAL_DVR_AND_FIELD_ALGEBRA": {
  "kind":"named_classical_algebra",
  "statement":"Elementary polynomial division, unique factorization in a polynomial ring over a field, and the uniformizer description of a DVR. ALC18 proves the finite-type field lemma needed for the actual closed residue, and ALC19 proves the finite-field primitive-element argument and constructs the unramified coefficient DVR directly as O[T]/(G), with all coefficient structures and completeness checked.",
  "source_keys":["flat_dvr","res_fin","unr_ex"]},
}
USES = {i:[] for i in REL}
for i in [1,2,3,20]: USES[i]=["ALC_GENERAL_LOCAL_COEFFICIENT_DATA"]
for i in [5,6,7,8,9]: USES[i]=["ALC_CLASSICAL_NOETHERIAN_ALGEBRA"]
for i in [4,11,12,13,14,15,16,17,18,21,22]: USES[i]=["ALC_ORIGINAL_UNIVERSAL_SPACE"]
for i in [10,18,19,21]: USES[i]+=["ALC_CLASSICAL_DVR_AND_FIELD_ALGEBRA"]
USES[4]+=["ALC_CLASSICAL_NOETHERIAN_ALGEBRA"]
USES[20]+=["ALC_CLASSICAL_NOETHERIAN_ALGEBRA"]


def sha(data): return hashlib.sha256(data).hexdigest()
def dump(name,data): (HERE/name).write_text(json.dumps(data,indent=2,ensure_ascii=False)+"\n")


def inherited(cid):
    comp = "rank_two_connectedness_v54" if cid.startswith("RTC") else "arithmetic_component_propagation_v53"
    path=ROOT/comp/"provenance.json"; body=path.read_bytes()
    old=next(x for x in json.loads(body)["claims"] if x["id"]==cid)
    loc=old["proof_location"]; main=(ROOT/loc["file"]).read_bytes()
    block=b"".join(main.splitlines(keepends=True)[loc["line_start"]-1:loc["line_end"]])
    if sha(block)!=loc.get("sha256",loc.get("proof_range_sha256")): raise ValueError(("inherited block",cid))
    scopes={
      "RTC7":"Full original wpres, co_B and gr_A at both allowed ranks, same actual A/B/graded pieces; upstream FinA is not assumed.",
      "RTC9":"Full original cont_u at both allowed ranks, including all matrix and ordinary-character entry maps and every actual ideal-power filtration.",
      "ACP16":"Full original chartOfFlat: actual flat map from a local Noetherian ring, exact contraction of the maximal ideal, and all minimal-prime/chart conclusions at its literal premises.",
    }
    return {"id":cid,"component":comp,"file":loc["file"],"label":"claim:"+cid,
      "file_sha256":sha(main),"line_start":loc["line_start"],"line_end":loc["line_end"],
      "proof_range_sha256":sha(block),"parent_provenance_file":str(path.relative_to(ROOT)),
      "exact_parent_provenance_sha256":sha(body),"scope":scopes[cid]}


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
        sources[key]={"id":"ALC_SRC_"+key.upper(),"path":rel,"declaration":decl,
          "line_start":first,"line_end":last,"source_commit":PIN,"file_sha256":sha(body),
          "full_file_sha256":sha(body),"range_sha256":sha(piece),"range_bytes":len(piece),
          "snapshot_file":str(dst.relative_to(ROOT)),"verified_equal_to_pinned_git_blob":True,
          "url":url+f"#L{first}-L{last}"}
        texts[key]=piece.decode()
        excerpts.append("["+sources[key]["id"]+"] "+decl+"\n"+sources[key]["url"]+"\n"+piece.decode())
    text=(HERE/"main.tex").read_text();mainsha=sha(text.encode())
    blocks={m.group(1):m for m in re.finditer(r"% BEGIN (ALC\d+)\n.*?% END \1\n",text,re.S)}
    expected={"ALC"+str(i) for i in REL}
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
        cid="ALC"+str(i);m=blocks[cid];first=text[:m.start()].count("\n")+1
        claims.append({"id":cid,"title":m.group().split("\n")[1],"introduced_in":VERSION,
          "classification":"B","depends_on":["ALC"+str(j) for j in deps]+parents,
          "external_input_ids":USES[i],"sources":[sources[k] for k in keys],
          "proof_location":{"file":HERE.name+"/main.tex","label":"claim:"+cid,
            "line_start":first,"line_end":first+m.group().count("\n")-1,
            "sha256":proofhash[cid],"bytes":len(m.group().encode())},
          "status":"complete_at_stated_scope_independently_reviewed" if cid in reviewed else "complete_at_stated_scope_pending_independent_review",
          "independent_review_files":[r["file"] for r in reviews if cid in r["claims"]],
          "source_proof_is_not_human_proof":True})
    human=[inherited(cid) for cid in ["RTC7","RTC9","ACP16"]]
    ext=[{"id":eid,**record,"source_bindings":[sources[k] for k in record["source_keys"]]} for eid,record in EXT.items()]
    endpoints=[
      {"id":"full_original_cpl_of_univ","claim":"ALC3","scope":"Every commutative local O, Noetherian O-algebra D, IsCO O R and the exact original residue-compatible universal property; every power, including zero"},
      {"id":"full_original_loc_cpl","claim":"ALC4","scope":"Both original ranks, every supplied Loc and every O'-algebra iota' on O' tensor A agreeing with original iota on 1 tensor A"},
      {"id":"full_original_cpl_is","claim":"ALC5","scope":"Every Noetherian commutative ring and maximal ideal; actual Cpl is the completion of the localization, with all original IsCplAt fields"},
      {"id":"Noetherian_completion_exactness_and_flatness","claim":"ALC8","scope":"Every Noetherian commutative ring and ideal; finite-module exactness/tensor comparison and flatness, with no Jacobson-radical hypothesis"},
      {"id":"full_original_c3a","claim":"ALC9","scope":"Every Noetherian D, maximal y and local R with original IsCplAt; flatness, every prime below y, every prime contraction, all minimal primes and minimal primes over every ideal"},
      {"id":"full_original_loc_flat","claim":"ALC11","scope":"Both original ranks and every supplied Loc, with actual A-to-local-ring map, x maximal and pi(x) maximal; the proof also obtains pi(x)=mB"},
      {"id":"full_original_idem","claim":"ALC13","scope":"Every original IsCO coefficient algebra C, every commutative C-algebra K and Integral O C rho at either allowed rank; coordinate projectors lie in the C-span"},
      {"id":"full_original_types","claim":"ALC15","scope":"Both original ranks, every target field and every ring map from actual A, without a supplied target coefficient-algebra structure; exact irreducibility iff TI and special-fiber triangular dichotomy"},
      {"id":"full_original_loc_rho","claim":"ALC17","scope":"Both original ranks, every supplied Loc, every compatible residue map and every local ideal P; exact continuity, residual matrices/ordinary characters, triP/triM/ee/TI comparisons and triangular endpoint"},
      {"id":"full_original_unr_ex","claim":"ALC19","scope":"Every original coefficient DVR and finite target field with its prescribed O-algebra structure killing mO; finite unramified coefficient DVR and a compatible residue embedding are constructed"},
      {"id":"full_original_cpl_uniq","claim":"ALC20","scope":"Every original Noetherian D, maximal y and IsCplAt target R; every complete ideal-adic target ring T, unique extending map with mR sent into its ideal, actual Cpl equivalence and yR=mR"},
      {"id":"full_original_cpl_univ","claim":"ALC20","scope":"Every commutative local O, original Noetherian D, residue map, supplied IsCplAt completion and exact coefficient scalar tower; all original IsCO targets and unique maps"},
      {"id":"full_original_cpl_ex","claim":"ALC20","scope":"Every commutative local O, Noetherian O-algebra D and O-algebra map D to its residue field; the actual universal IsCO completion is constructed"},
      {"id":"full_original_loc_ex","claim":"ALC21","scope":"Both original ranks and every original maximal ideal x over mB; a single Loc with the complete prescribed record is constructed before all later test objects"},
      {"id":"actual_local_chart_consumer_join","claim":"ALC22","scope":"The exact local chart, representation and all ideal comparisons are returned to the actual rank-two/rank-three propagation definitions; other dimension, incidence, seed and propagation inputs remain"},
    ]
    retained=[
      {"id":"ALC_ACTUAL_SPACE_AND_MODULARITY_REALIZATION","statement":"Original universal Spaces are supplied antecedents of the completed arithmetic implications. Actual automorphic/modularity spaces, ideals, patching and their realization are separate producers.","source_keys":["space","tworuns","linked","prop_defs"]},
      {"id":"ALC_SHARP_COMPONENT_CHAINS_AND_DIMENSIONS","statement":"Actual Pres/EPres producers, sharp2/sharp3 component chains, triangular/coincident-character dimension estimates, and the nice-prime inputs remain. Local completion, local flatness, local representation/type classification and local existence are no longer retained gaps.","source_keys":["integral","sharp2","sharp3","dim","gl2","gl3_local"]},
      {"id":"ALC_GLOBAL_DENSITY_AND_SEED_INCIDENCE","statement":"Closed-point density, homogeneous minimal-prime incidence, the exact graded-power comparison and actual seed-prime dimension comparison remain at their original source scopes. The local chart is already constructed at every closed point to which those results apply.","source_keys":["jac","min_hom","l41","seed","gl2","gl3_final"]},
      {"id":"ALC_RANK_THREE_CORNER_AND_PROPAGATION","statement":"The actual rank-two-to-three corner/exceptional ideal, full rank-two AllGood, full rank-three propagation and actual OffFin remain. Rank-two and rank-three rings and modularity ideals stay separate on the common frame; no independent coefficient extensions are identified.","source_keys":["corner","gl2","gl3_final","tworuns"]},
      {"id":"ALC_AUTOMORPHIC_AND_ALT_PRODUCERS","statement":"Original P at arithmetic entry, automorphic seeds, P1'/P23'/SeedIn, arithmetic-point classicality and the terminal Alt WitA/WitAQ producers remain. FinPtDown was already completed by RTC24 and is not reopened or replaced by an untyped identification.","source_keys":["prop_defs","tworuns","linked"]},
    ]
    retained=[{**r,"source_bindings":[sources[k] for k in r["source_keys"]]} for r in retained]
    contracts={"schema":"rh-human-component-contract/1",**common,"closed_subcontracts":endpoints,
      "full_original_cpl_of_univ_supplied":True,"full_original_cpl_is_supplied":True,
      "full_original_cpl_uniq_supplied":True,"full_original_c3a_supplied":True,
      "full_loc_cpl_supplied":True,"full_loc_flat_supplied":True,"full_loc_rho_supplied":True,
      "full_original_idem_supplied":True,"full_original_types_supplied":True,
      "full_original_unr_ex_supplied":True,"full_original_cpl_univ_supplied":True,
      "full_original_cpl_ex_supplied":True,"full_original_loc_ex_supplied":True,
      "both_allowed_ranks_preserved":True,"arbitrary_field_ring_map_types_scope_preserved":True,
      "all_ideal_comparisons_and_all_compatible_residue_maps_preserved":True,
      "general_local_O_scope_of_completion_suppliers_preserved":True,
      "completion_has_no_added_Jacobson_radical_hypothesis":True,
      "actual_localization_completion_Cpl_identified":True,
      "actual_maps_scalar_towers_and_every_ideal_power_preserved":True,
      "finite_residue_field_only_used_where_originally_supplied":True,
      "unramified_coefficient_extension_constructed_by_monic_polynomial":True,
      "opaque_UnramExtY_imported_as_human_proof":False,"full_general_UnramExtY_supplied":False,
      "full_cone_u_imported_as_human_proof":False,"full_cone_u_supplied":False,
      "rank_two_only_RTC17_used_for_rank_three":False,"upstream_FinA_not_assumed":True,
      "original_universal_Space_remains_a_premise":True,
      "full_sharp2_supplied":False,"full_sharp3_supplied":False,
      "actual_dimensions_density_and_seed_incidence_supplied":False,
      "full_PropagationTheoremGL2_supplied":False,"full_PropagationTheoremGL3_supplied":False,
      "actual_OffFin_producer_supplied":False,"actual_automorphic_or_Alt_producer_supplied":False,
      "full_GdEnd_supplied":False,"full_HostEnd_supplied":False,
      "original_P_retained_at_arithmetic_entry":True,"host_ell_3_allowed":True,"same_g1":True,
      "rank_two_and_rank_three_rings_and_ideals_kept_distinct":True,
      "choice_order":["Fix the original common frame, marking and each supplied rank-specific Space",
        "For a given closed x retain its actual residue field A/x and its prescribed O-algebra structure",
        "Choose the finite unramified O' and compatible residue embedding before forming O' tensor A",
        "Complete at the kernel of that single residue map, retaining the actual inclusion iota",
        "The completed Loc is fixed before every later IsCO test algebra, residue map and local ideal",
        "Use actual contraction through iota for every local/global comparison; do not identify separate rank rings or unrelated coefficient extensions"],
      "retained_suppliers":retained,"exact_whole_closures":{},"new_global_frontier_leaf_closures":[],
      "selected_producer_closed":False,"root_ledger_modified":False,"no_lean_replay":True}
    dump("contracts.json",contracts)
    keys=["co","space","loc","frame","integral","cpl_def","cpl_of_univ","loc_cpl",
          "cpl_is","cpl_uniq","c3a","loc_flat","idem","types","loc_rho","unr_ex",
          "cpl_univ","cpl_ex","loc_ex","chart","prop_defs"]
    dump("original_contracts.json",{"schema":"rh-original-contracts/1",**common,
      "contract_keys":keys,"verbatim_source_contracts":{k:texts[k] for k in keys},
      "scope_note":"All full endpoint flags refer to the original quantified contracts. ALC proves the required completion algebra and actual marked-matrix type classification directly. It does not claim the larger cone_u or general UnramExtY theorem, and it does not replace original Space/Ok or later dimension, seed and propagation premises."})
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
      "full_original_local_completion_flatness_and_representation_closed":True,
      "full_original_arbitrary_field_types_both_ranks_closed":True,
      "full_original_local_existence_closed":True,
      "actual_local_completion_flatness_or_existence_remain_open":False,
      "actual_dimensions_density_and_seed_incidence_remain_open":True,
      "full_PropagationTheoremGL2_remains_open":True,"full_PropagationTheoremGL3_remains_open":True,
      "actual_OffFin_producer_remains_open":True,"full_GdEnd_remains_open":True,
      "full_HostEnd_remains_open":True,"actual_Alt_producers_remain_open":True,
      "original_P_retained":True,"separate_rank_rings_and_coefficient_extensions_preserved":True})
    (HERE/"source_excerpts.txt").write_text("\n\n".join(excerpts))
    report="""ARITHMETIC LOCAL CHARTS — v0.55

ALC1–ALC22 give detailed human proofs of the actual local completion,
flatness, representation/type dictionary and existence producers in
both original ranks. The original universal Space is a supplied
antecedent; its generic algebra and continuity are inherited from
RTC7/RTC9, upstream of FinA.

ALC1–ALC4 recover every finite quotient from the original universal
property and prove full cpl_of_univ and loc_cpl at their literal maps.
The general completion supplier retains arbitrary commutative local O.

ALC5–ALC9 construct Noetherian ideal-adic completion, identify the
original completion of the localization, prove Artin–Rees by the Rees
algebra, prove finite-module exactness and the tensor comparison, and
then prove flatness and every prime/minimal-prime conclusion of c3a.
There is no extra Jacobson-radical hypothesis on the generic ideal.
ALC10–ALC11 prove the DVR coefficient map flat and supply full loc_flat.

ALC12–ALC15 give the complete type classification for every field and
every ring map from the actual A, in ranks two and three. Opposite
weight products prove the special-fiber triangular dichotomy. Explicit
marked-matrix projectors and a finite connectivity argument prove
irreducibility. Rank three uses its actual reflection and odd-entry
conditions, and works at ell=3. Full idem is proved at its original
Integral premise; full cone_u is not imported or claimed.

ALC16–ALC17 prove every local continuity, residual matrix/ordinary
character and ideal comparison, for every compatible residue map and
every local ideal. The result is the full original loc_rho.

ALC18 proves finiteness of each actual closed residue field. ALC19
constructs the finite unramified coefficient DVR as O[T]/(G), checks
its domain, valuation, completeness, maximal ideal and exact residue
embedding, and supplies full unr_ex without importing UnramExtY.
ALC20 proves full cpl_univ/cpl_ex and the coefficient-independent
three-part cpl_uniq. ALC21 constructs the entire Loc record, with the
same tensor residue map and universal property, at every original
maximal x over mB. ALC22 installs these actual maps in the original
rank-two/rank-three chart consumers using reviewed ACP16.

EXACT BOUNDARY
Actual universal/modularity realization, Pres/EPres and sharp component
chains, triangular/coincident dimensions, global density and seed
incidence, the rank-three corner/exceptional ideal, full propagation,
OffFin, automorphic seeds/classicality and Alt WitA/WitAQ remain.
Original P and the common marking are retained. The ranks and their
coefficient extensions are never silently identified. No whole
selected obligation or complete human RH/GRH proof is closed.
All v54 and earlier artifacts remain unchanged. No Lean replay or PDF.
"""
    (HERE/"report.txt").write_text(report+f"\nPin: {PIN}\nMain SHA256: {mainsha}\nStatus: {status}\nClaims: {len(claims)}; source files/ranges: {len(files)}/{len(sources)}\n")
    dump("hashes.json",{"component":HERE.name,"artifact_version":VERSION,
      "hashes":{p.name:sha(p.read_bytes()) for p in sorted(HERE.iterdir()) if p.is_file() and p.name!="hashes.json"}})
    print(json.dumps({"component":HERE.name,"claims":len(claims),"source_files":len(files),
      "source_ranges":len(sources),"main_sha256":mainsha,"status":status},indent=2))


if __name__=="__main__": main()
