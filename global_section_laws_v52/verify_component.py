#!/usr/bin/env python3
"""Read-only verification of GSL proof/source/hash contracts; no Lean replay."""
from pathlib import Path
import hashlib
import json

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
sha = lambda b: hashlib.sha256(b).hexdigest()
load = lambda n: json.loads((HERE / n).read_text())
provenance = load("provenance.json")
manifest = load("source_manifest.json")
contracts = load("contracts.json")
main = (HERE / "main.tex").read_bytes()
assert sha(main) == provenance["proof_file_sha256"]
assert sha(main) == contracts["proof_file_sha256"]
for c in provenance["claims"]:
    p = c["proof_location"]
    b = b"".join((ROOT / p["file"]).read_bytes().splitlines(keepends=True)
                 [p["line_start"]-1:p["line_end"]])
    assert len(b) == p["bytes"], c["id"]
    assert sha(b) == p["sha256"], c["id"]
for f in manifest["files"]:
    b = (ROOT / f["snapshot_file"]).read_bytes()
    assert len(b) == f["bytes"] and sha(b) == f["sha256"], f["path"]
for r in manifest["ranges"]:
    b = (ROOT / r["snapshot_file"]).read_bytes()
    part = b"".join(b.splitlines(keepends=True)[r["line_start"]-1:r["line_end"]])
    assert sha(b) == r["full_file_sha256"], r["id"]
    assert sha(part) == r["range_sha256"], r["id"]
    assert len(part) == r["range_bytes"], r["id"]
for x in load("inherited_inputs.json")["inputs"]:
    b = (ROOT / x["proof_file"]).read_bytes()
    assert sha(b) == x["proof_file_sha256"], x["id"]
    loc = x["proof_location"]
    part = b"".join(b.splitlines(keepends=True)[loc["line_start"]-1:loc["line_end"]])
    assert sha(part) == x["proof_block_sha256"], x["id"]
for x in load("explicit_inputs.json")["inputs"]:
    if "exact_source_statement_text" in x:
        assert sha(x["exact_source_statement_text"].encode()) == x["statement_sha256"], x["id"]
for c in contracts["completed_original_conditional_laws"]:
    assert c["completed_result"] == "full_original_conditional_implication"
    assert c["global_producer_status"] == "not_globally_supplied_pending_geometric_producers"
    assert sha(c["exact_definition_text"].encode()) == c["definition_sha256"]
assert contracts["global_section_laws_unconditionally_supplied"] is False
assert contracts["selected_whole_obligations_closed"] == []
assert load("closure.json")["globally_supplied_laws"] == []
validation = load("tex_validation.json")
assert validation["status"] == "PASS"
assert validation["proof_file_sha256"] == sha(main)
assert not any(validation["diagnostics"].values())
print(json.dumps({
    "status": "PASS",
    "main_sha256": sha(main),
    "claims": len(provenance["claims"]),
    "source_files": len(manifest["files"]),
    "source_ranges": len(manifest["ranges"]),
    "global_section_laws_unconditionally_supplied": False,
    "no_earlier_files_modified": True,
}, indent=2))
