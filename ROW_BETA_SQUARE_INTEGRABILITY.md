# Square integrability and local quotient descent at the first beta step

Let $a>n$ be the big and small source ranks, $d=a+n$ the target rank, $e=(a-n)/2$, and $D=[E:\mathbb Q]$. At $(p,q)=(0,1)$ the big source is definite. The small source and the target each contain the indicated rational hyperbolic plane and have rational Witt index one. Here $e>0$ and $n>1$. For a fixed finite test $\phi$, write $J(f\otimes\phi)$ for the integrated theta function of an arbitrary real Schwartz test $f$. On the primed side require full-row-rank support in barred coordinates at one fixed split place. The following estimate holds on both sides for a target Siegel representative of logarithmic parameter $T\ge0$:
$$
  \int_{[U_{\rm source}]}|\theta(f\otimes\phi;g,h)|\,dg
     \le C_\phi\,p_\phi(f)\,e^{DaT/2}.
$$
Here $p_\phi$ is a continuous Schwartz seminorm, and $C_\phi$ also absorbs fixed Haar normalizations and the compact parts of the Siegel sets. In particular $\|J(f\otimes\phi)\|_2\le C'_\phi p_\phi(f)$. [Seminorm form of the pointwise majorant][l2-semi] · [Passage through the two quotient integrations][l2-quot]

## The cusp exponent

Write $S\ge0$ for the logarithmic small-source parameter. The three sorts of row weights are $S,-S,0$, with $n-2$ zero rows. The corresponding target weights are $T,-T,0$, with $d-2$ zero columns. Thus the sum of the positive parts of the tensor weights is
$$
 W(S,T)=2\max(S,T)+(d-2)S+(n-2)T .
$$
The four corners contribute $S+T+|S-T|$. The positive row paired with a zero column and the positive column paired with a zero row give the remaining summands. The Poisson bound for the squared theta function, and the full-rank minor estimate, give for every integer $M\ge0$
$$
 |\theta(f\otimes\phi;g,h)|^2
 \le C_{\phi,M}\,p_{\phi,M}(f)^2
         \exp\{D W(S,T)-M(S-T)_+\}.
$$
The nonzero minor enters only on the primed side. After fixing the finite support and clearing one denominator, a nonzero minor has absolute value bounded below at some archimedean embedding. When $S>T$ the expanding row gains at least $e^{S-T}$, and spending $M(n+1)$ powers of Schwartz decay on the minor gives the displayed factor. The compact factors of the two Siegel sets enlarge the common finite lattice support and the seminorm by bounded amounts. On the definite source the squared theta estimate instead uses $W(0,T)=aT$ with $a$ rows and no rank restriction. The same seminorm is valid for every $f$ with these frozen finite factors. [Exact positive weights][l2-weight] · [Integral minor and gain][l2-minor] · [Additional powers of Schwartz decay][l2-decay] · [Uniformity over the compact sets][l2-semi]

For a rank-one unitary group of dimension $r$, the Siegel density in this convention is bounded, after integration over its compact factors, by a fixed multiple of $e^{-D(r-1)S}\,dS$. Indeed the horizontal unipotent block has $r-2$ coordinates over $E$ of weight one and its centre has one coordinate over $F$ of weight two. Their product gives the parabolic modulus $e^{D(r-1)S}$. On the range $0\le S\le T$, taking square roots and multiplying by the small-source density gives the exponent
$$
 D\left(\frac n2 T+eS\right).
$$
Its integral is at most $(De)^{-1}e^{DaT/2}$. On $S\ge T$ the exponent becomes
$$
 \frac{Da}{2}T-\left(\frac M2-D(e+1)\right)(S-T).
$$
Take $M=2D(e+1)+2$. Integration on this range adds at most $e^{DaT/2}$ times the same constant. The big-source bound follows by integrating over a compact quotient. Finally multiply the square of the resulting bound by the target density $e^{-D(d-1)T}dT$. The remaining integral is
$$
 \int_0^\infty e^{-D(n-1)T}\,dT=\frac{1}{D(n-1)}.
$$
The calculation also covers compact portions at $S=0$ or $T=0$ by adjusting the constants. It gives absolute convergence for the indicated points and a continuous map to target $L^2$. [Unitary torus and density conventions][l2-rho] · [General primed square integrability][l2-general]

## Local smoothness, semisimplicity and the designated place

For a fixed finite test the map from real Schwartz space to $L^2$ is linear and continuous by the seminorm bound. The source acts trivially after integration because the integral converges absolutely and the quotient measure is right invariant. The target action is right translation by covariance. Since the real Weil action is smooth in the Schwartz topology, a target Lie derivative passes through the $L^2$ map by convergence of the difference quotients there. Iterating gives every derivative, and real source differentiation gives zero. Compact smoothness and finite compact types hold for polynomial oscillator vectors. This proves the equivariance as a map of Harish-Chandra modules, including the infinitesimal actions on the Hilbert-space images. At an arbitrary finite place $v$ one may vary over all local Schwartz–Bruhat tests as long as a primed full-rank factor is kept at another place. The images are smooth for the target $v$-adic group by local Schwartz smoothness. The constants may change with a finite test; they can be made uniform at fixed compact support and finite translation level by using a basis of the resulting finite-dimensional local test space. [Squared norm and continuity for the realized theta integrals][l2-est] · [Real and finite targets of the individual kernel argument][l2-kills]

At the prescribed full-rank place $v_1$ arrange a second split place $v_2$ outside the data. Replace the frozen $v_2$ component by a full-rank representative of the same source-coinvariant class, using the row sieve. The difference is a finite sum of source translates minus their original tests at $v_2$. For every original full-rank $v_1$ input these differences have vanishing integrals by absolute convergence and source invariance, using $v_1$ as the spectator throughout this replacement. Now keep $v_2$ full-rank and allow arbitrary $v_1$ inputs. The resulting map realizes the original integral on its prescribed domain and extends it to the full local Schwartz space at $v_1$. This uses the sieve before applying local duality. Its normalized degree is nonzero because $n-1<d/2$. No value of a possibly divergent integral without a spectator has entered. [Full-rank sieve and its degree][l2-sieve] · [Full-rank support in the actual barred coordinates][l2-so]

For any one active local group, the image $V$ of the local slice is therefore a quotient of the full local theta module of the trivial representation of the source, in the splitting carried by that oscillator. This full module is admissible and has finite length. Its maximal semisimple quotient is either zero or the unique small theta lift, with multiplicity one. For split finite places these are the $\mathrm{GL}_r\times\mathrm{GL}_d$ theorems: Mínguez states finite length on p. 718 and proves the uniqueness and Hom dimension one in Theorem 1. For nonsplit finite places use the characteristic-zero unitary Howe theorem; at infinity use the algebraic real Howe theorem on the polynomial module. A twist of the splitting transports the corresponding source character and target action. [Mínguez, pp. 718–719](https://www.numdam.org/item/10.24033/asens.2080.pdf#page=2) · [Gan–Takeda, Theorem 1.2](https://arxiv.org/pdf/1407.1995#page=2) · [Howe, real algebraic correspondence](https://www.math.utah.edu/~ptrapa/math-library/howe/howe-transcending-1989.pdf)

The positive definite inner product inherited from target $L^2$ makes the image semisimple. Indeed, at a finite place, for $u\in V$ fixed by a compact open $C$ project orthogonally onto $N^C$ for any invariant submodule $N$. This is finite-dimensional by admissibility. Compact averaging of any vector in $N$ to $N^C$ shows the difference is orthogonal to *all* of $N$. Thus $V=N\oplus (N^\perp\cap V)$ and the summands are invariant. For a real Harish-Chandra module decompose a compact-finite vector into its finitely many compact types, project in each finite-dimensional isotypic part, and apply the same argument. The orthogonal complement is stable under the real Lie algebra by skew-adjointness on the smooth vectors, and hence under its complexification. As $V$ has finite length, it is a direct sum of irreducibles. The unique multiplicity-one cosocle gives $V=0$ or $V\simeq\theta(\mathbf1)$. For a prescribed onto irreducible local projection $p$, uniqueness forces $\ker p\subseteq\ker J$ on this slice. The assertion concerns an individual integral and holds also for a frozen slice which vanishes identically. It requires no multiplicity statement in the global automorphic spectrum. [Application to the prescribed projections][l2-kills]

For a finite sum of factorizable tests, lift these local assertions by multilinearity. At any finite set of varying places the kernel of the tensor of surjections is the sum of the kernels in individual slots. Outside this set the fixed vacuum classes agree when matching, and enlarging it tensors with nonzero vacuum classes. Consequently a zero local quotient tensor is killed by the corresponding individual lift. Obtaining a comparison scalar for the two different source groups still uses the relevant local matching and boundary or Petersson formulas.

[l2-semi]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/WeilBound/ThetaLifts/FrameEstimates/InitialPairs/SquareIntegrableOfLatticeTorus.lean#L44-L67
[l2-quot]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/WeilBound/ThetaLifts/FrameEstimates/InitialPairs/SquareIntegrableOfLatticeTorus.lean#L69-L129
[l2-weight]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/WeilBound/ThetaLifts/FrameEstimates/InitialPairs/SquareIntegrableIntegralHolds.lean#L94-L111
[l2-minor]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/WeilBound/ThetaLifts/FrameEstimates/ExistsColsDetNeZero.lean#L93-L148
[l2-decay]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/WeilBound/ThetaLifts/FrameEstimates/LatFull.lean#L13-L46
[l2-rho]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/WeilBound/ThetaLifts/FrameEstimates/SquareIntegrableWeilRange.lean#L39-L60
[l2-general]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/WeilBound/ThetaLifts/FrameEstimates/InitialPairs/SquareIntegrableOfLatticeTorus.lean#L161-L184
[l2-est]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/WeilBound/ThetaLifts/FrameEstimates/WeilConv.lean#L60-L76
[l2-kills]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/WeilBound/ThetaLifts/SphericalLattices/ThetaKillsCuspFormsSpherical.lean#L149-L190
[l2-sieve]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AbelianVarietyTheory/Proofs/DivisorProofs/ExistsTranslatesEqPrimFrameLat.lean#L213-L255
[l2-so]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AbelianVarietyTheory/BlockTheory/DivisorBase/WeilTensorModels.lean#L267-L279
