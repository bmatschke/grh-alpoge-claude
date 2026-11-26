# Constancy of the reverse theta lifts at the compact square

Fix a matched datum with $p=q=0$. Put $d=a+a'$ and $T=S_0\cup Q$. The two Hermitian spaces $V,V'$ and the skew-Hermitian space $W$ have definite real signatures. The dimension inequalities give $a>a'\ge2$. For a polynomially matched pair $y=(\Phi,\Phi')$ with $\Phi'$ in the designated space $S^\circ$, let
$$
 f_y(h)=sI_V(\Phi)(h)+tI_{V'}(\Phi')(h),\qquad s,t\in\mathbb C .
$$
For $X=V$ or $V'$ and any adelic Schwartz test $\Psi$ for $X\otimes W$, set
$$
 T_{X,\Psi}f_y(g)
   =\int_{[U(W)]} f_y(h)\overline{\theta_X(\Psi)(g,h)}\,dh .
$$
**Both functions of $g$ are constant.** The constants can differ with $X$, $\Psi$, $y$, $s,t$ and the Haar measure. The proof does not require proportionality of the incoming theta integrals. [Signatures and characters][rc-geo] · [Exact input and conclusion][rc-thc] · [Use in the compact base][rc-use]

## Realizing the same input on either side

The adelic quotient of a definite unitary group is compact. The convergent theta sums on products of these quotients are continuous. Integration over compact quotients gives continuous $I_V,I_{V'}$, and the quotient height is bounded. Consequently every $f_y$ satisfies the rapid-decay bounds used by the source, including for matched pairs obtained by varying a finite factor. All theta pairings below converge absolutely. Their left rational invariance follows from rational invariance of the theta sum. Right translation of both factors leaves their Petersson pairing unchanged by unimodularity. [Compact quotient and rapidity][rc-cpt] · [Analytic pairing and covariance][rc-cov]

We use two explicit compatibility statements for the given matching maps. Each unprimed polynomial datum admits a polynomial match with primed test in $S^\circ$, and each primed polynomial datum admits a match. The $V$ integral kills tests matched to zero, and the $V'$ integral kills tests in $S^\circ$ matched to zero. The [full-rank representative](../construction/ROW_DEFINITE_LOCAL_QUOTIENTS.md#full-rank-representatives-at-the-prescribed-split-place) supplies the partners. The [definite local descent](ROW_DEFINITE_THETA_COMPARISON.md#descent-on-each-local-factor) proves the kernel assertions without comparing the two global integrals. Their producers in the pin use the local coinvariant maps and the vanishing of their kernels under theta integration. [Exact quantifiers][rc-input] · [Production of surjectivity][rc-mat] · [Production of the kernel statement][rc-fact]

On matched pairs with second member in $S^\circ$, the map $y\mapsto f_y$ thus factors through its unprimed member. Indeed the difference of pairs with equal first member has the form $(0,\delta')$, whose primed integral vanishes. Denote the resulting map by $C$. Across *all* polynomial matches, $C(\Phi)$ depends only on $\Phi'$: the difference in first members with the same second member matches zero, and $(\delta,0)$ is in the preceding restricted pair space. Denote this second realization by $C'$. This argument uses kernels only for zero matches. A possible extension of the linear maps from these spaces plays no role in their evaluated values. [Two factorizations][rc-facmaps]

For a split local $h_0\in U(W)(F_v)$, simultaneous Weil translation preserves polynomial matching. Enlarge the finite set in the tensor presentation by $v$, using equality of the two unramified vacuum images at added places. The two local operators induce the same endomorphism on the common quotient by the equivariance of the matching maps and their surjectivity. Apply this endomorphism at the $v$ factor of the tensor equality. The $S^\circ$ condition also persists: at its designated place it is a full-row-rank support condition in the split matrix model, preserved by invertible right multiplication. Other places leave that factor unchanged. The defining theta sums then give
$$
 C(\omega_V(1,h_0)\Phi)(h)=C(\Phi)(hh_0),
 \qquad
 C'(\omega_{V'}(1,h_0)\Phi')(h)=C'(\Phi')(hh_0).
$$
For the second equality, choose a matching first member and use the first equality. This gives access to arbitrary local Schwartz variations in the *opposite* oscillator when computing either reverse lift. [Polynomial matching and raw quotient equivariance][rc-finmaps] · [Local tensor argument][rc-trans] · [The two actions on the representatives][rc-actions]

## The good local character

Use places $v\notin T$ whose underlying **rational** prime splits completely in $E$. For such a $v$, choose a prime $w$ of $E$ above it. Write $\nu=\alpha/\beta$. Its $w$ component is unramified, unitary, and satisfies $\nu_w(\varpi_v)\ne1$. In fact the value has infinite order. Here are the arithmetic reasons for that last property. The field $E$ is CM and Galois over $\mathbb Q$. The infinity character of $\nu$ has exponents $k_\tau=m_{\alpha,\tau}-m_{\beta,\tau}>d$ at the chosen CM embeddings. Take a positive power making its finite unit characters trivial, and make a positive power of $w$ principal, say $(z)=w^h$. The idelic product law identifies the corresponding power of the local uniformizer value, up to inversion, with the archimedean phase of $z$. If this value were torsion, so would be the square of that phase. Fix one embedding $\tau_0$. The square is the image under $\tau_0$ of
$$
 \prod_{\tau}\big(g_\tau(z)/g_\tau(\bar z)\big)^{N k_\tau},
 \qquad \tau=\tau_0 g_\tau,\quad N\ge1 .
$$
Complete splitting makes the decomposition group at $w$ trivial, and the chosen CM type and its complex conjugate partition the embeddings. At $w$ only the identity embedding, in the numerator for $\tau_0$, contributes. The valuation $hNk_{\tau_0}$ is nonzero. A root of unity has zero valuation there. The same conclusion holds for $\nu^{-1}$. [Good places and the weight gap][rc-geo] · [Reduction to the CM Hecke value][rc-nu] · [Valuation calculation][rc-val]

## Two rectangular matrices and one square matrix

Let $k=F_v$, $X$ the output space of dimension $n$ and $X'$ the opposite source of dimension $n'$. Then $n+n'=d$. In the split Weil model let $\chi,\chi'$ be the unitary characters occurring in the right actions on the $n$-row and $n'$-row matrices respectively, and $\eta=\chi/\chi'$. On $X=V'$ this ratio is $\alpha_w/\beta_w$, and on $X=V$ it is its inverse. The formulas for the $n$-row test are
$$
 \omega(1,h)A(Y)=\chi(\det h)|\det h|^{n/2}A(Yh),\qquad
 \omega(g,1)A(Y)=\eta(\det g)|\det g|^{d/2}A({}^{t}\!gY).
$$
The first formula on the opposite test uses $\chi'$ and exponent $n'/2$. [Split Weil actions][rc-om] · [Their application in the two orientations][rc-actions]

Fix $g_*\in U(X)(\mathbb A)$ and all test factors outside $v$. Use the realization of $f_y$ on $X'$. Pair this variable input with the output theta test on $X$ at $g_*$. The pairing is linear in the opposite test and conjugate-linear in the output test. Insert $\bar A$ in the output slot and $B$ in the opposite slot to form a bilinear functional $b(A,B)$. Simultaneous right translation leaves the original integral unchanged. Since $\overline{\chi}=\chi^{-1}$, inserting both Weil factors gives
$$
 b(A(\,\cdot\,h),B(\,\cdot\,h))
   =\xi(\det h)b(A,B),\qquad \xi(x)=\eta(x)|x|^{-d/2}.
$$
In particular $\xi(\varpi_v)$ is outside $\mathbb R_{>0}$. Each compactly supported locally constant function on the product of the rectangular matrix spaces is a finite sum of separated tests, by a finite partition into compact-open boxes. The tensor product of the two test spaces is identified with this product test space. Stacking the two blocks therefore gives a well-defined functional $D$ on Schwartz–Bruhat tests on $\operatorname{Mat}_d(k)$ with the same right transformation law. [From a global pairing to local tests][rc-cov] · [Bilinearity, character and stacking][rc-bi] [and][rc-stack]

For completeness, this right transformation law implies
$$
 D(\phi(g\,\cdot\,))=\xi(\det g)D(\phi),\qquad g\in\mathrm{GL}_d(k).
$$
On the open invertible locus the right-equivariant distribution is a scalar multiple of integration against $\xi(\det x)^{-1}d^\times x$. This follows by twisting by the smooth character and uniqueness of Haar integration on locally constant compactly supported functions. The group is unimodular, so the integral also has the displayed left law. For fixed $g$, the difference between the two sides is a right-equivariant distribution supported on the singular matrices. It vanishes by the following rank argument.

In the stratum of rank $r<d$, the image of the matrix is unchanged by right multiplication. A Grassmannian chart trivializes its image bundle and identifies this stratum locally over the image parameter with $H\backslash\mathrm{GL}_d(k)$, where $H$ fixes the standard surjection onto $k^r$. In a basis adapted to it, $H$ consists of matrices with their first $r$ rows equal to $(I_r,0)$. Hold a compactly supported test in the image parameter fixed. A right-equivariant distribution on the orbit can be lifted to the group by integrating tests over the left $H$ fibers with right Haar measure on $H$. This averaging surjects onto orbit tests: local sections on pivot charts and a compact-open bump of integral one on $H$ give local preimages, and a finite partition handles a compact support. The lifted distribution has on the one hand the right-equivariant Haar description above. On the other hand, left translation by an element of $H$ contributes a positive real modular factor. Taking the element acting by $\varpi_v$ on just one unused basis vector forces $\xi(\varpi_v)$ to be positive real if the distribution is nonzero. Thus it vanishes. Finite sums of product tests recover the whole chart. Starting with support in rank $\le d-1$, restrict successively to rank $r$ inside the open set of ranks $\ge r$. Tests there restrict to tests on the closed stratum, and every compact-open test on the stratum extends by a finite compact-open partition in the ambient open set. This removes each stratum in turn. The pin proves the same vanishing by a pivot-chart induction using translations of the free row coordinates. [Open orbit and singular-support vanishing][rc-loc] · [Pivot-chart induction][rc-ind]

Apply the displayed left law to $\operatorname{diag}({}^{t}g,I_{n'})$, which acts only on $A$. Returning to the conjugate-linear output slot contributes the conjugate of the scalar in $\omega(g,1)$. Its product with the left-covariance scalar is exactly
$$
 \overline{\eta(\det g)|\det g|^{d/2}}\,
       \xi(\det g)=1.
$$
The reverse theta lift is therefore invariant under the entire local group $U(X)(F_v)\simeq\mathrm{GL}_n(k)$. Linearity on the opposite slot and conjugate linearity on the output slot extend this identity from pure tensors to every specified polynomial input and every Schwartz output test. The place $v$ can be any of the good places above, whether or not a particular finite presentation originally included it. [Cancellation at the original pairing][rc-cancel]

## From local invariance to a constant on the full quotient

Let $f(g)=T_{X,\Psi}f_y(g)$. Its full left stabilizer $L=\{u:f(ug)=f(g)\ \text{for all }g\}$ is a closed subgroup. It contains $U(X)(F)$. It contains each good local group since conjugation by an adelic element preserves the single-place subgroup, turning right invariance into left invariance. At any one such $v$, $SU(X)(F_v)\simeq\mathrm{SL}_n(F_v)$ is noncompact. The strong approximation theorem for connected simply connected absolutely almost simple groups, applied to $SU(X)$ off this $v$, places $SU(X)(\mathbb A)$ in $L$. This uses $n\ge2$ and works for a definite form since the split place supplies noncompactness. [Closed stabilizer][rc-stab] · [Application of strong approximation][rc-su] · [Platonov, strong approximation theorem](https://doi.org/10.1070/IM1969v003n06ABEH000838)

It remains to treat the determinant torus $U(1)$. Choose a rational nonsingular Hermitian line in $X$. Acting by the scalar $z$ on the line and by the identity on its orthogonal complement gives a continuous determinant section $S$. The subgroup $N=S^{-1}L$ contains the rational norm-one elements and the norm-one elements supported at each good place. Pull it back to the ideles of $E$ by $b\mapsto b/\bar b$. This surjects onto $U(1)(\mathbb A)$ by adelic Hilbert 90. The pullback contains $E^\times$ and the positive real scaling subgroup, so its quotient is compact by compactness of the norm-one idele class group. It also contains $E_w^\times$ for all but finitely many degree-one primes of $E$: outside ramification, degree one in a Galois extension of $\mathbb Q$ implies complete splitting, and $b/\bar b$ is then supported on the allowed split place of $F$. [Rational determinant section][rc-sec] · [Idelic pullback and its local subgroups][rc-idel]

A proper closed pullback would yield a nontrivial unitary Hecke character $\omega$ of $E$ trivial locally at all these degree-one primes. For real $\sigma>1$, the Euler product for $L(\sigma,\omega)/\zeta_E(\sigma)$ differs from one only at finitely many exceptional degree-one primes and the primes of residue degree at least two. The latter contribution to the absolute value of the logarithm stays bounded down to $\sigma=1$ since $\sum_p p^{-2}<\infty$, with at most $[E:\mathbb Q]$ factors above each $p$. The finitely many local ratios are bounded above and away from zero as well. Thus $|L(\sigma,\omega)|$ tends to infinity with $\zeta_E(\sigma)$ as $\sigma\downarrow1$. Hecke's continuation gives holomorphy at the real point $1$ for every nontrivial unitary character, a contradiction. This uses only regularity at that point and the pole of the Dedekind zeta function. It eliminates the entire determinant obstruction. Every $g$ is the product of $S(\det g)\in L$ and a determinant-one element already in $L$. Hence $f(g)=f(1)$. [The Hecke character test][rc-hecke] · [Compact-quotient character separation][rc-char] · [Hecke input in the pin][rc-hinp]

In the compact-base comparison take $X=V'$ and $\Psi=\Phi'$ from the matched pair. Integrating this constant over $[U(V')]$ and interchanging the two integrations gives
$$
 T_{V',\Phi'}f_y(g)=
 \frac{\langle f_y,I_{V'}(\Phi')\rangle_{[U(W)]}}
      {\operatorname{vol}([U(V')])}.
$$
This is the constant with the original Haar measures and the convention linear in the first argument. It can be zero for a particular test. The matching surjectivity and zero-kernel statements used above concern how the actual maps represent matched pairs, and must be supplied if working from abstract test spaces. The local distribution argument and the determinant calculation introduce no further multiplicity assumption. The separate reverse-lift squared-norm identity used next in the compact-base proof comes from doubling and Siegel–Weil. [Volume evaluation][rc-use] · [Separate doubling identity][rc-dbl]

[rc-geo]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AbelianVarietyTheory/BlockTheory/DivisorBase/WeilTensorModels.lean#L350-L393
[rc-thc]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/WeilBound/ThetaLifts/LatticeBasics/PairsStable.lean#L87-L101
[rc-use]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/WeilBound/ThetaLifts/LatticeBasics/PolZero.lean#L83-L102
[rc-cpt]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/WeilBound/ThetaLifts/LatticeBasics/PolZero.lean#L44-L71
[rc-cov]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/WeilBound/ThetaLifts/LatticeBasics/ThConstAn.lean#L83-L110
[rc-input]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AbelianVarietyTheory/Definitions/Divisors/CTSmallCone.lean#L203-L227
[rc-mat]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/WeilBound/ThetaLifts/WeilDomination/MatchEx.lean#L158-L161
[rc-fact]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/WeilBound/ThetaLifts/CartanFactorisation/Factor.lean#L117-L143
[rc-facmaps]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/WeilBound/ThetaLifts/LatticeBasics/ThConst.lean#L99-L129
[rc-finmaps]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AbelianVarietyTheory/BlockTheory/DivisorBase/WeilTensorModels.lean#L458-L481
[rc-trans]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/WeilBound/ThetaLifts/LatticeBasics/ThConstMatch.lean#L108-L149
[rc-actions]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/WeilBound/ThetaLifts/LatticeBasics/ThConst.lean#L134-L168
[rc-nu]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/WeilBound/ThetaLifts/LatticeBasics/GoodNe.lean#L42-L62
[rc-val]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AbelianVarietyTheory/Proofs/DivisorProofs/HeckeValueNotFiniteOrder.lean#L24-L96
[rc-om]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/WeilBound/ThetaLifts/LatticeBasics/ThConstInv.lean#L67-L77
[rc-bi]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/WeilBound/ThetaLifts/LatticeBasics/ThConstInv.lean#L99-L120
[rc-stack]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/WeilBound/ThetaLifts/LatticeBasics/ThConstLoc.lean#L113-L147
[rc-loc]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/WeilBound/ThetaLifts/LatticeBasics/LocDistE.lean#L37-L92
[rc-ind]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/WeilBound/ThetaLifts/LatticeBasics/LocDistD.lean#L94-L148
[rc-cancel]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/WeilBound/ThetaLifts/LatticeBasics/ThConstInv.lean#L121-L152
[rc-stab]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/WeilBound/ThetaLifts/LatticeBasics/ConstOfGood.lean#L131-L147
[rc-su]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/WeilBound/ThetaLifts/LatticeBasics/ConstOfGood.lean#L47-L69
[rc-sec]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/WeilBound/ThetaLifts/LatticeBasics/ConstOfGood.lean#L71-L106
[rc-idel]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/WeilBound/ThetaLifts/LatticeBasics/ConstIdele.lean#L122-L172
[rc-hecke]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/WeilBound/ThetaLifts/LatticeBasics/ConstHecke.lean#L31-L80
[rc-char]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/WeilBound/ThetaLifts/LatticeBasics/ConstHecke.lean#L89-L111
[rc-hinp]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AbelianVarietyTheory/PublishedTheorems/TwistedTraceFormula/HeckeLEntireAndNonzeroAtOne.lean#L16-L31
[rc-dbl]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/WeilBound/ThetaLifts/LatticeBasics/CoefLine.lean#L34-L61
