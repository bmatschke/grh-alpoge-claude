#!/usr/bin/env python3
"""Build pinned Lean and written-proof provenance for TW1--TW8."""
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
FML = "src/Formalism/GaloisCohomology/Statement.lean"
PTL = ("src/Development/AbelianVarietyTheory/Proofs/FoundationProofs/"
       "LengthEqLengthInvariantsOfTorsionLevels.lean")


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


def P(folder, file, declaration, role="source endpoint or exact definition"):
    return (BASE + folder + "/" + file + ".lean", declaration, role)


def W(file, declaration, role="source endpoint or exact definition"):
    return P("LayeredIsomorphisms", file, declaration, role)


def Q(file, declaration, role="source endpoint or exact definition"):
    return P("QuadraticExtensions", file, declaration, role)


def T(file, declaration, role="source endpoint or exact definition"):
    return P("NumberFieldTowers", file, declaration, role)


def A(file, declaration, role="source endpoint or exact definition"):
    return P("AdditiveValuationNorms", file, declaration, role)


def B(declaration, role="literal endpoint quantifier or bound"):
    return (BASE + "PrimeSetBoundDataOfPrimitiveChar.lean", declaration, role)


spec = {
    "TW1": [
        P("PublishedTheorems", "FerreroWashington", "FerreroWashington",
          "literal finite-layer rank proposition, including l=2 with mu_4"),
        Q("IsAlgClosureRat", "fwRk", "uniform infinite-tower character-rank consequence"),
        Q("IsAlgClosureRat", "abRk", "all algebraic-closure and abelian-field models"),
        Q("LevelRk", "levelRk", "finite class rank to finite-layer character rank"),
        Q("LevUAnti", "infRk", "finite-layer rank to tower rank"),
    ],
    "TW2": [
        Q("IsAlgClosureRat", "baseRk", "exact 4*(g+6*M.deg) constant"),
        Q("IsAlgClosureRat", "towerTwo", "rank before q,d and all base-field models"),
        Q("IsAlgClosureRat", "towerFixed", "fixed odd-prime family"),
        Q("IsAlgClosureRat", "twoBase", "original E versus containing two-primary layer"),
        Q("OrbTwo", "orbTwo", "q and d orbit counts 2*o and 4*o"),
        Q("IneTwo", "ineTwo", "one mod-two inertia dimension"),
        Q("CharStep", "charStep", "allowing one prime's ramification"),
        Q("QuadStep", "quadStep", "quadratic restriction rank bound"),
        Q("CompIndex", "compIndex", "actual fixing-subgroup index divides two"),
        Q("ShaTwo", "shaTwo", "one extra unit of length on the original field"),
        Q("KerTwo", "kerTwo", "restriction-kernel length at most one"),
        T("GenIff", "genIff", "compact module generator/rank equivalence"),
        T("RankXRk", "rankXRk", "mod-l character dimension versus generator count"),
        (BASE + "StmtFields.lean", "IsCompField", "original fixing subgroup"),
        W("SecondBound", "TwoBase"),
        W("SecondBound", "TwoIn"),
        W("SecondBound", "FixedIn"),
    ],
    "TW3": [
        (FML, "qzTw", "literal negative cyclotomic twist"),
        (FML, "zlTw", "compact dual twist"),
        (FML, "Sha", "given local-data strict kernel"),
        (FML, "VLen", "actual global H2 length"),
        (FML, "Sha2Zl", "compact strict H2 kernel"),
        P("GaloisLibrary/GaloisCohomologyLength", "LevelInertiaLeLevelDec",
          "shaInv", "closure-independent strict length"),
        P("GaloisLibrary/GaloisCohomologyLength", "ShaLenEqShaInv",
          "shaLen_eq_shaInv", "every original closure and local-data record"),
        T("ExistsDescends", "step0", "exact all-layer coinvariant equality"),
        T("ExistsDescends", "exists_descends", "one cyclotomic generator and exact level"),
        T("Imports", "desc", "strict-character descent"),
        T("XTwApplyApply", "dTw", "negative twist on character module"),
        T("XTwApplyApply", "xTw", "positive twist on contragredient dual"),
        T("CokerDual", "cokerDual", "invariants/coinvariants and length"),
        A("ShaLeV", "shaLeV", "exact strict-length to actual VLen inequality"),
        (PTL, "finite_level", "finite PT specialization at every coefficient level"),
        (PTL, "ptShaAt", "finite-level to compact/discrete strict-length comparison"),
    ],
    "TW4": [
        T("XTwApplyApply", "IsTower", "exact root/positivity/generator interface"),
        A("ABoundOfIsTower", "aBound_of_isTower", "complete tower-to-ABound source endpoint"),
        A("ABoundOfDescends", "aBound_of_descends"),
        A("GenLevel", "genLevel", "maximal roots and exact cyclotomic level"),
        A("XUnip", "xUnip", "mod-l unipotence"),
        A("UnipPow", "unipPow", "nilpotence exponent bounded by generators"),
        A("Growth", "growth", "R per layer beyond jZero"),
        A("ImportsMore", "step", "one-layer cokernel increment"),
        A("ImportsTer", "phi", "range contains l*X"),
        A("DetBound", "detBound", "determinant bound with Z_l centers"),
        A("PadicUnitsDistanceLeMax", "ball", "one p-adic center per eigenvalue"),
        A("Helly", "helly", "compact nested balls"),
        A("LteNorm", "lteNorm", "exact principal-unit distance including l=2"),
        A("ExistsCentresLevel", "exists_centres", "all layer lengths"),
        A("ExistsCentresLevel", "exists_centres_norm", "literal norm-cutoff first bound"),
        W("SecondBound", "ABound"),
        W("SecondBound", "SecondBound"),
        W("SecondBound", "jZero"),
    ],
    "TW5": [
        W("Exc", "exc", "at most R exceptional integer twists"),
        W("Near1", "near1", "one integer near each p-adic center"),
        W("SecondBound", "FirstBound"),
        W("SecondBound", "Good"),
        W("Window1", "window1", "elementary interval induction with exact denominator"),
        W("Window", "window", "single square window"),
    ],
    "TW6": [
        W("Rootdeg", "rootdeg"),
        W("Layeremb", "layeremb", "conductor bound before discriminant estimate"),
        W("Imports", "disc", "cyclotomic subfield discriminant upper bound"),
        W("Layerdisc", "layerdisc", "all q,d-independent reference-field constants"),
        W("EquivOfRange", "abiso", "all models of same AbF"),
        W("Layeriso", "layeriso", "all separately specified layer models"),
        (BASE + "StmtFields.lean", "IsAbField"),
        (BASE + "StmtFields.lean", "IsLayer"),
        P("GaloisLibrary/GaloisCohomologyLength", "ShaLenEqShaInv",
          "shaLen_eq_shaInv", "original local-data invariance"),
    ],
    "TW7": [
        P("GeneratorCountTuples", "LemmaK", "LemmaK",
          "literal incoming quantitative compact-cohomology statement, supplied by KB8"),
        P("GeneratorCountTuples", "LemmaK", "kBound"),
        W("Klen", "klen", "log cardinality to length using log l > 1/2"),
        W("Kexp", "kexp", "small exceptional twist and discriminant exponents"),
        W("ImportsAlt", "point", "all twists, including exceptional ones"),
        W("Point2", "point2", "uniform constant C and +1"),
        W("Logs", "logs", "floor logarithm and admitted exponent estimates"),
        W("Final", "final", "3 eps/4 to 4 eps/5 absorption"),
        W("SecondBound", "ptBound"),
    ],
    "TW8": [
        W("ThmBabOfLemmaK", "thmBab_of_lemmaK",
          "literal exists K before all Ct>=1 endpoint"),
        W("ThmBabOf", "thmBab_of", "full simultaneous assembly and thresholds"),
        W("PartA", "partA", "two-primary family uniform in original E and q,d"),
        W("PartB", "partB", "every reference field and layer model"),
        W("Vvat", "vvat", "all finite twist sums and all original local data"),
        W("Kmono", "kmono", "increase CK before choosing K"),
        Q("IsAlgClosureRat", "fixedIn"),
        Q("IsAlgClosureRat", "twoIn"),
        B("BConst"), B("BConst.R"), B("BConst.J"),
        B("admitted"), B("PrimePair"), B("OddPrimesWithRootsOfUnity"),
        B("BaAt"), B("BbAt"), B("IsBWindow"), B("BShape"), B("ThmBab"),
        (BASE + "LengthEqAddEigen.lean", "VVat",
         "finiteness plus sum, universally quantified over original local data"),
    ],
}
titles = {
    "TW1": "Exact Ferrero-Washington finite-layer and tower rank interface, including two",
    "TW2": "One q,d-uniform two-primary rank bound and original-host quadratic restriction",
    "TW3": "Negative-twist strict descent, positive dual coinvariants and finite-PT limit comparison",
    "TW4": "Complete p-adic center, growth and reference-layer ABound",
    "TW5": "At most R exceptional twists and one exact common square window",
    "TW6": "Uniform reference-layer sizes and all field/local-data model transfers",
    "TW7": "All-twist quantitative bounds and exponential absorption from LemmaK",
    "TW8": "Literal exists BConst K before every Ct>=1 ThmBab, on one fixed-pair window",
}
deps = {
    "TW1": [],
    "TW2": ["TW1"],
    "TW3": ["TW1", "LD3", "LK2", "LK3", "KB1", "KB6"],
    "TW4": ["TW1", "TW3"],
    "TW5": ["TW4"],
    "TW6": [],
    "TW7": ["TW4", "TW5", "KB8"],
    "TW8": ["TW2", "TW4", "TW5", "TW6", "TW7"],
}
classical = {
    "TW1": ["TW-FW", "TW-IW", "TW-CF"],
    "TW2": [], "TW3": [], "TW4": [], "TW5": [],
    "TW6": ["TW-CD"], "TW7": [], "TW8": [],
}
scopes = {
    "TW1": "All primes including 2; abelian F containing mu_l, or mu_4 at 2; every root-layer model.",
    "TW2": "R0=4*(g+6*M.deg) chosen before all prime pairs; all original E and all twists k>=1.",
    "TW3": "k>=1; actual negative-twist strict local kernel; every reference closure/local record; no k=0 assertion.",
    "TW4": "All primes and all layer indices; at most R generators; exact jZero=Nat.log l R+3; extended lengths allowed.",
    "TW5": "Integer cutoff Z>=1, exact norm cutoff and R exceptions; entire real square window, including endpoint inequalities.",
    "TW6": "Uniform degree/discriminant constants and all AbF/layer/local-data models; same relative algebra structure.",
    "TW7": "Literal LemmaK supplied by KB8; exact 3*eps/4 and 4*eps/5 exponents; thresholds independent of varying q,d.",
    "TW8": "One K before all Ct>=1; X0 before admitted functions, X and q,d; one fixed pair and one Y; every original E and separately every reference-layer model.",
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
        "id": cid, "title": titles[cid], "introduced_in": "0.25",
        "status": "Complete human proof in the stated scope, conditional only on listed inputs",
        "mathematical_status": "derived human reconstruction and simplification; not a Lean kernel replay",
        "scope": scopes[cid], "depends_on": deps[cid],
        "classical_inputs": classical[cid],
        "bespoke_inputs": ([{"name": "LemmaK", "supplied_by": "KB8", "constant": 31,
                             "scope": "Literal universal original-data compact H2 cardinality bound"}]
                           if cid == "TW7" else []),
        "proof_location": {"file": "simultaneous_cohomological_windows/main.tex",
                           "paragraph": cid, "label": "claim:" + cid,
                           "line_start": start, "line_end": end,
                           "sha256": sha(block), "bytes": len(block)},
        "sources": [source(*entry) for entry in spec[cid]],
        "source_relation": "Exact semantic endpoint and quantifier match; classical mu=0 translation, compact duality, elementary inertia/rank and p-adic matrix arguments simplify the internal Lean route.",
        "component_ledger": "simultaneous_cohomological_windows/provenance.json",
    })

out = {
    "schema": "rh-human-reconstruction-provenance/1",
    "artifact_version": "0.25", "date": "2026-11-22",
    "repository": "https://github.com/CocoSgt/riemann-hypothesis-lean",
    "commit": PIN, "component": "simultaneous_cohomological_windows",
    "scope": "KB8, LD3, LK2, LK3 and named classical inputs imply literal exists K forall Ct>=1 ThmBab K Ct.",
    "claims": claims, "dependency_graph": deps,
    "external_claim_dependencies": {
        "LD3": "local_duality_closure/provenance.json",
        "LK2": "local_k_duality/provenance.json",
        "LK3": "local_k_duality/provenance.json",
        "KB1": "k_theory_bridge/provenance.json",
        "KB6": "k_theory_bridge/provenance.json",
        "KB8": "k_theory_bridge/provenance.json",
    },
    "classical_input_registry": "simultaneous_cohomological_windows/classical_inputs.json",
    "source_files": list(cache.values()),
    "validation": {
        "claim_count": len(claims),
        "claim_source_links": sum(len(c["sources"]) for c in claims),
        "source_files_checked_against_pinned_git_blobs": len(cache),
        "main_tex_sha256": sha(tex_raw),
        "verification_kind": "Pinned source blob and exact written/source byte-range hashes; human mathematical proof, not Lean replay",
    },
}
(HERE / "provenance.json").write_text(json.dumps(out, indent=2, ensure_ascii=False) + "\n")
(HERE / "source_locators.txt").write_text(
    "\n\n".join(c["id"] + " — " + c["title"] + "\n" +
                "\n".join(s["declaration"] + "\n" + s["url"] +
                          "\nfile " + s["sha256"] + "\nrange " + s["range_sha256"]
                          for s in c["sources"]) for c in claims) + "\n")
print(json.dumps(out["validation"], indent=2))
