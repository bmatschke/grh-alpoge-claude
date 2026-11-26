RH AND DIRICHLET-GRH: HUMAN RECONSTRUCTION, VERSION 0.14
Date: 2026-11-21
Source: https://github.com/CocoSgt/riemann-hypothesis-lean
Pinned commit: 7cbf7a0c32fca1badf05931879a37c3f8a2b03b4

CURRENT STATUS
==============
Partial human reconstruction of RH and Dirichlet GRH. The actual chart values, neighbor naturality and direct Forms0/level-zero carrier construction now give the concrete integral comparison for supplied true-column Ok/Pins/Laws/Later data. The initial decorated-point realization is now constructed from the literal unramified CM and valid-decoration hypotheses, including at dyadic places. The diagonal base point, supported splice and exact frame modification are proved. Canonical refill and the conditional point installation are proved; all ParamsT fields and seven of twenty-one ParameterChoice families are proved. Actual arithmetic host and column-law supply, terminal/symmetric-column data, fourteen parameter families, SizesAt, host/point existence and the independent global branches remain. No complete self-contained RH/GRH proof or Lean kernel replay is asserted.

The complete current readable note is RH_readable_reconstruction_v0_14.tex.
No new PDF was rendered in this round, following the user's preference to
prioritize proof work, TeX and the updated archive. The 150-page v0.13 PDF
is preserved under history/version_0_13/ as a historical predecessor;
it does not contain the v0.14 increment. No v0.14 page count or visual
layout review is claimed. tex_validation.json records the exact check used.

NEW MATHEMATICS
===============
- AD1-AD4: explicit integral unitary diagonal base point with the exact last-row residue; transition integrality and residue cancellation; supported conjugate-pair splice checking every IsPtOf field; global-lattice recovery and exact rational-frame modification.
- DR1-DR3: derive split/unramified local algebras from literal cmUnram, lift every unit norm including in residue characteristic two, construct local orthonormal bases and an actual unitary finite-adelic realizer, and install every type/auxiliary residue and rational frame. All five IsPtOf fields and the actual adelic Col.UnimodGenus are supplied.
- FC1-FC19: actual finite charts, residue-functional normalization preserving all carriers, quotient projections, Fock norm and period identities, common GLoc characters, reduction levels, specified level-zero level, coefficient-field rationality, BwTie, dilation and a direct Forms0 construction. DR3 supplies its initially conditional geometric realization.
- CV1-CV10: actual complex member-space equality, rational preimages and exact all-prime integral chart criterion; terminal-row value clauses under its supplied row chart. Integral Weyl lattices and determinant shifts are retained.
- NB1-NB8: paired-prime Hermitian duality, the actual up/down decorated lattices and functional extensions, raw/preferred coupling-label preservation, exact moving matrices/projections, and both full naturality statements via AD3.
- VE1-VE11: explicit even/odd coefficient-field block polynomials; universal presentation-independent ValEx; evaluation injectivity and the unique semilinear comparison; all comparison hypotheses and the actual true-column concrete comparison with Ce=1 and exact integral image span. DR3 discharges the independent initial-realizer premise.
- RF1-RF16: complete canonical refill and conditional LedPart/point lattice-height installation; exact uniform rank/scale/thin/gap/band/prime inequalities; every ParamsT field; exponential word count <=2^(k-3). Seven parameter families are complete; fourteen and SizesAt remain.

REMAINING INPUTS
===============
- Supply the actual arithmetic host, literal CM data and true-column Ok/Pins/Laws/Later from their upstream arithmetic construction. DR3 now proves initial decorated-point realization under those data, and VE11 proves the concrete integral comparison. Neither initial realizability nor the stronger rational-semilocal genus route is an additional comparison premise.
- Complete the particular symmetric penultimate HSym/lamSym identification, terminal full/row levels and ReadsP, til_ties vector/incidence/evaluation geometry and the exact terminal CarT joins. The common penultimate subgroup/orbit carrier, scalar residue identity and conditional terminal values/norms are already reconstructed. These terminal tasks are not additional premises of the direct level-zero comparison.
- Supply actual Lay/RecOK/LedOK and RecExP geometry and its mass/window estimates, the HC/level/initial-size existence constructors, all fourteen remaining ParameterChoice families and the complete SizesAt package for the same D,L. Canonical refill, exact lattice patch, ParamsT and the band/lambda/prime/word-count estimates are already proved. The global uniform threshold and degree-pair order must be preserved.
- Construct the underlying HostAx/character field with its Galois, cyclotomic and half-different properties and actual rank/model inputs; prove the exact ShortNorm/SmallOne/ThinH and PairEx/cohomological-window suppliers retained in HC. Biased tops and the CT2=64 second set remain proved.
- Actual theta/common-image identities, chain norms and eigenvalue bounds; AG archimedean spectral-word identities, arithmetic positive-semidefinite kernel and mass normalization, loop/nongeneric/degenerate bounds.
- Actual dimension balance, retained-source integral/isometric metric transport and discarded-target control.
- Congruence denominators LinkN/LinkV and two-primary/odd-minus/odd-plus cohomological windows for ordinary and fixed-character hosts.
- Full simultaneous PairEx prime selection, uniform gain-to-centered-prime-sum and final global parameter supply.

HOW TO CONTINUE
===============
Start with continuation_checkpoint.json. next_source_targets.json records
50 exact next-source ranges and their remaining human
scope. The targets are a work map, not additional proved claims.

provenance.json contains 536 stable claims and
8431 exact source-range links;
provenance.txt is its readable companion. Every new component has main.tex,
report.txt, a hashed source ledger and a reproducible locator builder.
The cumulative TeX embeds the complete readable proof text, so it does not
need the fragments in order to compile with a standard LaTeX installation.

For a claim lookup:
  python3 backtrack.py VE9
For source excerpts from a pinned checkout:
  python3 backtrack.py VE9 --repo /absolute/path/to/lean-source
For all recorded source byte and inclusive-range checks:
  python3 backtrack.py --check-all --repo /absolute/path/to/lean-source
For a future PDF build, run pdflatex twice on the current TeX in a build
directory, then inspect the rendered pages. Such a build is not included
in this version's verification claims.

PRESERVATION AND VERIFICATION
============================
All 465 previous claim records retain every original field and source
array. All previous source-file records and mathematical dependency lists
are unchanged. Version-0.14 notes are additive. The package preserves all
485 v0.13 files, moving only its 18 root files to history/version_0_13/
when those current filenames are replaced or retired. Earlier historical
directories and component bytes remain intact.

Scoped mathematical reviews and exact source/hash checks are recorded in
reviews_v0_14/. The mathematical dependency graph is acyclic; it is a
human reconstruction graph, not a transitive Lean dependency audit.
No full Lean compilation, independent kernel replay, or global proof
certification was performed. SHA256SUMS covers every packaged file except
itself. package_v0_14.py verifies predecessor continuity, archive CRCs and
every archived file against that manifest.
