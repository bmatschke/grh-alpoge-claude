# Independent review of arithmetic_component_propagation_v53

**Verdict: PASS.** All nineteen numbered human proofs were read independently and checked against the original source interfaces and the relevant producer bodies. No unresolved mathematical, quantifier, source-binding or endpoint-scope defect was found. The author manuscript and metadata were not edited.

Reviewer: `/root/bessel_nonvanishing`. Review date: 2026-11-23.

Frozen manuscript SHA256: `b9613cd1e1248c726fb734f4af5d8aa59a213e3aaf6f59ff3086082b5991cce7`.

Pinned Lean commit: `7cbf7a0c32fca1badf05931879a37c3f8a2b03b4`.

## Main scope checks

The most important simplification is the residue-constant ring in ACP1–2. For an original complete discrete valuation test ring A with finite residue field, the subring C=k+m_A has the required residue field, is complete and Noetherian, and has precisely the same positive maximal-ideal powers as A. The proof of finite generation over k[[t]] uses finiteness of the residue extension and a convergent coefficient expansion. It also handles the field case. Matrix entries, every value of the ordinary character, their inverses, and the coefficient map all lie in this single ring. Thus passage through the supplied Space preserves every original finite-point test and its adic-continuity condition. There is no replacement of the original IsCD scope by a more restrictive test category, and the source point_loc conclusion is not used as an input.

ACP3–7 were checked against the exact ordered-product flag identity, the frame separator, and the original finite-character and diagonal-character statements. The spectral projectors use only unit separator differences and work over the original local coefficient ring. The finite-character bound is uniform across the finite quotients used in the proof. Both local branches in the diagonal-character argument are treated, including the polarization/inverse/reversed-index computation. No exception at ell=3 is introduced.

ACP8–11 cover both prime-kernel branches. In the off-triangular case, the finite-ideal radical bound collapses the actual weight-zero algebra to its residue constants. In the other case, one global triangular direction gives multiplicative diagonals, which are determined by the preceding character argument. The five cycle products and determinant signs were checked explicitly. Together these prove the full original FinPtOf from its original OffFin antecedent. They do not produce OffFin or silently import an automorphic statement. The inherited fixed-frame application keeps the already chosen marker.

The specialization proof in ACP12–13 was checked without adding a catenarity hypothesis. The one-dimensional quotient follows from the maximal avoiding prime, principal ideal theory and finite prime avoidance. The finite-family construction preserves the source dimension thresholds and includes an empty forbidden family.

For ACP14–17, all ten local-data conditions and all eight global-data conditions were compared with their literal definitions. The local two-state induction retains the original type-I and thick-component alternatives without imposing a new disjointness or partition assumption. The global argument uses finite unions of irreducible components, the supplied density and connectedness statements, and the precise marked-point condition. The flat-chart proof gives the required component correspondence by going-down and open-immersion closure, at the original topological scope. The final chart transfer is conditional on those original inputs and does not produce arithmetic dimension, core or corner data.

ACP18 proves the stated radical/intersection implication and does not assert the missing ideal producers. For ACP19, I checked that the original Af.IsAutCsd and AutCsd0 formulas use the same attached-representation predicate, while IsAutCsdA appends the WitA condition. The rank-two Alt statement similarly appends WitAQ to the original newform conclusion with identical premises. Projection therefore proves the asserted Alt-to-original implication with the same marker, Marks and FinEnd. No converse or independent production of an Alt endpoint is claimed.

## Claim-by-claim record

### ACP1 — PASS

The residue-constant ring C=k+m_A has maximal ideal exactly m_A and m_C^N=m_A^N for every N>=1, including the multiplication argument t^N a=t^(N-1)(ta). Closedness gives the required completeness. Finiteness of the original residue field makes k_A/k finite; recursive t-adic expansions make A a finite k[[t]]-module, and C is a finite submodule. The field case is separated. This proves the full IsCO specialization actually needed for every original IsCD test ring.

### ACP2 — PASS

The scalar tower forces the test ring to characteristic ell. All matrix entries, all ordinary-character values and their inverses lie in the same C, and the equal maximal-ideal powers preserve the exact adic-continuity condition. Restriction gives the original IsLift datum. The supplied Space universal property and the coefficient map therefore give the required point on the actual algebra; automatic locality of coefficient-algebra maps is justified. No point_loc theorem or stronger test-ring assumption is imported.

### ACP3 — PASS

The Lagrange projectors are valid over an arbitrary commutative local ring because the separator differences are units. Their residue ranks are one, and lifted bases give an invertible change of basis. Inserting a variable factor in the ordered product, then applying two projectors, kills every lower entry and fixes each diagonal entry. This proves the original ordered flag statement with its actual arbitrary dimension and coefficient scope.

### ACP4 — PASS

The frame separator gives pairwise distinct residual weights for both n=2 and n=3. ACP3 applied on the original universal ring yields the exact local characteristic polynomial, and the coefficient map transports it to the supplied algebra and every allowed point. This is the full o1 statement; no additional local triangulation hypothesis is assumed.

### ACP5 — PASS

For an exponent h=ell^a m with ell not dividing m, the geometric sum is a unit at a principal unit. Reduction to an ell-power and the domain hypothesis then force the unit to be one. This proves the source principal-unit torsion statement at characteristic ell without a completeness hypothesis.

### ACP6 — PASS

Reduction modulo maximal-ideal powers has finite principal-unit ell-group image. The source continuity/open-kernel assumptions produce the required finite continuous quotients, and the uniform detector exponent applies to all of them. Krull intersection, followed by ACP5, recovers equality of the full characters. The finite-residue condition and the uniform quantifier on the exponent are used exactly where necessary.

### ACP7 — PASS

The multiplicative diagonal entries give the characters required in ACP6. The frame gen and cl fields supply the local detectors and one common finite-character bound. Both local branches are checked: the direct branch uses the stated diagonal condition, and the conjugate branch uses the exact polarization/inverse/reversed-index identity. The original reference characters and ell=3 scope are preserved.

### ACP8 — PASS

The six-term determinant expansion is explicit. Killing the three two-cycle terms and the two oriented three-cycle terms leaves precisely the product of the three diagonal factors, with the correct signs.

### ACP9 — PASS

A prime test kernel in the off-triangular locus contains one of the original controlling ideals. The finite-ideal radical condition and the killed coefficient maximal ideal force the weight-zero algebra to factor through its original residue constants. The needed diagonal entries and five cycle products have weight zero; their reductions give exactly the required vanishing and reference diagonals.

### ACP10 — PASS

In the complementary case the prime kernel contains an entire upper or lower off-triangular ideal, giving one triangular direction for every group element. Diagonal multiplicativity is then valid globally. The source local characteristic polynomial forces the required inertial diagonal values in a domain, and ACP7 recovers their exact characters. No off-triangular ideal is silently used in this branch.

### ACP11 — PASS

ACP1-10 cover every original IsCD finite-residue test ring, every allowed scalar tower and IsLiftA point, and both prime-kernel branches. The full original FinPtOf follows from its literal OffFin antecedent. The fixed-frame consequence uses AFE15/16/20 on the identical earlier marker. OffFin and automorphy producers remain explicitly retained.

### ACP12 — PASS

The maximal prime avoiding a chosen element exists by Noetherian ascending-chain termination. In the quotient, every nonzero prime contains that element. Principal ideal theory, the finite minimal primes over its ideal, and prime avoidance force the maximal ideal to have height one. The proof retains the original local and avoidance hypotheses and does not require catenarity.

### ACP13 — PASS

The dimension drop after adjoining the coefficient element is at most one by systems of parameters and the generalized principal ideal theorem. A minimal component of sufficient dimension avoids each forbidden ideal by its dimension bound. A product of chosen avoiding elements, with a nonmaximality witness, reduces the full finite-family claim to ACP12. The empty-family case is included.

### ACP14 — PASS

The two-state component-chain induction accounts for all ten original LocData.Ok fields. A good type-I component or a thick component carrying the specified exceptional-prime chain is propagated through every high-dimensional adjacency. Nice-prime supply, extension, P1 and P23 are applied at their exact scopes; neither a partition nor disjointness of the two component types is added. This gives the full original LocProp.

### ACP15 — PASS

The finite unions of good and bad relevant irreducible components are closed. The original density and preconnected-core hypotheses force a common core point if both occur; the closed-set point condition then gives a marked point where the local incidence rule contradicts badness. All eight GlobData.Ok fields are preserved. No openness of the component predicate or unprovided geometric density is inserted.

### ACP16 — PASS

Flat local maps are faithfully flat after the stated localization and give going-down. The proof then identifies closures from minimal primes with whole irreducible components through the chart point, using the open immersion and density in an irreducible component. This establishes all original ChartOfFlat outputs for the supplied arbitrary topological space and does not add Noetherian hypotheses to the target.

### ACP17 — PASS

The three chart assertions are transported using the full min-prime component correspondence from ACP16 and the supplied local conditions. The good type-I seed uses ACP14 precisely when needed. The original openness and closedness hypotheses are kept, and the conclusion is the full GlobOfCharts interface without producing the arithmetic chart inputs.

### ACP18 — PASS

The ideal implication follows because any prime containing M intersect I contains M or I, using MI contained in their intersection. Applying the two given radical bounds proves the combined bound. The weight observation identifies the single finite ideal needed by both loci, while the existence and arithmetic bounds of those ideals remain separate.

### ACP19 — PASS

The source AutCsd0 formula equals the original Af.IsAutCsd formula, with the same AttC predicate. IsAutCsdA is its conjunction with the continuity-to-WitA property, and AutEnd2Ao adds WitAQ to the original newform conclusion with identical premises. Projecting these conjuncts preserves the same marker, Marks and FinEnd. The implication is only Alt-to-original and produces no Alt endpoint or witness theorem.

## Independent binding verification

I independently recomputed the complete manuscript hash and all nineteen delimited proof-block hashes. All thirty-seven source snapshots were compared byte-for-byte with the corresponding pinned git blobs and with the read-only checkout. All forty-three source-range hashes and byte counts were recomputed. The five inherited proof blocks AFE15, AFE16, AFE20, LFC3 and LFC6 were checked against their files, proof ranges and parent provenance. Every check passed.

The companion JSON records the exact hash for every reviewed claim, its source ranges, the inherited bindings and the retained scope. The author reported a successful two-pass draft TeX check; this review did not repeat compilation or replay Lean. The review evaluates the human proofs rather than treating the verified source declaration as their proof.

## Boundaries retained

The supplied frame and Space, OffFin, the arithmetic rank-specific dimension/core/corner and chart suppliers, and the automorphic WitA/WitAQ producers remain exactly where the manuscript states them. The original P premise in the inherited frame entry remains retained. Named classical commutative-algebra results remain recorded in the author's input file. This packet closes the listed original subtheorems; it does not close a whole selected RH/GRH obligation by itself.
