#!/usr/bin/env python3
"""Record one complete case-II chain and the exact remaining support producer."""
from pathlib import Path
import json

ROOT = Path(__file__).resolve().parent
components = ['symplectic_universal_arithmetic','symplectic_modular_support',
              'symplectic_automorphic_seeds','symplectic_promodular_realization',
              'case_two_installation']
scope = (
 'Partial human reconstruction of RH and Dirichlet GRH, prioritizing complete dependency chains. '
 'KX supplies literal LevEx, LocCFTAll, LamEx, PhiAll and ProModularRingExists, with the exact universal maps and the source nonempty-Pair antecedent. '
 'QX supplies the literal adjoint lifting theorem, characteristic-zero support, actual two-Link and IsPhi constructions, and the five-clause PMExAlt join from a precisely restricted actual rank-four ordinary Hecke/support input. '
 'SX constructs the literal SeedIIAlt, including a cuspidal ordinary Hilbert congruence, fixed-central weight change, integral induced matrices, exact residual entries, local flags and the actual automorphic witness. '
 'UX supplies the entire original case-II ProModAlt witness from SeedIIAlt and PMExAlt: towers, lattices, three residual lines, uniform cohomology bounds, actual Space and completions, component propagation and coefficient descent. '
 'YX closes PMExAlt implies CountII through the original same-datum image-density, model, rigidity, catalogue and normalized count joins. '
 'The actual rank-four Hecke/support producer, the case-IV seed and case-III promodularity, CountI and CountV, and the separate common-family/gap, theta/local, denominator and metric/spectral branches remain. '
 'Historical proofs, original claim/source records and dependency edges are preserved. No full human RH/Dirichlet-GRH proof, new Lean build or independent kernel replay is claimed.'
)
new = [
 'KX1–KX9: actual local coefficient maps; complete arithmetic levels; local reciprocity with the prescribed torsion condition; exact inertia-character weight algebra; Phi for the actual global/local groups; a universal determinant over the actual coefficient DVR; and the literal universal ordinary Pair ring and weight-map triangle. Pair relations are kept distinct from the stronger Hecke RingProps.',
 'QX: exact AdjointLiftingTheorem by a matched polarized adjoint-Selmer theorem, regular-local characteristic-zero support, actual two Links and IsPhi maps, and the full five-clause potential-modularity tower join. The retained input is narrowed to actual rank-four HidaPropsAlt ideals and P1core on those two residual Links, with the common coefficient threshold and fixed embedding. P3core is not needed by this join.',
 'SX1–SX8: the literal SeedIIAlt. Mixed ordinary refinements exclude every Eisenstein lift; fixed-central Hida control supplies the two different local weight pairs; an explicit Ribet lattice and induced symplectic basis give the exact residual root-entry alternative. The same tower, ordered local flags, correcting character, coefficient maps and embedding are retained.',
 'UX1–UX12: full case-II promodularity from SeedIIAlt and PMExAlt. The construction includes every intermediate original object: tame/deep towers, the lattice shape, the three polynomial residual links, coefficient-uniform bounds, actual Space and flat universal completions, quantitative component propagation, and the final valued point annihilating the actual ideal.',
 'YX1–YX2: the complete conditional chain PMExAlt implies the actual CountII. SX8 supplies the seed and UX12 supplies promodularity; IX, AX/DX/MX/PX, RX, CX and SP then give every same-datum image-density, rigidity, catalogue, length and coefficient-return step. CountI, CountIII, CountV and PMExAlt consequently suffice for PointHV.',
 'A separate ordinary-support dependency audit follows the exact remaining Hida/patching producer. It records every field of HidaPropsAlt and why a generic dense set, an unrelated finite quotient, or an unmatched residually Schur theorem cannot replace the required input.'
]
remaining = [
 'The actual rank-four ordinary Hecke/support input on QX’s two constructed Links: one uniform coefficient threshold, actual HidaPropsAlt (ring, dense, pt, end1, end2, twist) and P1core, for every later coefficient DVR and every actual universal B/Lambda. QX supplies the downstream PMExAlt join, not this arithmetic producer.',
 'The literal SeedIVAlt and the complete case-III ProModAlt construction. SX8 supplies SeedIIAlt only, and UX12 covers Ctx2 only. The historical targets combining II/IV seeds and II/III promodularity therefore retain their unsupplied scopes.',
 'Actual CountI, CountIII and CountV for the selected YX2 height route. CountII is proved conditionally on PMExAlt; JX’s alternative full-image-density route remains valid with its original hypotheses. No unconditional CountII or PointHV assertion is made.',
 'One actual common family satisfying HostExW/DesignExists and its dependent layout, coefficient maps, St/ColPin/R3.Read, rational good-row spectrum and remaining Core fields.',
 'Genuine compatible theta/toric/local installation: nonzero theta maps, convergence and separation, critical toric ratios, Choice.FieldOK, NTh/NChoice/ChoiceSide/NdSpec/LocAll and the actual operator identities.',
 'Actual local Galois denominator tables, original type/e0 action, parameter dictionaries, localization/theta composition, rank bindings, NormChoiceFacts and Tie4. The existing conditional LinkN chain retains the exact restoration cost d_j log|G|.',
 'The actual common arithmetic gap and all SizeData2/ErrWindows/BNBounds and IdentU readings on that same family; the existing downstream scalar and analytic implications retain their exact arithmetic contract.',
 'Actual source/target lattices and metrics, NprimeMuR/LinkMu transport and rank compatibility, plus normalized finite-word, Poisson, image/norm, kernel/mass, Gram and exceptional-term comparisons for the actual operators.',
 'Matched classical theorem leaves remain explicit. The full original HidaUAlt, ModUAlt, HypothesesH\u0027, LiteratureRankNHypothesis, all-rank CountQAlt and unchanged-level LevelPNAlt are not inferred from the selected rank-four consequences.'
]
updates = {
 'AX10':'YX supplies its pointwise G1 use on every Ctx2 datum from PMExAlt, with the original level, weights and common embedding. The original full two-case AX10 statement and all its hypotheses remain unchanged.',
 'PX10':'YX2 supplies Fin0, NoEnd and actual pointwise RX6 rigidity on the same Ctx2 datum from PMExAlt, then applies this unchanged cotangent/trace comparison.',
 'SP10':'YX2 now closes the complete original Case-II count chain conditional only on PMExAlt. The original paired-count claim and its broader hypotheses are preserved; Case III remains a separate input.',
 'IX9':'KX and QX supply actual universal rings, Links, IsPhi and the downstream support join subject to the exact rank-four Hecke/support producer. The original finite-fibre implication is unchanged.',
 'IX10':'UX12 now supplies its actual ProModAlt premise on every Ctx2 datum from PMExAlt and the actual SX8 seed; YX1 installs the resulting full case-II endpoint at one fixed embedding. Case III is not inferred.',
 'JX1':'The original full-image-density implication to both counts remains. YX2 supplies the stronger specialized route PMExAlt implies CountII, using the actual SX8 and UX12 case-II producers.',
 'JX2':'The original CountI/CountV/full-image-density sufficient cut remains. YX2 adds the sufficient cut CountI, CountIII, CountV and PMExAlt, because its entire case-II chain is now reconstructed.',
 'HV10':'YX2 supplies its CountII premise conditionally on PMExAlt; the other actual CountI, CountIII and CountV inputs remain explicit, with the unchanged original-field quantifier order.',
 'VW3':'YX2’s CountI/CountIII/CountV/PMExAlt sufficient cut propagates through the existing HV/TW/OB window assembly with the previously stated prime-pair hypotheses.',
 'VW4':'The added YX2 sufficient cut retains the same Ct=401 specialization and cutoff exponent 400; actual remaining counts, PMExAlt and prime-pair inputs remain explicit.',
 'GH7':'The selected cohomological route gains the complete conditional case-II chain. The separate actual family, gap, theta/local and metric/spectral obligations retain their original roles.'
}
cfg = {
 'artifact_version':'0.29','date':'2026-11-22','predecessor_version':'0.28',
 'components':components,'tex_component_order':components,
 'scope':scope,'new_in_this_version':new,'remaining_major_inputs':remaining,'claim_updates':updates,
 'completed_previous_frontier':[
  'Literal arithmetic/universal-ring packages LevEx, LocCFTAll, LamEx, PhiAll and ProModularRingExists are supplied by KX.',
  'Literal AdjointLiftingTheorem and the downstream actual two-Link/support join are supplied by QX with its narrowed arithmetic producer explicit.',
  'Literal SeedIIAlt is supplied by SX8 on every original permitted tower and fixed embedding.',
  'The full original Ctx2 promodular witness is supplied by UX12 from the actual seed and PMExAlt.',
  'YX closes PMExAlt implies CountII, including all original point, count and coefficient-return joins. Compound historical targets retain their unsupplied Case-IV and Case-III scope.'
 ],
 'next_local_priority':'Reconstruct the actual rank-four HidaPropsAlt plus P1core producer on QX’s two Links, preserving its common threshold and every later-coefficient/universal-ring quantifier. QX and YX then propagate it through the complete case-II chain to CountII. Next close SeedIVAlt and case-III promodularity as a separate complete chain.',
 'next_steps':[
  'Follow ordinary_support_dependency_audit from the actual Hecke module and ideal through every HidaPropsAlt field and P1core; retain exact original residual hypotheses and coefficient thresholds.',
  'Substitute that producer into QX’s five-clause PMExAlt join and immediately apply YX2 for the unconditional original CountII. No further case-II seed, model, rigidity or catalogue supplier is needed on that route.',
  'Construct literal SeedIVAlt and the entire case-III promodular witness, preserving the common embedding and every residual-pattern quantifier, then use the existing downstream image-density/count joins.',
  'Continue CountI and CountV through their complete actual Kato/unitary and filtration endpoints, using existing suppliers only in their proved scopes.',
  'Retain the separate actual common-family, arithmetic-gap, theta/local, denominator and metric/spectral branches and the original window prime-pair hypotheses.'
 ],
 'precision_notes':[
  'The reported formal verification is accepted as background; these are human reconstruction obligations.',
  'KX’s universal Pair ring retains its nonempty-Pair antecedent and is not the stronger RingProps/Hecke ideal. Its determinant argument includes the source degree-zero and truncated-coefficient conventions.',
  'QX proves the literal adjoint theorem but does not promote the entire original H\u0027, all-rank ModUAlt or HidaUAlt packages. The actual rank-four HidaPropsAlt plus P1core input is uniformly quantified; P3core is unused.',
  'SX’s cusp is proved by incompatible local ordinary refinements. The geometric/arithmetic character inversion, dual/twist, fixed central character, residual root entries, literal muOf and AllWin clauses are explicit.',
  'UX supplies actual universal spaces with flags, polynomial lines, flat completions, coefficient-uniform dimensions, exact-residue local descent and the original ordered inertia equalities. An abstract support isomorphism would not suffice.',
  'YX proves PMExAlt implies CountII, not unconditional CountII. It reruns the original joins pointwise on Ctx2; it does not substitute a case-II restriction for a full two-case antecedent.',
  'The selected added height cut is CountI, CountIII, CountV and PMExAlt, with the established prime-pair inputs for the window. The earlier JX sufficient cut remains valid.',
  'Compound historical targets are retained until their complete stated scopes are supplied. Zero exact retirements is compatible with closing a substantial proper subchain.',
  'All historical claim fields, source arrays and edges are preserved. Semantic updates are additive, include previous snapshots, and describe sufficient dependencies rather than a necessity claim or completion percentage.',
  'No new Lean build or PDF is required. Draft-mode TeX verifies syntax/references; mathematical reviews bind final proof and provenance bytes.'
 ],
 'tex_front_summary':r'''\textbf{What version 0.29 achieves.}
One complete case-II chain is now reconstructed:
\texttt{PMExAlt}$\Rightarrow$\texttt{CountII}.
The intermediate seed is an actual cuspidal ordinary automorphic
construction, and the promodular witness is built on the original
valued point through three explicit residual lines and one common
deformation space.  The existing rigidity, catalogue, local algebra
and normalized coefficient return complete the count.

The arithmetic and universal-ring packages are also supplied, as is
the literal adjoint lifting theorem.  The five-clause tower join is
reduced to actual rank-four ordinary Hecke ideals and their precise
support property on two constructed Links.  That arithmetic producer
remains.  The case-IV seed, case-III promodularity, other counts and
the separate family/gap/theta/local/metric/spectral branches retain
their roles.  This is \textbf{a partial human reconstruction; the full
human-readable RH and Dirichlet-GRH proof is not yet finished}.''',
 'tex_scope_bridge':r'''\paragraph{Version-0.29 scope of the historical conditional proofs.}
KX supplies \texttt{LevEx}, \texttt{LocCFTAll}, \texttt{LamEx},
\texttt{PhiAll} and \texttt{ProModularRingExists}, retaining the
last statement's original nonempty-pair antecedent.  QX supplies
the literal adjoint lifting theorem and the complete downstream
two-Link/support join.  Its actual rank-four ordinary Hecke ideals
and \texttt{P1core} producer remain explicit.

SX8 supplies \texttt{SeedIIAlt}.  UX12 supplies every clause of
the original case-II \texttt{ProModAlt} witness from that seed and
\texttt{PMExAlt}.  YX then applies the existing original-point,
rigidity, catalogue and count machinery to prove
\texttt{PMExAlt}$\Rightarrow$\texttt{CountII}.
It makes only pointwise case-II substitutions in the older proofs;
their full two-case statements and original hypotheses remain.
The added sufficient height cut is \texttt{CountI},
\texttt{CountIII}, \texttt{CountV} and \texttt{PMExAlt}.

The compound historical seed and promodularity targets retain
their unsupplied case-IV and case-III scope.  Current supplier
replacements are additive and recorded in
Section~\ref{sec:dependency-audit-v29}.  The separate actual
family, gap, theta/local, denominator and metric/spectral
obligations remain substantive.

''',
 'tex_remaining_local':r'''The entire case-II seed and promodularity construction is supplied
by SX and UX.  Together with the prior BX/IX/AX/DX/MX/PX/RX/CX/SP
suppliers, YX proves \texttt{PMExAlt}$\Rightarrow$\texttt{CountII}.
KX and QX supply the universal objects, adjoint theorem and full
five-clause join from the exact actual rank-four Hecke/support input.
Constructing that input remains the next arithmetic producer.

Case III still requires its case-IV seed and its full promodular
construction.  The added height cut retains \texttt{CountI},
\texttt{CountIII}, \texttt{CountV} and \texttt{PMExAlt}; the
established downstream window keeps its prime-pair hypotheses.
The actual denominator tables, \texttt{NormChoiceFacts}/\texttt{Tie4},
common family, gap, genuine theta/local installation and exact
metric/global/spectral comparisons remain on their original branches.''',
 'tex_next_target':r'''Construct the actual rank-four ordinary Hecke ideals and
\texttt{P1core} on QX's two Links, with the common coefficient
threshold before every later universal ring.  The supplementary
ordinary-support audit records the precise source producers and
all six \texttt{HidaPropsAlt} fields.  QX and YX already supply
the complete path from that input through \texttt{PMExAlt} to
\texttt{CountII}.  Then close the case-IV seed and case-III
promodularity as a complete second chain.  Continue the other
actual counts and the independent family/gap/theta/local/metric
branches without changing their original scopes.''',
 'tex_reading_order':r'''For the new complete chain read SX (the actual case-II seed),
UX (the original promodular witness), and YX (the original count).
KX constructs the universal arithmetic objects; QX proves the
adjoint and five-clause tower joins and specifies their exact
remaining ordinary Hecke/support producer.  BX/IX supply the
cohomology and image-density transport, AX/DX/MX/PX the actual
model and comparison, and RX/CX/SP the rigidity, catalogue and
length bound.  The unchanged HV/TW/OB/VW claims supply the
guarded height/window assembly.  The current audit is
Section~\ref{sec:dependency-audit-v29}.''',
 'tex_ledger_rows':[
  r'KX1--KX9 & Complete universal arithmetic & Actual levels, reciprocity, weights, Phi, determinants and the universal Pair ring.',
  r'QX & Adjoint and actual support joins & Two Links and the five-clause tower join; the precise rank-four Hecke producer remains.',
  r'SX1--SX8 & Complete case-II seed & Actual cuspidality, fixed-central weights, induced lattice, local flags and automorphy.',
  r'UX1--UX12 & Complete case-II promodularity & Actual towers, residual lines, spaces, component propagation and coefficient descent.',
  r'YX1--YX2 & Complete conditional case-II count & PMExAlt gives CountII with all original point, length and coefficient quantifiers.'
 ],
 'tex_dependency_update':r'''\section{Dependency audit after the complete case-II chain}
\label{sec:dependency-audit-v29}

This audit records exact sufficient obligations, preserves every
version-0.28 semantic node, and includes prior snapshots for changed
nodes.  It is not an exhaustive Lean graph or a completion percentage.
Historical claims, source arrays and dependency edges are unchanged.

The principal new closed chain is
\[
 \texttt{PMExAlt}
 \xRightarrow[\mathrm{SX8}]{\mathrm{UX12}}
       \text{actual case-II promodularity}
 \xRightarrow{\mathrm{YX1}}\text{case-II image density}
 \xRightarrow{\mathrm{YX2}}\texttt{CountII}.
\]
SX8 supplies the seed at every given permissible tower and fixed
embedding.  UX12 supplies the actual valued point, coefficient
maps, restrictions, ordered inertia and support ideal, using three
explicit residual lines in one actual deformation space.  YX uses
the existing original-point, model, rigidity and catalogue machinery
with every constant and normalized coefficient return in its
original quantifier order.  No case-III input is used in this chain.

KX supplies the exact universal arithmetic packages.  QX supplies
the literal adjoint lifting theorem, the actual two Links and
\texttt{IsPhi} maps, and the complete five-clause tower join.
Its retained arithmetic input is the actual rank-four
\texttt{HidaPropsAlt} ideals together with \texttt{P1core} on
those Links, uniformly after one coefficient threshold.
The six fields \texttt{ring}, \texttt{dense}, \texttt{pt},
\texttt{end1}, \texttt{end2} and \texttt{twist} belong to the
same ideal and the same fixed embedding.  A generic dense subset
or an unrelated quotient does not supply this record.
The stronger all-rank packages and unused \texttt{P3core} are
not promoted.

The added sufficient height cut is
\[
 \texttt{CountI}\wedge\texttt{CountIII}\wedge\texttt{CountV}
       \wedge\texttt{PMExAlt}
       \xRightarrow{\mathrm{YX2}}\texttt{PointHV}.
\]
The existing TW/OB/VW assembly retains its prime-pair hypotheses
and its $C_t=401$ cutoff exponent $400$.  The earlier JX cut
through full two-case image density remains valid as stated.

The historical seed target combines cases II and IV, while the
promodularity target combines cases II and III.  Supplying SX8
and UX12 narrows those targets but does not retire their entire
scope.  The actual ordinary Hecke/support producer, case-IV seed,
case-III construction, remaining counts, and independent actual
family/gap/theta/local/denominator/metric/spectral branches remain.
The milestone is a complete conditional case-II dependency chain,
not the full human-readable RH/Dirichlet-GRH proof.
'''
}
(ROOT/'increment_v0_29.json').write_text(json.dumps(cfg,ensure_ascii=False,indent=2)+'\n')
print('Configured v0.29: '+', '.join(components))
