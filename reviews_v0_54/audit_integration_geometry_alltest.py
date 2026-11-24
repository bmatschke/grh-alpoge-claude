#!/usr/bin/env python3
"""Independent v0.54 preservation, proof/source binding and exact-scope audit.

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
OLD = ROOT / "history/version_0_53"
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
    data = path.read_bytes()
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


def proof_bytes(claim):
    loc = claim["proof_location"]
    data = raw(loc["file"])
    lines = data.splitlines(keepends=True)
    a, b = loc["line_start"], loc["line_end"]
    need(1 <= a <= b <= len(lines), claim["id"] + ": valid proof line range")
    return data, b"".join(lines[a-1:b])


need(subprocess.check_output(["git", "-C", str(SOURCE), "rev-parse", "HEAD"], text=True).strip() == PIN,
     "read-only source checkout has the exact accepted pin")
cfg = read("increment_v0_54.json")
stats = read("integration_stats_v0_54.json")
base = read("history/version_0_53/provenance.json")
current = read("provenance.json")
old_index = read("history/version_0_53/source_index.json")
index = read("source_index.json")
record = read("history/version_0_53/baseline_record.json")
need(digest(BASELINE.read_bytes()) == record.get("archive_sha256", record.get("sha256")), "original supplied archive SHA256")
need(record.get("source_commit", PIN) == cfg["source_commit"] == PIN, "baseline and current source pin agree")
need(PIN.encode() in raw("history/version_0_53/README.md"), "frozen baseline readme declares the exact accepted source pin")

# Check preservation against the supplied archive as well as its own manifest.
manifest = raw("history/version_0_53/SHA256SUMS").decode()
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
need(len(entries) == 7874, "baseline contains exactly 7874 manifest artifacts")
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
    for rel in ["RH_GRH_reconstruction_roadmap_v0_53.txt",
                "RH_GRH_parallel_execution_plan_v0_53.txt"]:
        need(prefix + rel in names and raw("history/version_0_53/" + rel) == archive.read(prefix + rel),
             "frozen predecessor planning file equals supplied archive: " + rel)

old_claims, claims = base["claims"], current["claims"]
need(len(old_claims) == 3361, "baseline contains exactly 3361 numbered claims")
need(claims[:3361] == old_claims, "all 3361 original claim objects retained literally")
need(current["source_files"][:len(base["source_files"])] == base["source_files"], "original provenance source inventory retained literally")
need(index["source_files"][:len(old_index["source_files"])] == old_index["source_files"], "original source-index prefix retained literally")
new = claims[3361:]
need(len(new) == 90 and len(claims) == 3451, "90 new claims and 3451 cumulative claims")
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
    "actual_section_localization_v54": 21,
    "rank_two_connectedness_v54": 25,
    "archimedean_orbital_scalar_v54": 18,
    "wach_inclusion_saturation_v54": 26,
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
    need(current["component_scope_metadata_as_received_v0_54"].get(component) == scope,
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
# This independently tests the completed/retained boundaries, not just counts.
asl = sidecars["actual_section_localization_v54"]["contracts.json"]
asl_cl = sidecars["actual_section_localization_v54"]["closure.json"]
need(asl.get("global_perf_producer_supplied") is True and
     asl_cl.get("global_perf_producer_supplied") is True,
     "ASL supplies full original universal arbitrary-base smooth-projective Perf")
need(asl.get("global_section_laws_unconditionally_supplied") is False and
     asl_cl.get("global_section_laws_unconditionally_supplied") is False and
     asl_cl.get("globally_supplied_laws") == [],
     "ASL complete Perf does not unconditionally supply section laws")
discharged = {x["id"] for x in asl["formerly_retained_producers_now_supplied"]}
need(discharged >= {"GSL_PERF_GEOMETRY", "FCD_ACTUAL_AFFINE_SECTIONS", "FCD_ACTUAL_SMOOTH_CHARTS",
                    "FCD_ACTUAL_GEOMETRIC_DEHOM", "FCD_ACTUAL_GEOMETRIC_CUBE"},
     "ASL supplies every formerly retained actual geometric model producer")
need({x["id"] for x in asl["remaining_global_producers"]} >= {
     "GSL_POL_BASE_CHANGE", "GSL_VANISH_CLOSED", "GSL_RANK_CLOSED", "GSL_TWIST_GEOMETRIC",
     "GSL_SERRE", "GSL_MUL_PULL", "GSL_MUL_GEOMETRY", "GSL_TORSION_DESCENT",
     "GSL_GEOM_INTEGRAL", "GSL_RANK_ONE", "GSL_SECTION_DECOMP", "GSL_FINITE_GROWTH", "GSL_SQUARE",
     "GSL_INHERITED_NFL", "GSL_INHERITED_TDR"},
     "ASL retains exact separate P,V,R,T producers and inherited original geometry scope")
need({x["id"] for x in asl["inherited_inputs"]} == {"FCD13", "FCD18", "GSL8", "GSL9", "GSL10"},
     "ASL consumes the exact completed algebra and finite-matrix join")
need("ASL21" in {x["claim_id"] for x in asl["completed_original_suppliers"]},
     "ASL full original Perf endpoint is bound to ASL21")

rtc = sidecars["rank_two_connectedness_v54"]["contracts.json"]
rtc_cl = sidecars["rank_two_connectedness_v54"]["closure.json"]
for key in [
    "full_original_wpres_supplied", "full_original_co_B_supplied",
    "full_original_gr_A_supplied", "full_original_cont_u_supplied",
    "generic_graded_algebra_both_allowed_ranks", "upstream_FinA_not_assumed",
    "full_original_preconnected_rank_two_supplied",
    "arbitrary_target_k_algebras_preserved", "arbitrary_core_residue_fields_preserved",
    "formal_series_evaluated_only_at_topologically_nilpotent_coordinates",
    "only_polynomial_image_evaluated_in_arbitrary_target", "broader_IsBar_scope_preserved",
    "full_original_finPtDown_supplied", "finPtDown_arbitrary_rank_and_all_primes",
    "all_original_IsCD_tests_and_scalar_towers_preserved",
    "extended_and_original_coefficient_frames_kept_distinct",
    "original_P_retained_at_arithmetic_entry", "host_ell_3_allowed", "same_g1",
]:
    need(rtc.get(key) is True, "RTC completed supplier or preserved original quantifier: " + key)
for key in [
    "general_point_loc_imported", "full_general_point_loc_supplied",
    "rank_three_triangular_realization_supplied", "full_loc_cpl_supplied",
    "full_loc_flat_supplied", "full_loc_rho_supplied",
    "full_PropagationTheoremGL2_supplied", "full_PropagationTheoremGL3_supplied",
    "actual_OffFin_producer_supplied", "actual_automorphic_or_Alt_producer_supplied",
    "full_GdEnd_supplied", "full_HostEnd_supplied", "selected_producer_closed",
]:
    need(rtc.get(key) is False, "RTC retains the independent downstream producer: " + key)
need({x["id"] for x in rtc["retained_suppliers"]} >= {
    "RTC_ACTUAL_SPACE_AND_MODULARITY_REALIZATION",
    "RTC_ACTUAL_LOCAL_COMPLETION_AND_FLATNESS", "RTC_DIMENSION_DENSITY_AND_SEED_INCIDENCE",
    "RTC_RANK_THREE_CORNER_AND_PROPAGATION", "RTC_AUTOMORPHIC_AND_ALT_WITNESSES",
    "RTC_BROADER_POINT_REALIZATION",
}, "RTC records all six independent actual downstream supplier families")

aos = sidecars["archimedean_orbital_scalar_v54"]["contracts.json"]
aos_cl = sidecars["archimedean_orbital_scalar_v54"]["closure.json"]
need(aos.get("endpoint_claim") == "AOS18" and aos.get("primary_endpoint_claim") == "AOS11"
     and aos.get("positive_test_endpoint_claim") == "AOS12",
     "AOS exact primary, positive-test and full integration endpoints are distinguished")
need(aos.get("remaining_exact_producers_for_PushInf") == [] and
     aos.get("remaining_exact_producers_for_AprimeInf") == [],
     "AOS has no stale retained producer in the completed infinity scalar chain")
for name in ["PlaceJac", "GaugeDens", "GaugeVolU", "HinfCompact", "PushInf", "ConstTest",
             "ExInf", "HtotInf", "WeilInf", "AinfValue", "AinfClause", "GinfTest", "AprimeInf"]:
    need(any(name in x for x in aos["completed_original_substatements"]),
         "AOS records complete original infinity supplier: " + name)
need(bool(aos.get("shared_data_preserved")) and bool(aos.get("remaining_downstream_boundaries")),
     "AOS preserves original character/bridge/measures and independent arithmetic volume/transport boundaries")
need(any("every section" in x.lower() for x in aos["shared_data_preserved"]),
     "AOS retains arbitrary original sections without an added measurability premise")

wis = sidecars["wach_inclusion_saturation_v54"]["contracts.json"]
wis_cl = sidecars["wach_inclusion_saturation_v54"]["closure.json"]
we = {x["endpoint"]: x for x in wis["completed_source_endpoints"]}
for name, ident in {
    "GlobalTheory.IoInj.abstract": "WIS17",
    "GlobalTheory.IoInj.ioE_injective_saturated_inter": "WIS18",
    "GlobalTheory.HWL.Rational.padic_closed": "WIS19",
    "GlobalTheory.Decompl.FixL.fixSub_ladic": "WIS20",
    "GlobalTheory.Decompl.exists_fix_lift_of_fix_mod": "WIS21",
    "GlobalTheory.TiltComplete.tilt_separated_complete": "WIS22",
    "GlobalTheory.Decompl.nearPi_sep_complete": "WIS24",
    "GlobalTheory.Decompl.fixSub_nearPi_complete": "WIS25",
}.items():
    need(we.get(name, {}).get("claim") == ident and
         we.get(name, {}).get("all_original_premises_retained") is True,
         "WIS supplies the complete original endpoint: " + name)
need(we["HWL.WachEx via WLD26"]["status"] == "conditional_reduction_only" and
     len(wis["conditional_reduction_extra_inputs"]["WIS26"]) == 2,
     "WIS full inclusion leaves exactly two period-ring suppliers before WachEx")
need(any("LocTied" in x and "IsStd" in x for x in wis["entry_premises"]),
     "WIS retains original tied realization data explicitly")
for key in ["stronger_mu_adic_completeness_not_claimed", "same_actual_period_rings_and_maps",
            "no_extra_interlayer_transition_hypothesis"]:
    need(wis.get(key) is True, "WIS exact scope guard: " + key)
need(any("HW/Fon/Cmp" in x for x in wis["remaining"]) and
     any("ConclF" in x for x in wis["remaining"]),
     "WIS preserves full comparison and common denominator-family boundaries")

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
            need(raw("source_snapshot_v0_54/" + path) == data_s, "aggregate source snapshot exact: " + path)
        data_s = source_data[path]
        need(digest(data_s) == src.get("file_sha256", src.get("full_file_sha256", src.get("sha256"))), cid + ": full source hash " + path)
        lines = data_s.splitlines(keepends=True)
        a, b = src["line_start"], src["line_end"]
        need(1 <= a <= b <= len(lines) and digest(b"".join(lines[a-1:b])) == src["range_sha256"],
             cid + ": exact source range " + path + ":" + str(a) + "-" + str(b))
        source_ranges.add((path, a, b))
        if src.get("snapshot_file"):
            need(raw(src["snapshot_file"]) == data_s, cid + ": original component snapshot exact")
snapshot = read("source_snapshot_v0_54/manifest.json")
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
            parent_loc = byid[item["id"]]["proof_location"]
            need(all(parent_loc.get(k) == v for k, v in loc.items()), component + ": inherited proof location agrees with cumulative ledger " + item["id"])
        for binding in item.get("claim_bindings", []):
            loc_data = raw(binding["file"])
            part = b"".join(loc_data.splitlines(keepends=True)[binding["line_start"]-1:binding["line_end"]])
            need(digest(part) == binding["sha256"], component + ": explicit inherited claim binding " + binding["id"])
            need(item.get("proof_hashes", {}).get(binding["id"]) == binding["sha256"],
                 component + ": inherited hash table agrees " + binding["id"])
            parent_loc = byid[binding["id"]]["proof_location"]
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
            parent_loc = byid[item["id"]]["proof_location"]
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
        loc = claim["proof_location"]
        expected = loc.get("range_sha256", loc.get("sha256", loc.get("paragraph_sha256")))
        need(expected in {digest(part), digest(part.rstrip(b"\r\n"))}, cid + ": inherited proof-block integrity")
        if loc.get("file_sha256"):
            need(digest(data_p) == loc["file_sha256"], cid + ": inherited file integrity")
        inherited_checked.add(cid)

# Inspect original reviews as well as the registry summary.
registry = read("reviews_v0_54/review_registry.json")
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
        for source_row in review.get("source_files_verified", review.get("source_files", [])):
            path = source_row["path"]
            need(path in all_component_sources and digest(all_component_sources[path]) ==
                 source_row.get("sha256", source_row.get("file_sha256")),
                 cname + ": original independent review source-file binding: " + path)
        for source_row in review.get("source_ranges_verified", review.get("source_ranges", [])):
            path = source_row["path"]
            lines = all_component_sources[path].splitlines(keepends=True)
            part = b"".join(lines[source_row["line_start"]-1:source_row["line_end"]])
            need(source_row.get("range_sha256", source_row.get("sha256")) in
                 {digest(part), digest(part.rstrip(b"\r\n"))},
                 cname + ": original independent review source-range binding: " + path)
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
need(reviewed == {c["id"] for c in new}, "all 90 new claims covered by independent reviews")

# The whole selected graph is immutable in this release; progress is additive.
old_map = read("dependency_audit_v0_53/obligation_map.json")
new_map = read("dependency_audit_v0_54/obligation_map.json")
old_nodes = {n["id"]: n for n in old_map["nodes"]}
nodes = {n["id"]: n for n in new_map["nodes"]}
need(len(nodes) == len(new_map["nodes"]) == 121 and set(nodes) == set(old_nodes), "original 121 selected nodes retained")
need(cfg["closed_selected_leaves"] == {}, "no new whole selected leaf closure")
for cid, old_node in old_nodes.items():
    for key, value in old_node.items():
        if key == "contract" and cid in cfg.get("updated_contracts", {}):
            need(nodes[cid].get("historical_contract_narrative_v0_53") == value, cid + ": previous exact contract narrative retained")
        else:
            need(nodes[cid].get(key) == value, cid + ": original selected scope/status field retained: " + key)
logical = {k: n["requires"] for k, n in nodes.items()}
need(sum(map(len, logical.values())) == 161, "all original 161 selected edges retained")
check_dag(logical, "selected sufficient-route graph remains acyclic")
closed_statuses = {"proved_in_stated_scope", "published_application_checked", "complete", "closed"}
opens = {k for k, n in nodes.items() if n["gate"] == "LEAF" and n["status"] not in closed_statuses}
old_register = read("dependency_audit_v0_53/remaining_leaf_register.json")
register = read("dependency_audit_v0_54/remaining_leaf_register.json")
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
    need(nodes[cid].get("version_0_54_progress") == progress, cid + ": exact additive progress record")
coverage = read("dependency_audit_v0_54/route_coverage.json")
need(coverage["graph_sha256"] == bindings["dependency_audit_v0_54/obligation_map.json"], "route coverage binds current graph")
need(set(coverage["shared_open_leaf_ids"]) == opens & rh & grh and set(coverage["dirichlet_grh_only_open_leaf_ids"]) == (opens & grh) - rh, "route coverage exactly reproduces reachability")
delta = read("dependency_audit_v0_54/closure_delta.json")
need(delta["closed_selected_leaves"] == {} and delta["closed_nested_producers"] == cfg["closed_nested_producers"], "whole and nested closure records kept separate")
disposition = read("dependency_audit_v0_54/target_disposition.json")
old_disposition = read("dependency_audit_v0_53/target_disposition.json")
need(len(disposition["records"]) == len(old_disposition["records"]) == 245 and len(disposition["scope_groups"]) == 107, "245 original source dispositions and 107 scope groups retained")
need(all(all(after.get(k) == v for k, v in before.items()) for before, after in zip(old_disposition["records"], disposition["records"])), "historical disposition records retained with additive notes")
need(disposition["scope_groups"] == old_disposition["scope_groups"], "historical target scope grouping unchanged")
targets = read("next_source_targets.json")
old_targets = read("history/version_0_53/next_source_targets.json")
need(targets["targets"] == old_targets["targets"], "all original next-source targets retained literally")
checkpoint = read("continuation_checkpoint.json")
need(checkpoint["remaining_major_inputs"] == cfg["remaining_major_inputs"] and checkpoint["next_targets"] == cfg["next_targets"], "continuation checkpoint carries exact current frontier and priorities")
for key, expected in {
    "current_roadmap": "RH_GRH_reconstruction_roadmap_v0_54.txt",
    "current_progress_report": "RH_reconstruction_progress_v0_54.txt",
    "current_parallel_plan": "RH_GRH_parallel_execution_plan_v0_54.txt",
}.items():
    need(checkpoint["version_0_54_update"].get(key) == expected and (ROOT / expected).is_file(),
         "continuation checkpoint points to actual current deliverable: " + key)
need(targets["next_local_priority"] == cfg["next_targets"] and current["scope"] == cfg["status"], "current priorities and provenance scope match configuration")
expected_stats = {"new_claims": 90, "cumulative_claims": 3451, "selected_nodes": 121, "selected_edges": 161,
                  "open_count": 24, "open_categories": categories, "shared_open": 17, "extra_grh_open": 7,
                  "new_source_files_checked": len(source_data), "new_unique_source_ranges_checked": len(source_ranges)}
need(stats == expected_stats, "every integration statistic independently recomputed")
scope_updates = cfg["validation_scope_updates"]
for key in [
    "full_original_actual_section_localization_and_cube_comparison_complete",
    "full_original_arbitrary_base_smooth_projective_Perf_complete",
    "independent_PolBaseChange_Serre_all_cover_H1_integrality_rank_square_inputs_remain",
    "full_original_upstream_wpres_co_B_gr_A_cont_u_complete_without_FinA",
    "full_original_preconnected_rank_two_complete",
    "full_original_FinPtDown_complete_at_all_original_ranks_and_primes",
    "actual_LocFlat_LocRho_dimension_seed_propagation_OffFin_automorphic_inputs_remain",
    "full_original_PlaceJac_GaugeDens_GaugeVolU_complete",
    "full_original_PushInf_ConstTest_exact_scalar_complete",
    "full_original_ExInf_HtotInf_WeilInf_AinfValue_AprimeInf_complete",
    "all_original_selfdual_fiber_witnesses_and_all_sections_preserved",
    "original_setting_bridge_and_infinity_measures_preserved",
    "RealBracket_arithmetic_quotient_volumes_finite_place_and_transport_counting_remain",
    "full_original_four_clause_actual_Wach_inclusion_complete",
    "full_original_padic_fixed_subring_tilt_and_NearPi_completeness_inputs_complete",
    "two_exact_period_ring_suppliers_before_full_WachEx_remain_explicit",
    "original_LocTied_IsStd_and_Bhatt_Scholze_inputs_retained",
    "coherent_Wach_HW_Fon_Cmp_and_common_ConclF_remain_explicit",
    "GLOBAL_LOCAL_GAIN_full_v49_closure_preserved",
    "no_new_whole_selected_obligation_closed",
]:
    need(scope_updates.get(key) is True, "current validation scope guard: " + key)
for key in ["all_layer_WachEx_claimed_unconditional",
            "actual_section_localization_gluing_and_affine_geometric_suppliers_remain_explicit",
            "three_exact_period_ring_suppliers_before_full_WachEx_remain_explicit",
            "actual_geometric_section_model_PolBaseChange_Serre_integrality_rank_square_suppliers_remain_explicit"]:
    need(scope_updates.get(key) is False,
         "superseded or forbidden closure/frontier flag explicitly disabled: " + key)
    need(new_map["validation"].get(key) is False,
         "current graph does not retain an incompatible historical flag: " + key)
need("complete" in scope_updates.get("superseded_v53_actual_geometric_model_flag_explanation", "") and
     "remaining" in scope_updates.get("superseded_v53_three_period_suppliers_explanation", ""),
     "superseded geometric-model and three-period-supplier scopes explicitly explained")

# Check both readers against component blocks and the historical proof body.
old_reader = raw("RH_readable_reconstruction_v0_53.tex").decode()
reader = raw("RH_readable_reconstruction_v0_54.tex").decode()
short = raw("RH_new_proofs_v0_54.tex").decode()
for name, body in [("cumulative", reader), ("new-proofs", short)]:
    need(not re.search(r"@(NEW|OLD|TOTAL|OPEN|SHARED|EXTRA|C|B)@", body),
         name + ": no unreplaced inventory placeholders in assembled manuscript")
old_audit = raw("dependency_audit_v0_53/main.tex").decode()
marker = re.search(r"^\\section\{[^\n]+", old_audit, re.M)[0]
end = r"\section{The arithmetic still to be written out}"
need(old_reader[old_reader.index(marker):old_reader.index(end)] == reader[reader.index(marker):reader.index(end)], "entire historical cumulative proof body preserved verbatim")
def unbreak(s):
    return re.sub(r"\\allowbreak[ \t]*", "", s)
for c in new:
    _, block = proof_bytes(c)
    pattern = r"^% BEGIN " + re.escape(c["id"]) + r"\s*\n.*?^% END " + re.escape(c["id"]) + r"[ \t]*(?:\n|$)"
    for name, body in [("cumulative", reader), ("new-proofs", short)]:
        matches = re.findall(pattern, body, re.M | re.S)
        need(len(matches) == 1 and unbreak(matches[0]) == unbreak(block.decode()), c["id"] + ": exact complete block in " + name + " edition, modulo harmless line breaks")
for name in ["v0_54_frontmatter.tex", "v0_54_audit_intro.tex", "dependency_audit_v0_54/main.tex",
             "RH_dependency_audit_v0_54.txt", "RH_reconstruction_progress_v0_54.txt",
             "RH_GRH_reconstruction_roadmap_v0_54.txt", "RH_GRH_parallel_execution_plan_v0_54.txt", "README.md"]:
    raw(name)
for name in ["RH_reconstruction_progress_v0_54.txt", "RH_GRH_reconstruction_roadmap_v0_54.txt",
             "RH_GRH_parallel_execution_plan_v0_54.txt"]:
    text_doc = raw(name).decode()
    need(all(re.search(r"\b" + re.escape(cid) + r"\b", text_doc) for cid in opens),
         name + ": every one of the 24 exact open register identifiers is present")
    need(PIN in text_doc and all(str(n) in text_doc for n in [90, 3451, 121, 161, 24]),
         name + ": current source pin and inventory are stated")
tex = read("tex_validation.json")
need(tex["artifact_version"] == "0.54" and len(tex["documents"]) == 2, "both current reader editions have draft TeX validation")
old_tex = read("history/version_0_53/tex_validation.json")
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
for path in sorted(ROOT.glob("*v0_54.py")):
    raw(str(path.relative_to(ROOT)))
raw("reviews_v0_54/narrative_scope_review.txt")
raw("reviews_v0_54/audit_integration_geometry_alltest.py")

notes = [
    "The accepted Lean source is not re-audited for formal correctness. This checks exact human proof/source bytes, independent reviews, preservation, mathematical scope and the assembled reading editions; no Lean build or kernel replay was run.",
    "All 3361 predecessor claim records and original dependency edges remain unchanged. The entire historical cumulative proof body is preserved verbatim, and all 90 new numbered blocks appear exactly in both editions modulo harmless TeX line breaks.",
    "ASL completes the original actual smooth-projective Perf producer over arbitrary rings, including the twisted power extension, all-degree localization/dehomogenization, actual cube map and affine dual-basis geometry. Its single model and fixed matrices precede every coefficient change and specified pullback. Independent polarization, all-cover H1, geometric rank and square-law inputs remain explicit; the full section laws are not claimed unconditional.",
    "RTC completes the upstream actual coefficient-ring/grading suppliers without FinA, the rank-two preconnected core and original arbitrary-rank coefficient descent. Actual local charts and flatness, sharp dimensions, seed incidence, complete rank-specific propagation, OffFin and automorphic producers remain. Original P, the same g1, distinct original/extended coefficient frames, nilpotent coefficient tests and Host ell=3 are retained.",
    "AOS completes the exact original archimedean orbital/integration scalar on the same setting, bridge and infinity measures, for every original self-dual/fiber witness and every section. Arithmetic quotient volumes, finite-place factors, original RealBracket inputs, all-family transport/counting and global spectral identifications remain separate.",
    "WIS completes all four actual coefficient inclusion clauses, the generic p-adic closed-image theorem, arbitrary-H fixed-subring p-completeness and fixed mod-p lifts, and exact tilt/NearPi separation/summation suppliers. Its determinant shortcut supplies only the needed Jacobson consequence, without claiming the stronger mu-adic theorem. Original LocTied/IsStd and realization premises remain; the actual prism and remaining homogeneous invariant matrix descent are still required before WachEx.",
    "No new whole selected leaf closes. All 121 selected nodes, 161 edges and original whole statuses remain. Exactly 24 whole obligations remain: 17 shared RH/Dirichlet-GRH and seven extra Dirichlet-GRH; inventory counts are not completion percentages.",
]

result = {
    "schema": "rh-independent-integration-review/1", "artifact_version": "0.54", "date": "2026-11-23",
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
    "inherited_parent_provenance_bindings_checked": inherited_parent_bindings,
    "all_component_manifest_source_files_checked": len(all_component_sources),
    "all_component_manifest_source_ranges_checked": len(component_manifest_ranges),
    "separately_pinned_dependency_files_checked": dependency_files_checked,
    "passed_check_count": len(checks), "notes": notes,
    "input_bindings": dict(sorted(bindings.items())),
}
out = ROOT / ("reviews_v0_54/preflight_geometry_alltest.json" if args.preflight else "reviews_v0_54/integration_geometry_alltest.json")
out.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n")
print(json.dumps({k: result[k] for k in ["status", "errors", "statistics", "baseline_manifest_artifacts_preserved", "baseline_artifacts_retained_in_history", "passed_check_count"]}, ensure_ascii=False, indent=2))
raise SystemExit(bool(errors))
