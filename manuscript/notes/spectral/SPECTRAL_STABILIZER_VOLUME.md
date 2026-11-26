# The common stabilizer and fixed-unipotent volumes

Roadmap B8.02b, Claim 7 uses two Haar measures on the same arithmetic row. The common stabilizer of two flags uses normal-form coordinate Lebesgue measure at scale one. The fixed flag uses the Bessel-model measure at scalar parameter one. We compute both covolumes. An exact calculation of the trace-zero diagonal improves the two-sided bound in the source. [Claim 7 and its use in Claim 8][claim]

Let $E/F$ be the row's CM extension, unramified at every finite place, $f=[F:\mathbb Q]$, $v=v_E\ge1$, and $\rho=2v=|\operatorname{disc}E|^{1/(2f)}$. The relative discriminant is the unit ideal, so the discriminant tower formula gives $|\operatorname{disc}E|=|\operatorname{disc}F|^2$ and hence $|\operatorname{disc}F|=\rho^f$. Choose one embedding above each real place. The adapted pair of flags has length $r$ in dimension $2r+k+1$, pairing rank $j$, and block labels $\beta(0),\ldots,\beta(r-1)$. Put
$$
 m=r-j,\qquad A=\#\{(a,b):0\le a<b<r,\ \beta(a)=\beta(b)\},
 \qquad B=\binom m2.
$$
Fix the adapted form $\mathcal F$ of the term $t$. Let $\Gamma_0$ and $\Gamma_t$ be the groups in the common rational unipotent stabilizer preserving the reference completion and the term lattice, respectively. For this adapted form the weight in the [frame-fibre calculation](SPECTRAL_FRAME_FIBRE.md#relative-weights-in-the-bounded-set) is
$$
 \omega(t,\mathcal F)=\frac{[\Gamma_0:\Gamma_0\cap\Gamma_t]}
                   {[\Gamma_t:\Gamma_0\cap\Gamma_t]} .
$$
The exact scale-one volumes are
$$
 \boxed{\quad V_R=\omega(t,\mathcal F)\, v^{f(A+(k+1)m+B)}\rho^{fm/2},
 \qquad V_N=\rho^{f(r^2+r/2)}.\quad}                        \tag{1}
$$
Here $V_R$ uses the prescribed conjugation of the measure for this chart. The fixed-term amplitude uses $\omega_t=\inf_{\mathcal F}\omega(t,\mathcal F)$ after the chartwise bounds have been obtained. The identity for $V_N$ refers to the fixed-frame arithmetic subgroup in the Bessel model. The hypotheses on the host, marked flags and integral term are the standing hypotheses of Claim 7. [Term and reference stabilizers][weight] · [Measures in the actual term chart][chart] · [Term infimum][inf]

## Integral coordinates for the reference completion

Write $X,X'$ for the isotropic flag spaces, $I=X\cap X'$, and $\Lambda$ for the term lattice. Its inner module is $L=(X+X')^\perp\cap(\Lambda+X)$. The framed self-duality gives $I\subset L$, self-duality modulo $I$, and membership of the marked last vector $z$ in $L$. In the adapted splitting of $(X+X')^\perp$ with radical $I$, let $W_n$ be the chosen nondegenerate complement and $M=L\cap W_n$. The projection of $L$ along $I$ is exactly $M$ because $I\subset L$. A vector of $W_n$ pairs integrally with $M$ precisely when it pairs integrally with $L$; self-duality modulo $I$ therefore makes $M$ self-dual. Its rank is $k+1$, including the last-vector direction. The reference completion keeps this entire $M$, including any gluing between that direction and its definite perpendicular. [Inner module on the actual term][inner] · [Construction of the unimodular middle lattice][middle]

The flag-line ideals are $\mathfrak d^{-(r-a)}$ with $\overline{\mathfrak d}=\mathfrak d$ and $N_E\mathfrak d=\rho^{2f}$. Put $n_a=r-a$. In the following table an ideal or a vector lattice denotes its simultaneous image at the $f$ embeddings. The scalar in the last column multiplies each archimedean coordinate. The rows describe the successive translation lattices after setting the earlier group coordinates to zero. [Coordinate choices and their factors][factors]

| Coordinate | Independent entries | Arithmetic lattice per entry | Scale |
|---|---:|---|---:|
| Upper flag entry, $a<b$, $\beta(a)=\beta(b)$ | $A$ | $\mathfrak d^{-(b-a)}$ | $\rho^{b-a}$ |
| Middle displacement of the dual vector, $b\ge j$ | $m$ | $\mathfrak d^{-n_b}M$ | $\rho^{n_b}$ |
| Upper off-diagonal skew entry, $j\le a<b$ | $B$ | $\mathfrak d^{-(n_a+n_b)}$ | $\rho^{n_a+n_b}$ |
| Imaginary part of the skew diagonal, $a\ge j$ | $m$ | $\{t\in\mathfrak d^{-2n_a}:t+\bar t=0\}$ | $\rho^{2n_a}$ |

For the upper entry the ideal is the quotient of the two flag-line ideals. The adapted block normal form allows an elementary change within a block together with its inverse adjoint on the opposite lines. Thus every coefficient in that ideal occurs. A dual tail vector has coefficient ideal $\mathfrak d^{n_b}$. After fixing the upper coordinates, the component of its displacement in $W_n$ must belong to $\mathfrak d^{-n_b}M$, by testing on all multiples by $\mathfrak d^{n_b}$. For chosen middle components $y_b$ in those lattices, the correction on the isotropic lines is a matrix $C$ solving $C+C^*=-G$ in compatible Gram conventions, where $G$ is the Hermitian matrix of the $y_b$. Set one strict triangular half of $C$ to zero, fill the other from $-G$, and take $C_{aa}=-\theta G_{aa}$ with $\theta+\bar\theta=1$ in $\mathcal O_E$. Such a $\theta$ exists by surjectivity of the integral trace, proved below. The entries have the required product ideals by integrality of $M$. This gives the isometric lift of every middle displacement: translate each dual vector by its middle component and isotropic correction and take the opposite adjoint displacement on $W_n$. The displayed matrix equation is the preservation of all pairings between dual vectors. The inverse has the same ideal conditions. With the middle and upper coordinates zero the remaining displacements are exactly the skew matrices of the last two rows. [Elementary within-block lifts][top] · [Integral middle and skew lifts][lifts]

Take half-open additive fundamental parallelepipeds in the four rows. Reduce the upper coefficients in order of increasing $b-a$, using an elementary change for each entry. In a product of upper unitriangular matrices the cross terms at distance $b-a$ involve strictly shorter distances. Once the upper part is fixed, use the lifts with zero upper part to reduce the middle coordinates. Once these are fixed, the skew subgroup acts by independent addition. This produces a unique representative in the product box: any two reductions agree successively on the upper differences, middle rows and skew entries. Lifts of a particular middle element may differ by the skew kernel; the final reduction removes that ambiguity. The chart is injective. The coordinate ordering with the unipotent radical first and the ordering in the definition of scale-one measure give the same measure, since the upper group acts on the radical by triangular transformations of determinant one. The volume of the box in the prescribed Haar measure is consequently the product of its additive covolumes. [Triangular multiplication][law] · [Exact Haar measure of the product box][box]

## The four additive determinants

For ordinary Lebesgue measure in $\mathbb C^f$, an $E$-ideal $J$ has covolume $2^{-f}|\operatorname{disc}E|^{1/2}N_E J=v^fN_EJ$. This follows by replacing conjugate pairs of embedding rows in the discriminant matrix by real and imaginary parts. Multiplication by the positive scalar $\rho^n$ on every copy of $\mathbb C$ contributes $\rho^{2nf}$. In $\rho^n\mathfrak d^{-n}$ this cancels $N_E(\mathfrak d^{-n})$ exactly. Every upper and off-diagonal skew entry therefore contributes $v^f$. [Minkowski covolume with the prescribed place measure][ideal]

For the middle row put $d=k+1$. In a pseudobasis $M=\sum_i J_i e_i$ with Gram matrix $G$, self-duality gives the determinant ideal identity $(\det G)\prod_i J_i\overline{J_i}=\mathcal O_E$. At a place $\tau$, let $P_\tau$ give the columns of the $e_i$ in the chart. Its Hermitian form matrix has absolute determinant one, so $|\det P_\tau|^2=|\tau(\det G)|$. Taking norms in the determinant ideal identity gives $\prod_\tau|\det P_\tau|^2\prod_i N_E J_i=1$. The lattice volume is therefore $v^{fd}$. Twisting by $\mathfrak d^{-n_b}$ and multiplying by $\rho^{n_b}$ cancel in each of its $d$ coordinates. Every middle row contributes $v^{f(k+1)}$, independently of the choice of $M$. [Unimodular determinant in the middle-space realization][det] · [Row lattice and scaling][rows]

For the diagonal fix $n=n_a$. Since $E/F$ is unramified at all finite primes, the star-stable ideal $\mathfrak d$ is $\mathfrak q\mathcal O_E$ for an ideal $\mathfrak q$ of $F$. At a split prime the two exponents agree by conjugation, and at an inert prime its ramification index is one. Thus $N_F\mathfrak q=\rho^f$. Also $\operatorname{Tr}_{E/F}\mathcal O_E=\mathcal O_F$. Locally the trace of the split algebra is onto. At an inert prime reduction gives the surjective trace of a finite separable extension of residue fields, so the integral trace ideal contains a local unit. This includes residue characteristic two. Hence $\operatorname{Tr}_{E/F}(\mathfrak d^{-2n})=\mathfrak q^{-2n}$ by localization.

Project the complex lattice $\rho^{2n}\mathfrak d^{-2n}$ onto its real coordinates. The image is the real embedding of $\tfrac12\rho^{2n}\mathfrak q^{-2n}$ because $\Re \tau(t)=\tau(\operatorname{Tr}_{E/F}(t))/2$. Its covolume equals
$$
 2^{-f}\rho^{2nf}\sqrt{|\operatorname{disc}F|}\,N_F(\mathfrak q^{-2n})
       =2^{-f}\sqrt{|\operatorname{disc}F|}.
$$
The kernel is exactly the imaginary lattice in the last row, identified with $\mathbb R^f$ by imaginary parts. Lift a $\mathbb Z$-basis of the image and adjoin a basis of the kernel. The determinant of this block triangular matrix shows that the complex covolume $v^f$ is the product of the two covolumes. The imaginary covolume thus equals
$$
               \frac{v^f}{2^{-f}\sqrt{|\operatorname{disc}F|}}
                 =\rho^{f/2}.                                   \tag{2}
$$
This is the covolume in the coordinate $\operatorname{Im}(t)$ of a trace-zero element $t$. The equality uses the kernel of the real projection. Projecting all of $\mathfrak d^{-2n}$ onto its imaginary part would give a different lattice in general. Finite unramifiedness is used both for the ideal descent and the trace image. The pinned proof uses the coarser interval $[(8v)^{-f},(8v)^f]$ for exactly this imaginary-part coordinate. [Finite unramifiedness on the host][unram] · [Pinned skew lattice and scaling][diag]

## Transport to the arithmetic term and the fixed Bessel model

Multiplication of the four factors gives the reference value $V_0=v^{f(A+(k+1)m+B)}\rho^{fm/2}$. Both full lattices are commensurable. Their stabilizers in the common rational group are commensurable as well: multiples of either lattice sandwich the other, and its stabilizer permutes the finite interval of intermediate lattices. A fundamental set for $\Gamma_0\cap\Gamma_t$ has volume $[\Gamma_0:\Gamma_0\cap\Gamma_t]V_0=[\Gamma_t:\Gamma_0\cap\Gamma_t]V_R$. In the adapted factorization $n_1g_*n_2$ of the inverse term-coordinate element, the actual term measure is the pushforward of this chart measure by conjugation by $n_2^{-1}$. The original real embeddings $\phi_\tau$ identify the actual arithmetic subgroup of the term with the simultaneous image of $\Gamma_t=R_{\mathcal F}(F)\cap\operatorname{Stab}(\Lambda_t)$. The adapted embeddings $n_{2,\tau}\phi_\tau$ realize that same subgroup in normal form. Conjugation carries its fundamental set and measure together. This proves the first equality of (1) for any measurable fundamental set in these coordinates. It also establishes the source bound directly: $A,B\le\binom r2$, $m\le r$, and $\rho^{1/2}\le8v$, so
$$
 V_R/\omega(t,\mathcal F)\le v^{kmf}(8v)^{f(A+B+2m)}
                  \le v^{kmf}(8v)^{2(r+1)^2 f}.
$$
[Commensurable domain comparison][index] · [Actual chart and conjugation][chart]

For the fixed flag paired with itself the supplied base normal form has $j=0$, constant $\beta$, $\Lambda_{\rm ref}=\Lambda_0$, and the common arithmetic group is the full fixed-frame unipotent. Hence $m=r$ and $A=B=\binom r2$. Its coordinate covolume is $v^{f(rk+r^2)}\rho^{fr/2}$. The Bessel measure per place is $(2v)^{-rk}2^{r(k+1)+r(r-1)}$ times coordinate Lebesgue. Indeed in the Lie algebra norm each independent complex upper, middle or off-diagonal skew entry occurs twice. Its two real directions contribute a Jacobian factor of two, and each real skew diagonal contributes one. The number of complex coordinates is $r(k+1)+r(r-1)$. The Bessel normalization contributes the remaining $(2v)^{-rk}$ at scalar one. The equality of Haar measures follows from their densities at the identity. Therefore the product over all places gives
$$
 V_N=\big((2v)^{-rk}2^{r(k+1)+r(r-1)}\big)^f
              v^{f(rk+r^2)}\rho^{fr/2}
     =\rho^{f(r^2+r/2)}.
$$
This gives $0<V_N<\infty$ and $V_N^{-1}\le1$ on the actual host. Both arithmetic volume inputs in the [orbital amplitude](SPECTRAL_ORBITAL_AMPLITUDE.md) follow with its prescribed measures and relative weight. [Fixed normal form and product-measure transport][self] · [Lie norm computation][lie] · [Haar density at the identity][haar]

[claim]: https://github.com/rh-lean-roadmap/rh-lean-roadmap/blob/94e6a98b4e74932a0298d6bd22d44cf60c62764b/docs/src/book/main.tex#L41746-L41777
[weight]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AbelianVarietyTheory/Definitions/SemilocalFrames/NormalFormDualOrthogonalLast.lean#L87-L110
[chart]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AbelianVarietyTheory/Proofs/FlagMeasures/IntegralStabiliserCovolumeLeIndexWeight.lean#L23-L78
[inner]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AbelianVarietyTheory/Proofs/FlagMeasures/HermitianStabiliserCovolumeLe.lean#L108-L120
[middle]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AbelianVarietyTheory/Proofs/FlagMeasures/ExistsUnimodularTraceOnMiddleSpaceLift.lean#L106-L172
[factors]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AbelianVarietyTheory/Proofs/FlagMeasures/CovolumeReferenceLatticeStabiliserBounds.lean#L107-L130
[top]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AbelianVarietyTheory/Proofs/FlagMeasures/IsBlockOfFrame.lean#L633-L638
[lifts]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AbelianVarietyTheory/Proofs/FlagMeasures/RefLatticeStabilizerMiddleBottomLayers.lean#L440-L531
[law]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AbelianVarietyTheory/Proofs/FlagMeasures/CommonStabilizerFromCoordinatesProductLaw.lean#L142-L172
[box]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AbelianVarietyTheory/Proofs/FlagMeasures/MeasureCommonStabilizerCoordsBoxImage.lean#L31-L66
[ideal]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AbelianVarietyTheory/Proofs/FlagMeasures/ExistsFundIpow.lean#L16-L77
[det]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AbelianVarietyTheory/Proofs/FlagMeasures/UnimodularLatticeFundamentalSetVolume.lean#L163-L251
[rows]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AbelianVarietyTheory/Proofs/FlagMeasures/ExistsFundamentalSetRowsMiddleSpace.lean#L57-L70
[diag]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AbelianVarietyTheory/Proofs/FlagMeasures/ExistsFundSkew.lean#L89-L121
[index]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AbelianVarietyTheory/Proofs/FlagMeasures/HermitianStabiliserCovolumeLe.lean#L109-L126
[self]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AbelianVarietyTheory/Proofs/FlagMeasures/IntegralUnipotentCovolumeFiniteBounded.lean#L61-L104
[lie]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AbelianVarietyTheory/Proofs/FlagMeasures/HaarLieNilpotentEqLebesgue.lean#L386-L393
[haar]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AbelianVarietyTheory/Proofs/FlagMeasures/HaarLieNilpotentEqLebesgue.lean#L530-L567

[inf]: https://github.com/rh-lean-roadmap/rh-lean-roadmap/blob/94e6a98b4e74932a0298d6bd22d44cf60c62764b/docs/src/book/main.tex#L41465-L41476
[unram]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AbelianVarietyTheory/Proofs/GlobalInterpolation/UnramifiedOfIsCMUnram.lean#L35-L44
