# An all-prime bound for the depth of the target theta weight

On a supplied nonterminal deep cover $Y$, let $(a,N)$ be the theta weight in B8.28, let $c_{\tau i}=a_{\tau i}-a_{\tau,i+1}$, and keep the prescribed integral frames and formal charts. For **every** rational prime $\ell$ the original target depth on $Y$ satisfies
$$
 d_\ell^{1/2500}(a,N)\ \le\ H_\ell=\sum_{\tau,i}i\,v_\ell(c_{\tau i}!).
$$
This gives upper allowance zero for every $\ell>\max_{\tau,i}c_{\tau i}$, including either base prime $g_0,g_1$ in the standing range. At those two primes the separate weight change yields $d_{g_i}^{1/2500}(u_1)\le1$. The construction below proves the local estimate even at ramified primes. The weighted cost of the small blocks fits the prescribed family budget. The [full reference-depth estimate](PERIOD_REFERENCE_DEPTH_BUDGET.md) handles the large blocks under the stated jet and chart comparisons by first removing the common local valuation.

The proof uses the split ray-field cover in B8.25c, the short period basis and integral jet lift of B8.28c,d, the harmonic derivative comparisons in B8.28v and vb, and the [all-frame denominator on the actual row](PEL_ALL_FRAME_DENOMINATORS.md).

## Auxiliary level and weight

Let $e=\lfloor3\log b/\log3\rfloor$, $t=15^{\lfloor e/4\rfloor}$, and $M=t^2$. The full marking contains level $t^4$. The bound $M\ge15^{-2}b^{3\log(15)/(2\log3)}$ gives $M/b^3\to\infty$. The weight bounds give $D\le frU+V$ with $TU\le9b$ and $TV\ll fmb$. Since $m\le r$ and $T\ge(frL_x)^{24}$, we have $D\ll b$. Also $s=\operatorname{rank}_{\mathbf Z}X\le2fm$, $\kappa=\operatorname{rd}(E)^2/(4f)\le b^{2/7}$ and $s^3\ll b^{1/8}$ by $\operatorname{rd}(E)^7\le b$ and $(frL_x)^{24}\le T\le b$. Consequently beyond one family cutoff,

$$
4D+4\le M,\qquad 2D\sqrt s<M,\qquad
2500D^2\kappa s^3\le M,\qquad D<\min(g_0,g_1).
$$

[Actual level and size estimates][size] · [Degree bound][gaps] · [Width bounds][width]

Use the disjoint-column harmonic differential $P$ of B8.28e. For each nonzero gap $c_{\tau i}$ take a separate set of $i$ columns and raise its leading $i$-row minor to power $c_{\tau i}$. The actual weight has enough columns. The mixed Laplacians vanish because conjugate rows use disjoint columns. This integral polynomial has degree $D$. Its full-row factor on the CM type kills every zero boundary Fourier term, giving cuspidal theta derivatives for all characteristics on the finer marking by the same calculation. [Cusp test][cusp] · [Weight and number of columns][weight]

## Theta rules integral at the selected prime

The actual covering field in B8.25c contains the ray class field furnishing the pairing roots of order $M'=g_0g_1 15^e$, hence the specified root of order $t^4$. Its universal half-marking labels the first of the complementary CM summands. The second is its Weil dual with values in $\mu_{t^4}$ by principal polarization. Trivializing that value group by the chosen root gives universal full $t^4$ labels. This works over the generic cover, and the resulting rules are defined over its coefficient field. [Ray field of the constructed cover][field] · [Half-marking and its dual](PEL_MARKED_LEVEL.md)

The symmetric rigidified line $L^M$ gives an involution $\iota$ above $[-1]$ on its theta group fixing central scalars. There is a unique normalized lift $u_x$ above every marked point $x\in A[M]$ satisfying $\iota(u_x)=u_x^{-1}$ and $u_x^M=1$. To see existence fppf-locally, take any lift $u$, put $h=\iota(u)u$ and $k=u^M$, both central. Then $h^M=k^2$. Choose integers $a,b'$ with $2a+Mb'=1$, using oddness of $M$. The scalar $h^{-a}k^{-b'}$ has square $h^{-1}$ and $M$-th power $k^{-1}$, so multiplying $u$ by it gives the desired lift. Its uniqueness follows from coprimality of $2,M$, and therefore it descends. This supplies individual algebraic translation operators; their pairwise products can carry the usual commutator scalars.

On each abelian factor use the translates by $z\in A[t^2]$ of $[t]^*s_0$ in $H^0(L^{t^2})$, where $s_0$ is the framed principal theta generator. Use the cubical rigidification and the level-$t^4$ marking to select torsion lifts. Apply $P(\nabla)$ to the exterior product of $N$ choices at zero and divide by $t^D$. These are the usual theta derivatives at the marked points $tz\in A[t]$. Indeed $[t]\circ T_z=T_{tz}\circ[t]$, and the normalized cube identifies $[t]^*L$ with $L^{t^2}$. Pullback respects the canonical gauge and acts by $t$ on every tangent direction. Compatible torsion-frame choices multiply the readings by roots of unity. Each factor depends linearly on its original theta generator, so the weight has exactly $N$ theta columns. [Full marked theta evaluations](PERIOD_CARRYING_THETA_ORDERS.md) · [Cubical graph line](PEL_THETA_LINE.md)

Fix $g=g_0$ or $g_1$ and $\lambda\mid g$. Then $t$ is a unit at $\lambda$. At any integral frame over $\lambda$, pass to split uniformization. The coefficient of the pullback at index $tx$ has order at least $Q(x)=Q(tx)/M$. Its normalized translates preserve the Fourier lattice with coefficient-order bounds $Q(y)/M$, since shifting the index and changing the cubical torsion frame change both orders by the same amount. All abelian coefficients are integral, so these sections have integral germs. Since $g$ splits completely in $E$, B8.28v(1) applied to those germs and $P$ gives integral canonical derivative values at every original trait above $\lambda$. The all-frame bound gives a common denominator for the finite list at other places. Weak approximation clears it by a scalar which is a unit at $\lambda$. This produces actual global integral target sections with the same $\lambda$-orders. [Unramified harmonic integrality][integral] · [Clearing other places][clear] · [All-frame denominators](PEL_ALL_FRAME_DENOMINATORS.md)

## A small value on each original trait

In the $j$-th column of each $i$-block choose a linear formal coordinate whose differential on the first $i$ tangent vectors is the $j$-th coordinate covector. Such choices exist by saturation of the frame minors. Form their product, using exponent $c_{\tau i}$ at each copy. Its homogeneous degree-$D$ jet kills all lower-order terms of $P(\nabla)$ at the origin. Its principal-symbol value is $\prod_{\tau,i}(c_{\tau i}!)^i$, a $g$-adic unit. B8.28c,d yield a section of the Fourier lattice of $L^M$ on the product whose jet is this jet times a scalar of order at most $D^2\kappa s^3\phi/M\le\phi/2500$. At good reduction the scalar is a unit. [Short period basis and jet lift][jet] · [Principal symbol and factorials][symbol]

Here is the spanning argument for the scalar isogeny. The subgroup $A[t]=tA[t^2]$ is isotropic for the theta commutator of $L^{t^2}$ because multiplying each argument by $t$ takes its value to the $t^2$-th power. Its cardinality $t^{2\dim A}$ makes it maximal isotropic. Pullback along $[t]$ splits the translation extension on $A[t]$. The invariant line is the pullback of the principal section line on the quotient, which $[t]$ identifies with the original abelian variety. Its section $[t]^*s_0$ is primitive in the Fourier lattice. In fact its coefficient at index zero on the abelian quotient is the pullback under $[t]$ of a primitive principal theta coefficient, remaining nonzero on the special fibre by surjectivity. The commutator identifies $A[t^2]/A[t]$ with the characters of $A[t]$. The normalized translates give primitive generators of the character lines because both translation and inverse translation preserve the Fourier lattice. The character projectors over the splitting trait have unit denominator $|A[t]|$. Consequently the interpolating section is an integral linear combination of the translated generators. The same argument applies to the product of $N$ copies. [Integral character projectors and primitive lines][fourier] · [Primitive principal coefficient](PERIOD_CARRYING_THETA_ORDERS.md)

After applying the differential, some rule has order at most $\phi/2500$. The factor $t^{-D}$ and the scalar clearing the other primes are units at $\lambda$. Both the orders and phase scale by ramification, proving the upper bound on all original traits. At a good-reduction frame the selected integral target section therefore has unit value. The weight-change inequality B8.28z then gives $d_g^{1/2500}(u_1)\le1$ on the cover, since its different term vanishes at $g$. [Weight change][change]

## An explicit range of zero target depth

For each rational prime $\ell$ let $H_\ell=\sum_{\tau,i}i\,v_\ell(c_{\tau i}!)$, with $v_\ell(\ell)=1$. Then on the supplied cover

$$
d_\ell^{1/2500}(a,N)\le H_\ell \qquad\text{for every rational prime }\ell .
$$

For $\ell\nmid15$ use the scalar isogeny above. The principal-symbol value in the interpolation argument has order exactly $H_\ell v(\ell)$. At unramified $\ell$ the harmonic integrality lemma gives the lower order zero needed for clearing other denominators.

At the remaining host primes use the precise exponent of the ordered integral connection estimate B8.28vb(b). The host is Galois and conjugation moves every prime over every prime divisor of its conductor, as verified in Claim 3 of B8.28v. For an integral framed chart Claim 4 there supplies the integral parts $\xi^0_{\tau,i}$ of the eigenlifts and their vertical corrections $\psi_{\tau,i}$ in a fractional module $J$, with its classes of residual primes $q$ and signs. It verifies all three opposite-pair vanishing identities. The conjugated $\xi^0$ operators preserve the integral formal chart. Part (a) of B8.28vb identifies the harmonic polynomial evaluation with the ordered-operator evaluation; the contraction vanishes since conjugate embeddings never occur in the same column of $P$. Part (b) puts this evaluation on separated integral germs in $J^\nu$ whenever each monomial of $P$ has $\sum_{b,q}\min(n^+_{qb},n^-_{qb})\le\nu$, where $n^\pm_{qb}$ counts the differentiations of the indicated class and sign in column $b$. For this particular differential **each column is assigned to one embedding**. Its monomials therefore give $\min(n^+_{qb},n^-_{qb})=0$ in every class and column, whatever the place-dependent signs. Taking $\nu=0$ gives $J^0=V$. The evaluated derivative is integral at the ramified prime, with no rounding loss. The theta germs used here are products of the integral germs on their separate copies; the same estimate on any integral germ follows by expanding its finite jet in monomials. [Ordered operator with arbitrary exponent][ordered] · [Host eigenlifts and application][eigen] · [Native chart calculation][native]

For $\ell=3,5$ the actual base system of level $M_0=g_0g_1$ is tame. Use B8.28m with its own two complementary half-level factors and the same polynomial $P$, and pull the resulting integral base cusp section back to the cover. The homogeneous jet above gives $\delta_{M_0}(P;y)\le H_\ell$ by testing the infimum on that jet. The germ of every base generator is integral, and the factor $M_0^{-D}$ is a unit. Thus the same harmonic lower bounds and scalar clearing apply to these base rules. The jet and phase inequalities hold with $M_0\ge b^{16}$. Forgetting the cover level leaves both the trait valuation and phase unchanged. [Tame base derivatives][base] · [Cover pullback][pull]

This gives upper allowance zero at every prime above the largest individual gap, including primes at most $D$ when they exceed that gap. Each original good-reduction frame at such a prime has a unit-valued global integral target section of theta weight. The small blocks in B8.28r already fit the family budget over *all* primes. Indeed their total $\\sum_{\\mathrm{small}} i c_{\\tau i}$ is at most $V$, each gap is at most $J$, and prime factorization gives

$$
 T\\sum_\\ell\\sum_{(\\tau,i)\\,\\mathrm{small}}i v_\\ell(c_{\\tau i}!)\\log\\ell
 =T\\sum_{(\\tau,i)\\,\\mathrm{small}}i\\log(c_{\\tau i}!)
 \\le TV\\log(2J)\\ll fmbL_x.
$$

This fits $O(E_p)$ on the actual family. Thus only the big blocks, which are the CM-type blocks of size $i\\ge k-1$, need a sharper aggregate estimate in this factorial bound. The separate weight changes and intersection comparisons also enter period entry 7. [Small blocks][gaps] · [Family budget][width]

[ordered]: https://github.com/rh-lean-roadmap/rh-lean-roadmap/blob/02a95b4c62db610642af5f278ee5d0d6df87b348/docs/src/book/main.tex#L20962-L21003
[eigen]: https://github.com/rh-lean-roadmap/rh-lean-roadmap/blob/02a95b4c62db610642af5f278ee5d0d6df87b348/docs/src/book/main.tex#L52249-L52306
[native]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/ReciprocityTheory/ReductiveGroups/ArithmeticGeometry/PullbackSections/HolomorphicFamilies/ChartValJ.lean#L31-L158
## The factorial estimate cannot pay for the large blocks

On the original selected first nonterminal layer take a thick CM-type position. Its large-signature block has length $k$. In the source's zero-based row coordinates the entries at $k-2$ and $k-1$ have difference $B_\rho-1$, where $B_\rho\ge b$ at a thick position. Indeed their unshifted entries in the concatenated row are $v_{k-2}=0$ and $-B_\rho$, and the successive row shifts subtract one from the gap. The common additive weight twist drops out of this difference. Equivalently, the uniform cloud and node bounds give a gap at least $b-\eta-2r$, where $\eta,r=o(b)$. In the quotient-weight formula the next position is $k-1<k=p_{\rm sig}$, so the numerator correction is $+2$. Therefore the actual gap $c_{\tau,k-1}$ is at least a fixed positive multiple of $b/T$ eventually. Here $T=T_*$ is the weight-division parameter, $d_{\rm fl}+1\le T$, and the integer part in the quotient costs at most one. These are positions present on the selected family with positive thick density. [Original two row weights and selected thick positions][bigrow] · [Native cloud and node inequalities][nativegap] · [Quotient rule][quotweight]

Put $L_x=\log b=x^\varepsilon$. The selected sizes and the formula for $T$ give $\log T=O(\log x)=o(L_x)$. For $c=c_{\tau,k-1}$ sufficiently large, $\log(c!)\ge\lfloor c/2\rfloor\log(c/2)$. The one block consequently gives
$$
 T\sum_\ell H_\ell\log\ell
 =T\sum_{\sigma,i} i\log(c_{\sigma i}!)
 \ \ge T(k-1)\log(c!)\gg k b L_x.
$$
The required budget is $E_p=f m b L_x\log\log x$. In the original ranges $f=2n_H\ll x^{2+8\varepsilon}$, $m\ll\sqrt{x}$ and $k\gg x^{9/2+10\varepsilon}$, so $k/(fm\log\log x)\to\infty$. Thus even this one realized gap forces the explicit factorial allowance above the budget. The calculation lower-bounds the majorant $H_\ell$ in aggregate. It gives no lower bound on the actual reference depths. Finishing this route requires sharper estimates on the large-block depths, such as control of their variation among frames at the same prime. [Family degree and size ranges][bigsize] · [Required weighted budget][budget]


[base]: https://github.com/rh-lean-roadmap/rh-lean-roadmap/blob/02a95b4c62db610642af5f278ee5d0d6df87b348/docs/src/book/main.tex#L20698-L20713
[pull]: https://github.com/rh-lean-roadmap/rh-lean-roadmap/blob/02a95b4c62db610642af5f278ee5d0d6df87b348/docs/src/book/main.tex#L20690-L20697

[field]: https://github.com/rh-lean-roadmap/rh-lean-roadmap/blob/02a95b4c62db610642af5f278ee5d0d6df87b348/docs/src/book/main.tex#L49668-L49684
[size]: https://github.com/rh-lean-roadmap/rh-lean-roadmap/blob/02a95b4c62db610642af5f278ee5d0d6df87b348/docs/src/book/main.tex#L51518-L51530
[gaps]: https://github.com/rh-lean-roadmap/rh-lean-roadmap/blob/02a95b4c62db610642af5f278ee5d0d6df87b348/docs/src/book/main.tex#L21434-L21449
[width]: https://github.com/rh-lean-roadmap/rh-lean-roadmap/blob/02a95b4c62db610642af5f278ee5d0d6df87b348/docs/src/book/main.tex#L51640-L51655
[cusp]: https://github.com/rh-lean-roadmap/rh-lean-roadmap/blob/02a95b4c62db610642af5f278ee5d0d6df87b348/docs/src/book/main.tex#L20336-L20343
[weight]: https://github.com/rh-lean-roadmap/rh-lean-roadmap/blob/02a95b4c62db610642af5f278ee5d0d6df87b348/docs/src/book/main.tex#L53620-L53632
[integral]: https://github.com/rh-lean-roadmap/rh-lean-roadmap/blob/02a95b4c62db610642af5f278ee5d0d6df87b348/docs/src/book/main.tex#L21028-L21047
[clear]: https://github.com/rh-lean-roadmap/rh-lean-roadmap/blob/02a95b4c62db610642af5f278ee5d0d6df87b348/docs/src/book/main.tex#L20651-L20662
[jet]: https://github.com/rh-lean-roadmap/rh-lean-roadmap/blob/02a95b4c62db610642af5f278ee5d0d6df87b348/docs/src/book/main.tex#L20545-L20569
[symbol]: https://github.com/rh-lean-roadmap/rh-lean-roadmap/blob/02a95b4c62db610642af5f278ee5d0d6df87b348/docs/src/book/main.tex#L51711-L51735
[fourier]: https://github.com/rh-lean-roadmap/rh-lean-roadmap/blob/02a95b4c62db610642af5f278ee5d0d6df87b348/docs/src/book/main.tex#L51731-L51747
[change]: https://github.com/rh-lean-roadmap/rh-lean-roadmap/blob/02a95b4c62db610642af5f278ee5d0d6df87b348/docs/src/book/main.tex#L21588-L21597

[bigrow]: https://github.com/rh-lean-roadmap/rh-lean-roadmap/blob/02a95b4c62db610642af5f278ee5d0d6df87b348/docs/src/book/main.tex#L6216-L6265
[quotweight]: https://github.com/rh-lean-roadmap/rh-lean-roadmap/blob/02a95b4c62db610642af5f278ee5d0d6df87b348/docs/src/book/main.tex#L20201-L20210
[bigsize]: https://github.com/rh-lean-roadmap/rh-lean-roadmap/blob/02a95b4c62db610642af5f278ee5d0d6df87b348/docs/src/book/main.tex#L15245-L15362
[budget]: https://github.com/rh-lean-roadmap/rh-lean-roadmap/blob/02a95b4c62db610642af5f278ee5d0d6df87b348/docs/src/book/main.tex#L51646-L51662
[nativegap]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AbelianVarietyTheory/Proofs/DivisorProofs/EntRCloudSub.lean#L157-L184
