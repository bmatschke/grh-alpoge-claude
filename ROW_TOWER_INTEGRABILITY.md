# Absolute convergence and square integrability with several source cusp parameters

Write $a,n$ for the two source dimensions, $d=a+n$ for the target dimension, $e=(a-n)/2$ and $D=[E:\mathbf Q]$. Put $y=p+q$. The big source, small source and target have signatures $(a-p,p)$, $(q,n-q)$ and $(d-y,y)$ at every real place. In the grid range $e,n>2y+1$. Their rational Witt indices are $p,q,y$. Indeed at each successive step the remaining indefinite Hermitian norm form has dimension at least six over $F$, so it is isotropic at every finite place and every real place. Hasse–Minkowski and rational Witt splitting give the next hyperbolic plane, until a definite real signature bounds the index. For the skew-Hermitian target first multiply by the fixed totally imaginary scalar. [Grid inequalities][g-rank] · [Rational splitting](ROW_BETA_RATIONAL_PLANES.md)

For a target Siegel representative with ordered parameters $T_1\ge\cdots\ge T_y\ge0$, let $\mathcal A_{b}(T),\mathcal A_s(T)$ stand for the integrals of the **absolute values** of the two theta kernels over their respective source quotients, with any allowed target compact factor. The big finite test is unrestricted. The small finite test is primed at its prescribed split place, so its barred matrix test is supported on matrices of full row rank. On fixed finite factors the estimates are
$$
 \mathcal A_b(T)\ll P_b(f_b)\exp\!\left(\frac D2a\sum_{j=1}^{y}T_j\right),\qquad
 \mathcal A_s(T)\ll P_s(f_s)\exp\!\left[\frac D2\left(a\sum_{j=1}^{q}T_j+(n-2q)\sum_{j=q+1}^{y}T_j\right)\right].
 \tag{1}
$$
Here $P_b,P_s$ are continuous archimedean Schwartz seminorms, and the constants may depend on the finite tests and the compact sets. Both majorants belong to target $L^2$ against the corresponding Siegel density. The proof below gives the second estimate uniformly in the number of cusp parameters in the sense of a single formula. It makes no assertion that numerical constants are uniform as the row varies.

## The full-rank estimate in individual coordinates

For a source of dimension $r$ and rational Witt index $h$, let $S_1\ge\cdots\ge S_h\ge0$ be its chamber coordinates. The source and target torus weights are respectively $\{\pm S_i,0^{r-2h}\}$ and $\{\pm T_j,0^{d-2y}\}$. The sum of the positive parts of all their pairwise sums equals
$$
 W_r(S,T)=d\sum_i S_i+r\sum_jT_j-2\sum_{i,j}\min(S_i,T_j).
 \tag{2}
$$
Indeed the four signed weights from $S_i,T_j$ contribute $2\max(S_i,T_j)$, and adding the zero-weight contributions gives (2). Poisson summation for the squared theta function gives a sum of Schwartz matrix coefficients indexed by rational $r\times d$ matrices. The fixed compact factors enlarge finite supports by a compact set and archimedean norms by a fixed factor. In rational Witt coordinates there is consequently a common denominator $m_0$. For a single entry with weight $u$, a rapidly decreasing majorant on $m_0^{-1}\mathcal O_E$ sums to $O(\exp(D\max(u,0)))$, by counting lattice points in dyadic balls in the Minkowski embedding. Multiplying these estimates over all entries gives the squared-kernel bound $C P(f)^2\exp(D W_r)$. [Weights and chamber measure][g-weights] · [Squared theta coefficient formula][g-sq] · [Denominators, diagonal coordinates and lattice count][g-lattice] · [Compact factors and seminorms][g-compact]

For the small source, full rank can be imposed in this coefficient sum. Partition the barred local test at the distinguished place into finitely many pieces on compact open balls $C$ so small that $C+C$ is full rank. This follows from openness of full rank and the fact that $2Y$ has full rank for every $Y$ in the support. Pair each piece with its reflection in the product expressing the squared theta value. The two theta values agree by rational negation. A nonzero coefficient requires a translation in the sum of the two supports before reflection, up to sign and invertible changes of basis in the split matrix chart. Its rational indexing matrix therefore has full row rank. Apply the estimate to each piece and use the triangle inequality on their theta values. [Reflection in the theta sum][g-reflect] · [Split support and its transfer to rational matrices][g-cut]

Define
$$
 \Delta(S,T)=\max\bigl(0,\max_{1\le i\le q}(S_i-T_i)\bigr)
$$
with value zero for $q=0$. For every integer $M\ge0$ the squared small kernel has the stronger bound
$$
 C_M P_M(f)^2\exp\bigl(DW_n(S,T)-M\Delta(S,T)\bigr). \tag{3}
$$
To prove it, write $X$ for a contributing rational matrix in the two fixed Witt bases. For a given $i\le q$, take the $i$ source rows expanded by $e^{S_1},\ldots,e^{S_i}$ in the inverse torus action. These rows are independent. They admit a nonzero $i\times i$ minor. At most $i-1$ target columns have contracting weight $\lambda>T_i$, so at least one column of that minor has weight $\lambda\le T_i$. That column has a nonzero entry $x$ in one of the selected rows, say the $k$th. Since $m_0 x$ is a nonzero algebraic integer, some complex embedding has $|x|\ge m_0^{-1}$. One may use its chosen representative at the underlying real place since complex conjugation preserves modulus. The size of the scaled matrix in these coordinates is thus at least $m_0^{-1}e^{S_k-\lambda}\ge m_0^{-1}e^{S_i-T_i}$, up to fixed norm equivalence. Maximizing over $i$ gives $1+\|X_{S,T}\|\gg e^{\Delta}$. Allocate $M$ extra Schwartz powers to this bound and the original lattice sum still converges. This proves (3). The pinned minor estimate uses the determinant and the excess of prefix sums. The entry estimate above uses the same rational basis and denominator, recording which target columns can occur in a nonzero minor. For two source directions this controls $S_2-T_2$ even when $S_1+S_2\le T_1+T_2$. [Nonzero minors and an archimedean lower bound][g-min1] · [Inverse torus applied to these entries][g-min2] · [Allocating extra Schwartz powers][g-decay]

## Integrating the source parameters

The source density contributes $\exp(-D\rho_r(S))\,dS$, where $\rho_r(S)=\sum_i(r-2i+1)S_i$ in one-based indexing. After taking the square root of (2)'s kernel estimate, the exponent including density and divided by $D$ is
$$
 H_r(S,T)=\frac r2\sum_jT_j+\sum_{i=1}^h\bigl(d/2-r+2i-1\bigr)S_i-\sum_{i,j}\min(S_i,T_j).
 \tag{4}
$$
For $r=a$, discard the final nonpositive term. Set $v_k=S_k-S_{k+1}$, $S_{p+1}=0$. The coefficient of $v_k$ in the remaining source exponent is $\sum_{i=1}^k(-e+2i-1)=-k(e-k)$. The resulting source chamber integral costs at most $\prod_{k=1}^p [D k(e-k)]^{-1}$, proving the big estimate when $e>p$. The empty product covers the compact source.

For $r=n$, every one-sided slope of (4) in $S_i$ is between $L=e+1-y>0$ and $U=e+2q-1$. Indeed it is $e+2i-1$ less the number of $T_j$ above the moving coordinate, with either adjacent slope allowed at a tie. For fixed $T$, the maximum on $0\le S_i\le T_i$ occurs at $S_i=T_i$ for every $i\le q$. Denote this point by $T_{\le q}$. Equation (4) is a sum of functions of individual $S_i$, so the slope bounds also give on the entire chamber
$$
 H_n(S,T)\le H_n(T_{\le q},T)-L\sum_i(T_i-S_i)_++U\sum_i(S_i-T_i)_+.
$$
In the square root of (3) choose $M\ge 2qD(U+L)$, using $\sum_i(S_i-T_i)_+\le q\Delta$. The resulting integrated absolute-value majorant is bounded by
$$
 C P(f)\exp\bigl(D H_n(T_{\le q},T)\bigr)\int_{\mathbf R^q}\exp\!\left(-DL\sum_{i=1}^q|S_i-T_i|\right)dS
 = C P(f)\left(\frac{2}{DL}\right)^q \exp\bigl(DH_n(T_{\le q},T)\bigr).
$$
The enlarged domain removes dependence of the integral on the chamber walls. Finally $\sum_{i,j\le q}\min(T_i,T_j)=\sum_{i=1}^q(2i-1)T_i$, and $\sum_{i\le q,\,j>q}\min(T_i,T_j)=q\sum_{j>q}T_j$. Substitution in (4) gives exactly the small exponent in (1). For $q=0$ there is only the compact source integral, and the formula gives $n\sum T_j/2$. [Positive weights as a sum of minima][g-sum] · [Multiplicity of a self-minimum][g-self] · [Source chamber integration][g-chamber]

## The target integral and two mixed-signature examples

The target density is $\exp(-D\sum_{j=1}^y(d-2j+1)T_j)\,dT$. Put $u_k=T_k-T_{k+1}$ with $T_{y+1}=0$. After multiplying by the squared big bound in (1), the coefficient of $-Du_k$ is $B_k=k(n-k)$. For the squared small bound it is
$$
 C_k=\begin{cases}
 k(n-k),&1\le k\le q,\\
 q(n-q)+\ell(a-\ell),&k=q+\ell,\quad 1\le\ell\le p.
 \end{cases}
$$
Indeed the small bound leaves the decay coefficients $n-2j+1$ for the first $q$ target coordinates and $a-2\ell+1$ for the next $p$, and passage to $u$ takes their prefix sums. All coefficients are positive in the grid range. The positive-orthant integrals are $D^{-y}\prod_{k=1}^y B_k^{-1}$ and $D^{-y}\prod_{k=1}^y C_k^{-1}$. [Rank-one roots and Haar chamber density][g-weights] · [Passage from torus bounds to adelic quotient integrals][g-quot]

| Upper square | Small-source bound, exponent after removing $D/2$ | Big target decay coefficients in $u$ | Small target decay coefficients in $u$ |
|---|---|---|---|
| $(0,2)$ | $a(T_1+T_2)$ | $n-1,\ 2(n-2)$ | $n-1,\ 2(n-2)$ |
| $(1,2)$ | $a(T_1+T_2)+(n-4)T_3$ | $n-1,\ 2(n-2),\ 3(n-3)$ | $n-1,\ 2(n-2),\ 2(n-2)+a-1$ |

The estimates prove source absolute convergence at every target argument, polynomial growth in target height, and square integrability of each original theta integral and every finite linear combination. The seminorm estimate also applies after fixing different finite factors or any fixed compact set of target translates. At $(1,2)$, using the bound for the compact big source from $(0,2)$ would miss the source integration. Its single chamber variable is controlled by $e>1$ in (4). [Torus height and quotient reduction][g-height]

[g-rank]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AbelianVarietyTheory/BlockTheory/DivisorBase/WeilTensorModels.lean#L360-L369
[g-weights]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/WeilBound/ThetaLifts/FrameEstimates/SquareIntegrableWeilRange.lean#L50-L69
[g-sq]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/WeilBound/ThetaLifts/FrameEstimates/SqAllC.lean#L62-L87
[g-lattice]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/WeilBound/ThetaLifts/FrameEstimates/LatTor.lean#L118-L158
[g-compact]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/WeilBound/ThetaLifts/FrameEstimates/InitialPairs/SquareIntegrableOfLatticeTorus.lean#L44-L67
[g-reflect]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/WeilBound/ThetaLifts/FrameEstimates/ThetaSumNeg.lean#L75-L125
[g-cut]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/WeilBound/ThetaLifts/FrameEstimates/HermitianFormDetNeZero.lean#L90-L153
[g-min1]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/WeilBound/ThetaLifts/FrameEstimates/ExistsColsDetNeZero.lean#L13-L38
[g-min2]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/WeilBound/ThetaLifts/FrameEstimates/ExistsColsDetNeZero.lean#L84-L143
[g-decay]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/WeilBound/ThetaLifts/FrameEstimates/LatFull.lean#L13-L46
[g-sum]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/WeilBound/ThetaLifts/FrameEstimates/InitialPairs/SquareIntegrableIntegralHolds.lean#L94-L104
[g-self]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/WeilBound/ThetaLifts/FrameEstimates/InitialPairs/SquareIntegrableIntegralHolds.lean#L180-L192
[g-chamber]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/WeilBound/ThetaLifts/FrameEstimates/InitialPairs/SquareIntegrableIntegralHolds.lean#L58-L92
[g-quot]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/WeilBound/ThetaLifts/FrameEstimates/InitialPairs/SquareIntegrableOfLatticeTorus.lean#L69-L129
[g-height]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/WeilBound/ThetaLifts/FrameEstimates/SquareIntegrableWeilRange.lean#L61-L73
