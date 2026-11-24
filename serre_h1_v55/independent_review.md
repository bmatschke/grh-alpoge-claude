# Independent mathematical review: SHV1–SHV21

**Result: PASS.** Reviewer: `/root/arithmetic_common_frame`. Author: `geometry_alltest`. This review is bound to `serre_h1_v55/main.tex`, SHA256 `9f7faf053020e9f02982c99f62da627b93c7b0f14f1fbec5e0d595f3907c1b46`, and accepted source commit `7cbf7a0c32fca1badf05931879a37c3f8a2b03b4`.

All 21 human proof blocks were independently read. All 31 full source snapshots were compared byte-for-byte with both the accepted Git blobs and the read-only checkout; all 71 cited ranges were independently hashed. The 11 inherited bindings were checked, including their exact proof blocks and parent provenance hashes. FCD15 is correctly classified as background whose relevant calculation is reproved, and GSL17 is a subsequent consumer rather than an upstream premise.

## Mathematical findings

The algebraic exactness argument is complete. Homogeneous localization preserves the short exact sequences by explicit numerator lifting and the fraction zero criterion. The signed Laurent-monomial contraction works over an arbitrary base ring. Its only surviving monomials have every exponent negative, so each fixed-degree cohomology is finite free and every positive-degree complex is exact. The finite free shift bound is chosen once. Over a Noetherian base, a list of nu+1 finite homogeneous kernels suffices to shift any cohomological degree past the finite augmented length. No finite global-dimension theorem or unbounded maximum is assumed.

The finite section model has the required order of choices and actual maps. The ASL dehomogenizations and FCD13 quotient argument supply finite chart modules over the original evaluation maps. FCD10 gives one finite homogeneous submodule before every twist. Its inclusion is bijective on all nonempty localized vertices, while the empty vertex is explicitly kept separate. This is sufficient for the ordinary section complex, whose degree one is augmented degree two. The all-integer section formulas retain the original line bundles, transitions and structure map.

The all-cover step is a substantive proof, not a change of terminology. SHV10 returns refined primitives to the original cover. SHV11 proves the equivalence with the literal coordinate predicate in both directions, including its chart assignment and transition factors. The affine proof uses a first exponent to extend sections and a second exponent to kill discrepancies on whole overlaps. The power unit-ideal identity then gives an explicit primitive. A finite principal refinement exists by affine quasi-compactness even when the initial cover is arbitrary. SHV14 glues corrected local primitives on that initial cover. The signs in SHV15 agree with the actual Cube.d maps; the source primitive requires the negative of the degree-zero cochain.

These arguments give the full original Serre first-cohomology supplier over every Noetherian ring, for every actual line bundle and every sufficiently large integer twist. The bound is fixed before the arbitrary test cover and cocycle. No smoothness, reducedness, integrality, field hypothesis or unproved global section base-change theorem is inserted.

The high-power polynomial result is also complete. Saturation is applied to a finite span while the ambient section module may be infinite. The separate no-common-chart-power-torsion hypothesis follows by cancellation only on the nonzero loci and then sheaf equality. Homogenization in SHV20 preserves its original arbitrary variable set and arbitrary containing submodule. For the trivial bundle, the degree-zero section one gives a single cyclic span; the degree-t homogeneous part of the resulting polynomial acts by the original section coordinates. The natural threshold precedes both t and the section, independently of the M-dependent threshold in the other Serre conjunct.

## Exact scope and remaining work

The packet supplies the original finite graded section model, uniform large-degree exactness, affine all-cover H1 vanishing, reverse cover comparison, full Serre H1 input and full high-power homogeneous-polynomial section input. Both conjuncts of the original Serre theorem are therefore supplied. In particular the formerly retained nested input GSL_SERRE is discharged.

The packet does not assert the remaining polarized base-change, multiplication geometry/pullback, torsion-invariant descent, geometric integrality, rank-one, section decomposition, growth or square-law producers. GSL17 still retains its other original hypotheses. No whole selected RH/Dirichlet-GRH obligation is closed, and the earlier ASL Perf theorem keeps its own exact vanishing antecedent.

## Per-block checks

- **SHV1:** Homogeneous lifting, localization zero criterion, injectivity and restriction compatibility prove the actual short exact sequence; arbitrary variable set and every finite vertex are retained.
- **SHV2:** The Laurent-monomial decomposition, signed contraction and finite all-negative-exponent top contribution are correct over every commutative R, including the empty variable set and zero divisors.
- **SHV3:** The one bound 1+sum of absolute shifts makes every summand positive before every cohomological degree; finite cohomology does not require R Noetherian.
- **SHV4:** Successive kernels remain graded and finite by Noetherianity; the finite recursion is chosen before the degree and asserts no finite global dimension or termination of the resolution.
- **SHV5:** The explicit lift, boundary correction and final descent prove exactness transfer, including the bottom-degree zero-term convention.
- **SHV6:** A list of nu+1 free presentations suffices for every cohomological degree because the augmented complex has length nu; one maximum precedes all twists and degrees.
- **SHV7:** Inherited FCD10 supplies one finite homogeneous K; inclusion is bijective at each nonempty localization by actual power saturation and injectivity, without a false empty-vertex claim.
- **SHV8:** The exact ASL dehomogenization and FCD13 quotient identify finite chart modules; ASL16 projectivity is used only on affine charts. One K and its actual inclusion give the original all-integer section-cube model over arbitrary R.
- **SHV9:** The original ordinary degree-one complex is augmented degree two, and nonempty-vertex bijections suffice to transport the exact Cube.d 1/Cube.d 2 relation.
- **SHV10:** The corrected primitives phi_(a,tau(k))+u_k glue on each original cover member and give the original coboundary. Arbitrary index sets and restrictions are preserved.
- **SHV11:** Both directions of the coordinate/section equivalence retain the original chart assignments, transition units and every smaller-open cocycle identity; refinement descent returns to the original cover.
- **SHV12:** Two distinct common powers are used: the first extends finitely many sections, the second kills the overlap discrepancies on entire pairwise intersections. No zero divisor is cancelled.
- **SHV13:** The power unit-ideal identity gives an explicit primitive on a finite principal cover, and quasi-compact refinement plus SHV10 handles every original affine-open cover. No Noetherian assumption is added.
- **SHV14:** Differences of local primitives glue to a cocycle on the prescribed cover; solving it corrects and glues the primitives on the arbitrary test cover, without affine-intersection or finiteness assumptions.
- **SHV15:** The original differential has u_j-u_i and x_jk-x_ik+x_ij; the required primitive is -u. Antisymmetry and sorting recover every ordered cocycle identity, including repeated indices.
- **SHV16:** Affine all-cover vanishing, exact prescribed-cover signs and cover locality prove the complete original FirstCohomologyVanishes predicate from the literal finite secCube exactness premise.
- **SHV17:** The full original Serre H1 statement holds at every Noetherian base, every actual line bundle M and all sufficiently large integer twists. Its threshold precedes every cover/cocycle, with no smoothness or global base-change premise.
- **SHV18:** Only the finite span K requires Noetherian exactness; the ambient G may be infinite. Singleton-localization compatibility and the separate common-power-torsion hypothesis give exact high-degree membership.
- **SHV19:** Graded components are killed separately, and section cancellation takes place only on the original nonzero loci; covering sheaf equality gives zero globally.
- **SHV20:** Homogenization works for arbitrary variable sets, arbitrary containing submodules and negative source degree; only finite polynomial support is used, and epsilon-surjectivity is not added.
- **SHV21:** The original trivial-bundle degree-zero section supplies one cyclic span, and the high-degree homogeneous component returns one polynomial on every original chart with the original cst map. Its natural threshold and the independent M-dependent Serre threshold have exactly the two original quantifier orders.

## Review disposition

No mathematical or scope correction was required. There are no unresolved findings. Only this review and its JSON companion were written; no author manuscript, source snapshot, contract or prior proof was modified. No Lean replay was performed.
