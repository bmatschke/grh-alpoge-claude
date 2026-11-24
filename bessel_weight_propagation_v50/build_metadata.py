#!/usr/bin/env python3
"""Pin the BSP target statements and hash each independent human proof block.

The source checkout is read only.  This script copies exact pinned blobs as
scope evidence; it does not replay Lean or treat source proofs as human proofs.
"""
from pathlib import Path
import hashlib
import json
import subprocess

HERE = Path(__file__).resolve().parent
WORK = HERE.parent
REPO = Path("/workspace/scratch/249d32c24541/formal_source")
PIN = "7cbf7a0c32fca1badf05931879a37c3f8a2b03b4"
VERSION = "0.50"
COMPONENT = HERE.name
SNAPSHOT = WORK / "source_snapshot_v0_50" / "analysis"
BASE = "src/ReciprocityTheory/ReductiveGroups/DiscreteSeries/LaplaceOperators/"
URL = "https://github.com/CocoSgt/riemann-hypothesis-lean/blob/" + PIN + "/"

def sha(data):
    return hashlib.sha256(data).hexdigest()

def write_json(name, data):
    (HERE / name).write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n")

def lp(path):
    return BASE + path

groups = {
    "original_statements": [
        lp("LaplaceEstimates/StepDownStatement.lean"),
        lp("LaplaceEstimates/PsiDatumStatement.lean"),
        lp("EquivariantL2Space.lean"),
    ],
    "gap": [lp("LaplaceEstimates/GapNeed.lean")],
    "kernel_datum": [
        lp("KTypeLemma/PsiDatum.lean"),
        lp("LaplaceEstimates/ClosedIrreducibleLowestTypeData.lean"),
        "src/ReciprocityTheory/ReductiveGroups/DiscreteSeries/CasimirCoefficients/IsClosedKset.lean",
    ],
    "capelli": [
        lp("LaplaceEstimates/CapVal.lean"),
        lp("LaplaceEstimates/CapValA.lean"),
        lp("CapelliIdentity/CapelliCentralStatement.lean"),
        lp("KTypeLemma/QuotientHighestWeightTensorStandard.lean"),
    ],
    "multipliers": [lp("LaplaceEstimates/HasDerivAtExp.lean")],
    "period_differentiation": [
        lp("LaplaceEstimates/SmoothMatrixMaps/IntOfBound.lean"),
        "src/Formalism/RealPlaceAnalysis/SmoothOnG.lean",
        "src/Formalism/RealPlaceAnalysis/SmoothOnGVIff.lean",
        "src/ReciprocityTheory/ReductiveGroups/DiscreteSeries/CasimirCoefficients/PsiExistsStatement.lean",
    ],
    "group_integral": [
        lp("LaplaceEstimates/CayleyConjInvMemHermitianGroup.lean"),
        lp("LaplaceEstimates/FinBFrobConjGe.lean"),
    ],
    "reproduction": [
        lp("LaplaceEstimates/ReproducingFormulaClosedInvariant.lean"),
        lp("LaplaceEstimates/ExistsOrthogonalProjectionInner.lean"),
        lp("LaplaceEstimates/FinProj.lean"),
    ],
    "fubini": [
        lp("LaplaceEstimates/FinFub.lean"),
        lp("LaplaceEstimates/ProductBoundThreeFactors.lean"),
    ],
    "final": [
        lp("LaplaceEstimates/ToL2EqZeroOfEqZeroOnUJset.lean"),
        lp("LaplaceEstimates/StepDown.lean"),
        lp("LaplaceEstimates/StepUp.lean"),
    ],
    "remaining_tensor": [
        lp("LaplaceEstimates/SmoothMatrixMaps/TMapSpec.lean"),
        lp("LaplaceEstimates/SmoothMatrixMaps/MemLpOfBound.lean"),
    ],
    "remaining_evaluation": [
        lp("LaplaceEstimates/CapIdx.lean"),
        lp("LaplaceEstimates/SumGammaNnMinus.lean"),
    ],
    "remaining_quotient": [
        lp("LaplaceEstimates/QuotP.lean"),
        lp("LaplaceEstimates/QuotM.lean"),
    ],
}

head = subprocess.check_output(["git", "-C", str(REPO), "rev-parse", "HEAD"], text=True).strip()
if head != PIN:
    raise SystemExit("Pinned source checkout HEAD mismatch")
files = {}
for path in sorted({path for paths in groups.values() for path in paths}):
    disk = (REPO / path).read_bytes()
    blob = subprocess.check_output(["git", "-C", str(REPO), "show", PIN + ":" + path])
    if disk != blob:
        raise SystemExit("Source working tree differs from pinned blob: " + path)
    destination = SNAPSHOT / path
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_bytes(blob)
    files[path] = {
        "path": path, "snapshot_path": str(destination.relative_to(WORK)),
        "sha256": sha(blob), "bytes": len(blob), "line_count": len(blob.splitlines(keepends=True)),
        "source_commit": PIN, "verified_equal_to_pinned_git_blob": True,
        "url": URL + path,
    }

source_groups = {}
exact_ranges = {
    "src/Formalism/RealPlaceAnalysis/SmoothOnG.lean":
        (18, 33, "Original real local SmoothOnG, Rd and complexified matrix-unit derivative Eab"),
    "src/Formalism/RealPlaceAnalysis/SmoothOnGVIff.lean":
        (155, 170, "Original vector-valued local smoothness and complexified tangential derivative EabV"),
}
for group, paths in groups.items():
    source_groups[group] = []
    for i, path in enumerate(paths, 1):
        entry = files[path]
        first, last, declaration = exact_ranges.get(
            path, (1, entry["line_count"], "Complete pinned file; exact statement and relevant source scope identified in the human claim"))
        source_lines = (SNAPSHOT / path).read_bytes().splitlines(keepends=True)
        source_range = b"".join(source_lines[first - 1:last])
        source_groups[group].append({
            "id": f"BSP_{group}_{i:02d}", "path": path,
            "line_start": first, "line_end": last,
            "declaration": declaration,
            "file_sha256": entry["sha256"], "range_sha256": sha(source_range),
            "range_bytes": len(source_range), "source_commit": PIN,
            "verified_equal_to_pinned_git_blob": True,
            "url": URL + path + f"#L{first}-L{last}",
        })

specs = [
    (1, "Whole original GapNeedStatement", [], ["original_statements", "gap"], [],
     "Every k,r>=0 and original signature, including proof that the impossible q0=0 case is excluded by StepGap itself; exact beta/2 and beta/4 thresholds."),
    (2, "Whole PsiDatumStatement and large-gap cyclic lowest-type rigidity", [],
     ["original_statements", "kernel_datum"],
     ["DC1", "DC2", "DC3", "DC4", "DC7", "DC8", "DC9", "DC10", "DC11", "DC12"],
     "Arbitrary dimension and signature at original hNeed/q0/HC/gap scope; every compact kernel type and exact IsMu. Broader cyclic rigidity proved only at h>hNeed, not at every weaker ClosedIrreducibleLowestTypeData scope."),
    (3, "Whole original CapValStatement on the generated module", [],
     ["original_statements", "capelli"], ["DC4"],
     "Any original unitary derived datum satisfying the coefficient identity, without irreducibility of the ambient representation; every complex omega and every generated-module vector."),
    (4, "Whole original MultStatement", [],
     ["original_statements", "multipliers"], ["BWP1", "BWP3"],
     "Every middle vector z, including z=0, r=0 and all original standard/dual vectors; invariance under actual H_z N, exact right derivatives and linear-entry growth."),
    (5, "Whole original PerStatement", [1],
     ["original_statements", "period_differentiation"], ["BNV1", "AMD8"],
     "Every original Cayley, Bessel datum, weak Haar pair, xi and free translate; original local ambient smoothness and every right derivative word at exponent 1-aExp."),
    (6, "Exact original finB_intJ power-integral threshold", [],
     ["group_integral"], ["DC6"],
     "Arbitrary signature of positive noncompact rank and Haar normalization; all b>2nq0."),
    (7, "Pointwise closed-invariant-space reproduction", [],
     ["reproduction"], [],
     "Every closed invariant subspace with its stated positive-degree four-vector orthogonality and every continuous L2 representative; equality at every group point, not only almost everywhere."),
    (8, "Whole original finProj", [1, 2, 6, 7],
     ["original_statements", "kernel_datum", "reproduction"], [],
     "All original scalar function spaces Wf and smooth lowest-type spaces W' with exact image relation, actual compact stability, Casimir and decay; literal normalized Psi kernel."),
    (9, "Whole original finFub_int' and finFub", [1, 6],
     ["original_statements", "fubini"], ["BNV1", "BNV19", "DC6"],
     "Every original data set and kernel at StepGap; Bochner integrability of the actual product integrand and extraction of the nonzero prescribed Bessel integral with both free translates."),
    (10, "Whole original FinStatement", [8, 9],
     ["original_statements", "final"], ["BNV1"],
     "Every original Wf,W', compact stability, image, Casimir and period-injectivity hypothesis; unchanged Haar/character/compact data. Shifted quotient existence is not asserted."),
]

main = (HERE / "main.tex").read_bytes()
lines = main.decode().splitlines(keepends=True)
claims = []
for number, title, dependencies, group_names, inherited, scope in specs:
    identifier = f"BSP{number}"
    start = next(i for i, line in enumerate(lines, 1) if line.strip() == "% BEGIN " + identifier)
    end = next(i for i, line in enumerate(lines, 1) if line.strip() == "% END " + identifier)
    proof = "".join(lines[start - 1:end]).encode()
    assert r"\begin{proof}" in proof.decode() and r"\end{proof}" in proof.decode()
    claims.append({
        "id": identifier, "title": title, "introduced_in": VERSION,
        "classification": "B", "status": "complete human proof at the explicitly stated scope",
        "depends_on": [f"BSP{i}" for i in dependencies] + inherited,
        "external_input_ids": ["BSP_STANDARD_ANALYSIS", "BSP_FINITE_COMPACT_THEORY"],
        "published_input_ids": [], "scope_note": scope, "source_groups": group_names,
        "sources": [item for group in group_names for item in source_groups[group]],
        "proof_location": {
            "file": COMPONENT + "/main.tex", "label": "claim:" + identifier,
            "line_start": start, "line_end": end, "sha256": sha(proof), "bytes": len(proof),
        },
        "source_proof_is_not_human_proof": True, "whole_obligation_closure": False,
    })

manifest = {
    "schema": "rh-source-manifest/1", "artifact_version": VERSION, "component": COMPONENT,
    "source_commit": PIN, "snapshot_root": str(SNAPSHOT.relative_to(WORK)),
    "checkout_head_verified": True, "source_files": list(files.values()),
    "total_files": len(files), "total_bytes": sum(entry["bytes"] for entry in files.values()),
    "all_verified_equal_to_pinned_git_blob": True,
    "source_is_evidence_for_target_scope_not_a_substitute_for_the_human_proof": True,
    "no_lean_replay": True,
}
write_json("source_manifest.json", manifest)

inherited = []
for name, identifiers in [
    ("discrete_series_core", "DC1--DC13; especially DC4 Capelli, DC6 decay, DC8--DC11 cyclic rigidity and DC12 orthogonality"),
    ("bessel_nonvanishing_v50", "BNV1 original IntS, BNV19 coefficient period estimates; BNV23 remains conditional"),
    ("bessel_wave_packets_v49", "BWP1 and BWP3 exact groups and compact stabilizer"),
    ("adelic_measures_v48", "AMD8 weak Haar scope"),
]:
    path = WORK / name / "main.tex"
    inherited.append({
        "component": name, "claims": identifiers, "file": str(path.relative_to(WORK)),
        "sha256": sha(path.read_bytes()),
    })
classical = [
    {"id": "BSP_STANDARD_ANALYSIS", "status": "ordinary background retained",
     "content": "Finite-dimensional linear algebra, polar coordinates, Haar integration on Lie groups, Tonelli/Fubini and dominated differentiation, local smooth retractions of embedded submanifolds, Hilbert orthogonal projections and strong continuity of unitary translations. The reproduction formula and its Fubini majorant are proved in the component."},
    {"id": "BSP_FINITE_COMPACT_THEORY", "status": "ordinary compact representation background retained as in DC1",
     "content": "Finite-dimensional compact unitary complete reducibility, Schur's lemma, and uniqueness of the irreducible compact highest-weight type. No Bessel multiplicity-one, formal-degree polynomial, tensor-eigenspace quotient or period evaluation is imported."},
]
write_json("classical_inputs.json", {
    "schema": "rh-explicit-inputs/1", "component": COMPONENT, "inputs": classical,
})
reviews = []
review_path = HERE / "independent_review.json"
if review_path.exists():
    reviews.append({
        "file": "independent_review.json", "sha256": sha(review_path.read_bytes()),
        "content": json.loads(review_path.read_text()),
    })
validation_path = HERE / "tex_validation.json"
validation = json.loads(validation_path.read_text()) if validation_path.exists() else {"status": "pending"}
write_json("provenance.json", {
    "schema": "rh-human-component-provenance/1", "artifact_version": VERSION,
    "date": "2026-11-23", "component": COMPONENT, "source_commit": PIN,
    "main_tex_sha256": sha(main), "proof_file_sha256": sha(main),
    "claims": claims, "source_groups": source_groups,
    "source_inventory": list(files.values()), "source_files": list(files.values()),
    "retained_foundations": classical, "inherited_human_inputs": inherited,
    "independent_reviews": reviews, "builder": "build_metadata.py", "validation": validation,
    "whole_obligation_closures": [], "no_lean_replay": True,
})

remaining = [
    {"id": "BSP_REMAINING_TENSOR_MAPS", "source_declarations": ["TMapStatement", "TMapDStatement"],
     "source_file": lp("LaplaceEstimates/PsiDatumStatement.lean"),
     "content": "All standard/dual tensor coefficients from the original generated module are smooth L2 functions; exact intertwining derivatives and every derivative-word bound at exponent 1-aExp.",
     "status": "not reconstructed; BSP4 alone supplies only the scalar multipliers"},
    {"id": "BSP_REMAINING_ADJUGATE", "source_declarations": ["EigStatement"],
     "source_file": lp("LaplaceEstimates/PsiDatumStatement.lean"),
     "content": "Complementary Capelli minors yield the required standard and dual Euler eigenspace vectors when the Capelli polynomial annihilates the module.",
     "status": "not reconstructed; BSP3 supplies the polynomial-annihilation input"},
    {"id": "BSP_REMAINING_EVALUATION", "source_declarations": ["EvalPStatement", "EvalMStatement"],
     "source_file": lp("LaplaceEstimates/PsiDatumStatement.lean"),
     "content": "Nonzero original coefficient period produces a nonzero period of the exact Capelli-minor standard/dual tensor image, under the exclusions u_j != lambda_s +/- 1/2.",
     "status": "not reconstructed; exclusions alone do not prove this operator-period assertion"},
    {"id": "BSP_REMAINING_QUOTIENT", "source_declarations": ["QuotPStatement", "QuotMStatement"],
     "source_file": lp("LaplaceEstimates/PsiDatumStatement.lean"),
     "content": "Construct Wf and W' at lambda +/- e_s with exact image relation, shifted lowest type and Casimir, actual compact stability and period injectivity.",
     "status": "not reconstructed; BSP10 consumes these properties without constructing the quotient"},
]
write_json("contracts.json", {
    "schema": "rh-root-producer-contracts/1", "artifact_version": VERSION,
    "component": COMPONENT, "source_commit": PIN, "proof_file_sha256": sha(main),
    "endpoint_claim": "BSP10",
    "completed_original_substatements": [
        "Whole GapNeedStatement at all original k,r and signature quantifiers",
        "Whole PsiDatumStatement for arbitrary dimensions and signatures",
        "Whole CapValStatement for every original derived datum and the entire generated module",
        "Whole MultStatement, including standard and dual multipliers",
        "Whole PerStatement, with actual integral and every derivative word",
        "Exact finB_intJ group-integral threshold b>2nq0",
        "Pointwise closed-invariant-space reproduction and whole finProj",
        "Whole finFub_int' and finFub with a simpler proved product majorant",
        "Whole FinStatement, retaining every shifted quotient hypothesis",
    ],
    "remaining_exact_producers": remaining,
    "downstream_boundary": {
        "StepStatement": "open until both standard and dual remaining producers are supplied",
        "BesselNVGap": "still conditional through BNV23",
        "ConcreteSettingExists": "still conditional through BNV23/BWP24 and retains supplied Forms0",
    },
    "not_claimed": [
        "Either whole one-unit propagation direction, or the whole original StepStatement",
        "Existence of the original shifted quotient or its nonzero evaluation period",
        "Unconditional BesselNVGap or supplied-form ConcreteSettingExists",
        "Removal of Forms0, ambient form supply, orbital/fiber comparison or a whole selected obligation",
        "RH or unrestricted Dirichlet GRH",
    ],
    "proposed_whole_obligation_closures": [], "whole_obligation_closures": [],
    "no_lean_replay": True,
})
write_json("closure.json", {
    "schema": "rh-component-closure/1", "artifact_version": VERSION,
    "component": COMPONENT, "proof_file_sha256": sha(main),
    "human_claims": [claim["id"] for claim in claims],
    "fully_proved_claims_at_stated_scope": [claim["id"] for claim in claims],
    "proved_conditional_implications": [],
    "remaining_source_producers": [entry["id"] for entry in remaining],
    "whole_obligation_closures": [], "all_sources_pinned": True, "no_lean_replay": True,
})
(HERE / "report.txt").write_text(f"""Bessel weight propagation analytic producers, version {VERSION}
Source commit: {PIN}

The manuscript contains ten proved claims, BSP1--BSP10, at their stated exact
scope. It proves full original GapNeedStatement, PsiDatumStatement, CapValStatement,
MultStatement, PerStatement and FinStatement. The final reconstruction includes
the original finProj, finFub_int' and finFub. No whole obligation is closed.

Main mathematical additions:
  * Original gap arithmetic, retaining k=0 and excluding q0=0 from StepGap.
  * Exact kernel datum and rigidity of every cyclic lowest-type realization
    at the stated hNeed scope, derived from inherited DC8--DC12.
  * Capelli eigenvalue on the entire generated module, not just its lowest type.
  * Both exact invariant standard/dual multipliers, and differentiation under
    the prescribed operator period with every original datum and weak Haar pair.
  * Pointwise reproduction in the actual right-regular Hilbert space using
    the four-vector degree orthogonality, without a formal-degree polynomial.
  * A simplified product majorant for the final Fubini interchange, preserving
    the original exponent thresholds and both free translates.
  * Reconstruction of a literal nonzero Bessel integral from every original
    lowest-type quotient datum satisfying the exact period-injectivity premise.

Exact boundary:
The whole original StepStatement remains open. TMap/TMapD, the complementary
Capelli-minor eigenspace assertion, EvalP/EvalM, and QuotP/QuotM still need their
human proofs. Scalar multiplier identities and the Capelli polynomial eigenvalue
do not replace these suppliers. BSP10 consumes the shifted quotient's specified
data; it does not manufacture that data or assert its existence.
BNV23 and BesselNVGap therefore remain conditional, and the global setting still
retains Forms0. No orbital/fiber comparison or whole RH/GRH closure is claimed.

Evidence:
{len(files)} source files, {manifest['total_bytes']} bytes, each checked byte-for-byte
against git show at the pinned commit and copied to the shared analysis snapshot.
Every human block has a separate SHA-256 in provenance.json.
No Lean replay or build was run.
TeX validation: {validation.get('status', 'pending')}.
Independent review is incorporated in provenance when present.
""")
(HERE / "README.txt").write_text(
    "BSP1--10 are proved in main.tex; read contracts.json for the exact open boundary.\n"
    "Source scope is pinned in source_manifest.json; source proofs are not substitutes for human proofs.\n"
    "Rebuild: python build_metadata.py\n"
    "Draft TeX check: python validate_tex.py --format ../global_local_gain_v46/validation/pdflatex.fmt\n"
)
print(json.dumps({
    "component": COMPONENT, "claims": len(claims), "source_files": len(files),
    "source_bytes": manifest["total_bytes"], "main_sha256": sha(main),
    "tex_status": validation.get("status"), "whole_obligation_closures": [],
}, indent=2))
