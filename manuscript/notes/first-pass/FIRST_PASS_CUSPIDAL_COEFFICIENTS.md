# The coefficient field of a cuspidal row at almost every prime

Fix a good finite type $\sigma$ with nonzero isotypic space in row $1\le j\le m$ of the [labelled state](FIRST_PASS_LABELLED_STATE.md). Write $E$ for its CM field and $K$ for the image in $\mathbf C$ of its specified coefficient subfield $L_0$. The [good-row parameter proof](FIRST_PASS_CUSPIDAL_ROW.md) gives an eligible unitary cuspidal representation $\pi$ of $\mathrm{GL}_r(\mathbf A_E)$, regular algebraic and conjugate self-dual, whose local parameters agree with this row at **every** split place of $E/E^+$. The following argument proves the coefficient clause of the row assertion with this same $\pi$ and this same $K$. It uses the [normalized row Hecke eigenvalues](FIRST_PASS_HECKE_RATIONALITY.md) in $L_0$ and the given character frame. [Exact row statement][require] · [Order of the deductions][chain]

## From the other half of a split prime

Write $Nw$ for the residue-field size. At a place $w$ where $\pi$ is spherical let $A_w$ be its multiset of arithmetic Frobenius eigenvalues in the project's convention. Form the monic polynomial
$$
 P_w(X)=\prod_{a\in A_w}\bigl(X-(Nw)^{(1-r)/2}a\bigr).
$$
At a split $w$ use the row Hecke comparison at its conjugate $\bar w$, omitting the finite exceptional set and the primes where the row character $\mu_{j-1}$ is ramified. Conjugate self-duality changes the eigenvalues to their reciprocals between the two halves. This cancels the inversion in the Hecke formula at $\bar w$. Set $q=Nw=N\bar w$ and $c=\mu_{j-1}(\bar w)^{-1}q^{-n_V/2}$, using the frame's uniformizer value. If $h_k\in K$ is the given normalized row eigenvalue there, the resulting equality is
$$
 e_k(A_w)= h_k\,q^{-k(r-k)/2}\,c^{-k},\qquad 1\le k\le r .
$$
Here $e_k$ is the $k$th elementary symmetric function. The frame comparison gives $\mu_{j-1}(\bar w)\in K^\times$. The ambient rank $n_V$ is even, $r$ is odd, and $k(r-k)$ is even. Thus the displayed factors are in $K$, as is $q^{(1-r)/2}$. The coefficients of $P_w$ belong to $K$ at all split places outside a finite set. No choice of a root of a Hecke polynomial is required. [Split Hecke eigenvalues and character values][split] · [Parity and passage to the polynomial][parity]

## A uniform set of primes for descent

For a regular algebraic polarized cuspidal representation of a general linear group over a CM field, Barnet-Lamb, Gee, Geraghty and Taylor, Theorem 2.1.1(2), identifies the Frobenius-semisimplified Weil–Deligne parameter of the associated $\ell$-adic representation at $w\nmid\ell$ with the parameter in the $(1-r)/2$ normalization. For our odd rank, take the quadratic character attached to $E/E^+$ as polarizing character. It is trivial on norms from $E$ and takes the required value $-1$ at every real place. Thus the polarization relation reduces to conjugate self-duality. At a spherical place its parameter has trivial inertia and zero monodromy. In the unitary normalization an unramified character sends **arithmetic** Frobenius to the inverse of its uniformizer value. Reading both sides at arithmetic Frobenius gives $P_w$ as written above. This is the unramified consequence needed from local–global compatibility. [Barnet-Lamb–Gee–Geraghty–Taylor, Theorem 2.1.1][blggt] · [The uniform unramified conclusion on the specified closure][uniform]

Fix $\ell=2$ and a field isomorphism $\iota:\overline{\mathbf Q}_2\simeq\mathbf C$. Let $U$ consist of the spherical primes of $\pi$ away from 2. This cofinite set works for every coefficient isomorphism. For $\gamma\in\operatorname{Aut}(\mathbf C/K)$ take the two continuous representations associated to the same $\pi$ via $\iota$ and $\gamma\circ\iota$. At a split prime in $U$ outside the previous finite set, their characteristic polynomials at a Frobenius lift agree **over** $\overline{\mathbf Q}_2$, since $\gamma(P_w)=P_w$.

Frobenius elements at such split primes, allowing conjugates and all choices of lifts, are dense in $G_E$. Indeed Chebotarev gives the required conjugacy classes in every finite quotient. One may restrict to prime ideals of absolute residue degree one: the ideals of degree at least two have Dirichlet density zero. After the ramified primes are removed, a degree-one prime of $E$ lies over a split prime of $E^+$, by multiplicativity of residue degrees. Equality of each characteristic-polynomial coefficient now extends by continuity on $G_E$ in its 2-adic realization. The complex field automorphism is used only to compare algebraic values. In particular at any $w\in U$ both representations give the same polynomial over $\overline{\mathbf Q}_2$ at Frobenius. Applying the two coefficient identifications gives $\gamma(P_w)=P_w$. This holds for every $\gamma$ and every $w$ in the same $U$. [Degree-one Frobenius density on this host][dense] · [Two coefficient identifications and continuity][galois]

The fixed field of $\operatorname{Aut}(\mathbf C/K)$ is $K$. In characteristic zero an algebraic element outside $K$ has a distinct conjugate, and the corresponding embedding extends to an automorphism of $\mathbf C$. For a transcendental element, extend it to a transcendence basis, translate that basis element by 1 and extend the automorphism to the algebraic closure. Thus every coefficient of $P_w$ belongs to $K$ on $U$. This fixed-field argument also explains why 2-adic density alone would be insufficient to place a limiting coefficient in the original number field. [Coefficient descent][descent]

## A direct automorphic proof and uniqueness

There is also a way to remove the split-prime restriction using only automorphic results at this step. Clozel's Theorem 3.13 gives a cuspidal conjugate $\pi^\gamma$ of each regular algebraic cuspidal $\pi$, with finite part obtained by applying $\gamma$ to its scalars. At a spherical place the spherical Hecke algebra has rational double-coset generators. Their eigenvalues are the elementary symmetric functions of the geometric Satake eigenvalues with the factors $q^{k(r-k)/2}$. These factors and $q^{(1-r)/2}$ are rational in our odd rank. The roots are nonzero. Thus inversion of the roots and the shift used for $P_w$ give a reversible, $\gamma$-equivariant passage between $P_w$ and the spherical Hecke character. If $\gamma$ fixes $K$ it follows from the split calculation that $\pi_w^\gamma\simeq\pi_w$ at all but finitely many split primes. [Clozel, *Motifs et formes automorphes*, Theorem 3.13][clozel]

Apply Ramakrishnan's Corollary B to the quadratic extension $E/E^+$. Outside its finite ramified set, the places of relative residue degree one are exactly the split places. The corollary therefore gives $\pi^\gamma\simeq\pi$. Reading the local Hecke character again at **every** spherical place gives $P_w\in K[X]$, including primes over 2. The same corollary also shows that any two candidate cuspidal lifts of the row are isomorphic: they agree at the spherical split primes by the prescribed row comparison and Satake. Both deductions start from an existing cuspidal lift. This identifies precisely how much global multiplicity one supplies here. [Ramakrishnan, *A mild Tchebotarev theorem for GL(n)*, Corollary B][rama]

## Put back the frame character

The row assertion asks for $\pi\otimes\eta^{-1}$ with the **ambient** shift $(1-n_V)/2$. Write $n_V=r+t$ and $t=2b+1$. At $w\in U$ the character $\eta^{-1}$ contributes $\eta_w(\varpi_w)$ on arithmetic Frobenius. The difference of the two shifts is $-b-1/2$. The existing frame gives $y_w=\eta_w(\varpi_w)(Nw)^{-1/2}\in K^\times$, so every old root is multiplied by
$$
 \lambda_w=y_w(Nw)^{-b}\in K^\times .
$$
The required polynomial is $\lambda_w^rP_w(X/\lambda_w)\in K[X]$. Since the embedding $L_0\hookrightarrow K$ is an isomorphism onto this image, this gives the polynomial over the exact field requested at every $w\in U$. The same $\pi$ realizes the split local comparisons with which we started. [Frame, rank difference and Frobenius calculation][eta] · [Scaling the polynomial][scale]

[blggt]: https://annals.math.princeton.edu/wp-content/uploads/annals-v179-n2-p03-p.pdf#page=38

[require]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AbelianVarietyTheory/Definitions/AutomorphicMembership/BlocksUnique.lean#L137-L141
[chain]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AutomorphicArithmetic/ThetaCorrespondence/ThetaPairLifts/ThirdPlaceSeries/SCuspOfParSt.lean#L19-L31
[split]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AbelianVarietyTheory/Proofs/IwasawaDecomposition/EsymmMapMulConst.lean#L34-L94
[parity]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AbelianVarietyTheory/Proofs/IwasawaDecomposition/EsymmMapMulConst.lean#L95-L128
[uniform]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AutomorphicArithmetic/ThetaCorrespondence/ThetaPairLifts/ThirdPlaceSeries/ExistsRepUniform.lean#L22-L55
[dense]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AbelianVarietyTheory/Proofs/IwasawaDecomposition/ChebSplitNd.lean#L13-L24
[galois]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AutomorphicArithmetic/ThetaCorrespondence/ThetaPairLifts/ThirdPlaceSeries/GalPolLiftsOfSplit.lean#L21-L72
[descent]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AutomorphicArithmetic/ThetaCorrespondence/ThetaPairLifts/ThirdPlaceSeries/GalPolLiftsOfSplit.lean#L68-L79
[eta]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AbelianVarietyTheory/Proofs/IwasawaDecomposition/ProdXSubCScaleMemLifts.lean#L52-L95
[scale]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AbelianVarietyTheory/Proofs/IwasawaDecomposition/ProdXSubCScaleMemLifts.lean#L23-L42

[clozel]: https://www.jmilne.org/math/Books/AA1988a.pdf
[rama]: https://www.its.caltech.edu/~dinakar/papers/mildTcheb-JNT.pdf#page=2
