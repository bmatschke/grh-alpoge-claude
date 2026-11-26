# Elementary divisors of a ramified word-prime incidence block

In the [word-prime Hecke index](PERIOD_WORD_PRIME_HECKE_INDEX.md), the mixed-to-ordinary part of the upward operator consists of copies of one integral matrix. Its determinant suffices for the mean slope. The full list of its elementary divisors determines the loss for individual integral directions on this part of the map.

Let $p=T_u\ge3$, $k\ge1$, $W=\mathbf F_p^k$, and $O$ the coefficient DVR at a place above $p$. Give it the valuation $v_O(p)=e$. On each side of the matrix, use arrays whose sum on each punctured line is zero. Source lines are in $W$ and target lines are in $W^*$. The map is
$$
 (\mathcal H b)(g)=\sum_{g(z)=1}b(z).
$$
For $1\le j\le p^k-2$ let $s_p(j)$ be its base-$p$ digit sum. The multiset of valuations of the elementary divisors of this map on those integral lattices is
$$
 \boxed{\left\{\ e\left\lfloor\frac{s_p(j)}{p-1}\right\rfloor:
       1\le j\le p^k-2,\quad (p-1)\nmid j\ \right\}.}             \tag{1}
$$
Each label contributes once, including repeated valuations. The number of labels is $(p-2)(p^k-1)/(p-1)$. A coefficient fibre of rank $a$ repeats the multiset $a$ times. The formula concerns the map from the **mixed** coefficient lattice to the ordinary one. The subsequent change from the scaled ordinary lattice to the mixed one has the explicit determinant given in the companion proof. Composing the two requires retaining their relative bases to determine individual invariant factors of the composite.

## The integral character basis

Identify $W$ with $L=\mathbf F_{p^k}$ and pair it with itself by $(y,z)\mapsto\operatorname{Tr}_{L/\mathbf F_p}(yz)$. This pairing is perfect, also when $p\mid k$. The nonzero vectors form the multiplicative cyclic group $L^\times$. The lines are its cosets of $\mathbf F_p^\times$. The trace-form diagonalization for this incidence graph is due to Nica. We use it integrally at the defining characteristic and follow the valuations through the two field sizes. [Nica, *Unimodular graphs and Eisenstein sums*](https://arxiv.org/abs/1505.05034)

One can complete $O$ and pass to a finite unramified extension containing the Teichmüller lifts of $L$. Neither change alters elementary-divisor valuations. Let $\omega:L^\times\to O'^\times$ be the Teichmüller character in that extension. The functions $z\mapsto\chi_j(z)=\omega(z)^{-j}$, with $j$ modulo $p^k-1$, give an integral basis of all arrays: their inverse Fourier matrix has denominator $p^k-1$, which is a unit. The line sum of a character vanishes exactly when its restriction $\chi_{j,0}$ to $\mathbf F_p^\times$ is nontrivial. In the other case summing over that subgroup multiplies the character by $p-1$, also a unit. This proves the label constraint in (1) over the integers of the extension.

In that basis, row $g_y(z)=\operatorname{Tr}(yz)$ gives
$$
 (\mathcal H\chi_j)(g_y)=\chi_j(y)^{-1} E_j,\qquad
 E_j=\sum_{\operatorname{Tr}z=1}\chi_j(z).
$$
Thus the matrix is diagonal up to a permutation between the two bases. The diagonal entries are Eisenstein sums. Let $\psi(t)=\zeta_p^t$ and $G_L(\chi_j)=\sum_{z\ne0}\chi_j(z)\psi(\operatorname{Tr}z)$, adjoining $\zeta_p$ only for the following valuation calculation. The contribution from trace zero to this last sum vanishes: multiplication by a scalar in $\mathbf F_p^\times$ preserves that fibre and can multiply the summand by a nontrivial character value. The sum over the trace-$t$ fibre for $t\ne0$ is $\chi_{j,0}(t)E_j$. It follows that
$$
 G_L(\chi_j)=E_jG_{\mathbf F_p}(\chi_{j,0}).
$$
Stickelberger's Gauss-sum valuation, or the Gross–Koblitz formula, gives $v_p(G_L(\omega^{-j}))=s_p(j)/(p-1)$ with $v_p(p)=1$. On the prime field the corresponding valuation is $r/(p-1)$ for $r\equiv j\pmod{p-1}$, $1\le r\le p-2$. Since $r$ is also the residue of the digit sum, their difference is $\lfloor s_p(j)/(p-1)\rfloor$. This computes the valuations of entries already in the unramified extension. Descending them, or equivalently comparing the determinantal ideals before and after the faithfully flat extension, proves (1). [Gross and Koblitz, *Gauss sums and the p-adic Γ-function*](https://www.sas.rochester.edu/mth/sites/doug-ravenel/otherpapers/gross_koblitz.pdf)

## Consequences for the integral test

The labels $j$ and $p^k-1-j$ give exponents summing to $k-1$, since their base-$p$ digit sums add to $k(p-1)$ and neither is a multiple of $p-1$. This recovers the mean valuation $e(k-1)/2$ used in the determinant and the symmetry expected from $\mathcal H^t\mathcal H=p^{k-1}I$. For instance, for $p=3$, $k=3$ the exponents in $p$-units are $0,1,2$ with multiplicities $3,7,3$. For the general reduction modulo the maximal ideal the surviving directions are exactly the labels with $1\le s_p(j)\le p-2$. Stars and bars gives the rank
$$
             \binom{k+p-2}{k}-1.
$$
Indeed each digit sum in this range automatically enforces all the base-$p$ digit bounds. If a row functional has values $a_j$ on the corresponding inverse-character basis vectors in the unramified extension, then the ideal generated by its values on the image of the ramified incidence map has valuation
$$
 \min_j\left(v_{O'}(a_j)+e\left\lfloor s_p(j)/(p-1)\right\rfloor\right)
$$
with the zero functional assigned $+\infty$. This provides a direction-by-direction finite reading of a served period on a matched middle block. Applying it to an original period requires the values of that period on the indicated coefficient fibres. [Source of the matched neighbor transports](https://github.com/yyyyychen/RH-Natural-Language-Proof/blob/d4dfb1a282dbf857288e73eb1f546dbfcc5899b8/tex/ramified-column.tex#L288-L340)
