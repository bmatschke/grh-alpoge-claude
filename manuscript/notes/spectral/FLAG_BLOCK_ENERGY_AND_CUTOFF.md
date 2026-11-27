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
