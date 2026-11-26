#!/usr/bin/env python3
"""Independent, read-only pinned-source and raw-paragraph audit for DC1--DC22."""
from pathlib import Path
import hashlib
import json
import re
import subprocess

HERE = Path(__file__).resolve().parent
VERSION = HERE.parent
COMPONENT = VERSION / "discrete_series_core"
REPO = VERSION.parent / "lean-source"
PIN = "7cbf7a0c32fca1badf05931879a37c3f8a2b03b4"
sha = lambda b: hashlib.sha256(b).hexdigest()

def run():
    ledger_bytes = (COMPONENT / "provenance.json").read_bytes()
    ledger = json.loads(ledger_bytes)
    manifest_bytes = (COMPONENT / "source_manifest.json").read_bytes()
    manifest = json.loads(manifest_bytes)
    main = (COMPONENT / "main.tex").read_bytes()
    report = (COMPONENT / "report.txt").read_bytes()
    cache = {}

    def blob(path):
        if path not in cache:
            cache[path] = subprocess.check_output(
                ["git", "show", f"{PIN}:{path}"], cwd=REPO)
        return cache[path]

    files = []
    for entry in manifest["files"]:
        path = entry["path"]
        data = blob(path)
        assert sha(data) == entry["sha256"], (path, "full-file hash")
        assert len(data) == entry["bytes"], (path, "full-file bytes")
        assert len(data.splitlines()) == entry["line_count"], (path, "lines")
        files.append({"path": path, "bytes": len(data), "sha256": sha(data)})

    markers = list(re.finditer(rb"(?m)^\\paragraph\{(DC\d+):", main))
    paragraphs = {}
    for index, match in enumerate(markers):
        a = match.start()
        z = markers[index + 1].start() if index + 1 < len(markers) else len(main)
        paragraphs[match.group(1).decode()] = {
            "sha256": sha(main[a:z]), "bytes": z-a,
            "line_start": main[:a].count(b"\n") + 1,
            "line_end": main[:z].count(b"\n") + (0 if main[:z].endswith(b"\n") else 1)
        }
    assert set(paragraphs) == {f"DC{i}" for i in range(1, 23)}

    links = 0
    ranges = {}
    claims = []
    claim_files = set()
    for claim in ledger["claims"]:
        cid = claim["id"]
        actual = paragraphs[cid]
        loc = claim["proof_location"]
        assert actual["sha256"] == loc["paragraph_sha256"], (cid, "paragraph hash")
        for field in ("bytes", "line_start", "line_end"):
            assert actual[field] == loc[field], (cid, field, actual[field], loc[field])
        for s in claim["sources"]:
            path = s["path"]
            data = blob(path)
            full = sha(data)
            assert full == s["full_file_sha256"], (cid, path, "source file")
            if "sha256" in s:
                assert full == s["sha256"], (cid, path, "legacy source hash")
            lines = data.splitlines(keepends=True)
            a, z = s["line_start"], s["line_end"]
            assert 1 <= a <= z <= len(lines), (cid, path, "range")
            raw = b"".join(lines[a-1:z])
            assert sha(raw) == s["range_sha256"], (cid, path, "range hash")
            assert len(raw) == s["range_bytes"], (cid, path, "range bytes")
            assert s["source_spelling"] in raw.decode(), (cid, path, "declaration spelling")
            links += 1
            claim_files.add(path)
            ranges[(path, a, z)] = {"path": path, "line_start": a, "line_end": z,
                                    "bytes": len(raw), "sha256": sha(raw)}
        claims.append({"id": cid, "raw_paragraph": actual,
                       "source_link_count": len(claim["sources"])})

    def verify_extra_source(s):
        data = blob(s["path"])
        raw = b"".join(data.splitlines(keepends=True)[s["line_start"]-1:s["line_end"]])
        assert sha(data) == s["full_file_sha256"]
        assert sha(raw) == s["range_sha256"]
        assert len(raw) == s["range_bytes"]
        assert s["source_spelling"] in raw.decode()
        return raw

    inventories = []
    for inventory in ledger["field_inventories"]:
        raw = verify_extra_source(inventory["source"])
        names = re.findall(rb"(?m)^  ([A-Za-z_][A-Za-z_0-9']*)\s*:", raw)
        names = [x.decode() for x in names]
        assert names == inventory["fields"], (inventory["record"], "fields")
        assert len(names) == inventory["field_count"]
        inventories.append({"record": inventory["record"], "fields": names})
    endpoint_links = 0
    for endpoint in ledger["completed_endpoints"]:
        for s in endpoint["sources"]:
            verify_extra_source(s)
            endpoint_links += 1

    result = {
        "result": "PASS", "reviewer": "/root/comparison_span",
        "author": "/root/global_frame", "pin": PIN,
        "scope": "Independent source-byte, source-range, raw-proof paragraph and exact location audit. Mathematical review is a separate companion record.",
        "inputs": {"main.tex": sha(main), "report.txt": sha(report),
                   "provenance.json": sha(ledger_bytes),
                   "source_manifest.json": sha(manifest_bytes)},
        "counts": {"claims": len(claims), "source_links": links,
                   "distinct_source_ranges": len(ranges), "claim_source_files": len(claim_files),
                   "indexed_source_files": len(files), "inventoried_fields": sum(len(x["fields"]) for x in inventories),
                   "completed_endpoint_links": endpoint_links},
        "claims": claims,
        "field_inventories": inventories,
        "source_files": files,
        "source_ranges": list(ranges.values()),
        "limitations": ["No Lean build or kernel replay.", "No modification to sources or reviewed inputs.",
                        "Source verification does not itself prove the mathematical reconstruction."]
    }
    output = HERE / "discrete_series_core_source_audit.json"
    output.write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n")
    print(json.dumps({"result": result["result"], "counts": result["counts"],
                      "output": str(output), "sha256": sha(output.read_bytes())}))

if __name__ == "__main__":
    run()
