# The overlap of two different period maps

Fix a point of the completed construction and two distinct binary words $u,v$. Its $k-2$ bits select interior weight parameters. The associated chain has $m$ theta lifts, with $m$ fixed for all these words. Write $A_u:V_u\to Z$ and $A_v:V_v\to Z$ for the normalized period maps on their full complex columns, $f_u,f_v$ for the column dimensions and $D^\star$ for the dimension main term of the common row. In an integer dimension $D$, two independently and uniformly rotated isometric columns have expected squared overlap $f_u f_v/D$, by averaging either orthogonal projector. The arithmetic proof gives a deterministic upper bound of this size with the comparison dimension $D^\star$. For the actual completed hosts it yields
$$
 \|A_u^* A_v\|_{\rm HS}^2
 \le \{1+(1+o(1))\sigma_g\}\frac{f_uf_v}{D^\star},
 \qquad \sigma_g=f\left(g_0^{-1}+g_1^{-1}\right).
$$
Here $f$ is the degree of the totally real host field, and $g_0,g_1$ are its two distinguished split level primes. The asymptotic is uniform in points and pairs once the target, the admissible $\varepsilon>0$ and the family constants are fixed. The source endpoint requires the upper factor $1+b^{-6}$ with $b=\exp(x^\varepsilon)$. [Full Gram theorem on the selected families](../spectral/SPECTRAL_FULL_GRAM_ON_MATCHED_FAMILIES.md) · [Original statement and the full-column hypotheses][mixed4-frame]

## The scalar term and its coefficient

The mixed operator pairs two Poincaré series, each divided by the square root of its unfolding constant. Their absolute majorants are square integrable, so Cauchy–Schwarz makes their product integrable. Unfolding groups the terms by rational double cosets for the two stabilizers. The part with zero Gram invariant vanishes for distinct words. At a separating place the relevant intertwiners are between inequivalent compact types, and the identity cell also has zero local pairing. Squaring the norm of the remaining sum groups pairs of terms with the same lattice row and level label. In a single such term two flags of $r+1$ vectors have nonsingular joint Gram matrix, where $r=m/2-1$ and $m$ is the length of the chain. Their joint span has dimension $2r+2$ in a Hermitian space of dimension $k+2r+1$. Its perpendicular has dimension $k-1$. The dimension of the subspace where a pair's flag identifications agree can therefore be at most $k-1$, giving pair corank at least one. [Unfolding and classification][mixed4-unfold] · [Jin's paired subspace and scalar conditions][mixed4-pairs]

At generic corank one the scalar partners are the pairs whose identifications agree also in the last marked coordinate in the sense of the two flag quotient tests. These pairs contribute the principal term. Their summands carry phases, so the relevant quantity is a squared norm of a sum over partners. Jin and the Roadmap control it by interpolation at an interior bit where $u$ and $v$ differ. The separation of the weight choices there gives a common interval on which to recover the leading coefficients of the differential operators. Applying this at successive flag blocks suppresses nonzero frequencies of the arithmetic sampling lattice. The zero Fourier coefficient at a singleton is the preceding energy with coefficient one. Retaining this coefficient is necessary when the number of layers grows. [Separating weight and frequency scale][mixed4-gap] · [Interpolation, signed words and exact initial energy](../spectral/SPECTRAL_LEVEL_ZERO_AND_CUTOFFS.md) · [Lattice summation and its hypotheses](../spectral/SPECTRAL_THREE_LETTER_SCALAR_SAMPLING.md)

Here is the numerical argument in the original five-insertion version. After dividing by the initial energy and the product of the square roots of the finite density bounds, let $R_i$ bound the square root of the energy through $i$ flag steps, with $R_0=1$. The positive-kernel bounds for singleton frequencies and for the longer last blocks give
$$
 R_i\le (1+h)R_{i-1}+\sum_{j=2}^i h^{j-1}R_{i-j},
 \qquad h=(C/\Theta)^f,\quad \Theta\ge k^{1/16}.
$$
To see how the principal coefficient survives, set $B=1+2h$ and induct from zero. The right side divided by $B^{i-1}$ is at most $1+h+\sum_{j\ge2}(h/B)^{j-1}=1+h+h/(1+h)\le B$. Thus $R_i\le(1+2h)^i$. The final squared allowance above one satisfies $\delta_s\le\exp(4(r+1)h)-1$. The compact cutoffs in this calculation are removed first on one finite collection of flag prefixes, where all initial energies have the stated limits. Absolute convergence then permits exhaustion by finite collections. The continuous initial energy, converted back to column measures using formal-degree orthogonality, contributes at most $f_uf_v/D^\star$. Thus each lift multiplies the principal term by a factor tending to one sufficiently rapidly for their product to have the same property. [Original energy recursion and cutoff limit][mixed4-rec] · [Row masses and formal degree][mixed4-mass] · [Positive block bounds and the cutoff limit](../spectral/FLAG_BLOCK_ENERGY_AND_CUTOFF.md)

Write $\Delta=f_uf_v/D^\star$, $t_0=m^5 f\log b$ and $E=\exp(-kf\log k/3)$. The scalar contribution divided by $\Delta$ is at most $A=(1+\delta_s)e_1$, where $1\le e_1\le\exp(12 f2^{-(k-m)})$ bounds the product of the finite representation-density ratios. The generic nonscalar pairs and the pairs of corank at least two have absolute counting estimates. Each of the two errors entering the generic sum is at most $E\Delta$, and the higher-corank error in the nongeneric sum obeys the same bound. Nongeneric corank-one pairs have a local defect. A proper residue image saves its index; in the full-image case the signed character sum gives the saving. Combining the defective place with the orbital-volume cost leaves $N\Delta$, where $N=2^{-(k-2r-5)}\exp(C_4t_0)$. The finite Gram matrix contracts the row vectors with normalized squared operator bound $P$. Applying the triangle inequality to the generic and nongeneric vectors **after** taking their respective norms gives
$$
 \frac{\|A_u^*A_v\|_{\rm HS}^2}{\Delta}
 \le P\bigl(\sqrt{A+2E}+\sqrt{N+E}\bigr)^2 .
$$
For an equal word the identity contributes $I$, the nonidentity zero-Gram part can survive, and there is no separating bit for the scalar estimate. Its diagonal estimate is used separately. [Jin's defective-place and absolute estimates][mixed4-defect] · [Assembly and distinction between equal and unequal words][mixed4-assembly]

## The cost at the two finite levels

The finite operator supplies an elementary reason its factor $P$ is so close to one. At a distinguished place put $q=g_i$, $G=\operatorname{GL}_k(\mathbb F_q)$, and let $U$ be the upper unitriangular subgroup. Its character $\xi$ is nontrivial on every simple upper root subgroup. On a free level orbit the finite kernel is convolution by the character of $\operatorname{Ind}_U^G\xi$, normalized by its value at the identity. By character orthogonality and Frobenius reciprocity the eigenvalue on a type $\pi$ is
$$
 \frac{|U|}{\dim\pi}\dim\operatorname{Hom}_U(\xi,\pi).
$$
Finite Whittaker multiplicity one makes the last factor zero or one. If it is one, restrict to the abelian last-column subgroup $\mathbb F_q^{k-1}$. It has a nonzero character on the given Whittaker vector. The group $\operatorname{GL}_{k-1}$ acts transitively on its $q^{k-1}-1$ nonzero characters, so all corresponding eigenspaces have the same dimension. In the eigenspace of the specified character, its stabilizer contains the rank-$(k-1)$ mirabolic subgroup, and the original vector retains a Whittaker character on its upper unitriangular group. Repeating the last-column argument inside the successive mirabolic subgroups gives $\dim\pi\ge\prod_{j=1}^{k-1}(q^j-1)$. Since $|U|=q^{k(k-1)/2}$, the local eigenvalue is at most $\prod_{j=1}^{k-1}(1-q^{-j})^{-1}$. Tensoring over the $f$ places at each of the two split primes gives the admissible squared bound
$$
 P=\prod_{i=0}^1\prod_{j=1}^{k-1}(1-g_i^{-j})^{-f}.
$$
For $q\ge3$ and $k\ge2$, the logarithm of the single-place product is $q^{-1}+O(q^{-2})$ uniformly in $k$. Indeed the $j=1$ factor gives that expansion and $\sum_{j\ge2}-\log(1-q^{-j})\ll q^{-2}$. Thus $P=1+(1+o(1))\sigma_g$ as soon as $g_i\to\infty$ and $\sigma_g\to0$. [Finite convolution, multiplicity and dimension bound][mixed4-finite]

At any completed host of this construction the size estimates are
$$
 f\asymp x^{2+8\varepsilon},\quad
 m\asymp x^{1/2-\varepsilon/16},\quad
 k\asymp x^{9/2+10\varepsilon},\quad
 (kb)^8\le g_i\le b^{C_g}.
$$
In particular $t_0/k=O(x^{-21\varepsilon/16})$, while $m=o(k)$. This gives $N\le e^{-c k}$ for some fixed $c>0$. The same upper bound holds for $E$ and $\log e_1$ beyond a common cutoff. Also $h\le e^{-(f/32)\log k}$ once $k\ge C^{32}$, and $f\log k/\log b\to\infty$. Hence for every fixed $A_0>0$ all these errors, together with $\delta_s$, are $O_{A_0}(b^{-A_0})$. To absorb a square root use the estimates with $2A_0$. The two-radical expression above is consequently at most $P(1+O_{A_0}(b^{-A_0}))$. The constants in the orbital and interpolation estimates are fixed by the family hypotheses before the word pair is chosen. Since $\sigma_g\ge f b^{-C_g}$, taking $A_0>C_g$ proves the claimed result with its actual finite levels. Since $\sigma_g\le2f/(k^8b^8)$, one may in particular use $1+b^{-8}$ on these hosts. This refines the excess in the mixed norm estimate. The leading dimension factor and the analytic conclusion concern the original period maps. [Completed ranks][mixed4-ranks] · [Level and size hypotheses][mixed4-levels] · [Quantifiers on the selected family](../spectral/SPECTRAL_FULL_GRAM_ON_MATCHED_FAMILIES.md#the-order-of-the-constants)

[mixed4-frame]: https://github.com/rh-lean-roadmap/rh-lean-roadmap/blob/c7755c1086f05d0918ee8496d95912e4f35e22f9/docs/src/book/main.tex#L10650-L10674
[mixed4-unfold]: https://github.com/rh-lean-roadmap/rh-lean-roadmap/blob/c7755c1086f05d0918ee8496d95912e4f35e22f9/docs/src/book/main.tex#L46701-L46727
[mixed4-pairs]: https://github.com/yuiyuiui/Natural-Language-Proof-Generalized-Riemann-Hypothesis/blob/405237610e58ab9d4a9d5d54d9a0548a0c44227c/sections/integral-division.tex#L3493-L3529
[mixed4-gap]: https://github.com/rh-lean-roadmap/rh-lean-roadmap/blob/c7755c1086f05d0918ee8496d95912e4f35e22f9/docs/src/book/main.tex#L46246-L46292
[mixed4-rec]: https://github.com/rh-lean-roadmap/rh-lean-roadmap/blob/c7755c1086f05d0918ee8496d95912e4f35e22f9/docs/src/book/main.tex#L46595-L46635
[mixed4-mass]: https://github.com/rh-lean-roadmap/rh-lean-roadmap/blob/c7755c1086f05d0918ee8496d95912e4f35e22f9/docs/src/book/main.tex#L46639-L46661
[mixed4-defect]: https://github.com/yuiyuiui/Natural-Language-Proof-Generalized-Riemann-Hypothesis/blob/405237610e58ab9d4a9d5d54d9a0548a0c44227c/sections/integral-division.tex#L3622-L3648
[mixed4-assembly]: https://github.com/yuiyuiui/Natural-Language-Proof-Generalized-Riemann-Hypothesis/blob/405237610e58ab9d4a9d5d54d9a0548a0c44227c/sections/integral-division.tex#L4193-L4224
[mixed4-finite]: https://github.com/rh-lean-roadmap/rh-lean-roadmap/blob/c7755c1086f05d0918ee8496d95912e4f35e22f9/docs/src/book/main.tex#L46667-L46696
[mixed4-ranks]: https://github.com/rh-lean-roadmap/rh-lean-roadmap/blob/c7755c1086f05d0918ee8496d95912e4f35e22f9/docs/src/book/main.tex#L3144-L3158
[mixed4-levels]: https://github.com/rh-lean-roadmap/rh-lean-roadmap/blob/c7755c1086f05d0918ee8496d95912e4f35e22f9/docs/src/book/main.tex#L15528-L15556
