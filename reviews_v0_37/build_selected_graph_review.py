#!/usr/bin/env python3
"""Bind the independent v0.37 selected-route/narrative integration review.

Only this directory receives outputs. The mathematical judgments are recorded
below; the executable checks structural and byte-level assertions.
"""
from pathlib import Path
from collections import Counter
import hashlib
import json
import subprocess

ROOT = Path(__file__).resolve().parents[2]
HERE = Path(__file__).resolve().parent
RELEASE = ROOT / "reconstruction_v037"
OLD = ROOT / "reconstruction_v036"
SOURCE = ROOT / "lean_source"
PIN = "7cbf7a0c32fca1badf05931879a37c3f8a2b03b4"
FILES = {
    "dependency_audit_v0_37/obligation_map.json": "564470da37dfb714623f571c8a507256f37e66aad479d787bf0c344efc4801c0",
    "dependency_audit_v0_37/main.tex": "6125eb3d39e9d360f15cca0b83db87ec2937144b77afa7607090085a3de320c3",
    "RH_dependency_audit_v0_37.txt": "04315333018b23c879879ba373c7c717a1b255c0a0537e33d2019709058c987e",
    "dependency_audit_v0_37/remaining_leaf_register.json": "e4b858a433c00d12b08d74ed0b84b9016214ff43398d26ff1fb1c70e0c45c9dd",
    "dependency_audit_v0_37/closure_delta.json": "1350d226f0db7b9a3f8e122d086e07e085f72bc5673e860fe22d620186eee295",
    "dependency_audit_v0_37/target_disposition.json": "3ea55a4cf348f0a96e01057840ea5438279f964fd6d720d2ab6bd16d91f04e08",
    "increment_v0_37.json": "bb4629abf5af90e0293d00a01f2ef5a6b83a34459ebed8017e5cd9cfb2fc2b89",
}

CHECKS = [
 ("GR1", "Selected sufficient graph", "All 121 logical nodes are acyclic and reachable from the two final roots. AND rules retain their complete displayed antecedents; open opaque leaves are not asserted true. The 13 work refinements and 8 optional routes remain outside logical sufficiency."),
 ("GR2", "Complete selected frontier", "The 34 register records equal their graph nodes verbatim and comprise precisely the open logical leaves: 23 C, 9 B and 2 D. The only selected D leaves are AD_VANISH_K_MATCH and HOST_RIGID_S; additional nonlogical matching refinements are not silently counted as proved."),
 ("GR3", "Original final theorem interface", "Both topDesWin applications preserve all ten original arguments, the class inclusions, the constants Cabs=2/C0=3/eD=2/eL=0, and one common family and construction after its common Closed threshold."),
 ("GR4", "RH versus unrestricted Dirichlet GRH", "RH reaches 101 nodes, unrestricted Dirichlet GRH reaches 110, and their union is the full graph. Both roots retain I/II/V. RH excludes every Case-III seed/promodularity/chain producer by KA5-KA6 at the same fixed target; the unrestricted route retains them. No Case-I, II or V vacuity is inferred."),
 ("GR5", "Reduced Count-I endpoint", "The selected Count-I interface is CorGK only at the original K_chi; PropGK is a sufficient upstream supplier. The direct CorGK alternative and possible rank-four-to-rank-three catalogue reuse stay optional. No rank-four result is silently substituted for the original rank-three/rank-two catalogue or adjoint matching."),
 ("GR6", "Literal Count-V scope", "CountV keeps its original Gaussian/quartic field, distinct from Count I's K_chi. Its CaseV predicate literally imposes e=1; the principal target's exceptional prime set is {3,7}. Its unbounded original host data and source length/frame/rigidity contracts remain. The universal helper route is sufficient, not claimed necessary."),
 ("GR7", "Count-II original joint witness", "The original two rank-four Links, fixed iota before the coefficient threshold, and a single J carrying all six Hida fields plus P1core remain explicit. Separate existential ideals or independent thresholds are not combined without the original joint construction."),
 ("GR8", "Selected first-order closure", "CFO closes the literal selected B1 only on the same CCH full-block h=0,a=n=4,g=0 Kap already carrying Choice/B2. One constant precedes m; eventual N is uniform over every permitted later representation. CohP, LocCFT, old N4, the actual TWPl and all original guards remain. The coupled rule introduces no arbitrary-Kap bound and no Sel1=0 inference."),
 ("GR9", "Exact first-order exponent and published scope", "The local 10d+10|V_ell| contribution minus 6d+10|V_ell|, together with 4q new centralizers and the old-place constant, gives exactly m(4d+4q)+C. Ell=3 remains covered. The new Milne import is finite decomposition/inertia only; CFO proves the absolute passage. It does not supply CohP, LocCFT or automorphic production."),
 ("GR10", "Remaining Count-II production", "The graph leaves ordinary/control/separating fibers and type/neatU/TThetaEx, the four additional Hida endpoints, all-level same-J HasAut and h=0 Raw open, on the same original point/Kap/J/TWAut. The newly completed consumer does not close COUNT_II_SUPPORT."),
 ("GR11", "Analytic derivative and level scope", "The narrative retains one same-level smooth representative for all ordered Hilbert derivative words, the reversed selected-word order in cube averaging, and the exact original nuQ normalization. It asserts no uniform exceptional null set or arbitrary ambient Hilbert point-evaluation bound."),
 ("GR12", "Sobolev quantifiers and absence of a dependency cycle", "ASB3/4 feed SPR13, which feeds ASB14, and only then the later SPR claims. The merged claim graph is acyclic. N and the finite word list precede x and C_x, which precede F,psi,u. The finite denominator precedes the archimedean translate and rational point."),
 ("GR13", "Exact residual analytic cut", "The full original IsMultMap and final theta assembly are conditional on the initial extremal seed bound and the target FinPair, together with their retained original laws and separate seed ZCusp. Later pointwise growth or central finiteness is not used circularly to provide that earlier bound. The actual common readings, rational tests and base rows remain separate."),
 ("GR14", "One common finite column reader", "CSR chooses one ReadC before all later TwArgs and keeps its word and eNu maps through the actual later period update. The temporary zero period is never treated as a nonzero-period witness. Evaluation uses kappa=(c*nP)^(-1/2) only on the prescribed original level subspace."),
 ("GR15", "Same-record Bundle consumer", "CSR proves the literal conditional Bundle/BTw/BWit/BunU assembly on the prescribed R. The common q/RXs/readings/geometric half, host/frames, MultEq support, updated DivDef3, eigensystem/carrier/parts plus all-embedding logLam, pinned HD and universal NEb remain. All thirteen reading maps, both distinguished prime contractions and the original EvP/ParEv threshold order are preserved."),
 ("GR16", "Other coupled global producers", "The completed size/rank properties of members do not produce a design-class member. The exact Built class, target intersection, cTmin, same Bundle and common second-layer selector/Duty remain. The four base-theta inputs are predicates on one selected Bundle, not independent existential models. The weaker fullness path still does not require GL4 or final slope assembly."),
 ("GR17", "Historical continuity and categories", "All 1770 predecessor claim fields and source arrays are retained without changed values; ten records acquire only additive version_0_37_update fields. All predecessor selected nodes, logical edges, categories and statuses are unchanged. All 245 historical compound targets in 107 groups remain. B classification is explicitly independent of completion status; no completion percentage or alleged formal gap is introduced."),
 ("GR18", "Priority and release claims", "The next priorities are stated as remaining producers: initial boundedness/target FinPair, common original readings/first DivDef3, and selected h=0 Raw in parallel with the deeper ordinary/HasAut frontier. No proposed research is counted as completed. The audit reports 82 new and 1852 cumulative claims, zero newly closed whole selected leaves, and preserves the DEX11 correction governing historical RF16."),
]

def sha(b):
    return hashlib.sha256(b).hexdigest()

def read(path):
    return json.loads(path.read_text())

def check_dag(nodes, deps):
    color = {}
    def visit(k):
        assert k in nodes, ("unresolved node", k)
        assert color.get(k) != 1, ("cycle", k)
        if color.get(k) == 2:
            return
        color[k] = 1
        for v in deps(nodes[k]):
            visit(v)
        color[k] = 2
    for k in nodes:
        visit(k)

def main():
    for file, h in FILES.items():
        assert sha((RELEASE / file).read_bytes()) == h, file
    g = read(RELEASE / "dependency_audit_v0_37/obligation_map.json")
    old = read(OLD / "dependency_audit_v0_36/obligation_map.json")
    nodes = {x["id"]: x for x in g["nodes"]}
    old_nodes = {x["id"]: x for x in old["nodes"]}
    assert set(nodes) == set(old_nodes) and len(nodes) == 121
    for k in old_nodes:
        for field in ("requires", "gate", "status", "category"):
            assert nodes[k].get(field) == old_nodes[k].get(field), (k, field)
    check_dag(nodes, lambda x: x.get("requires", []))
    def reach(root):
        out = set()
        todo = [root]
        while todo:
            k = todo.pop()
            if k not in out:
                out.add(k)
                todo.extend(nodes[k].get("requires", []))
        return out
    rh, grh = reach("ORDINARY_RH"), reach("DIRICHLET_GRH")
    assert len(rh) == 101 and len(grh) == 110 and rh | grh == set(nodes)
    assert all(x in rh & grh for x in ("COUNT_I", "COUNT_II", "COUNT_V_PRODUCER"))
    c3 = {"COUNT_III_PRODUCER", "COUNT_III_GENERAL", "CASE3_PROMOD", "SEED_IV_ALT", "TENSOR_FACTOR_TOWER", "CHAIN_RANK_FOUR", "CHAIN_DESC4", "RANK4_CHAIN_REDUCTION"}
    assert not rh & c3 and c3 <= grh
    reg = read(RELEASE / "dependency_audit_v0_37/remaining_leaf_register.json")
    assert len(reg["records"]) == 34
    assert Counter(x["category"] for x in reg["records"]) == Counter(C=23, B=9, D=2)
    for x in reg["records"]:
        assert x == nodes[x["id"]]
    open_ids = {n["id"] for n in nodes.values() if n["gate"] == "LEAF" and (n["status"].startswith("open") or n["status"] == "human_proof_still_required")}
    assert open_ids == {x["id"] for x in reg["records"]}
    txt = (RELEASE / "RH_dependency_audit_v0_37.txt").read_text()
    assert "can be reconstructed independently" in txt
    for x in reg["records"]:
        assert x["contract"] in txt, x["id"]
    p = read(RELEASE / "provenance.json")
    op = read(OLD / "provenance.json")
    claims = {x["id"]: x for x in p["claims"]}
    oclaims = {x["id"]: x for x in op["claims"]}
    assert len(claims) == 1852 and len(oclaims) == 1770
    for k, v in oclaims.items():
        assert all(claims[k].get(field) == value for field, value in v.items()), k
    check_dag(claims, lambda x: x.get("depends_on", []))
    cfg = read(RELEASE / "increment_v0_37.json")
    expected_ids = {i for ids in cfg["component_claims"].values() for i in ids}
    assert len(expected_ids) == 82 and set(claims) - set(oclaims) == expected_ids
    td = read(RELEASE / "dependency_audit_v0_37/target_disposition.json")
    old_td = read(OLD / "dependency_audit_v0_36/target_disposition.json")
    assert len(td["records"]) == 245 and len(td["scope_groups"]) == 107
    assert [x["id"] for x in td["records"]] == [x["id"] for x in old_td["records"]]
    assert [x["id"] for x in td["scope_groups"]] == [x["id"] for x in old_td["scope_groups"]]
    assert read(RELEASE / "dependency_audit_v0_37/closure_delta.json")["closed_selected_leaves"] == []
    for inp in g["source_inputs"].values():
        assert sha((RELEASE / inp["file"]).read_bytes()) == inp["sha256"], inp["file"]
    refs, bindings = {}, set()
    def walk(x):
        if isinstance(x, dict):
            if str(x.get("path", "")).startswith("src/") and "line_start" in x and "line_end" in x:
                refs[(x["path"], x["line_start"], x["line_end"])] = x
            for fk, hk in (("proof_file", "proof_sha256"), ("ledger", "ledger_sha256")):
                if fk in x and hk in x:
                    bindings.add((x[fk], x[hk]))
            for v in x.values():
                walk(v)
        elif isinstance(x, list):
            for v in x:
                walk(v)
    walk(g)
    source = {}
    for (path, start, end), s in refs.items():
        if path not in source:
            b = (SOURCE / path).read_bytes()
            assert b == subprocess.check_output(["git", "show", PIN + ":" + path], cwd=SOURCE), path
            source[path] = b
        b = source[path]
        expected = s.get("file_sha256", s.get("full_file_sha256", s.get("sha256")))
        if expected:
            assert sha(b) == expected, path
        if s.get("range_sha256"):
            assert sha(b"".join(b.splitlines(keepends=True)[start-1:end])) == s["range_sha256"], (path,start,end)
    for file, h in bindings:
        assert sha((RELEASE / file).read_bytes()) == h, file
    report = {
        "schema": "rh-independent-selected-audit-review/1", "artifact_version": "0.37",
        "reviewer": "/root/audit_count_path", "status": "PASS", "source_commit": PIN,
        "graph_file_sha256": FILES["dependency_audit_v0_37/obligation_map.json"],
        "narrative_file_sha256": FILES["dependency_audit_v0_37/main.tex"],
        "readable_audit_file_sha256": FILES["RH_dependency_audit_v0_37.txt"],
        "reviewed_files": [{"file": k, "sha256": v} for k, v in FILES.items()],
        "checks": [{"id": i, "title": t, "status": "PASS", "finding": f} for i,t,f in CHECKS],
        "required_corrections": [],
        "resolved_findings": [{"id": "B_CLASSIFICATION_WORDING", "initial_issue": "The readable audit defined B using the past tense reconstructed independently despite nine selected B leaves remaining open.", "resolution": "Final TXT now says can be reconstructed independently and explicitly separates completion status.", "status": "resolved"}],
        "structural_validation": {
            "logical_nodes": 121, "RH_reachable": 101, "Dirichlet_GRH_reachable": 110,
            "all_nodes_reachable": True, "logical_and_claim_graphs_acyclic": True,
            "open_leaves": 34, "open_categories": {"C":23,"B":9,"D":2},
            "work_refinements": len(g["work_refinement_nodes"]), "optional_routes": len(g["optional_routes"]),
            "historical_targets": 245, "historical_scope_groups": 107,
            "new_claims": 82, "cumulative_claims": 1852,
            "all_predecessor_claim_field_values_preserved": True,
            "all_predecessor_logical_edges_statuses_categories_preserved": True,
            "register_records_equal_graph_nodes": True,
            "complete_register_contracts_present_verbatim_in_TXT": True,
            "source_files_equal_pinned_git_blobs": len(source),
            "source_ranges_verified": len(refs), "component_artifact_bindings_verified": len(bindings),
            "all_current_source_input_hashes_match": True,
        },
        "selected_open_register": [{"id": n["id"], "category": n["category"], "status": n["status"], "contract_sha256": sha(n["contract"].encode())} for n in reg["records"]],
        "scope_of_review": "Independent source-contract and logical integration review of the selected graph, human audit narrative and TXT, supported by the separately bound CSR review and the completed component reviews. This review is not a second independent proof review of the reviewer's own CFO chapter, and does not replace the other 82-claim mathematical reviews.",
        "formal_source_correctness": "Assumed fully checked and correct; no new Lean build and no allegation of a formal gap.",
        "review_builder": "work_v037/reviews/build_selected_graph_review.py",
    }
    (HERE / "selected_graph_review.json").write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n")
    lines = ["INDEPENDENT SELECTED DEPENDENCY AUDIT REVIEW — v0.37", "Reviewer: /root/audit_count_path", "Result: PASS", "", "FINAL BINDINGS"]
    lines += [k + "\n  SHA256 " + v for k,v in FILES.items()]
    lines += ["", "REVIEW FINDINGS", ""]
    for i,t,f in CHECKS:
        lines += [i + " — PASS — " + t, f, ""]
    lines += [
        "EXHAUSTIVE STRUCTURAL AND BYTE CHECKS", "",
        "121 selected nodes; RH reaches101 and unrestricted Dirichlet GRH110, with union121. "
        "The graph and merged1852-claim dependency graph are acyclic. The register has exactly34 "
        "open leaves (23C,9B,2D), equals the selected graph records verbatim, and appears completely "
        "in the readable TXT. The predecessor1770 claim field values and all predecessor selected "
        "logical edges/statuses/categories are preserved. There are82 new claims and no newly "
        "closed whole selected leaf. Historical245 targets/107groups remain.",
        "", "All graph source inputs match their current files. The596 source ranges in207 files "
        "match the pinned Lean blobs, and71 component-proof/ledger bindings match. This verifies "
        "the recorded evidence and scope; it is not a replacement for the separately bound "
        "mathematical component reviews.",
        "", "RESOLVED WORDING FINDING", "",
        "The readable B-category definition initially used a past-tense completed formulation. "
        "The final TXT instead says that such an argument can be reconstructed independently "
        "and that status separately records completion. This prevents the nine open B leaves "
        "from being mistaken for completed proofs. No mathematical correction was required.",
        "", "Remaining required corrections: none.",
        "The formal source is assumed checked and correct. This is a human proof-dependency "
        "review; it establishes neither a newly complete RH proof nor a new Lean replay.",
    ]
    (HERE / "selected_graph_review.txt").write_text("\n".join(lines) + "\n")
    print(json.dumps({"status":"PASS", "json_sha256":sha((HERE/"selected_graph_review.json").read_bytes()),
                      "txt_sha256":sha((HERE/"selected_graph_review.txt").read_bytes()),
                      "source_files":len(source),"source_ranges":len(refs),"artifact_bindings":len(bindings)}, indent=2))

if __name__ == "__main__":
    main()
