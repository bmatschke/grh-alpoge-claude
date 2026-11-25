# Sampling the last singleton on the mixed Bessel slice

Fix two selected words, a real place and a valid prefix of total length $r$. Append a block of length one. Its residual group is $G_0=U(k,1)$, including when the original flag has $r>0$. The final negative vectors have norms $-T_p,-T_q$. Write $\zeta$ for their standardized complex pairing, $A=\sqrt{T_pT_q}$ and $s=|\zeta|^2-A^2$. The full Gram polynomial equals $|D_r|^2s$, since $D_{r+1}=D_r\zeta$ and the complete prefix minor $D_r\ne0$. Hence the full cut at $\varepsilon$ has residual width $\varepsilon/|D_r|^2$. The top singleton point weight has final factor $s_+^{k-1}$. The exponent in the arithmetic coordinate substitution is $\nu_{r+1,1}=0$, so the last singleton has the same coordinate before and after standardization. [Frames, group and point weights][model] · [Source coordinate change][coordinate]

Consider the empty differential word and allow cross terms between prefixes of the same two compact types. At a fixed valid prefix, the original double-cutoff test gives a smooth residual coefficient with bounded support and the actual residual frames, by the native slice theorem. Its remaining compact average uses the two probability Haar measures. The local results also apply to any smooth compactly supported residual test meeting $s=0$. Uniform passage from original double cutoffs to the full global coefficient is a separate input. [Native slice theorem][slice1] · [Residual frames and smoothness][slice2]

## The physical measure and the singleton wave

Use fixed unitary bases taking each normalized negative frame to the last negative unit vector. Both compact stabilizers are then identified with $K=U(k)$. For a smooth operator-valued test $F$ the actual residual compact average is

$$
 J(g)=\int_{K^2}\pi(a)F(a^{-1}gb)\pi'(b)^{-1}\,da\,db .
$$

Thus $J(agb)=\pi(a)J(g)\pi'(b)$. Use Hilbert–Schmidt inner products linear in their first argument. Each cross-pairing $\langle J_1(g),J_2(g)\rangle$ descends to $K\backslash G_0/K$. The frame bases and the sections in this proof are common to all prefixes in the chosen family. Fixed positive factors for each prefix can be absorbed into its vector.

For the prescribed residual Haar measure $d\mu$, use probability Haar on the right $K$. The quotient $G_0/K$ consists of $(x,w)\in\mathbb C^k\times\mathbb C$ with $|w|^2-\|x\|^2=1$. Its measure is
$c_X\delta(\|x\|^2-|w|^2+1)d^{2k}x\,d^2w$: this measure is invariant under $U(k,1)$, and invariant quotient measure is unique up to a scalar. The left $K$ rotates $x$ transitively on each sphere. The pairing $\zeta$ is $Aw$ up to the fixed sign or conjugation of the chosen Hermitian convention. Radial integration in $x$ yields

$$
 \zeta_*\mu=C_H\,s_+^{k-1}d^2\zeta,\qquad
 C_H=\frac{c_X\,|\mathbb S^{2k-1}|}{2A^{2k}}
     =\frac{k\,\mu\{0<s<A^2\}}{\pi A^{2k}}.                     \tag{1}
$$

The last equality calibrates the factor for any specified Haar measure by integrating over that annulus.

Write $j_i(\zeta)$ for $J_i$ on one common section. The cross-pairing is independent of the section. Put

$$
 D_{12}(\zeta)=C_H s_+^{k-1}\langle j_1(\zeta),j_2(\zeta)\rangle
$$

and extend by zero to $s\le0$. Formula (1) gives the *actual* Fourier pairing

$$
 \int_{\mathbb C}D_{12}(\zeta)e^{2\pi i\,2\Re(\xi\zeta)}\,d^2\zeta
 =
 \big\langle e^{2\pi i\,2\Re(\xi\zeta(\cdot))}J_1,J_2
                                      \big\rangle_{L^2(G_0,\mu)}. \tag{2}
$$

In particular the zeroth Fourier coefficient equals the residual Gram pairing. Simultaneous multiplication by the wave is an isometry, so the twisted and untwisted vectors for every finite set of prefixes have a joint positive Gram matrix. This also identifies the signed one-node calculation directly: for $\phi_\omega=e^{\omega\zeta-\bar\omega\bar\zeta}$, both initial insertions are $(J,0)$ while the positive wave transforms this array to $(\phi_\omega J,\omega\phi_\omega J)$. Its alternating contraction with $(J',0)$ is $\omega\langle\phi_\omega J,J'\rangle$, including at zero. [Source residual forms][forms] · [Terminal wave and one-node formulas][wave]

## The compact weight difference controls vanishing at the Gram wall

For the two dominant integral highest weights of $K$, denoted $\lambda,\lambda'$, put

$$
 d=\sum_i|\lambda_i-\lambda'_i|=\sum_i|u_i-u'_i|.
$$

The compact Harish–Chandra shifts cancel. For distinct selected compact weights this is at least the width of their differing coordinate. [Source cut][cut]

Write $w=e^{i\theta}\sqrt{1+\|x\|^2}$. There is a smooth section

$$
 g_\theta(x)=\operatorname{diag}(I_k,e^{i\theta})
 \begin{pmatrix}
 I_k+xx^*/(1+\sqrt{1+\|x\|^2}) & x\\
 x^*&\sqrt{1+\|x\|^2}
 \end{pmatrix}.
$$

Direct multiplication gives $g_\theta(x)\in U(k,1)$ and $g_\theta(ax)=a g_\theta(x)a^{-1}$ for $a\in K$. The homogeneous Taylor coefficient of degree $m$ of $J(g_\theta(x))$ at $x=0$ thus defines a $K$-map

$$
 \operatorname{Sym}^m((\mathbb C^k)_{\mathbb R}\otimes\mathbb C)
                      \otimes W_q\ \longrightarrow W_p .
$$

The complexified real standard representation is standard plus dual standard. In a tensor path starting at $\lambda'$, an application of the standard representation adds one coordinate unit to a highest weight and a dual factor subtracts one unit, retaining dominance. This follows from the compact Pieri rule, with determinant twists for arbitrary integral weights. Consequently there is no path to $\lambda$ in fewer than $d$ steps. The jets for $m<d$ vanish at every $\theta$, also after differentiating in $\theta$. Taylor's theorem on the compact phase circle and $s=A^2\|x\|^2$ prove

$$
 \|J(g_\theta(x))\|_{\rm HS}=O_J(\|x\|^d),\qquad
 \int_{0<s<\eta}\|J(g)\|_{\rm HS}^2d\mu(g)=O_{J,A,\mu}(\eta^{k+d}).
                                                                    \tag{3}
$$

Thus a bounded cutoff that equals one outside this layer costs $O(\eta^{(k+d)/2})$ in $L^2$ for any smooth, square-integrable residual average. This estimate applies to tests smooth through the wall. It also holds for finite linear combinations of such tests, retaining the cross terms in their squared norm. The constants may depend on the fixed prefix; in full Gram coordinates $\eta=\varepsilon/|D_r|^2$. [Compact tensor calculation in the reconstruction](SPECTRAL_BESSEL_MOMENTS.md)

## A sampling criterion on the selected CM lattice

The cross-pairing on the common section with $x=t e_1,\ t\in\mathbb R$, is smooth and even in $t$, since a fixed element of $U(k)$ takes $e_1$ to $-e_1$. Its Taylor series through order $2d-1$ vanishes by the jet calculation. A smooth even function of $t$ is smooth in $t^2$ on the closed half-line, as follows by Taylor expansion with remainder to arbitrary order. Consequently near $s=0$

$$
 D_{12}(\zeta)=s_+^{k-1+d}a_{12}(\theta,s)
$$

with $a_{12}$ smooth up to the boundary. With compact support this gives $D_{12}\in W^{h,1}(\mathbb C)$ for every integer $h\le k-1+d$, $h\ge0$; no boundary delta occurs because lower-order traces vanish. The selected large ranks give $h=5$.

For each real place $v$, let $V_v$ be the finite-dimensional subspace of $L^2(G_0,\mu_v)$ spanned by the chosen compactly supported smooth averaged coefficients. Assume these spaces are nonzero, since otherwise all the product densities vanish. Define

$$
 B_v=\sup_{\substack{J,J'\in V_v,\ \|J\|_2=\|J'\|_2=1\\
                         e\in\mathbb R^2,\ |e|=1}}
       \|\partial_e^5D_{J,J'}\|_{L^1(\mathbb C)},\qquad
 Z_v=\frac{g}{4\pi}B_v^{1/5},\qquad g=g_0g_1.                  \tag{4}
$$

Finite dimensionality and the proved regularity make $B_v$ finite. A zero $L^2$ vector is zero pointwise by smoothness. For $\ell\ne0$, integrate by parts five times in the unit direction corresponding to $\Re(v(\ell)\zeta)$ and use the trivial bound from (2). The compression of the phase multiplier of frequency $v(\ell)/g$ to $V_v$ has operator norm at most $\min\{1,(Z_v/|v(\ell)|)^5\}$. Independent unit vectors in the two slots of (4) give the operator norm.

For any vector in $\bigotimes_v V_v$, also allowing a finite Hilbert-space multiplicity with trivial multiplier, let $I$ be its squared norm. Evaluate on the common sections at all places, take the squared norm and multiply by the local densities in (1). The resulting $D\ge0$ is continuous with compact support and has integral $I$. For a sum of tensors it includes all cross-prefix terms. By (2), the trace-frequency Fourier coefficient at $\ell$ is the matrix coefficient of the tensor product of the compressed multipliers. Its absolute value is therefore at most $I\prod_v\min\{1,(Z_v/|v(\ell)|)^5\}$.

The actual last singleton period lattice and its trace dual satisfy

$$
 L=\{t\in g\mathcal O_E:t+\bar t\in g^2\mathcal O_E\},\quad
 L^*=\{\ell\in E:\operatorname{Tr}_{E/\mathbb Q}(\ell L/g)\subset\mathbb Z\}
                   \ \subset J_0=g^{-1}\mathfrak d_E^{-1}.
$$

The containment follows from $g^2\mathcal O_E\subset L$. For $\ell\in J_0\setminus\{0\}$, $\prod_v|v(\ell)|\ge\sqrt{N(J_0)}$ by the integral ideal norm bound. Put $T=(\prod_vZ_v/\sqrt{N(J_0)})^{1/f}$ with $f=[E:\mathbb Q]/2$. If $T<1/2$, the dyadic-box estimate B8.10aa sums the product of the fifth-power bounds at nonzero frequencies at cost at most $(CT^{5/2})^f$, with an absolute constant. The periodization of $D$ is continuous and its Fourier series is absolutely convergent. Thus Poisson summation gives, for every translate,

$$
 \left|\operatorname{covol}(L)\sum_{t\in t_0+L}D(t)-I\right|
                  \le I\,(CT^{5/2})^f.                           \tag{5}
$$

This includes sample points on the wall. [Two lattices and Fourier normalization][lattice] · [Ideal estimate and dual inclusion][latticeproof]

Equations (1)–(3) give the physical Haar density, wave identity and boundary suppression on this residual cell. To use (5) at relative error $b^{-7}$ it would suffice to prove $T<1/2$ and $(CT^{5/2})^f\le b^{-7}$ uniformly in the prefix spans and cutoffs. The local hypotheses on smooth residual tests alone cannot bound (4) uniformly. For example take an averaged test $J$ nonzero at a point $\zeta_0$ with $s>0$, choose a smooth compactly supported scalar bump $\psi$ equal to one near zero, and replace $J$ by $\psi((\zeta-\zeta_0)/h)J$. Compact equivariance is preserved. As $h\downarrow0$ its squared norm is asymptotic to a positive constant times $h^2$. For a nonzero coordinate derivative of $|\psi|^2$ of order five, the corresponding $L^1$ derivative of its diagonal density before normalization is asymptotic to a positive constant times $h^{-3}$, by the change of variable $\zeta=\zeta_0+h z$. After unit $L^2$ normalization the ratio in (4) grows as $h^{-5}$. This example concerns the unrestricted test space; quantifying the actual selected discrete-series coefficients can use their spectral equations. The relative criterion uses the same residual Haar on both sides. It does not determine a conversion from the total tower energy to the ambient formal degree. The nonempty differential words, earlier singleton levels and blocks of length at least two still require their respective comparison and sampling estimates. [Five-companion estimate used by the source][five] · [Full recurrence and target][target]

[model]: https://github.com/rh-lean-roadmap/rh-lean-roadmap/blob/94e6a98b4e74932a0298d6bd22d44cf60c62764b/docs/src/book/main.tex#L17120-L17146
[coordinate]: https://github.com/rh-lean-roadmap/rh-lean-roadmap/blob/94e6a98b4e74932a0298d6bd22d44cf60c62764b/docs/src/book/main.tex#L46189-L46219
[slice1]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Formalism/HermitianCurvature/HermitianCurvatureProofs/SliceCompactSupportCoefficient.lean#L14-L30
[slice2]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Formalism/HermitianCurvature/HermitianCurvatureProofs/SliceCompactSupportCoefficient.lean#L208-L232
[forms]: https://github.com/rh-lean-roadmap/rh-lean-roadmap/blob/94e6a98b4e74932a0298d6bd22d44cf60c62764b/docs/src/book/main.tex#L17248-L17266
[wave]: https://github.com/rh-lean-roadmap/rh-lean-roadmap/blob/94e6a98b4e74932a0298d6bd22d44cf60c62764b/docs/src/book/main.tex#L44899-L44926
[cut]: https://github.com/rh-lean-roadmap/rh-lean-roadmap/blob/94e6a98b4e74932a0298d6bd22d44cf60c62764b/docs/src/book/main.tex#L44930-L44941
[lattice]: https://github.com/rh-lean-roadmap/rh-lean-roadmap/blob/94e6a98b4e74932a0298d6bd22d44cf60c62764b/docs/src/book/main.tex#L17997-L18010
[latticeproof]: https://github.com/rh-lean-roadmap/rh-lean-roadmap/blob/94e6a98b4e74932a0298d6bd22d44cf60c62764b/docs/src/book/main.tex#L46021-L46028
[five]: https://github.com/rh-lean-roadmap/rh-lean-roadmap/blob/94e6a98b4e74932a0298d6bd22d44cf60c62764b/docs/src/book/main.tex#L46262-L46292
[target]: https://github.com/rh-lean-roadmap/rh-lean-roadmap/blob/94e6a98b4e74932a0298d6bd22d44cf60c62764b/docs/src/book/main.tex#L46439-L46468
