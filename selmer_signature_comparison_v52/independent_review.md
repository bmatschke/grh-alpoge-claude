# Independent mathematical review of SSC1–SSC17

**Result: PASS.** Reviewer: /root/arithmetic_common_frame. Author: root.
The reviewed proof file is selmer_signature_comparison_v52/main.tex, SHA256
bffbd3642816c573be20fdcafdc9d0253b1b7a66787c8402412000ada8c45b94.
The source commit is 7cbf7a0c32fca1badf05931879a37c3f8a2b03b4.

I read all seventeen human proof blocks and checked their mathematical arguments
against the original source contracts. I separately checked all thirty-two
source snapshots and thirty-two cited ranges against the pinned Git blobs,
all seventeen numbered proof ranges, and all eight inherited DFD proof blocks
and their parent provenance bindings. This is a review of the human
reconstruction and its scope, without a Lean replay.

## Principal conclusions

The packet supplies the full original Selmer-signature comparison on the actual
representation family. Its integral conjugacy argument works over an arbitrary
commutative local ring. Its comparison of coefficient DVRs allows arbitrary
injective local maps, without imposing finite generation or completeness on
the extension. The local-condition argument respects the original order:
span the pushed allowed cocycles, intersect with the continuous cocycles, then
pass to cohomology. It retains the original lattices, local embeddings,
characters and bad sets.

The final join supplies the actual SignatureChoiceCondition under the
original JointSix.main hypotheses. SSC17 consequently removes the signature
supplier retained in DFD15. It remains conditional on a coherent actual
HWOf, FonOf, and CmpOf construction. Neither the whole original
exists_setup_large producer nor the global denominator frontier leaf is
declared closed.

## Checks by claim

| Claim | Mathematical and scope checks |
|---|---|
| SSC1 | Residual absolute irreducibility supplies a matrix basis by density and a unit determinant. The group-algebra argument proves that trace equality identifies the two algebra maps, and the explicit matrix-unit construction gives an invertible integral intertwiner. The zero-rank case is separated. No DVR, completeness, or irreducibility of the second representation has been inserted. |
| SSC2 | The rational splitting gives the trace identity without asserting an integral direct-sum splitting. The character block and Speh normalization use the same parameter list and the correct exponent of the norm. Chebotarev extends equality in the original nonarchimedean coefficient field. The inverse of the intertwiner has the required orientation after the prescribed character twist. |
| SSC3 | Equality of valuation rings is converted to equality of rational-linear kernels using the clopen unit-ball condition and density. Algebraically closed image density makes the bridge conjugacy exact. The period-ring witness is transported by the tensor of the coefficient map and the field automorphism. The scalar compatibility with the original copy of the local integers follows from approximation and separatedness. |
| SSC4 | The coefficient extension uses integral basis coordinates. In the full source scope the matrix homomorphism need not be continuous. The corrected proof keeps the continuous crystalline cocycle and the rational boundary vector separate; it does not assert continuity of the rational coboundary. Each coordinate preserves the literal pair of witnesses, and continuity of the quotient coordinate map gives the required continuous quotient cocycle. Integral conjugacy likewise preserves the separate witnesses. The actual local bridge and bad-set identities give the original Selmer equality. |
| SSC5 | A possibly infinite residue basis lifts to compatible bases modulo every power of the source uniformizer. Generation and independence are proved by finite induction. Locality makes denominators from the source cofinal in the target valuation, giving the required direct-sum description of the torsion quotient. No finiteness or completeness assumption is hidden here. |
| SSC6 | Compactness and discreteness make each continuous cocycle have finite image and hence finite coordinate support. The proof transports boundaries, restrictions and the actual local spans. In particular, a target coefficient multiplying a pushed cocycle can be expanded modulo one annihilator, so all its coordinates remain in the original allowed span. Tensor identification and DVR flatness give the Selmer base change. Finite lengths scale by the ramification factor; the infinite-length case and the source's zero-denominator conventions are treated separately. |
| SSC7 | Same-character polynomial relations identify the common image ring and fraction field. Intersecting with the first valuation ring gives a DVR that embeds into the second: integrality descends through the shared relations and the second DVR is integrally closed. Both coefficient maps are local, and the common character has its actual values in this ring. |
| SSC8 | The two arbitrary coefficient extensions are compared through the common DVR. Same-character relations preserve local triviality exactly, and the actual index and coefficient-map transports are retained. Normalized lengths therefore agree, including infinite length. |
| SSC9 | The two quotient-lattice presentations are identified equivariantly. At the actual continuous lattice representation a rational boundary may be absorbed into the crystalline lift. Integral corrections give the required bridge lifts, with no claim that arbitrary chosen representatives are continuous. The fraction witnesses transport through both original bridges, yielding the local-condition inclusion and the full Selmer injection. |
| SSC10 | The proof distinguishes the rational normalized length from extended nonnegative division. It handles infinite numerators before division and the degenerate denominator convention explicitly. At the actual locations the denominator is positive and finite. The resulting inequality is the original unconditional comparison, with the infinite signature-length case treated directly. |
| SSC11 | The good-row and triple data select one signature with all required side, attachment and length properties. The same representation, first character, family indices and coefficient map are used throughout. All five original SelCore fields hold on the actual point family. |
| SSC12 | Equality of the places is turned into equivalence of all divisibility comparisons between powers of the chosen element and the rational prime. This gives the exact cross-multiplied normalized valuation identity. The zero-element and infinite-length-to-natural conventions are respected, as is scaling under a local coefficient extension. |
| SSC13 | The fixed-power argument on wild inertia uses the nonarchimedean estimate and a power invertible at the place. The original prime-power order of the character is retained. The tame generator and wild inertia give the precise cyclic image, and the principal-ideal divisibility proves the conductor infimum. The inverse character gives the same value because the two differences from one differ by a unit. |
| SSC14 | The relevant auxiliary place lies outside the bad set and the coefficient prime, so the first twist is unramified there. The same NChTie character and its two embeddings identify the normalized root values. Both orientation choices use the preceding inverse-character argument, yielding the exact summed tame-conductor bound. |
| SSC15 | The rational splitting identity descends to the original integral characteristic polynomial, then reduces using the actual Hecke tie. The residual hypothesis supplies irreducibility over the stated algebraically closed field. Passing to the algebraic closure of the original residue field preserves nonzero proper invariant subspaces, proving absolute irreducibility for every actual good-point lattice. |
| SSC16 | The original Chebotarev, point-family, coefficient tie, good-triple, same-twist, good-row and residual-irreducibility premises are all retained. The signature side equals the same Boolean used in the twist, so the two applications of psiAt cancel on that one character. The two Selmer conclusions and the conductor estimate give the full original JointSix.main. The actual twist-killing bound remains the squared-prime budget from DFD11. |
| SSC17 | The cutoff is chosen before the scale, its witness, location, finiteness witness and arbitrary finite exceptional subset. The actual hub and point family from DFD9 carry the new signature supplier. All previous setup fields remain on this same family. The coherent Wach functor and comparison are explicitly retained as the sole extra supplier in this conditional reduction. |

## Findings resolved before approval

Two findings were reported to the author and corrected in the reviewed file.

1. The introductory normalized-length formula had a malformed denominator.
   It is now an actual fraction with both length operators and the subsequent
   explanation of the source's natural-number convention.
2. The former wording in SSC4 absorbed a rational coboundary into a continuous
   crystalline lift. The full original coefficient-comparison statement does
   not assume continuity of the matrix homomorphism, so that absorption was
   not justified at its complete scope. The final proof instead transports
   the continuous crystalline part and the rational boundary vector separately.
   It derives continuity only for the quotient cocycle, where it is available.
   This resolves the scope issue without restricting the theorem or adding
   a premise. The later absorption in SSC9 is valid because that claim uses
   the actual continuous lattice representation.

There are no unresolved mathematical, source-scope, or binding findings.

## Preserved boundaries

The original arithmetic and geometric entry assumptions of the datum,
Chebotarev, the actual supplied local period-ring data, and the original
family premises remain as stated. Standard finite-dimensional density,
linear algebra, elementary DVR module theory, extension of algebraic field
embeddings, and the ordinary field-theoretic properties used in the proofs
are retained at their stated scope.

The packet proves the original signature supplier, not a replacement on a
different family or with different local conditions. It does not construct
the coherent Wach data, does not supply all local row estimates or all
ConclF fields, and does not close a selected global frontier leaf.

The standalone two-pass draft TeX validation is bound to the reviewed proof
hash and reports no overfull box, missing character, undefined reference or
LaTeX error. The accompanying JSON binds every reviewed numbered block,
source range, and inherited human input.
