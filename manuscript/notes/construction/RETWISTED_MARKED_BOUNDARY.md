# A bound for each marked short theta class at every integral frame

Fix a marked PEL row over its prescribed coefficient field $K$, with the original graph theta line, frame laws and canonical harmonic connection. Assume its uniformizations at the designated embeddings, auxiliary level $l.A=1$, target rank $r\ge1$ and squarefree marking level $M$. At the tested residue characteristic $p$ assume $M/p^{\operatorname{ord}_p M}\ge3$. This holds everywhere for the ordinary marking $g_0g_1$ and its squarefree auxiliary covers retaining those two primes. Take even theta degree $n$, the source's nonnegative dominant row weight $a$, a permitted self-dual lattice $\Lambda$ standard at $M$, an admissible odd multiple $N$ of $M$, and its integral highest-weight harmonic polynomial $P$ of degree $d$. Use the original requirement `LastPos` in indefinite signature, namely $a(\tau,m_\tau-1)>0$ for each $\tau$ in the CM type with $m_\tau>0$. Definite components have no isotropic boundary. The assertion below also holds whenever the characteristic sections in its proof are already known to be cuspidal at all designated embeddings. [Weight conditions][weight] · [Point-mass cusp construction on the marked model][cusplean]

For **every** class $u\in Q^n$, with $Q=\mathrm{LevQ}(\mathrm{Dw},l)$, there is a section $S_u$ over $K$. Its value on a framed point is the individual normalized short class

$$
 X_u=(m_\Lambda N^d)^{-1}\sum_{z\in Z_\Lambda}J_{P,N}(u,z).
$$

Here $m_\Lambda=[\Lambda\cap O_E^n:NO_E^n]^r$ and $J$ uses the two original symmetric theta-group translations in their prescribed order. For an abelian CM host $E/\mathbb Q$, its value on **every integral frame** with finite residue field over $p$ satisfies

$$
 v(\alpha_p^d X_u)\ \ge\ -\lfloor d/2\rfloor\,
 \frac{\operatorname{ord}_p|\Delta_E|}{[E:\mathbb Q]}\,v(p),
 \qquad \alpha_p=\begin{cases}p&p\mid M,\\1&p\nmid M.\end{cases}
 \tag{1}
$$

The required good-reduction input is the different estimate on the original graph-line chart. Formula (1) includes every semistable degeneration tested by the marked-row cusp criterion. It is independent of $N$. The local splitting extension used to read $X_u$ may depend on the test and $N$, exactly as in ICL.13. [Good-frame estimate][good] · [Definition of the grouped value][icl] · [Good-to-all test criterion][roadbd]

## Recovering one class over the prescribed field

Take the marked row itself as the base of the identity cover. Choose the coefficient function $q\mapsto\mathbf1_{q=u}$ and take the lattice scalar parameter to be one. Its values belong to $K$. Write $c_0=|Q|^n$. The resulting section at a framed point has value $X_u/c_0$, since only that class occurs in the outer sum. Equivalently one may use the $\beta_H(\Lambda)$-normalized formula and multiply by $\beta_H(\Lambda)c_0$. In the scalar-one convention set $S_u$ equal to $c_0$ times the section. There is no further cardinality denominator in $S_u$. This use of point masses takes place on the identity cover of whichever row bears the marking, including an upper row with its own larger absolute level. [Project construction for individual residues][own] · [Source definition][short]

For completeness, over a faithfully flat splitting of the framed test algebra choose the marked division points on the prescribed half of the torsion and enumerate the isotropic group. Over a common splitting, the difference between two choices of a division point is $N$-torsion on that half. Local standardness of $\Lambda$ at $M$ puts the tuple of differences in $Z_\Lambda$. Translation by this tuple permutes the enumeration. The columnwise theta-group changes yield scalars whose squared product is one by isotropy and whose product has order dividing the odd integer $N^2$. Their product therefore equals one. This compares the inner sums for **each** $u$. Harmonicity makes the contraction independent of the logarithmic frame. Thus the two images in the tensor-square splitting algebra agree, and the faithfully flat equalizer produces the value over the original algebra. Base change and triangular covariance produce the indicated section over $K$. This is the project’s identity-cover descent and explains why a fixed characteristic can be used separately. [Original comparison and naturality][localcmp] · [Existing descent proof][ownproof]

At every designated embedding, its analytic reading is a finite sum of characteristic theta derivatives. On an indefinite component the zero-frequency terms at a rational isotropic line have a deficient row block in an adapted basis. Each highest-weight term has a full-height minor in a relevant block by the last-row positivity. Hence the zero-frequency terms vanish. Changing the marking acts by a finite Fourier transform of characteristics, so the calculation applies at every rational boundary. On the definite components there is no boundary condition to check. This argument works on the individual residue indicator. It proves that $S_u$ is a cusp section before any outer sum is taken. [Original finite-characteristic proof][owncusp] · [Roadmap B8.43o, where this is proved separately for point masses][roadpoint]

The identification of $S_u$ with the source's $X_u$ at a bad test is an identity on the **generic fibre**. Its abelian variety in characteristic zero has finite étale $N^2$-torsion. A finite extension of its fraction field makes all geometric $N^2$-torsion rational. Every marked $M$-torsion point has an $N$-division point killed by $N^2$, since $M\mid N$. Decomposing the finite $O_E$-module into primary factors retains the summands supported at the half-ideal, since the marked point is killed by this ideal. This gives the required half-ideal power condition. Enumerating $Z_\Lambda$ in that same rational torsion gives the distinct geometric tuples, and the odd normalized lifts produce the ordered sections. The equalizer identity above therefore computes $S_u$ by the literal $X_u$ even when the special fibre degenerates. A further field extension scales both sides of (1) by its ramification index. Only the split torsion and the generic connection are used for this identification. [The source constructs all these witnesses over the rationalized generic field][rat] · [Comparison on geometric points and return to the original evaluation][val]

## Preserving the rational different exponent through the boundary

Let $h=[E:\mathbb Q]$, $s=\lfloor d/2\rfloor$, and $D_p=\operatorname{ord}_p|\Delta_E|$. The cusp section

$$
                  T_{u,p}=p^{sD_p}(\alpha_p^d S_u)^h
$$

is defined over $K$. Its row weight and theta degree are $ha$ and $hn$, since sections multiply in the source's framed model. They meet the same nonnegativity and dominance conditions. Cuspidality of the power follows either from vanishing at each cusp or from the product law for the original sections. At every good integral frame the good-frame estimate gives $v(T_{u,p})\ge0$. Apply B8.43n at each coefficient place over $p$. Its hypotheses are exactly a cuspidal section at every designated embedding on this marked model, the prime-to-$p$ level bound and good-frame integrality at that place. It follows that $v(T_{u,p})\ge0$ at every original integral frame there. Expanding this inequality and dividing by $h>0$ proves (1) without rounding its rational coefficient. The zero section satisfies all inequalities with valuation $+\infty$. The proof needs neither roots of $p$ in $K$ nor a choice of integral trace germ on a semiabelian boundary. [Products of cusp rules][power] · [Proof of the marked boundary criterion][arc]

In particular $X_u$ is integral at all unramified nonlevel places, including bad-reduction tests there. Recombining the classes in (ICL.13) incurs exactly the displayed outer division by $c_0$ for the integral-weight inequality of that formula. The estimate for the individual $X_u$ has no such division. On a further descent from the marked upper row, the prescribed weight-zero factor $c_\delta$ multiplies the sum. A root-of-unity normalization has valuation zero. [Cover scalar in the original evaluation][val]

Consequently these rows satisfy the individual boundary estimate (1). For an abstract cover one must still identify the actual marked PEL model, its graph line, connection, all designated uniformizations, and any lower-level scalar. The construction of a common arithmetic point and compatible two-pass data for every exclusion set and prescribed final host remains open.

[weight]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Formalism/LocalToGlobal/ProjectiveLattices/ThProps.lean#L18-L28
[cusplean]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AbelianVarietyTheory/Proofs/InertiaEigenvalues/ExistsCuspCoefficient.lean#L15-L34
[good]: https://github.com/bmatschke/grh-alpoge-claude/blob/7d979b4d629b48e05bd3260b5bdec1cb52b7b468/RETWISTED_JET_DIFFERENT.md#L5-L50
[icl]: https://github.com/bmatschke/grh-alpoge-claude/blob/7d979b4d629b48e05bd3260b5bdec1cb52b7b468/integral_cusp_lattices_v46/main.tex#L832-L886
[roadbd]: https://github.com/rh-lean-roadmap/rh-lean-roadmap/blob/94e6a98b4e74932a0298d6bd22d44cf60c62764b/docs/src/book/main.tex#L23735-L23741
[own]: https://github.com/bmatschke/grh-alpoge-claude/blob/7d979b4d629b48e05bd3260b5bdec1cb52b7b468/FIRST_PASS_DISTINGUISHED_COVER.md#L3-L18
[short]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Formalism/LocalToGlobal/ProjectiveLattices/ThShort.lean#L239-L265
[localcmp]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AbelianVarietyTheory/Proofs/CuspFormEvaluations/IsotropicSumIndependentOfChoicesLocal.lean#L88-L145
[ownproof]: https://github.com/bmatschke/grh-alpoge-claude/blob/7d979b4d629b48e05bd3260b5bdec1cb52b7b468/continuation_v76/descent.tex#L4-L72
[owncusp]: https://github.com/bmatschke/grh-alpoge-claude/blob/7d979b4d629b48e05bd3260b5bdec1cb52b7b468/continuation_v73/compare.tex#L256-L311
[roadpoint]: https://github.com/rh-lean-roadmap/rh-lean-roadmap/blob/94e6a98b4e74932a0298d6bd22d44cf60c62764b/docs/src/book/main.tex#L57935-L57939
[rat]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AbelianVarietyTheory/Proofs/RingsOfIntegers/ExistsThetaValData.lean#L90-L132
[val]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AbelianVarietyTheory/Proofs/RingsOfIntegers/EvROfFrMapFromTest.lean#L40-L92
[power]: https://github.com/bmatschke/grh-alpoge-claude/blob/7d979b4d629b48e05bd3260b5bdec1cb52b7b468/integral_cusp_lattices_v46/main.tex#L443-L469
[arc]: https://github.com/rh-lean-roadmap/rh-lean-roadmap/blob/94e6a98b4e74932a0298d6bd22d44cf60c62764b/docs/src/book/main.tex#L57858-L57887
