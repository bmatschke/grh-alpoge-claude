# Rationality of the composite theta images in the common bottom target

The [lower-row laws](LOWER_ROW_ASSEMBLY.md) include separating arithmetic evaluations for the individual lift targets. The weight-specific construction asks for common evaluations of the composite maps into a single bottom space.

## Rational tests on the actual weight-supported column

Let $z'$ be the prescribed restriction of the saturated first-pass datum to $W=z.W_1(F_0)$, and write $E$ for its common bottom Hilbert space. In the eventual range and under the analytic, Hida-level and advance-field inputs of the row construction, the composite maps on $z'$ admit one separating family of complex-linear tests reading every rational source image in the specified coefficient embedding. This includes the reference tuple and each of the frame-character tuples present on this restriction. For each fixed choice the tests use one common archimedean pair. The conclusion also applies to any admissible choice satisfying these inputs. The arithmetic assumptions for making the advance field choice include the period-normalized CM jet values and critical-value comparisons described in the [field construction](ROW_COEFFICIENT_FIELD.md). The upstream sufficient package also specifies the toric and zeta denominator, lattice and twist transport, and Hecke reflection conditions. [Upstream arithmetic package](https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AbelianVarietyTheory/Definitions/Divisors/HypothesisBundleConversions.lean#L7-L19) [Original row and its separate lift-test definitions][cr-test] · [Untwisted restriction](UNTWISTED_BOTTOM_ROW.md) · [Pinned assembly and its outside inputs][cr-all]

Write $\iota:K\hookrightarrow\mathbb C$ for the Hilbert-model coefficient embedding, $t_0$ for the prescribed reference tuple, and $C_t=\prod_{i,j}c_{ij,t}$. Every factor is nonzero by the [square comparisons](ROW_TOWER_INDUCTION.md). The [normalized square calculation](ROW_MIXED_GRID_RATIOS.md) gives $r_t\in K^\times$ with $\iota(r_t)=C_t/C_{t_0}$. The [finite tests](ROW_TEST_CONVERGENCE.md) define linear functionals $p_a:E\to\mathbb C$, and [period detection](ROW_PERIOD_ASCENT.md) on the [common real choice](ROW_COMMON_REAL_TEST.md) gives $\bigcap_a\ker p_a=0$. On the good rational source block, the opposite-path calculation, the [mixed-cell unfolding](ROW_MIXED_CELL_UNFOLDING.md) and the definite jet evaluations give
$$
 \iota(e_t) C_t\,p_a(\Theta_t j_t x')=\kappa\,v_{t,a}(x'),
 \qquad e_t\in\mu(K).
$$
Here $\kappa$ is the evaluation of the *same* real polynomial combination for every $t,a,x'$. To see that $v_{t,a}(x')\in\iota(K)$, choose at every contributing cell the coset expansion at its specified depth. Its coefficients are products of the actual unfolded local test values in the requested field. The two normalized definite kernel chains carry the rational input coefficients into that field, and so does the final compact branching pairing. The class weights are products of reciprocals of finite stabilizer orders, the local cell coefficients are rational, and $s_{AA}$ belongs to the same field by the auxiliary conductor and square-root clauses. Finite summation proves the assertion. On the first pass the [staircase volume and its auxiliary factor](ROW_MIXED_CELL_SUPPORT.md#the-common-staircase-volume-and-the-finite-arithmetic-class-sum) are common to all $(t,a)$. The class sum is independent of the admissible expansion. [Period and normalization](ROW_PERIOD_JET_FORMULA.md) · [Coefficient calculation for the actual finite sum][cr-v]

For an arbitrary $x\in F_{R,t}$ take $x'=\sum_g a_g\rho_t(g)x$, where $\sum_g a_g g$ is the good central idempotent in the rational group algebra and $\rho_t(g)$ denotes the **source group action**. At the bottom, the trivial level gives precisely this idempotent. The stored action satisfies $\Theta_t j_t(\rho_t(g)x)=g_E\Theta_t j_tx$. Since the good projector acts as the identity on the Hilbert target, semilinearity gives
$$
 \Theta_t j_t x' = \sum_g\iota(a_g)g_E\Theta_t j_tx=\Theta_t j_tx .
$$
Use the finite sum evaluated at $x'$. [Source projection and identity on the target][cr-proj]

If $\kappa\ne0$, set $\lambda=C_{t_0}/\kappa$. Writing $v_{t,a}(x')=\iota(b)$ yields
$$
  (\lambda p_a)(\Theta_t j_tx)=\iota\!\left(\frac{b}{e_t r_t}\right).
$$
Thus a single nonzero scale works for the whole target and preserves separation. If $\kappa=0$, including when the real polynomial combination itself is zero, all the periods on all these images vanish because $\iota(e_t)C_t\ne0$. Separation makes each image zero. Take $\lambda=1$ and retain all tests on $E$. This branch permits a nonzero target. [The two cases on the specified choice][cr-cases]

To pass to $z'.R.\mathrm{toCx3}(z'.F)$, let $c$ be the prescribed identity or complex conjugation and $o$ the underlying identification of the twisted space with the Hilbert model. It satisfies $o(au)=c(a)o(u)$. Then $u\mapsto c((\lambda p_a)(o(u)))$ is complex-linear, the family still separates, and its values lie in $(c\circ\iota)(K)$, the original datum's coefficient embedding. At the eventual stage the field and size requests precede the eligible data. If the Hida estimates are applied on the auxiliary stage with the same group, copy the specified datum there and pull the tests back. Copying twice recovers the original record and its complex theta maps. This gives the claimed test on $z'$. [Conjugation and the specified embedding][cr-twist] · [Size and field choices on the stage][cr-at] · [Return to the prescribed record][cr-copy]

There is an immediate consequence for the actual images. In rational source bases, concatenate the columns $((\lambda p_a)(\Theta_t j_tb))_a$ over all allowed tuples. Its entries lie in the embedded coefficient field, and its complex kernel is exactly the space of relations among the original images by separation. Row reduction in that field therefore gives generators for *all* joint relations, including relations between distinct tuples. On this pinned restriction the lower-row multiplicity equality and the row test now provide the two inputs to the source's weight assertion, with its regularized Siegel–Weil and Hecke continuation hypotheses. The third-stage starting-choice constructor then takes the row-lift family on this same restriction. Its application retains the pinned core, geometric, group, support and standard-reading hypotheses. Using this family, the [first-pass starting state](FIRST_PASS_STARTING_STATE.md) retains the set of exceptional coefficient places. Subsequent exports and retwisting concern additional data. [Weight assertion on the pinned record][cr-holds] · [Use on the exact restriction][cr-next]

[cr-test]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Formalism/LocalToGlobal/IndefiniteReal/RationalAdjoints/RatZOfTests.lean#L18-L29
[cr-all]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AbelianVarietyTheory/Proofs/DivisorProofs/RationalityOfThetaHypotheses.lean#L65-L76
[cr-v]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AbelianVarietyTheory/Proofs/TwistedOperators/RowTestRationalSumsOfFiniteSumsMeaningful.lean#L34-L92
[cr-proj]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AbelianVarietyTheory/Proofs/TwistedOperators/RowTestHilbertModelsOfChoiceClaims.lean#L20-L62
[cr-cases]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AbelianVarietyTheory/Proofs/TwistedOperators/RowTestHilbertModelsOfChoiceClaims.lean#L96-L147
[cr-twist]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AbelianVarietyTheory/Proofs/TwistedOperators/RowTestComplexSideOfHilbertModels.lean#L13-L20
[cr-at]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AbelianVarietyTheory/Proofs/IwasawaDecomposition/AtDatRowTest.lean#L44-L65
[cr-copy]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AbelianVarietyTheory/Proofs/TwistedOperators/EqualMultiplicitiesRowTestOfSameGroupTransfer.lean#L16-L27
[cr-holds]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AbelianVarietyTheory/Proofs/IwasawaDecomposition/HoldsFromPrintedInputs.lean#L58-L95
[cr-next]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AbelianVarietyTheory/Proofs/IwasawaDecomposition/ConstructionStartingChoicesOfFineAdelicData.lean#L195-L240

## Descent of the joint image

Let $E$ be the finite-dimensional bottom target of the very datum under consideration, let $k$ be the image of its specified coefficient embedding, and put
$$
\mathcal V=\{\Theta_t(j_t x):t\text{ an allowed tuple},\ x\text{ a rational source vector for }t\},\qquad
V_k=\operatorname{span}_k(\mathcal V),\quad V_{\mathbf C}=\operatorname{span}_{\mathbf C}(\mathcal V).
$$
The required bottom row test holds **if and only if** some complex basis of $V_{\mathbf C}$ drawn from $\mathcal V$ already spans $V_k$ over $k$. Equivalently, $V_k$ has finite dimension over $k$ equal to $\dim_{\mathbf C}V_{\mathbf C}$. These statements include a zero row. [Bottom target, rational embeddings and theta maps](https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Formalism/LocalToGlobal/IndefiniteReal/PartsOrth.lean#L61-L70) · [Original test](https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Formalism/LocalToGlobal/IndefiniteReal/RationalAdjoints/RatZOfTests.lean#L18-L20)

Indeed a separating family gives a complex-linear injection $J:E\to\mathbf C^N$ sending $\mathcal V$ into $k^N$. Pick a basis $v_1,\ldots,v_d$ of $V_{\mathbf C}$ from $\mathcal V$. The matrix with columns $Jv_i$ has a nonzero $d$-row minor over $k$. Solving that minor for the coefficients of $Jv$, for each $v\in\mathcal V$, gives coefficients in $k$. Injectivity gives the same expansion of $v$. Conversely, extend such a basis to a complex basis of $E$. Its dual coordinate forms separate $E$ and take values in $k$ on every original $\Theta_t(j_t x)$, including tuples beyond those used to choose the basis. The dimension version follows because a complex basis drawn from $\mathcal V$ is $k$-linearly independent. Thus one can close this weight-specific step by proving rationality of transition coordinates across *all* tuples in the same target on the requested column.

## Computing the coefficients with the given Hermitian form

For a positive-dimensional image, choose $y_1,\ldots,y_d$ from the actual image vectors as a complex basis of $V_{\mathbf C}$. Use the Hermitian form on the bottom target, with the convention that it is linear in the second variable. Form the nonsingular Gram matrix $G=(\langle y_a,y_b\rangle)_{a,b}$ and the column $g(y)=(\langle y_a,y\rangle)_a$. If $G_i(y)$ replaces column $i$ of $G$ with $g(y)$, the exact condition on the original data is
$$
   \frac{\det G_i(y)}{\det G}\in k
   \qquad (y\in\mathcal V,\ 1\le i\le d).
$$
Indeed for $y=\sum_b c_b y_b$ the equation is $Gc=g(y)$. Cramer's rule identifies the ratios with the unique coordinates already proved to characterize the row test. A common rescaling of the Hermitian form cancels. For a zero-dimensional image any dual basis of $E$ gives the tests. Since each $j_t$ is semilinear for the specified embedding, it suffices to check the images of a rational basis at each allowed $t$. On the restricted untwisted datum the reference tuple and at most two others occur. This gives a finite matrix of actual image columns from bases of the corresponding rational source spaces. [Exact first-pass tuple set](UNTWISTED_BOTTOM_ROW.md)

Equivalently, concatenate those basis images as the columns of a single complex linear map from the direct sum of the source coordinate spaces. Its complex kernel must be the scalar extension of its relations over $k$. To see this, use the independent columns $y_i$ as pivots. The expressions of all other columns in these pivots give a basis of relations with one distinct nonpivot coefficient equal to one. These relations descend exactly when their pivot coefficients lie in $k$, by uniqueness of this normalized basis of relations (or by row reduction over $k$). The condition therefore includes relations between different tuples, even when each tuple separately has a rational basis for its image.

## Descent from a separating period identity

The reconstruction already gives a second way to produce the common evaluations. Suppose the same separating complex-linear periods $p_a$ on $E$ satisfy, on the actual data,
$$
  \iota(z_t)c_t\,p_a(\Theta_t j_t x)=\kappa w_{t,x,a},
  \qquad w_{t,x,a}\in k,\quad c_t/c_{t_0}\in k^\times,
$$
where $\iota$ is the distinguished embedding, $z_t$ a root of unity in its domain, $c_t\ne0$ and $\kappa$ is independent of $t,x,a$. It suffices to have the formula after the rational central projection that fixes the composite image. If $\kappa\ne0$, the rescaled tests $(c_{t_0}/\kappa)p_a$ separate $E$ and take values in $k$ on all these images. If $\kappa=0$, all the images are zero by separation. The earlier descent proof transports these tests through the possible complex conjugation of the real model. The opening proof verifies separation, the normalized unfolded identity and membership in the coefficient field on the specified weight-supported datum. [Normalization and conjugation, TD15–16](theta_descent/main.tex#L463-L543) · [Finite sums and the analytic inputs to the identity](theta_test_inputs/main.tex#L1019-L1035)

## Which comparisons between tuples are necessary?

Suppose the period identity is established and the resulting linear map $\Psi$ given by the periods is injective on $V_{\mathbf C}$. Injection on the joint image suffices for the following argument, since at the end one can extend its basis to all of $E$. Suppose that for the finite list of rational source basis images $y_j$ one has
$$
 \Psi(y_j)=\alpha_{t(j)}a_j,\qquad a_j\in k^N,\quad \alpha_{t(j)}\in\mathbf C^\times .
$$
Here $\alpha_t$ can include the unknown tuple period and any common nonzero scalar. The case of zero common scalar in the period identity was handled above. Delete zero columns. Choose a maximal linearly independent subset of the $a_j$, with indices $B$. The same indices give a basis of the original $V_{\mathbf C}$. For $j\notin B$ write $a_j=\sum_{b\in B}d_{bj}a_b$. A nonzero minor over $k$ puts every $d_{bj}$ in $k$. Injectivity gives the unique expansion
$$
 y_j=\sum_{b\in B}d_{bj}\frac{\alpha_{t(j)}}{\alpha_{t(b)}}\,y_b .
$$
Consequently the row test holds **if and only if** $\alpha_{t(j)}/\alpha_{t(b)}\in k^\times$ for every $d_{bj}\ne0$. Necessity follows even when the rational tests eventually used on $E$ differ from $\Psi$, by the basis criterion at the start of this note. Sufficiency follows by taking coordinates in the $y_b$ and extending them across a complement. The result concerns the true scalar multiples of the columns, so changing their individual $k$-basis conventions does not affect descent.

Join two distinct tuple labels by an edge when they occur together as $t(j),t(b)$ in the preceding test. It suffices to compare the scalars on a spanning tree of each connected component. Products and inverses inside $k^\times$ give every other required edge ratio. A single active tuple needs no scalar comparison. If the nonzero tuple images form a direct sum across tuples, choose the column basis in each summand and no comparison occurs. Three active tuples joined in one component require at most two comparisons. Pairwise intersections alone do not justify omitting an edge. For example, in dimension two the rational columns $(1,0),(0,1),(1,1)$ have pairwise distinct lines with zero intersection, but the third column has nonzero coefficients along both pivots. This calculation is available when normalized finite evaluations and injectivity on the joint image have been proved. It does not assume that the actual tuple images are independent. [Actual untwisted index set](UNTWISTED_BOTTOM_ROW.md) · [Square and bottom constants](ROW_SQUARE_RATIOS.md) · [Period-to-jet identity](ROW_PERIOD_JET_FORMULA.md)

## What remains if a period misses part of the image?

Let $P:E\to\mathbf C^N$ be a common complex-linear period map on the actual bottom target. Let $y_1,\ldots,y_s$ be the images of rational bases for all the allowed tuples. Suppose the formula and the required tuple comparisons give $P(y_j)\in k^N$, after a single nonzero rescaling of $P$. More generally it suffices that these columns have coordinates over $k$ in some complex basis of their image chosen from the columns. The preceding ratio calculation decides this latter condition using only the normalized finite columns, without assuming $P$ is injective. We can then isolate the exact additional descent question even when $P$ has a kernel.

Choose pivot indices $B$ for the observed columns $P(y_b)$ and solve a nonzero minor to write $P(y_j)=\sum_{b\in B}a_{bj}P(y_b)$ with $a_{bj}\in k$. For each nonpivot define the actual vector
$$
 z_j=y_j-\sum_{b\in B}a_{bj}y_b\quad\in\ker P .
$$
The spans of the original images decompose over both fields:
$$
 V_k=\bigoplus_{b\in B}k y_b\ \oplus\ \operatorname{span}_k\{z_j:j\notin B\},
 \qquad
 V_{\mathbf C}=\bigoplus_{b\in B}\mathbf C y_b\ \oplus\ \operatorname{span}_{\mathbf C}\{z_j:j\notin B\}.
$$
Indeed the change of generators subtracts only $k$-multiples of pivots. Applying $P$ to a relation forces every pivot coefficient to be zero by independence of the observed pivots. In particular the second summand on the right is exactly $V_{\mathbf C}\cap\ker P$. Thus the original row test is equivalent to equality of the dimensions of the two residual spans over their respective fields. A residual basis made of actual $z_j$ gives, together with the $y_b$, coordinates taking values in $k$ on the original images. Extend that basis to the entire bottom target to obtain separating tests there.

This gives a concrete sufficient check on any individual realization. If an independent upper bound on the dimension of the joint image equals the rank of a minor of the observed columns, every residual is zero and the joint image descends. A nonzero residual need only satisfy the same basis criterion within the smaller space $V_{\mathbf C}\cap\ker P$. When all observed columns vanish, the list of residuals is the original list. The computation claims no rank equality for a particular Hida datum. The [common real test](ROW_COMMON_REAL_TEST.md) ensures that changing the real test alone cannot detect a residual missed by the whole finite catalogue at the selected pair. [Normalization required of the actual periods](ROW_PERIOD_JET_FORMULA.md)
