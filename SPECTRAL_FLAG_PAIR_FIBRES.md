# Counting both flags over a common sublattice

Fix the tied rows, level and reduced Gram labels of Roadmap B8.08k and B8.10ac. Let $g\ge3$, let $L$ be the rank-$k$ positive definite middle lattice, and put $N=T_u^f$, $f=[F:\mathbb Q]$, $r=r_S$, $m=2r+2$. Work with the original nonsingular terms and the prescribed row equivalences. Write $h_Z$ for the reduced-label height, $H=h_Zh_{Z'}$, and choose the standing height constant large enough for the single-frame representative bounds below. Let $\Delta$ satisfy $1\le\Delta\le H^3$. We count the original pairs of corank $s$, $2\le s\le k$, with those two labels and with pair determinant at most $\Delta$. Throughout, the determinant of an integral definite lattice is the positive square root of its discriminant-module order. This is an integer here. At a split prime of the CM extension the two factors of the discriminant module are in perfect duality and have equal order. At an inert prime the residue field has square cardinality, and there are no finite ramified primes. An inclusion of additive index $a$ in equal rank multiplies this determinant by $a$.

Let $\mathcal W_s(\Delta)$ be the sum of the original row weights of these pairs divided by the total row mass. Put
$$
 j=k-s,\qquad A_s=16(s+\log f),\qquad p=k+A_s,\qquad
 X_s=\begin{cases}M_sM_j/M_k&j>0,\\1&j=0.\end{cases}
$$
The masses $M_i$ are those of the standard unimodular genera. Under the standing tied-row hypotheses one has
$$
 \mathcal W_s(\Delta)
 \le 4\,81^{sf} X_s(\Delta/N)^k H^{E_s},\qquad
 E_s=8r+18s(1+r)+8r^2+\tfrac72 A_s+3.                 \tag{1}
$$
In particular both end ranks admit a label-independent $X_s$. There is no additional height exponent proportional to $k$ from the genus factor. Below we give a sharper bound with the sublattice indices still visible. The [two determinant cutoffs](SPECTRAL_FLAG_PAIR_DETERMINANTS.md) specialize the result to the original nondegenerate and degenerate classes. The real orbital majorant is a separate input. [Original count and normalization][roadmap]

## Why the isometry adds no multiplicity

Write $\Lambda$ for the full row lattice, $F$ for its base flag and $F_1,F_2$ for the moving flags. An original pair gives the triple $(F_1,F_2,\beta)$, where $\beta$ is the relative isometry of the full lattices. The original pair indexing is injective on each row modulo the triple equivalence, by the pair representative condition of the tied data. The row weight of a pair depends only on $\Lambda$. Grouping by $\Lambda$ therefore bounds the desired sum by the weighted sum of triple-class counts. In particular, multiplicities at the level of raw flag bases would give the wrong counting problem. [Original pairs, their equivalence classes and their row weights][rows]

For fixed moving flags, two admissible isometries induce the same map from $X_1^\perp/X_1$ to $X_2^\perp/X_2$, where $X_i$ is the $r$-dimensional isotropic span of $F_i$. Here is the reason for uniqueness on this quotient. Their ratio fixes the class of the last vector itself modulo $X_1$. On the orthogonal quotient of its perpendicular by $X_1$, the ratio preserves a positive definite integral trace lattice. The common level marking makes it the identity modulo $g$ on that lattice. More explicitly, a representative $x$ in the row lattice and perpendicular to $X_1$ and the last vector can be matched modulo $g\Lambda+X_1$ with a representative in the base-flag perpendicular. This follows by extending the resulting integral functional on the primitive isotropic intersection using unimodularity. The two markings match that same representative with the two images of $x$ modulo $g\Lambda+X_2$. Subtract them and pull back. The difference from $x$ in the orthogonal quotient lies in $g$ times its integral lattice. The integral isometry group of the positive definite trace lattice is finite, and the principal congruence kernel on a free abelian group is torsion-free at level $g\ge3$. Thus the ratio is the identity there. The last vector has nonzero norm and supplies the remaining rational line in $X_1^\perp/X_1$. Now move the two flags by independent allowable unipotents and conjugate $\beta$ accordingly. The same uniqueness gives precisely triple equivalence. Consequently an ordered pair of single-frame classes accounts for at most one triple class in this count. [Integral congruence and quotient argument][unique] · [Transport under the two unipotents][common]

## The lattice shared by the two frame counts

For a single flag use $B_i\subset A_i\subset L$ for the projections of its two lifted lattices, respectively the theta lattice and the level lattice, to the base definite space. These projections preserve the finite index $I_i=[A_i:B_i]$. For the triple the projected pair lattice $M$ has rank $k-s$, lies in both $A_i$, and the native pair determinant is $\det(M)I_1I_2$. These statements use the transversality of the lifted flags to the base isotropic span. In passing to the second flag the pair condition identifies the two projections modulo that span. Take
$$
 P=M\cap B_1\cap B_2 .
$$
The map $M/P\longrightarrow A_1/B_1\oplus A_2/B_2$ is injective. Hence $P$ has rank $j$, is contained in each $B_i$, and satisfies $\det P\le\det(M)I_1 I_2\le\Delta$. Summing over all such $P$ can overcount pairs, which is permissible for an upper bound. [Projections, indices and common intersection][common]

For a fixed $P$ the number of single-frame classes with label $Z$ and $P\subset B_1$ is at most
$$
 K=N^{2r}\Delta^r 9^{sf} H^{9s(1+r)+4r^2}.                    \tag{2}
$$
Here are the choices in the counting argument, including the powers that enter (2).

* Use integral triangular changes to realize the chosen Gram representative exactly. A frame-fixing rational isometry puts the row in split form, preserving the definite middle lattice and carrying the equivalence relation by conjugation. A represented reduced label admits a representative with control parameter $Q\le h_Z^2$, bounding the norm of a nonzero maximal row minor, the archimedean product of the Gram quantity, and the different factor used in the skew coordinates. [Reduction to an exact Gram representative][split] · [Size of the representative][rep]
* A lift of $P$ is the graph of $r$ linear functionals into the fixed isotropic space with its prescribed coefficient ideals. Restriction from the saturation costs at most $[P^{\rm sat}:P]\le\Delta$ per functional. On the saturation the classes modulo pairing with $L$ number at most $|L^\#/L|=N^2$ per functional. Indeed the saturation is a projective direct summand as an integer-ring module, so an integral functional extends to $L$. Eichler transformations realize the resulting changes of representatives. The coefficient ideals are invertible and preserve these indices locally. This costs at most $N^{2r}\Delta^r$. [Representatives and changes of lifts][lifts]
* Fix that graph. In $S=L\cap P^\perp$ of rank $s$ the perpendicular coordinates form a tuple $w_0,\ldots,w_r$ in the Hermitian dual of $S$. The extracted denominator ideal $I$ has $\mathrm N I\le\Delta^2N^2$ and $I S^\#\subset S$. If $Y$ denotes the first $r$ rows of the Gram representative, fix one nonzero maximal minor and take the cofactor linear combination of the tuple. Its Hermitian norm is fixed by the Gram equation. Packing at the $f$ complex places bounds the choices for the combination by $9^{sf}(\mathrm N I\,Q)^s$. For a fixed combination, adjugate elimination in the nonzero minor bounds the kernel modulo integral row operations on the tuple by $(\mathrm N I\,Q)^{sr}$. The row operations are realized by frame-fixing integral unipotents. For equal perpendicular coordinates the remaining difference is in the fixed isotropic frame and satisfies the skew Gram equation. Reduction modulo central integral skew translations costs at most $Q^{2r^2}$. These are covering counts of the actual orbits, so no independence of the three choices is required. [Cofactor and kernel count][tuple] · [Skew translations and realization][fixed]

Multiplying gives $N^{2r}\Delta^r9^{sf}(\Delta^2N^2Q)^{s(1+r)}Q^{2r^2}$. The height choices give $N^2\le H$, $Q\le H^2$ and $\Delta\le H^3$. They imply (2), retaining the exponent $4r^2$ in the last factor. The same bound holds for $Z'$. We have now bounded the row count by $K^2$ times the number of rank-$j$ sublattices $P\subset L$ with $\det P\le\Delta$. This last number is invariant under isometry of $L$. Normalized averaging with the actual row weights agrees with the inverse-automorphism genus mean for such functions. The equality groups the row lattices by their middle class, whose total row weight is the same multiple of its inverse stabilizer at every class. [Row-to-genus identity][genus]

## Summing the index without a height loss at the two end ranks

For $j\ge1$ and any saturated rank-$j$ lattice $V$, let $a_j(n)$ count the sublattices of additive index $n$ in $V$. These numbers depend only on $E,j$. For $z>j$ their generating series is
$$
 D_j(z)=\sum_{n\ge1}a_j(n)n^{-z}
       =\prod_{i=0}^{j-1}\zeta_E(z-i).
$$
Indeed, over every local discrete valuation ring the projective lattice is free. In triangular form, fixing the diagonal valuations gives one residue choice per off-diagonal entry modulo its corresponding diagonal ideal. With residue field of size $q$ the sum of these counts, weighted by the local index to power $-z$, is $\prod_{i=0}^{j-1}(1-q^{i-z})^{-1}$. Independent local lattices equal to the original one almost everywhere give exactly one global sublattice by intersection. This also proves the formula for a nonfree projective $V$.

By the [primitive genus mean](SPECTRAL_HIGHER_CORANK_MASSES.md), the normalized number of possible saturations of determinant $d$ is at most $X_s N^{A_s-k}d^p$. If the index in the saturation is $n$, the determinant becomes $dn$. Sum first over $1\le d\le\Delta/n$. For $x\ge1$, the increasing function $t^p$ gives $\sum_{1\le d\le x}d^p\le x^p+x^{p+1}/(p+1)$ by retaining the last term and integrating the others. Extending the positive sums in $n$ yields
$$
 \mathcal W_s(\Delta)\le K^2 X_s(\Delta/N)^k(\Delta N)^{A_s}
 \left[D_j(p)+\frac{\Delta}{p+1}D_j(p+1)\right].                 \tag{3}
$$
For $j=0$ the zero lattice is the only possibility, and the direct bound is $K^2$. The prefactor in (3) after $K^2$ is at least one when $s=k$, using $A_k\ge k$, $N,\Delta\ge1$ and $D_0=1$.

The Euler factors in (3) are uniformly bounded even with varying field. In fact $\log\zeta_E(t)\le2f\log\zeta(t)$ and $\log\zeta(t)\le2^{-t}(1+2/(t-1))$ for $t>1$, by summation and the integral test. The smallest argument in $D_j(p)$ is $s+A_s+1$. This gives $\log D_j(p)\le 2f\,2^{-(s+A_s)}(1+2/(s+A_s))<\log 2$, using $s\ge2$ and the definition of $A_s$. Also $D_j(p+1)\le D_j(p)$. The bracket in (3) is therefore at most $4H^3$. Substitution of (2) and $(\Delta N)^{A_s}\le H^{7A_s/2}$ proves (1).

The same sum bounds the contribution covered by lattices of saturation index at least $Y\ge1$. For $j\ge1$ replace the two Dirichlet series inside the bracket of (3) by
$$
 e^{2f}Y^{-(s+A_s-1)},\qquad e^{2f}Y^{-(s+A_s)},
$$
respectively. Indeed $D_j(j+1)\le e^{2f}$ since $\sum_{t=2}^{\infty}\log\zeta(t)\le\sum_{n\ge2}1/[n(n-1)]=1$. Comparing the powers of $n\ge Y$ proves both bounds. For $j=0$ the only possible index is one.

## Use in the collision estimate

For $m=2r+2$, one can choose a single absolute $c$ large enough that $E_s\le c(s+m)m+c(1+\log_2(2f))$ and $4\,81^{sf}\le(csf)^{6sf}$ for all these ranks. Thus (1) supplies the required finite count at every specified cutoff. Its label dependence has the same shape at $s=k-1,k$ as in the interior. In the [label moment calculation](SPECTRAL_HIGHER_CORANK_MASSES.md) one can use the rank-specific moment displayed there also at those end ranks, whenever the cited orbital bounds hold at that order. The height cost from $X_s$ is zero there as well.

For the full collision classes, the [flag determinant and angular calculation](SPECTRAL_FLAG_PAIR_DETERMINANTS.md) supplies both original cutoffs, identifies the reduced-label Gram product in the integral normalization, and improves $\Delta_i\le H^3$ to $\Delta_i\le\sqrt H$. It also gives a smaller exponent than (1) on those classes. The real squared-amplitude estimates and their normalization on the operator still enter the global bound. [Original nondegenerate count][nd] · [Original degenerate count][deg]

[roadmap]: https://github.com/rh-lean-roadmap/rh-lean-roadmap/blob/02a95b4c62db610642af5f278ee5d0d6df87b348/docs/src/book/main.tex#L45778-L45874
[rows]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Formalism/SharpRestriction/CuspSpanNormBounds/CayleyDegreeNondegeneracy/RowsCnt.lean#L93-L186
[unique]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AbelianVarietyTheory/Proofs/FlagMeasures/PairIsometryUniqueOnOrthModIsotropic.lean#L39-L197
[common]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AbelianVarietyTheory/Proofs/FlagMeasures/OneLeSizeZ.lean#L81-L140
[split]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AbelianVarietyTheory/Proofs/FlagMeasures/FrameTermCountSublatticeBound.lean#L214-L235
[rep]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AbelianVarietyTheory/Proofs/FlagMeasures/CountTermsGramClassOverSublattice.lean#L221-L265
[lifts]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AbelianVarietyTheory/Proofs/FlagMeasures/ExistsSublatticeLiftsModuloFixingUnipotent.lean#L234-L421
[tuple]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AbelianVarietyTheory/Proofs/FlagMeasures/CardIntegralFramesFixedLiftLe.lean#L166-L230
[fixed]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AbelianVarietyTheory/Proofs/FlagMeasures/CardIntegralFramesFixedLiftLe.lean#L412-L540
[genus]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AbelianVarietyTheory/Proofs/FlagMeasures/RowLatticesMeanEqGenusMean.lean#L891-L910
[nd]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Formalism/SharpRestriction/CuspSpanNormBounds/CayleyDegreeNondegeneracy/RowsND.lean#L157-L189
[deg]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Formalism/SharpRestriction/CuspSpanNormBounds/CayleyDegreeNondegeneracy/RowsDeg.lean#L185-L231
