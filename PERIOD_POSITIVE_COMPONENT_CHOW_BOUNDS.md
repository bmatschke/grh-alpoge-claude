# Period entry 7 on positive-dimensional components

## A sufficient condition from a subsystem of cusp forms

Fix the quotient weight $u_1$ on a good cover. Let $V_Z$ be the space of quotient-weight cusp forms on a component $Z$ over the coefficient field $K$, with its integral lattice and Petersson metrics. Its complete series has projective image $X_Z\subset\mathbf P(V_Z^*)$ of dimension $d=f\binom r2$ and degree $\Delta_Z$. The last nonterminal layer has $q_{\rm sig}=1$. In this note a short section must be globally integral and satisfy the claimed norm bound at every embedding.

Take integral sections of norm at most $e^{\lambda_Z}$ spanning a subspace $W_Z$. Complete a basis of $W_Z$ to a $K$-basis of $V_Z$ with members of the roadmap's integral generating frame, of norm at most $e^{J_Z}$, where $0\le\lambda_Z\le J_Z$. Let $X'_Z$ be the image closure of the projection $\pi_W:X_Z\dashrightarrow\mathbf P(W_Z^*)$. If $\dim X'_Z=d$, set
$$
  \delta_Z=[K(X_Z):K(X'_Z)]\deg X'_Z .
$$
Otherwise put $\delta_Z=0$. Write $N_Z=\dim_KV_Z$, $e=(d+1)\Delta_Z$, and $H_j=\sum_{i=1}^j1/i$, with $H_0=0$.

**Proposition.** For the Chow form $F_{X_Z}$ put $h'_Z=h_0(F_{X_Z})/e$, using the finite coefficient norms of the full integral frame and the archimedean sphere means in spectral roadmap v36 B8.25p. Then
$$
 h'_Z\ge -B_Z,\qquad
 B_Z=\lambda_Z+(1-\delta_Z/\Delta_Z)(J_Z-\lambda_Z)
                  +\log N_Z+\tfrac12 H_{N_Z-1}.                    \tag{1}
$$
Under the roadmap's determinant and numerical inputs recorded below, the cover slope consequently satisfies
$$
 \mu_Y(u_M)\ge
 -2T_*\,\frac{\sum_Z \mathcal B\Delta_Z B_Z}{\sum_Z\mathcal B\Delta_Z}
 -C E_p,\qquad \mathcal B=\binom{T_*-1}{d},                       \tag{2}
$$
with $C$ uniform in the family. Thus a bound $\sum_Z\Delta_Z T_*B_Z/\sum_Z\Delta_Z=O(E_p)$ suffices on the cover. The subsequent flat untwist, type projection and descent to the original level still use their respective roadmap inputs.

**Proof of the moving-degree estimate.** In the chosen basis, let $w$ be the first group of hyperplane coefficients, and $y$ the rest. The form $F_X(w+t y)$ has a nonzero term of $t$-degree at most $(d+1)(\Delta-\delta)$. Degenerate $X$ by the diagonal action multiplying the last point coordinates by $t$. Its Chow form is $F_X(w+t y)$ for $t\ne0$. The first nonzero $t$-coefficient represents the Chow form of the special fibre cycle by the Chow specialisation law for a flat projective family over a smooth curve. One can see the law by cutting with $d$ generic hyperplanes and taking the norm of the remaining hyperplane on the resulting finite flat scheme. The components contribute their Chow forms raised to their generic lengths.

For a full-dimensional projection let $K_0=K(X')$, $L=K(X)$, and $m=[L:K_0]$. On the chart of a nonzero first-group point coordinate, divide all coordinates by it. Over the generic point of $X'$ the orbit closure on this chart has ring
$$
 A=K_0[t,tz_1,\ldots,tz_s]\subset L[t],
$$
where the $z_i$ are the remaining coordinate ratios. Each $tz_i$ is integral over $K_0[t]$ by scaling a monic polynomial of $z_i$. Thus $A$ is finite and torsion free, hence free over $K_0[t]$. Its rank is $m$ because the $z_i$ generate $L$ over $K_0$. Modulo $t$, the monic equations make each $tz_i$ nilpotent. Hence $A/tA$ is local with residue field $K_0$ and length $m$. The special fibre contains the cycle $m[X']$ in the first coordinate subspace. The remaining effective cycle has degree $\Delta-\delta$ by flatness. The first cycle's Chow form involves only $w$, and the remaining Chow form has total degree $(d+1)(\Delta-\delta)$. Thus the first $t$-coefficient contains a monomial with at most this many $y$ factors, counted with multiplicity. For $\delta=0$ the same bound follows from total degree. This also shows $0\le\delta\le\Delta$.

**Refinement using the base locus.** Suppose $W\ne0$ and its projective base locus $B=X\cap\{w_{\rm point}=0\}$ has geometric dimension $b_0\ge0$. In (1) one may replace $1-\delta/\Delta$ by
$$
             \frac{b_0+1}{d+1}\,(1-\delta/\Delta).                 \tag{1a}
$$
For the flat limit in the proof above, every point in the pure complementary coordinate plane belongs to $B$. Indeed if $f$ is any homogeneous polynomial in the ideal of $X$, the polynomial $f(tw_{\rm point},y_{\rm point})$ vanishes on the family, since it vanishes on the generic scaled orbit. At $t=0$ it implies $f(0,y_{\rm point})=0$. Conversely points of $B$ are fixed under the action. In particular the intersection of the residual cycle's support with the pure complementary plane has dimension at most $b_0$. Choose $d-b_0$ general hyperplanes from $W$. On the complement of that plane the subsystem has no base point, so intersecting residual components with successive general members lowers dimension by one each time or eliminates the component. On the plane the intersection already has dimension at most $b_0$. The whole residual intersection therefore has dimension at most $b_0$, and $b_0+1$ further general unrestricted hyperplanes avoid it. Thus the residual Chow form is nonzero after restricting its first $d-b_0$ blocks to $W$. The pure $m[X']$ factor is still generically nonzero on those blocks. In their product, some monomial has at most $(b_0+1)(\Delta-\delta)$ expensive factors, since only the last $b_0+1$ blocks of the residual form can contribute them. This applies also when $\dim X'<d$ and the entire limit is treated as residual. The empty-base case gives $\delta=\Delta$ separately. In particular isolated common zeros give an additional factor $1/(d+1)$ in the expensive contribution, without a transversality or reducedness assumption.

**Proof of (1).** Let $a\in K^\times$ be the coefficient of such a monomial, $k$ its total exponent in the expensive coordinates. At each finite place, its absolute value is at most the coefficient norm of the full integral frame. Indeed our vectors are integral linear combinations of frame members locally. At each embedding substitute the corresponding linear combination of basis sections in each block, using polyradii $e^{-\lambda}/N$ for the short vectors and $e^{-J}/N$ for the others. Each block then has norm at most one. Cauchy's coefficient estimate and the spherical submean give
$$
 \log|\sigma(a)|\le m_\sigma(F_X)+(e-k)\lambda+kJ
                            +e(\log N+H_{N-1}/2).
$$
The submean inequality follows by moving a unit vector to the first coordinate and applying submean in the orthogonal directions, since the spherical mean of the log modulus of the first coordinate equals $-H_{N-1}/2$. Iterate through the $d+1$ blocks. Sum over the places using the product formula for $a$, and insert $k/e\le1-\delta/\Delta$. Nonfree integral lattices are allowed.

**Proof of (2) directly for the determinant height.** This derivation avoids an additive convention for the Fubini–Study height. The proof of B8.25e immediately before its equation p8c3-det-degree supplies, for $v=r_Z,\ w=\mathcal B\Delta_Z,\ T=T_*,\ \zeta=1-w/v$,
$$
 D_0/v\ge (w/v)\{Th'_Z-d(d+1)c-J_{\rm cut}-T\log\beta/2\}
       -\zeta\{Tc+T\log\beta/2+2P\kappa\}.
$$
Here $D_0$ is the unsquared untwisted degree, $P=P_*$, $q=\kappa/T$, $J_{\rm cut}=dP(q+1)$, and $0\le\zeta\le z\le1/2$. Furthermore $c=\log(n_1\Lambda)+(1+\log n_1)/2\le3P(q+1)$, by the following inputs from that proof:
$$
 \log\beta,\log n_1\le P,\quad \log\Lambda\le P(q+1),\quad TP\le\sqrt b,
 \quad zP\kappa\le b,\quad d^2Pq\le b/7,\quad d^2P\le b/14,\quad J_{\rm cut}\le9b.
$$
For $b\ge1$ these show $d(d+1)c\le2b$, $T\log\beta/2\le b/2$, and the last brace multiplied by $\zeta$ is at most $9b$. Therefore $D_0/v\ge-(w/v)TB_Z-21b$. The flat-twist estimate in the same proof gives $d_Z\ge D_0-v C_p(frL_x)^2$. Sum and apply B8.25e (8.29c), which doubles the unsquared mean. Using $\sum w\le\sum v$, $B_Z\ge0$, and $b+(frL_x)^2=O(E_p)$ gives (2).

**What the arithmetic construction still needs.** One sufficient test is $\delta_Z\ge(1-\rho)\Delta_Z$ on each component and $\sum_Z\Delta_Z T\lambda_Z/\sum_Z\Delta_Z=O(E_p)$. Indeed $N_Z\le n_1$ gives $T(\log N_Z+H_{N_Z-1}/2)=O(TP)=O(\sqrt b)$. For the roadmap coarse frame take $J_Z=\log\Lambda$. Then
$$
 T\rho J_Z\le \rho P\kappa+\rho TP\le b+\sqrt b,
$$
since $z=7(d^2/T+d\rho)\ge\rho$. The Weyl comparison B8.25e gives the explicit degree target $\Delta'_Z=\deg_Z(u_1-3r\eta_H)\ge(1-\rho)\Delta_Z$. Multiplying every member of a lower-weight subsystem by the same generically nonzero factor preserves its projective ratios and moving degree. For a proposed multiplication construction one must verify integrality and cuspidality of the resulting sections, the moving degree of the particular subsystem, and its Petersson norms. The numerical Weyl comparison and large-radius frame alone leave these questions open.

A direct full-degree test only needs $d+1$ integral sections. If their common base locus on $X_Z$ is empty, they define a morphism whose pullback of $\mathcal O(1)$ is the ample $\mathcal O_{X_Z}(1)$. This morphism is finite onto its image by ampleness and properness. The projection formula gives $\delta_Z=\Delta_Z$, so the coarse radius entirely drops out of (1). Merely separating a dense open set does not show this property. On this full-degree route a direct proof bypasses Chow specialisation: restricting the Chow form to that subsystem gives a nonzero polynomial because the displayed tuples have no common zero. Choose a nonzero coefficient and apply the same product-formula argument with $k=0$.

For a concrete norm target, equation p8c3-row-sum of the same roadmap gives $T\|u_1\|_1\le834fmb$, while $E_p=fmbL_x\log\log x$. Thus a per-unit-weight bound $\lambda_Z\le C L_x\log\log x\,\|u_1\|_1+O(P_*)$ would suffice, with a constant independent of the layer, rank and field. The coarse construction charges a polynomial in $frL_x$ per unit weight and does not imply this sharper bound.

**A weaker arithmetic hypothesis for the full-degree test.** Let $s_0,\ldots,s_d$ have no common zero on $X_Z$, possibly after a common finite number-field extension $L/K$. Each $s_i$ can be an arbitrary nonzero rational section of $V_{Z,L}$. Put
$$
 \ell(s)=\sum_{v\in M_L}\frac{[L_v:\mathbf Q_v]}{[L:\mathbf Q]}
                               \log\|s\|_v ,
$$
using the lattice gauge at finite places and the Petersson norm at the embeddings with their usual weights. This is invariant under scaling $s$ by $L^\times$ and under enlarging $L$. In this case the sharper bound is
$$
 h'_Z\ge -\frac{H_{N_Z-1}}2-\frac1{d+1}\sum_{i=0}^d\ell(s_i).       \tag{3}
$$
Indeed $a=F_{X_Z}(s_0,\ldots,s_d)\in L^\times$ by the incidence definition. At finite places its absolute value is bounded by the coefficient norm times $\prod_i\|s_i\|_v^\Delta$. At infinity the submean bound gives $\log|a|_v\le m_v(F)+eH_{N_Z-1}/2+\Delta\sum_i\log\|s_i\|_v$. The product formula proves (3) exactly, including archimedean conjugate weights. Consequently only the **mean absolute adelic height of the $d+1$ projective lines** matters; it can absorb large costs on some sections or embeddings. This means a prospective construction can rescale separately at each line, work over an auxiliary number field and retain finite denominator costs in $\ell(s)$. In (2) use the positive part of the global weighted mean if the right side of (3) leads to some signed $B_Z$. Indeed $-T\sum w_ZB_Z/\sum r_Z\ge-T\max(0,\sum w_Z B_Z/\sum w_Z)$, irrespective of the individual signs. No such tuple with the required uniform mean height has been exhibited here.

**Comparison with the roadmap's positive-dimensional argument.** Roadmap B8.28 uses the averaged arithmetic intersection input B8.26 at $u'=u_1-3r\eta_H$, producing $s_Z$ with component mean at least $-X$. Through the finite carrying-order, archimedean point-norm and section-count comparisons in degrees $8a$, it proves
$$
 \max(0,\Delta'_Z(s_Z+c_s))\le\Delta_Z(h_Z+c_s+c_c),
$$
where $h_Z$ denotes its Fubini–Study Chow height. B8.29 bounds the residual cost of the coarse shift by $(6d+10+T(z+2\rho))c_s$ after averaging, and obtains the slope without constructing short sections at degree one. The existing project repair permits that asymptotic argument on the normalization via fixed-twist invariance. Its finite carrying-order and archimedean point-norm hypotheses and the B8.26 mean must still hold for the actual selected cover. The original lattice/field tie, period normalization and terminal definite calculation do not check those positive-dimensional inputs. After either route gives a cover slope, B8.29 uses the signed flat untwist, horizontal-type injection with its rank loss and trace descent to import it to the core; reference-lattice passage and served indices come afterward. No positive-dimensional layer is thereby unconditionally closed.

A simple curve shows why an adequate Chow lower bound can coexist with costly basepoint-free tuples at degree one. Embed $\mathbf P^1_\mathbf Q$ by all degree $D\ge2$ monomials, with the ordinary coefficient lattice. Give those monomials orthogonal archimedean lengths 1 except for $x^D$, whose length is $e^J$. The sections without $x^D$ form $yH^0(\mathcal O(D-1))$ and have moving degree $D-1$. Inequality (1) therefore gives $h'_Z\ge-J/D-O(\log D)$. But in any basepoint-free pair at least one section is nonzero at $[1:0]$, so its $x^D$-coefficient is nonzero. At every place its norm bounds the modulus of that coefficient, with the extra $e^J$ at infinity. Its absolute line height is at least $J$ by the product formula, even after field extension. The other line has nonnegative height by the same argument with any nonzero coefficient. Thus the mean cost in (3) is at least $J/2$. Taking $J=D$ separates these estimates. The example concerns general Hermitian linear systems; it makes no assertion that the automorphic image exhibits this behaviour.

**Sources.** RH Lean Roadmap, spectral v36, pin 02a95b4c62db610642af5f278ee5d0d6df87b348, B8.25p, B8.25e, B8.29, especially the paragraph preceding p8c3-det-degree and the estimates p8c3-hs-parameters and p8c3-det-costs. For the Chow form and its cycle interpretation see Kapranov, Sturmfels and Zelevinsky, *Chow polytopes and general resultants*, Duke Mathematical Journal 67 (1992), 189–218; Eisenbud and Schreyer, *Resultants and Chow forms via exterior syzygies*, Journal of the American Mathematical Society 16 (2003), 537–579, §1.

[Determinant inequality](https://github.com/rh-lean-roadmap/rh-lean-roadmap/blob/02a95b4c62db610642af5f278ee5d0d6df87b348/docs/src/book/main.tex#L51019-L51048) · [Quotient-weight sum](https://github.com/rh-lean-roadmap/rh-lean-roadmap/blob/02a95b4c62db610642af5f278ee5d0d6df87b348/docs/src/book/main.tex#L51531-L51540) · [Carrying sections on the native cover](https://github.com/rh-lean-roadmap/rh-lean-roadmap/blob/02a95b4c62db610642af5f278ee5d0d6df87b348/docs/src/book/main.tex#L53665-L53722) · [Chow forms and incidence](https://arxiv.org/abs/math/0111040)
