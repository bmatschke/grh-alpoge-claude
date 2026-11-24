#!/usr/bin/env python3
"""Hash the BST human proofs and exact source evidence; never replay Lean."""
from pathlib import Path
import hashlib
import json
import subprocess

HERE = Path(__file__).resolve().parent
WORK = HERE.parent
REPO = Path("/workspace/scratch/249d32c24541/formal_source")
PIN = "7cbf7a0c32fca1badf05931879a37c3f8a2b03b4"
VERSION = "0.51"
COMPONENT = HERE.name
SNAPSHOT = WORK / "source_snapshot_v0_51" / "analysis"
BASE = "src/ReciprocityTheory/ReductiveGroups/DiscreteSeries/LaplaceOperators/"
URL = "https://github.com/CocoSgt/riemann-hypothesis-lean/blob/" + PIN + "/"

def sha(data):
    return hashlib.sha256(data).hexdigest()

def dump(name, value):
    (HERE / name).write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n")

def lp(path):
    return BASE + path

# A None declaration denotes the whole file. Named declarations below are
# isolated up to the next top-level declaration, with exact byte/range hashes.
groups = {
    "decay_scope": [
        (lp("LaplaceEstimates/IfaceSt.lean"), "def DecDerivStatement"),
        (lp("ReproducingKernels/DecDeriv.lean"), None),
        (lp("ReproducingKernels/DecDerivA.lean"), None),
        (lp("ReproducingKernels/DecRepro.lean"), None),
    ],
    "tensor_scope": [
        (lp("LaplaceEstimates/PsiDatumStatement.lean"), "def TMapStatement"),
        (lp("LaplaceEstimates/PsiDatumStatement.lean"), "def TMapDStatement"),
        ("src/ReciprocityTheory/ReductiveGroups/DiscreteSeries/DiscreteSeriesExistence/IsSmoothL2OfCasimirEigen.lean", "def IsSmoothL2"),
        ("src/Formalism/RealPlaceAnalysis/SmoothOnG.lean", None),
    ],
    "generated_coefficients": [
        (lp("LaplaceEstimates/SmoothMatrixMaps/TmDSingleMulVec.lean"), None),
        (lp("LaplaceEstimates/SmoothMatrixMaps/TmAContDiffMulLeft.lean"), None),
        (lp("LaplaceEstimates/SmoothMatrixMaps/CoefXHasDeriv.lean"), None),
        (lp("LaplaceEstimates/SmoothMatrixMaps/FrobTranslateLe.lean"), None),
    ],
    "tensor_calculus": [
        (lp("LaplaceEstimates/SmoothMatrixMaps/TmETmapSmooth.lean"), None),
        (lp("LaplaceEstimates/SmoothMatrixMaps/TMapSpec.lean"), None),
        (lp("LaplaceEstimates/SmoothMatrixMaps/MemLpOfBound.lean"), None),
        (lp("KTypeLemma/QuotientHighestWeightTensorStandard.lean"), None),
    ],
    "minor_definitions": [
        (lp("CapelliIdentity/CapelliCentralStatement.lean"), None),
    ],
    "minor_alternation": [
        (lp("CapelliIdentity/ColAnti.lean"), None),
        (lp("CapelliIdentity/RowAnti.lean"), None),
        (lp("CapelliIdentity/ProdOfFnUpdateEq.lean"), None),
    ],
    "row_column": [
        (lp("CapelliIdentity/RowCol.lean"), None),
        (lp("CapelliIdentity/RowColA.lean"), None),
    ],
    "expansion": [
        (lp("CapelliIdentity/Expand.lean"), None),
    ],
    "eigenspace": [
        (lp("LaplaceEstimates/PsiDatumStatement.lean"), "def EigStatement"),
        (lp("LaplaceEstimates/ListProdMemOfForall.lean"), None),
        (lp("CapelliIdentity/Tensor.lean"), None),
        (lp("CapelliIdentity/WhittakerZeroStatement.lean"), None),
    ],
    "step_join": [
        (lp("LaplaceEstimates/StepDownStatement.lean"), None),
        (lp("LaplaceEstimates/StepUp.lean"), None),
        (lp("LaplaceEstimates/StepDown.lean"), None),
    ],
    "retained_evaluation": [
        (lp("LaplaceEstimates/PsiDatumStatement.lean"), "def EvalPStatement"),
        (lp("LaplaceEstimates/PsiDatumStatement.lean"), "def EvalMStatement"),
        (lp("LaplaceEstimates/CapIdx.lean"), None),
        (lp("LaplaceEstimates/SumGammaNnMinus.lean"), None),
    ],
    "retained_quotient": [
        (lp("LaplaceEstimates/PsiDatumStatement.lean"), "def QuotPStatement"),
        (lp("LaplaceEstimates/PsiDatumStatement.lean"), "def QuotMStatement"),
        (lp("LaplaceEstimates/QuotP.lean"), None),
        (lp("LaplaceEstimates/QuotM.lean"), None),
    ],
}
assert subprocess.check_output(["git", "-C", str(REPO), "rev-parse", "HEAD"], text=True).strip() == PIN
files = {}
for path in sorted({path for entries in groups.values() for path, _ in entries}):
    blob = subprocess.check_output(["git", "-C", str(REPO), "show", PIN + ":" + path])
    assert (REPO / path).read_bytes() == blob, path
    dest = SNAPSHOT / path
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_bytes(blob)
    files[path] = {
        "path": path, "snapshot_path": str(dest.relative_to(WORK)),
        "source_commit": PIN, "sha256": sha(blob), "bytes": len(blob),
        "line_count": len(blob.splitlines(keepends=True)), "url": URL + path,
        "verified_equal_to_pinned_git_blob": True,
    }

source_groups = {}
for group, entries in groups.items():
    source_groups[group] = []
    for number, (path, declaration) in enumerate(entries, 1):
        info = files[path]
        lines = (SNAPSHOT / path).read_bytes().splitlines(keepends=True)
        first, last = 1, len(lines)
        if declaration:
            first = next(i for i, line in enumerate(lines, 1)
                         if line.decode().startswith(declaration))
            ends = [i for i in range(first + 1, len(lines) + 1)
                    if lines[i - 1].decode().startswith(("def ", "theorem ", "lemma ", "end "))]
            last = min(ends) - 1 if ends else len(lines)
            while last > first and not lines[last - 1].strip():
                last -= 1
        selected = b"".join(lines[first - 1:last])
        source_groups[group].append({
            "id": f"BST_{group}_{number:02d}", "path": path,
            "line_start": first, "line_end": last,
            "declaration": declaration or "Complete source file; relevant declarations identified in the human proof",
            "file_sha256": info["sha256"], "range_sha256": sha(selected),
            "range_bytes": len(selected), "source_commit": PIN,
            "verified_equal_to_pinned_git_blob": True,
            "url": URL + path + f"#L{first}-L{last}",
        })

specs = [
    (1, "One compact smooth convolution fixing the entire lowest type", [],
     ["decay_scope"], ["DC1", "DC2", "DC7", "DC9", "DC10", "DC11"],
     "Arbitrary dimension/signature at the original hNeed scope; one kernel for all lowest-type vectors and any Haar normalization."),
    (2, "Whole original DecDerivStatement", [1],
     ["decay_scope"], ["DC6"],
     "Every original word and pair of kernel vectors; exact exponent -h/(8 sqrt(2q0)); no derivative-loss premise."),
    (3, "All generated-module coefficient words and free left translates", [2],
     ["tensor_scope", "generated_coefficients"], ["DC2"],
     "Any original unitary derived datum with its exact coefficient identity; every generated vector, word, lowest-type w and x0 in G; no ambient irreducibility."),
    (4, "Both literal tensor maps and exact first-derivative intertwining", [3],
     ["tensor_scope", "tensor_calculus"], [],
     "Every x1 in C^n, every free x0, every tuple in the generated module; both exact standard and contragredient actions."),
    (5, "Whole original TMapStatement and TMapDStatement", [3, 4],
     ["tensor_scope", "tensor_calculus"], ["BSP1", "BSP6"],
     "All derivative words satisfy the original exponent 1-aExp; every word lies in the actual L2 space, giving full IsSmoothL2."),
    (6, "Shifted-minor alternation and exact commutator", [],
     ["minor_definitions", "minor_alternation"], [],
     "Any associative complex algebra satisfying matrix-unit relations; every list, including repeats and empty lists."),
    (7, "Equality of shifted row and column minors", [6],
     ["minor_definitions", "row_column"], [],
     "All list lengths and index lists; a full double-sum commutator cancellation proves the noncommutative equality."),
    (8, "Whole original CapelliExpandStatement", [6, 7],
     ["minor_definitions", "expansion"], [],
     "Both complementary expansions, exact left operator order and shifts x-1 and x-m, including m=0."),
    (9, "Whole original EigStatement", [8],
     ["minor_definitions", "eigenspace"], [],
     "Arbitrary complex module and stable submodule annihilated by the Capelli operator; every original y, beta, v and real omega."),
    (10, "Whole CapelliTensorStatement and exact positive/negative Casimir shifts", [9],
     ["minor_definitions", "eigenspace", "tensor_calculus"], ["BSP3"],
     "Both standard/dual tensor representations and Casimirs; no nonzero eigenspace vector or shifted quotient existence is asserted."),
    (11, "Exact conditional reduction of whole StepStatement to four suppliers", [5, 9, 10],
     ["step_join", "retained_evaluation", "retained_quotient"],
     ["BNV1", "BSP1", "BSP2", "BSP3", "BSP10"],
     "Retains full original EvalP, EvalM, QuotP, QuotM at unchanged scope; every original parameter, exclusion, Bessel datum and Haar pair."),
]
main = (HERE / "main.tex").read_bytes()
lines = main.decode().splitlines(keepends=True)
claims = []
for number, title, own, names, inherited, scope in specs:
    identifier = f"BST{number}"
    first = next(i for i, line in enumerate(lines, 1) if line.strip() == "% BEGIN " + identifier)
    last = next(i for i, line in enumerate(lines, 1) if line.strip() == "% END " + identifier)
    proof = "".join(lines[first - 1:last]).encode()
    assert b"\\begin{proof}" in proof and b"\\end{proof}" in proof
    claims.append({
        "id": identifier, "title": title, "introduced_in": VERSION, "classification": "B",
        "status": "complete human proof of the explicitly conditional implication" if number == 11
                  else "complete human proof at the explicitly stated scope",
        "depends_on": [f"BST{i}" for i in own] + inherited,
        "external_input_ids": ["BST_STANDARD_ANALYSIS", "BST_FINITE_COMPACT_THEORY"] +
                              (["BST_ORIGINAL_EVAL_QUOT"] if number == 11 else []),
        "published_input_ids": [], "scope_note": scope, "source_groups": names,
        "sources": [source for name in names for source in source_groups[name]],
        "proof_location": {
            "file": COMPONENT + "/main.tex", "label": "claim:" + identifier,
            "line_start": first, "line_end": last, "sha256": sha(proof), "bytes": len(proof),
        },
        "source_proof_is_not_human_proof": True, "whole_obligation_closure": False,
    })
manifest = {
    "schema": "rh-source-manifest/1", "artifact_version": VERSION, "component": COMPONENT,
    "source_commit": PIN, "snapshot_root": str(SNAPSHOT.relative_to(WORK)),
    "checkout_head_verified": True, "source_files": list(files.values()),
    "total_files": len(files), "total_bytes": sum(f["bytes"] for f in files.values()),
    "all_verified_equal_to_pinned_git_blob": True, "no_lean_replay": True,
    "source_is_evidence_for_target_scope_not_a_substitute_for_the_human_proof": True,
}
dump("source_manifest.json", manifest)
inherited = []
for component, ids in [
    ("discrete_series_core", ["DC1", "DC2", "DC6", "DC7", "DC9", "DC10", "DC11"]),
    ("bessel_nonvanishing_v50", ["BNV1", "BNV23"]),
    ("bessel_weight_propagation_v50", ["BSP1", "BSP2", "BSP3", "BSP6", "BSP10"]),
]:
    path = WORK / component / "main.tex"
    inherited.append({"component": component, "claims": ids,
                      "file": str(path.relative_to(WORK)), "sha256": sha(path.read_bytes())})
classical = [
    {"id": "BST_STANDARD_ANALYSIS", "status": "ordinary background retained",
     "content": "Smooth compact approximate identities on finite-dimensional Lie groups; Haar invariance and compact-group averaging; differentiation of compactly supported integrals; partitions of unity and local submanifold charts; finite-dimensional exterior algebra. Exact kernel reproduction, every derivative estimate, and both noncommutative adjugate identities are proved here."},
    {"id": "BST_FINITE_COMPACT_THEORY", "status": "ordinary compact representation background retained",
     "content": "Schur's lemma and finite-dimensional compact isotypic decomposition, as in the inherited DC construction. The full multiplicity-one lowest isotypic space is inherited from the proved DC9--DC10, not assumed from a Bessel uniqueness theorem."},
    {"id": "BST_ORIGINAL_EVAL_QUOT", "status": "four exact source producers retained",
     "content": "Full EvalPStatement, EvalMStatement, QuotPStatement and QuotMStatement with all original data, exclusions and operator periods. Used only by the explicitly conditional BST11.",
     "source_file": lp("LaplaceEstimates/PsiDatumStatement.lean"), "source_commit": PIN,
     "source_is_not_human_proof": True, "used_only_by_claims": ["BST11"]},
]
dump("classical_inputs.json", {"schema": "rh-explicit-inputs/1", "component": COMPONENT, "inputs": classical})
reviews = []
for path in sorted(HERE.glob("independent_review*.json")):
    reviews.append({"file": str(path.relative_to(WORK)), "sha256": sha(path.read_bytes()),
                    "content": json.loads(path.read_text())})
validation = json.loads((HERE / "tex_validation.json").read_text())
assert validation["proof_file_sha256"] == sha(main)
dump("provenance.json", {
    "schema": "rh-human-component-provenance/1", "artifact_version": VERSION,
    "date": "2026-11-23", "component": COMPONENT, "source_commit": PIN,
    "main_tex_sha256": sha(main), "proof_file_sha256": sha(main), "claims": claims,
    "source_groups": source_groups, "source_files": list(files.values()),
    "source_inventory": list(files.values()), "retained_foundations": classical,
    "inherited_human_inputs": inherited, "independent_reviews": reviews,
    "builder": COMPONENT + "/build_metadata.py", "validation": validation,
    "whole_obligation_closures": [], "no_lean_replay": True,
})
remaining = [
    {"id": "BST_REMAINING_EVAL_P", "source_declaration": "EvalPStatement",
     "statement": "Nonzero exact old period implies nonzero period of nnPlus tensor image at u_j != lambda_s+1/2."},
    {"id": "BST_REMAINING_EVAL_M", "source_declaration": "EvalMStatement",
     "statement": "Nonzero exact old period implies nonzero period of nnMinus tensor image at u_j != lambda_s-1/2."},
    {"id": "BST_REMAINING_QUOT_P", "source_declaration": "QuotPStatement",
     "statement": "Construct the actual Wf,W' for lambda+e_s, with exact image relation, shifted lowest type and Casimir, compact stability and period injectivity."},
    {"id": "BST_REMAINING_QUOT_M", "source_declaration": "QuotMStatement",
     "statement": "Construct the actual Wf,W' for lambda-e_s with every analogous original property."},
]
for entry in remaining:
    entry.update({"source_file": lp("LaplaceEstimates/PsiDatumStatement.lean"),
                  "source_commit": PIN, "status": "not reconstructed in this component"})
dump("contracts.json", {
    "schema": "rh-root-producer-contracts/1", "artifact_version": VERSION,
    "component": COMPONENT, "source_commit": PIN, "proof_file_sha256": sha(main),
    "endpoint_claim": "BST11",
    "completed_original_substatements": [
        "DecDerivStatement for every kernel vector pair and derivative word",
        "TMapStatement and TMapDStatement for all original generated-module tuples",
        "Both full IsSmoothL2 conclusions and original exact exponent/intertwining",
        "CapelliExpandStatement in every associative complex algebra",
        "EigStatement for arbitrary stable modules with exact complementary minors",
        "CapelliTensorStatement and exact +/-1 Casimir shifts",
    ],
    "remaining_exact_producers": remaining,
    "conditional_join": "EvalP + EvalM + QuotP + QuotM imply the whole original StepStatement; BNV23 then yields BesselNVGap and the setting on its retained supplied-Forms0 scope.",
    "not_claimed": [
        "Nonzero complementary-minor period or full EvalP/EvalM",
        "Shifted lowest-type quotient existence or full QuotP/QuotM",
        "Unconditional StepStatement, BesselNVGap, ConcreteSettingExists or Forms0 supply",
        "Any whole selected obligation, orbital/fiber comparison, RH or unrestricted Dirichlet GRH",
    ],
    "proposed_whole_obligation_closures": [], "whole_obligation_closures": [],
    "no_lean_replay": True,
})
dump("closure.json", {
    "schema": "rh-component-closure/1", "artifact_version": VERSION,
    "component": COMPONENT, "proof_file_sha256": sha(main),
    "human_claims": [c["id"] for c in claims],
    "fully_proved_claims_at_stated_scope": [c["id"] for c in claims if c["id"] != "BST11"],
    "proved_conditional_implications": ["BST11"],
    "remaining_source_producers": [entry["id"] for entry in remaining],
    "whole_obligation_closures": [], "all_sources_pinned": True, "no_lean_replay": True,
})
(HERE / "report.txt").write_text(f"""Bessel shift suppliers, version {VERSION}
Formal source pin: {PIN}
Frozen main SHA-256: {sha(main)}

Eleven human claims, BST1--BST11, form a complete analytic/algebraic packet.
BST11 is an explicitly conditional reduction, not an unconditional step proof.

Completed exact producers:
  * Compact smooth convolution fixing every vector of the lowest type.
  * Full DecDerivStatement, with all words and the original unchanged exponent.
  * Full TMapStatement and TMapDStatement: every generated-module tuple,
    all free translates, arbitrary x1, exact standard/dual intertwining,
    every derivative-word estimate, and every actual L2 derivative.
  * Shifted column/row minor alternation and equality, with a full
    double-sum commutator cancellation and no imported adjugate identity.
  * Both complementary Capelli expansions and full EigStatement.
  * Full CapelliTensorStatement and the exact two Casimir shifts.

The remaining unit-shift suppliers are precisely EvalP, EvalM, QuotP, QuotM.
Their full original premises and operator periods are retained. The eigenspace
vectors are not asserted nonzero; scalar Casimir agreement does not construct
the required quotient. BNV23 and its global-setting join remain conditional,
with the original supplied Forms0 scope unchanged.

Verification:
{len(files)} source files / {manifest['total_bytes']} bytes checked against pinned
Git blobs; exact statement and source-range hashes are in provenance.json.
All proof paths are relative to the root of the reconstructed bundle.
Two-pass draft TeX: {validation['status']}; no PDF and no Lean replay.
Independent review is incorporated separately when available.
""")
(HERE / "README.txt").write_text(
    "Read main.tex for BST1--BST11 and contracts.json for the exact residual suppliers.\n"
    "Regenerate metadata: python build_metadata.py\n"
    "Draft TeX check: python validate_tex.py --format ../global_local_gain_v46/validation/pdflatex.fmt\n"
    "The proof may simplify the source; source files establish exact target scope and are not proof certificates.\n"
)
print(json.dumps({"component": COMPONENT, "claims": len(claims), "source_files": len(files),
                  "source_bytes": manifest["total_bytes"], "main_sha256": sha(main),
                  "tex_status": validation["status"], "whole_obligation_closures": []}, indent=2))
