# Independent mathematical review: BNV1–BNV23

**PASS at the exact stated scope.** Reviewer: /root, independent of the author /root/bessel_nonvanishing.

I read every claim and checked the central endpoint definitions directly in the pinned source: IntSStatement; the complete RaisingLoweringNormIdentities declaration file; BesselNZ/BesselAll; GapLap; IsHCTypeU/IsHCTypeW and the independently quantified Cayley witnesses; and the literal endomorphism-valued BesselNVGap. I also read the inherited DC6, DC8, DC11, DC13, BWP2 and AMD8 proofs actually used. All cited source file and range bytes were independently compared with the pinned Git blobs.

The analytic proof is substantive: it derives the uniform highest-weight estimates and tangent Gaussian, proves a global Cayley majorant, obtains a nonzero Gaussian integral, and identifies it with the original vector period by the exact compact Schur factor. The Vandermonde construction matches the character rather than assuming a generic pairing. The transport proof retains every permitted character, measure, compact representation, Cayley matrix and lowest vector, and the final return is to the actual operator integral.

## Corrections made and rechecked

1. The Gaussian majorant now has one eventual threshold before every integration variable. Pointwise convergence remains pointwise; no unsupported exchange of nonuniform bounds and integration occurs.
2. GaussianLimitHaar retains the original eventual almost-everywhere strong measurability, with nonsingular Haar dilation supplying the scaled measurability.
3. Compact Schur orthogonality now has the original arbitrary ambient sigma-finite second measure, including measures not supported on N. Zero extension of the original kernel and its compact equivariance are explicitly proved at this scope.
4. The separate existential unitary Cayley witnesses for the supplied discrete series and the supplied lowest vector are explicitly reconciled by a compact inner conjugacy.
5. TeX row breaks in the threshold display were corrected without changing its mathematics.

## Remaining producer

BNV23 is a complete conditional deduction. The original two-sided StepStatement is not proved by this chapter, and no abstract branching result is substituted for its tensor, quotient and nonzero-evaluation argument. The unconditional BesselNVGap, unconditional analytic setting and whole selected global obligations therefore remain open at this chapter's boundary. The supplied Forms0 scope is retained.

## Claim-by-claim assessment

- **BNV1**: The polynomial chart and its quadratic inverse bound give exponent b>2d; the original 2rn^2 dominates 2d, including k=0 and the compact r=0 case. Haar regularity is supplied by AMD8.

- **BNV2**: The half-integral coset and interlacing imply each initial displacement is a nonnegative integer; the original initial and tail indexing agrees.

- **BNV3**: Every opposite-sign interval contains an adjacent sign change; positive telescoping proves the exact all-pairs condition.

- **BNV4**: Tail coordinates are raised in the required order. All endpoints preserve the lattice/gap and every upward excluded equality is avoided.

- **BNV5**: The reversed initial-block order preserves strict decrease; the split j<=i/j>i check proves the exact downward exclusion.

- **BNV6**: The finite number of unit moves and zero-length cases give the complete original WalkStatement for every step-closed predicate.

- **BNV7**: The displayed cubic estimates dominate all three original hNeed terms and StepGap. No source parity or rank guard is removed.

- **BNV8**: The compact root half-sums give the exact initial U(k) highest weight; remaining gaps grow linearly with t and all lattice conditions are retained.

- **BNV9**: Lagrange interpolation gives the signed moment identities. The Vandermonde basis is nondegenerate and the half-Gram correction constructs the exact isotropic dual frame, also at r=0.

- **BNV10**: The H-self-adjoint block calculation removes all unused trace entries. c_a(t)=-2it gives the exact original character, including its sign and factor two, with fixed Cayley and WCols.

- **BNV11**: Finite logarithm and exponential are inverse on the original nilpotent flag algebra. Lower-central coordinates give Jacobian one for BCH translations and the exact prescribed additive-Haar pushforward.

- **BNV12**: Unipotent trace n and polar singular values give the global norm bound. The finite logarithm converts it to small-s quadratic and large-s linear bounds, including the compact zero-algebra case.

- **BNV13**: The Casimir cancellation was independently checked against DC8. It yields uniform noncompact lowering bounds; commutators then give all original centered estimates for arbitrary real t>=1 and arbitrary d.

- **BNV14**: Conjugation moves the lowering operator to the highest side. The Taylor residual and centered-action bounds are O(t^-1/2) after differentiation; the phase is purely imaginary. The resulting scalar ODE proves uniformity in the representation.

- **BNV15**: Positive real part permits a real linear diagonalization of the complex Gaussian. The right-half-plane square-root formula and nonzero Haar scalar prove nonvanishing, including dimension zero.

- **BNV16**: The corrected statement has a single eventual bound before all integration variables. A fixed integrable scaled majorant proves positivity of Re B and dominated convergence. AE-strong measurability is sufficient because positive dilations are nonsingular.

- **BNV17**: The corrected statement matches the source arbitrary ambient sigma-finite measure. Zero extension off the closed group preserves compact equivariance and measurability; the original phase has norm one on all matrices. Schur averaging yields exactly 1/dim(Vpi).

- **BNV18**: The actual coefficient identity, uniform dimension-free DC6 estimate, fixed Cayley phase and Gaussian limit give the whole StepIBase endpoint. The original r=0 and k=1 cases are included.

- **BNV19**: The Gaussian/exponential bound converts to a reciprocal Frobenius power above the exact IntS threshold. Absolute Bochner convergence holds for every original translation and Haar pair.

- **BNV20**: The explicit Levi matrix normalizes N, maps the compact stabilizer and matches every character coordinate before exponentiation. The positive middle frames preserve the same compact Harish-Chandra label.

- **BNV21**: The two free translates absorb arbitrary Cayley changes; explicit conjugation and Haar scalars handle all other data. Compact cyclicity expands any source vector into a finite combination using any target nonzero vector, with absolute convergence already proved.

- **BNV22**: Independent unitary Cayley witnesses are reconciled by compact inner conjugacy. DC13/DC11 identify the entire original lowest type; evaluation of the actual endomorphism integral on xi is the nonzero vector period.

- **BNV23**: The unit-shift StepStatement remains an explicit producer. IntS, the base, finite walk and universal return consume it without weakening the original BesselNVGap quantifiers. Forms0 is retained in the analytic setting.

No unresolved mathematical or original-scope defect remains in the reviewed snapshot. This review is not a Lean build, kernel replay, or proof of any retained original producer.
