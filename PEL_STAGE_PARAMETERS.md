# Putting the marked moduli spaces on the original arithmetic column

Fix an assembled arithmetic stage and its given frame. Write $E$ for its CM field, $K=\mathbf Q(\sqrt{-d})$ for the distinguished imaginary quadratic subfield, $K_s\subset L_0\subset L$ for its coefficient fields, and $e:L\hookrightarrow\mathbf C$ for its prescribed embedding. The moduli schemes at the initial level, their coefficient embeddings and the lattices that enter their period maps can all be chosen on this very stage. The construction also gives a framed point at **every** coefficient embedding. The analytic comparison required on the active rows is stronger and is described at the end. [Source statement for the canonical parameters][par] · [Comparison of the marked level](PEL_MARKED_LEVEL.md) · [Construction of the theta line](PEL_THETA_LINE.md)

## The two primes and the coefficient embedding

Use the ordered pair $P_a=f.P.\mathrm{pb}(a)$ supplied by the frame, where $P_a$ lies over $g_a$ for $a=0,1$. The two distinct odd rational primes satisfy $g_a\equiv1\pmod{4}$ and $g_a\equiv1\pmod d$. Quadratic reciprocity gives $(-d/g_a)=1$, hence $(g_a)=P_a\bar P_a$ in $\mathcal O_K$. Extension of ideals to $\mathcal O_E$ gives the level

$$
 M=g_0g_1,\qquad A=1,\qquad
 \mathfrak b=(P_0\mathcal O_E)(P_1\mathcal O_E).
$$

The two conjugate products are coprime and multiply to $(M)$. The argument works for either choice above each $g_a$. The label $a$ persists through contraction back to $\mathcal O_K$, which is precisely how the theta level checks whether a prime of $E$ belongs to the chosen half. Each prime divisor removed from $M$ leaves the other $g_a\ge3$, so the source's good-level inequality holds at every rational prime. [Splitting and the CM type][splitting] · [Level for prescribed primes][level] · [Use in the reference theta level][use]

The stage coefficient ring is $\mathcal O_{K_s}$, embedded by $e$. Its image generates exactly $F_O=e(K_s)\subset\mathbf C$, since every field element is a fraction of integers. Consequently $\mathcal O_{F_O}\simeq\mathcal O_{K_s}$ by $e^{-1}$, and the coefficient inclusion used later is already specified on these parameters:

$$
 j:F_O\longrightarrow L,\qquad e(j(y))=y,\qquad j(F_O)=K_s .
$$

The stage contains the specified roots of orders $g_a(g_a-1)$. Taking $(g_a-1)$-st powers gives the standard roots $\zeta_{g_a}$ under $e$. Bézout then gives the **specified** $\zeta_M$ as a product of integer powers of these roots. The embedded stage ring contains $\mathcal O_E$ in the distinguished embedding $\varphi_0$, hence $F_O$ contains $\varphi_0(E)$. Since $E/\mathbf Q$ is Galois here, it contains the images of every embedding of $E$. This establishes the coefficient-data requirements before selecting period charts. The moduli base itself is $K$ because $A=1$; later coefficient extension to $F_O$ uses the displayed inclusion. [Stage root calculation][root] · [Exact stage field][fo] · [Integral coefficient maps and all conjugates][coef] · [Later comparison for any pinned core](continuation_v77/coefficients.tex#L64-L88)

## Which lattice and Hermitian sign?

The arithmetic row $0\le i<m$ corresponds to $j=i+1$. Its signature is $(p_j,q_j)=(k+j-1,m-j)$ and $r=p_j+q_j=k+m-1$. In particular $p_j>q_j$ throughout and the last row has $q_m=0$. Use the lattice $L_j=\mathfrak a L^0_{W_j}$, where $L^0_{W_j}$ is the specified unimodular Hermitian lattice and $\mathfrak a$ is the stage fractional ideal called `AA`. The alternating form and the lattice embedding are

$$
 B_j(x,y)=\operatorname{Tr}_{E/\mathbf Q}\bigl(\xi_0 h_j(x,y)\bigr),
 \qquad
 \iota_j(x)=\text{the coordinates of }x\text{ in the stage frame of }W_j .
$$

Indeed, $(\xi_0)\mathfrak a\bar{\mathfrak a}=\mathfrak D_{E/\mathbf Q}^{-1}$, the inverse different. Taking the trace dual of the scaled Hermitian lattice therefore gives back $L_j$. The coordinate map carries it onto the stage's rational lattice recovered from its finite completions at the identity. To check the sign, the distinguished root is $\varphi_0(\sqrt{-d})=i\sqrt d$ and $\xi_0=-1/(\mathrm N(\mathfrak c_K)\sqrt{-d})$ has positive imaginary part there. The form $h_j$ is conjugate-linear in the first variable. With this choice of $\xi_0$, the positive complex structure acts as $+i$ on the positive Hermitian directions and $-i$ on the negative ones. Reversing the trace form interchanges the two multiplicities at this embedding, contradicting $p_j>q_j$. Thus the signed trace is fixed and $\iota_j$ is an isometry to precisely the coordinates used by the later finite group action. The unitary level acts identically modulo $M$ on the completed $L^0_{W_j}$ and has trivial archimedean component. Scaling by the fractional ideal gives the same finite congruence test, since the ideal is locally principal. [Signature and rank][ranks] · [Trace-dual ideal][dual] · [Sign and coordinate image][iota] · [Definition of the finite level][kf]

For $j=0$ or $j>m$ the source repeats the datum for $j=1$. This provides the same positive rank at every index and permits the same representing scheme there. The separate coordinate map into the stage frame can be set to zero at these unused indices. The orientation, trace-duality and signature calculations on active rows give the canonical row data of `exists_par_pins_canon`. The moduli construction applied to these actual lattices supplies its scheme for every $j$. [Index extension][indices] · [Canonical assembly][par] · [Coordinate maps on unused rows][fallback]

## A framed point at every embedding

At the inclusion $F_O\subset\mathbf C$, a compatible complex structure on $L_j\otimes\mathbf R$ gives a marked period and hence a point by PUN15, PUN22 and PUN24. Since the resulting moduli scheme over $F_O$ is of finite type and nonempty, it has a closed point with residue field finite over $F_O$. Any embedding $\sigma:F_O\hookrightarrow\mathbf C$ extends to this residue field. The resulting complex point has the prescribed semilinear labels: the eigenvalue attached to $a\in\mathcal O_E$ and label $\tau$ is $\sigma(\tau(a))$. The determinant multiplicities at these labels agree with the original ones because $\sigma(\tau(\sqrt{-d}))=\sigma(\varphi_0(\sqrt{-d}))$ precisely when $\tau$ belongs to the original CM type. Choose an ordered basis of each such Lie eigenspace. On the abelian fiber the ample principal theta line has a one-dimensional space of sections by Riemann–Roch and vanishing of higher cohomology. Any nonzero section supplies the last part of the framed point. [Marked periods and actual moduli points](principal_uniformization_v48/main.tex#L1228-L1269) · [Exact framed point][frpt] · [Abelian-variety Riemann–Roch and index theorem][avrr]

The quantified chart laws apply to $1\le j\le m$ and to those $\sigma$ that preserve the distinguished root. For the other pairs the source only requires an inhabitant of its finite list of domains and maps. Take its single definite domain with identity Hermitian matrix and integral lattice, mapping constantly to the framed point just constructed. Its integral isometry group is finite since its matrix entries are algebraic integers bounded at every complex embedding. One may therefore take the trivial arithmetic subgroup in that domain datum. This supplies the entire unused-index branch. On every active pair use the [unitary component comparison](PEL_ADELIC_COMPONENTS.md) with the marked lattice, group, coefficient labels and $\iota_j$ above. [The source's two branches][fallback] · [The single definite domain][definite] · [Remaining analytic comparisons](principal_uniformization_v48/main.tex#L1271-L1315)

[par]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AbelianVarietyTheory/Proofs/UnitaryExistence/ExistsParPinsCanon.lean#L20-L66
[splitting]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Formalism/LocalToGlobal/ProjectiveLattices/ExistsParameterConditions.lean#L11-L67
[level]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Formalism/LocalToGlobal/ProjectiveLattices/LevelPb.lean#L237-L289
[use]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AbelianVarietyTheory/Proofs/IwasawaDecomposition/ExistsReferenceTupleThetaComparisonNormalisedDat.lean#L152-L171
[root]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AbelianVarietyTheory/Proofs/IwasawaDecomposition/HermitianCodeWordStagesHasRootOfUnity.lean#L15-L55
[fo]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AbelianVarietyTheory/Proofs/IwasawaDecomposition/MemFOAssembledIff.lean#L14-L32
[coef]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Formalism/LocalToGlobal/ProjectiveLattices/ExistsParameterConditions.lean#L69-L169
[ranks]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Formalism/LocalRingCardinality/Params.lean#L6-L46
[dual]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Formalism/LocalToGlobal/ProjectiveLattices/HostInt.lean#L138-L155
[iota]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AbelianVarietyTheory/Proofs/UnitaryExistence/ExistsLatticeEmbeddingLiftDatumHermitianSpace.lean#L22-L66
[kf]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Formalism/LocalToGlobal/ProjectiveLattices/CuspidalL2Subspace.lean#L28-L42
[indices]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Formalism/LocalToGlobal/ProjectiveLattices/ExistsParameterConditions.lean#L188-L210
[fallback]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AbelianVarietyTheory/Proofs/UnitaryExistence/HeckeCharacterFamilyConductor.lean#L31-L68
[frpt]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Formalism/LocalToGlobal/ProjectiveLattices/IsCombAt.lean#L67-L77
[definite]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AbelianVarietyTheory/Proofs/UnitaryExistence/ExistsUniformisationDataNonemptyComponent.lean#L102-L170
[avrr]: https://www.math.ru.nl/personal/bmoonen/BookAV/CohomLB.pdf
