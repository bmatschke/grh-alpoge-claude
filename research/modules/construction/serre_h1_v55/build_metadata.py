#!/usr/bin/env python3
"""Bind SHV's human proofs, original interfaces and pinned source bodies.
Writes only this component. No Lean replay or changes to older components.
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
ROOT = "src/Development/AbelianVarietyTheory/"
C = ROOT + "Proofs/CoherentCohomologyProofs/"
A = ROOT + "Proofs/AbelianSchemeLawProofs/"
D = ROOT + "Definitions/QuasicoherentCohomology/"
L = ROOT + "Definitions/AbelianSchemeLaws/"
ap = argparse.ArgumentParser()
ap.add_argument("--source-root", type=Path,
                default=Path("/workspace/scratch/249d32c24541/formal_source"))
args = ap.parse_args()
sha = lambda b: hashlib.sha256(b).hexdigest()
def write(name, data):
    (HERE/name).write_text(json.dumps(data, ensure_ascii=False, indent=2)+"\n")

proof = (HERE/"main.tex").read_bytes()
base = dict(artifact_version="0.55", component=COMP, source_commit=PIN,
            proof_file_sha256=sha(proof), status="written_pending_independent_review")
rows = []
def src(key, file, lo, hi, declaration, prefix=C):
    rows.append((key, prefix+file, lo, hi, declaration))

src("homogeneous_localization", "ExistsAwayFracOfMemHomLoc.lean", 170, 228,
    "xProd; homLoc and homogeneous fraction representatives", D)
src("homogeneous_maps", "ExistsAwayFracOfMemHomLoc.lean", 371, 447,
    "homLocMap; injective, surjective, exact and bijective-of-X statements", D)
src("graded_cube", "ExistsAwayFracOfMemHomLoc.lean", 577, 634,
    "grCube; original restriction, shift and graded cube maps", D)
src("graded_augmentation", "ExistsAwayFracOfMemHomLoc.lean", 673, 695,
    "grAug; naturality and augmentation bijective iff augmented degrees 0 and 1 exact", D)
src("graded_short_exact", "ExistsAwayFracOfMemHomLoc.lean", 700, 778,
    "GradedShortExact; homogeneous localization and cubeComplex_shortExact", D)
src("homloc_short_exact_theorem", "ExistsAwayFracOfMemHomLoc.lean", 729, 740,
    "GradedShortExact.homLoc", D)
src("graded_surjection", "IsGradedMapLinearCombination.lean", 489, 518,
    "grFree; isGradedMap_linearCombination; exists_graded_surjection", D)
src("cube_differential", "IsIsoTermComparisonRestrictScalars.lean", 9, 25,
    "Cube and cubeSign", D)
src("cube_complex", "IsIsoTermComparisonRestrictScalars.lean", 371, 423,
    "cubeComplex; cechComplex and their maps", D)
src("cube_exactness_shift", "IsIsoTermComparisonRestrictScalars.lean", 494, 505,
    "cechComplex_exactAt_succ_iff; cechComplex_exactAt_succ_iff_cube", D)
src("cube_length", "IsIsoTermComparisonRestrictScalars.lean", 547, 559,
    "isZero_cubeComplex_X; isZero_cubeComplex_homology", D)
src("monomial_basis", "ExistsMonomialBasisCechCubePolynomialGrading.lean", 10, 90,
    "Laurent numerator and exact restriction-compatible polynomial monomial bases")
src("monomial_exactness", "CubeComplexExactAtOfMonomialBasis.lean", 12, 71,
    "Cube.above; cubeComplex_above_exactAt; cubeComplex_exactAt_of_monomialBasis")
src("polynomial_finite_exact", "CubeComplexPolyGradingFiniteExact.lean", 11, 44,
    "finite_neg_sum_eq; cubeComplex_polyGrading_finite_exact")
src("polynomial_endpoint", "CubeComplexPolyGradingFiniteExact.lean", 25, 44,
    "cubeComplex_polyGrading_finite_exact")
src("free_finite_exact", "CubeComplexGrFreeFiniteAndExactAt.lean", 9, 33,
    "cubeComplex_grFree_finite_and_exactAt")
src("exactness_transfer", "CubeComplexGradedModuleExactAtOfLargeDegree.lean", 9, 13,
    "exactAt_quot_of_shortExact")
src("large_degree_induction", "CubeComplexGradedModuleExactAtOfLargeDegree.lean", 15, 36,
    "cubeComplex_grCube_exactAt_of_card_lt")
src("large_degree_endpoint", "CubeComplexGradedModuleExactAtOfLargeDegree.lean", 38, 46,
    "cubeComplex_grCube_exactAt_of_finite")
src("finite_saturated_submodule", "ExistsFiniteGradedModuleLineBundleSections.lean", 19, 39,
    "exists_finite_grCube_hom_bijective", A)
src("actual_finite_graded_module", "ExistsFiniteGradedModuleLineBundleSections.lean", 41, 59,
    "exists_finite_graded_module_secCube", A)
src("actual_finite_graded_interface", "ExistsFiniteGradedModuleLineBundleSectionsStatement.lean", 1, 12,
    "GlobalTheory.T.exists_finite_gradedModule_lineBundleSections", A)
src("section_cocycle_definitions", "CechHOneVanishesOnOpenOfIsAffineOpen.lean", 13, 25,
    "IsCocycle; IsCoboundary; CechHOneVanishesOnOpen", A)
src("refinement_descent", "CechHOneVanishesOnOpenOfIsAffineOpen.lean", 32, 62,
    "isCoboundary_of_refine", A)
src("coordinate_equivalence", "CechHOneVanishesOnOpenOfIsAffineOpen.lean", 64, 103,
    "h1Zero_iff", A)
src("cover_locality", "CechHOneVanishesOnOpenOfIsAffineOpen.lean", 105, 164,
    "cechHOneVanishesOnOpen_of_cover", A)
src("affine_extend_kill", "CechHOneVanishesOnOpenOfIsAffineOpen.lean", 166, 200,
    "exists_extend; exists_kill, with all larger exponents", A)
src("affine_all_cover", "CechHOneVanishesOnOpenOfIsAffineOpen.lean", 202, 268,
    "cechHOneVanishesOnOpen_of_isAffineOpen", A)
src("ordered_cocycle", "CechHOneVanishesOnOpenOfIsAffineOpen.lean", 270, 284,
    "add_eq_of_ordered", A)
src("original_differential_signs", "CechHOneVanishesOnOpenOfIsAffineOpen.lean", 360, 398,
    "restrict_d_one; restrict_d_two; IsCocycle.diag; IsCocycle.swap", A)
src("exact_to_coboundary", "CechHOneVanishesOnOpenOfIsAffineOpen.lean", 400, 438,
    "isCoboundary_of_exactAt", A)
src("coboundary_to_exact", "CechHOneVanishesOnOpenOfIsAffineOpen.lean", 440, 493,
    "exactAt_of_isCoboundary", A)
src("all_cover_from_exact", "CechHOneVanishesOnOpenOfIsAffineOpen.lean", 584, 600,
    "exactAt_one_of_h1ZeroOn; h1ZeroOn_of_exactAt_one; h1Zero_of_exactAt_one", A)
src("exact_secCube_endpoint", "FirstCohomologyVanishesOfExactSecCube.lean", 14, 19,
    "firstCohomologyVanishes_of_exact_secCube")
src("literal_geometric_inputs", "FirstCohomologyVanishesSpecOfIsLocalRing.lean", 13, 42,
    "pw; tw; VeryAmpleBy; IsProjBy; exact FirstCohomologyVanishes", L)
src("serre_h1_endpoint", "SerreVanishingH1Twist.lean", 16, 28,
    "exists_h1Zero_tw_of_veryAmpleBy")
src("serre_h1_interface", "SerreVanishingH1TwistStatement.lean", 11, 12,
    "GlobalTheory.T.serre_vanishing_h1_twist")
src("saturation_high_degree", "MemSpanOfSaturatingOfLe.lean", 9, 39,
    "mem_span_of_saturating_of_le")
src("cyclic_chart_saturation", "ExistsHomogeneousFormEqHighPowerSection.lean", 19, 59,
    "exists_X_pow_smul_mem_span_of_dehomogenisation")
src("actual_no_common_torsion", "ExistsHomogeneousFormEqHighPowerSection.lean", 72, 101,
    "restrict_eq_zero_of_X_pow_smul; grSum_eq_zero_of_X_pow_smul")
src("actual_constant_section", "ExistsHomogeneousFormEqHighPowerSection.lean", 103, 132,
    "twZeroTrivEquiv; constant-one coordinates; twTrivOfSec")
src("polynomial_endpoint_actual", "ExistsHomogeneousFormEqHighPowerSection.lean", 134, 166,
    "exists_form_eq_sec_pw")
src("polynomial_interface", "ExistsHomogeneousFormEqHighPowerSectionStatement.lean", 11, 12,
    "GlobalTheory.T.exists_homogeneousForm_eq_highPowerSection")
src("serre_conjunction", "SerreVanishingVeryAmple.lean", 14, 17,
    "serre_h1Zero_and_sections_polynomial", A)
src("serre_conjunction_interface", "SerreVanishingVeryAmpleStatement.lean", 10, 11,
    "GlobalTheory.T.serre_vanishing_very_ample", A)
src("positive_power_consumer", "FirstCohomologyVanishesDescent.lean", 123, 228,
    "original multiplication-power comparison and first_cohomology_vanishes_powers", A)

previous = json.loads((WORK/"actual_section_localization_v54/contracts.json").read_text())
retained = [dict(x) for x in previous["remaining_global_producers"] if x["id"] != "GSL_SERRE"]
completed_serre_input = next(dict(x) for x in previous["remaining_global_producers"] if x["id"] == "GSL_SERRE")
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
    sources[key] = dict(id="SHV_SRC_"+key.upper(), path=path, declaration=declaration,
        line_start=lo, line_end=hi, source_commit=PIN, file_sha256=row["sha256"],
        full_file_sha256=row["sha256"], range_sha256=sha(part), range_bytes=len(part),
        snapshot_file=row["snapshot_file"], verified_equal_to_pinned_git_blob=True,
        url=row["url"]+f"#L{lo}-L{hi}")
for inp in retained:
    inp["sources"] = [sources["retained_"+inp["id"].lower()+"_"+str(j)]
                      for j in range(len(inp.get("sources", [])))]
    inp["globally_discharged_by_this_component"] = False
    inp["boundary_inherited_from"] = "actual_section_localization_v54/contracts.json"

specs = [
("SHV1", [], ["homogeneous_localization","homogeneous_maps","graded_short_exact","homloc_short_exact_theorem"],
 "Exact original graded localization and short exact complexes.",
 "The vertex theorem permits an arbitrary variable set and finite I; no flatness of an unrelated coefficient change is assumed."),
("SHV2", [], ["monomial_basis","monomial_exactness","polynomial_finite_exact"],
 "Laurent-monomial contraction and the full positive-degree polynomial calculation.",
 "Arbitrary commutative R including zero divisors; every integer degree; finite free surviving top cohomology and exactness in all degrees at t>=1, including an empty variable set."),
("SHV3", ["SHV2"], ["free_finite_exact"],
 "A single explicit bound for every shift and cohomological degree of a finite graded free module.",
 "The source bound 1+sum |d_l| is fixed before the degree and cohomological index; zero rank and negative shifts are allowed."),
("SHV4", [], ["graded_surjection","large_degree_induction"],
 "A finite list of original homogeneous syzygies over a Noetherian polynomial ring.",
 "Any prescribed finite length; no claim that the last kernel vanishes or is projective, and no finite global-dimension premise."),
("SHV5", [], ["exactness_transfer"],
 "Exactness transfer through the actual short exact sequence of cochain complexes.",
 "Includes degree zero, with negative terms interpreted as zero; proof is an explicit cycle lift and boundary correction."),
("SHV6", ["SHV1","SHV3","SHV4","SHV5"], ["large_degree_induction","large_degree_endpoint","cube_length"],
 "Full original uniform large-degree exactness for every finite graded module.",
 "One finite list of nu+1 free presentations and one maximum before every integer t and every cohomological degree."),
("SHV7", ["FCD10"], ["finite_saturated_submodule","homogeneous_maps"],
 "The original one finite homogeneous submodule with every nonempty localization bijective.",
 "Arbitrary R; one K before all degrees; the general given-submodule power-saturation criterion is also proved; no empty-vertex isomorphism asserted."),
("SHV8", ["SHV7","FCD13","ASL8","ASL9","ASL12","ASL14","ASL16"], ["actual_finite_graded_module","actual_finite_graded_interface","graded_cube"],
 "Full original finite graded module for every actual section-cube degree.",
 "Arbitrary R, original f,H,M,s_i, original scalar map and restrictions; no smoothness or Noetherianity for this model."),
("SHV9", ["SHV6","SHV8"], ["serre_h1_endpoint","cube_exactness_shift"],
 "Uniform positive-degree exactness of the actual prescribed-cover section complex.",
 "Noetherian R; every positive cohomological degree at one twist threshold; augmented degree two is ordinary degree one."),
("SHV10", [], ["section_cocycle_definitions","refinement_descent"],
 "A primitive on a refinement descends to the original cover.",
 "Arbitrary cover index sets and actual line-bundle sections; no affine, separatedness or finite-cover premise."),
("SHV11", ["SHV10"], ["coordinate_equivalence","literal_geometric_inputs"],
 "Exact equivalence with the original all-cover coordinate predicate.",
 "Every original chart assignment and transition unit, all smaller opens and arbitrary index sets; both directions are proved."),
("SHV12", ["ASL15"], ["affine_extend_kill","affine_all_cover"],
 "Two finite denominator exponents correct a principal-cover cocycle.",
 "N clears pairwise denominators, K kills triple discrepancies on whole pairwise overlaps; arbitrary ring and actual restrictions."),
("SHV13", ["SHV10","SHV12"], ["affine_all_cover"],
 "Full original all-cover first-cohomology vanishing on every affine open.",
 "No Noetherian hypothesis; finite principal refinement of an arbitrary cover, explicit unit-ideal powers and descent to that original cover."),
("SHV14", [], ["cover_locality"],
 "The original local-to-global all-cover cocycle argument.",
 "Arbitrary index sets; pairwise overlaps need not be affine or quasi-compact; corrected local primitives glue on the original test cover."),
("SHV15", [], ["ordered_cocycle","original_differential_signs","exact_to_coboundary","coboundary_to_exact"],
 "Exact original ordered differential and cocycle/coboundary equivalence.",
 "Finite or infinite linearly ordered index sets; the source differential u_j-u_i requires primitive psi_i=-u_i."),
("SHV16", ["SHV11","SHV13","SHV14","SHV15"], ["all_cover_from_exact","exact_secCube_endpoint"],
 "Full original reverse implication from affine-cover exactness to coordinate vanishing.",
 "Every original all-cover coordinate test follows from exactness on the supplied affine cover; no unproved sheaf-cohomology comparison remains."),
("SHV17", ["SHV9","SHV16","ASL2"], ["serre_h1_endpoint","serre_h1_interface","literal_geometric_inputs"],
 "Full original exists_h1Zero_tw_of_veryAmpleBy.",
 "Every Noetherian commutative R, actual f,H,s and arbitrary actual M; one integer bound before all integer twists and all covers/cocycles; no smoothness."),
("SHV18", ["SHV6","SHV7"], ["saturation_high_degree","graded_augmentation"],
 "Full original sufficiently high homogeneous membership in a saturated finite span.",
 "The ambient graded module need not be finite; retains both separate chart saturation and no common chart-power torsion hypotheses."),
("SHV19", ["ASL2","ASL8"], ["actual_no_common_torsion"],
 "No common chart-power torsion in the actual graded line-bundle sections.",
 "Original cover by D(s_i), arbitrary R and actual M,H; cancellation only where the section is a unit."),
("SHV20", [], ["cyclic_chart_saturation"],
 "Full original cyclic-chart dehomogenization saturation theorem.",
 "Arbitrary variable set and arbitrary containing submodule; no finiteness, Noetherianity or added epsilon-surjectivity premise."),
("SHV21", ["SHV17","SHV18","SHV19","SHV20","ASL2","ASL8","ASL14"],
 ["actual_constant_section","polynomial_endpoint_actual","polynomial_interface","serre_conjunction","serre_conjunction_interface"],
 "Full original homogeneous-polynomial high-power sections and both Serre conjuncts.",
 "One natural threshold before t and every actual section sigma; one degree-t polynomial evaluated in every original chart with the original scalar map; the H1 bound separately may depend on M.")
]
lines = proof.splitlines(keepends=True)
claims = []
for ident, deps, groups, title, scope in specs:
    lo = next(i for i,l in enumerate(lines) if l.strip() == ("% BEGIN "+ident).encode())
    hi = next(i for i,l in enumerate(lines) if l.strip() == ("% END "+ident).encode())
    block = b"".join(lines[lo:hi+1])
    claims.append(dict(id=ident, title=title, introduced_in="0.55", classification="B",
        depends_on=deps, external_input_ids=["SHV_STANDARD"], scope_note=scope,
        source_groups=groups, sources=[sources[g] for g in groups],
        proof_location=dict(file=COMP+"/main.tex", label="claim:"+ident,
            line_start=lo+1,line_end=hi+1,sha256=sha(block),bytes=len(block)),
        proof_status="complete at the stated original mathematical hypotheses",
        status="complete human proof; pending independent review",
        scope_class="complete_at_original_mathematical_hypotheses",
        source_proof_is_not_human_proof=True))

inherited = []
uses = [
("flat_chart_descent_v53","FCD10","dependency","Finite homogeneous chart-saturating generators in SHV7."),
("flat_chart_descent_v53","FCD13","dependency","The exact dehomogenization quotient used in SHV8."),
("flat_chart_descent_v53","FCD15","background_only","Its explicit free Laurent-monomial calculation is recalled and reproved in SHV2 to add a uniform positive-degree bound over arbitrary R; the Noetherian finite-module conclusion of FCD15 is not assumed for SHV2."),
("actual_section_localization_v54","ASL2","dependency","Actual integer twists, chart units and the canonical zero-twist identification."),
("actual_section_localization_v54","ASL8","dependency","Actual graded polynomial action and its coordinate evaluation."),
("actual_section_localization_v54","ASL9","dependency","The original VeryAmpleBy cover and its actual affine intersections."),
("actual_section_localization_v54","ASL12","dependency","All-degree actual graded-section cube with its exact restriction maps."),
("actual_section_localization_v54","ASL14","dependency","Full actual chart dehomogenization, every ratio family and homogeneous power-kernel."),
("actual_section_localization_v54","ASL15","dependency","Actual ordinary section extension and power-killing on affine principal opens."),
("actual_section_localization_v54","ASL16","dependency","Finite projectivity of actual affine line-bundle sections."),
("global_section_laws_v52","GSL17","next_consumer","The reviewed positive-power vanishing implication now consumes the proved Serre H1 input; its other original geometric inputs remain.")
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
("SHV2","polynomial_endpoint","Finite cohomology and full exactness at every positive polynomial degree, over arbitrary R."),
("SHV3","free_finite_exact","Full original free-module finite/exact statement with its common shift bound."),
("SHV5","exactness_transfer","Original exactness transfer through a termwise short exact sequence."),
("SHV6","large_degree_endpoint","One large-degree threshold for every cohomological degree of any finite graded module over Noetherian R."),
("SHV7","finite_saturated_submodule","One finite homogeneous K before all degrees; actual inclusion bijective at every nonempty homogeneous localization."),
("SHV8","actual_finite_graded_module","One actual finite graded section-cube model over arbitrary R, before all integer twists."),
("SHV10","refinement_descent","An actual cocycle primitive descends from a covering refinement to every original cover member."),
("SHV11","coordinate_equivalence","Both directions of the exact original coordinate/section all-cover equivalence."),
("SHV13","affine_all_cover","Every section cocycle on every cover of every affine open is an actual coboundary."),
("SHV14","cover_locality","The full original cover-local all-cover vanishing construction."),
("SHV15","exact_to_coboundary","The original ordered exactness-to-coboundary implication, with its negative primitive convention."),
("SHV15","coboundary_to_exact","The original reverse ordered cocycle-to-exactness implication."),
("SHV16","exact_secCube_endpoint","Full original firstCohomologyVanishes_of_exact_secCube."),
("SHV17","serre_h1_endpoint","Full original Serre H1 supplier at arbitrary Noetherian R, with no smoothness."),
("SHV17","serre_h1_interface","Exact exported original Serre H1 interface."),
("SHV18","saturation_high_degree","Full original mem_span_of_saturating_of_le, without finite ambient G."),
("SHV20","cyclic_chart_saturation","Full original cyclic dehomogenization saturation, including arbitrary variables and arbitrary containing K."),
("SHV21","polynomial_endpoint_actual","Full original exists_form_eq_sec_pw with the actual all-chart polynomial equation."),
("SHV21","polynomial_interface","Exact exported original homogeneous-form interface."),
("SHV21","serre_conjunction","Both original Serre conjuncts, with their distinct bound quantifiers.")
]:
    h=header(key)
    endpoints.append(dict(claim_id=ident, source=sources[key],
        exact_source_declaration_header=h, declaration_header_sha256=sha(h.encode()),
        output=output, status="complete at all original hypotheses; no newly assumed opaque producer"))

standard = dict(id="SHV_STANDARD", name="Ordinary graded-module, scheme and sheaf foundations",
    kind="standard_background_not_a_selected_project_gap",
    scope_note=("Commutative rings and polynomial monomial bases; elementary module localization and direct-sum gradings; "
        "Hilbert's basis theorem and the Noetherian finite-submodule property; affine principal-open basis and compactness; "
        "the sheaf gluing/equality axioms and original line-bundle chart identifications. "
        "All particular uniform bounds, section-cocycle primitives, change-of-cover maps and Serre conclusions are proved here."),
    sources=[sources["graded_surjection"],sources["literal_geometric_inputs"]],
    globally_discharged_by_this_component=False)
completed_serre_input["supplied_by"]=["SHV17"]
completed_serre_input["status"]="fully supplied at its exact original all-cover H1 scope"
completed_serre_input["globally_discharged_by_this_component"]=True
completed_serre_input["sources"]=[sources["serre_h1_endpoint"],sources["serre_h1_interface"],sources["serre_conjunction"]]
guards = [
 "The Serre endpoints assume precisely Noetherian R and original VeryAmpleBy data; no smoothness, reducedness, integrality or field hypothesis is added.",
 "SHV8's single finite homogeneous module exists over arbitrary R and is fixed before all integer twists; nonempty vertices are bijective, and the empty vertex is only the actual inclusion in small degrees.",
 "SHV6 chooses nu+1 finite graded free presentations and one maximum before every integer degree and cohomological index; the last syzygy is not assumed projective or zero.",
 "The original augmented degree two is ordinary Cech degree one, and the original ordered differential u_j-u_i is converted to primitives by psi_i=-u_i.",
 "SHV12 uses a first exponent to extend coordinates and a second to kill discrepancies on the whole pairwise overlap; no cancellation across zero divisors occurs.",
 "SHV13 and SHV16 preserve arbitrary cover index sets and return primitives on the original cover, not just a refinement.",
 "FirstCohomologyVanishes retains every original chart assignment, all transition units and all smaller-open restriction identities.",
 "SHV18 does not assume the ambient graded module finite; it preserves both separate saturation and no-common-chart-power-torsion premises.",
 "SHV20 permits an arbitrary polynomial variable set and arbitrary containing submodule; it does not add epsilon surjectivity.",
 "SHV21's one natural bound precedes both the degree t and every section sigma; one homogeneous polynomial works on every original H-chart with the original scalar map.",
 "The H1 bound may depend on M; the polynomial bound uses the fixed trivial-bundle graded construction for f,H,s.",
 "Both original Serre conjuncts are supplied, including GSL_SERRE, but full positive-power abelian vanishing, global section base-change/twist laws, Moduli and whole RH/GRH selected obligations are not thereby supplied."
]
scope = dict(full_original_serre_h1_supplied=True,
    full_original_high_power_polynomial_supplied=True,
    full_original_serre_conjunction_supplied=True,
    full_original_finite_graded_actual_section_model_supplied=True,
    full_original_large_degree_localization_exactness_supplied=True,
    full_original_affine_all_cover_h1_supplied=True,
    full_original_reverse_cover_comparison_supplied=True,
    no_smoothness_added=True, arbitrary_cover_indices_preserved=True,
    one_finite_module_before_all_degrees=True, one_bound_before_all_twists_and_cocycles=True,
    original_actual_sections_and_scalar_maps_preserved=True,
    global_positive_power_abelian_vanishing_unconditionally_supplied=False,
    global_section_laws_unconditionally_supplied=False,
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
    formerly_retained_producers_now_supplied=[completed_serre_input],
    remaining_global_producers=retained,independent_reviews=[]))
write("inherited_inputs.json",dict(schema="rh-inherited-inputs/1",**base,inputs=inherited))
write("retained_foundations.json",dict(schema="rh-retained-foundations/1",**base,
    inputs=[standard],remaining_global_producers=retained,
    scope_note="No unsupplied original geometric producer is a hypothesis of SHV17 or SHV21. These retained producers are independent inputs to later abelian section-law arguments."))
write("explicit_inputs.json",dict(schema="rh-explicit-inputs/1",**base,inputs=[standard],
    inherited_human_proofs=inherited,original_pointwise_interfaces=endpoints,
    remaining_global_producers=retained))
write("closure.json",dict(schema="rh-component-closure/1",**base,**scope,new_claim_count=len(claims),
    completed=[x["output"] for x in endpoints],
    completed_original_endpoint_claim_ids=sorted({x["claim_id"] for x in endpoints},key=lambda s:int(s[3:])),
    formerly_retained_producers_now_supplied=[completed_serre_input],
    globally_supplied_laws=["original Serre all-cover H1","original high-power homogeneous-polynomial sections","both original Serre conjuncts"],
    pending_actual_geometric_producers=[x["id"] for x in retained],
    selected_obligation_statuses_unchanged=True,earlier_proof_components_modified=[],
    graph_nodes_added=0,graph_edges_added=0,independent_reviews=[]))
write("hashes.json",dict(schema="rh-component-hashes/1",**base,
    proof_blocks={x["id"]:x["proof_location"]["sha256"] for x in claims},
    primary_source_files={x["path"]:x["sha256"] for x in files.values()},
    inherited_proof_blocks={x["id"]:x["proof_block_sha256"] for x in inherited}))
print(json.dumps(dict(component=COMP,proof_sha256=sha(proof),claims=len(claims),
    primary_files=len(files),source_ranges=len(sources),inherited_bindings=len(inherited)),indent=2))
