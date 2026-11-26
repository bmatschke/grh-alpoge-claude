RH AND DIRICHLET-GRH: HUMAN RECONSTRUCTION, VERSION 0.16
Date: 2026-11-22
Source: https://github.com/CocoSgt/riemann-hypothesis-lean
Pinned commit: 7cbf7a0c32fca1badf05931879a37c3f8a2b03b4

CURRENT STATUS
==============
Partial human reconstruction of RH and Dirichlet GRH. The prescribed-character cyclotomic host, all HostDer fields and trace-self-dual half-different are constructed under the literal prime and splitting hypotheses. Actual ambient periods, trace isometries, CM-j integrality and the normalized one-dimensional theta arithmetic are reconstructed. The local-index/nonvanishing and canonical replacement suppliers and the complete standard all-twist comparison are proved with their original data and interfaces. Multidimensional vacuum/indicator/covariance, the actual NChoice/TupTied arithmetic join, Pins.iX, all five Later stages, analytic prime/window and geometric point suppliers, and the four independent global branches remain. Named classical inputs are explicit. No complete self-contained RH/GRH proof, full Lean build or independent kernel replay is asserted.

The complete current readable note is RH_readable_reconstruction_v0_16.tex.
No new PDF was rendered in this round, following the user's preference to
prioritize proof work, TeX and the updated archive. The 150-page v0.13 PDF
is preserved under history/version_0_13/ as a historical predecessor;
it does not contain the v0.14, v0.15 or v0.16 increments. No v0.16 page count or visual
layout review is claimed. tex_validation.json records the exact check used.

NEW MATHEMATICS
===============
- AH1-AH18: construct the mixed character frame and exact Artin sign correction, cyclotomic fixed field, primitive conductor, stabilized order, kept characters, kernel and twist formulas. Prove all 30 HostDer fields, including ramification/decomposition, CM type, relative half-different, trace self-duality and the three discriminant bounds. Complete literal fieldChi under its original q,d/splitting conditions and quantifier order.
- PA1-PA15: construct the actual normalized period and unkilled half-point, rational four-copy trace isometry, algebraic complex extension, all local AtP choices and all AmbIn.Ok fields. Prove genuine finite support of kappa on split primes, actual CM-j integrality and FieldOK, and algebraic torsion coordinates. The exact conditional even-theta transfer is retained and then supplied by TA.
- TA1-TA14: reconstruct the normalized one-dimensional odd/even theta arithmetic. A purely analytic product/Legendre argument, formal ODE uniqueness and a descended CM polynomial give galSg; exact division quotients and their constant term give gal1. Fixed-field descent proves all rational-translate coefficients algebraic, and exact half-period/conjugate-curve transport gives all use1 clauses. No arbitrary embedding is assumed continuous.
- CI1-CI19: reconstruct finite local cosets and normal forms, actual projected-kernel characters, finite-field support/nonzero counts and local reduction. Prove exists_chIdx_of_cst and twIdx_ok_closed, and the canonical replacement join under its actual supplied inputs. The nonvanishing comes from explicit finite counts and the character rigidity from a stabilized sum, independently of Laws or a completed comparison.
- TX1-TX16: construct the variable-twist full/row terminal charts with their different depths, the common penultimate character and carrier, the integral Law0 equivalence, all twisted chain/form/level data and exact terminal incidence/evaluation. Join the ten actual SymmetricTwistedColumnsAtPrimes fields in colsTwPTiedS_std, retaining the original NChoice, TupTied and same-xi interface.

REMAINING INPUTS
===============
- Complete the canonical analytic supplier: the actual StdOK/four-copy vacuum identity and normalized indicator/covariance (finAlg_step), then the remaining EvLg join. AH, PA, TA and CI now supply its host arithmetic, ambient periods, CM-j, primitive one-dimensional theta and local-index ingredients. Pins.iX and all five Later stages remain explicit.
- Construct the actual normalized arithmetic NChoice with its finite DVR extensions, valuation embeddings and Mt basis/integral-lattice comparison, then TupTied on the same selected primes and characters. TX16 proves the all-twist comparison conditional on this precise original interface. OneLevelSymmetricColumns is a stronger optional target with additional restrictions.
- Supply the simultaneous q,d prime/splitting conditions in the required analytic windows, the actual top-weight and du/Dstar logarithmic windows, analytic LevelPrime, and the geometric Lay/RecOK/LedOK/RecExP construction with its mass/window bounds. AH18 constructs the field once its stated prime hypotheses hold; the earlier numerical and conditional constructors do not themselves produce those analytic/geometric inputs.
- Actual theta/common-image identities, chain norms and eigenvalue bounds; AG archimedean spectral-word identities, arithmetic positive-semidefinite kernel and mass normalization, loop/nongeneric/degenerate bounds.
- Actual dimension balance, retained-source integral/isometric metric transport and discarded-target control.
- Congruence denominators LinkN/LinkV and two-primary/odd-minus/odd-plus cohomological windows for ordinary and fixed-character hosts.
- Full simultaneous PairEx prime selection, uniform gain-to-centered-prime-sum and final global parameter supply.

HOW TO CONTINUE
===============
Start with continuation_checkpoint.json. next_source_targets.json records
26 exact next-source ranges and their remaining human
scope. The targets are a work map, not additional proved claims.

provenance.json contains 690 stable claims and
10374 exact source-range links;
provenance.txt is its readable companion. Every new component has main.tex,
report.txt, a hashed source ledger and a reproducible locator builder.
The cumulative TeX embeds the complete readable proof text, so it does not
need the fragments in order to compile with a standard LaTeX installation.

For a claim lookup:
  python3 backtrack.py TA12
For source excerpts from a pinned checkout:
  python3 backtrack.py TA12 --repo /absolute/path/to/lean-source
For all recorded source byte and inclusive-range checks:
  python3 backtrack.py --check-all --repo /absolute/path/to/lean-source
For a future PDF build, run pdflatex twice on the current TeX in a build
directory, then inspect the rendered pages. Such a build is not included
in this version's verification claims.

PRESERVATION AND VERIFICATION
============================
All 608 previous claim records retain every original field and source
array. All previous source-file records and mathematical dependency lists
are unchanged. Version-0.16 notes are additive. The package preserves all
651 v0.15 files, moving only its 20 root files to history/version_0_15/
when those current filenames are replaced or retired. Earlier historical
directories and component bytes remain intact.

Scoped mathematical reviews and exact source/hash checks are recorded in
reviews_v0_16/. The mathematical dependency graph is acyclic; it is a
human reconstruction graph, not a transitive Lean dependency audit.
No full Lean compilation, independent kernel replay, or global proof
certification was performed. SHA256SUMS covers every packaged file except
itself. package_v0_16.py verifies predecessor continuity, archive CRCs and
every archived file against that manifest.
