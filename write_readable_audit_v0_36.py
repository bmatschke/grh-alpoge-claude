#!/usr/bin/env python3
"""Write the standalone complete selected audit and its manuscript chapter."""
from pathlib import Path
import collections,json
ROOT=Path(__file__).resolve().parent;AUD=ROOT/"dependency_audit_v0_36"
cfg=json.loads((ROOT/"increment_v0_36.json").read_text())
g=json.loads((AUD/"obligation_map.json").read_text())
records=json.loads((AUD/"remaining_leaf_register.json").read_text())["records"]
cats=collections.Counter(n["category"] for n in records)
def esc(t):
    m={"\\":r"\textbackslash{}","&":r"\&","%":r"\%","$":r"\$","#":r"\#","_":r"\_","{":r"\{","}":r"\}",
       "→":r"$\to$","−":r"$-$","≥":r"$\ge$","≤":r"$\le$","ε":r"$\varepsilon$","λ":r"$\lambda$","Ψ":r"$\Psi$","𝒞":r"$\mathcal C$","^":r"\textasciicircum{}","~":r"\textasciitilde{}"}
    return "".join(m.get(c,c) for c in t)
plain="""RH / DIRICHLET-GRH RECONSTRUCTION — COMPLETE SELECTED DEPENDENCY AUDIT
Version 0.36 — 22 November 2026

STATUS AND SCOPE

This version completes the original simultaneous ioP producer, the exact regular quotient and its smooth/cusp/Gelfand suppliers, and the original one-point rank-four Choice together with the obstruction bound for its same chosen zero-dimensional Kap. There are 71 new human proof claims in four chapters and 1770 cumulative claims.

The underlying Alpoge–Claude Lean proof is accepted as fully checked and correct. The human reconstruction remains incomplete: a proved implication on supplied original data does not construct those data. This release does not claim the final RH or Dirichlet-GRH theorem as a complete human proof, and no new Lean build or kernel replay was performed.

This is a connected sufficient-interface audit of the selected human route. It records every selected remaining obligation below, with original object, normalization and quantifier constraints, and preserves all 245 historical compound targets in 107 scope groups. It is not a theorem of absolute minimality or an exhaustive transitive Lean dependency computation. Shared obligations occur once in the selected graph, and optional alternatives remain outside its AND requirements.

The source is pinned at 7cbf7a0c32fca1badf05931879a37c3f8a2b03b4. Every new claim has exact source ranges, a human proof range and an independent review binding. The current audit governs superseded frontier statements in historical chapters without rewriting their proofs.

CURRENT REGISTER

The selected graph still has 121 nodes and 34 open coupled leaves:
A — direct published theorem application with all hypotheses matched: 0 open leaves.
B — elementary or moderately difficult independent reconstruction: 9.
C — substantial or deep reconstruction: 23.
D — unresolved human understanding of the formal source: 2.

No additional whole selected leaf is closed in this version. Several substantive C and B subcontracts inside the theta and CountII leaves are now discharged. The inherited full final-global assembly remains closed. Consequently a constant whole-leaf count conceals substantial mathematical progress; counts are navigation aids, not completion percentages.

The two D obligations are AD_VANISH_K_MATCH and HOST_RIGID_S. They describe an unresolved human match to the formal source, not a defect alleged in the checked Lean proof.

THE NEW MATHEMATICAL WORK

"""+"\n\n".join(cfg["new_in_this_version"])+"""

THE EXACT COEFFICIENT BRIDGE

CFB1–CFB6 construct the coefficient model on the actual c0L, cV and BV. The original coefficient tie gives covariance on rational points. Its basis images extend uniquely over the prescribed complex embedding; the polynomial model has exactly the original VV as its range. Cayley weak approximation, the finite-part triviality and continuity extend the rational identity to every original source-real point. Conjugation uses BV^{-1} g BV in the literal order.

Compact cyclicity is proved for the actual extremal polynomial and the actual VV, rather than postulated as an unnamed intertwiner. This is the precise interface consumed by the Fock construction. It does not replace the coefficient module or norm.

CFB7–CFB13 reconstruct all ArithAt fields and the forced selected lamLdef. Integer endpoint gaps remove the literal floors in the two exponent sequences. The two antitonicity statements, original sign order, and both minor-weight identities are checked. In particular the third determinant exponent is
  x3 = -[(p-q)/2 - e - 1/2],
so its e term has positive sign. The three integer exponents and the coefficient tie are installed on one original R and i before a parameter t is chosen. Compatible existence of that R, tie and its models remains upstream.

ONE ORIGINAL io_i BEFORE EVERY PARAMETER t

JIO1–JIO12 first reconstruct the parameter-free polynomial map. The factorial Fock form has the exact substitution adjoint. Its two group actions include the correct inverse-transpose convention and all determinant twists. The positive and negative minor products give the prescribed joint weights. Reversing the negative block produces the actual joint bottom vector.

A finite compact type is extended holomorphically by an explicit normalized peaked-Haar kernel. The kernel concentrates at the identity, giving an invertible averaged operator; the resulting integral is a finite holomorphic expression in matrix entries and inverse entries. A one-variable identity theorem along polar-decomposition curves extends the group and adjoint identities. No additional complexification theorem is imported.

Bottom matrix coefficients are determined by their weight, through triangular factorization and holomorphic continuation. Their Gram identities construct the transfer map on orbit spans. The operator on the entire original LowT is constructed using compact-equivariant projections and commuting one-place operators; it is not restricted to a substituted irreducible summand.

Combining that map with the exact coefficient bridge gives a bilinear io. Its normalization is explicit. If v_tau^0 and w^0 are the nonzero selected inputs, multiply the map by
  C = ||w^0|| product_tau ||v_tau^0||,
then divide each input by its own norm. Their norms become one and the value is exactly Delta, with no undetermined scalar or phase.

JIO13–JIO18 then check that this same polynomial construction works for the actual theta and Weil data at every t. The universal IsThetaAt law forces the stored vacuum to be a theta function, by perturbing a place model with an operator from an annihilating functional. Its real vacuum equations and creators give the whole stored thP_pt_theta predicate.

The actual level-character exponents are transported through ChrEq using one-place finite nets and real density. Finite-order parameter twists have zero real exponent, so the weights chosen before t remain valid for every t. Real determinant roots give the exact character values, including the factor of two in the source's rational-exponent convention.

For the vacuum phase, the proof uses CW24's explicit auxiliary eta0 and then compares two full Weil data with the same prescribed splitting characters by BTH14. It neither identifies eta0 with the stored level eta nor assumes a universal IsEtaTilde property that has not been supplied. This fixes the actual action normalization.

Changing the original source and target bases gives the literal Fock substitution, with conjugated coefficients on negative target rows and the original creator scale. Differentiation through the actual Weil action is justified by its theta-space L2 isometry and genuine Heisenberg difference-quotient convergence, then continuous representatives give equality pointwise.

JIO19 proves the original quantifier order:
  for every i, there exists one io_i, for every t, IsIoW(..., io_i).
Both intertwining laws and the exact unit-input Delta normalization are included. If the original R has the weak OrZero choice law, this existence activates the strong predicate for the stored ioP. It is not necessary, or asserted, that the newly constructed witness equals the stored one.

REGULAR QUOTIENT, SMOOTH WORDS, CUSP CLOSURE AND CENTRAL SCALARS

RQC1–RQC6 construct the entire original IsReg from a supplied FinPair. The measure is exactly
  nu = (mu restricted to F)_* autMk
on the original rational quotient. Countably many rational translates unfold Haar integration. An invariant integral is independent of the fundamental domain, so right translations preserve this exact quotient measure. Quotient almost-everywhere equalities lift to Haar-almost-everywhere equalities on the whole adelic group, matching the original Repr convention.

Strong continuity is written out: compare quotient indicator symmetric differences with finite-measure lifted sets, use compact/open regularity to prove continuity of Haar translations, then pass from simple functions to every L2 vector using the isometry. No alternate quotient normalization is introduced.

RQC7–RQC10 prove stability of the full original exponential-word smooth subspace and the complete complexified derived Lie identities. The literal SmoothMultilinear.smooth_map has the source's full target generality. Every ordered Hilbert derivative word acts by the corresponding ordered filtered word in each model factor; one-place operator order is never commuted away. The same finite level survives every derivative word.

RQC11–RQC16 supply the complete original cusp-closure producer. A compact set K meets a rational orbit with multiplicity at most
  N_K = #(Gamma intersection K K^{-1}).
For a rational invariant continuous representative h of H, unfolding and Cauchy–Schwarz give
  integral_K |h| <= N_K mu(F)^(1/2) ||H||_2.
Compact averaging is therefore continuous from such representatives in the L2 norm into local L1. Vanishing averages pass from finite regular-orbit combinations to their closed Hilbert span, and continuity upgrades vanishing back to every point.

The actual ZI transvection group, Haar measure and arbitrary fundamental domain are retained. The compact adelic quotient supplies a compactly contained Borel domain; invariant integration transfers the result to every original domain. This proves every ZCusp quantifier and, with the inherited CTC12 criterion and original finite level, genuine cuspidality. The argument never restricts an arbitrary ambient L2 equivalence class to a measure-zero subgroup.

RQC17–RQC20 prove the original Gelfand-scalar supplier. The operator of index k is exactly the sum of ordered matrix-unit cycles of length k+1. It is the trace of a matrix power with operator entries. Conjugation invariance uses cyclicity only when one matrix has scalar entries, avoiding an invalid general trace rule for noncommuting entries.

A weight-preserving word-reordering argument puts lower, diagonal and upper generators in order. On the actual highest vector, upper generators vanish, and a zero-weight word with lower generators but no upper generators is impossible. The surviving diagonal words give a scalar polynomial in the original weights. The derived adjoint formula makes the cyclic operator symmetric; conjugation invariance makes it commute with the group. Pairing with the dense orbit of the nonzero highest vector then gives the same scalar on every smooth vector. No unbounded operator is extended by continuity.

RQC21 transfers that scalar to the literal pointwise gelf operators once actual pointwise derivative identities are supplied; the span of one function witnesses central finiteness. This is useful downstream, but it cannot be used circularly to justify initial boundedness required before the Hilbert construction.

The remaining analytic producers are now concentrated: initial boundedness; the actual target FinPair; existence of the original continuous smooth representatives and every derivative identity; the fixed-order Sobolev estimate, continuous evaluation and uniform moderate growth. The full IsMultMap is still not claimed.

THE COUPLED ONE-POINT Choice AND B2

CCH1–CCH17 work at the full-block h=0,a=n=4 point produced by original NiceI normalization. In this case the off-diagonal module Od vanishes. A Kap with g=0 is constructed with every source generation, independence and local-correction field.

The trace detector is nevertheless constructed for the full original twisted polarized cocycle module. A trace-zero cocycle gives a matrix-algebra derivation; the matrix-unit computation makes it inner. Extension from the full cyclotomic kernel and polarization preserve the source twist and transpose sign. Only 2 and a nonzero cyclotomic scalar are inverted, so rank four in characteristic 3 is included; division by 4 or 4! is never used.

PhiCond supplies finite residual cocycle spaces. An explicit t-adic lifting argument gives finite generation, allowing a single finite trace list. One finite coefficient extension then splits the relevant regular elements. The extension is a finite free complete DVR and is presented as k'[[u]]. Ramification is tracked as j(t)=v u^e with v a unit and e>=1.

The same list remains a detector after extension through finite-free coordinates. All original NP fields, ordered characters, flags and polarization, N3, N4 for every retained old subgroup, the full determinant polynomial law and the original point kernel are transported. Nothing is replaced by an abstract compatible point.

For this same chosen g=0 Kap, B2 has an explicit zero-cocycle witness and C=0 for every m and every N, including zero. The construction is stronger in those later parameters than eventual-N existence. The logical rule is coupled:
  exists one Choice witness with g=0 AND B2 for that same witness.
It does not prove the universal TaylorWilesObstructionBound for an arbitrary Kap.

The selected CountII residue is still substantial: original ordinary/control and separating arithmetic fibers; the integral type, full TThetaEx/IsWt and neatU; four additional Hida endpoints on the exact J; all-level same-J HasAut; the precise B1 bound with D=4[L+:Q]+4q; and h=0 Raw support propagation. Full CohP, LocCFT and all original side conditions remain. In particular g=0 does not make the Sel1 group in B1 vanish.

THE FINAL CUT AND NEXT WORK

The final ten-input interface is unchanged: DesignExists together with the nine original Closed inputs for LinkN, LinkEta, LinkIRR, SmallLevelRankEq, guarded LinkDIVt, fullness/rank, LinkG, guarded LinkS and guarded LinkGLOBAL. The complete inherited global assembly consumes its exact original compatible family and second layer; it does not construct them.

RH and two-primary Dirichlet targets retain Cases I,II,V. Unrestricted Dirichlet GRH also retains CaseIII, SeedIV and the original chains. Original fields, coefficient embeddings, metrics, common choices, VWinAt(chi,401), floor(x^400) and the final 1/2+9epsilon endpoint keep their inherited scopes.

"""+cfg["next_local_priority"]+"""

The source-anchored continuation notes refine these priorities. The analytic note targets the exact smooth-representative/Sobolev interface. The CountII note separates the remaining numerical B1/Selmer count from the ordinary and automorphic module producers. The common-construction note traces BunU/selected-realization output on the same R to its original geometric, row, side and local inputs. These notes are work plans, not further closure certificates.

Every remaining selected contract follows. The paragraph under each numbered heading is copied exactly from the current graph.

EVERY REMAINING SELECTED OBLIGATION
"""
intro=r"""\section{Current dependency audit: simultaneous theta maps and coupled one-point data}
\label{sec:dependency-audit-v36}

\paragraph{Status and scope.}
This version adds 71 human proof claims, for 1770 cumulative claims.
It completes the original simultaneous $ioP$, the exact regular,
smooth-vector, cusp-closure and Gelfand-scalar suppliers, and the
required one-point rank-four \texttt{Choice} together with
\texttt{B2} for its same chosen $g=0$ witness.
The underlying Alpoge--Claude Lean proof is accepted as fully checked
and correct. The human reconstruction remains \textbf{incomplete}.
No new Lean replay is claimed.

The selected sufficient graph has 121 nodes and 34 open coupled
leaves: 23 C, 9 B and 2 D. No further whole selected leaf is closed;
substantial nested producers inside theta and CountII are discharged.
The final-global assembly remains closed from version 0.35.
All 245 historical compound targets in 107 groups, and all selected
logical edges, remain. These counts are neither completion percentages
nor a theorem of absolute minimality.

\begin{center}\small
\begin{tabular}{cp{0.80\textwidth}}
A & A published theorem applied with every original hypothesis and normalization checked.\\
B & An elementary or moderately difficult argument reconstructed independently.\\
C & A substantial or deep reconstruction obligation.\\
D & A possible gap in our human understanding of the formal source.\\
\end{tabular}
\end{center}
The two D leaves are \texttt{AD\_VANISH\_K\_MATCH} and
\texttt{HOST\_RIGID\_S}; they do not allege a formal error.
No new published theorem is imported in this version.

\paragraph{One original theta map before all parameters.}
CFB1--CFB13 prove the exact coefficient-to-polynomial bridge on
the same $c_{0L},cV,BV$, with range precisely the original
$\mathrm{VV}$, covariance at every real source point, and compact
cyclicity of its actual extremal polynomial.
The complete original weight arithmetic removes the literal floors,
identifies the forced $\mathrm{lamLdef}$, and gives the three integer
determinant twists and both signed minor-weight identities.

JIO1--JIO19 construct the full original \texttt{exists\_ioP}.
The factorial form and Fock substitution have their exact adjoints.
An explicit peaked-Haar kernel extends each finite compact type
holomorphically; bottom-weight coefficient identities give the orbit
Gram transfer. The resulting operator acts on the whole original
$\mathrm{LowT}$. With the same coefficient bridge, it yields the
parameter-free bilinear map. Its normalization is explicit:
multiplying by $\|w^0\|\prod_\tau\|v_\tau^0\|$ and normalizing
the inputs makes its value exactly $\Delta$.

The universal place-model law gives the stored theta vacuum.
Original splitting characters have parameter-independent real
exponents, and the actual Weil character and creator substitution
give both intertwining laws. The vacuum phase uses CW24's explicit
auxiliary $\eta_0$ and BTH14's equality of full Weil data with the
same prescribed characters. It neither identifies $\eta_0$ with
the stored level character nor assumes an unproved universal
\texttt{IsEtaTilde} restriction.
The conclusion has the necessary order
\[
       \forall i\ \exists io_i\ \forall t:\quad
                         \mathrm{IsIoW}(\ldots,io_i).
\]
It activates the strong predicate for the stored weak
\texttt{OrZero} choice, without asserting equality of two witnesses.

\paragraph{The regular quotient and exact analytic suppliers.}
RQC1--RQC6 construct the full \texttt{IsReg} from the supplied
\texttt{FinPair}, on the literal measure
$(\mu|_{\mathcal F})_*\mathrm{autMk}$.
Unfolding gives the global almost-everywhere representative convention
and measure preservation. Indicator symmetric-difference estimates,
Haar regularity and density give strong continuity.

RQC7--RQC10 prove the full smooth subspace, complexified derived
Lie identities and the exact multilinear smoothness producer.
Every Hilbert derivative word has its original right-fold order,
and all derived tuples retain the same finite level.

RQC11--RQC16 prove the whole cusp-closure supplier.
For compact $K$, the finite rational orbit multiplicity is bounded
by $N_K=\#(\Gamma\cap KK^{-1})$, and
\[
 \int_K|h|\le N_K\mu(\mathcal F)^{1/2}\|H\|_2
\]
for a rational invariant representative $h$ of $H$.
This controls compact averages in local $L^1$, allowing their
vanishing to pass to a closed Hilbert orbit span when continuous
representatives are supplied. The actual transvection group,
every Haar measure and every fundamental domain are retained.
An arbitrary ambient $L^2$ class is never restricted to a
measure-zero unipotent subgroup.

RQC17--RQC20 prove the exact Gelfand scalar endpoint.
The $k$-th operator is a sum of ordered matrix-unit cycles of
length $k+1$. Scalar-matrix trace invariance permits the original
frame change. Weight-preserving word reordering evaluates it on
the actual highest vector. Formal symmetry, group covariance and
density of that vector's orbit give the same scalar on every
smooth vector. No unbounded operator is extended by continuity.
RQC21 gives the literal pointwise central-finiteness field once
pointwise derivative identities are supplied.

Initial boundedness, the actual target \texttt{FinPair}, actual smooth
representatives with every derivative identity, and the fixed-order
Sobolev evaluation/growth estimates remain. The full
\texttt{IsMultMap} is not claimed. Post-Hilbert central finiteness
cannot supply earlier boundedness.

\paragraph{The coupled one-point arithmetic construction.}
CCH1--CCH17 construct the entire required $h=0,a=n=4$
\texttt{Choice}, on the point supplied by the original NiceI
normalization. The off-diagonal module vanishes, and an actual
$g=0$ \texttt{Kap} satisfies all generation and local-correction fields.
The full twisted polarized trace detector is still constructed:
trace vanishing gives a matrix derivation and an explicit inner
expression, followed by extension from the full cyclotomic kernel.
Polarization divides only by $2$, so rank four at $\ell=3$ is included.

The actual $\Phi$ condition and an explicit $t$-adic lifting argument
give finite generation and one finite detector list. One common
finite local extension splits the regular elements. Ramification
$j(t)=vu^e$ is tracked in the detector, continuity and old \texttt{N4}.
Every original \texttt{NP} field, character, ordered flag,
polarization, \texttt{N3/N4}, full determinant law and point kernel
is retained.

For that \emph{same} chosen $g=0$ witness, the literal \texttt{B2}
has $C=0$ before every $m$ and every $N$:
\[
 \exists\text{ one Choice witness }\
       [\,g=0\ \text{and B2 for that same witness}\,].
\]
This does not close the arbitrary-\texttt{Kap} obstruction theorem.
The original ordinary/control/type data, four Hida endpoints,
same-$J$ all-level \texttt{HasAut}, exact first-order \texttt{B1}
with $D=4[L^+:\mathbb Q]+4q$, and $h=0$ \texttt{Raw} remain,
with \texttt{CohP}, local class field theory and every original
side condition. In particular $g=0$ does not force the
\texttt{Sel1} group to vanish.

\paragraph{Final cut and next priority.}
The ten-input final interface, all shared objects and all original
AND edges are unchanged. RH and two-primary targets retain I/II/V;
unrestricted Dirichlet targets additionally retain III, SeedIV and
the chain arguments. The original window exponent $401$,
$\lfloor x^{400}\rfloor$ and $1/2+9\epsilon$ estimate keep their scopes.
"""+esc(cfg["next_local_priority"])+r"""

\paragraph{Every remaining selected obligation.}
Each paragraph below is the complete current contract from the graph.
Its category describes the remaining human work, not correctness of
the underlying formal theorem.
"""
(AUD/"audit_intro.txt").write_text(plain);(AUD/"audit_intro.tex").write_text(intro)
tex=intro+"\n\\begin{description}[style=nextline]\n"
for i,n in enumerate(records,1):
    tex+=f"\\item[{i}. {esc(n['id'])} --- {n['category']}] {esc(n['title'])}. {esc(n['contract'])}\n\n"
    plain+=f"\n{i}. {n['id']} — {n['category']} — {n['title']}\n\n{n['contract']}\n\n"
tex+="\\end{description}\n"+r"""
\paragraph{Validation and continuity.}
All predecessor claims, source arrays and mathematical dependency
edges are preserved. New proof ranges and exact source ranges are
hashed and independently reviewed. The release checks the complete
remaining register, selected reachability, review bindings and
predecessor manifest, then TeX syntax and references in draft mode.
There is no PDF production or Lean replay. Historical RF16 remains
governed by DEX11. The current audit and additive scope updates
govern older frontier descriptions.
"""
plain+="""VALIDATION AND CONTINUITY

Every predecessor claim, source array and mathematical dependency edge is preserved. New source/proof ranges are bound to the pinned commit and independent reviews bind the released bytes. Release checks cover the complete remaining register, selected graph reachability, review hashes and every predecessor manifest entry. Draft TeX checks syntax and references only, without PDF production or Lean replay. The preserved DEX11 correction governs historical RF16. The current audit and additive scope updates govern older frontier descriptions.
"""
(AUD/"main.tex").write_text(tex);(AUD/"audit.txt").write_text(plain)
(ROOT/"RH_dependency_audit_v0_36.txt").write_text(plain)
print("Audit written:",len(plain.split()),"words;",len(records),"exact remaining contracts.")

