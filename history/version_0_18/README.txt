RH AND DIRICHLET-GRH: HUMAN RECONSTRUCTION, VERSION 0.18
Date: 2026-11-22
Source: https://github.com/CocoSgt/riemann-hypothesis-lean
Pinned commit: 7cbf7a0c32fca1badf05931879a37c3f8a2b03b4

CURRENT STATUS
==============
Partial human reconstruction of RH and Dirichlet GRH. Arithmetic scalar extension, actual rank comparison, finite Artin/ring-class character descent, nonempty-local character/conductor compatibility, local parahoric rigidity and the exact conditional choice/tuple join are reconstructed. The actual Fontaine, de Rham and crystalline ring constructions, invariants and fundamental intersection supply LocStage; the bare empty-index NStage and Later are constructed on the same adapted rows. A qualitative ray-prime argument supplies the original sized PreX with exact norm factors, spaces, letters, integer mass-index normalization and pins; the actual chosen-volume empty-jet stage is constructed. Rational theta adjoint/level cuts, common-image and Gram deductions, exact rational row/lift comparisons and common row-test normalization are reconstructed under their explicit tests and operator/type identities. Nonempty choice-compatible stages, actual realization/frame/core suppliers, quantitative mass and prime windows, primitive theta test/operator identities, and the four global branches remain. No complete self-contained RH/GRH proof, full Lean build or independent kernel replay is asserted.

The complete current readable note is RH_readable_reconstruction_v0_18.tex.
No new PDF was rendered in this round, following the user's preference to
prioritize proof work, TeX and the updated archive. The 150-page v0.13 PDF
is preserved under history/version_0_13/ as a historical predecessor;
it does not contain any increment after v0.13. No v0.18 page count or visual
layout review is claimed. tex_validation.json records the exact check used.

NEW MATHEMATICS
===============
- RC1–RC21: prove finite-evaluation scalar extension and actual RankTie; construct the coefficient-valued Artin character under the stated global reciprocity input and descend through the actual NTw universal map. Prove Frobenius detection, exact conductor/local-character compatibility, coherent side/packet readings and the precise ChoiceSide join. Transport all MuIsW fields on the actual ColW/Pre2/St, and prove the local parahoric, additive-character and nonzero-form arguments yielding LevEq from Joint. Prove the selector under TwCoverPair and the finite integral subbasis/prime-avoidance construction with S chosen before all forbidden sets; actual twisting/full-rank/adm7 inputs remain. Actual realization/weight/frame and compatible nonempty-stage suppliers remain.
- LS1–LS22: prove explicit Ax approximation, bounded cyclotomic projections and vanishing of every nonzero Tate-twist invariant, including at 2. Construct the actual Ainf theta map, BdR DVR, divided-power completion embedding, logarithmic period and crystalline ring; prove Frobenius injectivity/fixed ring, the fundamental intersection and exact de Rham/crystalline invariant fields. Check the literal local-stage fields and construct the bare empty-index NStage and Later on the same adapted rows. This model supplies no NChoice or representation comparison.
- IG1–IG14: reconstruct imaginary-quadratic ray partial zeta functions by Gaussian Poisson summation; prove nonvanishing at 1 by the entire character-product and nonnegative Taylor argument, hence arbitrarily large prime norms in every ray class. Construct the actual cyclic host, separated auxiliary primes, two-word HC columns, norm factors, diagonal spaces, every original PreX field and positive integer mass-index normalization. Restrict to the source singleton and set its window exactly, obtaining the original exists_pre_sized. Supply orientation/pins and the actual chosen-volume empty-jet stage. Expand the recursive-existence arrow with actual core and quantitative window premises retained.
- TD1–TD16: prove fixed-field coordinate recovery, rational theta kernel/adjoint cuts, finite-group and idempotent level descent, and common theta image with its exact Gram factor from positive operator identities. Construct literal rational row/lift matrices, the base-lift relation, quotient-metric spectral orthogonality and the principal Hermitian lattice. Prove one common row-test normalization, including the zero-scalar case, Boolean conjugation transport and uniform threshold order. Actual test convergence/period/rational-ratio and positive theta identity suppliers remain.

REMAINING INPUTS
===============
- Construct the same actual nonempty twist/local data needed by NChoice, with its NTw universal ring-class maps, compatible indices/sides and IsGalOf local values; supply the realized MtFam/NExpTied/TwFrameC, Joint and CellWt. RC proves the rank/character/local-level mechanics and actual MuIsW transport, but ColW/Pre2/St/RowPk and their simultaneous compatible existence remain substantive. RC20 gives readings only on twisted places, whereas RC11 needs an all-place reading. RC21 retains aux3/FullRank/adm7 and settings; finite prime avoidance does not prove their lattice-index estimates. The empty-Tw model of LS cannot supply NChoice.twI.
- Supply the actual full Hecke-character frame and geometric V4.Core, VolumeEqMass2, Lay/RecOK/LedOK. IG supplies an original sized PreX and exact chosen-volume noJet stage, not VolTieG or a compatible recursive core. Quantitative SiegelMassRatioCM/window_lower, prescribed top/logarithmic windows, LevelPrime and simultaneous prime selection remain; qualitative unbounded ray primes do not give these estimates.
- Supply the actual compatible common theta tests (choice/FieldOK, LinK/InjK, Formula2K, SumRatK, RatioK) and positive operator/type identities (ThmBop/ThmAop, PartsE/PartsW, actual HoldsL). TD derives common image, rational matrices and exact metrics from them; quantitative eigenvalue and chain-norm estimates, AG spectral-word identities, positive-semidefinite kernel/mass normalization and exceptional-word bounds remain.
- Actual dimension balance/GalD, retained-source integral/isometric metric transport and discarded-target control remain. Equal rank, rational common image and a constructed positive metric do not supply these stronger assertions.
- Congruence denominators LinkN/LinkV and two-primary/odd-minus/odd-plus cohomological windows for ordinary and fixed-character hosts remain.
- Full simultaneous PairEx prime selection, uniform gain-to-centered-prime-sum and final global parameter supply remain.

HOW TO CONTINUE
===============
Start with continuation_checkpoint.json. next_source_targets.json records
103 exact next-source ranges and their remaining human
scope. The targets are a work map, not additional proved claims.

provenance.json contains 820 stable claims and
12105 exact source-range links;
provenance.txt is its readable companion. Every new component has main.tex,
report.txt, a hashed source ledger and a reproducible locator builder.
The cumulative TeX embeds the complete readable proof text, so it does not
need the fragments in order to compile with a standard LaTeX installation.

For a claim lookup:
  python3 backtrack.py TD8
For source excerpts from a pinned checkout:
  python3 backtrack.py TD8 --repo /absolute/path/to/lean-source
For all recorded source byte and inclusive-range checks:
  python3 backtrack.py --check-all --repo /absolute/path/to/lean-source
For a future PDF build, run pdflatex twice on the current TeX in a build
directory, then inspect the rendered pages. Such a build is not included
in this version's verification claims.

PRESERVATION AND VERIFICATION
============================
All 747 previous claim records retain every original field and source
array. All previous source-file records and mathematical dependency lists
are unchanged. Version-0.18 notes are additive. The package preserves all
797 v0.17 files, moving only its 20 root files to history/version_0_17/
when those current filenames are replaced or retired. Earlier historical
directories and component bytes remain intact.

Scoped mathematical reviews and exact source/hash checks are recorded in
reviews_v0_18/. The mathematical dependency graph is acyclic; it is a
human reconstruction graph, not a transitive Lean dependency audit.
No full Lean compilation, independent kernel replay, or global proof
certification was performed. SHA256SUMS covers every packaged file except
itself. package_v0_18.py verifies predecessor continuity, archive CRCs and
every archived file against that manifest.
