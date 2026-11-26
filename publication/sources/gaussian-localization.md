# Bounding a cuspidal theta derivative on a complex component

The geometric argument needs an upper bound for a theta derivative on the whole complex component. Fix the level geometry of Roadmap Lemma B8.25gca, a good complex embedding and an even number $N$ of columns. Write $f=[E:\mathbb Q]/2$, $r$ for the Hermitian rank, $R_E$ for the root discriminant, $\xi>0$ for the absolute value of the polarizing scalar and $D$ for the degree of the homogeneous differential polynomial $P$. We derive the analytic estimate, keeping both the dimension and the shortest period in the bound. [Layer and parameter hypotheses](https://github.com/rh-lean-roadmap/rh-lean-roadmap/blob/c7755c1086f05d0918ee8496d95912e4f35e22f9/docs/src/book/main.tex#L20422-L20457)

## Projecting a Gaussian ball to the torus

Let $V=\mathbb C^d$, $d\ge1$, with its Euclidean norm and Lebesgue measure. Let $\Lambda$ be a lattice of covolume $v$ whose nonzero vectors have length at least $\ell>0$. Let $F$ be entire and suppose $W(z)=|F(z)|^2\exp(-\pi q\|z\|^2)$ is $\Lambda$-periodic for some $q>0$. Set $M_2=v^{-1}\int_{V/\Lambda}W(z)\,dz$. For every $w\in V$,
$$
 W(w)\le 2q^d v\left(1+\frac{2\sqrt{2d}}{\sqrt{\pi q}\,\ell}\right)^{2d}M_2 .
$$
Take $R=\sqrt{2d/(\pi q)}$. The Gaussian probability density $q^d\exp(-\pi q\|z\|^2)$ has expected squared radius $d/(\pi q)$, by differentiation of the Gaussian integral. Markov's inequality puts at least half its mass inside radius $R$. The entire function
$$
 F_w(z)=F(z+w)\exp\left(-\pi q\sum_j z_j\overline{w_j}-\tfrac12\pi q\|w\|^2\right)
$$
has squared absolute value $W(w)$ at zero. Its squared absolute value times $\exp(-\pi q\|z\|^2)$ is $W(w+z)$. On each sphere the average of $|F_w|^2$ is at least its value at the centre, by subharmonicity. Integrating in the radius therefore gives $W(w)/(2q^d)\le\int_{\|z\|<R}W(z+w)\,dz$.

Lifts of a single torus point that meet this ball are $\ell$-separated. The open balls of radius $\ell/2$ about them are disjoint inside a ball of radius $R+\ell/2$. Comparing their real $2d$-dimensional volumes bounds the number of lifts by $(1+2R/\ell)^{2d}$. Integrating this multiplicity against $W$ on the torus proves the claim. In the principal torus normalization of the formal source $v\le1$. Replacing 2 by 4 in the packing factor gives the bound used there. [Formal torus supremum statement](https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/ReciprocityTheory/ReductiveGroups/ArithmeticGeometry/SquareIntegrability/GCauchyStatement.lean#L277-L281) · [Packing and covolume in the formal argument](https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/ReciprocityTheory/ReductiveGroups/ArithmeticGeometry/SquareIntegrability/LemmaS.lean#L236-L286)

## Extracting a derivative without an extra factorial

Suppose $|G(z)|\le C\exp(a\|z\|^2)$ for an entire $G$, with $a>0$. Let $u_1,\ldots,u_D$ be unit vectors, allowing repetitions. For $D>0$ form $G(\sum_i t_i u_i)$ in $D$ independent variables. The coefficient of $t_1\cdots t_D$ is the required iterated directional derivative. Cauchy's inequality on a polydisk of radius $h$ bounds this coefficient by $Ch^{-D}\exp(aD^2h^2)$. Setting $h=(2aD)^{-1/2}$ gives $C(2aeD)^{D/2}$. Every auxiliary variable is differentiated once, even if two directions agree. At $D=0$ the bound is $C$. Summing monomials of the same degree costs the sum of their absolute coefficients.

For the normalized theta section, the tensor torus has complex dimension $d=frN$. A base minimum at least $\lambda$ gives a tensor minimum $\ell\ge\lambda/(2f^{3/2}N^2R_E)$. The standard vacuum and projection normalize the mean square after the finite-index factors cancel. Passing back to the frame contributes $(2\xi)^{D/2}$ to a homogeneous derivative of degree $D$. These are the tensor-lattice and vacuum comparisons at this step. Apply the ball estimate at $q=1$, take a square root and apply the derivative inequality at $a=\pi/2$. With $B_P=\sum_\alpha|P_\alpha|$ at the chosen embedding this gives, in the orthonormal frame $x$,
$$
 |s(x)|\le \sqrt{2}\,B_P(2\pi e\xi D)^{D/2}
 \left(1+\frac{8f^{3/2}N^2R_E\sqrt{2d}}{\sqrt\pi\,\lambda}\right)^d .
$$
The bound is uniform in the lattice characteristics. [Tensor minimum, isogeny and mean square](https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AbelianVarietyTheory/Proofs/CuspFormEvaluations/NormalisedThetaValueBound.lean#L71-L145) · [Standard vector and harmonic polynomial at the frame](https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AbelianVarietyTheory/Proofs/CuspFormEvaluations/ThetaGeneratorPointwiseBoundOrthonormalFrame.lean#L46-L101)

## Where cuspidality enters

Write $A=e^L$ and use the source bounds $L\ge1$, $r\le N$, $M\le A^{30}$, $R_E\le A^3$, $fr\le A$, $D\le\kappa\le A^{20}$, $frN\le2\kappa$ and $B_P\le\rho$. Cuspidality makes the supremum $S$ over the component frames finite. For $S>0$, choose a frame whose point norm exceeds $S/2$. The geometric transvection estimate and orthonormalization supply a frame of the same norm with Gram factors of absolute value one and
$$
 \lambda_1^2\ge 2R_E^{-2}\min\left(1,
 \frac{\pi}{2M\sqrt{d_H}(3f\kappa+2)\log 2}\right),
 \qquad \sqrt{d_H}\le R_E .
$$
This comparison uses the level-geometry laws where the point norm is close to its maximum. Since $3f\kappa+2\le A^{24}$, the minimum is at least $A^{-57}$ and $\lambda=A^{-40}$ is admissible. [Transvection model, level and polarization](https://github.com/rh-lean-roadmap/rh-lean-roadmap/blob/c7755c1086f05d0918ee8496d95912e4f35e22f9/docs/src/book/main.tex#L51484-L51553)

We have $N\le2A^{20}$ and $\sqrt{2d}\le2A^{10}$. The parenthesis in the bound for $|s(x)|$ is at most $1+64A^{95}\le A^{102}$, whose $d$th power is at most $\exp(204\kappa L)$. If $D\ge1$ the logarithm of the normalized derivative factor is $D(1+\log D)/2\le11\kappa L$. For $D=0$ this factor is one. Finally $2\sqrt2\le\exp(4\kappa L)$ since $2\kappa\ge d\ge1$. Combining the bounds proves
$$
 (2\pi\xi)^{-D/2}S\le\rho\exp(219\kappa L)
           \le\rho\exp\bigl(9000(frL)^2\kappa\bigr).
$$
The separate lower estimate requires particular nonzero block determinants. The proof above explains the upper estimate under the indicated tensor, model and frame comparisons. [Upper and lower estimates with their hypotheses](https://github.com/rh-lean-roadmap/rh-lean-roadmap/blob/c7755c1086f05d0918ee8496d95912e4f35e22f9/docs/src/book/main.tex#L20452-L20482)
