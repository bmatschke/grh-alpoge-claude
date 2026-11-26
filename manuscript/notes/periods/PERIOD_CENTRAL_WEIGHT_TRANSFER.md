# The central-weight quotient and the discarded slope on the marked ray cover

Fix a sufficiently large member of a selected family and a nonterminal lift. Use the notation of the [selected reference determinant](PERIOD_SELECTED_REFERENCE_DETERMINANT.md). Thus $B$ is the deep integral cusp lattice in the rational pullback of the original type, $L_0$ the integral core type, $L$ its row realization, $e$ the retained orthogonal projector, and $C_b=(1-e)L$ its projected complement. Put $s=\mu(L_0)=\mu(B)-I$, $Z=frL_x$, $L_x=x^\epsilon$, $b=e^{L_x}$ and $U=E_p$. All slopes here use squared norms. Write $P$ for the fitted size parameter, $\kappa$ for the size of the actual central weight, and $M_i$ for the signed main term. Here $S$ is the subgroup of the deep-level automorphism group carrying the character.

At the selected scales the rank loss in the central-weight quotient costs $O(b/Z^{10})$ in squared slope. The discarded-type contribution to the reference log covolume has absolute value $O_N(bx^{-N})$ for each fixed $N$ under the native discarded-rank bound and parent cusp estimates. Consequently, if the negative-shift lattice satisfies $\mu(A)\ge-M_i-C_*U$ for a uniform $C_*\ge0$, the ensuing bound is

$$
\frac{\operatorname{lcv}(M_j)}{D_R}
  \le M_i+C_*U+O(b/Z^{10}).
\tag{1}
$$

In particular the transfer preserves the coefficient $C_*=C_F+C_U$ when it comes from the fitted degree and flat comparison. The bounds below specify the geometric and analytic inputs to this implication.

## The descent index at every coefficient prime

The core coefficient field $F$ contains the marked imaginary quadratic field. The selected deep extension $F'$ is its compositum with the ray class field of modulus $N_*=g_0g_1 15^e$. Write $m_*=15^e$. The [cyclotomic descent calculation](PERIOD_CYCLOTOMIC_DESCENT.md) gives

$$
m_* B\subseteq\mathcal O_{F'}\pi^*L_0\subseteq B,\qquad
0\le I\le 2\log m_*.
\tag{2}
$$

The local relative different clears the pullback lattice by trace duality. The marked cyclotomic coefficient pin removes the extra ramification at the two split level primes. Even the coarser integer $N_*$ suffices throughout this proof. Indeed, for any prime $\mathfrak p$ of the imaginary quadratic base and $\mathfrak P$ above it in its abelian ray field $R$, the different exponent divided by the ramification index is the mean of the conductor exponents $a_{\mathfrak p}(\chi)$ over the ray characters. Each exponent is at most $v_{\mathfrak p}(N_*)$. Hence $N_*\mathcal O_R\subseteq\mathfrak D_{R/H}$, with $H$ the imaginary quadratic base. The relative different after compositum divides the extended different. This gives the weaker annihilator $N_*$ at each coefficient prime as well. [Sized ray compositum][s6-ray] · [Trace-dual containment][s6-diff] · [Different under compositum and conductors][s6-cond]

## Short vectors at the actual central weight

Use $n=n_V$, the even column count of the selected member, and let $d_a$ be its harmonic degree. The native parameter equals $\kappa=d_a+frn/2$. The selected row satisfies $n\ge8fr+4$, its positive-block entries exceed $n/2$, and both signature blocks are nonempty. The good-cover estimates give $\log N_*\le30L_x$, $s_{\rm fld}(E)\le3L_x$, $\log(fr)\le L_x$, and $s_{\rm fld}(F')\le391Z^2$. Here $s_{\rm fld}$ is the source’s number-field size bound. In addition,

$$
 b/2\le\kappa\le4frb,\qquad |M_i|\le9rL_x\kappa,\qquad P\ge Z^{12}.
\tag{3}
$$

In particular $\log\kappa\le20L_x$ eventually. These are the conditions at the actual member at which the central even-weight theorem is used. [Actual column count, positive block and use of the theorem][s6-central] · [Identity for the harmonic degree][s6-kappa] · [Sharper signed main-term and weight-size bounds][s6-main] · [Lower bound on the fitted parameter][s6-host]

The three inputs to that theorem can be stated before choosing vectors in the quotient. At this weight the stable theta rules for the specified self-dual auxiliary lattices with integral harmonic polynomials span the full deep cusp space over $F'$. In the probability Petersson metric their analytic estimate includes the auxiliary lattice index to the power $r/2$. The determinant-ideal comparison supplies a nonzero scalar $s_\Lambda$ with $|\sigma s_\Lambda|[\Lambda:\Lambda\cap\mathcal O_E^n]^{r/2}\le e^{s_{\rm fld}(F')}$ for every embedding. The common additional clearing integer for the finite tests is

$$
N_a=\left(N_*^{frn+d_a}|\operatorname{disc}E|^{d_a}\right)^2.
$$

Since $frn+d_a\le2\kappa$, $d_a\le\kappa$ and $\log|\operatorname{disc}E|\le4fL_x$, its log is at most $(120+8f)L_x\kappa$. The source proves integrality at the level primes by separating first and higher prime powers, and uses the determinant-ideal scalar away from the level. These statements apply to every framed test of the deep rule space. The common scalar at the finite primes and the lattice-dependent scalar are both nonzero, so multiplying the spanning rules by them preserves their rational span. The archimedean supremum bound also bounds the Petersson norm because the underlying measure has mass one. This gives an integral spanning set of log length at most $C_\theta Z^2\kappa$ uniformly at all embeddings, using the native span, theta norm and finite-frame comparison theorems. Chen’s minimum-column construction for the moving weights can be read separately from this application at $n_V$. [Three theta estimates and their assembly][s6-assemble] · [Exact integer and its proof at every coefficient place][s6-int] · [Marked-level expression for the integer][s6-intform] · [Source for the determinant-ideal scalar][s6-scalar] · [Chen’s stable range][s6-stable]

The unnormalized $S$-trace with the inverse character takes these vectors integrally into $B$ because the character values are algebraic units. Reindexing gives the specified character, and on its eigenspace the trace is multiplication by $|S|$. Its norm is at most $|S|$, as each translate is isometric. Thus $B$ has an integral spanning set with log length

$$
H_B=C_\theta Z^2\kappa+45Z^2\le C_B Z^2\kappa
\qquad (\kappa\ge1).
\tag{4}
$$

Taking independent members and using Hadamard gives $\mu(B)\ge-2H_B$ even when their determinant spans a proper sublattice. [Character lattice on the marked cover][s6-type] · [Trace, integrality and the $45Z^2$ bound][s6-gmin]

## The fitted transfer loses little before computing any component height

Let $a=\operatorname{rk}A$, let $h$ be the rank of the saturated quotient of the direct sum of the trace targets by $\Phi A$, and put $\theta=h/(a+h)$. The opposite-direction multiplication map and the shifted rank estimate give $h/a\le b/(P\kappa)$. On this same cover the translating section at $c_0\lambda$ has multiplication norm at most $e^{C_v Z^9}$ and a group determinant nonzero on every component. Its character traces therefore have joint kernel zero and squared operator norm at most $e^{D_\Phi}$, with

$$
D_\Phi=2 C_v Z^9+135Z^2 .
$$

The $135$ comes from the three factors of $|S|$ in the summed squared norms. These inputs use the component orbit-separating evaluation and bounded integral realization of the translating section, and the rank comparison at the two shifted weights. [Use of the actual section and its marked weight][s6-maps] · [Translate determinant and quantitative construction][s6-translate] · [Two shifted ranks][s6-ranks]

Project the short vectors of (4) from each copy of $B$ onto the quotient. Their images still span and orthogonal projection does not increase norms. Wedge $h$ independent images. The result is an integral determinant vector of log length at most $hH_B$ at every embedding, with the unit of the rank-zero determinant understood when $h=0$. Apply the saturated determinant identity with $t=-M_i-C_*U-D_\Phi$. It gives

$$
\mu(B)\ge t-\theta(t+2H_B)
       \ge t-\theta(t+2H_B)_+ .
$$

Here $C_*U,D_\Phi\ge0$, so $t_+\le |M_i|$. Using (3) and (4) **before** replacing $H_B$ or $|M_i|$ by $P\kappa$ gives

$$
\theta(t+2H_B)_+
 \le \frac{b}{P}\bigl(9rL_x+2C_B Z^2\bigr)
 \le (9+2C_B)\frac{b}{Z^{10}}.
\tag{5}
$$

Since $Z$ is at most a fixed polynomial in $x$ and $b=\exp(x^\epsilon)$, $D_\Phi+I=o(b/Z^{10})$. It follows that $s\ge -M_i-C_*U-O(b/Z^{10})$. This estimate requires a lower bound for the negative-shift lattice only through its stated coefficient $C_*$.

## A two-sided bound for the projected complement

In the probability metric let $M_{\rm par}$ be the maximal squared slope of the full integral parent cusp lattice. At the primitive core frame the CM reading and the squared point-evaluation estimate give

$$
M_{\rm par}\le 2\lambda_s+2\log B_{\rm ev}+\log\operatorname{rd}(F)\le x^{A_0}b
$$

for a fixed exponent $A_0$. Here a nonzero integral cusp form has mean log supremum at least $-\lambda_s$, and its squared supremum is at most $B_{\rm ev}$ times its squared probability Petersson norm. Integrating the squared norm of point evaluation on an orthonormal basis gives the parent rank bound $\operatorname{rk}\le B_{\rm ev}$. Minkowski in each nonzero sublattice gives the first displayed inequality. To pass to the row field, take a common normal extension. Over this field the unique maximal destabilizing subspace is Galois stable, and its saturated intersection with the extended parent lattice descends by flatness. The same argument bounds subspaces of the parent after any further coefficient extension. This uses the parent CM and point-evaluation estimates with the marked Lie normalization. For the quotient volume, only an upper bound enters this argument. [CM norm reading][s6-cm] · [Probability evaluation, rank and Minkowski][s6-parent] · [Native parent bound at the pinned member][s6-nativepar] · [Field extension and saturation][s6-ext]

Let $g=|\mathcal G_p|$ be the denominator of the native projector in the sense that $g(1-e)L\subseteq L$. If $r_b>0$, the following bounds apply in the *same* probability metric:

$$
 -2(H_B+\log m_*)\le \mu(C_b)\le M_{\rm par}+2\log g,\qquad
 -2H_B-I\le s\le M_{\rm par}.
\tag{6}
$$

The upper bounds follow from inclusion in the parent lattice, multiplying $C_b$ by $g$ first. For its lower bound take the compositum of the deep and row coefficient fields over $F$. By (2), $m_*$ times each short vector in $B$ belongs to the extended core type. The integral row realization identifies this lattice with the extension of $L$. Projecting these vectors by $1-e$ now gives integral vectors in the extension of $C_b$ which span its rational space. Orthogonality makes projection contractive. Hadamard and invariance under base extension prove the lower bound, even if $C_b$ itself has no comparably short spanning family over the smaller field. This is where the annihilator in (2) is stronger than a normalized bound for the index.

The discarded-rank comparison on this member gives $r_b/r_t\le3\eta$ for $\eta=\exp(-x^{e_z/7})$, $e_z>0$, so $r_b/r_g\le4\eta$ eventually. For $r_b=0$ put the following term equal to zero. Otherwise (6) implies

$$
\left|\frac{r_b}{r_g}\bigl(\mu(C_b)-s\bigr)\right|
 \le 4\eta\left[(M_{\rm par})_+ +2H_B
                   +2\log m_*+2\log g+I\right].
\tag{7}
$$

Every bracketed term is at most $x^{A_1}b$ for a fixed $A_1$, by (2)–(4), $2\log g\le b$, and the parent estimate. This proves the stated two-sided bound without assuming the fitted lower bound on $\mu(A)$. The native small discarded rank uses the marked semisimple-label bounds and the two determinant-shift ranks for the relevant stabilizer subgroups. It is a separate geometric input. Finally the positive measure contribution in the reference determinant is at most $122fr^2L_x$, also $o(b/Z^{10})$. Substitution in the exact reference identity proves (1). [Discarded rank and its hypotheses][s6-badrank] · [Orthogonal projector and denominator][s6-project] · [Exact reference identity and one-sided measure estimate](PERIOD_SELECTED_REFERENCE_DETERMINANT.md)

The outstanding height calculation in (1) is the lower bound for $\mu(A)$ on the marked negative-shift lattice, notably its fitted component degrees and flat comparison. The quantitative transfer above uses the original good-cover theta, orbit separation, rank and parent-norm theorems at the sites indicated. The paired-reference comparison follows separately in the project.

[s6-ray]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AbelianVarietyTheory/Proofs/DivisorProofs/ExistsGoodCoverOverSizedField.lean#L111-L159
[s6-diff]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AbelianVarietyTheory/Proofs/DivisorProofs/GaloisStableLatticeRationalSpanInclusions.lean#L36-L46
[s6-central]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AutomorphicArithmetic/ThetaCorrespondence/ThetaPairLifts/ThirdPlaceSeries/CoveringMinGenusBound.lean#L34-L47
[s6-kappa]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AbelianVarietyTheory/Proofs/DivisorProofs/NormPhiHatIndPhi.lean#L49-L56
[s6-main]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AbelianVarietyTheory/Proofs/DivisorProofs/SizeBoundStatement.lean#L278-L300
[s6-host]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AbelianVarietyTheory/Definitions/Divisors/QuoIff.lean#L18-L30
[s6-assemble]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AbelianVarietyTheory/Proofs/DivisorProofs/EvenDomainWeightBound.lean#L109-L149
[s6-int]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AbelianVarietyTheory/Proofs/DivisorProofs/ExistsBoundedIntegerGoodCoverThetaSeriesIntegral.lean#L31-L118
[s6-intform]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AbelianVarietyTheory/Proofs/DivisorProofs/IsIntegralFourierCoeffClassIndicatorLevelPoint.lean#L23-L30
[s6-scalar]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AbelianVarietyTheory/Proofs/DivisorProofs/ExistsSmallScalarReflexIdealSelfDualLatticeStatement.lean#L13-L16
[s6-gmin]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AbelianVarietyTheory/Proofs/DivisorProofs/MinimalGenusBound.lean#L114-L147
[s6-maps]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AutomorphicArithmetic/ThetaCorrespondence/ThetaPairLifts/ThirdPlaceSeries/CoveringDescentMapsCompatible.lean#L43-L68
[s6-project]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AbelianVarietyTheory/Definitions/Divisors/CovolXOfCovol.lean#L61-L74
[s6-nativepar]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AutomorphicArithmetic/ThetaCorrespondence/FockModels/TamagawaPeterssonLambdaSqNonneg.lean#L596-L633
[s6-type]: https://github.com/yyyyychen/RH-Natural-Language-Proof/blob/d4dfb1a282dbf857288e73eb1f546dbfcc5899b8/tex/deep-cover-on-core.tex#L130-L163
[s6-stable]: https://github.com/yyyyychen/RH-Natural-Language-Proof/blob/d4dfb1a282dbf857288e73eb1f546dbfcc5899b8/tex/deep-cover-denominators.tex#L314-L339
[s6-translate]: https://github.com/yyyyychen/RH-Natural-Language-Proof/blob/d4dfb1a282dbf857288e73eb1f546dbfcc5899b8/tex/covolume-component-transfer.tex#L746-L798
[s6-ranks]: https://github.com/yyyyychen/RH-Natural-Language-Proof/blob/d4dfb1a282dbf857288e73eb1f546dbfcc5899b8/tex/covolume-component-transfer.tex#L1159-L1205
[s6-parent]: https://github.com/yyyyychen/RH-Natural-Language-Proof/blob/d4dfb1a282dbf857288e73eb1f546dbfcc5899b8/tex/parent-cusp-slope.tex#L100-L164
[s6-cm]: https://github.com/yyyyychen/RH-Natural-Language-Proof/blob/d4dfb1a282dbf857288e73eb1f546dbfcc5899b8/tex/parent-cusp-slope.tex#L53-L83
[s6-ext]: https://github.com/yyyyychen/RH-Natural-Language-Proof/blob/d4dfb1a282dbf857288e73eb1f546dbfcc5899b8/tex/parent-cusp-slope.tex#L166-L201
[s6-badrank]: https://github.com/yyyyychen/RH-Natural-Language-Proof/blob/d4dfb1a282dbf857288e73eb1f546dbfcc5899b8/tex/parent-cusp-slope.tex#L228-L273
[s6-cond]: https://github.com/rh-lean-roadmap/rh-lean-roadmap/blob/dc5594a62bb2b94139788df817db693cd939a046/docs/src/book/main.tex#L49684-L49691
