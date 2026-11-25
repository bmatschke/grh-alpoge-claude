# How much failure of integrality can the mean-slope argument tolerate?

Alpöge’s items 15 and 16 bring many theta periods into a common integral structure and compare their images. This suggests asking what the final average costs if some periods have denominators. The answer for the mean-slope argument is the logarithmic index of the vectors on which each period is integral, added over all words and divided by the total source rank. A denominator in a single direction of a large space can therefore cost very little. An analogous average pays for any excess in the archimedean operator heights. The estimates below are deductions for the human proof. Alpöge’s remark motivates the question. [Alpöge, items 15–16](https://alpo.ge/remark.pdf#page=4) · [The original use of both bounds, GFA7–8](global_assembly/main.tex#L452-L543)

## The two losses and their exact normalization

Work on one of the selected members over its totally complex coefficient field $K$. Write $N_i$ for the **shifted** integral word lattices and $C$ for the integral dual sharp-row lattice. The rational period maps are $B_i:N_{i,K}\to C_K$. Write $r_i=\operatorname{rank}N_i$, $R=\sum r_i>0$ and $n=\operatorname{rank} C>0$. Give all spaces their original archimedean metrics. For any word define its largest permissible integral sublattice by

$$
N_i'=\{v\in N_i:B_i v\in C\}.
$$

A common denominator of the images of finitely many module generators shows that $N_i'$ has finite index in $N_i$. At a finite place $w$, choose bases of the two original lattices over the discrete valuation ring. If the nonzero elementary divisors of the period matrix are $\pi_w^{e_1},\ldots,\pi_w^{e_m}$ up to units, then

$$
\operatorname{length}_{O_{K,w}} (N_i/N_i')_w
       =\sum_{j=1}^{m}(-e_j)_+ .
$$

Indeed the coordinate paired with $\pi_w^{e_j}$ must be divisible by $\pi_w^{(-e_j)_+}$. Kernel coordinates are unrestricted. Multiplying by the logarithms of residue-field sizes and summing gives $\log\#(N_i/N_i')$. This index is minimal among sublattices on which $B_i$ is integral. Its logarithm is zero exactly when the original map was integral. For example, elementary divisors $\pi_w^{-m},1,\ldots,1$ cost $m\log Nw$ at that place in any source rank. Clearing the entire lattice by $\pi_w^m$ would introduce that index cost in every direction. [Original finite-place test and finite exceptional set](continuation_v89/integral.tex#L78-L153)

Let $h_i$ be the assigned upper bound for the mean logarithm of the **squared** archimedean operator norm. For $B_i\ne0$ set $e_i^\infty=(h_\infty(B_i)-h_i)_+$ using the actual mean in these metrics. Set $e_i^\infty=0$ for a zero map. Define

$$
\Delta=\frac1R\left(\frac{2}{[K:\mathbb Q]}\sum_i\log\#(N_i/N_i')
                +\sum_i r_i e_i^\infty\right).
$$

The factor two is required because the reconstruction uses squared Hermitian slopes. Intersecting with the integral domain decreases the total degree by exactly the first term inside parentheses. Increasing the height allowances to $h_i+e_i^\infty$ decreases the sum of the adjusted slopes by the second term. The archimedean maps and metrics themselves are the same. [Native squared determinant/index formula, GLS.3](global_slope/main.tex#L39-L51) · [Classical height convention and slope inequality, Bost, Proposition 4.5](https://numdam.org/item/10.1007/s10240-001-8191-3.pdf#page=39)

## The mean-slope bound with losses

Assume that the original source slopes adjusted by $h_i$ have rank-weighted mean at least $s$ and are all at most $s+u$, with $u\ge0$. Assume that the target slopes are at least $s-H$, with $H\ge0$. At a fixed complex embedding suppose the period maps satisfy the following spanning estimate, with $a,\beta\ge0$, for every collection of subspaces $E_i$ of the complexified sources:

$$
 \operatorname{codim}_{C_{\mathbb C}}\sum_i B_i(E_i)
       \le a+\beta\sum_i\operatorname{codim}E_i .
$$

Then the mean target slope satisfies

$$
\boxed{\displaystyle
s-\mu(C)\le \frac{aH}{n}
    +\frac{\beta R}{n}\frac{H(u+\Delta)}{H+u}.}
$$

When $H+u=0$ the target floor already yields the conclusion, with the fraction set to zero. For the proof, pass to the integral maps $N_i'\to C$. A sublattice of $N_i'$ is contained with finite index in its saturation in $N_i$ on the same subspace. Its degree can only increase on saturation. Consequently the new adjusted slopes still have upper bound $s+u$, and their mean is at least $s-\Delta$ by the index calculation. For $0\le v\le H$, the source filtration of adjusted slope at least $s-v$ maps into the target filtration of slope at least $s-v$. This is the nonzero-map slope inequality applied to the lower-slope quotient. If $q(v)$ is the missing source dimension, the spanning estimate bounds the missing target dimension by $a+\beta q(v)$.

Integration in $v$ bounds the target mean deficit. The integral of $q(v)$ is the sum over the new adjusted slopes $\lambda$, counted with rank, of $\min(H,(s-\lambda)_+)$. For every $\lambda\le s+u$ this is at most $H(s+u-\lambda)/(H+u)$. The mean bound for $\lambda$ now gives the displayed formula. [The original filtration argument](gram_frame/gram_frame_section.tex#L84-L111)

On the scales of the reconstruction write $D$ and $M$ for the full analytic target and total source dimensions, $\tau=x^{-C_H}$ and $b=\exp(x^\varepsilon)$. On the eventual range of the original frame estimates we have $a\le6\tau D$, $\beta=4D/M$, $R\le M$, $n\ge(1-\delta)D$ with $\delta\le1/7$, and $H\le b/\tau$. Substituting gives

$$
s\le\mu(C)+5u+7b+5\Delta.
$$

In particular the arithmetic bound $\Delta\le b$ would give $5u+12b$ at this step. This replaces exact integrality and the individual height bounds **for this mean-slope deduction** by a single uniform bound on the measured losses. Establishing it for the selected theta maps remains arithmetic work. Any other use of the original assertions retains its own hypotheses. [Constants in the original comparison](gram_frame/gram_frame_section.tex#L113-L132)

There is also a way to recover the **original** frame conclusion for every permitted $H>0$. On the hypotheses of GFA8, put $\sigma=x^{-C_H}$. Take $s$ to be the actual adjusted mean and $u$ its original upper spread. With $a=D(5\sigma+4d+4\sqrt{e_0})$ and $\beta=4D/M$, the extra term compared with (GFA.21) is at most $4H\Delta/((1-\delta)(H+u))$. It is at most $4\Delta/(1-\delta)$. The published reconstruction of (GFA.22) already has an additive allowance $\log\#\mathrm{Word}$, left unused when deriving it from (GFA.21). Thus

$$
\Delta\le\tfrac14(1-\delta)\log\#\mathrm{Word}
$$

suffices for the literal (GFA.22) with the original error parameters, uniformly in $H$. Indeed, $uH/(H+u)\le u\log(1+H/u)$ for $u>0$, with both sides interpreted as zero for $u=0$. The original bounds on $d$ and $e_0$ handle the other terms exactly as in GFA8. This condition and $\Delta\le b$ serve different conclusions. The latter permits an additional $5b$ in the application at its chosen $H$. [The unused allowance and all-$H$ statement](global_assembly/main.tex#L537-L562)

## Measuring the angles without normalizing the period maps

Item 16 also points to a direct sufficient test for the spanning estimate. Choose any one inner product on the common complex target. Let $P_i$ be orthogonal projection onto $\operatorname{im}B_i$, let $S=\sum_iP_i$ and $r=\operatorname{tr}S$. For every subspace $L$ of the dual target, identified with a subspace of the target by this inner product, $\dim B_i^\vee(L)\ge\operatorname{tr}(P_LP_i)$. Indeed the compression $P_LP_iP_L$ has eigenvalues in $[0,1]$ and its rank is the rank of $P_i$ on $L$. Thus the largest shortfall in the dual spanning test is at most $\operatorname{tr}(I-\beta S)_+$. Here positive part is taken on the eigenvalues.

For $r>0$ and $\beta r/n\ge2$ the shortfall is at most

$$
n\left(\frac{n}{r^2}\sum_{i,j}\operatorname{tr}(P_iP_j)-1\right).
$$

To see this, take $z=n\lambda/r$ for each eigenvalue $\lambda$ of $S$. Then $(1-(\beta r/n)z)_+\le(1-z)^2$ for every $z\ge0$. Sum over the eigenvalues and expand $\operatorname{tr}(S^2)$. The sum over pairs is the classical fusion frame potential with unit weights. Cauchy–Schwarz gives the lower bound $r^2/n$, with equality precisely when the sum of projections is scalar. A bound on its excess on the actual arithmetic images therefore controls exactly the type of dimension loss used above. One may compute the projections from any full-column-rank bases of the image spaces. No sizes of the nonzero singular values are needed for this test. [Massey–Ruiz–Stojanoff, §2.2](https://arxiv.org/pdf/0811.3159#page=4) · [Equivalence of the primal and dual spanning estimates](PERIOD_IMAGE_SPANNING.md)

This last criterion concerns one summed second moment. A family-wide estimate on that moment is still needed if one uses this route. The original relative trace formula organizes the pairings of automorphic kernels into identity and other geometric contributions. Equating those kernels with the orthogonal projections onto the arithmetic images would itself need proof. [Original four-part kernel expansion and mixed estimate](actual_gram/actual_gram_section.tex)
