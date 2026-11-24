# Edition 0.75 · The definite Siegel–Weil identity and the arithmetic kernel

The theta-spanning argument needed an equality between two infinite series. At zero elliptic arguments one series counts rational matrices in definite lattices with specified test functions. The other sums over rational maximal isotropic subspaces in a doubled space. The manuscript proves that their stabilizer-weighted class averages agree **for every family admitted in the original definition**, at every period, for even row count $n$ and column degree $d$ with $4d<n$. This is the original definite Siegel–Weil assertion used at the arithmetic kernel. [Definite identity and kernel](continuation_v75/identity.tex) · [New TeX manuscript](RH_new_proofs_v0_75.tex) · [Cumulative TeX manuscript](RH_readable_reconstruction_v0_75.tex)

The reader now has the arithmetic kernel formula (ICL.6) on the stated doubling and level data, as well as the real reproducing formula (ICL.7) from edition 0.74. **Ten whole obligations remain**, all shared by RH and unrestricted Dirichlet GRH. These formulas are prerequisites inside the geometric and rationality obligations. The full contracts also ask for the common geometric objects and their comparison with this analytic construction. [Edition 0.74](RH_reconstruction_progress_v0_74.md) · [Original obligation contracts](continuation_v75/obligations.json)

## Why the difference must vanish

Let $D_X(Z)$ denote the weighted theta sum minus the weighted Eisenstein sum, after twisting the column lattice by $X$. Its period $Z$ has positive definite imaginary part at each CM embedding. Write $I(X)$ for the ratio of the additive covolumes of the standard lattice and $X$, and $J(Z)$ for the product of the determinants of those imaginary parts. Set $k=n/2$. The quantity whose supremum matters is

$$
  I(X)^k J(Z)^k |D_X(Z)|.
$$

The proof first shows that this supremum $S$ is finite, over **all** relevant twists and periods of one admitted family. It then selects one rational prime $q$ with a degree-one ideal distinct from its conjugate and prime to the given level. The identity obtained by summing over neighboring lattices gives

$$
 S\le \frac{q^k(1+q^d)}{q^{2k}+q^d}\,S .
$$

In positive degree the denominator minus the numerator is $(q^k-1)(q^k-q^d)>0$. Hence $S=0$. On the standard column lattice, the twist is the original family, giving the asserted equality. In degree zero both series have a single term and agree term by term. [Split prime, neighbor counts and contraction](continuation_v75/definite.tex) · [Hecke identity with the original weights](continuation_v75/hecke.tex)

Two issues are essential to this argument.

- **The weights have to match.** At the chosen prime, a neighbor shrinks one residue lattice along a hyperplane and enlarges the conjugate lattice by the dual line. Reversing an edge exchanges the two primes. Counting the isometries carrying one lattice to the other shows why each class enters with the reciprocal of the order of its stabilizer. The pointwise calculation also treats matrices whose image has a pole at the conjugate prime. A finite character sum detects exactly when their image belongs to the unique possible neighbor. [Definite mass](continuation_v75/identity.tex) · [Neighbor calculation](continuation_v75/hecke.tex)
- **One bound has to work for all periods and twists.** The boundary value in every rational direction is the lower-degree difference for a new admitted family. By induction it vanishes. The Fourier expansion then has only totally positive definite frequencies, which give enough decay on a region where the imaginary part is bounded below. Rational reduction theory carries every period into that region with a uniform bound on denominators. A separate finite-lattice calculation preserves admission on those moves, including its locality clause. Finally the finite ideal class group puts all column twists into one fixed level for the estimate. [Boundary limits](continuation_v75/boundary.tex) · [Invariant norm](continuation_v75/bounds.tex) · [Level and locality](continuation_v75/admission.tex)

## From the zero slice to cusp forms

The manuscript constructs the required finite Weil action from Poisson summation. It checks the sign in Fourier inversion, the level transformations, and the inner product used by the original tests. [Finite Hermitian Weil action](continuation_v75/weil.tex)

The proof also controls the convergence needed to take limits and derivatives. Bounded-denominator representatives of the isotropic spaces, together with Minkowski's second theorem, reduce the absolute Eisenstein estimate to a lattice series. If the CM type has $s$ embeddings, the decay exponent is $sn$ on a lattice of real dimension $4sd$. This gives exactly the required range $n>4d$. [Convergence and uniform high-region estimate](continuation_v75/convergence.tex)

In the doubled kernel the variables off the zero slice enter through a Gaussian and an invariant family of harmonic polynomials. Absorbing every Gaussian derivative into the differential operator gives an invariant polynomial in its derivative variables. Such a polynomial is generated by pairings of the two elliptic blocks. The heat equations replace each pairing by $2\pi i$ times a period derivative. All period derivatives of the identically vanishing zero slice vanish. This proves the differentiated comparison without asserting equality of the two series at arbitrary elliptic arguments. [Invariant differential operator](continuation_v75/heat.tex) · [Original heat equations and graph coefficients](continuation_v74/orbit.tex)

Applying this to the doubled tests of a supplied level system gives the original periodized arithmetic kernel (ICL.6), with one nonzero scalar, the specified class weights and the conjugated level multiplier. Together with (ICL.7), diagonal dominance and the earlier unfolding argument, it expresses every bounded holomorphic form in the stated range as a finite linear combination of analytic theta functions. The same coefficients work at every lattice and frame in that system. The conclusion uses the indicated invariant harmonic family and the doubled test, theta product and graph-coordinate transformation laws. [Kernel and scope](continuation_v75/identity.tex) · [Real reproducing integral](continuation_v74/reproduce.tex) · [Unfolding](integral_cusp_lattices_v46/main.tex)

## What the rational-test argument still needs

The next step is to compare those analytic theta generators with the actual short algebraic sections used on the identity cover. Equation (ICL.12) specifies the multiplier on each component and requires the remaining scalar to be independent of the component. The comparison has to use the original principal charts and their common finite-level system, including covariance, support, cuspidality and admission. Once these constructions are made, the coefficient descent and the transport from split kernels to rational class sums can be applied on those very data. The outer existence of a linked selection with its required integral and rational structures is a further obligation. [Exact short-section comparison](integral_cusp_lattices_v46/main.tex) · [Base dictionary transport](continuation_v74/vacuum.tex) · [Linked family](continuation_v74/bundle.tex) · [Checkpoint](CURRENT_CHECKPOINT_v0_75.json)

## Verification

This edition adds 30 indexed claims and brings the cumulative total to 4,202. The claim ledger binds each new proof to its TeX, its mathematical dependencies and the original Lean source ranges. The verifier checks those bindings against the public predecessor and the pinned original Git tree. The verification record gives the number of new claims, source excerpts and files, plus the local typesetting results. [Claim ledger](continuation_v75/claims.json) · [Validation record](continuation_v75/validation.json)

~~~sh
python3 continuation_v75/verify.py --formal-git formal_source
pdflatex RH_new_proofs_v0_75.tex
pdflatex RH_new_proofs_v0_75.tex
~~~
