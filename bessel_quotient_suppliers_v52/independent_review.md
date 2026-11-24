# Independent mathematical review: BQS1–BQS23

**Verdict: PASS.** No unresolved mathematical, quantifier, source-binding, or endpoint-scope defect was found.

Reviewer: `/root/geometry_alltest`, independently of the author `/root/bessel_nonvanishing`.
Date: 23 November 2026.

Proof: `bessel_quotient_suppliers_v52/main.tex`.
Full SHA256: `e9707407e3ce6f22a073d8195eff756c5584a6ccc06347605ff3e3f59c6035d1`.
Accepted formal source pin: `7cbf7a0c32fca1badf05931879a37c3f8a2b03b4`.

## Mathematical findings

The manuscript proves the complete original standard and dual quotient suppliers. It does so for arbitrary tuples in the original Euler eigenspaces, including the exact source and target quantifiers. Joining these suppliers to the already reviewed evaluation and transport packets proves both one-weight directions and the original endomorphism-valued Bessel nonvanishing statement. The setting consequence retains the given `Forms0` datum.

I read all 23 human proofs and compared their scopes with the original definitions and intermediate theorem interfaces. The review concentrated on the following points.

### Euler algebra, cyclic models, and trace transfer

The annihilating-polynomial proof compares polynomial coefficients and uses a recursive identity; it does not substitute an operator into noncommuting coefficients. The standard and dual triangular flags give the full Verma product statement without distinct-root or integrality assumptions. Strict decrease enters only where eigenvalue separation and the extremal line require it.

The principal-minor model is holomorphic on the actual inverse-minor domain and is zero outside that domain. The manuscript does not assume differentiability across its boundary. The compact integral transfer preserves the exact derivative order, conjugation, coefficient functional, and Haar normalization. For the trace-kernel implication, each vector lies in a finite compact-stable word-degree cutoff even when the whole formal subspace is infinite dimensional. The compact matrix factor is inverted before the transfer theorem is applied.

In BQS10, the diagonal correction is sufficient to compute the weights after compact lowering words. The argument does not presume that the model map intertwines the off-diagonal compact action. Cone failure forces the image to vanish on the entire compact PBW span. At the extremal weight, a nonempty lowering word has positive root height, so the same full span argument proves the line bound. These steps match the original abstract theorem's arbitrary target operator family.

### Incomplete targets and the exact gap

BQS14 compares the given compact type with its actual discrete-series model by taking their diagonal copy in a direct sum. The diagonal copy need not have scalar Casimir at the outset. This causes no circularity: DC9's finite-layer argument requires the negative first-layer relation and the stated gap, and these hold coordinatewise. The positive compact-Casimir increment excludes another copy of the original compact type. Applying the central Casimir to its resulting unique highest line then compares the two coordinate scalars.

The numerical hypotheses are preserved: `hNeed < b + 2` implies the three model thresholds, and the candidate parameter in BQS15 loses exactly two gap units. The partial-sum bounds give integral coordinate changes in the interval from minus one to one. Strict decrease follows separately for adjacent equal-sign and opposite-sign entries. No enlarged gap is introduced.

The K3 construction selects a compact highest weight of minimum nonnegative root height under its fixed partial-sum upper bound. Any nonzero negative first-layer image would give a smaller admissible height. The tensor Casimir identity and the positive-root norm identity then force the required shifted lowest weight. All orthogonal complements used here are finite dimensional. Neither completeness nor an actual noncompact group action is imposed on the target.

### Closure, smoothness, and the original quotient

BQS18 proves closure invariance using the actual orbit Taylor estimate and compact logarithms. Its compact-finite conclusion uses the original weaker `StdGap`, with no additional integrality or coefficient identity. The finite layer bound survives completion through the actual bounded compact character projector.

BQS19 and BQS20 retain arbitrary source operators. The first does not assume source stability, `X` contained in `G`, or the chosen lowest type contained in the image. The second adds exactly the stated inclusion, finite compact hulls, stable kernel, and saturation condition. The only infinite-dimensional orthogonal projection occurs in the complete actual `L2` space. The source complement remains an algebraic choice.

The smooth lift is constructed on the original generated subspace from actual square-integrable functions and then extended algebraically. All derivative words are controlled by the inherited estimates. The simultaneous period kernel is invariant under the exact tensor action. Equality of smooth `L2` classes gives equality at every group point by Haar full support; the original weak Haar supports then give equality of the original period integrands. The character, Haar pair, Cayley matrix, vectors, and free translate are unchanged.

I compared all six conclusions in BQS22 with `PsiDatumStatement.lean`: actual function image, both directions of the smooth `L2` image equivalence, compact irreducible highest weight, shifted Casimir, actual compact-group stability, and pointwise injectivity of the prescribed periods. Both signs match. The conclusion is not restricted to complementary-minor tuples.

## Claim coverage

| Claims | Reviewed conclusion |
|---|---|
| BQS1–BQS3 | Tensor generation, both Euler products, and selected projectors |
| BQS4–BQS5 | Full cyclic Verma product, both weight cones, and extremal lines |
| BQS6–BQS9 | Actual principal-minor model, compact integral transfer, and full trace-kernel implication |
| BQS10–BQS13 | Abstract cone transfer, both original K2 statements, and one line witness before every target |
| BQS14–BQS17 | Incomplete-target Schmid–Casimir comparison and both original K3 image theorems |
| BQS18–BQS20 | Original closure/compact-finite results and both arbitrary-source quotient lemmas |
| BQS21–BQS22 | Full smooth lift, fixed-data period kernel, and all six outputs of both original quotients |
| BQS23 | Full one-weight propagation and literal Bessel nonvanishing; setting on supplied `Forms0` scope |

The companion JSON records a separate reasoning assessment and the exact proof and source hashes for every claim.

## Independent binding checks

The frozen main file and all 23 numbered blocks were hashed independently. All 55 source snapshots, totaling 438,090 bytes, were compared byte for byte with `git show` at the accepted pin. All 66 distinct referenced line ranges were hashed independently, and all 31 inherited human-proof block bindings were checked against their actual files. Every binding passed.

No author proof or author metadata was modified by this review. No Lean replay was performed; formal correctness was accepted as instructed. This review evaluates the readable mathematical reconstruction and its exact original scope.

## Retained boundaries

`BesselNVGap`, `StepStatement`, `QuotPStatement`, and `QuotMStatement` have no remaining supplier premise in this packet after the stated inherited results are joined. `ConcreteSettingExists` remains a consequence for a supplied original `Forms0` datum. The ambient form producer, orbital/fiber and Siegel–Weil comparisons, local uniqueness, and downstream global spectral identifications remain separate. No whole selected `GLOBAL_SPECTRAL` obligation, unrestricted RH endpoint, or unrestricted Dirichlet-GRH endpoint is declared closed.
