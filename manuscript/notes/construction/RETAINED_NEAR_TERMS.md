# Which rational elements contribute near the diagonal?

Fix a row member with the original row identification and the counting parameters of ARO24–27. The retained-row count uses the total level projector and the two projectors onto bad labels at $q_0$ and $q_1$. In each trace the same two facts localize its near-diagonal terms. A congruence at the complementary level prime and a bound at every infinite place force each rational element in a near term to be unipotent. A nonidentity element can then contribute only at lattices whose least normalized Harder–Narasimhan size is at most $2^{1/4}e^{\varepsilon/2}\sqrt{\varepsilon}$. Here $\varepsilon=10^{-6}/(n^8 f^2)$ in the original count. Both assertions are pointwise. They require no Haar-volume estimate or decay estimate for discrete-series matrix coefficients. [The three projected counts](../../../research/modules/construction/global_quantitative_v42/main.tex#L168-L249) · [Actual kernels and support](../../../research/modules/construction/arithmetic_rows_v46/main.tex#L980-L1035)

## From the finite test to global unipotence

Write $n\ge1$ for the rank, $E/F$ for the CM extension, and $f=[F:\mathbf Q]$. For an adelic point $x$, equip $\Lambda_x=E^n\cap x_f\widehat\Lambda$ with its prescribed positive archimedean metrics. For a level projector that tests labels at $q_j$, use $g=q_{1-j}$. The finite test at $g$ is supported on a conjugate of the level subgroup with unipotent reduction. The total projector has this property at either prime. In particular, whenever the summand for $\gamma\in U(V)(F)$ is nonzero, the finite part of $x^{-1}\gamma x$ stabilizes $\widehat\Lambda$ and is unipotent modulo $g$. Conjugation and intersection with $E^n$ give

$$
 \gamma\Lambda_x=\Lambda_x,\qquad
 (\gamma-I)^n\Lambda_x\subset g\Lambda_x.
$$

The counting range has $4n<q_0,q_1$ and both primes split completely in $E$, so $g\mathcal O_E$ is radical. The argument below only uses radicality and the indicated size inequality. [Support and the common counting range](../../../research/modules/construction/arithmetic_rows_v46/main.tex#L980-L1112) · [Lattice at the adelic point](https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AbelianVarietyTheory/Proofs/FlagMeasures/LatUnipMapMulVec.lean#L36-L62) · [Counting hypotheses and radius](https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AbelianVarietyTheory/Definitions/SemilocalFrames/LayerProd.lean#L96-L115)

Take $A_v=(x^{-1}\gamma x)_v$ in the prescribed frame. Write $s_{v,i}$ for the logarithms of its singular values, so the source's Cartan distance is $d_{\rm HS}(A_v)=(\sum_i s_{v,i}^2)^{1/2}$. A near term satisfies $d_{\rm HS}(A_v)\le\varepsilon$ at every real place $v$ of $F$. We allow the full range $\varepsilon=c/(n^8f^2)$, $0<c\le10^{-5}$, in the following argument. [Cartan distance](https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AbelianVarietyTheory/Definitions/SemilocalFrames/LayerProd.lean#L15-L23)

For each $1\le j\le n$ put $a_j=\operatorname{tr}(\gamma^j)-n$. It is an algebraic integer because $\gamma$ preserves the full lattice $\Lambda_x$, which is free after localization at each finite prime. At every prime $\mathfrak p\mid g$, the reduction of $\gamma$ is unipotent, so the reduction of $\gamma^j$ has trace $n$. Radicality gives $a_j\in g\mathcal O_E$. At infinity, $\|A_v\|_{\rm op}\le e^{\varepsilon}$, and therefore

$$
 |\operatorname{tr}(A_v^j)-n|\le n(e^{j\varepsilon}+1)<3n<g.
$$

Here $n\varepsilon\le10^{-5}$. Each embedding of $E$ is the chosen embedding over some $v$ or its conjugate, and the trace is invariant under change of frame. Thus every conjugate of $a_j/g$ has modulus less than one. The norm of a nonzero algebraic integer is a nonzero integer, forcing $a_j=0$.

Newton's identities recover the first $n$ elementary symmetric functions from these power sums in characteristic zero. Since the power sums are those of $n$ ones, the characteristic polynomial is $(T-1)^n$. Cayley–Hamilton gives $(\gamma-I)^n=0$ over $E$, hence at every place. This argument uses the complementary prime on the *support* of the actual projector, so it applies to the exceptional-label projectors as well as the total trace. [Pinned near-element theorem](https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AbelianVarietyTheory/Proofs/FlagMeasures/ConjPowOfMulEqOne.lean#L93-L157)

## A sharper radius and a bound on the least lattice size

The identities $\operatorname{tr}A_v=n$ and $\det A_v=1$ give an especially short estimate in the original metric. Suppress $v$ and put $s_i=s_{v,i}$. Then $\sum_i s_i=0$ and

$$
 \|A-I\|_{\rm HS}^2
 =\operatorname{tr}(A^*A)-2\operatorname{Re}\operatorname{tr}A+n
 =\sum_i (e^{2s_i}-1-2s_i)
 \le 2e^{2\varepsilon}\sum_i s_i^2 .
$$

The inequality is Taylor's formula with $|s_i|\le\varepsilon$. Consequently every $A_v-I$ has Hilbert–Schmidt norm at most $\Delta=\sqrt2 e^{\varepsilon}\varepsilon\le 3\sqrt{n\varepsilon}$. The source’s two auxiliary numerical bounds are $3\sqrt{n\varepsilon}<1/4$ and $3\sqrt{n\varepsilon}\,qnf\le1/100$ when $q^2\le n$. Indeed the latter product is at most $3\sqrt c/n^2\le3/\sqrt{10^5}<1/100$. [Original radius contract](https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AbelianVarietyTheory/Statements/CuspFrameWeights/ConvolutionSmoothL2.lean#L136-L143)

Let $m(x)$ be the infimum of normalized sizes of nonzero sublattices of $\Lambda_x$, and let $M(x)$ be the supremum of the normalized sizes of its positive-rank quotients by saturated sublattices, each with its quotient metrics. Hermitian self-duality, with the chosen compatible majorants, gives $M(x)=1/m(x)$. Indeed the dual of a quotient by a saturated sublattice is an integral sublattice of the dual with reciprocal normalized size. Saturation can only lower the size of a sublattice with the same span, and the Hermitian pairing identifies the dual isometrically up to conjugation. The normalization divides out the covolume of the coefficient ring, so no discriminant factor remains. [Definitions of the two sizes](https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Formalism/HarderNarasimhan/StatementPl.lean#L28-L50) · [Self-duality on the actual lattice](https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AbelianVarietyTheory/Proofs/FlagMeasures/OrthogonalCanonicalFiltrationStepsAutPoint.lean#L340-L360)

If $T=\gamma-I\ne0$, then $T\Lambda_x$ is a positive-rank sublattice. The lattice $\Lambda_x/(\ker T\cap\Lambda_x)$ maps bijectively onto it. At every complex place the map from the quotient space to the image has operator norm at most $\Delta$. For an image of rank $r$ its real Jacobian is at most $\Delta^{2r}$ at that place. Taking covolumes and then the $1/(2fr)$-th power gives

$$
 m(x)\le\operatorname{size}(T\Lambda_x)
 \le \Delta\,\operatorname{size}\bigl(\Lambda_x/(\ker T\cap\Lambda_x)\bigr)
 \le \Delta M(x).
$$

This is the determinant argument underlying Bost's slope inequality. It proves $m(x)^2\le\Delta$. Thus on $m(x)>t_*=\sqrt\Delta$ the sum of the absolute values of the nonidentity near terms is zero. At the counting radius $t_*<0.0012/(n^4f)$, which in particular gives the full original vanishing on $m(x)\ge1/2$. [Bost, Proposition 4.5](https://numdam.org/item/10.1007/s10240-001-8191-3.pdf#page=39) · [Determinant bound in the source normalization](https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Formalism/HarderNarasimhan/StatementPl.lean#L112-L132) · [Where this vanishing enters the count](https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AbelianVarietyTheory/Proofs/FlagMeasures/NearTermsModeratePointsOneTypeBound.lean#L116-L141)

## Bounding the flag constant by a published residue estimate

For the source's CM extension unramified at every finite prime, the coefficient $\kappa_j$ in the flag measure formula can be bounded uniformly by an elementary calculation once Louboutin's unconditional bound for the residue of a Dedekind zeta function is used. Let $L=\log n\ge15$, $s=\sqrt n$, $q^2\le n$, and $\log\operatorname{rd}_E\le e^n$. For every nonempty flag type of total rank $J\le q$ one has

$$
 0<\kappa_j\le \exp\!\left(-\tfrac23 Jnf\log n\right).
$$

This gives the $1/2$ in the source's flag-constant assertion with room to spare, simultaneously for the stated fields, ranks and flag types. For the empty type the constant is one. [Original flag constant](https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AbelianVarietyTheory/Definitions/SemilocalFrames/DefClassNum.lean#L11-L28) · [Original estimate](https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AbelianVarietyTheory/Statements/CuspFrameWeights/SameKindIsometric.lean#L104-L110)

Write $d=2f$, $v=\operatorname{rd}_E/2$, and $D_N=2nJ-2J^2-\sum_i j_i^2$ for the dimension of the unipotent radical. Put $b_k=2\pi^k/(k-1)!$, $S_r=\prod_{k=1}^r b_k$, and $R_E=\operatorname{Res}_{z=1}\zeta_E(z)$. With $\eta$ the unramified quadratic character of $E/F$, the exact coefficient is

$$
\kappa_j =
 v^{-fD_N/2}\,2^{-f(nJ-J^2+J/2)}
 \left(\frac{S_p S_q}{S_{p-J} S_{q-J}\prod_i S_{j_i}}\right)^f
 R_E^a\,
 \frac{\prod_i\prod_{\ell=2}^{j_i}\zeta_E(\ell)}
      {\prod_{h=n-2J+1}^{n} L(h,\eta^h)} .
$$

Indeed the two half-factors at conjugate split primes in the source multiply to the Euler factor over $F$, and the inert factor uses $\eta(\mathfrak p)=-1$. All factors are positive. [Euler factors and normalization of $v$](https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Formalism/HermitianLattices/StatementMass.lean#L25-L46)

The main saving comes from the $J$ factors in $S_p/S_{p-J}$. Each has $k-1\ge n-2\sqrt n\ge0.99n$, since $p=n-q$ and $s\ge200$. Integrating $\log u$ between $1$ and $k-1$ gives $(k-1)!\ge ((k-1)/e)^{k-1}$. Thus $\log b_k\le2-0.99n(L-2.16)\le-0.84nL$. Here $\log(2\pi)<2$ and $1+\log\pi-\log(0.99)<2.16$. In $S_q/S_{q-J}$ each factor has $k\le s$, giving $\log b_k\le2s$. Finally $\log(S_{j_i}^{-1})\le\sum_{k=1}^{j_i}(k-1)\log s\le j_i sL/4$. The combined logarithm of the sphere factors, divided by $fJ$, is at most $-0.84nL+2s+sL/4$.

Minkowski's ideal-class bound gives $\sqrt{|d_E|}\ge(\pi/4)^f d^d/d!$. The first $d/2$ factors in $d!$ are at most $d/2$, so $\operatorname{rd}_E\ge\pi/2>3/2$. Therefore $v^{-fD_N/2}\le\exp(0.3fnJ)$, since $D_N\le2nJ$ and $\log(4/3)<0.3$. The displayed power of $2$ is at most one. Louboutin's Theorem 1 for any number field of degree $d>1$ gives

$$
 R_E\le\left(\frac{e\log |d_E|}{2(d-1)}\right)^{d-1}.
$$

The base is at most $e\log\operatorname{rd}_E\le e^{n+1}$. Hence $\log R_E^a\le 2fJ(n+1)$, including when that logarithm is negative. [Louboutin, *Explicit bounds for residues of Dedekind zeta functions*, Theorem 1](https://www.sciencedirect.com/science/article/pii/S0022314X00925459) · [General bound restated by Louboutin, p. 171](https://smf.emath.fr/sites/default/files/2026-04/smf_sem-cong_11_171-178__sample.pdf#page=1)

The remaining Euler products satisfy $\zeta_E(\ell)\le\zeta(\ell)^{2f}$ and $1/L(h,\eta^h)\le\zeta(h)^f$ by primewise comparison. Moreover,

$$
 \sum_{h=2}^{\infty}\log\zeta(h)
 \le\sum_{r=2}^{\infty}\sum_{h=2}^{\infty}r^{-h}
 =\sum_{r=2}^{\infty}\frac1{r(r-1)}=1 .
$$

Since $a\le J$ and $J\ge1$, their total logarithmic cost is at most $3fJ$. After division by $fJ$, the positive terms left against the saving $-0.84nL$ sum to at most $2.3n+5+2s+sL/4\le0.16nL$. For the last inequality divide by $nL$ and use $L\ge15$ and $s\ge200$. This yields $\log\kappa_j\le-0.68JnfL$, which implies the asserted bound.

## How much of the flag domain can support a near term?

Assume the source's geometric flag measure inequality for the original lattice, Haar measures and measurable fundamental domain. Write $\Pr$ for its Haar measure restricted to that domain and divided by its total mass. Assume $2q+2\le n=p+q$. For a nonempty canonical isotropic flag write $j_1,\ldots,j_a\ge1$ for its successive rank jumps, $J=\sum_i j_i\le q$, and $0<\tau_1<\cdots<\tau_a<1/2$ for its sizes. The canonical filtration has a nonempty flag exactly when $m(x)<1/2$, and then its first size equals $m(x)$. The sum of its rank jumps is at most $q$ by isotropy. [First size and the empty flag](https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AbelianVarietyTheory/Proofs/FlagMeasures/CanonicalFlagExistsUniqueSemistable.lean#L289) · [Rank bound](https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AbelianVarietyTheory/Proofs/FlagMeasures/NonzeroFlagProbabilityBoundOfVolumeRatioInductio.lean#L58-L83)

Set $N=n-2J\ge2$. For any $0<t<1/2$, the flag measure inequality, with constant $\kappa_j$, implies

$$
 \Pr\{\text{flag of type }j,\ m(x)\le t\}
 \le \kappa_j\, N^{-a} \,t^{2f j_1 N}.
$$

Indeed the source's density is its product over the layers multiplied by $\prod_i 2 f j_i/\tau_i$. Keep the factors $\tau_i^{2f j_i N}$. Every discarded factor is a nonnegative power of $\tau_i/\tau_k$ for $i<k$, $\tau_i\tau_k$, or $\tau_i^2$, and is at most one. Integrate the resulting product over the larger box $(0,t]\times(0,1)^{a-1}$. Each one-dimensional integral contributes $1/N$, together with $t^{2fj_1N}$ at the first index. [Flag measure contract](https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AbelianVarietyTheory/Statements/CuspFrameWeights/SameKindIsometric.lean#L95-L102) · [Density](https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AbelianVarietyTheory/Definitions/SemilocalFrames/DefClassNum.lean#L30-L37) · [Layer powers](https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AbelianVarietyTheory/Definitions/SemilocalFrames/LayerProd.lean#L29-L38)

In the large-rank range just proved, put $X=nf\log n$. The union of the regions that can support nonidentity near terms has probability at most

$$
 t_*^{2f(n-2q)}\sum_{J=1}^{q}2^{J-1}e^{-2JX/3}.
$$

There are $2^{J-1}$ ordered compositions of $J$, and $j_1N\ge n-2q$. The inequality bounds the measure in the original automorphic quotient. The trace also weights each point by the sum of all contributing kernel terms. On the moderate range, [C83N5–6](../../../archive/rounds/v83/continuation_v83/nearflag.tex#L97-L150) already count this multiplicity and integrate it under the flag-measure inequality and the numerical bound proved above. The [integral flag classification](../geometry/RETAINED_FLAG_CLASSES.md) and the [sum of their normalized volumes](../geometry/RETAINED_FLAG_MEASURE.md) now give that measure inequality. The [projector proof](../arithmetic/RETAINED_PROJECTOR_COUNTS.md) supplies the separate far and deep estimates. [Multiplicity in a given flag](https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AbelianVarietyTheory/Proofs/FlagMeasures/NearTermsModeratePointsOneTypeBound.lean#L153-L178) · [Retained-row obligation](RETAINED_DIMENSION_COMPARISON.md)
