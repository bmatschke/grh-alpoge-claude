# A uniform degeneration estimate for the period carrying section

Use a nonterminal deep cover and its component $Z$ as in [the carrying-section comparison](PERIOD_CARRYING_THETA_ORDERS.md). Put $n=k+m-1$, $d_E=[E:\mathbf Q]=2f$, and let $q>0$ be the smaller signature index. Fix $R=3$ or $5$. The full marking contains level $R^4$. A single section of a higher tensor power on $Z$ has a finite order estimate on **all** original traits, with the same archimedean cost per degree. The improvement uses the freedom in the generating residues of the level labels.

## Construction on the component

Let $A=\mathcal O_E/R\mathcal O_E$. The marked Hermitian lattice is projective of rank $n$ over $\mathcal O_E$, and its reduction is free of rank $n$ over the product of Artin local rings $A$. Let $\mathcal B$ be the finite set of its ordered $A$-bases and $J=|\mathcal B|$. For each $b\in\mathcal B$, choose one lift of its $n$ labels giving a theta product $f_b$ nonzero at a geometric generic point of $Z$. Such a choice exists **for each** specified $b$. The independent changes of lift evaluate each factor on a complete coset of abelian $R$-torsion. Some evaluation is nonzero there in characteristic zero by the theta-group argument for the principal line. Each lift still generates the higher marking by Nakayama. The labels are indices of rules on the given full cover. The geometric point selects indices from this list. It introduces no new field of definition for the selected rules. The rule allows every generating tuple, without any requirement that changes among these tuples preserve the Hermitian form. [Original numerator selection][selection] · [Two levels and their archimedean bounds](PERIOD_CARRYING_THETA_ORDERS.md)

Set $F=\prod_{b\in\mathcal B} f_b$. This gives one generically nonzero section fixed on the component, independent of the prime, valuation and frame. Its product with the original twists is $H=F^{24}(K_{\rm key}^{3n}S_Z)^J$, of weight $8J(u_1-u')$. If $G$ is the component Bergman supremum and $\beta=P_0+B'_0$, the preceding archimedean comparison for each $f_b$ gives

$$
 |H(y)|^2\le e^{8J\beta}G(y)^{8J}|K_{\rm key}^{3n}S_Z|^{2J}.
$$

## Finite order at any degenerating trait

Let $X$ be the period lattice, $Q$ its positive definite cubical quadratic order with valuation $v$ taking value one on a trait uniformizer, and $t=\dim_E(X\otimes\mathbf Q)>0$. Write $L$ for the smallest real number for which the lattice vectors satisfying $Q(x)\le L$ span $X\otimes\mathbf Q$ over $E$. Discreteness and positive definiteness give this threshold and a basis $z_1,\ldots,z_t$ of the rational $E$-space in $X$ with $Q(z_i)\le L$. In the definition of the phase use the functional $C\mapsto\sum_i C(wz_i,z_i)$, where $w\in\mathcal O_E$ has $w+\bar w=1$. It is integral on integral balanced forms and equals $\frac12\sum_i C(z_i,z_i)$. If this vanishes on a positive semidefinite balanced form, its radical contains an $E$-basis, so the form is zero. Applying the functional to the polarization of $Q$ yields

$$
 \phi_{\rm fin}\le\sum_{i=1}^t Q(z_i)\le t L .
$$

Let $W=\operatorname{span}_E\{x\in X:Q(x)<L\}$. It has codimension $h\ge1$. The quotient $Y=X/(W\cap X)$ is torsion-free over $\mathcal O_E$, hence projective of rank $h$. The level period map onto $X/RX$, followed by the map to $Y/RY$, is surjective even at a wild prime. Indeed this is the geometric generic-fibre period map obtained by taking division points of a period in the semiabelian extension. Fix a column index in an ordered marking basis. As $b$ varies over $\mathcal B$, its column is uniform on vectors which generate a direct summand of rank one in $A^n$. The fraction of such vectors mapping to zero in $Y/RY$ is at most $R^{-d_E h}$.

For the count, the quotient is free of rank $h$ over the semilocal ring $A$. Its kernel is free of rank $n-h$, and the quotient map splits. Every vector extending to a basis occurs in the same number of bases by the transitive action of $\mathrm{GL}_n(A)$. A vector of $A^n$ extends to a basis precisely when its image at every residue field is nonzero. Writing $N\mathfrak p=|\mathcal O_E/\mathfrak p|$, the exact fraction is

$$
 R^{-d_E h}\prod_{\mathfrak p\mid R}
 \frac{1-(N\mathfrak p)^{-(n-h)}}{1-(N\mathfrak p)^{-n}}
 \ \le\ R^{-d_E h} .
$$

This computation includes ramification and the case $h=n$, where the numerator vanishes. For each column mapping nontrivially to $Y/RY$, every lattice representative of its period residue modulo $RX$ lies outside $W\cap X$ and has $Q\ge L$. The actual theta factor has order at least $L/R^4$ for *every* lift of that column. This uses the source's termwise bound $Q(R^2\chi+y)/R^4$, which holds in every residue characteristic. All the other factors have nonnegative order. Summing first over bases, then over their $n$ columns, gives

$$
 \frac{v(F)}{J}\ \ge\ \frac{n(1-R^{-d_E h})L}{R^4}
 \ \ge\ \frac{n(1-R^{-d_E})}{tR^4}\,\phi_{\rm fin}.
$$

Every individual basis also gives $v(f_b)\ge\phi_{\rm fin}/R^4$. Since the toric Lie algebra gives $t\le q$, the resulting coefficient works throughout the row. For a trait of relative ramification $e_0$ over the coefficient place $\lambda$, set $\operatorname{ord}=v/e_0$. With the source's finite twist allowance $e_\lambda$, the estimate is

$$
 \frac{\operatorname{ord}(H)}{8J}\ \ge\ c_R\frac{\phi_{\rm fin}}{e_0}-e_\lambda,
 \qquad c_R=\frac{3}{R^4}\max\left\{1,\frac{n}{q}(1-R^{-d_E})\right\} .
$$

It includes good reduction by setting the phase to zero. The level-three coefficient is at least $8n/(243q)$ since $d_E\ge2$. In particular this estimate gains a factor that grows with $n/q$ in the family. [Finite termwise order and positivity][orders] · [Toric rank bound][rank]

## Use in the height comparison

For any fixed $c<c_R$ with $c\ge0$, the same coefficient $c$ works in **every sufficiently large degree** $8a$. Write $a=jJ+r$ with $0\le r<J$, fix one basis $b_0$, and use the section $H^j(f_{b_0}^{24}K_{\rm key}^{3n}S_Z)^r$. Its normalized archimedean bound is unchanged. Its normalized finite phase coefficient is at least $(jJ/a)c_R$, with the same normalized twist allowance, and $jJ/a\to1$. The threshold is allowed to depend on the fixed component in the asymptotic section count. On degrees divisible by $8J$ the full coefficient $c_R$ holds exactly. All these multiplication maps are injective by generic nonvanishing. [Degree-by-degree use in B8.28][degree]

Consequently the reference-depth input to this part of B8.28 may be weakened to a bound for $d_\ell^c(u_1)$ at any one such $c$, where the depth subtracts $c\phi_{\rm fin}/v(\ell)$ from the infimum of normalized valuations of actual integral target cusp sections. The same cost and ramification conventions then give the finite Fubini–Study correction. This proves a uniform lower order for the actual higher-power numerator. An upper bound for the target depth with a family-weighted prime sum is still needed. Good reduction has phase zero and receives no saving from this estimate. The separate arithmetic intersection estimate of B8.26 also remains necessary in this route. [Reference-depth definition][depth] · [Finite correction in B8.28][correction]

[selection]: https://github.com/rh-lean-roadmap/rh-lean-roadmap/blob/02a95b4c62db610642af5f278ee5d0d6df87b348/docs/src/book/main.tex#L53679-L53686
[orders]: https://github.com/rh-lean-roadmap/rh-lean-roadmap/blob/02a95b4c62db610642af5f278ee5d0d6df87b348/docs/src/book/main.tex#L51600-L51646
[rank]: https://github.com/rh-lean-roadmap/rh-lean-roadmap/blob/02a95b4c62db610642af5f278ee5d0d6df87b348/docs/src/book/main.tex#L20545-L20555
[depth]: https://github.com/rh-lean-roadmap/rh-lean-roadmap/blob/02a95b4c62db610642af5f278ee5d0d6df87b348/docs/src/book/main.tex#L20622-L20630
[correction]: https://github.com/rh-lean-roadmap/rh-lean-roadmap/blob/02a95b4c62db610642af5f278ee5d0d6df87b348/docs/src/book/main.tex#L53689-L53705
[degree]: https://github.com/rh-lean-roadmap/rh-lean-roadmap/blob/02a95b4c62db610642af5f278ee5d0d6df87b348/docs/src/book/main.tex#L53747-L53757
