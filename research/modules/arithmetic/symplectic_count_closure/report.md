# SP1–SP10: complete algebra suppliers and the paired-count join

## Completed milestone

This component closes the literal **LemmaM′** and **LemmaM** as complete human-readable algebraic chains. It also closes the actual `shaCoc` and `mPrime` comparison on a supplied `Model D`, proves exact return from an auxiliary coefficient DVR to the original character, and proves the arithmetic join from a precisely stated finite trace catalogue and actual model geometry to the literal `CountII ∧ CountIII` conclusion.

**CountII and CountIII remain conditional.** The model must still be constructed on the actual arithmetic datum, its required geometric and representation-theoretic properties must still be proved, and the uniform finite automorphic catalogue must still be supplied. The full readable proof distinguishes these obligations from the completed universal algebraic theorems.

The source is pinned at `7cbf7a0c32fca1badf05931879a37c3f8a2b03b4` in the CocoSgt/riemann-hypothesis-lean repository. No Lean kernel replay was attempted. Formal verification remains the project's accepted background; this work supplies and checks the mathematical reconstruction.

## Stable claim inventory

| Claim | Endpoint | Remaining bespoke input |
|---|---|---|
| SP1 | Literal `UpperTheory.V.Alg.LemmaM'` | None |
| SP2 | Multigraded Euler positivity, quotient monotonicity, product formula and scalar lower bound | None |
| SP3 | Rees support, one-sided point exclusion, generic support and admissibility | None beyond the explicit M1–M5 theorem hypotheses |
| SP4 | Finite cover by two-sided orbits; generic graded multiplicity at most one | None beyond explicit M2/M4 |
| SP5 | Leading-form lattice count and exact lower Euler factor | None beyond the explicit algebraic hypotheses |
| SP6 | Literal `UpperTheory.V.Alg.LemmaM`, including every finite two-sided cover and factor two | None |
| SP7 | Actual `shaCoc` and `mPrime` on original Good D and actual Model D | Model existence is not asserted; the implication itself is proved using RV3 |
| SP8 | Character order/kernel/conductor/case invariants and normalized coefficient return | None; uses RV1 |
| SP9 | Literal `NumberSp4Alt` from the exact uniform finite catalogue | Catalogue existence and classification |
| SP10 | Literal `CountII ∧ CountIII` on original coefficients | G1 actual data/admissible-class production; G2 actual Model and point/orbit comparison; SP9 catalogue |

Each source-backed endpoint has exact declaration ranges, first lines, file hashes and range hashes in `provenance.json`. The ledger has **153 claim-source links and 37 retained-frontier links across 85 source files**. Every source file is checked against its pinned Git blob.

## Why LemmaM is now a complete chain

The proof starts with the literal source data: a complete coefficient DVR, a finite-type integer-graded algebra over its complete local degree-zero part, generators in weights ±1 and ±2, the original augmentation, the saturated cotangent modules, and the exact five M1–M5 conditions. The valuation is the source's normalized extension to the fixed algebraically closed field. No extra finite-residue assumption is imposed on LemmaM; finite residue is used exactly where LemmaM′ requires it.

The Euler engine is proved from finite homogeneous prime filtrations. In particular, eventual nonnegativity is not assumed as an unexplained intersection-theory input. The zero-section case is replaced by a nonzero section of the same multidegree, reducing it to an exact multiplication sequence. Product-of-sections identities then extract the Smith exponents one at a time.

The three-variable Rees algebra records negative degree two, positive degree two, and the additional saturated-square equation. The support argument proves that its relevant generic support is exactly restricted to two-sided points. Both one-sided points are constructed from a single symmetric prime-testing ideal. The relevant field algebra is a nonzero finite-type algebra before extending the field; the proof never applies the Nullstellensatz to an arbitrary transcendental prime residue field.

A useful simplification gives the upper multiplicity. Normalize a nonzero negative degree-two function to one. The tangent condition makes this slice finite étale. Adjoining a square root of the original degree-two function identifies the localized algebra with that slice times a one-dimensional torus. Reducedness follows by faithful flatness, and each localized graded component has dimension at most one. Squaring the required equations costs exactly `2^(r+1+r′)`.

For the lower bound, eliminate the zero-weight equations by a recursive formal change of coordinates. The leading-form quotient is a finite free lattice whose rank is counted by monomials of prescribed positive and negative weights. Its explicit generating-function difference is `2^(r−1+r′)`. The scalar-product Euler formula contributes `2 Σ c_i`, giving the lower bound `2^(r+r′) cotLen`.

Finally, the one-element Euler characteristic is evaluated directly by determinant and field norms. The lower factor `2^(r+r′)` and upper factor `2^(r+1+r′)` cancel to leave the exact factor **2**. A cover must consist entirely of two-sided points, as in the source: this matters because the source valuation imposes no value at zero. Extra representatives of the same orbit are harmless because all summands are nonnegative.

The argument does not depend on an automorphy, rigidity, catalogue, RH or GRH statement. Its actual arithmetic use still needs verification of M1–M5 on the original model; that is a separate obligation, not part of the universal algebraic theorem.

## Two additional completed interfaces

SP7 constructs the source's precise normalized cocycle family. RV3 gives finite length of the original strict Selmer module. Normalizing at the source's fixed residual-nontrivial element makes the cocycle representative canonical and additive. One common scalar kills both all cocycle values and all finitely many actual local coboundary parameters. The prime-to-ℓ inertia argument proves exactly `UnrT` on every original valuation subring.

On the actual Model, derivative lifts are not presumed additive. Their differences descend to the representation ring. Square-zero algebra maps and the model's generation property force those differences to vanish modulo the common scalar. The `(2,0)` matrix entry recovers the original cocycle, giving the additive injection required by SP1. The augmentation's descent through the model quotient is proved explicitly from `at0`.

SP8 returns a bound to the original coefficient ring with no loss. Injectivity preserves character order, the unit kernel, conductor, primary projections, parity and both cases. It preserves the two logarithmic parameters used to choose auxiliary roots. RV1 supplies exact base change of the strict local kernel: module lengths and `v_O(ℓ)` are multiplied by the same ramification index. Their ratio and the prior uniform exponent are unchanged.

## What the count arithmetic proves, and what it does not

SP9 assumes the full finite trace catalogue with its required uniformity, integrality, complex-conjugation action, trace bound and representation classification. It then proves everything needed to form the integer product: nonvanishing, integrality, rationality, the logarithmic bound, injectivity of the selected factors, and the ℓ-adic product inequality. The integer is chosen before ℓ, the original algebraic closure, the complex embedding, and the representation family. The geometric-versus-arithmetic Frobenius inverse convention is explicit.

SP10 uses the actual trace element and exact point/orbit comparison to join SP6 and SP7 to the source's `D.Ineq`. It proves the original strict Selmer group injects into `D.Sha`, including any extra primes in D.S; this is the inequality named `shaEq`, not an equality. A direct unramified-cohomology computation handles those extra primes. The finite character times a strictly negative cyclotomic twist has Frobenius eigenvalue different from one, so the unramified quotient is zero.

The last numerical step gives an explicit generous exponent depending only on the fixed primitive character and the catalogue's two constants. It is selected before the host, coefficient ring and character. SP8 then returns the result to the original coefficients. There is no omitted parameter-dependent constant in that arithmetic join.

The outstanding input registry records G1, G2 and the catalogue as actual propositions, not generic labels. Its source locators include `dataEx`, `levOf`, `level`, `safe4'`, `exModel`, `aW`, `aSmooth`, `m1b`, `m2`, `m3`, `m4`, `ptLift`, `ptScale`, `twoIrr`, `conjTorus`, `ptAct`, `ptExt`, `CountQAlt`, `countQ_alt`, `EigData` and `EigData.Classifies`.

At the larger source-interface level, the remaining work includes image density, the full cohomology package, actual installation of the weighted presentation theorem, the automorphic catalogue and symplectic rigidity. The separate framed-deformation component now supplies the universal LemmaP implication as FP8; its proof does not itself verify its hypotheses on the actual Galois functor. RV3/RV7 already supply SoFin/SoV and BR7 supplies CorX, with their original quantifiers.

## Validation and review

- Main TeX SHA256: `be6f26510549b7b3879e5a65f46c00b5ab0108909550340ed2342f57d0827c92`.
- Provenance SHA256: `ca23ed4861e3212b2fc2edff0bf7dd0af54e6e3a7966d1e038a088d840308f44`.
- Source bytes: all 85 files match the pinned Git commit.
- TeX: two successful draft-mode passes using the cumulative preamble; no undefined references, missing characters or overfull boxes; no PDF generated.
- Root and both other agents independently read SP1–SP6. Their identified scope/finite-type precision corrections have been incorporated. Hash-bound PASS records are present in the shared v0.26 review directory.
- Root independently reviewed all ten frozen SP claims, including the actual cocycle/model comparison and the full arithmetic join. The cumulative release ledger determines the final review status and incoming component hashes.
- This component's author independently reviewed FP1–FP8 and verified all 99 source links, 36 pinned files and eight human-proof ranges. The final PASS review is bound to FP main SHA256 `3079ea88a360e4efd6e4625479ff4d5cd52dc42472a933eff74c44def4699cd8` and provenance SHA256 `c39863cc6055ccdb1a3cf7e94b768676507f6f722faa615330ac901fb5bfa96a`.

The validation scripts check exact bytes and TeX syntax. Mathematical certification rests on the written proof and the independent reviews; the scripts do not claim to perform it.
