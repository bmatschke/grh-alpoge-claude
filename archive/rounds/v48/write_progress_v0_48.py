#!/usr/bin/env python3
"""Generate the substantive v0.48 progress report and current README.txt.

All inventory and closure figures come from the frozen integrated v0.48
records. This script does not integrate, alter a proof or change a ledger.
Use --check to validate the same inputs without writing the two TXT files.
"""
from __future__ import annotations

import argparse
from collections import Counter
from datetime import date
import hashlib
import json
from pathlib import Path
import textwrap

VERSION = "0.48"
PIN = "7cbf7a0c32fca1badf05931879a37c3f8a2b03b4"
OUTPUT = "RH_reconstruction_progress_v0_48.txt"


CHAPTERS = [
    (
        "one_character_v48", "OCH", 30,
        "ONE CHARACTER: THE COMPLETE ORIGINAL TRACE AND LENGTH IMPLICATION",
        """
The principal whole-contract advance is TASK_ONE_CHAR_PROOF. The chapter
proves the original implication

       InpZ and AutomorphyUnramifiedCoefficients imply OneChar.

InpZ was assembled in KIZ2. The separate automorphy premise still supplies
one marked element g1 with three properties of the same deformation
problem: finite weight-zero entry algebra FinA, rank-three automorphy AutB,
and the universal rank-two extension-modularity statement LemW. The proof
does not independently choose these three witnesses or infer their
producer from the implication. Every original coefficient datum, fixed
embedding iota, conductor, exponent and GD guard is retained. [OCH28–OCH30]

A substantial part of the proof constructs the local crystalline component
itself. Positive filtered representations have exact finite-cocycle
comparison. At cyclotomic weight one, the possible nonfinite direction is
annihilated by the actual difference between the Frobenius character and
the cyclotomic character; at larger positive weights it vanishes. This
gives triangular lifts over all finite Artin coefficient algebras, followed
by ordinary conjugacy. Artin–Rees thickening and a truncated unramified
twist prove both directions of the saturated ordinary-ideal comparison,
including the critical e=1 case. [OCH1–OCH6]

The resulting ideal is the original It. Its completed local chart has
twelve variables, with multiplicities (1,2,3,4,2) in matrix weights
(-2,-1,0,1,2). The proof retains integral contraction, the specified base
point and all-target conjugation stability. It then constructs the actual
normalized global ring and graded model. The relative equation counts and
all eight normalization equations remain exact. FinA makes the quotient
weight-zero module finite; finiteness of the ambient weight-zero ring is
not asserted. Torus rescaling produces actual local points from every
graded point, and every relevant derivation has the required actual and
integral lift. [OCH7–OCH14]

No continuity condition is silently added to the source's algebra maps.
Strict localness bounds the first coordinate values and implies adic
continuity. For an arbitrary map to dual numbers, extend coefficients
finitely to contain those small values. Formal Taylor division modulo
the square of the coordinate-difference ideal expresses every series by
its constant and linear terms. The map is therefore determined by finitely
many second-coordinate values and is continuous in a finite coefficient
algebra. This allows the local period argument to apply to all actual
first-order deformations quantified in PtHyp. [OCH13, OCH15, OCH20]

The marked matrix difference has eigenvalues zeta,0,-zeta, with zeta a
unit in the strict residual sense. Its projectors force any invariant
subspace to be a coordinate subspace. A two-sided point is consequently
either irreducible over the quadratic field, or an irreducible outer
two-dimensional block plus the middle line. An intertwiner is diagonal
and gives exactly conjugation by T(t)=diag(t,1,t^(-1)), including the
outer-block square-root case. Type-I irreducibility persists on the full
infinite cyclotomic kernel: an abelian-quotient self-twist would contradict
the actual infinite inertia character. [OCH16–OCH18]

The earlier matched adjoint theorem and full Type-II rigidity supply all
three PtHyp fields on this same ring. The polarization twist is
epsilon^(-1), with multiplier epsilon^(-2). Every two-sided point gives
the original Adm3 representation or the original Adm2 representation with
the exact conductor allowance N|disc K|. The latter is a rank-two block
plus a line; the resulting rank-three representation need not be
irreducible. [OCH19–OCH22]

For the lower bound, put alpha=Psi^(-1). Each torsion Selmer class has the
canonical representative

 nu[z](g) = z(g) - (alpha(g)-1)(alpha(g1)-1)^(-1)z(g1).

The unit at g1 makes this well-defined and injective on classes. A class
killed by b has a representative and the needed local primitive already
killed by b. Multiplication by E10-E21 embeds it into the actual normalized
matrix-cocycle space. The square-zero representation (1+epsilon*gamma)r0
then gives the required point derivation and integral lift. The generic
additive-injection lemma bounds every torsion layer; taking their directed
union gives Vlen <= model length before finiteness is known. [OCH23–OCH25]

All five geometric length hypotheses hold for one model and one trace
element. The upper-bound theorem is reapplied to the final irredundant
cover; summands are not simply deleted from an earlier estimate. This
produces a finite isomorphism-irredundant set X of actual admissible
representations and the original inequality

       Vn <= 2 sum_(rho in X) v_ell(tr rho(sigma) - t),
       t = Psi(sigma) + 1 + Psi(sigma)^(-1).

The generic valuation is e_O*v_ell, where e_O=v_O(ell), so dividing the
model length by e_O gives exactly the printed normalization. The finite
upper bound proves finiteness before a natural-number length is taken.
Same-valued roots of unity place the character in an unramified coefficient
ring; RV7 returns the same X and normalized Vn to the supplied original
ring. The original GD conditions, including small-prime restrictions they
already imply, remain unchanged. AUT_UNRAM_COEF remains the outstanding
separate automorphy producer. [OCH26–OCH30]
""",
    ),
    (
        "principal_uniformization_v48", "PUN", 24,
        "PRINCIPAL UNIFORMIZATION: EXACT ARITHMETIC MODELS AND ACTUAL MODULI POINTS",
        """
This chapter supplies substantial original constructors for the principal
chart. It retains the same CM host, Hermitian space, perfect integral
alternating lattice and level. It also constructs individual marked
moduli points. The finite holomorphic family and its simultaneous
normalized theta frames remain to be assembled; no whole principal-chart
closure is claimed. [PUN1–PUN24]

The quadratic norm theorem is deduced from Hasse–Minkowski by applying it
to U^2-delta V^2-xW^2. If delta is not a square, a nonzero global isotropic
vector must have W nonzero and gives the desired norm solution. A direct
induction then proves Hermitian local-to-global isometry. It handles an
isotropic vector by making a hyperbolic pair and handles split local
quadratic algebras by dual bases. Thus no additional Hermitian
local-to-global theorem is inserted as an assumption. [PUN1–PUN2]

The original positive complex structure determines the exact Hermitian
signature. At finite places, perfection of the integral alternating trace
pairing identifies the lattice with its dual for the same fractional
ideal xi^(-1)D^(-1). The host's unramified quadratic extension makes that
ideal a common scalar ideal locally. Unimodular Hermitian diagonalization
then puts both lattices in the same local space, including dyadic places.
The global isometry embeds every component datum of the same signature
in the prescribed original space. Globally projective lattices are retained;
there is no assumption that they are free over the integer ring. [PUN3–PUN5]

The half-level condition is proved equivalent to the full congruence
condition, with modulus lcm(M,A). Finite index uses the original order
of cosets. Freeness on the full flag domain and one transvection modulus
are established before all later isotropic integral vectors, real integral
scalars and either sign. These give every LatModel field and the complete
ModelsOf/ModelBase/NegXi constructor for a supplied FamilyUnif, on the
same fixed matrix and scalar. Supplying a family and constructing its
arithmetic models remain distinct tasks. [PUN6–PUN11]

The cusp-center argument constructs the actual zGam, rather than a
commensurable substitute. Polynomial central coordinates give its faithful
additive action. Exact congruences show finite generation and full rational
span, so LatZ holds for every original family and every cusp rank, with
rank |Psi|*rho^2. Periods are then constructed for every ordered original
type. The coefficient ideal calculation uses a fractional-ideal
pseudobasis and the original XcFD lattice. [PUN12–PUN17]

The Fourier phase retains its factor of one-half. For the original
kappa0=+/-2xi0 it is one-half, up to sign, of the rational trace. The host
element w0 satisfies w0+bar(w0)=1. For conjugation-fixed u in the inverse
different,

                  (1/2)Tr(u) = Tr(w0*u) is an integer.

This identity supplies the integral converse without dividing by two in
the integer ring. The resulting ExpoMatch is the whole original A=1
statement for every cusp, rank and basis, on the exact coefficient lattice
and modulus M. No ideal principalization or saturation replaces the
required equality. [PUN18–PUN19]

From an original period P, the quotient C^g/P(L) receives the canonical
semicharacter alpha(Pa)=exp(pi*i*B(a,w0*a)). The explicit
Appell–Humbert factors produce the actual primitive, rigidified, symmetric
cubical line. The named Riemann algebraicity, Appell–Humbert, GAGA and
Poincare/Picard foundations supply their classical conclusions; the
primitive identity and adjoint action are checked for this object.
Perfection makes its polarization an isomorphism, so KTriv holds over
every C-algebra, including nonreduced algebras. [PUN20]

The theta commutator is computed in the source's multiplication order,
giving exp(-2*pi*i*B(a,b)/n), with its negative sign. All positive torsion
levels, their tower compatibility and both level markings are preserved.
These are algebraic identities, so the geometric clause works over every
algebraically closed field and every C-to-k embedding, with no continuity
assumption on that embedding. The supplied Moduli representing property
then yields an actual marked point. [PUN21–PUN22]

Two such points are equal exactly when an integral marked isometry and
a complex-linear period equivalence satisfy the original half/full level
congruences. The primitive line itself, not only its polarization class,
is recovered. Local unit norms also construct an actual marked genus at
each prescribed base embedding, hence nonemptiness in positive rank.
The representing Moduli scheme is retained as supplied. Reverse extraction
at arbitrary moduli points, local period lifts, holomorphic dependence,
the finite N1c family and normalized frames still remain. [PUN23–PUN24]
""",
    ),
    (
        "adelic_measures_v48", "AMD", 17,
        "ADELIC MEASURES: THE WHOLE MEASURED BLOCK AND SIMULTANEOUS NORMALIZATIONS",
        """
AMD removes the measured-block constructor from the remaining adelic
setting work. It proves the full original adelic isomorphism, constructs
all measures in MGExists and MWCore, and obtains MExists with every
same-bridge MeasTie equality. It further makes unipotent covolume one
compatible with prescribed infinity, global-H and local-S measures.
The normalized nonzero Bessel block and later orbital/fiber comparisons
remain separate producers. [AMD1–AMD17]

The bridge is built from the actual tensor splitting and original
archimedean coordinate matrices. Its finite map is continuous for exactly
the source's principal-congruence topology. Rational points are sent to
the same rational matrices, and the compact-subgroup correspondence keeps
the original local lattice and archimedean majorant conditions. The
coordinate equations characterize the bridge, so the conclusions hold
for every supplied witness rather than only a convenient choice.
Empty matrices and rank zero remain within scope. [AMD1–AMD3]

For every original standard frame the exact flag stabilizer decomposes
as S=N semidirect H, where H is the unitary group of the remaining
orthogonal space. The proof uses the generic Nsub definition, testing
all vectors of the perpendicular quotient; it does not replace it by a
smaller convenient subgroup. All groups are closed and locally compact,
and no definiteness premise is added to the standard frame. Explicit
nilpotent Lie coordinates give the H-action determinant

                       Norm_E/F(det h)^(-r) = 1.

Thus H preserves Haar measure on N at finite and infinite places and
on the restricted product. The product pushforward mu_S=mult_*(mu_N x mu_H)
is literally Haar, with no unnamed scalar adjustment. [AMD4–AMD7]

The source's weak Haar predicate assumes only nonzero measure,
sigma-finiteness, support on the subgroup and left invariance. AMD proves
these conditions sufficient on the actual unimodular groups. Tonelli
applied in two orders gives

                    lambda(A)*nu(B) = lambda(B)*nu(A).

A set of finite positive nu-measure and a compact set of finite positive
Haar measure force the comparison scalar to be finite and positive.
Consequently the supplied weak measures are genuine Haar measures.
Their exact pushforwards supply InfTransfer without adding local
finiteness as a new hypothesis. [AMD8–AMD9]

MGExists chooses all five group-measure entries, including arbitrary
degenerate tuple stabilizers, and preserves its three specified original
measure ties. MWCore constructs all eight frame-measure entries and
eleven normalization clauses. MExists then uses one bridge before every
word, the actual coordinate frame and both supplied infinity measures.
All five MeasTie equalities follow literally. The Bessel block appearing
among the original antecedents is taken as supplied; its independent
existence is not required to prove this measured-block implication.
[AMD10–AMD12]

If a global Haar measure and its infinite factor are both prescribed,
Haar uniqueness allows the sole positive scalar to be absorbed into the
finite factor. Applying this separately to N and H preserves the two
infinity measures, both global measures and the entire local-S family.
For N, a central flag of its rational nilpotent Lie algebra reduces
adelic cocompactness to the additive Chinese remainder construction.
The resulting compact representative set gives a Borel fundamental
domain of finite positive measure. All measurable fundamental domains
have that same measure, including the source's almost-everywhere version,
so rescaling gives exactly its covolume value one. [AMD13–AMD16]

These constructions coexist on one MeasW and preserve the fixed infinity
ties at every word. Together with ASG18's eight earlier blocks, AMD12
leaves only the original Bessel W block among the setting blocks.
The full Siegel–Weil rescaling still needs compatible orbital/stabilizer
measures and normalized local fiber identities. Existence of Haar
measures and unipotent covolume one does not itself prove those
identities or the Bessel decay/nonvanishing assertions. [AMD17]
""",
    ),
    (
        "common_compatibility_v48", "GCF", 18,
        "COMMON COMPATIBILITY: ACTUAL COLUMN STAGES, PERIODS AND DIVISION TRANSPORT",
        """
GCF constructs the original true-volume column-stage endpoint: one GJStage
with full GIs2, chosen before every later W,V,S,N. On the actual recursive
record it supplies every one of the five GroupCompatibilityAll fields
and the complete dependent IsRecG equality. It also proves exact
comparison-map preservation under every original division choice. These
results reduce the global local-gain task to realization of the selected
common family, with its remaining rows, kernel/theta, divisor, object and
gauge fields. They do not assert that an arbitrary given family's
comparison already equals the constructed one. [GCF12–GCF18]

The first step constructs finite-adelic Hilbert–90 lifts and the canonical
scalar determinant map. Its kernel is the exact open subgroup required
by the original selected-prime congruences. The quotient criterion uses
balanced conjugate valuations and the principal-unit condition at those
selected primes. Arbitrary generic data with extra primes are not silently
substituted. Rational local generators absorb fixed finite ideles by
approximation, giving every original lift and scalar law. [GCF1–GCF3]

The same decorated points and their rational and residue frames then
give the point determinant identity. Endpoint, intermediate and terminal
column determinants are all read on those actual representatives. The
relative determinant law works in every rank and for globally nonfree
lattices, using local bases and the original positive-part valuation
convention. An already given local-tie family is preserved in the full
Hermitian-column construction. Thus the proof does not join separate
existence statements with incompatible choices. [GCF4–GCF6]

The period-field argument uses the actual CM elliptic torsion. A field
automorphism fixing the squared and cubed invariants can only introduce
a sixth-root ambiguity. The distinguished two-torsion point removes its
sign part. A suitable pair of three-torsion abscissae and their quartic
identity reduce the remaining ambiguity to a cube root. The original
Base already contains the required third roots of unity. Consequently
the given discriminant root, rather than a newly chosen root in an
extension, has complete DataIn over the same coefficient field. Field
automorphisms are applied only to algebraic torsion identities, never
to analytic limits. [GCF7–GCF10]

This proves all OmegaCompatible fields with the original different-ideal
generator and exact normalization

                    Omega = (pi*|rho*d|^2/area)^(-1).

Conjugate periods and the true lattice differ only by the allowed
twelfth-root homothety, preserving their area. The identity holds at
every complex embedding and every later stage. The original true-volume
foundation is used through the already reconstructed GV19; no new
volume theorem is silently asserted. [GCF11, GCF14]

The recursive local models, coefficient rings and comparison maps are
then constructed together. All four ring isomorphisms and five commuting
equations are actual maps. The rank formulas and normalized valuations
give the original numerical record with Ce=1. Uniqueness of the
evaluation polynomial transports the same forms and comparison to
every later stage over the fixed initial data. GCF14 combines these
with the original local, period and volume ties to prove the literal
exists_trueVolume_stage_of_any_column_choice and its pinned
exists_GJStage_GIs2 specialization. [GCF12–GCF14]

For arbitrary submodules and real heights, setDiv leaves the relevant
comparison hypotheses unchanged. The unique evaluation polynomial
therefore gives equality of the actual comparison maps, including their
values outside lattice tuples. The complete IsRecG, ColT and
ColumnDataSplitPrimes records transport through the division. This is
stronger than an isomorphism between their images and is needed to
identify the eventual supplied Extra.cmp. [GCF15–GCF16]

Within the original selected D3 class, ChosenE already supplies the
selected tops on the same subset. The existing GLG argument gives Adm2F
with the unchanged threshold

          max(x_a,x_b,Fm.x1+1,(16*C_b+2)^(3/epsilon)).

Thus the selected-class top supplier is no longer an independent task.
For an arbitrary family outside D3 it remains an antecedent. The final
class-level LinkG consumer still requires the original eventual WPt/TSel
realization, with joint (D,O) equality and one dependent
(Gt,cmp,tw,ker) equality. Both Closed-class premises and all earlier
threshold choices are retained. Once that realization is supplied,
LGS13 provides all five original LinkG fields with its unchanged
constants; it does not follow merely from the completed column stage.
GLOBAL_LOCAL_GAIN therefore remains open. [GCF17–GCF18]
""",
    ),
]


NEXT_PRODUCERS = """
THE NEXT ORIGINAL PRODUCERS

1. Supply AUT_UNRAM_COEF. OneChar's local geometry, arithmetic model,
rigidity and trace/length argument are now written. The next arithmetic
task is the original AutomorphyUnramifiedCoefficients producer: one
marked g1 must jointly give FinA, AutB and the universal LemW for the
same unramified coefficient problem and fixed iota. The completed InpZ,
rank-three congruence integer and PropGK finite consumer remain reusable.
None supplies that automorphy premise by circularly using OneChar.

2. Finish the common principal chart. The exact source target remains
FrameUnif.exists_unf_hasPrinc in CongrOfDvdModulus.lean. PUN now supplies
the norm theorem, models for a supplied family, all-rank LatZ, the A=1
exponent dictionary and actual individual marked moduli points. Continue
with reverse uniformization at arbitrary moduli points, prescribed local
period lifts, holomorphic dependence of moduli and exponentials, and
the simultaneous theta-frame family. Assemble N1c, then the exact
FramesOK/CoverTri/FibTri and IsUnf/FromTest dictionary on the same points.
The original coefficient field, Gaussian norm, phases and both levels
must remain common. Integral cusp spanning, higher covers and all-tuple
class sums still need their listed analytic and geometric producers.

3. Finish the adelic Bessel and row setting. AMD supplies the measured
block and all its same-bridge ties. The remaining setting block is the
normalized nonzero Bessel W, with its original local model, uniqueness
and decay properties. Continue the compatible orbital/stabilizer and
local fiber normalizations under the original Siegel–Weil foundation,
then the Witt/genus/level/representation transport to arithmetic columns.
The actual AutTie, RowDictTie and LabTie and the cylinder counts must
concern one AllRows object and one simultaneous threshold. Earlier row
finiteness and finite local character estimates remain available.

4. Realize the compatible selected common family. GCF gives the actual
GIs2 stage and preserves its comparison under arbitrary setDiv; D3 gives
its selected TopsF/Adm2F. The next task is the full eventual WPt/TSel
realization and its dependent equalities. The remaining Wit fields are
rows, kernel/theta, divisor, object and gauge data on the same earlier
choices. The independent global denominator, retained-defect,
period/height, normalized spectral and second-layer selection producers
retain their full quantitative scopes and common-family requirements.

5. Continue the remaining shared arithmetic and case suppliers. Preserve
the F3 coefficient bridges and F4 common-overfield reading, the entire
coefficient field and exact valuation/norm/GoodCoef data, the complex
Hecke standard and character data, base rows, host/frame lengths and
nonzero chains. Group ties, support, carriers, parts, all-embedding
period readings, HD/d3b and NEb remain at their registered scopes.
The second DivRows3 requirement and the remaining RH case installations
are distinct from already completed first divisibility and Hida support.

These are parallel starting points with precise interfaces. A later
assembly must use the same fields, embeddings, measures, row spaces,
comparison maps and earlier thresholds. The final remaining-leaf register
is authoritative for whole selected contracts; the chapter boundaries
record which internal producers have now been removed.
"""

READING_AND_CHECKS = """
READING, FOUNDATIONS AND REPRODUCIBILITY

RH_new_proofs_v0_48.tex collects the four new chapters with the current
audit. RH_readable_reconstruction_v0_48.tex is the cumulative reader.
The complete delivery pairs these TeX readers with this substantive TXT
report and the full ZIP. Each component records its human proofs, exact
source contracts, source/proof ranges and hashes, retained foundations,
repeatable builder and validation. Independent mathematical reviews are
bound to the reviewed text; integration and semantic reviews check the
assembled inventory and scope.

Published foundations remain explicitly named inputs. Their applications
must match the actual objects and normalizations; a source hash is not
a substitute for that argument. New numbered deductions, external
foundations and original open antecedents are separately recorded. The
accepted source pin is unchanged, and no Lean build or kernel replay is
performed. The complete human proof of RH and unrestricted Dirichlet GRH
still requires the remaining original producers.
"""


def read_json(root: Path, relative: str):
    return json.loads((root / relative).read_text(encoding="utf-8"))


def clean(text: str) -> str:
    return textwrap.dedent(text).strip()


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def build_report(root: Path) -> tuple[str, dict]:
    cfg = read_json(root, "increment_v0_48.json")
    stats = read_json(root, "integration_stats_v0_48.json")
    graph = read_json(root, "dependency_audit_v0_48/obligation_map.json")
    register = read_json(root, "dependency_audit_v0_48/remaining_leaf_register.json")
    assert cfg["artifact_version"] == graph["artifact_version"] == VERSION
    assert register["artifact_version"] == VERSION
    assert cfg["source_commit"] == graph["source_commit"] == PIN
    assert set(cfg["closed_selected_leaves"]) == {"TASK_ONE_CHAR_PROOF"}
    assert set(cfg["components"]) == {item[0] for item in CHAPTERS}

    all_claims = []
    chapter_rows = []
    for component, prefix, expected_count, title, body in CHAPTERS:
        ledger = read_json(root, component + "/provenance.json")
        claims = ledger["claims"]
        assert [claim["id"] for claim in claims] == [
            prefix + str(i) for i in range(1, expected_count + 1)
        ], component
        assert ledger["source_commit"] == PIN
        all_claims.extend(claims)
        chapter_rows.append(
            f"{prefix}1–{prefix}{expected_count}: {len(claims)} claims; {component}/main.tex"
        )
    classes = Counter(claim["classification"] for claim in all_claims)
    assert len(all_claims) == stats["new_claims"]

    nodes = {node["id"]: node for node in graph["nodes"]}
    assert len(nodes) == stats["selected_nodes"]
    assert sum(len(node["requires"]) for node in nodes.values()) == stats["selected_edges"]
    records = register["records"]
    open_ids = {record["id"] for record in records}
    open_classes = Counter(record["category"] for record in records)
    assert len(open_ids) == len(records) == stats["open_count"]
    assert dict(open_classes) == stats["open_categories"]

    def reachable(start: str) -> set[str]:
        seen = set()
        todo = [start]
        while todo:
            node_id = todo.pop()
            if node_id not in seen:
                seen.add(node_id)
                todo.extend(nodes[node_id]["requires"])
        return seen

    rh = reachable("ORDINARY_RH")
    grh = reachable("DIRICHLET_GRH")
    extra = sorted((grh - rh) & open_ids)
    assert len(open_ids & rh & grh) == stats["shared_open"]
    assert len(extra) == stats["extra_grh_open"]
    day = date.fromisoformat(cfg["date"]).strftime("%d %B %Y").lstrip("0")
    paragraphs = [
        "RH AND UNRESTRICTED DIRICHLET GRH — HUMAN RECONSTRUCTION v0.48",
        day + "\nAccepted source commit: " + PIN,
        "CURRENT RESULT",
        clean("""
        Version 0.48 completes TASK_ONE_CHAR_PROOF, the full original
        OneChar implication with its separate unramified-coefficient
        automorphy premise retained. Three further chapters construct
        original principal-uniformization suppliers and actual individual
        moduli points, the complete adelic measured block and simultaneous
        measure normalizations, and the true-volume column compatibility
        stage with exact period and division transport.

        The human-readable reconstruction remains incomplete. The closed
        implication does not establish AUT_UNRAM_COEF. The new geometric
        and adelic records do not yet construct every required common
        family. This report explains the actual mathematics, exact
        normalizations and the remaining original producers.
        """),
        "INTEGRATED INVENTORY",
        "\n".join([
            f"New human claims: {stats['new_claims']} "
            f"({', '.join(str(v) + ' ' + k for k, v in sorted(classes.items()))}).",
            f"Cumulative claims: {stats['cumulative_claims']}; "
            f"predecessor records retained: {stats['cumulative_claims'] - stats['new_claims']}.",
            f"Selected dependency graph: {stats['selected_nodes']} nodes and {stats['selected_edges']} edges.",
            f"Whole obligations still open: {stats['open_count']} "
            f"({open_classes['C']} C and {open_classes['B']} B).",
            f"Shared RH/Dirichlet-GRH obligations: {stats['shared_open']}; "
            f"additional Dirichlet-GRH obligations: {stats['extra_grh_open']}.",
            f"Increment source inventory: {stats['new_source_files_checked']} pinned files "
            f"and {stats['new_unique_source_ranges_checked']} distinct cited ranges.",
        ]),
        clean("""
        These figures come from the final v0.48 increment and integration
        statistics and are checked against every new claim and the final
        obligation graph/register. Class B denotes a written human proof
        at its stated scope. Named classical foundations are recorded
        separately. Counts describe the inventory, not a percentage of
        completion; a complete internal supplier need not close the larger
        selected contract that consumes it.
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
            f"{node_id} ({nodes[node_id]['category']}): {nodes[node_id]['contract']}"
            for node_id in extra
        ),
        clean("""
        These retain the original tensor-factor, seed, residual-chain and
        image/automorphy conditions. Seed choices and the fixed embedding
        precede the later towers. The rank-four propagation keeps its
        original residual point and depth bound. The new rank-three
        OneChar implication does not identify or close these additional
        contracts.
        """),
        clean(READING_AND_CHECKS),
        "REPORT INPUT BINDINGS\n"
        + "increment_v0_48.json SHA256: " + sha256(root / "increment_v0_48.json")
        + "\nintegration_stats_v0_48.json SHA256: "
        + sha256(root / "integration_stats_v0_48.json"),
    ])
    report = "\n\n".join(paragraphs).rstrip() + "\n"
    words = len(report.split())
    if not 3000 <= words <= 4500:
        raise ValueError(f"Progress report has {words} words; expected 3000–4500")
    summary = {
        "artifact_version": VERSION,
        "output": OUTPUT,
        "words": words,
        "new_claims": stats["new_claims"],
        "cumulative_claims": stats["cumulative_claims"],
        "whole_closures": sorted(cfg["closed_selected_leaves"]),
        "remaining_whole": stats["open_count"],
        "extra_grh": len(extra),
    }
    return report, summary


def build_readme(root: Path) -> str:
    stats = read_json(root, "integration_stats_v0_48.json")
    cfg = read_json(root, "increment_v0_48.json")
    day = date.fromisoformat(cfg["date"]).strftime("%d %B %Y").lstrip("0")
    sections = [
        "RH AND UNRESTRICTED DIRICHLET GRH — HUMAN RECONSTRUCTION v0.48",
        day + "\nAccepted source commit: " + PIN,
        "CURRENT RESULT",
        clean("""
        Partial human reconstruction, accepting the pinned Alpoge-Claude
        formal source as fully checked and correct. Version 0.48 completes
        the selected TASK_ONE_CHAR_PROOF: InpZ together with the original
        AutomorphyUnramifiedCoefficients implies OneChar. AUT_UNRAM_COEF
        remains a separate producer. The complete human proof of RH and
        unrestricted Dirichlet GRH is still unfinished.
        """),
        f"There are {stats['new_claims']} new claims and "
        f"{stats['cumulative_claims']} cumulative claims. The selected graph retains "
        f"{stats['selected_nodes']} nodes and {stats['selected_edges']} edges. "
        f"The {stats['open_count']} remaining whole obligations comprise "
        f"{stats['open_categories']['C']} C and {stats['open_categories']['B']} B; "
        f"{stats['shared_open']} are shared RH/GRH obligations and "
        f"{stats['extra_grh_open']} are additional Dirichlet-GRH obligations. "
        f"This increment cites {stats['new_source_files_checked']} pinned source files "
        f"in {stats['new_unique_source_ranges_checked']} distinct ranges. "
        "Claim counts are an inventory, not a completion percentage.",
        "READING ORDER",
        clean("""
        1. RH_reconstruction_progress_v0_48.txt: substantive mathematics,
           exact endpoints, retained hypotheses and next producers.
        2. RH_new_proofs_v0_48.tex: the current audit and four new chapters.
        3. RH_readable_reconstruction_v0_48.tex: the cumulative manuscript.
        4. RH_dependency_audit_v0_48.txt: the remaining selected contracts.
        5. continuation_checkpoint.json, next_source_targets.json,
           provenance.json and dependency_audit_v0_48/: exact continuation
           and dependency records.
        """),
        "FOUR NEW CHAPTERS",
        "\n".join(
            f"{component}/main.tex — {prefix}1–{prefix}{count}: {title}."
            for component, prefix, count, title, _ in CHAPTERS
        ),
        clean("""
        OCH proves the actual local crystalline component, graded model,
        point rigidity, normalized Selmer injection and exact trace bound.
        Its finite representation set is isomorphism-irredundant; the Adm2
        branch need not be irreducible in rank three. PUN constructs exact
        same-space arithmetic models, all-rank cusp-center lattices, the
        A=1 Fourier exponent match and individual primitive moduli points,
        retaining the supplied Moduli scheme. AMD constructs the full
        measured block, all same-bridge ties and compatible prescribed
        measures with unipotent covolume one. GCF supplies full GIs2 before
        all later choices, actual periods and comparison-preserving
        division transport; selected D3 also supplies TopsF/Adm2F.
        """),
        "REMAINING SCOPE",
        clean("""
        The next arithmetic task is AUT_UNRAM_COEF with one marked element
        supplying FinA, AutB and universal LemW. Geometry still needs the
        finite holomorphic N1c family, simultaneous normalized frames and
        full principal-chart dictionary. The adelic setting still needs
        the normalized nonzero Bessel block, orbital/fiber comparisons and
        arithmetic transport and row ties/counts. Global local gain still
        needs the selected common-family WPt/TSel realization with its
        joint dependent equalities; denominator, retained-defect,
        period/height, spectral and second-layer producers retain their
        original scopes. The seven additional GRH contracts are explicit
        in the progress report and final register.

        Exact coefficient rings and embeddings, original small-prime
        guards, data chosen before later choices, measure and period
        normalizations, same row spaces and actual comparison maps remain
        in scope. Conditional implications do not establish their retained
        inputs. No Lean build or kernel replay is claimed.
        """),
        "PROVENANCE, REVIEW AND DELIVERY",
        clean("""
        The delivery contains both TeX readers, this guide, the substantive
        TXT report and the full ZIP. Every new claim has source/proof
        ranges and hashes in its component provenance. Source snapshots,
        named foundations, independent mathematical/integration/semantic
        reviews, validation records and repeatable scripts are included.
        Predecessor proof chapters and claim records are preserved; mutable
        v0.47 root metadata is retained in history/version_0_47.
        SHA256SUMS covers the distributed files.
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
