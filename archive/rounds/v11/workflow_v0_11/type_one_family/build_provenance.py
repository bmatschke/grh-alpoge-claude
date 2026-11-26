"""Rebuild GI1–GI8 provenance from the immutable source checkout.

Writes only this component's provenance.json and source_locators.txt.
Uses original source bytes, inclusive one-indexed ranges, and exact
Git-blob comparison. No network, source edits or Lean compilation.
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
    "SCALE": "src/Formalism/LocalRingCardinality/DataParams₂.lean",
    "SIZE": "src/Formalism/SharpRestriction/ElevenLe.lean",
    "CORE": "src/Formalism/SharpRestriction/FamCore.lean",
    "FAM": "src/Formalism/SharpRestriction/ParConsts.lean",
    "EXTRA": "src/Formalism/LocalRingCardinality/DataExtra.lean",
    "G": GB + "IsResidueClassZero.lean",
    "SMALL": GB + "SmallOrderPrimes.lean",
    "MEAN": GB + "LogarithmicSums/MeanNum.lean",
    "SLOPE": GB + "LogarithmicSums/SlopeEstimateOfLemmaBSlopeLine.lean",
    "JOINT": GB + "Joints.lean",
    "LOCAL": GB + "ProjectionLemmaBaseLevel.lean",
    "DEF": GB + "DefsInst.lean",
    "PLANE": GB + "PlaneCountTheoremWithConstants.lean",
    "FAMNO": "src/Formalism/LocalToGlobal/GroupLattices/AdmissibleFamilyNoKernel.lean",
    "CORNER": GB + "CornerGLContinuity.lean",
    "TOP": GB + "TopChoiceBounds.lean",
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
    # Lean permits an outer anonymous section to run to end of file.
    if any(kind == "namespace" or label is not None for kind, label in stack):
        raise RuntimeError((path, "unclosed named namespace or section", stack))
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


CLAIMS = [
    {
        "id": "GI1", "title": "The exact global Type-I parameter dictionary and minimal numerical data",
        "status": "proved_from_literal_definitions_and_stated_size_fields",
        "dependencies": [],
        "statement": "The actual a,Xprime,bprime,delta1,Y,Yb,lambda,c,I,rho,Q,Nplus,Df have the report's exact formulas. SizeN/SizeK give x^(9/2)<=k<=x^6 and N<=nprime<=n<=x^3; c=16kDelta. Family existence and size fields remain supplied data.",
        "sources": many("SCALE", ["Scale", "L", "b", "a", "X'", "b'", "A", "p0", "delta1", "SizeData₂"], "literal_scale_and_size_data")
            + many("SIZE", ["szTh", "SizeN", "SizeK", "SizeDel", "SizesAt"], "literal_supplied_size_fields")
            + many("G", ["Consts", "Consts.Nonneg", "hG", "KG", "rG", "N1", "Gp", "cG", "L1", "L2", "Nstar", "La", "rho", "Qp", "topsPos", "NplusF", "DIf", "Cand"], "actual_parameter_definitions")
            + many("SMALL", ["HypI", "TypePrimeSizeConds"], "exact_numerical_target_and_source_hypotheses")
            + many("MEAN", ["k_le_x_pow_six", "ord_le_n"]),
    },
    {
        "id": "GI2", "title": "A uniform scalar threshold gives the needed period gap and L2<U directly",
        "status": "proved_without_the_full_NumMean_record",
        "dependencies": ["GI1", "GII2"],
        "statement": "For fixed epsilon,K choose one threshold by GI2.2. The actual logarithmic estimates imply 3Gp<=x^(epsilon/4)<=nprime and L2<514logx<=ceil(x^(epsilon/8))=goodU. These hold before prime/orbit/family-index choices, including an empty L2 defining set.",
        "sources": many("MEAN", ["ev_log", "ev_pow", "rE", "rG_rE", "cGE", "cNE", "cGE_nonneg", "inv_delta1", "one_le_xpow", "Gp_le", "first_count_le_log", "xpow_le_exp", "second_level_lt_good_of_log"])
            + many("TOP", ["segment_count_log_bounds"], "GII2_completed_logarithmic_interface")
            + many("SLOPE", ["NumMean"], "only_Gp_and_second_level_fields_used; full_record_not_assumed")
            + many("CORNER", ["LargeScaleConditions"], "source_geometric_numerical_interface"),
    },
    {
        "id": "GI3", "title": "All first thirteen actual AuxBlock8.HypI inequalities",
        "status": "proved_with_actual_top_count_and_literal_conductor_bound",
        "dependencies": ["GI1", "GI2", "GII1", "GII3", "GJ2"],
        "statement": "For actual candidate Type-I primes and good tops, rho<=x^-2, GJ2 adm5(epsilon/48), and the supplied size fields imply the first thirteen fields. In particular 2I<=bprime/14, kY²YbNlambda loga<=x39<=Xprime, K.kI Nlambda²<=k, and 2YbNlambda<k.",
        "sources": many("SMALL", ["adm1", "adm5", "HypI"], "actual_count_size_and_numerical_definitions")
            + many("MEAN", ["parameter_product_le_arith", "restHypI_ev"], "parallel_source_calculation; report_uses_only_pointwise_rho_and_direct_GI2")
            + many("SLOPE", ["mem_goodReps", "Nv_eq", "RestHypI"], "actual_representatives_and_top_cardinality")
            + many("G", ["Good", "NplusF", "Cand", "goodReps"], "literal_selected_orbit_data")
            + many("TOP", ["uniform_constant_orbits_holds", "family_uniform_constant_holds"], "GII3_completed_actual_count_supply")
            + many("PLANE", ["sizes_bound_of_log_estimates", "family_sizes_bound"], "GJ2_completed_adm5_supply"),
    },
    {
        "id": "GI4", "title": "The literal rounded depth and final exponential size budget",
        "status": "proved_with_source_constants_and_no_depth_replacement",
        "dependencies": ["GI1", "GI2", "GJ2"],
        "statement": "The actual Df is <=x49 and the final source product is <=x86 exp(x^(epsilon/4)/2+4x^(23epsilon/48))<=bprime. Four explicit quarter-budget inequalities absorb the log-polynomial, Q, discriminant and Xprime losses.",
        "sources": many("MEAN", ["b'_eq", "big_le_b'", "DI_arith", "height_bound_product_arith", "restHypI_ev"])
            + many("G", ["cG", "Qp", "DIf"], "literal_normalizations")
            + many("SIZE", ["SizeDel"], "supplied_log_Delta_bound")
            + many("SMALL", ["HypI"], "exact_fourteenth_field"),
    },
    {
        "id": "GI5", "title": "The exact family HypIAt with uniform quantifier order and actual weight windows",
        "status": "proved_for_supplied_FamP_with_positive_KLa_and_FamilyWindowLogBound",
        "dependencies": ["GI2", "GI3", "GI4", "GII3", "GJ2"],
        "statement": "Eventually for every family index, candidate Type-I prime and good representative, L2<U, 3Gp<=nprime, actual AuxBlock8.HypI, and actual wPos weights in winA/winB hold. rho<=rhoB<=x^-2 uses only the family window and rho fields; no prime-band sum is imported.",
        "sources": many("FAMNO", ["hypIAt_ev"], "exact_family_endpoint; report_gives_shorter_direct_numerical_proof")
            + many("CORE", ["FamCore"], "literal_Lx_Leps_family_index_and_unbounded_window_assumptions")
            + many("FAM", ["FamP"], "literal_sizes_fills_rho_le_and_nested_extra_assumptions")
            + many("SIZE", ["SizeBot", "SizeDel", "SizesAt"], "actual_supplied_window_and_conductor_fields")
            + many("G", ["rhoB", "CbLarge", "rho_le_rhoB", "winA", "winB", "wPos", "aL", "bL", "ParametersFill"], "actual_family_normalizations")
            + many("CORNER", ["WindowLogBound", "FamilyWindowLogBound"], "exact_eventual_window_premise")
            + many("PLANE", ["exists_place", "eventually_sizes_admitted", "windows_of"], "parallel_source_supplier; report_reads_relevant_fields_directly")
            + many("JOINT", ["HypIAt"], "exact_target")
            + many("TOP", ["family_log_bound_threshold"], "GII3_completed_uniform_window_supply"),
    },
    {
        "id": "GI6", "title": "The exact global-to-local HypI conversion with the doubled band radius",
        "status": "proved_pointwise_under_literal_global_HypI_and_completed_orbit_geometry",
        "dependencies": ["GI1", "GII1"],
        "statement": "For C0=K.La, CH<=min(K.kI,K.DI),2CH<=K.rho, the literal substitution m=k-1,ccl=floor(c),Dp=Df,cStar=8(Df+1),bl=bprime,bu=bprime+I gives local HypI. The key exact inequality is 2deltaI<=rho; floor and ceiling directions preserve the final depth and size constraints.",
        "sources": many("JOINT", ["ibW", "OrbitSegs", "scale_facts", "hypI_69_to_13"])
            + many("LOCAL", ["EvenGapHyp", "LaI", "deI", "HypI"], "literal_local_hypothesis")
            + many("G", ["InBand0", "InBand", "rho_le_rhoB", "Cand"], "exact_excluded_band_normalization")
            + many("TOP", ["bs_segs", "orbit_segments"], "GII1_completed_actual_segment_geometry")
            + many("SMALL", ["HypI"], "literal_global_hypothesis"),
    },
    {
        "id": "GI7", "title": "Cyclic predecessor identification and exact local-to-global time comparison",
        "status": "proved_for_arbitrary_signed_degrees_with_unchanged_depth",
        "dependencies": ["GI1"],
        "statement": "On every odd selected position dPrev=dMinus is a nonzero distance<nprime and yPrev agrees exactly. If 2C<=K.thresholdOne and C<=K.thresholdTwo, bprime<=a/p and c_local<=c6f imply literal tI<=tIf<=ceil_nat(tIf); no sign condition on the degree functions or leading minimum sum is used.",
        "sources": many("JOINT", ["posAdd_iff", "nearestEven", "tI_le_tIf"])
            + many("LOCAL", ["dPrev", "yPrev", "LaI", "tI"], "literal_local_time")
            + many("G", ["dMinus", "c6f", "tIf", "NplusF", "DIf"], "literal_global_time_and_ceiling"),
    },
    {
        "id": "GI8", "title": "The canonical exceptional mean and explicit global Type-I coefficient vector",
        "status": "proved_using_completed_TC6_and_GJ1; supplied_family_identification_is_explicit",
        "dependencies": ["GI6", "GI7", "GII1", "GJ1", "TC6"],
        "statement": "The exact box restriction/zero-extension bijection transfers TC6's mean to actual kapI and proves adm8 with Cm>=302114. A sufficient fixed vector is K.La>=880; K.kI,K.DI>=2800001; K.rho>=5600002; thresholdOne>=604228; thresholdTwo>=302114. FamP.ex.kapI_def supplies the canonical identification; general Inst requires KapIDef.",
        "sources": many("JOINT", ["sum_boxLoc", "card_boxLoc", "meanLoc_eq", "winA_eq", "winB_eq", "kappa_share_of_least_serving", "type_one_hypothesis_of_segments"])
            + many("G", ["boxLoc", "meanLoc", "winA", "winB"], "exact_product_boxes_and_normalized_mean")
            + many("LOCAL", ["IaZ", "IbZ", "meanKap", "WeightI", "Conclusion2"], "completed_TC6_interface")
            + many("DEF", ["kapISet", "KapIDef", "KapIDef.le", "KapIDef.mem_Icc", "sInf_mem_kapISet"], "GJ1_completed_canonical_infimum_interface")
            + many("EXTRA", ["Extra"], "actual_nested_kapI_def_family_field")
            + many("PLANE", ["KapIDefF", "kapIDefF", "family_kappa_bound", "family_first_bound_of_theorem"], "exact_family_identification_and_application")
            + many("SMALL", ["adm7", "adm8"], "literal_global_certificate_and_mean_endpoints"),
    },
]

ids = {c["id"] for c in CLAIMS}
assert ids == {f"GI{i}" for i in range(1, 9)}
external = sorted({d for c in CLAIMS for d in c["dependencies"] if d not in ids})
def visit(name, path=()):
    if name in path:
        raise RuntimeError("dependency cycle: " + " -> ".join(path + (name,)))
    for child in next(c for c in CLAIMS if c["id"] == name)["dependencies"]:
        if child in ids:
            visit(child, path + (name,))
for name in ids:
    visit(name)

# Verify the report/main claim coverage, display delimiters, and source anchors.
report = (HERE / "report.txt").read_text()
main = (HERE / "main.tex").read_text()
for name in ids:
    assert re.search(r"^" + name + r"\. ", report, re.M), name
assert main.count(r"\[") == main.count(r"\]"), "unbalanced display delimiters"
for claim in CLAIMS:
    for source in claim["sources"]:
        info = next(v for v in FILES.values() if v["path"] == source["path"])
        start, end = source["line_start"], source["line_end"]
        assert 1 <= start <= end <= info["line_count"]
        assert DECL.match(info["_lines"][start - 1].decode("utf-8"))
        assert source["pinned_url"].endswith(f"#L{start}-L{end}")

artifacts = []
for name in ["main.tex", "report.txt", "build_provenance.py"]:
    raw = (HERE / name).read_bytes()
    artifacts.append({"path": name, "sha256": sha256(raw).hexdigest(), "bytes": len(raw)})

payload = {
    "artifact_version": "0.11", "component": "type_one_family",
    "repository": BASE_URL, "commit": COMMIT, "head_verified": actual_head,
    "line_range_convention": "inclusive, one-indexed, original bytes including line endings",
    "claims": CLAIMS,
    "source_files": [{k: v for k, v in f.items() if not k.startswith("_")} for f in FILES.values()],
    "artifacts": artifacts,
    "explicit_external_dependencies": external,
    "derived_simplifications": [
        "The full NumMean package is unnecessary: direct logarithmic estimates prove its two fields used in restHypI_ev.",
        "No prime-band sum is needed for family HypIAt; the pointwise bound rho<=rhoB<=x^-2 follows directly from the supplied window and family rho fields.",
        "Only the displayed SizeN/SizeK/SizeDel fields and the family filling identity are needed for the numeric inequalities; the unused Nm+1 TypePrimeSizeConds field is avoided.",
        "The actual selected-weight windows follow directly from SizeData2 and SizeBot; they are not assumed as a separate local weight condition.",
        "The final exponential budget is the explicit four-quarter inequality after the unchanged source depth is bounded by x49.",
    ],
    "outside_scope": [
        "Construction or existence of the simultaneous FamP arithmetic data, including its supplied size/rho/filling fields.",
        "Type-II numerical supply and actual good-orbit combinatorics are the separate GII component.",
        "The canonical infimum proof and supplied family kapI identification are GJ1; lambda/logQ numerical supply is GJ2.",
        "Aggregate prime sums, global degree-pair selection and global arithmetic/spectral/cohomological RH/GRH endpoints remain separate.",
    ],
    "scope_note": "Complete human proofs of the named actual numerical, reindexing, time and mean interfaces under their literal supplied-family hypotheses and the listed completed dependencies. Source-byte validation is not a Lean build or kernel replay.",
}
(HERE / "provenance.json").write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n")
out = [f"GI1–GI8 exact source locators at {COMMIT}", ""]
for claim in CLAIMS:
    out.extend([claim["id"] + ": " + claim["title"], "Dependencies: " + ", ".join(claim["dependencies"])])
    for source in claim["sources"]:
        out.extend([
            f"  {source['declaration']} | {source['path']}:{source['line_start']}-{source['line_end']} | {source['role']}",
            "    " + source["pinned_url"],
            f"    file sha256 {source['full_file_sha256']} ; range sha256 {source['range_sha256']}",
        ])
    out.append("")
(HERE / "source_locators.txt").write_text("\n".join(out) + "\n")
print(json.dumps({
    "claims": len(CLAIMS), "source_files": len(FILES),
    "locators": sum(len(c["sources"]) for c in CLAIMS),
    "external_dependencies": external, "artifacts": artifacts,
}, indent=2))
