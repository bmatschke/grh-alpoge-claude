# The deep trace and the three arithmetic counts

Fix an actual automorphic row with the group, Haar measures, lowest-type vectors, level and parameters of ARO24–27, on its uniform counting range. Let $e$ be its total idempotent or either of the two idempotents cutting out the bad labels at one distinguished prime. Write $D$ for the dimension of the $e$-projected archimedean intertwiner space, $V$ for the original quotient volume, $a=d_\infty\operatorname{Re}e(1)$ and $D^\star=aV$. Then, uniformly in the row and in these three choices,
$$
               |D-D^\star|\le e^{-nf\log n/16}D^\star .
$$
This is the counting theorem in Roadmap B8.53, at these three original test functions. The classical input for volume is the nonsingular representation-density formula in the convergent range of Siegel–Weil with self-dual measures. The comparison below supplies the arithmetic counts required by ARO28 whenever the indicated row and its parameter ties have been realized. Identifying their counted good indices with the indices on a particular selected family is a further assertion. [External statement and its hypotheses][count] · [Classical input in the required measures](RETAINED_DIMENSION_COMPARISON.md#the-classical-input-is-a-representation-density-formula) · [ARO26–28](arithmetic_rows_v46/main.tex#L1043-L1168)

## Matching the theorem to the three projectors

The rank and real degree are $n,f$, the source's single signature is $(p,q)$, and $g=g_0g_1$ is the level. ARO25–26 write each test in the finite convolution algebra of the full lattice stabilizer with its own $\mu_f(K(g))$ in the denominator. Each is a self-adjoint idempotent, hence of positive type. Its support at the complementary prime has unipotent reduction even when the label at the tested prime is bad. Either prime serves for the total test. The two distinguished primes split completely, are larger than $4n$, and the additional level predicate of B8.53 holds by the explicit cylinder formula. ARO27 matches the Harish–Chandra parameter, its strict decrease and parity, the bound $|\lambda_i|\le b^2$, the corresponding opposite-sign gap $h$, the fixed signature, $q^2\le n$, the discriminant and the level growth. Use the constants $c_b=c=1/16$ specified by B8.53 in this application. Its rank cutoff and lower gap constant are chosen for the level-growth exponent $A$ before choosing a row, a type subset or a cylinder. When $q=0$, the [definite trace](continuation_v83/cylinder.tex#L68-L96) already gives equality. Below suppose $q\ge1$. [Pinned counting hypotheses][base] · [Source of the uniform constants][const]

## Why a small deep locus also has a small trace

Set $N=n^2f$, $H=nf\log n$, $r=\mathrm{rd}_E$, $X=nfrgb$ and $\tau_* = X^{-11q}$. Let $K_e$ be the kernel of the projector including the archimedean rank-one test. B8.53e, applied on the quotient just identified, gives a continuous kernel, its diagonal as the sum of squared basis values, and
$$
             \int_{\operatorname{least}(x)<\tau_*} K_e(x,x)\,dx
                         \le e^{-N}D.
$$
Here the right side has the actual dimension $D$. An estimate for the measure of this set alone would permit all the basis mass to concentrate there. The deep trace estimate uses cuspidality and short unipotent orbits. The following details specify the scale of the estimate and show why the same corollary applies to the bad-label tests. [Corollary and parameter definitions][deep] · [Proof for the counted basis][kernel]

Take first any finite orthonormal family of $D_0$ intertwiners in the projected space. By irreducibility their adjoint products are scalar, so they are isometries with orthogonal images. The finite test forces $K(g)$ invariance. The lowest-type vectors and their Lie derivatives have continuous representatives, obtained by a compact smooth average at infinity followed by the compact-type projector and finite-level average. Their constant terms vanish. In the proof of B8.53e, the real projector reproduces each basis vector by coefficient orthogonality. Its constant term along a proper radical can be computed after convolution, since the [large-gap real coefficient bound](RETAINED_FAR_TERMS.md) dominates the polynomial in the inverse least lattice size and the growth of the radical integral. The translated discrete-series coefficient has zero integral over that radical by Harish–Chandra's cuspidality theorem. This proves cuspidality even for a test initially defined on all of $L^2$. [Cuspidality on these vectors][cusp] · [Real discrete-series input in the proof][kernel]

Write $\tau=\operatorname{least}(x)$ at a deep point. In the isotropic flag from $\tau$ up to $1/2$, at most $q$ consecutive ratios have product $2\tau$. One ratio is at most $(2\tau)^{1/q}$. Its isotropic sublattice determines a proper parabolic. The real quotient of its unipotent radical at the given finite level can be represented by paths of total Hilbert–Schmidt length at most
$$
           \rho=\frac{n^2\sqrt f\,g r}{4}(2\tau)^{1/q}.
$$
For this step the external proof bounds the dual shortest vector of the Hom lattice by the ratio of the source and target slopes, with the inverse different included. Euclidean transference bounds the covering radius. The first layer is lifted together with its adjoint. Approximation in the centre uses $\Phi-\Phi^*$, and reduction by $2g$ in the first layer clears the half appearing in the quadratic term of the unipotent exponential. Additive approximation first in that layer and then in the centre handles all the finite places. This explains the level $g$ and the discriminant $r$ in the displayed radius. [The two covering radii and congruence][cover] · [Banaszczyk’s transference theorem](https://doi.org/10.1007/BF01445125)

Put $k=8qN$ and $B=\sqrt n\,b^2+\tfrac32 n^{3/2}+3(k+N)$. Casimir estimates bound Lie differentiation through this order. On the paths the least size is at least $\tau e^{-\rho}\ge\tau/2$. Integration on an ordered exponential cube of side $1/B$ in $N$ real directions bounds evaluation of the vector of basis functions. Its overlap is bounded by the same separated arithmetic ball used for the far terms. The inequality $|v(0)|^2\le(2/s)\int_0^s|v|^2+2s\int_0^s|v'|^2$ iterated over the cube yields the initial squared factor $(6B)^N e^f (17\sqrt n/\tau^2)^{2N}$. A zero constant term lets one subtract the average over the short orbit. The fundamental theorem of calculus bounds the difference by the path length times one more derivative. Repeating on the derivative spaces $k$ times costs $(2\rho\sqrt f B)^{2k}$ in the squared estimate. If $P_0$ is the product of the scalars changing the original infinite Haar measures to Hilbert–Schmidt gauges, and $k_R=\mu_f(K(g))$, B8.53d gives
$$
 \sum_{i=1}^{D_0}|F_i(w,x)|^2
 \le U D_0 P_0/k_R,\qquad
 U=(2\rho\sqrt f B)^{2k}(6B)^Ne^f(17\sqrt n/\tau^2)^{2N}.
$$
B8.53b gives $P_0 V\le X^N g^{2N} k_R$. In particular rescaling the quotient Haar measure does not affect the integrated bound. This absolute-volume estimate uses the same one-vector Siegel–Weil ratios as the [flag measure](RETAINED_FLAG_MEASURE.md), starting in rank two with Minkowski's ideal and lattice bounds. The finite index is at most $g^{2N}$ by reduction on integral endomorphisms. [Sobolev bound and iteration][sob] · [Absolute volume in the chosen gauges][volume]

For the exponent, let $Y=X^q$. We have $X\ge16$, $B\le30X^3$, $n^2fgrB/2\le X^6$ and $\tau Y^{11}\le1$. Taking the $N$th root, the orbit factor contributes at most $Y^{96}(2\tau)^{16}$. The inverse lattice-size factor consumes $\tau^{-4}$. With $Bng^2 X\le Y^{10}$, the remaining expression is at most $2^{16}\,6\cdot289 e\,Y^{-26}\le e^{-1}$. Hence $U X^N g^{2N}\le e^{-N}$. This gives $e^{-N}D_0/V$ pointwise at deep points. On the moderate region the cube bound for a single normalized linear combination gives a uniformly bounded evaluation functional, so the sum of squared basis evaluations there is bounded independently of $D_0$. Integrating and using the deep inequality bounds $(1-e^{-N})D_0$ independently of the finite family. The full projected space is finite dimensional. Its basis gives the continuous diagonal and the claimed integrated deep bound. The unfolded orbit sum agrees with the finite-rank kernel on compactly supported tests, and locally uniform convergence gives equality of their continuous kernels. [Numerical lemma][num] · [Kernel identification and finiteness][kernel]

## Combining the four contributions

On the moderate region the absolute nonidentity contributions are at most $\alpha D^\star$ for [near terms](RETAINED_FLAG_MEASURE.md) and $\beta D^\star$ for [far terms](RETAINED_FAR_TERMS.md), where $\alpha=e^{-H/4}$ and $\beta=e^{-N}$. The geometric flag bound also gives $\operatorname{vol}(\mathrm{deep})\le\alpha V$ in the eventual range. On the deep region the diagonal has total mass at most $\beta D$. Thus
$$
 |D-D^\star|\le(2\alpha+\beta)D^\star+\beta D,
 \qquad
 (1-\beta)|D-D^\star|\le(2\alpha+2\beta)D^\star .
$$
For sufficiently large $n$ the last coefficient after division by $1-\beta$ is at most $e^{-H/16}$. This includes $D^\star=0$, and the bounds take one threshold for all three projectors. In particular they meet the weaker relative-error allowance $1/2$ of GQT5. [Combination in the pinned proof][combine] · [Three-count deduction](global_quantitative_v42/main.tex#L340-L378)

For a given row system, the nonnegative local weights from ARO29 and the size inequalities of GQT3 now imply the desired bound on its discarded fraction as soon as the full and good arithmetic indices are identified with the family's indices. The family statement requires one and the same automorphic realization, its two finite-type label projectors in the prescribed tame generators, the isometry carrying the good space and the common eventual size conditions. B8.52 uses a label realization among its hypotheses. The [selected-family proof](SELECTED_RETAINED_DEFECT.md) identifies this isometry and proves the scalar estimate with the required family quantifiers. [Label realization in the counting theorem][labels] · [What the original family operation consumes][ties]

[count]: https://github.com/rh-lean-roadmap/rh-lean-roadmap/blob/94e6a98b4e74932a0298d6bd22d44cf60c62764b/docs/src/book/main.tex#L24055-L24100
[deep]: https://github.com/rh-lean-roadmap/rh-lean-roadmap/blob/94e6a98b4e74932a0298d6bd22d44cf60c62764b/docs/src/book/main.tex#L24147-L24192
[cover]: https://github.com/rh-lean-roadmap/rh-lean-roadmap/blob/94e6a98b4e74932a0298d6bd22d44cf60c62764b/docs/src/book/main.tex#L58597-L58621
[sob]: https://github.com/rh-lean-roadmap/rh-lean-roadmap/blob/94e6a98b4e74932a0298d6bd22d44cf60c62764b/docs/src/book/main.tex#L58576-L58624
[volume]: https://github.com/rh-lean-roadmap/rh-lean-roadmap/blob/94e6a98b4e74932a0298d6bd22d44cf60c62764b/docs/src/book/main.tex#L58506-L58528
[num]: https://github.com/rh-lean-roadmap/rh-lean-roadmap/blob/94e6a98b4e74932a0298d6bd22d44cf60c62764b/docs/src/book/main.tex#L24147-L24163
[kernel]: https://github.com/rh-lean-roadmap/rh-lean-roadmap/blob/94e6a98b4e74932a0298d6bd22d44cf60c62764b/docs/src/book/main.tex#L58626-L58646
[base]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AbelianVarietyTheory/Definitions/SemilocalFrames/LayerProd.lean#L96-L115
[const]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AbelianVarietyTheory/Proofs/FlagMeasures/CountConstantsOfSiegelWeil.lean#L11-L26
[cusp]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AbelianVarietyTheory/Proofs/FlagMeasures/CountedVectorsAreCuspFormsSingleLowestKType.lean#L85-L114
[combine]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AbelianVarietyTheory/Proofs/FlagMeasures/DiscreteSeriesCountingOfFiniteAndBounds.lean#L34-L142
[labels]: https://github.com/rh-lean-roadmap/rh-lean-roadmap/blob/94e6a98b4e74932a0298d6bd22d44cf60c62764b/docs/src/book/main.tex#L24019-L24049
[ties]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AbelianVarietyTheory/Proofs/GlobalInterpolation/RowCountsOfLinkedTies.lean#L13-L25
