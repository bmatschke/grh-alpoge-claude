# Independent mathematical review: PGR1–PGR20

**Verdict: PASS.** All twenty human proofs have been read against the pinned original contracts and relevant producer bodies. No unresolved mathematical or quantifier defect remains after the corrections below.

- Reviewer: `/root/geometry_alltest`, independent of the author.
- Original source commit: `7cbf7a0c32fca1badf05931879a37c3f8a2b03b4`.
- Reviewed manuscript SHA256: `8d6d48631a02e3784d9e9db686c49f6fefe80bcc582d94146ecf1a5a8d6cc94e`.
- Exact byte checks: 20 proof blocks, 39 original-repository snapshots and pinned Git blobs, 84 distinct original-source ranges, and four inherited proof blocks.
- Formal correctness is accepted. No Lean replay was performed.

## Main mathematical conclusions

The packet proves the full original universal `KExpansionC` implication. It keeps an arbitrary original `D`, supplied `HidaSetting X`, `Full X`, both words, both `FoldOK` and `InHH` premises, all four orbital premises, and full `AbsConvT`. Its conclusion is the literal operator `HasSum` and the original every-column-vector sesquilinear identity. It also proves the full original `KTie` implication on the supplied `FinX`, with both original `DimTie` identities and the actual finite fibers of `toTerm`.

The strongest mathematical checks were the finite inverse-different phase, the two-prime trivial-stabilizer argument, the exact full `PD` return carrier, and the analytic order of operations. The proof obtains an absolute mixed integral from folding before any complex unfolding. It derives absolute slab integrability for every strict column section before orbit regrouping. Only afterward does `AbsConvT` justify operator-norm convergence. Consequently the final Gram identity is not being used to prove the integrability on which it depends.

The original columns use an antilinear Riesz map. The manuscript preserves the reversed inner product, both phases, the one finite-level volume, and the same supplied infinite measures and domains. Its normalized Gram identity and the transport to the original spectral datum have the correct conjugations. Zero normalizers and zero-dimensional spaces are covered by the literal total-inverse convention. A target projection retains its correction term unless a separate range statement kills it.

## Corrections resolved before binding

- **PGR_REVIEW_1:** The initial generic FoldBound statement imposed Hausdorffness, although the original FoldBound does not. The author removed Hausdorffness from the Tonelli folding inequality and kept it only in the compact-finiteness/Borel refinement. PGR12 explicitly uses the compact Hausdorff case.
- **PGR_REVIEW_2:** The initial human statement called every quotient domain measurable, whereas the original IsFundamentalDomain permits null-measurable domains with a.e. coverage and disjointness. The corrected statement includes the original a.e. domains and the proof replaces them by measurable representatives, removes the countable union of translated null exceptional sets, and uses unchanged restricted integrals. PGR10 explicitly uses the same convention. Strict IsSFund statements elsewhere remain strict.
- **PGR_REVIEW_3:** Root independently noted that the operator transport and the orbital term index set both used the same symbol. The author retained mathcal T for operator transport and changed the term index set to mathfrak T; the formulas now distinguish both objects.
- **PGR_REVIEW_4:** The source range described as covering scl/blk originally began after those definitions. The bound range now includes the actual scl, blk, aTermL, aTerm and Hilbert-Schmidt encoding definitions. The mathematical formula needed no change.

## Claim-by-claim review

### PGR1: Full inverse-different triviality of every supplied additive character

**PASS.** The supplied finite character is used throughout. Clearing finite-adelic denominators proves unit modulus without an added continuity assumption. Rational trace integrality and Chinese remaindering prove the full inverse-different annihilator, including ramified places; finite generation extends it to the completed ideal.

Proof block SHA256: `309aa28389ded49978d037488adce66a04a260af0b657eb18d05a98e27cbdefb`.

### PGR2: Rational Levi splitting and exact character product

**PASS.** The explicit hyperbolic projection gives the rational Levi factor over the original field and after scalar extension. The upper-flag equations imply the required additive character coordinate and its Levi invariance. The supplied rational character identity cancels the actual infinite and finite factors, including isotropic rank zero.

Proof block SHA256: `a98ee2da9f1360997e5d05fefc10de1abc57c93061af8afe77c8e3d76ca2c9ed`.

### PGR3: Full UnipotentConjugateInLevel with its finite phase

**PASS.** RCV12 supplies actual level membership and its stronger bw congruence. The human proof then supplies the missing phase: the rational character coordinate lies in the completed inverse different, the e/z and bw parts agree modulo g above the two level primes, and g is a unit elsewhere. PGR1 yields exactly the original chi2 equality.

Proof block SHA256: `5d1f5253e6e6c411f5fac19edc6a30fa258a59e0005c5500ddf8411dc881e51d`.

### PGR4: Integral Levi extraction and exact smaller-level splitting

**PASS.** The fractional-ideal lattice splitting makes the orthogonal projection integral. Applying it to nh and then to the inverse gives preservation by both h and h inverse, so n is integral as well. The smaller-level factorization follows on the same lattice and with the same xu, not after replacing the level.

Proof block SHA256: `31bd419ff1188563ab3b49208c80a9ea104cec6a957eb345523f0017c7b4fef6`.

### PGR5: Full original NeatKu at every finite column

**PASS.** A rational column stabilizer preserves the actual full lattice. Its positive-definite complement has a finite integral isometry group, hence the stabilizer has finite order. Unipotent reduction at a residue characteristic forces that order to be a power of that prime; the two distinct auxiliary primes force the element to be one. No prime-versus-rank bound or arithmetic gap is used.

Proof block SHA256: `6286342106c44875e8b361abdf43494ad4423b203d0be12fe984373d0ceb608b`.

### PGR6: Actual sharp is an antilinear Hilbert coordinate bijection

**PASS.** The original Cols covariance forces the displayed reconstruction formula. Trivial column stabilizers give uniqueness of both rational and compact factors; every list of linear functionals therefore occurs. Riesz representation is conjugate-linear, and the reversed order in colCore is retained exactly.

Proof block SHA256: `d4b31547cd655da2e4311fc1968fb8967e4890cc7e47584b88ea4e0f456adcff`.

### PGR7: Actual seed well-definedness, measurability, covariance and reproduction

**PASS.** Integral Levi extraction and the finite character identity establish independence of every finite decomposition. Rational covariance uses the exact finite/infinite product. Countable right-level cosets and continuity of the wave function give measurability; continuous linear evaluation commutes with the supplied Bochner reproducing identity.

Proof block SHA256: `cbf1b3a650f3a9a522a139aeed0e33dc8028136a50623282099e9dec32c9d5b8`.

### PGR8: Rational unipotent density and strict column domains

**PASS.** Finite exponential and logarithm for the characteristic-zero unipotent group reduce finite-adelic density to additive approximation in a finite-dimensional rational vector space. The integral-lattice dictionary makes each original column unipotent discrete at infinity. The countable neighborhood construction gives strict measurable domains for precisely that subgroup.

Proof block SHA256: `2e281752c6b24dc4790cd6147aa4ae738efbd70e8caa62ba4dd0a9c737db251d`.

### PGR9: Exact column unipotent dictionary and finite phases

**PASS.** A rational linear map preserves the lattice exactly when it preserves its completions. The actual level-membership theorem identifies this group with NOcol, and rational injectivity makes the lift unique. The finite character is the inverse of the infinite character, with no finite-index replacement.

Proof block SHA256: `cab7571062518f4ea253cea87fed1646423ddb79eef7a46610555feffbf35637`.

### PGR10: All-section support cells and their exact product measure

**PASS.** Coverage uses the supplied Levi column classes and unipotent density; uniqueness uses integral Levi extraction and the full NeatKu result. Countable intersection partitions compare the original quotient with every strict column domain. Product integration contributes exactly one finite-level volume, with no hidden stabilizer mass.

Proof block SHA256: `11e6cd26e7454e209f3a7ee20ec31ced053a26b4458204c8897342bc3fc0a846`.

### PGR11: Full general FoldBound and compact multiplicity finiteness

**PASS.** The generic Tonelli argument needs only the original topological-group and Haar hypotheses. The unique expression gamma=delta inverse times s gives the exact multiplicity bound. The corrected statement accepts null-measurable a.e. fundamental domains and explicitly transports the proof through measurable representatives. Hausdorffness is used only for the compact finiteness and Borel refinement.

Proof block SHA256: `cb31680dae99ef15bf61195d42ba1c88b7a2c37c908d47a9cc7db46452f92c49`.

### PGR12: Full general finite, L2 and mixed Poincare identities

**PASS.** The averaging inequality proves the mixed absolute integral bound before any complex unfolding. It yields the exact a*A*J and a*J squared estimates, pointwise convergence, representative independence, and the original L2 statement. Nonnegative unfolding and then domination justify all complex sums. Inversion of the second coset index gives the correct S intersection rS-prime r-inverse stabilizer and arbitrary a.e. domains.

Proof block SHA256: `2309971338b17d962f93ec93adf0eeea049345fb738577ddf824a73a3ea0a31d`.

### PGR13: Actual absolute slabs and single unfolding

**PASS.** The nonnegative absolute quotient integral is finite before the slab change of variables. Applying the every-section cell formula and dividing only by the positive finite level volume proves SlabAbs for every strict column section. The actual InHH fields identify the original quotient L2 inner product, with precisely one volK2 factor.

Proof block SHA256: `d99d9a31a50398374c05763bb1557e1eb2a68b74ebdf04f5050bfab5301a5adb`.

### PGR14: Complete original flag-return carrier and double quotient

**PASS.** The return identity supplies both lattice transport directions. Transport of the original row data proves IsLift and every local/primitivity and different-weighted FrameOK field. Chinese remaindering produces one integral upper-unitriangular matrix for all required primes. The conclusion is the original localized ModG condition, and active terms are exactly the original double quotient without a Gram-nondegeneracy restriction.

Proof block SHA256: `2343836386459a00061089181bb2892c4d521a0350c048d19ba4196bd0bbef71`.

### PGR15: Full pointwise support reindexing and finite phase

**PASS.** Inverting the original Poincare index and removing rational Levi and unipotent support factors gives the literal return set. Trivial Levi stabilizers reduce the remaining equivalence exactly to the original right column-unipotent quotient. The chi(k) inverse factor and right-unipotent wave covariance cancel, and absolute convergence justifies both the scalar and norm reindexings.

Proof block SHA256: `bab3dac2388e6e5bce64b9e218bba60f04e549046ada9c3b14a7a1d0ca0dbc6e`.

### PGR16: Exact orbit unfolding with every original section

**PASS.** The return double quotient gives the exact orbit set and rational stabilizer. The checked covariance f_(nr)(x)=f_r(n inverse x) has the correct infinite/finite phase orientation. Countable tiling first proves equality of absolute integrals, then the complex identity for every prescribed strict orbital domain. The full original AmpWellDef and OOFundIndep premises remain supplied.

Proof block SHA256: `41c45d776539795c70b9e2cb093601566189c3d627770fbf9f46a86b2679d786`.

### PGR17: Exact TermVal and universal-scope EntryUnfold

**PASS.** The Bochner rank-one operator is the literal OOt. Evaluation in the conjugate-linear first inner-product slot conjugates chi and produces precisely the scalar term phase. Absolute scalar unfolding is established independently of operator convergence. Finite-dimensional norm comparison transfers the first full AbsConvT clause to aTerm and every block, including zero-dimensional cases.

Proof block SHA256: `47449e64e908099ac722b73b4f45cc838ba14781cae579834a6d54b7825af11a`.

### PGR18: Full original universal KExpansionC

**PASS.** The complete original universal KExpansionC is obtained on arbitrary supplied D, X, Full, and ordered word pair with exactly the two FoldOK, two InHH, four orbital, and full AbsConvT premises. The original rows, sections, measures, characters, and representatives persist. The HasSum and every-vector sesquilinear identity follow, without a gap or positivity condition on c0.

Proof block SHA256: `7318b804f39039609ccd40ab420100051d87e90f43fbf54d91ad7b2e0a03352e`.

### PGR19: Full period linearity and exact antilinear Gram transport

**PASS.** PuLinear is proved under only its original InHH premise. The period map is continuous from the finite-dimensional original ColT into the ambient complete quotient L2 space. Two antilinear Riesz maps give the exact complex-linear Gram transport. Total inverse and square-root rules handle zero normalizers, and arbitrary target projections retain the full correction term.

Proof block SHA256: `ee9e56d1b8854092c36d62388c704d61d45657e1e3a9350722ad557ef39111b7`.

### PGR20: Full original KTie on the supplied finite spectral datum

**PASS.** The original FinX and both DimTie identities identify the actual sOf normalizers and adjoints. Conjugation by the two antilinear coordinates is a real-linear continuous norm isometry on operator spaces, which is sufficient to transport HasSum. The literal finite toTerm fibers and absolute norm series give both KExpansion and KAbsConv; no FinX existence, SIso, or new period-range identification is inferred.

Proof block SHA256: `5ec3b4d59a49788988d7bf43fdaa6a17747833e2ad03b8eb672c204e4d6b6232`.

## Exact retained boundary

KExpansionC is the full original conditional theorem. FullExists, Forms0, the independent global FoldOK/InHH/orbital/AbsConv producers, FinX existence, SIso and the later coherent period-range/global spectral join are not supplied by this packet. KTie retains arbitrary original FinX and both DimTie identities.

No whole selected obligation is closed by this review. The explicit ordinary background consists of finite-dimensional linear algebra and Riesz/adjoint theory, number-field lattices and different ideals, Chinese remaindering and additive finite-adelic approximation, basic Haar theory, Tonelli and Bochner integration, and absolute convergence. The actual finite character, stabilizer, support, return-carrier and unfolding suppliers are proved in this chapter rather than imported as new assumptions.

## Binding record

`independent_review.json` records each of the twenty proof-block hashes, every full pinned source-file hash, every distinct exact source-range hash, and each inherited proof-file and block hash. The separate supporting Mathlib definition is pinned to its own commit, not mislabeled with the RH repository commit. `review_by_geometry.py` independently recomputes those bindings. It is a reproducibility check of the recorded review, not a substitute for mathematical reading.
