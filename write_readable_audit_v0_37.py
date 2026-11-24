#!/usr/bin/env python3
"""Write the self-contained v0.37 audit and every exact remaining contract."""
from pathlib import Path
import json
ROOT=Path(__file__).resolve().parent;AUD=ROOT/'dependency_audit_v0_37'
cfg=json.loads((ROOT/'increment_v0_37.json').read_text());reg=json.loads((AUD/'remaining_leaf_register.json').read_text())
records=reg['records'];new=cfg['expected_new_claims'];total=1770+new
def esc(s):
 return ''.join({'\\':r'\textbackslash{}','_':r'\_','&':r'\&','%':r'\%','$':r'\$','#':r'\#','{':r'\{','}':r'\}','~':r'\textasciitilde{}','^':r'\textasciicircum{}','≤':r'$\le$','≥':r'$\ge$','→':r'$\to$','∩':r'$\cap$','κ':r'$\kappa$','λ':r'$\lambda$','χ':r'$\chi$','𝒞':r'$\mathcal C$','Ψ':r'$\Psi$','ε':r'$\varepsilon$','−':r'$-$'}.get(c,c) for c in s)
plain=f'''RH AND DIRICHLET-GRH HUMAN RECONSTRUCTION — v0.37
22 November 2026
Source commit: 7cbf7a0c32fca1badf05931879a37c3f8a2b03b4

STATUS

This version adds {new} independently reconstructed human proof claims, bringing the cumulative ledger to {total}. The underlying Alpoge–Claude Lean proof is accepted as fully checked and correct. This audit concerns the completeness of its human reconstruction. The human RH and Dirichlet-GRH proof remains incomplete.

The main completed endpoints are the original smooth-representative and fixed-level Sobolev producers; the full bounded-holomorphic multiplicity-space map; the exact selected CountII first-order bound with exponent 4[L+:Q]+4q; and the finite common-selected realization/Bundle assembly consumers. The two initial analytic producers—boundedness of the actual extremal theta function and the target finite-volume fundamental domain—now form the precise residual analytic cut. The completed assembly consumes them and does not produce them.

The selected sufficient dependency graph has 121 nodes. RH reaches 101 and unrestricted Dirichlet GRH reaches 110; their union is the whole selected graph. It retains 34 open coupled leaves: 23 C, 9 B and 2 D. No additional whole selected leaf is closed in this version, because the newly completed source theorems lie inside broader coupled producer contracts. All 245 historical compound targets in 107 groups, all predecessor claim fields/source arrays, and all selected logical edges are retained. These counts are neither completion percentages nor an absolute minimality theorem.

CLASSIFICATION

A: a direct published-theorem application with its original hypotheses and normalizations checked.
B: an elementary or moderately difficult argument that can be reconstructed independently; status separately records whether it is complete.
C: a substantial or deep argument still requiring reconstruction.
D: a possible gap in our human understanding of the source; not an allegation of a gap in the accepted formal proof.

The two open D leaves are AD_VANISH_K_MATCH and HOST_RIGID_S. Completed arguments may be B while still consuming C producers. We distinguish proving a consumer theorem from supplying every input to that theorem. The newly checked A application is the finite local decomposition/inertia theorem in CFO_LOCAL_DECOMP; it is an internal support node rather than a new open top-level leaf.

I. THE ORIGINAL SMOOTH REPRESENTATIVE AND MULTIPLICITY MAP

SPR1–SPR13 start from the same original finite pair and its quotient measure nu=(mu restricted to F)_*autMk. RQC already supplies the regular representation and compact local L1 bounds. No alternative Haar scale, quotient or representative convention is introduced.

The basic compact L1 estimate makes the representative map continuous into L1(K), for each compact K. Compact-set integral tests detect equality almost everywhere. This justifies parameter integrals and continuous averaging without asking for one exceptional null set uniform over all parameters. Averaging by a continuous compactly supported kernel gives a continuous representative, and averaging inside the original open level approximates every vector fixed by its finite subgroup while preserving that same fixed condition.

Point evaluation is first defined on the dense subspace with continuous representatives. Compact-uniform bounds let it extend as a continuous linear functional on the Hilbert closure. This is a bounded functional for each point, not an unjustified claim that the point-functional family is continuous in operator norm.

The explicit one-dimensional identity is
  v = integral_0^s (1/s) rho(c(t))v dt
      - integral_0^s ((s-t)/s) rho(c(t))dv dt.
Its iteration gives a finite sum of cube averages of ordered Hilbert derivative words. For the product Theta(t)=c1(t1)...cr(tr), the subset I={{i1<...<ik}} contributes the derivative d_ik...d_i1 and the product of the exact weights 1/s or -(s-tj)/s. This reversed selected-word order is essential; no Lie derivatives are commuted. The weights and list are chosen before the derivative maps, invariant smooth domain and vector.

Combining those averages gives ONE continuous representative assignment R. Smoothness of all curve products is stable under translation and every ordered derivative, by adding a derivative variable and differentiating a joint smooth family. Continuous representative uniqueness then transfers the Hilbert derivative to the actual pointwise derivative. Consequently every right-fold derivative of Rv represents the corresponding Hilbert derivative of v. SPR13 is the full original SmoothRep.exists_smooth_repr, retaining invariance under the supplied U intersect Gf, not merely some existential replacement level.

ASB1–ASB6 supply the original analytic chart and local Sobolev input used in this construction. A basis of the actual Hermitian Lie algebra is chosen one place at a time. Cayley coordinates and the inverse function theorem give the ordered exponential chart. For each small adelic shift x, one finite part a_x belongs to U intersect Gf and is independent of the cube parameter. Its reparametrization has a uniform inverse-Lipschitz bound. Averaging that bound over one compact positive-Haar neighborhood converts cube integrals to Haar integrals, using only left Haar invariance. The endpoint one-dimensional Sobolev inequality iterates with the same noncommuting derivative order.

ASB7–ASB12 give the complete rational-point multiplicity bound. A compact set of finite adeles has one integer denominator. The original tensor-product topology permits the same conclusion after a finite field-basis decomposition. An integral basis and the inverse complex-embedding matrix bound each integral coordinate by the actual house. Counting bounded integer coordinate arrays gives a polynomial bound.

For the original group of rank n over its CM field E, an admissible exponent is
  N = 2 [E:Q] n^2.
If gamma*y=x*u*o and gamma0*y=x*u*o0, the injection
  gamma -> gamma gamma0^(-1)
has image x*u*(o o0^(-1))*u^(-1)*x^(-1). The denominator is fixed from x and the compact Omega Omega^(-1) before u,y; u has trivial finite component. Its archimedean entries are bounded by a fixed multiple of the literal normInf(u)^2. Thus the rational count has one exponent before x and is uniform in u,y. Rank zero is treated separately, with exponent zero and 0^0=1 as in the source.

Unfolding the same fundamental domain converts this count into an L2 integral bound. ASB14 proves the exact original order of choices:
  original data and U -> N and finite word list S -> x and C_x -> F,psi,u.
The resulting inequality is
  |psi(xu)| <= C_x normInf(u)^N sum_(l in S) ||d_l F||_2.
It holds for every permitted continuous representative psi. The joint argument has no cycle: ASB3/4 feed SPR13; SPR13 feeds ASB14; later SPR claims consume ASB14.

SPR14–SPR21 apply this construction to the already reconstructed Hilbert multilinear map. Uniqueness gives one pointwise multilinear map T on the original model smooth spaces, at one common finite level. Every derivative is the value at the corresponding updated tuple. The fixed-level inequality gives one exponent before all tuples and all derivative words. The original central scalar theorem supplies z-finiteness; the original closed-orbit cusp theorem supplies the full all-transvection/Haar/domain ZCusp condition and genuine cusp. No arbitrary ambient L2 class is restricted to a measure-zero subgroup.

For evaluation continuity, filter each finite derivative list by the chosen slot, preserve its order, and use the bounded Hilbert multilinear map. This produces exactly the source Sobolev2 bound. A Hamel-basis extension supplies the required ambient algebraic functional; the bound is asserted on the original smooth vectors, without claiming Hilbert-norm boundedness on the ambient space.

All five original IsMultMap fields—aut, cusp, lev, equiv and cont—are now proved. SPR21 is the full BackForm.exists_multMap on its exact supplied bounded HolForm, target FinPair and separate seed ZCusp. Its extremal value is the original seed by continuous representative uniqueness.

SPR22 proves exact lowest-type restriction from equality at one tuple with every component nonzero: compact irreducibility gives an algebraic orbit span in each slot, and the actual frame conjugation transports the two equivariance laws. SPR24 proves full linear theta lifting on arbitrary source vector spaces by Hamel-basis choice and the actual bilinear integral on range(ext). It does not require finite dimension or injectivity of ext.

SPR25 assembles the family for every i,t on the same R, once the actual target FinPair and initial extremal seed bound are supplied. The original open level is checked by integrality of the conjugated matrix and its inverse and congruence at every prime in L.Pg union L.Q. Norm P kills the residue field, so both flag conditions and the residual subgroup condition hold. The same weak stored-choice rule activates the stored predicate without identifying separate existential witnesses.

II. THE EXACT SELECTED FIRST-ORDER COUNT

CFO1–CFO21 close the selected B1 supplier for the SAME full-block h=0,a=n=4,g=0 Kap produced by CCH. This is precisely the object already carrying Choice and B2. The proof does not replace it by a better-adapted object and does not infer Sel1=0 from g=0.

The selected dualN estimate retains the source's entire later representation class: one constant is chosen before m; the eventual N threshold is uniform over every admissible rep-prime satisfying its stated finite Zl premise. The auxiliary determinant-kernel and local fixed-vector arguments are checked with the original truncated coefficient module. No unlisted dependence on the later representation is introduced into the constant.

The actual ArSys and Counts packets are built on the original Taylor–Wiles prime family under the unchanged complete CohP. The local decomposition quotient is identified with the procyclic residue Galois group. The only new published import consists of Milne, Algebraic Number Theory v3.08, Theorem 7.58(a), Proposition 8.10 and Proposition 8.13(b). Their hypotheses are checked on finite Galois subextensions of the chosen algebraic closure, finite places, complete discrete-valued completions, finite perfect residue fields and normal transition subgroups. CFO11 proves the inverse-limit passage and fixes arithmetic Frobenius as 1 in the profinite integers. It never treats an infinite extension as a complete DVR. This import supplies neither LocCFT nor global duality or ordinary automorphic existence.

The local/global cardinality cancellation is exact. Put d=[L+:Q], q=T.q. At rank four the local ordinary exponent is
  m(4(d'_v+1)+6(1+d_v))+C_v.
The sum over ell-adic places contributes m(10d+10|V_ell|). The real-place and ordinary-normalization factors remove m(6d+10|V_ell|). The q new centralizers contribute 4mq, and old N4 turns the distinguished old place into a constant. The final exponent is therefore
  m(4d+4q)+C.
Only allowed units, including 2, are inverted; ell=3 is included. This is the literal selected T.B1(Kap,4[L+:Q]+4T.q).

The resulting coupled rule supplies one original Choice witness together with B1 and B2 on that very witness. It does not prove the universal arbitrary-Kap FirstOrderDualArithmeticBound or obstruction statement. Both original rank-four Links, fixed iota, the one common coefficient threshold and the same ideal J remain. The outstanding CountII producers are ordinary/control/separating arithmetic fibers and type/neatU/TThetaEx; four Hida endpoints; all-level same-J HasAut; and h=0 Raw propagation. Complete CohP, LocCFT, N4 and all original side conditions remain explicit.

III. THE COMMON SELECTED REALIZATION AND BUNDLE

CSR1–CSR22 reconstruct the original finite assembly on the same R. The column theorem chooses one face and one ReadC before any later TwArgs. The initial period choice may be zero; the later selected period is transported literally, so this is not a hidden nonzero-period existence assertion. Both word maps and the actual basis maps are kept where the later period installation requires them.

The actual evaluation placement uses the supplied EvalTieT and models_HE on the original selected level subspace of MMap. With nP the cardinality of the original finite subgroup and c the original positive evaluation scalar, choose
  kappa=(c*nP)^(-1/2).
The resulting semilinear extension obeys nP||sEE(v)||^2=||v||^2 on the specified level subspace and preserves the actual good-subspace condition. The algebraic complement is not assigned an unproved global norm bound.

The source's inactive scalar/error update changes only absent parts. On a nonzero selected eigenspace, the retained MultEq support identifies the same scalar; on a zero rational component its projector is zero. This preserves both actual row Gram matrices and all thirteen reading maps. The exact updated DivDef3 output remains an explicit original supplier. The selected period, spectral point/scalar, rational exponent data, character and instance casts then give every RealIn and RealTB field.

The actual lower-map cancellation uses the real norm identity, and the row-side construction retains both pde and pde-prime contractions. Finite carrier selection preserves the already chosen eigensystems and all-embedding logLam data; it supplies record fields from those inputs. CSR21–CSR22 check every Bundle, BTw, BWit and BunU field on the same R, including EvP/ParEv threshold order and the original side and row packets.

The remaining realization inputs are now explicit: the actual common q/RXs/geometric half and Read/ReadL; host/frame data; MultEq nonzero-part support; the exact updated DivDef3; eigensystem/carrier/parts and all-embedding logLam; HD with the original d3b; and NEb. Original rational tests and actual base rows remain. The fact that these supplied records can be assembled compatibly does not construct them.

IV. FINAL CUT AND NEXT PRIORITY

The original ten-input final interface is unchanged. Its complete global assembly consumes the compatible family, original second layer and duties, local installation, denominator/retained-defect, period-height, local-gain and spectral producers. Those upstream objects and estimates remain in the exact contracts below.

RH and two-primary targets retain Cases I/II/V. Unrestricted Dirichlet GRH additionally retains CaseIII, SeedIV and the original chains. The unchanged VWinAt(chi,401), floor(x^400) and 1/2+9epsilon endpoints retain their established scopes.

'''+cfg['next_local_priority']+'''

The continuation notes give exact pinned source locators for the next analytic, CountII and common-construction tasks. They are planning aids; they do not add closure claims.

EVERY REMAINING SELECTED OBLIGATION

Each following contract is copied exactly from the selected dependency graph. Shared original objects and quantified thresholds are part of the obligation.
'''
intro=r'''\section{Current dependency audit: original pointwise maps and selected first-order bounds}
\label{sec:dependency-audit-v37}

\paragraph{Status and classification.}
'''+esc(f'This version adds {new} human proof claims, for {total} cumulative claims. The underlying Alpoge–Claude Lean proof is accepted as fully checked and correct. The human RH/Dirichlet-GRH reconstruction remains incomplete.')+r'''
The selected sufficient graph retains 121 nodes and 34 open coupled
leaves: 23 C, 9 B and 2 D. No additional whole selected leaf is closed;
the new work completes substantial nested original producers.
All 245 historical compound targets in 107 groups and every selected
logical edge remain. These counts are not completion percentages.

\begin{center}\small
\begin{tabular}{cp{0.80\textwidth}}
A & A published application with all original hypotheses checked.\\
B & An elementary or moderately difficult independent reconstruction.\\
C & A substantial or deep reconstruction obligation.\\
D & An unresolved point in our human source understanding.\\
\end{tabular}
\end{center}
The two D leaves, \texttt{AD\_VANISH\_K\_MATCH} and
\texttt{HOST\_RIGID\_S}, do not allege a formal error.

\paragraph{Complete original pointwise realization.}
SPR1--SPR13 reconstruct the actual smooth-representative producer
on the same finite pair and literal quotient measure. Compact local
$L^1$ bounds give continuous averaging and bounded evaluation
functionals. The exact identity
\[
 v=\int_0^s s^{-1}\rho(c(t))v\,dt
       -\int_0^s\frac{s-t}{s}\rho(c(t))dv\,dt
\]
iterates to a finite cube sum, keeping the selected derivative words
in their original reversed order. No noncommuting derivatives are
interchanged. One representative assignment is smooth along every
curve product, and every pointwise derivative represents the same
ordered Hilbert derivative, on the same finite level.

ASB1--ASB14 supply the actual one-place chart, its cube/Haar
comparison, the local Sobolev bound, the finite-tensor denominator,
and the complete rational-point count. An admissible exponent is
$2[E:\mathbb Q]n^2$. The denominator is chosen before the
archimedean translate and rational orbit point. Unfolding gives
\[
 |\psi(xu)|\le C_x\,\mathrm{normInf}(u)^N
                         \sum_{l\in\mathcal S}\|d_lF\|_2,
\]
with $N,\mathcal S$ before $x,C_x$, and these before $F,\psi,u$.
The dependency order is ASB3/4, then SPR13, then ASB14, then
the later SPR claims; it has no cycle.

SPR14--SPR21 produce the same pointwise multilinear map and all
five original \texttt{IsMultMap} fields. Cusp closure retains the
full transvection/Haar/domain quantifiers. The central scalar action
gives the exact pointwise central-finiteness condition. Filtered
derivative words give the required Sobolev evaluation functional;
its extension to the ambient vector space is algebraic, without
an asserted Hilbert-norm bound there.
This is the full original \texttt{BackForm.exists\_multMap} on
bounded \texttt{HolForm}, the original \texttt{FinPair}, and the
separate seed \texttt{ZCusp}.

SPR22--SPR25 give exact lowest-type restriction and generic linear
theta assembly for every original $i,t$ on the same $R$.
The open principal level retains the actual conjugating matrix,
integrality of it and its inverse, and both finite flag sets.
The remaining analytic suppliers are precisely the \emph{initial}
bound on the extremal theta function and the \emph{target}
finite pair. Post-Hilbert growth cannot justify an earlier bound.
Separate geometric readings, rational tests and base rows remain.

\paragraph{Exact selected first-order arithmetic.}
CFO1--CFO21 prove selected \texttt{B1} on the very same
$h=0,a=n=4,g=0$ witness already carrying CCH's \texttt{Choice}
and \texttt{B2}. The \texttt{dualN} constant precedes $m$ and
its eventual $N$ threshold is uniform over every permitted
representation. The actual \texttt{ArSys/Counts} use unchanged
\texttt{CohP}, \texttt{LocCFT} and local guards.

The only new published import is Milne's finite
decomposition/inertia theorem: \emph{Algebraic Number Theory}
v3.08, Theorem 7.58(a), Proposition 8.10 and Proposition 8.13(b).
Finite Galoisness, finite places, complete discrete-valued
completions, perfect residue fields and normal transitions are
checked. CFO11 proves the absolute inverse-limit passage.

With $d=[L^+:\mathbb Q]$, the local sum contributes
$m(10d+10|V_\ell|)$, the real and ordinary-normalization
factors remove $m(6d+10|V_\ell|)$, and the $q$ new centralizers
contribute $4mq$. Old $N4$ contributes only a constant. Thus
\[
                  \text{final exponent}=m(4d+4q)+C.
\]
This is the literal selected \texttt{B1}; $\ell=3$ is included.
It is coupled with \texttt{Choice/B2} on one witness, not a
universal arbitrary-\texttt{Kap} result. In particular $g=0$
does not imply \texttt{Sel1}=0. The ordinary/control/type
producer, four Hida endpoints, all-level same-$J$ \texttt{HasAut}
and $h=0$ \texttt{Raw} remain, for both original Links with
fixed $\iota$ and one common coefficient threshold.

\paragraph{Finite common-selected assembly.}
CSR1--CSR22 prove the original columns, one \texttt{ReadC}
before later \texttt{TwArgs}, and actual period/evaluation
placement. The original normalization is
\[
 \kappa=(c n_P)^{-1/2},\qquad n_P\|sEE(v)\|^2=\|v\|^2
\]
on the specified original level subspace.
The inactive scalar/error update preserves both row metrics
and all thirteen reading maps. Exact real and side transports,
both contraction maps, and finite carrier choices give every
\texttt{Bundle/BTw/BWit/BunU} field with original
\texttt{EvP/ParEv} threshold order.

The actual common geometry and readings, host/frames,
\texttt{MultEq} support, updated \texttt{DivDef3},
eigensystem/carrier/parts and all-embedding \texttt{logLam},
\texttt{HD} with original \texttt{d3b}, and \texttt{NEb}
remain original suppliers. Initial zero periods are replaced
by the actual later periods; no nonzero period is inferred
from this record choice. Rational tests and base rows remain.

\paragraph{Final cut and next priority.}
The original ten-input final interface and all common objects
remain. RH and two-primary targets retain I/II/V;
unrestricted Dirichlet targets additionally retain III,
SeedIV and chains. The original $401$, $\lfloor x^{400}\rfloor$
and $1/2+9\epsilon$ bounds keep their scopes.
'''+esc(cfg['next_local_priority'])+r'''

\paragraph{Every remaining selected obligation.}
Each paragraph is the full current contract in the selected graph.
'''
(AUD/'audit_intro.txt').write_text(plain);(AUD/'audit_intro.tex').write_text(intro)
tex=intro+'\n\\begin{description}[style=nextline]\n'
for i,n in enumerate(records,1):
 tex+=f"\\item[{i}. {esc(n['id'])} --- {n['category']}] {esc(n['title'])}. {esc(n['contract'])}\n\n"
 plain+=f"\n{i}. {n['id']} — {n['category']} — {n['title']}\n\n{n['contract']}\n\n"
tex+='\\end{description}\n'+r'''
\paragraph{Validation and continuity.}
All predecessor claims, source arrays and dependency edges are
retained. Independent mathematical reviews bind the new proof,
source and metadata bytes. The current audit governs historical
frontier descriptions. DEX11 still governs historical RF16.
Draft TeX checks syntax and references only; no PDF or Lean
replay is produced.
'''
plain+='''VALIDATION AND CONTINUITY

All predecessor claims, source arrays and mathematical dependency edges are retained. Independent mathematical reviews bind every new proof and its source/metadata bytes. Release validation checks all selected contracts and reachability, the predecessor manifest, source ranges, review bindings and draft TeX syntax/references. No PDF or Lean replay is produced. DEX11 still governs historical RF16. The current audit and additive scope updates govern historical frontier descriptions.
'''
(AUD/'main.tex').write_text(tex);(AUD/'audit.txt').write_text(plain);(ROOT/'RH_dependency_audit_v0_37.txt').write_text(plain)
print('Audit written:',len(plain.split()),'words;',len(records),'exact remaining contracts.')
