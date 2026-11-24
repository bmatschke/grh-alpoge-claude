#!/usr/bin/env python3
"""Bind the independent v0.38 graph/narrative review to the reviewed release.

The assertions verify structure and byte identity. Mathematical judgments are
the separately performed human review recorded in CHECKS, not inferred from
these assertions. Only this review directory receives outputs.
"""
from pathlib import Path
from collections import Counter
import argparse
import hashlib
import json
import subprocess

PIN = "7cbf7a0c32fca1badf05931879a37c3f8a2b03b4"
HERE = Path(__file__).resolve().parent
WORKSPACE = HERE.parents[1]

CHECKS = [
    ("GA1", "Selected sufficient graph",
     "The selected logical graph retains all 121 predecessor nodes and every logical edge and gate. Its AND rules are sufficient conjunctions on the displayed same witnesses, not assertions that the open input producers already exist. Nonlogical refinements and optional routes stay outside logical sufficiency."),
    ("GA2", "Exact single closure",
     "The only status/category change among selected nodes is BASE_THETA_CUSPIDAL_EXTENSION: its complete producer is proved in its original common-data scope. The 33 remaining open leaves are exactly 22 C, 9 B and 2 D. No Raw, common construction or second division output is closed by inference."),
    ("GA3", "Root scopes",
     "RH reaches 101 nodes; unrestricted Dirichlet GRH reaches 110; together they reach all 121. Both retain Cases I/II/V. The fixed-target two-primary exclusion removes the Case-III branch only from the RH route. Unrestricted GRH retains CaseIII, SeedIV and the original chains."),
    ("GA4", "Original final interface",
     "The original ten-input final interface and its common-family/Closed order are unchanged. Completed assembly consumers retain the original local installation, denominator, retained-defect, period-height, local-gain, spectral and second-layer suppliers."),
    ("GA5", "Finite-volume scope",
     "FV proves the entire original FiniteVolume2 for every actual CM unitary group, every Haar measure and every supplied a.e. fundamental domain. Borel's algebraic group, rational-character, topology and quotient conventions have been matched. FV is not an assertion that an isotropic quotient is compact."),
    ("GA6", "Finite classes and arithmetic components",
     "Finite adelic classes hold at every original open finite level. The arithmetic Gamma_s statement is restricted to compact-open K, and a general original open level supplies such a sublevel. Each target FinPair is chosen before all later t,x and function choices."),
    ("GA7", "Pre-Hilbert initial bound",
     "SBD proves full enveloping-center finiteness directly on the actual initial highest-weight seed, with original frame, gelf length and right-fold conventions. It does not obtain initial boundedness circularly from the later regular Hilbert representation."),
    ("GA8", "Original cusp and checked published application",
     "SBD's original ZI/additive-adele dictionary and compact finite-level fundamental domain give real transvection averages. Its cocharacter argument supplies a central rational transvection in every proper rational parabolic radical. The real unipotent quotient and all cusp/center/norm/arithmetic hypotheses of Miller–Schmid are checked before the finite rational Siegel cover is used."),
    ("GA9", "Complete analytic endpoint and quantifiers",
     "For all original i,t,x the initial bound has exists C before all g, without invented uniformity in t,x. Together with target FinPair and inherited io/lowest-type/Sobolev/pointwise-MMap results, SBD supplies the exact all-parameter theta extension on the same R. No additional eventual threshold is introduced. Common readings, rational tests and actual base rows remain separate."),
    ("GA10", "Generic row integrability remains separate",
     "SBD's actual seed theorem is not promoted to universal CuspRapidDecay or global quotient-height decay for arbitrary IsAutFunSm/IsCuspFun. DI explicitly consumes additional RowPairInt for every original translated c(v),w(v') pair on the same MY0, scaled measure and fd0. Identity, inversion and quotient right invariance give the untranslated/adjoint products, then finite summation gives e0. IsMultIP witness existence is not required: empty witness sets give the original default zero."),
    ("GA11", "Original common design class",
     "The active common producer retains Cdes=WithTw(WithSm Cprime), Cprime=WithChN(A intersect target class), one Built class A, cT=cTmin and original RecExP/RecAtG. Size/rank properties of members do not supply a member. A single ReadC precedes later twists; all metrics, fields, periods and maps remain coupled."),
    ("GA12", "Actual base reading and tests",
     "The active base-reading contract retains every-family/eventual/i<m order, original weak models/Weil data and phase-one pins, and exact LiftTie.theta/mtRead/mjRead/ThDef3 identification with Bundle.P.A3/P.Zs/P.S0. Rational tests and RowsHold0_3 remain independent same-Bundle producers. No isomorphic replacement is substituted."),
    ("GA13", "First versus second division outputs",
     "DI supplies a sufficient conditional first-DivDef3 constructor at the actual updated R,F,Y,Z,C,sEE, including level/projector/composite identities and li/span/lat. Its full five-predicate real-group input, Pins/Holds, nonzero stored IsItW chain, group tie and additional RowPairInt remain. It does not yet reconstruct the original theorem from its original premises alone. The stronger second DivRows3 theta square and common datum are not produced."),
    ("GA14", "Literal row measure and finite choice",
     "The row metric retains ofReal(nP^-1) times original nu0 on unchanged fd0. DI's finite adjoint argument compares the complete IsMultIP witness sets and their original choices. It does not introduce a replacement Petersson pairing or a new existence/nonzero scalar premise."),
    ("GA15", "Count-II joint witness and thresholds",
     "Both original rank-four Links retain fixed iota before one common coefficient threshold and one J carrying all six Hida fields plus P1core. The same full-block h=0,a=n=4,g=0 Choice/B1/B2 is used. One B1 constant precedes m, and eventual N is uniform over every original admissible rep-prime under its finiteness guard. Actual TWPl, CohP, LocCFT, old N4 and ell=3 remain."),
    ("GA16", "Completed representation and conditional limit",
     "CRW supplies the actual completed full-block S6, coefficient DVR and cotangent/presentation comparison on its original point/completion inputs. CohLim is proved only on the same supplied Lim. The full determinant-law application does not invert n!, and selected g=0 is not a Sel1=0 assertion."),
    ("GA17", "Raw support and descent remain",
     "The one-point ChainAbs/Core implication consumes the matched patched ring/maps/modules, support dimension/fiber and annihilator-J equivalence. Actual S4, patching and S5 support, coefficient normalization and pro-ell descent remain. Ordinary/control/type/neatU/TThetaEx, four Hida endpoints and all-level same-J HasAut remain open."),
    ("GA18", "Other retained shared producers",
     "Actual NBuilt/NdSpec and the original row-spectrum/projection square remain distinct from their completed transport consumers. Quantitative LinkS retains the literal Gamma normalization and exponentially small uniform errors. The weaker second-layer fullness route is not enlarged to require the stronger GL4/final-assembly path."),
    ("GA19", "Historical continuity",
     "All 245 inherited compound targets in 107 groups retain their predecessor scopes and receive only additive version updates. All predecessor claim fields and source arrays are preserved. Historical RF16 remains governed by DEX11. Counts describe registers, not mathematical completion percentages."),
    ("GA20", "Next priority and classifications",
     "The continuation note uses the newly closed theta extension as an input, then prioritizes actual common reading, rationality tests, a bounded generic row-integral subtarget, actual local rows and spectral estimates. Prospective work is not counted as proof. B records difficulty/reconstructibility separately from completion; D records human understanding only."),
    ("GA21", "Explicit unproved global-height bridge",
     "Published.CuspRapidDecay requires IsUnifModerate in the global source height. IsAutFunSm and ASB/SPR give per-finite-coset normInf growth. ExistsSigmaList.growth_iff uses quantitative polynomial unitary reduction, not supplied by FV's qualitative finite classes. DI therefore retains RowPairInt as an additional human producer; universal cusp decay alone is not silently treated as a proved route to those integrals. The direct componentwise M–S alternative in the note retains its generic center and NI-cusp bridges as prospective."),
]

RESOLVED = [
    {
        "id": "RESTORE_ORIGINAL_DESIGN_CLASS",
        "initial_issue": "The replacement active common contract omitted the original Cdes/Cprime/A/cT and RecExP/RecAtG prefix.",
        "resolution": "The complete original class and common-family scope is restored in the active contract, not only retained historically.",
    },
    {
        "id": "RESTORE_BASE_READING_QUANTIFIERS",
        "initial_issue": "The replacement base-reading contract omitted the explicit every-family/eventual/i<m order and stored-map identifications.",
        "resolution": "The original quantified prefix and LiftTie.theta/mtRead/mjRead/ThDef3 to Bundle.P.A3/P.Zs/P.S0 identities are restored.",
    },
    {
        "id": "NO_EXTRA_SCALAR_WITNESS",
        "initial_issue": "One draft next-step sentence requested a nonzero scalar-witness input for the row pairing.",
        "resolution": "The sentence now asks only for actual pair/finite-translate integrability and distinguishes the separate nonzero IsItW chain. DI's empty-witness case remains explicit.",
    },
    {
        "id": "B_CLASSIFICATION_VERSUS_STATUS",
        "initial_issue": "The draft TeX legend described all B arguments as already reconstructed although nine B leaves remain open.",
        "resolution": "B is now reconstructibility/difficulty; completion is stated separately.",
    },
    {
        "id": "FULL_DI_REAL_GROUP_CONTRACT",
        "initial_issue": "Summary contracts named only two of DI1's five retained real-group predicates.",
        "resolution": "The full DiscreteSeriesCover/HarishChandraModules/CasselmanWallach/HarishChandraFinite/CuspRapidDecay input is retained explicitly in active contracts and common binding.",
    },
    {
        "id": "CFO_EXACT_UNIFORMITY",
        "initial_issue": "The new Count-II contract compressed the prior exact quantifier order to 'all original dualN uniformity'.",
        "resolution": "The one-C-before-m, eventual-N-uniform-all-admissible-representations/finiteness/TWPl/CohP sentence is restored.",
    },
    {
        "id": "ROW_PAIR_INTEGRABILITY_HEIGHT_GUARD",
        "initial_issue": "Final DI source backtracking found that applying CuspRapidDecay to IsAutFunSm values silently used the unreconstructed global-height growth_iff/polynomial-reduction bridge.",
        "resolution": "DI and the active audit now retain exact additional RowPairInt. The first division result is described as a sufficient conditional refinement, not the entire original theorem from original premises alone; the continuation note records the missing conversion and smaller prospective L2 route.",
    },
]


def sha(data):
    return hashlib.sha256(data).hexdigest()


def read(path):
    return json.loads(path.read_text())


def dag(nodes, deps):
    color = {}
    def visit(k):
        assert k in nodes, ("unknown dependency", k)
        assert color.get(k) != 1, ("cycle", k)
        if color.get(k) == 2:
            return
        color[k] = 1
        for child in deps(nodes[k]):
            visit(child)
        color[k] = 2
    for k in nodes:
        visit(k)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--release", type=Path, default=WORKSPACE / "reconstruction_v038")
    ap.add_argument("--predecessor", type=Path, default=WORKSPACE / "reconstruction_v037")
    ap.add_argument("--source", type=Path, default=WORKSPACE / "lean_source")
    ap.add_argument("--expected", type=Path, required=True,
                    help="JSON map of finally reviewed release paths to exact SHA256")
    args = ap.parse_args()
    release, prior, source = args.release.resolve(), args.predecessor.resolve(), args.source.resolve()
    expected = read(args.expected)
    for file, digest in expected.items():
        assert sha((release / file).read_bytes()) == digest, ("reviewed bytes changed", file)
    aud, old_aud = release / "dependency_audit_v0_38", prior / "dependency_audit_v0_37"
    g, old = read(aud / "obligation_map.json"), read(old_aud / "obligation_map.json")
    assert g["source_commit"] == old["source_commit"] == PIN
    nodes, old_nodes = ({n["id"]: n for n in x["nodes"]} for x in (g, old))
    assert len(nodes) == len(g["nodes"]) == 121 and set(nodes) == set(old_nodes)
    changed = []
    for k, o in old_nodes.items():
        n = nodes[k]
        for f in ("requires", "gate"):
            assert n.get(f) == o.get(f), (k, f)
        if (n["category"], n["status"]) != (o["category"], o["status"]):
            changed.append(k)
    assert changed == ["BASE_THETA_CUSPIDAL_EXTENSION"], changed
    closed = nodes[changed[0]]
    assert closed["status"] == "proved_in_stated_scope" and closed["category"] == "B"
    assert closed["closure"]["claim"] == "SBD16"
    dag(nodes, lambda n: n["requires"])
    def reach(root):
        seen, todo = set(), [root]
        while todo:
            k = todo.pop()
            if k not in seen:
                seen.add(k)
                todo.extend(nodes[k]["requires"])
        return seen
    rh, grh = reach("ORDINARY_RH"), reach("DIRICHLET_GRH")
    assert len(rh) == 101 and len(grh) == 110 and rh | grh == set(nodes)
    assert {"COUNT_I", "COUNT_II", "COUNT_V_PRODUCER"} <= rh & grh
    case3 = {"COUNT_III_PRODUCER", "COUNT_III_GENERAL", "CASE3_PROMOD", "SEED_IV_ALT",
             "TENSOR_FACTOR_TOWER", "CHAIN_RANK_FOUR", "CHAIN_DESC4", "RANK4_CHAIN_REDUCTION"}
    assert not rh & case3 and case3 <= grh
    for k in ("work_refinement_nodes", "work_refinement_links", "optional_routes"):
        assert g[k] == old[k], k
    reg = read(aud / "remaining_leaf_register.json")
    leaves = [n for n in nodes.values() if n["gate"] == "LEAF" and n["status"] not in
              ("proved_in_stated_scope", "published_application_checked")]
    assert len(leaves) == len(reg["records"]) == 33
    assert Counter(n["category"] for n in leaves) == Counter(C=22, B=9, D=2)
    assert {n["id"] for n in leaves if n["category"] == "D"} == {"AD_VANISH_K_MATCH", "HOST_RIGID_S"}
    assert {n["id"]: n for n in leaves} == {n["id"]: n for n in reg["records"]}
    txt = (release / "RH_dependency_audit_v0_38.txt").read_text()
    for n in reg["records"]:
        assert n["contract"] in txt, ("TXT missing full contract", n["id"])
    for key in ("Cdes=WithTw(WithSm Cprime)", "cT(eps,y)=cTmin(y)", "RecExP/RecAtG"):
        assert key in nodes["DESIGN_CHOICES_COMMON"]["contract"], key
    for key in ("For every family", "eventually", "for each i<m", "LiftTie.theta", "mtRead",
                "mjRead", "ThDef3", "Bundle.P.A3", "P.Zs", "P.S0"):
        assert key in nodes["BASE_THETA_READINGS"]["contract"], key
    for k in ("DESIGN_CHOICES_COMMON", "BASE_THETA_READINGS"):
        for pred in ("DiscreteSeriesCover", "HarishChandraModules", "CasselmanWallach",
                     "HarishChandraFinite", "CuspRapidDecay"):
            assert pred in nodes[k]["contract"], (k, pred)
        assert "RowPairInt" in nodes[k]["contract"], (k, "missing extra row integrability")
    for k in ("COUNT_II_SUPPORT", "DESIGN_CHOICES_COMMON", "BASE_THETA_READINGS",
              "BASE_THETA_RATIONAL_TESTS", "SLR_BASE_ROWS_PRODUCER",
              "SECOND_LAYER_COMPATIBLE_SELECTION"):
        assert nodes[k]["status"] == old_nodes[k]["status"] and nodes[k]["category"] == old_nodes[k]["category"]
    td, old_td = read(aud / "target_disposition.json"), read(old_aud / "target_disposition.json")
    assert len(td["records"]) == 245 and len(td["scope_groups"]) == 107
    assert td["scope_groups"] == old_td["scope_groups"]
    assert [n["id"] for n in td["records"]] == [n["id"] for n in old_td["records"]]
    for new_r, old_r in zip(td["records"], old_td["records"]):
        for k, v in old_r.items():
            if k != "predecessor_record_sha256":
                assert new_r[k] == v, ("historical target mutated", old_r["id"], k)
    assert read(aud / "closure_delta.json")["closed_selected_leaves"] == ["BASE_THETA_CUSPIDAL_EXTENSION"]
    for inp in g["source_inputs"].values():
        assert sha((release / inp["file"]).read_bytes()) == inp["sha256"], inp["file"]
    refs, bindings = {}, set()
    def walk(x):
        if isinstance(x, dict):
            if str(x.get("path", "")).startswith("src/") and "line_start" in x and "line_end" in x:
                refs[(x["path"], x["line_start"], x["line_end"])] = x
            for fk, hk in (("proof_file", "proof_sha256"), ("ledger", "ledger_sha256")):
                if fk in x and hk in x:
                    bindings.add((x[fk], x[hk]))
            for y in x.values():
                walk(y)
        elif isinstance(x, list):
            for y in x:
                walk(y)
    walk(g)
    source_bytes = {}
    for (file, start, end), record in refs.items():
        if file not in source_bytes:
            data = (source / file).read_bytes()
            assert data == subprocess.check_output(["git", "show", PIN + ":" + file], cwd=source), file
            source_bytes[file] = data
        data = source_bytes[file]
        digest = record.get("file_sha256", record.get("full_file_sha256", record.get("sha256")))
        if digest:
            assert sha(data) == digest, file
        if record.get("range_sha256"):
            assert sha(b"".join(data.splitlines(keepends=True)[start - 1:end])) == record["range_sha256"], (file, start, end)
    for file, digest in bindings:
        assert sha((release / file).read_bytes()) == digest, ("graph artifact binding", file)
    cfg = read(release / "increment_v0_38.json")
    component_claims = {}
    for component in cfg["components"]:
        p = read(release / component / "provenance.json")
        ids = [c["id"] for c in p["claims"]]
        assert ids == cfg["component_claims"][component]
        component_claims[component] = ids
    expected_new = set(sum(component_claims.values(), []))
    merged = read(release / "provenance.json")
    prior_prov = read(prior / "provenance.json")
    claims, old_claims = ({c["id"]: c for c in p["claims"]} for p in (merged, prior_prov))
    assert len(claims) == len(merged["claims"])
    assert set(claims) - set(old_claims) == expected_new
    assert len(expected_new) == cfg["expected_new_claims"]
    for k, record in old_claims.items():
        for f, v in record.items():
            assert claims[k].get(f) == v, ("predecessor proof field mutated", k, f)
    dag(claims, lambda c: c.get("depends_on", []))
    applications = read(aud / "published_applications.json")["freshly_checked_applications"]
    assert len({a["id"] for a in applications}) == len(applications)
    report = {
        "schema": "rh-independent-selected-audit-review/1",
        "artifact_version": "0.38",
        "reviewer": "/root/audit_literature",
        "status": "PASS",
        "source_commit": PIN,
        "graph_file_sha256": expected["dependency_audit_v0_38/obligation_map.json"],
        "narrative_file_sha256": expected["dependency_audit_v0_38/main.tex"],
        "readable_audit_file_sha256": expected["RH_dependency_audit_v0_38.txt"],
        "reviewed_files": [{"file": k, "sha256": v} for k, v in expected.items()],
        "checks": [{"id": k, "title": t, "status": "PASS", "finding": f} for k, t, f in CHECKS],
        "resolved_findings": [dict(r, status="resolved") for r in RESOLVED],
        "required_corrections": [],
        "structural_validation": {
            "logical_nodes": len(nodes),
            "logical_edges": sum(len(n["requires"]) for n in nodes.values()),
            "all_predecessor_logical_edges_and_gates_preserved": True,
            "only_changed_status_category_node": changed,
            "RH_reachable": len(rh), "Dirichlet_GRH_reachable": len(grh),
            "all_selected_nodes_reachable": True,
            "logical_and_claim_graphs_acyclic": True,
            "open_leaves": len(leaves),
            "open_categories": dict(Counter(n["category"] for n in leaves)),
            "work_refinement_nodes": len(g["work_refinement_nodes"]),
            "optional_routes": len(g["optional_routes"]),
            "nonlogical_and_optional_records_unchanged": True,
            "historical_targets": 245, "historical_scope_groups": 107,
            "historical_target_fields_preserved_except_predecessor_rebinding": True,
            "register_equals_open_graph_leaves": True,
            "all_register_contracts_present_verbatim_in_TXT": True,
            "new_claims": len(expected_new),
            "predecessor_claims": len(old_claims),
            "cumulative_claims": len(claims),
            "all_predecessor_claim_fields_preserved": True,
            "source_files_equal_to_pinned_git_blobs": len(source_bytes),
            "source_ranges_verified": len(refs),
            "component_artifact_bindings_verified": len(bindings),
            "all_graph_source_input_hashes_match": True,
            "published_application_records": len(applications),
        },
        "remaining_leaf_register": [{"id": n["id"], "category": n["category"], "status": n["status"],
                                    "contract_sha256": sha(n["contract"].encode())} for n in reg["records"]],
        "scope_of_review": (
            "Independent mathematical scope, same-object quantifier and logical integration review of "
            "the selected graph, narrative and readable audit. The reviewer independently reviewed SBD "
            "mathematics; FV is the reviewer's own component and its independent proof review is the "
            "root's finite_volume_review. CRW and DI proof reviews are separate team certificates. "
            "This graph review does not replace any of those per-claim mathematical reviews."
        ),
        "formal_source_correctness": "Assumed fully checked and correct. No Lean replay/build and no alleged formal gap.",
        "review_builder": "build_selected_route_graph_review.py",
    }
    out_json = HERE / "selected_route_graph_review.json"
    out_txt = HERE / "selected_route_graph_review.txt"
    out_json.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n")
    lines = ["INDEPENDENT SELECTED AUDIT REVIEW — v0.38", "Reviewer: /root/audit_literature",
             "Result: PASS", "", "EXACT REVIEWED BINDINGS"]
    for file, digest in expected.items():
        lines.extend([file, "  SHA256 " + digest])
    lines.extend(["", "MATHEMATICAL AND SCOPE FINDINGS", ""])
    for k, title, finding in CHECKS:
        lines.extend([k + " — PASS — " + title, finding, ""])
    lines.extend(["RESOLVED DRAFT FINDINGS", ""])
    for r in RESOLVED:
        lines.extend([r["id"], r["initial_issue"], r["resolution"], ""])
    lines.extend(["STRUCTURAL AND HASH VALIDATION", "",
                  json.dumps(report["structural_validation"], ensure_ascii=False, indent=2), "",
                  "REVIEW SCOPE", report["scope_of_review"], "",
                  "Remaining required corrections: none.", report["formal_source_correctness"]])
    out_txt.write_text("\n".join(lines) + "\n")
    print(json.dumps({"status": "PASS", "graph_sha256": report["graph_file_sha256"],
                      "review_json_sha256": sha(out_json.read_bytes()),
                      "review_txt_sha256": sha(out_txt.read_bytes()),
                      "validation": report["structural_validation"]}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
