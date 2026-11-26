# Integral periods on the reference row of the linked selector

On the actual joint selector, the arithmetic column periods satisfy the local lower bounds used in period-height entry 1, under the construction and analytic inputs described below. For the descended rational functional itself, there is a finite obstruction at the reference row which can be calculated before any word or period matrix is given. This refines the previous finite exceptional set obtained from the entries of those matrices. It also gives a congruence test at each remaining reference place. [Earlier content ideal](../../../archive/rounds/v89/continuation_v89/integral.tex#L74-L150)

## Arithmetic periods on the same selection

The six arithmetic rows on the constructed points give the following four statements about the terminal pairing. Terminal evaluation followed by lowering is rational and integral at both the reference and the used twisted tuples. For an integral point vector and an admissible row, the class sum has a rational representative with valuation at least $-e_wv_p(\Delta_u)$ at every allowed place. In class coordinates each numerator is integral there by the Weyl-dual row condition, and the point stabilizer order in the denominator divides $\Delta_u$ under the common stabilizer-denominator condition. Localization preserves the estimate. The native proof obtains the reference class sum from the integral row of the constructed column. The joint selection takes these same four rows, the sharp column row at $T_u$ and the arithmetic row at $g_0,g_1$, retaining their closed statements on the third design class. [Class sum on the constructed point][origin] · [Six arithmetic rows][six] · [Closed rows on the actual selector][select]

The two ordinary and enhanced column estimates have a separate source. The witness of linkage supplies a constructed point $q$, a bundle there, its reciprocity comparison, and the equality of the full triple $(D,O,b)$. Projection of that very equality to $(D,O,b.R)$ identifies the selected reciprocity datum with the constructed one. This is the association required in B8.56. Under its weak-correspondence and reciprocity inputs, on good members it gives the compatible local chains and complementary bounds, and the selected kernel conditions for the orbit and jet bounds. This includes level-free places of discriminant, inert and signal type. At the serving tuple the excluded twist primes avoid the residue characteristic. Together with the design stabilizer bound these are the two selection inputs of B4.16. B4.31 combines its column estimates with the terminal, word-prime and two fixed-prime rows. Each closed hypothesis uses the original staged thresholds. Taking their common range before choosing the member, word or place gives the following bound there for every arithmetic word $u$, $n\in N_u$ and admissible row $r$ at $\mu_w$:
$$
 a=\iota^{-1}P_u^{\mu_w}(n,r)=0
 \quad\hbox{or}\quad v_w(a)\ge k_{u,w}:=\lfloor e_w\operatorname{sg}(u,w)\rfloor .
$$
Here the common stabilizer-denominator, level-prime, lattice and filling conditions are those in the constructed-family application of B4.29–31. Outside the size support $k_{u,w}=0$. This conclusion concerns the arithmetic column period. [Projection of the actual witness][link] · [Local kernel and twist comparison][local] · [Pointwise construction][localproof] · [Family bound with its hypotheses][family] · [Size support][support]

## A word-independent obstruction at reference-served places

Fix one such member, its **sharp level** and reference tuple $t_0$. Let $G$ be the rational good-row coordinate space at that tuple, with class-space embedding $J$, and let $q:G\to W$ be its surjective map to the native rational target; in R88L1 coordinates it is $e_{RR}P_{t_0}$. Let $M\subset G$ be the full lattice of good rational reference tests whose embedded forms belong to the native integral carrier. The forms and generator readings identify these as admissible tests. Fullness follows by intersecting the full integral form lattice with the rational good space. Equivalently one can take the inverse image of the integral form lattice under its level basis; its tests suffice. Let $A_0\subset W$ be the module of actual attained reference rows. It is a full lattice, and wherever the serving tuple is $t_0$ its localization equals that of the sharp row lattice. [Good coordinates and the reference lattice](../../../archive/rounds/v88/continuation_v88/rows.tex#L12-L100) · [Localization](../../../archive/rounds/v89/continuation_v89/integral.tex#L65-L87)

Let $s:W\to G$ be the native orthogonal section. It is rational: choose rational basis columns $C$ of $\ker q$ and write $H$ for the rational matrix of the reference Hermitian pairing. The kernel projection has matrix $C(C^*HC)^{-1}C^*H$, since the Gram matrix on the kernel is nonsingular. If the kernel is zero, the projection is zero. Apply its complement to any rational right inverse of $q$ to obtain $s$; the result does not depend on the right inverse. R88L3 identifies the actual rational map $B_u(n)(y)$ with the arithmetic reference period on $J(sy)$ for every rational $n,y$. This identity uses only the reference tuple and its rationality law. [Native section and identification with the recorded pairing](../../../archive/rounds/v88/continuation_v88/rows.tex#L99-L144)

Form the finite module
$$
 D_0=(M+s(A_0))/M .
$$
It depends only on the reference tests, their quotient, and the sharp reference-row lattice. A nonzero common denominator of the coordinates of the finitely many generators of $s(A_0)$ relative to $M$ annihilates $D_0$. Its localized elementary divisors can be calculated from these row matrices alone, including the case where a global integral basis is unavailable. Where $A_0=q(M)$ it is also $(M+\Pi M)/M$, with $\Pi$ the orthogonal projection to $\ker q$, because $s q=1-\Pi$.

If $t_w=t_0$ and $(D_0)_w=0$, each $y\in (A_0)_w$ has $sy\in M_w$. The bound on the arithmetic periods extends by bilinearity and localization to all $n\in (N_u)_w$ and $sy\in M_w$. The R88L3 identity therefore gives
$$
 B_u((N_u)_w)((A_0)_w)\subseteq \mathfrak p_w^{k_{u,w}}\mathcal O_w.
$$
Multiplication by the actual local factor $\mathfrak p_w^{-k_{u,w}}$ of the division ideal proves the original integral-dual assertion at $w$ for every word simultaneously. In particular, outside the size support, every reference-served place outside $\operatorname{Supp}(D_0)$ satisfies entry 1. This proves the same implication at reference-served places inside the size support, with their actual nonzero shifts.

There is an exact test also when $(D_0)_w\ne0$. For fixed unshifted $n\in (N_u)_w$ let $\ell_n(z)=\iota^{-1}P_u^{\mu_0}(n,Jz)$ on $G$. The rational arithmetic coordinate reading gives its values in $K$. By the arithmetic bound $\ell_n(M_w)\subseteq \mathfrak p_w^{k_{u,w}}\mathcal O_w$, so it induces a homomorphism
$$
 (D_0)_w\longrightarrow K/\mathfrak p_w^{k_{u,w}}\mathcal O_w .
$$
The original integral-dual test for this word and place holds exactly when this map vanishes for a generating set of $(N_u)_w$. Indeed $M_w+s((A_0)_w)$ generates the domain before quotienting, the values on $M_w$ already vanish there, and the values on $s((A_0)_w)$ are precisely the native paired values. If $\pi_w^a$ kills $(D_0)_w$, its image is contained in the finite module $\mathfrak p_w^{k_{u,w}-a}\mathcal O_w/\mathfrak p_w^{k_{u,w}}\mathcal O_w$. Thus one may test a finite congruence using reference tests. Neither finiteness nor the arithmetic lower bound forces that congruence to vanish.

The same obstruction bounds the finite loss in the weaker mean-slope argument. For a reference-served $w$ put $N'=(I_uN_u)_w$. Bilinearity and the arithmetic bound give $\ell_{n'}(M_w)\subseteq\mathcal O_w$ for every $n'\in N'$. The map
$$
 N'\longrightarrow\operatorname{Hom}_{\mathcal O_w}((D_0)_w,K/\mathcal O_w),
 \qquad n'\longmapsto[z\mapsto\ell_{n'}(z)\bmod\mathcal O_w]
$$
has as kernel exactly the largest submodule $N'_{\rm int}$ on which the original pairing is integral against the actual sharp row. This follows by testing $s((A_0)_w)$ as above. Each summand $\mathcal O_w/\mathfrak p_w^a$ of $(D_0)_w$ has dual $\mathfrak p_w^{-a}\mathcal O_w/\mathcal O_w$ of length $a$. Hence the local source loss satisfies
$$
 \operatorname{length}_{\mathcal O_w}(N'/N'_{\rm int})
 \le \operatorname{length}_{\mathcal O_w}((D_0)_w).
$$
The bound is independent of the word rank. With $m_+$ positive-rank words, total rank $R>0$ and $n_K=[K:\mathbb Q]$, the reference-place contribution to the averaged finite loss is at most $2m_+\log\#D_0/(n_KR)$. Comparing this number with a prescribed family allowance still requires a bound for the order of $D_0$. [Index normalization and mean-slope argument](PERIOD_LATTICE_LOSS.md#the-two-losses-and-their-exact-normalization)

## One common change of the target for the mean-slope consequence

At each reference-served $w$, keep the sublattice
$$
 R'_w=\{y\in R_w:s y\in M_w\}.
$$
Under $R_w=(A_0)_w$, the map $y\mapsto sy\bmod M_w$ identifies $R_w/R'_w$ with $(D_0)_w$. Thus the local index is word independent, even when one only knows that $A_0$ is a full lattice. It is finite and vanishes at all but finitely many reference-served places. The orthogonal representative of each element of $R'_w$ is integral, so the arithmetic valuation estimate there, followed by the original column shift, puts every word map in $(R'_w)^\vee$.

If the original bounds hold on the other serving tuples, use $R'_w=R_w$ there and glue by intersection, keeping the archimedean metrics. More generally, prescribed finite-index sublattices solving the other local tests can be included with their own indices. In either case every shifted word map is integral into the same enlarged dual target. The normalized mean of the dual increases by exactly
$$
 \mu((R')^\vee)-\mu(R^\vee)
 =\frac{2}{\mathrm{rk}\,R}\sum_w\frac{\log Nw}{[K:\mathbb Q]}\,
                         \operatorname{length}(R_w/R'_w).
$$
This is the determinant/index formula with squared norms. Containment gives $\mu_{\max}(R')\le\mu_{\max}(R)$ by saturation, so the lower slope bound on the dual target used in the frame argument is preserved. The rational maps, their infinite norms, their complex images and the spanning inequality also agree. One may therefore run the [mean-slope deduction](PERIOD_LATTICE_LOSS.md) with this target and then pay the displayed mean difference once to return to $R^\vee$. For the literal integral assertion at the original target the local congruence tests above still apply. For its mean-slope use this gives a single row-index budget divided by the target rank, independently of the number of words.

## What the retained multiplicity comparison proves for entries 1 and 4

Fix a member on the common eventual range of the original selector. Use its sharp level, coefficient embedding, arithmetic word-to-column identification and serving tuple $t_w$. Assume the constructed-family arithmetic lower bound of B4.31, the integral column and row identifications of B4.38–45, and the well-formed row, rational coordinate and good-subspace identifications in R88L1–3. For entry 4 use the spectral admissibility $\mathrm{FinX}$ of R89C1 and surjectivity of the reference good row onto the native target. These hypotheses, the join and the multiplicity identity must refer to the same realization.

Here the selector retains the actual identity $\mathrm{MIstar2}$ in the combined row after its common cutoff. It retains the divisor comparison $h_{\rm DivG}$ and selects the join $\mathrm{selJ}$ on the same bundle. The construction obtains the latter from the witness of linkage and its comparison by transport along the equality of complete realization packages. The chosen join projects to the row, column, metric and pairing data of $\mathrm{JoinAt}$. Two normalizations can be read separately: the weak characterization in the linked witness fixes the reference lift phase at one, and $\mathrm{MIUnit2}$ fixes the relative scalar $\zeta_{u,t_0}$ at one for every word. [Joint selector][c14sel] · [Multiplicity on the common range][c14mi] · [Join on the same bundle][c14join] · [Conversion to JoinAt][c14joinat] · [Lift phase on the selected face](../../../archive/rounds/v74/continuation_v74/bundle.tex#L3-L31) · [Relative scalar and unit][c14unit]

**Entry 1.** Let $P_t(x,F)$ be the rational arithmetic pairing on the face, and let $A_tF$ denote the image of its integral row in sharp-row coordinates. The multiplicity comparison in the original sign convention gives
$$
 B^{\rm coord}_u(x,A_tF)=z_{u,t}P_t(x,F).
$$
If a pair of rational arguments has nonzero $P_t$, the ratio of its two rational values is the field representative of $\zeta_{u,t}$ and the identity holds on all arguments. If $P_t$ vanishes identically, both forms vanish and one can take $z_{u,t}=1$. The serving unit condition gives $v_w(z_{u,t_w})=0$. The scalar multiplying $B^{\rm coord}$ in the reverse convention of B4.45 is $z_{u,t_w}^{-1}$. The retained divisor row identifies $B^{\rm coord}$ with the native $D.\mathrm{div}.Bk$ under the recorded word and sharp-row isomorphisms. This is a bilinear equality before any integrality conclusion. [Rational scalar on all inputs][c14z] · [Divisor comparison][c14div] · [Native column equality][c14bk]

For $n\in (N_u)_w$, B4.31 and the integral row comparison put the values on $A_{t_w}M_{t_w}$ in $\mathfrak p_w^{k_{u,w}}\mathcal O_w$, where $k_{u,w}=\lfloor e_w\operatorname{sg}(u,w)\rfloor$. The unit leaves this valuation unchanged. The localization of the sharp row is the localization of that image. The native shifted word lattice is locally $\mathfrak p_w^{-k_{u,w}}(N_u)_w$. Thus the pairing on the two shifted and sharp lattices is integral at every finite place. Intersecting the valuation rings proves $B_u(N'_u)\subseteq RR^\vee$, including the places outside the size support where the shift is zero. [All-place arithmetic bound][c14bound] · [Original integral-dual transfer][c14dual]

**Entry 4.** Write $Z_j$ for the good theta image of the $j$-th reference row-basis vector. At $t_0$ the factor $\zeta_{u,t_0}=1$, so the retained identity gives exactly
$$
 \iota(P_{t_0}(e_i,e_j))=a_u
  \langle s_{EE}(A Z_j), P_{m(u)}(N_u e_i)\rangle,\qquad a_u\ne0 .
$$
The same $A$ preserves the good row space and its norm for all words. Its restriction is onto by finite dimensionality. Each $N_u$ is unitary in that word’s column metric. In the notation of R89C2, let $J$ be the semilinear row identification, $K_u$ the column coordinate map, and $\eta$ the identity or conjugation prescribed by the join. The maps $V=J^{-1}AJ$ and $U_u=(\eta K_u)^{-1}N_u(\eta K_u)$ are complex-linear unitaries, since the corresponding norm scales cancel. The same $V$ serves every word. The joined row basis contributes its scalar $\lambda\ne0$, and the word’s inner-product comparison contributes $\kappa_u\ne0$. In the native coordinates the scalar is $\eta(a_u\lambda)\kappa_u$. Both sides are bilinear in the two rational basis coordinates after the specified conjugations, so equality on basis pairs extends to complex arguments. Taking the distinguished lift of the row target and composing the column map with its final wordwise isometry gives the asserted identity with the native Bessel pairing. R88L3 supplies its rational clause. [Base-tuple proof and scalar conventions](../../../archive/rounds/v89/continuation_v89/comparison.tex#L34-L98) · [Direct native implication][c14four]

This proves both implications on a member with those retained rows and hypotheses. An independent construction of the multiplicity row uses a nonzero **full reference row** with a preimage under descent, the matched two-step seesaw and the comparison of measures. The diagonal argument for that nonvanishing uses the unrestricted full-row estimate and the ramified dimension inequality; the [original prime window verifies its dimension premise](PERIOD_FULL_REFERENCE_PAIRING.md). A single nonzero pairing between a descended row and a signed sum on one marking orbit also suffices. At the reference tuple the same mixed identity implies the kernel vanishing used by [entry 6](PERIOD_REFERENCE_MAP_HEIGHT.md). The reference projection and congruence test in [the reference integrality proof](#a-word-independent-obstruction-at-reference-served-places) give a separate route at reference-served places. [Analytic anchor and transport][c14anchor] · [Scope of the diagonal estimate](PERIOD_BASE_COMPARISON.md)

[c14sel]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AbelianVarietyTheory/Proofs/GlobalInterpolation/NonemptyHypsOfAllRows.lean#L33-L80
[c14mi]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AbelianVarietyTheory/Proofs/DivisorProofs/PartitionSelectionEvaluation.lean#L50-L69
[c14join]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AbelianVarietyTheory/Proofs/GlobalInterpolation/EntriesCombinedReal.lean#L73-L95
[c14joinat]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Formalism/LocalToGlobal/SiegelLatticeTheory/FlagStabilizerTensors/JoinSI.lean#L417-L429
[c14unit]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Formalism/LocalToGlobal/IndefiniteReal/IsometricPeriodsOfUnitHypotheses.lean#L21-L28
[c14z]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Formalism/LocalToGlobal/IndefiniteReal/IsometricPeriodsOfUnitHypotheses.lean#L78-L118
[c14div]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AbelianVarietyTheory/Proofs/GlobalInterpolation/BkLawEntries.lean#L81-L93
[c14bk]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AbelianVarietyTheory/Proofs/IwasawaDecomposition/RationalPairingEqColumnPairing.lean#L60-L96
[c14four]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Formalism/LocalToGlobal/SiegelLatticeTheory/FlagStabilizerTensors/AdmissibleOfTransported.lean#L145-L185
[c14bound]: https://github.com/rh-lean-roadmap/rh-lean-roadmap/blob/02a95b4c62db610642af5f278ee5d0d6df87b348/docs/src/book/main.tex#L7539-L7562
[c14dual]: https://github.com/rh-lean-roadmap/rh-lean-roadmap/blob/02a95b4c62db610642af5f278ee5d0d6df87b348/docs/src/book/main.tex#L7926-L7964
[c14anchor]: https://github.com/rh-lean-roadmap/rh-lean-roadmap/blob/02a95b4c62db610642af5f278ee5d0d6df87b348/docs/src/book/main.tex#L44412-L44448

[origin]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AbelianVarietyTheory/Proofs/GlobalInterpolation/ReferencePeriodIntegralBundlePointsOfOverColumns.lean#L9-L16
[six]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AbelianVarietyTheory/Proofs/GlobalInterpolation/PeriodEntriesAtBuilt.lean#L17-L32
[select]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AbelianVarietyTheory/Proofs/GlobalInterpolation/NonemptyHypsOfAllRows.lean#L78-L88
[link]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AbelianVarietyTheory/Proofs/GlobalInterpolation/LinkedBundlesOfCasselmanWallach.lean#L40-L47
[local]: https://github.com/rh-lean-roadmap/rh-lean-roadmap/blob/02a95b4c62db610642af5f278ee5d0d6df87b348/docs/src/book/main.tex#L24357-L24384
[localproof]: https://github.com/rh-lean-roadmap/rh-lean-roadmap/blob/02a95b4c62db610642af5f278ee5d0d6df87b348/docs/src/book/main.tex#L59235-L59260
[family]: https://github.com/rh-lean-roadmap/rh-lean-roadmap/blob/02a95b4c62db610642af5f278ee5d0d6df87b348/docs/src/book/main.tex#L7539-L7562
[support]: https://github.com/rh-lean-roadmap/rh-lean-roadmap/blob/02a95b4c62db610642af5f278ee5d0d6df87b348/docs/src/book/main.tex#L6464-L6475
