# Independent mathematical review: NFR1–NFR13

Reviewer: root. Author: geometry_alltest. Result: PASS at the exact written scope.

The whole proof text and the original ModelsOf, ModelBase, ThetaData, IsThetaPt, IsNormUn, FrameOK and FramesOK contracts were read independently. This review checks the human argument; source hashing is a separate provenance check.

## NFR1

The first-linear Hermitian convention is followed throughout. Positive columns use conjugated coordinates and negative dual rows use unconjugated coordinates, giving exactly the original relab/perFr dictionary and host multiplicities.

## NFR2

The Q block matrix and trace with minus xi0 give the positive Hermitian form with the original alternating-form sign. Orthogonalization identifies the domain with the connected indefinite unitary group and positive triangular factors. Actual period entries are holomorphic; the separate onto clause is not asserted.

## NFR3

The polynomial w squared equals w minus 2m gives an idempotent w to the fourth power modulo eight whose adjoint is its complement. The two summands are complementary Lagrangians. Elementary symplectic shears, including the explicit unit diagonal factorization, lift the prescribed basis integrally.

## NFR4

Riemann relations produce h and tau on the same ordered lattice. Inherited HUF20 gives one pair of half characteristics on the connected domain and the actual algebraic section and zero-rigidified frame. Every original ThetaData field is accounted for.

## NFR5

Normal convergence gives holomorphy. Nonzero Fourier coefficients prove nonvanishing; the recurrence under the second lattice generators leaves one scalar parameter. This proves the complex section line directly and does not import SecTwistSt or SecBaseChangeSt.

## NFR6

The nonzero determinant multiplier has an actual pointwise square root. Scaling the same algebraic section and differentiating the same exponential produces the required ordered tangent eigenbasis. IsThetaPt and IsNormUn have their literal original data.

## NFR7

The normalized periods and Riemann relations give H = transpose(h) times inverse(Im tau) times conjugate(h). Determinants give det(H) det(Im tau) = absolute(det h) squared, with all factors positive.

## NFR8

Unit signed principal minors fix each Hermitian block determinant. Multiplication over the actual CM type yields the exact product of 2 absolute(type xi0), rather than an unspecified positive constant.

## NFR9

An actual half-open lattice parallelepiped is a fundamental domain. Orthogonality in the first torus variable and tiling in the second give the Gaussian theta mean 1 divided by sqrt(2 to the g times det(Im tau)); the zero-dimensional convention is consistent.

## NFR10

The quadratic holomorphic gauge gives the exact unit semicharacter and Gaussian weight. Scalar readings remain those of the actual section in the rescaled frame; the zero rigidification is preserved.

## NFR11

The normConst factor and exact Hermitian determinant cancel the Gaussian denominator and leave mean exactly one. Only the squared modulus of the chosen square root occurs, so its arbitrary sign has no effect.

## NFR12

The actual isomorphism, exponential, tangent basis, section generator, multiplier, weight and normalized mean supply every original FrameOK clause. The direct Fourier argument is sufficient for the section-generator field.

## NFR13

Choice on the finite supplied family gives all normalized points simultaneously and exactly the first FramesOK field. FromTest uses TDR13 only with its original SecBaseChangeSt premise. The three other FramesOK fields, CoverTri, FibTri and complete IsUnf remain explicit.

## Scope and verification

The source commit is 7cbf7a0c32fca1badf05931879a37c3f8a2b03b4. All 31 pinned source files and 31 ranges, the full proof file, 13 claim blocks and six inherited proof blocks were checked byte-for-byte. The supplied Moduli and the original inherited foundations remain. NFR1–NFR12 do not require a new section-base-change premise; the FromTest conclusion in NFR13 retains it. No full FramesOK, IsUnf, hasPrinc or whole selected obligation is inferred. There are no unresolved findings.
