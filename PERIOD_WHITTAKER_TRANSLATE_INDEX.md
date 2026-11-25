# A single Whittaker determinant for the actual base image index

In equation (5) of [the signed base reduction](PERIOD_SIGNED_LEVEL_TRANSFER.md), the two image indices may be bounded with one signed determinant on a specified subspace for each served place and layer. All denominators coming from this extraction cost $o(b)$ on the linked window. The original deduction bounds every subspace of the ambient cusp-form space simultaneously. The estimate below applies even when no such positive remainder bound has been supplied.

## Local calculation

Use the geometric, group-action and projected-lattice identifications of [B4.54a][local] and [its application in B8.38b][application]. Let $B,\Theta$ be the actual ambient and normalized stable theta lattices over the valuation ring at $v$. In the local lemma one has $\Theta\subseteq B$. Write $W$ for the $U,\psi$ eigenspace, $Z=W\cap\mathrm{im}(e)$ for the actual selected row, and $D=\dim Z$. With left coset representatives $g_1,\ldots,g_s$ for $P/U$, put
$$
 \mathcal V=\bigoplus_{a=1}^s \rho(g_a) Z,\qquad h=|U|,
 \quad J_v=[B\cap\mathcal V:\Theta\cap\mathcal V]_v .
$$
Throughout, the index is the signed determinant valuation with positive index for a sublattice. The space $\mathcal V$ is independent of the representatives because $U$ acts on $Z$ by a scalar character. It is stable under $P$. Directness follows from the character condition of B4.54a. Indeed $H=\sum_{u\in U}\psi(u)^{-1}\rho(u)$ satisfies $H\rho(g_a^{-1}g_c)z=h\delta_{ac}z$ on $Z$.

For either $L=B$ or $L=\Theta$, write $L_Z=L\cap Z$, $L_{\mathcal V}=L\cap\mathcal V$ and $L^\oplus=\bigoplus_a\rho(g_a)L_Z$. Group stability and the coordinate extractors give
$$
     L^\oplus\subseteq L_{\mathcal V}\subseteq h^{-1}L^\oplus .
$$
If the first $s-1$ coefficients of an element of $L_{\mathcal V}$ lie in $L_Z$, subtract their translates. The last translated coefficient lies in $L$ on its own, hence its preimage lies in $L_Z$. Therefore the first $s-1$ coefficients give an injection
$$
  L_{\mathcal V}/L^\oplus \hookrightarrow
  (h^{-1}L_Z/L_Z)^{s-1}.
$$
In particular $0\le c_L=[L_{\mathcal V}:L^\oplus]_v\le (s-1)D v(h)$. Transitivity of signed indices now gives the exact formula
$$
       s[B_Z:\Theta_Z]_v=J_v+c_\Theta-c_B .                     \tag{1}
$$
At every place with $h$ a unit there is equality $s[B_Z:\Theta_Z]_v=J_v$.

Use the inclusions $\Theta\subseteq\sigma\Theta_K$, $h(\Theta_K)_W\subseteq\Theta_0$, and $e\Theta_0\subseteq e\Theta_J$ from B4.54a. For $z\in\Theta_Z$, the vector $hz/\sigma\in\Theta_0$ is fixed by $e$. Thus $(h/\sigma)\Theta_Z\subseteq e\Theta_J$. The local comparison $X_3\subseteq A$ with loss $e_v\xi_{vj}$ proves the bound on the original theta image
$$
 [M_j:A_{j,t_w}]_v\le
   \frac{J_{vj}}s-Dv(\sigma_{vj})
       +D(2-1/s)v(h)+e_v\xi_{vj} .                              \tag{2}
$$
This uses the coordinate identifications $M_j=B_Z$ and $A_{j,t_w}=A$ at both $v=w,\bar w$ of the *same* serving tuple. It requires no depth cutoff, positive-part inequality, or bound on the ambient cusp dimension. The factor $2-1/s$ includes the cost of putting $h(\Theta_K)_W$ in the projected lattice. Away from the divisors of $h$ the averaging contribution vanishes exactly, while the comparison allowance $e_v\xi_{vj}$ in (2) can remain.

## The signed target on the selected family

For each twisted $w$, put $j$'s data at $v=w,\bar w$ equal to those of the run actually serving $w$. The parameter $t_{\bar w}=t_w$, and the original rule chooses a run by the residue characteristic. Use (2) twice and sum, counting the two terms also at a self-conjugate place. With $s_j=[P:U]$ and the usual weights $\ell_w$, this gives
$$
 \frac1D\sum_{j,w\in{\rm Tw}}\ell_w i_{jw}
 \ \le\ 2\sum_{j,w\in{\rm Tw}}\ell_w
  \left\{\frac{J_{wj}}{s_jD}-v_w(\sigma_{wj})\right\} + o(b).     \tag{3}
$$
Indeed the error before the $o(b)$ estimate is bounded by
$$
  4\sum_{j,w\in{\rm Tw}}\ell_w v_w(h_j)
   +\frac2D\sum_{w\in{\rm Tw}}\ell_w e_w\sum_j\xi_{wj}.
$$
The original geometric comparison supplies $\sum_j\xi_{wj}\le p_w^{-2}$; under the specified number-field normalization, the second term is at most $2D^{-1}\sum_p (\log p)/p^2$. At a theta prime $v_w(h_j)/e_w=fr(r-1)/2$, $r=k+m-1$; at every other prime it vanishes. The two theta primes are $g_0,g_1$. Thus the first term is at most $2mfr(r-1)(\log g_0+\log g_1)$, using the $m$ layers (or the same bound with their actual count). It is polynomial in $x$ and hence $o(b)$ on [the original linked window][window]. Restricting these nonnegative errors to twisted places only decreases them.

Consequently the following *sufficient* arithmetic estimate for entry 7 can replace the individual two-run subspace bounds on this route:
$$
 \frac{\sum_j\operatorname{lcv}(M_j)}D
  +\sum_{j,w\in{\rm Tw}}\ell_w
      \left\{\frac{2J_{wj}}{s_jD}-2v_w(\sigma_{wj})+\frac{q_{jw}}D\right\}
 \le \sum_{j,\rho}\beta_jw_{j\rho}\log\Omega+2F_*
         +O\!\left(mL(B_0+N_c)\right).
$$
The version retaining the embedding correction subtracts $E_{Q,0}/D$ on the left. This is a signed upper bound on a fixed family of actual translate-span determinants, the retained target covolumes, and the source pairing, with the original main term. Neither the determinant identity nor the extraction estimate proves this remaining arithmetic bound. In particular, the central arithmetic input $J_{wj}$ still measures the *integral* normalized theta image. A rational isomorphism or an ambient determinant outside this particular subspace does not specify it.

The remaining index can be arbitrarily large under the local extraction assumptions alone. Over a DVR take $P=U=1$, $Z=K$, $B=\mathcal O$, $e=1$, $\sigma=1$, and $\Theta=\Theta_K=\Theta_0=\Theta_J=X_3=A=\pi^N\mathcal O$. The error is zero and (2) reads $N\le N$. This example isolates the need for arithmetic information on the actual theta sections. It makes no assertion about their values on the selected PEL family.

[local]: https://github.com/rh-lean-roadmap/rh-lean-roadmap/blob/02a95b4c62db610642af5f278ee5d0d6df87b348/docs/src/book/main.tex#L31776-L31813
[application]: https://github.com/rh-lean-roadmap/rh-lean-roadmap/blob/02a95b4c62db610642af5f278ee5d0d6df87b348/docs/src/book/main.tex#L54143-L54162
[window]: https://github.com/rh-lean-roadmap/rh-lean-roadmap/blob/02a95b4c62db610642af5f278ee5d0d6df87b348/docs/src/book/main.tex#L32985-L33008
