# The weight-two endpoint of the Hilbert expansion

Let $F$ be totally real of degree $f\ge2$, let $D=|\operatorname{disc}F|$, and fix nonzero fractional ideals $\mathfrak a,\mathfrak b$. Write $\mathfrak a^\vee=\mathfrak D_F^{-1}\mathfrak a^{-1}$ for the trace dual and $\omega_{\mathfrak a}=\sqrt D\,N\mathfrak a$. The first-pass host has $f=2\,\mathrm{ord}\ge2$. For $z\in\mathbb H^f$ and $\Re\sigma>0$, form the sum over nonzero pairs $(a,b)\in\mathfrak a^\vee\oplus\mathfrak b$ modulo simultaneous multiplication by $O_F^\times$, with summand
$$
 P(a,b;z)^{-2}|P(a,b;z)|^{-2\sigma},\qquad
 P(a,b;z)=\prod_{v:F\hookrightarrow\mathbb R}2\pi i(a_v+b_v z_v).
$$
It converges absolutely there. Indeed $|a_v+b_v z_v|$ is comparable to $(a_v^2+b_v^2)^{1/2}$ for fixed $z_v$. The majorant is a constant times $|N_{F(i)/\mathbb Q}(a+ib)|^{-1-\Re\sigma}$. After clearing fixed denominators, its sum is bounded by the convergent ideal zeta series, since $O_F^\times$ has finite index in $O_{F(i)}^\times$. [Definitions and domain][w2-def] · [Absolute convergence][w2-abs]

## What happens to the zero frequency

Separate $b=0$, whose contribution is $A(\sigma)$, then apply Poisson summation on $\mathfrak a^\vee$ in the remaining terms. Put $y_v=\Im z_v$ and $k(\sigma)=((2\pi i)^{-2}(2\pi)^{-2\sigma})^f$. The zero dual frequency in the $b\ne0$ sum is
$$
 k(\sigma)\,\omega_{\mathfrak a}\,(N\mathfrak b)^{-1-2\sigma}
 \zeta_{[\mathfrak b]^{-1}}(1+2\sigma)\,c(\sigma)^f
 \prod_v y_v^{-1-2\sigma}.
$$
The ordinary ideal class is $[\mathfrak b]^{-1}$ because $b$ modulo units corresponds to the integral ideal $(b)\mathfrak b^{-1}$. The one-dimensional zero-frequency factor can be evaluated throughout $\Re\sigma>-1/2$. Its odd part integrates to zero, and the beta integral gives
$$
 c(\sigma)=\int_{\mathbb R}\frac{|t+i|^{-2\sigma}}{(t+i)^2}\,dt
 =\int_{\mathbb R}\frac{t^2-1}{(1+t^2)^{\sigma+2}}\,dt
 =-\sigma\sqrt\pi\,\frac{\Gamma(\sigma+1/2)}{\Gamma(\sigma+2)} .
$$
In particular $c'(0)=-\pi$. The partial zeta has at most a simple pole at $1$. The pinned argument obtains finite pole order from its functional equation, then uses $0\le\zeta_C(x)\le\zeta_F(x)$ on $x>1$ and the Dedekind zeta residue bound to improve the order to at most one. Consequently the zero frequency extends holomorphically and vanishes to order at least $f-1$ at $\sigma=0$. All of its spatial derivatives vanish there as well. The separate $b=0$ part is holomorphic on the same half-plane by its absolutely convergent one-variable ideal sum with exponent $2+2\Re\sigma>1$. [Poisson decomposition][w2-poisson] · [Zero frequency and removal of the pole][w2-zero] · [Simple-pole bound][w2-pole]

## Nonzero frequencies and the surviving constant

For $b\ne0$ and $\nu\in\mathfrak a\setminus\{0\}$ the nonzero Fourier term is a product of one-dimensional transforms of $(t+iy)^{-2}|t+iy|^{-2\sigma}$ with the phase $e^{2\pi i\nu_v b_v\Re z_v}$. Fix compact subsets of $\Re\sigma>-1/2$ and $\mathbb H^f$ and a real derivative order $j$. Fourier integration by parts, after scaling by $|b_v|\Im z_v$, gives a fixed $m$ such that for every integer $p\ge0$ the absolute value of the $j$th derivative is bounded by
$$
 C_p\prod_v\frac{(|b_v|+|b_v|^{-1})^m}{(1+|b_v\nu_v|)^p}.
$$
The strict half-plane bound makes the original one-variable kernel integrable at infinity, and differentiating in its real integration variable improves decay. Dirichlet's unit theorem allows representatives $b$ with the $|b_v|$ mutually comparable. Multiplying $b$ by a unit and $\nu$ by its inverse preserves the term. With these representatives take $p=mf+f+1$. Writing $B=\sum_v|b_v|$, $V=\sum_v|\nu_v|$, discreteness bounds each away from zero, and $\prod_v(1+|b_v\nu_v|)\gg BV$. The majorant is therefore $O(B^{-(f+1)}V^{-p})$, summable over both lattices of rank $f$. This gives local uniform convergence of every spatial derivative, and holomorphy in $\sigma$ of each such derivative. Together with the zero-frequency calculation it gives the continuation required for all iterated Wirtinger derivatives. [Fourier estimate][w2-bound] · [Summable exponents][w2-sum] · [Termwise continuation][w2-good]

At $\sigma=0$ the transform with Fourier kernel $e^{-2\pi i\nu t}$ equals $-4\pi^2|\nu|e^{-2\pi\nu y}$ when $\nu y>0$ and zero otherwise. Thus the nonconstant holomorphic terms are indexed by $\nu b$ totally positive. After multiplication by $\sqrt D/\omega_{\mathfrak a}^2$, each pair contributes
$$
 N((\nu)\mathfrak a^{-1})\exp\!\left(2\pi i\sum_v v(\nu b)z_v\right).
$$
The surviving constant comes from $b=0$. Replacing $a$ by the ideal $(a)\mathfrak D_F\mathfrak a$ gives
$$
 A(0)=(2\pi i)^{-2f}(D\,N\mathfrak a)^2
 \zeta_{[\mathfrak D_F\mathfrak a]}(2).
$$
The ordinary partial-zeta functional equation pairs this class with $[\mathfrak a]^{-1}$. With $\Gamma_{\mathbb R}(2)=\pi^{-1}$ and $\Gamma_{\mathbb R}(-1)=-2\pi$, it gives the exact normalized constant $\sqrt D\,A(0)/\omega_{\mathfrak a}^2=2^{-f}\zeta_{[\mathfrak a]^{-1}}(-1)$. This is the constant term used in the coefficient bound for $s=1$. The external analytic input at this step is Hecke's functional equation for ordinary class partial zeta functions, with the different in the product of the paired classes. Rationality of its value at $-1$ enters the subsequent arithmetic estimate. [Partial-zeta functional equation][w2-fe] · [Nonzero modes][w2-modes] · [Normalized constant][w2-const] · [Endpoint assembly][w2-close]

[w2-def]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AbelianVarietyTheory/BlockTheory/DivisorBase/OmegaFactorization.lean#L100-L134
[w2-abs]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AbelianVarietyTheory/Proofs/DivisorProofs/SummableHilbertEisensteinLatticeClassWeightTwo.lean#L16-L29
[w2-poisson]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AbelianVarietyTheory/Proofs/DivisorProofs/HeckeWeightTwoContinuationEqLatticeSeries.lean#L79-L116
[w2-zero]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AbelianVarietyTheory/Proofs/DivisorProofs/HeckeEisensteinZeroFrequencyPartIsSmoothHolomorphic.lean#L34-L76
[w2-pole]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AbelianVarietyTheory/Proofs/DivisorProofs/PartialZetaTotallyRealAtMostSimplePole.lean#L122-L169
[w2-bound]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AbelianVarietyTheory/Proofs/DivisorProofs/FTermIteratedFDerivBound.lean#L33-L53
[w2-sum]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AbelianVarietyTheory/Proofs/DivisorProofs/SummableHeckeBalancedLatticeDoubleSum.lean#L122-L160
[w2-good]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AbelianVarietyTheory/Proofs/DivisorProofs/HeckeEisensteinNonconstantFourierSumSmoothHolomorphic.lean#L18-L35
[w2-fe]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AbelianVarietyTheory/PublishedTheorems/Divisors₂/PartialZetaFunctionalEquation.lean#L11-L17
[w2-modes]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AbelianVarietyTheory/Proofs/DivisorProofs/HeckeEisensteinWeightTwoQExpansion.lean#L19-L73
[w2-const]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AbelianVarietyTheory/Proofs/DivisorProofs/HeckeWeightTwoConstantTermEqPartialZetaNegOne.lean#L95-L165
[w2-close]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AbelianVarietyTheory/Proofs/DivisorProofs/HeckeWeightTwoContinuationOfFunctionalEquation.lean#L23-L63
