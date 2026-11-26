# Independent review of AQ1–AQ5

**Result: PASS.** No further changes required.

Reviewed text: `analytic_envelope.tex`

SHA-256: `71df803d44f5fc658f81d6a414c88ea9d94bac8c89f43434de650f3dcf0fdb5c`.

Pinned source: `7cbf7a0c32fca1badf05931879a37c3f8a2b03b4`.

The review checks the complete analytic implication in its stated conditional scope. It does not certify existence of the arithmetic envelope windows. One endpoint wording precision edit was applied before the reviewed hash: for each x in the shrunken interval, the source integer bounds are applied at floor(x) and floor(x)+1.

## AQ1

PASS: Since H is continuous and locally a finite ramp sum, g_+ is locally integrable. Every nonnegative envelope dominating g dominates g_+, and choosing R=g_+ gives the converse. Fixed lower thresholds follow from the universally quantified starting threshold. Substitution x=exp(u) gives the exact x^(-theta-1) weight.

Claim SHA-256: `9e818c8165daa6573b26fbd264a6abf8ea42258e09d2337ba935f12c228f2bcc`.

## AQ2

PASS: The two exponential tilts give denominators sigma+h-2 and sigma-h-2. Multiplying by sigma^k, the lower tail uses k>=kappa U and the upper tail k<=kappa U+1, whose extra factor is fixed. With (m-1)h=(1+d-m)h=4m and sigma=(h+2)^2+3, both exponents are <=-m. The constants depend only on fixed delta, including arbitrarily small positive delta.

Claim SHA-256: `b3756fbf8be02003350120410d88215994952c98994d825453bc55b0287c26fe`.

## AQ3

PASS: The inequality |A_k(sigma+it)|+A_k(sigma)<=2 integral g_+ w follows from real g and nonnegative w. The positive-window integral, exponential-series bound and AQ2 give the displayed estimate uniformly in t. If a horizontal pole distance is below D, a small generic change of t yields a unique nearest pole and an analytic remainder at a larger radius r<D. Otherwise an attained nearest pole is real, unique and has positive residue, so A_k(sigma)>0 eventually. Eta is chosen after the fixed radii but before arbitrarily late windows, making B>r. Both cases force incompatible exponential rates. The principal pole is canceled by the centering and coincident zero residues have positive weighted multiplicities.

Claim SHA-256: `73e89b859718f24aff8dee69f0e5b91067cf50c05b15fc3663e04bcf4bba1c90`.

## AQ4

PASS: A sequence of theta decreasing to one half excludes each individual right-hand zero. The family and positive stretch are fixed before eta and the window. Functional equations and imprimitive Euler factors give exactly the inherited Dirichlet-GRH scope; principal psi alone gives RH. The analytic result supplies no arithmetic envelopes.

Claim SHA-256: `d79408378dc4a7fc61a8e039411d677dc8bdcc7be6e68e06524df3deab7a3043`.

## AQ5

PASS: Original H has principal coefficient one, so on each open unit interval H_double_prime=-1/x. Concavity gives nonnegative interpolation error; subtracting the quadratic majorant gives a convex zero-boundary function and error <=1/(8n). Concavity of x^theta yields the endpoint transfer. The final floor(x),floor(x)+1 formulation checks both integer endpoints after shrinking a lambda-window to a fixed mu-window.

Claim SHA-256: `fee6d74156a00f462ebc2232de5b0c5ccea5d4bb9e4db9138e87d9cfecce4ce7`.

All 15 cited source ranges in 10 source files were checked directly against the pinned Git objects and checkout. No new numerical tests or Lean compilation were performed.
