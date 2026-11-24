#!/usr/bin/env python3
"""Pin the BSE human proofs and exact source scope; never replay Lean."""
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
RELEVANT = "src/Formalism/SharpRestriction/CuspSpanNormBounds/RelevantZeroGramTerms.lean"
URL = "https://github.com/CocoSgt/riemann-hypothesis-lean/blob/" + PIN + "/"


def sha(data):
    return hashlib.sha256(data).hexdigest()


def dump(name, value):
    (HERE / name).write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n")


def lp(path):
    return BASE + path


# A None declaration means the complete source file. Named declarations are
# isolated up to the next top-level declaration; the exact range is hashed.
groups = {
    "actual_period": [
        (lp("EquivariantL2Space.lean"), "def sInt "),
        (lp("EquivariantL2Space.lean"), "def IsBData "),
        (lp("LaplaceEstimates/PsiDatumStatement.lean"), "def per "),
        (lp("LaplaceEstimates/HaarRightStatement.lean"), "def PerEquivStatement "),
        (lp("LaplaceEstimates/HaarRightStatement.lean"), "def HaarRightStatement "),
        (lp("LaplaceEstimates/SIntEquiv.lean"), None),
    ],
    "bessel_geometry": [
        ("src/Formalism/FormalDegreeBessel/StatementG.lean", None),
        (RELEVANT, "def IsCayley "),
        (RELEVANT, "def IsFrameW "),
        (RELEVANT, "def IsHCTypeW "),
        (RELEVANT, "def IsHaarOn "),
        (RELEVANT, "def ellA "),
        (RELEVANT, "def psiGen "),
    ],
    "compact_type": [
        (RELEVANT, "def IsKTypeOf "),
        (RELEVANT, "def IsHCTypeU "),
        ("src/Formalism/FormalDegreeBessel/StatementDS.lean", "def lowK "),
        (lp("LaplaceEstimates/BlockEmbeddingSkewHermitian.lean"), "theorem exists_derived "),
    ],
    "frame_law": [
        (lp("LaplaceEstimates/HaarRightStatement.lean"), "def FrameLawStatement "),
        (lp("LaplaceEstimates/HaarRightStatement.lean"), "theorem frameLaw "),
        (lp("LaplaceEstimates/FrameForm.lean"), None),
        (lp("LaplaceEstimates/BlockEmbeddingSkewHermitian.lean"), None),
        (lp("LaplaceEstimates/LFSingleNe.lean"), None),
    ],
    "capelli_restriction": [
        (lp("CapelliIdentity/CapelliCentralStatement.lean"), None),
        (lp("CapelliIdentity/CapelliCentralStatement.lean"), "def CapelliBStatement "),
        (lp("CapelliIdentity/CapelliCentralStatement.lean"), "def WhittakerZeroStatement "),
        (lp("CapelliIdentity/CapelliWhittakerZero.lean"), None),
        (lp("CapelliIdentity/WhittakerZeroStatement.lean"), None),
    ],
    "minor_covariance": [
        (lp("LaplaceEstimates/EvalMC.lean"), None),
        (lp("LaplaceEstimates/EvalMD.lean"), None),
        (lp("LaplaceEstimates/EvalMD.lean"), "def CapelliCovStatement "),
    ],
    "tensor_period": [
        (lp("LaplaceEstimates/PsiDatumStatement.lean"), "def xJ "),
        (lp("LaplaceEstimates/PsiDatumStatement.lean"), "def tMap "),
        (lp("LaplaceEstimates/PsiDatumStatement.lean"), "def tMapD "),
        (lp("LaplaceEstimates/StepDownStatement.lean"), "def xOne "),
        (lp("LaplaceEstimates/EvalPA.lean"), None),
        (lp("LaplaceEstimates/EvalPB.lean"), None),
        (lp("LaplaceEstimates/EvalMF.lean"), None),
    ],
    "evaluation_plus": [
        (lp("LaplaceEstimates/PsiDatumStatement.lean"), "def EvalPStatement "),
        (lp("LaplaceEstimates/CapIdx.lean"), None),
    ],
    "evaluation_minus": [
        (lp("LaplaceEstimates/PsiDatumStatement.lean"), "def EvalMStatement "),
        (lp("LaplaceEstimates/SumGammaNnMinus.lean"), None),
    ],
    "retained_quotients": [
        (lp("LaplaceEstimates/PsiDatumStatement.lean"), "def QuotPStatement "),
        (lp("LaplaceEstimates/PsiDatumStatement.lean"), "def QuotMStatement "),
        (lp("LaplaceEstimates/StepDownStatement.lean"), None),
    ],
}
assert subprocess.check_output(
    ["git", "-C", str(REPO), "rev-parse", "HEAD"], text=True
).strip() == PIN
files = {}
for path in sorted({path for entries in groups.values() for path, _ in entries}):
    blob = subprocess.check_output(["git", "-C", str(REPO), "show", PIN + ":" + path])
    assert (REPO / path).read_bytes() == blob, path
    dest = SNAPSHOT / path
    dest.parent.mkdir(parents=True, exist_ok=True)
    if dest.exists():
        assert dest.read_bytes() == blob, "existing snapshot has different bytes: " + path
    else:
        dest.write_bytes(blob)
    files[path] = {
        "path": path,
        "snapshot_path": str(dest.relative_to(WORK)),
        "source_commit": PIN,
        "sha256": sha(blob),
        "bytes": len(blob),
        "line_count": len(blob.splitlines(keepends=True)),
        "url": URL + path,
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
            first = next(
                i for i, line in enumerate(lines, 1)
                if line.decode().startswith(declaration)
            )
            ends = [
                i for i in range(first + 1, len(lines) + 1)
                if lines[i - 1].decode().startswith(("def ", "theorem ", "lemma ", "end "))
            ]
            last = min(ends) - 1 if ends else len(lines)
            while last > first and not lines[last - 1].strip():
                last -= 1
        selected = b"".join(lines[first - 1:last])
        source_groups[group].append({
            "id": f"BSE_{group}_{number:02d}",
            "path": path,
            "line_start": first,
            "line_end": last,
            "declaration": declaration.strip() if declaration else
                "Complete source file; relevant declarations identified in the human proof",
            "file_sha256": info["sha256"],
            "range_sha256": sha(selected),
            "range_bytes": len(selected),
            "source_commit": PIN,
            "verified_equal_to_pinned_git_blob": True,
            "url": URL + path + f"#L{first}-L{last}",
        })

specs = [
    (1, "Whole original PerEquivStatement with the given weak Haar measures", [],
     ["actual_period", "bessel_geometry"],
     ["AMD8", "BWP1", "BWP3", "BNV11", "BST3", "BST5", "BSP5"],
     "Every original Bessel datum, arbitrary matrix P and period point, every matrix function and target vector; includes the source's zero convention for undefined Bochner integrals."),
    (2, "Full compact derived action and exact Capelli polynomial", [],
     ["compact_type", "capelli_restriction"], ["BST6"],
     "Every original IsHCTypeU(k,u), including k=0; all vectors and every complex polynomial parameter. The highest vector is derived from the literal dominated-weight predicate."),
    (3, "Whole original FrameLawStatement with explicit nonzero kappa", [1, 2],
     ["frame_law", "bessel_geometry", "compact_type"],
     ["BST3", "BSP5", "BWP1", "BNV11"],
     "Every complete original derived datum, free x0,w,xi,g, and every generated-module vector; the same original compact frame gives both infinitesimal laws and the exact compact polynomial."),
    (4, "Whole CapelliBStatement and WhittakerZeroStatement", [],
     ["capelli_restriction"], ["BST6", "BST7", "BST8"],
     "Arbitrary complex modules and linear intertwiner, every complex parameter, arbitrary simple-root character values; no kappa nonvanishing is assumed for the identity; rank-zero restriction needs no bracket relation."),
    (5, "Whole CapelliCovStatement and both complementary-minor transformations", [],
     ["minor_covariance", "capelli_restriction"], ["BST6", "BST9"],
     "Any associative complex algebra with the exact gl_n commutator, every invertible frame and complex parameter. Quantum Cauchy--Binet preserves the original operator order."),
    (6, "Actual standard and dual tensor periods in one unchanged frame", [],
     ["tensor_period", "bessel_geometry"], ["BSP4", "BST5", "BSP5"],
     "Every generated-module tuple, every original period point and Haar pair; the r=0 scalars have the exact opposite standard/dual signs."),
    (7, "Whole original EvalPStatement with an explicit witness and exact period", [2, 3, 4, 5, 6],
     ["evaluation_plus", "tensor_period"], [],
     "All original data and quantifiers, exclusion u_j != lambda_s+1/2, actual standard tensor map and original operator period; witness y=Q^-1 e_j*; k=0 and r=0 included."),
    (8, "Whole original EvalMStatement with an explicit witness and exact period", [2, 3, 4, 5, 6],
     ["evaluation_minus", "tensor_period"], [],
     "All original data and quantifiers, exclusion u_j != lambda_s-1/2, actual dual tensor map and original operator period; witness alpha=last row of Q; k=0 and r=0 included."),
    (9, "Exact conditional full Step/Bessel reduction to the two original quotient suppliers", [7, 8],
     ["retained_quotients", "evaluation_plus", "evaluation_minus"],
     ["BST11", "BNV23", "BWP24"],
     "Retains the complete original QuotP and QuotM; then gives both Step directions, BesselNVGap, and the original setting only on its inherited supplied-Forms0 scope."),
]

main = (HERE / "main.tex").read_bytes()
lines = main.decode().splitlines(keepends=True)
claims = []
for number, title, own, names, inherited, scope in specs:
    identifier = f"BSE{number}"
    first = next(i for i, line in enumerate(lines, 1) if line.strip() == "% BEGIN " + identifier)
    last = next(i for i, line in enumerate(lines, 1) if line.strip() == "% END " + identifier)
    proof = "".join(lines[first - 1:last]).encode()
    assert b"\\begin{proof}" in proof and b"\\end{proof}" in proof
    claims.append({
        "id": identifier, "title": title, "introduced_in": VERSION, "classification": "B",
        "status": "complete human proof of the explicitly conditional implication" if number == 9
                  else "complete human proof at the explicitly stated scope",
        "depends_on": [f"BSE{i}" for i in own] + inherited,
        "external_input_ids": ["BSE_STANDARD_HAAR_AND_LIE"] +
                              (["BSE_ORIGINAL_QUOTIENTS"] if number == 9 else []),
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
    ("adelic_measures_v48", ["AMD8"]),
    ("bessel_wave_packets_v49", ["BWP1", "BWP3", "BWP24"]),
    ("bessel_nonvanishing_v50", ["BNV11", "BNV23"]),
    ("bessel_weight_propagation_v50", ["BSP4", "BSP5"]),
    ("bessel_shift_suppliers_v51", ["BST3", "BST5", "BST6", "BST7", "BST8", "BST9", "BST11"]),
]:
    path = WORK / component / "main.tex"
    inherited.append({"component": component, "claims": ids,
                      "file": str(path.relative_to(WORK)), "sha256": sha(path.read_bytes())})
classical = [
    {"id": "BSE_STANDARD_HAAR_AND_LIE", "status": "ordinary background retained",
     "content": "Uniqueness and change of variables for Haar measures; the continuous modulus of a group automorphism; compact-group unimodularity; Bochner linearity and dominated differentiation already supplied by BSP5; finite-dimensional Lie differentiation and torus weight shifts; U(k) is connected and generated by exponentials. The actual period covariance, compact Capelli polynomial, nilpotent character and every noncommutative minor identity are proved in this chapter or inherited BST claims."},
    {"id": "BSE_ORIGINAL_QUOTIENTS", "status": "two exact source producers retained",
     "content": "Full QuotPStatement and QuotMStatement: literal Wf and W', exact tensor-image relation, shifted lowest compact type and Casimir, actual compact-group stability, and injectivity of the prescribed period on the chosen quotient. Used only by explicitly conditional BSE9.",
     "source_file": lp("LaplaceEstimates/PsiDatumStatement.lean"), "source_commit": PIN,
     "source_is_not_human_proof": True, "used_only_by_claims": ["BSE9"]},
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
    {"id": "BSE_REMAINING_QUOT_P", "source_declaration": "QuotPStatement",
     "statement": "Construct the original Wf,W' for lambda+e_s with exact image relation, shifted lowest type and Casimir, actual compact stability and period injectivity."},
    {"id": "BSE_REMAINING_QUOT_M", "source_declaration": "QuotMStatement",
     "statement": "Construct the original Wf,W' for lambda-e_s with every analogous original property."},
]
for entry in remaining:
    entry.update({"source_file": lp("LaplaceEstimates/PsiDatumStatement.lean"),
                  "source_commit": PIN, "status": "not reconstructed in this component"})
dump("contracts.json", {
    "schema": "rh-root-producer-contracts/1", "artifact_version": VERSION,
    "component": COMPONENT, "source_commit": PIN, "proof_file_sha256": sha(main),
    "endpoint_claim": "BSE9",
    "completed_original_substatements": [
        "PerEquivStatement for all original data, arbitrary matrix P and matrix functions",
        "Compact exists_derived with the exact whole-space Capelli polynomial",
        "FrameLawStatement for every original generated-module vector and datum",
        "CapelliBStatement and WhittakerZeroStatement at their full algebraic scope",
        "CapelliCovStatement in every associative complex algebra",
        "EvalPStatement for the literal standard tensor period",
        "EvalMStatement for the literal dual tensor period",
    ],
    "exact_evaluation": {
        "frame": "Q=g0^-1 g P^-1; d=2r+k; j*=0 if r>0 and d if r=0",
        "standard_witness": "y=Q^-1 e_j*",
        "dual_witness": "alpha=e_d^t Q",
        "character_scalar_r_positive": "kappa=-T(z)*product_a |c_a|^2/4^r",
        "standard_period": "kappa*product_j(u_j-lambda_s-1/2)*old_period for r>0; replace kappa by -sqrt(T(z)) for r=0",
        "dual_period": "kappa*product_j(u_j-lambda_s+1/2)*old_period for r>0; replace kappa by sqrt(T(z)) for r=0",
        "all_original_character_haar_compact_representation_and_translates_preserved": True,
    },
    "remaining_exact_producers": remaining,
    "conditional_join": "QuotP + QuotM now imply the whole original StepStatement via BST11 and BSE7-BSE8; BNV23 then gives BesselNVGap and the setting only on its retained supplied-Forms0 scope.",
    "not_claimed": [
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
    "fully_proved_claims_at_stated_scope": [c["id"] for c in claims if c["id"] != "BSE9"],
    "proved_conditional_implications": ["BSE9"],
    "remaining_source_producers": [entry["id"] for entry in remaining],
    "whole_obligation_closures": [], "all_sources_pinned": True, "no_lean_replay": True,
})
(HERE / "report.txt").write_text(f"""Bessel complementary-minor period evaluation, version {VERSION}
Formal source pin: {PIN}
Frozen main SHA-256: {sha(main)}

Nine human claims, BSE1--BSE9. The first eight prove their full stated
analytic/algebraic targets. BSE9 is an explicitly conditional implication.

Completed original producers:
  * PerEquivStatement, including arbitrary matrix P and the original
    undefined-Bochner-integral convention; neither Haar measure is rescaled.
  * The compact derived action and exact whole-space Capelli polynomial.
  * FrameLawStatement for all original generated-module vectors.
  * CapelliBStatement, WhittakerZeroStatement and CapelliCovStatement.
  * Full EvalPStatement and full EvalMStatement at their original scope.

With Q=g0^-1 g P^-1 and d=2r+k, the standard witness is Q^-1 e_j*,
where j*=0 for r>0 and j*=d for r=0. The dual witness is the last row of Q.
For r>0 their exact periods are, respectively,
  kappa * product_j(u_j-lambda_s-1/2) * old_period,
  kappa * product_j(u_j-lambda_s+1/2) * old_period,
with kappa=-T(z)*product_a |c_a|^2/4^r.
For r=0 replace kappa by -sqrt(T(z)) and +sqrt(T(z)), respectively.
These are formulas for the prescribed integrals with the original character,
compact representation, arbitrary Haar normalizations and free translates.
The rank-zero cases and empty compact products are included.

The only remaining exact unit-shift suppliers in the BST/BSE conditional join
are QuotPStatement and QuotMStatement. They must construct the actual Wf,W'
and every original shifted-type, image, stability and injectivity property.
BSE9 retains these full producers. No unconditional StepStatement, BesselNVGap,
ambient Forms0 supplier, whole selected obligation, RH or GRH is declared closed.

Verification:
{len(files)} source files / {manifest['total_bytes']} bytes checked against pinned
Git blobs; exact statement/range hashes are in provenance.json.
All proof paths are relative to the reconstructed bundle root.
Two-pass draft TeX: {validation['status']}; no PDF and no Lean replay.
Independent review is incorporated separately when available.
""")
(HERE / "README.txt").write_text(
    "Read main.tex for BSE1--BSE9 and contracts.json for the two exact residual quotient suppliers.\n"
    "Regenerate metadata: python build_metadata.py\n"
    "Draft TeX check: python validate_tex.py --format ../global_local_gain_v46/validation/pdflatex.fmt\n"
    "The source establishes exact target scope; the mathematical proofs are the human arguments in main.tex.\n"
)
print(json.dumps({"component": COMPONENT, "claims": len(claims), "source_files": len(files),
                  "source_bytes": manifest["total_bytes"], "main_sha256": sha(main),
                  "tex_status": validation["status"], "whole_obligation_closures": []}, indent=2))
