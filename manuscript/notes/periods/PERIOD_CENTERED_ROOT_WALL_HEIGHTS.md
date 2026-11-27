# The centered root intersection from finitely many wall heights

At a fixed cutoff on a matched nonterminal root origin, the centered intersection in the [Frobenius calculation](PERIOD_ROOT_FROBENIUS_CORRECTION.md) can be recovered from heights of powers of individual root lines on one wall. For distinct cross-block gaps the interpolation formula has exactly one summand per gap. The original height estimates at increasing cutoffs then make its centered limit zero. The signed transition on the same origin gives
$$
          I_N(Y)=h_{\rm fl}(Y)+R_N(Y) .                                  \tag{1}
$$
Thus the mixed comparison has $\epsilon=0$ under the geometric hypotheses below. No uniform bound on interpolation coefficients over the family enters (1).

Write $n=r+s$, $f=|\Psi|$, $d=f\binom n2$, $e=frs$. At cutoff $M\ge2$, let $I_M=(\sum_ZP_{M,Z})/(\sum_ZV_Z)$ on the actual models, including their generic extension-degree normalization and smoothed metrics. Set $\mathcal A_M=I_M-h_{\rm fl}$, $L_z=-\sum_{\tau,i}z_{\tau i}X_{\tau i}$, $H(z)=(d+1)D(L_z^d)$ and $A_M(z)=\mathcal A_M(L_z^{d+1})$. The two symmetries used at this step are exact. The square comparison for successive steps in the **same** block makes $A_M$ alternating under their interchange. A transitive group of host automorphisms preserves $A_M$ after summing all components. On the compact flag the corresponding label permutation is an isometry. These are the native properties I8 and PropA. Only the first is asserted component by component. [Definitions and quantifiers][props] · [Square comparison][square] · [Host transport on the original models][host] · [Compact-flag label isometry][flag]

## Recovering the two calibrations as a derivative

Let $\Delta_{\rm in}(z)$ be the product of $z_{\tau i}-z_{\tau j}$ for $i<j$ in the same block and put
$$
 \Pi(z)=\prod_{\tau,\ i<r\le j}(z_{\tau i}-z_{\tau j}),\qquad
 C_M(z)=\frac{A_M(z)}{H(z)} .
$$
The Weyl formula gives $H=c\Delta_{\rm in}\Pi$ with $c>0$ fixed. Each within-block difference divides $A_M$ by alternation, and these linear factors are pairwise relatively prime. Accordingly $q_M=A_M/\Delta_{\rm in}$ is a homogeneous polynomial of degree $e+1$, symmetric within blocks and invariant under the transitive label action. The rational function $C_M=q_M/(c\Pi)$ is regular wherever $\Pi\ne0$ and is homogeneous of degree one. In particular it has a derivative at $z^0$, the row weight equal to zero in each first block and $-1$ in each last block. [Weyl degree and its normalization][weyl]

Use $\mu=L_{z^0}$, the within-block Vandermonde $J(X)=\prod(X_{\tau j}-X_{\tau i})$ with $i<j$ in the same block, and $D_*=D(\mu^eJ)>0$. Choose the flat test with the same Hodge factor as the second calibration.
$$
 Q_1=\mu^eJ/D_*,\qquad Y_0=p_{\tau_0,1}Q_1,\qquad
 Y_H=\mu^{e+1}J/((e+1)D_*) .
$$
It has $D(Q_1)=1$. The [flat law](PERIOD_FLAT_SCALAR_AT_CUTOFF.md) gives the same scalar as every other admissible $Q_1$ on the matched original model.

Write $\mathbf1$ for the vector with every entry one and $p=\sum_\tau p_{\tau,1}$. Along $z^0+u\mathbf1$ the cross-block gaps all equal one. Applying $J(\partial_z)$ to the numerator and denominator of the identity $A_M=C_MH$, at any point of this line, gives
$$
 C_M(z^0+u\mathbf1)=
 \frac{\mathcal A_M((\mu-up)^{e+1}J)}{(e+1)D((\mu-up)^eJ)} .
$$
Indeed $H$ vanishes to order $d-e$ in the within-block differences there, so every derivative in the product rule must hit $H$. The common scalar $(-1)^{d-e}(d+1)!/(e+1)!$ cancels, and the resulting denominator is nonzero. In fact $D((\mu-up)^eJ)=D_*$ since the complete degree-one power sum in any row is geometrically zero. Setting $u=0$ and differentiating there now gives
$$
 C_M(z^0)=\mathcal A_M(Y_H),\qquad
 dC_M(z^0)[\mathbf1]=-f\mathcal A_M(Y_0).
$$
In the second equation the $f$ terms are equal by label symmetry. [Normalization on the partial flag](PERIOD_HODGE_TEST_ON_BASE.md) · [Degree-one flag relation][flatrel]

For the fitted row $v$ let $S_0=\sum_{\tau,i<r}v_{\tau i}$, $a_0=S_0/r$ and $a_H=S_0/(fr)-(\sum_{\tau,i\ge r}v_{\tau i})/(fs)$. Averaging $v$ under the block and host permutations gives $(a_0/f)\mathbf1+a_Hz^0$. The derivative at the fixed point $z^0$ is invariant under those permutations. Euler's identity gives $dC_M(z^0)[z^0]=C_M(z^0)$. Thus, for $Y=L_v^{d+1}/H(v)+a_0Y_0-a_HY_H$,
$$
       \mathcal A_M(Y)=C_M(v)-dC_M(z^0)[v].                             \tag{2}
$$

## A formula on the cross-block walls

Suppose first that all $e$ cross-block gaps $g=v_{\tau i}-v_{\tau j}$, $i<r\le j$, are distinct, and write $D_v(t)=\prod_g(t+g)$. They are positive for the regular dominant $v$ under consideration. Moving from $v$ to $v+t z^0$ preserves every within-block difference and increases every cross gap by $t$. Hence
$$
 C_M(v+t z^0)=
       \frac{D_v(0)A_M(v+t z^0)}{H(v)D_v(t)} .
$$
The numerator in $t$ has degree at most $e+1$. By homogeneity its polynomial part after division by $D_v(t)$, with the displayed normalization, is $tC_M(z^0)+dC_M(z^0)[v]$. This follows by expanding $tC_M(z^0+v/t)$ at infinity. The remainder has simple poles with residues given by evaluation of the numerator divided by $D'_v(-g)$. Evaluating it at zero proves the exact finite-cutoff formula
$$
 \boxed{\displaystyle
 \mathcal A_M(Y)=\frac{D_v(0)}{H(v)}
       \sum_g\frac{A_M(v-g z^0)}{gD'_v(-g)} .}                          \tag{3}
$$
The signs matter because successive poles need not have residues of the same sign. For repeated gaps, ordinary polynomial division gives the corresponding partial fractions with higher-order poles. The following interpolation treats all such rows using ordinary heights alone.

The weights $v-gz^0$ in (3) need not be dominant. For a given term, move the colliding pair to $(\tau_0,r-1),(\tau_0,r)$ by a label permutation and permutations within the blocks. The value of $q_M$ is unchanged. Denote the resulting weight by $w$. Choose a rational point $b$ on that wall with $\|b\|_\infty<1/2$ and every other adjacent gap positive. For example, start with rows $-i/(4(n+1))$, and add $1/(4(n+1))$ to entries $i\ge r$ in row $\tau_0$. The polynomial
$$
          s\longmapsto q_M\bigl(b+s(w-b)\bigr)
$$
has degree at most $e+1$. Take $e+2$ distinct rational $s$ sufficiently near zero that these points remain in a fixed dominant wall patch with the other gaps bounded below. At each point $x$, the number $\Delta_{\rm in}(x)$ is nonzero and $h_{\rm fl}(L_x^{d+1})=0$ by pullback to the partial flag. Thus its polynomial value is $I_M(L_x^{d+1})/\Delta_{\rm in}(x)$. Lagrange interpolation at $s=1$ recovers $q_M(w)$ from these ordinary model heights, and multiplication by $\Delta_{\rm in}(v-gz^0)$ recovers $A_M(v-gz^0)$. This uses at most $e(e+2)$ evaluations on the one chosen dominant wall. [Dominant patch and rational center][patch] · [Compact flag vanishing on its walls][props]

For repeated gaps choose a rational direction $h$ for which the differences $h_{\tau i}-h_{\tau j}$ are pairwise distinct across the $e$ cross pairs. Only finitely many proper hyperplanes are excluded. For $e+2$ distinct small rational $t$ the rows $v+th$ remain regular dominant and have distinct cross gaps, by avoiding finitely many further values of $t$. The polynomial
$$
 \frac{H(z)}{\Delta_{\rm in}(z)}
       \bigl(C_M(z)-dC_M(z^0)[z]\bigr)
     =q_M(z)-c\Pi(z)dC_M(z^0)[z]
$$
has degree at most $e+1$. Interpolate it on that line to recover its value at $v$, then divide by $c\Pi(v)\ne0$. This bounds the number of ordinary wall evaluations by $e(e+2)^2$ and applies to coincident gaps at different embeddings. All interpolation weights are fixed once $v$ and the rational points have been chosen. Their size plays no part in passing to the limit for this row.

## The cutoff identity on a matched origin

The original geometric wall estimate gives $|I_M(L_x^{d+1})|=O(\log M/M)$ for each of the finitely many dominant wall points above. To see why the actual model enters this estimate, set $\theta=5f/M$, add $2\theta$ to the first block at the distinguished embedding, and smooth with perturbation $\theta^2$. The geometric top degree of the perturbed line is $O(\theta)$ by the Weyl formula and the effective auxiliary difference. The horizontal curve lower bound and the dense-family upper bound, together with semipositivity and finite-fibre nefness, bound its arithmetic top intersection by $O(\theta\log M)$. Uniform smoothing and the variation bound for the root-line coefficients contribute $O(\theta^2)+O(\theta\log M)$. The normalizations divide by the same generic extension degree as $P_{M,Z}$. Summing and dividing by $V$ proves the claimed estimate with constants allowed to depend on the tower. Formula (3) and the two interpolations prove $I_M(Y)-h_{\rm fl}(Y)\to0$ on this fixed tower. [Actual wall estimate and hypotheses][wall] · [Degree and perturbation estimates][perturb] · [Origin's two curve bounds][curves]

Finally apply the local change of model to the pair of cutoffs $N,M$, for the single $Y$ above. A common normal model pulls back both flags and has the same degree normalization on the two sides. Their metrics agree under the generic identification, with vertical difference supported at the good primes $N<p\le M$. On a homogeneous summand $p_{\tau,k}Q$, the intersection of that vertical difference with the complementary classes gives the native Frobenius correction, including the multiplicities of the components of $\operatorname{div}(p)$. Its terms of order one are $-\log(p)S/(p-1)+\kappa_pT$. They vanish after summing the terms of $Y$ because $S(Y)=T(Y)=0$. Consequently
$$
 I_N(Y)-I_M(Y)=\sum_{\substack{N<p\le M\\p\ \mathrm{good}}}\rho_p(Y).
$$
The series on the right is absolutely convergent as $M\to\infty$ because for this fixed polynomial each surviving degree $k\ge2$ contributes $O_Y(\log(p)/p^2)$. Its limit is precisely $R_N(Y)$. This proves (1). Cofinal cutoff pairs with this same scalar transition and the finitely many vanishing wall tests already suffice. [Actual common model and pullback degrees][pair] · [Local power-sum comparisons][local] · [Decomposition and sign][split] · [Assembly of changes of model][change]

On the prescribed global split model, GRT34 proves the local change of Newton classes. GRT37–40 transport the component heights and give dense points at bounded cost. GRT41 and GRT44–45 prove the adjacent identity for the singular root metrics. GRT52 supplies the uniform abelian determinant comparison, and GRT53–57 prove the vertical and horizontal inequalities and the asserted wall rate on the matched tower. The final equality can therefore be inserted in the weighted lower bound when the chosen global family, its root origin and the arithmetic intersection system have been identified. [Wall calculation](GOOD_ROOT_TOWER_COMPARISONS.md#claim:GRT57) · [Weighted lower bound](PERIOD_ROOT_FROBENIUS_CORRECTION.md#inserting-the-two-scalar-estimates)

[props]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AutomorphicSpectrum/Definitions/DivisibilityTowers/Proportional.lean#L108-L137
[square]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AutomorphicSpectrum/Proofs/DivisibilityProofs/FullIntersectionTowerI8Identity.lean#L26-L29
[host]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AutomorphicSpectrum/Proofs/DivisibilityProofs/GoodTowerGlobalExtra.lean#L20-L28
[flag]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AutomorphicSpectrum/Proofs/DivisibilityProofs/FlagHeightLabelInvariant.lean#L129-L144
[weyl]: https://github.com/rh-lean-roadmap/rh-lean-roadmap/blob/dc5594a62bb2b94139788df817db693cd939a046/docs/src/book/main.tex#L20099-L20119
[patch]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/WeilBound/CoreStatements/FlagImmersions/AntisymmetryTowerTheorem.lean#L31-L50
[wall]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AutomorphicSpectrum/Proofs/DivisibilityProofs/TowerWeilTheorem.lean#L120-L145
[perturb]: https://github.com/rh-lean-roadmap/rh-lean-roadmap/blob/dc5594a62bb2b94139788df817db693cd939a046/docs/src/book/main.tex#L50067-L50153
[curves]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AutomorphicSpectrum/Proofs/DivisibilityProofs/GoodTowerI5.lean#L17-L20
[pair]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AutomorphicSpectrum/Proofs/DivisibilityProofs/GoodTowerGlobalConditions.lean#L197-L230
[local]: https://github.com/rh-lean-roadmap/rh-lean-roadmap/blob/dc5594a62bb2b94139788df817db693cd939a046/docs/src/book/main.tex#L50272-L50319
[split]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AutomorphicSpectrum/Proofs/DivisibilityProofs/PowerSumDeltaDecomposition.lean#L47-L70
[change]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AutomorphicSpectrum/Proofs/DivisibilityProofs/LinkedTowerPowerSum.lean#L12-L36
[flatrel]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/WeilBound/CoreStatements/FlagImmersions/DegFlPowerSumMul.lean#L14-L25

## Size of the intersection at the fitted weight

On the same origin assume also the calibrated flat and Hodge estimates in the [Frobenius calculation](PERIOD_ROOT_FROBENIUS_CORRECTION.md#inserting-the-two-scalar-estimates), with the uniform constants of the fitted family. Then for $F=L_v^{d+1}$, $v=u'$ and $H=H(v)$,
$$
 \frac{P_N(F)}{VH}\ \ge -C\|u'\|_1\lambda_N,\qquad
 T_* C\|u'\|_1\lambda_N=O(E_p).
$$
Indeed $|a_0|\le\|u'\|_1/r$, $0\le a_H\le n\|u'\|_1/(rfs)$, $n/r\le2$, and the two normalized height costs are $O(n\lambda_N)$ and $O(fs\lambda_N)$, respectively. For the latter, $\log(n+1)\ll\lambda_N$ by the cutoff bound $B\ge4fn^2$ and $N=\lfloor B\rfloor$. The flag height is nonnegative and the remaining Frobenius loss is at most $21\|u'\|_1/(5fn^2)$. Equation (1) removes the centered error. Finally $T_*\|u'\|_1\le834fmb$, $N\le132b$, $\log\operatorname{rd}(E)\le2L_x$ and $|L_E|\le7L_x$ with $L_x=\log b$, so $\lambda_N=\log(N\operatorname{rd}(E))+|L_E|=O(L_x)$. This fits $E_p=fmbL_x\log\log x$ throughout the eventual range. [Weight sum](https://github.com/rh-lean-roadmap/rh-lean-roadmap/blob/dc5594a62bb2b94139788df817db693cd939a046/docs/src/book/main.tex#L51547-L51551) · [Cutoff and local budget](https://github.com/rh-lean-roadmap/rh-lean-roadmap/blob/dc5594a62bb2b94139788df817db693cd939a046/docs/src/book/main.tex#L53739-L53751)

Where the model-to-record comparison and degree proportionality hold, this bound supplies the input $X_0$ of the [degree-weighted height transfer](PERIOD_WEIGHTED_ROOT_INTERSECTION.md). Passing to the actual determinant further uses the trace, section and carrier comparisons on those same components. [Transfer to the Petersson Chow height](PERIOD_RECORD_TRACE_TO_CHOW.md)
