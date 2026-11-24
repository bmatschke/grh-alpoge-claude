# Independent review of TW1–TW8

**Outcome: PASS in the stated classical-input scope.**

Reviewer: `/root/core_closure`, independently of the author of this component.
Date: 2026-11-22.
Reviewed file: `simultaneous_cohomological_windows/main.tex`.
Frozen SHA256: `6ab57b5ec822e23aadd4798bba48fd2f42fb8c35c59609d30c7aabec53051af5`.
Pinned Lean commit: `7cbf7a0c32fca1badf05931879a37c3f8a2b03b4`.

The eight written proofs supply the literal statement

\[
\exists K:\mathrm{BConst}\quad\forall C_t\ge1,\quad
\mathrm{ThmBab}(K,C_t),
\]

using KB8, LD3, LK2–LK3 and the four expressly named classical inputs. The proof includes the translation from classical Ferrero–Washington to the exact source rank interface; the two-primary bound uniform in the varying prime pair; strict infinite-tower descent; finite-to-compact Poitou–Tate passage; the actual `ABound` and `SecondBound`; the exceptional-twist and common-window argument; and transport to every original field, closure and local-data record. No additional bespoke supplier is hidden inside those steps. This review does not assert closure of `PointHV`, the remaining count predicates, the geometric/arithmetic branches, RH or GRH.

## Review method and source integrity

I read all eight mathematical proofs and compared the final conclusion and its quantifiers with the pinned definitions of `BConst`, `admitted`, `PrimePair`, `OddPrimesWithRootsOfUnity`, `BaAt`, `BbAt`, `IsBWindow`, `BShape` and `ThmBab` in `PrimeSetBoundDataOfPrimitiveChar.lean`. I also checked the exact interfaces `ABound`, `SecondBound`, `FirstBound`, `VVat`, and their layer and local-data conventions. The independent byte verification recomputed every written proof-range hash, every source range and its first line, every referenced file hash, and equality with the pinned Git blob: **8 proof ranges, 100 source links, 62 source files, no failures**. The result is recorded in `simultaneous_windows_source_validation.json`.

The provenance check is an identity check, not a substitute for the mathematical review and not a Lean kernel replay. The final component's own draft-mode TeX validation was inspected; the author reports two successful passes, ten pages, no overfull boxes and no missing glyphs. I did not request a PDF.

## TW1: all-prime Ferrero–Washington and finite-layer ranks

The root hypotheses make the full cyclotomic tower a genuine cyclotomic Z_l-extension: its image is an open subgroup of `1+l Z_l`, or of `1+4 Z_2` at two. This removes the possible two-torsion issue before applying the Iwasawa structure theorem. The unramified Iwasawa module is finitely generated torsion over the Iwasawa algebra. Ferrero–Washington removes its l-power factors; distinguished-polynomial factors are finite free over Z_l, and finite errors preserve finite generation over Z_l. The proof therefore supplies a finite generator bound, including any finite submodule, rather than only a rational rank bound.

The finite-layer consequence is proved, not assumed as an unspecified control theorem. In the local cyclotomic tower, the residue degrees over a fixed finite extension of Q_l are bounded and eventually constant. The local cyclotomic image is open, so the number of primes also eventually stabilizes. Thus the relevant upper layers are totally ramified at a fixed prime. Such a layer intersects the lower Hilbert class field only in the lower field; base change of that Hilbert class field stays unramified. Class-field reciprocity consequently makes the finite-layer norm maps surjective on the tail. Projection from the inverse limit then bounds the l-ranks of the tail class groups by the Z_l-generator count. Finitely many earlier layers cause only a finite enlargement. This supplies the exact finite-layer statement recorded by `Published.FerreroWashington`.

The accepted primary inputs were checked at their stated locations: Sharifi's Theorem 6.2.1 states the Ferrero–Washington theorem for every prime, including two; the later odd-prime restriction on a minus-part corollary does not restrict that theorem. Sharifi's Corollary 3.2.7 identifies the norm limit with the unramified Galois group, and Proposition 3.2.11 states finite generation and torsion. The structure theorem is Theorem 2.2.13 with Remark 2.2.11 and Lemma 2.2.12. Finite class-field reciprocity is already the exact classical leaf used in KB6. No size bound for class numbers is inferred merely from the uniform rank bound.

## TW2: uniform varying-prime ranks and the original host

The infinite two-primary base attached to the fixed abelian datum has a fixed residual character bound. The congruences on q and d give, respectively, at most `2o` and `4o` primes in that base tower. At either odd residue characteristic, the pro-two tame inertia supplies at most one F_2-character per prime and wild inertia supplies none. This yields the extra `6o` term before adjoining the two quadratic fields.

For a subgroup of index two, the restriction five-term sequence bounds invariant mod-two characters without a spurious extra dimension: the dimension-one `H^1(C_2,F_2)` kernel is compensated by at most the dimension-one `H^2(C_2,F_2)` term. In characteristic two, `(tau-1)^2=0`, so total dimension is at most twice invariant dimension. This argument also establishes finiteness before using a numerical dimension. Iterating twice gives the stated bound `4(g+6o)`, uniformly in q and d. The quadratic fields are unramified outside the already permitted places, so the subgroup argument applies inside the same maximal allowed extension.

The resulting compact pro-two abelian quotient has finite mod-two dimension. Compact Nakayama gives a finite Z_2 generating set; a finite-generation hypothesis has not been silently inserted. The comparison of every original `IsCompField` model E with the appropriate cyclotomic layer uses an extension of degree at most two. The restriction kernel on the strict negative-twist group has length at most one: its inflation group is the first cohomology of a cyclic group of order two on a cyclic two-primary module (or the divisible rank-one module). The source's extra one is retained. The argument transports the local conditions, not just the abstract field.

## TW3: strict tower descent and compact duality

The negative twist is tracked correctly. Over the infinite cyclotomic field it is trivial; after descent the character action is `u^{-k}` times inverse conjugation, and Pontryagin duality gives the positive-twist operator `u^k rho(gamma)` on the compact quotient X. Replacing that operator by its inverse does not change the image of its difference from one. Thus the displayed coinvariant formula has the correct sign and action convention.

For k at least one the scalar `u^{-k l^a}-1` is nonzero and acts surjectively on Q_l/Z_l. The procyclic `H^1` and `H^2` terms needed by inflation–restriction vanish. At places above l the local cyclotomic image is open, so the same scalar argument establishes the inverse preservation of strict local vanishing. Away from l the tower is unramified, and the entire inertia group already lies in the infinite-level group. The claimed equivalence of strict kernels and coinvariants therefore holds in both directions. It does not claim the corresponding statement for k equal to zero.

For the reference-layer comparison, the dual of `Z/l^r(k+1)` is exactly the finite subgroup of `(Q_l/Z_l)(-k)`. LD3 gives the finite strict `Sha^2`/`Sha^1` pairings. Their compatibility uses the same normalized Q/Z-valued cup-product invariants: coefficient reduction on the compact side is paired with coefficient inclusion on the torsion side. Arbitrarily chosen separate finite-level perfect pairings would not suffice; the text correctly avoids that shortcut.

Finite global and local `H^1` give Mittag–Leffler. Cochains are inverse limits with surjective transition maps, so compact `H^2` equals the inverse limit of finite `H^2`; kernels commute with that inverse limit. Discrete torsion cohomology commutes with the filtered union because every continuous cochain from a compact profinite domain has finite image; filtered colimits are exact and there are finitely many local terms. Duality then identifies the full strict torsion kernel with the dual of a submodule of the actual compact global `H^2`. This proves the required length inequality, including infinite lengths before KB8 is used.

The join to LK2–LK3 explicitly goes through the original decomposition group, its selected henselization, the completion, and a finite subfield of the specified p-adic algebraic closure. The root, cyclotomic-character, cochain, cup-product and localization compatibilities supplied in KB6 are preserved. The proof covers every original local-data record, not merely one chosen completion model.

## TW4: generator bounds, matrix lift and valuation centers

Reduction of the pro-l action on `X/lX` is unipotent, even when X has torsion. The specified `j_0=floor(log_l R)+3` is beyond the level needed to force the operator minus one into `l^2X`. The cyclotomic-sum operator then has cokernel of length at most R. The Nakayama argument is applied to a finitely generated quotient of X and is valid at l equal to two. Factoring successive operators proves the exact per-layer loss and the earlier-layer monotonicity.

Lifting the action to a matrix on a chosen Z_l^R surjection gives a surjection of cokernels. It does not require X to be free. Smith normal form bounds the quotient length by the determinant valuation; zero determinant is consistently assigned infinite valuation. Factoring that determinant over an algebraic extension causes no unwanted rationality assumption on its eigenvalues.

The p-adic ball argument produces centers in Z_l for every eigenvalue, without assuming it lies in the image of the cyclotomic exponential. Its pairwise-intersection estimate and compactness yield the stated bound. Summing the R inequalities, then applying TW3 at the reference layer, supplies both halves of the literal `ABound` and its exact `SecondBound`. The norm convention and the primitive-root exponent match the source.

## TW5–TW6: one interval and every field model

For a given center, there is at most one integer between 1 and Z whose valuation distance exceeds `floor(log_l Z)`; two would differ by a positive multiple of a larger power than Z. The exception budget is therefore R. The elementary induction on the number of bad logarithms yields the exact factor `2^(R+2)(C_t/eta)^R`. It is applied once to the union of the finite many constituent exception sets, producing one interval and one Y for the whole family. No choice is made separately for each point x.

The discriminant bound follows from the displayed cyclotomic modulus and the degree bound for the fixed reference layer. The prime-power totient inequality gives `l^b<=2n_0`, including b equal to zero. The resulting constants depend only on the fixed degree, conductor and layer index; in the two-primary family they are independent of q and d. Sharifi's equation (4.2.1) explicitly states the conductor–discriminant identity for an arbitrary abelian field, so the cited bound is correctly matched.

Field-model transport extends the prescribed base isomorphism to algebraic closures, preserves roots of unity and the unique prescribed cyclotomic layer, and pulls back continuous cocycles and the actual local conditions. This is sufficient for the universally quantified layer and local-data records. The reference fields are not conflated with the original host E.

## TW7–TW8: quantitative absorption and final quantifiers

KB8 gives finite actual compact `H^2` for every original datum and positive twist. Its logarithmic cardinality bound becomes a length bound with the factor two because `log l>1/2`. Exceptional twists are forced below `x^(epsilon/(2C_K))`; the reference discriminant contributes `x^(epsilon/4)`, giving exactly the exponent `3epsilon/4`. Nonexceptional twists use the logarithmic first bound. The reference comparison and layer-growth bound keep the same finite constant uniformly over the varying family.

The sole requested precision edit was to list l explicitly among TW7's fixed parameters, because `j_0` appears in its chosen constant. The author made that edit before freezing the reviewed hash. The fixed prime is two in the varying pair family and one of finitely many already fixed odd primes in the reference family, so this is exactly the uniformity needed by TW8.

The gap between `3epsilon/4` and `4epsilon/5` absorbs the polynomial number of twists and the logarithmic term after a threshold depending only on the stated fixed constants. Finiteness is established before taking the real-valued sums.

The construction of `BConst` occurs before every `C_t>=1`: R0 and R_l are functions of the fixed abelian data alone, and the same `C_K` is used throughout. For fixed M, B', L, epsilon, A1 and C_t, all thresholds are chosen before the admitted functions, X and the prime pair. The two-primary threshold is uniform in q,d. Each fixed odd-prime threshold transports to every model. Their finite maximum is raised to the common J before X is chosen.

The prime pair is then fixed, one union of exceptions gives one Y, and every x in `[Y,Y^2]` satisfies both the original-E and separately quantified reference-layer conclusions. The formulas for R, J, `j_0`, the size condition on `log(qd)`, and the entire quantifier order agree with the literal `ThmBab` definition. The proof uses KB8 only after the independent tower and reference comparison have been established, so there is no feedback from `ThmBab` into `LemmaK`.

## Remaining boundary

The reviewed chain is complete relative to its named classical leaves and the already reconstructed KB/LD/LK suppliers. It removes `ThmBab` as an unreconstructed input of the existing window/character assembly. It leaves `PointHV` and the other globally recorded branches outside its scope. The PASS judgment is for the fixed bytes and the explicitly stated endpoint; it is not a claim that all downstream RH/GRH dependencies have been discharged.

### Primary references independently checked

- Romyar Sharifi, *Iwasawa Theory*, [Theorem 6.2.1](https://math.ucla.edu/~sharifi/notes/iwasawa-ch06.html): all-prime Ferrero–Washington statement.
- Sharifi, [Corollary 3.2.7 and Proposition 3.2.11](https://math.ucla.edu/~sharifi/notes/iwasawa-ch03.html): norm-limit/Galois identification and finitely generated torsion Iwasawa module.
- Sharifi, [Theorem 2.2.13, Remark 2.2.11 and Lemma 2.2.12](https://math.ucla.edu/~sharifi/notes/iwasawa-ch02.html): structure theorem and finite errors.
- Sharifi, [equation (4.2.1)](https://math.ucla.edu/~sharifi/notes/iwasawa-ch04.html): abelian conductor–discriminant identity.
- J. S. Milne, [*Class Field Theory*](https://www.jmilne.org/math/CourseNotes/CFT.pdf), V, Theorem 3.6, Corollary 3.7 and Example 3.9: finite Hilbert class-field interpretation and reciprocity, also checked in the KB review.
