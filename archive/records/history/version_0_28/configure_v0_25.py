#!/usr/bin/env python3
"""Describe the completed LemmaK/ThmBab chains and the exceptional CountZ leaf."""
from pathlib import Path
import json

ROOT=Path(__file__).resolve().parent
components=['local_k_duality','torsion_homology','k_theory_bridge',
            'simultaneous_cohomological_windows','count_z_closure']
scope=(
 'Partial human reconstruction of RH and Dirichlet GRH, prioritizing complete dependency chains. '
 'LK1–LK4 supply all three literal native local-K interfaces, including nonfree coefficients and the residue-characteristic Euler factor. '
 'TB1–TB10 construct the ordered Hermitian-form nerve, prove its acyclicity and all-prime orbit/stabilizer torsion estimates, and supply TorsBound49 and TorsBoundPow22. '
 'KB1–KB8 construct the actual KBridge from precisely matched classical K-theory and prove the universal LemmaK31 on the original arithmetic data. '
 'TW1–TW8 translate classical Ferrero–Washington into the exact finite-layer rank interface and close every tower, coinvariant, exception-set, field-model and simultaneous-window step of ThmBab, with one BConst before all Ct>=1. '
 'CZ1–CZ6 independently prove literal PropZ and CountZ by vanishing, with exponent zero. '
 'Together with the earlier odd-minus theorem OB8 and VW assembly, this leaves PointHV as the sole unresolved major cohomological supplier on that selected route; its shared K/local inputs and CountZ are supplied, while CountI/II/III/V and their remaining original-field assembly are retained. '
 'The actual common family and arithmetic gap, genuine theta/local installation, actual local denominator tables, global/spectral estimates and exact lattice-metric transport remain separate substantive obligations. '
 'All earlier proofs and original claim/source records are preserved. No complete human RH/Dirichlet-GRH proof, fresh Lean build or independent kernel replay is claimed.'
)
new=[
 'LK1–LK4: exact LocalFinitenessK, LocalTateDualityK and LocalEulerCharK. The original finite K inside PadicAlgCl is used, cycK and continuous cochains are identified, all four cup-product bijections are matched for arbitrary finite nonfree modules, and |H1|=|H0||H2||M|^[K:Q_l] includes l=2.',
 'TB1–TB10: the complete all-prime torsion-homology supplier. The actual ordered perfect-form nerve is constructed and proved acyclic. A spectral-sequence proof retains every stabilizer prime; row-module residues replace normal forms; an inverse-Hermitian inequality simplifies the near-vector bound. The literal endpoints are TorsBound49 and explicit TorsBoundPow22.',
 'KB1–KB8: an actual finite K-theory module and maps supply KBridge. Finite coefficient Dwyer–Friedlander comparison, inverse limits, Arlettaz Hurewicz annihilation and integral homology stability are matched in their precise scopes, including e=1 and l=2. Original-place local transport, finite duality, class-number and tensor calculations then yield one universal LemmaK31.',
 'TW1–TW8: the full simultaneous ThmBab supplier. Classical mu=0 is translated into the literal all-layer class-rank bound, including 2. The q,d-uniform two-primary generator bound, twisted coinvariants, p-adic centers, finite exceptional twists, one common square window, all field-model transports and exact quantifier order are proved. One BConst works for every Ct>=1.',
 'CZ1–CZ6: the entire exceptional odd-plus CountZ supplier, with exponent C=0 because the actual length is zero. Direct cyclotomic-inertia control, residual-trivial and residual-quadratic cocycle arguments, the actual Gauss-sum quadratic field and an elementary h(Q(sqrt(l)))<l estimate close PropZ and its original-host CountZ specialization.',
 'The dependency audit propagates LemmaK31 and ThmBab immediately into the older conditional chains. With OB8 already available, only PointHV remains at the major cohomological cut in VW. Its local-K, LemmaK and CountZ premises are discharged separately; the other four counts and remaining assembly are explicitly retained. The global family/gap and local/metric/spectral obligations are unchanged.'
]
remaining=[
 'One actual common family satisfying HostExW/DesignExists and its dependent layout, coefficient maps, St/ColPin/R3.Read, rational good-row spectrum and remaining Core fields. The cohomological suppliers proved here do not construct this geometric state.',
 'The literal odd-plus supplier PointHV on every original host and field. Its local-K interfaces, LemmaK31 and CountZ are supplied. Actual CountI, CountII, CountIII and CountV, and the remaining count/layer/finite-sum assembly, still need human reconstruction. Their constants must be chosen before hosts and varying fields. These obligations include the precisely stated rigidity, congruence and automorphy suppliers; they are not discharged by the now-proved ThmBab windows.',
 'Genuine compatible theta/toric/local installation: nonzero theta maps, convergence and separation, critical toric ratios, Choice.FieldOK, NTh/NChoice/ChoiceSide/NdSpec/LocAll and the actual operator identities. Initial zero theta and empty toric fields remain initialization only.',
 'Actual local Galois denominator tables and original type/e0 action, parameter dictionaries, localization/theta composition and rank bindings for the LN chain. All NormChoiceFacts and Tie4 fields demanded by the stronger CutGivesAlt route remain actual supplier obligations. LN already proves the conditional scalar, cut and original-family restoration steps.',
 'The actual common arithmetic gap and all SizeData2/ErrWindows/BNBounds and IdentU readings on that same family. WB supplies the downstream character, moving-cutoff and scalar chain, and AN2/AN3/GH6 the analytic endpoint, from this exact arithmetic contract.',
 'Actual source/target lattices and metrics, NprimeMuR/LinkMu transport and retained/discarded rank compatibility. Equal dimensions or congruence-length bounds do not provide the required metric comparison.',
 'Global and spectral links for the actual operators: image/norm comparisons, normalized finite-word and Poisson/spectral statements, arithmetic kernel and mass identities, diagonal/off-diagonal Gram bounds and exceptional terms, with their original normalizations and common-family bindings.',
 'Precisely matched classical theorems remain explicit citation leaves. This increment uses finite local/global duality and class field theory; Quillen finite generation, Borel ranks, Dwyer–Friedlander surjectivity, Arlettaz Hurewicz annihilation and van der Kallen stability; Ferrero–Washington, the ordinary Iwasawa module theorem and abelian conductor–discriminant. Their written specializations are complete, while proofs of these general classical results from first principles are outside the current reconstruction.'
]
updates={
 'VW1':{'supplied_by':['LK2','LK3','TB10','KB8','TW8'],
   'closure':'The entire two-primary and prescribed reference-layer ThmBab supplier is available on one common window; the odd-minus supplier was already OB8. The original-field odd-plus PointHV comparison remains.'},
 'VW2':{'supplied_by':['KB8','TW8'],
   'closure':'The simultaneous original-field and all-prescribed-layer window input is supplied with one BConst before all Ct>=1. Its combination with the odd-plus input still requires PointHV.'},
 'VW3':{'supplied_by':['LK1','LK2','LK3','LK4','TB10','KB4','KB8','TW1','TW2','TW3','TW4','TW5','TW6','TW7','TW8','CZ6'],
   'closure':'The selected sufficient bespoke cohomological cut is reduced from ThmBab plus PointHV to PointHV alone. Its shared LemmaK, local-K and exceptional CountZ inputs are separately supplied. CountI/II/III/V and the remaining PointHV assembly are not inferred.'},
 'VW4':{'supplied_by':['TW8','KB8','CZ6'],
   'closure':'Insert the single BConst and universal ThmBab theorem of TW8, together with earlier OB8=ThmBcFree240, into the existing same-field/fixed-pair assembly. Only PointHV remains as its major cohomological premise; QP classical prime-pair inputs and actual host installation remain.'},
 'QP25':{'supplied_by':['TW8','VW3','VW4'],
   'closure':'The fixed-pair rescaling has both the odd-minus and simultaneous two-primary/reference-layer suppliers. Literal PointHV and the original compatible host are still required.'},
 'OH6':{'supplied_by':['TW8','KB8','CZ6'],
   'closure':'The two-primary term and all reference-layer window inputs are supplied, alongside the earlier odd-minus term. The odd-plus PointHV comparison and separate congruence/family inputs remain.'},
 'GH7':{'supplied_by':['TW8','KB8','CZ6'],
   'closure':'The shared uniform integral H2 bound and the full simultaneous ThmBab branch are supplied. The exceptional odd-plus count vanishes. Remaining PointHV, family/gap, genuine local/theta, exact metric and spectral suppliers remain explicit.'}
}
cfg={
 'artifact_version':'0.25','date':'2026-11-22','predecessor_version':'0.24',
 'components':components,'tex_component_order':components,'scope':scope,
 'new_in_this_version':new,'remaining_major_inputs':remaining,'claim_updates':updates,
 'completed_previous_frontier':'Actual local-K matching, all-prime torsion homology, actual KBridge, LemmaK31, exact Ferrero–Washington rank translation, the entire simultaneous ThmBab supplier and exceptional CountZ are closed.',
 'next_local_priority':'Close one actual remaining PointHV count supplier end to end, then propagate it through the full case/layer assembly. Retain CountI/II/III/V explicitly until their rigidity, automorphy or denominator inputs are actually supplied. In parallel the exact actual local-denominator table and type/theta state remain the next LinkN chain.',
 'next_steps':[
  'Start from dependency_audit_v0_25/obligation_map.json and its exact next_targets.json. LemmaK31, native local-K, ThmBab and CountZ are available suppliers, not future reconstruction targets.',
  'For PointHV choose a complete remaining CountI/II/III/V branch. Trace its actual rigidity, congruence, automorphy or vanishing hypotheses, and close their whole sufficient dependency chain before promoting the count to a supplied theorem.',
  'Reconstruct the remaining original-field CountIV/CountVs, case partition and finite-sum/layer descent needed to connect all counts to PointHV. Use KB8, LK2/LK3 and CZ6 directly; keep the original coefficient and local-data normalization.',
  'Once PointHV is supplied, immediately substitute it with TW8 and OB8 into VW3/VW4 and QP22, retaining the same original field, every prescribed layer model, one common window and fixed prime pair.',
  'For LinkN supply the full actual local Galois denominator table and type/theta/rank identities on the same family. LN already handles the finite integral algebra, all-prime summation and exact restoration cost d_j log|G|.',
  'Keep the actual common family, arithmetic gap and size/error packages, nonzero theta/local installation, global/spectral comparisons and exact NprimeMuR/LinkMu metric transport as independent substantive obligations.',
  'Preserve every historical claim and source record. Add new premise closures rather than rewriting the assumptions of older proofs. Keep classical citation leaves separate from bespoke interfaces and from source/TeX integrity checks.'
 ],
 'precision_notes':[
  'TB proves full torsion, including primes dividing stabilizer orders. No published torsion estimate with small primes discarded is used.',
  'TB10 supplies the explicit power exponent 22; KB8 supplies the uniform cohomology exponent 31 before all fields, primes, twists, closures and LData choices.',
  'KBridge is constructed from canonical K-theory. No universal construction for arbitrary Plus or KPublished records is asserted, and no missing wrapper is treated as a formal-proof gap.',
  'Dwyer–Friedlander is used at finite coefficient levels, including degree two; at l=2 the cofinal levels r>=2 and the primitive fourth root are explicit. The compact cochain H2 is identified through a finite-group Mittag–Leffler argument.',
  'LK works on the specified finite field K inside PadicAlgCl and arbitrary finite nonfree coefficient modules. KB6 supplies the original-place henselization/completion transport needed for global local restrictions.',
  'Ferrero–Washington mu=0 is converted into finite-layer class-rank bounds using Z_l finite generation and eventual total-ramification norm surjectivity, with early layers absorbed. The case l=2 is included.',
  'TW3 matches the negative discrete twist with the positive compact dual and proves the strict local-kernel comparison. TW4 constructs p-adic centers by compactness, without assuming eigenvalues are cyclotomic powers.',
  'TW8 chooses one BConst before Ct and every other parameter; R0 and R_l are functions of their fixed base data. A single exception-set union gives one window for the two-primary and all odd reference-layer terms.',
  'The original E in the two-primary conclusion and separately quantified reference-layer models are not identified. Their estimates hold on the same parameter interval and fixed pair.',
  'CZ proves actual Selmer vanishing, not just finiteness or a residue-character dimension bound. Its quadratic cocycle argument treats every original l-adic place, and C=0 is chosen uniformly before all hosts.',
  'PointHV remains an unresolved major supplier. Its CountI/II/III/V and remaining case/layer assembly are not closed merely because LemmaK and CountZ are now available.',
  'Current semantic obligations are a finite sufficient-condition map, not an exhaustive Lean dependency graph or a necessity/minimality claim. Claim counts measure navigation only.',
  'No new PDF is generated. Draft-mode TeX checks syntax and references; independent mathematical reviews assess the written proofs. Neither is a new Lean build or kernel replay.'
 ],
 'tex_front_summary':r'''\textbf{What version 0.25 achieves.} The shared quantitative
cohomology chain is now complete: LK supplies the exact local interfaces,
TB proves the full arithmetic-group torsion bound, and KB constructs
the actual $K$-theoretic bridge and proves \texttt{LemmaK} with
constant $31$. TW carries this through every tower, exceptional-twist
and field-model step to the full simultaneous \texttt{ThmBab}
theorem, with one constant record before all $C_t\ge1$.
Together with the earlier odd-minus theorem and VW assembly, this
leaves \texttt{PointHV} as the remaining major cohomological supplier.
CZ additionally proves its exceptional \texttt{CountZ} input by
vanishing. The other counts, actual common family and arithmetic gap,
genuine theta/local data and global metric/spectral comparisons remain
explicit. This is \textbf{a partial human reconstruction; the full
human-readable proof of RH and Dirichlet GRH is not yet complete}.''',
 'tex_scope_bridge':r'''\paragraph{Version-0.25 scope of the historical conditional proofs.}
Historical mathematical proofs and their original hypotheses are preserved.
LK1--LK4 now supply the three exact native local-K interfaces. TB1--TB10
prove the all-prime torsion supplier, and KB1--KB8 construct the actual
\texttt{KBridge} and supply \texttt{LemmaK 31}. TW1--TW8 supply
the literal Ferrero--Washington rank specialization and the full
$\exists K\,\forall C_t\ge1,\ \texttt{ThmBab}\ K\ C_t$.
Thus the simultaneous two-primary/reference-layer input of VW3--VW4,
QP25 and the older cohomological budget is supplied, alongside the
earlier odd-minus theorem OB8. CZ1--CZ6 independently supply
\texttt{PropZ} and \texttt{CountZ}, uniformly with exponent zero.
The selected major cohomological frontier is now \texttt{PointHV};
its other counts and remaining assembly retain their stated inputs.
The actual common family/gap, genuine theta/local data, actual local
denominator tables and global metric/spectral comparisons remain.
The current frontier is stated in Sections~\ref{sec:dependency-audit-v25}
and~\ref{sec:remaining}, and in the version-0.25 audit.

''',
 'tex_remaining_local':r'''HP in Section~\ref{sec:highest-weight-closure} supplies its exact
highest-weight, irreducibility, classification and descent interfaces.
The actual form/lattice/signature state and genuine compatible
theta/toric installation remain required.

The odd-minus branch is complete through LD/OS/OB, with
\texttt{ThmBcFree} constant $240$. In the new chapters,
LK, TB and KB supply the exact native local-K interfaces,
full torsion homology, actual \texttt{KBridge} and
\texttt{LemmaK 31}. TW supplies the entire simultaneous
\texttt{ThmBab} theorem, including every prescribed reference-layer
model on one window. CZ supplies the exceptional \texttt{CountZ}
by vanishing. Consequently the selected major cohomological cut
in VW is now \texttt{PointHV}. Its other four counts and remaining
case/layer assembly must still be reconstructed on the original data.
The QP classical prime-pair leaves and actual host installation
retain their stated roles.

LN in Section~\ref{sec:congruence-chain} already proves the
conditional original-family \texttt{LinkN} chain, with restoration
cost $d_j\log|G|$ and unchanged cohomological coefficient.
The actual local denominator tables and type/theta/rank identities
remain suppliers. The stronger cut's \texttt{NormChoiceFacts} and
\texttt{Tie4} are not consequences of a good cut alone.

WB closes the character, moving-cutoff and scalar consequences of
the exact WB7 arithmetic contract, and AN2--AN3/GH6 supplies the
analytic contradiction. The actual gap, size/error packages and
common host readings must still be constructed. DA's uniform family
join retains the exact lattice-metric premise and the remaining
global/spectral operator estimates. See
Section~\ref{sec:dependency-audit-v25} for the current sufficient
dependency map and its classical leaves.
''',
 'tex_next_target':r'''\paragraph{The next target: complete an actual odd-plus supplier.}
The entire \texttt{LemmaK} and simultaneous \texttt{ThmBab}
branches are complete, and \texttt{CountZ} is supplied by CZ6.
The next cohomological target is the literal \texttt{PointHV}.
Its actual \texttt{CountI}, \texttt{CountII}, \texttt{CountIII}
and \texttt{CountV} and their remaining case/layer assembly must
be reconstructed, including their exact rigidity, congruence and
automorphy inputs. The available \texttt{LemmaK 31}, LK and CZ
suppliers should be substituted immediately wherever they occur.
For the common arithmetic family, the full actual local-denominator
table and type/theta/rank identities can already be propagated
through LN10. Genuine theta/local installation, the arithmetic gap,
and exact lattice-metric and global/spectral comparisons remain
other complete-chain targets.
''',
 'tex_reading_order':r'''For this increment, read LK1--LK4 and TB1--TB10, then KB1--KB8
and TW1--TW8. They form the complete local/torsion-to-\texttt{LemmaK}
and simultaneous-window chain. Read CZ1--CZ6 independently for the
exceptional odd-plus vanishing supplier. Then read VW3--VW4 with
the version-0.25 scope annotations to see the immediate substitution
of TW8 alongside OB8. Section~\ref{sec:dependency-audit-v25}
records the remaining \texttt{PointHV} branch and its exact inputs.
For the global spine retain WB7--WB8, AN2--AN3/GH6 and DA1--DA2.
Historical proofs preserve their original hypotheses; the additive
version-0.25 annotations identify those now supplied. Exact proof
and pinned-source locators remain in the ledger.
''',
 'tex_ledger_rows':[
  'LK1--LK4 & Exact native local-K interfaces & Finite nonfree duality, original cyclotomic cochains and the residue-characteristic Euler factor.',
  'TB1--TB10 & Complete all-prime torsion supplier & Ordered perfect-form nerve, orbits and stabilizers; TorsBound49 and TorsBoundPow22.',
  'KB1--KB8 & Actual KBridge and LemmaK31 & Classical K-theory maps, original local transport, finite cardinalities and one universal bound.',
  'TW1--TW8 & Complete simultaneous ThmBab & Class-rank translation, twisted towers, finite exceptions, common window and all field models.',
  'CZ1--CZ6 & Complete exceptional CountZ & Actual Selmer vanishing in the residual-trivial and residual-quadratic cases; uniform exponent zero.'
 ],
 'tex_dependency_update':r'''\section{Dependency closure after the shared cohomology and tower reconstruction}
\label{sec:dependency-audit-v25}

\paragraph{A complete quantitative supplier.}
The new chapters prove the chain
\[
 \begin{aligned}
 \text{Hermitian lattice and ordered nerve (TB)}
     &\longrightarrow\mathtt{TorsBoundPow}(22),\\
 \text{classical $K$-theory comparisons (KB)}
     &\longrightarrow\mathtt{KBridge},\\
 \mathtt{TorsBoundPow}(22)+\mathtt{KBridge}+\text{LD/LK}
     &\longrightarrow\mathtt{LemmaK}(31).
 \end{aligned}
\]
The torsion subgroup is the full integral torsion of the actual
$\operatorname{GL}_{4e+4}(\mathcal O_L)$ homology. The comparison
module, maps, Hurewicz kernel exponent and finite-rank homology
identification are constructed. The final compact cohomology is
that of the original $L,\Omega,D$, with the original discriminant
and degree. The constant $31$ is uniform before all of these choices.
The precise Quillen, Borel, Dwyer--Friedlander, Arlettaz, stability,
class-field and finite-duality results remain named classical leaves.

\paragraph{Closing the simultaneous window.}
TW1 proves that classical Ferrero--Washington $\mu=0$, together
with the ordinary Iwasawa module theorem, supplies exactly the
bounded class-group rank interface, including the prime $2$.
TW2--TW4 prove the uniform two-primary generator bound, strict
negative-twist coinvariant comparison, finite-layer growth and
the at-most-$R$ center bound. TW5 gives one square window for a
finite union of exceptional twists. TW6--TW8 preserve every field
model and the quantifier order. The resulting endpoint is
\[
             \exists K:\mathtt{BConst},\quad
             \forall C_t\ge1,\quad\mathtt{ThmBab}(K,C_t).
\]
The two-primary and odd reference-layer fields are separately
quantified on this same window and prime pair. Neither an isolated
window nor a convenient substitute field is used.

\paragraph{Immediate downstream substitution.}
Take the $K$ supplied by TW8. Together with OB8's constant-$240$
odd-minus theorem, the existing VW proof now gives
\[
 \mathtt{PointHV}\ \Longrightarrow\
 \forall C_t\ge1,\ \forall\text{ primitive }\psi,\
                          \mathtt{VWinAt}(\psi,C_t).
\]
This displayed implication retains the exact VW definitions and
its already stated classical prime-pair roles. With $C_t=401$,
the unchanged VW4/QP22 rescaling gives the same fixed pair
throughout the arbitrarily late three-halves window with cutoff
exponent $400$. Thus the selected cohomological frontier has one
remaining major supplier, \texttt{PointHV}. It does not follow
that the arithmetic host or the final gap is already available.

\paragraph{The exceptional odd-plus count is also supplied.}
CZ proves actual Selmer vanishing, first when the residual twist
is trivial and then when it is quadratic. The latter identifies
the original quadratic field by a finite Gauss sum and proves
$h(\mathbb Q(\sqrt\ell))<\ell$ directly. Local coboundary
normalization at every original $\ell$-adic place then gives
the full vanishing. The literal conclusion is
\texttt{PropZ} and \texttt{CountZ}, with exponent $C=0$.
It is independent of the automorphy and rigidity inputs.

\paragraph{The exact remaining cohomological and global scope.}
For \texttt{PointHV}, LK, KB8 and CZ6 are available suppliers.
The actual \texttt{CountI/II/III/V}, their substantive arithmetic
inputs, and the remaining original-field case/layer and finite-sum
assembly remain explicit. The audit separates these tasks from
the completed \texttt{ThmBab} and odd-minus chains.
Outside cohomology, the actual common family, genuine theta/local
state, local denominator tables, arithmetic gap and size/error
packages, global/spectral comparisons and exact lattice-metric
transport are retained. LN supplies its full conditional
denominator/restoration chain; WB and AN supply the full analytic
deduction from their arithmetic contract. No necessity or minimality
claim is made for this sufficient-condition map.

'''
}
(ROOT/'increment_v0_25.json').write_text(json.dumps(cfg,ensure_ascii=False,indent=2)+'\n')
print('Wrote increment_v0_25.json')
