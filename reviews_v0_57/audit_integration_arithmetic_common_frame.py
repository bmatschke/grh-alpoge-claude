#!/usr/bin/env python3
"""Independent v0.57 preservation, proof/source binding and exact-scope audit.

Run only after the release assembler announces stable current inputs.
This does not run Lean or infer producer existence from a conditional theorem.
"""
from pathlib import Path
import argparse
import collections
import hashlib
import json
import re
import subprocess
import zipfile

ROOT = Path(__file__).resolve().parents[1]
OLD = ROOT / "history/version_0_56"
PIN = "7cbf7a0c32fca1badf05931879a37c3f8a2b03b4"
ap = argparse.ArgumentParser()
ap.add_argument("--source", type=Path, required=True)
ap.add_argument("--baseline", type=Path, required=True)
ap.add_argument("--preflight", action="store_true", help="Write only a provisional audit while release inputs are still changing")
args = ap.parse_args()
SOURCE, BASELINE = args.source.resolve(), args.baseline.resolve()
errors, checks, bindings = [], [], {}
digest = lambda b: hashlib.sha256(b).hexdigest()


def need(ok, label, detail=None):
    if ok:
        checks.append(label)
    else:
        errors.append({"check": label, "detail": detail})


def raw(rel, bind=True):
    path = ROOT / rel
    try:
        data = path.read_bytes()
    except FileNotFoundError:
        if args.preflight:
            print(json.dumps({"status": "PRELIMINARY_INCOMPLETE", "missing_input": rel,
                              "errors_so_far": errors, "passed_checks_so_far": len(checks)},
                             ensure_ascii=False, indent=2))
        raise
    if bind:
        bindings[str(path.relative_to(ROOT))] = digest(data)
    return data


def read(rel):
    return json.loads(raw(rel))


def walk_dicts(data):
    if isinstance(data, dict):
        yield data
        for value in data.values():
            yield from walk_dicts(value)
    elif isinstance(data, list):
        for value in data:
            yield from walk_dicts(value)


def check_dag(graph, label):
    done, active = set(), set()
    def visit(node):
        if node not in graph:
            raise ValueError(("unknown dependency", node))
        if node in active:
            raise ValueError(("cycle", node))
        if node in done:
            return
        active.add(node)
        for parent in graph[node]:
            visit(parent)
        active.remove(node)
        done.add(node)
    try:
        for node in graph:
            visit(node)
        need(len(done) == len(graph), label)
    except ValueError as exc:
        need(False, label, str(exc))


anchor_locations = {}


def exact_proof_location(claim):
    """Resolve legacy anchors without changing any historical ledger record."""
    loc = claim["proof_location"]
    if "line_start" in loc and "line_end" in loc:
        return loc
    cid = claim["id"]
    if cid in anchor_locations:
        return anchor_locations[cid]
    data = raw(loc["file"])
    need(loc.get("anchors") == [cid], cid + ": legacy anchor is the exact numbered claim")
    starts = list(re.finditer(rb"^\\paragraph\{" + re.escape(cid.encode()) + rb":", data, re.M))
    need(len(starts) == 1, cid + ": legacy proof paragraph has one exact anchor")
    if len(starts) != 1:
        raise ValueError(("ambiguous legacy anchor", cid))
    start = starts[0].start()
    following = re.search(rb"^\\paragraph\{", data[starts[0].end():], re.M)
    end = starts[0].end() + following.start() if following else len(data)
    block = data[start:end]
    expected = claim.get("proof_paragraph_sha256")
    need(digest(block) == expected, cid + ": exact original legacy paragraph SHA256")
    resolved = {"file": loc["file"], "line_start": data[:start].count(b"\n") + 1,
                "line_end": data[:end].count(b"\n"), "sha256": digest(block), "bytes": len(block)}
    anchor_locations[cid] = resolved
    return resolved


def proof_bytes(claim):
    loc = exact_proof_location(claim)
    data = raw(loc["file"])
    lines = data.splitlines(keepends=True)
    a, b = loc["line_start"], loc["line_end"]
    need(1 <= a <= b <= len(lines), claim["id"] + ": valid proof line range")
    return data, b"".join(lines[a-1:b])


need(subprocess.check_output(["git", "-C", str(SOURCE), "rev-parse", "HEAD"], text=True).strip() == PIN,
     "read-only source checkout has the exact accepted pin")
cfg = read("increment_v0_57.json")
stats = read("integration_stats_v0_57.json")
base = read("history/version_0_56/provenance.json")
current = read("provenance.json")
old_index = read("history/version_0_56/source_index.json")
index = read("source_index.json")
record = read("history/version_0_56/baseline_record.json")
need(digest(BASELINE.read_bytes()) == record.get("archive_sha256", record.get("sha256")), "original supplied archive SHA256")
need(record.get("source_commit", PIN) == cfg["source_commit"] == PIN, "baseline and current source pin agree")
need(PIN.encode() in raw("history/version_0_56/README.md"), "frozen baseline readme declares the exact accepted source pin")

# Check preservation against the supplied archive as well as its own manifest.
manifest = raw("history/version_0_56/SHA256SUMS").decode()
entries = [line.split("  ", 1) for line in manifest.splitlines() if line.strip()]
preserved = archived = 0
archived_paths = []
for expected, rel in entries:
    current_path, history_path = ROOT / rel, OLD / rel
    if current_path.is_file() and digest(current_path.read_bytes()) == expected:
        preserved += 1
    elif history_path.is_file() and digest(history_path.read_bytes()) == expected:
        preserved += 1
        archived += 1
        archived_paths.append(rel)
    else:
        need(False, "baseline artifact preserved at its exact original bytes", rel)
need(len(entries) == 9122, "baseline contains exactly 9122 manifest artifacts")
need(preserved == len(entries), "every baseline manifest artifact retained")
need(BASELINE.stat().st_size == record["bytes"], "original archive byte length")
with zipfile.ZipFile(BASELINE) as archive:
    names = set(n for n in archive.namelist() if not n.endswith("/"))
    candidates = [n for n in names if n == "SHA256SUMS" or n.endswith("/SHA256SUMS")]
    manifest_name = min(candidates, key=lambda n: (n.count("/"), len(n)))
    prefix = manifest_name[:-len("SHA256SUMS")]
    need(archive.read(manifest_name) == manifest.encode(), "frozen manifest equals original archive manifest")
    for expected, rel in entries:
        name = prefix + rel
        need(name in names and digest(archive.read(name)) == expected,
             "baseline manifest agrees with archive member: " + rel)
    for rel in record.get("frozen_root_files", [p.name for p in OLD.iterdir() if p.is_file() and p.name != "baseline_record.json"]):
        if prefix + rel in names:
            need((OLD / rel).read_bytes() == archive.read(prefix + rel),
                 "frozen mutable root equals supplied archive: " + rel)
    for rel in ["RH_GRH_reconstruction_roadmap_v0_56.txt",
                "RH_GRH_parallel_execution_plan_v0_56.txt"]:
        need(prefix + rel in names and raw("history/version_0_56/" + rel) == archive.read(prefix + rel),
             "frozen predecessor planning file equals supplied archive: " + rel)

old_claims, claims = base["claims"], current["claims"]
need(len(old_claims) == 3645, "baseline contains exactly 3645 numbered claims")
need(claims[:3645] == old_claims, "all 3645 original claim objects retained literally")
need(current["source_files"][:len(base["source_files"])] == base["source_files"], "original provenance source inventory retained literally")
need(index["source_files"][:len(old_index["source_files"])] == old_index["source_files"], "original source-index prefix retained literally")
new = claims[3645:]
need(len(new) == 101 and len(claims) == 3746, "101 new claims and 3746 cumulative claims")
ids = [c["id"] for c in claims]
byid = {c["id"]: c for c in claims}
graph = current["mathematical_dependency_graph"]
need(len(ids) == len(set(ids)) and set(graph) == set(ids), "unique numbered claims exactly equal DAG nodes")
need(all(graph.get(k) == v for k, v in base["mathematical_dependency_graph"].items()), "all original mathematical dependency edges retained")
check_dag(graph, "cumulative human-argument DAG acyclic with no unknown parent")
order = current["dependency_topological_order"]
pos = {k: i for i, k in enumerate(order)}
need(len(order) == len(ids) and set(order) == set(ids), "topological order covers each numbered claim once")
need(all(pos.get(p, len(ids)) < pos.get(n, -1) for n, ps in graph.items() for p in ps), "every dependency precedes its consumer")

expected_counts = {
    "arithmetic_connectedness_v57": 27,
    "period_gram_v57": 20,
    "determinant_jet_v57": 21,
    "section_growth_v57": 7,
    "faithful_etale_v57": 26,
}
need(set(cfg["components"]) == set(expected_counts), "exact five independently reviewed components")
component_ledgers, sidecars, incoming = {}, {}, []
for component in cfg["components"]:
    ledger = read(component + "/provenance.json")
    component_ledgers[component] = ledger
    incoming.extend(ledger["claims"])
    need(len(ledger["claims"]) == expected_counts[component], component + ": expected claim count")
    need(ledger.get("source_commit", PIN) == PIN, component + ": source pin")
    scope = {k: v for k, v in ledger.items() if k not in {"claims", "source_files", "source_inventory", "source_groups"}}
    need(current["component_scope_metadata_as_received_v0_57"].get(component) == scope,
         component + ": full finalized metadata and original premises retained")
    sidecars[component] = {}
    for filename in ["contracts.json", "closure.json", "original_contracts.json", "retained_foundations.json",
                     "classical_inputs.json", "published_inputs.json", "explicit_inputs.json", "claim_dag.json", "source_manifest.json", "tex_validation.json", "inherited_inputs.json", "retained_inputs.json", "literature_inputs.json", "external_reference.json", "supporting_sources.json", "status.json", "source_mapping.json", "next_consumer.json"]:
        if (ROOT / component / filename).is_file():
            sidecars[component][filename] = read(component + "/" + filename)
    for filename in ["report.txt", "independent_review.md", "next_source_handoff.txt"]:
        if (ROOT / component / filename).is_file():
            raw(component + "/" + filename)
    artifact_manifest = read(component + "/hashes.json")
    if artifact_manifest.get("proof_file_sha256"):
        need(artifact_manifest["proof_file_sha256"] == digest(raw(component + "/main.tex")),
             component + ": artifact inventory binds the final whole proof")
    if isinstance(artifact_manifest.get("files"), list):
        artifact_rows = artifact_manifest["files"]
        need(len(artifact_rows) == len({row["file"] for row in artifact_rows}),
             component + ": artifact inventory has distinct file paths")
        if artifact_manifest.get("file_count") is not None:
            need(artifact_manifest["file_count"] == len(artifact_rows), component + ": artifact inventory count")
    else:
        artifact_rows = [{"file": filename, "sha256": expected}
                         for filename, expected in artifact_manifest.get("hashes", artifact_manifest).items()]
    for artifact_row in artifact_rows:
        filename = artifact_row["file"]
        rel = filename if filename.startswith(component + "/") else component + "/" + filename
        artifact_data = raw(rel)
        need(digest(artifact_data) == artifact_row["sha256"], component + ": finalized artifact manifest " + filename)
        if artifact_row.get("bytes") is not None:
            need(len(artifact_data) == artifact_row["bytes"], component + ": artifact byte length " + filename)
    for filename, value in sidecars[component].items():
        if not isinstance(value, dict):
            continue
        full_hash = value.get("proof_file_sha256", value.get("main_tex_sha256"))
        if full_hash:
            need(full_hash == digest(raw(component + "/main.tex")),
                 component + ": sidecar binds current whole proof: " + filename)
        need(not value.get("pending_review_claims"),
             component + ": no pending independently reviewed claim in " + filename)
    need("pending_independent_review" not in str(ledger.get("status", "")),
         component + ": finalized component status acknowledges independent review")
    for filename in ["contracts.json", "closure.json"]:
        if filename not in sidecars[component]:
            continue
        closure = sidecars[component][filename]
        for key in ["exact_whole_closures", "whole_obligations_closed", "whole_obligation_closures", "new_global_frontier_leaf_closures",
                    "whole_selected_leaf_closed", "proposed_global_frontier_leaf_closures",
                    "whole_selected_obligations_closed", "proposed_whole_obligation_closures", "selected_whole_obligations_closed"]:
            if key in closure:
                need(closure[key] in (False, [], {}), component + ": no new whole selected closure in " + key)
        bound = closure.get("proof_file_sha256", closure.get("main_tex_sha256"))
        if bound:
            need(bound == digest(raw(component + "/main.tex")), component + ": closure proof-file binding")
    external_records = {r["id"] for value in [ledger, *sidecars[component].values()]
                        for r in walk_dicts(value) if isinstance(r.get("id"), str)}
    for claim in ledger["claims"]:
        for key in ["external_input_ids", "published_input_ids", "foundation_input_ids", "conditional_input_ids"]:
            for name in claim.get(key, []):
                need(name in external_records, claim["id"] + ": explicit retained input record " + name)
                need(name not in graph, claim["id"] + ": supplied input distinct from numbered human theorem " + name)
need([c["id"] for c in incoming] == [c["id"] for c in new], "new claim ordering exactly matches configured components")

# Published references and acknowledged literature retain their own hashes and
# roles. They are never counted as files in the accepted formal-source checkout.
nonformal_snapshots_checked = []
for component, component_sidecars in sidecars.items():
    seen = set()
    for filename in ["published_inputs.json", "classical_inputs.json", "literature_inputs.json", "external_reference.json"]:
        for record in walk_dicts(component_sidecars.get(filename, {})):
            snapshot_file = record.get("snapshot_file", record.get("snapshot_path"))
            expected = record.get("sha256")
            if not snapshot_file or not expected or snapshot_file in seen:
                continue
            if "/source_snapshot/" in snapshot_file:
                continue
            seen.add(snapshot_file)
            data = raw(snapshot_file)
            need(digest(data) == expected, component + ": exact separately identified reference snapshot " + snapshot_file)
            if record.get("bytes") is not None:
                need(len(data) == record["bytes"], component + ": reference snapshot byte length " + snapshot_file)
            if "used_as_opaque_mathematical_premise" in record:
                need(record["used_as_opaque_mathematical_premise"] is False,
                     component + ": literature suggestion is not an opaque proof premise " + snapshot_file)
            nonformal_snapshots_checked.append({"component": component, "snapshot_file": snapshot_file,
                                                "sha256": digest(data), "role": record.get("role"),
                                                "commit": record.get("commit"), "url": record.get("url")})

# Completed original suppliers are distinguished from their larger consumers.
# These independently selected guards test exact mathematical scope.
acc = sidecars["arithmetic_connectedness_v57"]["contracts.json"]
acc_cl = sidecars["arithmetic_connectedness_v57"]["closure.json"]
for key in [
    "full_original_c1ch_supplied", "c1ch_general_prime_nilradical_scope",
    "c1ch_additional_IsCO_antecedent_not_needed", "exact_N_equals_Nprime_plus_n_d_plus_one_preserved",
    "actual_Chained_both_ranks_supplied", "full_original_loc_dim_supplied", "full_original_fibre_supplied",
    "full_original_ab_gen_supplied", "rank_two_stronger_fibre_bound_supplied", "rank_two_l51_supplied",
    "full_sharp2_supplied", "full_original_dim_B_supplied", "full_original_l52_supplied",
    "l52_stronger_nd_plus_three_bound", "full_original_NicePrimeEx_supplied",
    "rank_two_actual_Nice_curve_supplier_supplied", "full_original_min_hom_supplied",
    "full_original_jac_supplied", "full_original_l41_supplied", "rank_two_full_seedpt_supplied",
    "full_PropagationTheoremGL2_supplied", "rank_two_all_local_and_global_propagation_fields_supplied",
    "rank_two_seed_weak_inclusion_preserved", "seed_x_chosen_before_every_Loc",
    "FinLam_P1prime_SeedIn_are_original_antecedents", "same_A_B_x_Oprime_R_iota_preserved", "same_g1",
    "original_P_retained_at_arithmetic_entry", "host_ell_3_allowed", "equal_characteristic_coefficient_DVR_allowed",
    "rank_two_and_rank_three_rings_and_ideals_kept_distinct", "upstream_FinA_not_assumed",
    "transcendence_degree_taken_before_completion", "exact_coefficient_uniformizer_cut_retained", "no_lean_replay",
]:
    need(acc.get(key) is True, "ACC completed supplier or exact original scope: " + key)
for key in [
    "c1ch_restricted_to_regular_local", "full_original_l51_both_ranks_supplied", "full_seedpt_both_ranks_supplied",
    "full_PropagationTheoremGL3_supplied", "full_original_EPres_supplied", "full_sharp3_supplied",
    "ModIn_or_automorphic_seed_producers_supplied", "actual_OffFin_producer_supplied",
    "actual_automorphic_or_Alt_producer_supplied", "full_GdEnd_supplied", "full_HostEnd_supplied",
    "full_ClComp_and_ClChain_claimed_separately", "root_ledger_modified", "selected_producer_closed",
]:
    need(acc.get(key) is False, "ACC independent producer or forbidden scope enlargement remains: " + key)
for key in [
    "full_c1ch_closed", "full_sharp2_closed", "full_PropagationTheoremGL2_closed",
    "full_EPres_remains_open", "full_sharp3_remains_open", "rank_three_triangular_and_seed_producers_remain_open",
    "full_PropagationTheoremGL3_remains_open", "actual_OffFin_producer_remains_open",
    "ModIn_automorphic_and_Alt_producers_remain_open", "full_GdEnd_remains_open", "full_HostEnd_remains_open",
    "original_P_retained", "separate_rank_rings_and_coefficient_extensions_preserved",
]:
    need(acc_cl.get(key) is True, "ACC exact closure or retained boundary: " + key)

pgr = sidecars["period_gram_v57"]["contracts.json"]
pgr_cl = sidecars["period_gram_v57"]["closure.json"]
pgr_ret = sidecars["period_gram_v57"]["retained_inputs.json"]
need(pgr.get("primary_endpoint_claim") == pgr.get("endpoint_claim") == "PGR18" and
     pgr.get("next_consumer_claim") == "PGR20", "PGR exact universal KExpansionC and subsequent KTie endpoints")
need(pgr.get("remaining_missing_proof_steps_in_KExpansionC") == [] and
     pgr_cl.get("remaining_missing_proof_steps_in_KExpansionC") == [] and
     pgr_ret.get("unsupplied_new_mathematical_premises_inside_KExpansionC") == [],
     "PGR leaves no disguised new unfolding or period-matching hypothesis")
for key in ["original_endpoint_is_an_implication_with_its_named_premises",
            "no_disguised_period_matching_or_unfolding_assumption"]:
    need(pgr_ret.get(key) is True, "PGR preserves its original implication scope: " + key)
for token in ["PsiDd", "KsetSplit", "NeatKu", "FoldBound", "PoincareSeries", "SlabAbs", "EntryUnfold", "KExpansionC", "KTie"]:
    need(any(token in x for x in pgr["completed_original_substatements"]),
         "PGR records the completed original supplier: " + token)
retained_pgr_text = json.dumps(pgr["retained_original_premises"], ensure_ascii=False)
for token in ["D7", "HidaSetting", "Full", "FoldOK", "InHH", "FundExists", "OOIntAll", "OOFundIndep",
              "AmpWellDef", "AbsConvT", "FinX", "DimTie"]:
    need(token in retained_pgr_text, "PGR retains each original supplied setting or analytic antecedent: " + token)
for token in ["FullExists", "Forms0", "FoldOKC", "InHHC", "FundExistsC", "OOIntAllC", "OOFundIndepC",
              "AmpWellDefC", "AbsConvC", "JacGauge", "RhsWLim", "PlaceSplit", "ProdExact", "RealBracket"]:
    need(any(token in x for x in pgr["remaining_downstream_boundaries"]),
         "PGR retains the independent producer: " + token)
need(not sidecars["period_gram_v57"]["classical_inputs.json"].get("new_unreconstructed_published_mathematical_premises"),
     "PGR distinguishes classical background from a newly imported unproved supplier")


djw = sidecars["determinant_jet_v57"]["contracts.json"]
djw_cl = sidecars["determinant_jet_v57"]["closure.json"]
for key in [
    "full_original_ThmP_supplied", "full_original_BiValue_supplied", "full_original_BiContent_supplied",
    "full_original_BiWindow_supplied", "full_original_content_and_window_supplied", "full_original_MtoHM_supplied",
    "full_original_block_of_normal_form_supplied", "actual_integral_germs_constructed",
    "actual_unit_scalar_identity_proved", "actual_row_window_from_original_MConcl_supplied",
]:
    need(djw.get(key) is True and djw_cl.get(key) is True, "DJW completed literal supplier: " + key)
for key in ["original_LemmaM_existence_supplied", "unconditional_BiSupply_supplied",
            "global_Moduli_or_theta_family_supplied", "global_section_laws_supplied", "GLOBAL_LOCAL_GAIN_reopened"]:
    need(djw.get(key) is False and djw_cl.get(key) is False, "DJW retains the independent original boundary: " + key)
need(bool(djw.get("quantifier_guards")), "DJW records full original coefficient, derivative, zero-size and germ quantifiers")

sgv = sidecars["section_growth_v57"]["contracts.json"]
sgv_cl = sidecars["section_growth_v57"]["closure.json"]
for key in ["full_original_secM_finite_and_growth_output_supplied", "full_original_sections_growth_supplied",
            "all_integer_SecM_finiteness_reused", "exact_positive_power_growth_supplied",
            "actual_identity_product_and_scalars_retained"]:
    need(sgv.get(key) is True and sgv_cl.get(key) is True, "SGV completed original section-growth supplier: " + key)
need(sgv.get("completed_nested_frontier_ids") == sgv_cl.get("completed_nested_frontier_ids") == ["GSL_FINITE_GROWTH"],
     "SGV closes exactly the nested GSL_FINITE_GROWTH frontier")
for key in ["general_filtered_polynomial_growth_supplied", "original_rank_one_supplied",
            "original_torsion_section_decomposition_supplied", "full_GlobalSectionsRankAlgClosed_supplied",
            "full_original_all_cover_positive_power_H1_supplier_supplied", "full_SecBaseChangeSt_supplied",
            "full_SecBaseChangeAnySt_supplied", "full_SecTwistSt_supplied", "global_Moduli_supplied"]:
    need(sgv.get(key) is False and sgv_cl.get(key) is False, "SGV retains the independent geometric supplier: " + key)
need(bool(sgv.get("quantifier_guards")), "SGV records arbitrary-characteristic and exact positive-power quantifiers")

fet = sidecars["faithful_etale_v57"]["contracts.json"]
fet_cl = sidecars["faithful_etale_v57"]["closure.json"]
for key in ["actual_AI_action_preserved", "all_primes_including_two", "fixed_basis_original_integral_lattice_and_rank",
            "linear_descent_distinguished_from_nonlinear_conjugacy", "full_original_etale_functor_all_morphisms"]:
    need(fet.get(key) is True, "FET exact original period-ring and coefficient scope: " + key)
fe = {x["endpoint"]: x for x in fet["completed_source_endpoints"]}
for name, claim in {
    "GlobalTheory.TiltFaithful.faithH": "FET4",
    "GlobalTheory.HWL.FixedBasis.exists_det_ne_zero": "FET6",
    "GlobalTheory.HWL.FixedBasis.main / exists_cyclotomicKernelFixedBasis_wittTensorLattice": "FET13",
    "GlobalTheory.HWL.MatDecompl.decompletion / etalePhiMatrix_decompletion_to_wach": "FET20",
    "GlobalTheory.EtaleBasis.exists_etBasis": "FET21",
    "GlobalTheory.HWL.EtMod.nonempty_wEt": "FET25",
}.items():
    need(fe.get(name, {}).get("claim") == claim and fe.get(name, {}).get("all_original_premises_retained") is True,
         "FET complete original endpoint with its retained premises: " + name)
need(fet.get("conditional_reduction_extra_inputs") == {}, "FET adds no new opaque period-ring premise")
for key in ["full_original_FaithH_complete", "full_original_fixed_basis_complete",
            "full_original_Frobenius_matrix_decompletion_complete", "full_original_EtBasis_complete", "full_original_WEt_complete"]:
    need(fet_cl.get(key) is True, "FET complete original supplier: " + key)
for key in ["full_HW_Fon_Cmp_complete", "full_GLOBAL_DENOMINATOR_supplier_supplied"]:
    need(fet_cl.get(key) is False, "FET preserves independent common-family comparison boundary: " + key)
for token in ["Herr", "HW/Fon/Cmp", "ConclF"]:
    need(any(token in x for x in fet["remaining"]), "FET retains independent downstream producer: " + token)

source_data, source_ranges, proof_files = {}, set(), {}
for original in incoming:
    cid = original["id"]
    integrated = byid[cid]
    need(integrated.get("depends_on", []) == original.get("depends_on", []) == graph[cid], cid + ": exact proof dependency record")
    for key, value in original.items():
        if key not in {"proof_location", "sources"}:
            need(integrated.get(key) == value, cid + ": component field retained: " + key)
    data, block = proof_bytes(integrated)
    pl = integrated["proof_location"]
    need(digest(data) == pl["file_sha256"], cid + ": exact whole proof file")
    need(digest(block) == pl["sha256"] == pl["range_sha256"], cid + ": exact numbered proof block")
    need(bool(re.search(rb"^% BEGIN " + cid.encode() + rb"\s*$", block, re.M)) and
         bool(re.search(rb"^% END " + cid.encode() + rb"\s*$", block, re.M)), cid + ": block includes complete own markers")
    need(len(re.findall(rb"^% BEGIN " + cid.encode() + rb"\s*$", data, re.M)) == 1, cid + ": numbered marker unique")
    proof_files[pl["file"]] = digest(data)
    need(len(original.get("sources", [])) == len(integrated.get("sources", [])), cid + ": all source records retained")
    for before, after in zip(original.get("sources", []), integrated.get("sources", [])):
        need(all(after.get(k) == v for k, v in before.items() if k != "range_sha256"), cid + ": source annotations retained")
    for src in integrated.get("sources", []):
        if "path" not in src or "line_start" not in src:
            continue
        path = src["path"]
        if path not in source_data:
            data_s = (SOURCE / path).read_bytes()
            need(data_s == subprocess.check_output(["git", "-C", str(SOURCE), "show", PIN + ":" + path]),
                 "exact pinned Git source blob: " + path)
            source_data[path] = data_s
            need(raw("source_snapshot_v0_57/" + path) == data_s, "aggregate source snapshot exact: " + path)
        data_s = source_data[path]
        need(digest(data_s) == src.get("file_sha256", src.get("full_file_sha256", src.get("sha256"))), cid + ": full source hash " + path)
        lines = data_s.splitlines(keepends=True)
        a, b = src["line_start"], src["line_end"]
        need(1 <= a <= b <= len(lines) and digest(b"".join(lines[a-1:b])) == src["range_sha256"],
             cid + ": exact source range " + path + ":" + str(a) + "-" + str(b))
        source_ranges.add((path, a, b))
        if src.get("snapshot_file"):
            need(raw(src["snapshot_file"]) == data_s, cid + ": original component snapshot exact")
snapshot = read("source_snapshot_v0_57/manifest.json")
need(snapshot["commit"] == PIN and {r["path"] for r in snapshot["files"]} == set(source_data), "source snapshot inventory exactly covers cited files")
for row in snapshot["files"]:
    need(digest(raw(row["snapshot_path"])) == row["sha256"], "snapshot manifest hash: " + row["path"])
for name, items in [("provenance", current["source_files"]), ("source index", index["source_files"])]:
    mapping = {s["path"]: s for s in items}
    need(len(items) == len(mapping), name + ": unique source paths")
    for path, data_s in source_data.items():
        need(mapping.get(path, {}).get("sha256", mapping.get(path, {}).get("file_sha256")) == digest(data_s), name + ": exact current source " + path)

# Independently verify every component manifest, including source evidence not
# repeated in an integrated claim. Such extra evidence does not inflate the
# aggregate count of files/ranges actually cited by the new claims.
all_component_sources = dict(source_data)
component_manifest_ranges = set()
for component in cfg["components"]:
    manifest = sidecars[component]["source_manifest.json"]
    need(manifest["source_commit"] == PIN, component + ": source-manifest pin")
    for row in manifest.get("files", manifest.get("source_files", [])):
        path = row["path"]
        if path not in all_component_sources:
            data_s = (SOURCE / path).read_bytes()
            need(data_s == subprocess.check_output(["git", "-C", str(SOURCE), "show", PIN + ":" + path]),
                 component + ": additional exact pinned Git source blob " + path)
            all_component_sources[path] = data_s
        data_s = all_component_sources[path]
        need(digest(data_s) == row["sha256"], component + ": source manifest full-file hash " + path)
        if row.get("bytes") is not None:
            need(len(data_s) == row["bytes"], component + ": source manifest byte count " + path)
        snapshot_file = row.get("snapshot_file", row.get("snapshot_path"))
        need(bool(snapshot_file) and raw(snapshot_file) == data_s,
             component + ": source manifest actual snapshot " + path)
    for row in manifest.get("ranges", []):
        path = row["path"]
        lines = all_component_sources[path].splitlines(keepends=True)
        a, b = row["line_start"], row["line_end"]
        need(1 <= a <= b <= len(lines), component + ": manifest range valid " + path)
        part = b"".join(lines[a-1:b])
        need(row["range_sha256"] in {digest(part), digest(part.rstrip(b"\r\n"))},
             component + ": manifest exact source range " + path + ":" + str(a) + "-" + str(b))
        if row.get("range_bytes") is not None:
            need(row["range_bytes"] == len(part), component + ": manifest range byte length " + path)
        component_manifest_ranges.add((path, a, b))
    declarations = set()
    for record in walk_dicts(sidecars[component]):
        for text_key, hash_key in [
            ("exact_definition_text", "definition_sha256"),
            ("exact_source_statement_text", "statement_sha256"),
        ]:
            if text_key in record and hash_key in record:
                need(digest(record[text_key].encode()) == record[hash_key],
                     component + ": retained contract text hash " + record.get("id", record.get("name", "")))
        if "exact_source_declaration_header" in record:
            header = record["exact_source_declaration_header"]
            src = record["source"]
            part = b"".join(all_component_sources[src["path"]].splitlines(keepends=True)[src["line_start"]-1:src["line_end"]])
            need(digest(header.encode()) == record["declaration_header_sha256"] and header in part.decode(),
                 component + ": exact original declaration header " + record.get("claim_id", ""))
        if not all(k in record for k in
                   ["source_path", "declaration_text", "declaration_sha256", "line_start", "line_end"]):
            continue
        path, text_decl = record["source_path"], record["declaration_text"]
        key = (path, record["line_start"], record["line_end"], record["declaration_sha256"])
        if key in declarations:
            continue
        declarations.add(key)
        if path not in all_component_sources:
            data_s = (SOURCE / path).read_bytes()
            need(data_s == subprocess.check_output(["git", "-C", str(SOURCE), "show", PIN + ":" + path]),
                 component + ": additional exact original-contract source " + path)
            all_component_sources[path] = data_s
        lines = all_component_sources[path].decode().splitlines(keepends=True)
        text_range = "".join(lines[record["line_start"]-1:record["line_end"]])
        need(digest(text_decl.encode()) == record["declaration_sha256"] and text_decl in text_range,
             component + ": literal original-contract declaration and hash " + path)

# Dependency repositories are separately pinned and never counted as RH-source
# Git files. Any separately pinned dependency evidence is checked on its own recorded revision.
dependency_files_checked, dependency_manifest_bindings = [], []
for component in cfg["components"]:
    manifest = sidecars[component]["source_manifest.json"]
    deps = manifest.get("dependency_files", []) + manifest.get("supporting_sources", [])
    if not deps:
        continue
    lake_bytes = subprocess.check_output(["git", "-C", str(SOURCE), "show", PIN + ":lake-manifest.json"])
    need(lake_bytes == (SOURCE / "lake-manifest.json").read_bytes(),
         component + ": exact original dependency-manifest Git bytes")
    # This immutable earlier source snapshot carries precisely the same RH pin.
    lake_snapshot = "source_snapshot_v0_53/lake-manifest.json"
    need(raw(lake_snapshot) == lake_bytes, component + ": retained dependency-manifest snapshot equals pinned original")
    dependency_manifest_bindings.append({"component": component, "source_commit": PIN,
                                         "snapshot_file": lake_snapshot, "sha256": digest(lake_bytes)})
    lake = json.loads(lake_bytes)
    declared = {x["name"]: x for x in lake["packages"]}
    declared_by_repository = {x.get("url", "").removesuffix(".git"): x for x in lake["packages"]}
    for row in deps:
        snapshot_file = row.get("snapshot_file", row.get("snapshot_path"))
        data_d = raw(snapshot_file)
        need(digest(data_d) == row["sha256"] and len(data_d) == row["bytes"],
             component + ": exact separate dependency snapshot " + row["path"])
        package = declared.get(row.get("dependency"), declared_by_repository.get(row["repository"].removesuffix(".git"), {}))
        need(package.get("rev") == row["source_commit"],
             component + ": dependency pin equals original lake-manifest " + row["path"])
        need(package.get("url", "").removesuffix(".git") == row["repository"].removesuffix(".git") and row["source_commit"] != PIN,
             component + ": dependency source kept distinct from RH pin " + row["path"])
        if manifest.get("dependency_commit"):
            need(row["source_commit"] == manifest["dependency_commit"], component + ": explicit dependency revision agrees")
        result_row = {"component": component, "path": row["path"], "snapshot_file": snapshot_file,
                      "source_commit": row["source_commit"], "sha256": digest(data_d)}
        if row.get("line_start") is not None:
            lines = data_d.splitlines(keepends=True)
            a, b = row["line_start"], row["line_end"]
            need(1 <= a <= b <= len(lines), component + ": dependency definition range valid " + row["path"])
            part = b"".join(lines[a-1:b])
            need(digest(part) == row["range_sha256"], component + ": exact dependency definition range " + row["path"])
            if row.get("range_bytes") is not None:
                need(len(part) == row["range_bytes"], component + ": exact dependency definition byte length")
            result_row.update(line_start=a, line_end=b, range_sha256=digest(part))
        dependency_files_checked.append(result_row)

# Check inherited human blocks and every explicit parent-ledger binding separately.
inherited_checked, inherited_parent_bindings = set(), []
for component, ledger in component_ledgers.items():
    own = {c["id"] for c in ledger["claims"]}
    parents = {p for c in ledger["claims"] for p in c.get("depends_on", []) if p not in own}
    inherited_sidecar = sidecars[component].get("inherited_inputs.json", {})
    inherited_records = (ledger.get("inherited_human_inputs", []) + ledger.get("inherited_inputs", [])
                         + inherited_sidecar.get("inputs", []) + inherited_sidecar.get("components", []))
    for item in inherited_records:
        filename = item.get("proof_file", item.get("file"))
        expected = item.get("proof_file_sha256", item.get("file_sha256", item.get("sha256")))
        if filename and expected:
            need(digest(raw(filename)) == expected, component + ": inherited whole proof file " + filename)
        if item.get("id") in byid:
            parents.add(item["id"])
        parents.update(item.get("claims", []))
        if item.get("exact_parent_provenance_sha256"):
            parent_file = item.get("parent_provenance_file", item["component"] + "/provenance.json")
            need(digest(raw(parent_file)) == item["exact_parent_provenance_sha256"], component + ": current inherited parent-ledger binding " + item["id"])
            inherited_parent_bindings.append({"consumer": component, "claim": item["id"], "parent": parent_file})
        if item.get("provenance_file") and item.get("provenance_sha256"):
            parent_file = item["provenance_file"]
            need(digest(raw(parent_file)) == item["provenance_sha256"],
                 component + ": exact explicit inherited parent-ledger binding " + item["id"])
            inherited_parent_bindings.append({"consumer": component, "claim": item["id"], "parent": parent_file})
        if item.get("proof_location"):
            loc = item["proof_location"]
            data_p = raw(loc["file"])
            part = b"".join(data_p.splitlines(keepends=True)[loc["line_start"]-1:loc["line_end"]])
            need(digest(part) == item.get("proof_block_sha256", loc.get("sha256")), component + ": exact inherited block " + item["id"])
            parent_loc = exact_proof_location(byid[item["id"]])
            need(all(parent_loc.get(k) == v for k, v in loc.items()), component + ": inherited proof location agrees with cumulative ledger " + item["id"])
        for binding in item.get("claim_bindings", []):
            loc_data = raw(binding["file"])
            part = b"".join(loc_data.splitlines(keepends=True)[binding["line_start"]-1:binding["line_end"]])
            need(digest(part) == binding["sha256"], component + ": explicit inherited claim binding " + binding["id"])
            need(item.get("proof_hashes", {}).get(binding["id"]) == binding["sha256"],
                 component + ": inherited hash table agrees " + binding["id"])
            parent_loc = exact_proof_location(byid[binding["id"]])
            need(parent_loc["file"] == binding["file"] and parent_loc["line_start"] == binding["line_start"]
                 and parent_loc["line_end"] == binding["line_end"],
                 component + ": inherited claim coordinates equal cumulative proof " + binding["id"])
        if not item.get("proof_location") and filename and item.get("line_start") is not None:
            data_p = raw(filename)
            a, b = item["line_start"], item["line_end"]
            part = b"".join(data_p.splitlines(keepends=True)[a-1:b])
            expected = item.get("proof_range_sha256", item.get("proof_block_sha256"))
            need(expected in {digest(part), digest(part.rstrip(b"\r\n"))},
                 component + ": exact directly recorded inherited block " + item["id"])
            parent_loc = exact_proof_location(byid[item["id"]])
            need(parent_loc["file"] == filename and parent_loc["line_start"] == a and parent_loc["line_end"] == b,
                 component + ": direct inherited range agrees with cumulative ledger " + item["id"])
    for cid in parents:
        if cid not in byid:
            need(False, component + ": inherited numbered input exists", cid)
            continue
        if cid in inherited_checked:
            continue
        claim = byid[cid]
        data_p, part = proof_bytes(claim)
        loc = exact_proof_location(claim)
        expected = loc.get("range_sha256", loc.get("sha256", loc.get("paragraph_sha256")))
        need(expected in {digest(part), digest(part.rstrip(b"\r\n"))}, cid + ": inherited proof-block integrity")
        if loc.get("file_sha256"):
            need(digest(data_p) == loc["file_sha256"], cid + ": inherited file integrity")
        inherited_checked.add(cid)

# Inspect original reviews as well as the registry summary.
registry = read("reviews_v0_57/review_registry.json")
reviewed, review_count = set(), 0
need({r["component"] for r in registry["complete_component_reviews"]} == set(cfg["components"]), "independent review registry covers all components")
for component in registry["complete_component_reviews"]:
    cname = component["component"]
    intended, seen = {c["id"] for c in component_ledgers[cname]["claims"]}, set()
    need(component["result"] == "PASS" and set(component["claims"]) == intended, cname + ": exact review coverage declaration")
    for rr in component["independent_reviews"]:
        review = read(rr["review_file"])
        review_count += 1
        need(bindings[rr["review_file"]] == rr["review_sha256"], cname + ": exact independent review bytes")
        reviewer = review["reviewer"].removeprefix("/root/")
        reviewer = "root" if reviewer == "/root" else reviewer
        need(reviewer == rr["reviewer"] and reviewer != component["author"], cname + ": reviewer independent of author")
        need(str(review.get("status", review.get("result", review.get("verdict", "")))).startswith("PASS"), cname + ": original review passes")
        need(review["source_commit"] == PIN, cname + ": review source pin")
        for key in ["unresolved_findings", "remaining_findings", "unresolved_issues", "unresolved_defects",
                    "issues", "errors", "findings", "requested_math_corrections", "required_corrections", "material_corrections_required"]:
            need(not review.get(key), cname + ": no unresolved review item in " + key)
        full = digest(raw(rr["proof_file"]))
        need(full == rr["proof_file_sha256"] == review.get("proof_file_sha256", review.get("proof_sha256", review.get("reviewed_sha256", review.get("main_sha256")))), cname + ": review binds final complete proof")
        if review.get("review_report") and review.get("report_sha256"):
            need(digest(raw(review["review_report"])) == review["report_sha256"], cname + ": review report integrity")
        elif review.get("review_file") and review.get("review_sha256"):
            report_path = review["review_file"]
            if not (ROOT / report_path).is_file():
                report_path = cname + "/" + report_path
            need(digest(raw(report_path)) == review["review_sha256"], cname + ": review narrative integrity")
        for filename, expected in review.get("input_bindings", {}).items():
            need(digest(raw(filename)) == expected,
                 cname + ": every independent-review input binding remains exact: " + filename)
        # Review schemas may retain numeric count summaries under the old
        # *_verified names. Select their actual record arrays explicitly;
        # counts never substitute for the individual hash bindings.
        def review_records(keys):
            for key in keys:
                value = review.get(key)
                if isinstance(value, list) and value and all(isinstance(x, dict) for x in value):
                    return value
            return []
        inherited_review_rows = review_records([
            "inherited_inputs_checked", "inherited_inputs_verified", "inherited_bindings", "inherited_verification"
        ])
        inherited_review_ids = {row["id"] for row in inherited_review_rows}
        inherited_manifest = sidecars[cname].get("inherited_inputs.json", {})
        inherited_declared_ids = {row["id"] for row in inherited_manifest.get("inputs", [])
                                  if row.get("id") in byid}
        inherited_declared_ids.update(cid for row in inherited_manifest.get("components", [])
                                      for cid in row.get("claims", []))
        need(inherited_declared_ids <= inherited_review_ids,
             cname + ": independent review individually binds every declared inherited proof")
        for key in ["inherited_inputs_checked", "inherited_inputs_verified"]:
            declared = review.get(key)
            if isinstance(declared, list) and all(isinstance(x, str) for x in declared):
                need(set(declared) <= inherited_review_ids,
                     cname + ": every reviewed inherited ID has its own exact hash binding")
            elif type(declared) is int:
                need(declared == len(inherited_review_rows),
                     cname + ": inherited review count equals its bound record array")
        for inherited_row in inherited_review_rows:
            cid = inherited_row["id"]
            need(cid in byid, cname + ": reviewed inherited claim exists: " + cid)
            if cid not in byid:
                continue
            loc = exact_proof_location(byid[cid])
            data_p = raw(loc["file"])
            part = b"".join(data_p.splitlines(keepends=True)[loc["line_start"]-1:loc["line_end"]])
            expected = inherited_row.get("proof_range_sha256", inherited_row.get("proof_block_sha256"))
            need(expected in {digest(part), digest(part.rstrip(b"\r\n"))},
                 cname + ": original independent review inherited block: " + cid)
            full_expected = inherited_row.get("proof_file_sha256", inherited_row.get("file_sha256"))
            if full_expected:
                need(digest(data_p) == full_expected,
                     cname + ": original independent review inherited whole file: " + cid)
            parent_expected = inherited_row.get("exact_parent_provenance_sha256",
                inherited_row.get("parent_provenance_sha256", inherited_row.get("provenance_sha256")))
            if parent_expected:
                parent_file = inherited_row.get("parent_provenance_file",
                    inherited_row.get("provenance_file", str(Path(loc["file"]).parent / "provenance.json")))
                need(digest(raw(parent_file)) == parent_expected,
                     cname + ": original independent review parent provenance: " + cid)
        reviewed_source_files = review_records(["source_files_verified", "source_files", "source_verification"])
        reviewed_source_ranges = review_records([
            "source_ranges_verified", "source_ranges", "range_verification", "source_range_verification"
        ])
        component_manifest = sidecars[cname]["source_manifest.json"]
        manifest_paths = {row["path"] for row in component_manifest.get("files", component_manifest.get("source_files", []))}
        need({row["path"] for row in reviewed_source_files} == manifest_paths,
             cname + ": independent review individually binds every source-manifest file")
        required_ranges = {(row["path"], row["line_start"], row["line_end"])
                           for row in component_manifest.get("ranges", [])}
        required_ranges.update((row["path"], row["line_start"], row["line_end"])
                               for claim in component_ledgers[cname]["claims"]
                               for row in claim.get("sources", []) if "line_start" in row)
        need(required_ranges <= {(row["path"], row["line_start"], row["line_end"])
                                 for row in reviewed_source_ranges},
             cname + ": independent review individually binds all claim and manifest source ranges")
        for key in ["source_files_verified", "source_files_checked"]:
            if type(review.get(key)) is int:
                need(review[key] == len(reviewed_source_files),
                     cname + ": source-file review count equals its exact binding array")
        for key in ["source_ranges_verified", "source_ranges_checked"]:
            if type(review.get(key)) is int:
                need(review[key] == len(reviewed_source_ranges),
                     cname + ": source-range review count equals its exact binding array")
        for source_row in reviewed_source_files:
            path = source_row["path"]
            need(path in all_component_sources and digest(all_component_sources[path]) ==
                 source_row.get("sha256", source_row.get("file_sha256")),
                 cname + ": original independent review source-file binding: " + path)
            need(source_row.get("source_commit", PIN) == PIN,
                 cname + ": original independent review source-file pin: " + path)
        for source_row in reviewed_source_ranges:
            path = source_row["path"]
            lines = all_component_sources[path].splitlines(keepends=True)
            a, b = source_row["line_start"], source_row["line_end"]
            need(1 <= a <= b <= len(lines), cname + ": original independent review range is valid: " + path)
            part = b"".join(lines[a-1:b])
            need(source_row.get("range_sha256", source_row.get("sha256")) in
                 {digest(part), digest(part.rstrip(b"\r\n"))},
                 cname + ": original independent review source-range binding: " + path)
            if source_row.get("file_sha256"):
                need(source_row["file_sha256"] == digest(all_component_sources[path]),
                     cname + ": original independent range binds the exact whole source: " + path)
        dependency_review_rows = review_records([
            "dependency_files_verified", "supporting_source_verification", "supporting_sources_verified"
        ])
        expected_dependency_rows = {x["path"]: x for x in dependency_files_checked if x["component"] == cname}
        need(set(expected_dependency_rows) <= {x["path"] for x in dependency_review_rows},
             cname + ": independent review individually binds each separate dependency source")
        for dep in dependency_review_rows:
            expected_dep = expected_dependency_rows.get(dep["path"], {})
            snapshot_file = dep.get("snapshot_file", dep.get("snapshot_path", expected_dep.get("snapshot_file")))
            need(snapshot_file and digest(raw(snapshot_file)) == dep["sha256"] == expected_dep.get("sha256"),
                 cname + ": independent review separately pinned dependency binding " + dep["path"])
            need(dep.get("source_commit") == expected_dep.get("source_commit"),
                 cname + ": independent review exact dependency revision " + dep["path"])
            if expected_dep.get("range_sha256"):
                need(all(dep.get(k) == expected_dep[k] for k in ["line_start", "line_end", "range_sha256"]),
                     cname + ": independent review exact dependency definition range " + dep["path"])
            if dep.get("original_lake_manifest_sha256"):
                need(dep.get("original_lake_manifest_source_commit") == PIN and any(
                    row["component"] == cname and row["sha256"] == dep["original_lake_manifest_sha256"]
                    for row in dependency_manifest_bindings),
                    cname + ": independent review binds the exact original dependency manifest")
        claimed = review.get("claims_reviewed", review.get("reviewed_claims", review.get("claims", review.get("blocks", []))))
        hashes = dict(review.get("proof_hashes", {}))
        if isinstance(claimed, dict):
            for cid, val in claimed.items():
                hashes[cid] = val if isinstance(val, str) else val.get("block_sha256", val.get("proof_range_sha256", val.get("sha256")))
        else:
            for val in claimed:
                if isinstance(val, str):
                    need(val in hashes, cname + ": review has explicit numbered hash " + val)
                else:
                    cid = val.get("id", val.get("claim"))
                    hashes[cid] = val.get("block_sha256", val.get("proof_range_sha256", val.get("range_sha256", val.get("sha256", val.get("proof_location", {}).get("sha256")))))
        need(hashes == rr["proof_hashes"] and set(hashes) == set(rr["claims"]), cname + ": registry exactly retains original per-block review hashes")
        for cid, expected in hashes.items():
            need(cid in intended and byid[cid]["proof_location"]["sha256"] == expected, cid + ": independent review binds exact integrated proof block")
        seen.update(hashes)
    need(seen == intended, cname + ": every numbered proof independently reviewed")
    reviewed.update(seen)
need(reviewed == {c["id"] for c in new}, "all 101 new claims covered by independent reviews")

# The whole selected graph is immutable in this release; progress is additive.
old_map = read("dependency_audit_v0_56/obligation_map.json")
new_map = read("dependency_audit_v0_57/obligation_map.json")
old_nodes = {n["id"]: n for n in old_map["nodes"]}
nodes = {n["id"]: n for n in new_map["nodes"]}
need(len(nodes) == len(new_map["nodes"]) == 121 and set(nodes) == set(old_nodes), "original 121 selected nodes retained")
need(cfg["closed_selected_leaves"] == {}, "no new whole selected leaf closure")
for cid, old_node in old_nodes.items():
    for key, value in old_node.items():
        if key == "contract" and cid in cfg.get("updated_contracts", {}):
            need(nodes[cid].get("historical_contract_narrative_v0_56") == value, cid + ": previous exact contract narrative retained")
        else:
            need(nodes[cid].get(key) == value, cid + ": original selected scope/status field retained: " + key)
logical = {k: n["requires"] for k, n in nodes.items()}
need(sum(map(len, logical.values())) == 161, "all original 161 selected edges retained")
check_dag(logical, "selected sufficient-route graph remains acyclic")
closed_statuses = {"proved_in_stated_scope", "published_application_checked", "complete", "closed"}
opens = {k for k, n in nodes.items() if n["gate"] == "LEAF" and n["status"] not in closed_statuses}
old_register = read("dependency_audit_v0_56/remaining_leaf_register.json")
register = read("dependency_audit_v0_57/remaining_leaf_register.json")
need(opens == {n["id"] for n in old_register["records"]} == {n["id"] for n in register["records"]}, "exact same 24 original whole leaves remain open")
need(all(n == nodes[n["id"]] for n in register["records"]), "current register literally agrees with current graph")
categories = dict(collections.Counter(nodes[k]["category"] for k in opens))
need(len(opens) == 24 and categories == {"C": 17, "B": 7}, "24 open leaves: 17 C and 7 B")
def reachable(start):
    seen, todo = set(), [start]
    while todo:
        node = todo.pop()
        if node not in seen:
            seen.add(node)
            todo.extend(logical[node])
    return seen
rh, grh = reachable("ORDINARY_RH"), reachable("DIRICHLET_GRH")
need(len(opens & rh & grh) == 17 and len((opens & grh) - rh) == 7 and not ((opens & rh) - grh), "17 shared and 7 additional GRH leaves, none RH-only")
need("COUNT_III_PRODUCER" not in rh and "COUNT_III_PRODUCER" in grh, "Count III remains extra GRH scope")
need(all(nodes[k]["status"] == "proved_in_stated_scope" for k in ["AD_VANISH_K_MATCH", "HOST_RIGID_S", "GLOBAL_LOCAL_GAIN"]), "all inherited selected whole closures retained")
need(all(new_map["source_inputs"].get(k) == v for k, v in old_map["source_inputs"].items()), "selected graph source-input records retained")
for key, item in new_map["source_inputs"].items():
    need(digest(raw(item["file"])) == item["sha256"], "selected graph input file binding: " + key)
for cid, progress in cfg.get("selected_node_progress", {}).items():
    need(nodes[cid].get("version_0_57_progress") == progress, cid + ": exact additive progress record")
coverage = read("dependency_audit_v0_57/route_coverage.json")
need(coverage["graph_sha256"] == bindings["dependency_audit_v0_57/obligation_map.json"], "route coverage binds current graph")
need(set(coverage["shared_open_leaf_ids"]) == opens & rh & grh and set(coverage["dirichlet_grh_only_open_leaf_ids"]) == (opens & grh) - rh, "route coverage exactly reproduces reachability")
delta = read("dependency_audit_v0_57/closure_delta.json")
need(delta["closed_selected_leaves"] == {} and delta["closed_nested_producers"] == cfg["closed_nested_producers"], "whole and nested closure records kept separate")
disposition = read("dependency_audit_v0_57/target_disposition.json")
old_disposition = read("dependency_audit_v0_56/target_disposition.json")
need(len(disposition["records"]) == len(old_disposition["records"]) == 245 and len(disposition["scope_groups"]) == 107, "245 original source dispositions and 107 scope groups retained")
need(all(all(after.get(k) == v for k, v in before.items()) for before, after in zip(old_disposition["records"], disposition["records"])), "historical disposition records retained with additive notes")
need(disposition["scope_groups"] == old_disposition["scope_groups"], "historical target scope grouping unchanged")
targets = read("next_source_targets.json")
old_targets = read("history/version_0_56/next_source_targets.json")
need(targets["targets"] == old_targets["targets"], "all original next-source targets retained literally")
checkpoint = read("continuation_checkpoint.json")
need(checkpoint["remaining_major_inputs"] == cfg["remaining_major_inputs"] and checkpoint["next_targets"] == cfg["next_targets"], "continuation checkpoint carries exact current frontier and priorities")
for key, expected in {
    "current_roadmap": "RH_GRH_reconstruction_roadmap_v0_57.txt",
    "current_progress_report": "RH_reconstruction_progress_v0_57.txt",
    "current_parallel_plan": "RH_GRH_parallel_execution_plan_v0_57.txt",
}.items():
    need(checkpoint["version_0_57_update"].get(key) == expected and (ROOT / expected).is_file(),
         "continuation checkpoint points to actual current deliverable: " + key)
need(targets["next_local_priority"] == cfg["next_targets"] and current["scope"] == cfg["status"], "current priorities and provenance scope match configuration")
expected_stats = {"new_claims": 101, "cumulative_claims": 3746, "selected_nodes": 121, "selected_edges": 161,
                  "open_count": 24, "open_categories": categories, "shared_open": 17, "extra_grh_open": 7,
                  "new_source_files_checked": len(source_data), "new_unique_source_ranges_checked": len(source_ranges)}
need(stats == expected_stats, "every integration statistic independently recomputed")
scope_updates = cfg["validation_scope_updates"]
for key, value in scope_updates.items():
    need(new_map["validation"].get(key) == value,
         "current selected graph retains the exact configured scope update: " + key)
for key in [
    "full_original_c1ch_loc_dim_fibre_ab_gen_l52_NicePrimeEx_min_hom_jac_l41_complete",
    "full_original_sharp2_and_PropagationTheoremGL2_complete",
    "rank_three_EPres_Sharp_corner_thick_chain_OffFin_and_automorphic_producers_remain",
    "full_original_FaithH_fixed_basis_nonlinear_matrix_decompletion_EtBasis_WEt_complete",
    "linear_solution_descent_and_nonlinear_conjugacy_distinguished",
    "Herr_quantitative_comparison_and_common_ConclF_remain",
    "full_actual_local_Wach_consumer_Herr_quantitative_and_common_family_remain",
    "full_original_secM_finite_and_growth_and_GSL_FINITE_GROWTH_complete",
    "section_growth_valid_in_every_characteristic_with_exact_original_section_action",
    "multiplication_invariant_descent_arbitrary_test_integrality_rank_square_inputs_remain",
    "full_original_ThmP_BiValue_BiContent_BiWindow_MtoHM_block_of_normal_form_complete",
    "actual_integral_row_window_proved_at_original_MConcl", "original_RowData_LemmaM_existence_remains",
    "full_original_KExpansionC_at_exact_universal_analytic_premises_complete",
    "absolute_majorant_proved_before_unfolding", "GLOBAL_LOCAL_GAIN_full_v49_closure_preserved",
    "no_new_whole_selected_obligation_closed",
]:
    need(scope_updates.get(key) is True and new_map["validation"].get(key) is True,
         "current configuration and graph exact scope guard: " + key)
for key in [
    "actual_dimensions_component_bounds_seed_propagation_OffFin_automorphic_inputs_remain",
    "component_chains_sharp_dimensions_EPres_seed_propagation_OffFin_remain",
    "FaithH_EtBasis_Herr_quantitative_comparison_common_ConclF_remain",
    "coherent_Wach_HW_Fon_Cmp_and_common_ConclF_remain_explicit", "full_HW_Fon_Cmp_claimed",
    "multiplication_invariant_descent_integrality_rank_growth_square_inputs_remain",
    "new_arithmetic_gap_added_to_KExpansionC", "period_identity_supplies_uniform_spectral_estimate",
    "all_layer_WachEx_claimed_unconditional",
]:
    need(scope_updates.get(key) is False and new_map["validation"].get(key) is False,
         "completed or forbidden frontier flag explicitly disabled: " + key)
for key in ["superseded_v56_arithmetic_frontier_explanation", "superseded_v56_etale_frontier_explanation",
            "superseded_v56_growth_frontier_explanation"]:
    need(bool(scope_updates.get(key)) and new_map["validation"].get(key) == scope_updates.get(key),
         "superseded v56 frontier is explicitly replaced: " + key)
need(type(scope_updates.get("remaining_period_ring_suppliers_before_original_conditional_WachEx")) is int and
     scope_updates["remaining_period_ring_suppliers_before_original_conditional_WachEx"] == 0 and
     new_map["validation"].get("remaining_period_ring_suppliers_before_original_conditional_WachEx") == 0,
     "current graph preserves zero period-ring suppliers inside the already proved original WachEx implication")

# Check both readers against component blocks and the historical proof body.
old_reader = raw("RH_readable_reconstruction_v0_56.tex").decode()
reader = raw("RH_readable_reconstruction_v0_57.tex").decode()
short = raw("RH_new_proofs_v0_57.tex").decode()
for name, body in [("cumulative", reader), ("new-proofs", short)]:
    need(not re.search(r"@(NEW|OLD|TOTAL|OPEN|SHARED|EXTRA|C|B)@", body),
         name + ": no unreplaced inventory placeholders in assembled manuscript")
old_audit = raw("dependency_audit_v0_56/main.tex").decode()
marker = re.search(r"^\\section\{[^\n]+", old_audit, re.M)[0]
end = r"\section{The arithmetic still to be written out}"
need(old_reader[old_reader.index(marker):old_reader.index(end)] == reader[reader.index(marker):reader.index(end)], "entire historical cumulative proof body preserved verbatim")
def unbreak(s):
    return re.sub(r"\\allowbreak(?:\{\})?[ \t]*", "", s)
for c in new:
    _, block = proof_bytes(c)
    pattern = r"^% BEGIN " + re.escape(c["id"]) + r"\s*\n.*?^% END " + re.escape(c["id"]) + r"[ \t]*(?:\n|$)"
    for name, body in [("cumulative", reader), ("new-proofs", short)]:
        matches = re.findall(pattern, body, re.M | re.S)
        need(len(matches) == 1 and unbreak(matches[0]) == unbreak(block.decode()), c["id"] + ": exact complete block in " + name + " edition, modulo harmless line breaks")
for name in ["v0_57_frontmatter.tex", "v0_57_audit_intro.tex", "dependency_audit_v0_57/main.tex",
             "RH_dependency_audit_v0_57.txt", "RH_reconstruction_progress_v0_57.txt",
             "RH_GRH_reconstruction_roadmap_v0_57.txt", "RH_GRH_parallel_execution_plan_v0_57.txt", "README.md"]:
    raw(name)
for name in ["RH_reconstruction_progress_v0_57.txt", "RH_GRH_reconstruction_roadmap_v0_57.txt",
             "RH_GRH_parallel_execution_plan_v0_57.txt"]:
    text_doc = raw(name).decode()
    need(all(re.search(r"\b" + re.escape(cid) + r"\b", text_doc) for cid in opens),
         name + ": every one of the 24 exact open register identifiers is present")
    need(PIN in text_doc and all(str(n) in text_doc for n in [101, 3746, 121, 161, 24]),
         name + ": current source pin and inventory are stated")
tex = read("tex_validation.json")
need(tex["artifact_version"] == "0.57" and len(tex["documents"]) == 2, "both current reader editions have draft TeX validation")
old_tex = read("history/version_0_56/tex_validation.json")
old_overfull = next(d["overfull_box_warnings"] for d in old_tex["documents"]
                    if "readable_reconstruction" in d["tex_filename"])
for item in tex["documents"]:
    need(item["tex_sha256"] == digest(raw(item["tex_filename"])), item["tex_filename"] + ": TeX report binds current edition")
    need(item["syntax_compile_succeeded"] and not item["undefined_references_or_citations"] and not item["missing_character_warnings"], item["tex_filename"] + ": draft syntax and references pass")
    need(not item["pdf_generated"] and not item["pdf_visual_review_performed"], item["tex_filename"] + ": limited validation scope stated accurately")
    need(not any("multiply defined" in w for w in item["warnings"]),
         item["tex_filename"] + ": no duplicate labels")
    need(item["overfull_box_warnings"] == 0 if "new_proofs" in item["tex_filename"]
         else item["overfull_box_warnings"] <= old_overfull,
         item["tex_filename"] + ": no new overfull-box warnings")
for path in sorted(ROOT.glob("*v0_57.py")):
    raw(str(path.relative_to(ROOT)))
raw("reviews_v0_57/write_root_reviews.py")
narrative_record = raw("reviews_v0_57/narrative_scope_review.txt").decode()
need("Status: PASS" in narrative_record, "independent narrative-scope record passes")
for expected, filename in re.findall(r"^([0-9a-f]{64})  (.+)$", narrative_record, re.M):
    need(digest(raw(filename)) == expected, "narrative review binds the current exact input: " + filename)
raw("reviews_v0_57/audit_integration_arithmetic_common_frame.py")

notes = [
    "The accepted Lean source is not re-audited for formal correctness. This independently checks exact human proof/source bytes, mathematical review bindings, preservation, scope and assembled reading editions; no Lean build or kernel replay was run.",
    "All 3645 predecessor claim records and original dependency edges remain unchanged. The historical cumulative proof body is preserved verbatim, and all 101 new numbered blocks occur exactly in both editions modulo harmless TeX line breaks.",
    "ACC completes full c1ch for the original general complete Noetherian local prime-nilradical scope, not merely a regular-local special case. It transports APD25 with N=N-prime+n*d+1, retains the coefficient-uniformizer cut, and supplies full rank-two sharp2, seedpt and PropagationTheoremGL2 at the original Ok/Big/FinLam/P1-prime/weak SeedIn premises. The seed point is fixed before every local coefficient extension. Rank-three EPres, sharp3, its triangular/corner/seed arguments, GL3 propagation, actual OffFin and ModIn/automorphic producers remain; original P, Host ell=3 and distinct rings/maps are retained.",
    "PGR completes universal original KExpansionC at the supplied arbitrary D7/HidaSetting/Full and every named analytic premise. It constructs the absolute majorant before unfolding, keeps actual measures, phases, normalization and anti-linear sharp, then proves the supplied-FinX/DimTie KTie return. It adds no arithmetic-gap specialization or hidden period-matching premise. The setting/family, FoldOK/InHH, orbital and convergence producers, remaining FinX fields and global operator/volume/spectral estimates remain independent.",
    "DJW proves the literal FormalSeriesBounds ThmP, all natural-parameter BiValue, BiContent/BiWindow, full MtoHM and block_of_normal_form. Its actual integral germ uses the t-coordinates rather than declaring the logarithm integral, and the determinant scalar is proved to be a unit. All original formal-ring, zero-size, derivative and restriction quantifiers remain. Original RowData LemmaM and the actual global Moduli/theta/section-law family remain independent; GLOBAL_LOCAL_GAIN is not reopened.",
    "SGV completes exactly the nested GSL_FINITE_GROWTH input in every characteristic and dimension zero: original SecM finiteness is returned through the actual section/scalar dictionary, and fixed positive N,d satisfy dim SecM(Nt)=d*t^g for every t>=1. Milne's explicitly identified ample-line-bundle results are the classical geometric input. This does not claim the source's general filtered polynomial-growth theorem, all-cover positive-power H1, torsion section decomposition, rank-one, integrality, square/translation or global section laws.",
    "FET supplies actual FaithH, fixed bases for the original integral lattice and rank, genuine nonlinear Frobenius conjugacy, EtBasis and every WEt functor field at their literal original premises. The coefficient scope includes p=2 and rank zero. IFD24 surjectivity is used in the p-adic conjugacy correction; IFD25 descends an already satisfying linear matrix and is not substituted for that construction. Original Good/GamS/WSer/IoS/IoW and conditional BS/LocTied are retained; Herr, quantitative comparison and common HW/Fon/Cmp/ConclF remain independent.",
    "No new whole selected leaf closes. All 121 selected nodes, 161 edges and original whole statuses remain. The 24 open obligations split into 17 class C and seven class B; separately, they split into 17 shared RH/Dirichlet-GRH and seven extra Dirichlet-GRH. These are different partitions, and claim or leaf counts are not completion percentages.",
]


result = {
    "schema": "rh-independent-integration-review/1", "artifact_version": "0.57", "date": "2026-11-24",
    "reviewer": "/root/arithmetic_common_frame", "reviewer_name": "arithmetic_common_frame", "source_commit": PIN,
    "status": ("PRELIMINARY_PASS" if args.preflight else "PASS") if not errors else "FAIL", "errors": errors,
    "scope": "Independent baseline preservation, numbered proof/source ranges, inherited human-block integrity, mathematical-review coverage, selected-route scope and assembled-reader audit; no Lean replay.",
    "statistics": stats, "exact_whole_closures": {}, "baseline_claims_preserved": len(old_claims),
    "baseline_source_files_preserved": len(base["source_files"]),
    "baseline_manifest_artifacts_preserved": preserved, "baseline_artifacts_retained_in_history": archived,
    "baseline_displaced_artifacts": archived_paths,
    "all_new_claims_reviewed": len(reviewed), "independent_review_file_count": review_count,
    "new_proof_files": proof_files,
    "component_ledgers": {c: {"claims": len(d["claims"]), "ledger_sha256": bindings[c + "/provenance.json"]} for c, d in component_ledgers.items()},
    "inherited_numbered_blocks_checked": sorted(inherited_checked),
    "legacy_anchor_locations_verified_without_ledger_mutation": anchor_locations,
    "inherited_parent_provenance_bindings_checked": inherited_parent_bindings,
    "all_component_manifest_source_files_checked": len(all_component_sources),
    "all_component_manifest_source_ranges_checked": len(component_manifest_ranges),
    "separately_pinned_dependency_files_checked": dependency_files_checked,
    "original_dependency_manifest_bindings_checked": dependency_manifest_bindings,
    "separately_identified_reference_snapshots_checked": nonformal_snapshots_checked,
    "passed_check_count": len(checks), "notes": notes,
    "input_bindings": dict(sorted(bindings.items())),
}
out = ROOT / ("reviews_v0_57/preflight_arithmetic_common_frame.json" if args.preflight else "reviews_v0_57/integration_arithmetic_common_frame.json")
out.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n")
print(json.dumps({k: result[k] for k in ["status", "errors", "statistics", "baseline_manifest_artifacts_preserved", "baseline_artifacts_retained_in_history", "passed_check_count"]}, ensure_ascii=False, indent=2))
raise SystemExit(bool(errors))
