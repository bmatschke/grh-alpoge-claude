# The terminal row double lift in entries 1 and 4

At the last pair $j=m-2$, the original row Bessel period of **two downward lifts** can be evaluated by an ordinary compact integral. The test on the definite column remembers both row tests, their finite translates, and the rational identification of the two complementary lines. The integral identity below holds before taking sums over finite charts. The subsequent conversion to the marked arithmetic recurrence has additional hypotheses at the finite places.

## The row integral

Write $A=X_j,\ S=X_{j+1},\ X=X_{j+2}$, $V=V_j,\ W=V_{j+1}$, and let $T$ be the terminal row space. Write $[H]=U(H)(F)\backslash U(H)(\mathbb A_F)$. The rank-zero terminal Witt decompositions identify $V$ with $V_0=A\perp L$ and $W$ with $S$. Write $d:S\to W$ for the latter isometry, $\alpha:U(A)\to U(V)$ for the first embedding, and $\iota:U(T)\to U(X)$ for the inclusion of the first summand in $X=T\perp L''$. Use the matching Weil splittings, standard additive character, and rational comparison of lines of the given terminal geometry. In particular, in the original Gram convention,
$$
 \tau^*H_L\tau=-\xi_0\bar\xi_0 H_{L''}.
$$
Let $\omega_1,\omega_2$ be the row Weil actions for $(V,W),(W,T)$, and $\eta_1,\eta_2$ their prescribed column counterparts for $(A,S),(S,X)$. Evaluation of a Weil translate at zero denotes the theta kernel in the source's adelic model. [Prescribed rank-zero geometry and actions][rowred] · [Opposite-line identity][rowline]

For admissible row theta tests $\Phi_1,\Phi_2$, put
$$
 (\mathcal L_1^{\Phi_1}H)(v)=\int_{[W]}(\omega_1(v,w)\Phi_1)(0)\,H(w)\,dw,\qquad
 (\mathcal L_2^{\Phi_2}F)(w)=\int_{[T]}(\omega_2(w,h)\Phi_2)(0)\,F(h)\,dh.
$$
The row period of a continuous automorphic input pair is $\mathcal P(\phi,G)=\int_{[A]}\phi(x)G(\alpha x)\,dx$. Indeed the unipotent radical in the Bessel integral is the identity group since its isotropic flag has length zero. Its character is $1$ and its specified mass is $1$. This is a bilinear period. The star in the Bessel character disappears at rank zero. [Rank-zero Bessel period][rowfu]

Let $R_b f(x)=f(xb)$. For $g\in U(V)(\mathbb A_F), b\in U(W)(\mathbb A_F), b_T\in U(T)(\mathbb A_F)$, pull $\omega_1(g,b)\Phi_1$ to the model for $(V_0,S)$, obtaining $\Xi$, and pull $\omega_2(b,b_T)\Phi_2$ to the model for $(S,T)$, obtaining $\widetilde\Phi_2$. These are the actual rank-zero pullbacks. Both unipotent Fourier maps at rank zero have zero-dimensional blocks and the remaining average has mass one. For $u$ in the oscillator coordinate space for $(A,S)$, split the second oscillator coordinate as $v=(v_T,v_{L''})$ using $X=T\perp L''$. In the coordinates from the two specified orthogonal decompositions put
$$
 C_{g,b,b_T}(u,v)=\widetilde\Phi_2(v_T)\,
       \Xi\!\left(u,{\rm ofAdj}_{L,S}(\tau v_{L''})\right).
$$
Here ${\rm ofAdj}$ is the weighted adjoint on the source's skew-Gram model. The factor and sign in the Gram relation above are part of the formula. [Rank-zero pullback][rowpull] · [Coupled test][rowtest]

For any two-variable test $C$ write
$$
 (\mathcal D^C\phi)(z)=\int_{[S]}\int_{[A]}\phi(x)
  \Big(\eta_2(s,z)\big[v\mapsto
       (\eta_1(x,s)[u\mapsto C(u,v)])(0)\big]\Big)(0)\,dx\,ds .
$$
Use the definite measures $dx,ds$, the geometric middle row Haar $dw=d_*ds$, and the original top row Haar $dh$, each descended to its own quotient. Then for continuous automorphic $\phi,F$,
$$
 \boxed{\displaystyle
 \mathcal P\!\left(\phi,R_g\mathcal L_1^{\Phi_1}\mathcal L_2^{\Phi_2}F\right)
    =\int_{[T]}(R_{b_T}F)(h)\,
       (\mathcal D^{C_{g,b,b_T}}\phi)(\iota h)\,dh .} \tag{1}
$$

**Proof.** Right invariance of the quotient measures replaces $F$ by $R_{b_T}F$ and the tests by the two displayed Weil translates. The middle translates cancel by the change of variable $w\mapsto wb$. The integrand on $[A]\times[W]\times[T]$ is a product of two continuous theta kernels and the two continuous automorphic inputs. Rational invariance descends each factor to the indicated quotients, which are compact here. The product is bounded and the three quotient measures are finite. Fubini therefore moves $dh$ to the outside and $dx$ to the inside. The rational isometry $d$ identifies the middle rational point groups and the adelic groups. Pulling back a fundamental domain in $W$ gives a fundamental domain in $S$, so changing $w$ to $d(s)$ gives exactly $ds$. [Compact quotient Fubini][rowfub] · [Pushforward on fundamental domains][rowmap]

It remains to identify the two kernels at fixed $x,s,h$. Apply the target orthogonal tensor rule to $\eta_2(s,\iota h)$ on $T\perp L''$. The $T$-factor is the second row kernel, pulled back by $d$. On $L''$ the opposite-line rule identifies the action at $(s,1)$ on $f({\rm ofAdj}(\tau\,\cdot))$ with the action at $(1,s)$ on $f$, evaluated at the same adjoint. The target line uses splitting character $\chi_z^{-1}$ while the corresponding source line uses $\chi_z$. The negative Gram identity and the two conjugations in the opposite-line rule give this equality of operators with scalar $1$. Apply the source orthogonal tensor rule on $A\perp L$ to join the $A$-action and this line action. The result is the first row kernel at $(\alpha x,d(s))$; multiplication with the second gives precisely the original product. The two commuting column actions on the separate test variables put this product in the order defining $\mathcal D^C$. This proves (1). [Pointwise tensor calculation][rowseesaw] · [Assembly inside the quotient integral][rowred]

The measure equality used in (1) can be arranged simultaneously for all tuples. Fix a finite Haar $\mu_f$ on the middle group. Let $K_t$ be its registered finite level and $\nu_t$ the tuple's level-normalized adelic Haar. Its compact real factor is probability Haar. The product $\nu_0=\mu_f(K_t)\nu_t$ is independent of $t$ by the common-measure construction. Since $d_*ds$ and $\nu_0$ are Haar measures on that same group, $dw=d_*ds=\kappa_*\nu_0$ with a positive scalar $\kappa_*$ independent of $t$. At the top the analogous construction gives $dh=\mu_{T,f}(K^T_t)\nu^T_t$. Thus replacing the middle Haar by $\nu_t$ *in the definition of the first row lift* would divide its value by $\kappa_*\mu_f(K_t)$. Formula (1) already uses $dw$ on that side. [Construction of both measures and their scalars][rowmeasure]

## Inserting the prescribed finite charts

For a permitted ramified section $\psi$ and frame $y$, write $R_t(\psi;y)$ for its family of chart readings. The marked lower period $\mathcal P^F_{t,j}$ sums $\mathcal P$ over the input charts, with its chart-dependent finite trace on the row function. The marked upper period $\mathcal P^T_{t,m}$ sums the upper restriction integrals against the specified top traces. Write $D_{t,j}^{C}$ for $\mathcal D^C$ with the two prescribed finite column operations inserted and summed over the initial and intermediate charts. These are three different operations even when the set of upper charts is a singleton. [Definitions of the three marked operations][rowdefs]

Take the actual row tests prescribed by $P_1,P_2$, the word's real polynomials. Suppose the tuple readings and translated tests have their registered finite shape, the twists have their local terminal chart identities, the fixed-type contraction holds, and the level-prime integral identity holds on the translated spherical top row. The three finite sets of places are pairwise disjoint. Their finite tests, common vacuum, matching Weil splittings, and level character must all be those of the same realization. Then one common admissible real test $C_*$ satisfies, for every tuple $t$, frame $y$, permitted $\psi$, top multiplicity map $F$, and smooth vector $v$,
$$
 \mathcal P^F_{t,j}\!\left(R_t(\psi;y),
        \mathcal L_1^{\Phi_{t,1}}\mathcal L_2^{\Phi_{t,2}}F(v)\right)
 =
 c^V_{t,j}\,\mathcal P^T_{t,m}\!
       \left(D_{t,j}^{C_*}R_t(S_{t,j}\psi;y),F(v)\right), \tag{2}
$$
where $S_{t,j}$ is the prescribed column correction. In the built finite charts the scalar is
$$
 c^V_{t,j}={\rm sc}_{t,j}{\rm sc}_{t,j+1}\,
 c_{G,j}c_{T,t,j}\prod_{p\ {\rm twist}}
        \frac{1}{{\rm idx}_{p,j+1}{\rm idx}_{p,j+2}} .
$$
The two ${\rm sc}$'s normalize the row tests under the registered base moves; $c_G$ is the fixed-place contraction and $c_T$ is the prescribed level-prime monomial in the tuple's character data. The empty product is one. [Exact scalar in the geometric construction][rowscalar] · [Normalized assertion][rowgoal]

To see the origin of (2), expand the incoming trace as a finite sum of translates and apply (1) in each term, using $g$ times the base move, the registered middle move and the top move. The shape of the two moved row tests pulls out ${\rm sc}_{t,j}{\rm sc}_{t,j+1}$ by bilinearity. The terminal twist chart identity replaces the sum over translates by the two successive finite twist operations with the indicated inverse indices. At each twist place the top chart has cardinality one, so the product top chart has cardinality one. The top trace and its coefficient survive this summation. Disjoint-place operations commute. Applying the fixed-type contraction gives $c_{G,j}$; applying the level-prime identity **under the upper integral** gives $c_{T,t,j}$ and moves $S_{t,j}$ onto the incoming reading. Its test correction is the word's common two-variable operator. Applied to the unshifted coupled test from the common vacua this gives $C_*$. Formula (1)'s rank-zero pullback makes that unshifted test independent of the tuple, and the vacuum law gives the required real-test condition after the correction. The remaining two column operations and chart sums are precisely $D_{t,j}^{C_*}$. [Expansion of the lower trace][rowleft] · [Twist summation including the top trace][rowq] · [Two fixed-place contractions and common test][rowright]

For the twist factor one can check the indices before rescaling the charts by the tagged roots of unity. Put $I_k=\prod_p{\rm idx}_{p,k}$ and $M_\alpha=\prod_p{\rm wt}_{p,j}(\alpha_p)$. The lower trace is $M_\alpha$ times the convolution of the unweighted local traces. By bilinearity the two marked column operations for the intermediate chart $\gamma$ supply $M_\alpha\prod_p{\rm wt}_{p,j+1}(\gamma_p)$. The unweighted local comparison replaces the intermediate **weighted** sum by $I_{j+1}$ times the lower kernel. The single top trace has coefficient $I_{j+2}$, since its local weights equal the top indices. Consequently the chart equation requires the exact cancellation
$$
 (I_{j+1}I_{j+2})^{-1}\, I_{j+2}\, I_{j+1}=1 .
$$
Both indices are nonzero. The argument factors out $M_\alpha$ on both sides without dividing by it, so charts of zero weight cause no exception. Tagged rescalings of the traces and edge kernels must be applied together when passing to the selected geometric columns. [Scalar calculation on the unrescaled local data][rowindices]

If the arithmetic row maps are used in place of the two analytic lifts on the left, the row reading is multiplied by $c^I_{t,j}c^I_{t,j+1}$, with the prescribed two smooth-vector intertwiners applied. These multipliers come from the two original row-map identities. Formula (2) introduces neither an additional $\kappa_*$ nor the interior cell-integration scalar. The latter enters $c^V$ only at positive Bessel index. Combining (2) with the common definite-column frame formula and the common terminal reading gives the last step of the homogeneous recurrence on a realization satisfying the enumerated laws. No division by a row period is involved. Applying this result to every selected realization still requires the finite identities and row readings just specified. Earlier pairs require their positive-rank unfolding with the noncompact middle group. [Original row-map normalization][rowio] · [Finite hypotheses and their assembly][rowpins] · [Definite column](PERIOD_DEFINITE_DOUBLE_LIFT.md) · [Terminal reading](PERIOD_TERMINAL_COMMON_TEST.md)

## Convergence at an interior pair

For an interior pair of indices $(\sigma+1,\sigma)$, one can also supply the two rapid-decay inputs for the **ordered** row unfolding on a realized tuple. Assume the original two row spaces consist of smooth cuspidal multiplicity maps at their registered levels and characters, cusp rapid decay holds for their smooth evaluations, and the upper one-step lift has the tuple's specified arithmetic reading. Then $G(v)$ is rapidly decreasing on $V_{j+2}$. On $V_{j+1}$ the *actual* inner lift is $c^I_{t,j+1}(\mathrm{io}_{t,j+1}G)(\mathrm{It}_{j+1}(P_2,v))$, so it too is rapidly decreasing with the prescribed test and Haar measure. For the original linked mixed models, continuous automorphic column reading and admissible row theta tests, the Bessel-to-Fourier–Jacobi one-edge estimate therefore gives an absolutely integrable function of the outer stabilizer coset $h_1$. At each fixed $h_1$, the reverse one-edge estimate gives an absolutely integrable function of the inner stabilizer coset $h_2$ whose integral is that outer function's value. The common measure on each stabilizer quotient is the one determined by its prescribed subgroup and ambient Haar measures. The proof has used the decay of the *already integrated* inner lift in the outer estimate. Reversing two noncompact integrations would require further control of the integral of the absolute two-variable kernel. Evaluating the finite cells and the real averages of the ordered integral is a separate part of the interior recurrence. [The two decay deductions on this very row](https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AbelianVarietyTheory/Proofs/DecoratedLatticeProofs/SeeSawDoubleStepLinearRelationsPeriods.lean#L94-L125) · [Exact two quotient assertions](https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AbelianVarietyTheory/Definitions/LatticeFrames/IsQuasiFam.lean#L77-L87) · [Composition of the directed one-edge estimates](https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AbelianVarietyTheory/Proofs/DecoratedLatticeProofs/BesselDoubleStepUnfoldingOfUnfoldingsAndLink.lean#L32-L56) · [Detailed mixed-cell integrability argument](../construction/ROW_MIXED_CELL_UNFOLDING.md#absolute-integrability-in-the-prescribed-order)

[rowred]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AbelianVarietyTheory/Proofs/DecoratedLatticeProofs/LastTwoStepsDoubleLiftPeriodEqIntegral.lean#L293-L373
[rowline]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AbelianVarietyTheory/Proofs/DecoratedLatticeProofs/WeilRepSourceLineEqOppositeTargetLine.lean#L16-L40
[rowfu]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AbelianVarietyTheory/Proofs/DecoratedLatticeProofs/DoubleLiftPeriodRankZeroFubiniCompactQuotient.lean#L20-L53
[rowpull]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AbelianVarietyTheory/Proofs/DecoratedLatticeProofs/LastTwoStepsDoubleLiftPeriodEqIntegral.lean#L188-L214
[rowtest]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AbelianVarietyTheory/Definitions/LatticeFrames/CombAtSingleZero.lean#L29-L36
[rowfub]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AbelianVarietyTheory/Proofs/DecoratedLatticeProofs/DoubleLiftPeriodRankZeroFubiniCompactQuotient.lean#L89-L163
[rowmap]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AbelianVarietyTheory/Proofs/DecoratedLatticeProofs/LastTwoStepsDoubleLiftPeriodEqIntegral.lean#L143-L185
[rowseesaw]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AbelianVarietyTheory/Proofs/DecoratedLatticeProofs/LastSeeSawThetaIdentity.lean#L22-L55
[rowmeasure]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AbelianVarietyTheory/Proofs/DecoratedLatticeProofs/ExistsGeometricMeasureVolume.lean#L94-L186
[rowdefs]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AbelianVarietyTheory/Definitions/LatticeFrames/ValLastX.lean#L119-L139
[rowscalar]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AbelianVarietyTheory/Proofs/DecoratedLatticeProofs/TrueGeometryFamilyInvariance.lean#L74-L91
[rowgoal]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AbelianVarietyTheory/Definitions/LatticeFrames/ValLastX.lean#L194-L200
[rowleft]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AbelianVarietyTheory/Proofs/DecoratedLatticeProofs/SeeSawLastTwoStepsDoubleLiftPeriodValue.lean#L204-L249
[rowq]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AbelianVarietyTheory/Proofs/DecoratedLatticeProofs/SeeSawIteratedIntegralLawLastStepsOfLocalFactori.lean#L126-L194
[rowright]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AbelianVarietyTheory/Proofs/DecoratedLatticeProofs/SeeSawLastTwoStepsDoubleLiftPeriodValue.lean#L249-L359
[rowio]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AbelianVarietyTheory/Definitions/LatticeFrames/ValLastX.lean#L140-L153
[rowpins]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AbelianVarietyTheory/Proofs/DecoratedLatticeProofs/SeeSawLatticeFramePinsFiniteIntegralLaws.lean#L109-L128
[rowindices]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AbelianVarietyTheory/Proofs/DecoratedLatticeProofs/SeeSawIteratedIntegralLawLastStepsOfLocalFactori.lean#L66-L128
