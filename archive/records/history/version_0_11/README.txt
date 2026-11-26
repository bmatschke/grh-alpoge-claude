RH AND DIRICHLET-GRH READABLE RECONSTRUCTION — VERSION 0.11
Prepared for Benjamin Matschke, 21 November 2026.

STATUS
This is a partial human reconstruction, not a completed independent proof
of RH or Dirichlet GRH. It preserves both completed supplied-data local
theorems and now proves the actual numerical family supply, finite
coefficient extension, orbit application and global degree selection.
Full arithmetic-family construction and four independent global branches
remain explicit. These are limits of this exposition, not assertions of
omitted arguments in the released source.

MAIN NOTE AND READING ORDER
RH_readable_reconstruction_v0_11.pdf is the cumulative 125-page note.
Its matching TeX source is included. Start with the route and analytic
argument, or go directly to the new application:

  GJ1–GJ5: actual family/orbit join, page 92.
  GW1–GW6: one degree pair controlling all candidate primes, page 94.
  HW1–HW3: the active host preselection and fixed-pair family, page 96.
  GII1–GII10: actual Type-II family data and probability, page 82.
  GI1–GI8: actual Type-I family hypotheses and mean, page 86.
  BC1–BC8: standard coefficient ring and finite extension, page 89.

The shorter main sections are supported by complete expanded report.txt
companions in those six component directories. Each directory also has
a standalone source-ledger builder and declaration/range locators.

WHAT THE NEW PROOFS ESTABLISH
GII proves the actual per-good-orbit count, logarithmic windows and every
Type-II numerical inequality, including N1^2<=rN and the full Q^5 size
budget. Its probability argument proves uniform-Bernoulli BadProb and
existential TopsOK, with forced-point conditioning handled explicitly.
The actual host additionally needs biased coset selection and Frame.Shares;
uniform per-good-orbit density alone is not an abundance assertion.

GI proves all fourteen actual Type-I numerical fields, exact window and
forbidden-band translation, the actual cyclic predecessor/time bound,
and the canonical mean from the completed local theorem TC6. The fixed
coefficient vector is chosen before a single threshold uniform in all
family indices, primes and good representatives.

BC constructs the standard ring W(F_(q^2))[omega]/(omega^2-p), a finite
normalization and an embedding inducing the specified number-field place.
It proves integral coefficient-lattice, algebraic-dual, arbitrary clean
intersection and GoodRankK transport. LPprime extends with precisely the
same height t, depth D, deficit kappa and conductor c*. The image of omega
need not be a uniformizer in the larger ring. StdSubAt means a standard
coefficient SUBRING. The actual GroupCompatibilityFamily ring field is
one application; recC/IsRecCEv is another sufficient identification.

GJ proves attainment of the universal Type-I deficit infimum without
losing its ring/weight/target quantifiers. It obtains explicit uniform
scale bounds, identifies the actual cyclic orbits and weights, and proves
the literal OrbitLatticeBounds join for both prime ranges.

GW uses exact constant-fibre marginalization of the finite degree boxes.
The local mean bound E kappa_v<=Nv*x^-12 yields E Sigma_p<=m*|TT|*x^-12.
An elementary harmonic sum and the indicator bound give
  E Z <=8*x^(-9-gamma), gamma=1/2-(1453/150)eps>2447/7800.
For 32*x^-gamma<=1, one pair satisfies the exact source inequality
  sum_candidates (log p)/p * (2*1_(Sigma_p>x^-eps)+4*Sigma_p) <= x^-9.
The same pair is used at all primes; independence between primes is not
required. ChosenW transports it through every member carrying the pair.
Optional CoverAll gives a carrier, but it is not imposed on the active route.

HW follows that active route: transfer the point degree condition to host
WOK, preselect one pair, rebuild points at all distinguished positions
with that fixed pair, and pass through KitS/famOfKits to ChosenWall and
ChosenWS. The upstream host and point constructors, numerical supply at
that construction, and biased Frame.Shares remain explicit premises.

PRESERVED LOCAL ENDPOINTS
Type I: TC6 proves literal HypI=>Conclusion2 for C0>=880, CH>=2800001,
C=302114. Type II: EA9 proves literal Hyps=>ConclusionE for C>=4129,
with cloud constants (10,54,1088). The sufficient constants are not
claimed optimal. Their original proofs and ledgers are unchanged.

SOURCE AND BACKTRACKING
Repository: https://github.com/CocoSgt/riemann-hypothesis-lean
Pinned commit: 7cbf7a0c32fca1badf05931879a37c3f8a2b03b4
Current ledger: 408 stable claims, 6793
source links, 949 indexed primary source files.
There are 40 new claims: GII10+GI8+BC8+GJ5+GW6+HW3.

Every source record has its qualified declaration, inclusive original
line range, pinned URL, full-file SHA256 and range SHA256. The current
component builders compare source bytes with the pinned Git blobs.
provenance.json is authoritative; provenance.txt is its readable view.
source_index.json records the full-file hashes. The explicit mathematical
dependency graph is acyclic; it is not a Lean transitive dependency audit.

Examples after unpacking, with a local pinned source checkout:
  python backtrack.py GW5
  python backtrack.py HW2 --repo /path/to/riemann-hypothesis-lean
  python backtrack.py BC7 --repo /path/to/riemann-hypothesis-lean --entry 1
  python backtrack.py --check-all --repo /path/to/riemann-hypothesis-lean
The read-only helper works without network access and can resolve every
historical ID, its newer annotations, and the current continuation ranges.

CONTINUITY
All 368 prior claim fields/source arrays, all 890 prior source-file
records and every prior mathematical dependency edge are preserved.
Only version_0_11_update annotations are appended to EA9 and TC6.
Every predecessor file is byte-identical at its original package path or
under history/version_0_10/. Exactly twelve superseded root files are
archived there, including the v0.10 note and checkpoint. Earlier histories
and all earlier source locators remain included.

NEXT WORK
The concrete next targets are in next_source_targets.json and the
continuation checkpoint. They prioritize actual host construction with
biased Frame.Shares, the underlying local-place/character/rank/comparison
data, and the remaining gain/prime-loss estimates. They distinguish
active constructors from wrappers and optional sufficient interfaces.
The same four independent branches remain: actual theta/spectral kernels,
dimension/metric/discarded-target control, congruence/cohomological windows,
and simultaneous PairEx plus the centered prime-sum window theorem.

VERIFICATION AND LIMITS
The mathematical cross-reviews, exact-source checks, historical-preservation
checks, PDF visual review and package checksums are recorded. visual_qa.json
names the exact reviewed PDF by SHA256. Every PDF page was rendered and
visually reviewed. SHA256SUMS covers every package file except itself.
No Lean source was modified; no full Lean build or independent kernel replay
was run. This package makes no new public verification-status assertion.
