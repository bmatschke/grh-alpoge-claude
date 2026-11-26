# A single terminal test for homogeneous seesaw relations

Fix one word $u$ of the marked column construction. Use its common terminal archimedean frame and its prescribed lowering map. For tuple $t$, let $U_t=b_T K_t b_T^{-1}$ be the moved finite level and $\epsilon_t[b_T]$ its single top translate. Write $P_t=\epsilon_t\operatorname{vol}(U_t)$ in the given quotient measure with probability Haar measure at infinity. Write $D_{t,m}(\psi,F)$ for the arithmetic terminal period on the permitted column and read top row, and $\mathcal P_{t,m}(\psi,F;y,v)$ for the analytic terminal period with column frame $y$ and smooth top vector $v$. On the terminal class and frame data of the geometric construction there exists **one** pair $y_u,v_u$ such that
$$
 \mathcal P_{t,m}(\psi,F;y_u,v_u)=P_t D_{t,m}(\psi,F)
 \qquad\text{for every }t,\psi,F. \tag{1}
$$
The choice precedes the tuples, class representatives, sections and coefficients of a relation. The common complex frame coordinates of $y_u$ can be taken integral. The smooth vector $v_u$ is complex. [Native top level][pin] · [Common lowering on the true columns][low] · [Terminal step in B8.08i][road]

## The compact average

Let $V_\lambda$ and $V_\sigma$ be the terminal frame-function representations and $B:V_\lambda\to V_\sigma$ the marked lowering. The group $H=\prod_\tau U(n)$ acts on rank $n+1$ frames by $\operatorname{diag}(k_\tau,1)$ and on rank $n$ frames by $k_\tau$. On functions it acts by inverse translation. The compact real terminal group maps onto $H$, so its probability Haar measure pushes forward to Haar probability on $H$. The interlacing branching rule from $U(n+1)$ to $U(n)$ at each embedding gives $\operatorname{Hom}_H(V_\lambda,V_\sigma)=\mathbf C B$. The true column formula identifies $B$ with the standard nonzero interlacing map in the polynomial model times specified powers of the nonzero marked frame coordinate. That formula gives the same $B$ for the reference and twisted tuples. The smooth-vector map $j$ is onto $V_\sigma$. [True column formula][low] · [Range of the original smooth-vector map][j] · [Compact average and branching convention][avg]

Choose invariant Hermitian metrics, linear in their first arguments. Define $e_y$ by $\Phi(y)=\langle\Phi,e_y\rangle$ and the rank-one map $T_{y,v}$ by $T_{y,v}\Phi=\Phi(y)j(v)$. Averaging by
$$
 T\longmapsto\int_H \rho_\sigma(k)T\rho_\lambda(k)^{-1}\,dk
$$
gives the Hilbert–Schmidt orthogonal projection onto $\mathbf C B$. Haar invariance makes the average equivariant. Pairing its integrand with $B$ removes $k$ by unitarity. The numerator of the projection coefficient is $\operatorname{tr}(B^*T_{y,v})=\langle j(v),B e_y\rangle$. Thus for every linear functional $\ell$ on the lower space,
$$
 \int_H \ell(\rho_\sigma(k)j(v))\,
          \Phi(\operatorname{diag}(k,1)y)\,dk
    = a(y,v)\ell(B\Phi),\qquad
 a(y,v)=\frac{\langle j(v),B e_y\rangle}{\operatorname{tr}(B^*B)}. \tag{2}
$$
The native translated row reading is $J(v,k)(z)=j(v)(k^{-1}z)$, which gives precisely the two actions in (2). [Translated frame comparison][avg] · [Original frame realization][j]

The evaluations span the dual of $V_\lambda$, since a frame function zero at every frame is zero and the space is finite dimensional. Even the frames with integer entries and nonzero determinant at each embedding suffice. These are Zariski dense in the product of general linear groups. Indeed, multiplying a polynomial zero on these frames by the product of the determinants produces a polynomial zero on every integer matrix tuple. Restricting successively in each coordinate makes this polynomial identically zero. In the frame-function model multiplication by sufficiently large powers of the determinants clears all negative determinant twists. Thus the evaluations at the integer frames still separate the upper space. Since $B\ne0$, some such $y_u$ has $B e_{y_u}\ne0$. Choose $v_u$ using the range of $j$ so that
$$
 j(v_u)=
 \frac{\operatorname{tr}(B^*B)}{\|B e_{y_u}\|^2}\,B e_{y_u}.
$$
This gives $a(y_u,v_u)=1$ before any automorphic sections are evaluated. [Frame-function polynomial model][pol] · [Range and equivariance][j]

## Reading the marked finite classes

Lift each marked definite class $c$ to $h_c$ with its finite matrix and with identity archimedean component. Conjugation by $b_T$ identifies the moved level with the marked finite level. The resulting double cosets are the original marked classes, and the rational stabilizer at $h_c$ identifies with its group $\Gamma_c$ of marked lattice isometries. Indeed, preservation of the finite lattice and its markings is the finite matrix criterion for membership in the stabilizer. Recovering the rational isometry is unique by injectivity at the finite adeles. The quotient integral on the cell has measure $\operatorname{vol}(U_t)/|\Gamma_c|$ times Haar probability integration at infinity. The row and column level characters cancel in the product after the finite move. [Representatives and stabilizers][reps] · [Moved-level invariance][lev] · [Integral with these measures][per]

For a given smooth top row $F$, the rule $j(v)\mapsto F(v)(h_cb_T)$ gives a linear functional on $V_\sigma$ because $j$ is bijective onto this space. The nondegenerate coefficient pairing identifies the functional with a coefficient vector. Rational left invariance and the conjugated right level character give that vector its required class-stabilizer character. Extending the vectors by the marked transformation rule therefore gives a class reading $G_F$. With the translate coefficient included the functional at $c$ becomes
$$
 \ell_{c,F}(w)=\epsilon_t|\Gamma_c|\,
       \operatorname{period}_t(\operatorname{single}_c w,G_F).
$$
The arithmetic period of a section supported at $c$ includes $1/|\Gamma_c|$, so multiplication by the order recovers the unweighted evaluation, and the translate supplies $\epsilon_t$. The expression on lowered vectors is independent of any extension choices since each lowered vector is in the range of $j$. [Construction from the smooth row][read] · [One-class formula][j]

The marked terminal embedding identifies the column at $h_c$ with $\Phi_c=\operatorname{ev}_{z}\psi(c)$. Its lowering is $B\Phi_c=(\operatorname{lowerMap}\operatorname{ev}_z\psi)(c)$. Substituting (2), the stabilizer factor in $\ell_{c,F}$ cancels the Haar denominator separately at each class. The sum of the single-class sections is the lowered section. There is at most one top chart, and the live-chart law covers every source class. If the chart set is empty, the permitted column is zero and both periods vanish. Thus for every $y,v$ the answer is $a(y,v)P_tD_{t,m}(\psi,F)$, with the different moved-level volumes retained. Equation (1) follows. [Marked evaluation and empty-chart case][tail] · [Class-factorization proof][per]

For any finite coefficients $\beta_i$, the equation $\sum_i\beta_i P_{t_i}D_{t_i,m}=0$ is equivalent to the analytic terminal relation for all $y,v$, and also to the relation tested at the single pair in (1). The coefficients may absorb all preceding chain weights. Zero periods are included.

Application to a linked member uses its actual marked class matrices, moved-level equality, top chart and smooth representation with the displayed range. The native assembly obtains these terminal data from the identified row and column records, with distinct constructions for untwisted and twisted representatives. To pass from this terminal equivalence to the requested spectral pairing, the two-step recursion must still transfer homogeneous relations on the original coupled column and row kernels, including at $m-2,m-1$, and the descended top row must agree with the specified bottom row. Row-lift surjectivity and the shifted all-place dual assertion require their separate inputs. [Instantiation on the original family][fam] · [Inputs for the last pair][last] · [Inputs for the interior pairs][step]

[pin]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AbelianVarietyTheory/Definitions/LatticeFrames/PinColL.lean
[low]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AbelianVarietyTheory/Proofs/DecoratedLatticeProofs/TrueColumnsBranchingMapEquivariantNonzeroCommon.lean#L145-L181
[j]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AbelianVarietyTheory/Definitions/LatticeFrames/TopFormula.lean#L26-L40
[avg]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AbelianVarietyTheory/Proofs/DecoratedLatticeProofs/UnitaryAverageTranslateEqSmulBranchingMap.lean#L111-L230
[pol]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AbelianVarietyTheory/Proofs/DecoratedLatticeProofs/UnitaryAverageTranslateEqSmulBranchingMap.lean#L74-L84
[reps]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AbelianVarietyTheory/Proofs/DecoratedLatticeProofs/LastSpaceMovedLevelClassPointsRepresentatives.lean#L89-L191
[lev]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AbelianVarietyTheory/Proofs/DecoratedLatticeProofs/LastPeriodLawMovedLevel.lean
[per]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AbelianVarietyTheory/Proofs/DecoratedLatticeProofs/SeeSawLastPeriodFactorizationOfClassData.lean#L72-L144
[read]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AbelianVarietyTheory/Proofs/DecoratedLatticeProofs/ExistsRowFormReadingLevelFormLastSpace.lean#L12-L53
[tail]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AbelianVarietyTheory/Proofs/DecoratedLatticeProofs/LastPeriodTailEqLoweredEvaluationPeriod.lean#L17-L90
[fam]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AutomorphicArithmetic/ThetaCorrespondence/ThetaPairLifts/ThirdPlaceSeries/ClsPinDOfFamCol.lean#L12-L78
[last]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AbelianVarietyTheory/Proofs/DecoratedLatticeProofs/SeeSawLastTwoStepsTransportLinearRelations.lean#L92-L137
[step]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AbelianVarietyTheory/Proofs/DecoratedLatticeProofs/SeeSawDoubleStepLinearRelationsPeriods.lean#L82-L149
[road]: https://github.com/rh-lean-roadmap/rh-lean-roadmap/blob/02a95b4c62db610642af5f278ee5d0d6df87b348/docs/src/book/main.tex#L44358-L44410
