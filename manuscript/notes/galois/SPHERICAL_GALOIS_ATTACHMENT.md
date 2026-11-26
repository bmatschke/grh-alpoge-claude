# Spherical Galois attachment over CM fields

The cohomological window needs a single Galois representation whose Frobenius polynomials and Hodge filtration can be read at specified places. Proposition B9.38 first asks for agreement at almost all places, then asserts local properties at **every** spherical place for **every** semisimple representation with that agreement. Theorem 2.1.1 of Barnet-Lamb, Gee, Geraghty and Taylor supplies the representation over the given CM field. We deduce both quantifiers and compute the local polynomials and jumps in the conventions of B9.38. [Statement of B9.38][spherical] · [Theorem 2.1.1, p. 538][theorem] · [The four local assertions in Lean][core]

## From infinitesimal characters to algebraic weights

<!--
% BEGIN GSPH1
-->

<span id="claim:GSPH1"></span>Let $E/F$ be a CM extension with $F$ totally real and $c$ its nontrivial automorphism. Fix a prime $\ell$ and an isomorphism $\iota:\overline{\mathbb Q}_\ell\to\mathbb C$. The input is a cuspidal representation $\pi$ of $\mathrm{GL}_a(\mathbb A_E)$, $a\ge1$, and a Hecke character $\chi$ of $F$. Its polarization reads $\pi^c\simeq\pi^\vee\otimes(\chi\circ N_{E/F}\circ\det)$ with $\chi_v(-1)=(-1)^a$ at each real place. These are the CM field and polarization conditions in §2.1 of the published theorem, with $E,F,a$ in place of the authors' $F,F^+,n$. [Polarized inputs in B9.02][input] · [Published definitions, pp. 536–537][weights]

At each complex embedding $\sigma:E\hookrightarrow\mathbb C$, list the infinitesimal weights in decreasing order $z_1>\cdots>z_a$. They belong to $(a-1)/2+\mathbb Z$. The half-sum of positive roots has coordinates $\rho_i=(a+1-2i)/2$. Hence $\lambda_i=z_i-\rho_i$ is integral and $\lambda_i-\lambda_{i+1}=z_i-z_{i+1}-1\ge0$. This is a dominant algebraic highest weight. The tuple of these weights over the embeddings gives an algebraic representation with the infinitesimal character of $\pi_\infty$. The authors label $\pi$ by the highest weight $\mu$ of the representation $\Xi_\mu$ whose **dual** has the infinitesimal character of $\pi_\infty$. Taking the dual reverses and negates the highest weight, so $\mu_{\sigma,a+1-i}=-\lambda_i$. For $\sigma=\iota\circ\tau$ this gives
$$
 \frac{a-1}{2}-z_i
   =\mu_{\sigma,a+1-i}+i-1,\qquad
 H_\tau=\{\mu_{\iota\tau,j}+a-j:1\le j\le a\}.
$$
This identifies B9.04 with the multiset in part (3) of the theorem, including multiplicity at each embedding. The authors assign $-1$ to the cyclotomic character. For a de Rham representation their multiplicity at $i$ is the dimension of the $\tau$-component of $\operatorname{gr}^i D_{\rm dR}$. [Weights in B9.04][input] · [Hodge–Tate convention, p. 510][conventions] · [Theorem 2.1.1(3)][theorem]

<!--
% END GSPH1
-->

<!--
% BEGIN GSPH2
-->

<span id="claim:GSPH2"></span>The common weight can also be read from $\chi$. Write $\chi_v(x)=x^{b_v}$ on the positive reals. Polarization pairs the infinitesimal weights at conjugate embeddings by $z\mapsto b_v-z$, so $b_v$ is a sum of two weights in $(a-1)/2+\mathbb Z$ and is integral. The finite unit character of $\chi$ has finite image. On a finite-index subgroup of the totally positive global units the product of the infinite characters is therefore $1$. Taking logarithms, $(b_v)_v$ annihilates the logarithms of those units. By Dirichlet's unit theorem these span the hyperplane of coordinate sum zero, so all $b_v$ equal one integer $b$. Substitution in the jump formula gives $H_{\tau c}=a-1-b-H_\tau$ and supplies $w_{\rm gt}=a-1-b$ for B9.04. [Parallel weight in B9.07a][parallel]

<!--
% END GSPH2
-->

## One representation and its spherical polynomials

<!--
% BEGIN GSPH3
-->

<span id="claim:GSPH3"></span>Apply Theorem 2.1.1 to $(\pi,\chi)$ to obtain the continuous semisimple representation $r_0=r_{\ell,\iota}(\pi)$ of $G_E$ in rank $a$. At a finite place $w$, put $K=E_w$, write $q$ for the residue cardinality and $\varpi$ for a uniformizer. If $\pi_w$ is spherical, its normalized Satake multiset $B=\{\beta_1,\ldots,\beta_a\}$ consists of the uniformizer values of its unramified inducing characters. The Satake isomorphism determines their unordered multiset from the character of the spherical Hecke algebra. Local reciprocity in the published theorem sends $\varpi$ to **geometric** Frobenius. Parts (2) and (4) compare the Frobenius-semisimplified parameter of $r_{0,w}$, transported by $\iota$, with the local Langlands parameter of $\pi_w\otimes|\det|_K^{(1-a)/2}$. Since $|\varpi|_K=q^{-1}$, its Weil action is unramified, its monodromy is zero and its geometric-Frobenius eigenvalues are $\alpha_i=q^{(a-1)/2}\beta_i$. For any $h\in W_K$ the arithmetic degree $d(h)$ takes value $1$ on arithmetic Frobenius, so the polynomial is
$$
 P_h(X)=\prod_{i=1}^a (X-\alpha_i^{-d(h)}).
$$
In particular $d=-1$ gives the inverse-arithmetic-Frobenius polynomial of B9.38 and $d=0$ gives $(X-1)^a$. [Satake, Theorem 3][satake-transform] · [Reciprocity and local Langlands, pp. 509–510][artin] · [Uniqueness of the Satake multiset in Lean][satake]

For $w\nmid\ell$, part (2) identifies the Frobenius-semisimplified Weil–Deligne parameter of $r_{0,w}$ with this parameter. Frobenius semisimplification preserves the inertia action and the monodromy operator. In the passage from a Weil–Deligne representation back to an $\ell$-adic representation, inertia acts by its finite Weil action times the exponential of a scalar multiple of monodromy. Here both factors are the identity. Thus $r_{0,w}$ itself is unramified, and its inverse Frobenius has the stated polynomial for every lift. Almost all finite places are spherical and only finitely many divide $\ell$, giving weak attachment. [Theorem 2.1.1(2)][theorem] · [Weak attachment and Frobenius in Lean][weak]

<!--
% END GSPH3
-->

<!--
% BEGIN GSPH4
-->

<span id="claim:GSPH4"></span>For $w\mid\ell$, a spherical vector is fixed by $\mathrm{GL}_a(\mathcal O_K)$ and hence by its Iwahori subgroup. Part (4) applies at this very place. It gives crystallinity and the same normalized Weil–Deligne parameter. Part (3) gives de Rham comparison with the jumps just computed. This works for each spherical $w$ even when $\pi$ has level at another place above $\ell$ or $K/\mathbb Q_\ell$ is ramified. In rank one take the idèlic norm on $E$, polarized by the square of the norm on $F$ times the quadratic character of $E/F$. This character of the extension is odd at each real place and trivial on norms. Here $\beta_1=q^{-1}$ and the infinitesimal weight is $1$. Its cyclotomic realization has geometric-Frobenius root $q^{-1}$ in the Weil parameter and filtration jump $-1$, fixing both signs in this example. [Theorem 2.1.1(3)–(4)][theorem]

<!--
% END GSPH4
-->

## The choice of period comparison

<!--
% BEGIN GSPH5
-->

<span id="claim:GSPH5"></span>Fix a prolongation at $w\mid\ell$ and any bridge inducing it. The bridge embeds the completion $K$ in $\overline{\mathbb Q}_\ell$ and identifies the decomposition group with its local Galois group through that embedding. Work over a finite coefficient field $L$ for $V=r_{0,w}$ enlarged to contain the images of $K$. For a compatible period datum $P$, the ties of B9.06 give Galois-equivariant isomorphisms from its crystalline and de Rham rings to Fontaine's rings. They preserve $\mathbb Q_\ell$, commute with crystalline Frobenius and preserve each de Rham filtration step. Tensor each with the identity on $V$ and take $G_K$-invariants. This identifies the two computations of $D_{\rm cris}(V)$ and of the filtered $D_{\rm dR}(V)$, including their ranks. [Ties required in B9.06][ties] · [Period-ring identifications in Lean][period] · [Local bridge in Lean][bridge]

For the embedding labels, the de Rham identification sends each algebraic scalar $x$ to its lift in $B_{\rm dR}^+$ reducing under $\theta$ to $x$. Such a lift as a root of its minimal polynomial is unique. Two roots with this residue have difference times a unit equal to zero, since the derivative at $x$ is nonzero in the residue field $\mathbb C_\ell$. Thus the identification respects the action of $K$. On splitting $K\otimes_{\mathbb Q_\ell}L$ into its embedding factors it preserves each factor and its graded dimensions. For any local embedding the label $\tau$ in the jump formula is its restriction to $E$ through the bridge.

For the Weil polynomial, let $K_0$ be the maximal unramified subfield of $K$ and let $f=[K_0:\mathbb Q_\ell]$. On crystalline invariants the Weil action at $h$ is $\varphi^{-f d(h)}$ on a coefficient component. Indeed the Galois factor in the period action fixes these invariants and the correcting Frobenius power is $-f d(h)$. The isomorphism of crystalline rings intertwines $\Phi=\varphi^f$. Even a change of identification of $K_0$ only permutes components of $K_0\otimes_{\mathbb Q_\ell}L$. The invertible $L$-linear Frobenius $\varphi$ cycles these components and intertwines the restrictions of $\Phi$, so their characteristic polynomials agree, also for inverse powers. Consequently every compatible datum and inducing bridge gives $P_h(X)$ after applying $\iota$. The argument applies at each prolongation, since the decomposition groups at two prolongations are conjugate and the local embeddings are transported with them. [Weil action on period invariants in Lean][weil] · [Fontaine's construction of the Weil–Deligne parameter][fontaine]

<!--
% END GSPH5
-->

## Why the statement holds for every weak attachment

<!--
% BEGIN GSPH6
-->

<span id="claim:GSPH6"></span>Let $r$ be any other weakly attached representation. Outside the union of the exceptional sets for $r$ and $r_0$, both are unramified and both have the same inverse-Frobenius polynomial by uniqueness of the Satake multiset. Their traces agree on these conjugacy classes. Chebotarev density, followed by continuity of the traces, gives equality on $G_E$. Brauer–Nesbitt over $\overline{\mathbb Q}_\ell$ identifies the two semisimple representations. Restricting the global isomorphism to each decomposition group transports the inertia action, the filtered comparison and the Weil polynomials. This proves B9.38 over every CM field, including the fields used in the descent at ramified places. The ramified comparison then gives B9.05–06 for the same $r$ and the same $H_\tau$. The Roadmap's odd-rank approximation and two stable-range lifts give a different construction of the spherical representation. [Ramified comparison on this representation](RAMIFIED_LOCAL_COMPARISON.md) · [Roadmap's construction of B9.38][construction] · [Even-rank subtraction](../../../publication/full/even-rank-attachment.md)

<!--
% END GSPH6
-->

[theorem]: https://annals.math.princeton.edu/wp-content/uploads/annals-v179-n2-p03-p.pdf#page=38
[weights]: https://annals.math.princeton.edu/wp-content/uploads/annals-v179-n2-p03-p.pdf#page=36
[conventions]: https://annals.math.princeton.edu/wp-content/uploads/annals-v179-n2-p03-p.pdf#page=10
[satake-transform]: https://www.numdam.org/articles/10.1007/BF02684781/
[artin]: https://annals.math.princeton.edu/wp-content/uploads/annals-v179-n2-p03-p.pdf#page=9
[input]: https://github.com/rh-lean-roadmap/rh-lean-roadmap/blob/c7755c1086f05d0918ee8496d95912e4f35e22f9/docs/src/book/main.tex#L24578-L24604
[parallel]: https://github.com/rh-lean-roadmap/rh-lean-roadmap/blob/c7755c1086f05d0918ee8496d95912e4f35e22f9/docs/src/book/main.tex#L24629-L24638
[ties]: https://github.com/rh-lean-roadmap/rh-lean-roadmap/blob/c7755c1086f05d0918ee8496d95912e4f35e22f9/docs/src/book/main.tex#L24624-L24627
[spherical]: https://github.com/rh-lean-roadmap/rh-lean-roadmap/blob/c7755c1086f05d0918ee8496d95912e4f35e22f9/docs/src/book/main.tex#L25131-L25136
[construction]: https://github.com/rh-lean-roadmap/rh-lean-roadmap/blob/c7755c1086f05d0918ee8496d95912e4f35e22f9/docs/src/book/main.tex#L60985-L61009
[core]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AbelianVarietyTheory/Definitions/GaloisGeometry/CyclicStrongAtCusp.lean#L75-L96
[satake]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AbelianVarietyTheory/PublishedTheorems/GaloisCohomology%E2%82%82/StrongMultiplicityOne.lean#L61-L76
[weak]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AutomorphicArithmetic/AutomorphicVarieties/AutomorphicForms/BlochKatoSelmerVanishes.lean#L69-L83
[period]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Formalism/LocalRingCardinality/AdicCompletionLocal/LocTied.lean#L11-L36
[bridge]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Formalism/SharpRestriction/LevelLetterCocycles/DataNLoc.lean#L574-L591
[weil]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AbelianVarietyTheory/Definitions/AutomorphicMembership/FiniteDimensionalLetter.lean#L219-L225
[fontaine]: https://www.numdam.org/item/AST_1994__223__321_0/
