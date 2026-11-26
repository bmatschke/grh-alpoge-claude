#!/usr/bin/env python3
"""Bind the completed independent mathematical review to the checked bytes."""
from pathlib import Path
import hashlib
import json
import subprocess

ROOT = Path(__file__).resolve().parents[2]
HERE = Path(__file__).resolve().parent
COMP = ROOT / "work_v036" / "regular_quotient"
SOURCE = ROOT / "lean_source"
HUMAN = ROOT / "reconstruction_v035"
sha = lambda b: hashlib.sha256(b).hexdigest()
pin = "7cbf7a0c32fca1badf05931879a37c3f8a2b03b4"
proof_bytes = (COMP / "main.tex").read_bytes()
proof_lines = proof_bytes.splitlines(keepends=True)
prov_bytes = (COMP / "provenance.json").read_bytes()
closure_bytes = (COMP / "closure.json").read_bytes()
prov, closure = json.loads(prov_bytes), json.loads(closure_bytes)
assert prov["source_commit"] == closure["source_commit"] == pin
assert prov["main_tex_sha256"] == closure["main_tex_sha256"] == sha(proof_bytes)
assert closure["provenance_sha256"] == sha(prov_bytes)

files, ranges = {}, set()
for s in prov["source_inventory"]:
    path = s["path"]
    if path not in files:
        b = (SOURCE / path).read_bytes()
        assert b == subprocess.check_output(["git", "show", pin + ":" + path], cwd=SOURCE), path
        files[path] = b
    b = files[path]
    part = b"".join(b.splitlines(keepends=True)[s["line_start"] - 1:s["line_end"]])
    assert sha(b) == s["sha256"] == s["file_sha256"], path
    assert sha(part) == s["range_sha256"], s["id"]
    assert len(part) == s["range_bytes"], s["id"]
    ranges.add((path, s["line_start"], s["line_end"]))

notes = {
 "RQC1": "Countable restricted products, the finite module topology, the closed unitary matrix equation, norm-based rational discreteness and countability match the original group. Discreteness is used as subgroup discreteness, giving closedness.",
 "RQC2": "Countable rational translates of the supplied null measurable domain partition almost everywhere. Left Haar invariance and Tonelli give unfolding and domain independence without renormalization.",
 "RQC3": "A quotient null set lifts to a null set on the supplied domain, and countably many rational translates give global AE on all GA. Completed exceptional sets are covered by measurable null sets.",
 "RQC4": "The right-translation composition order and pullback order match the original monoid homomorphism. Right invariance and fundamental-domain independence preserve exactly nuQ.",
 "RQC5": "The rational-saturation comparison inequality is correct; compact approximation of a finite-measure lift gives continuity of indicators, then simple functions, then all L2 vectors by uniform isometry.",
 "RQC6": "The val, iso and cont fields of IsReg all hold on the same quotient space and measure. The val field is global AE. Restriction to the original fundamental domain proves equality with any supplied IsReg.",
 "RQC7": "Appending the derivative variable proves stability of the full smooth subspace. Group conjugation and the Hermitian real-form decomposition retain the original derivatives and do not assume unbounded operators are continuous.",
 "RQC8": "Cayley/product coordinates justify directional linearity; left-invariant fields give the bracket with the correct sign. The conjugate-first formal adjoint is H^(-1)Z*H, agreeing with minus conjH in the source.",
 "RQC9": "Actual frame conjugation and HCU14 match atTau/oneP. Ordered separate equivariance proves the original all-word smoothness for an arbitrary inner-product target and operator monoid homomorphism; no target unitarity or strong continuity is added.",
 "RQC10": "The induction preserves the literal right-fold order and the ordered per-place filters. Derivative stability keeps the whole tuple in the original smooth spaces. HCU18 explicitly supplies the unchanged finite eigenlaw.",
 "RQC11": "The multiplicity bound uses Gamma intersect KK^(-1), with the correct left-translate order. Unfolding and Cauchy--Schwarz yield the local L1 estimate from the same global L2 norm.",
 "RQC12": "Finite compactly supported averaging is continuous. Tonelli and left Haar invariance yield the K Omega local L1 bound and the original finite-domain estimate.",
 "RQC13": "Continuous orbit representatives and the uniform compact-average L1 estimate pass zero averages to a closed orbit span. The proof never restricts an arbitrary ambient L2 class to a measure-zero subgroup.",
 "RQC14": "CTC1 identifies the actual algebraically generated transvection subgroup with A_F. Its rational subgroup is discrete cocompact. The countable Borel minimum construction gives a compactly contained domain for every Haar measure; domain independence includes absolute convergence.",
 "RQC15": "Every original isotropic vector, Haar measure and rational domain is retained. Pushing the compactly contained subgroup domain to GA and then transferring the integral proves literal ZCusp, including the vacuous anisotropic case.",
 "RQC16": "The seed ZCusp assumption is explicit. The actual HCU18 map lies in the same closed orbit span. Continuous representative uniqueness upgrades finite eigenlaws to pointwise ones; the original open finite level and CTC12 give genuine cusp for supplied representatives.",
 "RQC17": "The matrix identity E_p=p^T E (p^(-1))^T has the correct entry indices. Trace cycling is used only with a scalar-entry matrix, never between arbitrary noncommutative operator matrices.",
 "RQC18": "The adjacent-inversion/shorter-length induction proves only the needed ordered-word spanning. Each nonzero commutator preserves weight. Upper factors kill the highest vector, and strictly lower-only words cannot have total zero weight.",
 "RQC19": "Reversing and transposing closed paths gives the formal adjoint sum in the H^(-1) frame; RQC17 removes that frame. Covariance, symmetry and reality of the highest-vector scalar all have the stated inner-product convention.",
 "RQC20": "The explicit OrthFr determinant/Gram argument supplies nonsingularity. Irreducibility makes the actual highest-vector orbit dense. Pairing the already defined operator value with this orbit proves the scalar identity on every original smooth vector without extending an unbounded operator.",
 "RQC21": "HolShape, matching WtIs and original IsExtVec are now explicit. Complex-word transport uses only the supplied real pointwise derivative identities and multilinearity. The same one-dimensional span witnesses all original zfin operators, including zero/empty cases.",
 "RQC22": "The matching HolShape/WtIs/IsExtVec and IsInfFam guards are explicit; the separate seed ZCusp guard is retained for cusp. IsReg is genuinely removed on the supplied FinPair, while actual FinPair/boundedness and pointwise Sobolev representative production remain open."
}
assert set(notes) == {c["id"] for c in prov["claims"]}
claims = []
for c in prov["claims"]:
    loc = c["proof_location"]
    part = b"".join(proof_lines[loc["line_start"] - 1:loc["line_end"]])
    assert sha(part) == loc["sha256"], c["id"]
    assert len(part) == loc["bytes"], c["id"]
    assert part.startswith(("% BEGIN " + c["id"]).encode())
    assert part.rstrip().endswith(("% END " + c["id"]).encode())
    claims.append({
        "id": c["id"], "status": "PASS",
        "proof_range": loc, "depends_on": c["depends_on"],
        "review": notes[c["id"]],
        "source_ids_reviewed": c["source_ids"],
    })

inherited = []
for h in prov["baseline_dependencies"]:
    b = (HUMAN / h["file"]).read_bytes()
    lines = b.splitlines(keepends=True)
    assert sha(b) == h["sha256"] == h["file_sha256"], h["file"]
    for c in h["claims"]:
        part = b"".join(lines[c["line_start"] - 1:c["line_end"]])
        assert sha(part) == c["sha256"], c["id"]
        assert len(part) == c["bytes"], c["id"]
        inherited.append(c["id"])

text = proof_bytes.decode()
assert "If the same seed also satisfies" in text and r"\mathrm{ZCusp}(V,\phi)" in text
assert r"\mathrm{WtIs}(M,w)" in text and r"\mathrm{IsExtVec}(M,v_0)" in text
assert "HCU18" in next(c for c in prov["claims"] if c["id"] == "RQC10")["depends_on"]
assert "HCU17" in next(c for c in prov["claims"] if c["id"] == "RQC22")["depends_on"]
assert closure["selected_top_level_leaf_closed"] is False

record = {
    "schema": "rh-independent-mathematical-review/1",
    "version": "0.36", "date": "2026-11-22",
    "component": "regular_quotient",
    "reviewer": "/root/audit_literature", "author": "/root",
    "status": "PASS", "scope": "Independent mathematical and exact-source/quantifier review of all RQC1–RQC22, plus byte/range validation.",
    "source_commit": pin,
    "proof_file": "regular_quotient/main.tex",
    "proof_file_sha256": sha(proof_bytes),
    "provenance_file_sha256": sha(prov_bytes),
    "closure_file_sha256": sha(closure_bytes),
    "claims_reviewed": list(notes),
    "claim_reviews": claims,
    "resolved_findings": [
        {"id": "RQC-REVIEW-1", "scope": "RQC22", "finding": "HolForm by itself does not include seed cuspidality.", "resolution": "The final statement and proof explicitly retain ZCusp(V,phi) for every cusp conclusion."},
        {"id": "RQC-REVIEW-2", "scope": "RQC21/RQC22", "finding": "The original model/weight/extremal guards should not be compressed into an unspecified holomorphic model.", "resolution": "HolShape(M), WtIs(M,w), IsExtVec(M,v0), and IsInfFam(theta) are explicitly retained in the final appropriate statements."},
        {"id": "RQC-REVIEW-3", "scope": "RQC10 metadata", "finding": "The final unchanged finite-level eigenlaw uses HCU18.", "resolution": "The direct HCU18 edge is present; the inherited HCU18 proof block is hash-bound."},
        {"id": "RQC-REVIEW-4", "scope": "RQC20 and RQC15", "finding": "An HCU1 cross-reference and a nonessential CTC12 aside were not direct declared proof inputs.", "resolution": "RQC20 proves its Gram/nonsingularity facts explicitly; RQC15 removes the unused aside."}
    ],
    "open_findings": [],
    "validation": {
        "proof_blocks_verified": len(claims),
        "source_inventory_ranges_verified": len(prov["source_inventory"]),
        "distinct_source_ranges_verified": len(ranges),
        "pinned_source_files_verified": len(files),
        "claim_source_occurrences_verified": sum(len(c["sources"]) for c in prov["claims"]),
        "inherited_claim_blocks_verified": len(inherited),
        "inherited_claims": inherited,
        "pinned_git_blob_comparison": True,
        "all_file_and_range_hashes_matched": True,
        "new_lean_build": False,
        "tex_review": "Not part of this mathematical review; author performs the separate draft syntax/layout check."
    },
    "boundary": "These B implications remove IsReg, smooth-map, cusp-closure and scalar-action subtargets on their stated original inputs. Actual FinPair/boundedness and pointwise smooth/Sobolev representative production remain C; no full theta extension or RH/GRH closure is asserted."
}
(HERE / "regular_quotient_review.json").write_text(json.dumps(record, indent=2, ensure_ascii=False) + "\n")
out = [
    "INDEPENDENT MATHEMATICAL REVIEW — REGULAR QUOTIENT v0.36",
    "Reviewer: /root/audit_literature; author: /root",
    "Result: PASS for RQC1–RQC22.",
    "Source pin: " + pin,
    "",
    "Bound proof SHA256: " + record["proof_file_sha256"],
    "Bound provenance SHA256: " + record["provenance_file_sha256"],
    "Bound closure SHA256: " + record["closure_file_sha256"],
    "",
    "The review independently checked every claim's mathematics, original",
    "definitions and quantifier scope. It also verified each proof range,",
    "each listed source range, all source files against the pinned git blobs,",
    "and all listed inherited human proof ranges. No Lean replay was performed.",
    "",
    "VALIDATED SCOPE",
    "The finite pair and quotient-measure normalization stay unchanged.",
    "Repr is global almost-everywhere equality on GA. The full IsReg producer",
    "is proved on that supplied pair, including uniqueness of any IsReg.",
    "All derivative words keep their original order and unchanged finite level.",
    "Cusp closure treats every original ZI, Haar measure and rational domain,",
    "and uses compact-average L1 control, not restriction of an arbitrary L2",
    "class to a subgroup. The Gelfand scalar proof uses only scalar-entry",
    "trace cycling, weight-preserving ordered-word spanning, formal symmetry",
    "and density of the actual highest-vector orbit.",
    "",
    "RESOLVED REVIEW FINDINGS",
]
for f in record["resolved_findings"]:
    out += [f["id"] + " (" + f["scope"] + "): " + f["finding"], "  " + f["resolution"]]
out += ["", "PER-CLAIM REVIEW"]
for c in claims:
    out += [c["id"] + " — PASS", c["review"], "Proof-range SHA256: " + c["proof_range"]["sha256"], ""]
v = record["validation"]
out += [
    "HASH AND SOURCE ACCOUNTING",
    f"{v['proof_blocks_verified']} proof blocks; {v['source_inventory_ranges_verified']} source ranges",
    f"({v['distinct_source_ranges_verified']} distinct); {v['pinned_source_files_verified']} pinned source files;",
    f"{v['claim_source_occurrences_verified']} claim-source occurrences; {v['inherited_claim_blocks_verified']} inherited proof blocks.",
    "All checked file and range hashes match.",
    "",
    "BOUNDARY",
    record["boundary"],
    "There are no open mathematical findings in the reviewed component.",
    "TeX syntax/layout validation is separately owned by the author.",
]
(HERE / "regular_quotient_review.txt").write_text("\n".join(out) + "\n")
print(json.dumps({
    "status": "PASS", "proof_sha256": sha(proof_bytes),
    "review_json_sha256": sha((HERE / "regular_quotient_review.json").read_bytes()),
    "review_txt_sha256": sha((HERE / "regular_quotient_review.txt").read_bytes()),
    **record["validation"]
}, indent=2))
