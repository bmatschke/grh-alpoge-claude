# Lowest-type coefficients on the moderate region

Consider any of the three original finite projectors on a framed arithmetic row satisfying ARO24–27. Write $n=p+q$, $1\le q\le p$, $f=[F:\mathbb Q]$, $N=n^2 f$, and let $V$ be the quotient volume with the Haar measures of that row. Its main term is $D^\star=d_\infty V\operatorname{Re} e(1)$. On the counting range with $q^2\le n$ and the gap in ARO27, the integral on the moderate region of the absolute sum of the far terms is at most $e^{-N}D^\star$. The result also holds if the bad-label projector is zero. The following argument supplies the pointwise premise of C83N4. It uses the lowest compact type of the actual discrete series, with its original unit vector. [Previous ball count and shell summation](continuation_v83/cylinder.tex#L99-L226) · [Original weight and level tests](arithmetic_rows_v46/main.tex#L1069-L1153)

## The compression at one real place

Let $S$ be the lowest $K=U(p)\times U(q)$ type, with decreasing Harish–Chandra parameter $\lambda$. For $X$ Hermitian in the noncompact tangent space, write $d=\|X\|_{\rm HS}$. We use the compact integral for the compression of $\sigma(\exp X)$ to $S$, proved in B8.53a. With probability Haar measure and a unit highest-weight vector $u\in S$, it is the integral of
$$
 (\dim S)\,P_{\sigma(k)u}
       \prod_{i=1}^{n-1}\Delta_i(\exp(k^{-1}Xk))^{-s_i},
 \qquad s_i=\lambda_i-\lambda_{i+1}+1,\qquad k\in K .
$$
Here $P_v$ denotes orthogonal projection on the unit vector $v$, and $\Delta_i$ is the leading principal minor of size $i$ in the parameter order. In the project's conjugate model the corresponding compact matrix entries are conjugated. This preserves the positive projection integral and its norm. The unweighted integral is the identity by compact Schur orthogonality. The formula applies at gap $h\ge120nq^{3/2}$, which follows from the ARO27 gap after one increase of the counting cutoff. [Exact compression and hypotheses][formula] · [Proof in the human reconstruction][road] · [Adriazola’s coefficient calculation][jim]

The representation-theoretic identification of this integral matters because the real type need not be scalar. In the cited proof, compact covariance and the common value at the identity fix the order-zero term. Both the actual coefficient and the analytic minor integral satisfy the first-order Schmid equations on the lowering components. For the integral this follows by differentiating leading minors in an upper triangular direction that adds an earlier column to a later column. The resulting derivatives vanish, and highest-weight orthogonality removes the other contracted terms. For uniqueness, commute noncompact derivatives past one another. A commutator is compact and acts on a lower-order jet by compact covariance. The first possibly nonzero jet of order $j>0$ is therefore symmetric and $K$-equivariant and kills every slice in a lowering component. On the orthogonal complement of its kernel, the mixed Casimir on each remaining one-slot component is bounded below by $g-2n$, for the opposite-sign gap $g>2n$. The tensor Casimir thus exceeds the target Casimir there by at least $2j(g-2n)$. Equivariance places this excess in the kernel, so the jet vanishes. Analyticity along each $\exp(tX)$ identifies the two coefficients. This argument explains the role of the gap in using the cited formula for an arbitrary unit vector in $S$. [Uniqueness and Casimir bound][jet] · [Identification of the actual coefficient][formula]

## A dimension-uniform estimate

Put $Y=k^{-1}Xk$. If $Y=U\operatorname{diag}(\omega_a)U^*$, Cauchy–Binet writes $\Delta_i(e^{tY})$ as the moment generating function of a real random variable $Z_i$. Its value at a subset $I$ of size $i$ is $\sum_{a\in I}\omega_a$, and its probability is the squared absolute minor of the first $i$ rows of $U$ in columns $I$. The probabilities sum to one by orthonormality. Differentiating the compressed determinant at zero gives
$$
 \mathbb E Z_i=\operatorname{tr}Y_{[i],[i]}=0,\qquad
 B_i=\mathbb E Z_i^2=\sum_{b\le i<a}|Y_{ab}|^2 .
$$
Indeed $Y$ has zero diagonal, and the second derivative of the log determinant subtracts the squared internal block from the trace of the first block of $Y^2$. The off-diagonal signature blocks give $\operatorname{rank}Y\le2q$. Cauchy–Schwarz gives $|Z_i|\le\sqrt{2q}\,d$.

For $d>0$ put $s=\min(1,1/(\sqrt{2q}\,d))$. Since $|sZ_i|\le1$, the inequality $e^y\ge1+y+y^2/3$ on $[-1,1]$ and $\log(1+a/3)\ge a/4$ for $0\le a\le1$ give $\log\mathbb E e^{sZ_i}\ge s^2B_i/4$. Convexity of the log moment generating function gives $\log\Delta_i(e^Y)\ge sB_i/4$. In $\sum_i s_i B_i$ the coefficient of $|Y_{ab}|^2$ with $b<a$ is $\lambda_b-\lambda_a+a-b$. Nonzero entries join opposite signs, so this coefficient is at least $h$. Their squared moduli sum to $d^2/2$ on this half of the matrix. Thus each integrand weight is at most
$$
 \exp\!\left[-\frac h8\min\!\left(d^2,\frac{d}{\sqrt{2q}}\right)\right].
$$
The same inequality for the norm of the compression follows by integrating positive rank-one projections with their normalization above. At $d=0$ use unitarity. The compact factors of a Cartan decomposition act isometrically on $S$, so the bound holds for all $y$ with $d=d_v(y)$ and for the prescribed lowest-type vector. [Minor estimate and product][minor]

At the finite places $e=e^*=e*e$, so evaluation is an inner product of translates and $|e(y_f)|\le e(1)$. Multiply the real and finite bounds by the formal degrees. This gives exactly the kernel bound of C83N4 with prefactor $D^\star/V$. Its shell estimate sums over all supported rational elements, with the same finite projector. On the moderate region $\operatorname{least}(\Lambda_x)\ge X_0^{-11q}$, $X_0=nf\,\mathrm{rd}_E\,g_{\rm lev}b$, it absorbs the lattice packing factor into the gap. Integration yields the stated $e^{-N}D^\star$ for each of the three projectors with one cutoff. The definite case already has the exact identity contribution. [Summation and uniform threshold](continuation_v83/cylinder.tex#L164-L226) · [External proof on these parameters][far]

[formula]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AbelianVarietyTheory/Proofs/FlagMeasures/LowestKTypeCompressionFormulaOfStrictLowestKType.lean#L22-L81
[road]: https://github.com/rh-lean-roadmap/rh-lean-roadmap/blob/94e6a98b4e74932a0298d6bd22d44cf60c62764b/docs/src/book/main.tex#L58485-L58505
[jim]: https://github.com/jimjamzola/RH-Alpoge-Reconstruction/blob/aa9c86bf2a7d29b08575641fecea19a2a603e87c/manuscript/sec14_bessel.tex#L1819-L1833
[jet]: https://github.com/rh-lean-roadmap/rh-lean-roadmap/blob/94e6a98b4e74932a0298d6bd22d44cf60c62764b/docs/src/book/main.tex#L58466-L58482
[minor]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AbelianVarietyTheory/Proofs/FlagMeasures/ProdLeadMinorDecay.lean#L94-L169
[far]: https://github.com/rh-lean-roadmap/rh-lean-roadmap/blob/94e6a98b4e74932a0298d6bd22d44cf60c62764b/docs/src/book/main.tex#L58437-L58451
