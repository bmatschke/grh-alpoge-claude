#!/usr/bin/env python3
"""Rebuild pinned Lean and written-proof provenance for OB1--OB8."""
from pathlib import Path
import argparse
import hashlib
import json
import re
import subprocess

parser = argparse.ArgumentParser()
parser.add_argument("--repo", type=Path,
                    default=Path(__file__).resolve().parents[2] / "lean-source")
args = parser.parse_args()
HERE = Path(__file__).resolve().parent
REPO = args.repo
PIN = "7cbf7a0c32fca1badf05931879a37c3f8a2b03b4"
BASE = "src/Development/AutomorphicArithmetic/AutomorphicVarieties/"
ODD = BASE + "OddResidueBounds/"
BERN = BASE + "GaloisLibrary/BernoulliNumbers/"
SEL = BASE + "GaloisLibrary/SelmerTransport/"
STK = BASE + "StickelbergerElements/"
EVAL = BASE + "StickelbergerCharacterEval/"


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


cache = {}


def source(path, spelling, role="source endpoint or exact definition"):
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
        pinned = subprocess.check_output(
            ["git", "-C", str(REPO), "show", PIN + ":" + path])
        if pinned != raw:
            raise ValueError("Pinned Git blob mismatch: " + path)
        cache[path] = {"path": path, "sha256": sha(raw), "bytes": len(raw),
                       "lines": len(lines), "verified_equal_to_pinned_git_blob": True}
    return {
        "path": path, "declaration": actual, "source_spelling": spelling,
        "line_start": start, "line_end": end,
        "sha256": sha(raw), "range_sha256": sha(block), "range_bytes": len(block),
        "first_line": lines[start - 1].decode().rstrip("\n"),
        "url": f"https://github.com/CocoSgt/riemann-hypothesis-lean/blob/{PIN}/{path}#L{start}-L{end}",
        "role": role, "verified_equal_to_pinned_git_blob": True,
    }


def O(file, declaration, role="source endpoint or exact definition"):
    return (ODD + file + ".lean", declaration, role)


def B(file, declaration, role="source endpoint or exact definition"):
    return (BERN + file + ".lean", declaration, role)


def S(file, declaration, role="source endpoint or exact definition"):
    return (SEL + file + ".lean", declaration, role)


spec = {
    "OB1": [
        O("ActEx", "actEx"), O("ActFacts", "actFacts"), O("ActConj", "actConj"),
        O("DegExistsLift", "deg"),
        O("ThmBcOfPsiBound", "ncard_charSet_le_ker_index"),
        (BASE + "StmtFields.lean", "IsCompField", "literal original-field fixing condition"),
        (BASE + "StmtFields.lean", "deg", "fixed exceptional-prime parameter"),
    ],
    "OB2": [
        B("MapGenBChar", "Bprim"), B("MapGenBChar", "charSet"),
        B("MapGenBChar", "parKer"), B("MapGenBChar", "den"), B("MapGenBChar", "bnd"),
        B("Primmem", "b_primmem"), B("Denupper", "b_denupper"),
        B("Prodint", "b_prodint"), O("ProdVal", "prodVal"),
        O("ZeroMemUnrHom", "alN"),
    ],
    "OB3": [
        O("ZeroMemUnrHom", "PsiBound", "exact retained bespoke interface"),
        O("ZeroMemUnrHom", "psiLen", "literal eigenspace length"),
        O("ChiFacts", "chiFacts"), O("PsiReal", "psiReal"), O("AtPrime", "atPrime"),
        S("ShaLenEq", "shaLenEq"), S("QoBase", "qoBase"),
        S("ShaDecompSign", "shaDecompSign"), S("ExistsO", "existsO"),
        S("DvrFacts", "dvrFacts"), S("NormO", "normO"),
        O("ThmBcOfPsiBound", "prime_of"), O("ThmBcOfPsiBound", "primeBound_of"),
    ],
    "OB4": [
        O("Imports", "gen"), O("UnrInj", "unrInj"), O("UnrSel", "unrSel"),
        O("SelCard", "selCard"), O("FnOne", "fnOne"),
        O("LogH", "logH"), O("LogDisc", "logDisc"),
        O("TorsRep", "torsRep"), O("CobOne", "cobOne"),
        O("ContinuousToTorsionBounded", "Z1_H1_qz_twist_l_power_torsion"),
    ],
    "OB5": [
        O("ZKill", "zKill"), O("ResKill", "resKill"), O("TotKill", "totKill"),
        O("HomKill", "homKill"), O("ClKill", "clKill"),
        O("NearLevel", "congr"), O("YLevel", "yLevel"), O("YNear", "yNear"),
        (STK + "CoefMapSingle.lean", "Eone", "exact first-weight coefficient"),
        (STK + "CoefMapSingle.lean", "yEl", "exact inverse-sensitive higher element"),
        (STK + "CoefMapSingle.lean", "ytEl", "integer approximating element"),
        (STK + "TwistedBernoulliValueCongrPowMulFirst.lean",
         "twistedBernoulliValue_congr_pow_mul_first", "Bernoulli binomial congruence"),
        O("ZeroMemUnrHom", "actRep", "original cohomology action"),
        ("src/Formalism/GaloisCohomology/Statement.lean", "qzTw",
         "exact negative twist"),
        ("src/Formalism/GaloisCohomology/Statement.lean", "Sha",
         "exact original local kernel"),
    ],
    "OB6": [
        O("KillPow", "killPow", "reconstructed in the needed odd-prime scope"),
        O("AdjKill", "adjKill"), O("DetVal", "detVal"), O("BdxLog", "bdxLog"),
        (EVAL + "Detint.lean", "higherStickelberger_det_exists_int_bounded"),
        (EVAL + "NormCharEvalHigherStickelbergerLe.lean",
         "norm_charEval_higherStickelberger_le"),
        (EVAL + "GroupRingCharEvalStickelbergerYNeZeroOfParity.lean",
         "groupRingCharEval_stickelbergerY_ne_zero_of_parity"),
        (EVAL + "MemZpowersIff.lean", "bdX"),
        (EVAL + "MemZpowersIff.lean", "denY"),
        (EVAL + "MemZpowersIff.lean", "sizeY"),
    ],
    "OB7": [
        O("LenPow", "lenPow"), O("ThmBcOfPsiBound", "stick_of"),
        O("ThmBcOfPsiBound", "stickBound", "odd-prime scope with explicit constant 240"),
        O("ZeroMemUnrHom", "StickBound", "only odd-prime specialization needed"),
        (BASE + "LengthEqAddEigen.lean", "ShaMinus", "exact twist-adjusted minus eigenspace"),
        (BASE + "LengthEqAddEigen.lean", "minusLen"),
    ],
    "OB8": [
        O("ThmBcOfPsiBound", "log_bnd_le_mul_log"),
        O("ThmBcOfPsiBound", "thmBc_of"),
        O("ThmBcOfPsiBound", "thmBcFree_of"),
        (BASE + "PrimeSetBoundDataOfPrimitiveChar.lean", "ThmBcFree",
         "full universal endpoint"),
        (BASE + "PrimeSetBoundDataOfPrimitiveChar.lean", "PrimePair"),
        (BASE + "LengthEqAddEigen.lean", "VVminusLe",
         "all original closures/local data/finite prime subsums"),
        (BASE + "StmtFields.lean", "minusBound", "exact VW bound"),
        (BASE + "StmtFields.lean", "condF", "minimum conductor on the original E"),
    ],
}
titles = {
    "OB1": "Original cyclotomic action, character count and fixed exceptional-prime set",
    "OB2": "Integral primitive Bernoulli product and uniform valuation budget",
    "OB3": "Same-field eigenspace comparison and all tame-prime bounds from PsiBound",
    "OB4": "Uniform ambient cohomology generator bound with constant 8",
    "OB5": "Finite Jacobi annihilator transfer to the actual negative cyclotomic twist",
    "OB6": "Signed determinant and one uniform annihilating power with constant 30",
    "OB7": "Exponent times generators: odd-prime Stickelberger length bound with 240",
    "OB8": "Full original-field ThmBcFree with constant 240",
}
deps = {
    "OB1": [], "OB2": [],
    "OB3": ["OB1", "OB2", "OS9"],
    "OB4": [],
    "OB5": ["OB1", "OS1"],
    "OB6": ["OB1", "OB2", "OB5"],
    "OB7": ["OB4", "OB6"],
    "OB8": ["OB1", "OB3", "OB7"],
}
classical_inputs = {
    "OB1": [], "OB2": ["OB-BC"], "OB3": ["OB-LF"],
    "OB4": ["OB-KU", "OB-MD"],
    "OB5": ["OB-BC", "OB-CF"],
    "OB6": [], "OB7": [], "OB8": [],
}
scopes = {
    "OB1": "The given cyclotomic embedding and IsCompField fixing condition; no new field model.",
    "OB2": "k>=2, all characters with kernels in a specified parity-compatible set; no k=1 claim.",
    "OB3": "Literal PsiBound; odd primes not dividing original field degree; all original local data.",
    "OB4": "Any cyclotomic subfield, every prime and every integer twist; original ambient H1[l].",
    "OB5": "Odd prime, e>=1, actual Sha with negative twist; exact finite Jacobi annihilator supplied by OS1; no classical Stickelberger leaf.",
    "OB6": "Odd prime only; uniform annihilating exponent. No unused l=2 Procyc generalization claimed.",
    "OB7": "Odd-prime specialization of StickBound with explicit constant 240.",
    "OB8": "Exact ThmBcFree for all AbF, s,t>=2, PrimePair, original CM E, closure, local-data family and finite odd-prime set.",
}
tex_raw = (HERE / "main.tex").read_bytes()
tex_lines = tex_raw.splitlines(keepends=True)
claims = []
for cid in titles:
    start = next(i for i, line in enumerate(tex_lines, 1)
                 if line.decode().startswith("\\paragraph{" + cid + ":"))
    end = min([i for i, line in enumerate(tex_lines, 1)
               if i > start and line.decode().startswith("\\paragraph{")] or
              [len(tex_lines) + 1]) - 1
    block = b"".join(tex_lines[start - 1:end])
    claims.append({
        "id": cid, "title": titles[cid], "introduced_in": "0.24",
        "status": "Complete human proof in the stated scope, conditional only on listed inputs",
        "mathematical_status": "derived human alternative; not a Lean kernel replay",
        "scope": scopes[cid], "depends_on": deps[cid],
        "classical_inputs": classical_inputs[cid],
        "bespoke_inputs": ([{"name": "PsiBound", "supplied_by": "OS9",
                             "scope": "Literal universal original-field character-length interface"}]
                           if cid == "OB3" else
                           [{"name": "Finite Jacobi class-group annihilation", "supplied_by": "OS1",
                             "scope": "OS.3 at L=R*l^m, a<L; cancel 2 on odd l-primary class characters"}]
                           if cid == "OB5" else []),
        "proof_location": {"file": "odd_minus_bounds/main.tex", "paragraph": cid,
                           "label": "claim:" + cid, "line_start": start, "line_end": end,
                           "sha256": sha(block), "bytes": len(block)},
        "sources": [source(*entry) for entry in spec[cid]],
        "source_relation": "Exact endpoint and definition match; finite-cocycle and elementary arithmetic simplifications replace portions of the internal Lean route.",
        "component_ledger": "odd_minus_bounds/provenance.json",
    })

out = {
    "schema": "rh-human-reconstruction-provenance/1",
    "artifact_version": "0.24", "date": "2026-11-22",
    "repository": "https://github.com/CocoSgt/riemann-hypothesis-lean",
    "commit": PIN, "component": "odd_minus_bounds",
    "scope": "OS1 and PsiBound (OS9), plus named classical theorems, imply exact ThmBcFree with C=240.",
    "claims": claims, "dependency_graph": deps,
    "external_claim_dependencies": {"OS1": "odd_minus_supplier/provenance.json", "OS9": "odd_minus_supplier/provenance.json"},
    "classical_input_registry": "odd_minus_bounds/classical_inputs.json",
    "source_files": list(cache.values()),
    "validation": {
        "claim_count": len(claims),
        "claim_source_links": sum(len(c["sources"]) for c in claims),
        "source_files_checked_against_pinned_git_blobs": len(cache),
        "main_tex_sha256": sha(tex_raw),
        "verification_kind": "Exact proof/source byte-range hashes and pinned Git blob identity; human mathematical reconstruction, not Lean replay",
    },
}
(HERE / "provenance.json").write_text(json.dumps(out, indent=2, ensure_ascii=False) + "\n")
(HERE / "source_locators.txt").write_text(
    "\n\n".join(c["id"] + " — " + c["title"] + "\n" +
                "\n".join(s["declaration"] + "\n" + s["url"] +
                          "\nfile " + s["sha256"] + "\nrange " + s["range_sha256"]
                          for s in c["sources"]) for c in claims) + "\n")
print(json.dumps(out["validation"], indent=2))
