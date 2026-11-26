# Independent review of WIS1–WIS26

**Verdict: PASS at the stated original scopes.**

Reviewer: `geometry_alltest`, independent of the author. Accepted source commit:
`7cbf7a0c32fca1badf05931879a37c3f8a2b03b4`.
Final proof SHA256: `b8a0a01360ca62dfb41866260c57044889110735718f6b64a7b89d8506e261fa`.

I read all 26 human proof blocks and compared the original declarations, actual ring/map definitions and principal producer bodies. I independently checked every source snapshot against its pinned git blob, every cited range hash, all 26 proof-block hashes, and the inherited WLD26 binding. This is a mathematical and scope review; formal correctness is accepted and no Lean replay was attempted.

## Main mathematical checks

The finite-field coefficient argument in WIS1 correctly uses a trace-dual lattice to prove finiteness before applying the ordinary PID and DVR criteria. Finite freeness and the relation p=u varpi^e justify the two required complete, separated filtrations. WIS2–5 then establish the actual Witt and tensor facts coordinatewise; they do not assume that the coefficient tensor ring is a domain.

The determinant shortcut in WIS6 is sufficient. For z in Jac(D), det(1-z M_b)=1+zq is a unit. The adjugate inverse, evaluated at the algebra identity, supplies an actual inverse of 1-zb in C. The result proves precisely the Jacobson property required in the embedding theorem. It neither uses nor claims the stronger mu_s-adic completeness theorem.

The abstract embedding proof has no injectivity circularity. The Frobenius cycle keeps every component idempotent nonzero. WIS10 proves regularity of t_W from p-torsion-freeness. WIS11–12 cancel only that proved regular element or actual units, and WIS13 derives injectivity afterward. The maximal-ideal proof of unit reflection uses the dichotomy with the correct branch directions.

The crucial residual assertion in WIS15 is proved. When the leading exponent k_i is below m, the parenthesized factor in WIS.23 is the image of a unit of B because g(pi) is in Jac(B). This excludes that case. After the integral digit has been removed, multiplying the residual equation by u t^(e-1) makes its right side p f(x-prime), so the proved p-saturation of c(B) keeps the next residual integral. WIS16 can therefore iterate. Its final limit argument uses only algebraic preservation of p-power congruences, without a new continuity premise on j.

The actual endpoint WIS18 retains the supplied Good, Gamma, WSer, WIo and IoW data. The precision-one density, saturation, Frobenius ties and io_pi equality are the original record fields. All four clauses of ioE_injective_saturated_inter are supplied, rather than only the two immediately used for lattice existence.

The fixed-subring arguments retain arbitrary sets H. The Galois action fixes the O basis, so WIS21's Teichmuller lift is truly fixed in every coordinate. The p-adic fixedness argument needs only preservation of literal p-power divisibility. It does not rely on a compactness, finite-group or continuity assumption on H.

WIS22 is uniform in every original s>=0. The exponent p^(s+r) kills the rth coordinate of tau=epsilon_s-1 by the original cyclotomic identities. Stabilized finite coordinate sums are compatible under Frobenius. The separately constructed tail sum establishes actual tau^m divisibility and gives the complete original separation/summation result.

WIS23–25 preserve the genuine approximation subgroups pi^m c(B)+pW. Replacing c(B) by W would destroy this filtration when pi is a unit; the manuscript explicitly avoids that error. The coordinate criteria are proved in both directions, shifted summation retains every m and k, and the fixed-subring correction changes the approximate limit only by pW. The hypothesis pi in W^H is retained precisely where required.

## One resolved scope clarification

I requested that WIS26 explicitly retain the original LocTied(p,P,AI), and hence the IsStd instance used by the Bhatt–Scholze realization clause. Good and the supplied Gamma/R/I records alone do not state that premise. The author added it to the statement and corresponding metadata before the final hash above. This is a clarification of the inherited WLD26 scope, not a third remaining period-ring supplier. No unresolved finding remains.

## Exact remaining boundary

WIS26 now consumes the complete inclusion theorem while retaining the actual Wach prism and the homogeneous cyclotomic-kernel-fixed Frobenius matrix-solution descent as the two period-ring suppliers. The original crystalline-realization premise, tied period data and supplied etale records remain. The chapter does not assert the matrix theorem, actual prism, FaithH, EtBasis, Herr-class comparison or a whole selected RH/GRH closure.

## Evidence binding

The accompanying JSON binds all 26 claim blocks individually, all 20 primary source files and 22 exact source ranges, and WLD26. Each source file was independently compared with the accepted pinned git blob. No proof or author metadata was edited by the reviewer; only these review files were written.
