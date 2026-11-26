# Independent review of the rational graph calculation

Reviewed TeX SHA-256: `98287c24095cf4241e8b464c28bcfd0451bc57fd097161a385b0502c277766a8`.

I checked the block identities of E76Q1 against the pinned graph matrix and MapConjInv. Multiplying its four blocks gives the two denominators and the numerator for the stated left and right projections. The mixed matrix commutes with the signature projection because its two off-diagonal blocks pair distinct frame and inverse-frame coordinates. In the Gaussian identity the order of multiplication matters. Using Q* = Q' − 2iYC*, the left term becomes Y^{-1} − 2i C*(Q')^{-1}, and QC* = CQ' gives the required cancellation. For the determinant, elimination produces det(g) = det(A−WC) det(Q), and (A−WC)Q' = 1 follows immediately from CD*=DC* and AD*−BC*=1. This verifies the determinant orientation.

I checked E76Q2–E76Q3 against the ordinary period action and EisensteinSeriesTermUnitaryGraph. The real elliptic variables after the invertible frame changes separate the individual rational Fourier coefficients, with the nonzero Gaussian at a fixed period. In the second slot the theta product is antilinear, giving the conjugated multiplier in the graph coefficient. This argument uses the doubled product and its Heisenberg law for the actual finite tests; D76K1–D76K3 supply those premises.
