#!/usr/bin/env python3
"""Rebuild the v0.40 continuation-note source and component bindings.

This script records audit evidence only. It neither replays Lean nor
modifies any mathematical component or earlier release.
"""
from __future__ import annotations
import argparse
import hashlib
import json
from pathlib import Path
import subprocess

HERE = Path(__file__).resolve().parent
PIN = "7cbf7a0c32fca1badf05931879a37c3f8a2b03b4"
parser = argparse.ArgumentParser()
parser.add_argument("--source", type=Path, default=HERE.parents[1] / "lean_source")
parser.add_argument("--baseline", type=Path, default=HERE.parents[1] / "reconstruction_v039")
parser.add_argument("--components", type=Path, default=HERE.parent)
args = parser.parse_args()

def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()

old = json.loads((args.baseline / "continuation_notes_v0_39" /
                  "next_division_and_readings_sources.json").read_text())
old_by_id = {a["id"]: a for a in old["source_anchors"]}
spec = []
for name in [*(f"P{i:02}" for i in range(1, 10)),
             *(f"R{i:02}" for i in range(1, 7)),
             *(f"T{i:02}" for i in range(1, 9)), "D02"]:
    a = old_by_id[name]
    spec.append((name, a["path"], a["line_start"], a["line_end"], a["description"]))

DEF = "src/Development/AbelianVarietyTheory/Definitions/AutomorphicMembership/"
IWA = "src/Development/AbelianVarietyTheory/Proofs/IwasawaDecomposition/"
DIV = "src/Development/AbelianVarietyTheory/Proofs/DivisorProofs/"
spec += [
    ("G01", DEF+"FieldValuesMemFixedField.lean", 35, 78,
     "Original Dat, RowsAre and forced-place W1; retained common geometric realization"),
    ("G02", "src/Formalism/LocalToGlobal/IndefiniteReal/LinksStage.lean", 290, 309,
     "The nineteen original Inputs fields on the common realization"),
    ("G03", DEF+"StableIffCarrierEq.lean", 63, 100,
     "Keep, Pins, Holds and GeoEx with actual phase/group/geometric guards"),
    ("G04", DEF+"JEvExists.lean", 107, 127,
     "Original GeoHalf and all seven InGeo fields"),
    ("G05", DEF+"NonzeroPlacesOverPrimesLifts.lean", 21, 120,
     "Copy/Coh, common Pre2, full HoldsL and the later same-object St"),
    ("G06", DEF+"ReadPk.lean", 51, 88,
     "Original period, CoreP and RowPk common inputs"),
    ("G07", IWA+"FittingLaterStagesRowIsConstructionState.lean", 22, 29,
     "st_of_fits: original same-stage finite installation interface"),
    ("G08", IWA+"ExistsTransportedStateHeckeGaloisStage.lean", 16, 23,
     "exists_st_copyN: preserves eta/V/S/G and eigenrepresentation while changing N"),
    ("E01", DEF+"NonzeroPlacesOverPrimesOfLifts.lean", 121, 127,
     "St.rowsAre uses the separate eta equality for full ReadL"),
    ("E02", DEF+"StrictHenselianAcyclic.lean", 32, 82,
     "Original LA/LI/LC, universal NEb and eventual SEta contract"),
    ("E03", IWA+"SEta.lean", 21, 41,
     "sEta: PrN/PtSt and actual common arithmetic eigen-theta producer"),
    ("N01", IWA+"GroupTieOfLocalCoefficient.lean", 12, 27,
     "grpTie_of_LC: precise local/level/idempotent/psi field dictionary"),
    ("N02", DIV+"FinRepApply.lean", 109, 125,
     "Actual IsGoodRep and MultEq, distinct from the finite Reps catalogue"),
    ("N03", IWA+"SelectedRealizationSide.lean", 50, 91,
     "recIn_parts_exists: common MultEq/NEb/reciprocity and nonzero/logLam inputs"),
    ("T09", DIV+"ReferenceTupleLiftsSpanAllTuples.lean", 99, 145,
     "placeEx_core and coefficient/level-preserving exists_retie_core"),
    ("T10", DIV+"MLat3OfTie.lean", 15, 16,
     "Original base MLat from the same FWTie; proposed downstream implication"),
    ("T11", DIV+"CovarianceAtConstantXi.lean", 22, 120,
     "exists_scalar_core, covAt_of_xiConst_core and point_identity_core implementation"),
    ("T12", DIV+"ClassSumsSpanCuspFormsBaseTupleSecondField.lean", 361, 363,
     "Exact classSumsSpan_core producer and its classSumsSpan_of_pins_core input"),
    ("D01", "src/Formalism/LocalToGlobal/Divisibility/DivisionCompatibleToSub2Indef2.lean", 233, 311,
     "First ThDef3/DivDef3 versus the six stronger DivRows3 fields"),
    ("D03", IWA+"LiftCuspFormSpaceThetaMapEqData.lean", 128, 172,
     "theta_of and thDef3_thTheta: exact T1/T2 inputs and stronger theta square"),
    ("D04", IWA+"RowLatticesMetricsAgreeOfRealGroupTheorems.lean", 19, 37,
     "Both literal row lattice and metric comparisons"),
    ("D05", IWA+"ZeroSubspaceSpannedByDataZeroSubspaceLifts.lean", 39, 155,
     "Finite orthogonal kernel/range identity and divisionRows_rationalLift"),
    ("D06", IWA+"NumbersEqConcreteNumbersAtBaseLevel.lean", 17, 91,
     "Exact numerical comparison with original MjHTie and IdxDefs"),
    ("D07", IWA+"RationalPairingEqColumnPairing.lean", 23, 94,
     "Coordinate pairing and original BuRational/BtVanish consumer"),
]

source_files = {}
anchors = []
for ident, rel, first, last, description in spec:
    f = args.source / rel
    raw = f.read_bytes()
    if rel not in source_files:
        blob = subprocess.check_output(["git", "-C", str(args.source), "show", f"{PIN}:{rel}"])
        assert raw == blob, rel
        source_files[rel] = sha(raw)
    lines = raw.splitlines(keepends=True)
    assert 1 <= first <= last <= len(lines), (ident, first, last, len(lines))
    section = b"".join(lines[first-1:last])
    anchors.append({
        "id": ident, "description": description, "path": rel,
        "line_start": first, "line_end": last,
        "full_file_sha256": sha(raw), "range_sha256": sha(section),
        "range_bytes": len(section), "source_commit": PIN,
        "verified_equal_to_pinned_git_blob": True,
        "url": f"https://github.com/CocoSgt/riemann-hypothesis-lean/blob/{PIN}/{rel}#L{first}-L{last}",
    })
assert len({a["id"] for a in anchors}) == len(anchors)

bindings = []
component_specs = [
    ("comparison_packet", args.components, [f"PKT{i}" for i in range(1,31)]),
    ("common_readings", args.baseline, ["RDR12", "RDR20", "RDR21", "RDR22"]),
    ("row_integrability", args.baseline, ["RPI14", "RPI15"]),
    ("division_identity", args.baseline, ["DI1", "DI19", "DI20", "DI21"]),
    ("common_selected", args.baseline, ["CSR16", "CSR18", "CSR20", "CSR21", "CSR22"]),
    ("small_level_rank", args.baseline, ["SLR9"]),
    ("base_theta", args.baseline, ["BTH8", "BTH11", "BTH12"]),
    ("global_final_installation", args.baseline, ["GFI15", "GFI16", "GFI17"]),
]
for name, root, claims in component_specs:
    cdir = root / name
    ledger = json.loads((cdir / "provenance.json").read_text())
    indexed = {c["id"]: c for c in ledger["claims"]}
    main = (cdir / "main.tex").read_bytes()
    lines = main.splitlines(keepends=True)
    bound = []
    for ident in claims:
        loc = indexed[ident]["proof_location"]
        raw = b"".join(lines[loc["line_start"]-1:loc["line_end"]])
        assert sha(raw) == loc["sha256"], (name, ident)
        bound.append({"id": ident, "line_start": loc["line_start"],
                      "line_end": loc["line_end"], "proof_range_sha256": sha(raw),
                      "proof_range_bytes": len(raw)})
    files = {}
    for base in ["main.tex", "provenance.json", "closure.json", "published_applications.json"]:
        p = cdir / base
        if p.exists():
            files[base] = {"file": f"{name}/{base}", "sha256": sha(p.read_bytes())}
    bindings.append({"component": name, "scope": "completed only in the component's printed original conditional scope",
                     "origin": "current work_v040 component" if root == args.components else "frozen reconstruction_v039",
                     "files": files, "claims": bound})

note = HERE / "next_division_and_readings.txt"
payload = {
    "schema": "rh-continuation-source-audit/1", "artifact_version": "0.40",
    "note": note.name, "note_sha256": sha(note.read_bytes()),
    "source_commit": PIN,
    "status": "source-grounded proposed next work only; no new proof or whole-leaf closure",
    "formal_proof_assumption": "Pinned Alpoge-Claude Lean proof accepted as fully checked and correct; statuses concern human reconstruction only.",
    "scope": "Common geometry, phase-correct rational tests, actual Fits/eta/local/nonzero producers and second DivRows3 after complete PKT21/27/30.",
    "source_anchors": sorted(anchors, key=lambda a: a["id"]),
    "component_bindings": bindings,
    "validation": {"source_files": len(source_files), "source_ranges": len(anchors),
                   "all_source_files_equal_pinned_git_blobs": True,
                   "component_count": len(bindings),
                   "proof_blocks_verified": sum(len(b["claims"]) for b in bindings),
                   "no_lean_build_or_replay": True},
    "metadata_builder": Path(__file__).name,
}
out = HERE / "next_division_and_readings_sources.json"
out.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n")
print(json.dumps({"note_sha256": sha(note.read_bytes()), "manifest_sha256": sha(out.read_bytes()),
                  **payload["validation"]}, indent=2))
