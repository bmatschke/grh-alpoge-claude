RH AND DIRICHLET-GRH READABLE RECONSTRUCTION — VERSION 0.13
Prepared for Benjamin Matschke, 21 November 2026.

STATUS
This is a partial human reconstruction, not a completed self-contained proof
of RH or Dirichlet GRH. Version 0.13 proves the common global-frame/companion
algebra, actual class-rank equality and exact integral comparison span under
the literal compatible-forms/value hypotheses. It also patches the prescribed
local lattices and installs the exact normalized length fields under their
stated local and refill assumptions. The simultaneous forms/value/model
construction and independent global inputs remain explicitly identified.
These are boundaries of this exposition, not claims of missing arguments in
the released Lean source. The GRH scope is Dirichlet L-functions.

MAIN NOTE AND READING ORDER
RH_readable_reconstruction_v0_13.pdf is the cumulative 150-page note.
Its matching TeX source is included. The new sections start here:

  SF1-SF7: one global frame for all local comparisons, page 108.
  CR1-CR6: the actual class-rank identity, page 111.
  CS1-CS9: the exact global comparison lattice, page 114.
  LP1-LP5: patch selected local lattices into one global lattice, page 118.

For this increment, read SF then CR then CS. LP is a separate advance in the
point construction. Each component directory includes a readable expanded
report.txt, the main.tex fragment, source provenance and its ledger builder.
The current remaining-work section starts on page 139; the claim ledger
starts on page 141. Every earlier component and historical proof is retained.

NEW MATHEMATICS AND ITS BOUNDARY
SF uses one supplied global orthonormal integral basis throughout. In the
actual positive true-column coordinates that basis is standard. The explicit
Hermitian dual of L_pi=O_E^(n-1) plus pi O_E gives the exact companion identity
L_pi + conjugate(pi) L_pi# = O_E^n. The projected lattices away T are expressed
in the same global frame. The original embeddings, representatives, c^s
parity and normalized valuations survive the frame replacement. This does
not independently construct all standard forms/carriers and their values.

CR computes the actual integral Weyl fiber rank, identifies the double-coset
classes with the relevant lattice-orbit classes and proves stabilizer
triviality using the actual upper-unitriangular conditions at two distinct
auxiliary primes. Evaluation gives the product rank formula and literal
locPack_d_eq/pack_d_eq. The Joint0 argument is unused in this rank equality.
Delta is not equated with its dual coefficient lattice nabla over integers.

CS proves exact integral span O-span(C(global lattice))=M. Its odd-position
duality is an integral complementary-minor map with the correct signs and
integral Gram inverse. It retains the same embeddings and parity. Pivot
descent and exact finite-place approximation give rational integral-function
spanning. The rational comparison becomes surjective using CR and the
separate emb_basis/Fi_zero bridge; an L-linear retraction handles descent.
The final span equality follows from the integrality criterion. All steps
retain the same supplied Forms0, ValEx, Joint0, character rationality and
comparison record. SameUloc is supplied by Joint0, not another open theorem.
No norm or covolume equality is inferred from the module equality.

LP proves the exact finite-place patch over a number ring by denominator
clearing and localization of an intersection with a common-denominator
condition. For finitely many prescribed A_P, it obtains N_P=A_P and leaves
all other localizations unchanged, with dM subset N subset d^(-1)M. The
actual reference is retained Mram. Type-prime targets may enlarge it, so a
global containment N subset M is not claimed. Conditional setLat installs
lenMN=lenLoc.toNat/e_w, with the exact finite-length equality. Full geometric
Lay/RecOK/LedOK, canonical refill, pointRecExP/ObjCP and NumAt remain inputs.

PRESERVED LOCAL ENDPOINTS
Type I: TC6 proves literal HypI=>Conclusion2 for C0>=880, CH>=2800001,
C=302114. Type II: EA9 proves literal Hyps=>ConclusionE for C>=4129,
with cloud constants (10,54,1088). These sufficient constants and their
proofs are preserved; they are not claimed optimal. The v0.12 biased tops,
no-relation set, conditional host joins and local identifications also remain.

SOURCE AND BACKTRACKING
Repository: https://github.com/CocoSgt/riemann-hypothesis-lean
Pinned commit: 7cbf7a0c32fca1badf05931879a37c3f8a2b03b4
Current ledger: 465 stable claims, 7593 source links, 1098 indexed source
files. The 27 new claims are SF7+CR6+CS9+LP5.

Each source entry records the original declaration, exact inclusive line
range, pinned URL, full-file SHA256 and range SHA256. Source bytes were
checked against pinned Git blobs. provenance.json is authoritative;
provenance.txt is its readable view; source_index.json records file hashes.
The mathematical dependency graph is acyclic. It is not a Lean transitive
dependency audit. next_source_targets.json records 30 exact continuation
ranges, grouped by forms/value supply, point/NumAt, host arithmetic and the
four independent global branches.

Examples after unpacking, with a local pinned source checkout:
  python3 backtrack.py SF7
  python3 backtrack.py CR6 --repo /path/to/riemann-hypothesis-lean
  python3 backtrack.py CS9 --repo /path/to/riemann-hypothesis-lean --entry 1
  python3 backtrack.py LP4
  python3 backtrack.py --check-all --repo /path/to/riemann-hypothesis-lean

The read-only helper works without network access. Its final check verified
1109 distinct files including continuation targets, all 7593 claim-source
ranges and all 30 target ranges. The output is preserved in reviews_v0_13.
No Lean sources are bundled or modified; use a separate pinned checkout.

BUILD AND CONTINUITY
The PDF was built offline using the installed LaTeX packages and fonts.
Ordinary pdflatex can build the supplied cumulative TeX; build_pdf.py also
records the environment-specific offline format and font-map workaround.
assemble_v0_13.py reproduces the cumulative TeX from the archived v0.12
source and four fragments. merge_v0_13.py merges the exact ledgers and checks
the continuation against a sibling lean-source checkout at the pinned commit.
finish_metadata_v0_13.py records the final review/checkpoint metadata; its
reproduction uses the separate scratch render manifest, not bundled images.

All 438 prior claim fields/source arrays, all 1032 prior source-file records
and every old dependency adjacency list are preserved. Only explicit v0.13
annotations are appended to PL13, PL16, BC8, LI5 and LI8. Earlier local
conclusion records retain their exact values. Every one of the predecessor's
425 files is byte-identical at its original path or in history/version_0_12/.
Exactly twelve superseded root files, including the old PDF, are archived.

REMAINING WORK
The next priority is the simultaneous standard forms and polynomial-value
construction: formsTiedSym_std, val_tied, the carrier/column joins and ValEx.
The new comparison theorem is proved with those actual compatible data as
explicit premises. The remaining point and NumAt construction must retain
the Mram reference and type-prime/ramification distinctions proved in LP.
Underlying HostAx/character-field and analytic suppliers also remain.

The four independent global branches are unchanged: theta/spectral kernels;
dimension/metric/discarded-target control; congruence/cohomological windows;
and simultaneous PairEx plus the centered prime-sum window theorem.
Optional CoverAll and IsRecCEv are not imposed on the active family route.

VERIFICATION
Mathematical cross-reviews, exact source checks and continuity checks are
recorded. visual_qa.json identifies the final PDF by SHA256. All 150 pages
were rendered and reviewed in contact sheets; the front page and every new
proof page were also inspected individually. No clipping or missing-glyph
issues were observed. The final TeX log has no overfull boxes or unresolved
references. SHA256SUMS covers every package file except itself; transient
build output and render images are excluded. No full Lean build or independent
kernel replay was run. No new public verification-status assertion is made.
