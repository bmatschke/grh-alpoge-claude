# The reference quotient and the height of each nonzero word map

Fix the original linked selector, a selected member, its **sharp level** and the **reference tuple** $t_0=\mu_0$ at that level. Entry 6 asks for the infinite-place mean of the log **squared** operator norm of each nonzero native word map $B_u$ to be at most its assigned $h_u$. On the selected definite-table and lower-weight hypotheses, it suffices to prove
$$
          P_{u,0}(x,k)=0\qquad(x\in X_u,\ k\in\ker q). \tag{1}
$$
Here $P_{u,0}$ is the actual arithmetic point evaluation before taking the quotient. The original mixed period comparison implies (1) already at its reference tuple. There is also a quantitative alternative below that permits (1) to fail. Neither argument needs finite-place integrality, nonreference-tuple comparisons, or normalization of the sizes of the scalar factors in the complex Bessel comparison. The derivation uses the selected table and analytic hypotheses specified below.

## The two lifts of a reference-row vector

Use the prescribed column isometry to identify $X_u$ with the reference column, keeping its infinite metrics. In the coordinates of the selected definite face write $V$ for the reference test space, $H$ for its Hermitian form, $q:V\to Q$ for the surjective reference quotient, and $i:Q\to W$ for the native isomorphism onto the sharp target. For each rational basis vector $y\in Q$, choose a rational lift $z$. In the native distinguished ambient inner product R88L3 projects $J(z)$ onto $J(\ker q)$, where $J=j_A\circ V_0$. It solves the Gram equations on an independent family of rational image columns. Their Gram matrix is positive definite and rational for the distinguished conjugation. Thus the projection is $J(z')$ for a rational $z'\in\ker q$. Assign $s(y)=z-z'$ on the basis and extend over $K$. Then $qs=1$, and the native section in the definition of $B_u$ has value $J(sy)$ in the original ambient space. Reading the definite period via $C.\mathrm{pt}$ and using the retained norm-extension law to identify the recorded rational map gives
$$
                 B_u(x,iy)=P_{u,0}(x,s y).                 \tag{2}
$$
This identity over $K$ transports to every coefficient embedding. The main proof below uses only (2) and $qs=1$. Under (1) an arbitrary rational section gives the same evaluation. [Selected rational section and period][section] · [Formal construction of the kernel lift][rational]

The original distinguished metric can also be checked directly. Let $M$ be the original class Gram matrix, $L$ the level inclusion, $L^+$ its projection to level coordinates, and $G$ the good-coordinate inclusion into the original class space. The sharp forms tie gives $\langle j_A x,j_A y\rangle=\sigma_0(h_{H_{\rm lev}}(x,y))$ and the coordinate matrix in $J$ is $L^+G$. The definitions give $H_{\rm lev}=|P|^{-1}L^*ML$ and $H=|P|^{-1}G^*MG$, for the same selected subgroup $P$. The range of $G$ lies in the level space, so $LL^+G=G$ at the distinguished embedding. Substituting this in $(L^+G)^*H_{\rm lev}(L^+G)$ gives $H$. Thus the metric used to construct the native distinguished section really is the reference test metric in these coordinates, including its normalization. Positivity now also makes $J$ injective there and identifies $s$ with the distinguished minimal lift. Only the last, CM-field alternative below needs this distinguished identification. [Sharp forms reading][sharpforms] · [Forms tie and coordinate matrices][formstie] · [Normalized restricted Gram matrices][grams] · [Containment of the good space in the level][contain]

At an embedding $\sigma$ representing the infinite place $v$, let $j_v:Q_\sigma\to V_\sigma$ be the minimal-norm lift with respect to $H_v$. Its coordinate matrix is
$$
 j_v=H_v^{-1}q_\sigma^*(q_\sigma H_v^{-1}q_\sigma^*)^{-1}.
$$
The actual quotient metric makes this map an isometry. Put $E_v=s_\sigma-j_v$. Since $q_\sigma s_\sigma=q_\sigma j_v=1$, its image is in $\ker q_\sigma$. This kernel is orthogonal to $j_v Q_\sigma$ by construction of $j_v$ independently of the choice of $s$. Thus a rational section and an isometric section are both available. They can differ at embeddings that do not commute with the distinguished conjugation. [Native definition and quotient metric][metric]

Let $C_v$ be the positive self-adjoint operator on $Q_\sigma$ representing the pullback of the metric of $W_v$ relative to its quotient metric. The actual row identities give the scalar $c_{pv}=\kappa_v\prod_j\lambda_{jpv}$ on each spanning primitive subspace. Write $a_v$ for the minimum over the nonzero primitive spaces. For a nonzero word map this set is nonempty. The norm of a covector on $W_v$ is bounded by $a_v^{-1/2}$ times its pulled-back quotient dual norm. For an exact formula let $\Pi_{\gamma,v}$ be the orthogonal projector onto the entire eigenspace at the distinct eigenvalue $\gamma$ of $C_v$, and let $d_x\in V_\sigma$ represent the covector $P_{u,0,\sigma}(x,-)$ by Riesz duality. Then (2) gives
$$
       \|B_u\|_v^2
       =\sup_{\|x\|=1}\sum_{\gamma}\gamma^{-1}
                       \|\Pi_{\gamma,v}s_\sigma^*d_x\|^2 .     \tag{3}
$$
Grouping by distinct eigenvalues covers coincident primitive scalars. Formula (3) uses the actual column metrics and the word's evaluation matrix. [Sharp row scalar at the reference tuple and every place][scalar]

## The estimate on the selected family

The definite condition factors this reference evaluation into the ordinary and complementary kernels followed by the terminal period, starting in the prescribed column frame and ending at $H_v$. The squared transition bounds multiply. With $A$ the terminal-table bound and $s_{jv}$ the assigned layer costs, put $D_{uv}=\exp((A+\sum_j s_{jv})/2)$. Then
$$
   \|P_{u,0,\sigma}\|\le D_{uv},\qquad
   A\le H_{P,u},\quad \langle s_{jv}\rangle_\infty\le H_{K,uj}.
$$
B8.36 derives the definite condition from the point-evaluation identifications, compatible weights, lattice fullness and size bounds. B8.37 supplies it eventually on a linked family in $W_3$ for every permitted $C\ge0$. The sharp-level lower-weight assertion of B8.08b gives $\log\lambda_{jpv}\ge L_{6,j}$ on the prescribed covolume-family/admissible-point hypotheses, including $P$ of Definition B1.15ac. For eligible $F_m,C_H$, one cutoff serves all later indices, every point in the specified class, every real $C$, all layers and primitive blocks, and all infinite places. The existing project reduction identifies the specific one-layer analytic inputs. Use the same constants and division/row identifications throughout, and take the maximum of the eventual cutoffs before $i,u,v$. [Definite table][table] · [Table budgets][budget] · [Selected-family definite condition][family] · [Sharp lower bound and quantifiers][low] · [One-layer prerequisites][onelayer]

Under (1), scalar extension gives $P_{u,0,\sigma}(x,E_v y)=0$. Replace $s_\sigma$ by $j_v$ in (2), then apply its norm one property and the dual row comparison. For every nonzero $B_u$ one obtains
$$
 h(B_u)\le A+\sum_j\langle s_{jv}\rangle_\infty-\langle\log a_v\rangle_\infty
 \le H_{P,u}+\sum_j H_{K,uj}-\sum_j L_{6,j}
       -\langle\log\kappa_v\rangle_\infty=h_u.             \tag{4}
$$
Every scalar extension of a nonzero rational linear map is nonzero, so the logarithms in (4) exist. The hypothesis of entry 6 excludes zero maps. Equation (4) retains a negative $h_u$ when prescribed. The reference mixed identity implies (1) because its model row argument factors through $iq$, including at a kernel vector. Thus if that upstream native identity and the table/floor inputs are retained, entry 6 requires no further independent family hypothesis. A self-contained proof can target just (1) together with the table/floor inputs. [Reference matrix criterion and row factorization][criterion] · [Original allowance and nonzero-map convention][allowance]

## Two routes without reference kernel vanishing

When (1) is unavailable, write $R_{uv}=P_{u,0,\sigma}|_{X_{u,\sigma}\times\ker q_\sigma}$ in the restricted test metric and $\eta_{uv}=\|R_{uv}\|\|E_v\|/D_{uv}$. The triangle inequality in (2) gives $\|B_u\|_v\le a_v^{-1/2}D_{uv}(1+\eta_{uv})$. Orthogonality also gives $s_\sigma^*s_\sigma=1+E_v^*E_v$, hence $\|B_u\|_v^2\le a_v^{-1}D_{uv}^2(1+\|E_v\|^2)$. The actual available slack is
$$
 S_u=h_u-\big(A+\sum_j\langle s_{jv}\rangle_\infty-\langle\log a_v\rangle_\infty\big)\ \ge0 .
$$
It therefore suffices that
$$
 \left\langle\min\{2\log(1+\eta_{uv}),\,\log(1+\|E_v\|^2)\}\right\rangle_\infty
       \le S_u                                             \tag{5}
$$
for each required word. Every term is determined by the reference matrices and original tables. A family estimate establishing (5) remains open.

A purely algebraic sufficient hypothesis is that $\ker q$ have a basis over the selected conjugation-compatible CM subfield $K_0$ in the same reference coordinates as $H$. With $G$ the matrix of that basis, the projection $G(G^*HG)^{-1}G^*H$ transports to the orthogonal projection at every embedding, since $H$ is over $K_0$ and every restricted embedding commutes with its conjugation. Applying the complementary projection to any rational lift gives $s$ and proves $E_v=0$ at all places. The zero-dimensional kernel uses the zero projection. The native well-formedness condition supplies CM rationality of $H$, whereas the kernel is initially only given as the kernel of a matrix over $K$. The kernel's field of definition remains to be derived for this route. It concerns the sharp test quotient specifically. [Native field and metric hypotheses][metric]

For a concrete example of the field issue take $K=\mathbb Q(i,r)$ for the real root $r$ of $t^3-t-1$. Let the distinguished conjugation fix $r$ and send $i$ to $-i$. Set $H=I$, $q=(1,r)$, and use the actual quotient metric at each place. Then $s=(1,r)^{\mathsf T}/(1+r^2)$ is the distinguished minimal lift. At an embedding sending $r$ to a nonreal root $z$ the squared operator norm of $s_\sigma$ for the local quotient metric is
$$
             \frac{(1+|z|^2)^2}{|1+z^2|^2}>1 .
$$
The difference of numerator and denominator is $4(\operatorname{Im}z)^2$, and $1+z^2\ne0$. The cubic is irreducible over $\mathbb Q$ by the rational root test and has discriminant $-23$, so such an embedding exists and extends to $K$. This example verifies the possible cost of replacing a local isometric lift by a transported rational lift even with a rational positive Gram matrix. It makes no assertion about the actual sharp kernels.

Equations (2)–(5) give the exact reference reduction and the conditional height estimate. For a direct reconstruction the remaining independent step is reference kernel vanishing, the slack bound (5), or another proof controlling (3), on the same selected range together with the cited table and spectral inputs.

## The same Gram determinant in entries 6 and 7

The metric identification at the distinguished place above implies that one can use the rational orthogonal section $s=H^{-1}q^*(qH^{-1}q^*)^{-1}$ over $K$. Here the star uses the distinguished involution. At an embedding $\sigma$ put $\sigma'(a)=\overline{\sigma(\bar a)}$, $A=q_\sigma H_\sigma^{-1/2}$ and $B=q_{\sigma'}H_\sigma^{-1/2}$. The source and conjugate-source test metrics agree because $H$ has its entries in the conjugation-compatible subfield. Let $U=(AA^*)^{-1/2}A$ and $V=(BB^*)^{-1/2}B$. Both matrices have orthonormal rows. In the Euclidean test coordinates defined by $H_\sigma^{1/2}$ and quotient coordinates defined by $(AA^*)^{-1/2}$, the native section becomes
$$
       B^*(AB^*)^{-1}(AA^*)^{1/2}=V^*(UV^*)^{-1}.
$$
The inverse exists because the distinguished rational Gram determinant is nonzero. Thus the singular values of $s_\sigma$ are the reciprocals of the singular values of $UV^*$, which lie in $(0,1]$. With the notation $g,d_\sigma$ of [the sharp-row mean computation](PERIOD_RELATIVE_DETERMINANTS.md#direct-computation-on-the-sharp-row),
$$
 \det(s_\sigma^*s_\sigma)
    =|\det(UV^*)|^{-2}
    =\frac{|\sigma(g)|^2}{d_\sigma d_{\sigma'}}.
$$
The first adjoint in this display uses the actual source and quotient metrics at $\sigma$. Averaging the logarithm gives exactly $2E_{Q,1}$ in the normalization of that computation. Since every singular value of $s_\sigma$ is at least one, $\log(1+\|E_v\|^2)=\log\|s_\sigma\|^2\le\log\det(s_\sigma^*s_\sigma)$ at positive rank. In (5), $2E_{Q,1}\le S_u$ is therefore a sufficient alternative, accessible from rational quotient matrices. Entry 7 contains the same defect with coefficient $-1/D_1$. These coefficients have different sizes. Cancellation would require a further estimate.

There is an exact field test for $E_{Q,1}=0$. Choose a nonzero maximal minor $p_{I_0}$ of $q$ and write $p_I$ for its maximal minors in the reference coordinates. All the summands defining the defect are nonnegative, and an individual one vanishes precisely when the two row spaces of $U,V$ coincide. Right multiplication by the common invertible metric factor shows that this is equivalent to equality of the row spaces of $q_\sigma,q_{\sigma'}$. Their Plücker coordinates give equality precisely when $\sigma(p_I/p_{I_0})=\sigma'(p_I/p_{I_0})$ for every $I$. At all embeddings this says that every ratio is in the maximal subfield of $K$ on which all embeddings commute with the distinguished conjugation. The field test can therefore be applied directly to the ratios of minors of the given quotient matrix. The requisite field property or small-defect estimate has not been established for the selected quotients. At zero rank the word map is zero and entry 6 imposes no condition.

[section]: continuation_v88/rows.tex#L100-L145
[metric]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Formalism/LocalToGlobal/IndefiniteForms/IndefSide.lean#L69-L96
[scalar]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Formalism/LocalToGlobal/IndefiniteReal/CxCoreRG.lean#L60-L87
[table]: https://github.com/rh-lean-roadmap/rh-lean-roadmap/blob/02a95b4c62db610642af5f278ee5d0d6df87b348/docs/src/book/main.tex#L21808-L21876
[budget]: https://github.com/rh-lean-roadmap/rh-lean-roadmap/blob/02a95b4c62db610642af5f278ee5d0d6df87b348/docs/src/book/main.tex#L32441-L32477
[family]: https://github.com/rh-lean-roadmap/rh-lean-roadmap/blob/02a95b4c62db610642af5f278ee5d0d6df87b348/docs/src/book/main.tex#L21928-L21952
[low]: https://github.com/rh-lean-roadmap/rh-lean-roadmap/blob/02a95b4c62db610642af5f278ee5d0d6df87b348/docs/src/book/main.tex#L16960-L16969
[onelayer]: PERIOD_OFF_BASE_SCALAR.md
[criterion]: continuation_v89/comparison.tex#L34-L98
[allowance]: https://github.com/rh-lean-roadmap/rh-lean-roadmap/blob/02a95b4c62db610642af5f278ee5d0d6df87b348/docs/src/book/main.tex#L8759-L8787
[rational]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AbelianVarietyTheory/Proofs/DivisorProofs/BuRatOfCoordinates.lean#L17-L45
[sharpforms]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AbelianVarietyTheory/Definitions/AutomorphicMembership/StableIffCarrierEq.lean#L150-L158
[formstie]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Formalism/LocalToGlobal/Divisibility/RowSideTie.lean#L35-L78
[grams]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Formalism/LocalToGlobal/Divisibility/GoodPartHermitianSpec.lean#L90-L141
[contain]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Formalism/LocalToGlobal/Divisibility/RowLatLemmas.lean#L118-L125
