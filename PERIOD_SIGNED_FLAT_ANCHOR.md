# The signed determinant twist on the selected deep component lattice

Fix a sufficiently large selected family member, a nonterminal lift $i$, and a good deep cover at that lift. Write $p=k+i$, $q=m-i-1$, $r=p+q$ with $i$ zero-based. Let $\Lambda_M$ be the deep integral cusp lattice of weight $u_M=u_W-c_0\lambda$ and theta exponent zero. Let $A$ be the deep integral cusp lattice of weight $G_s(-c_0)$. Both slopes use the squared Petersson norm of the same uniformization and the same dictionary of frames. Use $L=x^\epsilon$, $b=e^L$, $U=fmbL\log\log x$, and let $M_i$ be the signed row main term. Under the native deep goodness, flat-degree and unramified-point hypotheses, the determinant and theta twist has the lower bound

$$
\mu(A)\ge \mu(\Lambda_M)-M_i-(60+8q)fbL
 -n_Vfr\left(\tfrac12\log(2\pi)+\log\operatorname{rd}(E)\right)
 -2\ell_S .
\tag{1}
$$

Here $E$ is the host CM field of degree $2f$, $n_V$ is the even column count and $\ell_S$ is the sum of logarithms of the distinct bad rational primes of the cover. In particular the total loss after $M_i$ is $O(U/\log\log x)$. This identifies which coefficient of $U$ must come from the fitted component degree.

## The integral and metric identification

For each of the $f$ CM labels let $w_\tau$ be the selected anchor. Its coordinate is $k-2$ in a block of length $p=k+i$, so the positive-block weight formula gives $w_\tau>n_V/2$. Put $W=\sum_\tau w_\tau$. The identity of exponent functions for the negative shift is
$$
\operatorname{ex}(G_s(-c_0))=
\operatorname{ex}\bigl(u_M+\operatorname{par}(w),n_V/2\bigr).
$$
The cusp transformation laws, the finite support lattices in the cusp spaces, the Lie factors and the archimedean Petersson norms depend only on these exponents. The twisted lattice and $A$ consequently have the same rank and squared slope. The twist preserves the positive rank of $\Lambda_M$. [Anchor and weight definitions][f6-w] · [Positive-block inequality][f6-pos] · [Matching the integral lattice and metric][f6-congr] · [Application to the selected cover][f6-at]

Set $\delta=\log\operatorname{rd}(E)$ and let $\omega$ be the selected logarithmic CM period. The flat degree calculation at each $\tau$ yields
$$
c_{1,\tau}=-\tfrac12(p-q)\omega-q(\log d_0-\delta),
$$
where $d_0$ is the host parameter denoted by `D.host.d`. The integral flat twist at the same cover gives
$$
\mu(A)-\mu(\Lambda_M)\ge
 2\sum_\tau w_\tau c_{1,\tau}
 -2q\delta\sum_\tau |w_\tau|
 -n_Vfr\left(\tfrac12\log(2\pi)+\delta\right)-2\ell_S .
$$
The factor two converts ordinary normalized arithmetic degree into squared slope. The different allowance in this formula is exactly the same $\delta$ that enters $c_{1,\tau}$. Because $\sum|w_\tau|=W$, the first two terms on the right reduce to
$$
-(p-q)\omega W-2q\log(d_0)W.
\tag{2}
$$
This cancellation is valid in the lower estimate itself. It requires no equality in the estimate for the integral twisting section. The residual $n_Vfr\,\delta$ comes from the theta root. [CM flat degree on each component][f6-cm] · [Native coefficient and bad primes][f6-c1] · [Rank and integral degree comparison][f6-twist] · [CM determinant calculation in Roadmap v39][f6-road]

The unrounded numerical bounds in the native anchor proof are
$$
|M_i-(p-q)\omega W|\le 60fbL,\qquad W\le 4fb .
$$
They follow by comparing the pivot coordinate with the selected row center separately at every embedding. Now use $0\le\log d_0\le L$ in (2). This gives (1). The host bounds $\delta\le2L$, $frn_VL\le b$, $\ell_S\le40L$, together with $2\le m$, $0\le q\le m$ and $L\ge10$, show that (1) loses at most an absolute multiple of $fmbL=U/\log\log x$. These bounds are uniform over the indicated lifts and covers. [Pivot discrepancy and the $4fb$ bound][f6-anc] · [Host estimates][f6-host] · [Bad-prime sum and signed coefficient in Chen][f6-chen]

Consequently, a fitted lower bound $\mu(\Lambda_M)\ge-C_U U$ on this marked member yields $\mu(A)\ge-M_i-C_U U-O(U/\log\log x)$. Applying the [central-weight transfer](PERIOD_CENTRAL_WEIGHT_TRANSFER.md) with this lower bound gives
$$
\frac{\operatorname{lcv}(M_j)}{D_R}
 \le M_i+C_U U+O\!\left(\frac{U}{\log\log x}\right).
$$
Here the transfer's additional $O(b/(frL)^{10})$ is absorbed. The outstanding geometric estimate is the lower bound for $\mu(\Lambda_M)$ in the fitted Petersson metric. Chen derives it from the normalized component height, rank share and component Hilbert–Samuel inequalities. This sign calculation does not establish those inputs or the separate paired-reference inequality. [Chen's component-to-slope calculation][f6-degree]

[f6-w]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AbelianVarietyTheory/Definitions/Divisors/NormNegCmConstantEqAtAllEmbeddings.lean#L59-L76
[f6-pos]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AbelianVarietyTheory/Proofs/DivisorProofs/MinimalGenusBound.lean#L88-L100
[f6-congr]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AbelianVarietyTheory/Proofs/DivisorProofs/FlatBoundOfAnchor.lean#L32-L68
[f6-at]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AbelianVarietyTheory/Proofs/DivisorProofs/FlatBoundOfAnchor.lean#L125-L156
[f6-cm]: https://github.com/yyyyychen/RH-Natural-Language-Proof/blob/d4dfb1a282dbf857288e73eb1f546dbfcc5899b8/tex/deep-cover-flat-degree.tex#L44-L114
[f6-c1]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AbelianVarietyTheory/Proofs/DivisorProofs/FlatLineC1LogBound.lean#L59-L77
[f6-twist]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AbelianVarietyTheory/Proofs/DivisorProofs/FlatLineThetaRootTwistTwistingSectionStatement.lean#L12-L15
[f6-road]: https://github.com/rh-lean-roadmap/rh-lean-roadmap/blob/c535d69c2d028dd05547e05c4b0efde1225ce454/docs/src/book/main.tex#L49376-L49415
[f6-anc]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AbelianVarietyTheory/Proofs/DivisorProofs/AnchorBoundStatement.lean#L156-L205
[f6-host]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AbelianVarietyTheory/Proofs/DivisorProofs/FlatLineC1LogBound.lean#L30-L56
[f6-chen]: https://github.com/yyyyychen/RH-Natural-Language-Proof/blob/d4dfb1a282dbf857288e73eb1f546dbfcc5899b8/tex/covolume-component-transfer.tex#L436-L507
[f6-degree]: https://github.com/yyyyychen/RH-Natural-Language-Proof/blob/d4dfb1a282dbf857288e73eb1f546dbfcc5899b8/tex/covolume-component-transfer.tex#L359-L418
