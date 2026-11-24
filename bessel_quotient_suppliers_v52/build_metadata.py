#!/usr/bin/env python3
"""Bind the BQS human proofs to exact original source scopes; no Lean replay."""
from pathlib import Path
import hashlib
import json
import re
import subprocess

HERE = Path(__file__).resolve().parent
WORK = HERE.parent
REPO = Path("/workspace/scratch/249d32c24541/formal_source")
PIN = "7cbf7a0c32fca1badf05931879a37c3f8a2b03b4"
VERSION = "0.52"
COMPONENT = HERE.name
SNAPSHOT = HERE / "source_snapshot"
DS = "src/ReciprocityTheory/ReductiveGroups/DiscreteSeries/"
LAP = DS + "LaplaceOperators/"
URL = "https://github.com/CocoSgt/riemann-hypothesis-lean/blob/" + PIN + "/"

def sha(data):
    return hashlib.sha256(data).hexdigest()

def dump(name, value):
    (HERE / name).write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n")

def k(path):
    return LAP + "KTypeLemma/" + path + ".lean"

def l(path):
    return LAP + "LaplaceEstimates/" + path + ".lean"

def d(path):
    return DS + path + ".lean"

KDEFS = k("QuotientHighestWeightTensorStandard")
PDEFS = l("PsiDatumStatement")
SETTING = "src/Formalism/LocalToGlobal/SiegelLatticeTheory/HaarTransversals/UnitaryHaarProducts/SettingBlocks.lean"
CONCRETE = "src/Formalism/LocalToGlobal/SiegelLatticeTheory/HaarTransversals/ConcreteSettingExists.lean"

# Named declarations end immediately before the next top-level declaration.
# A None selector binds the complete file, including hypotheses and namespaces.
groups = {
    "tensor_scope": [
        (KDEFS, None),
        (d("IsInfUnitary"), None),
        (LAP + "EquivariantL2Space.lean", None),
        (k("SingleSmulFin"), "theorem gen_statement"),
    ],
    "euler": [
        (k("ProdShiftEeVOfCapelli"), "theorem prodShift_eeV_of_capelli"),
        (k("ProdShiftEeVOfCapelli"), "theorem prodShift_eeV_of_capelli'"),
        (k("StandardKTypeOfCentralChar"), None),
        (k("K1V"), None),
        (k("DualKTypeOfStandardKType"), None),
    ],
    "verma": [
        (k("VermaProductIdentity"), None),
        (k("VermaCone"), None),
        (k("VermaConeA"), None),
        (k("VermaConeB"), None),
        (k("VermaConeC"), None),
    ],
    "cyclic_model": [
        (k("IndicatorRholMem"), None),
        (k("RightHolRightHolEq"), None),
        (k("RightHolPowerDetDiag"), None),
    ],
    "transfer": [
        (k("TransferStatement"), None),
        (k("Transfer"), None),
    ],
    "formal_words": [
        (k("TensorActionApplyDual"), None),
        (k("SACommSES"), None),
        (k("LiftHighestWeightVector"), None),
        (k("InnerCompactWordActionAdjoint"), None),
    ],
    "trace": [
        (k("LowestKTypeVectorExists"), "theorem lowestKType_trace_integral"),
        (k("LowestKTypeVectorExists"), "theorem lowestKType_trace ("),
    ],
    "cone_transfer": [
        (k("MemEigenTensorSpaceIff"), "theorem lowestKType_tensor_lift"),
        (k("K2V"), None),
    ],
    "dual": [
        (k("CompRevRev"), None),
        (k("TensVdApply"), None),
        (k("DualLowestKTypeOfStandard"), None),
        (k("K2Vd"), None),
    ],
    "universal_line": [
        (l("QuotPA"), "theorem line_V"),
        (l("QuotMA"), "theorem line ("),
    ],
    "schmid_casimir": [
        (k("SchmidCas"), None),
        (d("DiscreteSeriesExistence/CFCore"), None),
        (d("BochnerInequality/Permute"), None),
        (d("BochnerInequality/SchForm"), None),
    ],
    "standard_image": [
        (k("ThreeAddLeGapBound"), "theorem shifted_weight_parameter"),
        (k("ThreeAddLeGapBound"), "theorem k3V"),
        (k("ConeNorm"), None),
    ],
    "dual_image": [
        (k("CasimirValueSubSingle"), "theorem k3Vd"),
    ],
    "closure": [
        (d("AnalyticVectors/Closure"), None),
        (d("DiscreteSeriesExistence/PropsKfin"), None),
        (d("BochnerInequality/CasimirGapAtNoncompactWeight"), None),
        (d("DiscreteSeriesExistence/BridgeExpK"), None),
    ],
    "generic_quotient": [
        (l("ImageLeClosGen"), None),
    ],
    "smooth_period": [
        (l("QuotMA"), "theorem exists_lin"),
        (l("ToL2CongrOnUnitaryBis"), None),
        (d("DiscreteSeriesExistence/RightDerivativeToL2"), None),
        (d("DiscreteSeriesExistence/IsSmoothL2OfCasimirEigen"), "def IsSmoothL2"),
        ("src/Formalism/RealPlaceAnalysis/SmoothOnG.lean", None),
        (PDEFS, "def xJ"),
        (PDEFS, "def coefX"),
        (PDEFS, "def tMap ("),
        (PDEFS, "def tMapD"),
        (PDEFS, "def per ("),
    ],
    "original_quotients": [
        (PDEFS, "def QuotPStatement"),
        (PDEFS, "def QuotMStatement"),
        (l("QuotP"), None),
        (l("QuotM"), None),
    ],
    "step_join": [
        (l("StepDownStatement"), None),
        (l("StepDown"), None),
        (l("StepUp"), None),
    ],
    "original_endpoints": [
        (SETTING, "def BesselNVGap"),
        (SETTING, "theorem settingExists_of_inputs"),
        (CONCRETE, None),
    ],
}

assert subprocess.check_output(
    ["git", "-C", str(REPO), "rev-parse", "HEAD"], text=True
).strip() == PIN
files = {}
for path in sorted({path for entries in groups.values() for path, _ in entries}):
    blob = subprocess.check_output(["git", "-C", str(REPO), "show", PIN + ":" + path])
    assert (REPO / path).read_bytes() == blob, path
    target = SNAPSHOT / path
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_bytes(blob)
    files[path] = {
        "path": path, "snapshot_path": str(target.relative_to(WORK)),
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
            matches = [i for i, line in enumerate(lines, 1)
                       if line.decode().startswith(declaration)]
            assert matches, (path, declaration)
            first = matches[0]
            ends = [i for i in range(first + 1, len(lines) + 1)
                    if lines[i - 1].decode().startswith(
                        ("def ", "theorem ", "lemma ", "end "))]
            last = min(ends) - 1 if ends else len(lines)
            while last > first and not lines[last - 1].strip():
                last -= 1
        selected = b"".join(lines[first - 1:last])
        source_groups[group].append({
            "id": f"BQS_{group}_{number:02d}", "path": path,
            "line_start": first, "line_end": last,
            "declaration": declaration or "Complete pinned file, including contextual hypotheses",
            "file_sha256": info["sha256"], "range_sha256": sha(selected),
            "range_bytes": len(selected), "source_commit": PIN,
            "verified_equal_to_pinned_git_blob": True,
            "url": URL + path + f"#L{first}-L{last}",
        })

specs = [
    (1, "Tensor generation, Euler commutation and finite compact hulls", [],
     ["tensor_scope"], [],
     "All complex matrix-unit modules and all generated-module tuples; no completion."),
    (2, "Both full Euler polynomials from the exact ordered adjugate identities", [],
     ["tensor_scope", "euler"], ["BST8"],
     "Any stable complex module with scalar Capelli polynomial, including repeated roots and rank zero."),
    (3, "Full original standard/dual lowest-type Euler statements and projectors", [2],
     ["tensor_scope", "euler"], ["BSP2", "BSP3"],
     "Every original unitary datum at the unchanged hNeed gap; no chosen coefficient identity added."),
    (4, "Full VermaProductIdentity", [1],
     ["tensor_scope", "verma"], [],
     "Every cyclic lowest-weight module; no strictness, integrality, positivity or nonzero-generator assumption."),
    (5, "Full VermaConeStatement and both extremal lines", [1, 4],
     ["tensor_scope", "verma"], [],
     "Every simultaneous weight vector in either selected Euler eigenspace; no highest-vector or unitary requirement."),
    (6, "The actual zero-extended principal-minor cyclic model", [],
     ["cyclic_model"], ["DC2"],
     "Exact Rhol action and inverse-minor domain, with no smoothness assertion across the zero-extension boundary."),
    (7, "Full TransferStatement through the actual compact average", [],
     ["transfer"], ["DC2", "DC3"],
     "Every finite family of arbitrary complex matrix words, every group element and the exact ordered derivatives."),
    (8, "Formal word action, Euler maps and finite highest-vector lifts", [1],
     ["formal_words"], [],
     "Arbitrary compact-unitary derived module, possibly incomplete; finite word hulls only."),
    (9, "Full lowestKType_trace_integral and trace-kernel implication", [6, 7, 8],
     ["trace", "formal_words", "transfer"], ["DC3"],
     "Every compact-stable formal subspace; supplied exact coefficient identity and HC parameter, no additional gap or Casimir."),
    (10, "Full abstract lowestKType_tensor_lift", [4, 5],
     ["cone_transfer"], [],
     "Arbitrary formal and target vector spaces and target operator family; only original compact relations and universal trace premise."),
    (11, "Full EigenspaceWeightConeStandard", [6, 8, 9, 10],
     ["tensor_scope", "cone_transfer", "trace"], ["BSP2"],
     "Original all-data cone and extremal-line clauses; exact normalized kernel link is supplied rather than assumed."),
    (12, "Actual signed reversal and full EigenspaceWeightConeDual", [11],
     ["tensor_scope", "dual"], [],
     "Same Hilbert space and actual twisted group action; exact Euler sign, reversed parameter, gap and compact weights."),
    (13, "One highest-line witness before every target and map", [1, 11, 12],
     ["universal_line"], [],
     "Full abstract line theorem with no target norm, bracket or completeness; original standard and dual applications."),
    (14, "Full SchmidCasimirStatement on incomplete targets", [],
     ["tensor_scope", "schmid_casimir"], ["DC1", "DC8", "DC9", "DC11"],
     "Arbitrary complex Casimir scalar, exact hNeed < gap+2 margin, no target group action or completion."),
    (15, "The candidate shifted parameter at the exact h-2 gap", [],
     ["standard_image"], [],
     "Integral root cone and original partial-sum upper bound; no strengthening of the gap."),
    (16, "Full QuotientHighestWeightTensorStandard", [1, 3, 11, 13, 14, 15],
     ["tensor_scope", "standard_image"], ["DC8", "BST10"],
     "Every nonzero arbitrary tuple image and every infinitesimally unitary target, possibly incomplete; shifted strictness only."),
    (17, "Full QuotientHighestWeightTensorDual", [12, 16],
     ["tensor_scope", "dual", "dual_image"], [],
     "All original source and incomplete-target quantifiers, transported by complex-linear signed reversal."),
    (18, "Original group-invariant closure and weak-gap compact-finite theorem", [],
     ["closure", "tensor_scope"], ["DC7", "DC8", "DC9", "DC10"],
     "Closure invariance without completeness or gap; full data_kfin_le under StdGap, without added integrality or constructive gap."),
    (19, "Full image_le_closGen", [18],
     ["generic_quotient"], [],
     "Arbitrary source operators with no bracket, stability, X <= G or gap hypothesis; exact universal image and line inputs."),
    (20, "Full quot_generic", [18, 19],
     ["generic_quotient"], [],
     "Arbitrary source operators and map, original weak gap, one universal highest line, finite compact hulls and exact saturation."),
    (21, "Full smooth lift and actual simultaneous period kernel", [1],
     ["smooth_period", "original_quotients"], ["BST5", "BSP5", "BNV1"],
     "Original IsSmoothL2 lift and all-data period kernel with fixed character, vector, Haar pair and Cayley matrix."),
    (22, "Full original QuotPStatement and QuotMStatement", [1, 13, 16, 17, 20, 21],
     ["original_quotients", "tensor_scope"], ["BSP1"],
     "All six original outputs, arbitrary Euler tuples, exact smooth image, actual compact action and period injectivity."),
    (23, "Full StepStatement and BesselNVGap, with supplied-form setting", [22],
     ["step_join", "original_endpoints"],
     ["BSE7", "BSE8", "BSE9", "BST5", "BST9", "BST11", "BSP10",
      "BNV1", "BNV6", "BNV7", "BNV18", "BNV21", "BNV22", "BNV23",
      "BWP24", "ASG18", "AMD17"],
     "Original endomorphism integral for every original datum; ConcreteSettingExists only on the inherited supplied Forms0 scope."),
]

main = (HERE / "main.tex").read_bytes()
lines = main.decode().splitlines(keepends=True)
claims = []
for number, title, own, source_names, inherited_ids, scope in specs:
    identifier = f"BQS{number}"
    first = next(i for i, line in enumerate(lines, 1) if line.strip() == "% BEGIN " + identifier)
    last = next(i for i, line in enumerate(lines, 1) if line.strip() == "% END " + identifier)
    proof = "".join(lines[first - 1:last]).encode()
    assert b"\\begin{proof}" in proof and b"\\end{proof}" in proof
    claims.append({
        "id": identifier, "title": title, "introduced_in": VERSION, "classification": "B",
        "status": "complete human proof at the explicitly stated scope",
        "depends_on": [f"BQS{i}" for i in own] + inherited_ids,
        "external_input_ids": ["BQS_STANDARD_ANALYSIS", "BQS_FINITE_COMPACT_THEORY"]
                              + (["BQS_SUPPLIED_FORMS0"] if number == 23 else []),
        "published_input_ids": [], "scope_note": scope, "source_groups": source_names,
        "sources": [entry for name in source_names for entry in source_groups[name]],
        "proof_location": {
            "file": COMPONENT + "/main.tex", "label": "claim:" + identifier,
            "line_start": first, "line_end": last, "sha256": sha(proof), "bytes": len(proof),
        },
        "source_proof_is_not_human_proof": True, "whole_obligation_closure": False,
    })

inherited_components = {
    "discrete_series_core": ["DC1", "DC2", "DC3", "DC7", "DC8", "DC9", "DC10", "DC11"],
    "bessel_nonvanishing_v50": ["BNV1", "BNV6", "BNV7", "BNV18", "BNV21", "BNV22", "BNV23"],
    "bessel_weight_propagation_v50": ["BSP1", "BSP2", "BSP3", "BSP5", "BSP10"],
    "bessel_shift_suppliers_v51": ["BST5", "BST8", "BST9", "BST10", "BST11"],
    "bessel_period_evaluation_v51": ["BSE7", "BSE8", "BSE9"],
    "bessel_wave_packets_v49": ["BWP24"],
    "adelic_setting_v47": ["ASG18"],
    "adelic_measures_v48": ["AMD17"],
}
inherited = []
inherited_index = {}
for component, identifiers in inherited_components.items():
    path = WORK / component / "main.tex"
    data = path.read_bytes()
    old_lines = data.splitlines(keepends=True)
    old = json.loads((WORK / component / "provenance.json").read_text())
    index = {entry["id"]: entry for entry in old["claims"]}
    bindings = []
    for identifier in identifiers:
        entry = index[identifier]
        loc = entry["proof_location"]
        first, last = loc["line_start"], loc["line_end"]
        selected = b"".join(old_lines[first - 1:last])
        bound = loc.get("sha256", loc.get("paragraph_sha256"))
        assert bound and bound == sha(selected), (component, identifier, bound, sha(selected))
        binding = {
            "id": identifier, "file": str(path.relative_to(WORK)),
            "line_start": first, "line_end": last, "sha256": sha(selected),
            "bytes": len(selected), "scope": entry.get("scope_note", entry.get("title")),
        }
        bindings.append(binding)
        inherited_index[identifier] = binding
    inherited.append({
        "component": component, "claims": identifiers,
        "file": str(path.relative_to(WORK)), "sha256": sha(data),
        "proof_hashes": {b["id"]: b["sha256"] for b in bindings},
        "claim_bindings": bindings,
    })

known = {c["id"] for c in claims} | set(inherited_index)
assert all(dep in known for c in claims for dep in c["depends_on"])
assert len({c["id"] for c in claims}) == 23
foundations = [
    {
        "id": "BQS_STANDARD_ANALYSIS", "status": "ordinary mathematical background retained",
        "content": "Finite-dimensional holomorphic differentiation, compact Haar integration, local Lie group charts and matrix logarithms, elementary differential equations, Taylor's theorem, Bochner integration, L2 density/strong continuity, and bounded orthogonal projection in a complete Hilbert space. No target completion is assumed in K3. The actual derivatives, estimates, closure passage and period kernel are proved in the indicated human claims or inherited proofs.",
    },
    {
        "id": "BQS_FINITE_COMPACT_THEORY", "status": "ordinary finite-dimensional background retained",
        "content": "Finite spectral decomposition and Schur orthogonality for compact unitary modules; orthogonal complements only in finite-dimensional spaces where used for incomplete targets; PBW normal-order spanning via the displayed matrix-unit commutators; algebraic complements of vector subspaces. No discrete-series classification or Bessel multiplicity-one theorem is imported.",
    },
    {
        "id": "BQS_SUPPLIED_FORMS0", "status": "exact original given datum retained",
        "used_only_by_claims": ["BQS23"],
        "content": "The inherited supplied Forms0 datum in the original setting construction. It is required only for BQS23's ConcreteSettingExists consequence, not for QuotP/QuotM, StepStatement or BesselNVGap. No ambient Forms0 existence supplier is asserted.",
        "source_file": CONCRETE, "source_commit": PIN,
    },
]
manifest = {
    "schema": "rh-source-manifest/1", "artifact_version": VERSION, "component": COMPONENT,
    "source_commit": PIN, "snapshot_root": str(SNAPSHOT.relative_to(WORK)),
    "checkout_head_verified": True, "source_files": list(files.values()),
    "total_files": len(files), "total_bytes": sum(f["bytes"] for f in files.values()),
    "distinct_source_ranges": len({(r["path"], r["line_start"], r["line_end"])
                                  for group in source_groups.values() for r in group}),
    "all_verified_equal_to_pinned_git_blob": True, "no_lean_replay": True,
    "source_is_evidence_for_target_scope_not_a_substitute_for_the_human_proof": True,
}
validation = json.loads((HERE / "tex_validation.json").read_text())
assert validation["proof_file_sha256"] == sha(main)
assert validation["status"] == "PASS"
reviews = []
for review_file in sorted(HERE.glob("independent_review*.json")):
    reviews.append({
        "file": str(review_file.relative_to(WORK)), "sha256": sha(review_file.read_bytes()),
        "content": json.loads(review_file.read_text()),
    })
dump("source_manifest.json", manifest)
dump("inherited_inputs.json", {
    "schema": "rh-inherited-human-inputs/1", "artifact_version": VERSION,
    "component": COMPONENT, "proof_file_sha256": sha(main), "components": inherited,
    "all_current_proof_ranges_verified": True,
})
dump("classical_inputs.json", {
    "schema": "rh-explicit-inputs/1", "component": COMPONENT, "inputs": foundations,
    "new_unreconstructed_published_mathematical_premises": [],
})
dump("provenance.json", {
    "schema": "rh-human-component-provenance/1", "artifact_version": VERSION,
    "date": "2026-11-23", "component": COMPONENT, "source_commit": PIN,
    "main_tex_sha256": sha(main), "proof_file_sha256": sha(main), "claims": claims,
    "source_groups": source_groups, "source_files": list(files.values()),
    "source_inventory": list(files.values()), "retained_foundations": foundations,
    "inherited_human_inputs": inherited, "independent_reviews": reviews,
    "builder": COMPONENT + "/build_metadata.py", "validation": validation,
    "whole_obligation_closures": [], "no_lean_replay": True,
})
completed = [
    "GenStatement and both full Euler annihilating polynomials/projectors",
    "VermaProductIdentity and VermaConeStatement at their arbitrary-module scopes",
    "Actual principal-minor cyclic module and full TransferStatement",
    "Full trace-kernel implication and lowestKType_tensor_lift",
    "EigenspaceWeightConeStandard and EigenspaceWeightConeDual",
    "One universal highest-line witness before every target and map",
    "SchmidCasimirStatement and both QuotientHighestWeightTensor statements on incomplete targets",
    "Original closure_genSub_stable and full data_kfin_le at StdGap",
    "Full image_le_closGen, quot_generic and exists_lin",
    "Actual period kernel, fixed-data saturation and all six outputs of QuotPStatement/QuotMStatement",
    "Full original StepStatement, including StepUp and StepDown",
    "Full original BesselNVGap endomorphism-valued integral",
]
remaining = [
    "Ambient Forms0 supply remains separate from the supplied-Forms0 setting consequence",
    "Orbital/fiber comparison and Siegel-Weil comparison",
    "Local uniqueness and downstream global spectral identifications",
]
dump("contracts.json", {
    "schema": "rh-root-producer-contracts/1", "artifact_version": VERSION,
    "component": COMPONENT, "source_commit": PIN, "proof_file_sha256": sha(main),
    "endpoint_claim": "BQS23", "quotient_endpoint_claim": "BQS22",
    "completed_original_substatements": completed,
    "remaining_exact_producers_for_QuotP_QuotM_Step_BesselNVGap": [],
    "conditional_join": "ConcreteSettingExists follows on exactly the inherited supplied Forms0 scope; that datum is not constructed here.",
    "remaining_downstream_boundaries": remaining,
    "shared_data_preserved": [
        "Original representation/domain/lowest type, compact group and exact hNeed/StepGap",
        "Arbitrary selected Euler tuple and original shifted parameter",
        "One y_s chosen before every target intertwiner, including incomplete targets",
        "Fixed z,c,u,pi,muW,muN,P,x0,w,xi throughout the actual period-kernel quotient",
        "Actual smooth image and pointwise-on-group representative relation",
        "All-data original endomorphism integral and inherited Forms0 choice order",
    ],
    "not_claimed": [
        "Unconditional ambient Forms0 existence",
        "Whole GLOBAL_SPECTRAL selected obligation closure",
        "New orbital/fiber, Siegel-Weil or local uniqueness supplier",
        "Unrestricted RH or Dirichlet-GRH final endpoint",
    ],
    "proposed_whole_obligation_closures": [], "whole_obligation_closures": [],
    "no_lean_replay": True,
})
dump("closure.json", {
    "schema": "rh-component-closure/1", "artifact_version": VERSION,
    "component": COMPONENT, "proof_file_sha256": sha(main),
    "human_claims": [c["id"] for c in claims],
    "fully_proved_claims_at_stated_scope": [c["id"] for c in claims],
    "completed_original_producer_contracts": ["QuotPStatement", "QuotMStatement", "StepStatement", "BesselNVGap"],
    "conditional_consequences": [{"claim": "BQS23", "consequence": "ConcreteSettingExists",
                                  "retained_input": "Original supplied Forms0 datum"}],
    "remaining_source_producers_in_this_quotient_chain": [],
    "remaining_downstream_boundaries": remaining,
    "whole_obligation_closures": [], "all_sources_pinned": True, "no_lean_replay": True,
})
dump("claim_dag.json", {
    "schema": "rh-claim-dependency-dag/1", "artifact_version": VERSION,
    "component": COMPONENT, "proof_file_sha256": sha(main),
    "nodes": [{"id": c["id"], "depends_on": c["depends_on"]} for c in claims],
    "inherited_nodes": sorted(inherited_index), "all_dependencies_resolve": True,
})
words = len(re.findall(r"\S+", main.decode()))
(HERE / "report.txt").write_text(f"""Bessel quotient suppliers, version {VERSION}
Formal source pin: {PIN}
Frozen main SHA-256: {sha(main)}

Twenty-three complete human claims, BQS1--BQS23; {words} whitespace-delimited TeX words.
The primary endpoint BQS22 proves full original QuotPStatement and QuotMStatement.
BQS23 consumes reviewed BST/BSE/BSP/BNV and proves full StepStatement and BesselNVGap.
The endomorphism-valued integral has the original universal representation, compact
type, lowest vector, nondegenerate character, Cayley and weak-Haar quantifiers.
ConcreteSettingExists is obtained only with the original supplied Forms0 datum.
No whole selected obligation is closed, and GLOBAL_SPECTRAL remains open.

Mathematical route:
  BQS1--BQS5: both Euler annihilators/projectors, exact cyclic flags,
    integral root cones and extremal lines for arbitrary complex modules.
  BQS6--BQS12: actual principal-minor model, compact derivative transfer,
    formal compact word space, universal trace kernel, and both actual K2 cones.
  BQS13--BQS17: one highest-line witness before every target/map;
    Schmid/Casimir comparison on a diagonal lowest type using inherited DC9;
    minimum integral-cone height and the exact h-2 margin give both K3 types.
  BQS18--BQS21: actual group-invariant closure, weak-gap compact-finite closure,
    the full arbitrary-source generic quotient, smooth lifting, and the fixed
    actual simultaneous period kernel with exact saturation.
  BQS22--BQS23: both full original quotients; two-sided propagation; full
    original Bessel endomorphism nonvanishing; supplied-form global setting.

Scope safeguards:
  * K3 targets may be incomplete and have only an infinitesimal unitary action.
  * The generic quotient source operators need not satisfy bracket relations.
  * The line witness is chosen once before all target maps.
  * The weak StdGap closure theorem does not acquire a constructive-gap premise.
  * The actual compact group and all six original quotient outputs are retained.
  * Wf consists of complex-valued functions ON matrices, with exact smooth L2 image.
  * No abstract branching functional replaces the fixed actual period kernel.
  * The supplied Forms0 scope is retained; ambient forms/global comparisons remain.

Verification:
{len(files)} source files, {manifest['distinct_source_ranges']} distinct exact ranges,
{manifest['total_bytes']} bytes verified against the pinned Git blobs.
Every new proof block and every inherited proof range is hash-bound.
All artifact and snapshot paths are root-relative within the reconstructed bundle.
Two-pass draft TeX {validation['status']}; no errors, undefined references, missing
characters or overfull boxes. No PDF and no Lean replay.
Independent review is recorded separately after freeze.
""")
(HERE / "README.txt").write_text(
    "Read main.tex for BQS1--BQS23 and contracts.json for completed and retained scopes.\n"
    "Draft check: python validate_tex.py --format ../global_local_gain_v46/validation/pdflatex.fmt\n"
    "Build source/proof bindings: python build_metadata.py\n"
    "Check existing bindings without rebuilding: python verify_hashes.py\n"
    "Source declarations identify exact targets; the human proofs supply the mathematics.\n"
)
print(json.dumps({
    "component": COMPONENT, "claims": len(claims), "source_files": len(files),
    "source_ranges": manifest["distinct_source_ranges"], "source_bytes": manifest["total_bytes"],
    "main_sha256": sha(main), "tex_status": validation["status"],
    "completed_endpoints": ["QuotP", "QuotM", "StepStatement", "BesselNVGap"],
    "whole_obligation_closures": [],
}, indent=2))
