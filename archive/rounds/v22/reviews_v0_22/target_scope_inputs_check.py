#!/usr/bin/env python3
"""Read-only checks for the current v0.22 scope review; no source/build audit."""
from pathlib import Path
import hashlib
import json

ROOT = Path(__file__).resolve().parent.parent
sha = lambda b: hashlib.sha256(b).hexdigest()

def check():
    names = ["increment_v0_22.json", "next_source_targets.json",
             "RH_readable_reconstruction_v0_22.tex",
             "automorphic_realization/report.txt",
             "quantitative_weil_dictionary/report.txt",
             "discrete_series_core/report.txt", "simultaneous_prime_pairs/report.txt",
             "ray_prime_estimates/report.txt",
             "history/version_0_21/next_source_targets.json"]
    raw = {name: (ROOT/name).read_bytes() for name in names}
    increment = json.loads(raw[names[0]])
    targets = json.loads(raw[names[1]])
    old = json.loads(raw[names[-1]])
    branches = targets["global_branches_unchanged"]
    assert len(branches) == len(old["global_branches_unchanged"]) == 4
    assert branches == old["global_branches_unchanged"]
    branch_checks = []
    for index, (new, prior) in enumerate(zip(branches, old["global_branches_unchanged"]), 1):
        canonical = lambda x: json.dumps(x, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode()
        assert canonical(new) == canonical(prior)
        branch_checks.append({"branch": index, "identical_json_record": True,
                              "canonical_sha256": sha(canonical(new)),
                              "claim_ids": new["claim_ids"]})
    assert targets["target_count"] == len(targets["targets"])
    keys = {t["path"]+":"+t.get("source_spelling", t["declaration"].rsplit(".", 1)[-1])
            for t in targets["targets"]}
    retired = increment["replaced_target_keys"]
    assert not (set(retired) & keys), (set(retired) & keys)
    main = raw["RH_readable_reconstruction_v0_22.tex"].decode()
    marker = "\\textbf{What version 0.22 achieves.}"
    a = main.index(marker)
    b = main.index("\\end{minipage}", a)
    c = main.index("The arithmetic window theorem remains the main unfinished obligation")
    z = main.index("\\section{Claim ledger and reading order}", c)
    fragments = {}
    for name, x, y in [("current_front_summary", a, b), ("current_remaining_and_next_target", c, z)]:
        fragment = main[x:y].encode()
        fragments[name] = {"sha256": sha(fragment), "bytes": len(fragment),
                           "line_start": main[:x].count("\n")+1,
                           "line_end": main[:y].count("\n") + (0 if main[:y].endswith("\n") else 1)}
    # These are descriptive structural checks, not proofs of the targets.
    required_scope_tokens = ["critical", "Choice.FieldOK", "NTh", "VWinAt",
                             "CN", "BD", "HD", "Harish", "Tamagawa", "GapHyp"]
    scopes = json.dumps(increment, ensure_ascii=False) + json.dumps(targets, ensure_ascii=False)
    assert all(token in scopes for token in required_scope_tokens)
    result = {"result": "PASS", "scope": "Input identity, four protected branch records, retired keys, and current-text locations only.",
              "input_sha256": {name: sha(b) for name,b in raw.items()},
              "input_bytes": {name: len(b) for name,b in raw.items()},
              "protected_global_branch_records": branch_checks,
              "target_count": len(targets["targets"]),
              "retired_key_count": len(retired), "retired_keys_absent_from_active_targets": True,
              "retired_scopes": retired, "current_text_fragments": fragments,
              "no_input_writes": True}
    out = ROOT / "reviews_v0_22/target_scope_inputs_check.json"
    out.write_text(json.dumps(result, indent=2, ensure_ascii=False)+"\n")
    print(json.dumps({"result":result["result"], "target_count":result["target_count"],
                      "retired_key_count":len(retired), "input_sha256":result["input_sha256"],
                      "output":str(out), "sha256":sha(out.read_bytes())}, indent=2))

if __name__ == "__main__":
    check()
