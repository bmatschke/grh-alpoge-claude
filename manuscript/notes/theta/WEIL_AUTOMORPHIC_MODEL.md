# The Weil representation on the rational lattice

Two analytic inputs to the unitary theta construction already have human proofs. One supplies the global oscillator representation with prescribed determinant characters. The other supplies the real discrete series with prescribed lowest compact type. The first concerns the action on functions used to form a theta kernel. The second specifies the representation one wants to see in that kernel. [Precise global existence assertion][exist] · [Precise real existence assertion][ds]

## How a sum over a lattice gives the theta kernel

Let $E/F$ be the CM extension in the source, let $S,T$ be its Hermitian spaces, and put $W=\operatorname{Res}_{E/F}\operatorname{Hom}_E(S,T)$. The symplectic form $B$ is the trace to $F$ of the Hermitian pairing on matrices multiplied by the fixed imaginary scalar $\xi_0$. A pair of isometries acts by $r(g,h)w=hwg^{-1}$. Fix the supplied standard additive character $\psi$ of $\mathbb A_F/F$, with the source's negative sign at infinity. [Form, action and function space][model]

Choose a rational polarization $W=L\oplus L^\vee$. In the Schrödinger realization the Heisenberg operators satisfy $\rho(w)\rho(u)=\psi(B(w,u)/2)\rho(w+u)$. The functional
$\vartheta(\Phi)=\sum_{a\in L(F)}\Phi(a)$ on Schwartz–Bruhat functions is invariant under rational translations and rational modulations. Translating its argument through the Heisenberg representation gives a function on all of $W(\mathbb A_F)$,

$$
        Z\Phi(w)=\vartheta(\rho(w)\Phi).
$$

The two basic identities now have immediate meanings. For $\gamma\in W(F)$ the rational translation law is $Z\Phi(\gamma+w)=\psi(-B(\gamma,w)/2)Z\Phi(w)$. Right translation by $u$ with the compensating phase $\psi(B(w,u)/2)$ gives $Z(\rho(u)\Phi)(w)$. At zero the function is the original theta sum. Weil's Fourier expansion on the compact rational quotient, equations (20)–(23), gives the unitary equivalence of the rational-lattice and Schrödinger models. His Theorem 6 is Poisson summation for the canonical rational lift of the symplectic group. The unitary dual-pair splitting for two Hecke characters restricting to the prescribed powers of the quadratic character respects that rational lift. Thus rational group elements leave evaluation at zero invariant. [Weil, *Sur certains groupes d’opérateurs unitaires*](https://doi.org/10.1007/BF02391012) · [Gan, *Automorphic forms and the theta correspondence*, §§3.2–3.5](https://swc-math.github.io/aws/2022/2022GanNotes.pdf)

The source works with continuous functions satisfying this translation law, fixed by a finite open Heisenberg level and smooth in all real directions. Its concrete construction works on exactly that space $\Theta$. At finite places it transports vectors fixed by a self-dual lattice to vectors fixed by the transformed lattice, using a normalized finite sum. At infinity it uses Gaussian oscillator operators. The two actions commute on $\Theta$. The pointwise continuity and equality of the squared norms follow there. Indeed $|f|^2$ is periodic under $W(F)$, so integrating it over any measurable fundamental domain computes the same quotient integral, and rescaling the additive Haar measure rescales both sides by the same constant. The construction verifies the rational splitting for these very operators by cancellation of the finite and real phases. [Finite norm and operators](../../../research/modules/theta/canonical_weil/main.tex#L169-L215) · [Smooth domain and product of the two actions](../../../research/modules/theta/canonical_weil/main.tex#L535-L657) · [Rational evaluation for this normalization](../../../research/modules/theta/canonical_weil/main.tex#L1013-L1116)

## What is measured at a split prime?

At a finite split place choose one factor of $E_v=F_v\times F_v$, with idempotent $e$. Its conjugate gives the other factor. Write $X=eW_v$ and $Y=\bar eW_v$, two perfectly paired Lagrangians. The local isometry on $X$ is $A(t)=h_e t g_e^{-1}$. The normalized change of variables on $\mathcal S(X)$ is
$U_A\phi(t)=|\det_{F_v}A|_v^{-1/2}\phi(A^{-1}t)$. Multiplication by a unitary scalar leaves its Heisenberg covariance intact. The splitting characters fix this scalar. For group elements supported at $v$, let $x$ and $y$ be the idèles equal to $\det g_e$ and $\det h_e$ in the selected factor and one elsewhere. The phase required by the source is

$$
              \chi_T(x)^{-1}\chi_S(y).
$$

The order and inverse matter. On switching factors the two determinant lifts are replaced by their inverses under conjugation. Every prescribed $\chi$ kills $a\bar a$ because its restriction to $F$ is a power of the quadratic norm character. Hence switching factors preserves their character values. [Split idempotents and determinant coordinates][idem] · [Character and invariant-functional formula][ident]

There is an elementary reason why this phase is visible to *every* invariant linear functional, including discontinuous ones. In the Schrödinger model the operators for $y_0\in Y$ are modulations $M_{y_0}\phi(t)=\psi_v(B(t,y_0))\phi(t)$, upon choosing the pairing convention. The quotient of $\mathcal S(X)$ by the linear span of $(M_{y_0}-1)\phi$ is one-dimensional, with quotient map $\phi\mapsto\phi(0)$. Indeed, any locally constant compactly supported $\phi$ vanishing at zero is supported on a compact set away from zero. Each point of that set has a compact open neighborhood on which some modulation is constant with value $c\ne1$, by nondegeneracy of the pairing. Refine a finite subcover into disjoint compact open pieces. The restriction of $\phi$ to each piece equals $(M_{y_0}-1)$ applied to that restriction divided by $c-1$. Conversely every such difference vanishes at zero. The same argument applies to each finite sum of tensors with arbitrary vectors at the other places. Consequently the operator acts on this quotient by its phase times $|\det_{F_v}A|_v^{-1/2}$. This positive number is independent of the functional.

How does one know that this phase and rational automorphy hold for a *single* global action? In the repository's proof the finite lattice sum first gives a strictly positive scalar at a split prime, by character orthogonality on the lattice quotient. The action is multiplied by the crossed determinant character above. For powers of a fixed auxiliary Hecke character the global finite and archimedean phases cancel on rational pairs. To pass to arbitrary prescribed $\chi_S,\chi_T$, divide these by the respective powers of the auxiliary character. The quotients $\nu_S,\nu_T$ are trivial on $\mathbb A_F^\times$. Hilbert 90 therefore defines a character on norm-one idèles by $\widetilde\nu(z/\bar z)=\nu(z)$. The resulting global twist is $\widetilde\nu_T(\det g)^{-1}\widetilde\nu_S(\det h)$. It is trivial on rational pairs, and has exactly the required quotient of determinant phases at each split prime. This identifies the normalization for the functions in the source in all ranks. [Positive lattice factor and determinant cut](../../../research/modules/theta/canonical_weil/main.tex#L217-L299) · [Global phase cancellation and character change](../../../research/modules/theta/canonical_weil/main.tex#L1118-L1238) · [Pinned construction for prescribed characters][twist]

Finally the requested group acts on the algebraic vector space of *all* complex functions on $W(\mathbb A_F)$. Choose a vector-space complement to $\Theta$. The direct sum of the action on $\Theta$ and the trivial action on the complement gives a group representation on that entire space. All the functional, norm and continuity identities are tested on $\Theta$, which is preserved by the Heisenberg operators. This completes the interpretation of the global existence input. [Source clauses][ident] · [Full construction](../../../research/modules/theta/canonical_weil/main.tex#L1118-L1153)

## The real discrete-series input

For $U(p,q)$ a regular Harish-Chandra parameter in the ordinary parameter lattice and a choice of order of the positive and negative coordinates determine a discrete-series representation. In the chosen chamber its lowest compact highest weight is $\mu_0=\lambda+\rho_n-\rho_c$, where $\rho_n$ and $\rho_c$ are half the sums of positive noncompact and compact roots. Atiyah and Schmid’s Theorem 8.5 gives multiplicity one for this type and puts every occurring compact highest weight $\mu$ in $\mu_0$ plus the positive root cone. With $\rho=\rho_c+\rho_n$ and $D=\mu-\mu_0$, this gives

$$
 \|\mu+2\rho_c\|^2-\|\mu_0+2\rho_c\|^2
       =2\langle\lambda+\rho,D\rangle+\|D\|^2.
$$

The right side is strictly positive for $D\ne0$. This proves the exact lowest-type test in the source. Square integrability of matrix coefficients follows from discrete-series orthogonality, and in rank zero the one-dimensional representation of the trivial group supplies the required empty weight. The ordinary existence assertion is thus covered by the existing discrete-series chapter. [Atiyah–Schmid, Theorems 8.1 and 8.5](https://doi.org/10.1007/BF01389783) · [Passage from the derived group and the lowest-type proof](../../../archive/rounds/v90/continuation_v90/discrete.tex#L26-L170) · [Ordinary existence statement][ds]

[exist]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AbelianVarietyTheory/PublishedTheorems/AutomorphicForms₂/WeilRepresentationUnitaryPair.lean#L12-L15
[ds]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AbelianVarietyTheory/PublishedTheorems/AutomorphicForms₂/DsExistsOfDiscreteSeriesExists.lean#L13-L20
[model]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Formalism/LocalToGlobal/IndefiniteReal/LocalNewformFunction.lean#L21-L49
[idem]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Formalism/LocalToGlobal/BesselHermitianTheta/TiedWeil.lean#L65-L78
[ident]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Formalism/LocalToGlobal/IndefiniteReal/LocalNewformFunction.lean#L51-L75
[twist]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AbelianVarietyTheory/Proofs/DivisorProofs/ExistsWeilDatumOfSplittingCharacters.lean#L32-L42
