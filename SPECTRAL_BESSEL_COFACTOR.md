# The Bessel projection scalar from the Capelli comatrix

In the [length moment](SPECTRAL_BESSEL_MOMENTS.md) the tensor projection is paired with a Bessel functional. The adjacent-rank real branching calculation in the adjoint-functor reader identifies the relevant comatrix and fixes its shifts. For the higher Bessel flag one must also remove both chains of isotropic frame directions. The following calculation gives the matrix entry for every rank $r\ge1$ needed in the nonidentity zero-Gram cell. [Reader's comatrix calculation][reader] · [Native scalar and frame conventions][frame]

Use zero-based indices and $n=k+2r+1$. In the basis adapted to the flag the compact middle block has indices $r,\ldots,r+k-1$. The negative line is in position $r+k$. Write $\mathcal E=(E_{ab})$ for the matrix of generators, with $[E_{ab},E_{cd}]=\delta_{bc}E_{ad}-\delta_{ad}E_{cb}$. On the tensor with the dual defining representation the split Casimir in the convention of the moment note is $-\mathcal E$. Its idempotents are denoted $P_s$, with $\mathcal E P_s=(\mu_s+(n-1)/2)P_s$. This follows by subtracting the Casimir of the shifted summand of parameter $\mu-e_s$ from the sum of the two constituent Casimirs. The normalized covector and evaluation in this basis give, up to unit scalars, the **last input column and first output row** for $r>0$. This follows by pairing the first isotropic basis vector with its last dual. [Transport to the frame basis][frame]

Write $Q_n(v)$ for the Capelli column determinant with successive shifts $v,v-1,\ldots,v-n+1$, and $\mathcal A(v)$ for the comatrix with its signed complementary minors (transpose of the cofactor matrix). Antisymmetrization of the ordered entries in the evaluation representation gives
$$
 \mathcal A(v)(\mathcal E+(v-n+1)I)=Q_n(v) I .
$$
The central polynomial is the scalar $\prod_t(v+\mu_t-(n-1)/2)$ on the discrete series of this parameter, by its infinitesimal character. On the range of $P_s$ the second factor on the left vanishes at $v_s=-\mu_s+(n-1)/2$. Dividing the polynomial identity on this summand by $v-v_s$ and evaluating there gives
$$
 \mathcal A(v_s)=\prod_{t\ne s}(\mu_t-\mu_s)\,P_s.
$$
On every other summand the right-hand side of the original identity vanishes at $v_s$ while the factor multiplying the comatrix is invertible there. The roots are distinct on the entire permitted shift ball. Molev–Nazarov–Olshanski, Proposition 2.7 and Remarks 2.8 and 2.11, give the alternating formulas with either row or column ordering. They apply by the evaluation homomorphism $T(z)\mapsto I+\mathcal E/z$. [Quantum determinant formulas][mno] · [Projector at a simple root][proj]

The desired comatrix entry uses rows $0,\ldots,n-2$ and columns $1,\ldots,n-1$. Let $L$ be the period in its normalized simple-root character. On strictly upper entries outside the middle block, $L E_{ab}=p_{ab}L$. The only nonzero $p_{ab}$ that these cofactor expansions encounter are on the two chains
$$
  0\longrightarrow\cdots\longrightarrow r-1\longrightarrow r+k,
  \qquad
  r+k\longrightarrow r+k+1\longrightarrow\cdots\longrightarrow n-1 .
$$
Their moduli are one except for the two arrows incident to $r+k$, each of modulus $\sqrt T$. These values are the derivatives of the unit simple-root character, with the negative line scaled to Hermitian norm $-T$. On the compact middle block the period intertwines its matrix units with the derived action on the coefficient representation. [Frame character at the matrix units][frame]

First expand by rows $0,\ldots,r-1$ in increasing order. At each step the removed row is absent from the current column set. In the alternating expansion putting its matrix unit next to $L$, every term vanishes except that of the outgoing arrow. This deletes the column at the head of that arrow. In this row expansion the remaining minor keeps parameter $v$. Next remove the last $r$ columns in decreasing order. The removed column index is absent from the remaining row set. With this column first in the column-ordered expansion, only the incoming arrow survives. Its deletion shifts the parameter of the smaller minor from $v$ to $v-1$, as the successive shifts start at $v-1$ after the first factor. Reordering distinct row and column lists costs only their permutation signs by quantum minor alternation. The disjoint-index conditions remove the diagonal scalar of the first factor. These two steps use the two ordered expansions of a quantum minor; commuting ordinary determinant entries would give an unjustified shift. The factors from the two chains have product of absolute value $T$, including when $r=1$. [Row expansion and surviving indices][row] · [Column expansion and successive shifts][col]

The remaining determinant is the full compact $k$-block, at $v_s-r=-\mu_s+k/2$. The source's compact infinitesimal character $u_1,\ldots,u_k$ gives at this argument the eigenvalue
$$
     \prod_{i=1}^k(-\mu_s+\tfrac12+u_i).
$$
Combining with the projector formula gives the scalar $c_s$ of the evaluated projection, in absolute value,
$$
       |c_s|=T\frac{\prod_{i=1}^k|\mu_s-1/2-u_i|}
                         {\prod_{t\ne s}|\mu_s-\mu_t|}.
$$
Zeroes of the numerator are allowed. This proves the Capelli matrix-entry step from the frame equivariance, compact infinitesimal character and signed tensor decomposition. The comparison $|c_s|=|\kappa_s|^2$ concerns the adjoint for the normalized periods and is used separately in the [formal-degree cancellation](SPECTRAL_BESSEL_MOMENTS.md#the-shift-scalar-and-the-spectral-gaps).

[reader]: https://github.com/adjoint-functor/theta-periods-to-rh-reader/blob/c0fe7c673cb8acaa328bebb2440ee3334c520b9a/tex/periods.tex#L5574-L5615
[mno]: https://arxiv.org/abs/hep-th/9409025
[proj]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AbelianVarietyTheory/Proofs/JetHarmonics/CapelliComatrixPicksSplitCasimirEigencomponent.lean
[frame]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AbelianVarietyTheory/Proofs/JetHarmonics/DualTensorBesselMoment.lean#L80-L168
[row]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AbelianVarietyTheory/Proofs/JetHarmonics/GlRelationRowStepsFunctionalEigen.lean
[col]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AbelianVarietyTheory/Proofs/JetHarmonics/BesselColumnStepsFunctionalEigen.lean
