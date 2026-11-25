# The relative determinants in period-height entry 7

The seventh entry involves the absolute mean slope of the sharp row. The following identities compute the reference mean and also the mean directly at the sharp level. The computation uses the underlying isomorphisms and metric identities prior to the quantitative covolume or cut estimates in B5.08x. The reference rank throughout is $D=D_R>0$. The finite weights are $\ell_w=\log Nw/[K:\mathbb Q]$. The serving tuples satisfy $t_{\bar w}=t_w$, so the glued lattices use the same tuple at a conjugate pair. The bar on $K$ is the distinguished involution, which induces complex conjugation at $v_0$. At other embeddings the two operations can differ. [Reference hypotheses][data] · [Native local determinant identity][native]

## Exact cancellation at a conjugate pair

Transport the Hermitian form $H_{jt}$ on the definite source of $\theta_{jt}$ to the fixed rational target $KM_j$ by $h_{jt}(x,y)=H_{jt}(\theta_{jt}^{-1}x,\theta_{jt}^{-1}y)$. For a basis $m$ of $M_j$ over the semilocal ring at $w,\bar w$, write $\Delta_{jt}(m)=\det h_{jt}(m,m)$. In a semilocal basis $e$ of $T_{jt}$ put $\theta_{jt}e=mB$ and $J=H_{jt}(e,e)$. Then $\Delta_{jt}(m)=\det J/(\overline{\det B}\det B)$. The signed index of the theta image at $z$ is $v_z(\det B)$. The signed index of the Hermitian dual at $w$ is $-v_w(\det J)$ by the inverse Gram matrix. Consequently
$$
 [M_j:\theta_{jt}T_{jt}]_w+[M_j:\theta_{jt}T_{jt}]_{\bar w}
       +[T_{jt}:T_{jt}^\sharp]_w=-v_w\Delta_{jt}(m).                 \tag{1}
$$
This includes fractional lattice inclusions and self-conjugate places, where the first index occurs twice. The answer is independent of the choice of full source lattice $T_{jt}$ for the fixed rational map and form. A new semilocal basis of $M_j$ multiplies the determinant by a unit at both places. [Index convention and semilocal change][local]

For any rational basis $m$ the ratios $r_{jt}=\Delta_{j,t_0}(m)/\Delta_{jt}(m)$ are independent of $m$ and belong to the fixed field $K^{\bar{}}$. Set $r_t=\prod_jr_{jt}$. If $G_{t,w}$ is the quotient Gram determinant in a semilocal basis, B5.08a and (1) give
$$
 [L_{t_0}:R_0]_w+[L_{t_0}:R_0]_{\bar w}
   =v_w(G_{t_w,w}/G_{t_0,w})+v_w(r_{t_w}).                         \tag{2}
$$
In the original local identity the possible extra scalar in the row determinant factorization has zero valuation at the serving place, by its explicit hypothesis. Formula (2) retains this convention. The word-pairing comparison scalar of B8.08a is distinct from $r_{jt}$. Its unit property alone gives no estimate on $v_w(r_{jt})$. [Native unit hypothesis][native] · [Which scalar B8.08a compares][wordunit]

## Reading the relative determinants on single rational columns

Write $m_\alpha=\dim W_{j,\alpha}=\dim E_\alpha$ for the multiplicities. For a fixed rational basis of $KM_j$ set $A=h_{jt}(m,m)$ and $B=h_{j,t_0}(m,m)$. The relative characteristic polynomial $\det(XA-B)/\det A$ is monic, invariant under rational basis change, and has coefficients in $K^{\bar{}}$: transposing and applying bar fixes both Hermitian matrices and fixes the indeterminate. At $v_0$ the fixed target metric $g_j$ obeys $g_j(x,y)=\lambda_{jt\alpha v_0} h_{jt}(x,y)$ for $x$ in the block and all $y$. The same identity holds at $t_0$. These identities make $W_{j,\alpha}$ a relative eigenspace with eigenvalue $\lambda_{jt\alpha v_0}/\lambda_{j,t_0,\alpha,v_0}$. The blocks span the target. Thus
$$
  \sigma_0\!\left(\frac{\det(XA-B)}{\det A}\right)
  =\prod_\alpha\left(X-\frac{\lambda_{jt\alpha v_0}}
                                  {\lambda_{j,t_0,\alpha,v_0}}\right)^{m_\alpha},
  \qquad
  \sigma_0(r_{jt})=\prod_\alpha
      (\lambda_{jt\alpha v_0}/\lambda_{j,t_0,\alpha,v_0})^{m_\alpha}. \tag{3}
$$
If a block contains the image of a nonzero rational target vector $x_\alpha$, that same probe computes the individual ratio at every used $t$ as the image of the single element $h_{j,t_0}(x_\alpha,x_\alpha)/h_{jt}(x_\alpha,x_\alpha)$ in $K^{\bar{}}$. Positivity at $v_0$ makes the denominator nonzero. The rational-column result for a contributing reference block supplies such a vector after the rational reference map. Absent blocks carry exponent zero. Equation (3) needs only spanning and the metric identities, so the determinant remains available even before finding the individual probes. [Same target and all second arguments][data] · [Rational reference columns](continuation_v73/reading.tex#L61-L128)

## Reference mean and the remaining quantitative test

Set
$$
 A_0=D^{-1}\sum_{j,\alpha}m_\alpha
       \langle\log\lambda_{j,t_0,\alpha,v}\rangle_\infty,\qquad
 I_{\rm tw}=\prod_{w\in\mathrm{Tw}}\mathfrak p_w^{v_w(r_{t_w})},
 \qquad Q_{\rm fin}=D^{-1}\sum_w\ell_w v_w(G_{t_w,w}).
$$
The exponents of $I_{\rm tw}$ are signed. Let $P,H$ be the reference quotient matrix and its positive test Gram matrix in fixed rational bases, with $H$ in the coefficient subfield where all embeddings respect bar. Define $g=\det(PH^{-1}P^*)^{-1}$ algebraically. At an embedding $\sigma$, let $d_\sigma=\det(P_\sigma H_\sigma^{-1} P_\sigma^*)^{-1}$, now using the complex adjoint, and $\sigma'(a)=\overline{\sigma(\bar a)}$. Set
$$
 E_Q=\frac1{2[K:\mathbb Q]}\sum_\sigma
        \log\frac{|\sigma(g)|^2}{d_\sigma d_{\sigma'}}\ge0.
$$
Indeed $H_{\sigma'}=H_\sigma$. The complex image of $g^{-1}$ is the mixed Gram determinant of the row frames of $P_\sigma$ and $P_{\sigma'}$ for $H_\sigma^{-1}$. Cauchy–Schwarz on their exterior powers gives the inequality. Equality holds exactly when their row spaces agree at every embedding. The ratio defining $E_Q$ is unchanged under simultaneous induced basis changes. The product formula and the semilocal basis-change rule for the quotient Gram then give $\operatorname{lcv}(\Lambda_{t_0})=\sum_w\ell_wv_w(G_{t_0,w})-E_Q$ in the squared-norm convention. Explicitly, in global standard coordinates the archimedean determinant contributes $[K:\mathbb Q]^{-1}\sum_\sigma\log d_\sigma$, and the rational Gram contributes $[K:\mathbb Q]^{-1}\sum_\sigma\log|\sigma(g)|$. Their difference is $-E_Q$. Local determinant-line changes multiply the rational Gram by $\bar c c$ and give the same finite contribution to the lattice covolume after summing the conjugate places. This argument also applies to a projective lattice with no global integral basis. [Base quotient and product formula][global]

The reference metric on $L_{t_0}$ multiplies its log covolume by an additive $Dq_\kappa+D A_0$ relative to $\Lambda_{t_0}$, by the blockwise determinant identity. The squared-norm covolume of the glued lattice differs from that of $L_{t_0}$ by $2\sum_w\ell_w[L_{t_0}:R_0]_w$. Insert (2), use $\ell_w=\ell_{\bar w}$, and cancel the reference quotient Gram terms. This gives the exact expression
$$
 \mu(R_0^\vee)-q_\kappa
  = A_0+Q_{\rm fin}+\frac{\log N I_{\rm tw}}{D[K:\mathbb Q]}
       -\frac{E_Q}{D}.                                               \tag{4}
$$
All determinant-line expressions in (4) refer to the reference realization. Using this reference calculation to estimate the sharp mean requires a passage between levels. The next calculation works on the sharp level itself.

For the constructed quotient the known containment $|G|s\Lambda_t^\sharp\subseteq\Lambda_t$ gives $v_w(G_{t,w})/D\le v_w(|G|s)$ by the inverse Gram matrix. Hence $Q_{\rm fin}\le\log(|G|s)$, uniformly even though the type varies with $w$. For example, the following *single signed estimate* suffices for the reference premise of B5.08 if $\log(|G|s)=O(mL(B_0+N_c))$:
$$
 A_0+\frac{\log N I_{\rm tw}}{D[K:\mathbb Q]}-2F_*
   -\sum_{j,\rho}\beta_j w_{j\rho}\log\Omega
            \ \le\ C mL(B_0+N_c).                                  \tag{5}
$$
One can also retain $-E_Q/D$ if it helps. Algebraically, the finite term before division by $D$ is at most $h([1:(r_t^{-1})_t])$, the absolute projective logarithmic height. At each finite place the valued numerator $v_w(r_{t_w})$ is at most $\max(0,\max_t v_w(r_t))$, precisely the local contribution after weighting. The infinite contributions of the projective height in these coordinates are nonnegative. This bound has no extra factor for the number of places or layers but loses cancellations that (4) preserves. [Quotient denominator][den] · [Precise required error and passage][target]

## Direct computation on the sharp row

Let $i$ denote either row level, $i=0$ for reference and $i=1$ for sharp. Use its own rational quotient maps $P_{i,t}$, row identifications $\iota_{i,t}$, quotient lattices $\Lambda_{i,t}$, common target $E_i$ and dimension $D_i>0$. The sharp row identifications are also isomorphisms, and its glued row $R_1=R_{\mathrm c}$ uses these quotient lattices at the same serving places. Define the algebraic quotient form at the distinguished place by $H^Q_{i,t}=(P_{i,t} H_{V,i,t}^{-1}P_{i,t}^*)^{-1}$. Positivity and surjectivity at $v_0$ give invertibility over $K$. Transport it to $E_i$ with $\iota_{i,t}$ and call its matrix $S_{i,t}$ in any common rational target basis. Put $s_{i,t}=\det S_{i,t_0}/\det S_{i,t}$. At $w$, write $C_t$ for the columns of an image of a semilocal quotient-lattice basis in this rational basis. Then
$$
 G_{i,t,w}=\overline{\det C_t}\det C_t\det S_{i,t}.
$$
The signed local image index for $L_{i,t_0},L_{i,t}$ is $v_w(\det C_t/\det C_{t_0})$. Thus the paired index equals $v_w(G_{i,t,w}/G_{i,t_0,w})+v_w(s_{i,t})$ directly at either level. This step does not use a layer map or a comparison between levels. [Sharp quotient, row isomorphisms and gluing][sharp]

With $m_{i,\alpha}=\dim E_{i,\alpha}$, put
$$
 A_i=D_i^{-1}\sum_{j,\alpha}m_{i,\alpha}
     \langle\log\lambda_{j,t_0,\alpha,v}\rangle_\infty,
 \quad I_i=\prod_{w\in\mathrm{Tw}}\mathfrak p_w^{v_w(s_{i,t_w})},
 \quad Q_i=D_i^{-1}\sum_w\ell_w v_w(G_{i,t_w,w}).
$$
Form $E_{Q,i}$ from the level's own base quotient. Its proof and sign above apply at this level. The base metric of $E_i$ relative to its definite quotient scales by $\kappa_v\prod_j\lambda_{j,t_0,\alpha,v}$ on each block. Applying this base identity, the paired index calculation, and the product formula gives exactly
$$
 \mu(R_i^\vee)-q_\kappa=A_i+Q_i+
           \frac{\log NI_i}{D_i[K:\mathbb Q]}-E_{Q,i}/D_i.          \tag{6}
$$
At $v_0$ the row metric identities likewise give $\sigma_0(s_{i,t})=\prod_{j,\alpha}(\lambda_{jt\alpha v_0}/\lambda_{j,t_0,\alpha,v_0})^{m_{i,\alpha}}$ in the shared-$\kappa$ conventions. An extra tuple normalization in the native determinant identity contributes its $D_i$th power, with zero valuation at its serving place when it is a served unit. The directly defined $s_{i,t}$ in (6) needs no normalization convention. For a block with a rational probe let $r_{jt,\alpha}$ denote its individual algebraic ratio in (3). If all contributing blocks have such probes and the common factor is a served unit, the first and third terms of (6) together equal the weighted average with weights $m_{i,\alpha}/D_i$ of
$$
 b_\alpha=\sum_j\langle\log\lambda_{j,t_0,\alpha,v}\rangle_\infty+
               \sum_{w\in\mathrm{Tw}}\ell_w v_w\!\left(\prod_jr_{j,t_w,\alpha}\right).
$$
This gives the exact level-specific multiplicities in place of an error for passage between them. It also permits computing $I_1$ directly from rational quotient matrices without determining any individual scalar. With the exact $Q_1-E_{Q,1}/D_1$ term retained, the bound
$$
 A_1+Q_1+\frac{\log NI_1}{D_1[K:\mathbb Q]}-E_{Q,1}/D_1
 \le \sum_{j,\rho}\beta_j w_{j\rho}\log\Omega+2F_*+C mL(B_0+N_c)   \tag{7}
$$
suffices for the sharp slope premise of the kernel-factorial calculation in B5.08 with passage cost zero. Indeed insert its left side as $\widetilde\mu_C$ by (6) and use the right side as the allowable intermediate bound. The same word estimates and base-term identification then yield entry 7. [Sharp arithmetic target][arithmetic] · [Word cancellation][target]

The finite ideal can also be computed in the fixed field $F=K^{\bar{}}$. Each $s_{i,t}$ is a ratio of determinants of Hermitian forms and lies in $F^\times$. The common tuple $t_w=t_{\bar w}$ descends to $t_{\mathfrak v}$ at each prime $\mathfrak v$ of $F$. Thus $I_i=J_i\mathcal O_K$ with $J_i=\prod_{\mathfrak v:t_{\mathfrak v}\ne t_0}\mathfrak v^{v_{\mathfrak v}(s_{i,t_{\mathfrak v}})}$. Indeed $v_w(s_{i,t_w})=e(w/\mathfrak v)v_{\mathfrak v}(s_{i,t_{\mathfrak v}})$ at every prime, including ramified ones. It follows that $\log N_K I_i/[K:\mathbb Q]=\log N_F J_i/[F:\mathbb Q]$. The one-prime example below shows why this descent and finite support still leave the size of the selected ideal to be bounded.

The [reference section calculation](PERIOD_REFERENCE_MAP_HEIGHT.md#the-same-gram-determinant-in-entries-6-and-7) identifies $E_{Q,1}$ as half the averaged log determinant of the sharp reference section in its local quotient metrics. It supplies an explicit test for its vanishing in terms of maximal minors.

### The Gram bound at the actual sharp level

For the constructed definite row at *every* tuple, the original row-block theorem gives the good class data at denominator $s=1$. The additional inert Hecke operators leave this class datum unchanged. Indeed the row coefficients use the standard Hermitian form and the two Weyl lattices on the decorated class lattice $N$. This $N$ is unimodular, including at the twisted tuples. Each star-compatible coefficient embedding preserves its Hermitian self-duality and the tensor Weyl duality exchanges the two coefficient lattices. Hence $A_c^\sharp=\Delta_c$ integrally. These are exactly the two coefficient containments entering the class datum with $s=1$. The original construction gives the same conclusion simultaneously on the layer blocks. This use of an explicit admissible denominator leaves the previously chosen lattices, maps and tuple selector fixed. [Construction on every tuple][allrows] · [Inert operators on the same row][three] · [Class lattices][coeff] · [Unimodularity][unim] · [Weyl and frame duality][dual]

For an arbitrary subgroup character level, the original test-lattice calculation gives $|G|s\,M_{i,t}^\sharp\subseteq M_{i,t}$ in its normalized form. In particular the reciprocal subgroup order $1/|P_i|$ is already in the Gram matrix on the retained test space. The orthogonal section of the quotient takes a vector of $\Lambda_{i,t}^\sharp$ into the test dual because pairing it against a test vector is pairing against the projected test vector. Projection of its $|G|$-multiple gives
$$
 |G|\,\Lambda_{i,t}^\sharp\subseteq\Lambda_{i,t},\qquad
 v_w(G_{i,t,w})/D_i\le v_w(|G|),\qquad
 Q_i\le\log |G|\le 2mL(B_0+N_c).                                   \tag{8}
$$
The middle inequality follows by taking the determinant of the integral matrix $|G|$ times the inverse semilocal Gram. The last bound is the native group-order estimate on the selected size data and the identification of the row group; it applies when $s=1$, uniformly over the tuples. Thus the quotient-Gram contribution to (7) is controlled at the required scale on the constructed sharp row. Its remaining sufficient condition is (5) with $A_1,D_1,I_1$ and the sharp multiplicities. It is possible to retain the nonpositive Gram defect when testing this sharper version. [Test dual and quotient][testdual] · [Metric normalization][levelnorm] · [Group order at denominator one][onebudget]

Uniform boundedness of the positive real ratios alone does not bound these selected valuations. For example take $K=\mathbb Q(i)$, one one-dimensional target, identity source forms, target metric one, and the integral maps $\theta_{t_0}=p^n+1$, $\theta_t=p^n$ for a fixed rational prime $p$. The relative scalar is $(p^n/(p^n+1))^2$, lying between $1/4$ and $1$ at both complex embeddings, whereas its valuation at any $w$ above $p$ is $2ne_w$. This tests the inference from an archimedean ratio alone. The Rallis inner product theorem can give analytic formulas for the lift norms after identifying vectors, measures and local data, but that formula alone does not establish (5). The original geometric covolume and two-run cut estimates remain a separate sufficient route to the same reference bound. The quantitative step still needed is a uniform estimate on the actual family, either (7) directly or a reference estimate such as (5) together with a justified passage to the sharp level. [Rallis formula](https://arxiv.org/abs/1207.4709) · [Original two-run route][global]

[data]: https://github.com/rh-lean-roadmap/rh-lean-roadmap/blob/02a95b4c62db610642af5f278ee5d0d6df87b348/docs/src/book/main.tex#L8223-L8275
[local]: https://github.com/rh-lean-roadmap/rh-lean-roadmap/blob/02a95b4c62db610642af5f278ee5d0d6df87b348/docs/src/book/main.tex#L9103-L9121
[native]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Formalism/QuotientMetricDivisors/HermitianTwistDivisors/ConjugateWeightLatticeOfGeneral.lean#L174-L229
[wordunit]: https://github.com/rh-lean-roadmap/rh-lean-roadmap/blob/02a95b4c62db610642af5f278ee5d0d6df87b348/docs/src/book/main.tex#L16447-L16458
[global]: https://github.com/rh-lean-roadmap/rh-lean-roadmap/blob/02a95b4c62db610642af5f278ee5d0d6df87b348/docs/src/book/main.tex#L32935-L32973
[sharp]: https://github.com/rh-lean-roadmap/rh-lean-roadmap/blob/02a95b4c62db610642af5f278ee5d0d6df87b348/docs/src/book/main.tex#L8286-L8330
[arithmetic]: https://github.com/rh-lean-roadmap/rh-lean-roadmap/blob/02a95b4c62db610642af5f278ee5d0d6df87b348/docs/src/book/main.tex#L8452-L8488
[den]: https://github.com/rh-lean-roadmap/rh-lean-roadmap/blob/02a95b4c62db610642af5f278ee5d0d6df87b348/docs/src/book/main.tex#L8427-L8449
[target]: https://github.com/rh-lean-roadmap/rh-lean-roadmap/blob/02a95b4c62db610642af5f278ee5d0d6df87b348/docs/src/book/main.tex#L9082-L9100

[allrows]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Formalism/LocalToGlobal/Divisibility/DivisionHeightBoundColumns.lean#L202-L239
[three]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Formalism/LocalToGlobal/Divisibility/HeckeCSDICommTrRep.lean#L130-L173
[coeff]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Formalism/LocalToGlobal/Columns/CoefCol.lean#L59-L103
[unim]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Formalism/LocalToGlobal/Columns/StdLatUnimodular.lean#L81-L99
[dual]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Formalism/LocalToGlobal/Columns/CoefficientsModP.lean#L25-L35
[testdual]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Formalism/LocalToGlobal/Divisibility/RowLatLemmas.lean#L22-L74
[levelnorm]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Formalism/LocalToGlobal/Divisibility/GoodPartHermitianSpec.lean#L134-L145
[onebudget]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Formalism/LocalToGlobal/Divisibility/DivisibilityConstruction/RBLam.lean#L116-L135
