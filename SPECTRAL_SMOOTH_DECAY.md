# Discrete-series decay on the smooth vectors used by the Bessel integral

The [shifted Bessel realization](SPECTRAL_BESSEL_REALIZATION.md) uses absolute convergence with an arbitrary smooth vector in the second slot. Miličić gives the decay rate on the Harish–Chandra module in terms of the gaps from the noncompact walls. Completing the matrix coefficients in a weighted supremum norm gives a smooth-vector seminorm for every exponent strictly below the available decay rate. In particular the large numerical margin on the actual shift ball supplies all the integrals in B8.02b, Claims 2–4. [Miličić, *Asymptotic behaviour of matrix coefficients of the discrete series*, pp. 59–60 and 84–85][mil] · [Bernstein–Krötz, *Smooth Fréchet globalizations of Harish-Chandra modules*][bk]

Let $G=U(p,q)$, $p=k+r$, $q=r+1$, $n=p+q$. In a unitary Cayley basis put $R(g)=\max(1,\|g\|_{\rm op},\|g^{-1}\|_{\rm op})$. Fix a shifted representation of parameter $\mu=\lambda+\nu$ with $\|\nu\|_1\le km^5$. Write $h$ for its least gap $|\mu_i-\mu_j|$ between coordinates of opposite signature. On the chosen grid $h\ge n^{19}/2$. Constants and differentiability orders below may depend on the vector and shift. The numerical exponent needed in the moment estimates is independent of those constants.

## Matching the noncompact roots

Remove the compact central character by restriction to $SU(p,q)$. Multiplying by a central unitary phase preserves coefficient magnitudes, and subtracting the mean from the parameter preserves root differences. The group $U(p,q)$ is the product of its special unitary subgroup and its compact center up to finite kernel. In the type $A_{n-1}$ root system use roots $e_i-e_j$ of squared length two. For any root $\alpha$, Miličić's constant is
$$
       k(\alpha)=\tfrac14\sum_{\beta} |(\alpha,\beta)|=n-1.
$$
The two roots $\pm\alpha$ contribute four in total. There are $4(n-2)$ other roots sharing exactly one index, each contributing one. Roots connecting opposite signature blocks are precisely the noncompact ones. Thus $\kappa=h/(n-1)$ satisfies the hypothesis of the theorem on every shift.

In the positive Cartan chamber write $t_1\ge\cdots\ge t_q\ge0$ for the logarithms of the hyperbolic singular values. Here $R=e^{t_1}$. The restricted half-sum is $\rho(t)=\sum_{i=1}^q(n+1-2i)t_i\ge(n-1)t_1$. This follows from the roots $e_i\pm e_j$ of multiplicity two, $e_i$ of multiplicity $2(p-q)$ and $2e_i$ of multiplicity one. Miličić's theorem bounds each $K$-bifinite coefficient by a constant times $\Xi(g)^{1+\kappa}(1+\|t\|)^d$ for a finite $d$. The standard chamber estimate for $\Xi$ is a polynomial times $e^{-\rho(t)}$. Hence for every exponent $M<h+n-1$,
$$
    |\langle v,\sigma(g)y\rangle|\le C_{v,y,M}R(g)^{-M}
          \qquad(v,y\text{ both }K\text{-finite}).                \tag{1}
$$
The constants in (1) are allowed to vary with both $K$-types. The smooth-vector argument below uses no bound on that variation. [Miličić's root criterion and chamber estimate][mil]

## Passing to a smooth vector without a uniform bound in the compact types

Fix a nonzero $K$-finite first vector $v$. For any $0<B<h+n-1$, let $C_{0,B}(G)$ be the Banach space of continuous functions for which $R^B F$ vanishes at infinity, with norm $\sup_g R(g)^B|F(g)|$. Right translation by $x$ has operator norm at most $R(x)^B$ by submultiplicativity. It is strongly continuous, first on compactly supported functions and then by density. For $K$-finite $y$, the coefficient $c_y(g)=\langle v,\sigma(g)y\rangle$ belongs to this space by using a strictly larger exponent in (1).

Let $H_B$ be the closed span in this norm of all right translates of these $c_y$. For any compact type $\delta$, Haar integration over $K$ gives a bounded projection $P_\delta$ on $H_B$. On every generator it satisfies
$$
      P_\delta R(x)c_y=c_{P_\delta\sigma(x)y},
$$
where the projection on the right acts in the original representation. The right side belongs to the finite-dimensional image of its $\delta$-isotypic space by admissibility. That image is closed in $H_B$, and every element of it already occurs by taking $x=1$. Thus the $K$-finite elements of $H_B$ are precisely the coefficient functions of the original Harish–Chandra module. The map from that module is injective by irreducibility, since the translates of $v$ span a dense subspace. The derived actions agree: a derivative of $c_y$ is $c_{d\sigma(X)y}$, which still has the bound (1). Along a one-parameter group the fundamental theorem of calculus expresses the difference quotient as an average of translates of this derivative. Strong continuity in the weighted norm justifies the limit and its iteration.

It follows that $H_B$ is an admissible Banach globalization of the original module, of moderate growth by the translation bound. The smooth-vector topology on $H_B^\infty$ has moderate growth as well, since the adjoint action moves a finite list of Lie derivatives with coefficients polynomially bounded by $R(x)$. Casselman–Wallach uniqueness gives a continuous isomorphism $\sigma^\infty\to H_B^\infty$ extending $y\mapsto c_y$. Evaluation at any $g$ is continuous in the weighted norm. Density of the $K$-finite vectors in the smooth topology therefore identifies the new function at $g$ with the actual coefficient for every smooth $y$. Taking its norm proves
$$
   |\langle v,\sigma(g)y\rangle|
       \le C_v p_v(y)\,R(g)^{-B}\qquad(y\in\sigma^\infty).        \tag{2}
$$
No uniformity in the constants of (1) across compact types is required. The stronger exponent from (1) was used only to put each initial coefficient in $C_{0,B}$. [Bernstein–Krötz on Banach globalizations, smooth vectors and uniqueness][bk]

Here $p_v$ can be taken as a finite sum of Hilbert norms of Lie derivatives by the usual smooth-vector topology of a unitary representation. For a translate of the first vector use $R(g_0^{-1}g)\ge R(g)/R(g_0)$. Finite linear combinations give (2) for the entire span of the translates of $K$-finite vectors used in the Bessel integral. Take $B=h/(8\sqrt{2q})-1$, which is positive and strictly less than $h+n-1$ throughout the actual shift ball. Equivalent matrix norms in a fixed Cayley frame change only the constant. This proves the needed smooth coefficient estimate at the native gap. Together with the [absolute integral, realization and adjoint](SPECTRAL_BESSEL_REALIZATION.md), [moment recursion](SPECTRAL_BESSEL_MOMENTS.md), [real section](SPECTRAL_ORBITAL_AMPLITUDE.md) and [marked genus mean](SPECTRAL_PAIRED_GENUS.md), it supplies the nonidentity singular-cell estimate on the tied row. [Source smooth-decay convention][native]

[mil]: https://www.math.utah.edu/~ptrapa/math-library/milicic/milicic-asymptotics-duke-1977.pdf
[bk]: https://arxiv.org/abs/0812.1684
[native]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Formalism/LocalToGlobal/SiegelLatticeTheory/BesselDiscreteSeries/DecInfPf.lean#L59-L125
