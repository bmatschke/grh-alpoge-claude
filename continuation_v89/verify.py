#!/usr/bin/env python3
"""Verify the manuscript, upstream source bindings and v0.89 period comparison and corrected heights."""
import argparse
from collections import Counter
from functools import lru_cache
from graphlib import TopologicalSorter
from hashlib import sha256
import json
from pathlib import Path
import re
import subprocess
import sys
from types import ModuleType


ROOT = Path(__file__).resolve().parents[1]
EDITION = "0.89"
DIR = "continuation_v89"
BASE = "87105d2530059535dcbac22470eb9fdce18ecdf1"
PREVIOUS = "CURRENT_CHECKPOINT_v0_88.json"
OLD_GRAPH = "continuation_v88/obligations.json"
REPORT = ROOT / DIR / "validation.json"
INPUT = re.compile(rb"\\input\{([^}]+)\}")


def archived(path):
    return subprocess.check_output(["git", "-C", str(ROOT), "show", f"{BASE}:{path}"])


def archive_json(path):
    return json.loads(archived(path))


def checks():
    # Use exactly the same claim-marker/line-range checks as previous releases.
    path = "continuation_v60/verify.py"
    mod = ModuleType("archived_byte_checks")
    mod.__file__ = str(ROOT / path)
    exec(compile(archived(path), mod.__file__, "exec"), mod.__dict__)
    mod.git = lru_cache(maxsize=None)(mod.git)
    return mod


def historical_ids(core, previous, checkpoint):
    original = archive_json("continuation_v59/claims.json")
    initial = archived(original["predecessor_ledger"])
    core.check(core.blob_id(initial) == original["predecessor_ledger_git_blob"], "wrong historical ledger")
    ids = [c["id"] for c in json.loads(initial)["claims"]]
    ids.extend(c["id"] for item in original["components"] for c in item["claims"])
    for edition in range(60, 89):
        ids.extend(c["id"] for c in archive_json(f"continuation_v{edition}/claims.json")["claims"])
    known = core.distinct(ids, "historical claim IDs")
    core.check(len(known) == previous["mathematical_state"]["cumulative_claims"]
               == checkpoint["predecessor"]["cumulative_claims"] == 4848, "wrong historical claim total")
    return known


def check_graph(core, previous, checkpoint, graph):
    check = core.check
    check(graph["base_commit"] == BASE and graph["base_graph_path"] == OLD_GRAPH, "wrong graph predecessor")
    data = archived(OLD_GRAPH)
    core.digest(data, graph["base_graph_sha256"], OLD_GRAPH)
    old = json.loads(data)
    expected = dict(old, edition=EDITION, base_commit=BASE, base_graph_path=OLD_GRAPH,
                    base_graph_sha256=sha256(data).hexdigest(), closure_groups=[], derived_nodes=[])
    check(graph == expected, "a whole obligation or an original contract changed")
    for key in ("shared_open_ids", "additional_grh_open_ids"):
        check(checkpoint[key] == previous[key] == graph[key], f"wrong open set {key}")
    expected_nodes = graph["nodes"]
    denominator = next(node for node in expected_nodes if node["id"] == "GLOBAL_DENOMINATOR")
    check(denominator["status"] == "proved_in_stated_scope" and "GLOBAL_PERIOD_HEIGHT" in graph["remaining"],
          "wrong denominator or period status")
    nodes = {n["id"]: n["requires"] for n in expected_nodes}
    core.distinct([n["id"] for n in expected_nodes], "graph node IDs")
    check(all(set(req) <= nodes.keys() for req in nodes.values()), "unknown obligation dependency")
    tuple(TopologicalSorter(nodes).static_order())
    state = checkpoint["mathematical_state"]
    counts = dict(Counter(row["category"] for row in graph["remaining_contracts"]))
    check(checkpoint["whole_open_by_class"] == counts, "wrong open counts by class")
    result = {"closed_whole_obligations": [], "derived_nodes": [], "remaining": len(graph["remaining"]),
              "shared": len(graph["shared_open_ids"]), "additional": len(graph["additional_grh_open_ids"]),
              "nodes": len(nodes), "edges": sum(map(len, nodes.values()))}
    for key, field in (("remaining", "whole_open_obligations"), ("shared", "shared_rh_grh_open"),
                       ("additional", "additional_unrestricted_dirichlet_grh_open"), ("nodes", "selected_graph_nodes"),
                       ("edges", "selected_graph_edges"), ("closed_whole_obligations", "new_whole_obligation_closures")):
        check(result[key] == state[field], f"wrong checkpoint field {field}")
    check((result["remaining"], result["shared"], result["additional"], result["nodes"], result["edges"])
          == (9, 9, 0, 121, 161), "wrong selected graph counts")
    return result


def inputs(data):
    # Strip the comment suffix, retaining the escaped percent sign used by TeX.
    data = re.sub(rb"(?<!\\)%[^\n]*", b"", data)
    return [name.decode().removesuffix(".tex") for name in INPUT.findall(data)]


def verify_readers(core, checkpoint, manifest):
    entry = checkpoint["entry_points"]
    expected = {"new_proofs": "RH_new_proofs_v0_89.tex", "new_claims": f"{DIR}/claims.json",
                "whole_obligations": f"{DIR}/obligations.json", "validation": f"{DIR}/validation.json",
                "cumulative_manuscript": "RH_readable_reconstruction_v0_89.tex",
                "previous_claims": "continuation_v88/claims.json"}
    core.check(all(entry[k] == v for k, v in expected.items()), "wrong edition entry points")
    short = core.local_file(entry["new_proofs"])
    cumulative = core.local_file(entry["cumulative_manuscript"])
    chapter = f"{DIR}/chapters"
    core.check(inputs(short).count(chapter) == 1, "supplement does not include its chapters exactly once")
    previous = archive_json(PREVIOUS)["entry_points"]["cumulative_manuscript"]
    original_inputs = inputs(archived(previous))
    core.check(inputs(cumulative) in ([chapter, *original_inputs], [chapter, previous.removesuffix(".tex")]),
               "cumulative reader must include this edition and its intact predecessor chain")
    manuscripts = {c["manuscript"] for c in manifest["claims"]}
    core.check(all(Path(p).parent == Path(DIR) and Path(p).suffix == ".tex" for p in manuscripts),
               "new manuscript outside its edition")
    for local in (ROOT / DIR).glob("*.tex"):
        if re.search(rb"^% BEGIN ", local.read_bytes(), re.M):
            core.check(local.relative_to(ROOT).as_posix() in manuscripts, f"{local.name}: unledgered chapter")
    chapter_inputs = [name + ".tex" for name in inputs(core.local_file(chapter + ".tex"))]
    core.check(core.distinct(chapter_inputs, "chapter inputs") == manuscripts, "reader and ledger chapter mismatch")
    reviews = manifest["reviews"]
    core.check(core.distinct([r["manuscript"] for r in reviews], "reviewed manuscripts") == manuscripts,
               "one review is required for each manuscript")
    core.distinct([r["path"] for r in reviews], "review paths")
    for review in reviews:
        core.check(Path(review["path"]).parent == Path(DIR), "review outside its edition")
        core.check(review["manuscript_sha256"].encode() in core.local_file(review["path"]),
                   f"{review['path']} does not identify its reviewed manuscript bytes")
    return {Path(p).stem: sha256(core.local_file(p)).hexdigest() for p in sorted([*manuscripts, chapter + ".tex"])}


def verify_existing_family(core, previous, current):
    core.check(current["denominator_family"] == previous["denominator_family"],
               "the proved denominator contract or its witnesses changed")


def verify_endpoints(core, claims, current, previous):
    by_id = {claim["id"]: claim for claim in claims}
    proof = current["period_height"]
    complete = dict(previous["period_height"]["complete_entries"], **{"9": "H89V3"})
    core.check(proof["complete_entries"] == complete and proof["other_required_entries"] == [1, 2, 6, 7],
               "incorrect status of the nine period-height entries")
    core.check(proof["partial_entries"]["4"]["rationality"] == "R88L3"
               and proof["partial_entries"]["4"]["spectral_admissibility"] == "R89C1",
               "incorrect Bessel comparison status")
    for field, endpoint in [("complete_height_comparison", "H89V3"), ("base_period_test", "R89C3"),
                            ("chain_factorization", "S89K3"), ("local_integrality_test", "I89M3"),
                            ("quotient_height_decay", "R89D2"), ("fixed_type_finiteness", "R89D3")]:
        core.check(proof[field] == endpoint and endpoint in by_id, f"missing endpoint {field}")
    edges = {key: set(claim["dependencies"]) for key, claim in by_id.items()}
    core.check("H89V1" in edges["H89V2"] and "H89V2" in edges["H89V3"]
               and {"R89C2"} <= edges["R89C3"] and {"S89K1", "S89K2"} <= edges["S89K3"],
               "missing cancelled-height or comparison dependency")
    core.check({"TFR2", "SFS4", "SFS5"} <= edges["R89C1"], "missing original spectral inputs")


def upstream_bytes(core, formal, pin, claims):
    @lru_cache(maxsize=None)
    def lines(path):
        return core.git(formal, "cat-file", "blob", f"{pin}:{path}").splitlines(keepends=True)

    return sum(len(core.inclusive(lines(s["path"]), s["lines"], s["path"]))
               for claim in claims for s in claim["source_ranges"])


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--upstream", "--formal-git", dest="formal", type=Path, metavar="PATH",
                        help="verify every cited source blob and excerpt at the pinned Lean commit")
    parser.add_argument("--write-report", action="store_true",
                        help="write the checked totals and hashes to validation.json; requires --upstream")
    args = parser.parse_args()
    if args.write_report and not args.formal:
        parser.error("--write-report requires --upstream to measure the cited source bytes")
    core = checks()
    previous = archive_json(PREVIOUS)
    current = json.loads(core.local_file("CURRENT_CHECKPOINT_v0_89.json"))
    manifest = json.loads(core.local_file(f"{DIR}/claims.json"))
    graph = json.loads(core.local_file(f"{DIR}/obligations.json"))
    pred = current["predecessor"]
    core.check(pred["checkpoint"] == PREVIOUS and pred["reconstruction_commit"] == manifest["base_commit"] == BASE,
               "wrong base revision")
    core.check(current["mathematical_edition"] == current["package_version"] == manifest["edition"] == graph["edition"]
               == EDITION and previous["mathematical_edition"] == pred["mathematical_edition"] == "0.88",
               "wrong edition")
    pin = manifest["formal_pin"]
    core.check(current["original_source"] == previous["original_source"]
               and pin == current["original_source"]["commit"], "upstream source changed")
    formal = args.formal
    if formal:
        if formal.is_file() and formal.name == ".git":
            formal = formal.parent
        tree = core.git(formal, "rev-parse", pin + "^{tree}").decode().strip()
        core.check(tree == current["original_source"]["tree"], "upstream tree mismatch")

    known = historical_ids(core, previous, current)
    added, ranges, files = core.verify_claims(manifest, known, pin, formal)
    claims = manifest["claims"]
    state = current["mathematical_state"]
    core.check(added == state["new_claims_in_this_package"] and len(known) + added == state["cumulative_claims"],
               "wrong new or cumulative claim count")
    verify_endpoints(core, claims, current, previous)
    verify_existing_family(core, previous, current)
    graph_summary = check_graph(core, previous, current, graph)
    rendered = verify_readers(core, current, manifest)

    stats = {"edition": EDITION, "pin": pin, "predecessor": BASE, "new_claims": added,
             "cumulative_claims": len(known) + added, "source_ranges": ranges, "distinct_pinned_files": files,
             "reviewed_manuscripts": len(manifest["reviews"]), "graph": graph_summary,
             "proof_block_bytes": sum(len(core.inclusive(core.local_file(c["manuscript"]).splitlines(keepends=True),
                                                        c["lines"], c["id"])) for c in claims),
             "rendered_source_sha256": rendered}
    readers = current["entry_points"]
    stats["reader_source_sha256"] = {
        readers[key]: sha256(core.local_file(readers[key])).hexdigest()
        for key in ("new_proofs", "cumulative_manuscript")
    }
    if formal:
        stats["source_excerpt_bytes"] = upstream_bytes(core, formal, pin, claims)
    entry = current["entry_points"]
    report = json.loads(REPORT.read_bytes()) if REPORT.is_file() else {}
    if "new_proofs_pdf" in entry:
        path = entry["new_proofs_pdf"]
        core.check(path == "RH_new_proofs_v0_89.pdf", "wrong short reader PDF")
        data = core.local_file(path)
        core.check(data.startswith(b"%PDF-"), f"{path} is not a PDF")
        pdf = {"tex": entry["new_proofs"], "path": path, "sha256": sha256(data).hexdigest(), "size_bytes": len(data)}
        if args.write_report:
            report.setdefault("short_reader", {}).update(pdf)
        else:
            core.check(all(report["short_reader"][k] == v for k, v in pdf.items()), "short reader PDF mismatch")

    if args.write_report:
        report.update(stats)
        report.setdefault("verification_command", f"python3 {DIR}/verify.py --upstream formal_source")
        temp_path = REPORT.with_suffix(".json.tmp")
        temp_path.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        temp_path.replace(REPORT)
    else:
        core.check(all(report.get(k) == v for k, v in stats.items()), "validation report disagrees with checked edition")
        core.check(type(report.get("source_excerpt_bytes")) is int and report["source_excerpt_bytes"] > 0,
                   "missing upstream byte count")
    mode = "checked against pinned Git bytes" if formal else "indexed; use --upstream to check Git bytes"
    print(f"Verified {added} new claims, {len(known) + added} cumulative claims, 9 open obligations "
          f"(9 shared, 0 additional).")
    print(f"{ranges} source ranges in {files} pinned files ({mode}); {len(manifest['reviews'])} reviewed manuscripts.")


if __name__ == "__main__":
    try:
        main()
    except (OSError, ValueError, TypeError, KeyError, subprocess.CalledProcessError) as exc:
        sys.exit(f"Verification failed: {exc}")
