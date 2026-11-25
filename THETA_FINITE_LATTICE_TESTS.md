# The finite test vectors at every twist

Once a lattice vacuum $f_0$ has been chosen, the finite test vector amounts to a function on matrices over residue fields. The interior and terminal chain steps prescribe a function detecting a flag. The definite-row lift prescribes an identity block on the conjugate half of the same split places. Their auxiliary determinant characters have opposite exponents. Finite Fourier inversion puts each of these explicit functions inside the original global theta space and fixes its value there uniquely.

**Theorem.** Fix the two Hermitian spaces $S,T$, their self-dual lattices and finite adelic frames, the real data, and a normalized vacuum $f_0$ for those data. Let $P_g$ be the marked primes and $Q$ the auxiliary primes for the tuple under consideration. Assume the disjointness and oriented split-prime condition of the source. For every choice of the prescribed residue characters the chain test and the definite-row test, with their respective level data, each determine a theta vector for their defining normalized vacuum. Every allowed model for the selected split half gives that same vector. This proves the original statements `StepVecExists` and `ThPVecExists`, whose quantifier is over **every** such vacuum. In an application the vector and the set $Q$ may vary with the tuple. [Both existence statements][exists] · [Split-prime condition for every tuple][tuple]

## A local function with a prescribed global vacuum

Write $W=\operatorname{Hom}_E(S,T)(\mathbb A_F)$ and let $B$ be the source's full alternating trace form on $W$. Write $H_w$ for the Heisenberg translation, which uses $B/2$ in its formula. Set $e=\sum_{P\in P_g\cup Q}e_P$, where $e_P$ selects the factor at $P$. The orientation condition is $e\bar e=0$. The sum is uniquely determined by the primes, since its value is one in their factors and zero in the others. The two finite spaces $X=eW$ and $Y=\bar eW$ are in perfect duality via $(x,y)\mapsto\psi(B(x,y))$. Put $L=e\Lambda$ and $L'=\bar e\Lambda$ for the completed Hom lattice $\Lambda$ with the source's fractional-ideal factor. Self-duality says that $L'$ is the annihilator of $L$, and conversely. The defining vacuum condition fixes $f_0$ under $H_l$ for $l\in L$ and $H_{l'}$ for $l'\in L'$. Indeed, decompose a vector into its single-prime summands. Translations within either isotropic half compose without phase, including at primes above 2. [Original lattice and vacuum condition][vac] · [Self-duality and single-prime decomposition][halves] · [Trace-dual lattice calculation](canonical_weil/main.tex#L30-L52)

View the Schwartz–Bruhat functions on $X$ as functions on $W$ by extension by zero. Their translations and modulations are
$$
 \tau_u\Phi(x)=\Phi(x+u),\qquad
 M_v\Phi(x)=\psi(B(x,v))\Phi(x)\qquad(u\in X,\ v\in Y).
$$
Choose representatives $u\in X/L$ and $v\in Y/L'$, with zero representing the zero classes. The functions $\tau_uM_v1_L$ form an algebraic basis. Different $u$ give disjoint supports $-u+L$. On each such coset a locally constant function is a function on $L/kL$ for some positive integer $k$. Its characters are represented by $v\in k^{-1}L'/L'$ under the displayed pairing. Fourier inversion therefore gives a finite expansion, and character orthogonality gives uniqueness. Compact support meets only finitely many cosets. This is the finite-level form of the Schrödinger representation. [Weil, *Sur certains groupes d’opérateurs unitaires*](https://doi.org/10.1007/BF02391012) · [Finite Fourier formula in the earlier reconstruction](finite_weil_arithmetic/main.tex#L459-L490)

Define the linear map on this basis by
$$
       \mathcal T_{f_0}(\tau_u M_v1_L)=H_u H_v f_0 .
$$
The commutation relation on both sides is $\tau_uM_v=\psi(B(u,v))M_v\tau_u$, respectively $H_uH_v=\psi(B(u,v))H_vH_u$. Replacing $u$ by $u+l$ and $v$ by $v+l'$ multiplies both sides by the same $\psi(B(l,v))$, since the two lattice halves fix their respective vacuum vectors. Hence the map intertwines all translations and modulations and sends $1_L$ to $f_0$. Conversely these properties force its value on each basis vector. Its injectivity follows from the joint eigencharacters of the commuting integral translations from $L$ and $L'$. The images are nonzero and distinct pairs of cosets have distinct joint eigencharacters. This follows by testing a difference of $v$ against $L$, or a difference of $u$ against $L'$, using the two annihilator identities. The resulting eigenvectors are linearly independent. Each image is a theta function since finite Heisenberg translation preserves the defining theta space. It also satisfies the real Fock vacuum equations, since translations at finite places commute with the real Heisenberg action. [Model definition][model] · [Both normalized models in the pinned construction][models]

The formal statement takes the model map on **all** functions on $W$, with the intertwining laws imposed for compactly supported, locally constant functions on the chosen half. Indeed, the source's finite-level condition is support in $k^{-1}L$ and periodicity under $kL$ for some $k>0$. Extend $\mathcal T_{f_0}$ by zero on an algebraic complement of this subspace. This gives a model on the required domain. Any other such model agrees on the displayed basis and hence on the two specified tests. Interchanging $e$ and $\bar e$ gives the other model with the same normalization. If the union of primes is empty, the chosen half is the zero space and the construction simply sends its unit indicator to $f_0$. [Exact universal characterization][model]

## The functions to insert

Write $a=\dim_E S$, $b=\dim_E T$. In each case require integrality of the entire framed finite matrix, then impose the following conditions on its reductions. Off the chosen half, or when any stated condition fails, the test function is zero. For a residue matrix $y$, write $y^{[j]}$ for its upper left $j$-square block, using the source's zero padding when necessary. A condition “zero below $j$” applies to the entries below row $j$ in the first $j$ columns. [Frame maps and residue conventions][frames]

| | Chain test | Definite-row test |
| --- | --- | --- |
| Polarization | $x\in eW$ | $x\in\bar eW$ |
| Matrix to reduce | $y=\beta_T^{-1}x\beta_S$, of size $b\times a$ | $y=\beta_S^{-1}G_S^{-1}\overline{x}^{\,t}G_T\beta_T$, of size $a\times b$ |
| At $P\in P_g$ | Zero below $a$. The block $g_P=y_P^{[a]}$ must be invertible and block upper triangular for the level flag. The tuple of its leading $r$-square blocks must belong to the specified group $H$. | Zero below $b$ and $y_P^{[b]}=1_b$. The value from the marked places is then one. |
| At $P\in Q$ | Zero below $r$ and $\det y_P^{[r]}\ne0$. Multiply by $\xi_P(\det y_P^{[r]})$. | Zero below $b$ and $\det y_P^{[b]}\ne0$. Multiply by $\xi_P(\det y_P^{[b]})^{-1}$. |

On its marked support the chain test has value
$$
 \chi_H\big((g_P^{[r]})_{P\in P_g}\big)
 \prod_{P\in P_g}\left[
      \left(\prod_{c=1}^{s} c_{g,c,P}(\det g_{P,cc})\right)
                        \,\chi_{j,P}(\det g_P)^{-1}\right].
$$
Here $g_{P,cc}$ is the $c$-th diagonal block after the leading block, with determinant interpreted as in the level datum. The character $\chi_H$ is evaluated once on the joint tuple. Multiplying by the auxiliary factors in the table gives the complete test. The conjugation in the adjoint matrix sends $\bar eW$ back to the primes in $e$ for reduction. In particular both tests use the residue fields at the marked primes in their given orientations. [All three residue factors][res] · [Chain test][chain] · [Definite-row test][row]

Both functions are Schwartz–Bruhat. The frames and Gram matrices are invertible, so the inverse image of integral matrices on the finite chosen half is a compact open lattice. Reduction at finitely many primes cuts it into finitely many compact open classes. Each test is constant on each class. The finite Fourier construction therefore gives its unique image for every twist, including $Q=\varnothing$, where the auxiliary factor is one. For the chain ranks $a\le b$, the framed rectangular matrix with identity on top and zeros underneath at every chosen prime has test value one. The same holds in the adjoint coordinates for the row ranks $b\le a$. Both matrices have preimages on their prescribed half, and injectivity gives a nonzero theta vector in these respective ranks. [Chain construction and finite-level bound][chainproof] · [Adjoint construction and bounds][rowproof] · [Rectangular identity test for the row][nonzero]

[exists]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Formalism/LocalToGlobal/IndefiniteReal/DatumVec.lean#L185-L205
[tuple]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AbelianVarietyTheory/Proofs/IwasawaDecomposition/LiftsAtAndSeedFacts.lean#L151-L159
[vac]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Formalism/LocalToGlobal/IndefiniteReal/LocalNewformFunction.lean#L184-L226
[halves]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AbelianVarietyTheory/Proofs/IwasawaDecomposition/EqZeroOrEqOfPlaceIdem.lean#L161-L199
[model]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Formalism/LocalToGlobal/IndefiniteReal/LocalNewformFunction.lean#L241-L261
[models]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AbelianVarietyTheory/Proofs/IwasawaDecomposition/EqZeroOrEqOfPlaceIdem.lean#L187-L211
[frames]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Formalism/LocalToGlobal/IndefiniteReal/DatumVec.lean#L23-L50
[res]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Formalism/LocalToGlobal/IndefiniteReal/DatumVec.lean#L51-L78
[chain]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Formalism/LocalToGlobal/IndefiniteReal/DatumVec.lean#L84-L96
[row]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Formalism/LocalToGlobal/IndefiniteReal/DatumVec.lean#L109-L119
[chainproof]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AbelianVarietyTheory/Proofs/IwasawaDecomposition/StepVecExists.lean#L18-L30
[rowproof]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AbelianVarietyTheory/Proofs/IwasawaDecomposition/GramMapMulInv.lean#L58-L83
[nonzero]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AbelianVarietyTheory/Proofs/IwasawaDecomposition/ExistsNonvanishingFiniteDatumDefiniteLift.lean#L108-L122
