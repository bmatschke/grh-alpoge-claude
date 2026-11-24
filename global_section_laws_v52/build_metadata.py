#!/usr/bin/env python3
"""Pin GSL source ranges, proof blocks and exact conditional contracts.

This script reads but never modifies earlier proof components or formal source.
It performs no Lean replay.  Source snapshots are contained in this component.
"""
from pathlib import Path
import argparse
import hashlib
import json
import re
import subprocess

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
PIN = "7cbf7a0c32fca1badf05931879a37c3f8a2b03b4"
VERSION = "0.52"
COMPONENT = HERE.name
REPOSITORY = "https://github.com/CocoSgt/riemann-hypothesis-lean"
A = "src/Development/AbelianVarietyTheory/Proofs/AbelianSchemeLawProofs/"
C = "src/Development/AbelianVarietyTheory/Proofs/CoherentCohomologyProofs/"
D = "src/Development/AbelianVarietyTheory/Definitions/AbelianSchemeLaws/"
E = "src/ReciprocityTheory/ReductiveGroups/ArithmeticGeometry/ExtensionDescent/"

parser = argparse.ArgumentParser()
parser.add_argument("--repo", type=Path, required=True)
args = parser.parse_args()
repo = args.repo.resolve()

def sha(b):
    return hashlib.sha256(b).hexdigest()

def write_json(name, data):
    (HERE / name).write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n")

FILES = {
    "definitions": D + "FirstCohomologyVanishesSpecOfIsLocalRing.lean",
    "pol": E + "NonzeroLocus.lean",
    "global_defs": E + "GlobalSectionsRankAlgClosed.lean",
    "any_defs": E + "SecBaseChangeAnySt.lean",
    "bc": A + "SecBaseChangeOfPerf.lean",
    "matrix": A + "ExistsMulEqSmulOneOfMulVecInjective.lean",
    "proj_matrix": C + "ExistsMatricesOfProjectiveComplex.lean",
    "flat_complex": C + "ExistsFiniteProjectiveComplexQuasiIso.lean",
    "cube_transfer": C + "ExistsFiniteProjectiveComplexOfNoetherianModel.lean",
    "cech": C + "ThreeTermComplexOfProjectiveCechModel.lean",
    "affine": C + "VeryAmpleCompactQuasiSeparatedAffineCharts.lean",
    "perf_geom": A + "NonemptyPerfectSectionsComplexOfSmoothProj.lean",
    "cech_model": C + "ExistsFiniteProjectiveCechComplexLineBundle.lean",
    "noeth_model": C + "DehomogenisingCompOfSaturating.lean",
    "twist": A + "FinrankOfIsSecBasis.lean",
    "h1iso": A + "FirstCohomologyVanishesOfIsoOfIsGen.lean",
    "projectivity": A + "VeryAmpleByOfRelAmple.lean",
    "vanish": A + "FirstCohomologyVanishesDescent.lean",
    "growth": A + "FinrankSectionsLineBundlePowEqPow.lean",
    "geom_sections": A + "SecMInvariantEqBotOrUnivAtGeometricPoint.lean",
    "translate": A + "TwistedPowTranslate.lean",
    "laws": A + "LawsOfH0EqOneClosedFields.lean",
    "serre_statement": A + "SerreVanishingVeryAmpleStatement.lean",
    "serre": A + "SerreVanishingVeryAmple.lean",
    "rank_one": A + "FinrankSectionsPrincipalPolarisationEqOne.lean",
    "integrality": A + "IsIntegralOfSmoothFieldOfConnectedSpace.lean",
    "cube_growth": A + "CubeTheoremAndSectionsFiniteGrowthAbelianVariety.lean",
    "pol_producer": A + "AbelianSchemeLawsWithoutCohomology.lean",
}

blobs = {}
file_records = {}
for key, path in FILES.items():
    blob = subprocess.check_output(["git", "show", PIN + ":" + path], cwd=repo)
    if (repo / path).read_bytes() != blob:
        raise SystemExit("Formal working tree differs from pinned blob: " + path)
    blobs[key] = blob
    destination = HERE / "source_snapshot" / path
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_bytes(blob)
    file_records[key] = {
        "path": path,
        "snapshot_file": str(destination.relative_to(ROOT)),
        "bytes": len(blob),
        "sha256": sha(blob),
        "file_sha256": sha(blob),
        "line_count": len(blob.splitlines()),
        "source_commit": PIN,
        "verified_equal_to_pinned_git_blob": True,
        "url": REPOSITORY + "/blob/" + PIN + "/" + path,
    }

RANGES = {
    "literal_perf": ("definitions", 16, 88, "cst, pw, tw, VeryAmpleBy, IsProjBy, all-cover FirstCohomologyVanishes and every literal Perf field"),
    "literal_pol": ("pol", 15, 75, "Rigidified, Sym, RelAmple, KTriv and original PolAV"),
    "rank_contract": ("global_defs", 19, 22, "GlobalSectionsRankAlgClosed"),
    "bc_contract": ("global_defs", 32, 41, "SecBaseChangeSt with locally Noetherian S and arbitrary affine target R"),
    "pol_bc_contract": ("global_defs", 160, 165, "PolBaseChangeSt: Cartesian record, dimension, all-test multiplication and generated bundle isomorphism"),
    "any_contract": ("any_defs", 16, 25, "SecBaseChangeAnySt with arbitrary S and arbitrary affine target"),
    "twist_contract": ("any_defs", 27, 58, "twistLB, IsSecBasis, IsPullSecLC and complete SecTwistSt"),
    "section_charts": ("bc", 22, 78, "section extensionality, chartIn and chartOut"),
    "section_reps": ("bc", 81, 172, "Rep, uniqueness, finite sums, pullback and actual section/kernel equivalence"),
    "section_basis": ("bc", 181, 287, "affine test objects, actual pullbacks and basis_of_rep"),
    "fiber_vanish": ("bc", 293, 325, "actual power chart comparison and exists_h1Zero"),
    "bc_join": ("bc", 327, 401, "geometric point and full original secBaseChange_of_perf"),
    "minor": ("matrix", 9, 53, "exists_mul_eq_smul_one_of_mulVec_injective"),
    "certificate": ("matrix", 55, 156, "exists_kernel_certificate with D0B=0, CB=rI, BC+HD0=rI"),
    "universal_kernel": ("matrix", 158, 181, "exists_matrix_basis_ker_of_exact_at_point over every target ring"),
    "projective_matrices": ("proj_matrix", 7, 170, "split projective complex, explicit free matrices and universal kernel/exactness comparisons"),
    "flat_cone": ("flat_complex", 14, 244, "flatness of images, explicit augmented cone and arbitrary-module tensor exactness"),
    "free_construction": ("flat_complex", 255, 348, "exists_free_step and descending finite free-complex construction"),
    "universal_projective": ("flat_complex", 403, 622, "cone/quasi-isomorphism equivalence and bounded finite projective model over Noetherian R"),
    "noeth_transfer": ("cube_transfer", 9, 60, "arbitrary-base transfer from exact Noetherian flat cube model"),
    "cech_base_change": ("cech", 24, 98, "actual affine-section Cech base change and coordinate formula"),
    "perf_from_model": ("cech", 106, 156, "perf_of_projective_model: every field of literal Perf"),
    "affine_intersections": ("affine", 24, 50, "finite nonempty intersections of very-ample nonzero loci are affine"),
    "perf_geometry_contract": ("perf_geom", 15, 23, "nonempty_perf_of_smooth_isProjBy, retained global geometric producer"),
    "cech_geometry_contract": ("cech_model", 19, 43, "exists_finite_projective_complex_cechLB, retained geometric producer"),
    "noeth_geometry_contract": ("noeth_model", 44, 114, "exists_noetherian_model_grCube, retained graded-presentation/geometric model producer"),
    "twist_basis_tools": ("twist", 33, 174, "actual coefficient combinations, basis transport and perf_bas"),
    "surjective_lift": ("twist", 176, 216, "perf_lift for a surjective coefficient map and literal LinComb pullback"),
    "basis_rank": ("twist", 218, 256, "Cmb, IsSecBasis and exact finrank of a supplied section basis"),
    "twist_bundle_tools": ("twist", 258, 308, "three-factor generator, power chart map and actual translation inverse"),
    "twisted_fiber": ("twist", 312, 370, "geometric_fibre from arbitrary S, applying local-Noetherian twist law to P'/Spec K"),
    "twist_join": ("twist", 372, 421, "complete secTwist_of_perf including every residue-section lift"),
    "h1_iso": ("h1iso", 129, 224, "all-cover vanishing under an actual generated bundle isomorphism and scheme isomorphism"),
    "projectivity": ("projectivity", 29, 121, "veryAmpleBy_of_relAmple and polAV_veryAmpleBy"),
    "average": ("vanish", 65, 119, "first_cohomology_vanishes_descent by averaging invariant functions"),
    "power_vanish": ("vanish", 123, 228, "actual multiplication-power comparison and first_cohomology_vanishes_powers"),
    "growth_algebra": ("growth", 13, 123, "exact exponent from monotonicity, good square dilation and two-sided growth"),
    "rank_geometric": ("growth", 125, 260, "finite torsion index, section multiplication injectivity and finrank_sections_lineBundlePow_eq_pow"),
    "geometric_section_equiv": ("geom_sections", 222, 243, "actual section linear equivalence"),
    "geometric_base_change": ("geom_sections", 304, 423, "original-data pullback equivalence and full geometric-fiber rank"),
    "twist_translation": ("translate", 23, 121, "global field square generator, iterated square law, finite-surjective root and twisted_pow_translate"),
    "law_assembly": ("laws", 64, 91, "exact original join and its suppliers; wrapper is not treated as a human proof"),
    "serre_input": ("serre_statement", 1, len(blobs["serre_statement"].splitlines()), "exact retained Serre all-cover H1 input, first conjunct"),
    "serre_producer": ("serre", 14, len(blobs["serre"].splitlines()) - 2, "retained Serre producer and its immediate geometric suppliers"),
    "rank_one_input": ("rank_one", 12, 16, "retained principal-polarization h0=1 producer"),
    "integrality_input": ("integrality", 15, len(blobs["integrality"].splitlines()) - 2, "retained smooth geometrically connected to geometrically integral supplier"),
    "growth_input": ("cube_growth", 25, len(blobs["cube_growth"].splitlines()) - 2, "retained cube and actual finite-section/two-sided-growth producers"),
    "pol_input": ("pol_producer", 15, len(blobs["pol_producer"].splitlines()) - 2, "retained polarization base-change producer"),
}

sources = {}
for key, (file_key, start, end, declaration) in RANGES.items():
    lines = blobs[file_key].splitlines(keepends=True)
    if not (1 <= start <= end <= len(lines)):
        raise SystemExit(f"Invalid source range {key}: {start}--{end} of {len(lines)}")
    block = b"".join(lines[start - 1:end])
    fr = file_records[file_key]
    sources[key] = {
        "id": "GSL_SRC_" + key.upper(),
        "path": fr["path"],
        "declaration": declaration,
        "line_start": start,
        "line_end": end,
        "source_commit": PIN,
        "file_sha256": fr["sha256"],
        "full_file_sha256": fr["sha256"],
        "range_sha256": sha(block),
        "range_bytes": len(block),
        "snapshot_file": fr["snapshot_file"],
        "verified_equal_to_pinned_git_blob": True,
        "url": fr["url"] + f"#L{start}-L{end}",
    }

def declaration(file_key, kind, name):
    text = blobs[file_key].decode()
    marker = kind + " " + name
    start = text.index(marker)
    if kind == "theorem":
        depths = {"(": 0, "[": 0, "{": 0}
        close = {")": "(", "]": "[", "}": "{"}
        end = None
        for i in range(start, len(text)):
            char = text[i]
            if text[i:i + 2] == ":=" and not any(depths.values()):
                end = i
                break
            if char in depths:
                depths[char] += 1
            elif char in close:
                depths[close[char]] -= 1
        if end is None:
            raise SystemExit("No theorem assignment: " + name)
    else:
        match = re.search(r"\n\n(?=(?:def |abbrev |theorem |structure |attribute |end ))", text[start:])
        if not match:
            raise SystemExit("No definition end: " + name)
        end = start + match.start()
    return text[start:end].strip()

def theorem_type(file_key, name):
    text = declaration(file_key, "theorem", name)
    marker = "theorem " + name
    rest = text[len(marker):].lstrip()
    if not rest.startswith(":"):
        raise SystemExit("Expected unbound theorem type: " + name)
    return rest[1:].strip()

def outer_arrows(text):
    parts = []
    depths = {"(": 0, "[": 0, "{": 0}
    close = {")": "(", "]": "[", "}": "{"}
    begin = 0
    for i, char in enumerate(text):
        if char in depths:
            depths[char] += 1
        elif char in close:
            depths[close[char]] -= 1
            if min(depths.values()) < 0:
                raise SystemExit("Unbalanced theorem type")
        elif char == "→" and not any(depths.values()):
            parts.append(text[begin:i].strip())
            begin = i + 1
    if any(depths.values()):
        raise SystemExit("Unbalanced theorem type at end")
    parts.append(text[begin:].strip())
    return parts

bc_args = outer_arrows(theorem_type("bc", "secBaseChange_of_perf"))
tw_args = outer_arrows(theorem_type("twist", "secTwist_of_perf"))
van_args = outer_arrows(theorem_type("vanish", "first_cohomology_vanishes_powers"))
rank_args = outer_arrows(theorem_type("growth", "finrank_sections_lineBundlePow_eq_pow"))
tr_args = outer_arrows(theorem_type("translate", "twisted_pow_translate"))
assert len(bc_args) == 8, len(bc_args)
assert len(tw_args) == 9, len(tw_args)
assert len(van_args) >= 7, len(van_args)
assert len(rank_args) == 6, len(rank_args)
assert len(tr_args) >= 3, len(tr_args)

EXTERNAL = [
    ("GSL_STANDARD", "Ordinary algebra and scheme foundations", "foundation",
     "Finite-dimensional linear algebra; sheaf gluing; affine schemes and invertible modules; localization; tensor products and their Tor sequence; finite projectives, flatness and Nakayama; existence of algebraic closures and arbitrarily large primes. Needed steps are explained where used.", [], None),
    ("GSL_PERF_GEOMETRY", "Universal geometric Perf producer", "retained_global_producer",
     "For every arbitrary commutative R, every smooth IsProjBy morphism X -> Spec R and every actual line bundle M, supply Nonempty(Perf f M). GSL5--10 complete its algebra and section realization from the actual section-cube model; global geometric model existence remains pending.",
     ["perf_geometry_contract", "cech_geometry_contract", "noeth_geometry_contract"], bc_args[0]),
    ("GSL_POL_BASE_CHANGE", "PolBaseChangeSt", "retained_global_producer",
     "Every S,S',f,P; actual Cartesian P', same g, all-test multiplication preservation and generated bundle isomorphism. No base Noetherianity restriction.",
     ["pol_bc_contract", "pol_input"], declaration("global_defs", "def", "PolBaseChangeSt")),
    ("GSL_VANISH_CLOSED", "Positive-power all-cover H1 vanishing", "conditional_producer_reduced_in_GSL17",
     "Every algebraically closed field K, original PolAV P/K and n>=1: FirstCohomologyVanishes(pw P.L n). The complete reduction is proved in GSL17; its Serre/multiplication/invariant-function producers remain.",
     ["power_vanish", "fiber_vanish"], bc_args[2]),
    ("GSL_RANK_CLOSED", "GlobalSectionsRankAlgClosed", "conditional_producer_reduced_in_GSL19",
     "Every algebraically closed K, original P/K and n>=1: literal SecM has finrank n^P.g. The complete reduction is proved in GSL19; initial rank-one, decomposition, growth and integrality producers remain.",
     ["rank_contract", "rank_geometric"], declaration("global_defs", "def", "GlobalSectionsRankAlgClosed")),
    ("GSL_TWIST_GEOMETRIC", "Original geometric translated-power supplier", "conditional_producer_reduced_in_GSL21",
     "Every locally Noetherian S, P/S, algebraically closed K-point, q>=1 and c: qth root d and actual generated LinComb with maps snd/translPt c/translPt d and exponents q-1,1,-q. Its exact locally Noetherian scope suffices through GSL22 over arbitrary original S.",
     ["twist_translation", "twisted_fiber"], tw_args[7]),
    ("GSL_SERRE", "Original Serre all-cover H1 input", "retained_upstream_producer",
     "Every Noetherian base ring R, actual VeryAmpleBy H and every actual line bundle M: all integer twists t>=t0 have FirstCohomologyVanishes. The sections-polynomial conjunct is not assumed or proved for GSL17.",
     ["serre_input", "serre_producer", "power_vanish"], van_args[1]),
    ("GSL_MUL_PULL", "Actual global multiplication-power generator", "retained_upstream_producer",
     "Every S,P,n: actual generated LinComb for L^(n^2)/[n]^*L, including the exact maps and exponents.",
     ["power_vanish", "law_assembly"], van_args[3]),
    ("GSL_MUL_GEOMETRY", "Finite-flat-surjective multiplication geometry", "retained_upstream_producer",
     "Every locally Noetherian S,P,n>=1: [n] finite, flat, surjective, etale if n is a unit on the base.",
     ["power_vanish", "twist_translation", "law_assembly"], van_args[4]),
    ("GSL_TORSION_DESCENT", "Every-open torsion-invariant function descent", "retained_upstream_producer",
     "For every algebraically closed K, P/K and n nonzero in K, every invariant actual function on [n]^{-1}U has exactly one preimage on U, for every open U.",
     ["power_vanish", "law_assembly"], van_args[5]),
    ("GSL_GEOM_INTEGRAL", "Smooth geometric-connectedness integral-fiber supplier", "retained_upstream_producer",
     "Original universal implication Smooth f and GeometricallyConnected f -> GeometricallyIntegral f; GSL19 uses its original P/K fiber instance.",
     ["integrality_input", "rank_geometric"], rank_args[0]),
    ("GSL_RANK_ONE", "Original principal-polarization rank-one input", "retained_upstream_producer",
     "Every algebraically closed K and original PolAV P/K has finrank(SecM P.A P.L 1)=1. Full KTriv and actual line bundle remain part of P.",
     ["rank_one_input", "rank_geometric"], rank_args[1]),
    ("GSL_SECTION_DECOMP", "Actual torsion-indexed section decomposition", "retained_upstream_producer",
     "Every algebraically closed K,P, n nonzero in K,j>=1: actual coefficient-linear equivalence of SecM(n^2*j) with all functions A[n](K) -> SecM(j). No cardinality formula is separately assumed.",
     ["rank_geometric", "law_assembly"], rank_args[2]),
    ("GSL_FINITE_GROWTH", "Actual finite sections and two-sided dimension growth", "retained_upstream_producer",
     "Every algebraically closed K,P: all nonnegative powers have finite section modules; some N,c,C with N,c>=1 bound h0(Nt) above and below by t^P.g for all t>=1.",
     ["rank_geometric", "growth_input"], rank_args[3]),
    ("GSL_SQUARE", "Original local-on-base square generator", "retained_upstream_producer",
     "Every S,P,T,x,y,p: actual generated square LinComb on the inverse image of an open neighborhood of p. No original Noetherian restriction is inserted.",
     ["twist_translation", "law_assembly"], tr_args[0]),
    ("GSL_NOETH_CUBE_DATA", "Supplied original Noetherian cube model data", "pointwise_input_to_complete_conditional_theorem",
     "For a particular finite ordered cube A over arbitrary R: R0 Noetherian, flat nonempty C0 vertices, finite Cech cohomologies, actual base-change map bijective on every nonempty vertex. GSL8 proves its entire source conclusion. Its universal geometric availability is not asserted.",
     ["noeth_transfer", "noeth_geometry_contract"], theorem_type("cube_transfer", "exists_finite_projective_complex_of_noetherian_model")),
    ("GSL_CECH_MODEL_DATA", "Supplied universally valid projective model of the actual section complex", "pointwise_input_to_complete_conditional_theorem",
     "Actual finite affine-intersection cover, actual nonnegative finite-projective complex, actual map to the section Cech complex, quasi-isomorphism after every R-algebra. GSL10 proves every Perf field from exactly these data.",
     ["perf_from_model", "cech_geometry_contract"], theorem_type("cech", "perf_of_projective_model")),
    ("GSL_INHERITED_NFL", "NFL22 supplied-data principal uniformization implication", "inherited_proved_implication",
     "Retain the same Moduli record, actual family/model/frame sections, all HUF/PUN foundations, and every other original-data premise. Only substitute law instances once their geometric producers are supplied.", [], None),
    ("GSL_INHERITED_TDR", "TDR13 literal AllTest supplied-data implication", "inherited_proved_implication",
     "Retain the same Moduli and reduced test-algebra scope. Its original section law may receive GSL23 only at the exact retained premises.", [], None),
]
external_records = []
for ident, name, kind, scope, groups, exact in EXTERNAL:
    item = {
        "id": ident, "name": name, "kind": kind, "scope_note": scope,
        "source_commit": PIN, "sources": [sources[g] for g in groups],
        "globally_discharged_by_this_component": False,
    }
    if exact is not None:
        item["exact_source_statement_text"] = exact
        item["statement_sha256"] = sha(exact.encode())
    external_records.append(item)
external_ids = {x["id"] for x in external_records}

# id, dependencies, source groups, explicit external premises, precise scope
CLAIMS = [
    ("GSL1", [], ["section_charts", "twist_contract"], ["GSL_STANDARD"],
     "Actual LB sections, covers, pullback, linearity and literal LinComb/LPow chart conversions."),
    ("GSL2", [], ["minor"], ["GSL_STANDARD"],
     "Adjugate left inverse at an injective field point over arbitrary R, with empty-rank case."),
    ("GSL3", ["GSL2"], ["certificate"], [],
     "Two-denominator certificate D0B=0, CB=rI, BC+HD0=rI for middle-exact field specialization; arbitrary zero divisors."),
    ("GSL4", ["GSL3"], ["universal_kernel"], [],
     "One chosen kernel basis before every ring map inverting r; local-unit and residue-coordinate lifting."),
    ("GSL5", [], ["projective_matrices"], ["GSL_STANDARD"],
     "Explicit finite free matrices from finite projective three-term complex, all tensor products and actual fixed kernel coordinates."),
    ("GSL6", [], ["free_construction", "universal_projective"], ["GSL_STANDARD"],
     "Bounded nonnegative complex over Noetherian R with finite cohomology: finite model, finite free positive terms, no termwise finiteness of C."),
    ("GSL7", ["GSL6"], ["flat_cone", "universal_projective"], ["GSL_STANDARD"],
     "With flat C terms, finite projective model and arbitrary-module tensor quasi-isomorphism by explicit bounded cone."),
    ("GSL8", ["GSL6", "GSL7"], ["noeth_transfer"], ["GSL_NOETH_CUBE_DATA"],
     "Complete original cube-transfer theorem at supplied Noetherian flat finite-cohomology model; arbitrary R and subsequent target."),
    ("GSL9", ["GSL1"], ["cech_base_change", "literal_perf"], ["GSL_STANDARD"],
     "Actual finite affine-intersection section Cech complex commutes with every ring map; H0 gluing and all-cover H1 exactness."),
    ("GSL10", ["GSL5", "GSL8", "GSL9"], ["perf_from_model", "literal_perf", "affine_intersections", "perf_geometry_contract"], ["GSL_CECH_MODEL_DATA"],
     "Every literal Perf field including fixed coordinate functions, universal actual-section equivalences and H1 exactness; very-ample cover bridge."),
    ("GSL11", ["GSL1"], ["section_reps", "literal_perf"], [],
     "Linearity, uniqueness and naturality forced by the printed Perf.sec coordinates; no naturality assumed of chosen equivalences."),
    ("GSL12", ["GSL3", "GSL4", "GSL11"], ["section_basis", "twist_basis_tools"], [],
     "At supplied Perf and H1-zero geometric point, one family of actual sections becomes a basis after every map inverting r, with rank from the same fiber."),
    ("GSL13", ["GSL1", "GSL11"], ["surjective_lift", "twist_contract"], [],
     "General surjective coefficient-ring map lifts every actual LinComb section from one fixed spanning cycle matrix; exact IsPullSecLC."),
    ("GSL14", ["GSL1"], ["h1_iso", "twist_basis_tools", "geometric_section_equiv"], [],
     "Actual scheme/bundle isomorphisms transport sections, bases and every-cover cocycle vanishing by unit formulas and gluing."),
    ("GSL15", ["GSL14"], ["projectivity", "literal_pol", "pol_bc_contract"], ["GSL_POL_BASE_CHANGE"],
     "Complete original polAV_veryAmpleBy from PolBaseChangeSt, arbitrary original S and affine target R and specified Cartesian model."),
    ("GSL16", [], ["average"], ["GSL_STANDARD"],
     "Finite-group averaging descends all-cover H1 vanishing from the exact every-open invariant-function descent input."),
    ("GSL17", ["GSL14", "GSL15", "GSL16"], ["power_vanish", "serre_input"], ["GSL_POL_BASE_CHANGE", "GSL_SERRE", "GSL_MUL_PULL", "GSL_MUL_GEOMETRY", "GSL_TORSION_DESCENT"],
     "Complete original positive-power vanishing implication, all algebraically closed characteristics; upstream inputs retained."),
    ("GSL18", [], ["growth_algebra"], ["GSL_STANDARD"],
     "Exact h(j)=j^g from original monotonicity, good-square relation and two-sided growth; simplified bounded-gap real squeeze."),
    ("GSL19", ["GSL1", "GSL18"], ["rank_geometric", "rank_contract"], ["GSL_GEOM_INTEGRAL", "GSL_RANK_ONE", "GSL_SECTION_DECOMP", "GSL_FINITE_GROWTH"],
     "Complete original rank-from-growth/decomposition implication for all original P over algebraically closed fields."),
    ("GSL20", ["GSL1", "GSL14"], ["geometric_base_change", "fiber_vanish", "pol_bc_contract"], ["GSL_POL_BASE_CHANGE", "GSL_VANISH_CLOSED", "GSL_RANK_CLOSED"],
     "Full original geometric-fiber rank and H1 from actual PolBaseChangeSt; arbitrary S,T and actual pullback models."),
    ("GSL21", [], ["twist_translation"], ["GSL_SQUARE", "GSL_MUL_GEOMETRY"],
     "Original locally Noetherian geometric twist theorem; finite-surjective qth root and generated square-law iteration, including inseparable q."),
    ("GSL22", ["GSL1", "GSL14", "GSL20"], ["twisted_fiber", "twist_bundle_tools"], ["GSL_POL_BASE_CHANGE", "GSL_TWIST_GEOMETRIC", "GSL_VANISH_CLOSED", "GSL_RANK_CLOSED"],
     "Arbitrary original S: actual Cartesian twisted fiber identified with a pure qth power by inverse translation after PolAV base change to Spec K."),
    ("GSL23", ["GSL1", "GSL3", "GSL4", "GSL11", "GSL12", "GSL14", "GSL15", "GSL20"], ["bc_join", "bc_contract", "any_contract"], ["GSL_PERF_GEOMETRY", "GSL_POL_BASE_CHANGE", "GSL_VANISH_CLOSED", "GSL_RANK_CLOSED"],
     "Both complete original conditional base-change laws: neighborhood and n^g actual sections before every arbitrary target R', t and literal pulled tuple. Global producer inputs remain."),
    ("GSL24", ["GSL3", "GSL4", "GSL11", "GSL15", "GSL22"], ["twist_join", "twist_basis_tools", "basis_rank", "twist_contract"], ["GSL_PERF_GEOMETRY", "GSL_POL_BASE_CHANGE", "GSL_VANISH_CLOSED", "GSL_RANK_CLOSED", "GSL_TWIST_GEOMETRIC"],
     "Complete original local twisted-basis conclusion at retained producers, exact q^g basis of original twistLB; stronger universal subsequent-base-change clause."),
    ("GSL25", ["GSL1", "GSL13", "GSL24"], ["twist_join", "surjective_lift", "twist_contract"], ["GSL_PERF_GEOMETRY", "GSL_POL_BASE_CHANGE", "GSL_VANISH_CLOSED", "GSL_RANK_CLOSED", "GSL_TWIST_GEOMETRIC"],
     "Every literal residue-field LinComb section lifts with exact IsPullSecLC; full SecTwistSt conditional implication, not global producer closure."),
    ("GSL26", ["GSL3", "GSL4", "GSL5", "GSL8", "GSL10", "GSL14", "GSL15", "GSL17", "GSL19", "GSL20", "GSL21", "GSL22", "GSL23", "GSL24", "GSL25", "NFL22", "TDR13"], ["law_assembly", "bc_join", "twist_join", "perf_geometry_contract", "cech_geometry_contract", "noeth_geometry_contract"], ["GSL_PERF_GEOMETRY", "GSL_POL_BASE_CHANGE", "GSL_VANISH_CLOSED", "GSL_RANK_CLOSED", "GSL_TWIST_GEOMETRIC", "GSL_INHERITED_NFL", "GSL_INHERITED_TDR"],
     "Exact conditional law installation into unchanged supplied-data TDR/NFL; global geometric producers, Moduli and inherited HUF/PUN foundations remain. No selected whole closure."),
]

tex = (HERE / "main.tex").read_bytes()
text = tex.decode()
claims = []
for ident, deps, groups, ext, scope in CLAIMS:
    for e in ext:
        assert e in external_ids, e
    start = text.index("% BEGIN " + ident + "\n")
    end = text.index("% END " + ident + "\n", start) + len("% END " + ident + "\n")
    block_text = text[start:end]
    block = block_text.encode()
    title = re.search(r"\\paragraph\{" + ident + r": ([^\n]+)\}", block_text).group(1)
    conditional = bool(set(ext) - {"GSL_STANDARD", "GSL_INHERITED_NFL", "GSL_INHERITED_TDR"})
    claims.append({
        "id": ident, "title": title, "introduced_in": VERSION, "classification": "B",
        "depends_on": deps, "external_input_ids": ext, "scope_note": scope,
        "source_groups": groups, "sources": [sources[g] for g in groups],
        "proof_location": {
            "file": COMPONENT + "/main.tex", "label": "claim:" + ident,
            "line_start": text.count("\n", 0, start) + 1,
            "line_end": text.count("\n", 0, end),
            "sha256": sha(block), "bytes": len(block),
        },
        "proof_status": "complete_at_stated_scope",
        "status": "written_pending_independent_review",
        "scope_class": "complete_original_conditional_implication" if conditional else "complete_at_explicit_mathematical_hypotheses",
        "source_proof_is_not_human_proof": True,
        "independent_review_files": [],
    })
assert len(claims) == 26
assert re.findall(r"^% BEGIN (GSL\d+)$", text, re.M) == [x["id"] for x in claims]

inherited = []
for component, ident, use in [
    ("test_ring_descent_v50", "TDR13", "Only the supplied-Moduli/section-law AllTest implication, unchanged."),
    ("normalized_frame_laws_v51", "NFL22", "Only the same-family supplied-data principal uniformization implication, unchanged."),
]:
    prov = json.loads((ROOT / component / "provenance.json").read_text())
    record = next(c for c in prov["claims"] if c["id"] == ident)
    loc = record["proof_location"]
    data = (ROOT / loc["file"]).read_bytes()
    if sha(data) != prov["proof_file_sha256"]:
        raise SystemExit("Inherited proof changed: " + component)
    block = b"".join(data.splitlines(keepends=True)[loc["line_start"] - 1:loc["line_end"]])
    if sha(block) != loc["sha256"]:
        raise SystemExit("Inherited block changed: " + ident)
    inherited.append({
        "id": ident, "component": component, "title": record["title"],
        "proof_file": loc["file"], "proof_file_sha256": sha(data),
        "proof_block_sha256": sha(block), "proof_location": loc,
        "source_commit": PIN, "use": use,
        "all_original_premises_retained": True,
    })

common = {
    "artifact_version": VERSION, "component": COMPONENT, "source_commit": PIN,
    "proof_file_sha256": sha(tex), "status": "written_pending_independent_review",
}
write_json("source_manifest.json", {
    "schema": "rh-pinned-source-manifest/1", **common,
    "repository": REPOSITORY,
    "snapshot_root": COMPONENT + "/source_snapshot",
    "files": list(file_records.values()), "ranges": list(sources.values()),
    "file_count": len(file_records), "range_count": len(sources),
    "total_bytes": sum(x["bytes"] for x in file_records.values()),
    "all_files_verified_equal_to_pinned_git_blobs": True,
})
write_json("provenance.json", {
    "schema": "rh-human-claim-provenance/1", **common,
    "source_repository": REPOSITORY, "claims": claims,
    "new_claim_count": len(claims),
    "global_section_laws_unconditionally_supplied": False,
})
write_json("inherited_inputs.json", {
    "schema": "rh-inherited-inputs/1", **common, "inputs": inherited,
})
write_json("explicit_inputs.json", {
    "schema": "rh-explicit-inputs/1", **common, "inputs": external_records,
    "global_geometric_producers_are_not_closed": True,
})
write_json("retained_foundations.json", {
    "schema": "rh-retained-foundations/1", **common,
    "inputs": [x for x in external_records if x["kind"] not in
               {"pointwise_input_to_complete_conditional_theorem", "inherited_proved_implication"}],
    "separate_unchanged_boundary": [
        "Actual Moduli existence is not supplied.",
        "All inherited HUF/PUN classical-foundation premises remain.",
        "No common final Bundle or selected uniformization obligation is closed on unsupplied data.",
    ],
})
literal_contracts = []
for name, key, kind, src, claim_ids, prerequisites in [
    ("SecBaseChangeSt", "global_defs", "def", "bc_contract", ["GSL23"],
     ["GSL_PERF_GEOMETRY", "GSL_POL_BASE_CHANGE", "GSL_VANISH_CLOSED", "GSL_RANK_CLOSED"]),
    ("SecBaseChangeAnySt", "any_defs", "def", "any_contract", ["GSL23"],
     ["GSL_PERF_GEOMETRY", "GSL_POL_BASE_CHANGE", "GSL_VANISH_CLOSED", "GSL_RANK_CLOSED"]),
    ("SecTwistSt", "any_defs", "def", "twist_contract", ["GSL24", "GSL25"],
     ["GSL_PERF_GEOMETRY", "GSL_POL_BASE_CHANGE", "GSL_VANISH_CLOSED", "GSL_RANK_CLOSED", "GSL_TWIST_GEOMETRIC"]),
]:
    exact = declaration(key, kind, name)
    literal_contracts.append({
        "name": name,
        "completed_result": "full_original_conditional_implication",
        "global_producer_status": "not_globally_supplied_pending_geometric_producers",
        "claim_ids": claim_ids, "exact_retained_prerequisites": prerequisites,
        "source": sources[src], "exact_definition_text": exact,
        "definition_sha256": sha(exact.encode()),
    })
write_json("contracts.json", {
    "schema": "rh-human-component-contracts/1", **common,
    "claim_ids": [c["id"] for c in claims],
    "completed_original_conditional_laws": literal_contracts,
    "entry_premises_for_full_conditional_join": [
        "GSL_PERF_GEOMETRY", "GSL_POL_BASE_CHANGE", "GSL_VANISH_CLOSED",
        "GSL_RANK_CLOSED", "GSL_TWIST_GEOMETRIC"],
    "proved_geometric_reductions": [
        {"output": "GSL_VANISH_CLOSED", "claim_ids": ["GSL14", "GSL15", "GSL16", "GSL17"],
         "remaining_upstream": ["GSL_POL_BASE_CHANGE", "GSL_SERRE", "GSL_MUL_PULL", "GSL_MUL_GEOMETRY", "GSL_TORSION_DESCENT"]},
        {"output": "GSL_RANK_CLOSED", "claim_ids": ["GSL18", "GSL19"],
         "remaining_upstream": ["GSL_GEOM_INTEGRAL", "GSL_RANK_ONE", "GSL_SECTION_DECOMP", "GSL_FINITE_GROWTH"]},
        {"output": "GSL_TWIST_GEOMETRIC", "claim_ids": ["GSL21", "GSL22"],
         "remaining_upstream": ["GSL_SQUARE", "GSL_MUL_GEOMETRY"]},
        {"output": "GSL_PERF_GEOMETRY", "claim_ids": ["GSL5", "GSL6", "GSL7", "GSL8", "GSL9", "GSL10"],
         "completed_part": "All finite-complex algebra and actual Perf field construction from the original geometric Cech model.",
         "remaining_upstream": ["Universal actual geometric Noetherian section-cube model with flat vertices and finite cohomology, or equivalently the exact retained exists_finite_projective_complex_cechLB producer."]},
    ],
    "quantifier_guards": [
        "SecBaseChangeAnySt: every S,P,n>=1,p; choose V and n^g actual sections before every arbitrary R',t and every literal pulled tuple.",
        "SecBaseChangeSt: locally Noetherian S only; affine target R' remains arbitrary, not assumed flat/reduced/Noetherian.",
        "SecTwistSt: every S,P,q>=1 and every local R,t,c; actual q^g basis and every literal residue LinComb section lift.",
        "Geometric twist supplier keeps its locally Noetherian original scope; apply it to P'/Spec K before returning to arbitrary original S.",
        "No geometric root is lifted to R; the original local twisted sections are constructed by the same kernel matrix.",
        "No global Moduli existence or change of normalized family is asserted.",
    ],
    "inherited_inputs": inherited,
    "external_inputs": external_records,
    "global_section_laws_unconditionally_supplied": False,
    "selected_whole_obligations_closed": [],
})
write_json("closure.json", {
    "schema": "rh-component-closure/1", **common,
    "new_claim_count": 26,
    "completed": [
        "Explicit universal two-denominator kernel certificate and all-target kernel basis.",
        "Finite-projective to free three-term complex, bounded Noetherian flat-complex universal model, and arbitrary-base transfer.",
        "Every literal Perf field from a supplied actual universal Cech model.",
        "Actual section linearity, naturality, all-target bases and surjective-ring-map section lifting.",
        "Original projectivity, H1 descent, power vanishing, rank-growth and geometric twist reductions at their named source inputs.",
        "Full original conditional SecBaseChangeAnySt, SecBaseChangeSt and SecTwistSt implications.",
    ],
    "completed_conditional_endpoint_claim_ids": ["GSL23", "GSL24", "GSL25", "GSL26"],
    "pending_actual_geometric_producers": [
        x["id"] for x in external_records if x["kind"] in
        {"retained_global_producer", "retained_upstream_producer"}],
    "globally_supplied_laws": [],
    "global_section_laws_unconditionally_supplied": False,
    "selected_whole_obligations_closed": [],
    "selected_obligation_statuses_unchanged": True,
    "earlier_proof_components_modified": [],
    "graph_nodes_added": 0, "graph_edges_added": 0,
})

report = f"""GLOBAL SECTION LAWS — VERSION 0.52
Accepted formal source: {REPOSITORY}
Pin: {PIN}
Main proof SHA-256: {sha(tex)}
New claims: GSL1–GSL26 (26); no whole selected closure.

The packet proves the complete ORIGINAL CONDITIONAL implications for
SecBaseChangeAnySt, SecBaseChangeSt and SecTwistSt. It does NOT label any
of these three laws globally supplied while its geometric producer
premises remain pending.

Completed mathematics
---------------------
GSL1–4 gives actual section charts and an explicit certificate
D0 B=0, C B=r I, B C+H D0=r I over the original commutative ring.
One B,r is chosen before EVERY later ring map inverting r. Zero divisors,
nonflat/nonreduced/non-Noetherian targets, empty matrix dimensions and
the zero target ring are allowed.

GSL5–10 constructs finite free matrices from three finite projectives,
builds a bounded finite-projective complex for a Noetherian flat complex
with finite cohomology, proves its quasi-isomorphism survives tensoring
with ANY module, and transfers through the exact Noetherian cube model
to arbitrary R. On the actual affine section cover this supplies every
literal Perf field, including fixed coordinate functions and all-target
section equivalences. The universal geometric existence of this Cech
model is still pending.

GSL11–15 proves forced linearity/naturality of Perf section coordinates,
one local actual-section basis valid on every affine test, all-section
lifting through a surjective coefficient map, all-cover H1 and basis
transport, and actual VeryAmpleBy from PolBaseChangeSt.

GSL16–22 proves the exact finite-group H1 averaging argument; original
positive-power vanishing from Serre/multiplication/descent inputs; the
exact exponent h(j)=j^g from good-square dilation and two-sided growth;
the original geometric rank and fiber transport; the generated geometric
twist from a qth root and square law; and its actual inverse-translation
comparison after polarization base change. The geometric twist input is
used only on the Noetherian base Spec K, so original S remains arbitrary.

GSL23 chooses the neighborhood and n^g basis BEFORE every target ring,
map and tuple of actual pulled sections. GSL24 supplies the q^g basis on
the ORIGINAL twisted line bundle over every local R. GSL25 lifts EVERY
literal residue LinComb section using the same matrix and gives exact
IsPullSecLC. No geometric root is lifted to R. GSL26 installs these
conditional laws into unchanged TDR/NFL implications at the same data.

Retained producer boundary
--------------------------
The full conditional join retains exactly: universal geometric Perf;
PolBaseChangeSt; positive-power H1 over all algebraically closed fields;
GlobalSectionsRankAlgClosed; and the original geometric translated-power
generator at its locally Noetherian scope. Their exact source types,
complete proved reductions, and remaining geometric suppliers are in
contracts.json and explicit_inputs.json. Upstream work still includes
the geometric Noetherian section-cube model, polarization base change,
Serre/multiplication/torsion-invariant descent, initial principal h0=1,
actual torsion section decomposition, finite/two-sided growth, geometric
integrality and the square generator. The separate Moduli record and
inherited HUF/PUN foundations remain. No unsupplied common Bundle,
IsUnf or selected RH/GRH leaf is declared closed.

Evidence and verification
-------------------------
All {len(file_records)} full source snapshots and {len(sources)} cited ranges are checked against
the pinned git blobs; snapshots total {sum(x['bytes'] for x in file_records.values())} bytes.
Every numbered proof block has a root-relative location, exact byte
count and SHA-256. TDR13 and NFL22 are inherited with verified complete
file and block hashes; no earlier file was modified.
Draft TeX is validated separately in tex_validation.json (two passes,
no PDF). No Lean replay is performed. Independent mathematical review
is pending; the reviewer should bind its findings to the frozen main
and all 26 numbered proof blocks.
"""
(HERE / "report.txt").write_text(report)
hash_names = [
    "main.tex", "build_metadata.py", "validate_tex.py", "provenance.json",
    "source_manifest.json", "contracts.json", "closure.json",
    "explicit_inputs.json", "retained_foundations.json",
    "inherited_inputs.json", "report.txt", "tex_validation.json",
]
write_json("hashes.json", {
    "schema": "rh-component-file-hashes/1", **common,
    "files": [{"file": COMPONENT + "/" + name,
               "sha256": sha((HERE / name).read_bytes()),
               "bytes": (HERE / name).stat().st_size}
              for name in hash_names if (HERE / name).exists()],
})
print(json.dumps({
    "component": COMPONENT, "claims": len(claims), "main_sha256": sha(tex),
    "source_files": len(file_records), "source_ranges": len(sources),
    "source_bytes": sum(x["bytes"] for x in file_records.values()),
    "inherited_blocks": len(inherited),
    "global_section_laws_unconditionally_supplied": False,
}, indent=2))
