# Independent review of HXD1–HXD3

Reviewed TeX SHA-256 is `3baab2dcdb57dcc1ed1c543569d38b4a1b2130c733b96257c90804f0860e1264`. The formal source pin is `7cbf7a0c32fca1badf05931879a37c3f8a2b03b4`.

**HXD1.** I checked the source definitions of the prime-to-ℓ part, ℓ-part, dyadic projection, `th1`, `f0`, and `n0` in `DirichletPrimeToLPartMulLPowerPart.lean:78–102` and their arithmetic uses in `Th1Facts.lean:11–76`. Splitting in the character's cyclic group and applying the CRT projection preserves the product on the full level. The residual ℓ-power character is trivial on all units. The chapter uses the source value of the order modulo the least common multiple of 4 and the actual order of θ, with no auxiliary dimension choice.

**HXD2.** The conductor of the odd primitive product divides ℓ times the conductor of θ², even if these factors have a common prime. Passing to the primitive dyadic constituent first makes its value defined on every odd class. The calculation with 5 gives exact conductor exponent t−1 for its squared quartic twist, including the boundary t=4. The numerical hypothesis on the supplied positive q yields the exact inequality in the new character data. The parity and both primitive-character conditions match `UnramifiedCocycleIsCoboundaryOfBernoulliUnit.lean:14–22`, `HcXiSq.lean:120–135`, and `HcDirData.lean:29–109`.

**HXD3.** The single unit modulo ℓN² represents the Galois action at all levels, including 4 and f2ⁿ. The Teichmüller value reduces to the ordinary residual cyclotomic value, and the ℓ-power factor vanishes under the original residue map exactly as required in `DirGPowOne.lean:23–68`. Substitution of both frame identities produces the square times the sign. Its inverse retains that sign. This supplies the finite-character input to BR7 over the originally quantified field and coefficient ring.

The author incorporated the primitive-dyadic-character clarification before the hash above was taken. No additional input is needed to pass from the host's two arithmetic hypotheses to this instance of BR7. The passage from its absolute cocycles to the Selmer quotient on the original host is proved separately in HXP1–HXP4.
