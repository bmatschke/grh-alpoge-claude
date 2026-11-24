# Independent review: arithmetic local charts, v0.55

**Verdict: PASS.** No unresolved mathematical or scope finding.

Reviewer: `/root/bessel_nonvanishing`, independently of the author.

Reviewed manuscript: `arithmetic_local_charts_v55/main.tex`  
SHA-256: `298731fbda1c627de41482687a8f4a416f9ce18790466cc971a738ee3ce717f9`  
Pinned Lean source: `7cbf7a0c32fca1badf05931879a37c3f8a2b03b4`.

All **22 human proof blocks** were read. The original `IsCO`, `IsCplAt`, `Loc`, `Integral`, `cpl_of_univ`, `loc_cpl`, `cpl_is`, `cpl_uniq`, `c3a`, `loc_flat`, `idem`, `types`, `loc_rho`, `unr_ex`, `cpl_univ`, `cpl_ex` and `loc_ex` statements were checked against the pinned sources. The actual rank-two and rank-three propagation consumers were also inspected. No proof-text correction was required.

## Principal mathematical checks

The completion arguments retain arbitrary commutative local coefficient rings where the original statements allow them. The two finite-quotient maps are genuine inverse maps, compatible at every exponent. Formal substitution and successive degree corrections construct the Noetherian completion and identify every ideal power; the proof does not assume the ideal lies in the Jacobson radical. The Rees-module proof supplies Artin–Rees, and the finite-module completion argument supplies both exactness and its canonical tensor description. Flatness is then proved for the original algebra structure. The explicit local faithfully-flat argument supplies every prime and minimal-prime clause of `c3a`.

For each original local object, the proof keeps the specified finite coefficient extension and every allowed map from its tensor product. Residue-compatible universality is used only with the correct scalar tower. The resulting map from the original entry algebra is flat, its maximal-ideal contraction is the supplied point, and its contraction to the actual coefficient ring is exactly the original maximal ideal.

The representation argument covers both ranks and arbitrary field-valued ring maps. A product of a surviving lower entry and upper entry, raised to their opposite positive weights, is an actual weight-zero monomial in the original coefficient ring. Its vanishing residue proves the special-fiber triangular dichotomy without a rank-two-only point-realization argument. The marked difference produces all coordinate projectors by formulas dividing only by 2. Polarization supplies the reflected edge pairs, and the rank-three connectivity proof covers every possible surviving-edge case. Characteristic 3 remains allowed. The broader original `idem` scope, over an arbitrary commutative coefficient algebra target with its original `Integral` premise, is also preserved.

The local representation theorem proves all ideal comparisons for arbitrary ideals and the literal residual entry and ordinary-character formulas for every compatible residue map. The final lower-unit/upper-maximal implication uses the proved two-rank special-fiber dichotomy on the actual residue map.

The existence proof constructs the coefficient DVR directly as a monic polynomial quotient. Finite freeness gives completeness and uniformizer injectivity; the field residue and geometric-series inverse imply locality. Minimum coefficient valuations give the unit-times-uniformizer factorization and prove the domain and DVR assertions. This establishes every original `unr_ex` field and the precise residue embedding. The tensor residue map and its completion then give one complete `Loc` record before all later test algebras and maps.

The final chart is the actual spectral contraction map. Applying the inherited `ChartOfFlat` to the identity open chart gives exactly the component correspondence required by the source consumers. All ideal comparisons use this map, and rank-specific rings and coefficient extensions stay distinct.

## Claim-by-claim findings

### ALC1 — PASS

Automatic locality uses only the common residue identification over a commutative local O: a unit lift of the target residue would turn a unit in the source into a nonunit. This also gives exact residue compatibility and continuity for every maximal-ideal power. The nilpotent quotients have every original IsCO field; no finite-residue or DVR restriction is added.

### ALC2 — PASS

Both finite-quotient maps are constructed with the original universal property. Locality makes the reverse map factor through the Nth quotient; one composite is checked on the surjective D image and the other by universal uniqueness. Their reduction compatibility is exact.

### ALC3 — PASS

Injectivity and surjectivity of the canonical quotient isomorphisms give respectively the exact contraction and density fields. Exponent zero is separately included, and the completion identification retains the supplied D-algebra map. This supplies the full cpl_of_univ statement.

### ALC4 — PASS

Every original iota-prime on O-prime tensor A is covered. The finite coefficient extension makes this tensor ring Noetherian. Restriction to A uses the literal Loc.univ with its scalar tower, and agreement on pure tensors returns the full tensor universal property for the supplied map.

### ALC5 — PASS

Finite truncations define the formal substitution map into the inverse limit without a Jacobson-radical assumption. Successive homogeneous corrections prove its surjectivity and the exact kernels at every power. Noetherianity follows from the stated power-series Hilbert theorem. At a maximal ideal, localization induces the same finite quotients and hence the actual source Cpl and map.

### ALC6 — PASS

The Rees algebra and Rees module are finite and Noetherian at the stated scope. Finitely many homogeneous generators of the induced filtration yield the exact Artin-Rees equality, and hence both cofinality inclusions. This proof does not import the desired completion-flatness theorem.

### ALC7 — PASS

The induced-filtration completion embeds, successive representatives lift surjectively, and the middle kernel is identified using the cofinal filtrations. A finite presentation then gives the canonical tensor comparison. None of the arguments requires injectivity of E into its completion.

### ALC8 — PASS

Exactness on finite ideals and the explicitly retained finite-ideal flatness criterion prove completion flatness. The second assertion uses the compatible finite quotients and completeness of the supplied IsCplAt target to produce a D-algebra, rather than merely ring, identification.

### ALC9 — PASS

Localizing the flat map at an actual prime gives a flat local, hence faithfully flat, map. Nonzero fibers give going down. It yields all source c3a clauses, including minimal primes over every ideal, with the actual contraction map.

### ALC10 — PASS

The finite-field image argument proves maximal contraction for an arbitrary ring map. In the DVR argument the target is not a field, exactly as in the original IsDiscreteValuationRing scope, so the uniformizer image is nonzero. Injectivity and torsion-free flatness follow for the specified extension.

### ALC11 — PASS

Completion flatness is composed with the base-changed original flat DVR extension. The actual map iota is this composite. Finite residue gives maximality of x and of its B contraction; the inherited exact local B structure gives equality with mB. Both original ranks are covered.

### ALC12 — PASS

A surviving lower entry and upper entry have strictly opposite integer weights. The indicated positive powers give an actual weight-zero monomial in B and zero in the original residual representation, so its image must vanish. This contradicts field-valued survival and proves the full special-fiber dichotomy for both ranks and arbitrary target fields.

### ALC13 — PASS

The original Integral.ze and normalized diagonal difference give an invertible marked scalar times the weight diagonal. Polynomial projector formulas divide only by 2, preserving ell=3 and arbitrary commutative C-algebras. For actual u, the same scalar is constructed inside the original B directly, so no unsupplied full cone_u or Integral producer is imported.

### ALC14 — PASS

Coordinate projectors reduce invariant subspaces to subsets of basis vectors. Nonzero entries propagate these subsets along the directed graph. The two rank-three adjacent reflected pairs, the odd-weight condition, and the remaining long arrow exhaust the cases and always give a directed cycle or both adjacent directions.

### ALC15 — PASS

Necessity uses explicit proper coordinate lines. Sufficiency uses the actual B-projectors and the polarization-reflection identity after the arbitrary ring map A to K. The separate special-fiber output is ALC12. No prescribed coefficient structure, finiteness or algebraicity of K is introduced.

### ALC16 — PASS

Inherited cont_u is transported through x0 to every local maximal-ideal power. The residue assertion is proved for every original compatible residue map by lifting each actual B element from O, giving literal diagonal and ordinary-character equality. All three ideal dictionaries hold for every ideal, without primality.

### ALC17 — PASS

In a local ring, failure of the original lower ideal to lie in x forces its image ideal to be the unit ideal. The proved two-rank special-fiber type theorem, applied to the exact residue map with kernel x, then forces the upper ideal into the local maximal ideal. This is the complete loc_rho endpoint.

### ALC18 — PASS

The actual A/x is finite type over the inherited finite residue field of B. The included finite-type-field argument shows it is a finite algebraic field extension, and the original O action kills mO. The specific residue embedding is preserved for the next construction.

### ALC19 — PASS

A finite-field generator and a monic lift G give the explicit finite free O-algebra O[T]/(G). Completeness and the field residue make every element outside the uniformizer ideal a unit. The minimum coefficient valuation gives the unit-times-uniformizer factorization, proving the domain, DVR, completeness, residue characteristic and exact maximal-ideal extension. The residue isomorphism respects the original O action.

### ALC20 — PASS

The inverse-limit completion is chosen before all target coefficient algebras and maps. Its universal property preserves the exact residue and scalar tower for arbitrary local O. For the coefficient-independent cpl_uniq, an arbitrary J-adically complete target is allowed; extension and uniqueness follow from compatible quotients, with yR equal to the actual maximal ideal. All original outputs are present.

### ALC21 — PASS

One finite unramified coefficient extension and one compatible residue embedding determine a single tensor residue map and its completion. Its restriction to A has maximal-ideal contraction exactly x. Every field of Loc, including the two coefficient structures, scalar tower and universal quantifiers over later IsCO targets, is constructed on this same object.

### ALC22 — PASS

The completed actual Loc has the flat map needed by inherited ACP16 with the identity open chart. This gives precisely the component chart used by the original rank-two and rank-three consumers. Ideal, TI, exceptional and good-locus comparisons retain the actual contractions. Sharp dimensions, density, seed incidence, propagation and automorphic inputs are explicitly left separate.

## Source and inherited-input verification

Independently verified all **31 full source snapshots** against both the pinned Git blobs and the read-only source checkout, and checked all **42 exact range hashes** and byte lengths. Every new proof block was matched to its provenance range and SHA-256. The inherited blocks **RTC7, RTC9 and ACP16** were checked against their frozen manuscripts and exact parent-provenance hashes. All declared claim dependencies resolve. The separately supplied two-pass draft-TeX report is bound to the reviewed manuscript and records zero diagnostics.

The accompanying JSON binds every claim to its exact proof hash and records the full source and inherited-input checks. Routine byte checks do not replace the mathematical review above.

## Retained boundaries

The chapter proves the original local completion, flatness, representation/type and local-existence suppliers. It does not prove the remaining `Pres`/`EPres`, sharp component chains, numerical dimension bounds, density and seed incidence, rank-three corner, full propagation, `AllGood`/`OffFin`, or automorphic and terminal Alt producers. The original supplied universal spaces and full frame assumptions remain exactly where the source theorems require them. The original arithmetic `P` premise is unchanged. The explicit standard commutative-algebra background remains recorded in the component metadata.

No whole selected RH/GRH obligation is closed by this review. No Lean replay was performed.
