# Independent review of CAF1–CAF11

**Outcome: PASS at the stated scope.** The character seed and actual CM-field
producers are complete human arguments on their explicit original inputs.
The large marked frame and the rank-two and rank-three automorphic
representation constructions correctly remain separate tasks. No whole
selected obligation should be closed from this chapter alone.

Reviewer: /root/bessel_nonvanishing, independent of the chapter author.
Source pin: 7cbf7a0c32fca1badf05931879a37c3f8a2b03b4.
Reviewed manuscript SHA-256:
a669741edd7a2ea317baba0004b18142a2e56406af1802e064f92162626f80e1.

## Scope and original-data audit

I read all eleven human proofs and compared the main endpoints with the
original Gen, UFacts, SeedClause, HasFrameW, HasFrame, and
FieldPairCharacterTripleConditions declarations. I also inspected the
original seed_cl, gd_ex, host_ex, GD, and HostData applications.
All 24 source files cited by the chapter were checked byte-for-byte against
the pinned Git blobs, and their file hashes agree with the chapter's
provenance. This was a mathematical and source-scope review, not a Lean build.

The source seed_cl chooses one positive modulus before both the later CM
field and the later prime. CAF6 fixes the quadratic field, stripped
prime-to-ell modulus, exponent, and two core characters at exactly that
stage. CAF7 permits every original compatible later L and w. The
order-ell auxiliary character is correctly allowed to depend on the later
prime. There is no field-dependent replacement of the modulus.

The chapter's smaller collection of seed-relevant clauses of Gen is
legitimate: each clause is a field or immediate part of that original
record. The chapter neither asserts the remaining Gen clauses nor uses its
strict cohomology or local-degree fields without proof.

## Checks by mathematical block

- **CAF1–CAF2:** The DVR norm argument, completeness, Teichmuller lift, and
  norm congruence are correct. Conductor stripping uses the given inertia
  group, total ramification of the ell-power cyclotomic extension, and
  unramified prime-to-ell roots. It does not require an abelian target.
  The two original SplitAt clauses follow from the displayed factorization
  and congruence.

- **CAF3:** The negative square root generates the actual embedded imaginary
  quadratic field, with the given character's Galois kernel. Trivial inertia
  gives the discriminant conclusion by the integral trace pairing. This
  also has the source's broader quadratic-field scope and does not
  improperly require odd ell.

- **CAF4–CAF5:** The power subgroup has the literal prescribed kernel, index
  ell, and inertia behavior. The elementary proof of primes congruent to
  one is valid: a prime divisor of Phi_R(A) is prime to R and has A of exact
  order R, since the cyclotomic factors of X^R-1 have disjoint roots in that
  characteristic. Choosing w greater than R gives the required
  coprimalities. The entire decomposition action is trivial on the
  prescribed roots, giving the full witness-prime split clause.

- **CAF6–CAF7:** Every field of the original character-triple record is
  accounted for. This includes prime-to-ell order, distinct core
  characters, parity at the same complex conjugation, literal quadratic
  values, and the all-element norm congruence. The square nondegeneracy
  condition follows from the strict norm congruence and the supplied
  residual square witness; it is not replaced by a genericity assumption.
  The discriminant and auxiliary-character restrictions match the source.

- **CAF8:** The field is the actual fixed field inside the supplied
  algebraic closure. Containing every complex conjugation makes the first
  fixed field totally real; adjoining the same imaginary quadratic field
  gives the CM extension. Both subgroup equalities are literal, including
  the maximal real subgroup. A stray comma in the fixed-field exponent was
  an editorial issue and was removed in the reviewed final snapshot.

- **CAF9:** The Dat specialization preserves the original quadratic field
  and character. The quadratic conductor input is explicit, with the
  standard elementary Gauss-sum explanation. The residual local component
  is a power of the mod-ell cyclotomic character, uniformly over conjugate
  prolongations. The GD.eta guard yields the needed kernel noncontainment,
  because the prime-to-ell local component is trivial on the cyclotomic
  kernel. The modulus is exactly abs(discr K) times N_{ell'}.

- **CAF10:** The host argument is separate. High dyadic conductor provides
  a unit congruent to minus one modulo four in the kernel of the dyadic
  character. Its lift to dyadic inertia kills every prime-to-two
  cyclotomic component, including the ell-adic cyclotomic character.
  This proves kernel noncontainment for every odd ell, including 3. The
  argument does not insert the GD.gen guard or a prime-to-ell order
  hypothesis on the host character. The modulus N_{ell'} squared agrees
  with the source's exponent-two factorization.

- **CAF11:** The same L, g1, Phi, C0, w, and GalLink are used. The original
  g1 maps to Phi.g0 under the original quotient map; GalLink.del puts it in
  the original quadratic kernel, and GalLink.psi with
  Ok.baseSubgroup_spec supplies the square witness. There is no replacement
  marked element and no assertion that the supplied large frame has
  already been constructed.

## Integration recommendation

Accept CAF1–CAF11 as proved at their stated scopes, with the chapter's
explicit ordinary local and cyclotomic foundations retained. Keep frame_ex,
the strict cocycle and quotient/local-link construction, and the
automorphic seed suppliers open. Preserve the distinction between the
cohomological frame over the maximal real subfield and the original
rational CountV host frame in later transport.

No unresolved mathematical or quantifier defect was found.
