# A direct level criterion for a nonzero ramified Bessel period

Fix one word of the tied Poincaré model. Write $G$ for its unitary group, $S=N\rtimes H$ for the rational Bessel subgroup, $a_i=h_i x_u$ for its finitely many fine column representatives, and $K=K_2$ for the prescribed finite level. Use the actual left $S(F)$-invariant scalar seed $\phi=\Phi_u(T)$ and its prescribed archimedean wave function. The analytic hypotheses are the absolute convergence, unfolding, cell measures, and identity normalization of the tied model. These results give two geometric nonvanishing tests; the second test gives unconditional strict positivity on sufficiently refined auxiliary levels of each fixed tied model.

## An injective core at the prescribed level

Take one nonzero basis vector supported on one marked column and set
$$
 T=\prod_{v\mid T_u}(1-R(a_v))\,T_0 ,
$$
where now $a_v$ is a nonidentity diamond in the $v$th marking factor. There is such a diamond since $T_u>2$. The regular action on the word-prime markings makes the $2^f$ terms distinct. Each factor is killed by the norm in that marking coordinate, hence $T\ne0$ lies in the original ramified subspace. One can equally use any other nonzero ramified column vector. The identity-cell isometry guarantees that its single seed has positive squared mass, and the absolute unfolding hypotheses give it finite first mass. [Free diamond orbit and single-orbit difference](PERIOD_FULL_REFERENCE_PAIRING.md) · [Scalar seed, convergence and measures][seed]

For each column in the support choose a bounded measurable set $C_i$ in an archimedean fundamental domain of $N_i=N(F)\cap\operatorname{Aut}(\Lambda_i)$. Assume their cells give more than half the first mass of $\phi$, using the original Haar measures. Such sets exist without any uniform size claim by finite mass and exhaustion. The condition can be tested on the archimedean integrals of $|\langle J T(i),W(x)\rangle|$ over $C_i$ and the whole domain, by PGR10. The finite-level multiplier is the same on both sides.

Use the ordered rational frame $b_1,\ldots,b_{r+1}=e_1,\ldots,e_r,z_u$. For each $j$ choose an $E$-basis of linear forms $\lambda$ annihilating the span of $b_1,\ldots,b_{j-1}$. For each pair of support columns $(i,i')$ choose positive rational integers $A,B$ with $A b_j\in\Lambda_i\cap\Lambda_{i'}$ and $B\lambda(\Lambda_i)\subset\mathcal O_E$. They may be chosen separately for each $j,\lambda,i,i'$ and exist by the full lattice property. In the following product take all embeddings $\tau:E\hookrightarrow\mathbb C$ with the usual pair of conjugates at each complex place. Use any Euclidean metrics in the ambient vector spaces and their duals. Write
$$
 M_\tau(i,i')=\sup_{x\in C_i,\,x'\in C_{i'}}
                     \|x_\tau (x'_\tau)^{-1}\|_{\rm op}.
$$
An explicit sufficient condition for nonvanishing of the **prescribed-level** ramified period is that for every such pair and each frame test one has
$$
 \prod_\tau A B\|\lambda_\tau\|\,\|b_{j,\tau}\|
                        (1+M_\tau(i,i')) < (g_0g_1)^{[E:\mathbb Q]} .       \tag{1}
$$
One may replace every factor by the supremum of the corresponding actual expression $|AB\lambda_\tau((x_\tau(x'_\tau)^{-1}-1)b_{j,\tau})|$. This is a linear return-coordinate test, even for long flags.

Indeed a collision between the two chosen cells in $G(F)\backslash G(\mathbb A)$ gives, after removing their left $S(F)$-translates, a rational return $\gamma$ with $a_i^{-1}\gamma_f a_{i'}\in K$ and $\gamma_\infty=x(x')^{-1}$. In particular $\gamma\Lambda_{i'}=\Lambda_i$. Hence $y=AB\lambda((\gamma-1)b_j)\in\mathcal O_E$. At every prime above $g=g_0g_1$ the marked frame congruence (PGR.35) gives $(\gamma-1)b_j\in \sum_{t<j}\mathcal O_{E,v} b_t+g\Lambda_{i,v}$. Applying $AB\lambda$ gives $y\in g\mathcal O_{E,v}$. These are local congruences on the original lattice. Integrality elsewhere now gives global divisibility of this scalar by $g$. If nonzero it would have absolute norm at least $g^{[E:\mathbb Q]}$. Condition (1) excludes this. The vanishing of all tests puts $\gamma b_j-b_j$ in the earlier prefix for every $j$. In the flag parabolic each isotropic line quotient is therefore fixed and its middle unitary factor fixes the class of $z_u$. Its action on the complement of that class is precisely $H$ and its unipotent radical is $N$. Thus $\gamma\in S(F)$. The two points are identified already on the left $S(F)$-quotient. Equivalently the return dictionary allows only $i=i'$ and the single identity coset on the diagonal. [Frame congruence and exact rational return][ret]

Let $C$ be the resulting subset of $S(F)\backslash G(\mathbb A)$. It meets each fibre over $G(F)\backslash G(\mathbb A)$ at most once, with the prescribed null-set conventions. On its image in the latter quotient, isolate the term belonging to $C$ in the scalar periodic sum. Integrating the triangle inequality there and unfolding the other absolute summands gives
$$
  \|P_uT\|_{L^1}\ge\int_C|\phi|-\int_{(S(F)\backslash G(\mathbb A))\setminus C}|\phi|>0 .
$$
No sign or estimate on any individual Gram cell is needed. This is the relative, marked application of the classical integral nonvanishing argument. The uniform issue in (1) is the size of the archimedean **first-mass** cores and their arithmetic coordinates on the family. The existing second-moment length concentration alone does not give that comparison. [Muić, Fourier coefficients of automorphic forms and integrable discrete series](https://arxiv.org/abs/1505.02263)

## A single auxiliary prime gives injectivity on a fixed word

There is also a precise range in which all strict period tests hold. Fix the entire old datum, including the two marked primes and its archimedean function. Away from a finite set of finite places $v$ of $F$ choose a common smooth integral model, hyperspecial $K_v$, and its principal congruence subgroup $K_v(1)$. Define
$$
 J_v=(K_v\cap x_{u,v}^{-1}S(F_v)x_{u,v})K_v(1),\qquad
 h_v=[K_v:J_v].
$$
It is an open compact subgroup since $K_v(1)$ is normal. Replace every seed by
$\phi_v=\phi\,\mathbf1_{S(F_v)x_{u,v}K_v(1)}$ at that one finite coordinate, and denote its scalar Poincaré sum by $P_v T$. The cutoff is invariant under left $S(F)$, independent of the finite class, and disjoint in its local variable from every word-prime diamond. On the old support cell $a_iK$ it retains exactly the right coset of the subgroup using $J_v$ at $v$. This follows from $a_i=h_i x_u$ with $h_i\in H(\mathbb A_f)$. The old rational stabilizers $N_i$ are retained because their local intersection belongs to $x_{u,v}^{-1}S(F_v)x_{u,v}\cap K_v$. There are no new rational stabilizers, and the absolute values are dominated by the original absolute periods.

In the old column metric let $\alpha_u I$ denote its actual positive identity-cell Gram contribution. Then as $v$ tends to infinity outside the fixed excluded set, at congruence depth **one**,
$$
       \|h_v P_v^*P_v-\alpha_u I\|_{\rm op}\longrightarrow0 .                 \tag{2}
$$
The Gram in (2) is taken in the actual scalar automorphic $L^2$ quotient, with its old Haar measure. In particular the auxiliary map is injective on the entire original finite-dimensional column and on its ramified part at every sufficiently large such prime. For any finite set of fixed words, one auxiliary prime works for all, and all the resulting periods have right principal level $K_v(1)$ there.

To prove (2) unfold the paired restricted seeds, grouping terms in the same old columns as in PGR13 and PGR15. The group of right finite integration on each retained coset has volume $v_K/h_v$. The unipotent domains stay unchanged. Each old rational return for the ordered column pair $(i,i')$ contributes its old scalar archimedean integral and old unit phase times $1/h_v$ if $a_i^{-1}\gamma_f a_{i'}\in J_v$ at $v$, and zero otherwise. The same assertion follows by partitioning the old support cells into cosets and doing the scalar unfolding, before summing rational returns. The old absolute version (PGR.31) bounds the sum of the absolute integrals with both old coordinate arguments. After cancelling $1/h_v$ this majorant is independent of $v$.

For any fixed $\gamma\in G(F)\setminus S(F)$ select a regular defining function of the closed subgroup $S$ in $G$ nonzero at $\gamma$. Spread the groups, the inclusion and the equation over a localization of $\mathcal O_F$. For all but finitely many $v$, $x_{u,v},h_{i,v},h_{i',v}\in K_v$, $h_{i,v},h_{i',v}\in S(\mathcal O_v)$, and their reductions preserve the subgroup. The finite return condition above would imply that the reduction of $\gamma$ belongs to $S(k_v)$, since after conjugation by $x_{u,v}$ the reduction of $J_v$ lies in that subgroup. The nonzero algebraic value of the chosen equation is a unit at all but finitely many places and rules this out. The return condition is well defined on the old right cosets by preservation of the $N_i$. Among the returns in $S(F)$ the old dictionary permits only one identity coset on a diagonal pair; it is always retained. Dominated convergence therefore gives the identity contribution for every pair of fixed column vectors. Taking a finite orthonormal basis gives operator-norm convergence, proving (2).

The same proof at a single good place with $K_v(n)$ and $n\to\infty$ uses closedness of the local subgroup. The varying-prime, depth-one form also gives a finite exclusion test for a chosen accuracy: truncate each entry's absolutely convergent return sum to meet the desired tail budget, then discard the primes dividing a nonzero defining-function value for any of the finitely many retained nonidentity returns, together with their denominators and the original bad primes. This cutoff depends on the fixed data.

The exact distinction from the original level can be seen by projecting back. At each auxiliary good prime $\chi_v=1$. With $E_{K_v}$ the probability Haar average over the original $K_v$, averaging the cutoff on each old support coset gives $E_{K_v}\phi_v=\phi/h_v$. The finite coset sum commutes with the absolutely convergent periodization, so
$$
                     h_v E_{K_v}P_vT=P_uT .                               \tag{3}
$$
Equation (2) proves strict positivity for the finer period. Its projection (3) to the prescribed level is the additional nonvanishing needed on the original family. The cutoff in (1) is one way to prove that nonvanishing at the original level directly. It is open uniformly on the prescribed data. The auxiliary-level proof requires no new seesaw or theta-descent identifications and makes no claim that changing this level is admissible for those independent arithmetic steps.

[seed]: ../../../research/modules/spectral/period_gram_v57/main.tex#L58-L119
[ret]: ../../../research/modules/spectral/period_gram_v57/main.tex#L928-L1079

## Constructing first-mass cores and removing the unipotent diameter

Here are quantitative versions of the two parts of (1). They are useful when the level is prescribed. Write $\mathcal N(g)=\max(1,\|g\|,\|g^{-1}\|)$ in the project Cayley coordinates at a real place. Realize the local wave function with the [normalized Bessel integral](../spectral/SPECTRAL_BESSEL_REALIZATION.md) on its fixed test vector. On this model the [smooth matrix-coefficient estimate](../spectral/SPECTRAL_SMOOTH_DECAY.md), the bounded norm of the unitary stabilizer character, and the scalar identifying the Bessel functional give
$$
 \|W_\tau(x)\|\le C_\tau \int_{S_\tau}\mathcal N(sx)^{-\eta_\tau}ds,
 \qquad \eta_\tau>2b_\tau,\quad b_\tau=10(2r+k+1)^2 .
$$
Indeed the rank's opposite-sign gap permits the exponent in the existing coefficient estimate to be taken strictly larger than $2b_\tau$. One fixed nonzero matrix-coefficient realization of the local Bessel functional and its scalar are absorbed in $C_\tau$; the local functional is unique up to scalar. The local constants are fixed-datum constants here, not claimed uniform. Put $J_{S,\tau}=\int_{S_\tau}\mathcal N^{-b_\tau}$ and $J_{G,\tau}=\int_{G_\tau}\mathcal N^{-b_\tau}$, both finite by the original growth computation. Then
$$
 \sup_x\|W_\tau(x)\|\le C_\tau U_\tau,\qquad
 U_\tau=\frac{2^{2b_\tau}J_{S,\tau}}{1-2^{2b_\tau-\eta_\tau}} .
$$
In fact if $s_0x$ lies in the radius-$D$ ball, each other such $s$ satisfies $\mathcal N(ss_0^{-1})\le D^2$. The subgroup is unimodular, so the volume of the slice of that ball is bounded by $D^{2b_\tau}J_{S,\tau}$. Sum the dyadic shells. On the complement of the image of the radius-$R_\tau$ ball in $S_\tau\backslash G_\tau$, quotient integration also gives $\int\|W_\tau\|\le C_\tau J_{G,\tau}R_\tau^{-(\eta_\tau-b_\tau)}$. On the full quotient the same bound holds with $R_\tau=1$.

Take the inverse image of the product of these compact quotient balls in every supported $N_i\backslash G_\infty$. Each is compact, since $N_i\backslash S_\infty$ is compact. Put $L_i=\|JT(i)\|$ and $v_i=\operatorname{vol}(N_i\backslash S_\infty)$. The seed outside these cores has first mass at most
$$
 v_K\Big(\sum_i v_iL_i\Big)
  \prod_\tau(C_\tau J_{G,\tau})\,
  \sum_\tau R_\tau^{-(\eta_\tau-b_\tau)} .
$$
This follows from the union bound and the product majorant; no factoring of the possibly entangled coefficient vectors $JT(i)$ is required. The full first mass is at least
$$
 \frac{\alpha_u\|T\|^2}{(\max_iL_i)\prod_\tau C_\tau U_\tau}.
$$
Indeed the numerator is the exact single-seed squared mass and the denominator bounds its supremum. If the first display of masses is less than half the second, these quotient cores meet the required first-mass condition.

For these quotient cores, there is a variant of the arithmetic separation bound (1) which is independent of the diameter of a fundamental set of the real unipotent lattice. Suppose that the first $j-1$ exact flag conditions have already been established for a putative collision $\gamma$. Put $Y=\operatorname{span}(b_1,\ldots,b_{j-1})$ and $Q=V/Y$, with the bars denoting projection to $Q$. Both $\gamma$ and $S$ preserve $Y$ and $S$ fixes $\bar b_j$. In $Q$ choose the filtration induced by the full rational isotropic flag, its perpendicular and its dual flag in $V$. The real action of $S$ on every graded piece is compact: the unipotent radical acts trivially, its flag and dual line quotients have trivial Levi action, and the middle action fixes $z_u$ and acts unitarily on its positive definite complement. Choose invariant real graded metrics, and quotient ambient Euclidean norms. For the quotient lattice $\bar\Lambda_i$ let $\mu_{ij}>0$ be a lower bound for the geometric mean, over embeddings of $E$, of the graded norm of every nonzero vector in any successive lattice quotient of its saturated filtration. It exists: in a rational basis of each graded piece clear the finitely many coordinate-lattice denominators and use one nonzero coordinate and its nonzero absolute field norm. The ability to choose $\mu_{ij}$ uniformly of adequate size would require its own arithmetic estimate. Let $c_{j,\tau}\ge1$ bound the operator norms of all natural projections from a filtration subspace of $Q_\tau$ to its graded quotient in the chosen metrics.

Take $A b_j\in\Lambda_i\cap\Lambda_{i'}$ as above. PGR.35 gives
$A(\gamma-1)\bar b_j\in g\bar\Lambda_i$: project the local congruence modulo $Y$, and use global integrality elsewhere. At a collision write $x=s k,\ x'=s'k'$ at infinity with $s,s'\in S_\infty$ and $\mathcal N(k_\tau),\mathcal N(k'_\tau)\le R_\tau$. Since $\gamma=s k(k')^{-1}(s')^{-1}$ preserves $Y$, so does $k(k')^{-1}$. On the quotient,
$$
 s^{-1}(\gamma-1)\bar b_j=(k(k')^{-1}-1)\bar b_j.
$$
The first nonzero graded component on the left has the same norm as the component before applying $s^{-1}$. The right side has quotient norm at most $(1+R_\tau^2)\|\bar b_{j,\tau}\|$. Consequently
$$
 \left(\prod_\tau A c_{j,\tau}(1+R_\tau^2)\|\bar b_{j,\tau}\|\right)^{1/[E:\mathbb Q]}
                      <g\mu_{ij}                                         \tag{4}
$$
forces $(\gamma-1)\bar b_j=0$. Iterate from $j=1$ through the negative vector, testing every supported pair. This proves original-level ramified nonvanishing if (4) holds and the explicit first-mass inequality above holds at the same radii. The remaining comparison concerns real matrix-coefficient constants and arithmetic lengths of the graded lattices on the prescribed family.
