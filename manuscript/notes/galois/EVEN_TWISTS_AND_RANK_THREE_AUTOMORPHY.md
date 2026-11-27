# Even twists, cyclotomic class groups and rank-three automorphy

The cohomological height estimate must sum Selmer lengths over coefficient primes. Already at level two, its even twists detect eigenspaces in cyclotomic class groups. We compute that specialization, test a proposed published lifting theorem on its residual representation and identify the component-support question on the separate route used in the formal source.

## The level-two length and the cyclotomic class group

<!--
% BEGIN ETS1
-->

<span id="claim:ETS1"></span>Let $\ell$ be an odd prime, $e\ge2$ even with $(\ell-1)\nmid e$, and $M=(\mathbf Q_\ell/\mathbf Z_\ell)(-e)$. Write $S_\ell(e)$ for the subgroup of continuous $H^1(\mathbf Q,M)$ cut out by zero restriction to $D_\ell$ and to every finite inertia group away from $\ell$. The source takes the length of this group with zero restriction also at $D_2$ when $N=2$, $\psi=1$ and the coefficient ring is $\mathbf Z_\ell$. To compare these definitions, $I_2$ acts trivially, and an unramified class at $2$ is represented by an element of $M/(2^{-e}-1)M$. The scalar is nonzero in $\mathbf Z_\ell$, so multiplication by it is surjective on $M$. Every unramified local class at $2$ is therefore zero. The infinite place has order two and contributes zero in odd-primary cohomology. [Coefficient character and the two Selmer lengths](https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AutomorphicArithmetic/AutomorphicVarieties/CharacterLevelBounds/ShaFamMono.lean#L15-L34) · [Decomposition and inertia subgroups](https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AutomorphicArithmetic/AutomorphicVarieties/GaloisLibrary/SelmerTransport/ConjStableShaFam.lean#L92-L96) · [Kernel of local restrictions](https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AutomorphicArithmetic/AutomorphicVarieties/GaloisLibrary/SelmerTransport/ConjStableShaFam.lean#L164-L168) · [Normalized length](https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AutomorphicArithmetic/AutomorphicVarieties/HeightAndVanishing/DirichletPrimeToLPartMulLPowerPart.lean#L114-L120)

Let $F=\mathbf Q(\zeta_\ell)$, $\Delta=\operatorname{Gal}(F/\mathbf Q)$, and let $\omega$ be its mod-$\ell$ cyclotomic character. The groups $M^{G_{\mathbf Q}}$ and $M^{D_\ell}$ vanish. On the first torsion layer a generator of $\mathbf F_\ell^\times$ acts through its nontrivial $(-e)$-th power in each case, and a nonzero fixed element of any higher order would give a fixed element of order $\ell$. From $0\to M[\ell]\to M\xrightarrow{\ell}M\to0$ the global $\ell$-torsion therefore equals $H^1(\mathbf Q,\mathbf F_\ell(-e))$. The map from finite to divisible coefficients is injective on $H^1(D_\ell,-)$ by the same argument. At $v\ne\ell$ it is injective on $H^1(I_v,-)$ because $M^{I_v}=M$ is divisible. Thus the finite-coefficient group carries exactly these local kernels. The extra condition at $2$ was removed on divisible coefficients before this comparison.

Over $F$ the residual character is trivial. The outer terms in inflation–restriction vanish by averaging over $\Delta$ of order $\ell-1$. A global class now amounts to an additive character $f$ of $G_F$ with $f(\delta g\delta^{-1})=\omega^{-e}(\delta)f(g)$, where $\delta$ is lifted to $G_{\mathbf Q}$. Away from $\ell$, the inertia groups are the same on restriction since $F/\mathbf Q$ is unramified there. At $\ell$ the local restriction is injective since the index divides $\ell-1$. We obtain the unramified characters of $G_F$ that are trivial on the decomposition group at the unique prime $\lambda$ over $\ell$. Under Artin reciprocity these characters factor through $\operatorname{Cl}(F)/\ell$. The Frobenius of $\lambda$ there is trivial because $\lambda=(1-\zeta_\ell)$ is principal. This proves
$$
 S_\ell(e)[\ell]\simeq
 \operatorname{Hom}_{\Delta}\bigl(\operatorname{Cl}(F)/\ell,\,\mathbf F_\ell(-e)\bigr).
$$
The Artin map commutes with conjugation, so precisely the $\omega^{-e}$ eigenspace contributes to this Hom. The dimensions agree. In particular the full $\ell$-primary Selmer group vanishes exactly when this eigenspace vanishes. Even $e$ selects an even character. The group and coefficient at issue here are specified before taking any estimate over primes. [Milne, *Class Field Theory*, Theorem 0.4](https://www.jmilne.org/math/CourseNotes/CFT.pdf) · [Independent derivation, §17](https://github.com/jimjamzola/RH-Alpoge-Reconstruction/blob/b50dae1aa964142b04c11f791812ca7d4962e133/manuscript/sec17_twisted.tex#L74-L97)

<!--
% END ETS1
-->

## What the fixed-field counting estimate implies

<!--
% BEGIN ETS2
-->

<span id="claim:ETS2"></span>Take the single field $K=\mathbf Q(\sqrt{-7})$ that the repository uses in Case I for the principal target. Its discriminant is $-7$ and its class number is one, since the imaginary quadratic Minkowski bound $(2/\pi)\sqrt 7$ is less than two. Assume the source estimate $\mathrm{CorGK}$ for this $K$, keeping its quantifiers over the level, character and finite sets of primes. Fix $N=2$, $H=(\mathbf Z/2)^\times$, and $e\ge2$ even. For any finite set $L$ of primes $\ell\ge5$ with $\ell\ne7$ and $(\ell-1)\nmid 2e$, one has
$$
 \sum_{\ell\in L}\operatorname{length}_{\mathbf Z_\ell}S_\ell(e)\log\ell
 \ \le\ C(e+1)^A,\qquad C=2^{A+1}c_5(\log 11+\log 13),
$$
and all the lengths in the sum are finite. Here $c_5,A$ are the constants for this single field. [Fixed-field Case I and the principal target](../../../research/modules/arithmetic/count_i_aggregation/main.tex#L365-L385) · [The field of the principal target](../../../research/modules/arithmetic/count_i_aggregation/main.tex#L421-L430) · [Fixed-field estimate with its order of quantifiers](https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AutomorphicArithmetic/AutomorphicVarieties/UnitaryThreeGroups/KatoUse.lean#L44-L53)

Indeed the trivial character is the only member of the orbit. Its order is one, its inertia component is trivial, and its parity agrees with even $e$. The coprimality conditions follow from $\ell\nmid7$ and $(7,2)=1$. The kernel condition says here that $K$ is not contained in $\mathbf Q(\zeta_\ell)$. The quadratic field ramifies at $7$, whereas the cyclotomic field is unramified at $7$. This supplies every condition in the predicate $\mathrm{GD}$, including the displayed restriction on $2e$. Take the coefficient ring to be the image of $\mathbf Z_\ell$ in $\overline{\mathbf Q}_\ell$. It has ramification index one, so the normalized length equals the integral length of ETS1. The auxiliary primes $11$ and $13$ are distinct and prime to $30\cdot2\cdot7$. The two-integer argument for $\mathrm{CorGK}$ still applies when a summand has one of those characteristics, by using the other auxiliary prime. Finally $[\,(\mathbf Z/2)^\times:H\,]=1$. Substitution gives the asserted constant. [The admissibility predicate](https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AutomorphicArithmetic/AutomorphicVarieties/HeightAndVanishing/Counts.lean#L9-L23) · [Normalization by the ramification index](https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AutomorphicArithmetic/AutomorphicVarieties/CharacterLevelBounds/ShaFamMono.lean#L66-L76) · [The two auxiliary integers and the sum of valuations](https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AutomorphicArithmetic/AutomorphicVarieties/UnitaryThreeGroups/CorGSumLog.lean#L49-L73)

A nonzero $\omega^{-e}$ class-group eigenspace in ETS1 now forces $\log\ell\le C(e+1)^A$. This is a conditional bound on the size of the exceptional primes. It permits exceptional eigenspaces and gives no numerical cutoff without effective values of the constants. The manuscript's Case-I reduction uses only one field after it fixes a target. Its actual window levels form a smaller set than the levels quantified in $\mathrm{CorGK}$ for that field. A direct proof for those window levels would have to verify the precise character sums the height argument uses. [Case-I aggregation and its quantifiers](../../../research/modules/arithmetic/count_i_aggregation/main.tex#L459-L480)

<!--
% END ETS2
-->

## Integral eigenlines of the marked element

<!--
% BEGIN ETS3
-->

<span id="claim:ETS3"></span>Let $A$ be a complete Noetherian local coefficient ring, with residue field $k$, and let $r$ be a lift of the specified split rank-three residual representation. At a marked $g_1$, $\eta(g_1)=1$ and $u^2-1\in k^\times$ for $u=\bar\Psi(g_1)$. The linear factor of the split residual representation there is $\operatorname{diag}(u,1,u^{-1})$. Its eigenvalue differences are units because $u$, $u-1$, $u+1$ are units. The three simple roots of the reduced characteristic polynomial of $R=r(g_1)_{\mathrm{GL}_3}$ lift uniquely by Hensel's lemma to $\lambda_1,\lambda_2,\lambda_3\in A$, in their prescribed order. Their differences are units in $A$. The characteristic polynomial equals the product of the corresponding three linear factors by monic division and these unit differences. [The mark and its unit condition](https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AutomorphicArithmetic/AutomorphicVarieties/UnitaryThreeGroups/BaseRepGL3NormalisedOfPsiEqOne.lean#L68-L79) · [The three torus weights](https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AutomorphicArithmetic/AutomorphicVarieties/UnitaryThreeGroups/UnitaryThreeReflectionRight.lean#L235-L248) · [The split representation](https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AutomorphicArithmetic/AutomorphicVarieties/UnitaryThreeGroups/UnitaryThreeReflectionRight.lean#L291-L301) · [The marked subgroup and integral lift condition](https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AutomorphicArithmetic/AutomorphicVarieties/UnitaryThreeGroups/RhoKApply.lean#L68-L83)

In $A[R]$ take
$$
 E_i=\prod_{j\ne i}(R-\lambda_j I)(\lambda_i-\lambda_j)^{-1}.
$$
Chinese remaindering for the three comaximal factors and Cayley–Hamilton give $\sum E_i=I$, $E_iE_j=0$ for $i\ne j$, $E_i^2=E_i$ and $R E_i=\lambda_i E_i$. Each image is a direct summand of $A^3$. Reduction gives the corresponding one-dimensional residual eigenspace, so each image is a free $A$-line by projectivity over a local ring and Nakayama's lemma. A local map of such coefficient rings takes these projectors to the projectors with the same residual labels, by uniqueness of the Hensel roots. In particular the ordered decomposition is intrinsic to this mark and works integrally before passage to a field of points. This calculation controls the matrix of $g_1$. The automorphy assertion quantifies over the entire Galois representation at every point. [Stacks Project, §10.153, Henselian local rings](https://stacks.math.columbia.edu/tag/04GE)

<!--
% END ETS3
-->

## A test of the rank-three lifting theorem

<!--
% BEGIN ETS4
-->

<span id="claim:ETS4"></span>For $K=\mathbf Q(\sqrt{-7})$, $N=2$, $\psi=1$, $e=2$, $\ell=11$, the hypotheses $\mathrm{GD}$ used by the one-character estimate hold by ETS2, since $10\nmid4$. The residual character $\omega$ restricted to $G_K$ has order ten by $K\cap\mathbf Q(\zeta_{11})=\mathbf Q$. The untwisted constituents on $G_K$ are $\omega^2,1,\omega^{-2}$. In the normalization used for $\mathrm{IsAutI}$ the common twist is $\omega^{-1}$, so the constituents are $\omega,\omega^{-1},\omega^{-3}$. Each extends as a character of $G_{\mathbf Q}$ and hence is fixed by conjugation by complex conjugation on $G_K$. The conjugate-dual operation with the rank-three multiplier $\omega^{-2}$ fixes the middle character and exchanges the two distinct exterior characters. Thus the residual representation as a whole admits this duality, and its exterior constituents fail hypothesis (iv) of Allen–Newton–Thorne, Theorem 1.1. More generally, twisting all three untwisted constituents by a common $\xi$ could make each individually polarized with multiplier $\mu$ only if $\xi^c=\xi^{-1}\mu$ from the middle one. The exterior one would then require $(\omega^2)^c=(\omega^2)^{-1}$, contradicting its order five. This test concerns the residual hypothesis of a proposed lifting theorem. It is independent of whether a particular deformation component has any characteristic-zero Type-I points. [Character in the local datum](https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AutomorphicArithmetic/AutomorphicVarieties/UnitaryThreeGroups/RhoKApply.lean#L38-L46) · [Normalization of the Type-I representation](https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AutomorphicArithmetic/AutomorphicVarieties/UnitaryThreeGroups/RhoKApply.lean#L85-L91) · [Allen–Newton–Thorne, Theorem 1.1(iv)–(vi)](https://doi.org/10.1112/S0010437X20007484)

The theorem also pairs local conditions at an auxiliary place: the semisimplification of the lift has consecutive cyclotomic twists at that place and an automorphic seed there is an unramified twist of Steinberg. Producing a seed and proving support for every relevant component are substantive steps on the manuscript's route. In the native one-character theorem one fixes the complex embedding first. One then needs a *single* $g_1$ that is marked, gives a weight-zero algebra finite over the coefficient ring for every indicated deformation datum, supplies automorphy of every indicated Type-I point, and supplies modularity of every indicated rank-two extension at a Type-II point with fixed middle entry. ETS3 provides the integral projectors once the mark is given. Neither their distinctness nor a dimension count proves the assertions about points. [All four conditions at one mark](https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AutomorphicArithmetic/AutomorphicVarieties/AutomorphicCases/AutomorphyUnramifiedCoefficients.lean#L12-L27) · [The consumer after coefficient descent](https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AutomorphicArithmetic/AutomorphicVarieties/ModularityArgument/KatoQuadraticCharacters/OneChar.lean#L158-L176)

The source has a different route through a larger CM field and a linked frame. The rank-three descent theorem takes as inputs ordinary-compatible automorphy at the larger field's frame, a descent assertion, and ramification, flag and restriction conditions on every point to be descended. On that same frame the finiteness theorem obtains a finite-index subgroup working for all residual DVR points from the frame's finiteness assertion. These implications explain where a proof can supply the missing arithmetic. The component propagation argument also requires automorphic support on a starting component and control at the crossings for the components it reaches. To complete this route in prose one must construct the linked frame and its supported points in the original quantifier order (or supply the smaller estimates used on the chosen windows). The displayed counterexample rules out a direct application of the published Theorem 1.1 to all the residual triples at this step. [Rank-three descent with its assumptions](https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AutomorphicArithmetic/AutomorphicVarieties/ModularityArgument/ThresholdArguments/DenseThresholdCases/AutEnd3Alt.lean#L13-L21) · [Finite-index subgroup from a linked frame](https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AutomorphicArithmetic/AutomorphicVarieties/CurveDVRSpecialization/FinEndOfFinPt.lean#L9-L20) · [Component propagation in this repository](../../../research/modules/construction/arithmetic_component_propagation_v53/main.tex) · [Comparison with the recent reconstruction, §17](https://github.com/jimjamzola/RH-Alpoge-Reconstruction/blob/b50dae1aa964142b04c11f791812ca7d4962e133/manuscript/sec17_twisted.tex#L289-L305)

<!--
% END ETS4
-->

## The same obstruction after a change of CM field

<!--
% BEGIN ETS5
-->

<span id="claim:ETS5"></span>Let $\theta$ be a residual character of $G_{\mathbf Q}$ and restrict the triple $(\theta,1,\theta^{-1})$ to an arbitrary CM field $L$ inside $\overline{\mathbf Q}$. Allow any common character twist $\xi$ on $G_L$. Hypothesis (iv) of Allen–Newton–Thorne, Theorem 1.1, cannot hold for this triple over $L$. To see this, lift the CM involution to $G_{\mathbf Q}$. Since $\theta$ takes values in a commutative group and extends across this lift, $\theta^c=\theta$ on $G_L$. Denote the polarization multiplier by $\mu$. If $\xi$ and $\xi\theta$ both satisfy the individual constituent condition, division of their two character identities gives $\theta|_{G_L}=\theta^{-1}|_{G_L}$. In that case the outer constituents $\xi\theta$ and $\xi\theta^{-1}$ are equal. The residual semisimplification then has a repeated absolutely irreducible constituent, also excluded by (iv). If these outer constituents are distinct, one of the individual identities already fails. The argument applies to every common twist and to every such $L$, including a field over which $\theta$ becomes trivial. [Allen–Newton–Thorne, Theorem 1.1(iv)](https://doi.org/10.1112/S0010437X20007484) · [Diagonal restriction of the split representation](https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AutomorphicArithmetic/AutomorphicVarieties/UnitaryThreeGroups/UnitaryThreeReflectionRight.lean#L291-L301)

For the original arithmetic character one takes $\theta=\bar\chi_\ell^e\bar\psi$. This calculation specifies which base-change proposal the published theorem rules out. The source goes through automorphic support and descent on linked frames: it constructs two auxiliary realizations for ranks two and three and compares them on their common arithmetic points. The strengthened window theorem then uses its marked arithmetic conclusions along with the local and rank-four inputs. Thus validating this construction, or independently proving the required Selmer sums on the selected windows, would address the actual height estimate. [The two realizations and their conclusions](https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AutomorphicArithmetic/AutomorphicVarieties/ModularityArgument/ThresholdArguments/DenseThresholdCases/TwoRuns.lean#L80-L109) · [The strengthened marked producer](https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AutomorphicArithmetic/AutomorphicVarieties/ModularityArgument/ThresholdArguments/DenseThresholdCases/AutomorphyU3OfEndoscopy.lean#L27-L44) · [Passage from the strengthened inputs to the window bound](https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AutomorphicArithmetic/AutomorphicVarieties/ModularityArgument/ThresholdArguments/DenseThresholdCases/WindowBoundOfLiteratureLevel.lean#L25-L34)

<!--
% END ETS5
-->

## What a component-support proof must establish

<!--
% BEGIN ETS6
-->

<span id="claim:ETS6"></span>Let $R$ be a Noetherian deformation ring acting on a finite module $P$. Put $J=\ker(R\to\operatorname{End}(P))$. A prime $\mathfrak q$ lies in $V(J)$ exactly when $P_{\mathfrak q}\ne0$. In fact an element of $J\setminus\mathfrak q$ kills the localization, and if the localization vanishes a single product of denominators outside $\mathfrak q$ kills a finite set of generators. By Nakayama the same criterion detects $P\otimes_R\kappa(\mathfrak q)\ne0$. If a comparison homomorphism takes a point-prime to the coefficient ring by contraction, this is exactly the test that the corresponding modular ideal lies in the contracted prime. Proving this test at the generic prime of every component meeting the prescribed points suffices by specialization to all its points. If an eligible point is shared by components, its membership in the support alone gives the specialization conclusion only at that point. Passing in the other direction to the generic point of a different component requires more information. [Local propagation, seed and good-point predicates](https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AutomorphicArithmetic/AutomorphicVarieties/CurveDVRSpecialization/PropagationTheoremGL2.lean#L30-L47)

For an explicit finite free family let $W$ be a complete DVR, $\Lambda=W[[t]]$, and $R=\Lambda[X]/(X(X-t))$. This ring is finite free of rank two over $\Lambda$, with basis $1,X$. Its two components have generic ideals $(X)$ and $(X-t)$ and meet above $t=0$. Indeed evaluation at $0,t$ embeds $R$ in $\Lambda^2$ with image the pairs congruent modulo $t$. The module $P=R/(X)\simeq\Lambda$ is finite free and faithful over the weight algebra. Its support contains the entire first component and the intersection point $(X,t)$, since $J=(X)$. But $X$ is nonzero modulo $(X-t)$, where it becomes $t$. The second generic point is outside this support. Thus finite freeness over the weight algebra, a supported starting component and a connected component graph leave a genuine arithmetic condition at the crossing.

The formal propagation theorem states this condition in two forms. At a suitable Type-I prime, support must pass to the required primes contained in it. Across the exceptional rank-three locus, a sequence of *thick links* must transfer support from an incoming Type-I prime to every eligible outgoing Type-I prime. In the induction a thick vertex retains its incoming supported prime until the outgoing transfer applies. The argument first propagates rank-two support, uses it in the rank-three exceptional locus, then passes to the arithmetic points of both ranks. For a human proof on the host, the module supplied by the ordinary automorphic family must satisfy these transfer rules and carry the specified seed. Once the arithmetic points have been obtained, the separate descent theorem supplies the finite-index and marked conclusions under its stated hypotheses. [Invariant carried through an exceptional vertex](https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AutomorphicArithmetic/AutomorphicVarieties/CurveDVRSpecialization/LocProp.lean#L17-L43) · [Propagation around the connected chain](https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AutomorphicArithmetic/AutomorphicVarieties/CurveDVRSpecialization/LocProp.lean#L44-L75) · [Rank two, rank three and passage to points](https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AutomorphicArithmetic/AutomorphicVarieties/CurveDVRSpecialization/AbsMain.lean#L12-L30) · [Independent construction and its stated input boundary, §6](https://github.com/alexisdpc/riemann/blob/e985e0a7cba26c6c0f6acceb51c3bb4f2b7d74c5/technical.html)

<!--
% END ETS6
-->

## Removing the extra local conditions at the level primes

<!--
% BEGIN ETS7
-->

<span id="claim:ETS7"></span>Let $\ell$ be prime, let $O$ be one of the finite DVRs over $\mathbf Z_\ell$ in the source, and write $E_\ell=\operatorname{Frac}O$. For $e\ge1$ and a finite Dirichlet character $\psi$ of order prime to $\ell$, put $M_\psi=(E_\ell/O)(-e)\otimes\psi^{-1}$. This is the actual coefficient of the length $V'$ since $O$ is finite free over $\mathbf Z_\ell$ and $O\otimes(\mathbf Q_\ell/\mathbf Z_\ell)=E_\ell/O$. For $p\ne\ell$ consider a locally unramified cohomology class, i.e. a class trivial on $I_p$. Inflation–restriction places it in $H^1(D_p/I_p,M_\psi^{I_p})$. Inertia acts through the finite character at $p$. If this character is nontrivial, some inertia element acts by a root of unity of order prime to $\ell$ different from one. Its reduction also differs from one, so $M_\psi^{I_p}=0$. Otherwise $M_\psi^{I_p}=M_\psi$. Arithmetic Frobenius acts by $p^{-e}\psi(\mathrm{Frob}_p)^{-1}$. This scalar differs from one, since $p^e$ is not a root of unity. Multiplication by its difference from one is surjective on $E_\ell/O$. A cocycle on the procyclic quotient is determined by Frobenius, and its value is therefore a coboundary. In both cases triviality on inertia already implies triviality on $D_p$. [The allowed coefficient rings](https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AutomorphicArithmetic/AutomorphicVarieties/HeightAndVanishing/DirichletPrimeToLPartMulLPowerPart.lean#L10-L15) · [The divisible coefficient and twist](https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AutomorphicArithmetic/AutomorphicVarieties/GaloisLibrary/SelmerTransport/ConjStableShaFam.lean#L14-L35) · [The inverse character and lengths](https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AutomorphicArithmetic/AutomorphicVarieties/CharacterLevelBounds/ShaFamMono.lean#L15-L34)

Consequently adding every decomposition group over $N$ to the original strict condition at $\ell$ gives exactly the same kernel for these characters. In particular $V'=V$ here at *every* positive level $N$. The argument concerns the groups themselves, before taking lengths, so it applies also before finiteness has been proved. The prime-to-order hypothesis holds in the source's generic case. At a ramified prime with an $\ell$-power character the inertia invariants can be finite and the argument removing the decomposition condition need not apply. [Original inclusion for the two local conditions](https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AutomorphicArithmetic/AutomorphicVarieties/CharacterLevelBounds/ShaFamMono.lean#L42-L67) · [The generic coefficient-prime assumptions](https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AutomorphicArithmetic/AutomorphicVarieties/HeightAndVanishing/Counts.lean#L9-L23)

<!--
% END ETS7
-->

## All characters with one kernel occupy distinct summands

<!--
% BEGIN ETS8
-->

<span id="claim:ETS8"></span>Fix $N$ and a kernel $H$ occurring in the orbit of the source. Let $F=\mathbf Q(\zeta_N)^H$, $\Gamma=\operatorname{Gal}(F/\mathbf Q)$ and $d=[F:\mathbf Q]$. Then $\Gamma$ is cyclic and $d$ is the order of each character in this orbit. For $\ell\nmid d$ set $S_{F,\ell}(e)$ equal to the unramified-away-from-$\ell$ part of $H^1(F,(\mathbf Q_\ell/\mathbf Z_\ell)(-e))$ with zero restriction at each $v\mid\ell$. With $\ell$ odd the real places contribute zero. The analogous rational group with source coefficient $M_\psi$ and the additional level conditions in $V'$ is canonically identified, using the standard generator of the character line, with
$$
 (S_{F,\ell}(e)\otimes_{\mathbf Z_\ell}O)^{(\psi)}.
$$
Here $\Gamma$ acts on the first factor through its natural action on twisted cohomology, including the cyclotomic action on the coefficient. The superscript specifies the eigenspace on which $g$ acts as $\psi(g)$. [Characters, common kernel and cyclic quotient](https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AutomorphicArithmetic/AutomorphicVarieties/HeightAndVanishing/OrbFacts.lean#L17-L28) · [The character and its cyclotomic level subgroup](https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AutomorphicArithmetic/AutomorphicVarieties/CharacterLevelBounds/ShaFamMono.lean#L108-L128) · [Conjugation on the Selmer group and restriction](https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AutomorphicArithmetic/AutomorphicVarieties/GaloisLibrary/SelmerTransport/RestrictionMemInvariantH1.lean#L213-L231)

Indeed the degree $d$ is invertible on the coefficients, so the first and second cohomology groups of $\Gamma$ with values in any invariant submodule vanish by averaging. Restriction identifies rational cohomology with the invariant classes over $F$. At every finite prime the corresponding quotient of decomposition groups, and likewise of inertia groups, has order dividing $d$. Local restriction on degree-one cohomology is injective for the same reason. Thus each zero local restriction can be checked after passing to $F$, including at primes ramified in $F/\mathbf Q$. ETS7 removes the extra level conditions first. Over $F$ the finite twist is trivial. Taking the tensor with the finite free $O$ commutes with these kernels, as is also seen using a finite $\mathbf Z_\ell$-basis. Untwisting the $\Gamma$-invariance leaves the displayed $\psi$-eigenspace.

For two distinct characters in the orbit the integral operators $d^{-1}\sum_{g\in\Gamma}\psi(g)^{-1}g$ are orthogonal idempotents. This follows by summing the powers of the value at a generator. Their images form a direct sum in the single module $S_{F,\ell}(e)\otimes O$. When the latter has finite length, division by $e_O=\operatorname{length}_O(O/\ell O)$ gives the uniform orbit inequality
$$
 \sum_{\ker\psi=H} V_n(e,\psi)\ \le\
 \operatorname{length}_{\mathbf Z_\ell}S_{F,\ell}(e).
$$
Indeed $O/\ell^a O$ has length $a e_O$. There is no multiplicity factor for the number of characters in the orbit. The field $F$ is a function of $N,H$ alone, even when the coefficient ring is separately chosen at each prime. [The normalized quantity in the count](https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AutomorphicArithmetic/AutomorphicVarieties/HeightAndVanishing/DirichletPrimeToLPartMulLPowerPart.lean#L114-L120) · [The source orbit](https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AutomorphicArithmetic/AutomorphicVarieties/HeightAndVanishing/DirichletPrimeToLPartMulLPowerPart.lean#L140-L146) · [Order of the field, integer and coefficient-prime quantifiers](https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AutomorphicArithmetic/AutomorphicVarieties/UnitaryThreeGroups/KatoUse.lean#L36-L52)

<!--
% END ETS8
-->

## A finite integer controlling all eligible coefficient primes

<!--
% BEGIN ETS9
-->

<span id="claim:ETS9"></span>For a number field $F$, an odd prime $\ell$ and $e\ge1$, put $M=(\mathbf Q_\ell/\mathbf Z_\ell)(-e)$ and $T=\mathbf Z_\ell(e+1)$. Then
$$
 S_{F,\ell}(e)^\vee \ \simeq\
 \ker\!\left(H^2(G_{F,S},T)\longrightarrow
                 \bigoplus_{v\mid\ell}H^2(F_v,T)\right)
 \ \subseteq\ K_{2e}(\mathcal O_F)\otimes\mathbf Z_\ell ,
$$
where $S$ consists of the places above $\ell$ and infinity, and the dual is Pontryagin duality. The same assertion holds for $\ell=2$ if $F$ is totally imaginary. A class unramified away from $\ell$ factors through $G_{F,S}$ because inertia there acts trivially and the cocycle vanishes on the closed normal subgroup those inertia groups generate. Under these hypotheses the archimedean Tate cohomology in positive degree vanishes. [Inertia, decomposition and the absolute kernel](https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AutomorphicArithmetic/AutomorphicVarieties/CharacterLevelBounds/ShaAbsTop.lean#L137-L145) · [The quotient-group realization of the length](https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AutomorphicArithmetic/AutomorphicVarieties/CharacterLevelBounds/ShaAbsTop.lean#L194-L202)

Apply Poitou–Tate to the finite pair $\mathbf Z/\ell^a(-e)$ and $\mathbf Z/\ell^a(e+1)$, whose cup product takes values in $\mu_{\ell^a}$. The two local kernels in degrees one and two are perfect duals. The exact direct limit on the first side gives $S_{F,\ell}(e)$ since $S$ is finite and continuous cohomology of a profinite group with discrete torsion coefficients commutes with the direct limit. The dual inverse limit is the displayed kernel. The degree-one global and local groups with finite coefficients are finite, so their inverse systems satisfy the Mittag–Leffler condition and the continuous degree-two cohomology with lattice coefficients is the inverse limit. The comparison for primes inverted on $\mathcal O_F[1/\ell]$ identifies global Galois cohomology here with étale cohomology. The Quillen–Lichtenbaum calculation for number rings identifies $H^2_{\mathrm{et}}(\mathcal O_F[1/\ell],T)$ with the $\ell$-part of $K_{2e}(\mathcal O_F)$. Localization at $v\mid\ell$ causes no loss in this assertion: $K_{2e}(\kappa(v))=0$ and $K_{2e-1}(\kappa(v))$ has order $|\kappa(v)|^e-1$, prime to $\ell$. The even group of the ring of integers is finite by finite generation and Borel's rank formula. [Milne, *Arithmetic Duality Theorems*, I.4.10 and II.2.9](https://www.jmilne.org/math/Books/ADTnot.pdf) · [Weibel, *The K-book*, VI.8.1–8.2](https://sites.math.rutgers.edu/~weibel/Kbook/Kbook.VI.pdf)

Apply this to the character field $F$ of ETS8 and set $B_{N,H,e}=|K_{2e}(\mathcal O_F)|$. If the quotient with kernel $H$ is noncyclic there is no character with that kernel and one may take $B_{N,H,e}=1$. Otherwise this single positive integer is chosen before any coefficient prime, coefficient ring or auxiliary prime. At every odd $\ell$ for which an orbit member satisfies the source's generic predicate, $\ell\nmid d$. ETS8 and the injection above prove finiteness of every length in the orbit and
$$
 \sum_{\ker\psi=H} V_n(e,\psi)\le v_\ell(B_{N,H,e}),\qquad
 \sum_{\ell\in L}\log\ell\,\sum_{\ker\psi=H}V_n(e,\psi)
       \le \log B_{N,H,e}
$$
for any finite set $L$ of such primes. The second inequality follows by prime factorization. This proves the finiteness and valuation clauses in the one-integer construction with coefficient one. Its separate size clause requires a bound on the logarithm of an admissible integer with a fixed exponent as $e,N,H$ vary. Finiteness of the even $K$-group supplies the integer without that rate. For the rational trivial character with $(\ell-1)\nmid e$, the local $H^2$ is dual to $M^{D_\ell}=0$, so the entire $\ell$-primary $K$-group occurs. [Finiteness, valuations and the required uniform logarithmic size](https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AutomorphicArithmetic/AutomorphicVarieties/UnitaryThreeGroups/KatoUse.lean#L36-L53) · [Summation of prime valuations](https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AutomorphicArithmetic/AutomorphicVarieties/UnitaryThreeGroups/CorGSumLog.lean#L54-L73)

<!--
% END ETS9
-->

## Finiteness also at primes dividing the character order

<!--
% BEGIN ETS10
-->

<span id="claim:ETS10"></span>Fix any prime $\ell$, a finite Dirichlet character $\psi$, its coefficient DVR $O$, and $e\ge1$. The strict source group defining $V'(N,e,\psi)$ is finite, including when $\ell$ divides the order of the character. Write $F$ for the fixed field of its kernel in the cyclotomic field of level $N$. Use $L=F$ for $\ell$ odd and $L=F(i)$ for $\ell=2$. In the latter case $L$ has only complex places. On $G_L$ the module is $(\mathbf Q_\ell/\mathbf Z_\ell)(-e)\otimes O$. A Selmer class restricts to the kernel $S_{L,\ell}(e)\otimes O$ of ETS9, since zero on an inertia or decomposition group implies zero on its subgroup. This gives finiteness of the restriction image independently of any character idempotents. [The original length including level primes](https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AutomorphicArithmetic/AutomorphicVarieties/CharacterLevelBounds/ShaFamMono.lean#L23-L36) · [Restriction and the local kernels](https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AutomorphicArithmetic/AutomorphicVarieties/GaloisLibrary/GaloisCohomologyLength/ShaAbsRes.lean#L6-L17)

In inflation–restriction the possible kernel is $H^1(\operatorname{Gal}(L/\mathbf Q),M_\psi^{G_L})$. The cyclotomic image of $G_L$ is an open subgroup of $\mathbf Z_\ell^\times$, since $L$ has finite degree. Choose a cyclotomic value $u$ in it of infinite order. Then $u^{-e}-1\ne0$. The invariant module is contained in its kernel on $E_\ell/O$, which is finite. First cohomology of a finite group with a finite module is finite. This proves the assertion for the full preimage of the restricted Selmer group. For odd $\ell$, the group $\operatorname{Gal}(F/\mathbf Q)$ is cyclic of order $d$. Its first cohomology is a subquotient of the cyclic $O$-module $M_\psi^{G_F}$, by the cyclic resolution, and is killed by $d$ by restriction and corestriction. Its normalized length is therefore at most $v_\ell(d)$. The restriction argument gives $V_n(e,\psi)\le v_\ell(d)+v_\ell(|K_{2e}(\mathcal O_F)|)$ also for these primes. The sharper sum with no orbit multiplicity is available when $\ell\nmid d$ by ETS8–9. [Base change and the coefficient length of a scalar](https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AutomorphicArithmetic/AutomorphicVarieties/GaloisLibrary/SelmerTransport/ConjStableShaFam.lean#L16-L35) · [Order of the cyclic character field](https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AutomorphicArithmetic/AutomorphicVarieties/HeightAndVanishing/OrbFacts.lean#L17-L23)

In particular at fixed $F,e$ only finitely many odd primes can contribute, since the two integers just exhibited have finite prime support. The same holds for fixed $F$ and a finite range of positive twists, by taking a finite union. These are pointwise results as the host field and the twist range vary. They do not give the uniform height estimate on windows. [Finite lengths and the summed length as distinct clauses](https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AutomorphicArithmetic/AutomorphicVarieties/CharacterLevelBounds/ShaFamMono.lean#L69-L77)

<!--
% END ETS10
-->

## The exact primitive part and the least possible integer

<!--
% BEGIN ETS11
-->

<span id="claim:ETS11"></span>Fix an orbit as in ETS8 and let $A=K_{2e}(\mathcal O_F)$. For $\ell\nmid d$ take the idempotent $P_d$ of the primitive characters of $\Gamma$, namely the sum of the character projectors for characters of exact order $d$. This is defined in $\mathbf Z[1/d][\Gamma]$. For a generator $\gamma$, the coefficient of $\gamma^j$ is $d^{-1}\sum_{(b,d)=1}\zeta_d^{-bj}$, an algebraic integer divided by $d$ and fixed by every automorphism of $\mathbf Q(\zeta_d)$. The idempotent is independent of the generator and is invariant under inversion. For each coefficient prime for which an orbit member satisfies $\mathrm{GD}$ one has the exact equality
$$
 \sum_{\ker\psi=H}V_n(e,\psi)
       =m_\ell,\qquad
 m_\ell=\operatorname{length}_{\mathbf Z_\ell}
                   P_d(A\otimes\mathbf Z_\ell).
$$
A faithful character identifies $\Gamma$ with the full group of $d$th roots of unity in the coefficient ring, so all primitive characters occur in the orbit. [Conjugate powers and the full primitive orbit](https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AutomorphicArithmetic/AutomorphicVarieties/HeightAndVanishing/OrbFacts.lean#L17-L27) · [The orbit summed by the count](https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AutomorphicArithmetic/AutomorphicVarieties/UnitaryThreeGroups/KatoUse.lean#L36-L52)

It suffices to show that the local degree-two target in ETS9 has zero primitive part. Its dual is $\bigoplus_{\lambda\mid\ell} ((\mathbf Q_\ell/\mathbf Z_\ell)(-e))^{G_{F_\lambda}}$ by local Tate duality. After tensoring with $O$ the $\psi'$-part is identified, by choosing one $\lambda$ and using the transitive $\Gamma$-action, with $M_{\psi'}^{D_\ell}$. Explicitly an eigenvector in this sum is determined by its coordinate at $\lambda$ with the eigencharacter condition for the stabilizer. Twisting that coordinate by $(\psi')^{-1}$ makes it fixed by $D_\ell$. On inertia at $\ell$ the restriction of $\psi$ is its $\ell$-level component, since the roots of unity of order prime to $\ell$ are unramified. The source assumes that this component squares to one. Each primitive power $\psi'=\psi^b$ therefore also has inertia square one. Writing $\omega$ for the residual cyclotomic character, the square of the residual character of $M_{\psi'}$ on inertia is $\omega^{-2e}$. It is nontrivial by $(\ell-1)\nmid2e$ and the total ramification of $\mathbf Q_\ell(\mu_\ell)/\mathbf Q_\ell$. Thus $M_{\psi'}^{D_\ell}=0$, since any nonzero invariant would give one of order the coefficient uniformizer. This proves the required vanishing over $O$ and hence over $\mathbf Z_\ell$ by finite freeness and faithful flatness. Applying $P_d$ to the kernel in ETS9 and using invariance of $P_d$ under duality gives the equality of lengths. This avoids choosing a trace-dual lattice for a ramified coefficient field. [Quadratic inertia component and nondivisibility](https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AutomorphicArithmetic/AutomorphicVarieties/HeightAndVanishing/Counts.lean#L9-L23) · [Projection to the level prime](https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AutomorphicArithmetic/AutomorphicVarieties/HeightAndVanishing/DirichletPrimeToLPartMulLPowerPart.lean#L64-L81) · [Local and global Tate duality](https://www.jmilne.org/math/Books/ADTnot.pdf)

There is now an exact size test for the one-integer route. Fix the quadratic field $K$ of that route and its data $N,H,e,p$. Among the odd primes $\ell\ne p$ with $\ell\mid |A|$, retain those at which *some* allowed coefficient datum has an orbit member satisfying $\mathrm{GD}$ for this $K$. The integer
$$
 M_{K,N,H,e,p}=\prod_{\ell\ {\rm retained}}\ell^{\lceil m_\ell/2\rceil}
$$
is determined before choosing any later $\Omega,\ell,O$. It satisfies all the required inequalities $\sum V_n\le2v_\ell(M)$ simultaneously, including when an eligible prime lies outside $|A|$. Conversely, for every retained prime use a witnessing coefficient datum in the universal assertion. The equality just proved shows that any nonzero witnessing integer must have valuation at least $\lceil m_\ell/2\rceil$. Thus its absolute value is a multiple of $M$. If the orbit can never occur the empty product works. A polynomial upper bound of the size required in $\mathrm{PropGK}$ for this explicit product is necessary and sufficient for that particular route. The alternative on the original restricted windows may ask for less. [Size and universal integer in the original proposition](https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AutomorphicArithmetic/AutomorphicVarieties/UnitaryThreeGroups/KatoUse.lean#L36-L43)

<!--
% END ETS11
-->

## Detecting zero lengths by class groups and reflection

<!--
% BEGIN ETS12
-->

<span id="claim:ETS12"></span>At an odd generic prime let $L=F(\mu_\ell)$ and $\Delta=\operatorname{Gal}(L/\mathbf Q)$. Its order divides $d(\ell-1)$ and is prime to $\ell$. For a character in the orbit write $\theta=\omega^{-e}\bar\psi^{-1}$ in the residue field $k$ of $O$. It is nontrivial on inertia at $\ell$ by ETS11. Its parity is even because the finite character's parity agrees with $e$. Write $\mathcal S_\psi$ for the original strict Selmer group. With $\pi$ a uniformizer of $O$ there is an isomorphism
$$
 \mathcal S_\psi[\pi]\ \simeq\
 \operatorname{Hom}_{k[\Delta]}
     \big((\operatorname{Cl}(L)/\ell)\otimes_{\mathbf F_\ell}k,\,k(\theta)\big).
$$
As in ETS1 the exact sequence for multiplication by $\pi$ identifies the global first layer, since the global and $\ell$-local invariants are zero. At $p\ne\ell$, inertia invariants on divisible coefficients are zero or divisible by ETS7, so the maps on finite-coefficient inertia cohomology are injective. Over $L$ the residual character becomes trivial. Restriction is an isomorphism onto invariants globally and injective at every inertia and decomposition group, since the relevant quotient groups have order prime to $\ell$. Artin reciprocity over $L$ gives equivariant class characters once all inertia is killed. Their values on the classes of primes $\lambda\mid\ell$ must be zero to obtain the strict condition. A decomposition group fixes $[\lambda]$, and $\theta$ is nontrivial on that group, so every equivariant homomorphism already kills $[\lambda]$. This replaces the principality argument of ETS1 in fields where such primes can represent nontrivial ideal classes. [The twist whose first layer is being tested](https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AutomorphicArithmetic/AutomorphicVarieties/CharacterLevelBounds/ShaFamMono.lean#L15-L34) · [The local subgroups](https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AutomorphicArithmetic/AutomorphicVarieties/GaloisLibrary/SelmerTransport/ConjStableShaFam.lean#L92-L96) · [Hilbert class field and the Artin map](https://www.jmilne.org/math/CourseNotes/CFT.pdf)

We give the reflection test to see which of these contributions already vanish. Let $H_L/L$ be the maximal everywhere unramified elementary abelian $\ell$-extension. Its Galois group is $\operatorname{Cl}(L)/\ell$. Since $L$ contains $\mu_\ell$, Kummer theory pairs this group perfectly with a radical $D\subset L^\times/L^{\times\ell}$ into $\mu_\ell$. The pairing is $\Delta$-equivariant. After scalar extension to $k$, a $\theta$-part of the Galois group has a dual radical part with character $\eta=\omega\theta^{-1}$. For a representative $a$ of an element of $D$, every valuation of $a$ is divisible by $\ell$. Indeed in the unramified Kummer extension the valuation of its $\ell$th root is integral. Thus $(a)=\mathfrak b^\ell$, and the map $a\mapsto[\mathfrak b]$ takes $D$ to $\operatorname{Cl}(L)[\ell]$. Its kernel consists of radicals represented by units.

The field $L$ is abelian CM. For a unit $u$, $u/\bar u$ has all conjugates of modulus one and is a root of unity by Kronecker's theorem. Since $\ell$ is odd, the minus part of the units modulo $\ell$ is therefore generated by roots of unity. Its only possible character is $\omega$: $[L:\mathbf Q]$ is prime to $\ell$, so $L$ contains $\mu_\ell$ and does not contain $\mu_{\ell^2}$. The character $\eta$ is odd and differs from $\omega$, since $\theta$ is even and nontrivial. Consequently the $\eta$-part of the radical injects into the $\eta$-part of $\operatorname{Cl}(L)[\ell]\otimes k$. Vanishing of the latter forces $\mathcal S_\psi[\pi]=0$ and hence $\mathcal S_\psi=0$, because this is a $\pi$-primary torsion module. This gives an arithmetic zero criterion for each generic orbit member, including nontrivial characters. [The parity and genericity used here](https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AutomorphicArithmetic/AutomorphicVarieties/HeightAndVanishing/Counts.lean#L14-L22) · [Sharifi, Kummer theory and reflection for cyclotomic class groups](https://www.math.ucla.edu/~sharifi/misc/aws-iwasawa.pdf)

<!--
% END ETS12
-->

## Unconditional zero contributions for the trivial character

<!--
% BEGIN ETS13
-->

<span id="claim:ETS13"></span>Take $\psi=1$, any level $N$, any even $e\ge2$, and an odd $\ell$ with $(\ell-1)\nmid e$. By ETS7 and ETS1 the whole strict Selmer group is zero if and only if the $\omega^{-e}$ eigenspace in the $\ell$-part of the class group of $\mathbf Q(\mu_\ell)$ is zero. Thus the following four tests remove actual terms from the sum.

* If $5\le\ell$ and $e\equiv2$ or $4\bmod(\ell-1)$, the exponents of the eigenspaces are $\ell-3$ and $\ell-5$ respectively. Kurihara proves vanishing in the first case. Dutour Sikirić, Elbaz-Vincent, Kupers and Martinet deduce it in the second case from $K_8(\mathbf Z)=0$. The excluded trivial residual character is already outside the stated hypotheses. [Kurihara, Corollary 3.8](https://www.numdam.org/item/CM_1992__81_2_223_0.pdf) · [Dutour Sikirić et al., Theorem 6.4 and Corollary 7.1](https://arxiv.org/pdf/1910.11598)
* For $\ell>3$ with $\ell\equiv3\bmod4$ and $e\equiv(\ell-3)/2\bmod(\ell-1)$, the exponent $-e$ equals $(\ell+1)/2$ modulo $\ell-1$. This even eigenspace vanishes by Osburn's Theorem 1.1. [Osburn, Theorem 1.1](https://maths.ucd.ie/~osburn/van.pdf)
* Let $k_0$ represent $-e$ in the even range $2\le k_0\le\ell-3$. If $\ell$ does not divide the numerator of $B_{k_0}$, Herbrand's theorem gives zero for the odd class eigenspace $\omega^{1-k_0}$. Indeed its nonvanishing would force that divisibility. The Kummer argument of ETS12 transfers the vanishing to $\omega^{k_0}$, since the reflected character is $\omega^{1-k_0}$. For the trivial character this argument needs only $(\ell-1)\nmid e$, which makes the $\ell$-local residual character nontrivial. To pass between $\ell$-torsion and reduction modulo $\ell$ in either eigenspace, lift its character by Teichmüller and apply the integral idempotent of the group of order $\ell-1$ to the finite class group. A finite abelian $\ell$-group vanishes exactly when either its first layer or its reduction does. [Ribet, §1, statement of Herbrand's implication](https://math.berkeley.edu/~ribet/Articles/invent_34.pdf) · [Nelson’s worked irregular pairs](https://github.com/ultronozm/grh-workbook/blob/8590e35eb9a6e8cd07d546bd5b3b115ebac9672a/20261125T004000--denominators-and-sha__workbook.tex#L148-L166)
* For every odd $\ell<2^{31}$ the published computation of Hart, Harvey and Ong verifies the vanishing of the entire even part, including at irregular primes. For clarity, extension and norm between the maximal real subfield and the cyclotomic field identify the $\ell$-primary class group of the real subfield with the plus part: their composites are multiplication by two and $1+c$, and two is a unit. The even $\omega^{-e}$ eigenspace is contained there. [Hart, Harvey and Ong, §1, item (2)](https://arxiv.org/abs/1605.02398)

For example, at $\ell=37$ and $e=4$ the reflected Bernoulli test involves $B_{32}$, whose numerator is divisible by $37$. The $K_8$ result nevertheless gives strict length zero at this irregular prime. At $e=2$, $\ell=11$, the arithmetic contribution in ETS4 likewise vanishes, even though this residual representation fails the published lifting hypothesis. A failure of that citation need not force any nonzero summand at the test input. For a nontrivial $\psi$, the relevant class group is the larger one in ETS12. [The source group to which vanishing applies](https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AutomorphicArithmetic/AutomorphicVarieties/CharacterLevelBounds/ShaFamMono.lean#L23-L34) · [The nonnegative contributions in the sum](https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AutomorphicArithmetic/AutomorphicVarieties/UnitaryThreeGroups/KatoUse.lean#L44-L52)

<!--
% END ETS13
-->

## The rate obtainable from present torsion bounds

<!--
% BEGIN ETS14
-->

<span id="claim:ETS14"></span>There is a quantitative application of ETS9 for characters of bounded order and bounded positive twist. Let $d=[F:\mathbf Q]$, $m=2e$, $n=2m+1=4e+1$ and $b=dn+1$. Since $F$ is abelian over $\mathbf Q$, it is totally real or CM. De la Torre Durán's Theorem 4.5 applies to the part of $K_{2e}(\mathcal O_F)$ at primes greater than $b$. For any finite set $L$ of *eligible* coefficient primes $\ell>b$, the orbit inequality and that theorem give
$$
 \sum_{\ell\in L}\log\ell\sum_{\ker\psi=H}V_n(e,\psi)
 \ \le\
 \exp\!\big(O(n^2d(\log n+\log d))\big)\,|D_F|^{O(n^2)} .
$$
Here the occurrence of $n$ on the right is the dimension parameter in the torsion estimate. The subscript in $V_n$ on the left denotes normalization by the ramification index, as in ETS8. This application respects the restriction on torsion primes in the cited theorem. Each of the $d$ characters of $\operatorname{Gal}(F/\mathbf Q)$ has conductor dividing $N$, so the conductor–discriminant formula gives $|D_F|\le N^d$. On any fixed bounded range of $e$ and $d$ the expression on the right is therefore bounded by a polynomial in $N$ with constants depending only on those two bounds. This supplies that portion of the uniform count for all eligible $\ell>b$. [De la Torre Durán, §4, Theorem 4.5 and Remark 4.6](https://arxiv.org/pdf/2611.06300) · [Milne, *Class Field Theory*, conductor–discriminant formula](https://www.jmilne.org/math/CourseNotes/CFT.pdf) · [Required dependence on the twist and level](https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AutomorphicArithmetic/AutomorphicVarieties/UnitaryThreeGroups/KatoUse.lean#L36-L52)

Even for $F=\mathbf Q$ the estimate supplied by this substitution for the logarithm of the large-prime torsion order is $\exp(O(e^2\log(2e)))$. The desired logarithmic bound at $N=2$ has size $C(e+1)^A$. The exponents in the preprint’s estimate thus do not establish the desired rate by substitution. ETS11 gives a sharper object whose size suffices, since it keeps only the eligible primitive pieces. ETS13 also eliminates the indicated residues, regular Bernoulli pairs and a finite range of primes for the trivial orbit. Controlling the remaining primitive orders uniformly as the twist and level vary is the unresolved quantitative arithmetic question on this route. The selected-window alternative keeps its own quantifiers. [Eligibility of the remaining primes](https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AutomorphicArithmetic/AutomorphicVarieties/HeightAndVanishing/Counts.lean#L9-L23) · [Fixed constants and auxiliary primes in the source](https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AutomorphicArithmetic/AutomorphicVarieties/UnitaryThreeGroups/CorGSumLog.lean#L37-L54)

<!--
% END ETS14
-->

## The full strict Selmer group and the local correction on the host

<!--
% BEGIN ETS15
-->

<span id="claim:ETS15"></span>Let $E$ be a totally imaginary number field of degree $n$ and let $e\ge1$. Write $A(E,e)=K_{2e}(\mathcal O_E)$ and $\mathcal S_\ell(E,e)$ for the original strict group on that field. On every coefficient prime ETS9 identifies its dual with the localization kernel in $A(E,e)\otimes\mathbf Z_\ell$. This identification respects field automorphisms. Cup products, the sum of local invariants and the étale Chern comparison are all natural, and the Pontryagin dual has the contragredient action. Choosing different extensions of the same places conjugates the restriction maps and preserves the kernels. Thus it holds for every choice of local data in the source. In particular all the prime and twist lengths on a fixed CM host are finite, including at two. [Global and local kernels in the source](https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AutomorphicArithmetic/AutomorphicVarieties/CharacterLevelBounds/ShaAbsTop.lean#L137-L145) · [Conjugation on the two strict groups](https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AutomorphicArithmetic/AutomorphicVarieties/LengthEqAddEigen.lean#L64-L92) · [Global duality](https://www.jmilne.org/math/Books/ADTnot.pdf) · [Number-ring comparison, VI.8.2](https://sites.math.rutgers.edu/~weibel/Kbook/Kbook.VI.pdf)

Local duality bounds the index of this kernel by the product of the orders of $(\mathbf Q_\ell/\mathbf Z_\ell)(-e)^{G_{E_v}}$ over $v\mid\ell$. If such a group contains an element of order $\ell^a$, the image of $G_{E_v}$ in $(\mathbf Z/\ell^a)^\times$ has exponent dividing $e$. Its index is at most $[E_v:\mathbf Q_\ell]\le n$, by intersecting $E_v$ with the local cyclotomic field. For odd $\ell$ the group of units is cyclic, so it contains at most $e$ elements killed by the $e$th power map. At two the units modulo $2^a$ are a product of at most two cyclic groups, one of order at most two, so this kernel has at most $2e$ elements. In either case $\varphi(\ell^a)\le2en$ and hence $\ell^a\le4en$. Each local invariant group is a subgroup of the cyclic torsion at this bounded exponent. There are at most $n$ places above each prime and at most $4en$ possible primes. It follows that
$$
0\le\log|A(E,e)|-\sum_\ell\log|\mathcal S_\ell(E,e)|
  \le 4 e n^2\log(4en).
$$
The sum is finite since each dual is a subgroup of the indicated primary part of one finite group. This controls the total local correction uniformly before choosing a prime set. [Prime weights and the contribution at two](https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AutomorphicArithmetic/AutomorphicVarieties/LengthEqAddEigen.lean#L107-L131) · [Local Tate duality, I.2](https://www.jmilne.org/math/Books/ADTnot.pdf)

<!--
% END ETS15
-->

## Descent of the sign at ramified primes and the special value

<!--
% BEGIN ETS16
-->

<span id="claim:ETS16"></span>Let $E\subset\mathbf Q(\mu_N)$ be CM, $F=E^+$, $n=[E:\mathbf Q]=2s$, and $c$ complex conjugation. Put $m=e+1\ge2$ and $\delta=(-1)^m$. For every odd $\ell$, the eigenspace called $\mathcal S_\ell^-$ in the source has eigenvalue $\delta$. ETS15 gives an injection of its dual into the same eigenspace of $A(E,e)\otimes\mathbf Z_\ell$, since $\delta^{-1}=\delta$. The two sign projectors $(1\pm c)/2$ are integral for all these primes, including primes dividing $n$. [The sign on the cohomology with its coefficient twist](https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AutomorphicArithmetic/AutomorphicVarieties/LengthEqAddEigen.lean#L64-L88) · [Action on the original field](https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AutomorphicArithmetic/AutomorphicVarieties/OddResidueBounds/ZeroMemUnrHom.lean#L44-L55)

The $c=1$ part of $A(E,e)\otimes\mathbf Z_\ell$ is $A(F,e)\otimes\mathbf Z_\ell$. Here is a descent argument also at a finite prime ramified in $E/F$. Let $\pi:\operatorname{Spec}\mathcal O_E[1/\ell]\to\operatorname{Spec}\mathcal O_F[1/\ell]$. For $T_a=\mathbf Z/\ell^a(m)$ the sheaf $\pi_*\pi^*T_a$ has stalk the product of copies of $(T_a)_{\bar y}$ over the geometric points above $\bar y$. They form a single orbit under $1,c$, including the one-point orbit at a ramified prime. The action on the pulled-back stalks is the canonical permutation, so their invariant part is the diagonal copy of $T_a$. Finite direct image is exact, and the projector $(1+c)/2$ splits the sheaf. Taking cohomology and then the inverse limit identifies the invariant degree-two cohomology with that of the base. The inverse-limit identification uses finiteness of the finite-coefficient degree-one groups as in ETS9. Apply the natural number-ring comparison over both fields. This proves descent for the full group used to bound the strict length. [Stacks Project, Proposition 59.55.2](https://stacks.math.columbia.edu/tag/03QN) · [Weibel, VI.8.2](https://sites.math.rutgers.edu/~weibel/Kbook/Kbook.VI.pdf)

Let $Z_m$ be the product of $L(1-m,\chi^*)$ over the characters of $\operatorname{Gal}(E/\mathbf Q)$ with $\chi(-1)=(-1)^m$, using their primitive inducing characters. Exactly $s$ characters have each sign since $c$ is nontrivial. For $m$ even $Z_m=\zeta_F(1-m)$, by the abelian factorization into primitive Dirichlet functions, with the Euler factors at ramified primes included in that factorization. Wiles's odd-primary special-value theorem gives
$$
v_\ell\!\left(\left|A(E,e)_\ell^{c=1}\right|\right)
     =v_\ell\big(w_m(F) Z_m\big),
\qquad
w_m(B)=\big|H^0(B,(\mathbf Q/\mathbf Z)(m))\big|.
$$
For $m$ odd one has $m\ge3$ and $Z_m=L(E/F,1-m)$ for the nontrivial quadratic character of $E/F$. This identity follows by cancelling the even Dirichlet factors as functions *before* evaluation. Kolster's higher relative class number formula gives the odd valuations of $w_m(E)Z_m$ as those of $h_m(E)/h_m(F)$. At odd primes $h_m(B)$ is the order of the same degree-two group as $A(B,e)$. The descent just proved therefore identifies this valuation with that of $|A(E,e)_\ell^{c=-1}|$. Both special values are nonzero and rational. These are odd-primary identities, so the undetermined power of two in the general formulas introduces no hypothesis. [Wiles’s theorem and the higher special-value formula, VI.8.7–8.8](https://sites.math.rutgers.edu/~weibel/Kbook/Kbook.VI.pdf) · [Voight, §1, Proposition 1.3, giving Kolster’s formula](https://jvoight.github.io/articles/higherrel-062618.pdf) · [The two sums as distinguished by the source](https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AutomorphicArithmetic/AutomorphicVarieties/LengthEqAddEigen.lean#L113-L125)

<!--
% END ETS16
-->

## A single integer bounding all odd valuations of the critical value

<!--
% BEGIN ETS17
-->

<span id="claim:ETS17"></span>For the host of ETS16 put $D=mN(m+1)!$ and let $w$ be the odd part of $w_m(F)$ for even $m$ or $w_m(E)$ for odd $m$. We first prove $w\mid D$. Both fields are contained in $\mathbf Q(\mu_N)$. For an odd prime $\ell\nmid N$ the cyclotomic image of $G_{\mathbf Q(\mu_N)}$ is all $\mathbf Z_\ell^\times$, by the Chinese remainder theorem on each finite cyclotomic extension. Invariants of order $\ell^a$ then require $\ell-1\mid m$ and $a\le1+v_\ell(m)$. For $\ell\mid N$, set $b=v_\ell(N)$. The image contains $1+\ell^b\mathbf Z_\ell$ by the same finite cyclotomic argument. The binomial expansion gives $v_\ell((1+\ell^b)^m-1)=b+v_\ell(m)$, since $\ell$ is odd. A fixed element of order $\ell^a$ forces $a\le b+v_\ell(m)$. Together these bounds show $w\mid Nm\prod_{\ell-1\mid m,\,\ell\ {\rm odd}}\ell$, which divides $D$. [Higher roots of unity as cyclotomic invariants, Voight §1](https://jvoight.github.io/articles/higherrel-062618.pdf) · [The cyclotomic restriction in the source](https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AutomorphicArithmetic/AutomorphicVarieties/OddResidueBounds/ZeroMemUnrHom.lean#L15-L35)

For a primitive character $\chi^*$ of conductor $f\mid N$, summing the Hurwitz zeta function in residue classes gives
$$
 L(1-m,\chi^*)=-\frac{f^{m-1}}m
                 \sum_{a=1}^f\chi^*(a)B_m(a/f).
$$
Here $B_m(y)=\sum_{j=0}^m\binom mj B_j y^{m-j}$ and all $(j+1)!B_j$ are integers. The latter follows by induction from $\sum_{j=0}^{k}\binom{k+1}jB_j=0$ for $k\ge1$. After expansion, the factor $f^{m-1}(a/f)^{m-j}$ is $a^{m-j}f^{j-1}$. Thus $D L(1-m,\chi^*)$ is an algebraic integer, also for $f=1$. To bound its absolute value use the generating series $z/(e^z-1)$. On $|z|=1$ its modulus is at most $(3-\exp(1))^{-1}<4$ by the exponential series. Cauchy's estimate gives $|B_j|\le4j!$ and the polynomial expansion gives $|B_m(y)|\le4\exp(1)m!<12m!$ for $0\le y\le1$. Therefore $|L(1-m,\chi^*)|\le12(m-1)!N^m$. [NIST DLMF, Hurwitz zeta at negative integers](https://dlmf.nist.gov/25.11.E14) · [Primitive character and the cleared Bernoulli value](https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AutomorphicArithmetic/AutomorphicVarieties/OddResidueBounds/ZeroMemUnrHom.lean#L71-L85) · [Nonvanishing at the required parity](https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AutomorphicArithmetic/AutomorphicVarieties/StickelbergerCharacterEval/GroupRingCharEvalStickelbergerYNeZeroOfParity.lean#L14-L29)

The $s$ factors in ETS16 are stable as a set under conjugation of their character values, so $D^s Z_m$ is a nonzero rational algebraic integer. The positive integer $I_m=|wD^s Z_m|$ is divisible by the order of the whole odd part of the $\delta$-eigenspace in the sense of ETS16, namely the product of the corresponding orders over the odd primes. In fact its valuation at every such prime is that order's valuation plus $s v_\ell(D)$. This passage through an integer controls odd numerators even when $Z_m$ has a power of two in its denominator. We have the simultaneous bound
$$
 I_m\ \le\ D^{s+1}\{12(m-1)!N^m\}^{s}.
$$
The formula uses primitive characters at their own conductors. No removal of an Euler factor at a prime dividing the larger $N$ enters the bound. [Size of the cleared value in the original argument](https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AutomorphicArithmetic/AutomorphicVarieties/OddResidueBounds/ThmBcOfPsiBound.lean#L110-L145)

<!--
% END ETS17
-->

## The complete odd-minus window estimate on the original fields

<!--
% BEGIN ETS18
-->

<span id="claim:ETS18"></span>For every abelian CM field $E\subset\mathbf Q(\mu_N)$, set $n=[E:\mathbf Q]$ and let $t\ge2$ be an integer. For every finite set $S$ of odd primes and every original local-data family one has
$$
 \sum_{\ell\in S}\log\ell \sum_{1\le e<t}
     \operatorname{length}_{\mathbf Z_\ell}\mathcal S_\ell(E,e)^{c=(-1)^{e+1}}
 \ \le\ (n+1)t^2\log(tN).
$$
For fixed $m=e+1$, ETS16–17 bound that contribution over all odd primes by $\log I_m$. Finiteness of each subgroup already follows from ETS15. Put $u=\log(tN)$, so $n\ge2$, $N\ge3$ and $2\le m\le t$. The bounds $mN\le tN$ and $m+1\le tN$ give $\log D\le(m+2)u$. Also $(m-1)!N^m\le(tN)^m$ and $12\le(tN)^2$. Hence $\log I_m\le(2s+1)(m+2)u=(n+1)(m+2)u$. Finally $\sum_{m=2}^{t}(m+2)=(t-1)(t+6)/2\le t^2$, since $(t-2)(t-3)\ge0$ for integers $t\ge2$. Nonnegativity permits restriction to every input prime set. [All finite odd-prime sets and every local datum](https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AutomorphicArithmetic/AutomorphicVarieties/LengthEqAddEigen.lean#L113-L119) · [Original field and conductor in the minus estimate](https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AutomorphicArithmetic/AutomorphicVarieties/OddResidueBounds/ThmBcOfPsiBound.lean#L147-L168)

In the source's field predicate the set of cyclotomic moduli containing $E$ is nonempty. Its least member $N=\operatorname{condF}(E)$ is positive and itself admits an embedding. Transport to its image identifies the strict groups and the complex conjugation on the originally specified field, for any choice of the ambient closure. Now $(n+1)\le3n$ and the first term in $\operatorname{minusBound}(C,o,n,N,t)$ is $3nt^2\log(tN)$. Thus $C=0$ witnesses the literal assertion $\mathrm{ThmBcFree}$. This includes odd primes dividing the field degree or conductor. In particular ETS16–18 give a second proof of OB8 directly from the special-value theorems, independent of the character annihilators used in OS1–9. The other sign is $c=(-1)^e$. At the corresponding special values its characters have the parity of a trivial zero, so the nonzero product used here measures only the minus contribution in the source's convention. [Cyclotomic embedding and the least conductor](https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AutomorphicArithmetic/AutomorphicVarieties/StmtFields.lean#L36-L45) · [The exact first and exceptional terms](https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AutomorphicArithmetic/AutomorphicVarieties/StmtFields.lean#L69-L71) · [The free minus estimate](https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AutomorphicArithmetic/AutomorphicVarieties/PrimeSetBoundDataOfPrimitiveChar.lean#L64-L68) · [OB8, the character-annihilator proof](../../../research/modules/construction/odd_minus_bounds/main.tex#L756-L827)

<!--
% END ETS18
-->

## The complementary K-group estimate on the selected windows

<!--
% BEGIN ETS19
-->

<span id="claim:ETS19"></span>For an abelian CM host $E$ and cutoff $t$, let $W(E,t)=\sum_{\ell}\sum_{1\le e<t}\log|\mathcal S_\ell(E,e)|$, including $\ell=2$. Bounding this sum is equivalent to bounding the original sums over all finite prime sets, because ETS15 gives finite support at this fixed field and cutoff. Write $A_\ell(e)=K_{2e}(\mathcal O_E)\otimes\mathbf Z_\ell$. Define the integer $P(E,t)$ by taking, for each $e$, the order of $A_2(e)$ times the product of $|A_\ell(e)^{c=(-1)^e}|$ over the odd primes, and multiplying these integers for $1\le e<t$. Then
$$
 \log P(E,t)-4n^2t^2\log(4nt)
 \ \le\ W(E,t)\ \le\
 \log P(E,t)+(n+1)t^2\log(tN).
$$
For the upper bound, apply the injection of ETS15 at two and on the $(-1)^e$ eigenspace at odd primes. ETS18 supplies the other strict eigenspace. For the lower bound, its nonnegative contribution can be dropped. On the retained eigenspaces the index of the dual strict group is at most the order of the full local target in ETS15. The same index bound holds without projecting at two. Sum that claim over the twists, using $\sum_{1\le e<t} e\le t^2$. There is no use of a sign projector at two. [The dyadic term, both odd terms and the window sum](https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AutomorphicArithmetic/AutomorphicVarieties/LengthEqAddEigen.lean#L107-L131) · [Assembly on the same field and prime set](https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AutomorphicArithmetic/AutomorphicVarieties/LengthEqAddEigen.lean#L133-L145)

On the source windows both explicit errors fit below the allowed height with room to spare. Indeed, let $m_0$ be the fixed initial modulus and $h(x)$ the power-of-two layer. The host embeds in the cyclotomic field of modulus $\operatorname{lcm}(2^{h(x)+2},m_0,q,d)$. To check this even if a larger containing modulus is used to witness the field predicate, an automorphism fixing these four cyclotomic subfields has exponent congruent to one at all four moduli. It meets the defining kernel condition and fixes the given host. Take $N$ to be its least cyclotomic modulus. Then $n\le N\le 2^{h(x)+2}m_0 qd$. With $2^{h(x)}\le x^4$, $t\le x^{401}$, $x\ge X^{1/J}$ and $\log(qd)\le X^{\varepsilon/(4J)}$, one has $\log(Nt)\le2x^{\varepsilon/4}$ once $x$ is large for $m_0,\varepsilon$. Both error terms are therefore at most $\exp(C x^{\varepsilon/4})$ for an absolute $C$ above that threshold. In particular a bound for $\log P(E,t)$ with any fixed margin below $\exp(\frac12 x^\varepsilon)$ suffices on the very same windows. Conversely any proposed bound for $W(E,t)$ controls this product up to the displayed additive error. Obtaining that remaining size estimate on a common family is a separate arithmetic question. The stronger fixed-field alternative for its generic character orbits has the exact criterion in ETS11. [Kernel describing the actual host](https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AutomorphicArithmetic/AutomorphicVarieties/StmtFields.lean#L36-L45) · [Bounds on layer and twist functions](https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AutomorphicArithmetic/AutomorphicVarieties/PrimeSetBoundDataOfPrimitiveChar.lean#L23-L27) · [Order of window thresholds and auxiliary primes](https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AutomorphicArithmetic/AutomorphicVarieties/PrimeSetBoundDataOfPrimitiveChar.lean#L41-L53) · [Independent reconstruction, window definition and decomposition](https://github.com/jimjamzola/RH-Alpoge-Reconstruction/blob/b50dae1aa964142b04c11f791812ca7d4962e133/manuscript/sec17_twisted.tex#L104-L152)

<!--
% END ETS19
-->

## An exact nonzero Selmer contribution over the ninth cyclotomic field

<!--
% BEGIN ETS20
-->

<span id="claim:ETS20"></span>Take $E=\mathbf Q(\mu_9)$, $n=6$, and $e=2$, so $m=3$. We compute the entire contribution from the minus sign at the odd primes in this example. The group $(\mathbf Z/9)^\times$ is generated by $2$ and has order six. Let $z$ be a primitive sixth root with $z^2=z-1$. Of the three odd characters, the one sending $2$ to $-1$ is induced by the nontrivial character modulo three. The other two, sending $2$ to $z$ and $\bar z$, have conductor nine. For the conductor-three character, the value at $-2$ is $-3\{B_3(1/3)-B_3(2/3)\}=-2/9$, where $B_3(y)=y^3-3y^2/2+y/2$. For the character sending $2$ to $z$ the six unit residues in order are $1,2,4,8,7,5$. Pair residues $a$ and $9-a$, using $B_3(1-y)=-B_3(y)$. The value is
$$
 -54\{B_3(1/9)+zB_3(2/9)+z^2 B_3(4/9)\}
   =-(4+10z)/3.
$$
Its conjugate product is $(16+40+100)/9=52/3$. Thus $Z_3=-104/27$. The odd higher roots of unity have order $27$: at three the field has cyclotomic image $1+9\mathbf Z_3$, whose cubes are $1+27\mathbf Z_3$; at every other odd prime the image is full and $\ell-1$ does not divide three. By ETS16 the odd part of $A(E,2)^{c=-1}$ therefore has order the odd part of $27|Z_3|=104$, namely $13$. In particular the prime three, which divides both the degree and the conductor, contributes no length. [Value at a negative integer](https://dlmf.nist.gov/25.11.E14) · [Use of the primitive inducing character](https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AutomorphicArithmetic/AutomorphicVarieties/OddResidueBounds/ZeroMemUnrHom.lean#L71-L85)

At $13$ the extension $E_v/\mathbf Q_{13}$ is unramified for every $v\mid13$. Its inertia acts on the first layer of $(\mathbf Q_{13}/\mathbf Z_{13})(-2)$ through the nontrivial square inverse of the mod-$13$ cyclotomic character. Thus the local invariants vanish, and ETS15 gives equality with the whole indicated $K$-group component at $13$. The odd-minus strict group is consequently cyclic of order $13$ at that prime and zero at every other odd prime. Its prime-weighted contribution for this twist is exactly $\log13$. This calculation exhibits a nonzero term in the general abelian CM theorem. [The strict sign and its length](https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AutomorphicArithmetic/AutomorphicVarieties/LengthEqAddEigen.lean#L68-L76) · [Local duality](https://www.jmilne.org/math/Books/ADTnot.pdf)

<!--
% END ETS20
-->
