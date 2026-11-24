#!/usr/bin/env python3
"""Independent v0.53 preservation, proof/source binding and exact-scope audit.

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
OLD = ROOT / "history/version_0_52"
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
cfg = read("increment_v0_53.json")
stats = read("integration_stats_v0_53.json")
base = read("history/version_0_52/provenance.json")
current = read("provenance.json")
old_index = read("history/version_0_52/source_index.json")
index = read("source_index.json")
record = read("history/version_0_52/baseline_record.json")
need(digest(BASELINE.read_bytes()) == record.get("archive_sha256", record.get("sha256")), "original supplied archive SHA256")
need(record.get("source_commit", PIN) == cfg["source_commit"] == PIN, "baseline and current source pin agree")
need(PIN.encode() in raw("history/version_0_52/README.md"), "frozen baseline readme declares the exact accepted source pin")

# Check preservation against the supplied archive as well as its own manifest.
manifest = raw("history/version_0_52/SHA256SUMS").decode()
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
need(preserved == len(entries), "every baseline manifest artifact retained")
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
    for rel in ["RH_GRH_reconstruction_roadmap_v0_52.txt",
                "RH_GRH_parallel_execution_plan_v0_52.txt"]:
        need(prefix + rel in names and raw("history/version_0_52/" + rel) == archive.read(prefix + rel),
             "frozen predecessor planning file equals supplied archive: " + rel)

old_claims, claims = base["claims"], current["claims"]
need(len(old_claims) == 3279, "baseline contains exactly 3279 numbered claims")
need(claims[:3279] == old_claims, "all 3279 original claim objects retained literally")
need(current["source_files"][:len(base["source_files"])] == base["source_files"], "original provenance source inventory retained literally")
need(index["source_files"][:len(old_index["source_files"])] == old_index["source_files"], "original source-index prefix retained literally")
new = claims[3279:]
need(len(new) == 82 and len(claims) == 3361, "82 new claims and 3361 cumulative claims")
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
    "flat_chart_descent_v53": 18,
    "arithmetic_component_propagation_v53": 19,
    "global_measure_rescaling_v53": 19,
    "wach_lattice_descent_v53": 26,
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
    need(current["component_scope_metadata_as_received_v0_53"].get(component) == scope,
         component + ": full finalized metadata and original premises retained")
    sidecars[component] = {}
    for filename in ["contracts.json", "closure.json", "original_contracts.json", "retained_foundations.json",
                     "classical_inputs.json", "published_inputs.json", "claim_dag.json", "source_manifest.json", "tex_validation.json", "inherited_inputs.json"]:
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

# These are the reviewed endpoint distinctions, independently of the aggregate
# claim count. Completed implications cannot discharge their own antecedents.
fcd = sidecars["flat_chart_descent_v53"]["contracts.json"]
fcd_cl = sidecars["flat_chart_descent_v53"]["closure.json"]
need({r["claim_id"] for r in fcd["completed_original_suppliers"]} == {"FCD8", "FCD12", "FCD18"},
     "FCD closes exactly the three full original algebraic model suppliers")
need(fcd.get("global_section_laws_unconditionally_supplied") is False and
     fcd_cl.get("global_section_laws_unconditionally_supplied") is False and fcd_cl["globally_supplied_laws"] == [],
     "FCD actual geometric section laws and Perf producer remain separate")
need(set(fcd_cl["pending_actual_geometric_producers"]) ==
     {"FCD_ACTUAL_AFFINE_SECTIONS", "FCD_ACTUAL_SMOOTH_CHARTS", "FCD_ACTUAL_GEOMETRIC_DEHOM", "FCD_ACTUAL_GEOMETRIC_CUBE"},
     "FCD preserves exact four actual geometric next suppliers")
need("GSL_GEOM_INTEGRAL" in fcd_cl["unchanged_upstream_boundary"], "FCD retains geometric integrality")
acp = sidecars["arithmetic_component_propagation_v53"]["contracts.json"]
for key in ["full_original_FinPtOf_closed", "all_original_IsCD_tests_preserved",
            "finite_residue_degree_supplied_by_IsCD", "specified_scalar_tower_preserved",
            "ordinary_character_values_and_inverses_in_C", "full_Alt_to_original_projection_closed",
            "WitA_and_WitAQ_retained_on_terminal_route", "original_P_retained", "host_ell_3_allowed", "same_g1",
            "extended_and_original_coefficient_frames_kept_distinct"]:
    need(acp.get(key) is True, "ACP exact completed/retained scope: " + key)
for key in ["full_original_FinPt_producer_supplied", "full_PropagationTheoremGL2_closed",
            "full_PropagationTheoremGL3_closed", "full_general_point_loc_closed",
            "source_point_loc_used_as_axiom", "actual_Alt_producer_supplied", "full_GdEnd_closed",
            "full_HostEnd_closed", "full_GdEndAlt_closed", "full_HostEndAlt_closed", "full_original_finPtDown_supplied"]:
    need(acp.get(key) is False, "ACP unsupplied larger producer remains explicit: " + key)
need({x["id"] for x in acp["closed_subcontracts"]} >=
     {"full_original_FinPtOf", "full_original_NicePrimeEx", "full_original_LocProp",
      "full_original_GlobProp", "full_original_ChartOfFlat", "full_original_GlobOfCharts"},
     "ACP full original finite-point implication and abstract propagation subtheorems all recorded")
need("ACP_FINPT_COEFFICIENT_DESCENT" in {x["id"] for x in acp["retained_suppliers"]},
     "ACP original finPtDown transport is recorded as a separate retained supplier")
need("FinA" in next(x["statement"] for x in acp["retained_suppliers"]
                   if x["id"] == "ACP_ARITHMETIC_CHART_GEOMETRY"),
     "ACP generic arithmetic chart producer explicitly excludes circular downstream FinA input")
gmr = sidecars["global_measure_rescaling_v53"]["contracts.json"]
gmr_cl = sidecars["global_measure_rescaling_v53"]["closure.json"]
need(gmr.get("endpoint_claim") == "GMR19", "GMR full RescaleStep3 endpoint is GMR19")
need(gmr.get("remaining_exact_producers_for_RescaleStep3") == [] and
     gmr_cl.get("remaining_source_producers_in_this_measure_normalization_chain") == [],
     "GMR completed normalization chain has no stale retained subproducer")
need(gmr_cl.get("conditional_consequences") == [{"claim": "GMR19", "consequence": "RescaleStep3",
     "retained_input": "Exact original SiegelWeilUnitaryConvergent"}],
     "GMR full implication retains the original Siegel-Weil premise")
need(bool(gmr.get("shared_data_preserved")) and bool(gmr_cl.get("remaining_downstream_boundaries")),
     "GMR retains same setting/bridge/measures and separate arithmetic volume/spectral boundaries")
wld = sidecars["wach_lattice_descent_v53"]["contracts.json"]
wld_cl = sidecars["wach_lattice_descent_v53"]["closure.json"]
for key in ["no_extra_flatness_of_period_extension", "same_actual_etale_module_and_all_original_maps",
            "no_extra_interlayer_transition_hypothesis"]:
    need(wld.get(key) is True, "WLD exact scope guard: " + key)
for key in ["full_original_generic_build_complete", "full_original_generic_build_prism_complete"]:
    need(wld_cl.get(key) is True, "WLD complete original generic supplier: " + key)
for key in ["unconditional_original_all_layer_WachEx_complete", "full_HW_Fon_Cmp_complete",
            "full_GLOBAL_DENOMINATOR_supplier_supplied"]:
    need(wld_cl.get(key) is False, "WLD explicit unsupplied final supplier: " + key)
we = {x["claim"]: x for x in wld_cl["completed_source_endpoints"]}
need(we["WLD24"]["endpoint"] == "GlobalTheory.WachLattice.build" and
     we["WLD25"]["endpoint"] == "GlobalTheory.WachLattice.build_prism" and
     we["WLD26"]["status"] == "conditional_reduction_only", "WLD generic construction distinguished from actual all-layer WachEx")

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
            need(raw("source_snapshot_v0_53/" + path) == data_s, "aggregate source snapshot exact: " + path)
        data_s = source_data[path]
        need(digest(data_s) == src.get("file_sha256", src.get("full_file_sha256", src.get("sha256"))), cid + ": full source hash " + path)
        lines = data_s.splitlines(keepends=True)
        a, b = src["line_start"], src["line_end"]
        need(1 <= a <= b <= len(lines) and digest(b"".join(lines[a-1:b])) == src["range_sha256"],
             cid + ": exact source range " + path + ":" + str(a) + "-" + str(b))
        source_ranges.add((path, a, b))
        if src.get("snapshot_file"):
            need(raw(src["snapshot_file"]) == data_s, cid + ": original component snapshot exact")
snapshot = read("source_snapshot_v0_53/manifest.json")
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
# Git files. Their exact bytes were independently fetched in the FCD math review.
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
registry = read("reviews_v0_53/review_registry.json")
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
            need(source_row["range_sha256"] in {digest(part), digest(part.rstrip(b"\r\n"))},
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
need(reviewed == {c["id"] for c in new}, "all 82 new claims covered by independent reviews")

# The whole selected graph is immutable in this release; progress is additive.
old_map = read("dependency_audit_v0_52/obligation_map.json")
new_map = read("dependency_audit_v0_53/obligation_map.json")
old_nodes = {n["id"]: n for n in old_map["nodes"]}
nodes = {n["id"]: n for n in new_map["nodes"]}
need(len(nodes) == len(new_map["nodes"]) == 121 and set(nodes) == set(old_nodes), "original 121 selected nodes retained")
need(cfg["closed_selected_leaves"] == {}, "no new whole selected leaf closure")
for cid, old_node in old_nodes.items():
    for key, value in old_node.items():
        if key == "contract" and cid in cfg.get("updated_contracts", {}):
            need(nodes[cid].get("historical_contract_narrative_v0_52") == value, cid + ": previous exact contract narrative retained")
        else:
            need(nodes[cid].get(key) == value, cid + ": original selected scope/status field retained: " + key)
logical = {k: n["requires"] for k, n in nodes.items()}
need(sum(map(len, logical.values())) == 161, "all original 161 selected edges retained")
check_dag(logical, "selected sufficient-route graph remains acyclic")
closed_statuses = {"proved_in_stated_scope", "published_application_checked", "complete", "closed"}
opens = {k for k, n in nodes.items() if n["gate"] == "LEAF" and n["status"] not in closed_statuses}
old_register = read("dependency_audit_v0_52/remaining_leaf_register.json")
register = read("dependency_audit_v0_53/remaining_leaf_register.json")
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
    need(nodes[cid].get("version_0_53_progress") == progress, cid + ": exact additive progress record")
coverage = read("dependency_audit_v0_53/route_coverage.json")
need(coverage["graph_sha256"] == bindings["dependency_audit_v0_53/obligation_map.json"], "route coverage binds current graph")
need(set(coverage["shared_open_leaf_ids"]) == opens & rh & grh and set(coverage["dirichlet_grh_only_open_leaf_ids"]) == (opens & grh) - rh, "route coverage exactly reproduces reachability")
delta = read("dependency_audit_v0_53/closure_delta.json")
need(delta["closed_selected_leaves"] == {} and delta["closed_nested_producers"] == cfg["closed_nested_producers"], "whole and nested closure records kept separate")
disposition = read("dependency_audit_v0_53/target_disposition.json")
old_disposition = read("dependency_audit_v0_52/target_disposition.json")
need(len(disposition["records"]) == len(old_disposition["records"]) == 245 and len(disposition["scope_groups"]) == 107, "245 original source dispositions and 107 scope groups retained")
need(all(all(after.get(k) == v for k, v in before.items()) for before, after in zip(old_disposition["records"], disposition["records"])), "historical disposition records retained with additive notes")
need(disposition["scope_groups"] == old_disposition["scope_groups"], "historical target scope grouping unchanged")
targets = read("next_source_targets.json")
old_targets = read("history/version_0_52/next_source_targets.json")
need(targets["targets"] == old_targets["targets"], "all original next-source targets retained literally")
checkpoint = read("continuation_checkpoint.json")
need(checkpoint["remaining_major_inputs"] == cfg["remaining_major_inputs"] and checkpoint["next_targets"] == cfg["next_targets"], "continuation checkpoint carries exact current frontier and priorities")
for key, expected in {
    "current_roadmap": "RH_GRH_reconstruction_roadmap_v0_53.txt",
    "current_progress_report": "RH_reconstruction_progress_v0_53.txt",
    "current_parallel_plan": "RH_GRH_parallel_execution_plan_v0_53.txt",
}.items():
    need(checkpoint["version_0_53_update"].get(key) == expected and (ROOT / expected).is_file(),
         "continuation checkpoint points to actual current deliverable: " + key)
need(targets["next_local_priority"] == cfg["next_targets"] and current["scope"] == cfg["status"], "current priorities and provenance scope match configuration")
expected_stats = {"new_claims": 82, "cumulative_claims": 3361, "selected_nodes": 121, "selected_edges": 161,
                  "open_count": 24, "open_categories": categories, "shared_open": 17, "extra_grh_open": 7,
                  "new_source_files_checked": len(source_data), "new_unique_source_ranges_checked": len(source_ranges)}
need(stats == expected_stats, "every integration statistic independently recomputed")
scope_updates = cfg["validation_scope_updates"]
for key in [
    "full_original_homogeneous_chart_descent_and_finite_graded_presentation_complete",
    "full_original_exists_noetherian_model_grCube_complete",
    "actual_geometric_section_model_PolBaseChange_Serre_integrality_rank_square_suppliers_remain_explicit",
    "actual_section_localization_gluing_and_affine_geometric_suppliers_remain_explicit",
    "full_original_FinPtOf_complete_from_OffFin",
    "all_original_IsCD_tests_and_specified_scalar_tower_preserved",
    "full_original_abstract_NicePrime_LocProp_GlobProp_ChartOfFlat_GlobOfCharts_complete",
    "actual_GL2_GL3_propagation_OffFin_and_automorphic_producers_remain_explicit",
    "full_original_Alt_to_original_projection_complete",
    "actual_Alt_WitA_WitAQ_suppliers_remain_explicit",
    "full_original_global_and_local_stabilizer_measure_suppliers_complete",
    "full_original_RescaleStep3_complete_on_supplied_setting",
    "same_standard_character_before_all_words_places_auxiliary_tuples",
    "original_setting_bridge_and_infinity_measures_preserved",
    "arithmetic_quotient_volume_identities_and_global_transport_counting_remain_explicit",
    "full_original_generic_Wach_build_and_build_prism_complete",
    "three_exact_period_ring_suppliers_before_full_WachEx_remain_explicit",
    "coherent_Wach_HW_Fon_Cmp_remains_explicit",
    "global_denominator_actual_ConclF_family_producer_remains_explicit",
    "GLOBAL_LOCAL_GAIN_full_v49_closure_preserved",
    "no_new_whole_selected_obligation_closed",
]:
    need(scope_updates.get(key) is True, "current validation scope guard: " + key)
need("algebraic Noetherian cube model is complete" in
     scope_updates.get("superseded_v52_geometric_model_flag_explanation", "") and
     "actual geometric section localization/comparison" in
     scope_updates.get("superseded_v52_geometric_model_flag_explanation", ""),
     "broad inherited geometric-model flag is qualified to the remaining actual geometric comparison")
for key in ["all_layer_WachEx_claimed_unconditional"]:
    need(scope_updates.get(key) is False, "superseded or forbidden closure flag explicitly disabled: " + key)

# Check both readers against component blocks and the historical proof body.
old_reader = raw("RH_readable_reconstruction_v0_52.tex").decode()
reader = raw("RH_readable_reconstruction_v0_53.tex").decode()
short = raw("RH_new_proofs_v0_53.tex").decode()
for name, body in [("cumulative", reader), ("new-proofs", short)]:
    need(not re.search(r"@(NEW|OLD|TOTAL|OPEN|SHARED|EXTRA|C|B)@", body),
         name + ": no unreplaced inventory placeholders in assembled manuscript")
old_audit = raw("dependency_audit_v0_52/main.tex").decode()
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
for name in ["v0_53_frontmatter.tex", "v0_53_audit_intro.tex", "dependency_audit_v0_53/main.tex",
             "RH_dependency_audit_v0_53.txt", "RH_reconstruction_progress_v0_53.txt",
             "RH_GRH_reconstruction_roadmap_v0_53.txt", "RH_GRH_parallel_execution_plan_v0_53.txt", "README.md"]:
    raw(name)
for name in ["RH_reconstruction_progress_v0_53.txt", "RH_GRH_reconstruction_roadmap_v0_53.txt",
             "RH_GRH_parallel_execution_plan_v0_53.txt"]:
    text_doc = raw(name).decode()
    need(all(re.search(r"\b" + re.escape(cid) + r"\b", text_doc) for cid in opens),
         name + ": every one of the 24 exact open register identifiers is present")
    need(PIN in text_doc and all(str(n) in text_doc for n in [82, 3361, 121, 161, 24]),
         name + ": current source pin and inventory are stated")
tex = read("tex_validation.json")
need(tex["artifact_version"] == "0.53" and len(tex["documents"]) == 2, "both current reader editions have draft TeX validation")
old_tex = read("history/version_0_52/tex_validation.json")
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
for path in sorted(ROOT.glob("*v0_53.py")):
    raw(str(path.relative_to(ROOT)))
raw("reviews_v0_53/audit_integration_arithmetic_common_frame.py")

notes = [
    "The accepted Lean source is not re-audited for formal correctness. This checks the human reconstruction's actual proof/source bytes, reviews, preservation and scope; no Lean build or kernel replay was run.",
    "All 3279 predecessor claim records and original dependency edges remain unchanged. The whole historical cumulative proof body is preserved verbatim; all 82 new numbered proof blocks appear in both current readers with only harmless TeX line-break insertions.",
    "FCD completes the full original simultaneous flat-chart coefficient descent, graded saturating presentation and Noetherian graded-cube model. One finite certificate collection determines one model and all actual cube comparisons before any later coefficient map. Original coefficient rings may be nonreduced or zero and later maps need not be flat. The actual geometric section charts and localization/gluing comparison, polarization, vanishing, integrality, rank and square producers remain explicit.",
    "ACP completes full original FinPtOf from a supplied rank-three Space and literal OffFin. IsCD itself supplies finite residue degree for the k+m_A construction; all ideal powers, coefficient structures and ordinary-character values/inverses are retained. NicePrimeEx and the full abstract local/global/chart propagation principles are proved, while actual arithmetic dimensions, connectedness, corner ideal, GL2/GL3 propagation and OffFin remain separate. Actual TwoRuns returns FinPt on an extended coefficient frame; finPtDown is an explicit retained transport to the original frame before AFE20. Generic arithmetic gr_A/loc_cpl remain upstream, and UCE13's downstream FinA antecedent is not used to fill that gap. Alt-to-original projection keeps the same g1 and does not produce the terminal WitA/WitAQ fields. Original P and Host ell=3 remain.",
    "GMR completes the original global and local stabilizer-measure suppliers and full RescaleStep3 at its original SiegelWeilUnitaryConvergent antecedent. It keeps the standard character before all places and auxiliary tuples, and the same supplied setting, bridge and infinite measures. Arithmetic quotient-volume identities, original all-family transport/counting and global spectral identifications remain distinct producers.",
    "WLD completes generic Wach build and build_prism at their original hypotheses, without adding period-extension flatness or interlayer hypotheses. The actual period prism, injectivity/unit reflection and homogeneous fixed-Frobenius matrix descent are retained before all-layer WachEx. Complete coherent HW/Fon/Cmp and the actual global denominator family remain open.",
    "FCD's four Mathlib completion/smoothness snapshots are separately pinned to the revision declared by the accepted lake-manifest; they are not mislabeled as RH-source Git blobs or added to the main-repository citation counts.",
    "No new whole selected leaf closes. All 121 selected nodes, 161 edges and original whole statuses remain. Exactly 24 whole obligations remain: 17 shared RH/Dirichlet-GRH and seven extra Dirichlet-GRH; inventory counts are not completion percentages.",
]

result = {
    "schema": "rh-independent-integration-review/1", "artifact_version": "0.53", "date": "2026-11-23",
    "reviewer": "/root/arithmetic_common_frame", "source_commit": PIN,
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
out = ROOT / ("reviews_v0_53/preflight_arithmetic_common_frame.json" if args.preflight else "reviews_v0_53/integration_arithmetic_common_frame.json")
out.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n")
print(json.dumps({k: result[k] for k in ["status", "errors", "statistics", "baseline_manifest_artifacts_preserved", "baseline_artifacts_retained_in_history", "passed_check_count"]}, ensure_ascii=False, indent=2))
raise SystemExit(bool(errors))
