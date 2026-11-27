# An admissible node spacing for the classical specialization

The classical specialization of the proof uses a common set of nodes at all lifts of a word. This calculation checks a change in their spacing on the original degree boxes. We follow one choice through the smoothing arguments, the signed degree error and the finite-prime terms. Here the Dirichlet character is trivial, and all estimates are for fixed admissible family constants and sufficiently large scale.

## The exponent required before choosing the mesh

<!--
% BEGIN WNS1
-->

<span id="claim:WNS1"></span>Adriazola's November 27 specialization to the trivial character takes $h_{\rm old}=2\lceil x^{402}\rceil$ between adjacent nodes. The standard row takes $T_O=\lceil x^{377}\rceil$ and requires $4T_O^2+2t_r\le h$, where $t_r$ is the positive odd rank increment. For $x\ge2$, $4x^{754}>2(x^{402}+1)$, so the proposed spacing fails already at that inequality. To choose a replacement, first fix the earlier box exponent $c_D\ge0$ and all preceding family constants. Take $c_h\ge1300+c_D$, increasing it to any larger lower bound already imposed on it by the preceding family data. Set
$$
 h=2\lceil x^{c_h}\rceil,\qquad
 \Delta=\lceil x^{c_D}\rceil,\qquad S_c=4k\Delta,\qquad \eta=mh.
$$
This choice precedes $x$, the host model, the shift and the word. It is the order of the original size-row quantifiers. [The reported spacing problem](https://github.com/jimjamzola/RH-Alpoge-Reconstruction/blob/3dd303f7af5190d7cc3cb3c23a2e8b072e6518d8/JustRH/RESEARCH_STATUS.md#L23-L39) · [Standard scale and integral ceiling](https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AbelianVarietyTheory/Definitions/GlobalTwisting/PairRowIffQdRows.lean#L12-L25) · [Order of the choices](https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AbelianVarietyTheory/Definitions/GlobalTwisting/PairRowIffQdRows.lean#L107-L126)

Here is a direct check of the four block-length inequalities. On the source rank data, eventually $T_O\le x^{378}$, $t_r\le x^{401}$, $1\le m\le x$, $k\le x^5$, $f\le x^3$ and $N=k+m(t_r+1)\le x^{402}$. For the row factors write $P=C_P z^{12}$, $D_y=f\binom{k+m-1}{2}$ and $c=C_{hT}$. The established rank estimates give $D_y\le x^{12}$, $z\le x^7$, and the fixed constants $C_P,c$ are at most $x$ eventually. Thus $P\le x^{85}$. For $x\ge6$ the four respective left sides
$$
 4T_O^2+2t_r,\quad P D_y f m^2NT_O,\quad
 P(fmk)^3 k/m,\quad cT_O Nf^2m^2kD_yP
$$
are at most $x^{757}, x^{882}, x^{117}, x^{891}$. Each is at most $h$. The extra size inequality $4N^3+2t_r+6\le h$ follows from $N\le x^{402}$ and $c_h\ge1300$. Both $kS_c$ and $m(t_r+1)\eta$ are polynomial in $x$. They are eventually smaller than $w''=b/(nZ)$ times any fixed positive constant, since $b=\exp(x^\varepsilon)$, $Z=\exp(x^{\varepsilon/3})$, and $n$ is polynomial. These four block inequalities and the stated node-size inequalities consequently hold at one threshold. [Four native block-length inequalities](https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AbelianVarietyTheory/Proofs/GlobalInterpolation/SzRowNodeGapBlockLength.lean#L19-L56) · [Substitution of the actual row variables](https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AbelianVarietyTheory/Proofs/GlobalInterpolation/SzRowNodeGapBlockLength.lean#L56-L81) · [Additional node-size thresholds](https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AbelianVarietyTheory/Proofs/GlobalInterpolation/ExplicitChoiceSizeNodes.lean#L11-L33)

<!--
% END WNS1
-->

## The same nodes in every translated word

<!--
% BEGIN WNS2
-->

<span id="claim:WNS2"></span>Keep the original degree boxes, word bits and starting integers $B_\rho$. At a marked place use $b_t+\lfloor b'/x\rfloor$, at an unmarked thin place $\lceil b/(nZ)\rceil$, and at a thick place $\lceil b\rceil$ with the permitted torsion correction at one designated place. Here $b'=xb/Z$ and $b'\le b_t\le(1+x^{-2})b'$ on the original top boxes. Indeed if $N_*=2n\delta_1$ and $L=x^\varepsilon$, their upper width is $N_*L\Lambda b'/k$, where $4N_*L\Lambda/k\le x^{-2}$ by the original size estimate. At layer $j=1,\ldots,m$ the lower node and its midpoint are
$$
 b_{j-1,\rho}=B_\rho+(j-1)h,\qquad
 w_{j\rho}=B_\rho+(j-\tfrac12)h .
$$
All are integers. Each half-gap is $h/2\ge(t_r+3)/2$ eventually. Since $2+mh=o(bx^{-2})$ and $mh=o(b')$, the thick nodes are in $[b,b(1+x^{-2})]$, and every other node, including a marked one, is in $(0,2b']$. The selected $a_t$ still satisfies $|a_t/b-x|\le1/(kx^{12})$. Thus the single-shift smoothing estimate in the comparison applies throughout its original node boxes, uniformly in the words and shifts. Its thick arguments $a_t/w_{j\rho}$ stay in $[x-2/x,x+2/x]$, and the thin arguments are at least $Z/3$. These statements require only the original field and weight-box hypotheses for that estimate. [Original bottom-box width and bound](https://github.com/bmatschke/grh-alpoge-claude/blob/1f87524a48dfb72bd22c73c4eefb828d1452293e/research/modules/construction/size_conditions/main.tex#L201-L222) · [Source base nodes and midpoint](https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AbelianVarietyTheory/Definitions/GlobalTwisting/PairRowIffQdRows.lean#L93-L105) · [Numerical boxes and the one-shift proposition](https://github.com/jimjamzola/RH-Alpoge-Reconstruction/blob/3dd303f7af5190d7cc3cb3c23a2e8b072e6518d8/JustRH/sec5_weights.tex#L52-L76) · [Dependence of the error on the boxes](https://github.com/jimjamzola/RH-Alpoge-Reconstruction/blob/3dd303f7af5190d7cc3cb3c23a2e8b072e6518d8/JustRH/sec5_weights.tex#L119-L147)

In the classical specialization the field is the real dyadic subfield composed with $\mathbf Q(\sqrt{-q},\sqrt{-d})$ for distinct large odd primes $q,d\equiv3\bmod4$. Its roots of unity are $\{\pm1\}$. Indeed an odd prime dividing the root order must ramify and so equals $q$ or $d$. Their inertia orders are two whereas each corresponding prime cyclotomic field has ramification index greater than two. The field $\mathbf Q(i)$ is unramified at both primes and the joint inertia fixed field is the totally real dyadic subfield, which excludes $i$. Correct $\sum_\rho B_\rho$ to even parity at a single thick place. There are $f=2n$ places in the CM type, so $\sum_\rho w_{j\rho}$ is even for every $j$, giving the torsion character condition also with the larger spacing. Appending $t_r+1$ entries $-w_{j\rho}$ in the comparison chain preserves the order of each row, since $w_{1\rho}$ dominates the initial negative endpoints and the midpoints increase. [Torsion condition on the formal weights](https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AbelianVarietyTheory/Definitions/GlobalTwisting/PairRowIffQdRows.lean#L99-L105) · [Classical field and weight chain](https://github.com/jimjamzola/RH-Alpoge-Reconstruction/blob/3dd303f7af5190d7cc3cb3c23a2e8b072e6518d8/JustRH/sec7_theta_chain.tex#L69-L95)

<!--
% END WNS2
-->

## The exact change of the column degrees and the signed height

<!--
% BEGIN WNS3
-->

<span id="claim:WNS3"></span>Write $\delta=h-h_{\rm old}\ge0$ and $d_j=(j-\tfrac12)\delta$. Compare the two numerical tuples with the same ranks, starting nodes, word bits, top degrees and initial word parameters $U_i$. At layer $j=l+1$ the $k$ head degrees in the source are $U_i+w_{j\rho}-N_l-t_r/2+i$. Each therefore increases by $d_j$. For each $0\le q<l$ the tail contains $t_r+1$ copies of $(l-q)(h-t_r-1)$. Each increases by $(l-q)\delta$. These changes hold for every word separately. Define $n_{j\rho}$ to be the sum of the column degrees, $\Delta_u^n=\sum_{j,\rho}(n_{j\rho}-a_\rho^\circ-kw_{j\rho})$, and $\mathcal S=\sum_{j,\rho}(p_j-q_j-k)w_{j\rho}$ for the signatures $(p_j,q_j)=(k+j-1,m-j)$. Then the new value minus the old one is
$$
 \Delta_{\!h}\mathcal S=\frac{f\delta\,m(m^2-1)}6,\qquad
 \Delta_{\!h}(\Delta_u^n-\mathcal S)
       =\frac{f t_r\delta\,m(m^2-1)}6 .
$$
For the first identity sum $(2j-m-1)d_j$. In the second, the $k$ head changes cancel $k d_j$. At each place the tails contribute $(t_r+1)\delta\sum_{l=0}^{m-1}l(l+1)/2$, and this sum is $m(m^2-1)/6$. Thus the change in the combined degree error has positive sign when $m>1$ and $\delta>0$. The possible increase of $|\ell|(\Delta_u^n-\mathcal S)_+$ is at most $|\ell|f t_r\delta\,m(m^2-1)/6$, where $\ell$ is the log CM period of the comparison. With $|\ell|=o(x^\varepsilon)$, this is polynomial in $x$. The bound is uniform in the word. [Actual head and tail formulas](https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Formalism/LocalRingCardinality/CoeNeZeroOfNotMem.lean#L12-L39) · [Integral positive column degrees](https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Formalism/LocalRingCardinality/CoeNeZeroOfNotMem.lean#L145-L186) · [Signed height before absorption](https://github.com/jimjamzola/RH-Alpoge-Reconstruction/blob/3dd303f7af5190d7cc3cb3c23a2e8b072e6518d8/JustRH/sec15_heights.tex#L23-L36) · [The degree error in the height bound](https://github.com/jimjamzola/RH-Alpoge-Reconstruction/blob/3dd303f7af5190d7cc3cb3c23a2e8b072e6518d8/JustRH/sec15_heights.tex#L115-L133)

The bare factorial-size terms in that height can also be compared. Set $\phi(y)=y\log y-y$, $\phi(0)=0$. On nonnegative integral arguments $u,v\le U$, telescoping the integrals of $\log y$ over consecutive unit intervals gives $|\phi(u)-\phi(v)|\le |u-v|(1+\log(1+U))$. There are at most $fmN$ degrees, each moves by at most $m\delta$, and their sizes are at most $b x^A$ for some fixed $A$ from the displayed formulas and the original top boxes. The total change in $\sum\phi(\nu)$ is therefore polynomial in $x$. With a nonempty top set the comparison budget $\mathcal B$ is at least $xb$, so both changes are $o(\mathcal B)$ for each fixed $\varepsilon>0$. The comparison of the actual kernel norms, frames and integral lattices at the new weights continues to enter the height hypothesis. [Original signed rows and degrees](https://github.com/rh-lean-roadmap/rh-lean-roadmap/blob/0be265ccb325908c67f872361d564c66b99e96f7/docs/src/book/main.tex#L6218-L6248) · [Height hypothesis for the physical frames](https://github.com/jimjamzola/RH-Alpoge-Reconstruction/blob/3dd303f7af5190d7cc3cb3c23a2e8b072e6518d8/JustRH/sec15_heights.tex#L65-L106)

<!--
% END WNS3
-->

## The change in the finite inert terms

<!--
% BEGIN WNS4
-->

<span id="claim:WNS4"></span>For the classical field retain a fixed admissible rank and prime datum. In the finite correction table take $Y_0=xnZ$ and write $\Delta\eta=m\delta$. All places receive the same increase $d_j$ at the $j$th node. At the inert primes of the first kind the exponent contains $\sum_\rho w_{j\rho}/(p^2-1)$, with the remaining digit term independent of the gap. Its increase is $fd_j/(p^2-1)$. For the other inert primes put $\gamma_p=p/(p^2-1)$, let $I$ be the union of the designated Frobenius orbits, $J$ its complement and $J_T$ the top set in $J$. Every orbit has length $r_p$. Its maximization uses the budgets $D_s=(k-1)w_j(\rho_s)$ in inequalities $\sum_l(p^ly_{sl}+y_{s-l,l})\le D_s$, $y_{sl}\ge0$. The maximum of $\sum_{s,l}y_{sl}$ can only increase when the budgets increase. Consequently the change in $\gamma_p\sum_s D_s-\max\sum y_{sl}$ is at most $\gamma_p r_p(k-1)d_j$. Summing over starting places, dividing by $r_p$, and taking the positive part bounds the increase of the first term by $\gamma_p|I|(k-1)d_j$. The other varying terms contribute $\gamma_p|J_T|\Delta\eta+12|J|d_j/p$. The digit terms keep their ranks, top degrees and cutoff. The correction for an element of odd nontrivial order is absent on this classical dyadic Galois group. [The two native inert exponents](https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Formalism/LocalRingCardinality/DataErr.lean#L121-L157) · [Feasible orbit arrays and their normalization](https://github.com/jimjamzola/RH-Alpoge-Reconstruction/blob/3dd303f7af5190d7cc3cb3c23a2e8b072e6518d8/JustRH/sec16_finite_correction.tex#L91-L125)

Since $\gamma_p\le2/p$, the increase per prime is at most $C f(k+1)\Delta\eta/p$ in both cases. For $n_0=\lfloor Y_0\rfloor\ge2$, $\lfloor n_0/p\rfloor\ge n_0/(2p)$ for $p\le n_0$. Taking valuations of $n_0!$ proves $\sum_{p\le Y_0}\log(p)/p\le2\log n_0$. Thus the increase in the sum of the inert exponents with their original weights $2\log p$, over all $m$ lifts, is at most $C'fm(k+1)\Delta\eta\log(2Y_0)$. This is polynomial in $x$. The separate auxiliary-prime exponent uses $2\sum_\rho W_u(\rho)$, where $W_u$ is the maximum of absolute shifted weight entries and excludes the top head. On the appended rows of WNS2 each entry changes by at most $m\delta$ and the rank shifts are fixed. Its change in absolute value is at most $2fm\delta$ per lift. For an admissible word prime with $\log T_u=O(m\log b)$ this also contributes a polynomial amount after multiplication by $m\log T_u$. Both costs are $o(\mathcal B)$ uniformly. These are bounds for the numerical table on the stated data. Identifying the integral operators with that table at the resized weights is an outstanding realization condition. [Auxiliary-prime maximum](https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Formalism/LocalRingCardinality/DataErr.lean#L98-L110) · [Finite-place normalization and realization condition](https://github.com/jimjamzola/RH-Alpoge-Reconstruction/blob/3dd303f7af5190d7cc3cb3c23a2e8b072e6518d8/JustRH/sec16_finite_correction.tex#L45-L81) · [Native orbit estimate](https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AbelianVarietyTheory/Proofs/DivisorProofs/OtherLossSum.lean#L166-L197)

<!--
% END WNS4
-->
