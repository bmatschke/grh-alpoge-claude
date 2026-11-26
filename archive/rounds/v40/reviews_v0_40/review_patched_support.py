#!/usr/bin/env python3
"""Bind the independent mathematical review of PMS1--PMS32 to exact bytes.

This script verifies evidence and writes a previously performed human review;
it does not purport to mechanically establish mathematical correctness.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import subprocess
from pathlib import Path

PIN = "7cbf7a0c32fca1badf05931879a37c3f8a2b03b4"

NOTES = {
    1: "The entire original S5 antecedent is retained: one ultrafilter containing all tails, all-series semilinearity in the finite quotient, genuinely R-linear paired maps, and one exponent before every generator and precision. Finite X suffices for PMod; freeness is imposed for S5.",
    2: "The bounded diagonal index tends to infinity along the given filter and avoids countable-completeness assumptions. A fixed finite generating set of A permits simultaneous coefficient choices and proves both directions of the actual ultralimit ideal criterion.",
    3: "Every X/m_L^j X is a finite set; its unique ultrafilter value is compatible in j and determines one element of the complete finite module X. Diagonal precision choices preserve R-linearity, both paired compositions, and localization at the same f.",
    4: "The degree-a coefficient calculation uses k=a+1, covers a=0 and rank zero, and gives the literal QRegAt condition. The ultralimit transport uses only finitely many monomials and the preceding ideal criterion.",
    5: "The exact localized tower has surjective transitions, kernel I^k P_(k+1), and I^k P_k=0. Its scalar action factors through BB/I^k=R_f/I^k; density and strictness recover every IsYCpl field without assuming BB local or nonzero.",
    6: "Compatible finite generators yield a surjection from one finite free complete module onto the actual inverse limit. Corrections at depth k are in I^k; the same argument proves every exact quotient kernel and not just an abstract module with the right fiber.",
    7: "Quasiregularity follows by applying the exact quotient at degree a+1. The fiber map is BB-linear because I kills X. The annihilator criterion retains the order: for every k, one denominator exponent before every precision j.",
    8: "Finite coefficient quotients give a nilpotence exponent for m_R on X/J_j X. Paired maps transfer it to f*m_R^c M_N inside I+J_j. Iteration gives f^k*m_R^(ck), so the extra denominator k is independent of j and the approximate relations give the actual radical-annihilator field.",
    9: "For primes containing I and avoiding f, finite-module completion identifies BB/q^v BB with (R/q^v)_f and preserves structural maps. Localizing and completing produces the literal completion of R_q. Faithful flatness is used only for the specified local completion.",
    10: "Finite-module support is tested by the residue-field fiber. Base change preserves the nonzero fiber at the contracted prime without a flatness premise. With I in Q, the exact PMod fiber gives the source annihilator equivalence.",
    11: "An arbitrary support prime Z below Q contracts to a support prime of BB contained in the new center. Faithful flatness lifts that prime into the second completion, and the fiber criterion preserves support and equality of contractions. Z need not be minimal.",
    12: "The faithful action algebra E=R/Ann X is finite over L0. After localization and completion, its finite algebra splits into complete local factors. The factor specified by the same q acts as an idempotent on La tensor X; hence the actual completed fiber is a direct summand of a finite free La-module and is free over local La.",
    13: "Krull intersection on N/I^k N makes every I^k N closed in the maximal-ideal topology. Since I lies in the maximal ideal, this proves actual I-adic completeness. Lifting a free fiber basis and using least total degree plus quasiregularity gives a genuine La[[Y]]-basis, including the zero-fiber case.",
    14: "La[[Y]] is regular local of dimension d+|sigma| by the explicit parameter chain and height bound. The faithful action on the free module N makes C/Ann N finite and torsion free over this domain. Every minimal associated prime contracts to zero, so each integral quotient has the claimed dimension. The zero-module case is vacuous.",
    15: "Quotienting each completion by the original relation ideal gives the exact R/ii completion. The radical-annihilator inclusion preserves containing and minimal primes; dim, fib, and full arbitrary-center move are all supplied, with equal contractions in R/ii.",
    16: "Surjectivity O->K proves the original coefficient map is local and identifies its kernel after the explicit changes w_i->w_i-F_i(s). The Unit variable maps to the same t. The prime chain and height bound give dimension 1+D before completion, and the two checked completion lemmas preserve it.",
    17: "The literal RRObj/RMaps, one original Lim, original MN and X0 actions, all five Tup.Maps fields, full coefficient-series identities, roots, and the exact f/ii are retained. The PRG inputs do not themselves assume the patched module being constructed here.",
    18: "The original splitting algebra is finite free over B by PRG. Tensoring with the actual L0-free base module gives the stated X0 freeness, coefficient action, and y-annihilation. Completeness and finite residue of the actual L0 follow from the coefficient DVR, with no freeness assumption on B over L0.",
    19: "The integer binomial identity gives divisibility by ell^j for N>=j+k without division in the coefficient ring. It covers zero ideals, empty variables, and rank zero. Quotienting the actual supplied free module preserves the entire series action, and no global rank bound is introduced.",
    20: "Inherited JSP9 supplies the integral full-law word identity. Compactness gives one open normal subgroup before all coefficients and finite group-algebra sums. The source's i>n Nat-subtraction convention is explicitly handled by signed lambda_n, and the ambient normal-core refinement is valid because Phi0 is open. Full tuple equality invokes the actual universal property.",
    21: "The original ProL guard activates T.ph_lim; its finite intersections and Lambda.p_lim give one event before every a in R. A common quotient of the two splitting algebras compares whole homomorphisms by PMS20, including all characters, section, roots, and y. The zero quotient branch is harmless.",
    22: "The splitting-polynomial congruence is transported through the same formal root variables and the same base module quotient. The resulting map respects all coefficient-series scalars. The stronger ell^j divisibility of f-F_N, rather than only m_R-adic divisibility, is what later makes both paired compositions exact.",
    23: "A power of m_B kills the finite coefficient quotient of M0. Uniform piCong then makes the canonical congruence map R-linear for every scalar at once. Composing it with the original semilinear Taylor--Wiles maps gives genuinely R-linear quotient maps with both compositions equal to the original f.",
    24: "The kernel-coset equality produces a lift with the prescribed finite-level image in the coset of the already given limiting lift. Normality handles the conjugation term; V contained in Phi0 preserves the exact subgroup. No untracked replacement of the original tuple is made.",
    25: "The ker and pol relations are approximated on the exact common cosets. Polarization retains the inverse, conjugation by ct, and exponent 1-n. Uniform cyclotomic congruence works for negative unit powers as well, and each approximant is killed by the actual finite-level pair.",
    26: "The ordinary relation preserves the List.ofFn factor order and every original character. For inertia, compatibility plus Adapted proves membership in the finite-level residual Ip intersection, not merely in the geometric inertia image. Both give exact annihilation after specialization.",
    27: "The ph and ta lifts preserve their designated cosets and actual images. Both ordered auxiliary-prime expressions retain all roots and y variables. The exact TWMaps.rel1/rel2 exponent is the single stored A.ex on the original module.",
    28: "One exponent A.ex+1 is fixed before all six relation constructors, every generator, precision, and level event. f-F_N and a-a' have the required congruences, and the extra power handles the zero-image branch and A.ex=0. No infinite intersection of large events is used.",
    29: "All three generic patching hypotheses are installed on the same original MN, X0, rho, pi, Lim ultrafilter, f and ii. PMS15 gives all S5 fields for arbitrary center families. Normalized point centers have parameter exactly 1+D+nq, with no new coefficient ring, point, ideal, or module substituted.",
    30: "The trace identity is derived from the full multiplicative homogeneous law in A[t,s]/(t^(n+1),s^2). The total-degree coefficient st^n vanishes and yields trace(h*chi_x(x))=0 integrally. All six generators then map to zero under the exact pi; q2 uses p_ta and pi(y)=0. The proof requires n>=1 and adapted data, not ProL or n! invertibility.",
    31: "Original GenBy gives density through the exact pair values and Unit section; PRG supplies algebraic generation by the actual splitting roots. Cotangent generators lift to m_R because the residue maps agree. Successive homogeneous corrections converge in R and prove actual surjectivity, not just dense image or surjectivity after localization.",
    32: "The equality of annihilators uses actual pi-surjectivity, followed by finite-module base-change support and the literal TWBase.supp at the contracted prime. The ideal is the same J. The normalized lifted-point support interface preserves all guards and leaves OoPair/OoPt/final Core assembly separate. Both rank-four Links, fixed iota, common coefficient threshold, and upstream Hida/ordinary/control/type producers remain explicit.",
}

PRIMARY = [
    ("PMS_NOETHERIAN", "https://stacks.math.columbia.edu/tag/00FM", "Lemmas 10.31.1, 10.31.2, 10.31.4", "turn188581469view0", "All base rings in these applications are Noetherian; variable sets are finite; the action algebras are submodules of finite endomorphism modules."),
    ("PMS_COMPLETION_FINITE", "https://stacks.math.columbia.edu/tag/00MA", "Lemma 10.97.1", "turn970270676view0", "The rings are Noetherian and every module for exactness/tensor comparison is finite. No exactness claim for arbitrary infinite modules is used."),
    ("PMS_COMPLETION_FLAT", "https://stacks.math.columbia.edu/tag/00MB", "Lemma 10.97.2", "turn970270676view1", "The actual localized completion is an ideal-adic completion of a Noetherian ring; flatness preserves the finite graded-piece exact sequences."),
    ("PMS_COMPLETION_QUOTIENTS", "https://stacks.math.columbia.edu/tag/031C", "Lemma 10.97.4", "turn970270676view2", "The finitely generated ideal is the displayed y-ideal or the specified local maximal ideal; the exact extended-ideal quotients are used."),
    ("PMS_COMPLETION_NOETHERIAN", "https://stacks.math.columbia.edu/tag/05GH", "Lemma 10.97.5", "turn970270676view3", "The original rings are Noetherian, so the quotient is Noetherian and the completion ideal is finitely generated."),
    ("PMS_FAITHFUL_LOCAL_COMPLETION", "https://stacks.math.columbia.edu/tag/00MC", "Lemma 10.97.3", "turn970270676view4", "The ring is the actual Noetherian localization at qBB and the ideal is its maximal ideal, hence lies in the Jacobson radical."),
    ("PMS_KRULL_INTERSECTION", "https://stacks.math.columbia.edu/tag/00IP", "Lemma 10.51.4", "turn188581469view2", "C is Noetherian local, its maximal ideal is proper, and N/I^kN is finite. This gives closedness before claiming I-adic completeness."),
    ("PMS_FINITE_ALGEBRA_FACTORS", "https://stacks.math.columbia.edu/tag/0325", "Lemma 10.160.2", "turn188581469view1", "La is Noetherian complete local and E_p tensor La is finite. Its factor is selected by the original q after reduction to the same residue field."),
    ("PMS_REGULAR_PARAMETERS", "https://stacks.math.columbia.edu/tag/00NQ", "Lemma 10.106.3", "turn188581469view3", "La is the supplied regular local coefficient completion and a minimal generating list of its maximal ideal is used."),
    ("PMS_REGULAR_PARAMETERS", "https://stacks.math.columbia.edu/tag/00NP", "Lemma 10.106.2", "turn188581469view4", "La and each successive regular parameter quotient are regular local; the domain conclusion supplies the exact prime chains."),
    ("PMS_HEIGHT", "https://stacks.math.columbia.edu/tag/0BBZ", "Lemma 10.60.12(1)", "turn391997917view0", "The relevant prime is minimal over the displayed finite generating list: the maximal ideal of La[[Y]], or the normalized prime itself."),
    ("PMS_MINIMAL_ASSOCIATED", "https://stacks.math.columbia.edu/tag/02CE", "Proposition 10.63.6", "turn391997917view1", "The module is C0 over the Noetherian ring C0. Its support is the full spectrum and each minimal prime is associated."),
    ("PMS_INTEGRAL_DIMENSION", "https://stacks.math.columbia.edu/tag/00OK", "Lemma 10.112.4", "turn391997917view2", "The actual extension A0->C0/Z0 is proved injective and finite, hence integral. Injectivity is not assumed from mere nonzero support."),
    ("PMS_COMPLETION_DIMENSION", "https://stacks.math.columbia.edu/tag/07NV", "Lemma 15.44.1", "turn391997917view3", "The localized coefficient ring at ker(g) is Noetherian local and its completion is the literal La in the source contract."),
    ("PMS_COMPLETION_DIMENSION", "https://stacks.math.columbia.edu/tag/07NY", "Lemma 15.44.4", "turn391997917view4", "The same localized ring is proved regular by the explicit parameter count and matching prime chain; maximal-ideal completion preserves regularity."),
]


def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def block(data: bytes, lo: int, hi: int) -> bytes:
    lines = data.splitlines(keepends=True)
    assert 1 <= lo <= hi <= len(lines), (lo, hi, len(lines))
    return b"".join(lines[lo - 1 : hi])


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--workspace", type=Path, default=Path(__file__).resolve().parents[2])
    ap.add_argument("--component", type=Path)
    ap.add_argument("--source", type=Path)
    ap.add_argument("--output", type=Path, default=Path(__file__).resolve().parent)
    args = ap.parse_args()
    root = args.workspace.resolve()
    component = (args.component or root / "work_v040/patched_support").resolve()
    source = (args.source or root / "lean_source").resolve()
    output = args.output.resolve()
    data = (component / "main.tex").read_bytes()
    prov_bytes = (component / "provenance.json").read_bytes()
    closure_bytes = (component / "closure.json").read_bytes()
    apps_bytes = (component / "published_applications.json").read_bytes()
    prov = json.loads(prov_bytes)
    closure = json.loads(closure_bytes)
    apps = json.loads(apps_bytes)
    assert prov["source_commit"] == closure["source_commit"] == PIN
    assert prov["proof_file_sha256"] == prov["main_tex_sha256"] == sha(data)
    assert closure["proof_file_sha256"] == closure["proof_sha256"] == sha(data)
    assert prov["published_applications"]["sha256"] == sha(apps_bytes)
    assert set(prov["published_applications"]["ids"]) == {a["id"] for a in apps}
    assert {a["id"] for a in apps} == {p[0] for p in PRIMARY}
    assert [c["id"] for c in prov["claims"]] == [f"PMS{i}" for i in range(1, 33)]
    assert closure["proof_claims"] == [f"PMS{i}" for i in range(1, 33)]

    files = {}
    for s in prov["source_files"]:
        path = s["path"]
        buf = (source / path).read_bytes()
        git = subprocess.check_output(["git", "show", f"{PIN}:{path}"], cwd=source)
        assert buf == git, path
        assert sha(buf) == s["sha256"] == s["full_file_sha256"], path
        if "file_sha256" in s:
            assert s["file_sha256"] == sha(buf), path
        if "bytes" in s:
            assert s["bytes"] == len(buf), path
        files[path] = buf
    src_rows = {}
    for s in prov["source_inventory"]:
        buf = files[s["path"]]
        assert s["source_commit"] == PIN
        assert s["sha256"] == s["full_file_sha256"] == sha(buf)
        rb = block(buf, s["line_start"], s["line_end"])
        assert sha(rb) == s["range_sha256"], s["id"]
        assert len(rb) == s["range_bytes"], s["id"]
        assert s["id"] not in src_rows
        src_rows[s["id"]] = s
    occurrences = 0
    claim_reviews = []
    for c in prov["claims"]:
        n = int(c["id"][3:])
        p = c["proof_location"]
        pb = block(data, p["line_start"], p["line_end"])
        assert sha(pb) == p["sha256"], c["id"]
        assert len(pb) == p["bytes"], c["id"]
        assert f"% BEGIN {c['id']}".encode() in pb and f"% END {c['id']}".encode() in pb
        for s in c["sources"]:
            assert s == src_rows[s["id"]], (c["id"], s["id"])
            occurrences += 1
        claim_reviews.append({"id": c["id"], "status": "PASS", "proof_range_sha256": p["sha256"], "proof_lines": [p["line_start"], p["line_end"]], "note": NOTES[n]})

    inherited = []
    for key in ["inherited_proof_inputs", "peer_proof_inputs"]:
        for entry in prov[key]:
            rel = entry["path"]
            candidates = [root / rel, root / "work_v040" / rel, root / "reconstruction_v040" / rel]
            path = next((p for p in candidates if p.is_file()), None)
            assert path is not None, rel
            ib = path.read_bytes()
            assert sha(ib) == entry["sha256"], rel
            for b in entry["claim_proof_blocks"]:
                bb = block(ib, b["line_start"], b["line_end"])
                assert sha(bb) == b["sha256"], b["id"]
                assert len(bb) == b["bytes"], b["id"]
                inherited.append({"id": b["id"], "path": rel, "file_sha256": sha(ib), "proof_range_sha256": b["sha256"], "role": entry["role"]})
    deps = {c["id"]: c["depends_on"] for c in prov["claims"]}
    allowed = set(deps) | {i["id"] for i in inherited}
    for name, dd in deps.items():
        assert set(dd) <= allowed, (name, set(dd) - allowed)
    visiting, done = set(), set()

    def visit(node):
        if node not in deps or node in done:
            return
        assert node not in visiting, node
        visiting.add(node)
        for dep in deps[node]:
            visit(dep)
        visiting.remove(node)
        done.add(node)

    for node in deps:
        visit(node)

    validation_path = component / "validation/validation.json"
    validation = json.loads(validation_path.read_bytes()) if validation_path.is_file() else None
    result = {
        "schema": "rh-independent-human-proof-review/1",
        "version": "0.40",
        "component": "patched_support",
        "reviewer": "audit_literature",
        "status": "PASS",
        "review_scope": "All PMS1--PMS32; independent mathematical and exact-source review, all 13 primary application certificates, quantifier and same-object checks, metadata and closure scope.",
        "source_commit": PIN,
        "standing_assumption": "Pinned Lean correctness is accepted. This is review of the human reconstruction; no Lean build or replay was run.",
        "proof_file": "patched_support/main.tex",
        "proof_file_sha256": sha(data),
        "provenance_file_sha256": sha(prov_bytes),
        "closure_file_sha256": sha(closure_bytes),
        "published_applications_file_sha256": sha(apps_bytes),
        "claims_reviewed": [f"PMS{i}" for i in range(1, 33)],
        "claim_reviews": claim_reviews,
        "resolved_findings": [
            {"id": "PMS_REVIEW_1", "claim": "PMS20", "severity": "precision", "finding": "The source quantifies over all natural coefficient indices, and its Nat subtraction does not make i>n coefficients zero.", "resolution": "Final proof states lambda_i=(-1)^(i-n)lambda_n for i>n, so the same finite quotient covers every source index.", "status": "resolved"},
            {"id": "PMS_REVIEW_2", "claim": "PMS32", "severity": "scope precision", "finding": "Selected Count-II wording should not restrict the general permitted odd-prime route to the illustrative ell=3 case.", "resolution": "Final proof applies at every permitted odd ell, including ell=3 when the original hypotheses hold, and preserves both Links and the common coefficient threshold.", "status": "resolved"}
        ],
        "unresolved_review_findings": [],
        "primary_sources_independently_opened": [{"application_id": i, "url": u, "locator": l, "retrieval_ref": r, "hypothesis_match": h, "status": "PASS"} for i, u, l, r, h in PRIMARY],
        "source_evidence_validation": {"pinned_files": len(files), "distinct_ranges": len(src_rows), "claim_source_references": occurrences, "proof_blocks": len(claim_reviews), "inherited_and_peer_blocks": len(inherited), "all_pinned_file_bytes_verified": True, "all_range_hashes_verified": True, "all_proof_block_hashes_verified": True, "all_inherited_file_and_block_hashes_verified": True, "local_claim_dependency_dag": "PASS"},
        "source_inventory_bound": [{"id": s["id"], "path": s["path"], "declaration": s["declaration"], "lines": [s["line_start"], s["line_end"]], "file_sha256": s["sha256"], "range_sha256": s["range_sha256"]} for s in prov["source_inventory"]],
        "inherited_proof_inputs_verified": inherited,
        "scope_checks": [
            "Full original universal S5, including arbitrary center index set and full move, is established on exactly its original antecedents.",
            "The arithmetic construction keeps the actual supplied TWAut and full RRObj/RMaps, rather than assuming an unconstructed patched module.",
            "One Lim ultrafilter precedes all level modules and centers; one piCong event precedes every R-scalar; one A.ex+1 precedes every relation and precision.",
            "The coefficient dimension requires the exact O->K surjection and Unit->t law; the same J is recovered by the actual TWBase.supp equivalence.",
            "The full determinant arguments are integral and valid at rank four in residue characteristic three, without n! inversion.",
            "OoPair/OoPt, final selected Core assembly, and original automorphic/ordinary/control/type/Hida production are separate scopes; no closure of COUNT_II_SUPPORT or unrestricted Core is inferred from PMS alone."
        ],
        "author_standalone_validation_observed": validation,
        "review_builder": {"file": "review_patched_support.py", "sha256": sha(Path(__file__).read_bytes()), "purpose": "Evidence binding only; mathematical findings are the written independent review above."},
        "new_lean_build": False,
    }
    output.mkdir(parents=True, exist_ok=True)
    out_json = output / "patched_support_review.json"
    out_json.write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n")
    lines = [
        "INDEPENDENT HUMAN-PROOF REVIEW: PATCHED SUPPORT, v0.40",
        "Status: PASS",
        "Reviewer: audit_literature",
        "Scope: all PMS1--PMS32, exact source, primary applications, and closure scope.",
        f"Pinned source: {PIN}",
        "The formal source is assumed checked and correct. No Lean build or replay.",
        "",
        "FINAL EVIDENCE BINDING",
        f"main.tex SHA256: {sha(data)}",
        f"provenance.json SHA256: {sha(prov_bytes)}",
        f"closure.json SHA256: {sha(closure_bytes)}",
        f"published_applications.json SHA256: {sha(apps_bytes)}",
        f"Verified: {len(files)} pinned files; {len(src_rows)} distinct ranges; {occurrences} claim-source references; 32 proof blocks; {len(inherited)} inherited/peer blocks.",
        "",
        "REVIEW FINDINGS",
        "No unresolved mathematical or scope issue was found. Two precision corrections were requested and resolved: all natural lambda indices under the original truncated subtraction; and every permitted odd ell rather than an ell=3-only shorthand.",
        "",
        "PER-CLAIM MATHEMATICAL REVIEW",
    ]
    for c in claim_reviews:
        lines.extend([f"{c['id']}: PASS. {c['note']}", f"Proof block SHA256: {c['proof_range_sha256']}", ""])
    lines.extend(["PRIMARY APPLICATIONS", "All thirteen application certificates were checked against fifteen primary pages. The ring, ideal, finiteness, local/completeness, regularity, and injectivity hypotheses are matched in the mathematical argument.", ""])
    for i, u, l, _, h in PRIMARY:
        lines.extend([f"{i}: {l}; {u}", f"Hypotheses: {h}", ""])
    lines.extend(["SCOPE", *result["scope_checks"], "", "This review certifies the human arguments at their stated scope. Source and proof hashes establish correspondence and reproducibility; they do not substitute for the mathematical review."])
    out_txt = output / "patched_support_review.txt"
    out_txt.write_text("\n".join(lines) + "\n")
    print(json.dumps({"status": "PASS", "main_sha256": sha(data), "provenance_sha256": sha(prov_bytes), "closure_sha256": sha(closure_bytes), "apps_sha256": sha(apps_bytes), "review_json_sha256": sha(out_json.read_bytes()), "review_txt_sha256": sha(out_txt.read_bytes()), "files": len(files), "ranges": len(src_rows), "references": occurrences, "proof_blocks": 32, "inherited_peer_blocks": len(inherited)}, indent=2))


if __name__ == "__main__":
    main()
