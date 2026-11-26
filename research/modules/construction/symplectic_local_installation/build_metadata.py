#!/usr/bin/env python3
"""Rebuild DX closure, input registry and report after provenance is refreshed."""
from pathlib import Path
import hashlib
import json

HERE = Path(__file__).resolve().parent
COMP = "symplectic_local_installation"
PIN = "7cbf7a0c32fca1badf05931879a37c3f8a2b03b4"
prov_raw = (HERE / "provenance.json").read_bytes()
prov = json.loads(prov_raw)
main_hash = hashlib.sha256((HERE / "main.tex").read_bytes()).hexdigest()
assert prov["main_tex_sha256"] == main_hash


def dump(name, value):
    (HERE / name).write_text(json.dumps(value, indent=2, ensure_ascii=False) + "\n")


classical = [
    {
        "id": "DX-LT",
        "name": "Finite local Tate duality with the normalized Brauer invariant",
        "statement": "For every finite extension K/Q_p and every finite continuous ell-primary G_K-module M, finite local cohomology vanishes above degree two; cup products with Hom(M,mu_{ell^r}) are perfect in degrees (0,2),(1,1),(2,0), with H2(mu_{ell^r}) identified by the Brauer invariant. No freeness or p!=ell hypothesis.",
        "primary_sources": [{
            "author": "J. S. Milne", "title": "Arithmetic Duality Theorems",
            "edition": "Second edition, 2006",
            "url": "https://jmilne.org/math/Books/ADTnot.pdf",
            "location": "Chapter I, Theorem 2.1 and Corollary 2.3, printed pages 26--28; Brauer invariant in I.1",
        }],
        "native_match": "DX1 plus existing LK1--LK3 and KB6: original completion/henselization, all coefficient duals and cups, and compatible root actions. The rational lattice limit is proved, not imported.",
        "used_by": ["DX1"],
    },
    {
        "id": "DX-LE",
        "name": "Finite local Euler--Poincare characteristic",
        "statement": "|H0(K,M)||H2(K,M)|/|H1(K,M)| equals the inverse cardinality of O_K/|M|O_K, hence 1 for p!=ell and |M|^{-[K:Q_ell]} for p=ell.",
        "primary_sources": [{
            "author": "J. S. Milne", "title": "Arithmetic Duality Theorems",
            "edition": "Second edition, 2006",
            "url": "https://jmilne.org/math/Books/ADTnot.pdf",
            "location": "Chapter I, Theorem 2.8, printed page 31, PDF zero-based page 38",
        }],
        "native_match": "DX1 and LK4 compute the literal native local-degree factor; arbitrary finite nonfree modules and every prime are retained.",
        "used_by": ["DX1"],
    },
    {
        "id": "DX-GF",
        "name": "Global finiteness for finite S-cohomology",
        "statement": "If S is finite, contains all archimedean places and all places dividing |M|, and M is a finite continuous G_{F,S}-module, every finite-degree cohomology group is finite. In degrees at least three its real-place comparison gives zero for odd ell.",
        "primary_sources": [{
            "author": "J. S. Milne", "title": "Arithmetic Duality Theorems",
            "edition": "Second edition, 2006",
            "url": "https://jmilne.org/math/Books/ADTnot.pdf",
            "location": "Chapter I, Corollary 4.15, printed page 62, PDF zero-based page 69; higher-degree comparison in I.4.10(c)",
        }],
        "native_match": "DX1 identifies the actual quotient by omitted inertia with G_{F,S}, and uses the original ContainsAbove premise. High-degree vanishing is asserted only under the native odd-ell premise.",
        "used_by": ["DX1"],
    },
    {
        "id": "DX-GE",
        "name": "Global truncated Euler--Poincare formula, including real 2-primary modules",
        "statement": "For finite S and a finite G_{F,S}-module whose order is invertible away from S, |H0||H2|/|H1| equals the product over archimedean places of |H0(F_v,M)|/||M||_v. This is explicitly the truncated degree-0/1/2 expression, also when real-place 2-primary higher cohomology persists.",
        "primary_sources": [{
            "author": "J. S. Milne", "title": "Arithmetic Duality Theorems",
            "edition": "Second edition, 2006",
            "url": "https://jmilne.org/math/Books/ADTnot.pdf",
            "location": "Chapter I, Theorem 5.1 and the immediately preceding definition, printed page 67, PDF zero-based page 74; assumptions on printed page 66",
        }],
        "native_match": "DX1 gives exactly |H0||H2||M|^[F:Q]=|H1| times real fixed-vector cardinalities times |M|^r2. The real and complex normalized absolute values are evaluated explicitly.",
        "used_by": ["DX1"],
    },
    {
        "id": "DX-CM",
        "name": "Noetherian completion and Krull intersection",
        "statement": "Completion is exact on finite modules over a Noetherian ring, remains Noetherian, and agrees modulo every power of the completed ideal. For a Noetherian local ring and a proper ideal, the intersection of its powers in a finite module is zero.",
        "primary_sources": [
            {"author": "The Stacks Project Authors", "title": "The Stacks Project",
             "url": "https://stacks.math.columbia.edu/tag/00M9",
             "location": "Algebra, Lemma 10.96.3"},
            {"author": "The Stacks Project Authors", "title": "The Stacks Project",
             "url": "https://stacks.math.columbia.edu/tag/0BNH",
             "location": "Algebra, Lemmas 10.97.1--10.97.6"},
            {"author": "The Stacks Project Authors", "title": "The Stacks Project",
             "url": "https://stacks.math.columbia.edu/tag/00IP",
             "location": "Algebra, Lemma 10.51.4 (Krull intersection)"},
        ],
        "native_match": "DX5 applies these only to the explicit Noetherian universal ring/presentation and its actual origin. The continuous represented functor, unobstructedness, weights, satSq and the completion kernel annihilator are proved in the chapter.",
        "used_by": ["DX5"],
    },
]
dump("classical_inputs.json", {
    "schema": "rh-classical-input-registry/1", "artifact_version": "0.27",
    "component": COMP, "commit": PIN,
    "inputs": classical,
    "inherited_matched_inputs": [
        {"via": ["KB6", "LK1"], "statement": "Original decomposition group to henselization/completion equivalence, preserving inertia and the specified roots of unity; finite local field in its native algebraic closure."},
        {"via": ["LD3"], "statement": "Finite Poitou--Tate on the actual cochains and invariant family, including all coefficient and place quantifiers."},
        {"via": ["FP1", "FP2", "FP3"], "statement": "Complete Noetherian local algebra, actual continuous universal matrix lifts and formal-torus weight extraction, with their earlier elementary algebra inputs."},
    ],
    "not_assumed": [
        "Full BlochKatoLocal or arbitrary local period-module models",
        "Integral formal smoothness of the universal local deformation rings",
        "A compact subset of an algebraic closure being contained in a finite extension",
        "A deformation representability or local chart theorem beyond the proved FP and DX chains",
    ],
})

endpoints = [
    {"name": name, "supplied_by": "DX1", "scope": scope}
    for name, scope in [
        ("ReciprocityTheory.Gal.LocalFiniteness", "Full native interface for every prime and every finite coefficient module."),
        ("ReciprocityTheory.Gal.LocalTateDuality", "Full native interface, including nonfree modules and both degree-one orders; original target before choosing the invariant."),
        ("ReciprocityTheory.Gal.LocalEulerChar", "Full native interface and literal local-degree cardinality factor."),
        ("ReciprocityTheory.Gal.GlobalFiniteness", "Full native interface; only the higher-degree vanishing clause has its original odd-ell premise."),
        ("ReciprocityTheory.Gal.GlobalEulerChar", "Full native interface including ell=2 and real places, via the truncated Euler formula."),
        ("GlobalTheory.Published.PoitouTateNormalised", "Full original definition and quantifier order, projected from LD3 by forgetting ConjCompatible."),
    ]
]
endpoints += [
    {"name": "ReciprocityTheory.Gal.GreenbergWiles", "supplied_by": "DX3",
     "scope": "Full literal universal interface; GreenbergWilesAt itself retains 0<r, ell odd, ContainsAbove, original cyclotomic descent, arbitrary original local placements and local submodules."},
    {"name": "PhiCond D.Gam ell", "supplied_by": "DX2",
     "source_producer": "UpperTheory.V.GradeZeroInterpolatingElement.phiGam",
     "scope": "Original Good D and actual global quotient, plus local decomposition PhiCond."},
    {"name": "D.Nums", "supplied_by": "DX4",
     "source_producer": "UpperTheory.V.GradeZeroInterpolatingElement.nums",
     "scope": "Every original residual descent, Normalises proof and weight, on unchanged Good D."},
    {"name": "UpperTheory.V.Loc.spChartL", "supplied_by": "DX6",
     "scope": "Exact source fourteen-parameter completion/chart output on every original universal eqL ring, with full original Good hypotheses; obtained without the unused full BlochKatoLocal package."},
    {"name": "UpperTheory.V.GradeZeroInterpolatingElement.tanLz", "supplied_by": "DX6",
     "scope": "One integral nonzero denominator for each original negative-Psi tangent and actual inertia vanishing for every weight-zero tangent."},
    {"name": "UpperTheory.V.Loc.spChartP", "supplied_by": "DX7",
     "scope": "Exact source ten-parameter completion/chart output for every original q in Sb and universal eqP ring; entire inertia kernel killed in all Artin lifts."},
    {"name": "Nonempty (LocBase D)", "supplied_by": "DX8",
     "source_producer": "UpperTheory.V.GradeZeroInterpolatingElement.locBase",
     "scope": "All original record fields, same O and actual decomposition groups, unique arbitrary tuple maps, actual graded SmoothPt and counts dL(j)+|Sb|dP(j)."},
]
closure = {
    "schema": "rh-human-component-closure/1", "artifact_version": "0.27",
    "component": COMP, "commit": PIN,
    "main_tex_sha256": main_hash,
    "provenance_sha256": hashlib.sha256(prov_raw).hexdigest(),
    "closed_claim_ids": list(prov["dependency_graph"]),
    "dependency_graph": prov["dependency_graph"],
    "external_claim_dependencies": prov["external_claim_dependencies"],
    "literal_supplied_endpoints": endpoints,
    "remaining_bespoke_inputs_inside_stated_implications": [],
    "theorem_hypotheses_retained": [
        "The original Raw datum D satisfies the literal Good predicate. Its global construction is handled by the AX branch, not asserted anew here.",
        "The specified original coefficient O, fraction field, residual field, algebraic closure, decomposition places and local maps are retained.",
        "DX5 is a general chart-transfer implication whose actual local unobstructedness and tangent-count hypotheses are fully discharged in DX6 and DX7.",
    ],
    "not_promoted": [
        {"name": "GlobalTheory.Published.BlochKatoLocal",
         "reason": "Full arbitrary period-module/cohomology package is outside the reconstruction and unnecessary for the direct local chart proof."},
        {"name": "UpperTheory.V.Loc.LocalPublishedTheorems",
         "reason": "All six finite local fields are supplied via LK/DX, but the entire bk field remains outside scope."},
        {"name": "UpperTheory.V.GradeZeroInterpolatingElement.CohomologyHyp",
         "reason": "Finite local/global/PT/UO/GW fields are supplied; the containing loc record still includes the unpromoted bk field. The actual exModel consumer is supplied directly."},
        {"name": "Integral formal smoothness or integral regularity",
         "reason": "Only the actual characteristic-zero origin completion is proved smooth. The integral ring may have additional components or torsion."},
        {"name": "OnComp or global automorphy/rigidity/count suppliers",
         "reason": "Original ordinary-component specialization is AX8; global model and comparison are separate MX/PX chains."},
        {"name": "RH or Dirichlet GRH reconstruction",
         "reason": "This component closes local arithmetic installation inputs, not the remaining global dependency graph."},
    ],
    "new_classical_input_ids": [x["id"] for x in classical],
    "source_validation": prov["validation"],
}
dump("closure.json", closure)
dump("remaining_inputs.json", {
    "schema": "rh-component-remaining-inputs/1", "artifact_version": "0.27",
    "component": COMP, "main_tex_sha256": main_hash,
    "remaining_bespoke_inputs_for_DX2_DX4_DX8_on_Good_D": [],
    "named_classical_inputs": [x["id"] for x in classical],
    "incoming_arithmetic_hypothesis": "Original D.Good, with actual facts supplied by AX6.",
    "larger_unpromoted_packages": closure["not_promoted"][:3],
    "consumer_join": "FP8 and the DX2/DX4/DX8 installed inputs feed the independent MX10 original Model constructor; no new local predicate remains.",
})
dump("input_registry.json", {
    "schema": "rh-component-input-registry/1", "artifact_version": "0.27",
    "component": COMP, "main_tex_sha256": main_hash,
    "claim_inputs": prov["external_claim_dependencies"],
    "classical_registry": COMP + "/classical_inputs.json",
})
dump("next_targets.json", {
    "schema": "rh-component-next-targets/1", "artifact_version": "0.27",
    "component": COMP, "next_targets_within_this_component": [],
    "integration_joins": [
        {"consumer": "MX10", "supplied_ids": ["DX2", "DX4", "DX8"],
         "condition": "The same original Good D must be used throughout."},
        {"consumer": "PX global tangent/comparison", "supplied_ids": ["DX1", "DX6"],
         "condition": "Use exact original local characters and tanLz denominator; ordinary component specialization remains AX8."},
        {"consumer": "CountV native cohomology inputs", "supplied_ids": ["DX1", "DX3"],
         "condition": "Promote only the literal native finite interfaces proved here, not arbitrary host/model conclusions."},
    ],
})
report = f"""V0.27 — Complete arithmetic symplectic local installation

Component: {COMP}
Pinned source: {PIN}
Main SHA256: {main_hash}
Provenance SHA256: {hashlib.sha256(prov_raw).hexdigest()}

Outcome
DX1--DX8 close the original PhiCond, Nums and actual LocBase inputs of exModel
on every unchanged Good datum.  This is an actual supplier chain.  The integral
universal representations, arbitrary target maps, ordinary and finite-inertia
formal germs, all torus weights, the graded satSq chart return and the completed
local coproduct are constructed.  There is no remaining bespoke local supplier
inside these stated implications.

The central simplification
The ordinary germ is four negative flag directions plus two unramified torus
directions plus four positive-root cocycle spaces, each two-dimensional.
Positive-root H2 vanishes because every root character differs from 1 and chi.
This proves unobstructedness as well as the exact fourteen parameter weights.
At q in Sb, every Artin representation kills the entire actual Iq intersect
ker psi.  Its quotient is finite cyclic inertia times Zhat.  Explicit averaging,
symplectic form correction, a six-dimensional Cayley slice and the GL2
centralizer give exactly ten weighted parameters.  Averaging is only over E.
The integral rings themselves are not asserted smooth.

Exact outgoing interfaces
DX1: native LocalFiniteness, LocalTateDuality, LocalEulerChar,
     GlobalFiniteness, GlobalEulerChar and PoitouTateNormalised.
     GlobalEulerChar includes 2 via Milne's explicitly truncated ratio.
DX2: actual PhiCond(D.Gam), and local decomposition PhiCond.
DX3: full native GreenbergWiles with its original odd-prime premise, and exact
     framed cochain Euler identity.
DX4: original D.Nums, all descents, normalization proofs and weights.
DX5: integral representability and exact generic completion/graded chart join.
DX6: ordinary fourteen-parameter chart and literal tanLz.
DX7: finite-inertia ten-parameter chart on all original q in Sb.
DX8: actual original LocBase with counts dL(j)+|Sb|dP(j).

Scope
Full BlochKatoLocal, LocalPublishedTheorems and CohomologyHyp are not promoted.
Their six finite local fields and other finite cohomology fields are supplied,
but their unused full period-module field remains outside scope.  The actual
Model arithmetic prerequisites are discharged directly.  Good itself and
ordinary OnComp specialization are the separate AX branch; the Model and
global point comparisons are MX/PX.  No claim of RH or GRH completion is made.

Provenance
{prov['validation']['claim_source_links']} exact claim source links,
{prov['validation']['scope_boundary_source_links']} exact scope-boundary links,
{prov['validation']['source_files_checked_against_pinned_git_blobs']} pinned source files,
and eight separately hashed human-proof ranges.
All source bytes were checked against the pinned Git blobs.
No Lean kernel replay and no PDF generation were performed.
TeX draft validation is recorded separately in tex_validation.json.
"""
(HERE / "report.txt").write_text(report)
print(json.dumps({
    "main_tex_sha256": main_hash,
    "provenance_sha256": hashlib.sha256(prov_raw).hexdigest(),
    "closure_sha256": hashlib.sha256((HERE / "closure.json").read_bytes()).hexdigest(),
    "claim_count": len(prov["claims"]),
    "claim_source_links": prov["validation"]["claim_source_links"],
    "scope_boundary_source_links": prov["validation"]["scope_boundary_source_links"],
    "source_files": prov["validation"]["source_files_checked_against_pinned_git_blobs"],
}, indent=2))
