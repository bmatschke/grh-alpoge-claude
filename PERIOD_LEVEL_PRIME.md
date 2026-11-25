# Integral elliptic theta moments at a word's level prime

Let $p=T_u$ be the level prime of a selected word. On the eventual range, $p\ge5$ splits in the imaginary quadratic field $K_d$ and is prime to the discriminant and the curve ideal. The first input of Roadmap B4.22c asks for integral binomial moments in a particular ordinary coordinate. It follows from Bannai and Kobayashi, including all the required ideal curves, directions and prime-to-$p$ translates. For the subsequent matrix kernels a separate calculation gives the local exponent, conditional on the one-step comparisons on the chosen column. [Elliptic hypothesis][matrix] · [Level-prime period statement][level]

The [matrix and terminal calculation](PERIOD_LEVEL_PRIME_MATRIX.md) now applies this elliptic estimate to the prescribed normalized section on a constructed good column. It makes the two finite Fourier counts explicit, transfers the bound to the actual rational class-sum pairing and accounts for rounding the word-prime shift.

## The half-period and the ordinary coordinate

Write $\Lambda=\delta\mathfrak c$ for the ideal lattice scaled to have Weierstrass discriminant one. The normalized even theta section on $\mathbb C/\Lambda$ has its simple zero at a nonzero half-period $P$ and takes value one at zero. Write $\vartheta$ for the reduced theta with simple zero at zero and derivative one. For the Hermitian form $H$ of the principal polarization use the reduced translation
$$
 U_t F(z)=F(z+t)\exp(-\pi H(z,t)-\pi H(t,t)/2).
$$
For $h$ representing $-P$, translation changes the semicharacter by the character of the half-period and changes the divisor to $[P]$. This is the factor of automorphy of the prescribed even section, by the reduced theta transformation law. The ratio of the two sections is then a nowhere-vanishing function on the elliptic curve and hence constant. Thus the required section is $U_h\vartheta/(U_h\vartheta)(0)$. [Reduced translations, §1.3][translate] · [Exact normalized half-period formula][half] · [Normalization on the actual ideal curve][ideal]

The model is good at $p$. Indeed $j=1728g_2^3$ is a CM algebraic integer, $g_2^3-27g_3^2=1$, and $2,3$ are units at $p$. The split CM action gives ordinary reduction. In the parameter $t_E=-2x/y$, Bannai–Kobayashi, Corollary 2.16(i), gives the formal expansion of $U_b\vartheta$ for every prime-to-$p$ torsion point $b$. It is an integral unit series times $t_E^{\mathbf 1_{b=0}}$, with the point read modulo the period lattice. In particular $(U_h\vartheta)(0)$ is a unit. Moreover $U_tU_h\vartheta$ differs from $U_{t+h}\vartheta$ by a root of unity for prime-to-$p$ torsion $t$. This follows by multiplying the translation factors and using that the alternating form is integral on periods and rational on torsion lifts. The normalized even section and all the specified translates therefore have integral expansions. This includes the translate whose value at the origin vanishes. [Corollary 2.16 and its proof][bk]

Let $h_c=N\mathfrak c$, let $\delta_0$ denote the discriminant root of the principal ideal, and fix the comparison $\jmath:\mathbb C\simeq\mathbb C_p$. In the principal ordinary chart the logarithm of the point with multiplicative coordinate $1+Z$ is $\Omega_0\log(1+Z)$. The isogeny from the principal curve to the ideal curve with multiplier $h_c\delta/\delta_0$ has degree $h_c$. Indeed $h_c\mathcal O_{K_d}\subseteq\mathfrak c$ has index $h_c$ in $\mathfrak c$. It extends to the good models and is an isomorphism on formal groups at $p$. For directions $v_j=\delta a_j$ with $a_j\in\mathfrak c$ substitute on the principal formal group
$$
 1+Z=\prod_{j=1}^r(1+Z_j)^{\jmath(a_j)/h_c}.
$$
Every exponent belongs to $\mathbb Z_p$ since the chosen completion of $K_d$ is $\mathbb Q_p$, and hence every binomial coefficient in the substitution is integral. Under the isogeny the logarithm becomes
$$
 \sum_{j=1}^r\omega\,\jmath(v_j)\log(1+Z_j),
 \qquad \omega=\Omega_0/\jmath(\delta_0).
$$
Thus a formal map of integral charts realizes exactly the requested scale, even when $\jmath(\delta/\delta_0)$ is a nonrational unit. After substitution, the coefficient of $Z^\nu$ is the iterated binomial derivative $A_\nu(U_t\theta_\Lambda;v_1,\ldots,v_r)$ of B4.22c. This follows by expanding the commuting translation operators $(1+Z_j)^{D_j}$ in powers of $Z_j$. All these coefficients are integral. [Isogeny and ordinary period][period] · [Definition of the derivatives][matrix]

Mahler interpolation gives one measure of norm at most one on $\mathbb Z_p^r$ with these binomial moments. On products of binomial polynomials send the basis element with index $\nu$ to $A_\nu$. Finite differences recover the coefficients and have norm at most one, so this functional is bounded for the supremum norm. The span is dense, by one-variable Mahler approximation on each factor applied to the indicators of residue boxes. Extension by continuity gives the measure, and the falling-factorial expansion of powers gives its ordinary power moments. This proves the elliptic input in B4.22c. To use the four-copy argument for a matrix theta section one still needs its specified lattice intertwiners, normalized translations and prime-to-$p$ averaging. With these comparisons, the multidegree $(\nu,\nu,\nu,\nu)$ of four independent copies gives $A_\nu^4$ and hence the original bound. [Mahler][mahler] · [Four-copy argument][four] · [Lattice moves and translations][moves]

## The local exponent after the lifts

Assume the pointwise split-level kernel and neighbor comparisons of B4.22b on the chosen column, including its rational jets and marked lattices. Let $S_i$ be the local lattice of forms at stage $i$, $K_i$ the lift to stage $i+1$, $C_0=1$ and $C_{i+1}=K_i C_i$. Let $U_i$ be the ordered product of the upward neighbor operators at the $r$ selected indices and let $s=(t+1)/2$ in the rank-increment notation of the source. Each reciprocal class stabilizer is a $p$-unit. Its finite group acts faithfully in rational dimension at most $2fN_m$, and an element of order $p$ would need a primitive eigenvalue of degree $p-1>2fN_m$. [Size of the level prime][size] · [Pointwise comparisons][point]

The neighbor identity passes to class sums by counting each incident orbit with weight the reciprocal of its pair stabilizer from either end. It gives $U_{i+1}K_i=p^{sr}K_iU_i$. At the coefficient places where the markings occur (the seen places), the local comparison gives $p^{d_i}U_{i+1}K_iS_i\subseteq S_{i+1}$ with common upper exponent $d_i=fN_m+2\sum_\tau W_{u,\tau}$. At a remaining marked index, scaling one basis direction by $p$ costs at most the first weight, since a column of a generating minor uses that row at most once. [One-step comparison on forms][step]

Commuting $U_{i+1}$ through $C_{i+1}$ gives a factor $p^{sr(i+1)}$. Induction with $B_0=0$ and $B_{i+1}=B_i+d_i+sr(i+1)$ gives
$$
 p^{B_m} C_mU_0^m S_0\subseteq S_m,\qquad
 B_m=\sum_{i=0}^{m-1}d_i+sr\,m(m+1)/2.
$$
The actual input is $p^{a_0}U_0^m z$, with $z\in S_0$ and $a_0$ equal to minus $m$ times the sum of the selected last initial weights. The sign condition gives $a_0\ge0$. On a seen place $r=n_T$, and the common exponent gives $B_m=mT^*_{u,w}$. The terminal column therefore belongs to $p^{a_0-mT^*_{u,w}}S_m$. On an unseen place the set of selected indices is empty, $a_0=0$, and the second point estimate gives $K_iS_i\subseteq p^{fs}S_{i+1}$. The resulting terminal column belongs to $p^{mfs}S_m$. This also holds for each used twisted tuple with $p\notin Q'(\mu)$ under the stated level-zero identifications. The bijection of decorated representatives preserves their marking kernels and upward sums, hence the same presentation of the input. [Induction][step] · [Twisted columns][twist]

At the level prime the terminal stabilizer loss is zero. Under the terminal evaluation of B4.19 these inclusions give lower valuations $e_w(a_0-mT^*_{u,w})$ and $e_wmfs$ for nonzero periods, respectively, with $v_w(p)=e_w$. Both imply the required lower bound $e_w S_{u,w}$ since $S_{u,w}=-mT^*_{u,w}$ and $T^*_{u,w}=0$ at the unseen places. To transfer this bound to the actual arithmetic functional on its shifted row lattice also requires its local unit comparison. The pointwise matrix identities, terminal evaluation and shifted row comparison remain hypotheses of this part of the argument. [Terminal evaluation][terminal] · [Height entry 1](continuation_v89/integral.tex#L65-L151)

[mahler]: https://doi.org/10.1515/crll.1958.199.23
[bk]: https://arxiv.org/pdf/math/0610163#page=29
[matrix]: https://github.com/rh-lean-roadmap/rh-lean-roadmap/blob/94e6a98b4e74932a0298d6bd22d44cf60c62764b/docs/src/book/main.tex#L7227-L7270
[period]: https://github.com/rh-lean-roadmap/rh-lean-roadmap/blob/94e6a98b4e74932a0298d6bd22d44cf60c62764b/docs/src/book/main.tex#L31049-L31061
[four]: https://github.com/rh-lean-roadmap/rh-lean-roadmap/blob/94e6a98b4e74932a0298d6bd22d44cf60c62764b/docs/src/book/main.tex#L30974-L30992
[moves]: https://github.com/rh-lean-roadmap/rh-lean-roadmap/blob/94e6a98b4e74932a0298d6bd22d44cf60c62764b/docs/src/book/main.tex#L7271-L7306
[size]: https://github.com/rh-lean-roadmap/rh-lean-roadmap/blob/94e6a98b4e74932a0298d6bd22d44cf60c62764b/docs/src/book/main.tex#L7046-L7077
[point]: https://github.com/rh-lean-roadmap/rh-lean-roadmap/blob/94e6a98b4e74932a0298d6bd22d44cf60c62764b/docs/src/book/main.tex#L7323-L7373
[step]: https://github.com/rh-lean-roadmap/rh-lean-roadmap/blob/94e6a98b4e74932a0298d6bd22d44cf60c62764b/docs/src/book/main.tex#L31326-L31349
[twist]: https://github.com/rh-lean-roadmap/rh-lean-roadmap/blob/94e6a98b4e74932a0298d6bd22d44cf60c62764b/docs/src/book/main.tex#L31349-L31357
[terminal]: https://github.com/rh-lean-roadmap/rh-lean-roadmap/blob/94e6a98b4e74932a0298d6bd22d44cf60c62764b/docs/src/book/main.tex#L7015-L7043
[level]: https://github.com/rh-lean-roadmap/rh-lean-roadmap/blob/94e6a98b4e74932a0298d6bd22d44cf60c62764b/docs/src/book/main.tex#L7174-L7186
[ideal]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AbelianVarietyTheory/Proofs/GlobalInterpolation/EvenThetaFunctionCmLatticeIntegralSplitPrime.lean#L35-L55
[translate]: https://arxiv.org/pdf/math/0610163#page=14
[half]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Formalism/LocalToGlobal/TorsionIntegrality/EisensteinTranslationProducts/SemiChar.lean#L18-L34
