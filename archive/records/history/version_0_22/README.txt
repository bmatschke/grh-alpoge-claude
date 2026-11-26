RH AND DIRICHLET-GRH: HUMAN RECONSTRUCTION, VERSION 0.22
Date: 2026-11-22
Source: https://github.com/CocoSgt/riemann-hypothesis-lean
Pinned commit: 7cbf7a0c32fca1badf05931879a37c3f8a2b03b4

CURRENT STATUS
==============
Partial human reconstruction of RH and Dirichlet GRH. This increment supplies actual full-range Mt forms on a compatible supplied geometric state, original-DVR good lattices and Hecke signatures, and the literal initial SideB endpoint with its zero theta/empty toric initialization and supplied NTh exposed. It proves four supported local primitives. It proves the quantitative moved-vacuum dictionary with exponent [F:Q]ab and one common scalar unit. It constructs the large-gap discrete series used later and calibrates formal degree using the named Harish-Chandra theorem, giving a restricted RealTied join. It proves PrimesRel and full simultaneous PairEx using the explicitly named quadratic class-number formula, Bombieri log-free density/exception refinement, and Heath-Brown density theorem; compatible supplied hosts satisfy RealBox/ThinH, while winPairs retains VWinAt. Genuine same-object theta/local installation, critical toric ratios and original-choice joins, the remaining full Core, named classical inputs and independent global/cohomological/spectral branches remain. This is not a complete self-contained RH/Dirichlet-GRH proof, full Lean build or independent kernel replay.

The complete current readable note is RH_readable_reconstruction_v0_22.tex.
No new PDF was rendered in this round, following the user's preference to
prioritize proof work, TeX and the updated archive. The 150-page v0.13 PDF
is preserved under history/version_0_13/ as a historical predecessor;
it does not contain any increment after v0.13. No v0.22 page count or visual
layout review is claimed. tex_validation.json records the exact check used.

NEW MATHEMATICS
===============
- MR1–MR26: actual full-range Mt realization, exact normalized Hecke integrality and used/unused tuple readings on a supplied compatible state. An integral additive K-reading into the original DVR fraction field and flat descent prove stability of the actual good lattice. Integral finite signatures and actual type spaces give the literal initial SideB conditional on NTh; Theta=ThetaPsi=0, Dat=PEmpty, thP=twDel=0, eH=1 and TwL.empty are exposed. Four local primitives give finite simultaneous splitting, residual-block locality, supported nonzero eigenvectors and freeness of the original relation quotient.
- QD1–QD22: the moved-vacuum scalar has all conjugates of modulus one and is a unit at every standard finite prime. Entire-jet uniqueness gives one kappa for all these primes. The finite Fourier quotient has cardinal n dividing k^([F:Q]ab), coefficients nu_i/n with nu_i^(2k^2)=1, conjugate l1 norm at most one and k-torsion translations. Rational/split/stabilizer factorization and the real vacuum determinant give exists_kappa, movedVacuum_dict and dictAt_big on the supplied original choices.
- DC1–DC22: a principal-minor average, decay/Hilbert closure, Schmid/PBW coercivity, unique lowest type and rigidity construct the actual large-gap discrete series. Full central parameters and signs are identified. Compact-dual Haar density and a scalar Bergman integral calibrate the named Harish-Chandra formal-degree theorem. The later weights satisfy the gap, giving all four restricted RealTied fields. All 21 Core fields are audited with the exact remaining layout/arithmetic inputs retained.
- QP1–QP25: the effective exceptional-zero gap, Page uniqueness and relative progression theorem follow from named CN/BD inputs. Twist cancellation, bounded-coefficient mean squares and a continuum maximal argument give polynomial-window selection. Zero-box tails, including imprimitive Euler factors, give the exact 4 log y bound. Named HD density bounds bad conductors. Both primes satisfy all congruences, windows, character rows and primitive-inducer clauses, yielding full PairEx. A compatible supplied host satisfies RealBox/ThinH; winPairs retains VWinAt.

REMAINING INPUTS
===============
- Construct the compatible original St/ColPin/R3.Read and all tuple lattice ties, and the genuine RatIn good-row spectral/integral inputs. MR now supplies form realization and lattice/signature construction from these. GlobalArtin, GalEx, RowCusp, ChebSplit, fixed-field containment and the precise polynomial highest-weight theorem remain explicit where used.
- Install a compatible nonplaceholder theta/toric NTh and genuine nonempty local family on those same forms. Complete NChoice/TupTied/ChoiceSide, NdSpec/LocAll, actual Psi/MtLoc/Act comparisons, residual/tame agreements and IsTripleWith/IsTripleFor. The initial second_step has zero theta fields and an empty toric family and assumes a later NTh; it does not solve these joins.
- Complete the same-object V4.Core and dependent layout/RecOK/LedOK, ranks, forced primes, conductor support/exponents and stage compatibility. DC supplies the sufficient large-gap RealTied portion with exact Haar scale, retaining Harish-Chandra formal degree and GV unitary Tamagawa. Universal DiscreteSeriesExist/FormalDegreeFormula2 remain separate if their stronger ranges are needed. Hasse–Minkowski remains named.
- Prove actual critical ToricRatioConjugates/ratio_algebraic/NFRatio arithmetic and the original-embedding/frame/family Choice.FieldOK join. QD supplies quantitative DictAt and common scalar units; WA/CW supply normalized jets, bottom periods and full Weil data. The separate universal IsEtaTilde/global-norm-index bridge is not inferred.
- Complete actual theta convergence, separation, nonvanishing, unfolding/tower/ratio and positive ThmBop/ThmAop/PartsE/PartsW inputs. Quantitative finite Weil arithmetic does not supply these analytic/operator identities.
- Complete independent chain-norm and archimedean spectral-word identities, positive kernel/mass normalization, exceptional-word bounds, actual GalD/dimension balance, integral/isometric metric transport and discarded-target control.
- Complete LinkN/LinkV congruence denominators, two-primary and odd-minus/odd-plus cohomological windows and the literal JointWin/ThmBc/VWinAt supplier. QP proves PrimesRel/PairEx and compatible-host RealBox/ThinH, but does not construct arbitrary hosts or VWinAt.
- For a fully self-contained analytic reconstruction, expand the retained quadratic class-number formula CN, Bombieri log-free density with exceptional-zero factor BD, and Heath-Brown 1979 Theorem 1 HD. Current PrimesRel/PairEx follow from these unconditional classical theorems without RH/GRH. The fixed 1/8 auxiliary PNTAPRelW and oversized explicit source density constants are not claimed; existential-constant PrimesRel and direct twistK suffice.

HOW TO CONTINUE
===============
Start with continuation_checkpoint.json. next_source_targets.json records
221 exact next-source ranges and their remaining human
scope. The targets are a work map, not additional proved claims.

provenance.json contains 1168 stable claims and
15522 exact source-range links;
provenance.txt is its readable companion. Every new component has main.tex,
report.txt, a hashed source ledger and a reproducible locator builder.
The cumulative TeX embeds the complete readable proof text, so it does not
need the fragments in order to compile with a standard LaTeX installation.

For a claim lookup:
  python3 backtrack.py QP22
For source excerpts from a pinned checkout:
  python3 backtrack.py QP22 --repo /absolute/path/to/lean-source
For all recorded source byte and inclusive-range checks:
  python3 backtrack.py --check-all --repo /absolute/path/to/lean-source
For a future PDF build, run pdflatex twice on the current TeX in a build
directory, then inspect the rendered pages. Such a build is not included
in this version's verification claims.

PRESERVATION AND VERIFICATION
============================
All 1073 previous claim records retain every original field and source
array. All previous source-file records and mathematical dependency lists
are unchanged. Version-0.22 notes are additive. The package preserves all
1065 v0.21 files, moving only its 19 root files to history/version_0_21/
when those current filenames are replaced or retired. Earlier historical
directories and component bytes remain intact.

Scoped mathematical reviews and exact source/hash checks are recorded in
reviews_v0_22/. The mathematical dependency graph is acyclic; it is a
human reconstruction graph, not a transitive Lean dependency audit.
No full Lean compilation, independent kernel replay, or global proof
certification was performed. SHA256SUMS covers every packaged file except
itself. package_v0_22.py verifies predecessor continuity, archive CRCs and
every archived file against that manifest.
