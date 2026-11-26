# The absolute Siegel lemma in the arithmetic flag argument

One input to the good root tower in period entry 7 asks for a line of large degree in each Hermitian lattice, allowing the field of definition of the line to vary. It follows directly from Gaudron and Rémond's absolute Siegel lemma. The field extension and the metrics in their result have exactly the normalizations needed here. [Roadmap B8.26u, Claim 1](https://github.com/rh-lean-roadmap/rh-lean-roadmap/blob/dc5594a62bb2b94139788df817db693cd939a046/docs/src/book/main.tex#L49785-L49797) · [Original definition of the slope, line degree and assertion](https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/GroundTheory/HeightsAndTheta/Heights/KernelsLattice.lean#L25-L88)

Let $\overline F$ be the given full $\mathcal O_K$-lattice of rank $i\ge1$ with its conjugation-compatible Hermitian metrics. Give its generic fibre the adelic norm defined at each finite place by the lattice unit ball and at each infinite place by the given metric. Let $\Lambda$ denote the infimum of the multiplicative heights of its nonzero algebraic vectors and $H_i=\sum_{a=1}^i 1/a$. Lemma 3.2 gives
$$
 \log\Lambda+\widehat\mu_{\max}(\overline F)
        \le (H_i-1)/2 .
$$
Here $\widehat\mu_{\max}\ge\widehat\mu$ by taking the whole space, and $H_i-1\le\log i$ by integral comparison. [É. Gaudron and G. Rémond, *Minima, pentes et algèbre tensorielle*, Israel J. Math. 195 (2013), Lemma 3.2, p. 574](https://lmbp.uca.fr/~gaudron/art10.pdf#page=10)

Given $\varepsilon>0$, choose $x$ with $H_{\overline F}(x)<e^\varepsilon\Lambda$ and take $K'$ generated over $K$ by its finitely many coordinates. The saturated line is $(K'x)\cap(F\otimes_{\mathcal O_K}\mathcal O_{K'})$, with the induced norms. Its normalized Arakelov degree equals $-\log H_{\overline F}(x)$. To see the finite contribution, locally write $x=\pi^a u$ with $u$ primitive in the extended lattice. The coefficient ideal of the saturated line relative to $x$ is $\pi^{-a}\mathcal O_{K',w}$, giving $a\log Nw$ in the degree before division by $[K':\mathbb Q]$. At an embedding $\sigma$, half the logarithm of its one-by-one Gram determinant is $\log\|x\|_\sigma$. Summation over all embeddings counts a complex place twice, as in the absolute height. The same computation applies to $\det F$ and gives the slope normalization in the lemma. The product formula makes the line degree independent of the vector chosen on it. Thus
$$
 \widehat{\deg}_{K'}(K'x)
 >\widehat\mu(\overline F)-\tfrac12(H_i-1)-\varepsilon
 \ \ge\widehat\mu(\overline F)-\tfrac12\log i-\varepsilon.
$$
This supplies the line input with no contribution from the discriminant or degree of the extension. The subsequent comparison of arithmetic model slopes over the components requires the other root-tower and intersection inputs of B8.26.
