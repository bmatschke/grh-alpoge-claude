# The number of normal labels at a represented nonsingular Gram point

Fix a corank-one partner class $c$ and a represented block point $\gamma$ in it in the two-word calculation of B8.10. The result applies to both the nongeneric class count and the same-word generic scalar class count wherever the two normal coordinates separate labels. Put $f=[F:\mathbb Q]$, where $E/F$ is the host CM extension. Write $\mathfrak d$ for the absolute different of the totally real field $F$, $s=r(r+1)$ and $G=D_{r+1}\overline{D_{r+1}}-TT'D_r\overline{D_r}\ne0$. Define
$$
 A=(G)\mathfrak d^{-2s},\qquad
 d_{\rm sp}(A)=\prod_{\mathfrak p\ {\rm split\ in}\ E/F}
                     (1+v_{\mathfrak p}(A)),\qquad P=N_{F/\mathbb Q}A.
$$
Here $A$ is an integral ideal. In the selected host, $|\mathrm{disc}(E)|=|\mathrm{disc}(F)|^2$, so $P=\operatorname{rd}(E)^{-2sf}|N_{F/\mathbb Q}G|$. Thus $P$ is the normalized Gram norm $\widehat N_G$ in B8.10. For $w_E=|\mu(E)|$, the number of distinct labels has the bounds
$$
 M(c,\gamma)\ \le\ w_E^2\,d_{\rm sp}((T)A)\,d_{\rm sp}((T')A)
 \ \le\ w_E^2 4^f d_{\rm sp}(A)^2
 \ \le\ w_E^2 12^f P .                                           \tag{1}
$$
For any fixed $\eta>0$ the last expression can be replaced as an upper bound for $M$ by $C_\eta^f P^\eta$, with $C_\eta$ independent of the field, the rank and the word primes. The unchanged parameter $G$ still depends on the words. Formula (1) removes the separate factors in $T,T'$ and the root discriminant from the *label multiplicity*. Other parts of the global estimate have their own measure and discriminant factors. [Roadmap count and partner classes][count] · [Use in the squared norm][assembly]

## Divisibility of the actual normal vector

Let $\Lambda$ be the integral Hermitian lattice of a term, with the two lifted flags in that lattice, and put $I=\mathfrak d\mathcal O_E$. For either flag write $f_0,\ldots,f_r=z$ for its frame and $m_a=r-a$. The lattice equality for the lifted flag gives $I^{-m_a} f_a\subset\Lambda$ for $a<r$. The last vector is integral by the lift condition. Since ideals are invertible this says $f_a\in I^{m_a}\Lambda$ for every $a$. These are properties of the actual representatives used in the formula for the normal, by the two lift and row conditions in the source. The same holds for the primed flag. The ideal $I$ is fixed by conjugation, so every mixed pairing $Z_{ab}$ belongs to $I^{m_a+m_b}$. Expanding either of the leading minors of orders $r,r+1$ gives membership in $I^s$, since $2\sum_{a=0}^{r-1}m_a=2\sum_{a=0}^{r}m_a=s$. Hence $G\in I^{2s}\cap F=\mathfrak d^{2s}$ and $A$ is integral. [Integral frame and weighted entries][weights] · [The two lifted frames in the term lattice][frames]

The normal in the first lattice is
$$
 y=T\sum_{b=0}^{r}\operatorname{adj}(Z)_{b,r} f'_b+D_{r+1}z .
$$
Every summand of the determinant for $\operatorname{adj}(Z)_{b,r}$ uses the rows other than $r$ and columns other than $b$. The sum of their weights is $s-m_b$. Multiplication by $f'_b$ restores $I^{m_b}$, including $b=r$. The last term contains $D_{r+1}\in I^s$. Therefore $y\in I^s\Lambda$. Interchanging the flags and transporting by the term's lattice isometry gives $y'\in I^s\Lambda'$. This is stronger than simply knowing $TG$ is the norm of an integral vector. [Cofactor and normal formula][vector] · [Second normal and common lattices][frames]

## Pairwise integrality and the count

Choose one occurring reference term $t_0$ for $(c,\gamma)$, ignoring terms of zero amplitude. In the class, both lattices are fixed. The source's line comparison gives $y_t=x_t y_0+e_t$ with $e_t$ in the fixed totally isotropic flag space perpendicular to $y_0$. Also $x_t\bar x_t=1$ and $h(y_0,y_0)=TG$. The primed statements use $T'$. The normal-separation property says that equality of both coordinates forces equality of the normal label in this class and point. Choosing one term for each occurring label thus injects the labels into the pairs of coordinates. [Line comparison][line] · [Paired coordinates and label separation][sep] · [Norms of both vectors][norms]

The form is taken linear in its first variable. For any two of the chosen terms, all mixed and isotropic terms drop out, giving
$$
             TG\,x_t/x_u=h(y_t,y_u)\in I^{2s}.
$$
At a prime $\mathfrak p$ of $F$ split as $(w,\bar w)$ choose one of its two places. Both orders of the two terms are allowed in this formula, whence
$$
 \max_t v_w(x_t)-\min_t v_w(x_t)
                    \le v_{\mathfrak p}((T)A).                      \tag{2}
$$
The conjugate valuation is the negative of the chosen one. At a nonsplit prime every norm-one element has valuation zero. Thus at most $d_{\rm sp}((T)A)$ different valuation vectors occur. Two elements with the same vector differ by a global unit of absolute value one at every archimedean embedding, hence by a root of unity. Indeed all powers are algebraic integers of bounded degree with all conjugates on the unit circle. Their monic polynomials have bounded integer coefficients, so two powers coincide. Applying this argument separately to both coordinates gives the first inequality in (1). The word primes split completely and each has at most $f$ real-field prime factors of exponent one. Each such factor increases the divisor count by at most two, including when it already divides $A$. This proves the second inequality.

For the last inequality use $(a+1)^2\le Q^a$ for $Q\ge4$, $(a+1)^2\le(4/3)3^a$ for $Q=3$, and $(a+1)^2\le(9/4)2^a$ for $Q=2$. The exceptional constants are the maxima of $(a+1)^2/Q^a$ on the nonnegative integers. There are at most $f$ places above each rational prime. Multiplying gives $d_{\rm sp}(A)^2\le3^fP$. For arbitrary fixed $\eta>0$ use $(a+1)^2\le4^a\le Q^{\eta a}$ for $Q\ge 4^{1/\eta}$. At the finitely many remaining rational primes use $\sup_{a\ge0}(a+1)^22^{-\eta a}<\infty$ at at most $f$ places per prime. Finally $\varphi(w_E)\le 2f$ and $\varphi(n)^2\ge n/2$ by the prime-power formula. Thus $w_E\le8f^2$ and the torsion and splitting factors are absorbed in $C_\eta^f$.

## Substitution into the spectral energy estimate

For a Hilbert-space subtotal $V_{c,\gamma,\nu}$ and any positive point weights $w(\gamma)$, weighted Cauchy–Schwarz gives
$$
 \left\|\sum_{\gamma,\nu}V_{c,\gamma,\nu}\right\|^2
 \le \left(\sum_{\gamma:\,M>0}w(\gamma)^{-1}\right)
       \sum_{\gamma,\nu}w(\gamma) M(c,\gamma)\|V_{c,\gamma,\nu}\|^2 .
$$
First apply the inequality to finite partial sums with the weight $w(\gamma)M(c,\gamma)$ for each label. Absolute convergence or the indicated finite energy bound permits passage to the limit. Thus the original reciprocal point sum works unchanged, and the factor on the energy side from counting labels can be taken to be $C_\eta^f\widehat N_G^\eta$. In particular if $A$ is the unit ideal it costs at most $w_E^24^f$, however large the word primes. This proves the needed arithmetic multiplicity bound in this step on the tied rows. Bounding the actual real orbital amplitudes and proving a signed lower bound for the remaining trace require further input. [Finite Gram coefficients](SPECTRAL_FINITE_CHARACTER_VALUES.md) · [Nonsingular local densities](SPECTRAL_SCALAR_DENSITIES.md)

[count]: https://github.com/rh-lean-roadmap/rh-lean-roadmap/blob/02a95b4c62db610642af5f278ee5d0d6df87b348/docs/src/book/main.tex#L17690-L17716
[assembly]: https://github.com/rh-lean-roadmap/rh-lean-roadmap/blob/02a95b4c62db610642af5f278ee5d0d6df87b348/docs/src/book/main.tex#L45740-L45755
[weights]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Formalism/LocalToGlobal/SiegelLatticeTheory/CokernelGLCounts/RankPointCounts/StepNormOneOfLeaves.lean#L114-L149
[frames]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Formalism/LocalToGlobal/SiegelLatticeTheory/CokernelGLCounts/RankPointCounts/FramesMem.lean#L21-L69
[vector]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Formalism/LocalToGlobal/SiegelLatticeTheory/CokernelGLCounts/RankPointCounts/PairingOmegaPrimeZ.lean#L54-L122
[line]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Formalism/LocalToGlobal/SiegelLatticeTheory/CokernelGLCounts/RankPointCounts/NmlLineHolds.lean#L22-L55
[sep]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Formalism/LocalToGlobal/SiegelLatticeTheory/CokernelGLCounts/RankPointCounts/RelCOfOcc.lean#L84-L124
[norms]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Formalism/LocalToGlobal/SiegelLatticeTheory/CokernelGLCounts/RankPointCounts/FramesMem.lean#L94-L122
