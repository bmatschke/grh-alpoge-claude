# From the real-place estimates to the norm of one arithmetic term

To multiply the [four local amplitude estimates](SPECTRAL_ANGULAR_FROM_ORDINARY_AMPLITUDE.md), the ordinary squared bound needs a comparison between the product of critical levels and the dimension ratio on its word. This comparison is a scalar calculation on the actual genus masses and the two split levels. The calculation below keeps the small Euler factors. The only direction needed for the ordinary row costs at most $\exp(4f2^{-k})$.

## Critical product and the exact dimension ratio

Fix a word with level $T$. Write $k$ for the column rank, $r$ for the isotropic rank, $m=2r+2$, $n=k+m-1$, $f=[F:\mathbf Q]$, $v=\mathrm{rd}(E)/2$, and $g=g_0g_1$. Write $d_u^S$ for the arithmetic column dimension and $D^\star$ for the target size. Put $P_u=\prod_\tau(T_{{\rm crit},\tau}(u)/T)^k$, and denote the $j$th special-value factor of the standard unitary mass ratio by $L_j>0$. Use the standard consecutive mass ratios, the split-level counts and the source's comparison of $d_u^S,D^\star$ with these masses. Then
$$
 \frac{D^\star}{d_u^S}=P_u E_T,\qquad
 E_T=\prod_{j=k+1}^n L_j
       \prod_{i=0,1}\prod_{j=k+1}^n(1-g_i^{-j})^f
       (1-T^{-k})^{-f}.                                             \tag{1}
$$
Here $T,g_0,g_1\ge2$ and $k\ge2$. With $0<L_j$ and $|\log L_j|\le f\log\zeta(j)$, this implies
$$
 |\log E_T|\le8f2^{-k},\quad
  P_u^{-1}=E_T\,d_u^S/D^\star\le e^{4f2^{-k}}d_u^S/D^\star.          \tag{2}
$$
For example $f\le k$ eventually makes the last factor $1+o(1)$ uniformly over the words. Both estimates use positive real factors.

**Proof of (1).** Put $F_h=\prod_{a=0}^{h-1}a!$, and let $M_j$ be the standard mass in rank $j$. Its ratio to $M_{j-1}$ equals $[((j-1)!)(v/\pi)^j]^f\,|d_F|^{-1/2}L_j$ with $|d_F|=(2v)^f$ for this host. The split row and column index ratio at a single residue cardinality $q=g_i$ equals
$$
 q^{km+m(m-1)/2}\prod_{j=k+1}^n(1-q^{-j}).
$$
Indeed $|\mathrm{GL}_h(\mathbf F_q)|=q^{h^2}\prod_{a=1}^h(1-q^{-a})$. The common lower-rank factors cancel. The prescribed unipotent denominators leave $n^2-k^2-r(2k+2r+1)=km+m(m-1)/2$ in the exponent. Each of the two levels occurs at $f$ split places. The arithmetic counts give $D^\star=M_n\,\mathrm{idx}_{\rm row}\prod_\tau d_{\sigma,\tau}$ and $d_u^S=M_k\,\mathrm{idx}_{\rm col}\prod_\tau[\mathrm{Vand}(u_\tau)/F_k]\,(T^k-1)^f$, with $d_{\sigma,\tau}$ the specified discrete-series degree in the arithmetic normalization. Multiply the consecutive ratios and put $(T^k-1)^{-1}=T^{-k}(1-T^{-k})^{-1}$. The factorials give $(F_n/F_k)F_k=F_n$ at each label and $\sum_{j=k+1}^n j=(m-1)k+m(m-1)/2$. The remaining factor at that label is exactly $(T_{{\rm crit},\tau}/T)^k$ by the [critical-level formula](SPECTRAL_ORDINARY_SQUARED_AMPLITUDE.md#the-section-mass-in-the-original-units). This gives (1). [Actual word and split index comparisons](https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AbelianVarietyTheory/Proofs/FlagMeasures/SmallOnUnivUnconditional.lean#L103-L145) · [Mass, dimensions and critical-power comparisons](https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AbelianVarietyTheory/Proofs/FlagMeasures/SmallOnUnivUnconditional.lean#L146-L211)

**Proof of (2).** For $j\ge3$, the integral test gives $\log\zeta(j)\le\zeta(j)-1\le2^{-j}+2^{1-j}/(j-1)\le2^{1-j}$. Sum over $j>k$ to bound the logarithm of the positive $L$-product in absolute value by $2f2^{-k}$. The logarithms of the two split-level products are nonpositive, with combined absolute value at most $4f2^{-k}$ by $-\log(1-x)\le2x$ for $0\le x\le1/2$. The last factor has log between zero and $2f2^{-k}$. Adding gives the two-sided bound, and discarding the nonpositive factors gives the sharper upper bound. In the source's relative-error convention one may take $\delta=e^{8f2^{-k}}-1$. The identity for $P_u^{-1}$ only needs the sharper upper bound. [Scalar contract and its zeta error](https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Formalism/HermitianCurvature/StatementSz.lean#L142-L156)

For the actual split levels $g_0,g_1\ge4$ and $T\ge3$, one can use the sharper two-sided bound $|\log E_T|\le(5/2)f2^{-k}$. Indeed the positive terminal term divided by $f2^{-k}$ is at most $(2/3)^k/(1-3^{-k})\le1/2$. The absolute contribution from both split levels divided by the same quantity is at most $2(1/2)^k/[3(1-4^{-(k+1)})]<1/2$, by summing the two geometric series. Combine each sign with the $L$-product bound.

The identified dimension is exactly the dimension of the original $\mathrm{Mu}_0$ space. On a tied admissible member the column class-number formula, its marked level identification and the row mass identity supply the two dimension comparisons, for the sufficiently large split type primes and split $T$ in the source. This gives (1) on those data with no class-counting error. If a smaller theta image is used in its place, the upper bound in (3) would require an upper bound on the ratio of the original dimension to that image dimension. [Original column space](https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Formalism/LocalRingCardinality/RhoDetPrimeEqMuTildeMulChiPow.lean#L342-L347) · [Rank comparison for admissible members](https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AbelianVarietyTheory/Proofs/DecoratedLatticeProofs/AdmissibleRanksAllMembers.lean#L38-L68)

## One relevant term with nonzero Gram determinant

Let its reduced Gram label be $Z$. Write $n_\tau$ for the local normalizer $\eta_\tau G_\tau^k$ and $n_Z=\prod_\tau n_\tau$. Assume the term's two local flags and its quotient measures are those of the local calculations. Let $V_t>0$ be its arithmetic orbit-volume factor, and suppose its amplitude satisfies the squared factorization $a_t^2=V_t^2\prod_\tau\|J_{\tau,t}\|_{\rm HS}^2$. Let $d_u$ denote the compact dimension of the incoming word and use the Weyl dimension comparison $d_u=\prod_\tau\dim W_\tau$. Then for $0\le q\le C_{\rm pr}km^2$ the ordinary part of the local result gives
$$
 \frac{n_Z a_t^2}{d_u}
 \le V_t^2\,\Gamma S_Z^{C_2m^2-2q/(r+1)}
              e^{4f2^{-k}}\frac{d_{u'}^S}{D^\star}.                    \tag{3}
$$
Indeed multiply the nonnegative inequalities at all real places. The product of the sizes is $S_Z$, the product of the losses is at most $\Gamma S_Z^{C_2m^2}$ by the [loss calculation](SPECTRAL_REAL_LOSS_PRODUCTS.md), and the remaining critical power is $P_{u'}^{-1}$. Apply (2) on the outgoing word. In particular a bound $V_t\le h_Z^{C_Vr^2}$ supplies exactly the row-height factor $h_Z^{2C_Vr^2}$ in the ordinary term estimate. The critical-scale lower bound at a single place used for the angular inequality and this product comparison have different proofs. [Original product, norm factorization and volume insertion](https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Formalism/SharpRestriction/CuspSpanNormBounds/CayleyDegreeNondegeneracy/RowsTrm.lean#L324-L387)

For application on a selected family, (1) uses the host's standard mass law and the exact identification of its marked dimensions with $D^\star,d_u^S$. Equation (3) also requires the factorization in the actual term measures and its orbit-volume estimate. After these comparisons the single moment used in the [higher-corank summation](SPECTRAL_HIGHER_CORANK_MASSES.md) lies in the local range, since the specified integer is at most $(9c+3)km^2$ at the usual threshold. [Counting moment and its threshold](https://github.com/rh-lean-roadmap/rh-lean-roadmap/blob/dc5594a62bb2b94139788df817db693cd939a046/docs/src/book/main.tex#L16572-L16593)
