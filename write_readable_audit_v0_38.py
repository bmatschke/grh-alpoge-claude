#!/usr/bin/env python3
"""Write a current human-readable audit, including every exact remaining contract."""
from pathlib import Path
import json
ROOT=Path(__file__).resolve().parent;AUD=ROOT/'dependency_audit_v0_38'
cfg=json.loads((ROOT/'increment_v0_38.json').read_text());reg=json.loads((AUD/'remaining_leaf_register.json').read_text())
records=reg['records'];new=cfg['expected_new_claims'];total=cfg['predecessor_claim_count']+new
def esc(s):
 return ''.join({'\\':r'\textbackslash{}','_':r'\_','&':r'\&','%':r'\%','$':r'\$','#':r'\#','{':r'\{','}':r'\}','~':r'\textasciitilde{}','^':r'\textasciicircum{}','≤':r'$\le$','≥':r'$\ge$','→':r'$\to$','∩':r'$\cap$','κ':r'$\kappa$','λ':r'$\lambda$','χ':r'$\chi$','𝒞':r'$\mathcal C$','Ψ':r'$\Psi$','ε':r'$\varepsilon$','−':r'$-$','/':r'/\allowbreak{}'}.get(c,c) for c in s)
plain=f'''RH AND DIRICHLET-GRH HUMAN RECONSTRUCTION — v0.38
22 November 2026
Source commit: 7cbf7a0c32fca1badf05931879a37c3f8a2b03b4

STATUS

The full selected cuspidal theta-extension obligation is now reconstructed on its original common-data premises. This version supplies both initial analytic gates left by v0.37: finite volume of the actual target quotient and boundedness of the original extremal theta function. It also advances the original selected rank-four completed-point/patching route and proves the first exact division-identity constructor on the common selected realization.

There are {new} new human proof claims and {total} cumulative claims. The underlying Alpoge–Claude Lean proof is accepted as fully checked and correct. The complete human RH/Dirichlet-GRH proof remains unfinished; this audit concerns the reconstruction, not formal validity.

Exactly one whole selected leaf closes: BASE_THETA_CUSPIDAL_EXTENSION. The selected sufficient graph keeps all 121 nodes and all logical edges. RH reaches 101 nodes and unrestricted Dirichlet GRH reaches 110; together they reach the whole graph. Its open coupled leaves decrease from 34 to 33: 22 C, 9 B and 2 D. All 245 historical compound targets in 107 groups remain with additive scope updates. These numbers measure the chosen register, not a percentage of mathematical difficulty or a proof of absolute minimality.

CLASSIFICATION

A: a direct published-theorem application, with the original hypotheses checked.
B: an elementary or moderately difficult argument independently reconstructible; status separately states whether its proof is complete.
C: a substantial or deep argument still requiring reconstruction.
D: a possible gap in our human understanding of the formal source, not an allegation of a gap in the accepted formal proof.

Checked A applications are internal completed inputs, so there are no open A leaves in the current selected register. The two D leaves remain AD_VANISH_K_MATCH and HOST_RIGID_S. The published-application registry records the exact theorem, checked hypotheses, conclusion used and limits of each import. Consumer theorems can be complete while the original objects satisfying their premises still require construction.

I. FINITE VOLUME FOR THE ORIGINAL ADELIC UNITARY QUOTIENT

FV1–FV11 start with the actual CM extension E/F and the actual nondegenerate Hermitian form J. They identify the source matrix group with the adelic points of Res_(F/Q) U(J), including its exact topology and rational subgroup. After the splitting extension, the unitary group becomes a general linear group. This proves connectedness and reductivity. The center is the restriction of the norm-one torus; its real points are a finite product of circles. A rational character is trivial: its restriction to the derived group is trivial, and the involution sends the determinant character to its inverse, leaving no nonzero invariant character. Rank zero is handled directly.

These checks justify Borel's finite-volume theorem for this actual group. The precise published inputs are Lemma 5.5 and Theorem 5.6(i) of A. Borel, Some finiteness properties of adele groups over number fields, Publications mathematiques de l'IHES 16 (1963), 5–30. Theorem 5.1 supplies finite adelic classes. The application certificate checks the exact connected reductive algebraic group and rational-character condition.

The remaining measure argument is written independently. One first obtains a finite-volume quotient for a permitted Haar measure and fundamental domain. Any other Haar measure differs by a positive scalar. Two a.e. fundamental domains have equal measure by a countable disjoint partition into rational translates and left invariance. Thus finite volume holds for every original Haar measure and every supplied a.e. fundamental domain, exactly as FiniteVolume2 requires. The proof never replaces the given quotient measure by an arbitrary probability normalization.

Consequently each stored target W_i admits its actual FinPair. These pairs can be chosen before every theta parameter t, finite translation x and coefficient vector. The same proof gives a finite set of adelic classes at an original open level. For a compact-open subgroup K and finite representative s, the real group is the original product of unitary groups, and
  Gamma_s = {{gamma_infinity : gamma rational, gamma_f in s K s^(-1)}}
is an arithmetic subgroup of that exact real group. An arbitrary original open level contains a compact-open sublevel; one never calls the subgroup arithmetic merely because an unrestricted open level was supplied.

II. THE INITIAL THETA BOUND, PROVED BEFORE HILBERT REALIZATION

SBD1–SBD16 provide the other initial gate. Let phi be the actual extremal theta function U_itx(e_i). Inherited HCU/TAE/FIA/CTC/JIO give the original smoothness, uniform moderate growth, highest-weight differential equations, finite level and transvection cusp condition. The first task is to obtain the full enveloping-center finiteness needed for the published decay theorem without using the later Hilbert construction.

The source's iterated curve smoothness is converted to ordinary manifold smoothness in its actual second-kind charts. The right differential operator R_X acts along g exp(tX), with bracket +[X,Y]. Its complexification and original right-fold derivative order are retained. The initial vector satisfies upper-triangular annihilation and the specified diagonal weight in the original x0Mat frame.

For any element z of the full enveloping-algebra center, commutator swaps put words into lower/diagonal/upper order. Only a spanning statement is needed, not PBW linear independence. Choose a generic diagonal element avoiding the finitely many nonzero weights in one expression for z. A polynomial in its adjoint action removes every nonzero-weight word and fixes z. In an ordered weight-zero word, a nonempty upper factor annihilates phi; with no upper factor, any nonempty lower product has strictly negative total height and cannot have weight zero. The surviving diagonal polynomial acts by a scalar. This proves full-center scalar action directly on the initial seed. It also gives the literal original gelf operators, with length k+1 and the original derivative order. There is no assumption that those displayed operators generate the full center.

Next the original ZI subgroup is identified exactly. Choose a nonzero anti-invariant eta in E and an isotropic rational vector xi. With
  T_xi = xi xi* J,    T_xi^2=0,
  z_xi(a) = 1 + eta a T_xi,
the map a -> z_xi(a) is the original transvection subgroup, isomorphic to the additive adele group of F. The rational subgroup corresponds exactly to F. A nonzero matrix coordinate gives a continuous inverse and proves closedness.

For a compact-open additive subgroup B of the finite adeles, choose denominator bounds b O_hat subset B subset c^(-1) O_hat. The Chinese remainder theorem gives A_f=F+B. The rational intersection F intersect B is a lattice; a half-open real parallelepiped Q gives the exact fundamental domain Q x B for F in A. This makes the source ZCusp integral a genuine compact quotient integral. On an arithmetic component, take B to be the inverse image of s K s^(-1) under the finite transvection map. Integrating over Q x B then gives the corresponding real transvection average of phi_s equal to zero, with its original finite level.

The crucial cusp comparison treats every proper rational parabolic P of Res_(F/Q)U(J). Milne's Algebraic Groups (2017), Theorem 25.1 and Proposition 17.60, give a rational cocharacter lambda with P=P(lambda) and unipotent radical N=U(lambda). Restriction-of-scalars adjunction makes this an F-cocharacter of the original unitary group. The Hermitian form pairs only weights m and -m. A nonzero vector in a highest positive weight space is isotropic. Every element of N fixes it, because N strictly raises weights; unitarity also fixes its Hermitian dual row. Its transvection lies in N, has positive conjugation weight, and is central in N.

A separate elementary argument proves compactness of each real unipotent arithmetic quotient. Choose a rational central flag and second-kind exponential coordinates. Clear denominators so fixed steps in every coordinate belong to the arithmetic lattice. Reducing coordinates from the highest quotient downward moves every point into a compact box. The triangular multiplication also proves unimodularity. Fubini and the central transvection's zero average now give the zero N-constant term for every proper rational P. This verifies the precise parabolic cusp hypothesis, not just a maximal-parabolic or informal cusp condition.

For each finite component, SBD12 checks every hypothesis of Miller–Schmid, Rapid decay of smooth cuspidal automorphic forms, Advances in Mathematics 231 (2012), 940–964, Theorem A: the actual reductive rational group and compact real center, its actual arithmetic Gamma_s, smoothness, moderate growth in a faithful matrix norm, full-center finiteness, and every proper rational-parabolic cusp integral. No K-finiteness or Hecke-finiteness assumption is added. A faithful representation including the standard representation, its dual and the trivial representation has norm at least one and controls the source's normInf.

The theorem's decay with exponent one bounds phi_s on a Siegel set. The finite rational Siegel covering in equation (2.8) gives finitely many translates. For each translate, its conjugated arithmetic group and translated cusp hypotheses are checked separately. Taking the finite maximum bounds phi_s on the whole real group. Taking the finite maximum over the original adelic classes gives
  for every original i,t,x, there exists C_itx such that
  |U_itx(e_i)(g)| <= C_itx for every original adelic g.
This is precisely the initial bound required. No bound uniform in t or x is claimed or needed.

FV supplies finite pairs before t,x, and inherited SPR supplies the complete pointwise multiplicity map, exact lowest-type restriction and linear lifting. SBD14–SBD15 therefore construct the original all-parameter theta maps on the same R. They preserve measures, levels, frames, metrics, integral formulas and stored-choice activation. SBD16 specializes this universal result to the selected base-parameter finite bases. No additional eventual family threshold is introduced. The whole selected BASE_THETA_CUSPIDAL_EXTENSION leaf is closed.

The original common geometric readings, rational tests and actual base rows remain separate. Also, this theorem does not prove the source's universal quotient-height CuspRapidDecay predicate for arbitrary IsAutFunSm/IsCuspFun. That broader predicate remains a source input; its growth conversion is unreconstructed, and the human division consumer explicitly retains RowPairInt as explained below.

III. THE SELECTED COMPLETED REPRESENTATION AND ONE-POINT COMPARISON

CRW1–CRW21 retain the same original h=0, a=n=4, g=0 Choice/B1/B2 witness, point, Kap, T, TWPl, TWAut and paired ideal J. Put d=[L+:Q], q=T.q and D0=4d+4q. The odd coefficient space is zero; the first-order Selmer space need not vanish.

On the explicitly normalized coefficient data O onto K, for the original point f:B->K[[t]], p=ker f and section s with f(s)=t, the proof first establishes f is local. Completeness then evaluates O[[S]] at s, giving B/p=K[[t]] and m_B=p+(s). The actual coefficient ring is
  O_circ = completion of O[[S]]_(varpi),
a DVR with residue field K((t)). Its map to R=completion of B_p supplies the source's original coefficient sections and residue map rF. This uses neither a substituted coefficient field nor a presumed flat map into R.

The original NP.span condition implies that the residual full-block representation spans all 4-by-4 matrices over K((t)); it is split absolutely irreducible. Chenevier's Theorem 2.22(i), applied to the full Cayley–Hamilton determinant law over the actual henselian completed ring, identifies its Cayley–Hamilton quotient with the matrix algebra. This theorem requires no inversion of 4!, so ell=3 is included. The proof then independently normalizes the residual representation and original polarization, using only inversion of 2 and a convergent matrix square-root iteration. A finite trace-Gram matrix and Artin–Rees comparison supply the actual continuity. Every closed-ideal and NonSS field in the original full-block S6 is checked separately.

An O_circ-derivation from R to its residue field kills p^2 and the coefficient power-series subring. Finite generators of p give a bounded target lattice L and the estimate
  alpha(m_B^j) subset t^(j-1) L.
This is proved before invoking the truncated deformation conditions; it is not a hidden trace-boundedness premise. Differentiating the original representation gives the polarized cocycle and a cotangent-to-Selmer map. The trace and original determinant coefficients prove injectivity. The unchanged selected B1/B2 bounds then control the original limit cohomology on a supplied Lim and give the D0 bound for the actual relative cotangent space.

Lifting cotangent generators and iterating the maximal-ideal approximation produces a surjection from O_circ[[X_1,...,X_D0]] onto the actual completed local ring. The prescribed presOut0/GalOut dimension comparison and the h=0 ChainAbs consumer are reconstructed on the original patching inputs. The standard Noetherian, completion, Artin–Rees and dimension facts are separately listed as checked Stacks Project applications.

This does not close Raw. Its remaining producers are the actual S4/limit data, patched ring/maps/modules with S5 support, and CoreBC coefficient normalization/added Unit parameter and pro-ell descent back to the original point and same ideal J. The old coefficient ring need not already surject onto the point residue field. Ordinary/control/separating arithmetic fibers, type/neatU/TThetaEx, four Hida endpoints and all-level same-J HasAut also remain. Both rank-four Links, fixed iota, ell=3, full CohP/LocCFT/N4 and the common coefficient threshold are preserved.

IV. THE FIRST EXACT DIVISION IDENTITY ON THE SAME REALIZATION

DI1–DI21 prove the first literal DivDef3 on the same CSR updated R,F,Y,Z,C,sEE. They retain the original common readings, Pins/Holds, full stored nonzero chain, all five real-group predicates and original group-tie premise, PLUS the additional RowPairInt producer for exactly the actual pairs and required finite residual translates with their original scaled measures and domains. This is a conditional sufficient refinement, not the original theorem from its original premises alone. The stronger second DivRows3 theta square is outside this result.

The level proof starts from the actual finite residual block and its flag-character transformation law on the vacuum. The finite Weil action commutes with the archimedean creators, so the same character holds on every polynomial vector. Translating the unchanged theta integral then gives the level identity at the original nonzero It value.

To extend that equality to the full smooth model, the defect is regarded as an equivariant multilinear map. Compact averaging with normalized powers of the polynomial (2n+Re tr(k))/(3n) approximates a smooth vector in every Sobolev seminorm and gives K-finite vectors. The original HarishChandraModules premise and an explicit finite interpolation argument propagate a nonzero kernel vector through the K-finite tensor product. Separate Sobolev continuity extends the zero defect to all smooth vectors. This proves StepLev and TopLev without importing a new general Fock cyclicity theorem.

For RowProj, the actual finite-group central idempotent is self-adjoint. Moving it between the two slots gives the same scalar-witness equations in the source's definition of ipM. If neither pair has a witness, both values are the source's default zero. If a witness exists, a nonzero tensor norm proves its scalar unique, so the two literal ipM values agree. The measure remains exactly nP^(-1) times the original quotient measure on the same fundamental domain. No rescaling or replacement Petersson pairing is introduced.

The remaining finite tensor, cardinality and integral-lattice arguments give both composite RowSideDef3 records and the li/span/lat fields of the first theta record. This supplies the first DivDef3 constructor on the selected realization. It does not construct that realization, its stored nonzero chain, group tie, rational tests or stronger theta square.

The generic row argument uses the explicitly additional RowPairInt premise. The source derives such integrability from CuspRapidDecay only after converting per-finite-coset normInf growth to global-height IsUnifModerate through a polynomial unitary reduction theorem. That conversion remains unreconstructed; qualitative finite classes and the existing coset estimates do not supply it. FV supplies volume, but SBD's initial highest-weight seed theorem alone does not supply this broader condition. The immediate smaller question is whether integrability of the actual pairs and their required finite translates can be reconstructed directly. No existence of an IsMultIP scalar witness is required for DI12; the nonzero IsItW chain used in the level proof is a separate input. That is recorded as a next task, not a proved substitute.

V. FINAL CUT AND PRIORITY

The original ten-input final interface is unchanged. Its global assembly consumes one compatible family with the original second layer and duties, local installation, denominator/retained-defect, period-height, local-gain and spectral producers. Their actual common objects and estimates remain in the contracts below.

RH and two-primary targets retain Cases I/II/V. Unrestricted Dirichlet GRH additionally retains CaseIII, SeedIV and the original chains. The established VWinAt(chi,401), floor(x^400) and 1/2+9epsilon endpoints keep their scopes.

'''+cfg['next_local_priority']+'''

The continuation notes contain pinned locators and the smallest remaining supplier contracts. They are work plans, not additional proof claims.

EVERY REMAINING SELECTED OBLIGATION

Each following contract is copied exactly from the current selected graph. Shared original objects, simultaneous choices and quantified thresholds are part of the obligation.
'''
intro=r'''\section{Current dependency audit: the initial analytic gates and exact selected consumers}
\label{sec:dependency-audit-v38}

\paragraph{Status and classification.}
'''+esc(f'This version adds {new} human proof claims, for {total} cumulative claims. The underlying Alpoge–Claude Lean proof is accepted as fully checked and correct. The complete human RH/Dirichlet-GRH reconstruction remains unfinished.')+r'''
Exactly one whole selected leaf closes:
\texttt{BASE\_THETA\_CUSPIDAL\_EXTENSION}. All 121 selected
nodes and all logical edges remain. RH reaches 101 nodes and
unrestricted Dirichlet GRH reaches 110. There are now 33 open
coupled leaves: 22 C, 9 B and 2 D. All 245 historical compound
targets in 107 groups remain. These counts are not completion
percentages or a proof of absolute minimality.

\begin{center}\small
\begin{tabular}{cp{0.80\textwidth}}
A & A direct published application with original hypotheses checked.\\
B & An independently reconstructible elementary or moderate argument; proof status is separate.\\
C & A substantial or deep argument still requiring reconstruction.\\
D & An unresolved point in our human understanding of the source.\\
\end{tabular}
\end{center}
Checked A applications are completed internal inputs. The two open
D leaves remain \texttt{AD\_VANISH\_K\_MATCH} and
\texttt{HOST\_RIGID\_S}; neither alleges a formal error.

\paragraph{The actual quotient has finite volume.}
FV1--FV11 identify the original group with
$\operatorname{Res}_{F/\mathbb Q}U(J)$, including the actual adelic
topology and rational subgroup. Splitting over the CM extension
gives a general linear group, hence connected reductivity. The
real center is a product of circles; rational characters vanish
because conjugation inverts the determinant character.
Borel's Lemma 5.5 and Theorem 5.6(i) in \emph{Some finiteness
properties of adele groups over number fields} (1963) therefore
apply. Theorem 5.1 gives the required finite adelic classes.

Haar uniqueness and a countable partition of two a.e. fundamental
domains prove the full original \texttt{FiniteVolume2} for every
supplied Haar measure and domain. No probability normalization
replaces the original quotient measure. Each actual target
$W_i$ admits its \texttt{FinPair}, chosen before all $t,x$.
For compact-open $K$, the exact group
\[
 \Gamma_s=\{\gamma_\infty:\gamma\in G(\mathbb Q),\
                         \gamma_f\in sKs^{-1}\}
\]
is arithmetic. Each original open level contains such a sublevel.

\paragraph{The initial seed bound has no Hilbert-space circularity.}
SBD1--SBD4 prove full enveloping-center finiteness directly from
the initial highest-weight equations in the original frame.
Commutator swaps give triangular word spanning. A polynomial in
the adjoint action of a generic diagonal element removes every
nonzero weight. In a remaining ordered word the upper factor
annihilates the seed; a nonempty lower-only product cannot have
weight zero. Thus every central element acts by its diagonal
scalar. This precedes Hilbert realization and keeps the exact
\texttt{gelf} length $k+1$ and right-fold derivative order.

SBD6--SBD8 identify the exact original transvection subgroup as
\[
 a\longmapsto 1+\eta a\xi\xi^*J,\qquad
 \eta\in E^{-}\setminus\{0\},\quad \xi^*J\xi=0.
\]
It is the additive adele group, with rational subgroup $F$.
For compact-open finite $B$, a real lattice parallelepiped $Q$
gives the literal fundamental domain $Q\times B$. This turns
the source's \texttt{ZCusp} integral into the real transvection
average at the same finite level.

Milne's \emph{Algebraic Groups}, Theorem 25.1 and Proposition
17.60, give $P=P(\lambda)$ and $N=U(\lambda)$ for every proper
rational parabolic. In the actual unitary representation,
Hermitian weights pair $m$ with $-m$. A nonzero top positive
weight vector is isotropic, is fixed by $N$, and supplies a
central transvection in $N$. A rational central flag and
descending exponential-coordinate reduction prove compactness
of the real unipotent arithmetic quotient. Fubini now converts
the zero central-transvection average into the zero full
$N$-constant term. All proper rational parabolics are covered.

SBD12 checks Miller--Schmid's Theorem A on the actual arithmetic
component: connected reductive rational group, compact real
center, arithmetic subgroup, smoothness, moderate growth in a
faithful norm, full-center finiteness, and every rational cusp.
Exponent-one decay bounds a Siegel set. The finite rational
cover in their equation (2.8), with each conjugated arithmetic
group and translated cusp condition checked, bounds the full
real component. Finite adelic classes then give exactly
\[
 \forall i,t,x\ \exists C_{itx}\ \forall g:\qquad
             |U_{itx}(e_i)(g)|\le C_{itx}.
\]
Uniformity in $t,x$ is neither claimed nor needed.

FV's finite pairs and this bound feed the complete inherited
SPR multiplicity map, exact lowest-type restriction and linear
lifting. SBD14--SBD16 complete the original all-parameter theta
maps and the selected base extension on the same $R$, with no
new eventual threshold. Common geometric readings, rational
tests and actual base rows remain separate. The stronger
universal quotient-height \texttt{CuspRapidDecay} for arbitrary
multiplicity forms is not a consequence asserted here.

\paragraph{The original selected completion and cotangent comparison.}
CRW1--CRW21 retain the original $h=0,a=n=4,g=0$ point,
\texttt{Kap}, $T$, \texttt{TWPl/TWAut} and paired $J$.
The odd space is zero; \texttt{Sel1} need not vanish.
On normalized coefficient data $O\twoheadrightarrow K$,
for $f:B\to K[[t]]$, $f(s)=t$ and $\mathfrak p=\ker f$,
locality and coefficientwise lifting give
\[
 B/\mathfrak p=K[[t]],\qquad
 \mathfrak m_B=\mathfrak p+(s),\qquad
 O^\circ=\widehat{O[[S]]_{(\varpi)}}.
\]
This is the actual coefficient DVR with residue $K((t))$,
mapping to the original $\widehat{B_{\mathfrak p}}$.
The original full-block span condition gives a split absolutely
irreducible residual determinant. Chenevier's Theorem 2.22(i)
then supplies its full determinant representation. No $4!$
inversion is used, so $\ell=3$ is retained. Polarization,
continuity, closed ideals and every \texttt{NonSS} field are
checked independently on that representation.

For the original coefficient derivations, finite generators
give $\alpha(\mathfrak m_B^j)\subset t^{j-1}L$ for a fixed
lattice $L$. The polarized cotangent-to-Selmer injection and
the coupled selected \texttt{B1/B2} bound give
$D_0=4[L^+:\mathbb Q]+4q$ cotangent generators on the supplied
limit. Successive approximation constructs the actual
$O^\circ[[X_1,\ldots,X_{D_0}]]$ presentation and the
\texttt{presOut0/GalOut} and $h=0$ \texttt{ChainAbs}
dimension comparisons. Standard commutative-algebra imports
have separate exact applicability certificates.

The original \texttt{Raw} producer still needs actual
\texttt{S4}, patched rings/maps/modules with \texttt{S5}
support, and coefficient/pro-$\ell$ descent. Ordinary/control,
type/neat levels, four Hida endpoints and all-level same-$J$
\texttt{HasAut} remain. Both Links, fixed $\iota$, complete
\texttt{CohP/LocCFT/N4} and the common coefficient threshold
are preserved.

\paragraph{The first division identity on the same realization.}
DI1--DI21 prove first \texttt{DivDef3} on CSR's exact updated
$R,F,Y,Z,C,sEE$. Original readings, \texttt{Pins/Holds}, the
full nonzero stored chain, all five real-group predicates and group tie
remain inputs. The additional \texttt{RowPairInt} premise
supplies the actual pairs and finite translates on the original
scaled measures and domains. This is a sufficient refinement,
not the whole original theorem from its original premises alone. Finite Weil transformation of the vacuum and
commutation with creators give the polynomial character law.
Translation of the actual integral proves the level identity
at the nonzero stored vector. Compact polynomial averaging,
the original \texttt{HarishChandraModules} premise and an
explicit finite interpolation argument then kill the equivariant
level defect on the entire smooth tensor product.

For \texttt{RowProj}, self-adjointness of the actual finite-group
central idempotent makes the two literal \texttt{ipM} scalar-witness
sets equal. If the set is empty, both chosen values are zero;
if nonempty, a nonzero tensor norm proves uniqueness. The measure
stays exactly $n_P^{-1}$ times the original quotient measure on
the same domain. Composite row identities and the exact finite
integral-lattice descent give the first theta record's
\texttt{li/span/lat}.

The common datum, nonzero chain and group tie are not constructed
by this identity theorem. Generic multiplicity-pair integrability, explicitly
\texttt{RowPairInt}, is still required; the source passes
from coset growth to global-height growth through an unreconstructed
polynomial unitary reduction theorem. Consequently the initial highest-weight seed bound does not
prove the broader sufficient \texttt{CuspRapidDecay} premise.
The stronger second \texttt{DivRows3} theta square remains separate.

\paragraph{Final cut and next priority.}
The original ten-input final interface remains. RH and
two-primary targets retain I/II/V; unrestricted Dirichlet GRH
also retains III, SeedIV and the original chains. The established
$401$, $\lfloor x^{400}\rfloor$ and $1/2+9\epsilon$ endpoints
keep their scopes.
'''+esc(cfg['next_local_priority'])+r'''

\paragraph{Every remaining selected obligation.}
Each following paragraph is the full current contract in the graph.
'''
(AUD/'audit_intro.txt').write_text(plain);(AUD/'audit_intro.tex').write_text(intro)
tex=intro+'\n\\begin{description}[style=nextline]\n'
for i,n in enumerate(records,1):
 tex+=f"\\item[{i}. {esc(n['id'])} --- {n['category']}] {esc(n['title'])}. {esc(n['contract'])}\n\n"
 plain+=f"\n{i}. {n['id']} — {n['category']} — {n['title']}\n\n{n['contract']}\n\n"
tex+='\\end{description}\n'+r'''
\paragraph{Validation and continuity.}
All predecessor claims, source arrays and dependency edges are
preserved. Independent mathematical reviews bind the new proof,
provenance and closure bytes. The current audit governs historical
frontier statements; DEX11 still governs historical RF16.
Draft TeX checks syntax and references, with no PDF or Lean replay.
'''
plain+='''VALIDATION AND CONTINUITY

All predecessor claims, source arrays and mathematical edges are retained. Independent mathematical reviews bind every new proof and its source/closure metadata. Release validation checks exact remaining contracts and reachability, predecessor bytes, pinned source ranges, review bindings and draft TeX syntax/references. No PDF or Lean replay is produced. DEX11 still governs historical RF16. The current audit and additive scope updates govern historical frontier descriptions.
'''
(AUD/'main.tex').write_text(tex);(AUD/'audit.txt').write_text(plain);(ROOT/'RH_dependency_audit_v0_38.txt').write_text(plain)
print('Audit written:',len(plain.split()),'words;',len(records),'exact remaining contracts.')
