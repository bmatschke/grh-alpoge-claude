# Reading the level-prime correction on the selected arithmetic column

Fix a linked arithmetic member, a word $u$, and an even $j$ with $j+4\le m$. Write $R_j=\operatorname{rank}X_j$. Use the original word's integral definite frames, live twist charts, row lifts and Weil characters. For the bundle transfer, the original hypotheses are its linkage to a witnessed bundle, the pointwise row data and the existence of the marked real readings. In particular the pointwise row data include the row join, the real frames, the primitive rows, and the signature and node gaps. The pointwise supplier constructs these on the eventual linked members under its listed representation and size inputs. Equality of the full bundle transports them to the selected member. Given them, the geometric data and the following correction are constructed for **every** $u$ in that member. This needs no identification between an independently chosen geometric word and the arithmetic word. [Pointwise row construction][aw-pt] · [Whole-bundle equality][aw-link] · [Extraction of the word and its charts][aw-geo]

Write $\operatorname{rd}_{t,j,\alpha,y}$ for the scalar automorphic reading of the arithmetic column at the chart $\alpha$ and jet $y$. At every registered level place let $S_{p,j,\varepsilon_p}$ be its finite Fourier/sign operator on ramified scalar forms. For a tuple $t$ let $S'_{t,j,\varepsilon}$ be the operator on the word's arithmetic columns chosen by the construction. On its ramified columns supported on the retained charts one has the exact identity of automorphic functions

$$
 \operatorname{rd}_{t,j,\alpha,y}(S'_{t,j,\varepsilon}\phi)
     =\left(\prod_{p\mid T}^{\rm ordered}
                  S_{p,j,\varepsilon_p}\right)
        \operatorname{rd}_{t,j,\alpha,y}(\phi).
 \tag{A}
$$

Here the product ranges over the registered split places, in their recorded order. The finite Heisenberg operation defining an arithmetic edge acts on its theta test by the composition $d^Q_{t,j,\alpha\gamma}\circ d^G_j\circ d^T_j$, with the word's rescaled $d^Q$. Both equations are identities of actions on the indicated spaces. They fix the normalization even when a particular period or chart entry is zero. [Arithmetic correction and readings][aw-read] · [Three operators and chart phases][aw-three] · [Installation in the assembled column][aw-col]

To see (A), express the ordered product as a finite sum of right translates supported at level places. Each local operation preserves the ramified space at its place. Operations at the other places preserve that condition by disjoint support. The transformed scalar forms are therefore invariant under the stabilizer of each marked lattice pair. The arithmetic finite translation action lifts the sum to an arithmetic column with exactly these readings. A zero reading in an omitted chart remains zero under the finite sum. Evaluating at the identity frame recovers the individual arithmetic coefficient and proves the vanishing on omitted classes. This proves (A) on the ramified live-chart space. The existence statement about arithmetic representatives needs no canonical action on the complement of this space. The original constructor selects the level and fixed-type data on the common frames, forms the corrected column using those choices, installs (A), and then applies the finite integral laws. Thus one may choose the explicit $c_{T,t,j,p}$ and $c_{G,j}$ of [the finite-factor calculation](PERIOD_INTERIOR_FINITE_FACTORS.md) in that construction. If a word is presented only by an abstract existential witness its bare scalar still need not equal that representative. [Local translations and lift][aw-lift] · [Omitted classes][aw-zero] · [Order of choices][aw-choice] · [Use on the same finite integrals][aw-install]

## The common operator and its exact norm at the bottom

Let $q$ be the residue cardinality of the local field in the word's split level charts, and let $h$ be the length of their recorded list. The list has no repetitions in this application. For a nonempty bottom jet fibre the source realizes each choice of signs $\varepsilon$ by a single linear equivalence $A_\varepsilon$ of the native bottom type $\mu_u$. For every tuple $t$ its correction satisfies

$$
 S'_{t,0,\varepsilon}\operatorname{col}_{t,0}(v)
     =\operatorname{col}_{t,0}(A_\varepsilon v),\qquad
 \langle A_\varepsilon v,A_\varepsilon w\rangle
        =q^{h R_0}\langle v,w\rangle.
 \tag{B}
$$

The finite Fourier sum at one place multiplies the squared inner product on ramified vectors by $q^{R_0}$ in the prescribed unnormalized convention. Applying the places successively gives $q^{h R_0}$. Reading at one bottom jet compares the scalar-form and bottom-type inner products by the same positive constant on both sides, which cancels. Polarization gives linearity and the norm identity gives injectivity, hence bijectivity on the finite-dimensional bottom type. At the reference tuple this constructs $A_\varepsilon$. For each other tuple the arithmetic reading is intertwined by (A), and injectivity of the bottom chart reading proves the first equality of (B) on the word's bottom space. If the bottom jet fibre is empty the source takes the identity, with scale one. [Inner-product and norm calculation][aw-norm] · [Injectivity and comparison for every tuple][aw-unif]

There is a resulting explicit normalization for any $n$ consecutive corrected pairs starting at stage zero, $2n\le m$. A correction at level $j+1$ moved past a definite lift to level $j$ contributes $q^{h(R_{j+1}-R_j)/2}$, independent of the tuple and the sign. The two opposite powers of the unramified splitting character cancel in this commutation. At the $i$th pair, $0\le i<n$, the new correction moves through exactly $2i$ earlier edges. Consequently the scalar multiplying the ordinary $2n$-edge column with transformed bottom input equals

$$
 c_S(n)=\prod_{i=0}^{n-1}\prod_{j=0}^{2i-1}q^{h(R_{j+1}-R_j)/2}
        =q^{\frac h2(\sum_{i=0}^{n-1}R_{2i}-nR_0)}.
 \tag{C}
$$

The transformed bottom input is $(A_{\varepsilon_{2n-2}}\cdots A_{\varepsilon_0})v$. By (B) the composite has norm scale $q^{hnR_0/2}$ on a nonempty bottom jet fibre. Thus the product of the scalar in (C) and the composite norm scale is exactly $q^{(h/2)\sum_{i<n}R_{2i}}$. The same bottom transformation serves every tuple. The iterated equality holds on every retained reading. At $2n=m$ the terminal pairing takes the same scalar by the tail reading law. These powers measure the cost of commuting level corrections down the chain. The level factor in the individual two-column period still appears with the twist, fixed-type, base-move and quotient-volume factors from the interior calculation. Nonvanishing of the bottom Bessel functional on the required spectral projection remains an independent input. [Edge scalar and its iterated definition][aw-edge] · [Cancellation of the two characters][aw-cancel] · [Every stage and terminal reading][aw-chain]

[aw-pt]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AbelianVarietyTheory/Proofs/DecoratedLatticeProofs/RowsOfRepresentationTheoryOfHyp.lean#L204-L228
[aw-link]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AbelianVarietyTheory/Proofs/DecoratedLatticeProofs/MainTheoremPublishedResultsFinal.lean#L39-L49
[aw-geo]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AbelianVarietyTheory/Proofs/DecoratedLatticeProofs/AllTrueFamilyDatum.lean#L128-L172
[aw-read]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AbelianVarietyTheory/Proofs/DecoratedLatticeProofs/TrueGeometryJointTwistRelation.lean#L12-L41
[aw-three]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AbelianVarietyTheory/Proofs/DecoratedLatticeProofs/TrueGeometryFamilyInvariance.lean#L58-L94
[aw-col]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AbelianVarietyTheory/Proofs/DecoratedLatticeProofs/TrueGeometryFamilyInvariance.lean#L219-L235
[aw-lift]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AbelianVarietyTheory/Proofs/DecoratedLatticeProofs/LevelPrimeOperatorsActOnRamifiedColumns.lean#L80-L107
[aw-zero]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AbelianVarietyTheory/Proofs/DecoratedLatticeProofs/LevelPrimeOperatorsActRamifiedColumnsVanishing.lean#L44-L69
[aw-choice]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AbelianVarietyTheory/Proofs/DecoratedLatticeProofs/TrueGeometryFamilyColumnData.lean#L49-L61
[aw-install]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AbelianVarietyTheory/Proofs/DecoratedLatticeProofs/TrueGeometryFamilyColumnData.lean#L83-L131
[aw-norm]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AbelianVarietyTheory/Proofs/DecoratedLatticeProofs/LevelPrimeOperatorsStepZeroScaleNorms.lean#L208-L249
[aw-unif]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AbelianVarietyTheory/Proofs/DecoratedLatticeProofs/TypeDataUnitShiftRelation.lean#L128-L168
[aw-edge]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AbelianVarietyTheory/Definitions/LatticeFrames/TailRd.lean#L32-L49
[aw-cancel]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AbelianVarietyTheory/Proofs/DecoratedLatticeProofs/DefiniteLiftCommLevelPrimeOperators.lean#L175-L195
[aw-chain]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AbelianVarietyTheory/Proofs/DecoratedLatticeProofs/SeeSawKernelChainLevelPrimeOperatorToStepZero.lean#L139-L184
