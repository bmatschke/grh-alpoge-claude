# Switching the two global theta determinants at a single rational prime

The native positive-remainder comparison uses two *global* theta modules on one cusp-form space. At each row of its construction the coordinate map and group action are common, and the selected run is constant away from the characteristic $p_*=p_{\rm de}$ and constant above it. This is stronger than having an unrelated local lattice at every twisted place. It gives the following alternative sufficient inequality for entry 7. It requires the geometric lattice, action, local comparison and finite-type identifications specified below. It does not require the positive-excess conclusion of either run.

## A lattice built before choosing the place

Fix a layer, its common number field $K$, its full ambient lattice $B$, the Whittaker character space $W$, the retained idempotent $e$, its target $Z=W\cap\operatorname{im}e$, $D=\dim Z>0$ and $M=B\cap Z$. Put $h=|U|$, $H=\sum_{u\in U}\psi(u)^{-1}\rho(u)$. On either serving domain the initial theta lattice $\Theta_1$ lies in the stable lattice $\Theta\subset B$. The original hypotheses give $H\Theta\subset\Theta\cap W$, $\Theta\subset\sigma_w\Theta_K$, $h(\Theta_K)_W\subset\Theta_0$, and $e\Theta_0\subset e\Theta_J\subset Z$. In particular $eH$ has image precisely $Z$: those inclusions give containment on the span of a full lattice, and on $Z$ the map acts by $h$. The original type realization has $g=|G|$ with $ge(B\cap W)\subset B$: its projector coefficients have denominator $g$ and the level action preserves the full lattice. Any common positive integer clearing this map works in the exact inequality.

For run $a=1,2$, take $D$ global theta sections $y_{ai}\in B$ lying in that run's initial lattice at every place it serves, whose $eHy_{ai}$ are independent. They exist whenever the full-weight integral short-section input of the runs is supplied: its finite set spans the entire ambient space over the small geometric field and its module is the third summand in the defining theta module. Scalar extension under the common coordinates preserves spanning, and extracting $D$ columns after projection preserves independence. Integrality of the selected sections follows from the corresponding integral-theta input. Alternatively clear a common global denominator when rationally spanning integral theta modules have been supplied; any archimedean cost of such a change stays in the inequality.

Write $x_{ai}=geHy_{ai}$, $L_a=\sum_i\mathcal O_K x_{ai}\subset M$. All of these are actual lattices on the same target, regardless of where either run is being applied. At a twisted $w$, let $a(w)=2$ for $w\mid p_*$ and 1 elsewhere. Then
$$
 (h/(\sigma_w g))L_{a(w),w}\subset e\Theta_J.
$$
In fact for $y\in\Theta$, $Hy/\sigma_w\in(\Theta_K)_W$, and projection after multiplication by $h$ gives the inclusion. By the source comparison of indices via $X_3\subset A_{t_w}$, it follows that
$$
 [M:A_{t_w}]_w\le [M:L_{a(w)}]_w+
    D\{v_w(h)-v_w(\sigma_w)-v_w(g)\}+ e_w\xi_{wj}.
\tag{1}
$$
In particular this use does not assert an inclusion $e\Theta_J\subset A_{t_w}$.

## Cancelling the target lattice

Choose any rational basis of $Z$, put $X_a=(x_{ai})_i$ in this basis, and set $\alpha=\det X_2/\det X_1\in K^\times$. The ratio is the same for $eHy$, or for $e(H/h)y$. At every $w$, $[M:L_2]_w-[M:L_1]_w=v_w(\alpha)$. Both original indices $[M:L_a]_w$ are nonnegative. Hence extending the switched sum from twisted places to all finite places yields
$$
 \sum_{w\in {\rm Tw}}\ell_w[M:L_{a(w)}]_w
 \le\sum_w\ell_w[M:L_1]_w+
  {\log p_*\over[K:\mathbf Q]}\operatorname{ord}_{p_*}|N_{K/\mathbf Q}\alpha|.
\tag{2}
$$
The last term is signed. This is the sum across the entire fibre over $p_*$; replacing it by a sum over twisted places alone without keeping the discarded complement would not follow. Formula (2) uses $v_w$ normalized on a local uniformizer, $\ell_w=\log Nw/[K:\mathbf Q]$.

In the squared-norm covolume convention $\operatorname{lcv}(L_1)=\operatorname{lcv}(M)+2\sum_w\ell_w[M:L_1]_w$. Let
$$
 \mathcal A_j=D^{-1}\big\langle\log\det\operatorname{Gram}_{\sigma}
         (e(H/h)y_{1i})\big\rangle_\infty
$$
in the prescribed target metric. Then $\operatorname{lcv}(L_1)/D=\mathcal A_j+2\log(gh)$. With $i_{jw}=[M:A_{t_w}]_w+[M:A_{t_w}]_{\bar w}$, use the common tuple at conjugate places and apply (1) and (2). This gives
$$
 \frac{\operatorname{lcv}(M)+\sum_{w\in{\rm Tw}}\ell_w i_{jw}}D
 \le \mathcal A_j+
  {2\log p_*\over D[K:\mathbf Q]}\operatorname{ord}_{p_*}|N_{K/\mathbf Q}\alpha_j|
 -2\sum_{w\in{\rm Tw}}\ell_w v_w(\sigma_{wj})+\mathcal E_j,
\tag{3}
$$
where
$$
 \mathcal E_j=2\log(g_jh_j)+
 2\sum_{w\in{\rm Tw}}\ell_w\big(v_w(h_j)-v_w(g_j)\big)+
 \frac2D\sum_{w\in{\rm Tw}}\ell_w e_w\xi_{wj}.
$$
The total error has upper bound $2\sum_j\log g_j+4\sum_j\log h_j+ (2/D)\sum_p(\log p)/p^2$. For the two fixed level primes, $h=(g_0g_1)^{fr(r-1)/2}$, and the finite level group is the product of $f$ copies of the local general linear groups at the two primes (a subgroup or quotient has no larger order). Thus the logarithms are $O(fr^2(\log g_0+\log g_1))$ per layer, polynomial in $x$ on the linked family and $o(b)$ after summation. In any realization using a larger clearing denominator one should retain its exact contribution in (3).

The signed bound for entry 7 now follows if
$$
 \sum_j\left\{\mathcal A_j+
 {2\log p_*\over D[K:\mathbf Q]}\operatorname{ord}_{p_*}|N_{K/\mathbf Q}\alpha_j|
 -2\sum_{w\in{\rm Tw}}\ell_w v_w(\sigma_{wj})
 +D^{-1}\sum_{w\in{\rm Tw}}\ell_w q_{jw}\right\}
 \le \sum_{j,\rho}\beta_jw_{j\rho}\log\Omega+2F_*+
 O\!\left(mL(B_0+N_c)\right).
\tag{4}
$$
The embedding-defect version retains $-E_{Q,0}/D$ on the left. This replaces the absolute target covolume and the many integral image indices together. The only comparison between the two global bases is one signed ordinary prime valuation per layer. The source-pairing term $q$ and the scale valuations still refer to all their designated places. A sharper version of (2) subtracts the discarded sum over all non-twisted places of the active lattice indices.

Both $e$ and $H/h$ are orthogonal projections for the invariant Petersson norm, hence their composition is contractive. After transferring to the prescribed target norm with the specified embedding-by-embedding comparison, Hadamard bounds $\mathcal A_j$ by twice the averaged logarithmic section norms and the corresponding norm-transfer cost. In particular the native S4 produces a coarse size bound from $G\,|\kappa|$ in its mean-log-sup metric. The stated input gives neither a sufficiently sharp comparison with the signed main terms in (4) nor the switch valuation. An inclusion $L_{1,w}\subset L_{2,w}$ at every $w\mid p_*$ would make the latter nonpositive. Full rank alone cannot do this: $L_1=\mathbf Z,L_2=p_*^n\mathbf Z$ gives positive switch $n$. No conclusion about the sign for the actual run pair follows from this example. More invariantly one may use the full projected lattices of the generating lists and the fractional ideal $\det L_2/(\det L_1)$ in (2); their determinant ideals need not be principal.

[Common run selector, coordinates and transported theta lattices](https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AbelianVarietyTheory/Proofs/DivisorProofs/HasIndexBoundOfRuns.lean#L129-L190). [Global theta module and its short summand](https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Formalism/SharpRestriction/Divisibility/WeightAlgebra.lean#L141-L163). [Finite spanning sets under S4](https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Formalism/SharpRestriction/Divisibility/WeightAlgebra.lean#L321-L336). [B4.54a with the exact comparison hypotheses](https://github.com/rh-lean-roadmap/rh-lean-roadmap/blob/02a95b4c62db610642af5f278ee5d0d6df87b348/docs/src/book/main.tex#L8185-L8212). [B8 projected image on this layer](https://github.com/rh-lean-roadmap/rh-lean-roadmap/blob/02a95b4c62db610642af5f278ee5d0d6df87b348/docs/src/book/main.tex#L54143-L54162). [Projector denominator and invariant metric](https://github.com/rh-lean-roadmap/rh-lean-roadmap/blob/02a95b4c62db610642af5f278ee5d0d6df87b348/docs/src/book/main.tex#L21703-L21714).

## Exact cancellation of the large normalization at the recursion prime

For the full-weight short summand the scale in (3) is known explicitly. Put $p_1=p_{\rm de}$, $p_2=p'_{\rm de}$, $u_j=D_F(\kappa_j)+2frn_\kappa$, and $\gamma_j=(g_0g_1)^{fr(n_\kappa-n_F)}$. Here $n_\kappa=n_V=r+t$, $n_F=w_F.n$ and $p_1\ne p_2$. With the native weight addition and scalar ties, $\sigma_{wj}=\sigma_j$ for a *single* global nonzero algebraic integer on this layer. If $Y_{ai}$ denote the unscaled vectors in the original short theta module and $y_{ai}=c_{aj}Y_{ai}$ their normalized counterparts in (3), then
$$
                c_{aj}=\sigma_j\,\gamma_j\, p_a^{u_j}.
\tag{5}
$$
Indeed the full-weight summand is $s_K(g_0g_1)^{frn_\kappa}\operatorname{shortTh}(\kappa)$. In $s_K$ the factor depending on the run is exactly $p_a^{u_j}$. Its common remaining share is the product of $n(w_L)^T n(w_F)$ with the prescribed powers of $Q_S,q,d$. The equality $n(w_L)^T n(w_F)=n(\kappa)$ is the source's weight identity, and $\sigma_j$ uses the very same powers of $Q_S,q,d$ together with $n(\kappa)(g_0g_1)^{frn_F}$. This proves (5) for arbitrary vectors of that summand. The unscaled vectors need only belong to the short module, which is an integral span of the actual generators.

Replace $\mathcal A_j,\alpha_j$ by $\mathcal A_j^{\rm raw},\alpha_j^{\rm raw}$ computed with $Y_{ai}$. Then $\alpha_j=(p_2/p_1)^{D u_j}\alpha_j^{\rm raw}$, and
$$
 \mathcal A_j=\mathcal A_j^{\rm raw}+2\langle\log|\sigma(\sigma_j)|\rangle_\infty+
                 2\log\gamma_j+2u_j\log p_1.
$$
The $p_1$-valuation of the norm of the scalar $(p_2/p_1)^{D u_j}$ is exactly $-[K:\mathbf Q]D u_j$. Thus the last archimedean term cancels in (3), regardless of its size, and the product formula cancels the finite contribution of $\sigma_j$ at every twisted place. In (4) the first three terms in braces may consequently be replaced **exactly** by
$$
 \mathcal A_j^{\rm raw}+
 \frac{2\log p_1}{D[K:\mathbf Q]}\operatorname{ord}_{p_1}
       |N_{K/\mathbf Q}\alpha_j^{\rm raw}|
 +2\sum_{w\notin{\rm Tw}}\ell_w v_w(\sigma_j)+2\log\gamma_j .
\tag{6}
$$
Since $0\le n_\kappa-n_F\le r+t$ and the ranks and logarithmic levels are polynomial in the family parameter, $\sum_j\log\gamma_j=o(b)$. The off-twist scale sum in (6) is supported only at divisors of $g_0g_1Q_S qd$, by the explicit integral formula and $n(\kappa)$ supported at the two level primes. It cannot in general be set to zero. The distinguished-prime factors $p_a^{u_j}$ require no size estimate whatsoever. Formula (6) still requires a bound for the archimedean size of the *actual raw* projected basis and the switch of the two actual raw theta modules. The cutoff, signed main terms and pairing contribution are those of (4).

[Distinguished primes of the two runs](https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AbelianVarietyTheory/Definitions/Divisors/RealisedChainTorusEq.lean#L21-L33). [Ordinary level and own-prime scalars](https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Formalism/SharpRestriction/Divisibility/AbelianOpenPart/OEOsInjective.lean#L48-L81). [Global scale and its coordinate tie](https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AbelianVarietyTheory/Definitions/Jets/EmbShortThLeThetaPlain.lean#L30-L67). [Normalizer under addition of weights](https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AbelianVarietyTheory/Proofs/JetHarmonics/ThetaScaledSpanLeSigmaSmulUnscaledSpan.lean#L61-L105).


On the prescribed weight family the last finite sum of (6) has an ordinary rational-prime formula. Let $b_p^{\rm off}=[K:\mathbf Q]^{-1}\sum_{w\mid p,\ w\notin{\rm Tw}} e_wf_w$. The two type-prime fibres are twisted in full: all entries in the prescribed rows are positive in absolute value and the first row is nonempty at every layer, so its Fock degree is positive, and the identification of base terms forces a nonzero entire fibre into the twist set. Hence $b_{g_0}^{\rm off}=b_{g_1}^{\rm off}=0$. Write $A_j=T D_F(w_L)+D_F(w_F)$, $B_j=T\lceil D_F(w_L)/2\rceil+\lceil D_F(w_F)/2\rceil$. The factor $n(\kappa)$ and the explicit level factors in $\sigma_j$ have support only at the two type primes. The other factor is the rational integer $Q_S^{A_j}(qd)^{B_j}$. Therefore
$$
 \sum_{w\notin{\rm Tw}}\ell_w v_w(\sigma_j)
 =A_j\sum_{p\mid Q_S} b_p^{\rm off}\operatorname{ord}_p(Q_S)\log p
      +B_j(b_q^{\rm off}\log q+b_d^{\rm off}\log d).
$$
The coefficients $b_p^{\rm off}$ only use the given twist set, not a local theta section. On the prescribed size family $b_d^{\rm off}=0$ as well. At each position $w_j(\rho)=e_{j-1}=B_\rho+(j-1/2)h_0>0$, by the marked, thin and thick cases in the prescribed weights. Since $k>1$ and $A$ is nonempty, $F_d(j)=-(k-1)\sum_{t\in A}\min(w_j(0,t),w_j(1,t))/2<0$. The full-fibre implication applies again. The exact off-twist scale is therefore supported only at primes dividing $Q_S q$. Moreover $A_j=D_F(\kappa_j)$ by coordinatewise weight addition, and $0\le 2B_j-A_j\le T+1$ by parity. Summing the rounding error in $2B_j b_q^{\rm off}\log q$ costs at most $m(T+1)\log q=o(b)$ because $T^2\le b$ and $m,\log q$ are polynomial in $x$. Thus to the permitted precision the entire off-twist scale contribution $2\sum_{j,w\notin{\rm Tw}}\ell_wv_w(\sigma_j)$ equals
$$
 \left(\sum_j D_F(\kappa_j)\right)
 \left(2\sum_{p\mid Q_S} b_p^{\rm off}\operatorname{ord}_p(Q_S)\log p+
                         b_q^{\rm off}\log q\right)+o(b).
$$
The multiplier in the second parentheses is the same for all layers. It is a known nonnegative quantity on the given selection. [Prescribed positive weights](https://github.com/rh-lean-roadmap/rh-lean-roadmap/blob/02a95b4c62db610642af5f278ee5d0d6df87b348/docs/src/book/main.tex#L6252-L6267). [Definition of the ramified base term](https://github.com/rh-lean-roadmap/rh-lean-roadmap/blob/02a95b4c62db610642af5f278ee5d0d6df87b348/docs/src/book/main.tex#L6281-L6295). [Positive Fock degree and the full nonzero fibres](https://github.com/rh-lean-roadmap/rh-lean-roadmap/blob/02a95b4c62db610642af5f278ee5d0d6df87b348/docs/src/book/main.tex#L31858-L31903).

The signed ramified-prime term in the target itself costs at most the allowed error on these weights. In the notation of the rational hook formula put $B_{\rm Fock}=\sum_jD_F(\kappa_j)$ and $M_d=(k-1)\sum_{j,t}\min\{w_j(0,t),w_j(1,t)\}$. Since $w_j(0,t)\le9b'/4$, $|A|\le f$, $kb'\le b$, $\log d\le L$, one has $0\le M_d\log d\le 9B_0/4$. Thus $2F_*=-B_{\rm Fock}\log(g_0g_1)+2F_{\rm ord}+O(B_0)$, where $F_{\rm ord}$ is the original sum outside $g_0,g_1,d$. The explicit quantity of the preceding paragraph can therefore be combined with $B_{\rm Fock}\log(g_0g_1)$ on the left of (4), keeping the positive marked term with its full sign. The uniform bound for the resulting signed arithmetic expression remains open. [Bounds on the smaller ramified weights](https://github.com/rh-lean-roadmap/rh-lean-roadmap/blob/02a95b4c62db610642af5f278ee5d0d6df87b348/docs/src/book/main.tex#L42928-L42933).
