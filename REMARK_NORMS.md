# The CM period that centers the prime count

Item 9 of Alpöge’s remarks groups three computations together. A CM elliptic period fixes the scale of a derivative, the Weyl dimension formula counts archimedean representation directions, and a Hermitian genus mass counts lattice classes with weights reciprocal to their automorphism orders. The first computation answers a question visible at the very end of the argument. Why does the centering term of a prime sum contain exactly $L'(1,\chi)/L(1,\chi)$? The *same* logarithmic derivative is the constant term, up to explicit elementary terms, in the average area of the CM period lattices. The equality, including its sign and its metric normalization, follows from the classical first Kronecker limit formula. [Alpöge, item 9](https://alpo.ge/remark.pdf#page=4) · [Prime-sum centering, CMP.8 and CMP.10](conditional_main_v42/conditional_main.tex#L152-L166)

## The area identity

Let $k$ be an imaginary quadratic field with fundamental discriminant $-d<-4$ and primitive quadratic character $\chi$. Write $h$ for its class number, $\gamma$ for Euler’s constant, and $\ell_\chi=L'(1,\chi)/L(1,\chi)$. Suppose $M\subset\mathbb C$ is a number field and the curve $Y^2=4X^3-g_2X-g_3$ over $M$ has geometric endomorphism ring $\mathcal O_k$. Set $\Delta=g_2^3-27g_3^2\ne0$. For each $\rho:M\hookrightarrow\mathbb C$, take the period lattice of the differential $dX/Y$ on the conjugate curve and let $A_\rho$ be its Euclidean area. Then

$$
\frac1{[M:\mathbb Q]}\sum_\rho \log\frac{A_\rho}{\pi}
=\gamma+\log\frac{2\pi}{\sqrt d}-\ell_\chi
-\frac{\log|N_{M/\mathbb Q}\Delta|}{6[M:\mathbb Q]}.
$$

The source chooses $\Delta=1$. The general version keeps track of the change of differential, which matters when comparing normalizations of a period theorem. [Normalized conjugate areas in the pinned proof](https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AbelianVarietyTheory/Proofs/FoundationProofs/MeanLogPeriodConjugatesEqChowlaSelberg.lean#L202-L213)

**Proof.** Represent each ideal class by a lattice homothetic to $\mathbb Z+\tau_c\mathbb Z$ and set $y_c=\operatorname{Im}\tau_c$. The Epstein zeta function in the normalization needed here is
$Z(\tau,s)=\sum_{(m,n)\ne(0,0)}y^s/|m+n\tau|^{2s}$. For $\operatorname{Re}s>1$, grouping ideals by class gives

$$
\zeta(s)L(s,\chi)=\zeta_k(s)=\tfrac12(2/\sqrt d)^s\sum_c Z(\tau_c,s).
$$

Indeed, for a fractional ideal $I$, a nonzero $\alpha\in I$ gives the integral ideal $(\alpha)I^{-1}$ of norm $|\alpha|^2/N(I)$ in the inverse class. Every such ideal occurs twice, since the units are $\{1,-1\}$. The covolume of $I$ is $N(I)\sqrt d/2$, which gives the indicated scale. Kronecker’s first limit formula gives residue $\pi$ and constant term $2\pi(\gamma-\log 2-\log(\sqrt y\,|\eta(\tau)|^2))$ for $Z(\tau,s)$. Divide the constant term of each side of the last display by its residue. On the left this gives $\gamma+\ell_\chi$. On the right it gives $\log(2/\sqrt d)+2\gamma-2\log 2-h^{-1}\sum_c\log(y_c|\eta(\tau_c)|^4)$. Hence

$$
\frac1h\sum_c\log(4\pi y_c|\eta(\tau_c)|^4)
=\gamma+\log(2\pi/\sqrt d)-\ell_\chi .
$$

This is the logarithmic form of the Chowla–Selberg calculation needed here. [Siegel, *Advanced Analytic Number Theory*, Ch. I, Theorem 1, printed p. 13](https://mathweb.tifr.res.in/Documents/Publications/Lectures/tifr23.pdf) · [Selberg and Chowla, *On Epstein’s Zeta-function*](https://doi.org/10.1515/crll.1967.227.86) · [Class-sum calculation in the pinned proof](https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AbelianVarietyTheory/Proofs/HomogeneousIdeals/DedekindZetaEqSumRealEisenstein.lean#L116-L155)

To pass to the actual conjugate lattices, write one as $\omega(\mathbb Z+\tau\mathbb Z)$. Its area is $|\omega|^2y$ and its Weierstrass discriminant is $(2\pi/\omega)^{12}\eta(\tau)^{24}$. Consequently
$\log(A_\rho/\pi)+\frac16\log|\rho(\Delta)|=\log(4\pi y|\eta(\tau)|^4)$. This expression is independent of homothety and basis. By the main theorem of complex multiplication, the Hilbert class polynomial is irreducible over $k$, hence over $\mathbb Q$, and its $h$ roots give exactly these ideal classes. Each embedding of $\mathbb Q(j)$ has $[M:\mathbb Q(j)]$ extensions to $M$. Thus the embedding average of the right side is exactly the class average already evaluated. Averaging the discriminant term gives the asserted norm correction. [Sutherland, Theorem 21.1 and Corollary 21.2](https://ocw.mit.edu/courses/18-783-elliptic-curves-fall-2025/mit18_783_f25_lec21.pdf) · [Lattice-area and discriminant normalizations](https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AbelianVarietyTheory/Proofs/HomogeneousIdeals/DedekindZetaEqSumRealEisenstein.lean#L190-L211)

## How the formula enters the arithmetic inequality

The higher-dimensional host has CM field $E\supseteq k$. Its integral period line contributes a correction of $-\log(\mathrm{rd}_E/\sqrt d)$ to the elliptic mean. Here $\mathrm{rd}_E=|\operatorname{disc}E|^{1/[E:\mathbb Q]}$. In the project’s host the relative different factors as $\mathfrak b\bar{\mathfrak b}$. The lattice index cancels the choice of a vector in the period line by the product formula. What remains is $-[E:\mathbb Q]^{-1}\log N_{E/\mathbb Q}\mathfrak D_{E/k}$, which equals this correction by discriminant transitivity. This argument applies to every allowed coefficient field and every period line labeled by an embedding of the chosen CM type. [Integral period-line calculation](continuation_v83/waterloo.md#the-arithmetic-period-calculation) · [Statement and proof for all the chosen lines](https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AbelianVarietyTheory/Proofs/DivisorProofs/MeanLogPeriodChowlaSelberg.lean#L55-L86)

With the source’s discriminant-one differential the arithmetic period is therefore $\log\Omega_E=\gamma+\log(2\pi/\mathrm{rd}_E)-\ell_\chi$. On substituting it, the centering term of CMP.8 becomes

$$
\mathcal M(a,w)=
 a\left(\log a-1-\frac1f\sum_{\rho\in\Phi}\log w(\rho)
          +\log(2\pi/\mathrm{rd}_E)-\log\Omega_E\right).
$$

One can see the same term before the final prime sum, in the norm of an individual lift. Let $c_\tau$ generate the integral line at $\tau$ over a field of definition, and write $\omega_{\rho,\tau}$ for the negative logarithm of its squared norm in the embedding $\rho$. The expression for this number is $\log(A_\rho/\pi)-2\log|\rho(c_\tau)|$. A generator has lattice index one, so the preceding line calculation gives $[M:\mathbb Q]^{-1}\sum_\rho\omega_{\rho,\tau}=\log\Omega_E$ for each $\tau$. If the generators were originally chosen over another coefficient field, pass to the compositum. Equality of their principal ideals with the prescribed lines descends along the faithfully flat extension of integer rings. This gives the same conclusion over every admissible $M$ containing the generators. The derivative orders $n_\tau$ at a fixed step are independent of $\rho$. The embedding average of the period contribution $-\sum_\tau n_\tau\omega_{\rho,\tau}$ to its log squared norm is thus exactly $-(\sum_\tau n_\tau)\log\Omega_E$. This evaluates the full period term of that step for the supplied generators. [Construction of the generators](column_laws/main.tex#L757-L779) · [Generator metric](https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AbelianVarietyTheory/Proofs/DivisorProofs/MeanLogMetricGeneratorEqMeanPeriod.lean#L10-L57) · [One-step kernel bound](https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AbelianVarietyTheory/BlockTheory/DivisorBase/TopPlaceLogTheta.lean#L17-L25)

A constant error per derivative would change this expression by that constant times the derivative order $a$ at every contributing step. This explains the need for the exact normalization. The genus mass has its own successive-rank ratio, already derived in the reconstruction. To use the two computations in the full period-height estimate one must still exhibit the chosen theta sections and arithmetic metrics together and control the norms of the resulting maps as the chain grows. [Exact Hermitian mass ratio, MF19](mass_formula/main.tex#L862-L889) · [The arithmetic and analytic heights compared in the slope argument](gram_frame/gram_frame_section.tex#L44-L111)

## A short literature proof of the successive-rank mass ratio

For the mass calculation the base field changes. Let $F=E^+$ be totally real of degree $f$ and assume the CM extension $E/F$ is unramified at every finite place. Let $\eta$ be its quadratic Hecke character, let $D_F=|\operatorname{disc}F|$, and put $v=\mathrm{rd}_E/2$. Let $M_r$ be the genus mass of the positive definite standard Hermitian lattice $\mathcal O_E^r$ with identity Gram matrix. Thus $M_r=\sum_{[L]}1/|\operatorname{Aut}_{\mathcal O_E}(L)|$, with the full unitary group as the isometry group. Gan, Hanke and Yu give an exact formula for this mass. Their adelic Haar measure gives volume one to the product of the entire compact group at infinity and the finite lattice stabilizers. Hence each double coset contributes exactly the reciprocal stabilizer order used here. [Gan–Hanke–Yu, *On an exact mass formula of Shimura*, (2.1)–(2.2) and (4.1)](https://web.math.princeton.edu/~jonhanke/Web-02/Mass-Formula-of-Shimura/shimura-mass.pdf#page=3)

Their maximality and local-factor requirements hold for the standard lattice. Locally it is self-dual. If $x$ belongs to a larger lattice with integral norms, polarizing the norm against all integral multiples of the standard basis vectors shows that the trace pairing of each coordinate of $x$ with all local integers is integral. The trace dual is the integer ring for a split or unramified quadratic algebra. Thus $x$ already lies in the lattice, including at dyadic places. At a split place the stabilizer is $\mathrm{GL}_r(\mathcal O_{F_v})$. At a nonsplit place the signed determinant is a unit and every unit is a norm in an unramified quadratic extension. Tables 1 and 2 give local correction factor one. For $r\ge1$, Propositions 4.4–4.5 and (4.2)–(4.3) therefore give

$$
 M_r=2^{1-rf}\prod_{j=1}^r |L_F(1-j,\eta^j)|.
$$

The factor $2$ is the Tamagawa number of the positive-rank unitary group. Taking absolute values uses positivity of the mass. [Gan–Hanke–Yu, §3, Tables 1–2, and §4, Propositions 4.4–4.5](https://web.math.princeton.edu/~jonhanke/Web-02/Mass-Formula-of-Shimura/shimura-mass.pdf#page=9) · [Local field and norm conventions, MF1–2](mass_formula/main.tex#L36-L89)

In the quotient $M_r/M_{r-1}$ for $r\ge2$, the Tamagawa numbers cancel and the sole new factor is $2^{-f}|L_F(1-r,\eta^r)|$. The project asks for $r\ge3$. Write $\epsilon=r\bmod 2$. The completed $L$-function has discriminant factor $D_F^{s/2}$ and archimedean factor $\Gamma_{\mathbb R}(s+\epsilon)^f$, with $\Gamma_{\mathbb R}(s)=\pi^{-s/2}\Gamma(s/2)$. Indeed the finite conductor is one and $\eta$ is the sign character at every real place. Equivalently, for even $r$ the function is $\zeta_F$, and for odd $r$ it is $\zeta_E/\zeta_F$. These two completed Dedekind zeta functional equations give the same factors since $|\operatorname{disc}E|=D_F^2$. In both parities the gamma reflection and duplication formulas give
$\Gamma_{\mathbb R}(r+\epsilon)/|\Gamma_{\mathbb R}(1-r+\epsilon)|=2(r-1)!/(2\pi)^r$.
Consequently

$$
 \frac{M_r}{M_{r-1}}
 =D_F^{r-1/2}
   \left(\frac{(r-1)!}{(2\pi)^r}\right)^f L_F(r,\eta^r)
 =\frac{\big((r-1)!(v/\pi)^r\big)^f}{\sqrt{(2v)^f}}\,
    L_F(r,\eta^r).
$$

Here $D_F=(2v)^f$. The final Euler product ranges over primes of $F$ and agrees term by term with the source’s $\operatorname{lValEta}(E,r)$. This recovers precisely the genus-mass ratio in MF19 by citation and a functional equation. The earlier reconstruction also treats arbitrary integral lattices with explicit bad-place density factors. [Euler factors, MF.3](mass_formula/main.tex#L65-L82) · [Target identity, MF.43](mass_formula/main.tex#L862-L889)
