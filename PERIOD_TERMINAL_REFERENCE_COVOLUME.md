# The terminal reference covolume in the seventh period entry

In [the signed level formula](PERIOD_SIGNED_LEVEL_TRANSFER.md), the last reference covolume has a definite, zero-dimensional calculation. The reduction below retains its signed main term and saves the factor $\log\log x$ in the terminal error. It needs only the indicated *terminal* comparisons. It does not require small-section estimates on any positive-dimensional compactification. The remaining layers $1\le j<m$ and the sum of served indices are separate obligations.

Throughout, $D=D_0>0$, $r=k+m-1$, $L=x^\varepsilon$, $b=e^L$, $B_0=fmbL$, and $T_m=r\log\Omega\sum_\rho w_{m,\rho}$. Write $\mu$ for the squared-norm slope, twice the ordinary normalized Arakelov slope $\widehat\mu$.

## The determinant before deleting bad types

Use the marked definite component system split over a coefficient extension as in the terminal case of B8.29, its integral CM eigenbundles and theta line, and the probability Petersson measure over components. Extension of the coefficient field preserves normalized degrees of extended lattices. At a component $Z$, put
$$
 V_Z=\mathcal L_{\theta,Z}^{n_{\rm col}}\otimes
       \bigotimes_\tau W_{\nu_\tau}(\omega_{\tau,Z}),\qquad
 \nu_{\tau,i}=\lambda_{\tau,i}-n_{\rm col}/2,\quad
 d_\tau=\dim W_{\nu_\tau}.
$$
Here $|\nu|=\sum_i\nu_i$ is the signed central exponent. The functor $W$ is the integral dual Weyl module, with determinant twists for negative entries, and $\omega_{\tau,Z}$ has rank $r$. If $G_{\nu}$ is the Gram matrix of the integral standard-monomial basis on the standard Hermitian $r$-space in the source's Schur metric, the determinant functor gives the exact identity
$$
 2\widehat\mu(V_Z)=2n_{\rm col}\widehat{\deg}\mathcal L_{\theta,Z}
 +\sum_\tau\left(\frac{2|\nu_\tau|}{r}\widehat{\deg}\det\omega_{\tau,Z}
          -\frac{1}{d_\tau}\log\det G_{\nu_\tau}\right).       \tag{1}
$$
Indeed the determinant character of an irreducible algebraic representation of $\mathrm{GL}_r$ has exponent $|\nu|d_\nu/r$ by restriction to the center. This computes both the finite transition determinants and the change of archimedean frame. The remaining universal Gram determinant is evaluated in the standard frame. Tensor products distribute these terms with multiplicities equal to complementary dimensions, which disappear upon dividing by the fibre rank. In the stated Schur metric each standard monomial is a product of flag minors of absolute value at most one on the unitary group, multiplied in squared norm by the normalization $d_\nu$. Hadamard gives $\log\det G_\nu\le d_\nu\log d_\nu$. A determinant twist has modulus one on the unitary group. These identities require no free global basis of the eigenlattices.

Insert the terminal CM comparisons
$$
 \widehat{\deg}\det\omega_{\tau,Z}=-\tfrac r2\log\Omega,\qquad
 \widehat{\deg}\mathcal L_{\theta,Z}\ge
 \tfrac12\sum_\tau\widehat{\deg}\det\omega_{\tau,Z}
   +fr(\tfrac14\log(2\pi)-\tfrac12\log\operatorname{rd}E).
$$
The second comparison accounts for the finite different in the eighth-power theta key. The result is
$$
 2\widehat\mu(V_Z)\ge
 -\log\Omega\sum_{\tau,i}\lambda_{\tau,i}-\sum_\tau\log d_\tau
 +n_{\rm col}fr(\tfrac12\log(2\pi)-\log\operatorname{rd}E).
$$
The original weight bounds are $r|a_\tau-w_{m,\rho(\tau)}|\le20b$, $\sum_i|\lambda_{\tau,i}-a_\tau|\le10mb$, and $|\log\Omega|\le3L$. Therefore the signed term on the right is at least $-T_m-30B_0-60fbL$. The Weyl formula and the original size bounds give $\sum_\tau\log d_\tau\le3fb$ and $n_{\rm col}fr\log\operatorname{rd}E\le2b$. Since $m\ge2$ and $L\ge10$, it follows that
$$
                    2\widehat\mu(V_Z)\ge -T_m-61 B_0 .           \tag{2}
$$
This calculation retains the full central character and its sign.

Let $P$ be the marked type-character subgroup acting freely, write $N$ for the number of its orbits, and take one fibre per orbit. The integral orbit-sum map of B8.29 has full rank. Its Petersson squared norm is exactly $N^{-1}\sum_o\|v_o\|^2$, since the character values have modulus one. Thus the squared slope in the probability metric is at least the *average* of (1) over orbits plus $\log N$, even if the orbit-sum image only has finite index in the integral lattice. In particular it is at least $-T_m-61 B_0+\log N$. Only type-subgroup freeness enters here. For the realized metric put $C_2=\max_\sigma|\log c_\sigma^2|$, where $c_\sigma$ rescales ordinary Petersson norms. On the source's row volume and Weyl-dimension comparisons before their final coarsening,
$$
 C_2=O(fr^2(L+\log(fr+3)+1)+\log|\operatorname{disc} E|)=O(x^A)=o(b).
$$
In particular the realized character-lattice slope satisfies $\mu(L_\chi)\ge h:=-T_m-61B_0+\log N-C_2$.

## Exact cost of the good projection

Write $e$ for the good orthogonal idempotent, $L_g=L_\chi\cap\operatorname{im}e$, $L_b=L_\chi\cap\ker e$, $d_g,d_b$ for their ranks, and $Q=L_\chi/(L_g\oplus L_b)$. For realization field $K$,
$$
 \mu(L_g)=\frac{d_g+d_b}{d_g}\mu(L_\chi)
       -\frac{d_b}{d_g}\mu(L_b)-\frac{2\log|Q|}{[K:\mathbb Q]d_g}. \tag{3}
$$
The bad term is taken as zero when $d_b=0$. This is the finite-index determinant identity, with the archimedean splitting orthogonal at each embedding. If $g=|G|$ clears $e$, then $1-e$ embeds $Q$ into $g^{-1}L_b/L_b$. Thus the last term has size at most $2(d_b/d_g)\log g$.

The terminal rank computation uses the free action on marked components of each subgroup $H_a$ unrestricted at the one chosen local prime and unipotent at the other. On each such free orbit the component space is a sum of regular representations. Taking the trace of the product of the type and bad projectors gives the local bad share $u_a$ times the character rank, by its identity coefficient. The union bound for the commuting projectors gives $d_b/(d_g+d_b)\le u_0+u_1\le\delta$, with $\delta=e^{-x^{\varepsilon/(7J)}}$ at the project threshold. This argument requires only the indicated subgroup actions.

For the cut one only needs an upper bound on $\mu(L_b)$ when $d_b>0$, or directly a bound on its weighted excess in (3). The component tests below prove $\mu(L_b)\le\log N+O(x^{A'}b)$ directly on the terminal CM data. Alternatively, the source supplies the coarser sufficient input $\mu_{\max}(\Lambda_{\rm all})\le x^{A'}b$ on its hypotheses. Since $|T_m|,B_0,2\log g\le x^{A''}b$ eventually, the loss beyond the lower bound $h$ in (3) is at most $C\delta x^{A'''}b=o(b/x^n)$ for every fixed $n$. Finally the primitive row comparison (8.32a) gives $\operatorname{lcv}(M_m)/D\le-\mu(L_g)$. Consequently, under the terminal CM data, realized measure and finite-group comparisons detailed here,
$$
 \boxed{\displaystyle \frac{\operatorname{lcv}(M_m)}{D}
     \le T_m+61B_0-\log N+o(b).}                                 \tag{4}
$$
For the original signed level formula (5) the terminal excess can therefore be budgeted by $62B_0$ eventually. One may discard $-\log N$. This removes the final absolute layer from the sufficient inequality *conditional on the identified terminal inputs*, leaving $m-1$ positive-dimensional absolute layers and the served index sum (including its terminal indices). The numerical constant concerns only the terminal absolute summand.

## Direct bound on the discarded sublattice from definite CM evaluations

For the original *definite* polarized component fibres the upper slope used in (3) can itself be proved, without an ambient cusp-form estimate. Retain the integral component-evaluation and realized-metric identifications above, the rank-one polarized host of the same CM type and its CM line-degree formula, and the two-sided finite orders of the theta key in B8.24a. On these pointwise CM inputs every sublattice $S\subseteq L_\chi$ satisfies
$$
                 \mu(S)\le \log N+O(x^A b) .                       \tag{5}
$$
All constants below are uniform in the component. The estimate is enough even if the number of components is very large.

**Integral maps of controlled norm.** Fix a component abelian variety $A$ and take the principally polarized rank-one $\mathcal O_E$-CM host $A_*$ of its CM type. The [rank-one period lattice](https://github.com/rh-lean-roadmap/rh-lean-roadmap/blob/02a95b4c62db610642af5f278ee5d0d6df87b348/docs/src/book/main.tex#L7200-L7217) gives this host. Let $I=H_1(A_*,\mathbb Z)$ and $J=H_1(A,\mathbb Z)$, projective $\mathcal O_E$-modules of ranks one and $r$. Every $E$-linear rational map of the underlying vector spaces respects the Hodge complex structures, since on each $E$-embedding the structures are the same scalar at signature $(r,0)$. A map preserving period lattices thus induces a holomorphic homomorphism of the complex abelian varieties, hence an algebraic homomorphism. Therefore
$$
 U=\operatorname{Hom}_{\mathcal O_E}(A_*,A)=\operatorname{Hom}_{\mathcal O_E}(I,J),\qquad
 U^*=\operatorname{Hom}_{\mathcal O_E}(A,A_*) .
$$
The second equality is via composition, since $I$ is invertible, $I\otimes U=J$, and $\operatorname{End}_{\mathcal O_E}(I)=\mathcal O_E$. Both polarizations are principal and their Rosati involutions on $E$ are conjugation, so adjunction gives a bijection $U\to U^*$. The positive definite Hermitian lattice $H(v,w)=v^\dagger w$ is consequently self-dual. This argument also covers nonfree ideal classes.

For its trace Euclidean norm the dual lattice is $\mathfrak D_E^{-1}U$. The [trace-lattice transference bound and its host estimate](https://github.com/rh-lean-roadmap/rh-lean-roadmap/blob/02a95b4c62db610642af5f278ee5d0d6df87b348/docs/src/book/main.tex#L49698-L49703) produce $E$-independent $v_1,\ldots,v_r\in U$ with $0<\tau H(v_i,v_i)\le B=4f^3r^4\operatorname{rd}(E)^2$ at every embedding. Indeed for a nonzero element of the dual the codifferent norm and AM–GM give squared trace norm at least $2f/\operatorname{rd}(E)^2$. Apply $\lambda_{2fr}(U)\lambda_1(U^*)\le2fr$ to the *Euclidean* polar lattice and extract an $E$-basis of short elements. The $2fr$ independent vectors span the full rational space, hence also span it over $E$. Retaining a vector whenever it lies outside the previous $E$-span gives $r$ independent short maps. The two meanings of dual here are distinguished by the codifferent. [Banaszczyk, 1993](https://doi.org/10.1007/BF01445125)

Take a finite field extension on which the finitely many maps needed for all components are defined and on which the CM varieties have good reduction. Good reduction is potential for the rank-one CM host and for its isogenous powers. The abelian schemes extend the maps over every finite valuation ring by the Néron property. Differentiating and dualizing the saturated integral Lie eigenspaces gives an integral, generically injective map
$$
       F_\tau:\omega_{\tau,Z}\longrightarrow H_{\tau,*}^{\oplus r},
       \qquad H_{\tau,*}=(\operatorname{Lie}_\tau A_*)^\vee .
$$
Indeed $A_*^r\to A$ is an isogeny because the chosen elements span $U_E$. The adjoint identity for polarized Hodge metrics gives $\|d v_i\|_\sigma^2=\tau_\sigma H(v_i,v_i)\le B$ at the corresponding conjugate embedding, hence $\|F_\tau\|_\sigma\le\sqrt{rB}$. The scalar changes shared by the polarized Lie metrics on source and target cancel. Conjugating the algebraic maps conjugates the identity $v_i^\dagger v_i=H(v_i,v_i)$, so at an embedding not fixing the original base the conjugate source and target still have the same type, and the right side is another embedding of the same totally positive algebraic integer. In the final row the separate scaling $c_\sigma$ is retained in $C_2$. The [rank-one CM degree](https://github.com/rh-lean-roadmap/rh-lean-roadmap/blob/02a95b4c62db610642af5f278ee5d0d6df87b348/docs/src/book/main.tex#L32794-L32810) gives $\widehat{\deg}H_{\tau,*}=-\tfrac12\log\Omega$ in the chosen normalization. [Serre–Tate](https://annals.math.princeton.edu/1968/88-3/p05)

**Schur coefficient tests.** Put $t_\tau=\nu_{\tau,r}$, $\alpha_\tau=\nu_\tau-t_\tau\mathbf1$ and $s_\tau=|\alpha_\tau|\ge0$. Factor the possibly negative determinant power $(\det\omega_{\tau,Z})^{t_\tau}$ off the polynomial dual Weyl representation. In the standard bideterminant model for $W_\alpha(\mathcal O^r)$, coefficients in the ordinary matrix-entry monomials of the polynomial are integral linear functionals. They jointly separate the generic fibre. Each such functional has operator norm at most $r^s$, where $s=|\alpha|$. To see this, evaluation on a unitary matrix has norm one for the source metric $d_\alpha\int_{U(r)}|p|^2$. The squared norm of evaluation is constant on $U(r)$ by invariance, and integration of the sum over an orthonormal basis gives $d_\alpha/d_\alpha=1$. By singular-value decomposition and the maximum modulus theorem in each diagonal singular-value variable, $|p(T)|\le\sup_{U(r)}|p|$ for every contraction $T$. Matrices with entries of absolute value at most $1/r$ are contractions. The coefficient estimate follows from multivariable Cauchy on this polydisc and homogeneity. Also $\|W_\alpha(F)\|\le\|F\|^s$ by singular-value decomposition and the nonnegative torus weights of total degree $s$.

Combining $F_\tau$ and these coefficients, the tensor products of integral tests on $V_Z$ take values in the same arithmetic line for that component,
$$
  T_Z=\mathcal L_{\theta,Z}^{n_{\rm col}}\otimes
       \bigotimes_\tau (\det\omega_{\tau,Z})^{t_\tau} H_{\tau,*}^{s_\tau}.
$$
They separate its vectors and individually have norm at most $A_0=(r\sqrt{rB})^{\sum_\tau s_\tau}$. The theta-key comparison in B8.24a has finite orders between 0 and $4B(w)$ and constant complex norm $(2\pi)^{2fr}$. Applied in both directions to the degree formula, this gives
$$
 \left|\widehat{\deg}\mathcal L_{\theta,Z}
    -\tfrac12\sum_\tau\widehat{\deg}\det\omega_{\tau,Z}\right|
 \le fr(\tfrac14\log(2\pi)+\tfrac12\log\operatorname{rd}E).
$$
The same terminal pointwise orders already give (2). For the signed determinant twists, $|t_\tau|\le4b+10mb+n_{\rm col}/2$, $s_\tau\le20rmb$, and $|\widehat{\deg}\det\omega_{\tau,Z}|\le 3rL/2$, so negative exponents are included by absolute value in the line degree. The rank-one and determinant degree formulas and the polynomial size of $f,r,n_{\rm col}$ now give $\max_Z|\widehat{\deg}T_Z|+\log A_0=O(x^A b)$. In particular no isogeny degree raised to the representation dimension appears. [Bounds for both orders of the key](https://github.com/rh-lean-roadmap/rh-lean-roadmap/blob/02a95b4c62db610642af5f278ee5d0d6df87b348/docs/src/book/main.tex#L49117-L49119)

Compose tests with evaluation on the representative components. This evaluation is integral, including after extending scalars, by the component integral-frame reading. Since the character permutes the other marked components by isometries, any fixed representative has evaluation norm at most $\sqrt N$ in the probability Petersson norm. The tests therefore have realized norm at most $A_0\sqrt N e^{C_2/2}$. Restricted to any rank-$d>0$ sublattice $S$, choose $d$ tests linearly independent on its generic fibre. Their determinant is a nonzero integral map from $\det S$ to a tensor product of $d$ of the lines $T_Z$. Hadamard bounds its norm by $(A_0\sqrt N e^{C_2/2})^d$. Taking normalized degrees yields
$$
 \mu(S)\le 2\max_Z\widehat{\deg}T_Z+2\log A_0+\log N+C_2 .
$$
Degrees descend through the auxiliary extension by normalization. This proves (5), independently of B8.25d's ambient maximum-slope estimate and of any upper bound on the number of components. In (3) the excess $\mu(L_b)-h+2\log g$ is thus $O(x^{A'}b)$, since the two $\log N$ terms cancel. Hence (4) follows on the terminal polarized CM, integral section, realized metric and finite projector comparisons already specified, with no additional coarse bad-slope hypothesis.

The geometric identification used here takes the actual terminal fibre of the marked moduli problem with its principal polarization and integral eigenspaces. These are the [universal principal PEL comparison](https://github.com/rh-lean-roadmap/rh-lean-roadmap/blob/02a95b4c62db610642af5f278ee5d0d6df87b348/docs/src/book/main.tex#L19748-L19760) and the [evaluation, local bases, and Gram matrices of the terminal fibre](https://github.com/rh-lean-roadmap/rh-lean-roadmap/blob/02a95b4c62db610642af5f278ee5d0d6df87b348/docs/src/book/main.tex#L53820-L53830). The rank-one polarization is principal by the [self-duality of its period lattice](https://github.com/rh-lean-roadmap/rh-lean-roadmap/blob/02a95b4c62db610642af5f278ee5d0d6df87b348/docs/src/book/main.tex#L30917-L30921). Its type is the [one induced from the distinguished imaginary quadratic field](https://github.com/rh-lean-roadmap/rh-lean-roadmap/blob/02a95b4c62db610642af5f278ee5d0d6df87b348/docs/src/book/main.tex#L47930-L47934). The [marked-stage signature and its conjugate embeddings](PEL_STAGE_PARAMETERS.md) match this type at the terminal stage. The argument with integral homology uses the whole period lattices of these two abelian varieties. It requires no identification of those period lattices with free modules or with a chosen arithmetic basis. Identifying the original row lattice with the integral geometric section lattice remains an explicit comparison in this result.

### Recovering the terminal determinant degrees from the single rank-one CM host

There is also a direct verification of the first CM identity in (2), independent of the flat-degree law at other signatures. For the module $U$ above the evaluation $U\otimes_{\mathcal O_E} I\longrightarrow J$ is an isomorphism of **integral** period lattices. Indeed $I$ is an invertible fractional ideal and $U=\operatorname{Hom}(I,J)=I^{-1}J$. To construct the corresponding abelian variety, choose a projective presentation $U=e\mathcal O_E^h$ for an idempotent matrix $e$. Its image on $A_*^h$ is a direct factor, complementary to the image of $1-e$. The evaluation map of abelian varieties from this factor to $A$ induces exactly the integral period isomorphism above and is therefore an isomorphism. Over a common good-reduction extension the evaluation and its inverse extend by the Néron property; their extensions are inverses by uniqueness. This uses no assertion about a short isogeny preserving integral differentials.

Write $T_{\tau,*}$ for the saturated integral Lie eigenspace of $A_*$ and $\mathcal O'$ for a coefficient valuation ring containing all embedding values. Taking eigenspaces in $e\,\operatorname{Lie}(A_*^h)$ gives exactly
$$
 \operatorname{Lie}_\tau A
  \simeq (U\otimes_{\mathcal O_E,\tau}\mathcal O')\otimes_{\mathcal O'}T_{\tau,*}.
$$
Indeed $e$ commutes with the $\mathcal O_E$ action. An integral vector in its image satisfying the eigenrelations is already an integral eigenvector in the ambient direct sum and equals its own image under $e$. In that eigenspace $e$ acts by $\tau(e)$. This remains valid at primes dividing the discriminant. At each complex embedding the induced metric is the tensor of the rank-one polarized metric and the positive form given by the corresponding embedding of $H$. This follows by evaluating the polarized Gram pairings on the maps, since $v^\dagger w=H(v,w)$.

To compute the multiplicity determinant degree, choose an integral $E$-basis $v_i$ of the vector space, set $U_0=\sum_i\mathcal O_Ev_i\subset U$ and $\mathfrak n=\operatorname{Fitt}_0(U/U_0)$. For $g=(H(v_i,v_j))$, self-duality gives $(\det g)=\mathfrak n\bar{\mathfrak n}$, by the determinant pairing on $\det U$ or by localization. Consequently the normalized finite log index of $\tau(U_0)$ in $\tau(U)$ after extending to $K'$ equals $\log N_{E/\mathbb Q}\mathfrak n/[E:\mathbb Q]$. The conjugates on the infinite side average to
$$
 \frac1{2[K':\mathbb Q]}\sum_{\sigma:K'\hookrightarrow\mathbb C}
        \log|(\sigma\circ\tau)(\det g)|
  =\frac{\log|N_{E/\mathbb Q}\det g|}{2[E:\mathbb Q]}
  =\frac{\log N_{E/\mathbb Q}\mathfrak n}{[E:\mathbb Q]} .
$$
Each embedding of $E$ above the chosen label occurs with the same multiplicity $[K':E]$ when counted through $\sigma\circ\tau$. The two determinant terms have opposite signs in the normalized degree, so the multiplicity space has determinant of degree zero. Dualization now gives $\widehat{\deg}\det\omega_{\tau,Z}=r\,\widehat{\deg}H_{\tau,*}=-r\log\Omega/2$ for every original definite component in the specified metric.

Only a pointwise theta estimate is needed on these good abelian fibres. The [normalized theta-key statement on abelian schemes](https://andrewodesky.com/rh/lean/GlobalTheory.KeyFam.keyFormula_holds/) specifies a unit over every good DVR in a full Lie basis and the exact archimedean metric transformation. A coarser sufficient comparison can even avoid the sharp different-ideal length in B8.24a. Write $T=\operatorname{Lie} A$ and $T_\#=\bigoplus_\tau T_\tau\subset T$. If $\Delta=|\operatorname{disc}E|$, the primitive idempotent $e_\tau$ projecting the rational Lie algebra onto the $\tau$-part has $\Delta e_\tau$ integral: in a trace basis it is $\sum_i \tau(b_i^*)b_i$, with $\Delta b_i^*\in\mathcal O_E$. Thus $\Delta T\subseteq T_\#\subseteq T$. The normalized determinant defect is between zero and $fr\log\Delta$. The eigenspaces are orthogonal at infinity, and the theta key transforms to the fourth power of this determinant times a unit. It follows that
$$
 \left|\widehat{\deg}\mathcal L_{\theta,Z}
    -\tfrac12\sum_\tau\widehat{\deg}\det\omega_{\tau,Z}\right|
 \le \tfrac{fr}{4}\log(2\pi)+\tfrac{fr}{2}\log\Delta .
$$
Its contribution after multiplying by $2n_{\rm col}$ is polynomial in $x$, hence $o(b)$, and is absorbed in (4). This proves the needed theta comparison from the key on ordinary abelian schemes without a boundary extension or the sharp placewise different formula. The algebraic existence and metric normalization of this abelian theta key are inputs. Bost’s arithmetic key formula also relates the dual theta section line to the stable Faltings height; its stated metric constants depend on the Faltings convention. [de Jong–Shokrieh, §13.4, Theorem 13.1](https://doi.org/10.1112/S0010437X21007661)

The terminal degree also follows directly from a published arithmetic theorem, bypassing the normalized theta scalar. Normalize degrees by the field degree. On the common good-reduction model $\pi:\mathcal A\to\operatorname{Spec}\mathcal O_{K'}$, the given symmetric rigidified line $\mathcal L$ extends cubically, its polarization is principal, and $\ker\lambda_{\mathcal L^{\otimes2}}=\mathcal A[2]$ is finite flat, including above 2. This is a Moret-Bailly model. In the marked component reading $\mathcal L_{\theta,Z}=(\pi_*\mathcal L)^\vee$: its local lattice is the dual of the integral theta-generator line and the squared norm of the inverse generator is $N_\theta^{-1}$. The theta norm $N_\theta$ in the marked frame is precisely the Haar-probability $L^2$ norm squared with the rigidified, translation-invariant curvature metric used in de Jong–Shokrieh (12.2). In the complex torus trivialization the pointwise metric is $|\vartheta(z)|^2e^{-\pi H(z,z)}$; it has the required curvature and rigidification. For a full Lie basis with row matrix $W$, the de Jong–Shokrieh squared Faltings norm (12.1) of its dual top form is $\operatorname{vol}(D)/|\det W|^2$. The squared norm of this form in the project's full cotangent convention is $N_\eta=\operatorname{vol}(D)/(\pi^g|\det W|^2)$, with $g=fr$. Thus
$$
 h_F(A)=\widehat{\deg}_{\rm proj}\det\omega_{\rm full}-\tfrac g2\log\pi.
$$
By their Theorem 13.1,
$$
 \widehat{\deg}\mathcal L_{\theta,Z}
   =\tfrac12 h_F(A)+\tfrac g2\log(\pi\sqrt2)
   =\tfrac12\widehat{\deg}_{\rm proj}\det\omega_{\rm full}
        +\tfrac g4\log(2\pi).
$$
The term $\log(2\pi)$ therefore has the required sign and multiplicity. Passing to the saturated eigenbases changes the full cotangent degree by at most $g\log\Delta$ as just proved. This gives the estimate used in (4) from the ordinary integral theta-generator and metric identifications alone. No degenerating family is involved at this terminal point. [de Jong–Shokrieh, equations (12.1)–(12.2) and Theorem 13.1](https://doi.org/10.1112/S0010437X21007661) · [Marked norms and transformation rule](https://andrewodesky.com/rh/lean/GlobalTheory.KeyFam.keyFormula_holds/) · [Terminal inverse generator](https://github.com/rh-lean-roadmap/rh-lean-roadmap/blob/02a95b4c62db610642af5f278ee5d0d6df87b348/docs/src/book/main.tex#L53825-L53828)

## Scope and sources

The [semiabelian valuation transfer](PEL_SEMIABELIAN_SECTION_TRANSFER.md) handles simultaneous integral tests. A common rescaling of the archimedean norms by $e^t$ changes a normalized squared log covolume by $2t$ while preserving every recovered valuation, so that transfer alone cannot imply (4). On the identified terminal fibre the calculation requires the rank-one host period, the integral component and projector comparisons, and the realized metric. The ordinary theta-line degree formula above and the integral coefficient tests give both the requisite degree comparison and the upper slope of the discarded sublattice. The estimate on the component fibres in (2) does not use the ambient maximal slope. The [all-layer reduction](PERIOD_REFERENCE_WORD_COVOLUME.md) still applies to the other layers. A leading arithmetic Hilbert–Samuel formula for a fixed metrized model does not supply a uniform estimate at the original weights as the levels, model and dimension vary.

Pinned Roadmap passages give the [flat degree, terminal anchor and host bounds](https://github.com/rh-lean-roadmap/rh-lean-roadmap/blob/02a95b4c62db610642af5f278ee5d0d6df87b348/docs/src/book/main.tex#L49098-L49129), [terminal fibres, key theta comparison and component norm](https://github.com/rh-lean-roadmap/rh-lean-roadmap/blob/02a95b4c62db610642af5f278ee5d0d6df87b348/docs/src/book/main.tex#L53820-L53853), [row measure and coarse slope inputs](https://github.com/rh-lean-roadmap/rh-lean-roadmap/blob/02a95b4c62db610642af5f278ee5d0d6df87b348/docs/src/book/main.tex#L49692-L49745), [terminal finite-group trace and cut](https://github.com/rh-lean-roadmap/rh-lean-roadmap/blob/02a95b4c62db610642af5f278ee5d0d6df87b348/docs/src/book/main.tex#L53855-L53892), and [comparison to the recursive reference frame](https://github.com/rh-lean-roadmap/rh-lean-roadmap/blob/02a95b4c62db610642af5f278ee5d0d6df87b348/docs/src/book/main.tex#L21700-L21729).
