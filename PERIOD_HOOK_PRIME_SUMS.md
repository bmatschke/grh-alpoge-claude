# The hook contribution at the actual arithmetic cutoff

Consider the signed sufficient inequality (10) for period-height entry 7 in [the sharp determinant calculation](PERIOD_RELATIVE_DETERMINANTS.md). Write $F=K^{\bar{}}$, and let $J_i$ be the fractional ideal in that field for level $i$, $D_i$ its row rank and $E_{Q,i}$ its conjugate-embedding correction. Work first at $i=1$. The [character comparison](PERIOD_SIGNED_LEVEL_TRANSFER.md) also permits $i=0$ under its fitted-row hypotheses. Throughout the family parameter $\varepsilon>0$ is fixed.

## The rational hook and the special primes

Let $\mathcal P$ be the list of the positive and negative partitions in every layer $j$ and real label $\rho$, with their specified lengths. Set $h=\prod_{\lambda\in\mathcal P}\operatorname{Hook}(\lambda)$ and $B=\sum_{\lambda\in\mathcal P}|\lambda|$. Each embedding representative used in the metric calculation agrees on the distinguished quadratic field and permutes the real labels with their signatures. The two partitions are given by the corresponding transported row coordinates. The full list of factors therefore has the same product at every representative, and the integer denoted $\mathcal H$ in (10) equals $h^{[K:\mathbb Q]}$. This gives the single fractional ideal $(h)^{D_i}J_i$ over $F$. In particular any norm used below includes all residue degrees. [Partitions at the transported labels][part] · [Permutation of labels][perm]

More precisely, let $Y=X''=|A|x\exp(x^{\varepsilon/3})$ and let
$$
 M_d=(k-1)\sum_{j=1}^m\sum_{t\in A}\min\{w_j(0,t),w_j(1,t)\},
 \qquad \eta=(g_0g_1)^B d^{M_d}.
$$
The weights $w_j$ are integral at these points. At each of the two marked type primes $g_0,g_1$, the base term in layer $j$ equals minus one half its total Fock degree. The prescribed pair of rows identifies that degree with the box count in the two partitions at all its labels. At the host prime $d$ the base term is minus one half the corresponding summand of $M_d$. The place weights on a full fibre over $p$ satisfy $\sum_{w\mid p}e_w\ell_w=\log p$. The identification of the base terms puts the whole nonzero fibre in the twist set. All other base terms are supported at $p\le Y$. Thus, with $F_j(p)$ the value in B4.02 and $F_{\rm ord}=\sum_{p\le Y,\,p\notin\{g_0,g_1,d\}}\sum_j F_j(p)\log p$,
$$
 2F_*=-\log\eta+2F_{\rm ord}.
$$
In particular the sign of the marked powers in the numerator below is positive. The sufficient test at level $i$ is
$$
 \frac{\log N_F\big((h\eta)^{D_i}J_i\big)}{D_i[F:\mathbb Q]}
 -\frac{E_{Q,i}}{D_i}-2F_{\rm ord}
 -\sum_{j,\rho}\beta_j w_{j\rho}\log\Omega
 \ \le\ C mL(B_0+N_c).                                      \tag{1}
$$
This rewriting is exact. At either $g_a$, the rational hook is a unit for every sufficiently large member. Indeed each hook is at most the largest row entry plus its number of rows, hence at most $x^C b$ for a fixed family constant $C$, whereas $g_a\ge(kb)^8$. The whole exponent contributed there by $h\eta$ is $B$. No local sign or cancellation for $J_i$ has been assumed. [Base terms][terms] · [Integral weights][weights] · [Fock degrees and the full fibre][fibres] · [Moving sizes][size]

The coefficient of the CM period can likewise be retained without reconstructing diagrams. With $P=k+j-1$, $Q=m-j$, $u=(t_{\rm ch}+1)/2$ and the indexed interlacing and auxiliary coordinates $v_s,b_\ell$ at one label, the box count at $(j,\rho)$ is
$$
 B_{j\rho}=(P-Q)w_j(\rho)+\sum_{s=0}^{k-2}v_s
 -\sum_{\ell=0}^{j-1}b_\ell+\sum_{\ell=j}^{m-1}b_\ell
 -\binom P2-\binom Q2-(P+Q)u .
$$
Sum the entries of the big row and the negatives of the entries of the small row in B4.02z. Reversing the latter to form the partition preserves their sum. Here $\beta_j=P-Q$. This identity distinguishes the total box coefficient $B$ at the marked primes from the coefficient $\sum\beta_j w_{j\rho}$ of $\log\Omega$. [Weight coordinates][weights] · [Arithmetic coefficient][beta]

## A uniform estimate on every subset of primes below the cutoff

For a partition of length $l$, set $a_r=\lambda_r+l-r$ for $1\le r\le l$. The $a_r$ are strictly decreasing and nonnegative. Define $A_0=\max(2,\max_{\lambda,r}a_r)$, $R=\sum_\lambda l$ and $Q_0=\sum_\lambda\binom l2$. Empty partitions contribute zero to these last two sums. The source's factorial formula and counting multiples of powers of $p$ give
$$
 v_p(\operatorname{Hook}(\lambda))=
 \sum_{r=1}^l\frac{a_r-s_p(a_r)}{p-1}-
 \sum_{r<s} v_p(a_r-a_s),
$$
where $s_p$ is the base-$p$ digit sum. Equivalently the last sum counts the unordered index pairs that coincide modulo each $p^t$, summed over $t\ge1$. All factors are positive integers before the factorial quotient is taken. [Hook formula in the original normalization][hook]

For arbitrary real choices $0\le c_p\le1$ the following estimate is uniform, including when $c_p$ depends on the member or its serving tuples:
$$
 \left|\sum_{p\le Y}c_p
 \left(v_p(h)-\frac{B}{p-1}\right)\log p\right|
 \ll Q_0\{\log^2(2Y)+\log(2A_0)\}
       +RY\log(2A_0Y).                                        \tag{2}
$$
The shift from $\lambda_r$ to $a_r$ adds $Q_0$ boxes in the factorial numerators and costs at most $Q_0\sum_{p\le Y}\log p/(p-1)$. Bounding by the sum over integers gives the first logarithm squared. Each digit sum divided by $p-1$ is at most $1+\log A_0/\log p$, so the digit costs at most $R Y\log(2A_0Y)$. The total valuation cost of each Vandermonde factor over any subset of primes is at most its log, bounded by $\log A_0$. These three bounds also work for the sum of the absolute discrepancies over primes. Since $R,Q_0,\log A_0$ grow at most polynomially in $x$ and $Y=|A|x\exp(x^{\varepsilon/3})$, the right side is $o(b/x^N)$ for every fixed $N$. In particular the digit, shift and Vandermonde errors cost less than the original budget **even when every ordinary prime is selected separately**. For a selection of primes of $F$ over $p$, use $c_p=\sum_{\mathfrak v\ {\rm selected}} e_{\mathfrak v} f_{\mathfrak v}/[F:\mathbb Q]$ for the rational hook term. The actual $J_i$ still uses its own valuations. [Cutoff and window][window]

## The complement of the cutoff

Use $\varphi(t)=t\log t-t$ with $\varphi(0)=0$ and write $\Phi=\sum_{\lambda,r}\varphi(\lambda_r)$. Stirling's estimate (or the elementary integral comparison for $\log n!$) gives $\log h=\Phi+O((R+Q_0)\log(2A_0))$. Indeed replacing each $a_r$ by $\lambda_r$ costs at most $O((l-r)\log(2A_0))$ in $\varphi$, treating the interval from zero to one directly. The Vandermonde denominator contributes at most $Q_0\log A_0$. Combining this with (2) gives an estimate of the entire tail, including all prime powers.

At the actual $Y$ its main term has a closed form. Unconditionally, for an absolute $c>0$,
$$
 \sum_{p\le Y}\frac{\log p}{p-1}=\log Y-\gamma+
 O\big(\exp(-c\sqrt{\log Y})\big).
$$
For details, partial summation of $\psi(t)=t+O(t\exp(-c_0\sqrt{\log t}))$ gives $\sum_{n\le Y}\Lambda(n)/n=\log Y+C+O(\exp(-c_1\sqrt{\log Y}))$ with smaller positive constants. In the Laplace transform at $s>0$, this implies $-\zeta'(1+s)/\zeta(1+s)=1/s+C+o(1)$ as $s\downarrow0$, so the Laurent expansion gives $C=-\gamma$. Extending the prime-power sum to all powers of primes $p\le Y$ costs $O(\log(2Y)/\sqrt{Y})$. For $p\le\sqrt Y$ the first omitted power contributes at most $1/Y$ before the logarithm and the geometric tail factor is at most two. For $p>\sqrt Y$ start at $p^{-2}$ and sum over integers. Because $B\le x^C b$ and $\log Y\ge x^{\varepsilon/3}$, the PNT error multiplied by $B$ is $o(b/x^N)$ for every fixed $N$. This application uses an unconditional estimate for the ordinary Chebyshev function. [Fiori, Kadiri and Swidinsky, Theorem 1][pnt]

We obtain the two absolute estimates
$$
 \begin{aligned}
 \sum_{p\le Y}v_p(h)\log p &= B(\log Y-\gamma)+o(b/x^N),\\
 \sum_{p>Y}v_p(h)\log p &= \Phi-B(\log Y-\gamma)+o(b/x^N).
 \end{aligned}                                                   \tag{3}
$$
For a selected subset the finite explicit sum in (2) is required. A prime number theorem for a changing Frobenius class is unnecessary for (2); using the full-set main term for a selected subset would require another estimate.

Equations (1)–(3) evaluate the hook term and the special-prime main terms to the precision required by entry 7. For example, at all ordinary $p\le Y$ the difference between the hook valuation and the known ordinary base term is given to that precision by the finite sum with coefficients $B/(p-1)-2\sum_j F_j(p)$. At $d\le Y$ the hook contribution also occurs in (3), while its special-prime base term is already in $\eta$. To finish (1) one needs an upper bound for the signed sum including the actual relative theta ideal $J_i$ and the embedding correction. The calculation does not determine those valuations. The [base-level signed test](PERIOD_SIGNED_LEVEL_TRANSFER.md) expresses their combined effect in intrinsic lattice terms.

[part]: https://github.com/rh-lean-roadmap/rh-lean-roadmap/blob/02a95b4c62db610642af5f278ee5d0d6df87b348/docs/src/book/main.tex#L8862-L8876
[perm]: https://github.com/rh-lean-roadmap/rh-lean-roadmap/blob/02a95b4c62db610642af5f278ee5d0d6df87b348/docs/src/book/main.tex#L32419-L32427
[terms]: https://github.com/rh-lean-roadmap/rh-lean-roadmap/blob/02a95b4c62db610642af5f278ee5d0d6df87b348/docs/src/book/main.tex#L6281-L6307
[weights]: https://github.com/rh-lean-roadmap/rh-lean-roadmap/blob/02a95b4c62db610642af5f278ee5d0d6df87b348/docs/src/book/main.tex#L6187-L6210
[fibres]: https://github.com/rh-lean-roadmap/rh-lean-roadmap/blob/02a95b4c62db610642af5f278ee5d0d6df87b348/docs/src/book/main.tex#L31858-L31903
[beta]: https://github.com/rh-lean-roadmap/rh-lean-roadmap/blob/02a95b4c62db610642af5f278ee5d0d6df87b348/docs/src/book/main.tex#L8989-L9004
[hook]: https://github.com/rh-lean-roadmap/rh-lean-roadmap/blob/02a95b4c62db610642af5f278ee5d0d6df87b348/docs/src/book/main.tex#L8794-L8806
[window]: https://github.com/rh-lean-roadmap/rh-lean-roadmap/blob/02a95b4c62db610642af5f278ee5d0d6df87b348/docs/src/book/main.tex#L5520-L5533
[size]: https://github.com/rh-lean-roadmap/rh-lean-roadmap/blob/02a95b4c62db610642af5f278ee5d0d6df87b348/docs/src/book/main.tex#L32985-L33010
[pnt]: https://arxiv.org/abs/2204.02588
