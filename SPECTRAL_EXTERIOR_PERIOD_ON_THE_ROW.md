# A single exterior shift on the selected real discrete series

Multiplying an orbital integral by its leading minor of order $\ell$ introduces two projected Bessel periods. An algebraic tensor decomposition determines which representations occur. To bound their coefficients one must also compare the period on each new representation to the period on the old one. We make this comparison for the two real flag models in the [minor iteration](SPECTRAL_SHIFTED_MINOR_MOMENTS.md), using their common group Haar measure, their own quotient measures and the normalized [integrated Bessel forms](SPECTRAL_BESSEL_REALIZATION.md).

## Translation inside one regular chamber

Write $n=k+2r+1$, $m=2r+2$, and $\mu=\lambda+\nu$. Take $0\le\ell\le r+1$ and let $E=\bigwedge^\ell\mathbb C^n$ with exterior representation $\rho$. The invariant Hermitian form on $E$ has matrix $\Gamma=\bigwedge^\ell J$, a Hermitian involution for the standard Euclidean inner product. The weights of $E$ are $\mathbf1_I$ for the subsets $I$ of size $\ell$, with multiplicity one. On the grid used below the ordering of all coordinates and the signature labels remain fixed. Indeed the anchor gap is at least $nm^{10}$ and the shift radius $q_0=km^5$ is less than a quarter of that gap.

Let $H$ and $H_I$ be the discrete series with parameters $\mu$ and $\mu+\mathbf1_I$ in this labelled chamber. The coherent family through the discrete series takes the discrete-series character of the same chamber at every regular parameter in it. Its tensor identity gives $[E\otimes H]=\sum_I[H_I]$ on Harish–Chandra modules. One can apply discrete-series translation on the derived group and keep the central-circle character, which shifts by the common weight $\ell$. Distinct subsets give distinct infinitesimal characters since both coordinate lists stay in the same strict order. The primary decomposition for the center of the enveloping algebra therefore separates all the terms. The character identity gives each primary module length one. Consequently this is a direct sum of actual modules. The smooth globalization theorem carries the inclusions and projections to continuous maps on smooth vectors. The identical argument for weights $-e_i$ supplies the dual defining tensor used in the [initial length recurrence](SPECTRAL_BESSEL_MOMENTS.md). [Zuckerman's tensor product theorem](https://annals.math.princeton.edu/articles/196-1/p05) · [Coherent translation](https://www.mathunion.org/fileadmin/ICM/Proceedings/ICM1978.2/ICM1978.2.ocr.pdf) · [Bernstein and Krötz on smooth globalization](https://arxiv.org/abs/0812.1684)

Equip the tensor with the product of the invariant indefinite form on $E$ and the unitary form on $H$. Inequivalent unitary irreducibles are orthogonal for this form by Schur's lemma, first on the modules of compact-finite vectors. Its restriction to each summand is a nonzero real multiple of the unitary form there. A zero multiple would put a whole summand in the radical of the product form. Scale the inclusions $i_I$ to make these multiples $\epsilon_I\in\{-1,1\}$. Then the projections $p_I$ obey $p_I i_J=\delta_{IJ}$ (the identity on the common summand when $I=J$), $\sum i_I p_I=1$, and $p_I=\epsilon_I i_I^\dagger$ for the indicated forms. Smooth continuity extends these identities to the vectors used below.

## Where the square root of the formal degree enters

Work first in the unit simple-root character. Put $X=S\backslash G$ for the Bessel quotient. For a live period $B$ on $H$, the map $v\mapsto F(v)(x)=\sqrt d\,B(\pi(x)v)$ is an isometry into the Hilbert space of square-integrable equivariant sections on $X$. Define $F_I$ with its own degree $d_I$ on each live child. The [rank-one integral and isometry](SPECTRAL_BESSEL_REALIZATION.md) also specify the zero case. Let $\omega=f_0\wedge\cdots\wedge f_{\ell-1}$ in the flag model. The group $S$ acts trivially on this wedge: on the initial flag its unipotent acts triangularly with diagonal one and the compact middle group fixes the initial vectors modulo their predecessors (also for the final vector when present). Denote contraction with $\omega$ in the invariant form by $\operatorname{ev}_\omega$.

The map $T_I v=p_I(\omega\otimes v)$ intertwines $S$. Uniqueness of the parent Bessel functional gives $B_I T_I=\kappa_I B$, where $\kappa_I=0$ if $B_I=0$. To see the adjoint relation with the same scalar, take a compact-finite test vector $w$ in the parent and one $y$ in the child. Under the integrated matrix coefficient on $S$, moving $T_I$ to the other side gives $T_I^*=\epsilon_I\operatorname{ev}_\omega i_I$. The extended integrals have the same Haar measure and twist on both sides. Their rank-one factorizations give
$$
 (B_I T_I w)(B_I y)^*=\epsilon_I (Bw)(B\operatorname{ev}_\omega i_I y)^* .
$$
Take $Bw\ne0$, cancel that column, and extend by smooth density. Thus $B\operatorname{ev}_\omega i_I=\epsilon_I\overline{\kappa_I}B_I$, including the child with zero integrated period. This argument uses the relative scale of the two rank-one forms. [Bessel multiplicity one](https://arxiv.org/abs/0908.1728) · [Projection, adjoint and torus transport in the original proof][side]

Set $b_I=\epsilon_I\overline{\kappa_I}\sqrt{d/d_I}$. For any smooth $y$ in a live child one has
$$
 |b_I|^2\|y\|^2\le
 \int_X\|\rho(x)^{-1}\omega\|_{\rm Eucl}^2\,\|F_I(y)(x)\|^2\,dx .                 \tag{1}
$$
For a proof, let $e$ run through the standard orthonormal exterior basis. Write $y_e$ for the $e$-coordinate of $i_Iy$. Tensor $\Gamma e$ with a smooth parent vector $v$, apply the group action at $x$, and contract with $\omega$. The adjoint relation expands the resulting multiple of $F(v)(x)$ as the finite sum of $b_J F_J(p_J(\Gamma e\otimes v))(x)$ over the live children. The scalar multiplying $F(v)(x)$ has modulus $|h_e(x)|$ with $|h_e(x)|=|[\rho(x)\Gamma e,\omega]_\Gamma|$. Pair with $F_I(y)$ and integrate. The child images of inequivalent representations are orthogonal because the adjoint of one isometric embedding composed with the other is an intertwiner. The absolute value of the surviving pairing is $|b_I|\,|\langle y_e,v\rangle|$, by signed adjointness and $\Gamma^2=1$. Cauchy–Schwarz, the parent isometry and $v=y_e$ give
$$
 |b_I|^2\|y_e\|^2\le \int_X |h_e(x)|^2\|F_I(y)(x)\|^2\,dx .
$$
This includes $y_e=0$. Summing over $e$ gives (1): the sum of $|h_e|^2$ is $\|\rho(x)^{-1}\omega\|_{\rm Eucl}^2$ by invariance and Parseval, and $\sum_e\|y_e\|^2\ge |[i_Iy,i_Iy]|=\|y\|^2$. [Quotient pairing][pair] · [Weighted coordinate estimate][weight]

## A product of successive flag lengths

For a unit lowest-compact-type vector $y$ in the child, $dP(x)=\|F_I(y)(x)\|^2dx$ is a probability measure. Gram–Schmidt gives $\|\rho(x)^{-1}\omega\|_{\rm Eucl}^2=\prod_{a<\ell} L_a(x)^2$, where $L_a$ is the Euclidean length of the $a$th residual vector. Write $R_j=L_{j+1}/L_j$. At the child's own shift $\eta=\nu+\mathbf1_I$, the [length recurrences](SPECTRAL_BESSEL_MOMENTS.md) give
$$
 \mathbb E L_0^{2u}\le A(T)^u,\quad
 A(T)=n^2T\beta^4(6b_v)^{2(2r+2)},\qquad
 \mathbb E R_j^{2v}\le\beta^{4v}.
$$
Here $u,v\le2n^2$, $\|\eta\|_1+u\le q_0$, and $\beta$ is the grid envelope. The first recurrence lowers the parameter at each step. The second takes Lie derivatives within the same representation. This distinction saves shift reserve.

For $\ell\ge1$ the product equals $L_0^{2\ell}\prod_{j=0}^{\ell-2} R_j^{2(\ell-1-j)}$. Hölder, including a factor of one for any unused reciprocal exponent, bounds its mean by $A(T)^\ell\beta^{2\ell(\ell-1)}$ whenever $\ell/u+\ell(\ell-1)/(2v)\le1$. For $\ell=1$ use $u=1$. For $\ell>1$ take $u=\ell+1$ and $v=2n^2$. The condition becomes $(\ell-1)\ell(\ell+1)\le4n^2$, satisfied on the selected grid where $m^4\le k$. Thus $\|\nu\|_1+\ell+u\le q_0$ suffices. In particular this covers the interior shifts $\|\nu\|_1\le C_nkm^3$ eventually for each fixed $C_n$ as $m$ grows. The envelope $H(T)=\max(1,T)\beta^{20(r+1)}$ works since $\ell-1\le r$ and $A(T)\beta^{4r}\le H(T)$ using $n\le\beta$ and $6b_v\le\beta^2$. For $\ell=0$ the child is the parent up to unitary equivalence and the rank-one normalization gives modulus one for the nonzero scalar. [Exterior wedge and lengths][wedge] · [Original lowest-type product estimate][product]

## The two physical periods and the sum over shifts

Transport from the unit character to the two physical frames scales their wedges by numbers of moduli $S_\ell$ and $S'_\ell$. By equivariance these multiply the projected-period scalars. Equation (1) therefore gives $|\kappa_I^{\rm phys}|^2d/d_I\le S_\ell^2 A(T)^\ell\beta^{2\ell(\ell-1)}$ on the first side and the corresponding bound with $S'_\ell,T'$ on the second. The [common-section mass computation](SPECTRAL_SHIFTED_MINOR_MOMENTS.md) bounds the absolute coefficient $a_I$ of the unit-section child amplitude by $\sqrt{d/d_I}\,|\kappa_I^{\rm phys}\kappa_I^{\prime\rm phys}|$. Its remaining degree factor is thus $\sqrt{d_I/d}$.

In fact the summation of these degree factors costs at most $\binom n\ell$. For the same group Haar measure the discrete-series degree formula on this chamber gives $d_I/d=\Delta(\mu+\mathbf1_I)/\Delta(\mu)$ with $\Delta(x)=\prod_{i<j}(x_i-x_j)$. The polynomial $\sum_{|I|=\ell}\Delta(x+\mathbf1_I)$ is alternating, since a permutation also permutes all the subsets. It is divisible by $\Delta(x)$ and has degree at most $\deg\Delta$. Its highest-degree part is $\binom n\ell\Delta(x)$. Division proves the exact identity $\sum_I d_I/d=\binom n\ell$. All ratios are positive. Cauchy–Schwarz now yields $\sum_I\sqrt{d_I/d}\le\binom n\ell$, also for any subcollection on the left. We obtain
$$
 \sum_{I\ {\rm live}} |a_I|
 \le \binom n\ell\,S_\ell S'_\ell\,[A(T)A(T')]^{\ell/2}\beta^{2\ell(\ell-1)} .       \tag{2}
$$
The original cost $b^{C_Dm^2}$ follows with one $b^{Um^2}$ allowance for subset multiplicity in place of the former two. All constants can be chosen before the iteration depth. This proves the one-step period and degree estimates for these selected normalized local models. The pointwise estimate through which (2) enters the global count still requires the [wave and compact-type estimates](SPECTRAL_ORDINARY_SQUARED_AMPLITUDE.md) and the physical orbital and section identifications specified there.

[side]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AbelianVarietyTheory/Proofs/FlagMeasures/LeadingMinorLineUnitAmplitudesLargeGaps.lean#L276-L311
[pair]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/CompanionTheory/AutomorphicTheory/PieriRules/ThetaBesselIsometries/TensorMomentTransfer.lean#L65-L106
[weight]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/CompanionTheory/AutomorphicTheory/PieriRules/ThetaBesselIsometries/TensorMomentWeighted.lean#L54-L118
[wedge]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AbelianVarietyTheory/Proofs/FlagMeasures/FlagWedgeFixedAndLengthEqProdDistances.lean#L23-L68
[product]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AbelianVarietyTheory/Proofs/FlagMeasures/ProductMomentFirstLengthsLowestVector.lean#L25-L110
