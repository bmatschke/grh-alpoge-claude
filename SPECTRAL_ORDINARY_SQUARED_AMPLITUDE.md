# The ordinary squared amplitude and the mass of its real section

Fix one real place and two supplied words. Write $s=r+1=m/2$, $N=k+2r+1$, $R=2v=\mathrm{rd}(E)$, $g=g_0g_1$, $d=\dim W$, $d'=\dim W'$, and $G=d_s^2-TT'd_{s-1}^2>0$ for the real Gram factor. The $d_l$ are absolute leading cross minors. Put $\eta=(e\pi/(g^mTkv))^k$, $t'=T_{\rm crit}(u',\tau)/T'$ and let $L_\tau$ be the [ordinary real loss](SPECTRAL_REAL_LOSS_PRODUCTS.md). The argument gives the ordinary, unweighted local target
$$
                  \eta G^k\|J_\gamma\|_{\rm HS}^2/d
                       \le L_\tau(t')^{-k} .                            \tag{1}
$$
This includes every positive-Gram cell with $d_{s-1}=0$, for both equal and different compact weights. It uses the specified intermediate wave-shortening, compact-type contraction and terminal-minor expansion estimates in the v38 Roadmap proof of B8.10hb. That proof is presented there as an outline with links to the corresponding formal arguments. The deduction below takes those intermediate assertions as inputs, gives their specialization at minor exponent zero, and calculates the real section normalization. The printed final bound $b^{Cm^5}$ of B8.10hb by itself does not imply (1). [Original normalized target][target] · [Roadmap theorem and hypotheses][theorem]

## The section mass in the original units

Let $M$ be the source's big-cell integral of $\|J\|_{\rm HS}^2$ with weight
$$
 w(c,\zeta)=\prod_{a=0}^{r-1}|c_a|^{2(2(r-a)+k-1)}
              (|\zeta|^2-TT')_+^{k-1}
$$
against ordinary product planar Lebesgue measure. On this big cell the common unipotent stabilizer is trivial and the quotient for $J$ is the input Haar measure $dg$. Put $d_{\rm form}=\mathrm{deg}(A)=d_\sigma^{\rm arith}$, the actual input degree, and $V_j=(2\pi)^{j(j+1)/2}/\prod_{a=0}^{j-1}a!$. For unipotent Haar density $\kappa=\theta R^{-rk}$, one has the explicit estimate
$$
              M\le \frac{dd'(TT')^k}{2^s}
                \frac{V_N V_{k-1}}{d_{\rm form} V_k^2}
                \frac{\theta^2}{R^{2rk}} .                            \tag{2}
$$

For the normalization in (2), let $c$ be the density of $dg$ in the source's Euclidean Lie coordinates, and $d_\sigma$ its discrete-series formal degree. The compact-dual scale tie gives $d_\sigma=d_{\rm form}/(cV_N)$. In the disintegration of $dg$ along the two Bessel groups, the quotient measure on the diagonal section is $\alpha w(c_a,\zeta)\,d^{2r}c_a\,d^2\zeta$ with
$$
                    \alpha=\frac{c\,2^s V_k^2}{V_{k-1}(TT')^k\kappa^2}.
$$
The two unipotent integrations account for $\kappa^{-2}$. The Bruhat-coordinate Lebesgue Jacobian in the input Frobenius metric has constant $2^r$, obtained from the differential at the opposite Weyl element. The paired equal-norm coordinates for the $r$ diagonal complex directions contribute a real determinant two each; the two nilpotent and the middle directions are isometric blocks. The terminal $U(k,1)$ polar measure, with both compact Haar measures probabilities, contributes $2V_k^2/(V_{k-1}(TT')^k)$ and the displayed radial power $k-1$. In that calculation the radial coordinate is the pairing of the original negative vectors, rescaled from a unit pair by $\sqrt{TT'}$. Lebesgue area and the $k-1$ radial powers together produce $(TT')^{-k}$. [Actual section definition][section] · [Differential and Bruhat Jacobian][jac] · [Full double-coset disintegration][dis] · [Degree and density with this Haar measure][constants]

The Hilbert–Schmidt integral on the latter double quotient satisfies $\alpha M\le dd'/d_\sigma$. Here are the normalizations in the Schur argument. Choose the [detecting coefficient](SPECTRAL_ZERO_PENULTIMATE_CONVERGENCE.md) with $\langle L(v),\xi\rangle=\langle L'(v'),\xi'\rangle=1$. On every generic section point its orbit integral $\mathcal O$ satisfies $\|J\|_{\rm HS}^2=dd'\|\mathcal O\|_{\rm HS}^2$. To bound the squared integral of $\mathcal O$, truncate the two period integrals to Følner sets in the Bessel groups (compact extensions of nilpotent groups). Disintegrate the square of the truncated integral over $G$, dividing by the product of the two Følner volumes. On a generic orbit this amounts to averaging the squared truncated integral over translations of the truncations. Expand its square: the two normalized intersection volumes are bounded by one and converge to one at each fixed translation. The original large-gap decay makes the single orbit integral absolutely integrable there, so its squared double integral controls this convergence. Fatou gives the upper bound by the limit of the integrals over $G$. In that integral ordinary Schur orthogonality gives $d_\sigma^{-1}$ times the two normalized one-sided square averages. Their intersection-volume limits give respectively $\langle\xi,L(v)L(v)^*\xi\rangle=1$ and its primed analogue. This proves the asserted upper bound. The [absolute convergence argument](SPECTRAL_ZERO_PENULTIMATE_CONVERGENCE.md) also justifies the coefficient identity on the individual boundary orbits. Substituting $\alpha$ and $d_\sigma$ gives (2). [Fatou and Schur integrals][fatou] · [Witness normalization][schur]

In fact (2) leaves only a factor of order $b^{O(m^2)}$ at the target critical scale. Write $h_m=m(m-1)/2$. Then
$$
 \frac{\eta(t')^k}{d}\,M
 \le\left(\frac ek\right)^k(k-1)!\,
       \frac{\theta^2(Rg)^{h_m}}{2^s R^{(m-1)/2}} .                  \tag{3}
$$
To check it directly, the source definition gives
$$
 T_{\rm crit}^k=(\pi/v)^{-((m-1)k+h_m)}
 R^{-(m-1)/2}g^{km+h_m}
 \frac{d_{\rm form}\prod_{a<N}a!}{\operatorname{Vand}(u')}.
$$
Weyl's dimension formula gives $d'=\operatorname{Vand}(u')/\prod_{a<k}a!$. Substitute both expressions and $V_j$ into (2). The factors $(TT')^k$, $d_{\rm form}$, both Vandermondes and $g^{km}$ cancel against those in $\eta(t')^k/d$. The remaining factorial is $(k-1)!$, and the surviving $R,g$ powers are exactly those in (3). Since $\log((k-1)!)\le\int_1^k\log x\,dx$, the first factor is at most $e$. Also $|\log_b\theta|\le C_1m^2$ and $R,g$ are bounded by fixed powers of $b$. This proves the stated section allowance without any new unknown proportionality scalar. [Definition of critical power][critical] · [Volume and factorial cancellation][vol]

## Specializing the wave estimate to exponent zero

Use $B=b^{C_\beta}$ as a single envelope for the weights, splitting scale and character transport, allowing terminal heights up to a fixed $O(m)$ power of this envelope, with fixed $C_\beta$ large enough. Thus a factor $B^{O(m^4)}$ is admissible in (1). In the unit-character model let $\widetilde E(F;\gamma)$ be the Roadmap tower's point-weighted squared energy and $\widetilde I(F)$ its integral on the singleton section. The coefficient $F$ is the detecting compact-finite coefficient above, or its common nonzero scalar multiple. The following are the precise intermediate estimates being used.

* In the distinct-compact-weight case take $p_0=2s$. The wave argument applied to $H=G^{p_0}F$ gives $\widetilde E(H;\gamma)\le (C_2\Lambda^2)^s\widetilde I(H)$, where $1\le\Lambda\le B^{6m}$. This follows after both cutoffs have been removed, and hence holds on a merged terminal block. Its hypotheses are the signed endpoint bound, the compact slice Fourier and lift estimates, and the cut grid with $3s$ available letters. [Selected grid][grid] · [Actual cutoff removal and endpoint][short]
* For equal compact weights put $n_0=30s^2+6$. At a Gram-positive point the two shifted compact-type contractions satisfy $\|v\|^2\le(3B)^{2n_0}(T'/G)^{n_0}\sum_\pm\|A_\pm^*v\|^2$, whereas $\|A_\pm\|^2\le(G/T')^{n_0}$. The [compact contraction proof](SPECTRAL_EQUAL_TYPE_CONTRACTIONS.md) supplies both inequalities with an improved constant on these types. Each shifted cut admits the same shortening estimate on $G^{p_0}FA_\pm$. Apply the first inequality at the selected point to an orthonormal target basis and the second on the singleton integration section. The scalar $T'^{n_0}$ cancels exactly. [Equal-weight contractions on both sides][equal]
* On that section the normalized terminal-minor expansion for $D_s^h$ has sum of absolute coefficients at most $B^{(|C_h|+6)m^2h}$, with every child of squared section energy at most $\widetilde I(F)$ after the positive scalar normalization. This is the $a'=h$ conclusion of the exterior-power step of B8.10hb. The shift reserve needed when the external minor exponent is zero is $q_0=40s^3+s(s+1)$, so the stated reserve $sh+s(s+1)\le q_0$ holds for $h\le40s^2$. Its hypotheses include the shifted-period cofactor estimates, degree ratios and signed tensor projections. [Moment normalization and exterior expansion][mom] · [Underlying real-period bounds](SPECTRAL_BESSEL_MOMENTS.md)

Set $h=2p_0=4s$ in the distinct case and $h=2p_0+n_0$ in the equal case. Thus $h\le40s^2$. The preceding shortening and contraction bounds give
$$
 \widetilde E(F;\gamma)\le
  B^{O(m^2)}G(\gamma)^{-h}
     \int G(c)^h\widetilde E(F;c)\,dc .                              \tag{4}
$$
Here the factors $\Lambda^{2s}$ and $(3B)^{2n_0}$ have the stated cost; absorbing the two signs costs a factor two. On the positive singleton section $G(c)\le |D_s(c)|^2$. Apply the triangle inequality in the section $L^2$ space to the expansion for $D_s^h F$. Its coefficient sum is squared **once**, giving
$$
 \int G(c)^h\widetilde E(F;c)\,dc
 \le B^{2(|C_h|+6)m^2h}\widetilde I(F).
$$
At external exponent zero there is no expansion of a further factor $D_l^e$. Inserting this inequality in (4) gives $B^{O(m^4)}\max(1,G^{-1})^{40s^2}$. For distinct weights the cost here is already $B^{O(m^3)}$ and the Gram exponent is $4s$. The tower-to-orbit factor $\pi^{2\sum_i s_i(s_i-1)/2}$ and the section change bounded by $\pi^{2m^2}$ both cost $B^{O(m^2)}$. [Tower and sectional constants][convert]

In the prescribed character the torus parameter is $\xi=\pi/(vg)$ and the transported Gram factor is $\xi^{2r(r+1)}G$. The transported squared point-to-section comparison costs at most $\max(\xi,\xi^{-1})^{2m^2+2rm}$. Thus transport of the Gram inverse costs at most $B^{O(r(r+1)h)}=B^{O(m^4)}$ in (4), or $B^{O(m^3)}$ for distinct weights. The two section masses use the same detector. Multiplying it by $\sqrt{dd'}$ absorbs the compact dimensions in the orbital and section identities simultaneously. The physical big-cell section integral for that coefficient equals $M$. At the selected point the root measure multiplied by $\theta'$ contributes at most $(\theta')^{-2}\le b^{2|C_1|m^2}$ to the squared norm. Consequently for the source's $J$ and its point weight $p$ one gets
$$
            p\,\|J_\gamma\|_{\rm HS}^2
              \le b^{C_3m^4}\max(1,G^{-1})^{40s^2}M .                \tag{5}
$$
The numerical hypotheses transferred here are the original gap and two-cluster conditions, the strict interlacing of both compact words, the wide cut for different local weights or the interior separated gap for equal local weights, and $T\xi^{2r},T'\xi^{2r}\ge1$. The source verifies the grid conditions in the eventual family and obtains the last gate from its critical-level and split-prime size inputs. When applied to independent local data these are hypotheses. [Grid verification][rowgrid] · [Terminal-scale check in the supplied family][frame] · [Torus comparison][torus] · [Section equality and root multiplier][root]

## The Gram and block-end factors

Let $s_i$ be the block lengths and $l_i$ their ends, with final index $j$. Write $U_l=\max(d_l,d_l^{-1})$ at a nonzero block end. If $s_j\ge2$, then $d_{s-1}=0$ and
$$
       p/G^k=d_s^{2(s_j-2)}
                       \prod_{i<j} d_{l_i}^{2(s_i+s_{i+1})}.
$$
If $s_j=1$, then
$$
       p/G^k=G^{-1}\prod_{i<j} d_{l_i}^{2(s_i+s_{i+1})}.
$$
For the second formula, substitute $G=d_{s-1}^2(|t_j|^2-TT')$ in the terminal singleton factor $(|t_j|^2-TT')^{k-1}$. In the other blocks substitute $|t_i|^{s_i}=d_{l_i}/d_{l_{i-1}}$. The difference of adjacent exponents is $2(s_i+s_{i+1})$. This telescopes to the displayed formula, also giving the first when the final block has length at least two. Therefore $G^k/p\le \max(1,G)\prod_i U_{l_i}^{2s}$ in all cases. Multiplying (5) by this expression and by (3) yields (1), with a fixed enlargement of the constant in $L_\tau$. For a terminal block of size two the terminal-minor multiplier in $p/G^k$ is exactly one. [Point-weight formula][weight] · [Original loss function][loss]

The deduction proves the unweighted inequality from the Roadmap's specified intermediate analytic results and the supplied Haar and degree ties. The outstanding analytic comparisons include the compact wave and boundary estimates and the physical realization of the shifted orbital amplitudes. The two compact contractions are computed above, and the [normalized exterior-period estimate](SPECTRAL_EXTERIOR_PERIOD_ON_THE_ROW.md) supplies the one-step coefficients in the terminal expansion on that realization. The [shifted minor estimates](SPECTRAL_SHIFTED_MINOR_MOMENTS.md) extend this calculation to the full requested ordinary moment on the stated analytic data. The [angular argument](SPECTRAL_ANGULAR_FROM_ORDINARY_AMPLITUDE.md) then gives both angular conclusions with their original normalization.

[target]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Formalism/SharpRestriction/CuspSpanNormBounds/CongruenceAtSplitFrobeniusHolds.lean#L434-L487
[theorem]: https://github.com/rh-lean-roadmap/rh-lean-roadmap/blob/dc5594a62bb2b94139788df817db693cd939a046/docs/src/book/main.tex#L17604-L17637
[section]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Formalism/FormalDegreeBessel/StatementBF.lean#L137-L156
[jac]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AbelianVarietyTheory/Proofs/FlagMeasures/LintegralBigCellHaarDensityConstant.lean#L280-L324
[dis]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AbelianVarietyTheory/Proofs/FlagMeasures/BesselDoubleCosetMeasureBigCellEq.lean#L140-L171
[constants]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AbelianVarietyTheory/Proofs/FlagMeasures/MeasurableBcWeight.lean#L201-L279
[fatou]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AbelianVarietyTheory/Proofs/FlagMeasures/LintegralHsNormSqDoubleCosetLeFatou.lean#L129-L195
[schur]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AbelianVarietyTheory/Proofs/FlagMeasures/LintegralHsNormSqMatrixCoeffLeFormalDegree.lean#L20-L44
[critical]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Formalism/HermitianCurvature/StatementSz.lean#L10-L18
[vol]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Formalism/SharpRestriction/CuspSpanNormBounds/BruhatCellsKronecker/FamilyStatementOfItemsFourSeven.lean#L64-L150
[grid]: https://github.com/rh-lean-roadmap/rh-lean-roadmap/blob/dc5594a62bb2b94139788df817db693cd939a046/docs/src/book/main.tex#L45024-L45040
[short]: https://github.com/rh-lean-roadmap/rh-lean-roadmap/blob/dc5594a62bb2b94139788df817db693cd939a046/docs/src/book/main.tex#L45107-L45137
[equal]: https://github.com/rh-lean-roadmap/rh-lean-roadmap/blob/dc5594a62bb2b94139788df817db693cd939a046/docs/src/book/main.tex#L45139-L45173
[mom]: https://github.com/rh-lean-roadmap/rh-lean-roadmap/blob/dc5594a62bb2b94139788df817db693cd939a046/docs/src/book/main.tex#L45229-L45279
[convert]: https://github.com/rh-lean-roadmap/rh-lean-roadmap/blob/dc5594a62bb2b94139788df817db693cd939a046/docs/src/book/main.tex#L45280-L45301
[rowgrid]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Formalism/SharpRestriction/CuspSpanNormBounds/BruhatCellsKronecker/StandardHypothesesOfScaleHyp.lean#L562-L669
[frame]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AbelianVarietyTheory/Proofs/FlagMeasures/UniformAmplitudeBoundWideRangeLargeGap.lean#L34-L44
[torus]: https://github.com/rh-lean-roadmap/rh-lean-roadmap/blob/dc5594a62bb2b94139788df817db693cd939a046/docs/src/book/main.tex#L45353-L45406
[root]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AbelianVarietyTheory/Proofs/FlagMeasures/AmplitudeEqBesselFunctionLargeGaps.lean#L150-L193
[weight]: https://github.com/rh-lean-roadmap/rh-lean-roadmap/blob/dc5594a62bb2b94139788df817db693cd939a046/docs/src/book/main.tex#L17123-L17135
[loss]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Formalism/SharpRestriction/CuspSpanNormBounds/NormalizedLocalScale.lean#L26-L48
