#!/usr/bin/env python3
"""Create the current human audit and a verbatim register of all selected open contracts."""
from pathlib import Path
import json,collections
ROOT=Path(__file__).resolve().parent;AUD=ROOT/'dependency_audit_v0_32'
cfg=json.loads((ROOT/'increment_v0_32.json').read_text())
reg=json.loads((AUD/'remaining_leaf_register.json').read_text())
g=json.loads((AUD/'obligation_map.json').read_text())
records=reg['records'];cats=collections.Counter(x['category'] for x in records)
intro=r'''\section{Current dependency audit: actual size and rank, local operators, and the base theta frontier}
\label{sec:dependency-audit-v32}

\status{Version 0.32 accepts the underlying Alp\"oge--Claude Lean
proof as fully checked and correct. The new work closes the original
construction-class size and rank obligations and the specified global
local calculations. It also narrows the actual base-theta construction.
The human reconstruction remains incomplete. Every remaining selected
obligation is classified below; an unresolved human reading is not a
claim of a gap in the formal proof.}

\subsection{What is now proved on the original objects}

The most useful change is in design existence. DEX7 had reduced it
to three compatible inputs on one class: original \texttt{DesignChoices},
the closed \texttt{TuSize} implication, and the closed original
\texttt{RankM} formula. DSZ10 and RMP11 now prove the latter two
on the exact construction class. Thus only the actual common-family
construction remains inside this selected design cut. This is a
statement about the dependencies of the human proof, not an assertion
that its most difficult construction has become elementary.

The class is essential. Let
\[
 \mathcal A=\texttt{cls}(Q,\mathrm{Lk},E),\quad
 \mathcal C'=\texttt{WithChN}(\mathcal A\cap\mathcal G),\quad
 \mathcal C_{\rm des}=\texttt{WithTw}(\texttt{WithSm}(\mathcal C')),
                                                               \tag{AU32.1}
\]
where $\mathcal G$ is the actual target class. Membership in
$\mathcal A$ contains the original \texttt{Link} and \texttt{QOf}
property. Its positivity field permits \texttt{cls\_at}; the
source's \texttt{pick} then gives the very Bundle whose $R$ field
supplies the columns. The same \texttt{Built} witness contains the
actual real-place data. DSZ and RMP use these projections on the
same $D$, level, field, weights, metrics and stored degree variables.
They prove properties of every member of $\mathcal A$.
They do not prove that this class has a member satisfying all the
other required duties.

\paragraph{The degree and prime-size calculation.}
The new finite product comparison is
\[
 0<d_n(\lambda)\le d_\tau(\lambda)
         \left(\max_{a,b}|\lambda_a-\lambda_b|\right)^{pq}.
                                                               \tag{AU32.2}
\]
DSZ2 checks that the source's quantitative gap exceeds the actual
general construction and rigidity threshold in DC1--DC13. DC18--DC19,
with the previously matched Harish--Chandra theorem and the exact
compact-dual Haar normalization, therefore identify the stored row
degree with $d_r(\lambda)$ using the literal \texttt{dsigTie}.
This closes the original $h_3$ slot on every supplied family.

For prime size, use the original family cloud, not a freshly chosen
equally spaced model. Its interior coordinates satisfy
$u_i=v_{i-1}-1/2-\xi_i\Delta$, $\xi_i\in\{0,1\}$.
At distance $d$ the row-to-column factor is at most
$4d/(4d-1)$. Hence the interior logarithmic loss is at most
$\frac{k}{3}(1+\log k)$. The remaining factors give
\[
 \log\frac{V_r(v,-b)}{V_k(u)}\le5kmL.
                                                               \tag{AU32.3}
\]
The factorial factors cancel exactly against the mass ratio.
Combining this upper estimate with QW6's proved lower estimate gives,
for $X_u=(fk)^{-1}\log(D_*/d_*(u))$ and
$C_0=\max(5,C_{YL}+1)$,
\[
 15mL\le X_u\le(7+3C_0)mL
                                                               \tag{AU32.4}
\]
on one late-family threshold. The original $\Gamma_u$ correction
and original prime window then yield
\[
 B^{m/2}\le T_u,\qquad
 \log T_u\le(8+3C_0)mL.
                                                               \tag{AU32.5}
\]
The source's larger constant
$c_T(y)=\max(11,16+3\max(5,y+1))$ is unchanged.
DSZ10 supplies the needed original volume identity on the construction
class from \texttt{Built}/\texttt{RealTied} and RSL1--RSL3.
This proof replaces only the upper comparison needed for
\texttt{TuSize}; it does not assert the stronger full Vandermonde
variation or counting package.

\paragraph{The original class number and rank.}
RMP begins with the actual column lattice $L$:
$L\subset L^\#\subset T^{-1}L$ and $|L^\#/L|=T^{2f}$.
At every one of the $f$ split places over $T$, the original nonzero
prime-order functional gives one nonzero discriminant component.
Duality gives equal lengths to the two components; their total
cardinality forces each length to be one. Choosing the half singled
out by that functional gives the literal self-dual \texttt{overLat}.
The local level fixes a specified nonzero functional, giving
$T^k-1$, rather than the projective-line index.

The actual auxiliary levels and the original genus mass now give
\[
 |\mathrm{cls}_0|=\mu_k\,\mathrm{idxPi}\,(T^k-1)^f.
                                                               \tag{AU32.6}
\]
Two distinct auxiliary primes force the finite rational level
stabilizers to be trivial. The original \texttt{Forms0} value maps
therefore identify the dimension of the actual $\mathrm{Mu}_0$
with this class count times the exact Weyl dimension product.
The stored \texttt{FactDuStar} gives the literal rank identity
\[
                    d_M(u)=d_*(u)(T_u^k-1)^f.
                                                               \tag{AU32.7}
\]
The class-number proof is stronger than its source-facing contract:
it does not need \texttt{GBig}. The rank proof does not use a
theta square, finite-character assertion or metric comparison.
The existing construction-class Bundle supplies its needed columns.

\paragraph{The original local Hecke and congruence calculations.}
GLE1--GLE2 prove every clause of the eventual
\texttt{HidaSetting} from the actual parameter windows and the
lower bound in \texttt{TuSize}. The remaining GLE proofs retain
the same original \texttt{Forms0}, finite field-valued character
and stabilizer identifications. They give the exact lattice
coordinates and
\[
 U_v(B_{w,v})\subset S_w,\qquad D_v(S_w)\subset B_{w,v},
 \qquad U_vD_v=T^{k-1}\quad\hbox{on }M^{\rm ram}.
                                                               \tag{AU32.8}
\]
The finite two-step move calculation includes the line contribution,
the inverse diamond convention, and the character-one comparison
between equal endpoints. The second branch is also exact:
\[
 T^{b_v}S_w\subset B_{w,v},\qquad
 \ell(B_{w,v}/T^{b_v}S_w)
      =\frac{e_wd_S}{k}(|\lambda|+kb_v),
                                                               \tag{AU32.9}
\]
where $|\lambda|$ denotes the signed sum of its entries.
The determinant shift is retained when computing each elementary
divisor. Exact sequences give the one-operator bound, then the
source's original ordered product and its $m$th power give the
complete congruence length bound. No interchange of differently
ordered factors is assumed. Empty unseen-place products are treated
as the identity.

These close five explicit GL6 implication tasks. Together with the
actual second-layer supplier and D3's built-in \texttt{TuSize},
they give the remaining original $N_\lambda\subset S^{\rm ram}$
inclusion used in RSL fullness. The second-layer selector remains
a shared producer. For the global-slope branch, the original three
GL4 slots and the final numerical/lattice assembly remain unwritten.

\subsection{The smaller actual base-theta frontier}

BTH1 proves smooth-topology cyclicity of nonzero smooth vectors in
the irreducible source models. BTH2 then proves that the multiplicity
map is determined by its lowest-type values. These steps make the
continuity needed for uniqueness explicit.

BTH3 proves absolute convergence of the actual base lowest-type theta
integral. The original positive-definite real groups are compact;
the stored finite double-coset representatives give a compact set of
adelic representatives. Unfolding bounds the measure of the prescribed
fundamental domain by that of this compact set. The actual weak Weil
continuity and automorphy fields make the integrand bounded there.
This does not by itself prove a smooth cuspidal target extension.

Once the requisite base extensions and exact source readings are
supplied, BTH assembles the linear map, activates the original weak
choices and constructs the good-projected target map. Its Hilbert
reading uses an explicit tensor witness in the geometric theta law.
One base rational test family supplies both the rational adjoint
image and rational coordinates in the stored target basis.
The finite unitary argument kills the orthogonal complement of the
original good cut without replacing the source idempotent by a
self-adjoint one. This gives the actual base theta square.

BTH13--BTH15 also prove the exact normalization for the source's
already stored Weil action. A continuous adelic unitary character
trivial on rational and split-supported points is trivial; the
Heisenberg scalar lemma and positive split normalization then show
that two full Weil data with the same characters agree on the theta
space. Comparing the original action with the canonical construction,
with its determinant-character twist, gives its required finite
lattice-stabilizer character. The canonical action is therefore
identified with the actual source action where the covariance proof
uses it; this is a proved step, not an additional producer premise.

The exact remaining same-bundle inputs are listed in the register
below. Their principal mathematical parts are the actual geometric
reading, the smooth cuspidal extension of the now-convergent basis
integrals, the simultaneous rational tests, and the original base
rows. They must hold on one selected Bundle with its exact field,
embeddings, Hilbert and rational metrics, level, basis and chosen
maps. Independent models with matching dimensions do not suffice.
The stronger nonbase theta package remains relevant only to its
other consumers, not automatically to this base rank argument.

\subsection{The final theorem interface and the count branches}

The final sufficient interface is unchanged: one compatible
\texttt{DesignExists} and nine \texttt{Closed} predicates,
\[
\begin{gathered}
 \texttt{LinkN},\quad\texttt{LinkEta},\quad\texttt{LinkIRR},\quad
 \texttt{SmallLevelRankEq},\\
 \texttt{TuSize}\Rightarrow\texttt{DGamSize}\Rightarrow\texttt{LinkDIVt},
 \qquad\texttt{ChosenE}\Rightarrow
       (\texttt{NuFullF}\wedge\texttt{MuRank}),\\
 \texttt{LinkG},\qquad\texttt{TuSize}\Rightarrow\texttt{LinkS},\qquad
 \texttt{TuSize}\Rightarrow\texttt{DGamSize}\Rightarrow\texttt{LinkGLOBAL}.
                                                               \tag{AU32.10}
\end{gathered}
\]
All outer thresholds are joined before one family is selected.
The constants $C_{\rm abs}=2$, $C_0=3$, $e_D=2$, $e_L=0$
and the ZW exponent $1/2+9\epsilon$ are unchanged. HX still
uses the original \texttt{VWinAt}$(\chi,401)$ and cutoff
$\lfloor x^{400}\rfloor$.

For RH and targets of power-of-two character order, the selected
arithmetic count route requires I, II and V. General Dirichlet
targets additionally require the actual Case-III/SeedIV/chain
construction. CountII retains all six original \texttt{HidaPropsAlt}
fields and \texttt{P1core} on the same ideal of each of its two
original rank-four Links, after one coefficient threshold.
CountI's fixed field and CountV's Gaussian/quartic host are distinct.
The Case-V exponent $e=1$ is the original twist exponent, not the
unbounded dyadic host exponent. These distinctions survive every
geometric simplification in the present version.

\subsection{Classification and priority}

\begin{description}[style=nextline]
\item[A: matched published application.]
An identified published theorem is applied to the original object,
with all consumed hypotheses checked. The retained HC-Deg, MF and
GV applications remain recorded in their earlier scopes. They do
not become new unproved local claims in this version.
\item[B: independent elementary or moderate reconstruction.]
Some B arguments are complete certificates; the register below
contains only those B proof tasks still unwritten. A theorem name
in the Lean source is not counted as its human proof.
\item[C: substantial construction or proof.]
The exact original target is identified, but its substantial
geometric, analytic, representation-theoretic or arithmetic
producer remains to be reconstructed.
\item[D: incomplete human source understanding.]
The original instance or hypothesis bridge still needs a precise
human identification. This does not question the checked Lean proof.
\end{description}

Prioritize the common original row/theta reading, smooth cuspidal
extension and base rational tests: their construction is shared
with several other period, spectral and specialization consumers.
The next bounded global branch is the actual \texttt{ColVal}
dictionary and its two GL4 slope estimates, followed by the final
\texttt{FamGLmin} assembly. In parallel, the same-ideal rank-four
ordinary Hecke/support producer remains the main independent count
priority. Repeating the now proved size, rank or local length
arguments would contribute less to the final theorem.

The audit records selected sufficient dependencies. Its AND rules
retain the proof of each implication and every actual producer
premise. Shared refinements are navigation links rather than extra
logical implications. All 245 inherited compound continuation records
and their 107 groups remain, with precise current subclaim updates.
Neither their counts nor the selected leaf count is a percentage of
the mathematical work, and no absolute minimality theorem is asserted.

\subsection{Complete current selected obligation register}

The following is the complete open-leaf register for this selected
route. Completed certificates and matched A applications are in the
provenance and published-input registries. Coupled hypotheses below
must be supplied on the same original objects.
'''
def esc(s):
 table={'\\':r'\textbackslash{}','&':r'\&','%':r'\%','$':r'\$','#':r'\#','_':r'\_','{':r'\{','}':r'\}','~':r'\textasciitilde{}','^':r'\textasciicircum{}','Ψ':r'\(\Psi\)','≤':r'\(\le\)','𝒞':r'\(\mathcal C\)','₂':r'\( {}_2\)','→':r'\(\to\)','≥':r'\(\ge\)','∩':r'\(\cap\)'}
 return ''.join(table.get(c,c) for c in s)
tail='\n\\begin{description}[style=nextline]\n'
for i,r in enumerate(records,1):
 tail+='\\item['+str(i)+'. '+r['category']+': '+esc(r['title'])+'.]\n'
 tail+='\\texttt{'+esc(r['id'])+'}. '+esc(r['contract'])+'\n\n'
tail+='\\end{description}\n'
(AUD/'main.tex').write_text(intro+tail)

text='''RH AND DIRICHLET GRH — HUMAN RECONSTRUCTION v0.32
22 November 2026
Current complete-proof dependency audit and continuation guide

STATUS

We assume the Alpoge–Claude formal Lean proof is fully checked and correct. This remains a partial human reconstruction. The current work proves actual original degree/size, class-number/rank and local Hecke/length arguments, and narrows the base-theta producer. It does not yet provide a complete human proof of RH or Dirichlet GRH.

The source is pinned at commit 7cbf7a0c32fca1badf05931879a37c3f8a2b03b4 in https://github.com/CocoSgt/riemann-hypothesis-lean. Every new proof claim has exact source ranges and hashes. No new Lean build or kernel replay is claimed.

1. THE MOST IMPORTANT DEPENDENCY REDUCTION

The design cut previously had three inputs on one construction class: DesignChoices, Closed TuSize, and Closed original RankM. DSZ10 and RMP11 now supply the latter two on exactly that class. The original compatible DesignChoices/common class-member construction remains. This is not an inference of existence from a universal property.

Precisely, A=cls(Q,Lk,E), Cprime=WithChN(A intersect the target class), and Cdes=WithTw(WithSm Cprime), with Bd=Bundle and cT(eps,y)=max(11,16+3 max(5,y+1)). Membership of A supplies Link.pos and QOf; cls_at/pick gives the original Bundle. Its Built witness supplies RealTied, while its R field supplies the original columns. Both new Closed proofs may choose epsilon1=1 and zero transported bounds before the family. Their inner eventual thresholds are allowed to depend on that same family. The common family and its other duties still have to be constructed.

2. ACTUAL FORMAL DEGREES AND THE DIRECT LEVEL-PRIME SIZE PROOF

DSZ1–DSZ3 prove the finite compact/noncompact root-product comparison and match the source gap to the actual general DC1–DC12 existence threshold and DC13 rigidity. The previously checked Harish–Chandra input, with the exact compact-dual Haar normalization, then gives D.dsig(rho)=dimV(rowLam) through the original cdScaleTie and dsigTie. This completes the h3 family slot.

For the actual interior coordinates u_i=v_(i-1)-1/2-xi_i Delta, xi_i in {0,1}, the row-to-column factor at distance d is at most 4d/(4d-1). Its logarithm has a harmonic-sum bound k(1+log k)/3. The other factors are bounded directly by the original windows, yielding log(Vr/Vk)<=5kmL. This uses the actual cloud and does not choose new coordinates.

The mass-ratio factorials cancel the two Weyl denominators exactly. With X_u=log(Dstar/dstar(u))/(fk), C0=max(5,CYL+1), the new upper comparison and previous QW lower comparison give 15mL<=X_u<=(7+3C0)mL eventually. The original Gamma correction has log Gamma<=fk, and the original chosen prime lies in its specified window. Hence B^(m/2)<=T_u and log T_u<=(8+3C0)mL. The source cTmin is larger and remains unchanged.

DSZ10 supplies the only additional original volume identity on the construction class through Built/RealTied and RSL1–RSL3. The proof replaces only the upper estimate needed for TuSize; no full Vandermonde variation/counting theorem is claimed.

3. THE ORIGINAL CLASS NUMBER AND RANK FORMULA

RMP1–RMP8 begin with the literal column lattice L subset Ldual subset T^(-1)L and |Ldual/L|=T^(2f). At each of the f split places over T, the original nonzero prime-order functional gives a nonzero discriminant component. Duality makes the two component lengths equal; the total index forces each to have length one. Selecting the functional's factor constructs the literal self-dual overLat.

The local level fixes a specified nonzero functional. Its exact index is T^k-1, with no projective-line division by T-1. The actual auxiliary indices and original genus mass give |cls0|=massI*idxPi*(T^k-1)^f. Two distinct auxiliary-prime reductions force all finite rational level stabilizers to be trivial. This is a direct proof of ClassNumberFormula_2, stronger than the source-facing statement because GBig is unused.

RMP9–RMP11 use the original Forms0 value maps, coefficient polynomial span, rho shift and finite class set to prove Mu0Tie and literal RankM. FactDuStar matches the exact stored dstar: dM(u)=dstar(u)*(T_u^k-1)^f. Construction-class membership supplies the same Bundle.R, so no separate selector-existence premise remains inside this rank property. Constructing a common class member remains upstream.

4. THE ACTUAL GLOBAL LOCAL CALCULATIONS

GLE1–GLE2 extract all four strict HidaSetting requirements directly from the actual parameter windows and the lower TuSize bound. Eventually m>=4 and T>=b^2; the weights lie in [-2b,2xb], with b>=24x and b>=3N. Full NumsL, upper logT and DlSize are not needed for this consumer.

GLE3–GLE11 retain the original Forms0, finite K-valued character, coefficient embeddings and stabilizer data. They prove exact S/B polynomial-coordinate lattices, both integral up/down maps, the actual DU endpoint/fiber formula and ramified inverse UD=T^(k-1). The second-branch length is exact: length(B/T^b_v S)=e_w*dS*(|lambda|+k*b_v)/k, where |lambda| is the signed sum of weights. The determinant shifts and full dimension dS are retained.

DVR exact sequences bound each normalized operator. Induction over the original ordered product and its mth power identifies the literal Nlam and proves the complete congruence length bound, including the unseen-place empty product. No commutativity of arbitrary factor order is assumed. These completed implications still consume the same compatible second-layer forms and character. That common producer remains in the graph. The three original GL4 slots and final global assembly remain B tasks.

5. THE BASE THETA FRONTIER

BTH proves smooth-topology lowest-type uniqueness and absolute convergence of the actual lowest-type theta integral. The original definite real factors are compact, the stored finite double-coset representatives give a compact adelic representative set, and unfolding gives finite fundamental-domain measure. The actual weak Weil fields make the integrand continuous and bounded there.

The remaining smooth cuspidal extension is a separate substantial requirement. Finite-basis extensions activate the original weak choices and construct the good-projected map. The subsequent exact Hilbert reading, rational adjoint image, finite idempotent kernel argument and original target basis give the base theta square from the precise coupled producer recorded below. One base rational test family serves both rational descent and matrix coordinates. Original base rows remain a separate predicate on the same Bundle.

BTH13–BTH15 prove the required finite-action normalization for the actual source action. The first proves that a continuous adelic unitary character trivial on rational points and split-supported elements is trivial. The Heisenberg scalar lemma and positive split normalization then identify any two full Weil actions with the same characters on the original theta space. Comparison with the canonical construction, after the exact determinant-character twist, gives the original finite lattice-stabilizer character. The canonical model alone would not have supplied this assertion; the comparison is now a written proof.

6. UNCHANGED FINAL AND COUNT INTERFACES

The final sufficient rule still uses one compatible DesignExists and nine Closed predicates: LinkN, LinkEta, LinkIRR, SmallLevelRankEq, TuSize=>DGamSize=>LinkDIVt, ChosenE=>(NuFullF and MuRank), LinkG, TuSize=>LinkS, and TuSize=>DGamSize=>LinkGLOBAL. All transported bounds are joined before selecting one family. Cabs=2, C0=3, eD=2, eL=0 and the ZW window exponent 1/2+9epsilon are unchanged.

HX still uses VWinAt(chi,401) and cutoff floor(x^400). RH and power-of-two-order character targets require Counts I, II and V. Unrestricted Dirichlet targets additionally require the actual Case-III/SeedIV/chain construction. CountII requires all six HidaPropsAlt fields and P1core on the same ideal on both original rank-four Links, after one coefficient threshold. CountI and CountV use different fixed fields. In Case V, e=1 is the twist exponent and does not fix the host's dyadic exponent.

7. CLASSIFICATION AND NEXT PRIORITY

A — Direct application of an identified published theorem, with every consumed hypothesis checked on the original object.
B — An elementary or moderately difficult independent proof, including exact source-instance joins. Completed B certificates are separate from still-unwritten B tasks.
C — A substantial geometric, analytic, representation-theoretic or arithmetic reconstruction with an identified original target.
D — Incomplete human understanding of the exact source instance or hypothesis bridge; not an allegation of a defect in the checked Lean proof.

The retained HC-Deg, Hasse–Minkowski and Tamagawa applications keep their previously checked scopes. An A application is not classified as unresolved merely because the theorem is deep; its hypotheses have to be matched, and that matching is recorded separately.

Prioritize the actual common row/theta reading, smooth cuspidal base extension and rational tests, because their constructions are shared with other period, specialization and spectral consumers. The next bounded global branch is the actual ColVal dictionary and its two GL4 slope estimates, followed by the final FamGLmin assembly. In parallel, the same-ideal rank-four ordinary support/Hida/P1 producer remains the principal independent count branch. The now proved size, rank and local length calculations should not be repeated.

The graph records selected sufficient implications, with proofs of implications distinct from their producer premises. Its refinements do not establish absolute mathematical minimality. All 245 inherited compound continuation records and their 107 groups remain with precise current reductions. None of these counts is a completion percentage.

8. COMPLETE CURRENT SELECTED OBLIGATION REGISTER

Each entry below is an exact open contract from the selected graph. Completed certificates and matched published applications remain in provenance.json and dependency_audit_v0_32/published_applications.json. All clauses referring to a common Bundle or family must be supplied together on that object.

'''
text+=f"Current register: {len(records)} selected open contracts; "+', '.join(f'{v} category {k}' for k,v in sorted(cats.items()))+'. These are overlapping proof contracts, not equally weighted work units.\n\n'
for i,r in enumerate(records,1):text+=f"{i}. {r['id']} — {r['category']} — {r['title']}\n\n{r['contract']}\n\n"
text+='''9. READING FILES AND CONTINUITY

RH_readable_reconstruction_v0_32.tex contains all historical mathematical chapters plus the current audit and new chapters. The archive contains the exact source/proof ledgers, the selected dependency graph, complete remaining-leaf register, inherited target dispositions, independent reviews, validation and continuation checkpoint. Original claim/source fields and historical dependency edges are preserved; updated scopes are additive.

The historical RF16 exponent correction remains the one proved in DEX11. No old proof bytes are silently rewritten. Draft-mode TeX checks syntax and cross-reference resolution; no PDF is generated and no visual layout certification is claimed. Mathematical reviews and source hashes are recorded separately from those syntax checks.
'''
(ROOT/'RH_dependency_audit_v0_32.txt').write_text(text)
print('Current audit:',len(records),'open contracts;',len(text.split()),'words; TeX',len((intro+tail).encode()),'bytes.')
