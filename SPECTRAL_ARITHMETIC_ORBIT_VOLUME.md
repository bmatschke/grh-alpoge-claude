# The term amplitude and stabilizer volume on the arithmetic row

Fix a supplied pair of words $u,u'$, a relevant term $t$ with nonzero Gram determinant, and the tied lattice model of that term. Let $r=r_S\ge1$, $s=r+1$, $m=2s$, $f=[F:\mathbf Q]$, $R=\operatorname{rd}(E)=2v$, and $b$ be the source scale. Write $Z$ for the rational cross Gram matrix of the two marked frames. At a real place let $d_{\tau,l}$ be its normalized absolute leading minor. The height appearing in the volume estimate is

$$
 S_C(Z)=\prod_\tau\prod_{l=1}^s\max(1,d_{\tau,l}/b^{Cm^2}),
 \qquad h_C(Z)=b^{C^2m^3f} S_C(Z)^4 ,
$$

where the first product ranges over every real place and $1\le l\le s$. If $T_u,T_{u'}\le b^{C_Tm}$, take $C_V=\lceil\max(C_T,0)\rceil+20$. On the original arithmetic quotient, with the supplied root measures, one has

$$
 a_t^2=V_t^2\prod_\tau\|J_{\tau,t}\|_{\rm HS}^2,
 \qquad 0<V_t\le h_{C_V}(Z)^{C_Vr^2}.                                \tag{1}
$$

The result applies to every permitted pair of words on the concrete tied construction. For a row with a term operator or measures specified independently, the identification with this construction is a hypothesis. On the cell with all blocks of length one, $V_t=1$ exactly. [Arithmetic height][h] · [Original amplitude][a] · [All-word volume theorem][vt]

## Which measure occurs in the term

Choose an arithmetic lift of $t$ and a Bruhat representative of its pair of frames. Write $R_t$ for the common real unipotent stabilizer and $\Gamma_t$ for its integral subgroup preserving the term lattice. Let $K_t$ be a measurable fundamental set of $\Gamma_t$ in $R_t$. The root-coordinate Haar measure prescribed by the representative is transported to the lift by conjugation. Call it $\mu_R$. Then $V_t=\mu_R(K_t)$. The model supplies this pin and a positive finite covolume at every relevant nonsingular term. [Definition on representatives][pin] · [Realization for positive-Gram lifts][jfact]

There are two normalizations in (1). With the unit root measure let $J^1_{\tau,t}$ be the physical orbital operator. Let $V_N(u)$ and $V_N(u')$ be the unipotent covolumes of the two fixed flags in their scale-one Bessel measures. Unfolding at the lift gives

$$
       a_t^2 V_N(u)V_N(u')=V_t^2\prod_\tau\|J^1_{\tau,t}\|_{\rm HS}^2. \tag{2}
$$

Indeed relevance makes the rank-one coefficient integrand invariant under the common stabilizer. Disintegrate first over $\Gamma_t\backslash R_t$ and then over $R_t\backslash G_\infty$. The first integration supplies $V_t$ in the amplitude. The finite character has modulus one. In the second integration the pinned stabilizer measure is the product of the local root measures. Uniqueness of quotient integration identifies the product orbital operator on the tensor of the compact types. In product orthonormal bases its Hilbert–Schmidt square is the product of the local squares. The local transport from a Witt frame to the physical Bessel coefficients carries a scalar at each place. The product of their squared moduli equals the squared global coefficient normalization times $V_N(u)V_N(u')$. This accounts for both fixed-flag volumes in (2). The large-gap coefficient convergence and the quotient integration identity give the distinguished orbital integrals used here. [Unfolding and finite character][unf] · [Hilbert–Schmidt product on quotient measures][HS] · [Exact product of the transport scalars][const] · [Their combination on the actual lift][jfact]

At scale one $V_N(u)=V_N(u')=R^{f(r^2+r/2)}$. At a nonzero term the source divides each of the $f$ local quotient measures by

$$
                   \vartheta=(V_N(u)V_N(u'))^{1/(2f)}.
$$

This divides their squared norm product by $\vartheta^{2f}=V_N(u)V_N(u')$ and gives (1). The fixed-flag calculation also shows that the required $\vartheta$ is in the permitted local measure window. In the zero-amplitude case (2) and positivity give a zero product at unit scale already, and the construction takes $\vartheta=1$. Thus the same equality holds even when some local factor vanishes. [Fixed-flag covolumes](SPECTRAL_STABILIZER_VOLUME.md) · [Change of local measure][change] · [Raw identity and conversion to the tied packet][tie]

## An integral cover for the stabilizer

In this argument $D_l$ denotes the **unscaled arithmetic** leading minor of $Z$. Set $d=D_s$, $G=d\bar d-T_uT_{u'}D_{s-1}\overline{D_{s-1}}$ and $P=\prod_{\tau,l}\max(1,|\tau D_l|)$. The standing frame and self-duality conditions put both complete frames in the integral lattice. Hence $Z$, $G$ and $d$ are integral. At a positive-Gram place $d\ne0$. The determinant of the Hermitian Gram matrix of the two complete frames together is $(-1)^s G$, so their span is nondegenerate. [Frame integrality and Gram determinant][int]

Take the Bruhat form $LwU$ of the signed Gram matrix. Its leading minors agree in absolute value with those of $Z$. Here $L,U$ are lower and upper unitriangular and $w$ consists of the nonzero antidiagonal blocks of the relative point. Its free root coordinates are exactly the pairs $i<j$ in a common block. At the arithmetic level a candidate action on the second frame is an upper unitriangular matrix $a$ with $ZaZ^{-1}$ lower unitriangular. The first frame must transform by $(Za^{-1}Z^{-1})^*$. These actions preserve the pairings and fix the terminal self-pairing forms. Extend by the identity on the perpendicular complement of the combined span. This is an integral unipotent isometry when $a-1$ has entries divisible by $Gd$. Indeed $dZ^{-1}$ is integral, hence both frame increments are multiples of $G$ when the second increment is a multiple of $Gd$. The inverse of the combined frame Gram matrix has denominator $G$. The orthogonal projection onto the span on an integral input therefore has coefficients in $G^{-1}\mathcal O_E$; composing with the frame increments makes the change to the input integral. The inverse change is integral by unipotence. The resulting isometry belongs to the two integral flag unipotents. [Congruence lifting on the actual lattice][lift]

The source chooses $I=(G^2d)$ for this congruence lattice, giving

$$
 N I=\prod_\tau |\tau G|^4 |\tau d|^2
       \le (1+T_uT_{u'})^{4f}P^{10}.
$$

Here $|\tau G|\le(1+T_uT_{u'})P_\tau^2$ with $P_\tau=\prod_l\max(1,|\tau D_l|)$. The lifting argument just given already works with $I=(Gd)$, and hence also gives the sharper bound $(1+T_uT_{u'})^{2f}P^6$. Either ideal suffices for (1). The absolute norms use two complex embeddings above each real place. [Source choice and the weaker divisibility it actually uses][ideal]

To see how the height enters, put $\rho=\sqrt{2f}R$ and $B_0=4^s(s!)^2\rho^{2s}$. Simultaneous approximation by $\mathcal O_E$ gives representatives of size at most $\rho$ at every embedding. Apply this successively to the two unitriangular matrices by integral row and column shears. The entries of their reduced representatives are at most $\rho$ in absolute value. In the middle block $w$, ratios of consecutive nonzero block-end minors give powers of its antidiagonal entries. Expansion of a cross minor by Cauchy–Binet therefore bounds every reduced matrix minor at $\tau$ by $B_0\prod_l\max(1,|\tau D_l|)\max(1,|\tau D_l|^{-1})$, using a factor one for a zero minor. The product of the reciprocal terms for any one nonzero minor is at most the product of the direct terms, since $\prod_\tau|\tau D_l|\ge1$. Thus $B=B_0^fP^2$ bounds the product of the local minor allowances. [Triangular reduction, minor comparison and product bound][red]

In the Lie algebra the integral matrices consist of strictly upper $x$ such that $(LwU)x(LwU)^{-1}$ is strictly lower. Conjugation by $U$ identifies this space with the free root coordinates. The integral Lie-lattice estimate gives an additive fundamental set of volume at most

$$
   \bigl(|\operatorname{disc}E|^{1/2}(4s^2)^fB^4\bigr)^{s^2}.
$$

Projecting onto free coordinates and selecting a nonsingular minor in the remaining linear equations bounds the lattice index by the norms of those equation minors; their determinant bounds use the matrix minors above. Restrict entries to $s! I$. The lattice index increases by at most $[(s!)^{2f} N I]^{s^2}$, by reduction of all $s^2$ entries modulo $s!I$. The factorial clears the denominators in the truncated exponential. Its image is contained in the integral congruence stabilizer. The nilpotent exponential and the successive root-coordinate reductions give a group covering set $\Omega$ of the same volume as the restricted additive fundamental set. This last step uses the triangular nilpotent group law; it does not require an additive parallelepiped to tile under group multiplication. [Integral Lie-lattice bound][lie] · [Congruence index, exponential and cover][exp]

With the source's particular ordered coordinates, put $n_i$ for the Bruhat block lengths, $a=\sum_i\binom{n_i}{2}$, and $e=\sum_i n_i(n_i^2-1)/6$. A root $(i,j)$ changes rational coordinates from physical coordinates by $R^{-(j-i)}$. Pinned Haar has factor $c=2/(Rg_0g_1)$ per complex physical root at each place. Hence in rational coordinates its density is **exactly** $c^{fa} R^{2fe}$. This follows by multiplying the planar Jacobian $R^{2(j-i)}$ and the pinned factor for every root. Permutations of places and the root sign changes preserve Lebesgue measure. In particular $c\le1$ and $e\le s^3$. The integral lifts above translate every stabilizer point into the inverse image of $\Omega$. Translating the intersections of this inverse image with arithmetic fundamental translates yields $V_t\le c^{fa}R^{2fe}\operatorname{vol}(\Omega)$ by countable additivity and Haar invariance. For singleton blocks there are no roots, the root chart is injective on the stabilizer, and its prescribed measure on the zero-dimensional coordinate space has total mass one. This proves the asserted exact value on the big cell. [Pinned root transformation][haar] · [Planar Jacobian][jac] · [Covering a fundamental set][pack] · [Injectivity of the stabilizer chart][inj]

To verify the exponent, write $c_T=\lceil\max(C_T,0)\rceil$, $n=c_T+20$, $S=S_n(Z)$. The native rank and field bounds give $b\ge2$, $R\le b$, $|\operatorname{disc}E|^{1/2}\le b^f$, $\rho\le b^{2s}$ and $1+T_uT_{u'}\le b^{(1+4c_T)s}$. The conversion between unscaled and scaled leading minors gives $P\le b^{(2+4n)s^3f}S$. Inserting these bounds, $B=B_0^fP^2$, and the source's larger $I$ in the cover estimate, then multiplying by $R^{2fs^3}$, gives

$$
 V_t\le b^{s^2 f[3+(14+16c_T)s+26s^2+(36+72n)s^3]+2fs^3}
                  S^{18s^2}.
$$

Indeed the index contributes $P^{10}$ and the Lie lattice contributes $P^8$ inside the $s^2$ power. For the smaller congruence ideal their combined power is $P^{14}$ instead. Since $s=r+1\le2r$, $n\ge20$ and $S\ge1$, the displayed bound is at most $b^{8n^3r^2fs^3}S^{4nr^2}=h_n(Z)^{nr^2}$. For example, the exponent of $b$ divided by $r^2fs^3$ is at most $318+352n\le8n^3$. Leading minors are invariant under the allowed double-coset changes of the second flag. Thus the calculation uses precisely the same $h_n(Z)$ when the lifted frame is replaced by the arithmetic term representative used for counting. [Numerical exponents][num] · [Normalized minors and actual host bounds][scale] · [Transfer to the counted representative][att]

Substitution in [the critical product on rows](SPECTRAL_CRITICAL_PRODUCT_ON_ROWS.md) supplies $h_{C_V}(Z)^{2C_Vr^2}$ in the squared term bound. The argument uses nonsingularity of the single term and imposes no condition on the rank of the difference of two labels in a collision. It therefore supplies the same term input for every collision corank to which that row bound applies.

[h]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Formalism/SharpRestriction/CuspSpanNormBounds/CntPartners.lean#L139-L150
[a]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Formalism/SharpRestriction/CuspSpanNormBounds/BruhatCellsKronecker/FamilyPacketOfEquivalentStatement.lean#L72-L77
[vt]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AbelianVarietyTheory/Proofs/FlagMeasures/StabiliserCovolumeRelevantTermLeHeightPow.lean#L25-L50
[pin]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Formalism/LocalToGlobal/SiegelLatticeTheory/FlagStabilizerTensors/LoopTerm.lean#L92-L118
[jfact]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AbelianVarietyTheory/Proofs/FlagMeasures/LocalBesselJFactorAllWordsOfGap.lean#L18-L66
[unf]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AbelianVarietyTheory/Proofs/FlagMeasures/NormalisedLiftAmplitudeEqCovolumeMulLocal.lean#L14-L30
[HS]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AbelianVarietyTheory/Proofs/FlagMeasures/RealOrbitalIntegralHsNormEqProdLocal.lean#L146-L218
[const]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AbelianVarietyTheory/Proofs/FlagMeasures/AmplitudeConstantEqProdCovolumes.lean#L26-L67
[change]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Formalism/LocalToGlobal/SiegelLatticeTheory/FlagStabilizerTensors/LoopTerm.lean#L250-L298
[tie]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Formalism/LocalToGlobal/SiegelLatticeTheory/FlagStabilizerTensors/LoopTerm.lean#L805-L850
[int]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AbelianVarietyTheory/Proofs/FlagMeasures/CongruenceStabUFromIntegralUnipotentIsometry.lean#L307-L352
[lift]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AbelianVarietyTheory/Proofs/FlagMeasures/CongruenceStabUFromIntegralUnipotentIsometry.lean#L364-L562
[ideal]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AbelianVarietyTheory/Proofs/FlagMeasures/CongruenceStabUFromIntegralUnipotentIsometry.lean#L725-L766
[red]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AbelianVarietyTheory/Proofs/FlagMeasures/CovolumeIntegralUnipotentStabilizerOfTerm.lean#L232-L341
[lie]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AbelianVarietyTheory/Proofs/FlagMeasures/GramUnipotentLieLatticeDomainVolumeBound.lean#L567-L785
[exp]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AbelianVarietyTheory/Proofs/FlagMeasures/CovolumeCongruenceStabiliser.lean#L296-L395
[haar]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AbelianVarietyTheory/Proofs/FlagMeasures/StabiliserHaarRootCoordinatesLeLebesgue.lean#L17-L58
[jac]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AbelianVarietyTheory/Proofs/FlagMeasures/MeasurePreimageReindexScaleComplexLe.lean#L55-L105
[pack]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AbelianVarietyTheory/Proofs/FlagMeasures/StabiliserCovolumeLeRootCoordinateCover.lean#L18-L103
[inj]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Formalism/LocalToGlobal/SiegelLatticeTheory/TraceIntegralEstimates/ChartCG.lean#L34-L58
[num]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AbelianVarietyTheory/Proofs/FlagMeasures/CovolumeIntegralUnipotentStabilizerOfTerm.lean#L345-L392
[scale]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AbelianVarietyTheory/Proofs/FlagMeasures/CovolumeIntegralUnipotentStabilizerOfTerm.lean#L563-L682
[att]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AbelianVarietyTheory/Proofs/FlagMeasures/StabiliserCovolumeRelevantTermLeHeightPow.lean#L76-L105
