# How the finite level acts on the theta kernel

The tower uses a theta kernel to pass a prescribed character from one unitary group to the next. At a marked prime the two groups share a leading block of rank $r$. Matching that block cancels its contribution on the two sides. The determinants on the remaining blocks give the character that the lift carries. The definite-row kernel uses the Hermitian adjoint and gives the inverse source character.

Fix a tuple $u$ and the original level and splitting characters (the condition `LevCh.Is`), self-dual lattices, frames, real data and corresponding Weil actions. Use the normalized lattice vacuum and the finite test for the indicated pair. The marked and auxiliary sets $P_g,Q_u$ satisfy the oriented split-place conditions. A *matching pair* consists of finite level lifts $\kappa,\kappa'$ that preserve the lattices and prescribed flags, are the identity at infinity and have the same leading residue block at every marked prime. Write $G,H$ for their residue matrices in the two fixed frames. At an auxiliary prime, the subscript $\mathrm{lo}$ denotes the second diagonal block for the partition into the first $r$ coordinates and the rest. [Construction of the vacuum](THETA_LATTICE_VACUUM.md) · [The two finite tests](THETA_FINITE_LATTICE_TESTS.md) · [Lattice stabilizer character, BTH15](base_theta/main.tex#L1228-L1376)

## The increasing ranks

For the step from $Y_j$ to $Y_{j+1}$ let $d$ be the common rank increment, so their ranks are $r+jd$ and $r+(j+1)d$. For $j=m-1$ the second space is $X'$ of rank $r+md$. In rank $r+jd$ put
$$
 \ell_j(\kappa)=
 \prod_{P\in P_g}\ \prod_{c=1}^j\chi_{c,P}(\det G_{cc})\,
 \prod_{P\in Q_u}\xi_{u,P}(\det G_{\mathrm{lo}})^{-1}.
$$
Here $G_{cc}$ is the $c$th block *after* the leading block, and an empty block has determinant one. For every matching pair the test vector $v_j$ satisfies
$$
 \omega(\kappa,\kappa')v_j
   =\ell_j(\kappa)\,\ell_{j+1}(\kappa')^{-1}v_j .
$$

Indeed, the action pulls the matrix test back by $y\mapsto H^{-1}yG$. At a marked prime its support requires an invertible flag-preserving square block $Y$ with top block $I_r$, and zero rows below $Y$. Matching preserves this condition in both directions. The character on $Y$ is $\prod_{c=1}^j\chi_{c,P}(\det Y_{cc})\,\chi_{j+1,P}(\det Y)^{-1}$. The ratio after pullback gives the two flag products in the formula together with an extra $\chi_{j+1,P}(\det H)/\chi_{j+1,P}(\det G)$. The splitting character of the lattice vacuum cancels that extra factor. At an auxiliary prime the pullback gives $\xi_{u,P}(\det G_{00})/\xi_{u,P}(\det H_{00})$, while the vacuum contributes $\xi_{u,P}(\det H)/\xi_{u,P}(\det G)$. Multiplication leaves exactly the two lower-block factors above. The splitting characters are unramified on the remaining finite units. The normalized finite model transports this computation to the chosen global vector by Weil–Heisenberg covariance. [Matrix calculation, DI6](division_identity/main.tex#L359-L422) · [Transport and cancellation, DI7](division_identity/main.tex#L425-L537)

The identity also holds for every real Fock polynomial applied to $v_j$. A finite pair fixes each real Heisenberg direction, so its unitary action commutes first with real translations, then with their differentiated creation operators. If both levels carry a prescribed character on the leading marked blocks, its value on their common block cancels in the ratio. In particular, at the source level with leading block $I_r$, take $\kappa'=1$. The finite action is then $\omega(\kappa,1)v_j=\ell_j(\kappa)v_j$. This proves both parts of the tower’s finite source-level law (`LawsOK`), for every tuple, including the last step. [Polynomial vectors and full levels, DI8](division_identity/main.tex#L539-L581) · [The two principal-level specializations][chain]

## The definite row

Here $G$ acts on $V_i$ of rank $r+d$ and $H$ on $W_i$ of rank $r$. The definite-row test uses the conjugate split half. Taking the Hermitian adjoint switches the pullback to $y\mapsto G^{-1}yH$. Its marked-prime support is the column $\binom{I_r}{0}$, which is fixed because $G_{00}=H$. The vacuum contributes $\chi_{i+1,P}(\det G)/\chi_{i+1,P}(\det H)=\chi_{i+1,P}(\det G_{\mathrm{lo}})$. At an auxiliary prime the top square block of the column carries $\xi_{u,P}^{-1}$. Pullback supplies $\xi_{u,P}(\det G_{00})/\xi_{u,P}(\det H)$, and the vacuum again supplies $\xi_{u,P}(\det H)/\xi_{u,P}(\det G)$. The row formula is consequently
$$
 \omega(\kappa,\kappa')v_{i,u}
  = \left(\prod_{P\in P_g}\chi_{i+1,P}(\det G_{\mathrm{lo}})
          \prod_{P\in Q_u}\xi_{u,P}(\det G_{\mathrm{lo}})^{-1}\right)v_{i,u}
  = \ell_{V_i,u}(\kappa)^{-1}v_{i,u}.
$$
The last equality uses the definite level’s own convention, inverse $\chi_{i+1,P}$ at marked primes and positive $\xi_{u,P}$ at auxiliary primes. Taking the leading block to be $I_r$ and $\kappa'=1$ gives its source-only eigencharacter on the entire prescribed finite level. The same commutation with real creation operators applies. These identities compute the finite action on the constructed tests independently of the value of any subsequent global theta integral. [Adjoint calculation and matched-pair theorem][row] · [Specialization to the definite level][principal]

[chain]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AbelianVarietyTheory/Proofs/TwistedOperators/ChainStepsLevelCharacterConditionsHold.lean#L60-L89
[row]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AbelianVarietyTheory/Proofs/TwistedOperators/WeilActionLiftPairStepVectorInvLevelChar.lean#L41-L126
[principal]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AbelianVarietyTheory/Proofs/IwasawaDecomposition/LevelCharacterEigenvector.lean#L18-L28
