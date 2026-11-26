# Horizontal orders of the cusp base ideal in period entry 7

Fix a nonterminal deep cover, a component, and its complete quotient-weight cusp series as in [the carrying-section comparison](PERIOD_CARRYING_THETA_ORDERS.md). Write $I$ for its base ideal in the extending weight frame. On a horizontal prime divisor $D_0$ of the normalized blowup let $b_0=\operatorname{ord}_{D_0}I$. Under the period-chart and cusp-space identifications below, $b_0$ admits an upper bound independent of the numerator chosen for the height comparison.

Use the split base level $Q_0=g_0g_1$, the number $N$ of theta columns, and the thin-test constant $C_\chi=8100m^4(2fm)^4R_E^7$ of B8.25g, with $R_E=\operatorname{rd}(E)$ and $2f=[E:\mathbf Q]$. Write $X$ for the toric character lattice of the principal degeneration on a transverse complex disk. Use its integral symmetric monodromy form $B$, normalized by $B(x,x)=2Q(x)$ for the cubical quadratic order, and the ordinary integral dual $X^*=\operatorname{Hom}(X,\mathbf Z)$. At positive toric rank put $\mu^2=\min_{0\ne\eta\in X^*}B^{-1}(\eta,\eta)$. Then
$$
 b_0\ \le\ \frac{fNC_\chi}{R_E^2Q_0\mu^2}
       \ \le\ \frac{NC_\chi}{2Q_0}\,\phi_C(B).                       \tag{1}
$$
Here $\phi_C(B)$ is the infimum of $\ell(B)$ over the linear functionals integral on integral CM-balanced symmetric forms and strictly positive on every nonzero positive semidefinite such form. At toric rank zero the base order is zero. In the eventual size range, $N,m^4(2fm)^4,R_E^7\le b$ and $Q_0\ge b^{16}$, so the coefficient $NC_\chi/(2Q_0)$ is at most $4050b^{-13}$.

**Hypotheses on the chart.** Use an embedding admitting the analytic uniformization and the complete cusp space of B8.25g. At a general smooth complex point of $D_0$ choose a transverse disk whose punctured disk is in the interior. In a principal integral symplectic basis the assumed period chart is
$$
 Y=\Im\tau=\frac{L}{2\pi}\begin{pmatrix}B&0\\0&0\end{pmatrix}+O(1),
 \qquad L=\log(1/|t|).
$$
The vanishing real-period lattice in those coordinates is $X^*$. The residual block converges to a positive matrix, and the extending flag, theta and flat frames have point norms and inverse norms bounded by powers of $1+L$. These are the period and metric comparisons needed on the chosen cover. The normalization follows from $q_{ij}=t^{B_{ij}}$ times a unit and $\exp(2\pi i\tau_{ij})=q_{ij}$ for the toric pairing. Taking a general point preserves the generic orders of the monomial parameters and base ideal generators. Under ramified parameter change $b_0$ and $B$ scale by the same degree. [Brox's arc and monodromy comparison][brox] · [Framed horizontal tests](PERIOD_CARRYING_THETA_ORDERS.md)

**The dual minimum.** The squared Hermitian norm of a period $u+\tau v$ for $u,v\in\mathbf Z^g$ is $(u+\Re(\tau)v)^tY^{-1}(u+\Re(\tau)v)+v^tYv$. The block asymptotics give $Y\ge c\,1$ for large $L$. Thus $v\ne0$ gives length bounded away from zero. For $v=0$, if $u$ has a nonzero residual component $u_A$, minimization over the toric component gives $u^tY^{-1}u\ge u_A^tY_{AA}^{-1}u_A$, again bounded below. For $u=(\eta,0)$ the inverse Schur complement on the toric block is $(2\pi/L)(B^{-1}+O(L^{-1}))$, with relative error $O(L^{-1})$ in quadratic-form order. The estimate holds simultaneously for all integral vectors in this block. For positive toric rank the first minimum $\lambda$ therefore satisfies $L\lambda^2\to2\pi\mu^2$. The same proof omits the residual block for a totally toric degeneration. The thin condition $M\lambda^2<b$ eventually holds on the fixed disk. The analytic thin parameter $\phi=2f/(R_E^2\lambda^2)$ satisfies
$$
 \lim_{t\to0}\frac{\phi}{L}=\frac{f}{\pi R_E^2\mu^2}.                 \tag{2}
$$

**The cusp orders.** Retain the finitely many normalized theta derivatives at the base level in B8.25g. Before that proof rounds its exponential coefficient, the test section and the sum of squared evaluations give a lower bound for the sum, up to a positive constant fixed on this cover, of $\exp(-2\pi NC_\chi\phi/Q_0)$. Passage to the maximum loses at most the number of characteristics. Pullback and the central and flat weight changes on the component preserve point norms up to fixed positive factors. Thus at every sufficiently small $t$ one member of the resulting finite list has norm at least $c_1\exp(-\pi NC_\chi\phi/Q_0)$, for $c_1>0$ independent of $t$. These sections all belong to the complete complex cusp space of the target weight. Since the integral basis spans that space, all their framed readings vanish to order at least $b_0$. Their maximum norm is at most $c_2e^{-b_0L}(1+L)^{c_3}$ by the assumed metric bounds. Take logs, divide by $L$ and apply (2). This proves the first inequality in (1). At toric rank zero the first minimum is bounded below, so both the thin and thick Bergman estimates give a positive lower bound on the disk. A fixed basis and its positive Petersson Gram matrix bound the Bergman supremum by a constant times the maximum squared basis norm. These facts force the base order to be at most zero, hence zero in the regular frame. [B8.25g, the derivative sum and the transfer to the target weight][test]

**The CM comparison.** For completeness, let $\eta\in X^*$ be nonzero. Write $\eta=\operatorname{Tr}_{E/\mathbf Q}h$ for the unique $E$-linear covector $h:X_\mathbf Q\to E$. Trace duality applied to $a\mapsto\eta(ax)$ proves this and gives $h(X)\subset\mathfrak d_E^{-1}$, the codifferent. Every admissible $\ell$ on balanced forms extends integrally to the lattice of all bilinear matrices. Indeed the balanced symmetric integral matrices are the intersection of a rational linear subspace with that lattice and hence form a saturated subgroup. Write the extension as $\ell(C)=\sum_j C(x_j,x'_j)$. For each embedding $\sigma$ put $P_\sigma=\Re(\sigma h\otimes\overline{\sigma h})$ as a real bilinear form, and $P=\sum_\sigma P_\sigma$. Each $P_\sigma$ is balanced, positive semidefinite and nonzero. The element
$$
 z=\sum_j\left(h(x_j)\overline{h(x'_j)}
             +\overline{h(x_j)}h(x'_j)\right)\in\mathfrak d_E^{-2}
$$
is totally positive, since $\sigma(z)=2\ell(P_\sigma)>0$. Its field norm has absolute value at least $R_E^{-4f}$ by the fractional ideal inclusion. Taking the trace and applying the arithmetic-geometric mean inequality gives $\ell(P)\ge f/R_E^2$.

The real CM embedding blocks are $B$-orthogonal and their complex structures $J$ are isometries. If $\alpha$ is the restriction of $\eta$ on a conjugate pair, the pair contributes $(\alpha\otimes\alpha+(\alpha\circ J)\otimes(\alpha\circ J))/2$ to $P$. The two representing vectors are orthogonal of equal $B$-length. Bessel's inequality gives $P\le B^{-1}(\eta,\eta)B/2$. Applying $\ell$, choosing a shortest dual covector, and taking the infimum over $\ell$ proves the second inequality of (1). [Brox, DA1–DA5][brox]

**Application to the carrying divisor.** For the section $H$ of degree $8J$ constructed on this component from level $R=3$ or $5$, the [symmetrized-product estimate](PERIOD_SYMMETRIZED_CARRYING_SECTION.md) gives $\operatorname{ord}_{D_0}(H)/(8J)\ge c_R\phi_C(B)$ when the key and flat twists have unit order in the horizontal frames. Their constant positive point norms and the polylogarithmic metric comparisons give this unit order. With $q$ the smaller signature index and $n$ the Hermitian rank,
$$
 \frac{\operatorname{ord}_{D_0}(H)}{8J}-b_0
 \ \ge\
 \left[\frac{3}{R^4}\max\{1,(n/q)(1-R^{-2f})\}
                 -\frac{NC_\chi}{2Q_0}\right]\phi_C(B).
$$
The bracket is strictly positive eventually. This also gives a bound on the horizontal multiplicity of the complete target series itself. For the direct divisor-ideal comparison, vertical orders on the same model still enter its weighted cost. A separate [depth argument](PERIOD_REFERENCE_DEPTH_BUDGET.md) bounds the finite cost under its stated formal-chart and jet hypotheses. The [degree-weighted arithmetic intersection](PERIOD_WEIGHTED_ROOT_INTERSECTION.md) still needs an estimate on the actual components. [Normalized blowup and the remaining vertical cost](PERIOD_CARRYING_THETA_ORDERS.md)

[brox]: https://github.com/JoseBrox/GRH_distillation/blob/cde0bf419551e21a6fa70d52f4650fd758d75dd6/notes/geometry-divisor-arc-comparison.md
[test]: https://github.com/rh-lean-roadmap/rh-lean-roadmap/blob/dc5594a62bb2b94139788df817db693cd939a046/docs/src/book/main.tex#L51560-L51596
