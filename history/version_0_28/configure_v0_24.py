#!/usr/bin/env python3
"""Describe the complete odd-minus supplier and narrowed congruence frontier."""
from pathlib import Path
import json

ROOT=Path(__file__).resolve().parent
scope=(
 "Partial human reconstruction of RH and Dirichlet GRH, organized by complete dependency chains. "
 "LD1–LD4 match the literal finite local/global duality interfaces to precise classical theorems and prove the unramified reciprocity consequences. "
 "OS1–OS9 construct the finite Jacobi/Kolyvagin supplier of literal PsiBound, including auxiliary primes, finite-length descent, Bernoulli evaluation and original-field eigenspace descent. "
 "OB1–OB8 prove literal ThmBcFree with explicit constant 240 from OS9 and OS1 plus named classical inputs. This closes the entire odd-minus supplier and leaves ThmBab and PointHV as the two bespoke cohomological suppliers in the VW route. "
 "LN1–LN10 prove the integral cut, congruence-length bounds, elementary prime summation and exact restoration to original-family LinkN, conditional on the stated actual local Galois inequalities and type/theta/rank bindings. "
 "The common arithmetic family and gap, simultaneous two-primary/layer bounds, odd-plus comparison, actual theta/local installation, remaining local denominator suppliers, global/spectral estimates and exact lattice-metric transport remain explicit obligations. "
 "All earlier proofs and original claim/source records are retained. No complete self-contained human RH/Dirichlet-GRH proof, fresh Lean build or independent kernel replay is claimed."
)
new=[
 "LD1–LD4: finite procyclic and tame Euler calculations; literal unramified orthogonality; an exact match of Published.PoitouTateDuality, including the local invariant sign, primitive-root conjugation compatibility and vanishing archimedean Tate terms; finite reciprocity with one possible nonzero local cup. Classical local Tate duality, class field theory and finite Poitou–Tate are explicit citation leaves.",
 "OS1–OS9: the entire finite arithmetic PsiBound supplier. Jacobi elements are constructed and their norm/congruence laws proved; strict Kolyvagin classes and simultaneous admissible primes are constructed; finite reciprocity gives an annihilator comparison; valuation induction proves finiteness and length; Bernoulli evaluation, the residual case and original-field eigenspace descent finish the literal interface. No bespoke Rec, NuSys, count, vChar or PsiBound assumption remains.",
 "OB1–OB8: the complete quantitative odd-minus theorem ThmBcFree with uniform constant 240. Original-field coefficient and local comparisons, all-good-prime valuation budget, generator bound 8, negative-twist annihilator and exponent bound 30, and prime/twist summation are proved. OS1 supplies the precise class-group annihilation needed in OB5, so a separate general Stickelberger theorem is not an input. OS9 supplies the exact characterwise estimate in OB3.",
 "LN1–LN10: a complete conditional congruence chain from the original integral good cut to the original-family LinkN bound. A spectral filtration proves the congruence-length estimate without integral semisimplicity. Prime summation is elementary, including sparse small-order primes and all exceptional cases. The cut-restoration cost is exactly d_j log|G|, and the cohomological coefficient is unchanged. Actual local arithmetic tables, type/theta/rank identities and stronger cut compatibility remain identified inputs.",
 "Updated dependency audit: the odd-minus leaf is retired and propagated through VW3–VW4/QP25 immediately. The remaining cohomological cut is ThmBab plus PointHV on the same original field and simultaneous windows. LinkN is split into the now-proved conditional transport/numerical chain and its still-open actual local and geometric suppliers. Classical leaves and same-object quantifiers are recorded separately."
]
remaining=[
 "One actual common family satisfying HostExW/DesignExists and the required dependent layout, original coefficient maps, St/ColPin/R3.Read, rational good-row spectrum and remaining Core fields. The supplied HP representation theory and the new cohomological estimates do not construct this geometric state.",
 "The simultaneous two-primary and prescribed cyclotomic-layer supplier ThmBab, and the odd-plus comparison PointHV. These are the two remaining bespoke cohomological suppliers in the VW route. The two-primary, plus and minus bounds must concern the same original E; every prescribed layer model and its local-data choices must be controlled on the same parameter window and fixed pair. Isolated estimates on unrelated windows do not suffice.",
 "Genuine compatible theta/toric/local installation: nonzero theta maps, convergence and separation, critical toric ratios, Choice.FieldOK, NTh/NChoice/ChoiceSide/NdSpec/LocAll and the required actual operator identities. Initial zero theta and empty toric fields are still initialization only.",
 "Actual local Galois denominator tables and original type/e0 action, parameter dictionaries, localization/theta composition and rank bindings for the LN chain. All NormChoiceFacts and Tie4 fields demanded by the stronger CutGivesAlt route remain actual supplier obligations. LN's complete scalar and cut-restoration proofs do not establish those arithmetic inequalities.",
 "The actual common arithmetic gap and all SizeData2/ErrWindows/BNBounds and IdentU readings on the same family. WB supplies the full downstream character, moving-cutoff and scalar chain, while AN2/AN3/GH6 supplies the analytic endpoint.",
 "Actual source/target lattices and metrics, NprimeMuR/LinkMu transport and retained/discarded rank compatibility. Exact metric comparison is not inferred from equal dimensions or from the now-proved finite congruence calculation.",
 "Global and spectral links on actual operators: image/norm comparisons, normalized finite-word and Poisson/spectral statements, arithmetic kernel and mass identities, diagonal/off-diagonal Gram control and exceptional terms. Their arithmetic input and same-family bindings remain separate from local linear algebra.",
 "Matched classical citation leaves remain in their exact roles: finite local/global duality and class field theory; finite Chebotarev, cyclotomic and Kummer theory; S-units, Minkowski/conductor-discriminant and Bernoulli denominators; CN/BD/HD for prime-pair selection; Harish-Chandra degree and normalized unitary Tamagawa on the sufficient real-stage route. A source interface named literature is not automatically a matched classical theorem."
]
updates={
 "VW1":{"supplied_by":["OS9","OB8"],"closure":"The literal odd-minus ThmBcFree premise is supplied with C=240 for every original field, algebraic closure, local-data choice and finite odd-prime set. Two-primary and odd-plus bounds remain separate inputs."},
 "VW2":{"supplied_by":["OB8"],"closure":"Its odd-minus budget is now an available theorem with a uniform numerical constant; the original-field/conductor and uniform threshold deductions remain unchanged."},
 "VW3":{"supplied_by":["LD1","LD2","LD3","LD4","OS1","OS2","OS3","OS4","OS5","OS6","OS7","OS8","OS9","OB1","OB2","OB3","OB4","OB5","OB6","OB7","OB8"],"closure":"The complete odd-minus supplier is discharged relative to the precise classical leaves. The sufficient bespoke upstream cut reduces from ThmBab + PointHV + ThmBcFree to ThmBab + PointHV; original fields, all layers and simultaneous windows remain required."},
 "VW4":{"supplied_by":["OB8"],"closure":"Substitute ThmBcFree with C=240 into the already proved uniform same-field/fixed-pair assembly. Only ThmBab and PointHV remain as bespoke cohomological inputs to this route; QP classical leaves and actual host installation remain."},
 "QP25":{"supplied_by":["OB8","VW3","VW4"],"closure":"Exact fixed-pair rescaling now has its odd-minus input fully supplied; simultaneous ThmBab and PointHV plus the original compatible host remain necessary."},
 "OH6":{"supplied_by":["OS9","OB8"],"closure":"The odd-minus branch of the parity budget is supplied on the original field with finite lengths and uniform constant 240. Other cohomological and congruence premises are retained."},
 "DA2":{"supplied_by":["LN1","LN2","LN3","LN4","LN5","LN6","LN7","LN8","LN9","LN10"],"closure":"Its original-family LinkN premise is now a complete consequence of the detailed local denominator tables and actual type/theta/rank data. The cut-to-original implication is fully proved; actual local suppliers, LinkV, summability/finiteness guards and exact metric transport remain."},
 "GH7":{"supplied_by":["OB8","LN10"],"closure":"The odd-minus supplier is closed and the congruence branch has a complete conditional local-to-global/restoration chain. The remaining cohomological, family/gap, actual local/theta, metric and spectral suppliers are explicitly retained."}
}
cfg={
 'artifact_version':'0.24','date':'2026-11-22','predecessor_version':'0.23',
 'components':['local_duality_closure','odd_minus_supplier','odd_minus_bounds','congruence_chain'],
 'tex_component_order':['local_duality_closure','odd_minus_supplier','odd_minus_bounds','congruence_chain'],
 'scope':scope,'new_in_this_version':new,'remaining_major_inputs':remaining,'claim_updates':updates,
 'completed_previous_frontier':'The entire literal PsiBound -> ThmBcFree odd-minus supplier is closed with constant 240. Finite duality conventions are matched. Conditional congruence/cut-to-original transport and prime summation are complete; actual local arithmetic and type/theta bindings remain.',
 'next_local_priority':'Close one of the two remaining cohomological suppliers end to end: ThmBab with all simultaneous layer/window quantifiers, or PointHV with its exact odd-plus local/global comparison. In parallel, supply one full local-denominator table on the actual family, then feed it immediately through LN10 into LinkN.',
 'next_steps':[
  'Use dependency_audit_v0_24/obligation_map.json for current semantic status. OS9 and OB8 are now available suppliers, not future targets; preserve their exact original-field and local-data quantifiers.',
  'Pursue the complete ThmBab branch, including its actual LemmaK/KBridge/count and finiteness suppliers, with one common window for the two-primary and every prescribed cyclotomic-layer estimate.',
  'Pursue the exact PointHV branch as the alternative bounded cohomological target. Match every local/global duality and arithmetic comparison interface separately; the LD finite match does not automatically discharge stronger K-theoretic interfaces.',
  'For LinkN, supply the complete actual local Galois denominator table and the stated type/theta/rank identities on the same family. LN1–LN10 already handle integral cut construction from those identities, lengths, all-prime summation and restoration.',
  'Keep stronger CutGivesAlt/NormChoiceFacts/Tie4 obligations separate from the proved CutD.Good construction. Do not promote a good cut into a fully compatible arithmetic cut.',
  'After closing either remaining cohomological leaf, propagate it through VW3/VW4. When both are supplied, join QP22 on the same host and window before claiming the cohomological/fixed-pair endpoint unconditionally.',
  'For the full proof, retain the actual common family and arithmetic gap, genuine theta/local installation, global/spectral links and exact NprimeMuR/LinkMu metric transport as substantive obligations.',
  'Preserve every historical claim and source record. Record premise closures additively, and distinguish source/TeX integrity, independent argument review and formal kernel verification.'
 ],
 'precision_notes':[
  'The odd-minus branch is complete relative to the explicitly stated classical general theorems. No bespoke PsiBound, Rec, NuSys, count, vChar, killPow, gen, prodVal or atPrime supplier remains in its required scope.',
  'OS9 does not depend on OB2 Bernoulli nonvanishing. Its a=0 case uses infinite valuation; otherwise nonvanishing is a hypothesis of that case. The OS -> OB dependency is acyclic.',
  'OB5 uses the exact OS1 inverse-oriented Jacobi annihilator and cancels 2 only in an odd-primary character target. The classical general Stickelberger theorem is comparison material, not an input.',
  'OB8 has one numerical constant 240 for all original E, Omega, coefficient and local-data choices and all finite sets of odd primes. Individual lengths are proved finite before real sums are used.',
  'LD3 matches finite Published.PoitouTateDuality, including signs, conjugation and real Tate conventions. It is not a blanket match for all source LocalFinitenessK or LocalTateDualityK interfaces.',
  'LN2 retains the actual ordered-tuple good element, original type action and same-point local parameter identity. Finite-field labels are transported by tame characters, not embedded into C.',
  'LN3 explicitly assumes the actual rational eigenspaces span the original finite free module. Point separation alone is not claimed to supply this spanning property.',
  'LN8 proves the numerical prime summation from exact local arithmetic tables and uniform family scales. The table is a retained arithmetic supplier, not a conclusion of the scalar envelope.',
  'LN9 restores the original data at cost d_j log|G| without changing the original cohomological coefficient. Stronger cut arithmetic facts and exact metric transport are separate inputs.',
  'Historical reference edges remain unchanged; the semantic AND/OR map carries premise closures and actual-object bindings. Claim counts and graph acyclicity are not completion measures.',
  'No new PDF is generated. Draft-mode TeX checks syntax and references; independent mathematical reviews assess the written arguments. Neither is a new Lean build or kernel replay.'
 ],
 'tex_front_summary':r'''\textbf{What version 0.24 achieves.} The entire odd-minus
cohomological supplier is now reconstructed. LD matches the finite
duality conventions, OS constructs the Jacobi/Kolyvagin proof of the
literal characterwise bound, and OB proves the full quantitative
\texttt{ThmBcFree} estimate with explicit constant $240$. Its downstream
use is already closed in VW, so only \texttt{ThmBab} and
\texttt{PointHV} remain as bespoke cohomological inputs to that route.
LN proves the integral-cut, congruence-length, prime-summation and
cut-to-original \texttt{LinkN} chain; its actual local arithmetic
tables and type/theta bindings remain explicit. The updated audit
separates these suppliers from the remaining common family, arithmetic
gap, genuine theta/local data and global metric/spectral comparisons.
This is \textbf{a partial human reconstruction; the full human-readable
proof of RH and Dirichlet GRH is not yet complete}.''',
 'tex_remaining_local':r'''HP in Section~\ref{sec:highest-weight-closure} supplies the literal
characteristic-zero highest-weight, absolute-irreducibility,
classification and original-field descent leaves, including all five
clauses of \texttt{wt\_weights}. MR's actual form/lattice/signature
state and genuine compatible theta/toric installation remain required.

LD, OS and OB in Sections~\ref{sec:local-duality-closure},
\ref{sec:odd-minus-supplier} and \ref{sec:odd-minus-bounds} supply
the entire odd-minus branch, through literal \texttt{PsiBound} to
\texttt{ThmBcFree} with constant $240$. Consequently the sufficient
bespoke cohomological cut in VW is now \texttt{ThmBab} plus
\texttt{PointHV}, with the same original fields, local data, layers
and simultaneous windows. VW and QP22 already give the complete
conditional fixed-pair assembly. QP's CN/BD/HD classical leaves and
the actual host installation retain their stated roles.

LN in Section~\ref{sec:congruence-chain} proves the conditional
original-family \texttt{LinkN} chain. It includes integral cuts,
the congruence-length filtration, elementary summation over every
prime case, and restoration with exact cost $d_j\log|G|$.
Its actual local Galois denominator tables and type/theta/rank
identities remain suppliers. The stronger cut's
\texttt{NormChoiceFacts}/\texttt{Tie4} fields are not inferred
from \texttt{CutD.Good}.

WB in Section~\ref{sec:window-bridge} closes every character,
moving-cutoff and scalar step from the exact WB7 arithmetic contract;
AN2--AN3/GH6 supplies the final analytic contradiction. The actual
gap, size/error packages and common host readings must still be
constructed. DA's uniform family join retains all actual design
and global-link suppliers, particularly the normalized spectral
estimates and exact \texttt{NprimeMuR}/\texttt{LinkMu}
lattice-metric transport. The current semantic frontier is summarized
in Section~\ref{sec:dependency-audit-v24} and in the standalone
version-0.24 dependency audit.
''',
 'tex_next_target':r'''\paragraph{The next target: close a remaining supplier end to end.}
Both odd-minus targets, \texttt{PsiBound} and \texttt{ThmBcFree},
are complete.
The next cohomological endpoints are \texttt{ThmBab}, with all
two-primary and prescribed-layer estimates on one square window,
and \texttt{PointHV}, with its exact original-field odd-plus
comparison. Their interior finite-length, local/global and
counting inputs must be supplied, not merely their implication
wrappers. LD settles its stated finite-duality interfaces; stronger
K-theoretic local interfaces still require their own matches.
For the arithmetic family, a complete actual local-denominator
table and the stated type/theta/rank identities can now be propagated
through LN10 without further cut-restoration or scalar-prime work.
The exact \texttt{NprimeMuR} metric comparison and genuine theta/local
installation remain other substantial complete-chain targets.
''',
 'tex_reading_order':r'''For this increment, read LD1--LD4, then OS1--OS9 and OB1--OB8:
they form one complete finite-duality-to-odd-minus chain. Read
VW3--VW4 afterward to see its immediate downstream use. LN1--LN10
is the independent congruence chain; its opening and closing input
ledgers distinguish the proved transport from the actual local
arithmetic suppliers. Section~\ref{sec:dependency-audit-v24}
states the resulting frontier. For the global spine, retain
Sections~\ref{sec:analytic} and \ref{sec:scalar}, WB7--WB8 and
DA1--DA2. Historical conditional proofs preserve their original
hypotheses; version-0.24 scope annotations identify those now supplied.
Stable IDs and exact pinned source/proof locators remain in the ledger.
''',
 'tex_ledger_rows':[
  'LD1--LD4 & Finite duality and reciprocity & Exact local/global conventions, unramified annihilators and one-place reciprocity.',
  'OS1--OS9 & Complete finite arithmetic supplier & Jacobi elements, Kolyvagin classes, length descent and literal original-field PsiBound.',
  'OB1--OB8 & Complete quantitative odd-minus bound & Finiteness, valuation budget, negative-twist annihilator and ThmBcFree with constant 240.',
  'LN1--LN10 & Conditional original-family LinkN & Integral cuts, congruence filtration, prime sum and exact restoration; local arithmetic inputs retained.'
 ],
 'tex_dependency_update':r'''\section{Dependency closure after the odd-minus reconstruction}
\label{sec:dependency-audit-v24}

\paragraph{A complete supplier, with its classical leaves visible.}
The dependency chain is
\[
 \begin{aligned}
 \text{finite duality (LD)}&\longrightarrow
 \text{Jacobi/Kolyvagin construction (OS)}\\
 &\longrightarrow\mathtt{PsiBound}\longrightarrow
 \mathtt{ThmBcFree}(240)\quad\text{(OB)}.
 \end{aligned}
\]
The local and global finite-duality theorems, finite class field
theory, Chebotarev, Kummer and the other classical results stated in
those chapters remain identified citation leaves. Every bespoke
auxiliary-class, recurrence, length, special-value, coefficient,
negative-twist and quantitative step needed for this endpoint is
written out. OS1 also supplies the exact odd-primary class-group
annihilator used in OB5. OS9 is independent of OB2's Bernoulli
nonvanishing, so neither join introduces a circular dependency.

\paragraph{Immediate reduction of the cohomological frontier.}
Apply OB8 to the original field and local-data choices in VW3--VW4.
Its constant $240$ is independent of every varying field, prime,
twist and finite prime set allowed there. It therefore supplies
the \texttt{ThmBcFree} quantifiers before the window and permitted
prime pair are chosen. The already proved VW argument now yields the
following statement. Fix a \texttt{BConst} record $K$ and $C_t\ge1$. Then
\[
 \mathtt{ThmBab}(K,C_t)+\mathtt{PointHV}
 \ \Longrightarrow\
 \mathtt{JointWin}(C_t)+\mathtt{ThmBc}(C_t)
 \ \Longrightarrow\
 \forall\text{ primitive }\psi,\ \mathtt{VWinAt}(\psi,C_t).
\]
With the unchanged QP22 prime-pair inputs and $C_t=401$, VW4 gives
the same fixed pair throughout the arbitrarily late three-halves
window with cutoff exponent $400$. This substitution removes one
deep supplier; it does not construct the two remaining ones or the
common arithmetic host. In particular, \texttt{ThmBab} must control
all prescribed cyclotomic layers on one window, and
\texttt{PointHV} must use the original conductor and fields.

\paragraph{The exact congruence frontier.}
LN1--LN10 prove that the stated actual type/theta identities,
local Galois denominator tables and family scales imply
\texttt{LinkN} on the original family. Its numerical summation
uses elementary estimates and a proved sparse-residue-class bound;
its cut restoration costs exactly $d_j\log|G|$ and preserves the
cohomological coefficient. Those parts are complete. Construction
of the actual local tables and compatible geometric state remains
open. The stronger \texttt{CutGivesAlt} conclusion additionally
requires all \texttt{NormChoiceFacts} and \texttt{Tie4} fields;
the good-cut construction alone does not assert them.

\paragraph{What still separates this from the full proof.}
The remaining cohomological suppliers must be joined with the
actual common family, arithmetic gap and size/error packages,
genuine theta/local installation, global and spectral operator
comparisons, and exact lattice-metric transport. DA1 governs the
uniform threshold and same-family quantifiers, and DA2 retains
the exact metric premise. WB and the analytic endpoint are already
complete deductions from their stated contract. The updated
\texttt{dependency\_audit\_v0\_24/obligation\_map.json}
records these AND/OR obligations separately from the historical
reference graph. Counts of claims or source links do not measure
how much of these substantive obligations has been discharged.

'''
}
(ROOT/'increment_v0_24.json').write_text(json.dumps(cfg,ensure_ascii=False,indent=2)+'\n')
print('Wrote increment_v0_24.json')
