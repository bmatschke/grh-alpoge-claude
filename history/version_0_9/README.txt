RH AND DIRICHLET-GRH READABLE RECONSTRUCTION — VERSION 0.9
21 November 2026

START HERE
RH_readable_reconstruction_v0_9.pdf is the cumulative 93-page main note.
RH_readable_reconstruction_v0_9.tex is its self-contained LaTeX source.

This is a partial human reconstruction, not a self-contained RH or GRH
proof. GRH here concerns Dirichlet L-functions. It does not assert all
automorphic or Dedekind GRH. The completed local Type-II theorem from
v0.8 remains unchanged under its literal hypotheses, with C>=4129.

WHAT IS NEW
GG: the actual graded Gram lattice, its integral image lifting and exact
determinant bound. The proof uses an explicit integral auxiliary action
and does not import integral semisimplicity as a missing premise.
TP: sharper exact gamma integrality, compatible integral partners for
all ties, continuation multiplicities and their endpoint injection.
The source's literal TheoremMV7 is proved with CM=1.
SW: actual level saturation, an explicit harmonic change of basis,
its exact Fock normalization, ramified good block lattices, and a
terminal-window proof reusing TI5. The finite weighted sum retains the
actual coarse rank inequality rather than assuming density follows.
SW12: literal Std supplies kept-block legality, oPlus<=147a/250<=aPlus,
and total order<=t0 for Ct>=30.
RL: actual paired lifts into CCe and CCe', at height floor(t0), with
scalar valuation<=4kappa0. The factorial correction, raw generators,
reblocking and finite cleanup are explicit. ColNum, Room and NumCore
are derived from Std. The cleanup has no accumulated height penalty.

The new section starts are:
  GG 53, TP 55, SW 58,
  SW12 62, RL 64.
Some sections share a physical page. The starts are detected in the
final rendered PDF from the exact live section titles.

READING ORDER
For this iteration's endpoint, read RL and its closing scope paragraph,
then GG, TP and SW. TI3–TI5 are the earlier polynomial mechanism.
The expanded reports are in graded_gram/, tie_partners/,
segment_weighted/, segment_numerics/ and paired_lifts/.
For the global implication, begin with the analytic endpoint, scalar
balance and frame/slope sections. Ordinary RH and the general fixed
Dirichlet-character case have separate host/window sections.

REMAINING LOCAL WORK
Prove the upper and lower coarse rank-on-digits bounds. The upper bound
supplies SW8.1; the lower bound supplies retained mass for Type-I density.
Then identify the actual harmonic dimensions and KeyIneq interface,
supply the full numerical parameter package with its quantifier order,
and compare the constructed t0 height with the final shifted tI bound.
Only after those inputs match may TI7–TI8 be used for the full Type-I
exceptional-function result. The new next_source_targets.json provides
25 exact declaration ranges for that work.

The global theta/spectral, metric, cohomological-window and simultaneous
prime-selection branches remain as stated in the main note. A proof
under literal local Std is not a proof that all global choices exist.

PROVENANCE AND BACKTRACKING
provenance.json has 315 stable claims, 4579
exact source links and 764 primary source files.
provenance.txt is the readable ledger; source_index.json indexes files.
All earlier claim fields/source arrays and source-file records remain
verbatim. Current version_0_9_update fields state which old inputs are
now discharged. Older component reports retain their historical scope.
Superseded root files, including the previous PDF/TeX and target list,
are archived under history/version_0_8/.

Pinned repository: https://github.com/CocoSgt/riemann-hypothesis-lean
Pinned commit: 7cbf7a0c32fca1badf05931879a37c3f8a2b03b4

Portable read-only lookup:
  python3 backtrack.py --list
  python3 backtrack.py GG7
  python3 backtrack.py TP11
  python3 backtrack.py SW8
  python3 backtrack.py RL11 --repo /path/to/riemann-hypothesis-lean --entry 1
  python3 backtrack.py TI9
  python3 backtrack.py --check-all --repo /path/to/riemann-hypothesis-lean

With --repo, source-file SHA256 is checked before any excerpt is shown;
the selected inclusive-range SHA256 is checked as well. Default excerpts
are capped at160 lines; --max-lines changes that. The tool displays
version updates, exact proof locations and dependencies. No network is
needed if the pinned source is available locally.

The archive omits the huge source checkout and build caches. The
workflow_v0_9/ scripts record this workspace's assembly and checks;
backtrack.py is the portable reader utility. Expanded reports contain
longer proofs and source correspondence, not silently additional axioms.

PRECISION AND REVIEW
GG includes a z-degree-zero projection before its reduced highest
projector. SW1 treats each prefix kernel separately. SW3 retains the
additive factorial bound and the ramified w^q scaling. TP's multiplicity
weights are not dropped, and its partial inverses need not commute.
RL keeps fixed physical factorials and the multiplicative beHH=p^AHH
normalization. Its SSg is the span of generators of bounded actual
order; cleanup uses each generator's actual order, then the common bound.
The odd-power excluded band is an explicit Std hypothesis.

The mathematical peer-review records are in reviews_v0_9/. The main PDF
has been rendered and every page visually reviewed. No Lean source was
modified and no full Lean compilation or independent kernel replay was
run for this human reconstruction. Hash checks and mathematical reviews
are not presented as such a replay.

CONTINUATION AND INTEGRITY
continuation_checkpoint.json preserves earlier results and precision
constraints, records exact supersessions, and names the current inputs.
visual_qa.json identifies the exact reviewed PDF by SHA256.
SHA256SUMS covers every bundled file except itself. ZIP membership,
each CRC and every archived byte are checked against the final folder.
Every predecessor file is preserved either at its old component path
or in history/version_0_8/.
