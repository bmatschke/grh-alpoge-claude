# Finite frame evaluations for the signed base-row height

In equation (5) of the [signed level comparison](PERIOD_SIGNED_LEVEL_TRANSFER.md), the two theta-image indices and the source pairing index occur as one sum. On a layer identified with its geometric section row, all three are the valuation of a single determinantal ideal computed from **actual algebraic frame evaluations**. One can choose a finite collection of global trace functionals for the whole layer before choosing a served tuple or a coefficient prime. The signed height also has an exact formula using any one independent tuple of $D$ such functionals, in which the separate section covolume cancels.

## The dual lattice from finitely many algebraic tests

Write $F$ for the small geometric field, $C$ for the space of cusp sections of the prescribed weight and $B$ for its full lattice of sections integral at every finite-place test. We use the established [fullness and geometric comparison](RETWISTED_INTEGRAL_EVALUATIONS.md) and [exact specialization of a semiabelian frame](PEL_SEMIABELIAN_SECTION_TRANSFER.md). The conclusion below constructs tests for an already supplied full lattice.

At a place $\lambda$ of $F$, write $R=\mathcal O_{F_\lambda}$. For an algebraic framed point $y$ defined over a number field $L/F$ and integral at $\nu\mid\lambda$, compose its evaluation with
$$
        z\longmapsto\operatorname{Tr}_{L_\nu/F_\lambda}(u z),
        \qquad u\in\mathfrak D^{-1}_{L_\nu/F_\lambda}.
$$
These $F_\lambda$-linear functionals generate $(B\otimes R)^*$ integrally. Here the asterisk on a lattice denotes its **linear dual**, and the different is relative to $F_\lambda$. Indeed all these traces are integral on $B$. The trace pairing identifies the inverse different with $\operatorname{Hom}_R(\mathcal O_{L_\nu},R)$. Thus an element $z\in L_\nu$ outside $\mathcal O_{L_\nu}$ has a trace reading outside $R$ for some permissible $u$. Allowing the inverse different is important in wild ramification. [Dedekind complementary module and trace pairing](https://stacks.math.columbia.edu/tag/0BW0)

For $f\in C(F)$, integrality at all integral frames over $\lambda$ means precisely $f\in B\otimes\mathcal O_{F,\lambda}$. To prove this, start with a global denominator carrying $f$ into $B$. Only finitely many other places can fail any of their tests. Choose an integer of $F$ with sufficiently large orders there and order zero at $\lambda$, by ideal approximation. Its multiple of $f$ passes every test. If $f$ fails a test at $\lambda$, exact specialization gives a number-field framed point integral at $\nu$ with the same negative normalized valuation. For $f$ in the completed space outside $B\otimes R$, choose a rational section congruent to it modulo $B\otimes R$, by density. The corresponding inverse-different functional separates $f$ as well. Consequently the common inverse image of $R$ under the trace functionals is exactly $B\otimes R$. Their span is contained in the finite free linear dual, hence is finite; taking its polar and applying DVR biduality proves the asserted equality. Reduction modulo the maximal ideal and basis extraction now give $\dim_F C$ individual trace tests forming an actual basis of the completed dual. There is no residual error per section arising from small positive fractional valuations.

The functionals can also be taken globally. At one $\lambda$ choose a local basis of such functionals. For each of its framed points $y/L$, the evaluations of a finite list of integral generators of $B$ are algebraic numbers. Choose $c\in L$ approximating the chosen local multiplier at $\nu$, and approximating zero at the other places over $\lambda$, sufficiently closely that the resulting global trace functional
$$
         \mathcal E_{y,c}(f)=\operatorname{Tr}_{L/F}(c f(y))
$$
agrees modulo the maximal ideal on every generator of $B$ with the specified local trace. This uses the decomposition of the completed field trace into its local traces. Clear its finitely many other denominators by an integer of $F$ congruent to one modulo $\lambda$. This leaves a functional in $B^*$ with the same residue. These global functionals span the full local dual by Nakayama. The first such basis is rationally independent, so its span in $B^*$ has finite index. At the finitely many primes dividing this index repeat the construction and take the union. The result is a finite list spanning $B^*$ **at every place**. The number of tests, their fields and the trace multipliers can depend on the geometric row. This proof gives no uniform bounds for their sizes.

At a coefficient-field extension $K/F$, use this list on the base-changed ambient lattice, and restrict it to the actual row subspace $V$ of the layer. The source identification sends $M_j$ to the intersection of the ambient lattice with $V$. At every place this is a saturated submodule of a finite free module over a DVR. It is a direct summand there, so restriction of the above functionals generates $M_j^*$ locally at each $w$ of $K$. This also works with projective lattices and with dimensions smaller than the ambient cusp-space dimension. These uses require the original base-change and intersection identifications on that member. [Native ambient section lattice and scalar extension][ambient] · [The layer's actual target intersection][target]

## One ideal for the theta-image and pairing indices

Fix a layer with $D=\dim_K V=D_0>0$. For a tuple $t$ let $\theta_t$ be its rational layer isomorphism, $H_t$ its definite Hermitian source form and $T_t$ the source lattice. The star on a matrix below is conjugate transpose for the algebraic involution on $K$. In any rational target basis form
$$
       Q_t=\theta_t H_t^{-1}\theta_t^*.
$$
Write $E$ for the rectangular matrix with the global frame trace functionals above as its rows in that basis. Set $\mathfrak b_{j,t}$ equal to the fractional ideal generated by all the $D$-row, $D$-column minors of $E Q_t E^*$. Its construction uses the tuple's actual maps and coefficients. Fractional ideals and negative indices are permitted. For $t=t_w=t_{\bar w}$ the local identity is
$$
 v_w(\mathfrak b_{j,t})=
 [M_j:\theta_tT_t]_w+[M_j:\theta_tT_t]_{\bar w}
                         +[T_t:T_t^\sharp]_w .                     \tag{1}
$$
To see the sign, use bases of $M_j,T_t$ over the semilocal rings at $w,\bar w$. Write $B_t$ for the matrix of $\theta_t$ in those bases and $H'$ for the source Gram. The square matrix $B_t(H')^{-1}B_t^*$ has determinant valuation $v_w(\det B_t)+v_{\bar w}(\det B_t)-v_w(\det H')$, which is the right side. In these target coordinates the rows of $E$ span the full integral dual at both places. The minor with row set $I$ and column set $J$ is
$$
    \det E_I\,\det\!\big(B_t(H')^{-1}B_t^*\big)\,\overline{\det E_J}.
$$
One can select $I$ with $\det E_I$ a unit at $w$ and independently select $J$ with $\det E_J$ a unit at $\bar w$. All other minors add nonnegative valuations to the middle one. At a self-conjugate place one may take $I=J$. This proves (1), even without a single global pair of unit minors. The induced fractional ideal is independent of the finite generating set. [Semilocal index and transported form](PERIOD_RELATIVE_DETERMINANTS.md#exact-cancellation-at-a-conjugate-pair)

In particular, an *upper* bound on (1) can be certified by exhibiting a single nonzero mixed minor at each required place with sufficiently small valuation. Estimates for the multiplicity of vanishing of every theta section in isolation point in the opposite direction; (1) uses determinants of their jointly evaluated, contracted lifts. Off the twist set the native reference hypothesis makes (1) zero for the served tuple. If a tuple has integral values for all these minors at a place, then one nonzero minor in its reduction proves the **exact** vanishing of the local contribution there.

## A square determinant formula in which the target covolume cancels

For each layer choose any $D$ linearly independent global trace functionals from its list, called $A_j:V\to K^D$. One choice works at all places. It need not be a basis of the integral dual. Put
$$
 b_{j,t}=\det(A_j Q_t A_j^*)\in K^{\bar{}}\setminus\{0\}.
$$
Write $G_{j,\sigma}$ for the prescribed positive target metric at an embedding $\sigma$ in rational coordinates, and use the **complex** adjoint in the positive matrix $U_{j,\sigma}=A_{j,\sigma}G_{j,\sigma}^{-1} A_{j,\sigma}^{*_{\mathbb C}}$. In the squared-norm covolume convention, set $\langle z_\sigma\rangle_\infty=[K:\mathbb Q]^{-1}\sum_\sigma z_\sigma$. Then equation (5) of the signed comparison becomes
$$
 Z_0^{(0)}
  =\frac1{D}\sum_j\left\{
    \sum_{w\ {\rm finite}}\ell_w v_w(b_{j,t_w})
            -\left\langle\log\det U_{j,\sigma}\right\rangle_\infty
                    \right\}.                                      \tag{2}
$$
Indeed let $h_w=[\mathcal O_K^D:A_jM_j]_w$. The square minor calculation gives $v_w(b_{j,t_w})=v_w(\mathfrak b_{j,t_w})+h_w+h_{\bar w}$. The covolume of $M_j$ is the covolume of $A_j^{-1}\mathcal O_K^D$ plus $2\sum_w\ell_w h_w$. For the latter free lattice, using its displayed basis, the covolume is $-\langle\log\det U_{j,\sigma}\rangle_\infty$. Summing over conjugate pairs cancels the index corrections exactly. All prime sums are finite and unchanged under further scalar extension with the given selector. For the version retaining the embedding defect subtract the same $E_{Q,0}/D$ as in the [level comparison](PERIOD_SIGNED_LEVEL_TRANSFER.md). Formula (2) uses local values of the actual algebraic theta contractions and the determinant of the complex dual norm on the chosen tests. The evaluations themselves need no prescribed archimedean orthogonality.

These formulas close the passage from integral frame testing to exact finite local determinants on an identified section row. Entry 7 still requires proving that (2), after the two prescribed signed main terms (and optionally the defect) are subtracted, has a uniform upper bound of order $mL(B_0+N_c)$. The previous geometric covolume, two-run and cut estimates remain a sufficient route. Exact specialization of section valuations supplies the finite dual tests, but gives no upper bound on these mixed determinants or simultaneous control of their archimedean dual norms.

[ambient]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AbelianVarietyTheory/Proofs/DivisorProofs/HasIndexBoundOfRuns.lean#L29-L80
[target]: https://github.com/rh-lean-roadmap/rh-lean-roadmap/blob/02a95b4c62db610642af5f278ee5d0d6df87b348/docs/src/book/main.tex#L54143-L54159
