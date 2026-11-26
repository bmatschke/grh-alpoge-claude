# The paired reference estimate in Jin's reconstruction

Kaiwen Jin gives an estimate for the **sum of the two served theta-image indices and the Hermitian pairing index** used in period entry 7. It is in the integral division argument. Appendix J bounds the other term in the same calculation, the negative-member covolume. The two estimates use the same row in Jin's structural selection proposition. That proposition takes the arithmetic field and marking data and the trace, theta, Galois and geometric comparisons on the prescribed hosts and levels as inputs. Applying the calculation to our linked member therefore requires identifying that member with an admitted realization of those inputs. [Jin's structural selection][selection] · [Our signed base-layer identity, equation (5)](PERIOD_SIGNED_LEVEL_TRANSFER.md#transfer-of-the-signed-inequality-and-a-base-only-arithmetic-test)

## The finite estimate in the original units

Fix the coefficient field $K$ with its prescribed involution. At $v\mid p$ write $\ell_v=\log Nv/[K:\mathbb Q]$, $e_v=v_v(p)$, and $I_v(A,B)=v_v(\det B)-v_v(\det A)$ in a common rational frame. Let $D$ be the reference rank, $M_j$ the negative stage lattice, $T_{j,t}$ the projected upper lattice, $\theta_{j,t}$ its map and $t=\mu(v)=\mu(\bar v)$. Set

$$
 i_{jv}=I_v(M_j,\theta_{j,t}T_{j,t})+
         I_{\bar v}(M_j,\theta_{j,t}T_{j,t}),\qquad
 J_{jv}=I_v(T_{j,t},T_{j,t}^{\#}).
$$

The dual uses the stage form at the conjugate place. These are the two terms $i_{jw}+q_{jw}$ in our equation (5). Jin identifies the projected upper carrier using $P=(Z^*HZ)^{-1}Z^*H$ and identifies its geometric image and induced pairing with the indicated $\theta_{j,t}$ and $Z^*HZ$. The source also transports the support from the base member under coefficient extension. The signed indices multiply by relative ramification, while the normalized forced allowance $F_0(j,v)$ uses the valuation $v(p)=1$. Off the nonreference support $W$, all the base indices and $F_0$ vanish. [Lattice, dual and support identifications][identifications] · [Signed index and metric conventions][definitions]

On the matched member the two auxiliary runs give

$$
 \sum_j i_{jv}\le D e_v
 \left(2\sum_j F_0(j,v)+\sum_j\epsilon_{jv}+2/p^2\right)
 \qquad(v\in W).
$$

The error includes the truncated indices on the run assigned to each place and those at its conjugate. The run rank satisfies $n_Z/(hD)\le3$. Each run has weighted truncated allowance $n_Z fmb$. Thus the two runs and both signs cost at most $12fmb$ per stage after division by $hD$. The other prime errors have weighted sum $O(LB_0)$ per stage, where $L=x^\varepsilon$, $B_0=fmbL$. The $2F_0$ term is signed. At the two type primes its sign is needed before the ramified allowances are estimated. [Prime errors][primeerror] · [Two-run rank and truncated allowances][tworuns] · [Conjugate-place inequality][combined]

For the pairing, let $C$ be the intersection of the retained space with the upper carrier, so $\operatorname{length}(T_{j,t,v}/C_v)=e_v\eta_j(v)$. Suppose $\varpi_v^{n_{jv}} C_v$ lies in the lower class lattice, with $n_{jv}\le e_v J_0(j,v)$. Classwise integral pairing and the common stabilizer denominator $d_G$ give $d_G\varpi_v^{n_{jv}} C_v\subseteq T_{j,t,v}^\#$. By monotonicity of signed indices,

$$
 J_{jv}\le D e_vJ_0(j,v)+e_v\eta_j(v)+D v_v(d_G).
$$

The last determinant comes from scalar multiplication in rank $D$. Jin proves a prime sum $\sum_v\ell_v e_vJ_0(j,v)\le30|T_2|mbL^2+2mb$ for the matched coefficient lattices. The remaining $\eta_j(v)$ is the length of the projection onto the retained generic summand modulo its integral intersection, divided by $e_v$. Its quantitative estimate uses the strict field lengths on that coefficient field. [Pairing argument][pairing] · [Prime sum][lower] · [Projection denominator and its field input][denom]

In particular, the total $2/p^2$ error over all stages and serving places costs **less than one** in squared-slope units. Indeed $\sum_{v\mid p}e_v\ell_v=\log p$. There are 52 primes $p\le240$, and $2\sum_{p\le240}\log(p)/p^2<0.979$. One rational check sets $q=\lfloor\log_2p\rfloor$, bounds $\log p$ by $qU(1/3)+U((p-2^q)/(p+2^q))$ and sums, where

$$
 U(t)=2\sum_{i=0}^9\frac{t^{2i+1}}{2i+1}+
          \frac{2t^{21}}{21(1-t^2)} .
$$

For $p>240$ use the two residue classes $1,5\bmod6$. Since $\log x/x^2$ is decreasing there, bound each value at $n$ by its mean on $[n-6,n]$. The two sums together cost at most $\tfrac23(\log235+1)/235<0.019$, including the numerator $2$. Exact rational evaluation of the two upper estimates gives a sum below $0.997$. This allowance applies to a subset of the coefficient places as well, and is charged once after summing the stages. [Jin's inverse-square estimate][tail]

## Where the comparison enters entry 7

In our base-layer formula, adding the two bounds gives the signed main term $2\sum_{v\in W,j}\ell_v e_vF_0(j,v)$, the controlled prime and stabilizer errors, and the residual projection allowance $D^{-1}\sum_{j,v\in W}\ell_v e_v\eta_j(v)$. Jin identifies $\operatorname{lcv}(M_j)/D$ with the negative member's framed covolume divided by its rank at stage $i=j-1$. In Appendix J, $\operatorname{lcv}$ is twice the logarithmic basis height divided by $[K:\mathbb Q]$ and its bound is $\mathcal M_i+O(B_0\log\log x)$. The cutoff precedes the row, tied point and stage. This accounts for the factor of two and the main-term sign when inserting that estimate in our equation (5). [Combined base estimate and identification of the negative lattice][finalsum] · [Appendix J's statement and quantifiers][geom]

Thus the paired-reference inequality has a direct source on Jin's selected realization. To transfer it, match the rational stage maps and forms, both coefficient places and assigned tuple, the lower-lattice inclusion, the two-run rank and depth bounds and the residual Hecke projection on our selected member. The source gives a separate construction of a full grid on an admitted supported start preserving the definite corner tests and their ordered Fourier transforms. Its cross-tuple measured period identity also invokes the invertible linked word map and matching of both arrow readings on the tested columns. The single-square proportionality is stated for each fixed matching. These hypotheses matter when using Jin's separately stated period identity for entries 1 and 4. [Transport of definite tests][grid] · [Fixed-square normalization][square] · [Bottom row and common translation][bottom] · [Two-arrow calculation][twop]

[selection]: https://github.com/yuiyuiui/Natural-Language-Proof-Generalized-Riemann-Hypothesis/blob/405237610e58ab9d4a9d5d54d9a0548a0c44227c/sections/item01-level.tex#L18753-L18792
[identifications]: https://github.com/yuiyuiui/Natural-Language-Proof-Generalized-Riemann-Hypothesis/blob/405237610e58ab9d4a9d5d54d9a0548a0c44227c/sections/integral-division.tex#L8911-L8969
[definitions]: https://github.com/yuiyuiui/Natural-Language-Proof-Generalized-Riemann-Hypothesis/blob/405237610e58ab9d4a9d5d54d9a0548a0c44227c/sections/integral-division.tex#L8971-L9029
[primeerror]: https://github.com/yuiyuiui/Natural-Language-Proof-Generalized-Riemann-Hypothesis/blob/405237610e58ab9d4a9d5d54d9a0548a0c44227c/sections/integral-division.tex#L7779-L7822
[tworuns]: https://github.com/yuiyuiui/Natural-Language-Proof-Generalized-Riemann-Hypothesis/blob/405237610e58ab9d4a9d5d54d9a0548a0c44227c/sections/integral-division.tex#L7824-L7860
[combined]: https://github.com/yuiyuiui/Natural-Language-Proof-Generalized-Riemann-Hypothesis/blob/405237610e58ab9d4a9d5d54d9a0548a0c44227c/sections/integral-division.tex#L9175-L9199
[pairing]: https://github.com/yuiyuiui/Natural-Language-Proof-Generalized-Riemann-Hypothesis/blob/405237610e58ab9d4a9d5d54d9a0548a0c44227c/sections/integral-division.tex#L9137-L9173
[lower]: https://github.com/yuiyuiui/Natural-Language-Proof-Generalized-Riemann-Hypothesis/blob/405237610e58ab9d4a9d5d54d9a0548a0c44227c/sections/integral-division.tex#L8728-L8758
[denom]: https://github.com/yuiyuiui/Natural-Language-Proof-Generalized-Riemann-Hypothesis/blob/405237610e58ab9d4a9d5d54d9a0548a0c44227c/sections/integral-division.tex#L832-L861
[tail]: https://github.com/yuiyuiui/Natural-Language-Proof-Generalized-Riemann-Hypothesis/blob/405237610e58ab9d4a9d5d54d9a0548a0c44227c/sections/integral-division.tex#L9195-L9216
[finalsum]: https://github.com/yuiyuiui/Natural-Language-Proof-Generalized-Riemann-Hypothesis/blob/405237610e58ab9d4a9d5d54d9a0548a0c44227c/sections/integral-division.tex#L9212-L9223
[geom]: https://github.com/yuiyuiui/Natural-Language-Proof-Generalized-Riemann-Hypothesis/blob/405237610e58ab9d4a9d5d54d9a0548a0c44227c/sections/j-arithmetic-covolume.tex#L9-L30
[grid]: https://github.com/yuiyuiui/Natural-Language-Proof-Generalized-Riemann-Hypothesis/blob/405237610e58ab9d4a9d5d54d9a0548a0c44227c/sections/d-prescribed-level.tex#L787-L800
[square]: https://github.com/yuiyuiui/Natural-Language-Proof-Generalized-Riemann-Hypothesis/blob/405237610e58ab9d4a9d5d54d9a0548a0c44227c/sections/e-period-comparisons.tex#L283-L289
[bottom]: https://github.com/yuiyuiui/Natural-Language-Proof-Generalized-Riemann-Hypothesis/blob/405237610e58ab9d4a9d5d54d9a0548a0c44227c/sections/e-period-comparisons.tex#L1936-L1973
[twop]: https://github.com/yuiyuiui/Natural-Language-Proof-Generalized-Riemann-Hypothesis/blob/405237610e58ab9d4a9d5d54d9a0548a0c44227c/sections/e-period-comparisons.tex#L1975-L2021
