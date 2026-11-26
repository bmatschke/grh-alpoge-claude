# The good-row comparison using the arithmetic reference tuple

For the slope deduction one can remove the separate nonvanishing requirement at the prescribed ramified level. On each word whose pairing with the good row is nonzero, the prescribed arithmetic reference tuple already contains a nonzero pair. On a word whose entire pairing with the good row vanishes, the zero rational map gives its exact contribution to the same slope argument. This uses the same word spaces, row, levels, metrics and rank-weighted allowances. It also avoids the surjectivity of descent onto the **full** reference multiplicity space for this particular deduction. The proof still needs the homogeneous seesaw on the actual row and column tests, the joined coordinates, and the quantitative arithmetic estimates. We describe separately what follows for the original word maps.

## The relation needed on the prescribed rows

Fix a member, its number field $K$, its specified embedding into $\mathbb C$, and its sharp row space $W$. For an attained tuple $t$ let $q_t:V_t\to W$ denote its rational row map, including the selected identifications. The reference map $q_0$ is onto and the integral rows served by each attained $t$ span $W$ over $K$. Write $X_u$ for the prescribed ramified word space in rational coordinates, and $A_t:X_u\times V_t\to K$ for the arithmetic top evaluation. Let $S_u:X_{u,\mathbb C}\times W_{\mathbb C}\to\mathbb C$ be the **bottom** Bessel pairing with the actual good row, with the joined row and column isometries, finite translation and common row conjugation already inserted. Thus $S_u(x,q_t v)$ uses the descended good vector of that arithmetic input. It is complex bilinear in the joined coordinate conventions. The common change on the row must be the same for all words. [Joined complex coordinates](../../../archive/rounds/v89/continuation_v89/comparison.tex#L34-L98) · [Serving lattices and surjectivity](../../../archive/rounds/v89/continuation_v89/integral.tex#L59-L93)

The required analytic implication for a fixed word is
$$
 \sum_i l_i c_{t_i} A_{t_i}(x_i,v_i)=0
 \quad\Longrightarrow\quad
 \sum_i l_i S_u(x_i,q_{t_i}v_i)=0,\qquad l_i\in\mathbb C .       \tag{1}
$$
Use the actual normalizers $c_t\ne0$. It suffices to take **two** evaluations in (1), the first from the arithmetic reference tuple, and to use rational coordinate basis pairs for the second. A single pair is allowed with the other coefficient zero. The hypothesis is the direction in the original two-step calculation *before* the nonvanishing choice. It uses the arithmetic top rows already furnished at each tuple. No preimage of a separately chosen automorphic row is needed.

Here is its scope in the source. A double step on two polynomial row vectors introduces the row measures $I_{t,j}I_{t,j+1}$ and the upper coefficient $V_{t,j}K_{t,j}K_{t,j+1}$. The compact polynomial average is a linear combination of evaluations at invertible frames since these separate the polynomial coefficient space. Both steps use a frame combination chosen before inserting the tuple’s class function. The upper relation then annihilates the summand at every real translate after refining the finite levels to their intersection. Absolute cusp integration on the row and intermediate lift and density of the real polynomial translates give the lower relation on smooth vectors. At the terminal step the interlacing branching line has dimension one. Iteration yields (1) after the common bottom translation and period unfolding. The [split symmetric contraction](PERIOD_SPLIT_SYMMETRIC_CONTRACTION.md) supplies the translated support and scalar at that position. The second-pass [square theorem](../second-pass/SECOND_PASS_RAMIFIED_SQUARE.md) concerns the grid producing the preliminary datum, and its [bottom separation](../second-pass/SECOND_PASS_BOTTOM_SEPARATION.md) allows a choice of Schwartz tests. The endpoint homogeneous relation requires the prescribed tests simultaneously across tuples. The required identifications include the finite class kernel on the specified tests, its translated contraction, the terminal class reading, the actual row lifts, and their scalar and measure conventions. The implications below invoke these inputs at the construction point. They do not invoke the final Gram bound to build that point. [Homogeneous transport through the original chain][hom] · [Double-step premises and passage to smooth vectors][step] · [All-chart compact frame coefficients][frame]

Call a word active when $S_u$ is not identically zero. Since $q_0$ is onto and the rational coordinate bases span after extension of scalars, for an active word there is a rational reference basis pair $(x_*,v_*)$ with $b=S_u(x_*,q_0v_*)\ne0$. Equation (1) for this pair alone gives $a=c_0A_0(x_*,v_*)\ne0$. For each basis pair at each tuple, take the coefficients $(c_t A_t(x,v),-a)$ in the two-term implication. This proves
$$
                  S_u(x,q_t v)=(b/a)c_t A_t(x,v)                \tag{2}
$$
on every pair by bilinearity. In particular $A_0$ kills $\ker q_0$ in its row variable, and the original rational native map $B_u$, defined using a reference rational section of $q_0$, is the induced pairing. On these words,
$$
 B_u(x,q_t v)=(c_t/c_0)A_t(x,v),\qquad
 S_u(x,y)=(b/a)c_0 B_u(x,y).                                    \tag{3}
$$
All scalar extensions on the right use the fixed embedding. Choosing the common isometric coordinates first is necessary for the second equality to give the project's Bessel comparison. Since (2) only uses that the reference pair exists when $S_u\ne0$, no lower bound for any individual Bessel value is necessary.

## Exact phase on the constructed twisted charts

At a fitted row with the source's actual choice of twist charts and comparison constants, one has the sharper formula $c_t/c_0\in\mu_\infty$, the group of complex roots of unity. This calculation uses the normalizations in the construction. An arbitrary choice of representatives for a projective comparison scalar need not have this property.

Indeed $m$ is even. Apart from one wordwise constant, $c_t$ is its terminal period scalar times the product over the even $j<m$ of
$$
 \frac{V_{t,j}K_{t,j}K_{t,j+1}}{I_{t,j}I_{t,j+1}}.
$$
The following facts account for every factor on the original chart formulas.

* The level part of $V_{t,j}$ is the reciprocal of the two successive level indices $J_{t,j}J_{t,j+1}$. Haar subdivision gives $I_{t,j}J_{t,j}=I_{0,j}$. Thus dividing this part by the two row-level measures gives precisely $(I_{0,j}I_{0,j+1})^{-1}$ for every tuple.
* The two step-vector scalars are each a common nonzero scalar times a root of unity. Changing a split Weil character by the finite-order twist evaluates that twist on the ratio of the consecutive determinant representatives. The torus factor has fixed positive absolute constants and integer powers of the character evaluated on fixed ideles. A common character power for $t$ and $0$ gives equal powers of their torus factors. The other local scalar and the double-step contraction scalar are common, including the contraction convention $1$ on the terminal pair.
* With the source and target rephasing of the actual column charts, $K_{t,j}=V_j C_j c_{0,j}\rho_{t,j}$ with $V_j,C_j,c_{0,j}$ common nonzero and $\rho_{t,j}$ a root of unity. In the ordinary joins the two signs of the same intermediate determinant have exponents with even sum. In the penultimate join, reducing the parahoric element to blocks $A,D$ gives the multiplier $\delta(\det D)/\delta(\det g)=\delta(\det A)^{-1}$, paired with its inverse. The leftover determinant character is constant on each intermediate chart set by equality of the tame restrictions at the extra units. Hence the factors at the ends of a chart entry can be absorbed successively into roots of unity on the chart bases. At the terminal level each twisting place has exactly one label. The product also has exactly one, so the terminal scalar is the common terminal volume times a single root of unity.

These formulas give a finite product of roots of unity for the ratio. The rational-power support condition used in the original argument follows with right side $1$. This stronger conclusion relies on the specific chart construction. [Original vector factors, Haar indices and torus factors][factors] · [Native common factors and terminal singleton][col] · [Root-power calculation on the actual kernel and terminal factors][roots] · [Exact normalization of the total product][total] · [Parahoric phases and chart rescaling][phases]

Consequently on **every active word** each attained tuple satisfies
$$
     B_u(x,q_t v)=z_{u,t}A_t(x,v)\quad\text{over }K,\qquad
             z_{u,t}\in\mu(K),\qquad z_{u,0}=1.                 \tag{4}
$$
Indeed $q_t(V_t)$ spans $W$ and $B_u\ne0$, so a rational pair with nonzero left side in (3) exists. The ratio of its rational values lies in $K$ and has the required complex image. It is the same ratio on all inputs. The order of the cyclic group $\mu(K)$ is at most $2[K:\mathbb Q]^2$: if its order is $e$, then $\varphi(e)\le[K:\mathbb Q]$, and $\varphi(e)^2/e=\prod_{p^h\parallel e}p^{h-2}(p-1)^2\ge1/2$, also with the empty-product convention. Thus a single exponent $|\mu(K)|$ works for all active words and attained tuples at this member. For *any* finite place of $K$, and any chosen local generating lattices of $x,v$, the two lists of values in (4) generate exactly the same fractional ideal. At every complex embedding their absolute values also agree on corresponding arguments. These assertions compare the same inputs and their specified images under $q_t$; they do not identify determinant norms of two independent bases at different levels.

At a serving place $w$, the arithmetic lower bound $v_w(A_{t_w}(N_u,M_{t_w}))\ge k_{u,w}$ therefore transfers directly to $v_w(B_u(N_u,q_{t_w}M_{t_w}))\ge k_{u,w}$. Here $M_{t_w}$ is the served integral row, $N_u$ is the unshifted word lattice, and $k_{u,w}$ is the project's integer shift, zero away from the specified support. Since $q_{t_w}M_{t_w}$ generates the localization of the sharp row, dividing the word lattice by $\mathfrak p_w^{k_{u,w}}$ gives an integral map into its dual. The arithmetic content estimate on that tuple is a separate input. The [constructed-family calculation](PERIOD_REFERENCE_INTEGRAL.md) supplies it simultaneously in the word and place on the selected realization under its stated B4.31 and B8.56 kernel, reciprocity, stabilizer and integral row hypotheses. With other choices of constants the weaker statement that the ratio is a unit at this serving place suffices for the same implication.

## Using the comparison without an all-word nonvanishing theorem

Define a rational map $\widetilde B_u$ on every original word lattice. For active words take its native $B_u$, and for all other words take the zero map on the same domain and target. The choice depends only on the vanishing of the actual good-row pairing at the one embedding used by the frame argument. In either branch the resulting map is defined over $K$ and hence has a value at all its places. At an active word (3) gives the common isometric comparison up to its nonzero word scalar. At any other word both $S_u$ and $\widetilde B_u$ vanish, and scalar $1$ gives the same comparison. The zero map is integral everywhere. The nonzero maps obey the just-proved transfer and the [reference-kernel height bound](PERIOD_REFERENCE_MAP_HEIGHT.md) on its stated definite table and metric hypotheses. All original shifted modules and their individual slope allowances are used, including those of a zero map.

For the endpoint application, use the full analytic operators $A_i^{\rm an}$ and their original Gram bounds, ramified embeddings $J_i$ and good projection $P_0$. The comparison just proved gives $Y\widetilde B_i^\sigma=P_0A_i^{\rm an}J_iX_i$ with a common invertible target coordinate change and invertible wordwise source changes (absorbing the nonzero scalars). If the projected analytic operator vanishes, this equality holds for the zero map on the entire source. In particular the sums of images of **arbitrary** source filtration subspaces have the same dimensions on the two sides. The integral-map slope argument uses just these dimensions, heights of nonzero maps, and the original source and target lattice slopes. It gives the same bound with identical rank sums, errors and thresholds. Neither testing the sign of a real period effectively nor paying a loss for dropping a word is required by this existence proof. [Original Gram-to-slope proposition](../../../research/modules/spectral/gram_frame/gram_frame_section.tex#L44-L113) · [Comparison on all subspace images](PERIOD_IMAGE_SPANNING.md)

Thus strict nonvanishing on every word can be removed as an independent input for the **endpoint slope deduction**, even upstream of an all-word diagonal estimate on the point. For the literal assertions about every original map, a word where $S_u=0$ but the original rational $B_u\ne0$ cannot satisfy the original entry 4. The one-way implication (1) alone does not rule out that case. The stricter construction of full reference anchors, where needed elsewhere in the selector or for identifying those original maps, remains separate. Completing the endpoint route still requires the joined realization with (1) on its actual tests, the serving arithmetic bound and the other period and spectral inputs.

More explicitly, the signed covolume expression of entry 7 uses the chosen row components and lattices, their layer ranks, served theta-image and pairing indices, the assigned $h_u$ and the dual row slope. This substitution changes none of them. The adjusted source slopes $\mu_j(N'_u)-h_u$ are still averaged with multiplicity $\operatorname{rank}N'_u$ on **every** word. The set of words kept in that sum is the original set. The span on a word with zero good projection is already zero for every filtration step. Thus the signed inequality still has to be proved on the original rows with its original numerical precision. [Signed base-to-sharp comparison](PERIOD_SIGNED_LEVEL_TRANSFER.md)

## A quantitative test at the prescribed level from aggregate moments

There is also a bound for the dimension lost to zero restrictions at the good row. It works on the fixed prescribed levels, provided aggregate moment information is available on those levels. Use the normalized full operators $A_i^{\rm an}$ and put $Q=\sum_i A_i^{\rm an}(A_i^{\rm an})^*$, $t=\operatorname{tr}Q>0$, $D=\dim\mathcal H$ and $M=\sum_i\dim\mathcal V_i$. Here $J_i:V_i\to\mathcal V_i$ are the original ramified isometries. Write
$$
 \delta=\operatorname{codim}(\operatorname{im}P_0)/D,\quad
 v=D\operatorname{tr}(Q^2)/t^2-1,\quad
 e=M^{-1}\sum_i\|(A_i^{\rm an})^*A_i^{\rm an}-1\|_{\rm HS}^2 .
$$
Let $z=M^{-1}\sum_i\dim\ker(P_0 A_i^{\rm an}J_i)$, counting all invisible directions in the retained word spaces. Then
$$
 z-\sqrt{ez}\le B,\qquad
 B=(t/M)\big(\delta+\sqrt{\delta(1-\delta)v}\big),\qquad
 z\le \tfrac14\big(\sqrt e+\sqrt{e+4B}\big)^2.                 \tag{5}
$$
Choose orthogonal projections $L_i$ in the full word spaces onto the $J_i$-images of the indicated kernels. Their ranks sum to $zM$. The sum of the diagonal traces gives
$$
 \sum_i\operatorname{tr}\big(L_i(A_i^{\rm an})^*A_i^{\rm an}\big)\ge zM-M\sqrt{ez}
$$
by Hilbert–Schmidt Cauchy–Schwarz. Each $A_i^{\rm an}L_i$ takes values in $\ker P_0$. Positivity and $L_i\le1$ bound the same sum by $\operatorname{tr}((1-P_0)Q)$. Center the two matrices by $\delta I$ and $(t/D)I$. Their squared Hilbert–Schmidt norms after centering are $D\delta(1-\delta)$ and $t^2v/D$, respectively. This gives the first inequality in (5), and solving the quadratic in $\sqrt z$ proves the last. In particular the fraction of the total full source rank carried by completely inactive retained word spaces is at most this last quantity. The cap also applies to the kernels on the active words. The original aggregate Gram bounds give $v\le5\tau$, $e\le e_0$ and $t/M\le1+\sqrt{e_0}$; the last inequality follows by pairing the diagonal errors against the identity matrices. More generally, $z\to0$ follows if $e,\delta,\delta v\to0$ and $t/M$ stays bounded. This tests actual projected nonvanishing for any group of words of larger retained rank than the right side of (5) times $M$. It does not assume that every individual word already has a witness. The endpoint substitution itself does not charge this rank deficit and needs no estimate of $z$.

[hom]: https://github.com/rh-lean-roadmap/rh-lean-roadmap/blob/02a95b4c62db610642af5f278ee5d0d6df87b348/docs/src/book/main.tex#L44358-L44410
[step]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AbelianVarietyTheory/Proofs/DecoratedLatticeProofs/SeeSawDoubleStepLinearRelationsPeriods.lean#L82-L149
[frame]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AbelianVarietyTheory/Proofs/DecoratedLatticeProofs/SeeSawKernelLiftCombinationOfDefiniteClassData.lean#L14-L49
[factors]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AutomorphicArithmetic/ThetaCorrespondence/ThetaPairLifts/ThirdPlaceSeries/LawsLinksOfGeoRowsCols.lean#L155-L189
[col]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AutomorphicArithmetic/ThetaCorrespondence/ThetaPairLifts/ThirdPlaceSeries/ColSide.lean#L55-L75
[roots]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AutomorphicArithmetic/ThetaCorrespondence/ThetaPairLifts/ThirdPlaceSeries/ColSide.lean#L181-L221
[total]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AbelianVarietyTheory/Proofs/DecoratedLatticeProofs/SeeSawTotalConstantRatioOfFactorRatios.lean#L24-L71
[phases]: https://github.com/rh-lean-roadmap/rh-lean-roadmap/blob/02a95b4c62db610642af5f278ee5d0d6df87b348/docs/src/book/main.tex#L43652-L43694
