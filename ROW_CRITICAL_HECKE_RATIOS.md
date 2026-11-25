# Critical Hecke ratios for the bottom row

Fix a Hida grid, a square $(i,j)$, its reference tuple $t_0$, and its other allowed tuples $t$. Write $E$ for the host CM field. Let $L_t$ be the analytic continuation of the finite Hecke Euler product for the character $\nu_{ij,t}$. Then
$$
 \frac{L_t(s)}{L_{t_0}(s)}\in\overline{\mathbf Q}^{\,\times}
 \qquad\bigl(1\le s\le \mathrm{bigN}(D)+1,\quad s\in\mathbf Z\bigr).
$$
One number field contains these ratios for **all** squares, tuples and indicated integers of this grid. This proves the assertion called `NFRatio`. Membership in the image of a prescribed coefficient embedding is addressed in the [field construction](ROW_COEFFICIENT_FIELD.md). [Exact ratio field clause][field] · [Normal-form quantifiers][nf]

## Identifying the characters and their critical integers

At an unramified place $v$ the local factor of $L_t(s)$ is $(1-\nu_{ij,t}(\varpi_v)(Nv)^{-s})^{-1}$. At a ramified place it is $1$. The definition specifies this product for $\Re s>1$ and requires an entire continuation. Two witnesses agree on this half-plane, hence everywhere. The completion used in the functional equation includes the archimedean factors, and depending on convention a conductor factor. This distinction matters since the conductor can vary with the twist. [Euler factors and analytic condition][finite]

For this square $\nu_{ij,t}=\nu_{ij,t_0}\xi_t$, where $\xi_t$ has finite order. Finite order gives a trivial restriction to each connected archimedean factor. The grid assigns a CM type and, for every embedding $\tau$ in it, a positive integer $m_\tau$. The weight calculation gives
$$
 m_\tau=\kappa_\tau(s)+s,\qquad \kappa_\tau(s)>0
 \quad (0\le s\le\mathrm{bigN}(D)+1).
$$
The right side is independent of $s$. In the source convention the angular exponent is $2m_\tau$. Thus the archimedean monomial is $(z/|z|)^{2m_\tau}=z^{m_\tau}\bar z^{-m_\tau}$. The character identity stated on diagonal $E^\times$ gives the same identity on $(E\otimes_{\mathbf Q}\mathbf R)^\times$ by weak approximation and continuity. In particular all the twists are algebraic Hecke characters of weight zero with the same regular infinity type. Their complex gamma factors for the criticality test have arguments $s+m_\tau$ and $1-s+m_\tau$ on the dual side. Both are positive throughout the indicated positive interval. This checks criticality at the actual unshifted integer of the finite Euler product. [Weight and finite twist][weight] · [Archimedean convention and gamma factor][inf]

## Cancellation of CM periods

Write $d=[E^+:\mathbf Q]$. At the distinguished complex embedding, Blasius's theorem gives, up to a nonzero algebraic factor at a nonzero critical value,
$$
 L_t(s)\ \sim_{\overline{\mathbf Q}}\ (2\pi i)^{sd}\,
          p(\check\nu_{ij,t},\Phi_\nu),\qquad \check\nu=(\nu^c)^{-1}.
$$
Here $\Phi_\nu$ is the compatible CM type determined by the infinity type, hence it is common to every $t$. Any common discriminant normalization is algebraic. For the required values $s>1$ nonvanishing follows by absolute convergence of the unitary Euler product. At $s=1$ use the classical nonvanishing theorem for unitary Hecke characters on the line $\Re s=1$. The nonzero angular exponents here exclude a norm power and hence its pole. These checks apply also to the reference tuple. [Blasius, *On the critical values of Hecke L-series*](https://annals.math.princeton.edu/1986/124/p02) · [Lin, §2.1, Theorem 2.1 and Remark 2.3][lin] · [Nonvanishing on the grid][nonzero]

For a fixed CM type the class of the period in $\mathbf C^\times/\overline{\mathbf Q}^{\,\times}$ is multiplicative in the character. This follows by tensoring the rank-one rational structures and their comparison, equivalently by pullback along the diagonal of the CM torus. For a finite-order character $\eta$ of order $N$, the $N$-th power of its period class is therefore the class of the trivial character, which is $1$. A complex number whose $N$-th power is nonzero algebraic is itself nonzero algebraic. One can also see this by trivializing the weight-zero Artin character over its finite splitting field. Apply this to $\check\xi_t$. Dividing the two critical-value formulas cancels the power of $2\pi i$ and the reference CM period. The remaining factor is algebraic. Finally the character family, the square index set and the interval of $s$ are finite, so adjoining all these quotients gives a number field. This supplies the qualitative field assertion for which the pinned row-test assembly invokes toric conjugacy. The integral and valuation assertions elsewhere in the reconstruction keep their own hypotheses. [CM-period functoriality, Proposition 2.2 and its diagonal-map proof][lin] · [Use in the row-test field][join] · [Use of that field in the row test][test]

## The longer nonvanishing interval for the square tower

The tower requires $L_t(s)\ne0$ also for $1-e_0\le s\le0$, with $e_0$ the bottom half-rank difference. The grid inequalities give $e_0\le\mathrm{halfRank}$ and $m_\tau>\mathrm{halfRank}$ by evaluating $\kappa_\tau(s)+s$ at the half-rank. Hence $s+m_\tau>0$ throughout this interval. The dual value is taken at $1-s\ge1$, where Hecke nonvanishing applies, and its gamma arguments $1-s+m_\tau$ are positive. Gamma factors, conductor powers and the root number are all nonzero. The Hecke functional equation now gives $L_t(s)\ne0$. The auxiliary untwisted characters indexed by the tower have the same positive angular weights, giving their required nonvanishing at every positive integer. This supplies both parts of the tower input `LNe` on its field-data range. [Exact interval, rank comparison and auxiliary family][tower] · [Use of the functional equation at nonpositive integers][nonzero]

[field]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AbelianVarietyTheory/Definitions/TwistedInnerProducts/MemHalfCosetSelf.lean#L194-L201
[nf]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AbelianVarietyTheory/Definitions/TwistedInnerProducts/TwistPlacesOffPrimeQZero.lean#L81-L96
[finite]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AbelianVarietyTheory/Definitions/Divisors/EntireEqOfHalfPlane.lean#L45-L58
[weight]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AbelianVarietyTheory/Proofs/TwistedOperators/NormalFormToricRatio.lean#L37-L111
[inf]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AbelianVarietyTheory/Definitions/Divisors/IsFinSetSplitPlacesCoprimeConductor.lean#L34-L46
[nonzero]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AbelianVarietyTheory/Proofs/DivisorProofs/SquareBottomHalfRankDiffLeHalfRank.lean#L84-L126
[tower]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AbelianVarietyTheory/Proofs/DivisorProofs/SquareBottomHalfRankDiffLeHalfRank.lean#L132-L180
[lin]: https://www.ihes.fr/~linjie/IHES/Francais_files/Factorization%20of%20arithmetic%20automorphic%20periods.pdf
[join]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AutomorphicArithmetic/ThetaCorrespondence/ThetaPairLifts/LocalTypeDictionary/ThetaLiftExtensionFieldExists.lean#L23-L40
[test]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AutomorphicArithmetic/ThetaCorrespondence/ThetaPairLifts/LocalTypeDictionary/TestVectorAtDatumOfJoin.lean#L20-L32
