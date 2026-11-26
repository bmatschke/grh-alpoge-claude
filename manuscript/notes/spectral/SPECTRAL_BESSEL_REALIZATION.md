# The Bessel period on the shifted discrete series

Fix a real place, put $n=2r+k+1$, and write $G=U(k+r,r+1)$ in the Cayley frame. The final vector has Hermitian norm $-T<0$. Its stabilizer in the middle block is $U=U(k)$, and $N$ is the unipotent radical of the ordered isotropic flag. Set $S=U\ltimes N$, $V=V_\pi$ and $\tau(an)=\psi(n)\pi(a)$, where every successive simple-root character is nontrivial. Fix the source's $ds=da\,dn$, $dg$, and $d\mu$ on $S\backslash G$ by quotient integration. The compact action preserves Haar measure on $N$, so $S$ is unimodular. Inner products are conjugate-linear in the first variable. [Actual flags, two sides and transported measures][actual] · [Roadmap B8.02b, Claims 2–4][claims]

For $\|\nu\|_1\le q_0=km^5$, take the discrete series $\sigma=\sigma_\nu$ with parameter $\lambda+\nu$ and the original signature labels. The grid's separation preserves the strict ordering of the infinitesimal character through the shift ball, integer shifts preserve its Harish–Chandra lattice, and the opposite-sign gap stays at least $n^{19}/2$. Harish–Chandra's classification supplies these regular discrete series. Jiang–Sun–Zhu's Theorem A applies to the pair $U(k+r,r+1),U(k)$ with this generic flag character. Pairing the finite-dimensional target with its contragredient gives $\dim\operatorname{Hom}_S(\sigma^\infty,V\otimes\psi)\le1$. Xue's Theorem 1.1 provides a root-number criterion if one wants to determine which individual Hom spaces are nonzero. The moment recursion permits the zero period at a shift. It requires a nonzero normalized period at the initial representation only when the given coefficient is nonzero. [Parameter and shift hypotheses][claims] · [Exact family predicate][family] · [Jiang–Sun–Zhu, Theorem A][jsz] · [Xue, Theorem 1.1][xue]

## Absolute convergence on the actual smooth-vector domain

Write $D$ for the linear span of the $G$-translates of all $K$-finite vectors and $d_\sigma$ for the formal degree for $dg$. The period must accommodate arbitrary $y\in\sigma^\infty$ and $v\in D$. The [noncompact-root and smooth-globalization argument](SPECTRAL_SMOOTH_DECAY.md) proves the quantitative estimate used in the pinned source. For $a=h/(8\sqrt{2(r+1)})$, where $h$ is the opposite-sign gap, it bounds
$$
 |\langle v,\sigma(g)y\rangle|
 \le C_v p_v(y)\,\mathcal N(g)^{1-a}.                         \tag{1}
$$
Here $p_v$ is a finite sum of Hilbert norms of Lie derivatives. We take $\mathcal N(g)=\max(1,\|g\|_{\rm op},\|g^{-1}\|_{\rm op})$, equivalent to the source norm in the fixed Cayley frame. The source derives the estimate for $K$-finite $v$ from its smooth matrix-coefficient decay theorem using the integral exponent $M=\lceil a-1\rceil$ and gap reserve $M+32n^3<h$. Translating the first vector by $g_0$ changes the bound by at most $\mathcal N(g_0)^{a-1}$. Summing gives (1) on $D$. The constants and seminorms may depend on the representation and vector. [Precise domains][domains] · [Decay theorem and gap substitution][decay] · [Extension to the span of translates][translate]

For the ensuing integrals take $b=10n^2$. The grid gives $a-1\ge 2b$. Both $\int_G\mathcal N(g)^{-b}dg$ and $\int_S\mathcal N(s)^{-b}ds$ converge. Indeed, in Cartan coordinates the ball of radius $R\ge2$ in $G$ has Haar volume at most a constant times $(1+\log R)^{r+1}R^{2(r+1)(n-r-1)}$, by the restricted-root Jacobian. On $N$ the triangular chart has $d_N=2M_N+r$ real coordinates, $M_N\le2r^2+r(k+1)$, and $1+|t|\le C\mathcal N(n(t))^2$. Its measure is a constant times Lebesgue measure. Thus the $S$-ball has volume $O(R^{2d_N})$, and both exponents are less than $b$. This uses finiteness alone, so its implied constants do not enter the amplitude. Equation (1) now makes the following a Bochner integral, continuous in $y$ in the smooth-vector topology.
$$
 P(y,v)=\int_S\langle v,\sigma(s)y\rangle\tau(s)^{-1}\,ds
 \quad\in\operatorname{End}(V).                                \tag{2}
$$
The unitary twist has operator norm one. For $v,y\in D$, inversion gives $P(y,v)^*=P(v,y)$. Right translation in $S$ shows that $y\mapsto P(y,v)\xi$ is an $S$-equivariant Bessel map for every $\xi\in V$. [Real unipotent chart and growth][nil] · [Cartan Jacobian][cartan] · [Source continuity and absolute convergence][absolute]

## The quotient norm fixes the period scalar

With $w\in\sigma^\infty, v\in D, \xi\in V$, ordinary discrete-series Schur orthogonality gives
$$
 \int_{S\backslash G}\|P(\sigma(x)w,v)\xi\|^2\,d\mu(x)
 =\frac{\|w\|^2}{d_\sigma}\langle\xi,P(v,v)\xi\rangle.          \tag{3}
$$
To verify the interchange, put $c(g)=\langle v,\sigma(g)w\rangle$. Expanding the square produces the absolute majorant $\|\xi\|^2\int_S\int_G|c(g)c(tg)|\,dg\,dt$. By (1) and $\mathcal N(t)\le\mathcal N(tg)\mathcal N(g)$, the product is at most $C\mathcal N(g)^{-b}\mathcal N(t)^{-b}$. In the expansion the two stabilizer variables are $s,ts$ and $g=sx$. The remaining matrix coefficient of the twist is $\langle\xi,\tau(t)^{-1}\xi\rangle$. Schur orthogonality integrates $\overline{c(g)}c(tg)$ to $d_\sigma^{-1}\|w\|^2\langle v,\sigma(t)v\rangle$, proving (3) including its sign and scale. [Source product-integrability calculation][fubini] · [Formal-degree convention][degree]

If (2) vanishes identically, take $L_\nu=0$. Otherwise choose one nonzero map $L^0(y)=P(y,v_0)\xi_0$. By multiplicity one $P(y,v)\xi=A(v,\xi)L^0(y)$. On $D\times D$, adjoint symmetry makes this a single real scalar $c$ times the operator $L^0(y)L^0(v)^*$, where the vectors denote a column and a dual row. Indeed choose $y_0\in D$ with $L^0(y_0)\ne0$, which exists by smooth density. At $v=y=y_0$, self-adjointness makes the row a real multiple of $L^0(y_0)^*$. Adjoint symmetry at $(y_0,v)$ then determines every other row, and continuity gives the formula for every smooth $y$. Equation (3) makes $P(v,v)$ positive, hence $c>0$. For $L_\nu=\sqrt c\,L^0$ we have the prescribed rank-one identity on the full domain. Taking $v\in D$ with $L_\nu(v)\ne0$, putting $\xi=L_\nu(v)$ in (3), and cancelling $\|\xi\|^4$ gives
$$
 d_\sigma\int_{S\backslash G}\|L_\nu(\sigma(x)w)\|^2d\mu(x)=\|w\|^2 .
$$
The period is determined up to phase. Scaling $ds$ by $c_S>0$ multiplies its magnitude by $\sqrt{c_S}$, divides $d\mu$ by $c_S$, and leaves the displayed isometry intact for fixed $dg$. [Pinned normalization and zero case][normalized]

## Realizing the supplied coefficient

Let $w$ be a unit lowest-type vector and $W$ the continuous equivariant square-integrable coefficient on the quotient in the source, satisfying its reproducing identity. Put $p(g)=d_\sigma\overline{\langle w,\sigma(g)w\rangle}$, and let $R$ denote right translation on the space of square-integrable equivariant sections. Equation (1) gives $p\in L^1(G)$. The identity says $R(p)W=W$. Schur orthogonality gives $p^*=p$, $p*p=p$, and $p*\delta_g*p=\langle w,\sigma(g)w\rangle p$. Consequently
$$
 \langle W,R(g)W\rangle=\|W\|_2^2\langle w,\sigma(g)w\rangle.
$$
Thus $\sigma(g)w\mapsto R(g)W$ extends linearly to a bounded intertwiner of norm $\|W\|_2$, a multiple of an isometry if $W\ne0$. For smooth vectors the intertwiner gives smooth sections. In a local bundle chart the infinitesimal right actions span the tangent directions, and Sobolev embedding bounds evaluation at the identity coset by finitely many smooth-vector seminorms. Evaluation of the intertwiner there gives a continuous Bessel map $B$ with $W(x)=B(\sigma(x)w)$, pointwise by continuity.

If the integrated form (2) is zero on this representation, folding the same reproducing identity over $S\backslash G$ gives $W=0$. Indeed the inner operator on $W(y)$ is, up to adjoint, $d_\sigma P(\sigma(y)w,\sigma(x)w)$, and the second vector belongs to $D$. Fubini holds for almost every $x$ since convolution of the descended norm of $W$ with $|p|$ has $L^2$-norm at most $\|p\|_1\|W\|_2$. Hence nonzero $W$ forces nonzero $L_0$. Uniqueness now gives $B=c_0L_0$ and $\|W\|_2^2=|c_0|^2/d_0$. These arguments establish the smooth realization and the normalized probability measure used by the initial moment. [Exact reproducing and folding identities][reproduce]

## Adjoint on a shifted summand

At an interior shift write $E^*\otimes\sigma_\nu^\infty=\bigoplus_s i_s\sigma_{\nu-e_s}^\infty$ for the defining-dual Pieri decomposition, with coordinate projections $p_s$. Here $E^*$ denotes the dual of the defining complex representation of $G$. The defining-dual weights $-e_s$ have multiplicity one. All unit shifts involved stay in the same regular Weyl chamber, and the multisets of shifted coordinates are pairwise distinct. Consequently the summands have distinct infinitesimal characters for the center of the enveloping algebra. Their characters on the scalar circle all have the same shift. Under translation of discrete series in this chamber the summands are the indicated discrete series. The corresponding smooth decompositions use Casselman–Wallach globalization. The tensor of the invariant Hermitian signature form with the Hilbert form pairs distinct summands to zero. Its restriction to each summand is nondegenerate and is a real scalar multiple of that summand's invariant positive form by irreducibility. Scale $i_s,p_s$ inversely to make the scalar $\epsilon_s\in\{1,-1\}$. This constructs the signed isometry of the source. [Zuckerman's translation principle][zuck] · [Exact signed decomposition][signed]

Let $\omega$ be the fixed dual vector of the first flag column. Tensoring with $\omega$ and contracting against it in the invariant signature form are adjoints, and both commute with $S$. Set $A_s v=p_s(\omega\otimes v)$, $C_s y=\operatorname{contr}_\omega(i_s y)$, so $C_s=\epsilon_s A_s^*$ in the smooth pairings. If $L=L_\nu\ne0$, multiplicity one gives $L_{\nu-e_s}A_s=\kappa_sL$. For $v\in D$, $A_s v$ is in the corresponding translated finite-vector span since the other tensor factor is finite dimensional. Apply the adjoint identity inside the *same* integral (2) to get $P_\nu(C_s y,v)=\epsilon_s P_{\nu-e_s}(y,A_s v)$. Substitute the two normalized rank-one identities and choose $v$ with $Lv\ne0$. This gives
$$
 LC_s=\epsilon_s\overline{\kappa_s}L_{\nu-e_s},\qquad
 LC_s A_s=\epsilon_s|\kappa_s|^2 L .
$$
It also covers a zero neighboring period, in which case $\kappa_s=0$. This proves the absolute scalar identification in the [cofactor calculation](SPECTRAL_BESSEL_COFACTOR.md) and [length moment](SPECTRAL_BESSEL_MOMENTS.md). The proof uses discrete-series translation, the [proved smooth-coefficient decay](SPECTRAL_SMOOTH_DECAY.md), the defining reproducing identity of the given coefficient, and the indicated Haar conventions. The adjoint-functor reader treats restriction to an adjacent unitary group. Here the higher Bessel subgroup also carries the flag character, and the quotient measure fixes the scalar at every nonzero shifted period. [Native signed-adjoint identity][adjoint] · [Reader's adjacent-rank input][reader]

[actual]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AbelianVarietyTheory/Proofs/FlagMeasures/AmplitudeLocalDataMomentPieriHypotheses.lean#L59-L97
[claims]: https://github.com/rh-lean-roadmap/rh-lean-roadmap/blob/94e6a98b4e74932a0298d6bd22d44cf60c62764b/docs/src/book/main.tex#L41481-L41546
[family]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AbelianVarietyTheory/Definitions/Jets/SideFam.lean#L36-L45
[jsz]: https://arxiv.org/abs/0908.1728
[xue]: https://preprint.press.jhu.edu/ajm/sites/default/files/AJM-h-xue.pdf
[domains]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AbelianVarietyTheory/Definitions/Jets/SumIoPrAlt.lean#L29-L38
[decay]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Formalism/LocalToGlobal/SiegelLatticeTheory/BesselDiscreteSeries/DecInfPf.lean#L59-L125
[translate]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AbelianVarietyTheory/Proofs/JetHarmonics/SumNonneg.lean#L30-L65
[nil]: https://github.com/rh-lean-roadmap/rh-lean-roadmap/blob/94e6a98b4e74932a0298d6bd22d44cf60c62764b/docs/src/book/main.tex#L42316-L42350
[cartan]: https://github.com/rh-lean-roadmap/rh-lean-roadmap/blob/94e6a98b4e74932a0298d6bd22d44cf60c62764b/docs/src/book/main.tex#L42480-L42499
[absolute]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/CompanionTheory/AutomorphicTheory/PieriRules/ThetaBesselIsometries/BesselGapVanishing.lean#L100-L140
[fubini]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AbelianVarietyTheory/Proofs/FlagMeasures/BesselFormCoeffProductFubiniIntegrable.lean#L24-L74
[degree]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AbelianVarietyTheory/Proofs/FlagMeasures/BesselFormalDegreeEqOfSchurOrthogonality.lean#L7-L29
[normalized]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AbelianVarietyTheory/Definitions/Jets/SumIoPrAlt.lean#L132-L146
[reproduce]: https://github.com/rh-lean-roadmap/rh-lean-roadmap/blob/94e6a98b4e74932a0298d6bd22d44cf60c62764b/docs/src/book/main.tex#L42212-L42239
[zuck]: https://annals.math.princeton.edu/articles/196-1/p05
[signed]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AbelianVarietyTheory/Definitions/Jets/SumIoPrAlt.lean#L70-L99
[adjoint]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AbelianVarietyTheory/Proofs/JetHarmonics/TensorMomentEstimate.lean#L32-L68
[reader]: https://github.com/adjoint-functor/theta-periods-to-rh-reader/blob/c0fe7c673cb8acaa328bebb2440ee3334c520b9a/tex/periods.tex#L5308-L5326
