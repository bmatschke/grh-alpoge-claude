# Why the residual representation has no cyclotomic character subquotient

At a large coefficient prime a denominator estimate needs to control local cohomology. One step rules out a one-dimensional quotient even after replacing the residual representation by an arbitrary subrepresentation. We give the argument for the range of twists used in Roadmap B8.42bobh. The formal proof of Alpöge and Claude compares Sen weights of two lattices and uses the spacing of the jumps. The proof here computes the displacement of the two lattices directly on the one-dimensional quotient. [Original character obstruction](https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AbelianVarietyTheory/Proofs/InertiaEigenvalues/HomToCharacterLineEqZero.lean#L15-L63) · [RH Lean Roadmap, v41, B8.42bobh](https://github.com/rh-lean-roadmap/rh-lean-roadmap/blob/c7755c1086f05d0918ee8496d95912e4f35e22f9/docs/src/book/main.tex#L55457-L55472)

## The statement and its integral input

Let $K/\mathbb Q_\ell$ be unramified of degree $d'$, with $\ell\ge5$, and let $k$ be the residue field of the coefficient ring. Write $\omega$ for the residual cyclotomic character. The representation in question is $\overline W=(\chi_1^{-1}T_0)\otimes k$, where $T_0$ is the specified stable lattice and $\chi_1$ is the first character. We use the local theorem's exact realization $D$ by tuples of vector spaces over $B=k((X))$. Components have indices $i$ modulo $d'$. In each component the integral ring is $A=k[[X]]$. The linearized Frobenius $\varphi_i$ from component $i-1$ to $i$ is an isomorphism after scalar extension to $B$. On scalars, $\varphi(X)$ is a unit times $X^\ell$, and the chosen cyclotomic operator $\gamma$ fixes $k$ and satisfies $\gamma(X)/X\equiv1-X\pmod{X^2}$. For a lattice $N$, write $\varphi_i^*N_{i-1}=A\varphi_i(N_{i-1})$. [Scalar and representation data, B8.42bo–bod](https://github.com/rh-lean-roadmap/rh-lean-roadmap/blob/c7755c1086f05d0918ee8496d95912e4f35e22f9/docs/src/book/main.tex#L22396-L22441)

The integral inputs concern two specific lattices.

* The standard lattice $N$ of $D(\overline W)$ satisfies
  $X^{h_i-w_i}N_i\subset\varphi_i^*N_{i-1}\subset X^{-w_i}N_i$
  and $(\gamma_i-1)N_i\subset XN_i$. On $N_i/XN_i$ the operator induced by $X^{-1}(\gamma_i-1)$ has characteristic roots $u-w_i$ in $k$, counted with the multiplicities of $u$ in the prescribed jump multiset $U_i$.
* In $D(k(\omega^{-e}))$ there is a rank-one lattice $C$ with $\varphi_i^* C_{i-1}=X^eC_i$. Its cyclotomic action preserves $C_i$ and has multiplier $1+eX$ modulo $X^2$ in an integral basis. This input is used for $-1\le e<t$.

The lower-root action, primitive-divisor comparison and signed polynomial are proved on this integral lattice before reduction. [Wach comparison and primitive jets](../../manuscript/notes/galois/CYCLOTOMIC_WACH_COMPARISON.md)

The reduction then gives these statements on the two model lattices. The reconstruction's integral-model calculation explains how the Frobenius bounds and characteristic roots follow from that comparison. [Integral model and Sen computation](../../archive/rounds/v80/continuation_v80/model.tex#L5-L83) · [Exact standard and rank-one lattices, B8.42bobk](https://github.com/rh-lean-roadmap/rh-lean-roadmap/blob/c7755c1086f05d0918ee8496d95912e4f35e22f9/docs/src/book/main.tex#L22687-L22697)

**Claim.** Assume the position conditions (P1)–(P6) at the selected prime. For $-1\le e<t$, every $G_K$-equivariant map from a subrepresentation of $\overline W$ to $k(\omega^{-e})$ is zero. We spell out the position conditions used in the last step. [Exact position conditions and carry convention](https://github.com/rh-lean-roadmap/rh-lean-roadmap/blob/c7755c1086f05d0918ee8496d95912e4f35e22f9/docs/src/book/main.tex#L22362-L22374)

## The subquotient inherits the Frobenius bounds

Suppose the map is nonzero. Its image has dimension one, so it is onto. Write $E$ for the source subrepresentation, $P_i=N_i\cap D(E)_i$ and $Q_i$ for the image of $P_i$ in $D(k(\omega^{-e}))_i$. Exactness of $D$ identifies these subspaces and quotients over $B$. The full lattice $P_i$ of $D(E)_i$ is saturated in $N_i$, since $N_i/P_i$ injects into a vector space over $B$. Therefore an $A$-basis of $P_i$ extends to one of $N_i$. The Frobenius transforms of this extended basis give a $B$-basis in the next component, with the initial vectors spanning $D(E)_{i+1}$. Intersecting their integral span with $D(E)_{i+1}$ selects precisely the integral span of the initial vectors. Thus both height inclusions for $N$ pass to $P$. Applying the quotient map gives
$$
        X^{h_i-w_i}Q_i\subset\varphi_i^*Q_{i-1}\subset X^{-w_i}Q_i .
$$
The cyclotomic divisibility also descends. On $P_i$ this follows from $XN_i\cap D(E)_i=XP_i$. On $Q_i$ it follows by applying the quotient map.

The induced endomorphism $\nabla_i=X^{-1}(\gamma_i-1)$ on reduction modulo $X$ is $k$-linear. Indeed it preserves $XN_i$, because $\gamma(X)/X\equiv1\pmod X$ and $\gamma_i$ acts trivially on $N_i/XN_i$. The same holds on $P_i,Q_i$. The inclusions and projections commute with $\nabla_i$. Saturation gives an injection $P_i/XP_i\hookrightarrow N_i/XN_i$. The image on reduction surjects from $P_i/XP_i$ to $Q_i/XQ_i$. Consequently the eigenvalue of $\nabla_i$ on the one-dimensional quotient is among the roots of its characteristic polynomial on $N_i/XN_i$. This follows by taking a basis adapted to the kernel and then to the subspace, in which the characteristic polynomials multiply. [Subquotient comparison in the source](https://github.com/rh-lean-roadmap/rh-lean-roadmap/blob/c7755c1086f05d0918ee8496d95912e4f35e22f9/docs/src/book/main.tex#L55346-L55352)

## Computing the displacement on a line

The fractional ideals of $A$ are exactly the powers of $X$. Thus $Q_i=X^{a_i}C_i$ for an integer $a_i$. Its Frobenius exponent relative to $Q_i$ is $e+\ell a_{i-1}-a_i$. The two height inclusions say that this integer belongs to $[-w_i,h_i-w_i]$. Since $w_i\ge1$, $w_i+t\le h_i$, and $-1\le e<t$, the integer $e$ also belongs to that interval. Its length is $h_i$, so $|\ell a_{i-1}-a_i|\le h_i$. Define $\sigma_i=\lfloor\sum_{j\ge1}h_{i+j}/\ell^j\rfloor$. Iterating forward gives
$$
 |a_i|\le \ell^{-n}|a_{i+n}|+\sum_{j=1}^n \ell^{-j}h_{i+j}.
$$
The first term tends to zero by periodicity. As $a_i$ is integral, $|a_i|\le\sigma_i$.

For a generator $c_i$ of $C_i$, compute the multiplier of $\gamma_i$ on $X^{a_i}c_i$ modulo $X^2$. It is
$$
       (1-X)^{a_i}(1+eX)\equiv1+(e-a_i)X\pmod{X^2}.
$$
The formula holds also for negative $a_i$, by inversion of a unit. Therefore $e-a_i$ is the residual eigenvalue on $Q_i/XQ_i$. By the preceding paragraph some $u\in U_i$ satisfies $u\equiv y\pmod\ell$, where $y=w_i+e-a_i$. [Comparison by cyclic carries in the original proof](https://github.com/rh-lean-roadmap/rh-lean-roadmap/blob/c7755c1086f05d0918ee8496d95912e4f35e22f9/docs/src/book/main.tex#L55338-L55354)

## Why the congruence is impossible

Put $J_i=[w_i,w_i+t-1]$. The integer $y$ is within $\sigma_i+1$ of $J_i$, including when $e=-1$. Reflect coordinates by $z\mapsto h_i-z$ at a negative position and leave them unchanged at a positive position. Under this operation the designated low window becomes $[1,\eta'_i]$ and (P2)–(P3) put the reflected $J_i$ inside it. The reflected $y$ consequently lies in $[-\sigma_i,\eta'_i+\sigma_i+1]$.

If $u$ is outside the low window, (P6) excludes every residue in the larger reflected interval $[-2\sigma_i-2,\eta'_i+2\sigma_i+3]$. If $u$ is in the low window, its reflected coordinate belongs to $[1,\eta'_i]$. Its distance from the reflected $y$ is at most $\eta'_i+\sigma_i+1<\ell$ by (P4). The congruence forces equality, hence $u=y$. But (P5) puts every such $u$ at distance greater than $\sigma_i+2$ from $J_i$. Both cases are impossible. This proves the claim, with no restriction that $h_i<\ell$. [Excluded band in Roadmap B8.42bobf](https://github.com/rh-lean-roadmap/rh-lean-roadmap/blob/c7755c1086f05d0918ee8496d95912e4f35e22f9/docs/src/book/main.tex#L22626-L22650)

Taking $e=0$ excludes the trivial subrepresentation. Taking $e=-1$ excludes a map from $\overline W$ to $k(\omega)$. These are the two vanishings used with local Tate duality to remove the outer cohomology groups in the local Euler characteristic calculation. The mathematical input left upstream of this proof is the integral comparison that supplies the two lattices and their weights. [Application to local cohomology](https://github.com/rh-lean-roadmap/rh-lean-roadmap/blob/c7755c1086f05d0918ee8496d95912e4f35e22f9/docs/src/book/main.tex#L22583-L22600)
