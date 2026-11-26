#!/usr/bin/env python3
"""Build exact pinned-source and written-proof provenance for RV1--RV7."""
from pathlib import Path
import argparse
import hashlib
import json
import re
import subprocess

HERE = Path(__file__).resolve().parent
parser = argparse.ArgumentParser()
parser.add_argument("--repo", type=Path, default=HERE.parents[1] / "lean-source")
REPO = parser.parse_args().repo
PIN = "7cbf7a0c32fca1badf05931879a37c3f8a2b03b4"
BASE = "src/Development/AutomorphicArithmetic/AutomorphicVarieties/"
FML = "src/Formalism/GaloisCohomology/"
FOUND = "src/Development/AbelianVarietyTheory/Proofs/FoundationProofs/"
INERTIA = "src/Development/AbelianVarietyTheory/Proofs/InertiaEigenvalues/"
cache = {}


def sha(data):
    return hashlib.sha256(data).hexdigest()


def source(path, spelling, role="exact source endpoint or matched definition"):
    raw = (REPO / path).read_bytes()
    lines = raw.splitlines(keepends=True)
    starts = []
    pattern = (r"^(?:(?:private|protected|noncomputable)\s+)*"
               r"(?:def|abbrev|theorem|lemma|structure|class|instance)\s+([^\s:{(]+)")
    for i, line in enumerate(lines, 1):
        match = re.match(pattern, line.decode())
        if match:
            starts.append((i, match.group(1)))
    matches = [(i, name) for i, name in starts
               if name == spelling or name.endswith("." + spelling)]
    if len(matches) != 1:
        raise ValueError((path, spelling, matches))
    start, actual = matches[0]
    end = min([i for i, _ in starts if i > start] or [len(lines) + 1]) - 1
    while end > start and not lines[end - 1].strip():
        end -= 1
    block = b"".join(lines[start - 1:end])
    if path not in cache:
        pinned = subprocess.check_output(["git", "-C", str(REPO), "show", PIN + ":" + path])
        if raw != pinned:
            raise ValueError("Pinned blob mismatch: " + path)
        cache[path] = {
            "path": path, "sha256": sha(raw), "bytes": len(raw),
            "lines": len(lines), "verified_equal_to_pinned_git_blob": True,
        }
    return {
        "path": path, "declaration": actual, "source_spelling": spelling,
        "line_start": start, "line_end": end, "sha256": sha(raw),
        "range_sha256": sha(block), "range_bytes": len(block),
        "first_line": lines[start - 1].decode().rstrip("\n"),
        "url": f"https://github.com/CocoSgt/riemann-hypothesis-lean/blob/{PIN}/{path}#L{start}-L{end}",
        "role": role, "verified_equal_to_pinned_git_blob": True,
    }


def P(folder, name, decl, role="exact source endpoint or matched definition"):
    return (BASE + folder + "/" + name + ".lean", decl, role)


def S(name, decl, role="exact source endpoint or matched definition"):
    return P("GaloisLibrary/SelmerTransport", name, decl, role)


def C(name, decl, role="exact source endpoint or matched definition"):
    return P("CharacterLevelBounds", name, decl, role)


def L(name, decl, role="exact source endpoint or matched definition"):
    return P("LevelCohomology", name, decl, role)


def H(name, decl, role="exact source endpoint or matched definition"):
    return P("HeightAndVanishing", name, decl, role)


specs = {
    "RV1": [
        S("ConjStableShaFam", "QO", "original discrete coefficient module"),
        S("ConjStableShaFam", "eO", "original normalized-length denominator"),
        S("ConjStableShaFam", "twist₂", "actual transported scalar action"),
        S("DvrFacts", "dvrFacts", "injectivity, freeness and exact ramification normalization"),
        S("QoFacts", "qo_equiv", "original tensor quotient is the fraction-field quotient"),
        S("QoFacts", "qoFacts", "divisibility and exact scalar-torsion length"),
        S("ContinuousCocycleMapApply", "isBaseChange_h1Map",
          "continuous cohomology and actual coefficient map"),
        S("ContinuousCocycleMapApply", "isBaseChange_selMap",
          "all simultaneous local kernels"),
        S("SelBase", "selBase", "strict Selmer length under finite free local base change"),
        S("QoBase", "qoBase", "pure-twist normalization by eO"),
        S("QoExt", "qoExt", "exact normalized length under coefficient extension"),
        H("CoefIndep", "coef_le", "nested coefficient rings on original Omega"),
        C("ShaFamMono", "nrm", "source extended-to-real normalization"),
        C("ShaFamMono", "V'", "unchanged level-ell*N local family"),
    ],
    "RV2": [
        (FML + "Statement.lean", "LData", "original place and cyclotomic datum"),
        (FML + "Statement.lean", "qzTw", "negative twist"),
        (FML + "Statement.lean", "zlTw", "positive dual twist"),
        (FML + "Statement.lean", "Sha", "original strict finite-place kernel"),
        (FML + "Statement.lean", "Sha2Zl", "compact strict degree-two kernel"),
        (FML + "Statement.lean", "VLen", "actual compact H2 length"),
        (FML + "GaloisCohomologyProofs/LdataNonempty.lean", "chi_exists",
         "cyclotomic descent through original unramified quotient"),
        (FML + "GaloisCohomologyProofs/LdataNonempty.lean", "ldata_nonempty",
         "actual local datum exists on the chosen field"),
        S("ShaModel", "shaModel", "absolute/all-valuation versus original GS Selmer model"),
        S("ShaLenEq", "shaLenEq", "same original algebraic closure and local datum"),
        P("AdditiveValuationNorms", "ShaLeV", "shaLeV",
          "literal length comparison reconstructed with compatible finite duality"),
        (FOUND + "LengthEqLengthInvariantsOfTorsionLevels.lean", "finite_level",
         "finite coefficient PT pairings"),
        (FOUND + "LengthEqLengthInvariantsOfTorsionLevels.lean", "ptShaAt",
         "compatible limit comparison"),
        P("GeneratorCountTuples", "LemmaK", "HasMuQ", "precise roots at every prime"),
        P("GeneratorCountTuples", "LemmaK", "LemmaK", "literal incoming KB8 endpoint"),
        P("GeneratorCountTuples", "LemmaK", "kBound", "exact numerical bound with C=31"),
    ],
    "RV3": [
        L("ExistsAb", "exists_ab", "finite abelian extension inside original Omega"),
        L("ExistsAb", "soFin", "complete literal general-number-field endpoint"),
        C("ShaFamMono", "rho", "finite character inverse and negative cyclotomic twist"),
        C("ShaFamMono", "V", "exact source length being shown finite"),
        C("ShaFamMono", "h0", "actual invariants controlled before restriction"),
        C("ShaFamMono", "cls", "actual finite cyclotomic restriction"),
        C("ShaFamMono", "cls_spec", "roots fixed by the joint kernel"),
        C("LiftGens", "upV",
          "source comparison only: RV3 replaces its sharper generator bound by an explicit finite-quotient bound sufficient for soFin"),
        C("H0Nu", "h0Nu", "source H0 control, replaced by one explicit nonzero cyclotomic scalar"),
        C("RootVal", "rootVal", "valuation normalization on the original coefficient DVR"),
        S("ConjStableShaFam", "shaFam", "all original inertia and ell-adic decomposition groups"),
        S("ConjStableShaFam", "galOf", "original embedded restriction subgroup"),
    ],
    "RV4": [
        L("FdAdjoinRange", "fd_adjoin_range", "finitely many algebraic values generate a finite field"),
        L("FdAdjoinRange", "char_finext", "open-kernel finite character coefficients"),
        L("FdAdjoinRange", "coc_finext", "exact Baire/cocycle finite-extension capture"),
        (INERTIA + "CompactGroupRepDefinedOverFiniteExtension.lean",
         "exists_mem_adjoin_simple", "Krasner containment from dense algebraic numbers"),
        (INERTIA + "CompactGroupRepDefinedOverFiniteExtension.lean",
         "exists_countable_family", "countable finite-field cover cofinal for finite subsets"),
        (FOUND + "PadicAutomorphismUnique.lean",
         "denseRange_of_isAlgClosed_padicAlgCl", "rational polynomial approximation and density"),
    ],
    "RV5": [
        L("IntIffNorm", "qo_proj", "continuous quotient with integral unit-ball kernel"),
        L("IntIffNorm", "kill_of_len",
          "finite-length annihilation, simplified here by a composition series"),
        L("IntIffNorm", "core", "exact approximating-coboundary argument and explicit final witness"),
    ],
    "RV6": [
        L("IntIffNorm", "int_iff_norm", "actual integral lattice equals the unit ball"),
        L("IntIffNorm", "soVec", "complete original finite coefficient-field vector endpoint"),
        P("GaloisLibrary/LocalRingsCompletion", "DvrIntClosure", "dvr_intClosure",
          "finite DVR coefficient lattice in original E"),
        P("GaloisLibrary/LocalRingsCompletion", "DvrIntClosure",
          "isIntegral_iff_norm_le_one_bis", "same embedded norm and integral elements"),
        L("ExistsAb", "soFin", "finite strict Selmer premise supplied by RV3"),
    ],
    "RV7": [
        L("FdAdjoinRange", "soBar", "literal universal vector-coboundary endpoint"),
        P("SymplecticGSp4", "EntryMem", "SoV", "literal outgoing symplectic supplier"),
        P("SymplecticGSp4", "EntryMem", "SoFin", "literal outgoing finite-length supplier"),
        H("CoefIndep", "coefIndep", "full normalized-length comparison for possibly nonnested coefficient rings"),
        H("CoefIndep", "enat_cmp", "infinite-length convention retained explicitly"),
        H("CoefSup", "coefSup", "common coefficient ring, constructed here from a compositum"),
        H("DirichletPrimeToLPartMulLPowerPart", "Vlen", "original level module"),
        H("DirichletPrimeToLPartMulLPowerPart", "Vn", "original normalized length"),
        P("ModularityArgument/ThresholdArguments/DenseThresholdCases",
          "ConductorAtMapInjectiveCoeff", "sp4Main_alt",
          "downstream consumer only; RV does not assert CountII/CountIII or its other premises"),
    ],
}
titles = {
    "RV1": "Actual coefficient quotient, strict local base change and exact normalized lengths",
    "RV2": "Root-containing pure negative-twist Selmer finiteness from finite PT and LemmaK31",
    "RV3": "Arbitrary finite-order character restriction/control and literal SoFin",
    "RV4": "Countable finite-field cover and Baire/cocycle finite-extension capture",
    "RV5": "Finite-length quotient to exact vector coboundary by uniform approximation",
    "RV6": "Original finite coefficient-field lattice and local-witness descent, literal soVec",
    "RV7": "Literal universal SoV and SoFin, with full original normalized coefficient independence",
}
deps = {
    "RV1": [],
    "RV2": ["LD3", "LK2", "LK3", "KB1", "KB6", "KB8"],
    "RV3": ["RV1", "RV2"],
    "RV4": [],
    "RV5": ["RV1"],
    "RV6": ["RV1", "RV3", "RV5"],
    "RV7": ["RV1", "RV3", "RV4", "RV6"],
}
scopes = {
    "RV1": "All finite possibly ramified coefficient DVR extensions, arbitrary local subgroup families and discrete module representations. Finiteness equivalence and normalized finite-length equality use exact eO factors.",
    "RV2": "All primes including 2; original totally complex root-containing field/closure/local datum; every e>=1; no FW or Iwasawa assumption.",
    "RV3": "All original number fields and closures, all primes, arbitrary open-kernel finite-order characters including ell-power order, every e>=1. Bound via finite quotient and finite invariants, no averaging.",
    "RV4": "Compact Hausdorff group; continuous algebraic-valued cocycle whose scalar factors lie in one finite field. Actual subgroup structure, not a false compact-subset claim.",
    "RV5": "Exact same local family; finite-length quotient module; original finite coefficient field; local witnesses in that field; no assumed convergence of approximate witnesses.",
    "RV6": "Original finite E inside PadicAlgCl, arbitrary number field and closure, all primes, e>=1; local witnesses allowed initially in algebraic closure and then returned to E.",
    "RV7": "Every original Omega/l has SoV and SoFin. coefIndep includes all natural e and the source toNat convention at infinite length, plus possibly nonnested coefficient rings with equal embedded character values.",
}
classical = {cid: [] for cid in titles}
for cid in ["RV4", "RV5", "RV6"]:
    classical[cid] = ["RV-LF"]

raw = (HERE / "main.tex").read_bytes()
lines = raw.splitlines(keepends=True)
claims = []
for cid in titles:
    start = next(i for i, line in enumerate(lines, 1)
                 if re.match(r"\\begin\{(?:proposition|theorem)\}\[" + cid + r":", line.decode()))
    end = next(i for i, line in enumerate(lines, 1)
               if i > start and line.decode().startswith("\\end{proof}"))
    proof = b"".join(lines[start - 1:end])
    claims.append({
        "id": cid, "title": titles[cid], "introduced_in": "0.26",
        "status": "Complete human proof in the stated scope with listed established suppliers and classical inputs",
        "mathematical_status": "exact endpoint reconstruction with proved simplifications; no Lean replay",
        "scope": scopes[cid], "depends_on": deps[cid],
        "classical_inputs": classical[cid], "remaining_bespoke_inputs": [],
        "proof_location": {
            "file": "rank_one_cohomology/main.tex", "paragraph": cid,
            "label": "claim:" + cid, "line_start": start, "line_end": end,
            "sha256": sha(proof), "bytes": len(proof),
        },
        "sources": [source(*entry) for entry in specs[cid]],
        "source_relation": (
            "Literal SoFin/soVec/soBar/SoV and coefficient-independence interfaces matched. "
            "RV3 replaces the sharper upV generator estimate by a proved finite-quotient "
            "bound, sufficient for the full endpoint; that sharper intermediate estimate "
            "is not independently claimed here. RV4 and RV5 reconstruct the substantive "
            "Baire/cocycle and lattice approximation mechanisms."
        ),
        "component_ledger": "rank_one_cohomology/provenance.json",
    })

out = {
    "schema": "rh-human-reconstruction-provenance/1",
    "artifact_version": "0.26", "date": "2026-11-22",
    "repository": "https://github.com/CocoSgt/riemann-hypothesis-lean",
    "commit": PIN, "component": "rank_one_cohomology",
    "scope": "Literal SoFin and SoV for every original Omega and every prime, with general-number-field soFin/soVec/soBar and exact normalized coefficient independence.",
    "claims": claims, "dependency_graph": deps,
    "external_claim_dependencies": {
        "LD3": "local_duality_closure/provenance.json",
        "LK2": "local_k_duality/provenance.json",
        "LK3": "local_k_duality/provenance.json",
        "KB1": "k_theory_bridge/provenance.json",
        "KB6": "k_theory_bridge/provenance.json",
        "KB8": "k_theory_bridge/provenance.json",
    },
    "classical_input_registry": "rank_one_cohomology/classical_inputs.json",
    "source_files": list(cache.values()),
    "validation": {
        "claim_count": len(claims),
        "claim_source_links": sum(len(c["sources"]) for c in claims),
        "source_files_checked_against_pinned_git_blobs": len(cache),
        "main_tex_sha256": sha(raw),
        "verification_kind": "Exact written/source byte ranges and pinned Git blob checks; no Lean kernel replay",
    },
}
(HERE / "provenance.json").write_text(json.dumps(out, indent=2, ensure_ascii=False) + "\n")
(HERE / "source_locators.txt").write_text(
    "\n\n".join(c["id"] + " — " + c["title"] + "\n" +
                "\n".join(s["declaration"] + "\n" + s["url"] +
                          "\nfile " + s["sha256"] + "\nrange " + s["range_sha256"]
                          for s in c["sources"]) for c in claims) + "\n")
print(json.dumps(out["validation"], indent=2))
