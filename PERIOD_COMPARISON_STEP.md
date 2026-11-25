# The adelic height of a theta period

For the slope estimate, the image of a rational period and the direction of the map matter. Multiplying that map by a nonzero field element leaves both unchanged. A bound that charges separately for its denominator and its large archimedean norms can nevertheless assign an arbitrarily large cost to this operation. Bost's height of a rational linear map combines the two contributions before comparing them with the height allowance. Huang's Arakelov account of the Alpöge–Claude argument uses exactly this height in squared-norm conventions. Below we apply it to the original word lattices and to the rank-weighted mean required by the reconstruction. [Bost, §4.1.4 and Proposition 4.5](https://numdam.org/item/10.1007/s10240-001-8191-3.pdf#page=39) · [Huang, §2.2.1, equation (2.2.1)](https://hexagonmath.org/pdf/2611.00833v1#page=5)

## Computing the finite part on the actual lattices

Let $K$ be the coefficient field, $d_K=[K:\mathbb Q]$, $N_i$ a shifted integral word lattice and $C$ the integral dual sharp-row lattice. For a nonzero rational period $B_i:N_{i,K}\to C_K$ and any finite place $w$, put
$$
 m_{iw}=\max\{m\in\mathbb Z:B_i(N_{i,w})\subseteq\mathfrak p_w^m C_w\}.
$$
In bases of the two local lattices this is the minimum valuation of the nonzero matrix entries. It vanishes outside a finite set since a fixed nonzero rational matrix and its lattices are integral with unit content at almost all primes. The fractional ideal $J_i=\prod_w\mathfrak p_w^{m_{iw}}$ is the smallest fractional ideal with $B_i(N_i)\subseteq J_i C$. Put
$$
 f_i=-\frac{2}{d_K}\sum_{w}m_{iw}\log Nw,\qquad
 h_{\rm ad}(B_i)=f_i+\frac1{d_K}\sum_{\sigma:K\hookrightarrow\mathbb C}
                   \log\|B_{i,\sigma}\|_{\rm op}^2 .
$$
The norms are the prescribed source and target norms. The expression uses the content of the **shifted** map. In the earlier notation it is exactly $m_{iw}=v_w(C_{i,t_w})-k_{i,w}$, where $t_w$ is the tuple chosen at $w$ and $k_{i,w}$ is the integer lattice shift. Thus all quantities can be read in the original period matrices and metrics. [Local content ideal and the shift](continuation_v89/integral.tex#L84-L113) · [Original height comparison](global_assembly/main.tex#L486-L502)

For $a\in K^\times$, the finite part changes by $-2\log|N_{K/\mathbb Q}(a)|/d_K$ under $B_i\mapsto aB_i$. The archimedean part changes by its negative. Hence $h_{\rm ad}$ depends only on the projective class of this nonzero map. In a calculation one can divide the whole matrix by any nonzero rational pivot entry. The original lattices and norms still determine every local operator norm of the resulting matrix. This cancellation uses compatible evaluations across all embeddings of the field.

## What bound suffices for the mean slope?

Use the hypotheses and notation of the earlier mean-slope estimate. In particular the target has rank $n>0$ and all its slopes are at least $s-H$. The original source lattices have total rank $R>0$. Their slopes minus the assigned word heights $h_i$ have rank-weighted mean at least $s$ and are all at most $s+u$. Take $H,u\ge0$. At one complex embedding suppose that all source subspaces $E_i$ satisfy
$$
 \operatorname{codim}\sum_i B_i(E_i)\le a_0+\beta\sum_i\operatorname{codim} E_i ,
 \qquad a_0,\beta\ge0 .
$$
For $B_i\ne0$, define $e_i=(h_{\rm ad}(B_i)-h_i)_+$, and give zero maps $e_i=0$. Write $r_i=\operatorname{rank}N_i$ and $\Delta_{\rm ad}=R^{-1}\sum_i r_i e_i$. Then the mean target slope obeys
$$
 s-\mu(C)\le \frac{a_0H}{n}
       +\frac{\beta R}{n}\frac{H(u+\Delta_{\rm ad})}{H+u}.
$$
For $H=u=0$ the target floor gives the assertion directly. [Filtration inequality and its integration](PERIOD_LATTICE_LOSS.md#the-mean-slope-bound-with-losses)

**Proof.** Apply $B_i$ to $J_i^{-1}N_i$, with the ambient metrics, so its image is integral in $C$. Tensoring with an invertible fractional ideal preserves the rational subspaces of the Harder–Narasimhan filtration and translates every squared slope by the degree of the ideal line. Here that shift is $-f_i$. Indeed the saturated lattices on corresponding rank-$t$ subspaces differ in determinant by $J_i^{-t}$, so their normalized degrees differ by $-tf_i$. This proves the asserted slope translation for every step, including when $J_i$ is nonprincipal. Give the integral map height allowance $h_i+e_i-f_i$. This bounds its squared archimedean height by the definition of $e_i$. Its new adjusted slopes are therefore precisely the old adjusted slopes minus $e_i$. At a zero map keep the original source lattice and allowance.

All the complex images of source subspaces are preserved. The adjusted mean is now at least $s-\Delta_{\rm ad}$ and the same upper bound $s+u$ holds. For $0\le v\le H$ the integral map takes the source filtration step of adjusted slope at least $s-v$ into the target step of slope at least $s-v$. Apply the codimension bound to these steps and integrate in $v$. A source slope $\lambda\le s+u$ contributes at most $H(s+u-\lambda)/(H+u)$ to the integral of the missing source dimension. The mean bound gives the stated formula. [Native determinant and finite-index convention](global_slope/main.tex#L39-L52) · [Original slope filtration argument](gram_frame/gram_frame_section.tex#L84-L113)

For example take $K=\mathbb Q(i)$, both lattices $O_K$ with their standard metrics, allowance $h_i=0$, and $B_i(z)=p^{-m}z$ for a rational prime $p$ and $m>0$. The largest integral domain in the given source is $p^m O_K$, whose index contribution in squared degrees is $2m\log p$. The archimedean contribution to the *signed* height is $-2m\log p$, while the finite part is $2m\log p$. Thus $\Delta_{\rm ad}=0$ for all $m$. Conversely a denominator confined to a single direction of a high-rank space may cost less under the [elementary-divisor estimate](PERIOD_LATTICE_LOSS.md#the-two-losses-and-their-exact-normalization). The proof permits either construction separately for each word: use the lattice and allowance giving the lower wordwise loss, since each preserves the upper bound on adjusted slopes, the same complex images, and the corresponding lower bound on total adjusted degree.

On the scales used in the reconstruction one may insert $\Delta_{\rm ad}$ in the earlier estimate $s\le\mu(C)+5u+7b+5\Delta_{\rm ad}$. A sufficient arithmetic target at the chosen cutoff is consequently to bound the rank-weighted excess of the projective heights by $b=\exp(x^\varepsilon)$ on the selected family. For the original all-$H$ frame conclusion, the stricter sufficient bound is $\Delta_{\rm ad}\le (1-\delta)\log(\#\mathrm{Word})/4$, under the same frame hypotheses. Both conclusions still require the spanning estimate. The full period-height obligation separately asks for exact integrality, its specified archimedean allowance, and the other period assertions. A comparison on projective heights answers the height question used by the mean-slope deduction. It leaves those stronger assertions and the uniform arithmetic bound to be proved. [Constants and all-$H$ threshold](PERIOD_LATTICE_LOSS.md#the-mean-slope-bound-with-losses)
