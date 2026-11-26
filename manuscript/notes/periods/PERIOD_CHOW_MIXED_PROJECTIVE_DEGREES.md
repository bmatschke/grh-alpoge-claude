# How many costly sections enter a Chow coefficient?

Period entry 7 needs a lower bound for the height of the projective image of a space of cusp forms. Suppose some integral cusp forms are short in the Petersson metric and the others are available with a larger bound. The common base locus of the short forms can force a nonzero Chow coefficient to involve the others. Its least possible exponent has an exact formula in terms of the graph of the linear projection defined by the short forms. This gives a test for a proposed subsystem on the actual component. [The height convention and the determinant inequality](PERIOD_POSITIVE_COMPONENT_CHOW_BOUNDS.md)

## The coefficient and the graph

Let $X\subset\mathbf P(V^*)$ be a geometrically integral projective variety of dimension $d$ and degree $\Delta$ over a field of characteristic zero. Work over the algebraic closure for the intersection calculation. Let $0\ne W\subset V$ give a rational projection on $X$ with nonempty domain. Choose a basis of $W$ extended to a basis of $V$. The Chow form $F$ in $d+1$ hyperplanes has degree $\Delta$ in each block. Let $k$ be the smallest total exponent of the complementary coordinates in any nonzero monomial of $F$. Let $\Gamma$ be the closure of the graph of the projection to $\mathbf P(W^*)$, with $A,M$ the hyperplane classes from $X$ and the projection target. Put $g_j=\int_\Gamma A^{d-j}M^j$. Then
$$
 e=(d+1)\Delta,\qquad k=e-\sum_{j=0}^d g_j,\qquad
 \frac{k}{e}=1-\frac1\Delta\int_0^1\int_\Gamma ((1-t)A+tM)^d\,dt.       \tag{1}
$$
In particular $g_0=\Delta$. At the opposite end $g_d$ is the moving degree of the short subsystem, counted with the generic degree of its map. It vanishes if its image has dimension less than $d$ (for $d>0$). The intermediate degrees can still contribute. Formula (1) also proves independence of the chosen complement.

**Proof.** Choose general $a_i\in W$, $b_i\in V$, for $0\le i\le d$, and consider the one-variable polynomial
$$
 P(t)=F(a_0+t b_0,\ldots,a_d+t b_d).
$$
Its degree is $e$, since general $b_i$ have no common point on $X$. Its order at zero is exactly $k$. In fact the coefficient of $t^k$ is the part of $F$ of complementary degree $k$, evaluated at the short coordinates of the $a_i$ and the complementary coordinates of the $b_i$. These coordinates vary independently, so this coefficient is generically nonzero.

The two tuples define morphisms from $\Gamma$ to $\mathbf P^d$ via $M$ and $A$. Indeed each of the two systems is basepoint-free there and $d+1$ general members have no common point. For a fixed graph point their two projective values are independent general points of $\mathbf P^d$, so coincidence imposes $d$ conditions. Thus a generic pair has finitely many coincidences and avoids the closed subset over the original base locus and the singular locus of $X$, whose inverse images together are proper in the integral graph. On the remaining open part, the tuples are sections of the same line at each point of $X$. Their projective values agree exactly when $a_i(x)+t b_i(x)=0$ for all $i$ at one $t\ne0$. Intersect the two maps with the diagonal of $\mathbf P^d\times\mathbf P^d$. Its class is $\sum_{j=0}^d H_1^j H_2^{d-j}$, so the intersection number is $\sum_j g_j$.

For the multiplicity in this count, allow the coefficients to vary. Over smooth $x$ and $t\ne0$ the $d+1$ vanishing equations are independent linear equations on the $b_i$. The resulting incidence variety is smooth. Generic smoothness in characteristic zero gives transverse isolated solutions for a general pencil on every component dominating its parameter space. Two distinct points at the same $t$ impose $2(d+1)$ independent conditions because $V$ separates them. Those points and $t$ vary in dimension $2d+1$, so a general pencil avoids simultaneous solutions at distinct points. At a transverse solution the spatial derivative has rank $d$. After a change of basis in the tuple, its first $d$ equations cut out $x$ transversely, and the remaining equation has a simple zero in $t$. Locally that last equation cuts out the reduced Chow incidence divisor. Thus each coincidence contributes one to the number of nonzero roots of $P$ with multiplicity. Subtracting from $e$ gives $k$. Integrating the binomial expansion gives the last identity because $\binom dj\int_0^1(1-t)^{d-j}t^j\,dt=1/(d+1)$. [Chow forms and the incidence divisor, Eisenbud and Schreyer](https://arxiv.org/abs/math/0111040)

## The resulting period-height test

Use this on a component $X_Z$ in the degree-one quotient-weight embedding of the [Petersson determinant argument](PERIOD_POSITIVE_COMPONENT_CHOW_BOUNDS.md). Its basis consists of integral sections, the first ones spanning $W_Z$ of norm at most $e^{\lambda_Z}$, and the remaining ones of norm at most $e^{J_Z}$ at every embedding, with $0\le\lambda_Z\le J_Z$. Let $\beta_Z=k/e$, $N_Z=\dim V_Z$, and $H_i=\sum_{j=1}^i 1/j$. Select a nonzero coefficient with the least exponent. The integral coefficient bound at finite places and the sphere-mean bound at infinity give, by the product formula,
$$
 h'_Z\ge-\lambda_Z-\beta_Z(J_Z-\lambda_Z)
               -\log N_Z-\tfrac12 H_{N_Z-1}.                       \tag{2}
$$
Here $h'_Z$ is the unsquared normalized Chow height used by that argument. The determinant and rank comparisons there already absorb $T_*(\log N_Z+H_{N_Z-1}/2)=O(\sqrt b)$. The arithmetic test for this route is therefore the single degree-weighted bound
$$
 T_*\frac{\sum_Z\Delta_Z\{\lambda_Z+\beta_Z(J_Z-\lambda_Z)\}}{\sum_Z\Delta_Z}
       = O(E_p).
$$
The $g_j$ belong to this particular family of short forms. For example, for $X=\mathbf P^1\times\mathbf P^1$ embedded by $\mathcal O(a,b)$ with $a,b\ge1$, take the complete system of $\mathcal O(a-1,b)$ multiplied by a fixed section of $\mathcal O(1,0)$. Cancelling its common factor gives $g_0=2ab$, $g_1=(2a-1)b$, $g_2=2(a-1)b$. Hence $k=3b$ and $\beta=1/(2a)$. Even when $a=1$ and the short map has one-dimensional image, only half the degree of a least-cost Chow monomial is charged to the complement.

## When the geometric degrees come from two flag weights

There is an explicit specialization when the actual short system has the moving map of the smaller weight. Suppose that on a common proper model the pullbacks of $A,M$ are the root lines for $u_1,u'=u_1-3n\eta_H$, respectively, after removal of a fixed divisor. It suffices that their mixed intersections identify with the canonical ones, with one common generic-degree factor. This holds, for example, if both maps come from basepoint-free systems with those line classes on that model and the model dominates the graph generically finitely. Here $n$ is the layer rank, denoted $r$ in the quotient-weight statement. By polarization, geometric proportionality on canonical extensions evaluates the mixed polynomial at every intermediate weight. The Weyl degree is proportional to the product of positive root differences. The Hodge shift decreases each cross-block gap by $3n$ and fixes the within-block gaps. For each cross-block pair at each real label let $\theta_i$ be $3n$ divided by the original gap. Suppose $0\le\theta_i<1$. Then
$$
 \frac1\Delta\int_\Gamma((1-t)A+tM)^d=\prod_i(1-t\theta_i),
 \qquad
 \beta=1-\int_0^1\prod_i(1-t\theta_i)\,dt.                       \tag{3}
$$
In particular put $\rho_0=1-g_d/\Delta$. If $0<\rho_0<1$, convexity of $\prod_i(1-t\theta_i)$ (its second derivative is a sum of nonnegative terms) and concavity of its logarithm give
$$
 \frac{\rho_0}{2}\ \le\ \beta\ \le\
 1-\frac{\rho_0}{-\log(1-\rho_0)}.
$$
The upper bound is $\rho_0/2+O(\rho_0^2)$, and when $\rho_0=0$ the cost fraction is zero. With only one varying gap both sides of (3) give the exact half-loss $\rho_0/2$. [Geometric proportionality on canonical extensions](PERIOD_WEIGHTED_ROOT_INTERSECTION.md) · [The two quotient weights and their Weyl degrees](https://github.com/rh-lean-roadmap/rh-lean-roadmap/blob/dc5594a62bb2b94139788df817db693cd939a046/docs/src/book/main.tex#L20210-L20254)

For application to the selected family one must exhibit short sections with the stated integral and Petersson bounds and identify the graph of their actual linear system. The Roadmap constructs its generic carrying section in weight $8(u_1-u')$. This compares sections in multiples of eight. Applying (2) directly requires a construction in degree one. A passage through a higher-degree embedding would also have to compare its lattice and norm with those induced from the original embedding. The existing record-section argument uses its own arithmetic comparison in these higher degrees. [The degree-eight carrier](https://github.com/rh-lean-roadmap/rh-lean-roadmap/blob/dc5594a62bb2b94139788df817db693cd939a046/docs/src/book/main.tex#L53689-L53707) · [The record-section route](PERIOD_RECORD_TRACE_TO_CHOW.md)
