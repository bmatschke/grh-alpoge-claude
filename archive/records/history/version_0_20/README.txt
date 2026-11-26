RH AND DIRICHLET-GRH: HUMAN RECONSTRUCTION, VERSION 0.20
Date: 2026-11-22
Source: https://github.com/CocoSgt/riemann-hypothesis-lean
Pinned commit: 7cbf7a0c32fca1badf05931879a37c3f8a2b03b4

CURRENT STATUS
==============
Partial human reconstruction of RH and Dirichlet GRH. This increment proves normalized one-dimensional adic-character realization from the stipulated global Artin map, its finite-DVR descent and actual shift/block/local consequences with the installed-reading compatibility retained. It proves qualitative finite Weil algebraicity for the actual supplied representation and vacuum, the normalized jet field and period fields for supplied bottom triangles. It reconstructs the local Hermitian densities and global mass-ratio induction, with Hasse–Minkowski explicitly used as a named classical theorem. It constructs the actual ray-class LFam and proves its uniform weighted interval estimate, including polynomial real-zero bounds and exact Perron endpoints, thereby supplying ShortNorm and the required level/dyadic norm primes. Compatible nonempty arithmetic data and full geometric core, canonical new bottom-Weil existence, quantitative dictionaries, critical ratio fields and same-embedding theta joins, and the four global branches remain. No complete self-contained RH/Dirichlet-GRH proof, full Lean build or independent kernel replay is asserted.

The complete current readable note is RH_readable_reconstruction_v0_20.tex.
No new PDF was rendered in this round, following the user's preference to
prioritize proof work, TeX and the updated archive. The 150-page v0.13 PDF
is preserved under history/version_0_13/ as a historical predecessor;
it does not contain any increment after v0.13. No v0.20 page count or visual
layout review is claimed. tex_validation.json records the exact check used.

NEW MATHEMATICS
===============
- GA1–GA23: construct the actual normalized algebraic Hecke-to-adic character from GlobalArtin, prove finite-DVR closed-image/integral-unit/topology descent, and retain the exact inverse-Frobenius convention. Prove shift/block realizations, reading independence, identification with the installed first character under its reading record, all five host character laws and actual conditional local IsGalOf/DeltaRead consequences. Keep nonempty index/coverage and same-object form/tuple compatibility separate.
- WA1–WA19: prove the actual finite-Weil algebraic-span theorem using finite Heisenberg projectors, algebraic coefficients and pairings, split normalization to fix phase, positive-power closure and local unitary generation. Supply NFJet and SumsIn for every literal supplied bottom triangle. Construct standard bottom geometry conditional on the two new full Weil data, and reduce arbitrary splitting characters to the canonical eta case. Keep quantitative DictAt, critical ratio fields and the exact Choice embedding join explicit.
- MF1–MF20: prove local Hermitian diagonalization and representation, finite matrix/vector densities including dyadic places, the weighted local orbit law and literal LIStat, rank-one mass independence, global finite fiber patching, weighted singular-series averaging and the rank induction. Obtain the exact SiegelMassRatio and standard SiegelMassRatioCM normalization; explicitly retain only classical Hasse–Minkowski in the global representation step. Supply the mass premise of QW9 while retaining actual geometric volume/core identities.
- QR1–QR25: construct every field of the exact ray-class LFam with conductor4dM^2 and same-family NormOne support. Prove Mellin continuation, logarithmic derivative, a uniform B^-45 real-character value bound, B^-46 zero separation, family-wide unique simple exception, the uniform explicit formula and a B^-47 weighted short-interval bound. Close both QW11 suppliers and obtain ShortNorm with exponent47, then the literal level-prime window and nine-tenths dyadic norm-prime count.

REMAINING INPUTS
===============
- Construct compatible nonempty twist/local index data on the same D, with all-place SideB.cover, actual field containments and coefficient readings, normalized installed characters, genuine representation/weight/form data and the MtReal/NExpTied/ColW/Pre2/St/RowPk joins. GA now supplies normalized characters and conditional local identities after those inputs exist. Its character replacement on an empty-Loc skeleton is explicitly not the needed nonempty form realization. Global Artin reciprocity remains a named published input.
- Supply the compatible V4.Core and its real/twist/object/layout, recursive and integral comparisons, including the geometric VolumeEqMass2/VolTie and indefinite volume normalizations. MF now proves the actual mass ratio using classical Hasse–Minkowski; it does not identify these unrelated geometric volumes or construct the core.
- Construct the canonical full adelic bottom-Weil data (exists_weilDatum_etaTilde) with actual finite/real action, commutation and rational theta-distribution automorphy. WA proves finite algebraicity for any supplied literal datum and gives explicit splitting-character adjustment, not existence of every new full datum. The stronger quantitative all-embedding and finite-unit DictAt dictionary remains.
- Complete the critical ToricRatioConjugates field with its exact CM/reference-twist data, and join all theta fields through the same Choice.FieldOK embedding, normalization, frame and family. The qualitative finite-Weil arithmetic, NFJet and supplied-bottom SumsIn are now proved. Remaining analytic convergence, separating functionals, nonvanishing/tower/ratio and positive ThmBop/ThmAop/PartsE/PartsW inputs retain their literal scopes.
- Complete the independent quantitative chain-norm and archimedean spectral-word identities, positive kernel/mass normalization, exceptional-word bounds, actual GalD/dimension balance, integral/isometric metric transport and discarded-target control. Rational common image and rank equality alone do not give these estimates.
- Complete congruence denominators LinkN/LinkV, two-primary and odd-minus/odd-plus cohomological windows, simultaneous PairEx choices and uniform gain-to-centered-prime-sum/final parameter supply. QR now supplies the particular unconditional arithmetic ShortNorm and level/dyadic norm-prime theorems under their source interval and geometric hypotheses; it does not supply these simultaneous global objects.

HOW TO CONTINUE
===============
Start with continuation_checkpoint.json. next_source_targets.json records
150 exact next-source ranges and their remaining human
scope. The targets are a work map, not additional proved claims.

provenance.json contains 983 stable claims and
13936 exact source-range links;
provenance.txt is its readable companion. Every new component has main.tex,
report.txt, a hashed source ledger and a reproducible locator builder.
The cumulative TeX embeds the complete readable proof text, so it does not
need the fragments in order to compile with a standard LaTeX installation.

For a claim lookup:
  python3 backtrack.py QR24
For source excerpts from a pinned checkout:
  python3 backtrack.py QR24 --repo /absolute/path/to/lean-source
For all recorded source byte and inclusive-range checks:
  python3 backtrack.py --check-all --repo /absolute/path/to/lean-source
For a future PDF build, run pdflatex twice on the current TeX in a build
directory, then inspect the rendered pages. Such a build is not included
in this version's verification claims.

PRESERVATION AND VERIFICATION
============================
All 896 previous claim records retain every original field and source
array. All previous source-file records and mathematical dependency lists
are unchanged. Version-0.20 notes are additive. The package preserves all
928 v0.19 files, moving only its 20 root files to history/version_0_19/
when those current filenames are replaced or retired. Earlier historical
directories and component bytes remain intact.

Scoped mathematical reviews and exact source/hash checks are recorded in
reviews_v0_20/. The mathematical dependency graph is acyclic; it is a
human reconstruction graph, not a transitive Lean dependency audit.
No full Lean compilation, independent kernel replay, or global proof
certification was performed. SHA256SUMS covers every packaged file except
itself. package_v0_20.py verifies predecessor continuity, archive CRCs and
every archived file against that manifest.
