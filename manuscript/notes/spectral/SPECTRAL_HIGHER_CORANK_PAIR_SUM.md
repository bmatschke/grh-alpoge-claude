# The absolute sum over arithmetic pairs of corank at least two

Consider two words $u,u'$ in a tied member. The word $u$ indexes the incoming column of dimension $d=d_u^S$. Write $R'=d_{u'}^S/D^\star$, $r=r_S$, $\ell=r+1$, $m=2\ell$, $f=[F:\mathbf Q]$, $v=\mathrm{rd}(E)/2$, $g=g_0g_1$, $T=T_u$ and $N=T^f$. The compact real type of $u$ has dimension $d_\infty$. The row vectors $v_t$ are those in the arithmetic expansion of the Gram operator. A pair $p$ specifies two terms $t,t'$ on the same row and their relative isometry.

Use the original finite frame and row hypotheses, matched Haar and root measures, and real-place bounds on the positive-Gram terms at the moments below. For the latter it suffices to have the wave identities, signed one-step exterior periods, cofactor estimates, and measure and critical-scale comparisons of the [local calculation](SPECTRAL_SHIFTED_MINOR_MOMENTS.md) and the [angular estimate](SPECTRAL_ANGULAR_FROM_ORDINARY_AMPLITUDE.md). On these data there is a constant $K$ independent of the words, field and point in the eventual range such that

$$
\begin{aligned}
 \Gamma_1\sum_{p\ {\rm nondegenerate}}|\langle v_t,v_{t'}\rangle|
 &\le d R'\,(2/g)^{kf}\,e^{Kkf}k^{-kf}v^{(34-k)f},\\
 \Gamma_1\sum_{p\ {\rm degenerate}}|\langle v_t,v_{t'}\rangle|
 &\le d\,e^{Kkf}k^{-2kf}v^{(34-k)f}.
\end{aligned}\tag{1}
$$

Both sums range over the represented relevant nonsingular pairs of corank $2\le s\le k$. The class records degeneracy of the difference pairing on the exceptional quotient. The estimates are uniform also when a term's penultimate minor vanishes. The original thresholds include $m\le f\le k$, $\log f\le\sqrt r$, $1\le v\le b$, $g\ge(kb)^8$ and $k\ge C'm^5 f\log b$, with $C'$ chosen after the fixed count and local constants. Thus (1) supplies respectively the $dR'g^{-kf/2}$ and $d\exp(-kf\log k/2)$ allowances. [Original finite subtotals][subtotal]

## Count and amplitude in the same measure

Let $Z,Z'$ be the reduced Gram labels. Write $G_Z=g^{-mf}\det U_Z>0$, where $U_Z$ is the integral joint frame lattice, and let $n_Z=(\mathrm e\pi/(kv))^{kf}(G_Z/N)^k$. Set $b_1(Z)=1$, $b_2(Z)=T^{-f/2}K(Z)$, where $K$ is the product of the angular quotients (local value one at a zero penultimate minor). For $i=1,2$ in the order of (1), the weighted pair count at these labels, divided by the row mass $M$, is at most

$$
 X_s(csf)^{6sf}(h_Zh_{Z'})^{e_s}
 \left[\frac{(2/g)^{(s-i)f}\sqrt{G_ZG_{Z'}}\,b_i(Z)b_i(Z')}{N}\right]^k.
                                                               \tag{2}
$$

Here $X_s=M_sM_{k-s}/M_k$ for $s<k$, $X_k=1$, $e_s=c(s+m)m+c(1+\log_2(2f))$ and $h_Z=b^{c^2m^3 f}S_c(Z)^4$. Choose $c$ large enough for the explicit exponents in the [finite count](SPECTRAL_FLAG_PAIR_DETERMINANTS.md) and for the [orbit-volume bound](SPECTRAL_ARITHMETIC_ORBIT_VOLUME.md). In enlarging a previous height constant $c_0$ one may take $c\ge |c_0|+2$. Indeed $S_{c_0}\le b^{(c-c_0)m^2 f\ell}S_c$ and $c^2-c_0^2\ge2(c-c_0)$ give $h_{c_0}\le h_c$. The choice precedes the moment coefficient and eventual point threshold.

For an individual term put $A_t=a_t/\sqrt{d_\infty}$, where $a_t$ is the arithmetic amplitude before inserting the square root of its row weight. In the term measures the factorization and the stabilizer estimate give

$$
 n_Z A_t^2 b_i(Z)^{2k}
 \le h_Z^{2cr^2}\Gamma\,\eta_i\,\sigma_Z^{a_i-2q/\ell},\qquad
             \sigma_Z=S_{C_h}(Z),\quad \Gamma=b^{C_\Gamma m^5 f},
                                                               \tag{3}
$$

with $a_1=C_2m^2$, $a_2=C_2(m^2+2m^4)$ and

$$
 \eta_1=e^{(5/2)f2^{-k}}R',\qquad
 \eta_2=e^{2C_2m^6 f\log b}(C_a/k)^{kf}.
$$

Take the constants positive and large enough for all real places. For (3), multiply the local squared bounds. The compact dimensions multiply to $d_\infty$, the ordinary critical product is bounded using the outgoing column, and the square of the orbit volume costs $h_Z^{2cr^2}$. For $i=2$ the second angular bound absorbs the entire $b_2(Z)^{2k}$. Its two extra operator losses contribute the displayed exponential and the extra size exponent. [Critical product on the original column](SPECTRAL_CRITICAL_PRODUCT_ON_ROWS.md) · [Products of the real losses](SPECTRAL_REAL_LOSS_PRODUCTS.md)

Cauchy–Schwarz bounds the absolute inner product at one pair by its row weight times $d_\infty A_t A_{t'}$. The sum of these weights is exactly the quantity counted in (2) times $M$. Moreover $\Gamma_1 M d_\infty\le d$. Indeed at a lattice $\Lambda$ the $\Gamma_1$ marked finite type cosets give at least $\Gamma_1/|\mathrm{Aut}_{F_u}(\Lambda)|$ different marked classes over $\Lambda$. Two lifts in the same class differ by an automorphism, and an automorphism with the fixed flag and dual frame is determined by its action on the middle quotient. Summing over the lattices counts at most all marked classes. Neatness makes their number times $d_\infty$ equal to $d$. This inserts one arithmetic column dimension in each bound. [Row weights, marked classes and the dimension inequality][dimension]

Take square roots of (3) for the two terms in (2). All $b_i$ cancel. The denominator $\sqrt{n_Zn_{Z'}}$ removes exactly $(\sqrt{G_ZG_{Z'}}/N)^k$. Per unit $d$, the product left at the two labels is bounded by

$$
 X_s(2/g)^{(s-i)kf}(kv/(\mathrm e\pi))^{kf}(csf)^{6sf}
       \Gamma\eta_i(h_Zh_{Z'})^{e_s+cr^2}
       (\sigma_Z\sigma_{Z'})^{a_i/2-q/\ell}.                 \tag{4}
$$

## Summation over labels and ranks

Here is an entry-lattice bound with a variable exponent. Put $P=b^{(c^2+2\max(C_h-c,0))m^3 f}$, so that $h_Z\le P\sigma_Z^4$. For any $t_0>2$,

$$
 \sum_Z\sigma_Z^{-4t_0\ell^2}
 \le\left[\left(\frac{9t_0}{t_0-2}\right)^fP^{t_0}\right]^{\ell^2}. \tag{5}
$$

In each normalized entry lattice, two distinct points differ by an element whose product of complex absolute values is at least one. The open products of disks of radius $1/2$ around them are disjoint. A polydisk of radii $R_\tau\ge1$ therefore contains at most $9^f\prod R_\tau^2$ points. Integrating this count against $\prod t_0R_\tau^{-t_0-1}dR_\tau$ on $[1,\infty)^f$ bounds the sum of $\prod_\tau\max(1,|y_\tau|)^{-t_0}$ by $(9t_0/(t_0-2))^f$. Each of the $\ell^2$ normalized entries of a reduced label has product height at most $h_Z$. The entries determine the label. Multiplying the single-entry inequalities and enlarging to independent choices of entries proves (5), first for finite sets and then for their supremum. [Normalized entry lattices and recovery of labels][label]

Use $t_0=3$ and the integer

$$
 q_{s,i}=\left\lceil\ell\left(4e_s+4cr^2+a_i/2+12\ell^2\right)\right\rceil .
$$

The exponent on each label in (4) is now at most $-12\ell^2$. There is no loss proportional to $k$ from $X_s$, even at the end ranks. This order lies below the original common order $(9c+3)km^2$ at its threshold. In particular at $s=2$ the ordinary estimate needs order $O(m^3)$ and the angular estimate needs order $O(m^5)$, using $\log f\le\sqrt r$. Applying (5) twice absorbs the factors of $P$ and numerical constants into the following bound per unit $d$ at rank $s$:

$$
 (2/g)^{(s-i)kf}\eta_i F_s,\qquad
 F_s=(kv)^{kf}X_s C^{kf} b^{C^2(s+m)m^4 f}(Csf)^{6sf}\Gamma .
$$

Indeed the total exponent on $P$ is $2(e_s+cr^2)+6\ell^2=O((s+m)m)$. [Original moment threshold and rank bounds][ranks]

At $s=2$ the [adjacent mass formula](SPECTRAL_HIGHER_CORANK_MASSES.md) has the two denominator factorials $(k-2)!(k-1)!$. Its discriminant powers are $(2v)^f$, $(\pi/v)^{(2k-1)f}$ and at most $v^{32f}$ from $M_2$. Multiplying by $(kv)^{kf}$ leaves $v^{(34-k)f}$. Stirling's inequality and $f\le k$ give $F_2\le e^{O(kf)}k^{-kf}v^{(34-k)f}$. The logarithm of the height and counting factors is $O(kf)$ by the rank threshold. At $s\ge3$ the original rank estimate gives $F_s\le k^{skf/8}$. Its coarse endpoint bounds dominate $X_k=1$ and $X_{k-1}=M_1/(M_k/M_{k-1})\le1$ eventually, by the rank-one mass estimate and the adjacent ratio. Since $2/g\le k^{-7}v^{-1}$,

$$
 \sum_{s=3}^k (2/g)^{(s-2)kf}F_s
 \le v^{-kf}\sum_{s=3}^k k^{[-7(s-2)+s/8]kf}
 \le 2v^{-kf}k^{-53kf/8}
$$

eventually. This proves the first line of (1) after extracting the extra $(2/g)^{kf}$. For the second, $\eta_2\le e^{O(kf)}k^{-kf}$ because $m\le f$ and $k\ge C'm^5f\log b$. Each estimate applies uniformly to finite pair sets, so it proves absolute summability as well. Extending it to the full spectral operator requires the other corank classes, the signed diagonal estimates and the indicated analytic realizations on the selected family.

[subtotal]: https://github.com/rh-lean-roadmap/rh-lean-roadmap/blob/dc5594a62bb2b94139788df817db693cd939a046/docs/src/book/main.tex#L17921-L17956
[dimension]: https://github.com/rh-lean-roadmap/rh-lean-roadmap/blob/dc5594a62bb2b94139788df817db693cd939a046/docs/src/book/main.tex#L43911-L43940
[label]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Formalism/SharpRestriction/CuspSpanNormBounds/CayleyDegreeNondegeneracy/RowsSiz.lean#L95-L178
[ranks]: https://github.com/rh-lean-roadmap/rh-lean-roadmap/blob/dc5594a62bb2b94139788df817db693cd939a046/docs/src/book/main.tex#L43775-L43862
