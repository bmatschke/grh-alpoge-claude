# A negative Gram moment for the singular orbital integral

Fix a nonidentity zero-Gram term of one word, of rank $1\le j\le r=(m-2)/2$, in the [fixed-minor estimate](SPECTRAL_DIAGONAL_ZERO_CELL.md). Write $d=k-1$ and $h=d-j\ge k/2$. The source separates the finite genus count, the two real Bessel coefficients, and the volume of the section on which they are paired. We evaluate the section by a negative moment. This removes the two sums over Gram sizes in Roadmap B8.02b, Claim 6, and gives an additional $D_\delta^{-1/4}$ in the coefficient bound. The individual Bessel coefficients enter through weighted length tails. The [stabilizer calculation](SPECTRAL_STABILIZER_VOLUME.md) supplies the arithmetic Haar covolumes in the same charts. [Source statement and normalizations][road]

## The integral on complex balls

For $j$ columns in the radius-$M$ ball $B_d(M)\subset\mathbb C^d$, write $\Delta=(\det(X^*X))^{1/2}$. For ordinary real Lebesgue measure on each complex coordinate, $M>0$, $1\le j\le d$, and $0\le\alpha<d-j+1$, we have
$$
 \int_{B_d(M)^j}\Delta^{-2\alpha}\,dX
 =\pi^{dj}M^{2j(d-\alpha)}
 \prod_{i=0}^{j-1}
 \frac{\Gamma(d-i-\alpha)}{\Gamma(d-i)\Gamma(d+1-\alpha)}.       \tag{1}
$$
Indeed the Gram volume is the product of the successive distances to the spans of the preceding columns. Given $i$ independent columns, rotate their span to the first $i$ coordinates. For a uniform point in the unit ball the squared distance to that span has beta density with parameters $d-i,i+1$. To see this, at fixed squared perpendicular radius $t$ the polar-coordinate density contributes $t^{d-i-1}$ and the remaining ball contributes $(1-t)^i$. Multiplying its $(-\alpha)$-moment by the ball volume $\pi^d/\Gamma(d+1)$ gives the $i$th factor of (1), including $\pi^d$. It is independent of the preceding columns. Integrating in reverse order and scaling by $M$ proves the formula. Dependent columns have measure zero. The final column integral diverges at $\alpha=d-j+1$. Forrester's Proposition 8 and Corollary 11 give the corresponding matrix polar decomposition and determinant moments for ball ensembles. [Forrester, Proposition 8 and Corollary 11][forrester]

Take $\alpha=h+\tfrac12$. In the $i$th factor put $t=j-i\ge1$. Then $\Gamma(t-\tfrac12)/\Gamma(t)\le\sqrt\pi$, $\Gamma(h+t)/\Gamma(t)\ge h!$, and $\Gamma(j+\tfrac12)\ge\sqrt\pi/2$. Each gamma quotient is at most $2/h!$. Thus, for $M\ge1$,
$$
 \int_{B_d(M)^j}\Delta^{-2\alpha}\,dX
 \le (2\pi^{d})^j M^{2j^2}/(h!)^j.                            \tag{2}
$$
The half power stays a fixed distance from the pole while preserving the full factorial in every column.

## The section and the two Bessel coefficients

At one real place write $P>0$ for the normalized terminal pairing minor, $e=\max(1,\max_{l:\delta_l\ne0}d_l^{-1})$, and $s=\max(1,\max_l d_l/(2H)^{2r})$, where $d_l=\rho^{-2q_l}|\tau\delta_l|$ and $H=b^{C_Hm}$. Use the source's scale-one Haar measures. The two frames have length maxima $S_1,S_2$ (including reciprocal lengths) and projected Gram volumes $Y,Y'$. In its adapted section the source proves the following coordinate facts.

* For each fixed diagonal and middle Levi coordinate, $Y$ is the Gram volume of the projections of $j$ vectors $m_0^{-1}B_b\in\mathbb C^{k+1}$ onto a fixed subspace of dimension at least $d$. Here $|\det m_0|=1$, so the change from $B_b$ preserves Lebesgue measure. Integrating the normalized cutoff in the common stabilizer costs at most one. The section coordinates carry product Lebesgue measure.
* Take the bottom length interval $[1,2H]$ and the intervals $(2^iH,2^{i+1}H]$ for $i\ge1$. On the $(i,i')$ box put $R=2^{i+i'+1}H$ and $M=R^{2r}e$. The transformed columns have length at most $M$. The remaining coordinates lie in $n_1$ complex disks of radius $2rM^2$, $n_2$ real intervals of radius $2rM^2$, and $n_3$ complex disks of radius $M$, with $n_1,n_3\le r(r-1)/2$ and $n_2\le r$. The reverse frame has the same estimates for $Y'$ with the transported quotient measure.
* On both charts $YY'P\le2^j$ and $s\le2^{r(i+i')}$. The first inequality pairs the perpendicular projections, and the second bounds each leading minor by the product of the two frame length bounds. [Section coordinates and height box][coords] · [Projection and change of variables][projection] · [Pairing and measures][road]

Project further onto a $d$-plane inside the first projection. This can only decrease the Gram volume, since orthogonal projection is a contraction on the $j$th exterior power. After a unitary rotation the two complementary complex coordinates in each column cost $(\pi M^2)^{2j}$. Use (2) on the $d$-plane and multiply by the volumes of the remaining boxes. The total exponent of $M$ is at most $2j^2+4j+4n_1+2n_2+2n_3\le8r^2$. Using $h!\ge(h/\mathrm e)^h$ gives the following bound for the integral of $Y^{-2\alpha}$ along the section on the indicated shell, uniform in the base coordinates:
$$
 B=(16r)^{8r^2} M^{8r^2}(\pi\mathrm e/h)^{jh}.                 \tag{3}
$$
The same bound holds on the reverse section. This uses balls in the transformed column variables, so the estimate is uniform even when the middle Levi matrix has large operator norm. [One-sided unfolding][unfold]

In common coordinates $x$, fix unit vectors $v,w$ and put $F(x)=|\langle w,\Phi'(x)\rangle|$ and $F'(x)=|\langle v,\Phi(\gamma x)\rangle|$. The Gram factors used on these respective fibres are $Y(x)=Y_{z,z',\gamma}(x)$ and $Y'(x)=Y_{z',z,\gamma^{-1}}(\gamma x)$. Suppose each normalized squared coefficient vector assigns mass at most $(4r+4)2^{-2qi}$ to its own $i$th shell. Off the two null sets the integrand $FF'$ is bounded by $(2^j/P)^\alpha(FY^{-\alpha})(F'(Y')^{-\alpha})$. Apply Cauchy–Schwarz. For the first square use the one-sided unfolding for $\Phi'(x)$, inserting its own length shell on the base and the remaining shell cutoffs and $Y(x)^{-2\alpha}$ on the fibre. Compact averaging acts on the fixed unit vector and gives the one-sided dimension normalization. Formula (3) bounds the weighted fibre. Equivalently, first insert $\min(L,Y^{-2\alpha})$ in the unfolding and then use monotone convergence. For the second square push the common quotient forward by **left** translation $x\mapsto\gamma x$, and repeat for $\Phi$ and the reversed Gram in that chart. The two square roots together cost $B(4r+4)2^{-q(i+i')}$ after extracting the one-sided normalizations. Each squared bound has the factor $\kappa/s_R$ when $d\mu_N=\kappa\,d\ell_N$ and the common-stabilizer Haar density is $s_R$ times its chart density. The resulting product therefore carries this factor once, with $s_R=1$ here. [Orientation and the two one-sided bounds][orientation] · [Unfolding with a nonnegative measurable weight][unfold]

Now $M^{8r^2}=(2H)^{16r^3}2^{16r^3(i+i')}e^{8r^2}$. For $q>16r^3+1$ use $s\le2^{r(i+i')}$ and sum the remaining $2^{-(i+i')}$ over both indices. Apart from the one-sided coefficient normalizations this gives
$$
 4(4r+4)(16r)^{8r^2}(2H)^{16r^3}e^{8r^2}
 (8\pi\mathrm e/h)^{jh}P^{-h-1/2}s^{-(q-16r^3-1)/r}.         \tag{4}
$$

### The limiting exponent and its logarithmic cost

One can approach the pole in (1) without paying one pole per column. Put $\alpha=h+1-\eta$ for $0<\eta\le1/2$. In the notation $t=j-i$, the ratio $\Gamma(t-1+\eta)/\Gamma(t)$ is at most $1/\eta$ for $t=1$ and at most one for every $t\ge2$. Indeed $\Gamma(1+\eta)\le1$ by log convexity between 1 and 2, and the successive ratios decrease. Also $\Gamma(j+\eta)\ge\Gamma(1+\eta)\ge\mathrm e^{-2}$ by integrating on $[1,2]$. Thus (2) holds with $2^j$ replaced by $\mathrm e^{2j}/\eta$; the exponent $2j(d-\alpha)$ of $M$ can only decrease. After the two square roots in the shell calculation there is a single factor $1/\eta$ per real place. Choose $\eta=(2+\log^+P)^{-1}$ where $\log^+P=\max(0,\log P)$. Then $P^\eta\le\mathrm e$. With an absolute enlargement of the numerical constant, (4) holds with its $P$-factor replaced by
$$
                 P^{-h-1}(2+\log^+P).
$$
This estimates the paired section all the way to the limiting power, paying one logarithm. The one-sided integral itself diverges at that power. The fixed half-step in (4) avoids a logarithm and suffices for the original coefficient bound.

## Returning to the arithmetic label

Multiply (4) over the $f$ real places. The normalized terminal ideal has positive integer norm $D_\delta$, with $\prod_\tau P_\tau=\sqrt{D_\delta}$. For each nonzero minor $\prod_\tau d_{\tau l}\ge1$ by ideal integrality. Hence $\prod_\tau e_\tau\le((2H)^{2rf}\prod_\tau s_\tau)^{r+1}$. For $q=(\lceil C_s\rceil+2)kr$, the standing thresholds give $8r^2(r+1)+(16r^3+1)/r\le2k$. The net power of $S_\delta=\prod_\tau s_\tau$ is at most $-C_sk$.

For clarity the Bessel-model factor per place, besides the square root of the compact dimension, is $(2v_E)^{-rk}2^{r(k+1)+r(r-1)}$. The common-stabilizer and fixed-unipotent covolumes satisfy $V_R/\omega\le v_E^{k(r-j)f}(8v_E)^{2(r+1)^2 f}$ and $V_N^{-1}\le(8v_E)^{2(r+1)^2 f}$ at the scale of this chart, with $\omega$ its relative index weight. The residual large-rank power of $v_E$ is $v_E^{-kjf}\le1$. All remaining factors have the allowance of B8.02b since $1\le v_E\le b/2$, $h\ge k/2$ and $H=b^{C_Hm}$. Restoring the finite row weight $w_t$ and taking the infimum of the chart weights gives
$$
 \|v_t\|\le w_t\sqrt{\dim\pi_u}\,\omega_t
 (C/k)^{jhf} D_\delta^{-h/2-1/4}
 H(C)^{Cr^4} S_\delta^{-C_sk},\qquad H(C)=b^{Cm^2f}.          \tag{5}
$$
In particular (5) implies the requested power $D_\delta^{-h/2}$. Formula (1) and the section integral hold for the specified normal-form charts. Applying (5) to the actual coefficient uses the normalized length tail, and its identification with that coefficient. The [scale-one arithmetic calculation](SPECTRAL_STABILIZER_VOLUME.md) proves both covolume estimates above. The [normalized Bessel realization](SPECTRAL_BESSEL_REALIZATION.md), the [smooth decay from the noncompact-root gaps](SPECTRAL_SMOOTH_DECAY.md), and the [length moment calculation](SPECTRAL_BESSEL_MOMENTS.md) supply the analytic inputs at every real place on the tied model. The paired arithmetic mean has a [separate proof](SPECTRAL_PAIRED_GENUS.md).

[coords]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AbelianVarietyTheory/Proofs/FlagMeasures/FlagUnipotentGramNullAndFibreVolumeNormalForm.lean#L88-L153
[projection]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AbelianVarietyTheory/Proofs/FlagMeasures/MeasurePreservingMulVec.lean#L56-L162
[unfold]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AbelianVarietyTheory/Proofs/FlagMeasures/AmplitudeOneSideUnfolding.lean
[road]: https://github.com/rh-lean-roadmap/rh-lean-roadmap/blob/94e6a98b4e74932a0298d6bd22d44cf60c62764b/docs/src/book/main.tex#L41690-L41782
[forrester]: https://arxiv.org/abs/1701.04505

[orientation]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AbelianVarietyTheory/Proofs/FlagMeasures/AmplitudeDegenerateOperatorNormLeRealPlace.lean#L206-L221
