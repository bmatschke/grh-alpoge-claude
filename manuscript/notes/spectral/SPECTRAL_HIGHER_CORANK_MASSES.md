# Primitive sublattice masses in the higher-corank collision estimate

Fix the definite row of the tied model, of rank $k$ over the finite-unramified CM extension $E/F$. Put $f=[F:\mathbf Q]$, $v=\mathrm{rd}(E)/2\ge1$, $\rho=2v$, $T=T_u$ and $N=T^f$. The prime $T$ splits completely. Let $M_i$ be the standard unimodular genus masses and $m_0$ the actual row genus mass. We give the primitive sublattice mean on this row at **all** coranks $2\le s\le k$ and evaluate the factorials in its mass ratio. At corank two they give a factor $k^{-(1-o(1))kf}$ after the two orbital determinant normalizations have been cancelled. This pays the required degenerate collision saving with a weaker real-amplitude estimate. The identification of the full pair fibres and orbital amplitudes is stated separately below.

## The actual mean, including the last two coranks

Let $\delta\ge1$ be an integer and let $C_j(L,\delta)$ count saturated sublattices of rank $j=k-s$ of $L$ with discriminant module of additive order $\delta^2$. A saturated sublattice is exactly the intersection of its rational span with $L$. Use
$$
 X_s=M_sM_{k-s}/M_k\quad (2\le s<k),\qquad X_k=1.
$$
For $C\ge16$, uniformly in the determinant label,
$$
 \frac1{m_0}\sum_{[L]}\frac{C_j(L,\delta)}{|\mathrm{Aut}(L)|}
 \le X_s(\delta/N)^k(\delta N)^{C(s+\log f)}.                 \tag{1}
$$
In particular $X_s$ is independent of the two reduced Gram labels also when $s=k-1,k$.

Indeed (7)–(8) of the [two-lattice genus calculation](SPECTRAL_PAIRED_GENUS.md) apply to every $j,s\ge1$. The cyclic discriminant module of the row has order $N^2$, and choosing one hyperplane in the residue space at each of the $f$ places gives $m_0=M_k[(T^k-1)/(T-1)]^f\ge M_k N^{k-1}$. The genus bound for $j\ge1$, at $a=\delta^2$, divided by this actual mass, is
$$
 X_s\frac{\delta^j}{N^{k-1}}(\delta N)^{9s+8+4\log_2(2f)}.
$$
Passing to (1) uses $N/\delta^s\le \delta N$ and $9s+9+4\log_2(2f)\le16(s+\log f)$ for $s\ge2$. This includes $j=1$. The primitive-space argument uses only positive ranks on the two sides. At $s=k$ the zero lattice is the sole candidate, and occurs only for $\delta=1$. The right side of (1) is at least one since its exponent on $N$ is nonnegative. The original source uses a separate height-dependent index estimate for the two end ranks. Equation (1) treats the actual primitive-space average which is an input to counting pairs; the remaining index and isometry choices must still be counted. [Source mean and the endpoint split][mean] · [Actual split-level genus mass][split]

## The factorials retained by the genus formula

For $2\le s\le k-2$ put $h=\min(s,k-s)$ and $l=k-h$. With $L_i=L_F(i,\eta_{E/F}^i)$ the identity is
$$
 X_s=M_2\rho^f(\pi/v)^{(hl+3)f}
  \left[\prod_{a=0}^{h-1}\frac{(l+a)!}{a!}\right]^{-f}
  \frac{\prod_{i=3}^{h}L_i}{\prod_{i=l+1}^{l+h}L_i}.          \tag{2}
$$
To see this, divide the product of the adjacent mass quotients at $i=3,\ldots,h$ by those at $i=l+1,\ldots,l+h$ and multiply by $M_2$. Each quotient equals $\rho^{-f/2}[(i-1)!(v/\pi)^i]^f L_i$. There are two extra denominator factors and the difference between the two sums of indices is $hl+3$. This proves (2), including $h=2$. For the Euler ratio and its reciprocal, the logarithm is at most $2f\sum_{i\ge3}\log\zeta(i)\le2f(2-\zeta(2))< f\log3$. Here $L_i,L_i^{-1}\le\zeta(i)^f$ termwise, and $\sum_{n\ge2}\sum_{i\ge3}n^{-i}=2-\zeta(2)$. The Euler ratio is thus between $3^{-f}$ and $3^f$. [Unitary mass formula and local factors, Gan–Hanke–Yu](https://web.math.princeton.edu/~jonhanke/Web-02/Mass-Formula-of-Shimura/shimura-mass.pdf) · [Functional equation and small ranks](SPECTRAL_PAIRED_GENUS.md)

In particular $\prod_{a=0}^{h-1}(l+a)!/a!\ge(l!)^h\ge(l/\mathrm e)^{lh}$. Since $l\ge k/2$ and $hl\ge2k-4$, for $k\ge40$ we get the uniform inequality
$$
 (kv)^{kf}X_s
 \le\left[6\pi^3(80 f)^{16}(2\pi\mathrm e)^{2k}
                 k^{4-k}\right]^f.                              \tag{3}
$$
Indeed use $M_2\le(80fv^2)^{16f}$ and $2\pi\mathrm e/(kv)<1$ in (2). The residual power of $v$ per place is $32+1-3+k-(2k-4)=34-k\le0$. For each $\epsilon>0$, (3) is at most $k^{-(1-\epsilon)kf}$ for all sufficiently large $k$, uniformly for $1\le f\le k$ and $v\ge1$. This is a statement about the actual genus and involves no archimedean orbital estimate. At $s=k-1$ the exact replacement is $X_{k-1}=M_1/R_k$ where $R_k=M_k/M_{k-1}$; (3) is used only at the interior ranks.

## A weaker real estimate suffices for degenerate higher-corank pairs

Use the row normalization, index counts and amplitude notation of [B8.08k][sum]. Write $m=2r+2$, $b\ge2$, $H=b^{Cm^2f}$, $B=kf\log k$ and $g=g_0g_1$. In the original degenerate estimate the squared amplitude at label $Z$ is first multiplied by its Gram normalizer $n_Z$ and by
$$
 b_2(Z)^{2k},\qquad b_2(Z)=T^{-f/2}K(Z).
$$
The arithmetic bound contains exactly the inverse compensation when the normalized amplitudes are inserted. Retain this angular factor, the row weights, the permitted moment and the label decay. **For any fixed $0\le\theta<1/2$, one may replace the factor $(C_a/k)^{kf}$ in the degenerate real majorant by $k^{\theta kf}$** and still obtain the required total degenerate bound $d\exp(-B/2)$ in the original eventual range. The factor $\exp(O(m^6f\log b))$ in that majorant is allowed as before. Here $d$ is the dimension of the first column. The nondegenerate estimates retain their original assumptions. [Original fibre, amplitude and determinant cancellations][fibres]

To verify the rate, use the original fixed-label arithmetic counts for the degenerate class and sum the determinant-cancelled estimates over the represented labels. This argument is homogeneous of degree one in the bound for the squared normalized real amplitude, as each pair uses the product of two square roots. After label summation the bound at rank $s$ is
$$
 d(2/g)^{(s-2)kf}F_s\exp(Cm^6f\log b)k^{\theta kf}.
$$
Here $F_s=(kv)^{kf}\Xi_s C^{kf}H^{C(s+m)m^2}(Csf)^{6sf}\Gamma$, with even the original, coarser $\Xi_s$ permitted at the end ranks. At $s=2$, $\Xi_2=X_2$ for $k\ge4$. Each factor of $F_2$ apart from $(kv)^{kf}X_2$ has logarithm $O_C(kf)$, uniformly on the selected ranges. Indeed $C'm^5f\log b\le k$, $m\le f\le k$, $\log\Gamma= C_\Gamma m^5f\log b$, and $(2+m)m^4=O(m^5)$. The extra $Cm^6 f\log b$ is also $O_C(kf)$ since $m\le f$. Equation (3) therefore gives $d\exp(-(1-\theta-o(1))B)$ at $s=2$ and leaves room below $d\exp(-B/2)/k$.

For $s\ge3$ the source size calculation gives $F_s\le k^{skf/8}$, including its separate endpoint indices. This numerical bound follows from the adjacent mass formula and the displayed parameter inequalities in [the rank summation][rates]. Now $g\ge(kb)^8$, so $2/g\le k^{-7}$ for $k\ge2$. After division by $d$ the log bound in units of $B$ is at most $-7(s-2)+s/8+\theta+O_C(1/\log k)$. It is already below $-1$ at $s=3$ eventually, and decreases thereafter. Summation gives the claimed bound. The proof does not require an estimate of a signed sum.

There is also a part of this degenerate calculation on which the ordinary squared-integral estimate alone suffices. It is an inequality on each relevant nonsingular term, so may be applied even when the pair lies in the degenerate class. Its coefficient is $2R'$, $R'=d_{u'}/D^\star$. For pairs whose labels obey
$$
           2R'[b_2(Z)b_2(Z')]^k\le k^{\theta kf},               \tag{4}
$$
the uncancelled angular factor in the product of the ordinary majorants is already within the preceding allowance. All other powers are bounded by the degenerate majorant since the label size is at least one and $a_1\le a_2$ in the original notation. The same proof applies to any subset satisfying (4). For example when both penultimate minors vanish one has $K(Z)=K(Z')=1$; on the original dimension window $R'\le3/\Gamma^2$ this lies in (4) for sufficiently large parameters and any fixed $\theta>0$. This deduction requires the ordinary squared-integral and arithmetic pair-fibre comparisons on the selected terms. The remaining real test in this approach concerns the larger angular factors outside (4). [Ordinary amplitude on individual terms][ordinary] · [Dimension window](../periods/PERIOD_FULL_REFERENCE_PAIRING.md)

For a fixed interior rank the moments can be chosen separately as well. Set $e_s=c(s+m)m+c(1+\log_2(2f))$, $a_2=C_2(m^2+2m^4)$ and write $\sigma_Z$ for the source label size. After the two determinants cancel, $\Xi_s$ is constant in both labels. The estimate $h_Z\le P\sigma_Z^4$ therefore costs only $4(e_s+cr^2)$ in the exponent of each $\sigma_Z$. The integer
$$
 q_s=\left\lceil(r+1)\left[4(e_s+cr^2)+a_2/2+12(r+1)^2\right]\right\rceil
$$
suffices wherever the moment estimates are available up to the source maximum. Indeed the remaining power of each label is at most $-12(r+1)^2$, whose sum is bounded by the entry-lattice packing argument of [B8.08k][labels]. This moment is below the source's single common order. At $s=2$ its displayed formula is independent of $k$ for fixed $m,f$ and constants. Matching the remaining index and isometry fibres, actual orbital integrals and the other cells to the selected operator is still required for the global spectral assertion.

[mean]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AbelianVarietyTheory/Proofs/FlagMeasures/MeanCountPrimitiveSublatticesOverGenus.lean#L143-L219
[split]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AbelianVarietyTheory/Proofs/FlagMeasures/RowsRawMassAndGenusMass.lean#L32-L46
[sum]: https://github.com/rh-lean-roadmap/rh-lean-roadmap/blob/02a95b4c62db610642af5f278ee5d0d6df87b348/docs/src/book/main.tex#L16514-L16585
[fibres]: https://github.com/rh-lean-roadmap/rh-lean-roadmap/blob/02a95b4c62db610642af5f278ee5d0d6df87b348/docs/src/book/main.tex#L45778-L45874
[rates]: https://github.com/rh-lean-roadmap/rh-lean-roadmap/blob/02a95b4c62db610642af5f278ee5d0d6df87b348/docs/src/book/main.tex#L43810-L43862
[ordinary]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Formalism/SharpRestriction/CuspSpanNormBounds/CayleyDegreeNondegeneracy/RowsND.lean#L132-L149
[labels]: https://github.com/rh-lean-roadmap/rh-lean-roadmap/blob/02a95b4c62db610642af5f278ee5d0d6df87b348/docs/src/book/main.tex#L43767-L43806
