# Generic mass and weighted real energy on represented corank-one rows

Fix a represented positive nonsingular point $\gamma$ for one pair of words in the tied construction. Write $n=r+1=m/2$, $f=[F:\mathbb Q]$, $\rho=\operatorname{rd}(E)$ and $g=g_0g_1$. The block lengths are $s_1,\ldots,s_l$, with ends $j_i=s_1+\cdots+s_i$ and $j_0=0$. Use the matched finite family, the convergent Siegel–Weil mass input in its actual arithmetic measures, and the standing hypotheses $k\ge4r+7$, $k\ge m+f+5$, $T_u\equiv T_v\bmod g^2$. Put
$$
 L(s_l)=g^{2f[n(n-1)-(s_l-1)]},\quad
 E_{\rm den}=\max\!\left(1,\sup_{\rm represented}\prod_p h_p\right),\quad
 A_{\rm re}=\rho^{2r(r+1)(k-1)f}A_{\rm mass}.
$$
Here $h_p$ is the primitive joint density divided by the original single or double reference at $p$. For the actual generic mass and the source's physical point weight $p(\gamma)$,
$$
 0<n_{\rm gen}(\gamma)
 \le A_{\rm re}E_{\rm den} H(\gamma)^{r(r+1)}
                    \widehat N_G(\gamma)^{k-1}
 \le A_{\rm re}E_{\rm den} H(\gamma)^{r(r+1)}
                    \frac{p(\gamma)}{L(s_l)},\qquad
 E_{\rm den}\le \exp\!\bigl(\tfrac52 f\,3^{-(k-m+1)}\bigr).       \tag{1}
$$
The global height $H$ is the product of the finite local heights of this family. The bound concerns the generic reference mass used even when the term sum itself is nongeneric. [Density and reference factors](SPECTRAL_SCALAR_DENSITIES.md) · [Tied mass hypothesis][mass] · [Roadmap comparison][road]

## From the local frame weights to a single genus mass

At a finite place with a matched frame pair, use the integral class of its cross matrix under the two congruent upper unitriangular changes. On one representative of this class fix the two frames. Let $\lambda_p$ be the local generic lattice count with these frames fixed, weighted by the same inverse relative stabilizer volumes for the inner data as the mass $n_p^{\rm gen}$. In the native unfolding $n_p^{\rm gen}=w_p\lambda_p$. The factor $w_p>0$ is the weight of the integral frame class. Indeed the paired frame changes preserving the cross class act transitively on its presentations, and the stabilizer-orbit formula for these changes first sums over the frames and then over the lattices with frames fixed. The positive class weight is at most the sum of all integral class weights. That sum is bounded by the number of integral presentation classes before quotienting. Let $\delta_p$ be the product of the nonzero leading minors in these local integral coordinates. The triangular elimination bounds denominators of the two frame changes by $\overline{\delta_p}$ and $\delta_p$ respectively. In each of the $r(r+1)/2$ upper entries, reducing both changes modulo integral ones costs at most $q_p^{2v_D}$ together, and their relative integral change modulo the marked parameter costs $q_p^{2v_\theta}$. The resulting representatives cover every integral class, giving the bound $q_p^{r(r+1)(v_\theta+v_D)}$. On represented support $v_\theta,v_D,a\ge0$ and $H_p=q_p^{v_\theta+v_D+a}$. Therefore $w_p\le H_p^{r(r+1)}$, including at $H_p=1$. [Matched class weight][wclass] · [Integral class bound before enlargement][count] · [Integral class coordinates][icoord]

Choose the rational frames to agree with representatives of these integral classes at the finitely many exceptional places. Their changes are unitriangular and can be prescribed by finite-place approximation in the matrix entries. A rational unipotent isometry brings the first frame back to the original word frame. This preserves the point and determinant and transports the stabilizers by conjugation. The identity for the genus of the fixed pair gives $\mathcal G=V_0\prod_p\lambda_p$, with $\mathcal G$ the sum of inverse stabilizer orders over the glued unimodular lattices. Thus $n_{\rm gen}=\mathcal G\prod_p w_p\le H^{r(r+1)}\mathcal G$. This use of $V_0$ counts it once. [Prescribing and transporting the frames][glue] · [Genus product on the chosen frames][glueprod]

Counting the same pairs first by row lattice shows $\mathcal G=\rho_u\nu(Z)$, with $\rho_u$ the original row mass and $\nu$ its normalized fixed-Gram frame mean. In the common fixed-Gram groupoid the stabilizer is the subgroup fixing the embedded frame pair, so both sides give the same reciprocal orders. The convergent mean formula at this *represented integral* Gram matrix gives $\nu(Z)=c_{\rm expl}\delta(Z)^{k-1}\prod_p {\rm dens}_p(Z)$, where $\delta$ is the square root of the absolute norm of the scaled joint Gram determinant. At a marked place use the divided-difference basis and the single reference $\alpha_p$. Elsewhere use the product reference. The constant comparison in the same measures is
$$
 c_{\rm expl}\rho_u\prod_p\alpha_p=A_{\rm mass}\,{\rm ngFac},\qquad
 {\rm ngFac}\,\delta(Z)^{k-1}
   =\rho^{2r(r+1)(k-1)f}\widehat N_G^{k-1}.
$$
Consequently $\mathcal G=A_{\rm re}\widehat N_G^{k-1}\prod_p h_p$. The uniform density bound in (1) applies to this represented joint frame. This proves its first inequality and preserves the discriminant factor with its full $k-1$ exponent. [Groupoid and explicit density formula][mean] · [Comparison of constants][const] · [Scaled determinant][norm]

## The height cost in the point weight

Write $u(j)=j(2r+1-j)$, $d_{\tau j}=\rho^{-u(j)}|\tau D_j|$, with $D_j$ the raw leading minor, and $P_i=\prod_\tau d_{\tau j_i}^2$, $P_0=1$. The [minor ideal calculation](SPECTRAL_CORANK_ONE_RECIPROCAL_SUM.md) gives $P_i\ge g^{2f\min(j_i,r)}$. On setting $a_i=2(n-j_i)+s_i-1$, the formula for the Haar weight simplifies to
$$
 \frac{p(\gamma)}{\widehat N_G^{k-1}}
 =\prod_{i=1}^l(P_i/P_{i-1})^{a_i}
 =P_l^{s_l-1}\prod_{i<l}P_i^{s_i+s_{i+1}}.
$$
In fact $j_i(2r+1-j_i)-j_{i-1}(2r+1-j_{i-1})=s_i(2r+1+s_i-2j_i)$, giving the different weights of the block entries. Also $a_i-a_{i+1}=s_i+s_{i+1}$ and $a_l=s_l-1$. All exponents on the right are nonnegative. The sum of their level exponents after taking out $2f$ is $\sum_i s_i a_i-a_l=n(n-1)-(s_l-1)$, since $\sum_i s_i(j_i+j_{i-1})=n^2$. This proves the last mass comparison in (1) even on a cell with a vanishing penultimate minor. [Point and height definitions][pts] · [Block product identification][tel]

## Summing the real energies

Let $J_\tau$ denote the physical two-period operator and $M_\tau$ its big-cell integral with the same coefficient and ordinary complex coordinate measure. Use the physical point-to-section bound and the one-step leading-minor identity of the [shifted minor calculation](SPECTRAL_SHIFTED_MINOR_MOMENTS.md), including their stated large-gap, coefficient and wave estimates. Root measures may vary in the allowed window in the point estimate. With a fixed envelope $B=b^{C_H m^2}\ge1$ set $\sigma_\tau=\prod_{j\in B(\gamma)}\max(1,d_{\tau j}/B)$, $\sigma=\prod_\tau\sigma_\tau$. Here $B(\gamma)$ is the set of block ends. For any fixed $e\ge0$ with $e\le C_e m^2$, uniformly for the two ordered words, the sum over distinct represented points satisfies
$$
 \sum_\gamma w(\gamma) H(\gamma)^e p(\gamma)
                       \prod_\tau\|J_\tau(\gamma)\|_{\rm HS}^2
 \le R_0 b^{C m^5 f}\prod_\tau M_\tau,\qquad
 R_0=\frac{(9^f+2)^n}{g^{2rf}\rho^{2fr(r+1)}}.                   \tag{2}
$$
Here $w$ is the reciprocal-sum weight in the **raw** minor coordinates, whereas $p$ is the physical point weight in the different-scaled coordinates. The constant depends only on the fixed input constants and $C_e$.

To prove (2) retain the section-normalized estimate *before* converting its Jacobian to the ordinary $G_\tau^k$ bound. For $A=40n^2$ this estimate reads
$$
 p_\tau\|J_\tau\|_{\rm HS}^2
 \le M_\tau b^{C_3 m^4}\max(1,G_\tau^{-1})^A \sigma_\tau^{-2q/n}.
$$
To see the decay, multiply the normalized amplitude by the $q$-th power of the largest physical minor. The sum of absolute coefficients in the shifted expansion costs at most $b^{C_Dm^2q}$ before squaring, which is absorbed by $B^q$ when $C_H\ge C_D$. If all minors are below $B$, use the zeroth moment. The local $p_\tau$ multiply to the $p$ in (1). On this support, $\prod_\tau G_\tau=\widehat N_G\ge1$, and $0<G_\tau\le d_{\tau n}^2$. Hence $\prod_\tau\max(1,G_\tau^{-1})\le B^{2f}\sigma^2$. The original height definition gives
$$
 H=g^{-(2r+1)f}\widehat N_G\prod_iP_i
       \le B^{2(n+1)f}\sigma^4 .
$$
Since $u(j)\ge0$, $\rho\le b$ and the raw minor has magnitude $\rho^{u(j)}d_{\tau j}$,
$$
 w^2=\prod_{\tau,i}(1+|\tau D_{j_i}|^2)^4
 \le 16^{nf}\rho^{8f\sum_i u(j_i)} B^{8nf}\sigma^8 .
$$
Take $q=\lceil n(2A+4e+8)/2\rceil$. This is $O_{C_e}(m^3)$ and fits the available moment range on sufficiently late rows. The combined power of $\sigma$ is then nonpositive. The remaining constants are bounded by $b^{Cm^5 f}$ using $\sum_i u(j_i)\le n^3$. This bounds $w^2 H^e p\prod_\tau\|J_\tau\|^2$ pointwise by $b^{Cm^5f}\prod_\tau M_\tau$. Sum with $w^{-1}$ and use the point-only reciprocal bound $R_0$. The argument also proves absolute convergence of the displayed nonnegative energy. [Physical section and point bounds](SPECTRAL_ORDINARY_SQUARED_AMPLITUDE.md) · [Moment iteration](SPECTRAL_SHIFTED_MINOR_MOMENTS.md) · [Arithmetic reciprocal bound](SPECTRAL_CORANK_ONE_RECIPROCAL_SUM.md)

## The pinned section on the original row

Choose the source's physical word data at base scale one. Take $J_\tau^1$ at each represented point with its standard unit-root stabilizer measure and take $M_\tau$ on the big cell with the full ambient Haar measure. This is the integral in (2), since the common unipotent stabilizer on the big cell is trivial. Let $V_N(u)$ and $V_N(v)$ be the two integral unipotent covolumes at this base scale, and put $C_N=V_N(u)V_N(v)$. Then for the actual mass data and every compatible measurable choice of the diagonal sections one has
$$
 \prod_\tau M_\tau=C_N I_{\rm re},\qquad
 C_N J_2(\gamma)=g^{-2f e(\gamma)}
             \prod_\tau\|J^1_\tau(\gamma)\|_{\rm HS}^2,\qquad
 e(\gamma)=\sum_i s_i(s_i-1)/2.                                   \tag{3}
$$
In particular the scalar multiplying the product of section masses in the signed estimate is exactly $C_N^{-1}$, apart from the displayed cell factor. In these gauges $C_N=\rho^{f(2r^2+r)}$. [Source's section definition][mm] · [Two flag covolumes](SPECTRAL_STABILIZER_VOLUME.md) · [Unscaled pin and signed cell factor](SPECTRAL_SIGNED_CORANK_ONE_FIBRE.md)

Here is the constant calculation. Let $\kappa_\tau>0$ be the squared scalar carrying the original period coefficient to the local physical orbital coefficient. Multiplicity one and transport of the two fixed periods give the same scalar on all representatives. The original orbital square includes $s_0=|\mathrm{scl}(u,v)\operatorname{vol}K_2|^2$. Integrate the tensor product on the product of the local unit-root quotients. The double-coset section changes act by unitary transformations on each compact type, so preserve the Hilbert–Schmidt squares. The product of these squares therefore equals $(\prod_\tau\kappa_\tau/s_0)\|J_w\|^2$ for the original *unscaled* pin, also if the product vanishes. The period quotient norm identities, with the single-frame constants $c_0^{X}(u),c_0^{X}(v)$ in their level convention, give
$$
 (\prod_\tau\kappa_\tau)c_0^{X}(u)c_0^{X}(v)
       =(\operatorname{vol}K_2)^2 C_N,\qquad
 s_0=(\operatorname{vol}K_2)^2/[c_0^{X}(u)c_0^{X}(v)] .
$$
Thus the ratio is $C_N$. Scaling the original point quotient by $g^{-fe(\gamma)}$ gives exactly the second equation in (3). [Transport on the unit-root quotients][locpin] · [Product disintegration and original square][joint] · [Period constants][period] · [Exact covolume ratio][ratio] · [Scaling the point quotient][scpin]

For the section integral, let $\lambda_a=\rho^{-2(r-a)}$ for $0\le a<r$. Under the same transport each nonterminal diagonal complex coordinate is multiplied by $\lambda_a$. In the arithmetic-to-physical direction the inverse power from its Lebesgue area and its radial weight is $\lambda_a^{-2(M_a-1)}$, where $M_a$ is the source's diagonal weight index. Together with the planar-measure convention this gives the per-place factor $K_{\rm pl}=2^n\prod_{a<r}\lambda_a^{-2(M_a-1)}$. Changing these variables and applying Tonelli to positive squares yields
$$
  (\prod_\tau\kappa_\tau)I_C=K_{\rm pl}^{\,f}\prod_\tau M_\tau .
$$
The same calculation is independent of the diagonal representative by the double-coset invariance above. The admissible frame-passage identities give $I_C=c_0c'_0 K_{\rm pl}^{\,f} I_{\rm re}$, where $c_0,c'_0$ are the original mass-record constants with the ambient level divided out, and $(\prod_\tau\kappa_\tau)c_0c'_0=C_N$. Equivalently $c_0^X(u)=\operatorname{vol}(K_2)c_0$ and likewise on the other word. These equalities prove the first part of (3). Finiteness of $I_C$ on the supplied rows is the large-gap Bessel energy estimate. Here $M_a=2(r-a)+k+1$. The equalities also preserve zero energy without division by $I_{\rm re}$. [Diagonal Jacobian and product integral][coord] · [Original mass-record constants and exact section equality][section] · [Large-gap finiteness][energyfin]

## The nongeneric signed subtotal

Assume the original class-square identity and the convergence and local analytic hypotheses used in (2) and (3). Apply the [signed fibre bound](SPECTRAL_SIGNED_CORANK_ONE_FIBRE.md) at $k\ge60$, $f\le k$, under its standing size hypotheses and put $e=2+\max(2r(r+1),2m)+r(r+1)$. Insert (1) and the point identity (3) in the fixed-class [reciprocal Cauchy–Schwarz inequality](SPECTRAL_CORANK_ONE_RECIPROCAL_SUM.md). The factor from $L(s_l)$ and the signed pin is bounded uniformly by
$$
 \frac{g^{-2fe(\gamma)}}{L(s_l)}\le g^{-2fn(n-1)},
$$
since $e(\gamma)\ge s_l-1$. Use (2), then substitute (3) for the section masses. The $C_N$ factors cancel. With $\eta=1/2$ in the fixed-class reciprocal bound and the original arithmetic mass normalization
$$
 \Gamma_1 A_{\rm re} I_{\rm re}
   \le (\rho/2)^{fn}g^{fn(2r+3)}\Delta_{u,v}
$$
this gives
$$
 P(U_{\rm ng})\le
 9\,2^{32} f^2\,2^{-(k+1)}E_{\rm den}\, b^{C m^5 f}
 (2C_{1/2})^f(9^f+2)^{2n} 2^{-fn}
 g^{(2-2r)f}\rho^{fn(1-5r)}\Delta_{u,v}.                         \tag{4}
$$
For the normalization displayed above, changing from $I_C$ to $I_N$ introduces the ratio $V_{ZZ}/V_1$. Its inverse equals $\rho^{fn(8r^2+10r+3)/3}g^{fn(2r+3)}$. Inserting the diagonal frame-passage identities and the mass bound $\Gamma_1 A_{\rm mass}I_N/(c_0 c'_0)\le\Delta_{u,v}$ gives exactly the displayed factor. In (4) the exponents of $g,\rho$ are nonpositive for $r\ge1$. Enlarging $C$ absorbs the remaining finite factors and yields $P(U_{\rm ng})\le 2^{-(k+1)}b^{C m^5f}\Delta_{u,v}$. This proves the ordered-pair nongeneric summation on the specified analytic, arithmetic mean and mass inputs. Chen's point estimate and the repository's shifted-minor argument identify the local inputs to (2). The residual scalar sampling problem for different words concerns a separate quadratic form. [Original arithmetic normalization][pass] · [Signed class squares][squares] · [Chen's cell evaluation][chen]


The numerical saving in (4) depends on the order of the thresholds. After absorbing the displayed factors into $b^{C m^5 f}$, choose the final row constant $C_n\ge\max(C,2)$ and impose the source's mixed-row size condition $8C_n m^5 f\log b\le k$. Then
$$
 2^{-(k+1)}b^{C m^5 f}
 \le \tfrac12\exp[-(\log 2-1/8)k]
 \le \tfrac12 e^{-k/2}\le \tfrac12 b^{-8}.
$$
The last step uses $k\ge16\log b$. Without this size condition, (4) retains the two competing powers. At the stipulated size it puts the nongeneric contribution below the mixed row's $b^{-6}\Delta_{u,v}$ error allowance. That row still needs the distinct-word generic scalar estimate with leading coefficient one, the remaining coranks and the finite-type matrix estimate. The bound here is an upper bound on one class-square subtotal and establishes no independent lower bound for the common-period trace. [Distinct scalar and full mixed-row targets][mixed]


For the **equal-word generic scalar classes**, the same proof gives $P(U_{\rm sc})\le b^{C m^5 f}\Delta_{u,u}$. Indeed fix $v=u$, and partition generic terms by equality of row and the scalar corank-one equivalence. Symmetry and transitivity hold on represented generic terms. In this family the class-to-tuple computation selects just the empty set of positive-defect places. Thus the finite factor on the attained tuples is $|\prod_p Z_p(d_p)|^2$ with the same genus weights. At each active place its squared sum is at most $\mathcal W_p q_p^{2a_pm} n_{0,p}$, with $n_{0,p}\le4\mathcal W_p n_p^{\rm gen}$, and at height one there is exact reference normalization. Multiplying gives $H^{2+\max(2r(r+1),2m)}n_{\rm gen}$ as before. The common normal coordinates apply because two terms in one scalar equivalence class have the same row and satisfy the corank-one line relation. Consequently (1)–(3) and the identical class sum apply, with the factor $9\,2^{32} f^2 2^{-(k+1)}$ in (4) replaced by one. This is the coarse same-word estimate. [Scalar partner classes][sfam] · [Matched family and its zero-defect product][sfactor] · [Normal coordinates on these classes][snorm] · [Local zero-defect bound](SPECTRAL_COMPLEMENT_KERNEL_COUNTS.md)


[mass]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AbelianVarietyTheory/Proofs/FlagMeasures/FamilyGenericMassPositiveBoundedProof.lean#L21-L68
[wclass]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AbelianVarietyTheory/Proofs/FlagMeasures/MassClassEqWeightCount.lean#L231-L272
[count]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AbelianVarietyTheory/Proofs/FlagMeasures/HermitianFrameClassesTotalWeightLe.lean#L28-L50
[icoord]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AbelianVarietyTheory/Proofs/FlagMeasures/RmulMul.lean#L176-L254
[glue]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AbelianVarietyTheory/Proofs/FlagMeasures/GenericMassLeHeightPowMulGluedCount.lean#L142-L202
[glueprod]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AbelianVarietyTheory/Proofs/FlagMeasures/GenericMassLeHeightPowMulGluedCount.lean#L206-L238
[mean]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AbelianVarietyTheory/Proofs/FlagMeasures/GluedLatticeWeightedCountLeExplicit.lean#L81-L143
[const]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AbelianVarietyTheory/Proofs/FlagMeasures/MeanCountConstantEqUnscaledMainConstant.lean#L64-L85
[norm]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AbelianVarietyTheory/Proofs/FlagMeasures/NormsInvariantsGenericRationalFramePair.lean#L100-L120
[pts]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Formalism/LocalToGlobal/SiegelLatticeTheory/CokernelGLCounts/RowsConc.lean#L346-L380
[tel]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AbelianVarietyTheory/Proofs/FlagMeasures/GramInvariantPowLeHaarWeight.lean#L151-L196
[road]: https://github.com/rh-lean-roadmap/rh-lean-roadmap/blob/c535d69c2d028dd05547e05c4b0efde1225ce454/docs/src/book/main.tex#L45608-L45617
[pins]: https://github.com/rh-lean-roadmap/rh-lean-roadmap/blob/c535d69c2d028dd05547e05c4b0efde1225ce454/docs/src/book/main.tex#L45635-L45690
[chen]: https://github.com/yyyyychen/RH-Natural-Language-Proof/blob/d4dfb1a282dbf857288e73eb1f546dbfcc5899b8/tex/row-cell-evaluation.tex#L1-L36
[mm]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Formalism/SharpRestriction/CuspSpanNormBounds/NormalizedLocalScale.lean#L188-L194
[locpin]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Formalism/LocalToGlobal/SiegelLatticeTheory/FlagStabilizerTensors/RootLatticeThresholds/LocNorm.lean#L43-L65
[joint]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Formalism/LocalToGlobal/SiegelLatticeTheory/FlagStabilizerTensors/RootLatticeThresholds/TheoremBFixedOfExpansionLemmaJ.lean#L21-L49
[period]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Formalism/LocalToGlobal/SiegelLatticeTheory/FlagStabilizerTensors/RootLatticeThresholds/AmpWin.lean#L21-L29
[scpin]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Formalism/LocalToGlobal/SiegelLatticeTheory/CokernelGLCounts/RankPointCounts/NGAnalytic.lean#L208-L226
[coord]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/CompanionTheory/AutomorphicTheory/UniformLocalFormulas/HilbertSchmidtDiagonalInvariant.lean#L151-L212
[section]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/CompanionTheory/AutomorphicTheory/UniformLocalFormulas/UniformRestrictionOfEnergy.lean#L28-L61
[energyfin]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/CompanionTheory/AutomorphicTheory/UniformLocalFormulas/Closed.lean#L10-L18
[pass]: https://github.com/rh-lean-roadmap/rh-lean-roadmap/blob/c535d69c2d028dd05547e05c4b0efde1225ce454/docs/src/book/main.tex#L45577-L45592
[squares]: https://github.com/rh-lean-roadmap/rh-lean-roadmap/blob/c535d69c2d028dd05547e05c4b0efde1225ce454/docs/src/book/main.tex#L45709-L45717
[ratio]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Formalism/LocalToGlobal/SiegelLatticeTheory/FlagStabilizerTensors/RootLatticeThresholds/AmpWin.lean#L121-L146
[mixed]: https://github.com/rh-lean-roadmap/rh-lean-roadmap/blob/c535d69c2d028dd05547e05c4b0efde1225ce454/docs/src/book/main.tex#L18094-L18124
[sfam]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AbelianVarietyTheory/Proofs/FlagMeasures/GenericScalarClassTermsFormFamily.lean#L12-L26
[sfactor]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AbelianVarietyTheory/Proofs/FlagMeasures/GenericRowFamilyStepOfLeaves.lean#L48-L69
[snorm]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Formalism/LocalToGlobal/SiegelLatticeTheory/CokernelGLCounts/RankPointCounts/MainEqNml.lean#L38-L97
