# From root-model traces to the Chow height on integral frames

The nonterminal determinant in period entry 7 admits a direct passage from the root model to the projective image. The two constructions already use the same finite tests in the middle. A *record valuation* evaluates a section at an algebraic integral frame on a trait, with the valuation divided by the ramification index over the coefficient place. The original generic trace theorem bounds its output at every record valuation. The carrying-section argument needs precisely such lower bounds. Counting record-integral sections between the two steps removes the passage from record to Hodge–Tate valuations in equation (8.26d) and the return to record valuations in equation (8.28f). Hodge–Tate comparisons used to build or estimate the root model can still enter earlier in the proof.

Fix a selected nonterminal cover, component $Z$, coefficient field $K$, fitted weight $v=u_1-3n\eta_H$ and cutoff $N=\lfloor B(v,g)\rfloor$. Write $d$ for the dimension of the component flag variety, $a_Z$ for its normalized root-model slope, $\Delta'_Z$ for the geometric degree at $v$, and $\Delta_Z,h_Z$ for the degree and normalized Petersson Chow height of the image at $u_1$. Assume the finite extension of flag function fields, generic and analytic readings, model small-section lower bound, and the carrying, norm, normalization and nef Chow comparisons specified below on this cover. The argument uses these at the indicated weight. [Normalized intersection, degrees and rank descent](PERIOD_WEIGHTED_ROOT_INTERSECTION.md) · [Finite comparison at the carrying step](PERIOD_REFERENCE_DEPTH_BUDGET.md)

## The trace count with record integrality

Let $F=K(Z_{\rm fl})\subset L=K(M)$ be the supplied finite extension of degree $d_0$. In the model count write $A_m(t')$ for the small cusp sections in weight $mv$ of model sup norm at most $e^{mt'}$. Let $n^{\rm rec}_m(t)$ count cusp sections on $Z$ at the same archimedean threshold, integral for **every** record valuation above **every** finite coefficient place. Set
$$
 V^{\rm rec}_Z(t)=\limsup_{8\mid m,\ m\to\infty}
    \frac{d!\log n^{\rm rec}_m(t)}{[K:\mathbf Q]m^{d+1}} .
$$
The real norms are the component norms at the given host scalar. For the model lower bound use the same expression with $A_m(t')$ and denominator $[K:\mathbf Q]d_0m^{d+1}$. It is at least $\Delta'_Z(a_Z+t')$. On a supplied root origin this follows by multiplying sections on the smoothed nef model by the effective boundary section, applying the arithmetic volume lower bound and taking the smoothing limit. The identification of the limiting integral and metric on the actual root model is required. [Model smoothing, trace basis and finite places][rm] · [Section-count normalization][vol]

Fix the trace basis of the model in a weight $k_0v$, $8\mid k_0$, with sup norm at most $R_0$ on its finitely many members $f_i$. For clarity, a big smooth approximating line supplies a section of a multiple minus a fixed very ample class. Equal-degree coordinate monomials provide a field basis of $L/F$ after division by a common monomial, since their coordinate ratios generate $L$. One can increase to a common multidegree without changing linear independence by multiplying their rational readings by the same denominator. Multiply by the fixed section and boundary multiplier in the required powers to obtain the $f_i$ at weight $k_0 v$. Clearing a fixed denominator costs a constant on this component. Multiplication by a common nonzero rational reading preserves a field basis. In evaluating a section of weight $jv$ the weight gauge is common to every trace coordinate in that weight. Nondegeneracy of the field-trace pairing consequently makes
$$
       s\longmapsto \bigl(\operatorname{Tr}_{L/F}(s f_i)\bigr)_{i=1}^{d_0}
$$
injective, with the gauges understood. Indeed if the traces of the difference vanish against a basis, they vanish against every element, including the inverse of a nonzero difference after trivialization. Its trace pairing would then give $\operatorname{Tr}(1)=d_0\ne0$. [Construction on the model][basis] · [Original trace reading][reading]

The original trace result before its change of valuation gives a cusp section with each of these generic readings in degree $j=m+k_0$. Its sup norm is at most $d_0R_0e^{mt'}$. Its value under each record valuation above $\lambda\mid p$ is at least
$$
  -j\,\operatorname{ord}_\lambda(p)\,\mathbf 1_{p\in S_B}\,
  \bigl(h_E(p)+\mathbf 1_{p=2}\bigr)\|v\|_1 .
$$
Here $S_B=\{p:p\le B\ \text{or}\ p\mid 2|\operatorname{disc}E|M'\}$ and $h_E(p)=1/(p-1)+40v_p(|\operatorname{disc}E|)/[E:\mathbf Q]$. The archimedean factor is the triangle inequality for a sum of $d_0$ readings. The geometric input is the extension of these generic traces to the component cusp space with the stated complex-frame and integral-trait estimates. In the pinned source the three comparisons are assembled before its theorem that clears the Hodge–Tate denominators. [Original record-valued trace statement and proof][trace] · [Subsequent change to mixed valuations][mix]

Multiply all coordinates by the one rational integer
$$
   D_j=\prod_{p\in S_B}p^{\lceil j(h_E(p)+\mathbf 1_{p=2})\|v\|_1\rceil}.
$$
This makes them record-integral everywhere and is injective. Put $c_R=\|v\|_1\sum_{p\in S_B}(h_E(p)+\mathbf 1_{p=2})\log p$. Then $\log D_j\le jc_R+\sum_{p\in S_B}\log p$. For fixed $Z,t$ and $\eta>0$ take $t'=t-c_R-\eta$. For large $m$ one has $D_jd_0R_0e^{mt'}\le e^{jt}$, also when $t<0$. Thus $\#A_m(t')\le n^{\rm rec}_{m+k_0}(t)^{d_0}$. Divide by $[K:\mathbf Q]d_0m^{d+1}/d!$. Both indices are multiples of eight and $(m+k_0)/m\to1$. The upper limsup over shifted indices is bounded by the full limsup. The model lower bound and $\eta\downarrow0$ give
$$
              V^{\rm rec}_Z(t)\ \ge\ \Delta'_Z(a_Z-c_R+t).            \tag{1}
$$
The factors $d_0$ cancel even when the model is given only through a finite extension of function fields. The proof makes no division by a discriminant of a trace basis.

## Carrying these sections to the image

Use the nonzero carrying section $\theta_Z$ of degree eight in the difference between the target and source weights, together with its finite and archimedean comparisons on the selected component. Its balanced scalar at degree $m=8r'$ pays the cost $c_{\rm mult}$ for the divisor orders, the finite reference depths and the complex norm of the carrier. More explicitly, at each centred record test let $d_y$ be the minimum order of the integral weight-$u_1$ coordinates. The carrying bound is $v_y(\theta_Z)\ge8(d_y-e'_\lambda)$, with any stronger bound using an upper estimate for $d_y$ also sufficient. The balanced scalar clears $m e'_\lambda$ locally with the stated combined archimedean cost. For a source section already record-integral, $v_y(s)\ge0$ at this very test. Therefore the corrected $s\theta_Z^{r'}$ has valuation at least $md_y$. If $s$ has zero reading at a test the inequality holds there too. No estimate of its Hodge–Tate reading occurs. [Bounds at the same trait][carry] · [Direct divisor formulation](PERIOD_CARRYING_THETA_ORDERS.md)

The image model can be nonnormal. Divide the corrected generic reading by a nonzero homogeneous coordinate in the corresponding power and then express it in a local generator on the normalization. The original target test asks for precisely $m$ times that common coordinate order on every record valuation at which some cusp section has finite value. The no-base-point condition in the carrying theorem handles these valuations. The preceding bound makes this local representative integral at every centred test in the normalization comparison. It therefore gives a section of the pulled-back line on the normalization. Generic evaluation and multiplication by the nonzero carrier are injective. At infinity the Gram evaluation factor cancels against the Fubini–Study denominator on the target. The supplied carrier metric inequality and balanced scalar give a target threshold $t+c_{\rm mult}+\eta$ for all sufficiently large $m$. The normalization volume comparison identifies its leading small-section count with that on the image, with the pulled-back metric. These assertions require the original centred-test criterion, norm comparison and normalization theorem. [Original target small-section and carrying conditions](https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AbelianVarietyTheory/Definitions/Divisors/SemiposAtOfPositive.lean#L39-L70) · [Precise injection into the normalization][norm] · [Archimedean cancellation][height]

Take $t=c_s$, the shift given by the short integral generators. The target at $c_s+c_{\rm mult}+\eta$ is nef under the specified generator bound (enlarge a nonnegative allowance if necessary). Nef arithmetic Hilbert–Samuel and the Chow upper comparison give, upon using (1) and letting $\eta\downarrow0$,
$$
     \Delta_Z(h_Z+c_s+c_{\rm mult})
        \ \ge\ \Delta'_Z(a_Z-c_R+c_s).                            \tag{2}
$$
If the right side is negative, nonnegativity of the small-section count also permits replacing it by zero. Let $X_0\ge0$ satisfy $\sum_Z\Delta'_Z a_Z/\sum_Z\Delta'_Z\ge-X_0$. Since $(1-\rho)\Delta_Z\le\Delta'_Z\le\Delta_Z$, summing (2) yields
$$
 \frac{\sum_Z\Delta_Z(h_Z+c_s)}{\sum_Z\Delta_Z}
       \ \ge\ (1-\rho)c_s-X_0-c_R-c_{\rm mult}.                    \tag{3}
$$
Here the uniform nonnegative $c_R,c_{\rm mult}$ can be taken as in the sources. The route through the mixed count uses $2c_R$ in (1) and an additional $H_{\rm loc}$ in (2). Thus the direct argument removes $c_R+H_{\rm loc}$ from that combined allowance. Equation (3) feeds the existing weighted determinant descent. The root-model intersection estimate, model small-section lower bound and actual trace readings, the carrier and the final lattice comparisons retain their stated hypotheses. In particular (3) is an endpoint reduction. For the original mixed-valuation invariant $\nu_Z$, the [signed Hodge–Tate frame estimate](PERIOD_SIGNED_HODGE_TATE_FRAME_COST.md) gives a separate and sharper form of equation (8.26d).

[rm]: https://github.com/rh-lean-roadmap/rh-lean-roadmap/blob/dc5594a62bb2b94139788df817db693cd939a046/docs/src/book/main.tex#L50603-L50613
[vol]: https://github.com/rh-lean-roadmap/rh-lean-roadmap/blob/dc5594a62bb2b94139788df817db693cd939a046/docs/src/book/main.tex#L19977-L19991
[basis]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AutomorphicSpectrum/Proofs/GeometryProofs/GenericFrameComponentBound.lean
[reading]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AutomorphicSpectrum/Definitions/GlobalGeometry/ModelSmall.lean#L41-L63
[trace]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AutomorphicSpectrum/Proofs/GeometryProofs/UniformNormAllTowerBound.lean#L22-L33
[mix]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AutomorphicSpectrum/Proofs/GeometryProofs/UniformAllNormHeightBound.lean#L248-L291
[carry]: https://github.com/rh-lean-roadmap/rh-lean-roadmap/blob/dc5594a62bb2b94139788df817db693cd939a046/docs/src/book/main.tex#L53717-L53732
[norm]: https://github.com/rh-lean-roadmap/rh-lean-roadmap/blob/dc5594a62bb2b94139788df817db693cd939a046/docs/src/book/main.tex#L49310-L49315
[height]: https://github.com/rh-lean-roadmap/rh-lean-roadmap/blob/dc5594a62bb2b94139788df817db693cd939a046/docs/src/book/main.tex#L53758-L53780
