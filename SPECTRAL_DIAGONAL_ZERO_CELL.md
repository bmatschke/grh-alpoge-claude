# The nonidentity zero-Gram cell for one word

Fix a word $u$ in the full, unrestricted column of the selected spectral model. Write $d_u$ for its dimension and $Z_u$ for the sum of its orbital operators with zero Gram determinant outside the identity cell. On the tied model in the counting range, Roadmap B8.08q gives
$$
                     \|Z_u\|_{\rm HS}^2\le d_u e^{-kf\log k}.
$$
Here $k$ is the initial rank and $f=[F:\mathbb Q]$. This is the original word-space normalization. Below we derive the estimate from the fixed-minor orbital bound, using a direct count in fractional-ideal coordinates. The count removes the root-discriminant factor from the summation over minor labels. The fixed-minor estimate still uses arithmetic and archimedean inputs. [Pointwise spectral assertion][goal] · [Roadmap's uniform statement][uniform] · [Four cells in the selected expansion](actual_gram/actual_gram_section.tex#L12-L46)

## Why every contributing term has positive rank

Let $X,X'$ be the isotropic flag spaces of dimension $r=(m-2)/2$, with final vectors $z,z'$ of norm $-T_u$. A term contributes only if the infinitesimal unipotent characters agree on the common radical. Otherwise their quotient has a nontrivial character on the real intersection. Translation on the compact unipotent lattice quotient preserves its integral and multiplies it by a scalar different from one, so its orbital vector vanishes. For a relevant zero-Gram term the [normal form](SPECTRAL_GRAM_CELLS.md#why-unequal-words-have-no-zero-gram-term) gives $j=r-\dim(X\cap X')$, a nonzero leading pairing minor of order $j$ when $j>0$, and $z'-cz\in X+X'$ with $c\bar c=1$. [Character cancellation][vanish] · [Flag normal form][nf]

Suppose $j=0$. The two flags agree at every step. With indexing from zero, their framed vectors satisfy $e'_a-ce_a\in X_a$ and $z'-cz\in X$. The two primitive final vectors in the quotient lattice give $c\in\mathcal O_E^\times$. Its powers belong to the compact set on which all conjugates have modulus one, hence form a finite set in the embedded lattice $\mathcal O_E$. Thus $c$ has finite order. At each of the two marked primes the framed-level congruence gives $T_u(c-1)\equiv0$. Both primes are coprime to $T_u$. A finite-order unit reducing to one at residue characteristic $p$ has $p$-power order: raise it to its $p$-primary exponent, and let $a$ be the remaining order, prime to $p$. If $a>1$, the geometric sum of its first $a$ powers would be zero and would reduce to the nonzero element $a$. Applying this at the two distinct residue characteristics gives $c=1$. [Primitive lines and the two congruences][rankzero] · [Original equal-flag argument][idnative]

The integral identification here matters. The map $U:e_a\mapsto e'_a$ is unitriangular and preserves $X\cap\Lambda$ in the original row lattice $\Lambda$, as the two adapted frames have the same graded ideals. The saturated summand $X\cap\Lambda$ admits an integral retraction $P_0$ because the torsion-free quotient is projective. Unimodularity makes $P_0^*$ integral. Take $\theta\in\mathcal O_E$ with $\theta+\bar\theta=1$ using trace surjectivity of the finite-unramified CM extension. Set $P=P_0-\theta P_0P_0^*$. Isotropy gives $P_0^*P_0=0$, whence $P|_X=1$ and $PP^*=0$. For $A=(U-1)P$ we obtain $AA^*=A^*A=0$ and $A^{r+1}=0$. Thus $(1+A)(1+A^*)^{-1}$ is an integral isometry by multiplication, with a finite geometric sum for the inverse. It restricts to $U$ on $X$, and changes $z$ by an element of $X$. These are the framed identity-cell conditions. Consequently every relevant nonidentity term has $1\le j\le r$. For $r=0$ the whole remainder is zero. [Integral isometry in the source][rankzero] · [Positive rank for the exact term set][idnative]

## Summing all minor labels without a discriminant loss

Write $\rho=|\operatorname{disc} E|^{1/(2f)}$, $\mathfrak d=\mathfrak D_{F/\mathbb Q}\mathcal O_E$, and $q_l=\sum_{a=1}^l(r+1-a)$. The label of a rank-$j$ term is determined by its first $j$ leading minors $\delta_l$; some can vanish and $\delta_j\ne0$. The arithmetic normalization gives $\delta_l\in\mathfrak d^{2q_l}$. In the finite-unramified case $N_E\mathfrak d=|\operatorname{disc} F|^2=\rho^{2f}$. Thus in the scaled lattice
$$
 \mathcal L_l=\{(\rho^{-2q_l}\tau x)_{\tau}:x\in\mathfrak d^{2q_l}\}
                         \subset\mathbb C^f,
$$
any two distinct points differ by a vector $v$ with $\prod_\tau |v_\tau|^2\ge1$. Indeed the absolute norm of any nonzero element of the ideal is at least its ideal norm. This works for a nonprincipal ideal and requires no choice of generator. [Exact minor normalization][fixed] · [Integral ideal attached to a nonzero minor][ideal]

Put $R=(2b^{C_Hm})^{2r}\ge1$. Represent the tuple of minors by $x_l\in\mathcal L_l$. Define
$$
  s_\tau=\max(1,\max_{l\le j}|x_{l,\tau}|/R),\qquad
  S_\delta=\prod_\tau s_\tau,\qquad
  D_\delta=N_E((\delta_j)\mathfrak d^{-2q_j}).
$$
Then $D_\delta=\prod_\tau|x_{j,\tau}|^2\le R^{2f}S_\delta^2$. For any $h>2j$ there is also the uniform estimate
$$
 \sum_{\delta\text{ of rank }j} S_\delta^{-h}
       \le (5R)^{2fj}(1-2^{-(h-2j)})^{-f}.                   \tag{1}
$$

To prove (1), put $2^{a_\tau}\le s_\tau<2^{a_\tau+1}$. In each $\mathcal L_l$, open polydiscs of radius $1/2$ about different points are disjoint by the product-distance inequality. For the indicated shell all centres have coordinate modulus at most $2^{a_\tau+1}R$. Comparing volumes therefore bounds their number in that lattice by $\prod_\tau(2^{a_\tau+2}R+1)^2$. Multiply these bounds over $l\le j$ to count possible tuples, including zeros. The result is at most $(5R)^{2fj}2^{2j\sum a_\tau}$. On that shell the weight is at most $2^{-h\sum a_\tau}$. Summing the $f$ geometric series proves (1). The norm scaling is what removes the factor involving $\rho^{2q_l}$ that arises from counting all coordinates in $\mathcal O_E$. [Comparison with Roadmap's unscaled packing proof][packing]

## From the fixed-type estimate to the operator

For each ordered pair of types on one word, B8.02b bounds the sum of $\|v_t\|\|v_{t'}\|$ over any finite subset of pairs with the **same complete row** by $n_\pi\mu_u B_{j,\delta}B_{j',\delta'}$. Here the row label includes both lattice representatives and the finite-type index, $n_\pi$ is the archimedean coefficient dimension, and $\mu_u$ is the sum of the reciprocal stabilizer orders. Taking $C_s=C_p+4$ in that result gives, for $H(a)=b^{a m^2f}$,
$$
 B_{j,\delta}=(C/k)^{j(k-1-j)f}
      H(C)^{Cr^4}H(C_h)^{C_hr^4}
      D_\delta^{(j+1)/2}S_\delta^{-4k}.
$$
The exponent of $D_\delta$ is positive. The orbital amplitude contributes $-(k-1-j)/2$ and the number of terms contributes $k/2$. Bounding $D_\delta$ as above leaves the power $S_\delta^{-(4k-j-1)}$. Because $k\ge2r+5$, (1) applies with $h=4k-j-1$ and its last factor is at most $2^f$. The remaining extra factors are $R^{f(j+1)}(5R)^{2fj}2^f$. With $L=\log b>1$, $j\le r\le m$ and $\log R=2r(\log2+C_HmL)$, there is a constant $K\ge1$, depending only on the fixed constants, for which
$$
             \sum_\delta B_{j,\delta}
      \le e^{K m^6fL}(C/k)^{j(k-1-j)f}.                    \tag{2}
$$
These bounds apply to arbitrary finite subsets, so they control the corresponding nonnegative sums. [Fixed-type estimate and its two factors][fixed] · [Native amplitude and pair-count inputs][factor]

Let $B=kf\log k$. Choose the threshold in $C_\ell$ so that $C_\ell m^6L\le k\log k$ gives $Km^6 fL\le B/16$, $k\ge16$ and $\log C\le(\log k)/8$. This is possible since $m^6L\ge1$ and $k\log k$ is increasing for $k\ge1$. For $1\le j\le r$, $j(k-1-j)\ge k-2\ge7k/8$. Thus (2) is at most $e^{-45B/64}$ for each $j$. Summing the fixed-type bound over both ranks and labels bounds the same-row pair sum by $n_\pi\mu_u r^2 e^{-90B/64}$.

The finite Gram operator has norm at most $P_g\Gamma_1$, with $P_g=(1+3/g_0)^f(1+3/g_1)^f\le2$ since $g_i\ge(kb)^8$ and $f\le k$. Also $\Gamma_1 n_\pi\mu_u\le d_u$. Indeed $\Gamma_1$ counts marked finite cosets above a lattice before its stabilizer acts. Each fibre has at most the stabilizer order, and neatness gives one copy of the coefficient space per resulting class. Summing the resulting inequality over the lattice representatives gives the claimed normalization. Apply the finite Gram bound to sums of orbital vectors grouped by their finite indices. Different lattice-pair labels within a finite index are orthogonal, so the result is bounded by $P_g\Gamma_1$ times the same-row pair sum just estimated. The full tied expansion gives absolute convergence for passage from finite sums. Finally $\log(2r^2)\le3\log k\le3B/16$. This proves $\|Z_u\|_{\rm HS}^2\le d_u e^{-B}$. [Finite Gram bound](SPECTRAL_GRAM_CELLS.md#the-finite-gram-matrix-at-the-two-marked-primes) · [Mass and dimension][mass] · [Selected kernel and absolute convergence](period_range_v59/main.tex#L638-L668) · [Native assembly][assemble]

## Application and remaining inputs

On an admitted family use the original parameters $C_g=C_{YL}+1$, $c_b=1/4$, $C_w=3$, $c_T=1/2$, $C_T=C_{Tu}$ and $C_0=3$. The hypotheses are the original ties, the concrete spectral comparison and the counting range $\mathrm{KTwoHypotheses}$. This last condition includes the all-word size comparison that guards the spectral endpoint, the split level primes, weight gaps and the finite-unramified CM field. The source obtains the standing family range from $8C_\Gamma\le C_{k,\mathrm{low}}$, the level window $\mathrm{TuSize}$ and the arithmetic residual event. Complete splitting at the marked and level primes and the square-discriminant identity hold on the family. The relative discriminant formula gives finite unramifiedness from the square-discriminant identity. In the standing range $C_\ell\le m$, $f\ge m^4$, and $m^5fL\le k$ give $C_\ell m^6L\le m^7L\le k\log k$. The adjacent parameter gaps imply the weaker gaps for every distinct pair. The selected row supplies the base mass for the level window; its upper constant is required to be above the original ordered threshold. A late index with the guarded size comparison and these thresholds therefore uses its own word, coefficient module and measures in the estimate. The size bounds give $k\ge3x$, $f\ge1$ and $\varepsilon<1/52$, so eventually $e^{-kf\log k/2}\le e^{-x^{\varepsilon/8}}$ with one cutoff for all words and indices. This verifies the square-root error rate for the singular part of the diagonal kernel. [Exact native guards and output][k2] · [Family standing range][family] · [From standing to the same-word hypotheses][range] · [Splitting and discriminant][split] · [Selected level window](degree_prime_size/main.tex#L426-L510) · [Concrete selection](frame_v61/main.tex#L111-L162) · [Rank bounds](degree_prime_size/main.tex#L158-L188)

The [single-datum frame estimate](SPECTRAL_FRAME_FIBRE.md) now supplies the weighted count of inequivalent frames at a fixed minor label over a specified embedded lattice and congruence graph. For the two frames on a common row, the remaining arithmetic input is the separately normalized genus mean over pairs of these data and their level-compatible isometry. Its positive index powers cancel the inverse index powers in the two individual counts. The fixed-type bound also requires the local Bessel amplitudes. On these inputs the earlier rank exclusion, label summation, normalization and final rate apply. Writing $X_u$ for the sum of both nonzero-Gram cells, the triangle inequality now gives $\|K_{uu}-I\|_{\rm HS}/\sqrt{d_u}\le\|X_u\|_{\rm HS}/\sqrt{d_u}+e^{-kf\log k/2}$ when $d_u>0$. With $k\ge3x$, the last summand is eventually at most half the allowed $e^{-x^{\varepsilon/8}}$, uniformly in the word. The remaining diagonal estimate concerns $X_u$; the distinct-word bound is also needed for the full spectral obligation. [Native fixed-type producer][producer] · [Roadmap's outline register][outline] · [The full endpoint][goal]

[goal]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Formalism/SharpRestriction/GlobalTheoremInputs.lean#L142-L156
[uniform]: https://github.com/rh-lean-roadmap/rh-lean-roadmap/blob/94e6a98b4e74932a0298d6bd22d44cf60c62764b/docs/src/book/main.tex#L16852-L16869
[vanish]: https://github.com/rh-lean-roadmap/rh-lean-roadmap/blob/94e6a98b4e74932a0298d6bd22d44cf60c62764b/docs/src/book/main.tex#L43871-L43897
[nf]: https://github.com/rh-lean-roadmap/rh-lean-roadmap/blob/94e6a98b4e74932a0298d6bd22d44cf60c62764b/docs/src/book/main.tex#L41439-L41456
[rankzero]: https://github.com/rh-lean-roadmap/rh-lean-roadmap/blob/94e6a98b4e74932a0298d6bd22d44cf60c62764b/docs/src/book/main.tex#L41457-L41466
[idnative]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Formalism/LocalToGlobal/SiegelLatticeTheory/CokernelGLCounts/RankPointCounts/IsIdentityOfEqualFlags.lean#L45-L86
[fixed]: https://github.com/rh-lean-roadmap/rh-lean-roadmap/blob/94e6a98b4e74932a0298d6bd22d44cf60c62764b/docs/src/book/main.tex#L15740-L15771
[ideal]: https://github.com/rh-lean-roadmap/rh-lean-roadmap/blob/94e6a98b4e74932a0298d6bd22d44cf60c62764b/docs/src/book/main.tex#L15717-L15738
[packing]: https://github.com/rh-lean-roadmap/rh-lean-roadmap/blob/94e6a98b4e74932a0298d6bd22d44cf60c62764b/docs/src/book/main.tex#L43985-L44061
[factor]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AbelianVarietyTheory/Proofs/FlagMeasures/TypePOfLargeGapDiscreteSeriesBessel.lean#L15-L24
[mass]: https://github.com/rh-lean-roadmap/rh-lean-roadmap/blob/94e6a98b4e74932a0298d6bd22d44cf60c62764b/docs/src/book/main.tex#L43836-L43869
[assemble]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Formalism/LocalToGlobal/SiegelLatticeTheory/FlagStabilizerTensors/RowsPos.lean#L186-L208
[k2]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Formalism/SharpRestriction/CuspSpanNormBounds/NonGenericAndKTwoTheorems.lean#L36-L61
[family]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Formalism/SharpRestriction/CuspSpanNormBounds/StandingHypothesesHoldFamily.lean#L1602-L1629
[split]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Formalism/LocalToGlobal/SiegelLatticeTheory/ResidEvFree.lean#L82-L98
[producer]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AbelianVarietyTheory/Proofs/FlagMeasures/RowsPosTypeP.lean#L1-L10
[outline]: https://github.com/rh-lean-roadmap/rh-lean-roadmap/blob/94e6a98b4e74932a0298d6bd22d44cf60c62764b/docs/outline-proofs.md#L3-L10
[range]: https://github.com/rh-lean-roadmap/rh-lean-roadmap/blob/94e6a98b4e74932a0298d6bd22d44cf60c62764b/docs/src/book/main.tex#L41228-L41237
