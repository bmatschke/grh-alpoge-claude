#!/usr/bin/env python3
"""Portable RPI source/proof certificate builder. Does not run Lean.

python3 build_metadata.py --source /path/to/pinned/checkout \
    --human-root /path/to/reconstruction

Every source file is compared byte-for-byte with the pinned Git blob.
Line intervals are inclusive and hashes retain original newline bytes.
"""
from pathlib import Path
import argparse
import hashlib
import json
import re
import subprocess

HERE = Path(__file__).resolve().parent
DEFAULT_HUMAN = HERE.parent if (HERE.parent / "finite_volume").exists() else HERE.parents[1] / "reconstruction_v038"
ap = argparse.ArgumentParser(description=__doc__)
ap.add_argument("--source", type=Path, default=HERE.parents[1] / "lean_source")
ap.add_argument("--human-root", type=Path, default=DEFAULT_HUMAN)
args = ap.parse_args()
SOURCE, HUMAN = args.source.resolve(), args.human_root.resolve()
PIN = "7cbf7a0c32fca1badf05931879a37c3f8a2b03b4"
REPO = "https://github.com/CocoSgt/riemann-hypothesis-lean"
sha = lambda b: hashlib.sha256(b).hexdigest()
assert subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=SOURCE, text=True).strip() == PIN
decl = re.compile(r"^(?:(?:private|protected|noncomputable|unsafe|scoped)\s+)*(?:def|abbrev|theorem|lemma|structure|class|instance)\s+")
cache, sources = {}, {}


def add(sid, path, anchor, stop=None, role="Exact original definition or source endpoint, in the stated scope"):
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
        "id": sid, "path": path, "declaration": anchor, "declaration_anchor": anchor,
        "line_start": a + 1, "line_end": z, "sha256": sha(b), "file_sha256": sha(b),
        "range_sha256": sha(block), "range_bytes": len(block),
        "first_line": lines[a].rstrip(), "role": role,
        "verified_equal_to_pinned_git_blob": True,
        "url": f"{REPO}/blob/{PIN}/{path}#L{a + 1}-L{z}",
    }


D = "Development/AbelianVarietyTheory/"
IW = D + "Proofs/IwasawaDecomposition/"
BT = "Formalism/LocalToGlobal/BesselHermitianTheta/"
IR = "Formalism/LocalToGlobal/IndefiniteReal/"
DIV = "Formalism/LocalToGlobal/Divisibility/"
HT = D + "Proofs/HeightProofs/"
AUT = BT + "IsAutFunDef.lean"
SM = BT + "TiedSmooth.lean"
MULT = IR + "ScalarOnPartsFull.lean"
LEVEL = IR + "SubgroupCharExtensionOneApply.lean"
READ = D + "Definitions/AutomorphicMembership/StableIffCarrierEq.lean"
DECAY = D + "PublishedTheorems/AutomorphicForms₂/ExistsNormLeHeightPow.lean"

for sid, anchor in [
    ("actual_group", "abbrev GA"), ("actual_matrix", "def matHom"),
    ("rational_group", "def GQ"), ("finite_factor", "def GfC"),
    ("infinite_factor", "def GinfC"), ("actual_inf_family", "def IsInfFam"),
    ("actual_automorphic", "structure IsAutFun"), ("actual_right_translate", "def rTr"),
    ("isotropic_frame", "def IsIsoFrame"), ("actual_NI", "def NI"),
    ("actual_NIQ", "def NIQ"), ("actual_cusp", "def IsCuspFun"),
]:
    add(sid, AUT, anchor)
for sid, anchor in [
    ("actual_atTau", "def atTau"), ("actual_lieAt", "def lieAt"),
    ("actual_oneP", "def oneP"), ("actual_Rder", "def Rder"),
    ("actual_RderC", "def RderC"), ("actual_gelf", "def gelf"),
    ("actual_normInf", "def normInf"), ("actual_smooth_growth", "structure IsAutFunSm"),
]:
    add(sid, SM, anchor)
for sid, anchor in [
    ("actual_DSModel", "structure DSModel"), ("actual_model_rep", "def DSModel.rep"),
    ("actual_model_smooth", "def DSModel.sm"), ("actual_tuple", "abbrev DSModel.Vec"),
    ("actual_MMap", "abbrev MMap"), ("actual_mult_clauses", "structure IsMultMap"),
    ("actual_Mult_span", "def Mult"), ("actual_IsMultIP", "def IsMultIP"),
    ("actual_ipM_choice", "def ipM"), ("actual_postOn", "def postOn"),
    ("actual_goodPart", "def goodPart"),
]:
    add(sid, MULT, anchor)
for sid, anchor in [
    ("actual_flagL", "def flagL"), ("actual_flag1L", "def flag1L"),
    ("actual_level_group", "def levG"), ("actual_level_character", "def levChi"),
    ("actual_lift", "def IsLevelLift"), ("actual_finite_action", "def actG0"),
    ("actual_meas_lev", "def IsMeasLevW"), ("actual_meas_domain", "def IsMeasFD"),
]:
    add(sid, LEVEL, anchor)
for sid, anchor in [
    ("actual_linear_action", "def actL"), ("actual_gaL", "def gaL"),
    ("actual_real_data", "structure RealDat"), ("actual_nP", "def nP"),
]:
    add(sid, IR + "LinksDefs.lean", anchor)
for sid, anchor in [
    ("actual_models_inf", "abbrev models_inf"), ("actual_models_nu0", "abbrev models_ν0"),
    ("actual_IsModels", "structure IsModels"), ("actual_nonzero_chain", "structure IsItW"),
]:
    add(sid, IR + "LinksChar.lean", anchor)
for sid, anchor in [
    ("original_Pins", "structure Pins"), ("original_Holds", "structure Holds"),
    ("original_Read", "structure Read"), ("original_ReadL", "structure ReadL"),
    ("original_ReadC", "structure ReadC"), ("original_columns", "def colOf"),
    ("original_ids", "def idsOf"),
]:
    add(sid, READ, anchor)
for sid, anchor in [
    ("original_ext1", "def ext1"), ("original_full_level", "def full"),
    ("original_levFn", "def levFn"),
]:
    add(sid, DIV + "DefGroup.lean", anchor)
add("residue_unit_norm", D + "Proofs/TwistedOperators/NormLevChiFlagLEqOne.lean", "theorem norm_residueChar_eq_one")
add("flag_character_norm", D + "Proofs/TwistedOperators/NormLevChiFlagLEqOne.lean", "theorem norm_levChi_flagL_eq_one")
add("original_RowProj", IW + "GoodProjectorSmallestSpaceForms.lean", "def RowProj")
add("original_row_producer", IW + "RowProjHolds.lean", "theorem rowProj_holds")
add("original_translate_integral", IW + "IsLiftFlagGroupInv.lean", "theorem integral_act")
add("original_projector_ipM", IW + "IsLiftFlagGroupInv.lean", "theorem ipM_gaL",
    role="Source consumer. RPI uses DI11-DI12's reconstructed finite-adjoint argument, not its unexpanded SchurMult producer.")
add("original_nP_positive", D + "Proofs/TwistedOperators/ExistsVecOfNe.lean", "theorem nP_pos'")
add("first_DivDef3", DIV + "DivisionCompatibleToSub2Indef2.lean", "structure DivDef3")
add("separate_DivRows3", DIV + "DivisionCompatibleToSub2Indef2.lean", "structure DivRows3",
    role="Separate stronger second output, expressly not closed by RPI.")
add("original_division", IW + "DivisionCompatibleAtReadIdentifications.lean", "theorem GlobalTheory.divTied3_read",
    role="RPI15 closes its first-output implication by discharging DI's additional RowPairInt; original common premises remain.")
add("original_division_wrapper", IW + "DivisionCompatibleAtReadIdentificationsStatement.lean",
    "theorem _root_.GlobalTheory.T.divisionCompatible_at_readIdentifications",
    role="Combined source theorem; only its first DivDef3 output is claimed.")
for sid, anchor in [
    ("source_bounded_endpoint", "theorem bounded_of_cuspForm"),
    ("source_pair_endpoint", "theorem integrableOn_star_mul"),
    ("separate_global_rapid_decay", "def CuspRapidDecay"),
    ("separate_quotient_height", "def quotHeight"),
]:
    add(sid, DECAY, anchor,
        role="Original bounded/pair endpoint or explicitly separate stronger global-height predicate; no unproved source implication is imported.")
add("separate_global_growth_conversion", HT + "ExistsSigmaList.lean", "theorem growth_iff",
    role="Not used; its polynomial global-height conversion remains unclaimed.")
add("separate_polynomial_reduction", HT + "ExistsSigmaList.lean", "theorem reduction",
    role="Not used; no new reconstruction of this stronger quantitative adelic reduction is asserted.")
add("actual_finite_volume_contract", D + "Definitions/Foundations/CdScaleTieIff.lean", "def FiniteVolume₂")
add("actual_finite_classes", IW + "FiniteClassSetHermitianUnitaryOpenLevel.lean", "theorem exists_finset_classes",
    role="Inherited FV9 supplies this universal qualitative original endpoint.")
add("actual_finite_volume", IW + "FiniteVolumeAdelicUnitaryQuotient.lean", "theorem finVol",
    role="Inherited FV8 supplies finite volume for every original Haar/fundamental domain.")


def blocks(rel, ids, role):
    b = (HUMAN / rel).read_bytes()
    lines = b.splitlines(keepends=True)
    out = []
    for cid in ids:
        aa = [i for i, line in enumerate(lines) if line.strip() == ("% BEGIN " + cid).encode()]
        zz = [i for i, line in enumerate(lines) if line.strip() == ("% END " + cid).encode()]
        assert len(aa) == len(zz) == 1 and aa[0] < zz[0], (rel, cid)
        a, z = aa[0], zz[0] + 1
        b0 = b"".join(lines[a:z])
        out.append({"id": cid, "line_start": a + 1, "line_end": z,
                    "sha256": sha(b0), "range_sha256": sha(b0), "bytes": len(b0)})
    return {"file": rel, "sha256": sha(b), "file_sha256": sha(b), "role": role, "claims": out}


inherited = [
    blocks("finite_volume/main.tex", ["FV1","FV2","FV3","FV4","FV6","FV8","FV9","FV10"],
           "Exact actual algebraic/adelic group, measurable sections, every original finite-volume domain, finite open-level classes and real arithmetic components."),
    blocks("seed_boundedness/main.tex", ["SBD1","SBD5","SBD6","SBD10"],
           "Only generic smooth derivative/norm comparison, additive finite approximation, and arithmetic unipotent compactness are used. The special-seed ZCusp/central-finiteness/rapid-decay conclusions are not substituted."),
    blocks("constant_terms/main.tex", ["CTC11"],
           "Exact original NI Witt matrices, algebraic closure, rational subgroup and compact adelic quotient."),
    blocks("regular_quotient/main.tex", ["RQC4"],
           "Same original Haar/fundamental-domain right-translation identity used only in final finite-adjoint consumer."),
    blocks("division_identity/main.tex", ["DI10","DI11","DI12","DI13","DI14","DI15","DI16","DI17","DI18","DI19","DI20","DI21"],
           "Previously reconstructed first-output consumer is invoked only after the independent RPI14 row producer. RPI1-RPI14 do not use a DI implication requiring RowPairInt."),
]

milne = {
    "author": "J. S. Milne",
    "title": "Algebraic Groups: The Theory of Group Schemes of Finite Type over a Field",
    "year": 2017,
    "url": "https://www.jmilne.org/math/Books/iAG2017.pdf",
    "primary_source_verified": True,
}
ms = {
    "authors": ["Stephen D. Miller","Wilfried Schmid"],
    "title": "On the rapid decay of cuspidal automorphic forms",
    "publication": "Advances in Mathematics 231 (2012), 940-964",
    "doi": "10.1016/j.aim.2012.06.001",
    "version_inspected": "Author preprint arXiv:1106.2149v1, 10 June 2011; the unversioned PDF URL serves this version.",
    "url": "https://arxiv.org/pdf/1106.2149",
    "primary_source_verified": True,
}
applications = [
    {
        "id": "RPI_COCHARACTER_PARABOLICS", "classification": "A", "status": "checked published application",
        "publication": milne, "locators": [
            {"theorem":"Theorem 25.1","printed_page":544,"pdf_page_zero_based":555},
            {"theorem":"Proposition 17.60","printed_page":372,"pdf_page_zero_based":383}],
        "consumer_claims": ["RPI2","RPI5","RPI8"],
        "matched_hypotheses": [
            {"hypothesis":"Reductive group over the indicated field","actual_object":"U(J) over F in RPI2; Res_(F/Q) U(J) over Q in RPI5/RPI8","verification":"FV1-FV4 and FV10 give the exact smooth connected reductive groups, not only abstract isomorphic groups."},
            {"hypothesis":"Cocharacter defined over that same field","actual_object":"Weights (+1,0,-1) on the rational Witt decomposition; arbitrary Q cocharacter supplied for P; integral multiple of the rational simple-root dual","verification":"RPI2/RPI5/RPI8 construct or retain precisely these cocharacters; restriction-of-scalars adjunction is explicit."},
            {"hypothesis":"Parabolic defined over the same field for the converse","actual_object":"Every proper Q-parabolic in the real cusp test","verification":"Universal original real cusp target; no splitness assumption on U(J)."}],
        "output":"P=P(lambda) and Ru(P(lambda)) is the subgroup contracted to identity. Actual NI identification and inclusion are independently proved.",
        "all_hypotheses_checked": True,
    },
    {
        "id": "RPI_RELATIVE_ROOT_SETUP", "classification": "A", "status": "checked published application",
        "publication": milne,
        "locators":[{"statement":"25.16-25.17 and 25.22","printed_pages":"549-550","pdf_pages_zero_based":[560,561]}],
        "additional_primary_description":{"publication":ms,"locators":"(2.2)-(2.6), printed pp.6-7"},
        "consumer_claims":["RPI8"],
        "matched_hypotheses":[
            {"hypothesis":"Connected reductive group over Q","verification":"FV1-FV4/FV10 on the exact source Res_(F/Q) U(J)."},
            {"hypothesis":"Maximal Q-split torus and a rational minimal parabolic containing it","verification":"Selected in the published Siegel setup (2.2); A is its connected positive real part."},
            {"hypothesis":"Positive root system for that minimal parabolic","verification":"Use its Lie(N0) root spaces as in (2.5); possibly nonreduced roots are allowed."}],
        "output":"Finite rational root system, simple-root basis and nonnegative integral positive-root coefficients; rational split-torus weights. The norm bound and contraction estimates are proved independently.",
        "all_hypotheses_checked":True,
    },
    {
        "id": "RPI_REAL_SIEGEL_COVER", "classification":"A", "status":"checked published application",
        "publication":ms,
        "locators":[{"statement":"Equations (2.7)-(2.8), with standing (2.1)-(2.2)","printed_pages":"6-8","pdf_pages_zero_based":[5,6,7]}],
        "consumer_claims":["RPI8","RPI10"],
        "matched_hypotheses":[
            {"hypothesis":"Real points of a reductive rational linear algebraic group","verification":"FV1-FV4/FV10, actual G_infinity=Res_(F/Q)U(J)(R)."},
            {"hypothesis":"Compact real center","verification":"FV10 gives the product of the actual norm-one circles; rank zero is separate."},
            {"hypothesis":"Arithmetic subgroup","verification":"FV10 proves exact Gamma_s for compact-open finite K; every original open finite level supplies such a sublevel."},
            {"hypothesis":"Rational minimal parabolic and compatible maximal compact subgroup","verification":"Chosen in the standing setup; RPI8 uses exactly compact left factor in M N0 and the positive chamber."}],
        "output":"Finite rational q and one qualitative Siegel set with G_infinity=union Gamma_s q S. Each rationally translated function is checked separately in RPI10.",
        "all_hypotheses_checked":True,
        "explicit_exclusion":"Theorem A and full-center finiteness are not imported. Uniform moderate cusp decay is proved in RPI7-RPI10."},
]
published = {
    "schema":"rh-published-applications/1","component":"row_integrability","version":"0.39",
    "source_commit":PIN,"applications":applications,
    "proof_inspiration_only":{"publication":ms,"locators":"Section 5, printed p.28 (PDF p.27), after (5.11)",
                             "status":"Not an additional theorem import. RPI7-RPI10 explicitly prove the mean-zero contraction/iteration."},
    "not_checked_or_claimed":["Universal source CuspRapidDecay in quotient height",
                              "ExistsSigmaList.growth_iff via polynomial unitary reduction",
                              "Applying Miller-Schmid Theorem A while omitting its center-finiteness hypothesis"],
}
(HERE / "published_applications.json").write_text(json.dumps(published,indent=2,ensure_ascii=False)+"\n")

titles = {
    "RPI1":"Exact componentwise uniform growth",
    "RPI2":"Literal NI as the isotropic-stabilizer unipotent radical",
    "RPI3":"Finite-level product fundamental domain on original NI",
    "RPI4":"Descent of original NI cusp integrals to real arithmetic components",
    "RPI5":"Original NI normal inside every rational parabolic radical",
    "RPI6":"Every rational-parabolic cusp integral and all right derivatives",
    "RPI7":"Compact mean-zero derivative estimate with fixed lifts",
    "RPI8":"Checked rational Siegel/root setup and elementary norm contraction",
    "RPI9":"Quantitative iterated derivative contraction with compact factors",
    "RPI10":"Uniform-moderate cusp decay and all-real-points boundedness",
    "RPI11":"Boundedness of every original smooth cuspidal function",
    "RPI12":"All fixed translated products on every original finite-volume domain",
    "RPI13":"Actual Mult-span values and normalized residual actions",
    "RPI14":"Entire original DI RowPairInt with unchanged normalized measure",
    "RPI15":"First DivDef3 from original premises and same-data installation",
}
deps = {
    "RPI1":["FV10","SBD1","SBD5"],
    "RPI2":["CTC11","FV1","FV2","FV4"],
    "RPI3":["RPI2","CTC11","SBD6","SBD10","FV4","FV6","FV10"],
    "RPI4":["RPI1","RPI2","RPI3"],
    "RPI5":["RPI2","FV1","FV2","FV3","FV4","FV10"],
    "RPI6":["RPI3","RPI4","RPI5","SBD10"],
    "RPI7":["RPI3","SBD10"],
    "RPI8":["FV1","FV2","FV3","FV4","FV10"],
    "RPI9":["RPI1","RPI6","RPI7","RPI8"],
    "RPI10":["RPI6","RPI7","RPI8","RPI9"],
    "RPI11":["RPI1","RPI2","RPI3","RPI4","RPI5","RPI6","RPI10","FV9","FV10"],
    "RPI12":["RPI11","FV8"],
    "RPI13":["RPI11"],
    "RPI14":["RPI12","RPI13"],
    "RPI15":["RPI12","RPI13","RPI14","RQC4","DI10","DI11","DI12","DI13","DI14","DI15","DI16","DI17","DI18","DI19","DI20","DI21"],
}
classical = {
    "RPI2":["RPI_COCHARACTER_PARABOLICS"],
    "RPI5":["RPI_COCHARACTER_PARABOLICS"],
    "RPI8":["RPI_COCHARACTER_PARABOLICS","RPI_RELATIVE_ROOT_SETUP","RPI_REAL_SIEGEL_COVER"],
    "RPI10":["RPI_REAL_SIEGEL_COVER"],
}
maps = {
    "RPI1":["actual_group","rational_group","finite_factor","infinite_factor","actual_inf_family","actual_automorphic","actual_atTau","actual_lieAt","actual_oneP","actual_Rder","actual_RderC","actual_normInf","actual_smooth_growth"],
    "RPI2":["actual_matrix","rational_group","isotropic_frame","actual_NI","actual_NIQ","actual_cusp"],
    "RPI3":["rational_group","finite_factor","infinite_factor","isotropic_frame","actual_NI","actual_NIQ","actual_cusp"],
    "RPI4":["actual_automorphic","actual_cusp","actual_NI","actual_NIQ","finite_factor","infinite_factor"],
    "RPI5":["actual_group","actual_matrix","rational_group","isotropic_frame","actual_NI","actual_NIQ","actual_cusp"],
    "RPI6":["actual_cusp","actual_automorphic","actual_Rder","actual_smooth_growth","actual_NI"],
    "RPI7":["actual_cusp","actual_Rder","actual_smooth_growth"],
    "RPI8":["actual_group","actual_inf_family","infinite_factor","actual_normInf","actual_smooth_growth","actual_finite_classes"],
    "RPI9":["actual_Rder","actual_lieAt","actual_smooth_growth","actual_cusp","actual_normInf"],
    "RPI10":["actual_smooth_growth","actual_cusp","source_bounded_endpoint","separate_global_rapid_decay"],
    "RPI11":["actual_automorphic","actual_smooth_growth","actual_cusp","actual_inf_family","source_bounded_endpoint","actual_finite_classes","separate_global_growth_conversion","separate_polynomial_reduction"],
    "RPI12":["actual_automorphic","actual_smooth_growth","actual_cusp","actual_right_translate","actual_finite_volume_contract","actual_finite_volume","source_pair_endpoint"],
    "RPI13":["actual_DSModel","actual_model_rep","actual_model_smooth","actual_tuple","actual_MMap","actual_mult_clauses","actual_Mult_span","actual_goodPart","actual_postOn","actual_lift","actual_finite_action","actual_flagL","actual_level_character","actual_gaL","actual_linear_action","original_ext1","original_full_level","original_levFn","residue_unit_norm","flag_character_norm"],
    "RPI14":["actual_inf_family","actual_models_inf","actual_models_nu0","actual_IsModels","actual_real_data","original_Pins","original_Holds","actual_meas_lev","actual_meas_domain","actual_Mult_span","actual_goodPart","actual_finite_action","original_RowProj","original_row_producer","actual_nP","original_nP_positive"],
    "RPI15":["original_RowProj","original_row_producer","original_translate_integral","original_projector_ipM","actual_IsMultIP","actual_ipM_choice","original_Pins","original_Holds","original_Read","original_ReadL","original_ReadC","original_columns","original_ids","actual_nonzero_chain","first_DivDef3","separate_DivRows3","original_division","original_division_wrapper","separate_global_rapid_decay","separate_quotient_height"],
}
scopes = {
    "RPI1":"Every original IsInfFam and IsAutFunSm; after choosing compact-open finite K and s, one original N works for all real derivative words, with word/component constants. Source zfin unused.",
    "RPI2":"Every actual isotropic frame C; exact source subgroup closure equals the written Witt matrix group, with exact NIQ, topology and unipotent radical.",
    "RPI3":"Every compact-open subgroup of the same finite NI; real lattice and compact-closure product domain, with genuine convergent integrals.",
    "RPI4":"Every original NI cusp integral descends at each exact Gamma_s; same finite conjugation sKs^-1, no replacement by ZCusp.",
    "RPI5":"Every proper rational parabolic of Res_(F/Q)U(J); actual top-weight E-subspace gives original NI normal inside its radical.",
    "RPI6":"All rational-parabolic cusp averages on exact arithmetic components; every right word remains cuspidal via dominated differentiation on compact unipotent quotient.",
    "RPI7":"Fixed compact path set and constant before the smooth mean-zero function; left derivatives evaluated on lifts, no false descent assertion.",
    "RPI8":"Same arithmetic component and faithful norm; qualitative finite rational cover only, with rational roots and exact simple-root contraction constants.",
    "RPI9":"For each derivative length k, finite compact C_j=B_alpha^j C_left; constants may depend on k, exponent N does not; all cusp derivatives before each mean-zero step.",
    "RPI10":"Every smooth cuspidal function having supplied real uniform moderate growth; no center finiteness or K-finiteness needed. Check each rational left translate in finite cover.",
    "RPI11":"For all original D,V,theta,phi with IsInfFam, IsAutFunSm and IsCuspFun, one bound before all adelic g. Not uniform in phi and not a quotient-height assertion.",
    "RPI12":"Every supplied original Haar and a.e. rational fundamental domain; every fixed two right translates and scalars, every finite nonnegative measure rescaling and finite sum.",
    "RPI13":"Every element of literal algebraic Mult span and goodPart at arbitrary original DSModel/level, every smooth tuple; finite action uses exact chosen lift/character or its source zero branch.",
    "RPI14":"Every b,t,w in full datYt(t,0,P_b) Mult,c in dat0(P_b) goodPart,v,vprime,g, on same MY0, betaY0, theta, fd0 and ofReal(nP^-1)*nu0; original Pins/Holds only.",
    "RPI15":"Original DI first-output implication with all five real-group predicates, same readings, Pins/Holds/group tie and sEE; extra RowPairInt removed. No production of common data and no second DivRows3/theta square.",
}
assert set(titles) == set(deps) == set(maps) == set(scopes)
incoming = {c["id"] for f in inherited for c in f["claims"]}
assert all(c in titles or c in incoming for ds in deps.values() for c in ds)
assert all(s in sources for ss in maps.values() for s in ss)
assert all(p in {a["id"] for a in applications} for ps in classical.values() for p in ps)
tex = (HERE / "main.tex").read_bytes()
lines = tex.splitlines(keepends=True)
claims = []
for cid in titles:
    a = next(i for i,line in enumerate(lines) if line.strip() == ("% BEGIN " + cid).encode())
    z = next(i for i in range(a+1,len(lines)) if lines[i].strip() == ("% END " + cid).encode()) + 1
    b = b"".join(lines[a:z])
    claims.append({
        "id":cid,"title":titles[cid],"introduced_in":"0.39","classification":"B",
        "status":"complete independent human proof in the stated scope, with separately checked published inputs",
        "depends_on":deps[cid],"classical_inputs":classical.get(cid,[]),
        "quantifier_scope":scopes[cid],
        "proof_location":{"file":"row_integrability/main.tex","label":"claim:"+cid,
                          "line_start":a+1,"line_end":z,"sha256":sha(b),"range_sha256":sha(b),"bytes":len(b)},
        "source_ids":maps[cid],"sources":[sources[s] for s in maps[cid]],
    })

remaining = [
    {"id":"RPI_COMMON_ORIGINAL_DATA","classification":"C","status":"retained original common producer",
     "contract":"One actual R/readings/columns/geometry with original Pins/Holds, same rational tests and positive operators, original nonzero IsItW/chain activation, and all five original real-group predicates. RPI supplies row integrability, not these objects.",
     "source_ids":["original_Pins","original_Holds","original_Read","original_ReadL","original_ReadC","actual_nonzero_chain","original_division"],
     "not_new_independent_top_level_obligation":True},
    {"id":"RPI_SEPARATE_SECOND_DIVROWS3","classification":"B","status":"separate reconstruction and same-object installation",
     "contract":"Second DivRows3 output, including actual theta square and original row metrics, index identities and column pairing, on its original additional MjHTie/IdxDefs/BuRational/BtVanish inputs.",
     "source_ids":["separate_DivRows3","original_division_wrapper"],
     "not_new_independent_top_level_obligation":True},
    {"id":"RPI_UNIVERSAL_GLOBAL_HEIGHT_DECAY","classification":"C","status":"not proved; unnecessary for the exact closed row-pair endpoint",
     "contract":"Universal source CuspRapidDecay in original quotient height, and polynomial unitary reduction/growth_iff. RPI proves componentwise decay and actual global boundedness only.",
     "source_ids":["separate_global_rapid_decay","separate_quotient_height","separate_global_growth_conversion","separate_polynomial_reduction"],
     "not_required_for_closed_RPI_endpoint":True,"not_new_independent_top_level_obligation":True},
]
prov = {
    "schema":"rh-human-component-provenance/1","artifact_version":"0.39","date":"2026-11-22",
    "component":"row_integrability","source_commit":PIN,"main_tex_sha256":sha(tex),
    "metadata_builder":{"file":"build_metadata.py","sha256":sha(Path(__file__).read_bytes()),
                        "portable_invocation":"python3 build_metadata.py --source /path/to/pinned/checkout --human-root /path/to/reconstruction"},
    "claims":claims,"source_inventory":list(sources.values()),"baseline_dependencies":inherited,
    "published_applications":{"file":"published_applications.json","sha256":sha((HERE/"published_applications.json").read_bytes()),
                              "certificate_ids":[a["id"] for a in applications]},
    "remaining_producer_contracts":remaining,
    "validation":{"source_commit_verified":True,"pinned_blob_verified_files":len(cache),
                  "source_ranges":len(sources),"claim_source_occurrences":sum(map(len,maps.values())),
                  "all_source_ranges_exact":True,"all_inherited_claim_edges_explicit":True,
                  "all_published_hypotheses_matched":True,"new_lean_build":False,
                  "tex_validation":"See validation/validation.json: offline draft syntax/layout, no PDF."},
    "scope_note":"Entire DI RowPairInt is supplied independently, so the inherited first DivDef3 implication needs only original premises. No whole common-data selected leaf closure or universal quotient-height theorem is asserted.",
}
(HERE/"provenance.json").write_text(json.dumps(prov,indent=2,ensure_ascii=False)+"\n")
closure = {
    "schema":"rh-human-component-closure/1","version":"0.39","component":"row_integrability","source_commit":PIN,
    "standing_assumption":"The pinned Alpoge-Claude Lean proof is assumed fully checked and correct. Statuses concern the human reconstruction only.",
    "main_sha256":sha(tex),"main_tex_sha256":sha(tex),"sha256":sha(tex),
    "provenance_sha256":sha((HERE/"provenance.json").read_bytes()),
    "new_claim_ids":list(titles),"claim_count":len(titles),"class_counts":{"A":0,"B":15,"C":0,"D":0},
    "published_application_certificate_ids":[a["id"] for a in applications],
    "closed_contracts":[
        {"id":"RPI_NI_TO_REAL_CUSP","claims":["RPI2","RPI3","RPI4","RPI5","RPI6"],
         "classification":"B","status":"complete human producer",
         "contract":"Original NI/NIQ/IsCuspFun imply every classical rational-parabolic cusp integral on each original arithmetic component; all right derivatives preserve it."},
        {"id":"RPI_ORIGINAL_SMOOTH_CUSP_BOUNDED","claims":["RPI1","RPI7","RPI8","RPI9","RPI10","RPI11"],
         "classification":"B","status":"complete human producer with checked qualitative reduction",
         "contract":"IsInfFam+IsAutFunSm+IsCuspFun imply one bound before all original adelic g, without full-center or polynomial global-height inputs."},
        {"id":"DI_ROW_PAIR_INTEGRABILITY","claims":["RPI12","RPI13","RPI14"],
         "classification":"B","status":"closed original-data producer",
         "contract":"Exactly all b,t, full-level w, goodPart c, smooth tuples v/vprime and residual g; product conjugate(A_(R.eG g)(c(v)))*w(vprime) integrable on unchanged R.fd0 for ofReal(nP(F.lv2,b)^-1)*R.nu0.",
         "requires":["original Pins/Holds fields for IsInfFam and Haar/fundamental-domain data","same original MY0, levels, model, actions and scalar normalization"],
         "no_additional_analytic_supplier":True},
        {"id":"RPI_FIRST_DIVDEF3_ORIGINAL_PREMISES","claims":["RPI15"],
         "classification":"B","status":"closed conditional implication on original premises",
         "contract":"Inherited DI1-DI21 first-output constructor with its extra RowPairInt discharged; all original common/read/chain/rational/operator and five-predicate premises remain.",
         "requires":["DI20/DI21 reconstructed first-output consumer","RPI14 on the same realization"],
         "dependency_mode":"sufficient conjunction, not production of the retained original inputs"}],
    "same_object_sufficient_rule":{
        "universals":"Every same original D,G,A3,Ks,R,F,cG,X0,Y,Z,C,sEE and the original five real-group predicates, Pins/Holds and group-cardinality rule.",
        "row_quantifier_order":["fixed original realization and measures","every b,t","every original full-level w and goodPart c","every pair of original smooth tuples","every residual g"],
        "unchanged":["R.MY(0)","R.theta","R.betaY(0)","R.datYt(t,0,P_b)","R.dat0(P_b)","R.eG","original selected finite lift/levChi","R.fd0","ofReal(nP^-1)*R.nu0"],
        "output":"DI RowPairInt; then original first DivDef3 on the same idsOf/colOf/NuC. No new threshold."},
    "remaining_inputs":remaining,"selected_top_level_leaf_closed":False,
    "not_claimed":["Universal quotient-height CuspRapidDecay","Polynomial unitary reduction or growth_iff",
                   "Existence of an IsMultIP scalar for every pair","Original common R/readings/chain production",
                   "Stronger second DivRows3/theta square","New Lean replay/build"],
    "review_status":"Awaiting independent review at initial metadata build; external hash-bound review files record the final disposition.",
}
(HERE/"closure.json").write_text(json.dumps(closure,indent=2,ensure_ascii=False)+"\n")
loc = ["RPI source locators", "Pinned source: "+PIN, "All intervals inclusive; exact bytes verified against pinned Git blobs.", ""]
for cid in titles:
    loc += [cid+": "+titles[cid]]
    for sid in maps[cid]:
        s=sources[sid]
        loc += [f"  {s['path']}:{s['line_start']}-{s['line_end']}  {s['declaration']}",
                "    file_sha256="+s["file_sha256"]+" range_sha256="+s["range_sha256"]]
    loc += [""]
loc += ["Published applications: published_applications.json; exact primary URLs and checked hypotheses.",
        "No new Lean audit, replay or build."]
(HERE/"source_locators.txt").write_text("\n".join(loc)+"\n")
result = {"claims":len(claims),"source_files":len(cache),"source_ranges":len(sources),
          "claim_source_occurrences":sum(map(len,maps.values())),"inherited_blocks":sum(len(x["claims"]) for x in inherited),
          "main_sha256":sha(tex),"provenance_sha256":sha((HERE/"provenance.json").read_bytes()),
          "closure_sha256":sha((HERE/"closure.json").read_bytes()),
          "published_applications_sha256":sha((HERE/"published_applications.json").read_bytes())}
print(json.dumps(result,indent=2))
