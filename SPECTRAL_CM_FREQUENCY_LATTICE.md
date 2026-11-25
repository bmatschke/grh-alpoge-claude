# The exact frequency lattice for a flag block and the terminal sampling estimate

The trace condition in the actual flag lattice singles out one conjugation eigenspace. Its dual allows an extra denominator at the two marked primes in that eigenspace. Transverse differences satisfy an integral condition. Counting the transverse values first and the points above each value second gives a sharper version of Roadmap B8.10aa. For the last singleton this gives an absolutely summable Fourier bound with two real-direction derivatives on the real frequencies and three directional derivatives elsewhere. The estimates below have explicit dependence on the field degree and on $g=g_0g_1$. [Two flag lattices][lattices] · [Original fifth-power estimate][count] · [Selected singleton and physical Haar normalization](SPECTRAL_TERMINAL_SINGLETON.md)

## Trace dual of the congruence

Let $E/F$ be the given CM extension, $c$ complex conjugation and $f=[F:\mathbb Q]$. For a block of length $s$ let $\epsilon=(-1)^s$, $C=\mathfrak d_E^\nu$, and $D=C^\vee=\mathfrak d_E^{-\nu-1}$, where the dual is for the trace pairing $\operatorname{Tr}_{E/\mathbb Q}(xy)$. Both ideals are stable under $c$. The integer $g$ is odd. Write
$$
 L=\{t\in gC:(1-\epsilon c)t\in g^2 C\},\qquad
 L^*=\{y:\operatorname{Tr}(yt/g)\in\mathbb Z\ (t\in L)\}.
$$
Then
$$
 L^*=D+g^{-1}(1-\epsilon c)D
     =\{y\in g^{-1}D:(1+\epsilon c)y\in D\}.                 \tag{1}
$$
For the first identity reduce $C$ and $D$ modulo $g$. Their finite modules are in perfect duality under $\operatorname{Tr}(xy)/g\pmod{\mathbb Z}$. The image of $L/g$ in $C/gC$ is the kernel of $1-\epsilon c$. The annihilator of that kernel is the image of the adjoint endomorphism on $D/gD$. Indeed the image annihilates the kernel and has its annihilator's size by finite duality. The adjoint is $1-\epsilon c$ because trace commutes with $c$. Lifting the image gives the first equality. For the second, the opposite factors have zero product and, modulo the odd integer $g$, multiplication by $2$ is invertible. Thus the kernel of $1+\epsilon c$ modulo $g$ equals the image of $1-\epsilon c$. This proof also works for negative $\nu$.

Let $Y=\ker(1+\epsilon c)$ in $E$. This is $F$ for odd $s$ and the trace-zero line over $F$ for even $s$. The frequencies in $Y$ form exactly $g^{-1}(D\cap Y)$. For each other frequency the transverse value $u=(1+\epsilon c)y$ is a nonzero element of $D$ in the opposite line. In each complex embedding $|v(u)|\le2|v(y)|$. Put $d_D=\sqrt{N(D)}$. Each nonzero element of $D$ has product of embedding magnitudes at least $d_D$, by the norm of its integral quotient ideal. Consequently each transverse frequency has product of magnitudes at least $2^{-f}d_D$, and the difference between two frequencies with the same transverse value has product at least $g^{-f}d_D$ when they are distinct. The last statement concerns the actual differences within one fibre.

## Counting the two kinds of frequency

For positive $R_v$ put $V=\prod_v R_v$ and use the box $|v(y)|\le R_v$. A set on a real or imaginary line in each coordinate whose nonzero differences have product at least $b_*>0$ has at most $5^f\max(1,V/b_*)$ points in this box. To prove it, let $t=\max(1,(V/b_*)^{1/f})$ and partition each interval of length $2R_v$ into at most $\lceil4t\rceil$ intervals of length at most $R_v/(2t)$. Each product cell contains at most one point. The same bound applies to translates, by partitioning intervals of the same lengths.

There are at most $5^f g^f V/d_D$ nonzero frequencies on $Y$ in a nonempty box containing such a frequency. For the transverse frequencies, apply the interval bound first to $u$ with radii $2R_v$ and separation $d_D$, and then to the points of one fibre with radii $R_v$ and separation $g^{-f}d_D$. The existence of a nonzero transverse value implies $V/d_D\ge2^{-f}$. Since $g\ge3$, the two maxima are attained by the volume ratios. This gives
$$
 \#\{y\in L^*\setminus Y:|v(y)|\le R_v\}\le 50^f g^f(V/d_D)^2.    \tag{2}
$$
In particular only one factor $g^f$ enters this count. Applying a complex-box estimate directly to $g^{-1}D$ gives $g^{2f}$ in its volume term.

Here is the resulting summation rule. For directional scales $z_v>0$, let $T=(\prod_v z_v/d_D)^{1/f}$. For any $h>a\ge1$ on $Y$, and any $h'>a'\ge2$ off $Y$, there are constants depending only on the displayed exponents with
$$
 \begin{aligned}
 \sum_{0\ne y\in L^*\cap Y}\prod_v\min(1,(z_v/|v(y)|)^h)
     &\le [C_{h,a}(gT)^a]^f,\\
 \sum_{y\in L^*\setminus Y}\prod_v\min(1,(z_v/|v(y)|)^{h'})
     &\le [C_{h',a'}gT^{a'}]^f .                               \tag{3}
 \end{aligned}
$$
The scales in the two lines can be chosen independently. Use dyadic indices $n_v=\max(0,\lceil\log_2(|v(y)|/z_v)\rceil)$ with $H=\sum_v n_v$ and $R_v=2^{n_v}z_v$. The weights are bounded by $2^{hf-hH}$ in the first sum. A nonzero axial frequency gives $g^fV/d_D\ge1$, so the linear volume ratio can be raised to $a$. In the second sum (2) holds and $(V/d_D)^2\le2^{(a'-2)f}(V/d_D)^{a'}$. Sum each majorant over the nonnegative multi-indices using $\sum 2^{-(h-a)H}=(1-2^{-(h-a)})^{-f}$ and its primed version. This proves (3), including equality at the lower endpoint exponents $a=1$ and $a'=2$.

## Application to the final singleton

Here $\nu=0$, $Y=F$ and $D=\mathfrak d_E^{-1}$. Use the cross densities and Fourier pairing with squared mass $I$ in the [physical singleton calculation](SPECTRAL_TERMINAL_SINGLETON.md). At each $v$ let $b_{v,2}$ be the supremum of the $L^1$ norm of the second real-coordinate derivative of the cross density of two unit vectors in the chosen coefficient span. Let $b_{v,3}$ be the analogous supremum for the third derivative over unit directions in the plane. Define
$$
 z_{v,j}=g b_{v,j}^{1/j}/(4\pi),\qquad
 T_j=\big(\prod_v z_{v,j}/d_D\big)^{1/f},\quad j=2,3 .
$$
The normalization comes from $\exp(2\pi i\,2\Re(v(y)\zeta)/g)$. At real frequencies its direction is real at every place. At the other frequencies the direction may vary. Integration by parts and the elementary unitary bound give the product of the minima in (3) after compression to the local spans. The bound holds for sums of tensors with all cross terms, by taking the norm of the tensor product of the compressed phase multipliers. The compact smooth test and its wall vanishing from the cited calculation justify these derivatives after extension by zero. Zero derivative budgets follow by continuity from positive upper bounds.

It follows for every translate and for absolute constants $C_2,C_3$ that
$$
 \left|\mathrm{covol}(L)\!\sum_{t\in t_0+L}\!D_{\rm phys}(t)-I\right|
 \le I\left([C_2(gT_2)^{3/2}]^f+[C_3 gT_3^{5/2}]^f\right).       \tag{4}
$$
Indeed (3) ensures absolute convergence, and the continuous periodization has the resulting Fourier series. Taking $h=h'=5$ instead allows $a=a'=4$ with the corresponding directional budgets. The factor $g$ inside $z_{v,j}$ is the actual character normalization and is already included in $T_j$. In (4) the term from $F$ still sees the full denominator $g$. To obtain the required $b^{-7}$ relative error it suffices that the sum of the two rates in parentheses be at most $b^{-7}$ on the selected test family. This arithmetic result leaves a quantitative analytic requirement on the residual coefficients and the cutoffs. The other terminal blocks and the global nonzero-Gram operator estimates retain their own hypotheses.

[lattices]: https://github.com/rh-lean-roadmap/rh-lean-roadmap/blob/02a95b4c62db610642af5f278ee5d0d6df87b348/docs/src/book/main.tex#L17992-L18006
[count]: https://github.com/rh-lean-roadmap/rh-lean-roadmap/blob/02a95b4c62db610642af5f278ee5d0d6df87b348/docs/src/book/main.tex#L46108-L46115
