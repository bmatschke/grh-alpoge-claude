#!/usr/bin/env python3
"""Write root's mathematical review records after inspecting the component proofs."""
from pathlib import Path
import argparse, hashlib,json,re
ROOT=Path(__file__).resolve().parent
ap=argparse.ArgumentParser();ap.add_argument('component',choices=['initial_geometry','arithmetic_compatibility','local_stages']);a=ap.parse_args()
notes={
'initial_geometry':'''The entire IG1–IG14 mathematical text was read independently. Critical
literal endpoints and definitions were compared with the pinned source,
including exists_pre_sized, all17 PreX fields, the15 LevCh fields,
DsP_pos_and_lower, the g_big threshold, the9 RecOK fields including mink,
LedOK and recExP_of_recAtG.

IG1–IG3: the ray-class coset is a nonzero shifted plane lattice; its
multiplicity is precisely the congruent-to-one unit group. The covolume
cancels the ideal norm at s=1, giving one positive residue for every class.
Gaussian Mellin continuation is meromorphic only at1 and vanishes at−1.
If a nontrivial L vanishes at1, the product over all ray characters is
entire. Each local factor has nonnegative Dirichlet coefficients. Taylor
expansion from a real point>1 with Tonelli extends that nonnegative sum
to−1 and contradicts the zero there. No unproved abscissa bound or
nonvanishing premise occurs. The bounded higher-prime-power logarithm
and the convergent degree-two prime contribution prove qualitative
unbounded prime norms. The auxiliary quadratic-field norm construction
also supplies ordinary progression primes, including primes over2,
without an extra analytic nonvanishing theorem.

IG4–IG8: the chosen cyclic host labels, congruence selections and norm
factors are the same through releveling. The literal fourth-power BB
threshold is checked by the explicit modulus and valuation inequality.
The two HC words have exact half-integral coordinates and gaps; finite
weight spread is bounded before choosing the type prime. Its window is
chosen freely and made exact. The finite-adelic sign change is supplied
by actual local unit norms, rather than inferred from real signatures.
The seventeen PreX fields include the distinguished-prime splitting
cardinality and the actual spread and size conditions.

IG9–IG11: reduction of the finite automorphism group is injective because
a prime-to-p torsion element in the principal congruence kernel is
trivial, and the rational representation excludes p-torsion by its
dimension. This argument works with arbitrary ramification for the
prime-to-p cancellation step. The finite genus and integer-valued
binomial determinant give the positive integer mass-index factor.
The source then deliberately restricts to a singleton before resetting
duStar; the same norm/space/letter data survive and the lower window
endpoint is exactly T. Orientation uses the actual factor or its
conjugate and changes no type frame. Pins are checked on this datum,
not on an unrelated base.

IG12: positivity of the literal trueVol choice, including its fallback1,
proves the exact baseVol/noJet construction with the same Haar datum.
It does not prove a VolIs witness or geometric covolume.

IG13–IG14: the formal-degree factor is the ordered Vandermonde
polynomial; no discrete-series realization is inferred. The large-scale
g_big estimate is uniform in the later inputs. The recursive arrow
retains window_lower as an explicit input, rather than claiming its
mass-ratio deduction. Threshold minima/maxima are taken in the literal
order. du and Ds precede every supplied Lv. The dependent-pair equality
in FromCoreAt is used before forming BPt, and the actual setDiv
identities preserve QD. All nine RecOK duties and actual integral NP
comparisons in LedOK remain. Full HFrame, V4.Core, geometric volume
and quantitative mass/prime/window inputs remain explicit.

Corrections requested and incorporated: remove spurious commas from
mass-index exponents; explain prime-to-p torsion cancellation for a
possibly ramified DVR; retain all nine RecOK fields including mink.
Result: PASS under the displayed background and conditional scopes.
''',
'arithmetic_compatibility':'''The entire RC1–RC21 mathematical text was independently read, with
source comparisons at the literal rank/choice/MuIsW and local level
interfaces. Every construction retains the same D and embeddings.

RC1–RC2: finite evaluations detect the coefficient form space, allowing
a Hamel-basis coefficient extraction with only finitely many nonzero
global coefficient functions. This justifies scalar extension despite
the functions' infinite domain. Actual WtMatch and LevEq are necessary;
the actual jMt_basis, MtReal and NExpTied supply the rank comparison.
No abstract rank estimate replaces the realization.

RC3–RC7: global reciprocity and the actual NTw.art_univ remain explicit
inputs. The finite image makes the Hecke character kill the closed Artin
kernel. Primitive roots identify its finite values with the prescribed
coefficient field. Frobenius detection follows from the stated
uniformizer convention, finite-coordinate truncation and weak
approximation. It uses all Frobenius lifts as stated. Exact ramification,
anticyclotomic conjugacy and full decomposition triviality at ell are
separate verified properties. The actual universal ring-class map
supplies descent. Changes between primitive-root readings give a
prime-to-ell power, including the side sign and k=0 cases.

RC8–RC11: denominator clearing proves the same side embedding; a local
map reflects integrality because the inverse of a nonintegral element
is a nonunit. The complex embedding is algebraic, via the proved
continuum cardinality bound, without an invented continuity property.
Two-element and fixed conjugate-place orbits are handled separately.
The nonempty-local criterion proves character equality from IsGalOf
using locally constant finite-image characters, then derives the exact
conductor equality. Index and side compatibility are retained.
The simultaneous choice theorem preserves every quantifier of its
same-object level/weight supplier, including every applicable complex
reading. The empty local set makes only the relevant local clauses
vacuous, not the global reading and packet clauses.

RC12–RC13: resetting the five tuple fields produces a bare MuW row;
the proof explicitly refuses to transport an arbitrary RowPk through
this reset. The actual ColW/Pre2/St lift preserves the two assignment
maps by definition. All ten MuIsW fields, the frame equality and the
same QOf=T.Q equality are individually accounted for. Existence of
these simultaneous geometric records remains.

RC14–RC19: the rank-one conjugation has unit determinant a, puts both
matrices in the parahoric, and gives distinct lower-block determinant
characters, proving the scalar-action rigidity. Equal finite indices
of opposite parahorics forbid an automorphism landing in both.
The unipotent index is prime to the residue characteristic; finite
scalar quotient and Bezout recover the additive character on integral
entries. The explicit lower-triangular integral frame with first two
columns1 and(0,...,n−1) has determinant1. Integral positive-unitary
matrices are monomial root-of-unity matrices; unramified odd-prime
reduction and the second column kill both root and permutation.
The resulting trivial double-coset stabilizer constructs nonzero
forms for every nonzero weight. Actual Joint, local shapes and CellWt
remain the substantive realization inputs. Finite support decomposition
then proves global LevEq with exact local characters.

RC20–RC21: the selector is constant on valuation/conjugation classes
and gives readings only at twisted places; it does not supply RC11's
all-place hs. Faithful flatness, finite module restriction and
Noetherianity give a finite theta span. A minimal generating subset
of the actual averaged theta vectors is a DVR basis by dividing a
relation by its least-valuation coefficient and using torsion-freeness.
That family is chosen before all forbidden sets. Enlarging a finite
set by all primes over the same rational primes gives Apart; finite
induction supplies pairwise avoidance. The no-twisted-place case is
separate. Actual aux3 twisting/IdxAt inequalities, FullRank, adm7 and
settings remain explicit, not inferred from the finite construction.

Result: PASS under the displayed same-object hypotheses. No arbitrary
equal-rank lattice matching is promoted to Hecke or metric compatibility.
''',
'local_stages':'''The entire LS1–LS22 proof text was independently read. The primitive
completion, Frobenius and invariant arguments were checked, together
with the final same-object stage join. Literal source field inventories
and pinned endpoints accompany the component ledger.

LS1–LS3: the Hasse-derivative orbit halving gives a uniform Ax constant16.
The binomial valuation estimate and cyclotomic polynomial coefficient
bound are explicit. Uniform normalized-trace projections converge in
the cyclotomic completion, including p=2,n=1. The finite-coset product
reduces all finite-base Tate twists to the Qp case.

LS4–LS8: the sharp map is not treated as additive. The principal theta
kernel, p-saturation and quotient completeness are proved in the actual
Witt ring. The de Rham DVR and algebraic coefficient section are the
actual adic construction, not a formal replacement field. The divided-
power completion map is bounded modulo each xi power. Its injectivity
uses a finite divided-power intersection calculation and repeated
p-divisibility; density alone would not suffice. The logarithmic series
uses integral radical/power estimates that remain valid at2. Actual
Galois/cyclotomic and unramified coefficient identities are preserved.

LS9: the Frobenius coefficient induction was checked against
FrobeniusPeriodRingInjective.lean:coeff_mem, coeff_mem_of_frob and
pow_dvd_of_frob. Its invariant retains the auxiliary coefficient b.
Both cases N+r+1<=lN and N+r+1>lN are necessary; the latter uses
regularity modulo p and cancellation before descending. Denominator
clearing supplies the stated ideal power, and the final completion
argument uses the independently proved de Rham injection.

LS10–LS13: the nilpotent/Frobenius-fixed residue argument extracts Zp
digits. Simultaneous theta vanishing gives divisibility by mu by
successive Witt coefficients, and the Frobenius-image decomposition
holds in the completed divided-power ring. The eigenvector/filtration
induction handles p=2 through exponent p−2>=0. It identifies the exact
crystalline localization and proves only the stated fundamental
intersection, not an unproved surjective exact sequence.

LS14–LS17: the nonzero Tate-twist invariants exclude nonzero filtration
orders of de Rham invariants. Subtracting the algebraic residue lift
gives BdR^{G_K}=K. Crystalline invariants have a periodic Frobenius
orbit; polynomial interpolation along a primitive unramified root
orbit and the fundamental intersection force membership in K0.
This avoids assuming an unramifiedness/comparison theorem for
representations. The period, local-prime, Ainf and tie fields use the
same rings, maps, prime, filtration, period and normalized valuation.

LS18–LS22: the final bare stage is explicitly constructed on the same
adapted row object. Local-prime data exist at every rational prime even
though the representation/twist index sets of this auxiliary NStage
are empty. All nonvacuous prime, residue, cyclotomic and type/weight
fields are supplied. Empty universal statements are distinguished from
actual Galois data. The Later join reuses SE's other stages on those same rows. IG independently refines the
chosen-volume noJet construction. Its empty twist type
cannot receive NChoice.twI from the nonempty coefficient-place type.
No comparison for arbitrary geometric representations, nonzero
projector rank, Sha finiteness or quantitative bound follows.

Corrections requested and incorporated: clarify the dyadic squared
norm sentence; repair the missing quad macro; give the full coefficient
induction invariant and both cases in LS9.
Result: PASS within these explicit constructions and retained background.
'''}
component=a.component
path=ROOT/component/'main.tex'
raw=path.read_bytes()
marks=list(re.finditer(rb'(?m)^\\paragraph\{([A-Z]+\d+):',raw))
ledger=json.loads((ROOT/component/'provenance.json').read_text())
assert [m[1].decode()for m in marks]==[c['id']for c in ledger['claims']]
lines=[f'INDEPENDENT ROOT MATHEMATICAL REVIEW — {component} — v0.18',
'Reviewer: /root (independent of the delegated component author)',
'Pinned commit: 7cbf7a0c32fca1badf05931879a37c3f8a2b03b4',
'Scope: human mathematical/source review; no Lean compilation or kernel replay.','',notes[component],
'EXACT REVIEWED PROOF PARAGRAPHS']
for i,m in enumerate(marks):
 stop=marks[i+1].start()if i+1<len(marks)else len(raw)
 h=hashlib.sha256(raw[m.start():stop]).hexdigest()
 lines.append(m[1].decode()+' '+h)
lines+=['','Complete main.tex SHA256 '+hashlib.sha256(raw).hexdigest(),
         'The hash record binds this review to the actual paragraphs; it is not a proof checker.']
dest=ROOT/'reviews_v0_18'/('root_reviews_'+component+'.txt')
dest.write_text('\n'.join(lines)+'\n')
print(dest)
