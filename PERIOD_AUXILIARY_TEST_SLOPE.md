# The maximal slope of the auxiliary test lattice

At a fitted member of the original size family, the positive part of the maximal slope of its auxiliary test lattice is bounded by
$$
 \mu_{\max}^{+}(M)\ll_{\varepsilon,\mathcal F} x^A\exp\!\left(\tfrac12 x^{\varepsilon/4}\right).
 \tag{1}
$$
Here $\mu_{\max}^{+}=\max(0,\mu_{\max})$, $b=\exp(x^\varepsilon)$, and $\mathcal F$ specifies common constants for the polynomial size bounds below. In particular the test-lattice slope is $o(b^\eta)$ for every fixed $\eta>0$. This recovers the square-root bound stated in the comparison manuscript on the original fitted family. The missing input in that manuscript's displayed inference is the bound on the logarithm of the node spacing. There is also a weaker estimate requiring only the window width. [Comparison calculation][sidler] · [Pointwise size hypotheses][size] · [Original parameter record][param]

## The lattice and its slope

Fix a fitted record and a complete compatible choice with the original test-lattice identification. The initial positive definite top space $X_0$ has rank
$$
 n_p=k+m+m(k+m+4).
$$
The top-node class lattices are self-dual. The form lattice is the direct sum of their integral coefficient lattices over the finite test/class indices, with the original coordinate identification and Gram matrix $G_{\mathrm{form}}$. The test lattice $M$ is the coordinate dual under the standard bilinear pairing. Its frames $X'_v$ are those for $(G_{\mathrm{form}}^{-1})^{\mathsf T}$ in the original metric convention. The nonempty index set, a conjugation place and the star-compatible embeddings into the coefficient field are part of the original construction. Write $f$ for the number of host embedding labels. In these conventions the fitted-lattice theorem gives, for every real $C\ge1$,
$$
 \mu_{\max}(M)\le 4f n_p R_p(C)\log\bigl(n_pR_p(C)\bigr),\qquad
 R_p(C)=(m+1)(g_a(C)+1)+L_c+n_p.
 \tag{2}
$$
It also gives finite generation and nonvanishing of $M$ and invertibility of the frames. The coefficient $n_p$ in (2) is the rank of $X_0$. The direct sum can have many more coordinates. No extra count of tests, classes, or coefficient-field places multiplies (2). [Metric and dual][metric] · [Native slope statement][slope] · [Application at the fitted record][fitted]

Indeed the spread is the largest difference of entries of the dominant weight at one embedding, maximized over embeddings. At gap parameter one each such difference is at most $L_c+1+(m+1)g_a(1)+n_p\le R_p(1)$. Applying the original maximal-slope theorem for the dual direct sum with that spread proves (2) at $C=1$. The fitted lattice and frames are fixed before $C$ is quantified in the source, so this choice also bounds their slope if a later height estimate uses a larger control constant. In particular $n_pR_p(1)\ge1$, so the right side of (2) bounds $\mu_{\max}^{+}$. [Spread and quantifiers][fitted] · [Roadmap B8.21i][road-slope]

## Two bounds for the cloud width

Fix $0<\varepsilon<1/52$ in the original size family. Let $x\to\infty$, $X'=\exp(x^{\varepsilon/3})$, and use common polynomial upper bounds for $k,m,t,f$ in $x$. For instance the original pointwise hypotheses bound $k,m,n=f/2$ in explicit power windows and $t\le x^{C_t+\varepsilon/100}$. Thus $f,n_p,m+1$ are polynomially bounded. The integer $L_c$ is the maximum over embeddings of the positive part of the difference of the two endpoint cloud coordinates after flooring. All cloud coordinates come from real input entries in $[0,S_c]$ (or zero), so $L_c\le S_c$, with no rounding loss. The original row setting includes $m\ge44$. For $B=\max(1,\sqrt{L_c})$ its gap bound is $g_a(1)\le4t^7B$. Equivalently the explicit maximum defining $g_a(1)$ is $O(x^{A_0}(1+\sqrt{L_c}))$ whenever its ranks have polynomial bounds. Hence, enlarging $A_0$ if necessary,
$$
 R_p(1)\ll_{\mathcal F}x^{A_0}(1+\sqrt{L_c})+L_c .
 \tag{3}
$$
[Cloud and gap inequalities][gap] · [Exact gap and rank definitions][spread] · [Family rank bounds][size] · [Row hypotheses][rows]

**Using the window.** The scale definitions and the parameter record give
$$
 kS_c\le w''=\frac{b'}{xn}=\frac{b}{nX'},\qquad b'=\frac{xb}{X'}.
$$
Set $U=b/(knX')$. Then $0\le L_c\le U\le b/X'$, since $k,n\ge1$. In particular $\log(n_pR_p(1))=O_{\varepsilon,\mathcal F}(\log x+x^\varepsilon)$ by (3). Combining with (2) and absorbing polynomial factors gives some $A$ with
$$
 \mu_{\max}^{+}(M)\ll_{\varepsilon,\mathcal F}x^A(1+\sqrt U+U)
 \ll_{\varepsilon,\mathcal F}x^A(\sqrt b+b/X').
 \tag{4}
$$
For every fixed real $D$, the last bound divided by $b/x^D$ tends to zero, since $x^{A+D}/\sqrt b\to0$ and $x^{A+D}/X'\to0$. This argument uses only the width inequality and the stated polynomial rank and gap controls. The coarser comparison $5S_c\le xb$ used in the comparison manuscript does not by itself control the summand $+L_c$ in (3) by $O(x^A\sqrt b)$. [Scale definitions][scale] · [Width hypothesis][param] · [Coarse inequality][coarse]

**Using the spacing.** The original data also identify the width as $S_c=4k\Delta$ for the *same* positive node-spacing parameter $\Delta$ which satisfies $\log\Delta\le x^{\varepsilon/4}/2$. This is an explicit field of the parameter record immediately before the window inequality. Consequently
$$
 0\le L_c\le 4k\exp\!\left(\tfrac12 x^{\varepsilon/4}\right).
$$
Substitute this in (3), absorbing $4k$ and $\sqrt{4k}$ into a fixed power of $x$. If $Y=\exp(x^{\varepsilon/4}/2)$, then $Y\ge1$, $R_p(1)\ll_{\mathcal F} x^{A_1}Y$, and $\log(n_pR_p(1))=O_{\varepsilon,\mathcal F}(\log x+x^{\varepsilon/4})$. One more application of (2) proves (1). For any fixed $\eta>0$, the logarithm of the ratio of its upper bound to $b^\eta$ is at most $O(1)+A\log x+x^{\varepsilon/4}/2-\eta x^\varepsilon\to-\infty$. [Width identity][width] · [Logarithmic spacing bound][param] · [Human-readable size definition][size]

The constants and cutoffs are common to all fitted points and compatible test identifications under the specified common rank-growth bounds. An independent host can use the estimate once it supplies the same size hypotheses and the identification of the integral test lattice and its metric. The result bounds the positive auxiliary slope in the period-height inequality. Constructing the fitted evaluation on the selected quotient, bounding its map height and transporting the estimate to the sharp lattice require their own inputs.

[sidler]: https://github.com/Sidler4Hare/alpoge-claude-rh-reconstruction/blob/7d17bb991581172cebd554c33a205b1b0f3a2fb3/sections/actual-target-floor.tex#L290-L316
[param]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Formalism/LocalRingCardinality/DataParams.lean#L195-L204
[width]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Formalism/LocalRingCardinality/DataParams%E2%82%82.lean#L145-L160
[scale]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Formalism/LocalRingCardinality/DataParams%E2%82%82.lean#L21-L39
[gap]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AbelianVarietyTheory/Statements/PlaceShiftStatements/SetAtOfSizeAt.lean#L60-L119
[coarse]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Formalism/LocalRingCardinality/ColumnWeightSpreadOffTop.lean#L70-L75
[fitted]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AbelianVarietyTheory/Proofs/DivisorProofs/MultiplicityAtFittedPoints.lean#L82-L138
[metric]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AbelianVarietyTheory/Definitions/Divisors/GridTestLatticeLargestSlopeBound.lean#L107-L119
[slope]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AbelianVarietyTheory/Definitions/Divisors/GridTestLatticeLargestSlopeBound.lean#L196-L225
[size]: https://github.com/rh-lean-roadmap/rh-lean-roadmap/blob/94e6a98b4e74932a0298d6bd22d44cf60c62764b/docs/src/book/main.tex#L18465-L18524
[rows]: https://github.com/rh-lean-roadmap/rh-lean-roadmap/blob/94e6a98b4e74932a0298d6bd22d44cf60c62764b/docs/src/book/main.tex#L18540-L18548
[spread]: https://github.com/rh-lean-roadmap/rh-lean-roadmap/blob/94e6a98b4e74932a0298d6bd22d44cf60c62764b/docs/src/book/main.tex#L19129-L19146
[road-slope]: https://github.com/rh-lean-roadmap/rh-lean-roadmap/blob/94e6a98b4e74932a0298d6bd22d44cf60c62764b/docs/src/book/main.tex#L48126-L48159
