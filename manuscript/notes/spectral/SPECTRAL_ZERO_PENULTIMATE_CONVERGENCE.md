# Absolute convergence on the nonsingular real cells with a zero penultimate minor

Let $n=r+1=m/2$ and $G_{\mathbb R}=U(k+r,r+1)$. For a supplied pair of real Bessel flags write $F,F'$ for their matrices of $n$ columns, ending in the vectors of norm $-T,-T'$. Write $d_i$ for the absolute leading cross minors and $\mathcal G=d_n^2-TT'd_{n-1}^2$. On every original represented cell with $\mathcal G>0$, **including $d_{n-1}=0$**, the supplied large-gap Bessel coefficients satisfy
$$
 \frac1{c_N}\int_{R\backslash G_{\mathbb R}}
      \|\Phi(\gamma x)\|\,\|\Phi'(x)\|\,d\nu_R(x)<\infty .             \tag{1}
$$
Here $R=N'\cap\gamma^{-1}N\gamma$, $d\nu_R$ is the actual quotient measure, and $c_N>0$ is the common coefficient normalization. The integrand is the operator norm of the normalized rank-one integrand in the definition of $J$. The original absolute-convergence test only calls for (1) when $d_{n-1}\ne0$. Its ordinary squared Hilbert–Schmidt test calls for a numerical bound also when $d_{n-1}=0$. The proof below establishes (1) and gives a smaller exponent for growth on all these cells. [Original local tests][targets] · [Root normalization and coefficient data][native]

## A degree-$n$ bound in the real orbit coordinates

Write $S,S'$ for the two Bessel groups and $\mathcal N(g)=\max(1,\|g\|_{\rm op},\|g^{-1}\|_{\rm op})$. The involutive Hermitian matrix $H$ in the Cayley coordinates gives $\|g^{-1}\|_{\rm op}=\|g\|_{\rm op}$ on the group. First put $\gamma$ in the monomial normal form by left and right unipotent translations. The alternating column signs between the source's two cross-matrix conventions preserve monomiality and absolute minors. Thus $P=F^*H\gamma F'$ is invertible and monomial. A bounded left or right translate of a fixed orbit only changes the constants in the argument below. [Cross-matrix signs][signs]

On the common-stabilizer quotient of $S\times S'$, choose the source's transverse representative $(s,s')$. Its two upper unitriangular frame matrices are $sF=FV,\ s'F'=F'U'$. The transverse condition is $P^{-1}V^*P$ lower unitriangular. Concretely, the strictly lower entries of $V^*$ split according as conjugation by the monomial $P$ keeps them below or takes them above the diagonal. The latter belong to the common stabilizer. Multiplying lower unitriangular matrices in increasing subdiagonal order removes these entries uniquely, with coefficient one at each elimination. Their common-stabilizer lift acts on the opposite frame by the corresponding conjugate inverse; on the orthogonal complement of the joint span it acts as the identity. This is the section used for the source's exponent $5n^2$. [Transverse and stabilizer patterns][section] · [Section and its orbit disintegration][section2] · [Original polynomial estimate][old]

Put $y=s^{-1}\gamma s'$ and $X=\mathcal N(y)$. With $L=P^{-1}V^*P$ and $U=U'$,
$$
                  M=P^{-1}F^*HyF'=LU,\qquad \|M\|\le C_\gamma X .
$$
For $1\le j\le n$, the leading $j\times j$ square $M_j=L_jU_j$ has determinant one. Since $L_je_j=e_j$, the last column of $M_j^{-1}$ is the last column of $U_j^{-1}$. These entries are cofactors of $M_j$, each of degree $j-1$ in entries of $M$. They give every upper triangular entry of $U^{-1}$, as $j$ varies. Transposing $M=LU$ gives the same bound for $L^{-1}$. Conjugating by the fixed $P$ therefore yields
$$
               \|V^{-1}\|+\|(U')^{-1}\|\le C_\gamma X^{n-1}.         \tag{2}
$$

The span of $F,\gamma F'$ is nondegenerate. Its Gram determinant has absolute value $\mathcal G$, as follows by expanding the two-frame Gram matrix along the isotropic entries. It has the entire ambient negative index $n$. Indeed, the isotropic span of the first $r$ columns of $F$ splits off $r$ hyperbolic planes in the joint span, and its perpendicular modulo this isotropic span contains the final vector of negative norm. Fix a maximal negative plane $E_-$ inside the joint span. For every isometry $a$,
$$
                \|a\|\le C_\gamma(1+\|a|_{E_-}\|).
$$
To see this, choose a fixed change to a signed orthonormal basis adapted to $E_-$. In this basis write $a=\bigl(\begin{smallmatrix}A&B\\ C&D\end{smallmatrix}\bigr)$. Unitarity gives $A^*A=1+C^*C$ and $DD^*=1+CC^*$. Hence $\|C\|\le\|D\|$ and $\|A\|\le(1+\|D\|^2)^{1/2}$. The last block column is controlled by the restriction to $E_-$. Returning to the original basis costs a fixed factor.

On the joint spanning vectors one has $s^{-1}F=FV^{-1}$ and $s^{-1}\gamma F'=yF'(U')^{-1}$. Both are $O_\gamma(X^n)$. For the primed side use $s'^{-1}F'=F'(U')^{-1}$ and $s'^{-1}\gamma^{-1}F=y^{-1}FV^{-1}$, on the isometric joint span $\gamma^{-1}\operatorname{span}(F,\gamma F')$. We have proved the pointwise bound
$$
          \mathcal N(s)+\mathcal N(s')\le C_\gamma\mathcal N(s^{-1}\gamma s')^{\,n}.       \tag{3}
$$
The constant may depend on the two frames and their relative position. No proper leading cross minor was inverted.

## Integrating the two actual Bessel coefficients

Take Haar probabilities on the two compact stabilizers and the supplied unipotent Haar measures on $S,S'$. Use the same stabilizer Haar $d\mu_R$ that disintegrates $dg$ into $d\mu_R\,d\nu_R$, including the factor $\theta'$ on the source root measure. Write $d\nu$ for the corresponding quotient of $ds\,ds'$ by $t\in R$ acting as $(s,s')\mapsto(\gamma t\gamma^{-1}s,ts')$. Measures on $G_{\mathbb R}$ and its subgroups are unimodular here.

Put $a=4(k+r)n$. Balls of $\mathcal N$-radius $Y\ge2$ in $G_{\mathbb R},S,S'$ have Haar volume $O(Y^a)$, with data-dependent constants. For the group, Cartan integration with largest parameter $\log Y$ bounds the volume by $O((1+\log Y)^nY^{2n(k+r)})$. For a closed Bessel subgroup, disintegrate Haar measure of $G_{\mathbb R}$ on its quotient. Above a relatively compact quotient neighborhood of positive measure choose representatives in a fixed compact set. Its product with the subgroup ball is contained in a group ball of radius $C Y$, giving the same upper bound. [Cartan growth on the original group](SPECTRAL_SMOOTH_DECAY.md)

Fix a compact stabilizer neighborhood of positive finite Haar measure. Every quotient point with $\mathcal N(s^{-1}\gamma s')\le Y$ has by (3) a representative of heights at most $C_\gamma Y^n$. Multiplying by the fixed neighborhood puts that much stabilizer mass inside the product of two group balls of radii $C'_\gamma Y^n$. Weil disintegration and the preceding bounds give
$$
 \nu\{\mathcal N(s^{-1}\gamma s')\le Y\}\le C_{\gamma,\mu_R}Y^{2na}.
$$
Consequently $Q_{\gamma,b}=\int\mathcal N(s^{-1}\gamma s')^{-b}d\nu<\infty$ for every $b>2na$, by dyadic summation.

On each side the [normalized Bessel realization](SPECTRAL_BESSEL_REALIZATION.md) represents $\Phi(y)$ as a nonzero fixed scalar times
$\int_S m_v(s^{-1}y)\tau(s)\xi\,ds$, where $m_v(y)=\langle v,\sigma(y)w_0\rangle$, $w_0$ is the supplied lowest-type vector and $\tau$ is the unitary compact-type and character twist. Choose a compact-finite $v,\xi$ detecting the nonzero normalized period, and likewise on the primed side. A zero coefficient gives (1) immediately. This representation follows by applying the rank-one period identity to $\sigma(y)w_0,v,\xi$ and dividing by the resulting nonzero scalar. Absorb the two fixed comparison and vector norms into constants $C_v,C_{v'}$. Inversion of $s$ or a conjugation of the character leaves the absolute majorant unchanged.

Choose $b=2na+1,\ e=b+a+1$. The supplied large-gap [smooth decay estimate](SPECTRAL_SMOOTH_DECAY.md) gives $|m_v(y)|\le C_v\mathcal N(y)^{-e}$ on the whole group, and correspondingly on the other side. Indeed $e=O((k+2r+1)^3)$, whereas the original opposite-sign gap is at least $(k+2r+1)^{19}/2$ on the shifted grid and the smooth coefficient exponent is the gap divided by $8\sqrt{2n}$, minus one. Put $I_{e-b}=\int_{G_{\mathbb R}}\mathcal N(x)^{-(e-b)}dg(x)<\infty$.

Expand the two absolute majorants in (1). For nonnegative integrands the two Weil disintegrations exchange $ds\,ds'\,d\nu_R(x)$ with $d\nu(s,s')\,dg(x)$. Indeed,
$\mathcal N(s^{-1}\gamma x)^{-e}\mathcal N(s'^{-1}x)^{-e}$ at $(\gamma t\gamma^{-1}s,ts',x)$ equals its value at $(s,s',t^{-1}x)$; integration over the common $t$ is identical. With $a_1=s^{-1}\gamma x$, $a_2=s'^{-1}x$, one has $\mathcal N(a_1a_2^{-1})\le\mathcal N(a_1)\mathcal N(a_2)$. Therefore
$$
 \mathcal N(a_1)^{-e}\mathcal N(a_2)^{-e}
 \le \mathcal N(s^{-1}\gamma s')^{-b}\mathcal N(s'^{-1}x)^{-(e-b)}.
$$
Integrating first in $x$ gives the bound $c_N^{-1}C_v C_{v'} I_{e-b}Q_{\gamma,b}$ in (1). Rescaling $d\mu_R$ by a positive scalar divides both $Q_{\gamma,b}$ and the left side of (1) by that scalar. Thus the argument applies directly at the input root normalization. Unipotent translations to the monomial representative preserve the coefficient norms and transport the root measure by conjugation, as in its definition. [Two-sided Weil identity and coefficient kernel][kernel] · [Native integration over the cell][cell]

## Exact compact-dimension factor after unfolding

For nonzero starting coefficients let $L,L'$ be the normalized period maps and $d_\sigma$ the formal degree for the specified $dg$. Write $\Phi(y)=a_1 L(\sigma(y)w_0)$ and $\Phi'(y)=a_2 L'(\sigma(y)w_0)$, and $d=\dim W,\ d'=\dim W'$. The one-sided identities $d_\sigma\|L(\sigma(\cdot)w_0)\|_2^2=\|w_0\|^2$ and the two input masses $c_Nd,\ c_Nd'$ imply
$$
             \frac{|a_1a_2|}{c_N}
             =\frac{d_\sigma\sqrt{dd'}}{\|w_0\|^2}.                 \tag{4}
$$
Take compact-finite $v,v'$ and unit $\xi,\xi'$ so $L(v)^*\xi=L'(v')^*\xi'=1$, scaling $v,v'$ as necessary. Such compact-finite witnesses exist by smooth density and nonvanishing of the continuous periods. With the conventions in the expansion above, the single coefficient integral is
$$
 \mathcal O_\gamma=\int \langle v,\sigma(s^{-1}\gamma s')v'\rangle\,
          \tau(s)\xi\, (\tau'(s')\xi')^*\,d\nu(s,s').
$$
Its integral is absolutely convergent by the decay estimate for the two compact-finite witnesses and the bound on $Q_{\gamma,b}$. The integrations already justified above can now be performed with their phases. Integrating first on $S,S'$ gives the two normalized periods. Integrating first on $G_{\mathbb R}$ gives $\|w_0\|^2/d_\sigma$ times the indicated single matrix coefficient by discrete-series Schur orthogonality. Combining this with (4) gives exactly
$$
               \frac{\|J\|_{\rm HS}^2}{d}=d'\,\|\mathcal O_\gamma\|_{\rm HS}^2 .         \tag{5}
$$
This cancels both the formal degree and the initial normalization, also on all zero-penultimate cells. The coefficient witnessing the periods is scaled as specified; changing its normalization inside an external bound would change the right side. [Single coefficient and root-compatible identity][schur] · [Rank-one and quotient normalizations](SPECTRAL_BESSEL_REALIZATION.md)

## What the zero minor means for the squared estimate

For a relevant block point with block sizes $s_1,\ldots,s_j$, put $l_i=\sum_{a\le i}s_a$, $l_0=0$. The support condition $d_{n-1}=0$ says exactly $s_j\ge2$, and then $\mathcal G=d_n^2>0$. Such real pairing matrices are possible. For example, assign the two frames their prescribed individual Gram matrices $\operatorname{diag}(0,\ldots,0,-T)$ and $\operatorname{diag}(0,\ldots,0,-T')$, and pair them by a nonzero scalar times the reverse permutation, with the source's terminal column signs if needed. For $n\ge2$, permuting the basis gives $n$ two-dimensional blocks, each of determinant $-|t|^2$, hence signature $(n,n)$. Embed the resulting space in $U(k+r,r+1)$, and apply Witt extension separately to the two frames. This example asserts real representability only.

There is also a precise weight conversion on every such orbit. For the native point weight $p$, the unitary wave-grid formula gives each completed block $(t_i,s_i)$ a factor $|t_i|^{2s_i(k+2(n-l_i)+s_i-2)}$. Since $d_{l_i}/d_{l_{i-1}}=|t_i|^{s_i}$, telescoping yields
$$
            \frac p{\mathcal G^k}=
            d_n^{2(s_j-2)}
            \prod_{i<j}d_{l_i}^{2(s_i+s_{i+1})}.                 \tag{6}
$$
In particular a terminal block of size two has no remaining terminal-minor multiplier. The reciprocal of (6) is bounded by the product over block ends of $\max(d_l,d_l^{-1})^{2n}$, which fits the original loss. With $d_{\rm tar}=\dim W,\ \eta=(e\pi/(g^m Tkv))^k,\ t'_\tau=T_{{\rm crit},\tau}(u')/T'$, the requested ordinary bound is $\eta\mathcal G^k\|J\|_{\rm HS}^2/d_{\rm tar}\le L_\tau(t'_\tau)^{-k}$. Equivalently, (5) asks for $\eta\mathcal G^k d'\|\mathcal O_\gamma\|_{\rm HS}^2\le L_\tau(t'_\tau)^{-k}$ for this detecting coefficient. Formula (1) proves finiteness of the left side and gives an explicit integral majorant. Its constants $C_v,C_{v'}$ and $Q_{\gamma,b}$ have no uniform bound at the requested scale in this argument. The reconstruction's standardized point-energy theorem supplies a comparison to a separate squared section integral, at its stated height allowance and for its own matrix-coefficient normalization. Transferring that numerical inequality to this one still requires the section mass and its constants. [Wave-grid definition and point weight][weights] · [Standardized energy and transport][wave]

[targets]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Formalism/SharpRestriction/CuspSpanNormBounds/CongruenceAtSplitFrobeniusHolds.lean#L434-L487
[native]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Formalism/SharpRestriction/CuspSpanNormBounds/NormalizedLocalScale.lean#L127-L166
[signs]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Formalism/SharpRestriction/CuspSpanNormBounds/FrobeniusCoefficientMemLp/FramesPt.lean#L165-L174
[section]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Formalism/HermitianCurvature/FiniteOrderIntersectionInSmooth.lean#L36-L51
[section2]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Formalism/LocalToGlobal/SiegelLatticeTheory/FlagStabilizerTensors/RootLatticeThresholds/CompactCellConvergence/EtEquiv.lean#L15-L63
[old]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Formalism/PeriodIntegrals/UnitaryGroupMassFormula/PolynomialProperness/PolyProper5OfSteps.lean#L11-L55
[kernel]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AbelianVarietyTheory/Proofs/FlagMeasures/AmplifierOfHypotheses.lean#L53-L78
[cell]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Formalism/LocalToGlobal/SiegelLatticeTheory/FlagStabilizerTensors/RootLatticeThresholds/CompactCellConvergence/CellConvergence.lean#L40-L137
[weights]: https://github.com/rh-lean-roadmap/rh-lean-roadmap/blob/dc5594a62bb2b94139788df817db693cd939a046/docs/src/book/main.tex#L17123-L17136
[wave]: https://github.com/rh-lean-roadmap/rh-lean-roadmap/blob/dc5594a62bb2b94139788df817db693cd939a046/docs/src/book/main.tex#L17602-L17637

[schur]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AbelianVarietyTheory/Definitions/SemilocalFrames/OnePlaceKF.lean#L12-L57
