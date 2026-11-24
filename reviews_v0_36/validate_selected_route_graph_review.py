#!/usr/bin/env python3
"""Independent v0.36 selected-route review checks and frozen-byte report.

This validates the structural and byte claims of a completed mathematical
scope review.  It does not purport to automate that scope review or Lean.
"""
import argparse
import collections
import hashlib
import json
from pathlib import Path
import subprocess

PIN = "7cbf7a0c32fca1badf05931879a37c3f8a2b03b4"
FROZEN = {
    "dependency_audit_v0_36/obligation_map.json": "f32b31eec4273804e3f2e855c4ae3524e7824cd4b1ee73cbf456744220ff41d9",
    "dependency_audit_v0_36/main.tex": "774b659887c61215bd0c7caab2c6ae522adbd8a3fce0ddc86b6a366052ccf67a",
    "RH_dependency_audit_v0_36.txt": "f14973309c883d6159755c029f6c46f317365a18c1c11d878d9d2508c097388c",
}
COMPONENTS = {
    "coefficient_fock_bridge": ("CFB", 13, "coefficient_fock_bridge_review.json"),
    "joint_harmonic_io": ("JIO", 19, "joint_harmonic_io_review.json"),
    "regular_quotient": ("RQC", 22, "regular_quotient_review.json"),
    "count_choice": ("CCH", 17, "count_choice_review.json"),
}


def sha(b):
    return hashlib.sha256(b).hexdigest()


def canonical(v):
    return json.dumps(v, sort_keys=True, ensure_ascii=False, separators=(",", ":")).encode()


def read(p):
    return json.loads(p.read_text())


def walk(v, omit_history=True):
    if isinstance(v, dict):
        yield v
        for k, x in v.items():
            if omit_history and k in {"previous_interface", "previous_contract", "previous_node"}:
                continue
            yield from walk(x, omit_history)
    elif isinstance(v, list):
        for x in v:
            yield from walk(x, omit_history)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--release", required=True, type=Path)
    ap.add_argument("--baseline", required=True, type=Path)
    ap.add_argument("--original", required=True, type=Path,
                    help="Unchanged v0.29 next_source_targets.json")
    ap.add_argument("--source", required=True, type=Path)
    ap.add_argument("--out", required=True, type=Path)
    args = ap.parse_args()
    root, oldroot, repo = args.release.resolve(), args.baseline.resolve(), args.source.resolve()
    args.out.mkdir(parents=True, exist_ok=True)
    audit = root / "dependency_audit_v0_36"
    for f, h in FROZEN.items():
        assert sha((root / f).read_bytes()) == h, ("Reviewed bytes changed", f)
    graph = read(audit / "obligation_map.json")
    old = read(oldroot / "dependency_audit_v0_35/obligation_map.json")
    assert graph["source_commit"] == PIN
    nodes = {n["id"]: n for n in graph["nodes"]}
    oldnodes = {n["id"]: n for n in old["nodes"]}
    assert len(nodes) == len(graph["nodes"]) == 121
    assert nodes.keys() == oldnodes.keys()
    for id, n in nodes.items():
        for k in ("gate", "requires", "category", "status", "kind"):
            assert n.get(k) == oldnodes[id].get(k), ("Logical delta", id, k)
        assert n["gate"] in {"LEAF", "AND"}
        assert all(d in nodes for d in n["requires"])
        assert (n["gate"] == "LEAF") == (not n["requires"])
    grey, black = set(), set()

    def visit(i):
        assert i not in grey, ("Cycle", i)
        if i in black:
            return
        grey.add(i)
        for d in nodes[i]["requires"]:
            visit(d)
        grey.remove(i)
        black.add(i)

    for i in nodes:
        visit(i)

    def reach(i):
        out, pending = set(), [i]
        while pending:
            x = pending.pop()
            if x not in out:
                out.add(x)
                pending.extend(nodes[x]["requires"])
        return out

    rr, rg = reach("ORDINARY_RH"), reach("DIRICHLET_GRH")
    assert (len(rr), len(rg)) == (101, 110)
    assert rr | rg == nodes.keys()
    common_counts = {"COUNT_I_PRODUCER", "COUNT_II_SUPPORT", "COUNT_V_PRODUCER"}
    assert common_counts <= rr and common_counts <= rg
    case3 = {"COUNT_III_PRODUCER", "CASE3_PROMOD", "SEED_IV_ALT",
             "TASK_CASE3_PROMOD_JOIN", "TASK_CASE3_AUT_JOIN", "TENSOR_FACTOR_TOWER",
             "CHAIN_RANK_FOUR", "CHAIN_DESC4", "RANK4_CHAIN_REDUCTION"}
    assert not (case3 & rr) and case3 <= rg
    full = reach("GLOBAL_FULL_RANK")
    assert "GLOBAL_REAL_SECOND_LAYER" in full
    assert not any(x in full for x in ["TASK_GL4_COLUMN_VALUES", "TASK_GL4_SLOPE_LOWER",
                                      "TASK_GL4_SLOPE_MAX", "TASK_GL_FINAL_ASSEMBLY"])
    ten = graph["selected_interface_cuts"]["common_family"]["ten_contracts"]
    assert len(ten) == len(set(ten)) == 10 and ten[0] == "GLOBAL_DESIGN"
    for suffix in ["RH", "GRH"]:
        req = nodes["TOPDESWIN_" + suffix]["requires"]
        assert all(x in req for x in ten[1:]) and "DESIGN_" + suffix in req
        assert "GLOBAL_DESIGN" in reach("DESIGN_" + suffix)
    assert len(graph["work_refinement_nodes"]) == 13
    assert len(graph["optional_routes"]) == 8
    assert not ({n["id"] for n in graph["optional_routes"]} & nodes.keys())
    assert all(x.get("logical") is False for x in graph["work_refinement_links"])
    sufficient = graph["selected_interface_cuts"]["count_ii_v036"]["coupled_rule"]
    assert sufficient == read(audit / "closure_delta.json")["nested_coupled_rule"]
    assert read(audit / "closure_delta.json")["closed_selected_leaves"] == []
    closed_status = {"proved_in_stated_scope", "published_application_checked"}
    leaves = [n for n in graph["nodes"] if n["gate"] == "LEAF" and n["status"] not in closed_status]
    assert len(leaves) == 34
    cats = dict(collections.Counter(n["category"] for n in leaves))
    assert cats == {"C": 23, "B": 9, "D": 2}
    reg = read(audit / "remaining_leaf_register.json")
    assert reg["records"] == leaves
    assert {n["id"] for n in leaves if n["category"] == "D"} == {"AD_VANISH_K_MATCH", "HOST_RIGID_S"}
    standalone = (root / "RH_dependency_audit_v0_36.txt").read_text()
    assert standalone == (audit / "audit.txt").read_text()
    assert all(n["contract"] in standalone for n in leaves)

    # Independent source-input and evidence binding checks.
    for name, inp in graph["source_inputs"].items():
        assert sha((root / inp["file"]).read_bytes()) == inp["sha256"], ("Graph input", name)
    bc = graph["backlog_crosswalk"]
    assert sha((root / bc["file"]).read_bytes()) == bc["sha256"]
    assert bc["records"] == 245 and bc["scope_groups"] == 107
    current = read(root / bc["file"])
    previous = read(oldroot / "dependency_audit_v0_35/target_disposition.json")
    original = read(args.original)["targets"]
    predecessor_targets = read(oldroot / "next_source_targets.json")["targets"]
    assert len(current["records"]) == len(previous["records"]) == len(original) == 245
    assert len(predecessor_targets) == 245
    assert len({t["id"] for t in current["records"]}) == 245
    assert len(current["scope_groups"]) == 107
    for i, (c, p, o) in enumerate(zip(current["records"], previous["records"], original), 1):
        assert c["id"] == p["id"] and c["original_id"] == p["original_id"] == o.get("id")
        assert c["original_index_one_based"] == i
        assert c["original_record_sha256"] == sha(canonical(o))
        assert c["predecessor_record_sha256"] == sha(canonical(predecessor_targets[i-1]))
        for k in ["primary_category", "applicability", "disposition", "inherited_remaining_human_scope",
                  "inherited_scope", "inherited_retained_inputs", "scope_components"]:
            assert c.get(k) == p.get(k), ("Historical scope changed", i, k)
        assert c["primary_category"] in "ABCD"
        assert c["applicability"] in {"RH+GRH", "optional", "closed-in-stated-scope"}
    members = [i for g in current["scope_groups"] for i in g["member_ids"]]
    assert collections.Counter(members) == collections.Counter(c["id"] for c in current["records"])

    source_blobs, source_ranges, source_occurrences = {}, set(), 0
    graph_source_ranges = set()

    def validate_source(s, which):
        nonlocal source_occurrences
        path = s.get("path", "")
        if not path.startswith("src/") or not {"line_start", "line_end", "range_sha256"} <= s.keys():
            return
        if path not in source_blobs:
            blob = (repo / path).read_bytes()
            pinned = subprocess.check_output(["git", "show", PIN + ":" + path], cwd=repo)
            assert blob == pinned, ("Pin mismatch", path)
            source_blobs[path] = blob
        blob = source_blobs[path]
        h = s.get("file_sha256", s.get("full_file_sha256", s.get("sha256")))
        if h:
            assert sha(blob) == h, ("Full source hash", path)
        a, b = s["line_start"], s["line_end"]
        lines = blob.splitlines(keepends=True)
        assert 1 <= a <= b <= len(lines)
        segment = b"".join(lines[a-1:b])
        assert sha(segment) == s["range_sha256"], ("Source range", path, a, b)
        if "range_bytes" in s:
            assert len(segment) == s["range_bytes"]
        source_occurrences += 1
        key = (path, a, b)
        source_ranges.add(key)
        if which == "graph":
            graph_source_ranges.add(key)

    evidence_bindings = set()
    for obj in walk({k: graph[k] for k in ["nodes", "work_refinement_nodes", "optional_routes"]}):
        validate_source(obj, "graph")
        for fk, hk in [("ledger", "ledger_sha256"), ("proof_file", "proof_sha256")]:
            if fk in obj and hk in obj:
                assert sha((root / obj[fk]).read_bytes()) == obj[hk], ("Evidence hash", obj[fk])
                evidence_bindings.add((obj[fk], obj[hk]))
        if "ledger" in obj and "claims" in obj:
            cp = read(root / obj["ledger"])
            ci = {c["id"] for c in cp["claims"]}
            assert set(obj["claims"]) <= ci, ("Evidence claim absent", obj["ledger"])

    allclaims = {c["id"] for c in read(root / "provenance.json")["claims"]}
    assert len(allclaims) == 1770
    baselineclaims = {c["id"] for c in read(oldroot / "provenance.json")["claims"]}
    assert len(baselineclaims) == 1699
    newclaims, component_bindings, proof_hashes = set(), [], []
    new_source_occurrences = 0
    for comp, (prefix, num, review_name) in COMPONENTS.items():
        cp = read(root / comp / "provenance.json")
        closure = read(root / comp / "closure.json")
        reviewed = read(root / "reviews_v0_36" / review_name)
        hashes = {file: sha((root / comp / file).read_bytes()) for file in ["main.tex", "provenance.json", "closure.json"]}
        assert reviewed.get("status", reviewed.get("verdict", "")).startswith("PASS")
        assert reviewed["proof_file_sha256"] == hashes["main.tex"]
        assert reviewed["provenance_file_sha256"] == hashes["provenance.json"]
        assert reviewed["closure_file_sha256"] == hashes["closure.json"]
        assert not reviewed.get("required_corrections", [])
        assert not reviewed.get("unresolved_review_issues", [])
        assert not reviewed.get("open_findings", [])
        ids = {prefix + str(k) for k in range(1, num+1)}
        assert {c["id"] for c in cp["claims"]} == ids
        assert set(reviewed["claims_reviewed"]) == ids
        newclaims.update(ids)
        for c in cp["claims"]:
            assert set(c.get("depends_on", [])) <= allclaims
            pr = c["proof_location"]
            f = root / pr["file"]
            data = f.read_bytes()
            lines = data.splitlines(keepends=True)
            block = b"".join(lines[pr["line_start"]-1:pr["line_end"]])
            assert sha(block) == pr["sha256"], ("Proof block", c["id"])
            if "bytes" in pr:
                assert len(block) == pr["bytes"]
            proof_hashes.append({"id": c["id"], "file": pr["file"], "sha256": pr["sha256"]})
            for s in c["sources"]:
                validate_source(s, "component")
                new_source_occurrences += 1
        component_bindings.append({"component": comp, "claim_count": num,
                                   "main_tex_sha256": hashes["main.tex"],
                                   "provenance_sha256": hashes["provenance.json"],
                                   "closure_sha256": hashes["closure.json"],
                                   "peer_review_file": "reviews_v0_36/" + review_name,
                                   "peer_review_sha256": sha((root / "reviews_v0_36" / review_name).read_bytes()),
                                   "scope": "Final conditional endpoints and residuals inspected; mathematical proof review certified by the bound independent component review."})
    assert len(newclaims) == 71 and newclaims == allclaims - baselineclaims

    # Report the scope judgments separately from the automatic checks.
    findings = [
        {"id": "STRUCTURE_AND_COUNTS", "result": "PASS",
         "finding": "All 121 selected node IDs, kinds, statuses, categories, gates and dependency lists are unchanged from v0.35. All nodes are reachable jointly from the two roots; the graph is acyclic with no missing logical reference. RH reaches 101 and unrestricted Dirichlet GRH 110. The 34 open selected leaves remain exactly 23 C, 9 B, 2 D; v0.36 closes no whole selected leaf."},
        {"id": "COUNT_II_COUPLED_CHOICE", "result": "PASS",
         "finding": "CCH15 and CCH16 are consumed as one existential witness: the same extended original point and its constructed g=0 Kap satisfy the entire h=0,a=n=4 Choice and literal B2. C=0 is fixed before every m and works at every N for every later actual T. Neither the arbitrary-Kap obstruction theorem nor a new Choice witness is inferred. The complete twisted/polarized detector, original full cyclotomic kernel, ramification, old N4, full determinant law, same map/kernel and ell=3 are retained."},
        {"id": "COUNT_II_REMAINING_PRODUCERS", "result": "PASS",
         "finding": "COUNT_II_SUPPORT remains C with both original rank-four Links, fixed iota before the common coefficient threshold, and one J within each original ring carrying all six Hida properties and P1core. Ordinary/control/fibers, integral type/neatU/TThetaEx, four further Hida endpoints, same-J all-level HasAut, exact B1 with 4[L+:Q]+4T.q, and h=0 Raw remain. CohP, LocCFT, N4, nontrivial residual cyclotomic character and other original side conditions are explicit. g=0 is not treated as vanishing of Sel1."},
        {"id": "SIMULTANEOUS_IO_OBJECTS", "result": "PASS",
         "finding": "CFB13 and JIO19 preserve one original R, c0L/cV/BV, exact polynomial range VV(C,lam), inverse-transpose/conjugation order, original base model and signed weights. JIO chooses io_i before every t, retains exact unit-input Delta normalization and both actual Weil laws, and activates the stored OrZero choice without identifying two maps. The common R and its level-character, IsFam/tie, IsModels, Weil and vacuum predicates are supplied inputs, not produced family existence."},
        {"id": "RQC21_22_GUARDS", "result": "PASS",
         "finding": "IsReg is proved from the same supplied FinPair on literal nuQ. Hilbert smoothness and ordered words, cusp closure and Gelfand scalar action are completed conditional suppliers. RQC21 retains an actual pointwise multilinear map and its real derivative identities; RQC22 retains bounded HolForm, the target FinPair, model/frame/extremal hypotheses, and seed ZCusp for cusp conclusions. No Hilbert equivalence class is silently replaced by an actual smooth representative."},
        {"id": "ANALYTIC_RESIDUAL", "result": "PASS",
         "finding": "BASE_THETA_CUSPIDAL_EXTENSION stays C. Initial boundedness, actual FinPair, continuous smooth representatives with all pointwise/global-AE derivative identities, fixed-order Sobolev evaluation and uniform moderate growth, and the complete original IsMultMap/low-tensor restriction remain. The Sobolev exponent and finite word list precede x,F,psi on one fixed finite level. Post-Hilbert central finiteness is explicitly barred from circularly supplying initial boundedness."},
        {"id": "FINAL_CUT_AND_SHARED_OBJECTS", "result": "PASS",
         "finding": "The exact ten-input topDesWin cut, class inclusions, same selected family/CH and joined thresholds remain intact. The closed global consumer retains common construction, Duty, compatible second layer and Link inputs. The smaller fullness route excludes GL4 and final global-slope assembly. Base reading, analytic extension, rational tests and primitive rows remain joint predicates on one selected Bundle, with thresholds before family members and basis vectors."},
        {"id": "TARGET_AND_ROUTE_SCOPE", "result": "PASS",
         "finding": "RH and two-primary targets use Cases I/II/V; unrestricted Dirichlet GRH retains III, SeedIV and all selected chain producers. The Count-I Kstar field and Count-V Gaussian/quartic field are not identified. Fixed-target Count-V scope is retained, while stronger universal helpers are only sufficient. Direct-gap and broad catalogue alternatives remain outside selected logical reachability. Work-sharing/refinement edges do not act as sufficient AND expansions."},
        {"id": "HISTORY_NARRATIVE_AND_CLASSIFICATION", "result": "PASS",
         "finding": "All 245 historical records and 107 scope groups are preserved, including ten originally absent IDs represented by their stable audit IDs and original indices. Each A/B/C/D classification and applicability remains explicit; additive v0.36 updates do not silently retire compound obligations. Historical category totals are not completion percentages. The standalone and TeX narratives agree with the current graph and reproduce all 34 exact remaining contracts; D concerns only human source matching, never assumed formal correctness."},
    ]
    bound_files = ["dependency_audit_v0_36/remaining_leaf_register.json",
                   "dependency_audit_v0_36/target_disposition.json",
                   "dependency_audit_v0_36/closure_delta.json",
                   "dependency_audit_v0_36/published_applications.json",
                   "dependency_audit_v0_36/audit.txt",
                   "dependency_audit_v0_36/audit_intro.txt",
                   "dependency_audit_v0_36/audit_intro.tex"]
    report = {
        "schema": "rh-independent-selected-route-review/1", "artifact_version": "0.36",
        "date": "2026-11-22", "reviewer": "/root/audit_global_routes", "author": "/root",
        "status": "PASS", "verdict": "PASS", "source_commit": PIN,
        "scope": "Independent logical-scope review of the final selected graph and both narratives against v0.35, exact current component endpoints/closures and pinned source contracts; independent structural, provenance, review-binding and backlog validation. This is not a new Lean check or a second proof of every inherited claim.",
        "formal_correctness_assumed": True,
        "graph_file": "dependency_audit_v0_36/obligation_map.json",
        "graph_sha256": FROZEN["dependency_audit_v0_36/obligation_map.json"],
        "graph_file_sha256": FROZEN["dependency_audit_v0_36/obligation_map.json"],
        "narrative": {"file": "dependency_audit_v0_36/main.tex", "sha256": FROZEN["dependency_audit_v0_36/main.tex"]},
        "standalone_audit": {"file": "RH_dependency_audit_v0_36.txt", "sha256": FROZEN["RH_dependency_audit_v0_36.txt"]},
        "additional_bound_files": [{"file": f, "sha256": sha((root/f).read_bytes())} for f in bound_files],
        "predecessor": {"version": "0.35", "graph_file": "dependency_audit_v0_35/obligation_map.json", "sha256": sha((oldroot/"dependency_audit_v0_35/obligation_map.json").read_bytes())},
        "counts": {"selected_nodes": 121, "open_selected_leaves": 34, "open_categories": cats,
                   "rh_reachable": len(rr), "grh_reachable": len(rg), "additional_whole_selected_leaves_closed": 0,
                   "work_refinement_nodes": 13, "optional_route_records": 8,
                   "historical_target_records": 245, "historical_scope_groups": 107,
                   "baseline_claims": 1699, "new_claims": 71, "cumulative_claims": 1770},
        "findings": findings,
        "verification": {"missing_logical_references": [], "cycles": [],
                         "all_selected_nodes_reachable": True, "all_logical_edges_unchanged": True,
                         "all_node_statuses_and_categories_unchanged": True,
                         "remaining_register_exactly_matches_graph": True,
                         "all_remaining_contracts_in_standalone": True,
                         "all_graph_input_hashes_checked": len(graph["source_inputs"]),
                         "component_evidence_file_bindings_checked": len(evidence_bindings),
                         "distinct_direct_graph_source_ranges_checked": len(graph_source_ranges),
                         "distinct_source_ranges_checked_in_graph_and_new_claims": len(source_ranges),
                         "pinned_source_files_checked": len(source_blobs),
                         "new_claim_source_occurrences_checked": new_source_occurrences,
                         "new_proof_blocks_checked": len(proof_hashes),
                         "all_new_actual_depends_on_ids_indexed": True,
                         "all_four_component_reviews_bound_to_released_bytes": True,
                         "all_245_original_and_predecessor_record_hashes_checked": True,
                         "all_107_groups_partition_records": True,
                         "new_Lean_build_performed": False},
        "component_bindings": component_bindings,
        "new_proof_blocks": proof_hashes,
        "required_corrections": [], "unresolved_review_issues": [],
        "review_boundary": "The 34 retained selected producers/tasks remain open. Historical pending-review annotations inside immutable component metadata are superseded only by their exact-byte independent review records. No mathematical component was edited by this graph review.",
    }
    (args.out / "selected_route_graph_review.json").write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n")
    paragraphs = [
        "INDEPENDENT SELECTED-ROUTE REVIEW — VERSION 0.36\n",
        "Reviewer: /root/audit_global_routes\nVerdict: PASS\nSource pin: " + PIN + "\n",
        "Scope: the final selected-route dependency graph, TeX narrative, standalone audit and complete remaining register, compared with v0.35 and the exact four v0.36 component endpoints/closures. Formal correctness is assumed. This review checks the human reconstruction's logical scope and provenance; it is not a Lean replay or a claim that all remaining arithmetic/analytic inputs are proved.\n",
        "EXACT COUNTS\n121 selected nodes; 34 open selected leaves (23 C, 9 B, 2 D). No whole selected leaf is newly closed in v0.36. RH reaches 101 nodes and unrestricted Dirichlet GRH 110; their union is the entire selected graph. There are 13 nonlogical work-refinement nodes and 8 optional route records. The 245 historical continuation records remain in 107 scope groups. The cumulative proof has 1770 indexed claims, comprising 1699 inherited and 71 new claims.\n",
    ]
    for f in findings:
        paragraphs.append(f["id"] + " — " + f["result"] + "\n" + f["finding"] + "\n")
    v = report["verification"]
    paragraphs.append("INDEPENDENT BYTE AND STRUCTURE CHECKS\n"
                      f"Verified all {v['all_graph_input_hashes_checked']} graph input hashes and {len(evidence_bindings)} current component-evidence file bindings; {len(graph_source_ranges)} distinct direct graph source ranges; {len(source_ranges)} distinct graph/new-claim source ranges in {len(source_blobs)} pinned source files; all {new_source_occurrences} new claim-source occurrences and 71 proof blocks. Every checked source file equals its git blob at the stated pin. Every new depends_on ID is indexed, and all four independent component reviews bind to the released proof/provenance/closure bytes. All 245 original-record and predecessor-record hashes and the exact 107-group partition were checked. The full graph is acyclic with no missing reference. The open-leaf register equals the current graph leaves, and every exact remaining contract is present in the standalone audit.\n")
    paragraphs.append("FROZEN FILE BINDINGS\n" + "\n".join(f"{f}\n  SHA256 {h}" for f, h in FROZEN.items()) + "\n")
    paragraphs.append("OTHER BOUND AUDIT FILES\n" + "\n".join(f"{x['file']}\n  SHA256 {x['sha256']}" for x in report["additional_bound_files"]) + "\n")
    paragraphs.append("COMPONENT BINDINGS\n" + "\n\n".join(
        f"{x['component']} ({x['claim_count']} claims)\n  main.tex {x['main_tex_sha256']}\n  provenance.json {x['provenance_sha256']}\n  closure.json {x['closure_sha256']}\n  independent review {x['peer_review_file']}\n  review SHA256 {x['peer_review_sha256']}"
        for x in component_bindings) + "\n")
    paragraphs.append("REQUIRED CORRECTIONS: none.\nUNRESOLVED REVIEW ISSUES: none.\nNo mathematical component was changed in this review. The explicitly listed open producers are not review defects; they are the remaining human-proof frontier.\n")
    (args.out / "selected_route_graph_review.txt").write_text("\n".join(paragraphs))
    print(json.dumps({"status": "PASS", "counts": report["counts"], "verification": v,
                      "graph_sha256": report["graph_sha256"],
                      "review_json_sha256": sha((args.out/"selected_route_graph_review.json").read_bytes()),
                      "review_txt_sha256": sha((args.out/"selected_route_graph_review.txt").read_bytes())}, indent=2))


if __name__ == "__main__":
    main()
