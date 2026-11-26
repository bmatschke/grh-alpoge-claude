RH AND DIRICHLET-GRH READABLE RECONSTRUCTION — VERSION 0.10
21 November 2026

START HERE
RH_readable_reconstruction_v0_10.pdf is the cumulative 109-page note.
RH_readable_reconstruction_v0_10.tex is its self-contained LaTeX source.

NEW LOCAL CONCLUSION
TC6 completes the supplied-data local Type-I theorem: the literal HypI
implies Conclusion2 with C0>=880, CH>=2800001 and C=302114. The argument
now supplies the actual upper/lower ranks, weighted density, harmonic
models and cloud maps, uniform numerical fields, paired lattice lifts,
shifted height and exceptional-function conclusion. It uses direct
constructions instead of retaining the bundled AdmB/AdmT conditions as
unproved mathematical inputs.

The earlier supplied-data local Type-II theorem EA9 is unchanged:
ConclusionE holds under literal Hyps for C>=4129, with the cloud
constants (10,54,1088). Both statements retain their supplied local data.

This is still a partial human reconstruction of RH and Dirichlet GRH.
It is not a self-contained proof of either. GRH here concerns Dirichlet
L-functions; the note does not claim general automorphic or Dedekind GRH.
The actual global family existence and good-orbit abundance, finite-place
base change, theta/spectral and metric comparisons, cohomological windows
and simultaneous prime-selection arguments remain explicit work.

WHAT IS NEW
RU1–RU11: actual coarse upper rank, exact digit/HH dimensions, weighted
coefficient lattices and the paired HH assembly with primitive partners.
RD1–RD15: actual signed-chain lower rank, weighted bad-tail counting,
half-density, harmonic density and the final averaged segment loss.
HM1–HM12: harmonic-model and dimension identification, Smith/edge
transfer and KeyIneq, integral cloud maps via complementary minors,
and the complete-DVR RS-isomorphism argument for ring uniformity.
NP1–NP9: literal Std with H=4 and the full numerical package, including
all floor/ceiling bounds and the final shifted Type-I height.
TC1–TC6: primitive retraction, Smith splitting, Weyl losses, tensor
transport, the actual incoming GoodRankK construction, and Conclusion2.

The final heading-based section starts are:
  RU 66, RD 70, HM 74,
  NP 77, TC 80.
The titles are detected in heading-sized PDF spans, so prose references
on the cover cannot be mistaken for a section. Shared start pages are
allowed. No page number is hard-coded in the packaging procedure.

READING ORDER
For the new endpoint, read TC and its exact hypotheses, then RU/RD,
HM and NP. The previous GG/TP/SW/RL sections give the actual graded
Gram, compatible-partner, weighted-form and paired-lift mechanisms.
The expanded reports are in rank_upper/, rank_lower/, harmonic_model/,
numerical_parameters/ and type_one_closure/.
For the RH implication, begin with the analytic endpoint, scalar balance
and frame/slope sections. Ordinary RH and a fixed Dirichlet character
have distinct host/window sections and remain separately identified.

CURRENT GLOBAL FRONTIER
The next_source_targets.json map has 24 exact
declaration ranges in 12 source files,
plus the same four independent global branches as the prior checkpoint.
It now points to the actual arithmetic-family HypIAt/HypIIAt supply,
uniform good-orbit abundance and finite-place StdSubAt/LPBaseChange.
These are different from the literal local HypI/Hyps implications
completed here. In particular, HM12 proves invariance under RS
isomorphisms; it does not prove arbitrary finite coefficient extension
or the global standard-submodule/base-change construction.

The theta/common-image and spectral/arithmetic-kernel identities,
retained-source metric transport and discarded-target control,
congruence denominators, two-primary and odd cohomological windows,
PairEx prime selection and the uniform centered-prime-sum conclusion
remain as stated in the main note. Supplied good-orbit geometry alone
does not prove that sufficiently many global good orbits exist.

PROVENANCE AND BACKTRACKING
provenance.json has 368 stable claims, including
53 new claims, 5817 exact source
links and 890 indexed primary source files.
provenance.txt is the readable ledger; source_index.json indexes files.
All 315 old claim fields/source arrays, all 764 old source-file records,
and every old dependency-graph entry are preserved. Version histories
only append annotations. The current version_0_10_update fields explain
which earlier local premises have been discharged. Historical component
reports retain their original scope and wording.

Every predecessor component/workflow/history file remains byte-identical.
The twelve superseded v0.9 root files, including its PDF/TeX, target map
and ledger, are preserved under history/version_0_9/. The earlier history
and baseline_provenance.json remain at their existing paths.

Pinned repository: https://github.com/CocoSgt/riemann-hypothesis-lean
Pinned commit: 7cbf7a0c32fca1badf05931879a37c3f8a2b03b4

Portable read-only lookup:
  python3 backtrack.py --list
  python3 backtrack.py RU8
  python3 backtrack.py RD15
  python3 backtrack.py HM12
  python3 backtrack.py TC6
  python3 backtrack.py SW8
  python3 backtrack.py RU11 --repo /path/to/riemann-hypothesis-lean --entry 1
  python3 backtrack.py --check-all --repo /path/to/riemann-hypothesis-lean

The tool displays all version updates through version_0_10_update,
current proof locations linked by discharged_by, exact source ranges,
dependencies and merged applications. Historical status is labelled as
such, so it is read alongside the newer completion annotation.
With --repo, every excerpt is preceded by file- and inclusive-range
SHA256 verification. --check-all verifies all indexed source files,
all claim-source ranges and all current next-target ranges. The default
excerpt cap is 160 lines; --max-lines changes it. No network or third-party
Python package is required for the portable backtrack utility.

The huge source checkout and render/build caches are omitted. The
workflow_v0_10/ directory records the assembly, provenance, source-target,
review-metadata, rendering and packaging scripts. Those workflow scripts
record this workspace's layout; backtrack.py is the portable reader.
Review text, JSON join-source metadata and its builders are included
under reviews_v0_10/ as well as their applicable workflow locations.

PRECISION AND REVIEW
All earlier precision constraints remain in continuation_checkpoint.json,
with explicit supersession notes where the new local proofs apply.
The exact representation-dimension weights, digit multiplicities,
factorials and p/w normalizations are retained. The pairing convention
beHH=p^AHH G(F) is multiplicative. The lower-rank count uses actual kept
blocks; the upper matching does not require monotone early caps.

TC keeps the primitive dual factor p^(AH_minus-AH_plus), the one-sided
Smith hypothesis nLeD, the signs of the Weyl losses, and the small-weight
tensor height correction. Its incoming vectors are genuinely in the
cleaned lattices and satisfy GoodRankK through their actual pairing
matrix. An attained integer-valued exceptional certificate is transported
between RS-isomorphic coefficient rings; independently chosen exceptional
functions are not asserted equal. The constants stated above are
sufficient and are not claimed optimal.

Scoped mathematical cross-reviews are included. The exact final PDF has
been rendered and every page visually reviewed. No Lean source was
modified and no full Lean compilation or independent kernel replay was
run for this human reconstruction. Source-byte checks and mathematical
reviews are not presented as a kernel replay.

CONTINUATION AND INTEGRITY
continuation_checkpoint.json leads with the two completed local theorems
and the remaining global frontier. It preserves earlier findings and
precision constraints with their historical status.
visual_qa.json identifies the exact reviewed PDF by SHA256.
SHA256SUMS covers every bundled file except itself. ZIP membership,
duplicate-name absence, every CRC and every archived byte are checked
against the final folder. All predecessor files are preserved either
at their existing paths or in history/version_0_9/.
