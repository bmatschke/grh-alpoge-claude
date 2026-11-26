# How a Chow form controls the covolume at the required degree

The arithmetic volume comparison gives a lower bound for the mean height of the projective components. To use this in a period one needs the lattice of cusp forms at the prescribed weight, which is a single degree. The coefficient of the component height in that degree can be seen in one determinant. Its remaining polynomial factor has a useful sign after shifting the height by a constant times the degree. The construction of the determinant below is from Kaiwen Jin's Appendix J and Roadmap B8.25e. We retain its exact degrees in the inequality. [Jin's cut determinant](https://github.com/yuiyuiui/Natural-Language-Proof-Generalized-Riemann-Hypothesis/blob/405237610e58ab9d4a9d5d54d9a0548a0c44227c/sections/j-arithmetic-covolume.tex#L1835-L1895) · [Roadmap, component ranks and degrees](https://github.com/rh-lean-roadmap/rh-lean-roadmap/blob/c7755c1086f05d0918ee8496d95912e4f35e22f9/docs/src/book/main.tex#L20250-L20276)

## The power of the Chow form

Fix one nonterminal admissible component on its good cover. Use the birational projective image for weight $u_1$, of dimension $d\ge1$ and degree $\Delta$, and put $T=T_*>d$. The target cusp lattice has rank $v$. Intersect the image with $d$ generic hyperplanes $\ell_1,\ldots,\ell_d$. Their intersection with the image consists of $\Delta$ reduced points $y_j$ in the open locus where all the section identifications hold. A splitting field allows us to speak of individual points. All section lists and polynomial determinants below descend to the original coefficient field. The Chow form $F$ in $d+1$ hyperplanes is the incidence equation for having a common point on the image. With the first $d$ fixed in general position it is a nonzero scalar times $\prod_j\ell(y_j)$ in the last hyperplane $\ell$.

The source uses a resolution of the base ideals with a globally generated moving line and a nef and big adjoint twist. Its degree-zero sections surject onto the fibres at the cut. The Koszul complex on the $d$ cutting sections, together with vanishing of higher cohomology for those adjoint twists, identifies the final step of the jet filtration with the span of products of cutting degree $T-d$ and sections of degree $d$. These hypotheses matter because the embedded image may have a base locus in the original model. Choose $\Delta$ short degree-zero sections $s_i$ whose values form a basis on the cut. For each $|\alpha|=a<T-d$ take
$$
 s_i\ell_1^{\alpha_1}\cdots\ell_d^{\alpha_d}\ell^{T-a}.
$$
Their order-$a$ normal symbols at $y_j$ are the monomial of multi-index $\alpha$ times $s_i(y_j)\ell(y_j)^{T-a}$. Distinct monomials are independent since the cut is transverse. This group has $B=\binom{T-1}{d}\Delta$ columns. Choose $n_d$ further columns from the spanning list of the final filtration step and complete these to $v$ columns with constant short sections of degree $T$. The last two groups are independent of $\ell$. The choices can be kept on a dense open of the first $d$ hyperplanes, by nonvanishing of the pivots. [Base-ideal resolution, adjoint vanishing and the columns](https://github.com/rh-lean-roadmap/rh-lean-roadmap/blob/c7755c1086f05d0918ee8496d95912e4f35e22f9/docs/src/book/main.tex#L51215-L51228)

Write $D$ for their determinant in a fixed basis. In the filtration the symbol blocks are triangular and each normal monomial of degree $a$ contributes a factor $\prod_j\ell(y_j)^{T-a}$. Over the function field of the first $d$ hyperplanes this gives the factor $F^u$, where
$$
 u=\sum_{a=0}^{T-d-1}\binom{a+d-1}{d-1}(T-a),\qquad
 (d+1)u\Delta=B\{T+d(d+1)\}.
$$
For the second identity, use $a\binom{a+d-1}{d-1}=d\binom{a+d-1}{d}$ and sum the two binomial coefficients. The irreducible Chow form is primitive over the coefficient ring of the first $d$ hyperplanes. Gauss's lemma gives $D=F^uG$ in the full polynomial ring. The first $B$ columns have total parameter degree $T$, the next $n_d$ have degree $T-d$, and the others have degree zero. Hence the nonzero cofactor $G$ has exactly
$$
 e(G)=n_d(T-d)-Bd(d+1),\qquad 0\le n_d\le v-B.
$$
This counts the coefficients at the actual target degree. [Factorization and exact cofactor degree](https://github.com/rh-lean-roadmap/rh-lean-roadmap/blob/c7755c1086f05d0918ee8496d95912e4f35e22f9/docs/src/book/main.tex#L51225-L51248) · [Original monomial identities](https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AbelianVarietyTheory/Proofs/DivisorProofs/MonomialCountsDegreeAndWeightedSum.lean#L37-L68)

For a small example of the determinant mechanism, take the line $\mathbf P^1$, $d=\Delta=1$, $T=2$, with the usual sections $X,Y$. Write $\ell_1=aX+bY$ and $\ell=cX+d'Y$. The three columns in degree two are $\ell^2,\ell_1 X,\ell_1 Y$. In the basis $X^2,XY,Y^2$ their determinant is
$$
 \det\begin{pmatrix}c^2&a&0\\2cd'&b&a\\(d')^2&0&b\end{pmatrix}
     =(ad'-bc)^2.
$$
Here $ad'-bc$ vanishes exactly when the two hyperplanes have a common point on the line. The formula gives $u=2$ and $e(G)=0$. The example illustrates the symbol calculation independently of the higher-dimensional cusp data.

## An additive height with a nonnegative cofactor

For a multiform $P_0$ write $h_0(P_0)$ for the normalized sum of its log coefficient maximum in the integral generating frame at finite places and of its log spherical mean in the Petersson metric at infinity. Here “log spherical mean” means the mean of $\log|P_0|$. Let $n_1$ be the size of the frame and $\Lambda\ge1$ bound the norms of its columns at all embeddings. Set
$$
 c=\log(n_1\Lambda)+(1+\log n_1)/2.
$$
Then $h_0(P_0)+c\,e(P_0)\ge0$ for every nonzero multiform of total degree $e(P_0)$. Indeed, fix a nonzero coefficient after substituting the integral frame. At infinity Cauchy's coefficient bound on the unit polydisc incurs $(n_1\Lambda)^{e(P_0)}$. Spherical submean comparing a unit-vector value to the mean of the logarithm incurs at most $e(P_0)(1+\log n_1)/2$ in the logarithm. Summing the coefficient estimate over the places and using the product formula proves the assertion. Nonarchimedean coefficient maxima multiply, and logarithms add on the complex spheres away from zero sets of measure zero. Both $h_0$ and its shifted version are therefore additive on products. [Spherical bound, coefficient norm and additivity](https://github.com/rh-lean-roadmap/rh-lean-roadmap/blob/c7755c1086f05d0918ee8496d95912e4f35e22f9/docs/src/book/main.tex#L51104-L51130)

Put $h'=h_0(F)/((d+1)\Delta)$. The exact cofactor degree gives
$$
 \begin{aligned}
 h_0(D)&\ge B\{T+d(d+1)\}h'-c\{n_d(T-d)-Bd(d+1)\}\\
 &\ge BT h'-c n_d(T-d).
 \end{aligned}
$$
The term discarded is $Bd(d+1)(h'+c)\ge0$, by the same shifted-height bound on $F$. This argument works for either sign of the normalized Chow height $h_Z$. Converting from the spherical convention gives $h'\ge h_Z-(1+\log n_1)/2$. [Chow normalization and column norms](https://github.com/rh-lean-roadmap/rh-lean-roadmap/blob/c7755c1086f05d0918ee8496d95912e4f35e22f9/docs/src/book/main.tex#L51243-L51255)

Let $D_0$ be the **unsquared** normalized degree of the untwisted terminal cusp lattice of this finite-degree calculation. Its name refers to the final weight of this component calculation. The component is an interior layer of the theta tower. Write $P=P_*$, $q=\kappa/T$, $J=dP(q+1)$ and let $\beta$ bound the squared norm cost of multiplication by a unit section. The three groups of columns have norms bounded by $e^J\beta^{T/2}$, $e^{P\kappa}\beta^{(T-d)/2}$ and $e^{P\kappa}$. Their exterior products have coefficients in the determinant ideal at the finite places. Integrating Hadamard's inequality at the infinite places proves $D_0\ge h_0(D)$ minus the sum of the log column bounds. Thus
$$
 \frac{D_0}{B}\ge T h_Z-J-\frac T2(1+\log n_1+\log\beta)
 -\frac{v-B}{B}\left\{P\kappa+(T-d)(c+\tfrac12\log\beta)\right\}.
$$

On these same covers $\log n_1,\log\beta\le P$, $\log\Lambda\le P(q+1)$, $P\ge1$, $TP\le\sqrt b$, $zP\kappa\le b$, and $0\le(v-B)/B\le2z\le1$. Also $d^2Pq\le b/7$ and $d^2P\le b/14$. It follows that $J\le3b/14$, $c+\tfrac12\log\beta\le Pq+7P/2$, and the last brace times $(v-B)/B$ is at most $4b+(7/2)\sqrt b$. Changing to the anchored weight lowers the degree by at most $vC_p(frL_x)^2$, with $(frL_x)^2\le P\le\sqrt b$ and $v/B\le2$. For the original unsquared degree $d_Z$ this proves
$$
 \frac{d_Z}{B}\ge T h_Z-\frac{59}{14}b-(5+2C_p)\sqrt b
                \ge T h_Z-5b .
$$
The last inequality holds beyond a single cutoff since $C_p$ is a family constant and $b\to\infty$. No height of a component occurs in this error. [Norm and size parameters](https://github.com/rh-lean-roadmap/rh-lean-roadmap/blob/c7755c1086f05d0918ee8496d95912e4f35e22f9/docs/src/book/main.tex#L51144-L51154) · [Actual budgets, anchored twist and degree convention](https://github.com/rh-lean-roadmap/rh-lean-roadmap/blob/c7755c1086f05d0918ee8496d95912e4f35e22f9/docs/src/book/main.tex#L51263-L51282)

## Returning to the retained lattice

Write $B_Z=\binom{T-1}{d}\Delta_Z$ for each component. Their weighted mean height $\bar h$ obeys $\bar h\ge-(1-\lambda)c_s-\lambda X-c_c$ for $\lambda=\sum\Delta'_Z/\sum\Delta_Z\in[1-\rho,1]$, by the volume comparison. Its budgets give $T X,Tc_c\le C_{\rm ht}E_p$ and $2T\rho c_s\le C_{\rm ht}E_p$. Sum the finite-degree estimate over components. Since $B_Z\le v_Z$, $b\le E_p$, and the integral component sum embeds in the cover lattice, the cover's squared-norm slope satisfies
$$
 \mu_Y\ge\frac{2\sum_Z d_Z}{\sum_Z v_Z}
       \ge -(5 C_{\rm ht}+10)E_p .
$$
Here the factor two multiplies the finite and infinite terms together. [Component average](NORMALIZED_VOLUME_AND_COMPONENT_SLOPE.md#a-direct-passage-from-component-heights-to-the-slope) · [Height and transfer budgets](https://github.com/rh-lean-roadmap/rh-lean-roadmap/blob/c7755c1086f05d0918ee8496d95912e4f35e22f9/docs/src/book/main.tex#L21627-L21665)

One more sign matters at the change of character type. Put $C_U=5C_{\rm ht}+10$, $C_F=1183$, $M=M_{p,i}$ and $K=P\kappa$. Multiplication by an orbit-separating section and projection by the horizontal character give an injection from the shifted lattice of rank $r$ to a sum of copies of the zero-shift character lattice of total rank $n\le(1+b/K)r$. Its squared operator height is at most $2b$. The saturated image has mean slope at least $t=-M-(C_F+C_U)E_p-2b$. Short integral sections in the character type span the quotient, giving it mean slope at least $-2K$ when it has positive rank. Consequently, with $\theta=1-r/n$,
$$
 \mu_{\rm type}\ge t-\theta(t+2K)\ge -M-(C_F+C_U)E_p-5b .
$$
Indeed $\theta\le b/K$ and $t+2K\le2K-M\le3K$, since $|M|\le K$. Field descent costs at most another $2b$ by the trace-dual different bound. This gives the nonterminal core slope with a single copy of $(C_F+C_U)E_p$. The separate definite calculation supplies the terminal core bound. The orthogonal projection onto the retained lattice loses at most $E_p$ uniformly, and the measured recursive frame gives $\operatorname{lcv}/D_{\rm norm}\le-\mu(\Lambda_{\rm good})$. Thus the fixed-degree estimate applies with the sign required by the prime comparison. [Character injection, quotient and field descent](https://github.com/rh-lean-roadmap/rh-lean-roadmap/blob/c7755c1086f05d0918ee8496d95912e4f35e22f9/docs/src/book/main.tex#L54021-L54034) · [Measured norm and final projection](https://github.com/rh-lean-roadmap/rh-lean-roadmap/blob/c7755c1086f05d0918ee8496d95912e4f35e22f9/docs/src/book/main.tex#L21715-L21759)
