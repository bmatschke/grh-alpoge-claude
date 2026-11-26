# Edition 0.72 · Two arithmetic obligations closed

The manuscript now proves the marked theorem `THM_S6_S` and the original unramified-coefficient automorphy theorem `AUT_UNRAM_COEF`, relative to the classical theorems identified in the proofs. The latter produces its finite, rank-three and rank-two conclusions for the **same mark**. The count of open whole obligations falls from **12 to 10**. All ten are shared by the RH and unrestricted Dirichlet-GRH routes. [Short TeX reader](RH_new_proofs_v0_72.tex) · [Cumulative TeX manuscript](RH_readable_reconstruction_v0_72.tex)

## How the marked theorem closes

Edition 0.71 established that `HidaUAlt` implies the marked theorem. The new chapters supply the exact arithmetic hypotheses used to construct the Hida ideal. Its kernel cuts out the Hecke action on the original ordinary module. The earlier patching proof then applies both prime tests to that same ideal. On each eligible Gaussian host there is one marked element chosen before the universal ring. Every such ring has finite weight-zero part, and every allowed type-I point has the required twisted automorphy. [Hida construction and marked theorem, M72S1–3](continuation_v72/assembly.tex) · [Original marked contract, lines 17–25](https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AutomorphicArithmetic/AutomorphicVarieties/ModularityArgument/ThresholdArguments/DenseThresholdCases/ThmS6CoreS.lean#L17-L25)

| Input to the construction | What the chapter checks |
| --- | --- |
| [Local representation theory](continuation_v72/local.tex) | All 18 local fields, including the actual smooth duality map, the geometric lemma, both segment conventions, the depth-zero map and the local converse argument. |
| [Crystalline comparison](continuation_v72/crystal.tex) | The bar complex on all bounded divided-power thickenings, the integral comparison under reduction, and the source's first Hodge and tangent tests. Integration of a divided-power coordinate introduces no factorial denominators. |
| [CM and abelian schemes](continuation_v72/cm.tex) | All 11 fields, including CM reciprocity with the specified idèle convention, class-field and functional-equation constants, periods, duality and lifting over bounded divided-power bases. |
| [Global automorphy and Galois attachment](continuation_v72/aut.tex) | All 15 fields, including the exact local assertions for definite-unitary base change and the polarized Galois representation at and away from the coefficient prime. |
| [Remaining host hypotheses](continuation_v72/outer.tex) | Cohomology and its dimension bound, conjugation, the real cuspidal spectrum, cyclic descent, the newform normalization and rank-two attachment over totally real fields. |

## The original datum with unramified coefficients

The rank-three argument uses the given representation and its cyclotomic twist on the given quadratic field. The rank-two argument starts with each permitted extension of the two-dimensional corner. The marked residual trace excludes a self-twist that could make it reducible on the chosen auxiliary field. After descent to the rationals, the two Hodge jumps determine classical weight (2e+1). A possible quadratic discrepancy is corrected on the full rational Galois group. The newform is taken at its resulting conductor. These arguments supply all three fields of the original `GdEnd`. UCE19 then gives `FinA`, `AutB` and `LemW` together. [Common datum and rank-three descent](continuation_v72/datum.tex) · [Rank-two newform](continuation_v72/corner.tex) · [Joint conclusion](continuation_v72/return.tex)

## What this establishes on the route to RH and GRH

The marked theorem supplies the remaining input to the guarded Case V estimate. Unramified-coefficient automorphy supplies the remaining input to the one-character bound and the Case I count. With the previously reconstructed Case II and Case III arguments, this gives the cohomological window `VWinAt(χ,401)` and the requested arithmetic host on each selected route. The register records these consequences separately from the two whole obligations. [Case V](continuation_v72/assembly.tex) · [Counts, windows and hosts](continuation_v72/return.tex)

The ten open obligations concern the compatible design and two selection constructions, the theta readings, rational tests and base row identity, and the four global denominator, period-height, defect and spectral estimates. A concrete next target is the rational-test family on the selected theta bundle. It must separate the image and take values in the same embedded field on both the rational inputs and the stored target basis. [Remaining original contracts](continuation_v72/obligations.json)

## Verification

The 49 new indexed claims bring the cumulative total to 4,113. The checker verifies the original source excerpts, manuscript and review bytes, dependency graph and the prerequisites of each newly installed arithmetic consequence. Mathematical verification uses the written arguments and the cited classical results. The source check does not compile the upstream Lean project. [Claim ledger](continuation_v72/claims.json) · [Typesetting and validation](continuation_v72/validation.json) · [Checkpoint](CURRENT_CHECKPOINT_v0_72.json)

~~~sh
python3 continuation_v72/verify.py --formal-git formal_source
pdflatex RH_new_proofs_v0_72.tex
pdflatex RH_new_proofs_v0_72.tex
~~~
