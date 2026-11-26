# Both angular bounds from the ordinary real-place amplitude

Let $m=2r+2$, $r\ge1$, on a represented positive-Gram cell at a fixed real place. Set $s=r+1$, $d=\dim W$, $g=g_0g_1$, $t'=T_{\rm crit}(w',\tau)/T'$, $v=\mathrm{rd}(E)/2$, and $D=|D_r|$, the absolute penultimate leading cross minor. Write $G=d_s^2-TT'D^2>0$ and use the source's normalized squared amplitude
$$
 H=\left(\frac{\mathrm e\pi G}{g^mTkv}\right)^k
                    \frac{\|J\|_{\rm HS}^2}{d}.
$$
Take $d>0$. When $d=0$ the target representation and $J$ vanish, with zero normalized expression in the native convention. Let $L(C)$ and $P(C)$ be the ordinary and operator losses of the [real-place calculation](SPECTRAL_REAL_LOSS_PRODUCTS.md). Let $\sigma\ge1$ be the local size, and $q\ge0$ the moment index. The two angular bounds hold whenever the ordinary squared and operator bounds are available at that index. For $D=0$, and also on a range of nonzero minors specified below, the ordinary estimate suffices by itself. Both angular bounds also acquire positive moments of order $m^2$ directly from exponent zero. [Exact local targets, including the powers of $\sigma$][targets] · [Definition of normalized volume][volume]

Use $k\ge2r+6$, $k\ge\mathrm e\pi$, $v,g\ge1$, $2\le C_a\le C\le k$, $r+2\le\delta k$ and $6\mathrm e\pi A\le C$. Here $T,T',t'>0$ satisfy
$$
             T'/T\le A,\qquad T't'\ge g^m k^{3r}.                       \tag{1}
$$
At the chosen moment the ordinary hypothesis is
$$
             H\,\sigma^{2q/s}\le L(C_a)(t')^{-k}.                        \tag{2}
$$
For nonzero $D$, the operator hypothesis at that moment is, with $h=k-r-2$,
$$
         \|J\|\,\sigma^{q/s}\le P(C_a)
                           (C_a/(kv))^{rh}D^{-h}.                        \tag{3}
$$
The [shifted-minor argument](SPECTRAL_SHIFTED_MINOR_MOMENTS.md) supplies (2) and the [projected Gram integral](SPECTRAL_NONSINGULAR_ABSOLUTE_INTEGRAL.md) supplies (3) on nonzero minor cells throughout $0\le q\le C_{\rm pr}km^2$ under their analytic, Haar and degree hypotheses. Use the larger of their two size cutoffs. This can only decrease $\sigma$ and weakens both input inequalities. The operator proof also chooses its shell scale and loss constants before the moment coefficient. Its order $p=\lceil20r^3+sq+2\rceil$ satisfies $sp\le(3+C_{\rm pr})km^4\le\min(km^5,2(k+2r+1)^2)$ eventually. The residual geometric shell sum is bounded by an absolute constant. The following argument therefore proves both angular conclusions on that full range when the same local data satisfy those hypotheses. The [unweighted squared estimate](SPECTRAL_ORDINARY_SQUARED_AMPLITUDE.md) also gives the smaller-moment tests below with fewer inputs. [Native ordinary and operator estimates][inputs] · [Family parameters and target dimension][range]

Write $U=R=1$ when $D=0$. When $D>0$, set
$$
 x=\sqrt{G/(TT'D^2)},\qquad y=\sqrt{1+x^2},\qquad
 R=(1+y)/x,\qquad
 U=\min\left(1,\ T'x^2t'g^{-m}(C/k)^{2r(1-\delta)}\right).
$$
The source's $x,y$ are the hyperbolic sine and cosine of the cross-minor parameter. In particular $G/(TD^2)=T'x^2$. The two conclusions are
$$
 \begin{aligned}
 H\,\sigma^{2q/s}&\le L(C)P(C)^2 (t')^{-k}U^k,\\
 H\,\sigma^{2q/s}R^{2k}T^{-k}&\le L(C)P(C)^2(C/k)^k .
 \end{aligned}                                                          \tag{4}
$$
[Definitions at zero and nonzero minor][angles] · [Cross-minor identities and sign of $G$][hyper]

## What follows from the ordinary squared amplitude alone

If $D=0$, the first line of (4) follows from (2), monotonicity of $L$, and $P(C)\ge1$. For the second line (1) gives
$$
      \frac1{Tt'}=\frac{T'/T}{T't'}\le\frac{A}{g^m k^{3r}} .
$$
Multiply (2) by $T^{-k}$. The resulting bound is $L(C_a)[A/(g^m k^{3r})]^k$, which retains the whole critical-power gain and implies (4). There is no inverse penultimate minor in this argument. [Original zero branch][zero]

For a nonzero minor the same argument proves both lines of (4) whenever $U=1$ and $R^2\le CTt'/k$. An explicit sufficient range for both is
$$
                    x^2=G/(TT'D^2)\ge k^{-r}.                            \tag{5}
$$
Indeed $(C/k)^{2r(1-\delta)}\ge k^{-2r}$ since $1\le C\le k$ and $\delta>0$. By (1), the second argument of the minimum is at least $k^r x^2$. For every $x>0$,
$$
       R^2\le(1+\sqrt2)^2\max(1,x^{-2})<6\max(1,x^{-2}).
$$
For $x\ge1$ use $1/x+\sqrt{1+x^{-2}}\le1+\sqrt2$, and for $x\le1$ bound the numerator. Under (5), $R^2/(Tt')\le6A/(g^m k^{2r})\le C/k$, proving the claim. With the measured $T,T',t'$ one may enlarge this range further. Put $K=CTt'/k>1$. The two unrounded threshold conditions are
$$
 x^2\ge\frac{g^m}{T't'}(k/C)^{2r(1-\delta)},\qquad
 x\ge\frac{2\sqrt K}{K-1}.
$$
The second condition is equivalent to $1+\sqrt{1+x^2}\le\sqrt K\,x$, as follows by solving that inequality with both sides nonnegative. [Native hyperbolic split][split]

## The small nonzero minors at an available operator moment

Set $Z=H\sigma^{2q/s}$. By summing the squared norm of $J^*$ over an orthonormal basis of the target, $\|J\|_{\rm HS}^2/d\le\|J\|^2$. The minor is a nonzero block end, so the original loss contains $D^{2r+4}$ as an upper bound, since $C_am\ge2r+4$. Thus (3), the identity $D^{-2h}=D^{2r+4}D^{-2k}$ and $v\ge1$, $k\ge\mathrm e\pi$, give
$$
 Z\le L(C_a)P(C_a)^2
        \left[\frac{G}{TD^2g^m}(C_a/k)^{2rh/k}\right]^k .
$$
In the rearrangement the discarded factor is $(\mathrm e\pi/(kv))^k v^{-2rh}\le1$. Because $2rh/k=2r(1-(r+2)/k)\ge2r(1-\delta)$, the factor $(C_a/k)^{2rh/k}$ is at most $(C/k)^{2r(1-\delta)}$. The direction uses $C/k\le1$. Taking the minimum with (2) proves the first line of (4), even with the smaller prefactor $L(C_a)P(C_a)^2$. [Rank bound and exponent comparison][rank] · [Exact power of the block-end minor][minor]

For the second line use (2) when $x\ge1$. Then $R^2<6$ and (1) applies. When $0<x<1$, multiply the unshortened operator bound for $Z$ by $R^{2k}T^{-k}$ and insert $G=TT'D^2x^2$. The powers of $x$ cancel exactly. The result is bounded by
$$
 P(C_a)^2D^{2r+4}
 \left[\frac{\mathrm e\pi}{kg^m}\frac{T'}T(1+y)^2\right]^k
      v^{-k}(C_a/(kv))^{2rh}
 \le L(C_a)P(C_a)^2
      \left[\frac{6\mathrm e\pi A}{kg^m}\right]^k .
$$
Here $(1+y)^2<6$, since $x<1$. This proves (4) with the same moment on both sides. It permits the stated constant $C\ge6\mathrm e\pi A$. [Original second case][second]

## Positive moments obtained at exponent zero

On an actual cell the only nonzero leading minors are the block ends $I$ and the empty minor of norm one. The threshold $B=b^{C_hm^2}$ in the local size is at least one. Hence
$$
 \sigma=\prod_l\max(1,d_l/B)
     \le\prod_{l\in I}\max(d_l,d_l^{-1}).
$$
All other bases in $L(C)$ are at least one. For $0\le q\le Q$ we consequently have
$$
      L(C_a)\,\sigma^{2q/s}\le L(C)
        \quad\hbox{if}\quad (C-C_a)m\ge2Q/s .                           \tag{6}
$$
In particular $Q=a m^2$ for any fixed $a\ge0$ is allowed with $C\ge C_a+4a$, since $m=2s$. The source's eventual family range allows that fixed $C$ and $r+2\le\delta k$ after one cutoff. [Local size and ordinary loss][sizes] · [Uniform family choice][eventual]

On the zero branch and throughout (5), use (2) only at $q=0$, keep the prefactor $L(C_a)$ in its proof, and apply (6). This proves both angular lines and the ordinary squared line through the stated positive moments on the hypotheses of the [unweighted result](SPECTRAL_ORDINARY_SQUARED_AMPLITUDE.md). At all other nonzero minors, (2) and (3) just at $q=0$ give the two angular bounds with raw prefactor $L(C_a)P(C_a)^2$ and the final constant $C$ already in $U$. Apply (6) and $P(C_a)\le P(C)$ to get the same positive moments there. This last argument transfers the two angular estimates; a separate weighted operator estimate is needed for the operator line itself. There is also a test for the full requested moment on an individual cell. From the exact loss ratio, (6) holds at that $q$ if
$$
 \frac{2q}{s}\log\sigma\le (C-C_a)
 \left[m^4\log b+m^2|\log G|+m\sum_{l\in I}|\log d_l|\right].
$$
In particular, if every $d_l\le B$, then $\sigma=1$ and an exponent-zero estimate already supplies the corresponding line at every permitted $q$. For general size, the full requested range reaches a fixed multiple of $km^2$, while (6) with fixed constants gives order $m^2$.

[targets]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Formalism/SharpRestriction/CuspSpanNormBounds/CongruenceAtSplitFrobeniusHolds.lean#L464-L494
[inputs]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Formalism/SharpRestriction/CuspSpanNormBounds/CongruenceAtSplitFrobeniusHolds.lean#L434-L450
[volume]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Formalism/FlagUnipotentLattices/CardSubmodulesAndLinearEquivBounds.lean#L123-L150
[range]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Formalism/SharpRestriction/CuspSpanNormBounds/BruhatCellsKronecker/FamilyStatementOfItemsFourSeven.lean#L1460-L1513
[angles]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Formalism/SharpRestriction/CuspSpanNormBounds/NormalizedLocalScale.lean#L202-L206
[hyper]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Formalism/SharpRestriction/CuspSpanNormBounds/BruhatCellsKronecker/FamilyStatementOfItemsFourSeven.lean#L1423-L1444
[zero]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Formalism/SharpRestriction/CuspSpanNormBounds/BruhatCellsKronecker/FamilyStatementOfItemsFourSeven.lean#L1514-L1538
[split]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Formalism/FlagUnipotentLattices/CardSubmodulesAndLinearEquivBounds.lean#L152-L166
[rank]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Formalism/SharpRestriction/CuspSpanNormBounds/BruhatCellsKronecker/FamilyStatementOfItemsFourSeven.lean#L1247-L1296
[minor]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Formalism/SharpRestriction/CuspSpanNormBounds/BruhatCellsKronecker/FamilyStatementOfItemsFourSeven.lean#L1536-L1558
[second]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Formalism/FlagUnipotentLattices/MinkowskiFactorialBounds/LatticeSumBounds.lean#L827-L897
[sizes]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Formalism/SharpRestriction/CuspSpanNormBounds/NormalizedLocalScale.lean#L22-L47
[eventual]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Formalism/SharpRestriction/CuspSpanNormBounds/BruhatCellsKronecker/FamilyStatementOfItemsFourSeven.lean#L1564-L1580
