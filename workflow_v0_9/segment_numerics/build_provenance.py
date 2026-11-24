"""Rebuild SW12 provenance from the pinned, byte-identical Lean checkout.

Writes only this component's provenance.json and source_locators.txt.
No network, Lean edits, compilation or kernel replay. Inclusive ranges
retain their original bytes and line endings. Requires Python 3.11+.
"""
from pathlib import Path
from hashlib import sha256
import json
import re
import subprocess

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[1] / "alpoge-rh"
COMMIT = "7cbf7a0c32fca1badf05931879a37c3f8a2b03b4"
BASE_URL = "https://github.com/CocoSgt/riemann-hypothesis-lean"
GB = "src/Formalism/SharpRestriction/GrowthBounds/"
PATHS = {
    "STD": GB + "BinomialRatio/Transported.lean",
    "OBJ": GB + "ObjSeg.lean",
    "LOC": GB + "ColumnSystems.lean",
    "GEOM": GB + "BinomialRatio/SegmentStatementHolds.lean",
    "CAP": GB + "CoarseMultiplicity/PolyUpperBoundDelta.lean",
    "TOP": GB + "BinomialRatio/TopDegreeLeTwoB.lean",
    "NUM": GB + "BinomialRatio/CoarseDegreeAlternative.lean",
    "BL": GB + "CoarseMultiplicity/CoarseMultiplicityAtIdentity.lean",
    "OPLUS": GB + "CoarseMultiplicity/OPlusAtOf.lean",
    "OTARGET": GB + "CoarseMultiplicity/WeightWLet.lean",
}

PREFIX = r"(?:@\[[^\n]*\]\s*)?(?:(?:private|protected|noncomputable)\s+)*"
DECL = re.compile(r"^" + PREFIX + r"(?:def|theorem|lemma|abbrev|structure|inductive|instance)\s+(\S+)")
BOUNDARY = re.compile(r"^" + PREFIX + r"(?:def|theorem|lemma|abbrev|structure|inductive|instance|namespace|end|section|variable|attribute|open|include|set_option)\b")
NS = re.compile(r"^namespace\s+(\S+)")
SEC = re.compile(r"^(?:noncomputable\s+)?section(?:\s+(\S+))?\s*$")
END = re.compile(r"^end(?:\s+(\S+))?\s*$")

actual_head = subprocess.check_output(["git", "-C", str(REPO), "rev-parse", "HEAD"], text=True).strip()
if actual_head != COMMIT:
    raise RuntimeError(f"Source checkout is {actual_head}, expected {COMMIT}")

FILES = {}
for key, path in PATHS.items():
    raw = (REPO / path).read_bytes()
    pinned = subprocess.check_output(["git", "-C", str(REPO), "show", f"{COMMIT}:{path}"])
    if raw != pinned:
        raise RuntimeError(f"Working tree differs from pinned bytes: {path}")
    lines = raw.splitlines(keepends=True)
    stack, declarations = [], []
    for i, rawline in enumerate(lines):
        line = rawline.decode("utf-8").rstrip("\r\n")
        if m := NS.match(line):
            stack.append(("namespace", m.group(1)))
        elif m := SEC.match(line):
            stack.append(("section", m.group(1)))
        elif m := END.match(line):
            if not stack:
                raise RuntimeError((path, i + 1, "unmatched end"))
            kind, label = stack.pop()
            if m.group(1) and m.group(1) != label:
                raise RuntimeError((path, i + 1, "end mismatch", label, m.group(1)))
        elif m := DECL.match(line):
            namespace = ".".join(label for kind, label in stack if kind == "namespace")
            name = m.group(1)
            declarations.append({"name": name, "line": i,
                                 "qualified": f"{namespace}.{name}" if namespace else name})
    FILES[key] = {
        "path": path, "full_file_sha256": sha256(raw).hexdigest(),
        "bytes": len(raw), "line_count": len(lines),
        "verified_equal_to_pinned_git_blob": True,
        "_lines": lines, "_declarations": declarations,
    }


def locator(key, name, role="parallel_source_proof", occurrence=0):
    info = FILES[key]
    hits = [d for d in info["_declarations"] if d["name"] == name]
    if occurrence >= len(hits):
        raise RuntimeError((key, name, occurrence, "declaration not found"))
    decl = hits[occurrence]
    start = decl["line"]
    lines = info["_lines"]
    end = start + 1
    while end < len(lines) and not BOUNDARY.match(lines[end].decode("utf-8")):
        end += 1
    while end > start + 1 and not lines[end - 1].strip():
        end -= 1
    excerpt = b"".join(lines[start:end])
    if role == "parallel_source_proof" and re.match(r"^" + PREFIX + r"(?:def|abbrev|structure)\b", lines[start].decode("utf-8")):
        role = "definition_or_statement"
    return {
        "path": info["path"], "declaration": decl["qualified"],
        "source_spelling": name, "line_start": start + 1, "line_end": end,
        "role": role, "full_file_sha256": info["full_file_sha256"],
        "range_sha256": sha256(excerpt).hexdigest(), "range_bytes": len(excerpt),
        "pinned_url": f"{BASE_URL}/blob/{COMMIT}/{info['path']}#L{start+1}-L{end}",
    }


def many(key, names, role="parallel_source_proof"):
    return [locator(key, name, role) for name in names]


CLAIMS = [{
    "id": "SW12",
    "title": "Literal Std gives BLk(0), the exact OPlus bound and the complete t0 order estimate",
    "status": "proved_by_elementary_geometric_cap_estimates_and_exact_segment_summation",
    "dependencies": [],
    "statement": "Under Std(C0,Cde,CE1,CE2,1,X), every actual kept block satisfies BLk(E=0) and oPlus<=localOrderCap<=147a/250<=aPlus. Every kept family has sum blockOrd<=X.t0(C0,Ct) for Ct>=30; this last assertion works with arbitrary H in Std. The universal parameter supply HIext=>Std and t0<=expanded tI are not asserted.",
    "sources": many("STD", ["be", "Std"], "literal_hypotheses_and_parameters")
        + many("LOC", ["Loc", "k", "N", "Q", "La", "de", "E0", "t0", "seg"], "literal_local_objects")
        + many("OBJ", ["SegData", "SegBlock", "SegData.P", "SegData.Qj", "SegData.A0", "coarseA", "coarseC", "oEff", "cap", "Oplus", "DigitsOK", "Kept", "blockOrd", "cdist", "evenTops", "numSeg", "segStart", "segNext", "segG", "segDists", "segS", "segPos", "segData", "segATop", "segAPlus", "t0G4"], "literal_segment_blocks_and_order")
        + many("GEOM", ["cd_cases", "dist_pos_lt", "dist_odd", "segG_even", "dist_strictMono", "sigma_iff", "oddSet_disj", "sum_segS"], "cyclic_geometry_and_exact_count")
        + many("NUM", ["coarse_bounds", "eps", "Std.eps_ge", "Std.kQ", "Std.kQeps", "Std.levels"], "coarse_quotient_and_scale_bounds_proved_in_report")
        + many("CAP", ["poly_upper_bound_delta", "poly_lower_bound_delta", "upper_real_bound", "SegHyp.geo", "Std.forty_epsilon_le_delta", "Std.be18", "Std.Laeps", "Std.twoP", "kept_upper_level_bound", "extra_order_le_maximal", "maximal_order_le_a", "keptBL_of_std"], "exact_late_cutoff_and_BLk_targets; report_strengthens_maximal_order_to_147a_over_250")
        + many("TOP", ["coarseA_mul", "cap_le", "base_exponent_le_a", "SegHyp", "SegHyp.top_degree_le_two_b", "mul_sum_pow_lt_le_pow_of_segHyp", "SegHyp.Pcap", "errTop", "SegHyp.de0", "SegHyp.top_ord", "Rerr", "SegHyp.dig", "SegHyp.oplus", "SegHyp.seg_ord", "segHyp_of", "ord_all"], "exact_pointwise_and_total_order_targets")
        + many("BL", ["localOrderCap", "BLk"], "literal_lift_numerical_interface")
        + many("OTARGET", ["OPlusAt"], "source_universal_statement; human_proof_conditional_on_explicit_Std_supply")
        + many("OPLUS", ["oPlusAt_of"], "parallel_source_conditional_assembly; report_uses_shorter_geometric_bound"),
}]

artifacts = []
for name in ["report.txt", "main.tex", "build_provenance.py"]:
    raw = (HERE / name).read_bytes()
    artifacts.append({"path": name, "sha256": sha256(raw).hexdigest(), "bytes": len(raw)})

assert len(CLAIMS) == 1 and CLAIMS[0]["id"] == "SW12"
assert CLAIMS[0]["dependencies"] == []
payload = {
    "artifact_version": "0.9",
    "component": "segment_numerics",
    "claims": CLAIMS,
    "repository": BASE_URL,
    "commit": COMMIT,
    "head_verified": actual_head,
    "line_range_convention": "inclusive, one-indexed, original bytes including line endings",
    "source_files": [{k: v for k, v in info.items() if not k.startswith("_")} for info in FILES.values()],
    "artifacts": artifacts,
    "explicit_external_dependencies": [],
    "reused_completed_inputs": {},
    "derived_simplifications": [
        "The odd-distance geometric series gives P_i cap_i<=a/p^d_i+2b'/p directly.",
        "The cap geometric series proves localOrderCap<=147a/250, strengthening the archival <=a and shortening OPlusAt_of.",
        "Explicit five-term error coefficients permit 6(s+1)R, but the human endpoint retains the archival 30(s+1)R and Ct>=30.",
    ],
    "outside_scope": [
        "Uniform HIext/D1num/CBound to Std implication and quantified threshold supply thr_std.",
        "The comparison X.t0(C0,Ct)<=the expanded final Type-I loss tI.",
        "Global parameter supply and the other arithmetic, spectral and cohomological branches toward RH/GRH.",
    ],
    "scope_note": "SW12 is a complete human reconstruction of the three literal-Std numerical interfaces consumed by RL. No probability, rank or representation input is used. SW10 is compatible earlier work but not an external dependency. No Lean build or kernel replay is asserted.",
}
(HERE / "provenance.json").write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n")
lines = [f"SW12 segment-numerics provenance at {COMMIT}", ""]
for claim in CLAIMS:
    lines.extend([f"{claim['id']}: {claim['title']}", f"Status: {claim['status']}",
                  "Dependencies: " + ", ".join(claim["dependencies"])])
    for src in claim["sources"]:
        lines.append(f"  {src['declaration']} | {src['path']}:{src['line_start']}-{src['line_end']} | {src['role']}")
        lines.append(f"    {src['pinned_url']}")
        lines.append(f"    file sha256 {src['full_file_sha256']} ; range sha256 {src['range_sha256']}")
    lines.append("")
(HERE / "source_locators.txt").write_text("\n".join(lines) + "\n")
print(json.dumps({"claims": len(CLAIMS), "source_files": len(FILES),
                  "locators": sum(len(c["sources"]) for c in CLAIMS),
                  "verified_commit": COMMIT, "artifacts": artifacts}, indent=2))
