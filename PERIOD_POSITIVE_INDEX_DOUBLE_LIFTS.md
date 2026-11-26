# The positive-index row pairs and their finite quotient measures

At every permitted positive index the ordered two-step unfolding retains an explicit upper Bessel period. On the untwisted reference tuple its two finite averages reduce to one pair of representatives, with the quotient-volume factors below. This uses the analytic row realization and the specified finite support and invariance laws.

First assume $m\ge4$ and put $j=m-4$. This is the pair immediately before the [terminal double lift](PERIOD_TERMINAL_ROW_DOUBLE_LIFT.md). The incoming Bessel index is one and the outgoing index is zero. At this pair the original row period unfolds to an ordered integral of an explicit definite-column function. At the reference tuple one can evaluate **both finite quotient integrals at a single pair of representatives** and calculate the multiplier. These assertions use the matched Weil splittings and row measures of the word.

## From the two row kernels to the upper restriction period

Write $A=X_j,\ S=X_{j+1},\ A'=X_{j+2}$ for the definite spaces, and $V_i=V_{j+i}$ for $0\le i\le2$. The residual spaces in the two specified Bessel decompositions have orthogonal splittings $A\perp L,\ A'\perp L'$, and the Jacobi datum has residual space $S$. In the second Bessel datum the Witt index parameter is zero, so the prescribed embedding gives $\alpha':U(A')\to U(V_2)$. Let $R_1\subset U(V_1)$ be the Fourier–Jacobi subgroup and $R_2\subset U(V_2)$ the Bessel subgroup of these data, using their adelic points below. Let $\mu_i$ be the two ambient row Haar measures and $\rho_i$ the prescribed subgroup measures. Write $d\dot h_i=d\mu_i/d\rho_i$ for the quotient measures on $R_i\backslash U(V_i)(\mathbb A_F)$. The arithmetic quotient $[A']=U(A')(F)\backslash U(A')(\mathbb A_F)$ inside the upper period carries its own definite measure $dz$. [One-step data and their volumes][iv-dat] · [Exact quotient assertions][iv-ord]

Take admissible row tests $\Phi_1,\Phi_2$, a continuous automorphic column input $\phi$, and a row input $F$ on $U(V_2)$. Assume rapid decay of $F$ and of the inner lift $\mathcal L_2^{\Phi_2}F$. These follow for the specified smooth cuspidal multiplicity maps once the upper row-map identity holds. For $g,h_1,h_2$ on the successive rows, let
$$
 \Xi_1=\mathrm{flat}_{BF}\bigl(\omega_1(g,h_1)\Phi_1\bigr),
 \qquad
 \Xi_2=\mathrm{flat}_{FB}\bigl(\omega_2(h_1,h_2)\Phi_2\bigr).
$$
Here the flat maps are the stated Bessel-to-Fourier–Jacobi and reverse Fourier transforms. Use the rational line map $\tau$ of this *interior* link. It satisfies $\tau\zeta'=-\zeta$ and $\tau^*H_L\tau=\xi_0\bar\xi_0 H_{L'}$, with positive sign in the Gram relation. With $k(w)={\rm ofAdj}_{L,S}(\tau w)$, the coupled test is
$$
 C_{g,h_1,h_2}(u,v)=
 \int_{\mathcal F_L}\Xi_2(v,w)\,\Xi_1(u,k(w))\,dw .                    \tag{1}
$$
The coordinates use the two orthogonal splittings. The integral uses the prescribed additive fundamental domain for the rational matrices in the oscillator space $WO(S,L')$, with covolume one. Write $\mathcal D^C$ for the two definite Weil lifts using $C$ and the original measures on $[A]$ and $[S]$, in that order from the input. For the bilinear Bessel period $\mathcal P_{1}$ at index one,
$$
 \mathcal P_{1}\bigl(\phi,R_g\mathcal L_1^{\Phi_1}\mathcal L_2^{\Phi_2}F\bigr)
  =\int_{R_1\backslash U(V_1)(\mathbb A_F)}
       \left[\int_{R_2\backslash U(V_2)(\mathbb A_F)}
        \int_{[A']}(\mathcal D^{C_{g,h_1,h_2}}\phi)(z)\,
                         F(\alpha'(z)h_2)\,dz\,d\dot h_2\right]d\dot h_1 .    \tag{2}
$$
This is an ordered identity: the bracket is an absolutely integrable quotient function and the inner quotient integral exists for every outer representative in the stated unfolding model. [Line map and the two successive transforms][iv-link] · [Positive Gram relation][iv-gram] · [Original two-step unfolding][iv-unf]

**Proof.** Unfold the first Bessel period to the selected rational-frame orbit, integrate on the Fourier–Jacobi stabilizer quotient, and apply the Fourier–Jacobi-to-Bessel formula to the translated second test at this fixed outer point. The one-edge orbit bounds give the stated order of absolute integrability. This gives an upper Bessel period with column input obtained by applying the two flat transforms successively and with row input $R_{h_2}F$. At fixed $h_1,h_2$, split both residual Weil actions into the definite space and the complementary line. The two line actions have the same line splitting character. The linked weighted adjoint carries one to the conjugate of the other, so unitarity preserves their pairing on $\mathcal F_L$. The conjugation in the first transform and the star in that pairing cancel. Passing the definite actions through the line integral gives the two-variable test (1) with scalar one. The only reordering here interchanges $dw$ with integration over the definite quotient $[A]$. Their fundamental domains have finite measure, the column is bounded on $[A]$, and the two theta factors are bounded uniformly in $w$ and the input representative for fixed remaining arguments. Finally the index-zero Bessel flag is trivial with mass one, so the upper period is the $dz$ integral in (2). No interchange of the two noncompact quotient integrals enters. Finite chart traces give (2) term by term with their original coefficients. [Orbit bounds in both directions](ROW_MIXED_CELL_UNFOLDING.md#absolute-integrability-in-the-prescribed-order) · [Pairing of the line actions][iv-pair] · [Definite integral interchange][iv-fub] · [Index-zero period][iv-zero] · [Finite trace on this row][iv-sum]

## Exact finite evaluation at the reference tuple

Use the prescribed row tests attached to $P_1,P_2$, the permitted ramified input and frame, and $F=G(v)$ from the indicated smooth multiplicity space. Let $J(h_1,h_2)$ be the inner $dz$-integral of (2), summed over the incoming charts and the finite translations $g$ with their actual trace coefficients. Fix real row elements $a_1,a_2$, and denote by $b_1,b_2$ the two registered finite base moves on $V_1,V_2$. Suppose the finite tests and row readings have the prescribed moved-vacuum shapes, the good-place support and invariance laws, and the fixed-place support and invariance laws. These give the finite row-integrand laws cited below and are substantive inputs for identifying a chosen arithmetic member. They can be used before evaluating the fixed-place contraction or applying the level-prime correction.

Take the reference tuple with its conductor set identified with the ramification of its reference character. That character is trivial, so the set $Q$ of twist places is empty. Let $H_i=U(V_i)(\mathbb A_{F,f})$ and $R_i^f=R_i\cap H_i$. Use the prescribed finite Haar measures $\mu_i^f,\rho_i^f$. Let $K_i\subset H_i$ use the word's lattice stabilizer outside its fixed-type places and its specified subgroup $J_G(j+i)$ at those places. It is compact open; its intersection with the closed $R_i^f$ is compact open there. Put
$$
 \lambda_i=\frac{\mu_i^f(K_i)}{\rho_i^f(R_i^f\cap K_i)}\quad(i=1,2).
$$
Both are positive finite real numbers. For every fixed $a_1,a_2$ we obtain
$$
 \boxed{\displaystyle
 \int_{R_1^f\backslash H_1}\!
 \left[\int_{R_2^f\backslash H_2}J(a_1 q_1,a_2 q_2)\,d\dot q_2\right]d\dot q_1
   =\lambda_1\lambda_2\,J(a_1 b_1,a_2 b_2) .}                    \tag{3}
$$
In particular the value on the right still includes the actual row tests, chart weights and upper row translate. [Reference conductor][iv-ref] · [Compact levels and the two ratios][iv-vol] · [Moved integral before and after the base translations][iv-move]

**Proof.** Center the integrand by setting $H(q_1,q_2)=J(a_1q_1b_1,a_2q_2b_2)$. The moved-vacuum formula expresses $H$ as ${\rm sc}_{t,j}{\rm sc}_{t,j+1}$ times the standard integrand with row input $R_{a_2b_2}F$. The support and invariance statements apply to this centered integrand. It is left $R_i^f$-invariant and right $K_i$-invariant in each coordinate. A nonzero value requires $q_1\in R_1^f H_{1,Q} K_1$, where $H_{1,Q}$ is the subgroup of the finite adelic group supported on $Q$; for $q_1=1$ a nonzero value requires $q_2\in R_2^f H_{2,Q}K_2$. Both groups supported on $Q=\varnothing$ are the identity. The finite-cover condition at twist places itself is automatic in this case: take the trivial group, its identity representative and scalar one. It follows, including when $H(1,1)=0$, that
$$
 H(q_1,q_2)=
 \mathbf1_{R_1^fK_1}(q_1)\mathbf1_{R_2^fK_2}(q_2)\,H(1,1).
$$
Indeed outside the first cell everything vanishes; inside it reduce the first argument to $1$ by invariance, then apply the second support statement and the second invariance. On the quotient the image of $K_i$ has mass $\lambda_i$: integrate the indicator of $K_i$ using the ambient/subgroup quotient formula. On that image its fiber has mass $\rho_i^f(R_i^f\cap K_i)$, and the integral on the group is $\mu_i^f(K_i)$. Integrate the second indicator first and the first indicator second. Right translation by the finite $b_i$ preserves the quotient integrals. This proves (3) without dividing by a period or a trace coefficient. [Actual invariances and support][iv-cell] · [Moving the finite representatives][iv-move] · [One-coset integration][iv-mass]

## What changes at a twisted tuple

For $Q\ne\varnothing$, the two surviving groups supported on $Q$ generally have several contributing cells. Normalize Haar on each of those two groups and on its stabilizer so that their respective lattice compact opens have mass one. The same quotient calculation away from $Q$, first for the inner integral and then for its outer integral, multiplies the remaining ordered integral on $Q$ by $\lambda_1\lambda_2$. The $K_i$ used in these ratios include the standard $Q$-lattice opens. Thus the ratios are the word's two full finite volume ratios even as $Q$ changes. The source proves the outer invariance by uniqueness of the already integrated inner value and derives its support from that of a nonzero inner integrand. [Normalization at $Q$][iv-qat] · [The two successive quotient reductions][iv-quot]

Suppose the local interior chart identities at $Q$, the fixed-type value, the level-prime correction and the matching finite row and column readings are available on this tuple. Then the left side of (3) equals
$$
 c^V_{t,j}\,
  \mathcal P^F_{t,j+2,0}\!
   \left(D^{C_{a_1,a_2}}_{t,j}\,R_t(S_{t,j}\psi;y),\
             R_{a_2}F\right),\qquad
 c^V_{t,j}=\lambda_1\lambda_2\,{\rm sc}_{t,j}{\rm sc}_{t,j+1}
        c_{G,j}c_{T,t,j}
       \prod_{p\ {\rm twist}}\bigl({\rm idx}_{p,j+1}{\rm idx}_{p,j+2}\bigr)^{-1}.
                                                                    \tag{4}
$$
Here $R_t(\psi;y)$ is the reading in the permitted charts and $D_{t,j}$ inserts the prescribed two column operations and sums over intermediate charts. The corrected test $C_{a_1,a_2}$ is common to tuples for this real pair and these two polynomials. Apply the two flattenings and (1) to the common vacuum vectors at real pairs $(1,a_1)$ and $(a_1,a_2)$, then apply the fixed two-variable correction. Independence of the flat maps on the permitted tests gives the same function in every tuple. The two row-test scalars follow from moving the finite base points. The normalized $Q$-comparison gives the product of reciprocal indices, including the restored chart traces; the disjoint fixed-type and level-prime comparisons give $c_G,c_T$ and move $S_{t,j}$ to the incoming reading. The upper trace then combines with $R_{a_2}F$, since the fixed finite move commutes with the real element. This proves (4) under the stated local comparisons. It is a value at **fixed real row arguments**. To pass homogeneous relations through the real integrations one uses their vanishing for every such pair together with the ordered quotient argument, with the original real Haar measures. [Fixed-real-pair statement][iv-goal] · [Detailed finite reduction and upper trace at this stage][iv-value] · [Actual geometric scalar][iv-scalar] · [Passage of homogeneous relations through real integration][iv-rel]

Equation (2) identifies the integral before any finite-place value calculation. Equation (3) settles the finite average at the reference once its stated support, invariance and row matching hold. Extending (4) unconditionally to the selected twisted members still requires their matched split twist chart identities, the fixed-type and level-prime values, and their arithmetic row readings. The two row-map scalars $c^I_{t,j}c^I_{t,j+1}$ enter when replacing the two analytic lifts in (2) with their arithmetic row maps. They are separate from the finite Haar factor in (3). [Arithmetic row normalization][iv-rnorm]

## The recurrence at every interior index

Let $m\ge4$ be even. For each even $j$ with $0\le j\le m-4$, put $\sigma=(m-j-4)/2$. The source condition $j+2(\sigma+1)+2=m$ then holds. The incoming Bessel and intermediate Fourier–Jacobi data have index $\sigma+1$, and the outgoing Bessel datum $B'$ on $V_{j+2}$ has index $\sigma$. There are $m/2-1$ interior pairs. For $m=2$ there are none. The terminal pair $j=m-2$ uses its separate terminal law. [Arbitrary-index ordered step][iv-ord] · [Tuple indices and finite trace][all-trace]

Use the corresponding hypotheses, row Haar measures and tests of (1)–(2) at this $j$. Write $R_1$ for the adelic Fourier–Jacobi subgroup at $j+1$, $R_2$ for the adelic Bessel subgroup at $j+2$, $G_i=U(V_{j+i})(\mathbb A_F)$, and $d\dot h_i=d\mu_i/d\rho_i$ for the corresponding quotient measures. With the coupled test $C=C_{g,h_1,h_2}$ from (1), the index-dependent form of (2) is
$$
 \mathcal P_{j,\sigma+1}(\phi,R_g\mathcal L_1^{\Phi_1}\mathcal L_2^{\Phi_2}F)
 =\int_{R_1\backslash G_1}\left[\int_{R_2\backslash G_2}
   \mathcal P_{j+2,\sigma}(\mathcal D^{C}\phi,R_{h_2}F)\,d\dot h_2\right]d\dot h_1 .
$$
For clarity, let $N'$ be the flag unipotent of $B'$, $\alpha'$ the specified embedding of $U(X_{j+2})$ into $G_2$, and $\psi_{B'}(n)$ its Bessel character with source parameter $1$ and its marked vector. Then the inner period is
$$
 \int_{[X_{j+2}]} (\mathcal D^{C}\phi)(z)
   \left[\int_{[N']}F(n\alpha'(z)h_2)\,\overline{\psi_{B'}(n)}\,dn\right] dz .
$$
Here $[N']=N'(F)\backslash N'(\mathbb A_F)$ has mass one, and $dz$ is the given definite quotient measure. For $j\le m-6$ the upper index is positive and the character integral remains in the formula. The special case $j=m-4$ has trivial $N'$. [Flag measure, character, multiplication order and absolute convergence][all-flag]

**Proof.** The two one-step unfoldings and their linked intermediate Jacobi period hold for every $\sigma$. Rapid decay of $\mathcal L_2^{\Phi_2}F$ gives an integrable outer quotient function. For each outer representative, rapid decay of $F$ gives an integrable inner quotient function with value equal to that outer function at this representative. The expression for $\mathcal D^{C}$ follows from the arbitrary-index contraction, with $\tau\zeta'=-\zeta$, positive Gram factor $\xi_0\bar\xi_0$ and the same line splitting character on both edges. The coupling in (1) remains bilinear with scalar one. The character conjugation displayed above belongs to the upper period. With the standard additive character, continuous automorphy of its two inputs gives convergence of the two flag-period integrations by compactness modulo rational points. Applying this calculation to each term in the finite incoming trace retains every original coefficient. [Two-step proof][iv-unf] · [Arbitrary-index contraction][all-contr] · [Gram sign][iv-gram] · [Assembly of the finite trace][iv-sum]

At the reference tuple, let $J_j$ denote this upper Bessel period summed with its actual incoming trace coefficients as in (3). Fix $a_1,a_2$ and assume the moved-vacuum, admissible row, support and invariance laws stated there at these two edges. With $H_i=U(V_{j+i})(\mathbb A_{F,f})$, $R_i^f=R_i\cap H_i$, and $b_i,K_i$ the registered finite base moves and levels at this $j$, one has
$$
 \int_{R_1^f\backslash H_1}\left[\int_{R_2^f\backslash H_2}J_j(a_1q_1,a_2q_2)\,d\dot q_2\right]d\dot q_1
 =\prod_{i=1}^{2}\frac{\mu_i^f(K_i)}{\rho_i^f(R_i^f\cap K_i)}\ J_j(a_1b_1,a_2b_2).
$$
Indeed the proof of the centered support and invariance laws takes the same $j,\sigma$ and uses precisely the index-$\sigma$ Bessel subgroup in its second coordinate. Since $Q=\varnothing$, reducing the first argument to $1$ leaves a single possible second cell. Integrating their indicators in order gives the two displayed quotient masses, including when the representative value vanishes. This proves the reference finite calculation and the ordered analytic recurrence at all indicated ranks on matched data. Comparing the representative values with the prescribed arithmetic upper readings, obtaining the twisted chart, fixed-type and level-prime values, and inserting the two arithmetic row-map scalars still require their respective identities. Multiplying the single-pair factors along a deployed family also requires verifying the hypotheses at each stage for its actual descended column and row inputs. [Finite base moves][iv-move] · [Index-dependent support and stabilizers][iv-cell] · [Tuple comparison after the local readings][iv-goal]

[iv-dat]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AbelianVarietyTheory/Definitions/LatticeFrames/IsThetaFam.lean#L18-L67
[iv-ord]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AbelianVarietyTheory/Definitions/LatticeFrames/IsQuasiFam.lean#L77-L87
[iv-link]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AbelianVarietyTheory/Definitions/LatticeFrames/IsThetaFam.lean#L116-L136
[iv-gram]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AbelianVarietyTheory/Proofs/DecoratedLatticeProofs/BesselLineLinkGramSimilitudeBijective.lean#L41-L65
[iv-unf]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AbelianVarietyTheory/Proofs/DecoratedLatticeProofs/BesselDoubleStepUnfoldingOfUnfoldingsAndLink.lean#L32-L56
[iv-pair]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AbelianVarietyTheory/Proofs/DecoratedLatticeProofs/WeilDatumProductCompatibility.lean#L92-L143
[iv-fub]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AbelianVarietyTheory/Proofs/DecoratedLatticeProofs/DoubleStepEqTwoThetaColumnLifts.lean#L95-L145
[iv-zero]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AbelianVarietyTheory/Proofs/DecoratedLatticeProofs/DoubleLiftPeriodRankZeroFubiniCompactQuotient.lean#L20-L53
[iv-sum]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AbelianVarietyTheory/Proofs/DecoratedLatticeProofs/BesselPeriodDoubleStepIteratedQuotientIntegral.lean#L60-L110
[iv-ref]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Formalism/LocalToGlobal/NumberFieldFamilies/RamifiedPrimesTrivialTuple.lean#L41-L75
[iv-vol]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AbelianVarietyTheory/Definitions/LatticeFrames/PlaceLaws.lean#L97-L115
[iv-move]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AbelianVarietyTheory/Proofs/DecoratedLatticeProofs/SeeSawIteratedIntegrandVacuumFormBasePoints.lean#L24-L81
[iv-cell]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AbelianVarietyTheory/Proofs/DecoratedLatticeProofs/SeeSawDoubleStepFiniteIntegralCollapseTwistPlace.lean#L38-L105
[iv-mass]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AbelianVarietyTheory/Proofs/DecoratedLatticeProofs/QuotientIntegralOneDoubleCosetEqMulValue.lean#L7-L79
[iv-qat]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AbelianVarietyTheory/Definitions/LatticeFrames/PlaceLaws.lean#L28-L30
[iv-quot]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AbelianVarietyTheory/Proofs/DecoratedLatticeProofs/SeeSawDoubleStepFiniteIntegralCollapseTwistPlace.lean#L125-L195
[iv-goal]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AbelianVarietyTheory/Definitions/LatticeFrames/ValLastX.lean#L184-L193
[iv-value]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AbelianVarietyTheory/Proofs/DecoratedLatticeProofs/SeeSawFiniteIntegralsDoubleStepValue.lean#L93-L174
[iv-scalar]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AbelianVarietyTheory/Proofs/DecoratedLatticeProofs/TrueGeometryFamilyInvariance.lean#L83-L92
[iv-rel]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AbelianVarietyTheory/Proofs/DecoratedLatticeProofs/SeeSawPeriodsLinearRelationsDoubleStep.lean#L86-L116
[iv-rnorm]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AbelianVarietyTheory/Proofs/DecoratedLatticeProofs/SeeSawDoubleStepLinearRelationsPeriods.lean#L94-L121
[all-trace]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AbelianVarietyTheory/Definitions/LatticeFrames/ValLastX.lean#L119-L135
[all-contr]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AbelianVarietyTheory/Definitions/LatticeFrames/IsQuasiFam.lean#L93-L108
[all-flag]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AbelianVarietyTheory/Proofs/DecoratedLatticeProofs/DoubleThetaLiftValueBilinear.lean#L31-L74
