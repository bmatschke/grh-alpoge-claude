# Uniform block bounds and removal of the flag cutoff

In the scalar term for two different period maps, the zero Fourier mode must pass through $r+1=m/2$ levels with coefficient one. A fixed multiplicative loss at each singleton would overwhelm the answer. We give the estimate before the levels are summed. We use the original five insertions in B8.10e, so that the powers and the word budget agree with the pinned proof. The inputs at a real place are its compact signed coefficient form, its singleton Fourier and mixed lift identities, and the boundary limit on the same coefficient. The separating weight gives the scales used below. [Actual coefficient and weights][fb-coef] · [Boundary comparison for the terminal and residual slices](SPECTRAL_THREE_LETTER_SCALAR_SAMPLING.md) · [Separating-bit scale][fb-scale]

## What a block contraction measures

<!--
% BEGIN FBE1
-->

<span id="claim:FBE1"></span>Fix a Gram cutoff $\varepsilon>0$ and first cut the original coefficient off at compact support. At level $j\le r$, write $x_{p,w}$ for the inserted coefficient array on the residual group at the standardized prefix $p$ and admitted signed word $w$. In the arithmetic coordinates its vector is $\sqrt{n_j(p)}\,x_{p,w}/b(p)$, zero at invalid points. Here $n_j$ is the nonnegative point weight on the represented support and $b(p)>0$ the section factor. The positive coefficient form on these vectors is divided by $\Gamma_j^{\rm lev} n(w)$, with positive measure factor $\Gamma_j^{\rm lev}$ and $n(w)=\prod_{Y\in w}|P(Y)|>0$. At the terminal level use the normalized projected orbital vectors. The coefficient-form comparison of B8.10hbe on the residual rank $(k,r-j)$ applies to every finite linear combination. Quotient by its null space to obtain Gram vectors and a positive semidefinite matrix $G_j$ on every finite set of prefixes. The singleton Fourier identity at frequency zero gives precisely $G_{j-1}$ in this normalization.

At a nonzero frequency use the wave identity, or at a pair of distinct block entries use the lift identity, on the two finite linear combinations of prefixes. In each of five new positions interpolate the leading coefficient of the corresponding polynomial by its Lagrange coefficients $\ell_a(n)$. A positive letter is evaluated at $y_a$ and its companion at $y_a+1$. Put $d_n=\prod_{a=1}^5|\ell_a(n_a)|$, $D=\sum_n d_n$ and $\theta_n=d_n/D$. The grid gives $D>0$. The ratio from the two companion word norms and their mixed-form estimate is $\prod_a (|P(y_a)P(y_a+1)|/q_w(y_a))^{1/2}$, where $q_w>0$ is the word polynomial in the mixed estimate. The cut bound on this expression and the bounds on the sums of absolute Lagrange coefficients are taken **before** averaging. Weighted Cauchy–Schwarz bounds the remaining sum of products by
$$
 \left(\sum_n\theta_n\|u_n^+\|^2\right)^{1/2}
 \left(\sum_n\theta_n\|v_n^-\|^2\right)^{1/2}.
$$
The vectors here include the companion normalizations. Thus after multiplying by the fifth power of the frequency (respectively of $t^{-1}-{t'}^{-1}$), the mixed block has a positive block-matrix bound, with the fifth power of the corresponding wave or lift scale on both diagonal blocks. Indeed $2|\langle u,Mv\rangle|\le A(u,u)+B(v,v)$ follows from the displayed product bound for arbitrary $u,v$. The phase has modulus one. The unweighted Gram bound is available as well. At the terminal lift, if $t\ne t'$, one of $|t|,|t'|$ is at most $2/|t^{-1}-{t'}^{-1}|$ by the triangle inequality. Apply the terminal diagonal estimate on that side, then Gram Cauchy–Schwarz. These arguments introduce probability averages of energies and the prescribed scales, with no factor equal to the number of prefixes or interpolation nodes. [Compact residual form][fb-form] · [Wave, lift and terminal interpolation][fb-interp]

<!--
% END FBE1
-->

## The scale common to the places

<!--
% BEGIN FBE2
-->

<span id="claim:FBE2"></span>Choose an interior index $l$ where the two binary words differ. Write $\mathcal D$ for the weight spacing, $I=(\mathcal D-5)/2$ for the width of the cut, $h_0=v_l+y$ and $T_*=T_uT_v$. The ratio of the $l$th paired root factors on $5/2\le h_0\le\mathcal D/2$ satisfies
$$
 R_l^2=\frac{h_0+1}{\mathcal D-h_0}\le\frac{14h_0}{5\mathcal D}.
$$
This follows because exactly one denominator is shifted, $h_0+1\le7h_0/5$ and $\mathcal D-h_0\ge\mathcal D/2$. The cut has no pole. For the unshifted and edge factors use the interlacing and formal-degree comparisons of B8.10e. Write $t_\tau=(T_{{\rm crit},\tau}(u)T_{{\rm crit},\tau}(v)/T_*)^{1/2}$ with the critical levels defined from the Vandermonde factors on the same pair. The remaining root product, with its prefactors, is at most $C\sqrt{k}\,t_\tau$ before the factor $R_l$. Thus the full-cut ratio $B$ is at most $C'\sqrt k\,t_\tau$, while on $h_0\le N^3$ its supremum $B_1$ is at most $C'\sqrt{kN^3/\mathcal D}\,t_\tau$. The initial level and mass identity on the original selected row gives $\prod_\tau t_\tau\le C_t^f$. [Root pairing, edge factors and critical levels][fb-scale]

Before division by the ideal normalizers, B8.10e bounds the four types of scale by
$$
 C_A B_1,\quad C_A B d^{2i-2},\quad
 C_A B d^{2(i-1)+s-1},\quad
 (C_A B\kappa d^{2(i-1)}/\sqrt{T_*})^{1/2},
 \qquad d=\frac{C_A\kappa N}{gI}.
$$
Here $N=20(r+1)=10m$. The second expression starts at $i=2$ and the third at $s=2$. With $D_0=C_A\pi N/I$, the level and discriminant inequalities give $d\le D_0\le1$ at large rank and $\kappa\le\pi$ on the stated hosts. The four expressions are bounded, respectively, by a single constant times $t_\tau\sqrt{kN^3/\mathcal D}$, $t_\tau\sqrt k\,D_0^2$, $t_\tau\sqrt k\,D_0$ and $\sqrt{t_\tau}(k/T_*)^{1/4}$. Take the product over the places with the **same block indices** and then its $f$th root. The critical-level bound controls both the geometric mean of $t_\tau$ and that of its square root. Taking the largest such product in the definition of $\Theta^{-f}$ gives
$$
 \Theta\ \ge\ c\,\min\left\{
       \sqrt{\mathcal D/(kN^3)},\ I/(\sqrt{k}N),\ (T_*/k)^{1/4}\right\}
$$
with $c>0$ fixed before choosing the block. On the constructed family $\mathcal D\ge(kf\log b)^5$, $m\le f\le k$, $T_u,T_v\ge b^{m/2}$, $m\ge2$ and $b\ge k^{3/2}$. Since $N=10m$, the first two bounds grow at least as a fixed multiple of $k^{1/2}$, and the last at least as a fixed multiple of $k^{1/8}$. Enlarging the rank cutoff absorbs $c$ and gives $\Theta\ge k^{1/16}$. Thus there is a single scale for the block, even if the critical levels differ markedly from one place to another. [Threshold products and their uniform lower bound][fb-scale]

<!--
% END FBE2
-->

## Nonzero frequencies on the arithmetic lattice

<!--
% BEGIN FBE3
-->

<span id="claim:FBE3"></span>Let $E$ have $f$ complex places, one from each conjugate pair. Let $J$ be a fractional ideal and define $d_J=\sqrt{N(J)}$. Every $0\ne l\in J$ satisfies $\prod_v|v(l)|\ge d_J$, by the integral ideal $(l)J^{-1}$. Suppose $\prod_v z_v\le d_J(a/\Theta)^f$, with $\Theta>2a>0$. We claim that the sum over **all** nonzero elements of any subgroup of $J$ of
$$
 M_z(l)=\prod_v\min(1,(z_v/|v(l)|)^5)
$$
is at most $(C(a/\Theta)^{5/2})^f$ with absolute $C$. A zero $z_v$ makes the sum zero. Otherwise group elements by $n_v=\max(0,\lceil\log_2(|v(l)|/z_v)\rceil)$ and $h=\sum_v n_v$. Write $R_v=2^{n_v}z_v$, $U=\prod R_v/d_J$. A nonempty box has $1\le U\le 2^h(a/\Theta)^f$. Subdivide both real coordinate intervals in the $v$th place into pieces of length at most $R_v/(2U^{1/f})$. There are at most $25^fU^2$ product cells. Two points of one cell would have a difference with product of complex moduli strictly below $d_J$. A cell contains at most one. The shell weight per point is at most $2^{5f-5h}$. Its sum is at most $800^f (a/\Theta)^{2f}2^{-3h}$, hence at most $800^f(a/\Theta)^{5f/2}2^{-h/2}$ using $2^{-h}\le(a/\Theta)^f$ and $h\ge0$. Summing $2^{-h/2}$ over the tuples costs $(1-2^{-1/2})^{-f}$.

For a block of length $s$ starting at $b_0$, set $\nu=2r+3-2b_0-s$ and $g=g_0g_1$. Its period lattice contains $g^2\mathfrak d^\nu$, where $\mathfrak d$ is the different of $E$. Trace duality for the character $\exp(2\pi i\,\operatorname{Tr}(lt/g))$ puts the Fourier labels in $g^{-1}\mathfrak d^{-\nu-1}$. The inverse-difference labels belong to $g^{-1}\mathfrak d^{-\nu}$. The scales in B8.10e are chosen with exactly these two ideal norms in their product bounds. For fixed $t$, the map $t'\mapsto t^{-1}-{t'}^{-1}$ is injective, so the same shell sum bounds a row of off-diagonal labels. A fixed factor in the terminal scale is absorbed in $a$. The resulting error in either sum is at most $e=(C_1\Theta^{-5/2})^f$ for an absolute enlargement in this normalization. [The two ideals and their product bounds][fb-ideal] · [Local scales at the separating bit][fb-scale]

<!--
% END FBE3
-->

## Sampling a longer block

<!--
% BEGIN FBE4
-->

<span id="claim:FBE4"></span>For a full lattice $L_0\subset\mathbb C^f$ use the ordinary character dual for $2\operatorname{Re}\sum \sigma_v c_v$. Let $D(c)$ be the contracted nonnegative boundary density, integrable and continuous off the coordinate hyperplanes, extended there by zero. It is lower semicontinuous. At the boundary of a longer block the shorter vectors and their boundary approximants have joint Gram matrices. On each lattice shift the two mixed pairings and the boundary-boundary pairing have the same Fourier limit. For coefficients on a finite set of shifts, the quadratic form of the mean residual Gram kernel is the translation-invariant mean of a squared norm. This proves positive definiteness. One can take the mean along larger and larger translated lattice boxes whose distance from every coordinate hyperplane tends to infinity, passing to a subnet for the bounded pairings. For instance translate a box of side $n$ by $n^2$ times a lattice vector with every coordinate nonzero. Such a vector exists since a full lattice cannot lie in a finite union of proper real linear subspaces. Finite shifts change a vanishing fraction of a box, so the mean is translation invariant. The three boundary limits cancel one copy of the Fourier transform from the shorter pairing. Consequently in the normalization of B8.10hbb(b) we have $|\widehat D(\sigma)+A(\sigma)|\le J_0 F(\sigma)$, where $A$ is positive definite, $F$ is the summable shorter-pairing majorant and $J_0$ is the product of the positive section Jacobians.

Periodize $D$ on the torus with lattice $L_0$ and normalized Haar measure. The Fourier coefficients of the periodization are $\widehat D(\sigma)/\operatorname{covol}(L_0)$, with the matching sign in Fourier inversion. Take product Fejér means in any real lattice basis. The Fejér weights count pairs in a finite box with a specified difference, divided by the box size. The Fejér sum for $A$ is therefore its nonnegative quadratic form on the box characters at each point. The weights are at most one. Taking real parts bounds every Fejér mean of the periodization above by $J_0\sum_\sigma F(\sigma)/\operatorname{covol}(L_0)$. At $c_0$, periodization is bounded below locally by the sum of any fixed finite collection of translates of $D$. Lower semicontinuity and the nonnegative approximate identity give
$$
 \operatorname{covol}(L_0)\sum_{c\in Y}D(c)
       \le J_0\sum_{\sigma\in L_0^\vee} F(\sigma)
 \qquad (Y\subset c_0+L_0\ \text{finite}).
$$
In particular this inequality holds at the sampling coset itself, even if that coset meets a discontinuity of the periodization. [Boundary kernel and Fejér proof][fb-fejer] · [Root-sheet limits for the actual pairings](SPECTRAL_THREE_LETTER_SCALAR_SAMPLING.md)

For $L_R=(R(\mathbb Z+i\mathbb Z))^f$ its dual is $(2R)^{-1}(\mathbb Z+i\mathbb Z)^f$. In one complex coordinate there are $O(T^2)$ points of $\mathbb Z[i]$ in a disc of radius $T=\max(1,2Rz/g)$. The $j$th outer dyadic annulus costs at most $C T^2 2^{(2-5)j}$. The square-lattice sum divided by $R^{2f}$ is therefore bounded by $\prod_v C(R^{-2}+(z_v/g)^2)$. At each intermediate length let $R$ tend to infinity at fixed rank, reinstating the section Jacobians. The scale for the added coordinate gives
$$
 v_{b_0,a}=\frac{(\prod_\tau z_{b_0,a,\tau})^2}
  {N(g^{-1}\mathfrak d^{-(2r+3-2b_0-a)-1})}\le\Theta^{-2f}.
$$
The singleton integral starts the induction. Each intermediate coordinate costs $C^f v_{b_0,a}$ by the preceding square-lattice estimate. At the final coordinate use the actual period lattice with $\operatorname{covol}(L_{b_0s})=J_0$, and use FBE3 on the nonzero dual labels. Starting with the probability averages of FBE1 and composing them preserves total mass one. Thus the finite coset sum is bounded by $C_4^{fs}\prod_{a=1}^{s-1}v_{b_0,a}$ times an average of preceding diagonal energies. Constants from convergence of an individual boundary pairing disappeared before any factor was multiplied across coordinates. [Measure factors and block-volume induction][fb-vol]

<!--
% END FBE4
-->

## The recursion and the order of the limits

<!--
% BEGIN FBE5
-->

<span id="claim:FBE5"></span>Fix finite sets of permitted entries for each block start and length. They give finite prefix sets $X_i$ of total length $i$. On one such set contract an arithmetic majorant $B$ with the product $H$ of the local analytic kernels by $\operatorname{Re}\sum_{p,q}B(p,q)H(p,q)$. If the matrices are Gram matrices, this is the squared norm of the sum of the tensor products of their Gram vectors. It follows that the contraction preserves positive-semidefinite order in $B$, and that splitting the sum by last-block length costs a triangle inequality **after taking square roots**.

At a finite place the diagonal orbital kernel sums Gram contributions from the presentations of the fixed entry. Completing these to the whole residue class adds positive semidefinite matrices. Distinct residue classes give disjoint sub-sums of the predecessor presentations. The product comparison over the places follows by telescoping one factor at a time, using positivity of tensor products (or of entrywise products after restriction to common indices). Distinct global cosets have distinct tuples of residue classes. Completing to all tuples gives an upper bound $\eta_i K_{i-s}$ for the sum of the coset majorants against the preceding arithmetic kernel $K_{i-s}$. Here $\eta_i=1$ up to the last level and $\eta_{r+1}=e_1\ge1$ is the terminal density normalization. The terminal kernel is scaled by this same $e_1$.

For a singleton the zero Fourier coefficient contributes the predecessor itself. At each place one can use the ordinary Gram estimate or the companion bound, and for an inverse difference one has the original and the two companions. Summing the respective choices costs at most $2^f e$ in nonzero Fourier modes and $3^f e$ off the diagonal. Equivalently the off-diagonal sum is bounded by taking absolute mixed products, using $2ab\le a^2+b^2$, and applying the row sum to each end of the pair. Taking the supremum of the preceding normalized energies bounds each probability average. The squared-energy multipliers at a last singleton and a longer last block are therefore bounded, respectively, by
$$
 \eta_i(1+3^f e)(1+2^f e),\qquad
 \eta_i(1+3^f e)C_4^{fs}\Theta^{-2f(s-1)}\quad(s\ge2).
$$
The terminal singleton has only diagonal support. These bounds continue to hold as the auxiliary compact support increases with $\varepsilon$ fixed. Indeed the derivative estimate for the cut coefficient gives convergence in each finite pairing and an integrable majorant for the singleton integral. Positivity is closed under entrywise limits on a finite matrix, as evaluation on any fixed vector shows. The Lagrange weights for a fixed grid are fixed. If a compact approximation uses a choice of dominating probabilities, the admissible extensions on this finite tower form a finite set. Their probability vectors have a convergent subsequence in the closed simplex, and the limit satisfies the same inequalities. Taking the supremum of the energies gives the same bound for every choice. [Arithmetic domination and block estimates][fb-step] · [Compact-support passage for the original cut coefficient][fb-vol]

Divide square roots of energies by $\prod_{j\le i}\sqrt{\eta_j}$. A block skipping levels leaves a reciprocal product at most one. With $\Theta$ beyond a fixed threshold, the singleton square-root factor is at most $1+h$ for $h=(C/\Theta)^f$. For $s\ge2$, $s/2\le s-1$, so $C_4^{fs/2}\sqrt{1+3^f e}$ is absorbed into $C^{f(s-1)}$ for a single $C$. The bound for that block is $h^{s-1}$. A singleton uses at most ten new letters and a length-$s$ block at most $5(s+1)\le10s$. The total fits $N=20(r+1)$ at every prefix. Thus if $R_0$ is the maximum initial square-root energy on the reached words at that cutoff,
$$
 R_i\le(1+h)R_{i-1}+\sum_{s=2}^ih^{s-1}R_{i-s}
       \le (1+2h)^iR_0.
$$
For the last inequality, substitute the inductive bounds and use $\sum_{s\ge2}(h/(1+2h))^{s-1}=h/(1+h)$. The constants are fixed before $i,f,r$ and the finite entries are chosen. [Finite recursion and letter budget][fb-limit]

<!--
% END FBE5
-->

<!--
% BEGIN FBE6
-->

<span id="claim:FBE6"></span>For fixed host, word pair and finite tower, the initial normalized energy for each admitted word tends to $I_N=\prod_\tau J_\tau$. The signed residue formula evaluates a negative letter at $y+1$ and divides by that actual word weight. For clarity, the scalar-model argument is polynomial interpolation at fixed word length. Its positive boxes give the cutoff limit on a tensor grid of one more point than the degree in each variable. Before division by the word weight, the cutoff energy is a polynomial in these evaluation variables. Its candidate limit is the initial scalar energy times the product of the absolute word factors, also polynomial on the root-free cut where the sign of $P$ is fixed. Evaluation anywhere in the cut is a fixed finite linear combination of the grid values, which commutes with the limit. Division by the nonzero word weight at the chosen tuple now gives the normalized assertion. The width conditions $6NL_0\le I$ and $(k+2r+1)L_0\le I$ for boxes of length $L_0=O((r+1)^3)$ hold by $\mathcal D\ge(kf\log b)^5$. This covers each five-insertion history admitted by the budget, with its own interpolation coefficients. Taking the maximum over a finite collection commutes with this limit, also when $I_N=0$. At a represented terminal point the positive Gram value is fixed, so the cutoff eventually equals one there. Invalid points contribute zero. Finitely many points admit a common cutoff. The empty-word terminal kernel is then the Gram matrix of the original row vectors $V_p$, with its row and measure factors already included. Sending $\varepsilon$ to zero on this tower gives a squared-energy bound $e_1(1+2h)^{2(r+1)}I_N$. [Signed level-zero formula](SPECTRAL_LEVEL_ZERO_AND_CUTOFFS.md) · [Terminal identification and removal of the cutoff][fb-limit]

Now fix finitely many rows $\rho$. Absolute convergence of each row gives a tail bound $\sum_{p\notin X_{r+1}}|c_{\rho p}|\|V_p\|$ tending to zero as the finite sets grow. Every finite set of terminal points occurs in a finite tower by including each of its entries at its block start. The row norms converge, and their finite sum satisfies the same bound. Taking the supremum over finite row sets recovers the sum of their nonnegative squared norms whenever the full sum is used. There is no exchange of a rank limit with a cutoff limit. The *bound* is common to the towers and ranks because the factors already computed are common. On the constructed ranks $\Theta\ge k^{1/16}$, so beyond a fixed cutoff $h\le k^{-f/32}$. The relative loss due to the recursion is at most $\exp(4(r+1)h)-1$, within $b^{-7}$ at the family sizes in the mixed-period calculation. The unscaled initial energy and the separate finite density $e_1$ are both retained. [Comparison with the full period operators](../theta/MIXED_PERIODS_AT_THE_CONSTRUCTED_RANKS.md)

<!--
% END FBE6
-->

The following calculations fix the uncut normalization and identify the singleton scale and reciprocal-label coefficient on the regular cut. FBE12–19 compare the actual signed operators and terminal form and transport the germ under the residual estimates stated in FBE18. [Compact local comparison][fb-form] · [Actual coefficient and decay hypotheses][fb-coef]

## From Haar measure to the signed residual form

<!--
% BEGIN FBE7
-->

<span id="claim:FBE7"></span>First fix the normalization before differentiating the section. Nelson's real Bessel calculation gives a way to determine it on the uninserted coefficient. Let $G$ be the real unitary group, $R=U\rtimes H$ the marked unipotent and compact groups, $dh(H)=1$, $dr=du\,dh$ and $dg=dr\,d\dot z$ in quotient integration. Both groups are unimodular. Give the compact centre of $G$ mass one in the formal-degree formula so that the integral of the product of two coefficients on the central quotient equals its integral for this $dg$. Let $\tau$ be the unitary marking representation and $v$ a unit vector. For a unit vector $e$ in a square-integrable irreducible representation $\pi$ put $c(g)=\langle\pi(g)e,e\rangle$, with inner product linear in its first argument, and let $d_\pi$ be the formal degree for this $dg$. In the integrable range used for the uncut Bessel section, $c\in L^1(G)$ and the fibre integrals of $|c(y_*^{-1}r y)|$ are uniformly bounded. Put
$$
 W(y)=\int_R c(y_*^{-1}r y)\tau(r)^{-1}v\,dr,\qquad
 P=\langle W(y_*),v\rangle .
$$
Substitution in $R$ gives $W(sy)=\tau(s)W(y)$. Quotient integration bounds the $L^1$ norm of $W$ by $\|c\|_1$ and the given fibre bound makes it bounded, hence square integrable. Expand the first $W$ in $\int_{R\backslash G}\langle W(y),W(y)\rangle\,d\dot y$. Equivariance turns the result into $\int_G c(y_*^{-1}z)\langle v,W(z)\rangle\,dz$. Substitute the formula for the second vector. The integral of absolute values is bounded by $\|c\|_1$ times the fibre bound, so Fubini applies. Schur orthogonality in $z$ gives
$$
 d_\pi\int_G c(y_*^{-1}z)\overline{c(y_*^{-1}s z)}\,dz
       =\overline{c(y_*^{-1}s y_*)}.
$$
Thus $d_\pi\|W\|_2^2=\overline P=P\ge0$. Integrating on $U\backslash G$ gives the same norm, since $H$ has mass one. If the compact type is irreducible, its coordinate Gram operator commutes with $H$ by invariance. Its trace is $\|W\|_2^2$, so each diagonal entry is $\|W\|_2^2/\dim\tau$. For a nonzero section this fixes the scale giving orthonormal coordinates. For an uncut discrete-series coefficient this is the Schur normalization. Multiplying by the compact cutoff in FBE1 changes the matrix coefficient and requires the later cutoff limit. [Schur orthogonality, Theorem B][xfer-schur] · [Nelson's Bessel average, quotient measures and norm problems][xfer-nelson] · [Identification of the initial energy on the selected row](SPECTRAL_LEVEL_ZERO_AND_CUTOFFS.md)

<!--
% END FBE7
-->

<!--
% BEGIN FBE8
-->

<span id="claim:FBE8"></span>At a fixed positive-Gram compact cut the regular Jacquet integral has a local right inverse on the coefficient space of the slice. This supplies test vectors for the differential identities. In the two marked isotropic frames joined to their negative vectors, let $Z$ be the matrix of cross pairings and $Z_{[a]}$ its leading minor matrix of size $a$, where the whole matrix has size $a+1$. Give the two marks squared lengths $-tT_p,-tT_q$. The determinant of the joint Hermitian Gram matrix is
$$
 (-1)^{a+1}\left(|\det Z|^2-t^2T_pT_q|\det Z_{[a]}|^2\right).
$$
Indeed at $t=0$ exchanging the two block columns gives $(-1)^{a+1}|\det Z|^2$. The two diagonal blocks each have just one modified diagonal entry. A single such entry has zero cofactor at $t=0$, and the coefficient from taking both is $(-1)^aT_pT_q|\det Z_{[a]}|^2$. On the positive cut the matrix stays nonsingular for $0\le t\le1$. Its signature at zero is $(a+1,a+1)$, so its orthogonal complement in the marked unitary space is positive definite at $t=1$. To choose Witt frames locally, fix the first frame, solve the cross pairings for the dual-frame coordinates of the second, and orthogonalize its nondegenerate complement. Equivalently the isometry action on a nondegenerate frame of fixed Gram matrix is a submersion, with local sections obtained by completing a basis. Choices on the remaining positive space are related by compact unitary transformations. This explains which isotypic coefficient arrays a regular section may take. [Jin's joined Gram determinant and local frames][xfer-frame] · [Chen's marked-frame section][xfer-chen]

On a regular chart write $Z=Z_0 u$ with $u$ upper unitriangular. Gram–Schmidt with positive diagonal gives this decomposition by dividing the upper-triangular factor by its diagonal. It gives $u(Zu')=u(Z)u'$. Shrink the quotient coordinate chart so that the local frame section and this decomposition are defined on a neighbourhood of the support of a prescribed smooth test $A(Z_0)$. If the Jacquet integral in the removed coordinate is $\int\overline{\psi(u)}F(Z_0u)\,du$, take $F(Z_0u)=A(Z_0)\psi(u)\eta(u)$ for a smooth compactly supported $\eta$ of integral one in the **given** Haar measure. Integration recovers $A$. Do this successively on the removed coordinates in the actual order of integration. On a compact marking orbit use the corresponding compact-type average. On a vector fixed by the stabilizer with its type action this average is the identity, by probability normalization. The construction therefore lifts precisely the covariant test arrays on this chart. Compact quotient support and compact bumps give compact support upstairs. A partition of unity on the regular quotient glues the lifts by linearity. Multiplying either input by a scalar function of the surviving minor passes through the Jacquet integral, since that minor is constant on every integrated orbit. In particular the bare wave $\exp(sz-\bar s\bar z)$ passes through with its phase unchanged. A differentiated insertion on such a chart also differentiates the phase, as computed below. [Compact lifts for the one-pair descent][xfer-lift] · [Original wave and the invariant minor][xfer-nativewave]

<!--
% END FBE8
-->

<!--
% BEGIN FBE9
-->

<span id="claim:FBE9"></span>The one-singleton Jacobian gives an independent check on the scale of each signed coefficient. Use actual arithmetic coordinates at complex place $\tau$. Write $\Delta=|\operatorname{disc}E|^{1/(2f)}$, $\kappa=2\pi/(g\Delta)$, $D_g=2/(\Delta g^3)$, and for a singleton beginning at level $b$ set $\nu=2(r+1-b)$, $\lambda=(g/(2\pi))^\nu$ and $M_b=k+1+\nu$. The standard coordinate is $\lambda c$. The ratio of the arithmetic and standard point weights in this step is $(\Delta^{-\nu}\lambda^{-1})^{2(M_b-2)}=\kappa^{2\nu(M_b-2)}$. Indeed in the two-point pairing the two square-root factors supply one full point weight, and the singleton's section product has no factors. Changing complex area contributes $\lambda^{-2}$. The prescribed level measure satisfies $\Gamma_{b-1}/\Gamma_b=\kappa^{-2\nu(M_b-1)}/D_g$. Thus the arithmetic integral of a singleton, whenever the standard one-pair identity is used, is its parent pairing times
$$
 d_{b,1}=\kappa^{2\nu(M_b-2)}\lambda^{-2}\frac{\Gamma_{b-1}}{\Gamma_b}
        =\frac{\Delta^{2\nu}}{D_g}.
$$
At $b=r+1$ this gives $1/D_g$ with no coordinate dilation. The word and its normalization are identical in both entries. The product of these factors uses the covolume of the actual singleton period lattice. In the source normalization write $J=\mathfrak d^\nu$. A period is $t=g u$ with $u\in J$ and $u+\bar u\in gJ$. The first restriction costs $[J:gJ]=g^{2f}$. At every prime dividing the odd marked modulus $g$ the two conjugation idempotents are integral. Their lattices have rank $f$ each, and $1+\mathrm{conj}$ acts by $2$ on the plus lattice. Thus the second restriction costs $g^f$, giving $[J:L_{b,1}]=g^{3f}$. The covolume of $\mathcal O_E$ for one ordinary complex area per pair is $2^{-f}\sqrt{|\operatorname{disc}E|}$ and the ideal norm of $\mathfrak d^\nu$ is $|\operatorname{disc}E|^\nu$. Multiplying by the index gives exactly $(\Delta^{2\nu}/D_g)^f$. The reciprocal covolume in the zero Poisson frequency cancels this product. The result is the parent with coefficient one. [Original coordinates, densities and kernel][xfer-norm] · [Jin's singleton Jacobian and lattice normalization][xfer-single]

For a separate check on the archimedean Fourier convention, Jin's newer real-cell calculation uses $\psi(z)=\exp(2i\operatorname{Im}z)$ and ordinary complex area. For nonzero $\xi$ the real linear change of dual variables for $\psi(\xi w\bar z)$ has determinant $|\xi|^2/\pi^2$ relative to $e^{2\pi i\langle\eta,z\rangle}$. Thus Plancherel for $k-1$ coordinates costs $(\pi^2/|\xi|^2)^{k-1}$ in squared norm. This is the factor in the single-floor estimate. A bound on that integral with this factor cannot by itself supply the operator identity for the original signed array. [Jin's revised real-cell calculation][xfer-jinnew]

<!--
% END FBE9
-->

<!--
% BEGIN FBE10
-->

<span id="claim:FBE10"></span>There is an explicit positivity test for the signed insertion on each regular radial chart. Use Jin's two-by-two transfer $T_w(Y)$ on a word $w$ in the frame in which the previous residue form is $D_w>0$. Put $d(Y)=H_0 x(Y)$ for its lower-right entry, where $H_0>0$ on the cut, and $Q(Y)$ for the shifted quantum determinant. The one-site calculation needs the compact adjoint with respect to the **same** $D_w$ and measure, and the shifted cofactor identities for this transfer. Here is the resulting factorization. For any such Hermitian block form, writing the lower-left block as $D_w d\,\ell$ and lower-right block as $D_w d$, subtract the square of the lower component. Its quadratic form on $(u,v)$ becomes
$$
 \langle A_{\rm rem}u,u\rangle+
 \langle D_w d(v+\ell u),v+\ell u\rangle ,
$$
where $A_{\rm rem}=A-\ell^*D_w d\,\ell$. Here the adjoint uses the density of the common invariant compact test domain. For a positive site at $a$, the quantum determinant at $(a,a+1)$ gives $A_{\rm rem}=D_wQ(a)/(H_0x(a+1))$, and the second pivot is $D_wH_0x(a)$. For the negative site use the auxiliary transpose. The off-diagonal shear is then $D_w^{-1}\ell_w(a-1)^*D_w$, since the shifted alternating-line identity moves $T_{01}(a)$ through $d(a)$ to the entry at $a-1$. Thus its first pivot is $D_wQ(a-1)/(H_0x(a-1))$, and its second remains $D_wH_0x(a)$. In these formulas $x,Q$ act on the old diagonal type and bit. The compact interlacing makes the empty-word factors positive. Each old positive site multiplies the determinant by $(Y-t+1)/(Y-t)$, each old negative site by $(t-Y)/(t-Y-1)$. The analogous $x$ factors are adjacent linear quotients. The separation by more than two puts numerator and denominator on the same side of zero at every shifted evaluation. Induction and integration of the resulting squares give positive semidefiniteness for any finite family in this radial realization, including repeated compact types and the reflected companion at $a=y+1$. [Jin's positive pivots][xfer-positive] · [Reflected transfer and both shifted pivots][xfer-negative] · [Use on compact residual words][xfer-compact]

This also specifies how to verify an identification with the **group** differential operators. On a regular real-coordinate chart with smooth positive density $\rho\,dx$ and positive smooth fibre metric $D$, put $M=\rho D$. For $A=\sum_i a_i\partial_i+a_0$ the compact adjoint applied to $h$ is
$$
 A^\dagger h=M^{-1}\!\left(a_0^*Mh-\sum_i\partial_i(a_i^*Mh)\right).
$$
Integration by parts proves this with no boundary term on a compactly supported chart test. Products reverse order. To compare an order-$d$ operator with a proposed radial expression, use the lifts of FBE8 and test each vector coordinate against $(x-x_0)^\alpha/\alpha!$ times a bump equal to one near $x_0$, $|\alpha|\le d$. At $x_0$ these tests recover each coefficient of the differential operator in its ordinary derivative expansion. For the wave, $\partial_z f_s=s f_s$ and $\partial_{\bar z} f_s=-\bar s f_s$. Using $-\partial_{\bar z}$ for the reflected derivative gives the prescribed companion addition $+\bar s$, and $f_s$ has modulus one. This calculation determines the signs and the adjoint to check. Applying it to every ordered quantum minor and showing that the extensions across the singular block strata give the same pairings are still needed for the full mixed lift assertion.

<!--
% END FBE10
-->

[xfer-schur]: https://math.berkeley.edu/~jawolf/publications.pdf/paper_056.pdf#page=3
[xfer-nelson]: https://github.com/ultronozm/grh-workbook/blob/49fe050552850f18c51af2e3875ce94702aec99c/20261126T081500--a-bessel-function-at-a-real-place__workbook.tex#L157-L228
[xfer-frame]: https://github.com/yuiyuiui/Natural-Language-Proof-Generalized-Riemann-Hypothesis/blob/405237610e58ab9d4a9d5d54d9a0548a0c44227c/sections/g-real-restriction.tex#L1630-L1707
[xfer-chen]: https://github.com/yyyyychen/RH-Natural-Language-Proof/blob/d4dfb1a282dbf857288e73eb1f546dbfcc5899b8/tex/orbital-germ.tex#L405-L486
[xfer-lift]: https://github.com/yuiyuiui/Natural-Language-Proof-Generalized-Riemann-Hypothesis/blob/405237610e58ab9d4a9d5d54d9a0548a0c44227c/sections/g-real-restriction.tex#L8350-L8390
[xfer-nativewave]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Formalism/HermitianCurvature/HermitianCurvatureProofs/RadialWaveOrbital.lean#L11-L14
[xfer-norm]: https://github.com/rh-lean-roadmap/rh-lean-roadmap/blob/0be265ccb325908c67f872361d564c66b99e96f7/docs/src/book/main.tex#L46436-L46471
[xfer-single]: https://github.com/yuiyuiui/Natural-Language-Proof-Generalized-Riemann-Hypothesis/blob/405237610e58ab9d4a9d5d54d9a0548a0c44227c/sections/g-real-restriction.tex#L8421-L8446
[xfer-jinnew]: https://github.com/yuiyuiui/Natural-Language-Proof-Generalized-Riemann-Hypothesis/blob/163ad1f1289299b14dad7f48aa292cd5f85c69ca/sections/real-cell.tex#L1482-L1516
[xfer-positive]: https://github.com/yuiyuiui/Natural-Language-Proof-Generalized-Riemann-Hypothesis/blob/405237610e58ab9d4a9d5d54d9a0548a0c44227c/sections/g-real-restriction.tex#L6883-L6918
[xfer-negative]: https://github.com/yuiyuiui/Natural-Language-Proof-Generalized-Riemann-Hypothesis/blob/405237610e58ab9d4a9d5d54d9a0548a0c44227c/sections/g-real-restriction.tex#L7378-L7452
[xfer-compact]: https://github.com/rh-lean-roadmap/rh-lean-roadmap/blob/0be265ccb325908c67f872361d564c66b99e96f7/docs/src/book/main.tex#L44946-L44979

## The reciprocal of a regular block label

<!--
% BEGIN FBE11
-->

<span id="claim:FBE11"></span>One coefficient of the mixed lift can be computed on the normal block before comparing every ordered differential operator. Let a prefix of size $j$ end in a block of length $1\le u\le j$, starting at level $b_0$. Write its representative as $H\oplus\tau w_u$, where $H$ has size $j-u$, $w_u$ reverses the order of the $u$ basis vectors, and $\tau=\lambda t$ with $\lambda=(g/(2\pi))^{2r+3-2b_0-u}\mathrm i^{u-1}$. We work on the regular cut, so $t\ne0$ and $\det H\ne0$. Use the right unipotent character in which an adjacent upper matrix unit has coefficient one. Let $A(y)$ be the zeroth component of the normalized column-ordered Capelli minor, and $B(y)$ the component with the derivative of the surviving label. Denote their reflected operators by a superscript $\vee$. For a compact smooth test in the right-character model the coefficient of $y^j$ in $A$ is the identity. Indeed selecting the spectral scalar in every column gives the full ordinary minor, which is the normalization.

For $B$ the first $j-1$ ordinary rows vanish in column $j-u+1$ and outside the first $j$ columns. Deleting that column in the ordinary minor leaves $\det H\,\tau^{u-1}\det w_{u-1}$ with the ordered-minor convention. In the corresponding quantum expansion along the last column, the rightmost upper unit acts on the right average by its character. Only the adjacent entry survives. Repeating the deletion $u-1$ times leaves the minor of the head. Its highest spectral term is $y^{j-u}$, since every surviving column must supply its scalar term to attain this degree. The reflected expansion uses the last row. Moving its upper unit to the right lowers the argument by one at each deletion. All those shifts preserve the highest coefficient. Since $\det w_u=(-1)^{u-1}\det w_{u-1}$, division by $\det H\,\tau^u\det w_u$ gives $(-1)^{u-1}/\tau$ on the first side and $(-1)^{u-1}/\overline{\tau'}$ on the reflected side. For $u=1$ there are no deletions. For $u=j$ the empty head has determinant one. [Jin's normal-block computation][xfer-normal] · [Polynomial lift in the formal source][xfer-poly]

These calculations survive the orbital averages of a differentiated compact suffix on this cut. Near a given nonzero minor, insert a smooth cutoff equal to one in a neighbourhood of its value and zero near the divisor. The minor is right-invariant, so this insertion leaves its germ along the right integration fibre unchanged. Right translation differentiates the character on that fibre. The cutoff and compact support justify differentiating there. The left orbit preserves the minor. For the left average of each polynomial coefficient use interpolation at finitely many distinct real parameters where the cut integrals converge. Thus for a sesquilinear level form $F$ linear in its first entry the coefficient at $y^{2j-u}$ in
$$
 F(B(y)X,A^\vee(y+1)Y)-F(A(y)X,B^\vee(y+1)Y)
$$
is
$$
 \frac{(-1)^{u-1}}{\lambda}(t^{-1}-{t'}^{-1})F(X,Y).
$$
Conjugate linearity in the second entry removes the conjugation on $\lambda t'$. The shift by one preserves the leading term and fixes the companion word. Extract in five independent parameters starting with the last. Each remaining differentiated suffix is again a smooth test on this cut, giving the fifth power of the displayed scalar before FBE1 applies Cauchy–Schwarz. This determines the reciprocal-label coefficient for the normal-block minor. The full group operator and the compact coalescing-block comparison are treated in FBE12–19, with the residual integrability hypotheses given in FBE18. [Five interpolations after the right average][xfer-five] · [Local block estimate that consumes the coefficient][xfer-below]

<!--
% END FBE11
-->

[xfer-normal]: https://github.com/yuiyuiui/Natural-Language-Proof-Generalized-Riemann-Hypothesis/blob/405237610e58ab9d4a9d5d54d9a0548a0c44227c/sections/g-real-restriction.tex#L1455-L1516
[xfer-five]: https://github.com/yuiyuiui/Natural-Language-Proof-Generalized-Riemann-Hypothesis/blob/405237610e58ab9d4a9d5d54d9a0548a0c44227c/sections/g-real-restriction.tex#L1511-L1558
[xfer-poly]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Formalism/HermitianCurvature/HermitianCurvatureProofs/PBGLift.lean#L64-L104
[xfer-below]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Formalism/HermitianCurvature/HermitianCurvatureProofs/PBBLiftV.lean#L145-L172

[fb-form]: https://github.com/rh-lean-roadmap/rh-lean-roadmap/blob/c7755c1086f05d0918ee8496d95912e4f35e22f9/docs/src/book/main.tex#L44870-L44908
[fb-coef]: https://github.com/rh-lean-roadmap/rh-lean-roadmap/blob/c7755c1086f05d0918ee8496d95912e4f35e22f9/docs/src/book/main.tex#L46293-L46394
[fb-interp]: https://github.com/rh-lean-roadmap/rh-lean-roadmap/blob/c7755c1086f05d0918ee8496d95912e4f35e22f9/docs/src/book/main.tex#L46396-L46465
[fb-ideal]: https://github.com/rh-lean-roadmap/rh-lean-roadmap/blob/c7755c1086f05d0918ee8496d95912e4f35e22f9/docs/src/book/main.tex#L18004-L18025
[fb-scale]: https://github.com/rh-lean-roadmap/rh-lean-roadmap/blob/c7755c1086f05d0918ee8496d95912e4f35e22f9/docs/src/book/main.tex#L46244-L46293
[fb-fejer]: https://github.com/rh-lean-roadmap/rh-lean-roadmap/blob/c7755c1086f05d0918ee8496d95912e4f35e22f9/docs/src/book/main.tex#L44705-L44735
[fb-vol]: https://github.com/rh-lean-roadmap/rh-lean-roadmap/blob/c7755c1086f05d0918ee8496d95912e4f35e22f9/docs/src/book/main.tex#L46510-L46572
[fb-step]: https://github.com/rh-lean-roadmap/rh-lean-roadmap/blob/c7755c1086f05d0918ee8496d95912e4f35e22f9/docs/src/book/main.tex#L46573-L46611
[fb-limit]: https://github.com/rh-lean-roadmap/rh-lean-roadmap/blob/c7755c1086f05d0918ee8496d95912e4f35e22f9/docs/src/book/main.tex#L46612-L46639

## The four group operators on the regular section

<!--
% BEGIN FBE12
-->

<span id="claim:FBE12"></span>We compute the entrywise comparison proposed in FBE10. Work at one real place in the standard phase $\exp(2i\operatorname{Im}z)$, with the two characters acting on the left and right of the orbital section $U$. Order the next active Witt space as $(e,W,f)$, of dimension $m=2(r-i)+k+1$. The complexified right derivatives satisfy $[E_{ab},E_{cd}]=\delta_{bc}E_{ad}-\delta_{da}E_{cb}$. For equally long ordered lists $I,J$ use the column-ordered minor
$$
 \Delta_{I,J}(s)=\sum_{\pi}\operatorname{sgn}(\pi)
 \prod_{h=0}^{|J|-1}\big(E_{I_{\pi(h)},J_h}+(s-h)\delta_{I_{\pi(h)},J_h}\big).
$$
Write $D(s)$ for the full minor. Denote the signed minor deleting row $p$ and column $q$ by $m_{pq}$, and the double cofactor deleting ordered pairs $p<p'$, $q<q'$ by $n_{pp',qq'}$, with sign $(-1)^{p+p'+q+q'}$. At the current group point $g$ set $x=z'$, $y=g^{-1}z$, $\xi_j=\langle e_j,z'\rangle$, $\eta_j=\langle ge_j,z\rangle$, using linearity in the first slot. At a nonterminal site the marks are both the next $e$. Define $A(s;a,\beta)=\sum\beta_p a_q m_{pq}(s)$ and $B(s;a,b;\beta,\delta)=\sum(\beta\wedge\delta)_{pp'}(a\wedge b)_{qq'}n_{pp',qq'}(s)$ with scalar multipliers on the left. In order $00,01,10,11$ the group entries $Q_i(Y)$ are
$$
 D(s),\quad -A(s-1;x,\eta),\quad -A(s;y,\xi),\quad
 -B(s-1;y,x;\eta,\xi),\qquad s=Y+(m-1)/2.
$$

Write $w(c)e=cf$, $w(c)f=\bar c^{-1}e$, and restrict to $w(c)g'$ with $g'$ acting on $W$. The following calculation acts on $\Phi(c,g')=U(w(c)g')$. Put $P_+=s+c\partial_c$, $P_-=s-m+1-\bar c\partial_{\bar c}$ and $t=Q_{i+1}(Y)$. To expand from either end, introduce exterior variables $\epsilon_a$ and put $C_j=\sum_a\epsilon_a E_{aj}$. The bracket gives $\{C_j,C_l\}=-\epsilon_j C_l-\epsilon_l C_j$. Thus adjacent factors $C_j+u\epsilon_j,C_l+(u-1)\epsilon_l$ alternate in the columns. For rows the identical computation has the opposite sign and the shifts increase by one. Extracting both exterior coefficients in the product of the shifted sums gives the same minor, permitting row expansion with the shifts reversed.

Expand the outer columns and then the exposed outer rows. Differentiating the right character replaces the rightmost $E_{ej},E_{jf},E_{ef}$ by $x_j,\xi_j,0$ of the next site. Conjugating the corresponding left generators by $w(c)g'$ gives the substitutions $c^{-1}\eta_j,\bar c^{-1}y_j,0$ for the leftmost $E_{je},E_{fj},E_{fe}$. These are the two adjacent character entries and the zero on the nonadjacent root; the factors of $c$ come from the displayed action on $e,f$. Right derivatives preserve left covariance. Keeping both outer diagonals gives $P_-t_{00}P_+$. Deleting one interior row and column gives the two single cofactors, and deleting two gives both alternating orders in the two wedges of $B$. The middle full minor has shift $s-1$ since the dimension has fallen by two. For the other three entries the contractions delete $e$, $f$, or both before the same expansion. The four results in their action order are
$$
 \begin{aligned}
 00:\ &P_-t_{00}P_++P_-c^{-1}t_{01}+\bar c^{-1}t_{10}P_++|c|^{-2}t_{11},\\
 01:\ &-c(P_-t_{00}+\bar c^{-1}t_{10}),\\
 10:\ &-\bar c(t_{00}P_++c^{-1}t_{01}),\\
 11:\ &|c|^2t_{00}.
 \end{aligned}
$$
Multiplying the restriction by $|c|^{m-1}$ removes the half-dimension shifts from both Euler operators. The resulting matrix is $L^\vee Q_{i+1}L$, where
$$
 L=\begin{pmatrix}Y+c\partial_c&-c\\c^{-1}&0\end{pmatrix},
 \qquad L^\vee=\begin{pmatrix}Y-\bar c\partial_{\bar c}&\bar c^{-1}\\-\bar c&0\end{pmatrix}.
$$
The multiplicative density $d^2c/|c|^2$ gives zero divergence for both radial and angular translation, so the two displayed matrices are formal adjoints for real $Y$. Different pairs use independent coordinates. Iterating therefore restricts the original ordered products, including their lower-order terms. [Jin's active-group convention and calculation](https://github.com/yuiyuiui/Natural-Language-Proof-Generalized-Riemann-Hypothesis/blob/405237610e58ab9d4a9d5d54d9a0548a0c44227c/sections/g-real-restriction.tex#L5779-L5947)

<!--
% END FBE12
-->

<!--
% BEGIN FBE13
-->

<span id="claim:FBE13"></span>The exchange identity also descends to the actual middle matrix $M=Q_{i+1}$. Write $P$ for the permutation of two auxiliary factors and $R=(u-v)1-P$. Define $X=RM_1(u)M_2(v)-M_2(v)M_1(u)R$. For $K=L^\vee ML$, the exchange difference for $K$ is $L_2^\vee(v)L_1^\vee(u)X L_1(u)L_2(v)$. Indeed the Euler commutators $[c\partial_c,c^{\pm1}]=\pm c^{\pm1}$ give the site exchange for $L$, and complex conjugate differentiation gives it for $L^\vee$. The barred, unbarred and residual coefficient algebras commute. The $00,00$ entry on the group vanishes because the full shifted Capelli minors are central. The restriction admits tests $|c|^{2\beta}c^n V(g')$ for every $\beta\in\mathbb R,n\in\mathbb Z$ and every smooth covariant residual germ $V$. In fact, if $g_0$ is the old matrix then $c=(g_0)_{fe}$ and the residual block is $(g_0)_{WW}-(g_0)_{We}c^{-1}(g_0)_{fW}$. Its omitted factors are unipotent and are recovered by the outer row and column. Extending the test by their characters and inserting a bump equal to one near the test point gives the required germ.

After cancelling the test scalar, the coefficients on $X_{AB}$ have the form $\bar c^{-|A|}c^{-|B|}a_A(\beta)b_B(\gamma)$, $\gamma=\beta+n$, for binary pairs $A,B$. In the order $00,01,10,11$ these polynomials are
$$
 \begin{aligned}
 a&=((v-\beta)(u-\beta),\,u-\beta,\,v-\beta+1,\,1),\\
 b&=((u+\gamma)(v+\gamma),\,u+\gamma-1,\,v+\gamma,\,1).
 \end{aligned}
$$
The unit shifts come from differentiating reciprocal coordinates in the other factor. Radius and argument distinguish the two bit counts. At fixed $\beta$, infinitely many values of $n$ separate polynomial coefficients in $\gamma$, and then $\beta$ separates the others. At bit count one each pair of linear polynomials is independent for $u-v\ne1$. Polynomial continuation includes the exceptional value. Thus $X_{AB}V=0$ for every $A,B,V$. A rank-zero residual group can be placed inside a group with one additional exterior hyperbolic pair for this test.

On the positive terminal Gram cut put $H_0=|\langle gz',z\rangle|^2-TT'$. Complete $(g^{-1}z,z')$ by an orthonormal basis of their common perpendicular. For $M_{11}$ only the cofactor on this perpendicular survives. Its coefficient is $H_0$ because the two-vector Gram determinant is $-H_0$. On compact type $\rho$ the residual minor acts by $\prod_j(Y+\rho_j)$, by evaluating the central Capelli operator on a highest-weight vector. The off-diagonal adjunction uses Haar measure on the group, where compact test coefficients permit integration by parts. The compact stabilizer projections are self-adjoint. Disintegration over the marked inner product $\zeta$ gives density $H_0^{k-1}d^2\zeta$ as in FBE7. Moving $H_0^{(k-1)/2}$ into *both* coefficient vectors therefore gives the flat-density adjoint in FBE10 on regular compact tests. This procedure never integrates an unrestricted radial derivative across $c=0$. [Exchange and group adjunction](https://github.com/yuiyuiui/Natural-Language-Proof-Generalized-Riemann-Hypothesis/blob/405237610e58ab9d4a9d5d54d9a0548a0c44227c/sections/g-real-restriction.tex#L5949-L6203)

<!--
% END FBE13
-->

## A fixed head and a coalescing block

<!--
% BEGIN FBE14
-->

<span id="claim:FBE14"></span>Fix a complete head $H_0$ whose blocks have nonzero parameters. Its determinant is a product of signed block powers and is nonzero, although several leading minors inside a reversing block can vanish. Integrating this head in a compactly supported matrix test gives a new smooth compact test in the residual variable $Z$. To see properness on the support, the full matrix after elementary shears has blocks $(H,Hb;aH,aHb+Z)$ with $H=L_HH_0U_H$. If the off-diagonal blocks are $B,C$, then $b=H^{-1}B$, $a=CH^{-1}$ and $Z$ is the lower right block minus $CH^{-1}B$. The determinant of $H$ is fixed, so its adjugate bounds its inverse on the support. For the head's own orbit coordinates first remove its fixed row permutation. The remaining allowed lower factor and upper factor are unitriangular with a fixed invertible diagonal between them. Their entries are minors divided by initial products of that diagonal, by elimination. The roots omitted from the lower factor are exactly the stabilizer roots. All integrations are now over a bounded set, locally uniformly on each fixed determinant annulus. In a residual unitary slice the two removed radical factors are recovered from the outer blocks in the same way; the remaining block is the residual group matrix. With the entire end pivot $P$ invertible, its inverse is bounded by its adjugate and the determinant lower bound. If the original positive Gram cut is $\varepsilon$ the residual cut is $G_\mathrm{res}\ge\varepsilon/|\det P|^2$. Consequently all matrix and finite group derivatives at this stage are supported in a common compact set. The Jacobians of the additive shears are one. These statements apply to a prescribed reversing head directly, regardless of the values of its internal minors. [Inverse matrices and residual cut](https://github.com/yuiyuiui/Natural-Language-Proof-Generalized-Riemann-Hypothesis/blob/405237610e58ab9d4a9d5d54d9a0548a0c44227c/sections/g-real-restriction.tex#L677-L785)

The scalar matrix germ determines the value at an additional reversing block of length $s=d+1\ge2$. Take complex measure $|\beta|d^2x/(2\pi)$ for the character $e_\beta(x)=\exp(i\operatorname{Re}(\beta x))$. Let $B_\Phi(\tau,c)$ be the orbit integral at the split blocks $(\tau w_d,c)$ and $L_\Phi(z)$ that at $zw_s$, where $w_j$ reverses $j$ indices. On compact determinant annuli $D_0=c\tau^d$, the expansion for a smooth compact matrix test is
$$
 |\tau|^{d^2}B_\Phi(\tau,c)
   =s^{-1}\sum_{z^s=(-1)^dD_0}|z|^{d^2}e_\beta(sz/\tau)L_\Phi(z)+O(|\tau|).
$$
Here is the Jacobian computation. Use an upper unipotent $n$ of size $d$, a final upper column $p$ and a lower row $a$. Replace their coordinates by $\tau(n-1),\tau p,\tau a w_dn$. The real Jacobian of the inverse is $|\tau|^{-d(d+3)}$. After reversing rows the matrix has subdiagonal $\tau$, diagonal $(u,x_1,\ldots,x_d)$ and strictly upper part $Y$. Its determinant is $P_\tau u+Q_\tau=(-1)^dD_0$, with $P_0=\prod x_j$ and $Q_0=0$. Solving for $u$ contributes $|\tau|^{2d}/|P_\tau|^2$ relative to solving for the old last coordinate. On a compactly supported test the entries stay bounded and the determinant stays away from zero, so on the support $P_\tau$ and all $x_j$ stay away from zero for small $|\tau|$. All remaining variables then range over compact sets uniformly. The phase left at scale $\tau^{-1}$ is $G=\sum x_j+(-1)^dD_0/\prod x_j$; the difference $(u_\tau-u_0)/\tau$ is smooth in the amplitude.

Its critical points have $x_1=\dots=x_d=z$. The complex Hessian is $(1+\mathbf1\mathbf1^t)/z$ of determinant $s z^{-d}$; the real part has $d$ positive and $d$ negative eigenvalues. Stationary phase with the displayed measure gives $|\tau|^d|z|^d/s$ and a uniform remainder one order smaller. Off the critical neighbourhoods the gradient is bounded away from zero and repeated integration by parts gives the same error. Differentiating the determinant at $\tau=0$ gives $u'_0=\sum_{j}Y_{j,j+1}/z$. Substituting $Y=zv$ recovers the long-block character. Its Jacobian and $|P_0|^{-2}$ contribute $|z|^{sd-2d}$, which together with the Hessian gives $|z|^{d^2}$. The same estimate holds for a test valued in a Banach space when the support and derivative bounds just used hold in that norm, by applying the uniform scalar estimate to norm-one functionals. [Jin's matrix orbital calculation](https://github.com/yuiyuiui/Natural-Language-Proof-Generalized-Riemann-Hypothesis/blob/405237610e58ab9d4a9d5d54d9a0548a0c44227c/sections/g-real-restriction.tex#L558-L675)

One consequence is uniqueness at every prescribed head for compact matrix tests supported on invertible matrices, as ensured by the positive Gram cut. If all regular diagonal orbital integrals vanish, argue by induction on size. With last block a nonzero scalar, integrate that scalar and the two adjacent rectangular radicals first to obtain a smaller smooth compact test on invertible matrices. Its diagonal integrals vanish, so induction gives vanishing for every preceding head. For a last block of size $s>1$, freeze the preceding head by the calculation above. Every split integral in the displayed formula vanishes by the scalar case. Fix $D_0=(-1)^d z_0^s$. Choose a complex ray $1/\tau=t v$ on which the real frequencies of the $s$ roots are distinct. Multiply the expansion by $e_\beta(-s z_0tv)$ and average over $1\le t\le R$. The other oscillatory means tend to zero and the error costs $O(\log R/R)$. Thus $L_\Phi(z_0)=0$. This determines the singular value of a difference of tests from its regular transform, including at heads with internal zero minors. [Determination by the Jacquet integral](https://github.com/yuiyuiui/Natural-Language-Proof-Generalized-Riemann-Hypothesis/blob/405237610e58ab9d4a9d5d54d9a0548a0c44227c/sections/g-real-restriction.tex#L1630-L1813)

<!--
% END FBE14
-->

<!--
% BEGIN FBE15
-->

<span id="claim:FBE15"></span>The passage from a compact-annulus vector germ to the three mixed limits needs no global remainder bound tending to zero. Let $V$ be the Hilbert space of a positive cut kernel as in FBE1. Write $U_x(D)$ for the old vector after rescaling the last singleton and $B(z)$ for the normalized long-block vector. The hypotheses for this step are a uniform old diagonal bound $\|U_x\|_2\le C$ and, on every compact annulus of nonzero $D$, the germ
$$
 U_x(D)=M_x(D)+O_K(|x|^{-1}),\qquad
 M_x(D)=\sum_{z^s=D}e_\beta(szx)\frac{B(z)}{s|z|^{s-1}} .
$$
Conjugate the character if using the opposite convention for the first slot of the pairing. The old bound comes from the preceding block length after singleton disintegration. The factor $s|z|^{s-1}$ is the square root of the area Jacobian of $z\mapsto z^s$. On any annulus expand $\int\|M_x\|^2$ and change variable through its first root. For the cross term with root $\zeta z$, $\zeta^s=1$, $\zeta\ne1$, the phase has frequency $s(\zeta-1)x$ and its amplitude is integrable there. Riemann–Lebesgue removes this term. The diagonal gives the integral of $\|B\|^2$ on the inverse annulus. By the local germ and the uniform bound that integral is at most $C^2$. Exhaustion gives $B\in L^2(\mathbb C,V)$. The root sum of norms $m(D)=\sum_{z^s=D}\|B(z)\|/(s|z|^{s-1})$ has $\|m\|_2^2\le s\|B\|_2^2$, so controls all model tails simultaneously.

Put $C_xF(c)=|x|^{-(s-1)}F(c/x^{s-1})$, a unitary dilation. In the model–model pairing with a second head at $x+y$, undo the first dilation and write $\alpha^s=(x/(x+y))^{s-1}$ with $\alpha$ near one. With the first slot conjugate linear the terms have frequency $s(\zeta\alpha(x+y)-x)$ and amplitude $\langle B(z),|\alpha|B'(\zeta\alpha z)\rangle$. These amplitudes converge in $L^1$ by continuity of dilations in $L^2$. Only $\zeta=1$ survives, and its frequency tends to $y$ since $\alpha=1-(s-1)y/(sx)+O(|x|^{-2})$. The limit is $\int e_\beta(yz)\langle B(z),B'(z)\rangle\,d^2z$. In the old–model pairing, the old-minus-model difference tends to zero in $L^2$ on each annulus and stays bounded globally. The other factor is bounded by the dilated $m'$, which tends to $m'$ in $L^2$ in the common coordinates. Splitting off a tail of arbitrarily small $L^2$ norm proves the same limit. Taking adjoints gives the model–old limit. An old–old remainder may survive. Its translation average is positive definite because every finite quadratic combination of translated difference vectors is a squared norm before averaging. This is the positive correction admitted in the long-block Poisson inequality. The argument specifies exactly which local vector germ must hold in the original residual Hilbert norm. [Annular normalization and the three pairings](https://github.com/yuiyuiui/Natural-Language-Proof-Generalized-Riemann-Hypothesis/blob/405237610e58ab9d4a9d5d54d9a0548a0c44227c/sections/g-real-restriction.tex#L1269-L1453)

<!--
% END FBE15
-->

## The signed determinant and the terminal pairing

<!--
% BEGIN FBE16
-->

<span id="claim:FBE16"></span>The shifted determinant in FBE10 can be evaluated on the group. Keep the cofactor notation of FBE12, writing a double cofactor as an alternating function of either ordered pair, and let $s=Y+k/2$ at the terminal group. The cofactor multiplication identity is
$$
 m_{ij}(s+1)m_{qp}(s)-m_{qj}(s+1)m_{ip}(s)=D(s+1)n_{iq,jp}(s).
$$
For a direct verification multiply as a row vector in $p$ by $(E+(s+1)1)^t$. In a summed single cofactor this appends a row and gives $\delta_{cq}D(s+1)$ in column $c$. A summed double cofactor gives $\delta_{cq}m_{ij}(s+1)-\delta_{ci}m_{qj}(s+1)$ by the same expansion. The two products agree by centrality. Cancellation is legitimate over the fraction division algebra of the enveloping algebra with central variable $s$ (or by its formal Laurent series at $s=\infty$, where the matrix is invertible). The equality is polynomial, so holds on the actual differential operators.

The scalar multipliers $y_j,\eta_i$ need to pass the factors in this identity. Their commutators with $E_{ab}$ are $-\delta_{aj}y_b$ and $\delta_{bi}\eta_a$ respectively. Thus moving the exterior covector $\sum\epsilon_i\eta_i$ through a shifted column lowers its shift by one and reverses sign. Move the covectors to the right in both single and double cofactors. Expanding the determinant commutator in the row containing $y_j$ and the single cofactor commutator in the column containing $\eta_i$ gives on both sides the same correction
$$
 -\sum_{l,j,a}y_l m_{jl}(s+1)n_{aq,jp}(s)\eta_a
$$
when the constant vectors $x,\xi$ select column $p$, row $q$. After subtracting this term the displayed cofactor identity applies. By linearity one obtains
$$
 Q_{00}(Y+1)Q_{11}(Y)-Q_{10}(Y+1)Q_{01}(Y)
       =-A(s;y,\eta)A(s;x,\xi).
$$
In a frame beginning with the right mark, $A(s;x,\xi)$ is $-T'$ times the compact determinant on its orthogonal complement. In a frame transported from the left mark the other factor is $-T$ times the left compact determinant. Converting to left derivatives reverses their order, precisely the row convention of FBE12. For centered compact weights $u_j,u'_j$ the determinant is consequently
$$
 q(Y)=-TT'\prod_{j=1}^k(Y+\tfrac12+u_j)(Y+\tfrac12+u'_j).
$$
Together with the terminal $11$ entry in FBE13 this supplies the two scalar data for the Schur complements of FBE10. A positive site multiplies this determinant on the alternating auxiliary line by $(Y-a+1)/(Y-a)$, and a reflected site by $(a-Y)/(a-Y-1)$. For the reflected factor this follows by multiplying the partially transposed flips: if $P$ interchanges the two auxiliary spaces and $P_1,P_2$ are their contracted flips with the new bit, then $P_1P_2=P_1P=PP_2$ and $P_2P_1=P_2P=PP_1$. These relations give the exchange identity for the reflected site, so the alternating-line scalars multiply along the word. The same multiplication gives $T(Y)^t J T(Y-1)=q_w(Y-1)J$ with the contracted determinant and the alternating matrix $J$. Its lower-right entry is the shift in the negative shear in FBE10. This ties that shift to the group cofactor identity. [Shifted product and the two compact determinants](https://github.com/yuiyuiui/Natural-Language-Proof-Generalized-Riemann-Hypothesis/blob/405237610e58ab9d4a9d5d54d9a0548a0c44227c/sections/g-real-restriction.tex#L6031-L6153) · [Reflected site calculation](https://github.com/yuiyuiui/Natural-Language-Proof-Generalized-Riemann-Hypothesis/blob/405237610e58ab9d4a9d5d54d9a0548a0c44227c/sections/g-real-restriction.tex#L7378-L7421)

<!--
% END FBE16
-->

<!--
% BEGIN FBE17
-->

<span id="claim:FBE17"></span>On the positive compact cut there is a pointwise identification at the final singleton. For a word $w$ write $B_{b,w}$ for the product on its bit spaces of the site matrices $L_b(a)$ for positive letters and the entrywise adjoints for reflected letters, in reverse insertion order. Inserting a new site in the residue form of FBE10 gives
$$
 \mathcal R_{b-1,w}=B_{b,w}^*\mathcal R_{b,w}B_{b,w}.
$$
At the empty word both residue forms are the identity. The first site uses FBE12. In the induction step exchange the new site with each old site's root factor using FBE13 and FBE16. Old bit factors act on a different tensor component. At a positive letter this puts $L$ on the right and its mirror on the left. At a negative letter the auxiliary transpose reverses the product and puts the entrywise adjoint on the right. This proves the identity on regular compact test sections with the common density. It also explains why both columns must be evaluated at the same singleton parameter when splitting off $d^2c/|c|^2$.

At the last singleton the compact residual group on each marked side acts by left and right unitary maps on the Hilbert–Schmidt fibre. For a fixed prescribed head integrate its stabilizer roots first. Conjugating them to the other triangular factor preserves the character by relevance, and the successive shears have determinant one in the additive root coordinates. A mass-one cutoff in the stabilizer leaves precisely the head slice of FBE14. To use this statement for a differentiated word, first cut in the full head determinant away from zero while keeping a neighbourhood of its given value. The full determinant is invariant along the averaging directions. The compact lift of FBE8, with a mass-one bump along the upper triangular coordinates and normalized character bumps along the two removed radicals, has the required differentiated Jacquet integral. On the positive Gram cut the compact matrix test used here is obtained from the joint Gram matrix of the two marked frames. Its determinant is, up to sign, $|\det Z|^2-TT'|\det Z_{[r]}|^2$. This follows by expanding the two rank-one corrections from the marked vectors. Nonvanishing lets a pair of frames with the specified Gram extend locally by an orthonormal frame on their positive perpendicular. The remaining stabilizer is compact, so averaging the lift there preserves covariance. On compact subsets of this open the section and its inverse frame changes are bounded, giving compact tests after cutting. The difference of these tests has zero regular Jacquet integral. Applying the uniqueness argument of FBE14 permits evaluation at the *given* head.

Write $\gamma=a^{-1}\gamma_0(\zeta)b$ in the residual orbit. The same unitary map $U\mapsto\pi(a)U\pi'(b)^{-1}$ acts on both columns, for every bit. In the common intertwiner space let $E_\rho$ be the orthogonal compact type projections, retaining their full multiplicity spaces. Their sum is the identity. The squared terminal norm is the sum of the squared norms of the projected word vectors with the corresponding real squared type multipliers. Polarization gives the mixed pairing with those same multipliers and no cross terms between orthogonal types. The scalar in this evaluation is identical for both heads because the ratio of the last determinant square to the Gram is $|\zeta|^2/(|\zeta|^2-TT')$ irrespective of the head. The resulting measure is $(|\zeta|^2-TT')^{k-1}d^2\zeta$ on the positive region. The terminal vector of the positive cut is zero elsewhere. This recovers the last singleton including at prescribed reversing heads and for repeated compact types. Bounds for intermediate noncompact residual groups are required when passing from a matrix germ to a Hilbert-space germ at every preceding level. [Both site signs and the terminal compact projections](https://github.com/yuiyuiui/Natural-Language-Proof-Generalized-Riemann-Hypothesis/blob/405237610e58ab9d4a9d5d54d9a0548a0c44227c/sections/g-real-restriction.tex#L8304-L8420)

<!--
% END FBE17
-->

<!--
% BEGIN FBE18
-->

<span id="claim:FBE18"></span>For the compact cut there is an economical way to pass from the scalar stationary-phase estimate to the Hilbert estimate. It uses only **finiteness on smooth tests of fixed support** of the residual Bessel norm. The required analytic input in positive residual rank $\rho$ can be stated precisely. In the Witt model of $U(k+\rho,\rho+1)$ let $\Delta_j(g)$ be the exterior norm of the first $j+1$ vectors of the fixed isotropic frame after applying $g$, and put $\Xi(g)=\prod_{j=0}^\rho\Delta_j(g)^{-s_j}$, where $s_j^0=2$ for $j<\rho$, $s_\rho^0=k$, and $s_j=s_j^0-\varepsilon_j$ with small positive defects. Let $\ell$ be the real adjacent-root character on the unipotent radical. The two estimates used are
$$
 \int_G \|g\|^{-A}\|x^{-1}gy\|^{-A}\,dg\ \ll\ \Xi(x)\Xi(y),\qquad
 \int_N\Xi(n)(1+|\ell(n)|)^{-1/2}\,dn<\infty
$$
with the appropriate opposite frame on each side and sufficiently large $A$. They refer to the full residual unitary group, its two marked radicals and Frobenius matrix norm. Constants can depend on this fixed group and its marks. Jin gives a Heisenberg-coordinate proof of these estimates. In his recursion the squared exterior volumes are $d_j^2=L_jR_j+|B_j|^2$. Completing the square in the first complex coordinate and integrating then merges the first two shifts $\nu_0,\nu_1$ of the exponents and costs two planar integrals with exponents $2+\nu_0$ and $2+\nu_0+2\sum_{j>0}\nu_j$. Each is finite for exponent greater than two. At the last central coordinate the terminal integral reduces to the power $-(k-1)-\nu$ of $1+|v|^2/2$ on $\mathbb C^{k-1}$. For the phase-weighted integral the nonzero first coefficient at each rank is the pairing of the two Witt vectors, or the pairing with the negative mark at rank one. Taking the next defect at most $\min(\delta/8,\varepsilon_{\rm lower}/2)/(4\rho+4)$ permits the lower-rank character exponent $\delta/4$ at each descent, starting with $\delta=1/2$. These are estimates for one fixed residual norm, with no tower-uniform rate of convergence invoked. [Coordinate estimates, rank reduction and translation correlation](https://github.com/yuiyuiui/Natural-Language-Proof-Generalized-Riemann-Hypothesis/blob/405237610e58ab9d4a9d5d54d9a0548a0c44227c/sections/g-real-restriction.tex#L864-L1260)

To see precisely how they imply finiteness, unfold a squared orbital integral first against smooth frequency tests on the two characters. In the resulting ambient correlation average each unipotent variable under conjugation by the positive flag dilation of ratio $t$, using a smooth density supported in $1/2<t<2$. Each adjacent character entry scales by $t$, and its Haar Jacobian is a power of $t$. Integrating twice in $t$ by parts inserts a factor $(1+|\lambda\ell(n)|^2)^{-1}$ for frequency $\lambda$ in a neighbourhood of one. The derivatives of the test still have fixed compact support after these bounded conjugations. The two displayed estimates give an integrable majorant on both radicals, uniform for those frequencies. The unfolded formula therefore bounds the squared norm for almost every such frequency. For each regular orbit its integral is continuous in the frequencies by the fixed nonzero pivot bounds of FBE14. Fatou along a sequence approaching the prescribed frequencies gives the bound there. The two compact stabilizers have finite Haar volumes. In rank zero the compact angular integrals are bounded by a constant times $(1+|\zeta|)^{-A}$, which is square integrable in the terminal density for $A>k$. [Unfolding against frequencies](https://github.com/yuiyuiui/Natural-Language-Proof-Generalized-Riemann-Hypothesis/blob/405237610e58ab9d4a9d5d54d9a0548a0c44227c/sections/g-real-restriction.tex#L786-L862)

Here is a fixed-support continuity argument that avoids differentiating a Hilbert-space limit. For a compact set $K$ in the allowed residual group cut, consider the Fréchet space of smooth tests supported in $K$. The regular Jacquet transform to the orbital $L^2$ space is linear and is everywhere defined by the preceding estimate. Its graph is closed. Indeed convergence of smooth tests on the fixed support gives pointwise convergence at every regular orbit by its compact inverse coordinates. A sequence converging in $L^2$ has a subsequence converging almost everywhere, so the two limits agree. The closed graph theorem bounds the orbital norm by finitely many seminorms of the tests on $K$. Composing with any fixed word of group differential operators preserves this continuity. The residual form is a finite sum of pairings of such transforms, with one such differential on a column, hence is continuous for the same topology. In the Hilbert realization of its positive kernel the squared error of a column is its residual form evaluated twice on that error (conjugate the coefficients if the kernel is linear in the other slot). FBE14 bounds the error by $O(|\tau|)$ in each of the finitely many required group seminorms: differentiate the common compact coefficient in the residual group variables before stationary phase. The squared Hilbert error is consequently $O(|\tau|^2)$. The same argument works termwise at the top with its finite compact type projections. This transfers the coalescing germ into the actual cut kernel **under the displayed tail estimates**, including a head with internal zero minors. [Residual space and point-kernel norm](https://github.com/yuiyuiui/Natural-Language-Proof-Generalized-Riemann-Hypothesis/blob/405237610e58ab9d4a9d5d54d9a0548a0c44227c/sections/g-real-restriction.tex#L1358-L1398)

<!--
% END FBE18
-->

<!--
% BEGIN FBE19
-->

<span id="claim:FBE19"></span>To obtain the normalized germ in FBE15 from FBE14 and FBE18 one must also transport the densities. In the normalization of FBE9 put $u=s-1$, $i=b+u$, $q=g/(2\pi)$ for the marked modulus $g$, and $\lambda_{b,l}=q^{2r_S+3-2b-l}\mathrm i^{l-1}$. Use $\tau=\lambda_{b,u}/x$, $c=\lambda_{i,1}x^uD$, $z_{\rm st}=\lambda_{b,s}z$. Then $z_{\rm st}^s=(-1)^u c\tau^u$ is exactly $z^s=D$. The phase is fixed by $\lambda_{b,s}/\lambda_{b,u}=\mathrm i/q$, with conjugation for the Hilbert slot as in FBE15. For a block of length $l$ the density has the normalizing divisor $\beta_l=\prod_{j<l,\,j\ge1}(\kappa^{1-2j}/\pi)^{l-j}$, $\kappa=(q\Delta)^{-1}$, hence $\beta_s/\beta_u=\kappa^{-u^2}\pi^{-u}$. Put $m=k+2(r_S-i)+3$ in the lower levels. The split powers of absolute labels are $e_1=u(m+u-1)$, $e_2=m-2$, and the long power is $e_3=(u+1)(m+u-2)$. Direct subtraction gives $u-e_1+ue_2=-u^2$ and $e_3-u=se_2+u^2$. If the corresponding exponents of $q$ in the three $\lambda$'s are $\nu_1,\nu_2,\nu_3$, then $\nu_2=\nu_1-u-1$, $\nu_3=\nu_1-1$, and $\nu_1e_1+\nu_2(e_2+1)=\nu_3(e_3+1)+u^2$. Thus both normalized columns have the same multiplier of $|D_0|^{e_2}$ times the split $|\tau|^{u^2}$ and long $|z_{\rm st}|^{u^2}/s$ in FBE14. The factor $\pi^{-u}$ is accounted for by the difference of $u$ complex root coordinates in the orbital measures. Converting back leaves the long vector divided by $s|z|^u$, exactly the area normalization in FBE15. At the terminal level use $m=k+1$. The last factor is $(1-TT'/|x^uD|^2)^{(k-1-|w|)/2}$ on the split side and is $1+O_K(|x|^{-2u})$ uniformly on every fixed annulus. It does not change the leading germ or its error order. Any common zero prefix factor kills both columns. [Split and long column densities and terminal correction](https://github.com/yuiyuiui/Natural-Language-Proof-Generalized-Riemann-Hypothesis/blob/405237610e58ab9d4a9d5d54d9a0548a0c44227c/sections/g-real-restriction.tex#L1311-L1398)

<!--
% END FBE19
-->

## The two residual integrals

<!--
% BEGIN FBE20
-->

<span id="claim:FBE20"></span>Fix $G_r=U(k+r,r+1)$, $k\ge1$, in an orthonormal Witt basis for the Euclidean norm. Write $h(u,v)=u^*Hv$ with $H^*=H=H^{-1}$. Choose an orthonormal maximal isotropic frame $\phi$ extending the $r$ flag vectors by a null vector in the middle space, and put $\phi'=H\phi$. Thus $h(\phi'_i,\phi_j)=\delta_{ij}$. The frame index starts at zero. The volume of the first $j+1$ columns of $g\phi$ is $\Delta_j(g)$. Put $s^0=(2,\ldots,2,k)$, $\Xi_s=\prod\Delta_j^{-s_j}$, and use primes for the opposite frame. We first integrate on one radical fibre. In the decomposition $\mathbb Ce\oplus V'\oplus\mathbb Cf$ take $e=\phi'_0$, $f=\phi_0$. The radical $n(x,t)$ fixes $e$, sends $y\in V'$ to $y-h(x,y)e$ and sends $f$ to $f+x+(-h(x,x)/2+it)e$. Translation in these coordinates has real Jacobian one. Write $x=\sum_{i<p}(b_i\psi_i+a_i\psi'_i)+v$, where $p=r$, $\psi,\psi'$ are the two remaining null frames and $v\in\mathbb C^{l}$, $l=k-1$. Use the real coordinate $u=t+\Im\sum b_i\bar a_i$ and set
$$
 L_j=1+\sum_{i<j}|a_i|^2,\quad R_j=L_p+|v|^2+\sum_{i\ge j}|b_i|^2,\quad
 B_j=-|v|^2/2+iu-\sum_{i\ge j}b_i\bar a_i .
$$
The squared exterior volume $d_j^2$ of $n(x,t)(f,\psi_0,\dots,\psi_{j-1})$ is $L_jR_j+|B_j|^2$. The last $j$ columns have Gram determinant $L_j$. Subtract their first $j$ coefficients $b_i$ from the first column by column operations. The remaining part off $e$ is perpendicular to the last $j$ coordinate axes and has norm squared $R_j$. The projection of $e$ perpendicular to those columns has norm squared $1/L_j$. This gives the formula, including $j=0$.

Let $C_p(\nu)=\int\prod_{j=0}^p d_j^{-s^0_j-\nu_j}$ in this fibre and $K(q)=\int_{\mathbb C}(1+|z|^2)^{-q/2}\,d^2z$. The latter is $2\pi/(q-2)$ for $q>2$. For $p>0$, set $L=1+|a_0|^2$. The identity $d_0^2=L|b_0-a_0B_1/L|^2+d_1^2/L$ integrates the $b_0$ variable, giving $K(2+\nu_0)L^{-1+\nu_0/2}d_1^{-\nu_0}$. In the remaining $a_i,b_i,v$ substitute $\sqrt L$ times new variables, and in $u$ substitute $L$ times the new real variable. Every remaining $d_j$ acquires a factor $L$. The Jacobian is $L^{2p-1+l}$. The integral in $a_0$ and the lower integral therefore give
$$
 C_p(\nu)=K(2+\nu_0)K(2+\nu_0+2\sum_{j>0}\nu_j)
 C_{p-1}(\nu_0+\nu_1,\nu_2,\ldots,\nu_p).
$$
At $p=0$, $d_0^2=(1+|v|^2/2)^2+u^2$. Integration in $u$ leaves a constant times $(1+|v|^2/2)^{-l-\nu_0}$, integrable on $\mathbb C^l$ for $\nu_0>0$, also when $l=0$. Consequently a sufficient convergence criterion is
$$
 \sum_{i=0}^j\nu_i>0\ (0\le j\le p),\qquad
 \sum_{i=0}^j\nu_i+2\sum_{i>j}\nu_i>0\ (0\le j<p).
$$
These are precisely the inequalities used by the recursion after each merge. [Heisenberg coordinates and shifted integrals in Jin's proof](https://github.com/yuiyuiui/Natural-Language-Proof-Generalized-Riemann-Hypothesis/blob/405237610e58ab9d4a9d5d54d9a0548a0c44227c/sections/g-real-restriction.tex#L978-L1047)

<!--
% END FBE20
-->

<!--
% BEGIN FBE21
-->

<span id="claim:FBE21"></span>Put $D_j(g)=\det(h(\phi'_a,g\phi'_b))_{a,b\le j}$ and $P_s=\prod |D_j|^{-s_j}$ on the conull locus of nonzero minors. Let $s_j=s^0_j-\varepsilon_j$ with $0<\varepsilon_j\le1/10$. We prove
$$
 I_r(A)=\int_{G_r}\|g\|_{\rm F}^{-A}P_s(g)\,dg<\infty
 \qquad(A\ge2(k+r)(r+1)+1).
$$
The compact group $K=G_r\cap U(k+2r+1)$ acts transitively on orthonormal isotropic frames. Their projections to the positive and negative summands are orthogonal frames of length $1/\sqrt2$, so each can be completed to a unitary basis. Gram–Schmidt on $x\phi',y\phi'$ gives triangular matrices whose first $j+1$ diagonals have product of absolute value $\Delta'_j(x),\Delta'_j(y)$. For every nonnegative $K$-bi-invariant $F$, Haar invariance then gives
$$
 \int F(g)P_s(x^{-1}gy)\,dg=
 \Xi'_s(x)\Xi'_s(y)\int F(g)P_s(g)\,dg.
$$
This identity also holds before knowing finiteness, by change of variables for nonnegative integrands.

At rank zero the sign coordinates of $g\phi'$ are $(v,b)$ with $\|v\|=|b|$. The left compact average of $|D_0|^{-s_0}$ is at most $C|b|^{-s_0}$. For $k=1$ this is the integrability of $|1-e^{it}|^{-s_0}$ for $s_0<1$. For $k\ge2$ the first coordinate $z$ of a uniform complex unit vector has density $(k-1)(1-|z|^2)^{k-2}/\pi$ on the disc. Near $1$ it is at most $C|1-z|^{k-2}$, which suffices for $s_0<k$. A right compact average makes $b$ a constant of modulus $\ge1/\sqrt2$ times $1-az$ with $0\le a\le1$, since the last row of $g$ has negative norm one. This inverse-power average is bounded uniformly, using $|1-az|\ge a|1-z|$ for $a\ge1/2$. Projecting $G_0$ to the negative unit hyperboloid has compact fibres. In its coordinates the invariant measure is proportional to $\delta(\|v\|^2-|b|^2+1)\,dv\,d^2b$. The remaining integral is bounded by $\int_0^\infty t^{2k-1}(1+t)^{-A}\,dt$.

For $r>0$ put $d=\dim_{\mathbb C}V'=2r+k-1$. On the cell $c=h(e,ge)\ne0$ write $g=n_L^{-1} w_c m n_R$, where $w_ce=cf,\ w_cf=\bar c^{-1}e$, $m\in G_{r-1}$ acts in $V'$, and $w_c$ is the identity there. The vector $ge$ determines $c,n_L$ by isotropy, and the stabilizer of $e$ is $G_{r-1}\ltimes n(V',\mathbb R)$. The complement is the zero set of a nonzero analytic matrix entry. In the cone measure, the coordinates $Y=cx$ and $a=c(-h(x,x)/2+it)$ in $ae+Y+cf$ have Jacobian $|c|^{2d+2}$ before imposing isotropy, whose real equation contributes $|c|^{-2}$. Thus Haar density is a constant times $|c|^{2d}d^2c\,dn_L\,dm\,dn_R$. The minors are $c$ and $cD_{j-1}(m)$ by triangularity of the two radicals on the primed prefixes.

Write $b=2d+1$. Independently of $c,m$ one has
$$
 \int\|w_cm n(x,t)\|_{\rm F}^{-A}\,dx\,dt
 \ll \|m\|_{\rm F}^{b-A}\min(|c|^{-b},|c|^{-1}).
$$
Indeed the displayed matrix contains entries bounding $\|m\|_{\rm F}$, $|c||t|$, and both $|c|\|x\|$ and $\|mx\|$. Split $A$ into a power $>2d$ for $x$ and a power $>1$ for $t$. Using $\|mx\|$ in the second version preserves Lebesgue measure because $|\det m|=1$. For the fixed left radical put $D=\|n_L^{-1}f\|$ and let $d'_j$ be the exterior volume of $n_L^{-1}$ on $(f,\psi'_0,\dots,\psi'_{j-1})$. Rotate its first vector to $Df$ by $K$. Factoring the result times $w_c$ by the stabilizer of $e$ replaces $(c,m)$ with $(cD,m_0m)$. The extra right radical translates $n_R$ with Jacobian one. Orthogonal projection to the middle space after removing the first column gives $\Delta'_{j-1}(m_0)=d'_j/D$. Apply the right bound and the compact averaging identity at rank $r-1$. The exponent there is $A-b\ge 2(k+r-1)r+1$.

Set $S=\sum s_j$. On changing $cD$ to the radial variable, the scalar factor is $D^{-(2d+2-S)}$. The integral in $c$ converges at infinity for $S>1$ and at zero for $S<2d+1$, both valid here. Multiplication by $\prod_{j>0}(d'_j/D)^{-s_j}$ leaves the integral $C_r(\nu)$ of FBE20 with $\nu_0=\varepsilon_0+2\sum_{j>0}\varepsilon_j$ and $\nu_j=-\varepsilon_j$ for $j>0$. Inversion of the radical preserves measure and conjugation by the middle form interchanges its two frames. The first partial sums of $\nu$ are positive, and each second expression in FBE20 equals $\sum_{i=0}^{j}\varepsilon_i$. This finishes the induction. Finally $\prod|D_j(g)|^{s_j}\ll\|g\|_{\rm F}^{(r+1)(k+r)}$ by the exterior norm bound. Apply compact averaging to $xH,yH$ and compare the translated inverse norm with $P_s$. Unitary invariance of the Frobenius norm gives the first estimate of FBE18 for all $x,y$. [Rank induction and compact averaging](https://github.com/yuiyuiui/Natural-Language-Proof-Generalized-Riemann-Hypothesis/blob/405237610e58ab9d4a9d5d54d9a0548a0c44227c/sections/g-real-restriction.tex#L885-L1163)

<!--
% END FBE21
-->

<!--
% BEGIN FBE22
-->

<span id="claim:FBE22"></span>For $p>0$ let $F=\prod d_j^{-s^0_j+\varepsilon_j}$ in FBE20. Consider any complex linear form $Z$ in $(a_i,b_i,v)$ whose coefficient of $b_0$ is $\eta\ne0$. For real $c$, $0<\delta\le1/2$ and $0<\gamma\le\delta/8$, the following estimate is uniform in $Z,c$:
$$
 \int F(1+|c+2\Im Z|)^{-\delta}
 \ll |\eta|^{-\gamma}(1+|c|)^{-\delta/4}
 \qquad\left(\varepsilon_0+2\sum_{i>0}\varepsilon_i<\gamma/2\right).
$$
Here and below the measure includes the central variable. For a polynomial $P$ of degree at most two on $[1,2]$, if $|P|\le v$ on a set of length $h$, choose three points of the set at distances at least $h/6$ apart. Quadratic interpolation bounds each coefficient by $Cv/h^2$. With $M$ the largest coefficient modulus, split at $v=\sqrt M$ when $M\ge1$. The mean of $(1+|P|)^{-\sigma}$ is $\ll_\sigma(1+M)^{-\sigma/2}$ for $0<\sigma\le1/2$. First rotate all complex variables by $(1+it)^2/(1+t^2)$ for $1\le t\le2$. All $d_j$ and the measure are invariant. The numerator of the resulting real polynomial phase has coefficient norm comparable to $\max(|Z|,|c|)$, since the coefficients separate $\Re Z,\Im Z,c$. The average is at most $C(1+|c|)^{-\delta/4}(1+|Z|)^{-\delta/4}$. Next replace $(a_0,b_0)$ by $(ta_0,b_0/t)$ and keep $u$ fixed. The products $b_i\bar a_i$ are unchanged, and $L_j,R_j$ change by bounded factors. The Jacobian is one. The polynomial $tZ(ta_0,b_0/t)$ has constant coefficient $\eta b_0$. The second average costs at most $C|\eta b_0|^{-\gamma}$.

It remains to show $\int F|b_0|^{-\gamma}<\infty$. For $0<e<\gamma<2$,
$$
 \int_{\mathbb C}(|b-h|^2+D^2)^{-1+e/2}|b|^{-\gamma}\,d^2b
 \ll (|h|^2+D^2)^{-(\gamma-e)/2}\quad(D>0).
$$
Normalize $|h|^2+D^2=1$. The tail has exponent $-2+e-\gamma<-2$. On a bounded disc either $D\ge1/2$, or the possible singularities at $0,h$ are separated. Their individual powers are locally integrable uniformly. Apply this bound to the square in FBE20 with $e=\varepsilon_0$. Integration in $b_0$ leaves at most $CL^{-1+\gamma/2}d_0(0)^{-(\gamma-e)}$ times the other factors, where $d_0(0)$ sets $b_0=0$ only. Put $\alpha=\gamma/2-e>0$. Use $d_0(0)\ge d_1/\sqrt L$ for the power $\alpha$, and $d_0(0)\ge|u-c_1|$ for the power $\gamma/2$, with $c_1=\Im\sum_{i\ge1}b_i\bar a_i$. For fixed complex variables the rest of the $u$ integrand has logarithmic derivative $O(1/L)$, since each remaining $d_j^2$ is $A_j^2+(u-c_j)^2$ with $A_j\ge L$. On $|u-c_1|\le L$ that weight varies by a bounded factor and the mean of $|u-c_1|^{-\gamma/2}$ is $O(L^{-\gamma/2})$. The same estimate holds pointwise outside the interval. The last integral is thus bounded by a constant times the integral of
$$
 L^{-1+\alpha/2}d_1^{-\alpha}\prod_{j>0}d_j^{-s^0_j+\varepsilon_j}.
$$
Scaling the remaining variables as in FBE20 gives $K(2+\alpha-2\sum_{j>0}\varepsilon_j)C_{p-1}(\alpha-\varepsilon_1,-\varepsilon_2,\ldots,-\varepsilon_p)$. Both factors are finite by that claim because $\alpha>2\sum_{j>0}\varepsilon_j$. [Character averaging on a radical fibre](https://github.com/yuiyuiui/Natural-Language-Proof-Generalized-Riemann-Hypothesis/blob/405237610e58ab9d4a9d5d54d9a0548a0c44227c/sections/g-real-restriction.tex#L1124-L1219)

<!--
% END FBE22
-->

<!--
% BEGIN FBE23
-->

<span id="claim:FBE23"></span>Write $N_r$ for the radical preserving the first $r$ lines of the opposite flag. Its Bessel character $\ell_z$ is twice the imaginary part of the sum of the neighbouring flag entries, terminated by the negative mark $z$. We prove $\int_{N_r}\Xi_s(n)(1+|\ell_z(n)|)^{-\delta}\,dn<\infty$ for a positive bound on all the defects depending only on $k,r,\delta$. At $r=0$ the integral is one with mass-one Haar measure. At positive rank write $n=n(x,t)m$ with $m\in N_{r-1}$. Product measure is Haar since $x\mapsto mx$ has absolute determinant one. The outer radical contributes $2\Im h(mv_0,x)$ to $\ell_z(m)$, where $v_0$ is the first lower primed Witt vector if $r>1$ and is $z$ if $r=1$. This is the $e$-coordinate of the new neighbouring entry in $n(x,t)m$.

On the lower frame write $m\psi=\kappa\psi T$ by Gram–Schmidt with $\kappa$ compact and $T$ upper triangular. Rotate $x$ back by $\kappa^{-1}$. The $j$th exterior volume for $j\ge1$ is $\Delta_{j-1}(m)d_j$, and the zeroth is $d_0$, by the determinants on the prefixes. In the resulting phase the modulus of the $b_0$ coefficient is
$$
 \frac{|h(v_0,\psi_0)|}{\Delta_0(m)}.
$$
Indeed $\kappa\psi_0=m\psi_0/\Delta_0(m)$ up to phase and $m$ preserves $h$. The numerator is one for two paired Witt vectors. At rank one it is positive because the orthogonal complement of a negative vector in signature $(k,1)$ is positive definite. FBE22 now leaves the lower integral with exponents $(s_1-\gamma,s_2,\dots,s_r)$ and character exponent $\delta/4$. Given an admissible lower defect bound $e'$, choose $\gamma=\min(\delta/8,e'/2)$ and take all $\varepsilon_j\le\min(e'/2,\gamma/(4r+4),1/10)$ positive. This ensures the strict fibre inequality and leaves every lower defect admissible. The bounds may depend on the fixed mark, but their exponent choices precede it. For a compact marking stabilizer $w$, write $nw=w(w^{-1}nw)$. Exterior norms of $w^{\pm1}$ are bounded uniformly and conjugation preserves the Haar measure and $\ell_z$. Taking $\delta=1/2$ gives the second estimate of FBE18 on both original residual subgroups with the same defects as FBE21. In rank zero the Bessel stabilizers are compact, and its orbit density is $(|\zeta|^2-TT')^{k-1}$, integrable against a coefficient squared of decay order $A>k$. [Induction with the negative mark and the stabilizer](https://github.com/yuiyuiui/Natural-Language-Proof-Generalized-Riemann-Hypothesis/blob/405237610e58ab9d4a9d5d54d9a0548a0c44227c/sections/g-real-restriction.tex#L1204-L1260)

<!--
% END FBE23
-->

<!--
% BEGIN FBE24
-->

<span id="claim:FBE24"></span>The estimates give continuity in a norm independent of the support of a smooth residual test. For compact tests $u,v$ put $\|u\|_{A,j}=\max_{|D|\le j}\sup_g\|g\|_{\rm F}^A |Du(g)|$, allowing mixed left and right invariant derivatives in a fixed basis. For translations $h_1,h_2$ the absolute correlation of the tests is at most $\|u\|_{A,0}\|v\|_{A,0}C\Xi_s(h_1)\Xi_s(h_2)$ by FBE21. To integrate against the two characters average the dilation of each radical by its diagonal flag element at scale $a\in(1/2,2)$ with smooth mass-one density. Its weights on the first flag are $a^r,\ldots,a$, on the dual flag their inverses, and on the middle space one. It multiplies the marked adjacent character by $a$, fixes the marking stabilizer and changes Haar measure by a fixed power of $a$. After changing the ambient group variable, the dilations act on the tests by left and right translation by compact families of matrices. Integrate by parts with $1-\partial_a^2$ in each scale. The absolute majorant is then
$$
 C\|u\|_{A,4}\|v\|_{A,4}
 \prod_{j=1,2}\frac{\Xi_s(h_j)}{1+|\ell_j(n_j)|^2}
$$
uniformly for both frequencies in $[1/2,2]$ (enlarging $C$). Lie derivatives of order at most four suffice and powers of $\|g\|_{\rm F}$ are comparable under those bounded translations. FBE23 integrates this bound.

For precision, first smear the two frequencies by smooth product test functions supported in that interval. Expand the orbital square on the regular cell, disintegrate Haar measure there and change the two copies of each unipotent variable to a base point and its difference. The smearing introduces the Fourier transforms of the two tests in those differences. Their decay to order two and FBE21–23 make the unfolded integral absolutely convergent. Equivalently the identity follows first with compact domains and then by Fubini under this majorant. The resulting frequency distribution equals the continuous correlation obtained by integration by parts. Thus the squared orbital norm agrees with it almost everywhere. On each regular marked orbit, the fixed nonzero pivots recover the radical coordinates of a compactly supported coefficient, so the orbital integral is pointwise continuous in the frequencies. Fatou along regular frequencies tending to $(1,1)$ gives $\|Ju\|_{L^2}\le C\|u\|_{A,4}$ for the prescribed pair of characters. Polarization or Cauchy–Schwarz gives the mixed bound. Composing a word of length $h$ whose letters each have at most two matrix-entry multipliers and at most $2r+k+1$ invariant derivatives uses $\|u\|_{A+2h,4+(2r+k+1)h}$, since invariant derivatives of an entry are linear combinations of entries. This supplies FBE18 with a support-independent continuity estimate as well as its compact-support conclusion. [Dilation, disintegration and recovery at the specified frequencies](https://github.com/yuiyuiui/Natural-Language-Proof-Generalized-Riemann-Hypothesis/blob/405237610e58ab9d4a9d5d54d9a0548a0c44227c/sections/g-real-restriction.tex#L789-L862)

<!--
% END FBE24
-->

## Removing compact support at a positive Gram threshold

<!--
% BEGIN FBE25
-->

<span id="claim:FBE25"></span>Fix the selected real place, a positive Gram threshold $\epsilon$ and a marked head with nonzero determinant. Let $d=k+2r+1$, $N=20(r+1)$ and $R(g)=\max(1,\|g\|_{\rm F})$. Multiply the coefficient $F_\epsilon=\chi(G/\epsilon)F$ by $\eta(R(g)^2/M^2)$, with $\eta=1$ up to one and zero from four onwards. The Frobenius norm is already $\ge1$ on this unitary group. An invariant derivative of any order of $\|g\|_{\rm F}^2$ is a polynomial homogeneous of degree two in entries and conjugates. In every differentiated cutoff term the powers $M^{-2j}$ cancel the growth of the $j$ polynomial factors on $M\le R(g)\le2M$. The undifferentiated difference from one and all its differentiated terms vanish for $R<M$. Thus, for any weighted finite jet norm of FBE24,
$$
 \|(\eta(R^2/M^2)-1)u\|_{a,b}\le C_b M^{-1}\|u\|_{a+1,b}.
$$
For fixed $\epsilon$, all constant-order invariant derivatives of the original $F$ have the same available decay exponent. Such a derivative moves to one of the smooth representation vectors. The translated compact-finite vector and its derivatives remain finite sums of translates of compact-finite vectors. Apply the smooth coefficient estimate with the original gap to these pairs. In particular the selected gap $h\ge d^{19}/2$ permits every exponent strictly less than $h+d-1$ in that estimate. The Gram polynomial is the square of the last marked determinant minus $TT'$ times the square of the preceding one. Its degree in entries and conjugates is at most $2(r+1)$. Applying $j$ invariant derivatives to $\chi(G/\epsilon)$ costs at most $2(r+1)j$ powers of $R$, with a constant depending on $\epsilon,j$ and the marks. This proves the extra power required under the compact exhaustion. [Smooth discrete-series vectors at the selected gap](SPECTRAL_SMOOTH_DECAY.md) · [The original positive cutoff and order of approximations](https://github.com/yuiyuiui/Natural-Language-Proof-Generalized-Riemann-Hypothesis/blob/405237610e58ab9d4a9d5d54d9a0548a0c44227c/sections/g-real-restriction.tex#L4737-L4757)

Here is a direct check that taking the residual slice preserves this convergence for each fixed head. Use the group coordinates $g=R_1^{-1}D(P,\gamma)R_2$ where the leading block of the big cell is $P=g_{31}$, $R_j$ are three-block upper unitriangular, and the middle of $D$ is $\gamma$. Localize $|\det P|$ to a compact annulus about its prescribed value. With $i$ the rank of $P$, $\|P^{-1}\|\ll R^{i-1}$. The independent off-diagonal coordinates of $R_1,R_2$ are recovered from $-g_{21}P^{-1}$, $P^{-1}g_{32}$, $g_{11}P^{-1}$ and $P^{-1}g_{33}$. Recovering the last corner uses at most one product of two of these quantities (the skew-Hermitian coordinate subtracts a quadratic expression). Thus $\|R_j^{\pm1}\|\ll R^{2i}$ and $\|\gamma\|\ll R^{4i+1}$. The head unipotent entries are minors of the head divided by fixed pivot products after its fixed permutation; the adjoining blocks are obtained by one Schur complement. All these free variables are bounded by $C R^{r+1}$. At a fixed head no inverse of a vanished *internal* leading minor is used. All constants in these coordinate bounds may depend on the head.

For example, to estimate a sliced column with $A$ powers of residual decay and $b$ residual invariant derivatives, let $z$ collect all real integration coordinates, of dimension at most $8d^2$. This bound follows by counting the two outer triangular matrices and the two head triangular matrices even as full complex $d$ by $d$ matrices. Lebesgue measure in the independent unipotent entries is Haar, since the cross terms in triangular multiplication have Jacobian one. Additional fixed pivot powers in the density are constants on the fixed head or bounded on its determinant annulus. Here $1+|z|\ll R^{2(r+1)}$. Therefore a reserve of
$$
 (4r+1)A+2(r+1)(8d^2+1)
$$
powers bounds $R(\gamma)^A(1+|z|)^{8d^2+1}$. Residual differentiation can use right translation at $\gamma$ inside the factorization. In the ambient coefficient its direction is conjugated by the fixed $R_2$ in that integration, costing at most $4r$ powers per derivative. For a head word of length at most $N$ its group differential order is at most $Nr$ and its polynomial degree at most $Nr(r+1)$: each head cofactor of size $i$ uses at most $i$ invariant derivatives and at most $i+i^2$ coefficient entries from the two triangular substitutions. These estimates also follow by expanding the finite column determinant. Constants depending on the finitely many word parameters are harmless at this step. The surviving head phases have modulus one. Applying the pointwise bound and then integrating $(1+|z|)^{-8d^2-1}$ proves convergence in the residual seminorm. At the compact final factor only the head variables and the same Schur-complement bound occur.

For the norms in FBE24 it suffices to take $A=2(k+r)(r+1)+1+2N$ and $b=4+dN$. Even reserving the larger $A\le 2668d^6$, $b\le91d^3$ used in the matrix-germ computation, the total cost including Gram derivatives, word coefficients and one extra power is bounded by
$$
 (4r+1)A+2(r+1)(8d^2+1)+4rb+Nr(r+1)+2(r+1)(b+Nr)+1 .
$$
It is less than $12000d^7$ for $r+1\le d$, $N\le20d$ and $d\ge3$, hence less than $d^{19}/2$. At $r=0$ there are no head radicals or preterminal words to estimate and the rank-zero bound of FBE23 applies directly. At a nonempty fixed reversing head, apply FBE14 to each compact approximation before taking the pointwise limit in the finite Gram comparisons. The constants of stationary phase need not be bounded as $M$ grows. On each fixed fibre the residual cutoff stays positive since its Gram is the ambient Gram divided by $|\det P|^2$. FBE24 gives convergence of the mixed pairings, using the same exhaustion on both columns. For a finite collection of prefixes every entry therefore converges. A convergent subsequence of the word probabilities in their finite simplex gives the same limiting probabilities for every finite test, since entrywise convergence already holds for each prescribed test along the full sequence. [Block inverses and the fixed determinant](https://github.com/yuiyuiui/Natural-Language-Proof-Generalized-Riemann-Hypothesis/blob/405237610e58ab9d4a9d5d54d9a0548a0c44227c/sections/g-real-restriction.tex#L675-L754) · [Orders and norms in the compact exhaustion](https://github.com/yuiyuiui/Natural-Language-Proof-Generalized-Riemann-Hypothesis/blob/405237610e58ab9d4a9d5d54d9a0548a0c44227c/sections/g-real-restriction.tex#L4834-L4895)

<!--
% END FBE25
-->

<!--
% BEGIN FBE26
-->

<span id="claim:FBE26"></span>At $G\downarrow0$ an estimate with a constant depending on the Gram threshold cannot dominate the differentiated family. For the actual section of the selected coefficient the following computation isolates the estimates needed in the two limiting operations. In the frame of the level-zero proof put $G=|D_r|^2(|\zeta|^2-TT')$, $D=D_r\zeta$, $W=|D|^2/G$, $m=h+1\le N$ for the current word and $\sigma=4N$. Its pointwise squared component densities have the form $W^m c_a(Y)$, with bounded continuous $c_a$ on the parameter box $J$. Suppose the determinant-cleared word has an envelope $|D|^m|(g_Y X)_a|\le B_a$ with $B_a\in L^2(d\mu_0)$ throughout that box. For $\theta_\epsilon=(G/(G+\epsilon))^\sigma$,
$$
 \theta_\epsilon W^m c_a(Y)|(g_YX)_a|^2\le
 (\sup_J c_a)\epsilon^{-m} B_a^2.
$$
This uses $\theta_\epsilon G^{-m}\le\epsilon^{-m}$ for $m\le\sigma$. It suffices for continuity at fixed $\epsilon$. For differentiated removal let $Q_Y(s)=G^{-s}g_Y(G^s X)$ and $D_G=G\partial_G$. Locality and the finite order give $g_Y(\phi X)=\sum_{j=0}^{r+1}(D_G^j\phi)Q_Y^{(j)}(0)/j!$ by testing on $G^s$. With the original adjoint and parameter shift on the positive boxes, let $E_\epsilon$ be the maximum of the regulated energy divided by $|P(Y)|$. The comparison of the two weights and the triangular residue frame gives $\|Q_Y(s)\|_{\theta_\epsilon,Y}^2\le C_7 E_\epsilon |P(Y)|$ for $Y+s\in J$. Markov's inequality on the interval of length $L$ bounds the $j$th derivative at zero by $(2(r+1)^2/L)^j$ times its Hilbert supremum. The function $\theta_\epsilon(e^{v+z})/\theta_\epsilon(e^v)$ has modulus at most $e$ on the complex disc $|z|\le1/(4\sigma)$, so $|D_G^j\theta_\epsilon|/j!\le e(4\sigma)^j\theta_\epsilon$. In the adjoint identity the nonconstant terms now total at most
$$
 |P(Y)|E_\epsilon\,e\sqrt{C_7}\sum_{j\ge1}(8\sigma(r+1)^2/L)^j.
$$
For $L\ge16\sigma(r+1)^2(1+2e\sqrt{C_7})$ the sum costs at most half of $|P(Y)|E_\epsilon$. In using the adjoint one may first multiply $\theta_\epsilon$ by $\chi(G/\delta)$. Its positive logarithmic derivatives away from those of $\theta_\epsilon$ are bounded on the shrinking annulus and vanish pointwise. The fixed-$\epsilon$ weighted norms give dominated convergence there. Taking the supremum gives $E_\epsilon\le 2I$ for the old energy $I$. Fatou and Markov now give $L^2$ bounds for all the shift jets before the cutoff. Since $D_G^j\theta_\epsilon\to0$ for $j>0$, Cauchy–Schwarz and those unregulated jets pass the adjoint identity to the limit. The level-zero proof then interpolates the finite word grid to the actual signed evaluations. Thus one only needs the envelope and the transfers in this calculation for the original determinant-cleared words. Its fixed-$\epsilon$ majorant alone has no uniform integrable limit. [Level-zero adjoint and interpolation](SPECTRAL_LEVEL_ZERO_AND_CUTOFFS.md) · [Transfers and determinant-cleared word bounds](https://github.com/yuiyuiui/Natural-Language-Proof-Generalized-Riemann-Hypothesis/blob/405237610e58ab9d4a9d5d54d9a0548a0c44227c/sections/g-real-restriction.tex#L7193-L7277)

<!--
% END FBE26
-->

<!--
% BEGIN FBE27
-->

<span id="claim:FBE27"></span>The compact exhaustion also converges at an individual regular terminal orbit with nontrivial stabilizer. Let $g_0$ represent the orbit, with its fixed monomial cross Gram. For the left radical put $H=N\cap g_0Ng_0^{-1}$ and choose complement root coordinates so that $u=\rho s$, $\rho\in H$. Such coordinates are obtained by eliminating the free entries successively by unitriangular row operations, with diagonal one. They have product Haar measure. In the second radical write $v=g_0^{-1}\rho^{-1}g_0 u'$. Put $Z=s^{-1}g_0v=u^{-1}g_0u'$ and $X=R(s)+R(v)$, with the fixed unitary Frobenius norms of FBE25. Then
$$
 X\le C_{g_0}R(Z)^{6(r+1)^2},\qquad R(u')\le C_{g_0}R(u)X^2.
$$
For the first bound form the cross Gram on the two frames. Its lower and upper unitriangular factors are uniquely recovered in the complement coordinates from minors of sizes at most $r+1$ divided by fixed products of the monomial pivots. This is Gaussian elimination in the pivot row order, including when an unpermuted principal minor vanishes. Each entry thus has size $\ll_{g_0} R(Z)^{r+1}$. The finite inverse series of a unitriangular matrix of size $r+1$ costs at most $r$ such factors in each entry. These matrices bound $s^{-1}$ on the first fixed frame and, from $s^{-1}g_0=Zv^{-1}$, on the second by $\ll_{g_0}R(Z)^{1+r(r+1)}$. The two frames span a nondegenerate space with positive definite orthogonal complement on this regular orbit. Pairing with their images bounds the projection of $s$ on that span, using its fixed Gram inverse. The complementary norm of $s x$ for a Euclidean unit vector $x$ is bounded by this projection and the fixed bound on $|h(x,x)|$, since $h(sx,sx)=h(x,x)$. Thus the same polynomial bound controls $s$; $v=g_0^{-1}sZ$ costs one additional power, within the stated exponent. For the second inequality use $\rho=us^{-1}$ and submultiplicativity. In these coordinates inversion preserves the Frobenius norm of a unitary matrix.

Take a decay exponent $A$ and set $a=A/(6(r+1)^2)$, $b=4(r(2r+k+1)+1)$, $M=a-2b$. The gap in FBE25 allows $a\ge4b$. Normalize the stabilizer integral by inserting $R(u)^{-M}/\int_H R(\tau u)^{-M}\,d\tau$. It has mass one on each stabilizer orbit and its denominator is at least $R(s)^{-M}\int_H R(\tau)^{-M}\,d\tau$. Both this last integral and $\int_N R(\tau)^{-b}\,d\tau$ converge: there are at most $2r(2r+k+1)$ real free root coordinates, bounded by a constant times the matrix norm, with product Lebesgue measure. The absolute value of the normalized terminal integrand is consequently at most
$$
 C_{g_0} R(u)^{-M}X^{M-a}
 \le C'_{g_0} R(u)^{-(a-3b)} R(u')^{-b}.
$$
Both factors are integrable. Compact stabilizer integrations only change constants. The integrand converges pointwise for the common compact exhaustion and, for the undifferentiated terminal coefficient, for $\chi(G/\epsilon)\to1$ at positive Gram. Dominated convergence proves convergence at the prescribed point. A terminal point with empty relevant orbit has zero integral. No limiting supremum over different orbits is involved. [Fixed-orbit stabilizer and majorant](https://github.com/yuiyuiui/Natural-Language-Proof-Generalized-Riemann-Hypothesis/blob/405237610e58ab9d4a9d5d54d9a0548a0c44227c/sections/g-real-restriction.tex#L4758-L4833) · [Two-frame coordinate recovery](https://github.com/yuiyuiui/Natural-Language-Proof-Generalized-Riemann-Hypothesis/blob/405237610e58ab9d4a9d5d54d9a0548a0c44227c/sections/g-real-restriction.tex#L8785-L8866)

<!--
% END FBE27
-->

## Determinant-cleared differentials of the original coefficient

<!--
% BEGIN FBE28
-->

<span id="claim:FBE28"></span>There is a way to test unregulated $L^2$ using only group operators with polynomial coefficients. Put $t=TT'$, $H_0=|\zeta|^2-t$, $D_r=\prod c_j$, $D=D_r\zeta$. Let $(a_Y,b_Y)^t$ be the first column of the positive site product in FBE12. Use a superscript $\vee$ for the product with $p_j=c_j\partial_{c_j}$ replaced by $-\bar p_j$ and the $c_j$'s in the off-diagonal entries conjugated. In the terminal intertwiner frame with $\nabla_\pi=\partial_\zeta+\alpha_\pi\bar\zeta/H_0$, set
$$
 X=D_ra_Y,\quad Z=\overline{D_r}H_0(\ell_0(Y)a_Y+b_Y),\qquad
 X^\vee=\overline{D_r}a_Y^\vee,\quad
 Z^\vee=D_rH_0(m_0(Y)a_Y^\vee+b_Y^\vee),
$$
where $\ell_0=-\nabla-(Y+1/2)\bar\zeta/H_0$ and $m_0=-\nabla^*-(Y-1/2)\zeta/H_0$. We explain the group realization used for these four expressions.

Write $E=(e_1,\ldots,e_r)$, $F=(f_1,\ldots,f_r)$ for the paired flags, and $(w_0,\ldots,w_k)$ for a basis of the residual space. Orient the full basis as $(E,w_0,\ldots,w_k,f_r,\ldots,f_1)$. In the ordered minor convention of FBE12 contract $\Delta_{E,P}(Y+(d-1)/2)$ against $\det(h(gp_b,e_a))$ and sum over $r$-element basis lists $P$ in basis order. The reflected contraction uses $\Delta_{P,F}(Y-k/2-1)$ against $\det(p_b^*(g^{-1}e_a))$. After evaluation on the regular section only $P=E$ or $P=F$, respectively, survives. The first-column expansion leaves the diagonal Euler term and one adjacent character term. Expanding its cofactor on the exposed row gives the coefficient $-c_{j+1}/c_j$. Conjugating by the square root of the section density cancels the remaining half-dimension shift, exactly as in FBE12. Thus the suffix recursion is $P_j=(Y+p_j)P_{j+1}-(c_{j+1}/c_j)P_{j+2}$ with end values $1,Y+p_r$. The reflected recursion conjugates the quotient and replaces $p_j$ by $-\bar p_j$. These give $X,X^\vee$.

For the marked contraction let $I_i=(E,w_0,\ldots,\widehat{w_i},\ldots,w_k)$ and $J_i=(w_0,\ldots,\widehat{w_i},\ldots,w_k,f_r,\ldots,f_1)$. The multiplier for $\Delta_{I_i,P}(Y+(d-1)/2)$ is the full determinant with columns $(g^{-1}e_r,\ldots,g^{-1}e_1,g^{-1}z,P)$ times $-(-1)^{r(r+k+2)+i}h(w_i,z')$. For the reflected $\Delta_{P,J_i}(Y+k/2-1)$ use the covector determinant $(h(g\,\cdot,e_a)_a,h(g\,\cdot,z),P^*)$ times $-(-1)^i z'_i$. Sum over $i$ and $|P|=r+k$. Each multiplier is placed to the left of the differentiations. The two marking groups preserve the flag wedges and preserve the extra marked vector modulo that flag. On the right, conjugating a derivative conjugates its row and column lists; the determinant of the conjugating matrix from the exterior volume is canceled by its inverse in the complementary determinant. These contractions thus preserve the required covariance before applying $J$. Each has differential order at most $d$ and multiplier degree at most $r+1$ since $g^{-1}=Hg^*H$.

On the section the same suffix recursion reaches the last flag coordinate. The diagonal terms are $-(Y+p_r)q^0_{10}$ and $-(Y-\bar p_r)q^0_{01}$. In the other term the two contracted middle vectors occur as their alternating two-vector and two-covector wedges, exactly the double cofactor for $q^0_{11}$ in FBE12. Its scalar is $-1/c_r$, respectively $-1/\bar c_r$; reversing the two wedge orders in the reflected calculation changes the sign twice. Including the outside signs gives $\overline{D_r}(q^0_{10}a_Y+q^0_{11}b_Y)$ and $D_r(q^0_{01}a_Y^\vee+q^0_{11}b_Y^\vee)$. In the above frame the diagonal parts give $x(Y)Z,x(Y)Z^\vee$ and their off-diagonal parts are the type raises and lowers times $(\overline{D_r}/D_r)X,(D_r/\overline{D_r})X^\vee$. Subtract these terms and divide by $x(Y)=\prod_j(Y+\rho_{\pi j})$ on each type. Choosing $r+2$ distinct real parameters away from the roots in all types, polynomial interpolation recovers $Z,Z^\vee$ at any parameter, including a root. The four transfers on this frame are therefore finite sums of $J$ applied to polynomial group differentials, with bounded matrix multipliers. The uniform order and degree concern each summand; the number of terms may vary with the rank. [Exterior contractions, covariance and suffix minors](https://github.com/yuiyuiui/Natural-Language-Proof-Generalized-Riemann-Hypothesis/blob/405237610e58ab9d4a9d5d54d9a0548a0c44227c/sections/g-real-restriction.tex#L6576-L6800)

<!--
% END FBE28
-->

<!--
% BEGIN FBE29
-->

<span id="claim:FBE29"></span>To iterate these transfers, write $\Omega=D/|D|$, $K_j=(\overline{D_r}/D_r)S_j$ for a single compact-type raise, and work with the multiplication algebra generated by $K_j,K_j^*$, constant diagonal type matrices, $\Omega^{\pm1},\zeta^{-1},\bar\zeta^{-1}$. It consists of bounded multipliers for the fixed mark since $|\zeta|^2>t>0$. In the compact type frame of FBE28 the raises are constant and $\alpha_{\rho+\mathbf e_j}=\alpha_\rho-1$. For each of the four operators $U$ this gives $U(Y)K_j=K_jU(Y-1)$, with shift $+1$ for $K_j^*$. The phase of $K_j$ lowers the two site Euler operators by one and the change of connection gives the identical shift at the marked coordinate. Constant type diagonals commute with the four uncorrected families. For multiplication by $\Omega^a$, $a=\pm1$, the sites shift $Y$ by $a/2$ in both signs. Beyond $\Omega^a Z(Y+a/2)$ the residue has the extra term $at\,\Omega^{a-2}X(Y+a/2)/(2\bar\zeta)$. Its reflected version has $at\,\Omega^{a+2}X^\vee(Y+a/2)/(2\zeta)$. Differentiate the phase in $\zeta,\bar\zeta$ to obtain these terms, using $|\zeta|^2-H_0=t$. The unmarked operators commute with both inverse coordinates; the remaining nonzero commutators are
$$
 [Z,\zeta^{-1}]=\Omega^{-2}(1-t/|\zeta|^2)X,\qquad
 [Z^\vee,\bar\zeta^{-1}]=-\Omega^{2}(1-t/|\zeta|^2)X^\vee.
$$
The product rule thus moves any multiplier left of any one of the four operators, leaving bounded multipliers and words of the same or smaller length. Applying FBE28 successively gives a finite sum of bounded multipliers times transformed group coefficients. An $h$-letter composition costs at most $hd$ invariant derivatives and $h(r+1)$ powers of group growth, because invariant derivatives preserve the polynomial coefficient degree. For $h\le 2N+2$ the decay available in FBE25 leaves the threshold $2(k+r)(r+1)+1$ with four derivatives to spare. FBE24 bounds the $L^2$ transforms. To identify these transforms after compact exhaustion, on each regular orbit first use the fixed-orbit majorant of FBE27 or the same triangular recovery with all pivots nonzero; the coefficient and its finitely many differentiated versions have the extra power for that majorant. Fatou identifies the $L^2$ bound at the chosen characters. Equivalently the compact approximants converge by FBE24, and their almost-everywhere subsequential limit agrees with the pointwise regular transform. The orthonormal intertwiner frame with its square-root density is isometric for this norm.

Finally the original bare column uses $D^{-1}X$ and $\bar D^{-1}Z$ and a bounded residue multiplication matrix. Commuting a real power $|D|^u$ to the left shifts $X$ by $u/2$ and $X^\vee$ by $-u/2$. For $Z$ the correction is $ut\,\Omega^{-2}X(Y+u/2)/(2\bar\zeta)$, and for $Z^\vee$ it is $-ut\,\Omega^{2}X^\vee(Y-u/2)/(2\zeta)$. This follows from $p_j\log|D|=1/2$ and $\partial_\zeta\log|D|=1/(2\zeta)$. Writing the two inverse determinants as $|D|^{-1}\Omega^{\mp1}$ and commuting all $m$ positive powers to cancel them expresses the determinant-cleared word as a finite sum of the $L^2$ terms just bounded. On a compact parameter box separated from earlier poles the residue matrices are bounded and the remaining polynomials have degree at most $r+1$ in the newest parameter. Lagrange interpolation at $r+2$ fixed nodes gives a pointwise envelope by a constant times the sum of absolute values of finitely many $L^2$ functions. This constructs the $B_a$ used in FBE26. The remaining identification in this route is the choice of the *actual* compact intertwiner frame with the stated diagonal connection and constant raising matrices, together with the signed adjunction on the reached binary words in that frame. The determinant-cleared estimates apply to that prescribed frame once the identification is made. [Frame commutators and transfer of words](https://github.com/yuiyuiui/Natural-Language-Proof-Generalized-Riemann-Hypothesis/blob/405237610e58ab9d4a9d5d54d9a0548a0c44227c/sections/g-real-restriction.tex#L6800-L6878) · [Determinant shifts in the actual section](https://github.com/yuiyuiui/Natural-Language-Proof-Generalized-Riemann-Hypothesis/blob/405237610e58ab9d4a9d5d54d9a0548a0c44227c/sections/g-real-restriction.tex#L7217-L7277)

<!--
% END FBE29
-->

<!--
% BEGIN FBE30
-->

<span id="claim:FBE30"></span>We identify the frame in FBE28 using the original middle group on $|\zeta|^2>t$. In coordinates putting each negative mark on its last axis the middle representative fixes the common $k-1$ positive directions. Restriction to their $U(k-1)$ has multiplicity one in each of the two compact representations. Choose constant unit intertwiners on the common type lines. In this initial frame put $F=M_{10}$, $M_{11}=H_0 x(Y)$, $x_\rho(Y)=\prod_{j<k}(Y+\rho_j)$, in the unsigned convention. The cofactor omitting row zero commutes with $\bar\zeta$ because its generator bracket contains that row; the bracket with $\zeta$ expands its remaining column zero and gives the negative double cofactor. Thus $[F,\bar\zeta]=0,\ [F,\zeta]=-H_0x$. From the exchange relation of FBE13, on type $\rho$ the diagonal of $F(Y)/x_\rho(Y)+Y\bar\zeta$ is independent of $Y$. Its scalar commutators give the expression $H_0 x_\rho(Y)(-\partial_\zeta-A_\rho-(Y+1/2)\bar\zeta/H_0)$. On two distinct types the same relation with the parameters interchanged gives
$$
 (x_{\rho'}(u)-x_\rho(u))F_{\rho'\rho}(v)
 =(x_{\rho'}(v)-x_\rho(v))F_{\rho'\rho}(u).
$$
A nonzero block therefore has parameter-independent factor $S$ and $x_{\rho'}/(x_{\rho'}-x_\rho)=Y+a$. Comparing roots in the disjoint interlacing intervals leaves only $\rho'=\rho+\mathbf e_j$, $a=\rho_j+1$. The corresponding $S$ commutes with both radial coordinates, so it is a scalar multiplier on the line. The determinant of FBE16 at $Y=-\rho_j-1$ determines its norm squared as $-q(-\rho_j-1)/\prod_{i\ne j}(\rho_i-\rho_j)(\rho_i-\rho_j-1)$. This is constant on the radial annulus. An allowed edge has a nonzero value by strict interlacing; at the forbidden upper endpoint the corresponding compact polynomial vanishes.

For the phase of the diagonal put $d_\rho=\sum_j\rho_j$, $u_*=\sum_i(u_i+u_i')$, $\alpha_\rho=u_*/2-d_\rho$, $\nabla=\partial_\zeta+A_\rho$. Up to a type-independent scalar, the coefficient of $Y^k$ in $M_{00}$ is
$$
 \Theta=\zeta\nabla+\bar\zeta\nabla^*+d_\rho-2\alpha_\rho t/H_0.
$$
Indeed the diagonal Schur complement for $M_{00}$ has numerator $q(Y)$ plus the occupied raise-and-lower cofactors, divided by $H_0x_\rho(Y+1)$. Its two leading coefficients before the factor $1/H_0$ are $-t$ and $-t(1+u_*-d_\rho)$. The diagonal product $H_0x m_0\ell_0$ contributes $\zeta\nabla+\bar\zeta\nabla^*+t/H_0+d_\rho|\zeta|^2/H_0$ in degree $k$; the other shifts have degree at most $k-1$. The exchange relation gives $[\Theta,F(v)]=-F(v)$ by its leading coefficient. Project to the type line and substitute its diagonal expression for $F$. Using $[\zeta\nabla+\bar\zeta\nabla^*,\nabla]=-\nabla+\bar\zeta[\nabla^*,\nabla]$ gives $[\nabla^*,\nabla]=2\alpha_\rho t/H_0^2$. Thus for $\beta=\alpha_\rho\bar\zeta/H_0-A_\rho$ the imaginary one-form $\beta\,d\zeta-\bar\beta\,d\bar\zeta$ is closed.

There can still be monodromy on this annulus. On the representative $g(\zeta)$ the middle central circle $v$ rotates $\zeta$ to $v\zeta$. It also multiplies the coordinates other than the negative axis by $v$ on the left and just the first positive coordinate by $v$ on the right; these two stabilizer actions have integral common-line weight $m_\rho$. Differentiating this action gives $\zeta\partial_\zeta-\bar\zeta\partial_{\bar\zeta}+m_\rho$. Comparison with the preceding trace coefficient in the centered convention gives $2\Re(\zeta\beta)=u_*-d_\rho-m_\rho\in\mathbb Z$. Indeed the centered compact weights lie in $\mathbb Z+(k-1)/2$ and the $k-1$ interlacing coordinates in $\mathbb Z+k/2$. The closed form consequently has periods in $2\pi i\mathbb Z$. Its exponential integral defines a single-valued unitary change of frame giving $A_\rho=\alpha_\rho\bar\zeta/H_0$.

For an allowed single raise the $(\rho+\mathbf e_j,\rho)$ entry of $[F(u),F(v)]=0$ gives $[\nabla,S_j]=-(\bar\zeta/H_0)S_j$ by comparing the coefficient linear in $u$ after removing the common factors. In the normalized frame $\alpha_{\rho+\mathbf e_j}=\alpha_\rho-1$ cancels the right side, hence $\partial_\zeta S_j=0$. The constant modulus already proved forces this antiholomorphic multiplier to be constant. For two distinct raises, the entry on their square in the same commutator gives $(d-1)S_iS_j=(d+1)S_jS_i$ in the appropriate order with $d=\rho_j-\rho_i$, $|d|>1$. The two products have the same phase. Since monotone paths in the interlacing box differ by such squares, rephasing the constant line bases makes all nonzero raises positive. This proves the frame and the constant-matrix assertion for the original coefficient. [Group connection and its angular period](https://github.com/yuiyuiui/Natural-Language-Proof-Generalized-Riemann-Hypothesis/blob/405237610e58ab9d4a9d5d54d9a0548a0c44227c/sections/g-real-restriction.tex#L6205-L6453) · [Adjacent raises and the interlacing square](https://github.com/yuiyuiui/Natural-Language-Proof-Generalized-Riemann-Hypothesis/blob/405237610e58ab9d4a9d5d54d9a0548a0c44227c/sections/g-real-restriction.tex#L6454-L6522)

<!--
% END FBE30
-->

<!--
% BEGIN FBE31
-->

<span id="claim:FBE31"></span>In the preceding frame the adjoint on a positive word gives the energy of the actual group section. For the binary factor of a letter at $a$, let $R_a(Y)=((Y-a)1-\Pi_a)/(Y-a-1)$ with $\Pi_a$ the flip with the auxiliary factor. Let $S_w$ be the ordered product over the old letters, $T_w=Q_0 S_w$ where $Q_0$ includes the sign of the cut. Write $v_Y=(a_Y,b_Y)^t$ and $C_w=v_Y^*T_wv_Y$. The matrix $R_a$ is self-adjoint for real parameters separated from its pole. The exchange identity at $(a,Y)$ transports $T_w^*\mathcal R_w=\mathcal R_w T_w$ to the new residue form $\mathcal R_{aw}=\operatorname{diag}(\mathcal R_w,\mathcal R_w)T_w(a)$. The base case is the compact group adjoint of FBE13. On the alternating auxiliary line the shifted product of $R_a$ has scalar $(Y-a+1)/(Y-a)$. FBE16 and multiplication over disjoint bit factors give the determinant $Q(Y)=q(Y)\prod_a (Y-a+1)/(Y-a)$.

Conjugate by the old shear frame $F_w$ that diagonalizes the residue. Completing the two squares of FBE10 gives $\mathcal R_{Yw}=F_{Yw}^*D_{Yw}F_{Yw}$ with $F_{Yw}=\Lambda_w(Y)\operatorname{diag}(F_w,F_w)$. The diagonal factors of $\Lambda_w$ are $\zeta^{-1},H_0/\bar\zeta$, with the lower-left shear chosen by the off-diagonal coefficient. The new two weights relative to $D_w$ are $WQ(Y)/x(Y+1)$ and $Wx(Y)$, where $x$ includes the old zero-bit factors. Thus, writing $g_Y=\Lambda_w v_Y$, contraction gives $(g_Y^*D_{Yw}g_Y)F_w=D_wF_w C_w$. This step uses that $v_Y$ and its adjoint act on the $c_j$ variables and commute with the old radial frame. The shear residues stay in the bounded multiplication algebra of FBE29. At the empty word their terms are $(\zeta/\bar\zeta)S_j/(Y+\rho_j)$ in the appropriate projected types. Adjoining $a$ replaces the old diagonal residue in bit zero by $E_w(Y)-(E_w(Y)-E_w(a))/(Y-a)+t/\bar\zeta$, creates a scalar off-diagonal $-1/(Y-a)$ and conjugates the bit-one diagonal by the constant old pivot $x_w(a)$. These are bounded on the next separated box.

For the section reached by the old word let $u_w$ apply the old site matrices on their bits to the zero binary vector, in site order. The one-site identities $[p_i,c_i]=c_i$ and $[p_i,c_i^{-1}]=-c_i^{-1}$ give the same exchange relation between a new auxiliary site and each old bit site as between $R_a$ and the two auxiliary matrices. Move $S_w$ through these site products one factor at a time. The adjoint sites commute with the old sites in different complex variables (holomorphic versus antiholomorphic), and $Q_0$ acts in the middle coordinates. Since every $R_a$ fixes the auxiliary-zero, all-zero column, taking its auxiliary-zero component gives $C_wu_w=u_w C_0$. The centered Capelli operator on the original smooth coefficient has eigenvalue $P(Y)=\prod_i(Y+\lambda_i)$. Covariance and the decay and fixed-point bounds above allow its invariant derivatives to pass through the orbital integral on the regular section. The signed $C_0$ therefore acts on $j$ by $|P(Y)|$ on the cut. For $X_w=F_wu_wj$ the required adjoint identity follows. Compact radial truncation away from $G=0$ for the pairing is justified by FBE24–25 and FBE29 up to order $2N+2$.

A negative letter uses the partially transposed flip in $R^-_a=((a-Y)1-\Pi_a^{t_1})/(a-Y-1)$ to the left of the old transfer. Its alternating-line scalar is $(a-Y)/(a-Y-1)$. Transposition of the exchange at $(a,Y)$ gives $T_w(Y)R^-_a(Y)T_w(a)^t=T_w(a)^tR^-_a(Y)T_w(Y)$, so the same weighted adjunction holds. The shifted $11$ identity gives the reflected lower shear $D_w^{-1}\ell_w(a-1)^*D_w$. FBE10 then gives relative weights $WQ(a-1)/x(a-1)$ and $Wx(a)$, positive on the admitted intervals. These are the weights used on the compact projections of FBE17. Finally the all-zero path uses only $C_0$ for each signed letter. At each positive Gram cutoff its Gram energy is a polynomial of degree at most $k+2r+1$ in each of the actual evaluation parameters, with the same polynomial for the two sign conventions. The site degrees are at most $r$ on either side of the middle matrix of degree at most $k+1$. Interpolation on the separated positive grid of the level-zero proof therefore transports its cutoff limit to every reached signed word. FBE26 and FBE28–30 supply its differentiated cutoff bounds. The result is the uncut norm divided by $\Gamma_0$ after division by the native word weight. [Bit exchanges and the adjoint on the selected vector](https://github.com/yuiyuiui/Natural-Language-Proof-Generalized-Riemann-Hypothesis/blob/405237610e58ab9d4a9d5d54d9a0548a0c44227c/sections/g-real-restriction.tex#L6882-L7082) · [Signed insertions](https://github.com/yuiyuiui/Natural-Language-Proof-Generalized-Riemann-Hypothesis/blob/405237610e58ab9d4a9d5d54d9a0548a0c44227c/sections/g-real-restriction.tex#L7346-L7488) · [Box widths and interpolation on the constructed row](SPECTRAL_LEVEL_ZERO_AND_CUTOFFS.md)

<!--
% END FBE31
-->

<!--
% BEGIN FBE32
-->

<span id="claim:FBE32"></span>The constant $C_7$ in FBE26 can be chosen before the rank and the translated coefficient. Use the separated boxes of the level-zero proof, of length $L$ in the middle third of the cut of length $I$, with $6NL\le I$, $dL\le I$, $N\le L$ and $L>2$. On the next box any earlier letter is at distance $\ge L$. The old-letter factors $(Y-a)/(Y-a-1)$ and $(Y-a+1)/(Y-a)$ are between $1$ and $1+2/L$ or $1+1/L$. Their products, including the shifted pivot, are between $1$ and $e^2$ or $e$. Each of the compact polynomials in the weights has roots outside the cut in its indicated shift. The ratio of any such product of degree at most $d$ between two points of the box, in either direction, is at most $(1+3L/I)^d\le e^3$. Apply this separately to both compact polynomials in $Q$. The ratios of the two next weights are at most $e^{12},e^5$; that of $|P|$ is at most $e^3$.

The triangular change in the second component under a common shift subtracts the two residue matrices $E_w(Y)-E_w(Z)$. To see the rank dependence, separate the possible output edges. Terms at an old pole flip just that bit; terms at a type pole raise its one coordinate. For each fixed edge label the map on the other indices is a partial matching. An old pole gives a reciprocal difference of modulus $\le L/(L-1)^2$. Inserting it into the old-bit recursion in FBE31, or subtracting the two partial fractions of that recursion, gives squared coefficient times the weight ratio at most $e^{14}/L^2$: the rational products at earlier letters are bounded by $e^2$, and the shifted positive weights by the preceding ratio bounds (equivalently $|1/(Y-a)-1/(Z-a)|\le1/L$ for $Y,Z$ in the new box). The sum over at most $N\le L$ bit positions has squared operator norm at most $e^{14}$.

For the type terms put $b_j=-\rho_j-1$ and $R(t)=\prod_i(t+1/2+u_i)/\prod_j(t-b_j)$; let $\widetilde R$ have the second compact weights and the shifted poles $b_i+1$. By interlacing the residues of $R$ are $-A_j\le0$. Pair each zero with its neighbouring pole separately on either side of the cut, keeping the extra zero. The logarithmic derivative $R'/R$ is a signed sum of reciprocals; on either side the monotone telescoping differences and a possible unpaired endpoint have absolute sum at most $3/I$. The polynomial part of $R$ is monic linear. Hence $1+\sum A_j/(Y-b_j)^2=R'(Y)\le6|R(Y)|/I$. The same holds for $\widetilde R$. For an allowed raise the weight spacing gives $|b_j-b_i-1|\ge1$ for every $i$. Write $d_j=|Y-b_j|\ge I/3$. In the partial fractions for $\widetilde R(b_j)-\widetilde R(Y)$ use $|Y-b_i-1|\le(1+d_j)|b_j-b_i-1|$. This gives $|\widetilde R(b_j)|/|\widetilde R(Y)|\le 1+6d_j(1+d_j)/I\le11d_j^2/I$. Therefore
$$
 \sum_j \frac{A_j|\widetilde R(b_j)|}
 {|R(Y)\widetilde R(Y)|\,|Y-b_j|^3|Y-b_j-1|}
 \le 132/I^2 .
$$
The edge coefficient is the norm of the raise in FBE30 times the difference of its two resolvents. Squaring and taking the ratio of the incoming and outgoing weights cancels the two products of the other compact poles in its norm formula. This leaves each summand displayed above times at most $4e^7 L^2$, using $|Y-Z|\le L$, the two comparable pole distances and the bounded old-letter factors. Cauchy–Schwarz over the $k-1$ possible type raises bounds their squared norm by $528 e^7(k-1)L^2/I^2\le88e^7$, since $(k-1)L\le I$ and $6L\le I$. The two edge sums together cost at most $2e^{14}+176e^7$ in squared norm. Thus $C_R,C_d,C_P$ in the regulated estimate have absolute bounds. Choosing $L=C(r+1)^3$ with absolute sufficiently large $C$ meets the lower bound in FBE26, and the selected cut contains all the boxes by its stated gap and the level-zero estimate. This completes the differentiated energy limit at the parameters of the constructed family. [Two weight ratios and the residue calculation](https://github.com/yuiyuiui/Natural-Language-Proof-Generalized-Riemann-Hypothesis/blob/405237610e58ab9d4a9d5d54d9a0548a0c44227c/sections/g-real-restriction.tex#L7069-L7177) · [Actual cut width and signed grid](SPECTRAL_LEVEL_ZERO_AND_CUTOFFS.md)

<!--
% END FBE32
-->

## The hypotheses of the signed-word recursion

<!--
% BEGIN FBE33
-->

<span id="claim:FBE33"></span>Consider the actual finite-place presentations in the local model of the original main row, on a fixed finite prefix set $Y$. Write $N_p(t,t')$ for a local matrix of two last entries, $B_p$ for its predecessor matrix, and $L_p,L'_p$ for the period and reciprocal-difference subgroups. The local counting assertion says that one may complete the diagonal presentation sum to a positive matrix $H_p(t)$ depending on $t\bmod L_p$. It satisfies $0\le N_p(t,t)\le H_p(t)$ for $t\ne0$, and $\sum_{c\in A_p}H_p(c)\le B_p$ for each finite set of distinct local classes. Nonzero $N_p(t,t')$ requires $t^{-1}-{t'}^{-1}\in L'_p$. These are positive-semidefinite inequalities. In the presentation model each summand is the outer product of its vector of values on $Y$ with its conjugate. Adding presentations and partitioning them by residue class gives the inequalities. A phase depending on an entry has modulus one and disappears in its diagonal. At the last singleton the model has zero off-diagonal blocks for distinct nonzero entries.

Here is the passage to a finite global tower. For matrices on the same head set use the entrywise product. The product of Gram matrices is Gram, by tensoring their vectors. Consequently $\bigodot A_p\le\bigodot B_p$ if $0\le A_p\le B_p$ for every $p$, by successively replacing a factor and taking the product of positive matrices. Define $H(t)=\bigodot_p H_p(t)$ and multiply each entry $(x,y)$ by the actual factor $a(x)a(y)$ from the arithmetic normalization. This real diagonal congruence preserves positivity even when $a$ vanishes. If representatives $t$ are distinct modulo $L=\bigcap L_p$, their tuples of local residue classes are distinct. Form the product of the finite sums over the classes that actually occur in each coordinate. Its expansion contains the $H(t)$ once each and only adds positive matrices. Thus $\sum_t H(t)$ is dominated by the actual predecessor kernel, while every $H(t)$ dominates the original diagonal block. A nonzero off-diagonal product requires the reciprocal difference to belong to every $L'_p$, hence to the specified global reciprocal lattice. The displayed period equality and reciprocal inclusion suffice. The same tensor argument gives positivity of the finite arithmetic kernel itself: the equivalence condition on two labels has Gram vectors given by distinct orthonormal basis vectors, and the factors $d_p(x)\overline{d_p(y)}$ are diagonal congruences.

This constructs the dominating matrices after the finite tower has been chosen, just as the native quantifier requires. The local model has initial excess $e_i=0$ at all used levels. Hence the diagonal sum has coefficient one there. These deductions use the actual local factorization, with its top, pullback and unramified outside presentations. A different representation of their product by matrices with the same scalar total would still have to satisfy the stated local class conditions. [Original finite local model](https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Formalism/HermitianCurvature/StatementPB.lean#L282-L301) · [Residue matrices and product systems](https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Formalism/HermitianCurvature/StatementJ.lean#L584-L616) · [Construction on the finite prefixes](https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Formalism/HermitianCurvature/HermitianCurvatureProofs/GrowthOfBasic.lean#L978-L1012)

<!--
% END FBE33
-->

<!--
% BEGIN FBE34
-->

<span id="claim:FBE34"></span>We spell out the eighteen assertions used together on line 1120 of the original main row. The field has $f=[E:\mathbb Q]/2\ge1$ marked complex places, the chosen derivative order is $K=5$, and the scale $\Theta$ is positive. FBE2 gives the inequalities on window sizes and block volumes for the common box. FBE3 uses the period and reciprocal-difference lattices of that very box for both nonzero-frequency sums. At $K=5$ the required power $\Theta^{-(K-5/2)}$ is precisely $\Theta^{-5/2}$. These checks account for the three numerical inequalities, the size clause and the lattice-sum clause.

On the real side, for $\varepsilon>0$ the matrix for a word is its positive weight times the Gram matrix of the finitely many vectors given by that word at the chosen heads. Its contraction with $z_x\overline{z_y}$ is that weight times the squared norm of the sum. The weights are strictly positive products of the absolute shifted factors on the admissible, root-free cuts, including the displaced negative factors of FBE31. These give Gram positivity and word positivity. The wave, lift, and longer-block clauses are the inequalities for the original word vectors in FBE1–4 and FBE28–32. Their probability coefficients come from the normalized absolute word factors. They are chosen per allowed differentiation and type of embedding, before choosing the coefficients of a tested Gram form. The longer-block budget is $(s+1)K$.

For the Poisson clause, take the finite-dimensional real vector space of the complex embeddings, with its coordinate projections, the arithmetic period lattice and the dual character pairing in FBE3–4. At a fixed finite set of heads and a positive test matrix, the original diagonal contraction is the nonnegative function to be sampled. Its integrable extension, the normalized Fourier values and its pointwise values at the nonzero sampling entries are precisely the three identifications in the wave-function hypothesis. FBE4’s Fejér argument then bounds the sum at any finite subset of the translated lattice by the absolute zero mode plus the stated bound on finite sums of nonzero modes. This uses the same covolume in both Fourier readings. One cannot insert a new determinant factor when passing to the chosen real coordinates. The remaining two real clauses concern different ends of the recursion. At the empty head, FBE6 and FBE31–32 give convergence of the weighted initial energy to $jn$ for each permitted word. At a fixed finite family of represented terminal points the Gram thresholds are strictly positive. Their minimum gives eventual *equality* of the empty-word cut Gram with the terminal vector Gram on the pairs where the finite kernel is nonzero, as in FBE6 and FBE27. This verifies the eight real clauses on the stated native coefficient and frame. FBE38 gives the sampling inequality directly from the matched single-place wave forms, including at the sampling coset.

The remaining four finite assertions are positivity of the arithmetic kernel, support of its off-diagonal blocks, the interval $0\le e_i\le1$, and existence of a dominating residue system after the finite tower is fixed. They follow from FBE33 on the selected local model, initially with $e_i=0$. The eighteenth assertion, about row domination, is first applied with the identically zero coefficient. Its support and summability are immediate and its positive-kernel inequality is just the arithmetic kernel's positivity. Thus the displayed conjunction in the original source is obtained on the stated model and wave frame. The nonzero arithmetic row requires a further step. [Definitions of the eighteen assertions](https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Formalism/HermitianCurvature/StatementTC.lean#L209-L213) · [Actual Poisson and real inputs](https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Formalism/HermitianCurvature/StatementPB.lean#L302-L312) · [Main row and zero coefficients](https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Formalism/HermitianCurvature/HermitianCurvatureProofs/GrowthOfBasic.lean#L1098-L1127)

<!--
% END FBE34
-->

<!--
% BEGIN FBE35
-->

<span id="claim:FBE35"></span>Let $c_{\rho,p}$ now be the original arithmetic row coefficients. In the source the row hypothesis gives support at represented terminal points, absolute summability of $\sum_p |c_{\rho,p}|\,\|V_p\|$ for each $\rho$, and, on every finite terminal head set and finite row set $R$,
$$
 \sum_{\rho\in R}(c_{\rho,p}\overline{c_{\rho,q}})_{p,q}
       \ \le\ \mathrm{sd}\,K_{\rm top}.
$$
Assume the given density estimate $\mathrm{sd}\le2$. Put $\eta=\max(1,\mathrm{sd})$, multiply the terminal arithmetic kernel by $\eta$ and replace the terminal excess $e_{r+1}=0$ by $\eta-1$. The real word Gram and the row vectors stay in their original normalization. The positive difference $(\eta-\mathrm{sd})K_{\rm top}$ gives row domination with coefficient one for the rescaled kernel. Its support at the terminal level agrees with that of the original since $\eta>0$. Row summability is the given one. Scale each terminal dominating residue matrix by $\eta$. Its comparison with the terminal diagonal and its periodicity are preserved, and its predecessor-sum bound gains the factor $\eta=1+e_{r+1}$ required in FBE5. Every lower level keeps its original excess, and $0\le\eta-1\le1$. The real wave, lift and sampling inequalities quantify over *any* positive test kernel on the finite heads and continue to apply. The empty-head normalization and the eventual terminal Gram equality also keep their meanings.

The finite recurrence therefore uses the true rows with one density factor at the last level. Absolute row tails allow the finite head sets to exhaust each convergent vector sum exactly as in FBE6. The source then uses its stated inequality comparing the norm of the arithmetic coefficient to these row sums. In particular line 1120 itself contributes no additional hypothesis about positivity of the nonzero rows. FBE36–37 prove the density and row hypotheses for the matched scalar-partner realization, and FBE38 identifies its singleton Fourier readings. Their application requires the prescribed local models and measures on the coefficient in question. [Terminal rescaling in the original statement](https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Formalism/HermitianCurvature/StatementTC.lean#L270-L296) · [Nonzero row support, domination and summability](https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Formalism/HermitianCurvature/StatementPB.lean#L314-L323) · [Application to the actual rows](https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Formalism/HermitianCurvature/HermitianCurvatureProofs/GrowthOfBasic.lean#L1119-L1132)

<!--
% END FBE35
-->

## The density supplied by the represented arithmetic rows

<!--
% BEGIN FBE36
-->

<span id="claim:FBE36"></span>For the distinct-word scalar contribution take the same local characters, finite measures and terminal presentation classes as in the selected arithmetic row. Let $\theta$ comprise the terminal ratio and all the local marked isomorphism classes of a represented joint frame. Write $B_\theta(p)$ for the product of the phase-weighted local orbital sums at a terminal point $p$, including the local isomorphism multiplicities. The positive scalar $a_\theta$ is the product of the reciprocal local automorphism orders. The point kernel is the sum of the matrices $a_\theta B_\theta(p)\overline{B_\theta(q)}$ with the prescribed point normalization on both indices. Nonrepresented points have zero row coefficient.

The row Gram involves two counts on the same support. Holding a term $\gamma$ at $p$ fixed, its partners at $q$ have the same terminal ratio. Their unweighted phase sum equals $B_{\theta(\gamma)}(q)$. In fact a choice of local double orbit and a compatible local marked isomorphism at each exceptional place determines an orbit of partners. Additive approximation lifts the two unitriangular changes of coordinates from these finitely many places, and intersecting the chosen local lattices with the rational space recovers the global lattice. In the fixed tuple the phase depends only on the given local cosets. Next sum the partners at $p$ with the source lattice weights. Gluing the fixed represented frame to its definite complement along the discriminant module, with reciprocal stabilizer weights, counts its primitive representation mass. Relative to the single-frame reference this multiplies $a_\theta B_\theta(p)$ by the density ratio $d_\theta$ and the point weight $n(p)$. The two fibre counts and their normalization are proved for the selected model in the arithmetic row calculation. On the support of a fixed tuple the shifted determinant ideals agree and $n(p)=n(q)>0$. Consequently the two square-root point weights cancel the extra $n(p)$. This expresses the full represented Gram on any finite set of heads as a sum of the same positive rank-one matrices with coefficients $d_\theta a_\theta$. The empty represented family gives zero. Removing any collection of rows subtracts a positive matrix. Taking $\mathrm{sd}$ to be the supremum of the represented density ratios gives the finite domination in FBE35, with its off-diagonal phases intact. [Selected row and its two fibre counts](SPECTRAL_SCALAR_ROW_MASS.md#a-finite-terminal-flag-estimate-preserving-the-phases) · [Original normalized partner and mass identities](https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Formalism/LocalToGlobal/SiegelLatticeTheory/CokernelGLCounts/RankPointCounts/LsDatumBPf.lean#L27-L104) · [Jin, expansion of the actual Gram](https://github.com/yuiyuiui/Natural-Language-Proof-Generalized-Riemann-Hypothesis/blob/405237610e58ab9d4a9d5d54d9a0548a0c44227c/sections/g-real-restriction.tex#L4479-L4539)

Here is the bound $\max(1,\mathrm{sd})\le2$ entering FBE35. Put $h=k-2r-2\ge f+5$ in the large-rank range. The local density hypothesis bounds every $x<\mathrm{sd}$ by some finite product of $\exp(4q_v^{-h})$. The residue cardinality $q_v$ is at least the rational prime below it and there are at most $f$ places above any such prime. Thus the logarithm of each product is at most
$$
 4f\sum_{a=2}^{\infty}a^{-h}
 \le 4f\,2^{-h}\bigl(1+2/(h-1)\bigr)
 \le 8f\,2^{-(f+5)}\le\tfrac18 .
$$
The integral test gives the middle bound and $f/2^f\le1/2$ for $f\ge1$. It follows by approximation from below that $\mathrm{sd}\le e^{1/8}<2$. The [primitive density calculation on the chosen frames](SPECTRAL_SCALAR_DENSITIES.md) gives a sharper bound with their marked local factors. Either estimate controls the terminal coefficient in precisely the normalization of FBE35. The passage to the full arithmetic row also uses absolute summability of $|c_{\rho,p}|\|V_p\|$ over **all** represented terminal points in each row. Convergence of the integral at one fixed orbit is a different assertion. [Original density hypotheses](https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Formalism/HermitianCurvature/StatementPB.lean#L325-L330) · [Finite-product majorant in Lean](https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Formalism/HermitianCurvature/HermitianCurvatureProofs/DensitySumsAndDomination.lean#L182-L246)

<!--
% END FBE36
-->

## Absolute convergence of one arithmetic row

<!--
% BEGIN FBE37
-->

<span id="claim:FBE37"></span>Use the fixed selected adelic realization with its two Bessel sections, finite-level double-coset presentation, column measures and terminal point weights. We prove the row summability used in FBE35 for this realization. Constants in this convergence argument may depend on the fixed row. Let $\Gamma=G(F^+)$, let $S\subset\Gamma$ be the rational stabilizer of one marked flag, and let $W$ be its adelic section. Fold the scalar function $\|W\|$ to obtain $P(x)=\sum_{\gamma\in S\backslash\Gamma}\|W(\gamma x)\|$ on $\Gamma\backslash G(\mathbb A)$. At finite places replace the compact level factors by their absolute values. Finite type spaces and locally constant finite factors allow the use of a finite sum of such functions. We need $P\in L^2$.

Write $n$ for the matrix size. On the real group use the height $L(x)=\inf_{s\in S_\infty}\prod_v\|(sx)_v\|_{\rm op}$ in the unitary frames. The compact reproducer for the high-gap row gives $\|W(x)\|\le C\int_U\|W(xz)\|\,dz$ on a compact neighbourhood $U$. Its weighted integrability gives $\int_{S\backslash G(\mathbb A)}\|W(x)\|L(x)^h\,dx<\infty$ on the finite-level supports for $h=4n^2\sqrt{2\max_v q_v}$ in the noncompact case. For compact real factors the corresponding norm is bounded. The real estimate follows by integrating its lowest-type coefficient against $\|g\|_{\rm op}^h$ in Cartan coordinates and unfolding the compact and unipotent Bessel average. The gap $16 n^{19}$ dominates both the Haar exponent and $h$ there. The compact stabilizer and the rational unipotent quotient have finite volume in the stabilizer fundamental domain. [Reproducer and weighted estimate for this section](https://github.com/rh-lean-roadmap/rh-lean-roadmap/blob/0be265ccb325908c67f872361d564c66b99e96f7/docs/src/book/main.tex#L42662-L42726)

For clarity, the multiplicity of a compact translate in this folding is at most $C L(x)^h$ on each finite-level chart. Two rational translates of $xU$ through the same point differ by an element of $\Gamma\cap xUU^{-1}x^{-1}$. Their finite entries lie in a fixed denominator lattice on that chart. At $v$ their matrix entries are bounded by $C_v\|x_v\|_{\rm op}^2$, since inversion on the unitary group preserves this norm in diagonal signature coordinates. A fixed fractional-ideal lattice in all complex embeddings has at most $C\prod_v R_v^2$ points in a product of discs of radii $R_v\ge1$. This follows by packing a fixed small Euclidean box at each lattice point. Counting the $n^2$ entries therefore costs at most $C\prod_v\|x_v\|_{\rm op}^{4n^2}$. One can choose the real stabilizer representative within a factor two of the infimum: the compact and unipotent stabilizer quotient at the fixed finite level has a compact fundamental set modulo its rational points, with the unipotent part obtained in successive additive coordinates. Changing the rational representative and this bounded factor preserves the count up to a fixed constant. There are finitely many finite charts on the support. This proves the multiplicity bound used for the local average.

Indeed $\int_U P(xz)\,dz$ is at most the multiplicity times $\int_{\Gamma\backslash G(\mathbb A)}P$, by folding the integral over $xU$. Tonelli identifies the last integral with $\int_{S\backslash G(\mathbb A)}\|W\|$, which is finite. Reproduction gives $P(x)\le C\int_U P(xz)\,dz$. Unfolding one factor now gives
$$
 \int_{\Gamma\backslash G(\mathbb A)} P(x)^2\,dx
 =\int_{S\backslash G(\mathbb A)}\|W(x)\|P(x)\,dx<\infty .
$$
Do this for both words. Cauchy–Schwarz bounds $\int PP'$ and Tonelli unfolds that positive integral over $S\backslash\Gamma/S'$. Subdivision by the finite marked orbit gives the sum of integrals of the product of the two section norms on the same quotient slabs as the signed integral. This dominates the norm of each integrated tensor, since $\|v\otimes w^*\|_{\rm HS}=\|v\|\|w\|$. It bounds an **absolute sum over terms**, before any cancellation of the phases. The finite charts and quotient disintegrations are the prescribed ones for the two sections. [Absolute unfolding on the selected level](https://github.com/rh-lean-roadmap/rh-lean-roadmap/blob/0be265ccb325908c67f872361d564c66b99e96f7/docs/src/book/main.tex#L46775-L46785) · [Original estimate on quotient slabs](https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Formalism/LocalToGlobal/SiegelLatticeTheory/ClosedLocalOrbits/GaugeLatticeShifts/DoubleCosetSingleUnfolding.lean#L848-L887)

It remains to compare that sum with the actual point weights. For $n(p)>0$ the arithmetic coefficient $c_\rho(p)$ is the sum of $\sqrt{m_\gamma} A_\gamma(p)$ over the terms at $p$ in class $\rho$, divided by $\Phi_{r+1}(p)\sqrt{n(p)}$. Here $m_\gamma$ is its source lattice mass and $A_\gamma$ its finite orbit coefficient. In the same frames the real vector $V_p$ is $U(p)$ times a positive factor whose square is $C_0 n(p)\Phi_{r+1}(p)^2$, with $C_0$ independent of $p$. To check the $\Phi$ power, a terminal block shortening the remaining length from $m'$ to $m'-s$ contributes the exponent $m'(m'-1)-(m'-s)(m'-s-1)$. These exponents telescope to $r(r+1)$, leaving the indicated product of block factors and the absolute norm of the terminal Gram in $n(p)$. Thus
$$
 \sum_p |c_\rho(p)|\,\|V_p\|
 \le \sqrt{C_0}\sum_{p,\gamma:\rho(\gamma)=\rho}
          \sqrt{m_\gamma}\,|A_\gamma(p)|\,\|U(p)\| <\infty .
$$
The integral of the product of the two section norms on the corresponding slab dominates each $|A_\gamma(p)|\|U(p)\|$ with the common unfolding constants. The square roots of the source masses are bounded on the fixed finite set of definite lattice classes. A point with $n(p)=0$ has zero coefficient. This gives absolute convergence on every individual row without requiring the rate of convergence to be uniform across families. It permits regrouping the squared norm by scalar classes. On a fixed class, the possible occupied complete rows are indexed by the image of the target lattice stabilizer on the positive Levi quotient: two lifts differ by the same unipotent double-coset action exactly when this image agrees. Their common target weight is the reciprocal of that image's order. Summing the weights gives one. Together with the measured column-mass identity this gives the comparison of the actual scalar contribution with the row energies in FBE35 on this matched realization. [Terminal block-weight identity](https://github.com/yuiyuiui/Natural-Language-Proof-Generalized-Riemann-Hypothesis/blob/405237610e58ab9d4a9d5d54d9a0548a0c44227c/sections/g-real-restriction.tex#L5086-L5111) · [Regrouping and row mass](https://github.com/yuiyuiui/Natural-Language-Proof-Generalized-Riemann-Hypothesis/blob/405237610e58ab9d4a9d5d54d9a0548a0c44227c/sections/g-real-restriction.tex#L5265-L5309) · [Measured column calculation](SPECTRAL_SCALAR_ROW_MASS.md)

<!--
% END FBE37
-->

## Sampling the singleton at its actual arithmetic points

<!--
% BEGIN FBE38
-->

<span id="claim:FBE38"></span>There is a direct way to verify the Poisson inequality used by FBE34 on a matched family of singleton kernels. Fix the level, cut, word and finite prefix set $Y$ of the native assertion, and a positive test matrix $\kappa$ on $Y$. At a complex place $v$ write $G_{v,h,h'}(z_v)$ for the local singleton pairing, including the original word and point factors. On $V=\prod_v\mathbb C$ form the contraction
$$
 D(z)=\operatorname{Re}\sum_{h,h'\in Y}\kappa(h,h')
                 \prod_v G_{v,h,h'}(z_v)
$$
in the Gram orientation of the chosen sections. This is a positive scalar Gram contraction. Its values at the embedded nonzero arithmetic labels are exactly the real diagonal block entries in the sum of the native Poisson inequality. Put $D=0$ when one of the coordinates vanishes. These hyperplanes have zero Lebesgue measure and contain no embedded nonzero field element. Nonnegativity and continuity off them imply that this representative is lower semicontinuous everywhere.

On the realized local sections the off-hyperplane continuity follows from smooth slicing on the regular charts at a fixed positive cut, using the fixed-head integrable majorants of FBE25–27 in the noncompact limit. The singleton integral of each diagonal local pairing is finite and equals the preceding diagonal times its local Jacobian by FBE9. For an off-diagonal entry, Cauchy–Schwarz first in the Gram space and then in the one-variable integral bounds its $L^1$ norm by the geometric mean of the two diagonal integrals. The product over the places is integrable by Fubini, and $Y$ is finite.

For compact test sections, multiplying the first singleton slice by its additive character turns its pairing with the second slice into the Fourier transform of this local density at the corresponding dual label. This follows by using the singleton coordinate as the last integration variable: the phase is constant on its fibre. The common frame changes the argument by $\lambda_b=(g/(2\pi))^{2(r+1-b)}$. In the standard wave notation the dual argument is $2\pi i\xi/(g\lambda_b)$, with conjugation if the other slot is linear. The singleton Jacobian, the existing word factor and its parent normalization are those of FBE9. Cutting off both sections and then restoring them gives the same identity at the fixed cut. Indeed the $L^1$ norm of the difference of the two mixed densities is bounded by Cauchy–Schwarz applied to each difference vector and the unchanged vector in the singleton integral. The integrated squared difference tends to zero by the parent norm convergence of FBE25–27. Multiplication by a character preserves this bound, uniformly in the dual argument. Consequently the finite contraction of the actual wave pairings at a label $l$ is precisely $\widehat D(d(l))/\operatorname{covol}(\Lambda)$ in the source's character coordinates. The product of the singleton Jacobians is that same covolume. Here $\Lambda$ is the lattice of allowed periods, and its trace-dual frequencies are read with their prescribed additive character. [Fourier wave on the original coefficient](https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Formalism/HermitianCurvature/HermitianCurvatureProofs/ExistsNormBoundThreeFamilies.lean#L182-L226) · [Singleton normalization and wave variable](https://github.com/rh-lean-roadmap/rh-lean-roadmap/blob/0be265ccb325908c67f872361d564c66b99e96f7/docs/src/book/main.tex#L46478-L46491)

Periodize $D$ over $\Lambda$ with probability Haar measure on $V/\Lambda$. Its Fourier coefficients are $\widehat D(\xi)/\operatorname{covol}(\Lambda)$. For each finite set of distinct nonzero dual frequencies choose one allowed label above each. They are distinct and nonzero because the zero label maps to zero. The premise of the native inequality therefore bounds the sum of the absolute nonzero coefficients on every such finite set by $B$. Product Fejér means have weights in $[0,1]$ with finite support, so each mean is at most the absolute zero mode plus $B$. At every torus point the lower limit of the means is at least the periodized value by lower semicontinuity and positivity, as in FBE4. A finite set of distinct arithmetic labels in any allowed translate embeds injectively into the period coset and contributes at most that value. This proves the Poisson clause with the required quantifiers. It also explains the role of the zero set: an arbitrary almost-everywhere representative would not justify evaluation on this arithmetic set. The argument needs the original one-place singleton formulas on each word to which it is applied and the stated correspondence of the global finite and real frames. [Exact finite-coset assertion](https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Formalism/HermitianCurvature/StatementTB.lean#L160-L165) · [Trace-dual frame and stronger continuous-function presentation](https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Formalism/HermitianCurvature/StatementJ.lean#L265-L289)

<!--
% END FBE38
-->

## Matching the two period operators on a represented orbit

<!--
% BEGIN FBE39
-->

<span id="claim:FBE39"></span>Fix the two original marked words in one adelic realization and transport their actual Bessel coefficient and compact types to the standard real unitary frame. We identify the orbital operator at each point used in the terminal row. In particular the identification of the two type spaces can be kept independent of the point. Write $q=r+1$, $T,T'>0$ for the two mark norms, and $Z$ for the unsigned cross Gram matrix of a list of reversing blocks. Every block label is nonzero. Put $c=Z^{-1}e_q$.

Scale both rank-one diagonal mark matrices in the joint Gram by $s\in[0,1]$. After reducing the two off-diagonal blocks to identity, the rank-one determinant identity gives the determinant $(-1)^q|\det Z|^2(1-s^2TT'|c_q|^2)$. Positive terminal support is the inequality $1-TT'|c_q|^2>0$, equivalently $|\det Z|^2-TT'|\det Z_{[r],[r]}|^2>0$. The joint Gram consequently keeps its inertia $(q,q)$ along the segment, and its complement in the ambient group of signature $(k+r,r+1)$ is positive of dimension $k-1$. To choose the two compact rotations, project the vector $\gamma A'c$ for the right frame $A'$ onto the positive part of the left marked Witt frame $A$. Its inner products with $A$ form $e_q$, so its dual isotropic coordinates vanish and its mark component has coefficient $-1/T$. Its norm before projection is $-T'|c_q|^2$. Its projected norm squared is therefore $T^{-1}-T'|c_q|^2>0$. The reverse construction gives $T'^{-1}-T|c_q|^2$. Projection maps the common orthogonal complement isometrically onto the orthogonal complement of this positive vector in each positive frame. In fact vectors perpendicular to $A$ have only positive and isotropic components, so their inner products are computed on the positive components. Orthogonality against $\gamma A'c$ cuts out exactly the stated hyperplane. Dimensions give surjectivity. Normalizing the two projected vectors and using one orthonormal basis of the common complement produces two compact frame rotations at the same predetermined index. This works also when an intermediate leading minor inside a reversing block vanishes. [Pinned representatives in the two-period calculation](https://github.com/yuiyuiui/Natural-Language-Proof-Generalized-Riemann-Hypothesis/blob/405237610e58ab9d4a9d5d54d9a0548a0c44227c/sections/g-real-restriction.tex#L4939-L5002)

Set $\lambda=-\mathrm i g/(2\pi)$ and $\kappa=2\pi/(g\Delta)$, where $\Delta$ is the host root discriminant. The original isotropic vector at position $a$ becomes $\lambda^{-(q-a)}e_a$, with inverse conjugate change on its dual. The mark at the last position keeps its scale. A simple-root coordinate in the original character is then $\lambda$ times its model coordinate. Substitution in $\exp((4\pi\mathrm i/g)\operatorname{Re}\sum x_a)$ gives the model character on both sides. In a block $b,\ldots,i=b+s-1$, undoing the signed columns gives label $(-1)^{q-i}t$ before the column signs. At a nonzero entry $a+a'=b+i$ the signed coordinate factor is $(-1)^{i+a'}\bar\lambda^{q-a}\lambda^{q-a'}$. Its product with $t$ is $(g/(2\pi))^{2r+3-2b-s}\mathrm i^{s-1}t$. These changes identify the corresponding terminal representatives and preserve the sign of the Gram polynomial. They also transport the two fixed compact representations by isometries $E_v,E'_v$ determined by the original word frames.

One must divide by the stabilizer of this orbit. Its free root coordinates are the pairs $a<a'$ within one reversing block, as follows by solving the triangular stabilizer equation column by column. Conjugation sends each upper-triangular coefficient to its reversed opposite inside that block, and requiring both triangular conditions kills pairs in different blocks. The surviving coordinates give Haar coordinates with Jacobian one for translations by triangular matrices. Write $m=a'-a$. The right flag scaling and the dual pairing make its model coordinate $(\Delta\lambda)^{-m}$ times its arithmetic coordinate. Thus $(\kappa/\pi)d^2x_{\rm arith}$ becomes $(\kappa^{1-2m}/\pi)d^2x_{\rm model}$. There are $s-m$ such coordinates at height $m$. The arithmetic stabilizer measure consequently equals the model measure multiplied by
$$
 b_\kappa(p)=\prod_{\text{blocks of length }s}\prod_{m=1}^{s-1}
          \left(\frac{\kappa^{1-2m}}{\pi}\right)^{s-m}.
$$
Quotient integration with the same ambient Haar divides the orbital measure by this factor. In the integral defining the pinned arithmetic operator the two point-dependent rotations act by compact covariance. Changing the two unipotent variables by these rotations preserves the characters and the Haar measures and absorbs those rotations in the definition of the pinned value. The resulting operator is $E_v\,b_\kappa(p)^{-1}J_v^{\rm mod}(p)\,(E'_v)^{-1}$. Here $J_v^{\rm mod}$ integrates the transported *same* coefficient. The integrals converge on each such orbit by FBE27. Fubini for the finite product of places gives equality on every pure tensor, and finite-dimensional linearity extends it to the full type spaces. A square Gram pairing between two different terminal points has both inverse stabilizer factors. Multiplying by the square-root point weights now gives the terminal vector used by FBE35 and FBE37. On unrepresented points the arithmetic sum has zero coefficient, and on the zero-density locus the weighted vector is zero. This proves the comparison required by the original terminal tensor equation for these frames and measures. [The stabilizer measure and terminal tensor equation](https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Formalism/LocalToGlobal/SiegelLatticeTheory/ClosedLocalOrbits/RealObj.lean#L358-L383) · [The operator on pure tensors](https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Formalism/LocalToGlobal/SiegelLatticeTheory/ClosedLocalOrbits/RealObj.lean#L453-L478) · [Jin’s root coordinates and quotient calculation](https://github.com/yuiyuiui/Natural-Language-Proof-Generalized-Riemann-Hypothesis/blob/405237610e58ab9d4a9d5d54d9a0548a0c44227c/sections/g-real-restriction.tex#L5007-L5080)

<!--
% END FBE39
-->

<!--
% BEGIN FBE40
-->

<span id="claim:FBE40"></span>We calculate the starting energy of the actual mass record with the finite and real measures of FBE39. Let $F=E^+$, $f=[F:\mathbb Q]$, $\Delta=|D_F|^{1/f}$ and $g=g_0g_1$. The selected quadratic extension is unramified at finite places, so $\mathrm{rd}(E)=\Delta$. Put $q=r+1$ and
$$
 H_r=\frac{(r+1)(8r^2+10r+3)}3,\qquad
 c_N=\Delta^{2fr(r+1)(k-1)}g^{-2fr(r+1)}.
$$
At a finite place $v$ denote the measure of the two ordered unipotent coordinate sets by $U_v$ and that of the permitted cross Gram matrices by $Z_v$. These are additive volumes under the standard self-dual character. The expression called the ordinary volume in the mass record is the product of $U_v$ over the unmarked *finite* places. This follows by expanding its definition. The full numerator is $\prod Z_v$. A separate product of last-coordinate volumes occurs once in the numerator and once in the denominator. It is finite and positive since its factors are compact-open nonempty cosets or intersections of congruences on the marked data and are one outside finitely many places. Thus the record's actual initial integral is
$$
       B.\mathrm{IntN}=\frac{I_{\rm sep}}{c_N M_{\rm ar}},\qquad
       M_{\rm ar}=\prod_{v<\infty}U_v/Z_v .
$$
Here $I_{\rm sep}$ is the real integral on the positive diagonal Gram section with the original two coefficients and $2d^2c$ on each diagonal entry. The restriction to that section and the measure of its coordinates are precisely the definition of the continuous integral in the mass record. On the represented regular orbit the diagonal section is independent of its representative in the squared Hilbert–Schmidt norm, by compact unitarity and unipotent character covariance. [Mass datum and its scaling](https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Formalism/LocalToGlobal/SiegelLatticeTheory/CokernelGLCounts/MassDataConc.lean#L39-L92) · [Actual additive products at finite places](https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Formalism/LocalToGlobal/SiegelLatticeTheory/CokernelGLCounts/LocVol.lean#L194-L228) · [The continuous integral](https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Formalism/LocalToGlobal/SiegelLatticeTheory/ClosedLocalOrbits/RealObj.lean#L114-L164)

We compute $M_{\rm ar}$. At an ordinary place let $d_v$ generate the different of $F_v/\mathbb Q_p$. The quadratic integer algebra has self-dual Haar volume $|d_v|_v$. Indeed its annihilator is $d_v^{-1}$ times the lattice since the quadratic algebra is unramified, the two volumes multiply to one, and a base scalar acts in dimension two. Put $\alpha_i=d_v^{-(r-i)}$ for $0\le i\le r$. Integrality is imposed on $\alpha_i\alpha_jZ_{ij}$ and $\alpha_i^{-1}\alpha_j u_{ij}$ for $i<j$. Hence the exponents of $|d_v|_v$ in $Z_v,U_v$ are, respectively,
$$
 A=\sum_{i,j=0}^r\big(1+2(r-i)+2(r-j)\big),\qquad
 B'=2\sum_{0\le i<j\le r}\big(1-2(j-i)\big).
$$
Here $A=(r+1)^2(1+2r)$ and $\sum_{i<j}(j-i)=r(r+1)(r+2)/6$. Hence $A-B'=H_r$. At a marked split place of residue cardinality $Q$, reduction of all $q^2$ cross entries of the quadratic algebra costs $Q^{-2q^2}$. After translating and dividing by the uniformizer, the second condition fixes $Y_1+Y_2^{\mathsf t}$ modulo the prime. Congruence of the two marked norms modulo $g^2$ makes the specified Hermitian right side integral. For every residual $Y_1$ there is exactly one $Y_2$, giving $Z_v=Q^{-3q^2}$. In the unipotent coordinates the difference of the two lists is fixed on $r(r+1)/2$ quadratic coordinates, giving $U_v=Q^{-r(r+1)}$. Consequently
$$
              M_{\rm ar}=\Delta^{fH_r}g^{f(r+1)(2r+3)}.
$$
We used $\prod_v|d_v|_v^{-1}=|D_F|$ and the complete splitting of the marked primes. The same congruences have positive measure for the diagonal-coordinate factors above: the first residual value is fixed, and the second prescribes its trace to the next depth, a surjective map at a split place. [Finite coordinate lattices](https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Formalism/LocalToGlobal/SiegelLatticeTheory/CokernelGLCounts/LocVol.lean#L105-L152)

Let $N_v$ be the squared norm of the uncut actual section before division by its level-zero measure factor. In the separated integral, changing the complex coordinate $c_{r-a}$ by $(g/(2\pi))^{2a}$ for $1\le a\le r$ gives a Jacobian exponent $-2(2a+k)$ on the original density $|c_{r-a}|^{2(2a+k-1)}d^2c_{r-a}$. There are $r+1$ factors of two from the measures, including the final unchanged coordinate. The Hilbert–Schmidt inner product on a finite tensor product is a product on pure operators. Fubini therefore gives $I_{\rm sep}=K_{\rm loc}^{\,f}\prod_v N_v$ with
$$
 K_{\rm loc}=2^{r+1}\prod_{a=1}^{r}
       \left((g/(2\pi))^{2a}\right)^{-2(2a+k)} .
$$
In the level-zero denominator put $\kappa=2\pi/(g\Delta)$ and $d_e=2/(\Delta g^3)$. Its explicit factor is $\Gamma_0=d_e^{-(r+1)}\prod_{a=1}^r\kappa^{-4a(2a+k)}$. The powers of $g/(2\pi)$ cancel in $K_{\rm loc}\Gamma_0$. From $\sum a=r(r+1)/2$ and $\sum a^2=r(r+1)(2r+1)/6$ the result is $g^{3(r+1)}\Delta^{H_r+2r(r+1)(k-1)}$. Thus $(K_{\rm loc}\Gamma_0)^f=M_{\rm ar}c_N$ and
$$
          B.\mathrm{IntN}=\prod_{v\mid\infty}\frac{N_v}{\Gamma_0}.
$$
On each signed word this is the initial energy after the normalized cutoff limit by FBE26, FBE29–32 and the level-zero interpolation. The other two fields in the energy link are $B.e_1=\max(1,\mathrm{sd})$ and $B.\delta=C(r+1)(C/\Theta)^f$ by construction of the same mass datum. This proves the identification of the initial norm for this pair of measured coefficients. In the original invocation the initial argument of the real estimate is explicitly $B.\mathrm{IntN}$. The preceding computation identifies the integral to which that invocation refers. [Level-zero interpolation](SPECTRAL_LEVEL_ZERO_AND_CUTOFFS.md) · [Jin’s finite and real calculation](https://github.com/yuiyuiui/Natural-Language-Proof-Generalized-Riemann-Hypothesis/blob/405237610e58ab9d4a9d5d54d9a0548a0c44227c/sections/g-real-restriction.tex#L5133-L5208) · [Energy link on the actual words](https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Formalism/LocalToGlobal/SiegelLatticeTheory/FlagStabilizerTensors/SpectralTiesReal.lean#L222-L237)

<!--
% END FBE40
-->

<!--
% BEGIN FBE41
-->

<span id="claim:FBE41"></span>For the represented integral frames of the selected host, the finite-product density premise used at the terminal level follows from their local factors with the required order of quantifiers. Let $h=k-2r-2\ge f+5$, with $f=[F:\mathbb Q]$. For a finite place $v$ let $\ell(v)$ be its residue characteristic and $q_v$ its residue cardinality. Then $q_v\ge\ell(v)$ and any finite set of places of residue characteristic $\ell$ has at most $f$ elements, by $\sum_{v\mid\ell} e_v f_v=f$. The normalization $\alpha$ uses the first word's single-frame product at a marked place and both single-frame products at an ordinary place. Its Euler product is strictly positive. Its local factors are positive, and outside the finitely many word and marked primes the sums of the absolute logarithms converge by comparison with $C f\sum_{n\ge2}n^{-(k+1)}$. [The normalized density in the native data](https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Formalism/LocalToGlobal/SiegelLatticeTheory/CokernelGLCounts/DataInst.lean#L171-L205)

For any represented frame write $H_v$ for its primitive local density divided by the marked or ordinary reference at $v$. The integral lifting and first-residue counts for the actual two marked frames are given in the scalar-density calculation. Here is the passage from those counts to the native condition. At marked split places and at ordinary split places off the word primes one has $H_v\le1$. All dyadic places are in these cases. At an ordinary inert place the last marked vector has unit norm, so the residual corank loses at least one dimension. In the products of $1\pm q_v^{-j}$ for the density, every contributing index for an upper bound is then at least $h+1$. At a remaining split place the numerator is at most one and the denominator indices also start at least this high. The disjoint intervals of indices give
$$
        \log^+ H_v\ \le\ \frac{q_v^{-(h+1)}}{(1-q_v^{-1})(1-q_v^{-(h+1)})}
                     \ \le\ 4q_v^{-h}.
$$
Here a vanishing local density can be discarded when bounding positive products. The full product exists on every represented frame by the absolute logarithm bound at the good places, which allows the weaker starting index $h$ for the other sign. Let $\mathrm{sd}$ be the supremum of the represented unnormalized densities divided by the fixed positive $\alpha$. If $x<\mathrm{sd}$ and $x>1$, the supremum property gives a represented frame of ratio greater than $x$. Approximate its convergent product by a finite partial product greater than $x$. Bounding the factors individually gives
$$
          x\ \le\ \prod_{v\in S}\exp(4q_v^{-h})
$$
for the resulting finite set $S$. If $x\le1$, take the empty set, which also handles the empty collection of represented frames under the source convention. Thus the assertion is for *every* $x<\mathrm{sd}$ with its own finite set. Applying FBE36 bounds $\max(1,\mathrm{sd})$ before the row sum. [Primitive frame counts and the two reference factors](SPECTRAL_SCALAR_DENSITIES.md) · [Exact finite-set quantifiers](https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Formalism/HermitianCurvature/StatementPB.lean#L327-L331)

There is also a literal simplification at the last level. The source constructs the arithmetic datum of the two words by inserting their kernel with the two mark norms and the function $e(i)=0$ at every level. Hence $e(r+1)=0$ for this very datum. It follows before any bound on $\mathrm{sd}$ and before any estimate on the real energy. Together these verifications supply the density and zero-error steps at lines 1121–1123 of the native row for the selected integral presentation. [Construction with zero defect](https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Formalism/LocalToGlobal/SiegelLatticeTheory/CokernelGLCounts/DataInst.lean#L116-L137) · [Use at the terminal level](https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Formalism/HermitianCurvature/HermitianCurvatureProofs/GrowthOfBasic.lean#L1119-L1127)

<!--
% END FBE41
-->

## Why the actual period images survive the automorphic projection

<!--
% BEGIN FBE42
-->

<span id="claim:FBE42"></span>Let $X$ be a supplied high-gap Hida setting of the selected class with its normalized finite level $K$, finite character $\chi$ and native real discrete-series kernel $p_\infty$. Take a word $u$ with its prescribed Bessel wave and full finite column space. We show that its actual Poincaré period lies in the automorphic target used to form the Gram operator. The hypotheses on the setting enter in two places. For its original wave, SFS4 gives compact reproduction, weighted integrability and $p_\infty\in L^1$ at the stated gap and local multiplicity-one input. For every column $T$, PGR7 gives a measurable scalar seed $\Phi_T$ invariant on the left by its rational stabilizer $S$, right $K$-covariant by $\chi$, and satisfying the pointwise identity $\int p_\infty(z)\Phi_T(yz)\,dz=\Phi_T(y)$. These use the same finite character, infinite measures and levels as $X$. [Decay of the actual wave, SFS4](../../../research/modules/spectral/spectral_v60/main.tex#L197-L256) · [The scalar seed, PGR7](../../../research/modules/spectral/period_gram_v57/main.tex#L447-L501)

Let $\Gamma$ be the rational ambient group. In a fixed column the absolute value of each finite evaluation is bounded by a finite sum of norms of its coefficient vectors times the corresponding translates of the wave norm. Finiteness follows from the finite coarse class set and the compact-type equivariance at the marked level. For each of these positive seeds $W$ the first part of FBE37 gives a folded majorant $P^+(x)=\sum_{S\backslash\Gamma}|W(\gamma x)|$ in $L^2(\Gamma\backslash G)$. It is finite at every point: compact reproduction bounds each finite subsum at $x$ by its average over $xU$ with a common constant, and that average is bounded by the finite multiplicity of the compact translate times the $L^1$ norm of the folded seed. The argument uses one word at a time, so it applies equally to two copies of the same word. The finite sum of these majorants bounds the absolute Poincaré series of $\Phi_T$. Thus $P_T(x)=\sum_{S\backslash\Gamma}\Phi_T(\gamma x)$ converges absolutely at each $x$, is measurable and square integrable. Two transversals choose representatives differing by elements of $S$, so they give the same function by a bijection of summands. Right multiplication of the transversal by an element of $\Gamma$ proves left invariance.

To check the range assertion, test the convolution with $p_\infty$ against any $L^2$ function $b$ on the automorphic quotient. Enlarge $P^+$ to the finite majorant for the entire column. Right translations preserve quotient Haar. Tonelli and Cauchy–Schwarz give
$$
 \int |p_\infty(z)|\int_{\Gamma\backslash G}|b(x)|P^+(xz)\,dx\,dz
       \ \le\ \|p_\infty\|_1\|b\|_2\|P^+\|_2 .
$$
For the exchange of representatives, take $x$ in a measurable fundamental domain; the *sum* of the absolute values is invariant. This bound permits integrating each seed at $\gamma xz$ in the weak pairing. The pointwise reproduction of $\Phi_T$ then gives $R_{p_\infty}P_T=P_T$ in $L^2$. At a finite-level element $k$ the series transforms on the right by $\chi(k)$. The finite projector has kernel $\mathbf1_K(k)\overline{\chi(k)}/\mu(K)$. Since $|\chi(k)|=1$ and $0<\mu(K)<\infty$, its convolution fixes $P_T$ as well. The source defines the automorphic target as the range of the product of these operators. Applying the product to $P_T$ gives $P_T$ itself. This verifies all four clauses of the source period-range condition, including its quantifier over every transversal. [The original four clauses and target](https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Formalism/LocalToGlobal/SiegelLatticeTheory/HaarTransversals/PoincareInHH.lean#L179-L212) · [Finite normalized projector](https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Formalism/LocalToGlobal/SiegelLatticeTheory/HaarTransversals/UnitaryHaarProducts/InHHCut.lean#L372-L403)

In particular let $Q$ be the orthogonal projection onto this selected automorphic space (finite dimensional here by SFS1). Both normalized full-column period maps $\mathcal A_u$ and $\mathcal A_{u'}$ have their images in it, since the construction applies separately to the two original words with the common kernel and level. Then $(1-Q)\mathcal A_{u'}=0$. For their column inclusions $\iota$ this eliminates precisely the term $\iota_u^*\mathcal A_u^*(1-Q)\mathcal A_{u'}\iota_{u'}$ in PGR19. The unprojected Gram is carried to the finite full columns by the two Riesz anti-isometries. Taking the sum of squared column norms on an orthonormal basis preserves its Hilbert–Schmidt norm under these identifications. If the selected endpoint uses a different realization of the target, one still needs its isometry with this range carrying both period maps. The nonzero scale of a period remains part of that assertion. [Projected Gram formula, PGR19](../../../research/modules/spectral/period_gram_v57/main.tex#L1355-L1441) · [Norm under the two column identifications](https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Formalism/LocalToGlobal/SiegelLatticeTheory/FlagStabilizerTensors/RootLatticeThresholds/NormalizingConstantEq.lean#L24-L73)

<!--
% END FBE42
-->

## Both periods on a member of the selected family

<!--
% BEGIN FBE43
-->

<span id="claim:FBE43"></span>Let $\sigma$ be the original selector of linked bundles on its class. At $x>F.x_1$ and $a\in F.\mathrm{Ix}(x)$ put $b=\sigma(F,x,a)$. Write $R=b.R$ for its record and $S=b.S$ for its spectral tie. The latter is a tie *for $R$*: it contains the actual setting $X$, its full period data $Y$, a column comparison for every word, a row comparison, the local comparisons and a single adelic bridge with additive character and measures. Selecting $R$ and $S$ by these projections gives the selectors of the original argument with threshold $F.x_1$, also after restriction to the design subclass. The geometric part of this same $b$ supplies the core in GRT103. This is a pointwise construction for any supplied selector, including ones whose existence required a separate window argument. [The bundle and the two selectors](https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AbelianVarietyTheory/Definitions/GlobalTwisting/ColumnCompatibleSelection.lean#L63-L86) · [Columns, rows and local comparisons of the tie](https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Formalism/LocalToGlobal/SiegelLatticeTheory/FlagStabilizerTensors/STiesR.lean#L19-L39)

Under the original high-gap and standing hypotheses on this member, SFS4–5 give the finite-dimensional realization $h_F$ on $X,Y$ and FBE42 places every folded column in its automorphic target. Evaluate $I=S.hI(h_F)$ *once*. Write $U$ for its target isometry and $V_w$ for its column isometry at word $w$. Denote the original and concrete period maps by $P_w$ and $P^c_w$. The defining identity gives $UP_w=P^c_w V_w$. Taking inner products, for all $z,z'$ and all words $w,v$,
$$
 \langle P_w z,P_v z'\rangle
   =\langle P^c_w V_wz,P^c_v V_vz'\rangle,\qquad
 P_w^*P_v=V_w^{-1}(P^c_w)^*P^c_v V_v .
$$
In particular the two Gram blocks have identical operator norms, including on a restriction transported by the same $V_w,V_v$. The column identifications include the source's sharp-column inner products. Inserting the word normalizations multiplies both sides by the same factors because $I$ preserves the two word volumes. The local isomorphisms of $I$ apply at **every** prime and its term and pair bijections preserve the generic stratum, the scalar-pair predicate and the row values. The coherent choice of the two archimedean words comes from the same $S$ and the same $h_F$. Hence FBE39–42 and the Gram transport apply to the represented rows on this member whenever their arithmetic input hypotheses hold. The guarded uniform use in the original spectral link is quantified over precisely the projection $S\mapsto S.\mathrm{toSTies}$ of this selector. [The concrete columns and periods](https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Formalism/LocalToGlobal/SiegelLatticeTheory/FlagStabilizerTensors/ParametersTermRelations.lean#L238-L255) · [Intertwining both maps and transporting terms](https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Formalism/LocalToGlobal/SiegelLatticeTheory/FlagStabilizerTensors/ParametersTermRelations.lean#L286-L312) · [Precise selector in the link](https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AbelianVarietyTheory/Proofs/GlobalInterpolation/LinkAlt.lean#L16-L44)

<!--
% END FBE43
-->

## The frame inequality at the common guarded threshold

<!--
% BEGIN FBE44
-->

<span id="claim:FBE44"></span>On the family of FBE43 assume the original definite-space mass and volume comparison, the split-place critical-level estimate and the rank formula for the selected lattices. Then the word frame condition of SFS6 holds for **all** words and admissible indices beyond one threshold per family. We give the contradiction that produces its constant one.

Write $g=\mathrm{gg}(D)$, $\alpha=\mathrm{ka}(D)/g$, $r=D.R.r_S$, $T_w$ for the word prime, $Q_{w,\tau}$ for its critical level and $k=D.R.k$. For the rank formula the local coefficient at the trivial weight is read from the columns of $R$. The real theta realization of $R$ ties the definite-space volume to its mass, and the two marked primes and the word prime split by their norm conditions. Substituting these data in the class-number formula gives the rank row for all words once $x\ge\max(a,F.x_1+1)$, where $a$ is the record threshold. The convergent unitary Siegel–Weil comparison is one supplier of the required mass ratio. With the original formal degree and unramified Hermitian-lattice estimates the resulting level formula gives
$$
 \prod_\tau (Q_{w,\tau}/T_w)^k
 \le \exp(f\,2^{3-k})\,D^\star/d_w^S
 \le e^8 C_0 e^{k/4}.
$$
Here the standing column bound gives $D^\star/d_w^S\le C_0\Gamma_w^2$, the size inequalities give $\Gamma_w^2\le e^{k/4}$, and $f\le 2^k$ gives the bound $8$ in the exponent. The split-place critical-level estimate, at its family thresholds, gives $\alpha^{2r} Q_{w,\tau}\ge g^2$ for every $\tau$. [Rank row on the selected record](https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AbelianVarietyTheory/Proofs/FlagMeasures/ExactRanksAlongTiedFamily.lean#L16-L33) · [Volume and level inputs in this order](https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Formalism/LocalToGlobal/SiegelLatticeTheory/FlagStabilizerTensors/RootLatticeThresholds/SzHypFam.lean#L43-L65) · [Rank ratio and product upper bound](https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Formalism/SharpRestriction/CuspSpanNormBounds/BruhatCellsKronecker/CriticalLevelLowOfRefined.lean#L281-L366)

If $T_w\alpha^{2r}<1$, then $Q_{w,\tau}/T_w\ge g^2$ at every embedding. There is at least one embedding and $g\ge e$. Thus the displayed product is at least $g^{2k}$. For sufficiently large $k$ we have $C_0e^8<g^k$ and $e^{k/4}\le g^k$, contradicting its upper bound. This proves $1\le T_w\alpha^{2r}$ with the original normalization.

For uniformity take the maximum of the two size cutoffs, the cutoff for $m\ge2C_3$, the one for $C_u L\le m-1$, and the one for $k\ge C_0 e^8$. The fourth cutoff exists since $L=x^\varepsilon$, $m\ge x^{1/4}$ and $\varepsilon<1/4$. The family parameter threshold $sC_l\ge40$ suffices for the split-place estimate and for the gap bound of SFS7 after the original $C'$ threshold is also enforced. These choices all precede $a\in F.\mathrm{Ix}(x)$ and $w$. Take $C_0=3$ for the endpoint class. With the stated arithmetic inputs this supplies the frame condition at the guarded invocations of FBE43. Absolute estimates for the sums of the other pair strata still require their own arithmetic and counting bounds. [Uniform cutoff and admissibility](https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Formalism/SharpRestriction/CuspSpanNormBounds/BruhatCellsKronecker/CriticalLevelLowOfRefined.lean#L391-L436) · [Original family application of Siegel–Weil](https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AbelianVarietyTheory/Proofs/FlagMeasures/RanksFramesOfSiegelWeil.lean#L13-L17)

<!--
% END FBE44
-->

<!--
% BEGIN FBE45
-->

<span id="claim:FBE45"></span>Let $E/F$ be the CM extension, let $J=J^*$ be a nonsingular $M$-dimensional Hermitian form, and put $W=\operatorname{Mat}_{M,n}(E)$, $B=\operatorname{Herm}_n(E/F)$. Write $Q(X)=X^*JX$. The dimensions over $F$ are $2Mn$ and $n^2$. At a finite place $v$, or at all infinite places taken together, write $dX$ and $dS$ for the two self-dual measures in the statement. For a compactly supported test $\phi$ as there, the pushforward of $\phi\,dX$ under $Q$ has a canonical continuous density on the open set of invertible $S$. Its value is the integral of $\phi$ over $Q^{-1}(S)$ with the fibre measure $dX/dS$. This also treats a smooth test coupling all the real embeddings. [The domain and target measures](https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Formalism/UnipotentAdelicQuotients/SWXSDefs.lean#L94-L120) · [The density to be constructed](https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Formalism/UnipotentAdelicQuotients/SiegelWeilUnitaryConvergent.lean#L20-L41)

Indeed, if $Q(X)=S$, differentiation gives $dQ_X(Y)=Y^*JX+X^*JY$. For each Hermitian increment $A$ put $Y=XS^{-1}A/2$. The two summands are both $A/2$. Thus $dQ_X$ is onto on the entire inverse image of the open set. This works over $F_v$ above $2$ as well. In local submersion coordinates $(s,z)$ write $dX=J_0(s,z)\,dS(s)\,dz$ with $J_0>0$ the absolute Jacobian for the chosen measures. Near any invertible $s_0$ choose a compact neighborhood inside that open set. The intersection of its inverse image with the support of $\phi$ is compact. Cover it by finitely many such coordinate patches, using a smooth partition at infinity and compact open subpatches at a finite place. The sum of the integrals in $z$ of the localized tests times $J_0$ is continuous in $s$. If the support misses the fibre, its compact image misses a neighborhood of $s_0$. Change of variables and Fubini identify the integral of this sum on **each compact subset** of the regular locus with the integral of $\phi$ on its inverse image. Two such continuous functions agree everywhere on the open locus since Haar measure is positive on every nonempty open set. This proves chart independence and linearity for complex tests. The same change of variables defines a Radon measure supported on each regular fibre by integrating compactly supported tests there. [Weil, §§5–6, quotient gauges and their measures](https://doi.org/10.1007/BF02391774) · [Original condition on compact sets](https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Formalism/UnipotentAdelicQuotients/SWXSDefs.lean#L157-L171)

<!--
% END FBE45
-->

<!--
% BEGIN FBE46
-->

<span id="claim:FBE46"></span>Fix $T=T^*\in B(F)$ with $\det T\ne0$ and $2n<M$. Away from finitely many finite places, the density of FBE45 at $T$ for the prescribed integral lattice has the value
$$
 g_v(T)=\prod_{j=M-n+1}^{M}(1-\chi_v^{\,j}q_v^{-j}),
 \qquad
 \chi_v=\begin{cases}1&\text{at a split place},\\-1&\text{at an inert place}.\end{cases}
$$
Here $q_v$ is the residue cardinality. Exclude the places above $2$, the ramified places, the exceptional character conductors, the denominators of the bases and their inverses, and those where $J$ or $T$ fails to be integral and invertible or the test differs from the integral indicator. The source lattice then agrees with the full integral module. Both trace pairings are perfect over $\mathcal O_v$, so both integral boxes have self-dual volume one. [Finite tests in the original basis](https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Formalism/UnipotentAdelicQuotients/SWXSDefs.lean#L243-L261)

Put $D=2Mn-n^2$. The right inverse of $dQ$ in FBE45 works modulo the residue prime at each solution since $\overline T$ is invertible. In lifting a solution modulo $\varpi^e$ to one modulo $\varpi^{e+1}$ the new digit has a prescribed linear image and exactly $q_v^D$ possible values. The density on the shrinking balls about $T$ is therefore $q_v^{-D}$ times the number of residue solutions. This follows by dividing the volume of their preimage by $q_v^{-en^2}$ and using continuity at $T$. [Nelson's residue-count and lifting example](https://github.com/ultronozm/grh-workbook/blob/8590e35eb9a6e8cd07d546bd5b3b115ebac9672a/20261125T015500--siegel-weil-in-the-smallest-case__workbook.tex#L96-L120)

In the inert case these solutions are the isometric embeddings of the nonsingular $n$-space into the $M$-space over $\mathbf F_{q^2}$, with $q=q_v$. Every nonsingular Hermitian space there is isometric to the identity form by orthogonalization and surjectivity of the norm. Extending orthogonal bases gives transitivity and pointwise stabilizer $U_{M-n}(q)$. To count the orbit, for a nontrivial additive character of $\mathbf F_q$ and $c\ne0$ the sum $\sum_z\psi(cN z)$ is $1+(q+1)\sum_{a\ne0}\psi(ca)=-q$. Additive character orthogonality now gives $(q^{2m}-(-q)^m)/q$ vectors of length one in dimension $m$. Choosing the first unit vector and then an orthonormal basis of its complement gives $|U_m(q)|=q^{m^2}\prod_{j=1}^m(1-(-1)^j q^{-j})$. In the split case the form identifies the space with a vector space and its dual. A represented frame is a pair of $n$-frames with invertible prescribed cross pairing. The first frame and the joint kernel of the second give a direct sum. Changing the basis of that kernel is exactly its stabilizer $\mathrm{GL}_{M-n}(q)$ in $\mathrm{GL}_M(q)$. Counting ordered independent columns gives $|\mathrm{GL}_m(q)|=q^{m^2}\prod_{j=1}^m(1-q^{-j})$. In either quotient the leading power is $q^{M^2-(M-n)^2}=q^D$, which gives the displayed density.

For $n>0$ the absolute logarithm of a good factor is $O_{M,n}(q_v^{-(M-n+1)})$, with $M-n+1\ge3$. There are at most $[F:\mathbf Q]$ places above any rational prime. The sum converges, hence the net of products over finite sets of places converges. The finitely many exceptional values are precisely the fibre integrals in FBE45, including their Haar factors. A zero exceptional value makes every finite product containing that place zero. For $n=0$ all good factors are one. These arguments establish ordinary multiplicability also for complex tests with arbitrary exceptional factors. [Multiplicability in the source](https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Formalism/UnipotentAdelicQuotients/SiegelWeilUnitaryConvergent.lean#L32-L41)

<!--
% END FBE46
-->

<!--
% BEGIN FBE47
-->

<span id="claim:FBE47"></span>Write $H=U(J)$ and $[H]=H(F)\backslash H(\mathbf A_F)$. With $n,T$ as in FBE46, take a smooth compactly supported test at infinity and a restricted product of locally constant compactly supported tests at finite places. For every Haar measure $dh$ and every measurable fundamental domain $\mathcal F$, the fixed-Gram mean is
$$
 \frac{1}{\operatorname{vol}_{dh}(\mathcal F)}
 \int_{\mathcal F}\ \sum_{\substack{X\in W(F)\\Q(X)=T}}\Phi(h^{-1}X)\,dh
     =g_\infty(T)\prod_{v\nmid\infty} g_v(T).
$$
Here $g_\infty$ is the one integral for the joint archimedean test. Each $g_v$ uses the self-dual source and target measures for the same nontrivial character $\psi$ of $\mathbf A_F/F$. The identity allows any signature of $J$. [Exact mean, tests and finite product](https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Formalism/UnipotentAdelicQuotients/SiegelWeilUnitaryConvergent.lean#L15-L49)

First, $[H]$ has positive finite volume. For $M>0$, over an algebraic closure $H$ is $\mathrm{GL}_M$, whose algebraic characters are powers of the determinant. Conjugation of $E/F$ sends the determinant character to its inverse. Thus the connected reductive group $H$ has trivial group of $F$-rational characters. Borel's finite-volume criterion applies, and $M=0$ gives the one-point group. Haar measures exist. The discrete countable group $H(F)$ acts by left translations. Choose a countable cover of the quotient by images of neighborhoods on which the projection is injective, remove the preceding images from each, and lift the resulting Borel pieces. Their union is a fundamental domain. Partitioning any two domains by their countably many translates identifies their integrals on invariant integrable functions, also for domains defined up to null sets. A positive Haar rescaling cancels in the mean. [Borel, Theorem 5.6(i)](https://www.numdam.org/item/PMIHES_1963__16__5_0.pdf#page=18)

Weil's Theorem 5, formula (41), averages the rational points of maximal rank with fixed invariant and gives the integral over that adelic fibre with its quotient gauge. Apply it to the unitary space of $n$ vectors, whose invariant is the Hermitian Gram matrix. The unitary parameter in Weil's condition (B) is $1/2$, so the rank condition is precisely $M>2n$. If $r$ is the Witt index, $r\le M/2$ implies $M-r>n$. The theta integral of an absolute Schwartz majorant therefore converges. For the additional local transitivity hypothesis choose a finite place splitting in $E$ (there are infinitely many by Chebotarev). There the module is a space paired with its dual, and $M\ge2n$ permits a full zero-Gram frame consisting of the first $n$ basis vectors and $n$ dual vectors from the complementary coordinates. The full local isometry group is transitive on frames with any fixed pairing by Witt extension, equivalently by extending isomorphisms of the two frames and their kernels. The rational Gram $T$ is invertible, hence every point of its fibre has maximal rank. Inversion sends Weil's right quotient to the left quotient above and changes the action to $h^{-1}X$. Weil uses quotient mass one. The convergence criterion and the coefficient one in this range also appear in Yamana's Theorem 2. [Weil, §§44, 51–53, especially (41) on p. 77](https://doi.org/10.1007/BF02391774) · [Yamana, pp. 236–237](https://msp.org/pjm/2013/264-1/pjm-v264-n1-p11-p.pdf#page=3)

To match the gauge, choose $F$-bases of $W$ and $B$. The source Fourier pairing is $\sum_a\operatorname{Tr}_{E/F}h(X_a,Y_a)$ and the target pairing is $\tfrac12\operatorname{Tr}_{E/F}\operatorname{tr}(ST)$. Both are nondegenerate over $F$. For the second pairing this follows by testing the diagonal coordinates and then each off-diagonal pair using the nondegenerate field trace. Let $P_W,P_B$ be their rational matrices. Starting with the self-dual measure on $F_v$ for $\psi_v(st)$, the self-dual measure for a matrix $P$ is its coordinate product times $|\det P|_v^{1/2}$. Indeed substituting $P$ in Fourier inversion gives the factor $|\det P|_v^{-1}$ from the two transforms, which the squared measure multiplier cancels. This also proves uniqueness of the self-dual Haar scalar by testing a nonzero smooth compactly supported function with integrable Fourier transform. For the quotient of the two measures the extra factor at $v$ is therefore $|\det P_W/\det P_B|_v^{1/2}$. Its product, including infinity, is one.

Every such $\psi$ is obtained from the standard global character by multiplication by some $a\in F^\times$. The pointwise quotient measure then changes by $|a|_v^{(2Mn-n^2)/2}$, again of product one. The ground product measure gives $F\backslash\mathbf A_F$ covolume one, so in rational coordinates it gives exactly the adelic normalization of a rational gauge. This includes the different at finite places. The quotient gauge on the Gram fibre is locally characterized by $dX=(dX/dS)\,dS$, as in FBE45. A rational change in Weil's coordinates on the invariant space also has determinant of product one. FBE46 permits integration of the restricted product of tests against this gauge as the ordinary product of the fibre integrals. One can exhaust the restricted product by allowing arbitrary components at finitely many more places, keeping all other factors in their standard integral boxes. Outside the exceptional set the test itself already vanishes off these boxes and their positive volumes have a convergent product. This proves the asserted formula, including empty fibres. For $n=0$ the domain and target of the Gram map are points and both sides reduce to the value of the test. [Weil, §§3–6 and 44](https://doi.org/10.1007/BF02391774) · [Poonen, Corollary 5.4 and Proposition 5.5](https://math.mit.edu/~poonen/786/notes.pdf#page=27) · [Paired self-duality and the rational theta sum](https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Formalism/UnipotentAdelicQuotients/SWXSDefs.lean#L287-L309)

<!--
% END FBE47
-->

<!--
% BEGIN FBE48
-->

<span id="claim:FBE48"></span>The hyperplane volume argument uses the length of a **single** vector and allows every nonnegative measurable archimedean test, including indicators of individual Borel sets. Fix $M>2$ and $\beta\in F^\times$. Putting $n=1$ and $T=(\beta)$ in FBE47 gives the smooth one-vector formula. Indeed $s\mapsto(s)$ identifies $F_v$ with the Hermitian matrices of size one and $\tfrac12\operatorname{Tr}_{E_v/F_v}(st)=st$ for scalars. This holds on the infinite product as well. The identification preserves the self-dual target and turns the Gram map into $x\mapsto h(x,x)$. A vector of length $\beta$ is nonzero. [Comparison of scalar measures](https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AbelianVarietyTheory/Proofs/FlagMeasures/OneVectorCcOfSiegelWeil.lean#L307-L339) · [Application to the rational vectors](https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AbelianVarietyTheory/Proofs/FlagMeasures/OneVectorCcOfSiegelWeil.lean#L379-L426)

Fix the nonnegative finite tests in the volume problem. Their product is denoted by $\Phi_f$. Write $C=\prod_{v\nmid\infty}\int\Phi_v\,d\lambda_{v,\beta}$, where $\lambda_{v,\beta}$ is the actual fibre measure of FBE45. The nonnegative number $C$ is finite by FBE46. On the real vector space $W_\infty$ define two Borel measures. The first assigns to a Borel set $A$ the normalized integral
$$
  \mu_1(A)=\int_{[H]}\sum_{x\in W(F),\,h(x,x)=\beta}
       \mathbf 1_A((g^{-1}x)_\infty)\,\Phi_f((g^{-1}x)_f)\,d\bar g ,
$$
where $h(x,x)$ denotes the Hermitian length and $d\bar g$ has mass one. The second is $\mu_2=C\lambda_{\infty,\beta}$, regarded as a measure on $W_\infty$ supported on the length fibre. Positivity and countability give countable additivity of the first by Tonelli. For any nonnegative smooth compactly supported test their integrals agree by FBE47. The second is finite on compact sets by FBE45. Choosing a compactly supported smooth majorant of the indicator of each compact set shows that the first is also finite there. For an open set in $W_\infty\simeq\mathbf R^N$, exhaust it by compact subsets and insert smooth cutoffs between each compact subset and the open set. Inner regularity of locally finite Borel measures gives equality on all open sets, hence on all Borel sets. Applying simple functions and monotone convergence gives
$$
  \int_{[H]}\sum_{x:\,h(x,x)=\beta}
       f_\infty((g^{-1}x)_\infty)\,\Phi_f((g^{-1}x)_f)\,d\bar g
       =C\int f_\infty\,d\lambda_{\infty,\beta}
$$
for every measurable $f_\infty$ with values in $[0,\infty]$, with the usual extended-integral convention when $C=0$. The continuity of the fibre integrals of every compactly supported continuous test in FBE45 also makes any two admissible disintegrations agree at the specific regular value $\beta$. Agreement of those integrals identifies the fibre measures on Borel sets. Thus the identity applies even to indicators supported on the length fibre itself. In particular the same finite local masses and quotient normalization apply to the length-one test used to unfold the stabilizer of a unit vector. The further comparison with the actual family uses the selected self-dual lattice, its hyperplane, the real-place factors and the specified orbit unfolding. [Construction and comparison of the two Borel measures](https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AbelianVarietyTheory/Proofs/FlagMeasures/SiegelOneVectorMeasurableOfCompactSupport.lean#L134-L232) · [Use in the volume ratio](https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AbelianVarietyTheory/Proofs/GlobalInterpolation/VolumeRatio.lean#L12-L17)

<!--
% END FBE48
-->

<!--
% BEGIN FBE49
-->

<span id="claim:FBE49"></span>On the source's self-dual CM genus the one-vector mean gives the hyperplane volume ratio with the original group measures. Write $f=[F:\mathbf Q]$, $d_F=|\operatorname{disc} F|$, $M=\dim_E W\ge3$, and let $\eta$ be the quadratic character of $E/F$. The host used for this volume calculation is unramified at all finite places. Take a sign $\beta=1$ or $-1$ present at every real place of $W$. One can choose $x$ of length $\beta$ and a self-dual lattice in the given genus containing $x$. Put $W'=x^\perp$ with the induced lattice. If $\mathcal V$ denotes the source quotient volume for compact-dual Haar at infinity and unit volume on the finite lattice stabilizers, then
$$
 \frac{\mathcal V(W')}{\mathcal V(W)}
  =\left(\frac{(2\pi)^M}{(M-1)!}\right)^f
       \frac{d_F^{\,1/2-M}}{L_F(M,\eta^M)} .
$$
Here the $L$-value is the product of the **finite** Euler factors. In the host's notation $d_F=(2v)^f$. [Exact rank, volumes and ratio on the arithmetic setting](https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AbelianVarietyTheory/Proofs/GlobalInterpolation/VolumeRatioOfUnfolding.lean#L295-L325) · [Finite Euler factors and discriminant convention](https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AbelianVarietyTheory/BlockTheory/GlobalSignature/LocalDensityEuler.lean#L85-L143)

At a split finite place a self-dual lattice consists of an integral module and its dual, so it represents either unit. At an inert unramified place the nonsingular residue Hermitian form has a vector of nonzero length. Lift it and split off its unit line by orthogonal projection. Every unit of $\mathcal O_F$ at this place is a norm from the unramified quadratic extension. The residue norm is onto, and at each successive digit the correction is the residue trace, which is onto also in characteristic two. Induction gives an orthonormal lattice basis. In particular there are vectors of length $\beta$ at all finite places. At infinity existence is exactly the sign hypothesis. Apply Hasse–Minkowski over $F$ to the underlying quadratic form $h(y,y)-\beta t^2$. A rational isotropic point with $t\ne0$ gives $x=y/t$. If $t=0$, $h(y,y)$ itself contains a rational hyperbolic plane as a quadratic form and thus represents $\beta$. Choose such a rational $x$. At each exceptional finite place use Witt extension to carry an integral vector of length $\beta$ to $x$. Almost everywhere $x$ already belongs to the original lattice. Intersecting these locally specified lattices in $W(F)$ gives a lattice in the same genus containing $x$, self-dual because this condition is local. All local stabilizers have the same Haar volumes as before by conjugacy and unimodularity. At every place orthogonal projection along the unit line preserves the lattice. Its complementary lattice is self-dual. Any two unit vectors of length $\beta$ in a local lattice are carried to one another by matching their lines and their orthonormal complements (in the split case match the two integral direct sums). These identifications also show that the finite stabilizer of a vector inside the lattice stabilizer is exactly the stabilizer of the complementary lattice. [Use of the unit-vector complement and change of lattice](https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AbelianVarietyTheory/Proofs/GlobalInterpolation/VolumeRatioOfUnfolding.lean#L393-L421)

Choose the standard trace character. At a finite $v$ let $D_v=\#(\mathcal O_v/\mathfrak d_{F_v})$, where the different is relative to the rational local field. Its annihilator of $\mathcal O_v$ is $\mathfrak d_{F_v}^{-1}$. Thus $\mathcal O_v$ has self-dual volume $D_v^{-1/2}$. The integral source trace pairing is perfect in $\mathcal O_v$-coordinates before applying this character, by unimodularity and the étale trace dual. The source lattice has volume $D_v^{-M}$. The ratio of the source box volume to the target box volume is $D_v^{1/2-M}$. The normalized count for one unit vector is $1-\eta(v)^M q_v^{-M}$ by the residue calculation of FBE46. At residue characteristic two its lifting argument for one vector still applies because $dQ_x(y)=\operatorname{Tr} h(x,y)$ is onto on the residue lattice because $h(x,x)$ is a unit and the étale residue trace is onto. Hence the finite density product is
$$
 p=\prod_v D_v^{1/2-M}\bigl(1-\eta(v)^M q_v^{-M}\bigr)
   =d_F^{1/2-M}/L_F(M,\eta^M)>0 .
$$
Here $\prod_v D_v=d_F$ is the norm-of-the-different formula. [Local density on the actual lattice at each finite place](https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AbelianVarietyTheory/Proofs/GlobalInterpolation/VolumeRatioOfUnfolding.lean#L223-L245)

For the standard character the self-dual measure at a real embedding on $\mathbf C^M$ is $2^M$ times ordinary Lebesgue measure, by the trace pairing in FBE45. In the positive definite space disintegration by $s=\|x\|^2$ gives mass $c_M=(2\pi)^M/(M-1)!$ on $s=1$, by differentiating $2^M\pi^M s^M/M!$. The compact probability quotient $U(M)/U(M-1)$ thus has measure $c_M^{-1}$ times this fibre measure. In any signature, compare the two invariant densities at a positive or negative coordinate vector. The independent entries of a unitary Lie matrix are its imaginary diagonal entries and its complex entries on one side of the diagonal. The opposite entry is determined by conjugation and the two signature signs. Separating the column of the chosen vector leaves exactly the independent entries of the perpendicular unitary Lie algebra. The derivative of the orbit map on its remaining entries has absolute determinant one in these coordinates, including the imaginary entry in the vector direction. On the fibre the missing real entry is eliminated from $q(x)=\beta$ with derivative of absolute value $2$ at this basepoint, for either sign. These are the same absolute Jacobians as on the compact sphere. The group's compact-dual normalization fixes the density in these Lie coordinates to that of its compact form in each dimension. Consequently the quotient density is $c_M^{-1}$ times the fibre density in either signature, everywhere by transitivity. Over the $f$ places this factor is $c_M^{-f}$. [Compact-dual comparison at the basepoint and its translation](https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AbelianVarietyTheory/Proofs/GlobalInterpolation/IsCompactMatrixEntryAbsSumSublevel.lean#L252-L330) · [Jin's compatible compact-volume calculation](https://github.com/yuiyuiui/Natural-Language-Proof-Generalized-Riemann-Hypothesis/blob/405237610e58ab9d4a9d5d54d9a0548a0c44227c/sections/g-real-restriction.tex#L5383-L5397)

Take the finite test to be the indicator of the completed lattice and a nonnegative compactly supported real test positive at $x_\infty$. Its integral $a$ on the infinite length fibre is finite and positive by the submersion coordinates. FBE48 evaluates the normalized mean as $a p$. Conversely, all rational vectors of this length form one orbit by Witt extension. Expanding the sum into cosets of $U(W')(F)$ unfolds the unnormalized integral to the stabilizer quotient. At the finite places the integral vectors form one orbit under the lattice stabilizer, with quotient volume $1/1=1$ by the preceding lattice decomposition. The archimedean quotient integral is $c_M^{-f}a$. The resulting mean is $(\mathcal V(W')/\mathcal V(W))c_M^{-f}a$. Cancelling $a$ proves the displayed ratio for the normalizations enforced by the original volume tie. [Two evaluations on the same test](https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AbelianVarietyTheory/Proofs/GlobalInterpolation/VolumeRatioOfUnfolding.lean#L327-L391)

<!--
% END FBE49
-->

<!--
% BEGIN FBE50
-->

<span id="claim:FBE50"></span>The definite instance of the point-count input has zero error. For the indefinite instance, the estimate for elements away from the identity on the part of the quotient with controlled lattice size follows from the native arithmetic ball bound and the lowest-type decay estimate, with rank threshold depending only on the outer level exponent. We give the constants because the field degree and the inner level can both vary. Put $n=\dim W$, $f=[F:\mathbf Q]$, $r_0=\operatorname{rd}(E)$, $N=n^2f$, $H=nf\log n$ and $X=nfr_0gb$. Here $b\ge2$, $1\le g\le b^A$, $\log f\le\sqrt n$, $q^2\le n$ in signature $(n-q,q)$, and the distinguished completely split prime $g_0$ exceeds $4n$. Write $V$ for the quotient volume and $a$ for the identity term (the formal degree times $e(1)$). Thus $D^\star=aV$. [Native hypotheses and count](https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Formalism/SharpRestriction/CuspSpanNormBounds/PlaceDegreeData.lean#L364-L378) · [Roadmap, B8.53](https://github.com/rh-lean-roadmap/rh-lean-roadmap/blob/0be265ccb325908c67f872361d564c66b99e96f7/docs/src/book/main.tex#L24135-L24182)

The finite support forces a contributing rational $\gamma$ to preserve the translated lattice. Hence $\operatorname{tr}(\gamma^j)-n$ is integral. Unipotent reduction at every place above $g_0$ makes this element divisible by $g_0$ for every $1\le j\le n$, since $g_0$ splits unramified. In definite signature every archimedean conjugate has absolute value at most $2n<g_0$. If the element were nonzero, the absolute norm after division by $g_0$ would be a positive integer strictly less than one. All these traces therefore equal $n$. Newton's identities give characteristic polynomial $(z-1)^n$. At a definite real embedding a unitary matrix is diagonalizable, so $\gamma=1$. The quotient is compact modulo the discrete rational points (anisotropy and Borel's Theorem 5.6(ii)). The counting projector on this quotient has the folded finite-level and compact real coefficient as kernel, by Schur orthogonality and unfolding. Its continuous diagonal is precisely $a$ and its trace is $aV$. Equivalently, at a fixed open level there are finitely many finite cosets with compact archimedean fibres, where the compact type projection has finite rank. [Definite trace and projector in the original comparison](https://github.com/rh-lean-roadmap/rh-lean-roadmap/blob/0be265ccb325908c67f872361d564c66b99e96f7/docs/src/book/main.tex#L58790-L58801)

Suppose $q\ge1$. For the translated Hermitian lattice at $x$, let $\tau_1$ be the smaller of $1/2$ and the least normalized size of a nonzero sublattice. Define $\eta=1/(10^6 n^8f^2)$ and $\tau_*=X^{-11q}$. On $\tau_1\ge\tau_*$, the source's arithmetic ball estimate bounds the number of elements with displacement $d_v\le R_v$ by $A_x\exp(2n^2\sum_vR_v)$, where $A_x=(3\sqrt n/\tau_1^2)^{2N}$. Here $d_v$ is the Euclidean norm of the logarithms of real singular values. Use the lowest-type compression bound at gap $h$ and $|e(g_f)|\le e(1)$ from positive type. The absolute contribution of an element is then at most $a\exp[-(h/8)\sum_v\min(d_v^2,d_v/\sqrt{2q})]$. We estimate the sum over elements having some $d_v>\eta$. [Ball count and compression estimate, B8.53a](https://github.com/rh-lean-roadmap/rh-lean-roadmap/blob/0be265ccb325908c67f872361d564c66b99e96f7/docs/src/book/main.tex#L24184-L24199)

Divide each coordinate into $[0,\eta]$ and $(2^{j-1}\eta,2^j\eta]$, $j\ge1$. Put $T=h\eta^2/16$. For $d>\eta$, one has $\min(d^2,d/\sqrt{2q})\ge\eta d$. Multiplying the decay by the packing exponential gives a weight at most $\exp(-T2^{j-1})$ on shell $j$ provided $4n^2\eta\le T$. The zero shell has weight at most two. For $T\ge1$ the positive weights sum to at most $2e^{-T}$ by comparison with a geometric series. Designating one positive shell coordinate and summing the other coordinates gives at most $a A_x\,2f3^f e^{-T}$. For a nonempty range $A\ge0$. The original gap $h\ge C n^{19}f^5\log(br_0)$ with $C\ge8\cdot10^{14}(A+4)$ gives $T\ge50(A+4)n^3 f\log(br_0)$. On the indicated region,
$$
 \log A_x+\log(2f)+f\log3+N
 \le 2N\{\log(3\sqrt n)+22q\log X\}+\log(2f)+f\log3+N .
$$
Divide by $n^3f$. Using $\log X\le\log n+\sqrt n+(1+A)\log(br_0)$ bounds the right side by $44+o(1)+44(1+A)\log(br_0)/\sqrt n$. The $o(1)$ is uniform in $f,b,g,r_0$. As $\log(br_0)\ge\log2$, this is at most $T/(n^3f)$ for large $n$ depending only on $A$, and the two shell conditions also hold. The sum away from the identity is therefore at most $a e^{-N}$ pointwise. Integrating over the indicated region gives at most $e^{-N}D^\star$. [Original dyadic summation](https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AbelianVarietyTheory/Proofs/FlagMeasures/SummableOfSupport.lean#L42-L124) · [Uniform size comparison](https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AbelianVarietyTheory/Proofs/FlagMeasures/FarTermsModerateRegionOfFlagBound.lean#L53-L113)

<!--
% END FBE50
-->

<!--
% BEGIN FBE51
-->

<span id="claim:FBE51"></span>The other moderate-region contribution in FBE50 comes from nonidentity elements with every $d_v\le\eta$. Here is the explicit cancellation between the count of these elements and the volume of a thin lattice flag. We use the source's density bound for the successive short isotropic sublattices in the Harder–Narasimhan filtration. Put $\delta=3\sqrt{n\eta}$. All traces of powers in the integrality argument of FBE50 still agree with $n$, because at each real place the absolute value of a trace difference is at most $n(e^{n\eta}+1)<3n$. Thus $\gamma$ is unipotent. For $y=x_v^{-1}\gamma x_v$, using $\operatorname{tr} y=n$ gives $\|y-1\|_{\rm HS}^2=\|y\|_{\rm HS}^2-n\le n(e^{2\eta}-1)\le\delta^2$. If $\tau_1=1/2$, the product separation bound between two distinct integral endomorphisms gives at least $(1/2)^2$ for the geometric mean of their coordinate operator norms. Since $\delta<1/4$, only the identity is possible. [Near elements and their lowering operators](https://github.com/rh-lean-roadmap/rh-lean-roadmap/blob/0be265ccb325908c67f872361d564c66b99e96f7/docs/src/book/main.tex#L58799-L58823)

Otherwise write the small grades as $t_1<\cdots<t_s<1/2$ with rank increments $j_i\ge1$ and $J=\sum_i j_i\le q$. The size of a sublattice is the covolume divided by the fixed field factor, raised to the reciprocal of its real dimension. The bound on $\gamma-1$ carries the filtration at cutoff $t$ into the filtration at $\delta t$. For a nonzero image use the induced source quotient and bound the determinant by the product of the operator norms. All quotients of the part at level $t$ have size at most $t$. The central graded piece has smallest sublattice size at least $1/2$ and largest quotient size at most $2$, by duality. A nonzero endomorphism of this central piece consequently has geometric mean operator norm at least $1/4$. Thus the middle diagonal block of $\gamma-1$ also vanishes. Order the strict lowering blocks by their distance from the diagonal. At fixed earlier blocks, subtract two possibilities. The equation $y^*Jy=J$ determines the block dual to the first differing one. A block paired with itself has skew-adjoint difference. The remaining choices at a block form a set whose distinct points, in maximum real operator norm over the places, are separated by the ratio of least target size to largest source quotient size. Indeed apply the same determinant bound to the nonzero image of their difference.

For two distinct small grades $i<k$, the scales are $t_i/t_k$ and $t_it_k$, each of real dimension $2fj_i j_k$. The scale between a small grade and the middle is $t_i$, of dimension $2fj_i(n-2J)$, and the self-paired scale is $t_i^2$, of dimension $fj_i^2$. Write $(\lambda,m_\lambda)$ for this list with multiplicities. The separation is at least $\lambda/3$ in each case, using $t_i/2$ for the middle. Differences from a fixed representative are bounded by $2\delta$ on the graded spaces with the subspace and quotient norms. Disjoint norm balls of half the separation thus give at most $(1+12\delta/\lambda)^{m_\lambda}$ choices. Multiply over the free blocks. The flag density supplies the opposite powers $\prod_\lambda\lambda^{m_\lambda}$ and has coefficient at most $e^{-JH/2}$ times $\prod_i2fj_i\,dt_i/t_i$. As $\lambda\le1$ and $\sum m_\lambda\le3Jnf$, the product from packing and density is at most $\exp(36\delta qnf)\le2$ for the $\eta$ of FBE50 and large $n$. [Native packing on the successive graded blocks](https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AbelianVarietyTheory/Proofs/FlagMeasures/PowLePowRatio.lean#L479-L582) · [Precise flag density, B8.53b](https://github.com/rh-lean-roadmap/rh-lean-roadmap/blob/0be265ccb325908c67f872361d564c66b99e96f7/docs/src/book/main.tex#L24202-L24223)

On the moderate region $t_i\ge\tau_*$, each logarithmic integral is at most $Y=22fq^2\log X$. The hypotheses $\log\log r_0\le n$ and $\log\log b\le H/16$ give $\log X\le\log n+\sqrt n+e^n+(1+A)e^{H/16}$. Because $H\ge n\log n$, for large $n$ depending only on $A$ we have $Y\le e^{H/8}$, including the factors $f,q^2$. A given type therefore contributes at most $2e^{-3JH/8}D^\star$, since $s\le J$ and the coefficient at each real tuple is at most $a$. There are fewer than $2^q$ nonempty compositions of integers up to $q$. Their total is at most $e^{-H/4}D^\star$ for sufficiently large $n$. This proves the moderate near bound from the indicated density and lattice separation. [One-type integral](https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AbelianVarietyTheory/Proofs/FlagMeasures/NearTermsModeratePointsOneTypeBound.lean#L40-L97) · [Uniform sum over types](https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AbelianVarietyTheory/Proofs/FlagMeasures/OneTypeArith.lean#L57-L157)

<!--
% END FBE51
-->

<!--
% BEGIN FBE52
-->

<span id="claim:FBE52"></span>Write $D$ for the rank of the finite automorphic counting projector with continuous kernel $K$ and $D^\star=aV$ for the integral of its diagonal identity term. Let $\alpha=e^{-H/4}$ and $\beta=e^{-N}$ in the notation of FBE50. The exact two inputs on $\tau_1<X^{-11q}$ used alongside the moderate bounds are
$$
 \operatorname{vol}\{\tau_1<X^{-11q}\}\le\alpha V,\qquad
 \int_{\tau_1<X^{-11q}} K(x,x)\,dx\le\beta D .
$$
A small volume alone allows large diagonal values there. For instance the rank-one projector generated by a normalized function supported on a set of probability $s$ has all its trace on that set, for every $s>0$. The second inequality concerns the cuspidal vectors of this particular projector. [Deep mass of the counting projector, B8.53e](https://github.com/rh-lean-roadmap/rh-lean-roadmap/blob/0be265ccb325908c67f872361d564c66b99e96f7/docs/src/book/main.tex#L24253-L24272)

Integrate the difference between $K(x,x)$ and $a$. On the moderate region FBE50–51 give a combined cost $(\alpha+\beta)D^\star$. On the complement the nonnegative diagonal and the missing identity term cost at most $\beta D+\alpha D^\star$. Since $D\le D^\star+|D-D^\star|$, we obtain
$$
 (1-\beta)|D-D^\star|\le(2\alpha+2\beta)D^\star .
$$
For all sufficiently large $n$ irrespective of $f\ge1$, both $\alpha,\beta$ are at most $e^{-H/16}/8$ and $1-\beta\ge1/2$, using $N/H=n/\log n$. Thus $|D-D^\star|\le e^{-H/16}D^\star$. This also gives $D=0$ when $D^\star=0$. [Trace comparison](https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AbelianVarietyTheory/Proofs/FlagMeasures/DiscreteSeriesCountingOfFiniteAndBounds.lean#L34-L142)

The passage to the family fixes one function **before** the family member and level. For each real $A$ let $n_0(A),C_0(A)\ge0$ be thresholds valid in the uniform point theorem with $c=c_b=1/16$. These include its lowest-type decay, flag-density and deep-trace hypotheses. For the outer list $\ell$ set $A(\ell)=2(\ell[6]+1)$, with zero default at a missing index. On a family's actual list the seventh entry is $C_{YL}$. Set the rank threshold and gap coefficient to $n_0(A(\ell)),C_0(A(\ell))$ and take $c_{\rm Ic}=c=c_b=1/16$. Then $C\ge0$ and $A(\ell)=2(C_{YL}+1)$ on every member. The point theorem quantifies over the automorphic data and idempotent. Imposing an additional predicate on that same idempotent restricts the admissible tests, so the estimate holds for every such predicate with the same thresholds. Applying it for each index supplies the required family implication. The remaining analytic verifications are the uniform hypotheses of the point theorem itself. [Exact choices in the counting record](https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AbelianVarietyTheory/Proofs/FlagMeasures/CountConstantsOfSiegelWeil.lean#L11-L24) · [Level predicate and transport](https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Formalism/SharpRestriction/CuspSpanNormBounds/BridgeCountE.lean#L45-L88)

<!--
% END FBE52
-->

## The lowest-type coefficient and separation of integral matrices

<!--
% BEGIN FBE53
-->

<span id="claim:FBE53"></span>The shell argument of FBE50 uses two pointwise bounds. First consider an integral endomorphism of the translated Hermitian lattice, viewed in the archimedean frames. For a nonzero difference of two such endomorphisms, pass to the saturated quotient by its kernel and to the saturation of its image. The induced map is of the same positive rank on both sides. On exterior powers the determinant of this integral map can only increase the target covolume by its integral index. At place $v$ the determinant norm is bounded by $\|A_v\|_{\rm op}^{\operatorname{rank}A}$. The normalized target size is at least $\tau_1$, and the normalized source quotient size is at most $\tau_1^{-1}$ by self-duality of the filtered lattice. Multiplying over the places and taking the appropriate roots gives $(\prod_v\|A_v\|_{\rm op})^{1/f}\ge\tau_1^2$. To count elements with $d_v\le R_v$, scale their coordinates by $e^{\bar R-R_v}$, $\bar R=\sum_vR_v/f$. Their geometric mean separation is unchanged, hence the distance in the maximum of the Hilbert–Schmidt norms is at least $\tau_1^2$. The points lie in its ball of radius $\sqrt n e^{\bar R}$. Disjoint balls of radius $\tau_1^2/2$ in real dimension $2n^2f$ give $(1+2\sqrt n e^{\bar R}/\tau_1^2)^{2N}$. This is at most $(3\sqrt n/\tau_1^2)^{2N}\exp(2n^2\sum_v R_v)$, as used in FBE50. [Determinant separation on the count lattice](https://github.com/rh-lean-roadmap/rh-lean-roadmap/blob/0be265ccb325908c67f872361d564c66b99e96f7/docs/src/book/main.tex#L58886-L58898)

For the real coefficient start from the native compression formula on its actual lowest compact type $S$. At $\exp Z$, $Z=Z^*$ has only off-signature blocks. The formula is the Haar average over the compact group of the rank-one projections onto translates of a unit highest-weight vector times $\dim S$, with weight $\prod_{i<n}\Delta_i(e^{Y})^{-s_i}$. Here $Y=k^{-1}Zk$, $\Delta_i$ is the leading principal minor and $s_i=\lambda_i-\lambda_{i+1}+1>0$. The angle between two distinct signature positions has weight gap at least $h$. Write $d=\|Z\|_{\rm HS}$. In an eigenbasis of $Y$, Cauchy–Binet gives $\Delta_i(e^{tY})=\mathbb E e^{tU_i}$, where $U_i$ is the sum over an $i$-element eigenvalue set, with probabilities the squared absolute minors of the change of basis. The probabilities sum to one at $t=0$. Differentiating the determinant at zero gives $\mathbb E U_i=\operatorname{tr}Y_{[i]}=0$ and
$$
 \mathbb E U_i^2=\operatorname{tr}\big((Y^2)_{[i]}-Y_{[i]}^2\big)
 =\sum_{b\le i<a}|Y_{ab}|^2.
$$
At most $2q$ eigenvalues are nonzero, hence $|U_i|\le\sqrt{2q}\,d$. Take $t=\min(1,1/(\sqrt{2q}\,d))$ when $d>0$. For $|z|\le1$, $e^z\ge1+z+z^2/3$ by Taylor's integral remainder (its coefficient is minimized at $-1$). Concavity of $z^t$ gives $\mathbb E e^{tU_i}\le(\mathbb E e^{U_i})^t$. Since $0\le t^2\mathbb E U_i^2\le1$ and $\log(1+u/3)\ge u/4$ on this interval, we obtain $\log\Delta_i(e^Y)\ge t\mathbb E U_i^2/4$. [Spectral expansion of the minor](https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AbelianVarietyTheory/Proofs/FlagMeasures/LeadMinorExpHermitianEqConvexExpSum.lean#L34-L88) · [The second moment](https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AbelianVarietyTheory/Proofs/FlagMeasures/DerivLeadMinorExpHermitianZeroDiag.lean#L121-L190)

For every nonzero entry $Y_{ab}$ with $a>b$, the sum of $s_i$ over $b\le i<a$ is at least $h$. Summing the variance identity with these weights gives at least $hd^2/2$. Each positive projection in the compression formula therefore carries a scalar weight at most $e^{-htd^2/8}$. Without the scalar weights their normalized compact average is the identity on $S$ by Schur orthogonality. Positivity gives the same upper bound for the operator norm. The compact factor in the polar decomposition acts unitarily and the case $d=0$ follows by unitarity. The resulting exponent is exactly the $\min(d^2,d/\sqrt{2q})$ of FBE50, without a dimension factor for $S$. FBE60–61 identify this formula on the entire prescribed compact type of each admitted discrete series. [Weighted product of minors](https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AbelianVarietyTheory/Proofs/FlagMeasures/ProdLeadMinorDecay.lean#L121-L176) · [Passage to the actual group element](https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AbelianVarietyTheory/Proofs/FlagMeasures/LowestKTypeDecayGapOfCompressionFormulaGap.lean#L11-L32) · [Compression on the specified type](https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AbelianVarietyTheory/Proofs/FlagMeasures/LowestKTypeCompressionFormulaOfStrictLowestKType.lean#L22-L81)

<!--
% END FBE53
-->

## Volume of the arithmetic quotient in the cusp bound

<!--
% BEGIN FBE54
-->

<span id="claim:FBE54"></span>The absolute volume needed for the deep trace can be bounded on the unramified, self-dual CM host of FBE49. Write $r=\operatorname{rd}(E)$, $Y=r^f$, $L=1+\log Y$, $N=n^2 f$. Let $P_0=\prod_v c_v$, where $c_v$ times the original real Haar measure has Hilbert–Schmidt density one. Write $K_f$ for the full lattice stabilizer, $k_R=\mu_f(K(g))$ for the principal congruence volume and $\mathcal W=P_0V/\mu_f(K_f)$. Changing from the compact-dual normalization of FBE49 to density one multiplies the rank-$M$ compact volume divided by the rank-$(M-1)$ volume by $(2\pi)^M/(M-1)!$. Indeed the tangent column of a unit vector has one imaginary coordinate of weight one and $M-1$ complex coordinates of Hilbert–Schmidt weight $\sqrt2$. Its sphere volume $2\pi^M/(M-1)!$ therefore acquires the factor $2^{M-1}$. On both groups the independent Lie coordinates give the same absolute Jacobian in all signatures. Since $E/F$ is unramified at finite places, $d_F=r^f$. FBE49 thus gives $\mathcal W_M/\mathcal W_{M-1}=r^{f(M-1/2)}L_F(M,\eta^M)$ for every $M\ge3$. Remove negative unit lines first and end in definite rank two. There are at least two positive dimensions under $n\ge8,\ q^2\le n$. [Gauge change in the volume recurrence](https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AbelianVarietyTheory/Proofs/FlagMeasures/EnnrealVolumeRatioStepCancel.lean#L77-L119) · [Descent to the compact rank-two quotient](https://github.com/rh-lean-roadmap/rh-lean-roadmap/blob/0be265ccb325908c67f872361d564c66b99e96f7/docs/src/book/main.tex#L58900-L58915)

In definite rank two, Euclidean volume at the complex places gives covolume $(r^2/4)^f$ for the self-dual lattice. This follows from the trace discriminant and the determinant of the metric on a Hermitian basis, or by the self-dual trace pairing followed by its factor of two at each complex coordinate. The product of balls of squared radius $r$ has volume $(\pi^2r^2/2)^f>2^{4f}(r^2/4)^f$. Minkowski's theorem gives a nonzero integral vector with squared length at most $r$ at all places. Saturate its line. The pairing ideal of this rank-one lattice is $\mathfrak a\mathcal O_E$ for an integral ideal $\mathfrak a$ of $F$. Indeed a local generator gives its real Hermitian norm, and changing generators multiplies by a unit norm. The squared length of the chosen vector lies in this ideal, so $N_F\mathfrak a\le Y$. By self-duality, the discriminant modules of the saturated line and its saturated perpendicular are anti-isometric. Indeed the unimodular overlattice modulo the orthogonal sum injects into each discriminant module by saturation. Its squared order is the product of their orders by unimodularity. Both injections are therefore onto. Each module is of rank one over $\mathcal O_E/\mathfrak a\mathcal O_E$, hence cyclic (an invertible module over a finite product of local Artin rings is free). For fixed line classes, a graph is determined by one image and there are at most $(N_F\mathfrak a)^2$ possibilities. [Two lines and the integral gluing data](https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AbelianVarietyTheory/Proofs/FlagMeasures/RankTwoDefiniteUnimodularHermitianClassBound.lean#L168-L214)

An ideal class specifying a line and its pairing ideal determines its positive metric up to a totally positive unit modulo unit norms. Squares of real units are norms, giving at most $2^f$ choices by the unit theorem. In degree $d$, the number of integral ideals with norm at most $Y$ is at most $Y(1+\log Y)^{d-1}$. At each rational prime the Euler coefficients are bounded termwise by those of $\zeta(s)^d$, and summing over the first $d-1$ factors in an ordered product proves this estimate. Minkowski's ideal-class bound in $E$ gives an integral representative of norm at most $Y=\sqrt{|d_E|}$ in each class since the prefactor $(4/\pi)^f(2f)!/(2f)^{2f}$ is at most one. Thus the number of classes in rank two is at most $YL^f(2^f Y L^{2f})^2Y^2=4^fY^5L^{5f}$. Each automorphism group has order at least one, and the compact gauge volume of $U(2)$ is $8\pi^3$ per place. This bounds $\mathcal W_2$. [Rank-two class bound](https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AbelianVarietyTheory/Proofs/FlagMeasures/RankTwoDefiniteUnimodularHermitianClassBound.lean#L225-L254) · [Compact volume and rank exponent](https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AbelianVarietyTheory/Proofs/FlagMeasures/AbsoluteHermitianVolumeBoundArith.lean#L10-L34)

The Euler product costs at most $\prod_{M\ge3}\zeta(M)^f\le e^f$, since $\sum_{M\ge3}(\zeta(M)-1)=\sum_{a\ge2}1/(a^2(a-1))=2-\zeta(2)<1$. Let $Z\ge2$, $r\le Z$ and $2fr\le Z^2$. Then $L\le Z^2$ and $8\pi^3\cdot4e\le2^{12}$. Summing $M-1/2$ from $3$ to $n$ gives $(n^2-4)/2$. Consequently $\mathcal W\le Z^{f(12+5+10+(n^2-4)/2)}\le Z^N$ for $n\ge8$. Finally reduction modulo $g$ embeds $K_f/K(g)$ in the endomorphisms of the rank-$n$ projective lattice modulo $g$. Local freeness gives $g^{2fn^2}$ such endomorphisms. Hence $P_0V\le Z^N g^{2N}k_R$. The value $Z=X=nfrgb$ satisfies all three conditions in FBE50. [Insertion of the genus mass and Euler factors](https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AbelianVarietyTheory/Proofs/FlagMeasures/AbsoluteHermitianVolumeBoundArith.lean#L49-L123) · [The absolute volume at the actual level](https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AbelianVarietyTheory/Proofs/FlagMeasures/DeepRegionKernelDiagonalBound.lean#L48-L91)

<!--
% END FBE54
-->

## The volume of the short-flag region

<!--
% BEGIN FBE55
-->

<span id="claim:FBE55"></span>To bound the volume term in FBE52, let $\mathbf j=(j_1,\ldots,j_a)$ be a nonempty isotropic flag type, $J=\sum j_i\le q$, $p=n-q$, $S=\sum j_i^2$, $d_U=2nJ-2J^2-S$. Keep the measured parabolic unfolding of the original host. It bounds the filtration indicator by summing over rational isotropic flags and integrating the nonnegative test over their stabilizers. Conjugation on the free off-diagonal blocks gives the scales $\lambda^{m_\lambda}$ listed in FBE51. Changing each determinant norm from the covolume to its $(2fj_i)$th root gives the logarithmic measure $2fj_i\,dt_i/t_i$. We compute the size of the coefficient left by this unfolding. With $S_l=\prod_{u=1}^l 2\pi^u/(u-1)!$ and $R_E=\operatorname{res}_{s=1}\zeta_E(s)$, it is bounded by
$$
 (r/2)^{-fd_U/2}2^{-f(nJ-J^2+J/2)}
 \left(\frac{S_pS_q}{S_{p-J}S_{q-J}\prod_i S_{j_i}}\right)^f
 \frac{R_E^a\prod_i\prod_{l=2}^{j_i}\zeta_E(l)}
      {\prod_{M=n-2J+1}^n L_F(M,\eta^M)} .
$$
For clarity, the Haar factors entering this expression are the following. Each norm-one general linear Levi of rank $j$ has volume $R_E(r/2)^{fj^2}\prod_{l=2}^j\zeta_E(l)$ in the source gauge. Rank one gives $h_E\pi^f\operatorname{Reg}_E/w_E$ by the ideal classes, complex angular measures and unit domain, equivalently $R_E(r/2)^f$. The source's general linear Siegel step multiplies this by $(r/2)^{f(2j-1)}\zeta_E(j)$ at rank $j$. The real compact quotient factor per place is $2^{-d_U/2+nJ-J^2-J/2-S}S_pS_q/(S_{p-J}S_{q-J}\prod_i S_{j_i})$. The other contributions are the unipotent covolume $r^{fd_U/2}$, the factors $2^{fj_i^2}$ converting the Levi gauges, and division by the $2J$ unitary rank steps of FBE54. Those steps contribute $r^{f(2nJ-2J^2)}\prod_M L_F(M,\eta^M)$. Multiplication gives the displayed coefficient, using $d_U=2nJ-2J^2-S$. FBE63 derives the general linear factors in this gauge. FBE64 proves the integral orbit and sum over classes. The individual flag-stabilizer integral uses the original unipotent and real parabolic measures. [Genus and parabolic unfolding](https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AbelianVarietyTheory/Proofs/FlagMeasures/IsotropicFlagUnfoldingBound.lean#L213-L283) · [General linear rank recurrence](https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AbelianVarietyTheory/Proofs/FlagMeasures/GenLinTamagawaVolume.lean#L11-L30) · [Product in the flag gauge](https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AbelianVarietyTheory/Proofs/FlagMeasures/ProdFiveFactorsHermitianVolume.lean#L80-L127)

Here is a uniform bound for $R_E$. Set $Y=r^f$ and write $x_v$ for arbitrary real numbers with $\sum_v x_v=0$. Choose an integral ideal $A$ in the inverse of a prescribed ideal class of $E$. The product of complex discs $|z_v|^2\le e^{x_v}(Y N_E A)^{1/f}$ has volume $\pi^f Y N_E A$, strictly larger than $2^{2f}\operatorname{covol}(A)=2^fY N_E A$. A nonzero point $u$ of $A$ therefore gives the integral ideal $I=(u)A^{-1}$ of norm at most $Y$. With $I$ fixed all choices of $u$ differ by units. In coordinates $x_1,\ldots,x_{f-1}$ the possible $x$ for a fixed $u$ form a simplex of volume $\log(Y/N_E I)^{f-1}/(f-1)!$, since each $x_v$ has a fixed lower bound and the last coordinate is minus their sum. The translates cover a fundamental region of volume $\operatorname{Reg}_E$ for the lattice of the $\log|\epsilon_v|^2$. For $f=1$ use zero-dimensional volume one. Summing over ideal classes gives, for $s>1$, $h_E\operatorname{Reg}_E\le Y^s\zeta_E(s)$ by $z^{f-1}/(f-1)!\le e^{sz}$ for $z\ge0$. The class-number formula and $\zeta_E(s)\le(1+1/(s-1))^{2f}$ now bound $R_E$ by $[2\pi e(1+\log r)^2]^f$ on taking $s=1+1/\log r$. Minkowski's discriminant bound gives $r\ge3/2$ for a CM field, so $\log R_E/f\le C+2\log^+\!\log r$ for an absolute $C$. [Residue bound in the original normalization](https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AbelianVarietyTheory/Proofs/FlagMeasures/DedekindZetaResidueLeSixteenLogRootDiscrPow.lean#L48-L75) · [Flag factors and regulator domain](https://github.com/rh-lean-roadmap/rh-lean-roadmap/blob/0be265ccb325908c67f872361d564c66b99e96f7/docs/src/book/main.tex#L58939-L58964)

For large $n$, the log of the compact ratio divided by $J$ is at most $-n\log n+O(n+\sqrt n\log n)$. Indeed each of the $J$ factors from $S_p/S_{p-J}$ has $u-1\ge n-2\sqrt n$, so $\log((u-1)!)\ge(u-1)(\log(u-1)-1)$ gives this estimate. Each factor from $S_q/S_{q-J}$ has a bounded maximum by the consecutive ratio $\pi/u$. Deleting the denominators $S_{j_i}$ costs at most $O(\sqrt n\log n)$ per unit of $J$, since $j_i\le\sqrt n$. The first power of $r/2$ contributes at most $O(n)$ after division by $fJ$, and the power of two is at most one. Because $a\le J$ and $\log\log r\le n$, the residue costs $O(n)$ on that scale. The remaining zeta and inverse $L$ factors cost $O(1)$ by $\zeta_E(l)\le\zeta(l)^{2f}$, $L_F(M,\eta^M)^{-1}\le\zeta(M)^f$ and $M\ge3$. All constants in these estimates are absolute. Thus the flag coefficient is at most $e^{-JH/2}$ above an absolute rank threshold. For the volume alone keep just the factors $t_i^{2fj_i(n-2J)}$, bounding all other scales by one. Because $n-2J\ge1$, the remaining integral over the ordered sizes is at most the product over $i$ of $\int_0^1 2fj_i t_i^{2fj_i-1}\,dt_i=1$. Every point of least size below $1/2$ has one such type. There are $2^{J-1}$ compositions of $J$. The sum of their probabilities is at most $e^{-H/2}/(1-2e^{-H/2})\le e^{-H/3}$ for large $n$. This supplies the deep volume required in FBE52 and the coefficient required in FBE51 from the stated measured unfolding. [Integration and sum over flag types](https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AbelianVarietyTheory/Proofs/FlagMeasures/NonzeroFlagProbabilityBoundOfVolumeRatioInductio.lean#L65-L147) · [Measure on the arithmetic genus](https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AbelianVarietyTheory/Proofs/FlagMeasures/IsotropicFlagProbabilityBoundOfVolumeRatio.lean#L64-L103)

<!--
% END FBE55
-->

## A short unipotent orbit through a deep point

<!--
% BEGIN FBE56
-->

<span id="claim:FBE56"></span>Let $\tau<X^{-11q}$ be the least lattice size at $x$, with $q\ge1$. The canonical Harder–Narasimhan filtration of the self-dual lattice supplies its strictly increasing small sizes starting with $\tau$. These pieces are isotropic because the integral pairing of a piece of size below one with itself must vanish. A nonzero image in the dual would have to map a quotient of size below one to a sublattice of reciprocal size above one. Append $1/2$ to the list. The number of successive ratios is at most the total isotropic rank $q$. Their product is $2\tau$. Thus one consecutive pair $t<t'$ satisfies $t/t'\le s_0=(2\tau)^{1/q}$. We have $t^2\le s_0/4$ since $t'\le1/2$ and $s_0<1$. Let $R$ be the saturated piece ending at $t$, of rank $j\le q$. Its largest quotient size is at most $t$ and every nonzero sublattice above it in the quotient has size at least $t'$. This also bounds sublattices of $R^\perp/R$. Its opposite quotient $\Lambda/R^\perp$ has least size at least $1/t$ by self-duality. [The isotropic step chosen at the actual point](https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AbelianVarietyTheory/Proofs/FlagMeasures/UnipotentOrbitCover.lean#L47-L139)

Consider the integral Hom lattice taking a source $A$ of least size $\ge l$ to a target $B'$ of largest quotient size $\le h$, with ranks $a,b'$. For the trace of a composition its integral trace-dual maps $B'$ into $\mathfrak d_E^{-1}A$. This follows in local projective bases by pairing with each matrix unit and then intersecting the local conditions. A nonzero reverse map has image of some rank $m>0$. On saturating this image and quotienting by the kernel, multiplicativity of covolumes gives a lower bound $l/(rh)$ for the geometric mean operator norm, since twisting the target by $\mathfrak d_E^{-1}$ multiplies every normalized sublattice size by $|d_E|^{-1/(2f)}=r^{-1}$. Its global Hilbert–Schmidt norm is consequently at least $\sqrt f\,l/(rh)$ by the quadratic–geometric mean inequality. In the embedding space with ordinary real Euclidean inner product the trace is twice that inner product after the isometric transpose and complex conjugation. The Euclidean dual minimum is at least $2\sqrt f\,l/(rh)$. By the Euclidean transference inequality $\mu(L)\lambda_1(L^*)\le\dim_{\mathbf R}(L)/2$, every family of maps is within $ab'\sqrt f\,rh/(2l)$ of an integral one. The real dimension here is $2fab'$. For zero-dimensional Hom spaces the distance is zero. [Banaszczyk, Theorem 2.2](https://doi.org/10.1007/BF01445125) · [Trace-dual coordinates and covering radius](https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AbelianVarietyTheory/Proofs/FlagMeasures/LatticePairVolumeBounds.lean#L138-L191)

In the stabilizer of $R$ the first unipotent layer is $\operatorname{Hom}(R^\perp/R,R)$ of shape $j$ by $n-2j$. An integral block lifts to an integral skew endomorphism. To see this, split the saturated summands of the lattice over the Dedekind ring (their quotients are projective), extend the map from $R^\perp$ to the full lattice with image in $R$, and subtract its Hermitian adjoint. The adjoint is integral by self-duality and vanishes on $R^\perp$, so the required first block is unchanged. In orthogonal complex coordinates the horizontal lift and its opposite adjoint have combined norm $\sqrt2$ times the norm of the block. The unconstrained central component of this lift can be left to the next reduction. The radius modulo the centre is therefore at most $n^2\sqrt f\,r s_0/(8\sqrt2)$, since $j(n-2j)\le n^2/8$. For the centre first approximate half the required map from $\Lambda/R^\perp$ to $R$ and then subtract the adjoint. The error at most doubles. Its radius is at most $j^2\sqrt f\,r t^2\le n^2\sqrt f\,r s_0/16$ using $j\le n/2$. This argument works at residue characteristic two because skew-symmetrization requires no division in the integral lattice. [Integral lift of the first block](https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AbelianVarietyTheory/Proofs/FlagMeasures/ExistsStabilizerNilradicalIntegralLiftOfOrthogon.lean#L139-L173) · [The norm modulo the centre](https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AbelianVarietyTheory/Proofs/FlagMeasures/NilradicalFirstLayerCoveringRadiusLe.lean#L107-L185) · [Central lattice](https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AbelianVarietyTheory/Proofs/FlagMeasures/NilradicalCenterIntegralCoveringRadius.lean#L201-L309)

The nilpotent is three-block strictly upper triangular, so $A^3=0$ and all commutators are central. Reduce the logarithm of a real element first by $2g$ times an integral lift. The exponential of that multiple preserves the lattice and is the identity modulo $g$ because its quadratic term is $2g^2A^2$. Include the central part and the half-commutator from multiplication in the central remainder. Reduce this remainder by $g$ times an integral central map, whose square is zero. For an adelic element the same reduction at the finite places uses density of rational points in the finite adeles of each additive layer. First prescribe the first block up to the open congruence, lift it rationally, then prescribe the centre. Chinese remaindering in the corresponding fractional lattices provides both approximations with integral entries away from finitely many places. Thus every point of the adelic orbit, modulo rational translation and the finite open level, has a representative on a path $x\exp A\exp Z$ wholly in that orbit. Its two Hilbert–Schmidt lengths sum to at most
$$
 n^2\sqrt f\,grs_0\left(\frac{1}{4\sqrt2}+\frac{1}{16}\right)
 \le \rho=\frac14 n^2\sqrt f\,gr(2\tau)^{1/q}.
$$
The partial paths also belong to the orbit since both exponents lie in its conjugated nilpotent algebra. [Reduction and control of each partial path](https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AbelianVarietyTheory/Proofs/FlagMeasures/SmallFundamentalSetRealUnipotent.lean#L135-L218) · [Passage to the adelic orbit](https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AbelianVarietyTheory/Proofs/FlagMeasures/UnipotentOrbitCover.lean#L93-L141)

<!--
% END FBE56
-->

## The evaluation estimate along the short orbit

<!--
% BEGIN FBE57
-->

<span id="claim:FBE57"></span>On the lowest type and its derivatives let $V_j$ be the span through order $j$. Put $B_j=\sqrt n\,b^2+\tfrac32 n^{3/2}+3j$, $k=8qN$, and $B=B_{k+N}$. In the source's Hilbert–Schmidt Lie basis the single-place Casimir identity for the sum of squared derivative norms is $2\Omega_K-\Omega_G$. FBE60 and FBE62 identify the lowest type and compute the full central character in the cyclic-word convention. A compact highest weight occurring through order $j$ has $\|\mu+\rho_K\|\le\|\lambda\|+\|\rho_N\|+\sqrt2 j$ because each differentiation adds a weight of the adjoint representation. With $u_0=\|\rho_N\|+\sqrt2 j$, the Casimir bound is $2(\|\lambda\|+u_0)^2-\|\lambda\|^2+n^3/12\le(\|\lambda\|+2u_0+0.3n^{3/2})^2$. The inequalities $\|\lambda\|\le\sqrt n\,b^2$ and $\|\rho_N\|\le n^{3/2}/\sqrt3$ give the bound $B_j$ on an individual unit derivative. For a direction across the $f$ places, Cauchy–Schwarz gives $\|d\sigma(Z)u\|\le\sqrt f B_j\|Z\|_{\rm HS}\|u\|$ on $V_j$. [Infinitesimal character on the original data](https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AbelianVarietyTheory/Proofs/FlagMeasures/DiscreteSeriesStepBoundOfCountingHypotheses.lean#L17-L30) · [Casimir and derivative orders](https://github.com/rh-lean-roadmap/rh-lean-roadmap/blob/0be265ccb325908c67f872361d564c66b99e96f7/docs/src/book/main.tex#L58966-L58975)

Take $D$ isometric intertwiners with continuous differentiated representatives $F_i$ on these spaces. Put $F=(F_i)_i$. We prove the estimate from integration over an ordered exponential cube. Let $s=1/B$ and use one factor for each of the $N$ orthonormal real Lie coordinates. In one variable the fundamental theorem and Cauchy–Schwarz give $|v(0)|^2\le(2/s)\int_0^s |v(t)|^2\,dt+2s\int_0^s|v'(t)|^2\,dt$. A direct way to iterate despite noncommuting coordinates is to start with the full-cube $L^2$ bound for every vector in $V_{k+N}$ and remove the **rightmost** factor. At a point of the prefix cube the derivative along this last factor replaces the vector by its fixed Lie derivative, of norm at most $B$ times the original norm. Both functions are covered by the previous integral bound. The resulting bound on the shorter cube is valid one derivative order lower. Repeating gives a factor $(2/s+2sB^2)^N=(4B)^N\le(6B)^N$. This procedure never interchanges two Lie derivatives. [Removal of the last one-parameter group](https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AbelianVarietyTheory/Proofs/FlagMeasures/SobolevIteratedOneParameterSubgroups.lean#L104-L181)

For the full-cube integral, at one place a differential column in translated coordinates is its basis vector conjugated by the later exponentials. Its change in Hilbert–Schmidt norm is at most $e^{2n^2s}-1$, so the operator-norm perturbation of the $n^2$ columns is at most $n(e^{2n^2s}-1)$. The parameter $b^2\ge n^{19}$ on the count range yields $12n^3s,8n^5s\le1$. In ordinary matrix coordinates even the derivative of the product of exponentials differs from the inclusion of the coordinate subspace by at most $n(e^{3n^2s}-1)\le1/2$. Integrating that difference on a segment proves injectivity. In translated coordinates the determinant loss is at most $\exp(2n^3(e^{2n^2s}-1))\le e$. Products of two cube points, one inverted, have operator norm at most $e^{2n^2s}\le2$. Thickening by $K(g)$ costs $1/k_R$. The separation argument of FBE53 bounds the number of overlapping translates by $(1+4\sqrt n/\tau_1(y)^2)^{2N}$. More explicitly, if any chart translate passes through the same quotient point as a chosen one, the relative rational element preserves the translated lattice at the finite places and its real part lies in the product of the chart and its inverse. Packing those relative elements gives this bound. Chart integration for each component therefore costs at most $e^f P_0(1+4\sqrt n/\tau_1(y)^2)^{2N}\|u\|^2/k_R$ by the isometry. Summing squares over the $D$ components and using the cube estimate gives
$$
 \|F(u,y)\|^2\le (6B)^Ne^f
    (1+4\sqrt n/\tau_1(y)^2)^{2N}\frac{D P_0}{k_R}\|u\|^2
 \qquad (u\in V_k).
$$
[Coordinate density at all real places](https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AbelianVarietyTheory/Proofs/FlagMeasures/LintegralProductExpChartAllRealPlacesLe.lean#L124-L274) · [Counting quotient overlaps in the integral](https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AbelianVarietyTheory/Proofs/FlagMeasures/MeasurePreservingReindex.lean#L180-L216) · [Vector-valued evaluation estimate](https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AbelianVarietyTheory/Proofs/FlagMeasures/MeasurePreservingReindex.lean#L239-L285)

Assume now that the intertwiners have cuspidal image. Along the paths of FBE56 every singular value of the product and its inverse is at most $e^\rho$. Applying this to exterior powers and then taking normalized roots shows that $\tau_1(y)\ge\tau e^{-\rho}\ge\tau/2$ when $\rho\le\log2$. Thus $1+4\sqrt n/\tau_1(y)^2\le17\sqrt n/\tau^2$. Suppose that on all the paths the evaluation bound at order $j+1$ is $M\|u'\|$. For $u\in V_j$, integrating its right derivatives along a path of length at most $\rho$ bounds the change of $F(u,\cdot)$ from $x$ by $\rho\sqrt f B_j M\|u\|$. Its constant term on the rational unipotent quotient is zero. This quotient is compact and has invariant probability measure. Since every orbit value has a representative on a short path, averaging gives the same bound at $x$. The triangle inequality doubles it on the paths, including their prefixes. Apply this implication $k$ times to the cube estimate and square for the lowest unit tensor $w$. The result is
$$
 \|F(w,x)\|^2\le \frac{D P_0}{k_R}\,
 (2\rho\sqrt f B)^{2k}(6B)^Ne^f(17\sqrt n/\tau^2)^{2N}.
$$
The order $k+N$ used to choose $B$ accounts for both the $k$ cusp derivatives and the $N$ cube directions. [The iteration on all partial paths](https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AbelianVarietyTheory/Proofs/FlagMeasures/DeepPointBoundCuspidalIsometricIntertwinerFamily.lean#L68-L114) · [Specialization to the counted tensor](https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AbelianVarietyTheory/Proofs/FlagMeasures/DeepPointBoundCuspidalIsometricIntertwinerFamily.lean#L116-L183)

<!--
% END FBE57
-->

## Why the counted vectors have zero constant term

<!--
% BEGIN FBE58
-->

<span id="claim:FBE58"></span>Let $T$ be one isometric intertwiner in the range of the finite Hecke projector, $w$ the unit lowest-type tensor, and $\phi$ its normalized real matrix coefficient times the finite idempotent. The integral operator with kernel $\phi$ acts as the identity on $Tw$ by the finite projection and formal-degree orthogonality. The equality first holds in $L^2$. To get representatives on $V_j$, the compact-type projection expresses the lowest vectors as compact coefficient averages of translates of $w$. More explicitly the translates inside the irreducible lowest type span it, and compact Schur orthogonality realizes every matrix unit there as a compact average. Convolve the translates with a smooth approximate identity on the real group and project back to the type. The resulting endomorphism approaches the identity on that finite-dimensional type, hence is invertible for a small enough support. This represents each original lowest vector by a compactly supported smooth group average of $w$. In this argument the type projection on the given representation has image the stated lowest copy, by its multiplicity-one property. Lie derivatives transfer to derivatives of the averaging density. Thickening by the normalized finite level indicator and applying $T$ now gives continuous representatives $F(u)$, with right derivatives $F(d\sigma(Z)u)$, on all $V_j$. On compact neighbourhoods the periodized compact kernels have bounded overlap, as in FBE53. Thus convolution of an $L^2$ vector by any of the smooth compact kernels and its derivatives is pointwise defined and continuous by Cauchy–Schwarz. The cube part of FBE57 with one vector gives $|F(w,y)|\le C\tau_1(y)^{-2N}$ with $C$ depending only on these fixed data. [Representatives and their derivatives](https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AbelianVarietyTheory/Proofs/FlagMeasures/ExistsContinuousRowRepresentativesLowestKType.lean#L87-L137) · [Growth of lowest-type evaluations](https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AbelianVarietyTheory/Proofs/FlagMeasures/ExistsContinuousRepresentativeBoundedEvaluation.lean#L16-L42)

For a rational proper isotropic parabolic write $U$ for its unipotent radical and $[U]=U(F)\backslash U(\mathbf A)$. This quotient is compact by successive central quotients by additive vector groups. For fixed $x$, $\tau_1(mx)$ is bounded below on representatives for $[U]$ in a compact set because on finite compact translates only finitely many lattices occur, and real norms are uniformly comparable there. On the support of the finite coefficient a right translation by $g$ preserves the finite lattice and changes the reciprocal lower bound by at most $\exp(\sum_v d_v(g_v)/f)$, by the exterior powers of its inverse in the real frames. Multiplying the resulting growth by the bound of FBE53 for $\phi$ leaves an integrable majorant, uniformly in $m$. Indeed for large $d_v$ the decay coefficient is $h/(8\sqrt{2q})$ per unit of $d_v$. The growth of the vector costs $2n^2$ per unit, and the real Haar integral on unit Cartan shells costs at most $C_n e^{C n^2 d_v}$ by the product of the restricted-root hyperbolic sines (there are at most $n^2$ roots counted with multiplicity, of bounded Euclidean length). The large gap in FBE50 dominates both. Bounded $d_v$ and the finite support have finite measure. The same domination on compact sets of $x$ makes the reproducing integral continuous, so its $L^2$ identity holds pointwise by full support of Haar measure. [Domination for a compact unipotent quotient](https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AbelianVarietyTheory/Proofs/FlagMeasures/CuspidalOfConvolutionFixedModerateGrowth.lean#L119-L154)

Now insert the reproducing integral in the constant term at $x$. After the change of variables $z=xg$, Fubini gives the integral of $\phi(x^{-1}z)C_U(z)$ over the full adelic group, where $C_U(z)=\int_{[U]}F(w,mz)\,dm$. The inner average is unchanged by multiplying $z$ on the left by any element of $U(\mathbf A)$. At any one real place the rational isotropic flag gives a proper real parabolic. Disintegrate Haar measure along its embedded radical $U_v$. All other local factors of $\phi$ are constant on this fibre. The translated $K$-finite discrete-series coefficient has integral zero there by Harish-Chandra's cusp-form theorem. The real group $U(p,q)$ has compact centre and lies in the Harish-Chandra class. This proves $C_U(x)=0$ for all $x$. It applies also to translates of $Tw$, and the closed invariant cuspidal subspace contains the representation they generate. This supplies the zero average on the paths in FBE57 for every counted intertwiner. [Harish-Chandra’s theorem in the group case, Theorem 1](https://publications.mfo.de/bitstream/handle/mfo/3035/OWR_2007_49.pdf?isAllowed=y&sequence=1) · [The embedded real radical](https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AbelianVarietyTheory/Proofs/FlagMeasures/RealUnipotentIntegralDiscreteSeriesVanish.lean#L25-L56) · [Unfolding the constant term](https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AbelianVarietyTheory/Proofs/FlagMeasures/CuspidalOfConvolutionFixedModerateGrowth.lean#L157-L194) · [The counted Hecke image](https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AbelianVarietyTheory/Proofs/FlagMeasures/CountedVectorsAreCuspFormsSingleLowestKType.lean#L85-L113)

<!--
% END FBE58
-->

## The trace of the counting projector on the deep region

<!--
% BEGIN FBE59
-->

<span id="claim:FBE59"></span>We prove the second inequality in FBE52 for the counted projector, using the lowest-type inputs identified in FBE53 and FBE57–58. With $U_0=(2\rho\sqrt f B)^{2k}(6B)^N e^f(17\sqrt n/\tau^2)^{2N}$, put $Y=X^q$. On $0<\tau\le X^{-11q}$, we have $X\ge16$, $(2\tau)^{1/q}\le 2X^{-11}$ and $n^2\sqrt f\,gr\le X^2$. These inequalities give $\rho\le1/2<\log2$, as required in FBE57. From $q\le\sqrt n$, $b\ge2$, $f,g,r\ge1$ one has $B=\sqrt n b^2+\tfrac32 n^{3/2}+3(8q+1)n^2f\le30X^3$ term by term. Hence $n^2fgrB/2\le15 X^5\le X^6$ and $Bng^2X\le 30X^7\le Y^{10}$. Taking an $N$th root and using $k=8qN$, $f/N\le1$, we obtain
$$
 \begin{aligned}
 (U_0g^{2N}X^N)^{1/N}
 &\le 2^{16}\,6\cdot289e\,Y^{96}\tau^{12}Bng^2X\\
 &\le 2^{16}\,6\cdot289e\,Y^{-26}\le e^{-1}.
 \end{aligned}
$$
The positive power $\tau^{12}$ is the $16$ powers gained from the short orbit less the $4$ lost in the cube estimate per dimension. FBE54 gives $P_0V\le X^Ng^{2N}k_R$, so FBE57–58 bound the summed squared evaluations of an orthonormal family of $D$ counted intertwiners on the deep region by $e^{-N}D/V$. [Scalar exponent inequality](https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AbelianVarietyTheory/Proofs/FlagMeasures/DeepRegionExponents.lean#L7-L53) · [Rank and level constants](https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AbelianVarietyTheory/Proofs/FlagMeasures/DeepRegionExponents.lean#L54-L122) · [Multiplication by the quotient volume](https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AbelianVarietyTheory/Proofs/FlagMeasures/DeepRegionKernelDiagonalBound.lean#L77-L142)

To see that the projector has a finite trace, apply this to an **arbitrary finite** orthonormal family. For such intertwining operators Schur's lemma gives $T_i^*T_j=\delta_{ij}I$, so every combination $\sum_i c_iT_i$ with $\sum_i|c_i|^2=1$ is again isometric with the same Hecke and level conditions. On the moderate region the single-vector cube estimate in FBE57 is at most $C_1^2$, uniformly in that combination and point, since $\tau_1\ge X^{-11q}$. Evaluating the combination at $w$ and taking the supremum over the complex unit sphere gives $\sum_i|F_i(w,x)|^2\le C_1^2$. This uniformity avoids any factor of $D$ on the moderate region. Each $F_i(w)$ has squared integral one. Integrating on both regions gives $(1-e^{-N})D\le C_1^2 V$. Hence there is a finite orthonormal basis of the full multiplicity space. The finite coefficient projector acts on the $w$ line in each copy, so its diagonal is the sum over this basis. The finite-rank kernel is continuous by FBE58. Its orbital expansion also converges locally uniformly. On a compact set of $(x,y)$ the possible bounded changes of the two real radii and finite cosets change the packing prefactor by a bounded constant. The shell estimate in FBE50 then dominates the tail there. Unfolding on compactly supported tests identifies the two kernels as distributions and hence, by continuity and full support, pointwise. Integrating the pointwise deep bound for the full basis gives $\int_{\tau_1<X^{-11q}}K(x,x)\,dx\le e^{-N}D$. Together with FBE55 this supplies both integrals used in FBE52, on the stated local representation and measured parabolic inputs. [Passage to the diagonal of the counting operator](https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AbelianVarietyTheory/Proofs/FlagMeasures/DeepPointKernelBoundOfPointwiseBound.lean#L14-L47) · [Equality of the continuous kernels](https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AbelianVarietyTheory/Proofs/FlagMeasures/IntegrablePh.lean#L166-L224) · [Cuspidality, finiteness and trace](https://github.com/rh-lean-roadmap/rh-lean-roadmap/blob/0be265ccb325908c67f872361d564c66b99e96f7/docs/src/book/main.tex#L59017-L59048)

<!--
% END FBE59
-->

## Recovering the discrete series from the prescribed compact type

<!--
% BEGIN FBE60
-->

<span id="claim:FBE60"></span>Let $J=\operatorname{diag}(\epsilon_1,\ldots,\epsilon_n)$ for signs $\epsilon_i=\pm1$, $G=U(J)$, and $K=G\cap U(n)$. At a real place of the counting problem the parameter satisfies $\lambda_1>\cdots>\lambda_n$ and $\lambda_i\in(n-1)/2+\mathbf Z$. The data specify a nonzero irreducible strongly continuous unitary representation $\sigma$ with square-integrable coefficients. They prescribe a compact type of highest weight $\Lambda=\lambda+\rho_n-\rho_c$ that minimizes $\|\mu+2\rho_c\|^2$ among the compact types occurring. Here the roots are $e_i-e_j$ for $i<j$, with compact roots given by equal signs. The two half-sums are $\rho_c,\rho_n$, and $\rho_i=(n+1-2i)/2$ for $\rho=\rho_c+\rho_n$. We show from these hypotheses that $\sigma$ is the discrete series of parameter $\lambda$, and that its prescribed isotypic space $S$ is a single copy. [Parameter, weight and gap](https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Formalism/FormalDegreeBessel/StatementDS.lean#L11-L17) · [Unitarity and square integrability](https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Formalism/SharpRestriction/CuspSpanNormBounds/RelevantZeroGramTerms.lean#L19-L35) · [Norm minimum and the prescribed subspace](https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Formalism/SharpRestriction/CuspSpanNormBounds/RelevantZeroGramTerms.lean#L61-L90) · [The data at every place of the count](https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AbelianVarietyTheory/Definitions/SemilocalFrames/LayerProd.lean#L80-L88)

Put $\nu=\lambda-\rho$. Its entries are integers and $\nu_i-\nu_{i+1}=\lambda_i-\lambda_{i+1}-1\ge0$. The upper triangular Borel $\mathfrak b$ is stable under the Cartan involution and has compact diagonal Levi $T$. The character $\nu$ of $T$ is unitary and pairs nonnegatively with all positive roots. Vogan–Zuckerman's Theorems 5.3 and 6.16 give $A_{\mathfrak b}(\nu)$ with infinitesimal character $\nu+\rho=\lambda$. Since the split part of $T$ is trivial the real parabolic in their Langlands parameter is the whole group, giving the discrete series of this parameter. Its bottom compact type has weight $\nu+2\rho_n=\Lambda$. This weight is compact dominant: for consecutive indices $i<j$ of the same sign, $(\rho_n)_i-(\rho_n)_j$ counts the opposite-sign indices between them. The bottom type has multiplicity one by Sun, §6.3. The semisimple classification applies to $SU(p,q)$. Passing to $U(p,q)=Z(U(p,q))SU(p,q)$ fixes the scalar-circle exponent $\sum_i\Lambda_i=\sum_i\nu_i$, an integer. On the finite intersection the two characters agree because they are restrictions of the bottom compact type. This gives the representation with the specified action of the whole center. [Vogan–Zuckerman, (5.1), Theorems 5.3 and 6.16](https://numdam.org/item/CM_1984__53_1_51_0.pdf) · [Sun, §6.3](https://doi.org/10.1112/S0010437X06002508)

To recognize the representation supplied in the problem, use Harish-Chandra's exhaustion of the square-integrable irreducibles. Write $\eta$ for its parameter in the chamber dominant within each sign, allowing a different order between opposite signs. Write $\rho(\eta)$ for the half-sum in its full chamber. The preceding construction in that chamber gives $\Lambda_\eta=\eta+\rho(\eta)-2\rho_c$. By Theorem 5.3(c), every occurring compact highest weight has the form $\Lambda_\eta+\beta$ with $\beta$ a nonnegative sum of positive noncompact roots. For $\beta\ne0$ the difference of squared norms from the minimum is $2\langle\eta+\rho(\eta),\beta\rangle+\|\beta\|^2>0$. Hence the unique minimizing weight is $\Lambda_\eta$. The prescribed minimum gives $\Lambda_\eta=\Lambda$. The entries of $\eta+\rho(\eta)$ have exactly the order of the entries of $\eta$, because in descending order the coordinates of $\rho(\eta)$ are $(n-1)/2,(n-3)/2,\ldots,(1-n)/2$. Now $\eta+\rho(\eta)=\Lambda+2\rho_c=\lambda+\rho$ determines this order including opposite signs. Subtracting the half-sum in that order gives $\eta=\lambda$. A unitary intertwiner consequently identifies the entire subspace defined as the sum of all copies with the single bottom type of $A_{\mathfrak b}(\nu)$. For a definite signature this is the compact highest-weight classification and $S$ is the whole representation. [Harish-Chandra, discrete series II](https://doi.org/10.1007/BF02392813) · [Vogan–Zuckerman, Theorem 5.3](https://numdam.org/item/CM_1984__53_1_51_0.pdf) · [Original classification and strict minimum](https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AbelianVarietyTheory/Statements/CuspFrameWeights/EigenfunctionFiniteCoefficients.lean#L17-L30)

<!--
% END FBE60
-->

## The coefficient on the original leading principal minors

<!--
% BEGIN FBE61
-->

<span id="claim:FBE61"></span>Let $S$ be the bottom type of FBE60, let $\tau$ be the action of $K$ on $S$ and put $d=\dim S$. Fix a unit vector $w$ on its highest-weight line. For $z=e^Z$ with $Z=Z^*$ in the noncompact tangent space and $\Delta_i(y)=\det y_{1:i,1:i}$, one has the operator identity
$$
 P_S\sigma(z)|_S =
 d\int_K P_{\tau(k)w}\,
 \prod_{i=1}^{n-1}\Delta_i(k^*zk)^{-(\lambda_i-\lambda_{i+1}+1)}\,dk .
$$
Here $P_a u=a\langle a,u\rangle$ for a unit vector $a$, and $dk$ has mass one. Thus a single formula bounds every pair of vectors in $S$, including the arbitrary unit vector used by the counting operator. [Original operator formula and the vectors in the decay estimate](https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AbelianVarietyTheory/Statements/CuspFrameWeights/EigenfunctionFiniteCoefficients.lean#L50-L62) · [Highest and arbitrary lowest-type vectors](https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Formalism/SharpRestriction/CuspSpanNormBounds/RelevantZeroGramTerms.lean#L78-L90)

Apply Sun's formula (26) with $x=e^{Z/2}$ and compact factor $1$. The group is connected reductive with connected derived group of finite center, and FBE60 identifies both its module and its bottom layer. In Sun's integral over $u\in K$ the compact operator is $\tau(u^{-1})P_w\tau(u)$. The scalar is the character of weight $\nu+2\rho=\lambda+\rho$ evaluated on $\widetilde H_{\mathfrak b}(ux)$. To compute this torus point, write $ux=nav$ in $GL_n(\mathbf C)$ with $n$ upper unipotent, $a$ positive diagonal, and $v\in U(n)$, using upper triangular orthogonalization of the rows starting at the last row. The complex compact conjugation is $y\mapsto(y^*)^{-1}$. Thus Sun's (25) gives $a^2$, and $y=uzu^*=na^2n^*$. For the trailing principal minor $T_{i+1}(y)$ on rows $i+1,\ldots,n$ we obtain $T_{i+1}(y)=\prod_{j>i}a_j^2$. If $l_i=\lambda_i+\rho_i$, multiplication of powers gives
$$
 \prod_{i=1}^n(a_i^2)^{l_i}
   =(\det y)^{l_1}\prod_{i=1}^{n-1}T_{i+1}(y)^{-(l_i-l_{i+1})}.
$$
[Sun, Theorem 6.3 and (25)–(26)](https://doi.org/10.1112/S0010437X06002508) · [Brox’s calculation for the short reconstruction, §3](https://github.com/JoseBrox/GRH_distillation/blob/54fbc036a5de1274239b8c949c7a49b377056034/notes/lsernau-discrete-series-suppliers.md#L107-L182)

The change to the original order of minors uses the group equation. Since $JZJ=-Z$, one has $\operatorname{tr}Z=0$ and $JzJ=z^{-1}$. Every $u\in K$ commutes with $J$, so $\det y=1$ and $y^{-1}=JyJ$. Jacobi's complementary principal-minor identity (or the determinant formula for a Schur complement) gives
$$
 T_{i+1}(y)=\det y\;\det\big((y^{-1})_{1:i,1:i}\big)=\Delta_i(y).
$$
The second equality follows because the two restricted diagonal sign matrices cancel in the determinant. Also $l_i-l_{i+1}=\lambda_i-\lambda_{i+1}+1$. All $l_i$ are integral. The last factor in the source's product over *all* leading minors is a power of $\det y=1$, so it contributes one even for negative $l_n$. Changing variables $u=k^{-1}$ gives the displayed operator and keeps the Haar measure fixed. At $z=1$ the compact integral is $I_S/d$ by Schur orthogonality, which verifies the prefactor. Taking matrix entries and applying the variance estimate in FBE53 proves its stated decay on the admitted representations. [The exact integer exponents and leading minors](https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AbelianVarietyTheory/Definitions/SemilocalFrames/PosPartUnitaryMul.lean#L17-L26) · [The original large-gap specialization](https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AbelianVarietyTheory/Proofs/FlagMeasures/LowestKTypeCompressionFormulaOfStrictLowestKType.lean#L21-L38)

<!--
% END FBE61
-->

## The central character and the derivative norms on the same representation

<!--
% BEGIN FBE62
-->

<span id="claim:FBE62"></span>The infinitesimal character of the representation in FBE60 is the character of the center of $U(\mathfrak{gl}_n)$ on the finite-dimensional highest-weight module of weight $\nu=\lambda-\rho$. We compute its value in precisely the cyclic-word convention used for the lowest-type coefficient. Write $E=(E_{ij})$ for the matrix of elementary generators in the enveloping algebra and $D_s=\operatorname{tr}(E^s)$ for $s\ge1$, with the products in their indicated order. The brackets give, by induction and the product rule,
$$
 [E_{ab},(E^s)_{ij}]=\delta_{bi}(E^s)_{aj}-\delta_{aj}(E^s)_{ib}.
$$
Thus $D_s$ is central. The iterated right derivatives of $g\mapsto\langle y,\sigma(g)u\rangle$ expand into exactly the cyclic products in $D_s$ acting on $u$. Every $u\in S$ is a smooth vector, so this computation is valid for every $y$ in the Hilbert space. Smoothness follows, for example, by averaging a smooth approximate identity applied to vectors in $S$ against the compact type projector. These smooth vectors span $S$, since the resulting endomorphisms of the finite-dimensional isotypic space converge to its identity. [Cyclic derivatives and their specified eigenvalues](https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AbelianVarietyTheory/Definitions/SemilocalFrames/PosPartUnitaryMul.lean#L62-L80) · [Matrix powers and commutators](https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Formalism/RealPlaceAnalysis/StatementB.lean#L9-L35)

For a highest vector $v$ of the finite-dimensional module, write $(E^s)_{ii}v=b_i^{(s)}v$. Such a scalar exists since the highest-weight space is one-dimensional. A strictly upper entry of $E^s$ raises the highest weight and kills $v$. Expand $(E^{s+1})_{ii}=\sum_j E_{ij}(E^s)_{ji}$. The terms $j<i$ vanish on $v$. For $j>i$ commute $E_{ij}$ to the right, where it kills $v$, leaving $b_i^{(s)}-b_j^{(s)}$. This proves
$$
 b_i^{(0)}=1,\qquad
 b_i^{(s+1)}=(\nu_i+n-i)b_i^{(s)}-\sum_{j>i}b_j^{(s)} .
$$
Thus the scalar for $D_s$ is the sum of all entries of $A^s$, where $A$ has diagonal $\lambda_i+(n-1)/2$, entries $-1$ strictly above the diagonal and zeros below. This is exactly the prescribed eigenvalue for every $s$, including the central scalar for $s=1$. In particular $b_i^{(1)}=\nu_i$ and summing the recurrence once more gives $\sum_i(\nu_i^2+2\rho_i\nu_i)=\|\lambda\|^2-n(n^2-1)/12$ for the trace Casimir $D_2$. [Highest-vector recurrence](https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Formalism/RealPlaceAnalysis/StatementB.lean#L38-L52) · [Trace normalization of the quadratic operator](https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AbelianVarietyTheory/Proofs/FlagMeasures/GelfValTwoEqCvalR.lean#L15-L32)

Choose a real Hilbert–Schmidt orthonormal basis, written $\mathcal K$ in the compact directions and $\mathcal P$ in the Hermitian noncompact directions. The trace form has signs minus on $\mathcal K$ and plus on $\mathcal P$. Consequently $\Omega_G=D_2=-\sum_{\mathcal K}X^2+\sum_{\mathcal P}X^2$, while $\Omega_K=-\sum_{\mathcal K}X^2$. The derived operators of this unitary representation are skew-adjoint on smooth vectors in the sense of the inner-product identity. Hence
$$
 \sum_{X\in\mathcal K\cup\mathcal P}\|d\sigma(X)u\|^2
 =\langle u,d\sigma(2\Omega_K-\Omega_G)u\rangle .
$$
On a compact type of highest weight $\mu$ the two unitary blocks give $\|\mu+\rho_c\|^2-\|\rho_c\|^2$ for $\Omega_K$ by the same degree-two calculation on each block, including their centers. This holds throughout the span of successive derivatives, where one decomposes the vector into compact types. Substitution in FBE57 yields its derivative bound on the original representation at each place. Together with FBE61 this supplies the local representation inputs used in FBE53 and FBE57–59. The flag-volume calculation in FBE55 also uses the quotient Haar measures for its arithmetic parabolic. [Insertion at a counted real place](https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AbelianVarietyTheory/Proofs/FlagMeasures/DiscreteSeriesStepBoundOfCountingHypotheses.lean#L17-L31) · [Original lowest-type coefficient with arbitrary first vector](https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AbelianVarietyTheory/Proofs/FlagMeasures/LowestKTypeInfinitesimalCharLargeGap.lean#L170-L182)

<!--
% END FBE62
-->

## The general linear Levi volume in the lattice gauge

<!--
% BEGIN FBE63
-->

<span id="claim:FBE63"></span>For a totally complex number field $E$ of degree $2f$, write $r=|\Delta_E|^{1/(2f)}$ and $R_E=\operatorname{res}_{s=1}\zeta_E(s)$. Let $V_j$ be the sum in the source over the isomorphism classes of rank-$j$ integral lattices in $E^j$, of the covolume of the slab $1\le\prod_{v\mid\infty}|\det g_v|^2<e$ modulo the lattice's rational automorphisms. At infinity the measure is the product of ordinary complex area measures on the matrix entries divided by $|\det g_v|^{2j}$. Then for $j\ge1$
$$
 V_j=R_E(r/2)^{fj^2}\prod_{l=2}^j\zeta_E(l).
$$
In particular the quotient $V_j/V_{j-1}$ for $j\ge2$ is $(r/2)^{f(2j-1)}\zeta_E(j)$. [The lattice classes, stabilizer, determinant and gauge](https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AbelianVarietyTheory/Definitions/SemilocalFrames/DefClassNum.lean#L88-L107) · [The defining logarithmic slab](https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AbelianVarietyTheory/Definitions/SemilocalFrames/IsLatMeasurableConst.lean#L38-L43) · [The rank step required by the source](https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AbelianVarietyTheory/Proofs/FlagMeasures/GlNormOneAdelicQuotientVolumeSiegelStep.lean#L212-L217)

At finite places give each $GL_j(\mathcal O_v)$ mass one. Finite cosets modulo their product classify embedded lattices: intersect the local lattices $g_v\mathcal O_v^j$ with $E^j$ and recover them upon completion. Indeed all lie between two fixed fractional multiples of the standard lattice and the intermediate modules are reconstructed from the primary parts of the finite quotient. The rational $GL_j(E)$-orbits and their stabilizers are precisely those in $V_j$. The source takes an infimum of measures of measurable sets meeting every orbit in the slab. For each stabilizer a Borel fundamental set exists because the group is discrete in the product of the real groups and acts by left translation. For instance take countably many open sets on which the quotient map is injective and use the first such local section over each quotient point. Any measurable cover of the orbits has at least this measure by summing its indicator over the countable group and integrating on the fundamental set. Thus the source covolume agrees with the quotient integral. In an adelic slab the finite determinant of each chosen representative shifts the real log-determinant interval by a constant. Multiplication by a central positive scalar translates it back and preserves measure. Consequently $V_j$ is the measure of a unit-length log-determinant slab on $GL_j(E)\backslash GL_j(\mathbf A_E)$. [Infimum over measurable orbit covers](https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AbelianVarietyTheory/Definitions/SemilocalFrames/DefClassNum.lean#L35-L43) · [The sum over the original lattice classes](https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AbelianVarietyTheory/Definitions/SemilocalFrames/GlVolEqTsumSlabVol.lean#L140-L143)

The section $t\mapsto\operatorname{diag}(t,1,\ldots,1)$ splits the determinant on rational points and on adèles. It disintegrates the slab into the idèle-class slab and $SL_j(E)\backslash SL_j(\mathbf A_E)$. Conjugation by this section has determinant one on $\mathfrak{sl}_j$ (the off-diagonal factors occur in inverse pairs), so every fibre has the same quotient measure. At finite places the conditional Haar gives $SL_j(\mathcal O_v)$ mass one by the same split sequence on integral points. At infinity divide the given matrix density by the idèle density $d^2t/|t|^2$ to obtain the conditional Haar. The underlying invariant rational gauge on $SL_j$ is primitive over $\mathcal O_E$: at the identity its coordinates are the off-diagonal entries and $j-1$ diagonal entries, with the remaining diagonal eliminated by trace zero. Splitting off the determinant has absolute Jacobian one in these coordinates at the identity. Invariance then fixes the measure everywhere. [Kim, §2.3, local matrix and norm gauges](https://doi.org/10.1112/jlms.12830)

For $j\ge2$ put $d=j^2-1$. At a finite place of residue cardinality $Q$, the primitive algebraic gauge gives $SL_j(\mathcal O_v)$ mass $\#SL_j(\mathbf F_Q)/Q^d=\prod_{l=2}^j(1-Q^{-l})$. This follows by reduction on the smooth group, with an additive $d$-dimensional residue ball above each point, and by counting ordered bases and dividing by $Q-1$. For the adelic Tamagawa gauge the global discriminant factor is $|\Delta_E|^{-d/2}$ and each of the $f$ complex places uses twice ordinary area per coordinate. These normalizations give the rational additive line adelic covolume one since its unscaled fundamental parallelepiped has volume $2^{-f}\sqrt{|\Delta_E|}$. Thus the normalized Tamagawa measure is the source's conditional measure times
$$
 |\Delta_E|^{-d/2}2^{fd}\prod_{l=2}^j\zeta_E(l)^{-1}.
$$
The Euler products converge at all these integers. The special linear group is split, semisimple and simply connected, so its Tamagawa number is one. The fibre has volume $(r/2)^{fd}\prod_{l=2}^j\zeta_E(l)$ in the original gauge. For $j=1$ the fibre is a point of volume one. [Weil, *Adèles and algebraic groups*](https://albert.ias.edu/entities/publication/933622d7-3ada-4158-8fb3-4814a6501770) · [Kottwitz, *Tamagawa numbers*](https://annals.math.princeton.edu/1988/127-3/p05)

There are $h_E$ ideal classes on the idèle base. In each complex coordinate use $x_v=\log|t_v|^2$ and the angle $\theta_v$. Then $d^2t_v/|t_v|^2=\frac12 dx_v\,d\theta_v$. The log-unit lattice in the first $f-1$ coordinates has covolume $\operatorname{Reg}_E$ and the remaining coordinate can be replaced by $\sum_v x_v$ with Jacobian one. The angle torus contributes $(2\pi)^f$, with division by $w_E$ for the roots of unity. The slab therefore has measure $h_E\pi^f\operatorname{Reg}_E/w_E=R_E(r/2)^f$ by the analytic class number formula. Multiplying by the fibre mass gives the claim and supplies the general linear factors in FBE55 on every original Levi block. The estimate for how flags of the integral unitary genus are distributed among those blocks uses a separate quotient calculation. [Rank one and the ideal classes](https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AbelianVarietyTheory/Proofs/FlagMeasures/GlNormOneAdelicQuotientVolumeOneEqResidue.lean#L440-L457) · [The resulting factors in the flag bound](https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AbelianVarietyTheory/Definitions/SemilocalFrames/DefClassNum.lean#L22-L33)

<!--
% END FBE63
-->

## Counting the integral flag orbits in the given genus

<!--
% BEGIN FBE64
-->

<span id="claim:FBE64"></span>Fix a type $(j_1,\ldots,j_a)$ in FBE55 and put $s=\sum_i j_i$. In a self-dual Hermitian lattice $L$ in the genus of the original CM host take a saturated totally isotropic flag with last term $U$. Put $A_i=U_i/U_{i-1}$. A flag up to rational isometry of its ambient lattice is determined by the isomorphism classes of the projective $\mathcal O_E$-modules $A_i$ and the isometry class of the residual Hermitian lattice $L_0=U^\perp/U$. The residual class belongs to the genus of the rank $n-2s$ host of signatures $(p-s,q-s)$. This gives an upper bound by a sum over these classes even when some class tuples are never realized in the original genus. [Adapted lattice, pairing and all the flag steps](https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AbelianVarietyTheory/Definitions/SemilocalFrames/IsLatMeasurableConst.lean#L12-L23) · [Saturation in the original lattice](https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AbelianVarietyTheory/Proofs/FlagMeasures/ExistsAdaptedBasisSaturatedIsotropicFlag.lean#L68-L81)

Indeed, the ring $\mathcal O_E$ is Dedekind. Each $A_i$ and $L/U$ is torsion-free and projective, so the flag in $U$ splits with $U=\bigoplus_i A_i$. Define $U^\sharp$ as the conjugate dual, with the natural perfect evaluation pairing with $U$. Restriction of $L\simeq L^\sharp$ onto $U^\sharp$ is surjective since $U$ is a direct summand. Choose a module section of this restriction. Its self-pairing is a Hermitian form $B$ on $U^\sharp$. By $U=(U^\sharp)^\sharp$ this is the matrix-free version of the lower-right block $B$ in a Gram matrix with the other blocks $0,1,1$. There is $c\in\mathcal O_E$ with $c+\bar c=1$. Locally at each finite place the trace of the unramified quadratic or split étale algebra is onto: for an unramified field use the surjective residue-field trace and Nakayama, also in residue characteristic two. Thus the global trace image is an ideal of $\mathcal O_F$ that is the unit ideal at all its primes. Subtract from the section its component in $U$ given by the pairing $cB$. The new self-pairing is $B-cB-(cB)^*=0$ and the evaluation pairing stays perfect. This embeds the integral hyperbolic lattice $U\oplus U^\sharp$ as an orthogonal summand. Its complement is self-dual and maps isometrically onto $U^\perp/U$. The resulting isometry
$$
 (L,U_\bullet)\simeq
 \left(\bigoplus_i (A_i\oplus A_i^\sharp)\ \perp\ L_0,\quad
       \bigoplus_{i\le h} A_i\right)_{0\le h\le a}
$$
extends any prescribed isomorphisms on the $A_i$ and any isometry of the residual lattice by the inverse adjoints on $A_i^\sharp$. In particular its rational extension respects every flag subspace. [Integral dual blocks and the orthogonal complement](https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AbelianVarietyTheory/Proofs/FlagMeasures/ExistsAdaptedBasisSaturatedIsotropicFlag.lean#L110-L148) · [Conjugacy for a fixed tuple of classes](https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AbelianVarietyTheory/Proofs/FlagMeasures/FlagsConjugateOfSameAdaptedModels.lean#L176-L203)

At a nonsplit finite place every unimodular Hermitian lattice for an unramified quadratic extension has an orthonormal basis. Reduce the pairing to a nondegenerate finite-field Hermitian form, choose a vector of nonzero norm and lift it. Its norm is a unit and can be scaled to one since the norm is onto on units. The latter follows from the residue-field norm and successive lifting on principal units via the surjective trace. Splitting off this vector proves the assertion by induction. At a split place the two factors are dual lattices and choosing dual bases gives the corresponding result. At infinity removing $s$ hyperbolic planes gives precisely the prescribed signatures. Landherr's local-global theorem therefore gives a rational isometry with the residual host. In these rational coordinates the integral lattices at all finite places match the fixed residual lattice after a local unitary translation. Almost everywhere they already agree, so the translations define an element of the finite adèles. Residual lattice isometry classes are consequently indexed by the rational unitary double cosets modulo the full stabilizer. [Jacobowitz, unramified local Hermitian lattices](https://doi.org/10.2307/2372982) · [Landherr, local-global equivalence of Hermitian forms](https://doi.org/10.1007/BF02940728) · [The specified residual host](https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AbelianVarietyTheory/Proofs/FlagMeasures/ExistsAdaptedBasisSaturatedIsotropicFlag.lean#L23-L42) · [Realizing its integral lattice at the finite places](https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AbelianVarietyTheory/Proofs/FlagMeasures/ExistsFiniteAdelicPointLatticeEqSelfDual.lean#L25-L51)

For the volume estimate, decompose the original adelic quotient by finite cosets modulo the full stabilizer $K_f$. Each real-group quotient has stabilizer $\Gamma_L$ for its lattice $L$ and finite factor $\mu_f(K_f)$. On such a quotient majorize the filtration indicator by the sum of the indicators that an individual rational flag has its sizes in the prescribed measurable set. Saturating a rational flag gives its unique saturated integral flag in $L$. In an orbit of flags the sum runs over $\Gamma_F\backslash\Gamma_L$, with $\Gamma_F$ the stabilizer of a representative flag. Integrating on a fundamental domain and translating its copies gives the integral of the individual indicator over $\Gamma_F\backslash G_\infty$. All summands are nonnegative and the flag set is countable, so Tonelli applies even before the bound shows finiteness. The classification above permits at most one such orbit over each tuple when all original finite cosets are included. Extending the sum of the resulting product bounds to every tuple factors it into the $V_{j_i}$ of FBE63 and the sum for the residual unitary quotient. The same finite-coset disintegration on the residual host bounds this latter sum by its normalized volume. This proves the orbit and multiplicity steps in the unfolding. Its remaining input is the integral for one flag stabilizer in the product of the real parabolic gauges, including the covolume of its arithmetic unipotent radical in the chosen frame. [Decomposition into flag orbits](https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AbelianVarietyTheory/Proofs/FlagMeasures/IsotropicFlagUnfoldingBound.lean#L213-L241) · [The measured sum over integral blocks and residual classes](https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AbelianVarietyTheory/Proofs/FlagMeasures/IsotropicFlagUnfoldingBound.lean#L250-L279)

<!--
% END FBE64
-->
