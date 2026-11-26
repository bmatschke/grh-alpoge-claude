# Counting on the normalized image and averaging component degrees

## Why the two arithmetic volume comparisons have different hypotheses

A one-dimensional lattice already exhibits the positive part in the lower bound. Over $\operatorname{Spec}\mathbb Z$, fix a prime $p$ and integer $k\ge0$, take $p^k\mathbb Z$ as the integral line and give its rational coordinate the norm $e^{-a}|z|$. In degree $m$, the integral sections at threshold $e^{mt}$ number
$$
 1+2\left\lfloor e^{m(a+t-k\log p)}\right\rfloor .
$$
The logarithm of this number divided by $m$ tends to $(a+t-k\log p)_+$, also along $8\mid m$. Each unit of finite divisibility subtracts $\log p$ from the archimedean allowance. Strictly below that threshold only the zero section is counted. At equality there are three sections in every degree and their logarithmic growth rate is zero. On a flag component the dimension is $d$, the scale is $m^{d+1}/d!$, and a geometric degree multiplies the shifted component slope.

For the **source** we must count at an arbitrary real threshold. On each fixed smooth metric approximation the corrected line is nef on every geometric fibre and has semipositive curvature. A constant metric shift preserves both properties. Moriwaki's Corollary 6.4 bounds the section volume from below by the shifted self-intersection. Positivity of the count supplies the positive part afterwards. This application uses the tower's nefness and convergence theorems for the approximations of the original logarithmic metric. [Moriwaki, Corollary 6.4](https://arxiv.org/pdf/math/0612269#page=42) · [Marked models and the injections at the approximation degrees](../periods/PERIOD_VOLUME_BEFORE_SELECTION.md#the-volume-on-one-component)

For the **target** there is a shorter way to calculate the count on the precise model where the transferred sections are regular. Write $X$ for the arithmetic projective image, $\nu:Y\to X$ for its normalization, and $A_t$ for its weight-one line equipped with the original Petersson Fubini–Study metric times $e^{-t}$. For $t\ge c_s$, the integral coordinate sections of $\nu^* A_t$ generate its underlying line and have supremum norm at most one at every embedding. Thus the line has nonnegative degree on each vertical curve. On the normalization of a horizontal arithmetic curve, choose a generating section nonzero at the generic point. The finite contribution to its degree is the degree of an effective divisor. The infinite contribution is a sum of $-\log\|s\|\ge0$. At infinity the curvature is the pullback of the semipositive Fubini–Study form in the Petersson metric. These observations give arithmetic nefness on $Y$, including at $t=c_s$.

Apply the arithmetic Hilbert–Samuel formula to the *eighth power* of $\nu^*A_t$. In degree $n$ its small sections are exactly those counted on $Y$ at weight $8n$. Its arithmetic self-intersection scales by $8^{d+1}$, which cancels the same factor in the normalization of the count. By the projection formula the self-intersection of $\nu^* A_t$ equals that of $A_t$, since $\nu$ has generic degree one. Writing $I_X$ for the unnormalized self-intersection, the result is
$$
 \lim_{n\to\infty}
 \frac{d!\log \#\widehat H^0(Y,(\nu^*A_t)^{8n})}
 {[F:\mathbb Q]\,(8n)^{d+1}}
 =\frac{I_X(A_t)}{(d+1)[F:\mathbb Q]}
 =\delta_Z(h_Z+t).
$$
The last equality is the Fubini–Study Chow-height formula for the same finite lattice and the same metric, together with the constant-shift identity. The argument applies directly even if additional sections extend across the normalization in an individual degree. [Moriwaki, Corollary 5.5](https://arxiv.org/pdf/math/0612269#page=38) · [Roadmap B8.25l, arithmetic Hilbert–Samuel and the projection formula](https://github.com/rh-lean-roadmap/rh-lean-roadmap/blob/c7755c1086f05d0918ee8496d95912e4f35e22f9/docs/src/book/main.tex#L19655-L19667) · [Exact comparison of the Chow height with the shifted intersection](https://github.com/rh-lean-roadmap/rh-lean-roadmap/blob/c7755c1086f05d0918ee8496d95912e4f35e22f9/docs/src/book/main.tex#L49405-L49408) · [Jin’s component counts and threshold](https://github.com/yuiyuiui/Natural-Language-Proof-Generalized-Riemann-Hypothesis/blob/405237610e58ab9d4a9d5d54d9a0548a0c44227c/sections/j-arithmetic-covolume.tex#L3715-L3743)

## A direct passage from component heights to the slope

Here is a refinement of the arithmetic step of Roadmap B8.29. Suppose the shifted image degrees obey $0<(1-\rho)\delta_Z\le \delta'_Z\le\delta_Z$ and the $\delta'_Z$-weighted mean of $s_Z$ is at least $-X$. In the application every $\delta'_Z$ has the same value. Let $\lambda=\sum_Z\delta'_Z/\sum_Z\delta_Z$, and let $\bar h$ be the $\delta_Z$-weighted mean of $h_Z$. Sum the component volume inequality before normalizing. Since $(s_Z+c_s)_+\ge s_Z+c_s$, it gives
$$
 \bar h\ge -(1-\lambda)c_s-\lambda X-c_c .
$$
Here $X,c_s,c_c\ge0$ and $1-\rho\le\lambda\le1$.

The determinant comparison on the same components has coefficient $w_Z=\binom{T-1}{d}\delta_Z\le r_Z$, where $r_Z$ is the cusp lattice rank. Its unsquared degree $d_Z$ satisfies
$$
 d_Z/w_Z\ge T h_Z-3(d+1)|h_Z|-A\log(2+|h_Z|)-R.
$$
The constants $A>0,R\ge0$ are common to the components at this weight. Write $a=T-3d-4\ge0$ and $L_A=A\log\max(A,1)$. Put $v=\max(A,1)$ in $\log((2+u)/v)\le (2+u)/v-1$ to get $A\log(2+u)\le u+L_A+2$ for $u\ge0$. Since $h_Z\ge-c_s$, we also have $|h_Z|\le h_Z+2c_s$. Thus the $w_Z$-weighted determinant estimate, using exactly the same weights as $\bar h$, becomes
$$
 \frac{\sum_Z d_Z}{\sum_Z w_Z}\ge-K,\qquad
 K=a\big((1-\lambda)c_s+\lambda X+c_c\big)
       +(6d+8)c_s+L_A+R+2 .
$$
Every summand of $K$ is nonnegative. Consequently $\sum_Z d_Z\ge-K\sum_Z w_Z\ge-K\sum_Z r_Z$. The squared-norm slope on the cover is at least $2\sum d_Z/\sum r_Z\ge-2K$. The estimate needs only the upper rank comparison $w_Z\le r_Z$ at this division. In particular $K\le T(X+c_c)+(6d+8+T\rho)c_s+L_A+R+2$. This drops the terms $Tzc_s$ and one of the two $T\rho c_s$ allowances from the coarser bound, with $z$ the relative rank error in B8.25e. Subsequent changes of weight and character type retain their own rank estimates. [Roadmap, component degree and determinant hypotheses](https://github.com/rh-lean-roadmap/rh-lean-roadmap/blob/c7755c1086f05d0918ee8496d95912e4f35e22f9/docs/src/book/main.tex#L20250-L20272) · [Component volume inequality](https://github.com/rh-lean-roadmap/rh-lean-roadmap/blob/c7755c1086f05d0918ee8496d95912e4f35e22f9/docs/src/book/main.tex#L53970-L53984) · [Original determinant calculation](https://github.com/rh-lean-roadmap/rh-lean-roadmap/blob/c7755c1086f05d0918ee8496d95912e4f35e22f9/docs/src/book/main.tex#L53987-L54006)
