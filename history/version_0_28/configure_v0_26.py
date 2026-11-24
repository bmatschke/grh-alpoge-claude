#!/usr/bin/env python3
"""Describe the completed rank-one, algebra and original-field assembly chains."""
from pathlib import Path
import json

ROOT=Path(__file__).resolve().parent
components=['rank_one_cohomology','bernoulli_residual_vanishing',
            'symplectic_count_closure','framed_deformation_presentation',
            'point_hv_assembly']
scope=(
 'Partial human reconstruction of RH and Dirichlet GRH, prioritizing complete dependency chains. '
 'RV proves the literal arbitrary finite-character SoFin and algebraic-valued SoV suppliers, including exact coefficient independence. '
 'BR proves the prescribed Bernoulli-unit LemmaX, the original residual unramified-cocycle theorem, and both-character CorX. '
 'SP proves literal LemmaMprime and LemmaM, the actual shaCoc/mPrime comparison, coefficient return and the finite trace-product arithmetic, with the remaining symplectic data/model/catalogue inputs explicit. '
 'FP reconstructs the full universal LemmaP supplier, retaining exactly its own profinite-group, local-condition and finite obstruction hypotheses; it does not assert their installation on the arithmetic Raw datum. '
 'HV proves full CountVs and CountIV and every original-field, character, case, layer and finite-prime summation step from CountI/II/III/V to PointHV. '
 'With the earlier TW8 and OB8, the selected cohomological window route is now a complete implication from exactly those four actual count suppliers. '
 'CountI/II/III/V, their remaining arithmetic deformation/automorphy/catalogue/rigidity suppliers, and the common family/gap, genuine theta/local state, actual denominators and exact metric/spectral comparisons remain. '
 'All historical proofs and original claim/source records are preserved. No full human RH/Dirichlet-GRH proof, new Lean build or independent kernel replay is claimed.'
)
new=[
 'RV1–RV7: literal SoFin and SoV on every original algebraic closure and at every prime. Finite-character restriction controls H0 and the finite quotient without a prime-to-ell degree assumption. Baire and a proved Krasner argument capture the actual vector cocycle in one finite coefficient field. Lattice approximation gives an exact global coboundary. Coefficient independence includes nonnested rings and the source infinite-length convention.',
 'BR1–BR7: the entire LemmaX -> residual cocycle vanishing -> CorX chain. Integral partial Bernoulli sums, a finite Frobenius projection and a two-point contradiction preserve the exact dyadic threshold. The actual tame-index condition, finite class-field descent, the prior OS1 Jacobi ideal relation and the exact inverse-character scalar close the original residue-field theorem and both-character endpoint.',
 'SP1–SP6: full literal LemmaMprime and LemmaM. Additive injections are compared by cardinality, while the weighted intersection theorem is proved by a three-variable Rees algebra, explicit support argument, finite orbit slices, generic multiplicity one and exact leading-form difference. The final factor is exactly 2.',
 'SP7–SP10: complete actual shaCoc/mPrime comparison on a supplied Model, exact auxiliary coefficient return, construction of the integral trace product from a precisely quantified finite catalogue, and the paired-count arithmetic. The actual data/admissible-class construction, weighted model/point-orbit comparison and finite catalogue remain stated inputs; actual CountII and CountIII are not promoted to unconditional suppliers.',
 'FP: full literal LemmaP as a universal framed-deformation presentation theorem. Finite-level representability, torus weights, framed tangent identification, minimal homogeneous relations, actual small-extension obstructions and exact relation counts are reconstructed under the source hypotheses. Their arithmetic installation remains part of the actual model obligation.',
 'HV1–HV10: full CountVs and CountIV, an integral character comparison at every odd prime on every original CM field, the exact case partition, SumIn, SumOut and PointHV assembly. No odd prime dividing the original field degree is discarded. Constants are chosen before hosts and varying fields; all lengths are proved finite before normalization.',
 'The exact remaining cohomological cut is CountI and CountII and CountIII and CountV. HV10 carries these through PointHV and, with TW8/OB8/VW, to the existing universal VWinAt and fixed-pair window conclusions. The separate PointHV assembly task is closed. Global family/gap, genuine local/theta, denominator and exact metric/spectral obligations remain unchanged.'
]
remaining=[
 'The literal actual CountI, CountII, CountIII and CountV on original hosts and coefficient data. CountVs, CountIV and CountZ, together with every downstream PointHV assembly step, are supplied. One uniform count exponent must precede hosts and fields.',
 'For the paired CountII/III route, actual Raw/Good/OfCase data and admissible representation production, a compatible weighted Model satisfying the intersection and point-orbit comparison hypotheses, and the uniform conjugation-stable finite catalogue remain. The exact image-density, local/global cohomology including Fontaine inputs, rigidity and automorphy hypotheses must be installed on those same objects. LemmaM, Mprime, P, SoFin, SoV and CorX are now supplied as their precise universal theorems; this does not instantiate their arithmetic hypotheses automatically.',
 'The CountI Kato/unitary route and CountV filtration route retain their actual compatible automorphy, adjoint/rigidity, congruence-number and local-global comparison inputs. Shared algebra and rank-one suppliers should be substituted where their original hypotheses match.',
 'One actual common family satisfying HostExW/DesignExists and its dependent layout, coefficient maps, St/ColPin/R3.Read, rational good-row spectrum and remaining Core fields. No cohomological or formal deformation theorem alone constructs that geometric state.',
 'Genuine compatible theta/toric/local installation: nonzero theta maps, convergence and separation, critical toric ratios, Choice.FieldOK, NTh/NChoice/ChoiceSide/NdSpec/LocAll and actual operator identities. Initialization with zero or empty fields does not supply them.',
 'The actual local Galois denominator tables and original type/e0 action, parameter dictionaries, localization/theta composition and rank bindings in LN. NormChoiceFacts and Tie4 remain actual supplier obligations. LN already proves the conditional scalar/cut/restoration chain with exact cost d_j log|G| and unchanged cohomological coefficient.',
 'The actual common arithmetic gap and all SizeData2/ErrWindows/BNBounds and IdentU readings on that same family. WB supplies the downstream character, moving-cutoff and scalar chain, and AN2/AN3/GH6 supplies its analytic endpoint, from the exact arithmetic contract.',
 'Actual source/target lattices and metrics, NprimeMuR/LinkMu transport and retained/discarded rank compatibility, together with global/spectral comparisons for the actual operators: normalized finite-word and Poisson statements, image/norm comparisons, kernel/mass identities, Gram bounds and exceptional terms.',
 'Precisely matched classical theorems remain explicit citation leaves, including the earlier finite duality/K-theory/Iwasawa inputs and the finite class-field, local-field and elementary commutative-algebra facts used here. Written specializations are proved; these general classical theories are not reproved from first principles.'
]
updates={
 'VW1':{'supplied_by':['HV5','HV6','HV10','TW8','OB8'],
   'closure':'The full original-field PointHV assembly is supplied from the four actual CountI/II/III/V predicates; its CountVs/IV/Z and all field/coefficient/case/layer/sum comparisons are available. The actual four counts remain.'},
 'VW2':{'supplied_by':['HV10','TW8'],
   'closure':'The simultaneous ThmBab input remains complete. HV10 now supplies the exact odd-plus interface from the four-count cut; no separate assembly premise remains.'},
 'VW3':{'supplied_by':['RV3','RV7','BR7','SP1','SP6','HV5','HV6','HV8','HV9','HV10','TW8','OB8','CZ6'],
   'closure':'The selected sufficient cohomological cut is CountI and CountII and CountIII and CountV. HV10 closes their complete original-field passage to PointHV. Shared rank-one/residual/algebra suppliers are also supplied, while actual arithmetic model, catalogue and automorphy/rigidity inputs remain.'},
 'VW4':{'supplied_by':['HV10','TW8','OB8'],
   'closure':'The exact four-count premise now propagates through PointHV to VWinAt and the unchanged Ct=401 fixed-pair rescaling with exponent 400. Original prime-pair and actual-host roles are retained.'},
 'QP25':{'supplied_by':['HV10','VW3','VW4'],
   'closure':'The cohomological input is now completely assembled from actual CountI/II/III/V, with the earlier odd-minus and simultaneous two-primary/reference-layer suppliers. This does not supply the remaining compatible host or those counts.'},
 'OH6':{'supplied_by':['HV5','HV6','HV10','TW8','OB8'],
   'closure':'All selected cohomological assembly is available from the four actual count predicates. The original arithmetic family and separate congruence/local/metric inputs remain.'},
 'GH7':{'supplied_by':['RV7','BR7','SP1','SP6','HV10','TW8','OB8'],
   'closure':'Complete shared cohomology, rank-one/residual and weighted-intersection suppliers and full PointHV assembly are available. The actual four counts, model/catalogue/automorphy installation, common family/gap, genuine local/theta and exact metric/spectral suppliers remain.'}
}
cfg={
 'artifact_version':'0.26','date':'2026-11-22','predecessor_version':'0.25',
 'components':components,'tex_component_order':components,'scope':scope,
 'new_in_this_version':new,'remaining_major_inputs':remaining,'claim_updates':updates,
 'completed_previous_frontier':'Literal SoFin/SoV, CorX, LemmaMprime/M/P, CountVs/CountIV and the complete original-field four-count to PointHV assembly are supplied in their stated scopes.',
 'next_local_priority':'Install the now-complete shared suppliers on one actual arithmetic count route. For CountII/III close the exact Raw/admissible-class production, weighted Model with local conditions and point-orbit comparison, and finite catalogue, then use SP10 and HV10 immediately. Do not reopen the closed PointHV sums or rank-one/algebra suppliers.',
 'next_steps':[
  'Read dependency_audit_v0_26/obligation_map.json and its exact continuation targets. The audit distinguishes full suppliers, proved implications, retained arithmetic hypotheses and classical citation leaves.',
  'For CountII/III follow SP10 G1/G2 and the exact finite catalogue. Instantiate LemmaP on the actual framed Galois datum by proving its original PhiCond/local-condition/obstruction hypotheses, then match Model fields, M1–M4, irreducible points, traces and torus orbits. Apply SP7 and SP6 only to this same model.',
  'Supply the actual symplectic image-density and finite automorphic catalogue with the original level, weights, duality, all embeddings and Frobenius convention; retain every necessary Fontaine/local-global cohomology and adjoint-rigidity hypothesis until proved.',
  'For CountI and CountV reuse the exact universal LemmaM/Mprime/P and rank-one results, but reconstruct the actual Kato/unitary or filtration route through its final count theorem before marking it closed.',
  'Each newly completed count can be propagated without any further PointHV assembly work: HV5/HV6/CZ6 and HV8–HV10 prove all the original field/coefficient/case/layer and finite-prime summations. Once all four counts are supplied, apply the existing TW8/OB8/VW same-window and fixed-pair chain immediately.',
  'For LinkN supply the actual local denominator table and type/theta/rank identities on the common family; LN already proves the exact all-prime restoration. Genuine theta/local installation, arithmetic gap and exact metric/spectral comparisons remain independent complete-chain targets.',
  'Preserve every earlier proof and original claim/source record; update scope additively and retire an exact target only when its entire stated human obligation is supplied.'
 ],
 'precision_notes':[
  'The reported formal verification is accepted as background. The present remaining obligations are gaps in the human reconstruction, not an allegation about the Lean development.',
  'SoFin includes arbitrary finite-order characters and every prime. SoV captures the actual continuous cocycle in a finite field; it does not assume every compact algebraic-valued set lies in a finite extension.',
  'CorX preserves the original possibly nonsurjective residue map, both inverse characters and the exact tame relative-index condition. Only the needed odd-characteristic Jacobi annihilator specialization is asserted.',
  'LemmaMprime uses an additive injection, justified by finite-cardinality comparison. LemmaM keeps the exact factor 2, finite two-sided orbit cover, integral cotangent lattice and original valuation.',
  'LemmaP is a universal theorem with its original profinite-group, local-condition and obstruction hypotheses. Closing it does not establish those hypotheses or an actual arithmetic Model.',
  'SP10 is conditional on G1, G2 and the precise finite catalogue. Model construction and point-orbit comparison are not replaced by a package name or inferred from generic automorphy.',
  'HV4 proves a direct polynomial error bound replacing the combined source redAll/lossLe route; it does not claim the exact lossAll formula. Every odd prime dividing the field degree is retained, and the error vanishes at primes outside the exceptional set.',
  'LayerLe is the source unweighted strict-Selmer sum. All finiteness conclusions precede normalized real inequalities. Constants precede hosts, fields, coefficient rings and cutoffs in the literal order.',
  'CountI/II/III/V remain actual count obligations. CountVs, CountIV, CountZ and every downstream PointHV assembly step are supplied. This does not close the global family, arithmetic gap or metric/spectral obligations.',
  'The semantic audit is a finite sufficient-condition map, not an exhaustive Lean transitive dependency graph, necessity statement or completion percentage.',
  'No new PDF or Lean build is needed. Draft-mode TeX checks syntax/references; independent mathematical reviews are bound to the final texts and source ranges.'
 ],
 'tex_front_summary':r'''\textbf{What version 0.26 achieves.}
The finite-character suppliers \texttt{SoFin} and \texttt{SoV},
the Bernoulli-unit/residual supplier \texttt{CorX}, and the full
algebra theorems \texttt{LemmaM'}, \texttt{LemmaM} and
\texttt{LemmaP} are reconstructed in their exact scopes.
HV proves \texttt{CountVs}, \texttt{CountIV} and the complete
original-field passage from the four remaining count statements
to \texttt{PointHV}.  Combined with the already proved TW/OB
branches, the cohomological window route now has exactly the
actual \texttt{CountI/II/III/V} cut.  Their arithmetic model,
catalogue, automorphy and rigidity inputs remain, as do the
common family/gap and genuine local/theta/metric/spectral work.
This is \textbf{a partial human reconstruction; the complete
human-readable proof of RH and Dirichlet GRH is not yet finished}.''',
 'tex_scope_bridge':r'''\paragraph{Version-0.26 scope of the historical conditional proofs.}
The historical proofs and their original hypotheses are preserved.
RV now supplies literal \texttt{SoFin}, \texttt{SoV} and coefficient
independence; BR supplies the entire \texttt{CorX} branch; SP supplies
\texttt{LemmaM'} and \texttt{LemmaM}, and FP supplies the universal
\texttt{LemmaP} with its exact original hypotheses.  The latter's
arithmetic installation is still required.  SP's paired-count
endpoint explicitly retains actual data/admissible-class production,
the weighted model and point-orbit comparison, and the finite
catalogue.  These are not supplied by naming generic packages.

HV supplies \texttt{CountVs}, \texttt{CountIV} and every original-field
character, case, layer and finite-prime summation step to
\texttt{PointHV}; CZ already supplies \texttt{CountZ}.  The remaining
actual count cut is \texttt{CountI/II/III/V}.  Together with TW8,
OB8 and VW this is a complete implication to the same cohomological
window and fixed-pair endpoints.  No separate \texttt{PointHV}
assembly obligation remains.  The common family/gap, genuine
theta/local state, actual denominator tables and exact metric/global/
spectral comparisons retain their original roles.  The current
frontier is in Section~\ref{sec:dependency-audit-v26} and the
version-0.26 audit.

''',
 'tex_remaining_local':r'''HP supplies its stated highest-weight and descent interfaces;
the actual form/lattice/signature and genuine theta/toric state remain.
The shared LK/TB/KB quantitative branch, TW simultaneous windows,
OB odd-minus theorem and CZ exceptional count are complete.
RV and BR now close the arbitrary finite-character, vector and
residual rank-one suppliers.  SP and FP close the literal
\texttt{LemmaM'}, \texttt{LemmaM} and \texttt{LemmaP}, with their
actual hypotheses retained where an arithmetic model is needed.

HV proves the full \texttt{CountVs}/\texttt{CountIV} suppliers and
the original-field count-to-\texttt{PointHV} assembly, including
primes dividing the field degree.  Thus the selected cohomological
frontier is the four actual \texttt{CountI/II/III/V} predicates.
For the paired symplectic counts, SP10 states exactly the remaining
data/admissible-class production, compatible model and point-orbit
comparison, and uniform finite catalogue.  Closing universal
algebra theorems does not instantiate these geometric hypotheses.
The QP classical prime-pair inputs and actual host installation
remain in their stated scopes.

LN already supplies the conditional original-family \texttt{LinkN}
chain, with restoration cost $d_j\log|G|$ and unchanged
cohomological coefficient.  Its actual local denominator tables,
type/theta/rank identities, and the stronger cut's
\texttt{NormChoiceFacts}/\texttt{Tie4} remain.  WB closes the
character, moving-cutoff and scalar consequences of its exact
arithmetic contract, and AN/GH closes the analytic implication.
The actual common gap, size/error packages, lattice-metric transport
and global/spectral operator comparisons remain.  See
Section~\ref{sec:dependency-audit-v26} for the current sufficient
map and its precisely matched classical leaves.
''',
 'tex_next_target':r'''\paragraph{The next target: install a complete actual count supplier.}
Use the now-proved \texttt{SoFin}, \texttt{SoV}, \texttt{CorX},
\texttt{LemmaM'}, \texttt{LemmaM} and \texttt{LemmaP} on their
exact original hypotheses.  For the paired symplectic route,
SP10 isolates the remaining actual data/admissible representations,
weighted model with local conditions and point-orbit comparison,
and uniform finite trace catalogue.  Its arithmetic cohomology,
image-density, automorphy and rigidity inputs must be reconstructed
on these same objects.  CountI's Kato/unitary route and CountV's
filtration route are alternative complete-chain targets.
Once all four actual counts are available, HV10 already supplies
every step to \texttt{PointHV} and the TW/OB/VW window conclusion.
The separate common arithmetic family, genuine local/theta state,
actual denominator tables, arithmetic gap and exact metric/spectral
comparisons remain independent substantive tasks.
''',
 'tex_reading_order':r'''For this increment, read RV1--RV7 for arbitrary finite-character
finiteness, vector vanishing and coefficient return; BR1--BR7 for
the full Bernoulli-unit/residual branch; and SP1--SP6 for the
complete weighted intersection algebra.  The FP chapter supplies
the universal framed-deformation presentation theorem.  Then
SP7--SP10 distinguish the completed arithmetic join from the actual
model and catalogue still required.  Finally read HV1--HV10 for
the complete original-field four-count to \texttt{PointHV} chain
and its immediate cohomological-window consequence.
Section~\ref{sec:dependency-audit-v26} records exactly what remains.
For the global spine retain WB7--WB8, AN2--AN3/GH6 and DA1--DA2.
The additive current-scope annotations identify inputs now supplied;
all historical proofs keep their original hypotheses and locators.
''',
 'tex_ledger_rows':[
  'RV1--RV7 & Full rank-one finiteness and vector vanishing & Arbitrary finite characters, original local conditions, Baire capture and exact coefficient independence.',
  'BR1--BR7 & Full Bernoulli-unit and CorX supplier & Exact dyadic threshold, finite Frobenius projection, OS1 ideal relation and original residual field.',
  'SP1--SP6 & Complete LemmaMprime and LemmaM & Additive-injection cardinalities, Rees support, orbit multiplicity and the exact factor two.',
  'SP7--SP10 & Actual cocycle and paired-count join & Exact model/cotangent edge, trace product and coefficient return; actual model and catalogue retained.',
  'FP & Full universal LemmaP supplier & Framed representability and weighted obstruction presentation under the original group and local hypotheses.',
  'HV1--HV10 & CountVs, CountIV and full PointHV assembly & Integral character comparison at every odd prime, original fields and exact four-count/window quantifiers.'
 ],
 'tex_dependency_update':r'''\section{Dependency closure after rank-one, algebra and height assembly}
\label{sec:dependency-audit-v26}

\paragraph{The rank-one branches now reach their literal endpoints.}
RV proves the complete chain from finite duality and KB8 through an
actual finite root-containing extension, a finite quotient
restriction kernel and arbitrary finite-character Selmer finiteness.
Its Baire argument uses closed subgroups defined by the cocycle;
it does not assert that an arbitrary compact subset of the algebraic
closure lies in a finite field.  One finite coefficient lattice and
an explicit limiting identity then give the actual vector coboundary.
The endpoints are \texttt{SoFin}, \texttt{SoV} and exact coefficient
independence, including nonnested rings.

BR proves the prescribed \texttt{LemmaX} by integral partial sums
and finite Frobenius projection.  The precise conductor inequality
forces a two-point contradiction in odd characteristic.  It then
uses the original tame-index condition, finite class-field
reciprocity and the already proved OS1 Jacobi ideal relation to
derive the required scalar annihilator.  The resulting residual
coboundary lies in the original residue field.  The final
\texttt{CorX} handles both characters with the exact source data.

\paragraph{Complete algebra suppliers, with arithmetic installation separate.}
SP1 proves \texttt{LemmaM'} even though its injection is only
additive.  SP2--SP6 construct the exact weighted intersection
argument: admissible multigraded Euler characteristics, the actual
Rees support, two-sided orbit slices, generic multiplicity one,
an explicit leading-form Hilbert difference and the length--norm
formula.  The lower and upper multiplicities differ by exactly
a factor two, giving the literal \texttt{LemmaM}.
FP supplies the complete universal \texttt{LemmaP}, including
representability and the actual relation/obstruction construction.
Its original profinite-group, local-condition and finite-obstruction
hypotheses remain part of that theorem; proving it does not
construct a model for an arbitrary arithmetic datum.

SP7 proves the actual \texttt{shaCoc}/\texttt{mPrime} edge on a
supplied \texttt{Model}, with additive reductions of derivation
choices justified.  SP8 gives the exact return from auxiliary
coefficients.  SP9 proves the integral trace-product bound from
the precisely quantified finite catalogue.  SP10 carries the
actual data and compatible-model hypotheses and that catalogue
through all trace, valuation, polynomial absorption and coefficient
steps to \texttt{CountII}\,$\wedge$\,\texttt{CountIII}.
The data/model/catalogue requirements remain actual obligations;
generic automorphy or a named package cannot substitute for them.

\paragraph{The complete original-field height assembly.}
HV proves an integral character inequality at every odd prime.
Finite quotient cohomology gives a polynomial error when the prime
divides the original field degree, and gives zero error outside
the exceptional prime set.  The proof keeps the original
$E,\Omega,D$, the negative twist and the normalized coefficient
length.  HV5 proves \texttt{CountVs} from a field whose degree is
bounded before the host; HV6 proves the exact unweighted
\texttt{CountIV} layer comparison.  The case partition and all
finite-prime sums are then complete, yielding
\[
 \begin{gathered}
 \mathtt{CountI}\wedge\mathtt{CountII}\wedge
 \mathtt{CountIII}\wedge\mathtt{CountV}\\
 \Longrightarrow\ \mathtt{PointHV}
 \Longrightarrow\ \forall C_t\ge1\ \forall\psi,
                              \mathtt{VWinAt}(\psi,C_t).
 \end{gathered}
\]
The second implication uses the already proved TW8 and OB8 in VW.
The fixed-pair $C_t=401$ rescaling and cutoff exponent $400$ are
unchanged.  No separate original-field assembly task remains
after the four actual counts.

\paragraph{The retained frontier.}
The actual \texttt{CountI/II/III/V}, their remaining same-object
deformation, local-global cohomology, automorphy, finite catalogue
and rigidity suppliers, and the global common family/gap, genuine
theta/local installation, denominator tables and exact
metric/spectral comparisons remain.  The current audit preserves
the historical nodes and target snapshots, records the newly
supplied interfaces and narrows the retained targets.  It is a
finite sufficient-condition map, without a claim of necessity,
minimality or a percentage of the full proof.

'''
}
(ROOT/'increment_v0_26.json').write_text(json.dumps(cfg,ensure_ascii=False,indent=2)+'\n')
print('Wrote increment_v0_26.json')
