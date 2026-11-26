# The different of the common ray marking

On an exported origin the auxiliary ray field shared by the two marked levels can be adjoined **without any coefficient loss at any active prime**. This applies also to invariant sections with new ray-field coefficients. There is an exact formula for the cost of this field at the other primes.

Use the imaginary quadratic field $K$ of the construction, with units $\{1,-1\}$. Let $m_*=g_0g_1p_\delta p'_\delta$ be its fixed modulus and $N$ the squarefree joint support chosen in the [common marked-level construction](SECOND_PASS_COMMON_MARKED_LEVELS.md). Each $p\mid N$ splits in $K$. The support of $N$ avoids $m_*$ and every active coefficient characteristic. Write $H_h$ for the ray class field of $h\mathcal O_K$ in the prescribed embedding.

**Ray-field calculation.** The relative Galois group, with its factors indexed by the primes of $K$, is
$$
 \operatorname{Gal}(H_{m_*N}/H_{m_*})
 \simeq \prod_{p\mid N}\prod_{\mathfrak p\mid p} (\mathcal O_K/\mathfrak p)^\times .
$$
The extension is unramified away from $N$. Above each $p\mid N$ its ramification index is $p-1$, and it is tame. Hence, with $\operatorname{rd}$ denoting the absolute root discriminant,
$$
 \log\frac{\operatorname{rd}(H_{m_*N})}{\operatorname{rd}(H_{m_*})}
   =\sum_{p\mid N}\left(1-\frac1{p-1}\right)\log p.                \tag{1}
$$

Indeed the ray class exact sequence gives a surjection from $(\mathcal O_K/N)^\times$ onto the relative group. To see the kernel, represent a residue by a generator congruent to $1$ at $m_*$ and having that residue at $N$. Its ray class at $m_*N$ is trivial precisely if multiplication by a global unit equal to $1$ at $m_*$ makes that residue $1$. The odd marked factors force this unit to be $1$. The Chinese remainder theorem gives the displayed factors. At a prime $\mathfrak p$ over $N$ the local Artin image of the units is exactly its one residue factor, and $H_{m_*}/K$ is unramified there.

At an old prime $\mathfrak q\mid m_*$, the local units modulo $1+\mathfrak q^{v_{\mathfrak q}(m_*)}$ already inject into the old ray class group. In fact a local residue placed in its single factor can be a global unit residue only if that unit equals $1$ at every other marked factor. At least one other factor is odd, since $g_0$ and $g_1$ are distinct odd rational primes. Again only the identity qualifies. Enlarging the modulus by $N$ therefore leaves the order of this inertia group unchanged. No ramification appears over the old marked primes, including those in the active set. Away from both moduli the absolute extensions are unramified. The tame different exponent at an added prime is $e-1$. Since $K/\mathbf Q$ splits there and $H_{m_*}/K$ is unramified there, summing the local exponents in the discriminant tower gives (1), with a single term per rational prime. This includes the empty support. [Ray class sequence and the Artin map](https://www.jmilne.org/math/CourseNotes/CFT.pdf) · [Local inertia in a ray field](https://www.numdam.org/item/PMB_1989___1_A1_0.pdf)

**Integral sections with extended coefficients.** Let $B$ be a finite coefficient field containing the fixed ray field, and $L=BH_{m_*N}$ in the chosen side. One can include in $B$ the side's already prescribed finite character values. Let $M_\lambda$ be the completed lower integral evaluation lattice of the rational cusp space over $B_\lambda$ at an active coefficient place. Use the rational level descent, marked pullback and original integral-frame comparisons of the construction. In the space of invariant cover sections identified rationally with the scalar extension, the unit ball at $w\mid\lambda$ is exactly
$$
                   M_\lambda\otimes_{\mathcal O_{B_\lambda}}\mathcal O_{L_w}.
                                                                    \tag{2}
$$
Unramified extensions of local fields stay unramified under base change. Thus $L_w/B_\lambda$ has trivial different even if the residue characteristic divides the global relative degree. For a basis $b_i$ of $M_\lambda$ write an invariant reading as $\sum z_i b_i$. The trace test on lifts of the good algebraic frames gives $\operatorname{Tr}_{L_w/B_\lambda}(a z_i)\in\mathcal O_{B_\lambda}$ for every $a\in\mathcal O_{L_w}$. The inverse different is the integer ring here, so all $z_i$ are integral. Conversely integral combinations of the pulled-back basis are integral on every frame by forgetting the marking. This proves (2). It also follows directly on finite coefficient vectors from the [all-prime inverse-different lemma](../geometry/PEL_GOOD_FRAMES_AT_ALL_PRIMES.md#a-sharper-denominator-for-descent-from-a-ramified-coefficient-field). The completed statement follows by continuity, or by approximating the coefficients by algebraic coefficients with integral error. Individual compact invariants and the rational cover identification are essential hypotheses.

For $p\mid N$ the relative local extension after the same base change is tame with $e'\mid p-1$. Its inverse-different bound on coefficients, expressed in units of the valuation of $p$, is $(1-1/e')/e(B_\lambda/\mathbf Q_p)$. This isolates the contribution of the joint ray layer even when the side's other coefficient choices ramify. Formula (1) depends on $N$. The export permits arbitrary finite exclusions, so this calculation by itself gives no scale bound on $N$ or on the heights of the constructed points.
