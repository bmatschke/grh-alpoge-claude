# The generic corank-one frame mean and partner count

Use the original base flag $F$ and the actual set of row-lattice representatives with weights $w_\Lambda$. Write $r=r_S\ge1$, $s=r+1$, $m=2s$, $k$ for the definite rank, $N=T_u^f$, $g=g_0g_1$, and $h_C(Z)=\mathrm{HHZ}(b,C,Z)$. Use the compact dimensions and local factors $n_\tau(Z)$ of [the critical product](SPECTRAL_CRITICAL_PRODUCT_ON_ROWS.md). For the generic collision count there is a uniform $C$ such that

$$
 \mathbb E_{\rm row}\#\{\text{generic frame classes with label }Z\}
     \le h_C(Z)^{Cr^2}\prod_\tau n_\tau(Z).                              \tag{1}
$$

Here $\mathbb E_{\rm row}$ is the normalized $w_\Lambda$-weighted sum. A frame has label $Z$ when its raw cross-Gram matrix is integrally equivalent to $Z$ in the sense specified below. For any fixed represented generic frame $F'$ in one of these lattices, there is also the pointwise bound

$$
 \#\{\text{corank-one partner classes of }F'\text{ with label }Z''\}
       \le C^f\big[h_C(Z')h_C(Z'')\big]^{Cr^2},                         \tag{2}
$$

where $Z'$ is the Gram label of $(F,F')$. Both assertions count the source's frame equivalence classes. The partner in (2) must satisfy the actual isometry and level compatibility in the definition of a collision. These assertions hold for both equal and different words under the original standing hypotheses. [Exact count definitions][counts] · [Bounds and quantifiers][meanstmt] · [Fixed-first-frame statement][partnerstmt]

## Why no hyperplane count appears for a fixed first frame

Let $H'$ be the orthogonal complement of the two complete frame spans for $F,F'$, and denote by $P$ the projection of $\Lambda\cap H'$ to the definite rank-$k$ quotient $L=L_0(\Lambda,F)$. The combined frame Gram matrix is invertible. Consequently $H'$ has dimension $k-1$ and meets the isotropic space $X_F$ trivially. For any partner and its isometry $\beta$, the common subspace $\Theta_\beta$ is the first projection of pairs $(x,y)\in H'\times H''$ such that

$$
                         x-y\in X_F,\qquad \beta x-y\in X_{F''}.
$$

Corank one means $\dim\Theta_\beta=k-1$, so $\Theta_\beta=H'$. In particular this first projection is the same space for every counted partner. Its integral image $P$ has rank $k-1$ and lies in $L$. [Source subspaces and corank][theta] · [Rank and projected lattice][pierank]

It remains to check that this *integral* $P$ lies in the partner's projected perpendicular lattice. For $x\in\Lambda\cap H'$, choose $y\in H''$ in the displayed relation. The level compatibility gives integral corrections $x'\in\Lambda\cap X_F$, $x''\in\Lambda\cap X_{F''}$ and $l\in\Lambda$ satisfying

$$
               gl=(x-y-x')+(-\beta x+y-x'').
$$

In particular $l$ belongs to the combined rational span of $F,F''$. Genericity gives $gl$ in the sum of the two integral half-frame lattices there. Write $gl=p+q$ from those lattices. The two complete spans of $F,F''$ are independent by nonsingularity. Comparing components gives $x-y-x'=p$ and hence $y=x-x'-p\in\Lambda$. Its projection is the same as that of $x$. This proves the inclusion for every partner. Unimodular discriminant gluing bounds $\det P$ by the first frame's normalized Gram determinant, which is at most $h_C(Z')$. The source uses the square root of the additive discriminant-module order as this determinant. [Integral partner lifting][partnerlift] · [Determinant bound and use on all partners][partner]

Put $H=h_C(Z')h_C(Z'')$ and $\Delta=\max(1,\det P)$. Then $N,\Delta\le H$. The [fixed-sublattice frame-fibre calculation](SPECTRAL_FLAG_PAIR_FIBRES.md) in complementary rank one bounds the number of second-frame classes containing this very $P$ by

$$
                   N^{2r}\Delta^r9^f H^{9+9r+16r^2}.
$$

It counts the integral graph lifts, the residual line's cofactor vector, and the remaining integral shears on that same row lattice. Forgetting $\beta$ gives precisely the upper bound on frame classes requested in (2). One obtains $9^f H^{9+12r+16r^2}\le C^fH^{Cr^2}$ for $C\ge37$ and $r\ge1$. If the partner set is empty the same inequality holds. No averaging is used in this argument. [Source specialization of the fibre count][countfibre]

## Summing the first frames on the actual row

Set $H=h_C(Z)$ and define the determinant cutoff

$$
     G=\frac{\prod_\tau G_\tau(Z)}
             {|N_{E/\mathbf Q}(g)|^{r+1}},\qquad
     a=\left(\frac{e\pi}{kv}\right)^{kf},\qquad
     \prod_\tau n_\tau(Z)=a(G/N)^k.                                   \tag{3}
$$

For represented generic frames the projected integral perpendicular $P\subset L$ has rank $k-1$ and determinant at most $G$. This uses the generic determinant computation with the finite level divided out. Consequently a represented class has $G\ge1$. For an unrepresented relative-point label the count vanishes. On a relative-point label the local Gram values are nonnegative when represented by a physical frame. For labels outside the physical support the product in (3) is nonnegative as $k$ is even. We may therefore restrict the count to represented labels. The height estimate supplies $N,G\le H$. For a fixed such $P$, the uniform fibre bound is

$$
                         B=N^{2r}G^r9^fH^{9+9r+16r^2}.                 \tag{4}
$$

Every first-frame class is covered by one of these fibres. [Actual support, determinant, and covering by sublattices][first]

The primitive genus input in complementary rank one is the following. For each integer $1\le d\le G$, let $C_{k-1}(L,d)$ count saturated hyperplanes of determinant $d$. Then

$$
 \mathbb E_{\rm row} C_{k-1}(L,d)
       \le (d/N)^{k-1} a Q H^{11+3\log_2 f},\qquad
 Q=(2k\sqrt{\operatorname{rd}(E)})^f h_E2^f ,
$$

where $h_E$ is the class number of $E$. This applies to the actual row representatives. Their projected lattices give the genus with cyclic split-level discriminant of order $N^2$, and their total weights in each isometry class are proportional to the reciprocal automorphism orders. The split-level genus mass is at least $M_k N^{k-1}$, since the local hyperplanes contribute $[(T_u^k-1)/(T_u-1)]^f$. For a primitive hyperplane, count its definite complement of rank one and glue the two lattices along their discriminant modules. The [paired genus calculation](SPECTRAL_PAIRED_GENUS.md) applies to positive ranks on both sides. The native primitive bound uses the refined corank-one gluing estimate, $M_1\le h_E2^f$ and $M_{k-1}/M_k\le(2k\sqrt{\operatorname{rd}(E)})^f a$ from the adjacent unitary mass ratio. The original threshold also gives $Q9^f\le H$ for a fixed enlargement of $C$. [Primitive bound and transfer of row weights][primitive] · [Class number and root discriminant allowance][classnum]

Here is a short alternative to the polynomial divisor sum in the native proof. Let $j=k-1$, and let $a_j(n)$ count sublattices of additive index $n$ in a fixed projective rank-$j$ lattice. This number is independent of its ideal class. At each finite place the projective lattice is free and triangular form gives its local index series. Multiplication over places gives $\sum_n a_j(n)n^{-z}=\prod_{i=0}^{j-1}\zeta_E(z-i)$. If a sublattice has index $n$ in its saturation of determinant $d$, its determinant is $nd$. Summing the preceding positive bounds using $\sum_{d\le x} d^{k-1}\le x^k$ for $x\ge1$ yields

$$
 \mathbb E_{\rm row}\#\{P\subset L :\operatorname{rk}P=k-1,\ \det P\le G\}
 \le a(G/N)^k N Q H^{11+3\log_2 f}\prod_{t=2}^{k}\zeta_E(t).
$$

The last product is at most $e^{2f}$. Indeed $\log\zeta_E(t)\le2f\log\zeta(t)$, and summing $\log\zeta(t)\le\sum_{n\ge2}n^{-t}$ over $t\ge2$ gives $\sum_{n\ge2}[n(n-1)]^{-1}=1$. This keeps exactly the $k$th power of $G/N$. [Index series and saturation convention](SPECTRAL_FLAG_PAIR_FIBRES.md)

Multiply by (4), use $Q9^f\le H$, $e^{2f}\le9^f\le H$, and $N,G\le H$. The result is

$$
           \mathbb E_{\rm row}\#\{\text{first frames}\}
            \le a(G/N)^k H^{23+12r+16r^2+3\log_2 f}.
$$

Since $\log f\le\sqrt r$ and $r\ge1$, the exponent is at most $57r^2$. This proves (1) for $C\ge60$ and the fixed thresholds of the class-number and frame-fibre estimates. Equations (1) and (2) use the same classes as the native corank-one row argument. [Assembly of the two actual word counts][assemb]

## From the two frame counts to the original spectral pairs

For a nonzero relevant term $t$, let $Z_t=\widehat Z(F,F'_t)$ be the raw cross-Gram matrix. Its chosen reduced label $x_t$ satisfies $x_t=L Z_t U$, with $L$ lower and $U$ upper unitriangular over $\mathcal O_E$. Equations (1) and (2) accept any relative-point label in this equivalence class. Indeed the leading $j\times j$ block transforms by the two leading triangular blocks. Every leading determinant stays fixed, hence so do $G_\tau,h_C,n_\tau$. The same relative point still works in the signed Bruhat cell defining relevance. Reduction supplies a useful size bound on the other minors. The count with a chosen label $x$ therefore means all frames with cross-Gram equivalent to $x$. In sums where $x_t$ is chosen separately for each term, the fibre $x_t=x$ is contained in that count, regardless of how the choice was made. [Integral Gram equivalence][zrel] · [Generic-frame counting][zclasseq] · [Choice of reduced label][reduced] · [Invariants and relevance][zinvar]

On one row $\Lambda$, each concrete term is a double-coset class of a moving frame. Its counting class allows the unipotent stabilizer of the base frame on the left and an integral upper unitriangular basis change on the moving frame. On the actual row lattice every such basis change is realized by a unipotent lattice isometry stabilizing the moving flag. In split coordinates the top $r\times r$ block acts on the isotropic summand and by its inverse conjugate transpose on its dual. A Heisenberg translation realizes the last-column shear of the terminal vector $z'$ by the isotropic basis. For this translation use an integral vector pairing to $1$ with $z'$ and an integral $\theta$ with $\theta+\bar\theta=1$ to choose its central correction. Thus frame equivalence puts the two representatives in exactly the same double coset. Equality of the row and the frame class implies equality of the terms. The original pair indexing is isomorphic, compatibly with both projections, to a subset of the Cartesian product of the concrete term set with itself. Two pairs with equal first and second terms are consequently equal. These constructions apply to every ordered pair of words. [Integral realization of basis changes][frameop] · [Application to every actual word pair][frameword] · [Original double-coset identification][termeq] · [Term and pair projections on the actual source][pairproj]

The lattice version also explains why different relative isometries cannot introduce an extra factor in a generic corank-one fibre. Fix the two moving frames $F',F''$ and put $X'=X_{F'}$ and $X''=X_{F''}$. Let $\beta_1,\beta_2$ satisfy the common pair and level conditions and have corank one. Write $H'=(X_F^++X_{F'}^+)^\perp$ and define $H''$ similarly. For $x\in H'$, each corank-one condition gives a $y_i\in H''$ with $x-y_i\in X_F$ and $\beta_i x-y_i\in X''$. But $y_1-y_2\in X_F\cap H''=0$ by nondegeneracy of the combined span of $F,F''$. Thus $\gamma=\beta_1^{-1}\beta_2$ fixes the image of $H'$ in $(X')^\perp/X'$. It fixes the terminal vector $z'$ as well. The perpendicular to $z'$ in this quotient is definite of dimension $k$, and the image of $H'$ there has dimension $k-1$. Its remaining perpendicular line is nondegenerate and $\gamma$ acts on it by a scalar $\mu\in E$ with $\bar\mu\mu=1$. [Agreement on the common perpendicular][betaagree] · [The remaining line][betaline]

For clarity, take the inverse image $W$ of the remaining line in $(X')^\perp$ and let $I$ be the image of $\Lambda\cap W$ in $W/X'\cong E$. It is a nonzero fractional ideal. Lattice preservation gives $\mu I\subset I$, so $\mu\in\mathcal O_E$. At every prime $\mathfrak p\mid g$, the two pair markings compare a lift $y$ in the moving-frame perpendicular with the same base-frame representative modulo the level and the isotropic sublattices. Subtraction and pullback by $\beta_1^{-1}$ give $(\gamma-1)y\in g\Lambda_{\mathfrak p}+(\Lambda\cap X')_{\mathfrak p}$. An integral representative on the base side exists locally by unimodularity and the admissible level marking. For $y\in W$ the $g$-multiple in this difference also lies in $W$ since $X'\subset W$, so $(\mu-1)I_{\mathfrak p}\subset gI_{\mathfrak p}$. At primes away from $g$ integrality of $\mu$ suffices. It follows that $(\mu-1)/g$ is integral. Every complex embedding has $|\sigma(\mu)|=1$. Since $g=g_0g_1\ge3$, every conjugate of $(\mu-1)/g$ has absolute value $\le2/g<1$. The integer absolute norm forces $\mu=1$. This proves $\beta_2x-\beta_1x\in X''$ for every $x\in(X')^\perp$. This is precisely the quotient on which the pair equivalence compares the two maps. [Local subtraction of the two markings][betacong] · [Integrality on the line and CM norm][betanorm] · [Passage to abstract pair indices][betatop]

Fix a finite set $S$ of relevant, generic corank-one pairs with nonzero Gram determinants and chosen labels $x,y$ in their respective coordinates. Group them by the row and then by the first term's frame class. The first class determines the first term and hence its chosen representative. Each remaining pair now gives a partner of that representative. Equal second-frame classes give equal second terms, and therefore equal pairs. For the abstract row formulation the quotient uniqueness just proved gives equality by the same triple equivalence, with identity frame changes once the two terms have been identified. Thus (2) bounds each fibre and (1) bounds the normalized mean number of first classes. Interchanging the two frames replaces $\beta$ by $\beta^{-1}$, preserving corank one because the two projections of the common relation have equal rank. Applying both estimates gives

$$
 \frac{\sum_{p\in S} w_{\Lambda(p)}}{\sum_\Lambda w_\Lambda}
 \le C^f [h_C(x)h_C(y)]^{Cr^2}
       \min\!\left\{h_C(x)^{Cr^2}\prod_\tau n_\tau(x),\,
                      h_C(y)^{Cr^2}\prod_\tau n_\tau(y)\right\}.      \tag{5}
$$

The normalized weight on the left is the original pair mass on each index. Formula (5) supplies the two-label count in the corank-one row, including all multiplicities on the tied data. [Original normalized pair weight][pairmass] · [Both fibre injections][injections] · [Inversion and corank][pairswap] · [Native minimum bound][twocount]

[counts]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Formalism/SharpRestriction/CuspSpanNormBounds/CntPartners.lean#L185-L213
[meanstmt]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Formalism/SharpRestriction/CuspSpanNormBounds/CongruenceAtSplitFrobeniusHolds.lean#L291-L303
[partnerstmt]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Formalism/SharpRestriction/CuspSpanNormBounds/CongruenceAtSplitFrobeniusHolds.lean#L569-L580
[theta]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Formalism/SharpRestriction/CuspSpanNormBounds/IsPrimitiveSub.lean#L209-L223
[pierank]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AbelianVarietyTheory/Proofs/FlagMeasures/OneLeProdReal.lean#L220-L285
[partnerlift]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AbelianVarietyTheory/Proofs/FlagMeasures/ExistsPartnerLift.lean#L227-L273
[partner]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AbelianVarietyTheory/Proofs/FlagMeasures/OneLeProdReal.lean#L279-L342
[countfibre]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AbelianVarietyTheory/Proofs/FlagMeasures/CountTermsGramClassOverSublattice.lean#L1-L122
[first]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AbelianVarietyTheory/Proofs/FlagMeasures/CntClLeEncardMul.lean#L198-L249
[primitive]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AbelianVarietyTheory/Proofs/FlagMeasures/MeanPrimitiveCorankOneSublatticesBound.lean#L60-L168
[classnum]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AbelianVarietyTheory/Proofs/FlagMeasures/ClassNumberRootDiscFactorLeHHZ.lean#L1-L85
[assemb]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AbelianVarietyTheory/Proofs/FlagMeasures/RowCountsUniformConstantsFamilies.lean#L25-L47
[zclasseq]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Formalism/SharpRestriction/CuspSpanNormBounds/FlagEEqHyperbolic.lean#L119-L131
[reduced]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Formalism/SharpRestriction/CuspSpanNormBounds/CayleyDegreeNondegeneracy/RowsLab.lean#L33-L52
[zinvar]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Formalism/SharpRestriction/CuspSpanNormBounds/CayleyDegreeNondegeneracy/RowsTrm.lean#L143-L198
[frameop]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Formalism/LocalToGlobal/SiegelLatticeTheory/TraceIntegralEstimates/FrameOpFull.lean#L14-L155
[termeq]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Formalism/LocalToGlobal/SiegelLatticeTheory/FlagStabilizerTensors/TermTieOf.lean#L447-L470
[pairproj]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Formalism/LocalToGlobal/SiegelLatticeTheory/FlagStabilizerTensors/LoopTieOfInhab.lean#L20-L52
[betaagree]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Formalism/PeriodIntegrals/UnitaryGroupMassFormula/BetaUniqueness/AgreeOnH.lean#L12-L47
[betaline]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Formalism/PeriodIntegrals/UnitaryGroupMassFormula/BetaUniqueness/LineReduce.lean#L163-L219
[betacong]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Formalism/PeriodIntegrals/UnitaryGroupMassFormula/BetaUniqueness/FlagVectorMemLocalization.lean#L563-L601
[betanorm]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Formalism/PeriodIntegrals/UnitaryGroupMassFormula/BetaUniqueness/EigenvalueLastLineOne.lean#L116-L197
[betatop]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Formalism/SharpRestriction/CuspSpanNormBounds/CayleyDegreeNondegeneracy/RowsCnt.lean#L607-L646
[pairmass]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Formalism/LocalToGlobal/SiegelLatticeTheory/FlagStabilizerTensors/TermTieOf.lean#L436-L445
[injections]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Formalism/SharpRestriction/CuspSpanNormBounds/CayleyDegreeNondegeneracy/RowsCnt.lean#L403-L477
[pairswap]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Formalism/SharpRestriction/CuspSpanNormBounds/CayleyDegreeNondegeneracy/RowsCnt.lean#L580-L605
[twocount]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Formalism/SharpRestriction/CuspSpanNormBounds/CayleyDegreeNondegeneracy/RowsOneD.lean#L35-L52
[zrel]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Formalism/SharpRestriction/CuspSpanNormBounds/IsPrimitiveSub.lean#L279-L284
[frameword]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Formalism/LocalToGlobal/SiegelLatticeTheory/FlagStabilizerTensors/RootLatticeThresholds/LoopBFrame.lean#L18-L30
