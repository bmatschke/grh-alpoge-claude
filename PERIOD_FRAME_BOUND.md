# The period-height allowance and the frame estimate

On the selected family, the allowances $h_u$ for the individual words admit a two-sided bound after the common metric normalization is removed. Let $K$ be the row's coefficient field and put
$$
 q_\kappa=\frac1{[K:\mathbb Q]}\sum_{e:K\hookrightarrow\mathbb C}\log\kappa_e,
 \qquad L=x^\varepsilon,\qquad b=e^L,\qquad M=\max(C_t,5)+3.
$$
In the original parameter range, uniformly in the member at scale $x$ and the word $u$, eventually
$$
                  |h_u+q_\kappa|\le x^{9M+1}b.                 \tag{1}
$$
The one-sided estimate for $-h_u-q_\kappa$ is the numerical part of Roadmap B5.10a. Below we give both sides, including a sharper lower bound for the full archimedean kernel sum. The averaging measure in $q_\kappa$ is the normalized counting measure on **all** coefficient embeddings. The field defining this mean can have degree different from the number $f$ of row labels. [Height allowance on the original family][family] · [Exact mean and row kernel][kern] · [Roadmap height-exponent calculation][road]

## Bounding the kernel and hook terms

Use the polynomial
$$
 P=1+f+k+m+t+N_m+L,\qquad N_i=k+i(t+1).
$$
The original size conditions give $P\le x^M$ eventually and $P,b\ge1$. At each word, layer $i+1$ and archimedean label, write $y$ for one of the $N_i$ kernel entries. All these entries are positive integers. In the head block the last entry of the first layer is $\alpha_{k-1}+e_0-1-t/2>0$ since $\alpha_{k-1}>-b_0$ and $e_0-b_0\ge(t+3)/2$. The $\alpha_r+r$ are nonincreasing, and the increase of $e_i$ from one layer to the next is at least $t+3$, whereas $N_i$ increases by $t+1$. Thus this lower bound also works for the head entries in later layers. Every tail entry is $e_i-e_s-(i-s)(t+1)$ for $s<i$ and is positive by the same gap. [Actual head and tail coordinates](continuation_v89/heights.tex#L34-L76) · [Polynomial size comparison][poly]

Put $\lambda=\log\Omega=\gamma+\log(2\pi)-\log\mathrm{rd}(E)-d_1$, with $|d_1|\le L$ and $\mathrm{rd}(E)\ge1$ on the family. Each kernel summand is $g(y)=y\log y-(1+\lambda)y$. Its minimum on the positive half-line occurs at $y=e^\lambda$ and equals $-e^\lambda$. In particular
$$
  \sum_{i=0}^{m-1}\sum_\tau K_{u,i+1,\tau}
        \ \ge\ -2\pi e^\gamma\, f b\sum_{i=0}^{m-1}N_i.         \tag{2}
$$
This counts the actual number of kernel entries and costs at most a constant times $P^3 b$ for the entire negative contribution. It uses the upper bound on $\log\Omega$, which is stronger here than an absolute bound multiplied by the largest weight. For the other direction the row-size estimates give $y\le Y_1=11P^5b$, $\log Y_1\le16P$, and $|\lambda|\le7P$. Thus $|g(y)|\le264P^6b$ and the absolute value of the full sum is at most $264P^9b$. [Logarithmic derivative and discriminant estimates](continuation_v89/heights.tex#L93-L105) · [Kernel sizes on these weights][kernelbound]

For a layer $j$ and label $\rho$, write $a_i$ for its plus-hook weight, $n=k+j-1$, and $z_i=a_i+n-i$ for $0\le i<n$. The logarithm of the hook is
$$
       \sum_{i<n}\log\Gamma(z_i)
            -\sum_{i<l<n}\log(z_i-z_l).
$$
The two properties needed to bound both signs are $2\le z_i\le Y_2=10P^5b$ and $z_i-z_l\ge1$ for $i<l$. Indeed the bottom argument is $e_{j-1}-b_{j-1}-(t-1)/2\ge2$, the preceding arguments have the required separation by dominance, and the explicit weight sizes give the upper bound. Now $0\le\log\Gamma(z_i)\le Y_2\log Y_2$, while $0\le\log(z_i-z_l)\le\log Y_2$. Thus the hook logarithm lies between $-\binom n2\log Y_2$ and $nY_2\log Y_2$. Since $n\le P$ and $\log Y_2\le16P$, its absolute value is at most $160P^7b$. Summing over at most $mf\le P^2$ pairs gives $160P^9b$. This argument estimates the explicit hook factor in the allowance. The lower bound for the **actual theta eigenvalue** in B8.22 is a separate assertion. [Hook definition and level losses][definition] · [Bounds and separation of its arguments][hook]

The other pieces can be bounded with either sign. The terminal level term satisfies $0\le (\sum_s a_s)\log T_u\le2|C_{Tu}|P^4b$ by the top-weight estimates and the size of $T_u$. Its accompanying size term has absolute value at most $16|C_{\rm sz}|P^4b$. In each layer the extra kernel and hook size terms, after taking absolute values, cost at most $|C_{\rm sz}|(4P^4+P^7+6P^5)b$. For example the first is bounded using $fN_m^2L_a\le4P^4$ and the last using $fn_V^2 L'\le6P^5$. There are at most $P$ layers. Taking the absolute value of the exact formula for $h_u+q_\kappa$ therefore gives
$$
 |h_u+q_\kappa|\le (500+2|C_{Tu}|+30|C_{\rm sz}|)P^9b .
$$
Here $T_u$ is the actual word prime and $C_{Tu},C_{\rm sz}$ are the fixed family constants. Enlarge the common cutoff beyond that parenthesized constant, $9$, the word-level size cutoff and the initial family cutoff. This gives (1) before choosing the index or word. [Terminal and scale bounds][terminal] · [Exact decomposition and absorption][absorb]

## The two slope terms in entry 2

Let $d_u=\mathrm{rk}(N'_u)$ be the ranks of the actual divided column lattices, $r_*=\sum_u d_u$, and use the positive-total-rank range of the frame comparison. Put $\overline\mu_N=r_*^{-1}\sum_u d_u\mu(N'_u)$. The exact definition of the frame gives
$$
 \left|\bigl(s_{\rm fr}+\mu_{\max}(RR)\bigr)
        -\bigl(\overline\mu_N+\mu_{\max}(RR)+q_\kappa\bigr)\right|
   =\left|\frac1{r_*}\sum_u d_u(h_u+q_\kappa)\right|
   \le x^{9M+1}b.                                             \tag{3}
$$
In particular a common bound $\overline\mu_N+\mu_{\max}(RR)+q_\kappa\le x^A b$ implies the requested entry at any permitted middle exponent $C_H\ge1+\max(A,9M+1)$, after $x\ge2$. An upper bound on the rank-weighted **mean** of the divided slopes suffices. No absolute bound for the normalization $q_\kappa$ is needed. Conversely a polynomial-times-$b$ upper bound on the entry gives an upper bound of the same kind on the sum of slopes in (3), with the corresponding exponent allowance. This comparison concerns entry 2. An estimate for the norm of an individual period map is entry 6. [Frame definition][frame] · [Required inequality and distinct map-height entry][goal] · [Fullness of the selected divided lattices](continuation_v89/integral.tex#L43-L60)

The [divided-column estimate](PERIOD_DIVIDED_COLUMN_UPPER.md) now gives $\mu_{\max}(N'_u)\le x^{A_N}b$ for each positive-rank word on the original eventual design range. The prescribed unshifted lattice sits inside the actual stage-zero lattice even at the word prime, and the positive cost of the signed division is bounded directly. The [sharp-row transfer](PERIOD_SHARP_ROW_TRANSFER.md) gives $\mu_{\max}(R_1)\le\mu_{\max}(R_0)+2\log|G|$ on the same linked member. In view of (3), a normalized base-row estimate $\mu_{\max}(R_0)+q_\kappa\le x^{A_R}b$ suffices for entry 2. Indeed the upper bound for the frame is $x^{A_N}b+x^{A_R}b+8b+x^{9M+1}b$, which fits any permitted middle exponent exceeding $\max(A_N,A_R,9M+1)$ by one after a common cutoff.

The [fitted functional on the selected row](PERIOD_SELECTED_BASE_FUNCTIONAL.md) supplies this last bound at every serving place under the standing analytic hypotheses and the division premise of the period contract. Its common grid preserves the layer characters and the coefficient field of the selected bundle. The finite evaluation estimates the image of each changed lattice at its own tuple. With the [off-base eigenvalue floor](PERIOD_OFF_BASE_SCALAR.md) and [test-lattice estimate](PERIOD_AUXILIARY_TEST_SLOPE.md), this proves entry 2 on the admitted family. The [reference evaluation](PERIOD_REFERENCE_EVALUATION.md) gives an alternative criterion in terms of local lattice indices.

[family]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Formalism/SharpRestriction/ParConsts.lean#L61-L75
[kern]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Formalism/LocalRingCardinality/DataDIVDefs.lean#L56-L77
[poly]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Formalism/SharpRestriction/Divisibility/SlopeExcess/ConstRankBaseLePolyFourth.lean#L976-L1026
[kernelbound]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Formalism/SharpRestriction/Divisibility/SlopeExcess/ConstRankBaseLePolyFourth.lean#L511-L536
[definition]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Formalism/LocalRingCardinality/KernelPlaceMeanBound.lean#L9-L28
[hook]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Formalism/SharpRestriction/Divisibility/SlopeExcess/ConstRankBaseLePolyFourth.lean#L713-L763
[terminal]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Formalism/SharpRestriction/Divisibility/SlopeExcess/ConstRankBaseLePolyFourth.lean#L796-L865
[absorb]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Formalism/SharpRestriction/Divisibility/SlopeExcess/ConstRankBaseLePolyFourth.lean#L945-L975
[frame]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Formalism/LocalRingCardinality/DataArith.lean#L127-L135
[goal]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Formalism/SharpRestriction/GlobalTheoremInputs.lean#L77-L85
[arith]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Formalism/SharpRestriction/Divisibility/HookProducts/HhOfInputs.lean#L11-L24
[road]: https://github.com/rh-lean-roadmap/rh-lean-roadmap/blob/94e6a98b4e74932a0298d6bd22d44cf60c62764b/docs/src/book/main.tex#L33033-L33047
[divslope]: https://github.com/rh-lean-roadmap/rh-lean-roadmap/blob/94e6a98b4e74932a0298d6bd22d44cf60c62764b/docs/src/book/main.tex#L8733-L8759
[orig]: https://github.com/rh-lean-roadmap/rh-lean-roadmap/blob/94e6a98b4e74932a0298d6bd22d44cf60c62764b/docs/src/book/main.tex#L9301-L9311
[fitted]: https://github.com/rh-lean-roadmap/rh-lean-roadmap/blob/94e6a98b4e74932a0298d6bd22d44cf60c62764b/docs/src/book/main.tex#L19520-L19532
[select]: https://github.com/rh-lean-roadmap/rh-lean-roadmap/blob/94e6a98b4e74932a0298d6bd22d44cf60c62764b/docs/src/book/main.tex#L19536-L19543
[level]: https://github.com/rh-lean-roadmap/rh-lean-roadmap/blob/94e6a98b4e74932a0298d6bd22d44cf60c62764b/docs/src/book/main.tex#L8491-L8516
