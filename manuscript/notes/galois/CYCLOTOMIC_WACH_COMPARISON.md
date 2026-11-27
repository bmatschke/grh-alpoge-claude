# The integral Wach lattice at the cyclotomic roots

Two polynomials detect different parts of the local calculation. The roots below the chosen cyclotomic level control the action of inertia. The roots at that level control the elementary divisors of Frobenius. We construct a single lattice on which both calculations hold. This supplies the comparisons in B8.41ca–cb and the two height inclusions used in B8.41c. [Statements at the formal source's cyclotomic level][wc-stat] · [Level-one application](../../../archive/rounds/v80/continuation_v80/wach.tex)

## The evaluation of the crystal

<!--
% BEGIN WCC1
-->

<span id="claim:WCC1"></span>Let $p$ be prime, $K_0=W(k')[1/p]$ a finite unramified extension of $\mathbb Q_p$, $K'=K_0(\mu_{p^s})$, with $s\ge1$ and $s\ge2$ at $p=2$. Let $O$ be the integers in a finite extension $L$ containing $K'$. Let $T$ be an $O$-free $G_{K'}$-lattice of rank $d$ whose rational representation is crystalline. Put
$$
 S=W(k')[[Z]],\quad q=1+Z,\quad X=q^{p^{s-1}}-1,\quad
 Q=\Phi_{p^s}(q),\quad \varphi(q)=q^p .
$$
Take Witt Frobenius on the constants. Then $\varphi(X)=XQ$. The polynomial $Q$ is Eisenstein in $Z$ over $W(k')$, and evaluation at $q=\zeta_{p^s}$ identifies $S/Q$ with $\mathcal O_{K'}$. The pair $(S,(Q))$ is the cyclotomic prism. For example it is complete for $(p,Q)$ since $Q\bmod p=Z^{p^{s-1}(p-1)}$. Modulo $Q$ one has $\varphi(Q)=p$, giving the prism divisibility condition, and $S/Q$ is $p$-torsion free. A map to the Fontaine prism sends $q$ to $[\epsilon^{1/p^s}]$, for a compatible sequence of primitive roots $\epsilon=(1,\zeta_p,\zeta_{p^2},\ldots)$. Then $Q$ maps to $([\epsilon]-1)/([\epsilon^{1/p}]-1)$, a generator of $\ker\theta$. The cyclotomic action on $q$ is $q\mapsto q^{\chi(\gamma)}$.

By Bhatt and Scholze's Theorem 5.6 the underlying $\mathbb Z_p$-lattice has an integral prismatic $F$-crystal $\mathcal E$. Full faithfulness lifts multiplication by $O$ and every equivariant morphism, preserving products and compositions. Its value $M$ on $S$ is finite projective, hence free since $S$ is local. The idempotents of $O\otimes_{\mathbb Z_p}W(k')=\prod_{i:W(k')\hookrightarrow O}O$ split it into modules $N_i$ over $A=O[[Z]]$. Each is finite over $A$. Multiplication by $Z$ is injective on $M$, and $N_i/ZN_i$ is a summand of $M/ZM$. The latter is $p$-torsion free, so each summand is finite free over the DVR $O$. Lift a basis to $N_i$. Nakayama gives generation. Reducing a relation modulo $Z$ forces each coefficient to be divisible by $Z$. Cancel $Z$ and repeat. The intersection of its powers in $A$ is zero, proving freeness.

Write $A_*=\prod_i A$ and $B=(A_*[1/Z])^\wedge_p$. Modulo $p$ the localizations at $Z$ and $Q$ agree, and they agree modulo every $p^n$ because a unit lifts through a nilpotent ideal. Wu's Theorem 5.2 and Corollary 5.8 identify this completed étale evaluation with the cyclotomic $(\varphi,\Gamma)$-module of $T$. Here the residue field is perfect, $K'/K_0$ is totally ramified and the tower is $K'(\mu_{p^\infty})$. Its tail is the same cyclotomic tower over $K_0$. In Wu's coordinate with $q$ mapped to $[\epsilon]$, the ideal is $(\varphi^{s-1}([p]_q))$ with $[p]_q=1+\cdots+q^{p-1}$. The inverse Frobenius shift on the perfect Witt target carries its evaluation to the map above, with the corresponding shift on the unramified constants. The Frobenius isomorphism after étale base change identifies the two descriptions. In particular extension to $O\otimes W(C^\flat)$ gives $T\otimes_{\mathbb Z_p}W(C^\flat)$ with Frobenius on the Witt factor, where $C$ is the completed algebraic closure. This gives rank $d$ on each component. The crystal gives an isomorphism $\Phi_i:\varphi^*N_{i-1}[1/Q]\simeq N_i[1/Q]$, with $i-1$ the Frobenius predecessor. All the maps just used respect equivariant lattice maps. [Bhatt–Scholze, Theorem 5.6][wc-bs] · [Wu, Example 3.4, Theorem 5.2 and Corollary 5.8][wc-wu]

<!--
% END WCC1
-->

## The lower roots and the integral action

<!--
% BEGIN WCC2
-->

<span id="claim:WCC2"></span>Fix $\gamma\in\Gamma$ with $a=\chi(\gamma)$ and $v_p(a-1)=s$. Evaluation at $Z=0$ gives a morphism $(S,(Q))\to(W(k'),(p))$ over $\mathcal O_{K'}$, since $Q(0)=p$ and the induced map of quotients is residue reduction. This morphism is unchanged after applying $\gamma$. Crystal base change and its composition law identify the two induced actions on the value at the target. Thus $\gamma$ acts trivially on $M/ZM$, including each coefficient summand.

At $q=\zeta$, for $\zeta^{p^{s-1}}=1$, let $t_\zeta=\log(q/\zeta)$ in the characteristic-zero Taylor ring $L[[t_\zeta]]$. The parameter transforms as $\gamma(t_\zeta)=a t_\zeta$. At $1$, write the action in an integral frame after completion as $v(t)\mapsto G(t)v(at)$, with $G(0)=1$. Solve $H(t)=G(t)H(at)$ with $H(0)=1$. In degree $j>0$ the coefficient of $H_j$ on the left after subtraction is $1-a^j$. It is nonzero because the $p$-adic logarithm is injective on $1+p^s\mathbb Z_p$ in the stated range and $\log a\ne0$. The solution is invertible and its columns give a fixed frame. At a lower root of order $p^b$, $1\le b<s$, Frobenius pulls $t_{\zeta^p}$ back to $p t_\zeta$. This is an invertible change of parameter over $L$. Here $Q(\zeta-1)=p$, a Taylor unit, so $\Phi_i$ transports the fixed frame in the predecessor component. Induction reaches every root of $X$.

For $y\in N_i$, the vector $(\gamma-1)y$ has zero value at each lower root in that frame and hence in every integral frame. Divide each coordinate by the distinguished monic $X$ in $O[[Z]]$. The polynomial remainder has degree less than $p^{s-1}$ and vanishes at all $p^{s-1}$ distinct roots in $L$. It is zero. Finally $\gamma(X)=(1+X)^a-1\equiv aX\bmod X^2$. Multiplying out $\gamma(X^jy)$ gives, for every $j\ge0$,
$$
 (\gamma-1)N_i\subset XN_i,\qquad
 (\gamma-a^j)X^jN_i\subset X^{j+1}N_i .
$$
Applying an equivariant map gives the same inclusions on its image, even when that image fails to fill the target lattice. [Lower-root calculation in the Roadmap][wc-low]

<!--
% END WCC2
-->

## Comparing two lattices in the same étale module

<!--
% BEGIN WCC3
-->

<span id="claim:WCC3"></span>Let $R_0=O\otimes_{\mathbb Z_p}W(\mathcal O_{C^\flat})$ and $R_1=O\otimes_{\mathbb Z_p}W(C^\flat)$. Inside $R_1$, the cyclotomic embedding satisfies $B\cap R_0=A_*$. To see this, first reduce modulo a uniformizer $\pi$ of $O$. The inclusions become products of $k[[Z]]\subset k((Z))$ on the source side, with $k=O/\pi$. On the target side $k\otimes_{\mathbb F_p}\mathcal O_{C^\flat}$ is a product of copies of the valuation ring indexed by embeddings of $k$. Every unramified label occurs since embeddings of the residue field of $K_0$ extend to $k$. In the corresponding factor $Z$ maps to $z=\epsilon^{1/p^s}-1$, of finite positive valuation. A Laurent series with first nonzero coefficient in degree $h$ has valuation $h\,v(z)$ there. Its higher terms converge and have strictly larger valuation. This proves both injectivity and the intersection modulo $\pi$. Lift the residue of an element of the intersection to $A_*$, subtract and divide by $\pi$. Injectivity of $R_0/\pi\to R_1/\pi$ keeps the new element integral. Repeat and use $\pi$-adic completeness of $A_*$ and separation of $B$.

A second integrality test concerns a matrix $V$ over $R_1$ satisfying $\varphi(V)=H V H'+Y$ with $H,H',Y$ integral in $R_0$. For $O=\mathbb Z_p$, if the largest residue norm of an entry is $b>1$, the left side has largest norm $b^p$, while the right has norm at most $b$. Thus $\bar V$ is integral. Lift it by integral Teichmüller representatives $V_0$. Substitution of $V=V_0+pV_1$ gives the same equation for $V_1$ with new integral inhomogeneous term $(HV_0H'+Y-\varphi(V_0))/p$. This is integral because reduction on the Witt vectors of the perfect valuation ring has kernel $pW(\mathcal O_{C^\flat})$. Iteration proves the test. For arbitrary $O$ represent multiplication on a $\mathbb Z_p$-basis of $O$ by matrices. Frobenius acts only on the Witt entries. The test on the resulting larger matrices, applied to $1\in O$, recovers integrality of each original entry.

Let $M_1,M_2$ be componentwise free lattices spanning the same $B$-module of $T$ with Frobenius invertible after inverting $Q$. For either lattice write its basis in rows of $U$ in the constant $T$-frame over $R_1$. Clearing the $Q$-denominators of both Frobenius comparisons gives $Q^h\varphi(U)=PU$ and $Q^hU=H\varphi(U)$ for some $h\ge0$, with $P,H$ integral over $A_*$. Write $x$ for the image of $X$. Since $\varphi(x)=xQ$, the matrices $x^hU$ and $x^hU^{-1}$ have Frobenius respectively equal to $P(x^hU)$ and $(x^hU^{-1})H$. The test puts both in $R_0$. The two transition matrices multiplied by $X^{h_1+h_2}$ now lie in $B\cap R_0$. Thus for $e=h_1+h_2$ one has $X^e M_1\subset M_2$ and $X^e M_2\subset M_1$. [Two-sided comparison on the étale realization][wc-uniq]

<!--
% END WCC3
-->

<!--
% BEGIN WCC4
-->

<span id="claim:WCC4"></span>Suppose both lattices have the same ambient $\gamma$ acting trivially modulo $Z$. Each transition matrix has entries of the form $X^{-e}b$, $b\in A$. At the origin a pole of order $j>0$ in the matrix would have nonzero leading coefficient $C$ in $t_1^{-j}$. Intertwining the two actions gives $a^{-j}C=C$ since their matrices at zero are the identity. This contradicts $a^j\ne1$. Regularity then propagates from $\zeta^p$ on the preceding component to $\zeta$ by the Frobenius transition equation, because $Q$ is a Taylor unit at every lower root. The numerator of each entry vanishes to order at least $e$ at each simple root of $X$. The remainder on division by $X^e$ has the same multiplicities and degree less than $e\deg X$, hence vanishes. For $e=0$ the entries were already integral. This applies to the inverse transition too, so $M_1=M_2$. In particular the crystal evaluation is the unique free full lattice with these comparison and action properties inside the given étale module. [Uniqueness in B8.41cb][wc-uniq]

<!--
% END WCC4
-->

## The primitive divisor and the sign of a jump

<!--
% BEGIN WCC5
-->

<span id="claim:WCC5"></span>Write $P_i=\Phi_i(\varphi^*N_{i-1})$. At a primitive root $q=\zeta$ of order $p^s$, fix the embedding label of $K'$ given by $\zeta$ and the chosen coefficient component. Let $D_\zeta$ be its filtered de Rham space, with a jump $u$ meaning $\operatorname{gr}^u D_\zeta\ne0$. We need the relative position of $P_i$ and $N_i$ in their common rational space. Bhatt–Scholze's Construction 6.5 supplies both sides of that comparison. Its unit Frobenius module $M_2$ has completed lattice $D_\zeta\otimes B_{\rm dR}^+$. The modified module $M_3$ has completed lattice $\operatorname{Fil}^0(D_\zeta\otimes B_{\rm dR})$, glued by their identification (5) off the divisor. Their Frobenius map there is the unit-module map. In the proof of Theorem 5.6, the crystal of the specified lattice $T$, after inverting $p$, extends this modified module. Thus this calculation applies to its value after base change along the map to the Fontaine prism in WCC1.

Here is why the unmodified lattice computes the Frobenius **image**. The modification $M_2\rightsquigarrow M_3$ is supported on $I=(Q)$. Its Frobenius pullback is supported on $(\varphi(Q))$. At the primitive point $\varphi(Q)(\zeta-1)=Q(\zeta^p-1)=p$ is a unit after inverting $p$. Hence the pullbacks of $M_2$ and $M_3$ coincide there, and the Frobenius isomorphism of $M_2$ identifies this pullback with the ordinary lattice. In the same frame the target is the filtered modification. This explains the predecessor index on $P_i$.

The completed local ring on the given branch is $L[[t_\zeta]]$. Its map to the corresponding $B_{\rm dR}^+$ preserves the uniformizer order, since with compatible roots the image of $t_\zeta$ is Fontaine's $\log[\epsilon]/p^s$. Equivalently $Q$ maps to a generator of $\ker\theta$ and all other root factors of $Q$ are units at the chosen branch. Coefficients embed through their characteristic-zero lift in $B_{\rm dR}^+$. Varying the compatible roots and unramified embedding checks every branch and coefficient label. Orders of elements and elementary divisors of a matrix over this Taylor DVR are preserved by this map. In a basis $b_j$ adapted to the decreasing filtration with jumps $u_j$, the two extended lattices are generated respectively by $b_j$ and $t_\zeta^{-u_j}b_j$. Indeed the tensor filtration in degree zero pairs a vector of degree $u_j$ with $\operatorname{Fil}^{-u_j}B_{\rm dR}=t_\zeta^{-u_j}B_{\rm dR}^+$. Consequently, if all labelled jumps at this component lie in $[-M_i,h_i]$, $M_i,h_i\ge0$, then at **each** primitive Taylor branch
$$
 Q^{M_i}P_i\subset N_i,\qquad Q^{h_i}N_i\subset P_i .
$$
The same bounds apply to a crystalline quotient with the quotient filtration, by exactness and strictness of the de Rham comparison on crystalline representations. [Bhatt–Scholze, Construction 6.5 and (5)][wc-fil] · [Construction of the crystal of the specified lattice][wc-int] · [Height comparison used by B8.41c][wc-ht]

<!--
% END WCC5
-->

<!--
% BEGIN WCC6
-->

<span id="claim:WCC6"></span>These two inclusions hold over $O[[Z]]$. In bases of $N_i$ and $P_i$ the transition and its inverse belong to $\mathrm{Mat}_d(A[1/Q])$ by WCC1. Entries of either *scaled* transition can therefore be written $c/Q^b$ with $b\ge0$ and $c\in A$. WCC5 shows that $c$ vanishes to order at least $b$ at every primitive root. Divide by $Q^b$ over $O$. Its remainder is a polynomial of degree less than $b\deg Q$ divisible over $L$ by all the distinct root factors to multiplicity $b$, so it is zero. This argument for the two matrices proves the two integral inclusions, with no scalar power of $p$ introduced.

For a line with a common jump $u$ at these embeddings, the stronger equality is $Q^{\max(-u,0)}P_i=Q^{\max(u,0)}N_i$. At each primitive branch both sides equal $t_\zeta^{\max(-u,0)}$ times the ordinary lattice up to a unit. Apply the same two-way division test. At level one, in the unramified application, this gives the signed rank-one assertion of W80N2, including negative and zero jumps. When the source jump bounds are $[-M_i,h_i]$, the integral inclusions for both the source and target are precisely the input for the cokernel argument of B8.41c. [Level-one formulas W80N1–2](../../../archive/rounds/v80/continuation_v80/wach.tex#L12-L64) · [Use in the cokernel calculation][wc-ht]

<!--
% END WCC6
-->

## Primitive jets on the level-one lattice

<!--
% BEGIN WCC7
-->

<span id="claim:WCC7"></span>Take $p\ge5$, $s=1$ and $T$ crystalline over $K_0$ before restriction. Tame $\Delta\simeq\mu_{p-1}$ acts on $q$ by $q\mapsto q^d$. The crystal over $\mathcal O_{K_0}$ pulls back to the one used above by crystalline base change and full faithfulness. Constant term is a morphism of prisms over $\mathcal O_{K_0}$ fixed also by $\Delta$, so $\Delta$ acts trivially on $N_i/ZN_i$. Averaging any integral basis by $|\Delta|^{-1}\sum_{\delta\in\Delta}\delta$ gives a $\Delta$-invariant basis, since the change matrix reduces to the identity modulo $Z$. Put $v=1-p+\sum_{d\in\mu_{p-1}}q^d$. Calculation W80N1 gives $A^\Delta=O[[v]]$ and $v+p$ is a unit times $Q$. For $\chi(\gamma)=a=1+p$, WCC2 gives $(\gamma-1)N_i\subset ZN_i$. On invariant vectors the coefficients of this difference in the averaged basis belong to $O[[v]]$ and vanish at zero. Thus $\nu=(\gamma-1)/v$ acts integrally on $N_i^\Delta$.

At each primitive root put $t=t_\zeta$. Frobenius transports the fixed Taylor frame at the origin to a fixed frame of its **image** $P_i$ at $\zeta$, by $t_1\mapsto p t$. This exhibits $P_i=V[[t]]$ for a constant $L$-space $V$ on which $\gamma$ fixes the frame and substitutes $at$ on coefficients. The possibly different Taylor lattice $N_i$ is $\gamma$-stable. Choose $b$ with $t^bP_i\subset N_i\subset t^{-b}P_i$. On the finite quotient $t^{-b}P_i/t^bP_i$ the eigenvalues $a^j$, $-b\le j<b$, are pairwise distinct across degrees. The projections onto the homogeneous degrees are polynomials in $\gamma$ over $L$ by Lagrange interpolation. Thus $N_i/t^bP_i$ splits into $t^j F_j$ for subspaces $F_j\subset V$ nested by multiplication by $t$. A basis of $V$ adapted to these subspaces writes $N_i$ as a direct sum of $t^{-u}L[[t]]$ in the fixed frame, with the multiset of exponents prescribed by WCC5. This argument specifies a frame in which both the jumps and the cyclotomic action can be read.

On the summand of jump $u$, division by $v$ is regular at the primitive root and $v|_{t=0}=-p$. On the quotient by $t^j$ times that summand, the operator $\nu$ is triangular with diagonal
$$
 c(h-u)=\frac{1-a^{h-u}}p,\qquad 0\le h<j .
$$
For each summand these entries are distinct. Its characteristic polynomial annihilates it. The product over the **set** of exponents $h-u$ annihilates the direct sum, including repeated jumps. For $j=0$ the quotient is zero. Each $c(h-u)$ belongs to $\mathbb Z_p$ even when $h-u<0$. In the unramified situation the jumps at the primitive embeddings extending a fixed label agree by base change. Apply this polynomial to any integral invariant vector. Its Taylor order is at least $j$ at every primitive branch. Monic division by $Q^j$ in the invariant frame gives membership in $Q^j N_i=(v+p)^j N_i$. The quotient by the invariant scalar $(v+p)^j$ is itself invariant. This supplies the primitive-jet annihilator on the same integral module used for residual Sen multiplicities. [W80N4 and its use on primitive jets](../../../archive/rounds/v80/continuation_v80/wach.tex#L91-L125) · [Residual character obstruction](../../../publication/audit/character-obstruction.md)

<!--
% END WCC7
-->

[wc-bs]: https://www.math.uni-bonn.de/people/scholze/PrismaticCrystals.pdf#page=17
[wc-wu]: https://ems.press/journals/dm/articles/8965783
[wc-fil]: https://www.math.uni-bonn.de/people/scholze/PrismaticCrystals.pdf#page=21
[wc-int]: https://www.math.uni-bonn.de/people/scholze/PrismaticCrystals.pdf#page=26
[wc-stat]: https://github.com/rh-lean-roadmap/rh-lean-roadmap/blob/c7755c1086f05d0918ee8496d95912e4f35e22f9/docs/src/book/main.tex#L22116-L22155
[wc-low]: https://github.com/rh-lean-roadmap/rh-lean-roadmap/blob/c7755c1086f05d0918ee8496d95912e4f35e22f9/docs/src/book/main.tex#L54499-L54530
[wc-uniq]: https://github.com/rh-lean-roadmap/rh-lean-roadmap/blob/c7755c1086f05d0918ee8496d95912e4f35e22f9/docs/src/book/main.tex#L54531-L54561
[wc-ht]: https://github.com/rh-lean-roadmap/rh-lean-roadmap/blob/c7755c1086f05d0918ee8496d95912e4f35e22f9/docs/src/book/main.tex#L54582-L54593
