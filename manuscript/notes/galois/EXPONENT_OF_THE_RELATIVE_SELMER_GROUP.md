# A finite class group test for the relative Selmer bound

Fix a primitive Dirichlet character $\chi$ and one of the original windows. Write $E=E_1M_\chi$, $G=\operatorname{Gal}(E/E_1)$, $n=[E:\mathbf Q]$, and let $N$ be the cyclotomic level of the host in ETS39. For odd $\ell$ and $1\le e<t=\lfloor x^{401}\rfloor$ put
$$
 S=\mathcal S_\ell(E,e)^{c=(-1)^e},\qquad Q_{\ell,e}=S/S^G.
$$
Write $\mathcal R$ for the pairs with $\ell\in P_\chi$ or $\ell-1\mid 2e$. ETS38 and ETS39 explain which external estimates allow the height argument to retain just this sum. The following bounds also apply to every subset of $\mathcal R$. [Invariant part on the original window](EVEN_TWISTS_AND_RANK_THREE_AUTOMORPHY.md#claim:ETS38) · [Nonresonant orbit estimate](EVEN_TWISTS_AND_RANK_THREE_AUTOMORPHY.md#claim:ETS39)

## How much can the number of generators cost?

<!--
% BEGIN RSE1
-->

<span id="claim:RSE1"></span>Let $a_{\ell,e}$ be the least nonnegative integer such that $\ell^{a_{\ell,e}}Q_{\ell,e}=0$, and put $A=\max_{(\ell,e)\in\mathcal R}a_{\ell,e}$, with empty maximum zero. There is a constant $C$ independent of the window data (with $\chi,\varepsilon$ fixed) such that, eventually,
$$
 A\log 3\ \le\ \sum_{\mathcal R}\log|Q_{\ell,e}|\ \le\ A x^C,
 \qquad
 \sum_{\mathcal R}\log |Q_{\ell,e}[\ell^m]|\le m x^C\quad(m\ge0).
$$
In particular, for any fixed $0<\eta<\delta<1/2$, the part killed by $\ell^{\lfloor\exp(\eta x^\varepsilon)\rfloor}$ costs at most $\exp(\delta x^\varepsilon)$ in the log-order sum. This holds up to the original cutoff at every remaining prime.

To see the generator bound, put $L=E(\mu_\ell)$ and $d=[L:\mathbf Q]\le n(\ell-1)$. The argument in ETS22 applies to $L/E$, of degree dividing $\ell-1$. It realizes the $\ell$-primary part of $K_{2e}(\mathcal O_E)$ as a direct summand upstairs. By ETS15 the dual of the strict group embeds in the downstairs group. Hence $Q_{\ell,e}^\vee$ is a subquotient of the upstairs group. The generator number of a finite abelian $\ell$-group is the dimension of its $\ell$-torsion and also the dimension of its quotient modulo $\ell$. The first description bounds it on subgroups, the second on quotients, and duality preserves it. With $r_{\ell,e}=\dim_{\mathbf F_\ell}Q_{\ell,e}/\ell Q_{\ell,e}$ we obtain
$$
 r_{\ell,e}\log\ell\le\log h_L+d\log\ell
 \le\tfrac12 d^2\log(N\ell)+d\log\ell.
$$
Indeed KB6 applies to $H^2(G_{L,S_\ell},\mathbf Z_\ell(e+1))$ since $L$ contains $\mu_\ell$. The comparison with the even $K$-group is the one in ETS9. The class-number bound (KB.17) gives $\log h_L\le (d/2)\log|\operatorname{disc}L|$. The conductor-discriminant formula gives $|\operatorname{disc}L|\le(N\ell)^d$, since every character of the abelian field $L$ has conductor dividing $\operatorname{lcm}(N,\ell)$. [Strict group and localization](EVEN_TWISTS_AND_RANK_THREE_AUTOMORPHY.md#claim:ETS15) · [Prime-to-degree descent](EVEN_TWISTS_AND_RANK_THREE_AUTOMORPHY.md#claim:ETS22) · [The generator and class-number estimates](../../../research/modules/construction/k_theory_bridge/main.tex#L393-L535)

On these windows $n$ and $\log N$ are polynomially bounded in $x$ by ETS37. For a remaining pair, $\ell$ belongs to a fixed finite set or $\ell\le2t-1$. There are at most $(t-1)(|P_\chi|+2t)$ pairs. Thus $\sum_{\mathcal R}r_{\ell,e}\log\ell\le x^C$ for sufficiently large $x$. Each cyclic factor contributes at most $m\log\ell$ to the log-order of its subgroup killed by $\ell^m$. A factor of order $\ell^A$ contributes at least $A\log 3$ when $A>0$. These two observations prove all three estimates. [Growth of the moving field and level](EVEN_TWISTS_AND_RANK_THREE_AUTOMORPHY.md#claim:ETS37)

<!--
% END RSE1
-->

## The strict group at one finite layer

<!--
% BEGIN RSE2
-->

<span id="claim:RSE2"></span>For every $j\ge1$ put $b=1+\lfloor\log_\ell n\rfloor$, $L=E(\mu_{\ell^{j+b}})$, $D=\operatorname{Gal}(L/E)$, and $V=(\mathbf Q_\ell/\mathbf Z_\ell)(-e)$. Write $C_L=\operatorname{Cl}(\mathcal O_L[1/\ell])$, the ordinary class group modulo the classes of the primes above $\ell$. There is a natural isomorphism
$$
 \mathcal S_\ell(E,e)[\ell^j]\ \simeq\
 \operatorname{Hom}_{D}(C_L,V[\ell^j]).
$$
The target of a homomorphism carries the inverse cyclotomic twist. The field automorphisms of $E/\mathbf Q$ act on the right by lifting to $L$ and acting on both the ideals and the values. Equivariance under $D$ makes the action independent of the lift. The field $L$ works simultaneously for every positive twist $e$.

First restrict to $E_\infty=E(\mu_{\ell^\infty})$. This identifies the divisible-coefficient strict group with the twisted invariant characters of $G_{E_\infty}$ unramified everywhere and split above $\ell$, as in TW3. For clarity, the cyclotomic image here may have a finite subgroup of order dividing $\ell-1$. Its open principal-unit subgroup is isomorphic to $\mathbf Z_\ell$. On this subgroup a topological generator acts on $V$ by a scalar $u^{-e}\ne1$. The map $u^{-e}-1$ is surjective on $V$, so the two-term complex for $\mathbf Z_\ell$ gives $H^1=H^2=0$. Averaging over the prime-to-$\ell$ quotient gives the same vanishing for the full image. Inflation–restriction now gives the global identification. At $v\mid\ell$ the local image is open as well, so vanishing of the local $H^1$ descends the splitting condition. Inertia away from $\ell$ is unchanged under the cyclotomic tower. [Twisted tower descent and the local calculation](../../../research/modules/galois/simultaneous_cohomological_windows/main.tex#L338-L405)

To realize a class killed by $\ell^j$ on the stated finite field, lift it to $H^1(E,V[\ell^j])$ by the multiplication exact sequence on $V$. At $v\mid\ell$ its restriction is the boundary of some $z\in V^{G_{E_v}}$. Write $U_i=1+\ell^i\mathbf Z_\ell$. The local cyclotomic image has index at most $[E_v:\mathbf Q_\ell]\le n$ in $\mathbf Z_\ell^\times$. Its intersection with the procyclic group $U_1$ is $U_{1+s_v}$ with $\ell^{s_v}\le n$. In particular it contains $U_b$. For odd $\ell$, $v_\ell((1+\ell^b)^e-1)=b+v_\ell(e)$, by the binomial theorem (raising to the $\ell$th power raises the valuation by one). Thus $z$ is killed by $\ell^{b+v_\ell(e)}$. A preimage under multiplication by $\ell^j$ is killed by $\ell^{j+b+v_\ell(e)}$. On $G_{L_w}$ at any $w\mid v$ the cyclotomic character lies in $U_{j+b}$, whose $e$th powers lie in $U_{j+b+v_\ell(e)}$. Hence this preimage in the *twisted* module is fixed over $L_w$. Thus the boundary vanishes over that completion. Away from $\ell$ the action on $V$ is unramified, and $V^{I_v}=V$ is divisible, so the finite lift already vanishes on inertia. Also $V[\ell^j]$ is trivial over $L$. The restricted cocycle is therefore a character of $C_L$ by Artin reciprocity, with the indicated equivariance. The ambiguity of the global lift is a boundary from $V^{G_E}$. Its elements satisfy the same order bound by restriction to any $v\mid\ell$, so that boundary vanishes over $L$ too. Coboundaries with values in $V[\ell^j]$ vanish upon restriction to $G_L$. This constructs the map and its further restriction to $G_{E_\infty}$ agrees with the injective infinite-layer map. [The local invariant bound](EVEN_TWISTS_AND_RANK_THREE_AUTOMORPHY.md#claim:ETS15) · [Artin reciprocity for the class group](https://www.jmilne.org/math/CourseNotes/CFT.pdf)

Conversely, restrict an equivariant character of $C_L$ to $G_{E_\infty}$. It is a twisted invariant strict character and hence descends uniquely to a strict class on $E$, killed by $\ell^j$. To check that the original character is recovered, it suffices to show that a character of $C_L$ trivial on $G_{E_\infty}$ is zero. Such a character factors through $\operatorname{Gal}(E_\infty/L)$. Fix $v\mid\ell$. As just proved, the local cyclotomic image contains $U_{j+b}$, and the global image does too. The local decomposition image over $L$ and the global group $\operatorname{Gal}(E_\infty/L)$ are both $U_{j+b}$. Since the character is split at the chosen place, it vanishes on this entire group. This proves surjectivity and the naturality follows from restriction, the coefficient sequence and Artin reciprocity. When $E$ is unramified at $\ell$, the local cyclotomic image is all of $\mathbf Z_\ell^\times$ since the local cyclotomic extensions of $\mathbf Q_\ell$ are totally ramified. The same proof then permits $b=1$ for all twists. If in addition $\ell-1\nmid e$, the local invariant groups vanish already on the first torsion layer. There are no local or global boundaries to absorb, and the same isomorphism holds with $b=0$. Thus the two sorts of resonance $\ell-1\mid 2e$ at an unramified prime require at most one extra layer between them.

<!--
% END RSE2
-->

## Detecting a single class of large order

<!--
% BEGIN RSE3
-->

<span id="claim:RSE3"></span>Choose a generator $\sigma$ of $G$ and write $d_G=|G|$, $B=v_\ell(d_G)$ and $T_G=\sum_{i=0}^{d_G-1}\sigma^i$. In the notation of RSE2 the following test at $j=m+1$ detects whether $\ker(T_G:S\to S)$ has exponent greater than $\ell^m$. It asks for a surjective character
$$
 f:C_L\longrightarrow V[\ell^{m+1}],
 \qquad f(\tau I)=\tau f(I)\ (\tau\in D),\qquad c f=(-1)^e f,\quad T_G f=0.
$$
All actions in this formula are the actions on homomorphisms from RSE2, including their action on values. If $a=a_{\ell,e}$ from RSE1, and $k$ is the least integer such that $\ell^k\ker T_G=0$, then
$$
                         a\le k\le a+B.
$$
Thus at $\ell\nmid d_G$ the test detects $a>m$ exactly. At every odd $\ell$ the uncertainty in $a$ is bounded by the fixed $v_\ell([M_\chi:\mathbf Q])$.

Indeed $z\mapsto(\sigma-1)z$ identifies $S/S^G$ with $(\sigma-1)S\subset\ker T_G$. The polynomial $d_G-(1+X+\cdots+X^{d_G-1})$ is divisible by $X-1$ in $\mathbf Z[X]$. Evaluation at $\sigma$ gives $d_G\ker T_G\subset(\sigma-1)S$. This proves both inequalities, including the case of a trivial group. A finite abelian $\ell$-group has exponent greater than $\ell^m$ precisely when it contains an element of exact order $\ell^{m+1}$. Applying RSE2 to the simultaneous sign and norm conditions identifies such an element with the displayed surjection.

One can test this on the totally real field $L^+$ alone. Complex conjugation on $V[\ell^j]$ is multiplication by $(-1)^e$. Thus the sign condition on $f$ says exactly $f(cI)=f(I)$ on ideal classes. With $C_{L^+}=\operatorname{Cl}(\mathcal O_{L^+}[1/\ell])$, norm and extension of ideals induce maps $C_L\rightleftarrows C_{L^+}$. Their compositions are $1+c$ upstairs and $2$ downstairs, including at ramified primes, and both maps preserve the subgroups generated by primes over $\ell$. Since $2$ is a unit at $\ell$, norm identifies the $c$-coinvariants of $C_L\otimes\mathbf Z_\ell$ with $C_{L^+}\otimes\mathbf Z_\ell$. Pullback by norm therefore identifies the characters in the test with surjections from $C_{L^+}$ subject to the same $D$-equivariance and $T_G f=0$. The value action still comes from the lifts to $L$. In particular a surjection yields an everywhere unramified cyclic extension of $L^+$ of degree $\ell^j$ in which every prime above $\ell$ splits. The equivariance and norm equations select the extensions and identifications of their cyclic groups required here. [Ideal classes and the splitting condition](https://www.jmilne.org/math/CourseNotes/CFT.pdf)

In particular the following two assertions are equivalent, allowing different fixed constants strictly below $1/2$. On one original window the remaining sum in ETS39 is eventually at most $\exp(\delta x^\varepsilon)$ for some $0<\delta<1/2$. Equivalently, for some $0<\eta<1/2$ on that window, at every remaining pair the displayed surjection is absent at $m=\lfloor\exp(\eta x^\varepsilon)\rfloor$. For the forward implication choose $\eta>\delta$ and use $k\le a+B$ and RSE1. For the reverse implication, absence gives $a\le k\le m$ and RSE1 absorbs $x^C$ into any larger exponent $\delta<1/2$. Both statements require uniformity over the moving host data on the chosen interval. This reduces the outstanding estimate to the order of one specified kind of cyclic quotient of a finite ideal class group. The existence of an interval excluding all these quotients still requires an arithmetic estimate.

<!--
% END RSE3
-->

## Two first-layer tests for all resonant twists at a prime

<!--
% BEGIN RSE4
-->

<span id="claim:RSE4"></span>Fix $E,\ell$ and $j\ge1$. The isomorphism type of the group of elements killed by $\ell^j$ in the same-sign norm kernel of RSE3 depends on $e\ge1$ only through its residue modulo $\varphi(\ell^j)$. For $\ell\nmid|G|$ this also holds for $Q_{\ell,e}[\ell^j]$. In particular, at every resonant prime outside $P_\chi$, it takes just two tests on finite ideal class groups to decide **which of the two progressions of twists contribute at all**.

Indeed one can use the same $L$ in RSE2 for every $e$. If $e'\equiv e\pmod{\varphi(\ell^j)}$, the two inverse powers of the cyclotomic character on $\mathbf Z/\ell^j$ coincide. After identifying the two underlying cyclic value groups by a choice of generator, the actions of $\operatorname{Gal}(L/\mathbf Q)$ on values agree. The sign is unchanged since $\varphi(\ell^j)$ is even. Equivariance, sign, and the norm equation therefore cut out isomorphic subgroups for $e$ and $e'$. If $d_G$ is a unit at $\ell$, $(1/d_G)T_G$ projects onto $S^G$ and its kernel is canonically isomorphic to $Q_{\ell,e}$. This identifies its entire subgroup killed by $\ell^j$.

For $j=1$ the two representatives are $e_0=\ell-1$ and $e_1=(\ell-1)/2$. For each representative impose the conditions of RSE3 with values in $\mathbf F_\ell(-e_i)$. Since $\ell\notin P_\chi$ is prime to the late resonant level and to $|G|$, the real field $(E(\mu_{\ell^2}))^+$ suffices for both tests; $(E(\mu_\ell))^+$ already suffices for $e_1$. If the corresponding character space is zero, the quotient $Q_{\ell,e}$ vanishes for **every** positive $e\equiv e_i\pmod{\ell-1}$, since a nonzero finite $\ell$-group has nonzero $\ell$-torsion. If the space has dimension $r>0$, every twist in that progression has exactly $r$ cyclic factors in its quotient. A nonzero first layer leaves their orders to be bounded by the higher-layer test. For example at $\ell=5$ the two tests concern $e=4$ and $e=2$, and determine the generator numbers at every resonant even twist at that prime whenever $5$ is eligible.

<!--
% END RSE4
-->
