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

There is also a zero-loss test. If for some $v\mid\ell$ the integer $\sum_j b_{\sigma_j}\ell^j$ is nonzero modulo $\ell^{f_v}-1$, prescribe the residue of $a$ to generate $k(v)^\times$, the residue one above the other primes over $\ell$, and $a\equiv1\pmod{\mathfrak f}$. The same product formula gives a smoothing multiplier which is a unit. Every $Y_B$ is then integral. At shift one, nonzero angular infinity type suffices for the valuation bound. Integrality with zero loss additionally requires the displayed residue condition.

## An enlarged modulus and the price of extracting a class

There is a further bound when the modulus of a partial sum exceeds the conductor of its character. Assume $\ell$ is unramified in $E$. Let $\mathfrak m$ be prime to $\ell$ and divisible by the conductor of $\chi$. Let $H$ be the full ray class group at $\mathfrak m$, or a quotient of it if only the sum over the inverse image of one quotient class is sought. Assume the Kings–Sprang integral CM data for the finitely many characters $\chi\psi$, $\psi\in\widehat H$, use the same differential periods at $\lambda$. The base ring may be enlarged at $\lambda$ to contain the character values. All these characters have the same infinity exponents. Put
$$
 D_b=s_\ell+\min_{b_\sigma\ne0} v_\ell(|b_\sigma|),\qquad
 D_u=s_\ell+\min_{b_\sigma-1\ne0}v_\ell(|b_\sigma-1|).
$$
Assume the first minimum exists. The second is needed only if one of the twists has conductor one. Both exist in the nonzero angular case.

For a twist of nontrivial conductor, apply Theorem 4.10 to its full critical value. The auxiliary principal ideal can be chosen congruent to one modulo $\mathfrak m$ by the construction above. The normalized full value then has valuation at least $-D_b$, measured with $v(\ell)=1$. If a twist has conductor one, Theorem 4.10 has a second multiplier $1-(\chi\psi)(\mathfrak c')$. On principals its exponents are $b_\sigma-1$. Repeat the same residue and binomial argument to obtain an auxiliary principal ideal $\mathfrak c'$ with loss $D_u$. Impose the additional congruence $a'\equiv1\pmod{\mathfrak c}$ on its generator to keep the two ideals coprime. The prime-to-$\ell$ congruences are compatible with the prescribed residues at $\ell$. The theorem now gives loss at most $D_b+D_u$. Use $D=D_b$ when all twists have nontrivial conductor and $D=D_b+D_u$ otherwise. [Separate conductor-one formula, Theorem 4.10](https://arxiv.org/pdf/1912.03657#page=51)

For each twisted character, omitting the extra Euler factors to reach $\mathfrak m$ multiplies its true-conductor value at zero by factors $1-(\chi\psi)(\mathfrak p)$ at primes $\mathfrak p\nmid\ell$ where it is unramified. Each is locally integral. Indeed a positive power of $\mathfrak p$ is ray-principal for the true conductor. Its generator has valuation zero at every prime over $\ell$, so the principal-character formula shows that $(\chi\psi)(\mathfrak p)$ is a local unit. The Euler identities hold first in the domain of convergence and then at the critical value by continuation.

Let $Y^{(\mathfrak m)}_B$ be the sum restricted to $B\in H$ in this imprimitive ideal series, with the same period normalization. Finite character orthogonality gives
$$
     |H|Y^{(\mathfrak m)}_B
      =\sum_{\psi\in\widehat H}\psi(B)^{-1}Y^{(\mathfrak m)}(\chi\psi).
$$
The character coefficients are roots of unity. Hence
$$
    \frac{v_\lambda(Y^{(\mathfrak m)}_B)}{v_\lambda(\ell)}
       \ge -D-v_\ell(|H|).
$$
This proves an imprimitive bound and exhibits the loss from extracting one class. At fixed infinity type it is uniform over any set of these data on which $v_\ell(|H|)$ is bounded and the period hypotheses hold. For unrestricted auxiliary primes the orders of these groups can acquire new $\ell$-parts. Uniform control would require bounding that loss or recovering the individual class sums integrally. Identifying a quotient $H$ and its ideal sums with the project's order classes, with the same class measures, is a separate step.

## Applying the distribution formula at the actual modulus

There is a sharper result under the Kings–Sprang integral geometric hypotheses at the **chosen modulus** $\mathfrak m$. Keep $\ell$ unramified in $E$ and prime to $\mathfrak m$. For $\mathfrak m\ne(1)$, assume the specified $\mathfrak m$-torsion section is defined over the base of the integral CM realization with the chosen differential periods. Such prime-to-$\ell$ torsion can be rationalized after a finite extension of the good-reduction base at $\lambda$. This extension preserves the normalized valuations. Under these hypotheses no factor $|H|$ is needed, even when the conductor of $\chi$ is smaller than $\mathfrak m$.

Indeed let $\mathfrak b$ be an integral representative of an $\mathfrak m$-ray class, prime to $\ell\mathfrak m\mathfrak c$. Put $\Gamma_{\mathfrak m}=\{u\in\mathcal O_E^\times:u\equiv1\pmod{\mathfrak m}\}$. Integral ideals in this ray class correspond to
$$
  \Gamma_{\mathfrak m}\backslash (1+\mathfrak m\mathfrak b^{-1}),
        \qquad x\longmapsto (x)\mathfrak b.
$$
The principal-character identity holds on this coset because the conductor of $\chi$ divides $\mathfrak m$. Summing there for large real part and continuing to zero gives the formula of Lemma 4.2 with $\mathfrak m$ throughout. In particular the partial value equals $\chi(\mathfrak b)$ times the authors' Eisenstein–Kronecker series on the lattice $\mathfrak m\mathfrak b^{-1}$ at the indicated torsion point. The critical infinity type restricts to the smaller unit group $\Gamma_{\mathfrak m}$. [The ideal parametrization and analytic identity](https://arxiv.org/pdf/1912.03657#page=46)

Apply Theorem 4.9 to this lattice, its $\mathfrak m$-torsion section, and the degree-zero smoothing function of Proposition 4.12. That distribution relation gives the difference of the series for $\mathfrak b$ and $\mathfrak b\mathfrak c$, with coefficient $N\mathfrak c$ on the first. The theorem puts the result, including its period normalization, in the ring with $\mathfrak m N(\mathfrak b\mathfrak c)$ inverted over the base. Multiply by the local unit $\chi(\mathfrak b\mathfrak c)$ and use the partial-value identity twice. This gives
$$
 \chi(\mathfrak c)N\mathfrak c\,Y^{(\mathfrak m)}_B
        -Y^{(\mathfrak m)}_{B[\mathfrak c]}\in\mathcal O_\lambda
$$
for each *individual* ray class. This argument applies the authors' geometric theorem at $\mathfrak m$ without requiring that $\mathfrak m$ be the conductor of a primitive character. Choose $\mathfrak c=(a)$ as in the CM principal-ideal construction, with $a\equiv1\pmod{\mathfrak m}$. The classes coincide. Thus the loss is at most $D_b$, independent of the new primes and the size of the ray class group. The same bound holds when summing over the fibre of a quotient group. [Geometric integrality, Theorem 4.9](https://arxiv.org/pdf/1912.03657#page=50) · [Distribution relation and its application, Proposition 4.12 and Corollary 4.13](https://arxiv.org/pdf/1912.03657#page=52)

For $\mathfrak m=(1)$ the character is unramified at finite primes. Suppose $D_b,D_u$ are both defined and the corresponding conductor-one integral model hypotheses hold. In the conductor-one proof of Theorem 4.10, before summing over classes, the period-normalized combination on each representative $\mathfrak b$ is integral. Writing $E_{\mathfrak a}$ for the normalized series on $\mathfrak a^{-1}$, its four terms are
$$
 N\mathfrak c\,(E_{\mathfrak b\mathfrak c'}-E_{\mathfrak b})
      + E_{\mathfrak b\mathfrak c}-E_{\mathfrak b\mathfrak c\mathfrak c'} .
$$
Choose the two coprime auxiliary ideals principal and prime to $\ell$. All four ideals have class $B$. Multiplying by $\chi(\mathfrak b\mathfrak c\mathfrak c')$ and substituting $\chi(\mathfrak a)E_{\mathfrak a}=Y_B$ gives $(1-\chi(\mathfrak c'))(\chi(\mathfrak c)N\mathfrak c-1)Y_B$. The two principal-ideal constructions give loss at most $D_b+D_u$ at every ordinary ideal class, with no class-number denominator. [Two-ideal distribution in the proof of Theorem 4.10](https://arxiv.org/pdf/1912.03657#page=53)

## Comparison with the required toric values

For a unitary character $\lambda_0$ trivial on the real subfield ideles and an integer $h\ge1$, write the shifted ideal character as $\chi(\mathfrak a)=\lambda_0(\mathfrak a)(N\mathfrak a)^{-h}$. Its value at zero is the unitary value at $h$, with the same omitted Euler factors. If this is the critical algebraic character and period realization above, then $\lambda_0((m))=1$ for the chosen positive rational $m$. Hence $d=n(1-h)$. At $h>1$ the bound just proved applies. It gives integrality whenever $\ell$ is odd and $(\ell-1)\nmid n(h-1)$. At $h=1$ the scalar auxiliary ideal gives a zero multiplier. The [angular-type calculation on the original row](FIRST_PASS_EXPORT_LOCAL_CONDITIONS.md) shows that the two exponents at a conjugate pair differ, so the $b_\sigma$ cannot all be zero. The CM principal-ideal argument therefore gives its bound in the Kings–Sprang normalization at the true conductor, also at this endpoint. A conductor-one character also uses the separate two-ideal formula of Theorem 4.10.

The project normalizes $T$ by $(C_0T)^{12}/\Delta_\Lambda^{\mathrm{wt}}$ using its own integral period lattice $\Lambda$. It asks for a bound on **each order class** and on its character sums, including at primes of the fixed conductor. Kings–Sprang use the actual conductor of the algebraic character. At an enlarged modulus the Fourier argument incurs a class-group loss. The direct distribution argument removes it when the integral geometric data are provided at the enlarged modulus. A passage by a sum of disjoint ray classes would preserve the bound if its measure and the change of periods have integral coefficients at $\lambda$. Dividing by an index, changing the integral period basis, or restoring Euler factors requires accounting for that factor's valuation. The required exponent furthermore contains explicit contributions from real-subfield class zeta values, local conductor terms and the weight. The calculation above removes the smoothing loss at the stated primes or measures it explicitly. Establishing these normalization comparisons and treating the excluded primes are still needed for the full export. [Project's class terms and target exponent][target] · [Toric readings on the original row](FIRST_PASS_TORIC_COEFFICIENTS.md)

[target]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AbelianVarietyTheory/BlockTheory/DivisorBase/VpBounds.lean#L62-L89
