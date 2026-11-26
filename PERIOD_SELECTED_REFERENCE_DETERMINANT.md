# From the fitted quotient to the selected reference determinant

Fix a selected member, a nonterminal layer $j=i+1<m$, its core coefficient field $F$, its sized deep-cover field $F'$, and the row realization field $K$. Both $F'$ and $K$ extend $F$. The argument uses the two extensions separately. All slopes $\mu$ below are normalized squared-Hermitian slopes. A finite-index inclusion $L_0\subset L$ over a field $H$ raises the total squared degree by $2\log\#(L/L_0)/[H:\mathbf Q]$. A norm rescaling by $c$ at every infinite place changes the slope by $-2\log c$. [Selected origin and fields](PERIOD_SELECTED_MARKED_ORIGIN.md) · [Degree and index in the native normalization][degree]

## An exact identity for the reference determinant

Let $B$ be the integral cusp lattice on the deep cover, restricted to the $F'$-span of pullbacks of the **core type subspace** at the original weight. Write $L_0$ for the corresponding integral type lattice on the core. Concretely, the space in question is the span of $\mathrm{typeK}(p.\mathrm{fw},p.F.\mathrm{lv2},i)$, and each integral lattice is the intersection with the integral cusp forms on its own level. Let $L$ be the type lattice in the selected row realization over $K$. Let $e_g$ be the native good projector, orthogonal at all infinite places, and put

$$
 L_g=L\cap\operatorname{im}e_g,\qquad L_b=L\cap\ker e_g,\qquad
 r_t=\operatorname{rk}L=r_g+r_b .
$$

The native marked row has $r_g=D_R>0$. We use its actual Gram, rationality, projector and Petersson comparison laws. [Definitions of these lattices][definitions] · [Selected good rank and basis][reference]

There are two finite indices. With $\pi$ the geometric pullback and $\ell=r_t$, define

$$
 I=\frac{2}{[F':\mathbf Q]\,\ell}
      \log\#\big(B/(\mathcal O_{F'}\pi L_0)\big),\qquad
 J=\frac{2}{[K:\mathbf Q]}
      \log\#\big(L/(L_g\oplus L_b)\big).
$$

The first is a correction *per type dimension*. The second is a total degree. For each infinite place $v$ of $K$, use the source's representative $\sigma_v$. On the embedded core cusp space the row norm is $c_v$ times the core Petersson norm at $\sigma_v|_F$. Put $\bar c=(2/[K:\mathbf Q])\sum_{v\mid\infty}\log c_v$. Finally $n_P$ is the cardinality of the selected reference subgroup of the finite level. Then the covolume of the chosen reference matrix lattice satisfies the identity

$$
 \boxed{\displaystyle
 \frac{\operatorname{lcv}(M_j)}{D_R}
 =-\frac{r_t}{r_g}\big(\mu(B)-I-2\bar c\big)
     +\frac{r_b\mu(L_b)+J}{r_g}-\log n_P .}                 \tag{1}
$$

Interpret $r_b\mu(L_b)$ as zero when $r_b=0$. This formula retains the signs of the change of measure and the reference normalization. It also allows direct measurement of the actual gluing index. [Reference subgroup][refgroup] · [Metric comparison][core] · [Native comparison with the coordinate determinant][coord]

For the proof, pullback preserves Petersson norms for the probability measures, preserves linear independence after scalar extension, and detects integrality of a form defined over $F$. A putative pullback of a core form has the same evaluations on the covering correspondence as its canonical pullback. Subtract the two. A cusp section which pulls back zero in these evaluations vanishes by uniqueness. Applied to linear combinations this identifies the deep rational space used in the definition of $B$ with $F'\pi(L_0\otimes F)$. The trace argument below shows that the index defining $I$ is finite. Extending a Hermitian lattice with its norms preserves normalized degree: norms of determinant ideals acquire the extension-degree power and embeddings above each original embedding repeat with that same multiplicity. Hence $\mu(L_0)=\mu(B)-I$. [Pullback, normalized Petersson norm and integral tests][pull] · [Identification of the pullback span][span]

In the row field the rationality assertion identifies $L$ with the $\mathcal O_K$-span of the image of $L_0$. To see the intersection here, an integral row form over the core field which lies in the selected type subspace is the image of an integral cusp form. Its preimage belongs to the defining core type set. In reverse, the selected type space contains the images of that set and is closed under linear combinations. This proves the equality of the two integral spans for this field extension. On a point with its native row conditions and record tie the integral rationality statement follows from the pinned character values and type-space descent. The scalar $c_v$ changes a rank-$\ell$ Gram determinant by $c_v^{2\ell}$, so $\mu(L)=\mu(B)-I-2\bar c$. Because the two rational summands of $L$ are orthogonal, their Gram determinants multiply. Taking the finite index yields

$$
 r_t\mu(L)=r_g\mu(L_g)+r_b\mu(L_b)+J .
$$

If $g e_g L\subset L$ for the native integer $g=|\mathcal G_p|$, the map $1-e_g$ embeds $L/(L_g\oplus L_b)$ in $g^{-1}L_b/L_b$. Thus $0\le J\le 2r_b\log g$. The cost vanishes when the complementary rank is zero. [Field extension and selected integral span][core] · [Integral row rationality][rat] · [Projector and gluing][glue]

The frame giving $M_j$ is the selected good basis. Its coordinate lattice is the preimage of $L_g$ under the basis map, and its norm is $n_P^{-1/2}$ times the row norm. The rank equality $D_R=r_g$ uses the primitive rows. The coordinate determinant with the transported row norm gives $-\mu(L_g)$ per rank. The displayed scaling changes this by $-\log n_P$, since $K$ is totally complex. This proves (1) with equality in the estimate where the native source discards the nonpositive term. [Actual basis, rank and scaling][reference] · [Determinant under a scalar change][scale]

## The finite descent loss on the sized ray cover

For the cover used here one has

$$
 0\le I\le
 \frac{2}{[F':\mathbf Q]}\log N_{F'/\mathbf Q}\mathfrak D_{F'/F}
 \le 2\log M' \le 54L_x+4,\qquad M'=g_0g_1\,15^e.            \tag{2}
$$

All elementary divisors of $B/(\mathcal O_{F'}\pi L_0)$ are supported above primes dividing $M'$. This last support and the second inequality use the specified ray compositum. The relative-different bound alone works on any good cover with the indicated Galois descent laws. [Ray compositum and field inclusions][ray] · [Depth bound][depth] · [Host prime bounds][hostnum]

For the relative-different bound, the coefficient descriptions of deep sections in the pullback span are stable under $\operatorname{Gal}(F'/F)$. Indeed a linear combination of pullbacks is tested for integrality by evaluating the corresponding combination on the base after coefficient extension. Those tests are invariant under conjugating its coefficients. Consequently $\operatorname{Tr}_{F'/F}(a x)$ belongs to the core type lattice for every $x\in B$ and $a\in\mathcal O_{F'}$. To verify the ideal containment, localize at a prime of $F$ and write $x$ in a local basis of $L_0$. The trace of each coordinate times every integral coefficient is integral. By the defining duality of the codifferent each coordinate belongs to the inverse relative different. This argument uses the semilocal product over primes above the chosen prime, so it bounds each coefficient place. It follows that

$$
 \mathfrak D_{F'/F}B\subset\mathcal O_{F'}\pi L_0\subset B .
$$

The index of the leftmost lattice in $B$ is $N\mathfrak D_{F'/F}^{\,\ell}$, by local freeness over a Dedekind ring. The source's own ideal proof immediately before its relaxation to the absolute different uses this relative ideal. [Conjugation stability of the actual section tests][stability] · [Relative-different argument][different]

For the second inequality of (2) let $H=\mathbf Q(\sqrt{-d})$. The base coefficient field contains $H$ by its field pin, and $F'=FR$ for the ray class field $R/H$ of modulus $M'\mathcal O_H$. Under base change, $\mathfrak D_{F'/F}$ divides $\mathfrak D_{R/H}\mathcal O_{F'}$. Locally choose an integral generator of the ring of integers in the completion of $R/H$, with minimal polynomial $f$. Its minimal polynomial after base change divides $f$, and its derivative belongs to the new different even if the generator spans only an order over the new base. Therefore $f'$ evaluated at that generator belongs to the new different, as claimed. Taking normalized logarithmic norms gives

$$
 \frac{\log N\mathfrak D_{F'/F}}{[F':\mathbf Q]}
 \le \frac{\log N\mathfrak D_{R/H}}{[R:\mathbf Q]}
 \le \log M'.
$$

The last step follows from the conductor–discriminant formula. Each character of $\operatorname{Gal}(R/H)$ has conductor dividing $M'\mathcal O_H$, whose norm is $(M')^2$, and $[H:\mathbf Q]=2$. Finally $\log g_i\le9L_x+1$ and $e\log15\le9L_x$. This proves (2), including its support assertion. [Host subfield of the base coefficients][hostfield] · [Ray conductor–discriminant and compositum estimate][conductor]

## What is needed from the fitted quotient

Let $A$ be the integral cusp lattice at the negative shift $G_s(-c_0)$ on this cover, with $a=\operatorname{rk}A>0$. The finite group translates and the integral section of the compensating Hodge weight define the original family of maps $\Phi=(\phi_1,\ldots,\phi_{q_\Phi}):A\to B^{q_\Phi}$, where $q_\Phi$ is the number of maps. The maps are jointly injective on the generic fibre. Integrality into the particular $B$ above, the archimedean inequality $\sum_k\|\phi_k x\|^2\le e^{2P}\|x\|^2$, and the bound on $q_\Phi\ell$ are the assertions of the native map construction and rank comparison. The source takes $P=b$. These assertions still use the determinant-nonvanishing and norm estimates for the translating section. [Construction on this marked cover][maps] · [Use of all four assertions][descent]

Write $h=q_\Phi\ell-a$, $I_\Phi=(\Phi A\otimes F')\cap B^{q_\Phi}$, and $Q=B^{q_\Phi}/I_\Phi$ with quotient metrics. The latter is a projective lattice of rank $h$. Write $\deg_2$ for total normalized squared degree. If $h=0$ set $\deg_2 Q=0$. With adjoints taken in the indicated metrics on the span of $A$, the determinant of the exact sequence gives

$$
 q_\Phi\ell\,\mu(B)=a\,\mu(A)
  -\frac{2}{[F':\mathbf Q]}\sum_{w\mid\infty}\log\det(\Phi_w^*\Phi_w)
  +\frac{2}{[F':\mathbf Q]}\log\#(I_\Phi/\Phi A)+\deg_2 Q .   \tag{3}
$$

Indeed the Gram determinant on $\Phi A$ has the extra factor $\det(\Phi_w^*\Phi_w)$, saturation adds the finite index displayed, and the quotient metric gives exact additivity of degrees. This accounts for the possibility that the image is unsaturated. [Native product lattice and injection][product] · [Determinant and index conventions][degree]

It suffices to exhibit a single nonzero **integral vector in $\det Q$** whose mean log norm is at most $h\Lambda$, where the mean is $2/[F':\mathbf Q]$ times the sum over infinite places. Its generated sublattice gives $\deg_2 Q\ge-2h\Lambda$. For $h=0$ this lower bound is automatic. For example, take $h$ independent projections of integral vectors to $Q$ and bound their exterior product. The native uniform short generators of $B$ also suffice by inserting them into the summands of $B^{q_\Phi}$, selecting independent projections, and applying Hadamard. The new test concerns only this one quotient of rank $h$. Since the determinant in (3) is bounded by $e^{2aP}$ at each place, every $t\le\mu(A)-2P$ now gives

$$
 \mu(B)\ge\frac{a t-2h\Lambda}{a+h}
          =t-\frac{h}{a+h}(t+2\Lambda).                        \tag{4}
$$

If the rank comparison gives $h/a\le\epsilon$, the loss coefficient is at most $\epsilon/(1+\epsilon)$ when $t+2\Lambda\ge0$. When this sum is negative the displayed correction improves the bound.

For example, start with the [fitted degree-weighted Chow bound](PERIOD_WEIGHTED_ROOT_INTERSECTION.md). Let $y=(T-3d-4)[(1-\rho)c_s-X-c_c]-N_0$. The fitted determinant estimate there gives $\sum_Z d_Z\ge y\sum_Z w_Z$ for $w_Z=\mathcal B\Delta_Z$. The native component rank comparison gives $1-z\le(\sum_Z w_Z)/(\sum_Z r_Z)\le1$, $0\le z<1$. The component-to-cusp determinant comparison consequently gives

$$
 \mu_U\ge2(y-z\max(y,0)).
$$

Here $\mu_U$ is the squared slope at the fitted unanchored weight $u_M$. The flat comparison at the marked weight gives $\mu(A)\ge\mu_U-M_{p,i}-C_F E_p$. Thus (4) applies with $t=2(y-z\max(y,0))-M_{p,i}-C_F E_p-2P$. Its output substituted in (1), using (2), is the required *direction* of the reference-covolume inequality with all remaining quantities on specified lattices. In the native coarser budgets, the unanchored lower bound $-C_U E_p$ gives $\mu(L_0)\ge-M_{p,i}-[2(C_F+C_U)+9]E_p$, after $b\le E_p$ and the native gap and generator bounds. [Fitted component degrees and ranks][components] · [Flat comparison and original constants][low]

The remaining geometric input in this route is quantitative. It includes the Chow-to-arithmetic-degree estimate on the fitted images, the actual translating section and norm and rank comparisons, and the required lower bound for the quotient determinant in (3), or the native short spanning set implying it. The following measure comparison bounds the positive contribution of the row normalization and leaves a projected complementary-type slope. The single-word and paired-index passages from this reference bound to the full period-height entry have their own hypotheses. [Reference word and subsequent comparisons](PERIOD_REFERENCE_WORD_COVOLUME.md)

## The Petersson measure at the selected reference level

Keep the marked nonterminal layer and notation of the reference determinant identity. Write $r_t=r_g+r_b$, $s=\mu(B)-I$, and $e=e_g$. Let $K_1$ be the finite compact for the row with trivial subgroup and $K_P$ the compact for the reference subgroup $P=(p.F.\mathrm{lv2}.\mathrm{lvl}\,\mathrm{false}).P$. Both use the same frame and parahoric data. Denote by $V_i(K)$ the automorphic quotient volume for Haar measure giving $K$ finite volume one and having the row's prescribed archimedean density. At the real place $\tau$ let $d_{i,\tau}$ be the dimension of the lowest compact type. Define

$$
R_i=V_i(K_1)\prod_\tau d_{i,\tau},\qquad
R_i^{P}=V_i(K_P)\prod_\tau d_{i,\tau}.
$$

The measure term in the reference determinant is exactly $\log R_i^P$. More precisely, give the type space over the row field the probability Petersson norm transported from the core, and put $C_b=(1-e)L$ with its induced probability norm. With the term multiplied by $r_b$ taken to be zero if $r_b=0$, the identity becomes

$$
\frac{\operatorname{lcv}(M_j)}{D_R}
  =-s+\log R_i^P+\frac{r_b}{r_g}\bigl(\mu_{\mathrm{prob}}(C_b)-s\bigr).       \tag{5}
$$

This uses the native marked-row, rationality, Gram and orthogonal projector laws of the reference determinant identity. The additional analytic input is the actual row norm comparison from the original one-measure theorem. [Norm comparison on the marked row][determinant5-marked] · [Definition of the volume factor and its analytic input][determinant5-ratio] · [Inputs used to establish the one-measure theorem][determinant5-assembly]

**Comparison of norms.** Fix a unit extremal vector in each archimedean factor and evaluate the multiplicity map on their tensor. For the conjugate realization use its conjugate evaluation, whose absolute value is the same. Schur orthogonality identifies the pairing at unit vectors with the scalar multiplicity pairing. The row inner product multiplies that scalar by the product of the lowest compact type dimensions, according to its normalization. Passing from probability measure on the automorphic quotient to the row measure contributes its mass $V_i(K_1)$. The compact dimension product is invariant under the induced permutation and conjugation of archimedean embeddings. Thus on the embedded cusp space at every embedding of the row field, the squared row norm is $R_i$ times the squared probability norm. Hermitian polarization extends the identity to the complex span there. The marked type space is in that span by rationality. [Row inner product normalization][determinant5-rowip] · [Schur pairing and conjugate evaluation][determinant5-schur] · [Exact squared norm on the marked member][determinant5-norm]

**The finite subgroup factor.** The selected row has an isomorphism of its finite group with the residue group. The point supplies a finite adelic lift of every group element in the common parahoric whose reduction is exactly that element. The principal compact $K_1$ is the kernel of this reduction and $K_P$ is the inverse image of the image of $P$ under this isomorphism. Consequently $K_P/K_1\simeq P$ and $[K_P:K_1]=n_P$. In Haar measure normalized at $K_1$, the $n_P$ disjoint cosets give $K_P$ finite mass $n_P$. Dividing the measure by $n_P$ normalizes $K_P$ and divides the quotient volume by the same number. Thus $R_i^P=R_i/n_P$. This argument works directly on the adelic group, including when the quotient has stabilizers. [Finite level, frame and selected subgroup][determinant5-levels] · [Parahoric reduction and its preimages][determinant5-reduce] · [Definition of the lifts][determinant5-lifts] · [Lifts prescribed at the point][determinant5-point] · [Use on the selected subgroup][determinant5-actual] · [Trivial residual subgroup][determinant5-triv] · [Haar density normalization][determinant5-haar]

The row slope of any rank-positive sublattice of the type space equals its probability slope minus $\log R_i$. Moreover, $(1-e)L$ contains $L_b=L\cap\ker e$, and the map $1-e$ identifies $L/(L_g\oplus L_b)$ with $C_b/L_b$. Its normalized index therefore contributes exactly $J$ to the total degree of $C_b$. Substitute these facts in the reference identity and use $r_t-r_b=r_g$. This proves (5). In particular a common measure change is counted once per good dimension even when the bad rank is positive.

**Eventual one-sided estimate.** With the original parameter, host and weight bounds for a fixed family, one has, uniformly in the selected members and layers for all sufficiently large $x$,

$$
\log R_i^P \le 122 f r^2 L_x - \log n_P,\qquad
\frac{(\log R_i^P)_+}{E_p}
 \le \frac{122 r^2}{m e^{L_x}\log\log x}.
\tag{6}
$$

Here $L_x=x^\epsilon$ with fixed $\epsilon>0$, $b=e^{L_x}$ and $E_p=f m b L_x\log\log x$. The right-hand side tends to zero faster than every fixed negative power of $x$, since $r$ is polynomially bounded. The bound concerns the positive part, which is the direction needed in (5).

To check the constant, the native one-measure estimate is $\log R_i\le122 f r^2 S$ whenever its four size conditions hold at $S$. For some fixed family exponent $A$, the host bounds give $frn_V L_x\le x^A$. Eventually $5x^A\le e^{L_x}$, so $frn_V\le e^{L_x}$. The weight estimate at every layer gives $\mathrm{wtSize}\le fr(4b+1)\le 5fr b\le e^{2L_x}$. Furthermore $\log(g_0g_1)\le18L_x+2\le30L_x$, and the two terms $\log\mathrm{rd}_E$ and $|\mathrm{dlog}L(D,1)|$ are each at most $L_x$. These are exactly the four conditions with $S=L_x$. Apply the estimate, then subtract $\log n_P$. This verifies (6) using only the upper volume estimate. The analytic assumptions in that estimate remain those in the source's volume and Weyl dimension theorems. The fitted cusp degree and the projected complementary slope in (5) require their separate inputs. [Four size conditions and constant 122][determinant5-ratio] · [Pointwise weight and field estimates][determinant5-weights] · [Uniform host polynomial and parameters][determinant5-host] · [Unit scale on the marked family][determinant5-unit]


The [comparison with Chen’s determinant and component-transfer arguments](EXTERNAL_PROOF_COMPARISON.md#chens-selected-length-determinant-and-translating-section) gives a sufficient integral construction of the quotient wedge in (3). Apply the character trace to a short spanning set at the actual central weight, transfer its images to the copies of $B$, and wedge independent images in $Q$. This uses the native even-weight span at that weight. The translating-section determinant test and the marked component estimates in the comparison specify the model hypotheses for this route.

[determinant5-marked]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AbelianVarietyTheory/Proofs/DivisorProofs/ExactAtOfOneMeasure.lean#L43-L63
[determinant5-ratio]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AbelianVarietyTheory/BlockTheory/DivisorBase/OneMeasureSizes.lean#L15-L96
[determinant5-assembly]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AbelianVarietyTheory/Proofs/DivisorProofs/OneMeasureOfPublished.lean#L18-L24
[determinant5-schur]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AbelianVarietyTheory/Proofs/DivisorProofs/ExactRatioOfFundamentalDomain.lean#L55-L115
[determinant5-norm]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AbelianVarietyTheory/Proofs/DivisorProofs/ExactAtOfOneMeasure.lean#L105-L126
[determinant5-levels]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Formalism/LocalToGlobal/IndefiniteReal/LinksDefs.lean#L638-L676
[determinant5-reduce]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Formalism/LocalToGlobal/Divisibility/DefGroup.lean#L669-L697
[determinant5-lifts]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Formalism/LocalToGlobal/IndefiniteReal/ThPinsR.lean#L125-L129
[determinant5-haar]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Formalism/LocalToGlobal/IndefiniteReal/SubgroupCharExtensionOneApply.lean#L122-L140
[determinant5-weights]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AbelianVarietyTheory/Proofs/DivisorProofs/LogRatioUpperBound.lean#L119-L165
[determinant5-host]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AbelianVarietyTheory/Proofs/DivisorProofs/HostBoundHolds.lean#L103-L134
[determinant5-unit]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AbelianVarietyTheory/Proofs/DivisorProofs/LogRatioUpperBound.lean#L185-L216
[determinant5-point]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AbelianVarietyTheory/Definitions/Divisors/TupleReadBaseTupleEqFamily.lean#L203-L215
[determinant5-triv]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Formalism/LocalToGlobal/Divisibility/DefGroup.lean#L573-L586
[determinant5-rowip]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Formalism/LocalToGlobal/IndefiniteReal/LinksDefs.lean#L317-L323
[determinant5-actual]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AbelianVarietyTheory/Proofs/DivisorProofs/ExistsFiniteGroupLevel.lean#L17-L25

[degree]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AbelianVarietyTheory/Proofs/DivisorProofs/SlopeSqSubLeSlopeSqSpan.lean#L222-L248
[definitions]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AbelianVarietyTheory/Definitions/Divisors/CovolXOfCovol.lean#L26-L95
[reference]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AbelianVarietyTheory/Proofs/DivisorProofs/RecursionOfGramBound.lean#L22-L51
[refgroup]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Formalism/LocalToGlobal/IndefiniteReal/LinksDefs.lean#L670-L677
[core]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AbelianVarietyTheory/Proofs/DivisorProofs/CoveringLeFromMeasure.lean#L23-L85
[coord]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AbelianVarietyTheory/Proofs/DivisorProofs/CovolumePerRankLeNegSlopeScaled.lean#L58-L99
[pull]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AbelianVarietyTheory/Proofs/DivisorProofs/LevelCoverCuspFormPullbackInjectiveDescent.lean#L212-L231
[span]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AbelianVarietyTheory/Proofs/DivisorProofs/CuspFormLatticeSlopeSqGoodCoverLeCore.lean#L76-L150
[rat]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AbelianVarietyTheory/Proofs/DivisorProofs/RationalCoverBound.lean#L21-L36
[glue]: https://github.com/rh-lean-roadmap/rh-lean-roadmap/blob/dc5594a62bb2b94139788df817db693cd939a046/docs/src/book/main.tex#L21685-L21705
[scale]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AbelianVarietyTheory/Counterexamples/RotationExamples/MeasureFailsForLargeConstant.lean#L20-L38
[ray]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AbelianVarietyTheory/Proofs/DivisorProofs/ExistsGoodCoverOverSizedField.lean#L111-L159
[depth]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AbelianVarietyTheory/Proofs/DivisorProofs/DeepExistenceStatement.lean#L17-L43
[hostnum]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AbelianVarietyTheory/Proofs/DivisorProofs/HostBoundHolds.lean#L115-L129
[stability]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AbelianVarietyTheory/Proofs/DivisorProofs/LevelCoverCuspFormPullbackInjectiveDescent.lean#L151-L202
[different]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AbelianVarietyTheory/Proofs/DivisorProofs/GaloisStableLatticeRationalSpanInclusions.lean#L36-L46
[hostfield]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/ReciprocityTheory/ReductiveGroups/ArithmeticGeometry/BirationalGeometry/ToroidalCompactification/PushInvertible.lean#L12-L45
[conductor]: https://github.com/rh-lean-roadmap/rh-lean-roadmap/blob/dc5594a62bb2b94139788df817db693cd939a046/docs/src/book/main.tex#L49684-L49691
[maps]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AutomorphicArithmetic/ThetaCorrespondence/ThetaPairLifts/ThirdPlaceSeries/CoveringDescentMapsCompatible.lean#L43-L118
[descent]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AbelianVarietyTheory/Proofs/DivisorProofs/LowerBoundOfAllEstimates.lean#L65-L105
[product]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AbelianVarietyTheory/Proofs/DivisorProofs/HtMapLeOfPoints.lean#L69-L120
[components]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AbelianVarietyTheory/Proofs/DivisorProofs/UniformLowerBoundOfSums.lean#L34-L60
[low]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AbelianVarietyTheory/Proofs/DivisorProofs/LowerBoundOfAllEstimates.lean#L65-L123
