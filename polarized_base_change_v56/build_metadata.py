#!/usr/bin/env python3
"""Bind PBC's original arbitrary-base constructors to human proofs and pinned sources.
Writes only this component. No Lean replay or mutation of earlier components.
"""
from pathlib import Path
import argparse
import hashlib
import json
import subprocess

HERE = Path(__file__).resolve().parent
WORK = HERE.parent
COMP = HERE.name
PIN = "7cbf7a0c32fca1badf05931879a37c3f8a2b03b4"
REPO = "https://github.com/CocoSgt/riemann-hypothesis-lean"
A = "src/Development/AbelianVarietyTheory/Proofs/AbelianSchemeLawProofs/"
R = "src/ReciprocityTheory/ReductiveGroups/ArithmeticGeometry/"
T = R+"BirationalGeometry/ToroidalCompactification/"
E = R+"ExtensionDescent/"
S = R+"SemiabelianSchemes/"
ap = argparse.ArgumentParser()
ap.add_argument("--source-root", type=Path,
                default=Path("/workspace/scratch/249d32c24541/formal_source"))
args = ap.parse_args()
sha = lambda b: hashlib.sha256(b).hexdigest()
def write(name, data):
    (HERE/name).write_text(json.dumps(data, ensure_ascii=False, indent=2)+"\n")

proof = (HERE/"main.tex").read_bytes()
base = dict(artifact_version="0.56", component=COMP, source_commit=PIN,
            proof_file_sha256=sha(proof), status="written_pending_independent_review")
rows = []
def src(key, file, lo, hi, declaration, prefix=A):
    rows.append((key, prefix+file, lo, hi, declaration))

src("stalk_definitions", "ExistsOneAddKill.lean", 13, 28, "Fn; Reg; IsLoc; total inverse; Gen")
src("regular_calculus", "ExistsOneAddKill.lean", 30, 93, "section equality, local gluing, inverses and affine principal opens")
src("kill_frac", "ExistsOneAddKill.lean", 95, 119, "kill; frac, with arbitrary rings and quasi-compact vanishing locus")
src("generation_calculus", "ExistsOneAddKill.lean", 121, 153, "Gen.mono; Gen.loc")
src("local_global", "ExistsOneAddKill.lean", 155, 238, "van; local_global, including the unit-ideal affine criterion")
src("local_global_endpoint", "ExistsOneAddKill.lean", 165, 238, "local_global")
src("determinant_trick", "ExistsOneAddKill.lean", 240, 282, "exists_one_add_kill")
src("sc_calculus", "ExistsOneAddKill.lean", 284, 305, "Sc; restriction, multiplication, powers; original cover and unit hypotheses")
src("sc_ratios", "ExistsOneAddKill.lean", 306, 323, "Sc.exists_loc; Sc.ratio")
src("sc_extend", "ExistsOneAddKill.lean", 325, 384, "Sc.extend: full qcqs two-exponent section extension")
src("extra_section", "ExistsOneAddKill.lean", 386, 502, "extra_section")
src("pack_definition", "RelAmpleOfLocallyOnBase.lean", 13, 16, "Pack")
src("glue_pack", "RelAmpleOfLocallyOnBase.lean", 18, 103, "glue_pack")
src("pull_stalks", "RelAmpleOfLocallyOnBase.lean", 105, 155, "pb; local unit reflection; actual regular pullback; cst")
src("open_immersion_transport", "RelAmpleOfLocallyOnBase.lean", 157, 214, "pb_surj; reg_push; gen_push; pack_push")
src("pack_push_endpoint", "RelAmpleOfLocallyOnBase.lean", 194, 212, "pack_push")
src("polynomial_dictionary", "RelAmpleOfLocallyOnBase.lean", 216, 261, "gen_iff")
src("actual_section_dictionary", "RelAmpleOfLocallyOnBase.lean", 267, 299, "sec_tr; sv; loc_sv; ratio_iff")
src("ratio_dictionary_endpoint", "RelAmpleOfLocallyOnBase.lean", 282, 299, "ratio_iff")
src("section_gauge_hypotheses", "RelAmpleOfLocallyOnBase.lean", 303, 311, "exact U,kappa,c,G,N conditions; sc_sv")
src("exists_sv", "RelAmpleOfLocallyOnBase.lean", 313, 327, "exists_sv")
src("pack_generator_change", "RelAmpleOfLocallyOnBase.lean", 331, 337, "Pack.mono")
src("principal_base_constants", "RelAmpleOfLocallyOnBase.lean", 339, 358, "cst_mem")
src("constant_tuple_power", "RelAmpleOfLocallyOnBase.lean", 360, 366, "gm_const")
src("local_principal_pack", "RelAmpleOfLocallyOnBase.lean", 368, 448, "pack_of_relAmple")
src("rel_ample_local", "RelAmpleOfLocallyOnBase.lean", 450, 487, "relAmple_of_locally")
src("rel_ample_export", "RelAmpleOfLocallyOnBaseStatement.lean", 7, 8, "GlobalTheory.T.relAmple_of_locally_on_base")
src("bundle_identity", "PolBaseChangeOfRelAmpleLocal.lean", 16, 24, "lbIso_refl")
src("group_identity_inverse", "PolBaseChangeOfRelAmpleLocal.lean", 29, 43, "eSec_comm; inv_comm")
src("rigidified_pull", "PolBaseChangeOfRelAmpleLocal.lean", 45, 48, "rigidified_pull")
src("symmetry_pull", "PolBaseChangeOfRelAmpleLocal.lean", 50, 61, "sym_pull")
src("rel_ample_restrict", "PolBaseChangeOfRelAmpleLocal.lean", 65, 75, "relAmple_restrict")
src("polarized_constructor", "PolBaseChangeOfRelAmpleLocal.lean", 83, 108, "polBaseChange_of_relAmple_local")
src("polarized_export", "AbelianSchemeLawsWithoutCohomology.lean", 15, 16, "polBaseChange_holds")
src("very_ample_consumer", "VeryAmpleByOfRelAmple.lean", 113, 121, "polAV_veryAmpleBy")
src("perf_section_relation", "AbelianVarietyLineBundleSectionsFinite.lean", 34, 76,
    "Perf.exists_relation with all original chart-coordinate equations")
src("sections_finite", "AbelianVarietyLineBundleSectionsFinite.lean", 78, 100,
    "sections_finite_of_perf")
src("sections_finite_export", "AbelianVarietyLineBundleSectionsFiniteStatement.lean", 9, 10,
    "GlobalTheory.T.abelianVariety_lineBundle_sections_finite")
src("finite_from_dependence", "FiniteOfNotLinearIndependent.lean", 211, 239,
    "finite_of_not_linearIndependent; finite/finrank coefficient-isomorphism transport")
src("finite_secM", "FiniteOfNotLinearIndependent.lean", 242, 278,
    "finite_secM with the actual identity-product and every integer power")
src("chart_bundle_definitions", "CubicalStructures/CubeSymmetricSwapFirst.lean", 17, 84,
    "LB; IsLB; Gen; Sec; div; Iso; LinComb; pull; pullGen", S)
src("ample_polarized_contract", "NonzeroLocus.lean", 19, 76,
    "Rigidified; Sym; powOver; nonzeroLocus; RelAmple; translDiff; KTriv; full PolAV", E)
src("pol_base_change_contract", "GlobalSectionsRankAlgClosed.lean", 154, 165,
    "toBase; full arbitrary-base/all-test PolBaseChangeSt", E)
src("group_pullback_contract", "IsGrpPullback.lean", 25, 29,
    "IsGrpPullback, including arbitrary test T and compatible x0,y0", T)
src("abelian_contract", "AbelianSchemeQuotients/IsAbelianScheme.lean", 15, 19,
    "IsAbelianScheme: commutative, smooth, proper, geometrically connected", S)
src("abelian_base_change", "ChartPullbacks/TangentLinearity/ConstPullback.lean", 91, 103,
    "TLinPf.isAb_pullback", E)
src("total_unit_germs", "PullCub.lean", 14, 21, "gm, including value 1 outside the indicated open", T)
src("germ_cocycle", "PullCub.lean", 89, 107, "gm_cocycle; gm_self", T)
src("generated_iso_germ_contract", "PullCub.lean", 109, 147, "gw; PGen and isGen_iff", T)
src("chart_iso_comparison", "SabPull.lean", 18, 90,
    "ChartPull; LBIso.chartPull; LinComb transitions; chartPullLinComb", T)
src("group_pullback", "SabPull.lean", 102, 155,
    "pushHom; isGrpPullback_pullback", T)
src("group_pullback_endpoint", "SabPull.lean", 132, 153,
    "isGrpPullback_pullback", T)
src("generator_pull_comparison", "AmplePt.lean", 14, 69,
    "gen_chartPull; chartPullIn/Out; iso_linComb; actual nonzeroLocus", T)
src("k_triv_pull", "AmplePt.lean", 75, 113, "kTriv_pull", T)
src("rel_ample_pull", "AmplePt.lean", 117, 177, "relAmple_pull", T)
src("section_pull", "ThetaCore.lean", 80, 116,
    "gs_compat; full all-test sec_pull_down", T)
src("section_pull_endpoint", "ThetaCore.lean", 108, 116,
    "sec_pull_down", T)
src("lincomb_units", "IsMonHomOfMul.lean", 16, 65,
    "pw; pw_trans; exists_pw, all integer exponents", T)
src("generator_up", "IsMonHomOfMul.lean", 213, 267,
    "exists_up with its full all-test generator formula", T)

previous = json.loads((WORK/"serre_h1_v55/contracts.json").read_text())
retained = [dict(x) for x in previous["remaining_global_producers"] if x["id"] != "GSL_POL_BASE_CHANGE"]
completed_input = next(dict(x) for x in previous["remaining_global_producers"] if x["id"] == "GSL_POL_BASE_CHANGE")
for inp in retained:
    for j, s in enumerate(inp.get("sources", [])):
        src("retained_"+inp["id"].lower()+"_"+str(j), s["path"],
            s["line_start"], s["line_end"], s["declaration"], "")

files, sources = {}, {}
for key, path, lo, hi, declaration in rows:
    if path not in files:
        blob = subprocess.check_output(["git", "-C", str(args.source_root), "show", PIN+":"+path])
        assert (args.source_root/path).read_bytes() == blob, "Checkout differs from pin: "+path
        dest = HERE/"source_snapshot"/path
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_bytes(blob)
        files[path] = dict(path=path, snapshot_file=str(dest.relative_to(WORK)),
            bytes=len(blob), line_count=len(blob.splitlines()), sha256=sha(blob),
            file_sha256=sha(blob), source_commit=PIN,
            verified_equal_to_pinned_git_blob=True, url=REPO+"/blob/"+PIN+"/"+path)
    row = files[path]
    ls = (WORK/row["snapshot_file"]).read_bytes().splitlines(keepends=True)
    assert 1 <= lo <= hi <= len(ls), (key, lo, hi, len(ls))
    part = b"".join(ls[lo-1:hi])
    sources[key] = dict(id="PBC_SRC_"+key.upper(), path=path, declaration=declaration,
        line_start=lo, line_end=hi, source_commit=PIN, file_sha256=row["sha256"],
        full_file_sha256=row["sha256"], range_sha256=sha(part), range_bytes=len(part),
        snapshot_file=row["snapshot_file"], verified_equal_to_pinned_git_blob=True,
        url=row["url"]+f"#L{lo}-L{hi}")
for inp in retained:
    inp["sources"] = [sources["retained_"+inp["id"].lower()+"_"+str(j)]
                      for j in range(len(inp.get("sources", [])))]
    inp["globally_discharged_by_this_component"] = False
    inp["boundary_inherited_from"] = "serre_h1_v55/contracts.json"
    if inp["id"] == "GSL_FINITE_GROWTH":
        inp["completed_subproducer_claim_ids"] = ["PBC27"]
        inp["completed_subproducer"] = "Actual section finiteness, including every original integer-power SecM."
        inp["remaining_subproducer"] = "The exact two-sided t^g growth bounds and their original geometric dimension inputs."

specs = [
("PBC1", [], ["stalk_definitions","regular_calculus","sc_calculus","sc_ratios"],
 "Regular stalk functions, unit loci and same-degree ratios.",
 "Arbitrary scheme, actual regular representatives; total inverse is used only on its unit locus."),
("PBC2", [], ["kill_frac"],
 "Affine fractions and one power killing vanishing on a quasi-compact open.",
 "Arbitrary rings and zero divisors; quasi-compact W only for killing, affine W for fractions."),
("PBC3", ["PBC1","PBC2"], ["sc_calculus","sc_extend"],
 "Full original Sc.extend with both finite exponents.",
 "Original arbitrary cover/gauges, qcqs Z and every degree n; first clear fractions, then kill overlap discrepancies, without changing n."),
("PBC4", ["PBC2","PBC3"], ["local_global"],
 "The complete unit-ideal principal-open affineness criterion.",
 "An arbitrary family reduces to a finite unit-ideal expression; qcqs follows from its affine principal cover, then actual localized global rings glue."),
("PBC5", ["PBC1","PBC2"], ["generation_calculus","polynomial_dictionary"],
 "Generated-function substitution, localization and the literal polynomial-evaluation equivalence.",
 "Gen.iff has arbitrary R, arbitrary generator index set and actual coefficient map; no affineness or Noetherianity added."),
("PBC6", ["PBC1","PBC2","PBC4","PBC5"], ["local_global_endpoint"],
 "Full original local_global for affine generation.",
 "Arbitrary index family; keeps van(B,W)+(w_lambda)=B, not the stronger vanishing-ideal-zero condition."),
("PBC7", [], ["determinant_trick"],
 "Full original exists_one_add_kill by an explicit finite determinant.",
 "Any commutative B and ideal K; finite generators only; empty family, zero exponents and zero module are covered."),
("PBC8", ["PBC1","PBC2","PBC5"], ["extra_section"],
 "The actual mixed ratios and their higher-power ideal relations.",
 "Original finite T, arbitrary N,d>=0; no cancellation away from the stated unit loci; K is exact stalkwise vanishing on W."),
("PBC9", ["PBC5","PBC6","PBC7","PBC8"], ["extra_section"],
 "Full original extra_section: affine unit locus and the mixed-ratio generators.",
 "Every same-higher-degree tau, arbitrary ring, including empty T; produces precisely all s_j s_i^d/tau generators."),
("PBC10", ["PBC1","PBC3"], ["pack_definition","glue_pack"],
 "One positive common degree and finitely many globally extended mixed sections.",
 "One product N before any denominator tau; each mixed section has its own extension exponent; finite empty base-index case preserved."),
("PBC11", ["PBC1","PBC5","PBC6","PBC9","PBC10"], ["glue_pack"],
 "Affine generation for every denominator of the fixed common degree.",
 "The numerator family is fixed before arbitrary tau and its exact open E; no Noetherianity or flatness."),
("PBC12", ["PBC10","PBC11"], ["pack_definition","glue_pack"],
 "Full original glue_pack with its nonempty finite tuple and universal final open.",
 "Appends zero solely to realize Fin(M+1); retains every t,D IsLoc test and the actual R-map."),
("PBC13", ["PBC1","PBC5"], ["pull_stalks","open_immersion_transport","pack_push_endpoint"],
 "Original stalk pullback and open-immersion pack transport.",
 "Stalk functions extend by inverse stalk maps and zero outside the image, without claiming boundary regularity; actual regularity is only on the image."),
("PBC14", ["PBC1"], ["actual_section_dictionary","section_gauge_hypotheses","constant_tuple_power"],
 "The chosen-chart value and exact all-chart ratio dictionary.",
 "Forward dictionary only requires existing compatible sections and a chart containing each point, not an added IsLB premise."),
("PBC15", ["PBC1"], ["section_gauge_hypotheses","exists_sv"],
 "Full original exists_sv on every original chart.",
 "Keeps original kappa,c,G,N equation; G may be arbitrary here; no added global-unit or regular-ratio premise."),
("PBC16", ["PBC13"], ["principal_base_constants"],
 "Original cst_mem for the actual principal base neighborhood.",
 "Actual open immersion V=D(a) in affine B; equality as stalk functions on all Y via the given commutative square."),
("PBC17", ["PBC5","PBC13","PBC14","PBC16"], ["pack_generator_change","constant_tuple_power","local_principal_pack"],
 "Full original pack_of_relAmple.",
 "Same original open restrictions, map to A, line-bundle chart datum and pointwise chart choice; no additional IsLB hypothesis beyond the source."),
("PBC18", ["PBC1","PBC5","PBC12","PBC14","PBC15","PBC17"], ["rel_ample_local","rel_ample_export","ample_polarized_contract"],
 "Full arbitrary-base relAmple_of_locally and its exported original interface.",
 "Arbitrary S, actual L, qc and qs A.hom; every affine base open; finite good functions generate 1 without Noetherianity."),
("PBC19", ["PBC1"], ["chart_bundle_definitions","chart_iso_comparison","generator_pull_comparison","section_pull_endpoint","lincomb_units","generator_up","bundle_identity","generated_iso_germ_contract"],
 "Actual generated bundle comparisons, all-test section pullback and all integer LinComb powers.",
 "Literal chart records, negative exponents, unit gluing, every test Z,r,z; identity Iso uses the original transition units."),
("PBC20", ["PBC19"], ["rel_ample_pull","ample_polarized_contract"],
 "Full original relAmple_pull for a base map landing in a specified affine open.",
 "Original arbitrary Cartesian square and generated L' comparison; S' arbitrary; affine pushout/tensor surjectivity, with no flatness."),
("PBC21", ["PBC19","PBC20"], ["rel_ample_restrict"],
 "Full original relAmple_restrict on the literal nested pullback.",
 "The full inverse-image base open is allowed to be nonaffine; the actual pasted Cartesian square is retained."),
("PBC22", [], ["group_pullback_contract","group_pullback_endpoint","group_identity_inverse","abelian_contract","abelian_base_change"],
 "Actual pullback group and abelian/smooth-dimensional fields with every test map.",
 "Canonical original Over.pullback; injective push on every T, identity and inversion compatibility, and original g retained."),
("PBC23", ["PBC19","PBC22"], ["rigidified_pull","symmetry_pull"],
 "Full original rigidified_pull and sym_pull.",
 "Actual original generators pull to the actual bundle; symmetry remains locally on the base, without claiming a global symmetry tuple."),
("PBC24", ["PBC19","PBC22"], ["k_triv_pull","ample_polarized_contract"],
 "Full original kTriv_pull at every affine test ring.",
 "Canonical T-times-base isomorphism, same R,t,x,V and actual translated bundle generators; no faithful-flatness or field specialization."),
("PBC25", ["PBC18","PBC19","PBC21","PBC22","PBC23","PBC24"], ["polarized_constructor","polarized_export","pol_base_change_contract"],
 "Full original PolBaseChangeSt on the prescribed categorical pullback.",
 "Every S,S',f,P; literal A' and L.pull, g unchanged, all-test multiplication, actual Iso generator, every PolAV field."),
("PBC26", ["PBC25","GSL14","GSL15"], ["very_ample_consumer"],
 "Full original polAV_veryAmpleBy with the base-change premise supplied.",
 "Every R,t and specified Cartesian X,pi,f; original pw bundle and actual sections; N chosen separately for that test, not uniformly over all tests."),
("PBC27", ["PBC19","PBC26","ASL21"], ["perf_section_relation","sections_finite","sections_finite_export","finite_from_dependence","finite_secM"],
 "Full original actual-section finiteness and every integer-power SecM.",
 "The explicit n=Q.a+1 is chosen before every tuple; the actual Perf coordinate identity supplies a nonzero relation on every original chart; K-to-Gamma scalars and the identity fiber product are retained. Two-sided growth is not asserted.")
]
lines = proof.splitlines(keepends=True)
claims = []
for ident, deps, groups, title, scope_note in specs:
    lo = next(i for i,l in enumerate(lines) if l.strip() == ("% BEGIN "+ident).encode())
    hi = next(i for i,l in enumerate(lines) if l.strip() == ("% END "+ident).encode())
    block = b"".join(lines[lo:hi+1])
    claims.append(dict(id=ident, title=title, introduced_in="0.56", classification="B",
        depends_on=deps, external_input_ids=["PBC_STANDARD"], scope_note=scope_note,
        source_groups=groups, sources=[sources[g] for g in groups],
        proof_location=dict(file=COMP+"/main.tex", label="claim:"+ident,
            line_start=lo+1,line_end=hi+1,sha256=sha(block),bytes=len(block)),
        proof_status="complete at the stated original mathematical hypotheses",
        status="complete human proof; pending independent review",
        scope_class="complete_at_original_mathematical_hypotheses",
        source_proof_is_not_human_proof=True))

inherited = []
uses = [
("global_section_laws_v52","GSL14","dependency","Actual scheme/bundle-isomorphism section transport consumed in PBC26."),
("global_section_laws_v52","GSL15","dependency","The original all-affine-test very-ample implication, now discharged by PBC25."),
("global_section_laws_v52","GSL17","next_consumer","Its PolBaseChange and Serre premises are now supplied; multiplication comparison/geometry and every-open torsion descent remain."),
("global_section_laws_v52","GSL23","next_consumer","Full base-change conditional join retains closed-field vanishing and rank."),
("global_section_laws_v52","GSL24","next_consumer","The original twist-basis conditional join keeps its geometric translated-power supplier."),
("global_section_laws_v52","GSL25","next_consumer","The original residue-section-lift conditional join keeps every local ring and every residue section."),
("actual_section_localization_v54","ASL21","dependency","Completed arbitrary-base smooth-projective Perf producer used in PBC27; not reopened or an assumption of PBC25."),
("serre_h1_v55","SHV17","context","Completed original Noetherian-base, arbitrary-M, all-cover Serre H1; not an assumption of arbitrary-base relative ampleness."),
("serre_h1_v55","SHV21","context","Completed uniform homogeneous-polynomial high-power sections; not an added premise of PBC25.")
]
for comp, ident, role, use in uses:
    pp = WORK/comp/"provenance.json"
    prev = json.loads(pp.read_text())
    old = next(x for x in prev["claims"] if x["id"] == ident)
    loc = old["proof_location"]
    data = (WORK/loc["file"]).read_bytes()
    part = b"".join(data.splitlines(keepends=True)[loc["line_start"]-1:loc["line_end"]])
    assert sha(data) == prev["proof_file_sha256"]
    assert sha(part) == loc["sha256"]
    inherited.append(dict(id=ident, component=comp, role=role, title=old["title"],
        proof_file=loc["file"], proof_file_sha256=sha(data), proof_block_sha256=sha(part),
        proof_location=loc, source_commit=PIN, use=use,
        all_original_premises_retained=True,
        provenance_file=str(pp.relative_to(WORK)), provenance_sha256=sha(pp.read_bytes())))

def header(key):
    s=sources[key]
    ls=(WORK/s["snapshot_file"]).read_bytes().splitlines(keepends=True)
    return b"".join(ls[s["line_start"]-1:s["line_end"]]).decode().split(":=",1)[0].strip()
endpoints = []
for ident, key, output in [
("PBC3","sc_extend","Full original Sc.extend: prescribed degree and two finite powers over every qcqs Z."),
("PBC5","polynomial_dictionary","Full original gen_iff, with arbitrary generator family and actual coefficient map."),
("PBC6","local_global_endpoint","Full original local_global, including its vanishing ideal and arbitrary index family."),
("PBC7","determinant_trick","Full original exists_one_add_kill over arbitrary rings."),
("PBC9","extra_section","Full original extra_section for every tau and d>=0."),
("PBC12","glue_pack","Full original glue_pack, with one common positive degree and every final IsLoc open."),
("PBC13","pack_push_endpoint","Full original pack_push through the actual open immersion."),
("PBC14","ratio_dictionary_endpoint","Both directions of the original ratio_iff on every chart."),
("PBC15","exists_sv","Full original exists_sv, with the exact original gauge hypotheses."),
("PBC16","principal_base_constants","Full original cst_mem and its literal stalk-function subring membership."),
("PBC17","local_principal_pack","Full original pack_of_relAmple."),
("PBC18","rel_ample_local","Full original arbitrary-base relAmple_of_locally."),
("PBC18","rel_ample_export","Exact original exported relAmple_of_locally_on_base."),
("PBC19","section_pull_endpoint","Full original sec_pull_down, including all Z,r,z,j,k."),
("PBC19","generator_up","Full original exists_up and its all-test product-of-comparison-units identity."),
("PBC19","bundle_identity","Full original lbIso_refl with actual division-bundle units."),
("PBC20","rel_ample_pull","Full original relAmple_pull with its specified affine image."),
("PBC21","rel_ample_restrict","Full original relAmple_restrict on the full inverse-image base open."),
("PBC22","group_pullback_endpoint","Full original isGrpPullback_pullback."),
("PBC22","abelian_base_change","Full original isAb_pullback."),
("PBC23","rigidified_pull","Full original rigidified_pull."),
("PBC23","symmetry_pull","Full original sym_pull."),
("PBC24","k_triv_pull","Full original kTriv_pull at every original affine test."),
("PBC25","polarized_constructor","The entire original polarized constructor with its relative-ample premise supplied by PBC18."),
("PBC25","polarized_export","Full original polBaseChange_holds / PolBaseChangeSt."),
("PBC26","very_ample_consumer","Full original polAV_veryAmpleBy with its P premise supplied."),
("PBC27","perf_section_relation","Full original Perf.exists_relation over every field, using the actual cover and scalar map."),
("PBC27","sections_finite","Full original sections_finite_of_perf with both original producers supplied."),
("PBC27","sections_finite_export","Exact exported original actual-section finiteness."),
("PBC27","finite_secM","Full original finite_secM conditional implication, and actual integer-power finiteness for every original algebraically closed P.")
]:
    h=header(key)
    endpoints.append(dict(claim_id=ident, source=sources[key],
        exact_source_declaration_header=h, declaration_header_sha256=sha(h.encode()),
        output=output, status="complete at all original hypotheses; no newly assumed opaque producer"))

standard = dict(id="PBC_STANDARD", name="Ordinary commutative algebra and scheme/sheaf foundations",
    kind="standard_background_not_a_selected_project_gap",
    scope_note=("Ring localizations and the unit criterion in a local ring; sheaf equality and gluing; "
        "the affine principal-open basis, affine schemes, their section localizations and affine tensor-product fiber products; "
        "the scheme Cartesian universal property and stability of standard-smooth presentations/properness under base change. "
        "The required finite determinant annihilator, all denominator exponents, unit-ideal affineness criterion, "
        "mixed-ratio generation, actual bundle comparisons and complete relative-ample and polarized constructors are proved here."),
    sources=[sources["stalk_definitions"],sources["chart_bundle_definitions"],sources["abelian_contract"]],
    globally_discharged_by_this_component=False)
completed_input["supplied_by"]=["PBC25"]
completed_input["status"]="fully supplied at its exact original arbitrary-base and all-test scope"
completed_input["globally_discharged_by_this_component"]=True
completed_input["sources"]=[sources["pol_base_change_contract"],sources["polarized_constructor"],sources["polarized_export"]]
guards = [
 "PBC18 and PBC25 allow arbitrary scheme bases, arbitrary ring maps and nilpotents; no Noetherianity, reducedness, field or flatness premise is added.",
 "PBC3 retains qcqs Z and the original cover/unit/regular-ratio data; one exponent clears local fractions and a second kills entire overlap discrepancies.",
 "PBC7 uses finitely many ideal generators but does not assume B Noetherian or K finitely generated; empty families and zero exponents are covered.",
 "PBC9 preserves every d>=0 and every higher-degree tau; off-diagonal generators are kept, and van(B,W) is not discarded.",
 "PBC10 chooses a single positive common degree and the global numerator family before the arbitrary denominator in PBC11.",
 "PBC12 returns a Fin(M+1) tuple and proves the final assertion for every t and every D satisfying the exact IsLoc equation.",
 "PBC15 has exactly the original kappa,c,G,N hypotheses and P.IsLB; it does not add global G-unit or regular-ratio hypotheses.",
 "PBC17 preserves the original pack_of_relAmple chart-datum scope and chosen covering chart; no additional L.IsLB is introduced there.",
 "PBC18 returns original powOver sections, every coordinate identity and polynomial evaluation with the actual O(U) coefficient map.",
 "PBC20 uses only affine tensor-product base change for the actual nonzero-locus charts; it never asserts arbitrary nonflat base change of global sections.",
 "PBC19 keeps the literal division-bundle comparison, negative LinComb exponents, chart refinements and every test-scheme germ formula.",
 "PBC24 preserves every commutative R,t,x and every local generator on the same V; its fiber-product comparison is an actual isomorphism.",
 "PBC25 uses the specified Over.pullback A, literal L.pull and identical g; preserves all PolAV fields and every arbitrary test T for multiplication.",
 "PBC26 permits a separately chosen positive power on every specified affine Cartesian test; it does not assert a common power or a rank n^g basis on all tests.",
 "PBC27 chooses n before every tuple, proves actual relations on all original M charts from the Perf coordinate formula, and retains the original K-to-Gamma and identity-product comparisons for every integer j.",
 "GSL_POL_BASE_CHANGE is fully supplied. The remaining multiplication, closed-field vanishing/rank, square/translation, Moduli and whole RH/GRH selected obligations are not closed by this component."
]
scope = dict(full_original_sc_extend_supplied=True,
    full_original_exists_one_add_kill_supplied=True,
    full_original_extra_section_supplied=True,
    full_original_glue_pack_supplied=True,
    full_original_exists_sv_supplied=True,
    full_original_relAmple_of_locally_supplied=True,
    full_original_relAmple_pull_supplied=True,
    full_original_kTriv_pull_supplied=True,
    full_original_PolBaseChangeSt_supplied=True,
    full_original_polAV_veryAmpleBy_supplied=True,
    full_original_actual_section_finiteness_supplied=True,
    full_original_integer_power_SecM_finiteness_supplied=True,
    full_original_two_sided_section_growth_supplied=False,
    arbitrary_base_and_target_preserved=True,
    original_actual_bundle_and_cartesian_square_preserved=True,
    original_all_test_quantifiers_preserved=True,
    no_new_noetherianity_or_flatness_hypothesis=True,
    global_positive_power_abelian_vanishing_unconditionally_supplied=False,
    global_section_laws_unconditionally_supplied=False,
    global_Moduli_supplied=False,
    selected_whole_obligations_closed=[])
write("provenance.json", dict(schema="rh-proof-provenance/1",**base,source_repository=REPO,
    claims=claims,new_claim_count=len(claims),original_endpoints=endpoints,independent_reviews=[]))
write("source_manifest.json",dict(schema="rh-source-manifest/1",**base,repository=REPO,
    snapshot_root=COMP+"/source_snapshot",files=list(files.values()),ranges=list(sources.values()),
    file_count=len(files),range_count=len(sources),total_bytes=sum(x["bytes"] for x in files.values()),
    all_files_verified_equal_to_pinned_git_blobs=True))
write("contracts.json",dict(schema="rh-component-contracts/1",**base,**scope,
    claim_ids=[x["id"] for x in claims],completed_original_suppliers=endpoints,
    quantifier_guards=guards,inherited_inputs=inherited,external_inputs=[standard],
    formerly_retained_producers_now_supplied=[completed_input],
    remaining_global_producers=retained,independent_reviews=[]))
write("inherited_inputs.json",dict(schema="rh-inherited-inputs/1",**base,inputs=inherited))
write("retained_foundations.json",dict(schema="rh-retained-foundations/1",**base,
    inputs=[standard],remaining_global_producers=retained,
    scope_note="No unsupplied original geometric producer is an assumption of PBC18 or PBC25. The retained producers are independent inputs to later abelian section laws."))
write("explicit_inputs.json",dict(schema="rh-explicit-inputs/1",**base,inputs=[standard],
    inherited_human_proofs=inherited,original_pointwise_interfaces=endpoints,
    remaining_global_producers=retained))
write("closure.json",dict(schema="rh-component-closure/1",**base,**scope,new_claim_count=len(claims),
    completed=[x["output"] for x in endpoints],
    completed_original_endpoint_claim_ids=sorted({x["claim_id"] for x in endpoints},key=lambda s:int(s[3:])),
    formerly_retained_producers_now_supplied=[completed_input],
    globally_supplied_laws=["original relAmple_of_locally_on_base","original PolBaseChangeSt","original polAV_veryAmpleBy","original actual-section finiteness and integer-power SecM finiteness"],
    pending_actual_geometric_producers=[x["id"] for x in retained],
    selected_obligation_statuses_unchanged=True,earlier_proof_components_modified=[],
    graph_nodes_added=0,graph_edges_added=0,independent_reviews=[]))
write("hashes.json",dict(schema="rh-component-hashes/1",**base,
    proof_blocks={x["id"]:x["proof_location"]["sha256"] for x in claims},
    primary_source_files={x["path"]:x["sha256"] for x in files.values()},
    inherited_proof_blocks={x["id"]:x["proof_block_sha256"] for x in inherited}))
print(json.dumps(dict(component=COMP,proof_sha256=sha(proof),claims=len(claims),
    primary_files=len(files),source_ranges=len(sources),inherited_bindings=len(inherited)),indent=2))
