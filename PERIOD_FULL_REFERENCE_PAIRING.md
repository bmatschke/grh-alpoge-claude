# The full reference pairing on each word

## The simultaneous dimension premise

For each original good linked member in the eventual size range, let $C_u$ be the full marked complex column, $d_u=\dim C_u$, and use the normalizations $d_u^\star,D^\star,\Gamma$ of B5.11. The initial level satisfies
$$
 (T_u^\star)^{fk}=D^\star/(d_u^\star\Gamma^2),\qquad
 T_u^\star\le T_u\le (1+1/(fk))T_u^\star .
$$
Then, simultaneously for all words,
$$
             \frac12\le\frac{d_u\Gamma^2}{D^\star}\le e<3 .
$$
The comparability hypothesis of the native full-space diagonal spectral assertion holds with $C_0=3$ on these members. Roadmap B8.08j gives this precise estimate. Its use on an abstract approximating family requires the same count and window.

Indeed, the self-dual genus mass $M_k$ and type-level index $I_{01}$ give $M_k I_{01}$ classes before the level $T=T_u$. Stabilizers are trivial there. At the large type prime $g_0>2fk+1$, each stabilizer is a finite subgroup of a conjugate of the inverse image of a unipotent group, hence a $g_0$-group. An element of order $g_0$ in rational dimension $2fk$ requires a cyclotomic polynomial of degree $g_0-1$. Each class therefore contributes a whole copy of its coefficient space. Its dimension times the initial class count gives precisely $d_u^\star$. Each of the $f$ split places over $T$ adds a choice of nonzero vector in $\mathbf F_T^k$, giving $d_u=d_u^\star(T^k-1)^f>0$. The desired ratio equals $(T/T_u^\star)^{fk}(1-T^{-k})^f$. The upper bound uses $(1+1/(fk))^{fk}\le e$. The lower bound uses $T^k\ge 2^k\ge 2f$ for $1\le f\le k$ and Bernoulli's inequality.

[Roadmap B5.11 scales](https://github.com/rh-lean-roadmap/rh-lean-roadmap/blob/02a95b4c62db610642af5f278ee5d0d6df87b348/docs/src/book/main.tex#L9223-L9228) · [B8.08j proof](https://github.com/rh-lean-roadmap/rh-lean-roadmap/blob/02a95b4c62db610642af5f278ee5d0d6df87b348/docs/src/book/main.tex#L43753-L43765) · [B8.54 class count](https://github.com/rh-lean-roadmap/rh-lean-roadmap/blob/02a95b4c62db610642af5f278ee5d0d6df87b348/docs/src/book/main.tex#L58779-L58788) · [Native dimension window](https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AbelianVarietyTheory/Proofs/FlagMeasures/DuWinThreeOfCount.lean#L16-L93) · [Native count-to-window implication](https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AbelianVarietyTheory/Proofs/DecoratedLatticeProofs/ColumnDimensionWindowThreeOfColumnCount.lean#L19-L27)

## Extracting the reference vector

The diamond group $A=(\mathbf F_T^\times)^f$ acts freely on the markings of every initial class. Transporting a basis of the coefficient fibre over each orbit gives copies of the regular representation. If $E_i$ averages over factor $i$, the permitted column projection is $\Pi=\prod_i(I-E_i)$. Counting the characters nontrivial on every factor gives
$$
 h:=\operatorname{rank}\Pi=\rho d_u,\qquad
 \rho=\left(1-\frac1{T-1}\right)^f\ge 1-\frac f{T-1}\ge\frac34
$$
because $T-1\ge(g_0g_1)^2\ge4f$. Let $K=\alpha^{-1}P_u^*P_u$ on $C_u$, where $P_u$ is the unrestricted Bessel period operator and $\alpha>0$ its normalizing scalar. The native diagonal clause gives $\|K-I\|_{\rm HS}^2\le e_0d_u$ with $e_0\to0$ uniformly on its selected family, since the dimension premise holds. Each orthonormal kernel vector contributes one to the squared norm. Therefore
$$
      \operatorname{rank}(P_u|_{\Pi C_u})\ge(\rho-e_0)d_u>0
$$
eventually. Choose $\phi\in\Pi C_u$ with $p=P_u\phi\ne0$. Full translated evaluation $J_z$ maps the bottom reference multiplicity space onto the full $H$ in the conjugation convention of the Bessel pairing. Formal-degree orthogonality and cyclicity construct the intertwiner with any prescribed value in $H$. Cusp vanishing and finite level put it in the required multiplicity space. Central translation has inverse $z^{-1}$. Let $T_0$ evaluate to $p$. Then $\langle J_zT_0,p\rangle=\|p\|^2>0$. The row may have bad finite type. To build a family before the final selector is known, one can use the quantitative single-word estimates B8.08h on the actual point, or prove the criterion below there. Applying the final spectral conclusion conditional on membership of the selector being constructed would be circular.

[Native spectral quantifiers](https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Formalism/SharpRestriction/GlobalTheoremInputs.lean#L142-L157) · [Numerical and rank proofs B8.08h,f](https://github.com/rh-lean-roadmap/rh-lean-roadmap/blob/02a95b4c62db610642af5f278ee5d0d6df87b348/docs/src/book/main.tex#L44312-L44350) · [Full evaluation B8.08d](https://github.com/rh-lean-roadmap/rh-lean-roadmap/blob/02a95b4c62db610642af5f278ee5d0d6df87b348/docs/src/book/main.tex#L43696-L43722)

## A single finite orbit test for an upstream proof

Choose a generator $a_i$ of each cyclic marking factor and put $D=\prod_i(I-R(a_i))$ using the unitary diamond translations. In a simultaneous character basis $D$ is invertible on the characters nontrivial on every factor and zero on all others. Hence $\operatorname{im}D=\operatorname{im}\Pi$. Choose an orthonormal transported basis $\delta$ supported on individual markings with a single coefficient vector. Such choices are available since the action is free and isometric. The desired anchor exists precisely when $P_uD\delta\ne0$ for some such vector. Each test involves at most $2^f$ marked inputs in a single orbit, since
$$
 P_uD\delta=\sum_{S\subseteq\{1,\ldots,f\}}(-1)^{|S|}P_uR(a_S)\delta,\qquad a_S=\prod_{i\in S}a_i .
$$
A sufficient local test is
$$
 \sum_{\varnothing\ne S}\big|\langle P_u\delta,P_uR(a_S)\delta\rangle\big|<\|P_u\delta\|^2
$$
for one transported basis vector. There is also an exact averaged test $\operatorname{tr}(\Pi K)>0$ since this trace equals $\alpha^{-1}\|P_u\Pi\|_{\rm HS}^2$. Computing it uses only matrix coefficients within individual diamond orbits and along the same transported coefficient index. With normalized moments $m_j=d_u^{-1}\operatorname{tr}K^j$ one has
$$
 d_u^{-1}\operatorname{tr}(\Pi K)\ge m_1-\sqrt{(1-\rho)m_2}
$$
by Hilbert–Schmidt Cauchy–Schwarz on $I-\Pi$. Thus $m_1>0$ and $m_2/m_1^2<1/(1-\rho)$ suffice, with $1/(1-\rho)\ge (T-1)/f$. A family-uniform witness for these weaker tests still requires arithmetic estimates.

For the diagonal expansion $K=I+Z+X$ and the project's bound $\|Z\|_{\rm HS}\le\eta_Z\sqrt{d_u}$ on the singular part, a sufficient lower bound on a single real scalar is
$$
 d_u^{-1}\Re\operatorname{tr}(\Pi X)>-\rho+\eta_Z\sqrt\rho.
$$
This follows from the exact trace test and Cauchy–Schwarz on $\operatorname{tr}(\Pi Z)$. It avoids summing absolute values of all nonsingular cells. The scalar inequality is an open alternative unless supplied by an independently established bound.

## Descent, scalars and the two height entries

To compare with the top row, lift the selected full reference row through the actual tower. On each bottom Hecke eigenspace at the reference levels, the adjoint composite lift must have zero kernel, including multiplicities and all finite types. The doubling norm identity with a nonzero factor on that eigenspace gives injectivity if verified for the specified local Schwartz tests. Eigenparameters of distinct systems remain distinct after adjoining the common chain multisets at unramified places, by cancellation. Independence of the Hecke summands gives injectivity on the full bottom space. Finite-dimensional adjunction makes reference descent onto. A general Rallis formula alone does not verify injectivity for this fixed list of tests and levels. [Full reference descent, B8.08](https://github.com/rh-lean-roadmap/rh-lean-roadmap/blob/02a95b4c62db610642af5f278ee5d0d6df87b348/docs/src/book/main.tex#L44412-L44422) · [Gan, Qiu and Takeda, Rallis formula](https://arxiv.org/abs/1207.4709)

Full surjectivity can be weakened on this particular use. Let $W=J_z(\operatorname{im}\mathrm{Desc})\subset H$ for the actual top-to-bottom descent, and $Q_W$ its orthogonal projection. Precisely the necessary reference witness exists if $Q_WP_u\Pi\ne0$. Indeed choose a corner test $\delta$ above with $Q_WP_uD\delta\ne0$, set $\phi=D\delta$, and take a top row whose translated bottom evaluation equals $Q_WP_u\phi$. Its pairing with $P_u\phi$ is $\|Q_WP_u\phi\|^2>0$. Conversely a nonzero pairing on descended rows forces $Q_WP_u\Pi\ne0$ since $\operatorname{im}D=\operatorname{im}\Pi$. In particular,
$$
          \operatorname{codim}_H W<(\rho-e_0)d_u
$$
suffices under the diagonal estimate, because $\operatorname{im}(P_u\Pi)$ would otherwise have to fit in $W^\perp$ if all those pairings vanished. The retained row fraction controls a deficit relative to the ambient dimension, whereas this test compares the missing dimension to a single column of size comparable to $D^\star/\Gamma^2$. It takes an additional quantitative argument to pass between these scales.

The previous [bottom separation theorem](SECOND_PASS_BOTTOM_SEPARATION.md) applies to the core chain of ranks $r+1+i(r+5)$. The descent here uses the row chain of ranks $r+jt$ with $r=k+m-1$ and odd $t$. The bottom ranks and the finite tests differ. The doubling method and the cancellation of common Hecke parameters apply to both, but the nonzero norm on a specified core test does not establish a nonzero norm for the required row test. [Row ranks, B8.08g](https://github.com/rh-lean-roadmap/rh-lean-roadmap/blob/02a95b4c62db610642af5f278ee5d0d6df87b348/docs/src/book/main.tex#L16468-L16478) · [Core chain, B8.15c](https://github.com/rh-lean-roadmap/rh-lean-roadmap/blob/02a95b4c62db610642af5f278ee5d0d6df87b348/docs/src/book/main.tex#L18742-L18767)

Use the actual matched real row tests and finite charts for each double theta step and reference descent on the same realization. A polynomial compact average is a combination of evaluations on invertible frames because these determine each polynomial. Include the common determinant factors, pass to intersections of the actual finite levels, and sum the terms of an upper relation before evaluating the cusp integrals. Cusp decay for the intermediate lift justifies the exchange, and continuity and density extend from polynomial tests to smooth vectors. The terminal interlacing pair has one branching map. The compact evaluation and finite class sum give the prescribed terminal scalar. The initial chart is the single bottom finite translation. With the lift-volume and kernel scalars retained, iteration gives the implication
$$
 \lambda p_{\rm top}+\mu c_t A_t=0
 \quad\Longrightarrow\quad
 \lambda b_0+\mu B_t=0,\qquad b_0=\|p\|^2>0 .
$$
The same full reference row and top preimage are used for each tuple in the word. Here $A_t,B_t$ are the arithmetic and spectral pairing values on the test input. Taking $(\lambda,\mu)=(1,0)$ if $p_{\rm top}=0$ gives a contradiction. Taking $(\lambda,\mu)=(c_tA_t,-p_{\rm top})$ gives $c_t A_t b_0=p_{\rm top}B_t$ for all inputs, including vanishing ones. This derives the multiplicity identity without assuming it to get a nonzero bottom pairing. [B8.08i](https://github.com/rh-lean-roadmap/rh-lean-roadmap/blob/02a95b4c62db610642af5f278ee5d0d6df87b348/docs/src/book/main.tex#L44352-L44409)

The finite central translation is common across words in the joined row model. Each word's column change is rescaled by its positive norm multiplier. At the base tuple $\zeta_{u,t_0}=c_{u,t_0}/c_{u,t_0}=1$. These identifications give height entry 4 using reference good-row surjectivity and spectral admissibility. On the other tuples, B8.08a gives a positive power of $c_{u,t}/c_{u,t_0}$ rational and supported away from the serving residue characteristic. Any field representative then has valuation zero there. Where a rational pairing value is nonzero a representative is obtained as a ratio of the two paired values. If the scalar has no field representative, rationality forces every compared value to vanish, and the field factor $1$ suffices there. The same identity and the independent B4.31 all-place arithmetic bound give entry 1 with the actual integral column and row identifications. The R89C1–C2 spectral/arithmetic coordinates and the second-pass theta comparison must hold on the same member. The shared nonvanishing follows from the diagonal clause on its proper domain. The spectral theorem, full reference descent and tied arithmetic inputs are separate outstanding suppliers wherever the project has yet to establish them.

[Scalar normalization B8.08a](https://github.com/rh-lean-roadmap/rh-lean-roadmap/blob/02a95b4c62db610642af5f278ee5d0d6df87b348/docs/src/book/main.tex#L43624-L43694) · [Word identity and field representatives](https://github.com/rh-lean-roadmap/rh-lean-roadmap/blob/02a95b4c62db610642af5f278ee5d0d6df87b348/docs/src/book/main.tex#L44422-L44448) · [Native word anchor](https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AutomorphicArithmetic/ThetaCorrespondence/ThetaPairLifts/ThirdPlaceSeries/MiStar2AtRealisation.lean#L48-L113) · [Project height consequences](PERIOD_REFERENCE_INTEGRAL.md)
