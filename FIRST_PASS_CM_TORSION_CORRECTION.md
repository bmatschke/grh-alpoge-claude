# The elliptic weight-two correction at nonzero torsion

Let $d>4$ be a prime, $w=i\sqrt d$, and let the period lattice $\Lambda$ be stable under $w$. Choose $\Omega^{12}=\Delta_\Lambda$. For a nonzero point $P\in\mathbb C/\Lambda$ of order prime to $\ell$, put
$$
 p(P)=\frac{\wp_\Lambda(P)}{\Omega^2},\qquad
 H(P)=\frac{s_2(\Lambda)+\wp_\Lambda(P)}{\Omega^2}.
$$
Here $s_2$ is the complex-linear coefficient in the quasiperiod $\eta(t)=s_2t+(\pi/\operatorname{area}\Lambda)\bar t$. With $v_\ell(\ell)=1$, the bound at every embedding is
$$
 v_\ell(H(P))\ \ge\
 \begin{cases}
 -1,&\ell=2,\ d\equiv3\pmod4,\\
 -2,&\ell=2,\ d\equiv1\pmod4,\\
 -\tfrac12,&\ell=d,\\
 0,&\ell\notin\{2,d\}.
 \end{cases}
$$
For a built host $d\equiv3\bmod4$. The construction uses a nonzero marked point killed by $\ell+1$ on a level divisible by $\ell+1$. If $\Lambda=c_\tau(\mathbb Z+\tau\mathbb Z)$, take $P=c_\tau\,\operatorname{tors}_N(\tau,x)$ for its actual level mark $x$, and put $\omega=\Omega c_\tau/(2\pi i)$. Homogeneity gives the precise correction
$$
 H(P)=\frac{G_2^*(\tau)/(2\pi i)^2+\operatorname{wp}_N(x,\tau)}{\omega^2}.
$$
Thus no independent choice of elliptic differential or extra torsion period enters. [Mark and its order][mark] · [Conversion of both summands][tau] · [Application to this correction][app]

**Torsion coordinates.** Fix an embedding into $\overline{\mathbb Q}_\ell$ for the algebraic quantities. For every nonzero torsion point $T$ of order prime to $\ell$,
$$
 12p(T)\quad\text{and}\quad p(T)-p(P)
$$
are integral there. To see both assertions including in residue characteristics two and three, consider the normalized short equation
$$
 y^2=x^3-\frac{g_2(\Lambda)}{4\Omega^4}x-\frac{g_3(\Lambda)}{4\Omega^6}.
$$
Its discriminant is $1$ and its $x$-coordinate at $T$ is $p(T)$. The coefficients are algebraic since $j=1728g_2^3/\Delta_\Lambda$ is a CM singular modulus and the two normalized invariants satisfy the discriminant identity. The [integrality of the actual CM invariant](FIRST_PASS_CM_MODULAR_VALUES.md) gives good reduction after a finite local extension. In a good integral Weierstrass equation write $x=u^2x'+r$. Both discriminants are units, hence $u$ is a unit. The change-of-variables formula gives $12r=u^2 b_2'$ since $b_2=0$ in the displayed short equation. Every nonzero prime-to-$\ell$ torsion point reduces away from the origin, so its $x'$-coordinate is integral. This proves both assertions, as the shift cancels in a difference. [Integral CM $j$][j] · [Pinned torsion estimates][tors] · [Silverman, *The Arithmetic of Elliptic Curves*, III §1 and VII, Propositions 3.1 and 5.5](https://www.math.ens.psl.eu/~obenoist/refs/Silverman.pdf)

**Isogeny identity.** Let $\alpha\ne0$ preserve $\Lambda$ and have degree $n=\alpha\bar\alpha$ prime to $\ell$. Then
$$
 A_\alpha=(\alpha^2-n)H(P)-(\alpha^2-1)p(P)
      =\sum_{0\ne T\in\ker\alpha}\bigl(p(T)-p(P)\bigr)
$$
is integral. Indeed the distribution formula for $\wp$ is
$$
 \alpha^2\wp(\alpha z)=\wp(z)+
 \sum_{0\ne T\in\ker\alpha}\bigl(\wp(z+T)-\wp(T)\bigr).
$$
The poles and their principal parts on the two sides agree, and comparison at $z=0$ fixes the additive constant. Integrating by $\zeta'=-\wp$ and translating by a period $t$ gives $\alpha\eta(\alpha t)-n\eta(t)=t\sum_{T\ne0}\wp(T)$. The conjugate-linear terms cancel since $\alpha\bar\alpha=n$. The kernel has $n-1$ nonzero points, giving the asserted identity, and every such $T$ is prime to $\ell$. The same identity over $\mathbb C$ with $\alpha=w$ also proves algebraicity of $H(P)$, since all torsion coordinates are algebraic and $w^2-d=-2d\ne0$. [Isogeny and quasiperiod formulas][isog] · [Subtraction of torsion coordinates][diff]

**The prime factors.** Write $p=p(P)$. When $\ell\ne d$, the multiplier $\alpha=w$ gives
$$
 -2d\,H(P)+(d+1)p\ \text{ integral}.
$$
For $\ell\nmid 6d$, both $12$ and $2d$ are units, so $H(P)$ is integral. For $\ell=2$, $4p$ is integral. If $d\equiv3\bmod4$, then $4\mid d+1$, giving integrality of $2H(P)$. If $d\equiv1\bmod4$, then $2\mid d+1$, giving integrality of $4H(P)$. For $\ell=3$ and $d\equiv2\bmod3$, use $3\mid d+1$ and integrality of $3p$. [The multiplier $w$ at these primes][ordinary]

For $\ell=3$ and $d\equiv1\bmod3$, take $\alpha_\pm=1\pm w$. Both have norm $d+1$, a $3$-adic unit. Put $B_\pm=\alpha_\pm^2-1$. Then $B_-A_{\alpha_+}-B_+A_{\alpha_-}=4dw\,H(P)$ because the $p$-terms cancel and $w^2=-d$. The multiplier $4dw$ is a unit at three. Finally take $\ell=d$ and $\alpha=1+w$, of unit norm $1+d$. Here $12$ is a unit, so $p$ is integral. The coefficient of $H(P)$ in $A_\alpha$ is $2w(1+w)$ and has valuation $1/2$ since $w^2=-d$. This gives the last exceptional loss and proves the bound. [Cancellation at three][three] · [Half-valuation at $d$][ram]

[mark]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AbelianVarietyTheory/Proofs/DivisorProofs/CMLatticeDividedPowerJetIntegralityOfHyp.lean#L154-L162
[tau]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AbelianVarietyTheory/Proofs/DivisorProofs/EisensteinWeierstrassValuesLatticeTau.lean#L24-L38
[app]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AbelianVarietyTheory/Proofs/DivisorProofs/ImportsRestLast.lean#L23-L38
[j]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AbelianVarietyTheory/Proofs/DivisorProofs/IsIntegralJInvariantOfComplexMultiplication.lean#L40-L69
[tors]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AbelianVarietyTheory/Proofs/DivisorProofs/IsIntegralWeierstrassPTorsionNonrealMultiplier.lean#L53-L70
[isog]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Formalism/LocalToGlobal/TorsionIntegrality/EisensteinTranslationProducts/AnalyticIdentityTheorems/QuasiPeriodConstIsogeny.lean#L89-L147
[diff]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AbelianVarietyTheory/Proofs/DivisorProofs/IsogenyFormulaWeierstrassPIntegral.lean#L40-L72
[ordinary]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AbelianVarietyTheory/Proofs/DivisorProofs/ValuationBoundMultiplierSqrtNegD.lean#L52-L118
[three]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AbelianVarietyTheory/Proofs/DivisorProofs/ValuationBoundThreeInert.lean#L23-L58
[ram]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AbelianVarietyTheory/Proofs/DivisorProofs/AlgebraicValuationBoundAtRamifiedPrime.lean#L40-L64
