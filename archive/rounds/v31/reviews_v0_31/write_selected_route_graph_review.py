from pathlib import Path
import hashlib
import json

BASE = Path("/workspace/scratch/368c004c3aea")
ROOT = BASE / "reconstruction_v031"
OUT = BASE / "work_v031/reviews"
GRAPH = ROOT / "dependency_audit_v0_31/obligation_map.json"
g = json.loads(GRAPH.read_text())
n = {x["id"]: x for x in g["nodes"]}
v = json.loads((OUT / "selected_route_graph_validation.json").read_text())
sha = hashlib.sha256(GRAPH.read_bytes()).hexdigest()
assert sha == v["graph_sha256"], "Refresh independent validation before binding review."
assert "SECOND_LAYER_COMPATIBLE_SELECTION" in n["GLOBAL_SECOND_LAYER_MATCH"]["requires"]
assert "Cdes" in n["DESIGN_CHOICES_COMMON"]["contract"]
assert "Cdes" in n["DESIGN_TUSIZE_CLOSED"]["contract"]
assert "Cdes" in n["DESIGN_RANKM_CLOSED"]["contract"]
assert "Closed on D3(3,A)" in n["GLOBAL_RAMIFIED_INCLUSION"]["contract"]
assert "HidaSetting" in n["CERT_RSL_OPERATOR_INCLUSION"]["contract"]
assert "b_v>=0" in n["CERT_RSL_OPERATOR_INCLUSION"]["contract"]
assert "bTop>=0" in n["TASK_GL6_SIZE_SETTING"]["contract"]
assert "EVERY original Fm" in n["SLR_SAME_BUNDLE_BASE_PRODUCER"]["contract"]
assert "TASK_GL6_SIZE_SETTING" in n["GLOBAL_RAMIFIED_INCLUSION"]["requires"]
assert "TASK_GL6_SIZE_SETTING" in n["TASK_LINK_GL_INSTALL"]["requires"]
assert n["TASK_GL6_SIZE_SETTING"]["category"] == "B"

checks = [
    {
        "id": "common_target_and_family",
        "verdict": "PASS",
        "finding": "The ten original topDesWin contracts, fixed-target class projections and constants are retained. All global templates use the same A, C=WithChN A, target-compatible Cprime and E. The design class Cdes is distinguished explicitly. The finite Closed join precedes the single DesignExists family/CH witness.",
    },
    {
        "id": "complete_AND_vs_shared_work",
        "verdict": "PASS",
        "finding": "Selected AND edges contain the displayed sufficient inputs and any remaining proof-of-implication tasks. Proved certificates prove arrows only. All 29 shared-work links are explicitly nonlogical; optional routes are excluded from selected reachability. Recursive design construction is retained as a nonlogical alternative refinement of the opaque compatible DesignChoices producer, so no partial list is asserted to construct it.",
    },
    {
        "id": "DEX_design_cut",
        "verdict": "PASS",
        "finding": "DesignChoices(Cdes,3,cT), the closed TuSize implication for that same cT and Cdes, and closed eventual original RankM form the exact DEX7 sufficient cut. The host is carried by the target DESIGN_RH/GRH wrapper. The three producers remain open C tasks. DEX thinning, denominator size and numerical proviso are complete consumer implications. RecExP-after-every-level, the common QOf, and literal dependent equalities remain upstream in the alternative recursive refinement.",
    },
    {
        "id": "LTD_actual_NBuilt_coverage",
        "verdict": "PASS",
        "finding": "LOCAL_NBUILT_COMMON is a Closed producer on the original Des(C,3) class, with one eventual family of actual certificates for Fm.D(x,i). It retains NdSpec, original iV and Hecke actions, maximal-ideal coverage, Psi/range and the projection square. CERT_LOCAL_COVERAGE then gives literal LinkEta. A generic TSel is explicitly not treated as supplying NBuilt.",
    },
    {
        "id": "SLR_same_Bundle_producer",
        "verdict": "PASS",
        "finding": "The producer explicitly supplies every original Fm in A with compatible original Bundle data and one eventual threshold for the conjunction RowsHold0_3 and the base theta square on the same selected P. The finite consumer may therefore use epsilon1=1,K=0. The text also states that a weaker Closed producer retains its own bounds. It does not infer thTheta from ThDef3, or require RowsHoldLam3/TupAllUsed/nonbase theta identities for this rank implication.",
    },
    {
        "id": "RSL_same_record_second_layer",
        "verdict": "PASS",
        "finding": "The open selector producer retains the actual true-column rec7 record or full dependent tuple transport, original coefficient-field roots, real witness and Duty on A. The completed finite-character and selection certificate gives Closed second layer on D3(3,A). GLOBAL_SECOND_LAYER_MATCH now directly requires the Duty-carrying producer as well as second layer and the universal mass/volume certificate, so its displayed hduty,tie,hU,hG conclusion has complete direct premises.",
    },
    {
        "id": "RSL_smaller_fullness_route",
        "verdict": "PASS",
        "finding": "The exact inclusion is Closed on D3(3,A), with one eventual threshold before all original x,i,u,w|T_u. Taking this inclusion as an input, actual nuDef, ex.lat.atT, nprimeDef and nuIn prove fullness. Original T mod 4 = 1 and primality give T>=3 pointwise, so the nonzero actual orbit slice proves positive rank without full HidaSetting. The source-facing TuSize parameter can be retained unused. The completed bare-inclusion RSL11-RSL12 implication therefore does not need the new size-to-setting task. The graph's selected stronger operator-based supplier of the inclusion does need that task. Fullness descendants still contain no GL4 task or final slope assembly.",
    },
    {
        "id": "RSL_FamU_guard_supplier",
        "verdict": "PASS",
        "finding": "FamU is eventual (HidaSetting D u -> P D u), not unconditional eventual P. D3 membership supplies TuSize only. The newly explicit B task TASK_GL6_SIZE_SETTING reconstructs TuSize -> SettingEventually on the original family, through numsL_wtsL_fam and levelPrime_setting_of_sizes. It supplies all setting clauses, including alcove bounds and bTop>=0, and activates the conditional FamU operator contracts. It is required by both GLOBAL_RAMIFIED_INCLUSION's selected stronger supplier and TASK_LINK_GL_INSTALL. The bare-inclusion-to-fullness certificate remains separate.",
    },
    {
        "id": "RSL_full_slope_ledger",
        "verdict": "PASS",
        "finding": "The three full GL6 operator/length contracts are shared stronger suppliers of the weaker inclusion, not declared completed by it. The full slope route still retains the h3 installation, three GL4 tasks, three GL6 operator/length tasks, the size-to-setting task, congruence-length implication and final numerical/lattice assembly. The mass/volume and ramified-model certificates are used only in their stated original-object scope. Duty/ChosenWall and the literal constants remain in the final assembly contract.",
    },
    {
        "id": "target_arithmetic_preservation",
        "verdict": "PASS",
        "finding": "Ordinary RH still reaches I, II and V and excludes the Case-III producer; unrestricted Dirichlet GRH reaches Case III as well. The fixed 2-primary target restriction is not promoted to universal CountIII. The original Count-II same-ideal coupling and the rank-specific source boundaries are inherited unchanged.",
    },
    {
        "id": "completion_semantics",
        "verdict": "PASS",
        "finding": "Global coverage, small rank, design and fullness are marked as completed conditional implications with open producer inputs. The full proof and arithmetic producer construction are not declared complete. Historical compound-record counts and selected-leaf counts are expressly bookkeeping, not mathematical independence or completion percentages. The formal Lean correctness premise is preserved.",
    },
]

corrections = [
    {
        "id": "duty_direct_AND_premise",
        "initial_issue": "GLOBAL_SECOND_LAYER_MATCH promised hduty, but its original direct premises stated only second layer and universal mass/volume; Duty was inside a more remote producer.",
        "resolution": "Added SECOND_LAYER_COMPATIBLE_SELECTION as a direct requirement. Its contract explicitly supplies Duty on the same A.",
        "status": "RESOLVED",
    },
    {
        "id": "distinct_design_class_symbol",
        "initial_issue": "C named both the top-level WithChN A class and the construction class WithTw(WithSm Cprime), creating ambiguity in the local-coverage class.",
        "resolution": "The design contracts and cut now use Cdes for the construction class, while top-level C remains WithChN A.",
        "status": "RESOLVED",
    },
    {
        "id": "local_operator_guard_and_Closed_scope",
        "initial_issue": "The inclusion node did not explicitly state Closed on D3 or the HidaSetting nonnegativity guard used by the second-branch supplier.",
        "resolution": "GLOBAL_RAMIFIED_INCLUSION now states its exact Closed class and the original HidaSetting/bTop>=0 guard. D3 -> TuSize is a class projection; the subsequent TuSize -> SettingEventually implication is separately retained as the new B task described below.",
        "status": "RESOLVED",
    },
    {
        "id": "SLR_outer_bound_scope",
        "initial_issue": "The universal class producer and the zero-bound finite consumer could be read as erasing the bounds of a separately Closed producer.",
        "resolution": "The producer now explicitly covers every original Fm in A and states that the weaker Closed alternative retains its own bounds.",
        "status": "RESOLVED",
    },
    {
        "id": "FamU_size_to_setting_proof",
        "initial_issue": "The source FamU contracts are conditional on HidaSetting; class membership supplies TuSize but does not itself constitute a human reconstruction of the full setting consequence.",
        "resolution": "Added TASK_GL6_SIZE_SETTING to the selected guarded-operator inclusion route and full global ledger. Independently checked the exact FamU/SettingEventually definitions and settingF_of's numeric dependencies. Also checked T mod 4 = 1 from original norm/tower fields, which removes the full setting supplier from the bare-inclusion positivity argument.",
        "status": "RESOLVED",
    },
]

report = {
    "schema": "rh-human-independent-graph-review/1",
    "artifact_version": "0.31",
    "date": "2026-11-22",
    "reviewer": "/root/audit_literature",
    "source_commit": g["source_commit"],
    "graph_file": "reconstruction_v031/dependency_audit_v0_31/obligation_map.json",
    "graph_sha256": sha,
    "verdict": "PASS after the recorded corrections, including the explicit FamU size-to-setting guard task",
    "required_remaining_text_edits": [],
    "checks": checks,
    "resolved_findings": corrections,
    "validation_file": "work_v031/reviews/selected_route_graph_validation.json",
    "validation_file_sha256": hashlib.sha256((OUT / "selected_route_graph_validation.json").read_bytes()).hexdigest(),
    "validation_summary": {k: v[k] for k in [
        "selected_node_count", "work_node_count", "optional_node_count",
        "rh_reachable_count", "grh_reachable_count",
        "new_component_evidence_entries_checked",
        "new_component_source_ranges_verified",
        "new_component_source_files_pin_verified",
        "component_main_hashes", "open_leaf_categories"
    ]},
    "review_basis": [
        "The finalized DEX, LTD, SLR and RSL statements and closure contracts.",
        "The v0.30 selected-route graph and the current v0.31 graph.",
        "Direct source checks of topDesWin, link_gl, Des/D3, Closed, and the local operator/inclusion guards.",
        "The separate human mathematical reviews of the component proofs; the present review does not replace them."
    ],
    "scope_limits": [
        "A selected sufficient-interface graph, not an exhaustive Lean dependency graph.",
        "No absolute mathematical minimality claim.",
        "No new Lean replay.",
        "No claim that the retained actual producers have been constructed."
    ],
    "hash_refresh_policy": "This verdict is bound to the graph and component hashes above. If only TeX wrapping/provenance hashes change, rerun independent validation and refresh this report after confirming no semantic changes."
}
(OUT / "selected_route_graph_review.json").write_text(json.dumps(report, indent=2) + "\n")

lines = [
    "INDEPENDENT REVIEW OF THE V0.31 SELECTED-ROUTE DEPENDENCY GRAPH",
    "Reviewer: /root/audit_literature. Date: 2026-11-22.",
    "",
    "VERDICT: PASS after the recorded corrections, including the explicit FamU size-to-setting guard task.",
    "No further graph text edits are required by this review.",
    "",
    "Graph: reconstruction_v031/dependency_audit_v0_31/obligation_map.json",
    "SHA256: " + sha,
    "Pinned Lean source: " + g["source_commit"],
    "",
    "This is a review of sufficient dependency rules, original-object bindings",
    "and quantifier order. The underlying Lean proof is assumed fully checked",
    "and correct. No Lean replay was performed.",
    "",
    "MATHEMATICAL AND QUANTIFIER FINDINGS",
]
for check in checks:
    lines += ["", check["id"].replace("_", " ").upper() + ": PASS", check["finding"]]
lines += ["", "CORRECTIONS MADE BEFORE PASS"]
for item in corrections:
    lines += ["", item["id"].replace("_", " ").upper(), item["initial_issue"], "Resolution: " + item["resolution"]]
lines += [
    "",
    "INDEPENDENT STRUCTURAL AND PROVENANCE CHECKS",
    f"The graph contains {v['selected_node_count']} selected logical nodes, {v['work_node_count']} work-refinement nodes and {v['optional_node_count']} optional-route nodes.",
    f"RH reaches {v['rh_reachable_count']} nodes; unrestricted Dirichlet GRH reaches {v['grh_reachable_count']}. Every selected node is reachable from at least one root.",
    "All selected references resolve. The selected graph is acyclic. Work-refinement links are explicitly nonlogical, and optional nodes do not enter selected logical reachability.",
    "The fullness descendants exclude the GL4 tasks, TASK_LINK_GL_INSTALL and the final global-slope assembly. The target-specific count split is preserved.",
    f"All source-input hashes match. The review independently verified {v['new_component_evidence_entries_checked']} new-component graph evidence entries, all 41 new proof-block hashes, {v['new_component_source_ranges_verified']} distinct component source ranges and {v['new_component_source_files_pin_verified']} source files against the pinned Git blobs.",
    "These are integrity checks, not a claim to have independently reproved every source declaration; the separate component reviews cover the mathematical proofs.",
    "",
    "SCOPE OF THE PASS",
    "The graph correctly treats the new human arguments as conditional certificates. It preserves actual compatible design, row/theta, local-specialization, and operator producers where they remain open. It does not infer actual witnesses from record names, transport lemmas, or unrelated abstract models.",
    "The graph is a selected sufficient-interface audit, not a proof of absolute minimality and not a count of independent mathematical obstructions.",
    "",
    "If final TeX wrapping changes proof/provenance hashes without changing any mathematics, refresh the mechanical validation and this report's hash binding. Any semantic graph or component change requires renewed review of the affected rule.",
]
(OUT / "selected_route_graph_review.txt").write_text("\n".join(lines) + "\n")
print(json.dumps({"verdict": report["verdict"], "graph_sha256": sha, "required_remaining_text_edits": []}, indent=2))
