#!/usr/bin/env python3
"""Bind the independently authored v0.46 semantic review to final bytes.

The prose findings are the reviewer's judgments, not generated theorem checks.
The assertions below guard the exact final inventory, closure and file bindings.
This script changes only this reviewer's JSON report.
"""
import collections
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SOURCE = ROOT.parent / "formal_source"
PIN = "7cbf7a0c32fca1badf05931879a37c3f8a2b03b4"


def read(path):
    return json.loads((ROOT / path).read_text())


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def binding(path, scope):
    return {"path": path, "sha256": digest(ROOT / path), "review_scope": scope}


cfg = read("increment_v0_46.json")
stats = read("integration_stats_v0_46.json")
prior_map = read("dependency_audit_v0_45/obligation_map.json")
now_map = read("dependency_audit_v0_46/obligation_map.json")
prior_nodes = {n["id"]: n for n in prior_map["nodes"]}
now_nodes = {n["id"]: n for n in now_map["nodes"]}
prior_register = read("dependency_audit_v0_45/remaining_leaf_register.json")
now_register = read("dependency_audit_v0_46/remaining_leaf_register.json")
prior_open = {n["id"]: n for n in prior_register["records"]}
now_open = {n["id"]: n for n in now_register["records"]}
closed = {"CNR3", "TASK_PROP_GK_INSTALL"}
assert prior_nodes.keys() == now_nodes.keys()
assert set(prior_open) - set(now_open) == closed
assert not (set(now_open) - set(prior_open))
assert len(now_nodes) == 121
assert sum(len(n["requires"]) for n in now_nodes.values()) == 161
assert all(prior_nodes[k]["requires"] == now_nodes[k]["requires"] for k in now_nodes)
for key in now_nodes:
    for field in ["category", "kind", "status", "gate"]:
        if key not in closed:
            assert prior_nodes[key].get(field) == now_nodes[key].get(field), (key, field)
    if key in {"DESIGN_CHOICES_COMMON", "BASE_THETA_RATIONAL_TESTS"}:
        assert now_nodes[key]["contract"].startswith(prior_nodes[key]["contract"])
    else:
        assert now_nodes[key].get("contract") == prior_nodes[key].get("contract")
assert collections.Counter(n["category"] for n in now_open.values()) == {"C": 20, "B": 8}
assert stats == {
    "new_claims": 91, "cumulative_claims": 2768,
    "selected_nodes": 121, "selected_edges": 161,
    "open_count": 28, "open_categories": {"C": 20, "B": 8},
    "shared_open": 21, "extra_grh_open": 7,
    "new_source_files_checked": 172, "new_unique_source_ranges_checked": 233,
}
audit_text = (ROOT / "RH_dependency_audit_v0_46.txt").read_text()
assert all(n["contract"] in audit_text for n in now_open.values())

provenance = read("provenance.json")
checkpoint = read("continuation_checkpoint.json")
targets = read("next_source_targets.json")
assert provenance["scope"] == checkpoint["status"] == targets["current_status_v0_46"] == cfg["status"]
assert provenance["version_0_46_local_conclusions"] == checkpoint["new_in_this_version"] == cfg["local_conclusions"]
assert provenance["component_input_boundaries_v0_46"] == checkpoint["remaining_major_inputs"] == cfg["remaining_major_inputs"]
assert checkpoint["next_targets"] == targets["next_local_priority"] == cfg["next_targets"]
for key, value in checkpoint["current_dependency_audit"].items():
    if key not in {"artifact_version", "scope"}:
        assert value.startswith("dependency_audit_v0_46/") and (ROOT / value).exists()

expected_outputs = {
    "RH_new_proofs_v0_46.tex": "f292531f05355c031d9fd2ab90c562c4e67fca145a4d937a4217355c7f418420",
    "RH_readable_reconstruction_v0_46.tex": "da268e8ad5fc009e8cdebe40901401fa1759ba1da99f290b8a0eb32e26c2c24a",
    "RH_reconstruction_progress_v0_46.txt": "aab2550bd462ec774dfd7c6b4bf7e952585d6881b99a34e6d807a233890e40f7",
}
assert all(digest(ROOT / p) == h for p, h in expected_outputs.items())
tex = read("tex_validation.json")
assert tex["artifact_version"] == "0.46"
for item in tex["documents"]:
    assert digest(ROOT / item["tex_filename"]) == item["tex_sha256"]
    assert item["syntax_compile_succeeded"]
    assert not item["undefined_references_or_citations"]
    assert item["missing_character_warnings"] == 0
    assert not item["pdf_generated"] and not item["pdf_visual_review_performed"]
assert [x["passes"] for x in tex["documents"]] == [2, 3]
assert [x["overfull_box_warnings"] for x in tex["documents"]] == [0, 53]

reviewed = []
scope_scripts = "Current semantic scope, choice order, retained antecedents, selected closure and generated-output narrative; exhaustive preservation mechanics belong to the separate integration audit."
for path in ["increment_v0_46.json", "configure_v0_46.py", "assemble_v0_46.py", "integrate_v0_46.py", "write_progress_v0_46.py", "v0_46_frontmatter.tex", "v0_46_audit_intro.tex"]:
    reviewed.append(binding(path, scope_scripts))
for path, scope in [
    ("provenance.json", "Current scope, current_boundary_authority, version_0_46_local_conclusions, component_input_boundaries_v0_46 and inventory; not a rereading of every historical nested record."),
    ("continuation_checkpoint.json", "Current status, new_in_this_version, remaining_major_inputs, next_targets, current_dependency_audit, current_deliverable and version_0_46_update."),
    ("next_source_targets.json", "Current v0.46 status, precision notes, selected-frontier files and next_local_priority; historical compound records retain their prior meaning."),
]:
    reviewed.append(binding(path, scope))
for version, names in [
    ("0_45", ["obligation_map.json", "remaining_leaf_register.json"]),
    ("0_46", ["obligation_map.json", "remaining_leaf_register.json", "route_coverage.json", "closure_delta.json", "target_disposition.json", "published_applications.json"]),
]:
    for name in names:
        reviewed.append(binding("dependency_audit_v" + version + "/" + name,
            "Original selected whole-contract scopes, the two exact closures, preserved dependency edges and remaining categories; current additive progress is distinguished from historical evidence. The 245 historical target records are not freshly reread in full."))

for component in cfg["components"]:
    reviewed.append(binding(component + "/main.tex",
        "Stated endpoint, quantifier, normalization, guard and consumer scope. This report is not a fresh full independent mathematical review of every block; separate component reviews supply that coverage."))
    for name in ["contracts.json", "closure.json", "retained_foundations.json"]:
        if (ROOT / component / name).exists():
            reviewed.append(binding(component + "/" + name,
                "Exact original endpoint and retained-input boundaries, distinguishing actual producers from conditional installers and named classical foundations."))
    if component == "arithmetic_rows_v46":
        reviewed.append(binding(component + "/provenance.json",
            "Retained original SG.HidaSetting, RowsFinDim, same-object ties and exact CountIdempotentsClass antecedent, plus independent review coverage."))

for path in [
    "arithmetic_rows_v46/review_ARO1_ARO15_ordinary_structure.json",
    "integral_cusp_lattices_v46/review_ICL1_ICL9_main_proof_rigidity.json",
    "integral_cusp_lattices_v46/review_ICL10_ICL21_root.json",
]:
    reviewed.append(binding(path, "Separately saved focused mathematical review and its final proof/block bindings; establishes the stated authorship/review separation."))

generated = []
for path in [
    "RH_new_proofs_v0_46.tex", "RH_readable_reconstruction_v0_46.tex",
    "dependency_audit_v0_46/main.tex", "RH_dependency_audit_v0_46.txt",
    "README.md", "RH_reconstruction_progress_v0_46.txt", "README.txt",
    "integration_stats_v0_46.json", "tex_validation.json",
]:
    generated.append(binding(path,
        "Current front matter, audit, endpoint summaries, inventory, retained-input and continuation prose, and reported validation scope. For the cumulative reader this does not assert a fresh reading of every preserved historical chapter."))

selected = {
    "rank_three_congruence_v46": ["RNC1", "RNC5", "RNC8", "RNC16"],
    "prop_gk_installation_v46": ["PGK1", "PGK2", "PGK3", "PGK4", "PGK5", "PGK6"],
    "arithmetic_rows_v46": ["ARO18", "ARO24", "ARO28", "ARO29", "ARO30"],
    "integral_cusp_lattices_v46": ["ICL8", "ICL11", "ICL19", "ICL20", "ICL21"],
    "global_local_gain_v46": ["GLG7", "GLG8", "GLG9", "GLG13", "GLG14", "GLG15", "GLG17", "GLG18"],
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
            "review_scope": "Focused endpoint/guard/interface reading; full mathematical review coverage is separately recorded."})

source_checks = []
source_specs = [
    ("src/Development/AutomorphicArithmetic/AutomorphicVarieties/AutomorphicForms/CongruenceNumberRankThree.lean", 107, 140, "Literal Adm3/Adm2 disjunction, indexed orbit, original fixed-K constants and integer-before-all-later-coefficient quantifiers."),
    ("src/Development/AutomorphicArithmetic/AutomorphicVarieties/UnitaryThreeGroups/KatoUse.lean", 36, 64, "Full PropGK and distinct exact OneChar premise, including original Vlen/Vn and normalized integer valuation."),
    ("src/Development/AutomorphicArithmetic/AutomorphicVarieties/UnitaryThreeGroups/OrbEquiv.lean", 111, 173, "Original CNR3 -> OneChar -> PropGK producer; nonimaginary-quadratic branch and inverse-Frobenius use."),
    ("src/Formalism/SharpRestriction/GrowthBounds/LogarithmicSums.lean", 18, 22, "Literal RestStar constant-before-C-before-instance-families order and original error term."),
    ("src/Formalism/SharpRestriction/GrowthBounds/LogarithmicSums/RemainingCountingStatement.lean", 10, 20, "Literal FamilyAskBounds and RemainingCountingStatement under the original AdmFam antecedent."),
    ("src/Formalism/SharpRestriction/GlobalTheoremInputs.lean", 97, 140, "All five original LinkG_at conjuncts, exact loG/flG normalizations and full eventual LinkG."),
    ("src/Formalism/SharpRestriction/GrowthBounds/SmallOrderPrimes.lean", 220, 247, "Entire admG1 including the additional depth and valuation clauses; full admitted record is retained."),
]
for path, first, last, scope in source_specs:
    data = (SOURCE / path).read_bytes()
    excerpt = b"".join(data.splitlines(keepends=True)[first - 1:last])
    source_checks.append({"path": path, "sha256": hashlib.sha256(data).hexdigest(),
        "line_start": first, "line_end": last,
        "range_sha256": hashlib.sha256(excerpt).hexdigest(), "scope": scope})

findings = [
    ("EXACT_CNR3_QUANTIFIERS", "RNC16 matches the whole literal original CNR3: fixed imaginary quadratic K, then c,A, then e,N,p,w and the finite indexed root-of-unity orbit, then NN, then every odd coefficient prime including 3, closure, scalar tower, fixed iota, prolongation, arithmetic Frobenius and pairwise-nonisomorphic collection. Both original Adm3 and Adm2 alternatives remain. Repeated orbit values retain their indices; empty families are included."),
    ("BOUNDED_PUBLISHED_APPLICATION", "RNC1 is the single new class-A checked application. General regular-algebraic polarized Galois existence precedes weight identification; full coefficient-prime compatibility is used only at the checked Shin-regular weights. The classical-input registry keeps CM versus totally real, geometric-Frobenius, Hodge-sign and all-prime scopes explicit. No stronger all-rank CountK/CountQ, all-prime irreducibility or unrelated local correspondence theorem is inferred."),
    ("ORIGINAL_LEVELS_AND_CATALOGUES", "The auxiliary levels N^5 and (N|disc K|)^3 bound full automorphic labels without replacing the original Galois levels. The local LevelAt disjunction controls monodromy rather than inserting a new coefficient-prime factor. Full cusp labels and all-Aut(C) conjugation precede the later coefficient datum. The integer-power Satake formula removes any need for complex automorphisms to fix a chosen square root."),
    ("FINITE_PROP_GK_TASK_ONLY", "PGK1–6 prove the entire finite implication CNR3 and OneChar imply PropGK. The separate original OneChar is explicitly supplied, including finite original Selmer length and its finite trace/valuation sum. PGK6 handles all number fields, with an impossible-GD branch outside the imaginary quadratic case. The integer precedes every later coefficient ring; prime 3 is retained with the original GD guard, and no new coefficient extension or cross-character nonisomorphism assumption is introduced."),
    ("TWO_LITERAL_WHOLE_CLOSURES", "The original CNR3 producer and TASK_PROP_GK_INSTALL implication task are the only selected whole obligations closed. The latter was already classified as an implication-reconstruction task in v0.45; completing it does not supply OneChar, RIG_II, unconditional PropGK or Case I. The final audit and continuation state this distinction consistently."),
    ("ARITHMETIC_ROW_SETTING", "ARO uses the original adelic SG.HidaSetting, not the previously completed ordinary-Hecke setting. Actual reduction, both conjugate orientations, exact kernel and surjectivity, Haar-fiber volume V, the original additive character and full event algebra are proved on supplied original data. The chosen good rows, repeated labels, formal degrees and quotient measure are preserved in one AllRows/AllJoinA/PCountTie object before events vary."),
    ("COUNT_AND_WEIGHT_GUARDS", "RowsFinDim, GapHyp and original AutTie/RowDictTie/LabTie remain explicit. ARO28 retains exact CountIdempotentsClass; ARO29 retains normalized-type compatibility, TieAdmG, RangeW and FLC19's actual-rank/eventual guard. ARO30 requires one common family and simultaneous threshold before all varying members. Neither the common setting nor the arithmetic cylinder counts are inferred from the finite row construction; GLOBAL_RETAINED_DEFECT remains open."),
    ("WHOLE_INTEGRAL_LATTICE_FINITE_GENERATION", "ICL8 concerns the whole original valuation-nonnegative cusp lattice at every original weight. Its finite separating evaluations are integral at every finite prime of a single good model; ramified Lie eigenmodules are full saturated kernels, with no integral direct-sum claim. Scalar-extension injectivity uses the original reduced test algebras. No spanning, a priori saturation of the cusp lattice or merely bounded-denominator substitute is assumed."),
    ("ICL_CONNECTION_AND_FIVE_INPUT_GROUPS", "The identity cover is exact only given the original IsNab connection. Full spanning additionally retains the actual principal-chart, level-system, raw Gaussian/reproduction, short-rule/gluing/dictionary and ramified-jet groups, uniformly at every original row and required weight. These original unreconstructed producers are not reclassified as published foundations. The supplied CM/abelian-scheme/fixed-type finite-dimensionality foundations are separately named."),
    ("SAME_GEOMETRY_AND_BOTH_LEVELS", "The conditional Neumann/unfolding, finite harmonic span, original-field descent and one-scalar all-place denominator arguments retain the actual free lattice/frame action, original metric, measure and phases. ICL19–21 give exact conditional FullAt/LatFull and FWTie transport to both original Boolean MLat levels. Higher CoversAt, all-tuple class sums/uniqueness with phase rescalings, one PointIdentCore before all tuples, base ClassSumsSpan, common family existence, Fits and eta agreement remain open."),
    ("FULL_LOGARITHMIC_COUNTING_ENDPOINT", "GLG7 and GLG9 match the complete original RestStar and RemainingCountingStatement, including the constant chosen before the instance families, both candidate-prime ranges, all later members and lifts, arbitrary original top weights without an upper bound, and the exact error b_o=b^(x^(-epsilon/2)) with coefficient one. The original AdmFam antecedent is retained; its existence is not a consequence of the counting theorem."),
    ("LOCAL_DESCENT_AND_LENGTH_NORMALIZATION", "GLG13–15 retain both original integral representation models, actual coefficient-rational evaluations, the original comparison extension and exact finite-intersection descent. The normalized local length divides by v_O(p)=a_w e_w, matching the original A-length divided by e_w. No Galois-extension or unrecorded flatness assumption is introduced into the comparison consumer."),
    ("FIVE_FIELD_LINK_G_BOUNDARY", "GLG17 supplies all five literal LinkG_at fields with the same objects and constant 4|C|+1. GLG18 retains actual GroupCompatibilityFamily or its precise NPDescF consequence, full AdmFam including every admG1 clause and original first growth, and eventual MeanKappaBound. GW2 is available only with its actual guards; mere nonnegativity is not asserted to supply mean deficit. GLOBAL_LOCAL_GAIN and the other quantitative whole obligations remain open."),
    ("UNCHANGED_SELECTED_GRAPH_AND_OPEN_SCOPES", "Direct comparison preserves all 121 selected nodes and all 161 requires edges. Exactly CNR3 and TASK_PROP_GK_INSTALL leave the register. All 28 remaining category/kind/status fields are unchanged. DESIGN_CHOICES_COMMON and BASE_THETA_RATIONAL_TESTS retain their entire previous contract verbatim and append only the explicit ICL progress/boundary; every other selected contract is unchanged. The remaining inventory is 20 C plus 8 B, with 21 shared RH/GRH, 7 additional Dirichlet-GRH and no RH-only entry."),
    ("PREVIOUS_HIDA_AND_OTHER_COMPLETED_WORK", "The six-field same-J Hida result, actual LevelAlt/HasAut, both selected rank-four support Links, finite local weights, host rigidity and adjoint leaves remain completed at their existing scopes. The current roadmap does not reopen them or restore Case II. RH retains Cases I/V and OneChar/RIG_II; unrestricted Dirichlet GRH retains its separate Case III, Seed IV and rank-four chain branch."),
    ("CURRENT_METADATA_AND_READERS", "Current provenance.scope, checkpoint.status and next_source_targets.current_status_v0_46 equal the final increment status. Current conclusions, remaining inputs and next priorities agree. Active audit pointers name existing v0.46 files. Both readers, final progress, README files and audit agree on 91 new/2768 cumulative claims, two exact closures and 28 remaining obligations; the TXT audit contains every full current contract."),
    ("PRESERVATION_AND_VALIDATION_SCOPE", "The narrative correctly promises the complete historical proof body and predecessor claim records, with mutable v0.45 metadata retained in history; it does not promise an unchanged active tail/front matter. The independent integration audit separately records 7053 passed checks. Final draft TeX reports 2 new-reader passes and 3 cumulative passes, zero missing characters/undefined references, 0 new-reader and 53 inherited cumulative overfull boxes. No PDF visual certification, Lean/kernel replay, mechanically extracted Lean dependency graph, completion percentage or completed human RH/GRH proof is asserted."),
]

report = {
    "schema": "rh-semantic-scope-review/1", "artifact_version": "0.46",
    "reviewer": "ordinary_structure", "date": "2026-11-23", "status": "PASS",
    "source_commit": PIN,
    "scope": "Final independent semantic review of v0.46 configuration, integration/assembly narrative, current continuation metadata, five completed endpoint packets and generated readers/audit/progress/README. Direct comparison with the v0.45 selected whole-contract register. Separate from the exhaustive preservation/source/dependency audit.",
    "independence": "The reviewer independently reviews root-authored release scope and authored the separate ARO1–15 mathematical/source review. The reviewer authored ICL; its independent mathematical coverage is supplied by main (ICL1–9) and root (ICL10–21). RNC, PGK, ARO16–30 and GLG are checked here for exact endpoints, quantifiers, guards, retained foundations and consumer scope, not claimed as a fresh full mathematical re-review of every proof block.",
    "reviewed_files": reviewed,
    "focused_claim_blocks": blocks,
    "generated_outputs_reviewed": generated,
    "literal_source_boundary_checks": source_checks,
    "checks": [{"id": key, "result": "PASS", "finding": text} for key, text in findings],
    "inventory_checked": {
        "new_claim_blocks": 91, "new_claim_classifications": {"A": 1, "B": 90},
        "cumulative_claims": 2768, "predecessor_claims": 2677,
        "selected_nodes": 121, "selected_edges": 161,
        "prior_whole_obligations": 30, "whole_obligations": 28,
        "categories": {"C": 20, "B": 8},
        "root_scope_counts": {"shared_RH_GRH": 21, "GRH_only": 7, "RH_only": 0},
        "new_whole_leaf_closures": 2, "closed_whole_obligation_ids": sorted(closed),
        "whole_obligation_ids": list(now_open),
        "new_pinned_source_files": 172, "new_distinct_source_ranges": 233,
    },
    "corrections_resolved": [
        {"item": "Canonical-connection boundary in the ICL narrative", "resolution": "The final configuration, audit, contracts, continuation and progress explicitly retain the original IsNab connection alongside the five main spanning input groups. The identity cover is not presented as an unconditional connection producer."},
        {"item": "Historical preservation wording", "resolution": "The final audit and progress say complete historical proof body, distinguishing that preserved body from the actively updated front matter, remaining-input section and reading-order prose."},
        {"item": "ARO8 original-domain precision", "resolution": "The separately reviewed final ARO8 explicitly quantifies x in the original stabilizer K, matching the source reduction map and KppShape; its exact-source review remains bound to the frozen proof."},
    ],
    "material_corrections_required": [],
    "not_claimed": [
        "No fresh full independent mathematical review of all 91 new claims or all historical proofs.",
        "No replacement for the separately bound component mathematical reviews or exhaustive integration audit.",
        "No OneChar/RIG_II producer, unconditional PropGK or Case I conclusion from the completed finite implication.",
        "No all-rank CountK/CountQ or extension beyond the explicitly matched published automorphic applications.",
        "No common arithmetic/geometric-family existence, arithmetic cylinder-count theorem, unconditional cusp spanning or full global-gain producer from the conditional installers.",
        "No reconstruction of the retained original connection, five cusp-spanning producers or named classical foundations themselves.",
        "No complete human-readable RH or unrestricted Dirichlet-GRH proof, Lean replay, completion percentage or PDF visual certification.",
    ],
}
out = ROOT / "reviews_v0_46/semantic_scope_ordinary_structure.json"
out.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n")
print(json.dumps({"status": report["status"], "reviewed_files": len(reviewed),
    "generated_outputs": len(generated), "focused_claim_blocks": len(blocks),
    "source_boundary_ranges": len(source_checks), "sha256": digest(out)}, indent=2))
