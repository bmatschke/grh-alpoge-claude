# How the whole slope filtration changes between the selected character levels

On a linked member write $R_g$ for the principal good row and $R_0,R_1$ for the base and sharp rows, with their actual glued lattices. Let $e_0,e_1$ be the two character projectors, $h_i$ their subgroup orders, $c_i=\log h_i$, and $\mu_i=\mu(R_i)$. All degrees below use normalized squared norms. The principal Harder–Narasimhan filtration gives a common list of slopes for the two character cuts. The finite representation in each graded piece gives the number of times to use each slope. After sorting, the resulting list for level $i$ differs from the slopes of its actual row by at most $c_i$ in every position.

This comparison proves both assertions of Roadmap B4.55a on the selected rows. It also gives a version of the dual mean estimate in which one can replace a maximum by a bound on an averaged upper tail. [Original two assertions][pass] · [Group, lattices and all-place metrics on this bundle](PERIOD_SHARP_ROW_TRANSFER.md) · [Hermitian slopes and heights of maps, Bost §4.1][bost]

## Two integral maps bound every position in the polygon

Write $F_L^{>t}$ for the rational span of the Harder–Narasimhan steps of a Hermitian lattice $L$ with slope greater than $t$. For an integral map $A:L\to M$ with squared operator norm at most $\exp(c)$ at every embedding,
$$
                         A F_L^{>t+c}\subset F_M^{>t}.
                         \tag{1}
$$
Indeed, a nonzero map from that source step to the quotient by the target step induces an injection from a positive-rank source quotient into its image. The saturated kernel gives the quotient metric, and the projection to the target quotient is contractive. Its determinant inequality bounds the quotient slope by the target image slope plus $c$. But the source quotient has slope greater than $t+c$ and the image has slope at most $t$. This proves (1), including at filtration jumps.

Write $V=R_g\otimes K$ and identify $R_i\otimes K$ with $e_iV$ by $J_i$. The maps $J_i:R_i\to R_g$ and $S_i=J_i^{-1}h_i e_i:R_g\to R_i$ are integral even at primes dividing $h_i$. This follows by summing integral translates at each serving tuple before gluing. Both maps have squared norms at most $h_i$ at every embedding, by the subgroup-order normalization and unitarity. The principal filtration is $G$-invariant by uniqueness and the integral isometric action of $G$. In particular $F_{R_g}^{>t}\cap e_iV=e_i F_{R_g}^{>t}$. Applying (1) to the two maps gives
$$
 e_iF_{R_g}^{>t+c_i}\ \subseteq\ J_i F_{R_i}^{>t}\
 \subseteq\ e_i F_{R_g}^{>t-c_i}.
 \tag{2}
$$
The scalar $h_i$ disappears on rational subspaces. No integral equality between the actual level lattice and the intersection lattice is used. [Serving-tuple averaging and metrics](PERIOD_SHARP_ROW_TRANSFER.md#the-representation-and-the-glued-lattices)

Let $\alpha_j$ be the distinct slopes in the principal filtration, and $V_j$ its graded representations. By exactness of taking the image of an idempotent, $\dim e_iF_{R_g}^{>t}=\sum_{\alpha_j>t}\dim(e_i V_j)$. Make a list of the $\alpha_j$ with these multiplicities at level $i$, sorted in decreasing order. Equation (2) bounds each actual slope between its corresponding list entry minus $c_i$ and that entry plus $c_i$. This also proves the assertion for repeated slopes of either lattice.

## The dual mean bound, including its normalization

At the chosen embedding every constituent of every $V_j$ is good. Each good irreducible $\chi$ contains the base character once. Write $n_\chi$ for the sharp multiplicity. At each of the $2f$ marked factors of residue size $q$ and rank $r=k+m-1$, the mirabolic trace formula for the prescribed cuspidal blocks gives
$$
 n_w=\sum_{a=0}^k C_a\gamma_q(k-a),\qquad
 \gamma_q(0)=1,\quad \gamma_q(l)=q^l-q^{l-1}\quad(l>0).
$$
Here $C_a$ counts subsets of blocks of total length $a$. The empty set contributes $q^k(1-1/q)$. A subset with length $a$ determines a distinct subset of $a$ positions among $r$. Its normalized contribution is at most $q^{-a}$, so all nonempty choices contribute at most $(1+q^{-1})^r-1\le2r/q$ on the late range. The local traces multiply under the selected group and character identifications. With $g=\min(g_0,g_1)$, $4fr/g\le1$, and $\overline n=\prod_w q_w^k$, this proves
$$
 (1-\delta)\overline n\le n_\chi\le(1+\delta)\overline n,\qquad
                 \delta=8fr/g\le1/3
 \tag{3}
$$
after increasing the cutoff. For the lower bound use $\prod_w(1-q_w^{-1})\ge1-2f/g$; for the upper bound use $\exp(4fr/g)\le1+8fr/g$. In particular both levels see all occurring constituents. [Base character and selected types](continuation_v73/reading.tex#L3-L38) · [Mirabolic trace and derivative counts][trace] · [Exact finite-group calculation][count]

Let $p_j=\dim(e_0 V_j)/\mathrm{rk}\,R_0$ and $q_j=\dim(e_1 V_j)/\mathrm{rk}\,R_1$, omitting zero graded pieces and using the positive-rank range. In grade $j$ the ratio of sharp to base dimension is a weighted average of the $n_\chi$. The same is true of the total rank ratio. Hence $|q_j/p_j-1|\le \theta=2\delta/(1-\delta)\le3\delta$. Write $E_0=\sum_jp_j\alpha_j$, $E_1=\sum_jq_j\alpha_j$. Equation (2) gives $|\mu_i-E_i|\le c_i$. Given any $U\ge\mu_{\max}(R_0)$, the base level sees every principal grade, so $\alpha_j\le U+c_0$. Subtract the two means from this common upper bound to obtain
$$
 U+c_0-E_1\le(1+\theta)(U+c_0-E_0).
$$
Duality and the two metric errors give
$$
 \mu(R_1^\vee)\le\mu(R_0^\vee)+c_0+c_1+
                 \theta\bigl(U+\mu(R_0^\vee)+2c_0\bigr).
 \tag{4}
$$
Also (2) gives $\mu_{\max}(R_1)\le U+c_0+c_1$. Since $c_i\le\log|G|$, the two estimates imply the original B4.55a bounds with their stated constants. Formula (4) is invariant when one translates all the row slopes by the same amount and translates $U$ with them. Thus it applies to the normalized row and to the dual comparison entering the word-height calculation. It does not require the reference covolume estimate in order to pass between levels. That estimate is a separate input to the *absolute* word inequality. [Use in the division package][word]

For a threshold $T$ write $\mathcal T_i(T)=\mathrm{rk}(R_i)^{-1}\sum_l(\mu_l(R_i)-T)_+$. Two useful consequences of the same proof are
$$
 \mathcal T_1(T+c_0+c_1)\le(1+\theta)\mathcal T_0(T)
 \tag{5}
$$
and
$$
 \mu(R_1^\vee)\le\mu(R_0^\vee)+c_0+c_1+
       \theta\bigl(T-\mu_0+2c_0+2\mathcal T_0(T)\bigr).
 \tag{6}
$$
For (5) apply (2) entrywise and $q_j\le(1+\theta)p_j$. For (6), center $E_1-E_0$ at $T+c_0$. Its absolute value is at most $\theta\sum_jp_j|\alpha_j-(T+c_0)|$. Write the absolute deviation as $T+c_0-E_0+2\sum_j p_j(\alpha_j-T-c_0)_+$. Equation (2) gives (6). Thus the factor near $fr/g$ multiplies only a first absolute moment of the slope distribution.

## The effect of a few large base slopes on the mean-slope argument

The upper tail in (5) has a direct finite-place test. Use a reference lattice with the same infinite metrics as the base row and let $D_d(w)$ be the sum of the $d$ largest signed enlargement exponents at $w$, with $D_0(w)=0$. For $T\ge\mu_{\max}(R_{\rm ref})$,
$$
 \mathcal T_0(T)\le\frac1{\mathrm{rk}\,R_0}
 \max_{0\le d\le\mathrm{rk}\,R_0}
 \left(2\sum_w\ell_wD_d(w)-d(T-\mu_{\max}(R_{\rm ref}))\right).
 \tag{7}
$$
Indeed the unnormalized sum of positive excesses is the maximum of $\deg(L)-T\operatorname{rk}L$ over saturated sublattices, including zero. The slopes strictly above $T$ attain it. Use the reference determinant on the same subspace for each candidate, and apply the exterior-power comparison. [Signed local exponents](PERIOD_REFERENCE_EVALUATION.md#the-remaining-change-of-lattice)

This gives a relaxation for the mean deduction downstream of the frame. Take the integral or finite-index period sublattices and the spanning inequality of the [lattice-loss argument](PERIOD_LATTICE_LOSS.md). Use its source center $s$, upper spread $u\ge0$, average cost $\Delta$, total source rank $R$, target rank $n$, and dimension constants $a,\beta$. The target here is $R_1^\vee$. Choose $H=\max(0,s+T+c_0+c_1)$. Integrate the missing dimensions from $0$ to $H$ as in that argument. For target slopes $\lambda_l$, the normalized positive deficit $n^{-1}\sum_l(s-\lambda_l)_+$ equals the clipped integral plus $\mathcal T_1(H-s)$ by duality. It bounds the signed deficit $s-\mu(R_1^\vee)$. Since $H-s\ge T+c_0+c_1$, (5) gives
$$
 s-\mu(R_1^\vee)\le \frac{aH}{n}
 +\frac{\beta R}{n}\frac{H(u+\Delta)}{H+u}
 +(1+\theta)\mathcal T_0(T).
 \tag{8}
$$
The middle fraction is zero when $H=u=0$. Thus on the usual range for $H$, a base excess of order $b$ suffices for a mean bound with an additional error of that order. In (7) one divides by the total base rank even when a single direction has a large enlargement. The literal maximum in frame entry 2 is supplied separately by the [fitted estimate on the selected row](PERIOD_SELECTED_BASE_FUNCTIONAL.md).

[pass]: https://github.com/rh-lean-roadmap/rh-lean-roadmap/blob/02a95b4c62db610642af5f278ee5d0d6df87b348/docs/src/book/main.tex#L8489-L8515
[trace]: https://github.com/rh-lean-roadmap/rh-lean-roadmap/blob/02a95b4c62db610642af5f278ee5d0d6df87b348/docs/src/book/main.tex#L15033-L15075
[count]: https://github.com/rh-lean-roadmap/rh-lean-roadmap/blob/02a95b4c62db610642af5f278ee5d0d6df87b348/docs/src/book/main.tex#L32984-L32996
[word]: https://github.com/rh-lean-roadmap/rh-lean-roadmap/blob/02a95b4c62db610642af5f278ee5d0d6df87b348/docs/src/book/main.tex#L9134-L9164
[bost]: https://numdam.org/item/10.1007/s10240-001-8191-3.pdf#page=39
