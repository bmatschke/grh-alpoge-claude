#!/usr/bin/env python3
"""Rebuild the BNV provenance from exact pinned git blobs and the human TeX.

Reads the source checkout without modifying it; performs no Lean replay.
"""
from pathlib import Path
import hashlib
import json
import re
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

def lp(s):
    return BASE + s

groups = {
    "original_groups": [
        "src/Formalism/FormalDegreeBessel/StatementG.lean",
        "src/Formalism/LocalToGlobal/SiegelLatticeTheory/HaarTransversals/HidaSetting.lean",
    ],
    "original_target": [
        "src/Formalism/LocalToGlobal/SiegelLatticeTheory/HaarTransversals/UnitaryHaarProducts/SettingBlocks.lean",
        "src/Formalism/SharpRestriction/CuspSpanNormBounds/CayleySignature.lean",
    ],
    "scope": [lp("EquivariantL2Space.lean")],
    "integrability": [lp("ReproducingKernels/ReproCoreStatement.lean")],
    "walk": [
        lp("InterlacingWalks/LowerStepStatement.lean"),
        lp("InterlacingWalks/AdjGap.lean"),
        lp("InterlacingWalks/Walk.lean"),
        lp("InterlacingWalks/WalkEnds.lean"),
    ],
    "gap_bridge": [
        lp("SpectralGap/GapNum.lean"),
        lp("SpectralGap/GapBigLap.lean"),
        lp("SpectralGap/GapStep.lean"),
    ],
    "base_statements": [
        lp("LaplaceFoundations/IsHWSmooth.lean"),
        lp("LaplaceFoundations/RaisingLoweringNormIdentities.lean"),
        lp("LaplaceFoundations/AssemblyStatement.lean"),
    ],
    "large_parameter": [lp("LaplaceFoundations/OneLeNoncompactRankParabolicSign.lean")],
    "cyclic_frame": [
        lp("LaplaceFoundations/OneParameterSubgroups/ExistsCyclic.lean"),
        lp("LaplaceFoundations/BasePointPsiExpFormula.lean"),
    ],
    "exp_haar": [lp("LaplaceFoundations/UnipotentExpHaarSqrtBound.lean")],
    "majorant": [lp("LaplaceFoundations/LieExponentialMajorantHolds.lean")],
    "norm_estimates": [
        lp("LaplaceFoundations/NoncompactLoweringNormSmall.lean"),
        lp("LaplaceFoundations/DoubleSumDiagSplit.lean"),
    ],
    "tangent": [
        lp("LaplaceFoundations/MatrixCoeffBoundsImplyBound.lean"),
        lp("LaplaceFoundations/OneParameterSubgroups/OneParam.lean"),
    ],
    "gaussian": [
        lp("Laplace.lean"),
        lp("LaplaceFoundations/B6.lean"),
    ],
    "schur": [
        "src/ReciprocityTheory/ReductiveGroups/DiscreteSeries/CasimirCoefficients/IsClosedKset.lean",
        lp("LaplaceFoundations/NormPsiGen.lean"),
        lp("LaplaceFoundations/LowestKTypeIntertwinerExists.lean"),
        lp("LaplaceFoundations/SchurOrthogonalityWhittaker.lean"),
        lp("LaplaceFoundations/PsiCoef.lean"),
    ],
    "base_assembly": [
        lp("LaplaceFoundations/Assembly.lean"),
        lp("LaplaceFoundations/StepIBase.lean"),
    ],
    "transport": [
        lp("Transport.lean"),
        lp("TransportGeo.lean"),
        lp("TransportInt.lean"),
    ],
    "literal_return": [
        "src/Formalism/SharpRestriction/CuspSpanNormBounds/RelevantZeroGramTerms.lean",
        lp("BesselVectors/BesselNV.lean"),
        lp("BesselVectors/BesselNVGOfNv.lean"),
    ],
    "unit_shift_retained": [
        lp("LaplaceEstimates/StepDownStatement.lean"),
        lp("LaplaceEstimates/StepDown.lean"),
        lp("LaplaceEstimates/StepUp.lean"),
    ],
    "supplier_chain": [
        lp("ParitySignEqGapSign.lean"),
        lp("Imports.lean"),
        lp("BesselVectors/Closed.lean"),
        "src/Formalism/LocalToGlobal/SiegelLatticeTheory/WeightedGaugeFactors/FactsDS.lean",
        "src/Formalism/LocalToGlobal/SiegelLatticeTheory/BesselDiscreteSeries/BesselNVGapPf.lean",
    ],
}

head = subprocess.check_output(["git", "-C", str(REPO), "rev-parse", "HEAD"], text=True).strip()
if head != PIN:
    raise SystemExit("Pinned source checkout HEAD mismatch")

files = {}
for path in sorted({p for ps in groups.values() for p in ps}):
    disk = (REPO / path).read_bytes()
    blob = subprocess.check_output(["git", "-C", str(REPO), "show", PIN + ":" + path])
    if disk != blob:
        raise SystemExit("Source working tree differs from pinned blob: " + path)
    dst = SNAPSHOT / path
    dst.parent.mkdir(parents=True, exist_ok=True)
    dst.write_bytes(blob)
    lines = blob.splitlines(keepends=True)
    files[path] = {
        "path": path,
        "snapshot_path": str(dst.relative_to(WORK)),
        "sha256": sha(blob),
        "bytes": len(blob),
        "line_count": len(lines),
        "source_commit": PIN,
        "verified_equal_to_pinned_git_blob": True,
        "url": URL + path,
    }

source_groups = {}
for group, paths in groups.items():
    source_groups[group] = []
    for i, path in enumerate(paths, 1):
        f = files[path]
        source_groups[group].append({
            "id": f"BNV_{group}_{i:02d}",
            "path": path,
            "line_start": 1,
            "line_end": f["line_count"],
            "declaration": "Complete pinned source file; scope and relevant declarations described in the claim",
            "file_sha256": f["sha256"],
            "range_sha256": f["sha256"],
            "range_bytes": f["bytes"],
            "source_commit": PIN,
            "verified_equal_to_pinned_git_blob": True,
            "url": URL + path + f"#L1-L{f['line_count']}",
        })

# Every entry below has an independently delimited human proof in main.tex.
# Only BNV23 invokes the explicitly retained unit-shift producer.
specs = [
    (1, "Whole original IntSStatement", [], ["integrability", "original_groups"],
     ["BWP1", "BWP2", "BWP3", "AMD8"],
     "Every k,r, negative middle vector, original Haar pair and free translates; exact b>2rn^2, including r=0."),
    (2, "Sign, parameter lattice, and interlacing arithmetic", [], ["walk", "large_parameter"],
     [], "All k>=1,r>=0 with original HC, interlacing, and half-integrality assumptions."),
    (3, "Whole original AdjGapStatement", [], ["walk"],
     [], "Every strictly decreasing vector, every signature and real h."),
    (4, "Whole original RaiseStepStatement", [2, 3], ["walk"],
     [], "Every tail segment and all intermediate integral steps; no forbidden upward crossing."),
    (5, "Whole original LowerStepStatement", [2, 3], ["walk"],
     [], "Every initial-block segment and all intermediate steps; no forbidden downward crossing."),
    (6, "Whole original WalkStatement", [4, 5], ["walk"],
     [], "Every StepClosed predicate and every natural t, including zero-length and rank-zero segments."),
    (7, "Original GapBig to GapLap and StepGap", [3], ["original_target", "scope", "gap_bridge"],
     [], "Retains the original odd T and 1801 hypotheses, though the subproof needs fewer numerical assumptions."),
    (8, "Whole original LamTStatement", [2, 3], ["large_parameter", "base_statements"],
     [], "Exact affine lowest weight and compact initial weight; eventual analytic gap t/2."),
    (9, "Explicit cyclic isotropic frame", [], ["cyclic_frame"],
     [], "All real strictly decreasing 2r+1 nodes, including r=0; Vandermonde construction with exact Gram matrix."),
    (10, "Whole original PairingPropertiesStatement", [9], ["cyclic_frame", "base_statements", "original_groups"],
     [], "One Cayley matrix with WCols and the exact character c_a(t)=-2it; no scalar character ambiguity."),
    (11, "Whole original NsetExpInjectiveSurjective", [], ["exp_haar", "base_statements"],
     ["BWP1"], "Polynomial exp/log inverse, exact exp-pushforward Haar, realification norm, and polynomial logarithm bound."),
    (12, "Whole original CayleyMajorantBound", [11], ["majorant", "base_statements"],
     [], "Every Cayley matrix; global logarithmic lower bound in polar norm; compact degeneracy included."),
    (13, "Whole original HighestWeightVectorUniformBounds", [], ["norm_estimates", "base_statements"],
     ["DC8"], "Universal epsilon,d,Lambda0 and every original highest-weight/Casimir datum; constants uniform in t and representation."),
    (14, "Whole original TangentPairingStatement", [13], ["tangent", "base_statements"],
     [], "Every smooth highest-weight/Casimir vector; explicit differentiated ODE and uniform O_R(t^-1/2) error."),
    (15, "Nonvanishing of a complex Gaussian", [], ["gaussian"],
     [], "Any finite real dimension and additive Haar normalization; real part positive definite; dimension zero included."),
    (16, "Whole original GaussianLimitHaar", [15], ["gaussian", "base_statements"],
     [], "Pointwise Gaussian convergence and one uniform eventual polynomial majorant; positivity is deduced, not added."),
    (17, "Whole original WhittakerSchurOrthogonality", [], ["schur", "base_statements"],
     ["DC1", "DC2", "DC3"],
     "Exact probability-Haar factor 1/dim(Vpi), arbitrary sigma-finite measure on ambient matrices with no N-support assumption, zero-extended kernel and original vector integral."),
    (18, "Whole original StepIBaseStatement", [8, 10, 11, 12, 14, 16, 17], ["base_assembly", "base_statements"],
     ["DC1", "DC2", "DC3", "DC6", "DC7", "DC8", "DC9", "DC10", "DC11"],
     "All original k>=1,r,u,v,b assumptions; no initial low-gap assumption; exact nonzero period for every sufficiently large integral t."),
    (19, "Absolute convergence of every original coefficient period", [1], ["scope", "transport"],
     ["DC6", "AMD8"],
     "Every GapLap parameter in signature (k+r,r+1), every model/Cayley/Haar/character datum and free translates."),
    (20, "Exact normalizer conjugacy of all Bessel data", [], ["transport", "original_groups"],
     ["DC1"],
     "Explicit diagonal Levi scaling, negative-vector isometry, exact character equality, and preservation of framed compact label."),
    (21, "Original BesselNZ to BesselAll transport", [19, 20], ["scope", "transport"],
     ["DC1", "DC2", "DC3", "AMD8"],
     "Every permitted target datum and every nonzero vector; no extra derivative-decay or Bessel-uniqueness premise."),
    (22, "Return to the actual endomorphism-valued Bessel integral", [19], ["original_target", "literal_return"],
     ["DC11", "DC13"],
     "Conditional on BesselAll; every original supplied representation, lowest unit vector, compact type, character and Haar pair."),
    (23, "Conditional BesselNVGap and supplied-form ConcreteSettingExists", [1, 6, 7, 18, 21, 22],
     ["original_target", "unit_shift_retained", "supplier_chain", "literal_return"],
     ["BWP24", "ASG18", "AMD12"],
     "Explicitly conditional on the full original StepStatement; Forms0 retained for the setting; no whole selected obligation closure."),
]

main = (HERE / "main.tex").read_bytes()
main_text = main.decode()
main_lines = main_text.splitlines(keepends=True)
claims = []
for num, title, dependencies, sg, inherited, scope_note in specs:
    cid = f"BNV{num}"
    start = next(i for i, line in enumerate(main_lines, 1) if line.strip() == "% BEGIN " + cid)
    end = next(i for i, line in enumerate(main_lines, 1) if line.strip() == "% END " + cid)
    proof = "".join(main_lines[start - 1:end]).encode()
    assert r"\begin{proof}" in proof.decode() and r"\end{proof}" in proof.decode()
    claims.append({
        "id": cid,
        "title": title,
        "introduced_in": VERSION,
        "classification": "B",
        "status": "complete human proof of the explicitly conditional implication" if num == 23 else "complete human proof at the explicitly stated scope",
        "depends_on": [f"BNV{i}" for i in dependencies] + inherited,
        "external_input_ids": ["BNV_STANDARD_ANALYSIS", "BNV_FINITE_COMPACT_THEORY"] + (["BNV_ORIGINAL_UNIT_SHIFT"] if num == 23 else []),
        "published_input_ids": [],
        "scope_note": scope_note,
        "source_groups": sg,
        "sources": [item for group in sg for item in source_groups[group]],
        "proof_location": {
            "file": COMPONENT + "/main.tex", "label": "claim:" + cid,
            "line_start": start, "line_end": end,
            "sha256": sha(proof), "bytes": len(proof),
        },
        "source_proof_is_not_human_proof": True,
        "whole_obligation_closure": False,
    })

manifest = {
    "schema": "rh-source-manifest/1",
    "artifact_version": VERSION,
    "component": COMPONENT,
    "source_commit": PIN,
    "snapshot_root": str(SNAPSHOT.relative_to(WORK)),
    "checkout_head_verified": True,
    "source_files": list(files.values()),
    "total_files": len(files),
    "total_bytes": sum(f["bytes"] for f in files.values()),
    "all_verified_equal_to_pinned_git_blob": True,
    "source_is_evidence_for_target_scope_not_a_substitute_for_the_human_proof": True,
    "no_lean_replay": True,
}
write_json("source_manifest.json", manifest)

inherited = []
for name, ids in [
    ("discrete_series_core", "DC1–DC13, specifically DC6/DC8/DC11/DC13"),
    ("bessel_wave_packets_v49", "BWP1–BWP3 and BWP24"),
    ("adelic_measures_v48", "AMD8 and supplied-form measure join"),
    ("adelic_setting_v47", "ASG supplied Forms0 setting scope"),
]:
    p = WORK / name / "main.tex"
    inherited.append({"component": name, "claims": ids, "file": str(p.relative_to(WORK)), "sha256": sha(p.read_bytes())})

classical = [
    {"id": "BNV_STANDARD_ANALYSIS", "status": "ordinary background retained",
     "content": "Finite-dimensional linear algebra; Haar existence/uniqueness and scaling; Lebesgue change of variables, Tonelli/Fubini and dominated convergence; matrix polar decomposition and finite exponential/log identities; derived smooth representation calculus. Gaussian nonvanishing and the varying-parameter limit are proved here."},
    {"id": "BNV_FINITE_COMPACT_THEORY", "status": "ordinary compact representation background retained as in DC1",
     "content": "Finite-dimensional compact unitary complete reducibility, Schur's lemma, and uniqueness of the irreducible compact highest-weight type. The needed compact average identity is proved in BNV17; no Bessel multiplicity-one theorem is used."},
    {"id": "BNV_ORIGINAL_UNIT_SHIFT", "status": "original source producer retained and not reconstructed",
     "content": "The complete StepStatement in LaplaceEstimates/StepDownStatement.lean, including both directions, endpoint HC/gap conditions and exclusion u_j != eta_s +/- 1/2; its IntS antecedent is proved by BNV1.",
     "source_path": lp("LaplaceEstimates/StepDownStatement.lean"),
     "source_commit": PIN, "source_is_not_human_proof": True,
     "used_only_by_claims": ["BNV23"]},
]
write_json("classical_inputs.json", {"schema": "rh-explicit-inputs/1", "component": COMPONENT, "inputs": classical})

reviews = []
review_file = HERE / "independent_review.json"
if review_file.exists():
    reviews.append({"file": "independent_review.json", "sha256": sha(review_file.read_bytes()), "content": json.loads(review_file.read_text())})
validation_file = HERE / "tex_validation.json"
validation = json.loads(validation_file.read_text()) if validation_file.exists() else {"status": "pending"}
provenance = {
    "schema": "rh-human-component-provenance/1",
    "artifact_version": VERSION,
    "date": "2026-11-23",
    "component": COMPONENT,
    "source_commit": PIN,
    "main_tex_sha256": sha(main),
    "proof_file_sha256": sha(main),
    "claims": claims,
    "source_groups": source_groups,
    "source_inventory": list(files.values()),
    "source_files": list(files.values()),
    "retained_foundations": classical,
    "inherited_human_inputs": inherited,
    "independent_reviews": reviews,
    "builder": "build_metadata.py",
    "validation": validation,
    "whole_obligation_closures": [],
    "no_lean_replay": True,
}
write_json("provenance.json", provenance)

contracts = {
    "schema": "rh-root-producer-contracts/1",
    "artifact_version": VERSION,
    "component": COMPONENT,
    "source_commit": PIN,
    "proof_file_sha256": sha(main),
    "endpoint_claim": "BNV23",
    "completed_original_substatements": [
        "Whole original IntSStatement with b>2rn^2, arbitrary weak Haar pair and free translates",
        "Whole original AdjGap, RaiseStep, LowerStep and WalkStatement",
        "Original cubic GapBig to GapLap and StepGap, plus whole LamTStatement",
        "Whole original PairingPropertiesStatement with explicit Vandermonde Cayley frame and exact c_a(t)=-2it",
        "Whole NsetExpInjectiveSurjective, including prescribed exponential Haar and polynomial logarithm bound",
        "Whole original CayleyMajorantBound",
        "Whole HighestWeightVectorUniformBounds and TangentPairingStatement",
        "Whole GaussianLimitHaar, with uniform eventual majorant and no added Gaussian positivity premise",
        "Whole WhittakerSchurOrthogonality with factor 1/dim(Vpi)",
        "Whole StepIBaseStatement, with all original k>=1 and parameter quantifiers",
        "Original BesselNZ to BesselAll transport at GapLap, and the literal arbitrary-representation endomorphism return",
        "Original StepStatement implies whole BesselNVGap; with inherited supplied Forms0 it implies ConcreteSettingExists",
    ],
    "remaining_exact_producer": {
        "id": "BNV_ORIGINAL_UNIT_SHIFT",
        "source_declaration": "ReciprocityTheory.ChartRestriction.DS.Lap.StepStatement",
        "source_file": lp("LaplaceEstimates/StepDownStatement.lean"),
        "statement": "IntSStatement implies that BesselNZ(epsilon,eta,u) is StepClosed(epsilon,u,h) for every original k,r,epsilon,u,h with StepGap, p=k+r and q=r+1.",
        "status": "not reconstructed here; original formal source verified at the stated pin",
        "next_producers": [
            "StepUp: standard tensor, complementary Capelli minor, shifted highest/Casimir quotient at lambda+e_s, nonzero period evaluation",
            "StepDown: dual tensor and matching shifted quotient/evaluation at lambda-e_s",
        ],
    },
    "not_claimed": [
        "Unconditional BesselNVGap or unconditional nonzero integral at every target row",
        "The original StepStatement, either of its two directions, or its substantive Capelli/tensor/quotient producers",
        "An unconditional ConcreteSettingExists, removal of supplied Forms0, or any ambient form supplier",
        "Original orbital/fiber or Siegel-Weil measure/character comparison",
        "Any complete RH, unrestricted Dirichlet-GRH, or whole selected obligation closure",
    ],
    "proposed_whole_obligation_closures": [],
    "whole_obligation_closures": [],
    "no_lean_replay": True,
}
write_json("contracts.json", contracts)
write_json("closure.json", {
    "schema": "rh-component-closure/1", "artifact_version": VERSION,
    "component": COMPONENT, "proof_file_sha256": sha(main),
    "human_claims": [c["id"] for c in claims],
    "fully_proved_claims_at_stated_scope": [c["id"] for c in claims if c["id"] != "BNV23"],
    "proved_conditional_implications": ["BNV23"],
    "remaining_source_producers": ["BNV_ORIGINAL_UNIT_SHIFT"],
    "whole_obligation_closures": [], "all_sources_pinned": True,
    "no_lean_replay": True,
})
report = f"""Bessel nonvanishing reconstruction, version {VERSION}
Source commit: {PIN}

The main manuscript contains 23 proved claims (BNV1--BNV23). BNV23 is
explicitly conditional on the original StepStatement. No whole selected
obligation is proposed for closure.

Substantive completed producers:
  * Original IntSStatement, with the exact 2rn^2 exponent threshold.
  * Original finite interlacing walk, including every forbidden-crossing check.
  * Explicit cyclic isotropic frame and exact c_a(t)=-2it character identity.
  * Exact exponential Haar; global logarithmic polar majorant.
  * Uniform highest-weight norm bounds and O_R(t^-1/2) Gaussian coefficient
    approximation, derived by an explicit scalar ODE.
  * Whole GaussianLimitHaar and exact 1/dim(Vpi) compact Schur factor.
  * Entire StepIBaseStatement for every original parameter and all sufficiently
    large integer deformations.
  * Full transport from existential BesselNZ to every original Bessel datum,
    every nonzero compact-type vector and every weak Haar pair.
  * Return to the prescribed endomorphism integral for every supplied
    IsDSHpk representation and every original lowest unit vector.

Remaining Bessel boundary:
The original StepStatement, with both +/-1 parameter propagation directions.
Its IntS antecedent has been proved here. The step proofs still require the
substantive Capelli/tensor/shifted-quotient/nonzero-evaluation reconstruction.
Only after that input is supplied does BNV23 yield BesselNVGap. BWP24 then
gives ConcreteSettingExists with the inherited Forms0 input retained.
Orbital/fiber comparisons are not begun or claimed closed in this component.

Evidence:
{len(files)} source files, {manifest['total_bytes']} bytes, copied from the pinned
checkout and checked byte-for-byte against git show at the pin.
The human proof is not a replay of the Lean proof. No Lean build was run.
TeX validation status at metadata generation: {validation.get('status', 'pending')}.
Independent review is recorded separately when available.
"""
(HERE / "report.txt").write_text(report)
(HERE / "README.txt").write_text(
    "BNV1--23 are in main.tex; the source target and exact remaining input are stated there.\n"
    "Read contracts.json before interpreting the endpoint as a closure.\n"
    "Rebuild metadata: python build_metadata.py\n"
    "Validate TeX: python validate_tex.py --format ../global_local_gain_v46/validation/pdflatex.fmt\n"
    "The source snapshot is ../source_snapshot_v0_50/analysis; every file is checked against the pin.\n"
)
print(json.dumps({
    "component": COMPONENT, "claims": len(claims), "source_files": len(files),
    "source_bytes": manifest["total_bytes"], "main_sha256": sha(main),
    "tex_status": validation.get("status"), "whole_obligation_closures": []
}, indent=2))
