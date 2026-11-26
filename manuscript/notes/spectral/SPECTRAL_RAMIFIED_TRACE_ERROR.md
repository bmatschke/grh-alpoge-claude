# Isolating one stabilizer sum in the trace on the ramified column

Fix a word on the tied equal-word datum of B8.08oc with its absolute convergence. Write $\mathcal I=\prod_{v\mid g_0g_1}\mathrm{GL}_k(\mathbb F_{q_v})$ for the type group, $n=\dim V_\pi$ for the dimension of the compact coefficient representation, $w_\Lambda=1/|\operatorname{Aut}(\Lambda)|$ for the inverse stabilizer order of the coarse word-marked lattice, and $\mu=\sum_\Lambda w_\Lambda$. The full fine column has dimension $d=n\Gamma_1\mu$, where $\Gamma_1=|\mathcal I/\mathcal U|$. This is the exact free refinement count. The word-prime diamond projector has rank $\rho d$ with $\rho=(1-1/(T-1))^f$. [Fine and coarse classes](SPECTRAL_PROJECTED_FIRST_MOMENT.md) · [Dimension and mass](SPECTRAL_SCALAR_ROW_MASS.md)

For a retained nonzero-Gram cell, let $Z_{\Lambda,\Lambda'}(i)=\sum_{t:\,q_t=(\Lambda,\Lambda'),\,i_t=i}a_t$ be its actual subtotal of real orbital amplitudes at the exact type index $i$. Denote the resulting fine operator by $X$. One may also use the union of the two nonzero-Gram cells. For any set $D$ of coarse lattice pairs put
$$
 \mathcal E_D=\frac{1}{n\mu}
  \sum_{(\Lambda,\Lambda')\in D} w_\Lambda w_{\Lambda'}
    \sum_{i\in\mathcal I}\|Z_{\Lambda,\Lambda'}(i)\|_{\rm HS}^2 .
$$
Let $D_{\rm diag}$ consist of the diagonal coarse pairs and $D_{\rm proj}$ consist of pairs in the same diamond orbit. They are precisely the pairs isometric after replacing the marked vectors by their lines, with all other levels retained. Both weights in this energy are the original inverse stabilizer volumes. The subtotal is taken before squaring. [The same-index subtotals and their transport][rows]

## Normalized local character on a set of rational transports

Let $F_v(i,b)=\gamma_v(ib^{-1})/\gamma_v(1)$ be the matrix on the local type group under counting measure, with $\gamma_v$ its Gelfand–Graev character. The normalized matrix is real symmetric positive semidefinite. Write
$$
 e_v=\prod_{j=2}^k(1-q_v^{-j})^{-1}-1,\qquad
 p_v=\prod_{j=1}^{k-1}(1-q_v^{-j})^{-1},\qquad p=\prod_v p_v .
$$
Every column of $F_v$ has diagonal entry one and off-diagonal squared norm $e_v$. Its operator norm is at most $p_v$. Indeed central convolution on an irreducible representation has eigenvalue $|U_v|$ times its Whittaker multiplicity divided by its dimension. This multiplicity is at most one and a generic irreducible has dimension at least $\prod_{j=1}^{k-1}(q_v^j-1)$ by restriction to successive mirabolic groups. The exact column norm follows by character orthogonality from the local finite character calculation. The global matrix is $F=\bigotimes_v F_v$, with $0\le F\le pI$. [Finite row variance and the individual values](SPECTRAL_FINITE_CHARACTER_VALUES.md) · [Mirabolic dimension argument][gram]

Fix a compatible coarse pair $(\Lambda,\Lambda')$. Let $a$ vary over the diamonds carrying the first coarse class to the second. For each such $a$ take **all** rational isometries identifying its diamond translate with the second chosen representative. These form a torsor of size $h=1/w_{\Lambda'}$. They are isometries of the same pair of underlying definite lattices. Each has a definite coefficient transport $D_\gamma$, a unitary $n$-by-$n$ matrix in the trace convention, and a type displacement $b_\gamma$. Put its centre at $b_\gamma^{-1}$, so the column of $F$ evaluated at $i$ is $\gamma_{\rm fin}(i b_\gamma)/\Gamma_1$. Two different pairs $(a,\gamma)$ have distinct underlying isometries. The marked vectors are nonzero, so a given isometry determines the scalars of the diamond in every coordinate. Changing the choice of bases at a type prime conjugates the relative matrices and leaves ranks and orders unchanged.

At every type place the relative displacement of distinct transports is the reduction, up to conjugation, of a nonidentity automorphism of a positive definite integral lattice of rational rank $2fk$. The finite order of this automorphism is prime to $g_j$, since an element of order $g_j$ would require a cyclotomic factor of degree $g_j-1>2fk$. Its reduction in the chosen split half is nonidentity because the congruence kernel is pro-$g_j$ and the split-half action is faithful. Its order is prime to $g_j$, so it is semisimple and nonunipotent. In particular the centres are distinct in **each single type coordinate**. As the local character is zero on this type of relative displacement, the principal submatrix of $F$ indexed by these centres is the identity. [Original rational transport and compact stabilizers][rows] · [The faithful split local action](SPECTRAL_PROJECTED_FIRST_MOMENT.md)

Suppose $z$ takes values in a Hilbert space, is supported on the centres, and is extended by zero to $\mathcal I$. With counting measure and the same matrices acting in the group variable,
$$
 \|Fz\|\le\sqrt p\,\|z\|,\qquad
 \|(F-I)z\|\le\epsilon_g\|z\|,\qquad
 \epsilon_g=\min_{v_0}
 \left[
 \sqrt{\prod_{v\ne v_0}(1+e_v)-1}
 +\Big(\prod_{v\ne v_0}p_v\Big)\sqrt{e_{v_0}}
 \right].                                                        \tag{1}
$$
For the first bound use $F^2\le pF$ and $\langle z,Fz\rangle=\|z\|^2$. For the second, reserve one type coordinate $v_0$ and write $F=F_{\rm rest}F_{v_0}$ with identity operators on omitted coordinates. The error $(F_{\rm rest}-I)z$ has contributions at disjoint $v_0$-coordinates for different centres. Each single-centre column error on the remaining coordinates has squared norm $\prod_{v\ne v_0}(1+e_v)-1$. The one-place errors $(F_{v_0}-I)z$ are also mutually orthogonal, since at least one other coordinate remains and is distinct between the centres. Thus their norm is exactly $\sqrt{e_{v_0}}\|z\|$. Use $F-I=(F_{\rm rest}-I)+F_{\rm rest}(F_{v_0}-I)$ and $\|F_{\rm rest}\|\le\prod_{v\ne v_0}p_v$. This proves (1) uniformly in the number of isometries. On the actual parameters $e_v\le 1/(q_v(q_v-1)-1)$ and $p_v\le1+1/(q_v-2)$. Hence $p=1+O(f/g_0+f/g_1)$ and $\epsilon_g=O(\sqrt{f/g_0^2+f/g_1^2})$.

## The signed leading term and the error in the trace

For $a=1$ the pair is diagonal and the transports are precisely its coarse stabilizer, in the representative conventions above. Define the scalar
$$
 L_{\rm stab}=\frac{1}{n\mu}
 \sum_\Lambda w_\Lambda^2
 \sum_{\gamma:\,\Lambda\longrightarrow\Lambda,\ a=1}
       \operatorname{tr}\bigl(D_\gamma
             Z_{\Lambda,\Lambda}(b_\gamma^{-1})\bigr).
$$
This uses only the identity type index and its rational stabilizer translates. It retains their actual weights and signs. The projected trace satisfies
$$
 \left|\frac{\operatorname{tr}(\Pi X)}{\rho d}-L_{\rm stab}\right|
 \le \epsilon_g\sqrt{\mathcal E_{D_{\rm diag}}}
       +\sqrt{p(\rho^{-1}-1)}\sqrt{\mathcal E_{D_{\rm proj}}}.     \tag{2}
$$
In particular the factor on the second energy is $O(\sqrt{f/T})$ even when one projectively marked class splits into many vector-marked classes.

To prove this, in the exact trace formula (3) of [the projected first moment](SPECTRAL_PROJECTED_FIRST_MOMENT.md) average over *all* compatible transports for each diamond and each pair. Different choices give identical pair sums by reindexing the complete retained cell and changing the intermediate fibre basis in the trace. For fixed pair let
$$
 z_q(b_\gamma^{-1})=h^{-1}\frac{c(a)}{\rho}D_\gamma^*,
 \qquad \frac{c(a)}{\rho}=\left(-\frac1{T-2}\right)^{s(a)},
$$
where $s(a)$ is the number of changed scalars. The values are Hilbert–Schmidt matrices, and all other entries are zero. Splitting this array into $z^{(1)}$ and $z^{(\ne1)}$ according to the diamond gives
$$
 \frac{\operatorname{tr}(\Pi X)}{\rho d}
 =\frac{1}{n\mu}\sum_{\Lambda,\Lambda'} w_\Lambda
     \sum_i\langle F(z_q^{(1)}+z_q^{(\ne1)})(i),Z_{\Lambda,\Lambda'}(i)\rangle_{\rm HS}.
$$
Here $\langle A,B\rangle_{\rm HS}=\operatorname{tr}(A^*B)$. All finite character weights are real and the normalization uses $d=n\Gamma_1\mu$. Replacing $Fz_q^{(1)}$ by $z_q^{(1)}$ gives exactly $L_{\rm stab}$.

For each fixed $\Lambda$, every diamond determines one $\Lambda'$, has $h$ transports to its representative, and contributes $n|c(a)/\rho|^2/h$ to the squared norm in the appropriate pair. Multiplying that norm by $1/w_{\Lambda'}=h$ removes the auxiliary averaging denominator. Therefore
$$
 \sum_{\Lambda'}w_{\Lambda'}^{-1}\|z_q^{(1)}\|^2=n,\qquad
 \sum_{\Lambda'}w_{\Lambda'}^{-1}\|z_q^{(\ne1)}\|^2
 =n\sum_{a\ne1}|c(a)/\rho|^2=n(\rho^{-1}-1).
$$
The final identity follows by multiplying $f$ copies of $1+(T-2)/(T-2)^2$. Apply (1) to the two arrays. Cauchy–Schwarz on the actual pairs uses $w_\Lambda/w_{\Lambda'}$ for the test and $w_\Lambda w_{\Lambda'}$ for the orbital energy. Dividing by $n\mu$ proves (2).

For the nonzero-Gram union put $K=\alpha^{-1}P_u^*P_u=I+Z_0+X$. The already proved singular bound gives $|\operatorname{tr}(\Pi Z_0)|/(\rho d)\le\rho^{-1/2}e^{-kf\log k/2}$. Thus it suffices on the upstream family to prove
$$
 1+\Re L_{\rm stab}>
 \rho^{-1/2}e^{-kf\log k/2}
 +\epsilon_g\sqrt{\mathcal E_{D_{\rm diag}}}
 +\sqrt{p(\rho^{-1}-1)}\sqrt{\mathcal E_{D_{\rm proj}}}.           \tag{3}
$$
For example $\Re L_{\rm stab}\ge-1/2$ and $\mathcal E_{D_{\rm proj}}\le b^{15}$ suffice eventually: $g_j\ge(kb)^8$, $T-1\ge(g_0g_1)^2$, and $f,k$ have polynomial size in $x$ whereas $b=\exp(x^\varepsilon)$. The lower bound and this coarse-pair energy bound are sufficient tests. Neither is asserted here on the actual orbital amplitudes. Equation (2) proves the complete finite trace error estimate with its original stabilizer masses, irrespective of whether these particular sufficient bounds hold. [Singular estimate](SPECTRAL_DIAGONAL_ZERO_CELL.md) · [Implication for the period entries](../periods/PERIOD_REFERENCE_ROW_DESCENT.md)

[rows]: https://github.com/rh-lean-roadmap/rh-lean-roadmap/blob/02a95b4c62db610642af5f278ee5d0d6df87b348/docs/src/book/main.tex#L43967-L44006
[gram]: https://github.com/rh-lean-roadmap/rh-lean-roadmap/blob/02a95b4c62db610642af5f278ee5d0d6df87b348/docs/src/book/main.tex#L46579-L46606

## A positive first moment at the kernel of the Levi reduction

Write $K$ here for the original compact open ambient finite level and $K^\sharp=\ker(K\longrightarrow\mathcal U)$ for the kernel of its Levi reduction at the two type primes. The map is onto by the split-frame lift. Keep the original finite character on $K^\sharp$ and the original archimedean function. Put $\alpha^\sharp=\alpha\operatorname{vol}(K^\sharp)/\operatorname{vol}(K)>0$. On the tied realization with its actual Poincaré-period unfolding there is a nonnegative number $M^\sharp$ satisfying the exact identity
$$
                   M^\sharp=1+L_{\rm stab,0}+L_{\rm stab}.            \tag{4}
$$
Here $L_{\rm stab,0}$ is defined by the same stabilizer average as $L_{\rm stab}$, retaining only the nonidentity zero-Gram terms. In particular both scalar contributions are real. The earlier arithmetic estimate on the **same-row pairs** gives, for $B=kf\log k$ and $r=(m-2)/2$,
$$
       |L_{\rm stab,0}|\le r e^{-45B/64},
       \qquad \Re L_{\rm stab}\ge-1-r e^{-45B/64}.                  \tag{5}
$$
The lower bound is independent of the still unknown energy of the nonzero-Gram cells.

Here is the construction and normalization of (4). Above each coarse class $\Lambda$, take the $|\mathcal I|/|A_\Lambda|$ finer frames at $K^\sharp$, up to rational transport. At the original level an old discrete coordinate has a scalar seed $\phi$ for each unit vector in the coefficient fibre. For each finer frame use a representative $a$ for it and restrict the corresponding old seed to the part with finite support $S_u(F)aK^\sharp$, retaining its values there. The indicator of this support is invariant on the left under $S_u(F)$. The old seed in this coordinate is supported on $S_u(F)aK$ after passage to finite coordinates, by the rational unipotent approximation and the original support-cell decomposition. Thus pointwise the absolute value of the refined seed is at most the absolute value of the old one for the same coordinate and choice of basis. The absolute periodizations and products needed to unfold its squared norm are consequently dominated by the old integrable expressions. No bound with a varying new level is required. Denote the periodization of the restricted seed by $P^\sharp_{a,j}$ for an orthonormal basis indexed by $j$. Set
$$
  M^\sharp=
   \frac{1}{n|\mathcal I|\mu\,\alpha^\sharp}
      \sum_{a,j}\|P^\sharp_{a,j}\|_{L^2}^2 .
$$
The norm is on the same automorphic quotient with the old Haar measure. Right covariance is now needed only on $K^\sharp$. The finer bases may be chosen independently, since the sum of their squared images is unchanged. [Seed definition and actual covariance][seed] · [Absolute unfolding and squared norms][unfold]

For a refined coordinate its rational stabilizer in $S_u(F)$ on this finite coset is still $N_{u,\rho}$. Indeed inclusion in the old compact open forces the old stabilizer condition, which by neatness leaves this unipotent lattice. Conversely its integral unipotent radical acts as the identity on the middle quotient of the adapted flag and thus has trivial Levi reduction. This argument is unchanged by a split frame lift. The real integration domain for the one-coordinate seed, as well as both rational unipotent groups in the relative double-coset unfolding, are therefore unchanged. For a pair of representatives the active rational returns are selected from the old ones by $a^{-1}r_fa'\in K^\sharp$. Equivalently their relative type $s^{-1}i s'$ is the identity. On this subset the old Levi phase is one, and the root-pairing phase is the original one. Each active return hence has exactly the old archimedean integral, phase and stabilizer measures. Finite integration supplies the single factor $\operatorname{vol}(K^\sharp)$ in place of $\operatorname{vol}(K)$, and dividing by $\alpha^\sharp$ cancels this change. The identity-cell contribution on each diagonal fibre is the identity operator: amongst its rational frame stabilizers only the identity can reduce into $\mathcal U$ up to conjugation, by the prime-to-characteristic and neatness argument. It already has trivial relative Levi. [Integral unipotent and Levi decomposition][split] · [Single finite volume and rational return dictionary][return]

It follows that the proof of the ordinary trace formula for a complete retained cell applies with $\mathcal U$ replaced by $\{1\}$ in the final finite test. Indeed summing $\mathbf1_{x^{-1}i b_\gamma x=1}$ over $x\in\mathcal I$ gives $|\mathcal I|\mathbf1_{i=b_\gamma^{-1}}$; division by $|A_\Lambda|$ accounts for the fibre of the frame parametrization. Transport and choose all $|A_\Lambda|$ possible rational changes of the second intermediate representative and average. This gives $L_{\rm stab,0}$ or $L_{\rm stab}$ after division by $n|\mathcal I|\mu$. It also shows that each such scalar equals $(n\mu)^{-1}\sum_\Lambda w_\Lambda\operatorname{tr} Z_{\Lambda,\Lambda}(1)$ for the corresponding cell, by taking the identity transport for all classes. The sums are real, since taking adjoints in a one-coordinate squared-period computation interchanges a rational return and its inverse, preserving the identity, zero-Gram, and nonzero-Gram strata; equivalently (5) holds for their real parts without using this observation. This proves (4).

For the zero-Gram series the [same-row pair bound, before applying the finite Gram matrix](SPECTRAL_DIAGONAL_ZERO_CELL.md) yields $\mathcal E_{0,\rm all}\le r^2e^{-90B/64}$, also when $r=0$. Apply Cauchy–Schwarz to the averaged $z_q^{(1)}$ above against the zero-cell array with the original weights. Its dual weighted norm has square $n\mu$, as computed before (2). This gives $|L_{\rm stab,0}|\le \sqrt{\mathcal E_{0,\rm all}}$ and then (5). In fact (2) applies to this cell as well, by its rational stabilizer invariance. Writing $u_g=\epsilon_g$ and $v_T=\sqrt{p(\rho^{-1}-1)}$, we obtain
$$
 \left|\frac{\|P\Pi\|_{\rm HS}^2}{\alpha\rho d}-M^\sharp\right|
 \le u_g\sqrt{\mathcal E_{D_{\rm diag}}}
      +v_T\sqrt{\mathcal E_{D_{\rm proj}}}
      +(u_g+v_T)\,r e^{-45B/64}.                                  \tag{6}
$$
The two displayed energies here still refer to the union of nonzero-Gram cells. The spectral problem in (6) is to establish adequate positive mass at the refined level and to control its transfer to the prescribed level. Nonnegativity in (4) alone allows exact cancellation at the threshold $L_{\rm stab}=-1$ when the zero-cell contribution vanishes.

The refined squared norms also admit the *same* word-prime diamond projection. Assemble the single-coordinate seeds linearly into $P^\sharp$ on the refined column of dimension $d^\sharp=n|\mathcal I|\mu$. Mixed products are absolutely integrable by domination by the corresponding pair of old absolute periodizations. The actual diamonds lift to this column, since their support is away from the two type primes, and their action is free because it was free on the original fine classes. Let $\Pi^\sharp$ be their totally ramified projector and put $M^\sharp_\Pi=\|P^\sharp\Pi^\sharp\|_{\rm HS}^2/(\alpha^\sharp\rho d^\sharp)\ge0$. For this target the transfer error is smaller for all the nonidentity diamonds. With $\delta_T=\sqrt{\rho^{-1}-1}$ it is
$$
 \left|\frac{\|P\Pi\|_{\rm HS}^2}{\alpha\rho d}-M^\sharp_\Pi\right|
 \le \epsilon_g\left(\sqrt{\mathcal E_{D_{\rm diag}}}
             +\delta_T\sqrt{\mathcal E_{D_{\rm proj}}}
             +(1+\delta_T)r e^{-45B/64}\right).                     \tag{7}
$$
Indeed the identity cell is the identity on both fine columns: its rational returns within a Bessel stabilizer join precisely the same fine class, and their normalized scalar on that fibre equals one. Thus its normalized projected trace is one at both levels. In the other cells the principal-level finite trace uses the identity matrix in place of $F$ on *all* displaced centres, since $x^{-1}ib_\gamma x=1$ is equivalent to $i=b_\gamma^{-1}$ for every diamond as well. Subtract the refined and original traces, apply (1) to both $z^{(1)}$ and $z^{(\ne1)}$, and use their already computed weighted norms. For the singular cell use the same total energy estimate as in (5). This proves (7); the nonidentity-diamond coefficient in this comparison is $O(\sqrt{f/T}\sqrt{f/g_0^2+f/g_1^2})$.

[seed]: ../../../research/modules/spectral/period_gram_v57/main.tex#L58-L104
[unfold]: ../../../research/modules/spectral/period_gram_v57/main.tex#L760-L843
[split]: ../../../research/modules/spectral/period_gram_v57/main.tex#L295-L340
[return]: ../../../research/modules/spectral/period_gram_v57/main.tex#L881-L939
