# Elliptic transfer for the lower-row multiplicity comparison

Let $E/F$ be the CM extension of the stage. It is unramified at finite places. Let $G=U(V)$ and $G'=U(V')$ have the same odd rank $r$, with discrete series $M_\tau,M'_\tau$ at each real place and the same ordered integral Harish–Chandra parameter $\lambda_\tau$. For the original trace comparison the adjacent gaps are at least $r$. At each finite place the given group isomorphism $j_v$ comes from an $E_v$-linear isometry taking the specified lattice onto the specified lattice, where $E_v=F_v\otimes_F E$. For the good finite type and every proper block dimension $a$, some marked split place has no nonzero vectors invariant under the upper block unipotent group of type $(a,r-a)$. Use the auxiliary split Iwahori test and the marked type tests from the trace comparison. For each such finite test family, the traces on the two groups have **equal contributions from every irreducible characteristic polynomial**. [Exact hypotheses][hyp] · [Lattices, gaps and marked types][data]

## The orbital integral at a finite place

A polynomial contributing to the field part is monic, irreducible and conjugate reciprocal over $E$, of degree $r$ and nonzero constant term. Put $A=E[X]/P$, write $\alpha=X\bmod P$ and let $*$ extend conjugation on $E$ by $\alpha^*=\alpha^{-1}$. Its fixed field is $A^+$ and the centralizer torus is
$$
 T_P(k)=\{u\in (k\otimes_F A)^\times : uu^*=1\}.
$$
For $k=F_v$, a conjugacy class with polynomial $P$ is represented by a parameter $x\in(k\otimes_F A^+)^\times$ for which
$$
   h_x(y,z)=\operatorname{Tr}_{A/E}(x y z^*)
$$
after scalar extension is isometric to the given Hermitian space. In such an isometry $\phi$, multiplication by $\alpha$ gives the element $\gamma$ and multiplication by $u\in T_P(k)$ embeds its centralizer. Changing the generating vector multiplies $x$ by $bb^*$. Conversely a conjugator commutes with the action of $\alpha$, so after identifying the two polynomial models it is multiplication by an element of $(k\otimes_F A)^\times$. This gives exactly the stated norm equivalence, including when the completion of $A$ is a product. [Field, classes and orbital integrals][pol] · [Classification and localization][rat]

Choose a Haar measure $dt_v$ on $T_P(F_v)$ and transport it via this embedding to the centralizer. Push $dg_v$ forward by $j_v$ and put $f'_v=f_v\circ j_v^{-1}$. If $b_v$ is the lattice isometry defining $j_v$, use $b_v\phi$ for $G'$. The parameter $x$ is the same, $\gamma'=j_v(\gamma)$, and the square of torus embeddings commutes on each $u$. Hence the centralizer measure on $G'$ is exactly the pushforward of the old one. Weil's quotient integral formula now identifies the measures on the two centralizer quotients. A change of variables gives
$$
 O_{j_v(\gamma)}(f'_v;j_{v*}dg_v,dt_v)=O_\gamma(f_v;dg_v,dt_v).
$$
Apply the same argument with $b_v^{-1}$ to obtain equality of the sets of permitted norm classes, so the sums $\Phi_v(P)$ over them agree. The prescribed finite type convolution and the characteristic functions of the auxiliary Iwahori double cosets are transported by the same $j_v$, including their Haar normalizations. In particular no scalar arises from how the residue group was framed. [Finite orbital equality][finite] · [Transport of the test functions][ftest]

## The orbital integral at a real place

Fix $\tau$ and a signature $(p,q)$, $p+q=r$. Choose the pseudo-coefficient of the specified single discrete series with trace one in that representation, relative to the chosen group Haar measure. For a regular element with compact centralizer its orbital integral is $\overline{\Theta_{M_\tau}(\gamma)}/dt_\tau(T_P(F_\tau))$. At a regular element with noncompact centralizer the orbital integral vanishes. In the usual probability normalization on the elliptic torus the denominator is one. Rescaling $dt_\tau$ divides the quotient measure by the same scalar. This is the local pseudo-coefficient orbital integral theorem. Its other spectral consequences, in particular removal of nontempered contributions in the global spectral calculation, require the separate spectral argument. [Labesse, *Introduction to Endoscopy*, §III.6][lab] · [Exact orbital integral on an archimedean frame][arch]

When $T_P(F_\tau)$ is compact, the $r$ roots $z_0,\ldots,z_{r-1}$ of $P$ at the chosen embedding of $E$ are distinct and have modulus one. Orthogonal eigenlines give one real conjugacy class for each assignment of $p$ positive and $q$ negative lines. An isometry of the sign spaces can permute eigenlines within each sign. Thus the assignments run through cosets of $W_K=S_p\times S_q$ in $S_r$. This is a sum over **elements in a stable conjugacy class** for the pseudo-coefficient of one representation. It requires no averaging over choices of discrete-series representation. [Real classes and compact Weyl cosets][realclass]

Write $r=2k+1$. The character of the chosen discrete series at an ordered diagonalization has Harish–Chandra sign $(-1)^{pq}$. Its numerator is the $W_K$ alternating sum with integer exponents $\lambda_j+k$ after combining numerator and denominator with the common determinant shift. Its denominator is $\prod_{i<j}(z_i-z_j)$ in that ordering. Since $p+q$ is odd, $pq$ is even, and the sign equals $+1$ **at this place**. Reordering the roots changes the denominator by the permutation sign. As the admissible sign assignments run through the cosets, the numerators with this extra sign give the full $S_r$ alternant exactly once. Consequently, using zero-based indices,
$$
 \Phi_\tau(P)=
 \frac{1}{dt_\tau(T_P(F_\tau))}
 \overline{
   \frac{\det(z_i^{\lambda_j+k})_{0\leq i,j<r}}
        {\det(z_i^{r-1-j})_{0\leq i,j<r}}
 }.
$$
The Weyl highest weight here is $\lambda_j-k+j$. The quotient is symmetric in the roots and independent of the signature. Each summand uses its own assigned eigenline signs; comparison is after summing those conjugacy classes. A noncompact $T_P(F_\tau)$ contributes zero for both groups. Thus all real factors agree for the two specified discrete series, even at places where the signatures differ. This also proves that the product of the real transfer signs is $+1$. [Character on the compact torus][hchar] · [Odd-rank sign and determinant calculation][weyl]

## Why the local factors can be multiplied

For a fixed $P$ choose the same family of local Haar measures on $T_P$ for both groups. Normalize its standard compact subgroups to have mass one outside a finite set and take the restricted-product measure $dt$. For almost every finite $v$ the characteristic function of the framed compact contributes one on the trivial norm class and zero on every other class. To see this, discard the discriminant primes of the order generated by $\alpha$ and the finitely many primes where the lattice or the test is exceptional. The unramified integral conjugacy calculation then gives one class meeting the compact. Its intersection with the torus is the chosen compact subgroup of $T_P(F_v)$. The quotient of the two volume-one compacts has mass one on the orbit. [Integral conjugacy and normalized orbital integrals][unit]

A genuinely global condition is required to replace the rational class sum by a product of sums. Write $h_1$ for the trace form with $x=1$ and $J$ for the prescribed global Gram matrix. Suppose a collection $(x_v)$, trivial almost everywhere, gives trace forms isometric to $J$ at every place. In compatible bases the determinant of $h_x$ is that of $h_1$ times $N_{A^+/F}(x)$. Hence at each $v$ the norm of $x_v$ in $F_v^\times/N(E_v^\times)$ equals the image of the single global element $\delta=\det J/\det h_1\in F^\times$. For the quadratic extension $A/A^+$, the sum of the local norm-residue invariants over places above $v$ equals the invariant of $N_{A^+/F}(x_v)$ for $E/F$ at $v$, by compatibility of norm and corestriction. The product formula for $\delta$ gives precisely the reciprocity condition for the prescribed local norm classes. Quadratic norm reciprocity therefore supplies a global $x$ with these classes. The Hasse norm theorem makes its norm class unique, and the local-global principle for Hermitian forms puts $h_x$ on the prescribed global space. The proof uses the stage's unramified CM host in the pinned local-to-global and integral statements. This argument takes place separately for each global Hermitian space, allowing different signatures. [Determinant and local norm condition][norm] · [Global class construction][glue]

Unfold a rational conjugacy-class contribution along its centralizer. Multiplication on $A$ identifies that rational centralizer with $T_P(F)$, giving the common factor $\operatorname{vol}_{dt}(T_P(F)\backslash T_P(\mathbb A_F))$. It is finite since the global norm-one torus for the quadratic field extension is anisotropic over $F$. The remaining integral is a product of local orbital integrals. Summing the rational classes using the preceding bijection and the almost-everywhere unit calculation therefore gives the $P$-term
$$
 \operatorname{vol}_{dt}(T_P(F)\backslash T_P(\mathbb A_F))
      \prod_{v<\infty}\Phi_v(P)\prod_{\tau\mid\infty}\Phi_\tau(P).
$$
Every local factor and the global volume now agree. A local rescaling of the torus measure multiplies its global volume and inversely scales its orbital factor. The normalized test functions on the two groups may use arbitrary global Haar measures as in the source: use the pushed-forward finite factors and distribute the remaining positive global scale into the archimedean group factors when choosing their normalized pseudo-coefficients. [Unfolding and product of finite class sums][unfold] · [Global and local measures][meas]

Only finitely many rational characteristic polynomials can meet the compact adelic support since their coefficients belong to the diagonal copy of $E^r$ in a compact adelic set. Thus the finite sum of the displayed terms is the same for $G$ and $G'$. Once the trace on each group has been reduced to the irreducible-characteristic-polynomial kernel (the source assertion `EllTrace`), this proves equality of the geometric traces. To read off a single multiplicity one also needs the spectral calculation and separation for these tests. [Finite expansion][finsum] · [Termwise trace identity][finish] · [Assembly with the spectral side][sides]

The published local analytic inputs for this comparison are existence and the orbital-integral formula for normalized discrete-series pseudo-coefficients, and Harish–Chandra's discrete-series character formula. The comparison of their measures, the symmetry in the roots, the global norm-class compatibility and equality of the field terms are established above. The [simple trace proof](LOWER_ROW_SIMPLE_TRACE.md) supplies the reduction to this field kernel on the actual hosts. The [spectral extraction](LOWER_ROW_SPECTRAL_EXTRACTION.md) then applies to these matched traces.

[hyp]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AbelianVarietyTheory/Definitions/Divisors/HasTypeVec.lean#L35-L47
[data]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AbelianVarietyTheory/BlockTheory/TwistedDiscreteSeries/EllipticPartTestData.lean#L220-L239
[pol]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AbelianVarietyTheory/BlockTheory/TwistedDiscreteSeries/EllipticPartTestData.lean#L74-L159
[rat]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AbelianVarietyTheory/Proofs/TwistedOperators/RationalUnitaryClassesIffLocalClassFamilies.lean#L53-L117
[finite]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AbelianVarietyTheory/Proofs/DivisorProofs/StableOrbitalIntegralPreservedLatticeIsometry.lean#L44-L82
[ftest]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AbelianVarietyTheory/Proofs/DivisorProofs/TestFunctionsTransportLocalLatticeIsometries.lean#L148-L193
[arch]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AbelianVarietyTheory/Proofs/DivisorProofs/TraceEqXOfGeomExpansionX.lean#L61-L86
[realclass]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AbelianVarietyTheory/Proofs/DivisorProofs/CompactRealPlaceTorusClassesSignVectors.lean#L18-L30
[hchar]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AbelianVarietyTheory/PublishedTheorems/TwistedTraceFormula/DiscreteSeriesCharacter.lean#L174-L213
[weyl]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AbelianVarietyTheory/Proofs/DivisorProofs/FinsumDiscreteSeriesCharacterEqWeylCharacter.lean#L116-L144
[unit]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AbelianVarietyTheory/Proofs/TwistedOperators/EventuallyUnitaryTorusOrbitalClassTrivialLocal.lean#L29-L83
[norm]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AbelianVarietyTheory/Proofs/TwistedOperators/DetGramRatOneNeZero.lean#L376-L396
[glue]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AbelianVarietyTheory/Proofs/TwistedOperators/DetGramRatOneNeZero.lean#L475-L526
[unfold]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AbelianVarietyTheory/Proofs/TwistedOperators/IntegralCharpolyKernelEqStableOrbitalIntegrals.lean#L112-L138
[meas]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AbelianVarietyTheory/Proofs/DivisorProofs/TraceInputsImplyCuspidalTrace.lean#L105-L137
[finsum]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AbelianVarietyTheory/Proofs/TwistedOperators/EllipticPart.lean#L47-L92
[finish]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AbelianVarietyTheory/Proofs/DivisorProofs/TraceEqualityOfGeomExpansion.lean#L18-L49
[sides]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AbelianVarietyTheory/Proofs/DivisorProofs/TraceFormulaOfHyp.lean#L45-L62
[lab]: https://www.math.utah.edu/~ptrapa/src2006/labesse.pdf#page=31
