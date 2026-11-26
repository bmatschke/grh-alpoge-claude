#!/usr/bin/env python3
"""Rebuild NB source hashes from exact pinned Git blobs; no build/network."""
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
COL = "src/Formalism/LocalToGlobal/Columns/"
HF = "src/Formalism/LocalToGlobal/HermitianForms/"
PI = "src/Formalism/PeriodIntegrals/"
STD = COL + "StdLatUnimodular.lean"
DEC = COL + "DecoFin.lean"
UPL = IW + "ExistsNotMemConjMem.lean"
UP = IW + "InvSmulMem.lean"
DNL = IW + "DownMoveLocalDualLatticeEqLevelPrime.lean"
DNF = IW + "MoveDownLevelFunctionalEq.lean"
DNC = IW + "MoveDownLevelPrimeKeepsChart.lean"
DNA = IW + "MoveDownLevelPrimeAdelicFactorisation.lean"
DNT = IW + "ChartTiedLevelChainHost.lean"

# Every source spec is (path, exact declaration name, optional scope note).
# Human proofs can simplify the Lean argument without asserting identical
# proof terms; scope notes identify those cases and retained suppliers.
CLAIMS = [
    ("NB1", "Paired-prime localization and biduality of Hermitian lattices",
     "Proved by finite-generator denominators, local dual bases and LP1",
     ["LP1"], [
         (PI+"UnimodGenus.lean", "dual"),
         (PI+"UnimodGenus.lean", "IsUnimodular"),
         (PI+"IsoDet.lean", "localization₂"),
         (STD, "hStd"),
         (DEC, "dual_dual"),
         (DEC, "dual_lattice"),
         (DEC, "glue_unimodular", "The readable proof replaces this gluing argument by paired-prime local duality on the same global lattice formulas."),
     ]),
    ("NB2", "Construct the actual up lattice and its exact new residue kernel",
     "Proved for the literal upA/upN/Deco.up, including validity and all local lattice identities",
     ["NB1", "FC1"], [
         (STD, "Deco.Ok"),
         (STD, "Deco.L"),
         (STD, "Deco.Lsh"),
         (STD, "upA"),
         (STD, "upN"),
         (STD, "Deco.up"),
         (DEC, "MoveHyp"),
         (DEC, "upN_spec"),
         (DEC, "Deco.Ok.repl"),
         (DEC, "Deco.Ok.up"),
         (DEC, "Deco.Ok.mem_locP_L"),
         (DEC, "moveHyp_of_ok"),
         (DEC, "T_unif"),
         (UPL, "localization_dual_L_eq_localization_N"),
         (UPL, "localization_L_eq_localization_kerAt"),
         (UPL, "localization_up_L_eq_localization_N"),
         (UPL, "localization_dual_up_L"),
         (UPL, "lattices_at_up"),
     ]),
    ("NB3", "Construct the actual down lattice and the specified quotient functional extension",
     "Proved for literal dnN and TDat.extF; full validity and new dual_P=old L_P",
     ["NB1", "NB2"], [
         (STD, "Deco.kerAt"),
         (STD, "Deco.dnN"),
         (STD, "Deco.dn"),
         (DEC, "Deco.Ok.mem_kerAt"),
         (DEC, "Deco.Ok.dnN_spec"),
         (DEC, "Deco.Ok.dn"),
         (COL+"Record.lean", "modP.ext"),
         (COL+"Record.lean", "modP.ext_spec"),
         (COL+"Record.lean", "modP.ext_of_mem"),
         (COL+"Record.lean", "modP.ext_funAt"),
         (DNL, "extF_eq"),
         (DNL, "ok_dn_extF"),
         (DNL, "locP_Lsh_dn"),
     ]),
    ("NB4", "Actual move validity and raw/preferred coupling-label preservation",
     "Proved including no PtY.mv fallback, preferred normalization and rational-unitary invariance of chosen lift-frame cosets",
     ["NB2", "NB3", "FC1", "FC2", "FC3"], [
         (AM+"PredMemGamRanks.lean", "Ys.Off"),
         (AM+"PredMemGamRanks.lean", "PtY.mv"),
         (AM+"PredMemGamRanks.lean", "ysAt"),
         (AM+"ExtUHInjective.lean", "PtY.mv_spec"),
         (AM+"ExtUHInjective.lean", "mv_up"),
         (AM+"ExtUHInjective.lean", "mv_dn"),
         (AM+"ExtUHInjective.lean", "ysAt_off"),
         (COL+"FiniteSumNonzeroLargeDepth.lean", "frsF"),
         (COL+"FiniteSumNonzeroLargeDepth.lean", "locLat"),
         (COL+"FiniteSumNonzeroLargeDepth.lean", "ybSet"),
         (AM+"LatAtLattice.lean", "GStep.NormalFor"),
         (AM+"LatAtLattice.lean", "cosetIn"),
         (DNC, "SameG"),
         (DNC, "SameG.smul"),
         (DNC, "SameG.dn"),
         (DNC, "cosetIn_eq_of_sameG'"),
         (DNC, "GStep.NormalFor.eq"),
         (DNC, "GStep.exists_normalFor"),
         (DNC, "GStep.prefRep_eq_of_normal"),
         (DNC, "GStep.prefRep_normal"),
         (DNC, "TC.cosetIn_rep_cl_dn_eq"),
         (DNC, "TC.dn_keeps_chart"),
         (IW+"UpKeepsChart.lean", "SameG.up'"),
         (IW+"UpKeepsChart.lean", "TC.cosetIn_rep_up"),
         (IW+"UpKeepsChart.lean", "TC.up_keeps_chart"),
         (IW+"CouplingCosetFramesInvariantRationalUnitary.lean", "cosetIn_smul_unitary"),
         (IW+"PrimeNotMemOfMemQE.lean", "_root_.GlobalTheory.Mem.Col2.T_notMem_QE"),
         (IW+"LevelPrimesNotSelfConjugateDisjointTypeTwist.lean", "primes_atT"),
     ]),
    ("NB5", "Exact moving matrix, transported integral lattices and projection-functional equalities",
     "Proved with gamma=gam(mv), actual quotient representative and denominator cancellation",
     ["NB2", "NB3", "FC5"], [
         (UP, "inv_smul_mem"),
         (UP, "loc_sup_le"),
         (UP, "deco_up"),
         (UP, "sub_mem"),
         (DNL, "mulLat_Lsh_rep"),
         (DNL, "GlobalTheory.Mem.Col2.TC.dn_locP_lat"),
         (DNF, "N_dnPt"),
         (DNF, "f_dnPt"),
         (DNF, "fv_dn"),
         (DNF, "exists_smul_mem_N"),
         (DNF, "GlobalTheory.Mem.Col2.TC.dn_level_functional"),
         (IW+"LevelFunctionalLevelVectorLaws.lean", "fv_mk"),
         (IW+"StepGamMemUJ.lean", "GlobalTheory.Mem.Col2.TC.step_gam_mem_UJ"),
     ]),
    ("NB6", "Supported adelic move with exact inverse-character factorization",
     "Proved from full initial IsPtOf realizability, AD3 and the exact chart-reading data",
     ["NB2", "NB3", "NB4", "NB5", "AD1", "AD3", "FC11"], [
         (IW+"ValuedInvMulLe.lean", "exists_splice", "AD3 and NB retain the initial exists_isPtOf_cm supplier. The finite componentwise splice itself is proved."),
         (IW+"IsPointOfRationalUnitaryAdelicMul.lean", "isPtOf_ratMul"),
         (IW+"IsPointOfRationalUnitaryAdelicMul.lean", "isPtOf_ratAd"),
         (UP, "upAt_spec"),
         (UP, "exists_level"),
         (UP, "isPt_up"),
         (DNA, "coreMove", "Source reverse-splice factorization. NB instead uses a direct AD3 splice under the exposed full-realizer premise, preserving the exact required gamma and character."),
         (DNA, "pointGen", "Source reverse-splice construction; NB obtains the same existential conclusion by direct supported splice under initial realizability."),
         (DNA, "move_down_adelic"),
     ]),
    ("NB7", "Literal UpNatTieG for the actual true-column up move",
     "Proved with exact lattices, projections, embeddings and moving matrix; initial decorated realization remains supplied",
     ["SF2", "FC1", "FC3", "FC5", "NB2", "NB4", "NB5", "NB6"], [
         (HF+"TiedTwLv.lean", "UpNatTieG"),
         (UP, "upNatTie"),
         (IW+"TrueColumnSpacesStandardInFrameCoords.lean", "GlobalTheory.Mem.Col2.TC.spaces_in_coordinates", "Only its previously reconstructed coordinate and identity-on-matrices conclusions are reused here."),
         (IW+"InvMapMulMapMulCancelComplexEmbedding.lean", "GlobalTheory.Mem.Col2.TC.inv_map_mul_map_mul_cancel_complex_embedding"),
         (IW+"InvMapMulMapMulCancelComplexEmbedding.lean", "GlobalTheory.Mem.Col2.TC.tr_eq_of_isTr"),
     ]),
    ("NB8", "Literal DnNatTieG for the actual true-column down move",
     "Proved with the specified nonzero quotient functional and exact inverse character; initial decorated realization remains supplied",
     ["NB3", "NB4", "NB5", "NB6", "NB7", "FC5"], [
         (HF+"TiedTwLv.lean", "DnNatTieG"),
         (DNT, "gl_inv_map_mul_map"),
         (DNT, "tr_eq_of_isTr"),
         (DNT, "dnNatTieG_cols"),
     ]),
]

NEXT = [
    (IW+"ValuedLtOfMem.lean", "unimodGenus",
     "Prove the supplied unramified CM selfdual-lattice genus and its adelic class realization. NB proves neighbor selfduality but does not show that every selfdual decorated lattice has a unitary adelic realizer."),
    (IW+"ValuedLtOfMem.lean", "exists_isPtOf_cm",
     "Construct the initial unitary adele carrying the selfdual lattice with its exact finite type and auxiliary residue maps; combine with AD4's already reconstructed exact rational-frame modification. Expand decoPtSurj_of and reduction_surjective_bis rather than counting this join as a construction."),
    (IW+"LawsOfOk.lean", "laws_of_ok",
     "Construct the literal upstream true-column Laws from Ok by expanding the chain, level, period, zero-class and forms-law suppliers. NB requires those laws and does not use its naturality conclusion to manufacture them."),
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
        start, end = hits[0], hits[0] + 1
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
    for cid, title, status, dependencies, specs in CLAIMS:
        claims.append({
            "id": cid, "title": title, "status": status,
            "introduced_in": "0.14",
            "component_ledger": "neighbor_geometry/provenance.json",
            "dependencies": dependencies,
            "sources": [source_entry(*spec) for spec in specs],
        })
    targets = []
    for path, name, scope in NEXT:
        entry = source_entry(path, name)
        entry.update({
            "priority_group": 1,
            "role": "Retained initial decorated realization or upstream true-column supplier",
            "remaining_human_scope": scope,
            "human_status": "continuation_target_only; no additional proved claim",
        })
        targets.append(entry)

    main_tex, report = out / "main.tex", out / "report.txt"
    ids = re.findall(r"\\paragraph\{(NB\d+):", main_tex.read_text())
    if ids != [c["id"] for c in claims]:
        raise ValueError(("manuscript/ledger claim mismatch", ids))
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
        "lean_build_run": False, "kernel_replay_run": False,
        "pdf_build_run": False,
    }
    ledger = {
        "schema": "RH-readable-component-v1",
        "artifact_version": "0.14",
        "component": "neighbor_geometry",
        "repository": REPOSITORY, "commit": COMMIT, "head_verified": head,
        "scope": "NB1-NB8: actual global up/down lattice formulas, exact residues and preferred coupling labels, full naturality under explicit initial IsPtOf realizability",
        "claims": claims,
        "source_files": list(source_files.values()),
        "mathematical_dependency_edges": [
            [dependency, c["id"]] for c in claims for dependency in c["dependencies"]
        ],
        "input_boundaries": [
            "The actual TC datum, Ok, Pins, supplied Laws and Later remain inputs; their upstream construction is not asserted here.",
            "The chart data ReadsK, IdY, IdV, IdL are exact premises; FC constructs their specified portions with its retained geometric input.",
            "AD3 requires an initial full IsPtOf realizer of each valid raw decorated neighbor. Initial decorated realization remains supplied; AD4 only handles exact frame modification.",
            "The actual type/auxiliary/twist prime sets satisfy the full AD3 disjointness and no-conjugate-pair hypotheses from the supplied prime/selection/twist data.",
            "NB does not rely on FC19 or on the Forms0 up/down clauses being constructed; it supplies their naturality inputs.",
            "Terminal-row incidence and the upstream TC/period laws are not consequences of the neighbor calculation.",
        ],
        "precision_notes": [
            "Hermitian dual localization pairs P with conjugate(P); conjugation is not treated as an endomorphism of O_(P).",
            "The actual global integral submodule formulas upN=A# + conjugate(P)A and dnN=K+P K# are retained.",
            "Off-prime lattice equality and local codimension-one quotients are proved without rank-only inference.",
            "Equality of localizations yields the literal SameAt uniform global scalar witnesses by finite-generator denominator products in both directions.",
            "The actual q=T uniformizer is retained, including the exact type residue f_P(qy).",
            "Down uses the specified g on dnN/P dnN and its literal TDat.extF extension, not an arbitrary nonzero functional.",
            "DecoSet and PtY.mv fallback branches are excluded by proofs of actual validity, unchanged frames and coupling membership.",
            "Preferred chart labels are compared using identical sets of attainable coupling values under every common group action.",
            "Pure rational-unitary invariance uses congruence of chosen auxiliary lift-frames; exact equivariance of arbitrary lift choices is not assumed.",
            "Gamma is the source's exact gam(mv) in every lattice, residue, adelic and frame clause.",
            "L+P H and dnN are identified only after localization at P; their global equality is not used.",
            "Kappa=kappa0^{-1} yields exactly chi(kappa)^{-1}=sigma(chi_column(g0)).",
            "All coefficient and CM embeddings remain the supplied ones, with iota_tau=sigma composed with j_tau.",
        ],
        "simplifications": [
            "Paired-prime duality and equality of all localizations replace the glue_unimodular proof on the same actual global neighbor definitions.",
            "A direct AD3 splice handles both up and down under the retained full-realizer premise; the down source proof uses a reverse splice. The same existential conclusion and chosen gamma/character are proved.",
            "One denominator outside P and exact IdL projection laws replace the longer representative-by-representative functional comparison.",
        ],
        "artifacts": artifacts, "validation": validation,
    }
    out.joinpath("provenance.json").write_text(
        json.dumps(ledger, indent=2, ensure_ascii=False) + "\n")
    out.joinpath("next_targets.json").write_text(json.dumps({
        "version": "0.14", "component": "neighbor_geometry", "commit": COMMIT,
        "targets": targets,
    }, indent=2, ensure_ascii=False) + "\n")
    out.joinpath("source_locators.txt").write_text("\n\n".join(
        c["id"] + " " + c["title"] + "\n" + "\n".join(
            f"  {s['path']}:{s['line_start']}-{s['line_end']} {s['declaration']}\n"
            f"  {s['pinned_url']}\n"
            f"  full_file_sha256={s['full_file_sha256']}\n"
            f"  range_sha256={s['range_sha256']}"
            + (f"\n  scope={s['claim_scope_note']}" if "claim_scope_note" in s else "")
            for s in c["sources"])
        for c in claims) + "\n")
    print(json.dumps(validation, indent=2))
    print("next_targets", len(targets))
    print("main_tex_sha256", artifacts["main.tex"]["sha256"])
    print("report_sha256", artifacts["report.txt"]["sha256"])


if __name__ == "__main__":
    main()
