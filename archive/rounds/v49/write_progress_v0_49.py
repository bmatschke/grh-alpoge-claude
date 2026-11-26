#!/usr/bin/env python3
"""Generate the substantive v0.49 progress report and current README.txt.

Inventory and closure figures are read from the integrated v0.49 records.
This script never integrates, edits a proof, or changes a dependency ledger.
Use --check to validate all inputs and prose without writing either TXT.
"""
from __future__ import annotations

import argparse
from collections import Counter
from datetime import date
import hashlib
import json
from pathlib import Path
import textwrap


VERSION = "0.49"
PIN = "7cbf7a0c32fca1badf05931879a37c3f8a2b03b4"
OUTPUT = "RH_reconstruction_progress_v0_49.txt"


CHAPTERS = [
    (
        "witness_realization_v49", "WRS", 10,
        "THE ACTUAL BUILT FAMILY AND THE COMPLETE LOCAL GAIN",
        """
The whole-contract advance is GLOBAL_LOCAL_GAIN. Earlier chapters proved
the quantitative local-gain argument from two classwise inputs: actual
group compatibility and the prescribed admissible top data. GCF supplied
the complete true-volume column stage and comparison transport, and the
selected D3 class already supplied the tops. The remaining issue was
whether compatibility held on the family's given objects, including their
actual comparison maps and kernels. This chapter proves that it does.
[WRS4–WRS9; GCF16–GCF18; LGS13]

The proof uses information already present in membership of the original
built class. A Built witness contains the complete split-prime column
data and one dependent equality of the group, comparison, twisted forms
and kernel. Its actual constructed point BPt is obtained by the source's
designated division-lattice operation. No compatibility predicate is
added to the class, and no independently chosen kernel is substituted.
[WRS3–WRS6]

The first step checks that operation field by field. An arbitrary setDiv
changes the division submodules, their heights and the derived maximum
HH. The coefficient field, local embeddings, lattice tuples, ideal
classes, Taylor series and semilinear maps remain fixed. All seventeen
LocalToGlobal2 fields transport, including the integral-span and chain
identities. All nine KerT fields and the full EntC presentation transport
as well: the quotient evaluation, chosen section, minor functionals,
normalizing scalar and four KerEntHyp clauses still refer to the same
maps. This is transport of the actual geometric kernel. [WRS1–WRS2]

One transport map is then applied to the entire dependent tuple. This
matters because the kernel's type depends on the preceding comparison
data and the given Gy identification. Separate equalities of separately
chosen objects would not give the required result. The transported column
data supply full ColsExtraTiedS and every GroupCompatibilityAll field on
the supplied Extra. The actual BPt uses precisely nPrime and hExpl6;
pointObj_pt identifies its whole smaller object with the transported
core. Thus its comparison and kernel are the original ones. [WRS3–WRS5]

For any member of the unchanged class Fc.cls(Q,Lk,E), the membership
record gives one joint equality of (D,O,b) with that BPt and its bundle.
Transport through this equality supplies compatibility for every actual
x,hx,i. The selected IsGoodE predicate and its further original
conjunctions imply IsBuilt simply by forgetting fields. The arbitrary
bundle type, linkage and additional property E remain unchanged.
Compatibility therefore holds with the common threshold

                         x_g = Fm.x1 + 1.

Its Closed form chooses its cutoff and coefficient bound before the
family and external CH. The other Closed input follows from the original
D3 ChosenE field, retaining its own internal witness and the threshold
max(x_a,x_b,Fm.x1+1,(16C_b+2)^(3/epsilon)). Internal and external CH
are not identified. [WRS6–WRS8]

The completed LGS consumer now applies to those actual inputs. It retains
the coefficient cutoff 1/104, the mid bound 4129, the last bound
max(5600002,C_orb(epsilon)), the normalized lattice lengths, empty-served
cases, served-orbit coverage and both MeanKappaBound clauses. The gain
constant and error remain

             C_G = 4C_count + 1,    delta(x) = x^(-epsilon/2),
             b_o = b^delta(x).

All five LinkG_at fields hold on the same family, with delta tending to
zero before later indices and places vary. The chapter also proves the
universal original link_g implication for arbitrary classes at its
original TSel and Duty premises. [WRS9–WRS10]

For the selected built class, the stronger full WPt/RecT/TSel route is
unnecessary for this conclusion. It remains a separate producer wherever
other arguments need its row, host and Weil data. Likewise, a theorem
holding for every member of a class does not construct a common nonempty
design in that class. DESIGN_CHOICES_COMMON and the other selected global
comparisons remain open. The exact frozen predecessor contract is quoted
verbatim and hashed in this component's closure_comparison.json.
""",
    ),
    (
        "unramified_coefficient_extension_v49", "UCE", 19,
        "ORDINARY END DATA AND EVERY COEFFICIENT-ALGEBRA POINT",
        """
This chapter advances the actual AUT_UNRAM_COEF chain. It proves the full
implication from one original common ordinary end datum GdEnd to
AutomorphyUnramifiedCoefficients. GdEnd must supply the same marked
element g1 for FinEnd, rank-three AutEnd3 and rank-two AutEnd2. The chapter
does not construct that arithmetic datum. Its contribution is the full
curve, finite-generation and specialization argument that turns those
end conditions into FinA, AutB and universal LemW together. [UCE19]

The local work covers every original coefficient characteristic.
The actual inertia separator satisfies Psi(x)^2-1 being a unit. Over
the original local crystalline component, polynomial identities obtained
from all finite formal truncations give the ordered generic flag. A
valuation ring dominating a specialization carries that flag to the
specialized field; a finite-type basis scheme gives the required finite
field extension even though the group supplies infinitely many equations.
Noetherianity reduces their ideal to finitely many equations. [UCE1–UCE3]

The separator then gives integral projectors

            P_i = product_(j != i) (r(x)-d_j I)/(d_i-d_j),
            (d_0,d_1,d_2) = (Psi(x),1,Psi(x)^(-1)).

All denominators are units. Applying each projector to its coordinate
vector and normalizing produces a basis congruent to the identity.
Comparison with the generic ordered flag proves the full integral
CondT statement. Every local-domain specialization of the actual
normalized global ring is consequently an ordinary point, with the same
residual, continuity, normalization, away-inertia and local flag fields.
[UCE4–UCE5]

The ring has a finite power-series presentation by actual matrix-entry
deviations of weights w_i-w_j, where (w_0,w_1,w_2)=(1,0,-1).
Conjugation by T(1+T) gives integral homogeneity. Modulo each maximal-ideal
power, substitution Z=1+T is injective on Laurent polynomials; comparing
coefficients proves that each weight projection of a relation is again
a relation. This avoids division by torus eigenvalue differences in the
coefficient ring. Finite minimal exponent vectors generate the weight-zero
monoid and every fixed-weight module. [UCE6–UCE7]

A surviving element modulo the coefficient uniformizer is detected by
a characteristic-prime DVR curve. Choose a prime maximal among those
avoiding it. The quotient is one dimensional by the principal ideal
theorem and prime avoidance. Its finite residue field lifts by the roots
of X^q-X; the quotient is finite over a one-variable power-series ring,
and its fraction field supplies the complete DVR. Applying these curves
to weight-zero monomials proves the full original FinCrit. Torsion and
nonreduced rings remain within scope. [UCE8–UCE9]

The finite-end input is converted into a triangular statement without
an exception at characteristic three. Equality of characteristic
polynomials on a finite-index subgroup first implies equality everywhere:
take a power of each element, then use the fact that an element algebraic
over the finite residue field and congruent to a specified constant must
be that constant. Normalization gives the matrix difference
zeta*diag(1,0,-1), with zeta a unit. Its projectors force invariant
subspaces to be coordinate subspaces. [UCE10–UCE11]

If a full three-dimensional block or the outer two-dimensional block
were irreducible, its marked projectors and nonzero entry paths would
span the whole matrix algebra. Choose group matrices M_i forming a basis.
The trace Gram matrix tr(M_i M_j) is nonsingular, and its entries are
constants. Reduction must preserve its nonzero determinant. But all
reduced group matrices are diagonal, so that Gram matrix has rank at
most n instead of n^2. This contradiction gives the original upper-or-lower
triangular alternative. FinEnd therefore kills one sign of entry
deviations on every test curve and yields literal FinA. [UCE11–UCE12]
The abstract characteristic-three argument adds no exclusion. The final
Dat application retains the original GD.gen condition, ell-1 not dividing
2e, which itself excludes ell=3 in that arithmetic application.

Under FinA, the finite weight-zero entry algebra is compact and closed
inside the completed ring S; polynomial approximation identifies it
with S_0. The full entry algebra is the direct sum of the homogeneous
pieces S_j, each finite over the coefficient ring O. For an arbitrary
algebra map xi to the supplied algebraic closure, balanced monomials
force strict inequalities between the possible rescaling slopes. One
rational slope makes every chosen deviation strictly small under
xi_t(s)=t^j xi(s) for s in S_j. [UCE13–UCE14]

All values then lie in one finite coefficient field. On each finite
O-module S_j the restricted map is continuous; this justifies evaluation
of homogeneous formal relations. Uniform decay by total degree permits
regrouping the full series. Thus the rescaled map extends to the completed
S in a finite coefficient DVR, with agreement on every original entry.
No continuity or localness of the initial xi was assumed. The resulting
ordinary representation is exactly T(t)rT(t)^(-1) on both connected and
disconnected components. [UCE15–UCE16]

Irreducibility persists on every open subgroup. Otherwise the normal-core
restriction has three character lines permuted transitively. Ordered
inertia supplies distinct eigenvalues and a residual separator; a
three-cycle would force tr(r(gx^m))=0. The equations for m=0,1,2 contradict
the separator's condition. Finally the exact torus conjugacy transports
rank-three automorphy and every supplied outer rank-two extension, at
the fixed iota and original cyclotomic twists. GdEnd remains the single
open arithmetic producer input to this completed consumer; its named
inherited local and component foundations remain explicit. [UCE17–UCE19]
""",
    ),
    (
        "holomorphic_uniformization_v49", "HUF", 21,
        "THE FINITE HOLOMORPHIC UNIFORMIZATION FAMILY",
        """
The geometric advance is the whole original N1c theorem and every
FamilyUnif field. The preceding PUN chapter constructed individual
primitive moduli points. This chapter builds the finite positive
holomorphic family, including arbitrary-choice holomorphy, exact fiber
and lift statements, and the prescribed theta frames. The original
representing Moduli record remains supplied. The fixed complex embedding,
ordered type, level, two markings and projective O_E lattice are retained.
[HUF1–HUF21]

The source tests for holomorphic maps and dual-number derivatives are
first identified with ordinary analytic maps and tangent vectors. The
actual universal group becomes a proper smooth family of abelian
varieties, with its Lie bundle split into the prescribed embedding
eigenbundles. Local holomorphic eigenframes can match any prescribed
initial eigenbasis. The exponential of each fiber is surjective with
full lattice kernel. Its Appell–Humbert form and the original commutator
convention give the exact Weil scalar

                    exp(-2 pi i B(a,b)/n),    n>0.

The original Tate comparison recovers integral quotient maps at every
positive level, their compatibilities, t at lcm(M,A), the fixed root
and both markings. The reverse-point theorem consequently applies to
every given point over the prescribed embedding. [HUF1–HUF6]

Local continuation preserves any specified initial period and
exponential. Continuing a finite period basis initially gives a lattice
contained in the kernel. The quotient torus maps properly and locally
biholomorphically to the actual family; its covering degree is one at
the initial point and hence throughout a connected neighborhood. This
proves that the continued lattice is the entire kernel. The integral
alternating form is locally constant on the continued cycles, and the
two markings are sections of finite torsion coverings. One neighborhood
therefore preserves both markings and every positive-level Weil pairing.
There is no infinite sequence of shrinking neighborhoods. [HUF7–HUF8]

The period coordinates have precisely dimension f*p*q. Marked exponential
uniqueness uses the full original congruences and covers odd M=3. The
local map from a smooth moduli chart to the period domain is injective
by the already reconstructed marked-point equality; the injective
holomorphic-map theorem makes it locally biholomorphic. This proves
holomorphic dependence for arbitrary pointwise choices of the
uniformizing points and exponentials. Their continuity is part of the
conclusion. An analytic representing property for the moduli problem
is not inserted as an assumption. [HUF9–HUF12]

To obtain one finite family, use a finite affine cover and finiteness of
connected components of semialgebraic sets. The moduli scheme itself
need not be compact. Two marked integral genus data have intersecting
period images exactly when an integral isometry satisfies both source
congruences: the M congruence on the specified half-lattice and the A
congruence on the full lattice. Their images are equal or disjoint,
nonempty and open, and cover the prescribed complex moduli points.
Only finitely many such classes occur. [HUF13–HUF14]

Choose one representative of each class before any later period or
analytic base. Existing nonemptiness makes the number positive. The
point and exponential functions are total on all additive maps, with
harmless specified values on invalid periods. The arbitrary-choice
holomorphy theorem now applies to these same functions on every later
base. The integral congruences prove the exact fiber identity, and local
continuation proves the lift field without changing the selected family.
[HUF15–HUF16]

The theta construction preserves the first-linear Hermitian convention.
The source symplectic sign and positive imaginary part force the required
sign, and the actual primitive semicharacter determines one constant
half-characteristic. The resulting factors are exactly

     exp(2 pi i c_1.m - pi i n.tau.n - 2 pi i n.(w+c_2)).

They define a line whose fibers match the actual universal line.
Grauert's direct-image and analytic base-change theorem applies to
their Hom line, whose fiber space of sections has dimension one.
Rigidification then gives a global normalized frame on the original
open base, with no Stein or simply connected hypothesis. Fiberwise
projective GAGA supplies the required algebraic section. All five
IsThetaFrame clauses and the final N1c installation follow.
[HUF17–HUF21]

Appell–Humbert, the Riemann algebraicity theorem, GAGA, analytic local
theorems, the finite-component theorem and the precise Grauert theorem
with its corrigendum are separately named foundations. The numbered
claims prove their applications and the finite constructions. The
adjoining simultaneous framed-point choices FramesOK/CoverTri/FibTri,
the full IsUnf/FromTest dictionary and the final principal-chart
constructor remain separate. These are stronger remaining contracts
than the theta-frame family just completed.
""",
    ),
    (
        "bessel_wave_packets_v49", "BWP", 24,
        "NORMALIZED BESSEL PACKETS AND THE ANALYTIC SETTING",
        """
This chapter constructs the analytic Bessel packets on the original
representations and measures. It proves complete weighted-coefficient,
local-packet and global-assembly statements. The sole unproved local
input to its nonzero packet construction is the original BesselNVGap:
some prescribed endomorphism-valued Bessel integral must be nonzero.
The final setting conclusion retains that input and the inherited
supplied Forms0 scope. No whole spectral or global setting obligation
is declared closed. [BWP6, BWP14, BWP18, BWP24]

The literal unipotent group has an explicit global polynomial chart of
real dimension 2r^2+2rk+r, including r=0. Its multiplication has
Jacobian one in the chosen coordinates, giving Haar measure. A quadratic
bound for inverse coordinates proves the required reciprocal-norm
integral at the original exponent. The actual stabilizer is a closed
compact-by-unipotent group with unique factorization, unit modular
character and the exact psiGen. These statements apply to the supplied
weak Haar measures through the previously proved Haar promotion.
[BWP1–BWP3; AMD8]

A compact reproducer is built inside every prescribed identity
neighborhood. Harish–Chandra admissibility, retained as its named
classical foundation, makes the relevant compact-isotypic space finite
dimensional. A conjugation-averaged approximate identity acts invertibly
on that space. Cayley–Hamilton expresses its inverse action as a finite
linear combination of convolution powers, with support still inside
the chosen neighborhood. This supplies exact reproduction of the given
lowest vector. [BWP4]

Put n=2r+k+1, R=r+1 and N=4n^2*sqrt(2R). Every original cubic-gap
witness gives a lower bound h for all opposite-sign parameter
differences. For q_0=min(p,q)>0 it satisfies

                     h > 16n q_0 + 8N sqrt(2q_0).

The earlier discrete-series identification applies to the given
representation and lowest vector. Its coefficient estimate, multiplied
by the operator-norm weight and polar Jacobian, has large-radius rate
-h/(8sqrt(2q_0))+N+n sqrt(2q_0)<0. Radial integration proves the
whole original CoefWeightedLoc; the compact case is immediate from
continuity. [BWP5–BWP6; DC6, DC13]

For the supplied Haar measure, the kernel remains exactly

 d_sigma = ||w||^4 / integral |<w,sigma(g)w>|^2 dmu_G(g),
 e(g) = d_sigma conjugate(<w,sigma(g)w>).

Schur orthogonality gives integral e(g)sigma(g)w=w with this formal
degree. The invariant quotient height is the original infimum of
operator norms along the stabilizer. It is measurable and at least one.
Compact reproduction and the unipotent integral justify absolute
convergence and continuity of the vector-valued Bessel average A(x).
Equivariance, the exact Weil quotient formula and Tonelli give ordinary
and N-weighted quotient L1. The bound ||A||<=C*height^N then gives
finite squared L2. [BWP7–BWP13]

BesselNVGap supplies a nonzero endomorphism integral. Evaluating on a
vector with nonzero image gives A(x) nonzero. Continuity and the actual
quotient identity prove positive L2 even when the supplied ambient
quotient measure is not a preferred section measure. Normalize by
L2^(-1/2). A weighted joint norm bound justifies Bochner Fubini before
transporting either reproducer into the packet. All seven WlocExists
conclusions follow: continuity, exact equivariance and convolution,
L1, squared L2 equal to one, weighted L1 and compact reproduction.
[BWP14–BWP18]

Global assembly preserves two different coordinate changes. With Q the
given frame and P0 a Euclidean unitary Cayley matrix, use

 C_G(g)=P0^(-1)gP0,  C_S(s)=Q^(-1)sQ,  T(x)=Q^(-1)xP0.

Then T(sx)=C_S(s)T(x) and T(xg)=T(x)C_G(g). These identities
give the correct subgroup action, convolution and quotient pushforwards
while retaining the given lowest vector. The local character coefficient
4pi/g_D becomes exactly the source's global additive character.
The formal-degree integral is unchanged. [BWP20]

If the actual global subgroup measure is a times the product of chosen
local Haar measures, the quotient product scalar is C=a^(-1).
Multiply one local packet by C^(-1/2) and apply the supplied tensor map.
Its inner-product and spanning identities prove multilinearity and the
product norm formula. The resulting WBlk has every IsWu field on the
actual quotient measure, including squared L2 exactly one. The product
compact reproducer and weighted estimate give WuDecay for every later
MBlk; the required order is exists WBlk before forall MBlk.
[BWP19–BWP22]

Finally, the source global gap 16n^19 supplies each local cubic gap
using the odd witness t=n+6. The complete WFromLoc follows. On the
supplied Forms0 scope, the earlier ASG blocks and AMD measured block
then give ConcreteSettingExists, including one bridge, exact MeasTie,
decay and kernel integrability. BesselNVGap, the subsequent orbital and
Siegel–Weil comparisons, and the common-family row ties and counts
remain separate producers. [BWP23–BWP24; ASG1–ASG17; AMD12]
""",
    ),
]


NEXT_PRODUCERS = """
THE REMAINING PRODUCERS AND THE NEXT PARALLEL WORK

The local-gain closure removes an actual supplier from the selected
global argument. It does not remove the need to build one common family
on which all other estimates hold. The remaining work should use the
completed interfaces at their exact scope and preserve the original
choices of fields, maps, metrics, measures and thresholds.

First, arithmetic should construct the common GdEnd datum. UCE has
completed the downstream implications FinEnd -> FinA and FinA -> finite
ordinary representatives of every entry-algebra point, together with
the all-open irreducibility and both automorphy transports. What remains
is to supply FinEnd, AutEnd3 and AutEnd2 on the same marked g1 before
the later universal rings and points. The actual frame and seed choices,
general PfromAut/ModUAlt suppliers and descent keep their original
premises. Separate witnesses for those three end conditions would not
complete AUT_UNRAM_COEF. [UCE12, UCE16–UCE19]

Second, geometry can consume the now-proved N1c and full FamilyUnif.
The explicit next constructor is FrameUnif.exists_unf_hasPrinc in
CongrOfDvdModulus.lean. Its arithmetic genus models, quadratic norm
comparison, cusp lattice LatZ and l.A=1 Fourier exponent comparison
already have reconstructed inputs. The adjoining simultaneous framed
points and normalizations, full analytic IsUnf dictionary and reduced
test-ring AllTest/FromTest must now be supplied on those same models.
A bounded next supplier is allTest_of_secBaseChange in
FramedPointReducedFromTestRing.lean, using the finite-presented FrPt
frame bundle at the original SecBaseChangeSt premise. The supplied
Moduli record remains part of the original input scope.
[HUF21; PUN1–PUN13]

Third, the analytic branch should prove the exact BesselNVGap
endomorphism nonvanishing theorem for every original local parameter,
representation and Haar pair. The packet convergence, coefficient bound,
normalization, local-to-global assembly and decay are now written.
After nonvanishing, the setting must be linked to the original orbital
and fiber measures, characters and convergent Siegel–Weil statement.
The full transport, row dictionaries, FinX and common count inputs remain
stronger requirements than existence of the analytic setting alone.
[BWP14, BWP18, BWP24]

Fourth, the quantitative global branches still need their actual
denominator, retained-defect, period/height and spectral data and
inequalities. Completed finite row estimates and conditional consumers
should be reused, preserving the actual same-family normalizations and
eventual rank guards. WRS supplies compatibility and local gain on every
member of the unchanged built class. It neither constructs the common
nonempty design nor supplies the stronger full RecT/TSel record used
by the other comparisons. These are separate remaining obligations,
not additional assumptions on the newly proved local-gain endpoint.
[WRS6–WRS10; GQT1–GQT7; FLC19]

These four starting points can proceed in parallel. Their interfaces
must be joined only after the original same-object equalities and
choice order are established. The current remaining-leaf register
records the whole selected contracts; each new chapter records which
internal producers within those contracts have been completed.
"""


READING_AND_CHECKS = """
READING, FOUNDATIONS AND REPRODUCIBILITY

RH_new_proofs_v0_49.tex contains the current audit and the four new
chapters. RH_readable_reconstruction_v0_49.tex is the cumulative reader.
The complete delivery pairs these TeX manuscripts with this substantive
TXT report and the full ZIP. Every component includes the human proof,
exact source contract and range hashes, retained foundations, repeatable
metadata builder and standalone TeX validation. Independent mathematical
reviews bind to the text and individual claims; integration and semantic
reviews check the assembled records and scope.

Named classical theorems remain explicit foundations. Their applications
are matched to the actual objects and conventions in the written proofs;
recording a source hash alone would not supply that mathematical argument.
Original open antecedents and external foundations remain separate from
the numbered proof graph. The accepted source pin is unchanged. No Lean
build or kernel replay is performed. Completion of the remaining original
producers is still required for a full human-readable proof of RH and
unrestricted Dirichlet GRH.
"""


def read_json(root: Path, relative: str):
    return json.loads((root / relative).read_text(encoding="utf-8"))


def clean(text: str) -> str:
    return textwrap.dedent(text).strip()


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def build_report(root: Path) -> tuple[str, dict]:
    cfg = read_json(root, "increment_v0_49.json")
    stats = read_json(root, "integration_stats_v0_49.json")
    graph = read_json(root, "dependency_audit_v0_49/obligation_map.json")
    register = read_json(root, "dependency_audit_v0_49/remaining_leaf_register.json")
    assert cfg["artifact_version"] == graph["artifact_version"] == VERSION
    assert register["artifact_version"] == VERSION
    assert cfg["source_commit"] == graph["source_commit"] == PIN
    assert set(cfg["closed_selected_leaves"]) == {"GLOBAL_LOCAL_GAIN"}
    assert set(cfg["components"]) == {row[0] for row in CHAPTERS}

    claims = []
    chapter_rows = []
    for component, prefix, count, title, body in CHAPTERS:
        ledger = read_json(root, component + "/provenance.json")
        assert ledger["source_commit"] == PIN
        cs = ledger["claims"]
        assert [c["id"] for c in cs] == [prefix + str(i) for i in range(1, count + 1)]
        proof = root / component / "main.tex"
        assert sha256(proof) == ledger["proof_file_sha256"]
        claims.extend(cs)
        chapter_rows.append(
            f"{prefix}1–{prefix}{count}: {len(cs)} claims; {component}/main.tex"
        )
    classifications = Counter(c["classification"] for c in claims)
    assert len(claims) == stats["new_claims"]

    nodes = {node["id"]: node for node in graph["nodes"]}
    assert len(nodes) == stats["selected_nodes"]
    assert sum(len(node["requires"]) for node in nodes.values()) == stats["selected_edges"]
    records = register["records"]
    open_ids = {record["id"] for record in records}
    open_classes = Counter(record["category"] for record in records)
    assert len(open_ids) == len(records) == stats["open_count"]
    assert dict(open_classes) == stats["open_categories"]
    assert "GLOBAL_LOCAL_GAIN" not in open_ids
    assert {"DESIGN_CHOICES_COMMON", "AUT_UNRAM_COEF"} <= open_ids

    def reachable(start: str) -> set[str]:
        seen = set()
        todo = [start]
        while todo:
            item = todo.pop()
            if item not in seen:
                seen.add(item)
                todo.extend(nodes[item]["requires"])
        return seen

    rh, grh = reachable("ORDINARY_RH"), reachable("DIRICHLET_GRH")
    extra = sorted((grh - rh) & open_ids)
    assert len(open_ids & rh & grh) == stats["shared_open"]
    assert len(extra) == stats["extra_grh_open"]
    day = date.fromisoformat(cfg["date"]).strftime("%d %B %Y").lstrip("0")
    paragraphs = [
        "RH AND UNRESTRICTED DIRICHLET GRH — HUMAN RECONSTRUCTION v0.49",
        day + "\nAccepted source commit: " + PIN,
        "CURRENT RESULT",
        clean("""
        Version 0.49 completes GLOBAL_LOCAL_GAIN. The actual original
        built-class membership supplies compatibility on the given
        comparison maps and kernels; the previously proved quantitative
        argument then yields the full local-gain contract. Three further
        chapters prove the complete finite holomorphic uniformization
        family, the ordinary-end-to-coefficient-automorphy implication,
        and normalized local/global Bessel-packet constructors with their
        original nonvanishing premise retained.

        The human-readable reconstruction remains incomplete. Common
        design existence, the arithmetic common-end supplier and the
        remaining analytic and global comparisons are still required.
        This report explains the new proofs, their exact normalizations
        and the remaining original producers.
        """),
        "INTEGRATED INVENTORY",
        "\n".join([
            f"New human claims: {stats['new_claims']} "
            f"({', '.join(str(v) + ' ' + k for k, v in sorted(classifications.items()))}).",
            f"Cumulative claims: {stats['cumulative_claims']}; predecessor records retained: "
            f"{stats['cumulative_claims'] - stats['new_claims']}.",
            f"Selected dependency graph: {stats['selected_nodes']} nodes and {stats['selected_edges']} edges.",
            f"Whole obligations still open: {stats['open_count']} "
            f"({open_classes['C']} C and {open_classes['B']} B).",
            f"Shared RH/Dirichlet-GRH obligations: {stats['shared_open']}; "
            f"additional Dirichlet-GRH obligations: {stats['extra_grh_open']}.",
            f"Increment source inventory: {stats['new_source_files_checked']} pinned files "
            f"and {stats['new_unique_source_ranges_checked']} distinct cited ranges.",
        ]),
        clean("""
        These figures are read from the integrated v0.49 records and
        checked against every new claim and the final dependency graph.
        Class B denotes a written human proof at its stated scope;
        external foundations are separately identified. Counts describe
        the inventory, not a completion percentage. Completing an
        internal theorem need not close its larger selected obligation.
        """),
        "\n".join(chapter_rows),
    ]
    for index, (component, prefix, count, title, body) in enumerate(CHAPTERS, 1):
        paragraphs.extend([
            f"{index}. {title} ({prefix}1–{prefix}{count})",
            clean(body),
            "Proof and exact source/range map: " + component + "/main.tex; "
            + component + "/provenance.json.",
        ])
    paragraphs.extend([
        clean(NEXT_PRODUCERS),
        "THE ADDITIONAL DIRICHLET-GRH FRONTIER",
        f"The final graph has {len(extra)} open obligations reachable from "
        "Dirichlet GRH but not from ordinary RH. Their exact registered IDs "
        "and contracts are:",
        "\n\n".join(
            f"{item} ({nodes[item]['category']}): {nodes[item]['contract']}"
            for item in extra
        ),
        clean("""
        These preserve the original tensor-factor and residual-chain
        conditions, one compatible seed and the fixed embedding before
        later towers. The new rank-three coefficient consumers and local
        gain do not identify or close these additional contracts.
        """),
        clean(READING_AND_CHECKS),
        "REPORT INPUT BINDINGS\n"
        + "increment_v0_49.json SHA256: " + sha256(root / "increment_v0_49.json")
        + "\nintegration_stats_v0_49.json SHA256: "
        + sha256(root / "integration_stats_v0_49.json"),
    ])
    report = "\n\n".join(paragraphs).rstrip() + "\n"
    words = len(report.split())
    if not 3000 <= words <= 4500:
        raise ValueError(f"Progress report has {words} words; expected 3000–4500")
    return report, {
        "artifact_version": VERSION,
        "output": OUTPUT,
        "words": words,
        "new_claims": stats["new_claims"],
        "cumulative_claims": stats["cumulative_claims"],
        "whole_closures": sorted(cfg["closed_selected_leaves"]),
        "remaining_whole": stats["open_count"],
        "extra_grh": len(extra),
    }


def build_readme(root: Path) -> str:
    stats = read_json(root, "integration_stats_v0_49.json")
    cfg = read_json(root, "increment_v0_49.json")
    day = date.fromisoformat(cfg["date"]).strftime("%d %B %Y").lstrip("0")
    sections = [
        "RH AND UNRESTRICTED DIRICHLET GRH — HUMAN RECONSTRUCTION v0.49",
        day + "\nAccepted source commit: " + PIN,
        "CURRENT RESULT",
        clean("""
        Partial human reconstruction, accepting the pinned Alpoge-Claude
        formal source as fully checked and correct. Version 0.49 completes
        GLOBAL_LOCAL_GAIN: actual compatibility on the unchanged built
        class supplies the full original local-gain contract. The common
        nonempty design is separate. The complete human proof of RH and
        unrestricted Dirichlet GRH remains unfinished.
        """),
        f"There are {stats['new_claims']} new claims and "
        f"{stats['cumulative_claims']} cumulative claims. The selected graph retains "
        f"{stats['selected_nodes']} nodes and {stats['selected_edges']} edges. "
        f"The {stats['open_count']} remaining whole obligations comprise "
        f"{stats['open_categories']['C']} C and {stats['open_categories']['B']} B; "
        f"{stats['shared_open']} are shared RH/GRH obligations and "
        f"{stats['extra_grh_open']} are additional Dirichlet-GRH obligations. "
        f"This increment cites {stats['new_source_files_checked']} pinned files "
        f"in {stats['new_unique_source_ranges_checked']} distinct ranges. "
        "Claim counts are an inventory, not a completion percentage.",
        "READING ORDER",
        clean("""
        1. RH_reconstruction_progress_v0_49.txt: substantive mathematics,
           exact endpoints, retained hypotheses and next producers.
        2. RH_new_proofs_v0_49.tex: the audit and four new chapters.
        3. RH_readable_reconstruction_v0_49.tex: the cumulative manuscript.
        4. RH_dependency_audit_v0_49.txt: remaining selected contracts.
        5. continuation_checkpoint.json, next_source_targets.json,
           provenance.json and dependency_audit_v0_49/: exact continuation
           and dependency records.
        """),
        "FOUR NEW CHAPTERS",
        "\n".join(
            f"{component}/main.tex — {prefix}1–{prefix}{count}: {title}."
            for component, prefix, count, title, _ in CHAPTERS
        ),
        clean("""
        WRS proves all given-Extra comparison and kernel transports,
        actual BPt realization and both original Closed inputs on the
        unchanged selected class, then full LinkG with its constants and
        thresholds. UCE proves the original curve and finite-generation
        criteria, ordinary realization of every entry-algebra point,
        all-open irreducibility and the same-g1 GdEnd implication.
        HUF supplies full N1c/FamilyUnif, arbitrary-choice holomorphy,
        exact marked fibers/lifts and global theta frames on the supplied
        Moduli. BWP supplies weighted coefficients, normalized local
        packets, exact global tensor and measure assembly, and decay for
        every later measured block, retaining BesselNVGap.
        """),
        "REMAINING SCOPE",
        clean("""
        Arithmetic must supply the actual common GdEnd conditions before
        AUT_UNRAM_COEF is complete. Geometry must join N1c to the
        simultaneous framed-point choices and full IsUnf/FromTest
        principal-chart dictionary. The Bessel nonvanishing theorem,
        orbital/fiber and Siegel–Weil comparisons, and common transport,
        row ties and counts remain separate. Other global denominator,
        retained-defect, period/height and spectral producers retain
        their original scope. DESIGN_CHOICES_COMMON and full RecT/TSel
        for the other global arguments are not inferred from local gain.
        The seven additional GRH contracts remain explicit in the report
        and current register.

        Exact rings, embeddings, small-prime guards, earlier choices,
        measures, periods, row spaces and comparison maps remain in
        scope. Conditional implications do not produce their retained
        inputs. No Lean build or kernel replay is claimed.
        """),
        "PROVENANCE, REVIEW AND DELIVERY",
        clean("""
        The delivery contains both TeX readers, this guide, the substantive
        TXT report and the full ZIP. Each new claim has source/proof
        ranges and hashes in its component provenance. Source snapshots,
        named foundations, independent reviews, validation records and
        repeatable scripts are included. Predecessor proof chapters and
        claim records are preserved; mutable v0.48 root metadata is
        retained in history/version_0_48. SHA256SUMS covers the distributed
        files.
        """),
    ]
    return "\n\n".join(sections).rstrip() + "\n"


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parent)
    parser.add_argument("--check", action="store_true", help="Check without writing")
    args = parser.parse_args()
    root = args.root.resolve()
    report, summary = build_report(root)
    readme = build_readme(root)
    if not args.check:
        destination = root / OUTPUT
        destination.write_text(report, encoding="utf-8")
        summary["sha256"] = sha256(destination)
        readme_path = root / "README.txt"
        readme_path.write_text(readme, encoding="utf-8")
        summary["readme_sha256"] = sha256(readme_path)
    summary["written"] = not args.check
    print(json.dumps(summary, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
