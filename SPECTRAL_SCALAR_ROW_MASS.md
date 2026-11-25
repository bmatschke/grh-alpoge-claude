# The scalar row has the full-column mass normalization

Fix two words $u,v$ of one admitted selected Bessel datum and a represented joint tuple of nonsingular Gram matrix. All groups, lattices and Haar measures in this calculation belong to that datum. The result identifies the coefficient multiplying the normalized scalar-partner energy. This advances the mass and dimension comparison in the [earlier Gram calculation](actual_gram/actual_gram_section.tex#L181-L195).

## A word and its full column dimension

Let $H_u$ be the definite unitary group on the complement of the word frame. Write $K_{H,u}$ for its lattice stabilizer away from infinity, $K''_{H,u}$ for its actual marked level, $V_u$ for the adelic quotient volume, and $h_{\infty,u}=\operatorname{vol}H_u(F_\infty)$. Write $p_u=\dim\pi_u$ for the dimension of the compact coefficient representation and $d_u$ for the full column dimension. The mass $\rho_u$ of the coarse class set is the sum of the reciprocal automorphism orders of its lattice representatives. On the tied level,

$$
 d_u=p_u\,\Gamma_1\rho_u
     =\frac{p_u V_u}{h_{\infty,u}\operatorname{vol}K''_{H,u}},
 \qquad
 \Gamma_1=\prod_{\mathfrak p\mid g_0g_1}
   \frac{|\mathrm{GL}_k(\mathbf F_{q_{\mathfrak p}})|}
        {|U_k(\mathbf F_{q_{\mathfrak p}})|}.
 \tag{1}
$$

Indeed the split adapted basis identifies the integral definite block at each marked place with $\mathrm{GL}_k(\mathcal O_{F,\mathfrak p})$. Reduction is onto: a lift of an invertible residual matrix has unit determinant. The deep condition in that basis preserves the given frame modulo the marked prime and puts the definite block in the prescribed unitriangular subgroup (up to change of basis). Its kernel contains the principal congruence subgroup. Thus its index is the displayed finite quotient. Away from the marked places the two levels coincide. [Actual frame, level and column spaces][datum] · [Adapted level and index][index] · [Comparison on the word-conjugated level][typedindex]

For a coarse class with finite automorphism group $\Delta$, its refinements are the $\Delta$-orbits on $K_{H,u}/K''_{H,u}$. Every deep stabilizer is trivial. In fact a finite subgroup preserving the definite lattice and reducing into a unitriangular group at a place of residue characteristic $g_i$ is a $g_i$-group: the kernel of reduction is pro-$g_i$ and the residual group is a $g_i$-group. The rational subgroup embeds in either completion. Applying this at the two distinct marked characteristics forces its order to be one. Hence this coarse class has exactly $\Gamma_1/|\Delta|$ deep classes. Each deep class contributes one unrestricted copy of the coefficient space, also with its prescribed character, because the class has no stabilizer. This proves the first equality. Integrating over the double classes gives $V_u=h_{\infty,u}\operatorname{vol}K_{H,u}\,\rho_u$. Combining it with $\operatorname{vol}K_{H,u}=\Gamma_1\operatorname{vol}K''_{H,u}$ proves the second equality. In particular the single inequality used for the singular cell sharpens to equality for these full columns. [Arithmetic mass and stabilizers][mass] · [Full column count on the original setting][cols] · [Earlier one-sided use](SPECTRAL_DIAGONAL_ZERO_CELL.md#L55-L57)

## Putting both words on the common Haar scale

Write $n_{\infty,u}$ for the volume of the real fundamental domain for the integral unipotent group, $\mu_{N,u}$ for the finite volume of the corresponding integral unipotent level and $s_u$ for the volume of the deep Bessel level in the stabilizer $S_u=N_u H_u$. Use the mass-record normalization $c_u=n_{\infty,u}h_{\infty,u}/p_u$ after separating the ambient finite level. Strong approximation for the split unipotent radical gives $N_u(\mathbf A_f)=N_u(F)(K_f\cap N_u)$. It follows, for example, by ordering the successive additive coordinates and applying finite-place additive approximation in each central quotient. Thus its adelic covolume is $n_{\infty,u}\mu_{N,u}$, which is one in the compatible measure. In adapted flag coordinates the deep level is the product of this integral unipotent group with $K''_{H,u}$. Its measure is the product: the compact Levi preserves the integral unipotent lattice and hence its normalized Haar. We get

$$
 s_u=\mu_{N,u}\operatorname{vol}K''_{H,u},
 \qquad
 c_u^{-1}=\frac{d_u s_u}{V_u}. \tag{2}
$$

These equations apply separately to both words, on their respective conjugated levels. [Source level product][level] · [Source mass comparison][mass2] · [Exact definitions of the four volume and column fields][facts]

Let $V_G$ denote the ambient adelic quotient volume, $V_{uv}$ the quotient volume of the joint tuple stabilizer and $v^\dagger$ the deep **ambient** finite level volume. Let $\mathfrak d>0$ be the archimedean formal degree in this ambient Haar. The identity contribution to the dimension count is $D^\star=\mathfrak d V_G/v^\dagger$. For the same character and Gram-fibre measures, the stabilizer comparison gives $V_{uv}V_G=V_uV_v$. Its proof unfolds the rational tuple orbit, uses the compatible Siegel–Weil coefficient and cancels a finite positive test integral. Its hypotheses are the convergent smooth Siegel–Weil input, compatible disintegrations, and nonsingularity of the joint tuple; SVW18 proves the comparison for the actual rescaled datum under this input. Substituting (2) twice gives the following exact equality:

$$
 \boxed{\displaystyle
 \frac{V_{uv}v^\dagger}{s_us_v c_uc_v\,\mathfrak d}
 =\frac{V_{uv}v^\dagger\,d_ud_v}{V_uV_v\mathfrak d}
 =\frac{d_ud_v}{D^\star}.}
 \tag{3}
$$

No genus factor or $\Gamma_1$ remains in (3). The elementary factors can be traced before cancellation. At a marked place write $K$ for the ambient lattice level, $K^\natural$ for the intermediate frame level, and $K''$ for its deep ambient level. Put $a_{\mathfrak p}=|\mathrm{GL}_k|/|U_k|$. The split adapted flag gives the two successive residue orders $|\mathrm{GL}_k|\,|N|$ and $|U_k|\,|N|$, where $N$ is the common unipotent block. Hence $\operatorname{vol}K^\natural=a_{\mathfrak p}\operatorname{vol}K''$. Each word's stabilizer index gives $\operatorname{vol}S_w=a_{\mathfrak p}\operatorname{vol}S_w''$. The marked orbital-mass to unit-measure ratio is $\operatorname{vol}K\operatorname{vol}K^\natural/(\operatorname{vol}S_u\operatorname{vol}S_v)$, and its ordinary analogue is $(\operatorname{vol}K)^2/(\operatorname{vol}S_u\operatorname{vol}S_v)$. Therefore dividing the product of these ratios by the global $\operatorname{vol}K$ and multiplying by the finite Gram coefficient $\prod a_{\mathfrak p}=\Gamma_1$ gives $v^\dagger/(s_us_v)$, the factor in (3). This last conversion uses the local orbital-measure comparisons at the actual ordinary and marked places. It must be made with the same unit measure and the same represented frame used for the [normalized primitive densities](SPECTRAL_SCALAR_DENSITIES.md#L27-L40). [Stabilizer comparison on these measures](stabilizer_volume_v55/main.tex#L1029-L1078) · [Marked local-measure comparison][marked] · [Finite product and final scalar][cancel] · [Independent reconstruction of the same prefactor][reader]

## A finite terminal-flag estimate preserving the phases

For unequal words one can also use Lemma B8.10c of the RH Lean Roadmap. Its appendix gives a conventional proof for the selected arithmetic model. It assumes the actual word levels satisfy $T_u\equiv T_v\bmod (g_0g_1)^2$, the scalar-partner coefficients and terminal flag kernel use the same characters and Haar measures, and the row representatives and size hypotheses are those of its distinct-word estimate. The squared congruence holds for the prescribed word-prime data since $\pi_{T,w}\equiv1\bmod (g_0g_1)^2\mathcal O_E$ and $T_w=\pi_{T,w}\bar\pi_{T,w}$. The normalization $\alpha$ here is the product of the two single-frame references at ordinary places and the shared reference at marked places. The actual primitive density calculation uses exactly these references after passing to the divided-difference basis at the marked places. [Level congruence][wordlevel] · [Lemma and its scope][terminal] · [Selected finite factors](SPECTRAL_SCALAR_DENSITIES.md#L27-L40)

Let $Y$ be any finite set of terminal flags, $S$ any finite set of partner rows, and $c_{\rho p}$ their normalized complex coefficients. For arbitrary vectors $Z_p$ in a complex Hilbert space one has

$$
 \sum_{\rho\in S}\Big\|\sum_{p\in Y}c_{\rho p}Z_p\Big\|^2
 \le E_{\rm den}
 \sum_{p,q\in Y}K_{\rm top}(p,q)\langle Z_p,Z_q\rangle ,
 \tag{4}
$$

where the inner product is linear in the first argument and the terminal kernel has the corresponding orientation. To see the arithmetic content, group points by their terminal kind (the last minor divided by its predecessor when the predecessor is nonzero; a separate class otherwise) and their integral presentation classes at every finite place. For each resulting label $j$ let $v_j$ be the product of its local phase-weighted orbital sums, multiplied locally by the number of isomorphisms of the presentation, and let $a_j$ be the reciprocal product of its automorphism orders. Outside a finite set the reference term is one. The point kernel is a sum of positive matrices $a_jv_jv_j^*$. For the partner-row Gram the multiplier for a represented class is its density ratio $d_j$. Indeed the sum over partners of one term is its unweighted class orbital sum: the integral double-orbit conditions can be realized simultaneously by additive approximation in the upper and lower unitriangular coordinates, and the partner lattice is recovered by intersecting the local lattices with the rational space. The sum of row-*mass*-weighted terms in the same class gives the represented density, by gluing its definite complement of rank $k-1$ along the discriminant module and weighting by reciprocal stabilizer orders. Equal scalar partners have equal row mass. The remaining ratio of positive point weights is one on each contributing support: the shifted determinant ideals agree there and the terminal kind is fixed. Thus each multiplier is in $[0,E_{\rm den}]$. These are the two fibre identities used by B8.10c. For applications on another row presentation, both identifications with these phase-weighted counts would have to be proved. [Fibre identities and support argument][flagproof] · [Original partner and weighted fibre sums][partnersum]

Subtracting the represented Gram from $E_{\rm den}K_{\rm top}$ now leaves a positive matrix, also after restricting the partner rows and applying the point-to-flag diagonal rescaling. Apply the resulting scalar quadratic-form inequality to each orthonormal coordinate in the finite-dimensional span of the $Z_p$, and sum over those coordinates. This proves (4), including the interference between distinct $p,q$. In particular (4) applies to any finite family of actual terminal orbital vectors. It consumes the finite arithmetic comparison without a triangle inequality on individual phases.

The additional identification for the archimedean sampling theorem is precise. B8.10hbe requires the terminal lift of each cut word to intertwine the ordered residual slice operators with their radial representatives. In B8.10e, Claim 1 obtains that exact tower, its point weights and its energy identification from the built-data witness in the archive. Our local Bessel isometry and the finite matrix inequality (4) alone do not identify those residual operators. Once the identification is supplied, compact cutoffs give positive finite Gram matrices, and entrywise limits preserve that property; the integral passage additionally needs the derivative and support bounds stated in Claim 5. This is the analytic comparison needed to apply the mixed sampling bound on the tied family. [Radial intertwining hypothesis][radial] · [Source of the tower identification][carrier] · [Cutoff limit][cutlimit]

## Consequence for the remaining signed sum

On the selected represented frames we already have $\log E_{\rm den}\le (5/2)f\,3^{-(k-m+1)}$. If the remaining archimedean realization and sampling estimates, combined with (4), give an upper bound $(1+\delta)E_{\rm den}$ times the left side of (3), then the upper bound for that row is exactly $(1+\delta)E_{\rm den}d_ud_v/D^\star$. The additional finite Gram operator bound $P_g$ is applied when passing from rows to operators. It is distinct from the finite coefficient $\Gamma_1$ canceled above. The computation identifies the dimensional and volume scale without using a signed row bound. For the mixed words the remaining step is to identify the archimedean kernels on the right of (4) with the residual tower and prove its sampling bound with $\delta\le b^{-7}$. The same-word case allows a larger scalar bound. The higher-corank and nonscalar loop estimates and the nongeneric corank-one estimates remain separate. [Tied density bound](SPECTRAL_SCALAR_DENSITIES.md#L49-L63) · [Signed estimates and distinct error families][signed] · [Source of the local-energy and sampling inputs][sampling]

[datum]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Formalism/LocalToGlobal/SiegelLatticeTheory/CokernelGLCounts/MassDataInst.lean#L206-L232
[index]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Formalism/PeriodIntegrals/UnitaryGroupMassFormula/LatticeColumns/IdxCount.lean#L79-L112
[typedindex]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Formalism/LocalToGlobal/SiegelLatticeTheory/CokernelGLCounts/RankPointCounts/MassDataXSIdx.lean#L24-L90
[mass]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Formalism/LocalToGlobal/SiegelLatticeTheory/CokernelGLCounts/MassDataInst.lean#L60-L93
[cols]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Formalism/LocalToGlobal/SiegelLatticeTheory/CokernelGLCounts/RankPointCounts/MassDataXColumns.lean#L18-L32
[level]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Formalism/PeriodIntegrals/UnitaryGroupMassFormula/LevelStructures/Assembly.lean#L23-L30
[mass2]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Formalism/LocalToGlobal/SiegelLatticeTheory/CokernelGLCounts/RankPointCounts/MassDataXMasses.lean#L9-L14
[facts]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Formalism/HermitianCurvature/MemParahoricTimesPrincipalCongruenceIff.lean#L603-L655
[marked]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Formalism/LocalToGlobal/SiegelLatticeTheory/CokernelGLCounts/RankPointCounts/MassDataXTyped.lean#L60-L77
[cancel]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Formalism/HermitianCurvature/HermitianCurvatureProofs/LocalVolumePositivity.lean#L176-L207
[reader]: https://github.com/adjoint-functor/theta-periods-to-rh-reader/blob/c0fe7c673cb8acaa328bebb2440ee3334c520b9a/tex/trace.tex#L839-L876
[signed]: https://github.com/jimjamzola/RH-Alpoge-Reconstruction/blob/9eefc08b0819728d4dd2ef0568b49a61251af111/manuscript/sec14_bessel.tex#L1146-L1172
[sampling]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Formalism/HermitianCurvature/HermitianCurvatureProofs/GrowthOfBasic.lean#L1107-L1168
[wordlevel]: https://github.com/rh-lean-roadmap/rh-lean-roadmap/blob/94e6a98b4e74932a0298d6bd22d44cf60c62764b/docs/src/book/main.tex#L6318-L6325
[terminal]: https://github.com/rh-lean-roadmap/rh-lean-roadmap/blob/94e6a98b4e74932a0298d6bd22d44cf60c62764b/docs/src/book/main.tex#L17033-L17074
[flagproof]: https://github.com/rh-lean-roadmap/rh-lean-roadmap/blob/94e6a98b4e74932a0298d6bd22d44cf60c62764b/docs/src/book/main.tex#L44456-L44500
[partnersum]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Formalism/LocalToGlobal/SiegelLatticeTheory/CokernelGLCounts/RankPointCounts/LsDatumBPf.lean#L27-L104
[radial]: https://github.com/rh-lean-roadmap/rh-lean-roadmap/blob/94e6a98b4e74932a0298d6bd22d44cf60c62764b/docs/src/book/main.tex#L17553-L17596
[carrier]: https://github.com/rh-lean-roadmap/rh-lean-roadmap/blob/94e6a98b4e74932a0298d6bd22d44cf60c62764b/docs/src/book/main.tex#L46125-L46160
[cutlimit]: https://github.com/rh-lean-roadmap/rh-lean-roadmap/blob/94e6a98b4e74932a0298d6bd22d44cf60c62764b/docs/src/book/main.tex#L46376-L46385
