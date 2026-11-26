RH AND DIRICHLET-GRH: HUMAN RECONSTRUCTION, VERSION 0.21
Date: 2026-11-22
Source: https://github.com/CocoSgt/riemann-hypothesis-lean
Pinned commit: 7cbf7a0c32fca1badf05931879a37c3f8a2b03b4

CURRENT STATUS
==============
Partial human reconstruction of RH and Dirichlet GRH. This increment constructs the nonempty coefficient family indexed by every finite prime of the fixed coefficient field, complete coefficient towers, universal finite anticyclotomic quotients and readings inducing every prescribed full-field place; its bounded integral row representations retain GalEx, RowCusp and ChebSplit. It constructs the canonical finite and real Weil actions on the actual theta space, proves the rational pullback identity by exact finite and real phase cancellation, and supplies full bottom-Weil data and prescribed-character adjustments. It identifies the actual normalized adelic quotient volumes and their mass/trueVol/stage consequences, explicitly conditional on the precisely normalized classical unitary Tamagawa-number theorem; Hasse–Minkowski remains named for UnitSplit. It proves the actual Dirichlet analytic inputs, exact centered integral identities and uniform QH.thin/ThinH under the original real-zero exclusion/RealBox hypotheses. Genuine form realization and compatible nonempty local stages, the remaining full Core and discrete-series/formal-degree inputs, quantitative theta dictionaries, critical ratio fields and exact Choice joins, and the independent global/cohomological/simultaneous-prime branches remain. This is not a complete self-contained RH/Dirichlet-GRH proof, full Lean build or independent kernel replay.

The complete current readable note is RH_readable_reconstruction_v0_21.tex.
No new PDF was rendered in this round, following the user's preference to
prioritize proof work, TeX and the updated archive. The 150-page v0.13 PDF
is preserved under history/version_0_13/ as a historical predecessor;
it does not contain any increment after v0.13. No v0.21 page count or visual
layout review is claimed. tex_validation.json records the exact check used.

NEW MATHEMATICS
===============
- NR1–NR24: construct the actual nonempty TwR/RingSpec family on all finite primes of the fixed coefficient field, its complete unramified/cyclotomic coefficient towers, normalized characters and finite universal anticyclotomic quotients. Prove the exact SideB.cover coefficient clause and a Reading inducing every prescribed full-field place. Prove finite coefficient descent and stable integral lattices for compact representations, and the literal bounded rho_rows supplier under GalEx/RowCusp/ChebSplit. Preserve the fixed D, global fields, rows and embeddings.
- CW1–CW25: construct the finite lattice action, its signed Gauss normalization and crossed splitting character; construct the real oscillator by convergent Gaussian projectors with exact determinant phase and verified smooth domain. Prove finite-real commutation, pointwise continuity and a norm-sensitive scalar lemma. Evaluate the actual Gaussian theta test and cancel the rational finite/real phase to get the full rational pullback identity. Supply canonical and prescribed-character full Weil data, and the previously conditional standard bottom-Weil construction.
- GV1–GV21: construct the actual normalized Haar measures and fundamental domains; compute all finite and real gauge constants including the dyadic factor and compact-dual density. Prove the definite quotient-to-genus-mass identity directly. Using the explicitly retained classical unitary Tamagawa-number theorem, derive the exact positive quotient volume, signature independence, VolumeEqMass2, trueVol and same-stage VolTieG. Prove UnitSplit using the inherited Hasse–Minkowski input, the precise volume ratio, trueScale and conditional RealTied/Core joins with the separate discrete-series/formal-degree premises retained.
- CC1–CC20: reconstruct primitive Dirichlet completion, local zero counts, the zero-free strip with its real exception and the exact floor-endpoint explicit formula. Identify both centered constants and prove G0=-y integral psi0/u^2. A uniform tail argument supplies QH.thin and the actual same-host ThinH implication from RealBox. Add a derivative/increment estimate above the same exponential cutoff. Do not infer the distinct polynomial-window square-root estimates, PairEx or relative progression theorem.

REMAINING INPUTS
===============
- Install the new all-prime ring family into genuine compatible form and local data on the same D: TwF/TwL, MtFam/MtReal/MtAd/MtInput, full SideB, normalized residual/Hecke/tame agreements and nonempty LocsCover, followed by the exact NChoice/ColW/Pre2/St/RowPk joins. NR supplies coefficient coverage and inducing readings, not these form realizations. Global Artin reciprocity, GalEx, RowCusp and ChebSplit remain explicit inputs where used.
- Complete the same-object V4.Core with its layout, recursive/integral comparisons, forced primes and conductor-support/exponent identities. GV supplies actual geometric volumes and scale; its global volume theorem still uses the named unitary Tamagawa-number theorem. DiscreteSeriesExist and FormalDegreeFormula2 remain substantive separate inputs for the middle RealTied fields. Hasse–Minkowski remains named for UnitSplit and the earlier mass proof.
- Prove the stronger quantitative all-embedding/finite-unit DictAt dictionary, critical ToricRatioConjugates field and the exact same-embedding/frame/family Choice.FieldOK join. The canonical full Weil existence, qualitative finite arithmetic, normalized jets and supplied-bottom periods are available; the universal IsEtaTilde bridge via GlobalNormIndexTwo is not silently claimed by the actual-character bypass.
- Complete the remaining theta analytic convergence, separating functionals, nonvanishing/tower/ratio and positive ThmBop/ThmAop/PartsE/PartsW inputs with their literal data. Full Weil automorphy does not prove these analytic/operator inequalities.
- Complete independent chain-norm and archimedean spectral-word identities, positive kernel/mass normalization, exceptional-word bounds, actual GalD/dimension balance, integral/isometric metric transport and discarded-target control. Equality of rational spans or ranks remains insufficient for these estimates.
- Complete congruence denominators LinkN/LinkV and the two-primary and odd-minus/odd-plus cohomological windows, preserving the exact source objects and quantifiers.
- Construct simultaneous PairEx choices and RealBox on the actual selected host; prove the stronger relative progression estimate and the uniform gain-to-centered-prime-sum/final parameter chain. CC now supplies ThinH conditional on RealBox and controls all later exponential-cutoff endpoints, but it does not supply the different polynomial-window mean-square/zero-density estimates.

HOW TO CONTINUE
===============
Start with continuation_checkpoint.json. next_source_targets.json records
186 exact next-source ranges and their remaining human
scope. The targets are a work map, not additional proved claims.

provenance.json contains 1073 stable claims and
14695 exact source-range links;
provenance.txt is its readable companion. Every new component has main.tex,
report.txt, a hashed source ledger and a reproducible locator builder.
The cumulative TeX embeds the complete readable proof text, so it does not
need the fragments in order to compile with a standard LaTeX installation.

For a claim lookup:
  python3 backtrack.py CC19
For source excerpts from a pinned checkout:
  python3 backtrack.py CC19 --repo /absolute/path/to/lean-source
For all recorded source byte and inclusive-range checks:
  python3 backtrack.py --check-all --repo /absolute/path/to/lean-source
For a future PDF build, run pdflatex twice on the current TeX in a build
directory, then inspect the rendered pages. Such a build is not included
in this version's verification claims.

PRESERVATION AND VERIFICATION
============================
All 983 previous claim records retain every original field and source
array. All previous source-file records and mathematical dependency lists
are unchanged. Version-0.21 notes are additive. The package preserves all
997 v0.20 files, moving only its 19 root files to history/version_0_20/
when those current filenames are replaced or retired. Earlier historical
directories and component bytes remain intact.

Scoped mathematical reviews and exact source/hash checks are recorded in
reviews_v0_21/. The mathematical dependency graph is acyclic; it is a
human reconstruction graph, not a transitive Lean dependency audit.
No full Lean compilation, independent kernel replay, or global proof
certification was performed. SHA256SUMS covers every packaged file except
itself. package_v0_21.py verifies predecessor continuity, archive CRCs and
every archived file against that manifest.
