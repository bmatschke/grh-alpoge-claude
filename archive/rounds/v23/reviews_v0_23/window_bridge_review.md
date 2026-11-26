# Independent review: character balance and arithmetic-window bridge

Reviewer: `/root/dependency_audit`. Result: **PASS**.

Reviewed `window_bridge/main.tex`, SHA-256 `d122001e64bfc2d52237b1db4d1768a01dd0f016f34b444da563e62ac7dd492c`.

## WB1

Primitive-character reading includes ramified primes. CRT shows that triviality on the full p-power unit factor is exactly absence of p from the primitive conductor. Actual surjectivity gives injectivity of primitive reading. The principal ramp is now explicitly defined for all positive arguments.

## WB2

The finite character-balance identity has the correct logarithmic-derivative sign. Host hypotheses give exactly two unramified contributions and one ramified d contribution; the d>N case is handled by the empty sum.

## WB3

The even/odd binomial proof gives theta(y)<=y log(4); summing prime powers gives psi(y)<3y. The factorial estimate for positive integers yields the stated harmonic Lambda bound. The centered derivative bounds and exact 3a/min(w) Lipschitz constant hold, including positive ratios below 1.

## WB4

Averaging over the actual subgroup kills exactly the nonquotient characters and selected-set shifts. The surviving coefficient is bd2/2 with no extra subgroup cardinality. The thin ratio and total averaging error 2Q/x have the correct factors.

## WB5

The quotient family has fixed size 4o. Fourier bias 3:4 gives c=(3o+1)^(-1); the target-dependent error O(x^epsilon log x+log x) is uniformly little-o of x^(1/2+epsilon) for fixed positive epsilon, independently of growing host.

## WB6

SC1 uses the exact gain Qd2/2, yielding final exponent eD+eL+7. The cyclic psK=none condition excludes the unwanted quadratic character, so the sole retained character trivial on A is principal and has weight one.

## WB7

The source-compatible gap contract retains all actual fields, maps, orbit coverage, primitive identifications and arithmetic gain inequalities. Unpacking the record is not used to supply geometric existence or estimates.

## WB8

C and the positive epsilon range precede epsilon and every window. Taking 0<delta<1/2 fits AN3 directly. The fixed positive family is unchanged. The principal pole, Euler factors for imprimitive characters, functional equation, and ordinary RH specialization are scoped correctly.

The original arithmetic gap and same-object family supplier remain retained assumptions. This review checks the complete conditional bridge, not those upstream existence or geometric estimates. It does not replay the Lean kernel.
