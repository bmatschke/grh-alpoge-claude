#!/usr/bin/env python3
"""Build CV provenance from exact pinned Git blobs; no Lean build or network."""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import re
import subprocess

COMMIT = "7cbf7a0c32fca1badf05931879a37c3f8a2b03b4"
REPOSITORY = "https://github.com/CocoSgt/riemann-hypothesis-lean"
IW = "src/Development/AbelianVarietyTheory/Proofs/IwasawaDecomposition/"
AM = "src/Development/AbelianVarietyTheory/Definitions/AutomorphicMembership/"
GI = "src/Development/AbelianVarietyTheory/Proofs/GlobalInterpolation/"
SP = "src/Development/AbelianVarietyTheory/Proofs/SatakeParameters/"
COL = "src/Formalism/LocalToGlobal/Columns/"
CF = COL + "CoefficientsModP/"
HF = "src/Formalism/LocalToGlobal/HermitianForms/"
DIV = "src/Formalism/LocalToGlobal/Divisibility/"
VAL = IW + "HermitianChartComplexRationalIntegralForms.lean"
BAS = IW + "IsBasisAtOfIsLocBasis.lean"
ROW = IW + "ExistsEmbFIff.lean"

# Entries are path, declaration, and optionally a scope note. Declaration
# ranges retain exact original newlines; their bytes are hashed separately.
CLAIMS = [
    ("CV1", "Exact frame evaluation, polynomial injectivity and determinant-weight conventions",
     "Proved, including the literal true-column weight/embedding/coordinate identifications",
     ["SF2", "CS2"], [
        (HF+"IsLocBasis.lean", "Frames"),
        (HF+"IsLocBasis.lean", "fnOf"),
        (HF+"IsLocBasis.lean", "shiftOf"),
        (COL+"PolyFn.lean", "fnOf_injective"),
        (COL+"PolyFn.lean", "evFr_injective"),
        (DIV+"CoefMod.lean", "actP"),
        (COL+"PolyFnLemmas.lean", "evFr_actP"),
        (VAL, "cspan_eq"),
        (VAL, "valC_tr"),
        (VAL, "val_tied", "Weight and embedding identities in its first setup block; entire theorem is indexed."),
     ]),
    ("CV2", "Rational polynomial image and exact localized integral Weyl tensor span",
     "Proved with integral Delta retained; characteristic zero is used only for rational Weyl/dual-Weyl equality",
     ["IW3", "CS2"], [
        (VAL, "RatPol"),
        (VAL, "RatPol_shW"),
        (VAL, "exists_VV_of_mem_RatPol"),
        (VAL, "map_mem_RatPol"),
        (COL+"PolyFnLemmas.lean", "dualWeyl_eq_weyl"),
        (COL+"PolyFnLemmas.lean", "nablaSq_eq_delSq"),
        (HF+"TiedStep.lean", "RatSpan"),
        (HF+"TiedStep.lean", "IntSpan"),
        (DIV+"CoefMod.lean", "delStd"),
        (SP+"SmulMemLocPOfVal.lean", "ten_mem_delStd"),
        (SP+"SmulMemLocPOfVal.lean", "delStd_le_span"),
        (SP+"SmulMemLocPOfVal.lean", "smul_mem_localizationAt_of_valuation"),
        (GI+"MemClosureIff.lean", "mem_closure_iff"),
     ]),
    ("CV3", "Construct rational fixed-vector forms from their complex polynomial values",
     "Proved by coefficient lifting and evaluation injectivity; no stabilizer averaging or rank argument",
     ["CV1", "CV2"], [
        (AM+"PredMemGamRanks.lean", "rho"),
        (AM+"PredMemGamRanks.lean", "Fi"),
        (AM+"PredMemGamRanks.lean", "FormsK"),
        (AM+"PredMemGamRanks.lean", "embF"),
        (AM+"ExtUHInjective.lean", "evV_rho"),
        (AM+"ExtUHInjective.lean", "embF_mem"),
        (VAL, "exists_embF_iff"),
     ]),
    ("CV4", "Representative-independent extension to adelic polynomial automorphic functions",
     "Proved explicitly from a double-coset representative bijection and its self-relation",
     ["CV1"], [
        (VAL, "atInf_mul"),
        (VAL, "isUnit_atInf"),
        (VAL, "mem_fiC_iff"),
     ]),
    ("CV5", "Actual decorated-point transport matches stabilizer and adelic level characters",
     "Proved from exact ReadsK point/character/stabilizer clauses, retaining all residue and frame conditions",
     ["CV4"], [
        (AM+"ReferenceCharactersFactorTame.lean", "IsPtOf"),
        (AM+"ReferenceCharactersFactorTame.lean", "IsPtOf.of_extTo"),
        (IW+"IsPointOfRationalUnitaryAdelicMul.lean", "pullV_ratMul"),
        (IW+"IsPointOfRationalUnitaryAdelicMul.lean", "isPtOf_ratMul"),
        (IW+"IsPointOfRationalUnitaryAdelicMul.lean", "isPtOf_ratAd"),
        (IW+"LevOkTwists.lean", "good_of_mem"),
        (IW+"LevOkTwists.lean", "plc_mem"),
        (IW+"LevOkTwists.lean", "levOk_twists", "Only the disjoint auxiliary/twist support consequence is used by CV."),
        (AM+"PredMemGamRanks.lean", "stepY"),
        (AM+"LatAtLattice.lean", "Reads"),
        (AM+"LatAtLattice.lean", "ReadsK"),
        (VAL, "lev_part_smul"),
        (VAL, "stab_inv_iff"),
        (VAL, "val_tied", "Character matching and the Fi clause; entire theorem is indexed."),
     ]),
    ("CV6", "Rational semilocal bases and exact ordinary-dual bases after scalar extension",
     "Proved for the same prescribed primes/embeddings; Hermitian and ordinary duals are kept distinct",
     ["CS3"], [
        (HF+"IsLocBasis.lean", "IsLocBasis"),
        (BAS, "natCast_notMem"),
        (BAS, "isBasisAt_of_isLocBasis"),
        ("src/Formalism/LocalToGlobal/GlobalTheory/GL6/PBwLocGen.lean", "exists_isLocBasis"),
        (DIV+"CoefMod.lean", "tauLat"),
        (DIV+"CoefMod.lean", "dualFr"),
        (CF+"BaseCh.lean", "localized_baseChange_eq_of_localized_eq"),
        (CF+"BaseCh.lean", "bc_isBasisAt"),
        (CF+"PairBDual.lean", "pb_common_den"),
        (CF+"PairBDual.lean", "pb_isBasisAt_dualFr"),
        (VAL, "dualSet_std"),
     ]),
    ("CV7", "Exact localization and frame-value formula for the transported integral Weyl lattice",
     "Proved using integral basis independence and a finite-support LP2 denominator simplification",
     ["CV1", "CV2", "CV6", "CS2", "LP2"], [
        (DIV+"CoefMod.lean", "transLat"),
        (DIV+"CoefMod.lean", "delP"),
        (DIV+"CoefMod.lean", "delAtr"),
        (CF+"NablaIndependenceHolds.lean", "nb_stab_del"),
        (CF+"NablaIndependenceHolds.lean", "nb_indep"),
        (CF+"NablaIndependenceHolds.lean", "nb_sandwich_fam"),
        (CF+"NablaIndependenceHolds.lean", "nb_at_closed"),
        (CF+"NablaIndependenceHolds.lean", "nb_loc"),
        (CF+"NablaIndependenceHolds.lean", "nablaDeltaLocal_holds"),
        (GI+"MemClosureIff.lean", "mem_localization_delAtr"),
        (BAS, "mem_localization_delAtr_fn"),
     ]),
    ("CV8", "One denominator for all classes and the actual localized forms lattice",
     "Proved using actual finite class set and the fixed-vector lattice, with no integral index loss",
     ["CV7"], [
        (AM+"PredMemGamRanks.lean", "latOf"),
        (AM+"PredMemGamRanks.lean", "hlat"),
        (BAS, "mem_localization_latticeOf"),
        ("src/Formalism/LocalRingCardinality/Lemmas.lean", "mem_locW_iff"),
        (ROW, "mem_L_iff"),
     ]),
    ("CV9", "The actual all-prime ValuationCompatibleChart theorem",
     "Proved from exact TC.Ok/Pins/Laws/Later and supplied LevelChart/ReadsK/IdY data; okW is True",
     ["CV3", "CV5", "CV6", "CV7", "CV8", "SF2", "SF4"], [
        (HF+"TiedTwGen.lean", "LevelChart"),
        (HF+"TiedTwGen.lean", "lamTG"),
        (HF+"TiedTwGen.lean", "ValuationCompatibleChart"),
        (AM+"LatAtLattice.lean", "Laws"),
        (AM+"LatAtLattice.lean", "Pins"),
        (AM+"LatAtLattice.lean", "Later"),
        (AM+"LatAtLattice.lean", "IdY"),
        (IW+"TrueColumnSpacesStandardInFrameCoords.lean", "GlobalTheory.Mem.Col2.TC.spaces_in_coordinates"),
        (BAS, "fnOf_eq"),
        (VAL, "val_tied"),
        (IW+"HermitianChartComplexRationalIntegralFormsStatement.lean",
         "_root_.GlobalTheory.T.hermitianChart_complex_rational_integral_forms"),
     ]),
    ("CV10", "Terminal row complex/rational/integral value clauses",
     "Proved for the actual supplied row chart; clsP_tie ipP and NormPTie remain separate metric clauses",
     ["CV1", "CV2", "CV3", "CV4", "CV5", "CV6", "CV7", "CV8"], [
        (ROW, "exists_embF_iff"),
        (ROW, "mem_Fi_iff"),
        (ROW, "rat_iff"),
        (ROW, "lat_iff"),
        (ROW, "natW_shW"),
        (ROW, "VV_shW"),
        (ROW, "delStd_shW"),
        (AM+"ExtUHInjective.lean", "Lsh_empty"),
        (ROW, "clsP_tie",
         "CV10 proves its ptC, rat and lat fields, with exact frame and weight identities. The theorem's chart existence and metric fields belong to FC; this link is not a claim to have proved the whole theorem in CV."),
     ]),
]

NEXT = [
    (IW+"LawsOfOk.lean", "laws_of_ok",
     "Supply the actual I.Laws from I.Ok by expanding its chain, level, period, zero-class and forms-law suppliers. This is an upstream readable-proof target; do not count the record join alone as constructing these laws."),
    (IW+"LawsAll.lean", "laws_all",
     "Reconstruct the coefficient family Ok/basis/norm and level-prime lattice laws on the actual rational forms spaces, retaining exact Hermitian normalization and every all-place lattice identity. CV proves the value clauses, not these stronger family-law suppliers."),
    (IW+"EvLgCanonical.lean", "evLg_canonical",
     "Construct compatible TC.Ok/Pins/IsTw/JetsIn data within the source's precise large-data context, including the field enlargement containing the finite algebraic jet generators and the prescribed selection and character ranges. Keep its EvLg quantifiers and hypotheses; no unconditional global input is inferred."),
]


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--repo", type=Path,
                    default=Path(__file__).resolve().parents[2] / "lean-source")
    ap.add_argument("--out", type=Path, default=Path(__file__).resolve().parent)
    args = ap.parse_args()
    repo, out = args.repo.resolve(), args.out.resolve()
    out.mkdir(parents=True, exist_ok=True)
    head = subprocess.check_output(
        ["git", "-C", str(repo), "rev-parse", "HEAD"], text=True
    ).strip()
    if head != COMMIT:
        raise ValueError(("source HEAD does not match pin", head, COMMIT))

    cache: dict[str, bytes] = {}
    source_files: dict[str, dict] = {}
    decl_prefix = r"^(?:@\[[^\n]*\]\s*)?(?:private\s+)?(?:noncomputable\s+)?"
    boundary = re.compile(
        decl_prefix + r"(?:theorem|lemma|def|abbrev|structure)\s|"
        r"^(?:end(?:\s|$)|namespace\s|section(?:\s|$)|variable\s|attribute\s|"
        r"set_option\s|include\s|omit\s|open\s)"
    )

    def source_entry(path: str, name: str, scope_note: str | None = None) -> dict:
        if path not in cache:
            raw = subprocess.check_output(
                ["git", "-C", str(repo), "show", COMMIT + ":" + path]
            )
            local = repo / path
            present = local.is_file()
            if present and local.read_bytes() != raw:
                raise ValueError(("working tree differs from pinned Git blob", path))
            cache[path] = raw
            source_files[path] = {
                "path": path,
                "sha256": sha256(raw),
                "size_bytes": len(raw),
                "line_count": len(raw.splitlines()),
                "source_read_from_pinned_git_blob": True,
                "working_tree_file_present": present,
                "working_tree_equal_to_pinned_blob_if_present": True,
            }
        raw = cache[path]
        lines = raw.splitlines(keepends=True)
        pattern = re.compile(
            decl_prefix + r"(?:theorem|lemma|def|abbrev|structure)\s+"
            + re.escape(name) + r"(?=\s|\{|\(|:)"
        )
        hits = [i for i, line in enumerate(lines)
                if pattern.match(line.decode("utf-8"))]
        if len(hits) != 1:
            raise ValueError(("declaration lookup not unique", path, name, hits))
        start = hits[0]
        end = start + 1
        while end < len(lines) and not boundary.match(lines[end].decode("utf-8")):
            end += 1
        while end > start + 1 and not lines[end - 1].strip():
            end -= 1
        segment = b"".join(lines[start:end])
        url = f"{REPOSITORY}/blob/{COMMIT}/{path}#L{start+1}-L{end}"
        entry = {
            "path": path,
            "declaration": name,
            "line_start": start + 1,
            "line_end": end,
            "sha256": source_files[path]["sha256"],
            "full_file_sha256": source_files[path]["sha256"],
            "range_sha256": sha256(segment),
            "range_bytes": len(segment),
            "url": url,
            "pinned_url": url,
            "first_line": lines[start].decode("utf-8").rstrip(),
            "declaration_lines_within_range": [start + 1],
            "verified_against_pinned_git_blob": True,
        }
        if scope_note:
            entry["claim_scope_note"] = scope_note
        return entry

    claims = []
    for cid, title, status, dependencies, source_specs in CLAIMS:
        claims.append({
            "id": cid,
            "title": title,
            "status": status,
            "introduced_in": "0.14",
            "component_ledger": "chart_values/provenance.json",
            "dependencies": dependencies,
            "sources": [source_entry(*spec) for spec in source_specs],
        })
    targets = []
    for path, name, scope in NEXT:
        entry = source_entry(path, name)
        entry.update({
            "priority_group": 1,
            "role": "Upstream actual true-column and coefficient-family supplier",
            "remaining_human_scope": scope,
            "human_status": "continuation_target_only; no additional proved claim",
        })
        targets.append(entry)

    main_tex = out / "main.tex"
    report = out / "report.txt"
    manuscript_ids = re.findall(r"\\paragraph\{(CV\d+):", main_tex.read_text())
    expected_ids = [c["id"] for c in claims]
    if manuscript_ids != expected_ids:
        raise ValueError(("manuscript/ledger claim mismatch", manuscript_ids, expected_ids))
    artifacts = {
        p.name: {"sha256": sha256(p.read_bytes()), "size_bytes": p.stat().st_size}
        for p in (main_tex, report)
    }
    validation = {
        "claim_count": len(claims),
        "source_links": sum(len(c["sources"]) for c in claims),
        "source_file_count": len(source_files),
        "all_source_full_files_and_ranges_read_from_pinned_git_blobs": True,
        "all_present_working_tree_files_equal_pinned_blobs": True,
        "manuscript_claim_ids_match_ledger": True,
        "lean_build_run": False,
        "kernel_replay_run": False,
        "pdf_build_run": False,
    }
    ledger = {
        "schema": "RH-readable-component-v1",
        "artifact_version": "0.14",
        "component": "chart_values",
        "repository": REPOSITORY,
        "commit": COMMIT,
        "head_verified": head,
        "scope": "CV1-CV10: actual complex/rational/all-prime integral chart values; terminal row value clauses only",
        "claims": claims,
        "source_files": list(source_files.values()),
        "mathematical_dependency_edges": [
            [dependency, c["id"]]
            for c in claims for dependency in c["dependencies"]
        ],
        "input_boundaries": [
            "The actual TC datum with Ok and Pins, Laws l and Later Z remains supplied; the upstream laws_of_ok and canonical input suppliers are continuation targets.",
            "LevelChart, ReadsK and the identity-on-matrices IdY frame equivalence are exact premises of CV9; their simultaneous source construction is the FC branch.",
            "CV10 takes the actual terminal row chart and ReadsP. It proves ptC/rat/lat, not chart existence or ipP/NormPTie.",
            "No Hermitian norm, Petersson, period, diamond, cohomological or prime-window conclusion is inferred from the value or lattice statements.",
        ],
        "precision_notes": [
            "Integral Weyl Delta remains the coefficient lattice. Delta=nabla is used only over characteristic-zero fields.",
            "The determinant-shifted weight is retained in fnOf even though its natW and integral generator lattice are unchanged.",
            "Frames are all invertible matrices; no orthonormal restriction is used in polynomial injectivity.",
            "The actual coefficient embedding and each CM embedding remain fixed.",
            "Hermitian dual H_c# and ordinary linear dual of j_tau(H_c#) are distinct operations.",
            "The coefficient dual basis j_tau(b)^(-transpose) yields exactly b^(-1) after evaluation, including determinant factors.",
            "All finite-place denominator multipliers lie in the global integer ring and are integral at every other place.",
            "The localized polynomial-lattice equality is proved via LP2 after establishing a common denominator; arbitrary infinite intersections are not silently localized.",
            "The local class-basis quantifier is nonvacuous by semilocal basis existence.",
            "All coefficient places are covered: the source's output okW is identically True.",
            "Rational preimages and common integral denominators are constructed without division by stabilizer order.",
        ],
        "simplifications": [
            "Polynomial injectivity is proved by independent X_tau+s_tau I substitutions.",
            "Finite bad-place support plus LP2 replaces the source's quantitative uniform commensurability proof of nabDelLoc, with the same exact lattice conclusion.",
        ],
        "artifacts": artifacts,
        "validation": validation,
    }
    out.joinpath("provenance.json").write_text(
        json.dumps(ledger, indent=2, ensure_ascii=False) + "\n"
    )
    out.joinpath("next_targets.json").write_text(
        json.dumps({
            "version": "0.14",
            "component": "chart_values",
            "commit": COMMIT,
            "targets": targets,
        }, indent=2, ensure_ascii=False) + "\n"
    )
    out.joinpath("source_locators.txt").write_text(
        "\n\n".join(
            c["id"] + " " + c["title"] + "\n"
            + "\n".join(
                f"  {s['path']}:{s['line_start']}-{s['line_end']} {s['declaration']}\n"
                f"  {s['pinned_url']}\n"
                f"  full_file_sha256={s['full_file_sha256']}\n"
                f"  range_sha256={s['range_sha256']}"
                + (f"\n  scope={s['claim_scope_note']}" if "claim_scope_note" in s else "")
                for s in c["sources"]
            )
            for c in claims
        ) + "\n"
    )
    print(json.dumps(validation, indent=2))
    print("next_targets", len(targets))
    print("main_tex_sha256", artifacts["main.tex"]["sha256"])
    print("report_sha256", artifacts["report.txt"]["sha256"])


if __name__ == "__main__":
    main()
