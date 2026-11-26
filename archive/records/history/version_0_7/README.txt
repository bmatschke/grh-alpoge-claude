RH AND DIRICHLET-GRH READABLE RECONSTRUCTION — WORKING VERSION 0.7
21 November 2026

START HERE
RH_readable_reconstruction_v0_7.pdf is the complete 68-page main note.
RH_readable_reconstruction_v0_7.tex is self-contained LaTeX source.

The local selected-symbol theorem is now proved under its exact supplied
frame, DVR, degree and size hypotheses, with the source constants
C0=1088, Crk=1, Cdeg=10. This remains a partial human reconstruction,
not a self-contained proof of RH or GRH. The GRH scope is all Dirichlet
L-functions; unrestricted automorphic or Dedekind GRH is not asserted.

THE NEW LOCAL THEOREM
For supplied Conclusion2 data, the span of the actual allowed generators
contains an ambient integral direct summand with a basis of actual
generators. Its rank is at least q^(-rK) times the explicit degree product
and loss factor (1-N*r^2*k/Y), where q=p^n', k=r+K and N=|TT|.
Every polynomial in the entire allowed-generator span has normal degree
at most 10N(La*a/(p*k)+a*p^(-L1)+k*Q). The plane-normalized rank clause
also follows. Full compatible Type-II data and the Type-I branch are
separate tasks.

NEW IN THIS VERSION
* CG1–CG9: integral path-space identification, saturation, residue lifting,
  exact coarse labels and numerical margins, and an individual-generator
  congruence for Delta*u.
* LA1–LA6: actual segment residue bases, periodic geometry, mixed-radix
  injection including the wrap x-n', and exact physical degree matching.
* GP1–GP12: exact path weight, persistent tail deficits and Abel summation,
  a direct Weyl estimate, actual integral membership and independence,
  terminal residue padding, and RestSeg 1088.
* RS1–RS8: all family degree admissibility, label sums, binomial and
  geometric comparisons, and the complete RestPad/RestSum calculation.
* RK1–RK3: RestCount, actual-generator RestRank, primitive basis/complement,
  plane normalization and degree, completing the former SD8 frontier.

New section start pages:
  CG=34, LA=36, GP=37,
  RS=40, RK=41.
Expanded complete arguments are in coarse_lift/, segment_assembly/,
good_paths/, residue_summation/ and rank_closure/.

READING ORDER
For the new result, read RK first, then CG/LA/GP/RS.
For the global route, read the analytic endpoint, square-root scalar
balance and common-lattice slope comparison. The local route is EL,
SY/IP, IW/CB/CL, IN/WT, PG/DT, SD, CG/LA/GP/RS/RK, then JR, LW and LC/SR.
Ordinary RH and fixed-character Dirichlet GRH have separate host/window
sections. The main note retains the earlier reconstructed proofs.

Every historical component report and ledger is preserved byte-for-byte.
Their earlier status descriptions remain historical. The current main
note and explicit version_0_7_update entries in the merged ledger give
the current boundaries. SD8 is kept as a stable identifier; its former
quantitative-density frontier is now completed. Supplied-data local
conclusions are never silently promoted to global parameter existence.

SOURCE BACKTRACKING
provenance.json: 231 stable claim IDs, including 38 new claims,
and 2993 exact source links.
provenance.txt: the readable ledger.
source_index.json: hashes for 534 primary source files.
All earlier claim IDs and source arrays are preserved. Every full-file
and cited-range hash was rechecked. Ranges are one-based and inclusive.

Pinned repository:
  https://github.com/CocoSgt/riemann-hypothesis-lean
Pinned commit:
  7cbf7a0c32fca1badf05931879a37c3f8a2b03b4

The portable backtrack.py is read-only and needs no network connection:
  python3 backtrack.py --list
  python3 backtrack.py CG6
  python3 backtrack.py LA5
  python3 backtrack.py GP5 --repo /path/to/riemann-hypothesis-lean --entry 1
  python3 backtrack.py RS8
  python3 backtrack.py RK3
  python3 backtrack.py --check-all --repo /path/to/riemann-hypothesis-lean

It checks the source-file hash before printing an excerpt, and displays
every version-update field through version_0_7_update. Its default excerpt
cap is 160 lines; use --max-lines to change it. The archive omits the
enormous source repository and build caches. Component TeX files are
inclusion fragments. Component regeneration scripts record this workspace's
workflow; backtrack.py is the portable source-inspection entry point.

PRECISION THAT MATTERS
CG uses Frobenius only on canonical prime-field path coefficients, then
extends linearly; it assumes no inverse Frobenius on the residue field.
LA retains the actual periodic representative x-n' in the wrap.
GP counts under AdmLL and proves membership under the additional BOK
conditions; its independence proof retains the auxiliary monomial U.
The direct Weyl error constant 6 improves an intermediate bound only;
the source threshold 1088 and all downstream constants remain unchanged.
The theorem proved in RK is for supplied data, not a parameter-existence
theorem. The complete constraints are in continuation_checkpoint.json.

REMAINING LOCAL WORK
Connect the supplied-data Type-II results to the actual compatible frame,
chain, degree, size and simultaneous large-constant construction. Start
with PathPairCorrespondence and trace the hypotheses through CloudStep.
The concrete implementation targets and pinned ranges are recorded in
next_source_targets.json. In particular, retain the stronger FramesOK
segment-span and L2-gap bounds supplied by frames_of.
Reconstruct the separate Type-I r=1 family and its averaged exceptional
bound. Selected-symbol density, incoming membership, primitive selection,
normal degree and complementary count are completed inputs.

REMAINING GLOBAL WORK
Actual theta/common-image identities and chain norms; archimedean spectral
and arithmetic kernel estimates; dimension/metric/discarded-target bounds;
congruence denominators and ordinary/fixed-character cohomological windows;
simultaneous prime selection and the uniform centered-prime-sum estimate.

VERIFICATION LIMITS
No Lean source was modified, and no full Lean build or independent kernel
replay was run for this reconstruction. The shorter human arguments have
not been formalized and replayed in Lean. Source-reading provenance and
independent mathematical reviews are recorded as such. The final PDF hash
must match the all-pages visual-review record before this script packages it.

CONTINUATION
continuation_checkpoint.json records completed claims, exact assumptions,
reviews and next targets. SHA256SUMS covers every bundled file except itself.
ZIP CRCs and every archived byte are checked against the completed folder.
