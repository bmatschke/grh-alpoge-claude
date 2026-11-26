# The absolute orbital integral for two nonsingular real flags

At a real place of an original tied row let $J$ be the normalized Bessel orbital operator from the primed compact type to the unprimed one. Suppose the Gram determinant is nonzero and the penultimate minor has absolute value $D>0$. Put $n=r+1=m/2$, $h=k-2-r$, and $v=\mathrm{rd}(E)/2$. Let $d_l$ be the absolute values of the leading minors of the real cross Gram matrix including $d_r=D$. For $I$ the set of positive block ends put $E_0=\max(1,\max_{l\in I}d_l^{-1})$. Write $\sigma_\tau=\prod_{l=1}^{n}\max(1,d_l/b^{C_hm^2})$.

For any fixed requested moment coefficient $C_{\rm pr}$, in the original eventual range there are constants $C,C_h$ independent of the place, words, and represented flags such that the integral defining $J$ converges absolutely and, for every integer $0\le q\le C_{\rm pr} k m^2$,
$$
 \|J\|_{\rm op}
 \le (b^{Cm} E_0)^{Cr^3}
      \left(\frac C{kv}\right)^{rh}
      D^{-h}\,\sigma_\tau^{-q/n}.                              \tag{1}
$$
This gives the absolute-convergence and absolute-operator inputs, including the second inequality of the source's decay statement, on every such local orbit. It also gives squared Hilbert–Schmidt bounds on the ranges specified below. The measure in (1) is the original quotient measure. [Local target and moment range][tests]

## Projected Gram volume on the quotient

Set $S_1=S_g(z',x)$ and $S_2=S_g(z,\gamma x)$. Here $S_g$ is the maximum of one and the $r+1$ successive Euclidean distances of the transported frame vectors to the spans of their predecessors, including the terminal vector. [Shell variables][lengths] · [Frame lengths][distance] On the two quotient charts let $Y,Y'$ denote the Gram volumes of the projections used by the source, with the second evaluated at $\gamma x$. Use the following real flag identities.

* On fixing the positive diagonal and middle Levi coordinate $m_0$, the first Gram volume $Y$ is the exterior norm of the projections of $r$ vectors $m_0^{-1}B_a\in\mathbf C^{k+1}$ onto a subspace $P_0$ of dimension $k-2$ or $k-1$. In fact $P_0$ is the kernel of two Hermitian pairings with the middle terminal vectors, intersected with the kernel of the last coordinate. The pairings are independent by their nonsingular two-by-two Gram matrix. In the normal form, a change of the $r$ projected vectors contributes the determinant of the cross block, of absolute value $D$. This cancels the $D$ dividing the definition of $Y$. Also $|\det m_0|=1$. [Normal form and dimension][projection]
* On $S_1,S_2\le R$ the transformed vectors have norm at most $rR^{2r-1}E_0$. There are at most $r(r-1)/2$ remaining off-block complex coordinates of modulus $\le R^{2r}E_0$, at most $r(r-1)/2$ complex skew coordinates and $r$ real ones of modulus $\le rR^{4r-2}E_0^2$. These bounds come from solving the frame equations on an invertible block end by cofactors. The remaining central coordinates are recovered from the skew Gram relation, which is quadratic in the middle coordinates. The within-block upper triangular parameters are the common stabilizer. Splitting them off is triangular with real Jacobian one, and integration of a normalized stabilizer cutoff in these parameters costs at most one. [Off-block equations][off] · [Middle and central coordinates][rad] · [Measure and section][section]
* The pairing of the two projected frames through the inverse transpose of the cross block has operator norm at most two. Indeed on the two positive subspaces its value is a difference of their ambient Hermitian pairing and the pairing of their projections to the common definite quotient; each has norm at most the product of the original norms. Taking the $r$th exterior power gives $YY'D\le 2^r$. In the reversed chart the absolute values of the minors agree by Hermitian symmetry. [Pairing and exterior power][pair]

The integral estimate uses the worst dimension $d=k-2$ in the first identity. Set $M=rR^{2r}E_0\ge1$ and project further to a $d$-plane in $P_0$. This decreases Gram volume, so its negative powers bound those of $Y$. For $r$ vectors in the complex $d$-ball of radius $M$, the [ball Gram moment](SPECTRAL_ORBITAL_AMPLITUDE.md) at exponent $\alpha=h=d-r$ is at most
$$
     \pi^{dr}M^{2r^2}(h!)^{-r}.
$$
Indeed Gram–Schmidt gives a product over $0\le i<r$ of $\Gamma(r-i)/(\Gamma(d-i)\Gamma(r+1))$ times $\pi^{dr}M^{2r(d-h)}$. Each gamma ratio is at most $1/h!$. This exponent is strictly below the first pole $d-r+1$, so all integrals are finite. The other three complex coordinates in each vector cost $(\pi M^2)^{3r}$. Integrating the remaining off-block coordinates in disks of radius $M$ and the skew coordinates in disks or intervals of radius $M^2$ gives a total power of $M$ at most $2r^2+6r+r(r-1)+2r(r-1)+2r\le10r^2$. All other constants besides $\pi^{rh}(h!)^{-r}$ are at most $\exp(O(r^2\log(2r)))$. Consequently, in Lebesgue coordinates the fibre integral of $Y^{-2h}$ with the length restrictions, after the stabilizer cutoff above, is at most
$$
 \exp(O(r^2\log(2r)))R^{20r^3}E_0^{10r^2}
                 (\pi e/h)^{rh}.                              \tag{2}
$$
The identical estimate holds in the reverse chart. It is uniform in $m_0$, since the change of variables took place before the ball estimate.

## Moments on the actual Bessel coefficients

Use the source's real setup for each of the two compact words. The input is a unit vector of the lowest compact type of the prescribed discrete series of $U(k+r,r+1)$. Each initial smooth coefficient transforms under the supplied compact stabilizer type and the flag's prescribed simple-root character, and has squared quotient norm $c_N$ times the dimension of that compact stabilizer type, with the same positive $c_N$ on the two sides. Use Haar probabilities on compact stabilizers, the supplied Haar and quotient measures, and terminal norms $-T,-T'$ with $1\le T,T'\le b^{C_Tm}$. Transport to the unit character uses the torus scale $\xi=\pi/(vg)$, with $1\le v\le b$ and $1\le g\le b^{2C_g}$. The [signed shift realization](SPECTRAL_BESSEL_REALIZATION.md) and [projected period calculation](SPECTRAL_BESSEL_COFACTOR.md) give the moment argument its compatible formal degrees, tensor projections and rank-one period scalars, including any zero neighbouring periods. [Both local setups][setup]

More explicitly, put $N=k+2r+1$, $q_0=km^5$, $\beta=b^{\max(2,C_u)}$. On the source's grid, for each compact word one has $|\lambda_a|,|u_i|\le\beta$, $\lambda_a-u_i\in\mathbb Z+1/2$, $\lambda_i<u_i$ for $1\le i\le k$, and $u_{i+1}<\lambda_i$ for $1\le i<k$ in one-based indexing. The first $k-1$ nodes lie in $[0,b_v/8]$ at pairwise distances at least $\gamma_0=Nm^{10}$, and all remaining nodes lie in $[-2b_v,-b_v]$. The opposite-sign gap is at least $h_0=N^{19}$, with the source's gap condition at $h_0/4$, $100(q_0+1)\le\min(\gamma_0,h_0)$ and $10^6N^7\le b_v$. Use the source's discrete-series family with parameter $\lambda+\nu$ for all integral shifts $\|\nu\|_1\le q_0$. These conditions supply the initial length moment on each side before any pair of flags or minor $D$ is chosen. [Grid and shift family][grid]

Let $H=b^{C_Hm}$ dominate the length-moment scales at all places and words. Use the bottom shell $S\le2H$, and subsequent shells $2^iH<S\le2^{i+1}H$, $i\ge1$. The [length-moment proof](SPECTRAL_BESSEL_MOMENTS.md) gives the normalized mass of the $i$th shell at most $n\,2^{-2pi}$ for any integer $p$ with $np\le\min(km^5,2(k+2r+1)^2)$. It applies to both normalized coefficient vectors $\Phi,\Phi'$ by the [realization on the shifted series](SPECTRAL_BESSEL_REALIZATION.md). One may take
$$
 p=\lceil 20r^3+nq+2\rceil .
$$
For $C_{\rm pr}\ge0$, $n=m/2$ and $r<n$ give
$$
 np\le20nr^3+n^2 C_{\rm pr}km^2+3n
       \le(3+C_{\rm pr})km^4 .
$$
Hence $m\ge3+C_{\rm pr}$ gives $np\le q_0$, and $k\ge(3+C_{\rm pr})m^4$ gives $np\le k^2\le 2N^2$. Both hold eventually by the standing growth assumptions $m\longrightarrow\infty$ and $C'm^5 f\log b\le k$. The quantifier fixes $C_{\rm pr}$ before the eventual cutoff. In particular it covers the largest allowed $q$. For the bottom shell its mass is at most one. For a higher shell Markov's inequality uses the $n$ positive length moments only, each bounded by $H^{2p}$ for the same $H$ at every permitted order.

Fix unit vectors in the two compact types. On a box of shell indices $i,i'$, bound the absolute value of the product of coefficient pairings by $(2^r/D)^h$ times their product weighted by $Y^{-h}(Y')^{-h}$. Apply Cauchy–Schwarz. For the square containing $\Phi'(x)$ unfold the common quotient on the primed side. Its own shell is on the base, while $Y^{-2h}$ and the other shell are in the fibre in (2). For the other square push the common quotient forward under left translation $x\mapsto\gamma x$ and unfold on the reversed side. Conjugation carries the normal-form stabilizer density to the same density $s$ in that chart, as follows from the [reverse root-measure comparison][inverse]. The compact Haar probabilities give the normalized coefficient mass in the prescribed unit direction by Schur orthogonality. In using this last identity first bound the fibre uniformly by (2); the remaining own-shell restriction is invariant under the compact Bessel group. One may truncate each negative power inside the unfolding and take an increasing limit. The locus of zero Gram volume has fibre measure zero by the projected-ball calculation. The normalization of $J$ divides by the common coefficient normalization $c_N$, cancelling the two square roots of $c_N$. Each squared integral has measure factor $\kappa/s$ for unipotent Haar density $\kappa$ and stabilizer density $s$; the product of square roots retains it once. [Two-sided unfolding on these flags][unfold]

Use $R=2^{i+i'+1}H$ in (2). For each $l$, the two wedges of the first $l$ vectors have norms bounded by $S_1^l,S_2^l$. The Hermitian signature matrix is Euclidean unitary, so their pairing gives $d_l\le(S_1S_2)^l$. Taking the local cutoff $b^{C_hm^2}\ge(4H^2)^n$ therefore gives, with one fixed $C_h$ since $n=m/2$,
$$
      \sigma_\tau\le2^{n^2(i+i')}.
$$
The coefficient square roots give $n\,2^{-p(i+i')}$. Reserving $nq(i+i')$ in this exponent supplies $\sigma_\tau^{-q/n}$; $20r^3(i+i')$ pays the growth of (2). The remaining boxes have a convergent geometric sum bounded by an absolute constant. This proves integrability of every matrix entry on the common quotient. Finite dimensionality gives absolute integrability of the operator-valued integrand as well. Supremizing the bounds for the unit pairings gives
$$
 \|J\|_{\rm op}\le\frac{\kappa}{s}\exp(O(r^2\log(2r)))\,
      (2H)^{20r^3} E_0^{10r^2}
      (2\pi e/h)^{rh}D^{-h}\sigma_\tau^{-q/n}.                 \tag{3}
$$

The source densities, with the transported real frame and $a$ the number of root coordinates of the common stabilizer, have ratio
$$
 \frac{\kappa}{s}=
 \frac{(2v)^{-rk}\theta\,2^{r(k+1)+r(r-1)}}
      {\theta'(vg)^{-a}}
 =\frac{\theta}{\theta'}\,2^{r^2}(vg)^a v^{-rk},\qquad a\le r^2 .
$$
The two scale factors are in $[b^{-C_1m^2},b^{C_1m^2}]$, $1\le v\le b$, and $g\le b^{2C_g}$. Thus the ratio is at most $b^{O(m^2)}v^{-rh}$. The normalization of the source root coordinates is essential for the factor $(vg)^a$. Since $h\ge k/2$ eventually, (3) proves (1), on enlarging $C$ in terms of the fixed family constants. [Root coordinates and their measure][root] · [Density ratio][ratio]

## Where this supplies the squared estimate

Put $x=d_n$, $t=\sqrt{TT'}$, $G=x^2-t^2D^2>0$, $\eta=(e\pi/(g^mTk v))^k$, and $A_\tau=(b^{Cm}E_0)^{Cr^3}$ with the $C$ in (1). Let $d_\tau$ be the dimension of the target compact type, $L_\tau$ the ordinary [real loss](SPECTRAL_REAL_LOSS_PRODUCTS.md), and $t'_\tau=T_{{\rm crit},\tau}(u')/T'$. From $\|J\|_{\rm HS}^2\le d_\tau\|J\|_{\rm op}^2$, (1) gives the actual ordinary squared bound
$$
 \frac{\eta G^k\|J\|_{\rm HS}^2}{d_\tau}
 \le L_\tau(t'_\tau)^{-k}\sigma_\tau^{-2q/n}
$$
wherever $\eta G^k A_\tau^2(C/(kv))^{2rh}D^{-2h}\le L_\tau(t'_\tau)^{-k}$. This criterion involves only the row parameters and its local Gram minors. More explicitly it holds on the subset
$$
       G\le\frac{g^m Tkv}{e\pi\,t'_\tau}
              \big[L_\tau A_\tau^{-2}(kv/C)^{2rh}D^{2h}\big]^{1/k}.
$$
For an angularly weighted square, the same unconditional integral estimate replaces $G^k$ on the left of the numerical test by $[(x+tD)^2/T]^k$, since $G K_\tau^2=(x+tD)^2$. The ordinary Hilbert–Schmidt estimate outside its displayed range, and the case of a zero penultimate minor, still require a separate argument.

[tests]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Formalism/SharpRestriction/CuspSpanNormBounds/CongruenceAtSplitFrobeniusHolds.lean#L434-L487
[projection]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AbelianVarietyTheory/Proofs/FlagMeasures/TwoFlagsGramNumberNormalFormEqGramProjection.lean#L345-L481
[off]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AbelianVarietyTheory/Proofs/FlagMeasures/OffBlockEntriesBoundedNormalFormPairOfFlags.lean#L44-L122
[rad]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AbelianVarietyTheory/Proofs/FlagMeasures/RadicalCoordinatesBoundedMajorantLengths.lean#L206-L310
[section]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AbelianVarietyTheory/Proofs/FlagMeasures/FibreGramNumberNullAndCutoffIntegralBound.lean#L92-L132
[pair]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AbelianVarietyTheory/Proofs/FlagMeasures/TwoFlagsGramNumberMulTopMinorNormLeTwoPow.lean#L218-L296
[unfold]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AbelianVarietyTheory/Proofs/FlagMeasures/AmplitudeAbsolutelyConvergentOperatorNormLe.lean#L64-L150
[root]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AbelianVarietyTheory/Proofs/FlagMeasures/RootMeasureEqNormalFormRootMeasure.lean#L148-L194
[ratio]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AbelianVarietyTheory/Proofs/FlagMeasures/OneLeFoldrMax.lean#L29-L63

[inverse]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AbelianVarietyTheory/Proofs/FlagMeasures/AmplitudeAbsolutelyConvergentOperatorNormLe.lean#L163-L179

[lengths]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AbelianVarietyTheory/Definitions/SemilocalFrames/UpperOff.lean#L90-L103
[distance]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Formalism/SharpRestriction/CuspSpanNormBounds/RelevantZeroGramTerms.lean#L299-L304
[setup]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AbelianVarietyTheory/Proofs/FlagMeasures/AmplitudeLocalDataMomentPieriHypotheses.lean#L59-L97
[grid]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AbelianVarietyTheory/Definitions/Jets/SumIoPrAlt.lean#L155-L171
