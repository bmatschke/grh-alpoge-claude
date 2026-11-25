# Exact scalar of the marked split symmetric contraction

Fix one of the original split symmetric-position local chains. Let the local field have residue cardinality $q$, ring of integers $O$ and uniformizer $\pi$. The additive character has conductor $O$ and the additive Haar measure gives $O$ volume one. Write $2\rho+1$ for the original number of ordered auxiliary lines, $\kappa$ for the original middle rank, and $d$ for the size of the additional index set appended at each step. At level $h$ put
$$
 n_h=\kappa+h(1+d),\qquad c_h=2\rho+1-h,\qquad
 u_h=\max(c_h-1,0),\qquad b_h=\kappa\min(\rho,u_h)+h(1+d)u_h .
$$
In a double step $j,j+1$, write $c=2r$ for the source's symmetric parameter, so $j+c+2=2\rho$, $c_{j+1}=2r+2$ and $c_{j+2}=2r+1$. The scalar multiplying the product of the two original **normalized identity entries** in the contracted kernel is exactly
$$
       q^{-b_{j+1}-b_{j+2}
                -\binom{r+2}{2}(n_j+n_{j+1})
                -\binom{r+1}{2}(n_{j+1}+n_{j+2})}.                \tag{1}
$$
This identifies even the two single-test normalizations left in the [Fourier contraction calculation](REMARK_SEESAW.md), using the actual tame test, its frame pattern and the original unit-volume convention. The local scalar is common to tuples with these same marked tests. It has support only at the residue characteristic as a rational scalar.

### Moving the position of the root exchange

Let $E_p\Phi$ denote the integral over free entries in the affine root-exchange matrix at position $p$, against the fixed simple-root character. For one step with middle sizes $n_j,n_{j+1}$ and each allowed $1\le p$ before the symmetric cutoff, one has
$$
     E_{p+1}\Phi=q^{-p(n_j+n_{j+1})}E_p\Phi,\qquad
     E_p\Phi=q^{-\binom p2(n_j+n_{j+1})}E_1\Phi.                 \tag{2}
$$
The argument works before any assumption that a particular point has a nonzero identity entry.

To see it, in the comparison of the two free sets set all shared entries equal and keep their simple-root additive phase. The first set, at $p+1$, adds one row of length $n_j$ with entries in $\pi^p O$. The set at $p$ instead adds one column of length $n_{j+1}$ with $\pi^{p+1}y\in\pi O$, equivalently $y\in\pi^{-p}O$. Both insertions are off the simple-root character slots. In either case the integrand is the common integrand at zero insertion times the indicator of the displayed box. Here the closed bound on the row and the strict congruence on the scaled column have different origins. The scaled row must be integral on the support of the type test. Conversely adding an allowed row leaves the type class and the tame determinant character unchanged: on its invertible block the addition is left multiplication by $1+e_a w g^{-1}$, with the distinguished diagonal correction in $\pi O$ by the prescribed zero positions, hence unit determinant congruent to $1$. The remaining rectangular-block congruences are unchanged. The inserted column is supported only on off-diagonal entries constrained to be zero modulo $\pi$ in the symmetric level pattern (or in the rectangular block of the test), and adding a vector zero in the entire scaled residue block fixes the test. These are the separate native row and column insertion identities. Integrating the indicators costs $q^{-pn_j}$ in the first expression and $q^{pn_{j+1}}$ in the second. The remaining integral is identical by finite-product Haar integration. Division of these two constants and iteration prove (2). [Row operation with its tame character][row] · [Column congruence][column] · [The two actual free sets and their shared integral][exchange]

### The subgroup volume in the normalized identity entry

At target level $h$ the normalized identity entry is $E_1\Phi/v_h$. Write $D_h$ for its diagonal lattice frame and $J_h$ for the actual level. The denominator $v_h$ is the relative Haar volume
$$
  v_h=\frac{\operatorname{vol}(N_1\cap J_h)}
                 {\operatorname{vol}(N_1\cap\operatorname{Stab}(D_h O^{n_h+c_h}))}
      =q^{-b_h}.                                                   \tag{3}
$$
Indeed the source uses $C_{\rm grp}=R_1\cap J_h$ at the identity; the volume takes its intersection with the unipotent radical $N_1\subset R_1$. Conjugation by $D_h$ preserves $N_1$, and its Haar scale cancels in the ratio. In standard coordinates the denominator is the integral block upper-unitriangular group. The lattice level is the inverse image of its stated residue pattern and contains the principal congruence kernel. Strictly increasing block-level entries in $N_1$ are free independent residue parameters, and all other entries are those of the identity. Thus the inverse of (3) is the index obtained by setting to zero the parameters forbidden by the level pattern. [Definition of the unipotent and its ordering][unip] · [Subgroup, volume and normalized entry][vol] · [Exact symmetric level pattern][pat]

For the count, the middle $n_h$ coordinates have block level one, and the auxiliary line with original index $a$, $0\le a<c_h$, has block level $a+1$. Every free line-to-line entry goes from a smaller to a larger line index and is permitted. A middle-to-line entry is free for $1\le a<c_h$. From an original middle coordinate it is permitted exactly when $a>\rho$, excluding $\min(\rho,u_h)$ per coordinate. The other middle coordinates are the $h$ old line indices $c_h,\dots,2\rho$ and the $hd$ appended indices. None of them has a permitted entry into an earlier old line. This excludes $u_h$ per such coordinate, proving (3), including $c_h=1$. The level pattern applies at every stage by the original reindexing and iteration. [Permutation of the old and new middle coordinates][order] · [Full membership equivalence at every iterated level][iteration]

### Applying the two flattenings

In the first single test at the double-step position the remaining column variable $y$ ranges over $L=\pi^{-(r+1)}O^{n_{j+1}}$. Its flattened value is constant in $y$ on $L$, by the strict congruence of the scaled extra column, and zero off $L$ by the off-diagonal level condition. At $y=0$ its value is $E_{r+2}\Phi_j$. Equations (2) and (3) therefore make its scalar relative to the first normalized entry
$$
      v_{j+1}q^{-\binom{r+2}{2}(n_j+n_{j+1})}.
$$
For the second test the remaining row variable lies in $L^\perp=\pi^{r+1}O^{n_{j+1}}$. Outside this box scaled integrality fails in an actual matrix entry. Inside the box the row shear belongs to the source level, has determinant one and its selected superdiagonal character is trivial. The row shear thus recovers the value at zero, $E_{r+1}\Phi_{j+1}$. Its relative scalar is $v_{j+2}q^{-\binom{r+1}{2}(n_{j+1}+n_{j+2})}$. Under the conductor and measure conventions the Fourier transform of $\mathbf1_L$ is $\operatorname{vol}(L)\mathbf1_{L^\perp}$ and $\operatorname{vol}(L)\operatorname{vol}(L^\perp)=1$. Multiplying the scalars proves (1). [Actual column range and normalization][flatc] · [Actual row level, character and normalization][flatr] · [Symmetric pair contraction][pair]

For support in the translated second target variable, use the one-step support theorem of this same chain: nonvanishing of the position-$p$ operator on the translate $h$ implies $h\in R_pJ$. For $p=r+1$, outside this double coset its position-$p$ value is zero. Only $u\in L^\perp$ enters the double-step integral. There the row shear changes the translated zero-row operator by a level character scalar: the row shear acts on the right of the test matrix and the target translate on the left, so they commute. Each integrand is consequently zero. This transfers the one-step support to the original two-step kernel. The one-step theorem here is precisely the identified symmetric-chain input. Its proof uses block Iwasawa decomposition for the translated frame, followed by the residue-pattern test for a representative in the lattice stabilizer. This assertion concerns the split symmetric test. The other local configurations, matching these kernels to the global period, and the real and terminal integrals retain their own hypotheses. [Class reduction](https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AbelianVarietyTheory/Proofs/DecoratedLatticeProofs/SymmetricLevelChainClassAtEveryPosition.lean) · [Support from the symmetric level pattern](https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AbelianVarietyTheory/Proofs/DecoratedLatticeProofs/SymmetricLevelChainSupportAtOfPattern.lean) · [One-step support on the original chain][support] · [Two-step implication including the translated shear][pair]

[row]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AbelianVarietyTheory/Proofs/DecoratedLatticeProofs/SymLevelChainTestFunctionAddRow.lean#L121-L211
[column]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AbelianVarietyTheory/Proofs/DecoratedLatticeProofs/MatrixBlockColumnVanishingStep.lean#L37-L90
[exchange]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AbelianVarietyTheory/Proofs/DecoratedLatticeProofs/SymmetricLevelChainUnfoldedPositionExchange.lean#L24-L149
[unip]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AbelianVarietyTheory/Definitions/Foundations/SimpleSum.lean#L13-L21
[vol]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AbelianVarietyTheory/Definitions/TwistedInnerProducts/StandardOrderExtendedBasisApplyLowBlock.lean#L675-L730
[order]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AbelianVarietyTheory/Definitions/TwistedInnerProducts/StandardOrderExtendedBasisApplyLowBlock.lean#L649-L672
[pat]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AbelianVarietyTheory/Definitions/LatticeFrames/OnesRepresent.lean#L31-L48
[flatc]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AbelianVarietyTheory/Proofs/DecoratedLatticeProofs/FlatColumnIndicatorPureAtSymmetricPosition.lean#L183-L224
[flatr]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AbelianVarietyTheory/Proofs/DecoratedLatticeProofs/FlatRowIndicatorOfSymLevelExchange.lean#L52-L95
[pair]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AbelianVarietyTheory/Proofs/DecoratedLatticeProofs/SymLevelDoubleStepOfFlatColumnFlatRow.lean#L251-L321
[support]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AbelianVarietyTheory/Proofs/DecoratedLatticeProofs/SymmetricLevelChainOneIndexAtOfClassSupport.lean#L12-L42
[iteration]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AbelianVarietyTheory/Proofs/DecoratedLatticeProofs/SymmetricLevelChainPatternIterated.lean#L105-L118
