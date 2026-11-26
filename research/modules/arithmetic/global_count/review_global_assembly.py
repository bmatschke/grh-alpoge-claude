#!/usr/bin/env python3
"""Bind the independent GFA mathematical review to the reviewed final bytes."""
from pathlib import Path
import hashlib
import json
import subprocess

ROOT = Path(__file__).resolve().parents[2]
P = ROOT / "work_v034/global_assembly"
OUT = ROOT / "work_v034/reviews"
OUT.mkdir(parents=True, exist_ok=True)
PIN = "7cbf7a0c32fca1badf05931879a37c3f8a2b03b4"
sha = lambda b: hashlib.sha256(b).hexdigest()
expected = {
    "main.tex": "1e178c8bbe671dfdea7432ab04538a8a4c72cb84f0192fbce4ad347b850e7e70",
    "provenance.json": "890cdc5bc2bad45be0ae41dccb0fb6f0760decf5d9b9160d0b0c3e60d106710a",
    "closure.json": "73fc8a0aee0872d08f996491dabeda10050cef8a2e28a0703ecd69d128f0013d",
}
for f, h in expected.items():
    assert sha((P / f).read_bytes()) == h, f
j = json.loads((P / "provenance.json").read_text())
closure = json.loads((P / "closure.json").read_text())
raw = (P / "main.tex").read_bytes()
lines = raw.decode().splitlines(keepends=True)
assert j["source_commit"] == PIN
assert j["main_sha256"] == sha(raw)
assert closure["main_sha256"] == sha(raw)
assert closure["provenance_sha256"] == expected["provenance.json"]
assert len(j["claims"]) == 12
files, ranges, blocks = {}, set(), []
ref_count = 0
for c in j["claims"]:
    p = c["proof_location"]
    rb = "".join(lines[p["line_start"] - 1:p["line_end"]]).encode()
    assert p["sha256"] == p["range_sha256"] == sha(rb)
    assert p["file_sha256"] == sha(raw)
    assert "% BEGIN " + c["id"] in rb.decode()
    assert "% END " + c["id"] in rb.decode()
    blocks.append({"id": c["id"], "sha256": sha(rb),
                   "line_start": p["line_start"], "line_end": p["line_end"]})
    for a in c["sources"]:
        ref_count += 1
        path = a["path"]
        if path not in files:
            b = (ROOT / "lean_source" / path).read_bytes()
            git_b = subprocess.check_output(["git", "show", PIN + ":" + path],
                                            cwd=ROOT / "lean_source")
            assert b == git_b, path
            files[path] = b
        b = files[path]
        sl = b.decode().splitlines(keepends=True)
        sr = "".join(sl[a["line_start"] - 1:a["line_end"]]).encode()
        assert a["sha256"] == a["file_sha256"] == sha(b), path
        assert a["range_sha256"] == sha(sr), (path, a["declaration"])
        assert a["range_bytes"] == len(sr)
        assert a["first_line"] == sl[a["line_start"] - 1].rstrip()
        ranges.add((path, a["line_start"], a["line_end"], sha(sr)))
for a in j["inherited_proof_inputs"]:
    p = ROOT / "reconstruction_v033" / a["file"]
    if not p.exists():
        p = ROOT / "work_v034" / a["file"]
    assert p.is_file(), a
    assert sha(p.read_bytes()) == a["sha256"], p
assert "RSL11" in j["claims"][0]["depends_on"]
assert "GII3" in j["claims"][1]["depends_on"]
assert any(x["file"] == "type_two_family/main.tex" for x in j["inherited_proof_inputs"])

details = [
    (["GFA1"], "The actual lifted top weights give amax<=2a, Wt<=3b', k<=b' and bTop<=2b'; hence the original selected-place summand is at most 9(a/k+b'). The selected positions inject into the same TT. The appendage estimate concerns the absolute value of the negative appended weight, with the determinant shift retained."),
    (["GFA1"], "The original localized quotient length is n_w=e_w lenMN(u,w), and sum_(w|T) e_w log(Np_w)/[K:Q]<=log T. The squared-metric degree contributes 2 and the retained rank fraction is at least 1/2, giving exactly 36. GLE11's same-object inclusion activates RSL11; fullness of NuLat and of the actual ideal multiple Nu identifies lattice rank with the retained ambient dimension before division. The four other adm26 clauses and the zero-rank total-division boundary are matched."),
    (["GFA2"], "The actual Gp bound and p<X' imply log Qp<=Ce*x^(11epsilon/24)*log x<=x^(epsilon/2). Every displayed exponent in the two Dp/tv branches was checked from the literal formulas, including both rounding operations, the predecessor minimum, the branchwise distance-zero convention, and the original EpDef exponent. The resulting tau_p<=a*S^20 and crude prime count give Ta<=a*S^24<=b^2. Only this sufficient coarse bound is proved; the stronger weighted-prime/Mertens interface is not inferred."),
    (["GFA3"], "Local elementary divisors give the exact mean-slope correction with the same squared metrics. The finite denominator gives finite support. Maximal-ideal localization proves the global inclusion into the product ideal, and degree monotonicity in every rational subspace yields the maximal-slope bound. MT2 supplies precisely the same fractional-ideal shift, including negative signed floor values."),
    (["GFA4"], "TuSize gives T_u>=b^3>=X' eventually, so the actual VV definition forces tau_(T_u)=0. Every tau is a nonnegative integer. Kappa nonnegativity is now explicit from GK_nonneg and the nonempty nonnegative infimum defining kapI. Outside support the regular case uses lats0; the exceptional T_u case uses the j=1 positive EatT summand to force seenP=false, hence the empty ordered product, Nlam=Sram and zero local quotient. The same local objects are used throughout."),
    (["GFA5"], "The retained fraction delta=1-r/d is bounded by 2f/T. The floor error R is exactly the negative MT3 discrepancy and is nonnegative. The type cost, total Ta and ramified mean loss have the stated constants. The two factors giving 4*IOsum are preserved. The listed s', delta, reference slopes, type cost and floor error satisfy all original Places_at fields; the resulting upper/lower inequalities are the literal SlopesN_at. Thresholds precede members, words and places."),
    (["GFA6"], "A zero full target would make the diagonal kernel zero and force its squared Hilbert-Schmidt defect to equal positive d_u, contradicting e0<1. LinkIRR and RRFull then give positive actual RR rank. The dual is the algebraic O_K dual with its original metric; annihilators and metric quotients give mu_min(RR^vee)=-mu_max(RR), without a codifferent or trace-dual normalization. With full positive Nu rank, this is exactly Lat_at."),
    (["GFA7"], "The original nonnegative period factor is strictly positive by the same diagonal defect. Its inverse square root produces the exact Gram blocks. BesselId supplies one common designated embedding, the original rational map and nonzero scalar; source basis changes and the inverse transpose target change are invertible. The identity-or-conjugation representative change is applied to every matrix together. Integrality and nonzero-map heights are precisely the retained LinkDIV fields, while LinkS provides the actual mixed, diagonal and full-target estimates."),
    (["GFA8"], "Inherited GF8 applies to every H>0 with s-mu_min(RR^vee)<=H, with no upper restriction. Its source average is exactly s and maximal adjusted slope is s+u. For u>0 the elementary integral inequality converts 4uH/(u+H) to 4u log(1+H/u); for u=0 both expressions are zero under the source convention. The replacements 4d<=3sqrt(d), e=2e0 and subtraction of the nonnegative log word count give the literal full Frame_at predicate."),
    (["GFA9"], "The rank discard is bounded uniformly by 2f/b<=exp(-2*x^(epsilon/8)). The chosen d, eB and etaB depend on x and fixed CH, not the family member. The single threshold gives (etaB+4sqrt(eB))*x^CH<=6. Source discard and target discard remain separate. The resulting quantifier order is exactly FrameF."),
    (["GFA10"], "The inverse of the actual gcode/eTau map represents every rho in Phi. The two sign coordinates and the injective integer group label identify thick nodes with the original second set and original u0. The top, thin and thick intervals follow from the same stored weight windows, eta bound and rho inequality. The arbitrary frame/rank equalities in Nodes_at transport to these exact objects, and the unused unrepresented-code convention is retained."),
    (["GFA11"], "All seventeen Win_at clauses were checked in source order. The loose m/k windows and the separate exact k_up condition are not conflated. The source root-discriminant bound, QS tie, SizeN exponent and SizeQD windows give 0<=La<=2*x^epsilon. Both small-error clauses retain their constants. ThickSetDensityEventually is still an explicit same-family premise. The exact order forall c6>0 exists eK=5,x0 forall x>=x0 forall i is preserved."),
    (["GFA12"], "The primitive-character uniqueness proof is elementary and valid: CRT chooses unit representatives avoiding a finite exceptional set, multiplicativity identifies the induced characters, and nested prime-power reduction kernels give the minimum conductor. WB1 then identifies every positive integer value, including ramified primes, for the exact reciprocity reading. The sign swap in tE, all finite ramp terms and centering, the original Host.flPS quadratic identities, the same real logarithmic derivative and all four Char_at fields are retained. ChThin and ChQD remain supplied estimates; threshold zero for CharF adds no arithmetic estimate."),
    (["GFA1", "GFA2", "GFA3", "GFA4", "GFA5", "GFA6", "GFA7", "GFA8", "GFA9", "GFA10", "GFA11", "GFA12"], "The closure ledger claims complete conditional consumers only. It retains the original compatible family/selector/second layer, Duty/ChosenWall, local gain, spectral, retained-defect and period-map inputs. LossFS(Fm,0), the exact common-family linkCore/ChainTied assembly and its final Closed cutoff/transport wrapper remain explicit B work. No whole RH/GRH closure or Lean replay is claimed."),
]
checks = [{"id": f"GFA-REV-{i:02}", "claims": claims, "result": "PASS", "finding": text}
          for i, (claims, text) in enumerate(details, 1)]
review = {
    "schema": "rh-independent-proof-review/1", "artifact_version": "0.34",
    "reviewer": "/root/audit_global_routes", "date": "2026-11-22",
    "component": "global_assembly", "status": "PASS", "verdict": "PASS",
    "scope": "Independent mathematical and exact-source review of GFA1-GFA12 on the original supplied family. The pinned Lean proof is assumed correct; this review concerns the complete human implications and their retained antecedents.",
    "source_commit": PIN,
    "claims_reviewed": [c["id"] for c in j["claims"]],
    "proof_file": "global_assembly/main.tex",
    "provenance_file": "global_assembly/provenance.json",
    "closure_file": "global_assembly/closure.json",
    "proof_file_sha256": expected["main.tex"], "main_sha256": expected["main.tex"],
    "provenance_file_sha256": expected["provenance.json"],
    "closure_file_sha256": expected["closure.json"],
    "proof_blocks": blocks,
    "source_validation": {
        "claim_source_ranges_checked": ref_count,
        "distinct_source_ranges_checked": len(ranges),
        "pinned_files_checked": len(files),
        "all_ranges_and_blobs_match": True,
        "all_proof_block_hashes_match": True,
        "inherited_input_hashes_checked": len(j["inherited_proof_inputs"]),
        "all_inherited_input_hashes_match": True,
    },
    "checks": checks,
    "resolved_issues": [
        {"id": "GFA-RANK-BINDING", "claims": ["GFA1"], "resolution": "The final proof explicitly passes through RSL11, fullness of NuLat, actual NuFull of its ideal multiple, NuV_finrank and NuFull.rank before identifying the actual lattice rank with the retained dimension. The appended-weight statement is explicitly about absolute value."},
        {"id": "GFA-KAPPA-NONNEGATIVE", "claims": ["GFA4"], "resolution": "Both kappa branches are justified directly from GK_nonneg and Extra.kapI_def; the latter feasible set is nonempty because kappa=1 admits the zero-dimensional choice."},
        {"id": "GFA-METADATA-COVERAGE", "claims": ["GFA1", "GFA2"], "resolution": "RSL11, GII3, the full type_two_family inherited file, original EpDef/Extra and actual rank dictionary source ranges are included. The final GVC metadata is rebound after its wording-only peer-review corrections."},
    ],
    "required_corrections": [],
    "retained_hypotheses": closure["not_closed"],
    "limitations": [
        "No new Lean build or independent kernel replay was performed.",
        "Inherited mathematical results are used only in their recorded scope; the review verifies their input hashes and checks the applications relevant here.",
        "This is not an assertion that any open producer exists or that the entire human RH/GRH proof is complete.",
    ],
}
(OUT / "global_assembly_review.json").write_text(json.dumps(review, ensure_ascii=False, indent=2) + "\n")
text = [
    "GLOBAL ASSEMBLY GFA1-GFA12 — INDEPENDENT REVIEW — PASS",
    "Reviewer: /root/audit_global_routes",
    "Version: 0.34; date: 22 November 2026",
    "Source pin: " + PIN,
    "",
    review["scope"],
    "",
    "Frozen proof SHA256: " + expected["main.tex"],
    "Frozen provenance SHA256: " + expected["provenance.json"],
    "Frozen closure SHA256: " + expected["closure.json"],
    "",
    f"Independent byte checks: {ref_count} claim/source references, {len(ranges)} distinct ranges in {len(files)} pinned files, all 12 proof blocks, and {len(j['inherited_proof_inputs'])} inherited inputs. All match.",
    "",
]
for item in checks:
    text.extend([item["id"] + " (" + ", ".join(item["claims"]) + "): PASS", item["finding"], ""])
text.extend(["RESOLVED REVIEW FINDINGS", ""])
for item in review["resolved_issues"]:
    text.extend([item["id"] + ": " + item["resolution"], ""])
text.extend(["REQUIRED CORRECTIONS: none.", "", "RETAINED BOUNDARIES", ""])
text.extend("- " + s for s in review["retained_hypotheses"])
text.extend(["", "No new Lean replay, open-producer existence, or complete human RH/GRH proof is certified.", ""])
(OUT / "global_assembly_review.txt").write_text("\n".join(text))
print(json.dumps({"status": "PASS", "source_references": ref_count,
                  "distinct_ranges": len(ranges), "source_files": len(files),
                  "inherited_inputs": len(j["inherited_proof_inputs"]),
                  "review_json_sha256": sha((OUT / "global_assembly_review.json").read_bytes()),
                  "review_txt_sha256": sha((OUT / "global_assembly_review.txt").read_bytes())}, indent=2))
