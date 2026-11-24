#!/usr/bin/env python3
"""Build exact pinned source and human-proof provenance for FP1--FP8."""
from pathlib import Path
import argparse
import hashlib
import json
import re
import subprocess

HERE = Path(__file__).resolve().parent
parser = argparse.ArgumentParser()
parser.add_argument("--repo", type=Path, default=HERE.parents[1] / "lean-source")
REPO = parser.parse_args().repo
PIN = "7cbf7a0c32fca1badf05931879a37c3f8a2b03b4"
BASE = "src/Development/AutomorphicArithmetic/AutomorphicVarieties/CommutativeAlgebra/"
cache = {}


def sha(data):
    return hashlib.sha256(data).hexdigest()


def source(file, spelling, role="matched definition or complete source producer"):
    path = BASE + file + ".lean"
    raw = (REPO / path).read_bytes()
    lines = raw.splitlines(keepends=True)
    starts = []
    pattern = (r"^(?:(?:private|protected|noncomputable)\s+)*"
               r"(?:def|abbrev|theorem|lemma|structure|class|instance)\s+([^\s:{(]+)")
    for i, line in enumerate(lines, 1):
        match = re.match(pattern, line.decode())
        if match:
            starts.append((i, match.group(1)))
    matches = [(i, name) for i, name in starts
               if name == spelling or name.endswith("." + spelling)]
    if len(matches) != 1:
        raise ValueError((path, spelling, matches))
    start, actual = matches[0]
    end = min([i for i, _ in starts if i > start] or [len(lines) + 1]) - 1
    while end > start and not lines[end - 1].strip():
        end -= 1
    block = b"".join(lines[start - 1:end])
    if path not in cache:
        pinned = subprocess.check_output(["git", "-C", str(REPO), "show", PIN + ":" + path])
        if raw != pinned:
            raise ValueError("Pinned blob mismatch: " + path)
        cache[path] = {
            "path": path, "sha256": sha(raw), "bytes": len(raw),
            "lines": len(lines), "verified_equal_to_pinned_git_blob": True,
        }
    return {
        "path": path, "declaration": actual, "source_spelling": spelling,
        "line_start": start, "line_end": end, "sha256": sha(raw),
        "range_sha256": sha(block), "range_bytes": len(block),
        "first_line": lines[start - 1].decode().rstrip("\n"),
        "url": f"https://github.com/CocoSgt/riemann-hypothesis-lean/blob/{PIN}/{path}#L{start}-L{end}",
        "role": role, "verified_equal_to_pinned_git_blob": True,
    }


specs = {
    "FP1": [
        ("ResMapBijective", "IsCO", "original complete Noetherian local coefficient category"),
        ("ResMapBijective", "resMap_bijective", "fixed original residue-field identification"),
        ("ResMapBijective", "AdicCont", "actual adic-continuity convention"),
        ("ResMapBijective", "PhiCond", "exact open-subgroup finite-character hypothesis"),
        ("CoSurj", "co_surj", "cotangent surjectivity criterion proved by successive approximation"),
        ("CoQuot", "co_quot", "quotient belongs to the original coefficient category"),
        ("CoMvps", "co_mvps", "finite formal power-series coefficient ring"),
        ("CoEvLow", "co_ev", "power-series evaluation at maximal-ideal elements"),
        ("CoSpan", "co_span", "cotangent generators give a complete-local presentation"),
        ("FiniteLiftDualNumberOfPhiCond", "finite_lift_dualNumber_of_phiCond",
         "full finite tangent separation supplied by PhiCond"),
    ],
    "FP2": [
        ("UnivLift", "Seps", "finite set distinguishes dual-number lifts"),
        ("UnivLift", "ev_surj", "selected entries generate the actual finite coefficient subring"),
        ("UnivLift", "level", "finite Artin-level universal representation"),
        ("UnivLift", "assemble", "compatible Artin levels give the complete continuous representation"),
        ("UnivLift", "univ_lift", "literal general matrix-lift endpoint"),
        ("ExistsLiftDominatingPairOfMaximalIdealPowEqBot", "sub_co",
         "entry-generated finite subring has the original residue field"),
        ("ExistsLiftDominatingPairOfMaximalIdealPowEqBot",
         "exists_lift_dominating_pair_of_maximalIdeal_pow_eq_bot",
         "joint-entry product object; reconstructed by kernel intersection"),
        ("ResMapBijective", "Represents", "unique actual algebra maps; no conjugacy quotient"),
        ("ResMapBijective", "Lift.Generates", "all actual representation entries"),
    ],
    "FP3": [
        ("ResMapBijective", "wtPart", "actual support-defined formal weight submodule"),
        ("ResMapBijective", "wcomp", "actual weight projection"),
        ("ResMapBijective", "IsHomog", "kernel stable under every weight projection"),
        ("ResMapBijective", "WPres", "original finite weighted presentation"),
        ("ResMapBijective", "part", "actual image of the formal weight submodule"),
        ("TchPoly", "tchar", "formal near-identity torus characters"),
        ("HomogOfStable", "hos_art", "finite Artin-level extraction of weights"),
        ("HomogOfStable", "homog_of_stable",
         "torus-stable ideal is homogeneous; proved here by character independence"),
        ("EigenMem", "eigen_mem",
         "intrinsic formal-torus eigencondition equals membership in the actual weight part"),
        ("KerGen", "ker_gen", "finite homogeneous generators of a homogeneous ideal"),
        ("HomogSpan", "homog_span", "span of homogeneous generators is homogeneous"),
        ("LemmaP", "lp_homog_max", "the original maximal ideal is homogeneous"),
        ("LemmaP", "lp_homog_mul", "product with an ideal generated by homogeneous elements"),
        ("LemmaP", "lp_homog_sup", "sum of homogeneous ideals"),
    ],
    "FP4": [
        ("FramedTwoCoboundaries", "FormData", "original block involution and form-weight constraints"),
        ("FramedTwoCoboundaries", "HH", "actual near-identity block form group"),
        ("FramedTwoCoboundaries", "InH", "original form-preserving coset condition"),
        ("FramedTwoCoboundaries", "IsLocCond", "all five local-condition axioms retained"),
        ("HhGroup", "hh_group", "inverse and multiplication in the actual group"),
        ("HhSmall", "hh_small", "small Lie correction of a form-preserving matrix"),
        ("HhSection", "inv_supp", "support of the inverse form matrix"),
        ("HhSection", "fix_point", "half-error correction across a small extension"),
        ("HhSection", "hh_section", "graded form-group section with adic continuity"),
        ("ContSection", "cont_section", "continuous sections of actual weight-part surjections"),
        ("LocGraded", "square_zero_extension_ring", "auxiliary square-zero interpolation ring"),
        ("LocGraded", "torus_data", "formal-torus separation for finite kernel weights"),
        ("LocGraded", "split_data", "split-ring transfer of the actual local condition"),
        ("LocGraded", "loc_map", "ideal-defined local condition under base change"),
        ("LocGraded", "loc_graded",
         "needed finite-residue specialization reconstructed directly by the interpolation ring"),
        ("LocGradedTop", "loc_graded_top",
         "needed finite-residue arbitrary-local-topology specialization; no topological-group hypothesis added"),
        ("CoSqz", "co_sqz", "finite square-zero coefficient extension belongs to the original category"),
    ],
    "FP5": [
        ("FramedTwoCoboundaries", "Normalises", "original normalization hypotheses"),
        ("FramedTwoCoboundaries", "ad_mem", "actual adjoint-stability formula"),
        ("FramedTwoCoboundaries", "Frame", "same finite frame and original local groups/maps"),
        ("FramedTwoCoboundaries", "IsFramed", "all original framed equations and local conditions"),
        ("FramedTwoCoboundaries", "IsUnivFramed", "exact outgoing universal property"),
        ("FramedUniv", "coprod2", "completed coefficient coproduct"),
        ("FramedUniv", "Cut.all", "arbitrary equation family in the Noetherian ambient ring"),
        ("FramedUniv", "cut_HH", "closed near-identity form group"),
        ("FramedUniv", "cut_InH", "closed representation coset condition"),
        ("FramedUniv", "all_univ", "all actual equations and local conditions on one coefficient ring"),
        ("FramedUniv", "framed_of_univ", "frame normalization and actual unique tuple maps"),
        ("FramedUniv", "framed_univ", "full universal framed deformation endpoint"),
        ("CoordGrading", "coord_grading", "actual separating coordinate-family presentation"),
        ("FramedGrading", "framed_torus", "torus preserves all original framed data"),
        ("FramedGrading", "framed_grading", "complete weighted universal framed presentation"),
        ("MapPart", "map_part", "same original map B to R respects actual weight parts"),
    ],
    "FP6": [
        ("FramedTwoCoboundaries", "g", "actual form Lie algebra"),
        ("FramedTwoCoboundaries", "gw", "exact sign of the adjoint weight"),
        ("FramedTwoCoboundaries", "adRep", "original conjugation action"),
        ("FramedTwoCoboundaries", "H1c", "framed cocycles without quotient by coboundaries"),
        ("FramedTangent", "hh_iff", "dual-number form-group tangent"),
        ("FramedTangent", "inH_iff", "exact adjoint cocycle coordinates"),
        ("FramedTangent", "loc_iff", "tangent local condition equals vanishing on original N"),
        ("FramedTangent", "framed_iff", "sign convention for framed tangent vectors"),
        ("FramedTangent", "abstract", "cotangent dimension and actual entry basis"),
        ("FramedTangent", "framed_tangent", "exact count at every original weight"),
        ("RelPres", "rel_pres_min", "minimal homogeneous relative relation classes"),
        ("RelPres", "rel_pres", "relative presentation with unchanged original weight parts"),
        ("PresNew", "pres_new", "old variables plus chosen actual new entries"),
        ("PresIndep", "pres_indep", "independence of minimal relative relation classes"),
        ("LemmaP", "lp_taylor", "first-order expansion with a general complete-local O"),
        ("LemmaP", "lp_ker",
         "small relative relation kernel lies in base maximal ideal plus squared maximal ideal"),
    ],
    "FP7": [
        ("FramedTwoCoboundaries", "framedTwoCocycles", "exact global/local cocycle equations"),
        ("FramedTwoCoboundaries", "framedTwoCoboundaries",
         "actual boundary triples; span equals the linear image"),
        ("FramedTwoCoboundaries", "Ob",
         "literal Z2 quotient by the comap/intersection of B2"),
        ("KerCoef", "ker_coef", "homogeneous relation-kernel coefficient maps"),
        ("ObsCocycle", "lc_ker", "locally constant finite-kernel errors"),
        ("ObsCocycle", "co_gw", "defects have the exact adjoint weight"),
        ("ObsCocycle", "obs_cocycle", "actual global/local obstruction cocycle"),
        ("CocycleNormalForm", "cocycle_normal_form", "single boundary triple with distinguished-frame normalization"),
        ("ObsCorrect", "obs_correct",
         "matrix, frame and local-condition correction with exact signs"),
        ("ObsClass", "obs_class",
         "full obstruction classes and homogeneous one-dimensional quotient lifting property"),
    ],
    "FP8": [
        ("LemmaP", "lp_detect",
         "relation detection reconstructed by nonzero functional, universal section and cotangent surjectivity"),
        ("LemmaP", "lp_ob_zero", "zero adjoint module outside finite entry-difference weights"),
        ("LemmaP", "lp_pad", "padding by zero equations gives exact rather than upper counts"),
        ("FramedTwoCoboundaries", "IsUnivFramed", "literal universal tuple endpoint"),
        ("FramedTwoCoboundaries", "IsRelPres", "all old/new variable and kernel fields"),
        ("FramedTwoCoboundaries", "LemmaP", "literal complete target with its original hypotheses"),
        ("LemmaP", "lemmaP", "complete pinned source producer"),
    ],
}
titles = {
    "FP1": "Complete local algebra and finite tangent separation",
    "FP2": "The actual universal continuous matrix lift",
    "FP3": "Formal-torus character extraction and homogeneous ideals",
    "FP4": "Continuous graded small-extension lifts preserving the actual local condition",
    "FP5": "The universal framed tuple and its original weighted presentation",
    "FP6": "Exact framed tangent counts and the minimal relative relation kernel",
    "FP7": "Actual framed obstruction classes and a sign-correct small-extension correction",
    "FP8": "Literal LemmaP with exact generator and equation counts at every weight",
}
deps = {
    "FP1": [],
    "FP2": ["FP1"],
    "FP3": ["FP1"],
    "FP4": ["FP1", "FP3"],
    "FP5": ["FP1", "FP2", "FP3"],
    "FP6": ["FP1", "FP3", "FP5"],
    "FP7": ["FP4", "FP6"],
    "FP8": ["FP1", "FP5", "FP6", "FP7"],
}
scopes = {
    "FP1": "General complete Noetherian local O with finite residue k, not necessarily a domain or DVR. Original PhiCond for all open subgroups; no topological finite-generation assumption.",
    "FP2": "Actual continuous lifts of the same residual representation over every ring in the original coefficient category; unique algebra maps, with no conjugacy quotient.",
    "FP3": "Finite free integral weight lattice, arbitrary coefficient characteristic and zero divisors, finite weighted presentations in the original complete-local category.",
    "FP4": "Needed finite-residue specialization of the local graded-lift endpoint, with the original IsLocCond axioms and arbitrary topology on the original local group. Does not claim the unrestricted infinite-residue helper.",
    "FP5": "The original B, frame maps, local groups, form, normalizing representations and local conditions, all on the same actual universal ring.",
    "FP6": "Original unquotiented framed H1c and actual adjoint weight j; exact relative cotangent basis from actual entries, retaining original WB and its old relation ideal.",
    "FP7": "Original Z2/(Z2 intersect B2) obstruction spaces, actual local conditions and same B-map; no abstract replacement Selmer complex or stronger local topology.",
    "FP8": "Full literal LemmaP implication for every original datum satisfying its hypotheses. It does not assert PhiCond, local-condition axioms, finite obstruction spaces or the local graded datum on later arithmetic Raw inputs.",
}
classical = {
    "FP1": ["FP-NA"],
    "FP2": ["FP-PS"],
    "FP3": ["FP-NA", "FP-PS"],
    "FP4": ["FP-PS"],
    "FP5": ["FP-PS"],
    "FP6": ["FP-NA"],
    "FP7": [],
    "FP8": [],
}
raw = (HERE / "main.tex").read_bytes()
lines = raw.splitlines(keepends=True)
claims = []
for cid in titles:
    begin = next(i for i, line in enumerate(lines, 1) if line.decode().strip() == "% BEGIN " + cid)
    start = next(i for i, line in enumerate(lines, 1) if i > begin and line.decode().startswith("\\begin{"))
    end_marker = next(i for i, line in enumerate(lines, 1) if line.decode().strip() == "% END " + cid)
    end = end_marker - 1
    while not lines[end - 1].strip():
        end -= 1
    assert lines[end - 1].decode().strip() == r"\end{proof}"
    proof = b"".join(lines[start - 1:end])
    claims.append({
        "id": cid, "title": titles[cid], "introduced_in": "0.26",
        "status": "Complete human proof of the stated general implication with explicit classical inputs",
        "mathematical_status": "Literal endpoint reconstruction with proved simplifications; no Lean replay",
        "scope": scopes[cid], "depends_on": deps[cid],
        "classical_inputs": classical[cid], "remaining_bespoke_inputs": [],
        "proof_location": {
            "file": "framed_deformation_presentation/main.tex", "paragraph": cid,
            "label": "claim:" + cid, "line_start": start, "line_end": end,
            "sha256": sha(proof), "bytes": len(proof),
        },
        "sources": [source(*entry) for entry in specs[cid]],
        "source_relation": (
            "Complete literal LemmaP reconstruction. Finite-level kernel intersections replace "
            "the source assembly machinery; an explicit finite square-zero interpolation ring "
            "proves the needed local graded lift with the original topology; relation detection "
            "uses a one-dimensional kernel quotient and the universal section. These simplifications "
            "prove the required supplier statements; source loc_graded_top is only claimed in "
            "the finite-residue specialization needed by LemmaP."
        ),
        "component_ledger": "framed_deformation_presentation/provenance.json",
    })

out = {
    "schema": "rh-human-reconstruction-provenance/1",
    "artifact_version": "0.26", "date": "2026-11-22",
    "repository": "https://github.com/CocoSgt/riemann-hypothesis-lean",
    "commit": PIN, "component": "framed_deformation_presentation",
    "scope": "Complete literal general LemmaP with all original theorem hypotheses retained and every representability, grading, tangent, obstruction and relation-count supplier reconstructed.",
    "claims": claims, "dependency_graph": deps,
    "external_claim_dependencies": {},
    "classical_input_registry": "framed_deformation_presentation/classical_inputs.json",
    "source_files": list(cache.values()),
    "validation": {
        "claim_count": len(claims),
        "claim_source_links": sum(len(c["sources"]) for c in claims),
        "source_files_checked_against_pinned_git_blobs": len(cache),
        "main_tex_sha256": sha(raw),
        "verification_kind": "Exact human-proof/source byte ranges and pinned Git blob checks; no Lean kernel replay",
    },
}
(HERE / "provenance.json").write_text(json.dumps(out, indent=2, ensure_ascii=False) + "\n")
(HERE / "source_locators.txt").write_text(
    "\n\n".join(c["id"] + " — " + c["title"] + "\n" +
                "\n".join(s["declaration"] + "\n" + s["url"] +
                          "\nfile " + s["sha256"] + "\nrange " + s["range_sha256"]
                          for s in c["sources"]) for c in claims) + "\n")
print(json.dumps(out["validation"], indent=2))
