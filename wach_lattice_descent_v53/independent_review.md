# Independent review of WLD1–WLD26

**Verdict: PASS at the stated original premises.**

Reviewer: `/root/geometry_alltest`, independent of the author. Date: 2026-11-23.

Reviewed proof: `wach_lattice_descent_v53/main.tex`.

Main SHA256: `a2badad161459a2eea44ead9749f58d4b74891b139a6356a3e164207d9ebc8d6`.

Formal source pin: `7cbf7a0c32fca1badf05931879a37c3f8a2b03b4`.

I read every numbered human proof and checked the original producer bodies and definitions. I independently verified all 26 proof-block hashes, all 19 source snapshots against the pinned Git blobs, all 25 exact source ranges, and both inherited DFD12/SSC17 proof bindings. The companion JSON records the exact block and source hashes and a separate mathematical assessment for every claim. No Lean replay was requested or performed.

## Mathematical checks

### Tensor descent without flatness

WLD7 correctly uses the tuple indexed by coefficient-basis elements and an E-basis only as a spanning tuple. It does not call its dr vectors an E-basis. The square W-coordinate matrix has a right inverse; determinant invertibility descends by the explicitly supplied reflection of units. Decomposing 1 then proves spanning in the original D.

WLD8 proves injectivity of the actual map E tensor_A N -> D by an explicit tensor normal form. Moving the O-coefficients through the tensor product is valid because N is already an A-submodule. The resulting coefficients have images in c(W). Uniqueness of W-coordinates and injectivity of iota annihilate those coefficients. This does not require flatness of E or B over the intermediate rings. It matches `IsBaseChangeLatticeOfBasisAfterExtension.lean`, including the supplied basis and rank scope.

### Local-prism fractions, cancellation and the reverse span

WLD10 proves the necessary semilinear base-change basis and kernel statements directly. WLD11 uses the source's actual `FCrys.Phi_nat` fraction law: after transfer, a power of psi(Q) annihilates the relevant difference. Cancellation takes place in the free module over the domain W, with psi(Q) nonzero. No cancellation is performed in the possibly non-domain S. For the reverse inclusion, the proof clears both denominators and the discrepancy of an equality initially known only in a localization. The original arbitrary ideal element Q is sufficient because `FCrys.Phi` and its base-change law are indexed by each element of the prism ideal. The generator condition is needed later in the stated generic prism interface, not silently added to this local-value lemma.

### Fixed tuples and rank zero

WLD15 preserves the exact generic coefficient-descent premise with arbitrary target matrix U. In positive rank, the images of an E-basis form a B-basis because a square spanning matrix has invertible determinant. Fixed pure tensors show the Frobenius matrix is invertible over B, and unit reflection returns it to E. In rank zero, the tensor module is zero and injectivity of j forces the original etale module to vanish; the proof does not infer finite generation from natural-number finrank zero. The same distinction is maintained in WLD19.

### Actual lattice, functoriality and generic prismatic scope

WLD13 applies the full-faithfulness clause to the chosen realizing crystals and every original equivariant lattice map. This includes multiplication by an O-scalar, which is needed to prove A-stability. WLD14 identifies the actual image of the supplied trivial lattice using its original generator. Thus WLD18–24 construct one inverse-image submodule inside the supplied etale functor and verify all original WN fields on it, including maps, projectivity over the specified power-series ring and the noncrystalline zero convention.

WLD25 explicitly retains the original generic `hreal`, including the action tie, and the original direct `hmem`. It does not infer generic realizations from a theorem about only the standard period datum, nor replace `hmem` by a stronger matrix theorem. The all-layer specialization in WLD26 separately supplies realizations from the stated published input and tied data. Its three remaining period-ring suppliers are correctly retained.

## Resolved review finding

WLD17 invoked WLD6 without repeating injectivity of iota in that intermediate claim. The final `build_prism` interface already contained the assumption, so the final endpoint was not overstated. The author added the missing explicit sentence immediately after the WLD17 label. I checked that correction in the bound final proof. No unresolved mathematical finding remains.

## Scope of the verdict

The original generic `build` and `build_prism` implications are fully reconstructed. WLD26 remains conditional on the actual Wach prism, injectivity and reflection of units for ioE, and the homogeneous fixed-Frobenius matrix solution theorem. This review does not close those producers, full HW/Fon/Cmp, the quantitative local family bounds, the common ConclF family, or GLOBAL_DENOMINATOR. The published crystalline-lattice premise and its optional DFD12 conversion retain their original scope. No old component or author proof was edited by the reviewer.
