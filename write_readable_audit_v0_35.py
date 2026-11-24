#!/usr/bin/env python3
"""Write the current dependency audit, including every exact unresolved contract."""
from pathlib import Path
import collections, json, re

ROOT=Path(__file__).resolve().parent;AUD=ROOT/'dependency_audit_v0_35'
cfg=json.loads((ROOT/'increment_v0_35.json').read_text())
g=json.loads((AUD/'obligation_map.json').read_text())
records=json.loads((AUD/'remaining_leaf_register.json').read_text())['records']
cats=collections.Counter(x['category']for x in records)
count=cfg['expected_new_claims']
def esc(t):
    mapping={'\\':r'\textbackslash{}','&':r'\&','%':r'\%','$':r'\$','#':r'\#','_':r'\_','{':r'\{','}':r'\}',
     '→':r'$\to$','−':r'$-$','≥':r'$\ge$','≤':r'$\le$','ε':r'$\varepsilon$','λ':r'$\lambda$','Ψ':r'$\Psi$','𝒞':r'$\mathcal C$','^':r'\textasciicircum{}','~':r'\textasciitilde{}'}
    return ''.join(mapping.get(c,c)for c in t)

plain=f'''RH / DIRICHLET-GRH RECONSTRUCTION — COMPLETE SELECTED DEPENDENCY AUDIT
Version 0.35 — 22 November 2026

STATUS AND SCOPE

The original final-global assembly implication is now fully reconstructed on its stated inputs. This version adds {count} human proof claims across four chapters. It also proves full lowest-type smoothness and multiplicity one on the original discrete-series model, the exact extremal coefficient identity and Hilbert multilinear stage, the complete original auxiliary-prime supplier ArPl, and residual Hecke values for every supplied integral type.

The human reconstruction remains incomplete. We accept the underlying Alpoge–Claude Lean proof as fully checked and correct. A completed implication on a supplied compatible family does not construct that family, its common choices, or its arithmetic/spectral inputs. A Hilbert-valued map does not yet provide the source's pointwise smooth, Sobolev-continuous MMap.

This is a sufficient dependency audit of the selected human proof route. It records every selected remaining obligation below and preserves all 245 historical compound targets in 107 scope groups. It does not assert an absolute minimality theorem or a full Lean transitive-dependency computation. Shared obligations occur once in the graph; optional routes remain outside the selected AND requirements.

CURRENT COUNTS

The selected graph has {g['validation']['selected_node_count']} nodes and {len(records)} open coupled leaves:
A — published theorem application still awaiting a checked match: {cats['A']}.
B — elementary or moderately difficult independent reconstruction: {cats['B']}.
C — substantial/deep reconstruction: {cats['C']}.
D — unresolved human understanding of the formal source: {cats['D']}.

The former TASK_GL_FINAL_ASSEMBLY leaf is proved in its original conditional scope, reducing the open register from 35 to 34. The theta-extension and CountII leaves are narrowed without being falsely closed. Counts are navigation aids, not completion percentages: one coupled C obligation can contain much more work than several B obligations.

The two D obligations remain AD_VANISH_K_MATCH and HOST_RIGID_S. Their classification records an unresolved human match to the formal source. It is not a claim of a flaw in the checked Lean proof.

WHAT IS NEW

'''+ '\n\n'.join(cfg['new_in_this_version'])+'''

WHY THE GLOBAL ASSEMBLY LEAF IS NOW CLOSED

LFS reconstructs the complete finite loss calculation on the actual source record. Its four prime classes yield eleven terms. The exact dyadic small-order constant can be 12; elementary prime bounds suffice. Uniform original loss windows give the leading coefficient 2 log(4) C and the thirteen-error remainder. Both the prime-logarithmic IOsum and ASK−Ga estimates use the original support, actual finite-place weights and original ramified representative. The ASK identity is universal over the permitted frame/degree/weight reading, heterogeneous arithmetic-record equality and cutoff.

The same chosen integer functions av,bv and the same member i1 realizing them are retained. ChosenWS makes every member carrying that pair admissible for the loss bound. No realization of an arbitrary pair and no CoverAll assumption is inserted.

GFI then carries that realized pair to every original base point. It constructs the actual ledger Data, arithmetic and place equivalences, all four ties, one character functional and a common cutoff. It checks all eleven ledger conditions, all error windows and every budget/growth/cost/remaining-size field. The Closed cutoff and joined TransportedAlt tuple are chosen before the family and CH; the family's eventual x threshold precedes every member, base point, word, place and reading.

ChosenE plus ChosenWall supplies the exact required small-share packet. The source's second-set lower bound gives thick density by an explicit logarithmic estimate; an elementary harmonic sum suffices for the chosen-bad-prime conversion. These simplifications preserve the original conclusions. The selected final consumer retains Cabs=2, C0=3, column constant 4,eD=2, eL=0. The column constant is distinct from the ChosenQD parameter used as CL in the tied ledger. The downstream zero-free endpoint remains 1/2+9epsilon.

The original compatible family, Duty, second-layer selection, LinkG, LinkS, LinkIRR and LinkDIV remain inputs. Their graph edges are retained. Completing the assembly does not prove these producers.

WHAT THE THETA BRANCH NOW SUPPLIES

HCU works on the original signed negative-frame domain. Signed Gram–Schmidt gives an actual smooth triangular factor; polar decomposition gives the required connectedness. A local torus-contraction argument and holomorphic continuation prove coefficient uniqueness. The full smooth Borel-equation/holomorphic-section dictionary is written out, including the complex-linear differential.

The representation-theoretic step starts with a smooth compact-type seed and the full original lowKSub, defined as the algebraic supremum of every subspace of the specified type. Finite compact-weight arguments and the exact Vogan-norm inequality prove noncompact lowering. Coefficient uniqueness then forces every lowest-type subspace to equal the same seed. Thus the complete original LowSm and LowIrr, including multiplicity one, are proved; no smaller selected subspace or different DSModel is substituted. The ordered base model at the actual coefficient embedding is checked separately; no HolShape assertion at every embedding is inferred.

For a bounded original HolForm on a supplied FinPair/IsReg target, the quotient representative and holomorphic integration arguments give the exact matrix coefficient identity. The orbit Gram identity then constructs a continuous multilinear Hilbert map with the original extremal value, one-place actions, finite eigenlaws and closed-orbit containment. This is the whole original BackForm.exists_map stage.

Remaining analytic work is precise: one common io_i valid for every parameter t; boundedness and the actual finite-volume regular target; pointwise smooth representatives and their derivative identities in the Hilbert image; Sobolev point-evaluation bounds and uniform growth; central finiteness; and cusp-integral preservation under closed orbit span. These are the suppliers needed to turn the Hilbert map into the literal MMap on the full original Wall. Geometric readings, rational tests and base rows are separate remaining contracts.

WHAT COUNTII NOW SUPPLIES

CAP proves full ArPl under unchanged CohP. Finite H1 gives the required Phi condition for every open subgroup by an explicit induced cocycle. The residual determinant polarization proves normality of the exact character/cyclotomic kernel H, including coefficient characteristic 3 and degree zero. The Frattini tower is cofinal relative to the exact PL subgroup, as required by the source.

Unconditional finite-Galois Chebotarev is the one new published application. The finite extension, excluded primes and arithmetic Frobenius convention are checked. A direct construction gives degree-one split CM primes for every prescribed finite list. Actual enlarged levels retain the same local datum. Their complete closed kernels are generated by the selected tame elements modulo the exact PL subgroup, and the original tame clause of CohP gives the required relation with inverse arithmetic Frobenius. The bound

  #HomL(preimage H) <= #HomL(H) * ell^(q [Gamma:H])

is independent of the level. Every original TWGrp and TWPl field is checked, including n=0, q=0, N=0 where applicable. The original ArPl conjunction is available before and after the arbitrary list is selected, in the exact order used by Choice.

CAP also constructs the residual Hecke values at every QData level for any supplied integral type. Unramified Frobenius conjugacy/inertia checks and the factorization through the actual artOf give values independent of the permitted Frobenius and uniformizer preimages. This supplies IsRes, while the type/neatU/TThetaEx and ordinary/control producers remain explicit.

The whole same-ideal CountII producer is still open: ordinary/control and separating arithmetic fibers; four further Hida endpoints; same-J all-level HasAut; Choice; first-order and obstruction bounds; and Raw, with CohP and the other original side conditions retained. Both original rank-four Links keep the one coefficient threshold at fixed iota, ell=3 and their actual rings and ideals.

THE FINAL THEOREM CUT AND THE NEXT PRIORITY

The final ten-input interface is unchanged: DesignExists plus the nine original Closed inputs for LinkN, LinkEta, LinkIRR, SmallLevelRankEq, the guarded LinkDIVt, chosen fullness/rank, LinkG, guarded LinkS and guarded LinkGLOBAL. The global assembly consumer now supplies the final LinkGLOBAL implication on its original premises. It does not create the shared construction or the other inputs.

RH and two-primary Dirichlet targets still require Cases I,II,V. Unrestricted Dirichlet GRH additionally requires CaseIII, SeedIV and the original chain propagation/descent. The existing Gaussian/quartic and square-root-minus-seven count scopes remain distinct. VWinAt(chi,401), floor(x^400), all same-field/metric bindings, and the final 1/2+9epsilon estimate are retained.

'''+cfg['next_local_priority']+'''

The following is the complete current selected register. Each paragraph is the exact contract stored in the machine-readable graph. Its A/B/C/D category describes the work remaining, not whether the underlying formal theorem is correct.

EVERY REMAINING SELECTED OBLIGATION
'''

intro=r'''\section{Current dependency audit: completed global assembly and original lowest types}
\label{sec:dependency-audit-v35}

\paragraph{Status and exact scope.}
The final-global assembly implication is now reconstructed on its original
inputs. This continuation adds '''+str(count)+r''' human claims. It also proves
full original lowest-type multiplicity one, the extremal coefficient and
Hilbert-map stages, the complete original auxiliary-prime supplier, and
residual Hecke values for every supplied integral type.
The underlying Alpoge--Claude Lean proof is accepted as fully checked
and correct. This is still a \textbf{partial human reconstruction}:
the common geometric, analytic, local, spectral and ordinary arithmetic
producers listed below remain to be written out.

The selected sufficient graph has '''+str(g['validation']['selected_node_count'])+r''' nodes and
''' +str(len(records))+r''' open coupled leaves: '''+str(cats['C'])+r''' C,
'''+str(cats['B'])+r''' B and '''+str(cats['D'])+r''' D.
The entire conditional \texttt{TASK\_GL\_FINAL\_ASSEMBLY} leaf is
closed; the theta and CountII leaves are narrowed. All 245 historical
compound targets in 107 scope groups are retained. These counts are
neither completion percentages nor a theorem of absolute minimality.
Optional routes remain outside the selected AND requirements.

\begin{center}\small
\begin{tabular}{cp{0.80\textwidth}}
A & A published theorem applied with every original hypothesis and normalization checked.\\
B & An elementary or moderately difficult argument to reconstruct independently.\\
C & A substantial or deep reconstruction obligation.\\
D & A possible gap in our human understanding of the formal source.\\
\end{tabular}
\end{center}
The two D leaves remain \texttt{AD\_VANISH\_K\_MATCH} and
\texttt{HOST\_RIGID\_S}; they do not allege an error in the checked proof.

\paragraph{The complete original global consumer.}
LFS1--LFS17 derive both original losses from the same chosen tops,
bad-prime bound, local gains and chosen realized degree pair.
Four prime classes yield eleven terms, with order constant 12,
leading coefficient $2\log(4)C$ and the thirteen-error remainder.
The gain and prime-logarithmic dictionaries retain every finite-place
weight. The asked-sum identity holds for every permitted reading,
arithmetic-record equality and cutoff. The original $a_v,b_v,i_1$
remain unchanged; no \texttt{CoverAll} premise is added.

GFI1--GFI17 construct the actual common ledger, all ties, one character
and cutoff, every ledger inequality and every error, size, growth and
cost field. The original chosen-data conversion and the final
\texttt{Closed} order are proved. Its epsilon cutoff and joined
transport tuple precede the family and $C_H$; the eventual threshold
precedes all members, base points, words, places and readings.
The selected constants remain $C_{\rm abs}=2,C_0=3$, column constant
$4$, $e_D=2,e_L=0$. The column constant and chosen quadratic parameter
$C_L$ have their distinct original roles. The final zero-free endpoint
is still $1/2+9\epsilon$.
Compatible family/selector existence, duties and the actual
\texttt{LinkG/LinkS/LinkIRR/LinkDIV} producers remain upstream.

\paragraph{The original lowest type and Hilbert stage.}
HCU reconstructs the signed frame domain, smooth triangular factor,
connectedness, local/global holomorphic uniqueness and the full Borel
dictionary. Finite compact-weight arguments and the explicit Vogan-norm
inequality give lowering on the full original lowest subspace.
Coefficient uniqueness proves that every lowest-type summand is the
same smooth irreducible seed. Thus \texttt{LowSm/LowIrr}, including
multiplicity one of the original supremum, is supplied. The ordered
base model at its original coefficient embedding is checked.

On a bounded original \texttt{HolForm} with the supplied same-target
\texttt{FinPair/IsReg}, holomorphic integration gives the exact extremal
coefficient identity. The orbit Gram identity gives the full original
Hilbert multilinear map and finite eigenlaws. What remains is one
$io_i$ valid for every parameter, actual boundedness/finite volume,
smooth representatives and their derivatives, Sobolev point evaluation
and uniform growth, central finiteness and cusp closure. These are
needed for the pointwise smooth \texttt{MMap} on the full original
\texttt{Wall}; geometric readings, rational tests and base rows are
separate contracts.

\paragraph{The original auxiliary primes and residual values.}
CAP1--CAP14 prove full \texttt{ArPl} under unchanged \texttt{CohP}:
the exact residual subgroup and its normality, the $\mathrm{PL}$-relative
Frattini tower, split degree-one Chebotarev primes for every list,
the actual enlarged levels, complete closed kernel and inverse-Frobenius
tame relation. The single bound
\[
 |\operatorname{Hom}_\ell(p_N^{-1}H)|
 \le |\operatorname{Hom}_\ell(H)|\ell^{q[\Gamma:H]}
\]
is independent of $N$. Unconditional finite-Galois Chebotarev is the
one new published input, with its hypotheses and convention checked.
CAP15--CAP17 construct original \texttt{IsRes} values for any supplied
integral type at every \texttt{QData} level.
Ordinary/control, the type and \texttt{neatU/TThetaEx}, four further
Hida endpoints, same-ideal all-level \texttt{HasAut}, \texttt{Choice},
first-order/obstruction bounds and \texttt{Raw} remain producers.

\paragraph{Final cut and next priority.}
The exact final ten-input interface and every shared common-object
requirement are unchanged. RH and two-primary targets retain I/II/V;
unrestricted Dirichlet targets additionally retain III, SeedIV and
the chain arguments. The original window exponent 401, floor
$x^{400}$ and $1/2+9\epsilon$ estimate retain their scopes.
'''+esc(cfg['next_local_priority'])+r'''

\paragraph{Every remaining selected obligation.}
Each following paragraph is the full current contract from the graph.
Categories and completion status are separate; no conditional consumer
is counted as its missing producer.
'''
(AUD/'audit_intro.txt').write_text(plain)
(AUD/'audit_intro.tex').write_text(intro)
tex=intro+'\n\\begin{description}[style=nextline]\n'
for i,n in enumerate(records,1):
    tex+=f"\\item[{i}. {esc(n['id'])} --- {n['category']}] {esc(n['title'])}. {esc(n['contract'])}\n\n"
    plain+=f"\n{i}. {n['id']} — {n['category']} — {n['title']}\n\n{n['contract']}\n\n"
tex+='\\end{description}\n\n'+r'''\paragraph{Validation and continuity.}
Every predecessor proof, claim field, source array and dependency edge
is retained. Exact new source and proof ranges are bound to the pinned
commit and independently reviewed. The release checks all source ranges,
graph reachability, every displayed remaining contract and review hashes,
then checks TeX syntax and references in draft mode without a PDF.
These checks are not a new Lean replay. Historical RF16 remains governed
by DEX11. The current audit and additive scope updates govern older
frontier statements without silently rewriting historical mathematics.
'''
plain+='''VALIDATION AND CONTINUITY

Every predecessor proof, claim field, source array and mathematical dependency edge is preserved. Source/proof ranges are bound to commit 7cbf7a0c32fca1badf05931879a37c3f8a2b03b4. Independent mathematical reviews bind the released proof/metadata bytes. The release validator checks continuity, all source ranges, exact outstanding contracts, graph reachability and review hashes. Draft TeX checks syntax and references; it produces no PDF and is not a Lean replay. Historical RF16 remains governed by its preserved DEX11 correction. The current audit and additive scope updates govern superseded historical frontier statements.
'''
(AUD/'main.tex').write_text(tex)
(AUD/'audit.txt').write_text(plain)
(ROOT/'RH_dependency_audit_v0_35.txt').write_text(plain)
print('Audit written:',len(plain.split()),'words;',len(records),'exact open contracts.')
