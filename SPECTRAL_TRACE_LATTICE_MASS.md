# The mass at one trace lattice and the distribution of its index

Fix one represented nonsingular local point in the corank-one calculation B8.10d. Let $O$ be the integers of the split or unramified quadratic algebra over a local field with residue size $q$. Put $m=2(r+1)$, $n=k+m-1$, $t=n-m=k-1$, and assume $k\ge4r+7$, $r\ge1$. Each integral frame class has a rank-$m$ difference lattice $M$ in its nondegenerate frame span $Y$. A self-dual ambient lattice $\Lambda$ of a term has trace lattice $P=\Lambda\cap Y\supset M$. The defect order is the *additive* cardinality $\beta=|P/M|$. Define $n_0$ as the original unsigned mass of all terms with $\beta=1$, allowing all frame classes, and $n_i$ as the mass of those with $\beta=q^i$. These use the same datum and inverse stabilizer measures as the total mass $n_{\rm tot}$. The generic mass of the source can select a single distinguished class; it will be denoted by $n_{\rm gen}$.

On the source's orbit-to-frame identification, the unsigned positive-defect proportion satisfies
$$
 \frac{n_{\rm tot}-n_0}{n_0}\ \le\
 4\left\{\prod_{h=0}^{m-1}(1-q^{-b(t-h)})^{-g}-1\right\}
 \ \le\ 64q^{-b(k-m)} .                                      \tag{1}
$$
Here $(b,g)=(1,2)$ at a split place and $(2,1)$ at an inert place. When $n_0=0$ the un-divided inequalities apply and all the terms vanish. The bound holds separately inside every contributing integral frame class. In particular the height of the point is absent from (1).

## Trace mass under a change of integral basis

For a nonsingular integral Hermitian matrix $T$ in rank $m$, let $c(T)$ be its corank modulo the uniformizer. Write $\xi=1$ for split and $\xi=-1$ for inert. The primitive frame density, with both integer lattices of volume one in the tuple and Gram coordinates, is
$$
 d(T)=\prod_{h=n-m-c(T)+1}^{n}(1-\xi^h q^{-h}).
$$
The [finite-field computation](SPECTRAL_SCALAR_DENSITIES.md) proves this formula for every represented residual corank, including dyadic residue fields. At a primitive tuple the differential of the Gram map is onto the integral Hermitian matrices, so every valid first residue has the same lift density. The unramified-field formula is also given by Hironaka. Throughout this range $1/2\le d(T)\le2$, since all the indices are at least $k-m$, $\sum_{h\ge k-m}q^{-h}\le 2q^{-(k-m)}$, and the products are bounded by $1-\sum q^{-h}$ below and $\exp(\sum q^{-h})$ above. [Primitive local densities, Hironaka](https://doi.org/10.2969/jmsj/05130553)

Let $\sigma(P)$ denote the inverse-stabilizer mass of **all** self-dual ambient lattices whose intersection with the fixed span is $P$. If $T_P$ is the Gram matrix of a basis of $P$, then
$$
 \frac{\sigma(P)}{\sigma(M)}
   = \beta^{-t}\frac{d(T_P)}{d(T_M)}.                           \tag{2}
$$
To verify the normalization, choose an ambient self-dual reference lattice and normalize additive tuple measure $dX$ and Hermitian matrix measure $dT$ in its integral coordinates. On a nonsingular fibre of $h(X)=X^*JX$ the quotient measure $dX/dT$ is invariant under the ambient isometry group. This follows from $|\mathrm N\det g|=1$, invariance of the Gram map, and change of variables for a submersion. The rational isometry group acts transitively on this fibre by Witt extension. Its stabilizer fixes the span pointwise. The volume of a compact isometry orbit equals the volume of the compact group divided by the stabilizer volume in the pointwise fixer, up to the one constant comparing quotient Haar and $dX/dT$. Equivalently unfold across the self-dual lattice orbit: an integral primitive embedding of $M$ has inverse image of the ambient lattice on $Y$ exactly $M$. Therefore its fibre mass is proportional to $\sigma(M)$. The same compact Haar normalization is used for every trace condition when they are all imposed on the *one original tuple fibre*. Self-dual lattices form one orbit here: in the split case choose a basis on one factor and its dual on the other; in the unramified case lift an orthogonal unit-norm basis successively from the nondegenerate residual Hermitian form, by orthogonal subtraction and the surjectivity of unit norms. [Orbit and content normalization][orb] · [Passage to trace sublattices][trace]

Write a basis of $M$ as a basis of $P$ multiplied on the right by $A$. Multiplication sends $X$ to $XA$ and sends $T$ to $A^*TA$. The additive Jacobians are $|\mathrm N\det A|^n$ and $|\mathrm N\det A|^m$, respectively. The latter identity can be checked on Smith diagonal entries, since integral invertible basis changes have Jacobian one: each diagonal coordinate is multiplied by a norm and each pair off the diagonal contributes one additional norm from each of its two indices. It also holds componentwise at split places. As $|\mathrm N\det A|=\beta^{-1}$, the primitive fibre of $P$ written in the fixed tuple coordinates contributes $\beta^{-t}d(T_P)$. Both it and the primitive fibre of $M$ use the same orbit constant, proving (2). For different native frame classes use their triangular changes from the common difference frame: the determinant norm of the change of the two frames is one and the $\theta$-difference normalization is the same. Their common proportionality constant for $\sigma(M)/d(T_M)$ is therefore the same. [Common frame and determinant scale][frames]

## Counting the trace lattices of prescribed index

Write $A_d(i)$ for the number of sublattices of additive index $q^i$ in a free rank-$d$ $O$-lattice. It also counts abstract overlattices of that index in its fraction space by taking duals with respect to any fixed perfect pairing. A DVR with residue size $Q$ has lattice series $\prod_{h=0}^{d-1}(1-Q^h Z)^{-1}$ in its colength variable. Indeed project a sublattice to the last $d-1$ coordinates and intersect it with the first axis. If the intersection is $\pi^eO$, the lifts of a basis of the projected lattice have $Q^{e(d-1)}$ choices. Induct on $d$. In the split case one chooses the two component sublattices independently. In the inert case DVR colength one has additive index $q^2$. Consequently
$$
 \sum_{i\ge0}A_d(i)z^i=\prod_{h=0}^{d-1}(1-q^{bh}z^b)^{-g},
 \qquad A_d(i)\le16(i+1)q^{(d-1)i}.                            \tag{3}
$$
For the bound, divide the single-DVR coefficient in degree $e$ by $Q^{(d-1)e}$. It is bounded by $\prod_{j=1}^{d-1}(1-Q^{-j})^{-1}<4$, using $\prod_{j\ge1}(1-2^{-j})\ge(1/2)(3/4)(1-\sum_{j\ge3}2^{-j})>1/4$. Convolution gives the split bound. Inert orders with odd $i$ have coefficient zero.

On the frame-class disintegration, all positive terms in that class at index $\beta$ contribute at most the sum of $\sigma(P)$ over integral $P$ of that index. At order one the contribution equals $\sigma(M)$. These comparisons use that a lattice with a fixed frame class determines its residual datum up to the original complement action, and that any self-dual lattice meeting $Y$ exactly in $M$ gives the primitive datum. The comparison permits some extensions with $\beta>1$ to fail the frame-level test. Combining it with (2) gives
$$
       n_i\le4 A_m(i)q^{-it}n_0 .                               \tag{4}
$$
[Class and datum unfolding][class] · [Primitive equality and positive-index comparison][term]

Evaluate (3) at $z=q^{-t}$ and sum (4) over $i>0$. This gives the first bound in (1). Let $u=q^{-b(t-m+1)}$. The logarithm of the product is at most $g\sum_{j\ge0}u q^{-bj}/(1-u)\le8u$. Since $m\ge4$ and $t-m+1=k-m\ge m+3$, this is at most one, so subtracting one costs at most $16u$. The same argument with the series truncated at any prescribed lower order bounds the corresponding tail.

If $\mathcal W$ is the total weight of integral frame classes, the primitive mass satisfies $n_0\le4\mathcal W n_{\rm gen}$ under the original chosen-class convention. Indeed the common constant multiplying $d(T_M)$ lies between $1/2$ and $2$ times the primitive trace mass in any represented class. The distinguished class has relative inverse stabilizer weight at least one, in the project's normalization. At height one the source gives a single class and $n_{\rm tot}=n_0=n_{\rm gen}$. Thus (1) can also be used for the source's comparison of total and distinguished generic masses. The exact identity (2) concerns the primitive trace measure; (4) and (1) concern the actual term set after the arithmetic class and frame identifications. [Distinguished class and weight][gen]

[orb]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AbelianVarietyTheory/Proofs/FlagMeasures/SelfDualHermitianLatticeMassBounds.lean#L113-L155
[trace]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AbelianVarietyTheory/Proofs/FlagMeasures/SelfDualHermitianLatticeMassOfTrace.lean#L85-L118
[frames]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AbelianVarietyTheory/Proofs/FlagMeasures/FrameLatticeGramDetAndMinorsOrbitInvariant.lean#L141-L168
[class]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AbelianVarietyTheory/Proofs/FlagMeasures/SumOverDataTermCountEqLatticeMass.lean#L24-L52
[term]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AbelianVarietyTheory/Proofs/FlagMeasures/HermitianFrameClassTermsLeOverlatticeMasses.lean#L25-L71
[gen]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AbelianVarietyTheory/Proofs/FlagMeasures/TotalLeGeneric.lean#L101-L121
