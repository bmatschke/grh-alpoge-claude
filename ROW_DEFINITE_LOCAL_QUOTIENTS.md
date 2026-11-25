# The common local quotient at a definite square

Let $a>a'$ be the two intermediate ranks and $d=a+a'$ the even target rank. Fix a realized triple with $p=q=0$, its two Weil representations and its splitting characters $\beta,\alpha$. We describe why the two local projections used for [descent of the definite integrals](ROW_DEFINITE_THETA_COMPARISON.md) have the same target. The assertion involves their normalization on actual vectors. At a marked finite place it specifies exactly which pairs of Schwartz functions have equal image. At an unmarked place it specifies a common nonzero vacuum. The local inputs in the argument are the compact Fock decomposition, the split zeta transforms and the integral lattice model at inert places. We record the relevant comparisons in their normalizations below. [Triple and characters][triple] · [Projection and normalization conditions][match]

## The two determinant shifts at a real place

Put $\kappa=m_\alpha-m_\beta$ at this place. The weight gap and the parity in the splitting characters make $N=(\kappa-d)/2$ a positive integer. The target is $U(d)$, the big source has signature $(a,0)$ and the small source $(0,a')$. In the polynomial oscillator for the big side, the untwisted source action includes the scalar differential $d/2$. To obtain the prescribed source weight $\kappa/2$ in every coordinate one needs the determinant polynomial type $\det^N$ of $U(a)$. In the Cauchy decomposition of polynomials on $a$ by $d$ matrices this is the rectangular partition with $a$ rows of length $N$. It occurs once paired with the same partition of $U(d)$ padded with $a'$ zeroes. For instance the $N$th power of a maximal minor is a nonzero vector of this type. With the oscillator half shift, the target highest weight is
$$
 \lambda_b=((N+a/2)^{[a]},(a/2)^{[a']}).
$$
An exponent in brackets denotes the number of repetitions. On the small side the negative polarization gives the dual rectangular type, padded on the left, and the oscillator half shift is $-a'/2$. The weight is
$$
 \lambda_s=((-a'/2)^{[a]},(-N-a'/2)^{[a']}).
$$
The actual Weil splittings add $m_\beta/2$ and $m_\alpha/2$, respectively, to all target coordinates. Since $N+d/2=\kappa/2$, **the actual target highest weights coincide**. Averaging over each compact source projects onto its trivial type for its actual splitting, and the compact target module in that component is the single irreducible just calculated. The common weight identifies the modules; composing the two projections with that identification gives the two onto maps. Tensor these maps over the real places. Any common change of target basis preserves equality of images. [Fock weights and exponents][weights] · [Equality of the shifted weights][shift] · [Nonzero simple quotients][real] · [Translation to the actual Weil actions][realact]

## Split finite places

Put $k=F_v$, $q=\#k(v)$, and use the chosen split branch. Both targets can be realized on functions on $\mathrm{GL}_d(k)$. For a block upper triangular $p$ with invertible diagonal blocks $A,D$ of sizes $a,a'$, the transformation rule is
$$
 f(ph)=\alpha(\det A)\beta(\det D)
        |\det A|^{a'/2}|\det D|^{-a/2}f(h).
$$
Together with smoothness this is the normalized parabolic induction of the two unitary determinant characters. It is irreducible by unitary induction for the general linear group; the pinned proof uses the narrower two-character consequence of the geometric lemma. [Induced-function model][split] · [Tadić, Theorem A](https://www.numdam.org/item/10.24033/asens.1510.pdf) · [Precise irreducibility input][irr]

At a marked place use the prescribed big determinant-shell transform and the small full-frame integral. Changing the frame by the intermediate group cancels its Weil multiplier against the determinant weight in the transform. Acting by a target element right translates the output function. Changing the two column blocks by $p$ gives the displayed rule. These statements use the big and barred small polarizations, with their prescribed Haar factors. The [explicit complementary-frame tests](ROW_MATCHED_SQUARE_TESTS.md#an-explicit-split-place-comparison) give value one at the identity in both models. Each image is therefore a nonzero invariant subspace of the displayed induction and hence is the whole induction. Taking the transforms themselves as the projections makes equality of images exactly the marked zeta matching condition. [Matrix transforms][matrix] · [Transport, invariance and surjectivity][ram]

At an unmarked split place the relative character $\nu=\alpha/\beta$ is unramified. Use the normalized determinant-shell transform. On $r$ rows its normalizing polynomial is
$$
 P_r(X)=\prod_{j=0}^{r-1}(1-\nu(\varpi)q^{j-d/2}X).
$$
For the big transform the multiplication is performed on the determinant-valuation series **before** evaluation at one. This convention includes a possible zero factor at one. On the small side evaluation multiplies its convergent integral by $P_{a'}(1)\ne0$. For the integral square-matrix test the determinant-valuation series is $P_r(X)^{-1}$ with the maximal compact group of measure one. Indeed integral invertible matrices modulo right integral changes of basis parameterize finite-index sublattices; triangular lattice bases give one geometric series per diagonal pivot, with $q^j$ choices per additional unit of valuation at that pivot. Restriction of both normalized spherical vectors to the maximal compact is thus the constant one. Iwasawa decomposition and the common parabolic law give equality everywhere. Each map is again onto by irreducibility. The local dictionary transports the vacuum to the standard test in the specified charts. [Normalized transforms][norm] · [Vacuum calculation and Iwasawa comparison][unram]

## The inert spherical functions

At a nonsplit place of this triple the quadratic local extension is unramified, the residue characteristic is odd, the additive character has conductor zero and the lattices are self-dual in the prescribed model. All marked places are split. Put $d=2m$, $G=U(W)(F_v)$ and $K$ equal to the target lattice stabilizer. The local target contains a maximal isotropic space of rank $m$ with an integral Witt decomposition. Let $P$ be its stabilizer, with Levi $\mathrm{GL}_m(E_w)$. Write $z=\det A$ for its Levi determinant and $R=|N_{E_w/F_v}z|_v$. [Local hypotheses][triple] · [Isotropic coordinates and evaluation of the vacuum][evaluation]

In the Schrödinger polarization for this isotropic space let $\ell_{0,b}$ and $\ell_{0,s}$ be evaluation at zero, transported to the two given models and normalized to one on their lattice vacua. The unipotent radical acts by a quadratic phase equal to one at zero. The Levi change of variables and its Weil splitting give the factors
$$
        \lambda_b(p)=\beta_w(z) R^{a/2},\qquad
        \lambda_s(p)=\alpha_w(z) R^{a'/2}.
$$
Both evaluations are source invariant. At this inert place $\alpha_w,\beta_w$ are unramified and their restrictions to $F_v^\times$ are the quadratic character to the powers $a',a$. These powers have the same parity. A uniformizer of $F_v$ is also one of $E_w$, so $\alpha_w=\beta_w$, with values in $\{\pm1\}$. This gives the source invariance for the relative character and $\alpha_w\beta_w=1$. The product $\lambda_b\lambda_s=R^m$ is the parabolic modulus $\delta_P$. Indeed conjugation on the space of Hermitian matrices in its radical takes $X$ to $AXA^*$, whose determinant in absolute value over $F_v$ is $R^m$. [Character calculation][char] · [Transport of the evaluation functional][sieg] · [Normalized determinant and index calculation][mod]

For $j=b,s$, set $f_j(h)=\ell_{0,j}(\omega_j(1,h)\operatorname{vac}_j)$. It has left transformation $\lambda_j$, is right $K$-invariant and takes value one on $K$. Its left $K$-average $\Omega_j(h)$ is the normalized spherical coefficient. We verify equality of these two coefficients on the full target. The two induced-function spaces with left transformations $\lambda_b,\lambda_s$ have invariant bilinear pairing
$$
                 [u,v]=\int_K u(k)v(k)\,dk,\qquad \operatorname{vol}(K)=1.
$$
Indeed $uv$ transforms on the left by $\delta_P$, so integration over $K$ gives right-invariant integration of this density on $P\backslash G$ by the Iwasawa formula. Right translating the first argument by $h$ and the second by $h^{-1}$ in the two expressions for the same pairing yields $\Omega_b(h)=\Omega_s(h^{-1})$. The Cartan double coset $Kh^{-1}K$ equals $KhK$: the Weyl element interchanging the two integral isotropic frames reverses the Cartan parameter. Hence $\Omega_b=\Omega_s$. This equality uses the complementary ranks and both splittings. The compact invariance of the two vacua alone would only give two spherical coefficients. [Source computation by finite double-coset indices][mod] · [Inversion of the Cartan coset][cartan]

For clarity, the common coefficient determines the quotient as follows. Put $\ell_j(\phi)=\int_K\ell_{0,j}(\omega_j(1,k)\phi)\,dk$ and send $\phi$ to the function $h\mapsto\ell_j(\omega_j(1,h)\phi)$. It kills differences under the source group and is target equivariant. The local lattice-model generation theorem says that modulo those differences every vector is generated by target translates of the vacuum, and target compact averaging has image in the vacuum line. The first assertion follows by source compact averaging and generation of source-compact invariants by target translates. For the second, target-compact invariants are generated by source translates of the vacuum, which all have the same class. The precise lattice theorem for the given inert model is linked below. The images of both maps are consequently the span of the right translates of the same $\Omega=\Omega_b=\Omega_s$. This span is irreducible. If $f$ is a nonzero function in an invariant subspace, translate it so $f(1)\ne0$. Its normalized right $K$-average is a multiple of $\Omega$ by the vacuum-line assertion. Its value at one is still $f(1)$ by left $K$-invariance. It follows that the subspace contains $\Omega$, hence all its translates. Also $\Omega(1)=1$. This proves the two projection, irreducibility and common nonzero vacuum requirements in this case. [Lattice-model invariance and generation][latgen] · [Passage to the common function space][inert]

Taking the finite projections place by place and adjoining the real polynomial quotient gives the matching data for this definite triple on these local theorems. They can be chosen before comparing the global integrals. Absolute convergence, reverse constancy, and the doubled norm identity are the subsequent global steps. [Local assembly][assembly] · [Global comparison](ROW_DEFINITE_THETA_COMPARISON.md)

[triple]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AbelianVarietyTheory/BlockTheory/DivisorBase/WeilTensorModels.lean#L350-L393
[match]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AbelianVarietyTheory/BlockTheory/DivisorBase/WeilTensorModels.lean#L433-L470
[weights]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/WeilBound/CoreStatements/GaussianSeminormBounds/RealSeminormFiltration/CoreDefs.lean#L139-L149
[shift]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/WeilBound/CoreStatements/GaussianSeminormBounds/RealSeminormFiltration/CoreComb.lean#L342-L369
[real]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/WeilBound/CoreStatements/GaussianSeminormBounds/RealSeminormFiltration/CoreLM.lean#L14-L28
[realact]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/WeilBound/CoreStatements/GaussianSeminormBounds/RealSeminormFiltration/KRealAsm.lean#L325-L351
[split]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/WeilBound/CoreStatements/CompactAveragingSplitting/EigenvectorLifting/SplitLoc.lean#L20-L32
[irr]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/WeilBound/CoreStatements/TemperedRepresentationTheory/BernsteinNarrowness/RamifiedMultiplicityOneOfGeometricFiltration.lean#L15-L36
[matrix]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AbelianVarietyTheory/Definitions/Divisors/RankEqCardIffExistsFrameMatrixFirstColumnBlock.lean#L701-L723
[ram]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AutomorphicSpectrum/Proofs/BlockDecomposition/IsSmoothCharOfCondLE.lean#L110-L178
[norm]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/WeilBound/CoreStatements/CompactAveragingSplitting/EigenvectorLifting/SplitLoc.lean#L45-L67
[unram]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AutomorphicSpectrum/Proofs/BlockDecomposition/FinSplitOfNarrow.lean#L161-L191
[evaluation]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/WeilBound/ThetaLifts/SphericalLattices/FunAsm.lean#L113-L139
[char]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/WeilBound/ThetaLifts/SphericalLattices/FunChar.lean#L15-L32
[sieg]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/WeilBound/ThetaLifts/SphericalLattices/FunSieg.lean#L30-L62
[mod]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/WeilBound/ThetaLifts/SphericalLattices/FunAsm.lean#L143-L190
[cartan]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/WeilBound/ThetaLifts/SphericalLattices/InvMemKgKCart2.lean#L98-L130
[latgen]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/WeilBound/ThetaLifts/SphericalLattices/HoweDuality.lean#L13-L28
[inert]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/WeilBound/ThetaLifts/SphericalLattices/FinInert.lean#L94-L151
[assembly]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AbelianVarietyTheory/Definitions/Divisors/MatchingOfParts.lean#L28-L44

## Full-rank representatives at the prescribed split place

Let $v=v_1$, $k=F_v$, $n=a'$, $d=a+a'$, $Q=|\mathcal O_k/\varpi|$. Fix a barred Schrödinger chart with identity frames for the specified embedding $\tau_1$. It identifies local Schwartz spaces. The split oscillator formula sends $A\in\mathrm{GL}_n(k)$ to a genuine source translate acting by
$$
 f(Y)\longmapsto \nu(\det A)|\det A|^{d/2} f(AY)
$$
(the group element in the source convention is $A^t$). The chart's scalar, if changed, multiplies every test by the same nonzero number. The character $\nu$ is unitary. Write $p$ for the primed quotient transported through this chart. Since $p$ is invariant under every source translate, for each $A$ of determinant $\varpi^{-1}$,
$$
 p(f(A\cdot))=\nu(\varpi)Q^{-d/2}p(f).
$$
[Split comparison for arbitrary identity-frame charts][d1] · [Schwartz-space equivariance and unitary characters][d2] · [Source augmentation invariance][d3]

Every local Schwartz function is a finite linear combination of indicators of balls $C=Y_0+\varpi^l M_{n,d}(\mathcal O_k)$. Apply integral invertible row and column operations to put $Y_0$ in Smith normal form, clearing a common denominator first. Let $k_1\le\cdots\le k_r<l$ be the valuations of those diagonal entries visible modulo $\varpi^l$. Rescale their rows by $\varpi^{-k_j}$, and the other rows by $\varpi^{-l}$. In the resulting coordinates $Z=PYV$, the first $r$ rows of the ball belong to $e_j+\varpi^{l-k_j}\mathcal O_k^d$ and the remaining rows run independently through $\mathcal O_k^d$. The first $r$ residues are therefore linearly independent. Write $C_*$ for this normalized ball.

For $r\le i\le n$, let $f_i=1_{C_*}$ times the indicator that the first $i$ rows have independent residues. Thus $f_r=1_{C_*}$. For $c$ in the residue space of dimension $i$, choose integral lifts $\widetilde c_j$. Let $A_c$ replace row $i+1$ by
$$
 \varpi^{-1}\left(Z_{i+1}+\sum_{j=1}^i \widetilde c_j Z_j\right),
$$
keeping the other rows fixed. On the first $i$ independent residues, there is exactly one such $c$ making this row integral when $Z_{i+1}$ has dependent residue, and none when its residue is independent. A nonintegral row $Z_{i+1}$ never becomes integral under this test. All conditions on the remaining rows are unchanged. Thus as functions on *all* matrices,
$$
 f_{i+1}=f_i-\sum_c f_i(A_c\cdot).
$$
Pull this identity back via $Z=PYV$. The row matrices on $Y$ become $P^{-1}A_cP$, all of determinant $\varpi^{-1}$. The column operation commutes with row operations. Each step therefore multiplies the quotient class by $1-\nu(\varpi)Q^{i-d/2}$. The final $f_n(PYV)$ is a Schwartz function supported on full-row-rank matrices, with class equal to
$$
 \left(\prod_{i=r}^{n-1}(1-\nu(\varpi)Q^{i-d/2})\right)p(1_C).
$$
Each factor is nonzero because $i\le n-1<d/2$ and $|\nu(\varpi)|=1$. Divide by this product, then sum over the original balls. This gives a full-rank representative of every local class. It applies to the designated place even when its lattice vacuum has not been identified in the barred chart. The construction specializes for the centered unit ball to the primitive-frame sieve and its exact degree. [Row indicator computation][d4] · [Degree and splitting scalar][d5]

In particular, for each pure summand of a big polynomial test, enlarge its finite support to contain $X.T$ and $v_1$. At $v_1$ use the full-rank representative just proved. At the other finitely many places use the small quotient's surjectivity, and at infinity its surjectivity on the polynomial subspace. Use the fixed primed vacuum elsewhere. Outside the support the two vacuum images agree. Adding the resulting tensors gives a matched small test in $\mathrm{So}$. Conversely, lift each pure small test at the finite support and infinity by the unprimed quotient's surjectivity. For the last clause of $\mathrm{MatchEx}$, a polynomial match already gives the two polynomial decompositions; factor the global finite tests from each pure summand and take constant sequences of real polynomials. Every approximating primed tensor is the original tensor in $\mathrm{So}$. This proves all three clauses for given matching maps. [Polynomial matching and sequences][d6] · [Distinguished place and full-rank support][d7] · [Exact existence statement][d8]

[d1]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/WeilBound/CoreStatements/LocallyConstantCoinvariants/PfDict.lean#L7-L13
[d2]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/WeilBound/CoreStatements/LocallyConstantCoinvariants/RightOnto.lean#L38-L57
[d3]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AbelianVarietyTheory/BlockTheory/DivisorBase/WeilTensorModels.lean#L458-L470
[d4]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AbelianVarietyTheory/Proofs/DivisorProofs/ExistsTranslatesEqPrimFrameLat.lean#L105-L141
[d5]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AbelianVarietyTheory/Proofs/DivisorProofs/ExistsTranslatesEqPrimFrameLat.lean#L213-L248
[d6]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AbelianVarietyTheory/BlockTheory/DivisorBase/WeilTensorModels.lean#L474-L489
[d7]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AbelianVarietyTheory/BlockTheory/DivisorBase/WeilTensorModels.lean#L267-L279
[d8]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AbelianVarietyTheory/Definitions/Divisors/CTSmallCone.lean#L203-L208
