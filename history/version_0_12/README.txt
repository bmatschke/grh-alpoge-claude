RH AND DIRICHLET-GRH READABLE RECONSTRUCTION — VERSION 0.12
Prepared for Benjamin Matschke, 21 November 2026.

STATUS
This is a partial human reconstruction, not a completed independent proof
of RH or all-Dirichlet GRH. It preserves both completed supplied-data local
theorems, their actual numerical family supply, finite coefficient extension,
orbit application and global degree selection. This version proves the
biased top selection and its actual host joins, the separate no-relation
set, conditional host/window assembly and actual local identifications.
The remaining inputs are explicitly stated. These are boundaries of this
exposition, not assertions of omitted arguments in the released source.

MAIN NOTE AND READING ORDER
RH_readable_reconstruction_v0_12.pdf is the cumulative 137-page note.
Its matching TeX source is included. The new sections start here:

  BO1–BO5: actual biased orbit probability, page 97.
  BS1–BS7: one set with exact coset shares and small bad mass, page 99.
  HC1–HC10: actual host tops and conditional arithmetic assembly, page 101.
  LI1–LI8: Frobenius orbits as all local places, page 105.

For a short route through this increment, read BS's selection theorem,
HC's actual host application, and LI's orbit/place identification. BO
supplies the conditional probability input. Each component contains an
expanded report.txt with complete numerical/algebraic details, an exact
source ledger, a reproducible ledger builder and declaration/range locators.
Earlier sections and component reports remain included.

NEW MATHEMATICS
BO treats independent probabilities in [3delta/4,delta], with one selected
point forced. Empty and parity-marked cells are handled directly; the full
badness event is not treated as monotone or invariant under rotation. One
explicit threshold gives conditional badness <=Cb*x^-2, uniformly over the
actual point-dependent based orbits.

BS sums the variances of all coset counts and combines that one quadratic
error with the nonnegative weighted bad count. One finite average then
selects a set satisfying all conditions simultaneously. It has the literal
4/(3o+1),3/(3o+1) shares, with the stronger relative error x^-1 before the
source weakening. The weighted prime bound is <=|TT|*x^(-2+epsilon).
The quotient Fourier calculation explains the weight 1/(3o+1) for every
nontrivial character. No independence between prime-indexed bad events is
required.

HC derives the actual Ltwo bound, installs TT without changing its input
host data, and transports the exact predicates through supplied points and
families. It constructs the source predicate named admitted from supplied
HostAx fields and FieldRows. Its sphere/base-expansion proof gives the
separate no-relation set with constants32 and CT2=64, including removal of
zero, lower size and upper cardinality cap. It proves the elementary prime,
conductor, character and rank joins in the host assembly, retaining the
precise ShortNorm, SmallOne, ThinH, character-field/rank, PairEx and VWinAt
inputs. The o=1 host-only specialization removes the coset-share error and
does not need VWinAt for that host-only conclusion.

LI constructs the unramified completion by simple-root lifting, identifies
all primes with Frobenius orbits, and proves splitting over the real field
by a two-prime CRT argument. It builds the exact local algebra/lattice frame,
aligns the original complex and prescribed coefficient embeddings with the
essential c^s parity, and proves the normalized valuation identity. Under
Joint0 and LevelZeroCharacterRational it constructs the integral inverse
away character. Joint0 supplies the local-carrier equality; the separate
structural identity Cmp.gramN_zero supplies the matching Gram matrix.

PRESERVED LOCAL ENDPOINTS
Type I: TC6 proves literal HypI=>Conclusion2 for C0>=880, CH>=2800001,
C=302114. Type II: EA9 proves literal Hyps=>ConclusionE for C>=4129,
with cloud constants(10,54,1088). These sufficient constants and their
proofs are preserved; they are not claimed optimal.

SOURCE AND BACKTRACKING
Repository: https://github.com/CocoSgt/riemann-hypothesis-lean
Pinned commit: 7cbf7a0c32fca1badf05931879a37c3f8a2b03b4
Current ledger: 438 stable claims, 7396
source links, 1032 indexed primary source files.
The 30 new claims are BO5+BS7+HC10+LI8.

Each source entry records its qualified declaration, exact inclusive
original line range, pinned URL, full-file SHA256 and range SHA256. All
current source bytes are checked against pinned Git blobs. provenance.json
is authoritative; provenance.txt is the readable view; source_index.json
records full-file hashes. The explicit mathematical dependency graph is
acyclic. It is not a Lean transitive dependency audit.

Examples after unpacking, with a local pinned source checkout:
  python backtrack.py BS5
  python backtrack.py HC6 --repo /path/to/riemann-hypothesis-lean
  python backtrack.py LI3 --repo /path/to/riemann-hypothesis-lean --entry 1
  python backtrack.py --check-all --repo /path/to/riemann-hypothesis-lean
The read-only helper works without network access, resolves historical
claim annotations and verifies the current continuation ranges.

CONTINUITY
All 408 prior claim fields/source arrays, all 949 prior source-file records
and every prior mathematical dependency edge are preserved. Only current
version_0_12_update annotations are appended to GII9,GII10,BC8,HW3. Both
version_0_10_local_conclusions and version_0_11_local_conclusions retain
their exact earlier values. Every predecessor file is byte-identical at
its original package path or under history/version_0_11/. Exactly twelve
superseded root files are archived there, including the v0.11 note.

REMAINING WORK
The next-source map prioritizes the common global frame StdTied/Companion,
class-rank equality and actual comparison-lattice span, together with the
point/NumAt construction and the underlying arithmetic/analytic host inputs.
The four independent global branches remain: theta/spectral kernels;
dimension/metric/discarded-target control; congruence/cohomological windows;
and simultaneous PairEx plus the centered prime-sum window theorem.
Optional CoverAll and IsRecCEv are not imposed on the active route.

VERIFICATION
Mathematical cross-reviews, source checks, historical preservation, PDF
review and package checksums are recorded. visual_qa.json identifies the
exact reviewed PDF by SHA256. Every page was rendered and visually reviewed.
SHA256SUMS covers every package file except itself. No Lean source was
modified; no full Lean build or independent kernel replay was run. This
package makes no new public verification-status assertion.
