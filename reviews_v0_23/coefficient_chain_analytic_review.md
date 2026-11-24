# Independent review of the coefficient-representation closure

**Result: PASS for the stated HP1–HP6 scope.** No substantive mathematical defect or source-interface mismatch was found in the frozen text. The proof closes the characteristic-zero coefficient-representation branch, including the original-field `wt_weights` supplier. It does not claim construction of the compatible geometric, theta, toric, or local witnesses retained in MR/AR, or an unconditional proof of RH or Dirichlet GRH.

Reviewer: the analytic/cohomological-window reconstruction agent, independent of the author of HP1–HP6. Date: 2026-11-22.

## Frozen material and verification

Reviewed component: `chain_closure_core/main.tex`.

- Main TeX SHA256: `18ceea89209fe83e7c0bea6ddb72157a616d62cd4b4a6a84ab9e6542d260e30c`.
- Component provenance SHA256: `738b05daf0fafc007c9f11ff17e36567e3329b9ab335fb26cf332575508a8368`.
- Lean source commit: `7cbf7a0c32fca1badf05931879a37c3f8a2b03b4` in `CocoSgt/riemann-hypothesis-lean`.
- Independently recomputed all 6 proof-range hashes and all 42 recorded source-range hashes, lengths, and file hashes. The 26 distinct source files were also compared byte for byte against their pinned Git blobs. All comparisons passed.

This review checks the mathematical arguments and their match to the stated source definitions and endpoints. It is not a fresh Lean build or a kernel replay. Source-backed endpoints are those recorded in `chain_closure_core/provenance.json`; hashing is evidence of source identity, not a substitute for the mathematical review below.

## HP1: the literal polynomial model and fixed line

The identification with `dualWeyl`, `nablaSq`, and `VV` is correct. In particular, the source uses substitution by the transpose together with the last-weight determinant twist. This convention is preserved in HP.2. The right-upper-unipotent invariance equations are precisely the generic column-addition equations, and disjoint matrix-variable blocks realize the tensor product injectively.

The finite-equation argument proves scalar extension over every characteristic-zero field: it works inside a finite-dimensional column-multihomogeneous polynomial space, with rational row reduction. It does not require an unproved assertion about an integral lattice. Gaussian elimination on the open big cell gives the claimed unique upper-fixed vector for the left representation, since the transpose converts upper matrices into lower row operations. The resulting polynomial is the literal principal-minor vector `mtwHw`.

The pre-dominance extension is also valid. A nonzero fixed polynomial has nonzero value at the identity by its big-cell formula. Specializing the indicated two-by-two block makes exactly one leading principal minor equal to the variable and the others equal to one. A negative exponent would contradict polynomiality. This extension is sufficient for the later matrix-coefficient classification argument.

## HP2: existence, pairing, and absolute irreducibility

The maximal-height torus-weight argument supplies a nonzero upper-fixed vector in any stable subspace over an infinite characteristic-zero field. The finite weight projections can be obtained by interpolation at a single generic diagonal element. The coefficients of the elementary-unipotent orbit polynomial belong to the stable subspace by Vandermonde interpolation. Positive powers raise the chosen height, so maximality forces their vanishing.

The factorial pairing argument correctly establishes the needed duality rather than assuming it. Its restriction to the rational module has a positive-definite rational Gram matrix. Rational scalar extension then makes that restriction nondegenerate over every characteristic-zero coefficient field. Positivity is used only over the rationals inside the reals, not asserted for an arbitrary coefficient field.

The transpose adjoint identity includes the determinant twist, also when that twist is negative. Consequently the annihilator of a stable subspace is stable. If a proper nonzero stable subspace existed, it and its nonzero annihilator would both contain the same highest vector, contradicting the nonzero factorial self-pairing of that vector. This proves absolute irreducibility directly and closes the exact `HwFixedEx` and `HwFixedLine` interfaces without a retained Schur-module or highest-weight theorem.

## HP3: rational unitary points and the original coefficient fields

The Cayley parametrization supplies the required rational-point density. The skew-Hermitian matrices form a rational vector space, and the Cayley transform and its inverse are defined on nonempty open subsets. Polynomial identities on its rational points remain identities after extension of the coefficient field. This is adequate for passing invariance equations from the actual rational unitary group to its split algebraic group.

After splitting the CM field, the unitary equation pairs a matrix with its inverse transpose at the conjugate embedding. The selected embeddings are distinct and nonconjugate, so projection to their general-linear factors is surjective. HP2 therefore gives irreducibility, also after any coefficient extension. No embedding of an arbitrary coefficient field into the complex numbers is needed for this step.

The polynomial presentation of `IsAlgWeightF` is correctly retained on the original field: negative determinant powers are replaced using the conjugate embedding and the unitary equation. The finite dual is polynomial as well, because group inversion on unitary matrices is conjugate transpose.

## HP4: classification, duals, and literal highest-weight predicates

The classification proof is noncircular. The weight decomposition is read from the Laurent expansion of the torus action; the upper-fixed vector follows by the already proved maximal-height argument. Clearing finitely many inverse determinants makes the matrix coefficients polynomial. The orbit-spanning property makes the coefficient map injective. The pre-dominance part of HP1–HP2 proves dominance and irreducibility of its polynomial target, hence surjectivity.

The action calculation in HP.15 gives the dual composed with inverse transpose, together with the explicit determinant shift. Canceling that shift yields the stated canonical weight. The pairing identity gives the required equivalence between the canonical module and its dual composed with inverse transpose, so applying this involutive operation recovers the original representation. There is no use of the desired classification theorem as an input.

The three source conventions are distinguished correctly: `tenRepF` has highest weight lambda; `wtRepF` is its dual; and `mtRep`/`rhoVr` uses inverse-transpose matrices, whose dual is equivalent to `tenRepF` with the displayed lambda. The source's `HWAtF` specifies the highest weight of that dual where required. A single dual at unchanged embeddings would instead reverse and negate the ordinary highest weight, and the proof does not make that substitution incorrectly.

The verification of the literal `HWAtF` quantifiers is adequate. Any alternative polynomial matrix presentation agrees on dense rational unitary points, hence on the split group and the exact `evPtF` evaluation point. Contracting the other tensor factors reduces the claimed eigenvector to a nonzero upper-fixed vector in the selected factor, where HP1 determines its weight. This addresses changes of basis and polynomial presentation, not merely an abstract highest-weight isomorphism class.

## HP5: the inverse-transpose descent step

This is the convention-sensitive step requested for special review. Let S be the chosen nonzero irreducible constituent of the complexification. The frozen text classifies **its dual** and then dualizes back. Written with all intermediate objects, the argument is:

\[
S^*\simeq V_\lambda
\quad\Longrightarrow\quad
S\simeq V_\lambda^*
\quad\Longrightarrow\quad
S\simeq V_\lambda\circ\iota,
\qquad \iota(g)=g^{-t}.
\]

The last equivalence is HP.16 composed with the involution. Thus the inclusion of S into the complexification produces a map **from the inverse-transpose canonical module**. The argument never claims that twisting an arbitrary constituent by inverse transpose preserves that constituent's ordinary highest weight. Lambda is obtained by classifying the dual, exactly as the source's dual highest-weight endpoint requires.

The descent to the original field is valid. Applying a field-linear functional from the complex numbers to the coefficient field to the entries of the complex intertwiner preserves every intertwining equation, because all its coefficients lie in that field. Choosing the functional not to kill a nonzero entry preserves nonzeroness. One functional works for all rational group elements; there is no exchange of scalar extension with an infinite intersection. Absolute irreducibility of the canonical source and irreducibility of the target make the descended map an isomorphism.

The proof does not assume that an irreducible representation has irreducible complexification. It selects a minimal nonzero constituent first and derives the desired absolute statement only after descent. HP4's uniqueness subsequently identifies the prescribed dual highest weights. This matches `GlobalTheory.WtDescent.weight_descends`, including the original `rhoVr` inverse-transpose action.

For the subsequent `CellWt` comparison, the component preserves the supplied actual `MtReal`, `CharSide`, `SideRead`, field maps, and basis-change witnesses. It closes the representation comparison within AR14, rather than producing those geometric witnesses.

## HP6: exact `wt_weights` endpoint

I checked the statement and construction of `GlobalTheory.HeightCounting.FormsStep.wt_weights` in `ExistsWeightDataIntegral.lean`, together with the half-integral shift, original fraction-field characteristic-zero, and distinct-nonconjugate embedding suppliers. The following details match:

1. The actual frame and character records force a singleton shift to equal one half; the integer in the half-integrality witness can be zero. The row-gap and parity calculation is taken from the already reconstructed MR19 arithmetic, with the same infinitesimal-character identity. Missing singleton antecedents and unused rows are handled by zero padding.
2. The coefficient modules are constructed on the original fraction fields as duals of the literal `VV` modules, with `wtRepF` at the original side-dependent embeddings. No abstractly isomorphic replacement host or larger coefficient field is selected.
3. The original CM-type labels imply the embeddings are distinct and nonconjugate. The finite algebra and DVR hypotheses force characteristic zero: a nonzero prime kernel in the map from the l-adic integers would make the target a finite-dimensional domain over the residue field, hence a field, contradicting its nonfield DVR condition.
4. The five clauses are all supplied: irreducibility, `IsAlgWeightF`, every required base-change irreducibility assertion, existence of `HWAtF` on the dual, and the universally quantified infinitesimal-character identity obtained from uniqueness of that literal predicate.
5. The lower bound can be bottom, as in the source. The construction works over all original rows, sides, and coefficient extensions required by the endpoint.

The source's remaining global and geometric hypotheses are explicitly retained. In particular, this review does not remove `GlobalArtinReciprocity`, the specified D/frame/SideA records, star stability, or integrality of `eExp`; it confirms that the characteristic-zero representation-theory supplier no longer needs an extra unreconstructed representation theorem.

## Scope conclusion

HP1–HP6 form a coherent closed representation chain: literal polynomial equations and Gaussian elimination give the fixed line; the factorial pairing gives absolute irreducibility; rational-point density gives the actual unitary representation; matrix coefficients give classification and exact dual conventions; original-field descent gives the coefficient comparison; and the existing row arithmetic supplies the full literal `wt_weights` endpoint.

There are no requested mathematical changes to the frozen component. This positive review concerns that chain and its stated hypotheses. The retained compatible geometric and arithmetic suppliers remain separate obligations in the global dependency audit.
