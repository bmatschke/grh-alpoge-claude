# The probability of a short flag and the moderate near-orbit estimate

Let $E/F$ be the project's CM extension unramified at every finite place. Write $f=[F:\mathbb Q]$, $r=\mathrm{rd}_E$, $v=r/2$, and $\eta$ for the quadratic character of $E/F$. Use a row of rank $n=p+q$, signature $(p,q)$ at every infinite place, and its self-dual point lattices. If $2q+2\le n$, fix positive flag increments $j_1,\dots,j_a$ with $a\ge1$ and $J=\sum j_i\le q$. For every Borel subset $B$ of $0<t_1<\cdots<t_a<1/2$, the normalized Haar measure on the original automorphic fundamental domain satisfies
$$
 \Pr\{\text{canonical flag of type }j,\ t\in B\}
 \le \kappa_j\int_B D_j(t)\,dt. \tag{1}
$$
Here $D_j(t)=P_{\rm id}(j,t)\prod_i(2fj_i/t_i)$, with $P_{\rm id}$ the layer product of [C83N6](../../../archive/rounds/v83/continuation_v83/nearflag.tex#L97-L149), and $\kappa_j$ is the exact coefficient in the [flag constant estimate](../construction/RETAINED_NEAR_TERMS.md). The result applies on the quotient carrying the finite test in each of the three projected counts. [Source statement][contract] · [Roadmap, Lemma 37.17, proof of (40.574)][road]

## The contribution of one integral class

Give each real unitary group the Haar measure whose density at the identity is Euclidean for the Hilbert–Schmidt metric. Fix any Haar measure $\mu_f$ at the finite adeles and divide by $\mu_f(K)$ for the full lattice stabilizer. Write $V$ for the resulting volume of the rational quotient. In a ratio as in (1), replacing the original infinite Haar factors by these positive scalar multiples has no effect. The scale $\mu_f(K)$ cancels too. The finite tests at the two level primes are retained in the kernels to which (1) will be applied. [Gauges and quotients][normal]

Index realizable classes by the graded lattices $\Lambda_i$ of ranks $j_i$ and the residual lattice in signature $(p-J,q-J)$ as in the [integral flag classification](RETAINED_FLAG_CLASSES.md). For each list, use the explicit adapted-class inequality of Adriazola. In the gauges just chosen its upper bound for the real class slice is
$$
 c_{\rm Iw}^f(2v)^{fD/2}\!
 \left(\prod_i 2^{fj_i^2}\operatorname{slab}(\Lambda_i)\right)
 \operatorname{vol}_{0}(\Lambda_{\rm res})\int_B D_j(t)\,dt. \tag{2}
$$
The slab is the volume modulo the lattice automorphisms on $1\le\prod_{\sigma}|\det g_\sigma|^2<e$ for the Haar density $\prod_\sigma|\det g_\sigma|^{-2j_i}\,dg_\sigma$ with ordinary complex-coordinate Lebesgue measures. The residual factor is the real covolume of its integral isometry group. The other constants are
$$
 S=\sum_i j_i^2,\quad D=2nJ-2J^2-S,\quad
 c_{\rm Iw}=2^{-D/2}\,
 \frac{U_p U_q}
 {2^{S/2} U_{p-J}U_{q-J}\prod_i U_{j_i}},
 \quad U_k=2^{k(k-1)/2}\prod_{h=1}^k\frac{2\pi^h}{(h-1)!}.
$$
[Adriazola, inequality for one adapted class and its proof][ad] · [Identical source inequality][one]

For the normalization in (2), the parabolic of the adapted isotropic flag has real unipotent dimension $D$. The compact group in real Iwasawa integration has probability measure. Comparing the tangent measure of $NMK$ with the Hilbert–Schmidt measure gives the factor $2^{-D/2}\operatorname{vol}(K)/\operatorname{vol}(K\cap M)$. A compact $U(j_i)$ in the Levi occurs twice in the matrix, which gives $2^{j_i^2/2}$ in its metric volume. On the unipotent layers the integral Hom lattice between source and target grades has covolume given by the target covolume raised to the source rank divided by the source covolume raised to the target rank, with the coefficient-lattice covolume restored. Passing to the skew-adjoint half gives the bound $(2v)^{fD/2}P_{\rm id}(j,t_{\rm base})$ at the chosen base point. In detail the real and imaginary integral parts of each complex layer have equal covolume. At every rational prime one can choose an integral purely imaginary element which is a unit above that prime. Reduce an element minus its conjugate in each inert residue extension, or choose different components at split places, and use the Chinese remainder theorem. Multiplication in both directions then gives a squared covolume ratio which is a rational unit at every prime, hence one. The sum of the two lattices contains twice the whole lattice, and the sharper index bound $2^d$ in complex dimension $d$ follows by projecting a vector to its real part modulo the real integral lattice. The kernel of this map is exactly the sum, and the image lies in its half-lattice quotient. Thus either half has covolume at most $2^{d/2}$ times the square root of the whole covolume. The integral layers lift to group elements also above two. If an isometry holds through one nilpotent layer, its first error is self-adjoint, and multiplying by $1-u\,\text{error}$ cancels that layer for an integral $u+\bar u=1$. Strict filtration makes this induction terminate. The successive layer coordinates are triangular, so their covering covolumes multiply. Finally the Levi determinant coordinates carry $\prod_i2fj_i\,dt_i/t_i$, and the modular character carries the base layer product to $P_{\rm id}(j,t)$ at the moving point. These comparisons account for the full density of (2). [Radical lattice argument][rad] · [Levi integration and assembly][ad]

## The sum over classes

Every point of flag type in $B$ gives a saturated rational isotropic flag. Its finite lattice, flag, and real component can be moved by a rational unitary isometry and a lattice stabilizer element to the slice for its list. The sum over these slices is an upper bound, even if more than one flag occurs. One can see the measure inequality by decomposing the finite adeles into lattice-stabilizer cosets, then summing the indicator over rational translates modulo the flag stabilizer. Integration unfolds a countable sum of nonnegative functions. Each finite coset has mass $\mu_f(K)$, precisely the divisor in the definition of $V$. A measurable transversal in the real group for each stabilizer may be taken since the integral groups are discrete and countable. Residual double cosets unfolded in the same way sum to the normalized residual volume $V_0$. Enlarging the sum from realizable lists to all lists only increases it. Thus the numerator of (1), in the units used for $V$, is at most
$$
 c_{\rm Iw}^f(2v)^{fD/2}
 \prod_i\bigl(2^{fj_i^2}G_{j_i}\bigr)\,
 V_0\int_B D_j(t)\,dt, \tag{3}
$$
where $G_j=\sum_{[\Lambda]}\operatorname{slab}(\Lambda)$. This step includes all ideal classes of each graded lattice. No class number is introduced as a bound on the number of copies. The event is measurable. The point lattices have countably many rational sublattices, their covolumes are continuous in the real frame and locally constant at finite level, and the inequalities specifying successive semistable pieces are countable Borel conditions. For a fixed flag, the tuple of graded sizes is measurable, so taking its preimage of $B$ and the countable union over flags preserves measurability. [Unfolding and positive sum][sum]

## Volumes of the determinant slabs

For $j\ge1$ one has
$$
 G_j= v^{f j^2}\operatorname{Res}_{s=1}\zeta_E(s)
       \prod_{h=2}^j\zeta_E(h). \tag{4}
$$
In rank one the $h_E$ ideal classes have the same automorphism group. Set $s_\sigma=\log|z_\sigma|^2$ on each complex coordinate. The measure $dx_\sigma\,dy_\sigma/|z_\sigma|^2$ is $\tfrac12 ds_\sigma\,d\theta_\sigma$. A fundamental unit-log parallelepiped in the hyperplane $\sum s_\sigma=0$, measured after dropping one log coordinate, has volume $R_E$ (the usual number-field regulator). The slab $0\le\sum s_\sigma<1$ has width one in this last coordinate. The angles contribute $(2\pi)^f/w_E$ after quotienting by roots of unity. The analytic class-number formula gives $G_1=2^{-f}(2\pi)^f h_E R_E/w_E=2^{-f}\sqrt{|d_E|}\operatorname{Res}_{s=1}\zeta_E(s)$. Here $v^f=2^{-f}\sqrt{|d_E|}$.

For $j>1$ use Weil's theorem $\tau(\mathrm{SL}_j/E)=1$. Normalize finite additive measures on $E_w$ to give the integers volume one, and at complex places use $dx\,dy$. The additive adelic covolume is $\Delta=2^{-f}\sqrt{|d_E|}$. Hence the product measure on a group of dimension $d=j^2-1$ given by a rational volume form, before normalization by $\Delta^{-d}$, has quotient volume $\Delta^d$ on $\mathrm{SL}_j$. With the determinant-coordinate form on $\mathrm{GL}_j$ divided by $d(\det)/\det$, its integral generator at the identity is the usual volume form on $\mathfrak{sl}_j$. One diagonal entry is eliminated with coefficient one. The local compact volume for this latter form is
$$
 Q^{-d}\#\mathrm{SL}_j(\mathbf F_Q)=\prod_{h=2}^j(1-Q^{-h})
$$
by smooth reduction. Thus making the finite special-linear compact groups have volume one gives total special-linear quotient volume $\Delta^d\prod_{h=2}^j\zeta_E(h)$. The determinant has the section $t\mapsto\operatorname{diag}(t,1,\ldots,1)$ over both $E$ and the adeles, and over each finite compact on units. Conjugation by this section has determinant one on $\mathfrak{sl}_j$. Integrating along determinant fibres therefore multiplies the rank-one slab volume by the special-linear quotient volume. To identify this adelic slab with $G_j$, decompose by finite maximal-compact double cosets. They parametrize all projective lattice classes. On each such class the finite idele norm shifts the logarithmic determinant interval by a constant, preserving its width and the real covolume by scalar dilation. This gives (4), including the ordinary Lebesgue normalization at complex places. [Weil, *Adeles and Algebraic Groups*, Chapter III](https://doi.org/10.1007/978-1-4684-9156-2) · [Determinant slab in the source][gldef] · [Alternative primitive-column induction][gl]

## The unitary volume ratio

For a rank-$M$ step that removes a basis vector of norm $s=1$ or $-1$ in its signature, $M\ge3$, the normalized volumes satisfy
$$
 \frac{V_M}{V_{M-1}}=r^{f(M-1/2)} L_F(M,\eta^M). \tag{5}
$$
Here the remaining negative or positive directions are left in place. A standard diagonal signature form can be used by the local classification and Landherr's theorem in the [flag-class proof](RETAINED_FLAG_CLASSES.md). All finite stabilizers are transported within the self-dual genus, so their measures match after division by $\mu_f(K)$. The real frames identify the Hilbert–Schmidt measures.

Use the [one-vector form of Weil's convergent Siegel–Weil identity](../construction/RETAINED_DIMENSION_COMPARISON.md), in its range $M>2$. Take the integral-lattice indicator at each finite place and a compactly supported smooth test of positive fibre integral at infinity on the quadric of norm $s$. On the geometric side all rational vectors of norm $s$ form one orbit by Witt's theorem. The integral vectors of that norm form one orbit of the self-dual stabilizer locally: their spans split off a unimodular line, and their orthogonal complements in that genus are locally isometric. With the finite maximal compacts of both groups scaled to mass one the finite orbital factor is one. At infinity use a unit coordinate vector. In the tangent to its norm fibre write the varying coordinate parallel to the vector as $it$, and the remaining $M-1$ complex coordinates as $z$. Its horizontal lift in the unitary Lie algebra has squared Hilbert–Schmidt norm $t^2+2\sum_i |z_i|^2$. The quotient of the two group gauges therefore has density $2^{M-1}$ in the real coordinates $(t,z)$. On the Gram side the self-dual measure for the real trace pairing is $2^M$ times Lebesgue measure on $\mathbb C^M$, the scalar value has Lebesgue measure, and the derivative of signed norm in the radial direction has absolute value two. The fibre density is again $2^{M-1}$. Invariance extends the equality over the orbit. Thus the normalized unfolded mean of this test is $V_{M-1}/V_M$ times its archimedean fibre integral.

For the density calculation choose the standard adelic character of $\mathbb Q$ composed with $\operatorname{Tr}_{F/\mathbb Q}$. A change by $a\in F^\times$ scales the local vector-to-scalar measure ratio by $|a|_w^{M-1/2}$, whose product is one. On the Gram-density side let $Q$ be the finite residue cardinality and $i_w$ the norm of the absolute local different of $F_w$. The self-dual vector-space and scalar measures contribute $i_w^{1/2-M}$ since the relative different of $E/F$ is trivial. The count of norm-$s$ vectors modulo the maximal ideal is $Q^{2M-1}(1-\eta(w)^M Q^{-M})$. For a split residue algebra this follows by summing an additive character over the second half of a perfect pairing. For the quadratic field of residues, every nonzero norm has $Q+1$ preimages and the sum of a nontrivial character over the norms in one coordinate is $-Q$. Additive orthogonality in $M$ coordinates gives the stated formula for either unit $s$. Each solution is smooth since the linearized norm map onto the base residue field is surjective, also at two by the residue trace. Accordingly each residue solution lifts with factor $Q^{2M-1}$ at every step. This gives finite local density $i_w^{1/2-M}(1-\eta(w)^M Q^{-M})$. Its product is $r^{f(1/2-M)}/L_F(M,\eta^M)$, since $\prod i_w=|d_F|=r^f$. The product converges absolutely. Cancelling the positive archimedean integral between the two expressions for the mean proves (5). [Roadmap 37.6 and local densities][rstep] · [Source volume comparison][ustep]

Remove $J$ directions of each sign. The smallest ambient rank to which (5) is applied is $n-2J+1\ge3$. The residual genus is the one already identified, so $V/V_0$ is exactly the product of (5) for $n-2J<M\le n$. These quotients have positive finite volume by finite covolume of the adelic unitary group (its center is the anisotropic norm-one torus) and compact openness of the finite stabilizers.

## The normalized flag bound

Divide (3) by $V$ and insert (4) and (5). With $S_k=\prod_{h=1}^{k}2\pi^h/(h-1)!$, the coefficient of the remaining integral is
$$
 v^{-fD/2}2^{-f(nJ-J^2+J/2)}
 \left(\frac{S_pS_q}{S_{p-J}S_{q-J}\prod_iS_{j_i}}\right)^f
 \bigl(\operatorname{Res}_{s=1}\zeta_E(s)\bigr)^a
 \frac{\prod_i\prod_{h=2}^{j_i}\zeta_E(h)}
 {\prod_{h=n-2J+1}^n L_F(h,\eta^h)}.
$$
Indeed $\sum_{M=n-2J+1}^n(M-1/2)=2nJ-2J^2=D+S$, and $U_k=2^{k(k-1)/2}S_k$. Substituting these two identities in (3) and using $r=2v$ gives the displayed powers of $v$ and $2$. This is precisely $\kappa_j$ in (1). Both the archimedean product of gauge changes and the original finite compact volume cancel between numerator and denominator. [Five-factor identity and signs][five] · [Original ratio on a fundamental domain][div]

On the eventual counting range the [established inequality](../construction/RETAINED_NEAR_TERMS.md) bounds $\kappa_j$ by $\exp(-2Jnf\log n/3)$. With (1), C83N5–6 give the moderate near integral $\le D^\star\exp(-nf\log n/4)$ with the identity term $D^\star$ of the particular projector. The cusp probability estimate in that same note also becomes unconditional on this range. Indeed the middle-grade factors bound the integral of $D_j$ over the simplex by $(n-2J)^{-a}\le1$: discard the other factors, which are at most one, and enlarge to the unit cube. There are $2^{J-1}$ compositions of $J$. Their geometric sum is at most $2e^{-2nf\log n/3}\le e^{-nf\log n/3}$ eventually. In particular $\Pr\{m(x)<1/2\}\le e^{-nf\log n/4}$ eventually. The deep locus is a subset, so its **volume** satisfies this bound as well. The integral of the diagonal kernel over the deep locus and the far orbital contributions are separate estimates. [Weighted moderate-near estimate](../../../archive/rounds/v83/continuation_v83/nearflag.tex#L97-L149) · [Deep and far integrals in the counting formula][fard] · [Deep trace and projectors on this quotient](../arithmetic/RETAINED_PROJECTOR_COUNTS.md)

[contract]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AbelianVarietyTheory/Statements/CuspFrameWeights/SameKindIsometric.lean#L84-L102
[road]: https://github.com/rh-lean-roadmap/rh-lean-roadmap/blob/94e6a98b4e74932a0298d6bd22d44cf60c62764b/docs/src/book/main.tex#L58530-L58551
[normal]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AbelianVarietyTheory/Definitions/SemilocalFrames/DefClassNum.lean#L36-L46
[ad]: https://github.com/jimjamzola/RH-Alpoge-Reconstruction/blob/aa9c86bf2a7d29b08575641fecea19a2a603e87c/manuscript/sec14_bessel.tex#L1278-L1508
[one]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AbelianVarietyTheory/Proofs/FlagMeasures/FlagClassMeasureBoundLatticeStabiliser.lean#L174
[rad]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AbelianVarietyTheory/Proofs/FlagMeasures/UnipotentRadicalIntegralPointsCovolume.lean#L313-L405
[sum]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AbelianVarietyTheory/Proofs/FlagMeasures/IsotropicFlagUnfoldingBound.lean#L213-L283
[gldef]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AbelianVarietyTheory/Definitions/SemilocalFrames/DefClassNum.lean#L90-L109
[gl]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AbelianVarietyTheory/Proofs/FlagMeasures/GenLinTamagawaVolume.lean#L11-L30
[rstep]: https://github.com/rh-lean-roadmap/rh-lean-roadmap/blob/94e6a98b4e74932a0298d6bd22d44cf60c62764b/docs/src/book/main.tex#L58185-L58209
[ustep]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AbelianVarietyTheory/Proofs/FlagMeasures/EnnrealVolumeRatioStepCancel.lean#L77-L119
[five]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AbelianVarietyTheory/Proofs/FlagMeasures/ProdFiveFactorsHermitianVolume.lean#L80-L127
[div]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AbelianVarietyTheory/Proofs/FlagMeasures/IsotropicFlagProbabilityBoundOfVolumeRatio.lean#L64-L103
[fard]: https://github.com/rh-lean-roadmap/rh-lean-roadmap/blob/94e6a98b4e74932a0298d6bd22d44cf60c62764b/docs/src/book/main.tex#L58399-L58464
