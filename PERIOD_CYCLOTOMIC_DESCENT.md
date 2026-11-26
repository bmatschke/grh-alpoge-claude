# The cyclotomic part of the selected period lattice

The coefficient field of a nonterminal period row already contains the roots of unity at both of its marked primes. On the sized cover this identifies the entire ramified part of the coefficient extension. In particular, multiplying an integral deep section in the pullback span by $15^e$ suffices to put it in the scalar extension of the original integral lattice. The estimate works place by place and supplies a denominator for the actual vectors used in the [reference determinant](PERIOD_SELECTED_REFERENCE_DETERMINANT.md).

## The finite extension on this row

Let $H=\mathbf Q(\sqrt{-d})$, $M=g_0g_1$, $e=\lfloor3L_x/\log3\rfloor$ and $m=M15^e$. The fixed coefficient field $F=p.T.Q.c.F$ contains $H$ and $\zeta_M$. Indeed the initial level has auxiliary factor one and the coefficient record contains the specified primitive root of order $\operatorname{lcm}(M,1)$. The chosen primes $g_0,g_1$ are distinct and split in $H$. The selected host also splits $3,5$, and $15$ is prime to $M$. The sized cover uses $F'=FR$ with $R$ the ray class field of $m\mathcal O_H$ in the prescribed complex embedding. The construction includes $\zeta_m\in R$. Thus
$$
 F_c=F(\zeta_{15^e})=F H(\zeta_m)\subseteq F'.
$$
These assertions refer to the core and the chosen ray compositum. The row realization used for the period matrix may have a different coefficient field. [The original level and its marked roots](PEL_STAGE_PARAMETERS.md) · [The selected origin and sized cover](PERIOD_SELECTED_MARKED_ORIGIN.md) · [Coefficient pin][pin] · [Ray field and root][ray] · [Construction of the compositum][cover]

**Finite ramification.** The extension $R/H(\zeta_m)$ is unramified at all finite places. At a prime $\mathfrak p$ over $p^t\Vert m$, the completion $H_{\mathfrak p}$ equals $\mathbf Q_p$. The local units act on $R$ through $(\mathbf Z/p^t\mathbf Z)^\times$ by the modulus condition of Artin reciprocity. Their image is the inertia group. Restricted to the contained field $\mathbf Q_p(\zeta_{p^t})$, that image has order $\varphi(p^t)$, since this cyclotomic extension is totally ramified of that degree. Thus restriction on inertia is injective. At a prime outside the modulus the ray field itself is unramified. This proves the assertion, including for the higher powers of $3$ and $5$. Finite unramified extensions of local fields remain unramified in every factor after base change. It follows that $F'/F_c$ is unramified at all finite places. In the tower of differents this gives the exact identities
$$
 \mathfrak D_{F'/F}=\mathfrak D_{F_c/F}\mathcal O_{F'},\qquad
 \frac{\operatorname{rd}(F')}{\operatorname{rd}(F)}
 =\frac{\operatorname{rd}(F_c)}{\operatorname{rd}(F)} .
$$
Here $\operatorname{rd}$ is the absolute root discriminant. The relative different is consequently supported only over $3,5$. [Local units, inertia and the ray class field, Chapters I and V][cft]

## The lattice and its index

Let $L_0$ be the core integral type lattice of rank $\ell>0$, let $V=F\pi L_0$ be its rational pullback, and let $B$ be the deep integral cusp lattice intersected with $F'V$. The selected integral frame tests make $B$ stable under the semilinear action of $\operatorname{Gal}(F'/F)$. Integrality of core vectors is detected after pullback, giving $B\cap V=\pi L_0$. Both facts are used in the [relative-different argument](PERIOD_SELECTED_REFERENCE_DETERMINANT.md#the-finite-descent-loss-on-the-sized-ray-cover). Put $B_c=B\cap F_cV$. Then
$$
 B=\mathcal O_{F'}B_c,\qquad
 \frac{\log\#(B/\mathcal O_{F'}\pi L_0)}{[F':\mathbf Q]}
 =\frac{\log\#(B_c/\mathcal O_{F_c}\pi L_0)}{[F_c:\mathbf Q]} .
$$
Indeed $F'/F_c$ is Galois, since $R/H$ is abelian. Localize at a finite prime of $F_c$ and take the product of completions above it. Finite étale Galois descent identifies the stable module with scalar extension of its invariants, which are the indicated intersection. Alternatively the trace-dual basis is integral because the relative different is the unit ideal. This proves the lattice equality. Each local quotient index then scales by the extension degree in the global norm. This construction of $B_c$ takes place inside the given deep rational space and needs no moduli realization over $F_c$. [Galois stability of the frame tests][tests] · [Trace-dual inclusion][trace]

For $p\in\{3,5\}$ and $\lambda\mid p$ of $F$, let $s_\lambda$ be the largest $0\le s\le e$ for which $\zeta_{p^s}\in F_\lambda$. Define
$$
 h_{p,\lambda}=\begin{cases}
 0 & s_\lambda=e,\\
 e-s_\lambda & 1\le s_\lambda<e,\\
 e-1/(p-1) & s_\lambda=0<e .
 \end{cases}
$$
With the valuation normalized by $v_p(p)=1$, the local different of $F'/F$ has valuation at most $h_{p,\lambda}$ above $\lambda$. For $s_\lambda=e$ the other prime's roots generate only an unramified extension. For $1\le s=s_\lambda<e$, the minimal polynomial of $\zeta_{p^e}$ over $\mathbf Q_p(\zeta_{p^s})$ is $X^{p^{e-s}}-\zeta_{p^s}$ with compatible roots, whose derivative has valuation $e-s$. The cyclotomic integers are generated by the root. For $s=0<e$, differentiating $\Phi_{p^e}(X)=(X^{p^e}-1)/(X^{p^{e-1}}-1)$ at that root gives valuation $e-1/(p-1)$. In both calculations the different after further base change divides the extended different. Locally this follows by factoring the original monic minimal polynomial over the new field and using that the derivative of an integral generator belongs to the field different, also when it generates only a suborder. Adding the prime-to-$p$ roots and the remaining unramified extension contributes no new loss.

Define the normalized **squared** determinant index by $I=2\log\#(B/\mathcal O_{F'}\pi L_0)/(\ell[F':\mathbf Q])$. Trace duality gives $\mathfrak D_{F'/F}B\subseteq\mathcal O_{F'}\pi L_0$. Averaging the local bounds just obtained gives
$$
 0\le I\le 2\sum_{p=3,5}\log p\sum_{\lambda\mid p}
  \frac{[F_\lambda:\mathbf Q_p]}{[F:\mathbf Q]}h_{p,\lambda}.
$$
For $e\ge1$ this is at most $2e\log15-\log3-\tfrac12\log5$, hence less than $6(\log15/\log3)L_x$. For $e=0$ the index vanishes. More generally it vanishes if the requisite local $p^e$-th roots are already present at every place of $F$ over $p=3,5$.

For an actual integral section the corresponding denominator is also explicit. Set $s_p=\min_{\lambda\mid p}s_\lambda$. Then
$$
 3^{e-s_3}5^{e-s_5}B\subseteq\mathcal O_{F'}\pi L_0\subseteq B.
$$
This follows since the integer's valuation dominates that of the different everywhere. In particular $15^e$ clears all the vectors at once, and the two original marked primes require no denominator. This result supplies the finite descent step in period entry 7. The geometric lower bound for the negative-shift lattice remains a separate term in its reference determinant.

[pin]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/ReciprocityTheory/ReductiveGroups/ArithmeticGeometry/BirationalGeometry/ToroidalCompactification/PushInvertible.lean#L40-L45
[ray]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AbelianVarietyTheory/Proofs/DivisorProofs/ExistsGoodCoverOverSizedField.lean#L60-L78
[cover]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AbelianVarietyTheory/Proofs/DivisorProofs/ExistsGoodCoverOverSizedField.lean#L111-L142
[tests]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AbelianVarietyTheory/Proofs/DivisorProofs/LevelCoverCuspFormPullbackInjectiveDescent.lean#L151-L202
[trace]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AbelianVarietyTheory/Proofs/DivisorProofs/GaloisStableLatticeRationalSpanInclusions.lean#L36-L46
[cft]: https://www.jmilne.org/math/CourseNotes/CFT.pdf
