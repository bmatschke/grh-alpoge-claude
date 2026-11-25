# A common archimedean test for the entire bottom row

Fix the Hida datum, its grid, measures and Weil model, and a nonzero smooth tensor $w$ in the initial discrete-series model. Write $H$ for the bottom multiplicity space at the trivial finite character. For $u\in H$, a column $\Psi$, a finite coset datum $\Phi$, a tuple $\rho$ of real-place Fock polynomials and a coefficient covector $\xi$, write $P_{\rho,\xi}(u;\Psi,\Phi)$ for the actual terminal Bessel period of the successive theta lifts of $(e u)(w)$. Here the Hida model hypothesis makes $e$ injective with image exactly the prescribed multiplicity maps at the trivial character. On the finite catalogue use $\Psi_a,\Phi_a$ for its entries. The measures, finite level, $w$ and all finite entries are held fixed. [Original period][period] · [Selected space and separation quantifiers][quant] · [Marked and base choices][mark]

**Theorem.** Fix $\varepsilon$ and take the large-scale range in which the row size conditions imply the cusp parameter gaps. Use the grid scale $(1,C_F,b)$, so its gap constant is one. Under the real theta and cuspidal realization results used in [the increasing-rank row](ROW_TEST_CONVERGENCE.md), one archimedean pair $(\rho_*,\xi_*)$ satisfies
$$
 \bigcap_a \ker P_{\rho_*,\xi_*}(\,\cdot\,;\Psi_a,\Phi_a)
 =\bigcap_{\rho,\xi,a}\ker P_{\rho,\xi}(\,\cdot\,;\Psi_a,\Phi_a).
$$
It can be chosen with a monomial at every arrow and a covector from any fixed complex basis of the coefficient dual. No assertion that the right-hand side vanishes is needed for this choice. The equality is exactly the marking condition `RealOK`. If every nonzero bottom vector has a detector with archimedean data depending on the vector, this same pair separates the entire bottom space.

## Why all the archimedean functionals are proportional

At the last vertex let $\sigma_\tau^\infty$ be the smooth discrete series of the prescribed real unitary group, and $U_\tau$ the local factor of the dual coefficient representation of the definite top group. The latter representation is finite-dimensional irreducible. Its global dual decomposes as $\bigotimes_\tau U_\tau$. For example, one can realize the coefficient representation as a tensor product of its highest-weight modules, restrict each to the corresponding compact unitary group, then take the contragredient in each factor. The stored coefficient-space isomorphism intertwines this action, including the inverse in the definition of the column. [Coefficient dual and intertwining][coef]

The orthogonal extension at this vertex has $r=(m-2)/2$ hyperbolic planes, a middle vector of norm $-1$, and a positive definite orthogonal complement of rank $k=\dim_E V_{\mathrm{top},0}$. Thus the real pair has groups $U(k+r,r+1)$ and $U(k)$. The chosen flag and middle vector define the Bessel subgroup. Its character is generic since the stored coefficients on each successive simple root are nonzero. In the real trace convention the coefficients in the exponential are $-4\pi\tau(c_j)$. This identifies the setting of the archimedean Bessel uniqueness theorem, including the character on the radical and the diagonal action of the compact group. [Frame, sign and character on the actual grid][frame] · [Jiang–Sun–Zhu, §§2.1–2.2 and Theorem A][jsz]

For a smooth terminal multiplicity map $F$ and a permitted column $\Psi$, form the bilinear function
$$
 B_{F,\Psi}(\xi,v)=\mathcal B\bigl(\mathrm{pairVec}(\xi,\Psi),F(v)\bigr).
$$
Fix all tensor factors except those at $\tau$. Translating both inputs by the embedded compact group and changing the outer integration variable leaves the period invariant. Translating in the unipotent radical gives the specified character by the inner change of variables. For continuity, both integration quotients admit compact representatives. The absolute value of the integral is bounded by a constant depending on the column and measures times the supremum of $F(v)$ on their compact image. At fixed finite level the smooth automorphic realization controls this supremum by finitely many Sobolev seminorms of the varying smooth vector, with the other real vectors fixed. This follows from smooth globalization followed by local Sobolev evaluation on a compact neighborhood, or from the explicit multiplicity-map bound. The definite coefficient space is finite dimensional. These checks put the local slice in the **continuous** Bessel Hom space occurring in Theorem A. [Quotient, compact estimate and slice bound][cont] · [Two transformations][equiv]

That Hom space has dimension at most one. If at one place all local slices vanish then every global period vanishes. Otherwise choose a nonzero form $b_\tau$ in each local line and a local pair where it takes value one. With the other variables fixed, each slice is its value at this chosen pair times $b_\tau$. Replacing the pairs one place at a time gives
$$
 B_{F,\Psi}\bigl(\otimes_\tau x_\tau,\otimes_\tau v_\tau\bigr)
   = c_{F,\Psi}\prod_\tau b_\tau(x_\tau,v_\tau).
$$
Pure tensors span both algebraic tensor products, so the formula extends to their sums. In particular there is a single bilinear form $\ell$ independent of $F$ and $\Psi$ and every period is a scalar multiple of $\ell$. The zero family is covered by taking all coefficients zero. This application uses the multiplicity upper bound, so it requires no separate test for nonvanishing of a local Bessel model. The scalar $c_{F,\Psi}$ may depend on all the finite and automorphic data. [Passage from the local lines to the global form][line]

## Pullback through the actual theta integrals

For the $i$-th edge choose the one real intertwiner $I_i$ for its two signed discrete-series models. The prescribed finite coset vectors have the same archimedean vacuum at that edge. With a fixed finite coset and incoming multiplicity map $F_i$, the theta integral factors as $F_{i+1}(I_i(P,v))$ for **all** archimedean polynomials $P$ and smooth $v$. Here $F_{i+1}$ may depend on the finite coset and $F_i$. Algebraic Howe duality gives the fixed one-dimensional space of real intertwiners, cuspidality puts the output in the designated multiplicity space, and smooth globalization extends the equality from compact-finite vectors. The identification of the signed output uses the contragredient and the corresponding change of Fock frame. The coset change at finite places commutes with this real identification. [One-edge factorization](THETA_CUSPIDAL_FACTORIZATION.md) · [Signed frames, prescribed cosets and common intertwiner][arrow] · [Increasing arrow and convergence](ROW_TEST_CONVERGENCE.md)

Starting with $V_0=w$, put $V_{i+1}=I_i(\rho_i,V_i)$. Induction therefore gives $V(\rho,w)=V_m$ independent of the bottom row $u$ and the finite datum $\Phi$, and a terminal map $F_{u,\Phi}$ independent of $\rho$. The entire lifted function is $F_{u,\Phi}(V(\rho,w))$. The selected bottom rows satisfy the starting hypotheses: the principal row level fixes them since its modulus is divisible at the marked type primes, and its level character at the trivial tuple equals one. The stored map $e$ takes its values in exactly these rows. Applying the preceding bilinear formula gives
$$
 P_{\rho,\xi}(u;\Psi,\Phi)=A_w(\rho,\xi)\,c_{u,\Psi,\Phi},
 \qquad A_w(\rho,\xi)=\ell(\xi,V(\rho,w)).
$$
All scale, level and measure dependence allowed in this statement is retained. In particular $A_w$ is common only after fixing the grid, real models, $w$ and measures. [Iteration with the stated order of choices][tower] · [Principal-level row][good] · [Factorization on the prescribed stage][factor]

## Choosing the pair and computing its kernel

If some catalogue evaluation is nonzero for some $(u,a,\rho,\xi)$, expand each $\rho_i$ in monomials and $\xi$ in the chosen dual basis. Each polynomial has finite support. The integral is additive in each test coordinate by absolute convergence, and scalar multiplication of an input multiplies the integral by a scalar, with conjugation where the kernel convention requires it. A nonzero sum has a nonzero term. The resulting monomial tuple and basis covector $(\rho_*,\xi_*)$ satisfy $A_w(\rho_*,\xi_*)\ne0$. For every catalogue index and every $u$ it follows that
$$
 P_{\rho,\xi}(u;\Psi_a,\Phi_a)=
 \frac{A_w(\rho,\xi)}{A_w(\rho_*,\xi_*)}
 P_{\rho_*,\xi_*}(u;\Psi_a,\Phi_a).
$$
In particular the kernel intersection for this pair equals the intersection for all substitutions. If all catalogue evaluations are zero, both intersections equal $H$ and any monomial tuple and basis covector work. The coefficient module here is nonzero. This also covers $H=0$. The proof gives a choice of real test polynomials and does not bound their degrees. [Polynomial input at each edge][poly] · [Base conditions preserved on changing the pair][mark]

Now assume each nonzero $u$ has a nonzero period for some real pair, finite datum $\Phi$, and some allowed column. For fixed $\Phi$ the corresponding catalogue columns span the whole permitted column space. Linearity in the column gives a nonzero catalogue entry at that pair. The kernel intersection over all substitutions is therefore zero. The displayed theorem gives injectivity for one pair. Conversely fixed-pair injectivity supplies the variable-pair detector by taking a nonzero catalogue entry. This proves the equivalence with precisely the order required for `FunctionalsSeparate` on the Hida data. On the broader domain of that predicate, apply the factorization directly to the tensor lift of each $t\in R.\mathrm{EEat}(R.\mathrm{triv})$. The principal-level row condition puts these lifts in the required model, and the tensor-lift map is injective. Thus the same proof there involves every such $t$ without any separate assumption identifying this space with $H$. At fixed $\varepsilon,C_F$ take the maximum of the thresholds for the cusp gaps and variable-pair detection. [Spanning in the finite-data fibre](UNTWISTED_BOTTOM_ROW.md) · [Fixed-pair separation on the larger domain][sep]

**Consequence for the coefficient field.** The base-choice record already supplies the nonzero $w$, square proportionalities, frames, measures and catalogue. Its only additional condition for admissibility is `RealOK`. Replacing just the two archimedean entries by the pair constructed above thus marks *any* such base choice, even if a nonzero bottom vector is invisible. The finite field request and its transport only use the retained grid data. This removes the weak- and strong-separation premises from the field-construction step. Actual injectivity for the final rationality theorem still requires detection. [Choice and marking][mark] · [How the marked choice is used in field transport][carry] · [Coefficient-field proof](ROW_COEFFICIENT_FIELD.md)

[period]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AbelianVarietyTheory/Definitions/Divisors/BplusOfEquivariant.lean#L313-L332
[quant]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AbelianVarietyTheory/BlockTheory/DivisorBase/LevelPlusSubgroup.lean#L63-L94
[mark]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AbelianVarietyTheory/Definitions/TwistedInnerProducts/ExistsMatchOver.lean#L165-L219
[coef]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AbelianVarietyTheory/Proofs/TwistedOperators/DualCoefSpaceIsTensorOverRealPlaces.lean#L19-L85
[frame]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AutomorphicArithmetic/ThetaCorrespondence/BesselModels/SepGap.lean#L111-L166
[cont]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AbelianVarietyTheory/Proofs/TwistedOperators/TopSeparation.lean#L69-L135
[equiv]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AbelianVarietyTheory/Proofs/TwistedOperators/TopSeparation.lean#L135-L180
[line]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AutomorphicArithmetic/ThetaCorrespondence/BesselModels/SepGap.lean#L66-L99
[arrow]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AbelianVarietyTheory/Proofs/TwistedOperators/LevelInductionFromPairs.lean#L117-L175
[tower]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AbelianVarietyTheory/Proofs/TwistedOperators/FirstRowTowerMultiplicitySpacesOfArrow.lean#L13-L33
[good]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AbelianVarietyTheory/Proofs/TwistedOperators/GoodRowsPrincipalLevelAreRows.lean#L48-L84
[factor]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AutomorphicArithmetic/ThetaCorrespondence/BesselModels/SepGap.lean#L198-L220
[sep]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AutomorphicArithmetic/ThetaCorrespondence/BesselModels/SepGap.lean#L222-L258
[poly]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AbelianVarietyTheory/Definitions/Divisors/BasePlaceNotMemChiGridBadPlaces.lean#L545-L558
[carry]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AbelianVarietyTheory/Proofs/TwistedOperators/ExKeyOf.lean#L69-L89
[jsz]: https://arxiv.org/abs/0908.1728
