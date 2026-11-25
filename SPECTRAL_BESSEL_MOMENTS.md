# Length moments in the real Bessel model

The [singular orbital integral](SPECTRAL_ORBITAL_AMPLITUDE.md) needs concentration of a Bessel coefficient in the original real frame. This note derives the two-sided tail from local representation data and explains the dependence on the chain length. Interlacing bounds the normalized Pieri scalar by pairing each interior numerator with a distinct denominator. Only the $2r+2$ separated lower nodes enter the high power in the projection estimate. Replacing that number by the full dimension $n=k+2r+1$ would exceed the allowed height. [Original moment ranges][road]

## The normalized period and the adjacent lengths

Work at one real place, first in the unit simple-root character. Put $\mu=\lambda+\nu$ in a shift family with $\|\nu\|_1\le q_0=km^5$. Let $B_\nu$ be the continuous equivariant period to the compact coefficient representation. Write $\sigma_\nu$ for the discrete series, $d_\nu$ for its formal degree and $d\mu_X$ for the compatible measure on the Bessel quotient $S\backslash G$. The [realization argument](SPECTRAL_BESSEL_REALIZATION.md) constructs the source's normalized period model, including zero neighbouring periods, on these shifted discrete series. Its local inputs are the signed minuscule tensor decomposition on smooth vectors, the normalized rank-one Bessel integral, and its projected matrix entry in the Capelli identity below. Jiang–Sun–Zhu's Theorem A supplies uniqueness for the real unitary Bessel pair. The tensor projections and comparison of their scales also enter the estimate. [Jiang–Sun–Zhu][jsz] · [Local family and quotient measures][family]

Concretely, in the source normalization the integrated matrix coefficient $\mathcal B_{w,v}$ on the Bessel group sends $\eta$ to $\langle B_\nu v,\eta\rangle B_\nu w$. Schur orthogonality on $G$, integrated first over $S$ and then on its quotient, gives
$$
 \int_X\|\mathcal B_{\sigma_\nu(x)w,v}(B_\nu v)\|^2\,d\mu_X
                 =\|w\|^2\|B_\nu v\|^4/d_\nu.
$$
For a nonzero period choose $B_\nu v\ne0$ and cancel $\|B_\nu v\|^4$. Thus $w\mapsto\sqrt{d_\nu} B_\nu(\sigma_\nu(x)w)$ is an isometry. A square-integrable coefficient realized by this smooth model is proportional to its period coefficient by uniqueness. Dividing its squared norm by its total mass produces the same probability measure $d\rho$ for a unit vector $w$. A zero period has zero contribution. The normalized rank-one integral specifies which scale to use at *different* shifts. [Normalization and nonvanishing in the source][family]

Let $l_a(x)$ be the Euclidean distance of the transported $a$th frame vector from the span of its predecessors, including the final vector of Hermitian norm $-T$. Write $R_a=l_{a+1}/l_a$ for $a<r$. Take the residual vector $e$ at index $a$. Choose a unit vector $v$ by applying the Hermitian signature involution to the next unit residual and multiplying by a phase. Then its Hermitian pairings with the first $a+1$ vectors vanish and its pairing with the next has value $-\mathrm i l_{a+1}$ in the source convention. The rank-two skew endomorphism formed from $e,v$ has Hilbert–Schmidt norm at most $2l_a$. Conjugating its exponential by $x$ gives a unipotent fixing the flag with only the chosen simple-root contribution to the differential of the character. Indeed $e$ differs from the $a$th vector by a combination of earlier ones, and the pairings just computed kill the character on the other adjacent entries. The character differential has absolute value $2l_{a+1}$. Expand the derived endomorphism in matrix units $E_{bc}$ in a unitary Cayley basis and apply Cauchy–Schwarz to obtain
$$
 R_a(x)^2\|B_\nu(\sigma_\nu(x)w)\|^2
 \le\sum_{b,c}\|B_\nu(\sigma_\nu(x)E_{bc}w)\|^2.               \tag{1}
$$
[Simple-root character and rank-two endomorphism][root] · [Pointwise inequality][pointwise]

There is a short compact-type bound for iterating (1). Let $V_t$ be the span of products of at most $t$ matrix units applied to the entire lowest compact type. It is compact-stable. On $V_t$ the compact highest weights differ from the initial highest weight by at most $2t$ in Euclidean norm. Indeed each step is a quotient of tensoring by defining times dual defining, restricted to the two compact blocks. The compact Pieri rule changes at most two coordinates by one on each irreducible constituent. The shifted lowest weight has coordinates bounded by $3b_v+2n$, where $10^6n^7\le b_v\le\beta=b^{\max(2,C_w)}$. For $t\le2n^2$ the compact Casimir is bounded above by $(\sqrt n(3b_v+3n)+2t)^2$. The full Casimir has scalar $\|\mu\|^2-\|\rho_G\|^2\ge-n^3$. The signed adjoint relations show
$$
 \sum_{b,c}\|E_{bc}w\|^2
 =\langle w,(2\Omega_K-\Omega_G)w\rangle
 \le\beta^4\|w\|^2 \qquad(w\in V_t).
$$
The last inequality follows already from $b_v\ge10^6 n^7$. Multiply (1) by the preceding power of $R_a^2$, integrate and iterate, terminating with the isometry. For every unit vector of the lowest type,
$$
       \mathbb E_\rho R_a^{2p}\le\beta^{4p},\qquad 0\le p\le2n^2. \tag{2}
$$
In particular, $l_r^2\ge T\ge1$ since subtracting the isotropic preceding frame preserves the Hermitian norm. All inverse-length moments of order $2p$ are at most $\beta^{4rp}$ for $rp\le2n^2$, by telescoping and Hölder. This half of the tail even avoids a change of representation. [Casimirs on the actual grid](ROW_CORE_BRANCHING.md) · [Source's level proof of (2)][road]

## The shift scalar and the spectral gaps

At a shift with nonzero starting period and $\|\nu\|_1+1\le q_0$, let $p_{sc}$ be the projection from the $c$th coordinate of the dual defining tensor into the summand of parameter $\mu-e_s$. Write $\kappa_s$ for the period scalar on the tensor with the fixed initial frame covector. The adjoint identity with the invariant signed form gives $|\kappa_s|^2=|c_s|$, where $c_s$ is the period evaluated on the projection back into the tensor. In the Capelli cofactor formula its absolute value is $T\prod_{i=1}^k|\mu_s-1/2-u_i|/\prod_{t\ne s}|\mu_s-\mu_t|$, with $u_i$ the compact Bessel parameter. Equivalently it is the absolute residue at $\mu_s$ of $T\prod_i(z-1/2-u_i)/\prod_t(z-\mu_t)$. For the higher Bessel flag the [cofactor calculation](SPECTRAL_BESSEL_COFACTOR.md) proves this entry from its two chains of simple-root character values and the compact infinitesimal character. The formal-degree ratio for the same Haar measure cancels the unshifted differences exactly. Hence
$$
 \frac{|\kappa_s|^2d_\nu}{d_{\nu-e_s}}
     =T\frac{\prod_{i=1}^k|\mu_s-1/2-u_i|}
             {\prod_{t\ne s}|\mu_s-1-\mu_t|}.                   \tag{3}
$$
[Projected Bessel matrix entry][entry] · [Signed adjoint and degree cancellation][scalar]

Here is a bound on the right that uses only the prescribed interlacing and spacing. Use one-based indices and $k\ge2$, as on the actual grid. The first $k-1$ nodes $\lambda_t$ are in $[0,b_v/8]$ with pairwise gaps at least $\gamma=nm^{10}$, where $m=2r+2$ and $n=k+m-1$. The separate unshifted gap between nodes of opposite signature is at least $n^{19}$, and on the shift ball it is still at least $n^{19}/2$. The remaining nodes lie in $[-2b_v,-b_v]$. For $2\le i\le k-1$ one has $\lambda_i<u_i<\lambda_{i-1}$. Set $z=\mu_s-1/2$. If $s\le k-1$, match numerator $i$ to $t=i-1$ for $i\le s$ and to $t=i$ for $i>s$. The indicated endpoint of the interval is the farther from $z$, because $|z-\lambda_s|\le q_0+1/2$ and the upper gaps exceed $2q_0+1$. If $s\ge k$, match every interior numerator to $t=i-1$, since $z$ is below all upper nodes. All these indices are distinct and different from $s$.

Put $\Delta_0=\min(\gamma,b_v)$. Every matched denominator has modulus at least $\Delta_0-q_0-1$. The ratio of its matched numerator to it is bounded above by $1+(|\nu_t|+1/2)/(\Delta_0-q_0-1)$ by the triangle inequality. Their product is at most $\exp((q_0+k/2)/(\Delta_0-q_0-1))\le\mathrm e$ on the stated grid, since $n\ge k$, $m\ge2$ give $\gamma=nm^{10}\ge 4km^5=4q_0$, and the native grid also gives $b_v\ge100q_0$. Here $q_0\ge k\ge2$. The unmatched denominators are nonzero integers by regularity of the unit shift and the common integral spacing. Each of the two remaining numerators, $i=1,k$, has modulus at most $3\beta$ since $|\lambda_s|,|u_i|\le\beta$ and $q_0+1/2\le\beta$ on this grid. Consequently (3) is at most $9\mathrm e T\beta^2\le T\beta^4$. This uses the original $u_i$ throughout the shift family even if an individual perturbation crosses an interlacing endpoint. [Exact numerical hypotheses of the lowering estimate][lower] · [The two grid scales on both actual sides][grids] · [Regularity and the shifted opposite-sign gap][shiftgaps]

## The tensor projection and the positive-length moment

For detail about the required decomposition, a vector of level $i$ has its weights within $\ell^1$ distance $i$ of the lowest compact highest weight $\Lambda$, and belongs to a finite compact submodule with $\sqrt{\Omega_K}\le\sqrt{c_K(\Lambda)}+4ni$. Start with a highest-weight vector of level zero. At a unit shift the tensor projection $p_{sc}$ costs at most two in this level. Its weights change by one compact coordinate and the reference weight changes by one. For the Casimir bound, restrict the dual defining tensor to the compact group. Each compact highest weight moves by one unit. Equivalently, the square root of the sum of squares of the compact infinitesimal generators on a tensor is at most the sum of their two square roots, by the triangle inequality in the direct sum over generators. On the defining and dual defining representations the extra cost is at most $\sqrt n$. On the shifted summand the reference changes to $\Lambda-e_s$. The numerical grid gives the one-sided comparison $\sqrt{c_K(\Lambda)}+\sqrt n\le\sqrt{c_K(\Lambda-e_s)}+8n$, which pays for the projection at level $i+2$. For a component embedded back into the original tensor, projection and embedding together cost at most $2\sqrt n\le8n$ with the original reference $\Lambda$. [Level on the shifted summand][level] · [Level on its embedded components][components]

Here are the norm estimates that make the projection usable. For an input supported in coordinate $c$, let $P_s$ be the projection followed by embedding on the tensor, $x$ the input and $W=\operatorname{span}\{P_sx\}$. On the dual tensor the total Casimir is $\Omega_G+n+2D$. On the summand of parameter $\mu-e_s$ its scalar changes by $-2\mu_s+1$, so the eigenvalue of the split Casimir $D$ is $-\mu_s+(1-n)/2$. The $P_s$ are its spectral idempotents on $W$. In the cofactor residue preceding (3) the variable is affinely reparametrized to have nodes $\mu_s$; the compact numerator is evaluated at $\mu_s-1/2$ and the new formal degree uses $\mu_s-1$. The eigenvalues for the first $k-1$ nodes lie in $[-5b_v/32,b_v/32]$, and those for the other $2r+2$ lie in $[31b_v/32,65b_v/32]$ with mutual distances at least one. Use the ordinary positive Hilbert norm on the sum of tensor coordinates. In these coordinates $D$ has diagonal $-E_{aa}$ and off-diagonal $-E_{ab}$. On the levels just specified the off-diagonal part has norm at most $b_v/16$.

For the latter estimate use the signed Casimir identity above, subtract the diagonal sum, and apply Cauchy–Schwarz over the $n$ columns. It suffices to bound
$$
 n\left(2(\sqrt K+4ni)^2-c-\|\Lambda\|^2+8b_vi\right)\le (b_v/16)^2,
$$
where $K=c_K(\Lambda)$, $c=\|\mu\|^2-\|\rho_G\|^2$ and $i\le4n^2+2$. Here the diagonal sum is bounded below by $\|\Lambda\|^2-8b_vi$ on unit vectors, by the weight condition. In the compact highest-weight formula $\Lambda=\mu+U-V$, $K=\|\mu+U\|^2-\|V\|^2$, the coordinates of $U,V,\rho_G$ have modulus at most $n$. Thus $2K-c-\|\Lambda\|^2\le n(12nb_v+4n^2)$ and $\sqrt K\le4nb_v$. For example, $i\le6n^2$ bounds the left side by $444n^5b_v+1156n^7$, which is at most $b_v^2/256$ since $b_v\ge10^6n^7$. All estimates are on the entire span $W$ since the level condition is stable under sums. [Signed Casimir estimate and arithmetic][off]

On the circle of centre $-b_v/16$ and radius $9b_v/16$ the diagonal weight bound gives $\|(\zeta+\operatorname{diag}E_{aa})w\|\ge15b_v\|w\|/32$. The $b_v/16$ perturbation gives a resolvent bound $32/(13b_v)$ on $W$. Thus the contour projector $P$ onto the first group has norm at most $18/13$. Also $\|D\|\le3b_v$ on $W$. For each eigenvalue in the other group, apply Lagrange interpolation on $(1-P)W$. Each numerator has norm at most $6b_v$, the denominators have absolute value at least one, and $\|1-P\|<3$. Hence each of these idempotents has norm at most $3(6b_v)^{2r+1}$. [Contour and interpolation][contour]

The tensor carries an invariant Hermitian form $[\ ,\ ]$ given by the signature signs on its coordinates. The eigenspaces are orthogonal for this form. On each eigenspace in the first group the form is nonnegative: on every negative-sign coordinate the distance between its diagonal weights and the cluster eigenvalue is at least $15b_v/16$, so the eigenvector equation and the off-diagonal bound imply that the squared negative-coordinate norm is at most $\|w\|^2/225$. The sum of the absolute signed squared norms in that group is therefore $[Px,Px]\le\|Px\|^2$. In the other group bound each absolute signed squared norm by its ordinary squared norm. The invariant form on an embedded summand agrees with its shifted unitary norm up to the fixed sign, under the normalized tensor identification. Summing gives
$$
 \sum_s\|p_{sc}w\|^2
 \le \big((18/13)^2+9(2r+2)(6b_v)^{2(2r+1)}\big)\|w\|^2
 \le (6b_v)^{2(2r+2)}\|w\|^2.                                   \tag{4}
$$
[Positive signature on the first group][positive] · [Signed tensor normalization and assembly][norms]

The tensor decomposition of the product of the coefficient with each coordinate of the transported initial vector gives a sum over these shifted periods applied to $p_{sc}w$, with scalars of absolute value $|\kappa_s|$. Square, apply Cauchy–Schwarz to this sum of at most $n$ terms, sum over $n$ coordinates, and integrate the preceding moment in the shifted representation. The isometry, (3) and (4) give
$$
 \int_X l_0^{2p}d_\nu\|B_\nu(\sigma_\nu(x)w)\|^2\,d\mu_X
 \le\big(n^2 T\beta^4(6b_v)^{2(2r+2)}\big)^p\|w\|^2=:A^p\|w\|^2
$$
for $\|\nu\|_1+p\le q_0$ and $i+2p\le4n^2$. Each step consumes one shift and two levels. A zero starting period gives zero on the left. [Tensor coordinate recursion][recursion]

At shift zero combine this with (2) by Hölder applied to $l_a=l_0R_0\cdots R_{a-1}$ with $r+1$ factors, inserting ones. This yields $\mathbb E_\rho l_a^{2p}\le(A\beta^{4r})^p$ for $(r+1)p\le\min(q_0,2n^2)$. Since $6b_v\le\beta^2$, we have $A\beta^{4r}\le\max(1,T)\beta^{20(r+1)}$. Right compact invariance extends the bound to the full lowest type: the quadratic form for a bounded truncation of the weight commutes with the compact group, and its top eigenspace contains a highest-weight vector. Then increase the truncation. Torus transport to the prescribed character changes each length and its inverse by at most $\max(\xi,\xi^{-1})^r$, with $\xi=\pi/(v_Eg_0g_1)$. At $q=(\lceil C_s\rceil+2)kr$ the thresholds give $q\le km^3$, $r+1\le m$, and $m^4\le k$. Thus $(r+1)q\le km^4\le\min(q_0,k^2)$ meets both reserves. The source's $H=b^{C_Hm}$ absorbs this torus factor and the square roots of both moment constants. Markov's inequality and the union over $l_a,l_a^{-1}$ yield, for $u\ge1$,
$$
 \rho\{\max_a(l_a,l_a^{-1})>uH\}\le (4r+4)u^{-2q}.
$$
This supplies the tail used in the orbital estimate on the identified [smooth realization and normalized shifted periods](SPECTRAL_BESSEL_REALIZATION.md), with the signed tensor decomposition at the given gaps. The [cofactor argument](SPECTRAL_BESSEL_COFACTOR.md) gives the required matrix entry on that model. The finite arithmetic triple count has its own normalization. [Transport and the source's tail][transport] · [Paired genus calculation](SPECTRAL_PAIRED_GENUS.md)

[road]: https://github.com/rh-lean-roadmap/rh-lean-roadmap/blob/94e6a98b4e74932a0298d6bd22d44cf60c62764b/docs/src/book/main.tex#L41547-L41644
[family]: https://github.com/rh-lean-roadmap/rh-lean-roadmap/blob/94e6a98b4e74932a0298d6bd22d44cf60c62764b/docs/src/book/main.tex#L41481-L41546
[transport]: https://github.com/rh-lean-roadmap/rh-lean-roadmap/blob/94e6a98b4e74932a0298d6bd22d44cf60c62764b/docs/src/book/main.tex#L41652-L41694
[jsz]: https://arxiv.org/abs/0908.1728
[root]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AbelianVarietyTheory/Proofs/JetHarmonics/ExistsLieUnitaryElementSimpleRoot.lean
[pointwise]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AbelianVarietyTheory/Proofs/JetHarmonics/BesselCayleySideBound.lean
[entry]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AbelianVarietyTheory/Proofs/JetHarmonics/DualTensorBesselMoment.lean
[scalar]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AbelianVarietyTheory/Proofs/JetHarmonics/FamilySetupMomentGrowth.lean
[lower]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AbelianVarietyTheory/Proofs/JetHarmonics/LoweringBound.lean
[level]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AbelianVarietyTheory/Proofs/JetHarmonics/UnitaryGlModuleProjDualTensorLevelAddTwo.lean
[components]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AbelianVarietyTheory/Proofs/JetHarmonics/UnitaryGlModuleProjComponentsLevelAddTwo.lean
[off]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AbelianVarietyTheory/Proofs/JetHarmonics/UnitaryGlModuleLevelOffDiagNormSqLe.lean
[contour]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AbelianVarietyTheory/Proofs/JetHarmonics/CloudNodeProjectionNormLowLevel.lean
[positive]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AbelianVarietyTheory/Proofs/JetHarmonics/InvariantHermitianFormNonnegOfCloudEigen.lean
[norms]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AbelianVarietyTheory/Proofs/JetHarmonics/SumNormSqProjectionsTensorUnitaryGlLe.lean
[recursion]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AbelianVarietyTheory/Proofs/JetHarmonics/FamilySetupCayleyMoment.lean

[grids]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AbelianVarietyTheory/Proofs/FlagMeasures/AmplitudeLocalDataMomentPieriHypotheses.lean#L59-L67
[shiftgaps]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AbelianVarietyTheory/Proofs/JetHarmonics/NumericalFamilyShapeGaps.lean#L73-L112
