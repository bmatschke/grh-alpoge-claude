# The finite signed energy at a represented corank-one point

Fix an ordered pair of words on the original tied Hida model and a represented nonsingular block point $w$. Assume the standing split-level and character hypotheses, the concrete term and row identifications, the pinned quotient measures, and $k\ge4r+7$, with $r=r_S$. We compute the sum of the squared norms of the **nongeneric class subtotals** at $w$, before different block points and normal labels are combined in the final corank-one sum. The calculation applies to equal and unequal words.

Let $P$ be the finite set of places in the matched local family. For $p\in P$ let $d_p$ run through its representatives of the inner frame data, with density weight $w_p(d_p)$ relative to the reference datum. Write $Z_p(d_p)$ and $N_p(d_p)$ for the sums of the local phases with their lattice weights over the zero- and positive-defect orbits, respectively. Outside the exceptional subset $\Omega\subseteq P$ set $N_p=0$. These are functions on the *same* space of data for the word pair. Write $V(c,w,\nu)$ for the original vector sum at partner class $c$, block point $w$ and normal label $\nu$, and $D_{\rm att}$ for the local tuples attained by such nongeneric subtotals. Then
$$
\begin{aligned}
\sum_{c,\nu}\|V(c,w,\nu)\|^2
 &=V_0J_2(w)\sum_{d\in D_{\rm att}}\!
 \left(\prod_{p\in P}w_p(d_p)\right)
 \\ &\qquad{}\times\left|\prod_{p\in P}(Z_p(d_p)+N_p(d_p))-
              \prod_{p\in P}Z_p(d_p)\right|^2 .
\end{aligned}\tag{1}
$$
Here $V_0>0$ is the common mass for the reference genus at the point. If $w$ has block lengths $s_i$, put $e(w)=\sum_i\binom{s_i}{2}$. Let $J_w$ be the pinned real orbital operator including the two-word normalization $\mathrm{scl}(u,u')\operatorname{vol}(K_2)$ in the source definition. Its factor in (1) is
$$
                      J_2(w)=g^{-2f e(w)}\|J_w\|_{\rm HS}^2,
       \qquad g=g_0g_1,\quad f=[F:\mathbf Q].                    \tag{2}
$$
Points where the real integral vanishes contribute zero. On the represented support which has a nonzero vector, $J_2(w)>0$. [Definition of the original orbital operator][jdef] · [Actual free coordinates][freeroots] · [Selected mass and orbital normalization][jscale] · [Existence of the matched family for the tied row][family]

## Transport of the phase of an original term

Fix a term $t_0$ in one row and one rational unipotent double coset at $w$. Write $\ell_t=n^{-1}\ell_{t_0}m$ for the relative isometry of any term there, with rational unipotents on the two respective sides. Transport its row lattice to the common frame coordinates, obtaining $\Gamma_t$. The row determines the common inner datum $d_0$. Let $\mu(\Gamma_t)$ be the inverse relative volume of the stabilizer of $\Gamma_t$ in the common frame stabilizer, with the source reference subgroup of unit volume. Let $\omega(d_0,\Gamma_t)$ be the finite product of its local witness phases. All the term vectors in this row and double coset have the form
$$
  v_t = w_{t_0}\,g^{-fe(w)}\mu(\Gamma_t)\omega(d_0,\Gamma_t)\,T ,
             \qquad \|T\|=\|J_w\|_{\rm HS},                        \tag{3}
$$
where $T$ is placed in the common row coordinate and $w_{t_0}^2=w_{\Lambda}w_{\Lambda'}$ is the product of the two original row weights. In particular the same vector occurs for all defect patterns in this fixed fibre. [Original row vector and its weight][rowvector] · [Lattice mass and witness phase][gframes] · [Common operator including the phase and covolume][oper]

Here is the sign computation in (3). Choose matrices $U,U'$ for the move of the two frames of $t$ to the base frames and an integral admissibility witness $\xi$ for $t$. All three are upper unitriangular. Put $s(B)=\sum_iB_{i,i+1}$, and $\psi_g(a)=\exp(2\pi i\operatorname{Tr}_{E/\mathbf Q}(a)/g)$. In normalized finite coordinates choose the rational unipotents acting on the two base frames by $U$ and $U'\xi^{-1}$. At each finite place the phase is the first witness character times the inverse of the second. The additive-character product formula sends the finite first character to $\psi_g(s(U))^{-1}$ and the finite inverse second character to $\psi_g(s(U'\xi^{-1}))$. Since $s(AB)=s(A)+s(B)$ on unitriangular matrices, the resulting phase is
$$
    \omega(d_0,\Gamma_t)
      =\psi_g(s(U))^{-1}\psi_g(s(U'))\psi_g(s(\xi))^{-1}.          \tag{4}
$$
This also proves independence of the chosen admissibility witness. In moving from $t_0$ to $t$, the two matrices become $U_0A,U'_0A'$ for the actions of $n,m$ on the frames. The same additivity splits off the two characters of $t_0$. They multiply the one common real operator by a unit scalar. Its Hilbert–Schmidt norm is unchanged. The stabilizer covolume in these coordinates is $g^{-fe(w)}\mu(\Gamma_t)$, yielding (3). [Superdiagonal and additive character][character] · [Rational lifts of both unipotents][lifts] · [Finite product with all three signs][phase] · [Covolume in the two Haar normalizations](SPECTRAL_ARITHMETIC_ORBIT_VOLUME.md)

The phase actually averaged in the [positive-defect move estimate](SPECTRAL_MOVE_CHARACTER_CONDUCTOR.md) is the local factor of (4). To see this directly, use an admissible full-image Eichler move at a step $1\le J\le r$, writing $x=\sum\alpha_i f_i$ and $x'=\sum\alpha'_i f'_i$ in the current normalized frames, numbered from $1$. The moved lattice $\Gamma_1$ has the same inner datum. Its phase satisfies
$$
 \frac{\omega_p(d,\Gamma_1)}{\omega_p(d,\Gamma)}
 =\psi_{0,p}\!\left(-\theta_p^{-1}
       h(\alpha_J f_{J+1}+\alpha'_J f'_{J+1},u)\right).           \tag{5}
$$
Indeed the move uses the two frame unipotents on opposite sides of the witness pair. The extra correction on the second side fixes its perpendicular pointwise and has trivial character. Computing the superdiagonal of the two remaining unipotents gives $\alpha_J f_{J+1}$ and $\alpha'_J f'_{J+1}$ in the first slot of the Hermitian form. The two local characters multiply and their inverse gives (5), including the minus sign. The reverse parameter $(-u,\bar s)$ returns the original lattice when $s+\bar s=h(u,u)$. Thus the weighted reversible averaging of the local energy argument acts on the character which appears in (3). [Inverse move with fixed datum][move] · [Character of the two triangular factors][movep]

## The orbit mass over an attained tuple

On the fixed row and double coset, equality of the terms is equivalent to the transported lattices lying in the same rational frame-stabilizer orbit. Conversely, for a lattice orbit with inner datum $d_0$, the two rational unipotent lifts take the original and the second row lattice to the same transported lattice. Composing the first inverse with $\ell_{t_0}$ and the second lift therefore maps the second row lattice back to the first. The local admissibility witnesses give an integral frame representative for this map, hence an original term. These maps are mutually inverse on orbits. Genericity corresponds to zero defect at every place. There are finitely many lattice orbits in this fixed fibre. Summing (3) therefore keeps the complex sum $\sum_{[\Gamma]}\mu(\Gamma)\omega(d_0,\Gamma)$ intact. [Rational realization of the local lattices][surj] · [Orbit bijection and preservation of genericity][orbit] · [Signed vector sum][sum]

For a prescribed set $A\subseteq\Omega$ of positive-defect places, localize a lattice at all finite places. Its orbit, with this defect condition and fixed global inner datum, is counted by the product of the local lattice-orbit sums in the frame coordinates. The underlying patching uses rational approximation in the unipotent group and the fact that a full lattice is determined by its completions. Relative stabilizer indices multiply, and the phase is a product by (4). Almost all local factors equal $1$. Outside the chosen finite set $P$ the remaining factors can contribute a common complex number $\kappa$ of modulus one. It is independent of $A$ since outside $P$ every permitted orbit has zero defect. Summing over nonempty $A$ gives, up to that one common phase, exactly $\prod_p(Z_p+N_p)-\prod_p Z_p$. The coordinate changes identifying the local datum over the actual term preserve each of the two partial amplitudes. [Rational lattice orbits and products][product] · [One common phase for all defect sets][kappa] · [Transport to the two local amplitudes][actual]

It remains to convert the sum over $(c,\nu)$ into an actual local measure. For each attained tuple $d$, its preimage satisfies the exact identity
$$
             \sum_{(c,\nu)\mapsto d} w_{t(c,\nu)}^2
                         = V_0\prod_{p\in P} w_p(d_p).              \tag{6}
$$
Extend $d$ by the reference data outside $P$. Fixing this completed local genus, its rational classes are the orbits of the rational pointwise frame-fixing group, with inverse orders of the rational stabilizers. Unfolding one such orbit into the two row lattices and the relative double coset yields the sum of the original squared weights $w_{\Lambda}w_{\Lambda'}$ over its distinct row and normal-label keys. The key determines $(c,\nu)$ in this genus and conversely. Local closure of genericity and nongenericity ensures that when the tuple is attained this unfolding covers the entire genus of inner data required for the weight computation. In the restricted product of the local complement groups the finite-place stabilizers at $d$ and the reference tuple are commensurable open compact subgroups, equal almost everywhere in the reference coordinates. Passing through their intersection multiplies the inverse-stabilizer mass by the ratio of reference to new compact volume. The product of these ratios is $\prod_{p\in P}w_p(d_p)$, and the reference mass $V_0$ is positive. This proves (6) for attained tuples, which is exactly the support needed in (1). Squaring (3), using the common-phase calculation and substituting (6) proves (1). [Row and normal-label keys in a fixed genus][keys] · [Unfolding by rational stabilizers][stab] · [Restricted-product index calculation][index] · [Attained-tuple formula][weights]

## A bound retaining the mixed local moments

Use the inner product $\langle A,B\rangle_p=\sum_{d_p}w_p(d_p)\overline{A(d_p)}B(d_p)$, linear in the second argument. Enlarge the sum in (1) to all local tuples, using nonnegativity of its squared summand. When the two local squared norms are finite this gives
$$
 \frac{\sum_{c,\nu}\|V(c,w,\nu)\|^2}{V_0J_2(w)}
 \ \le\ \prod_{p\in P}\|Z_p+N_p\|_p^2
   -2\Re\prod_{p\in P}\langle Z_p,Z_p+N_p\rangle_p
   +\prod_{p\in P}\|Z_p\|_p^2 .                                   \tag{7}
$$
Here $J_2(w)>0$. The right side is the squared norm of the difference of two pure tensors. Expanding that one square proves the formula, with absolute convergence of the mixed products by Cauchy–Schwarz. Equality holds whenever the tuples omitted from (1) have vanishing product difference. Formula (7) retains the local mixed phase correlations even when neither of the two factors in the subtraction is small.

For an upper bound using the known local estimates, expand the tensor difference over nonempty subsets and apply the triangle inequality to those tensors. The [fixed-image-index bound](SPECTRAL_COMPLEMENT_KERNEL_COUNTS.md#the-finite-product-with-class-normalization) gives, for $k\ge60$, $f\le k$ and the stated standing rank hypotheses,
$$
  \sum_{c,\nu}\|V(c,w,\nu)\|^2
  \le J_2(w)\,9\cdot 2^{32} f^2\,2^{-(k+1)}
       H(w)^{2+\max(2r(r+1),2m)} n_{\rm gen}(w).                  \tag{8}
$$
The generic mass $n_{\rm gen}(w)$ already contains $V_0$. To obtain (8), a positive-defect place contributes at most $2^{16}q_p^{-(k+1)/2}$ in addition to the common norm bound, while zero-defect places use just the common bound. Multiplying the common factors and summing the nonempty products is the Euler-factor calculation in the linked estimate. Equation (8) is the signed finite-place saving on the actual class vectors for each block point. The global signed corank-one estimate still combines different points and normal labels within each class. The [reciprocal point-weight sum](SPECTRAL_CORANK_ONE_RECIPROCAL_SUM.md) now absorbs all the occurring normal labels for each fixed partner class. The generic-mass comparison and the weighted sum of the pinned real-orbital energy still enter in the original dimension and measure normalization. The mixed-word generic scalar main term also requires the sharp archimedean sampling comparison. [Global weighted point summation](SPECTRAL_POSITIVE_DEFECT_ENERGY.md#global-finite-product-and-corank-one-energy) · [Scalar main-term normalization](SPECTRAL_SCALAR_ROW_MASS.md)

[freeroots]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Formalism/LocalToGlobal/SiegelLatticeTheory/ClosedLocalOrbits/RealObj.lean#L357-L365
[jscale]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AbelianVarietyTheory/Proofs/FlagMeasures/FamilyGroupSumFactorsRowWeightAmplitudeProof.lean#L143-L180
[family]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AbelianVarietyTheory/Proofs/FlagMeasures/FamilyLocalObjectsExistAtTermsProof.lean#L17-L30
[rowvector]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Formalism/LocalToGlobal/SiegelLatticeTheory/ClosedLocalOrbits/TermOp.lean#L341-L355
[gframes]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AbelianVarietyTheory/Definitions/SemilocalFrames/GFrames.lean#L92-L119
[oper]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AbelianVarietyTheory/Proofs/FlagMeasures/RowTermAmplitudeEqMassMulPhase.lean#L67-L108
[character]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Formalism/LocalToGlobal/SiegelLatticeTheory/ClosedLocalOrbits/PairVal.lean#L77-L84
[lifts]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AbelianVarietyTheory/Proofs/FlagMeasures/MovedTermLatticeIsGlobalTermPhase.lean#L52-L93
[phase]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AbelianVarietyTheory/Proofs/FlagMeasures/MovedTermLatticeIsGlobalTermPhase.lean#L95-L134
[move]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AbelianVarietyTheory/Proofs/FlagMeasures/HermitianDoubleCosetMoveTermWeightCharacter.lean#L79-L112
[movep]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AbelianVarietyTheory/Proofs/FlagMeasures/HermitianDoubleCosetMoveTermWeightCharacter.lean#L113-L141
[surj]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AbelianVarietyTheory/Proofs/FlagMeasures/ExistsTermOfGlobalTermStrongApprox.lean#L170-L205
[orbit]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AbelianVarietyTheory/Proofs/FlagMeasures/RowDoubleCosetSumNormSqBound.lean#L64-L109
[sum]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AbelianVarietyTheory/Proofs/FlagMeasures/RowDoubleCosetSumNormSqBound.lean#L175-L227
[product]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AbelianVarietyTheory/Proofs/FlagMeasures/HermitianAmplitudeMassProductStructure.lean#L96-L155
[kappa]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AbelianVarietyTheory/Proofs/FlagMeasures/AmplitudeExpansionOverFinitePlaces.lean#L82-L135
[actual]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AbelianVarietyTheory/Proofs/FlagMeasures/GlobalAmplitudeEqLocalAmplitudes.lean#L34-L76
[keys]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AbelianVarietyTheory/Proofs/FlagMeasures/RowWeightsLocalOrbitsSumEqGenusMass.lean#L120-L187
[stab]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AbelianVarietyTheory/Proofs/FlagMeasures/UnfoldingGenusWeightsSumToMass.lean#L28-L74
[index]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AbelianVarietyTheory/Proofs/FlagMeasures/MassGenusLocalDataProductLocalWeights.lean#L26-L55
[weights]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AbelianVarietyTheory/Proofs/FlagMeasures/UnfoldingIdentityMatchedFamilyClosedTerms.lean#L149-L182
[jdef]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Formalism/LocalToGlobal/SiegelLatticeTheory/CokernelGLCounts/NGData.lean#L29-L44
