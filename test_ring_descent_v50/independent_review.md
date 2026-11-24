# Independent review of TDR1–TDR13

**Result: PASS at the stated premises and scope.**

Reviewer: `/root/arithmetic_common_frame`  
Author: `/root/geometry_alltest`  
Reviewed proof: `test_ring_descent_v50/main.tex`  
SHA-256: `e19e27576c1aa60c573efd79739da24edd3e76a48243a5c5290610661120e33f`  
Source pin: `7cbf7a0c32fca1badf05931879a37c3f8a2b03b4`

This review independently read the mathematical proofs and compared their exact interfaces with the pinned Lean definitions and endpoint statements. It accepts the readable proof of finite-subalgebra descent for every coefficient algebra and the return to the original `AllTest` predicate for every reduced coefficient algebra, conditional on the supplied original moduli data and `Out.SecBaseChangeSt`. It is not a claim to supply that section-base-change premise, to construct the moduli scheme, or to complete the surrounding common-family obligation.

## Findings on the requested sensitive points

### Arbitrary and nonflat coefficient changes

The distinction between the original base scheme and the new coefficient algebra is correct. In `GlobalSectionsRankAlgClosed.lean`, `SecBaseChangeSt` assumes the original scheme is locally Noetherian, then quantifies over every commutative ring and every affine map into the selected neighborhood. There is no reducedness or flatness restriction on that coefficient ring. The original moduli scheme and its finite field extension are locally Noetherian because they are smooth over fields. Applying this predicate with `n = 1` yields one stable basis section, exactly as used in TDR2.

TDR1 uses the idempotents of the split characteristic-zero algebra to obtain the eigenbundles. Direct-summand formation and Lie base change commute with arbitrary coefficient changes. Pullback of an isomorphism from a free module stays an isomorphism even when the algebra map is nonflat. Thus TDR3 does not infer stability of an arbitrary generator merely from a generic-fiber calculation: it uses the exact stable-section assertion proved in TDR2. Zero-rank eigenspaces and the zero coefficient ring are handled explicitly.

TDR8's localization map is indeed injective for every inclusion of rings and localization at the same element. A fraction that becomes zero gives an equality `h^N r = 0` in the larger ring, hence in the subring. This proof allows nilpotents and zero divisors. The finite-coefficient capture retains the coefficients witnessing the unit-ideal equation, so its principal opens still cover the descended spectrum. Relations among the captured generators hold by this injection; no hidden flatness or finite-presentation assumption on those relations is used.

### Applicability of the section premise to the actual universal object

The pinned `Obj.toPolAV` conversion in `ObjIsAbelianSchemeDimRigidifiedSym.lean` takes the original `Obj`, with its proper semiabelian group, rigidified symmetric line, relative ampleness and `KTriv` fields, to precisely the `PolAV` input required by `SecBaseChangeSt`. The geometric multiplicities determine the relative dimension. The conversion preserves the actual group and line; it is not a replacement by an unrelated principally polarized abelian variety. The independent source proof `ExistsLocalSectionNonzeroAllFibresModuli.lean` also applies `pushInvertible` to this same `Obj.toPolAV Xo.univ`. This confirms that the retained original data in TDR2 suffice.

At `n = 1`, the line in that section predicate is the source's one-fold `LPow`; the proof's identification with `PPx` is by the canonical pullback and one-fold line isomorphisms. The local basis assertions identify the direct-image sheaf with a line bundle, and the Zariski gluing argument proves the required global section and base-change identification for every affine target. No stronger `SecBaseChangeAnySt` has been introduced.

### Representability, finite presentation and finite descent

TDR7 constructs the frame schemes from explicit matrix-localization charts. Their transition maps come from the vector-bundle and line-bundle transitions. This establishes affineness and finite presentation over the moduli scheme, and identifies their points with the actual ordered eigenbases and actual chosen section. The manuscript does not extend the `Moduli.rep` axiom from reduced schemes to nonreduced schemes: it uses the already supplied universal family to construct a separate frame scheme over the actual base.

The separatedness used in TDR10 is justified by quasiprojectivity of the moduli scheme and by affineness of its frame bundle. The equality descent on overlaps uses the pullback of the closed diagonal. Its defining ideal maps to zero in an injective localized coefficient extension, so that ideal is already zero. This proves the needed equality of maps without assuming that an injective ring extension is faithfully flat or surjective on spectra. The theorem is stated for separated locally finite-type schemes, which covers the actual two uses; the metadata explicitly does not claim the more general source factorization theorem in every context.

Both proofs of TDR11 are valid. The short proof uses the constructed frame scheme and TDR10. The expanded proof verifies equality of the actual underlying chart maps before applying same-point frame equality and gluing. This is an essential detail: comparison of frame matrices alone would not have established equality of arbitrary underlying scheme maps.

### Literal `FrMap`, `FrameRing`, `TRing` and `FromTest`

The tangent base change in TDR3 is the coefficientwise map on dual numbers. Its section base change uses the canonical fiber-product map with both projection equations and the source's chartwise `appLE` identities. The uniqueness proof therefore rules out scalar ambiguity. TDR4 uses row coordinates, in agreement with the source's `FrChg`; its injection criterion retains the same-underlying-point premise.

TDR6 supplies all generic matrices and the separate unit section scalar, inverts their determinant product, and proves the universal property over every coefficient algebra. The exact actual-frame classifier follows from the unique comparison coordinates. Rank-zero determinants are correctly one. Finite type and reducedness survive the polynomial and localization construction.

TDR12 proves the full radical-ideal quotient presentation, including the unit ideal and the zero algebra. In TDR13, the descended subalgebra is reduced because it injects into the given reduced algebra. The frame is transported along the inverse of the actual presentation isomorphism, and the final algebra map is inclusion composed with that same isomorphism. The resulting triple is exactly `FromTest`, not an isomorphism-class substitute. For `CAt sigma`, the embedding is preserved. The test-ring witness may depend on the already chosen family's member, in agreement with the source's pointwise quantifier.

## Claim-level disposition

| Claims | Disposition | Main verification |
|---|---|---|
| TDR1 | PASS | Dual-number tangent interpretation; split idempotents; actual ranks; arbitrary base change. |
| TDR2 | PASS | Original `SecBaseChangeSt` at `n = 1`; actual line; invertible direct image and all coefficient targets. |
| TDR3–TDR4 | PASS | Literal `FrMap`, functoriality, unique matrix/scalar change and injection equality over the same point. |
| TDR5–TDR6 | PASS | Reduced finite-type local charts; explicit universal algebra; full classifier. |
| TDR7 | PASS | Constructed representability; finite presentation; separatedness; no misuse of reduced moduli representation. |
| TDR8–TDR9 | PASS | Nonflat localization injection, simultaneous finite capture and exact gluing. |
| TDR10–TDR11 | PASS | Separated point descent and complete original framed-point descent over arbitrary rings. |
| TDR12–TDR13 | PASS | Radical quotient equivalence and exact original `AllTest`/`FromTest` return. |

## Mechanical correspondence and remaining scope

All 24 snapshotted source files were independently compared byte for byte with `git show` at the stated pin. All 13 claim-block hashes and all source ranges referenced in the claim provenance match their actual bytes. These correspondence checks support reproducibility; they are separate from the mathematical reading above.

No unresolved mathematical or interface defect was found in this snapshot. No change to the author's proof was made. The supplied `Moduli` record, the original `SecBaseChangeSt` premise and standard algebraic-geometric foundations remain explicit. The normalized analytic frame family, its Borel and invariance conditions, the covering/fiber statements, `IsUnf`, and the common-family construction remain outside this packet. This review neither closes any selected compound obligation nor certifies a complete human RH/GRH proof. No Lean rebuild, kernel replay or PDF visual review is claimed.
