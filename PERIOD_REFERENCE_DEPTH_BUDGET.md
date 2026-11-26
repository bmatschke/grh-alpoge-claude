# The finite reference-depth budget for a nonterminal period row

Fix a supplied nonterminal good cover in period entry 7, its coefficient field, algebraic integral frames and the weights of Roadmap B8.25g. Write $T=T_*$, $L_x=\log b$ and $E_p=fmbL_x\log\log x$. Under the chart, jet and theta comparison hypotheses of B8.28 on that datum, the original theta weight has nonnegative upper allowances $e_\ell$ such that

$$
 d_\ell^{1/2500}(a,N)\le e_\ell,\qquad
       T\sum_\ell e_\ell\log\ell\ll E_p .
$$

With the flat-degree and determinant-line hypotheses of B8.28z on the cover, the same assertion holds for the quotient weight $u_1$, with the additional allowances in the last paragraph below. All constants in the prime sum are uniform in the prescribed family range. This replaces the over-budget large-block factorial estimate on the supplied datum. The comparison below imports local results of the human-readable Roadmap and identifies their exact uses. The [degree-weighted intersection estimate](PERIOD_WEIGHTED_ROOT_INTERSECTION.md) at the B8.26 cutoff and realization of the geometric data on the selected family are separate inputs. [Earlier factorial estimate](PERIOD_THETA_DEPTH_AT_MARKED_LEVEL.md) · [Reference-depth assembly in the Roadmap][assembly]

## The depth after scalar normalization

At a place $\lambda\mid\ell$, normalize the absolute valuation by $v_\ell(\ell)=1$. A block of size $i$ and exponent $n=c_{\tau i}$ has depth $\nu_{\tau i}(n;y)$, the infimum of the valuations of
$\det(D_{u_a}^{(b)})_{a,b\le i}^n F(0)$ on integral formal functions of $i$ copies. The $D_{u_a}^{(b)}$ are invariant directional derivatives on their respective copies, and the definition allows all compatible charts. Write $S(y)=\sum_{\tau,i}\nu_{\tau i}(c_{\tau i};y)$.

Suppose $a_0\le S(y)\le b_0$ for every algebraic integral frame at this place, with the lower bound also valid for every integral frame. In the tame theta interpolation at $\ell\ne g_0,g_1$, the cost to the reference depth is at most
$$
 b_0-\frac{\lfloor e_\lambda\max(0,a_0)\rfloor}{e_\lambda},
 \qquad e_\lambda=\operatorname{ord}_\lambda(\ell).
 \tag{1}
$$
Indeed, the saturated invariant derivatives preserve integral series, so $S\ge0$. Each nonzero block has $2i$ disjoint columns available. B8.28k,o take two copies of each column in an isotropic combination and identify the least valuation of this harmonic differential, including its theta-connection twist, with $S(y)$. Restriction along the limiting integral CM action matches the twisted jets to integral formal-group jets, and disjoint columns make the infima additive by testing products and expanding monomials. B8.28p approximates the local polynomial by a global harmonic differential to precision strictly above $b_0$ plus the uniform chart denominator. Thus the same interval works at all frames at this place for that one global differential. [Isotropic column comparison][columns] · [Uniform harmonic approximation][approx]

Tame interpolation on the base level $g_0g_1$ now gives two bounds. Every characteristic section has valuation at least $a=\max(0,a_0)$ on every frame over $\lambda$. At the specified frame some characteristic has valuation at most $b_0+\phi/(2500v(\ell))$, where $\phi$ uses the trait-normalized valuation $v$. This is B8.28m,n using the short period basis and the degree-$D$ jet. The full-size CM-type minor forces cuspidality. Multiply this section by a coefficient scalar of $\lambda$-order $-\lfloor e_\lambda a\rfloor$, clearing denominators at the other places as follows. The all-frame denominator gives finite support for the required corrections. Form the fractional ideal having the required lower orders at those places, order zero at the other unlisted places, and order $-\lfloor e_\lambda a\rfloor$ at $\lambda$. An element of that ideal outside its product with $\lambda$ has the exact prescribed order there and clears every other denominator. The normalized valuation changes at every frame above $\lambda$ by exactly $-\lfloor e_\lambda a\rfloor/e_\lambda$. This proves (1), including ramified coefficient fields. The definition of depth takes the supremum over places above this rational prime and over test frames *after* the infimum over integral sections for the given frame. A different section and scalar may therefore serve each target, while each chosen section is integral at every place. The finitely supported object in the denominator argument is a coefficient ideal. There can be infinitely many test frames. [Order of the supremum and infimum](https://github.com/rh-lean-roadmap/rh-lean-roadmap/blob/dc5594a62bb2b94139788df817db693cd939a046/docs/src/book/main.tex#L20632-L20636)

In particular summing the widths of all block intervals costs at most one rounding unit **per prime**, and costs zero extra if all lower endpoints vanish. Pulling back the resulting cusp rules preserves valuations and phase on the deep cover. At the two marked primes the [direct deep-level calculation](PERIOD_THETA_DEPTH_AT_MARKED_LEVEL.md) gives allowance zero for $(a,N)$. [Tame interpolation and scaling][jet] · [Integral frame denominator](PEL_ALL_FRAME_DENOMINATORS.md)

## Bounds for a block

Write $P=k+j-1, Q=m-j, r=P+Q$, with $1\le j<m$. A large block has $\tau$ in the CM type and $k-1\le i\le P$. Small blocks always have interval $[0,i v_\ell(n!)]$, by the degree-$in$ diagonal monomial. At $n=0$ use the zero interval.

At an odd unramified prime $p$, on an algebraic frame choose integral formal characters $\chi_b$ whose differentials on the leading $i$-frame have determinant of valuation at most $R_\tau$. The character-minor theorem B8.28xfa obtains $R_\tau=\sum_{t\ge0}p^{-t-1}\mu_{\overline{\tau_{t+1}}}$ along its Frobenius orbit. Its arithmetic input is the oriented Hodge–Tate cokernel estimate for the abelian quotient and the integral characters in the split torus directions. Laplace expansion of a full-size minor gives the stated bound for each leading minor, since the complementary minors are integral. Applying the determinant differential to the product of the characters evaluates to the $n$-th power of this one determinant. For a large block this gives upper endpoint
$$
 nR_\tau=
 \begin{cases}
 nQ/(p-1),&p\text{ split in }K,\\
 n\{Q/(p-1)+(P-Q)p/(p^2-1)\},&p\text{ inert in }K,
 \end{cases}
$$
where $K$ is the specified imaginary quadratic subfield. Indeed the orbit stays on the CM side in the first case and alternates in the second. At split primes the lower endpoint zero suffices. At the primes dividing $Q_S$, including 2, use the paired, possibly ramified factors of the host. The joint colength bound B8.28xe gives coefficients $t_\tau\ge0$ with $\sum_{\tau\in\Psi}t_\tau\le fQ(1+\delta_p/2)$, where $\delta_p=v_p(|\operatorname{disc}E|)/(2f)$, and upper endpoint $nt_\tau$ on each large block. These $t_\tau$ may vary with the frame. Their displayed sum suffices for a **uniform upper bound for the whole row** and the lower endpoint remains zero. [Character minors and Frobenius orbit][chars] · [Native split chart][splitlean] · [Native unramified length bound][unramlean]

At an odd unramified inert prime with $mp<k$, B8.28xgb supplies a lower endpoint on **every** integral frame,
$$
 \left(i-Q\left(\tfrac32+\tfrac12\log_p n\right)\right)
          \frac{np}{p^2-1}-i^2(1+\log_p n)\qquad(n\ge1).
$$
The proof uses the even Frobenius orbit. At each depth in a basis of integral $p$-typical curves only $Q$ directions per even type are lost to the following odd type. Through the least $h\ge0$ with $n\le p^{2h+1}$, at most $Q(h+1)$ frame directions require radius $1/(p-1)$. The other directions use $(1+p^{-(2h+1)})/(p^2-1)$. Coefficient comparison on the inverse logarithm, followed by the divided-power content of the determinant, gives the displayed estimate. Comparing it with the character upper endpoint cancels the term proportional to $i n p/(p^2-1)$ up to $P-i\le m$. Hence the width is at most
$$
 \frac{m n(4+\frac12\log_p n)}{p-1}+i^2(1+\log_p n).
 \tag{2}
$$
This uses an arithmetic character upper bound on algebraic frames and a formal-group lower bound with a wider domain. The common lower order will be removed by (1). [Full even-orbit proof][fine] · [Native determinant estimate][finelean]

### A smaller pair of radii when $mp\ge k$

Put $s_0=\min(i,Q)$ and $\kappa=\min_{\alpha}v_p(h_\alpha\alpha!)$, over the nonzero coefficients of $\det(Z)^n=\sum_\alpha h_\alpha Z^\alpha$. On every such block the interval can be taken as
$$
 \left[\kappa-
   \frac{n}{p-1}\left(s_0+\frac{i-s_0}{p}\right),\ \kappa\right].
 \tag{3}
$$
For the upper bound choose integral linear coordinates dual to the saturated frame and test the homogeneous monomial attaining $\kappa$. Only the principal symbol survives at zero.

For the lower bound, take the integral $p$-typical coordinates of B8.28xhb on the typed factor of B8.28xga. The input from that construction is an integral coordinate isomorphism with unit tangent matrix, adapted after a unimodular change to the $i$-frame. At most $Q$ of its selected curves have nonzero first nonlinear logarithm layer, since that layer lies in the next type. The usual logarithm coefficients of layer $a\ge1$ have valuation at least $-a$. For a curve whose first layer vanishes, the remaining layers have valuations at least $1-a$. Both bounds follow from the $p$-typical recurrence, in which the first-layer vanishing kills the last summand. [Adapted curves, recurrence and inverse logarithm][two]

Assign radius $R=1/(p-1)$ on curves with nonzero first layer and $R/p$ on the others. Give each input frame variable the radius of its selected curve. In the inverse logarithm the linear term has these orders. A nonlinear term from an ordinary curve has weighted order at least $-a+p^a R\ge R$ for $a\ge1$. A curve with vanishing first layer only contributes for $a\ge2$, where $1-a+p^aR/p\ge R$. The latter inequality is equality at $a=2$, and its left side increases afterwards. Thus every nonlinear term has order at least the *larger* required radius. Induction on total degree preserves the assigned orders of the inverse coordinates. This permits both radii in B8.28xhb to be halved.

An integral test function pulled back to the frame variables has coefficients of valuation at least minus their weighted degrees. Every monomial of the determinant symbol involves each selected row $n$ times across its copies. The valuation of every term of the derivative is consequently at least $\kappa-n\sum_{a=1}^i R_a$, giving (3). A unimodular rebase multiplies the determinant by a unit and the typed projection preserves this depth. Since $s_0\le m$, $i\le k+m-2$ and $k\le mp$, one has $(i+(p-1)s_0)/p\le(k+pm-2)/p\le2m$. The loss in (3) is at most $2mn/(p-1)$. This argument avoids computing $\kappa$, which can be large.

## Summing with the actual dimensions

Let $U=B_0+1, J=2B_0+1, B_0=\lfloor8b/T\rfloor$, use the small-block volume $V$ of B8.28b, and set $A=fmU$. The actual quotient weights have
$$
 \sum_{i\ge k-1}c_{\tau i}\le U\quad(\tau\in\Psi),\qquad
 \sum_{\mathrm{small}}i c_{\tau i}\le V,\qquad
 \max c_{\tau i}\le J .
$$
The first inequality telescopes at $u_{1,\tau,k-2}=0$. The second follows by summation by parts on the short and complementary blocks. On this family $TU\le9b, T(A+V)\ll fmb, TJ\ll b, Tr^3\le b$, and $\log(2J)\ll L_x$. There are at most $f(m+1)$ large blocks. [Gap bounds and actual row][gaps] · [Family bounds and prime sums][sum]

For $p\le J$, the following are nonnegative upper allowances $e_p$ for the full theta weight on the cover. Use the rows in order and put $h_p=\log J/\log p$.

| Prime condition | Upper allowance |
|---|---|
| $p\mid Q_S$ | $A(1+\delta_p/2)+V$ |
| $p\in\{q,d\}$ | $(frU+V)/(p-1)$ |
| Ordinary, split in $K$ | $(A+V)/(p-1)$ |
| Ordinary, inert in $K$, $mp<k$ | $[A(4+h_p/2)+V]/(p-1)+f(m+1)r^2(1+h_p)+1$ |
| Ordinary, inert in $K$, $mp\ge k$ | $(2A+V)/(p-1)+1$ |

At $q,d$ the factorial bound suffices because both primes exceed $4tr+1$ in the host, with $t\ge1$. All ordinary primes here are odd and unramified in $E$. The fourth and fifth rows use (2) and (3) before the single rounding in (1). For $p>J$, use the zero allowance on the cover from the earlier factorial result, including $g_0,g_1$.

The ramified first row summed against $\log p$ costs at most $(A+V)\log Q_S+A\log\operatorname{rd}(E)/2$, and the second costs $O((A+V)\log(qd))$. These logarithms are $O(L_x)$. Elementary prime sums give $\sum_{p\le J}\log p/(p-1)\ll\log(2J)$ and $\sum_{p\le J}\log p\ll J$. The extra $h_p$ in the numerator of the fourth row costs at most $O(A\log(2J)(1+\log\log(3k)))$, by summing $1/(p-1)$ up to $k/m$. For its additive term, $(1+h_p)\log p\le2\log(2J)$ and there are at most $k/m$ such primes. It contributes $O(fr^3\log(2J))$. The displayed family bounds and the polynomial growth of $k$ give $T\sum_p e_p\log p\ll E_p$ as asserted.

Finally put $\mathcal B=\{p:p\mid2d|\operatorname{disc}E|M'\}$ for the actual cover level $M'$. B8.28z compares the integral determinant twists to the original quotient weight on each component, adding $\mathbf1_{p\in\mathcal B}(1+Nfr\delta_p/2)$ to $e_p$. Here $N\le20fr^2$, $\log(2d|\operatorname{disc}E|M')\ll fL_x$, and $T(frL_x)^3\le b$. These additions cost $O(b)$ after multiplication by $T$. The resulting finite Fubini–Study correction therefore fits the prescribed budget. To finish the nonterminal covolume route one must still establish the [weighted intersection lower bound](PERIOD_WEIGHTED_ROOT_INTERSECTION.md) and compare the actual model, metric and section indices. [Quotient-weight comparison][twist] · [Component mean and its hypotheses][mean]

[assembly]: https://github.com/rh-lean-roadmap/rh-lean-roadmap/blob/dc5594a62bb2b94139788df817db693cd939a046/docs/src/book/main.tex#L53634-L53652
[columns]: https://github.com/rh-lean-roadmap/rh-lean-roadmap/blob/dc5594a62bb2b94139788df817db693cd939a046/docs/src/book/main.tex#L52081-L52095
[approx]: https://github.com/rh-lean-roadmap/rh-lean-roadmap/blob/dc5594a62bb2b94139788df817db693cd939a046/docs/src/book/main.tex#L52323-L52343
[jet]: https://github.com/rh-lean-roadmap/rh-lean-roadmap/blob/dc5594a62bb2b94139788df817db693cd939a046/docs/src/book/main.tex#L51877-L51902
[chars]: https://github.com/rh-lean-roadmap/rh-lean-roadmap/blob/dc5594a62bb2b94139788df817db693cd939a046/docs/src/book/main.tex#L52549-L52708
[fine]: https://github.com/rh-lean-roadmap/rh-lean-roadmap/blob/dc5594a62bb2b94139788df817db693cd939a046/docs/src/book/main.tex#L52778-L52970
[two]: https://github.com/rh-lean-roadmap/rh-lean-roadmap/blob/dc5594a62bb2b94139788df817db693cd939a046/docs/src/book/main.tex#L53020-L53107
[gaps]: https://github.com/rh-lean-roadmap/rh-lean-roadmap/blob/dc5594a62bb2b94139788df817db693cd939a046/docs/src/book/main.tex#L53245-L53272
[sum]: https://github.com/rh-lean-roadmap/rh-lean-roadmap/blob/dc5594a62bb2b94139788df817db693cd939a046/docs/src/book/main.tex#L51649-L51681
[twist]: https://github.com/rh-lean-roadmap/rh-lean-roadmap/blob/dc5594a62bb2b94139788df817db693cd939a046/docs/src/book/main.tex#L53570-L53631
[mean]: https://github.com/rh-lean-roadmap/rh-lean-roadmap/blob/dc5594a62bb2b94139788df817db693cd939a046/docs/src/book/main.tex#L20030-L20040
[finelean]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AbelianVarietyTheory/Proofs/DivisorProofs/DetDepthLowerBoundSaturatedEvenType.lean#L199-L283
[splitlean]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AbelianVarietyTheory/Proofs/UnramifiedDepth/ColengthBoundSplitPlaceChart.lean#L32-L74
[unramlean]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AbelianVarietyTheory/Proofs/UnramifiedDepth/LinearDataUnramifiedLengthBound.lean#L64-L124
