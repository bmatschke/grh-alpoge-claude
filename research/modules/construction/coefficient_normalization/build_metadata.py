#!/usr/bin/env python3
"""Portable coefficient-normalization certificates. No Lean replay/build.

python3 build_metadata.py --source /path/to/pinned/checkout \
    --human-root /path/to/reconstruction
"""
from pathlib import Path
import argparse
import hashlib
import json
import re
import subprocess

HERE = Path(__file__).resolve().parent
DEFAULT_HUMAN = HERE.parent if (HERE.parent / "proell_descent").exists() else HERE.parents[1] / "reconstruction_v039"
ap = argparse.ArgumentParser(description=__doc__)
ap.add_argument("--source", type=Path, default=HERE.parents[1] / "lean_source")
ap.add_argument("--human-root", type=Path, default=DEFAULT_HUMAN)
args = ap.parse_args()
SOURCE, HUMAN = args.source.resolve(), args.human_root.resolve()
PIN = "7cbf7a0c32fca1badf05931879a37c3f8a2b03b4"
REPO = "https://github.com/CocoSgt/riemann-hypothesis-lean"
MATHLIB_PIN = "0df444a360eaa60ab8c11dca51a86af692955474"
sha = lambda b: hashlib.sha256(b).hexdigest()
assert subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=SOURCE, text=True).strip() == PIN
decl = re.compile(r"^(?:(?:private|protected|noncomputable|unsafe|scoped)\s+)*(?:def|abbrev|theorem|lemma|structure|class|instance)\s+")
cache, sources = {}, {}

def add(sid, path, anchor, stop=None, role="Exact original definition or source endpoint in the claim's stated scope"):
    path = "src/" + path
    if path not in cache:
        b = (SOURCE / path).read_bytes()
        assert b == subprocess.check_output(["git", "show", PIN + ":" + path], cwd=SOURCE), path
        cache[path] = b, b.decode().splitlines(keepends=True)
    b, lines = cache[path]
    pattern = re.compile(re.escape(anchor.rstrip()) + r"(?=$|[\s:({])")
    hits = [i for i, line in enumerate(lines) if pattern.search(line)]
    assert len(hits) == 1, (sid, path, anchor, hits)
    a = hits[0]
    z = next((i for i in range(a + 1, len(lines))
              if (stop in lines[i] if stop else decl.match(lines[i]))), len(lines))
    while z > a and not lines[z - 1].strip():
        z -= 1
    block = "".join(lines[a:z]).encode()
    sources[sid] = {
        "id":sid, "path":path, "declaration":anchor, "declaration_anchor":anchor,
        "line_start":a+1, "line_end":z, "sha256":sha(b), "file_sha256":sha(b),
        "range_sha256":sha(block), "range_bytes":len(block),
        "first_line":lines[a].rstrip(), "role":role,
        "verified_equal_to_pinned_git_blob":True,
        "url":f"{REPO}/blob/{PIN}/{path}#L{a+1}-L{z}",
    }

A = "Development/AutomorphicArithmetic/AutomorphicVarieties/"
P = A + "PatchingModules/"
BC = P + "PatchingBaseChange/"
TW = P + "ThetaCoefficientMapEq.lean"
PS = P + "PatchedSupportCompletions.lean"
NP = P + "PairedDualFirstOrderDualMatrixSpace.lean"
UD = A + "WeilGroupCharacters/UniversalOrdinaryDeterminantRing.lean"
DET = A + "WeilGroupCharacters/RepAlg.lean"
AM = BC + "AlgebraMapEq.lean"

add("is_co", A+"CommutativeAlgebra/ResMapBijective.lean", "class IsCO")
add("residue_bijective", A+"CommutativeAlgebra/ResMapBijective.lean", "theorem resMap_bijective")
add("source_res", A+"CommutativeAlgebra/ResMapBijective.lean", "def res")
add("is_coef", PS, "class IsCoef")
for sid,anchor in [
    ("original_Pt","structure Pt"),("original_Adapted","def Adapted"),
    ("original_ChainConcl","def ChainConcl"),("original_Core","def Core"),
    ("original_CoreBC","def CoreBC"),("original_Raw","def Raw")]:
    add(sid,PS,anchor)

for sid,anchor in [
    ("actual_Til","def Til"),("actual_C","def C"),
    ("actual_iota","def ι"),("actual_s","def s"),("actual_coeff","def coeff"),
    ("actual_functor","def map"),("actual_lamEmb","def lamEmb"),
    ("actual_RBC","def RBC"),("actual_BaseRel","structure BaseRel")]:
    add(sid,AM,anchor)
for sid,anchor in [
    ("actual_TWGrp","structure TWGrp"),("actual_ProL","def ProL"),
    ("actual_Eig","def Eig"),("actual_B1","def B1"),("actual_B2","def B2"),
    ("actual_q1","def q1El"),("actual_q2","def q2El"),
    ("actual_fEl","def fEl"),("actual_spIdeal","def spIdeal"),
    ("actual_Sp","def Sp"),("actual_Sp_root","def Sp.u"),
    ("actual_delIdeal","def delIdeal"),("actual_pairGens","def pairGens"),
    ("actual_pairVals","def pairVals"),("actual_augIdeal","def augmentationIdealKernel"),
    ("actual_StOrTh","def StOrTh"),("actual_abelian2","abbrev abelian₂"),
    ("actual_Sinf","abbrev Sinf"),("actual_TWBase","structure TWBase"),
    ("actual_SpAt","abbrev SpAt"),("actual_TWRing","structure TWRing"),
    ("actual_TWRing_X","abbrev TWRing.X"),("actual_TWMaps","structure TWMaps"),
    ("actual_TWAut","structure TWAut")]:
    add(sid,TW,anchor)
for sid,anchor in [
    ("actual_NP","structure NP"),("actual_Kap","structure Kap"),
    ("actual_Sel1","def Sel1"),("actual_Bd1","def Bd1"),
    ("actual_Sel2","def Sel2"),("actual_DiscSt","def DiscSt"),
    ("actual_NonSS","def NonSS"),("actual_GenBy","def GenBy")]:
    add(sid,NP,anchor)
for sid,anchor in [
    ("actual_GFrame","structure GFrame"),("actual_eps","def eps"),
    ("actual_starOp","def starOp"),("actual_star","def star"),
    ("actual_oEl","def oEl"),("actual_Resid","structure Resid"),
    ("actual_Dbar","def Dbar"),("actual_Ip","def Ip"),
    ("actual_IsPsi","structure IsPsi"),("actual_Pair","structure Pair"),
    ("actual_Maps","def Pair.Maps")]:
    add(sid,UD,anchor)
for sid,anchor in [
    ("full_GDet","structure GDet"),("full_DetMap","def map"),
    ("actual_chi","def chi"),("actual_lam","def lam"),
    ("actual_generic","def gen"),("actual_CH","def CH"),
    ("actual_cont","def IsCont"),("actual_closure","def closureIdeal")]:
    if sid in ("actual_chi","actual_lam"):
        # These two declarations occur both in Det and GDet; select the latter by a dedicated interval.
        continue
    add(sid,DET,anchor)
# GDet.chi/lam/tr are one contiguous exact source range selected by their unique group-algebra signatures.
add("actual_chi",DET,"def chi (y : MonoidAlgebra A G)")
add("actual_lam",DET,"def lam (i : ℕ) (y : MonoidAlgebra A G)")
add("actual_trace",DET,"def tr (y : MonoidAlgebra A G)")
add("actual_chBar",A+"CommutativeAlgebraHeight/OfDetToDet.lean","def chBar")

for sid,file,anchor in [
    ("oprime","Oprime.lean","theorem UpperTheory.V.Pa.BC.oprime"),
    ("til_co","TilCo.lean","theorem UpperTheory.V.Pa.BC.til_co"),
    ("til_ev","TilEv.lean","theorem UpperTheory.V.Pa.BC.til_ev"),
    ("til_mod","TilMod.lean","theorem UpperTheory.V.Pa.BC.til_mod"),
    ("til_quot","TilQuot.lean","theorem UpperTheory.V.Pa.BC.til_quot"),
    ("til_mvps","TilMvps.lean","theorem UpperTheory.V.Pa.BC.til_mvps"),
    ("til_lam","TilLam.lean","theorem UpperTheory.V.Pa.BC.til_lam"),
    ("sinf_iso","SinfIso.lean","theorem UpperTheory.V.Pa.BC.sinf_iso"),
    ("actual_SinfRel","SinfRel.lean","structure SinfRel"),
    ("actual_RingRel","SinfRel.lean","structure RingRel"),
    ("til_sp","TilSp.lean","theorem UpperTheory.V.Pa.BC.til_sp"),
    ("sp_fin","SpFin.lean","theorem UpperTheory.V.Pa.BC.sp_fin"),
    ("tensor_finite","ExistsFiniteSpanningTaylorWilesTensor.lean","theorem UpperTheory.V.Pa.BC.exists_finite_spanning_taylorWiles_tensor"),
    ("resid_bc","ResidBc.lean","theorem UpperTheory.V.Pa.BC.resid_bc"),
    ("pair_bc","PairBc.lean","theorem UpperTheory.V.Pa.BC.pair_bc"),
    ("star_map","StarMap.lean","theorem UpperTheory.V.Pa.BC.star_map"),
    ("gen_bc","GenBc.lean","theorem UpperTheory.V.Pa.BC.gen_bc"),
    ("base_bc","BaseBc.lean","theorem UpperTheory.V.Pa.BC.base_bc"),
    ("free_bc","FreeBc.lean","theorem UpperTheory.V.Pa.BC.free_bc"),
    ("ring_bc","RingBc.lean","theorem UpperTheory.V.Pa.BC.ring_bc"),
    ("maps_bc","MapsBc.lean","theorem UpperTheory.V.Pa.BC.maps_bc"),
    ("xmaps_bc","XmapsBc.lean","theorem UpperTheory.V.Pa.BC.xmaps_bc"),
    ("quot_bc","QuotBc.lean","theorem UpperTheory.V.Pa.BC.quot_bc"),
    ("tensor_equiv","ExistsSemilinearEquivBaseChangeTensor.lean","theorem UpperTheory.V.Pa.BC.exists_semilinear_equiv_baseChange_tensor"),
    ("aut_bc","AutBc.lean","theorem UpperTheory.V.Pa.BC.aut_bc"),
    ("pt_lift","PtLift.lean","theorem UpperTheory.V.Pa.BC.pt_lift"),
    ("point_const_root","PtLift.lean","private theorem root_const"),
    ("point_surj_card","PtLift.lean","private theorem surj_of_card"),
    ("ps_ev","PsEv.lean","theorem UpperTheory.V.Pa.BC.ps_ev"),
    ("chain_lift","ChainLift.lean","theorem UpperTheory.V.Pa.BC.chain_lift"),
    ("chain_down","ChainLift.lean","private theorem UpperTheory.V.Pa.BC.chain_lift_down"),
    ("chain_tens","ChainTens.lean","theorem UpperTheory.V.Pa.BC.chain_tens"),
    ("til_prime","TilPrime.lean","theorem UpperTheory.V.Pa.BC.til_prime"),
    ("common_field","CommonField.lean","theorem UpperTheory.V.Pa.BC.common_field"),
    ("ss_descend","SsDescend.lean","theorem UpperTheory.V.Pa.BC.ss_descend"),
    ("nonSS_field","NonSSField.lean","theorem UpperTheory.V.Pa.BC.nonSS_field"),
    ("nonSS_mono","NonSSMono.lean","theorem UpperTheory.V.Pa.BC.nonSS_mono"),
    ("grp_quot_bc","GrpQuotBc.lean","theorem UpperTheory.V.Pa.BC.grp_quot_bc"),
    ("discSt_map","DiscStMap.lean","theorem UpperTheory.V.Pa.BC.discSt_map"),
]:
    role="Exact original helper endpoint; only the actual specialization proved in BCN is claimed where the source is more general."
    if sid=="ss_descend":
        role="Original finite-dimensional endpoint; BCN20 proves the stronger scalar-functional descent without that premise."
    if sid=="nonSS_field":
        role="Original three-ring endpoint with finite spanning premise; BCN21 proves the exact needed same-prime coefficient-map transport without that premise."
    add(sid,BC+file,anchor,role=role)
add("g_chmap",A+"CommutativeAlgebraHeight/GChmap.lean","theorem UpperTheory.V.CA.g_chmap")
add("source_closure_bc",BC+"ClosureBc.lean","theorem UpperTheory.V.Pa.BC.closure_bc",
    role="Comparison only: general arbitrary-local-map theorem is not claimed closed. BCN17-B19 independently prove the actual specialized extension identity.")
add("source_pair_mf",BC+"PairMf.lean","theorem UpperTheory.V.Pa.BC.pair_mf",
    role="Not an imported hypothesis; finite-generation route is bypassed in BCN.")
add("source_finE",A+"CommutativeAlgebraHeight/FinE.lean","theorem UpperTheory.V.CA.finE",
    role="Not imported or claimed reconstructed; not needed for the actual coefficient-normalization proof.")
add("source_augmentation_transport",BC+"MemSpanMapE0kerOfPairMaps.lean","theorem UpperTheory.V.Pa.BC.mem_span_map_e0ker_of_pair_maps",
    role="Actual call is supplied by stronger specialized equality BCN19; no full arbitrary-local-map closure is claimed.")
add("source_point_lift",A+"AlgebraTools/CaOverLift.lean","theorem UpperTheory.V.AlgebraTools.exists_lift_ker_eq",
    role="BCN12 independently proves its single-generator actual specialization with the prescribed prime.")
add("source_support",A+"AlgebraTools/CaSuppBc.lean","theorem UpperTheory.V.AlgebraTools.mem_support_baseChange")
add("original_coreBC_proof",P+"AutomorphicDetection/CoreBC.lean","theorem coreBC",
    role="Complete original coefficient-normalization proof; BCN23 reconstructs Core=>CoreBC and BCN24 its selected pointwise restriction.")
add("original_core_producer",P+"AutomorphicDetection/LiftPt.lean","theorem core",
    role="Upstream normalized Core producer remains the antecedent, not proved by this component.")

def blocks(rel,ids,role):
    b=(HUMAN/rel).read_bytes()
    lines=b.splitlines(keepends=True)
    out=[]
    for cid in ids:
        aa=[i for i,x in enumerate(lines) if x.strip()==("% BEGIN "+cid).encode()]
        zz=[i for i,x in enumerate(lines) if x.strip()==("% END "+cid).encode()]
        assert len(aa)==len(zz)==1 and aa[0]<zz[0],(rel,cid)
        a,z=aa[0],zz[0]+1
        block=b"".join(lines[a:z])
        out.append({"id":cid,"line_start":a+1,"line_end":z,"sha256":sha(block),
                    "range_sha256":sha(block),"bytes":len(block)})
    return {"file":rel,"sha256":sha(b),"file_sha256":sha(b),"role":role,"claims":out}

inherited=[blocks("proell_descent/main.tex",
                   ["PQL13","PQL14","PQL15","PQL16","PQL17","PQL18","PQL19","PQL20"],
                   "Only BCN25 uses inherited CoreBC=>Raw and its pointwise invariants; BCN1-B24 have no inherited theorem premise.")]

manifest=(SOURCE/"lake-manifest.json").read_bytes()
assert manifest==subprocess.check_output(["git","show",PIN+":lake-manifest.json"],cwd=SOURCE)
mathlib_item=next(x for x in json.loads(manifest)["packages"] if x["name"]=="mathlib")
assert mathlib_item["rev"]==MATHLIB_PIN
ml=HERE/"mathlib_SimpleModule_Basic.lean"
mb=ml.read_bytes()
assert sha(mb)=="832351437c85db0ce1ef6bcd272169bf3c2f02737e9bda10b914f471c6066b7d"
mlines=mb.splitlines(keepends=True)
assert b"class IsSemisimpleModule" in mlines[64]
assert b"abbrev IsSemisimpleRing" in mlines[72]
external={
    "id":"BCN_PINNED_SEMISIMPLE_DEFINITION",
    "kind":"checked exact dependency definition, not a published theorem application",
    "repository":"https://github.com/leanprover-community/mathlib4",
    "commit":MATHLIB_PIN,
    "path":"Mathlib/RingTheory/SimpleModule/Basic.lean",
    "local_copy":"mathlib_SimpleModule_Basic.lean",
    "url":f"https://raw.githubusercontent.com/leanprover-community/mathlib4/{MATHLIB_PIN}/Mathlib/RingTheory/SimpleModule/Basic.lean",
    "sha256":sha(mb),"file_sha256":sha(mb),"line_start":57,"line_end":73,
    "range_sha256":sha(b"".join(mlines[56:73])),
    "declarations":["IsSemisimpleModule","IsSemisimpleRing"],
    "checked_content":"IsSemisimpleRing E is IsSemisimpleModule E E, a complemented lattice of left submodules. No finite-dimensionality premise.",
    "source_manifest_file":"lake-manifest.json","source_manifest_sha256":sha(manifest),
    "used_by":["BCN20","BCN21"],
}
published={
    "schema":"rh-published-applications/1","component":"coefficient_normalization","version":"0.40",
    "source_commit":PIN,"applications":[],
    "new_published_theorem_imports":0,
    "checked_dependency_definitions":[external],
    "inherited_publication_scope":"BCN25 reuses the already certified PQL13-PQL20 route. Its Chenevier applications remain in the inherited PQL packet; no new application is asserted here.",
    "independent_proof_scope":"BCN1-B24 are elementary/moderate finite-field, complete-ring, module, prime, full-polynomial-law and semisimplicity arguments written in full.",
    "not_imported":["finE","pair_mf","general closure_bc","finite-dimensionality of the closed Cayley-Hamilton quotient"],
}
(HERE/"published_applications.json").write_text(json.dumps(published,indent=2,ensure_ascii=False)+"\n")

titles={
 "BCN1":"One lifted monic polynomial splitting over all equal-cardinality point fields",
 "BCN2":"Complete finite free DVR Oprime with every original clause",
 "BCN3":"Actual Til local ring, completion, residue and literal parameter",
 "BCN4":"Finite presentation and coefficientwise module/quotient transport",
 "BCN5":"Exact weight, auxiliary-variable, delIdeal and splitting-algebra isomorphisms",
 "BCN6":"Finite splitting algebra and actual theta-source module generation",
 "BCN7":"Full residual and Pair base change, adaptedness and dense generation",
 "BCN8":"Original TWBase including finite freeness and every-prime support",
 "BCN9":"Every TWRing with literal module presentation and unchanged arrays",
 "BCN10":"Full TWMaps including ordered annihilator relations and common exponent",
 "BCN11":"Entire original TWAut with literal Unit parameter",
 "BCN12":"Same-field point map with prescribed coefficient-tensor prime kernel",
 "BCN13":"Exact Pt, NP, Kap, B1 and B2 preservation",
 "BCN14":"All finite prime chains under finite free integral extension",
 "BCN15":"Prime extension/contraction through literal formal series",
 "BCN16":"Full polynomial-law Cayley-Hamilton ideal coefficient base change",
 "BCN17":"Finite free closed-ideal transport with cofinal local topologies",
 "BCN18":"Exact formal-series closed ideal via fixed finite group support",
 "BCN19":"Actual augmentationIdealKernel identity without finE",
 "BCN20":"Semisimple-ring descent without finite-dimensionality",
 "BCN21":"Generic same-prime NonSS ascent through a common overfield",
 "BCN22":"DiscSt transport with the same two tuples and StOrTh ascent",
 "BCN23":"Full original Core implies CoreBC for all equal-cardinality finite chains",
 "BCN24":"Selected h=0 full-block g=0 Core implies selected CoreBC pointwise",
 "BCN25":"Composition with inherited proell descent, full and selected Raw",
}
deps={
 "BCN1":[], "BCN2":["BCN1"],"BCN3":["BCN2"],"BCN4":["BCN2","BCN3"],
 "BCN5":["BCN2","BCN4"],"BCN6":["BCN3","BCN4"],
 "BCN7":["BCN2","BCN3"],"BCN8":["BCN4","BCN5","BCN7"],
 "BCN9":["BCN3","BCN4","BCN5","BCN7","BCN8"],
 "BCN10":["BCN4","BCN5","BCN6","BCN8","BCN9"],
 "BCN11":["BCN8","BCN9","BCN10"],"BCN12":["BCN1","BCN2"],
 "BCN13":["BCN7","BCN11","BCN12"],"BCN14":["BCN2","BCN3"],
 "BCN15":["BCN3","BCN4","BCN12"],"BCN16":[],
 "BCN17":["BCN16"],"BCN18":["BCN3","BCN17"],
 "BCN19":["BCN7","BCN16","BCN17","BCN18"],"BCN20":[],
 "BCN21":["BCN19","BCN20"],"BCN22":["BCN7","BCN21"],
 "BCN23":["BCN1","BCN2","BCN3","BCN7","BCN11","BCN12","BCN13","BCN14","BCN15","BCN19","BCN21","BCN22"],
 "BCN24":["BCN1","BCN2","BCN3","BCN7","BCN11","BCN12","BCN13","BCN14","BCN15","BCN19","BCN21","BCN22"],
 "BCN25":["BCN23","BCN24","PQL13","PQL14","PQL15","PQL16","PQL17","PQL18","PQL19","PQL20"],
}
maps={
 "BCN1":["is_coef","oprime","original_CoreBC"],
 "BCN2":["is_coef","oprime"],
 "BCN3":["is_co","residue_bijective","actual_Til","actual_C","actual_iota","actual_s","til_co"],
 "BCN4":["actual_Til","actual_functor","til_ev","til_mod","til_quot"],
 "BCN5":["actual_abelian2","actual_Sinf","actual_lamEmb","actual_delIdeal","actual_spIdeal","actual_Sp","actual_Sp_root","actual_SinfRel","til_lam","til_mvps","sinf_iso","til_sp","til_quot"],
 "BCN6":["actual_Sp","actual_spIdeal","actual_TWMaps","sp_fin","tensor_finite"],
 "BCN7":["actual_GFrame","actual_eps","actual_starOp","actual_star","actual_oEl","actual_Resid","actual_Dbar","actual_Ip","actual_IsPsi","actual_Pair","actual_Maps","actual_RBC","original_Adapted","actual_GenBy","actual_pairVals","full_DetMap","actual_chi","actual_lam","resid_bc","pair_bc","star_map","gen_bc"],
 "BCN8":["actual_TWBase","actual_BaseRel","actual_lamEmb","base_bc","til_mod","source_support"],
 "BCN9":["actual_TWRing","actual_RingRel","actual_SinfRel","actual_delIdeal","ring_bc","free_bc","til_mod"],
 "BCN10":["actual_TWMaps","actual_TWRing_X","actual_q1","actual_q2","actual_fEl","actual_SpAt","maps_bc","xmaps_bc","quot_bc","tensor_equiv","tensor_finite","til_sp"],
 "BCN11":["actual_TWAut","actual_TWBase","actual_TWRing","actual_TWMaps","aut_bc","actual_s"],
 "BCN12":["oprime","pt_lift","point_const_root","point_surj_card","source_point_lift","ps_ev","actual_Til","actual_C","actual_iota","actual_s"],
 "BCN13":["original_Pt","actual_NP","actual_Kap","actual_Eig","actual_B1","actual_B2","actual_Sel1","actual_Bd1","actual_Sel2","actual_Maps","original_Core","pt_lift","original_coreBC_proof"],
 "BCN14":["chain_lift","chain_down","chain_tens","original_ChainConcl"],
 "BCN15":["til_prime","til_quot","pt_lift","original_coreBC_proof"],
 "BCN16":["full_GDet","full_DetMap","actual_generic","actual_CH","actual_chi","g_chmap"],
 "BCN17":["actual_closure","actual_chBar","source_closure_bc","g_chmap"],
 "BCN18":["actual_closure","actual_chBar","actual_Til","actual_coeff","source_closure_bc","source_finE"],
 "BCN19":["actual_pairGens","actual_augIdeal","actual_Ip","actual_starOp","actual_star","actual_oEl","actual_eps","source_augmentation_transport","source_pair_mf","source_finE"],
 "BCN20":["ss_descend","actual_NonSS"],
 "BCN21":["actual_NonSS","common_field","nonSS_field","nonSS_mono","grp_quot_bc","actual_augIdeal"],
 "BCN22":["actual_DiscSt","actual_StOrTh","actual_trace","discSt_map"],
 "BCN23":["original_Core","original_CoreBC","original_ChainConcl","original_Pt","original_Adapted","actual_TWAut","original_coreBC_proof"],
 "BCN24":["original_Core","original_CoreBC","original_ChainConcl","original_Pt","actual_NP","actual_Kap","actual_B1","actual_B2","original_coreBC_proof"],
 "BCN25":["original_Core","original_CoreBC","original_Raw","original_Pt","original_ChainConcl","original_core_producer"],
}
scopes={
 "BCN1":"Every complete coefficient DVR O and one finite O-field K; one monic P then splits over every supplied finite O-field Kprime with the same cardinality, even with a different residue embedding.",
 "BCN2":"Constructs every original oprime output. Same uniformizer, finite free positive rank, local map, complete DVR, residue cardinality, monogenic generator and universal splitting.",
 "BCN3":"Every IsCO(O,R), for the particular constructed unramified Oprime; literal Til=(Oprime tensor_O R)[[s]], with m_A=m_R A, exact residue and local iota.",
 "BCN4":"Finite modules over Noetherian O-algebras, and all finitely generated ideal quotients. No arbitrary infinite tensor-product completeness claim.",
 "BCN5":"Original Empty-to-Unit Lambda and Sinf variable types, original finite delIdeal and every finitely generated Sp relation; exact constants, variables, roots and constant coefficient.",
 "BCN6":"Original finite formal splitting algebra over complete Noetherian local B, with coinciding residual roots allowed; exact theta-range finite spanning of Sp tensor_B M.",
 "BCN7":"Every original residual datum and full Pair; all coefficient algebras of the polynomial law, exact polarization/ordered ordinary/inertia data, same T adaptedness and GenBy.",
 "BCN8":"Every supplied original TWBase and every prime of the new B; same integer D and exact support ideal J extended along iota.",
 "BCN9":"Every original level N and all original TWRing fields; same group map, exponent array, lower inequalities and rank; full scalar-compatible module equivalence.",
 "BCN10":"Every original TWMaps at every level N; all fields including full Pair, all-series coefficient equation, roots, both compositions, ordered q1/q2 and one common ex.",
 "BCN11":"Every supplied empty-parameter TWAut gives actual Unit-parameter TWAut with lambda(X(inl()))=s; no new support or TWAut antecedent is manufactured.",
 "BCN12":"Every original point map f and every prescribed prime of the coefficient tensor ring over ker f; same K[[t]], new Oprime algebra onto K, exact f restriction, s->t and coefficient kernel.",
 "BCN13":"Entire same NP/Kap/eigen data, n,a,g and D+nT.q; B1/B2 constants before every m and original eventual-N sets unchanged.",
 "BCN14":"Every finite h-chain, all prime intermediate e_j, any endpoint prime below a chosen lift; finite-free going down and integral going up in exact orientations.",
 "BCN15":"Every prime Q of the Noetherian coefficient tensor; prime constant-series extension, exact contraction, and containment in selected point kernels.",
 "BCN16":"Every coefficient map, every full GDet and every characteristic, with no n! division. Equality of generated generic coefficient CH ideals.",
 "BCN17":"Finite free local B->A with m_B A subset m_A and m_A^c subset m_B A for one c>0; any topological G and any relation set Z. Exact same-H depth N/cN comparisons.",
 "BCN18":"Actual Noetherian A and T=A[[s]]; extraction at N+r with the same H, then finite generation inside one fixed finite support A[S]. Exact closed ideal equals ordinary extended ideal.",
 "BCN19":"The exact original augmentationIdealKernel of the constructed pair; arbitrary-local-map closure_bc and general finE remain unclaimed.",
 "BCN20":"Any field extension K/kappa and any central kappa-algebra E; no finite-dimensionality or separability. Matches pinned semisimple-ring definition.",
 "BCN21":"Any coefficient map B->S and prime qprime contracting to q; Iprime subset ordinary ideal generated by image I suffices. Actual application has exact equality by BCN19.",
 "BCN22":"Every ideal, same two independent n^2-tuples g,h, full trace-coefficient base change; forward StOrTh at primes.",
 "BCN23":"Full original Core antecedent implies full CoreBC, all original inputs, all h and equal-cardinality points, all chain tests, same J after contraction.",
 "BCN24":"Only a supplied normalized h=0,a=n,Kap.g=0 Core endpoint is needed for the corresponding CoreBC endpoint; selected rank four keeps n=a=4. No arbitrary-h,g Core antecedent.",
 "BCN25":"Composition with inherited PQL20, both full and pointwise selected; upstream normalized Core and initial same-J automorphic data remain supplied.",
}
assert set(titles)==set(deps)==set(maps)==set(scopes)
incoming={c["id"] for f in inherited for c in f["claims"]}
assert all(c in titles or c in incoming for ds in deps.values() for c in ds)
assert all(s in sources for ss in maps.values() for s in ss)
tex=(HERE/"main.tex").read_bytes()
lines=tex.splitlines(keepends=True)
claims=[]
for cid in titles:
    aa=[i for i,x in enumerate(lines) if x.strip()==("% BEGIN "+cid).encode()]
    zz=[i for i,x in enumerate(lines) if x.strip()==("% END "+cid).encode()]
    assert len(aa)==len(zz)==1 and aa[0]<zz[0],cid
    a,z=aa[0],zz[0]+1
    block=b"".join(lines[a:z])
    claims.append({
        "id":cid,"title":titles[cid],"introduced_in":"0.40","classification":"B",
        "status":"complete independent human proof in the stated scope",
        "depends_on":deps[cid],"classical_inputs":[],
        "quantifier_scope":scopes[cid],
        "proof_location":{"file":"coefficient_normalization/main.tex","label":"claim:"+cid,
                          "line_start":a+1,"line_end":z,"sha256":sha(block),
                          "range_sha256":sha(block),"bytes":len(block)},
        "source_ids":maps[cid],"sources":[sources[s] for s in maps[cid]],
        "checked_definition_ids":[external["id"]] if cid in ("BCN20","BCN21") else [],
    })
remaining=[
 {"id":"BCN_NORMALIZED_CORE_ANTECEDENT","classification":"C",
  "status":"retained original antecedent; not an additional normalization premise",
  "contract":"Actual normalized patched rings/maps/modules and support/local-dimension consumer on the same data. The selected h=0,a=n,g=0 consumer suffices for BCN24, so full arbitrary-g,h Core need not be produced for that route.",
  "source_ids":["original_Core","original_core_producer"],
  "not_new_independent_top_level_obligation":True},
 {"id":"BCN_INITIAL_SAME_IDEAL_AUTOMORPHIC_INPUT","classification":"C",
  "status":"retained original upstream arithmetic producer",
  "contract":"Initial TWAut(u,J,Empty,D,T), ordinary/control/type data, four Hida endpoints and same-J support data. The packet transforms the supplied TWAut; it does not produce its original antecedent.",
  "source_ids":["actual_TWAut","original_CoreBC","original_Raw"],
  "not_new_independent_top_level_obligation":True},
]
prov={
 "schema":"rh-human-component-provenance/1","artifact_version":"0.40","date":"2026-11-22",
 "component":"coefficient_normalization","source_commit":PIN,"main_tex_sha256":sha(tex),
 "metadata_builder":{"file":"build_metadata.py","sha256":sha(Path(__file__).read_bytes()),
                     "portable_invocation":"python3 build_metadata.py --source /path/to/pinned/checkout --human-root /path/to/reconstruction"},
 "claims":claims,"source_inventory":list(sources.values()),"baseline_dependencies":inherited,
 "external_definition_inputs":[external],
 "published_applications":{"file":"published_applications.json","sha256":sha((HERE/"published_applications.json").read_bytes()),"certificate_ids":[]},
 "remaining_producer_contracts":remaining,
 "validation":{"source_commit_verified":True,"pinned_blob_verified_files":len(cache),
               "source_ranges":len(sources),"claim_source_occurrences":sum(map(len,maps.values())),
               "all_source_ranges_exact":True,"all_inherited_claim_edges_explicit":True,
               "pinned_mathlib_definition_checked":True,"new_lean_build":False,
               "tex_validation":"See validation/validation.json; offline draft mode, no PDF."},
 "scope_note":"Complete coefficient-normalization implication, including the selected one-point variant, not production of Core or initial TWAut. Specialized closed-ideal equality avoids importing general finE/pair_mf/closure_bc."
}
(HERE/"provenance.json").write_text(json.dumps(prov,indent=2,ensure_ascii=False)+"\n")
closure={
 "schema":"rh-human-component-closure/1","version":"0.40","component":"coefficient_normalization","source_commit":PIN,
 "standing_assumption":"The pinned Alpoge-Claude Lean proof is assumed fully checked and correct. Statuses concern the human reconstruction only.",
 "main_sha256":sha(tex),"main_tex_sha256":sha(tex),"sha256":sha(tex),
 "provenance_sha256":sha((HERE/"provenance.json").read_bytes()),
 "new_claim_ids":list(titles),"claim_count":len(titles),"class_counts":{"A":0,"B":25,"C":0,"D":0},
 "published_application_certificate_ids":[],
 "closed_contracts":[
  {"id":"BCN_ORIGINAL_OPRIME","claims":["BCN1","BCN2"],"classification":"B","status":"complete producer",
   "contract":"Every original oprime field; one extension for all finite O-fields of the same cardinality."},
  {"id":"BCN_ORIGINAL_UNIT_TWAUT","claims":["BCN3","BCN4","BCN5","BCN6","BCN7","BCN8","BCN9","BCN10","BCN11"],
   "classification":"B","status":"complete producer on the supplied original empty-parameter TWAut",
   "contract":"Actual Til, same full residual/pair/module data, literal Unit parameter, same J extended, same T/D/all N/common ex and full TWMaps."},
  {"id":"BCN_SAME_POINT_KERNEL","claims":["BCN12","BCN13","BCN14","BCN15"],"classification":"B","status":"complete producer",
   "contract":"Every point retains K/NP/Kap/eigen/B1/B2 and exact f restriction; Oprime onto K, s maps t and any prescribed prime kernel; full finite-chain and endpoint prime lifting."},
  {"id":"BCN_CLOSED_IDEAL_AND_NONSS","claims":["BCN16","BCN17","BCN18","BCN19","BCN20","BCN21","BCN22"],
   "classification":"B","status":"complete independent algebraic producer",
   "contract":"Finite-free cofinal-topology closure, actual formal-series equality, same-prime NonSS and DiscSt transport, without general finite-dimensional CH finiteness."},
  {"id":"BCN_FULL_CORE_TO_COREBC","claims":["BCN23"],"classification":"B","status":"complete original implication",
   "contract":"Full original Core implies full CoreBC for every h and every equal-cardinality point chain."},
  {"id":"BCN_SELECTED_CORE_TO_COREBC","claims":["BCN24"],"classification":"B","status":"complete selected pointwise implication",
   "contract":"Supplied normalized h=0,a=n,g=0 Core consumer implies corresponding CoreBC without a full arbitrary-chain Core hypothesis; n=a=4 selected specialization exact."},
  {"id":"BCN_CORE_TO_RAW","claims":["BCN25"],"classification":"B","status":"complete composition with inherited PQL",
   "contract":"Full and selected pointwise Core-to-Raw implications; no initial arithmetic producer asserted."}
 ],
 "same_object_sufficient_rule":{
  "full_antecedent":"The original universally quantified Core statement.",
  "selected_antecedent":"Only the original normalized Core conclusion for each supplied h=0,a=n,Kap.g=0 point/data; in the selected rank-four route n=a=4.",
  "other_inputs":"Exactly original CoreBC or Raw inputs, including supplied TWAut, same T and original guards.",
  "quantifier_order":["original l,L,G0,T,n,O,r,B,u,J,D and supplied TWAut","h and full finite point family with equal |K_i|",
                      "one Oprime and Unit packet for the whole family","arbitrary chain/endpoint primes","compatible lifted primes and point maps","normalized Core invocation","contraction to original B,J"],
  "unchanged":["T","n","D","D+n*T.q","every x_i.NP","K_i","Kap","a","g","eigenvalues","B1 and B2 constants/eventual sets","all auxiliary N","common ex"],
  "exact_changes":["Oprime=O[X]/P","Til=(Oprime tensor_O B)[[s]]","Jprime=J.map(iota)","same f after restriction","lambda'(X(inl()))=s","each new f_i'(s)=t_i"],
  "output":"Original ChainConcl for the original B,J and prime kernels; selected variant requires no arbitrary-g,h Core."
 },
 "remaining_inputs":remaining,"selected_top_level_leaf_closed":False,
 "not_claimed":["Construction of initial normalized Core or TWAut","General finE theorem","General pair_mf theorem",
                "Arbitrary-local-map closure_bc theorem","Complete same-J Hida/ordinary/control/type producer","New Lean replay/build"],
 "review_status":"Awaiting independent review at initial metadata build; final external hash-bound review records disposition."
}
(HERE/"closure.json").write_text(json.dumps(closure,indent=2,ensure_ascii=False)+"\n")
loc=["BCN source locators","Pinned source: "+PIN,"All intervals inclusive; file bytes verified against pinned Git blobs.",""]
for cid in titles:
    loc.append(cid+": "+titles[cid])
    for sid in maps[cid]:
        s=sources[sid]
        loc += [f"  {s['path']}:{s['line_start']}-{s['line_end']}  {s['declaration']}",
                "    file_sha256="+s["file_sha256"]+" range_sha256="+s["range_sha256"]]
    loc.append("")
loc += ["Exact pinned mathlib definition: "+external["url"],
        "  local copy "+external["local_copy"]+":57-73 sha256="+external["sha256"],
        "No new published theorem imported; no Lean replay/build."]
(HERE/"source_locators.txt").write_text("\n".join(loc)+"\n")
result={"claims":len(claims),"source_files":len(cache),"source_ranges":len(sources),
        "claim_source_occurrences":sum(map(len,maps.values())),"inherited_blocks":sum(len(x["claims"]) for x in inherited),
        "main_sha256":sha(tex),"provenance_sha256":sha((HERE/"provenance.json").read_bytes()),
        "closure_sha256":sha((HERE/"closure.json").read_bytes()),
        "published_applications_sha256":sha((HERE/"published_applications.json").read_bytes())}
print(json.dumps(result,indent=2))

