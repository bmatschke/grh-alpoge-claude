# Independent targeted review: OB5

**Result: PASS.** Reviewer `/root/core_closure`; author `/root/analytic_closure`; date 2026-11-22. No changes requested.

Reviewed `odd_minus_bounds/main.tex` at SHA-256 `1cf2ac7b6d471ccbf594b1fe5c57fd554679e0d520e5c57df3d3478df3907f1b`, specifically OB5, lines 471–634, proof-range SHA-256 `aa4049befbf48dcd2dca19b6ed573953e93d61d18fb7c5cf7cc013c5a2e78695`. The OS1 dependency used in the join was read at `odd_minus_supplier/main.tex` SHA-256 `d84beec71cba025a3303be52ab11e0f03ca95a533a3ed333ae401b20bdd47a84`; its OS1 proof-range hash is `864c87ff9114ef87b5cd4939bcb37c15ed917df7f26238684c4897e709c03dff`.

## Bernoulli approximation and the exact original group-ring action

Expanding the first two Bernoulli terms gives the displayed coefficient `(a-1)/2 - j_L(b)`. In particular the sign of `j_L(b)` is negative: the kth-power difference contributes `-b^(k-1) j_L(b)`, while the next Bernoulli term contributes `(a-1)b^(k-1)/2`. The remaining terms lie in `L/(2kP_k)` times the integers. Summing cannot lower the common ell-adic divisibility. The distribution identity applies to every lift of each unit because ell divides R, and its powers of the extension degree cancel against the factor in `E_{L,k}`. Thus the same rational y is approximated coefficientwise, giving a single integral z independent of the class x.

The source `sumEl` inserts an inverse in its group element; the source argument `(piQ rho)^(-1)` cancels that inverse. Consequently the positive `[pi(b)]` in the chapter and the displayed approximating element are the exact source conventions, after OB1's identification of the actual quotient with the restriction image.

## A finite class character from the original Sha class

The cocycle has finite image because its profinite domain is compact and the coefficient module is discrete. Choose one common ell-power exponent that also kills the finitely many local coboundary witnesses at the source's selected ell-adic places. At a sufficiently high cyclotomic level, the coefficient action on all those values is trivial. The restricted cocycle is then a homomorphism, and its restriction to every ell-adic decomposition group vanishes. Conjugate places cause no gap: the additional cocycle-conjugation term is multiplied by `1-chi(g)^(-e)`, which kills the same bounded values. Away from ell, the original unramified-outside-S quotient already kills inertia.

The finite cyclotomic field is totally complex, so ordinary unramified class-field reciprocity applies without an infinite-place modification. The exact classical use is independently supported by [Milne, Class Field Theory, V, Theorem 3.6 and Example 3.9](https://www.jmilne.org/math/CourseNotes/CFT.pdf). Artin equivariance follows by conjugating Frobenius and preserves the inverse conjugation convention needed here.

## The OS1 join, including its factor of two

At a level L greater than a, with a a unit, the OS1 coefficient is `theta(t)=2 floor(at/L)-(a-1)`. Set b=at mod L and take b'=t. Then `2E1(b)=-theta(t)` and `sigma_b^(-1)=sigma_a^(-1)sigma_t^(-1)`. Therefore

`2 sum_b E1(b) sigma_b^(-1) = -sigma_a^(-1) sum_t theta(t) sigma_t^(-1)`.

OS1 gives a principal ideal for the right-hand annihilator on every ideal class. Evaluation by the class-group character therefore kills twice the required sum. Cancelling two is valid because its values have odd ell-power order. This proves the exact OB.22 on the finite level, with no independent Stickelberger annihilation theorem retained.

For v in the common infinite cyclotomic kernel and the R-root kernel, every relevant lift acts on the original cohomology class by the negative cyclotomic scalar times `f(sigma_b^(-1) v sigma_b)`. The source scalar is `chi(sigma_b)^(-e)`. At high enough level, `b^e chi(sigma_b)^(-e)` is one on the bounded values, so the approximation cancels the twist in the needed direction. The same exponent kills x and hence allows z_m to be replaced by z. No tensor or character convention is being switched implicitly.

## Restriction injectivity and the remaining finite factor

The cyclotomic quotient over a number field is an infinite open subgroup of `Z_ell^*`. For odd ell it is procyclic. A topological generator has a nontrivial negative e-th power because e is positive and the generator has infinite order. Multiplication by its scalar minus one is surjective on `Q_ell/Z_ell`; one coboundary therefore matches any continuous cocycle on the generator, and density makes the remaining cocycle zero. Inflation–restriction gives precisely the required injectivity on H1. Inflation from the source unramified quotient to the absolute group is injective as well.

The restriction of zx is an additive character and is zero on the R-root kernel. The remaining quotient embeds in `(Z/R)^*`; its exponent divides phi(R). Multiplying by phi(R), then using injectivity, proves OB.19. This proves annihilation uniformly for every x by the single z. It does not assert finiteness of any infinite-level class group.

## Provenance and scope

All **15** source ranges attached to OB5, from **12** files, were independently checked against their range hashes, lengths, full-file hashes and pinned Git blobs at `7cbf7a0c32fca1badf05931879a37c3f8a2b03b4`. The full chapter and OB5 proof hashes agree with the frozen provenance. The literal `qzTw`, `Sha`, `actRep`, `sumEl`, `yEl`, `ytEl`, `zKill`, `resKill` and `totKill` conventions were inspected.

This is a targeted independent review of OB5 and its use of the already reconstructed OS1 annihilator, not a fresh review of all OS1 distribution arguments or OB1–OB8. The parent review covers that wider scope. No Lean kernel replay or full Lean build was performed.
