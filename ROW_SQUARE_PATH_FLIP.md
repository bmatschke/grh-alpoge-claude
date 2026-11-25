# From the square integrals to the theta lift along the opposite path

Fix an admissible grid choice with the actual frames, real matching relation and measures of the row construction. Use the standing realization of its square triples with an auxiliary split place outside any prescribed finite set. Suppose that for each square and twist its number $c_{ij,t}$ satisfies the pointwise integral identity in the choice. We prove what this implies for the iterated lift. Write $D_t y$ for the column input supplied by the datum. With the ordinary local theta and cuspidal tower inputs of the row construction there is a common real polynomial tensor on the opposite path. For each $t$ there is a character phase $z_t$, chosen before the finite datum $\Phi$. One can choose a finite representative of its prescribed flipped tensor before the measure and $y$ are known. With these choices the opposite path converges termwise and
$$
 L_{\rm opp}(t,\Phi,y)
   =z_t\left(\prod_{i,j<m}c_{ij,t}\right)\theta_\chi(\Phi,D_ty).
$$
Here the two sides are actual functions on the final group. This direction of the identity also holds when a square constant vanishes. The normalized inverse identity used later requires all the constants to be nonzero. The [tower induction](ROW_TOWER_INDUCTION.md) supplies the pointwise comparisons, nonzero witnesses and invertible constants on every prescribed square under its stated inputs. [Pointwise and integrated statements][sq] · [Initial path and phase][start] · [Original inverse formulation][inv]

## Integrating one square against a cusp form

Write $g$ for the entering endpoint, $h$ for the fixed exiting endpoint and $u$ for the intermediate variable. Write $K_b(g,u;h)$ and $K_s(g,u;h)$ for the two finite sums of products of theta kernels. A right translate on the small intermediate group means $u\mapsto uk$. Fix a smooth listed cusp form $F$ at the entering endpoint, and assume the pure two-arrow iterates occurring in both matched sums converge. These are the hypotheses defining commutation on cusp forms. All the measures below are the quotient measures of this choice. [Precise domains and functions][sq]

On the big route, each product of theta kernels is, up to a scalar of bounded modulus, the theta kernel on the orthogonal sum of the endpoint spaces. This is the tensor product rule for the Weil representation with the given splitting characters and block embedding. Write $b$ for the rank of the intermediate space and $d$ for the sum of the two exterior ranks. The realized triple gives a real signature $(b-p,p)$ and $d<2(b-p)$. The [Siegel-set estimate](ROW_PERIOD_JET_FORMULA.md#convergence-in-the-range-used-for-a-square) bounds the integral of the absolute value by a polynomial in the height of the exterior block. The block height is bounded by a fixed constant times the product of the two endpoint heights. Left rational invariance at the first endpoint allows us to take a representative of height at most twice its quotient height $H(g)$. Summing the finitely many terms gives
$$
 \int_{[U_b]} |K_b(g,u;h)|\,du\ \le C_h(1+H(g))^{A}.
$$
The constants may depend on the tests and the measure. The rapid decay of $F$ on its finite-volume quotient makes the right side integrable after multiplication by $|F(g)|$. [Rank inequality][range] · [Product kernel and absolute convergence][big] · [Moderate growth of the integral of the norm][growth]

On the small route use the [primitive-frame translate](ROW_SQUARE_REGULARIZATION.md#absolute-convergence-at-a-fresh-split-place) at one split place outside the finite supports. Normalize its coefficient sum to one, and denote the operator by $R_z$. The combination is chosen for the tests and $h$ and works for every $g$. In the barred split model the translated Schwartz data have full-row-rank support at that place. The comparison with the joint theta kernel is pointwise in both $g,u$, with an exterior phase of absolute value one. [Translate and the joint kernel][trans]

Here is the dependence on the previously variable endpoint. In the two Siegel sets write $s,t'$ for the nonnegative decreasing logarithmic torus coordinates, $S=\sum s_i$, $T=\sum t'_j$ and $n$ for the small intermediate rank. Pad the lists with zeroes in prefix sums and put
$$
 v=\max_{0\le i\le \#s}\left(\sum_{j\le i}s_j-\sum_{j\le i}t'_j\right).
$$
Indices in these two sums start at $1$. Then $v\ge0$ and $S\le T+v$. For a full-row-rank rational matrix the $i$ rows with largest expanding weights admit a nonzero $i$-column minor. After clearing one finite denominator, the product formula bounds some archimedean absolute value of the unscaled minor below by a fixed positive constant. The column weights cost at most the sum of the $i$ largest positive endpoint weights. Expanding the determinant therefore gives $e^v\ll (1+\|Y_{\rm scaled}\|)^{n+1}$, uniformly in the lattice matrix. In the Poisson estimate for the squared theta sum, spend $M(n+1)$ powers of Schwartz decay on this minor and use the remaining powers to sum the lattice majorant. Counting in each real weight coordinate costs the positive weight sum, at most $dS+nT$. With $D=[E:\mathbb Q]$ the result, for any integer $M\ge0$, is
$$
  |\theta(u,h_{\rm ext})|^2\ll_{\Phi,M}
            \exp\{D(dS+nT)-Mv\}.
$$
This estimate is on the full-rank part picked out by the finite place. Compact Siegel factors change its constant. [Weight and prefix sums][weights] · [Minor estimate][minor] · [Summation with extra decay][lat] · [Two-variable estimate][semi]

Reduction theory gives $H(u)\ll e^{kS}$ and $e^T\ll (1+\operatorname{ht}(h_{\rm ext}))^{k'}$. Given $N$, take an integer $M\ge Dd+2kN$. Then
$$
 D(dS+nT)-Mv+2kNS\ \le\ (M+Dn)T .
$$
Consequently $H(u)^N|\theta(u,h_{\rm ext})|$ has a polynomial bound in the height of the exterior block. Set $N=0$, take $h_{\rm ext}$ to be the block of $g,h$, and reduce $g$ by rational invariance. This gives a bound $C'_h(1+H(g))^{A'}$ for the absolute value of the translated kernel, uniform in $u$. Since $[U_s]$ has finite volume, $F(g)R_zK_s(g,u;h)$ is absolutely integrable on the product of the two quotients. [Torus height estimates][heights] · [Reduction in the entering variable][both]

The pointwise square law for this degree-one translate now gives
$$
 \int F(g)\int K_b(g,u;h)\,du\,dg
       =c_{ij,t}\int F(g)\int R_zK_s(g,u;h)\,du\,dg .
$$
On the left, Fubini gives the ordinary big two-arrow lift. On the right, first apply Fubini to the **translated sum**. For a fixed $u$ expand the finite sum and integrate in $g$. For a pure test with kernels $K_1,K_2$, the term at $k$ is now
$$
 K_2(uk,h)\int K_1(g,uk)F(g)\,dg .
$$
Its $u$-integral converges by the assumed iterated convergence and right invariance of quotient measure. This integral equals the ordinary two-arrow term, independently of $k$. Summing with coefficients $z(k)$ gives it once. Thus the big lift equals $c_{ij,t}$ times the small lift at every $h$. The exchange of order required absolute integrability only after the translates had been combined. [Fubini on the big route][fub] · [Translation on a fundamental domain][right] · [Sum of the translated outer integrals][outer]

## Flipping the whole path

The given path descends from $(0,m)$ to $(0,0)$ and then moves right to $(m,0)$. Flip the squares $(i,j)$ in increasing $i$, and in increasing $j$ within each $i$. Before each flip the path contains the two arrows through $(i,j)$. Replacing them by the arrows through $(i+1,j+1)$ leaves the endpoints fixed. After the flip at $j=m-1$ for a given $i$, the horizontal step with that $i$ has moved from the bottom to the top. After $m^2$ flips the path runs along the top and then descends its right boundary. [Order and intermediate edges][order] · [Product over the squares][prod]

At infinity choose a linear section of the projection of each real matching relation onto its small polynomial tensor space. Such a section exists by surjectivity over $\mathbb C$. Apply it to the two polynomial factors at that square and expand its image in a finite sum of pure big tensors. Retain all other polynomial factors. Starting with the real polynomial for the given path defines the final polynomial once for every tuple and finite test. The initial polynomial comes from the given column intertwiners. The initial finite representatives on the descending path can be chosen for each $t$ with a single phase $z_t$ in the subgroup generated by the values of its finite-order character. The finite swapped-pair comparison fixes this phase for the chosen column vectors before $\Phi$ is inserted on the other part of the path. With this convention the starting lift is $z_t\,\theta_\chi(\Phi,D_ty)$. [Real lift of the matching relation][pol] · [Finite swapped-pair calculation][phase] · [Initial identity with its quantifiers][start]

At a marked finite place use the prescribed local flip at the given level. The tensor at each successive stage has integral support on its path coordinates and is constant modulo the specified depth. Split the coordinates of the path before and after the square into their finitely many residue classes. Their class indicators factor over the spectator arrows; the two sets of such arrows are disjoint and avoid the four edges of the square. Holding one class fixed leaves a two-arrow test of the prescribed depth. Applying the local flip to this slice gives exactly the slice of the new tensor, since the operator acts only in the two changed matrix variables. Take products over the finite marked set and the fixed vacuum at the other places. In the prescribed polarizations the resulting finite class sums represent the old and new adelic tensors with identical spectator factors. Equality of two such representations on the chosen half-space gives equality of their Fock tensors and lifts: the common local intertwiners are linear, and the products of the Schwartz functions agree on the independent edge variables. [Support and level at each stage][depth] · [Separation into spectator classes and matching of slices][slice] · [Change of finite representative in the lift][represent]

For each pure summand apply the initial part of the path to the listed cusp form. The cuspidal transition for the prescribed finite test and any Fock polynomial gives both absolute convergence and another listed cusp form. Iteration proves this for the common initial segment, then for either pair of middle arrows, then for the common final segment on each pure middle output. Apply the two-arrow identity to the function at the end of the initial segment. Linearity of the final segment on these convergent finite sums gives $L_{\rm new}=c_{ij,t}L_{\rm old}$. Termwise convergence came from the cuspidal transition even when the sum vanishes. Induction gives the displayed opposite-path identity. The finite representative was constructed only from the local tensors, independently of the measure and the form. [Convergence and preservation of the listed space][cusp] · [Application before and after the square][sand] · [Construction of the terminal representative][final]

For the period formula one can thus keep all scalars on the left until the last step. The [mixed-cell unfolding](ROW_MIXED_CELL_UNFOLDING.md) supplies its phase $z'_t$ and the common archimedean line. Applying the period to the identity above and using the jet evaluations gives $\iota(e_t)(\prod c_{ij,t})\mathcal P_a(\Theta_t j_t x)=\kappa\,v_{t,a}(x)$ for $x\in\mathrm{goodF}_t$ in the notation of the [period formula](ROW_PERIOD_JET_FORMULA.md), with $\iota(e_t)=z_tz'_t$. The [normalized cross-tuple product](ROW_GRID_PRODUCT.md) and this identity yield the [common-target arithmetic readings](COMPOSITE_ROW_RATIONALITY.md#rational-tests-on-the-actual-weight-supported-column).

[sq]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AbelianVarietyTheory/Definitions/Divisors/ExistsNotRelZero.lean#L207-L225
[start]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AutomorphicArithmetic/ThetaCorrespondence/ThetaPairLifts/LocalTypeDictionary/FlipSequenceStartCondition.lean#L18-L43
[inv]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AbelianVarietyTheory/Proofs/TwistedOperators/FlipOfWeilConvergenceAndTheta.lean#L62-L84
[range]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AbelianVarietyTheory/Proofs/DivisorProofs/SquareThetaTripleExistsSignatureRankAddLt.lean#L15-L53
[big]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AbelianVarietyTheory/Proofs/DivisorProofs/BigRouteKernelIntegrableOnUnitaryQuotient.lean#L19-L39
[growth]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AbelianVarietyTheory/Proofs/DivisorProofs/ModerateGrowthIntegralNormKernelBigVertexRoute.lean#L18-L53
[trans]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AbelianVarietyTheory/Proofs/DivisorProofs/TranslatedKernelLeThetaFunctionRouteBigVertex.lean#L38-L76
[weights]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/WeilBound/ThetaLifts/FrameEstimates/InitialPairs/SquareIntegrableIntegralHolds.lean#L94-L120
[minor]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/WeilBound/ThetaLifts/FrameEstimates/ExistsColsDetNeZero.lean#L93-L164
[lat]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/WeilBound/ThetaLifts/FrameEstimates/LatFull.lean#L13-L47
[semi]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/WeilBound/ThetaLifts/FrameEstimates/SoSemi.lean#L22-L102
[heights]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/CompanionTheory/ThickeningEstimates/SiegelDomainEstimates/SquareIntegrableWeilRange.lean#L61-L74
[both]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AutomorphicArithmetic/ThetaCorrespondence/ThetaPairLifts/LocalTypeDictionary/ExistsRegulariserAtPlace.lean#L30-L64
[fub]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AbelianVarietyTheory/Proofs/DivisorProofs/ThetaLiftEqIntegralRouteKernelFubini.lean#L29-L87
[right]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AbelianVarietyTheory/Proofs/DivisorProofs/SmallRouteCombinationMulLiftByDegree.lean#L18-L46
[outer]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AbelianVarietyTheory/Proofs/DivisorProofs/SmallRouteSumTranslatedOuterIntegralsEq.lean#L20-L65
[order]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AbelianVarietyTheory/Definitions/Divisors/ExistsGivenStageEqOne.lean#L18-L40
[prod]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AbelianVarietyTheory/Proofs/TwistedOperators/FlipOfWeilConvergenceAndTheta.lean#L29-L56
[pol]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AbelianVarietyTheory/Proofs/TwistedOperators/RangeSndRel.lean#L74-L141
[phase]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AutomorphicArithmetic/ThetaCorrespondence/ThetaPairLifts/LocalTypeDictionary/TwistedThetaFirstOccurrenceFiniteSwappedPair.lean#L14-L34
[depth]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AbelianVarietyTheory/Proofs/TwistedOperators/LocalFlipStageIsTensorPlaceDepth.lean#L24-L51
[slice]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AbelianVarietyTheory/Proofs/TwistedOperators/GridSquareFlipSmallRouteEqInvSmulBigRoute.lean#L193-L272
[represent]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AbelianVarietyTheory/Proofs/TwistedOperators/GridSquareFlipSmallRouteEqInvSmulBigRoute.lean#L315-L333
[cusp]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AbelianVarietyTheory/Proofs/TwistedOperators/RangeSndRel.lean#L143-L149
[sand]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AbelianVarietyTheory/Proofs/TwistedOperators/SandwichedFlipRouteThroughSmallEqInvConstRouteBi.lean#L163-L190
[final]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AbelianVarietyTheory/Proofs/TwistedOperators/FlippedFiniteTensorOfRepresentingOppositePath.lean#L440-L465
