#!/usr/bin/env python3
"""Bind APD's human proofs to original contracts; never execute Lean."""
from pathlib import Path
import argparse
import hashlib
import json
import re
import subprocess

HERE=Path(__file__).resolve().parent
ROOT=HERE.parent
PIN="7cbf7a0c32fca1badf05931879a37c3f8a2b03b4"
VERSION="0.56"
V="src/Development/AutomorphicArithmetic/AutomorphicVarieties/"
F=V+"FrobeniusSmoothVectors/"
A=V+"CommutativeAlgebra/"
H=V+"CommutativeAlgebraHeight/"
C=V+"CurveDVRSpecialization/"
T=V+"AlgebraTools/ConnectedPrimeFields/"

SPECS={
 "co":(A+"ResMapBijective.lean",9,75,"Full IsCO and exact residue-map contract"),
 "space":(F+"LeAdicClosure.lean",9,219,"Original NRep, IsBar, IsLift, Space, actual A/B and all named ideals"),
 "loc":(F+"LeAdicClosure.lean",220,259,"Original Loc with the prescribed O', iota, residue and universal property"),
 "frame":(F+"ContinuousCoboundaries2.lean",124,214,"Full original Frame, EC and Ok; original finite-field Euler scope"),
 "cochains":(F+"ContinuousCoboundaries2.lean",11,111,"Exact strict cocycles, boundaries, H1C, coneH0 and coneH2"),
 "cone":(F+"Integral.lean",11,48,"Original IsTr, IsPsi, Integral and all five Cone clauses"),
 "pres_contract":(F+"Integral.lean",50,87,"Original IsResMap, local contraction, Pres and separate EPres record"),
 "box_defs":(F+"PresDefs.lean",9,112,"Original Box, Of, Good and NRep.Univ"),
 "obs_defs":(F+"PresDefs.lean",114,189,"Exact tangent, square-zero map, SetLift, HasObs and IsMinPres"),
 "tan":(F+"TanFinite.lean",1,None,"Full pr_tan, including dual-number cardinality and arbitrary local O"),
 "minimal":(A+"ObsPres.lean",11,305,"Minimal-presentation, relation-detection and tangent-count algebra; APD does not claim full obs_pres"),
 "dualb":(F+"PrDualb.lean",5,None,"Full pr_dualb for every original finite minimal kernel family"),
 "mazur":(F+"PrMazur.lean",8,None,"Full pr_mazur with exact tangent variables and obstruction-dimension relations"),
 "count":(F+"PrCount.lean",5,None,"Full pr_count over arbitrary fields and topological groups"),
 "cl_sub":(H+"ClSub.lean",1,None,"Full cl_sub and residue-constant subalgebra construction"),
 "tri_bar":(F+"PointLoc.lean",42,269,"Broader IsBar triangularity in both ranks and vanishing of mixed weight-zero cycles"),
 "point_loc":(F+"PointLoc.lean",286,349,"Full point_loc for all original IsCL targets and compatible residue maps"),
 "alg_defs":(F+"AlgDefs.lean",9,121,"Actual Laurent subalgebra, HasVertex, vertex ideal, IsVertexRing and IsModel"),
 "vertex":(F+"AlgVertex.lean",5,None,"The actual Cone-to-HasVertex construction"),
 "alg_ft":(F+"SingleMemOfSpan.lean",15,None,"Finite generation of the Laurent subalgebra from entry spans"),
 "homog":(F+"AlgHomog.lean",1,None,"Homogeneous components of every power of the actual vertex ideal"),
 "alg_sep":(F+"AlgSep.lean",6,None,"Separation of the actual vertex ideal, without a global Jacobson hypothesis"),
 "alg_lau":(F+"AlgLau.lean",15,None,"Weighted Laurent representation and full ordinary characters"),
 "alg_cont":(F+"AlgCont.lean",49,None,"Exact quotient-module continuity transported to vertex powers"),
 "alg_model":(F+"AlgModel.lean",26,None,"All original model fields after weighting"),
 "alg_quot":(F+"AlgQuot.lean",16,None,"Every vertex quotient is an original coefficient algebra"),
 "alg_family":(F+"AlgFamily.lean",7,None,"Compatible maps from the supplied Space to all vertex quotients"),
 "alg_closed":(F+"AlgClosed.lean",6,None,"Source coefficient-closedness step; APD uses finite-residue compactness at full alg's actual scope"),
 "alg_limit":(F+"AlgLimit.lean",7,None,"Original recovery of A and B from quotient maps; broader alg_limit is not claimed"),
 "alg":(F+"AlgVring.lean",6,None,"Full original alg, including injective coefficient structure and finite Laurent evaluation"),
 "ext_A":(F+"ExtA.lean",6,None,"Full ext_A with arbitrary Noetherian local, possibly incomplete target"),
 "def_iso":(F+"DefIso.lean",34,None,"Full original def_iso and actual local normalized universality"),
 "box":(F+"ConjVal.lean",8,None,"Explicit semidirect extension and full pr_box"),
 "ofbox":(F+"PrOfbox.lean",7,None,"Full pr_ofbox retaining exact ordered ordinary characters"),
 "sec":(F+"InfPowBot.lean",5,None,"Full pr_sec, arbitrary topological domain, and discrete small kernel"),
 "setlift":(F+"PrSetlift.lean",23,None,"Continuous invertible and upper-triangular set lifts; full pr_setlift"),
 "omk":(F+"LcMatrix.lean",7,None,"Full pr_omk, actual kernel-valued defects and local constancy"),
 "evk":(F+"MapThetaLie.lean",1,None,"Entrywise kernel evaluation and signed adjoint identities"),
 "cocycle":(F+"BorelProjectionIsTwoCocycle.lean",7,None,"Full original global two-cocycle equation"),
 "cocv":(F+"PrCocv.lean",7,None,"Full local cone two-cocycle equation and Borel projection"),
 "sqz":(F+"PrSqz.lean",5,None,"All original pr_sqz exponential and coefficient multiplication identities"),
 "correct":(F+"PrCorrect.lean",6,None,"Full pr_correct with the exact signs of both matrix corrections"),
 "norm1":(F+"PrNorm1.lean",5,None,"Full first normalization over an arbitrary target O-algebra"),
 "norm2":(F+"JconjApply.lean",5,None,"Full second normalization and anti-diagonal symmetry"),
 "norm":(F+"PrNorm.lean",7,None,"Full pr_norm; no surjectivity premise on p"),
 "mu":(F+"PrMu.lean",5,None,"Full original pr_mu for an arbitrary annihilated ideal K"),
 "obs":(F+"ValSubOneMap.lean",8,None,"Full pr_obs with its one-sided quotient-kernel condition and arbitrary p"),
 "tbox":(F+"PrTbox.lean",6,None,"Full strict-cocycle dual-number box"),
 "dof":(F+"ResDual.lean",5,None,"Actual universal dual-number map and derivative identity on all Gamma"),
 "tsurj":(F+"PrTsurj.lean",12,None,"Full original pr_tsurj, with no independent tangent-surjectivity assumption"),
 "tor":(F+"GgMapOfGL.lean",7,None,"Full original weight-torus tangent construction pr_tor"),
 "res":(F+"PrRes.lean",7,None,"Full original pr_res, exact k-to-k' map and the triangular alternative"),
 "good":(F+"PrGood.lean",5,None,"Full original pr_good for all field maps and both allowed ranks"),
 "open":(F+"PrOpen.lean",5,None,"Full pr_open, including arbitrary coefficient residue fields"),
 "bdim":(F+"PrBdim.lean",7,None,"Full pr_bdim for all fields, ranks and change-of-basis matrices"),
 "brig":(F+"PrBrig.lean",6,None,"Full original local Borel rigidity"),
 "bstab":(F+"PrBstab.lean",6,None,"Full local Borel stability over every commutative ring"),
 "cfix":(F+"PrCfix.lean",7,None,"Full signed-involution fixed-space count for every rank, characteristic not two"),
 "dual":(F+"PrDual.lean",5,None,"Full pr_dual including outer weights and the exact sign character"),
 "flag":(F+"ZpowWNe.lean",5,None,"Actual ordinary-flag input from the supplied Space and separating characters"),
 "pres":(F+"HasObs.lean",26,124,"Full original pres on every supplied Loc, both ranks, exact N=N'+n*d+1"),
 "c1ch":(F+"EnnrealVolumeRatioStepCancel.lean",24,51,"Retained full component-chain supplier c1ch and exact dimension threshold"),
 "clcomp":(T+"ClComp.lean",1,None,"Retained actual complete-local component dimension body"),
 "clchain":(T+"ClChain.lean",1,None,"Retained actual complete-local connected-chain body"),
 "sharp2":(F+"ChainedBot.lean",51,86,"Actual rank-two consumer of pres, c1ch and strict triangular dimension"),
 "sharp3":(F+"ChainedOfComap.lean",72,142,"Actual rank-three Sharp consumer, including separate parity presentation"),
 "dim":(F+"KrullDimLtOfNotLeTriangular.lean",36,58,"Retained exact triangular and coincident-character strict dimension bounds"),
 "l51":(F+"CharpolyCoeffsInSubalgebra.lean",50,84,"Retained actual triangular quotient dimension bound"),
 "l52":(F+"TameInertiaCondition.lean",257,280,"Retained actual coincident-character prime dimension bound"),
 "gl2":(C+"ComponentsGoodRankTwo.lean",31,163,"Retained full rank-two propagation, incidence and seeds"),
 "gl3":(C+"PropagationTheoremGL3.lean",30,229,"Retained full rank-three propagation and typed local/global data"),
}

REL={
 1:([],["co","tan","obs_defs"],["ALC1"]),
 2:([1],["minimal","tan","mazur"],[]),
 3:([2],["minimal","dualb","obs_defs"],["ALC7"]),
 4:([2,3],["minimal","mazur"],[]),
 5:([1,2,3,4],["mazur","obs_defs"],[]),
 6:([],["count","cochains"],[]),
 7:([],["cl_sub","co"],[]),
 8:([],["tri_bar","space","frame"],[]),
 9:([],["cone","alg_defs","vertex","alg_ft","homog","alg_sep","alg_lau","alg_cont","alg_model"],["ALC6"]),
10:([7,8,9],["alg","alg_quot","alg_family","alg_closed","alg_limit","point_loc","cone","space"],["ALC6","RTC7"]),
11:([],["ext_A","space"],["RTC7","RTC9"]),
12:([10,11],["def_iso","loc","box_defs"],["ALC11","ALC17"]),
13:([],["box","ofbox","box_defs"],[]),
14:([],["sec","setlift","obs_defs"],["ALC6"]),
15:([14],["omk","evk","cocycle","cocv","cochains","obs_defs"],["ALC6"]),
16:([15],["sqz","correct","obs_defs"],[]),
17:([13,16],["norm1","norm2","norm","box_defs"],[]),
18:([14,15,16,17],["mu","obs","obs_defs","cochains"],[]),
19:([1,13,17,18],["tbox","dof","tsurj","box_defs"],[]),
20:([1,13,19],["tor","good"],[]),
21:([8,13,20],["res","good","flag","box"],["ALC17","ACP3","ACP4"]),
22:([13],["open","bdim","brig","bstab","cfix"],[]),
23:([13],["dual","frame"],[]),
24:([1,6,12,19,20,21,22,23],["pres","frame","count"],["LFC20"]),
25:([5,12,18,21,24],["pres","pres_contract","sharp2","sharp3"],[]),
}

PARENTS={
 "ALC1":("arithmetic_local_charts_v55","Full coefficient-map locality, residue preservation and continuity"),
 "ALC6":("arithmetic_local_charts_v55","Artin–Rees with the exact induced finite-submodule filtration"),
 "ALC7":("arithmetic_local_charts_v55","Exact finite-module completion and quotient completeness"),
 "ALC11":("arithmetic_local_charts_v55","Actual loc_flat, maximality and x over the same mB"),
 "ALC17":("arithmetic_local_charts_v55","Full actual loc_rho continuity, residue and ideal dictionary in both ranks"),
 "RTC7":("rank_two_connectedness_v54","Full upstream wpres, co_B, gr_A, actual degree-zero coefficient ring, without FinA"),
 "RTC9":("rank_two_connectedness_v54","Full actual fixed-weight continuity and cofinal ideal-power filtrations"),
 "ACP3":("arithmetic_component_propagation_v53","Ordered flag over every commutative local ring from the original ordered-product and separator hypotheses"),
 "ACP4":("arithmetic_component_propagation_v53","Literal local characteristic polynomial on actual A, preserved by every coefficient map"),
 "LFC20":("linked_frame_completion_v51","The complete original EC field on the constructed common frame; current pres takes this as part of F.Ok"),
}

SCOPES={
1:"Every local O and every original IsCO O R, arbitrary residue field; finite tangent and actual dual-number bijection",
2:"Every complete Noetherian local O and IsCO O R; exactly tangent-dimension variables, minimal linear coefficients",
3:"Actual relation space and full pr_dualb for every original finite kernel family",
4:"Every nonzero scalar quotient of the actual minimal relation extension; no splitting",
5:"Full pr_mazur at the literal HasObs predicate, with all its quotient quantifiers and exact counts",
6:"Full pr_count for arbitrary fields, arbitrary topological groups and arbitrary local-group index families",
7:"Full cl_sub, in fact without requiring the base O complete/Noetherian; original finite residue-degree premise retained",
8:"Every field-valued IsBar point in ranks two and three, not only diagonal-residual or finite-field points",
9:"Actual full Cone data, both ranks, injective coefficient map, finite Laurent algebra and exact vertex separation",
10:"Full alg and full point_loc at their original coefficient-DVR scopes; compactness only uses the supplied finite residue field",
11:"Full ext_A with any Noetherian local target, no completeness assumption",
12:"Full def_iso and actual NRep.Univ on the same prescribed O', L.R, iota and point x",
13:"Full pr_box and pr_ofbox at arbitrary rank and every commutative coefficient ring/ideal",
14:"Full pr_sec at every topological domain and full pr_setlift at arbitrary local coefficient O",
15:"Full kernel-valued/local-constant global and local defect theorems, arbitrary supplied SetLift and arbitrary p",
16:"Full pr_sqz at only IsSq and full pr_correct at the literal original data; exact signs retained",
17:"Full pr_norm1, pr_norm2 and pr_norm; the first two allow arbitrary target O-algebras with explicit kernel inclusion",
18:"Full pr_mu, pr_obs and actual HasObs; arbitrary quotient killing ker u, not only the minimal scalar quotient",
19:"Full pr_tbox and pr_tsurj at actual universal normalized data; tangent surjectivity is constructed",
20:"Full pr_tor at its arbitrary-rank original hypothesis; the invariant and noninvariant branches both retained",
21:"Full pr_res and pr_good, plus actual local ordered flags and box without new arithmetic hypotheses",
22:"Full Borel dimension/rigidity/stability, signed-involution fixed-space count and open-kernel supplier, each at its literal broad scope",
23:"Full pr_dual for every target field of characteristic ell, both ranks and either triangular orientation; outer weights use the exact sign",
24:"Exact actual tangent-obstruction excess on the same local ring; every finite-module EC premise verified",
25:"Full original HasObs.pres and Loc.Pres for every supplied Loc in rank two or three, no Big or nontriangularity premise",
}

def sha(b): return hashlib.sha256(b).hexdigest()
def dump(name,data): (HERE/name).write_text(json.dumps(data,indent=2,ensure_ascii=False)+"\n")

def inherited(cid):
    comp,scope=PARENTS[cid]
    parent=ROOT/comp/"provenance.json"; raw=parent.read_bytes()
    claim=next(c for c in json.loads(raw)["claims"] if c["id"]==cid)
    loc=claim["proof_location"];body=(ROOT/loc["file"]).read_bytes()
    piece=b"".join(body.splitlines(keepends=True)[loc["line_start"]-1:loc["line_end"]])
    if sha(piece)!=loc.get("sha256",loc.get("proof_range_sha256")): raise ValueError((cid,"inherited proof mismatch"))
    return {"id":cid,"component":comp,"file":loc["file"],"label":"claim:"+cid,
      "file_sha256":sha(body),"line_start":loc["line_start"],"line_end":loc["line_end"],
      "proof_range_sha256":sha(piece),"parent_provenance_file":str(parent.relative_to(ROOT)),
      "exact_parent_provenance_sha256":sha(raw),"scope":scope}

def main():
    ap=argparse.ArgumentParser();ap.add_argument("--repo",type=Path,required=True);args=ap.parse_args()
    repo=args.repo.resolve()
    if subprocess.check_output(["git","-C",str(repo),"rev-parse","HEAD"],text=True).strip()!=PIN:
        raise ValueError("source pin mismatch")
    files={};sources={};texts={};excerpts=[]
    for key,(rel,first,last,decl) in SPECS.items():
        body=subprocess.check_output(["git","-C",str(repo),"show",PIN+":"+rel])
        if body!=(repo/rel).read_bytes(): raise ValueError((rel,"checkout differs"))
        lines=body.splitlines(keepends=True);last=last or len(lines)
        if not 1<=first<=last<=len(lines): raise ValueError((key,"bad range",first,last,len(lines)))
        piece=b"".join(lines[first-1:last]);dst=HERE/"source_snapshot"/rel
        dst.parent.mkdir(parents=True,exist_ok=True);dst.write_bytes(body)
        url="https://github.com/CocoSgt/riemann-hypothesis-lean/blob/"+PIN+"/"+rel
        files[rel]={"path":rel,"snapshot_file":str(dst.relative_to(ROOT)),"sha256":sha(body),
          "bytes":len(body),"line_count":len(lines),"source_commit":PIN,"url":url,
          "verified_equal_to_pinned_git_blob":True}
        sources[key]={"id":"APD_SRC_"+key.upper(),"path":rel,"declaration":decl,
          "line_start":first,"line_end":last,"source_commit":PIN,"file_sha256":sha(body),
          "full_file_sha256":sha(body),"range_sha256":sha(piece),"range_bytes":len(piece),
          "snapshot_file":str(dst.relative_to(ROOT)),"verified_equal_to_pinned_git_blob":True,
          "url":url+f"#L{first}-L{last}"}
        texts[key]=piece.decode();excerpts.append("["+sources[key]["id"]+"] "+decl+"\n"+sources[key]["url"]+"\n"+piece.decode())
    body=(HERE/"main.tex").read_bytes();text=body.decode();mainsha=sha(body)
    blocks={m.group(1):m for m in re.finditer(r"% BEGIN (APD\d+)\n.*?% END \1\n",text,re.S)}
    expected={"APD"+str(i) for i in REL}
    if set(blocks)!=expected: raise ValueError("proof inventory")
    hashes={cid:sha(m.group().encode()) for cid,m in blocks.items()}
    reviews=[]
    for path in sorted(HERE.glob("independent_review*.json")):
        record=json.loads(path.read_text())
        if record.get("result",record.get("status"))!="PASS": continue
        if record.get("proof_file_sha256",record.get("main_sha256",record.get("main_tex_sha256")))!=mainsha:
            raise ValueError((path,"reviewed proof file changed"))
        ids=record.get("claims_reviewed",record.get("reviewed_claims",record.get("claims",[])))
        ids=[c if isinstance(c,str) else c.get("id",c.get("claim")) for c in ids]
        rh=record.get("proof_hashes",{})
        if any(rh.get(cid)!=hashes[cid] for cid in ids): raise ValueError("review block mismatch")
        reviews.append({"file":str(path.relative_to(ROOT)),"sha256":sha(path.read_bytes()),
          "reviewer":record.get("reviewer"),"result":"PASS","proof_file_sha256":mainsha,"claims":ids})
    reviewed={cid for r in reviews for cid in r["claims"]}
    status="complete_at_stated_scope_independently_reviewed" if expected<=reviewed else "complete_at_stated_scope_pending_independent_review"
    common={"artifact_version":VERSION,"component":HERE.name,"source_commit":PIN,
      "proof_file_sha256":mainsha,"status":status}
    claims=[]
    for i,(deps,keys,parents) in REL.items():
        cid="APD"+str(i);m=blocks[cid];first=text[:m.start()].count("\n")+1
        claims.append({"id":cid,"title":m.group().split("\n")[1],"introduced_in":VERSION,
          "classification":"B","depends_on":["APD"+str(j) for j in deps]+parents,
          "external_input_ids":["APD_ORIGINAL_DATA","APD_CLASSICAL_ALGEBRA"] if i>=7 else ["APD_CLASSICAL_ALGEBRA"],
          "sources":[sources[k] for k in keys],"original_scope":SCOPES[i],
          "proof_location":{"file":HERE.name+"/main.tex","label":"claim:"+cid,
            "line_start":first,"line_end":first+m.group().count("\n")-1,"sha256":hashes[cid],"bytes":len(m.group().encode())},
          "status":"complete_at_stated_scope_independently_reviewed" if cid in reviewed else "complete_at_stated_scope_pending_independent_review",
          "independent_review_files":[r["file"] for r in reviews if cid in r["claims"]],
          "source_proof_is_not_human_proof":True})
    human=[inherited(cid) for cid in PARENTS]
    external=[
      {"id":"APD_ORIGINAL_DATA","kind":"original_theorem_antecedent",
       "statement":"Original Frame/Ok, each rank-specific supplied universal Space, and the given Loc with its exact O', R, iota and residue map are retained. General coefficient/matrix lemmas retain only their literal source premises. No new presentation, tangent-surjectivity, obstruction, point_loc or def_iso assumption is introduced.",
       "source_bindings":[sources[k] for k in ["frame","space","loc","box_defs","obs_defs","pres"]]},
      {"id":"APD_CLASSICAL_ALGEBRA","kind":"named_classical_algebra_and_topology",
       "statement":"Nakayama's lemma, Hilbert's basis theorem and its complete finite-variable power-series version, elementary finite-dimensional linear algebra, Krull intersection for Noetherian local rings, and compactness of inverse limits of finite discrete sets. APD proves minimality, relation injection, residue-constant Noetherianity, actual vertex separation by Artin–Rees/determinant trick, all continuous lifts and every deformation correction. Artin–Rees and completion exactness are hash-bound ALC6/ALC7 inputs.",
       "source_bindings":[sources[k] for k in ["minimal","cl_sub","alg_sep","alg_closed","sec"]]},
    ]
    endpoint_specs=[
      ("full_original_pr_tan",1),("minimal_tangent_power_series_presentation",2),
      ("full_original_pr_dualb",3),("minimal_relation_nonsplitting",4),
      ("full_original_pr_mazur",5),("full_original_pr_count",6),
      ("full_original_cl_sub",7),("broad_IsBar_triangularity_both_ranks",8),
      ("actual_separated_Laurent_vertex",9),("full_original_alg",10),("full_original_point_loc",10),
      ("full_original_ext_A",11),("full_original_def_iso",12),("actual_local_NRep_Univ",12),
      ("full_original_pr_box",13),("full_original_pr_ofbox",13),
      ("full_original_pr_sec",14),("full_original_pr_setlift",14),
      ("full_original_pr_omk_and_two_cocycles",15),("full_original_pr_sqz_and_pr_correct",16),
      ("full_original_pr_norm1_pr_norm2_pr_norm",17),("full_original_pr_mu_and_pr_obs",18),
      ("actual_original_HasObs",18),("full_original_pr_tbox_and_pr_tsurj",19),
      ("full_original_pr_tor",20),("full_original_pr_res_and_pr_good",21),
      ("full_original_local_and_infinite_linear_algebra",22),("full_original_pr_dual",23),
      ("actual_tangent_obstruction_excess",24),("full_original_pres",25),
    ]
    endpoints=[{"id":eid,"claim":"APD"+str(i),"scope":SCOPES[i]} for eid,i in endpoint_specs]
    retained=[
      {"id":"APD_COMPONENT_CHAINS","statement":"Full c1ch and its actual ClComp/ClChain bodies remain. APD25 supplies the exact input Pres, including the original threshold; no Chained, sharp2 or sharp3 conclusion is claimed.","source_keys":["c1ch","clcomp","clchain","sharp2","sharp3"]},
      {"id":"APD_DIMENSIONS_AND_PARITY","statement":"Actual l51/l52 triangular and coincident-character bounds, their strict Big comparison, and the independent rank-three EPres record remain. Ordinary Pres is now supplied in both ranks; EPres is not inferred from it.","source_keys":["l51","l52","dim","pres_contract","sharp3"]},
      {"id":"APD_GLOBAL_PROPAGATION","statement":"Global density, homogeneous incidence, seed points, cross-rank corner and full GL2/GL3 propagation, actual OffFin, automorphic seeds and classicality remain. The exact completed local charts are not reopened.","source_keys":["gl2","gl3"]},
      {"id":"APD_ARITHMETIC_AND_ALT_ENTRIES","statement":"Original P/GC.Hypotheses2 at the arithmetic entry, separate rank-two/rank-three spaces, coefficient extensions and modularity ideals, common marking g1, Host ell=3 scope, and Alt WitA/WitAQ remain as previously typed. No whole GdEnd/HostEnd or selected terminal obligation closes.","source_keys":["frame","space","loc","gl2","gl3"]},
    ]
    retained=[{**r,"source_bindings":[sources[k] for k in r["source_keys"]]} for r in retained]
    contracts={"schema":"rh-human-component-contract/1",**common,"closed_subcontracts":endpoints,
      "full_original_pres_supplied":True,"full_pres_supplied":True,
      "actual_local_deformation_presentation_supplied":True,
      "exact_N_equals_Nprime_plus_n_d_plus_one":True,
      "full_original_pr_mazur_supplied":True,"full_original_pr_count_supplied":True,
      "full_original_point_loc_supplied":True,"full_original_alg_supplied":True,
      "full_original_ext_A_supplied":True,"full_original_def_iso_supplied":True,
      "actual_local_NRep_Univ_supplied":True,"actual_original_HasObs_supplied":True,
      "actual_tangent_surjectivity_supplied":True,"actual_small_extension_corrections_supplied":True,
      "all_original_HasObs_quotients_preserved":True,"broad_IsBar_scope_preserved":True,
      "finite_Laurent_polynomial_evaluation_only":True,
      "finite_residue_compactness_only_at_original_alg_scope":True,
      "full_original_general_alg_limit_supplied":False,"full_original_general_alg_closed_supplied":False,
      "full_original_obs_pres_supplied":False,
      "general_local_O_scope_of_deformation_lemmas_preserved":True,
      "same_A_B_x_Oprime_R_iota_preserved":True,"same_g1":True,
      "original_universal_Space_and_Loc_remain_antecedents":True,
      "new_opaque_presentation_or_obstruction_premise_added":False,
      "point_loc_or_def_iso_imported_as_human_proof":False,"upstream_FinA_not_assumed":True,
      "full_original_c1ch_supplied":False,"full_original_EPres_supplied":False,
      "full_sharp2_supplied":False,"full_sharp3_supplied":False,
      "actual_dimensions_density_and_seed_incidence_supplied":False,
      "full_PropagationTheoremGL2_supplied":False,"full_PropagationTheoremGL3_supplied":False,
      "actual_OffFin_producer_supplied":False,"actual_automorphic_or_Alt_producer_supplied":False,
      "full_GdEnd_supplied":False,"full_HostEnd_supplied":False,
      "original_P_retained_at_arithmetic_entry":True,"host_ell_3_allowed":True,
      "rank_two_and_rank_three_rings_and_ideals_kept_distinct":True,
      "choice_order":["Fix original common frame, marking and each supplied rank-specific Space",
        "Fix the original local point and its already supplied O', R, iota and residue map",
        "Prove universality for every later IsCO target without changing this local object",
        "Choose one ordinary box on this object before the family of small extensions",
        "For each small extension choose continuous set lifts and construct its linear obstruction map",
        "Prove the required section for every quotient permitted by the original HasObs predicate",
        "Use the same residual box for tangent counting and Euler comparison, then construct the exact presentation"],
      "retained_suppliers":retained,"exact_whole_closures":{},"new_global_frontier_leaf_closures":[],
      "selected_producer_closed":False,"root_ledger_modified":False,"no_lean_replay":True}
    dump("contracts.json",contracts)
    keys=["co","space","loc","frame","cochains","cone","pres_contract","box_defs","obs_defs",
      "tan","dualb","mazur","count","cl_sub","point_loc","alg","ext_A","def_iso","sec","setlift",
      "norm1","norm2","norm","obs","tsurj","tor","res","good","cfix","dual","pres"]
    dump("original_contracts.json",{"schema":"rh-original-contracts/1",**common,
      "contract_keys":keys,"verbatim_source_contracts":{k:texts[k] for k in keys},
      "scope_note":"Full pres includes actual point_loc/def_iso and the tangent/obstruction bodies. Compactness replaces the source coefficient-closedness proof at full alg's finite-residue arithmetic scope; it does not claim the more general alg_closed/alg_limit statements. No full obs_pres, c1ch, EPres, component/dimension or terminal closure is claimed."})
    dump("provenance.json",{"schema":"rh-human-component-provenance/1",**common,"claims":claims,
      "inherited_human_inputs":human,"classical_and_foundational_inputs":external,
      "independent_reviews":reviews,"source_proof_is_not_human_proof":True,"root_ledger_modified":False})
    dump("source_manifest.json",{"schema":"rh-pinned-source-manifest/1",**common,
      "source_repository":"https://github.com/CocoSgt/riemann-hypothesis-lean",
      "files":list(files.values()),"ranges":list(sources.values()),"file_count":len(files),"range_count":len(sources)})
    dump("inherited_inputs.json",{"schema":"rh-inherited-proof-bindings/1",**common,"inputs":human})
    dump("retained_foundations.json",{"schema":"rh-retained-foundations/1",**common,
      "inputs":external,"still_unsupplied_producers":retained})
    dump("classical_inputs.json",{"schema":"rh-classical-input-registry/1",**common,
      "inputs":[x for x in external if x["kind"].startswith("named_classical")]})
    dump("published_inputs.json",[])
    dump("claim_dag.json",{"schema":"rh-human-claim-dag/1",**common,
      "claims":[{"id":c["id"],"depends_on":c["depends_on"]} for c in claims]})
    dump("closure.json",{"schema":"rh-human-component-closure/1",**common,
      "closed_subcontracts":endpoints,"independent_reviews":reviews,
      "pending_review_claims":sorted(expected-reviewed,key=lambda c:int(c[3:])),
      "exact_whole_closures":{},"new_global_frontier_leaf_closures":[],
      "proposed_global_frontier_leaf_closures":[],
      "full_original_pres_closed":True,"actual_point_loc_and_def_iso_closed":True,
      "actual_tangent_and_obstruction_suppliers_closed":True,
      "full_c1ch_remains_open":True,"full_EPres_remains_open":True,
      "actual_dimensions_density_and_seed_incidence_remain_open":True,
      "full_PropagationTheoremGL2_remains_open":True,"full_PropagationTheoremGL3_remains_open":True,
      "actual_OffFin_producer_remains_open":True,"full_GdEnd_remains_open":True,
      "full_HostEnd_remains_open":True,"actual_Alt_producers_remain_open":True,
      "original_P_retained":True,"separate_rank_rings_and_coefficient_extensions_preserved":True})
    (HERE/"source_excerpts.txt").write_text("\n\n".join(excerpts))
    report="""ARITHMETIC PRESENTATIONS — v0.56

APD1–APD25 are detailed human proofs of full original HasObs.pres:
for every supplied rank-two/rank-three Loc, the actual local ring R
has a surjective O'[[X_1,...,X_N]] presentation whose kernel is generated
by N' listed relations and N = N' + n*d + 1. No Big or nontriangularity
hypothesis is added. All choices retain the same A, B, x, O', R and iota.

APD1–6 prove the full tangent/dual-number statement, minimal presentation,
the relation-space small extension, its scalar nonsplitting argument,
full pr_mazur and full pr_count. The relation bound is proved from the
original HasObs predicate, rather than imported as a theorem certificate.

APD7–12 prove full cl_sub, broad IsBar triangularity in both ranks,
the actual Noetherian separated Laurent vertex algebra, full alg and
point_loc, full ext_A and full def_iso. Compactness is used only for
the finite-residue coefficient algebra present in original alg; it
recovers B inside that coefficient ring. Evaluation t=1 is on finite
Laurent polynomials only. The broader alg_closed/alg_limit statements
are neither imported nor claimed. No diagonal residual premise is
substituted for the original IsBar premise.

APD13–20 construct boxes, continuous lifts across every small extension,
the explicit global/local defects, the signed square-zero corrections,
both normalization matrices, the exact original HasObs map and every
permitted quotient's section, strict tangent surjectivity and the
weight-torus tangent direction. The generic original scopes are kept:
arbitrary local coefficient O, arbitrary rank at the matrix lemmas,
arbitrary topological domain for pr_sec, and no surjectivity of p
where the original does not assume it.

APD21–25 verify the actual residual good/triangular/flag inputs, prove
full local Borel and infinite fixed-space linear algebra, prove the
cyclotomic dual vanishing including outer weights, and apply the
literal frame EC field and strict tangent count. The exact extra +1
is supplied by the weight-torus vector, including its invariant branch.
Padding only the obstruction space and the relation list gives literal
Pres on the original R. Host ell=3 remains permitted throughout.

RETAINED BOUNDARY
Full c1ch/ClComp/ClChain, EPres, sharp2/sharp3, l51/l52 and the strict
dimension comparison, global/seed incidence, cross-rank corner,
full GL2/GL3 propagation and actual OffFin remain. So do automorphic
seeds/classicality, the original P at arithmetic entry, and Alt WitA/
WitAQ. The common marking and separate rank rings/ideals/coefficients
are preserved. No whole selected terminal obligation closes.
All v55 and earlier files are immutable; no Lean replay or PDF.
"""
    (HERE/"report.txt").write_text(report+f"\nPin: {PIN}\nMain SHA256: {mainsha}\nStatus: {status}\nClaims: {len(claims)}; source files/ranges: {len(files)}/{len(sources)}\n")
    dump("hashes.json",{"component":HERE.name,"artifact_version":VERSION,
      "hashes":{p.name:sha(p.read_bytes()) for p in sorted(HERE.iterdir()) if p.is_file() and p.name!="hashes.json"}})
    print(json.dumps({"component":HERE.name,"claims":len(claims),"source_files":len(files),
      "source_ranges":len(sources),"main_sha256":mainsha,"status":status},indent=2))

if __name__=="__main__": main()
