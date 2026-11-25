# A uniform Fourier-coefficient bound at every cusp

Let $F=E^+$ be the real subfield of the first-pass CM host, $f=[F:\mathbb Q]\ge2$, and $s\ge1$. Fix a rational prime $\ell$ and an embedding $\lambda:\overline{\mathbb Q}\hookrightarrow\mathbb C_\ell$. Write $v_\lambda(\ell)=1$, $\delta=v_\ell(|\operatorname{disc}F|)$, and $|\kappa|=\sum_{\sigma:F\to\mathbb R}\kappa_\sigma$. In this section a coefficient has loss at most $r$ when it is algebraic and $v_\lambda$ of that coefficient is at least $-r$.

Consider an $O_F$-lattice $N O_F^2\subset L\subset O_F^2$. Suppose $t O_F^2\subset L$, where $t=M\ell^b$ and $\ell\nmid M$. Let $\rho_0$ bound the loss of all real conjugates of both coordinates of vectors of $L$, and also of $N$. This number may be negative. Choose $e,\rho\ge0$ with
$$
 e\ge\max_{C}\{-v_\ell(2^{-f}\zeta_C(1-2s))\},\qquad
 \rho\ge b+\delta/f+\rho_0.
$$
The partial zeta values here belong to $\mathbb Q$. Pick a nonzero row $y\in(\mathbb Z/N)^2$ killed by an integer prime to $\ell$. For every $\alpha\in\mathrm{GL}_2(\mathbb Z/N)$, the corrected Hilbert Eisenstein derivative attached to the transformed lattice and torsion row $(L_\alpha,y\alpha)$ has a convergent expansion in $q_N=\exp(2\pi i\tau/N)$. Every coefficient has loss at most
$$
 B=e+s\delta+2sbf+|\kappa|\rho. \qquad (1)
$$
The derivative is the source's `hfun` of weight $2sf+2|\kappa|$. Its correction is $W_y=(G_2+\wp((y_0\tau+y_1)/N))/(2\pi i)^2$. The full-level slash action sends index $\alpha$ to $\alpha\bar\gamma$ for $\gamma\in\mathrm{SL}_2(\mathbb Z)$, so the assertion applies at every cusp with the same $B$. The proof uses the Hilbert Eisenstein Fourier expansion in weight $2s$. At $s=1$ the [weight-two continuation](FIRST_PASS_CM_WEIGHT_TWO.md) supplies the exact constant and positive-frequency terms. [Normalized derivative][definition] · [Fourier and slash conventions][qdef] · [Hilbert Fourier expansion including weight two][weighttwo] · [Full family][all]

## Reduction to two fractional ideals

Lift $\alpha$ to an integral matrix $A$. The transformed lattice is
$$
 L_\alpha=LA+N O_F^2.
$$
It has level $N$ and this description is independent of the lift. An integral lift $A'$ of $\alpha^{-1}$ satisfies $A'A=1+NH$ with $H$ integral. Multiply this identity on the left by $(0,t)$ to obtain $(0,t)\in L_\alpha$. Each conjugate of a first coordinate of $L_\alpha$ is a sum of integral multiples of conjugate coordinates of $L$ and a multiple of $N$ by an algebraic integer. Thus the bound $\rho_0$ holds at every $\alpha$. The identity index gives the original lattice. [Level and inverse lifts][twist] · [Identity index][identity]

The first-coordinate projection has image an invertible fractional ideal $\mathfrak b$. Its kernel in the second coordinate is a lattice $\mathfrak a^\vee=\mathfrak D_F^{-1}\mathfrak a^{-1}$, where $\mathfrak D_F$ is the different. The projection splits since $\mathfrak b$ is projective. The second-coordinate component of a section is multiplication by some $x\in F$, giving
$$
 L_\alpha=\{(u,v):u\in\mathfrak b,\ v-ux\in\mathfrak a^\vee\}.
$$
In particular $t\mathfrak a\subset\mathfrak D_F^{-1}$ and all real conjugates of members of $\mathfrak b$ have loss at most $\rho_0$. The Galois hypothesis on $F/\mathbb Q$ gives $\mathfrak D_F^f=(|\operatorname{disc}F|)$. Hence all conjugates of elements of its inverse have loss at most $\delta/f$. Multiplication and addition in the fractional ideal product now give, for $\xi\in\mathfrak a\mathfrak b$ and each $\sigma$,
$$
 -v_\lambda(\sigma\xi)\le b+\delta/f+\rho_0\le\rho.
$$
This is where a local discriminant cost enters the derivatives. [Splitting][split] · [Inverse different][different] · [Product-ideal estimate][ideal]

## The Fourier coefficients

Use the normalized Hilbert coefficients $a_\xi$ for $\mathfrak a,\mathfrak b$. The constant term is $2^{-f}\zeta_{[\mathfrak a]^{-1}}(1-2s)$. For $\xi\ne0$ each nonzero term comes from factorizations $u v=\xi$ with $u\in\mathfrak a$, $v\in\mathfrak b$, up to opposite unit scalings, and with $\xi$ totally positive. Its summands are the integer powers $N((u)\mathfrak a^{-1})^{2s-1}$ of positive integer ideal norms. Thus every coefficient has loss at most $e$. For a multi-index $\mu$ the coefficient after diagonal restriction, translation, and differentiation is
$$
 E_{\mu,n}=\sum_{N\operatorname{Tr}(\xi)=n} a_\xi
  \exp(2\pi i\operatorname{Tr}(\xi x))
  \prod_\sigma (\sigma\xi)^{\mu_\sigma}.
$$
Only finitely many nonzero terms occur for each $n$. For $\xi\ne0$ in the support, positivity bounds every real conjugate by $n/N$, and $\xi$ lies in a fixed fractional ideal. Also $N\in\mathfrak a^\vee$ and $\mathfrak b\subset O_F$, so $N\operatorname{Tr}(\xi)$ is integral. The exponential is a root of unity and the nonarchimedean triangle inequality gives loss at most $e+|\mu|\rho$. [Class coefficients][classcoef] · [Trace fibres][tracefib] · [Diagonal restriction][diagonal]

The row $y'=y\alpha$ is nonzero and is killed by the same integer $M_0$ prime to $\ell$. Every positive Fourier coefficient of $W_{y'}$ is a sum of integers times roots of unity. Its constant term vanishes unless $y'_0=0$, when it is $\zeta/(1-\zeta)^2$ for a nontrivial $M_0$-th root $\zeta$. The identity $M_0/(1-\zeta)=-\sum_{h=0}^{M_0-1}h\zeta^h$ proves integrality at $\ell$, also when $\ell\mid N$. Therefore every coefficient of its series $C(q_N)$ has loss at most zero. [Torsion Fourier coefficients][torsion] · [Geometric sum][torsum]

In the normalized derivative the summand indexed by $\mu\le\kappa$ is an **integer** times
$$
  \left(\sqrt{|\operatorname{disc}F|}\,N\mathfrak a\right)^{2s}
  C(q_N)^{|\kappa|-|\mu|}\sum_{n\ge0}E_{\mu,n}q_N^n.
$$
Indeed each coordinate's multiplier is, up to sign, $\binom{\kappa_\sigma}{\mu_\sigma}(2s+\mu_\sigma)^{\overline{\kappa_\sigma-\mu_\sigma}}$, with the rising factorial. The common prefactor has loss at most $s\delta+2sbf$. To see this, $t\mathfrak a\mathfrak D_F$ is integral, so its norm gives $v_\ell(N\mathfrak a)\ge-bf-\delta$. The prefactor equals $|\operatorname{disc}F|^s(N\mathfrak a)^{2s}$. Taking coefficients in the product uses a finite convolution. Summing over $\mu$ gives (1). Neither the order of the finite level group nor the number of frequencies in a trace fibre enters its exponent. [Exact integral multipliers and series][series] · [Prefactor and convolution][prefactor]

## Specialization to varying order classes

For the original conductor $\mathfrak f$, put $a=a_0(\mathfrak f,\ell)$, the largest local conductor exponent above $\ell$, and $c=c_{\rm vp}(\mathfrak f,\ell)$. Let $D_K$ be the absolute discriminant of the imaginary quadratic field selected by the host, and put $g=v_\ell(D_K)$. The order lattice is $\Lambda=E\cap u\widehat{O_{\mathfrak f\prod Q}}$, with $u_v=1$ above $\ell$ and $Q$ prime to $\ell$. Using the standard quadratic integer generator $\theta$, the source constructs $L$ by taking pairs $(x_0,x_1)$ with $x_0\theta+x_1\in M_1 D_K\Lambda$ for an integer $M_1$ prime to $\ell$. This prime-to-$\ell$ scaling clears the denominators of $u$. If $x_0\theta+x_1=D_K z$ with $z$ integral, subtracting its conjugate shows $x_0^2/D_K$ is integral. The other coordinate has the same property by eliminating $x_0$ with $\theta,\bar\theta$. This gives $\rho_0=-g/2$. At $\ell$, the conductor is cleared by $\ell^a$. Clearing the other primes and including $M_0>1$ prime to $\ell$ as a factor produces a width $N=M_2\ell^{g+a}$, with $M_2$ prime to $\ell$ and $N O_F^2\subset L\subset O_F^2$. Thus $b=g+a$ is independent of $Q$ and $u$, even though the integer width varies. [Order-lattice construction][order]

For the original host choose the source's $e=c_{E,\ell}(z)=\max_C\max(0,-v_\ell(2^{-f}z_C))$, $z_C=\zeta_C(1-2s)$, and $\rho=2c+2a+g/2$. The inequality $\delta/f\le c$ verifies the lower bound on $\rho$. This gives the coefficient loss
$$
 c_{E,\ell}(z)+s\delta+2sf(g+a)+|\kappa|(2c+2a+g/2)
$$
for every relevant $Q,u$, every component $\alpha$, and every Fourier index. The [diagonal comparison on this lattice](FIRST_PASS_CM_DIAGONAL.md) carries these coefficient estimates back to the original jet. The smaller choice $\rho=g/2+a+\delta/f$ also suffices for these Fourier coefficients. The displayed choice is the one used when bounding the separate nonholomorphic elliptic correction at the CM point. [Substitution for the original lattice][sub]

[definition]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AbelianVarietyTheory/Definitions/Divisors/HasLevelStd.lean#L59-L75
[qdef]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AbelianVarietyTheory/Definitions/Divisors/HasQIff.lean#L9-L28
[weighttwo]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AbelianVarietyTheory/Proofs/DivisorProofs/HilbertEisensteinExpansionOfLipschitzHeckeZeta.lean#L61-L83
[all]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AbelianVarietyTheory/Proofs/DivisorProofs/ImportsSideTer.lean#L20-L36
[twist]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AbelianVarietyTheory/Proofs/DivisorProofs/TwistedHilbertLatticeContainsAndCoordinateSize.lean#L27-L93
[identity]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AbelianVarietyTheory/Proofs/DivisorProofs/MemMulMatSmulOneIff.lean#L28-L53
[split]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AbelianVarietyTheory/Proofs/DivisorProofs/ExistsSplitOfHilbertLatticeHasLevel.lean#L23-L95
[different]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AbelianVarietyTheory/Proofs/DivisorProofs/AlgebraicValuationAtLeastInverseDifferentElement.lean#L39-L58
[ideal]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AbelianVarietyTheory/Proofs/DivisorProofs/HilbertEisensteinCoefficientValuationBound.lean#L30-L80
[classcoef]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AbelianVarietyTheory/Proofs/DivisorProofs/ExistsHilbertEisensteinFourierCoeffFamily.lean#L18-L27
[tracefib]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AbelianVarietyTheory/Proofs/DivisorProofs/HilbertEisensteinCoeffSupportTraceFinite.lean#L120-L166
[diagonal]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AbelianVarietyTheory/Proofs/DivisorProofs/HasQExpansionOfLevelHilbertEisensteinQuasiPeriod.lean#L203-L226
[torsion]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AbelianVarietyTheory/Definitions/Divisors/ZetaActRefl.lean#L36-L69
[torsum]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AbelianVarietyTheory/Proofs/DivisorProofs/IsIntegralWeierstrassTorsionQCoefficients.lean#L20-L39
[series]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AbelianVarietyTheory/Definitions/Divisors/HasLevelStd.lean#L64-L85
[prefactor]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AbelianVarietyTheory/Proofs/DivisorProofs/HilbertEisensteinCoefficientValuationBound.lean#L309-L361
[order]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AbelianVarietyTheory/Proofs/DivisorProofs/MemPassScaled.lean#L42-L115
[sub]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AbelianVarietyTheory/Proofs/DivisorProofs/CMLatticeDividedPowerJetIntegralityOfHyp.lean#L194-L219
