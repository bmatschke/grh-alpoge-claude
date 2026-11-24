#!/usr/bin/env python3
"""Describe the actual symplectic data, deformation and comparison chains."""
from pathlib import Path
import json

ROOT = Path(__file__).resolve().parent
components = ['symplectic_arithmetic_data', 'symplectic_local_installation',
              'symplectic_model_construction', 'symplectic_model_comparison']
scope = (
    'Partial human reconstruction of RH and Dirichlet GRH, prioritizing complete dependency chains. '
    'AX constructs actual Raw/Good/OfCase data on the given coefficient ring when the required dyadic roots are present, or on the permitted finite extension with SP8/RV1 normalized return to the given ring, and proves their literal ordinary, level, dual and unlinking properties. '
    'Under the retained SymplecticFourImageDense predicate it supplies SP10 G1, with one common complex embedding before all irreducible points. '
    'DX installs the original PhiCond, Nums and LocBase from finite duality and explicit ordinary/finite-inertia deformations. '
    'MX constructs an actual Model over the coefficient ring of every original Good datum, including its two gradings, characteristic-zero chart, integral cuts and cocycle-to-derivation fields. '
    'PX closes the internal weighted-algebra, point, orbit, tangent and trace comparison and the actual D.Ineq from same-datum Fin0, NoEnd and AllIrr RigidAt. '
    'Thus the paired CountII/III route retains image-density, actual irreducible rigidity and the precise uniform automorphic catalogue; the arithmetic model and its internal comparison are supplied. '
    'The CountI/II/III/V cut and its already complete HV/TW/OB/VW downstream assembly remain. '
    'The common family/gap, genuine theta/local state, actual denominator tables and exact metric/spectral comparisons remain separate obligations. '
    'All historical proofs and original claim/source records are preserved. No full human RH/Dirichlet-GRH proof, new Lean build or independent kernel replay is claimed.'
)
new = [
    'AX1–AX5: the complete original-field auxiliary construction for both symplectic cases. Primitive dyadic characters, the quantitative conductor choice, Frobenius/inertia elements, residual vanishing and literal Raw/Good/OfCase are constructed. The given coefficient ring is used when it contains the required roots; otherwise SP8/RV1 permits a finite extension and proves the normalized return to the given ring.',
    'AX6–AX10: the actual normalization, level, ordinary-point, dual and safe unlinking properties. The image-density predicate supplies Fin0, NoEnd and one common complex embedding for all irreducible points; under precisely that retained input AX10 closes SP10 G1.',
    'DX1–DX4: finite local/global duality and Euler formulas are matched to the original places and coefficient twists; the explicit permutation-cocycle argument supplies PhiCond. Exact framed cochain and obstruction sequences give the literal Nums, including all weight dimensions and vanishing.',
    'DX5–DX8: actual local representability, the ordinary and finite-inertia characteristic-zero charts, the precise tangent condition tanLz, and the original LocBase are supplied. The full BlochKatoLocal package is not used as an unexplained model-construction premise.',
    'MX1–MX10: the complete actual Model constructor. It verifies the five inertia local-condition axioms, applies FP to the original frame, forms homogeneous cuts on a rational chart, constructs a domain quotient with the required OnComp witnesses, and supplies the representation-generation and all integral cocycle-to-derivation fields. DX supplies its actual arithmetic hypotheses.',
    'PX1–PX5: the first-weight-zero algebra, exact cotangent dimensions, TanGlob, quotient, arbitrary point lifting, finite entry generation and integral point scaling. A formal invariant-chart argument replaces the longer source calculation without changing the integral cotangent lattice.',
    'PX6–PX10: actual point classification, the two-sided irreducibility criterion, diagonal-conjugacy and torus-orbit comparison, infinitesimal lifting and rigidity, and the integral trace/cotangent inequality. The endpoint is literal D.Ineq under same-D Fin0, NoEnd and AllIrr RigidAt, with the exact factor two and original valuation.',
    'The paired-count frontier is now the exact image-density predicate, actual rigidity of every irreducible point on the same constructed datum, and SP9’s uniformly quantified finite automorphic catalogue. The source rigSp4_alt producer, including its local Hodge/adjoint prerequisites, remains to be reconstructed. No actual CountII/III supplier is yet promoted.'
]
remaining = [
    'The literal actual CountI, CountII, CountIII and CountV on original hosts and coefficient data. CountVs, CountIV and CountZ, and every downstream original-field PointHV assembly step, are already supplied. One uniform count exponent must precede hosts and fields.',
    'For the paired CountII/III route: SymplecticFourImageDense on the original datum, actual AllIrr RigidAt on that same datum, and the precise uniform conjugation-stable finite catalogue in SP9. AX closes the remaining data/ordinary/level/dual construction, DX/MX supply Model, and PX supplies its internal comparison. Fin0 and NoEnd come from the retained image-density predicate. The full source rigSp4_alt implication, including any required local Hodge and adjoint-vanishing joins, remains an explicit continuation target.',
    'The finite automorphic catalogue must preserve the original level, weights, duality, every embedding, Frobenius convention and quantifier order; its uniform bound precedes varying primes, fields, embeddings and point families. No generic finiteness slogan supplies this contract.',
    'CountI’s Kato/unitary route and CountV’s filtration route retain their actual compatible automorphy, adjoint/rigidity, congruence-number and local-global comparison inputs. Shared rank-one, algebra and finite cohomology suppliers should be substituted only where their original hypotheses match.',
    'One actual common family satisfying HostExW/DesignExists and its dependent layout, coefficient maps, St/ColPin/R3.Read, rational good-row spectrum and remaining Core fields. The new arithmetic deformation model does not construct that separate global geometric family.',
    'Genuine compatible theta/toric/local installation: nonzero theta maps, convergence and separation, critical toric ratios, Choice.FieldOK, NTh/NChoice/ChoiceSide/NdSpec/LocAll and actual operator identities. Their substantive fields remain required.',
    'The actual local Galois denominator tables and original type/e0 action, parameter dictionaries, localization/theta composition and rank bindings in LN. NormChoiceFacts and Tie4 remain actual supplier obligations. LN already proves the conditional scalar/cut/restoration chain with exact cost d_j log|G| and unchanged cohomological coefficient.',
    'The actual common arithmetic gap and all SizeData2/ErrWindows/BNBounds and IdentU readings on that same family. WB supplies the downstream character, moving-cutoff and scalar chain, and AN2/AN3/GH6 its analytic endpoint, from the exact arithmetic contract.',
    'Actual source/target lattices and metrics, NprimeMuR/LinkMu transport and retained/discarded rank compatibility, together with global/spectral comparisons for the actual operators: normalized finite-word and Poisson statements, image/norm comparisons, kernel/mass identities, Gram bounds and exceptional terms.',
    'Precisely matched classical citation leaves remain explicit. In this increment finite Tate/Poitou–Tate duality, Euler formulas, class-field theory and elementary complete-local algebra are specialized to the original objects; their full general theories are not reproved from first principles.'
]
updates = {
    'FP8': {'supplied_by': ['DX2', 'DX4', 'DX8', 'MX2', 'MX3', 'MX10'],
            'closure': 'The universal theorem retains its exact hypotheses. DX and MX now verify them on every original Good symplectic datum and complete an actual Model; this is a new arithmetic specialization, not a change to the historical universal statement.'},
    'SP7': {'supplied_by': ['DX8', 'MX9', 'MX10', 'PX1', 'PX3', 'PX10'],
            'closure': 'The formerly supplied-Model cocycle/cotangent comparison is now available on the actual constructed Model. Its integral lattice and original valuation are retained.'},
    'SP10': {'supplied_by': ['AX10', 'DX8', 'MX10', 'PX10'],
             'closure': 'G1 is supplied under the literal retained SymplecticFourImageDense predicate. Actual Model construction and all internal G2 comparison steps are supplied; PX10 uses same-D Fin0, NoEnd and AllIrr RigidAt. Image-density supplies the first two, while actual irreducible rigidity and the exact SP9 catalogue remain. Actual CountII/III are not yet closed.'},
    'VW3': {'supplied_by': ['AX10', 'DX8', 'MX10', 'PX10', 'HV10', 'TW8', 'OB8'],
            'closure': 'The four-count sufficient cut remains CountI/II/III/V. The paired-count data/model/comparison obligations have been reconstructed, retaining image-density, actual same-datum irreducible rigidity and the exact uniform catalogue. All downstream original-field PointHV and window assembly remains supplied.'},
    'GH7': {'supplied_by': ['AX10', 'DX8', 'MX10', 'PX10', 'HV10', 'TW8', 'OB8'],
            'closure': 'The actual symplectic deformation construction and internal comparison now join the previously closed shared algebra/cohomology and height-assembly chains. Actual four counts, their retained image/rigidity/catalogue/automorphy inputs, and common family/gap/local/metric/spectral work remain.'}
}
cfg = {
    'artifact_version': '0.27', 'date': '2026-11-22', 'predecessor_version': '0.26',
    'components': components, 'tex_component_order': components, 'scope': scope,
    'new_in_this_version': new, 'remaining_major_inputs': remaining, 'claim_updates': updates,
    'completed_previous_frontier': 'Actual symplectic Raw/Good/OfCase data, PhiCond/Nums/LocBase installation, Model construction and all internal weighted point/orbit/tangent/trace comparisons are supplied in their exact scopes. G1 retains image-density; the final D.Ineq retains actual Fin0/NoEnd/irreducible rigidity.',
    'next_local_priority': 'Close the remaining same-object symplectic image-density, actual irreducible rigidity and precise uniform automorphic-catalogue chains, then apply SP9/SP10 to CountII and CountIII. Do not reopen the constructed Model, its local charts, point-orbit comparison or the already closed PointHV assembly.',
    'next_steps': [
        'Read dependency_audit_v0_27/obligation_map.json and its exact source targets. The map distinguishes proved constructors, conditional joins, retained arithmetic predicates and classical citation leaves.',
        'Reconstruct the literal SymplecticFourImageDense route with its original residual conditions and all embeddings. AX10 then supplies both Fin0 and NoEnd and one common complex embedding before all irreducible admissible points.',
        'Reconstruct the complete rigSp4_alt producer of actual AllIrr RigidAt, including the local Hodge/adjoint joins it uses. Match every original PtInKeps point and the same Raw datum; a standalone RigiditySymplecticFour label does not yet supply this implication.',
        'Prove the exact SP9 uniform finite catalogue with the original conductor/level, weights, duality, Frobenius traces and embedding quantifiers. Combine it immediately with AX10, MX10, PX10 and SP10 to close the paired actual counts.',
        'For CountI and CountV reuse the exact rank-one/algebra/finite-cohomology suppliers where applicable, and carry the actual Kato/unitary or filtration route through its final count theorem.',
        'Once all four actual counts are supplied, HV10 already gives every original-field, character, case, layer and prime-summation step to PointHV, followed by TW8/OB8/VW to the common window and fixed-pair conclusion.',
        'Preserve the independent global common-family, genuine theta/local, denominator, arithmetic-gap and exact metric/spectral obligations. Retire an exact target only when its entire stated human scope is supplied; preserve all earlier proof and source records.'
    ],
    'precision_notes': [
        'The reported formal verification is accepted as background. Remaining tasks concern the human reconstruction, not alleged gaps in the Lean development.',
        'AX constructs both cases on the given coefficient ring when the required dyadic roots are present; otherwise it uses the permitted finite extension with SP8/RV1 normalized coefficient return. DX/MX/PX preserve the coefficient ring of that actual datum throughout. AX10 retains the literal image-density predicate and its one common embedding for the full irreducible family.',
        'DX’s local/global finite duality includes the original coefficient twist and normalization. The global Euler formula is the truncated H0/H1/H2 formula, also at 2; high-degree real-place vanishing is claimed only in its odd-prime scope.',
        'DX6–DX8 and MX use characteristic-zero completed charts exactly as SmoothPt requires. Neither integral formal smoothness nor the full BlochKatoLocal package is inferred.',
        'MX preserves the coefficient ring of its input datum, integral cotangent lattice, local conditions, every preimage in the entry identities, and every actual cocycle in the cocycle-to-derivation field.',
        'PX’s shorter invariant-chart proof preserves all integral data. The rational completion is used for chart dimensions; it is not a license to replace integral modules by their rationalizations in length inequalities.',
        'PX10 assumes the actual same-D Fin0, NoEnd and AllIrr RigidAt predicates. It does not prove that RigiditySymplecticFour alone yields the last predicate. The full rigSp4_alt producer remains a target.',
        'The final factor is exactly two. Trace values, finite orbit covers, conjugacy classes, valuation normalization and coefficient return are matched on the same constructed objects.',
        'CountI/II/III/V remain actual count obligations. CountVs/IV/Z and all downstream PointHV/window assembly are already supplied. The separate common geometric family and exact metric/spectral obligations remain.',
        'The semantic audit is a finite sufficient-condition map, not an exhaustive Lean transitive dependency graph, a necessity statement or a completion percentage.',
        'No new PDF or Lean build is needed. Draft-mode TeX checks syntax and references; mathematical reviews are independently bound to the final texts and source ranges.'
    ],
    'tex_front_summary': r'''\textbf{What version 0.27 achieves.}
The paired symplectic count route now has its actual auxiliary
\texttt{Raw/Good/OfCase} data, local cohomology and deformation
charts, and a complete \texttt{Model} construction over the
coefficient ring of that datum.  If the given ring lacks the
required dyadic roots, AX uses the permitted finite extension
with the already proved normalized coefficient return.
The weighted algebra, integral point lifting,
point classification, torus-orbit comparison, tangent calculation
and trace/cotangent inequality are reconstructed.  The remaining
paired-count cut is the exact image-density predicate, actual
irreducible rigidity on that same datum, and the uniform finite
automorphic catalogue.  \texttt{CountII/III} are not yet supplied.
The four-count to \texttt{PointHV} and cohomological-window chain
was already completed in version 0.26.  The common family/gap and
genuine local/theta/metric/spectral work retain their separate roles.
This is \textbf{a partial human reconstruction; the complete
human-readable proof of RH and Dirichlet GRH is not yet finished}.''',
    'tex_scope_bridge': r'''\paragraph{Version-0.27 scope of the historical conditional proofs.}
AX now constructs the original auxiliary symplectic data for both
cases and proves the ordinary, level, dual and safe unlinking
properties.  It uses the given coefficient ring when the required
dyadic roots are present, or the permitted finite extension with
SP8/RV1 normalized return otherwise.  DX/MX/PX keep the ring of
this actual datum throughout.  Its G1 conclusion retains exactly
\texttt{SymplecticFourImageDense}.  DX supplies the original
\texttt{PhiCond}, \texttt{Nums} and \texttt{LocBase}; MX uses them
to construct a literal \texttt{Model} for every original good datum.
The charts are characteristic-zero charts with their integral
lattices retained, not assertions of integral formal smoothness.

PX proves the internal G2 comparison through the actual
\texttt{D.Ineq} under the same datum's \texttt{Fin0},
\texttt{NoEnd} and \texttt{AllIrr RigidAt}.  Image-density supplies
the first two predicates; actual irreducible rigidity and the exact
SP9 catalogue remain.  The source \texttt{rigSp4\_alt} producer,
including its local Hodge/adjoint joins, is still a separate target.
The full \texttt{BlochKatoLocal} package is not required for the
new model construction, but no unused part of it is promoted.

The actual count cut remains \texttt{CountI/II/III/V}.  HV/TW/OB/VW
already supplies every subsequent height/window assembly step.
The common arithmetic family, genuine theta/local state, actual
denominator tables, arithmetic gap and exact metric/global/spectral
comparisons remain independent substantive obligations.  Historical
proofs retain their original hypotheses; the current frontier is in
Section~\ref{sec:dependency-audit-v27} and the version-0.27 audit.

''',
    'tex_remaining_local': r'''The original highest-weight/descent interfaces and the shared
cohomology, rank-one, residual and universal algebra suppliers
retain their proved scopes.  AX/DX/MX now install the actual
symplectic data and local deformation theory and construct the
original \texttt{Model}.  PX supplies its complete internal
weighted point/orbit/tangent/trace comparison.

The paired \texttt{CountII/III} route therefore retains the exact
image-density predicate, actual irreducible rigidity on the same
datum, and SP9's uniformly quantified finite automorphic catalogue.
The full \texttt{rigSp4\_alt} producer remains to be reconstructed.
The selected cohomological frontier is still the four actual
\texttt{CountI/II/III/V} predicates; HV supplies every original-field
step from them to \texttt{PointHV}, and TW/OB/VW its window endpoint.
The QP classical prime-pair inputs and actual host installation
retain their original roles.

LN already supplies the conditional original-family \texttt{LinkN}
chain with exact restoration cost $d_j\log|G|$.  Actual local
denominator tables, type/theta/rank identities,
\texttt{NormChoiceFacts}/\texttt{Tie4}, the common arithmetic gap,
size/error readings, lattice-metric transport and global/spectral
operator comparisons remain.  See
Section~\ref{sec:dependency-audit-v27} for the current sufficient
map and precisely matched classical leaves.
''',
    'tex_next_target': r'''\paragraph{The next target: close the remaining paired-count inputs.}
Use AX10, DX8, MX10 and PX10 on their exact original hypotheses.
The auxiliary datum, local charts, full model and internal
point-orbit/tangent/trace comparison are supplied.  Reconstruct the
literal image-density route, the complete producer of actual
irreducible rigidity, and the uniformly quantified SP9 catalogue.
These are required on the same datum and with the same embedding,
level, weights and Frobenius convention.  Then apply SP10 to both
actual counts.  CountI's Kato/unitary route and CountV's filtration
route remain complete-chain targets of their own.
Once all four counts are supplied, HV10 and TW/OB/VW already give
the entire height/window conclusion.  The separate common family,
genuine theta/local state, denominator, arithmetic-gap and exact
metric/spectral obligations retain their original roles.
''',
    'tex_reading_order': r'''For this increment, read AX1--AX10 for the actual symplectic datum
and its ordinary, level, dual and admissibility properties.  Read
DX1--DX8 for the finite duality calculation, exact framed dimensions
and original local charts.  MX1--MX10 then construct the full
\texttt{Model}, including the integral cuts and all cocycle-derived
derivations.  PX1--PX10 carry this model through its weighted algebra,
points, torus orbits, infinitesimal rigidity and trace inequality.
Return to SP9--SP10 for the exact remaining uniform catalogue and
paired-count join, then to HV10 and TW/OB/VW for the already closed
downstream height/window chain.
Section~\ref{sec:dependency-audit-v27} records the precise remaining
predicates.  For the global spine retain WB7--WB8, AN2--AN3/GH6 and
DA1--DA2; the global family, gap and metric/spectral interfaces remain.
''',
    'tex_ledger_rows': [
        'AX1--AX10 & Actual symplectic data and G1 & Original ring, both cases, ordinary/level/dual/unlinking properties; image-density retained.',
        'DX1--DX8 & Original arithmetic local installation & Exact finite duality, framed dimensions, ordinary and finite-inertia charts and tangent conditions.',
        'MX1--MX10 & Complete actual Model constructor & All local axioms, homogeneous integral cuts, domain chart and cocycle-to-derivation fields.',
        'PX1--PX10 & Complete internal model comparison & Invariant chart, actual points and orbits, tangent rigidity and exact trace bound; actual arithmetic predicates retained.'
    ],
    'tex_dependency_update': r'''\section{Dependency closure after actual symplectic model construction}
\label{sec:dependency-audit-v27}

\paragraph{The original arithmetic datum is now constructed.}
AX carries the quantitative dyadic-character choice and the
previous residual vanishing theorem through both cases of the
literal \texttt{Raw/Good/OfCase} construction.  Required roots
are taken in the given coefficient ring, or in the permitted
finite extension with SP8/RV1 normalized coefficient return.
Its later arguments
prove the actual ordinary-point condition, level, duality and
safe unlinking fields.  One common complex embedding is chosen
before every irreducible point under exactly the retained
\texttt{SymplecticFourImageDense} predicate.  This supplies SP10's
G1 in that stated scope.

\paragraph{The deformation theorem is installed on those objects.}
DX proves the exact finite local/global duality and Euler
specializations, the global and local \texttt{PhiCond}, and the
literal framed \texttt{Nums}.  Explicit ordinary and finite-inertia
deformations give the required characteristic-zero charts and
the exact tangent restriction.  They supply the original
\texttt{LocBase}; the full \texttt{BlochKatoLocal} package is not
an unexplained premise of this construction.

MX then closes the whole constructor: inertia local conditions,
universal framed presentation, homogeneous cuts, a domain quotient
with actual \texttt{OnComp} witnesses, representation generation,
and integral derivations attached to every actual Selmer cocycle.
The coefficient ring, cotangent lattice, matrix normalizations and
all preimage quantifiers are retained.  The result is an actual
\texttt{Model} for every original good symplectic datum.

\paragraph{The internal comparison reaches the arithmetic inequality.}
PX replaces the long invariant-chart calculation by a formal
weight-pairing argument and proves all required integral
generation and scaling statements.  It classifies the actual
points, identifies the two-sided irreducible locus, turns
conjugacy into the prescribed torus orbit, lifts tangent
derivations and applies the actual rigidity predicate.  The
previous weighted intersection theorem then gives the exact
factor-two trace/cotangent bound and the literal \texttt{D.Ineq}.
This last implication retains exactly the same datum's
\texttt{Fin0}, \texttt{NoEnd} and \texttt{AllIrr RigidAt}.

\paragraph{The remaining paired-count cut is explicit.}
A sufficient remaining input is the conjunction of
\texttt{SymplecticFourImageDense}, actual irreducible rigidity on
each constructed datum, and SP9's exact uniform finite
automorphic catalogue.  Image-density supplies \texttt{Fin0},
\texttt{NoEnd} and admissibility with a common embedding.  The
source \texttt{rigSp4\_alt} implication, including any required
local Hodge/adjoint inputs, is still a continuation target; merely
naming \texttt{RigiditySymplecticFour} does not close it.
Uniform catalogue bounds must precede the varying prime, original
field, embedding and representation family.

\texttt{CountII/III} remain open in the human reconstruction until
these inputs are supplied.  So do \texttt{CountI} and \texttt{CountV}.
HV10 and TW/OB/VW already close the entire downstream height/window
implication from the four-count cut.  The common geometric family,
arithmetic gap, genuine theta/local installation, actual denominator
tables and exact metric/global/spectral comparisons remain separate.
The machine-readable semantic map is a finite sufficient-condition
audit, not an exhaustive Lean dependency graph or a completion
percentage.  Every historical proof and original source record is
preserved, with additive current-scope annotations.

'''
}
(ROOT / 'increment_v0_27.json').write_text(json.dumps(cfg, ensure_ascii=False, indent=2) + '\n')
print(ROOT / 'increment_v0_27.json')
