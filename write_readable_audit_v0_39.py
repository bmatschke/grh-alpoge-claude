#!/usr/bin/env python3
"""Write the current audit with every exact open contract and no implied closures."""
from pathlib import Path
import json
ROOT=Path(__file__).resolve().parent;AUD=ROOT/'dependency_audit_v0_39'
cfg=json.loads((ROOT/'increment_v0_39.json').read_text());reg=json.loads((AUD/'remaining_leaf_register.json').read_text())
records=reg['records'];new=cfg['expected_new_claims'];total=cfg['predecessor_claim_count']+new
def esc(s):
 return ''.join({'\\':r'\textbackslash{}','_':r'\_','&':r'\&','%':r'\%','$':r'\$','#':r'\#','{':r'\{','}':r'\}','~':r'\textasciitilde{}','^':r'\textasciicircum{}','≤':r'$\le$','≥':r'$\ge$','→':r'$\to$','∩':r'$\cap$','κ':r'$\kappa$','λ':r'$\lambda$','χ':r'$\chi$','𝒞':r'$\mathcal C$','Ψ':r'$\Psi$','ε':r'$\varepsilon$','−':r'$-$','/':r'/\allowbreak{}'}.get(c,c) for c in s)
plain=f'''RH AND DIRICHLET-GRH HUMAN RECONSTRUCTION — v0.39
22 November 2026
Source commit: 7cbf7a0c32fca1badf05931879a37c3f8a2b03b4

STATUS

The entire original S4 limit-system construction and the full original CoreBC-to-Raw pro-ell descent are now reconstructed. The exact integrability needed for the actual row pairs is also supplied, removing the additional RowPairInt premise from the first division identity. The original level-zero side and moved-reading constructors are reconstructed on their original given data, with the precise extra eta agreement retained when passing to full ReadL.

There are {new} new proof claims and {total} cumulative claims. The underlying Alpoge–Claude Lean proof is accepted as fully checked and correct. The complete human RH/Dirichlet-GRH proof remains unfinished; this audit measures the reconstruction, not formal validity.

No additional whole selected leaf closes in this version. All 33 open compound obligations remain: 22 C, 9 B and 2 D. Several major nested producers inside them are now complete. The selected graph retains all 121 nodes and 161 logical edges: RH reaches 101 nodes, unrestricted Dirichlet GRH reaches 110, and their union reaches the entire graph. All 245 historical compound targets in 107 scope groups remain with additive scope updates. A compound leaf stays open until every original simultaneous duty is supplied on its actual common objects. These counts are not completion percentages or a claim of absolute minimality.

CLASSIFICATION

A: direct application of a published theorem, with the exact hypotheses checked.
B: elementary or moderately difficult argument independently reconstructible; proof status is recorded separately.
C: a genuinely substantial argument still requiring reconstruction.
D: possible gap in our human understanding of the formal source, not an allegation of an error in the accepted formal proof.

The current open register has no A leaves: the checked published applications are completed internal inputs. The two D leaves remain AD_VANISH_K_MATCH and HOST_RIGID_S. Every remaining selected contract appears verbatim below. The current audit governs older frontier descriptions preserved in the cumulative manuscript and archive.

I. EXACT INTEGRABILITY FROM THE ORIGINAL SMOOTH CUSP PREMISES — RPI1–RPI15

The decisive source fact is the order of the growth quantifiers. IsAutFunSm supplies one exponent N before every differential word D. On each actual arithmetic component, the original smooth function therefore satisfies
  |R_D f_s(u)| <= C_(D,s) ||u||^N.
The constants may depend on D and the finite component s; the exponent does not. RPI1 proves this using the inherited second-kind chart smoothness and an explicit faithful matrix norm. It uses the exact arithmetic subgroup Gamma_s obtained from an original compact-open finite sublevel.

RPI2–RPI6 identify the source cusp integrals precisely. For a positive-rank isotropic frame C, the original NI is the adelic unipotent radical of the unitary parabolic stabilizing im(C). In a rational Witt decomposition U + W + U', its elements are the explicit upper-unitriangular block matrices n(A,B) with B+B*=0 and top-right correction -A*J_W A/2. Thus the source generating conditions, topology, rational subgroup and Haar integrals refer to the actual radical. Finite adelic approximation and a real lattice domain turn the original NI cusp condition into a real radical average at the same component.

Every proper rational parabolic is included. Write P=P(lambda) and N=U(lambda). The largest positive cocharacter weight space U is nonzero and isotropic. P stabilizes it; the unitary radical N_U lies normally inside N. Its zero constant term, the compact arithmetic quotient of N/N_U and Fubini give the zero N-constant term. The same argument applies after every right derivative because differentiation takes place over a compact unipotent quotient. The published cocharacter and relative-root inputs are Milne, Algebraic Groups (2017), Theorem 25.1, Proposition 17.60 and 25.16–25.22, with the exact rational reductive group and fields checked.

RPI7–RPI10 then prove the needed decay argument independently. On a compact unipotent arithmetic quotient, a mean-zero smooth function has its value at the identity controlled by first derivatives along bounded paths. On a generalized Siegel set C_l A_epsilon C_r, choose a simple positive root alpha. Its maximal-parabolic radical is contracted by conjugation with a^(-1), by a factor bounded by a constant times alpha(a)^(-1). Iterating the compact mean-zero estimate gives, for every k,
  |f(l a r)| <= A_k alpha(a)^(-k) ||a||^N.
The compact left sets enlarge to B_alpha^k C_l; they remain fixed after k is chosen. Each application starts afresh with the already differentiated function. Moving coefficients are not differentiated, and the original uniform N still applies at the kth step.

Compact real center makes the rational simple roots span the split directions. Put R(a)=max(1,max_alpha alpha(a)); the fixed faithful weights give ||a|| <= C R(a)^d. Choosing alpha with largest value and k >= d(N+m) yields decay of order m on the Siegel set. The only reduction-theory import is the qualitative finite rational Siegel cover and its root setup in Miller–Schmid, On the rapid decay of cuspidal automorphic forms, equations (2.2)–(2.8), arXiv:1106.2149. Each rational translate has its conjugated arithmetic subgroup and cusp conditions checked. Finite adelic classes then bound every original smooth cuspidal function on the whole original adelic group.

This proof does not use Miller–Schmid Theorem A, full enveloping-center finiteness, the source growth_iff conversion or a polynomial unitary reduction theorem. It proves the exact boundedness needed here from the stronger uniform derivative growth already present in the original definition. It does not assert the stronger universal source CuspRapidDecay statement in its global quotient height.

RPI12–RPI14 apply boundedness to the actual multiplicity spaces. Mult is the algebraic span of IsMultMap maps, so each tuple value is a finite sum of bounded continuous functions. The good part is a subspace of that same Mult. A finite residual action is the original chosen finite right translate multiplied by the original inverse flag character, or the literal default zero when no lift exists. Its character has modulus one by an independent finite-character argument. All required products are bounded and continuous.

The inherited FV theorem gives finite volume for every original Haar measure and fundamental domain. Consequently the exact RowPairInt holds for every b,t,w,c,v,v-prime,g on the same MY0, the same fd0, and precisely
  mu_b = ofReal(nP(lv2,b)^(-1)) nu0.
Neither a probability normalization nor a replacement model is introduced. RPI15 now feeds this supplier into DI1–DI21. The first literal DivDef3 follows from its original premises alone: original readings, Pins/Holds, the stored nonzero IsItW chain, all five stated real-group predicates, group tie and rational positivity remain. The formerly additional RowPairInt is discharged. The empty/nonempty scalar-witness argument for the actual ipM remains valid without adding existence of a Schur scalar. The stronger second DivRows3 theta square remains separate.

II. THE ORIGINAL SIDE AND READING CONSTRUCTORS — RDR1–RDR22

These claims reconstruct two original endpoints, exists_side_reading_level_zero and read_of_moved, on their actual given geometric and comparison data. Their scopes are broader than a single convenient reader, and narrower than the existence of the whole common family. The first chooses one Side0 before every subsequent Read. The second works with each supplied Side0. Their conjunction gives the same ReadPk with all five original pins.

The local Hermitian-lattice construction is explicit. Take the original coefficient space and all prescribed local coordinate tests, define the simultaneous localization submodule by those tests, and impose the original distinguished Gram form. The two row frames are proved invertible using the actual primitive positive row data, generalized-Hecke primary projectors and the exact quotient metric. No semisimplicity statement for an unrelated finite-group action is substituted. A basis is lifted through the original involutively semilinear range, so every off-distinguished metric and coefficient twist matches the source.

The side is built in two stages to avoid circularity. The first auxiliary Side0 identifies the original rational-row test set, whose definition is independent of the not-yet-chosen lattice. The actual lattice is then defined from that fixed set and installed into the final Side0. Its goodness is proved with exactly the source meaning; no stronger HLat fullness theorem is inferred.

The lift-space map j_W is also literal. The supplied MjTie range property lifts the original bL/FW.j map through the original eW. The positive nP norm identity makes eW injective, giving uniqueness and the exact target coordinates. Thus the original map, norm scale and integral carrier remain together.

RDR13–RDR20 install every moved-reader field: finite levels, row and lift identifications, exact Mj tie, type quotients and their occurrences, the trivial base idele character, period ratios, the original used tuples and unused-chain vanishing, coordinate metrics, integral sets and centers. All twelve output ties hold simultaneously on the same R,F. The coordinate identifications come only from the supplied equalities, not from arbitrary isomorphisms.

There is one precise boundary at full ReadL. The named endpoints yield Read plus RationalReadingWithoutCongruence. To obtain full ReadL, the original guard is still required:
  o.eta(j,v)=q.eta(j,v) for every 1<=j<=m and every place v.
Together with Moved.eta this is exactly the remaining etaJ field. Arbitrary Over does not imply the guard. RDR22 proves the guarded constructor, not an unconditional ReadL theorem.

The remaining shared producer is therefore more specific: build the actual q/o/Moved/Fits realization, ChT/LfT/Reps comparison packet, primitive Holds/rational tests and eta agreement on one R,F. The level-zero side and moved-reader algorithms themselves no longer need reconstruction. The full BASE_THETA_READINGS leaf remains open because it also demands those actual inputs, the original family/eventual quantifiers, same Bundle and all phase-one/base-row ties.

III. THE ENTIRE ORIGINAL S4 LIMIT SYSTEM — LIM1–LIM19

LIM18 proves the full source theorem:
  for every original T:TWGrp, T.ProL implies Nonempty(Lim T).
This holds for every prime ell, including 3. It is not restricted to the selected rank-four point, and no original Lim field is omitted.

First, the exact ambient-relative PL residual is identified with the intrinsic pro-ell residual of the open normal subgroup H. Taking finite normal cores proves equality of the two intersections. Compactness gives the finite-quotient criterion: PL(H) lies in an open normal V if and only if the image of H in the finite quotient is an ell-group. The quotient by this residual is pro-ell; continuous functoriality and equality under surjective full-preimage maps are proved independently.

The finite-generation and finite-Hom bounds in the actual TWGrp produce one finitely generated profinite cover Pi and surjections pi_N to every original group at level N. Choose one ultrafilter containing every tail. In each finite quotient Pi/V, the images of the closed kernels ker(pi_N) have finitely many possibilities, so one value is selected on an ultrafilter-large set. These values are compatible. Their inverse limit gives a closed normal K, the quotient G=Pi/K and the exact kernel stabilization
  eventually: ker(pi_N) V = K V.
The resulting pi_o, global map h, eta, epsilon and distinguished involution are then installed on this same G.

The delicate local step uses the original PhiCond with its literal quantifier over every open subgroup. Finiteness of the relevant Hom sets gives stabilization of entire homomorphisms into each finite quotient. Thus, for each fixed finite quotient, one eventual set works for every local element and every original place. A collection of unrelated pointwise limits would not prove this; LIM12–LIM14 explicitly supply the full uniform local-map fields.

The same ultrafilter and finite quotients give the auxiliary ph and ta elements. Original Nq congruences and finite ell-power orders force their tame relation to become exact commutation in the limit. The outgoing ph and ta values are the original sg and identity. LIM18 lists and verifies every field: common cover, topology, finite generation, ultrafilter, all pi_N, pi_o, G,h, modH, distinguished ct, ker_lim, p_lim, both local convergence fields, ph/ta limits, commutation and both outgoing equalities. All finite intersections are taken inside one fixed ultrafilter.

LIM19 applies the full result to the exact matched pro-ell rank-four data and supplies CRW's formerly given Lim. The inherited cohomology bounds now apply to this actual object. The same B1 constant is chosen before m and each permitted eventual N set belongs to that ultrafilter. The g=0 simplification remains attached to the chosen Kap; it does not make the full first-order Selmer space vanish.

IV. FULL TWQUOT AND COREBC-TO-RAW DESCENT — PQL1–PQL21

Let P=PL_Gamma(H). PQL4–PQL5 construct each actual quotient Gamma/P, the full descended global object, and the complete TWQuot. The old level maps, both local-map families, eta, epsilon, c and tame elements descend together. The kernel-lifting clause is proved by correcting a chosen lift with an element of the original level-map kernel. Finite-Hom bounds are preserved by injective pullback, PhiCond uses the same bound, and the quotient system satisfies ProL. The original system is not presumed pro-ell.

Determinant descent is done for the full polynomial law, not merely its trace. Chenevier's Lemmas 1.19, 1.21 and 2.33 provide, respectively, the determinant-kernel/factorization criterion, Cayley–Hamilton ideal inclusion, and finite-quotient factorization of a continuous determinant over a discrete ring. The hypotheses are checked for the actual profinite group algebra and each coefficient reduction. No residual irreducibility, reducedness or inversion of n! is needed for these lemmas.

PQL8 proves closedness of the determinant kernel in exactly the original two-parameter topology, using the coefficient ideals m^a and open normal group subgroups. Every generic polynomial coefficient is tested in each discrete reduction, and separatedness forces the original coefficient to vanish. This is stronger than checking D(g)=1 on group elements.

PQL9 then proves [k]-1 belongs to the actual closed Cayley–Hamilton ideal for k in PL. In a finite group/coefficient quotient, the characteristic polynomial of an element h in H reduces to (X-1)^n. Cayley–Hamilton makes x-1 nilpotent up to a nilpotent coefficient ideal; hence it is nilpotent in the required quotient. In the commutative subalgebra generated by x, the ideal (ell,x-1) is nilpotent. Repeated ellth powers push 1+(ell,x-1)^b into 1+(ell,x-1)^(b+1), so x has ell-power order. The continuous image of H is a finite ell-group and kills PL. This proves the exact ideal membership in every original neighborhood. The full determinant law and all Pair fields therefore descend.

The original point, representation, Kap and truncated cocycles descend with their exact local conditions. The finite field image of the local coefficient ring kills its maximal ideal, so the point is unipotent on H in characteristic ell; no old O-surjects-onto-K premise is inserted. For a truncated affine cocycle, take the joint kernel of its representation and cocycle. After an ell-power kills the representation, an additional ell-power kills the additive cocycle. This supplies the finite ell-group quotient needed to kill PL. The same argument applies to the first-order square-zero coefficient algebra used in Sel1/Sel2.

PQL15 preserves both counting bounds. B1 uses pullback injections and the same boundary identifications; its one constant precedes every truncation m. B2 pulls back an entire admitted array, uses the original common coefficient and primitive relation, and descends the resulting relation. The original eventual N conditions and same C are unchanged.

PQL16–PQL17 retain literally the same B,J,K,f, eigenvalues and supplied automorphic modules. The same finite-level rings, maps, operators, ranks, free bases and common exponents satisfy the descended TWAut because their defining polynomials and rel1/rel2 identities agree. This transports a supplied all-level system; it does not construct the limiting patched module or prove S5.

The closed augmented ideals require a further direction check. PQL18 proves the needed inverse-image inclusion by lifting every generic Cayley–Hamilton coefficient and every local pair generator, and checking both the coefficient and group-ideal closure parameters. At a field-valued point this gives a surjection from the descended algebra onto the original one. Therefore original non-semisimplicity implies descended non-semisimplicity. Only this direction is claimed. The original discriminant stiffness is transported through identical lifted trace matrices. PQL20 then applies CoreBC to the actual quotient packet and transports the result back to the original prime and the same ideal J, proving the complete original CoreBC implies Raw theorem.

V. THE CURRENT MINIMAL SUFFICIENT CUT AND NEXT WORK

The next arithmetic branch is normalized Core itself: construct the actual limiting RRObj/RMaps and patched modules, then prove the S5 support dimension, fiber and annihilator contracts. In parallel, reconstruct Core-to-CoreBC coefficient normalization and its Unit parameter. The completed CRW comparison, full S4 and full pro-ell descent can then be used together. Reconstructing those completed consumers again would not advance the remaining support producer.

This is only the selected Raw subproblem. CountII still requires original ordinary/control/separating arithmetic fibers and type/neatU/TThetaEx; all four Hida endpoints; and all-level same-J HasAut. Both rank-four Links, fixed iota, ell=3, full CohP/LocCFT/N4, all local guards and one common coefficient threshold remain intact. There is no change of ideal between the ring, density, point, endpoint, twist and P1core duties.

The other high-contribution branch is the actual common geometric/comparison/test datum. Its reader and first-division constructors are now available; what remains is to supply their original hypotheses simultaneously and then the actual rational tests/base rows and stronger second theta square where required. Host/frame, MultEq, original chain/group, parts/logLam, HD/d3b, NEb, local NBuilt/NdSpec, denominator/defect/height/gain/spectral estimates and compatible second-layer selection remain in the selected graph.

RH and two-primary targets retain Cases I/II/V. Unrestricted Dirichlet GRH additionally retains III, SeedIV and the original chain propagation/descent. The optional AQ route remains optional. Historical RF16 remains governed by DEX11. The classified exact contracts below determine the present sufficient route; none is removed merely because its record-assembly consumer has been proved.

VI. EVERY REMAINING SELECTED OBLIGATION

'''
intro=r'''\section{Current dependency audit: exact row inputs, original readers, full limits and descent}
\label{sec:dependency-audit-v39}

The entire original \texttt{S4} and full
\texttt{CoreBC}$\Rightarrow$\texttt{Raw} pro-$\ell$ descent
are now reconstructed. Exact original row-pair integrability
discharges the extra \texttt{RowPairInt} premise of first
\texttt{DivDef3}. The original given-data side/read constructors
are reconstructed, with the precise $\eta$ guard retained for
full \texttt{ReadL}. The formal Lean proof is accepted as fully
checked and correct; this is still a partial human reconstruction.

'''+f'There are {new} new proof claims and {total} cumulative claims. '+r'''
No additional whole selected leaf closes. The 33 open compound
leaves remain $22\mathrm C+9\mathrm B+2\mathrm D$; their nested
producer obligations are narrower. All 121 selected nodes and
161 logical edges remain. RH reaches 101 nodes, Dirichlet GRH
110, and together they reach the full graph. All 245 historical
compound targets in 107 scope groups remain. These are scope
counts, not completion percentages or an absolute minimality claim.

\paragraph{Classification and exact scopes.}
A means a checked published application; B an independent
elementary or moderately difficult argument; C substantial
reconstruction; D unresolved human understanding of the source.
There are no open A leaves. The two D leaves remain
\texttt{AD\_VANISH\_K\_MATCH} and \texttt{HOST\_RIGID\_S}.
The current audit governs historical frontier statements.

\begin{longtable}{@{}p{0.19\linewidth}p{0.38\linewidth}p{0.36\linewidth}@{}}
\toprule
New claims & Completed original-input contribution & Remaining producer boundary\\
\midrule\endhead
RPI1--RPI15 & Exact row integrability and first division output without the extra analytic premise & Original common geometry, chain, predicates and group tie; second division square.\\
RDR1--RDR22 & Original level-zero side, moved reader and common pins; full reader with its $\eta$ guard & Actual common comparison/test datum and that guard.\\
LIM1--LIM19 & Entire original S4 and actual selected limit input & Limiting patched rings/modules and support.\\
PQL1--PQL21 & Full original quotient packet and CoreBC-to-Raw pro-$\ell$ descent & Normalized Core patching/S5 and coefficient normalization/Unit.\\
\bottomrule
\end{longtable}

\paragraph{Uniform growth closes the exact analytic supplier.}
RPI1 retains the source's decisive order of quantifiers:
\[
 \exists N\ \forall D,s\ \exists C_{D,s}\ \forall u:
           |R_Df_s(u)|\le C_{D,s}\|u\|^N.
\]
RPI2--RPI6 identify literal \texttt{NI} with the actual
unitary parabolic radical, construct its exact auxiliary
arithmetic quotient, and obtain every proper rational-parabolic
cusp integral, including all right derivatives. For a general
parabolic, the highest positive cocharacter weight space is
isotropic; its stabilizer radical lies normally in the given
radical. Compact-quotient Fubini gives the full constant term.
Milne's Theorem 25.1, Proposition 17.60 and relative-root setup
are applied with the original reductive group and field checked.

The remaining derivative estimate is proved independently.
Mean zero on a compact unipotent quotient bounds evaluation by
first derivatives along bounded paths. On a Siegel set,
conjugation by $a^{-1}$ contracts the appropriate radical by
$\alpha(a)^{-1}$. Repeated fresh applications give
\[
 |f(lar)|\le A_k\alpha(a)^{-k}\|a\|^N.
\]
The compact left sets enlarge only with $k$; moving coefficients
are never differentiated. The same original $N$ works at every
stage. Compact real center and the fixed faithful weights give
$\|a\|\le C R(a)^d$, with $R(a)$ the largest simple-root value
or one. Choose that root and $k\ge d(N+m)$. The qualitative
finite rational Siegel cover of Miller--Schmid, equations
(2.2)--(2.8), with every rational translate checked, and the
inherited finite adelic classes now give global boundedness
of each original function. Their Theorem A is not used;
no full-center or global-height conversion is assumed.

The actual multiplicity span and chosen finite translates
therefore give bounded continuous products. The exact original
finite-volume theorem implies integrability for every actual
$b,t,w,c,v,v',g$ on the same model and
\[
 (R.\mathrm{fd0},\mu_b),\qquad
 \mu_b=\operatorname{ofReal}(n_P^{-1})R.\nu_0.
\]
RPI15 supplies first \texttt{DivDef3} from its original premises
alone. It retains the five original real-group predicates,
readings, \texttt{Pins/Holds}, stored nonzero chain and group
tie. Universal quotient-height \texttt{CuspRapidDecay} and the
stronger second \texttt{DivRows3} are not asserted.

\paragraph{The two original reading producers.}
RDR builds an explicit simultaneous localization lattice and
the exact distinguished Gram frame. Original positive row
data, generalized-Hecke primary projectors and quotient metrics
give the actual invertible frames. A basis through the original
involutively semilinear range retains every coefficient twist.
A two-stage \texttt{Side0} construction fixes the rational-row
test set before defining the final lattice, avoiding circularity.
The original lift map $j_W$ is uniquely lifted through the
original $e_W$ using its range and positive $n_P$ norm identity.

RDR12 proves the whole level-zero endpoint, choosing one
\texttt{Side0} before every reader. RDR20 installs all original
\texttt{Read} fields and twelve simultaneous ties, including
levels, row/lift maps, types, periods, used tuples, coordinate
metrics, integral sets and centers. RDR21 gives their common
\texttt{ReadPk} and five pins. These named endpoints add no
premise beyond their original given data. Full \texttt{ReadL}
additionally retains the exact original condition
\[
 o.\eta(j,v)=q.\eta(j,v)\qquad(1\le j\le m,\ \text{every }v).
\]
RDR22 combines it with \texttt{Moved.eta} to install the
remaining \texttt{etaJ} field. Arbitrary \texttt{Over} does
not imply this equality. Actual \texttt{Fits/Moved},
\texttt{ChT/LfT/Reps}, primitive tests and common geometry
remain producers; no new family threshold is supplied.

\paragraph{The whole original limit theorem.}
LIM18 proves
\[
 \forall T:\mathrm{TWGrp},\qquad
        T.\mathrm{ProL}\Longrightarrow\mathrm{Nonempty}(\mathrm{Lim}(T)).
\]
The exact relative residual is identified with the intrinsic
pro-$\ell$ residual by finite normal cores. The original
finite-generation and finite-Hom bounds give one finitely
generated profinite cover $\Pi$ and all-level surjections
$\pi_N$. One ultrafilter containing every tail selects the
kernel images in every finite quotient. Their compatible limit
is a closed normal $K$, with $G=\Pi/K$, and
\[
 \ker(\pi_N)V=KV
 \quad\text{eventually for each }V\triangleleft_o\Pi.
\]
The original \texttt{PhiCond} stabilizes whole homomorphisms
into finite quotients. Thus each required eventual comparison
is uniform in every local element and every place. The same
ultrafilter gives the tame elements; their exact commutation
uses finite $\ell$-power order and the original congruences.
Every original \texttt{Lim} field is installed together.
The selected cohomology consumer now has an actual constructed
limit, retaining the constant before the truncation and all
original eventual sets. This supplies no patched module or S5.

\paragraph{Descent with the original coefficients and ideal.}
PQL constructs the entire \texttt{TWQuot}, including kernel
lifting, local maps, finite bounds and \texttt{ProL}. The full
polynomial determinant law descends. Chenevier's Lemmas 1.19,
1.21 and 2.33 are checked for the actual profinite group algebra
and discrete coefficient quotients; they require neither
residual irreducibility nor inversion of $n!$.

The determinant kernel is proved closed in both original
topology parameters. In a finite group/coefficient quotient,
Cayley--Hamilton and residual polynomial $(X-1)^n$ make
$x-1$ nilpotent. The commutative ideal $(\ell,x-1)$ is
nilpotent, and repeated $\ell$th powers show that $x$ has
$\ell$-power order. Hence the pro-$\ell$ residual is killed
in every quotient, proving the exact closed-ideal membership.
Full polynomial laws, all Pair fields, the actual point,
Kap and truncated cocycles descend. Pullback and exact
boundary identifications retain B1/B2, their constant order
and original eventual level conditions.

The same $B,J,K,f$, finite-level rings and supplied modules
give the descended \texttt{TWAut}. Exact inverse-image
inclusion for the closed augmented ideals yields a surjection
from the descended specialized algebra onto the original one.
This proves the needed one-way non-semisimplicity implication,
not an equivalence. Trace matrices retain discriminant
stiffness. Applying \texttt{CoreBC} and transporting its
conclusion back proves full \texttt{CoreBC}$\Rightarrow$
\texttt{Raw}, on the original ideal. Prime $\ell=3$ remains
included. Normalized Core and coefficient normalization/Unit
are separate remaining producers.

\paragraph{Next priority.}
'''+esc(cfg['next_local_priority'])+r'''

RH retains I/II/V; unrestricted Dirichlet GRH additionally III,
SeedIV and the original chains. The optional AQ route and the
DEX11 correction of historical RF16 retain their scopes.
Each following paragraph is the complete current selected contract.
'''
(AUD/'audit_intro.txt').write_text(plain);(AUD/'audit_intro.tex').write_text(intro)
tex=intro+'\n\\begin{description}[style=nextline]\n'
for i,n in enumerate(records,1):
 tex+=f"\\item[{i}. {esc(n['id'])} --- {n['category']}] {esc(n['title'])}. {esc(n['contract'])}\n\n"
 plain+=f"\n{i}. {n['id']} — {n['category']} — {n['title']}\n\n{n['contract']}\n\n"
tex+='\\end{description}\n'+r'''
\paragraph{Validation and continuity.}
Every predecessor claim field, source array and dependency edge
is retained. Independent mathematical reviews bind the new proof,
provenance and closure bytes. Draft TeX checks syntax and
references, with no PDF or Lean replay. The current audit governs
historical frontier descriptions; DEX11 still governs RF16.
'''
plain+='''VALIDATION AND CONTINUITY

Every predecessor claim field, source array and mathematical edge is retained. Independent mathematical reviews bind all 77 new proof claims and their source/closure metadata. Release validation checks exact current contracts, both final routes, predecessor bytes, pinned source ranges, review bindings and draft TeX syntax/references. No PDF or Lean replay is produced. DEX11 still governs historical RF16. Current scope updates govern older frontier descriptions without deleting historical proof bytes.
'''
(AUD/'main.tex').write_text(tex);(AUD/'audit.txt').write_text(plain);(ROOT/'RH_dependency_audit_v0_39.txt').write_text(plain)
print('Audit written:',len(plain.split()),'words;',len(records),'exact remaining contracts.')
