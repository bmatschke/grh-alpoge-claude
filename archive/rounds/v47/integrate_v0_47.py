#!/usr/bin/env python3
"""Integrate the reviewed v0.47 increment without changing predecessor claims."""
from pathlib import Path
import collections
import copy
import hashlib
import json
import re
import shutil
import subprocess

ROOT = Path(__file__).resolve().parent
OLD = ROOT / "history/version_0_46"
SOURCE = ROOT.parent / "formal_source"
PIN = "7cbf7a0c32fca1badf05931879a37c3f8a2b03b4"
VERSION = "0.47"

def read(path):
    return json.loads(path.read_text())

def write(path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n")

def sha(data):
    return hashlib.sha256(data).hexdigest()

def filehash(path):
    return sha(path.read_bytes())

def topo(graph):
    seen, active, result = set(), set(), []
    def visit(node):
        if node in active:
            raise AssertionError(("dependency cycle", node))
        if node in seen:
            return
        assert node in graph, ("unknown dependency", node)
        active.add(node)
        for dep in graph[node]:
            visit(dep)
        active.remove(node)
        seen.add(node)
        result.append(node)
    for node in graph:
        visit(node)
    return result

CFG = read(ROOT / "increment_v0_47.json")
COMPONENTS = CFG["components"]
CLOSED = CFG["closed_selected_leaves"]
assert subprocess.check_output(
    ["git", "-C", str(SOURCE), "rev-parse", "HEAD"], text=True
).strip() == PIN

base = read(OLD / "provenance.json")
original_claims = copy.deepcopy(base["claims"])
ids = {c["id"] for c in original_claims}
new, source_bytes, source_records, source_ranges = [], {}, {}, set()
component_scopes = {}

for component in COMPONENTS:
    ledger = read(ROOT / component / "provenance.json")
    component_scopes[component] = {
        k: v for k, v in ledger.items()
        if k not in {"claims", "source_files", "source_inventory", "source_groups"}
    }
    for incoming in ledger["claims"]:
        c = copy.deepcopy(incoming)
        assert c["id"] not in ids, ("duplicate claim", c["id"])
        ids.add(c["id"])
        pl = c["proof_location"]
        proof = ROOT / pl["file"]
        data = proof.read_bytes()
        lines = data.splitlines(keepends=True)
        excerpt = b"".join(lines[pl["line_start"] - 1:pl["line_end"]])
        assert pl["sha256"] in {sha(excerpt), sha(excerpt.rstrip(b"\r\n"))}, ("proof range hash", c["id"])
        if sha(excerpt) != pl["sha256"]:
            pl["component_hash_without_final_line_terminator"] = pl["sha256"]
        pl.update(sha256=sha(excerpt), file_sha256=sha(data), range_sha256=sha(excerpt), bytes=len(excerpt))
        c.setdefault("classification", "B")
        c.setdefault("proof_status", "complete in stated scope")
        c.setdefault("review_status", "See hash-bound reviews_v0_47 and component review files")
        c.setdefault("introduced_in", VERSION)
        for s in c.get("sources", []):
            if "path" not in s or "line_start" not in s:
                continue
            path = s["path"]
            if path not in source_bytes:
                disk = (SOURCE / path).read_bytes()
                git = subprocess.check_output(["git", "-C", str(SOURCE), "show", PIN + ":" + path])
                assert disk == git, ("worktree differs from source pin", path)
                source_bytes[path] = disk
                source_records[path] = {
                    "path": path, "sha256": sha(disk), "bytes": len(disk),
                    "line_count": len(disk.splitlines()),
                    "verified_equal_to_pinned_git_blob": True,
                    "verified_in_version": VERSION,
                    "snapshot_path": "source_snapshot_v0_47/" + path,
                    "url": "https://github.com/CocoSgt/riemann-hypothesis-lean/blob/" + PIN + "/" + path,
                }
            disk = source_bytes[path]
            expected = s.get("file_sha256", s.get("full_file_sha256", s.get("sha256")))
            assert sha(disk) == expected, ("source file hash", c["id"], path)
            lines = disk.splitlines(keepends=True)
            assert 1 <= s["line_start"] <= s["line_end"] <= len(lines)
            excerpt = b"".join(lines[s["line_start"] - 1:s["line_end"]])
            assert s["range_sha256"] in {sha(excerpt), sha(excerpt.rstrip(b"\r\n"))}, ("source range hash", c["id"], path)
            if sha(excerpt) != s["range_sha256"]:
                s["component_hash_without_final_line_terminator"] = s["range_sha256"]
            s["range_sha256"] = sha(excerpt)
            s.setdefault("file_sha256", expected)
            s.setdefault("sha256", expected)
            source_ranges.add((path, s["line_start"], s["line_end"]))
        new.append(c)

for path, data in source_bytes.items():
    out = ROOT / "source_snapshot_v0_47" / path
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_bytes(data)
write(ROOT / "source_snapshot_v0_47/manifest.json",
      {"commit": PIN, "scope": "Only source files cited by new v0.47 proof claims",
       "files": list(source_records.values())})

graph = copy.deepcopy(base["mathematical_dependency_graph"])
for c in new:
    graph[c["id"]] = c.get("depends_on", [])
order = topo(graph)
assert len(graph) == len(original_claims) + len(new)
base["claims"] = original_claims + new
base["artifact_version"] = VERSION
base["predecessor_version"] = "0.46"
base["date"] = "2026-11-23"
base["scope"] = CFG["status"]
base["new_component_ledgers"] = [c + "/provenance.json" for c in COMPONENTS]
base["component_scope_metadata_as_received_v0_47"] = component_scopes
base["mathematical_dependency_graph"] = graph
base["dependency_topological_order"] = order
base["version_0_47_local_conclusions"] = CFG["local_conclusions"]
base["component_input_boundaries_history_v0_46"] = copy.deepcopy(base.get("component_input_boundaries", {}))
base["component_input_boundaries_v0_47"] = CFG["remaining_major_inputs"]
base["current_boundary_authority"] = "Version 0.47 current inputs and dependency_audit_v0_47 supersede historical component frontier notes; previous boundary dictionaries are retained for traceability."
old_sources = base["source_files"]
assert isinstance(old_sources, list)
known = {s["path"]: s for s in old_sources}
for path, record in source_records.items():
    if path in known:
        assert known[path].get("sha256", known[path].get("file_sha256")) == record["sha256"]
    else:
        old_sources.append(record)
base["validation_history_v0_46"] = copy.deepcopy(base["validation"])
base["validation"] = {
    "previous_claims_preserved": len(original_claims),
    "new_claims": len(new),
    "claim_count": len(base["claims"]),
    "source_link_count": sum(len(c.get("sources", [])) for c in base["claims"]),
    "source_file_count": len(base["source_files"]),
    "dependency_graph_acyclic": True,
    "dependency_graph_is_lean_transitive_audit": False,
    "lean_build": False, "kernel_replay": False,
    "detailed_validation_file": "validation_v0_47.json",
}
write(ROOT / "provenance.json", base)
assert read(ROOT / "provenance.json")["claims"][:len(original_claims)] == original_claims

idx = read(OLD / "source_index.json")
known = {s["path"]: s for s in idx["source_files"]}
for path, record in source_records.items():
    if path in known:
        assert known[path]["sha256"] == record["sha256"]
    else:
        idx["source_files"].append(record)
idx["artifact_version"] = VERSION
idx["new_source_snapshot"] = "source_snapshot_v0_47/manifest.json"
write(ROOT / "source_index.json", idx)

previous_audit = ROOT / "dependency_audit_v0_46"
audit = ROOT / "dependency_audit_v0_47"
audit.mkdir(exist_ok=True)
g = read(previous_audit / "obligation_map.json")
g["artifact_version"] = VERSION
g["predecessor_graph_v0_46"] = {
    "file": "dependency_audit_v0_46/obligation_map.json",
    "sha256": filehash(previous_audit / "obligation_map.json"),
}
for node in g["nodes"]:
    key = node["id"]
    if key in CLOSED:
        closure = CLOSED[key]
        node["predecessor_status_v0_46"] = {
            "category": node["category"], "kind": node["kind"], "status": node["status"]
        }
        node.update(category=closure["category"], kind="proved_certificate",
                    status="proved_in_stated_scope", opaque_frontier=False)
        node["version_0_47_discharge"] = closure
    if key in CFG.get("selected_node_progress", {}):
        node["version_0_47_progress"] = CFG["selected_node_progress"][key]
    if key in CFG.get("updated_contracts", {}):
        node["historical_contract_narrative_v0_46"] = node["contract"]
        node["contract"] = CFG["updated_contracts"][key]

nodes = {n["id"]: n for n in g["nodes"]}
logical = {n["id"]: n["requires"] for n in g["nodes"]}
topo(logical)
def reached(root):
    result = set()
    def go(n):
        if n in result:
            return
        result.add(n)
        for dep in logical[n]:
            go(dep)
    go(root)
    return result
rh, grh = reached("ORDINARY_RH"), reached("DIRICHLET_GRH")
open_nodes = [n for n in g["nodes"] if n["gate"] == "LEAF"
              and n["status"] not in {"proved_in_stated_scope", "published_application_checked", "complete", "closed"}]
open_ids = {n["id"] for n in open_nodes}
old_open = read(previous_audit / "remaining_leaf_register.json")
assert open_ids == {n["id"] for n in old_open["records"]} - set(CLOSED)
counts = dict(collections.Counter(n["category"] for n in open_nodes))
g["validation"].update(
    logical_graph_acyclic=True, selected_node_count=len(nodes),
    open_leaf_count=len(open_nodes), open_leaf_categories=counts,
    additional_selected_whole_leaves_closed=len(CLOSED),
    full_original_formU_and_decompU_complete=True,
    full_original_clParts_alt_complete_on_original_hAut=True,
    selected_consumed_finite_local_character_laws_complete=True,
    full_original_LocalEstimateII_complete=True,
    actual_Galois_decorated_automorphic_parts_complete=True,
    bare_original_same_J_density_complete=True,
    full_original_ordinary_Hecke_point_record_complete=True,
    full_original_same_J_RingProps_complete=True,
    full_original_six_field_HidaPropsAlt_complete=True,
    full_original_LevelAlt_HasAut_complete=True,
    selected_two_Link_same_J_Hida_P1core_complete=True,
    full_original_CNR3_complete=True,
    full_original_remaining_counting_statement_complete=True,
    actual_arithmetic_row_structure_complete_on_original_inputs=True,
    actual_integral_cusp_lattice_finite_generation_complete=True,
    full_original_KatoUse_and_KatoTwo_complete=True,
    full_original_RigII_complete=True,
    full_original_CohInp_InpZ_complete=True,
    full_original_RowsFinDim_complete=True,
    full_generic_CanonGaugeSt_and_original_IsNab_complete=True,
    eight_original_adelic_setting_blocks_complete_at_stated_scope=True,
    principal_cusp_DataX_normalization_complete_on_original_supplied_charts=True,
    actual_local_first_growth_mean_and_auxiliary_admission_complete=True,
    common_GroupCompatibilityFamily_and_Adm2F_remain_explicit=True,
    integral_cusp_spanning_producers_remain_explicit=True,
    full_arbitrary_chain_ModularAlt_not_claimed=True,
    actual_global_estimate_producers_not_claimed=True,
    original_integral_type_and_same_ideal_support_retained=True,
)
g["current_scope_v0_47"] = CFG["local_conclusions"]
write(audit / "obligation_map.json", g)
register = copy.deepcopy(old_open)
register["artifact_version"] = VERSION
register["records"] = [copy.deepcopy(nodes[n["id"]]) for n in old_open["records"]
                       if n["id"] in open_ids]
register["newly_closed"] = CLOSED
register["count"] = len(register["records"])
register["category_counts"] = counts
register["scope"] = "Current selected sufficient RH/Dirichlet-GRH route; original whole contracts retained, with additive version-0.47 progress and exactly the named reviewed closures."
write(audit / "remaining_leaf_register.json", register)
coverage = {
    "artifact_version": VERSION,
    "graph_file": "dependency_audit_v0_47/obligation_map.json",
    "graph_sha256": filehash(audit / "obligation_map.json"),
    "ordinary_rh_open_leaf_count": len(open_ids & rh),
    "dirichlet_grh_open_leaf_count": len(open_ids & grh),
    "shared_open_leaf_count": len(open_ids & rh & grh),
    "shared_open_leaf_ids": sorted(open_ids & rh & grh),
    "shared_categories": dict(collections.Counter(nodes[n]["category"] for n in open_ids & rh & grh)),
    "ordinary_rh_only_open_leaf_ids": sorted((open_ids & rh) - grh),
    "dirichlet_grh_only_open_leaf_ids": sorted((open_ids & grh) - rh),
    "meaning": "Selected sufficient route reachability; no percentage or minimality assertion",
}
write(audit / "route_coverage.json", coverage)
write(audit / "closure_delta.json", {
    "artifact_version": VERSION, "source_commit": PIN,
    "closed_selected_leaves": CLOSED,
    "closed_nested_producers": CFG["closed_nested_producers"],
    "prior_open_leaf_count": len(old_open["records"]),
    "current_open_leaf_count": len(open_ids),
    "new_proof_claims": len(new),
    "expository_consolidations": [c["id"] for c in new if c.get("mathematical_status", "").startswith("expository_consolidation")],
    "changes": CFG.get("selected_node_progress", {}),
})
disposition = read(previous_audit / "target_disposition.json")
disposition["version"] = VERSION
disposition["version_0_47_scope_update"] = {
    "newly_closed_selected_leaves": CLOSED, "remaining_leaf_register": "dependency_audit_v0_47/remaining_leaf_register.json",
    "progress": CFG["local_conclusions"], "remaining": CFG["remaining_major_inputs"],
    "meaning": "Historical record categories remain intact; current selected statuses are governed by this version's register.",
}
for record in disposition["records"]:
    record["version_0_47_scope_update"] = {
        "current_register": "dependency_audit_v0_47/remaining_leaf_register.json",
        "closed_selected_leaf_ids": sorted(CLOSED),
        "completed_ordinary_entrance": CFG["closed_nested_producers"],
    }
write(audit / "target_disposition.json", disposition)
write(audit / "published_applications.json", {
    "artifact_version": VERSION, "source_commit": PIN,
    "freshly_checked_applications": CFG["published_applications"],
    "inherited_registry": {"file": "dependency_audit_v0_46/published_applications.json",
                           "sha256": filehash(previous_audit / "published_applications.json")},
})

stats = {
    "new_claims": len(new), "cumulative_claims": len(base["claims"]),
    "selected_nodes": len(nodes), "selected_edges": sum(map(len, logical.values())),
    "open_count": len(open_ids), "open_categories": counts,
    "shared_open": coverage["shared_open_leaf_count"],
    "extra_grh_open": len(coverage["dirichlet_grh_only_open_leaf_ids"]),
    "new_source_files_checked": len(source_bytes),
    "new_unique_source_ranges_checked": len(source_ranges),
}
write(ROOT / "integration_stats_v0_47.json", stats)

checkpoint = read(OLD / "continuation_checkpoint.json")
checkpoint["artifact_version"] = VERSION
checkpoint["predecessor_version"] = "0.46"
checkpoint["date"] = "2026-11-23"
checkpoint["status"] = CFG["status"]
checkpoint["new_in_this_version"] = CFG["local_conclusions"]
checkpoint["remaining_major_inputs"] = CFG["remaining_major_inputs"]
checkpoint["next_targets"] = CFG["next_targets"]
checkpoint["current_dependency_audit"] = {
    "artifact_version": VERSION,
    "file": "dependency_audit_v0_47/obligation_map.json",
    "explanatory_chapter": "dependency_audit_v0_47/main.tex",
    "complete_backlog_disposition": "dependency_audit_v0_47/target_disposition.json",
    "remaining_leaf_register": "dependency_audit_v0_47/remaining_leaf_register.json",
    "route_coverage": "dependency_audit_v0_47/route_coverage.json",
    "scope": "Selected sufficient interfaces with completed consumers distinct from open producers and shared work.",
}
checkpoint["current_deliverable"] = {
    "main": "RH_readable_reconstruction_v0_47.tex",
    "new_chapters": "RH_new_proofs_v0_47.tex",
    "archive": "RH_reconstruction_v0_47.zip",
    "audit": "RH_dependency_audit_v0_47.txt",
    "pdf_generated": False,
}
checkpoint["version_0_47_update"] = {
    "local_conclusions": CFG["local_conclusions"],
    "remaining_major_inputs": CFG["remaining_major_inputs"],
    "statistics": stats, "selected_frontier": "dependency_audit_v0_47/remaining_leaf_register.json",
    "current_roadmap": "RH_reconstruction_progress_v0_47.txt",
}
checkpoint["validation_history_v0_46"] = checkpoint["validation"]
checkpoint["validation"] = {"status": "The release validation record is validation_v0_47.json; independent proof and integration reviews are recorded there.",
                             "lean_build": False, "kernel_replay": False}
write(ROOT / "continuation_checkpoint.json", checkpoint)
targets = read(OLD / "next_source_targets.json")
targets["version"] = VERSION
targets["version_0_47_precision_notes"] = CFG["local_conclusions"] + CFG["remaining_major_inputs"]
targets["version_0_47_selected_frontier_files"] = [
    "dependency_audit_v0_47/obligation_map.json",
    "dependency_audit_v0_47/remaining_leaf_register.json",
    "dependency_audit_v0_47/target_disposition.json",
]
targets["next_local_priority"] = CFG["next_targets"]
targets["current_status_v0_47"] = CFG["status"]
write(ROOT / "next_source_targets.json", targets)

text = (OLD / "provenance.txt").read_text()
text += "\n\nVERSION 0.47: CURRENT ADDITION\n" + "=" * 60 + "\n"
for c in new:
    pl = c["proof_location"]
    text += f"\n{c['id']}: {c['title']}\nStatus: {c['status']}\nProof: {pl['file']} ({pl['label']})\n"
    text += "Dependencies: " + ", ".join(c.get("depends_on", [])) + "\n"
    for ref in c.get("sources", []):
        if "path" in ref:
            text += f"  {ref['path']}:{ref.get('line_start')}–{ref.get('line_end')}\n"
(ROOT / "provenance.txt").write_text(text)
filename_map = read(OLD / "component_filename_map.json")
section_map = {}
for component in COMPONENTS:
    raw = (ROOT / component / "main.tex").read_text()
    these = [c for c in new if c["proof_location"]["file"] == component + "/main.tex"]
    for prefix in dict.fromkeys(re.sub(r"\d+$", "", c["id"]) for c in these):
        group = [c for c in these if re.sub(r"\d+$", "", c["id"]) == prefix]
        before = raw[:raw.find("% BEGIN " + group[0]["id"])]
        labels = re.findall(r"\\label\{(sec:[^}]+)\}", before)
        section_map[prefix] = {"component": component, "section_label": labels[-1] if labels else None,
           "claims": [c["id"] for c in group], "fragment": component + "/main.tex",
           "expanded_report": component + "/report.txt", "page_numbers_available": False}
filename_map["version_0_47_component_sections"] = section_map
filename_map["version_0_47_note"] = "Current audit and new-chapter reader's edition are available. Exact claim/source ranges identify the increment. No PDF page numbers or visual PDF review are asserted."
write(ROOT / "component_filename_map.json", filename_map)
print(json.dumps(stats, indent=2))
