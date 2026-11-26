#!/usr/bin/env python3
"""Source-bound v0.41 continuation note and active-contract replacement proposal.

Read-only with respect to all proof packets and released audits. Writes only
next_count_ii_sources.json and count_ii_contract_replacements.json beside this
builder. Pass --source-root and --baseline for a relocated checkout.
"""
from pathlib import Path
import argparse, hashlib, json, subprocess

PIN = "7cbf7a0c32fca1badf05931879a37c3f8a2b03b4"
HERE = Path(__file__).resolve().parent
A = "src/Development/AutomorphicArithmetic/AutomorphicVarieties/"
D = A + "ModularityArgument/ThresholdArguments/DenseThresholdCases/"
H = A + "HeckeAlgebras/"
O = H + "OrdinaryHeckeCharacters/"
P = A + "PatchingModules/"
W = A + "WeilGroupCharacters/"
F = "src/Development/AutomorphicArithmetic/Foundations/GaloisRepresentations/"
I = "src/Development/AbelianVarietyTheory/Proofs/IwasawaDecomposition/"

# Inclusive line ranges. No declaration completion is inferred from a locator.
ANCHORS = [
 ("two_links", D+"LinkTwo.lean", 13,51, "exists_two_links_same_kappa_not_dvd_of_fit_deep"),
 ("outer_tower", D+"PotentialModularityTower.lean",38,66,"PotentialModularityTower; PMExAlt"),
 ("four_hida", D+"PointTheoremBaseObject.lean",26,38,"PointTheoremBaseObject; HidaPropsAlt"),
 ("cohomology", P+"TaylorWilesObstructionBound.lean",23,31,"CohP"),
 ("local_cft", P+"TaylorWilesObstructionBound.lean",115,117,"LocCFT"),
 ("hasaut", P+"TaylorWilesObstructionBound.lean",147,156,"HasAut; PfromAut"),
 ("tw_places", P+"TaylorWilesObstructionBound.lean",88,114,"TWPl"),
 ("fin_neat_free", H+"ContinuousTorusCharacter.lean",162,174,"Frame.FinLevel; Frame.Neat; Frame.Free"),
 ("actual_ord", H+"ContinuousTorusCharacter.lean",222,230,"Frame.Sp; valIn; Ord"),
 ("finite_patching", O+"FuCmpMem.lean",17,35,"fu_patch"),
 ("finU", O+"FuCmpMem.lean",131,195,"UpperTheory.V.Hi.finU"),
 ("classSet_finite", I+"DefiniteUnitaryClassSetFinite.lean",250,293,"DefU.ClassFin.classSet_finite"),
 ("ordAbs", O+"OrdFree.lean",106,245,"UpperTheory.V.Hi.ordAbs"),
 ("ordStruct", O+"OrdFree.lean",295,437,"UpperTheory.V.Hi.ordStruct"),
 ("ordFree", O+"OrdFree.lean",441,481,"UpperTheory.V.Hi.ordFree"),
 ("ordBC", O+"OrdBCMapOrd.lean",198,232,"UpperTheory.V.Hi.ordBC"),
 ("HSet_Ax", H+"CoefficientRepTrivialOnUnramified.lean",122,144,"HSet.Ax"),
 ("actual_Ax", D+"CLocConj.lean",178,237,"dense; UpperTheory.V.Hi.axU_s"),
 ("IsTypeAlt", D+"UnitaryHeckeData.lean",22,27,"IsTypeAlt"),
 ("TypeForAlt", D+"UnitaryHeckeData.lean",38,41,"CaseU.TypeForAlt"),
 ("UnitaryHeckeData", D+"UnitaryHeckeData.lean",59,70,"UnitaryHeckeData; M; IsJ"),
 ("TTypeEx", D+"TTypeEx.lean",18,21,"exists_integral_type_for_residual_rep"),
 ("TypeLoc", O+"TypeLoc.lean",74,158,"UpperTheory.V.Hi.typeLoc"),
 ("type_local", D+"PTypeEx.lean",23,71,"te_unr; te_loc"),
 ("type_tensor", D+"PTypeEx.lean",72,136,"te_root; exists_integral_type_for_residual_rep"),
 ("NonzeroTypes", D+"TypesNZeroFinal.lean",23,35,"cSteps_all_alt; nonzero_types_of_literal_automorphy"),
 ("type_final", D+"TypesNZeroFinal.lean",44,46,"exists_type_for_residual_rep'"),
 ("WtRep", H+"ContinuousTorusCharacter.lean",269,287,"WtRep"),
 ("ctrlOrd", O+"CtrlOrd.lean",220,225,"UpperTheory.V.Hi.ctrlOrd"),
 ("spec", O+"SpecIntIff.lean",100,180,"UpperTheory.V.Hi.spec"),
 ("hiComm", O+"HiComm.lean",218,230,"UpperTheory.V.Hi.hiComm"),
 ("hiAlg", O+"HiAlgUnit.lean",127,170,"UpperTheory.V.Hi.hiAlg"),
 ("automorphic_fibers", D+"AuTeichEx.lean",48,63,"automorphicHeckeSet_unitaryPointProperties_of_typeFor"),
 ("dense_weights", D+"TDenseU.lean",374,457,"isDomain_and_denseWt_of_isTheta"),
 ("separation", D+"TCoreSep.lean",37,66,"eq_zero_of_vanish_at_good_points_dense_weight"),
 ("full_determinant", D+"TCoreDet.lean",291,323,"coreDet_alt"),
 ("same_ideal", D+"ExistsHeckeIdeal.lean",28,84,"absH; exists_hecke_ideal"),
 ("point_properties", D+"UnitaryHeckeData.lean",43,55,"UnitaryPointProperties"),
 ("end1", F+"AdmissibleResidues/ArithmeticPointDecomposition.lean",26,34,"ArithmeticPointDecomposition"),
 ("end2", F+"PlainTorsionPairs/IrrArithPointsAutomorphicAway.lean",56,65,"IrrArithPointsAutomorphicAway; end2oN"),
 ("twist", W+"ArithmeticPointClassicality.lean",103,107,"TwistOk"),
 ("pt_producer", D+"HeckePolyCoeffZero.lean",18,22,"hecke_ideal_point_properties"),
 ("end_producer", D+"JEnd.lean",27,32,"decomposition_and_automorphicAway_of_isJ"),
 ("twist_producer", D+"JTwistA.lean",22,26,"twistOk_of_isJ"),
 ("same_J_Hida", D+"THidaU.lean",38,48,"hida_unitary_of_printed_hida"),
 ("level_contract", D+"PaLevel.lean",24,57,"LevPtAlt; ClassicalAlt; LevelAlt; LocPAlt; HasAutOfAlt"),
 ("level_producer", D+"BaseObjectHomExt.lean",82,135,"s4; level_of_isJ_unitaryHeckeData"),
 ("level_wrapper", D+"TLevelU.lean",19,22,"level_of_is_j_unitary_hecke_data"),
 ("all_level_aut", D+"THasAutOf.lean",19,49,"has_automorphy_of_statement"),
]

COMPONENTS = {
 "neat_levels": ["NTL17"],
 "ordinary_theta_weight": ["OTW12","OTW13"],
 "joint_support": ["JSP2","JSP3","JSP4","JSP5","JSP6","JSP7","JSP8","JSP11","JSP12"],
 "selected_core": ["SCI13"],
 "count_first_order": ["CFO7","CFO20","CFO21"],
 "count_auxiliary_primes": ["CAP13","CAP17"],
 "count_ii_producer": ["CIP4","CIP5"],
 "finite_volume": ["FV1","FV2","FV3","FV4","FV9"],
}
sha = lambda b: hashlib.sha256(b).hexdigest()
read = lambda p: json.loads(p.read_text())
def write(p, x):
    p.write_text(json.dumps(x, ensure_ascii=False, indent=2)+"\n")

def component_binding(root, baseline, name, claims):
    d = root/name
    if not d.is_dir():
        d = baseline/name
    main = (d/"main.tex").read_bytes()
    p = read(d/"provenance.json")
    allclaims = p["claims"]
    if isinstance(allclaims, dict):
        allclaims = list(allclaims.values())
    index = {c["id"]:c for c in allclaims}
    blocks = []
    lines = main.splitlines(keepends=True)
    for cid in claims:
        c = index[cid]
        loc = c.get("proof_location") or c.get("proof")
        a,b = loc["line_start"],loc["line_end"]
        h = sha(b"".join(lines[a-1:b]))
        expected = loc.get("range_sha256") or loc.get("sha256")
        assert h == expected, (cid,h,expected)
        blocks.append(dict(claim=cid,line_start=a,line_end=b,range_sha256=h,
                           file=name+"/main.tex"))
    files = {}
    for fn in ["main.tex","provenance.json","closure.json","published_applications.json"]:
        f=d/fn
        if f.is_file():
            files[fn] = dict(file=name+"/"+fn,sha256=sha(f.read_bytes()))
    return dict(component=name,files=files,proof_blocks=blocks)

def replacements(baseline):
    graphpath=baseline/"dependency_audit_v0_40/obligation_map.json"
    archived_targets=baseline/"history/version_0_40/next_source_targets.json"
    targetpath=archived_targets if archived_targets.is_file() else baseline/"next_source_targets.json"
    dispositionpath=baseline/"dependency_audit_v0_40/target_disposition.json"
    graph=read(graphpath)
    targets=read(targetpath)
    records=read(dispositionpath)["records"]
    nodes={x["id"]:x for x in graph["nodes"]}
    old=nodes["COUNT_II_SUPPORT"]["contract"]
    needle=("Current C producers are earlier: original ordinary/control/separating arithmetic fibers "
            "and type/neatU/TThetaEx; four Hida endpoints on this same J; all-level same-J "
            "TWAut/HasAut on both Links.")
    assert needle in old
    refined=("NTL17 now proves full original neatU for arbitrary integral tau0 and every level. "
             "OTW12 proves one original theta before every K with complete-coefficient IsTheta/IsWt; "
             "OTW13 and CAP17 assemble full UnitaryHeckeData on supplied exact TypeForAlt. "
             "The current producers are full original integral TypeForAlt; actual finite-level/HSet.Ax, "
             "ordinary projector/freeness/base-change/control and separating automorphic arithmetic fibers "
             "on the original Frame/glIwa operators; the four exact Hida endpoints "
             "PointTheoremBaseObject, ArithmeticPointDecomposition, IrrArithPointsAutomorphicAway "
             "and TwistOk on this same J; and actual all-level same-J LevelAlt/TWAut/HasAut on both Links. "
             "The near-term bounded target is finU followed by ordStruct/ordFree and ordBC, independent "
             "of the parallel substantial type construction. HLP's local theta Hecke branch does not "
             "identify the ordinary Frame operators by itself.")
    new=old.replace(needle,refined)
    ordinary=(
      "For each of the two original rank-four Links, fixed iota and ONE common coefficient threshold "
      "before every later coefficient DVR and actual universal B,Lambda, construct the exact integral "
      "TypeForAlt tau0. NTL17 already supplies full neatU; OTW12 supplies ONE theta before EVERY level K "
      "with original IsTheta/IsWt on the complete LamObj ring; CAP17 supplies IsRes and OTW13 assembles "
      "all UnitaryHeckeData fields on that supplied type. Still construct actual H.Ax (including finU "
      "and inverse-Frobenius density), the literal ordinary projector, finite free Ord and MK, exact "
      "coefficient base change and classical control, commuting ordinary Frame/glIwa Hecke operators, "
      "T=TK IsCO, ordinary units and generators, continuous full determinant and ordered characters "
      "satisfying every IsUniv/residual/torsion/inertia relation, and separating Good arithmetic fibers "
      "with the original flags, polarization, tame type, local-global compatibility and auxiliary I0 "
      "condition. Use those SAME R,H,M,T and J=Ann_B(M)=ker(B->T). Nonzero arithmetic assertions are "
      "required only in the nonzero-module branch. Keep ell=3 and the fixed iota; no replacement module, "
      "Hecke algebra, type, character or independently chosen ideal.")
    four=(
      "On the exact J=Ann_B(M)=ker(B->TK), same B,Lambda and fixed iota, prove the original Alt fields: "
      "PointTheoremBaseObject (all original arithmetic points, continuous attached representations, "
      "2<=n<=4, automorphy, I0-triviality, ordinary flags and every pairwise non-cyclotomic relation); "
      "ArithmeticPointDecomposition (full semisimple characteristic-polynomial twist decomposition and, "
      "when all block multiplicities are one, the cofinite strict Frobenius-ratio bound, not an "
      "unasserted exact-purity strengthening); IrrArithPointsAutomorphicAway (AutOffN at actual s.v0 "
      "for every irreducible arithmetic J-point); and TwistOk (all original open-kernel ell-power-order "
      "conjugate-inverse characters, Iu/I0 guards and full determinant/ordered-character twist equations). "
      "The same-J RingProps/Dense conditional transports JSP6-7 are complete, but their actual "
      "ordinary/automorphic suppliers remain. Preserve both rank-four Links, ell=3 and the common "
      "coefficient threshold.")
    hasaut=(
      "With the same original B,J fixed, for EVERY T:TWGrp(globOf(r,V)) and its actual TWPl, construct "
      "TWAut(pairOf(B.u),J,Empty,4[Lplus:Q],T): one base, one residual-eigenvalue lift family, every "
      "TWRing_N and every TWMaps_N with ONE common exponent. The concrete sufficient LevelAlt route "
      "chooses a single TWBase before its later V,h,q,v,w,Bq, then actual LevMod with separating "
      "LevPtAlt fibers, original semilinear/group maps, local IsoSum and WOT for EVERY IsRecT. "
      "Retain the exact LocPAlt/Bernstein-Zelevinsky/geometric-lemma/tame inputs and local level "
      "identities; these are not supplied merely by the names. The source common exponent is n!, "
      "hence 24 at rank four, with no factorial invertibility assumption, so ell=3 is retained. "
      "JSP8 constructs the base on supplied ordinary data; SCI13 closes selected Raw after the full "
      "TWAut and original arithmetic antecedents are supplied. Neither theorem constructs these "
      "higher-level arithmetic modules. Keep fixed iota and both Links under one prior coefficient threshold.")
    subcontracts = {
      "JSP_ORIGINAL_ORDINARY_DATA":ordinary,
      "JSP_FOUR_HIDA_ENDPOINTS":four,
      "JSP_SAME_IDEAL_HASAUT":hasaut,
    }
    joint=read(baseline/"joint_support/closure.json")
    oldsub={x["id"]:x for x in joint["remaining"]}
    subout=[]
    for k,v in subcontracts.items():
        subout.append(dict(id=k,classification="C",status="open_producer",
          original_component_contract=oldsub[k]["contract"],
          original_contract_sha256=sha(oldsub[k]["contract"].encode()),
          replacement_contract=v,
          integration_scope="Current canonical refinement only; keep frozen joint_support/closure.json unchanged."))
    active=[]
    annotation=dict(frontier="COUNT_II_SUPPORT",claims=["NTL17","OTW12","OTW13"],
       closed=("Full original neatU and TThetaEx; conditional full UnitaryHeckeData assembly from exact TypeForAlt."),
       retained=("Actual integral type, original ordinary/control/separating arithmetic data, four exact Hida "
                 "Alt endpoints and all-level same-J HasAut on both rank-four Links. SCI13 selected Raw remains complete."),
       canonical_subcontracts=list(subcontracts),
       guard=("Both rank-four Links; fixed iota; ONE threshold before all later coefficients and universal "
              "B,Lambda; same J within each original ring; ell=3; unchanged CohP/LocCFT/N4 and full support antecedents."))
    for i,(t,r) in enumerate(zip(targets["targets"],records)):
        d=t["version_0_40_disposition"]
        assert d["id"]==r["id"]
        if "COUNT_II_SUPPORT" not in d.get("canonical_count_node_ids",[]):
            continue
        active.append(dict(id=d["id"],original_id=t.get("id"),original_index_one_based=i+1,
          source_file=t["path"],declaration=t["declaration"],
          latest_frozen_selector=f"/targets/{i}/version_0_40_disposition",
          disposition_selector=f"/records/{i}",
          next_scope_update_field="version_0_41_scope_updates",
          append_annotation=annotation,
          preserve_other_scope_components=True))
    assert len(active)==17, len(active)
    work={x["id"]:x for x in graph["work_refinement_nodes"]}
    worknew = [
      dict(id="HIDA_FIELDS",status="open",category="C",
       replacement_contract=("On each actual rank-four Link produce all six original HidaPropsAlt fields on "
         "one J. NTL17/OTW12 close neatness and theta; OTW13 assembles the given-type record. JSP supplies "
         "conditional kernel/RingProps/Dense transports. Full TypeForAlt, actual finite-level ordinary "
         "freeness/base-change/control and separating fibers, and the four exact Alt fields remain; "
         "same-J HasAut is a separate retained producer. Selected Raw is complete by SCI13.")),
      dict(id="P1_CORE_MATCH",status="bypassed_for_selected_route",category="D",
       replacement_contract=("Historical external-literature matching refinement, no longer a mandatory "
         "selected-route task. CIP/CAP/CCH/CFO/LIM/PRG/PMS/CRW/BCN/PQL/SCI reconstruct the required original "
         "selected support implication, including ell=3, from the SAME-J all-level TWAut and unchanged "
         "CohP/LocCFT/N4/determinant/pro-ell antecedents. No independent published P1 theorem is required "
         "for this selected proof. Any stronger or arbitrary-chain literature comparison stays historical/optional; "
         "actual same-J HasAut and the full Count-II arithmetic producer remain open."),
       no_new_logical_gate=True,no_whole_count_ii_closure=True),
      dict(id="P1_CORE_ARITHMETIC_PRODUCER",status="open",category="C",
       replacement_contract=("Supply actual all-level HasAut/TWAut on the SAME original J from the ordinary "
         "Hecke system, together with the unchanged original arithmetic antecedents. The selected h=0, "
         "a=n=4,g=0 Choice/B1/B2, actual limiting/patching construction, normalization, descent and Raw "
         "consumer are complete; their final implication to P1core is supplied by JSP11/SCI13 with "
         "the original point, Kap, B,J,K,f,T and quantifiers. Do not require a new D literature match, "
         "another Raw proof, arbitrary-chain Core, arbitrary-Kap bounds or Sel1=0. Preserve both Links, "
         "ell=3, fixed iota and the common prior coefficient threshold."),
       no_new_logical_gate=True,no_whole_count_ii_closure=True),
    ]
    for x in worknew:
        x["old_contract"]=work[x["id"]]["contract"]
        x["old_status"]=work[x["id"]]["status"]
        x["old_contract_sha256"]=sha(x["old_contract"].encode())
        x["immutable_history_policy"]="Do not edit previous_interface or historical version_0_XX fields/cuts."
    return dict(schema="rh-count-ii-active-replacement-proposal-v1",artifact_version="0.41",
      source_commit=PIN,kind="source-anchored audit proposal; no new proof claim",
      baseline_bindings={str(p.relative_to(baseline)):sha(p.read_bytes())
        for p in [graphpath,targetpath,dispositionpath,baseline/"joint_support/closure.json"]},
      canonical_node=dict(id="COUNT_II_SUPPORT",category="C",status="open_producer",
        old_contract=old,old_contract_sha256=sha(old.encode()),replacement_contract=new),
      current_subcontracts=subout,
      current_work_refinement_replacements=worknew,
      active_target_count=len(active),active_target_replacements=active,
      selected_interface_cut_proposal=dict(key="count_ii_v041",
        newly_closed_nested=["ORIGINAL_NEAT_U","ORIGINAL_TTHETAEX"],
        conditional_assembly="OTW13: full original UnitaryHeckeData from exact TypeForAlt, using CAP17",
        remaining_nested=list(subcontracts),remaining=["COUNT_II_SUPPORT"],
        binding=annotation["guard"],no_logical_edge_change=True),
      historical_policy="Keep all previous-interface snapshots and versioned cuts unchanged; add current v0.41 annotations.",
      assertions=dict(no_new_proof=True,no_new_selected_leaf_closure=True,
        selected_raw_stays_complete=True,ell3_retained=True,two_links_retained=True))

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--source-root",type=Path,default=HERE.parent.parent/"lean_source")
    default_baseline=(HERE.parent if (HERE.parent/"dependency_audit_v0_40").is_dir()
                      else HERE.parent.parent/"reconstruction_v040")
    ap.add_argument("--baseline",type=Path,default=default_baseline)
    args=ap.parse_args()
    source=args.source_root.resolve(); baseline=args.baseline.resolve()
    assert source.is_dir() and baseline.is_dir()
    groups=[]; blobs={}
    for aid,path,a,b,decl in ANCHORS:
        data=(source/path).read_bytes()
        if path not in blobs:
            pinned=subprocess.check_output(["git","show",f"{PIN}:{path}"],cwd=source)
            assert data==pinned, path
            blobs[path]=dict(data=data,blob=subprocess.check_output(
                ["git","rev-parse",f"{PIN}:{path}"],cwd=source,text=True).strip())
        lines=data.splitlines(keepends=True)
        assert 1<=a<=b<=len(lines),(aid,a,b,len(lines))
        block=b"".join(lines[a-1:b])
        groups.append(dict(id=aid,path=path,declaration=decl,declaration_anchor=decl,
          line_start=a,line_end=b,sha256=sha(data),file_sha256=sha(data),
          range_sha256=sha(block),range_bytes=len(block),git_blob_sha=blobs[path]["blob"],
          verified_equal_to_pinned_git_blob=True,
          url=f"https://github.com/CocoSgt/riemann-hypothesis-lean/blob/{PIN}/{path}#L{a}-L{b}"))
    repl=replacements(baseline)
    rp=HERE/"count_ii_contract_replacements.json"
    write(rp,repl)
    components=[component_binding(HERE.parent,baseline,n,c) for n,c in COMPONENTS.items()]
    note=HERE/"next_count_ii.txt"
    manifest=dict(schema="rh-source-anchored-continuation-note-v2",artifact_version="0.41",
      source_commit=PIN,formal_correctness_assumed=True,no_lean_replay=True,
      note_file=note.name,note_sha256=sha(note.read_bytes()),
      note_word_count=len(note.read_text().split()),kind="work plan and current-contract audit; not proof",
      metadata_builder=dict(file=Path(__file__).name,sha256=sha(Path(__file__).read_bytes())),
      active_contract_replacements=dict(file=rp.name,sha256=sha(rp.read_bytes())),
      source_ranges=groups,source_file_count=len(blobs),source_range_count=len(groups),
      component_bindings=components,
      proposed_first_target="Exact FuCmpMem.finU then OrdFree.ordStruct/ordFree and OrdBCMapOrd.ordBC on the original Frame.",
      retained_parallel_type="Full original TypeForAlt; finite TypeLoc descent does not supply NonzeroTypes/typeConj/IsRecT.",
      no_new_published_application=True,no_new_proof_claim=True,no_whole_leaf_closure=True)
    out=HERE/"next_count_ii_sources.json"
    write(out,manifest)
    print(json.dumps(dict(note_sha256=manifest["note_sha256"],manifest_sha256=sha(out.read_bytes()),
        replacements_sha256=sha(rp.read_bytes()),words=manifest["note_word_count"],
        ranges=len(groups),files=len(blobs),components=len(components),
        active_targets=repl["active_target_count"]),indent=2))
if __name__=="__main__":
    main()
