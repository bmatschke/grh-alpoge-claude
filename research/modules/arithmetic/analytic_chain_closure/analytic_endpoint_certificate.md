# Analytic endpoint closure certificate

This is a dependency audit of existing claims AN2, AN3 and GH6, with CC1,
CC2 and QW14 providing the needed elementary Dirichlet facts. It introduces
no new theorem claim and changes none of the preserved text.

## Audited conclusion and its one arithmetic input

Fix a primitive Dirichlet target ψ. The family consists of the distinct
primitive inducers of its powers, with a positive coefficient for each and
coefficient 1 for the primitive principal character. Its weighted centered
sum is the fixed Hψ of AN1/GH2.

The required arithmetic input is: for every θ>1/2 there is a fixed constant
Cθ and arbitrarily late windows [Y,Y^(3/2)] on which Hψ(x)≤Cθ x^θ for all x.
It is enough that θ ranges over any sequence decreasing to 1/2. The constants
and the character family must be fixed before Y varies. The stronger
source-style bound Hψ(x)≤x^(1/2+Aψ ε), with Aψ independent of ε and ε chosen
before the window, has these quantifiers.

Under this input, the already reconstructed analytic argument proves
right-half-plane nonvanishing for this target and every constituent.
Applying it for every primitive target and then GH6 gives nonvanishing for
all positive-modulus Dirichlet characters to the right of 1/2, excluding
the principal pole at 1, and the critical-strip RH statement for all of
them. The ordinary Riemann hypothesis is the target of conductor 1.
This is Dirichlet GRH, not an assertion about arbitrary automorphic or
Dedekind L-functions.

## Dependency chain and verified mathematical joins

| Step | Existing proof | Why it closes |
|---|---|---|
| Continuation and primitive functional equation | CC1 | Finite Gauss transform, Schwartz Poisson summation and Mellin splitting give the actual completed L-function and root number; no GRH input is used. |
| Euler product and logarithmic derivative | CC2 | Absolute convergence on Re(s)>1 gives nonvanishing there and the von Mangoldt series. |
| L(1,χ)≠0 for nonprincipal χ | QW14 | The product over a full finite character group has nonnegative Dirichlet coefficients. If a nonprincipal factor vanished at 1 it would be entire and vanish at −2, contradicting its Taylor series with nonnegative coefficients at a real point >1. |
| Exact centered Mellin transform | AN2–AN3 | Centering cancels the apparent pole at 1. A zero ρ contributes the nonzero residue m/[ρ(1−ρ)]. |
| Positive character-family residue | AN3 | Real parts introduce the conjugate L-functions. Positive weights add multiplicities; coincident zeros cannot cancel. A real zero β∈(0,1) has positive residue. |
| Logarithmic-window localization | AN2 | The gamma density u^k exp(−336u)/k!, k=ceil(420U), has exponentially controlled tails outside [U,3U/2]. The bound concerns the positive part, so a one-sided upper bound is sufficient. |
| Exclusion of nonreal nearest poles | AN2–AN3 | A small vertical shift produces a unique nearest pole closer than both the real-center pole distance and 336−θ. Cauchy estimates isolate its derivative contribution and contradict the localized upper bound. |
| Real nearest-pole alternative | AN3 | If that shift argument does not apply, the nearest pole is real. Its positive residue forces a positive real derivative of exponentially larger size. The same one-sided inequality gives a contradiction. |
| Primitive to imprimitive transfer | GH6 | The finite extra Euler factors have modulus parameter p^(−Re(s))<1 for Re(s)>0 and are nonzero there. |
| Reflection to the critical line | GH6/CC1 | In the open strip the conductor, root number and gamma factors are nonzero. Reflection takes a zero left of 1/2 to a right-hand zero of the inverse primitive character. |

The contour disks in the nearest-pole argument lie in Re(s)>θ>0, because
their radii are less than 336−θ. Thus no unmentioned singularity at 0, or
trivial left-half-plane zero, enters the Cauchy estimate. A nearest pole
exists whenever the relevant distance is finite: poles are locally finite,
so minimizing a distance reduces to a compact disk. A sufficiently small
vertical perturbation avoids all finitely many equal-distance coincidences.

In the real-pole branch, uniqueness is uniqueness of the pole location;
coincident constituent zeros have already been combined into its positive
residue. This is why positivity of the family weights is essential.

## A simplification of the localization bound

Let g(u)=Hψ(e^u), σ=336, and A_k(z)=∫g(u)u^k e^(−zu)/k! du. Reality gives

    |A_k(σ+it)|+A_k(σ) ≤ 2∫g_+(u)u^k e^(−σu)/k! du.

Inside a good window g_+(u)≤Cθ e^(θu). Extending that part of the integral
to all u≥0 gives exactly Cθ/(σ−θ)^(k+1). Outside the window the old tail
estimate and the crude growth bound give O(σ^(−k)). Therefore the stronger
bound

    |A_k(σ+it)|+A_k(σ)
      ≤ 2Cθ/(σ−θ)^(k+1) + O(σ^(−k))

holds. The old proof's extra polynomial factor U+1 is unnecessary, but
harmless. Both versions give the same contradiction. This observation was
not used to alter any historical proof or claim metadata.

## Standard analytic leaves and excluded dependencies

The standard analytic background consists of basic complex analysis
(Cauchy's derivative bound, local factorization of holomorphic functions,
termwise integration/differentiation in a domain of absolute convergence),
the Gaussian Fourier transform/Poisson summation for Schwartz functions,
finite character orthogonality, and the elementary gamma-function facts.
CC1, CC2 and QW14 supply the particular Dirichlet instances used here.

The endpoint needs no zero-density theorem, Siegel-zero bound, prime number
theorem, conductor-uniform explicit formula or cohomological estimate.
Those results belong to producing the arithmetic windows, not to deducing
nonvanishing from them. In particular CN, BD and HD are leaves of the
QP22 pair-selection branch, not leaves of this final analytic criterion.

The arithmetic window input remains the sole substantive open leaf of this
analytic endpoint. Closing the endpoint does not discharge that input.

## Evidence and limits

The mathematical audit read the actual preserved AN2–AN3 and GH6 text,
CC1/CC2 and QW14, and the pinned source Statements.lean. The attached JSON
records their file hashes and exact prior source locators. This is a human
mathematical dependency certificate; it is not a new Lean build, an
independent kernel replay, or a claim that the arithmetic input was proved.
