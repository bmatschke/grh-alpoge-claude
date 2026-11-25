# Period heights on the original selected family

**Edition 0.88 · 25 November 2026**

Three of the nine entries in the original period-height estimate now have human proofs on one eventual range of the selected family. They give the large-prime support cutoff (entry 3), the full rational row lattice (entry 5), and the weighted error bound (entry 8). The rationality clause of the Bessel identity (entry 4) also holds. The original global denominator bound was completed in edition 0.87. **Nine whole obligations remain open**, all shared by RH and unrestricted Dirichlet GRH. [Period-height supplement (PDF)](RH_new_proofs_v0_88.pdf) · [Denominator supplement (PDF)](RH_new_proofs_v0_87.pdf) · [Cumulative manuscript source](RH_readable_reconstruction_v0_88.tex)

## The weighted error, including its two main contributions

Fix an allowed design family, a word $u$, and a lift $j$ at one of its late members. Let $E_{u,j,w}$ be its stored error at a finite place $w$ of the coefficient field $K$, let $e_w$ be its ramification index, and put $\ell_w=\log(\mathrm Nw)/[K:\mathbf Q]$. The estimate is

$$
\left|\sum_{w\in L.\mathrm{supp}}2\ell_we_w E_{u,j,w}
-\left(\sum_{s\in TT}a_s\right)\log(g_0g_1)\right|
\le C B_0,\qquad B_0=fmbx^\epsilon .
$$

The quantities $a_s$ are the distinguished weights on the member and $g_0,g_1$ are its two type primes. The same $C$ and starting scale work for every word and every lift at every subsequent member of the family. The proof works for $0<\epsilon<1/52$. Taking the outer endpoint $\epsilon_1=1/53$ gives the closed-family quantifier, which includes its upper endpoint. [Statement and quantifiers](continuation_v88/period.tex)

At each $g\in\{g_0,g_1\}$, conjugation pairs local valuations of a generator with $y\bar y=g$. Summing them gives half of $\log g$ for $y$. This identifies the exact weighted contribution at that prime. Subtracting the Fock degree from the sum of the row exponents leaves $\sum_{s\in TT}a_s$ up to the degree-count error. The top embeddings contribute the distinguished weights; the other coordinates are controlled by the original weight windows. This establishes the degree estimate with constant 40. The two prime fibres together give the main term in the display. [Valuation identity](continuation_v87/periodnext.tex) · [Degree and type-prime estimates](continuation_v88/errors.tex)

Away from these primes, the level-prime contribution uses exactly half the logarithmic mass at the places where the level character is seen. The stabilizer contributes at most $2\log D_{\Gamma,u}$, and cancelling the largest top row before taking the ramified supremum gives the ramified constant 4. For the remaining prime sum the two corrections give constants $18(1+1/\epsilon)$ and $848$. In the sparse term a nonzero Frobenius label of odd order forces $p\equiv\pm1\pmod{4M}$ in the real two-power cyclotomic quotient. This controls the term weighted by $\log p/p^3$ even after multiplication by the rank parameter. Adding the contributions gives the stated family bound. [Prime sums](continuation_v88/inert.tex) · [Constants and assembly](continuation_v88/errors.tex)

## Full lattice rank and rational Bessel values

At each tuple that occurs on the selected member, the positive down-up identity maps the good quotient onto the common row space. The separating rational functionals give a matrix of full column rank. An invertible minor expresses the change of row coordinates over the original coefficient field. Clearing denominators produces independent vectors of the integral row set at that tuple. The rational span of the global lattice is the intersection of these tuple spans. Along with the finite generation from B87H1, this proves fullness at both the sharp and base levels. [Tuple comparison and full rank](continuation_v88/rows.tex) · [Intersection of rational spans](continuation_v87/periodbessel.tex)

The same linked object carries the law for the recorded rational map $Bk$. Projecting away the base kernel with its rational Hermitian Gram matrix identifies the actual period on rational inputs. The norm extension's law then identifies this value with $Bk$ under the prescribed embedding. This proves the rationality clause of entry 4 for every word. The other clause asks for one unitary change of target coordinates, shared by all words, together with a nonzero scalar and a unitary source change for each word. [Rational pairing](continuation_v88/rows.tex) · [Finite test for a common unitary](continuation_v87/periodbessel.tex)

## What remains in GLOBAL_PERIOD_HEIGHT

| Entry of the original estimate | Status after this edition |
| --- | --- |
| 1, 2 | The integral image of the period map and the frame-size bound remain to be established on this family. |
| 3 | The support cutoff holds uniformly for all members past the starting scale. |
| 4 | Rationality holds. The common unitary comparison of the complex pairings remains open. |
| 5 | The sharp row lattice is full. The proof also gives the corresponding base statement. |
| 6, 7 | The bound on the height of each nonzero map and the upper bound for each word height remain. |
| 8 | The full weighted error inequality holds for all words and lifts. |
| 9 | The comparison of the corrected heights of two arbitrary words remains. |

For entry 4, the source's kernel-join theorem also asks for finite dimensionality of the spectral realization, a compatible identification of the real and spectral models, and the exact mixed-period identity. Its base-image surjectivity hypothesis is supplied by the tuple argument above. The mixed-period identity must compare all pairings at the same normalization. [Kernel-join theorem](https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AutomorphicArithmetic/ThetaCorrespondence/ThetaPairLifts/ThirdPlaceSeries/AdmissibleOfTransported.lean#L59-L61) · [Mixed-period hypothesis](https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Formalism/LocalToGlobal/IndefiniteReal/IsometricPeriodsOfHypotheses.lean#L80-L105) · [All nine entries](https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Formalism/SharpRestriction/GlobalTheoremInputs.lean#L77-L95)

## Verification

This edition adds **12 claims**, bringing the human reconstruction to **4,848**. The verifier checks 115 source ranges in 57 pinned Lean files, the proof text and dependencies, and preservation of all nine outstanding contracts and the preceding denominator result. Both readers were compiled. No fresh Lean replay was performed. [Checkpoint](CURRENT_CHECKPOINT_v0_88.json) · [Claim ledger](continuation_v88/claims.json) · [Obligation graph](continuation_v88/obligations.json) · [Validation record](continuation_v88/validation.json)
