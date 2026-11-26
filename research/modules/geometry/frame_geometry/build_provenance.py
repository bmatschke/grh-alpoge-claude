#!/usr/bin/env python3
"""Rebuild source-exact provenance for v0.8 periodic frame geometry.

Every cited full file is compared to the pinned Git blob before its
inclusive declaration range is hashed. No Lean files are changed.
"""
from pathlib import Path
import hashlib
import json
import re
import subprocess

WORK = Path(__file__).resolve().parents[2]
ROOT = WORK / "alpoge-rh"
OUT = Path(__file__).resolve().parent
COMMIT = "7cbf7a0c32fca1badf05931879a37c3f8a2b03b4"
REPO = "https://github.com/CocoSgt/riemann-hypothesis-lean"
GB = "src/Formalism/SharpRestriction/GrowthBounds/"
SC = "src/Formalism/SubspaceCounting/"
assert subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip() == COMMIT
files = {}
cache = {}
TOP = re.compile(
    r"^(?:(?:private\s+)?(?:noncomputable\s+)?"
    r"(?:theorem|lemma|def|structure|abbrev|class|end|namespace|section|variable|include|omit|open|attribute|instance|set_option|local)\b|@\[\s*)"
)


def source(path):
    if path not in cache:
        raw = (ROOT / path).read_bytes()
        pinned = subprocess.check_output(["git", "show", COMMIT + ":" + path], cwd=ROOT)
        assert raw == pinned, ("source differs from pinned Git blob", path)
        lines = raw.decode("utf-8").splitlines(keepends=True)
        cache[path] = (raw, lines)
        files[path] = dict(
            path=path, sha256=hashlib.sha256(raw).hexdigest(),
            bytes=len(raw), line_count=len(lines),
            verified_equal_to_pinned_git_blob=True,
            url=f"{REPO}/blob/{COMMIT}/{path}",
        )
    return cache[path]


def namespace_at(lines, first):
    stack = []
    for line in lines[:first - 1]:
        ns = re.match(r"^namespace\s+(\S+)", line)
        sec = re.match(r"^(?:noncomputable\s+)?section(?:\s|$)", line)
        end = re.match(r"^end(?:\s|$)", line)
        if ns:
            stack.append(("namespace", ns.group(1)))
        elif sec:
            stack.append(("section", ""))
        elif end:
            assert stack, ("unmatched source end", first, line)
            stack.pop()
    return ".".join(value for kind, value in stack if kind == "namespace")


def ref(path, name, role="proof"):
    _, lines = source(path)
    pat = re.compile(
        r"^(?:private\s+)?(?:noncomputable\s+)?"
        r"(?:theorem|lemma|def|structure|abbrev|class)\s+"
        + re.escape(name) + r"(?=[\s{(:])"
    )
    hits = [i for i, line in enumerate(lines) if pat.match(line)]
    assert len(hits) == 1, (path, name, hits)
    first = hits[0] + 1
    last = next((i for i in range(first, len(lines)) if TOP.match(lines[i])), len(lines))
    while last > first and not lines[last - 1].strip():
        last -= 1
    namespace = namespace_at(lines, first)
    qualified = (
        name.removeprefix("_root_.") if name.startswith("_root_.")
        else (namespace + "." if namespace else "") + name
    )
    excerpt = "".join(lines[first - 1:last]).encode("utf-8")
    return dict(
        path=path, declaration=qualified, source_spelling=name,
        line_start=first, line_end=last, role=role,
        sha256=files[path]["sha256"],
        range_sha256=hashlib.sha256(excerpt).hexdigest(),
        range_bytes=len(excerpt),
        url=f"{REPO}/blob/{COMMIT}/{path}#L{first}-L{last}",
    )


def gb(file, name, role="proof"):
    return ref(GB + file + ".lean", name, role)


def w(name, role="proof"):
    return gb("WittFrameLocaliserOrders", name, role)


def b(name, role="proof"):
    return gb("TopChoiceBounds", name, role)


def sc(file, name, role="definition"):
    return ref(SC + file + ".lean", name, role)


claims = []


def claim(cid, title, statement, sources, dependencies=(), status="faithful_translation", note=""):
    claims.append(dict(
        id=cid, title=title, status=status, statement=statement,
        depends_on=list(dependencies),
        assumptions=[
            "n=n'>0 is even; r>=2; the actual application has L1>=1.",
            "The explicitly expanded OrbitHyp, or the stated weaker OrbitRaw data, is supplied. No orbit-abundance premise is inferred from the construction.",
        ],
        proof_location=dict(file="frame_geometry_section.tex", anchors=[cid]),
        expanded_notes=dict(file="report.txt", section=cid),
        source_relation=note,
        sources=sources,
    ))


claim(
    "FG1", "Exact marked-cell, orbit-window and numerical hypotheses",
    "OrbitHyp is expanded into the actual u, ell, M, G′, N1 and three finite conditions: short-window sparsity, cyclic marked-tile coverage and long-window cardinality. It implies u>=1, ell>0 and floor(n/ell)>M+1. The real delta is positive, with no further h/x restrictions needed for this finite consequence.",
    [gb("UnramifiedQuadraticSetting", name, "actual_parameter_definition") for name in
     ["goodU", "goodEll", "orbitSmallMultiplicity", "goodG'", "orbitWindowCount", "IsGoodOrbit"]]
    + [gb("TableLineDegreeFive", "OrbitHyp", "exact_actual_hypothesis"),
       gb("CornerGLContinuity", "OrbitRaw", "general_raw_hypotheses")]
    + [sc("StatementB", name) for name in ["window", "CondA"]]
    + [sc("GoodOrbitIntervalTileCondition", name) for name in
       ["cell", "Marked", "CondTiles", "CondIntervals", "GoodOrbitIntervalTileCondition"]]
    + [gb("ScaleEdges/FramesOf", "de_pos_of"),
       w("bd_goodU_pos"), w("bd_U_le_G'"), b("bc_hyps")],
    note="Every finite premise is stated concretely. CondA counts all selected positions. Orbit abundance and asymptotic size supply are outside this theorem.",
)

claim(
    "FG2", "All marked tiles in one periodic sequence, including the incomplete-period remainder",
    "Sort all marked complete-tile indices s_a and define B_j=n floor(j/J)+ell*s_(j mod J). The next positive cyclic marked-index distance is <=M+1. The wrap adds exactly n-floor(n/ell)*ell, proving ell<=B_(j+1)-B_j<(M+2)ell, periodicity and coverage: the full bf_Seq statement.",
    [w(name, "enumeration_definition_or_proof") for name in
     ["bf_Seq", "bf_MS", "bf_ms", "bf_ms_mem", "bf_ms_lt", "bf_ms_le",
      "bf_ms_surj", "bf_ms_next", "bf_next", "bf_succ", "bf_seq"]],
    dependencies=["FG1"],
    note="The Euclidean-division presentation is the same explicit sequence as the source, including negative indices. It retains the physical remainder at the period wrap.",
)

claim(
    "FG3", "Unique lifted cell tops, parity, isolation and periodicity",
    "Each marked tile has exactly 3r increasing even selected points a_(j,v) in [B_j+(2v+1)u,B_j+(2v+2)u). Every earlier selected point y satisfies y+u<a_(j,v); the analogous right gap also follows. The points shift by n after J tiles. No condition on selected points in unmarked tiles is added.",
    [w(name) for name in
     ["bf_MT", "bf_tp", "bf_tp_spec", "bf_cu", "mul_add_le_of_succ_le",
      "bf_tp_lt", "bf_class", "bf_gap", "bf_card_image",
      "bf_posOf_add", "bf_tp_shift", "bf_top_iff", "bf_MT_of_marked"]]
    + [sc("GoodOrbitIntervalTileCondition", "MarkedRun", "parallel_source_interface")],
    dependencies=["FG1", "FG2"],
    note="The period's evenness is used explicitly to preserve parity under all integer lifts; u is not assumed even. Cell uniqueness supplies the exact bf_tp choices.",
)

claim(
    "FG4", "Middle-block frames and one common marked-tile index for all coordinates",
    "Set f_(j,i)=a_(j,r+i) for i<r and fr(j,i)=B_j for i>=r, exactly bf_F. The frames are selected, even, increasing, ordered and periodic, with no selected point between adjacent entries of one frame. Each frame uses one common marked-tile index, and every marked tile is represented.",
    [gb("SegRing", name, "literal_frame_definition") for name in ["posOf", "Frames"]]
    + [w(name) for name in ["bf_F", "bf_F_fr", "bf_cell", "bf_frames"]]
    + [b("bc_frames", "strong_common_index_statement_and_proof"),
       gb("CornerGLContinuity", "OrbitFrames", "strong_actual_target")],
    dependencies=["FG2", "FG3"],
    note="This proves the stronger existential tile index outside the universal coordinate quantifier, as in bc_frames. The total-function convention for i>=r is included.",
)

claim(
    "FG5", "Exact first/last intermediate tops, strict segment span and stronger L2 gaps",
    "The first r intermediate selected letters are the previous marked tile's final r tops; the last r are the current tile's first r. Thus every source endpoint is even and has gap>u>L2, as does the first current-frame entry. The physical segment span is strictly<(M+3)ell<=G′.",
    [gb("SegRing", name, "literal_segment_and_endpoint_definitions") for name in
     ["letters", "IsW", "LLset", "GapGt", "Valid"]]
    + [w(name) for name in
       ["bf_LL_mem", "bf_LL_first", "bf_LL_last", "bf_LL_key", "bf_gapGt", "bf_frames"]]
    + [b("bc_frames", "source_stronger_endpoint_and_span_conclusion")],
    dependencies=["FG2", "FG3", "FG4"],
    note="The first/last-r predicate is checked with its exact inclusive cardinalities. The argument actually gives at least 2r intermediate points, but preserves the source requirement >=r and every downstream constant.",
)

claim(
    "FG6", "Actual segment cardinality and strict oldest-even-predecessor separation",
    "Reduction is injective on each integer half-open interval of length<=n. CondIntervals and the strict span give |W_j|<=N1. A late selected letter has at least r old-frame even predecessors; if its r-th most recent predecessor were within L1<=L2, the r predecessors would contradict CondA. The source's default-zero oldest branch is unused.",
    [gb("SegRing", "oldest", "literal_sorted_predecessor_definition")]
    + [w(name) for name in
       ["bd_unfold_card", "bd_toNat_lt", "bd_orbit_interval", "bd_letters_card",
        "bd_oldest_far", "bd_fr_strict", "bd_fr_lt", "bd_vectors_before", "bd_gap_mono"]]
    + [b("bc_letters_card"), b("bc_oldest_far")],
    dependencies=["FG1", "FG4", "FG5"],
    note="The shorter half-open interval proof works even for L1=L2, matching bc_oldest_far. The actual OrbitHyp has the stronger 2L1<=L2. No interval length or endpoint is rounded incorrectly.",
)

claim(
    "FG7", "Complete FramesOK and stronger RestFrames construction",
    "Every Valid L1 N1 clause, strict segment span<G′, both stronger L2 endpoint-gap clauses, F.TT=TT, one common marked tile per frame, and coverage of all marked tiles are proved. Hence the literal frames_of and restFrames_proved finite construction conclusions hold from their stated actual or raw hypotheses.",
    [gb("SegRing", "Valid", "complete_validity_conjunction"),
     gb("ScaleEdges/FramesOf", "FramesOK", "exact_cloud_frame_target"),
     gb("ScaleEdges/FramesOf", "frames_of", "exact_actual_application"),
     gb("CornerGLContinuity", "OrbitFrames", "stronger_raw_target"),
     b("RestFrames", "raw_constructor_interface"),
     b("restFrames_proved", "actual_source_constructor"),
     w("bf_restFrames", "parallel_actual_parameter_constructor"),
     w("bd_RestFrames", "parallel_interface")],
    dependencies=["FG1", "FG2", "FG3", "FG4", "FG5", "FG6"],
    note="These exported constructors are conclusions of the expanded proof, not black-box hypotheses. This does not claim the other OrbitPositionsAndSizeBounds or PathPairCorrespondence clauses.",
)

claim(
    "FG8", "Frame-count and segment-cardinality bounds, with the supplied-orbit boundary",
    "The constructed frame satisfies 3rJ<=|TT| by disjoint marked tiles. The exact downstream bound Jr<=|TT| also holds for every Valid periodic frame by injecting its entries in one period. The constructed segments have |W_j|<=min(N1,|TT|), so the unchanged standard Ns=min(N1,2|TT|) is valid. None of these assertions proves abundance of OrbitHyp.",
    [sc("GoodOrbitIntervalTileCondition", "Marked", "exact_tile_occupancy")]
    + [w(name) for name in
       ["bf_MS", "bf_seq", "bf_F", "residue_position_injective_window",
        "frame_row_monotone", "frame_entries_strictMono", "frame_last_lt_next_first",
        "frame_entry_lt_of_lt", "frame_count_mul_le_tops"]]
    + [gb("TableLineDegreeFive", "OrbitHyp", "supplied_orbit_boundary"),
       gb("CornerGLContinuity", "OrbitSizeBounds", "separate_size_input_not_claimed"),
       sc("GoodOrbitIntervalTileCondition", "TileConditionFailureProbBound",
          "separate_abundance_input_not_claimed")],
    dependencies=["FG1", "FG2", "FG3", "FG4", "FG5", "FG6", "FG7"],
    status="derived_simplification",
    note="The 3rJ and min(N1,|TT|) refinements are explicitly derived and not substituted into downstream source constants. The source's exact Jr bound is also proved independently for a general Valid periodic frame.",
)

out = dict(
    schema_version="1.2", artifact_version="0.8", date="2026-11-21",
    owner="/root/lean_audit",
    repository=dict(url=REPO, commit=COMMIT),
    range_convention="One-indexed inclusive declaration ranges; full source bytes are compared with the pinned Git blob and unnormalized range bytes are hashed.",
    verification=dict(
        full_file_bytes_compared_with_pinned_git_blob=True,
        range_bytes_hashed_without_normalization=True,
        human_mathematical_proofs_supplied=True,
        lean_source_files_edited=False,
        local_lean_compilation=False,
        lean_kernel_replay=False,
        replacement_arguments_formalized=False,
    ),
    status_definitions=dict(
        faithful_translation="A complete human proof or explicit expansion of the precise cited source assertion under the stated finite hypotheses.",
        derived_simplification="An explicitly proved strengthening or shorter consequence with its source counterpart and unchanged application constants identified.",
        remaining_input="An unexpanded specialized input. No FG construction claim uses this status; global orbit abundance and numerical compatibility remain outside scope.",
    ),
    independent_reviews=[dict(reviewer="/root/readable_sources", scope="FG2 cyclic wrap; FG3 isolation; FG5 endpoints and strict span; FG6 oldest half-open interval", result="No correction found. The physical wrap remainder and oldest interval at equality are handled correctly.")],
    claims=claims,
    files=[files[path] for path in sorted(files)],
    outside_scope=[
        "Abundance of good subsets/orbits satisfying OrbitHyp and construction of the actual globally chosen TT.",
        "Asymptotic OrbitSizeBounds and simultaneous large-constant/degree/chain compatibility for the full Type-II family.",
        "The separate Type-I construction and global RH/Dirichlet-GRH analytic and cohomological inputs.",
    ],
)
(OUT / "provenance.json").write_text(json.dumps(out, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
(OUT / "source_manifest.json").write_text(
    json.dumps(dict(repository=out["repository"], files=out["files"]), ensure_ascii=False, indent=2) + "\n",
    encoding="utf-8",
)
locators = []
for c in claims:
    locators += [c["id"] + ": " + c["title"], "Status: " + c["status"]]
    for s in c["sources"]:
        locators += [
            "  " + s["declaration"], "  " + s["url"],
            "  full-file SHA256 " + s["sha256"],
            "  inclusive-range SHA256 " + s["range_sha256"],
        ]
    locators.append("")
(OUT / "source_locators.txt").write_text("\n".join(locators), encoding="utf-8")
print(json.dumps(dict(
    claims=len(claims),
    source_files=len(files),
    source_references=sum(len(c["sources"]) for c in claims),
    statuses={status: sum(c["status"] == status for c in claims) for status in out["status_definitions"]},
    every_source_byte_checked_against_pin=True,
)))
