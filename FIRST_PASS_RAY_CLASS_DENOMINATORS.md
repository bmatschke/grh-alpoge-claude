# Removing the smoothing factor from an individual critical ray-class value

One part of the first-pass export asks how the denominators of a toric coefficient vary when split primes are added to a conductor. Kings and Sprang give an integral formula for differences of individual partial Hecke values. At eligible primes the following consequence gives an explicit denominator for each ray class. Varying the principal ideal in the CM field also treats the critical shift one when the angular infinity type is nonzero. To apply it to the project's order-class sums one must also compare the two class measures and integral periods. [Kings–Sprang, *Eisenstein–Kronecker classes, integrality of critical values of Hecke $L$-functions and $p$-adic interpolation*, Theorem 4.10 and Corollary 4.13](https://arxiv.org/pdf/1912.03657#page=51) · [Published paper](https://doi.org/10.4007/annals.2025.202.1.1) · [Project's toric denominator statement][target]

## One ray class

Let $E$ be a CM field of degree $n$, $\mathfrak f\ne\mathcal O_E$ a conductor, and $\chi$ a critical algebraic Hecke character of conductor $\mathfrak f$ as in that theorem. Write its infinity type as $\beta-\alpha$ in the authors' convention. Use their CM abelian variety, integral differentials on it and its dual, and the rational torsion section required in Theorem 4.10. Let $R$ denote their base ring. Work at a finite place $\lambda$ over $\ell$ where $R$ and the character integers are integral and $\ell\nmid N\mathfrak f$. The authors' indicated choice of $R$ also inverts the field discriminant. For a ray class $B$ put
$$
 Y_B=\frac{(\alpha-1)!\,(2\pi i)^{|\beta|}}
               {\Omega^\alpha(\Omega^\vee)^\beta}
       L_{\mathfrak f}(\chi,0,B).
$$
Here the powers and factorial indexed by embeddings are products. For an auxiliary ideal $\mathfrak c$ prime to $\mathfrak f$ and $\ell$, choose an integral representative $\mathfrak b$ of $B$ prime to $\mathfrak f$, $\mathfrak c$ and $\ell$. Such representatives exist by approximation in the ray class. Corollary 4.13 gives
$$
       \chi(\mathfrak c)N\mathfrak c\,Y_B-Y_{B[\mathfrak c]}
       \ \in\ \mathcal O_\lambda .
$$
The dependence of the corollary's denominator on $N(\mathfrak b\mathfrak c)$ causes no loss at the chosen place. The local ring here can be taken in any algebraic coefficient field large enough for the data. When a nonzero multiplier expresses $Y_B$ as a quotient of algebraic numbers this also proves its algebraicity. [Definition of partial $L$-functions, §4.1](https://arxiv.org/pdf/1912.03657#page=46) · [Integral CM models and the smoothing formula, pp. 51–52](https://arxiv.org/pdf/1912.03657#page=51)

Choose a rational integer $m>1$ coprime to $\ell$ with $m-1\in\mathfrak f$. For example require $m\equiv1\pmod{N\mathfrak f}$. Then $\mathfrak c=(m)$ is trivial in the ray class group and $N\mathfrak c=m^n$. On positive integers congruent to one the infinity type gives $\chi((m))=m^{|\beta|-|\alpha|}$. Consequently, for
$$
 d=n+|\beta|-|\alpha|
$$
the same corollary gives $(m^d-1)Y_B\in\mathcal O_\lambda$ for **every** ray class $B$. Negative $d$ causes no difficulty since $m$ is a local unit.

Suppose $d\ne0$. For odd $\ell$ and $(\ell-1)\nmid d$, choose $m$ reducing to a generator of $\mathbf F_\ell^\times$. Then $m^d-1$ is a unit and every $Y_B$ is integral at $\lambda$. For any odd $\ell$, one can instead choose $m\equiv 1+\ell\pmod{\ell^2}$. For $\ell=2$ choose $m\equiv5\pmod 8$. In each case the Chinese remainder theorem also imposes the ray congruence. Put $s_\ell=1$ for odd $\ell$ and $s_2=2$. The binomial expansion gives
$$
 v_\ell(m^d-1)=s_\ell+v_\ell(|d|).
$$
Indeed, raising $1+\ell^{s_\ell}u$ to a prime-to-$\ell$ power preserves the valuation of the difference from one. Raising it to the $\ell$-th power increases that valuation by one, including in the indicated dyadic range. Inversion preserves it as well. Thus
$$
 \frac{v_\lambda(Y_B)}{v_\lambda(\ell)}
 \ \ge\ -s_\ell-v_\ell(|d|).
$$
For fixed infinity type, this loss is independent of the ray conductor as long as $\ell$ stays away from it and the integral-model hypotheses hold at $\lambda$. The auxiliary integer itself may change with the conductor. The same lower bound holds for any sum of these $Y_B$ with $\lambda$-integral coefficients.

## A principal ideal that also works at the endpoint

The scalar calculation loses all information when $d=0$. Varying the generator in the CM field gives a bound there as well. Suppose $\ell$ is unramified in $E$, still prime to the conductor, and keep the integral-model assumptions at the chosen coefficient place. For $a\equiv1\pmod{\mathfrak f}$ write the algebraic character on principals in the form
$$
       \chi((a))N(a)=\prod_{\sigma:E\hookrightarrow\overline{\mathbf Q}_\ell}
                             \sigma(a)^{b_\sigma}.
$$
Here the embeddings use the chosen coefficient reading, and $b_\sigma$ is the corresponding infinity exponent of the ideal character plus one from the norm. In particular $\sum b_\sigma=d$. Suppose at least one $b_\sigma$ is nonzero. Define
$$
 k=\min_{b_\sigma\ne0} v_\ell(|b_\sigma|),\qquad b'_\sigma=b_\sigma/\ell^k.
$$
We claim that there is a single principal ray-trivial auxiliary ideal, good at $\lambda$, for which the smoothing multiplier has normalized valuation exactly $s_\ell+k$. This gives $v_\lambda(Y_B)/v_\lambda(\ell)\ge -(s_\ell+k)$ for **all** $B$, including when $d=0$.

To prove it, work in a finite unramified extension of $\mathbf Q_\ell$ containing the images of the completions of $E$. For a prime $v\mid\ell$ of residue degree $f_v$, the embeddings inducing $v$ reduce to the $f_v$ different embeddings of its residue field. Relative to any one of these they are $z\mapsto z^{\ell^j}$ for $0\le j<f_v$. Pick $v$ with at least one of its $b'_\sigma$ nonzero modulo $\ell$. The polynomial
$$
     \sum_{j=0}^{f_v-1}\overline{b'_{\sigma_j}}\, Z^{\ell^j}
$$
is nonzero of degree at most $\ell^{f_v-1}<\ell^{f_v}$. Choose a residue $z$ where it does not vanish. Choose $u\in\mathcal O_E$ with residue $z$ at $v$, zero at the other primes above $\ell$, and zero modulo $\mathfrak f$. These conditions are compatible by the Chinese remainder theorem. Put $a=1+\ell^{s_\ell}u$. One may add a sufficiently large rational multiple of $\ell N\mathfrak f$ to $u$ to ensure $(a)$ is a nontrivial ideal. It is coprime to $\ell\mathfrak f$ and trivial in the ray class group.

Set $A'=\prod_\sigma\sigma(a)^{b'_\sigma}$. Modulo $\ell^{s_\ell+1}$, the expansion, including for negative integer exponents, is
$$
 A'\equiv 1+\ell^{s_\ell}\sum_\sigma b'_\sigma\sigma(u).
$$
The sum is a unit by the choice of $z$. Hence $v_\ell(A'-1)=s_\ell$ with $v_\ell(\ell)=1$. The same binomial power calculation as above gives $v_\ell((A')^{\ell^k}-1)=s_\ell+k$. But $(A')^{\ell^k}=\chi((a))N(a)$. Applying Corollary 4.13 with $\mathfrak c=(a)$ proves the claim.

There is also a zero-loss test. If for some $v\mid\ell$ the integer $\sum_j b_{\sigma_j}\ell^j$ is nonzero modulo $\ell^{f_v}-1$, prescribe the residue of $a$ to generate $k(v)^\times$, the residue one above the other primes over $\ell$, and $a\equiv1\pmod{\mathfrak f}$. The same product formula gives a smoothing multiplier which is a unit. Every $Y_B$ is then integral. Both arguments use the individual infinity exponents, so they apply to a critical twist at $h=1$ with nonzero angular infinity type.

## Comparison with the required toric values

For a unitary character $\lambda_0$ trivial on the real subfield ideles and an integer $h\ge1$, write the shifted ideal character as $\chi(\mathfrak a)=\lambda_0(\mathfrak a)(N\mathfrak a)^{-h}$. Its value at zero is the unitary value at $h$, with the same omitted Euler factors. If this is the critical algebraic character and period realization above, then $\lambda_0((m))=1$ for the chosen positive rational $m$. Hence $d=n(1-h)$. At $h>1$ the bound just proved applies. It gives integrality whenever $\ell$ is odd and $(\ell-1)\nmid n(h-1)$. At $h=1$ the scalar auxiliary ideal gives a zero multiplier. The [angular-type calculation on the original row](FIRST_PASS_EXPORT_LOCAL_CONDITIONS.md) shows that the two exponents at a conjugate pair differ, so the $b_\sigma$ cannot all be zero. The CM principal-ideal argument therefore gives its bound in the Kings–Sprang normalization at the true conductor, also at this endpoint. A conductor-one character also uses the separate two-ideal formula of Theorem 4.10.

The project normalizes $T$ by $(C_0T)^{12}/\Delta_\Lambda^{\mathrm{wt}}$ using its own integral period lattice $\Lambda$. It asks for a bound on **each order class** and on its character sums, including at primes of the fixed conductor. Kings–Sprang use the actual conductor of the algebraic character. If the auxiliary modulus is enlarged while the conductor stays smaller, an imprimitive distribution formula is also required. A passage by a sum of disjoint ray classes would preserve the bound if its measure and the change of periods have integral coefficients at $\lambda$. Dividing by an index, changing the integral period basis, or restoring Euler factors requires accounting for that factor's valuation. The required exponent furthermore contains explicit contributions from real-subfield class zeta values, local conductor terms and the weight. The calculation above removes the smoothing loss at the stated primes or measures it explicitly. Establishing these normalization comparisons and treating the excluded primes are still needed for the full export. [Project's class terms and target exponent][target] · [Toric readings on the original row](FIRST_PASS_TORIC_COEFFICIENTS.md)

[target]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AbelianVarietyTheory/BlockTheory/DivisorBase/VpBounds.lean#L62-L89
