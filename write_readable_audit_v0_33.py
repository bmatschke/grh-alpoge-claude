#!/usr/bin/env python3
"""Write a self-contained current audit and every exact remaining contract."""
from pathlib import Path
import collections,json,re
ROOT=Path(__file__).resolve().parent;AUD=ROOT/'dependency_audit_v0_33'
cfg=json.loads((ROOT/'increment_v0_33.json').read_text());g=json.loads((AUD/'obligation_map.json').read_text())
records=json.loads((AUD/'remaining_leaf_register.json').read_text())['records'];cats=collections.Counter(x['category']for x in records)
intro=r'''\section{Current dependency audit: original cuspidality, column slopes, and the same Hecke ideal}
\label{sec:dependency-audit-v33}

\status{Version 0.33 accepts the underlying Alp\"oge--Claude formal
proof as fully checked and correct. The new human work proves the
original finite isotropic averaging argument and genuine theta
cuspidality, all three GL4 implications and their FamGLmin assembly,
and the exact Hecke-kernel and single-point support transports.
The human reconstruction is still incomplete. The current register
below states every remaining selected obligation, with its original
objects and quantifiers; category D concerns our understanding of
the formal source, not a claim that the checked proof has a gap.}

\subsection{What this continuation actually supplies}

\paragraph{One finite average on the original kernels.}
FIA1--FIA8 use the original real datum, character, finite frames,
weighted lattice, residue maps, Fock seed and Weil covariance.
Choose once a prime $\mathfrak P$ in the stored nonempty good-prime
set and put $N=\#k(\mathfrak P)>0$. For each original index and
parameter, adelic pair $(h,g)$ and nonzero rational vector $\xi$,
there is a list $a_0,\ldots,a_{N-1}$ such that
\[
 \sum_{j=0}^{N-1}H_{\xi a_j}\omega(h,g)\operatorname{pt}(P)=0
                         \quad\text{for every polynomial }P.
 \tag{AU33.1}
\]
The period is fixed for the datum, and the list is chosen before
$P$. The list may depend on the other parameters. The finite
argument requires only $\xi\ne0$; isotropy is needed in the
constant-term argument which follows. The local phase uses the full
oriented symplectic form, while a raw Heisenberg operator uses its
half. FIA checks the sign and both half-datum guards explicitly.

\paragraph{Convergent constant terms and actual cuspidality.}
For an isotropic $\xi$ write $Z_\xi$ for the original rank-one
transvection group. CTC1 identifies it with $\mathbb A_F$, with
rational subgroup $F$, using $1+(t\xi_0)\xi\xi^*G_T$.
CTC2 supplies the uniform bound on compact Weil orbits from a
common finite level, exact Haar $L^2$ unitarity and an iterated
one-variable Sobolev estimate. CTC3--CTC7 reconstruct the local
character duality, algebraic split-half separation and positive
action on the along coinvariants. For a nonzero rational row the
positive definite source supplies a nonzero Hermitian norm; a
transvection then gives a unit phase different from one times a
positive real scalar. That product cannot be one.

Fourier coefficients on the compact along quotient therefore show
that the exact transvection constant-term functional satisfies
\[
 \mathcal C_\xi(H_{\xi a}f)=\mathcal C_\xi(f),\qquad
 \mathcal C_\xi(f)=\int_{Z_\xi(F)\backslash Z_\xi(\mathbb A)}
                                     \omega(1,z)f(0)\,dz.
 \tag{AU33.2}
\]
Applying it to (AU33.1) gives $N\mathcal C_\xi(f)=0$.
The original definite source has compact rational representatives
from its original finite class presentation. A finite coefficient
basis makes the two-variable kernel continuous and bounded there.
Thus Fubini is justified and the actual theta integral has zero
transvection constants.

CTC11 writes each original isotropic-frame unipotent group in Witt
coordinates as a two-step group of matrices $n(A,B)$, with $B$
skew-Hermitian. Its quotient by rational points is compact, by
successively reducing $A$ and the central $B$ coordinate in adelic
vector quotients. A transvection along any frame column is central.
Haar invariance and Fubini now force the full unipotent constant
term to vanish. Hence CTC13 proves genuine cuspidality of the
original base integral. It does not use the formal convention
assigning zero to a nonintegrable Bochner integral.

The remaining base extension is smaller but still substantial:
smoothness and uniform derivative growth, lowering and prescribed
lowest type, original finite-level/equivariance installation, and
bounded holomorphic realization in the specified Hilbert
multiplicity model. Separately, one original $\mathrm{ioP}$ must retain all
its parameter conditions; this is not the smooth Hilbert extension itself. Same-Bundle geometric readings,
simultaneous rational tests and actual base rows remain separate
coupled producers.

\paragraph{The three original GL4 slots.}
GLS1--GLS3 construct the literal column-value record from the same
supplied forms: original class lattices, conjugate coefficient
embeddings, local polynomial membership at every finite place,
and the exact infinite-place norm. For every supplied ColVal,
GLS6 proves
\[
                     \mu(Q_{c,\tau})=-\frac{\log T}{k}.
 \tag{AU33.3}
\]
This uses the original squared Hermitian slope, its factor two,
the discriminant index $T^{2f}$, and scalar extension without a
hidden finite-index change. GLS4 proves the exact highest-vector
Fock norm by a finite normal-order recurrence; GLS5 uses normalized
Weyl/coefficient lattice duality and Cauchy--Binet for its integral
determinant estimate. These give the original lower slope bound.

For the upper slope, GLS8 applies Banaszczyk's published Euclidean
transference theorem, Theorem 2.1 in \emph{Mathematische Annalen}
296 (1993), 625--635, on the actual positive trace lattice.
Its full rank, dimension, metric and trace/codifferent dual are
checked. The subsequent original class-map and coefficient-norm
arguments give the literal constant $4$, not an unspecified
constant. The primary source and complete hypothesis check are in
\texttt{global\_slope/published\_applications.json}.

GLS13 assembles all eleven original fields
\[
 h_{2b},h_{2v},h_3,h_{Za},h_{Zb},t_{CV},h_W,h_\mu,h_I,h_R,h_B
\]
of $\mathrm{FamGLmin}(D_3(3,\mathcal A),4)$ on the same supplied
second-layer selector and Duty. Earlier RSL/GLE/DSZ/RMP arguments
provide the other fields in their exact scopes. The common second
layer still has to be produced. The final numerical/lattice
implication through \texttt{linkGLOBAL7\_min/items} and
\texttt{link8} still has to be written. It retains
$C_{\rm abs}=2,C_0=3,C_5=4,e_D=2,e_L=0$.

\paragraph{Count II keeps one ideal throughout.}
For each of the two original rank-four Links, JSP constructs the
map from the given universal ordinary ring to the original Hecke
algebra. It writes explicit preimages of every spherical and
ordinary Hecke generator, proving surjectivity. Therefore
\[
          J=\ker(B\longrightarrow\mathbb T)
                        =\operatorname{Ann}_B(M),\qquad
                         B/J\simeq\mathbb T
 \tag{AU33.4}
\]
in the nonzero-module case; if $M=0$ the exact source alternative
is $J=B$. JSP verifies all eight RingProps fields using coefficientwise
polynomial-law tests at separating arithmetic fibers. It proves
the Dense implication with the exact weight and reciprocity
dictionary kept explicit. It also constructs the actual TWBase on
this same module and ideal.

The characteristic-prime argument is the source's one-point NiceI
case. Injective local coefficient extensions preserve kernels;
the normalized full matrix span supplies a nonzero trace
discriminant in every characteristic. Under HasAut and the six
retained arithmetic/patching contracts, the source one-point
support conclusion then gives P1core for the same $J$.
This reconstructs the transport, not the substantial patching
input itself. It works for the allowed coefficient prime $3$.

Still to produce are the original ordinary arithmetic/control data
and separating fibers, the precise reciprocity matching, the four
further Hida endpoints, all-level automorphic modules/HasAut, and
the retained single-point support inputs. The fixed $\iota$
comes first; one coefficient threshold for both Links precedes
every later DVR and every original universal $B,\Lambda$.
The seven properties must hold on each Link's same $J$.
The exact Artin-map/\texttt{IsWtPart} matching is a category D
subobligation within the coupled category C producer. The count
of two D leaves below refers to the selected graph granularity;
it does not suppress this nested source-understanding task.

\subsection{The selected complete-proof cut}

The final interface remains one compatible DesignExists and the
nine original Closed predicates: LinkN, LinkEta, LinkIRR,
SmallLevelRankEq, the TuSize/DGamSize implication to LinkDIVt,
the ChosenE implication to NuFullF and MuRank, LinkG, the TuSize
implication to LinkS, and the TuSize/DGamSize implication to
LinkGLOBAL. The Closed epsilon cutoffs and transport tuple are joined before
selecting one family. Eventual x thresholds may depend on that
supplied family and its class witness, but precede the indices,
places and other variables over which the bound is uniform. The construction-class TuSize and RankM proofs from
version 0.32 remain available; they do not create that class's
compatible member.

RH and the two-primary specialization still use I, II and V.
Unrestricted Dirichlet GRH additionally uses III, SeedIV and the
original chain. The Count-I and Count-V fields and prime scopes
remain distinct; the Count-V twist exponent is not the bounded
host dyadic exponent. The host still uses the original
$\mathrm{VWinAt}(\chi,401)$ and cutoff $\lfloor x^{400}\rfloor$;
the final reconstructed numerical exponent remains
$1/2+9\varepsilon$. The AQ route is an alternative conditional
route with its own arithmetic envelope.

Each remaining selected leaf is classified A, B, C or D. A means
a direct published application with hypotheses checked. Completed
A applications are retained in their registry and are not counted
as unresolved leaves. B means an elementary or moderately difficult
independent reconstruction. C means a substantial deep reconstruction.
D means a possible gap in our human understanding of the source.
A completed conditional argument can have open C producers;
its completion does not assert their existence.

The register now has 35 open leaves: 23 C, 10 B and 2 D.
The three GL4 implication leaves are closed; the theta and Count-II
leaves are narrowed. These are coupled sufficient contracts, not
equal-sized tasks or a percentage of proof completion. All 245
inherited compound targets in 107 groups remain dispositioned.
The 121-node selected graph is rooted in RH and Dirichlet GRH;
13 shared work refinements and eight optional routes remain
separate from its logical AND rules.

\subsection{Priority by contribution to the final theorem}

The next bounded global task is the residual numerical/lattice
assembly from the now complete same-selector FamGLmin package.
It should be reconstructed directly on the source's existing
frame, HN and loss variables, with all constants displayed.
The main shared analytic task is the smooth-growth/lowering and
Hilbert realization of the now cuspidal original theta integral.
This serves the common base reading, small-rank and later
period/spectral branches. The main independent arithmetic task
is the original rank-four ordinary control/arithmetic producer
and all-level same-ideal support construction. JSP identifies
which algebraic transports no longer need to be repeated.

The common recursive/geometric construction, local NBuilt/NdSpec,
the original denominator, retained defect, period, local-gain and
spectral producers remain on the path to both roots. Keep their
bindings visible while working on a bounded subtask. The next
branch should be selected for its effect on these root
dependencies, not for its position at the end of the latest chapter.

\subsection{Every remaining selected obligation}
The following contracts are reproduced from the machine-readable
current register. Their order groups the source's interfaces; it
does not assign equal cost or independent witnesses to them.
'''
def esc(t):
 mapping={'\\':r'\textbackslash{}','&':r'\&','%':r'\%','$':r'\$','#':r'\#','_':r'\_','{':r'\{','}':r'\}',
 '→':r'$\to$','−':r'$-$','≥':r'$\ge$','≤':r'$\le$','ε':r'$\varepsilon$','λ':r'$\lambda$','Ψ':r'$\Psi$','𝒞':r'$\mathcal C$','^':r'\textasciicircum{}','~':r'\textasciitilde{}'}
 return ''.join(mapping.get(c,c)for c in t)
tex= intro+'\n\\begin{description}[style=nextline]\n'
for i,n in enumerate(records,1):tex+=f"\\item[{i}. {esc(n['id'])} --- {n['category']}] {esc(n['title'])}. {esc(n['contract'])}\n\n"
tex+='\\end{description}\n\n'
tex+=r'''\paragraph{Validation and continuity.}
The release preserves predecessor claim fields, source arrays and
mathematical dependency edges. New source and proof ranges are bound
to the pinned commit and independently reviewed. The release
validator checks all inherited source ranges, graph connectivity,
exact remaining contracts, review hashes and draft TeX references.
These checks are not a new Lean replay. Historical RF16 remains
governed by its explicit DEX11 correction; no historical proof
bytes are silently rewritten. The current audit and additive scope
updates govern superseded historical frontier statements.
'''
(AUD/'main.tex').write_text(tex)
plain='''RH / DIRICHLET-GRH RECONSTRUCTION — VERSION 0.33
22 November 2026
MINIMAL COMPLETE-PROOF DEPENDENCY AUDIT: CURRENT SELECTED SUFFICIENT ROUTE

STATUS
We accept the underlying Alpoge–Claude Lean proof as fully checked and correct.
The human reconstruction remains incomplete. This continuation supplies the
original finite averaging and genuine theta cuspidality, all three original
GL4 implications and FamGLmin assembly, and exact same-ideal Hecke/support
transports. Category D concerns human source understanding only.

READING FILES
RH_readable_reconstruction_v0_33.tex contains all historical mathematical
chapters and the new proofs. The complete ZIP also includes every source
locator, claim ledger, review, current graph, old checkpoint and continuation
note. This file gives the complete selected outstanding-contract register.

NEW MATHEMATICAL WORK
'''+''.join(f'{i}. {s}\n\n'for i,s in enumerate(cfg['new_in_this_version'],1))+'''
THE KEY CUSPIDALITY CHAIN
The finite kernel has a nontrivial root-of-unity eigencharacter at one stored
good prime. With N equal to that prime's residue cardinality, the sum of its
first N powers is zero. The original finite Heisenberg translations commute
with every real creation word, so one list annihilates all polynomial kernels
for the fixed other parameters. Original Weil covariance transports that list
to the desired rational direction. No replacement vector or scalar is chosen.

For isotropic xi, the original transvection group is A_F with rational subgroup
F. The along space is isotropic. Compact-orbit bounds and exact Haar measures
make its constant-term functional well-defined. Local character duality,
split-half separation and the datum's positive split scalar give an eigenvalue
different from one for each nonzero rational-row Fourier coefficient. Haar translation
then kills those coefficients. Their separating character algebra proves that
the averaged function is constant along the isotropic direction. Thus every
summand in the finite average has the same constant term, which must be zero.

The original definite source has compact representatives from its finite class
presentation. A finite coefficient basis gives a jointly continuous bounded
kernel and justifies Fubini. The actual integral consequently has ZCusp.
In a rational Witt basis the full original unipotent group has coordinates
n(A,B), with B skew-Hermitian, and a central vector subgroup. Reducing A and
then B modulo rational vectors proves its quotient compact. The transvection
for a frame column is central. Central Haar averaging then forces the full
unipotent constant term to vanish. These are ordinary convergent integrals;
the formal default value for a nonintegrable Bochner integral is not used.

WHAT REMAINS OF THE THETA EXTENSION
Actual smoothness, uniform derivative growth, lowering and prescribed type,
finite-level/equivariance installation, and the bounded holomorphic/Hilbert
multiplicity realization remain. Separately, the original ioP must keep
its universal parameter quantifier, not only a base-parameter witness;
this simultaneous identification is not the smooth Hilbert extension itself. The same-Bundle
readings, simultaneous rational tests and actual base rows remain coupled.

THE GLOBAL SLOPE PACKAGE
The new ColVal uses the original class lattices, conjugate coefficient
embeddings, divided-power polynomial lattice, every finite-place membership
test and the exact archimedean norm. The squared Hermitian slope of each
column is exactly -log(T)/k, using the original discriminant index T^(2f).
The finite normal-order recurrence proves the normalized highest-vector Fock
norm and hook bound. Integral duality and Cauchy–Binet give the standard Weyl
slope estimate. For the upper bound, Banaszczyk's Euclidean transference
theorem is matched to the actual trace lattice and its codifferent dual;
the subsequent original class-map estimate retains coefficient 4.

Published application: W. Banaszczyk, New bounds in some transference theorems
in the geometry of numbers, Math. Ann.296 (1993),625–635, Theorem2.1,p.631.
Primary publisher: https://doi.org/10.1007/BF01445125
The exact lattice/hypothesis check is in global_slope/published_applications.json.
This is a checked A application inside a completed implication; it is not an
unresolved A leaf. The paper gives the Euclidean successive-minima bound;
GLS proves the application-specific field and metric transport.

All eleven FamGLmin(D3(3,A),4) fields now have human proofs on the same
supplied second layer. The actual compatible second layer still has to be
produced. The final linkGLOBAL7_min/items/link8 numerical and lattice join
still has to be written, with Cabs=2,C0=3,C5=4,eD=2,eL=0. The Closed
epsilon cutoff and transport tuple precede the supplied family and class
witness; the eventual x threshold may depend on these supplied objects
but precedes i,u and every place.

THE COUNT-II IDEAL AND SUPPORT BOUNDARY
The map B→T is surjective because every spherical and ordinary generator has
an explicit determinant/character preimage. In the nonzero case its kernel
J is exactly Ann_B(M), and B/J≅T as weight algebras. The zero-module source
alternative is J=B. RingProps and Dense follow from the stated original
arithmetic/control fibers and exact weight/reciprocity data. TWBase uses the
same module, scalar map and ideal; it does not produce the all-level TWAut.

For one NiceI point, finite local coefficient extensions preserve kernels.
The normalized rank-four full matrix span has a nonzero trace discriminant
even at coefficient prime3. Under HasAut and the six printed arithmetic/
patching contracts, the one-point support conclusion gives P1core on this J.
The proof does not replace that substantial support theorem by density.

The remaining producer supplies the original ordinary datum, control and
arithmetic fibers, exact reciprocity, four further Hida fields, all-level
automorphic modules and six retained support inputs. The fixed iota precedes
one common coefficient threshold for both original Links, and that threshold
precedes all later DVRs and actual universal B/Lambda. Separate ideals for
Hida properties and P1 would not satisfy the required joint interface.
The exact artOf/every-map IsWtPart reciprocity matching is a nested category D
subobligation inside this coupled category C producer. The two selected D
leaves below are a count at that graph granularity, not a claim that there
are no other source-understanding tasks inside the coupled contracts.

FINAL INTERFACE AND CLASSIFICATION
One DesignExists plus nine original Closed predicates remain the final
sufficient interface: LinkN,LinkEta,LinkIRR,SmallLevelRankEq,
TuSize→DGamSize→LinkDIVt,ChosenE→(NuFullF∧MuRank),LinkG,
TuSize→LinkS,TuSize→DGamSize→LinkGLOBAL. Join Closed epsilon cutoffs
and the transport tuple before selecting one common family. The eventual
x thresholds may depend on that family and its class witness, but precede
indices, places and the other variables over which the bounds are uniform. The v0.32 construction-class TuSize/RankM results remain
complete; they do not prove compatible class nonemptiness.

RH and two-primary targets require I/II/V; unrestricted Dirichlet GRH also
requires III,SeedIV and the original chain. CountI and CountV retain distinct
fixed fields and prime scopes. CountV's twist exponent is not the bounded
host dyadic exponent. Retain VWinAt(chi,401), cutoff floor(x^400), and the
final numerical exponent 1/2+9epsilon. AQ stays a separate conditional route.

A: direct published theorem application with hypotheses checked.
B: elementary or moderately difficult independent reconstruction.
C: deep argument requiring substantial reconstruction.
D: possible gap in human understanding of the formal source.

There are 35 current selected open leaves:23C,10B,2D, and no unresolved A
application. Three GL4 leaves closed; theta and Count-II leaves narrowed.
These are coupled contracts, not equal-sized tasks or a completion percentage.
All245 inherited compound targets in107 groups remain; the selected logical
graph has121 nodes. Its13 shared work refinements and8 optional routes are
kept outside the sufficient logical AND rules.

PRIORITY FOR THE NEXT CONTINUATION
'''+cfg['next_local_priority']+'''

The bounded global assembly can now connect a fully written FamGLmin package
to the original global loss bound. The analytic extension remains a shared
producer for base rows/small rank and later period/spectral work. The ordinary
arithmetic and patched-support producer is an independent deep branch needed
already by RH. Retain work on common recursive/geometric construction, local
NBuilt/NdSpec and denominator/defect/period/gain/spectral inputs as visible
root dependencies while choosing the next concrete branch.

EVERY REMAINING SELECTED OBLIGATION
The following contracts are reproduced verbatim from the current graph.
'''
for i,n in enumerate(records,1):plain+=f"\n{i}. {n['id']} — {n['category']} — {n['title']}\n\n{n['contract']}\n\n"
plain+='''VALIDATION AND CONTINUITY
Every predecessor claim field, source array and mathematical dependency edge
is preserved. Source/proof ranges are bound to the same pinned commit:
7cbf7a0c32fca1badf05931879a37c3f8a2b03b4.
Independent mathematical reviews bind the final proof/metadata bytes; the
release validator checks continuity, source ranges, exact outstanding
contracts, graph reachability and review bindings. Draft TeX checks syntax
and reference resolution. It generates no PDF and is not a Lean replay.
Historical RF16 is governed by its preserved DEX11 correction. The present
audit and additive scope updates govern superseded historical frontiers.
'''
(ROOT/'RH_dependency_audit_v0_33.txt').write_text(plain)
(AUD/'audit.txt').write_text(plain)
print('Audit written:',len(plain.split()),'words;',len(records),'exact open contracts.')
