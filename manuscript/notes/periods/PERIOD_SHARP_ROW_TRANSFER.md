# A maximum-slope comparison for the two selected character levels

Write $R_0,R_1$ for the native glued base and sharp row lattices on the same selected linked bundle. Write $P_i\leq G$ for the level subgroups, $\psi_i$ for their finite characters, and $h_i=|P_i|$. Use the normalized Arakelov slope with squared archimedean norms and the prescribed row metrics. On every member with positive sharp rank the base rank is positive and

$$
 \mu_{\max}(R_1)+q_\kappa
 \leq \mu_{\max}(R_0)+q_\kappa+\log(h_0h_1).
 \tag{1}
$$

The common metric normalization $q_\kappa$ can have either sign. The cost is at most $2\log|G|$. This proves the change of level needed for frame entry 2. The [comparison of the entire slope filtration](PERIOD_CHARACTER_SLOPES.md) also proves the dual mean assertion of B4.55a, used for entry 7. [Original pair of row estimates][passage] · [Use in the frame][frame]

## The representation and the glued lattices

Use the dependent identification of the selected member with its weighted point and bundle. It supplies one realization, face, good quotient, reference tuple and set of row tests. Work in the principal-level rational good row $V$ of that realization, with the trivial subgroup and its trivial character. Its finite $G$-action will be denoted by $\rho$. The base character subgroup $P_0$ still acts on $V$. Put

$$
 e_i=h_i^{-1}\sum_{h\in P_i}\psi_i(h)^{-1}\rho(h).
$$

The rational level inclusion $J_i$ identifies $R_i\otimes K$ with $e_i V$. Indeed, the point has stable kernels by its primitive equivariance, weak realization and separated blocks, and its level maps identify both character spaces in the good quotient. Its principal-level bijection identifies the entire good quotient. The primitive row tests separate it and have values in the embedded coefficient field on all the original tuple frames. An invertible minor on a reference basis therefore recovers rational coordinates of the maps from each other tuple, also at principal level. The group action and $J_i$ descend with these coordinates. At the distinguished embedding their images are the corresponding character ranges, and taking ranks gives the same range equalities over $K$. The central good projector acts as identity on $V$. The character pin identifies the groups, characters and catalogue in this realization with those of the weighted point. [Point and dependent identification](../local/LOCAL_SELECTED_FAMILY.md) · [Primitive data on this realization](../../../archive/rounds/v74/continuation_v74/bundle.tex#L3-L93) · [Primitive group and test data][prim] · [The package at both levels][pack] · [Principal rational transitions][rat] · [Rational action and ranges][ranges] · [Good projector][good]

Let $R_g$ be the native glued principal lattice. At every finite place $w$ all three lattices use the prescribed serving tuple $\mu(w)$. One has

$$
 \rho(g)R_g=R_g,\qquad J_i R_i\subseteq R_g,\qquad h_i e_i R_g\subseteq J_i R_i .
 \tag{2}
$$

For the middle inclusion, a level vector represented integrally at the serving tuple is also a principal vector there. For the last inclusion fix $y\in R_g$. Locally, after multiplication by an element $c$ outside the prime $w$, it has an integral representative at that tuple. Sum the translates of this representative with coefficients $\psi_i(h)^{-1}$. Those coefficients are units and translation preserves the integral principal forms. The sum is of the required character type. Equivariance of the good quotient and tuple transition identifies its image with $ch_i e_i y$. The rational preimage under $J_i$ is unique. At each $w$ the representative just constructed verifies its local membership, so it lies in the glued $R_i$. Translation of a representative and its inverse gives the first assertion of (2). This starts from arbitrary $y$ in the principal lattice. [Integral inclusion and averaging in each tuple][avg] · [Gluing and translations][glue]

At each embedding $v$ the compatible quotient metrics satisfy

$$
 \|J_i z\|_{g,v}^2=h_i\|z\|_{i,v}^2,\qquad
 \|\rho(g)y\|_{g,v}=\|y\|_{g,v}.
 \tag{3}
$$

The positive metric is the sum over the reference Hecke labels of their Hermitian forms with the chosen positive weights at $v$, divided at level $i$ by $|P_i|$. The group preserves those labelled subspaces, and the good orthogonal quotient and level inclusion use the same forms on each piece. The same positive label coefficients occur at that embedding in the principal metric, where the subgroup order is one. This verifies (3) also at embeddings with different weights from the distinguished one. In particular $e_i$ is orthogonal there, since $\psi_i$ has finite order. [Metric compatibility for all embeddings][metric] · [Unitary group action and subgroup order][data]

## A family of integral maps detects the sharp row

For $g\in G$ let

$$
 A_g=J_0^{-1}\,h_0e_0\rho(g)J_1 .
$$

These are maps $R_1\longrightarrow R_0$ by (2). Their squared operator norms are at most $h_0h_1$ at every embedding by (3). To prove joint injectivity, the subspace $\bigcap_g\ker(e_0\rho(g))\subset V$ is $G$-stable. If nonzero, after complexification it contains an irreducible summand. Every such summand is good by the central projector. On every good irreducible the base average has rank one. For the regular squarefree finite general linear series at this point the space of the prescribed generic character has dimension one at each factor, and the factors tensor. Thus a whole irreducible cannot lie in $\ker e_0$. The intersection is zero and restricting to $J_1(R_1\otimes K)$ proves the assertion. The argument only needs the occurrence of the base character on each good irreducible. [Character trace on the actual weighted point](../../../archive/rounds/v73/continuation_v73/reading.tex#L3-L38)

In general suppose a finite list of integral maps $A_j:L\to M$ on Hermitian number-field lattices has zero joint rational kernel and squared norms at most $B$ at each embedding. In any positive-rank sublattice $U\subseteq L$, filter by successive intersections with the kernels in the list. Each intersection is saturated in its predecessor. The next map injects the quotient into $M$ over $K$, carries it integrally onto its image lattice and has norm at most $\sqrt B$ for its quotient norm. For rank $r$ the determinant norm is at most $B^{r/2}$. Consequently the normalized degree of this quotient is at most $r(\mu_{\max}(M)+\log B)$. This follows by taking the degree of the image with its induced metric and applying the determinant estimate with the squared-norm convention. Degree adds for the induced and quotient metrics in the filtration. Summing and taking the supremum over $U$ gives $\mu_{\max}(L)\le\mu_{\max}(M)+\log B$. No factor for the number of maps occurs.

Applying this lemma to $A_g$ gives (1), and joint injectivity supplies positive base rank when the sharp rank is positive. In the selected range $\log|G|=\lambda_0\le4b$. For example, a bound $\mu_{\max}(R_0)+q_\kappa\le x^a b$ gives $\mu_{\max}(R_1)+q_\kappa\le x^{1+\max(a,1)}b$ for $x\ge9$. The [divided-column estimate](PERIOD_DIVIDED_COLUMN_UPPER.md) supplies the other slope term. The outstanding contribution to the frame is the quantitative base-row bound. [Size bound][frame] · [Frame decomposition](PERIOD_FRAME_BOUND.md)

[passage]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Formalism/LocalToGlobal/GlobalTheory/DivPassage.lean#L68-L79
[prim]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Formalism/LocalToGlobal/IndefiniteReal/BaseLiftsPackageOfPrimitiveLinks.lean#L199-L224
[pack]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Formalism/LocalToGlobal/IndefiniteReal/PackageFromPrimitiveStatements.lean#L35-L64
[rat]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Formalism/LocalToGlobal/IndefiniteReal/RationalAdjoints/RatMuOfRowTest.lean#L25-L42
[ranges]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Formalism/LocalToGlobal/IndefiniteReal/RhoSpec.lean#L196-L252
[good]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Formalism/LocalToGlobal/IndefiniteReal/PGoodOfRho.lean#L38-L94
[avg]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Formalism/LocalToGlobal/IndefiniteReal/RowGSurj.lean#L117-L168
[glue]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Formalism/LocalToGlobal/IndefiniteReal/RowGSurj.lean#L170-L231
[metric]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Formalism/LocalToGlobal/IndefiniteReal/MajorantAtBaseEqInnerOfPackage.lean#L142-L195
[data]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Formalism/LocalToGlobal/IndefiniteReal/BaseLiftsPackageOfPrimitiveLinks.lean#L240-L283
[frame]: https://github.com/rh-lean-roadmap/rh-lean-roadmap/blob/94e6a98b4e74932a0298d6bd22d44cf60c62764b/docs/src/book/main.tex#L33032-L33041
