# A human-readable reconstruction of RH and Dirichlet GRH

**Six obligations remain. All six are shared by RH and unrestricted Dirichlet GRH.** The aim is to explain the pinned Alpöge–Claude formal argument in ordinary mathematical language, using established theorems where their hypotheses and normalizations agree. The human proof is incomplete. [Proof idea](PROOF_IDEA.md) · [Mathematical guide](MATHEMATICAL_GUIDE.md) · [Verified obligation inventory](SELECTED_FAMILY_CHECKPOINT.json)

**Next proof target.** At an interior step of the original theta tower, identify one archimedean intertwiner that works before the finite twists are chosen. On the enlarged coefficient field, the [reference Weil kernel](THETA_REFERENCE_WEIL.md) now has the prescribed characters, vacuum and polynomial normalization. The [reference theta lift](THETA_REFERENCE_LIFT.md) identifies the integral, its multiplicity vector and its rational coordinates. Both results start with an existing realization of the original row. The [active roadmap](NEXT_STEPS.md) gives the construction still needed and the completion criterion for each open obligation.

| Work still open | Mathematical question |
|---|---|
| Base theta readings | Do the geometric and automorphic descriptions give the specified theta map at both levels? |
| Rational tests for theta | Can forms and their theta images be tested over the prescribed coefficient field for every required tuple? |
| Common family existence | Can one construct compatible members at the arbitrarily large scales needed for the prime-sum bound? |
| Periods and heights | Do the arithmetic period maps have the required integral and archimedean bounds, with one common row comparison? |
| Loss of retained dimension | How small is the fraction of the row space discarded on the chosen family? |
| Spectral estimates | Do the diagonal and mixed period operators satisfy their bounds with the required rates and uniformity? |

**Two other advances.** For every prescribed good point, complex multiplication and class field theory supply the required reciprocity datum before the bundle size is chosen. For the mean-slope argument, the finite denominators and archimedean norms of a period can be combined into one scalar-invariant height. [Reciprocity on a good point](COMMON_DESIGN_EXISTENCE.md) · [Projective height of a period](PERIOD_COMPARISON_STEP.md)

**Most recent whole obligations closed.** The chosen family retains its integral Hecke specialization. Its next theta lift uses the same columns, real realization and coefficient field. Its base rows have the prescribed eigenspaces and bases. These are assertions about every member of the family. Existence of sufficiently large members is the third open question above. [Selected-family proof](LOCAL_SELECTED_FAMILY.md) · [Base-row proof](SELECTED_BASE_ROWS.md) · [Collected proofs (PDF)](SELECTED_FAMILY_SUPPLEMENT.pdf)

## Reading and verification

- For the route from divisibility of theta lifts to a prime-sum bound, start with the [proof idea](PROOF_IDEA.md) and [Alpöge’s remark with references](ALPOGE_REMARK_GUIDE.md).
- For the individual arithmetic results, read the [split-prime base-change argument](LOCAL_BASE_CHANGE_BLOCKS.md), the [residual Galois comparison](LOCAL_RESIDUAL_REPRESENTATIONS.md) and the [local specialization supplement](LOCAL_SPECIALIZATION_SUPPLEMENT.pdf).
- For the large numbered manuscript, use [edition 0.90](RH_readable_reconstruction_v0_90.tex) and its [period comparison guide](RH_reconstruction_progress_v0_90.md). The [earlier reading index](history/github_reading_guide_before_current_roadmap.md) preserves the edition-specific navigation and reproduction instructions.
- Run `python3 verify_selected_family.py` at the repository root to check the six open leaves against both endpoints of the 121-node dependency graph. It also checks that the roadmap lists precisely those obligations. The project accepts the [pinned formal proof](https://github.com/CocoSgt/riemann-hypothesis-lean/tree/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4) as its starting point.

`main` is the working record. A proof update belongs with its evidence, the resulting next action in the [roadmap](NEXT_STEPS.md), and any change in the [whole-obligation inventory](SELECTED_FAMILY_CHECKPOINT.json). Historical numbered editions describe the state at their release.
