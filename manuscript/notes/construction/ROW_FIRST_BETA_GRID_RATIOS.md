# The normalized square constants on the last two grid columns

Let $g_t$ be the actual square constant on the prescribed grid at tuple $t$, with reference $0=\mu_0$. Write $K$ for the image of the specified coefficient-field embedding. Work at the scales, conductor depths, standard additive character and field data of the row construction. The conclusions use the standing Weil and local theta matching inputs, the definite doubling comparison and nonvanishing, the grid flip and block-witness construction, and the arithmetic clauses for the characters, bottom sums and critical Hecke values. On these inputs $g_t\ne0$ and $g_t/g_0\in K^\times$ for every square in columns $j=m-1$ and $j=m-2$ (when present). The last column has two definite sources. Its predecessor involves one descent to a definite triangle.

For $j=m-2$ put $e=(a-n)/2$, where $a,n$ are the big and small upper source ranks, and choose the standard arithmetic bottom triangle supplied by the grid condition `BottomIn`, on which the monomial sums satisfy `SumsIn`. Let $b_t$ be its constant witnessed by common polynomials. The more precise formula is
$$
 \frac{g_t}{g_0}
 =\eta_t\,\frac{b_t}{b_0}\,
   \frac{D_0^\beta}{D_t^\beta}\,
   \frac{L_0(e+1)}{L_t(e+1)},\qquad \eta_t\in\mu(K).
 \tag{*}
$$
The finite Hecke functions $L_u$ are those of the square character $\nu_u$ on $E$. Both local factors $D^\beta_0,D^\beta_t$ are evaluated using the same pair of adapted planes, local uniformizers and Haar conventions for $\{t,0\}$. All factors at $u=0$ use that same fitted base. The equality takes ratios on the given square and allows each comparison pair its own base. The ideal and Gauss factors can depend on this choice. The product in $(*)$ is intrinsic to the prescribed two grid constants. [Definition and arithmetic of the finite step](ROW_SQUARE_RATIOS.md) · [Fixed-model beta coefficient](ROW_FIRST_BETA_STEP.md)

## From the fixed model to the prescribed grid

Fix $i,\ j=m-2$. Write $0=\mu _0$, $T_t=\operatorname{locPl}(G,t)$, and $\xi_t=\nu_t/\nu_0$ for the finite twist, with $\xi_0=1$. Let $g_t$ be the nonzero regularized grid constant, $M_t$ the raw upper constant on the adapted model **with the two Haar measures fixed before comparing $t$ and $0$**, and $\ell_t$ the upper stage factor on its prescribed standard finite tests. For each $t$, use one fitting base, one adapted geometry and the same real quotient maps for the pair $\{t,0\}$. Denote the reference model constant for that choice by $M_0$. Then the normalized factor multiplying the fixed-Haar model recurrence is
$$
 \frac{g_t/M_t}{g_0/M_0}
 =\frac{\xi_t(y)}{\xi_0(y)}\,\frac{U_0}{U_t}\,
       \frac{\nu_0(k)}{\nu_t(k)}
 =\xi_t\!\left(\frac{y}{x^{(t)}k}\right).
 \tag{1}
$$
Here $y$ is a determinant-root idele for a single finite target translate, $x^{(t)}$ is an idele of local units on the chosen branches above the marked places, and $k$ records the change from the standard upper marking to the adapted upper marking. Thus this factor lies in the image of the individual finite twist. It is a root of unity in the specified coefficient-field embedding. [Grid comparison][fg-top] · [Finite order and coefficient field][fg-field]

**From standard finite tests to flipped tests.** Choose the common finite target translation $h$ carrying the standard doubled lattice to the grid lattice and a determinant root $y$ for $h$. In the two readings the translated standard vectors acquire scalars $c_A$ and $c_B\xi_t(y)$. Both $c_A,c_B$ are fixed across all tuples. At each $w\in T_t$ the relative factor of the standard zeta vectors is $\nu_{t,w}(x_w)$, where $x_w$ is a unit chosen before $t$. Put $U_t=\prod_{w\in T_t}\nu_{t,w}(x_w)$. For the actual flipped pair the relative zeta factor is $v_{t,w}^{-1}$, where $v_{t,w}=\mathrm{levVol}(G,t,i,j,w)\ne0$. This holds for **every** permitted depth and natural test after the partial Fourier transforms with their respective signs. On the restricted tensor product the remaining factors comparing the two local realizations are the same for the two pairs. Their product cancels. The standard tests used for this contraction have nonzero small image. If the ratio between the unshifted standard tests in the quotient is $a$, then the ratio for the flipped tests is
$$
 a\,c_A^{-1}c_B\,\xi_t(y)/(U_t V_t),\qquad V_t=\prod_{w\in T_t}v_{t,w}.
$$
The equation holds as an equality of vectors for every flip, including when both flipped images vanish. [Common translate and determinant root][fg-move] · [Both local zeta factors][fg-zeta] · [Contraction and cancellation][fg-tensor]

Write the grid measures as $A_t m,\ B_t m'$ in terms of the fixed stage measures. Set $C_B=B_0V_0$. Then $A_t=A_0$ and $B_tV_t=C_B$, by the small-level subgroup volume calculation. Multiplication by $A_t/B_t$ yields
$$
 \kappa_t=A_0c_A^{-1}c_B C_B^{-1}\xi_t(y)U_t^{-1}.
$$
Only real comparison scalars remain. Take the stage's fixed detecting small polynomial and lift its real quotient image after the fixed frame change to a big polynomial. Injectivity of the functional realization gives a proportionality of the two fixed polynomial images. Its scalar is independent of $t$ by the nonzero small image. The corresponding proportionality on the tied row relation is independent of $t$ by evaluation on a reference pair with nonzero real image, whose existence uses the big block witness. These two scalars multiply $\kappa_t\ell_t$ to give $g_t$. A further fixed real relation with the same vacua that carries square constants contributes one additional nonzero scalar independent of $t$. Dividing at the reference tuple gives $(g_t/g_0)/(\ell_t/\ell_0)=\xi_t(y)U_0/U_t$. [Explicit combined scalar][fg-formula] · [Big Haar][fg-haara] · [Small Haar and the level volumes][fg-haarb] · [Fixed real vectors and comparison of constants][fg-real] · [Change of real relation][fg-rel]

**From the standard marking to the beta-adapted marking.** On an upper stage read in its own standard split bases, the two prescribed standard test vectors have equal, nonzero finite quotient images. At an unmarked place this is the spherical vacuum and at a marked place the standard zeta pair gives the equality. Choose the fixed detecting real small polynomial $P'$ and lift its image under the common real model quotient to a big polynomial $P$. The stage factorization and the model identity give $\ell_u pP=M^{\rm std}_u p'P'$ for $u=t,0$, by injectivity of the functional realization. Cancelling the same $p'P'\ne0$ proves $M^{\rm std}_t/M^{\rm std}_0=\ell_t/\ell_0$. [Finite tests of the stage][fg-fintest] · [Detecting polynomial][fg-standard]

For one change of compatible markings, write $b_V,b_{V'},b_W$ and $\tilde b_V,\tilde b_{V'},\tilde b_W$ for the old and new split bases at $v$. The local unit is
$$
 k_v=\det(b_V^{-1}\tilde b_V)\det(b_{V'}^{-1}\tilde b_{V'})
                         \det(b_W^{-1}\tilde b_W).
$$
The matrices are integral invertible because they change bases of the same local lattices. In both mixed models evaluation of the unit vacuum at zero, whose value is one, fixes the scalar ambiguity of the coordinate intertwiner. Change of variables in the two zeta integrals shows that an old matched pair $(f,f')$ gives a new matched pair $(\nu_{u,v}(k_v)f,f')$, on the branch selected by the fitting base. At unmarked places the factor is one by unramifiedness on units. The finite scalar is consequently $\nu_u(k)$, where $k$ is the product of the corresponding embedded local ideles. The two twists have the same real splitting characters. They share the archimedean Cartan conjugations, real intertwiners and the scalar relating their two quotient maps. More explicitly, the big zeta function changes by $\beta(\det h)/\nu(\det g)$ and the small one by $\nu(\det g')\alpha(\det h)$ at the same shifted target argument, for the three basis changes $g,g',h$. The small multiplier divided by the big multiplier is $\nu(\det g\det g'\det h)$. The real changes consist of fixed source substitutions and a common target right translate on both functions. Schur uniqueness gives one additional scalar, common to the two twists. These substitutions are invertible, preserve primed support and act continuously on real Schwartz approximants. Applying them or their inverses carries the adapted identity itself to the prescribed presentation. [Local change of variables][cov] · [Transport of a matched pair][pair] Transport of the nonzero model identities gives
$$
 \frac{M_t}{M_0}=\frac{\nu_t(k)}{\nu_0(k)}\frac{\ell_t}{\ell_0}.
$$
If the construction compares both the adapted and standard readings with an intermediate one, then $k$ is the adapted change idele divided by the standard change idele. Reverse changes invert the determinants. The plane construction gives the same base and the same real maps for $t,0$ and may choose new ones for a different pair. Equation (1) uses the **upper** change idele. The lower one enters if its model constant is converted to a lower stage factor. [Three determinants and zeta covariance][fg-det] · [Finite idele][fg-rebase-fin] · [Archimedean transport][fg-rebase] · [Pairwise adaptation][fg-adapt]

Finally $T_0=W_0\subset T_t$, and every $w\in T_t\setminus W_0$ lies over a place outside $S_0$. There the reference numerator and denominator characters are unramified, hence $\nu_{0,w}(x_w)=1$. At every $w\in T_t$ one has $\nu_{t,w}=\xi_{t,w}\nu_{0,w}$. Taking $x^{(t)}$ to have component $x_w$ at each $w\in T_t$, and component one elsewhere including the conjugate branches, gives $U_t/U_0=\xi_t(x^{(t)})$. This proves the second equality in (1). Under the convention that the raw model uses **Darboux pushforwards of the grid measures** one has $M^{\rm push}_u=(A_u/B_u)M_u$. Therefore the literal coefficient in $g_u=\lambda_us_u M_u^{\rm push}$ satisfies
$$
 \frac{\lambda_t s_t}{\lambda_0s_0}
  =\frac{V_0}{V_t}\,\xi_t\!\left(\frac{y}{x^{(t)}k}\right).
$$
Multiplication by the quotient of measure transports restores (1) for the fixed-measure beta recurrence. [Marked branches][fg-places] · [Unramifiedness off the reference level][fg-unr] · [Local twists and base support][fg-u]

The calculation uses the [factorization for the actual standard tests](ROW_STAGE_STANDARD_TESTS.md), the normalized local quotient identifications, the regularized matched-test identity and block witness on this square, and the compatible model identities used in changing markings. In the pin the enclosing general theorems take the published-input collection, ThetaIntegralsAgree and LocalMatching as hypotheses. The local zeta and Haar formulas, tensor cancellation and change of markings on existing identities identify the normalized factor on these inputs. Independently varying the real quotient maps or the measures in the two models introduces additional scalar factors.

[fg-top]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AbelianVarietyTheory/Proofs/DivisorProofs/TopGridStagePolynomialExists.lean#L182-L192

[fg-field]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AbelianVarietyTheory/Proofs/DivisorProofs/XiAwayIm.lean#L16-L30

[fg-move]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AbelianVarietyTheory/Proofs/DivisorProofs/ThetaAtMove.lean#L62-L107

[fg-zeta]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AbelianVarietyTheory/Proofs/DivisorProofs/NotMemOfStanding.lean#L197-L229

[fg-tensor]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AbelianVarietyTheory/Proofs/DivisorProofs/TopGridStagePolynomialExists.lean#L94-L133

[fg-haara]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AbelianVarietyTheory/Proofs/DivisorProofs/ImportsRestRest.lean#L24-L43

[fg-haarb]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AbelianVarietyTheory/Proofs/DivisorProofs/GlResidueSurjective.lean#L317-L340

[fg-real]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AbelianVarietyTheory/Proofs/DivisorProofs/StageFactorNonvanishingScalars.lean#L195-L260

[fg-rel]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AbelianVarietyTheory/Proofs/DivisorProofs/ExistsNonvanishingFactorStage.lean#L34-L54

[fg-fintest]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AutomorphicArithmetic/LocalEmbeddings/StageGeoConst.lean#L46-L92

[fg-standard]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AutomorphicArithmetic/LocalEmbeddings/StageGeoConst.lean#L143-L178

[fg-det]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AutomorphicArithmetic/LocalEmbeddings/ReBaseZeta.lean#L204-L251

[fg-rebase-fin]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AutomorphicArithmetic/LocalEmbeddings/ReBaseMain.lean#L55-L99

[fg-rebase]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AutomorphicArithmetic/LocalEmbeddings/ReBaseMain.lean#L186-L222

[fg-adapt]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AbelianVarietyTheory/Proofs/DivisorProofs/TowerStageSuccessorCoefficients.lean#L353-L394

[fg-places]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AbelianVarietyTheory/Proofs/DivisorProofs/ValuationLeOneOfMem.lean#L226-L249

[fg-unr]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AbelianVarietyTheory/Proofs/DivisorProofs/SquareTowerFiniteFrame.lean#L395-L421

[fg-u]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AbelianVarietyTheory/Proofs/DivisorProofs/ExistsPowClose.lean#L82-L115

[fg-formula]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AbelianVarietyTheory/Proofs/DivisorProofs/TopGridStagePolynomialExists.lean#L216-L258


## The lower marking and the arithmetic bottom

Choose the [rational hyperbolic planes](ROW_BETA_RATIONAL_PLANES.md) in the small source and the common target. Their orthogonal complements give one definite triangle $Y$ for the whole family. Let $\ell_{1,u}$ denote the factor on its standard tests, and let $M_{1,u}$ be the lower model scalar with its fixed Haar measures. With $k_1$ the lower change-of-basis idele the same determinant calculation as above gives
$$
 \frac{M_{1,t}}{M_{1,0}}=\xi_t(k_1)\,\frac{\ell_{1,t}}{\ell_{1,0}} .
$$
The fixed-model beta identity gives $M_u=M_{1,u}/(C D^\beta_u L_u(e+1))$ for $u=t,0$ and one $C\ne0$ for the pair. In the additive and epsilon conventions of the [first beta calculation](ROW_FIRST_BETA_STEP.md),
$$
 D_u^\beta=\nu_u(\mathfrak b)^{-1}\nu_u(\mathfrak c)^{-1}
                   \prod_{v\in T_{u,F}}\epsilon_v(\nu_{u,\tau_v},-e).
$$
Here $T_{u,F}$ denotes the marked places of $F$ and the ideal values use unramified uniformizer readings at the support of the plane ideals. The arithmetic bottom can have different lattices and frames from $Y$. Transport the two common polynomials and compute the change of lattice by the determinant lifts of its three adelic isometries. The [bottom comparison](ROW_BETA_RATIONAL_PLANES.md#the-descended-bottom-and-the-specified-standard-bottom) gives $b_t/b_0=\zeta_t\,\ell_{1,t}/\ell_{1,0}$ with $\zeta_t\in\mu(K)$. This uses [injectivity for every prescribed definite finite vector](ROW_STAGE_STANDARD_TESTS.md) to identify any independently chosen family of constants on the same bottom. Existence of a standard bottom activates `BottomIn`, which supplies a possibly different standard bottom carrying the rational sums. Choose the latter in this comparison. [Standard bottom existence][botex] · [Arithmetic choice and its rational sums][botsums]

Multiply the upper and lower equations with (1). This proves $(*)$ with
$$
    \eta_t=\xi_t\!\left(\frac{y k_1}{x^{(t)}k}\right)\zeta_t^{-1}.
$$
The inverse on the upper change $k$ and the positive exponent on the lower change $k_1$ come from solving the recurrence for the upper grid constant. Both $\xi_t$ on ideles and the normalized bottom change take values in the embedded roots of unity. This also exhibits why the two levels may choose different marks. In the formal comparison one can absorb $\xi_t(k/k_1)$ into the first width ideal of the step at the cost of a common nonzero scalar, which drops out of the ratio. [Pairwise upper and lower constants][fg-adapt] · [Cancellation in the reduction][reduce] · [Equivalent change to the width ideal][width]

The finite linear system on the bottom arithmetic triangle gives $b_t/b_0\in K^\times$ using its rational monomial sums. The conductor calculation places $D_0^\beta/D_t^\beta$ in the units of $\mathcal O_K[1/Q_t]$, where $Q_t$ is the product of the norms of the new twisting primes. At the omitted base primes the primitive Hecke character is already ramified, so the Euler factors there are one. The nonzero critical ratio belongs to $K$ by the grid field hypothesis at $e+1$. These arguments use the original coefficient embedding. They give field membership for the product in $(*)$ without imposing a root-of-unity condition on the Hecke ratio or on the new-prime Gauss sums. [Bottom linear system](ROW_SQUARE_RATIOS.md#a-finite-linear-system-for-rational-periods) · [Hecke critical values](../galois/ROW_CRITICAL_HECKE_RATIOS.md) · [Prescribed field](ROW_COEFFICIENT_FIELD.md)

For $j=m-1$ start directly at the definite stage. The same top tensor and Haar calculation applies since it only uses the standard pair, the finite flip, its nonzero witness, and the common real relation. Transfer the definite stage to the prescribed arithmetic bottom as above. Thus $g_t/g_0$ is $b_t/b_0$ times a root of unity in $K$. There is no removed plane or critical Hecke value in this calculation. For $j=m-2$ the original grid law is the regularized identity $d(z)I_b=g_t I_s(z)$ at the prescribed endpoints for every allowed convergent $z$. The [full-rank replacement and block witness](ROW_FIRST_BETA_STEP.md#from-the-first-beta-model-to-the-grid-square) give this quantifier and $g_t\ne0$. The field conclusion is a two-column part of the all-square requirement.

[cov]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AutomorphicArithmetic/LocalEmbeddings/ReBaseZeta.lean#L26-L78
[pair]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AutomorphicArithmetic/ThetaCorrespondence/ThetaPairLifts/LocalTypeDictionary/DvReBaseMain.lean#L66-L111
[reduce]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AutomorphicArithmetic/ThetaCorrespondence/ThetaPairLifts/LocalTypeDictionary/SeesawFirstReductionLevel.lean#L40-L94
[width]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AbelianVarietyTheory/Proofs/DivisorProofs/SquareTowerStageRankFactorization.lean#L110-L139

[botex]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AbelianVarietyTheory/Proofs/TwistedOperators/BottomExistsIntegrable.lean#L104-L137
[botsums]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AbelianVarietyTheory/Definitions/TwistedInnerProducts/MemHalfCosetSelf.lean#L197-L231
