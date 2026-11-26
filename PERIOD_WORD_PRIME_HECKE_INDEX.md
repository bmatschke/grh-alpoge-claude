# The exact Hecke index at the prime of a selected word

Fix a word $u$ in the selected family and its level-zero definite column of rank $k$ as a unitary group. Put $T=T_u$, a rational prime split completely in the CM field $E$. At each of the $f$ selected split factors impose vanishing of the diamond trace. Let $R$ be this simultaneous trace-zero space, let $d_R=\dim_K R>0$ over the coefficient field, and at $w\mid T$ let $M=S_w\cap R$ be its ordinary integral lattice. Here $S_w$ is the column lattice in the original polynomial frames. Write $e_w=v_w(T)$, for the integer-valued valuation of the coefficient DVR $O$. The assertions below use the level-zero class realization, its free coarse classes, and the selected coefficient and neighbor identifications. These are the hypotheses of Chen's comparison on the same column. [Actual coefficient lattices][coef] · [Level-zero column][forms] · [Chen's weight comparison][mix] · [Realization of the final local image][return]

At a selected split factor $v$ seen by $w$, let $\tau$ denote its coefficient embedding, $\lambda=(\lambda_1,\ldots,\lambda_k)$ its dominant column weight and $s_\lambda=\sum_i\lambda_i$. Set $b_v=b_{\rm top}(\tau)=-\lambda_k$ at the selected top positions, where $b_v\ge0$. For any clearing exponent $b_v\ge-\lambda_k$ the same local calculation holds. Let $U_v$ be the unnormalized upward neighbor sum and $G_v=T^{b_v}U_v$. On the indicated column one has
$$
 \boxed{\quad
 \frac{\operatorname{length}_O(M/G_v M)}{e_w d_R}
     =\frac{k-1}{2}+\frac{s_\lambda}{k}+b_v .\quad}                 \tag{1}
$$
For the native exponent the weight term equals $k^{-1}\sum_{i=1}^{k-1}i(\lambda_i-\lambda_{i+1})$. Thus for a constant weight it vanishes. Chen proves an upper bound with full column rank and incidence term $k-1$. We compute the two lengths in Chen's exact sequence separately. [Native top exponent][btop] · [Sign on the eventual family][sign] · [Original comparison by two inclusions][chen]

## Computing the incidence index with polynomial coefficients

Let $B=B_{w,v}$ be the mixed lattice, using the kernel of the residue marking in the indicated coefficient factor and the usual lattice at every other embedding. Write $B_R=B\cap R$. The mixed lattice at an upper neighbor is exactly the ordinary lattice at its lower endpoint when both are written in one frame for their common local lattice. The word group acts by honest transport of values. The up operator on decorated points is the sum of the identity on these values. A rational change of a class representative transports its integral lattice isomorphically and multiplies by the unit level character. These facts give a block description over $O$, as follows. [Native upward and downward operators][ops] · [Chen's two endpoint frames][edge]

Hold fixed all data away from $v$ and take a representative for the common middle lattice $D$ at $v$ (together with its determined lattice in the opposite split factor). In the lower description, an endpoint over $D$ is a nonzero functional $g$ on $W=D/TD$. Its lower kernel is the inverse image of $\ker g$. In the upper description an endpoint is a nonzero $z\in W$: its enlarged lattice is $D+O_{E_v}T^{-1}\widetilde z$, with the unique marking trivial on $D$ sending $T^{-1}\widetilde z$ to one. This depends only on $z$. An edge between the two states occurs exactly when $g(z)=1$. Conversely the middle lattice is recovered as the ordinary lattice of the lower endpoint or the kernel lattice of the upper one. Thus each endpoint occurs in precisely the corresponding middle block in its own description. The other local states glue with these by taking the lattice with the prescribed completions. Requiring the original definite genus causes no further restriction: each local move lies in the split unitary group, with inverse-transpose move on the opposite factor. Equivalently the middle blocks are finite adelic double cosets with the local full lattice stabilizer at $v$.

For this description one may forget the magnitudes of the diamond markings at all other $T$-places, retaining their lines. The rational stabilizer of any resulting middle record is trivial. Indeed its group is finite by definiteness, and its faithful realization at the unchanged large type prime lies in the inverse image of an upper unipotent subgroup. This is a pro-$g_0$ group, and an element of order $g_0$ in rational dimension $2fk$ would require $g_0-1\le2fk$. The selected thresholds give the strict opposite inequality. Hence all the nonzero $z$ and $g$ in a given block really are distinct decorated classes when the other data are fixed. Restoring the other diamond scalars gives independent copies of their regular representations. Their simultaneous trace-zero conditions replace those factors by their integral augmentation lattices. This uses the integral split decomposition into the augmentation lattice and one basis vector, valid in every residue characteristic. [Free coarse classes on the selected word](PERIOD_FULL_REFERENCE_PAIRING.md) · [Integral diamond-orbit decomposition][diamond]

Use the common middle frame for the mixed values at $z$ and for the ordinary values at $g$. In both descriptions the value lattice is the same free $O$-module $C$ throughout this block. This is where the mixed lattice is essential. Coefficients at all other embeddings agree on these neighbors, since only the chosen embedding of the seen split pair can detect its lattice change at $w$. All torsors for changed class representatives can be trivialized on these individual finite sets by using the representatives just described. Equivariance transports back to the original representatives. The level character is trivial on the moving local group. An upper diamond can invert its scalar label. Inversion permutes each punctured line and preserves its augmentation lattice. At the remaining $T$-places the augmented factors act on separate coordinates and can be included in $C$. The integral map $U_v:B_R\to M$ on the block is consequently
$$
     (\mathcal H b)(g)=\sum_{z:\ g(z)=1}b(z)
$$
on the arrays with sum zero on each punctured line, tensored with $C$.

Counting functionals on one or two vectors gives $\mathcal H^t\mathcal H=T^{k-1}I$ on the linewise augmentation space. Indeed the diagonal has $T^{k-1}$ choices, distinct proportional vectors have no common functional of value one, and independent vectors have $T^{k-2}$ choices. The last terms vanish upon summing each line. The domain and target augmentation lattices have identical Gram determinants for the counting metric, since both are the direct sum of the same number of copies of the augmentation lattice of $\mathbf F_T^\times$. Therefore the absolute determinant of each square incidence block of rank $d$ in integral bases is $T^{(k-1)d/2}$. Tensoring with $C$ repeats this determinant for each basis vector of $C$. Summing ranks gives
$$
 \operatorname{length}_O(M/U_v B_R)=e_w d_R(k-1)/2.               \tag{2}
$$
In the archimedean class-sum metric the reverse neighbor sum is the Petersson adjoint on the rational trace-zero column. In the same middle blocks this is transposition with a common coefficient metric on both sides, because rational frame changes are isometries, all fine class measures agree and the level phases have absolute value one. Thus $T^{-(k-1)/2}U_v$ is unitary there. The mixed and ordinary *finite* lattices are what permit the sharper integral assertion (2). [Single-chart incidence identity](PERIOD_BOTTOM_PAIRING_AND_INTEGRAL_TESTS.md#the-integral-inverse-of-the-affine-incidence-matrix-on-one-reduced-chart) · [Spectrum and elementary divisors of this block](PERIOD_WORD_PRIME_INCIDENCE_DIVISORS.md)

## The weight contribution on the trace-zero subspace

Return to the fine class description of a single state. Going from the ordinary to the mixed frame at $v$ changes one basis vector by $T$. Its matrix $A$ has $v_w(\det A)=e_w$ and the mixed coefficient lattice in ordinary coordinates is $\rho_\lambda(A^{-1})C_0$. Unimodular changes preserve the divided-root Weyl lattice $C_0$. In the representation, the ordinary determinant acts on the top exterior power of the coefficient space by exponent $\dim(C_0\otimes K)\,s_\lambda/k$, including any unaffected tensor factors. Indeed a diagonal change has the same total weight in each coordinate by permutation symmetry, and a scalar has weight $s_\lambda$. The least exponent of a one-coordinate torus in a dominant highest-weight representation is $\lambda_k$. Hence $T^{b_v}C_0$ is contained in the mixed lattice and the length divided by the coefficient rank is $e_w(s_\lambda/k+b_v)$.

The mixed change is constant on each entire diamond orbit: rescaling the residue marking by a nonzero scalar fixes its kernel as well as its ordinary lattice. Use the same transport for mixed and ordinary coordinates throughout that orbit. Both integral trace-zero intersections are then obtained by tensoring the two respective coefficient lattices with the same $f$ integral augmentation factors. This shows directly, including the rank normalization, that
$$
 \operatorname{length}_O(B_R/T^{b_v}M)=e_w d_R(s_\lambda/k+b_v).
$$
Adding this to (2) proves (1), since $U_v$ is injective on $R$. This second determinant step distinguishes the actual trace-zero rank from the rank of the larger column used in the upper bound. [Weyl determinant and scalar shift][weyl] · [Original mixed lattice][coef]

## The full word-prime contribution to the source slope

For the product of all selected factors raised to the native power $m$, colengths add, with multiplicity $m$. For integral injective endomorphisms this follows by inserting the intermediate image lattice, irrespective of the order of multiplication. On a seen coefficient place the selected factors correspond bijectively to the top embeddings. At unseen places the prescribed product is empty and its scaling exponent is zero, so the unshifted local image is $M$. Thus for the unshifted source lattice $N^{(0)}$,
$$
 \frac{\operatorname{length}_{O_w}(M/N^{(0)}_w)}{d_R}=
 \begin{cases}
 m e_w\displaystyle\sum_{\tau\ {\rm top}}
       \left(\frac{k-1}{2}+\frac{s_{\lambda_\tau}}k+b_\tau\right)
          &w\text{ seen},\\
 0        &w\text{ unseen}.
 \end{cases}                                                     \tag{3}
$$
The family uses one common embedding on the distinguished imaginary quadratic subfield $K_0$. The seen places are exactly those over the prime $(\varpi)$ of $K_0$, where $\varpi\bar\varpi=T$. Since $K_{0,(\varpi)}=\mathbf Q_T$, their local degrees sum to $[K:K_0]=[K:\mathbf Q]/2$. For $\ell_w=\log \mathrm Nw/[K:\mathbf Q]$ this gives $\sum_{w\ {\rm seen}}e_w\ell_w=\tfrac12\log T$. The amount **subtracted** from the normalized squared source slope by this unshifted index at all places above $T$ is exactly
$$
 m\log T\sum_{\tau\ {\rm top}}
       \left(\frac{k-1}{2}+\frac{s_{\lambda_\tau}}k+b_\tau\right).
$$
This evaluates the unshifted source index. [Native word product and image][image] · [Choice of the same split half][half] · [Top labels][tops] · [Source slope identity][slope]

### The arithmetic shift at the same prime

Write $t$ for the odd tower parameter and $N_i=k+i(t+1)$ for the rank at stage $i$. Let $\lambda^{(i)}_{u,\tau,a}$ be its coefficient weight in position $a$, indexed from $1$ to $N_i$. For each coefficient embedding $\tau$, let $W_{u,\tau}$ be the maximum of $|\lambda^{(i)}_{u,\tau,a}-i(t+1)/2|$ over $0\le i\le m$ and $1\le a\le N_i$, omitting $a=1$ at every stage when $\tau$ is top. Define

$$
 E_{u,T}=2\sum_\tau W_{u,\tau}+fN_m+
          |\mathrm{Top}|\,\frac{(t+1)(m+1)}4 .
$$

Under the native level-prime size identities, each of the $m$ lifting stages contributes $-E_{u,T}$ at a seen $w\mid T$ and zero at an unseen $w\mid T$. Thus the signed shift $s_u(w)$ is $-mE_{u,T}$ on the seen half and zero on the other half. Because $m$ is even and $t$ is odd, $m(t+1)$ is divisible by four and $mE_{u,T}$ is integral. Hence $\lfloor e_ws_u(w)\rfloor=e_ws_u(w)$, including at ramified coefficient places. [Stage ranks][ranks] · [Native maxima and level-prime error][levelerror] · [Sum of the stage shifts][levelshift] · [Integrality][levelinteger]

The signed shift term in the squared-slope identity is therefore $2\sum_{w\mid T}\ell_w\lfloor e_ws_u(w)\rfloor=-mE_{u,T}\log T$. Together with (3), the full contribution of $T$ to the source slope difference $\mu(N_u)-\mu(S_R)$ is

$$
 \boxed{-m\log T\left[
 E_{u,T}+\sum_{\tau\in\mathrm{Top}}
 \left(\frac{k-1}{2}+\frac{s_{\lambda_\tau}}k+b_\tau\right)
 \right].}                                                       \tag{4}
$$

Here $S_R$ is the ordinary trace-zero source lattice and $N_u$ is its Hecke-image lattice with the prescribed fractional-ideal shift. The theta-image and Hermitian pairing indices of the target row, and the comparison of bottom periods for different tuples, remain separate obligations. [Source slope identity][slope]

## The paired Hecke determinant on the terminal theta image

Fix one attained tuple with the constructed rational definite chain, in particular the reference tuple, and fix one split factor $v$ of the word prime. Write $K_i$ for its class-sum theta map from rank $N_i$ to rank $N_{i+1}$, $s=(N_{i+1}-N_i)/2$ for the common half-increment, and
$$
 F=K_{m-1}\cdots K_0,\qquad I=F(R),\qquad d=\dim_K I,\qquad N_m=k+2ms .
$$
The actual up operators satisfy $U_{i+1,v}K_i=T^sK_iU_{i,v}$. The two sums count the same incident pairs with reciprocal stabilizer weights, and their normalized local kernel factors differ by $T^s$. Iteration gives $U_{m,v}F=T^{ms}F U_{0,v}$. Thus $U_{0,v}$ preserves $\ker(F|_R)$, and $A=U_{m,v}|_I$ is conjugate via $F$ to $T^{ms}$ times the endomorphism induced by $U_{0,v}$ on $R/\ker(F|_R)$. These statements apply to the image of the actual chain, of any rank. [Commutation on the marked class sums][img-w4] · [Transport of the original column][img-zero] · [Local normalization of the two moves](PERIOD_LEVEL_PRIME_MATRIX.md) · [Rationality and stability of the stage spaces][img-rat]

At the distinguished complex embedding, $T^{-(k-1)/2}U_{0,v}$ is unitary by the incidence calculation above. Its invariant kernel is carried onto itself in finite dimension, so its orthogonal complement carries the induced unitary quotient operator. Write $D_I=\det_K A$, with determinant one on a zero-dimensional image. Then
$$
                         D_I\,c(D_I)=T^{(N_m-1)d},                 \tag{5}
$$
where $c$ is the field involution in the column data. Indeed the preceding quotient calculation gives $|\sigma_0(D_I)|^2=T^{(2ms+k-1)d}$. The rational chain and the $K$-linear up operator give $D_I\in K$, and the selected coefficient embedding satisfies $\sigma_0(c(a))=\overline{\sigma_0(a)}$. Its injectivity proves (5) as an identity in $K$. Only this embedding needs to realize $c$ as complex conjugation. The field record specifies total complexity and the distinguished compatibility; no CM assertion about the whole coefficient field is needed. A chain known only over $\mathbf C$ gives the absolute-value statement at that embedding. [Coefficient field and its distinguished involution][img-conj] · [The $K$-linear up operator][img-up]

For $z=w,\bar w=c(w)$ over $T$, choose any full $O_z$-lattice $J_z$ in $I_z$. Use signed length $[J:J']_{\rm sgn}=\operatorname{length}(J/(J\cap J'))-\operatorname{length}(J'/(J\cap J'))$. Since $[J_z:AJ_z]_{\rm sgn}=v_z(D_I)$, (5) gives the exact paired index
$$
 [J_w:AJ_w]_{\rm sgn}+[J_{\bar w}:AJ_{\bar w}]_{\rm sgn}
                          =e_w(N_m-1)d .                           \tag{6}
$$
In particular, take the actual image lattice $J_z=F(M_z)$ of the level-zero trace-zero lattice. The same *single* normalized word factor $G_v=T^{b_v}U_{0,v}$ at both places gives $F(G_v M_z)=T^{b_v-ms}A J_z$. The tower length $m$ is even, hence $ms$ is integral. The sum of the corresponding signed lengths $[F(M_z):F(G_vM_z)]_{\rm sgn}$ is therefore $e_w(k-1+2b_v)d$. Each of these identities uses the same tuple and the same factor at both places. The prescribed source product in (3) instead uses an empty product at the unseen place. Equation (6) stops at the terminal definite theta image; passage to the sharp-row lattice or the terminal pairing would require an action compatible with the subsequent lowering and row projection, and identification of its integral image. [Terminal lowering and class-pairing tests][img-lower]

[coef]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Formalism/LocalToGlobal/Columns/CoefCol.lean#L85-L111
[forms]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Formalism/LocalToGlobal/Columns/ColForms.lean#L89-L108
[ops]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Formalism/LocalToGlobal/Columns/ScaledRamifiedLattice.lean#L92-L106
[image]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Formalism/LocalToGlobal/Columns/ScaledRamifiedLattice.lean#L222-L243
[half]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Formalism/LocalToGlobal/Columns/AtTLemmas.lean#L424-L454
[tops]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Formalism/LocalToGlobal/Columns/AtTLemmas.lean#L460-L485
[btop]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Formalism/SharpRestriction/AdmissibleParameterJoins/DIVfromGLo.lean#L152-L162
[sign]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Formalism/SharpRestriction/AdmissibleParameterJoins/DIVfromGLo.lean#L284-L296
[mix]: https://github.com/yyyyychen/RH-Natural-Language-Proof/blob/d4dfb1a282dbf857288e73eb1f546dbfcc5899b8/tex/ramified-column.tex#L148-L209
[edge]: https://github.com/yyyyychen/RH-Natural-Language-Proof/blob/d4dfb1a282dbf857288e73eb1f546dbfcc5899b8/tex/ramified-column.tex#L288-L340
[weyl]: https://github.com/yyyyychen/RH-Natural-Language-Proof/blob/d4dfb1a282dbf857288e73eb1f546dbfcc5899b8/tex/ramified-column.tex#L213-L267
[chen]: https://github.com/yyyyychen/RH-Natural-Language-Proof/blob/d4dfb1a282dbf857288e73eb1f546dbfcc5899b8/tex/ramified-column.tex#L421-L458
[diamond]: https://github.com/yyyyychen/RH-Natural-Language-Proof/blob/d4dfb1a282dbf857288e73eb1f546dbfcc5899b8/tex/ramified-column.tex#L67-L134
[return]: https://github.com/yyyyychen/RH-Natural-Language-Proof/blob/d4dfb1a282dbf857288e73eb1f546dbfcc5899b8/tex/column-orbit-length.tex#L550-L608
[slope]: https://github.com/yyyyychen/RH-Natural-Language-Proof/blob/d4dfb1a282dbf857288e73eb1f546dbfcc5899b8/tex/column-orbit-length.tex#L615-L634
[ranks]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Formalism/LocalRingCardinality/Params.lean#L6-L36
[levelerror]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Formalism/LocalRingCardinality/DataErr.lean#L98-L107
[levelshift]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Formalism/SharpRestriction/Divisibility/WeightDegreeSizes.lean#L887-L901
[levelinteger]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Formalism/SharpRestriction/AdmissibleParameterJoins/DIVfromGLi.lean#L10-L27

[img-w4]: https://github.com/yyyyychen/RH-Natural-Language-Proof/blob/d4dfb1a282dbf857288e73eb1f546dbfcc5899b8/tex/word-period.tex#L192-L214
[img-rat]: https://github.com/yyyyychen/RH-Natural-Language-Proof/blob/d4dfb1a282dbf857288e73eb1f546dbfcc5899b8/tex/terminal-period.tex#L28-L66
[img-conj]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Formalism/LocalToGlobal/Columns/AbelianHostFieldConditions.lean#L84-L107
[img-up]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Formalism/LocalToGlobal/Columns/ScaledRamifiedLattice.lean#L119-L134
[img-lower]: https://github.com/yyyyychen/RH-Natural-Language-Proof/blob/d4dfb1a282dbf857288e73eb1f546dbfcc5899b8/tex/terminal-period.tex#L80-L155

[img-zero]: https://github.com/yyyyychen/RH-Natural-Language-Proof/blob/d4dfb1a282dbf857288e73eb1f546dbfcc5899b8/tex/word-period.tex#L225-L235
