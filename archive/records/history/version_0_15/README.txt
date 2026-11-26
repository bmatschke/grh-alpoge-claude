RH AND DIRICHLET-GRH: HUMAN RECONSTRUCTION, VERSION 0.15
Date: 2026-11-22
Source: https://github.com/CocoSgt/riemann-hypothesis-lean
Pinned commit: 7cbf7a0c32fca1badf05931879a37c3f8a2b03b4

CURRENT STATUS
==============
Partial human reconstruction of RH and Dirichlet GRH. The actual TC.Ok-to-Laws implication and the complete reference symmetric/terminal FormsTiedSym and ColsTiedSym construction are now reconstructed. All twenty-one ParameterChoice families, all SizesAt clauses and the complete NumAt join are proved under the literal supplied data. The initial size datum, prescribed-frame/cyclic ranks, coded Harish-Chandra columns and conditional level-prime datum are explicitly constructed. Finite-field, orientation, principalization and normalized-jet reductions refine the canonical evaluation boundary. Primitive arithmetic host construction, local index/nonvanishing and analytic theta suppliers, the five Later stages, twisted comparisons, geometric point suppliers and the independent global branches remain. No complete self-contained RH/GRH proof or Lean kernel replay is asserted.

The complete current readable note is RH_readable_reconstruction_v0_15.tex.
No new PDF was rendered in this round, following the user's preference to
prioritize proof work, TeX and the updated archive. The 150-page v0.13 PDF
is preserved under history/version_0_13/ as a historical predecessor;
it does not contain the v0.14 or v0.15 increments. No v0.15 page count or visual
layout review is claimed. tex_validation.json records the exact check used.

NEW MATHEMATICS
===============
- TL1-TL13: prove TC.Ok implies all eleven TC.Laws fields directly, through finite Hermitian lattice classes, finite stabilizers and local levels, rational invariant forms, full integral lattices and all-place Fock metrics, actual residue moves and period extensions. No completed Forms0 or terminal comparison is used to supply its own law hypothesis.
- TL14-TL21: construct one number field for all normalized frame-character values, finite coefficient roots and tuple readings, oriented auxiliary factors and Pins.cof, finite principalizations, and the algebraic closure/finite-generation steps for normalized jets. Isolate the actual local-index/nonvanishing, period/trace-isometry, CM-j and primitive theta/covariance inputs of evLg_canonical. Full EvLg remains conditional on them.
- TG1-TG12: identify the exact penultimate HSym/lamSym and terminal row/full levels; prove the actual row chart, terminal vector/lattices/residue functional and adelic incidence; construct all FormsTiedSym, AtT/CarT, symmetric adelic/stabilizer and residue/level-zero joins, and the complete ColsTiedSym. Preserve the same movements, embeddings, auxiliary data and functional orientation.
- PN1-PN16: prove the fourteen remaining parameter families, then join them with RF into all twenty-one families and every one of the 111 actual ParameterChoice' fields for the same D,L. Preserve the nested threshold order and all four supplied HostArith fields.
- SZ1-SZ13: prove all 23 named SizesAt clauses plus splitBound>=11, all 21 NumAt fields and ChTT/ChCode; independently construct all 63 initial SizeData₂ fields and all 15 Val fields, with every Over label/code identity. Construct all 13 Ranks fields over any prescribed frame, and the literal cyclic-frame specialization.
- AC1-AC10: prove the bounded root-of-unity correction and the actual quadratic-subfield norm/parallel-weight identity; construct every coded HCParam and simultaneous HCVal family, then the complete chGood_of_host. Convert the retained norm-prime assertion into integral norm-one elements and all 15 LevCh fields; prove exists_levCh_of_levelPrime with its uniform threshold and supplied logarithmic window.

REMAINING INPUTS
===============
- Construct the actual arithmetic host and CM/character-field data, including Galois/frame, cyclotomic, half-different, norm and window properties. SZ13 now constructs ranks over prescribed and cyclic frames; AC constructs the coded columns once that host and its top-weight window are supplied. Rank construction alone does not supply the number field.
- Complete canonical TC.Ok and EvLg supply: the exact local coset/index, character and first-unfolding nonvanishing theorems; ambient periods and trace isometry; CM-j algebraicity; primitive normalized theta Taylor/torsion, four-copy/vacuum and covariance identities. TL proves all elementary finite-field/ideal/tuple reductions and Ok-to-Laws. Pins.iX and all five Later stages remain explicit where required.
- Extend the completed reference symmetric/terminal comparison to the actual variable-twist terminal frames, all-twist chain/joint data and standard twisted columns. The stronger OneLevelSymmetricColumns assertion has additional predicates and is not inferred from TG12.
- Supply the geometric Lay/RecOK/LedOK/RecExP construction and mass/window estimates, actual top-weight windows and uniform du/Dstar logarithmic window, and the analytic LevelPrime hypothesis. AC and SZ now prove all three conditional arithmetic constructors isolated by RF10; PN/SZ complete the numerical parameter and size packages. Their input existence is still substantive.
- Actual theta/common-image identities, chain norms and eigenvalue bounds; AG archimedean spectral-word identities, arithmetic positive-semidefinite kernel and mass normalization, loop/nongeneric/degenerate bounds.
- Actual dimension balance, retained-source integral/isometric metric transport and discarded-target control.
- Congruence denominators LinkN/LinkV and two-primary/odd-minus/odd-plus cohomological windows for ordinary and fixed-character hosts.
- Full simultaneous PairEx prime selection, uniform gain-to-centered-prime-sum and final global parameter supply.

HOW TO CONTINUE
===============
Start with continuation_checkpoint.json. next_source_targets.json records
37 exact next-source ranges and their remaining human
scope. The targets are a work map, not additional proved claims.

provenance.json contains 608 stable claims and
9381 exact source-range links;
provenance.txt is its readable companion. Every new component has main.tex,
report.txt, a hashed source ledger and a reproducible locator builder.
The cumulative TeX embeds the complete readable proof text, so it does not
need the fragments in order to compile with a standard LaTeX installation.

For a claim lookup:
  python3 backtrack.py TL13
For source excerpts from a pinned checkout:
  python3 backtrack.py TL13 --repo /absolute/path/to/lean-source
For all recorded source byte and inclusive-range checks:
  python3 backtrack.py --check-all --repo /absolute/path/to/lean-source
For a future PDF build, run pdflatex twice on the current TeX in a build
directory, then inspect the rendered pages. Such a build is not included
in this version's verification claims.

PRESERVATION AND VERIFICATION
============================
All 536 previous claim records retain every original field and source
array. All previous source-file records and mathematical dependency lists
are unchanged. Version-0.15 notes are additive. The package preserves all
575 v0.14 files, moving only its 20 root files to history/version_0_14/
when those current filenames are replaced or retired. Earlier historical
directories and component bytes remain intact.

Scoped mathematical reviews and exact source/hash checks are recorded in
reviews_v0_15/. The mathematical dependency graph is acyclic; it is a
human reconstruction graph, not a transitive Lean dependency audit.
No full Lean compilation, independent kernel replay, or global proof
certification was performed. SHA256SUMS covers every packaged file except
itself. package_v0_15.py verifies predecessor continuity, archive CRCs and
every archived file against that manifest.
