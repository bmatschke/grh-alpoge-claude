# A human-readable reconstruction of RH and Dirichlet GRH

**Six obligations remain. All six are shared by RH and unrestricted Dirichlet GRH.** The aim is to explain the pinned Alpöge–Claude formal argument in ordinary mathematical language, using established theorems where their hypotheses and normalizations agree. The human proof is incomplete. [Proof idea](PROOF_IDEA.md) · [Mathematical guide](MATHEMATICAL_GUIDE.md) · [Verified obligation inventory](SELECTED_FAMILY_CHECKPOINT.json)

**The first auxiliary column can now be constructed.** Its [small coefficient field and frame](FIRST_PASS_FIELDS.md) are fixed before the two successive field requests. The [mass estimate in item 9 of Alpöge’s remark](FIRST_PASS_COLUMN.md) gives one range for the weights of every word. On each resulting pinned column, once the specified group and volume identifications hold, the [geometric and automorphic constructions give both theta readings and rational tests at both levels](THETA_PINNED_COLUMNS.md). The [field-extension proof](THETA_FINE_EXTENSION.md) preserves a specified old datum that satisfies the lower-row laws, including its reference lattices and phase. A [common finite-level vector](LOWER_ROW_MARKED_TYPE.md) now supplies the marked type for the next family calculation, a trace comparison of cuspidal multiplicities on two unitary groups with different real data. [Active roadmap](NEXT_STEPS.md)

| Work still open | Mathematical question |
|---|---|
| Base theta readings | Can the two readings constructed on the starting column be carried through retwisting to the prescribed family? |
| Rational tests for theta | Can the tests at both levels be retained on the actual columns exported at each required size? |
| Common family existence | Can one construct compatible members at the arbitrarily large scales needed for the prime-sum bound? |
| Periods and heights | Do the arithmetic period maps have the required integral and archimedean bounds, with one common row comparison? |
| Loss of retained dimension | How small is the fraction of the row space discarded on the chosen family? |
| Spectral estimates | Do the diagonal and mixed period operators satisfy their bounds with the required rates and uniformity? |

For the loss of dimension, [the near-term argument](RETAINED_NEAR_TERMS.md) confines nonidentity rational elements to a small explicit cusp and proves the required decay of the flag constants. The trace still counts elements with multiplicity there. The [second-moment comparison](RETAINED_DIMENSION_COMPARISON.md) gives an alternative sufficient bound. The [reciprocity proof](COMMON_DESIGN_EXISTENCE.md) constructs the required datum on every prescribed good point. The [period comparison](PERIOD_COMPARISON_STEP.md) combines denominators and archimedean norms into a scalar-invariant height.

**Most recent whole obligations closed.** The chosen family retains its integral Hecke specialization. Its next theta lift uses the same columns, real realization and coefficient field. Its base rows have the prescribed eigenspaces and bases. These are assertions about every member of the family. Existence of sufficiently large members is the third open question above. [Selected-family proof](LOCAL_SELECTED_FAMILY.md) · [Base-row proof](SELECTED_BASE_ROWS.md) · [Collected proofs (PDF)](SELECTED_FAMILY_SUPPLEMENT.pdf)

## Reading and verification

- For the route from divisibility of theta lifts to a prime-sum bound, start with the [proof idea](PROOF_IDEA.md) and [Alpöge’s remark with references](ALPOGE_REMARK_GUIDE.md).
- For the individual arithmetic results, read the [split-prime base-change argument](LOCAL_BASE_CHANGE_BLOCKS.md), the [residual Galois comparison](LOCAL_RESIDUAL_REPRESENTATIONS.md) and the [local specialization supplement](LOCAL_SPECIALIZATION_SUPPLEMENT.pdf).
- For the large numbered manuscript, use [edition 0.90](RH_readable_reconstruction_v0_90.tex) and its [period comparison guide](RH_reconstruction_progress_v0_90.md). The [earlier reading index](history/github_reading_guide_before_current_roadmap.md) preserves the edition-specific navigation and reproduction instructions.
- Run `python3 verify_selected_family.py` at the repository root to check the six open leaves against both endpoints of the 121-node dependency graph. It also checks that the roadmap lists precisely those obligations. The project accepts the [pinned formal proof](https://github.com/CocoSgt/riemann-hypothesis-lean/tree/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4) as its starting point.

`main` is the working record. A proof update belongs with its evidence, the resulting next action in the [roadmap](NEXT_STEPS.md), and any change in the [whole-obligation inventory](SELECTED_FAMILY_CHECKPOINT.json). Historical numbered editions describe the state at their release.
