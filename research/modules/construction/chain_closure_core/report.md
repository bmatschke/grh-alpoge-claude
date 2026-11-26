# Closed coefficient-representation chain (v0.23)

## Result

HP1–HP6 close the characteristic-zero canonical polynomial representation input retained in v0.22. The endpoint is the literal `GlobalTheory.HeightCounting.FormsStep.wt_weights`, on the original coefficient fields, both sides, every used row and every prescribed coefficient extension, with the source's bound `c2 = bottom`. The same construction removes the two retained classification/duality premises from AR13 and hence from the representation branch of AR14's `CellWt` comparison.

This is an actual frontier reduction. It is not another record-assembly lemma: the previously unexpanded irreducibility, highest-vector and classification theorems now have a complete elementary proof in the manuscript.

## Main simplification

The source module `dualWeyl` consists of polynomials in a matrix X, with prescribed column multidegrees and invariance under upper unitriangular column operations. Its actual representation is `rho(g)f(X) = det(g)^d f(g^t X)`.

If a polynomial is additionally fixed by this upper-unipotent representation action, it is invariant under lower unitriangular row operations. Gaussian elimination X = L D U therefore forces

    f(X) = f(1) product_r Delta_r(X)^(nu_r - nu_(r+1)).

This is exactly the distinguished `mtwHw` line. No Schur straightening or general highest-weight theorem is needed.

A maximal row weight in any stable subspace gives a nonzero upper-unipotent fixed vector. The factorial bilinear pairing is nondegenerate on the actual module because its finite defining equations are rational and its rational Gram matrix is positive definite over R. The transpose-adjoint identity makes a perpendicular stable. A proper nonzero stable subspace and its perpendicular would both contain the same highest vector, contradicting its nonzero self-pairing. This proves simplicity directly over every characteristic-zero field.

The Cayley map proves density of the rational unitary group. Distinct nonconjugate CM embeddings project the split unitary group onto the full product of general linear factors, so the same original-field representations are absolutely irreducible. Finite rational coefficient equations prove scalar-extension compatibility.

For classification, take a highest vector in an arbitrary irreducible rational representation, polynomialize its matrix coefficients by determinant powers, and embed its twisted dual into the same polynomial model. The model's simplicity makes the embedding surjective. The factorial pairing removes the twisted dual. A 2 by 2 polynomial curve proves dominance if it was not known beforehand. This avoids using classification to prove classification.

## Exact convention and interface checks

- The transpose in `f(g^t X)` is retained throughout.
- Determinant twists of either sign are included in the factorial-adjoint identity.
- `tenRepF` has highest weight lambda; `wtRepF` is its dual, so its **double dual** has highest weight lambda.
- `rhoVr`/`mtRep` use inverse-transpose and are the tensor representation at the conjugate CM type. Their dual has weight lambda at the original embedding.
- `HWAtF` quantifies over polynomial matrix presentations. Density proves that competing presentations agree at the exact `evPtF` specializations; a fake highest weight cannot be introduced by choosing a different presentation.
- At a single selected embedding, the fixed subspace may have multiplicity from other factors. Applying a nonzero functional to the other factors proves the required single-factor weight uniqueness.
- The source's `SideA` and frame imply the actual eta_T singleton parameter is 1/2. The manuscript makes this check explicit.
- The original coefficient fraction fields have characteristic zero: a noninjective finite map from Z_l into the domain DVR O_0 would make O_0 a field, contradicting its stated nonfield clause. The prescribed injections then give characteristic zero in O and its fraction field.
- The original side embeddings are distinct and nonconjugate because they are a single injective reading composed with the CM-type labels.
- No integral equality between Weyl and dual-Weyl lattices is claimed or used.

## Dependency audit for this chain

| Item | Inputs used | Status |
|---|---|---|
| HP1 exact fixed line | Finite polynomial equations; LDU elimination | Closed |
| HP2 absolute simplicity | HP1; weight projection/interpolation; explicit factorial pairing | Closed |
| HP3 rational-group irreducibility | HP1–HP2; explicit Cayley density; prescribed CM embeddings | Closed |
| HP4 classification and literal dual highest weights | HP1–HP3; matrix-coefficient polynomialization and natural double dual | Closed |
| HP5 original-field descent/CellWt representation branch | HP3–HP4; existing AR12 coefficient descent and the supplied AR14 comparison objects | Representation leaf closed; geometric comparison objects retained |
| HP6 full wt_weights endpoint | HP1–HP4; proved MR19 row arithmetic; literal source SideA/frame/TwR/RingSpec data | Closed under exactly the source data; no extra representation theorem |

No Core, theta nonvanishing, prime-window estimate, automorphic Galois theorem, RH or GRH is used in HP1–HP4. HP6 retains the source's actual `GlobalArtinReciprocity`/`SideA` context; it does not produce those inputs. The old historical dependency records are left unchanged. New closure annotations must supply the old named representation premises from HP, rather than rewriting their history.

## What remains outside this chain

The full 21-field `V4.Core` still requires an actual compatible layout and `Over/RecOK/LedOK`, original `NChoice/MuIsW`, forced primes, good-row spectrum and stability, and theta/local comparison fields. The real representation/volume portion of the Core had already been closed in DC20 relative to the named Harish-Chandra/Tamagawa inputs; repeating that assembly would not advance the frontier.

The present result removes the representation-theory leaf from MR5/MR19 and AR13–AR14. It does not identify independently chosen geometric or local data, change lattices or inner products, construct a nonzero theta family, or infer a full Core from irreducibility.

## Evidence

`provenance.json` records HP1–HP6, 42 exact source ranges in 26 files, and the exact written-proof paragraph hashes. `build_provenance.py` regenerates them and checks every source file against pinned git objects at `7cbf7a0c32fca1badf05931879a37c3f8a2b03b4`. These are source-byte/locator checks, distinct from mathematical review. No Lean build or independent kernel replay was run for this human alternative.
