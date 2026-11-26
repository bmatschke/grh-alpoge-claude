#!/usr/bin/env python3
"""Record the root's completed independent readings, binding exact paragraphs.

This script records a human mathematical/source review. Its hash checks
are reproducibility checks, not an automated proof checker.
"""
from pathlib import Path
import argparse,hashlib,json,re
ROOT=Path(__file__).resolve().parent;REV=ROOT/'reviews_v0_19'
ap=argparse.ArgumentParser();ap.add_argument('--component',choices=['arithmetic_realization','theta_test_inputs'])
args=ap.parse_args()
def sha(b):return hashlib.sha256(b).hexdigest()
reviews={
'arithmetic_realization':'''INDEPENDENT MATHEMATICAL AND SOURCE REVIEW: AR
Reviewer: /root
Author reviewed: /root/class_rank
Result: PASS within the stated conditional scope

The entire main.tex section was read, including every numbered AR claim.
Source checks focused on the literal local shape and level characters,
tame-Artin orientation, Joint fields, coefficient descent, harmonic
evaluation/sign/injectivity, WtMap duties and installed series reading.
This is a human review, not Lean compilation or kernel replay.

Bad-place inclusion uses exact ramification and cancellation on units.
Selected halves are identified with the actual Pq choices; conjugation
stability and excluded residue primes justify uniqueness at local places.
The reciprocity map, Frobenius sign and inertia assumptions remain explicit.
The type-character comparison retains normalized algebraic adic-character
existence and chooses a twist away from the type prime using all-place
SideB.cover. It cannot use the empty-Tw auxiliary stage. Open-kernel finite
characters are read continuously without claiming that an arbitrary
Qbar_ell-to-C field isomorphism is continuous.

The conductor parahoric and type unipotent comparisons prove subgroup
equality as well as character values. Both selected local and conjugate
components are handled. Residue additive characters extend using divisible
C* and remain locally constant through their open kernel. The type-level
characters are chosen before the quantified complex embedding. IdFrame
reduction is literal, with no free conjugation of the frame. The common
unipotent character and finite residue multiplicative order yield exactly
the required (g_a-1)st power comparison.

Joint is formed from the intersection of the actual geometric and series
levels. Its identity frame, scalar restriction, map and translation laws
use the same realizations. SerAt.join is subsequently supplied only for
the installed reading; an arbitrary pre-existing rdV is not replaced.

Entrywise coefficient-field linear projection descends infinitely many
intertwining equations without assuming a finite intersection is enough.
Polynomiality passes to duals and to invariant subspaces through constant
coordinate matrices. Complex classification and the canonical dual
highest-weight theorem remain named inputs. A minimal complex irreducible
submodule and descended nonzero intertwiner prove a K-isomorphism by
irreducibility and the two dimension inequalities, without assuming
absolute irreducibility. Infinitesimal characters are compared by sorting
the strictly decreasing shifted integer sequence. Arbitrary base-change
bases are reconciled using inverse matrices over the original field.

The characteristic-zero Weyl/dual-Weyl identity is retained; no integral
identification is inferred. Orbit span follows by finite interpolation of
divided powers. Complementary minors preserve the exact extremal sign.
The harmonic injection uses the positive Fock pairing, its explicit
adjoint rule, the triangular big cell and continuity, rather than a rank
count. WtMap includes injectivity, harmonic membership, equivariance,
range containing the actual coefficient lattice and denominator clearing.

The global LevMatch multiplies all factors and retains the false-side
inverse convention. Pointwise form reading gives covariance and injectivity;
finite double-coset representatives give one product of denominators.
Each quotient of that product by a chosen factor is the product of the
other denominators in R. Integral closure supplies the root-of-unity
level scalars in R. Existing stabilizer covariance suffices; trivial
stabilizers are not assumed. The resulting integral preimage spans.

The final RankTie conclusion retains global MtFam/NExpTied, normalized
characters/weights, pinning and installed series. IsGalOf, side/index
choices, nonempty coverage, and the actual MuIsW ColW/Pre2/St/RowPk join
remain. Representation-theoretic primitives and algebraic adic-character
existence are not disguised as elementary deductions.
''',
'theta_test_inputs':'''INDEPENDENT MATHEMATICAL AND SOURCE REVIEW: TT
Reviewer: /root
Author reviewed: /root/comparison_span
Result: PASS within the stated conditional scope

The entire main.tex section was read, including every numbered TT claim.
Source checks focused on local integral normalization, the actual Fourier
and frame operations, finite unfolding support, all SumOK fields, the
fixed-field SumRatK calculation and the exact remaining NumbersIn and
analytic/tower/separation interfaces. This is a human review, not a Lean
build or independent kernel replay.

Compact locally constant integrals use finite cosets and rational Haar
volumes, including when the normalization set is not a subgroup. The
singular-ball cancellation uses an explicit rank-one matrix fixing the
singular center and having prescribed unit determinant. Totalized
nonintegrable multiplicative integrals are explicitly separated from
the genuinely integrable flat additive integrals. No analytic convergence
statement is obtained from the fact that a totalized integral is zero.

The ordered Fourier/middle/Fourier flips preserve literal support, depth
and coefficient fields; their phases are bounded roots of unity and
half-integral norm factors use only the finite required square roots.
The rational integer q is not identified with a uniformizer. The flat
support and missing tail bounds use actual translation characters and
annihilator lattices. The uniform representative proof uses h=b*kappa
and translations whose h-inverse images remove the potentially unbounded
b. Exact block multiplication and the literal free pattern retain the
correct symmetric unipotent group. Compactness of bounded matrix/inverse
pairs gives finitely many double cosets, hence the finite global support.
The rectangular tail argument keeps c rows and c+1 columns; the column
i.succ exists even for the last of the c row indices and for c=1.

Pure coset data of the same depth and idempotent are equal if their
supports meet. Evaluation then fixes each coefficient and bounds the
union of all expansion supports by one finite expansion. Expansion
independence is proved on finite-dimensional function spans using
separating point evaluations and tensor injectivity. The actual theta
vector characterization, weights, branching and class structures remain
the source ones. Rational inverse stabilizer orders do not require
trivial stabilizers. The eleven SumOK duties are accounted for.

A rational nonsingular coefficient minor proves polynomial coordinate
descent, not integral unimodularity. Rational substitutions, fixed jets,
the bilinear branching/Fock conventions and its nonzero rational
normalization retain the chosen coefficient field without assuming it
is closed under arbitrary complex conjugation. Every displayed term of
the finite global vK sum is in that same field. SumRatK is conditional
on its literal FieldOK; it does not prove a period identity or convergence.

Finite ray-class representatives control all finite-idele values of the
actual algebraic characters in a single number field. Only finitely many
local square roots and phase roots are adjoined. The moved-vacuum jet
calculation, compact Haar projection and finite bottom-period arguments
retain the exact common-data and scalar-normalization identities stated
in the text. Algebraicity of individually chosen values is not replaced
by membership in an arbitrary preassigned field.
The moved lattice has the literal orientation hatLambda=u*B*hatO.
The archimedean determinant exponent is N-k: N oscillator coordinates
contribute N/2 and the specified splitting contributes -b. The finite
Weil arithmetic and bottom full-Weil existence hypotheses remain explicit.
For the ratio calculation I checked the exact same-bottom-triangle join,
critical nonzero denominators, StepRatio products and K-linear projection.
The NumbersIn inventory has eight fields; Choice has thirteen fields,
IsBase has six, and Is adds RealOK. An arbitrary finite field compositum
does not establish the literal embLL FieldOK or the separation field.

The coefficient/jet/period finite-field joins preserve their quantifier
order. The remaining finite-Weil, critical L-ratio, convergence,
separating-functionals, period/tower/nonvanishing and positive spectral
operator/type suppliers are explicit. LinK, InjK and Formula2K are not
deduced from finite-dimensionality or local coefficient arithmetic.
''',
}
for component,body in reviews.items():
 if args.component and component!=args.component:continue
 p=ROOT/component/'main.tex';raw=p.read_bytes()
 ledger=json.loads((ROOT/component/'provenance.json').read_text())
 markers=list(re.finditer(rb'(?m)^\\paragraph\{([A-Z]+\d+):',raw))
 assert [m[1].decode()for m in markers]==[c['id']for c in ledger['claims']]
 out=body+'\nEXACT REVIEWED PROOF PARAGRAPHS\n'
 for i,m in enumerate(markers):
  b=markers[i+1].start()if i+1<len(markers)else len(raw)
  h=sha(raw[m.start():b]);c=ledger['claims'][i]
  assert c['proof_location']['sha256']==h,c['id']
  out+=c['id']+' '+h+'\n'
 out+='\nmain.tex SHA256 '+sha(raw)+'\n'
 out+='Pinned commit 7cbf7a0c32fca1badf05931879a37c3f8a2b03b4\n'
 (REV/('root_reviews_'+component+'.txt')).write_text(out)
 print(component,len(markers))
