# Descent of the integral theta sections to the original level

Let $K$ be the coefficient field of the pinned base row, $K'$ the coefficient field of an admissible tower cover, and $S$ any set of places of $K'$ over a fixed rational prime $\ell$. Assume $e(\lambda/p)=1$ for each $\lambda\in S$ and its restriction $p$ to $K$. Suppose the adelic reading $f$ of an $S$-integral cusp section on the cover is right invariant under the **original** compact level. Then there is an exact finite decomposition
$$
 f=\sum_j \sigma'(a_j)\, f_j,\qquad
 a_j\in\bigcap_{\lambda\in S}\mathcal O_{K',\lambda},
$$
where each $f_j$ is the original reading of a base section integral at every place below $S$. For $S=\varnothing$ the coefficient condition is vacuous. Neither the number of places nor the degree of the residue extension contributes any power of $\ell$. This is the descent used alongside the [uniform theta-series bound](FIRST_PASS_TOWER_SERIES_BOUND.md). [Quantifiers and level invariance][def] · [Combination of the three steps][assembly]

## Descent over the coefficient field

A rational cover form invariant under the base level is a finite $K'$-linear combination of base readings. The weight is dominant with the required positive last weight, and the holomorphic cusp space at base level is spanned by the algebraic cusp sections. The marking and base embedding identify the pullbacks of these sections. The original determinant correction is constant on each right coset of the base compact, since its root there is a finite unit congruent to one at the two type primes and the tame character evaluates to one. These conditions allow the base-level rational descent theorem to be applied with the actual adelic reading. In particular this step gives an identity of functions, with its specified coefficient embedding. [Tame factor on the original compact][tame] · [Application of rational descent][rat]

## A decomposition at one unramified place

Fix $\lambda\mid p$ in $S$. Write a rational decomposition upstairs as $f'=\sum_i a_i f_i^{\,\prime}$, where primes on the sections mean scalar extension from $K$. One identifies $f'$ as bounded at the integral framed tests over $\lambda$ by the compatibility of the pinned cover reading with scalar extension. For each of the finitely many cuspidal $f_i$, choose $\kappa_i\in K^\times$ making $\kappa_i f_i$ bounded at the integral framed tests above $p$. Choose $b_1,\ldots,b_h\in\mathcal O_{K'}$ lifting a basis of the residue field extension $k_\lambda/k_p$. Then
$$
 a_i=\sum_{j=1}^h x_{ij} b_j+\kappa_i\rho_i,\qquad
 x_{ij}\in K,\quad \rho_i\in\mathcal O_{K',\lambda}.
$$
Indeed a uniformizer of $K_p$ has valuation one at $\lambda$. Starting at the valuation of $a_i$, successively subtract each residue digit in the lifted basis until the remainder has valuation at least $v_\lambda(\kappa_i)$. This is a **finite approximation** to the needed precision, so one can keep the $x_{ij}$ in $K$. It applies when $K'/K$ is non-Galois or $p$ has other primes above it. [Residue lifts and approximation][approx] · [Local boundedness transferred from the cover][one]

Set $F_j=\sum_i x_{ij}f_i$. The error terms $\rho_i(\kappa_i f_i)^{\prime}$ are integral at every test over $\lambda$. Subtracting them shows that $\sum_j b_j F_j^{\,\prime}$ is integral there. To infer integrality of each $F_j$, take a base integral framed test, extend its complete valued field to admit the relevant embeddings of a normal closure, and pull the frame back there. The pin proves that the frame remains integral under this operation. Write $t_j$ for the base evaluations of $F_j$. For every conjugate in the decomposition group one obtains
$$
 \left|\sum_j g(b_j)t_j\right|\le 1 .
$$
If $\max_j|t_j|>1$, divide by a coordinate attaining the maximum and reduce modulo the maximal ideal. The residue coordinates $z_j$ satisfy $\sum_j g(\bar b_j)z_j=0$ for every residue automorphism, with one $z_j=1$. The decomposition group maps onto the residue automorphism group in the normal closure. The columns of this conjugate matrix are independent: the finite residue extension is separable, so trace-dual elements isolate the coefficients, also after embedding in a larger residue field. This contradicts $z_j=1$. Thus each base section $F_j$ is integral above $p$. Together the $F_j$ with coefficients $b_j$ and the $\kappa_i f_i$ with coefficients $\rho_i$ give the desired one-place decomposition. This argument avoids an average divided by the extension degree, which could have an $\ell$-denominator. [Conjugate sums and reduction][trace] · [Test fields and embeddings][test] · [Integral frames and the section calculation][frm] · [Stacks Project, trace pairing, Lemma 9.20.7](https://stacks.math.columbia.edu/tag/0BIL)

## Simultaneous integrality

Only finitely many primes of a number field divide $\ell$. In the local expansion for $\lambda$ multiply each base section by an integral $t\in K$ that is a unit at $p$ and makes that section integral at all other places below $S$. Such a $t$ exists by clearing the finitely many local section bounds and imposing the unit condition at $p$ by comaximality. Divide the coefficient by $t$. It stays integral at $\lambda$. For each $\lambda$ denote the resulting finite coefficient list by $A_\lambda$.

Take $N\ge1$ large enough to clear all poles of all these lists at all members of $S$. For each $\lambda$ put $I_\lambda=\prod_{\mu\in S,\ \mu\ne\lambda}\mu^N$ in $\mathcal O_{K'}$. Their sum is the unit ideal: a maximal ideal containing all of them would have to be one of the $\mu$, and then fail to contain the product omitting that $\mu$. Choose $e_\lambda\in I_\lambda$ with $\sum_\lambda e_\lambda=1$. Every $e_\lambda A_\lambda$ is integral throughout $S$. Multiply the local expansions by the $e_\lambda$ and add. Each expansion read $f$, so their sum still reads $f$. For the empty set use the initial rational expansion. All base sections in the resulting sum are integral below $S$, even when several $\lambda$ restrict to the same $p$. [Construction of the partition][part] · [Rescaling and recombination of the readings][glue] · [Stacks Project, Chinese remainder theorem, Lemma 10.15.4](https://stacks.math.columbia.edu/tag/00DT)

The literature supplies the separable residue-field calculation and the comaximal-ideal identity. The passage from integrality of this particular cover section to bounds at the extended framed points uses the moduli and reading comparisons above. Descent requires unramifiedness at the chosen places and invariance under the original compact. The integral-section bound on the cover has neither of these two additional hypotheses.

[def]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AbelianVarietyTheory/BlockTheory/NonGaloisCusps/TwistSeries.lean#L101-L117
[assembly]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AbelianVarietyTheory/Proofs/InertiaEigenvalues/UnramifiedDescentIntegralFormsTowerCover.lean#L21-L30
[tame]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AbelianVarietyTheory/Proofs/InertiaEigenvalues/CoverFormRationalDescentToBase.lean#L25-L54
[rat]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AbelianVarietyTheory/Proofs/InertiaEigenvalues/CoverFormRationalDescentToBase.lean#L58-L65
[approx]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AbelianVarietyTheory/Proofs/InertiaEigenvalues/CuspFormIntegralLatticeUnramifiedDescent.lean#L180-L265
[one]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AbelianVarietyTheory/Proofs/InertiaEigenvalues/UnramifiedDescentIntegralFormsOnePlace.lean#L35-L66
[trace]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AbelianVarietyTheory/Proofs/InertiaEigenvalues/CuspFormIntegralLatticeUnramifiedDescent.lean#L23-L102
[test]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AbelianVarietyTheory/Proofs/InertiaEigenvalues/CuspFormIntegralLatticeUnramifiedDescent.lean#L267-L318
[frm]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AbelianVarietyTheory/Proofs/InertiaEigenvalues/CuspFormIntegralLatticeUnramifiedDescent.lean#L344-L405
[part]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AbelianVarietyTheory/Proofs/InertiaEigenvalues/ExistsPartitionOneIntegralAtPlaces.lean#L6-L54
[glue]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AbelianVarietyTheory/Proofs/InertiaEigenvalues/GlueIntegralDecompositionsOverRationalPrime.lean#L46-L103
