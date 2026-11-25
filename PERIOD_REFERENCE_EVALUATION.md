# Fourier evaluation on the reference row before gluing the twists

The reference row admits an all-place height estimate under weaker hypotheses than Roadmap B8.22. The input is the ordinary evaluation-field choice of B8.17 on the member's own Hida realization. The proof constructs the matrix from its finite Fourier sums. At the reference tuple the twist support is empty, so the denominator estimate applies at **every** finite place of the coefficient field, including places at which the glued row later selects a different tuple. This gives a slope bound for the reference image lattice. For the glued row, a sum of largest local elementary divisors at just the changed places suffices. [Native finite and infinite estimates][claims] · [B8.17 and its field hypotheses][field] · [Original gluing rule][glue]

## What the linked member already supplies

Fix a member and the bundle chosen by the common selector. Its linkage identifies the datum, family object and bundle together with those of a weighted point $q$. The row record of that point contains the finite-group identification for its actual frame. Applied to its same coefficient, spectral and group records, the identification gives, for each $s=0,1$, a labeling $L_s$ at $g_s$ with the prescribed Teichmüller character and, simultaneously for all polynomials $P$,
$$
 e_{\rm ser}(g_s,P)=\sum_{\substack{\chi\ {\rm irreducible}\\\operatorname{HasLabel}(L_s,\chi,P)}}e_\chi
 \quad\text{in }\mathbf C[\operatorname{GL}_r(\mathbf F_{g_s})].
$$
The label contains generators compatible under the finite-field norms. This witnesses exactly the series condition used in B8.22, before any choice of a Fourier grid. The condition depends on the datum, so substitution along the linkage proves it for the selected bundle with the same labels. [Linked selection](LOCAL_SELECTED_FAMILY.md) · [Weighted point and row record][wpt] · [Group identification][grp] · [Application of that field][applygrp] · [Definition of the series][labels]

The same linkage gives a second part of the fitting check. At each twisted coefficient place $w$ the selected index has its residue characteristic and lies under $w$ or $\bar w$. The sets $Q(w)$ and depths agree at places above the same prescribed pair. Indeed a twisted place belongs to the active set by the off-support rule. The records there agree by coherence on the small field and by the conjugation law. If the common support is nonempty, the separation of the supports belonging to distinct indices forces the indices to agree as well. The goodness witness at $q$ gives split, conjugation-stable supports avoiding the excluded places, and a single function $N_0$ of the twist index furnishing the prescribed two-sided valuation bounds for every coprime power. Its quantifier precedes all the places and powers at this member. It can depend on the member. These deductions apply at each selected $x>F.x_1$ and every index there. [Goodness at the original point][wpt] · [Transport and proof of the twist conditions][twist] · [Exact remaining fitting clauses][fit]

## Constructing the reference matrix

Use a member point with the row conditions of B8.21b and its positive-rank level-zero row. In particular the rational projection $P_0:K^{n_V}\twoheadrightarrow K^{d_Q}$ is onto, the realization $\iota_0:K^{d_Q}\to RR_K$ is an isomorphism, and the base theta map on the indicated good vectors has kernel $\ker P_0$. Suppose the realization satisfies the Hida row setting and has an at-scale choice of grid, Weil data, row tests, measures and coset expansions satisfying the ordinary evaluation-field condition. Assume the local theta inputs $\mathscr P$ for the sum estimates and the separation and Fourier formula on this realization from B8.11, B8.15 and B8.16 with their hypotheses. These are statements about the kernels, tests and scalar expansion. The comparison with squared bottom theta norms over the coefficient field is a later condition in B8.20. The field condition being used here is the full one of B8.17, including its normalized values, phases and jets. On its stated class of completions B8.17 supplies a choice on the given realization when the coefficient field contains its requested finite set. Its quantifier puts that request before the completion. An already fixed field needs to satisfy this condition. [B8.17][field] · [Row, projection and lattice][glue] · [Hypotheses for the Fourier formula][formula] · [Uniform input to the local estimates][big]

Let $K$ be the coefficient field, $\sigma_0$ its specified complex embedding, and $e_{V,0}$ the original source inclusion at the reference tuple. For each test $a$ and standard source basis vector $e_j$ take the unique element of $K$ satisfying
$$
 \sigma_0(V_{aj})=v_{\rm row}(a,\mu_0,e_{V,0}e_j).
$$
For existence, expand the row sum in its finite coset and definite class sums. The scalar and the coefficients of the unfolded coset tensors lie in $\sigma_0 K$. The inverse stabilizer orders are rational. The top and opposite normalized kernel chains preserve the specified coefficient field on the rational test and rational initial form, and the terminal contraction preserves it too. Hence each evaluation is in $\sigma_0 K$. The validity of the coset expansion gives additivity in the initial rational form, and scalar multiplication gives $\sigma_0$-semilinearity. Expansion in the basis now proves the same identity with $(Vx)_a$ for every $x\in K^{n_V}$. This constructs a unique matrix in the original coordinates. Form its target lattice $M$ as the coordinate dual of the direct sum of coefficient lattices, with the inverse-transpose Gram metric. This construction takes only the grid, representatives and indexing. [Rationality term by term][rational] · [Extension from basis vectors and construction of the test lattice][basis] · [Target normalization](PERIOD_AUXILIARY_TEST_SLOPE.md)

For the kernel use only the base tuple in the Fourier formula. With $\ell_a$ the separating tests it gives
$$
 zc\,\ell_a\bigl(\Theta_0 j_0e_{V,0}x\bigr)=\gamma\,\sigma_0((Vx)_a).
$$
Here $z$ is a root of unity in its complex reading, and $c$ is the product of the nonzero reference square constants. The positive rank and surjectivity of $P_0$ give an $x$ with nonzero theta image. Separation makes the left side nonzero for some $a$, so $\gamma\ne0$. Vanishing of $Vx$ is consequently equivalent to $\Theta_0j_0e_{V,0}x=0$, which is equivalent to $P_0x=0$ by the injective row realization. Thus there is a unique injective $K$-linear $U:K^{d_Q}\to K^n$ with $UP_0=V$. This uses complex nonvanishing of the reference constants and the rationality of $V$. The argument requires no comparison of constants from two tuples. [Precise base-kernel argument][kernel] · [Identity on the good source][formula]

## Bounds at all places for this matrix

Write $b=e^L$, $L=x^\varepsilon$, and let $N_*=k+m(t+k+m+6)$. Define $\Sigma(G)=\sum_{v\in S_0}d_{\rm pl}(v)\log Nv$ using the prescribed grid **depths**. The base-place depth can exceed the character conductor exponent. With $C$ above the common thresholds the original sum theorem gives
$$
 \begin{split}
 h_{\rm quot}(U)=h(V)&\le H_{\rm ref}
     := CfmN_*bL+Cm^2N_*^2\Sigma(G),\\
 2\sum_w \ell_w d(w)&\le D_{\rm ref}
     := Cfm^2 N_*^2\bigl(L+\Sigma(G)\bigr)b,
 \qquad \ell_w=\frac{\log Nw}{[K:\mathbf Q]} .
 \end{split}
 \tag{1}
$$
The infinite height is the mean of log **squared** operator norms with the fitted dual target metric and the original source/direct quotient metrics. The equality follows place by place because $P_0$ in the corresponding orthonormal frames is a coisometry. For any target matrix $A$ and such a coisometry $J$, $JJ^*=1$ gives $\|AJ\|=\|A\|$. The inequality is the infinite sum bound applied to the matrix just constructed. It is uniform over the valid field-compatible choices at the stated scales. [Scale and depth budgets][scale] · [Finite, infinite and field hypotheses][big] · [Infinite estimate from the local factors][analytic] · [Quotient isometry][cois]

For the finite inequality, the reference character equals one. The level datum identifies its ramification support with the ramification of that character, so $Q(\mu_0)=\varnothing$. The avoidance hypothesis in the finite sum bound is a universal assertion over this set, hence holds at every $w$. For every $x$ in the original source lattice $M_0$ the estimate gives an $s\in K^\times$ with $sVx\in M$ and $v_w(s)\le\delta(w)$, for one nonnegative finitely supported loss $\delta$ independent of $x$. Therefore
$$
 V(M_{0,w})\subseteq\mathfrak p_w^{-d(w)}M_w,\qquad d(w)=\lfloor\delta(w)\rfloor .
$$
Indeed $v_w(s)$ is an integer, so membership follows in the localized lattice for every $x\in M_0$ and then for all $x\in M_{0,w}$ by linearity. The native finite loss is bounded by $m\,b_{\rm One}/2$ with $b_{\rm One}=CfmN_*^2(L+\Sigma(G))b$. This gives the factor $2$ in (1) and the bound on the entire finite contribution. The common cutoff has order $C_F$, then $C\ge C_0(C_F)$, then $x\ge x_0(\varepsilon,C,C_F)$ before realizations, choices, tests and places. Take the maximum with the cutoffs for rationality and the separation formula. [Empty ramification at the base][empty] · [Avoidance, loss and localization][claims] · [Simultaneous finite and infinite estimate][analytic]

Let $\Lambda_{\rm ref}=\iota_0P_0M_0$ in $RR_K$. With the direct quotient metric pulled across $\iota_0$, the slope inequality for the injective map $U\iota_0^{-1}$ gives
$$
 \mu_{\max}(\Lambda_{\rm ref},{\rm quot})
 \le \mu_{\max}(M)+H_{\rm ref}+D_{\rm ref}.
 \tag{2}
$$
To verify the signs and factor of two, the finite inclusions put the full image in $(\prod_w\mathfrak p_w^{-d(w)})M$, increasing its squared-norm slope by $2\sum_w\ell_wd(w)$. On a rank-$s$ sublattice the determinant of the injection has operator norm at most the $s$th power of the operator norm at each infinite place. Dividing degrees by $s$, then taking the supremum, gives (2). In the row metric divided in squared norm by $\kappa_v$, the lower block floor of B8.22 adds at most $3CfmN_*^2L$ to the height under the eigenvalue hypotheses proved in the scalar comparison. The slope of a fixed lattice in that divided metric is its original row slope plus $\langle\log\kappa\rangle_\infty$. [Original divided metric and height change][norm] · [Level-one floor and its hypotheses](PERIOD_OFF_BASE_SCALAR.md)

On the original size range, $\mu_{\max}(M)^+$ is $o(b^\eta)$ for every fixed $\eta>0$ by the [auxiliary slope estimate](PERIOD_AUXILIARY_TEST_SLOPE.md). The grid depth weight $\Sigma(G)$ has polynomial growth: off $v_0$ the depths are two. The auxiliary $q_0$ is one modulo the host conductor, so it splits completely and $Nv_0=q_0$. At $v_0$ the defining modulus allowance contributes at most $P_{\rm pf}+\log Nv_0$. Hence $\Sigma(G)\le 2P_{\rm pf}$ eventually, with $P_{\rm pf}=C f^2(k+m)^6\log(b(k+m)g_0g_1p_{\rm de}p'_{\rm de}|D_E|)$ for $C\ge\max(C_F,42)$. The growth bounds on ranks, $L$, prime logarithms and root discriminant make this polynomial in $x$. Thus (2), including the displayed metric change, is $O_{\varepsilon,\mathcal F,C}(x^A b)$ on the original ordered range; for fixed growth exponents one can increase $A$ once to absorb fixed constants at the final point cutoff. [Native depth formula][natdepth] · [Grid depths and modulus][modulus] · [Polynomial family estimate][powers]

## The remaining change of lattice

The local rule for $RR$ makes $(\Lambda_{\rm ref})_w=RR_w$ whenever $\mu(w)=\mu_0$. At a changed place define $h_w$ as the least nonnegative integer with $\mathfrak p_w^{h_w}RR_w\subseteq(\Lambda_{\rm ref})_w$. This integer is computable in the actual rational row space. In local bases let $T_w$ have as columns an $RR_w$ basis in the $(\Lambda_{\rm ref})_w$ basis. Then $h_w=\max(0,-\min_{a,b}v_w((T_w)_{ab}))$, with $v_w(0)=+\infty$. Changing either basis multiplies by invertible integral matrices, preserving the containment and its least exponent. In elementary-divisor coordinates $h_w$ is the positive part of the negative smallest exponent. Write $h_w=0$ at unchanged places. Then
$$
 \mu_{\max}(RR)+\langle\log\kappa\rangle_\infty
 \le \mu_{\max}(M)+H_{\rm ref}+D_{\rm ref}+3CfmN_*^2L
     +2\!\sum_{\mu(w)\ne\mu_0}\ell_w h_w .
 \tag{3}
$$
Indeed $RR\subseteq(\prod_w\mathfrak p_w^{-h_w})\Lambda_{\rm ref}$ by local containment. This gives (3) either by monotonicity of maximal slope for inclusions or by adding $h_w$ to the local allowance of the same map $U\iota_0^{-1}$. If every local row is the reference row, (3) proves the full **level-zero** functional inequality at any sufficiently large permitted height exponent under the preceding assumptions. For general selected points (3) gives an alternative to the toric-ratio argument for the finite twist loss. It still needs a uniform bound for the displayed weighted sum or the original fitted-grid control of the twisted evaluations. Finiteness of the changed set on each member alone supplies no such uniform bound. [Gluing law][glue] · [Original toric-ratio argument][toric]

### A signed test in the bottom coordinates

There is also a test allowing cancellation between places. It uses the generators of the two actual images, so it can be applied without choosing isomorphisms of ambient theta lattices. At a changed place choose a common $K_w$-basis of the bottom space of rank $r$. Let $A,B$ be full-row-rank generator matrices for the reference and selected lattices there. For $0\le s\le r$ let $J_s$ be the fractional ideal generated by all $r$-minors using $r-s$ columns from $A$ and $s$ from $B$. Set $D_s(w)=v_w(J_0)-v_w(J_s)$, with $D_s(w)=0$ at unchanged places.

If the Smith exponents of the selected lattice relative to the reference lattice are $a_1\le\cdots\le a_r$ (an exponent $-1$ means enlargement by one uniformizer denominator), then
$$
                  D_s(w)=-\sum_{i=1}^s a_i .
$$
Indeed choose a basis of the reference lattice and perform invertible integral column operations so that $A=[I_r\ \ 0]$. Changes of ambient basis multiply every $J_s$ by the same determinant. Integral column operations within either generator matrix preserve each ideal, by multilinearity and invertibility. With $A$ in the indicated form the nonzero mixed minors generate exactly the ideal of $s$-minors of $B$, giving the formula by Smith reduction. In particular $h_w=\max(0,D_1(w))$, and the proof of (3) works with the *signed* $D_1(w)$, since $RR_w\subseteq\mathfrak p_w^{-D_1(w)}(\Lambda_{\rm ref})_w$ also when $D_1(w)<0$.

For a rank-sensitive version let $\mu_s(L)$ be the supremum of slopes of rank-$s$ sublattices. Then for the same infinite metrics
$$
 \mu_s(RR)\ \le\ \mu_s(\Lambda_{\rm ref})+
                         \frac{2}{s}\sum_w\ell_wD_s(w).
$$
To see this, intersect both lattices with any rational $s$-plane. Locally each intersection is saturated, so its determinant line lattice is the intersection of the full $s$th exterior-power lattice with that line. The largest enlargement exponent of the latter exterior powers is $D_s(w)$. Summing the resulting determinant degrees proves the inequality. Passing to saturated sublattices suffices for the supremum. Thus a polynomial-times-$b$ upper bound on $\max_{1\le s\le r}(2/s)\sum_w\ell_wD_s(w)$ is another sufficient arithmetic test. At $w$ the two lattices are equal precisely when $D_1(w)\le0$ and $D_r(w)=0$. Determinant equality alone allows $\operatorname{diag}(\pi^{-H},\pi^H)$ relative to the unit lattice at any $H$. The [first-pass projector calculation](FIRST_PASS_TYPE_PROJECTION.md) likewise illustrates the role of saturation. Equality of the [full target lattices](RETWISTED_INTEGRAL_EVALUATIONS.md) on a supplied model gives no determinant estimate for two different bottom images.

B8.23 uses a stronger construction to obtain the prescribed Fourier choice with all the square-field data on the selected realization. The point's extension with list supplies a reference grid together with its field values and abelian layer list. The full extension must preserve the place $v_0$, its chosen lift and the actual layer characters. These equalities preserve the field condition on the grid characters and prime-power roots, and preserve the entire abelian list used to compare twists. The separate evaluation field and square-field conditions are provided by the full extension. This use of B8.23 requires its good-member, division and geometry hypotheses. The reference-lattice proof above already works with a B8.17 choice on the actual row and yields (3) without this prescribed-grid replacement. Availability of the field choice and uniform control of the changed lattices on the selected range would give the base-row bound. The [two-level transfer](PERIOD_SHARP_ROW_TRANSFER.md) and [divided-column estimate](PERIOD_DIVIDED_COLUMN_UPPER.md) then give entry 2. [Exact matching of the two grids][fit] · [How the list and full extension are used][preserve] · [B8.22 and B8.23][selected]

The grid may also be obtained over a finite coefficient extension if the new bottom row is the scalar extension of the specified one. Precisely, let $K'/K$ be such an extension. Suppose that each new place $w'\mid w$ uses the pullback of the original serving tuple, that its source lattice and the two maps $P_t,\iota_t$ are obtained by base change, and that the infinite metrics and $\kappa$ pull back. Flatness carries the image of $\iota_tP_t$ to the extended image. Thus the localizations of $RR'$ and $RR\otimes_{\mathcal O_K}\mathcal O_{K'}$ agree everywhere. For each original rational subspace its saturated lattice extends to the saturated lattice on the extended subspace, and normalized degree and the normalized mean of $\log\kappa$ are unchanged. Taking the supremum over the original subspaces proves that the extended estimate descends at zero cost. The full-target extension law by itself does not identify the serving tuples and the bottom image maps on the new arithmetic completion.

[wpt]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AbelianVarietyTheory/Definitions/AutomorphicMembership/DsigEq.lean#L24-L72
[grp]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AbelianVarietyTheory/Definitions/AutomorphicMembership/NonzeroPlacesOverPrimes.lean#L47-L56
[applygrp]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AbelianVarietyTheory/Proofs/TwistedOperators/RowTestHypothesesAtMemberAdelicData.lean#L18-L39
[labels]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AbelianVarietyTheory/Definitions/NonGaloisDescent/LabelDatum.lean#L81-L116
[twist]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AutomorphicArithmetic/ThetaCorrespondence/ThetaPairLifts/ThirdPlaceSeries/TwistsAtLinked.lean#L19-L46
[fit]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AbelianVarietyTheory/Proofs/IwasawaDecomposition/GridFieldHasLattices.lean#L20-L65
[big]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AbelianVarietyTheory/Statements/PlaceShiftStatements/InfClassAt.lean#L79-L96
[formula]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AbelianVarietyTheory/Statements/HeckeThetaIntegrals/FormulaAt.lean#L68-L94
[rational]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AbelianVarietyTheory/Proofs/TwistedOperators/RowTestRationalSumsOfFiniteSumsMeaningful.lean#L51-L97
[basis]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AbelianVarietyTheory/Definitions/Divisors/MulVecEqOfBasis.lean#L54-L110
[kernel]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AbelianVarietyTheory/Proofs/DivisorProofs/KernelAtFittedPoints.lean#L19-L85
[scale]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AbelianVarietyTheory/Statements/PlaceShiftStatements/InfClassAt.lean#L45-L54
[claims]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AbelianVarietyTheory/Statements/PlaceShiftStatements/InfClassAt.lean#L131-L179
[analytic]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AutomorphicArithmetic/ThetaCorrespondence/ThetaPairLifts/LocalTypeDictionary/SumSizeFiniteAwayArchimedeanCombined.lean#L26-L45
[empty]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AbelianVarietyTheory/Proofs/DivisorProofs/TypePartBase.lean#L49-L55
[preserve]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AutomorphicArithmetic/ThetaCorrespondence/ThetaPairLifts/ThirdPlaceSeries/EvPSizeRowsDlog.lean#L57-L92
[field]: https://github.com/rh-lean-roadmap/rh-lean-roadmap/blob/94e6a98b4e74932a0298d6bd22d44cf60c62764b/docs/src/book/main.tex#L18854-L18879
[glue]: https://github.com/rh-lean-roadmap/rh-lean-roadmap/blob/94e6a98b4e74932a0298d6bd22d44cf60c62764b/docs/src/book/main.tex#L18990-L19001
[cois]: https://github.com/rh-lean-roadmap/rh-lean-roadmap/blob/94e6a98b4e74932a0298d6bd22d44cf60c62764b/docs/src/book/main.tex#L19223-L19250
[norm]: https://github.com/rh-lean-roadmap/rh-lean-roadmap/blob/94e6a98b4e74932a0298d6bd22d44cf60c62764b/docs/src/book/main.tex#L48909-L48916
[modulus]: https://github.com/rh-lean-roadmap/rh-lean-roadmap/blob/94e6a98b4e74932a0298d6bd22d44cf60c62764b/docs/src/book/main.tex#L19117-L19128
[powers]: https://github.com/rh-lean-roadmap/rh-lean-roadmap/blob/94e6a98b4e74932a0298d6bd22d44cf60c62764b/docs/src/book/main.tex#L48969-L48979
[toric]: https://github.com/rh-lean-roadmap/rh-lean-roadmap/blob/94e6a98b4e74932a0298d6bd22d44cf60c62764b/docs/src/book/main.tex#L48917-L48937
[selected]: https://github.com/rh-lean-roadmap/rh-lean-roadmap/blob/94e6a98b4e74932a0298d6bd22d44cf60c62764b/docs/src/book/main.tex#L19520-L19543
[natdepth]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AbelianVarietyTheory/Definitions/Divisors/LeastSplitAuxiliaryPrimeThetaChainSpec.lean#L224-L256
