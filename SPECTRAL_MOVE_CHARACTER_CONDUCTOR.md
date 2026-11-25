# The exact last-layer character in the Hermitian lattice move

In the second-type family of the corank-one estimate B8.10d, the characters in the local move integral are precisely the nontrivial elements of one finite group of characters, with equal multiplicities. Their conductors are determined by the two top coefficients. On primitive moves, every character of conductor exponent greater than one contributes exactly zero to the norm-congruence integral. These assertions give a direct proof of the nontriviality and parameter-share inputs used by the [local Fourier bound](SPECTRAL_TWISTED_NORM_CONGRUENCE.md). The primitive calculation gives additional cancellation in the local integral itself.

## The group which supplies all the characters

Use the split or unramified quadratic algebra $E/F$ over a local field, uniformizer $\pi$ of $F$, residue cardinality $q$ and frame scale $\theta=1$ or $\pi$. Take an actual second-type presentation with self-dual row lattice $\Lambda$ and witness frames $g_i,g'_i$ indexed by $0,\ldots,r$. Write $B$ for the span of both full frames, $W=\Lambda\cap B^\perp$, and use the project’s additive character $\psi_0$ with dual ring $O_E$. The full frames are jointly independent over $E$ on the nonsingular locus. In the split case statements about bases and annihilators hold in the two factors. Write
$$
 M=\sum O_E g_i+\sum O_E\theta^{-1}(g'_i-g_i),\qquad
 D=(\Lambda\cap B)/M,\qquad R_\theta=\{(a,a'):a'\in O_E,\ a+a'\in\theta O_E\}.
$$
Indeed the two coefficients of each index in $\theta M$ range precisely over $R_\theta$. The chosen last occupied level is $J=j+1\le r$. In the coordinates of $\theta y$ for $y\in\Lambda\cap B$, all pairs at indices $i\ge J$ lie in $R_\theta$. Each class of $D$ has a representative supported on the two prefixes through $j$, obtained by subtracting the tail in $M$. Put $Y=\operatorname{span}(g_i,g'_i:i\le j)$ and $U=\Lambda\cap Y^\perp$. The witness changes preserve the prefixes and entire flag spans, including the final anisotropic vector modulo the isotropic prefix. Thus these $(Y,W,U)$ are the source lattices and spaces. [Term, frame, difference lattice and levels][model] · [Move and phase][mv]

Let $L$ be the image of $D$ in $E^2/R_\theta$ under the coefficient pair at $j$ of $\theta y$. Its kernel $D_{<J}$ consists of the classes of smaller level. For the parameters $(b,b')$ in the two prefixes with $b+b'\in\theta\Lambda$, the map $(b,b')\mapsto (b+b')/\theta\bmod M$ surjects onto $D$ by the preceding representatives. On this parameter lattice, normalized Haar measure pushes forward to uniform measure on $D$. Exact level $J$ therefore has measure
$$
 \frac{|D|-|D_{<J}|}{|D|}=\frac{\beta_J}{\beta}.
$$
Each nonzero element of $L$ has $|D_{<J}|$ preimages in $D$. The perturbation of the orbital phase at fixed $(b,b')$ is the character on $U$
$$
 \chi_l(u)=\psi_0\!\left(-h(z_l/\theta,u)\right),\qquad
 z_l=a g_{j+1}+a'g'_{j+1},                                      \tag{1}
$$
where $(a,a')$ are the coefficients of $b,b'$ at $j$. They agree with the two original dual-frame readings because the unipotent witnesses change a frame vector only by earlier ones. The move weight formula uses (1) with the original phase as its unit multiplier. [Original character and dual-frame reading][coords] · [Phase transport at a move][transport]

Adding a pair in $R_\theta$ changes $z_l/\theta$ by a member of $M\subset\Lambda$. This leaves (1) unchanged on $U$. Conversely, if (1) is trivial, then $h(z_l/\theta,U)\subset O_E$. Indeed $U$ is an $O_E$-module and the annihilator of $O_E$ for $\psi_0$ is exactly $O_E$. The self-duality of $\Lambda$ gives the dual of $U=\Lambda\cap Y^\perp$ in the ambient space as $\Lambda+Y$. To see this, extend the integral functional on $U$ to $\Lambda$ using saturation over the discrete valuation ring, represent the extension by a vector of $\Lambda$, and subtract. The difference is perpendicular to the span of $U$, hence in $Y$. Thus $z_l/\theta=\lambda+y$ with $\lambda\in\Lambda\cap B$ and $y\in Y$. The coefficient pair at $j+1$ of $\theta\lambda$ is precisely $(a,a')$. All such pairs are in $R_\theta$ by maximality of $J$. This proves injectivity of $l\mapsto\chi_l$ on $L$. All the characters are identically one on $W$, since $z_l\in B$. [Exact-level contradiction in the archive][char]

In particular, in the convention where exponent zero means the trivial character, the conductor on the *whole* move lattice $U$ is
$$
 c_l=\min\{c\ge0:\pi^c(a,a')\in R_\theta\}
   =\max\{0,-v_*(a'),v_F(\theta)-v_*(a+a')\}.                    \tag{2}
$$
Here $v_*$ is the minimum of the two valuations in the split case and $v_*(0)=+\infty$. This follows by applying injectivity to $\pi^cl$ and using $F$-linearity of multiplication by $\pi$. The conductor on $W$ itself is zero for every $l$.

## The primitive part of the norm congruence

Let $Q(u)=h(u,u)$, let $a_0\ge0$ be the norm-congruence exponent, and let $\mathcal P$ mean that $h(u,W)$ generates $O_E$. In the source this is equivalent to existence of $w\in W$ with $h(u,w)=1$. The property depends only on $u\bmod\pi U$, by the field or split ring unit-ideal criterion. For $l\ne0$ one has the exact formula
$$
 q^{a_0}\int_U {\bf1}_{Q(u)\in\pi^{a_0}O_F}{\bf1}_{\mathcal P}\chi_l(u)\,du
 =
 \begin{cases}
 0,& c_l>1,\\
 q^{e}\displaystyle\mathbb E_{\bar u\in U/\pi U}
  {\bf1}_{Q(\bar u)=0\ \mathrm{if}\ e=1}\,{\bf1}_{\mathcal P(\bar u)}
    \chi_l(\bar u), & c_l=1,
 \end{cases}                                                     \tag{3}
$$
where $e=\min(a_0,1)$, and for $e=0$ the norm indicator is identically one.

For the proof split $U=W\oplus C$ as additive $O_F$-lattices. Saturation of $W$ in $U$ supplies this splitting, with no requirement of orthogonality. Within a primitive residue class $u_0+\pi U$, fix any lift of its $C$-coordinate. As the $W$-coordinate varies through its fixed class, for each $a_0\ge1$ the congruence has conditional probability $q^{-(a_0-1)}$ if $Q(u_0)\equiv0\bmod\pi$, and zero otherwise. In fact at depth $n\ge1$ the next digit of $Q(u+\pi^nw)$ changes by $\operatorname{Tr}_{E/F}h(u,w)$ modulo $\pi$, after dividing by $\pi^n$. This residual functional on $W$ is onto because $h(u,W)=O_E$ and the residual trace is surjective, including in characteristic two. Exactly one $q$th of the lifts attains any specified next digit. The fraction is independent of the $C$-lift. The character is trivial on $W$. If $c_l>1$, its average on the remaining $\pi C$-coset vanishes. If $c_l=1$, its value is already fixed. This proves (3). For $a_0=0$ only the residue condition remains, with the same averaging argument.

Consequently the proportion of nonzero top characters with conductor one is exactly
$$
 t_L=\frac{|L[\pi]|-1}{|L|-1},\qquad |L[\pi]|\le q^4 .
$$
The bound follows from $L\subset E^2/R_\theta$ and the $O_F$-rank four of $R_\theta$. The unrestricted mean of all the move phases before deleting any parameters can also be written pointwise in $u$ as $(|L|{\bf1}_{L^\perp}(u)-1)/(|L|-1)$, by finite character orthogonality.

For an explicit consequence let $\rho=k-2r-3$, $b_0=(8/7)q^{1-\rho}$, and $b_{\rm bad}=(8/7)q^{2(1-\rho)}$ at an inert place or $(16/7)q^{1-\rho}$ at a split place. On the identified full-image move family all primitive moves are retained. The source’s affine trace-zero scalar fibre has measure one whenever the norm congruence holds. This remains true above 2: choose an element of $O_E$ of trace one. A solution to $s+\bar s=Q(u)$ in $\pi^{a_0}O_E$ exists exactly when $Q(u)\in\pi^{a_0}O_F$, and all solutions form one coset of the integral trace-zero reference lattice. Thus no integrality of $Q(u)/2$ is required. Combining (3) and the previous [unrestricted and bad-set estimates](SPECTRAL_TWISTED_NORM_CONGRUENCE.md) gives for the normalized retained, phase-weighted row the upper bound
$$
                   t_L(b_0+b_{\rm bad})+b_{\rm bad}.               \tag{4}
$$
For $c_l=1$ use the unrestricted estimate and subtract the primitive complement. For $c_l>1$ the primitive term is zero. The residual retained nonprimitive parameters cost at most $b_{\rm bad}$ across the whole average. Formula (4) supplements the uniform $b_0+b_{\rm bad}$ bound, which also holds directly. This is a bound on the weighted row of the kernel. Its unsigned normalization is a separate estimate. The moved-witness and phase comparisons are used in this application. The following argument verifies retention and identifies the invariant quotient on that model. [Scalar fibre][scalar] · [Primitive move stays in the selected family][retain]

## Why a primitive move preserves the filtered defect quotient

Write $x,x'$ for the two prefix parameters, $A=\Lambda\cap Y$, $D=(\Lambda\cap B)/M$. On the native moved-witness comparison let
$$
 E(v)=v+h(v,u)x-h(v,x)(u+cx),\qquad \Lambda'=E^{-1}\Lambda .
$$
Its new frame vectors are $g_i-h(g_i,u)x$ and $g'_i+h(g'_i,u)x'$. The term and datum match the old one by that comparison. In particular both prefix frames through $j$ stay fixed, since $u\perp Y$. Write $M'$ for their new full difference lattice. Independence identifies $M'\cap Y=M\cap Y$ by the common prefix generators.

Every $v\in A$ is in $\Lambda'$. Indeed decompose $v=v_0+v'_0$ along the prefixes. Both $x+x'$ and $\theta v_0+\theta v'_0$ belong to $\theta\Lambda$. The old second-type pairing test gives $h(x,\theta v'_0)\in\theta O_E$. The first prefix is totally isotropic, hence $h(v,x)\in O_E$. Now $u+cx\in\Lambda$ on a move and $h(v,u)=0$, so $E(v)\in\Lambda$. Thus $A/(M\cap Y)$ injects into the moved quotient.

For a primitive move choose $w\in W$ with $h(u,w)=1$. For any $y\in\Lambda'\cap B$, pairing $E(y)\in\Lambda$ with $w$ gives $-h(y,x)\in O_E$, because $y,x\in B$. Consequently $y+h(y,u)x=E(y)+h(y,x)(u+cx)$ belongs to $\Lambda\cap B$. Represent this vector in the old quotient by $v\in A$, and set $m=y+h(y,u)x-v\in M$. Let $T(m)=m-h(m,u)x$. For every $m\in M$ one has $T(m)\in M'+A$. On $g_i$ this is exactly the new frame vector. On $\theta^{-1}(g'_i-g_i)$ the difference between the corresponding new difference vector and $T(m)$ is $h(g'_i,u)(x+x')/\theta\in A$, since $g'_i,u\in\Lambda$. Linearity gives the assertion on $M$. Now $h(x,u)=h(v,u)=0$ gives $T(m)=y-v$, hence $y\in M'+A$. This proves surjectivity onto the moved quotient. It also gives $A=\Lambda'\cap Y$ since $M'\cap Y=M\cap Y\subset A$.

All quotient classes on both sides may therefore be tested on the *same* representatives in $A$, with the same coefficient pairs and the same filtration. The old second-type pairing on their two flag components gives the new second-type condition by the representative test. Thus a primitive move stays in the original family, preserving $\beta,J,\beta_J$ and the entire top group $L$. Even for a retained nonprimitive move, the above injection and the defining equality of the two finite orders $\beta$ imply surjectivity and the same equality of $L$. This last refinement permits the estimates (3)–(4) to be applied separately on every actual value of the top group in fixed prefix coordinates. The phase multiplier and the existence of the moved witnesses on the specified datum are the remaining geometric comparisons in this argument. [Witness equations][witeq] · [Integral trace representative][trrep] · [Pairing test on representatives][reptest]

[witeq]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AbelianVarietyTheory/Proofs/FlagMeasures/HermitianMovePreservesFrameLatticeLevels.lean#L98-L152
[trrep]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AbelianVarietyTheory/Proofs/FlagMeasures/HermitianDefectClassMemTraceFirstFrameSpan.lean#L125-L185
[reptest]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AbelianVarietyTheory/Proofs/FlagMeasures/PairingSecondTypeTestOnRepresentatives.lean#L113-L139

[model]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AbelianVarietyTheory/Definitions/SemilocalFrames/ComplementReferenceCompactSubgroup.lean#L128-L184
[mv]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AbelianVarietyTheory/Definitions/SemilocalFrames/NoLeak.lean#L17-L55
[coords]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AbelianVarietyTheory/Proofs/FlagMeasures/HermitianDoubleCosetKernelBoundByWeight.lean#L52-L112
[transport]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AbelianVarietyTheory/Proofs/FlagMeasures/HermitianDoubleCosetMoveTermWeightCharacter.lean#L82-L136
[char]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AbelianVarietyTheory/Proofs/FlagMeasures/FrameMoveCharacterNeOne.lean#L79-L139
[scalar]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AbelianVarietyTheory/Proofs/FlagMeasures/EichlerMoveScalarFibreMeasureOne.lean#L57-L105
[retain]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AbelianVarietyTheory/Proofs/FlagMeasures/HermitianDoubleCosetInFamilyMovedOfNotLeak.lean#L89-L140
