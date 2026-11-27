# The lower arithmetic volume before a family is chosen

For each nonterminal admissible point the relevant lower bound counts mixed-integral cusp sections of the fitted weight on the point's own flag component. It holds for every such point under the geometric inputs of Roadmap B8.25a. In particular it may be used inside the construction of the member and bundle conditions in B8.34. This note derives the lower bound on precisely the degree progression used by the carrying section. It uses B8.26u for the existence and properties of the marked root tower and Kaiwen Jin's Appendix J for the boundary and trace calculations. [Universal tower and cover statements][universal] · [Identification with the original component and generic flags](PERIOD_SELECTED_MARKED_ORIGIN.md) · [Geometric and arithmetic premises][premises]

The component comparison identifies each normalized volume with the total divided by the number of components on this deep cover. The same chapter constructs the unlabelled depth-four lattice and states which ramified labelled transitions and height bounds the volume argument still uses. [Root tower comparison](GOOD_ROOT_TOWER_COMPARISONS.md)

## The volume on one component

Fix the point, a good cover at the prescribed level, a component $Z$, and its fitted strictly decreasing weight $v=u'$. Put $d=\dim Z_{\rm fl}$ and $F$ equal to the coefficient field of this cover. Let $K=F(Z_{\rm fl})$ and let $K'/K$ be the finite extension on its root model at cutoff $N=\lfloor B(v,g)\rfloor$. Write $h=[K':K]$, $\delta=h[F:\mathbb Q]$, $\Delta=\deg_Z(v)>0$, and $a_Z$ for the model slope, the limiting self-intersection divided by $(d+1)$ times the limiting generic degree in the same normalization. Let $S_j(t)$ be the model cusp sections of weight $jv$ of supremum at most $e^{jt}$ in the model frame. Write $n_j(t)$ for the number of cusp sections on $Z$ at the same threshold in the mixed lattice. The mixed lattice reads Hodge–Tate frames at primes in $S_B$ and ordinary record frames elsewhere. Our volume convention is
$$
 V_Z(t)=\limsup_{8\mid j,\ j\to\infty}
   \frac{d!\log n_j(t)}{[F:\mathbb Q]j^{d+1}}.
$$
The analogous model count uses $\delta$ in the denominator. The zero section belongs to each count. [Jin's normalizations and metrics][jin-vol] · [Tower degree and finite-place sets in the native proof][native-count]

Let $\varepsilon$ be the tower's effective section vanishing along the boundary. On the smooth approximation with $s_i\downarrow0$, choose positive integers $q_i$ divisible by eight such that $q_is_i=8q_0$ for the fixed boundary parameter $q_0$. On the $i$th model let $M_i$ denote the cleared line of weight $q_i v$ with the auxiliary boundary term removed. Write $I_i$ for its arithmetic self-intersection and $G_i$ for its absolute generic degree over $\mathbb Q$. The marked tower gives
$$
 \frac{G_i}{\delta q_i^d}\longrightarrow\Delta,\qquad
 \frac{I_i}{(d+1)\delta q_i^{d+1}}\longrightarrow\Delta a_Z .
$$
For large $i$ the model has fibre-nef $M_i$ and a smooth semipositive metric. These are the hypotheses of Moriwaki's Corollary 6.4, which bounds the arithmetic self-intersection above by the arithmetic volume for every constant shift. Positive horizontal degree on every point is unnecessary for this lower bound. The fibre comparison in v40 constructs complementary adapted columns modulo $\ell^{R-2}$ with $R=4$ from the two Hodge–Tate maps and level coordinates. Their transition is upper triangular modulo the uniformizer and the ambient bundle has trivial scaling. This supplies the trivial-ambient-flag input on the marked finite fibres. [Moriwaki, Corollary 6.4][moriwaki] · [v40 Hodge–Tate frame comparison][ht] · [Approximation and convergence][approx]

Fix $t'\in\mathbb R$. Multiplication by $\varepsilon^{8j}$ takes a section of $jM_i$ of log supremum at most $jq_i(t'-Cs_i)$ into $S_{jq_i}(t')$. It is injective on this integral component and makes the section cuspidal. For the boundary estimate, the smoothing error on a chart with exhaustion $R$ is bounded per unit weight by
$$
 C(t_s^{1/3}+\epsilon(t_s)R)+Cs(1+\log R)-csR,\qquad
 t_s=e^{-1/s^2},\quad \epsilon(t_s)=o(s).
$$
For small $s$ the coefficient of $R$ is at most $-cs/2$, and $C\log R-cR/2$ is bounded above. Hence the total error is $O(s)$ up to the boundary. Fixed model comparisons at the finite places contribute only $O(s)$ per unit weight from the auxiliary line. One may equivalently use the tower's integral multiplication and smoothing bound directly. [Jin's boundary estimate and fixed vertical discrepancy][boundary] · [Roadmap's integral multipliers on the tower][trace-proof]

Apply Corollary 6.4 to $M_i$ shifted by $q_i(t'-Cs_i)$. Its self-intersection is $I_i+(d+1)q_i(t'-Cs_i)G_i$. The denominator converting arithmetic volume to our count is $(d+1)\delta q_i^{d+1}$. For each fixed $i$, the indices $jq_i$ form a subsequence of the multiples of eight, so the limsup of the model count over multiples of eight dominates
$$
 \frac{I_i+(d+1)q_i(t'-Cs_i)G_i}{(d+1)\delta q_i^{d+1}}.
$$
Pass to the limit in $i$ and use nonnegativity of the count to get $V^{\rm mod}_{8,Z}(t')\ge\Delta(a_Z+t')_+$. This use of Corollary 6.4 takes all powers of the *fixed* integral approximation $M_i$. No inference from a full-degree limsup to an arbitrary subsequence is required. [Native injection and normalization for these powers][native-powers]

## Two lattice changes and one field trace

Fix a homogeneous trace basis on the cover. One construction starts with rational basis elements $\eta_1,\ldots,\eta_h$ for $K'/K$. A single section $b$ of a fixed multiple $k_0 v$ can clear their horizontal poles and vanish along the boundary. Indeed the generic reference line is big, so for a fixed divisor containing these poles and the boundary, a sufficiently large multiple of the line minus that divisor has a nonzero section. Taking an eighth tensor power, if needed, preserves all vanishings and makes $8\mid k_0$. Fixed vertical denominators are cleared once, and the boundary vanishing bounds $b\eta_i$ in the logarithmic metric. In a generic frame the $b\eta_i$ still form a basis after dividing by a common nonzero frame factor. The homogeneous model construction gives the same type of basis by multiplying $h$ independent coordinate monomials by one fixed section. [Jin's basis and boundary argument][jin-trace] · [Roadmap's homogeneous construction][trace-proof]

For $s\in S_j(t')$ multiply by each $b\eta_i$, divide by the common gauge for weight $(j+k_0)v$, and take the field trace. The resulting tuple determines $s$ by separability in characteristic zero. To check regularity on a generic flag chart with normal domain $R$, take every valuation ring of $K'$ above $R$, meaning every valuation ring containing its image. The proper root model gives a centre and the matched root frames give a unit change there. In the chart frame the product lies in each such valuation ring, hence is integral over $R$. Its trace is integral and belongs to $K$, so normality puts it in $R$. The chart readings glue. The generic boundary valuations are positive on the product along all branches, so their traces vanish there as well. Alternatively the source's positive-gap cusp criterion applies after the norm bound. At each good embedding one bounds the trace on the dense set where it is a sum of $h$ branch readings, then extends by continuity to every frame. This costs $h$ times the largest fixed multiplier norm, independently of $j$. This argument for horizontal regularity concerns the characteristic-zero flag chart. [v40 valuation-ring argument and extension by continuity][trace-proof] · [Jin's boundary and trace norm][jin-trace]

Put
$$
 e_p=\frac1{p-1}+40\frac{v_p(|\operatorname{disc}E|)}{[E:\mathbb Q]}
       +\mathbf1_{p=2},\qquad c_2=\sum_{p\in S_B}e_p\log p .
$$
For a flag the lattice inclusions persist under intersection with any step and passage to the line quotient by the preceding step. Tensoring these lines with signed exponents therefore costs at most $e_p\|(j+k_0)v\|_1$ in units of the order of $p$. Apply this comparison first to pass from the model to the ordinary frame, then to pass from the ordinary frame to the mixed lattice at the target. Field trace preserves the ordinary bound by the ultrametric inequality on all branches, with valuations divided by ramification. The remaining primes only see a fixed denominator. Thus one integer works simultaneously for all $h$ traces,
$$
 M_j=M_{\rm fix}\prod_{p\in S_B}p^{\lceil 2(j+k_0)e_p\|v\|_1\rceil},
 \qquad \log M_j\le 2(j+k_0)c_2\|v\|_1+O_Z(1).
$$
All fixed data, including $B$ and $v$, are held fixed in this degree limit. [Jin's two comparisons and finite prime sum][finite] · [Native rounding and the final norm bound][native-slack]

For arbitrary $t$ and $\eta>0$ take $t'=t-2c_2\|v\|_1-\eta$. After the clearing and the fixed archimedean cost, the log norm is at most $(j+k_0)t-j\eta+O_Z(1)$, also when $t<0$. Thus for sufficiently large $8\mid j$,
$$
 \#S_j(t')\le n_{j+k_0}(t)^h.
$$
On dividing logarithms by $\delta j^{d+1}/d!$, the exponent $h$ exactly cancels the covering degree in $\delta$. Also $8\mid j+k_0$ and $(j+k_0)/j\to1$. The mixed volume dominates the model bound. Letting $\eta\downarrow0$ proves
$$
 \boxed{\quad V_Z(t)\ \ge\ \Delta\bigl(a_Z-2c_2\|v\|_1+t\bigr)_+\qquad(t\in\mathbb R).\quad} \tag{1}
$$
The basis, smoothing parameters, and the degree threshold absorbing the fixed constants can all depend on the component. None contributes a constant to (1). [Native shifted count][native-end] · [Jin's mixed-volume lower bound][jin-lower]

## The uniform estimate at the fitted weight

Use $s_Z=a_Z-2c_2\|v\|_1$. The actual cutoffs give a slightly sharper finite cost than the factor $60$ used in the two reconstructions. Indeed $N=\lfloor B\rfloor\ge128$ and $\#\{p\in S_B:p>N\}\le N$ on this tower. Since $\log x/(x-1)$ is decreasing on $x>1$, the tail of the first term in $c_2$ is at most $\log(N+1)$. The primes at most $N$ contribute at most $\log N+2.2$ by the factorial estimate of B8.26. The different term contributes at most $40\log\operatorname{rd}(E)$, and the extra dyadic term is $\log2$. As $2.2+\log2+\log(1+1/N)\le\log N$, this gives
$$
 c_2\le3\log B+40\log\operatorname{rd}(E)\le40\log(B\operatorname{rd}(E)).
$$
This bound uses the original tower's count of bad primes and works even if they cluster immediately above $N$. [Cutoff on this tower][n-cut] · [Factorial estimate and tail cardinality][prime-sum]

In Jin's convention $\mathrm{err}$ is the bracket in (J.3) with $B$ replacing $N$. It dominates $\|v\|_1\log(B\operatorname{rd}(E))$. B8.26c and (J.3) therefore give $\operatorname{mean}_Zs_Z\ge-(2C_*+97)\mathrm{err}$, and in particular the published bound with $2C_*+137$. At the original fitted quotient $T\|v\|_1\le834fmb$, $T\|v\|_\infty\le8b$, $4\le B\le132b$, and the tail spread contributes at most $6\|v\|_1$. Consequently the term $T X_b$ for this lower bound lies in $C_{\rm row}E_P$ uniformly on the eligible tail. The third, single finite lattice change made later by the theta multiplier contributes to the **upper** image comparison. [Mean of the tower slopes][mean] · [Jin's coefficient, fitted weight and budget][jin-slope] · [Normalized-image comparison](PERIOD_JIN_FULL_THETA_TRANSFER.md)

Roadmap B8.25a's premises are quantified before family and level. B8.26 and B8.26u apply on every supplied good cover at a nonterminal admissible point. That point, its chain and its flag model provide the input to (1). This proves the lower-volume step wherever B8.34 invokes B8.24, including for a prospective compatible selection. On those same hypotheses the other, logically distinct, ingredients include the normalized-image comparison on the target, conversion of the resulting Chow bound to the lattice estimate, and the signed finite index estimates. The v40 changes to the integral spanning generators and descent of the Hodge line under the horizontal level group belong to these later arguments. [All admissible points in B8.24][all-points] · [B8.34 construction and quantifiers][linked] · [v40 harmonic kernel and integral generators][short-a] · [Denominator and radius][short-b] · [Equivariant Hodge-line descent][orbit]

## From the Chow height to the original family covolume

Suppose now that the upper normalized-image comparison has been established on these same components. Write $h_Z$ for the normalized Chow height, $d_Z$ for the unsquared normalized Arakelov degree at the determinant weight, $r_Z$ for its rank, $T$ for the fitted degree, and $E=E_p$ for the layer error. The arithmetic determinant estimate B8.25e gives
$$
 d_Z\ge w_Z\{T h_Z-3(d+1)|h_Z|-A\log(2+|h_Z|)-R\},
 \quad w_Z=\binom{T-1}{d}\Delta_Z,\quad
 A\log\max(A,1)+R\le C_{\rm HS}E .
$$
Here $\Delta_Z$ is the image degree at the original quotient weight. The hypotheses on degrees and ranks are $(1-\rho)\Delta_Z\le\Delta'_Z\le\Delta_Z$, common positive shifted degree $\Delta'_Z=\Delta_*$, and $(1-z)r_Z\le w_Z\le r_Z$. In particular the unweighted mean bound on $s_Z$ is also its $\Delta'_Z$-weighted mean bound. More generally the latter suffices. For each $Z$, the image bound gives $h_Z+c_s\ge0$ and $\Delta_Z(h_Z+c_s+c_c)\ge\Delta'_Z(s_Z+c_s)_+$. Sum before dividing by $\sum_Z\Delta_Z$. If the weighted mean of $s_Z$ is at least $-X$, the weighted mean of $h_Z+c_s$ with weights $w_Z$ is at least $(1-\rho)c_s-X-c_c$. This follows because $\sum_Z\Delta'_Z/\sum_Z\Delta_Z\in[1-\rho,1]$, $X,c_s\ge0$. [Determinant estimate and degrees][det-deg] · [Degree-weighted derivation](PERIOD_WEIGHTED_ROOT_INTERSECTION.md)

Put $a=T-3d-4\ge0$ and $L_A=A\log\max(A,1)$. For $t\ge0$, $A\log(2+t)\le t+L_A+2$. From $|h_Z|\le h_Z+2c_s$ the braces above are at least $a(h_Z+c_s)-N_0$, where $N_0=(a+6d+8)c_s+L_A+2+R$. Put $y=a[(1-\rho)c_s-X-c_c]-N_0$. Then $\sum d_Z\ge y\sum w_Z$. In passing to $\sum r_Z$, a negative $y$ stays a valid lower bound while a positive $y$ is multiplied by at least $1-z$. Hence the doubled cover slope is at least $2(y-z\max(y,0))$. For the uniform estimate use
$$
 H=T(X+c_c)+c_s[6d+10+T(z+2\rho)]+L_A+R+4.
$$
The preceding inequalities give $y\ge-H$, and $H\ge0$ makes $-H$ valid regardless of the rank ratio. The B8.28 budgets $TX,Tc_c\le C_{\rm ht}E$ and $c_s[6d+10+T(z+2\rho)]\le C_{\rm ht}E$, together with $E\ge1$, give $\mu_Y(u_M)\ge-C_U E$, $C_U=2(3C_{\rm ht}+C_{\rm HS}+4)$. The factor two converts the entire degree from unsquared to squared norm. [v40 B8.29 arithmetic calculation][chow-slope] · [Exact reference determinant](PERIOD_SELECTED_REFERENCE_DETERMINANT.md)

At a nonterminal stage let $A_-$ be the negative-shift lattice and $B_\chi$ the zero-shift type lattice on the same cover. The flat comparison with $C_F=1183$ gives $\mu(A_-)\ge-M_{p,i}-(C_F+C_U)E$. For the horizontal group $S$ write $l=|S|$, $n=l\,\operatorname{rk}B_\chi$ and $r=\operatorname{rk}A_->0$. The orbit-separating section on this cover has a translate matrix invertible at each component's generic point. Multiplying by each translate and then taking the integral character sum gives an injective map $A_-\to B_\chi^{\oplus l}$, of squared operator norm at most $e^{2b}$. Conversely the same translate matrix embeds $B_\chi^{\oplus l}$ in the positive shift. The shifted rank comparison thus gives $r\le n\le(1+b/\mathcal K)r$, with $\mathcal K=P_*\kappa\ge\max(b,|M_{p,i}|)$. v40 obtains the separating section with the actual $c_0$ by descending the Hodge line to the finite quotient, one-point adjoint separation on the quotient and pullback to the entire étale orbit. This uses the complementary unipotent split mark when the other mark is unrestricted. [v40 orbit argument][orbit] · [Maps and ranks][maps] · [Rank comparison on the original cover][jin-ranks]

To bound the degree of the quotient by the saturated image, apply $\sum_{g\in S}\chi(g)^{-1}g$ to the short integral vectors of the **whole** zero-shift space. This operator is integral and acts by $l$ on the type. Its images therefore span the type rationally, and their norms are at most $e^{\mathcal K}$ at the family cutoff. Insert them into the $l$ summands, select $n-r$ independent vectors after quotient, and apply Hadamard. The quotient contributes at least $-2(n-r)\mathcal K$ to total squared degree. Saturating the image increases its degree. Thus for every $t\le\mu(A_-)-2b$,
$$
 \mu(B_\chi)\ge\frac{rt-2(n-r)\mathcal K}{n}
       \ge t-\frac b{\mathcal K}(|t|+2\mathcal K).
$$
For the second inequality a negative $t+2\mathcal K$ already improves the lower bound. At $t=-M_{p,i}-(C_F+C_U)E-2b$, the loss is at most $5b+(C_F+C_U)E$. The relative-different inclusion for the same core lattice costs at most $2b$ under normalized field descent. Using $b\le E$ gives $\mu_{\rm core}\ge-M_{p,i}-[2(C_F+C_U)+9]E$. At the terminal stage the integral character orbit sum on the finite set of definite components is norm-nonincreasing for the probability Petersson metric. The Weyl dimension, flat anchor and polarization terms there give $C_{\rm term}=135$. Hence the two formulas hold with $C_{\rm core}=\max\{135,2(C_F+C_U)+9\}$. [Jin's short vectors inside the type and core descent][jin-type] · [Relative different and saturation on the core space](PERIOD_SELECTED_REFERENCE_DETERMINANT.md) · [Terminal estimate][terminal]

Finally put $L=\Lambda_{\rm type}$ in the realized metric, $L_g=L\cap\operatorname{im}e$, $L_b=L\cap\ker e$ and write $r_g,r_b$ for their ranks. The projector here is orthogonal at every embedding. The group order $g_P$ clears it integrally. The two bad-label projector traces on regular copies bound the discarded rank by $3\delta\operatorname{rk}L$, $\delta=\exp(-x^{e_z/7})$. In the nonterminal case the translate matrix places the row representation inside regular copies; their dimension relative to the Whittaker space costs at most $3/2$. In the terminal case free orbits give the copies directly. This uses the original squarefree Green label shares at the two primes, the cover-rank comparisons, and compatibility of the finite group actions with the realized type. [Two-prime traces and ranks][bad-rank]

The map $1-e$ injects $L/(L_g\oplus L_b)$ in $g_P^{-1}L_b/L_b$. Thus the finite-index gain is at most $2r_b\log g_P$ in total squared degree, even when $r_b=0$. By orthogonality and $\mu(L_b)\le\mu_{\max}(\Lambda_{\rm all})$ for positive bad rank,
$$
 \mu(L_g)\ge\mu(L)-\frac{r_b}{r_g}
   [\mu_{\max}(\Lambda_{\rm all})+2\log g_P-\mu(L)] .
$$
For $\delta\le1/12$ one has $r_b/r_g\le4\delta$ and $r_g>0$. The realized norm comparison costs $C_1 E=2C_{\rm meas}E$. The polynomial size and maximal-slope bounds give a common upper bound $Q=(x^{A_0}+x^{B_0}+C_1+C_{\rm core}+1)E$ for each of $-\mu(L),\mu_{\max}(\Lambda_{\rm all}),2\log g_P$. The cost of projection is at most $12\delta Q\le E$ at one threshold for every point and layer. The good lattice has the primitive rank $D_{\rm norm}$ and its recursive frame rescales norms by $1/\sqrt{n_P}$ with $n_P\ge1$. Its normalized log covolume consequently satisfies B8.24 with $C_0=C_1+C_{\rm core}+1$. Since $E\ge0$, the same threshold works for all $C\ge C_0$. [Integral and orthogonal cut][projector] · [Realized norm, primitive rank, and common cutoff][last] · [Original terminal lattice and good projection](PERIOD_TERMINAL_REFERENCE_COVOLUME.md)

Under the named standing geometric, representation-theoretic and family-size inputs, these implications give the **preselection** geometric estimate B8.24 once the normalized-image comparison is in hand. B8.34 then takes the twelve open row conditions, the height-counting extension with its law, and the linked representation inputs. Its output supplies one pair of member and bundle conditions for all prospective compatible selections. The paired finite indices, local-error/window bound, and supply of those original open rows are separate from B8.24. [Exact hypotheses of B8.34][linked]

[moriwaki]: https://arxiv.org/pdf/math/0612269#page=42
[universal]: https://github.com/rh-lean-roadmap/rh-lean-roadmap/blob/6c23d34a14a3ecf19504ed4182596217ca75006b/docs/src/book/main.tex#L20030-L20046
[premises]: https://github.com/rh-lean-roadmap/rh-lean-roadmap/blob/6c23d34a14a3ecf19504ed4182596217ca75006b/docs/src/book/main.tex#L19936-L19940
[jin-vol]: https://github.com/yuiyuiui/Natural-Language-Proof-Generalized-Riemann-Hypothesis/blob/405237610e58ab9d4a9d5d54d9a0548a0c44227c/sections/j-arithmetic-covolume.tex#L3715-L3731
[native-count]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AutomorphicSpectrum/Proofs/GeometryProofs/UniformAllNormHeightBound.lean#L300-L327
[ht]: https://github.com/rh-lean-roadmap/rh-lean-roadmap/blob/6c23d34a14a3ecf19504ed4182596217ca75006b/docs/src/book/main.tex#L50443-L50448
[approx]: https://github.com/yuiyuiui/Natural-Language-Proof-Generalized-Riemann-Hypothesis/blob/405237610e58ab9d4a9d5d54d9a0548a0c44227c/sections/j-arithmetic-covolume.tex#L2959-L2963
[boundary]: https://github.com/yuiyuiui/Natural-Language-Proof-Generalized-Riemann-Hypothesis/blob/405237610e58ab9d4a9d5d54d9a0548a0c44227c/sections/j-arithmetic-covolume.tex#L3745-L3816
[trace-proof]: https://github.com/rh-lean-roadmap/rh-lean-roadmap/blob/6c23d34a14a3ecf19504ed4182596217ca75006b/docs/src/book/main.tex#L50749-L50755
[native-powers]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AutomorphicSpectrum/Proofs/GeometryProofs/FullIntersectionWeightBound.lean#L149-L204
[jin-trace]: https://github.com/yuiyuiui/Natural-Language-Proof-Generalized-Riemann-Hypothesis/blob/405237610e58ab9d4a9d5d54d9a0548a0c44227c/sections/j-arithmetic-covolume.tex#L3818-L3848
[finite]: https://github.com/yuiyuiui/Natural-Language-Proof-Generalized-Riemann-Hypothesis/blob/405237610e58ab9d4a9d5d54d9a0548a0c44227c/sections/j-arithmetic-covolume.tex#L3850-L3875
[native-slack]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AutomorphicSpectrum/Proofs/GeometryProofs/UniformAllNormHeightBound.lean#L332-L358
[native-end]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AutomorphicSpectrum/Proofs/GeometryProofs/UniformAllNormHeightBound.lean#L359-L372
[jin-lower]: https://github.com/yuiyuiui/Natural-Language-Proof-Generalized-Riemann-Hypothesis/blob/405237610e58ab9d4a9d5d54d9a0548a0c44227c/sections/j-arithmetic-covolume.tex#L3877-L3897
[mean]: https://github.com/rh-lean-roadmap/rh-lean-roadmap/blob/6c23d34a14a3ecf19504ed4182596217ca75006b/docs/src/book/main.tex#L20189-L20199
[jin-slope]: https://github.com/yuiyuiui/Natural-Language-Proof-Generalized-Riemann-Hypothesis/blob/405237610e58ab9d4a9d5d54d9a0548a0c44227c/sections/j-arithmetic-covolume.tex#L5418-L5453
[all-points]: https://github.com/rh-lean-roadmap/rh-lean-roadmap/blob/6c23d34a14a3ecf19504ed4182596217ca75006b/docs/src/book/main.tex#L19612-L19621
[linked]: https://github.com/rh-lean-roadmap/rh-lean-roadmap/blob/6c23d34a14a3ecf19504ed4182596217ca75006b/docs/src/book/main.tex#L21789-L21804
[short-a]: https://github.com/rh-lean-roadmap/rh-lean-roadmap/blob/6c23d34a14a3ecf19504ed4182596217ca75006b/docs/src/book/main.tex#L51155-L51164
[short-b]: https://github.com/rh-lean-roadmap/rh-lean-roadmap/blob/6c23d34a14a3ecf19504ed4182596217ca75006b/docs/src/book/main.tex#L51209-L51215
[orbit]: https://github.com/rh-lean-roadmap/rh-lean-roadmap/blob/6c23d34a14a3ecf19504ed4182596217ca75006b/docs/src/book/main.tex#L54016-L54018
[n-cut]: https://github.com/rh-lean-roadmap/rh-lean-roadmap/blob/6c23d34a14a3ecf19504ed4182596217ca75006b/docs/src/book/main.tex#L50740-L50747
[prime-sum]: https://github.com/rh-lean-roadmap/rh-lean-roadmap/blob/6c23d34a14a3ecf19504ed4182596217ca75006b/docs/src/book/main.tex#L50758-L50771
[det-deg]: https://github.com/rh-lean-roadmap/rh-lean-roadmap/blob/6c23d34a14a3ecf19504ed4182596217ca75006b/docs/src/book/main.tex#L20250-L20272
[chow-slope]: https://github.com/rh-lean-roadmap/rh-lean-roadmap/blob/6c23d34a14a3ecf19504ed4182596217ca75006b/docs/src/book/main.tex#L53987-L54011
[maps]: https://github.com/rh-lean-roadmap/rh-lean-roadmap/blob/6c23d34a14a3ecf19504ed4182596217ca75006b/docs/src/book/main.tex#L54021-L54032
[jin-ranks]: https://github.com/yuiyuiui/Natural-Language-Proof-Generalized-Riemann-Hypothesis/blob/405237610e58ab9d4a9d5d54d9a0548a0c44227c/sections/j-arithmetic-covolume.tex#L5476-L5529
[jin-type]: https://github.com/yuiyuiui/Natural-Language-Proof-Generalized-Riemann-Hypothesis/blob/405237610e58ab9d4a9d5d54d9a0548a0c44227c/sections/j-arithmetic-covolume.tex#L5532-L5587
[terminal]: https://github.com/rh-lean-roadmap/rh-lean-roadmap/blob/6c23d34a14a3ecf19504ed4182596217ca75006b/docs/src/book/main.tex#L54036-L54070
[bad-rank]: https://github.com/rh-lean-roadmap/rh-lean-roadmap/blob/6c23d34a14a3ecf19504ed4182596217ca75006b/docs/src/book/main.tex#L54073-L54088
[projector]: https://github.com/rh-lean-roadmap/rh-lean-roadmap/blob/6c23d34a14a3ecf19504ed4182596217ca75006b/docs/src/book/main.tex#L54090-L54105
[last]: https://github.com/rh-lean-roadmap/rh-lean-roadmap/blob/6c23d34a14a3ecf19504ed4182596217ca75006b/docs/src/book/main.tex#L21715-L21770
