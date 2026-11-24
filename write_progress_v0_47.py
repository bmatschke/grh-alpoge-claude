#!/usr/bin/env python3
"""Generate the substantive v0.47 progress report from integrated inventories.

This writes RH_reconstruction_progress_v0_47.txt and the root README.txt.
It does not run an integration, change a proof, or modify a shared ledger
or reader.  --check performs the same checks without writing either TXT.
"""

from __future__ import annotations

import argparse
from collections import Counter
from datetime import date
import hashlib
import json
from pathlib import Path
import textwrap


VERSION = "0.47"
PIN = "7cbf7a0c32fca1badf05931879a37c3f8a2b03b4"
OUTPUT = "RH_reconstruction_progress_v0_47.txt"


CHAPTERS = [
    (
        "type_ii_rigidity_v47", "KTR", 13,
        "TYPE-II RIGIDITY: THE ACTUAL NINE-DIMENSIONAL ADJOINT",
        """
The first closed obligation is the original RigII theorem. It starts with
an actual marked rank-three deformation point over the original coefficient
ring. Its TypeII condition separates a two-dimensional corner from a middle
line over the imaginary quadratic field K. The conclusion is vanishing of
every allowed Selmer cocycle in the full nine-dimensional polarized adjoint.
The original antecedent that every specified rank-two extension is modular
for the fixed embedding iota remains part of this theorem. [KTR4–KTR13]

The local argument extracts exactly what this application needs from the
point's defining ideal. The ordered ordinary ideal lies inside It. Its
matrix-product identities, evaluated against an inertia element with three
distinct eigenvalues, force the ordered characters

                 (epsilon^e, 1, epsilon^(-e)).

Normality then extends preservation of the ordered flag to full inertia.
Residual closeness, the original condition ell−1 not dividing 2e, the
prime-to-ell finite inertial image away from ell, and the class-number
condition prove that the middle character and corner determinant are one
over K. The calculation treats conjugate places using the actual
inverse-transpose action. [KTR4–KTR5]

This gives an explicit extension W to the rational Galois group, with
determinant the quadratic character eta and W(c)=diag(−1,1). Its restriction
to the full infinite cyclotomic kernel is irreducible. The proof reduces a
hypothetical failure to a quadratic self-twist, then contradicts it using
the infinite ordered inertia character. No finite cyclotomic layer replaces
that kernel. [KTR6–KTR8]

The modularity antecedent supplies the actual normalized newform of weight
k=2e+1. Kato's Theorem 14.2(1) applies at twist r=e: 1≤e≤k−1 and 2e≠k.
The paper's inverse-arithmetic-Frobenius polynomial identifies W with
V(f)(e), using the same iota. The proof matches the Bcris kernel at ell
and unramified local conditions elsewhere, and passes from finite discrete
Selmer groups to rational cocycle vanishing. Finite-character descent gives
the needed vanishing for W and W eta. The published application imposes no
new lower bound on the coefficient prime. [KTR1–KTR3]

Quadratic GL2 base change is applied to this same newform. Corner
irreducibility excludes the induced exception. The normalized Satake
comparison includes inert places, and an explicit symmetric pairing gives
the exact polarized corner adjoint required by the previously matched
Thorne theorem. Concrete projections and sections then yield

              ad(r) = A_4 direct-sum W direct-sum W eta
                                      direct-sum eta.

The dimensions are 4+2+2+1=9. The two off-diagonal sections have factor
1/2; the scalar line is retained. Applying the projections to a cocycle,
obtaining four primitives, and adding their images proves the literal
RigII conclusion. Kato, quadratic base change, the matched adjoint theorem
and the original cohomological foundations remain named inputs; their
representation-dependent applications are written out. [KTR9–KTR13]

Original endpoint: KatoTwoOfUseN.lean, RigII. The independent OneChar and
unramified-coefficient automorphy producers are not consequences of this closure.
""",
    ),
    (
        "kato_input_assembly_v47", "KIZ", 2,
        "THE COMPLETE COHOMOLOGICAL AND RANK-THREE INPUT RECORD",
        """
The second closed obligation is TASK_INP_Z_ASSEMBLY. KIZ constructs the
entire original CohInp/InpZ record by inserting already proved universal
statements into their exact fields. This matters because the later arithmetic
consumer must specialize all fields to one common choice of coefficient
ring, closure, number field, representation and embedding. Separate results
about unrelated chosen witnesses would not suffice. [KIZ1–KIZ2]

CohInp has five fields. The local field retains all seven original
assertions: finite local cohomology, duality and Euler characteristics both
for local fields and for the original decomposition groups, together with
the complete tied Bloch–Kato local statement. It includes the integral
annihilator directions on actual cocycles and cup products. Normalized
Poitou–Tate data are chosen before the finite place set and module; global
finite cohomology and Euler data retain their original prime-two scope.
The separate high-degree vanishing still has its original odd-prime guard.
[KIZ1, BX8, DX1]

The final CohInp field uses the uniform witness C_K=31 from KB8. Under
the source's root-of-unity guard, for every e≥1 it gives

 log |H^2(D,Z_ell(e+1))|
      ≤ exp((2e[L:Q])^31 log(2|disc L|)).

The exponent is fixed before L, ell and the remaining arithmetic datum.
The guard asks for an ell-th root when ell is odd and a fourth root when
ell=2. These distinctions are preserved. [KIZ1]

The six further InpZ fields are supplied by SP6 for LemmaM, SP1 for
LemmaMprime, FP8 for LemmaP, KTR13 for RigII, ADK6 for AdVanishK, and
RNC16 for the rank-three congruence integer. LemmaM keeps its quantifier
over every finite orbit cover; LemmaMprime keeps its merely additive
injection; LemmaP retains the actual universal framed ring and exact
weightwise generator and equation counts. These are the complete source
predicates, not numerical substitutes. [KIZ2]

The RNC integer is still chosen before every later coefficient prime,
embedding and admissible collection. All eleven record fields can therefore
be specialized to the same later objects. This closes the assembly contract
in KatoUse.lean and KatoTwoOfUseN.lean. Constructing the OneChar arithmetic
rings and points, proving its length estimate, and supplying their modularity
remain separate tasks.
""",
    ),
    (
        "row_finiteness_v47", "RFD", 9,
        "FINITE DIMENSIONALITY OF THE ORIGINAL AUTOMORPHIC ROW SPACE",
        """
RFD proves the full RowsFinDim statement on the original adelic quotient,
with its supplied Haar measures, fundamental domain and weak integral
operators. The finite test function e may be any locally constant function
supported in the original compact lattice stabilizer. The given infinity
unit vectors need not be smooth or compact-finite. [RFD1–RFD8]

Compactness first gives one finite cover on which e is constant. Intersecting
the corresponding open subgroups and taking a finite-index normal core
produces one compact open K_0 for which e is invariant on both sides.
This level is chosen from e alone. The fixed-level adelic quotient splits
into finitely many arithmetic real quotients, with the actual positive
measure factors. The matched Harish–Chandra finite-multiplicity theorem
therefore bounds the space of bounded intertwiners into this fixed-level
Hilbert space. Continuous spectrum in the ambient regular representation
does not obstruct that argument. [RFD1–RFD3, FV4–FV10]

Tensor the original infinity representations and unit vectors. If sigma
is the resulting irreducible representation, w its tensor unit vector,
and d the product of the original formal degrees, then

       m(g)=<w,sigma(g)w>,       phi(g)=d conjugate(m(g)).

The original four-vector Schur identity and integrability give, for the
integrated operator T in any unitary representation U,

              T*=T,       T^2=T,       T U(g) T=m(g)T.

Every v in ran(T) defines a bounded intertwiner by
A_v(sigma(g)w)=U(g)v. The compression identity proves that this prescription
is well-defined and has norm ||v||. Evaluation at w makes v↦A_v injective.
This supplies a direct bridge from the actual projector range to the finite
bounded-intertwiner space. [RFD4–RFD7]

The normalized K_0-average P_0 satisfies P_0 R_e=R_e=R_e P_0, while finite
and infinity convolution commute. Hence ran(R_e T) is contained in the
finite-dimensional range of T on K_0-fixed vectors. The weak operator
identities uniquely identify these operators with the source's HH range.
No idempotence of e or additional gap condition is introduced into
RowsFinDim. [RFD8]

RFD9 removes the separate finite-dimensionality premise from ARO18–ARO30.
Those row constructions still need their actual common setting, AutTie,
RowDictTie, LabTie and arithmetic counting hypotheses. The universal
finiteness theorem is a completed nested producer, while the whole retained
defect obligation remains open. Original endpoint: HaarTransversals/RowsDef.lean,
RowsFinDim.
""",
    ),
    (
        "adelic_setting_v47", "ASG", 18,
        "EIGHT ACTUAL BLOCKS OF THE COMMON ADELIC SETTING",
        """
ASG constructs eight dependent blocks of the original SG.HidaSetting
constructor on one original D: the unitary instance, integral lattice and
flags, finite additive character, reference frame, transport matrices,
automorphic bundle, finite representation block, and subgroup/quotient
measures. The original Forms0(D,u_0) is retained for its lattice construction,
and the original GapHyp is retained for its discrete-series bundle. The
construction keeps each preceding choice when forming the next block.
[ASG1–ASG18; SettingBlocks.lean]

The lattice argument is explicit. The original cmUnram residue condition
excludes ramified quadratic places and gives an integral trace-one element,
including at residue characteristic two. Forms0 supplies a norm-one vector
through its actual Gram factorization, then rescales it to cancel the norm
of the distinguished negative vector. This produces the extra isotropic
direction needed for a saturated isotropic module of rank s+1. Steinitz
decomposition installs the prescribed first s ideal factors and one final
fractional ideal. [ASG2, ASG5–ASG6]

An integral retraction supplies dual vectors. A triangular correction using
the trace-one element makes them mutually isotropic without dividing by two.
The proof keeps the conjugation on each ideal, including the final ideal
which need not be conjugation invariant. The retained s pairs split the
actual lattice orthogonally. [ASG7–ASG8]

The last hyperbolic plane supplies primitive vectors of every required
negative norm. Hilbert class field theory and Chebotarev choose a prime
ideal p with p*c=(alpha), coprime to its conjugate and the prescribed T.
An element w in p with w+conjugate(w)=1 gives

                 z=alpha*e+conjugate(−T*w/alpha)*f.

Pairing proves its norm is −T and that gamma*z integral forces gamma
integral. Thus all word vectors use the same lattice and common isotropic
frame. The localized generators and the stronger Lsub primitiveness verify
every original FixedHyp field. [ASG3–ASG4, ASG9]

The finite additive character has the exact negative finite-principal-parts
sign, so its rational product with the prescribed positive infinity factor
is one. Split local lattices construct the full source reference-frame and
transport targets. Their congruence interpretations keep positive moduli
and integral residue-span data. The actual character idempotent has its
original Haar-volume denominator and all seven admissibility fields.
[ASG10–ASG14]

The original gap and previously proved discrete-series decay give the full
automorphic bundle and its bounded weak integrals. The stabilizer's positive
complement supplies the finite representation block. Its exact integral
highest weight is alpha_i=nu_i−(k−1)/2+i, where nu is the original
Harish–Chandra parameter; half-integrality and interlacing verify integrality
and dominance. Subgroup Haar measures and the quotient measure satisfy
Weil's identity with the original ambient measure. [ASG15–ASG17]

ASG18 records the remaining boundary: the normalized nonzero Bessel-function
block W, measured-field block, Siegel–Weil rescaling and its measure/character
ties, Bessel uniqueness/local ties, arithmetic count, and common family
threshold are still required. The eight constructed blocks do not supply
those distinct objects.
""",
    ),
    (
        "canonical_cusp_connection_v47", "CNC", 16,
        "THE CANONICAL CUSP CONNECTION OVER EVERY COEFFICIENT ALGEBRA",
        """
CNC supplies the complete original IsNab connection on the supplied moduli
family, for every original coefficient algebra S. S may be nonreduced,
nonlocal or non-Noetherian. All calculations are formal and coefficientwise
in finite jet algebras. The construction does not require analytic
convergence in S. [CNC1–CNC16]

The original tangent eigenframes form the whole tangent basis: the embedding
matrix for an integral basis of O_E has nonzero discriminant, so its inverse
constructs the orthogonal coordinate idempotents after extension to the
coefficient field. Smooth-section formal coordinates then give compatible
jets with those exact tangent vectors. Properness and geometrically reduced
connected fibers imply universally that base functions are the only global
functions. A ratio of two normalized line isomorphisms is consequently one
as a function, even over a nonreduced base. This proves the normalized
biextension identities on the actual line bundles. [CNC1–CNC6]

The central formal calculation is written in full. Over a rational algebra,
the invariant one-form J(x)^(-1)dx has a coefficientwise radial primitive
giving the formal logarithm. A normalized symmetric additive two-cocycle
c(x,z) is a coboundary. With b_i(x)=partial_(z_i)c(x,0), one explicit
primitive is

                 h(x)=−integral_0^1 sum_i x_i b_i(t*x) dt.

Here integration just divides each coefficient of t^m by m+1. The same
formula works with formal parameters and over rings with nilpotents.
[CNC7–CNC8]

Two such corrections kill the two partial cocycles. The remaining adjoint
cocycles form a derivation with values in a matrix bimodule. The separability
element of O_E tensor Q makes this derivation inner and supplies one
bilinear correction simultaneously for every original adjoint action. A
final antisymmetric half correction kills the symmetry defect while
preserving the earlier identities. This proves the full generic CanonGaugeSt,
including its involution and sign conventions. [CNC9–CNC12]

Compatible normalized line generators give a unique formal germ f for every
original section. One chart is chosen before all degrees and sections at a
framed point. The connection is exactly the source constant-coefficient rule

              nabla_y(k,F)(alpha)
                = [D^alpha(f(x)*exp(k*h(x,[w_0]x)))]_(x=0),

with the original invariant differential operators. Uniqueness proves the
required equality for every valid germ. Negative degrees, unconstrained by
IsNab, receive the defined zero value. [CNC13–CNC15]

CNC16 removes the connection-existence premise from both Boolean-level
instances of ICL. The two geometric foundations are separately matched to
Stacks tags 05D9 and 0E0L. Principal analytic charts, integral valuation
bounds, finite theta systems and the remaining spanning producers stay
separate. Original endpoint: FormalGroupCharts/ExistsIsNabUncond.lean.
""",
    ),
    (
        "principal_cusp_lattices_v47", "PCL", 12,
        "THE EXACT PRINCIPAL CUSP LATTICE AND DENOMINATORS",
        """
PCL supplies the lattice and normalization subproducer on each original
supplied principal chart. It constructs the full DataX extension of that
chart's Data, retaining its field, Hermitian matrix, scalar, group,
modulus and metrics. The original IsUnf, HasPrinc/GamAt and LawsCore
premises remain explicit. [PCL1–PCL12]

The source convention here is h_G(x,y)=x^t G conjugate(y), linear in the
first variable, and B_(xi,G)=Tr_(E/Q)(−xi*h_G). The perfect alternating
Datum and its adjoint O_E-action determine a Hermitian form by the
nondegenerate trace pairing. This constructs the coordinate injection of
the actual lattice, with its original sign; no free O_E-basis of the
lattice is assumed. [PCL1]

For a fractional ideal a and Hermitian dual L#, direct ideal calculations
give (aL)#=conjugate(a)^(-1)L#. The trace dual satisfies

                    L^B=((xi)*D_E)^(-1)L#.

Perfection therefore gives Lambda#=(xi)*D_E*Lambda. If the actual
ideal identity (xi)*A*conjugate(A)*D_E=O_E holds, the particular lattice

                            L'=A^(-1)*Lambda

is Hermitian self-dual, and Lambda=A*L'. This is equality of the actual
lattices; no saturation or enlargement is used. It supplies the integral
and duality fields of DataX together with finite generation and full span.
[PCL2–PCL5]

The host identities are also proved concretely. Write K=Q(s), s^2=−d,
C=ccK, N=Norm_K(C), and let b be the original half-different. Then
D_K=(s), C*conjugate(C)=(N), and D_(E/K)=b*conjugate(b). Consequently

          xi_H=−1/(N*s),       A=(C*O_E)*b^(-1)

satisfy the required ideal identity. Every complex absolute value of xi_H
is 1/(N*sqrt(d)), with the original scalar normalization. [PCL7–PCL8]

The denominators are the prescribed integers N_A=Norm_E(b) and
N_C=Norm_K(C), uniform across components and embeddings. They give
N_A*Lambda subset L' and N_C*L' subset Lambda. The different-in-a-tower
identity yields

       N_A^2≤|disc E|,       log N_A≤([E:Q]/2)*log rd(E).

The original SupBoundPageRows hypothesis supplies log N_C≤2*large_2.sc.L.
The lattice and these integers are chosen before every later weight and
size record. [PCL9–PCL12]

Thus the complete exists_dataX_of_hasPrinc, dataXOfModel_of_gamAt and
DataXOfModelSt endpoints are available on every original row, good embedding
and component. The common uniformization and principal-congruence inclusion
are still actual input-production tasks. Original source anchor:
CubicalLineBundles/DataXOfModelOfGamAt.lean.
""",
    ),
    (
        "local_growth_suppliers_v47", "LGS", 13,
        "ACTUAL LOCAL GROWTH, CANONICAL MEAN AND FULL AUXILIARY ADMISSION",
        """
LGS supplies the local-growth, mean and admission inputs previously retained
by GLG. Its common GroupCompatibilityFamily remains explicit: the actual
Hermitian, forms, comparison, ring and GatIs fields must hold together on
the chosen family. The theorem does not substitute an abstract local
representation or an unrelated adelic setting for that record. [LGS1–LGS13]

The first steps prove the integral polynomial lattice sandwich with the
original exponent e_p, the orbit/window hypotheses, the chosen-Frobenius
small-order estimate, and all power-band inequalities. The existing
Type-I/II bounds are matched to the actual canonical deficit. Both clauses
of MeanKappaBound follow, including the pointwise bound for every degree
assignment at small primes. [LGS1–LGS7]

The retained common record then supplies the physical slot lattices,
finite class sets, trivial stabilizers, integral operators and rational
descent used in the tensor and finite-walk calculation. For the actual
served set, write Sigma=m*sum_v kappa_v, S=max_v S_v, and

              tau_P=e_p+sum_v m*(t_v+D_p+1).

The ceilings and the +1 are retained exactly. Eventually Sigma≤x^(−epsilon)
≤1/2 and io_P=2*S*Sigma. Smith-tail summation, using
product_v(1+m*kappa_v)≤exp(Sigma), gives

          NP subset p^(ceil(tau_P))*M_ram,
          length_O(M_ram/NP)
             ≤vUnit(G)*G.d*(tau_P+io_P).

Saturation of the ramified intersection justifies passage from the full
lattice to M_ram. Empty served sets and S=0 are treated directly. The
original full rank and coefficient-field ramification factor appear until
the exact local-to-global length identity cancels the latter. [LGS8–LGS10]

Only the auxiliary Ch field is replaced by zero. Every field needed by
the admitted record and LinkG is checked under this replacement. The
geometric theta chain, its lattice maps and the larger Extra.ker condition
are not transported; the zero auxiliary chain supplies just the valuation
clauses used by this consumer. [LGS11]

All twelve admission fields are then supplied with C_31=C_orb(epsilon),
C_e=1 and C_m=302114. These constants precede every delta>0; one threshold
then works for every later height and family member. The completed counting
consumer gives all five original LinkG conclusions with

              C_G=4*C_count+1,       b_o=b^(x^(−epsilon/2)).

The losses, selected rows, places, supports, degree functions and lattices
remain those of the same original family. [LGS12–LGS13, GLG9–GLG17]

The direction of the selected-top implication matters: actual TopsF supplies
Adm2F. One may instead assume Adm2F directly. The literal class-level
linkG_concrete5 consumes Closed(C,GroupCompatibilityFamily) and
Closed(C,Adm2F), then yields Closed(C,LinkG), with coefficient bounds chosen
before the family. This completes that implication and its analytic inputs,
while leaving the actual compatibility and selected-top producers open.
Original source anchor: GroupLattices/LinkGConcreteNoKer.lean.
""",
    ),
]


NEXT_PRODUCERS = """
PRECISE NEXT PRODUCERS AND PARALLEL STARTING POINTS

The remaining work should construct the following original inputs on their
common objects. The completed theorems above can be reused at their stated
scope; their removal from a local dependency list does not by itself close
a compound selected obligation.

1. Common principal geometry and lattice spanning. Construct the original
common IsUnf family with HasPrinc/GamAt, framed-point normalization and the
fixed metric dictionary. The concrete source target is
FrameUnif.exists_unf_hasPrinc in CongrOfDvdModulus.lean, lines 36–57.
Its inputs include the CM moduli consequence N1c, quadratic Hasse norm,
family flag-domain models, simultaneously normalized framed points and
the full analytic IsUnf dictionary; it also supplies LatZ and the l.A=1
exponent match. CNC supplies IsNab and PCL supplies the conditional
trace-dual lattice. The remaining ICL groups are the full principal-chart
package, finite theta/level system, Gaussian identity with absolute
integrability and reproduction, short-rule gluing with a simultaneous
dictionary, and ramified integral jet/value estimates. Higher CoversAt,
all-tuple class sums and uniqueness, one PointIdentCore with common lambda,z,
and ClassSumsSpan remain separate. Preserve both levels and original phases.

2. Finish the adelic setting and arithmetic rows. Build the normalized,
nonzero Bessel W block and its decay, the measured-field block, and the
original Siegel–Weil rescaling with its same-object measure and character
ties. Supply Bessel uniqueness/local ties and the actual AutTie, RowDictTie
and LabTie. RFD removes RowsFinDim. The arithmetic CountIdempotentsClass
theorem, or its three sufficient cylinder counts, must still hold for one
AllRows object with one simultaneous threshold. ARO's completed algebra
and finite local weight estimates can then be applied unchanged.

3. Global quantitative producers. Construct GroupCompatibilityFamily on the
chosen common family, including the actual comparison, level and GatTies,
and supply its selected TopsF or literal Adm2F. LGS supplies the auxiliary
admission, first-growth and canonical mean. The distinct original LinkN
denominator producer, period/height producer, normalized spectral producer
and second-layer compatible selection still need their full constants,
normalizations and earlier family thresholds. None follows from changing Ch.

4. OneChar and coefficient automorphy. Use the complete InpZ, the original
RNC congruence integer and the finite PGK consumer to prove the actual
OneChar trace/length estimate. Construct the separate AUT_UNRAM_COEF,
or AutomorphyUnramifiedCoefficients, datum that supplies its original
marked unramified-coefficient automorphy hypothesis. RigII retains its
universal extension-modularity antecedent, so it cannot supply that
antecedent merely by being installed in InpZ.

5. Remaining shared arithmetic and case suppliers. Continue the F3 local
coefficient bridges and F4 full common-overfield reading, including the
entire coefficient field and exact valuation, norm, GoodCoef and iq data.
The actual complex Hecke standard/no-Jordan and character data, base rows,
host/frame lengths, nonzero chains, group ties, MultEq support, carriers,
parts, all-embedding logLam, HD/d3b and NEb remain at their original scopes.
The second DivRows3 requirement is distinct from the completed first
DivDef3. RH Cases I and V also retain their listed producers. The completed
ordinary Hecke and Hida support remains available.

These branches can be pursued in parallel with explicit ownership. Their
interfaces must agree on the same fields, embeddings, lattices, measures
and thresholds when they are assembled. The final remaining-leaf register
and obligation map give the authoritative whole-contract boundaries.
"""


READING_AND_CHECKS = """
READING, FOUNDATIONS AND REPRODUCIBILITY

RH_new_proofs_v0_47.tex collects the seven new chapters; the cumulative
RH_readable_reconstruction_v0_47.tex includes the preceding reconstruction.
The complete delivery pairs these TeX readers with this TXT progress report
and the full ZIP. Each component contains its human proof, original scope
contracts, source inventory, exact source excerpts, retained foundations,
repeatable metadata builder and validation records. The final package also
contains the shared claim/dependency ledgers and independent reviews.

Numbered human claims and separately named classical foundations play
different roles. Published applications identify their actual hypotheses,
local conventions and normalization bridges. Source and proof hashes make
those identifications reviewable; they are not themselves mathematical
arguments. The accepted source pin is retained throughout, and this
continuation performs no Lean build or kernel replay. A complete human
proof of RH and unrestricted Dirichlet GRH still requires the remaining
original producers listed above and in the final register.
"""


def read_json(root: Path, relative: str):
    return json.loads((root / relative).read_text(encoding="utf-8"))


def clean(text: str) -> str:
    return textwrap.dedent(text).strip()


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def build_report(root: Path) -> tuple[str, dict]:
    cfg = read_json(root, "increment_v0_47.json")
    stats = read_json(root, "integration_stats_v0_47.json")
    graph = read_json(root, "dependency_audit_v0_47/obligation_map.json")
    register = read_json(root, "dependency_audit_v0_47/remaining_leaf_register.json")
    assert cfg["artifact_version"] == VERSION
    assert graph["artifact_version"] == VERSION
    assert register["artifact_version"] == VERSION
    assert cfg["source_commit"] == graph["source_commit"] == PIN
    assert set(cfg["closed_selected_leaves"]) == {"RIG_II", "TASK_INP_Z_ASSEMBLY"}
    assert cfg["components"] == [item[0] for item in CHAPTERS]

    all_claims = []
    chapter_rows = []
    for component, prefix, expected_count, title, body in CHAPTERS:
        ledger = read_json(root, component + "/provenance.json")
        claims = ledger["claims"]
        expected_ids = [prefix + str(i) for i in range(1, expected_count + 1)]
        assert [claim["id"] for claim in claims] == expected_ids, component
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
        "RH AND UNRESTRICTED DIRICHLET GRH — HUMAN RECONSTRUCTION v0.47",
        day + "\nAccepted source commit: " + PIN,
        "CURRENT RESULT",
        clean("""
        Version 0.47 completes two whole selected obligations: RIG_II, the
        original type-II adjoint rigidity theorem, and TASK_INP_Z_ASSEMBLY,
        the exact complete rank-three cohomological input record. It also
        supplies substantial actual inputs in five further chapters:
        universal row finite-dimensionality, eight dependent adelic setting
        blocks, the canonical cusp connection, the principal-chart lattice
        normalization, and local-growth/mean/admission estimates.

        The human-readable reconstruction remains incomplete. The closures
        concern their full original contracts, with the original antecedents
        retained. The new record assembly does not establish OneChar or its
        automorphy supplier, and the new geometric and quantitative results
        do not assert existence of the still-required common families.
        This report explains what is now proved and the precise next inputs.
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
        These figures are read from increment_v0_47.json and
        integration_stats_v0_47.json and checked against the new claim ledgers
        and final obligation graph/register. Class A records a checked
        published application; class B records a written proof at its stated
        scope. Counts measure the inventory and do not express a completion
        percentage. A nested producer can be completed while its larger
        selected contract remains open.
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
        f"The final graph still has {len(extra)} open obligations reachable from "
        "Dirichlet GRH but not from ordinary RH. Their exact registered IDs and "
        "contracts are:",
        "\n\n".join(
            f"{node_id} ({nodes[node_id]['category']}): {nodes[node_id]['contract']}"
            for node_id in extra
        ),
        clean("""
        These require compatible original tensor factors, seeds, residual
        chains and image/automorphy conclusions. The seed choices and fixed
        embedding precede the later towers, and the rank-four propagation
        retains its original residual point and depth bound. Progress in
        rank-three RigII does not identify or close any of these seven
        additional contracts.
        """),
        clean(READING_AND_CHECKS),
        "REPORT INPUT BINDINGS\n"
        + "increment_v0_47.json SHA256: " + sha256(root / "increment_v0_47.json")
        + "\nintegration_stats_v0_47.json SHA256: "
        + sha256(root / "integration_stats_v0_47.json"),
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
    stats = read_json(root, "integration_stats_v0_47.json")
    cfg = read_json(root, "increment_v0_47.json")
    day = date.fromisoformat(cfg["date"]).strftime("%d %B %Y").lstrip("0")
    sections = [
        "RH AND UNRESTRICTED DIRICHLET GRH — HUMAN RECONSTRUCTION v0.47",
        day + "\nAccepted source commit: " + PIN,
        "CURRENT RESULT",
        clean("""
        Partial human reconstruction, accepting the pinned Alpoge-Claude
        formal source as fully checked and correct. Version 0.47 completes
        the original type-II rigidity theorem RIG_II and the full selected
        cohomological input-record assembly TASK_INP_Z_ASSEMBLY. Both keep
        every original antecedent. The complete human proof of RH and
        unrestricted Dirichlet GRH remains unfinished.
        """),
        f"There are {stats['new_claims']} new claims and "
        f"{stats['cumulative_claims']} cumulative claims. The selected graph retains "
        f"{stats['selected_nodes']} nodes and {stats['selected_edges']} edges. "
        f"The {stats['open_count']} remaining whole obligations comprise "
        f"{stats['open_categories']['C']} C and {stats['open_categories']['B']} B; "
        f"{stats['shared_open']} are shared RH/GRH obligations and "
        f"{stats['extra_grh_open']} are additional Dirichlet-GRH obligations. "
        f"The new increment cites {stats['new_source_files_checked']} pinned source files "
        f"in {stats['new_unique_source_ranges_checked']} distinct ranges. "
        "Claim counts are an inventory, not a completion percentage.",
        "READING ORDER",
        clean("""
        1. RH_reconstruction_progress_v0_47.txt: substantive mathematics,
           exact new endpoints, retained hypotheses and next producers.
        2. RH_new_proofs_v0_47.tex: the current audit and seven new chapters.
        3. RH_readable_reconstruction_v0_47.tex: the cumulative manuscript.
        4. RH_dependency_audit_v0_47.txt: the remaining selected contracts.
        5. continuation_checkpoint.json, next_source_targets.json,
           provenance.json and dependency_audit_v0_47/: exact continuation
           and dependency records.
        """),
        "SEVEN NEW CHAPTERS",
        "\n".join(
            f"{component}/main.tex — {prefix}1–{prefix}{count}: {title}."
            for component, prefix, count, title, _ in CHAPTERS
        ),
        clean("""
        KTR proves full RigII through the ordered flag, the actual rank-two
        representation, cyclotomic irreducibility, matched Selmer vanishing
        and the entire nine-dimensional adjoint decomposition. KIZ installs
        all eleven original InpZ fields. RFD proves RowsFinDim for every
        admitted finite test function and arbitrary infinity unit vectors.
        ASG constructs eight dependent adelic setting blocks on the
        same supplied Forms0/Gap data. CNC constructs the full cusp connection
        over arbitrary coefficient algebras. PCL supplies the exact trace-dual
        lattice and discriminant bounds on a supplied principal chart. LGS
        supplies the actual admission, local first-growth and mean estimates,
        retaining the original compatibility and TopsF/Adm2F inputs.
        """),
        "REMAINING SCOPE",
        clean("""
        Next geometric producers include the common principal chart
        FrameUnif.exists_unf_hasPrinc, the full integral-cusp spanning inputs,
        normalized Bessel W, the measured block, Siegel–Weil normalization,
        common row ties and the arithmetic cylinder count. The global gain
        branch still needs GroupCompatibilityFamily and its selected
        TopsF-to-Adm2F supplier; denominator, period/height and spectral
        producers retain their original quantitative scopes. The actual
        OneChar theorem and AUT_UNRAM_COEF are separate from the completed
        InpZ assembly. The seven additional GRH contracts remain explicit
        in the report and final register.

        All original coefficient rings and embeddings, prime 3, data chosen
        before later choices, exact Haar/formal-degree normalizations,
        shared row objects and common geometric/arithmetic witnesses remain
        in scope. Conditional implications do not assert existence of their
        retained inputs. No Lean build or kernel replay is claimed.
        """),
        "PROVENANCE, REVIEW AND DELIVERY",
        clean("""
        The complete delivery contains the TeX readers, this reading guide,
        the substantive TXT report and the full ZIP. Every new claim has
        source/proof ranges and hashes in its component provenance. Pinned
        source snapshots, separately named published foundations, independent
        mathematical and integration reviews, validation records and
        reproducible scripts are included. Predecessor proof chapters and
        claim records are preserved; mutable v0.46 root metadata is retained
        in history/version_0_46. SHA256SUMS covers the distributed files.
        """),
    ]
    return "\n\n".join(sections).rstrip() + "\n"


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parent)
    parser.add_argument("--check", action="store_true", help="Check inputs and report without writing")
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
