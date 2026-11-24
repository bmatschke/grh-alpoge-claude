#!/usr/bin/env python3
"""Bind the completed independent SPR1–SPR25 mathematical review.

This is a byte/source-binding check, not an automated proof checker.
The substantive review is recorded in the per-claim notes below.
No Lean build is performed.
"""
from pathlib import Path
import argparse
import hashlib
import json
import subprocess

HERE = Path(__file__).resolve().parent
p = argparse.ArgumentParser(description=__doc__)
p.add_argument("--component", type=Path, default=HERE.parent / "smooth_representatives")
p.add_argument("--source", type=Path, default=HERE.parents[1] / "lean_source")
p.add_argument("--human-root", type=Path, default=HERE.parents[1] / "reconstruction_v036")
p.add_argument("--peer-root", type=Path, default=HERE.parent)
a = p.parse_args()
COMP, SOURCE, HUMAN, PEER = a.component.resolve(), a.source.resolve(), a.human_root.resolve(), a.peer_root.resolve()
PIN = "7cbf7a0c32fca1badf05931879a37c3f8a2b03b4"
EXPECTED_MAIN = "fad0f86c8abd6fd9373ba23feda6128447127722b11c9c9170441aee9d2370c1"
sha = lambda b: hashlib.sha256(b).hexdigest()
main = (COMP / "main.tex").read_bytes()
assert sha(main) == EXPECTED_MAIN, "Mathematical text changed; inspect changes before refreshing the review."
prov_bytes = (COMP / "provenance.json").read_bytes()
close_bytes = (COMP / "closure.json").read_bytes()
prov, closure = json.loads(prov_bytes), json.loads(close_bytes)
assert prov["source_commit"] == closure["source_commit"] == PIN
assert subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=SOURCE, text=True).strip() == PIN
assert prov["main_tex_sha256"] == closure["main_tex_sha256"] == sha(main)
assert closure["provenance_sha256"] == sha(prov_bytes)
lines = main.splitlines(keepends=True)
claims = prov["claims"]
assert [c["id"] for c in claims] == [f"SPR{i}" for i in range(1,26)]
for c in claims:
    q = c["proof_location"]
    b = b"".join(lines[q["line_start"]-1:q["line_end"]])
    assert b.splitlines()[0] == ("% BEGIN " + c["id"]).encode()
    assert b.splitlines()[-1] == ("% END " + c["id"]).encode()
    assert sha(b) == q["sha256"] and len(b) == q["bytes"]

files = {}
ranges = {}
for s in prov["source_inventory"]:
    path = s["path"]
    if path not in files:
        b = (SOURCE / path).read_bytes()
        assert b == subprocess.check_output(["git", "show", PIN + ":" + path], cwd=SOURCE), path
        files[path] = b
    b = files[path]
    assert sha(b) == s["file_sha256"] == s["sha256"]
    r = b"".join(b.splitlines(keepends=True)[s["line_start"]-1:s["line_end"]])
    assert sha(r) == s["range_sha256"] and len(r) == s["range_bytes"]
    ranges[s["id"]] = s
for c in claims:
    assert c["source_ids"] == [s["id"] for s in c["sources"]]
    for s in c["sources"]:
        assert s == ranges[s["id"]]

inherited = []
incoming_ids = set()
for item in prov["baseline_dependencies"]:
    candidates = [PEER / item["file"], HUMAN / item["file"]]
    matches = [path for path in candidates if path.is_file() and sha(path.read_bytes()) == item["file_sha256"]]
    assert matches, item["file"]
    b = matches[0].read_bytes()
    assert sha(b) == item["sha256"]
    ll = b.splitlines(keepends=True)
    for c in item["claims"]:
        bb = b"".join(ll[c["line_start"]-1:c["line_end"]])
        assert sha(bb) == c["sha256"] and len(bb) == c["bytes"]
        assert bb.splitlines()[0] == ("% BEGIN " + c["id"]).encode()
        assert bb.splitlines()[-1] == ("% END " + c["id"]).encode()
        incoming_ids.add(c["id"])
    inherited.append({"file": item["file"], "file_sha256": sha(b), "claims": [c["id"] for c in item["claims"]]})
for c in claims:
    assert all(d in {v["id"] for v in claims} | incoming_ids for d in c["depends_on"])

asb = json.loads((PEER / "adelic_sobolev/provenance.json").read_bytes())
assert asb["main_tex_sha256"] == sha((PEER / "adelic_sobolev/main.tex").read_bytes())
graph = {c["id"]: c["depends_on"] for c in claims + asb["claims"]}
visiting, done = set(), set()
def visit(cid):
    if cid in done or cid not in graph:
        return
    assert cid not in visiting, "Cycle involving " + cid
    visiting.add(cid)
    for d in graph[cid]:
        visit(d)
    visiting.remove(cid)
    done.add(cid)
for cid in graph:
    visit(cid)
assert "SPR13" in graph["ASB14"]
assert all(not d.startswith("SPR") or d == "SPR13" for d in graph["ASB14"])
assert {"ASB3","ASB4"} <= set(graph["SPR13"])

notes = {
 1: "AE linearity gives bounded local L1 maps. Compact-test equality is promoted to global AE by regularity and a countable compact exhaustion. Continuous representatives are unique by full Haar support; injectivity of iota is unnecessary.",
 2: "Compact parameter integration commutes with bounded compact-integration functionals; joint continuity and compact domination give continuity. Fubini is applied to a genuine continuous product integrand, avoiding an unsupported common exceptional set.",
 3: "The change z=x*y uses left Haar invariance. Compact support and the given local L1 bound give domination and continuity; product measurability/null-set replacement is justified by left-translation slices and Fubini. Hilbert averaging is integrable by strong continuity/isometry.",
 4: "The compact bump is supported inside the same open normalizing subgroup. Conjugation y^-1 H y preserves H-fixedness; normalized averaging approximates the vector. The level is not shrunk as an approximation varies.",
 5: "Evaluation is linear by uniqueness, bounded on the supplied subspace, and extends to its closure. Orthogonal projection extends it to all H. Compact-uniform limits give continuity; the local L1 map identifies the represented Hilbert limit globally.",
 6: "Right invariance transports existing representatives, making a continuous representative H-invariant. The exact scalar comparison yields compact-uniform evaluation bounds. Closure and fixed-level averaging density supply the full exists_eval contract.",
 7: "The one-parameter derivative transports to every real time. Integration of ((s-r)/s)rho(c(r))w gives the stated minus sign and normalization. No pointwise derivative of an AE class is used.",
 8: "The inductive insertion appends c_(N+1) to the group product and prepends d_(N+1) to the vector derivative. The explicit source right-fold word is the reverse of the increasing selected subset. No derivatives commute; the zero-dimensional cube is included.",
 9: "The strengthened parameter-smoothness condition is closed under left finite words and partial differentiation. Bounded outer operators pass through the derivative. Exact source generality is now explicit: topology on G, strong continuity and isometry are not required.",
 10: "Strongly continuous Hilbert derivatives integrate first; their continuous representatives are then identified by uniqueness. The ordinary FTC gives the pointwise derivative. Isometry is explicitly dropped, matching the generic source signature.",
 11: "The same derivative-stable H-fixed set uses one finite collection of cube weights and evaluations. The representative assignment works simultaneously for every vector in that set; finite sums and cube identity give the global representative law.",
 12: "Translated smooth vectors remain in the same fixed space. The finite evaluation formula and parameter-smooth derivatives give joint curve-product smoothness without assuming derived operators are bounded. One-letter transfer and induction give all original right folds.",
 13: "RQC pullbacks supply the original quotient measure/global-AE law, compact L1 bound and arbitrary IsReg. The actual ASB chart and comparison meet the generic hypotheses. One representative has every derivative identity and invariance under the SAME prescribed U intersect Gf.",
 14: "The Hilbert multilinear map is realized pointwise by unique continuous representatives. Additivity and scalar identities in each slot therefore hold everywhere. The whole original smooth span is used, not an alternate dense subspace.",
 15: "Finite character and one-place equivariance are identities of the same Hilbert vector and hence of its continuous representatives. J, chi, original atTau and the actual updated smooth tuple are retained.",
 16: "RQC7/9/10 and SPR13 transfer every Hilbert derivative to the corresponding updated pointwise tuple. Per-place filters preserve the source right-fold order, and common finite fixedness survives all words.",
 17: "ASB14 chooses N and its finite test list before every vector/representative. Applying it to each derived tuple produces one N before y and the outer derivative word. No claim of uniformity across changed initial levels is inserted.",
 18: "The previously retained pointwise derivative premise of RQC21 is now supplied by SPR16. Exact Gelfand-cycle scalars make span{T(y)} invariant for every place and cycle index, including T(y)=0, with no circular initial boundedness argument.",
 19: "The Hilbert image lies in the closed full regular orbit span of the same bounded seed. The independent RQC cusp-closure theorem applies to its continuous automorphic representative and separate seed ZCusp; CTC12 gives all original unipotent cusp clauses.",
 20: "Point evaluation is bounded by a finite list of exact filtered Hilbert derivative norms. Fixing other slots gives the required separate Sobolev2 estimate. Algebraic extension off the full smooth subspace preserves that estimate on every original SmoothVec; Hilbert-norm boundedness is not claimed.",
 21: "All five original IsMultMap fields are supplied explicitly. Equality at the initial extremal tuple follows from the same L2 seed and continuous uniqueness. Bounded HolForm, target FinPair and separate seed ZCusp remain genuine premises.",
 22: "LowIrr is the algebraic invariant-subspace irreducibility required for compact orbit span, not merely topological irreducibility. Original frame conjugation and both equivariance laws propagate equality; finite multilinear expansion proves the entire RestrictsTo predicate.",
 23: "HCU19 supplies the exact holomorphic seed from compact equivariance, smoothness and lowering. The separate bounded seed and target FinPair then feed SPR21; unit extremal components allow SPR22. This is a conditional extension consumer, not a rapid-decay or volume proof.",
 24: "Hamel-basis choice constructs a linear lift for arbitrary source dimension. The same integrable bilinear theta integral is defined on range(ext) itself, so no preimage ambiguity or injectivity hypothesis occurs. Literal original IsThetaP and IsThetaMult contracts are matched.",
 25: "The same R and one io_i precede all t. Exact principal-level conditions use both integral matrices and Norm(P) congruences for Pg union Q; the subgroup preimage is open and lies in the original levS on Gf. TAE/CTC supply integrability/smoothness/lowering/ZCusp; only target FinPair and initial extremal boundedness remain before the full original FiresAt and linear theta-family consumers.",
}
assert set(notes) == set(range(1,26))
findings = [
    {"id": "SPR_REVIEW_METADATA", "status": "resolved",
     "finding": "Direct inherited edges for HCU16 in SPR15 and RQC7/HCU16 in SPR16 were missing from the draft metadata.",
     "resolution": "Final per-claim edges and the inherited RQC7 proof block are present and byte verified."},
    {"id": "SPR_REVIEW_PRINCIPAL_LEVEL", "status": "resolved",
     "finding": "The original open-level argument needed an explicit check of its actual conjugation, both matrices, and both finite flag sets.",
     "resolution": "SPR25 now uses T=Pg union Q, integral m and m^-1, Norm(P) divisibility of m-I, trivial reductions, Kg<=lev and the open subgroup preimage. Four direct source declarations were added."},
    {"id": "SPR_REVIEW_GENERIC_SCOPE", "status": "resolved",
     "finding": "The chapter-wide isometry/topology assumptions obscured the stronger generic scope actually proved in SPR9/10.",
     "resolution": "SPR9 explicitly drops topology/strong continuity/isometry; SPR10 drops isometry while retaining strong continuity and representative hypotheses. The proofs and actual adelic application are unchanged."},
]
record = {
    "schema": "rh-independent-component-review/1", "version": "0.37",
    "component": "smooth_representatives", "reviewer": "/root/audit_literature",
    "status": "PASS", "source_commit": PIN, "claims_reviewed": [c["id"] for c in claims],
    "proof_file_sha256": sha(main), "provenance_file_sha256": sha(prov_bytes),
    "closure_file_sha256": sha(close_bytes), "all_required_corrections_resolved": True,
    "per_claim_reviews": [
        {"claim": c["id"], "status": "PASS", "proof_sha256": c["proof_location"]["sha256"],
         "source_ids_reviewed": c["source_ids"], "assessment": notes[i]}
        for i,c in enumerate(claims,1)],
    "resolved_findings": findings,
    "source_validation": {"pinned_files_verified": len(files), "distinct_ranges_verified": len(ranges),
        "claim_source_occurrences_verified": sum(len(c["sources"]) for c in claims),
        "proof_blocks_verified": len(claims), "inherited_files_verified": len(inherited),
        "inherited_claim_blocks_verified": sum(len(i["claims"]) for i in inherited),
        "all_files_equal_pinned_git_blobs": True, "all_proof_and_range_hashes_exact": True},
    "inherited_bindings": inherited,
    "joint_dependency_graph": {"acyclic": True, "checked_component_claims": len(graph),
        "exact_order": "ASB1-4 -> SPR13 -> ASB14 -> SPR14-25",
        "ASB_incoming_SPR_endpoint_only": "SPR13"},
    "retained_scope": ["Actual initial extremal theta boundedness", "Actual target FinPair",
        "Same selected original R and all stated family/model/Weil/vacuum/io laws",
        "No new primary-source CuspRapidDecay application certified by this packet",
        "No new Lean build or RH/GRH conclusion"],
    "new_lean_build": False,
    "review_builder": {"file": Path(__file__).name, "sha256": sha(Path(__file__).read_bytes())},
}
out = HERE / "smooth_representatives_review.json"
out.write_text(json.dumps(record, ensure_ascii=False, indent=2) + "\n")
text = [
    "Independent mathematical review — SPR1–SPR25, v0.37",
    "Reviewer: /root/audit_literature", "Status: PASS",
    "Source pin: " + PIN, "",
    "The complete chapter was read independently against the exact original",
    "contracts and the stated inherited human proofs. All required corrections",
    "are resolved. This records human mathematical review, not an automated",
    "proof checker or a Lean replay.", "",
    "Proof SHA256: " + sha(main), "Provenance SHA256: " + sha(prov_bytes),
    "Closure SHA256: " + sha(close_bytes), "",
    f"Verified {len(claims)} proof blocks, {len(ranges)} distinct source ranges,",
    f"{len(files)} pinned source files and {sum(len(c['sources']) for c in claims)} claim-source occurrences.",
    f"Verified {sum(len(i['claims']) for i in inherited)} incoming proof blocks in {len(inherited)} human/peer files.",
    "The joint 39-claim SPR/ASB dependency graph is acyclic.", "",
]
for i in range(1,26):
    text += [f"SPR{i} — PASS", notes[i], ""]
text += ["RESOLVED FINDINGS"]
for f in findings:
    text += [f["id"] + ": " + f["finding"], f["resolution"], ""]
text += [
    "BOUNDARY",
    "The packet fully reconstructs the original conditional smooth representative",
    "and bounded-holomorphic multiplicity-map producers. Its final theta-family",
    "installation still requires the initial extremal theta bound and actual",
    "target FinPair, on the same original R. It does not certify CuspRapidDecay",
    "by merely naming it, and does not construct the common selected datum.",
    "No actual derived operator is assumed bounded on the full Hilbert space.",
    "No new Lean replay was performed.", "",
]
(HERE / "smooth_representatives_review.txt").write_text("\n".join(text))
print(json.dumps({"status": "PASS", "proof_sha256": sha(main),
    "provenance_sha256": sha(prov_bytes), "closure_sha256": sha(close_bytes),
    "claims": len(claims), "source_files": len(files), "source_ranges": len(ranges),
    "review_json_sha256": sha(out.read_bytes()),
    "review_txt_sha256": sha((HERE / "smooth_representatives_review.txt").read_bytes())}, indent=2))
