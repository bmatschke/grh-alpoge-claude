# Three parts of the spectral estimate on the selected family

The spectral assertion uses the full column operators $K_{uv}=A_u^*A_v$ and the full target dimension $D_{\rm all}$. Its three outputs are a mixed Hilbert–Schmidt bound, a diagonal Hilbert–Schmidt bound and a dimension bound. The dimension output now holds with the required rate. Two inputs to the mixed calculation can also be obtained directly, namely the vanishing of the zero-Gram cell and the finite-type operator norm at the marked primes. [Exact outputs and rates][goal] · [Kernel conventions and cell decomposition](actual_gram/actual_gram_section.tex#L14-L46)

## The dimension output

At the selected point use the total level idempotent $e$ of the [retained-dimension calculation](SELECTED_RETAINED_DEFECT.md). Its image has dimension $D_{\rm all}$ and its main term is the very $D^\star$ of the row. The [trace count](RETAINED_PROJECTOR_COUNTS.md) gives
$$
 \left|D_{\rm all}/D^\star-1\right|\le \eta_1,
 \qquad \eta_1=\exp(-nf\log n/16).
$$
Here $D^\star>0$, $n$ is the total rank and $f$ the real degree. In the notation of the family sizes, this total rank is $R.r$ (at least $R.k$), while $R.n$ is half the real degree. Take the selected counting range for $\varepsilon$, decreasing its upper endpoint to $1/53$ if necessary. Beyond the maximum of its count cutoff, $F.x_1+1$ and $4$, the [family size bounds][size] give $n\ge100$ and $f\ge x^2$ at every index. Consequently $nf\log n/16\ge x^{\varepsilon/8}$ for $x\ge1$. This proves the last conjunct of the spectral assertion at every index after one cutoff, even before imposing the word-size comparability premise in that assertion. The exponent here uses the endpoint's $\varepsilon$, as required. [Arithmetic-to-spectral dimension identification][dim]

## The finite Gram matrix at the two marked primes

At a split marked place let $G=\mathrm{GL}_k(\mathbb F_q)$, $U$ its upper unitriangular group, and $\xi(u)=\psi(\sum_{a<k}u_{a,a+1})$ for the given nontrivial additive character. The level sum on a free finite orbit has kernel the character $\gamma$ of $\operatorname{Ind}_U^G\xi$, with $\gamma(1)=|G|/|U|$. Indeed, extending $\xi$ by zero gives $\gamma(x)=|U|^{-1}\sum_{y\in G}\xi(yxy^{-1})$. Between two orbit indices the group element relating them is unique. The orbit matrix is therefore central convolution by this class function or its conjugate, with counting measure. [Orbit identification and Haar convention][fin]

On an irreducible complex representation of character $\theta$, convolution by $\overline\gamma/\gamma(1)$ has scalar
$$
             \frac{|U|}{\theta(1)}\dim\operatorname{Hom}_U(\xi,\theta).
$$
This follows by taking the trace of the central operator and applying Frobenius reciprocity. The Gelfand–Graev multiplicity-one theorem for $\mathrm{GL}_k(\mathbb F_q)$ makes the last dimension zero or one. It applies to the specified simple-root character at each prime. [Brundan–Dipper–Kleshchev, Theorem 2.5d(ii)][gg]

Here the dimension in the denominator matters. On a summand containing a $\xi$-vector, restrict first to the last-column additive subgroup $\mathbb F_q^{k-1}$. The vector lies in a nontrivial character space there. All $q^{k-1}-1$ nontrivial characters are conjugate under $\mathrm{GL}_{k-1}$, so their spaces have equal dimension. Within the chosen space the stabilizer contains the mirabolic subgroup at rank $k-1$, and the same vector has the prescribed character on its upper unitriangular subgroup. Repeat with the last column of that mirabolic: the embedded $\mathrm{GL}_{k-2}$ permutes all its nontrivial characters transitively. Induction gives $\theta(1)\ge\prod_{a=1}^{k-1}(q^a-1)$. Since $|U|=q^{k(k-1)/2}$, every normalized eigenvalue lies between zero and
$$
 \prod_{a=1}^{k-1}(1-q^{-a})^{-1}
 \le (1-1/(q-1))^{-1}\le 1+3/q\qquad(q\ge3).
$$
The first inequality uses $\prod(1-t_a)\ge1-\sum t_a$. Conjugating the kernel permutes the irreducibles. Rank one gives the empty product. [The mirabolic dimension bound in the source][mir]

Write $\Gamma_1$ for the product of the identity values at the $2f$ marked places. The finite Gram matrix divided by $\Gamma_1$ is a direct sum of tensor products of the normalized orbit operators. Thus $0\preceq G_{\rm fin}\preceq P_g\Gamma_1 I$, where $P_g=(1+3/g_0)^f(1+3/g_1)^f$. For a finite set of orbital terms, sum the orbital vectors of terms with the same finite index to obtain $w_i$. Expanding the squared Hilbert–Schmidt norm pairs $G_{\rm fin}$ with their Gram matrix. Applying the operator bound one coordinate at a time gives
$$
        \|\operatorname{part}\|_{\rm HS}^2
               \le P_g\Gamma_1\sum_i\|w_i\|^2.
$$
Exhaust an absolutely summable cell by finite sets to obtain the same inequality for the whole cell. This retains the inner products between terms of the same row, where the remaining arithmetic estimates are needed. [Finite and limiting inequalities][cell]

## Why unequal words have no zero-Gram term

Use the normalized geometric expansion on the tied selected model. The gap range and the reproducing section supply the integrability used in folding the two Poincaré series. Their absolute majorants are square-integrable and their product is integrable by Cauchy–Schwarz. The ensuing double-coset integral is covariant under the intersection of the two stabilizers, by invariance of the quotient measure. If their unipotent characters disagree on the common character subgroup, translating by an element on which they disagree multiplies the integral by a nontrivial scalar, giving zero. The identity cell itself vanishes for distinct words by its type pairing. [Absolute unfolding](period_gram_v57/main.tex#L760-L843) · [Selected admissibility](continuation_v89/comparison.tex#L3-L28) · [Covariance and the identity cell][schur]

Here is a way to see the common compact group on a relevant zero-Gram cell. Work at a real place in the complex Hermitian space of signature $(r+k,r+1)$, where $r$ here is the isotropic flag length. Let $X,X'$ be the two isotropic $r$-planes and $z,z'$ their respective negative final vectors. Put $I=X\cap X'$ and $j=r-\dim I$. The local zero-Gram normal form gives $X=X_j\oplus I$ and $X'=X'_j\oplus I$ with $X_j,X'_j$ in nondegenerate duality. The final vectors are proportional modulo $X+X'$ with a nonzero factor. This last statement allows different final norms. In the transverse case, write $p_r$ and $p_{r+1}$ for the determinants of the cross pairings of the isotropic and full frames. Write $-T_u,-T_v$ for the negative norms. Zero Gram gives $|p_{r+1}|^2=T_uT_v|p_r|^2$. If both determinants vanished, there would be $0\ne y\in X$ perpendicular to $X'$ and $0\ne y'+\beta z'\in X'+\mathbb C z'$ perpendicular to $X+\mathbb C z$. Positivity of the two frame perpendiculars modulo their isotropic parts, together with $X\cap X'=0$, gives $\langle y,z'\rangle\ne0$ and $\beta\ne0$. This contradicts $y\perp y'+\beta z'$. Thus $p_r\ne0$. Subtracting vectors in $X,X'$ projects the two negatives onto $(X+X')^\perp$ with their norms unchanged. Their mutual pairing is the Schur complement $p_{r+1}/p_r$ up to conjugation. The two projected vectors have zero Gram determinant in a space with one negative direction, so they are proportional. In the intersecting case equality of the two flag characters propagates the leading coefficient of a common isotropic vector through the flags to the final vectors. [Normal-form argument][nf] · [Normal form with both word norms][two] · [Compact actions on the actual representatives][native]

Let $W=X+X'+\mathbb C z+\mathbb C z'$. The sum $X_j+X'_j$ is hyperbolic of dimension $2j$. Removing the projection of $z$ onto this sum subtracts an element of $X_j$, since $z\perp X_j$. Its new norm is still negative. The space $W$ is consequently the orthogonal sum of that hyperbolic space, the new negative line and the radical $I$. Thus $W^\perp/I$ is positive definite of dimension $k$. Choose a linear complement $D$ of $I$ in $W^\perp$. Projection identifies $D$ isometrically with **each** of the spaces
$$
 (X+\mathbb C z)^\perp/X,\qquad (X'+\mathbb C z')^\perp/X'.
$$
Indeed both have dimension $k$, and the kernel on $D$ is zero by positive definiteness. A unitary of $D$, extended by the identity on $D^\perp$, now fixes both labelled frames pointwise. Its simple-root displacement coefficients vanish in both Bessel characters. On the two definite factors it acts by the same element of $U(k)$ in two orthonormal bases. Their actions therefore differ by a fixed inner conjugation.

The selected word-separation hypothesis gives different highest weights at each real place for two distinct binary words. [Exact hypothesis and its use][sep] After undoing the inner conjugation, every matrix entry in the other real factors is an intertwiner between two inequivalent irreducible compact types. Schur's lemma gives zero. This proves termwise vanishing, including cells with $I=0$ or $I=X$. Absolute unfolding permits summing the terms. In particular only the generic and nongeneric **nonzero** Gram cells remain in the mixed estimate. For equal words the [singular remainder estimate](SPECTRAL_DIAGONAL_ZERO_CELL.md) uses a fixed-label local tail and weighted count of frame classes. The signed nonzero-Gram sums still require bounds. [Highest-weight argument in the pinned proof][last] · [Quantitative targets](actual_gram/actual_gram_section.tex)

## A comparison available for the surviving sums

The [primitive density calculation](SPECTRAL_SCALAR_DENSITIES.md) evaluates the normalized finite factor for represented generic joint frames, including the divided differences at the auxiliary primes. The dyadic ratios are at most one, and the marked last vector bounds the inert residual corank. The global signed same-row sum also requires the scalar-partner identities and archimedean energy estimate.

For the distinct-word contribution the Roadmap gives a more specific starting point than an estimate for an arbitrary matrix coefficient. B8.10hbe(c) expresses the terminal kernel as a finite Gram sum over the actual lifts, compact type projections and word multipliers. Multiplying each vector by the square root of its weight preserves positivity in a weighted diagonal term. In a mixed term the relative phases of the two vectors enter their inner product. The preceding marked-prime bound controls the finite orbit index and leaves these inner products to be estimated. B8.10hbe(b) treats them by a mixed Cauchy–Schwarz contraction on residual slices, and B8.10e applies that contraction to a differing bit of the two words. Checking the realization of those residual forms and the passage from compact cutoffs to the orbital sum is a specific route to the surviving estimate. The Roadmap lists both lemmas, and its signed corank-one bounds, among its outlined proofs. [Terminal Gram representation and mixed contraction](https://github.com/rh-lean-roadmap/rh-lean-roadmap/blob/94e6a98b4e74932a0298d6bd22d44cf60c62764b/docs/src/book/main.tex#L17553-L17600) · [Application to distinct words](https://github.com/rh-lean-roadmap/rh-lean-roadmap/blob/94e6a98b4e74932a0298d6bd22d44cf60c62764b/docs/src/book/main.tex#L18082-L18099) · [Proof status and original declarations](https://github.com/rh-lean-roadmap/rh-lean-roadmap/blob/94e6a98b4e74932a0298d6bd22d44cf60c62764b/docs/outline-proofs.md#L11-L23)

[goal]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Formalism/SharpRestriction/GlobalTheoremInputs.lean#L142-L157
[size]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AbelianVarietyTheory/Proofs/GlobalInterpolation/LinkIRROfJoinEx.lean#L39-L137
[dim]: https://github.com/rh-lean-roadmap/rh-lean-roadmap/blob/94e6a98b4e74932a0298d6bd22d44cf60c62764b/docs/src/book/main.tex#L35806-L35815
[fin]: https://github.com/rh-lean-roadmap/rh-lean-roadmap/blob/94e6a98b4e74932a0298d6bd22d44cf60c62764b/docs/src/book/main.tex#L46494-L46509
[gg]: https://pages.uoregon.edu/brundan/papers/gl.pdf
[mir]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Formalism/PeriodIntegrals/UnitaryGroupMassFormula/MirabolicBound/Development.lean#L112-L127
[cell]: https://github.com/rh-lean-roadmap/rh-lean-roadmap/blob/94e6a98b4e74932a0298d6bd22d44cf60c62764b/docs/src/book/main.tex#L46511-L46523
[schur]: https://github.com/rh-lean-roadmap/rh-lean-roadmap/blob/94e6a98b4e74932a0298d6bd22d44cf60c62764b/docs/src/book/main.tex#L46526-L46551
[nf]: https://github.com/rh-lean-roadmap/rh-lean-roadmap/blob/94e6a98b4e74932a0298d6bd22d44cf60c62764b/docs/src/book/main.tex#L41439-L41456
[two]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Formalism/LocalToGlobal/SiegelLatticeTheory/CokernelGLCounts/RankPointCounts/CplxNF.lean#L17-L32
[sep]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Formalism/LocalToGlobal/SiegelLatticeTheory/CokernelGLCounts/RankPointCounts/KappaOffDiagonal.lean#L47-L62
[native]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Formalism/LocalToGlobal/SiegelLatticeTheory/CokernelGLCounts/RankPointCounts/SubOneMulVecFix.lean#L207-L505
[last]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Formalism/LocalToGlobal/SiegelLatticeTheory/CokernelGLCounts/RankPointCounts/SchurNFCOf.lean#L20-L36
