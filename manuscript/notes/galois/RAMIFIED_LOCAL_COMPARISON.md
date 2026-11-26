# The local Galois comparison at ramified places

The cohomological window uses one global Galois representation at many finite places. The spherical attachment theorem B9.38 over CM fields follows from Theorem 2.1.1 of Barnet-Lamb, Gee, Geraghty and Taylor. Given a polarized cuspidal representation $\pi$ of $\mathrm{GL}_a$ over a CM field $E$, in the weight range of B9.02, it supplies a continuous semisimple $\ell$-adic representation $r$ matching the Satake polynomials at almost all places. It also gives the local comparison at every spherical place for **any** such weakly attached $r$, including after a change of CM field. We show how to recover the two ramified comparisons of B9.05–06 for this same $r$. A spherical component has a vector fixed by the standard maximal compact subgroup. Its Satake roots record its unramified Hecke data. [Derivation of B9.38](SPHERICAL_GALOIS_ATTACHMENT.md) · [Global statement and local tests][local-tests] · [Spherical theorem][spherical]

Fix a place $w$, a prolongation to the algebraic closure, and $\iota:\overline{\mathbb Q}_\ell\simeq\mathbb C$. Put $K=E_w$, let $p$ be its residue characteristic, and write $W_K$, $I_K$, $P_K$ for the Weil, inertia and wild inertia groups. The degree of arithmetic Frobenius is $1$. Local reciprocity $b_K:W_K\to K^\times$ sends geometric Frobenius to a uniformizer modulo units. For any weak local correspondence $R$ of B9.47 let
$$
 \sigma=\pi_w\otimes|\det|_K^{(1-a)/2},\qquad y=R(\sigma)=(\rho_y,N_y).
$$
Write $x=(\rho_x,N_x)$ for the Frobenius-semisimplified Weil–Deligne parameter of $r_w$. At $p=\ell$ we form it with the specified period comparison once potential semistability is established. The two implications concern $N_y=0$.

* **Toral test.** If $\rho_y([g,h])$ has characteristic polynomial $(X-1)^a$ for every $g,h\in W_K$, then $x\simeq y$.
* **Full tame test.** Assume $K\simeq\mathbb Q_p$ as a topological field and either $a=1$ or $p>16a^2$. Suppose each element of $P_K$ has polynomial $(X-1)^a$ on $y$, and for every lift of a topological generator of $I_K/P_K$ each repeated root $z$ satisfies $z^{p-1}=1$. Then $N_x=0$ and $\rho_x(t),\rho_y(t)$ have the same characteristic polynomial for every $t\in I_K$.

At $p\ne\ell$ the rank requirement at every place already follows from $\dim r=a$ and the rank law for $R$. At $p=\ell$ either test also gives potential semistability and the de Rham jumps $H_\tau$ at each induced embedding $\tau$. B9.38 supplies the separate crystalline assertion at spherical places. We follow the Roadmap's element-by-element descent. For the tame base change we use the published formula for level-zero supercuspidals. [Descent in B9.07][assembly] · [Weak local correspondence and type law][weak-law]

## Choosing a CM lift that stays cuspidal

<!--
% BEGIN GRLC1
-->

<span id="claim:GRLC1"></span>We will prescribe a finite abelian extension $L/K$ as the completion of a CM extension $M/E$. We need a cuspidal lift $\Pi$ to $M$ to which $r|_{G_M}$ is weakly attached. A cyclic base change of a cusp form can cease to be cuspidal when the form is isomorphic to its twist by a nontrivial character of the cyclic extension. The trace of $r$ lets us exclude this at every step.

At the start of a tower over a CM field $D$, choose an open normal subgroup $H\subset G_D$ on which $\operatorname{tr}r$ never vanishes. Such a subgroup exists by continuity since $\operatorname{tr}r(1)=a$. Let $D_1$ be its fixed field. In a finite Galois extension of $D^+$ containing $D_1$, choose generators of the subgroup fixing $D$. By Chebotarev we can represent each generator by a Frobenius at a fresh prime of $D^+$ with a chosen prime above it. These primes split in $D$. Require that they also split completely in the totally real abelian extension $F'/D^+$ we are about to choose. Then every generator fixes $D_1\cap DF'$ pointwise, because that prime splits completely in $DF'$ and is unramified in $D_1$. Hence $D_1\cap DF'=D$.

To make $F'$, prescribe a local abelian extension at the target and splitting at those auxiliary primes and at the real places. Take generators of the character group of the desired local Galois group. For each generator, Wang's Theorem 2.2 extends the corresponding local character to an idèle class character of $D^+$ trivial at the prescribed split places. In the exceptional case its global order may double, while its local character is still the prescribed one. The compositum of the character fields has precisely the requested completion, since the intersection of the local kernels is the local norm group.

If the target place of $D^+$ is nonsplit in $D$, first prescribe the quadratic completion $D_w/D^+_v$ itself. In $DF'$ the target then splits over $F'$ and its completion is still $D_w$. Repeat the construction over this new CM field, choosing a fresh trace subgroup, to prescribe $L/K$. For an initially split place only the latter construction is needed. Normality of the local extensions identifies the completions inside the chosen local closure. [Wang, Theorem 2.2][wang] · [Roadmap B9.38b and the auxiliary split primes][global-lift]

Factor each abelian extension $DF'/D$ into cyclic steps of prime degree. Disjointness from $D_1$ makes $H$ surject onto $\operatorname{Gal}(DF'/D)$. Thus at any intermediate field $D'$ the subgroup $H\cap G_{D'}$ still surjects onto the Galois group of the next step. A self-twist by a nontrivial step character $\omega$ would give
$$
 \operatorname{tr} r(\gamma)=\omega(\gamma)\operatorname{tr} r(\gamma)
 \qquad(\gamma\in G_{D'}).
$$
Indeed weak attachment gives this identity at good Frobenius elements and density gives it everywhere. Take $\gamma\in H\cap G_{D'}$ with $\omega(\gamma)\ne1$ to get a contradiction. Arthur and Clozel's Theorems III.4.2(a) and III.5.1 now give a cuspidal lift with the stated local base change. One applies their unitary statement after a norm twist and restores that twist by norm pullback. At good places of residue degree $f$ both the Satake roots and the inverse-Frobenius roots are raised to the $f$th power, including the factor $q^{(a-1)/2}$. Restriction to a finite-index normal subgroup preserves semisimplicity. This proves weak attachment for the next step and completes the induction. Strong multiplicity one carries the polarization with its norm-pulled character, and the infinitesimal weights at a complex embedding are those at its restriction to the lower field. [Arthur–Clozel, Chapters I and III][ac] · [Pinned formal construction of the lift][lean-lift]

<!--
% END GRLC1
-->

## Recovering the toral parameter

<!--
% BEGIN GRLC2
-->

<span id="claim:GRLC2"></span>The segment law for $R$ assigns a nonzero monodromy operator to a segment of length greater than one. Thus $N_y=0$ leaves only singleton segments. A local component of a cuspidal representation of $\mathrm{GL}_a$ is generic, so these singletons are unlinked. This means that no two support terms differ by the twist $|\det|_K$. Every commutator belongs to inertia. Its image under $\rho_y$ has finite order, so the toral test makes it the identity. Each irreducible cuspidal parameter therefore factors through an abelian group and has dimension one. The rank and character laws of $R$ give smooth characters $\xi_1,\ldots,\xi_a$ in the support of $\sigma$ with
$$
 y=\bigoplus_{j=1}^a(\xi_j\circ b_K,0).
$$
The following argument applies whenever the normalized support consists of unlinked characters. [Segment and character laws][weak-law] · [Zelevinsky, Theorems 4.2 and 9.7][zel] · [Support under the two local tests][support]

Fix $g\in W_K$ of nonzero degree. Let $U$ be the intersection of the kernels of the $\xi_j$ on $\mathcal O_K^\times$ and put $J=U\langle b_K(g)\rangle$. The valuation of $b_K(g)$ equals $-\deg_K g$. Thus $J$ is open of finite index in $K^\times$ and $J\cap\mathcal O_K^\times=U$. By local class field theory the extension $L/K$ with norm group $J$ satisfies $g\in W_L$. Each $\xi_j\circ N_{L/K}$ is unramified since norms of units lie in $U$. Realize this $L$ by the cuspidal CM lift just constructed. The choice of $L$ can depend on $g$.

The local lifting rule of Arthur and Clozel takes a Langlands quotient to the quotient for its lifted inducing data. On characters this is composition with the norm. It remains to check that these unramified characters induce irreducibly. Up to one common norm twist the lower local component is unitary, as it is a component of a cuspidal automorphic representation. In Tadić's Theorem D, any block of segment length greater than one or with more than one consecutive shift contributes two adjacent cuspidal twists to its support. Unlinking excludes both. The remaining unitary cuspidals have real shifts $0$ or $\pm e$ with $0<e<1/2$. After restoring the common twist, all the real exponents thus lie in one open interval of length one. The identity $|N_{L/K}z|_K=|z|_L$ preserves these exponents. No two pulled-back characters are adjacent, so Zelevinsky's irreducibility criterion applies. Their induction has a spherical vector since each is unramified. This argument also explains the use of the exponent bound when two distinct unit characters coincide after pullback. [Arthur–Clozel, I §6.4, pp. 59–60][ac] · [Tadić, Theorem D][tadic] · [Zelevinsky, Theorem 4.2][zel]

If $B$ is the Satake multiset of $\Pi_u$ at the place $u$ with $M_u=L$, its algebraically normalized roots $q_u^{(a-1)/2}B$ are $(\xi_j\circ N_{L/K})(\varpi_L)$. The spherical comparison for the restricted $r$ gives zero monodromy upstairs, away from $\ell$ by unramifiedness and above $\ell$ by crystallinity. Weil–Deligne restriction preserves the vanishing of monodromy in both directions and restricts the Weil action up to Frobenius semisimplification. In particular its characteristic polynomial at $g$ is the downstairs one. Since $b_K(g)=N_{L/K} b_L(g)$ and $\operatorname{ord}_L b_L(g)=-\deg_L g$, we get
$$
 N_x=0,\qquad
 \det(X-\rho_x(g))=\prod_{j=1}^a \bigl(X-\xi_j(b_K(g))\bigr).
$$
In this formula $g$ fixes the chosen completion $L$, so its polynomial has been computed on the element itself. [Formal comparison away from $\ell$][lean-away] · [Formal comparison above $\ell$][lean-above] · [Fontaine, Exposé VIII, §§1–2][fontaine-wd]

It remains to recover inertia from the nonzero-degree comparisons. Choose $\phi$ of degree one and put $P(X)=\sum_{j=0}^a c_jX^j$, the common characteristic polynomial at $\phi$. Its constant coefficient is nonzero. For $t\in I_K$ put $d_j=\operatorname{tr}\rho_x(t\phi^j)-\operatorname{tr}\rho_y(t\phi^j)$. Cayley–Hamilton on $\rho_x(\phi)$, followed by left multiplication by $\rho_x(t)$ and trace, gives the same zero sum as for $y$. Subtract to obtain $\sum c_jd_j=0$. For $1\le j\le a$ the element $t\phi^j$ has nonzero degree, hence $d_j=0$. It follows that $d_0=0$. The traces now agree on the entire Weil group. For a Frobenius-semisimple action with finite inertia, some power of Frobenius centralizes inertia. On each eigenspace of that power one can rescale Frobenius to have finite order. The resulting finite group acts semisimply, hence so does the Weil group. Equality of trace characters in characteristic zero identifies these semisimple representations. Together with $N_x=N_y=0$ this gives $x\simeq y$. [Trace lemma in the pinned Lean source][lean-trace] · [Multiplicity argument in the preceding section](../../../publication/full/even-rank-attachment.md)

<!--
% END GRLC2
-->

## Descent of the tame inertia polynomials

<!--
% BEGIN GRLC3
-->

<span id="claim:GRLC3"></span>Now let $K\simeq\mathbb Q_p$ with the full tame test. The finite image of wild inertia acts trivially, since its elements have all eigenvalues one. As before, the singleton cuspidal terms of $\sigma$ have irreducible parameters. To apply a published base-change formula one must identify its parameter with the one assigned by the particular weak map $R$.

For an irreducible tame Weil representation $T$ of rank $d$, diagonalize the finite cyclic image of tame inertia. Frobenius permutes the eigenspaces transitively by irreducibility. If the orbit length is $h$, choose an eigenvector for the $h$th power of Frobenius in one of the spaces. Its Frobenius translates span an invariant subspace of dimension $h$, so $h=d$ and each space is a line. In this cyclic basis a fixed geometric Frobenius $\Phi$ takes the last vector to $(-1)^{d-1}\det T(\Phi)$ times the first. Its determinant and the inertia orbit therefore determine $T$.

Let $K_d/K$ be unramified of degree $d$. The depth-zero parametrization realizes $T$ by a supercuspidal $u_0$ with a regular residue character of $\mathbb F_{p^d}^\times$. More precisely, for a tame character $\theta$ of $K_d^\times$ with that regular reduction, the classical parameter of $u_0=\pi_d(\theta)$ is
$$
 \operatorname{Ind}_{W_{K_d}}^{W_K}
       \big((\Delta_d^{\,d-1}\theta)\circ b_{K_d}\big),
$$
where $\Delta_d$ is the unramified quadratic character of $K_d^\times$. Every irreducible tame $T$ occurs. [Yang, §§3.3–4.3][yang]

The finite type of $u_0$ is the Green cuspidal labelled by the reduction of $\theta$. Hence B9.49 gives $R(u_0)$ the same inertia orbit. Evaluate on $I_{K_d}=I_K$ at the residue of $b_{K_d}(t)$ and take the $d$ Frobenius conjugates. The auxiliary global place in that type law can be obtained by the construction above with completion $K_d$. It has residue degree $d$ over $\mathbb Q_p$ and uniformizer $p$. The determinant law for the good class $u_0$ reads its central character at $b_K(\Phi)$, just as in the classical correspondence. The cyclic-basis calculation gives $R(u_0)=T$. If $T=R(u)$ came from a support term $u$, the injectivity clause of B9.47 with the good preimage $u_0$ gives $u=u_0$. For $d=1$ this comparison follows from reciprocity. This identifies every summand of $y$ with its classical parameter. The repeated-root test also explains the separation in the formal proof. A repeated inertia orbit of length $d>1$ would give a repeated eigenvalue at a tame generator outside the $(p-1)$st roots of unity. [Weak injectivity and type law][weak-law] · [Henniart, §1.3(i)][henniart] · [Roadmap B9.55a][support]

Take $L/K$ unramified of degree $a!$ and globalize it as above. For each $d$ in the support, $d\mid a!$, so $W_L\subset W_{K_d}$. The restriction of the displayed induced representation to $W_L$ splits into the $d$ conjugates of its inducing character restricted to $W_L$. Explicitly, on units the characters of $L^\times$ have values
$$
 z\longmapsto\overline\theta\bigl(
      N_{\mathbb F_{p^{a!}}/\mathbb F_{p^d}}(\bar z)^{p^i}\bigr),
       \qquad 0\le i<d .
$$
On the common uniformizer $p$, each has value $\big((-1)^{d-1}\theta(p)\big)^{a!/d}$, since $N_{L/K_d}(p)=p^{a!/d}$. Yang's Proposition 5.1 gives these characters as the base change of $u_0$. Equivalently, Henniart's cyclic restriction formula for cuspidal support applies along the prime-degree steps of the tower. The normalization by $|\det|^{(1-a)/2}$ commutes with these norm pullbacks. Thus the normalized support of $\Pi_u$ is the entire list of characters read by $y|_{W_L}$, with multiplicities. [Yang, Proposition 5.1 and (5.3)–(5.5)][yang] · [Henniart, §7.2, Property 1][henniart] · [Construction compared in B9.38d][tame-lift]

The exponent argument above applies to the original unlinked cuspidal terms in every rank. For a unitary cuspidal term its Weil parameter has unitary determinant, and a power of Frobenius centralizing inertia acts by a scalar by irreducibility. That scalar has modulus one. Its restriction therefore contributes characters of real exponent zero before the corresponding norm twist is restored. All the upper character exponents are again in one open interval of length one. The upper support is unlinked, so the toral comparison just proved applies to $r|_{G_M}$ at $u$. It gives $x|_{W_L}\simeq y|_{W_L}$ in Frobenius-semisimplified parameters and $N_x=0$. The extension is unramified, whence $I_L=I_K$. Evaluating at $t$ in this common group gives exactly the required inertia polynomial downstairs. For $a\ge2$ an unramified character of order $a!$ is invisible on $W_L$, since its Frobenius has degree $a!$ over $K$. This explains the scope of the inertia conclusion. [Formal statement with its inertia quantifier][lean-tame]

<!--
% END GRLC3
-->

## The filtered comparison above the coefficient prime

<!--
% BEGIN GRLC4
-->

<span id="claim:GRLC4"></span>Fix $w\mid\ell$ and any of the period data and bridges permitted in B9.06. Use their specified identifications with the crystalline and de Rham rings, preserving Frobenius, filtration and the chosen local embedding. An embedding for $K$ extends over each finite $L$ in the chosen closure. Restrict the decomposition-group action with this embedding. In the toral argument one of the fields chosen for $\phi$ already gives a crystalline restriction. In the tame argument the restriction to the unramified lift is potentially semistable by the toral case. Either gives potential semistability over $K$. In the Weil–Deligne construction on a common semistable extension, restriction keeps the monodromy operator and restricts the descent action. This justifies the polynomial comparisons for the originally chosen bridge. [Fontaine, Exposé VIII][fontaine-wd] · [Restriction for the chosen bridge in Lean][lean-above]

For the filtration, pass to a finite Galois extension $L'/K$ containing the upper comparison field and large enough for semistability. The filtered space $D_{\rm dR,L'}(r)$ has semilinear Galois action. Its invariants are $D_{\rm dR,K}(r)$ by the definition using $B_{\rm dR}$. Galois descent on each filtration step gives $\operatorname{gr}^i D_{\rm dR,L'}(r)=L'\otimes_K\operatorname{gr}^i D_{\rm dR,K}(r)$ and the full de Rham dimension downstairs. After splitting the coefficient embeddings, the dimension at an embedding extending $\tau$ is the downstairs dimension at $\tau$. Scalar extension from the upper comparison field to $L'$ preserves these dimensions as well. The infinitesimal weights on that comparison field are the pullbacks of the original ones, so its jumps give precisely $H_\tau=\{(a-1)/2-z\}$ with $z$ running over those weights, counted with multiplicity. The initial choices of prolongation, correspondence and compatible bridge were arbitrary. [Fontaine, Exposé III, §5.6][fontaine-dr] · [Embedding-by-embedding descent in Lean][lean-jumps]

<!--
% END GRLC4
-->

<!--
% BEGIN GRLC5
-->

<span id="claim:GRLC5"></span>With $r$ from B9.38, take $w_{\rm gt}=a-1-b$ and $H_\tau$ from B9.04 and B9.07a. Away from $\ell$ the dimension law holds for each local component, and the toral and full tame arguments give the two conditional conclusions. Above $\ell$ the spherical, toral and full tame cases give the corresponding clauses with these same weights. This proves the global assertion B9.02 for every weak local correspondence satisfying B9.47. Its toral clause supplies the polarized attachment used in claim GUA7 for a definite unitary form. The existence of the weak correspondence is the separate input B9.46. [Formal statement of the attachment](https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AutomorphicArithmetic/Foundations/GaloisRepresentations/TypeConditions/WeightsConjBis.lean#L26-L73) · [Use in the unitary assembly](../../../research/modules/galois/galois_assembly_v44/main.tex#L355-L383)

<!--
% END GRLC5
-->

[local-tests]: https://github.com/rh-lean-roadmap/rh-lean-roadmap/blob/c7755c1086f05d0918ee8496d95912e4f35e22f9/docs/src/book/main.tex#L24580-L24627
[spherical]: https://github.com/rh-lean-roadmap/rh-lean-roadmap/blob/c7755c1086f05d0918ee8496d95912e4f35e22f9/docs/src/book/main.tex#L25131-L25147
[assembly]: https://github.com/rh-lean-roadmap/rh-lean-roadmap/blob/c7755c1086f05d0918ee8496d95912e4f35e22f9/docs/src/book/main.tex#L59740-L59758
[weak-law]: https://github.com/rh-lean-roadmap/rh-lean-roadmap/blob/c7755c1086f05d0918ee8496d95912e4f35e22f9/docs/src/book/main.tex#L25303-L25346
[global-lift]: https://github.com/rh-lean-roadmap/rh-lean-roadmap/blob/c7755c1086f05d0918ee8496d95912e4f35e22f9/docs/src/book/main.tex#L61026-L61045
[support]: https://github.com/rh-lean-roadmap/rh-lean-roadmap/blob/c7755c1086f05d0918ee8496d95912e4f35e22f9/docs/src/book/main.tex#L61294-L61304
[tame-lift]: https://github.com/rh-lean-roadmap/rh-lean-roadmap/blob/c7755c1086f05d0918ee8496d95912e4f35e22f9/docs/src/book/main.tex#L61089-L61121
[wang]: https://doi.org/10.1007/s11425-015-4977-5
[ac]: https://www.math.toronto.edu/arthur/pdf/30.pdf
[zel]: https://doi.org/10.24033/asens.1379
[tadic]: https://doi.org/10.24033/asens.1510
[yang]: https://arxiv.org/pdf/1903.11497v1
[henniart]: https://doi.org/10.5802/jtnb.313
[fontaine-wd]: https://www.numdam.org/item/AST_1994__223__321_0/
[fontaine-dr]: https://www.numdam.org/item/AST_1994__223__113_0/
[lean-lift]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AutomorphicArithmetic/Foundations/GaloisRepresentations/SphericalGaloisCompatibility/ToralDeRham/WeaklyAttachedToralOfCmLift.lean#L29-L88
[lean-away]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AutomorphicArithmetic/Foundations/GaloisRepresentations/SphericalGaloisCompatibility/ToralDeRham/ToralGalois2.lean#L22-L56
[lean-above]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AutomorphicArithmetic/Foundations/GaloisRepresentations/SphericalGaloisCompatibility/ToralDeRham/ToralAboveOfHolds.lean#L31-L64
[lean-trace]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AbelianVarietyTheory/Proofs/SatakeParameters/CharPolEqOfDegNeZero.lean#L12-L36
[lean-tame]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AutomorphicArithmetic/Foundations/GaloisRepresentations/SphericalGaloisCompatibility/PAdicSplitting/LocalGlobalCompatAtIwahoriFixedPlaces.lean#L16-L32
[lean-jumps]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AutomorphicArithmetic/Foundations/GaloisRepresentations/SphericalGaloisCompatibility/ToralDeRham/GaloisCompatUnlinkedSupportOfSpherical.lean#L27-L67
