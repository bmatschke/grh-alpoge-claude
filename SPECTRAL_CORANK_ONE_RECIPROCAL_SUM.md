# A reciprocal-weight bound for represented corank-one block points

Let $E/F$ be the CM extension of the tied rows, $f=[F:\mathbf Q]$, $r=r_S\ge1$, $n=r+1$, and $I=\mathfrak d_{F/\mathbf Q}\mathcal O_E$. In this family $N_E I=\rho^{2f}$, where $\rho=\operatorname{rd}(E)$. Put $g=g_0g_1$ and $K=N_E(I^{r(r+1)})$. For a represented nonsingular point $\gamma$, write $D_j$ for its unscaled signed leading $j$-row minor and $B(\gamma)$ for its block ends. The point weight is
$$
 w(\gamma)=\prod_{\tau:E\hookrightarrow\mathbf C\,/\,\mathrm{conj}}
 \prod_{j\in B(\gamma)}(1+|\tau D_j|^2)^2 .
$$
Use one embedding from each complex conjugate pair. For each **fixed partner class** $c$, sum over its distinct attained pairs of a block point and a reduced normal label. On the positive nonsingular corank-one rows with the normal-coordinate separation in the [normal-label count](SPECTRAL_CORANK_NORMAL_LABELS.md), for every fixed $0<\eta<1$,
$$
 \sum_{(\gamma,\nu)\text{ attained for }c}\frac1{w(\gamma)}
 \le \left(\frac{C_\eta}{1-\eta}\right)^f
 \frac{(9^f+2)^n}{g^{2rf+2nf\eta}K^{1+\eta}}.                    \tag{1}
$$
The constant $C_\eta$ depends only on $\eta$. For distinct represented **points alone**, the upper bound is $(9^f+2)^n/(g^{2rf}K)$, without a normal-coordinate hypothesis. [Point weight][w] · [Root-discriminant normalization][root]

## Minor ideals from the two flags

Each flag vector of index $a=0,\ldots,r$ belongs to $I^{r-a}\Lambda$, since its multiple by every element of $I^{-(r-a)}$ is integral. Both flags have this property. Each term of the leading determinant consequently belongs to $I^{2\sum_{a<j}(r-a)}$. At each prime above $g$, every primed vector is congruent modulo $g\Lambda$ to a combination of the first flag. Its first $r$ vectors pair to zero with the entire first flag, terminal vector included. Thus all entries of the first $r$ cross-Gram rows belong locally to $g\mathcal O_E$. Every term of the determinant has at least $\min(j,r)$ such entries. The two level primes split completely in $E$, so $g$ is coprime to $I$. The triangular operations taking the raw pair to its block form preserve leading determinants, with only unit signs in the signed convention. This proves
$$
 D_j\in\mathfrak J_j=(g)^{\min(j,r)}I^{j(2r+1-j)},\qquad
 N_E\mathfrak J_n=g^{2rf}K.                               \tag{2}
$$
[Integral flags][flags] · [Cross-Gram and null vectors][null] · [Level condition][level] · [Leading minors][minor] · [Signs][sign]

## Counting in fractional ideals

For every nonzero fractional ideal $J\subset E$ and $\alpha>1$,
$$
 \sum_{0\ne x\in J}\prod_\tau(1+|\tau x|^2)^{-\alpha}
 \le \frac1{N_E J}\left(\frac9{\alpha-1}\right)^f .       \tag{3}
$$
Indeed, write $d=\sqrt{N_EJ}$. Distinct points $x,y\in J$ satisfy $\prod_\tau|\tau(x-y)|\ge d$ by the inclusion $(x-y)\subset J$. A polydisk with radii $R_\tau>0$ and center zero contains no nonzero point if $u=\prod R_\tau<d$. For $u\ge d$, dilate each complex coordinate by $u^{1/f}/R_\tau$. The product of these positive factors is one, so distinct transformed points have sup distance at least $d^{1/f}$. Disjoint open polydisks of radius $d^{1/f}/2$ around the transformed points fit inside the polydisk of radius $u^{1/f}+d^{1/f}/2$. Volume comparison bounds the count by $(1+2(u/d)^{1/f})^{2f}\le 9^f u^2/N_EJ$. Now integrate the count against the product of the positive measures $2\alpha R(1+R^2)^{-\alpha-1}\,dR$. Each measure has tail $(1+y^2)^{-\alpha}$ at $y$ and second moment $1/(\alpha-1)$. Tonelli gives (3), uniformly in the aspect ratios of the polydisks and the unit group. [Norm separation][norm]

## Removing the marked level from the normal-label divisor count

Use the raw cross-Gram convention $Z_{ab}=h(f'_b,f_a)$ with $h$ linear in its first slot. Put $s=r(r+1)$, let $X$ be the isotropic subspace of the fixed first flag, and write
$$
 c_b=\operatorname{adj}(Z)_{b,r},\qquad
 y=T\sum_b c_b f'_b+\det(Z)z.
$$
At the primes above $g$, every $c_b$ is divisible by $g^r$, since it is a minor of the first $r$ rows. Write $f'_b=\sum_a f_a\xi_{ab}+g v_b$ locally. The last cross-Gram row satisfies $Z_{rb}\equiv -T\xi_{rb}\pmod g$, since $h(z,z)=-T$ and $z$ is perpendicular to $X$. Laplace expansion along this row gives
$$
 \det(Z)+T\sum_b c_b\xi_{rb}\equiv0\pmod {g^{r+1}}.
$$
Thus $y=e+g^{r+1}v$ with $e\in X$ and $v$ integral locally. The same calculation applies after interchanging the flags, using the inverse of the unitriangular congruence matrix and transporting back to the second fixed lattice. In each partner class the first-side normals are perpendicular to the same $X$, and the second-side normals to its fixed primed counterpart. Therefore a pairing of two first-side normals equals the pairing of their differences with their respective $e$'s, since $X$ is totally isotropic. It is divisible by $g^{2n}$ locally. For split conjugate primes this computation uses the two local components together. The second-side pairings satisfy the same divisibility. At primes away from $g$, both normals retain the standard inclusion $y\in I^s\Lambda$ on their respective sides. [Cofactor normal and orthogonality][cof] · [Normal weights and paired coordinates](SPECTRAL_CORANK_NORMAL_LABELS.md)

Consequently the normal-label divisor argument applies with the smaller ideal
$$
 A_*=(G)\mathfrak d_{F/\mathbf Q}^{-2s}(g)^{-2n}.
$$
Indeed $h(y_0,y_0)=TG$ and $T$ is a unit above $g$, hence $A_*$ is integral there. Elsewhere this is the original integral Gram ideal. For a norm-one comparison coordinate $x$ we have $h(y_t,y_0)=x TG$ in this convention, and both $xTG$ and its conjugate have the same indicated ideal divisibility. Thus the valuation interval for $x$ at each split prime uses $(T)A_*$. The second side uses $(T')A_*$. The same divisor and torsion estimate gives $M(c,\gamma)\le C_\eta^f(N_FA_*)^\eta$ under the stated separation hypothesis. [Word levels][words] · [Normal comparison, norms, and divisor estimate](SPECTRAL_CORANK_NORMAL_LABELS.md)

## Summation with normal labels

Write $G=D_n\bar D_n-TT'D_r\bar D_r$. Since $TT'>0$ and the represented nonsingular Gram norm is positive at each place in this case, $0<\tau G\le |\tau D_n|^2$. Thus the normalized Gram norm satisfies $\widehat N_G=|N_F G|/K\le |N_E D_n|/K$. The preceding count costs at most $C_\eta^f(|N_ED_n|/(g^{2nf}K))^\eta$ labels for this class and point.

Fix a block composition $s_1+\cdots+s_l=n$, with ends $j_1,\ldots,j_l=n$. The list of *nonzero* end minors identifies at most $\prod_i s_i$ rational block points. Indeed, successive ratios give the $s_i$-th powers of the block parameters up to their prescribed signs. Each polynomial has at most $s_i$ roots in $E$. Sum independently over $D_{j_i}\in\mathfrak J_{j_i}\setminus\{0\}$, which enlarges the sum. For the terminal minor absorb $|N_E D_n|^\eta$ using $|z|^{2\eta}\le(1+|z|^2)^\eta$ in each embedding. Apply (3) with $\alpha=2-\eta$ there and with $\alpha=2$ elsewhere. Keep $1/N_E\mathfrak J_n$ and bound the other reciprocal ideal norms by one using (2). For $h=9^f$ the sum of $h^l\prod_i s_i$ over all compositions of $n$ is at most $(h+2)^n$. Its generating series is $1/(1-hz/(1-z)^2)$, its first positive-degree coefficients are $h,h(h+2)$, and subsequently $A_n=(h+2)A_{n-1}-A_{n-2}$. This gives (1). Taking the same argument with no labels or terminal norm power proves the point-only assertion. [Block-parameter fibers][fiber] · [Norm-one label count](SPECTRAL_CORANK_NORMAL_LABELS.md)

For the [actual signed class subtotals](SPECTRAL_SIGNED_CORANK_ONE_FIBRE.md) $V_{c,\gamma,\nu}$, weighted Cauchy–Schwarz followed by summation over $c$ now gives
$$
 \sum_c\Big\|\sum_{\gamma,\nu}V_{c,\gamma,\nu}\Big\|^2
 \le R_\eta\sum_\gamma w(\gamma)\sum_{c,\nu}\|V_{c,\gamma,\nu}\|^2 ,
$$
where $R_\eta$ is the right side of (1). This holds for finite subfamilies and then whenever the right side is finite. It puts the label multiplicity entirely in the reciprocal sum and introduces no factor counting partner classes. The remaining energy still involves the real squared orbital integrals and the generic mass at each represented point.

[w]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Formalism/SharpRestriction/CuspSpanNormBounds/BesselShellMomentBounds.lean#L235-L261
[root]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Formalism/LocalToGlobal/SiegelLatticeTheory/CokernelGLCounts/RankPointCounts/DualFamilyCounting/EmbVHomInjective.lean#L32-L45
[flags]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Formalism/LocalToGlobal/SiegelLatticeTheory/CokernelGLCounts/RankPointCounts/StepNormOneOfLeaves.lean#L112-L149
[null]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Formalism/SharpRestriction/CuspSpanNormBounds/BlockEnds.lean#L26-L63
[level]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Formalism/SharpRestriction/CuspSpanNormBounds/IsPrimitiveSub.lean#L136-L148
[minor]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Formalism/SharpRestriction/CuspSpanNormBounds/CayleyDegreeNondegeneracy/RowsTrm.lean#L143-L156
[sign]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Formalism/SharpRestriction/CuspSpanNormBounds/FlagEEqHyperbolic.lean#L14-L16
[norm]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Formalism/FlagUnipotentLattices/MinkowskiFactorialBounds/BlockMinorSumCounterexample.lean#L394-L402
[fiber]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Formalism/FlagUnipotentLattices/MinkowskiFactorialBounds/BlockMinorSumCounterexample.lean#L538-L550
[cof]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Formalism/LocalToGlobal/SiegelLatticeTheory/CokernelGLCounts/RankPointCounts/PairingOmegaPrimeZ.lean#L54-L122
[words]: https://github.com/rh-lean-roadmap/rh-lean-roadmap/blob/94e6a98b4e74932a0298d6bd22d44cf60c62764b/docs/src/book/main.tex#L6318-L6325
