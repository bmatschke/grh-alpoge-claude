# Products of real-place losses and the angular test at large corank

On a tied, represented, nonsingular row write $n=r+1=m/2$, $f=[F:\mathbf Q]$, $g=g_0g_1$, and $T=T_u$. The two loss products in the real orbital estimate admit explicit bounds at every subset of the real places. The special angular estimate for degenerate pairs can also be omitted in a range of coranks of the form $s\ge 2+O(m^2)$, provided the ordinary Hilbert–Schmidt estimate is available at its original moment. At smaller corank the same argument deals with the large-label tail. Both deductions keep the original row weights.

## The two loss products

Put $B=b^{C_hm^2}\ge1$, $d_{\tau l}=\rho^{-2a_l}|\tau p_l|$, $1\le l\le n$, and $g_\tau=d_{\tau n}^2-TT'd_{\tau r}^2$. Write
$$
 \sigma_l=\prod_\tau\max(1,d_{\tau l}/B),\qquad \sigma=\prod_{l=1}^n\sigma_l.
$$
The original real minors have these absolute values because the change to the real frame multiplies row and column $i$ by the same different factor. The determinant takes their product for each selected row and column. The additional empty minor in the real size equals one. The block ends $I$ are the strictly increasing partial sums of the positive block lengths. In block-antidiagonal normal form a leading principal minor is nonzero precisely at a block end. A completed block is invertible, while a proper leading square of the next reversed block is singular. The triangular transformations of the normal form preserve the minors. Thus $I\subset\{1,\ldots,n\}$ is common to all embeddings. The [flag determinant calculation](SPECTRAL_FLAG_PAIR_DETERMINANTS.md) gives
$$
 0<g_\tau\le d_{\tau n}^2,\qquad
 \prod_\tau g_\tau=\det U\ge1,\qquad
 \prod_\tau d_{\tau l}\ge1\quad(l\in I).
$$
For the last inequality, the square of the product is the norm of the integral minor ideal after its prescribed different is removed. [Dictionary on the actual terms][dict] · [Cell and block ends][ends]

Fix $C\ge0$. In this notation the two source losses at a place are
$$
 L_\tau=b^{Cm^4}\max(g_\tau,g_\tau^{-1})^{Cm^2}
         \prod_{l\in I}\max(d_{\tau l},d_{\tau l}^{-1})^{Cm},
 \qquad
 A_\tau=\left(b^{Cm}\max_{l\in I}\max(1,d_{\tau l}^{-1})\right)^{Cr^3}.
$$
For every subset $P$ of embeddings one has
$$
 \begin{aligned}
 \prod_{\tau\in P}L_\tau
 &\le b^{C(1+5C_h)m^4f}\sigma^{4Cm^2+2Cm},\\
 \prod_{\tau\in P}A_\tau
 &\le \big[b^{Cmf} B^{nf}\sigma\big]^{Cr^3}.                 \tag{1}
 \end{aligned}
$$
Indeed, if $z_\tau>0$ and $\prod z_\tau\ge1$, then the product of $\max(1,z_\tau^{-1})$ is at most the product of $\max(1,z_\tau)$. Consequently the product of $\max(z_\tau,z_\tau^{-1})$ over any subset is at most $(\prod\max(1,z_\tau))^2$. Apply this to $g_\tau$, using $\prod\max(1,g_\tau)\le B^{2f}\sigma_n^2$, and to each nonzero block-end minor, using $\prod\max(1,d_{\tau l})\le B^f\sigma_l$. For the second line bound the maximum of the inverse-minor factors by their product before applying the same inequality. Since $|I|\le n=m/2$, substitution gives (1).

The first bound fits $\Gamma\sigma^{C_2m^2}$, with $\Gamma=b^{C_\Gamma m^5 f}$, once $C(1+5C_h)\le C_\Gamma m$ and $C_2\ge5C$. The second fits $b^{C_2m^6f}\sigma^{C_2m^4}$ by enlarging $C_2$ in terms of the fixed $C,C_h$, since $r\le m/2$. Its label exponent in (1) is only $Cr^3$. These are the two multiplication steps in the source's ordinary and angular estimates, including mixed subsets of places. This calculation leaves the single-place operator inequalities and the row covolume to be established in their prescribed measures. [Local factors][factors] · [Two product tests and local inequalities][products]

## The ordinary estimate suffices for the large coranks

Use the ordinary squared-integral bound in [RowsND][ordinary] at its original moment $q$ and the dimension range $R'=d_{u'}/D^\star\le3/\Gamma^2$. The [actual pair count](SPECTRAL_FLAG_PAIR_FIBRES.md) and its [two determinant cutoffs](SPECTRAL_FLAG_PAIR_DETERMINANTS.md) apply. Work with the original eventual parameter bounds of the [primitive mass calculation](SPECTRAL_HIGHER_CORANK_MASSES.md). Write $Z,Z'$ for the labels of the two terms in the same word-pair problem and $S=\sigma_Z\sigma_{Z'}\ge1$. Define
$$
 A=\frac{4B^2}{g^mT},\qquad
 e_s=c(s+m)m+c(1+\log_2(2f)),\qquad
 D_s=(4c-1)k+4c(k-s)m ,
$$
where $c\ge1$ is chosen to dominate the finite-fibre and row-volume exponents in that calculation. The following bounds apply after taking absolute values.

1. For $s\ge3$, all angular configurations at that corank together contribute at most $6d k^{-kf}$, where $d=d_u>0$, whenever
   $$
               (g/2)^{s-2}\ \ge\ A k^{s/8+1}.                  \tag{2}
   $$
   In particular this covers every $s\ge 2+\lceil(2C_hm^2+2)/8\rceil$ with $s\ge3$, in the standing range. The sum over those coranks is $o(d\exp(-kf\log k/2))$.
2. At any $s\ge2$, the same label summation used in the weaker angular bound applies to all pairs satisfying, for fixed $0\le\theta<1/2$,
   $$
                     A^{kf} S^{-D_s}\ \le\ k^{\theta kf}.       \tag{3}
   $$
   In particular the ordinary bound covers the tail $S\ge\max(1,(A/k^\theta)^{kf/D_s})$. Equations (2) and (3) are sufficient tests. At the remaining low coranks only labels failing both (3) and the earlier direct angular test in the primitive mass note still need the special angular bound.

To prove this, the single-flag determinant inequality gives $G_Z\ge\det A_i I_i^2\ge1$. Indeed $A_i$ is a sublattice of the integral definite middle lattice, so its positive determinant is at least one, including the rank-zero convention. Thus $\det U=g^{mf}G_Z\ge g^{mf}$. The exact angular identity gives
$$
 K(Z)=J_Z/\sqrt{\det U}
 \ \le\ \frac{(2B)^f\sigma_{n,Z}}{g^{mf/2}}
 \ \le\ \left(\frac{2B}{g^{m/2}}\right)^f\sigma_Z.
$$
Here $J_Z=\prod_\tau(d_{\tau n}+\sqrt{TT'}\,d_{\tau r})\le2^f\prod_\tau d_{\tau n}$. This also works when the penultimate minor vanishes. Hence the factor left after applying an ordinary bound on each term of a degenerate pair obeys
$$
       [T^{-f}K(Z)K(Z')]^k\ \le\ A^{kf} S^k.                 \tag{4}
$$

The exponent $k$ on $S$ in (4) fits inside the same moment used for the original ordinary bound. Before taking account of (4), the exponent on each label after the two Gram normalizers cancel is at most
$$
      4e_s+4cr^2+C_2 m^2/2-q/n.
$$
Here $4e_s$ comes from the fibre height, $4cr^2$ from the two square roots of the squared orbital bounds (one such factor per label), and $C_2m^2/2$ is the ordinary loss. The genus factor $X_s$ is label-independent at every rank, including the two end ranks. The [source choice of $q$][moment] gives
$$
 q/n \ \ge\ 4ck+4e_k+4cr^2+C_2m^2/2+12n^2 .
$$
The $4ck$ in the source paid for a possible label dependence of its end-rank genus bound. Keeping $X_s$ frees that power. Since $e_k-e_s=c(k-s)m$, multiplication by (4) leaves at most $S^{-12n^2}S^{-D_s} A^{kf}$. The factor $S^{-12n^2}$ still gives the original summable majorant for both label sums. [Origin of the $4ck$ allowance][xi] · [Label summation and rank constants](SPECTRAL_HIGHER_CORANK_MASSES.md)

After this summation the rank bound, divided by $d$, is at most
$$
       2R' (2/g)^{(s-2)kf} F_s\,
       \sup_{\text{included pairs}} A^{kf} S^{-D_s}.
$$
Here $F_s$ is the rank factor in the primitive mass note, including the common $\Gamma$. For $2\le s\le k-2$ it uses exactly the source genus ratio. For $s=k-1$ the constant $M_1/(M_k/M_{k-1})\le1$ eventually. The [low-rank bound and adjacent mass formula](SPECTRAL_PAIRED_GENUS.md) bound its $f$-th root by $2(80 f v^2)^{16}(2v)^{1/2}(\pi/v)^k/(k-1)!$, which tends uniformly to zero for $f\le k,v\ge1$. At $s=k$ the constant is one. Both are bounded by the original end-rank upper bound evaluated at the constant part of the label height. Hence the existing numerical bounds $F_s\le k^{skf/8}$ at $s\ge3$, and $F_2\le k^{-(1-o(1))kf}$, still apply. With $2R'\le6$, (2) gives the first assertion. Its explicit corank range follows from $g/2\ge k^7 b^8$, $A\le b^{2C_hm^2+2}$ and $7(s-2)\ge s/8+1$ for $s\ge3$.

On the set (3), the factor apart from $2R'$ is bounded by $k^{\theta kf}$ as in the primitive mass argument. The fixed factor six costs $o(kf\log k)$ in the logarithm. At $s=2$ the exponent is $-(1-\theta-o(1))kf\log k$. For $s\ge3$ it is at most $(-7(s-2)+s/8+\theta+o(1))kf\log k$. Summing the covered terms gives the claimed allowance. The ordinary real estimate is an analytic input throughout this corank reduction. Formula (1) proves the indicated product bounds independently of it.

## A finite test for the remaining labels at corank two

At corank two put $v=\mathrm{rd}(E)/2$. In the proof of (3) of the [primitive mass calculation](SPECTRAL_HIGHER_CORANK_MASSES.md), keep the power $v^{(34-k)f}$. Indeed the two factorials there are $(k-2)!(k-1)!$, the exponent of $\pi/v$ is $2k-1$ per embedding, the rank-two mass costs at most $(80fv^2)^{16f}$, and $\rho=2v$. Multiplying by $(kv)^{kf}$ gives precisely the stated residual power of $v$ in the upper bound. The other rank-two factors have logarithm $O(kf)$ in the original eventual range. Thus
$$
 F_2\le \exp(O(kf))\,k^{-kf} v^{(34-k)f}.
$$
The implicit constant is independent of the represented labels and of $v$ in that range. The angular allowance in the primitive mass calculation therefore gains the reciprocal of this discriminant factor.

One can test a subset of the resulting range using finite ideals alone. Let
$$
 \beta_Z=\frac{TT'p_r\overline{p_r}}{p_n\overline{p_n}}\in F,
 \qquad \mathfrak u_Z=\{a\in\mathcal O_F:a\beta_Z\in\mathcal O_F\}.
$$
The terminal minor is nonzero on the represented nonsingular support. Every conjugate of $\beta_Z$ belongs to $[0,1)$ by positivity of the Gram determinant. The denominator ideal of $1-\beta_Z$ is also $\mathfrak u_Z$, since for integral $a$ the difference between $a\beta_Z$ and $-a(1-\beta_Z)$ is integral. Put $\mathfrak w_Z=(1-\beta_Z)\mathfrak u_Z$, a nonzero integral ideal, and $H_Z=\mathrm N\mathfrak u_Z/\mathrm N\mathfrak w_Z=1/\mathrm N_{F/\mathbf Q}(1-\beta_Z)$. The [word-prime hypotheses](https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Formalism/SharpRestriction/CuspSpanNormBounds/NormalizedLocalScale.lean#L167-L170) make $T,T'$ positive rational integer primes. Positivity at every real embedding then gives the two-sided estimate, valid at every corank,
$$
  H_Z\ \le\ K(Z)^2=\prod_\tau\frac{(1+\sqrt{\tau\beta_Z})^2}{1-\tau\beta_Z}
       \le 4^f H_Z\le4^f\,\mathrm N\mathfrak u_Z.
$$
For $p_r=0$, one can use $K(Z)=1$ exactly. In general the denominator ideal is calculated from the two principal ideals by dividing $(p_n\overline{p_n})$ by its ideal gcd with $(TT'p_r\overline{p_r})$. In particular common factors in the minors need no separate size allowance.

On the subset of corank-two pairs for which
$$
   2R'\left[
       \frac{4^f\sqrt{H_Z H_{Z'}}}
            {T^f}\right]^k S^{-(D_2+k)}
     \ \le\ v^{(k-34)f} k^{\theta kf},\qquad 0\le\theta<\tfrac12,
$$
the ordinary orbital estimate alone bounds the total by $d\exp(-(1-\theta-o(1))kf\log k)$. To see the exponent on $S$, use the moment calculation above *before* spending the $S^k$ in (4). The new finite-ideal bound uses no power of $S$, leaving $D_2+k$ spare and the full label-packing power $12n^2$. A sufficient test involving only the two ideal ratios as label data results on replacing $S^{-(D_2+k)}$ by one, since $S\ge1$. The exact angular test replaces the bracket by $T^{-f}K(Z)K(Z')$. For $k>34$ the discriminant gain also applies to (3) at $s=2$ by multiplying its right-hand side by $v^{(k-34)f}$, with the bounded dimension factor treated as in its proof.

Thus any pair still requiring the angular estimate at corank two must satisfy the strict reverse of the displayed finite test. At any other corank the same norm ratio bounds the angle within a factor $4^f$ on a pair, before raising it to the $k$-th power. In particular one can use $4^f\sqrt{H_ZH_{Z'}}/T^f$ as an upper bound in the ordinary rank summation with its full reserve $D_s+k$.

[dict]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Formalism/SharpRestriction/CuspSpanNormBounds/BruhatCellsKronecker/FamilyPacketOfEquivalentStatement.lean#L582-L645
[ends]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AbelianVarietyTheory/Proofs/FlagMeasures/CellPointBlockEndsLeadingMinors.lean#L91-L155
[factors]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Formalism/SharpRestriction/CuspSpanNormBounds/NormalizedLocalScale.lean#L25-L38
[products]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Formalism/SharpRestriction/CuspSpanNormBounds/CongruenceAtSplitFrobeniusHolds.lean#L434-L478
[ordinary]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Formalism/SharpRestriction/CuspSpanNormBounds/CayleyDegreeNondegeneracy/RowsND.lean#L132-L149
[moment]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Formalism/SharpRestriction/CuspSpanNormBounds/CayleyDegreeNondegeneracy/RowsNDF.lean#L270-L310
[xi]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Formalism/SharpRestriction/CuspSpanNormBounds/CayleyDegreeNondegeneracy/RowsND.lean#L234-L246
