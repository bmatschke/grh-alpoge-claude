# The split coupling kernel at the last pair

At the last pair of a split finite chart the Bessel index is zero. One column $y$ of the first test remains, and its Fourier dual $\eta$ becomes the distinguished row of the upper terminal matrix. Let $k$ be the local field, $O$ its integers, $q$ its residue cardinality, $\pi$ its uniformizer and $d=\# X(s+1)$ the number of entries of $y$. Use the original character of conductor $O$ and the additive measure giving $O$ volume one. Write $X,Z$ for the other matrix coordinates and $\Phi_{\rm top}(Z)$ for the top test with its empty column block appended. At the starting chart $\alpha$, write $\Psi_\alpha(X,y)$ for the prescribed translated penultimate test on the matrix obtained by adjoining $y$ to $X$. The scalar two-variable kernel, before applying the common local model map, is
$$
 K_\alpha(X,Z,\eta)=\Phi_{\rm top}(Z)
        \int_{k^d}\Psi_\alpha(X,y)\psi(-\eta\cdot y)\,dy . \tag{1}
$$
With Bessel index zero the first flat map has no free entries to integrate, so it is exactly column reindexing. The second Witt extension has a zero-dimensional block and restricts the test by appending empty columns. The remaining line map takes the Fourier transform in $y$ with parameter $-1$, and orthogonal addition of the terminal summands multiplies by the upper test. On the unmodified integral indicators the transform of $\mathbf1_{O^d}$ equals $\mathbf1_{O^d}$, fixing the normalization. [Rank-zero flat map and extension][flat] · [Native entries and Fourier sign][shape] · [Application in the local model][ker]

At a marked symmetric fixed-level place put $y_*=\pi^{-1}e_*$, with the star at the distinguished auxiliary coordinate of the original common frame. On the identity chart,
$$
 K_1(X,Z,\eta)=
 \Psi_1(X,y_*)\,\Phi_{\rm top}(Z)\,
    \psi(-\eta_*/\pi)\,\mathbf1_{O^d}(\eta).                 \tag{2}
$$
The penultimate frame presents the last column as $\pi y$. The marked level pattern requires that column to have residue $e_*$: its constrained off-diagonal entries are zero modulo $\pi$, its diagonal entry is one, and the added lower rows have zero residue. Replacing $y$ by $y+z$ for $z\in O^d$ changes the framed column by entries in $\pi O$, under which the marked tame test is invariant. Hence $\Psi_1(X,y)$ is $\Psi_1(X,y_*)$ times the indicator of $y_*+O^d$, also for $X$ at which it vanishes identically. Translating (1) gives (2). At integral $\eta$ its phase depends only on $\eta_*$ modulo $\pi O$. For $\eta\notin O^d$, translation by an element of $O^d$ on which $\psi(-\eta\cdot z)$ is nontrivial kills the integral. [Distinguished index and box][base] · [Original pattern and invariance][pattern] · [Application to the fixed tests][fixed]

At a split twist place use the actual boxes $M=c_2O^d$, $S=c_1O^d$ of the adapted chain. Set $L=S+M$. Adaptation gives support in $S$ and invariance under $M$. Let $R=L/M$ and $C=M^\perp/L^\perp$, with $(cO^d)^\perp=c^{-1}O^d$. Put $A_{\alpha,b}(X)=\Psi_\alpha(X,\tilde b)$ for $b\in R$ and any representative $\tilde b$. The source's coupling index consists of the classes attained by some chart and $X$ with nonzero $A_{\alpha,b}(X)$. Every other coefficient vanishes. Integrating by cosets in (1) gives
$$
 K_\alpha(X,Z,\eta)=
 \Phi_{\rm top}(Z)\,q^{-d\,\mathrm{ord}(c_2)}
 \mathbf1_{M^\perp}(\eta)
 \sum_{b\in R} A_{\alpha,b}(X)\psi(-\eta\cdot\tilde b).       \tag{3}
$$
The rational coefficient is $\operatorname{vol}(M)$. Off the annihilator the integrals vanish by translation in $M$. On the annihilator the phase is independent of the representative. The formula retains the scalars in the prescribed translated test. [Definitions and adaptation][shape] · [Finite sum for the original twist-place test][twist]

The Fourier test in (3) can be inverted before applying the local model map. For each $b_0\in R$,
$$
 \frac{1}{|R|}\sum_{\bar\eta\in C}
          \psi(\eta\cdot\tilde b_0)K_\alpha(X,Z,\eta)
   =\operatorname{vol}(M)\Phi_{\rm top}(Z)A_{\alpha,b_0}(X). \tag{4}
$$
The summand is independent of the frequency representative, since $L^\perp$ kills $L$. The conductor and the coordinate dot product give a perfect pairing of $L/M$ with $M^\perp/L^\perp$. In fact, writing $L=\pi^aO^d$ and $M=\pi^bO^d$ with $a\le b$, both groups have order $q^{d(b-a)}$, and an element pairing trivially with $M^\perp$ belongs to $M$. Finite character orthogonality in (3) proves (4), also when the top test or a coupling coefficient vanishes. At several split places the formulas tensor by product Haar measure.

These formulas evaluate the last split local Schwartz kernel in the specified charts. Identifying the resulting global periods still requires the actual two-lift identity and matching of the row and column data. The local-model map need not preserve the information recovered in (4). [Native assembly at all twist places][all] · [Last two-step transfer][last]

[flat]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AbelianVarietyTheory/Proofs/DecoratedLatticeProofs/SeeSawLastTwoStepsValueFixedLevelPlaces.lean#L40-L148
[shape]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AbelianVarietyTheory/Definitions/TwistedInnerProducts/StandardOrderExtendedBasisApplyLowBlock.lean#L788-L921
[ker]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AbelianVarietyTheory/Proofs/DecoratedLatticeProofs/IntIndFromCols.lean#L170-L221
[base]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AbelianVarietyTheory/Definitions/LatticeFrames/OnesRepresent.lean#L49-L62
[pattern]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AbelianVarietyTheory/Proofs/DecoratedLatticeProofs/SymmetricChainOneCouplingCosetOfPattern.lean#L76-L174
[fixed]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AbelianVarietyTheory/Proofs/DecoratedLatticeProofs/SeeSawLastTwoStepsValueFixedLevelPlaces.lean#L166-L234
[twist]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AbelianVarietyTheory/Proofs/DecoratedLatticeProofs/LastStepsKernelEqSumCouplingCosets.lean#L30-L112
[all]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AbelianVarietyTheory/Proofs/DecoratedLatticeProofs/SeeSawLastTwoStepsAllTwistPlaces.lean#L331-L448
[last]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AbelianVarietyTheory/Proofs/DecoratedLatticeProofs/SeeSawLastTwoStepsTransportLinearRelations.lean#L92-L137
