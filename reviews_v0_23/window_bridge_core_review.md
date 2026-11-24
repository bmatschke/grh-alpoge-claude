# Independent review of WB1–WB8

Reviewer: `/root/core_closure`  
Author: `/root`  
Result: **PASS**, after the three precision corrections already incorporated.  
Reviewed SHA256: `d122001e64bfc2d52237b1db4d1768a01dd0f016f34b444da563e62ac7dd492c`

This review checks the finite Fourier identity, primitive values at ramified primes, exact weighted Lipschitz constant, averaging normalization, scalar exponent arithmetic, and use of the terminal analytic criterion. It does not prove the open arithmetic contract or perform a Lean replay.

## WB1 — pass

- Finite Fourier normalization is |G|/f=2; averaging over inertia gives 2/|I_p| on the Frobenius coset. There is at most one matching inertia element.
- CRT argument identifies primitive values even at primes dividing the ambient modulus. Nontrivial inertia character is equivalent to p dividing the primitive conductor.
- Primitive-inducer injectivity follows by inducing to the same positive modulus then using surjectivity of the reciprocity map. Actual logarithmic derivatives are retained.

## WB2 — pass

- At p in S the Frobenius/inertia coset lies wholly in Phi, so there is no contribution. At d the inertia group has size two and its coset has exactly one member outside Phi, giving coefficient one.
- The cutoff N bounds a/w at every Phi point; all p^j>N contributions vanish. The infinite notation equals the finite source ASK including d>N.
- The index-two coset sum is f for the trivial character and -f for chi_d. Therefore subtracting the linear ramp term produces +a ell_chi_d in MAIN. The bijection partner has the exact c_infinity and sign conventions.

## WB3 — pass after precision edits

- The even/odd binomial induction proves theta(y)<=y log4, including the odd central-binomial bound since its two central coefficients are equal. Summing powers gives Psi(y)<3y from log4+4/e<3.
- The factorial identity gives the stated Mertens bounds for positive integer k, now stated explicitly. Floors cost at most log2 in the derivative comparison. C0=6+|gamma| is sufficient.
- For nonprincipal ramps a ell cancels in the weighted difference. The positive part is 1-Lipschitz and Psi(a/min(w,wprime)) yields constant 3.
- For the principal ramp the uncentered difference and a log(wprime/w) are nonnegative, with bounds 3a Delta/w and a Delta/w. Their difference has absolute value at most 3a Delta/w; summing their bounds would lose the exact constant.

## WB4 — pass

- Thin-point scale inequality follows from x>=3: (x-1)/(2x)>=1/3. Thick-point perturbation is at most 3(x+1)(eta+1).
- Counting f outside points and 2f characters then dividing by f gives 2f times the stated error bound. The two cost inequalities each contribute b/x.
- Averaging over A0 kills exactly the characters outside B. For the rest, s and u disappear and the surviving character is xi(e1(t)); no conjugation or sign is lost.
- The scalar coefficient is b|T2|/f=bd2/2, hence Qd2/2 after summing over t,j. There is no extra |A0| factor.

## WB5 — pass after precision edit

- Moving y_t to x costs one Lipschitz bound per bounded-quotient character. The bias error multiplies the crude O(x log x+x|ell|) bound and becomes O(x^epsilon log x), below x^(1/2+epsilon).
- epsilon>0 is now explicit, so all normalized errors tend to zero. Constants depend only on fixed target data, not growing host cardinalities.
- The 4:3 favored-coset density has nontrivial quotient Fourier coefficient 1/(3o+1); triangle inequality gives o errors and |B|=4o.

## WB6 — pass

- The four B/Q terms are bounded by 2Z,2Z,4Z,2Z, Z=x^(1/2+13epsilon/8), exactly as SC1.
- After dividing by Q/2, 4/x<=2x^(Cepsilon)Z for x>=3. Hence 20 becomes22 before division by d2, and the initial 4 yields26. The exponent is C+21/8; absorbing26 costs3epsilon/8.
- The primitive reading is injective and surjective onto the fixed powers. Excluding chi_q leaves only the principal character trivial on A among kept characters, so the weights match the fixed target exactly.
- The omitted sum has at most4o terms. Absorption at x^epsilon>=1+4o gives exponent C+4, and C=eD+eL+3 gives eD+eL+7.

## WB7 — pass

- Every arithmetic source premise remains an explicit same-data contract; the gap and family existence are not inferred from character algebra.
- IdentU retains exact maps, ledger main term, real logarithmic derivative and asked-sum equalities; coverage transfers the gap to every subgroup element.
- C is fixed before epsilon; K0 and CE are fixed before the moving windows. This is sufficient for all preceding thresholds.

## WB8 — pass relative to the already reconstructed analytic criterion

- Now chooses 0<delta<1/2, so theta=1/2+delta is in the established analytic range. Epsilon is chosen after delta and C, and the window then exceeds all fixed thresholds.
- The target family is fixed and all coefficients are positive. AN3 applies pointwise throughout each real window. This review checked the stored AN3 statement/proof use but did not repeat a separate literature audit of its classical analytic leaves.
- Euler factors are nonzero for Re(s)>0, primitive functional equations transfer left-strip zeros to the conjugate right half-plane, and the ordinary target recovers RH.
- Source ShapeWin passes eD=2,eL=0 into topDesWin, consistent with the conditional 1/2+9epsilon exponent.

## Conclusion

No unresolved mathematical or source-convention error was found in the reviewed scope. The chapter closes a substantive conditional chain from one explicit arithmetic contract to the fixed positive-character windows and the analytic RH/Dirichlet-GRH endpoint. The existence of that common arithmetic datum remains stated as an input.
