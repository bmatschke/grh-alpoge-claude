# The boundary term in the Hodge determinant height

On a supplied unitary component of period entry 7, the cusp weight in the base Hodge test has mean at most $2fs\lambda_N$ for the fitted cutoff. Its contribution to the normalized determinant height is therefore at most $fs\lambda_N$ when the corrected and original metrics are compared as below. The estimate is uniform over lattices and level subgroups with the integral trace pairing. It uses the original invariant Hodge measure. The arithmetic problem that remains is to realize these metrics and the lower height of the corrected determinant on the selected component.

## All short isotropic vectors

Let $E$ be CM of degree $2f$, $n=r+s$, $s\ge1$, $n\ge3s+1$. Let $\Gamma$ be an arithmetic level subgroup of the unitary isometry group of an $\mathcal O_E$-lattice $\Lambda$ of signature $(r,s)$ at each real place of the totally real subfield. On its symmetric-space quotient use Haar probability. At each point write $\|\cdot\|$ for the positive majorant and $\lambda_1$ for its first lattice minimum. We use the trace pairing of the component, integral on $\Lambda$, nondegenerate on $E$ by trace duality, with absolute value at most $\|v\|\|w\|$. Multiplication by $\alpha\in E$ has operator norm at most $\max_\sigma|\sigma\alpha|$.

Write $C_t$ for the number of **all** nonzero isotropic vectors of length less than $t$. Then
$$
             \mathbb E C_t=c_{\Gamma,\Lambda}\,t^k,
             \qquad k=2f(n-1),\quad 0\le c_{\Gamma,\Lambda}<\infty.       \tag{1}
$$
Here is a proof of finiteness and of the exponent, including the multiples on a rational isotropic line. There are finitely many $\Gamma$-classes of rational isotropic $E$-lines by finiteness of the arithmetic-group orbits of rational parabolic subgroups of this line type, together with Witt extension. For one representative $Ey$, with $0\ne y\in\Lambda$, the vectors in $Ey\cap\Lambda$ have the form $\alpha y$ for $\alpha$ in a fractional ideal $\mathfrak a$. The line stabilizer realizes a finite-index subgroup of the units on its line. Indeed in a rational Witt decomposition the diagonal matrices acting by $u,1,\bar u^{-1}$ on the line, perpendicular complement of the hyperbolic plane, and dual line preserve a split reference lattice for integral units $u$. The two integral stabilizers are commensurable, and taking the level subgroup preserves finite index. Thus it suffices to sum over $\alpha$ modulo this finite-index unit group. [Reduction theory for arithmetic groups](https://personal.math.ubc.ca/~cass/research/pdf/boulder-1.pdf)

For fixed $y$, its vector stabilizer has unipotent radical and reductive quotient the unitary group of $y^\perp/Ey$. It has no nontrivial rational character over $\mathbf Q$ (the determinant torus is norm-one). Its arithmetic stabilizer has finite covolume by Borel–Harish-Chandra. Unfold the sum over the $\Gamma$-orbit of $y$ by Tonelli. On the product of real null cones the resulting invariant measure is, up to a finite constant, the product of $\delta(h_w(z,z))\,dz$ at each place $w$. Indeed the group acts transitively on each punctured cone, and this coarea measure is invariant under the unitary group. On writing $z=(z_+,z_-)$ in a diagonal presentation of $h_w$, the null condition is $|z_+|^2=|z_-|^2$. Polar coordinates give a finite angular measure and radial density proportional to $R^{2n-3}\,dR$. This is integrable at zero. Common dilation by $t$ scales the product measure by $t^k$. Replacing $y$ by $\alpha y$ leaves the vector stabilizer unchanged and scales the orbit integral at fixed cutoff by $\prod_w|\alpha_w|^{-2(n-1)}=|N_{E/\mathbf Q}\alpha|^{-(n-1)}$. After clearing the fixed denominator of $\mathfrak a$, the sum over $\alpha$ modulo units is bounded by a fixed multiple of the sum of $N(\mathfrak b)^{-(n-1)}$ over integral ideals. This converges since $n-1>1$. Finitely many cusps give (1), including $c_{\Gamma,\Lambda}=0$ when there is no rational cusp. None of these covolumes or ideal sums needs a uniform bound. [Borel and Harish-Chandra, arithmetic subgroups](https://www.mathi.uni-heidelberg.de/~wienhard/retreat10/references/borel_harishchandra_2.pdf)

## A uniform estimate independent of the covolumes

Put $v_0=2f\operatorname{rd}(E)$, $t_0=v_0^{-1/2}$ and $a=2fs$, so $k\ge3a$ and $a\ge2$. There are $2f$ rationally independent integers $\omega_i\in\mathcal O_E$ with every conjugate of modulus at most $v_0$. For the norm squared given by the sum over all $2f$ embeddings, the dual trace lattice is the inverse different up to conjugation. Each nonzero dual vector has norm at least $\sqrt{2f}/\operatorname{rd}(E)$ by the norm of its ideal and arithmetic-geometric mean. Euclidean transference $\lambda_{2f}(\Lambda_E)\lambda_1(\Lambda_E^*)\le2f$ gives the claimed bound even with $\sqrt{2f}\operatorname{rd}(E)$. [Banaszczyk, transference for successive minima](https://doi.org/10.1007/BF01445125)

For two vectors of length strictly less than $t_0$, all trace pairings with $\omega_i$ times the second vector are integers of modulus strictly less than one. Trace duality makes the Hermitian pairing zero. Hence the short vectors span a totally isotropic $E$-space of real dimension at most $a$. Packing balls of radius $\lambda_1/2$ in this space shows, for $\lambda_1<t\le t_0$,
$$
          1\le C_t\le (1+2t/\lambda_1)^a .
$$
If $\lambda_1\ge t$ there are no short vectors. Thus with $I=\mathbb E C_{t_0}$ and $u=t_0/\lambda_1$, (1) gives $\Pr(u>x)\le I x^{-k}$ for $x\ge1$. On $u\le2$ one has $C_{t_0}\le5^a$. On $u>2$ one has $1+2u\le5u/2$. Integrating the tail on the latter set yields
$$
 I\le5^a+5^a2^{-k}\frac{k}{k-a}I
   \le5^a+\frac{75}{128}I,\qquad I\le\frac{128}{53}5^a .
$$
For example, the truncated moment used here is at most $I(2^{a-k}+a\int_2^\infty x^{a-k-1}\,dx)$. The coefficient estimate uses $k\ge3a$ and $a\ge2$. With $Y=\log^+u$, integration at the crossing point of $1$ and $(128/53)5^a e^{-kv}$ now gives
$$
 \mathbb E Y\le\frac{a\log 5+\log(128/53)+1}{k}<1.                 \tag{2}
$$
This includes the anisotropic case. On any sheet with the Roadmap's pointwise cusp weight $0\le U\le fs[2\log^+(1/\lambda_1)+\log(2fs\operatorname{rd}(E))]$ it follows that
$$
 \operatorname{mean} U\le fs[2+\log(4 f^2s\operatorname{rd}(E)^2)]
                  \le 2fs\log(N\operatorname{rd}(E))\le2fs\lambda_N. \tag{3}
$$
Indeed $N\ge4fn^2$ and $\exp(2)s\le4n^4$. The estimate holds on each sheet before averaging, with its own lattice. Finite-index sheets retaining the same lattice also have identical means by invariance and normalization. For the invariant Hodge determinant, its top curvature volume on the symmetric domain is proportional to invariant measure, and hence gives precisely Haar probability after normalization. The proportionality follows from invariance and transitivity, with positive top degree. On its canonical log-singular extension the non-pluripolar measure puts no mass on the boundary. [Pointwise majorant and original cusp integral](https://github.com/rh-lean-roadmap/rh-lean-roadmap/blob/dc5594a62bb2b94139788df817db693cd939a046/docs/src/book/main.tex#L50739-L50772) · [Automorphic metrics on toroidal compactifications](https://arxiv.org/abs/math/0502085)

## From the two metrics to a height inequality

Use weights $\phi=-\log\|e\|$ in a local frame. Write $H(\phi)$ for arithmetic self-intersection divided by $(e+1)$ times the geometric degree and by the coefficient-field degree where that degree is not already normalized. On the same integral determinant line suppose the original and corrected weights are semipositive of finite energy, with the usual arithmetic change-of-metric formula. If $\psi=\phi+U/2$ on the interior, then
$$
              H(\phi)\ge H(\psi)-\tfrac12\operatorname{mean}_{\phi}U.   \tag{4}
$$
For smooth weights put $u=\psi-\phi$, $\omega_t=c_1(\phi+tu)$ and $g=\deg L^e$. The normalized height increment is the integral from zero to one of $g^{-1}\int u\,\omega_t^e$, averaged over embeddings. Its derivative with respect to $t$ inside the outer integral is $-e g^{-1}\int du\wedge d^cu\wedge\omega_t^{e-1}\le0$, by Stokes with the positive convention for $dd^c$. Thus the increment is bounded above by the value at zero. For semipositive finite-energy weights the same inequality follows from the mixed energy formula and integration by parts for non-pluripolar products, which give $\int u\,\omega_\psi^j\omega_\phi^{e-j}\le\int u\,\omega_\phi^e$ successively for $j=1,\ldots,e$. These integrals use the normalized field average and have no boundary mass. Constant metric shifts give equality, fixing the normalization. This argument applies also after taking an ample rational perturbation if the arithmetic energies and original weighted means converge to the ones in (4). [Berman and Freixas i Montplet, §§2 and 4](https://arxiv.org/pdf/1209.0996) · [Energy and integration by parts](https://arxiv.org/abs/0907.4490)

Consequently, on a supplied component where the integral model realizes these two heights, the corrected horizontal-height and nefness argument giving $H(\psi)\ge-C_hfs\lambda_N$ entails $H(\phi)\ge-(C_h+1)fs\lambda_N$. The conclusion uses the corrected metric itself, or a sequence converging to its energy. A pointwise majorant for $U$ alone does not identify the cutoff determinant, its vertical correction, its regularizations, or the lower bounds on horizontal curves. The [flag-to-base projection](PERIOD_HODGE_TEST_ON_BASE.md) specifies exactly which part of this comparison enters the Hodge test.
