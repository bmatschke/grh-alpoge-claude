# Rank, lattice and finite places on an original column

Reviewed TeX SHA-256 `d22f7c4312afa29d1f29554f74d82fe1325fd5805f52b61961e83d09ca97926c`.

**H77S1.** The last equation of `RankVal` in `PairRowIffQdRows.lean:26–32` fixes the sum of the two ranks. `DiagSpacesOfOver.lean:102–105` specializes it to these precise stages using only the witness over the context. The product has two natural factors, giving the stated inequality without a threshold or a growth assumption.

**H77S2.** The diagonal-space witness and the sign at index i+1 give both the identity Gram matrix and the integral span of this specified frame in `DiagSpacesOfOver.lean:107–120`. The native predicate is characterized by those Gram entries and integral coordinates in `NotVstdOfGramOne.lean:40–68`. Basis-coordinate uniqueness proves the latter. Thus the proof yields the standard lattice even when other estimates obtained together with it in `EventuallyDefiniteSpacesStandardAndLarge` need a lower scale bound.

**H77S3.** `ExistsFineAdelicDatumOfHyp.lean:47–63` uses the projection to the real field to bring the rational prime into both real ideals. The half pin compares the primes below the selected CM primes in the host field K. The corrected statement gives equality of the contractions to its integers, exactly as in `IsAbsIrrCharCompIff.lean:84–86`. For the independently specified twist-place set, finite fibers of residue characteristic and conjugation invariance give both assertions (`ResCharConj.lean:44–56`). `ExistsFineAdelicDatumOfHyp.lean:119–122` identifies the used tuple subtype with membership in a singleton union a finite set. No selection of an analytic realization is involved.
