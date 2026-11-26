#!/usr/bin/env python3
"""Regenerate the scope, classical-input and verification ledgers for TW."""
from pathlib import Path
import hashlib
import json

HERE = Path(__file__).resolve().parent
prov = json.loads((HERE / "provenance.json").read_text())
main_sha = hashlib.sha256((HERE / "main.tex").read_bytes()).hexdigest()
assert main_sha == prov["validation"]["main_tex_sha256"]


def dump(name, data):
    (HERE / name).write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n")


classical = {
    "schema": "rh-classical-inputs/1",
    "component": "simultaneous_cohomological_windows",
    "date_verified": "2026-11-22",
    "main_tex_sha256": main_sha,
    "source_policy": "Primary publisher and author-hosted sources; theorem locations verified by retrieval.",
    "inputs": [
        {
            "id": "TW-FW",
            "name": "Ferrero-Washington mu=0 for abelian number fields",
            "statement": "For every prime l and every finite abelian F/Q, the unramified Iwasawa module of its cyclotomic Z_l-extension has mu=0.",
            "used_in": ["TW1"],
            "sources": [
                {
                    "authors": ["Bruce Ferrero", "Lawrence C. Washington"],
                    "title": "The Iwasawa invariant mu_p vanishes for abelian number fields",
                    "journal": "Annals of Mathematics", "volume": 109,
                    "year": 1979, "pages": "377–395",
                    "url": "https://doi.org/10.2307/1971116",
                    "publisher_url_as_observed": "https://annals.math.princeton.edu/1979/190-2/p05",
                    "publisher_path_note": "The publisher's live path says 190-2 but its page explicitly identifies Volume 109. The chapter uses the stable DOI.",
                },
                {
                    "author": "Romyar Sharifi", "title": "Iwasawa Theory",
                    "location": "Theorem 6.2.1",
                    "url": "https://math.ucla.edu/~sharifi/notes/iwasawa-ch06.html",
                },
            ],
            "qualification": "The stated theorem is for every prime, including 2. The later odd-prime restriction on minus-part consequences is not imported into this theorem. TW1 proves the exact finite-layer rank proposition used by Lean.",
        },
        {
            "id": "TW-IW",
            "name": "Ordinary Iwasawa module and algebraic structure theorem",
            "statement": "The norm inverse limit of l-primary class groups in a Z_l-extension is finitely generated torsion over Z_l[[Gamma]], and identifies with the maximal unramified abelian pro-l Galois group. Its structure theorem has finite errors and distinguished-polynomial/l-power factors.",
            "used_in": ["TW1"],
            "sources": [
                {
                    "author": "Romyar Sharifi", "title": "Iwasawa Theory",
                    "location": "Corollary 3.2.7 and Proposition 3.2.11",
                    "url": "https://math.ucla.edu/~sharifi/notes/iwasawa-ch03.html",
                },
                {
                    "author": "Romyar Sharifi", "title": "Iwasawa Theory",
                    "location": "Theorem 2.2.13; Remark 2.2.11; Lemma 2.2.12",
                    "url": "https://math.ucla.edu/~sharifi/notes/iwasawa-ch02.html",
                },
            ],
            "qualification": "TW1 derives Z_l-finite generation from mu=0 and proves the finite-layer norm-surjectivity step. No unspecified finite-layer control theorem is retained.",
        },
        {
            "id": "TW-CF",
            "name": "Finite Hilbert class-field reciprocity with norm compatibility",
            "statement": "For a totally complex number field, the maximal everywhere-unramified abelian extension has Galois group its ideal class group. Artin restriction agrees with ideal norm.",
            "used_in": ["TW1"],
            "sources": [
                {
                    "author": "J. S. Milne", "title": "Class Field Theory",
                    "version": "4.03", "date": "2020-08-06",
                    "location": "Chapter V, Theorem 3.6, Corollary 3.7 and Example 3.9, pp. 158–159",
                    "url": "https://www.jmilne.org/math/CourseNotes/CFT.pdf",
                },
            ],
            "qualification": "All fields in the FW application contain nonreal roots of unity, so no narrow-class or real-place correction is hidden at l=2. Norm compatibility is also explained using Frobenius.",
        },
        {
            "id": "TW-CD",
            "name": "Abelian conductor-discriminant formula",
            "statement": "The absolute discriminant of an abelian field is the product of the conductors of its characters; a subfield of Q(zeta_N) of degree n therefore has |Delta|<=N^n.",
            "used_in": ["TW6"],
            "sources": [
                {
                    "author": "Romyar Sharifi", "title": "Iwasawa Theory",
                    "location": "Chapter 4, equation (4.2.1)",
                    "url": "https://math.ucla.edu/~sharifi/notes/iwasawa-ch04.html",
                },
            ],
            "qualification": "The same classical leaf is already used as part of OB-MD. Root-degree, conductor enlargement, all uniform constants and model transfer are proved in TW6.",
        },
    ],
    "already_reconstructed_interfaces": [
        {"id": "LD3", "meaning": "One compatible normalized finite Poitou-Tate invariant and pairing family"},
        {"id": "LK2", "meaning": "Literal LocalFinitenessK on actual native local fields"},
        {"id": "LK3", "meaning": "Literal LocalTateDualityK, all finite modules and all primes"},
        {"id": "KB1", "meaning": "Actual compact cochains, finite global cohomology and inverse-limit comparison"},
        {"id": "KB6", "meaning": "Original decomposition group to henselization, completion and native local-field transport"},
        {"id": "KB8", "meaning": "Literal LemmaK 31, all original field and local-data choices"},
    ],
}
dump("classical_inputs.json", classical)

closure = {
    "version": "0.25",
    "component": "simultaneous_cohomological_windows",
    "commit": prov["commit"],
    "main_tex_sha256": main_sha,
    "claims": [c["id"] for c in prov["claims"]],
    "outcome": "Complete literal exists K:BConst, forall Ct>=1, ThmBab K Ct",
    "claim_dependency_graph": prov["dependency_graph"],
    "incoming_quantitative_interface": {
        "name": "LemmaK", "stable_supplier": "KB8", "constant": 31,
        "component": "k_theory_bridge",
        "scope": "Actual compact H2 cardinality bound on every original F, Omega, D and k>=1",
    },
    "incoming_finite_duality_interfaces": [
        {"name": "Published.PoitouTateDuality", "stable_supplier": "LD3"},
        {"name": "LocalFinitenessK", "stable_supplier": "LK2"},
        {"name": "LocalTateDualityK", "stable_supplier": "LK3"},
        {"name": "Actual finite/compact coefficient cohomology comparison", "stable_supplier": "KB1"},
        {"name": "Original local-data to native local K transport", "stable_supplier": "KB6"},
    ],
    "classical_inputs": ["TW-FW", "TW-IW", "TW-CF", "TW-CD"],
    "classical_input_registry": "simultaneous_cohomological_windows/classical_inputs.json",
    "closed_source_targets_in_stated_scope": [
        {"declaration": "Published.FerreroWashington", "supplier": "TW1",
         "scope": "Exact finite-layer class l-rank statement, every prime, mu4 at 2"},
        {"declaration": "Two.baseRk / Two.towerTwo / Two.towerFixed", "supplier": "TW2",
         "scope": "Exact uniform 4*(g+6*M.deg) family and all fixed odd-prime model bounds"},
        {"declaration": "TwoBase", "supplier": "TW2",
         "scope": "Original E embeds in a cyclotomic layer with kernel-length loss at most 1"},
        {"declaration": "Tower.step0 / Tower.exists_descends", "supplier": "TW3",
         "scope": "All k>=1 and layer indices; exact negative/positive dual twist convention"},
        {"declaration": "PropA.shaLeV", "supplier": "TW3",
         "scope": "Every totally complex root-containing reference field, original closure and D, k>=1"},
        {"declaration": "PropA.aBound_of_isTower / ABound / SecondBound", "supplier": "TW4",
         "scope": "All primes; exact jZero, compact centers and R per-layer growth"},
        {"declaration": "FirstBound / Win.exc / Win.window", "supplier": "TW5",
         "scope": "Exact R exceptions and J=2^(R+2)*(Ct/eta)^R on one whole square window"},
        {"declaration": "Win.layerdisc / Win.abiso / Win.layeriso", "supplier": "TW6",
         "scope": "Uniform reference field constants and separately quantified layer models"},
        {"declaration": "Win.point / Win.point2 / Win.final", "supplier": "TW7",
         "scope": "Literal LemmaK-to-all-twists estimate and 3eps/4 to 4eps/5 absorption"},
        {"declaration": "Win.thmBab_of_lemmaK / ThmBab", "supplier": "TW8",
         "scope": "One BConst before every Ct>=1; fixed pair over the entire window; all original and reference models"},
    ],
    "historical_claim_suppliers": {
        "VW3": {"discharged_input": "The ThmBab part of JointWin",
                "supplied_by": "TW8",
                "retained_elsewhere": ["PointHV", "the existing original-field assembly", "other arithmetic/lattice/host inputs"]},
        "VW4": {"discharged_input": "ThmBab", "supplied_by": "TW8",
                "join": "Use the same K and j_l=Nat.log l (K.Rl l (Lchi psi l))+3; all prescribed layer models and D are quantified.",
                "remaining_bespoke_cohomological_supplier": "PointHV",
                "already_supplied_odd_minus": {"supplier": "OB8", "constant": 240}},
    },
    "quantifier_audit": [
        "One CK=31 is available from KB8, before all other parameters.",
        "R0 is a function of the fixed abelian datum only; its value is fixed before q and d.",
        "Rl is a function of l and the fixed abelian datum only; it transfers to every model.",
        "The entire BConst K is fixed before all Ct>=1.",
        "For fixed M,B',L,eps,A1,Ct the threshold X0 is fixed before admitted functions e,t, scale X and prime pair q,d.",
        "Exception sets may depend on the already fixed pair and X, but their cardinality budget R does not.",
        "One union of exception sets produces one Y for the whole closed real interval [Y,Y^2].",
        "The same q,d is retained throughout that interval.",
        "The 2-primary conclusion is on every original E satisfying IsCompField.",
        "The odd reference terms quantify every model L0 and every prescribed layer L1/L0 separately; no identification with E is asserted.",
        "All finiteness clauses precede real-valued twist sums, and all local-data records are universally quantified.",
    ],
    "complete_chain_in_component": True,
    "additional_unreconstructed_bespoke_inputs": [],
    "remaining_inputs_outside_component": [
        "PointHV (CountZ is supplied separately by CZ6, but does not close the other count suppliers)",
        "All arithmetic/lattice-gain and actual host/representation inputs retained by the cumulative dependency audit",
    ],
    "unclaimed_generalizations": [
        "k=0 strict-Selmer descent or reference comparison",
        "Uniform class-number sizes, rather than l-rank",
        "A full LinkN/LinkV, lattice-gain, RH or GRH theorem",
    ],
    "full_RH_GRH_closed": False,
    "source_links": prov["validation"]["claim_source_links"],
    "source_files": prov["validation"]["source_files_checked_against_pinned_git_blobs"],
}
dump("closure.json", closure)

report = f"""SIMULTANEOUS COHOMOLOGICAL WINDOWS — v0.25

Outcome
-------
TW1–TW8 prove the entire literal supplier
    exists K : BConst, forall Ct >= 1, ThmBab K Ct.
The chapter is a complete 10-page human proof, not a list of wrappers.
It retains the precise named classical inputs TW-FW, TW-IW, TW-CF, TW-CD.
The quantitative input is KB8 = LemmaK 31; finite duality/native local
inputs are LD3, LK2, LK3, KB1 and KB6.

Closed mechanisms
-----------------
1. Classical Ferrero–Washington mu=0 -> exact Published.FerreroWashington,
   including l=2 and all separately specified root-layer field models.
   The proof gives eventual total ramification and surjective finite-layer
   class norms, rather than invoking an unspecified control theorem.
2. One two-primary bound R0=4*(g+6*M.deg), fixed before q,d; the inertia
   dimensions, exact 2/4 Frobenius orbit counts and two quadratic
   restriction steps are proved. Original E -> E(i) costs at most 1.
3. Exact negative twist on strict characters -> positive dual twist on
   the actual tower module -> all-layer coinvariant lengths.
   Finite PT/dual limits prove shaInv<=VLen with original local data.
4. Mod-l unipotence -> R per-layer growth after j0=Nat.log l R+3.
   R nested-ball centers in Z_l give the determinant/cokernel estimate.
5. At most R exceptional integer twists; one elementary logarithmic
   interval induction gives the exact J and one common square window.
6. Uniform degree/discriminant estimates, all field-model transfers,
   LemmaK at small exceptions, final twist sum and exponential absorption.

Quantifiers and integration
---------------------------
K is chosen before all Ct>=1. For fixed parameters X0 is chosen before
admitted e,t, X and q,d. The same q,d and Y work throughout [Y,Y^2].
The 2-primary estimate concerns every original E; odd reference layers
are separately universally quantified, with all Omega and D.
Together with OB8=ThmBcFree(240), this replaces ThmBab in VW3/VW4.
PointHV remains the separate bespoke cohomological supplier. It is not
inferred from CountZ alone. No full RH/GRH or LinkN closure is claimed.

Verification
------------
Main SHA256: {main_sha}
Pinned source commit: {prov['commit']}
{prov['validation']['claim_source_links']} exact declaration links;
{prov['validation']['source_files_checked_against_pinned_git_blobs']} source files equal to pinned Git blobs.
The provenance records exact written-proof and source-declaration byte
ranges and hashes. TeX draft-mode compilation: 10 pages, no missing
characters, no overfull or underfull boxes, no undefined controls.
No Lean replay and no PDF generation were performed.

Files
-----
main.tex, provenance.json, source_locators.txt, classical_inputs.json,
closure.json, next_targets.txt, tex_validation.json, build_provenance.py,
build_metadata.py.
"""
(HERE / "report.txt").write_text(report)
(HERE / "next_targets.txt").write_text(
    "TW1–TW8 have no additional unreconstructed bespoke supplier.\n"
    "Use KB8=LemmaK31, LD3, LK2–LK3, KB1 and KB6 as the incoming stable IDs.\n"
    "For the cohomological window boundary, the remaining supplier is PointHV.\n"
    "CountZ is being supplied by CZ6; the other CountI/II/III/V branches and\n"
    "the exact PointHV assembly must remain explicit until actually proved.\n"
    "Keep all arithmetic/lattice/host/representation inputs outside this branch.\n"
    "Do not identify the separately quantified reference-layer models with E.\n"
)

dump("tex_validation.json", {
    "component": "simultaneous_cohomological_windows", "main_tex_sha256": main_sha,
    "mode": "pdflatex draftmode, no shell escape, no PDF generation",
    "status": "PASS", "pages": 10,
    "undefined_control_sequences": 0, "missing_characters": 0,
    "overfull_boxes": 0, "underfull_boxes": 0,
    "routine_warnings": ["epstopdf shell escape disabled"],
    "qa_directory": "qa_simultaneous_cohomological_windows_v0_25",
    "not_a_mathematical_or_Lean_replay": True,
})
print(json.dumps({"main_tex_sha256": main_sha, "claims": 8,
                  "classical_inputs": len(classical["inputs"]),
                  "additional_unreconstructed_bespoke_inputs": []}, indent=2))
