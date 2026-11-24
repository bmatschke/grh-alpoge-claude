#!/usr/bin/env python3
"""Independent v0.56 preservation, proof/source binding and exact-scope audit.

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
OLD = ROOT / "history/version_0_55"
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
cfg = read("increment_v0_56.json")
stats = read("integration_stats_v0_56.json")
base = read("history/version_0_55/provenance.json")
current = read("provenance.json")
old_index = read("history/version_0_55/source_index.json")
index = read("source_index.json")
record = read("history/version_0_55/baseline_record.json")
need(digest(BASELINE.read_bytes()) == record.get("archive_sha256", record.get("sha256")), "original supplied archive SHA256")
need(record.get("source_commit", PIN) == cfg["source_commit"] == PIN, "baseline and current source pin agree")
need(PIN.encode() in raw("history/version_0_55/README.md"), "frozen baseline readme declares the exact accepted source pin")

# Check preservation against the supplied archive as well as its own manifest.
manifest = raw("history/version_0_55/SHA256SUMS").decode()
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
need(len(entries) == 8647, "baseline contains exactly 8647 manifest artifacts")
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
    for rel in ["RH_GRH_reconstruction_roadmap_v0_55.txt",
                "RH_GRH_parallel_execution_plan_v0_55.txt"]:
        need(prefix + rel in names and raw("history/version_0_55/" + rel) == archive.read(prefix + rel),
             "frozen predecessor planning file equals supplied archive: " + rel)

old_claims, claims = base["claims"], current["claims"]
need(len(old_claims) == 3538, "baseline contains exactly 3538 numbered claims")
need(claims[:3538] == old_claims, "all 3538 original claim objects retained literally")
need(current["source_files"][:len(base["source_files"])] == base["source_files"], "original provenance source inventory retained literally")
need(index["source_files"][:len(old_index["source_files"])] == old_index["source_files"], "original source-index prefix retained literally")
new = claims[3538:]
need(len(new) == 107 and len(claims) == 3645, "107 new claims and 3645 cumulative claims")
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
    "polarized_base_change_v56": 27,
    "arithmetic_presentations_v56": 25,
    "reference_covolume_v56": 25,
    "wach_prism_v56": 30,
}
need(set(cfg["components"]) == set(expected_counts), "exact four independently reviewed components")
component_ledgers, sidecars, incoming = {}, {}, []
for component in cfg["components"]:
    ledger = read(component + "/provenance.json")
    component_ledgers[component] = ledger
    incoming.extend(ledger["claims"])
    need(len(ledger["claims"]) == expected_counts[component], component + ": expected claim count")
    need(ledger.get("source_commit", PIN) == PIN, component + ": source pin")
    scope = {k: v for k, v in ledger.items() if k not in {"claims", "source_files", "source_inventory", "source_groups"}}
    need(current["component_scope_metadata_as_received_v0_56"].get(component) == scope,
         component + ": full finalized metadata and original premises retained")
    sidecars[component] = {}
    for filename in ["contracts.json", "closure.json", "original_contracts.json", "retained_foundations.json",
                     "classical_inputs.json", "published_inputs.json", "explicit_inputs.json", "claim_dag.json", "source_manifest.json", "tex_validation.json", "inherited_inputs.json"]:
        if (ROOT / component / filename).is_file():
            sidecars[component][filename] = read(component + "/" + filename)
    for filename in ["report.txt", "independent_review.md", "next_source_handoff.txt"]:
        if (ROOT / component / filename).is_file():
            raw(component + "/" + filename)
    artifact_hashes = read(component + "/hashes.json")
    artifact_hashes = artifact_hashes.get("hashes", artifact_hashes)
    for filename, expected in artifact_hashes.items():
        need(digest(raw(component + "/" + filename)) == expected, component + ": finalized artifact manifest " + filename)
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
        for key in ["whole_obligations_closed", "whole_obligation_closures", "new_global_frontier_leaf_closures",
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

# Completed original suppliers are distinguished from their larger consumers.
# These independently selected guards test exact mathematical scope.
pbc = sidecars["polarized_base_change_v56"]["contracts.json"]
pbc_cl = sidecars["polarized_base_change_v56"]["closure.json"]
for key in [
    "full_original_sc_extend_supplied", "full_original_exists_one_add_kill_supplied",
    "full_original_extra_section_supplied", "full_original_glue_pack_supplied",
    "full_original_exists_sv_supplied", "full_original_relAmple_of_locally_supplied",
    "full_original_relAmple_pull_supplied", "full_original_kTriv_pull_supplied",
    "full_original_PolBaseChangeSt_supplied", "full_original_polAV_veryAmpleBy_supplied",
    "full_original_actual_section_finiteness_supplied", "full_original_integer_power_SecM_finiteness_supplied",
    "arbitrary_base_and_target_preserved", "original_actual_bundle_and_cartesian_square_preserved",
    "original_all_test_quantifiers_preserved", "no_new_noetherianity_or_flatness_hypothesis",
]:
    need(pbc.get(key) is True and pbc_cl.get(key) is True,
         "PBC completed original supplier or preserved quantifier: " + key)
for key in ["full_original_two_sided_section_growth_supplied",
            "global_positive_power_abelian_vanishing_unconditionally_supplied",
            "global_section_laws_unconditionally_supplied", "global_Moduli_supplied"]:
    need(pbc.get(key) is False and pbc_cl.get(key) is False,
         "PBC retains the independent downstream geometric producer: " + key)
need({x["id"] for x in pbc["formerly_retained_producers_now_supplied"]} == {"GSL_POL_BASE_CHANGE"},
     "PBC discharges exactly the formerly retained GSL_POL_BASE_CHANGE input")
need(set(pbc_cl["pending_actual_geometric_producers"]) == {
    "GSL_VANISH_CLOSED", "GSL_RANK_CLOSED", "GSL_TWIST_GEOMETRIC",
    "GSL_MUL_PULL", "GSL_MUL_GEOMETRY", "GSL_TORSION_DESCENT", "GSL_GEOM_INTEGRAL",
    "GSL_RANK_ONE", "GSL_SECTION_DECOMP", "GSL_FINITE_GROWTH", "GSL_SQUARE",
    "GSL_INHERITED_NFL", "GSL_INHERITED_TDR",
}, "PBC preserves every independent vanishing/rank/growth/square and inherited geometry input")
need(set(pbc_cl["completed_original_endpoint_claim_ids"]) == {
    "PBC3", "PBC5", "PBC6", "PBC7", "PBC9", "PBC12", "PBC13", "PBC14", "PBC15", "PBC16",
    "PBC17", "PBC18", "PBC19", "PBC20", "PBC21", "PBC22", "PBC23", "PBC24", "PBC25", "PBC26", "PBC27"
}, "PBC records every complete original endpoint including the actual finiteness return")

apd = sidecars["arithmetic_presentations_v56"]["contracts.json"]
apd_cl = sidecars["arithmetic_presentations_v56"]["closure.json"]
for key in [
    "full_original_pres_supplied", "full_pres_supplied", "actual_local_deformation_presentation_supplied",
    "exact_N_equals_Nprime_plus_n_d_plus_one", "full_original_pr_mazur_supplied", "full_original_pr_count_supplied",
    "full_original_point_loc_supplied", "full_original_alg_supplied", "full_original_ext_A_supplied",
    "full_original_def_iso_supplied", "actual_local_NRep_Univ_supplied", "actual_original_HasObs_supplied",
    "actual_tangent_surjectivity_supplied", "actual_small_extension_corrections_supplied",
    "all_original_HasObs_quotients_preserved", "broad_IsBar_scope_preserved",
    "finite_Laurent_polynomial_evaluation_only", "finite_residue_compactness_only_at_original_alg_scope",
    "general_local_O_scope_of_deformation_lemmas_preserved", "same_A_B_x_Oprime_R_iota_preserved",
    "same_g1", "original_universal_Space_and_Loc_remain_antecedents", "upstream_FinA_not_assumed",
    "original_P_retained_at_arithmetic_entry", "host_ell_3_allowed",
    "rank_two_and_rank_three_rings_and_ideals_kept_distinct",
]:
    need(apd.get(key) is True, "APD completed supplier or preserved original scope: " + key)
for key in [
    "full_original_general_alg_limit_supplied", "full_original_general_alg_closed_supplied",
    "full_original_obs_pres_supplied", "new_opaque_presentation_or_obstruction_premise_added",
    "point_loc_or_def_iso_imported_as_human_proof", "full_original_c1ch_supplied", "full_original_EPres_supplied",
    "full_sharp2_supplied", "full_sharp3_supplied", "actual_dimensions_density_and_seed_incidence_supplied",
    "full_PropagationTheoremGL2_supplied", "full_PropagationTheoremGL3_supplied",
    "actual_OffFin_producer_supplied", "actual_automorphic_or_Alt_producer_supplied",
    "full_GdEnd_supplied", "full_HostEnd_supplied", "selected_producer_closed",
]:
    need(apd.get(key) is False, "APD independent downstream producer or forbidden shortcut remains: " + key)
for key in ["full_original_pres_closed", "actual_point_loc_and_def_iso_closed",
            "actual_tangent_and_obstruction_suppliers_closed"]:
    need(apd_cl.get(key) is True, "APD closure records the actual completed original supplier: " + key)
for key in ["full_c1ch_remains_open", "full_EPres_remains_open",
            "actual_dimensions_density_and_seed_incidence_remain_open",
            "full_PropagationTheoremGL2_remains_open", "full_PropagationTheoremGL3_remains_open",
            "actual_OffFin_producer_remains_open", "full_GdEnd_remains_open", "full_HostEnd_remains_open",
            "actual_Alt_producers_remain_open", "original_P_retained",
            "separate_rank_rings_and_coefficient_extensions_preserved"]:
    need(apd_cl.get(key) is True, "APD exact remaining producer or retained original data: " + key)
ae = {x["id"]: x["claim"] for x in apd["closed_subcontracts"]}
for name, claim in {
    "full_original_pr_tan": "APD1", "full_original_pr_mazur": "APD5", "full_original_pr_count": "APD6",
    "full_original_point_loc": "APD10", "full_original_ext_A": "APD11", "full_original_def_iso": "APD12",
    "actual_local_NRep_Univ": "APD12", "actual_original_HasObs": "APD18",
    "full_original_pr_dual": "APD23", "actual_tangent_obstruction_excess": "APD24",
    "full_original_pres": "APD25",
}.items():
    need(ae.get(name) == claim, "APD exact completed source endpoint: " + name)

rcv = sidecars["reference_covolume_v56"]["contracts.json"]
rcv_cl = sidecars["reference_covolume_v56"]["closure.json"]
need(rcv.get("primary_endpoint_claim") == rcv.get("endpoint_claim") == "RCV25",
     "RCV records the complete original reference-covolume endpoint")
need(rcv.get("remaining_exact_producers_for_CovolRef") == [] and
     rcv_cl.get("remaining_source_producers_inside_CovolRef") == [],
     "RCV has no stale retained supplier inside its completed CovolRef chain")
for name in ["TrDetUnimod", "RowBlockCovol", "BlockCovol", "unipotent_conj_mem_level", "NOratC",
             "DictGram", "DictEx", "DictPlace", "DictLat", "FibQ", "FibOnto", "NOfib",
             "KapSurj", "CoordMeas", "KapLaw", "CoordCovol", "CoordHaar", "CovolN",
             "ConstStep", "ShearStep", "ExpChart", "refN_map_kapL", "refNg_isHaarLoc",
             "FrameRow", "RefNBox", "refNX_haar", "covol_refN", "CovolRef"]:
    need(any(name in x for x in rcv["completed_original_substatements"]),
         "RCV records the exact completed original substatement: " + name)
need(any("D7" in x and "HidaSetting" in x and "HypX" in x for x in rcv["retained_original_premises"]),
     "RCV retains original supplied D7/HidaSetting and exact final HypX scope")
need(any("Reference word u" in x and "independent" in x for x in rcv["shared_data_preserved"]) and
     any("haarLie(Nset,1)" in x for x in rcv["shared_data_preserved"]) and
     any("Every original weak Haar" in x for x in rcv["shared_data_preserved"]),
     "RCV preserves the literal reference measure, independent words and every original Haar/domain")
for token in ["JacGauge", "RhsWLim", "PlaceSplit", "ProdExact", "RealBracket", "Forms0", "Transport/LevelMatch"]:
    need(any(token in x for x in rcv["remaining_downstream_boundaries"]),
         "RCV retains the independent downstream producer: " + token)

wpr = sidecars["wach_prism_v56"]["contracts.json"]
wpr_cl = sidecars["wach_prism_v56"]["closure.json"]
we = {x["endpoint"]: x for x in wpr["completed_source_endpoints"]}
for name, claim in {
    "GlobalTheory.Cyc.exists_integral_cyclotomicChar": "WPR2",
    "GlobalTheory.T.cyclotomicPowerSeriesAlgHom_action_laws": "WPR3",
    "GlobalTheory.PrismS.ker_eq_span": "WPR8", "GlobalTheory.PrismS.isAdicComplete_span": "WPR9",
    "GlobalTheory.PrismS.IoDescent.exists_retraction": "WPR11",
    "GlobalTheory.PrismS.IoDescent.exists_factor": "WPR12",
    "GlobalTheory.T.exists_wachInclusion_powerSeries_into_one_tmul_ainf": "WPR15",
    "GlobalTheory.Prism.ainfObj / ainfHom": "WPR19",
    "GlobalTheory.PrismSplit.existsUnique_of_separated": "WPR25",
    "GlobalTheory.T.existsUnique_unramifiedIntegers_coords_basis": "WPR26",
    "GlobalTheory.PrismS.exists_prism": "WPR29",
    "GlobalTheory.T.exists_wach_prism_over_integers": "WPR29",
    "GlobalTheory.WachLattice.main": "WPR30",
}.items():
    need(we.get(name, {}).get("claim") == claim and we.get(name, {}).get("all_original_premises_retained") is True,
         "WPR supplies the full original endpoint: " + name)
need(set(wpr["original_WachEx_premises_retained"]) == {"BhattScholzeCrystallineLattices", "LocTied"} and
     wpr.get("conditional_reduction_extra_inputs") == {},
     "WPR retains exactly original conditional WachEx hypotheses and adds no new period-ring premise")
for key in ["all_sixteen_original_prism_fields", "same_actual_period_rings_and_maps",
            "both_coefficient_coordinates_all_original_bases", "no_extra_continuity_noetherian_or_interlayer_assumptions"]:
    need(wpr.get(key) is True, "WPR full original scope or proved simplification: " + key)
for key in ["full_original_Wach_prism_complete", "full_original_conditional_WachEx_complete",
            "original_BS_and_LocTied_retained"]:
    need(wpr_cl.get(key) is True, "WPR exact completed original frontier: " + key)
need(type(wpr_cl.get("remaining_period_ring_suppliers_before_original_conditional_WachEx")) is int and
     wpr_cl["remaining_period_ring_suppliers_before_original_conditional_WachEx"] == 0,
     "WPR leaves no stale period-ring supplier inside the completed original WachEx implication")
for key in ["unconditional_original_all_layer_WachEx_complete", "full_HW_Fon_Cmp_complete",
            "full_GLOBAL_DENOMINATOR_supplier_supplied"]:
    need(wpr_cl.get(key) is False, "WPR leaves the original independent downstream boundary explicit: " + key)
for token in ["FaithH", "EtBasis", "Herr", "HW/Fon/Cmp", "ConclF", "GLOBAL_DENOMINATOR"]:
    need(any(token in x for x in wpr["remaining"]), "WPR retains the independent original consumer: " + token)

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
            need(raw("source_snapshot_v0_56/" + path) == data_s, "aggregate source snapshot exact: " + path)
        data_s = source_data[path]
        need(digest(data_s) == src.get("file_sha256", src.get("full_file_sha256", src.get("sha256"))), cid + ": full source hash " + path)
        lines = data_s.splitlines(keepends=True)
        a, b = src["line_start"], src["line_end"]
        need(1 <= a <= b <= len(lines) and digest(b"".join(lines[a-1:b])) == src["range_sha256"],
             cid + ": exact source range " + path + ":" + str(a) + "-" + str(b))
        source_ranges.add((path, a, b))
        if src.get("snapshot_file"):
            need(raw(src["snapshot_file"]) == data_s, cid + ": original component snapshot exact")
snapshot = read("source_snapshot_v0_56/manifest.json")
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
dependency_files_checked = []
for component in cfg["components"]:
    manifest = sidecars[component]["source_manifest.json"]
    deps = manifest.get("dependency_files", [])
    if not deps:
        continue
    lake = json.loads(all_component_sources["lake-manifest.json"])
    declared = {x["name"]: x["rev"] for x in lake["packages"]}
    for row in deps:
        data_d = raw(row["snapshot_file"])
        need(digest(data_d) == row["sha256"] and len(data_d) == row["bytes"],
             component + ": exact separate dependency snapshot " + row["path"])
        need(declared.get(row["dependency"]) == row["source_commit"] == manifest["dependency_commit"],
             component + ": dependency pin equals original lake-manifest " + row["path"])
        need(row["repository"] == manifest["dependency_repository"] and row["source_commit"] != PIN,
             component + ": dependency source kept distinct from RH pin " + row["path"])
        dependency_files_checked.append({"component": component, "path": row["path"],
                                        "source_commit": row["source_commit"], "sha256": digest(data_d)})

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
            parent_file = item["component"] + "/provenance.json"
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
registry = read("reviews_v0_56/review_registry.json")
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
        for dep in review.get("dependency_files_verified", []):
            need(digest(raw(dep["snapshot_file"])) == dep["sha256"] and
                 any(x["path"] == dep["path"] and x["sha256"] == dep["sha256"] for x in dependency_files_checked),
                 cname + ": independent review separately pinned dependency binding " + dep["path"])
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
need(reviewed == {c["id"] for c in new}, "all 107 new claims covered by independent reviews")

# The whole selected graph is immutable in this release; progress is additive.
old_map = read("dependency_audit_v0_55/obligation_map.json")
new_map = read("dependency_audit_v0_56/obligation_map.json")
old_nodes = {n["id"]: n for n in old_map["nodes"]}
nodes = {n["id"]: n for n in new_map["nodes"]}
need(len(nodes) == len(new_map["nodes"]) == 121 and set(nodes) == set(old_nodes), "original 121 selected nodes retained")
need(cfg["closed_selected_leaves"] == {}, "no new whole selected leaf closure")
for cid, old_node in old_nodes.items():
    for key, value in old_node.items():
        if key == "contract" and cid in cfg.get("updated_contracts", {}):
            need(nodes[cid].get("historical_contract_narrative_v0_55") == value, cid + ": previous exact contract narrative retained")
        else:
            need(nodes[cid].get(key) == value, cid + ": original selected scope/status field retained: " + key)
logical = {k: n["requires"] for k, n in nodes.items()}
need(sum(map(len, logical.values())) == 161, "all original 161 selected edges retained")
check_dag(logical, "selected sufficient-route graph remains acyclic")
closed_statuses = {"proved_in_stated_scope", "published_application_checked", "complete", "closed"}
opens = {k for k, n in nodes.items() if n["gate"] == "LEAF" and n["status"] not in closed_statuses}
old_register = read("dependency_audit_v0_55/remaining_leaf_register.json")
register = read("dependency_audit_v0_56/remaining_leaf_register.json")
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
    need(nodes[cid].get("version_0_56_progress") == progress, cid + ": exact additive progress record")
coverage = read("dependency_audit_v0_56/route_coverage.json")
need(coverage["graph_sha256"] == bindings["dependency_audit_v0_56/obligation_map.json"], "route coverage binds current graph")
need(set(coverage["shared_open_leaf_ids"]) == opens & rh & grh and set(coverage["dirichlet_grh_only_open_leaf_ids"]) == (opens & grh) - rh, "route coverage exactly reproduces reachability")
delta = read("dependency_audit_v0_56/closure_delta.json")
need(delta["closed_selected_leaves"] == {} and delta["closed_nested_producers"] == cfg["closed_nested_producers"], "whole and nested closure records kept separate")
disposition = read("dependency_audit_v0_56/target_disposition.json")
old_disposition = read("dependency_audit_v0_55/target_disposition.json")
need(len(disposition["records"]) == len(old_disposition["records"]) == 245 and len(disposition["scope_groups"]) == 107, "245 original source dispositions and 107 scope groups retained")
need(all(all(after.get(k) == v for k, v in before.items()) for before, after in zip(old_disposition["records"], disposition["records"])), "historical disposition records retained with additive notes")
need(disposition["scope_groups"] == old_disposition["scope_groups"], "historical target scope grouping unchanged")
targets = read("next_source_targets.json")
old_targets = read("history/version_0_55/next_source_targets.json")
need(targets["targets"] == old_targets["targets"], "all original next-source targets retained literally")
checkpoint = read("continuation_checkpoint.json")
need(checkpoint["remaining_major_inputs"] == cfg["remaining_major_inputs"] and checkpoint["next_targets"] == cfg["next_targets"], "continuation checkpoint carries exact current frontier and priorities")
for key, expected in {
    "current_roadmap": "RH_GRH_reconstruction_roadmap_v0_56.txt",
    "current_progress_report": "RH_reconstruction_progress_v0_56.txt",
    "current_parallel_plan": "RH_GRH_parallel_execution_plan_v0_56.txt",
}.items():
    need(checkpoint["version_0_56_update"].get(key) == expected and (ROOT / expected).is_file(),
         "continuation checkpoint points to actual current deliverable: " + key)
need(targets["next_local_priority"] == cfg["next_targets"] and current["scope"] == cfg["status"], "current priorities and provenance scope match configuration")
expected_stats = {"new_claims": 107, "cumulative_claims": 3645, "selected_nodes": 121, "selected_edges": 161,
                  "open_count": 24, "open_categories": categories, "shared_open": 17, "extra_grh_open": 7,
                  "new_source_files_checked": len(source_data), "new_unique_source_ranges_checked": len(source_ranges)}
need(stats == expected_stats, "every integration statistic independently recomputed")
scope_updates = cfg["validation_scope_updates"]
for key in [
    "full_original_both_Serre_very_ample_conjuncts_complete",
    "full_original_all_cover_H1_and_actual_high_power_polynomial_complete",
    "full_original_loc_cpl_LocFlat_types_LocRho_and_loc_ex_complete",
    "actual_dimensions_component_bounds_seed_propagation_OffFin_automorphic_inputs_remain",
    "full_original_VolStabFromSWS_complete_at_exact_retained_premises",
    "full_original_InVolumesAt_and_actual_GMR19_InVolumes_join_complete",
    "stabilizer_finite_mass_derived_before_real_scalar_cancellation",
    "any_original_IsOmT_and_all_domain_witnesses_preserved",
    "RealBracket_retained_Siegel_Weil_density_finite_place_and_transport_counting_remain",
    "full_original_inhomogeneous_invariant_Frobenius_matrix_descent_complete",
    "full_original_generic_additive_and_matrix_bijectivity_complete",
    "full_original_invariant_tilt_approximation_and_near_closedness_complete",
    "original_LocTied_IsStd_and_Bhatt_Scholze_inputs_retained",
    "coherent_Wach_HW_Fon_Cmp_and_common_ConclF_remain_explicit",
    "GLOBAL_LOCAL_GAIN_full_v49_closure_preserved", "no_new_whole_selected_obligation_closed",
    "full_original_arbitrary_base_RelAmpleOfLocallyOnBase_complete",
    "full_original_PolBaseChangeSt_and_polAV_veryAmpleBy_complete",
    "full_original_sections_finite_of_perf_and_all_integer_power_SecM_finiteness_complete",
    "multiplication_invariant_descent_integrality_rank_growth_square_inputs_remain",
    "full_original_point_loc_ext_A_def_iso_and_NRep_Univ_complete",
    "full_original_HasObs_and_pres_exact_variable_relation_count_complete",
    "component_chains_sharp_dimensions_EPres_seed_propagation_OffFin_remain",
    "full_original_CovolRef_all_words_domains_and_reference_measures_complete",
    "full_original_reference_Lie_normalization_and_FrameRow_complete",
    "JacGauge_PlaceSplit_ProdExact_RealBracket_remain",
    "full_original_Wach_prism_all_sixteen_fields_complete",
    "full_original_conditional_WachEx_complete",
    "FaithH_EtBasis_Herr_quantitative_comparison_common_ConclF_remain",
]:
    need(scope_updates.get(key) is True and new_map["validation"].get(key) is True,
         "current configuration and graph scope guard: " + key)
for key in [
    "independent_PolBaseChange_Serre_all_cover_H1_integrality_rank_square_inputs_remain",
    "PolBaseChange_multiplication_invariant_descent_integrality_rank_square_inputs_remain",
    "actual_LocFlat_LocRho_dimension_seed_propagation_OffFin_automorphic_inputs_remain",
    "RealBracket_arithmetic_quotient_volumes_finite_place_and_transport_counting_remain",
    "reference_unipotent_covolume_discriminant_supplier_remains",
    "two_exact_period_ring_suppliers_before_full_WachEx_remain_explicit",
    "one_exact_period_ring_supplier_before_conditional_WachEx_remains_explicit",
    "all_layer_WachEx_claimed_unconditional",
]:
    need(scope_updates.get(key) is False and new_map["validation"].get(key) is False,
         "completed or forbidden frontier flag explicitly disabled: " + key)
for key in [
    "actual_section_localization_gluing_and_affine_geometric_suppliers_remain_explicit",
    "three_exact_period_ring_suppliers_before_full_WachEx_remain_explicit",
    "actual_geometric_section_model_PolBaseChange_Serre_integrality_rank_square_suppliers_remain_explicit",
]:
    need(new_map["validation"].get(key) is False,
         "earlier retired frontier flag stays disabled: " + key)
for key in [
    "superseded_v54_Serre_remaining_flag_explanation", "superseded_v54_local_chart_remaining_flag_explanation",
    "superseded_v54_arithmetic_quotient_volume_flag_explanation", "superseded_v54_two_period_suppliers_explanation",
    "superseded_v55_PolBaseChange_remaining_flag_explanation", "superseded_v55_one_period_supplier_explanation",
]:
    need(bool(scope_updates.get(key)) and new_map["validation"].get(key) == scope_updates.get(key),
         "superseded frontier scope is explained explicitly: " + key)
need(type(scope_updates.get("remaining_period_ring_suppliers_before_original_conditional_WachEx")) is int and
     scope_updates["remaining_period_ring_suppliers_before_original_conditional_WachEx"] == 0 and
     new_map["validation"].get("remaining_period_ring_suppliers_before_original_conditional_WachEx") == 0,
     "current graph records zero period-ring suppliers inside original conditional WachEx")

# Check both readers against component blocks and the historical proof body.
old_reader = raw("RH_readable_reconstruction_v0_55.tex").decode()
reader = raw("RH_readable_reconstruction_v0_56.tex").decode()
short = raw("RH_new_proofs_v0_56.tex").decode()
for name, body in [("cumulative", reader), ("new-proofs", short)]:
    need(not re.search(r"@(NEW|OLD|TOTAL|OPEN|SHARED|EXTRA|C|B)@", body),
         name + ": no unreplaced inventory placeholders in assembled manuscript")
old_audit = raw("dependency_audit_v0_55/main.tex").decode()
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
for name in ["v0_56_frontmatter.tex", "v0_56_audit_intro.tex", "dependency_audit_v0_56/main.tex",
             "RH_dependency_audit_v0_56.txt", "RH_reconstruction_progress_v0_56.txt",
             "RH_GRH_reconstruction_roadmap_v0_56.txt", "RH_GRH_parallel_execution_plan_v0_56.txt", "README.md"]:
    raw(name)
for name in ["RH_reconstruction_progress_v0_56.txt", "RH_GRH_reconstruction_roadmap_v0_56.txt",
             "RH_GRH_parallel_execution_plan_v0_56.txt"]:
    text_doc = raw(name).decode()
    need(all(re.search(r"\b" + re.escape(cid) + r"\b", text_doc) for cid in opens),
         name + ": every one of the 24 exact open register identifiers is present")
    need(PIN in text_doc and all(str(n) in text_doc for n in [107, 3645, 121, 161, 24]),
         name + ": current source pin and inventory are stated")
tex = read("tex_validation.json")
need(tex["artifact_version"] == "0.56" and len(tex["documents"]) == 2, "both current reader editions have draft TeX validation")
old_tex = read("history/version_0_55/tex_validation.json")
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
for path in sorted(ROOT.glob("*v0_56.py")):
    raw(str(path.relative_to(ROOT)))
raw("reviews_v0_56/narrative_scope_review.txt")
raw("reviews_v0_56/audit_integration_geometry_alltest.py")

notes = [
    "The accepted Lean source is not re-audited for formal correctness. This checks exact human proof/source bytes, independent reviews, preservation, mathematical scope and assembled reading editions; no Lean build or kernel replay was run.",
    "All 3538 predecessor claim records and original dependency edges remain unchanged. The entire historical cumulative proof body is preserved verbatim, and all 107 new numbered blocks appear exactly in both editions modulo harmless TeX line breaks.",
    "PBC proves full arbitrary-base relative ampleness and literal polarized base change, with the actual Cartesian square, line bundle, rigidification/symmetry, unchanged dimension and every original affine test for KTriv. The synchronized gluing proof adds no Noetherian or flatness hypothesis. PBC26 supplies the original very-ample producer. PBC27 proves the Perf finite-relation lemma over every field, then original polarized section finiteness and every integer-power SecM at their original algebraically closed-field scopes; the separate arbitrary-field finite_secM implication retains its relation premise. GSL_POL_BASE_CHANGE is supplied; positive-power vanishing, multiplication/torsion descent, integrality/rank, two-sided growth, square/translation and original Moduli remain.",
    "APD proves full original point_loc, ext_A, def_iso and actual NRep.Univ, then the complete actual HasObs and local presentation pres with N=N-prime+n*d+1. Every original small-extension quotient and both ranks are retained, without Big or nontriangularity. Universal Space/Loc remain antecedents; c1ch/component chains, sharp dimensions, separate EPres, density/seeds, propagation, OffFin and automorphic/Alt suppliers remain. Same g1, Host ell=3, original P and distinct coefficient extensions remain explicit.",
    "RCV proves full CovolRef with the actual unipotent arithmetic lattice, trace determinant and exact reference Lie measure. Both reference and lattice words remain independent and all original domain/Haar witnesses are kept. JacGauge, PlaceSplit, ProdExact and RealBracket remain independent, along with Forms0, finite-place/counting/transport and final spectral producers. No new global character or infinity normalization is inferred from the reference calculation.",
    "WPR proves the prescribed Wach prism with all sixteen original fields, both coordinate decompositions and literal scalar map. The algebraic tensor factorization and tail-operator division introduce no continuity or Noetherian hypothesis. WPR30 completes the original BS plus LocTied implication to WachEx, using WIS18, IFD25 and WLD26. No period-ring supplier remains inside that implication. The original realization and tied-period premises, FaithH/EtBasis/Herr/quantitative comparison and common ConclF remain explicit.",
    "No new whole selected leaf closes. All 121 selected nodes, 161 edges and original whole statuses remain. Exactly 24 whole obligations remain: 17 shared RH/Dirichlet-GRH and seven extra Dirichlet-GRH; inventory counts are not completion percentages.",
]


result = {
    "schema": "rh-independent-integration-review/1", "artifact_version": "0.56", "date": "2026-11-24",
    "reviewer": "/root/geometry_alltest", "reviewer_name": "geometry_alltest", "source_commit": PIN,
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
    "passed_check_count": len(checks), "notes": notes,
    "input_bindings": dict(sorted(bindings.items())),
}
out = ROOT / ("reviews_v0_56/preflight_geometry_alltest.json" if args.preflight else "reviews_v0_56/integration_geometry_alltest.json")
out.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n")
print(json.dumps({k: result[k] for k in ["status", "errors", "statistics", "baseline_manifest_artifacts_preserved", "baseline_artifacts_retained_in_history", "passed_check_count"]}, ensure_ascii=False, indent=2))
raise SystemExit(bool(errors))
