# The finite level of the transported bottom period

Fix the bottom odd Witt string of the Sernau seesaw. Identify its rational Hermitian frame, marked middle vector, source form and base additive character with the frame on which the native simple-root character is being tested. Write $K^\circ$ for the finite lattice stabilizer, $K=J_M$ for its principal subgroup at the two marked primes, and $J_\vartheta=\mathrm{levelY}(\vartheta,0)\subset K$ for the additional principal level at the twist places. Put $R_h f(x)=f(xh)$. All period integrals below use the same transported Bessel quotient measure. The identity concerns the row produced by the last descent to the bottom in Sernau’s rewrite. Its application to an original selected word requires the stated identifications.

For a conjugate row $z_1$ on $Y_1$, let $T_\vartheta z_1$ denote its unscaled transposed theta integral. The actual row is $z_\vartheta=[K^\circ:J_\vartheta]T_\vartheta z_1$. This includes the case where all the preceding descents produced $z_1$. The Petersson pairing with the bottom Poincaré column tests exactly the row
$$
 Z_\vartheta=A_K z_\vartheta
   ={1\over[K:J_\vartheta]}\sum_{k\in K/J_\vartheta} R_kz_\vartheta
   =[K^\circ:K]\sum_{k\in K/J_\vartheta}R_k T_\vartheta z_1.                 \tag{1}
$$
Indeed the column is right $K$-fixed and the quotient measure is right invariant. Substitution of the finite sum into the Bessel integral gives Sernau's cut sum term by term. Its common prefactor is exactly $[K^\circ:K]=\prod_{i=0,1}|GL_n(\mathbf F_{p_i})|^{[E^+:\mathbf Q]}$, by surjectivity of reduction at the chosen split places. In particular, for every $d\in K$, $R_dZ_\vartheta=Z_\vartheta$, including when $d$ acts nontrivially on the unaveraged row. This follows by the permutation $kJ_\vartheta\mapsto dkJ_\vartheta$. [Principal level][act6-k] · [Actual finer level][act6-j] · [Normalized transposed lift][act6-t] · [Poincaré trace][act6-p] · [Actual seesaw cut sum][act6-s]

Use the [rational character comparison](EXTERNAL_PROOF_COMPARISON.md) with $a=\varepsilon/\beta=-\varepsilon M\delta_E$ for the native unit-parameter character. The torus $D$ acts by $a^{r-i}$ and its conjugate inverse on opposite string lines, and fixes $X$ and the middle vector. Every unit component away from $M$ belongs to $K$. Indeed the integral string lines differ from the rational ones by scalings, and $D$ fixes both summands of the single mixed integral generator. Define $t$ by keeping $D_f^{-1}$ at places over $M\mathfrak D_{E/\mathbf Q}$, setting its other components to one. For every real probe $g$,
$$
 B_{\rm wb}(g,\phi,Z_\vartheta)
   = B_{\rm nat}(D_\infty^{-1}g,\phi,R_tZ_\vartheta).                    \tag{2}
$$
The substitution by rational $D$ in the Bessel period preserves unipotent Haar by the product formula. It centralizes the source group. Rational left invariance moves $D^{-1}$ onto the test, and the finite unit components disappear by (1). Conjugating both row and character slots gives the same assertion in Petersson conventions. [Actual generic constant and integral lattice][act6-grad]

In particular, every twist place of the auxiliary sets used for the congruences disappears from the finite translation in (2). For each such $w$ the residue cardinality is a rational prime $p$ prime to the marked level $M$ and the prescribed auxiliary modulus of the Selmer construction. Write $K_0$ for the imaginary quadratic base. The field $E=K_0(\zeta_{q_1})$ contains $\mu_3$ and $\mu_{2^s}$. The roots of unity of order prime to the residue characteristic inject on reduction. Thus $p\ne2$ because the residue field of cardinality two cannot contain the cube roots of unity, and $2^s\mid p-1$. The tower inequalities give $2^s=m^{22}\ge x^{11}>\max(q_0,d,3)$. All prime divisors of $q_1d=3^c2^s q_0d$ are smaller than $p$, and the absolute different divides $(q_1d)$. This proves $D_w\in K_w$ at every one of these places. For the raw native coefficient $\varepsilon\xi_0$, the same conclusion holds wherever the additional integer $\mathrm N\mathfrak c_{K_0}$ is a unit, with $a=\varepsilon M u\Delta_{\rm rel}/\mathrm N\mathfrak c_{K_0}$ and the previously specified raw frame. (1) and (2) use the full normalized trace. They do not assert invariance of individual cut terms. [Prime-norm requirement][act6-aux] · [Construction of the actual twists][act6-chi] · [Field and size hypotheses][act6-data] · [Tower exponent][act6-size] · [Conductor in the different][act6-diff]

**The level at the remaining places.** Put $K'=tKt^{-1}$ and $H=K\cap K'$. The transported row $R_t Z_\vartheta$ has level $K'$, by direct right translation. On cuspidal spaces of the chosen real type $R_t:\mathcal A^K\to\mathcal A^{K'}$ is a Petersson isometry with inverse $R_{t^{-1}}$. Consequently the Petersson representatives for the two bottom period functionals on the matched datum satisfy
$$
 R_t P_{\rm wb}^{K}(g)\phi
   =P_{\rm nat}^{K'}(D_\infty^{-1}g)\phi.                         \tag{3}
$$
Pair both sides against $R_t y$ with $y\in\mathcal A^K$ and apply (2), whose character and unit-place calculation applies to every coarse row. Nondegeneracy proves (3), including for zero representatives. This fixes the exceptional finite translation on an explicitly identified level without evaluating it as a scalar. A different quotient Haar rescales the representative by the same positive factor as the period. [Riesz characterization][act6-riesz]

For the unit-parameter comparison all the nontrivial local intersections can be computed in split $GL_n$. The marked level primes split by their defining congruence. A rational prime $p\mid q_1d$ satisfies $p<2^s$, whereas a conjugation-fixed place over $p$ would give $p\equiv-1\pmod{2^{s+1}}$. Hence every exceptional factor at the different splits over the real subfield too. Choose one place in each conjugate pair, write $q$ for its residue cardinality and $e=|\operatorname{ord}_w(a)|>0$. With $b=\dim_E X+1$ and $n=2r+b$, the elementary divisors of $t$ relative to the actual lattice, up to order, have exponents
$$
 \lambda=e(r,r-1,\ldots,1,0^b,-1,\ldots,-r),\qquad
 S=\sum_{i<j}(\lambda_i-\lambda_j)
   =e\,r(r+1)(4r-1+3b)/3.
$$
At the opposite half, the absolute valuations of $a$ agree because $(M\delta_E)$ is invariant under conjugation. In the lattice basis adapted to the string this is a diagonal transformation, including its mixed fixed vector. Integral change of basis preserves the local subgroup and the ensuing index. If $I_w=[K_w:K_w\cap t_w K_wt_w^{-1}]$, then
$$
 I_w=\begin{cases}
 q^{S}, & w\mid M,\\
 [GL_n(\mathbf F_q):P(\mathbf F_q)]\,q^{S-B},
      & w\mid\mathfrak D_{E/\mathbf Q},
 \end{cases}\qquad
 B={n\choose 2}-{b\choose 2},
$$
where $P$ is the block parabolic of sizes $1^r,b,1^r$. At principal level $1+\pi M_n(\mathcal O)$, every positive gap $h=\lambda_i-\lambda_j$ imposes $h$ extra powers of $\pi$ on that off-diagonal entry. At full level, reduction modulo $\pi$ imposes the parabolic condition, then each positive gap imposes $h-1$ additional powers. The additive matrix coordinates have constant Haar density on these integral invertible matrices. At $r=0$ or $e=0$ the index is one. Taking one factor per split pair gives $[K:H]=\prod_w I_w$. If the output is also projected to $K$, its normalized Hecke action is exactly $[K:H]^{-1}\sum_{\gamma\in K/H}R_{\gamma t}Z_\vartheta$. Equation (2) itself uses the single transported row on $K'$. Identifying this row and its native source with the prescribed marked level, character and word-operated arithmetic column is still required for entries 1 and 4. [Split-place test][act6-split] · [Marked primes][act6-m]

The exceptional translate also has an exact expression on the first theta edge. Let $\Phi_\vartheta=\mathrm{datumY}(\vartheta,0)$ on $\operatorname{Hom}(Y_0,Y_1)$ and let $\omega_\vartheta$ be its actual twisted pair Weil representation, with Sernau's rank twist at stage one. Denote the unscaled transposed integral with test $\Phi$ by $T[\Phi]z_1$. Then the single finite alteration
$$
 \Phi_{\vartheta,t}
   =[K^\circ:K]\sum_{k\in K/J_\vartheta}
         \omega_\vartheta((1,tk),1)\Phi_\vartheta,\qquad
 R_t Z_\vartheta=T[\Phi_{\vartheta,t}]z_1                         \tag{4}
$$
works for every $z_1$, and so for each subsequent descent producing it. Indeed, the integrand at a right-translated argument $g(1,u)$ contains $\omega_\vartheta(g,h)\omega_\vartheta((1,u),1)\Phi_\vartheta$. Taking the finite sum in (1) gives (4), with the order $tk$ forced by $R_tR_k=R_{tk}$. The finite test does not depend on coset representatives because $\Phi_\vartheta$ itself is fixed by $J_\vartheta$ on the $Y_0$ side. Each term is the translate of an absolutely integrable theta kernel, and the sum is finite. This determines the correcting Schwartz test before the first descent and includes its splitting-character factors through the genuine representation. An identification with the native glued column after its word operators would have to use the action of this particular test. [Actual transposed theta integral][act6-t] · [Schwartz-vector level invariance and composition law][act6-weil]

On this actual edge the determinant-character scalar of the exceptional move is exactly $1$ at every place. In fact
$$
 \det D=(a/\bar a)^{r(r+1)/2},\qquad r=\varrho=m/2-1.
$$
For the unit-parameter comparison $\bar a=-a$ since $\bar\delta_E=-\delta_E$. The tower length $m$ is a power of two exceeding four, so $r(r+1)/2=(m/2-1)(m/4)$ is even. In the raw comparison $a$ belongs to the totally real subfield, giving the same determinant directly. Consequently every retained component of $t$ has determinant one. The source defines the pair action at $(g,h)$ as the underlying Weil action on $x\mapsto hxg^{-1}$ times $\alpha_{Y_0}(\det h)\alpha_{Y_1}(\det g)^{-1}$. Hence
$$
 \omega_\vartheta((1,t),1)=
 \omega_{\operatorname{Hom}(Y_0,Y_1)}
        \bigl(\operatorname{onHom}((1,t),1)\bigr).
$$
The exceptional operator in (4) is therefore independent of the splitting characters and of $\vartheta$ on the common Schwartz space. The residue representatives and their twisted action still enter the sum. [Purity of the different generator][act6-im] · [Bottom string length][act6-str] · [Power-of-two and size premises][act6-pow] · [Pair character and pair Weil representation][act6-pair] · [Rank convention][act6-rank]

[act6-k]: https://github.com/lsernau/grh-lean/blob/72fead102f663d5c7a407964a13dc0cf9d977207/grh/src/New/UpperBound/Objects/LiftChains.lean#L454-L467
[act6-j]: https://github.com/lsernau/grh-lean/blob/72fead102f663d5c7a407964a13dc0cf9d977207/grh/src/New/UpperBound/Objects/Rows.lean#L346-L365
[act6-t]: https://github.com/lsernau/grh-lean/blob/72fead102f663d5c7a407964a13dc0cf9d977207/grh/src/New/UpperBound/Seesaw/SeesawIdentity.lean#L171-L195
[act6-p]: https://github.com/lsernau/grh-lean/blob/72fead102f663d5c7a407964a13dc0cf9d977207/grh/src/New/UpperBound/Objects/PoincareMap.lean#L212-L253
[act6-s]: https://github.com/lsernau/grh-lean/blob/72fead102f663d5c7a407964a13dc0cf9d977207/grh/src/New/UpperBound/Seesaw/SeesawIdentity.lean#L358-L399
[act6-grad]: https://github.com/lsernau/grh-lean/blob/72fead102f663d5c7a407964a13dc0cf9d977207/grh/src/New/UpperBound/Seesaw/LevelIdeles.lean#L77-L132
[act6-aux]: https://github.com/lsernau/grh-lean/blob/72fead102f663d5c7a407964a13dc0cf9d977207/grh/src/New/Congruences/Selmer/AuxiliaryPrimes.lean#L93-L98
[act6-chi]: https://github.com/lsernau/grh-lean/blob/72fead102f663d5c7a407964a13dc0cf9d977207/grh/src/New/Congruences/Selmer/ClassSums.lean#L387-L415
[act6-data]: https://github.com/lsernau/grh-lean/blob/72fead102f663d5c7a407964a13dc0cf9d977207/grh/src/New/Reduction/Data/AdmissibleData.lean#L27-L38
[act6-size]: https://github.com/lsernau/grh-lean/blob/72fead102f663d5c7a407964a13dc0cf9d977207/grh/src/New/Reduction/Data/Sizes.lean#L78-L110
[act6-diff]: https://github.com/lsernau/grh-lean/blob/72fead102f663d5c7a407964a13dc0cf9d977207/grh/src/New/Derivatives/Field/PrimeDecomposition.lean#L253-L280
[act6-riesz]: https://github.com/lsernau/grh-lean/blob/72fead102f663d5c7a407964a13dc0cf9d977207/grh/src/New/UpperBound/Objects/PoincareMap.lean#L175-L201
[act6-split]: https://github.com/lsernau/grh-lean/blob/72fead102f663d5c7a407964a13dc0cf9d977207/grh/src/New/Derivatives/Field/PrimeDecomposition.lean#L787-L809
[act6-m]: https://github.com/lsernau/grh-lean/blob/72fead102f663d5c7a407964a13dc0cf9d977207/grh/src/New/Reduction/Data/AdmissibleData.lean#L139-L151
[act6-weil]: https://github.com/lsernau/grh-lean/blob/72fead102f663d5c7a407964a13dc0cf9d977207/grh/src/New/UpperBound/Seesaw/SeesawIdentity.lean#L227-L258
[act6-im]: https://github.com/lsernau/grh-lean/blob/72fead102f663d5c7a407964a13dc0cf9d977207/grh/src/New/Derivatives/Field/PrimeDecomposition.lean#L350-L365
[act6-str]: https://github.com/lsernau/grh-lean/blob/72fead102f663d5c7a407964a13dc0cf9d977207/grh/src/New/UpperBound/Seesaw/EdgePairEvaluation.lean#L1140-L1153
[act6-pow]: https://github.com/lsernau/grh-lean/blob/72fead102f663d5c7a407964a13dc0cf9d977207/grh/src/New/Reduction/Data/AdmissibleData.lean#L96-L118
[act6-pair]: https://github.com/lsernau/grh-lean/blob/72fead102f663d5c7a407964a13dc0cf9d977207/grh/src/Lib/Weil/DualPair/Defs.lean#L170-L182
[act6-rank]: https://github.com/lsernau/grh-lean/blob/72fead102f663d5c7a407964a13dc0cf9d977207/grh/src/Lib/Weil/DualPair/WeilAction.lean#L764-L769
