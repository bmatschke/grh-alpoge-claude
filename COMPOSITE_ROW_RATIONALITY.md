# Rationality of the composite theta images in the common bottom target

The [lower-row laws](LOWER_ROW_ASSEMBLY.md) include separating arithmetic evaluations for the individual lift targets. The weight-specific construction asks for common evaluations of the composite maps into a single bottom space.

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

## The period identity that would establish descent

The reconstruction already gives a second way to produce the common evaluations. Suppose the same separating complex-linear periods $p_a$ on $E$ satisfy, on the actual data,
$$
  \iota(z_t)c_t\,p_a(\Theta_t j_t x)=\kappa w_{t,x,a},
  \qquad w_{t,x,a}\in k,\quad c_t/c_{t_0}\in k^\times,
$$
where $\iota$ is the distinguished embedding, $z_t$ a root of unity in its domain, $c_t\ne0$ and $\kappa$ is independent of $t,x,a$. It suffices to have the formula after the rational central projection that fixes the composite image. If $\kappa\ne0$, the rescaled tests $(c_{t_0}/\kappa)p_a$ separate $E$ and take values in $k$ on all these images. If $\kappa=0$, all the images are zero by separation. The earlier descent proof transports these tests through the possible complex conjugation of the real model. Its arithmetic application requires separation and the normalized unfolded identity with the indicated coefficient-field membership on the same datum. These give concrete entries of the common-target calculation still to establish. [Normalization and conjugation, TD15–16](theta_descent/main.tex#L463-L543) · [Finite sums and the analytic inputs to the identity](theta_test_inputs/main.tex#L1012-L1027)
