# A depth estimate at small inert primes and the fitted component slope

On a selected nonterminal good cover, write $k,m$ for the family parameters, $P=k+j-1$, $Q=m-j$ for its signature at lift $1\le j<m$, $r=P+Q$, $f=[E:\mathbf Q]/2$, $T=T_*$, $L=x^\epsilon$, $b=e^L$, and $U=fmbL\log\log x$. The arithmetic target is the squared Petersson slope of the deep integral cusp lattice $\Lambda_M$ at $u_M=u_W-c_0\eta_H$, with theta exponent zero.

The reference-depth estimate below removes the factor $\log\log x$ in the finite carrying cost. With the marked model, section and height comparisons specified in the last section, it gives
$$
 \mu(\Lambda_M)\ge -C fmbL .
 \tag{1}
$$
The constant is uniform over the sufficiently large family and its nonterminal lifts. The local depth calculation is on every integral frame of the indicated odd unramified inert type. Its application uses the character estimate on algebraic frames and the global interpolation for these frames in the [finite reference-depth construction](PERIOD_REFERENCE_DEPTH_BUDGET.md).

## A separate radius for each depth

Let $p\ge3$ be unramified in the host and inert in its marked imaginary quadratic subfield. Use the typed formal group of a CM-type factor on a split chart with $v(p)=1$. Its Frobenius orbit is even, all odd types have multiplicity at most $Q$, and the selected saturated $i$-frame is supported in one even type. For an integer $n\ge1$, let $\nu_i(n)$ be the least valuation, interpreted as an infimum, of the $n$-th power of the determinant differential acting at zero on integral formal functions of $i$ copies. Then
$$
 \nu_i(n)\ge
 \frac{inp}{p^2-1}
 -\frac{nQp^3}{(p^2-1)^2}-i^2\log_p(n+1).
 \tag{2}
$$

Fix an arbitrary integer $K\ge0$. The typical-curve construction gives a *single* integral tangent basis $B$ and depths $-1\le\delta_b\le K$. In the frame's one even type there are at most $Q$ basis directions at **each** exact depth $a=-1,0,\dots,K-1$. This is the stage invariant preceding the coarser count $(K+1)Q$ in the statement of the native depth theorem. The inverse logarithm admits output radii
$$
 R_a=\frac{1+p^{-(2a+1)}}{p^2-1}.
$$
Here $R_{-1}=1/(p-1)$ and these radii decrease with $a$. [Stage construction and per-depth count][c7-stages] · [Exact invariant inside the native induction][c7-stageLean]

Write the frame matrix in this basis as $x=uB^{-1}$. It is integral and supported in the chosen type. Process its columns in increasing order of depth. At depth $a<K$, work only on the rows left after earlier pivots. All these rows vanish on earlier depth groups. In the current rectangular block, choose a nonzero pivot of least valuation, exchange rows if necessary and clear its column from all remaining rows. The elimination coefficients belong to the valuation ring. Freeze the pivot row and continue until the remaining rows vanish on this entire group. Each pivot consumes a previously unused column, so at most $Q$ rows are frozen at this depth. Earlier zero entries remain zero throughout. Assign $k_h=a$ to every row frozen at this stage and assign $k_h=K$ to all surviving rows. The product of the row operations is one $g\in\mathrm{GL}_i(\mathcal O)$ and
$$
 (gx)_{hb}\ne0\ \Longrightarrow\ k_h\le\delta_b,
 \qquad \#\{h:k_h=a\}\le Q\quad(-1\le a<K).
 \tag{3}
$$
This is finite elimination over the valuation ring, including when its value group is nondiscrete. The native proof uses integral elimination once on the combined set of all columns below depth $K$. [One-block elimination in the source][c7-elim]

Assign the input variable in direction $h$ the radius $\rho_h=R_{k_h}$. By (3), the linear target $z_b=\sum_h(gx)_{hb}X_h$ has weighted order at least $R_{\delta_b}$. The native inverse-logarithm estimate accepts arbitrary nonnegative input radii with this property. For clarity, the nonlinear coefficient $A_{b,t,e}$ multiplies the $p^t$-th power of coordinate $b$ in equation $e$. At depth $-1$ its valuation is at least $-t$ and $-t+p^tR_{-1}\ge R_{-1}$ for $t\ge1$. At depth $a\ge0$ the first layer vanishes. At $t=2$ its valuation is at least $-1$ and each nonzero coefficient has $\delta_e\ge a-1$, so $-1+p^2R_a=R_{a-1}\ge R_{\delta_e}$. At $t\ge3$ the valuation is at least $1-t$, and $1-t+p^t/(p^2-1)\ge R_{-1}$ for $p\ge3$. Solving in increasing total degree therefore preserves the output orders $R_{\delta_b}$. This argument concerns formal coefficients and requires no convergence at the endpoint of a disk. [Inverse-logarithm inequalities][c7-inv] · [Native theorem with arbitrary input radii][c7-invLean]

The integral coordinate change formed by adding the typical curves has invertible integral tangent matrix and integral inverse. The change of the $i$ frame rows multiplies the determinant operator by the unit $(\det g)^n$. Thus the same depth $\nu_i(n)$ is measured after both changes. Every monomial of $\det(Y)^n$ has degree $n$ in each row. Pulling an integral test function back to the formal frame and using the divided-power content of this polynomial gives
$$
 \nu_i(n)\ge \frac{in}{p-1}-i^2\log_p(n+1)-n\sum_h\rho_h .
$$
One may see the content estimate directly from Legendre's formula. For any monomial $Y^\alpha$ in the determinant power, $\sum_{a,b}\alpha_{ab}=in$, each $\alpha_{ab}\le n$, and each integral polynomial coefficient has nonnegative valuation. The base-$p$ digit sum satisfies $s_p(t)/(p-1)\le\log_p(t+1)$ for every nonnegative integer $t$ (the least integer for a prescribed digit sum fills the low digits first). Apply this to the $i^2$ factorials. [Determinant pullback and divided powers][c7-pull]

By (3) and a geometric series,
$$
 \sum_h\rho_h\le
 \frac{i+i p^{-(2K+1)}}{p^2-1}
  +\frac{Q}{p^2-1}\sum_{a=-1}^{K-1}p^{-(2a+1)}
 \le \frac{i+i p^{-(2K+1)}}{p^2-1}
       +\frac{Qp^3}{(p^2-1)^2}.
$$
Each finite $K$ bounds the same invariant $\nu_i(n)$. Letting $K$ tend to infinity in this scalar inequality proves (2). The integral changes of coordinates for different horizons may vary freely.

## Finite orders on the marked cover

For a large block $k-1\le i\le P$ and an algebraic integral frame, the character-minor estimate supplies upper endpoint $n(Pp+Q)/(p^2-1)$. The difference from (2) is at most
$$
 \frac{2mn}{p-1}+i^2\log_p(n+1).
 \tag{4}
$$
Indeed $P-i+Q=r-i\le m$, $Q\le m$, and $p^3/(p^2-1)^2\le1/(p-1)$ for $p\ge3$. The lower endpoint is uniform on all integral frames. Raising a negative lower endpoint to zero only reduces its width. For $n=0$ take width zero. The [reference-depth construction](PERIOD_REFERENCE_DEPTH_BUDGET.md) sums these intervals before clearing their common lower order by one coefficient-field scalar at the selected place, with at most one rounding unit per rational prime. This uses its formal character, integral jet realization and theta interpolation hypotheses. [Character endpoints at these primes][c7-char]

Use (4) only for $mp<k$. At other inert primes retain the estimate $2mn/(p-1)$ of the reference-depth construction. Let $J=2\lfloor8b/T\rfloor+1$, $A_0=fm(\lfloor8b/T\rfloor+1)$, and let $V$ bound the sum of $in$ on the small blocks. The sum of the large-block exponents over all labels is at most $A_0/m$ and there are at most $f(m+1)$ of them. Thus the new allowance in the small inert range $p\le J$ is
$$
 e_p=\frac{2A_0+V}{p-1}
     + f(m+1)r^2\log_p(J+1)+1 .
$$
The first term summed against $\log p$ is $O((A_0+V)\log(2J))$. The second costs $O(fr^3\log(2J))$ because there are at most $k/m$ relevant primes and $k\le r$. The rounding terms cost $O(J)$ by the elementary Chebyshev bound. All other prime regimes already contribute $O((A_0+V)L+J)$ in the native sum. Since $T(A_0+V)\ll fmb$, $Tr^3\le b$, $TJ\ll b$, and $\log(2J)\ll L$, the total, including the $O(b)$ price of returning from the theta weight to $u_1$, satisfies
$$
 T s_{\rm ref}\ll fmbL.
 \tag{5}
$$
This estimates the genuine finite correction comparing the carrier with the target cusp base ideal at all coefficient places and traits. Chen's boundary-order argument works over a number field, so its residue characteristics are zero and its factorial contractions are units there. In mixed characteristic the carrier bound before correcting that target ideal is $c_{\rm raw}$, and the applicable allowance is $c_{\rm raw}+s_{\rm ref}$. [Prime ranges and numerical sizes][c7-primes] · [Chen's characteristic-zero test][c7-chen0] · [Integral correction on this cover][c7-corr]

## The component lattice and its metric

Here are the geometric inputs for (1). On the selected component $Z$ use the fitted $u_1$, $u'=u_1-3r\eta_H$, the finite extension of its flag function field and its marked record valuations from the [selected origin](PERIOD_SELECTED_MARKED_ORIGIN.md). Use the [centered root estimate](PERIOD_CENTERED_ROOT_WALL_HEIGHTS.md) with its calibrated flat and Hodge tests and matched arithmetic functional, and the [record-to-Chow comparison](PERIOD_RECORD_TRACE_TO_CHOW.md) with model smoothing, integral trace, carrying order, projective image normalization and nef arithmetic Hilbert–Samuel on this component. Write $H_Z,D_Z$ for that image's component-probability Petersson Chow height and moving degree. The rank and determinant comparison uses the same $D_Z$, the same integral generating lattice at finite places and Petersson spheres at infinity. In particular its component degree $d_Z$ is the ordinary normalized degree at $u_M$, after its own short flat twist from the adjoint weight. [Rank shares on the moving system][c7-ranks] · [Precise finite and infinite norms in the determinant][c7-hs] · [Return to the fitted component at $u_M$][c7-ret]

To see the size of each contribution, set $J_Z=\binom{T-1}{d}D_Z$, $r_Z=\mathrm{rk}\Lambda_{M,Z}$, $z=7(d^2/T+d\rho)$. The rank estimates give $(1-z)r_Z\le J_Z\le r_Z$. The native short-generator cost is $[6d+10+T(z+2\rho)]c_s=O(fb)$. Both $T\|u_1\|_1$ and $T\|u'\|_1$ are at most $834fmb$. The model cost $TX_0$ and normalized trace cost $Tc_R$ are $O(fmbL)$ since the cutoff and root-discriminant factors are $O(L)$. In the thick region the actual Bergman loss is $C(\|u_1\|_1+(fr)^8)$, in the thin region the carrier's pointwise decay pays for the evaluation estimate. Its other numerator cost is $O((frL)^2)$. Hence $Tc_{\rm raw}=O(fmb+TP_*)=O(fmb)$ from $P_*\ge(frL)^{12}$ and $TP_*\le\sqrt b$. Adding (5) gives $Tc_{\rm mult}=O(fmbL)$. [Short-generator budget][c7-short] · [Weight sums and Bergman numerator][c7-size] · [Thick-region input at the native weight][c7-thick] · [Row and local costs][c7-budget]

More explicitly, put $R=\sum_Zr_Z$, $h=3d+4$ and $H_Z^+=H_Z+c_s\ge0$. The fitted determinant inequality after absorbing its logarithm gives
$$
 d_Z\ge J_Z\{(T-h)H_Z^+-(T+h)c_s-O(b)\}.
$$
The $O(b)$ is uniform, since the raw determinant remainder plus its logarithmic coefficient times the logarithm of that coefficient is at most $10240b$. The degree-weighted height comparison gives
$$
 \frac{\sum_Z J_ZH_Z^+}{\sum_ZJ_Z}
 \ge (1-\rho)c_s-X_0-c_R-c_{\rm mult}.
$$
The left side is nonnegative. Multiplying by $\sum J_Z/R\in[1-z,1]$ bounds the rank-normalized average below by $(1-z)(1-\rho)c_s-X_0-c_R-c_{\rm mult}$. The leftover coefficient of $c_s$ in the degree inequality is at most $2h+T(z+\rho)$. The preceding budgets give $2\sum d_Z/R\ge-O(fmbL)$. [Logarithmic remainder on the selected determinant][c7-ret] · [Weighted Chow comparison](PERIOD_WEIGHTED_ROOT_INTERSECTION.md)

There is no finite index in the final assembly. The component idempotents of the original cusp rules split the finite integral lattice, and at embedding $\sigma$ a section supported on $Z$ has global squared norm equal to $a_{Z\sigma}$ times its component-probability squared norm, where $a_{Z\sigma}$ is the mass of its support for the global probability measure. Components are orthogonal. For the coefficient field $F'$ and $t_Z=r_Z/R$ this gives exactly
$$
 \mu(\Lambda_M)=\frac{2\sum_Zd_Z}{R}
    +\sum_{r_Z>0} t_Z\frac1{[F':\mathbf Q]}
                     \sum_\sigma\log\frac1{a_{Z\sigma}}.
$$
Positive-rank supports have positive mass and disjoint supports have mass sum at most one. Weighted Jensen applied to $a_{Z\sigma}/t_Z$ bounds the correction below by $-\sum_{r_Z>0}t_Z\log t_Z\ge0$. This proves (1) with the global Petersson normalization used at the next step. [Integral splitting, norms and exact degree law][c7-mass] · [Application on the selected cover][c7-global]

Under the same geometric hypotheses and those of the [signed flat anchor](PERIOD_SIGNED_FLAT_ANCHOR.md) and [central-weight transfer](PERIOD_CENTRAL_WEIGHT_TRANSFER.md), the resulting reference bound is $\operatorname{lcv}(M_j)/D_R\le M_i+O(fmbL)$. This conditional estimate still uses the actual tower calibrations, depth-interpolation and determinant comparisons above. A self-contained proof of their common realization and the separate paired-reference inequality remains necessary for period entry 7.

[c7-stages]: https://github.com/rh-lean-roadmap/rh-lean-roadmap/blob/c535d69c2d028dd05547e05c4b0efde1225ce454/docs/src/book/main.tex#L52949-L52980
[c7-stageLean]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AbelianVarietyTheory/Proofs/DivisorProofs/LogFGLDepthStagesLowA.lean#L278-L320
[c7-elim]: https://github.com/rh-lean-roadmap/rh-lean-roadmap/blob/c535d69c2d028dd05547e05c4b0efde1225ce454/docs/src/book/main.tex#L53006-L53018
[c7-inv]: https://github.com/rh-lean-roadmap/rh-lean-roadmap/blob/c535d69c2d028dd05547e05c4b0efde1225ce454/docs/src/book/main.tex#L53020-L53059
[c7-invLean]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AbelianVarietyTheory/Proofs/DivisorProofs/ExistsSolutionOrdGeRadius.lean#L429-L438
[c7-pull]: https://github.com/rh-lean-roadmap/rh-lean-roadmap/blob/c535d69c2d028dd05547e05c4b0efde1225ce454/docs/src/book/main.tex#L53061-L53084
[c7-char]: https://github.com/rh-lean-roadmap/rh-lean-roadmap/blob/c535d69c2d028dd05547e05c4b0efde1225ce454/docs/src/book/main.tex#L53111-L53130
[c7-primes]: https://github.com/rh-lean-roadmap/rh-lean-roadmap/blob/c535d69c2d028dd05547e05c4b0efde1225ce454/docs/src/book/main.tex#L51789-L51816
[c7-chen0]: https://github.com/yyyyychen/RH-Natural-Language-Proof/blob/d4dfb1a282dbf857288e73eb1f546dbfcc5899b8/tex/deep-boundary-orders.tex#L357-L387
[c7-corr]: https://github.com/rh-lean-roadmap/rh-lean-roadmap/blob/c535d69c2d028dd05547e05c4b0efde1225ce454/docs/src/book/main.tex#L53844-L53869
[c7-ranks]: https://github.com/yyyyychen/RH-Natural-Language-Proof/blob/d4dfb1a282dbf857288e73eb1f546dbfcc5899b8/tex/covolume-component-ranks.tex#L394-L438
[c7-hs]: https://github.com/yyyyychen/RH-Natural-Language-Proof/blob/d4dfb1a282dbf857288e73eb1f546dbfcc5899b8/tex/covolume-hilbert-samuel.tex#L300-L328
[c7-ret]: https://github.com/yyyyychen/RH-Natural-Language-Proof/blob/d4dfb1a282dbf857288e73eb1f546dbfcc5899b8/tex/covolume-hilbert-samuel.tex#L480-L514
[c7-short]: https://github.com/rh-lean-roadmap/rh-lean-roadmap/blob/c535d69c2d028dd05547e05c4b0efde1225ce454/docs/src/book/main.tex#L53817-L53834
[c7-size]: https://github.com/rh-lean-roadmap/rh-lean-roadmap/blob/c535d69c2d028dd05547e05c4b0efde1225ce454/docs/src/book/main.tex#L51679-L51704
[c7-thick]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AutomorphicArithmetic/ThetaCorrespondence/ThetaPairLifts/HodgeBundleWeights/BergmanKernelThickPartEstimate.lean#L39-L48
[c7-budget]: https://github.com/rh-lean-roadmap/rh-lean-roadmap/blob/c535d69c2d028dd05547e05c4b0efde1225ce454/docs/src/book/main.tex#L53879-L53895
[c7-mass]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AbelianVarietyTheory/BlockTheory/DivisorBase/ComponentMassSum.lean#L23-L60
[c7-global]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AbelianVarietyTheory/Proofs/DivisorProofs/SumComponentDegreesDivLeLatticeSlope.lean#L53-L77
