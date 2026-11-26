# The full Gram bounds on the original selected families

Under the standing automorphic and arithmetic inputs of the reconstruction, the selected family satisfies the spectral endpoint with its original constant 3. The two operators act on the full word columns. The same diagonal estimate gives a strictly positive first moment on the ramified part of **each** word. The theorem is conditional on membership in the original selected class, as in the definition of the endpoint. [Original endpoint][end] · [Selected family and class](LOCAL_SELECTED_FAMILY.md) · [Class in the Roadmap][class]

## The normalized operators

Write $n=k+m-1$, $r=m/2-1$, $L=\log b=x^\varepsilon$, $t=m^5fL$, $z=kf\log k$, and $\Gamma=e^{C_\Gamma t}$. Fix a selected member and impose the endpoint's window $1/3\le d_u\Gamma^2/D^\star\le3$ for every word. The one selected bundle gives its Hida system $X$, full automorphic realization $Y$, the common character, compatible quotient measures and the isometric identification of its full word spaces and target. In finite dimension this identifies $\dim C_u=d_u^S$ and $D_X^\star=D^\star$. In what follows $d_u=d_u^S$. A common target unitary disappears in $K_{uv}=A_u^*A_v$, and source unitaries preserve both Hilbert–Schmidt norm and the diagonal identity. The scale of each period remains in $A_u$. [Selection and both ties][sel] · [Character, measures and dimensions][ties] · [Measured comparison of the full columns][column]

Let $H_{uv}$ denote the nonidentity zero-Gram part and put $R_{uv}=K_{uv}-H_{uv}-\mathbf1_{u=v} I$, interpreting the last term as zero between distinct columns. Set $M=d_ud_v/D^\star$. On these data the arithmetic row estimates give

| Words | Nonidentity zero Gram | Positive-Gram remainder |
|---|---|---|
| $u\ne v$ | $H_{uv}=0$ | $\|R_{uv}\|_{\rm HS}^2\le(1+b^{-6})M$ |
| $u=v$ | $\|H_{uu}\|_{\rm HS}^2\le d_u e^{-z}$ | $\|R_{uu}\|_{\rm HS}^2\le\Gamma M$ |

Here is how the strata give the two coefficients. The two type primes cost $P_g=\prod_{i=0}^1(1+3/g_i)^f$ on the squared norm, from finite Schur orthogonality. Write $A$ for the normalized generic scalar bound, $N'=2^{-(k-2r-5)}e^{C_4t}$ for the signed nongeneric bound, and $E=e^{-z/3}$. The two absolutely counted contributions, from generic nonscalar pairs and pairs of larger corank, are each at most $EM$. For the latter the nondegenerate and degenerate estimates are summed from corank 2 through $k$, including $k-1,k$ with their endpoint mass estimate. The nonscalar determinant estimate includes the case of a vanishing penultimate minor on one side. The common term weights come from the flag-stabilizer disintegration on one rational pair. Absolute convergence follows by unfolding against the two absolute Poincaré sums and Cauchy–Schwarz. Thus the finite-level inequality and the triangle inequality bound $\|R_{uv}\|_{\rm HS}^2/M$ by
$$
 P_g\bigl(\sqrt{A+2E}+\sqrt{N'+E}\bigr)^2 .
 \tag{1}
$$
[Unfolding and rotated measure][unfold] · [Zero-Gram classification][zero] · [Physical orbital measures][orb] · [Nonscalar bound and complete corank sum][corank] · [Finite contraction and (1)][contraction]

For distinct words the [three-letter estimate and the mass comparison](SPECTRAL_THREE_LETTER_SCALAR_SAMPLING.md) give $A\le(1+b^{-7})\exp(b^{-14})$. The sizes give $E,N'\le b^{-14}$ and $P_g\le\exp(6b^{-7})$. Writing $v=b^{-7}$, (1) is at most $(1+7v)(1+v+\sqrt2 v)^2\le1+16v\le1+b^{-6}$ at $b\ge16$. For an equal word $A\le e^{C_{\rm eq}t}$. This estimate sums the generic class squares in the same frame measure as the rotated point sum. For a defective place of order $q^i$ the two possibilities are a proper image, which saves $q^{-(k-1)}$, and a full image, where the signed character bound saves at least $q^{-(k-2r-5)}$ after Cauchy–Schwarz. The nonempty defect support supplies the factor in $N'$. With $M_0=\max(C_{\rm eq},C_4)$, (1) is at most $10\,4^f e^{M_0t}\le\Gamma$ when $C_\Gamma\ge M_0+1$ and $t\ge32f$. [Defective supports and their weights][ng] · [Equal-word frame and point sum][eq] · [Final scalar bounds][finish]

## The order of the constants

Jin's simultaneous selection constructs particular families on arbitrarily late windows. The universal family step uses the parameter version of the row estimates. On the original class $W_3=\mathcal D_3$, the six standing constants are
$$
 (C_g,c_b,C_w,c_T,C_T,C_0)=(C_{YL}+1,1/4,3,1/2,C_{Tu},3).
$$
The additional counting parameter for an equal pair can be fixed at $1$ because the two word levels and Vandermondes coincide. In B8.10d the six constants determine $C_4$, and together with that counting parameter they determine $C_{\rm eq}$, **before** the thresholds for $C',C_\ell$. Consequently $M_0+1$ is a function of the outer list alone. Require this lower bound when choosing the middle threshold. The family's own $C_\Gamma$ then satisfies the inequality used in (1), with the very same $\Gamma$ used in the window. [Counting hypotheses for equal pairs][pair] · [Quantified estimates for both signed sums][signed] · [Family threshold lists][lists] · [Quantifier in Jin's family construction][jinchoice]

For distinct words the level ratio is bounded in both directions by $a_*=3e^{7/4}$ and the Vandermonde ratios by $a_*^k$. For the loop estimates choose the fixed function with value $a_*$ where this comparison is needed. The outer and middle lists together determine the last thresholds for the loop estimates and for the finite-type bound. The entry with zero-based index 17 in their concatenation is the family's $C_\Gamma$. Thus $C_k$ and all six entries of the minimum defining $C_\ell$ may be required to dominate the necessary constants, including $8C_\Gamma$ in the rank bound. In particular the chosen rank satisfies $k\ge16C^{32}m^5fL$ once the corresponding threshold has been imposed. The rank, gap and level inequalities then hold on every admitted index. The critical product forces $T_u(\pi/(v_Eg_0g_1))^{2r}\ge1$ on the same window. [Full quantifier of the loop and mixed-row theorem][loop] · [Construction of its last threshold and critical-level test][last] · [Native standing hypotheses][size]

The geometric inputs to this application are also pointwise on this selected bundle. Selection gives the full row and finite-level dictionaries and the local arithmetic tie. The normalized neat levels, integrable coefficient projector and decay give its absolutely summable orbital expansion. The regular Gram formula uses the self-dual tuple and Hermitian-matrix measures for the same standard additive character. The quotient disintegration uses their ratio. Its hypothesis is $2a<M$ for a nonsingular $a$-frame in ambient rank $M$. For the joint frame here $a=m$ and $M=k+m-1$, so $k>m+1$ suffices. A single augmented flag uses fewer vectors, and the successive unit-hyperplane mass comparison uses $a=1$, $M\ge3$. At the two extreme coranks the residual mass uses the separate low-rank bound above. Radial cutoffs in the orbital amplitude are removed in the [selected section comparison](SPECTRAL_LEVEL_ZERO_AND_CUTOFFS.md). These identifications, the one selection cutoff and the original sizes are the premises used by the universal row transport. [Selected arithmetic dictionaries][dict] · [Integrability][integr] · [Neatness and finiteness on the native bundle][anc] · [Finite volume and nonsingular density][density] · [Application on the selected class][last]

## Original errors and ramified positivity

By the upper window and the triangle inequality, the diagonal entry in the table gives
$$
 \frac{\|K_{uu}-I\|_{\rm HS}^2}{d_u}
 \le \left(e^{-z/2}+\sqrt{3/\Gamma}\right)^2
 \le 2e^{-z}+6/\Gamma=:e_0 .
 \tag{2}
$$
Take $\eta_0=b^{-6}$ and the [already established dimension error](SPECTRAL_GRAM_CELLS.md) $\eta_1=e^{-nf\log n/16}$. With $y=x^{\varepsilon/8}$ we have $L=y^8$. Eventually $C_\Gamma t\ge2y+\log12$, $z\ge2y+\log4$ and $nf\log n/16\ge y$, uniformly in the index, since $f\ge x^2$, $k\ge100$ and $C_\Gamma>0$ is fixed in the family. Thus $\eta_0,\eta_1,\sqrt{e_0}\le e^{-y}$. Take the maximum of the selection, counting, size and numerical cutoffs before the point index. If the simultaneous window fails, the native assertion at this member is an implication with false premise, so all three errors may be zero. This proves the three clauses of $\operatorname{LinkS}(F_m,3)$ in the prescribed order. [Exact endpoint][end] · [Uniform passage and window implication][ev] · [Arithmetic class transport][transport]

On the window $d_u>0$. If its normalizing mass $c_u$ vanished, the native convention would give $K_{uu}=0$, contradicting (2) for $e_0<1$. Thus $c_u>0$. Now let $P$ be its unnormalized period, so $K_{uu}=c_u^{-1}P^*P$, with $\Pi$ the orthogonal projection to the word-prime ramified source. The free diamond action gives $r_u=\operatorname{tr}\Pi=d_u(1-1/(T_u-1))^f$. Since $T_u\ge b^{m/2}$, $f\le k$, $(kb)^8\le g_i\le b^{C_g}$ and $m\to\infty$ uniformly, Bernoulli's inequality gives $r_u\ge d_u/2$ beyond another common cutoff. Hilbert–Schmidt duality gives
$$
 c_u^{-1}\|P\Pi\|_{\rm HS}^2
 =\operatorname{tr}(\Pi K_{uu})
 \ge r_u-\sqrt{r_u d_u e_0}>0
 \qquad(e_0<1/2).
 \tag{3}
$$
This supplies the nonzero period on the source used in the [ramified first-moment calculation](SPECTRAL_PROJECTED_FIRST_MOMENT.md). A comparison with a prescribed arithmetic period, when needed, uses its separate normalized descent or seesaw identity. [Free source rank and period comparison][column] · [Growth of the selected rank][mgrowth]

[end]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Formalism/SharpRestriction/GlobalTheoremInputs.lean#L142-L157
[sel]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AbelianVarietyTheory/Proofs/GlobalInterpolation/LinkAlt.lean#L21-L48
[ties]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Formalism/LocalToGlobal/SiegelLatticeTheory/FlagStabilizerTensors/SpectralTiesReal.lean#L245-L279
[dict]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AutomorphicArithmetic/ThetaCorrespondence/ThetaPairLifts/ThirdPlaceSeries/STiesR.lean#L19-L29
[lists]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Formalism/SharpRestriction/ParamsHeightRankConstant.lean#L106-L162
[size]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Formalism/SharpRestriction/CuspSpanNormBounds/StandingNumericalData.lean#L106-L135
[mgrowth]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Formalism/SharpRestriction/CuspSpanNormBounds/StandingHypothesesHoldFamily.lean#L1186-L1193
[ev]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Formalism/SharpRestriction/CuspSpanNormBounds/StandingHypothesesHoldFamily.lean#L628-L652
[class]: https://github.com/rh-lean-roadmap/rh-lean-roadmap/blob/c535d69c2d028dd05547e05c4b0efde1225ce454/docs/src/book/main.tex#L15250-L15265
[loop]: https://github.com/rh-lean-roadmap/rh-lean-roadmap/blob/c535d69c2d028dd05547e05c4b0efde1225ce454/docs/src/book/main.tex#L17033-L17057
[last]: https://github.com/rh-lean-roadmap/rh-lean-roadmap/blob/c535d69c2d028dd05547e05c4b0efde1225ce454/docs/src/book/main.tex#L44526-L44550
[pair]: https://github.com/rh-lean-roadmap/rh-lean-roadmap/blob/c535d69c2d028dd05547e05c4b0efde1225ce454/docs/src/book/main.tex#L15566-L15572
[signed]: https://github.com/rh-lean-roadmap/rh-lean-roadmap/blob/c535d69c2d028dd05547e05c4b0efde1225ce454/docs/src/book/main.tex#L17839-L17854
[integr]: https://github.com/rh-lean-roadmap/rh-lean-roadmap/blob/c535d69c2d028dd05547e05c4b0efde1225ce454/docs/src/book/main.tex#L15972-L15988
[density]: https://github.com/yuiyuiui/Natural-Language-Proof-Generalized-Riemann-Hypothesis/blob/405237610e58ab9d4a9d5d54d9a0548a0c44227c/sections/integral-division.tex#L189-L195
[jinchoice]: https://github.com/yuiyuiui/Natural-Language-Proof-Generalized-Riemann-Hypothesis/blob/405237610e58ab9d4a9d5d54d9a0548a0c44227c/sections/simultaneous-comparisons.tex#L55-L77
[unfold]: https://github.com/yuiyuiui/Natural-Language-Proof-Generalized-Riemann-Hypothesis/blob/405237610e58ab9d4a9d5d54d9a0548a0c44227c/sections/integral-division.tex#L3424-L3491
[zero]: https://github.com/yuiyuiui/Natural-Language-Proof-Generalized-Riemann-Hypothesis/blob/405237610e58ab9d4a9d5d54d9a0548a0c44227c/sections/integral-division.tex#L3493-L3529
[ng]: https://github.com/yuiyuiui/Natural-Language-Proof-Generalized-Riemann-Hypothesis/blob/405237610e58ab9d4a9d5d54d9a0548a0c44227c/sections/integral-division.tex#L3622-L3641
[eq]: https://github.com/yuiyuiui/Natural-Language-Proof-Generalized-Riemann-Hypothesis/blob/405237610e58ab9d4a9d5d54d9a0548a0c44227c/sections/integral-division.tex#L3817-L3872
[orb]: https://github.com/yuiyuiui/Natural-Language-Proof-Generalized-Riemann-Hypothesis/blob/405237610e58ab9d4a9d5d54d9a0548a0c44227c/sections/integral-division.tex#L3998-L4026
[corank]: https://github.com/yuiyuiui/Natural-Language-Proof-Generalized-Riemann-Hypothesis/blob/405237610e58ab9d4a9d5d54d9a0548a0c44227c/sections/integral-division.tex#L4123-L4197
[contraction]: https://github.com/yuiyuiui/Natural-Language-Proof-Generalized-Riemann-Hypothesis/blob/405237610e58ab9d4a9d5d54d9a0548a0c44227c/sections/integral-division.tex#L4199-L4210
[finish]: https://github.com/yuiyuiui/Natural-Language-Proof-Generalized-Riemann-Hypothesis/blob/405237610e58ab9d4a9d5d54d9a0548a0c44227c/sections/integral-division.tex#L4211-L4224
[column]: https://github.com/yuiyuiui/Natural-Language-Proof-Generalized-Riemann-Hypothesis/blob/405237610e58ab9d4a9d5d54d9a0548a0c44227c/sections/integral-division.tex#L4226-L4235
[transport]: https://github.com/rh-lean-roadmap/rh-lean-roadmap/blob/c535d69c2d028dd05547e05c4b0efde1225ce454/docs/src/book/main.tex#L41215-L41220
[anc]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Formalism/LocalToGlobal/SiegelLatticeTheory/FlagStabilizerTensors/ThmSOwn.lean#L942-L960
