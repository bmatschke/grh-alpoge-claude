# A human-readable reconstruction of RH and Dirichlet GRH

**Six obligations remain. All six are shared by RH and unrestricted Dirichlet GRH.** The aim is to explain the pinned Alpöge–Claude formal argument in ordinary mathematical language, using established theorems where their hypotheses and normalizations agree. The human proof is incomplete. [Proof idea](PROOF_IDEA.md) · [Mathematical guide](MATHEMATICAL_GUIDE.md) · [Verified obligation inventory](SELECTED_FAMILY_CHECKPOINT.json)

**Next proof target.** Construct the normalized vacuum and the two finite test functions on the original self-dual lattices at every allowed twist. On a step already carrying these data, [the real discrete-series pair](THETA_INTERIOR_DISCRETE_SERIES.md), [vanishing of all proper constant terms](THETA_INTERIOR_CUSPIDALITY.md) and [factorization of the integral on smooth vectors](THETA_CUSPIDAL_FACTORIZATION.md) now prove both interior arrows of the tower. The [reference kernel](THETA_REFERENCE_WEIL.md) and [reference integral](THETA_REFERENCE_LIFT.md) also retain their normalizations under extension of coefficients. The [active roadmap](NEXT_STEPS.md) gives the next calculation for each obligation.

| Work still open | Mathematical question |
|---|---|
| Base theta readings | Do the geometric and automorphic descriptions give the specified theta map at both levels? |
| Rational tests for theta | Can forms and their theta images be tested over the prescribed coefficient field for every required tuple? |
| Common family existence | Can one construct compatible members at the arbitrarily large scales needed for the prime-sum bound? |
| Periods and heights | Do the arithmetic period maps have the required integral and archimedean bounds, with one common row comparison? |
| Loss of retained dimension | How small is the fraction of the row space discarded on the chosen family? |
| Spectral estimates | Do the diagonal and mixed period operators satisfy their bounds with the required rates and uniformity? |

For the loss of dimension, [Weil’s representation-density formula and a second-moment bound](RETAINED_DIMENSION_COMPARISON.md) identify a classical input and a sufficient estimate on the actual row multiplicities. The [reciprocity proof](COMMON_DESIGN_EXISTENCE.md) constructs the required datum on every prescribed good point. The [period comparison](PERIOD_COMPARISON_STEP.md) combines denominators and archimedean norms into a scalar-invariant height.

**Most recent whole obligations closed.** The chosen family retains its integral Hecke specialization. Its next theta lift uses the same columns, real realization and coefficient field. Its base rows have the prescribed eigenspaces and bases. These are assertions about every member of the family. Existence of sufficiently large members is the third open question above. [Selected-family proof](LOCAL_SELECTED_FAMILY.md) · [Base-row proof](SELECTED_BASE_ROWS.md) · [Collected proofs (PDF)](SELECTED_FAMILY_SUPPLEMENT.pdf)

## Reading and verification

- For the route from divisibility of theta lifts to a prime-sum bound, start with the [proof idea](PROOF_IDEA.md) and [Alpöge’s remark with references](ALPOGE_REMARK_GUIDE.md).
- For the individual arithmetic results, read the [split-prime base-change argument](LOCAL_BASE_CHANGE_BLOCKS.md), the [residual Galois comparison](LOCAL_RESIDUAL_REPRESENTATIONS.md) and the [local specialization supplement](LOCAL_SPECIALIZATION_SUPPLEMENT.pdf).
- For the large numbered manuscript, use [edition 0.90](RH_readable_reconstruction_v0_90.tex) and its [period comparison guide](RH_reconstruction_progress_v0_90.md). The [earlier reading index](history/github_reading_guide_before_current_roadmap.md) preserves the edition-specific navigation and reproduction instructions.
- Run `python3 verify_selected_family.py` at the repository root to check the six open leaves against both endpoints of the 121-node dependency graph. It also checks that the roadmap lists precisely those obligations. The project accepts the [pinned formal proof](https://github.com/CocoSgt/riemann-hypothesis-lean/tree/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4) as its starting point.

`main` is the working record. A proof update belongs with its evidence, the resulting next action in the [roadmap](NEXT_STEPS.md), and any change in the [whole-obligation inventory](SELECTED_FAMILY_CHECKPOINT.json). Historical numbered editions describe the state at their release.
