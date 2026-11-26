#!/usr/bin/env python3
"""Bind the independently authored v0.49 semantic-scope review to final bytes.

The mathematical scope judgments below come from the reviewer's reading of
the original contracts, current endpoint proofs, integration narrative and
final reports.  Mechanical assertions protect those bindings and the stated
inventory.  This is not a Lean audit, a new review of every historical proof,
or a replacement for the separately authored component proof reviews.
"""
from pathlib import Path
from collections import Counter
import hashlib
import json
import re
import subprocess

ROOT = Path(__file__).resolve().parent.parent
SOURCE = ROOT.parent / "formal_source"
PIN = "7cbf7a0c32fca1badf05931879a37c3f8a2b03b4"


def read(name):
    return json.loads((ROOT / name).read_text())


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def binding(name, scope):
    return {"path": name, "sha256": digest(ROOT / name), "review_scope": scope}


cfg = read("increment_v0_49.json")
stats = read("integration_stats_v0_49.json")
before = read("dependency_audit_v0_48/obligation_map.json")
after = read("dependency_audit_v0_49/obligation_map.json")
old_nodes = {n["id"]: n for n in before["nodes"]}
nodes = {n["id"]: n for n in after["nodes"]}
old_open = {n["id"]: n for n in read("dependency_audit_v0_48/remaining_leaf_register.json")["records"]}
open_nodes = {n["id"]: n for n in read("dependency_audit_v0_49/remaining_leaf_register.json")["records"]}
closed = {"GLOBAL_LOCAL_GAIN"}
qualified = {"AUT_UNRAM_COEF", "GLOBAL_RETAINED_DEFECT", "GLOBAL_SPECTRAL",
             "DESIGN_CHOICES_COMMON", "BASE_THETA_RATIONAL_TESTS",
             "SECOND_LAYER_COMPATIBLE_SELECTION"}
assert cfg["source_commit"] == PIN
assert old_nodes.keys() == nodes.keys()
assert set(old_open) - set(open_nodes) == closed
assert not (set(open_nodes) - set(old_open))
assert set(cfg["closed_selected_leaves"]) == closed
assert set(cfg["updated_contracts"]) == qualified
assert len(nodes) == 121
assert sum(len(n["requires"]) for n in nodes.values()) == 161
for key in nodes:
    assert nodes[key]["requires"] == old_nodes[key]["requires"]
    assert nodes[key]["gate"] == old_nodes[key]["gate"]
    if key not in closed:
        for field in ["category", "kind", "status"]:
            assert nodes[key].get(field) == old_nodes[key].get(field), (key, field)
    if key in qualified:
        assert nodes[key]["contract"].startswith(old_nodes[key]["contract"])
        assert nodes[key]["contract"] == cfg["updated_contracts"][key]
    else:
        assert nodes[key]["contract"] == old_nodes[key]["contract"]
assert old_nodes["GLOBAL_LOCAL_GAIN"]["category"] == "C"
assert nodes["GLOBAL_LOCAL_GAIN"]["category"] == "B"
assert nodes["GLOBAL_LOCAL_GAIN"]["status"] == "proved_in_stated_scope"
assert Counter(n["category"] for n in open_nodes.values()) == {"C": 17, "B": 7}
assert stats == {
    "new_claims": 74, "cumulative_claims": 3014,
    "selected_nodes": 121, "selected_edges": 161,
    "open_count": 24, "open_categories": {"C": 17, "B": 7},
    "shared_open": 17, "extra_grh_open": 7,
    "new_source_files_checked": 117, "new_unique_source_ranges_checked": 167,
}
assert all(n["contract"] in (ROOT / "RH_dependency_audit_v0_49.txt").read_text()
           for n in open_nodes.values())
coverage = read("dependency_audit_v0_49/route_coverage.json")
assert coverage["ordinary_rh_open_leaf_count"] == 17
assert coverage["dirichlet_grh_open_leaf_count"] == 24
assert coverage["shared_open_leaf_count"] == 17
assert len(coverage["dirichlet_grh_only_open_leaf_ids"]) == 7
assert not coverage["ordinary_rh_only_open_leaf_ids"]

closure_review = read(cfg["closure_reviews"]["GLOBAL_LOCAL_GAIN"])
exact = closure_review["selected_whole_contract_reviewed"]
assert exact["id"] == "GLOBAL_LOCAL_GAIN"
assert exact["full_original_contract_closed_in_stated_scope"]
assert exact["baseline_contract_sha256"] == hashlib.sha256(
    old_nodes["GLOBAL_LOCAL_GAIN"]["contract"].encode()).hexdigest()
comparison = read("witness_realization_v49/closure_comparison.json")
assert comparison["baseline_contract_verbatim"] == old_nodes["GLOBAL_LOCAL_GAIN"]["contract"]
assert not comparison["selected_family_TSel_premise_added"]
assert not comparison["common_family_nonemptiness_claimed"]
assert not comparison["full_RecT_or_TSel_claimed"]

provenance = read("provenance.json")
checkpoint = read("continuation_checkpoint.json")
targets = read("next_source_targets.json")
assert provenance["scope"] == checkpoint["status"] == targets["current_status_v0_49"] == cfg["status"]
assert provenance["version_0_49_local_conclusions"] == checkpoint["new_in_this_version"] == cfg["local_conclusions"]
assert provenance["component_input_boundaries_v0_49"] == checkpoint["remaining_major_inputs"] == cfg["remaining_major_inputs"]
assert checkpoint["next_targets"] == targets["next_local_priority"] == cfg["next_targets"]
assert targets["version_0_49_precision_notes"] == cfg["local_conclusions"] + cfg["remaining_major_inputs"]
for key, value in checkpoint["current_dependency_audit"].items():
    if key not in {"artifact_version", "scope"}:
        assert value.startswith("dependency_audit_v0_49/") and (ROOT / value).exists()
assert checkpoint["current_deliverable"]["main"] == "RH_readable_reconstruction_v0_49.tex"
assert checkpoint["current_deliverable"]["new_chapters"] == "RH_new_proofs_v0_49.tex"

proof_hashes = {
    "unramified_coefficient_extension_v49": "d39f5d881f5953bcd229876cd42f1f33f2f93d4d1d3c6cdb1762d93f38e0d68a",
    "bessel_wave_packets_v49": "7b0f0d374d1f0d5244416cb5d6ccaf584d006609a30523588a3ef7555fad85c3",
    "holomorphic_uniformization_v49": "84c73ce3b9c3f23510df99986e2a767c1ec8e98eca9b0ff046ea96a64e6bb0f1",
    "witness_realization_v49": "11bd6e9d80c617f7d95843ee5d97bbd787420269c8eceed0cc1841ebe728c235",
}
new_claims = []
for component in cfg["components"]:
    assert digest(ROOT / component / "main.tex") == proof_hashes[component]
    new_claims.extend(read(component + "/provenance.json")["claims"])
assert len(new_claims) == 74
assert Counter(c["classification"] for c in new_claims) == {"B": 74}
assert not cfg["published_applications"]
assert len({s["path"] for c in new_claims for s in c.get("sources", []) if "path" in s}) == 117
assert len({(s["path"], s["line_start"], s["line_end"])
            for c in new_claims for s in c.get("sources", []) if "line_start" in s}) == 167

tex = read("tex_validation.json")
assert tex["artifact_version"] == "0.49"
for item in tex["documents"]:
    assert digest(ROOT / item["tex_filename"]) == item["tex_sha256"]
    assert item["syntax_compile_succeeded"]
    assert not item["undefined_references_or_citations"]
    assert item["missing_character_warnings"] == 0
    assert not item["pdf_generated"] and not item["pdf_visual_review_performed"]
assert [d["overfull_box_warnings"] for d in tex["documents"]] == [0, 53]
progress = (ROOT / "RH_reconstruction_progress_v0_49.txt").read_text()
for name in ["increment_v0_49.json", "integration_stats_v0_49.json"]:
    assert name + " SHA256: " + digest(ROOT / name) in progress
assert "single open arithmetic producer input" in " ".join(progress.split())
assert "GD.gen" in progress
assert "allTest_of_secBaseChange" in progress
assert "prime3," not in (ROOT / "README.md").read_text()
final_output_hashes = {
    "increment_v0_49.json": "8d6c72aa988e478e9d76759c04cba742b5bc4759119fe0db98b05666ba96bdc2",
    "RH_new_proofs_v0_49.tex": "63ccfb98e61e54744a8d0994b2e5e663d14934a97e7ccb8a028042816ecbee31",
    "RH_readable_reconstruction_v0_49.tex": "b318d91062f01960bfa72bf936a135ca7d7fe4ceddb52b216e7f0e6717a2d00f",
    "RH_reconstruction_progress_v0_49.txt": "fb53db3df24b88e6532c944692b5645f5eb8e85643e477421b1838a52d9c5a9a",
    "README.txt": "b6c114186fa620e1fcdfcf25d3182b5330fe6b2bdadba5d6b863804f7d3497dc",
}
assert all(digest(ROOT / name) == expected for name, expected in final_output_hashes.items())

reviewed = []
script_scope = "Current semantic scope, exact selected closure, choice order, retained original premises and generated narrative; exhaustive preservation/source mechanics belong to the separate integration audit."
for path in ["increment_v0_49.json", "configure_v0_49.py", "assemble_v0_49.py",
             "integrate_v0_49.py", "write_progress_v0_49.py", "v0_49_frontmatter.tex",
             "v0_49_audit_intro.tex"]:
    reviewed.append(binding(path, script_scope))
for path, scope in [
    ("provenance.json", "Current scope, version_0_49_local_conclusions, current_boundary_authority, component_input_boundaries_v0_49, classification and new endpoint graph; not a rereading of every inherited claim."),
    ("continuation_checkpoint.json", "Current status, new_in_this_version, remaining_major_inputs, next_targets, current_dependency_audit, current_deliverable and version_0_49_update."),
    ("next_source_targets.json", "Current v0.49 status, precision notes, selected-frontier paths and next_local_priority; earlier version-specific records remain historical."),
]:
    reviewed.append(binding(path, scope))
for version, names in [
    ("0_48", ["obligation_map.json", "remaining_leaf_register.json"]),
    ("0_49", ["obligation_map.json", "remaining_leaf_register.json", "route_coverage.json",
              "closure_delta.json", "target_disposition.json", "published_applications.json"]),
]:
    for name in names:
        reviewed.append(binding("dependency_audit_v" + version + "/" + name,
            "Original whole-contract scope, exact single LinkG closure, unchanged requires edges and remaining categories. Six qualifications append preserved contract text; target-disposition history is not freshly re-reviewed in full."))

for component in cfg["components"]:
    reviewed.append(binding(component + "/main.tex",
        "Focused endpoint, normalization, quantifier and retained-premise reading. This is not a fresh independent proof review of every claim; separate component mathematical reviews provide that coverage. HUF is authored by this reviewer and independently reviewed by root."))
    for name in ["contracts.json", "original_contracts.json", "closure.json", "closure_comparison.json",
                 "retained_foundations.json", "classical_inputs.json", "published_inputs.json"]:
        if (ROOT / component / name).exists():
            reviewed.append(binding(component + "/" + name,
                "Exact original endpoint and retained-input boundaries, separating numbered deductions, named foundations, supplied original data and still-open producer statements."))
    reviewed.append(binding(component + "/provenance.json",
        "Current classification, exact endpoint identifiers, inherited input and named-foundation boundaries, and final independent review coverage."))
    for path in sorted((ROOT / component).glob("review_*.json")):
        record = json.loads(path.read_text())
        assert record.get("result", record.get("status")) == "PASS"
        assert record.get("proof_sha256", record.get("proof_file_sha256")) == digest(ROOT / component / "main.tex")
        reviewed.append(binding(str(path.relative_to(ROOT)),
            "Separately authored mathematical/source review, proof hash and actually reviewed block scope. Root's WRS6–WRS10 review additionally binds the original selected whole-contract text."))

generated = [binding(path,
    "Final current front matter, endpoint summaries, complete current audit, remaining-input and continuation narrative, inventory and validation scope. The cumulative binding does not claim a new reading of every historical proof.")
    for path in ["RH_new_proofs_v0_49.tex", "RH_readable_reconstruction_v0_49.tex",
                 "dependency_audit_v0_49/main.tex", "RH_dependency_audit_v0_49.txt",
                 "README.md", "RH_reconstruction_progress_v0_49.txt", "README.txt",
                 "integration_stats_v0_49.json", "tex_validation.json"]]

selected = {
    "witness_realization_v49": ["WRS" + str(i) for i in range(6, 11)],
    "unramified_coefficient_extension_v49": ["UCE9", "UCE12", "UCE16", "UCE17", "UCE18", "UCE19"],
    "bessel_wave_packets_v49": ["BWP7", "BWP18", "BWP19", "BWP20", "BWP21", "BWP22", "BWP23", "BWP24"],
    "holomorphic_uniformization_v49": ["HUF6", "HUF8", "HUF9", "HUF10", "HUF12", "HUF15", "HUF16", "HUF20", "HUF21"],
}
blocks = []
for component, ids in selected.items():
    data = (ROOT / component / "main.tex").read_bytes()
    for claim in ids:
        start = data.index(("% BEGIN " + claim + "\n").encode())
        end = data.index(("% END " + claim).encode(), start) + len(("% END " + claim).encode())
        if data[end:end + 1] == b"\n":
            end += 1
        blocks.append({"claim": claim, "path": component + "/main.tex",
            "line_start": data[:start].count(b"\n") + 1,
            "line_end": data[:end].count(b"\n"),
            "block_sha256": hashlib.sha256(data[start:end]).hexdigest(),
            "review_scope": "Focused endpoint/guard/interface reading. BWP1–BWP13 have this reviewer's separate complete mathematical/source review. HUF is authored here and independently reviewed by root; full WRS/UCE proof reviews are separately bound."})

source_specs = [
    ("src/Formalism/SharpRestriction/GlobalTheoremInputs.lean", 122, 141, "All five original LinkG_at fields, delta chosen before later indices, same actual Gx/GK and lattice data."),
    ("src/Development/AbelianVarietyTheory/Proofs/GlobalInterpolation/LinkG.lean", 14, 27, "Universal arbitrary-class installer at the literal TSel/Duty premises."),
    ("src/Development/AbelianVarietyTheory/Definitions/GlobalTwisting/ValidForConstructedPointClassesEventuallyWorking.lean", 67, 109, "Actual BPt, given layout identity, final point and original object at x,hx,i."),
    ("src/Development/AbelianVarietyTheory/Definitions/GlobalTwisting/ValidForConstructedPointClassesEventuallyWorking.lean", 222, 286, "Original unchanged cls/QOf/Built membership and its joint dependent (D,O,b) equality; no added compatibility predicate."),
    ("src/Development/AbelianVarietyTheory/Definitions/GlobalTwisting/FamilyClassSevenDutiesAndStableLattices.lean", 51, 67, "Actual object-property extraction from cls7 at every original x,hx,i."),
    ("src/Formalism/LocalToGlobal/GroupLattices/StdSubAtOfRing.lean", 36, 89, "Five original GroupCompatibilityAll fields and exact given-Extra family condition."),
    ("src/Formalism/SharpRestriction/ParamsHeightRankConstant.lean", 157, 181, "Closed chooses epsilon cutoff and coefficient bound before the family and CH."),
    ("src/Formalism/SharpRestriction/ParamsHeightRankConstant.lean", 187, 190, "DesignExists remains an existential common-family contract; universal local gain does not construct it."),
    ("src/Formalism/LocalToGlobal/ThresholdSelection.lean", 9, 16, "Full original TSelF/TSel remains stronger than selected compatibility."),
    ("src/Formalism/LocalToGlobal/ClassRec.lean", 21, 31, "Additional row pin, joints, host and Weil fields of RecT are not inferred from GroupCompatibilityAll."),
    ("src/Development/AutomorphicArithmetic/AutomorphicVarieties/AutomorphicCases/AutomorphyUnramifiedCoefficients.lean", 12, 27, "FinA, AutB and every-extension LemW supplied together by one marked g1, fixed iota, eO=1 final target."),
    ("src/Development/AutomorphicArithmetic/AutomorphicVarieties/CurveDVRSpecialization/RatTorsionFree.lean", 21, 68, "Exact OrdPt, FinEnd, AutEnd3/AutEnd2 and common GdEnd quantifiers."),
    ("src/Development/AutomorphicArithmetic/AutomorphicVarieties/CurveDVRSpecialization/GdMain.lean", 93, 129, "Literal GdEnd-to-unramified-automorphy endpoint and both torus-conjugacy returns."),
    ("src/Development/AutomorphicArithmetic/AutomorphicVarieties/HeightAndVanishing/Counts.lean", 9, 22, "All original GD guards, especially ell-1 not dividing 2e; no new prime restriction, no full-Dat ell=3 claim."),
    ("src/ReciprocityTheory/ReductiveGroups/ArithmeticGeometry/BirationalGeometry/ToroidalCompactification/IsHolPeriods.lean", 37, 116, "All five IsThetaFrame clauses, all FamilyUnif fields and complete original N1c with supplied Moduli and fixed ordered type."),
    ("src/Development/AbelianVarietyTheory/Proofs/ModuliProofs/ExistsThetaFrameFamily.lean", 19, 28, "Full generic theta-family conclusion at arbitrary given pointwise and holomorphic y/e, without a new InGenus assumption."),
    ("src/Development/AbelianVarietyTheory/Proofs/UnitaryExistence/CongrOfDvdModulus.lean", 36, 57, "Remaining original principal-chart endpoint and its adjoining FramesOK, IsUnf and FromTest producers; HUF supplies N1c only among these inputs."),
    ("src/Formalism/LocalToGlobal/SiegelLatticeTheory/HaarTransversals/UnitaryHaarProducts/SettingBlocks.lean", 323, 334, "Whole CoefWeightedLoc at the original numerical hypotheses, all supplied representations and exact exponent."),
    ("src/Formalism/LocalToGlobal/SiegelLatticeTheory/HaarTransversals/UnitaryHaarProducts/SettingBlocks.lean", 389, 452, "HCReprodDS, BesselNVGap and full seven-clause WlocExists; original nonvanishing premise retained."),
]
source_bindings = []
for path, first, last, meaning in source_specs:
    data = (SOURCE / path).read_bytes()
    pinned = subprocess.check_output(["git", "-C", str(SOURCE), "show", PIN + ":" + path])
    assert data == pinned
    lines = data.splitlines(keepends=True)
    assert 1 <= first <= last <= len(lines)
    source_bindings.append({"path": path, "line_start": first, "line_end": last,
        "file_sha256": hashlib.sha256(data).hexdigest(),
        "range_sha256": hashlib.sha256(b"".join(lines[first-1:last])).hexdigest(),
        "source_commit": PIN, "verified_equal_to_pinned_git_blob": True,
        "semantic_contract_checked": meaning})

report = {
    "schema": "rh-independent-semantic-scope-review/1",
    "artifact_version": "0.49", "date": "2026-11-23",
    "reviewer": "ordinary_structure", "reviewer_agent": "/root/ordinary_structure",
    "status": "PASS", "result": "PASS", "source_commit": PIN,
    "review_scope": "Independent semantic review of the assembled current-v0.49 release: exact original contract closure, conditional-versus-producer boundaries, choice order, small-prime and coefficient scope, named foundations, remaining graph, current metadata and final readers/reports. It does not reread all preserved historical proofs or replace component mathematical reviews or the independent integration audit.",
    "reviewed_files": reviewed, "generated_outputs_reviewed": generated,
    "focused_proof_blocks_reviewed": blocks, "original_source_contracts_checked": source_bindings,
    "inventory_checked": stats,
    "whole_selected_closure": {
        "id": "GLOBAL_LOCAL_GAIN", "proof_claims": ["WRS9", "WRS10"],
        "baseline_contract_preserved_verbatim": True,
        "baseline_contract_sha256": hashlib.sha256(old_nodes["GLOBAL_LOCAL_GAIN"]["contract"].encode()).hexdigest(),
        "all_five_original_LinkG_at_fields": True,
        "delta_before_varying_indices": True,
        "unchanged_selected_built_class_and_given_Extra": True,
        "selected_TSel_or_WPt_premise_added": False,
        "common_design_nonemptiness_inferred": False,
        "stronger_RecT_or_TSel_produced": False,
        "independent_whole_contract_review": cfg["closure_reviews"]["GLOBAL_LOCAL_GAIN"],
    },
    "findings": [
        "The only changed selected status is GLOBAL_LOCAL_GAIN, C to B/proved_in_stated_scope. The original contract text is preserved verbatim, all 121 nodes and 161 requires edges remain, and precisely 24 whole selected obligations remain (17 C and 7 B; 17 shared and 7 additional GRH). Counts are an inventory, never a completion percentage.",
        "WRS extracts the actual joint built witness already in the unchanged Fc.cls/QOf membership. The dependent comparison/kernel tuple and all kernel fields are transported by the original setDiv operation. The resulting compatibility belongs to the given Extra.cmp and Extra.ker, not an independently chosen isomorphic model. WRS7 fixes its threshold before later indices; WRS9 keeps the original Closed order, constants, normalized lengths, all five gain fields and delta(x)=x^(-epsilon/2).",
        "The universal original link_g theorem still has its printed TSel/Duty antecedents. The selected built-class proof supplies LinkG without adding them. This proves the selected estimate while leaving common-family nonemptiness, full RecT/TSel and the denominator, period/height, spectral and other second-layer producers open. The historical stronger route is bypassed for this estimate rather than falsely declared solved.",
        "UCE19 is the complete same-g1 GdEnd consumer. One fixed iota and one marked g1 precede all universal rings, entry maps and actual representations; FinEnd, AutEnd3 and AutEnd2 jointly supply FinA, AutB and every-extension LemW. Arbitrary entry-algebra maps are not assumed continuous, and intermediate finite coefficient DVRs may be ramified. GdEnd itself remains an explicit arithmetic producer, so AUT_UNRAM_COEF is still open. The current continuation explicitly requires the additional local/descent fields in the alternative GdEndAlt route to be matched to the original points; no name-only identification with GdEnd is permitted.",
        "Original small-prime hypotheses remain literal. The abstract local/ConstOfChar arguments retain permitted characteristic-three cases. The final Dat application retains GD.gen (ell-1 does not divide 2e), which excludes ell=3 there by the original condition. No unqualified all-Dat prime-three claim is made by the final prose.",
        "HUF supplies complete N1c and every FamilyUnif field, not only individual complex points: integral projective lattices and all-level comparisons, one-neighborhood prescribed local lifts, arbitrary-choice holomorphy, one finite positive disjoint family before later periods/bases, and global theta normalization on arbitrary open analytic bases. The original Moduli record, fixed embedding/type, both markings and all positive torsion levels remain in scope.",
        "HUF's analytic Hom-line argument checks properness, reduced base, flatness and constant h0=1; rigidification then gives global triviality. Projective GAGA is used on each fiber, without an unjustified algebraization of an arbitrary analytic parameter base. Appell–Humbert, Riemann/GAGA, Grauert with its corrigendum, injective holomorphic maps and semialgebraic finiteness are named foundations, separately recorded rather than counted as newly proved graph nodes.",
        "HUF does not supply the adjoining FramesOK/CoverTri/FibTri/IsUnf/FromTest producers or FrameUnif.exists_unf_hasPrinc. The current continuation points precisely to allTest_of_secBaseChange on all reduced coefficient algebras, using n=1 SecBaseChangeSt and finite-presentation descent, then to simultaneous principal frames. DESIGN_CHOICES_COMMON and BASE_THETA_RATIONAL_TESTS remain open at their original same-object, both-level and all-tuple scope.",
        "BWP supplies whole CoefWeightedLoc and WlocExists at the original numerical and BesselNVGap antecedents, keeping exact weak-Haar promotion, supplied quotient measures, eFun/formal-degree normalization, character factor and all seven local conclusions. Its global tensor vector is chosen before every later measured block. The constructed-vector decay does not assert Bessel uniqueness or decay of every arbitrary IsWu vector.",
        "ConcreteSettingExists retains BesselNVGap and the inherited supplied Forms0 scope. No original Bessel nonvanishing, multiplicity-one, orbital/fiber or Siegel–Weil comparison, full normalized spectral estimate, common row dictionary or count is inferred merely from that conditional analytic setting.",
        "All 74 new claims are class-B human deductions at their stated original-data/foundation scope. Separately hash-bound component reviews cover the actual mathematics; this semantic review does not treat a source theorem hash as a human proof. The cumulative reader preserves the complete historical body and marks its old audit as historical, while current metadata and targets point to v0.49.",
        "Final TeX validation is described accurately as draft syntax/reference/missing-character checking, with no PDF visual review and no Lean/kernel replay. The new reader has no overfull boxes; the cumulative reader retains the 53 inherited overfull diagnostics. The progress report and both README formats preserve the exact conditional and remaining-producer boundaries.",
    ],
    "resolved_editorial_findings": [
        {"topic": "UCE prime-three distinction", "resolution": "The final narrative explicitly retains GD.gen for Dat and distinguishes the abstract characteristic-three lemmas; README.md uses original permitted small-prime guards instead of an unqualified prime3 phrase."},
        {"topic": "Open producer versus named foundations", "resolution": "The progress report calls GdEnd the single open arithmetic producer input to the completed consumer and explicitly retains inherited local/component foundations."},
    ],
    "material_corrections_required": [], "unresolved_findings": [],
    "not_asserted": [
        "A full human-readable proof of RH or unrestricted Dirichlet GRH.",
        "Existence of the common nonempty design, full RecT/TSel, GdEnd, or the original supplied Moduli.",
        "Unconditional principal framed charts, all test-ring producers, higher CoversAt or all-tuple rational theta identities.",
        "Bessel nonvanishing, full spectral/orbital/Siegel–Weil producers or arbitrary-family local gain without its original premises.",
        "A fresh mathematical re-review of all predecessor claims, a formal dependency audit, Lean/kernel replay, or PDF visual certification.",
    ],
}
out = ROOT / "reviews_v0_49/semantic_scope_ordinary_structure.json"
out.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n")
print(json.dumps({"file": str(out.relative_to(ROOT)), "status": report["status"],
    "sha256": digest(out), "reviewed_files": len(reviewed),
    "generated_outputs_reviewed": len(generated), "focused_blocks": len(blocks),
    "source_contract_ranges": len(source_bindings)}, indent=2))
