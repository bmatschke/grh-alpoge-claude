"""Verify the current claim manifests using the byte-range checks shared by rounds 60–90."""
import argparse
from importlib.util import module_from_spec, spec_from_file_location
import json
from pathlib import Path
from urllib.parse import quote
from urllib.request import urlopen


ROOT = Path(__file__).resolve().parents[2]


def component_indexes(manifest, publications, closure):
    """Produce the Galois module's provenance and readable source locators from its claim manifest."""
    pin = manifest["formal_pin"]
    claims, blobs, locators = [], {}, []
    for claim in manifest["claims"]:
        cid = claim["id"]
        sources = []
        locators.append(f"{cid} — {claim['title']}")
        for binding in claim["source_ranges"]:
            path = binding["path"]
            lo, hi = binding["lines"]
            sources.append({"path": path, "lines": [lo, hi]})
            blobs[path] = binding["git_blob"]
            locators.extend([f"https://github.com/CocoSgt/riemann-hypothesis-lean/blob/{pin}/{quote(path)}#L{lo}-L{hi}",
                             f"git blob {blobs[path]}", f"range sha256 {binding['sha256']}"])
        locators.append("")
        published = [item["id"] for item in publications if cid in item["used_in"]]
        claims.append({"id": cid, "tex_anchor": "claim:" + cid, "conclusion": claim["title"],
                       "proof_dependencies": claim["dependencies"] + published, "source_ranges": sources})
    provenance = {
        "source_repository": "CocoSgt/riemann-hypothesis-lean", "source_commit": pin,
        "component": closure["component"], "status": closure["status"], "claims": claims,
        "source_blobs": dict(sorted(blobs.items())), "consumer": closure["formal_consumer"],
        "retained_inputs": closure["retained_foundations"],
    }
    return {"provenance.json": json.dumps(provenance, indent=2, ensure_ascii=False) + "\n",
            "source_locators.txt": "\n".join(locators)}


def verify_claim_records(checkpoint, *, fetch_upstream=False, write_indexes=False):
    path = ROOT / "archive/rounds/v60/continuation_v60/verify.py"
    spec = spec_from_file_location("archived_claim_checks", path)
    checks = module_from_spec(spec)
    spec.loader.exec_module(checks)
    checks.ROOT = ROOT

    pin = checkpoint["formal_source_pin"]
    known = set()
    source_files = {}
    new_indexes = {}
    total_ranges = 0
    for name in checkpoint["claim_manifests"]:
        manifest_path = ROOT / name
        manifest = json.loads(manifest_path.read_bytes())
        checks.check(manifest["formal_pin"] == pin, f"{name}: unexpected formal source revision")
        _, ranges, _ = checks.verify_claims(manifest, known, pin, None)
        total_ranges += ranges
        ids = {claim["id"] for claim in manifest["claims"]}
        known.update(ids)

        inputs = json.loads(manifest_path.with_name("published_inputs.json").read_bytes())
        checks.distinct([item["id"] for item in inputs], f"{name} published inputs")
        for item in inputs:
            uses = checks.distinct(item["used_in"], item["id"])
            checks.check(uses and uses <= ids and item["locators"] and item["url"],
                         f"{item['id']}: missing claim or publication locator")
        closure = json.loads(manifest_path.with_name("closure.json").read_bytes())
        checks.check(closure["source_commit"] == pin, f"{name}: unexpected closure source revision")
        for item in closure["closed_subcontracts"]:
            checks.check(item["claim"] in ids, f"{item['id']}: unknown supplying claim")
        for use in closure.get("consumers", []):
            record = ROOT / use["record"]
            foundations = {item["id"] for item in json.loads(record.read_bytes())}
            consumer = json.loads(record.with_name("provenance.json").read_bytes())
            required = {item["id"]: item["external_input_ids"] for item in consumer["claims"]}
            checks.check(use["supplied_by"] in ids and use["input"] in foundations
                         and use["input"] in required.get(use["claim"], []),
                         f"{use['claim']}: no matching retained input or supplying claim")

        for claim in manifest["claims"]:
            proof = checks.inclusive(checks.local_file(claim["manuscript"]).splitlines(keepends=True),
                                     claim["lines"], claim["id"])
            anchor = f'<span id="claim:{claim["id"]}"></span>'.encode()
            checks.check(proof.count(anchor) == 1, f"{claim['id']}: missing or repeated proof anchor")
            for binding in claim["source_ranges"]:
                source = binding["path"]
                oid, bindings = source_files.setdefault(source, (binding["git_blob"], []))
                checks.check(oid == binding["git_blob"], f"{source}: inconsistent Git blob IDs")
                bindings.append(binding)
        consumer = closure["formal_consumer"]
        checks.check(any(entry["lines"] == consumer["lines"]
                         for entry in source_files.get(consumer["path"], (None, []))[1]),
                     f"{name}: formal consumer has no corresponding source range")
        for index, contents in component_indexes(manifest, inputs, closure).items():
            target = manifest_path.with_name(index)
            if write_indexes:
                new_indexes[target] = contents
            else:
                checks.check(target.read_bytes() == contents.encode(), f"{target.name}: index out of date")
    if fetch_upstream:
        for source, (oid, bindings) in source_files.items():
            url = f"https://raw.githubusercontent.com/CocoSgt/riemann-hypothesis-lean/{pin}/{quote(source)}"
            with urlopen(url, timeout=45) as response:
                raw = response.read()
            checks.check(checks.blob_id(raw) == oid, f"{source}: wrong upstream Git blob")
            lines = raw.splitlines(keepends=True)
            for binding in bindings:
                block = checks.inclusive(lines, binding["lines"], source)
                checks.digest(block, binding["sha256"], f"{source} {binding['lines']}")
    for target, contents in new_indexes.items():
        target.write_text(contents, encoding="utf-8")
    print(f"Checked {len(known)} current manuscript claims and {total_ranges} source bindings "
          f"in {len(source_files)} Lean files" + (" against the pinned upstream bytes" if fetch_upstream else ""))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--fetch-upstream", action="store_true",
                        help="also check the pinned Lean excerpts by downloading their individual source files")
    parser.add_argument("--write-indexes", action="store_true",
                        help="regenerate module provenance and source locators from the verified claim records")
    args = parser.parse_args()
    checkpoint = json.loads((ROOT / "research/register/SELECTED_FAMILY_CHECKPOINT.json").read_bytes())
    verify_claim_records(checkpoint, fetch_upstream=args.fetch_upstream, write_indexes=args.write_indexes)
