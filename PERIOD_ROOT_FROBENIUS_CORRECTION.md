# The quadratic Frobenius correction in the nonterminal root intersection

Let $v=u'=u_1-3n\eta_H$ be the shifted weight on a nonterminal component of entry 7. Write $f=|\Psi|$, $r+s=n$, $d=f\binom n2$, $F=L_v^{d+1}$ and $H=(d+1)D(L_v^d)>0$ in the sign convention $L_v=-\sum v_{\tau i}X_{\tau i}$. Write $W=\|v\|_\infty$, $U_\tau=v_{\tau,0}-v_{\tau,n-1}$ and $U=\sum_\tau U_\tau$. Use the row's smaller-block separation $g$, set $B=4fn^2(1+W/g)$, and take the fitted cutoff $N=\lfloor B\rfloor\ge128$. Here $1\le s<r$, $n\ge4$, and every index in the last $s$ positions is separated from every other index of its row by at least $g$. In the Frobenius remainder displayed in B8.26b, the entire degree-two contribution has a fixed negative sign. At the specified cutoff the whole remainder satisfies
$$
 \frac{|R_N(F)|}{H}
 \le \left(\frac{3}{10f}+\frac{2}{5f^2}\right)\frac{sU}{n^2}
 \le \frac{7sU}{10fn^2}.                                            \tag{1}
$$
The Roadmap uses $2sU$ for this term. Formula (1) concerns the explicit numerical series, for any of the allowed paths through the embeddings and any omission of bad primes. Its identification with an arithmetic intersection on the chosen model is a separate assertion. [Cutoff series and model identity](https://github.com/rh-lean-roadmap/rh-lean-roadmap/blob/dc5594a62bb2b94139788df817db693cd939a046/docs/src/book/main.tex#L20158-L20177) · [Original bound on the series](https://github.com/rh-lean-roadmap/rh-lean-roadmap/blob/dc5594a62bb2b94139788df817db693cd939a046/docs/src/book/main.tex#L50934-L50946) · [Spacing and size of the actual row](https://github.com/rh-lean-roadmap/rh-lean-roadmap/blob/dc5594a62bb2b94139788df817db693cd939a046/docs/src/book/main.tex#L53739-L53751)

## Exact degree-two contribution

Put $\bar v_\tau=n^{-1}\sum_i v_{\tau i}$ and define
$$
 C_\tau=\frac{\sum_i(v_{\tau i}-\bar v_\tau)^2}{n^2-1},\qquad
 b_\tau=\sum_{i<r}(v_{\tau i}-\bar v_\tau),\qquad
 J_\sigma=\sum_{j<r\le i}\frac1{v_{\sigma j}-v_{\sigma i}} .
$$
For a good prime $\ell>N$, a starting embedding $\tau$ and $h\ge1$, let $\sigma$ be the embedding underlying $\operatorname{Fr}_{\ell,h-1}(\tau)$, forgetting its side. The corresponding summand of $R_{N,2}(F)/H$ is
$$
 -\frac{\log\ell}{\ell^{2h}}
 \left(C_\tau J_\sigma+
 \mathbf 1_{\sigma=\tau}\frac{2b_\tau}{n^2-1}\right).                 \tag{2}
$$
In particular $C_\tau,J_\sigma>0$ and $b_\tau\ge0$. The dependence on $\sigma$ remains even though the choice of side has disappeared.

To prove (2), choose any homogeneous decomposition $F=\sum_{\tau,k}p_{\tau,k}Q_{\tau,k}$. In the degree-two term $P_{\ell,\tau,h,1}$ is either $\sum_{i<r}X_{\sigma i}$ or $-\sum_{i\ge r}X_{\sigma i}$. Their difference is a complete power sum $p_{\sigma,1}$, which pairs to zero under $D$ against $Q_{\tau,2}$. This follows by multiplying the alternating coefficient formula by the symmetric linear form, which forces a repeated exponent. In both cases we may use the negative sum over the last $s$ coordinates.

Here are the signed coefficient details. Let $G(v)$ be the product, over all embeddings, of the determinants with rows $v_{\tau i}^{m}/m!$ at exponents $m=n-1,n-2,\ldots,0$ and columns indexed by $i$. Multinomial expansion gives $D(L_v^d)=d!G(v)$. In the factor $\tau$, raise one exponent by two and sum the resulting determinants, retaining the factorial of each new exponent. All rows except the first two create a repeated exponent. Dividing by the unmodified determinant, the two surviving terms give
$$
 \frac{h_2(v_\tau)}{n(n+1)}-\frac{e_2(v_\tau)}{n(n-1)}=C_\tau .
$$
Indeed the recurrence $\prod_i(z-v_{\tau i})=0$ at the column values expresses $z^n$ and $z^{n+1}$ in the rows of smaller exponent. The two required diagonal coefficients are $-e_2$ and $e_1^2-e_2=h_2$.

Write $\partial_{\sigma,B}=\sum_{i\ge r}\partial/\partial v_{\sigma i}$. Then
$$
 \frac{2D((\sum_{i\ge r}X_{\sigma i})Q_{\tau,2})}{H}
   =-\frac{\partial_{\sigma,B}(C_\tau G(v))}{G(v)}.                 \tag{3}
$$
For the extraction identity, apply the sum of the raised-exponent alternating coefficient functionals in row $\tau$ to $X_{\sigma i}F$. Multiplication by $p_{\tau',k'}$ lowers one exponent by $k'$ in the alternating sum. The cancellation of repeated exponents and the opposite signs of interchanged rows leave precisely $2$ times the original alternating functional on $X_{\sigma i}Q_{\tau,2}$. This is the original signed power-sum extraction lemma, valid for every choice of the decomposition. Alternatively, evaluation of the same raised functional by multinomial expansion differentiates the raised determinant product at $v_{\sigma i}$. The single additional factor in $L_v^{d+1}$ gives the minus sign in (3), after division by $H=(d+1)!G(v)$. [Original alternant definitions and sign](https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/WeilBound/CoreStatements/FlagImmersions/AltCMul.lean#L15-L30) · [Original extraction identity](https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/WeilBound/CoreStatements/FlagImmersions/RestDegreePowerBound.lean#L158-L198)

A common shift in the last $s$ coordinates leaves all within-block differences unchanged in the Vandermonde product $G$. Thus $\partial_{\sigma,B}\log G=-J_\sigma$. Moreover $\partial_{\sigma,B}C_\tau=-\mathbf 1_{\sigma=\tau}2b_\tau/(n^2-1)$. Insert the negative small-block sum in (3) to obtain (2).

## Bounding the remaining degrees

Each row satisfies $C_\tau\le nU_\tau^2/[4(n^2-1)]$, by taking the midpoint of its range as a trial center for the least-squares deviation. Also $b_\tau=n^{-1}\sum_{j<r\le i}(v_{\tau j}-v_{\tau i})\le rsU_\tau/n$ and $J_\sigma\le rs/g$. Therefore the bracket in (2) is at most
$$
 sU_\tau\left(\frac{4U_\tau}{15g}+\frac{2}{15}\right)
 \le \frac{8}{15}sU_\tau(1+W/g),
$$
The quadratic coefficient uses $nr/[4(n^2-1)]\le4/15$, and the linear coefficient uses $2r/[n(n^2-1)]\le2/15$. Both follow from $r\le n$ and $n\ge4$. Finally $U_\tau\le2W$.

Let $k\ge2$. Every prime $\ell>N$ satisfies $\ell>B$. Rosser and Schoenfeld's unconditional estimate $\vartheta(t)<1.01624t$, followed by partial summation, gives $\sum_{\ell>B}(\log\ell)/\ell^2\le 2(1.01624)/B$. For the further powers use $\ell^{-(k-2)}\le B^{-(k-2)}$ and $(1-\ell^{-k})^{-1}\le (1-128^{-2})^{-1}$. It follows that
$$
 \sum_{\ell>N}(\log\ell)\sum_{h\ge1}\ell^{-hk}
 \le \frac{9}{4B^{k-1}} .
$$
Taking $k=2$ and summing the preceding bracket over $\tau$ gives $|R_{N,2}(F)|/H\le 3sU/(10fn^2)$. [Rosser and Schoenfeld, *Approximate formulas for some functions of prime numbers*, Theorem 9, equation (3.32)](https://denisevellachemla.eu/Rosser-Schoenfeld-1962.pdf#page=8)

For $k\ge3$ the original coefficient estimate bounds $k|D(P_{\ell,\tau,h,k-1}Q_{\tau,k})|/H$ by $sU_\tau(2D_*)^{k-1}/k!$, with $D_*=n(1+2W/g)$. In its proof the row is translated before taking absolute values, and the complete power sum can again be discarded. Keep the full ratio $x=2D_*/B\le1/(fn)\le1/4$. Since the successive ratios in $\sum_{k\ge3}x^{k-1}/k!$ are at most $1/16$, the sum is at most $(8/45)x^2$. The prime bound now gives $|R_{N,\ge3}(F)|/H\le2sU/(5f^2n^2)$. Adding the two estimates proves (1). [Original single-coordinate coefficient estimate](https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/WeilBound/CoreStatements/FlagImmersions/RestDegreePowerBound.lean#L212-L248)

## The Hodge calibration at the partial-flag wall

The signed calculation also evaluates the quadratic remainder for the Hodge test used to calibrate the first-order part of the intersection. Put $a=rs$, $e=fa$, $m=d-e$ and $\mu=\sum_{\tau,i\ge r}X_{\tau i}$. Let $J(X)$ be the product, at all embeddings, of the differences $X_{\tau j}-X_{\tau i}$ over $i<j$ lying in the same one of the two blocks. The test and its normalization are $F_*=\mu^{e+1}J$ and $H_*=(e+1)D(\mu^eJ)>0$. Fix the partial-wall weight $v^0$ with all first-block entries zero and all second-block entries $-1$. Then $L_{v^0}=\mu$.

Write $J(\partial_v)$ for the constant-coefficient differential operator obtained by replacing $X_{\tau i}$ by $\partial/\partial v_{\tau i}$ in this precise product. Differentiating the powers of $L_v$ gives
$$
 J(\partial_v)F(v)\big|_{v^0}=\gamma F_*,
 \qquad J(\partial_v)H(v)\big|_{v^0}=\gamma H_*,
 \qquad \gamma=(-1)^m\frac{(d+1)!}{(e+1)!}.
$$
For the second equality, differentiate $H(v)=(d+1)D(L_v^d)$ under the linear functional $D$. The degree-two summand at a fixed $(\ell,\tau,h)$ is also a linear functional in $F$, by the raised-exponent extraction. Multiply (2) by $H(v)$ before applying $J(\partial_v)$. Its right side extends across $v^0$ because every cross-block gap is $1$ there. The within-block Vandermonde divides $H(v)$ and vanishes there to order $m$. Every derivative of $H(v)$ of order below $m$ therefore vanishes at $v^0$. In the product rule all $m$ derivatives must land on $H(v)$ for a nonzero term. This proves that the normalized quadratic summand for $F_*/H_*$ equals the right side of (2) at $v^0$.

At this weight $C_\tau=a/[n(n^2-1)]$, $b_\tau=a/n$ and $J_\sigma=a$. Thus the quadratic summand on the normalized Hodge test is exactly
$$
 -\frac{\log\ell}{\ell^{2h}}\,
 \frac{a(a+2\mathbf 1_{\tau=\sigma})}{n(n^2-1)}.                 \tag{5}
$$
For $k\ge3$, B8.26d bounds the normalized absolute coefficient of the Hodge test by $X^{k-1}/k!$, where $X=2(a+n)\le3n^2/2$. Since $X/B\le3/(8f)$, the same prime bound gives
$$
 \frac{|R_{N,\ge3}(F_*)|}{H_*}
 \le\frac94 f\,\frac{(3/(8f))^2}{6(1-3/32)}
 <\frac{3}{50f}.
$$
Here the ratio of consecutive terms is at most $(3/8)/4=3/32$. Dropping the negative contribution (5) gives the one-sided bound $R_N(F_*)/H_*\le3/(50f)$ at the fitted cutoff. [Hodge test and its normalization](https://github.com/rh-lean-roadmap/rh-lean-roadmap/blob/dc5594a62bb2b94139788df817db693cd939a046/docs/src/book/main.tex#L20119-L20135) · [Hodge-test coefficient estimate](https://github.com/rh-lean-roadmap/rh-lean-roadmap/blob/dc5594a62bb2b94139788df817db693cd939a046/docs/src/book/main.tex#L50883-L50894)

## A single comparison of arithmetic intersections at the cutoff

The new estimate can be used without determining the two first-order coefficients separately. For a homogeneous polynomial $Y$ let $I(Y)=P_N(Y)/V$ be the actual normalized arithmetic functional and let $E(Y)=h_{\rm fl}(Y)+R_N(Y)$. Use the flat test $Y_0=p_{\tau_0,1}Q_1$ with $D(Q_1)=1$ and the Hodge test $Y_H=F_*/H_*$ of B8.26a,b. Write $S_0=\sum_{\tau,i<r}v_{\tau i}$ and $b_0=\sum_\tau b_\tau$, and set $a_0=S_0/r$, $a_H=nb_0/(rfs)\ge0$. Then
$$
 Y=F/H+a_0Y_0-a_HY_H
$$
is annihilated by both first-derivative functionals $S$ and $T$ of B8.26b. Indeed their respective values on $F/H$, $Y_0$, $Y_H$ are $(-S_0,-\sum v_{\tau i})$, $(r,n)$, and $(0,fs)$. Thus at this single cutoff it is sufficient to prove $I(Y)\ge E(Y)-\epsilon$ for this one class, with $T_*\epsilon=O(E_p)$, and to supply the two scalar test heights. Since $E(Y_0)=0$, this gives
$$
 \frac{P_N(F)}{VH}\ge
 \frac{h_{\rm fl}(F)}{H}-\frac{7sU}{10fn^2}
 -a_0 I(Y_0)+a_H\bigl(I(Y_H)-E(Y_H)\bigr)-\epsilon.               \tag{4}
$$
This permits a one-sided scalar comparison on a single mixed class of the actual normalized flag models. The full tower identity implies it with $\epsilon=0$. Here $|a_0|\le\|v\|_1/r$, and $0\le b_0\le\|v\|_1$ follows from the row averages. The established flag and remainder estimates give $h_{\rm fl}(F)\ge0$ and $E(Y_H)\le\frac12fs\log(n+1)+3/(50f)$. Consequently the two geometric measurements $|I(Y_0)|\ll n\lambda_N$ and $I(Y_H)\ge-Cfs\lambda_N$ suffice in (4), as $n/r\le2$. The fitted row satisfies $sU\le6\|v\|_1$, so its Frobenius correction costs at most $21\|v\|_1/(5fn^2)$. [Flat and Hodge tests](https://github.com/rh-lean-roadmap/rh-lean-roadmap/blob/dc5594a62bb2b94139788df817db693cd939a046/docs/src/book/main.tex#L50881-L50914)

Equation (2) and estimate (1) are proved for the stated series. For (4) on the actual arithmetic model one must still match the smoothed, normalized root-line intersections to $E$ on $Y$ to the indicated precision and bound the two test heights with the prescribed metrics and finite integral structures. No estimate of a numerical Frobenius series identifies those model intersections by itself. The [record trace and carrying-section comparison](PERIOD_RECORD_TRACE_TO_CHOW.md) then transfers the bound to the component heights under its model and section hypotheses.

## Inserting the two scalar estimates

On the admitted, matched cutoff models of the [flat determinant](PERIOD_FLAT_SCALAR_AT_CUTOFF.md) and [base Hodge calculation](PERIOD_HODGE_TEST_ON_BASE.md), write $C=C(S_N)$, $u_E=\log\operatorname{rd}(E)$, $h_0=(r-s)\log\Omega/2$, and $a_0^\pm=\max(\pm a_0,0)$. Set
$$
 B_0=a_0h_0+a_0^+r(C+u_E)+a_0^-sC,\qquad
 B_H=(C_h+1)fs\lambda_N+\tfrac12fs\log(n+1)+\frac{3}{50f}.
$$
The interval for the flat height gives $a_0 I(Y_0)\le B_0$ for either sign of the fitted row sum. The [cusp mean](PERIOD_HODGE_CUSP_MEAN.md) and corrected horizontal-height bound give $I(Y_H)-E(Y_H)\ge-B_H$. With $U=\operatorname{spr}(v)$ the spread of the fitted weight, inequality (4) now reads
$$
 \frac{P_N(F)}{VH}\ge\frac{h_{\rm fl}(F)}H-
       \frac{7sU}{10fn^2}-B_0-a_HB_H-\epsilon .
$$
The only extra intersection estimate in this implication is $I(Y)\ge E(Y)-\epsilon$ for the single class $Y$ with both first derivatives zero. If the determinant comparison on a component has a negative normalized defect, use its $V_Z$-weighted mean absolute negative part in $B_H$. The implication still requires realization of the named model, lattice, metric and height data on the selected family and the required error budget for $\epsilon$.
