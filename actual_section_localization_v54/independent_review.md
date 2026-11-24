# Independent mathematical review of ASL1–ASL21

**Result: PASS.** Reviewer: `/root/arithmetic_common_frame`.

The reviewed main file has SHA-256
`598ffcead000aabb40672df843548733ab3a88509ace19b7eb5fb648b06a662e`.
All 21 numbered proofs were read against their original statements and
the relevant source bodies at accepted commit
`7cbf7a0c32fca1badf05931879a37c3f8a2b03b4`. All 34 source snapshots
were independently compared byte for byte with both the pinned Git
blobs and the read-only checkout; all 64 cited ranges were rehashed.
The five inherited proof blocks, their complete main-file hashes, and
their recorded provenance bindings were also checked. No Lean replay
was performed.

## Mathematical findings

The power-killing argument in ASL1 and ASL4–ASL5 has the original order
of quantifiers: a neighborhood and exponent are fixed before every
original chart index and smaller open. The global killing theorem uses
quasi-compactness alone. It does not insert quasi-separatedness where
the source does not require it.

ASL6–ASL7 correctly separate the first common exponent, which clears
denominators on finitely many affine charts, from the further common
exponent that kills the discrepancies on their quasi-compact overlaps.
The transition-unit shift identity proves agreement on the whole
overlap before gluing. It applies to every integer twist, including
negative twists, without cancelling a possibly zero-divisor section
on the ambient scheme. The final section is recovered in every
original bundle chart, not just the chosen finite refinement.

ASL8–ASL12 use the actual polynomial action and the actual product
section. The fraction map sends `a/X_I^k` to the restriction of `a`
divided by the invertible product section on `D_I`. Its injectivity and
surjectivity are exactly the two localization conclusions. The formula
for enlarging the finite chart set proves compatibility with every
restriction. The empty chart set is included. Pullback naturality of
these formulas is distinguished from a global-section base-change
isomorphism.

ASL14 now explicitly preserves the original universal quantifier over
all ratio families satisfying the coordinate identities. Such a family
agrees with the one in the `VeryAmpleBy` witness because the presenting
section is a unit on each relevant chart; sheaf equality gives global
agreement. The semilinear map, its surjectivity, its homogeneous
power-kernel and its degree-zero restriction therefore have the full
original scope. The use of inherited FCD13 gives the quotient by
`X_i−1` for this very map.

ASL16 constructs a finite dual basis for the actual affine section
module. The extra exponent in its evaluation identity is necessary
over rings with zero divisors and is supplied explicitly by ASL1.
The resulting splitting of a finite free module proves both
projectivity and finite presentation without assuming a Noetherian
coordinate ring or substituting an unrelated projective module.

ASL17 is valid for arbitrary, possibly nonflat, coefficient maps. The
canonical map becomes an isomorphism on the finite principal
trivializing cover; exactness of localization then detects both its
kernel and cokernel. The conclusion concerns affine source opens and
the nonempty vertices of the section cube. No isomorphism at the
global empty vertex is asserted. The pure-tensor formula respects the
specified Cartesian square and restriction maps. ASL18 uses exactly
the original scalar map, obtained from the affine scheme-to-ring
dictionary and the canonical global-sections isomorphism of `Spec R`.

ASL19 supplies every retained geometric hypothesis of FCD18 using the
same scheme, sections, chart coordinate rings and semilinear maps.
It constructs one Noetherian model and one cube comparison before
later coefficient changes. Flatness and comparison bijectivity are
required at nonempty vertices, precisely as in the inherited theorem.
ASL20 then applies the complete GSL8 argument to the unaugmented
Čech complex, preserving its differential and universal validity
under arbitrary coefficient changes.

ASL21 supplies every field of the literal `Perf` record. The matrices,
refined opens, original chart indices and coordinate functions are
fixed over the initial ring. The section equivalence for every later
ring and every specified pullback square has the original coordinate
formula. The `exact` field retains its own
`FirstCohomologyVanishes` antecedent; that antecedent is neither silently
assumed for existence nor claimed proved here. Thus the whole original
`nonempty_perf_of_smooth_isProjBy` implication is supplied.

## Corrections resolved before this review

The author removed literal commas accidentally printed inside four
exponents and made the arbitrary-ratio-family quantifier in ASL14
explicit, with its short uniqueness proof. The ASL4 dependency list
also correctly omits the globally quasi-compact cover claim ASL3.
These points are resolved in the hash above. There is no outstanding
correction or mathematical finding.

## Retained boundary

This packet supplies the actual smooth-projective `Perf` producer and
its stated section/localization suppliers. The separate polarized
base-change, vanishing, multiplication, integrality, principal-rank,
torsion/growth and square-law inputs remain visible. No unconditional
global section law, Moduli record, or whole selected RH/GRH obligation
is closed by this review. Earlier proof files were not changed.
