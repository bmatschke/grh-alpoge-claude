# The flat determinant test directly on the chosen cutoff model

For the nonterminal row let $r,s$ be its two signature ranks, $n=r+s$, $N=\lfloor B(u',g)\rfloor$, and $S_N$ the union of the exceptional primes $\mathcal B_{\mathscr T}$ with all primes at most $N$. Put $u_E=\log\operatorname{rd}(E)$ and
$$
 c_p=\begin{cases}2 & p=2,\\ 1/(p-1)&p>2,\end{cases}
 \qquad C(S)=\sum_{p\in S} c_p\log p,qquad
 h_0=\frac{r-s}{2}\log\Omega .
$$
Use the actual root model $M(N,Z)$, the map identifying its component with the marked PEL component, and the global and local comparisons specified below. For the flat class $Y_0=p_{\tau,1}Q_1$ of the mixed intersection calculation, $D(Q_1)=1$. The degree-weighted scalar $I(Y_0)=P_N(Y_0)/V$ then satisfies
$$
 h_0-sC(S_N)\ \le I(Y_0)\le\ h_0+r\bigl(C(S_N)+u_E\bigr).            \tag{1}
$$
In particular $|I(Y_0)|\ll n\lambda_N$ at the fitted cutoff, with $\lambda_N=\log(N\operatorname{rd}(E))+|L_E|$. The argument applies the flat-line construction at $N$ itself. It requires the selected model's root and flag identifications, its local Hodge–Tate lattice comparison, convergence of its smoothed intersections, and the corrected CM flat-degree formula. It eliminates the separate comparison of two cutoff models from this scalar test. The archimedean and integral identifications are essential even if the generic determinant and its volume are known. [Mixed class to which the estimate applies](PERIOD_ROOT_FROBENIUS_CORRECTION.md) · [Original source proof, stated at cutoff two][two]

## Which flat degree enters

On the marked component take the flat frame function of the determinant of the rank-$r$ block divided by the determinant of the conjugate rank-$s$ block. In a frame with Hodge Gram matrices $G_1,G_2$ its constant infinite logarithmic norm is $\log|\phi|+\tfrac12\log(\det G_1/\det G_2)$. Let its finite logarithmic norm on saturated record frames be $t_{p,\kappa}$, with $\kappa$ an embedding of the coefficient field into $\mathbf C_p$. These norms keep the same values on all compatible frames. The native flat-degree theorem is stated with a different correction in its finite norms. Its degree in those conventions is
$$
 h_{\rm corr}=\frac{r-s}{2}\log\Omega+s(\log d_K-u_E),
$$
where $d_K$ is the positive host discriminant parameter. To obtain the actual finite frame reading, add $s(\log|\mathfrak D_{E/\mathbf Q}|_{p,\kappa}-\log|d_K|_p)$ to the corrected local logarithmic norm. The local norm of the different is the absolute value of a local generator. Averaging the sum of the different terms over embeddings gives $-u_E$ by the norm-discriminant identity. Averaging the sum of $\log|d_K|_p$ gives $-\log d_K$ by the product formula. The normalized arithmetic degree uses the negative sum of these logarithmic norms. Thus the uncorrected record determinant has degree exactly $h_0$. This also fixes the sign of the determinant class used below. The host period relation is $\log\Omega=\gamma+\log(2\pi)-u_E-L_E$. [Two definitions of the finite norm][norms] · [Exact cancellation by the different and the product formula][cancel] · [Period and degree of the section on the marked component][record]

## The determinant of the two lattices

On a supplied root origin for $M(N,Z)$ the cumulative flag determinants give, by multiplication of successive quotients, the determinant of the first block divided by that of the conjugate block. At a prime outside $S_N$ the model and record lattices agree in both eigenspaces. On a test trait at $p\in S_N$, denote the model lattices by $L_+,L_-$ and the saturated record eigenspaces by $R_+,R_-$. In the normalization $v_p(p)=1$ the original root-model comparison is
$$
 R_+\subset L_+,\quad \kappa_p\delta_\tau L_+\subset R_+,
 \qquad
 R_-\subset L_-,\quad \kappa_pL_-\subset R_-,
$$
with $v_p(\kappa_p)=c_p$. For the left projection choose a generator of the local different, or an element of the global different of the same local exponent. Since the host is Galois, $v_p(\delta_\tau)=v_p(|\operatorname{disc}E|)/[E:\mathbf Q]=\delta_p$, for every embedding. The right block uses the intersection lattice and requires no different denominator. The model scalar at $2$ here uses $c_2=2$, as in the source's integral root model. The sharper comparison between two frames on an algebraically closed test does not by itself change this model scalar. [Root-model lattice inclusions][sand] · [Local coefficient inequalities][local]

Let $k_+$ and $k_-$ be the normalized valuations of the determinants expressing record bases in the respective model bases. Passing to top exterior powers, or summing elementary divisors of free lattices over the trait, gives $0\le k_+\le r(c_p+\delta_p)$ and $0\le k_-\le s c_p$. The coordinate of the flat section in the model bases is the ratio of the coefficients of its two wedges. Hence its model logarithmic norm minus its record logarithmic norm is $(-k_++k_-)\log p$. This is the signed inequality in the original proof before taking its absolute value. After negating to form the arithmetic degree, the local discrepancy per embedding lies between $-s c_p\log p$ and $r(c_p+\delta_p)\log p$. The model-to-record comparison can measure the order via a transverse trait or a finite extension. The factor $k/m$ in the local uniformizer comparison divides out that extension, so each local interval is in the normalization $v_p(p)=1$. Averaging over embeddings preserves these intervals. The discrepancy vanishes off $S_N$, and $\sum_{p\in S_N}\delta_p\log p=u_E$. This gives exactly the interval in (1) for the model flat height on each component. [Order on the model and difference of logarithmic norms][local] · [Averaging the local degree differences][places]

## Why this calculation applies at the requested cutoff

The exported root-flat theorem uses the exceptional set at cutoff $2$. Its proof proceeds through a more general construction on a Hodge model with a specified finite set $S$. Three facts allow the construction to be used with the enlarged set $S_N$ without changing the model.

1. Its component and period comparison works on a supplied origin for arbitrary $S$. The proof constructs a flat generic generator and identifies both determinant wedges with the specified record component. It invokes its hypothesis that $S$ equals the primes dividing $2\operatorname{disc}(E)M'$ only to infer $2\in S$ and $p\mid\operatorname{disc}(E)\Rightarrow p\in S$. In the comparison away from $S$ it uses $p\notin S$ and consequently $p\nmid\operatorname{disc}(E)$. All these implications hold for $S_N$. The Hodge model itself requires its elements to be primes. [Uses of the exceptional-set hypothesis][uses] · [Hypotheses of the determinant construction on an arbitrary $S$][core]
2. At every cutoff and component the good root origin supplies local freeness of the marked Hodge–Tate modules at its chosen primes. This is exactly the hypothesis used to obtain the two inclusions on the determinant calculation above, including the new good primes up to $N$. The complement uses the unmodified de Rham lattices and the numerical fibre comparison for the actual model. Thus the local data are used on the specified $M(N,Z)$ at all primes. [Freeness at every cutoff][origin] · [Construction of the lattice comparison at primes in $S$][sandapply]
3. The multidegrees and the smooth metrics of successive quotients telescope on the model. Write $D_i(t)$ for the smoothed cumulative flag line and $x_i(t)$ for the root. In the model convention $x_i(t)D_i(t)=D_{i-1}(t)$, with $D_{-1}(t)=1$. Thus the product is the inverse of the last cumulative line. Its unregularized value on the interior is exactly the flat Hermitian determinant described above, by evaluation on the two wedges and the Hodge Gram determinants. The regularization theorem for these same metrics gives a residual log ratio whose integral against every degree-$d_{\rm fl}$ root monomial tends to zero. The identity on the interior alone would not suffice to remove a boundary contribution. [Evaluation and telescoping on the actual origin][telescope] · [Regularization of the determinant metric][metric]

For any homogeneous $Q$ of degree $d_{\rm fl}$, arithmetic multilinearity and change of metric identify $P_{N,Z}(p_{\tau,1}Q)$ with the flat height times the geometric integral of $Q$, up to the residual integral just described, which vanishes in the limit. The flat term follows by the projection formula for a constant-field Hermitian line. The finite extension degree and coefficient-field degree divide both intersections in the root model's normalization. Therefore $P_{N,Z}(p_{\tau,1}Q_1)=h_{N,Z,\tau}V_Z$ under the individual geometric comparison. Averaging the established interval for $h_{N,Z,\tau}$ gives (1) with arbitrary positive $V_Z$. The elementary estimate $C(S_N)\le4\log N+\log2$ follows from the source's sum for $\log p/(p-1)$ and the additional $\log2$ at $2$. It uses $\#\mathcal B_{\mathscr T}\le N$, as on the fitted row. This proves the required size of the flat test. [Flat-line projection formula with the actual smoothing][push] · [Prime sum at the fitted cutoff][two]

### Exact change if the prime-to-prime model transition is available

There is also an exact check across cutoffs. Write $K=\mathbf Q(\sqrt{-d_K})$. At a good prime $p$ the source starts its path with the *first* arithmetic Frobenius iterate. If $p$ splits in $K$, every iterate stays on the left, so the rank sum in the degree-one transition is $r/(p-1)$ and cancels. If $p$ is inert, the ranks at successive iterates are $s,r,s,r,\ldots$. Subtracting $r/(p-1)$ from their weighted sum gives $(s-r)p/(p^2-1)$. The transition formula subtracts this quantity times $\log p$ when the cutoff is increased. Consequently, if the degree-one transition identity is supplied,
$$
 h_{N,Z,\tau}=h_{2,Z,\tau}
  +(r-s)\sum_{\substack{2<p\le N,\ p\notin\mathcal B_{\mathscr T}\\p\ {\rm inert\ in}\ K}}
            \frac{p\log p}{p^2-1}.
$$
This increment is nonnegative and independent of $Z$ and $\tau$. The direct estimate (1) needs no transition identity. The Hodge calibration and the comparison on the class annihilated by the two first derivatives remain separate requirements, as does construction of compatible root origins from the original marked data. [Initial Frobenius iterate](https://github.com/rh-lean-roadmap/rh-lean-roadmap/blob/dc5594a62bb2b94139788df817db693cd939a046/docs/src/book/main.tex#L50189-L50202) · [Sign of the cutoff transition][two]

[two]: https://github.com/rh-lean-roadmap/rh-lean-roadmap/blob/dc5594a62bb2b94139788df817db693cd939a046/docs/src/book/main.tex#L50382-L50434
[norms]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AutomorphicSpectrum/Definitions/GlobalGeometry/IsConstMul.lean#L72-L84
[cancel]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AutomorphicSpectrum/Proofs/GeometryProofs/KroneckerCharacterPeriodFormula.lean#L45-L148
[record]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/WeilBound/CoreStatements/FlagImmersions/SpecMapFactorisation.lean#L76-L113
[sand]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/WeilBound/CoreStatements/FlagImmersions/FibSandwich.lean#L104-L124
[local]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/WeilBound/CoreStatements/FlagImmersions/LocalCmpOf.lean#L104-L168
[places]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/WeilBound/CoreStatements/FlagImmersions/LogIdealNonpos.lean#L99-L155
[uses]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/WeilBound/CoreStatements/FlagImmersions/RootFlatOnHodgeOf.lean#L30-L46
[core]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/WeilBound/CoreStatements/FlagImmersions/TauInInjective.lean#L26-L51
[origin]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AutomorphicSpectrum/Definitions/DivisibilityTowers/GoodOrigin.lean#L53-L57
[sandapply]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/WeilBound/CoreStatements/FlagImmersions/TauInInjective.lean#L139-L157
[telescope]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/WeilBound/CoreStatements/FlagImmersions/RootFlatOnHodgeOf.lean#L47-L71
[metric]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/WeilBound/CoreStatements/TorusUniformisation/ChowMahlerFamilies/RootOfRealisationTelescoping.lean#L233-L289
[push]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AutomorphicSpectrum/Proofs/GeometryProofs/RootFlatPushforwardGeoFun.lean#L41-L90
