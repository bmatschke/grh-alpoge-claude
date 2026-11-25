# A Hecke determinant for a pair of auxiliary primes

Fix a fitted first-pass theta row, a sign, and an eligible coefficient place of residue characteristic $\ell$. Use its installed universal ray coordinates and integral Hecke readings. Write $r$ for the Hecke rank, $O$ for the coefficient DVR, and $b$ for the number of projected columns in a valid basis. The automorphic polynomial in the [specialization theorem](FIRST_PASS_COPRIME_SPECIALIZATION.md) admits the exponent bound $rb$ at each second prime. The levels of all chosen vectors belong to the finite avoidance set. One open normal subgroup prescribes the first-prime congruence before the level varies. This is the automorphic calculation in Roadmap Proposition B8.07q. [Roadmap proof][book] · [Pinned determinant theorem][det]

## Removing the extra test at a split prime

Take the representative $P$ of a split pair selected by the row, with norm $q$, away from $\ell$ and the level and type primes. Write $O_P$ for the local integers. Summing the determinant test on an integral $r$ by $N$ matrix $Z$ over its labels counts $(N-r)$-planes complementary to its residue row space. In full rank all complements are graphs from one fixed complement to the row space. Their number $q^{r(N-r)}$ cancels the weight of the test. At smaller rank there is no such complement. The summed test is the full-rank indicator.

The order-$j$ double coset runs once over the lattices $\varpi O_P^r\subset L\subset O_P^r$ of index $q^j$. A translated lattice test contributes exactly when the columns of $\bar Z$ belong to the residue space of $L$. If their span has codimension $h$, the annihilators of the admissible residue spaces are the $j$-planes in an $h$-dimensional space. Thus the weighted sum of the spherical tests has value
$$
 \sum_{j=0}^h \genfrac{[}{]}{0pt}{}{h}{j}_q(-1)^j q^{\binom j2}
   =\prod_{a=0}^{h-1}(1-q^a)=\mathbf1_{h=0}.
$$
The first identity is the finite $q$-binomial formula at one, obtained by counting subspaces relative to a fixed hyperplane. Both sides of the test identity vanish on nonintegral matrices. For a uniformizer idèle $x_P$, the row Hecke normalization contributes $\mu(x_P)^{-j}q^{-j\lfloor N/2\rfloor}$. This cancels the splitting character and modulus in the local Weil action. Translation adds $j$ times the ray coordinate of $x_P$ to the smaller-level label. Reindexing the character sum changes the sign of this shift. The inverse arithmetic Frobenius convention for $x_P$ then gives $y^j$, where $y$ is the signed arithmetic Frobenius value. [Identity on theta tests][theta] · [Installed reading and reciprocity][tie]

Let $H_j(P)$ be the integral matrix of the order-$j$ Hecke operator on the lattice obtained by intersecting the good subspace with the full integral lattice in the basis test. It is full in that subspace by clearing denominators. For a testing character inflated from the smaller level, the matrix of columns at the larger level is obtained by left multiplication by
$$
 C_P(y)= I_b+\sum_{j=1}^r(-1)^j q^{\binom j2}H_j(P)y^j .
$$
Indeed the integral multiple of the type projector commutes with every translate at $P$, since its type primes are disjoint from $P$. The matrix therefore concerns precisely the [projected tests](FIRST_PASS_EXPORT_TEST_BASES.md). The [uniform coefficient bound](FIRST_PASS_EXPORT_ROW_COEFFICIENTS.md) allows the same clearing power for these finitely many columns at every admitted level. In the good lattice their scaled empty-level determinant is nonzero. [Coordinates and determinants][matrix]

## First primes give units and second primes give bounded orders

Intersect the kernels of the residual Galois representations giving the reverse Hecke polynomials for the row signatures, with the conjugate conditions. These subgroups are open and normal. At a first prime impose the designated tame Frobenius class in the resulting quotient. Its residual action is scalar $c$ with $c^2\ne1$, and its cyclotomic value is one. Both orientations therefore give a nonzero reverse polynomial at one, either $(1-c)^r$ or $(1-c^{-1})^r$. To see this in the integral determinant, pass to a finite splitting extension and triangularize the commuting Hecke operators. Intersect their common flag with the extended lattice. The intersections are saturated and the successive rank-one quotients retain the diagonal characters after reduction. The determinant is a product of the indicated nonzero residues with their multiplicities. Its unit property descends to $O$. [Frobenius normalization][frob] · [Congruence subgroup][unit]

Let $g$ be the determinant polynomial at the first half of the primes, $f$ the determinant at both halves, and $m_\varnothing$ the scaled empty-level matrix. Successive removal of the first pairs at the trivial character gives $v_O(g(0))=v_O(\det m_\varnothing)$. At level $M$, set the second variables to zero. The chosen ray coordinates give $y=(1+X_i)^{\pm1}$ at the $i$th second prime. Hence
$$
 f\equiv g\prod_i \det C_{P_i'}((1+X_i)^{\pm1})
 \pmod{(Y_i,\ (1+X_i)^{\ell^M}-1)_i}.
$$
Represent the inverse by $(1+X_i)^{\ell^M-1}$. Division by the monic relations leaves a remainder of separate degrees below $\ell^M$. The character identity makes that remainder zero at all root tuples, so successive univariate interpolation over a characteristic-zero splitting field containing $\mu_{\ell^M}$ proves the congruence over $O$.

The reduction of $\det C_P(Y)$ has constant term one and degree at most $rb$. Its order $e$ at $Y=1$ is therefore at most $rb$. For either orientation $Y-1$ is $X$ times a unit after the substitution $Y=(1+X)^{\pm1}$. The residual factor is consequently $X^e$ times a unit, also in the truncation modulo $X^{\ell^M}$. For the empty basis the determinant is one. This bound holds for every admissible family satisfying the first-prime congruence and avoiding the prescribed levels. [Residual exponents][det] · [Use on a common family][join]

[book]: https://github.com/rh-lean-roadmap/rh-lean-roadmap/blob/94e6a98b4e74932a0298d6bd22d44cf60c62764b/docs/src/book/main.tex#L43412-L43441
[theta]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AbelianVarietyTheory/Proofs/InertiaEigenvalues/IsDetRootOfDetAt.lean#L190-L312
[tie]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AbelianVarietyTheory/Proofs/InertiaEigenvalues/UniversalTwistedSeriesDistributionOfCompatibilit.lean#L152-L363
[matrix]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AbelianVarietyTheory/Proofs/InertiaEigenvalues/AevalOneSubOne.lean#L142-L208
[frob]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AutomorphicArithmetic/Foundations/GaloisRepresentations/StringRepresentations/FrobDualOfTripleAttN.lean#L189-L250
[unit]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AbelianVarietyTheory/Proofs/InertiaEigenvalues/ExistsSubgroupIsUnit.lean#L75-L185
[det]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AbelianVarietyTheory/Proofs/InertiaEigenvalues/AevalOneSubOne.lean#L293-L465
[join]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AbelianVarietyTheory/Proofs/InertiaEigenvalues/AdmissibleIndexBoundAllPowersOfConditions.lean#L100-L126
