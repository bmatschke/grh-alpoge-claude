# How much of the row space can a slope cut miss?

This refinement uses Muralidhara Subbarao’s centered Gram-matrix inequality, proved in Theorem 19.1 of his second report on the Alpöge argument. We apply it to the actual period maps and average over the slope distribution. The integral maps, height bounds and common target identification are those of the main proof. [Subbarao, Theorem 19.1 and its proof, pp. 38–39][subbarao-cuts] · [Period maps and slope filtration](../../overview.md#why-a-family-of-period-maps-controls-the-mean-slope)

Let $A_u:V_u\to Z$ be the normalized full period maps at the distinguished embedding, $M=\sum_u\dim V_u$, $D=\dim Z$, $Q=\sum_u A_u A_u^*$, and $t=\operatorname{tr}Q$. Thus $D$ is the full target dimension. The comparison dimension $D^\star$ used to prove the spectral estimates has already been eliminated in the inequality below. Positive weights on the individual maps in Subbarao’s notation are included in our normalizations of $A_u$. The two hypotheses we use are
$$
 \sum_u\|A_u^*A_u-I\|_{\rm HS}^2\le eM,
 \qquad D\operatorname{tr}(Q^2)\le(1+\eta)t^2.
$$
Here $0\le e<1$, $\eta\ge0$ and $M,D>0$. We have $t\ge(1-\sqrt e)M>0$ by Cauchy–Schwarz.

Omit subspaces of the full sources of total dimension $zM$, and write $Q'$ for the sum formed from the retained source directions. Let $P$ be the orthogonal projector onto the complement of their image span in $Z$, and write $p=\operatorname{tr}(P)/D$. Since $PQ'=0$ and $Q-Q'\ge0$,
$$
 \frac{\operatorname{tr}(PQ)}{t}
 \le \frac{\operatorname{tr}(Q-Q')}{t}
 \le c(z),\qquad
 c(z)=\min\!\left(1,\frac{z+\sqrt{ez}}{1-\sqrt e}\right).
$$
For the last numerator, the identity part of $A_u^*A_u$ contributes the omitted dimension, while Cauchy–Schwarz on its defect contributes at most $M\sqrt{ez}$. To obtain the bound from the target side, subtract the mean from each operator. Then
$$
 \|P-pI\|_{\rm HS}^2=Dp(1-p),\qquad
 \|Q-tI/D\|_{\rm HS}^2\le\eta t^2/D .
$$
Their Hilbert–Schmidt inner product is $\operatorname{tr}(PQ)-pt$. Thus $p-\sqrt{\eta p(1-p)}\le c(z)$. If $p>c(z)$, squaring and taking the upper root of the quadratic gives
$$
 p\le F_\eta(c(z)),\qquad
 F_\eta(v)=\frac{2v+\eta+\sqrt{\eta^2+4\eta v(1-v)}}{2(1+\eta)}.
$$
For $p\le c(z)$ the same inequality holds since $F_\eta(v)\ge v$ on $[0,1]$. In particular, if both moment errors vanish, omitting a fraction $z$ of the full sources costs at most the same fraction of the full target. The two maps from one-dimensional spaces onto the two coordinate axes of $\mathbb C^2$ give equality at $z=1/2$ when one source is omitted.

Now let $s$ be the rank-weighted mean of the adjusted slopes $\lambda$ of the ramified source lattices, $s+U$ their maximum, and $s-H$ a lower bound for the slopes of $C=RR^\vee$. Let $d$ be the fraction of full source dimensions already omitted on passing to the ramified subspaces. Write $1-\delta=\operatorname{rank}_K(C)/D>0$. For a cutoff $s-h$ let $q(h)$ be the fraction of adjusted source slopes below it and $p_C(h)$ the fraction of target slopes below it. The cut omits the full-source fraction $z(h)=d+(1-d)q(h)$. Projection to $C$ cannot increase absolute codimension. The nonzero-map slope inequality places the retained images in its filtration step of slopes at least $s-h$. Consequently
$$
 (1-\delta)p_C(h)\le F_\eta(c(z(h))).
$$

Both $c$ and $F_\eta$ are increasing and concave on $[0,1]$. For $F_\eta$ concavity follows by composing the increasing concave square root with the nonnegative concave polynomial in the radicand. For $\eta>0$ its derivative is nonnegative because the square root is at least $\eta$ and $|1-2v|\le1$. At $\eta=0$ the function is the identity. For $c$ the square-root term is concave and truncating its sum with a linear function at one preserves these properties. When $H>0$, the clipped-deficit argument of the main proof gives
$$
 \frac1H\int_0^H q(h)\,dh
 =\frac1H\operatorname{ave}_\lambda\min(H,(s-\lambda)_+)
 \le\frac{U}{U+H}.
$$
Apply Jensen’s inequality to $F_\eta\circ c$ under the uniform probability measure on $[0,H]$. On the target, $s-\mu(C)\le\int_0^H p_C(h)\,dh$. The resulting estimate on the selected family is
$$
 s-\mu(C)\le\frac{H}{1-\delta}\,
 F_\eta\!\left(c\!\left(d+(1-d)\frac{U}{U+H}\right)\right).
$$
For $H=0$ the target floor gives $s\le\mu(C)$. This combination retains the actual distribution of adjusted source slopes through its clipped first moment. Subbarao’s application in §19.2 instead starts with a pointwise tail bound and integrates it. At $d=\delta=e=\eta=0$ the displayed upper allowance becomes $UH/(U+H)$. The original explicit bound and the resulting prime-sum exponent still apply.

[subbarao-cuts]: https://github.com/muralisubbarao2/Refinements-and-Extensions-to-Alpoge-Claude-proof-of-Riemann-Hypotheisis/blob/4c3cb4f5e43212ec8c0ae759502291ae16e3df02/Ram-Calculus-Alpoge-RH-Nov24-v2.pdf#page=38

## A uniform allowance for the selected periods

The second moment can retain its actual defect $\eta_* = D\operatorname{tr}(Q^2)/t^2-1\ge0$. With $a=\sqrt e$ and $\tau=x^{-C_H}$ the mixed and diagonal moment estimates give
$$
 1+\eta_*\le
 \frac{(1+\eta_1)\{1+\eta_0+\tau(1+a)^2\}}{(1-a)^2}.
$$
In the selected families $\eta_0,\eta_1,a\le\exp(-x^{\varepsilon/8})=o(\tau)$ and $d\le\exp(-2x^{\varepsilon/8})$. Hence $\eta_*\le\tau+o(\tau)$, uniformly in the member and words. The target fraction discarded satisfies $\delta=o(1)$ and $H\le b/\tau$. These statements all concern the same family parameters. [Gram-moment calculation](../../../research/modules/spectral/gram_frame/gram_frame_section.tex#L55-L86) · [Uniform source and target losses](../../../research/modules/spectral/gram_frame/gram_frame_section.tex#L115-L139)

From the centered estimate, the elementary inequality $\sqrt{\eta_* p}\le p/4+\eta_*$ gives $p\le(4/3)(c(z)+\eta_*)$. Use $c(z)\le(z+a)/(1-a)$ and integrate in the cutoff. When $H>0$ this gives
$$
 (1-\delta)(s-\mu(C))\le\frac43\!
 \left(\frac{(d+a)H+(1-d)UH/(U+H)}{1-a}
                         +\eta_*H\right).
$$
When $H=0$ the target floor gives $s\le\mu(C)$. In the displayed inequality $(d+a)H=o(b)$ and $\eta_*H\le(1+o(1))b$, while $UH/(U+H)\le U$. Therefore for every fixed admissible family exponent and every $\xi>0$, a single cutoff ensures
$$
 s-\mu(C)\le (4/3+\xi)(U+b)
$$
for all its members beyond that cutoff. Taking $\xi=1/6$ gives the admissible constant $3/2$. This deduction combines Subbarao's centered estimate with the clipped integral and the decay rates of the original period family.

## The factor three in the selected code

The actual selected code allows a smaller second-moment defect than the abstract rank assumptions alone give. Write $M=\sum_u f_u$, $\tau=x^{-C_H}$ and $T_u^\star$ for the lower endpoint of the selected norm-prime window. The exact column-rank formula gives
$$
 \frac{f_u\Gamma^2}{D^\star}
 =\left(\frac{T_u}{T_u^\star}\right)^{fk}(1-T_u^{-k})^f
 \ge 1-fT_u^{-k}\ge1-k2^{-k},
$$
because $T_u\ge\max(2,T_u^\star)$ and $f\le k$. There are $\lceil3\Gamma^2/\tau\rceil$ words in every selected translate. Sum the rank bound to obtain $D^\star/M\le\tau/[3(1-k2^{-k})]$. [Exact rank and prime window](https://github.com/rh-lean-roadmap/rh-lean-roadmap/blob/c7755c1086f05d0918ee8496d95912e4f35e22f9/docs/src/book/main.tex#L35877-L35883) · [Cardinality of the selected code](https://github.com/rh-lean-roadmap/rh-lean-roadmap/blob/c7755c1086f05d0918ee8496d95912e4f35e22f9/docs/src/book/main.tex#L10765-L10772)

In the trace estimate one can retain $D^\star/M$ throughout. With $a=\sqrt e$ and $\eta_*=D\operatorname{tr}(Q^2)/(\operatorname{tr}Q)^2-1$, this gives
$$
 1+\eta_*\le
 \frac{(1+\eta_1)\{1+\eta_0+(1+a)^2D^\star/M\}}{(1-a)^2}.
$$
The original precision $\eta_0,\eta_1,a=o(\tau)$ already gives $\eta_*\le(1/3+o(1))\tau$. [Full trace estimate](../../../research/modules/spectral/gram_frame/gram_frame_section.tex#L22-L42) · [Uniform losses](../../../research/modules/spectral/gram_frame/gram_frame_section.tex#L115-L139)

For $H>0$, let $p(h)$ be the full target fraction perpendicular to the images retained at the cut $s-h$, and put $P=\int_0^H p(h)\,dh$. The target slope bound implies $(1-\delta)(s-\mu(C))\le P$. Subbarao's centered bound gives $p(h)\le c(z(h))+\sqrt{\eta_*p(h)}$. The integral of $c(z(h))$ is at most
$$
 C_0=\frac{(d+a)H+(1-d)UH/(U+H)}{1-a}.
$$
Cauchy–Schwarz yields $P\le C_0+\sqrt{\eta_*HP}$. Taking the upper root gives $P\le C_0+\eta_*H/2+\sqrt{C_0\eta_*H+(\eta_*H)^2/4}$. Since $H\le b/\tau$, $d,a=o(\tau)$ and $\delta=o(1)$, it follows that
$$
 s-\mu(C)\le U+\frac{b}{6}
        +\sqrt{\frac{Ub}{3}+\frac{b^2}{36}}+o(U+b).
$$
The error is uniform even when $U/b$ varies. Divide the root expression by $U+b$ and use the uniform continuity of the square root on a bounded interval. The case $H=0$ follows from the target slope floor. For a single coefficient, use $\sqrt{\eta_*p}\le p/12+3\eta_*$ before integration. This gives $s-\mu(C)\le(12/11+o(1))(U+b)$, in particular $s-\mu(C)\le(11/10)(U+b)$ beyond a common cutoff. The common cutoff may depend on the fixed family parameters. [Subbarao’s centered inequality, Theorem 19.1](https://github.com/muralisubbarao2/Refinements-and-Extensions-to-Alpoge-Claude-proof-of-Riemann-Hypotheisis/blob/4c3cb4f5e43212ec8c0ae759502291ae16e3df02/Ram-Calculus-Alpoge-RH-Nov24-v2.pdf#page=38) · [Centered rank and clipped slope integral](CENTERED_PERIOD_RANK_AND_SLOPE.md)
