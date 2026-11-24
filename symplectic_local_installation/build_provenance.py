#!/usr/bin/env python3
"""Build exact pinned source/human-proof provenance for DX1--DX8."""
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
AV = "src/Development/AutomorphicArithmetic/AutomorphicVarieties/"
PT = "src/Development/AbelianVarietyTheory/PublishedTheorems/GaloisCohomology₂/"
GC = "src/ReciprocityTheory/Hypotheses/GalCoh"
cache = {}


def sha(data):
    return hashlib.sha256(data).hexdigest()


def path_of(file):
    if file.startswith("src/"):
        return file + ".lean"
    if file.startswith("PT/"):
        return PT + file[3:] + ".lean"
    return AV + file + ".lean"


def source(file, spelling, role):
    path = path_of(file)
    raw = (REPO / path).read_bytes()
    lines = raw.splitlines(keepends=True)
    pattern = (r"^(?:(?:private|protected|noncomputable)\s+)*"
               r"(?:def|abbrev|theorem|lemma|structure|class|instance)\s+([^\s:{(]+)")
    starts = [(i, m.group(1)) for i, line in enumerate(lines, 1)
              if (m := re.match(pattern, line.decode()))]
    matches = [(i, name) for i, name in starts
               if name == spelling or name.endswith("." + spelling)]
    if len(matches) != 1:
        raise ValueError((path, spelling, matches))
    start, name = matches[0]
    end = min([i for i, _ in starts if i > start] or [len(lines) + 1]) - 1
    while end > start and not lines[end - 1].strip():
        end -= 1
    block = b"".join(lines[start - 1:end])
    if path not in cache:
        pinned = subprocess.check_output(["git", "-C", str(REPO), "show", PIN + ":" + path])
        assert raw == pinned, "Pinned blob mismatch: " + path
        cache[path] = {
            "path": path, "sha256": sha(raw), "bytes": len(raw), "lines": len(lines),
            "verified_equal_to_pinned_git_blob": True,
        }
    return {
        "path": path, "declaration": name, "source_spelling": spelling,
        "line_start": start, "line_end": end, "sha256": sha(raw),
        "range_sha256": sha(block), "range_bytes": len(block),
        "first_line": lines[start - 1].decode().rstrip("\n"),
        "url": f"https://github.com/CocoSgt/riemann-hypothesis-lean/blob/{PIN}/{path}#L{start}-L{end}",
        "role": role, "verified_equal_to_pinned_git_blob": True,
    }


specs = {
    "DX1": [
        (GC, "LocalFinitenessAt", "exact finite continuous-cochain local finiteness target"),
        (GC, "LocalTateDualityAt", "all nonfree finite coefficient modules and both degree-one orders"),
        (GC, "LocalEulerCharAt", "original local-degree cardinality factor"),
        (GC, "LocalFiniteness", "literal universally quantified native interface"),
        (GC, "LocalTateDuality", "literal universally quantified native duality interface"),
        (GC, "LocalEulerChar", "literal universally quantified native Euler interface"),
        (GC, "ContainsAbove", "all primes above the coefficient prime remain in the actual S"),
        (GC, "archH0Card", "unmodified real fixed vectors and complex factor"),
        (GC, "GlobalFinitenessAt", "finite H0/H1/H2, higher vanishing only at odd ell"),
        (GC, "GlobalEulerCharAt", "literal truncated Euler identity including ell=2"),
        (GC, "GlobalFiniteness", "universal original global finiteness"),
        (GC, "GlobalEulerChar", "universal original global Euler identity"),
        ("PT/ExistsPrimitiveRootPow", "PoitouTateDuality", "incoming exact LD3 interface"),
        ("PT/PoitouTateNineTermTransgressionZeroApply", "IsLocalInvariants", "forget only ConjCompatible"),
        ("PT/PoitouTateNormalised", "PoitouTateNormalised", "identical quantifier order and remaining conclusions"),
        ("PadicHodgeTheory/DecEmb", "decEmb", "original decomposition group/inertia/cyclotomic comparison"),
        ("PadicHodgeTheory/TateFin", "tateFin", "source finite-to-native local dimension transfer"),
        ("LevelCohomology/HcGlobEuler", "globEuler", "exact k-dimensional rational-field specialization"),
        ("LevelCohomology/HcLocEuler", "locEuler", "exact local k-dimensional specialization"),
    ],
    "DX2": [
        ("CommutativeAlgebra/ResMapBijective", "PhiCond", "literal finite open-subgroup-character condition"),
        ("SymplecticGSp4/PhiGam", "permR", "original finite permutation representation"),
        ("SymplecticGSp4/PhiGam", "phi_condition_of_finite_cohomology", "explicit finite coset cocycle argument"),
        ("SymplecticGSp4/PhiGam", "phiGam", "actual global original D.Gam endpoint"),
        ("PadicHodgeTheory/PhiCond", "phiCond", "local finite-cohomology implication, enlarged package bypassed"),
        ("SymplecticGSp4/LocBase", "phi_dec", "original local PhiCond needed by local universal rings"),
        ("SymplecticGSp4/ResidueCharMemLevelPrimes", "Gam", "actual original unramified-outside-S quotient"),
    ],
    "DX3": [
        (GC, "GreenbergWilesAt", "all original local submodules, annihilators, placements and finite modules"),
        (GC, "GreenbergWiles", "literal universal interface, whose premise explicitly requires odd ell"),
        ("CommutativeAlgebra/FramedTwoCoboundaries", "H1c", "actual framed cocycles without quotient"),
        ("CommutativeAlgebra/FramedTwoCoboundaries", "framedTwoCocycles", "exact global/local 2-cocycle triples"),
        ("CommutativeAlgebra/FramedTwoCoboundaries", "framedTwoCoboundaries", "same global and local boundary formula"),
        ("CommutativeAlgebra/FramedTwoCoboundaries", "Ob", "literal intersection quotient"),
        ("LevelCohomology/HcDefs", "selF", "strict T and unramified Q conditions on original groups"),
        ("LevelCohomology/HcDefs", "shaF", "actual kernel of all local H2 restrictions"),
        ("LevelCohomology/FiniteCompactlySupportedH1", "framed_h1_euler_formula", "complete framed H1 dimension identity"),
        ("LevelCohomology/HcFrameOb", "frameOb", "actual cokernel-to-obstruction-to-Sha exact calculation"),
        ("LevelCohomology/HcGalTail", "galTail", "finite Poitou--Tate tail dimension identity"),
        ("LevelCohomology/HcPtTail", "ptTail", "original dual H0/cyclotomic coefficient matching"),
        ("LevelCohomology/HcUrIndex", "urIndex", "prime-to-ell inertia quotient removed by averaging"),
        ("LevelCohomology/HcUrAbs", "urAbs", "unramified local H1 equals Frobenius coinvariants"),
        ("LevelCohomology/HcDecZhat", "decZhat", "original decomposition quotient is procyclic"),
        ("LevelCohomology/HcGalCount", "galCount", "full framed Euler identity on the actual rational datum"),
    ],
    "DX4": [
        ("SymplecticGSp4/ResidueCharMemLevelPrimes", "Nums", "literal all-descent all-weight target"),
        ("SymplecticGSp4/ResidueCharMemLevelPrimes", "frame", "unchanged original frame and inertia intersections"),
        ("SymplecticGSp4/NumsZero", "nums_odd", "complex-conjugation parity for the actual odd roots"),
        ("SymplecticGSp4/NumsZero", "nums_gen", "global twisted-dual invariant vanishing"),
        ("SymplecticGSp4/NumsZero", "nums_all", "all original weight cases"),
        ("SymplecticGSp4/NumsZero", "nums", "complete target producer, CohomologyHyp bypassed exactly as stated"),
        ("LevelCohomology/HcSpAct", "spAct", "actual scalar adjoint character at weight j"),
        ("LevelCohomology/HcSpDim", "spDim", "root-by-root two/one/zero dimensions"),
        ("LevelCohomology/HcSpKer", "spKer", "finite prime-to-ell residual inertia quotient"),
        ("LevelCohomology/HcScalDim", "scalDim", "actual invariant and complex-conjugation dimensions"),
        ("LevelCohomology/H1cZero", "h1cZero", "actual framed cocycle vanishing from Good.xvan"),
        ("LevelCohomology/HcUnrOf", "unrOf", "all valuation conditions retained under conjugation"),
        ("SymplecticGSp4/DecompSigmaOrd", "Good", "incoming original arithmetic hypotheses remain explicit"),
        ("SymplecticGSp4/LMemMax", "facts", "complete incoming AX6 original character and residual separation facts"),
        ("SymplecticGSp4/MapRepApply", "spW", "original adjoint root subspace"),
    ],
    "DX5": [
        ("CommutativeAlgebra/ResMapBijective", "Represents", "unique actual lifts over every IsCO target"),
        ("CommutativeAlgebra/ResMapBijective", "WPres", "original finite homogeneous presentation"),
        ("CommutativeAlgebra/ResMapBijective", "HasOrigin", "kernel vanishes at simultaneous variable-zero origin"),
        ("CommutativeAlgebra/ResMapBijective", "satSq", "actual saturation inside the graded subalgebra"),
        ("CommutativeAlgebra/UnivLift", "univ_lift", "incoming FP2 actual matrix universal ring"),
        ("CommutativeAlgebra/UnivCond", "univ_cond", "closed polynomial conditions on actual representations"),
        ("CommutativeAlgebra/LiftGrading", "lift_grading", "incoming FP3 torus-to-weight construction"),
        ("CommutativeAlgebra/OrbitVanishingLocal", "IsChart", "all four original chart clauses"),
        ("CommutativeAlgebra/OrbitVanishingLocal", "SmoothPt", "actual target weight counts"),
        ("CommutativeAlgebra/ChartGr", "chart_gr", "chart return to the original graded subalgebra"),
        ("PadicHodgeTheory/IsInertiaInfiniteCyclotomic", "IsCompl", "exact source completion/density/injectivity clauses"),
        ("PadicHodgeTheory/LiftChart", "liftChart", "full generic chart comparison; explicit proof replaces source machinery"),
        ("SymplecticGSp4/LocBase", "ordSet", "infinite family of actual polynomial ordinary equations"),
        ("SymplecticGSp4/LocBase", "closedL", "actual ordinary condition is closed"),
        ("SymplecticGSp4/LocBase", "closedP", "actual all-Artin inertia-kernel condition is closed"),
        ("SymplecticGSp4/LocBase", "rep_ex", "original local universal rings; unused larger hypothesis bypassed"),
        ("SymplecticGSp4/LocBase", "lb_chart", "exact source completion-to-SmoothPt transfer"),
        ("SymplecticGSp4/LocBase", "pk_of", "actual weighted local representation/origin/chart package"),
    ],
    "DX6": [
        ("SymplecticGSp4/MapRepApply", "Ord", "all unnormalized spectral ordinary equations"),
        ("SymplecticGSp4/LocDefs", "eqL", "literal original ordinary equation condition"),
        ("SymplecticGSp4/LocDefs", "dimL", "exact two/one/zero weight multiplicities"),
        ("SymplecticGSp4/LocDefs", "tanSet", "O-valued continuous dual-number tangent set"),
        ("SymplecticGSp4/LocDefs", "Liftable", "source Artin lifting predicate; proved in the needed E-augmented germ"),
        ("PadicHodgeTheory/SpLiftL", "nonres", "all root characters differ from 1 and the cyclotomic character"),
        ("PadicHodgeTheory/SpLiftL", "spLiftL", "actual ordinary Artin lifting supplier, reproved by root H2 vanishing"),
        ("PadicHodgeTheory/SpTanL", "spTanL", "actual ordinary tangent equations"),
        ("PadicHodgeTheory/TangentSpaceDeformationAtL", "tangent_space_deformation_at_l", "source exact weighted tangent count"),
        ("PadicHodgeTheory/SpChartL", "spChartL", "complete original fourteen-parameter chart endpoint"),
        ("SymplecticGSp4/SpWApply", "tanLz", "literal negative-Psi denominator coboundary and weight-zero inertia vanishing"),
        ("SymplecticGSp4/LocBase", "pkL", "actual ordinary local package at the original origin"),
    ],
    "DX7": [
        ("SymplecticGSp4/DecompSigmaOrd", "Sb", "exact finite-prime selection and nontrivial inertia character"),
        ("SymplecticGSp4/LocDefs", "eqP", "entire original inertia-kernel condition on every coefficient ring"),
        ("SymplecticGSp4/LocDefs", "dimP", "zero/root multiplicities"),
        ("PadicHodgeTheory/SpTanP", "ps_ine", "two original inertia eigenspaces"),
        ("PadicHodgeTheory/SpTanP", "ex_psi", "nontrivial original inertia character"),
        ("PadicHodgeTheory/SpTanP", "spTanP", "actual finite-inertia tangent equation comparison"),
        ("PadicHodgeTheory/TangentSpaceDeformationDualNumbers", "tangent_space_deformation_dual_numbers", "source exact ten weighted tangent directions"),
        ("PadicHodgeTheory/SpLiftP", "spLiftP", "actual all-Artin finite-inertia lifting supplier, reproved explicitly"),
        ("PadicHodgeTheory/SpChartP", "spChartP", "complete original ten-parameter chart endpoint"),
        ("SymplecticGSp4/LocBase", "pkP", "actual finite-inertia local package"),
    ],
    "DX8": [
        ("SymplecticGSp4/ResidueCharMemLevelPrimes", "LocBase", "every field of the literal original output record"),
        ("SymplecticGSp4/LocBase", "pk_sum", "simultaneous local package over one original O"),
        ("SymplecticGSp4/LocBase", "locBase", "complete actual original LocBase endpoint"),
        ("CommutativeAlgebra/Coprod", "coprod", "completed local coproduct with actual universal maps"),
        ("CommutativeAlgebra/ChartSum", "chart_sum", "exact summed original weight multiplicities"),
        ("SymplecticGSp4/ExModel", "exModel", "consumer: exact PhiCond plus Nums plus LocBase, with LemmaP"),
    ],
}
titles = {
    "DX1": "Original finite local/global cohomology and normalized Poitou--Tate",
    "DX2": "Actual global and local PhiCond",
    "DX3": "Full finite Greenberg--Wiles and the framed Euler identity",
    "DX4": "Literal Nums on every original good datum",
    "DX5": "Integral universal local rings and actual weighted characteristic-zero charts",
    "DX6": "Ordinary fourteen-parameter chart and literal tanLz",
    "DX7": "All-Artin finite-inertia ten-parameter chart",
    "DX8": "Complete original LocBase and installed exModel arithmetic inputs",
}
deps = {
    "DX1": ["LD3", "LK1", "LK2", "LK3", "LK4", "KB6"],
    "DX2": ["DX1"],
    "DX3": ["DX1", "LD3"],
    "DX4": ["DX3", "AX6"],
    "DX5": ["DX2", "FP1", "FP2", "FP3", "AX6"],
    "DX6": ["DX1", "DX5", "AX6"],
    "DX7": ["DX5", "AX6"],
    "DX8": ["DX2", "DX4", "DX5", "DX6", "DX7"],
}
scopes = {
    "DX1": "Full literal native finite interfaces including nonfree coefficients, original valuations, roots, cup products and invariant order. Global Euler includes 2 via the explicit truncated classical formula; higher global vanishing remains odd-only. Rational rank-one formulas are proved by the actual compatible lattice limit.",
    "DX2": "The original D.Gam and every actual finite-prime decomposition group. No finite-generation assumption on the profinite group and no BlochKatoLocal.",
    "DX3": "Full literal GreenbergWiles, whose original premises require ell odd; all original finite modules and local submodules. Framed Euler identity uses original Z2/(Z2 intersect B2), distinguished zero frame and actual inertia intersections.",
    "DX4": "For every original Good D, every rb descent and its supplied Normalises proof, at every integral two-dimensional weight. Uses actual Good.xvan and residual separation; does not assume CohomologyHyp as a package.",
    "DX5": "Integral universal eqL/eqP rings for every IsCO target. Generic-chart implication is conditional on actual unobstructed E-Artin lifting and tangent counts, discharged by DX6/DX7. SmoothPt is on the actual graded subalgebra and origin; no integral smoothness claim.",
    "DX6": "Ordinary local chart for the unchanged Good D at its original ell-place, with all spectral equations and exact positive/negative root weights. Literal tanLz has one integral denominator and equality on every original local element.",
    "DX7": "For each original q in Sb, kill Iq intersect ker psi in every Artin lift, not only residually. The actual quotient, finite-character conjugation, Frobenius continuity and exact torus weights are proved.",
    "DX8": "Actual original LocBase record over the same coefficient O and original local groups, unique tuple maps and exact sum dL(j)+|Sb|dP(j). Along with DX2/DX4, closes the three actual arithmetic exModel inputs on Good D, not the larger BlochKatoLocal or CohomologyHyp packages.",
}
classical = {
    "DX1": ["DX-LT", "DX-LE", "DX-GF", "DX-GE"],
    "DX2": [],
    "DX3": [],
    "DX4": [],
    "DX5": ["DX-CM"],
    "DX6": [],
    "DX7": [],
    "DX8": [],
}
external = {
    "LD3": "local_duality_closure",
    "LK1": "local_k_duality", "LK2": "local_k_duality",
    "LK3": "local_k_duality", "LK4": "local_k_duality",
    "KB6": "k_theory_bridge", "AX6": "symplectic_arithmetic_data",
    "FP1": "framed_deformation_presentation",
    "FP2": "framed_deformation_presentation",
    "FP3": "framed_deformation_presentation",
}
external_records = {}
for cid, component in external.items():
    ledger_path = HERE.parent / component / "provenance.json"
    raw_ledger = ledger_path.read_bytes()
    ledger = json.loads(raw_ledger)
    claim = next(c for c in ledger["claims"] if c["id"] == cid)
    external_records[cid] = {
        "component": component,
        "provenance_file": component + "/provenance.json",
        "provenance_sha256": sha(raw_ledger),
        "main_tex_sha256": sha((HERE.parent / component / "main.tex").read_bytes()),
        "proof_location": claim["proof_location"],
    }

raw = (HERE / "main.tex").read_bytes()
lines = raw.splitlines(keepends=True)
claims = []
for cid in titles:
    begin = next(i for i, line in enumerate(lines, 1) if line.decode().strip() == "% BEGIN " + cid)
    start = next(i for i, line in enumerate(lines, 1) if i > begin and line.decode().startswith("\\begin{"))
    end = next(i for i, line in enumerate(lines, 1) if line.decode().strip() == "% END " + cid) - 1
    while not lines[end - 1].strip():
        end -= 1
    assert lines[end - 1].decode().strip() == r"\end{proof}"
    proof = b"".join(lines[start - 1:end])
    claims.append({
        "id": cid, "title": titles[cid], "introduced_in": "0.27",
        "status": "Complete human proof with exact original theorem scope and named classical inputs",
        "mathematical_status": "Actual supplier reconstruction with explicit simplifications; no Lean replay",
        "scope": scopes[cid], "depends_on": deps[cid],
        "classical_inputs": classical[cid], "remaining_bespoke_inputs": [],
        "proof_location": {
            "file": "symplectic_local_installation/main.tex", "paragraph": cid,
            "label": "claim:" + cid, "line_start": start, "line_end": end,
            "sha256": sha(proof), "bytes": len(proof),
        },
        "sources": [source(*entry) for entry in specs[cid]],
        "source_relation": (
            "Complete original arithmetic PhiCond/Nums/LocBase chain. Finite Tate and "
            "global Euler are matched to native interfaces; the framed exact sequences "
            "are proved on actual cochains. Explicit characteristic-zero ordinary-root "
            "and finite-inertia deformation functors replace the source's larger "
            "LocalPublishedTheorems assumption. Full BlochKatoLocal is neither needed "
            "nor promoted. The source definitions and exact outgoing endpoints are retained."
        ),
        "component_ledger": "symplectic_local_installation/provenance.json",
    })

scope_sources = [
    source("SymplecticGSp4/EntryMem", "CohomologyHyp", "larger record retained unpromoted"),
    source("PadicHodgeTheory/LocalPublishedTheorems", "LocalPublishedTheorems", "all finite fields supplied; entire bk remains outside scope"),
    source("PT/RationalDualityOfAllCoefficients", "BlochKatoLocal", "full arbitrary period-module package explicitly not claimed"),
]
out = {
    "schema": "rh-human-reconstruction-provenance/1", "artifact_version": "0.27",
    "date": "2026-11-22",
    "repository": "https://github.com/CocoSgt/riemann-hypothesis-lean",
    "commit": PIN, "component": "symplectic_local_installation",
    "main_tex_sha256": sha(raw),
    "scope": "Complete actual PhiCond, Nums and LocBase installation on the unchanged Good arithmetic datum, with direct generic local charts and literal tanLz; full BlochKatoLocal remains unpromoted.",
    "claims": claims, "dependency_graph": deps,
    "external_claim_dependencies": external_records,
    "classical_input_registry": "symplectic_local_installation/classical_inputs.json",
    "scope_boundary_sources": scope_sources,
    "source_files": list(cache.values()),
    "validation": {
        "claim_count": len(claims),
        "claim_source_links": sum(len(c["sources"]) for c in claims),
        "scope_boundary_source_links": len(scope_sources),
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
