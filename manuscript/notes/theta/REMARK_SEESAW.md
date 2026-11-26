# The local Fourier pairing inside the theta seesaw

In items 8 and 12 of his [remark, p. 4](https://alpo.ge/remark.pdf#page=4), Alpöge describes lifting up a unitary tower and reading the resulting period at the other end. Two classical ideas play different roles here. Kudla’s seesaw identity writes the same theta integral as a pairing on either of two groups. The Rallis inner product formula evaluates the Petersson pairing of **two theta lifts** by a doubling integral. The reconstruction needs both the transfer of a period and control of the size of a lift. The source’s statement of the latter takes two tests and two cuspidal forms, a positive definite target, and target rank strictly greater than twice the source rank. For a unitary pair this is in the previously established convergent range discussed by Gan–Qiu–Takeda. [Kudla, §1, (1.14)](https://wiki.epfl.ch/waldspurger/documents/1984%20kudla.pdf) · [Gan–Qiu–Takeda, §1.7 and the discussion preceding Theorem 1.3](https://arxiv.org/pdf/1207.4709) · [The normalized doubling integral in the source](https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AbelianVarietyTheory/BlockTheory/NonGaloisCusps/RallisInnerProductFormula.lean#L26-L66)

## What joins two successive lifts

At a split finite place an interior pair of steps, from Bessel to Fourier–Jacobi and back to Bessel, leaves one column variable $y$ in the first test and one row variable $u$ in the second. Both range over $k^N$ for a nonarchimedean local field $k$. Write $x,z$ for the remaining matrix variables, $\psi$ for the fixed additive character and $du,dy$ for the product Haar measures specified by the source. Write $\mathcal S$ for the compactly supported locally constant functions. The joining operation is the ordinary Fourier pairing

$$
\mathcal C(f,g)(x,z)=\int_{k^N}\int_{k^N}
 g(z,u)\,\psi(-u\cdot y)\,f(x,y)\,dy\,du .
$$

There is a reason this kernel must occur. Let $B(f,g)$ be a bilinear map with values in any complex vector space. Assume that translating either shared variable and compensating on the other test by the corresponding character leaves $B$ unchanged. Explicitly the operations on the pair $(f,g)$ are

$$
(f,g)\longmapsto
(\psi(-u_0\cdot y)f(x,y),\;g(z,u+u_0)),\qquad
(f,g)\longmapsto
(f(x,y+y_0),\;\psi(-u\cdot y_0)g(z,u)).
$$

**Then $B$ factors uniquely through the linearized Fourier pairing.** There is a unique linear map $\lambda$ on $\mathcal S(X\times Z)$ such that $B(f,g)=\lambda(\mathcal C(f,g))$. The extra variables $X,Z$ may be the full remaining matrix spaces. This proves the pinned local factorization with its native sign and applies also to vector-valued outputs. [Source statement](https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AbelianVarietyTheory/Definitions/LatticeFrames/ContrFactor.lean#L101-L112) · [Use for the split line model](https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AbelianVarietyTheory/Proofs/DecoratedLatticeProofs/LineContractionSplitPlaceLocalModel.lean#L19-L74)

Indeed, products $f(x,y)g(z,u)$ identify the algebraic tensor product with the test functions in all four variables. To see this, subdivide the compact support into cosets of product compact open lattices on which the function is constant. Extend $B$ to this test space by linearity. Multiplication by $\psi(u\cdot y)$ converts it to a functional invariant under ordinary translations in $(y,u)$. A translation-invariant linear map on test functions in an additive local vector space factors through Haar integration. On indicators of translates of one compact open lattice its value is constant. Subdivision into cosets of a common smaller lattice shows the value is proportional to volume on every compact open coset. Apply this argument with each fixed test function in $(x,z)$ and undo the character multiplication. This gives the displayed formula. The fiber integral is onto, since a test function of $(x,z)$ can be multiplied by a compactly supported function of $(y,u)$ of integral one before undoing the twist. This proves uniqueness as well. [Pinned proof of the factorization](https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AbelianVarietyTheory/Proofs/DecoratedLatticeProofs/HeisenbergInvariantFactorsContraction.lean#L25-L181)

## The scalar for the symmetric interior position

One can now evaluate exactly the part of the local constant contributed by joining the two tests. Suppose $\psi$ has conductor $\mathcal O_k$ and normalize $dy,du$ by $\operatorname{vol}(\mathcal O_k^N)=1$. For any lattice $L$ in $k^N$ write $L^\perp$ for its annihilator under $\psi(u\cdot y)$. Translation of the integral by a member of $L$ gives

$$
\int_L \psi(-u\cdot y)\,dy=\operatorname{vol}(L)\,\mathbf 1_{L^\perp}(u).
$$

For the two local tests $f=c_1F(x)\mathbf1_L(y)$ and $g=c_2G(z)\mathbf1_{L^\perp}(u)$ this gives $\mathcal C(f,g)=c_1c_2F(x)G(z)$. In particular, at the source’s symmetric position with parameter $c=2r$, the first box is $L=\varpi^{-(r+1)}\mathcal O_k^N$ and the second is $L^\perp=\varpi^{r+1}\mathcal O_k^N$. If the residue field has $q$ elements, the two volumes are $q^{N(r+1)}$ and $q^{-N(r+1)}$. Their product is exactly one at every rank and level. The source retains their product as two positive factors $V W$ in its formula $C_1C_2VW$. Thus, once the two individual flattened tests have the indicated shapes, contraction introduces no additional scalar or loss as the tower grows. [Pure-column and pure-row shapes](https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AbelianVarietyTheory/Definitions/LatticeFrames/ContrFactor.lean#L62-L74) · [The double-step product](https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AbelianVarietyTheory/Proofs/DecoratedLatticeProofs/SymLevelDoubleStepOfFlatColumnFlatRow.lean#L251-L321) · [Haar normalization](https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AbelianVarietyTheory/Definitions/Foundations/MatrixMeasurableSpace.lean#L47-L53)

The same calculation gives the support and phase for a pair of translated boxes. For $f(y)=\mathbf1_{\alpha+L}(y)$ and $g(u)=\mathbf1_{\beta+M}(u)$ take $H=M\cap L^\perp$. The contraction vanishes when $(\beta+M)\cap L^\perp$ is empty. Otherwise pick $u_0$ in that intersection. The answer is zero if $\alpha\notin H^\perp$, and otherwise is

$$
\operatorname{vol}(L)\operatorname{vol}(H)\,\psi(-u_0\cdot\alpha).
$$

Indeed, the inner Fourier integral contributes $\psi(-u\cdot\alpha)\operatorname{vol}(L)\mathbf1_{L^\perp}(u)$, and the remaining integral is over $u_0+H$. Character orthogonality on $H$ proves the formula and its independence of $u_0$. Finite linearity evaluates any given pair of locally constant compactly supported slices by subdivision into boxes. The symmetric calculation above is the case $\alpha=\beta=0$, $M=L^\perp$.

The [marked split symmetric calculation](../periods/PERIOD_SPLIT_SYMMETRIC_CONTRACTION.md) gives both shapes and proves that translated cells outside the specified double coset contribute zero at this position. The source derives the shapes by root exchange, the support of the level test and its character on row and column unipotents. The linked calculation evaluates both scalar factors on the source’s normalized identity entries. The other local and global normalizations still enter. On the global side, Huang’s Hypothesis 3.6.1 states the comparison for the actual descended Bessel period. Wang’s Theorem 4.5 gives a related global theorem on Fourier coefficients of theta lifts, expressed as an integral of periods on the other group. Wang states his computations for the orthogonal–symplectic pair and discusses the unitary extension in §2, footnote 2. Applying such a general transfer to the particular unitary vectors would still require identifying the test functions, their support and the resulting integral. [Column calculation](https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AbelianVarietyTheory/Proofs/DecoratedLatticeProofs/FlatColumnIndicatorPureAtSymmetricPosition.lean#L183-L224) · [Row calculation](https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AbelianVarietyTheory/Proofs/DecoratedLatticeProofs/FlatRowIndicatorOfSymLevelExchange.lean#L52-L95) · [Huang, §3.6](https://hexagonmath.org/pdf/2611.00833v1#page=10) · [Wang, Theorem 4.5](https://arxiv.org/pdf/2311.14234#page=22)
