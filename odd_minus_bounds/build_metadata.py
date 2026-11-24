#!/usr/bin/env python3
"""Record the semantic cutset and classical sources for the odd-minus chain."""
from pathlib import Path
import hashlib
import json

HERE = Path(__file__).resolve().parent
P = json.loads((HERE / "provenance.json").read_text())
SHA = hashlib.sha256((HERE / "main.tex").read_bytes()).hexdigest()
PIN = P["commit"]
BASE = "src/Development/AutomorphicArithmetic/AutomorphicVarieties/"


def write(name, obj):
    (HERE / name).write_text(json.dumps(obj, indent=2, ensure_ascii=False) + "\n")


classical = [
    {
        "id": "OB-CF",
        "name": "Equivariant Hilbert class-field reciprocity",
        "statement": "For a totally complex number field K, the Galois group of its maximal everywhere-unramified abelian extension is Cl(K), by the Artin map. The isomorphism is equivariant under automorphisms of K.",
        "used_in": ["OB5"],
        "sources": [{"author": "J. S. Milne", "title": "Class Field Theory", "version": "4.03", "date": "2020-08-06", "location": "Chapter V, Theorem 3.6, Corollary 3.7, Example 3.9, pp. 158–159", "url": "https://www.jmilne.org/math/CourseNotes/CFT.pdf"}],
        "qualification": "Only finite-image unramified characters of a finite cyclotomic field are used. Equivariance is checked by conjugating Frobenius. No infinite-level class-group structure is assumed.",
    },
    {
        "id": "OB-ST",
        "name": "Exact integral Stickelberger annihilator",
        "statement": "For K=Q(zeta_L), theta_L=L^(-1) sum_{b in (Z/L)^*} b sigma_b^(-1). For an integer a prime to L, (sigma_a-a) theta_L is integral and annihilates Cl(K). Integral group-ring multiples also annihilate.",
        "used_in": ["OB5"],
        "sources": [{"author": "Romyar Sharifi", "title": "Iwasawa Theory", "location": "Chapter 4, Definition 4.5.1, Lemma 4.5.2, Theorem 4.5.6", "url": "https://math.ucla.edu/~sharifi/notes/iwasawa-ch04.html"}],
        "qualification": "The proof uses -sigma_a^(-1)(sigma_a-a)theta_L and an integral multiple of the group norm. It does not use the false unrestricted rule that every rational multiplier making theta integral annihilates.",
    },
    {
        "id": "OB-KU",
        "name": "Kummer theory and the S-unit theorem",
        "statement": "When mu_l lies in K, H^1(G_K,mu_l)=K^*/K^{*l}; away from l, an unramified Kummer class has valuation divisible by l. The S-unit group has rank r_1+r_2-1+|S| and finite cyclic torsion.",
        "used_in": ["OB4"],
        "sources": [
            {"author": "J. S. Milne", "title": "Class Field Theory", "version": "4.03", "location": "Chapter VII, Appendix A, Theorem A.3 and Proposition A.5, pp. 226–227", "url": "https://www.jmilne.org/math/CourseNotes/CFT.pdf"},
            {"author": "J. S. Milne", "title": "Algebraic Number Theory", "version": "3.08", "date": "2020-07-19", "location": "Theorem 5.11, p. 90", "url": "https://www.jmilne.org/math/CourseNotes/ANT.pdf"},
        ],
        "qualification": "The Kummer Selmer cardinality sequence and the factor l^(2r) h_K are derived in OB4; they are not retained as extra inputs.",
    },
    {
        "id": "OB-MD",
        "name": "Minkowski ideal representative and conductor-discriminant formula",
        "statement": "Every ideal class of a degree-r number field has an integral ideal representative of norm at most (4/pi)^(r_2) r!/r^r sqrt(|Delta|). For an abelian number field, |Delta| is the product of the conductors of its characters.",
        "used_in": ["OB4"],
        "sources": [
            {"author": "J. S. Milne", "title": "Algebraic Number Theory", "version": "3.08", "location": "Theorem 4.3, p. 70", "url": "https://www.jmilne.org/math/CourseNotes/ANT.pdf"},
            {"author": "Romyar Sharifi", "title": "Iwasawa Theory", "location": "Chapter 4, equation (4.2.1)", "url": "https://math.ucla.edu/~sharifi/notes/iwasawa-ch04.html"},
        ],
        "qualification": "All ideal-counting estimates and log h_K <= 3r log L are proved in OB4. No analytic class-number formula or L(1) estimate is imported.",
    },
    {
        "id": "OB-BC",
        "name": "von Staudt–Clausen Bernoulli denominators",
        "statement": "For positive even j the denominator of B_j divides the product of primes p with p-1 dividing j; B_1=-1/2 and B_j=0 for odd j>1.",
        "used_in": ["OB2", "OB5"],
        "sources": [{"author": "Tudor Ciurca", "title": "Arithmetic of cyclotomic fields", "date": "2018-09-26", "location": "Theorem 6.1.5, p. 111", "url": "https://sites.pitt.edu/~caw203/pdfs/Ciurca--Arithmetic_of_cyclotomic_fields--UROP2018.pdf"}],
        "qualification": "Only denominators through order k are used. Fourier bounds, the primitive nonvanishing argument for k>=2, the Galois-stable product and the l-adic congruences are proved in the component.",
    },
    {
        "id": "OB-LF",
        "name": "Finite local fields and their integer rings",
        "statement": "The integers of a finite extension of Q_l form a complete DVR finite free over Z_l, and the l-adic absolute value extends uniquely.",
        "used_in": ["OB3"],
        "sources": [{"author": "J. S. Milne", "title": "Algebraic Number Theory", "version": "3.08", "location": "Theorem 7.38, Corollaries 7.39 and 7.42, Remark 7.43, pp. 123–124", "url": "https://www.jmilne.org/math/CourseNotes/ANT.pdf"}],
        "qualification": "Base change for cochains and local kernels, multiplication of length by the ramification index, character projectors, and norm/valuation cancellation are proved explicitly in OB3.",
    },
]
historical = [x for x in classical if x["id"] == "OB-ST"]
for x in historical:
    x["used_in"] = []
    x["retained_input"] = False
    x["replaced_by"] = "OS1 and the explicit odd-primary conversion in OB5"
classical = [x for x in classical if x["id"] != "OB-ST"]
write("classical_inputs.json", {
    "schema": "rh-classical-inputs/1", "component": "odd_minus_bounds",
    "date_verified": "2026-11-22", "main_tex_sha256": SHA,
    "source_policy": "Primary author-hosted books/notes; exact statements and theorem locations checked. Classical leaves are separate from stable project-claim dependencies.",
    "inputs": classical, "historical_comparisons_not_used": historical,
})

targets = [
    {"path": BASE + "PrimeSetBoundDataOfPrimitiveChar.lean", "declaration": "ThmBcFree", "supplier": "OB8", "scope": "Exact universal original-field statement, with explicit C=240"},
    {"path": BASE + "OddResidueBounds/ThmBcOfPsiBound.lean", "declaration": "thmBcFree_of", "supplier": "OB8", "scope": "Full implication with literal PsiBound supplied by OS9"},
    {"path": BASE + "OddResidueBounds/ThmBcOfPsiBound.lean", "declaration": "primeBound_of", "supplier": "OB3", "scope": "All odd primes not dividing the original field degree; every original local-data record"},
    {"path": BASE + "OddResidueBounds/KillPow.lean", "declaration": "killPow", "supplier": ["OB5", "OB6"], "scope": "Odd primes and e>=1, exactly the scope needed by ThmBcFree; explicit exponent constant 30"},
    {"path": BASE + "OddResidueBounds/Imports.lean", "declaration": "gen", "supplier": "OB4", "scope": "Every prime and twist; explicit generator constant 8"},
    {"path": BASE + "OddResidueBounds/ThmBcOfPsiBound.lean", "declaration": "stickBound", "supplier": "OB7", "scope": "Odd-prime specialization with explicit constant 240; no unused l=2 extension claimed"},
    {"path": BASE + "OddResidueBounds/ProdVal.lean", "declaration": "prodVal", "supplier": "OB2", "scope": "k>=2, all characters selected by a parity-compatible set of kernels; no unused k=1 extension claimed"},
    {"path": BASE + "OddResidueBounds/AtPrime.lean", "declaration": "atPrime", "supplier": "OB3", "scope": "Original-field O-eigenspaces and ramification-factor cancellation"},
    {"path": BASE + "OddResidueBounds/DegExistsLift.lean", "declaration": "deg", "supplier": "OB1", "scope": "Every odd prime divisor of the varying original degree divides the fixed abelian-base degree"},
]
write("closure.json", {
    "version": "0.24", "component": "odd_minus_bounds", "commit": PIN,
    "main_tex_sha256": SHA, "claims": ["OB" + str(i) for i in range(1, 9)],
    "outcome": "Full quantitative odd-minus supplier ThmBcFree with C=240",
    "claim_dependency_graph": P["dependency_graph"],
    "incoming_bespoke_interface": {"name": "PsiBound", "stable_supplier": "OS9", "component": "odd_minus_supplier", "local_status": "Assumed literally in OB3; supplied by OS9 in the combined reconstruction", "circularity_check": "OS9 accepts a=0 with v(0)=infinity and uses no OB2 nonvanishing; OB2 independently supplies nonzero integral values for quantitative finiteness."},
    "incoming_jacobi_interface": {"name": "Finite Jacobi class-group annihilation", "stable_supplier": "OS1", "component": "odd_minus_supplier", "join": "For large L=R*l^m>a, 2 sum E1(b) sigma_b^(-1)=-sigma_a^(-1) sum theta_(L,a)(t) sigma_t^(-1); cancel 2 on odd l-primary character values."},
    "classical_inputs": [x["id"] for x in classical],
    "classical_input_registry": "odd_minus_bounds/classical_inputs.json",
    "closed_source_targets_in_stated_scope": targets,
    "historical_claim_suppliers": {
        "VW4": {"discharged_input": "ThmBcFree", "supplied_by": "OB8", "constant": 240, "join": "The exact minusBound(C, M.deg, [E:Q], condF(E), t) bound on every original field and every finite odd-prime set", "retained_elsewhere": ["ThmBab", "PointHV", "the separate 2-primary and odd-plus branches of JointWin"]},
        "VW1": {"discharged_input": "The odd-minus part of ThmBc", "supplied_by": "OB8", "qualification": "Does not by itself close the other cohomological summands or produce a compatible lattice gain witness."},
    },
    "quantifier_audit": ["Every original CM abelian field E specified by IsCompField", "Every given algebraic closure and every family of local-data records", "One actual cyclotomic action and the attained condF embedding", "Every finite set of odd rational primes", "All 1<=e<t in the same bound", "Exceptional primes restricted to divisors of the fixed base degree M.deg", "One numerical constant 240 independent of all fields, primes, levels, twists and choices"],
    "complete_chain_in_component": True,
    "additional_unreconstructed_bespoke_inputs": [],
    "unclaimed_generalizations": ["l=2 part of source StickBound/Procyc", "k=1 Bernoulli primitive nonvanishing", "Any positivity or arithmetic lattice-gain theorem outside this quantitative odd-minus branch"],
    "full_RH_GRH_closed": False,
    "source_links": P["validation"]["claim_source_links"],
    "source_files": P["validation"]["source_files_checked_against_pinned_git_blobs"],
})

(HERE / "report.txt").write_text(f"""ODD-MINUS QUANTITATIVE CHAIN — VERSION 0.24

Outcome
=======
OB1–OB8 prove literal ThmBcFree with explicit numerical constant C=240
from literal PsiBound (supplied by OS9) and the finite Jacobi annihilator
proved in OS1. No additional project-specific
killPow, gen, prodVal, atPrime, character/field compatibility or degree
supplier is left behind this endpoint.

The endpoint is the exact original-field estimate
  sum_(l in S) log(l) sum_(1<=e<t) minusLen(E,l,e)
  <= 3 [E:Q] t^2 log(t condF(E))
     +240 sum_(odd prime l | M.deg)
          l [E:Q]^2 t^2 log(t l condF(E))^2,
including finiteness of every individual length, for every original
algebraic closure, local-data family and finite odd-prime set S.

Substantive closure
===================
OB1 keeps the actual cyclotomic action and proves the fixed exceptional
prime set using the original IsCompField subgroup. OB2 proves Bernoulli
integrality, nonvanishing for k>=2, the archimedean bound and the common
integer product that pays for all prime valuations. OB3 proves all
same-field Selmer/base-change/eigenspace comparisons and cancels the
ramification factor. OB4 proves the generator bound with constant 8.
OB5 transfers the exact finite Jacobi annihilator from OS1 to the
actual negative cyclotomic twist by finite cocycles; no infinite-level
class-group or bespoke restriction-annihilation theorem is imported.
OB6 supplies the signed determinant and a single uniform annihilating
power with constant 30. OB7 proves length <= exponent times generators,
giving 30*8=240. OB8 performs the complete finite twist/prime summation.

Classical inputs
================
The five precise classical leaves are Hilbert class-field reciprocity,
Kummer and S-unit theory, Minkowski plus conductor-discriminant,
von Staudt–Clausen, and finite local-field structure. They are stated with
author-hosted source URLs and theorem/page references in main.tex and
classical_inputs.json. The classical Stickelberger theorem is now only a
historical comparison: OS1 and the explicit identity in OB5 prove its
needed odd-primary consequence. All quantitative consequences are proved.

Interface and scope
===================
OB3 depends on stable claim OS9, with the literal PsiBound interface
spelled out in main.tex. OS9 does not import our Bernoulli nonvanishing,
so the connection is acyclic. OB5 depends on OS1, with its exact group-ring
orientation and the cancellation of 2 written explicitly. The source's unused l=2 StickBound and
k=1 Bernoulli generalizations are not claimed. The full RH/GRH argument,
the 2-primary and odd-plus cohomological suppliers, and compatible
geometric/lattice inputs are not asserted closed by this component.

Verification
============
Pinned Lean commit: {PIN}
8 consolidated claims; 79 exact declaration links; 53 distinct source
files checked byte-for-byte against pinned Git blobs. Proof and source
range hashes are reproducible with build_provenance.py. These checks
establish provenance, not a new Lean kernel replay. A separate TeX draft
syntax check is recorded in tex_validation.json, without generating a
PDF. Root has independently reviewed the mathematical chain; the frozen
review is stored with the project reviews.

Frozen main.tex SHA-256:
{SHA}
""")
(HERE / "next_targets.txt").write_text("""CONTINUATION BOUNDARY AFTER OB1–OB8

No unresolved bespoke supplier remains after OS1 and OS9 in the
quantitative odd-minus chain. Incoming literal PsiBound is supplied by OS9
and the finite Jacobi annihilator by OS1. Their branches join at OB8 and
supply the odd-minus input of VW4.

This component does not advance ThmBab, PointHV, the 2-primary or odd-plus
parts of JointWin, or the compatible geometric/lattice gain interfaces.
Their global statuses belong to the root dependency audit. Do not reopen
the elementary odd-minus wrappers merely because their historical Lean
declaration names remain visible in source locators.

Optional generalizations, unnecessary for this endpoint: l=2 Procyc /
StickBound, and k=1 primitive Bernoulli nonvanishing. These are deliberately
not continuation targets for the present chain-closing priority.
""")
print(json.dumps({"main_tex_sha256": SHA, "classical_inputs": len(classical),
                  "closed_source_targets_in_stated_scope": len(targets)}, indent=2))
