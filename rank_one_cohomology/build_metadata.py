#!/usr/bin/env python3
"""Refresh RV scope, classical-input and continuation records."""
from pathlib import Path
import hashlib
import json

HERE = Path(__file__).resolve().parent
WORK = HERE.parent
prov = json.loads((HERE / "provenance.json").read_text())
main_sha = hashlib.sha256((HERE / "main.tex").read_bytes()).hexdigest()
assert main_sha == prov["validation"]["main_tex_sha256"]


def dump(name, value):
    (HERE / name).write_text(json.dumps(value, indent=2, ensure_ascii=False) + "\n")


dump("classical_inputs.json", {
    "schema": "rh-classical-input-registry/1",
    "artifact_version": "0.26",
    "component": "rank_one_cohomology",
    "main_tex_sha256": main_sha,
    "date_verified": "2026-11-22",
    "inputs": [
        {
            "id": "RV-LF",
            "name": "Unique valuation and completeness of finite extensions of Q_ell",
            "statement_used": "Every finite extension E/Q_ell has a unique extended nonarchimedean absolute value, is complete, and satisfies |x|_E^[E:Q_ell]=|Norm_E/Q_ell(x)|_ell. The absolute value extends uniquely to the algebraic closure.",
            "source": {
                "author": "J. S. Milne",
                "title": "Algebraic Number Theory",
                "version": "3.08",
                "date": "2020-07-19",
                "locations": [
                    "Theorem 7.38, printed p.123",
                    "Corollary 7.40, printed p.124",
                ],
                "url": "https://www.jmilne.org/math/CourseNotes/ANT.pdf",
            },
            "used_in": ["RV4", "RV5", "RV6"],
            "matching": [
                "The field is the actual finite intermediate field inside PadicAlgCl(ell), with the unique extended valuation, at every prime including 2.",
                "Completeness makes each finite intermediate field closed in the noncomplete algebraic closure.",
                "RV6 proves the integral unit-ball equality, finite trace-dual lattice, discrete valuation ring and fraction field facts needed for the coefficient ring.",
                "RV4 proves the Krasner comparison and the countable cover, then proves the needed compact Baire argument and cocycle subgroup capture. They are not additional retained inputs.",
            ],
        }
    ],
    "proved_here_not_retained_as_additional_leaves": [
        {
            "name": "Prime-power cyclotomic degree",
            "proof": "RV3: shift sum_{j=0}^{ell-1} X^(j ell^(r-1)) by one and apply the explicitly checked Eisenstein criterion.",
            "comparison_reference": "Milne, Algebraic Number Theory, Proposition 6.2(a), printed p.96.",
        },
        {
            "name": "Krasner containment",
            "proof": "RV4: unique absolute value makes automorphisms isometries; the strict conjugate separation forces an automorphism fixing beta to fix alpha.",
            "comparison_reference": "Milne, Algebraic Number Theory, Proposition 7.60, printed pp.131-132.",
        },
        {
            "name": "Countable finite-field cover and Baire cocycle capture",
            "proof": "RV4: rational coefficient approximation, countable embedded Qbar, closed subgroups supplied by the cocycle equation, an open subgroup from compact Baire, and finite coset representatives.",
        },
        {
            "name": "Finite-length Selmer to vector vanishing",
            "proof": "RV5: finite-length annihilation, scaled quotient cocycles and one exact witness obtained from a single nontrivial scalar.",
        },
    ],
    "inherited_human_suppliers": {
        "LD3": "Compatible finite global Poitou-Tate duality, with its matched classical input.",
        "LK2": "Native finite-local-field cohomology finiteness, with its matched classical input.",
        "LK3": "Native finite-local-field Tate duality and actual cup/invariant identification.",
        "KB1": "Original compact cochains, finite global cohomology and inverse-limit comparison.",
        "KB6": "Original valuation/henselization/completion to native local-field transport.",
        "KB8": "Literal LemmaK31, with its recorded K-theory and other classical leaves.",
    },
    "not_required": [
        "Ferrero-Washington or an Iwasawa control theorem",
        "A prime-to-ell order hypothesis on the finite character",
        "An arbitrary compact-subset-in-finite-extension assertion",
        "Any automorphy, rigidity, trace-counting or CorX supplier",
    ],
})

endpoints = [
    {
        "name": "UpperTheory.V.X.soFin",
        "supplied_by": "RV3",
        "scope": "Arbitrary original number field k/Omega, every prime ell, every given finite coefficient DVR, every open-kernel finite-order character and every e>=1.",
    },
    {
        "name": "UpperTheory.V.X.soVec",
        "supplied_by": "RV6",
        "scope": "Actual finite coefficient field E, with local witnesses initially in PadicAlgCl; the global witness lies in E.",
    },
    {
        "name": "UpperTheory.V.X.soBar",
        "supplied_by": "RV7",
        "scope": "General original k/Omega and algebraic coefficient cocycle; finite-extension capture proved using Baire and the cocycle identity.",
    },
    {
        "name": "UpperTheory.V.GradeZeroInterpolatingElement.SoV",
        "supplied_by": "RV7",
        "scope": "For every original Omega/Q and every prime, all finite-order characters and all e>=1, with every original valuation condition.",
    },
    {
        "name": "UpperTheory.V.GradeZeroInterpolatingElement.SoFin",
        "supplied_by": "RV3",
        "scope": "For every original Omega/Q and every prime, all Coef ell and open-kernel characters and all e>=1.",
    },
    {
        "name": "UpperTheory.V.HV.coefIndep",
        "supplied_by": "RV7",
        "supporting_claims": ["RV1", "RV6"],
        "scope": "Same original Omega, level and local family; any natural twist; possibly nonnested coefficient rings with equal embedded Dirichlet values. Finiteness equivalent and exact normalized Vn equal, with explicit toNat-at-infinity convention.",
    },
]
dump("closure.json", {
    "schema": "rh-human-component-closure/1",
    "artifact_version": "0.26", "component": "rank_one_cohomology",
    "main_tex_sha256": main_sha,
    "closed_claim_ids": [c["id"] for c in prov["claims"]],
    "dependency_graph": prov["dependency_graph"],
    "external_claim_dependencies": prov["external_claim_dependencies"],
    "literal_supplied_endpoints": endpoints,
    "remaining_bespoke_inputs_inside_component": [],
    "new_classical_input_ids": ["RV-LF"],
    "proof_simplifications": [
        "The exact finite-quotient H1 kernel with finite H0 replaces the source's sharper abelian generator-count bound in upV. The full SoFin endpoint is proved; the sharper T.card*h0_global inequality is not claimed.",
        "The coefficient ring and every local restriction remain original. Finite character order may be divisible by ell; no averaging is used.",
        "The Baire argument applies to closed subgroups created by the cocycle identity, not to an arbitrary compact subset of PadicAlgCl.",
        "Finite-length vector descent uses an explicit witness c(g0)/(alpha(g0)-1), avoiding an unjustified limit of independently chosen witnesses.",
    ],
    "outgoing_symplectic_cut": {
        "supplied": [
            "forall original Omega and ell, SoV Omega ell and SoFin Omega ell",
            "original coefficient finiteness and normalized-length return via coefIndep",
        ],
        "not_supplied_by_this_component": [
            "CorX",
            "SymplecticFourImageDense",
            "CohomologyHyp, including all its differently named or normalized fields",
            "LemmaM, LemmaMprime and LemmaP",
            "NumberSp4Alt",
            "RigiditySymplecticFour",
            "Full CountII/CountIII assembly on the original Raw/host",
            "PointHV and the global arithmetic family/gain interfaces",
        ],
    },
    "prior_files_modified": False,
    "Lean_kernel_replay_run": False,
    "full_RH_GRH_closed": False,
})

old = json.loads((WORK / "dependency_audit_v0_25/next_targets.json").read_text())
by_id = {t["id"]: t for t in old["targets"]}
retire = []
for key, supplier in [("DA25-HV-06", "RV3"), ("DA25-HV-07", "RV7")]:
    t = dict(by_id[key])
    t["status"] = "safe_to_retire_in_exact_rank_one_scope"
    t["supplied_by"] = [supplier]
    t["previous_record"] = by_id[key]
    t["closed_scope"] = (
        "Full literal original-number-field finite-character Selmer finiteness, with no prime-to-ell order restriction."
        if supplier == "RV3" else
        "Full original algebraic-coefficient vector coboundary theorem, including Baire/cocycle finite-extension capture and coefficient/local-witness descent."
    )
    retire.append(t)
dump("retirement_candidates.json", {"targets": retire, "root_targets_modified": False})
dump("next_targets.json", {
    "component": "rank_one_cohomology",
    "remaining_targets_inside_component": [],
    "downstream_frontier": [
        "Use RV7 as the exact all-Omega/all-ell SoV-and-SoFin premise of sp4Main_alt.",
        "Use RV1/RV7 for exact original coefficient independence after the auxiliary roots-of-unity extension.",
        "The independently assigned CorX, finite algebra, other cohomology, automorphy, rigidity and trace-counting branches remain; this component does not retire them.",
    ],
})

report = f"""RANK-ONE COHOMOLOGY CLOSURE — v0.26

Outcome
=======
RV1--RV7 supply literal SoFin and SoV for every original Omega and
prime ell, plus the general-number-field soFin/soVec/soBar statements
and full original normalized coefficient independence.

Frozen text SHA-256: {main_sha}
Pinned Lean commit: {prov['commit']}
Exact declaration links: {prov['validation']['claim_source_links']}
Distinct source files checked against pinned blobs:
{prov['validation']['source_files_checked_against_pinned_git_blobs']}

Closed chain
============
RV1: actual QO=Frac(O)/O, positive eO, finite free coefficient
extension, all local kernels, length multiplication and normalization.
RV2: original strict negative-twist module -> compatible finite PT
pairings -> compact H2 -> KB8=LemmaK31. No FW hypothesis is used.
RV3: joint finite-character/cyclotomic kernel gives a root-containing
abelian extension in original Omega. A nonzero cyclotomic scalar
bounds H0; finite quotient cocycles bound the restriction kernel.
The whole original Selmer module therefore has finite length.
RV4: rational polynomial approximation and a proved Krasner argument
give a countable finite-field cover. The cocycle equation makes the
preimages closed subgroups; Baire supplies one open subgroup and
finitely many coset representatives capture the complete image.
RV5: finite-length annihilation yields uniformly approximating
coboundaries. One nontrivial scalar determines the exact witness.
RV6: construct the actual integral coefficient lattice, move every
local witness back into its finite field, and apply RV3/RV5.
RV7: capture the original algebraic-valued cocycle, apply RV6, and
specialize to the literal SoV/SoFin pair. Common coefficient composita
give full coefIndep, including its infinity convention.

Inputs and boundaries
=====================
Incoming proved suppliers: LD3, LK2, LK3, KB1, KB6, KB8.
New named classical background: RV-LF, unique finite-local-field
absolute value/completeness/norm formula (Milne ANT 7.38 and 7.40).
The coefficient lattice, Krasner comparison, countable cover, Baire
subgroup step, restriction kernel and vector approximation are written.
Remaining bespoke premises inside this component: none.

The character can have ell-power order. Original k/Omega/O, the
negative twist and every valuation subgroup remain fixed. At ell=2
the auxiliary base field contains mu4 before global duality is used.
No arbitrary compact subset capture or prior Selmer finiteness is
assumed. No new Lean replay or PDF is required.

The source's sharper upV generator estimate is replaced by a proved
finite-quotient bound sufficient for SoFin; its sharper constant is
not claimed. The full symplectic count's CorX, other cohomological
packages, finite algebra, automorphy, rigidity, trace counting and
original-host assembly remain separate. RH/GRH are not concluded.
"""
(HERE / "report.txt").write_text(report)
print("Updated classical_inputs.json, closure.json, retirement_candidates.json, next_targets.json and report.txt")
