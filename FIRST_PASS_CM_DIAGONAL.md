# The diagonal derivative on the original CM order lattice

Let $E$ be the built abelian CM host, $F=E^+$, $n=[F:\mathbb Q]\ge2$, $k=2s\ge2$, and fix a prime $\ell$ and an embedding of the algebraic numbers into $\mathbb C_\ell$. Normalize $v_\ell(\ell)=1$. The actual host has $d>4$ prime and $d\equiv3\bmod4$. Its CM type $(\phi_i)$ has common value $i\sqrt d$ on $w$ with $w^2=-d$. Put $\theta=(-1+w)/2$ and $\tau=(-1+i\sqrt d)/2$. The prescribed elliptic lattice $\Lambda$ is the ring of integers of this imaginary quadratic field, so equals $\mathbb Z+\tau\mathbb Z$. Take any $\Omega$ with $\Omega^{12}=\Delta_\Lambda$. Write $a=a_0(\mathfrak f,\ell)$, $c=c_{\rm vp}(\mathfrak f,\ell)$, $\nu=v_\ell(d)$, $e=c_{E,\ell}(z)$ and $d_\ell=v_\ell(|\operatorname{disc}F|)$. Here $z$ gives the rational partial zeta values at $1-k$ for the ordinary ideal classes of $F$. The loss of an algebraic number $x$ means $-v_\ell(x)$, with $v_\ell(0)=+\infty$. [Field, period and conductor conditions][field] · [Jet assertion][target]

**Passage to a Hilbert lattice.** For a permitted set $Q$ disjoint from $\ell$ and a representative $y$ equal to one at all places over $\ell$, put $\mathfrak f_Q=\mathfrak f\prod_{\mathfrak q\in Q}\mathfrak q$ and $\mathcal L_y=E\cap y\widehat{\mathcal O}_{\mathfrak f_Q}$. Choose positive integers $M,B$ prime to $\ell$ with
$$
 M\mathcal L_y\subset\mathcal O_E,\qquad B\ell^a\mathcal O_E\subset\mathcal L_y .
$$
For the first inclusion the lattice is integral at $\ell$, and only finitely many other denominators need clearing. For the second, $\ell^a$ has sufficient valuation at primes of $F$ over $\ell$ for the base conductor. Multiplication by an integer prime to $\ell$ puts it in $\mathfrak f_Q$. Another such integer clears the nonintegral components of $y^{-1}$. Now use $\mathfrak f_Q\widehat{\mathcal O}_E\subset\widehat{\mathcal O}_{\mathfrak f_Q}$. Set $H=Md$ and
$$
 L=\{(x_0,x_1)\in F^2:x_0\theta+x_1\in H\mathcal L_y\},\qquad N=(\ell+1)HB\ell^a .
$$
Then $N\mathcal O_F^2\subset L\subset\mathcal O_F^2$ and $v_\ell(N)=\nu+a$. For the upper inclusion write $Mu=r_0\theta+r_1$ for $u\in\mathcal L_y$, so the corresponding $x_j=dr_j$. With $\delta=\theta-\bar\theta$ one has $\delta^2=-d$, $\delta r_0=Mu-\overline{Mu}$, and $\delta r_1=\delta Mu-\theta(Mu-\overline{Mu})$. Thus $\delta r_j$, $dr_j$, and $dr_j^2$ are algebraic integers. In particular every conjugate of $x_j$ has valuation at least $\nu/2$. The lower inclusion follows by dividing $N(x_0\theta+x_1)$ by $H$ for $x_j\in\mathcal O_F$. The nonzero mark $t=(N/(\ell+1),N/(\ell+1))\bmod N$ has order $\ell+1$. [Choosing the multiples and level][level] · [Coordinate and mark estimates][coord]

**Equality of germs.** Identify $\phi_i|_F$ with the real embeddings $\sigma_i$. The map $u(x)=(x_0\theta+x_1)/H$ is an $F$-linear isomorphism since $[E:F]=2$ and $\theta\notin F$. Its restriction gives a bijection $(L\setminus\{0\})/\mathcal O_F^\times\longrightarrow(\mathcal L_y\setminus\{0\})/\mathcal O_F^\times$. For $|z_i|<1$ set $A_i=1+z_i$ and $B_i=\tau+z_i\bar\tau$. Then
$$
 \sigma_i(x_0)B_i+\sigma_i(x_1)A_i
       =H\big(\phi_i(u(x))+z_i\overline{\phi_i(u(x))}\big),\qquad
 \Im(B_i/A_i)=\Im(\tau)(1-|z_i|^2)/|1+z_i|^2>0 .
$$
The weighted summand is invariant under $\mathcal O_F^\times$, since $k$ is even and a unit has norm $\pm1$. At Hecke parameter $\xi$ the Hilbert summand is the original one times $H^{-n(k+2\xi)}$. For $k>2$ apply this to the absolutely convergent sum at $\xi=0$. For $k=2$ use the [weight-two continuation](FIRST_PASS_CM_WEIGHT_TWO.md) and reindex first on $\Re\xi>0$. Multiplication by the displayed entire factor carries the defining holomorphic continuation on $\Re\xi>-1/2$ to the continuation of the Hilbert sum. Uniqueness gives the same identity at zero for each $z$. Both sides use the constant $((k-1)!)^n|\operatorname{disc}F|^{(k-1)/2}$. Thus the normalized deformed germ $g$ is $H^{kn}$ times the normalized Hilbert germ in these coordinates. Every ordered word of derivatives with counts $\kappa_i$ has value
$$
 D^\kappa g(0)=H^{kn}\operatorname{jet}_k(L,\kappa;\tau,1,\bar\tau-\tau). \qquad (1)
$$
This is an undivided derivative. Equality of ordered and canonical words follows from holomorphy of the continued Hilbert germ in the deformation variables. The argument passes to the value at $\xi=0$ before differentiating in $z$. [Definitions of the continued sums][sums] · [Equivariance, bijection and continuation][germs] · [Ordered words and derivatives][words]

**Finite diagonal expansion.** Write $J=\sum_i\kappa_i$, $W=kn+2J$, $P=2\pi i$, $v=\pi/\Im\tau$ and $\omega=\Omega/P$. The elliptic marking gives $\omega^{12}=\Delta(\tau)$ in the source's normalized modular convention. For the chosen torsion mark put $C=wB_N(t)$, the holomorphic correction $(G_2+\wp_{\mathbb Z+\tau\mathbb Z}(t_\tau))/P^2$ with $t_\tau=(t_0\tau+t_1)/N$ modulo the lattice. Write
$$
 K=\frac{G_2^*(\tau)/P^2+\operatorname{wp}_N(t,\tau)}{\omega^2},
 \quad H_\mu=\frac{\operatorname{hfun}_k(L,\mu,C)(\tau)}{\omega^{kn+2|\mu|}},
 \quad \mathcal J=\frac{v^J\operatorname{jet}_k(L,\kappa;\tau,1,\bar\tau-\tau)}{P^W\omega^W}.
$$
Here $\operatorname{wp}_N=\wp(t_\tau)/P^2$. Then
$$
 \mathcal J=\sum_{\mu\le\kappa}\left(\prod_i
 (-1)^{\kappa_i-\mu_i}\binom{\kappa_i}{\mu_i}(k+\mu_i)^{\overline{\kappa_i-\mu_i}}\right)
 (-K)^{J-|\mu|}H_\mu . \qquad (2)
$$
The rising factorial of length zero is one. Scale the direction $(1,\bar\tau-\tau)$ by $v$ to obtain $(v,-P)$. Write $v=P^2C(\tau)+D$. Adding the radial component $D$ multiplies the one-embedding germ by $(1+Dz)^{-k}$ and replaces its parameter by $z/(1+Dz)$, by factoring $1+Dz$ from both homogeneous coordinates. Its old $m$th derivative contributes to the new $r$th derivative with coefficient $(-1)^{r-m}\binom{r}{m}(k+m)^{\overline{r-m}}D^{r-m}$, by expanding $z^m(1+Dz)^{-k-m}/m!$. Multiplying this identity over the embeddings proves the numerator formula. Each radial power costs two units of weight, and $(v/P^2-C(\tau))/\omega^2=-K$. This proves (2). [Definitions of the directions and weights][directions] · [Homogeneous expansion][diagonal] · [Nonholomorphic correction and evaluation][exp]

**Cancellation.** Use $b=\nu+a$, $\rho_0=-\nu/2$ and $\rho=2c+2a+\nu/2$. The discriminant tower gives $d_\ell/n\le v_\ell(|\operatorname{disc}E|)/(2n)\le c$. For the second inequality a base conductor prime over $\ell$ forces $\ell$ to be unramified in $E$, and otherwise $c$ equals the normalized discriminant exponent. Hence $b+d_\ell/n+\rho_0\le\rho$. The [Fourier estimate at all cusps](FIRST_PASS_CM_FOURIER_BOUND.md) and its [evaluation at the integral CM value of $j$](FIRST_PASS_CM_MODULAR_VALUES.md) give algebraicity and loss at most $e+s\,d_\ell+kn(\nu+a)+|\mu|\rho$ for $H_\mu$. The [elliptic correction](FIRST_PASS_CM_TORSION_CORRECTION.md) has loss at most one at $2$, one half at $d$, and zero elsewhere on this host. At $2$, the even field discriminant and Galoisness imply $c\ge1/2$. Indeed for ramification index $h\ge2$ the local different exponent is at least $h-1$, giving normalized discriminant exponent at least $(h-1)/h$. Thus $K$ has loss at most $\rho$ at every prime. Equation (2) and the ultrametric inequality give
$$
 -v_\ell(\mathcal J)\le e+s\,d_\ell+kn(\nu+a)+J(2c+2a+\nu/2). \qquad (3)
$$
[CM period, integral $j$ and correction][period] · [Parameter substitutions and dyadic case][sizes]

Choose algebraic $\gamma\ne0$ with $v_\ell(\gamma)=c+\nu/2$, possible since the exponent is rational. Set, for every $i$,
$$
 a_i=\Omega/\ell^a,\qquad b_i=(2\pi/\sqrt d)\gamma/a_i,\qquad
 U=D^\kappa g(0)\prod_i\big((b_i/a_i)^{\kappa_i}a_i^{-k}\big).
$$
The separate normalization bounds follow from $a_i/\Omega=\ell^{-a}$ and $a_i b_i\sqrt d/(2\pi)=\gamma$. By (1), $P\omega=\Omega$, and $2\Im\tau/\sqrt d=1$, one has the exact equality
$$
 U=\mathcal J (H\ell^a)^{kn}(\gamma\ell^{2a})^J .
$$
The per-derivative multiplier before substituting the imaginary part is $(2\Im\tau/\sqrt d)\gamma\ell^{2a}$. The extra factors are algebraic, of respective valuations $kn(\nu+a)$ and $J(c+\nu/2+2a)$. Subtracting them from (3) gives
$$
 \boxed{-v_\ell(U)\le e+s\,d_\ell+Jc\le e+knc+Jc.}
$$
This proves algebraicity and the requested loss for all words with counts $\kappa$ with the same coordinates. The order-lattice transport, radial identity and cancellation use the Hilbert Fourier expansion with its weight-two continuation and the modular and elliptic evaluation results used in (3). They require no further continuation or regularization. The jet assertion quantifies over $g$ satisfying the defining summation or continuation property. Existence also follows here by the reverse change of variables. Indeed write $L=\{(u,v): u\in\mathfrak b,\ v-\eta u\in\mathfrak a\}$ using the splitting of the projection onto its first fractional ideal. The shear $(u,v)\mapsto(u,v-\eta u)$ and division of each coordinate by $A_i$ reduce the Hilbert value to the ordinary pair-of-ideals Eisenstein value at $B_i/A_i+\sigma_i(\eta)$ in the upper half-plane. The scalar on the regulated series is $(\prod_i A_i)^{-k}|\prod_i A_i|^{-2\xi}$, entire in $\xi$ for each fixed $z$. The Hilbert expansion supplies this value and its continuation. Multiplying back by $H^{n(k+2\xi)}$ supplies a defining sum on the whole polydisc. The separate relation of its derivatives to the class-sum functional through the rising factor remains the derivative-formula input to the toric argument. [Splitting the lattice][split] · [Value on a pair of ideals][isg] · [Homogeneity before continuation][hom] [Exact change of normalization][factor] · [Final loss and analytic dependency][finish]

[field]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AbelianVarietyTheory/BlockTheory/DivisorBase/VpBounds.lean#L34-L55
[target]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AbelianVarietyTheory/Definitions/Divisors/JetAnalytic.lean#L239-L245
[level]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AbelianVarietyTheory/Proofs/DivisorProofs/MemPassScaled.lean#L42-L86
[coord]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AbelianVarietyTheory/Proofs/DivisorProofs/MemPassScaled.lean#L84-L118
[sums]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AbelianVarietyTheory/BlockTheory/DivisorBase/DefiningCoordinates.lean#L12-L34
[germs]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AbelianVarietyTheory/Proofs/DivisorProofs/DeformedLatticeValueEqHilbertEisensteinValue.lean#L96-L177
[words]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AbelianVarietyTheory/Proofs/DivisorProofs/DeformedLatticeSumDerivativesEqEisensteinJets.lean#L21-L53
[directions]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AbelianVarietyTheory/Definitions/Divisors/HasLevelStd.lean#L43-L67
[diagonal]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AbelianVarietyTheory/Proofs/DivisorProofs/EisensteinJetConjDirectionDiagonalExpansion.lean#L16-L49
[exp]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AbelianVarietyTheory/Proofs/DivisorProofs/SzJetConj.lean#L24-L56
[period]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AbelianVarietyTheory/Proofs/DivisorProofs/ImportsRestLast.lean#L21-L38
[sizes]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AbelianVarietyTheory/Proofs/DivisorProofs/CMLatticeDividedPowerJetIntegralityOfHyp.lean#L194-L219
[factor]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AbelianVarietyTheory/Proofs/DivisorProofs/CMLatticeDividedPowerJetIntegralityOfHyp.lean#L131-L140
[finish]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AbelianVarietyTheory/Proofs/DivisorProofs/CMLatticeDividedPowerJetIntegralityOfHyp.lean#L220-L252


[split]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AbelianVarietyTheory/Proofs/DivisorProofs/ExistsSplitOfHilbertLatticeHasLevel.lean#L23-L45
[isg]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AbelianVarietyTheory/Proofs/DivisorProofs/IsHilbertEisensteinLatticeValueOfEisensteinSerie.lean#L117-L140
[hom]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AbelianVarietyTheory/Proofs/DivisorProofs/HilbertEisensteinValueLinearChange.lean#L47-L105
