# Absolute convergence and target square integrability at $(p,q)=(1,1)$

At the first mixed grid square $j=m-3$ ($m\ge3$), write $a,n$ for the big and small source dimensions over $E$, $d=a+n$, $e=(a-n)/2$, and $D=[E:\mathbb Q]$. The signatures at every real place are $(a-1,1)$, $(1,n-1)$ and $(d-2,2)$. The good-geometry inequalities give $e>5$ and $n>5$. Each source has rational Witt index one and the target has rational Witt index two. Indeed the norm quadratic form over $F$ of an indefinite Hermitian space of dimension at least three is isotropic by Hasse–Minkowski because it is indefinite at infinity and has dimension at least six at each finite completion. For the skew-Hermitian target first multiply the form by a nonzero totally imaginary scalar giving the stipulated Hermitian signatures. Split one hyperbolic plane and apply the same argument to the target complement of signature $(d-3,1)$. Real signatures bound the indices in the opposite direction. [Rank and signature assumptions][mix-rank] · [Rational hyperbolic splitting](ROW_BETA_RATIONAL_PLANES.md)

For a pure test $\Phi=f\otimes\phi$ with fixed finite part, let $\mathcal A_{\Phi}(h)=\int_{[U_{\rm source}]}|\theta(\Phi;g,h)|\,dg$. The big test is unrestricted. The small test is primed at the prescribed split place. For a target Siegel representative of parameters $T_1\ge T_2\ge0$,
$$
 \mathcal A_{b,\Phi}(h)\le C_\phi p_\phi(f)e^{Da(T_1+T_2)/2},\qquad
 \mathcal A_{s,\Phi}(h)\le C'_\phi p'_\phi(f)e^{D(aT_1+(n-2)T_2)/2}.
$$
Here $p_\phi,p'_\phi$ are continuous Schwartz seminorms. The constants may depend on the finite tests and compact parts of the Siegel sets. Both pointwise absolute integrals belong to target $L^2$. Thus each integrated theta lift, and any fixed linear combination of the two, belongs to target $L^2$. This will allow Hilbert-space pairings with a cuspidal remainder once its two constant terms have been controlled.

**The kernel estimate.** Let $S\ge0$ be the rank-one source parameter and put $r=a$ or $n$. The source torus weights are $S,-S,0^{r-2}$, the target weights are $T_1,T_2,-T_1,-T_2,0^{d-4}$. The sum of the positive parts of all tensor weights is
$$
 W_r=2\max(S,T_1)+2\max(S,T_2)+(d-4)S+(r-2)(T_1+T_2).
$$
For each pair of nonzero source and target directions the four weights contribute $S+T_i+|S-T_i|=2\max(S,T_i)$. Poisson summation bounds the squared theta function by a sum of Schwartz matrix coefficients over rational $r\times d$ matrices. Frozen finite supports, including their compact translates, clear a common denominator. For one matrix entry of weight $u$ the number-field lattice sum of a sufficiently fast decreasing weight is $O(\exp(D\max(u,0)))$ because a ball of archimedean radius $R$ in the fixed fractional lattice has $O((1+R)^D)$ points, and summing dyadic shells with more than $D$ decay powers gives the bound. Taking a product over the entries gives $C_\phi p_\phi(f)^2\exp(DW_r)$. [Squared theta and matrix coefficients][mix-sq] · [Weight formula and convention][mix-cone] · [Lattice count in rational Witt coordinates][mix-product]

For the small test the exponent improves to $D W_n-M(S-T_1)_+$ for any integer $M\ge0$. To see why the positive-rank condition enters the **squared** estimate, cut the local barred test into finitely many compact-open pieces supported in matrix balls $C$ such that $C+C$ consists of full-row-rank matrices. Such a ball exists about each full-rank $Y$ since $2Y$ is still full rank. Pair each piece with its global reflection $\Phi(-\cdot)$ in the coefficient formula. Their theta values agree because rational negation permutes the theta sum and the Weil action commutes with reflection. In the barred chart the translation component of a nonzero reflected coefficient belongs, up to sign and invertible changes of basis, to $C+C$. This follows from intersecting the translated support with the reflected support, or from the character covariance of the Heisenberg pairing. Hence only full-row-rank rational matrices occur. Add the finitely many piecewise bounds by the triangle inequality. [Reflected theta and coefficient bound][mix-par] · [Local support cut and covariance][mix-cut]

For such a rational matrix the single expanding source row has a nonzero entry in a rational Witt basis. After clearing the common denominator, that entry has modulus bounded below at some complex embedding by the product formula. The largest available contracting target weight is $T_1$, so the rescaled matrix size gains at least a constant times $e^{S-T_1}$ when $S>T_1$. Increasing the Schwartz order gives the asserted exponential saving. The pin bounds minors of any size using $M(n+1)$ extra decay powers, which suffices here as well. These estimates use the adelic Siegel reduction and theta covariance/Poisson identities for the given Weil model. The finite local primed condition is stable under source and target translates. [Nonzero minor and norm estimate][mix-minor] · [Schwartz powers used for the saving][mix-decay] · [Compact translates and seminorm][mix-semi]

**Source integration.** The source Siegel density contributes $e^{-D(r-1)S}\,dS$. Dividing the logarithm of the resulting majorant by $D$ before the primed saving gives
$$
 H_r=\tfrac12 W_r-(r-1)S=
 \begin{cases}
 \frac r2(T_1+T_2)+(\frac d2-r-1)S,&0\le S\le T_2,\\
 \frac r2T_1+\frac{r-2}{2}T_2+(\frac d2-r)S,&T_2\le S\le T_1,\\
 \frac{r-2}{2}(T_1+T_2)+(\frac d2-r+1)S,&T_1\le S.
 \end{cases}
$$
For $r=a$ the slopes are $-e-1,-e,1-e$, all at most $-(e-1)$. Continuity across the breakpoints gives $H_a\le a(T_1+T_2)/2-(e-1)S$. Integrating costs at most $1/(D(e-1))$. For $r=n$ the slopes are $e-1,e,e+1$. Up to $S=T_1$ they are at least $e-1$, so the integral on $[0,T_1]$ is at most $\exp(DH_n(T_1))/(D(e-1))$. Beyond $T_1$, the square root of the primed saving makes the logarithmic slope $D(e+1)-M/2$. Take $M=2D(e+1)+2$. This last integral costs at most $\exp(DH_n(T_1))$, where $H_n(T_1)=(aT_1+(n-2)T_2)/2$. This proves the two estimates, including on $T_1=T_2$ and $T_2=0$.

**Target integration.** The target density is bounded by a constant times $e^{-D((d-1)T_1+(d-3)T_2)}dT_1dT_2$. The $d-4$ anisotropic $E$-coordinates in each direction and its $F$-valued central root of weight two give $D(d-3)(T_1+T_2)$. The two mixed $E$-roots $T_1\pm T_2$ give the remaining $2DT_1$. Multiplying by the squared big estimate gives $\exp(-D((n-1)T_1+(n-3)T_2))$, and the squared small estimate gives $\exp(-D((n-1)T_1+(a-1)T_2))$. In simple-root variables $u=T_1-T_2,\ v=T_2$, the respective chamber integrals are
$$
 \frac{1}{D^2(n-1)(2n-4)},\qquad
 \frac{1}{D^2(n-1)(d-2)}.
$$
Together with the compact factors these give continuous seminorm bounds into target $L^2$. Finite sums follow by the triangle inequality. The Haar calculation itself only requires $e>1$ and $n>2$. The argument applies to every tuple on the given square, with no assertion that the seminorm constants are uniform in a varying finite Schwartz function. [Springer, fundamental set theorem, §§2.1–2.2](https://math.stanford.edu/~conrad/conversesem/refs/springer.pdf#page=5) · [Adelic chamber integration][mix-siegel] · [Transfer of the majorants to the two quotients][mix-int]

[mix-sq]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/WeilBound/ThetaLifts/FrameEstimates/SqAllC.lean#L62-L87

[mix-cone]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/WeilBound/ThetaLifts/FrameEstimates/SquareIntegrableWeilRange.lean#L39-L59

[mix-product]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/WeilBound/ThetaLifts/FrameEstimates/LatTor.lean#L118-L149

[mix-par]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/WeilBound/ThetaLifts/FrameEstimates/ThetaSumNeg.lean#L75-L125

[mix-cut]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/WeilBound/ThetaLifts/FrameEstimates/HermitianFormDetNeZero.lean#L90-L145

[mix-minor]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/WeilBound/ThetaLifts/FrameEstimates/ExistsColsDetNeZero.lean#L96-L141

[mix-decay]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/WeilBound/ThetaLifts/FrameEstimates/LatFull.lean#L13-L46

[mix-semi]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/WeilBound/ThetaLifts/FrameEstimates/InitialPairs/SquareIntegrableOfLatticeTorus.lean#L44-L67

[mix-siegel]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/WeilBound/ThetaLifts/FrameEstimates/SquareIntegrableWeilRange.lean#L61-L69

[mix-int]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/WeilBound/ThetaLifts/FrameEstimates/InitialPairs/SquareIntegrableOfLatticeTorus.lean#L69-L129

[mix-rank]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AbelianVarietyTheory/BlockTheory/DivisorBase/WeilTensorModels.lean#L360-L369
