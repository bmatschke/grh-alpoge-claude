# Independent mathematical review: faithful_etale_v57

**Verdict: PASS.** Reviewer: `/root/arithmetic_common_frame`; author: `/root`. Date: 24 November 2026. This review is bound to the final main SHA256 `e466f2a29e5cb362b03f17809d917f0e444dfe4d32aa929b2ac6d5b2a81491cc` and all 26 exact numbered proof blocks. No Lean replay was performed.

## Scope and main conclusions

I read FET1–FET26 and checked their return against the original `FaithH`, `FixBasis`, `EtBasis`, matrix-decompletion and `WEt` statements at accepted commit `7cbf7a0c32fca1badf05931879a37c3f8a2b03b4`. The manuscript proves the full original faithful-invariants implication, the integral fixed-basis theorem, the actual nonlinear Frobenius conjugacy, the resulting étale basis and all fields of the étale functor. The same prescribed actions, coefficient inclusions and integral lattices are used throughout. Prime 2, rank zero, ramified coefficient extensions, non-Galois finite extensions and every allowed lattice morphism remain in scope.

FET2 uses a named classical foundation, rather than claiming to reprove finite-extension perfectoidness. I independently opened Scholze's *Perfectoid spaces*, Theorem 3.7(i), and Bhatt–Morrow–Scholze's *Integral p-adic Hodge theory*, Definition 3.5 and Example 3.6. The former has exactly the finite-extension scope used here; the latter explicitly includes the completed ring of integers of an algebraic extension containing the cyclotomic tower. The manuscript proves that its actual embedded field is the relevant finite compositum. The sharp expansion is printed and avoids treating sharp as additive or importing an unproved fixed-field equality.

The determinant average uses an infinite common-value set and polynomial nonvanishing, not division by the quotient order. The iterative averaging only requires finite-precision smoothness of the starting lattice vectors and exact invariance of the coefficients chosen at each step. Arbitrary Witt coefficients are not assumed continuous. The resulting vectors form a basis on the original tensor lattice, with its original O-rank.

For nonlinear conjugacy I checked both filtrations, the approximation-before-iteration order, the near-parameter contraction and inverse, the p-adic defect expansion and the limiting equation. The near-parameter filtration contains the image of the integral Witt tensor subring and is not replaced by the whole ambient ring. IFD24 supplies the correction's surjectivity; IFD25 is used only later to descend a matrix that already satisfies the equation. Thus the new argument does not conflate these two different tasks.

The functor construction descends actions and all lattice morphisms through the same injective coordinate maps. I compared the proof with every field of `ExistsOfLayers.WEt`, including all three module structures and both scalar towers. Choices of bases are made once, and uniqueness after embedding proves compatibility of the induced maps.

## Per-claim review

**FET1 — PASS.** Isometry and density identify actC; all inverse-limit coordinates identify actT. The supplied cyclotomic congruence determines the usual integral character, without changing AI or P.

**FET2 — PASS.** The finite cyclotomic levels give Frobenius surjectivity modulo p and a nondiscrete value group. The actual closed compositum LE0 equals the completed L-cyclotomic tower, so Scholze Theorem 3.7(i) applies, including p=2 and non-Galois L.

**FET3 — PASS.** The valuation intersection proves injectivity modulo p. The binomial estimate gives the sharp limit and its lift independence; recursive residue lifting gives the p-weighted expansion. Equivariance does not presuppose that g preserves E, and sharp is never treated as additive.

**FET4 — PASS.** The embedded tilt of the completed L-cyclotomic tower is fixed by G_L intersect ker chi. Fixing that tilt fixes its sharp expansions and hence L. This proves the original FaithH implication, in fact without needing its extra chi(g)=1 antecedent.

**FET5 — PASS.** FaithH separates finite H/N cosets on S^N. The prescribed epsilon is fixed by H, epsilon-1 is a nonzero nonunit, and its powers give the infinite common-value set; the argument includes p=2.

**FET6 — PASS.** Dedekind independence gives a spanning set of evaluation vectors; a determinant polynomial is nonzero at the q0 coordinate and therefore somewhere on the infinite common-value grid. Arbitrary finite index sets and zero matrix size are preserved by reindexing.

**FET7 — PASS.** Teichmuller lifting preserves the chosen residue determinant and exact N-fixedness; the Witt unit criterion applies over the perfect field F. No division by p or the finite quotient order occurs.

**FET8 — PASS.** Coset permutation makes the trace u fixed; multiplying by its fixed inverse produces an exactly trace-one, N-fixed coefficient in the original Witt ring.

**FET9 — PASS.** Finite coset shifts give the error modulo J_m. A common smaller normal subgroup handles every summand at each later precision. Only smoothness of x and exact fixedness of the averaging coefficient are used, not continuity of arbitrary Witt coefficients.

**FET10 — PASS.** Trace-one averages improve invariance by one precision and change the preceding iterate only in J_m. Completeness supplies the limit, and stability of each J_m plus separation proves exact H-fixedness without a global continuity assumption.

**FET11 — PASS.** Finite-dimensional module topology gives continuous integral coordinates for the original lattice action. Cofinal finite Galois subgroups supply N0. The larger Zp-basis tests invertibility, while commutation with O makes the same operator an automorphism over the original tensor ring.

**FET12 — PASS.** The fixed lifted vectors differ from one common automorphism image of the original O-basis by pM. The matrix 1+pZ has an integral geometric inverse, preserving lattice and rank; the empty basis handles rank zero.

**FET13 — PASS.** The literal RW, TW and FixBasis definitions agree with the construction. The finite Galois subgroup family is cofinal. No Good, crystalline or Wach assumption is inserted into the full exported fixed-basis theorem.

**FET14 — PASS.** The inherited near-parameter groups retain c(B), not all of W. Their intersection, common pole bounds, Frobenius-stable approximation, p-saturation and both summation properties apply to the same actual maps and H. Original ioE/character compatibility gives j(E) and t in the fixed ring.

**FET15 — PASS.** The exact contraction inequality p(i+2k+1)-2k >= i+2k+2 holds for every p>=2. The fixed near-parameter sum solves the equation modulo p by telescoping; this is distinct from the subsequent p-adic limit.

**FET16 — PASS.** Choosing precision 3k0+1 before the unknown Frobenius exponent is valid because both pole bounds and error precision scale by p^N. The ordered product of Frobenius iterates has the claimed conjugacy orientation.

**FET17 — PASS.** The negative error times the inverse has the required near-parameter order. The contraction identity gives (1+z)F1=j(A)phi(1+z) modulo p. A near-parameter geometric sum followed by a p-adic inverse makes 1+z invertible; WIS18 reflects the determinant unit to E.

**FET18 — PASS.** IFD24 supplies surjectivity for the vectorized operator j(A)phi(z)j(A^{-1})-z. Multiplication on the right recovers the exact correction equation; IFD25 alone would not justify this existence claim.

**FET19 — PASS.** The maintained defect has order p^(n+1), and saturation makes its quotient fixed. The explicit correction expansion kills its residue, preserves all congruences and converges in the fixed ring and E. Separation gives the exact nonlinear equation, with V=1+pZ invertible.

**FET20 — PASS.** The three conjugacies compose in the printed order, retaining fixed and invertible matrices. Unit reflection proves the stronger invertibility of the coefficient matrix. Every original good-layer and IoW premise is retained, including zero rank and p=2.

**FET21 — PASS.** Pure tensors show that Frobenius images span; semilinearity then makes the images of the finite basis span. Their coordinate matrix is invertible and fixed. The change e-prime=eV has exactly the stated matrix equation and ioE image.

**FET22 — PASS.** The coordinate embedding is injective, semilinear and spanning. The already supplied fixed-column Frobenius equation gives a rectangular IFD25 descent with zero inhomogeneous term and both coefficient matrices invertible.

**FET23 — PASS.** Normality of H fixes the Galois-transformed basis columns; the precise gamma_E matrix yields the required Frobenius system. Character injectivity identifies the kernel of resGamma with H, and its original surjectivity gives the quotient action. All laws descend by injectivity.

**FET24 — PASS.** Every original equivariant O-linear lattice morphism gives a fixed column system with the source Frobenius matrix. Its unique descent proves naturality, identity, composition, addition, scalar and action compatibilities despite independently chosen bases.

**FET25 — PASS.** Every WEt record field is supplied: three module structures, both scalar towers, exact rank, O-linear semilinear Frobenius/Gamma actions, all morphism laws, and the injective spanning natural tensor comparison. No crystalline hypothesis is needed for this etale functor.

**FET26 — PASS.** WPR30 applies to this same WEt under its original Bhatt-Scholze realization and LocTied premises. Herr/class-map, quantitative comparison and common ConclF estimates are not inferred; no whole denominator obligation is closed.

## Evidence and boundaries

All 12 full formal-source snapshots were independently compared byte-for-byte with both the accepted Git blobs and the read-only checkout. All 20 source ranges and all 26 proof ranges were independently hashed. The 15 inherited proof blocks were checked against their frozen parent ledgers and full proof files. Additional read-only checks included the original LocLat module-topology fields and continuous lattice-coordinate supplier; these justify the continuity assertion used in FET11. The current standalone TeX record is bound to the final main bytes and reports two passes with zero diagnostics.

The five missing spacing backslashes in FET.12, FET.14, FET.19, FET.20 and FET.21 were reported and corrected before this binding. The final text also consistently says finite extensions of Qp where intended. There is no outstanding mathematical or scope correction.

The original Good/GamS/WSer/IoS/IoW records remain supplied at the coefficient-conjugacy and functor endpoints. FET26 retains the original crystalline-realization and LocTied inputs of WPR30. Herr class maps, convergent evaluation and filtered comparison, quantitative local row bounds, and the actual common ConclF family are separate unfinished producers. This review closes no whole selected obligation.

Primary published statements checked:

- https://www.math.uni-bonn.de/people/scholze/PerfectoidSpaces.pdf — Theorem 3.7(i), printed page 17; retrieved reference `turn263184599view0`.
- https://www.math.uni-bonn.de/people/scholze/integralpadicHodge.pdf — Definition 3.5 and Example 3.6, printed page 21; retrieved reference `turn364147166view0`.
