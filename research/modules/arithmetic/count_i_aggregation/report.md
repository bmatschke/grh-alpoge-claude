# Arithmetic-count dependency audit and bounded closures

Version 0.30 working contribution, 22 November 2026. All formal-source statements in this report refer to `CocoSgt/riemann-hypothesis-lean` at commit `7cbf7a0c32fca1badf05931879a37c3f8a2b03b4`. The underlying Lean proof is assumed correct throughout. “Open”, “unmatched” and category D describe the human reconstruction only.

## Principal result: separate ordinary RH from unrestricted Dirichlet GRH

The actual Case-III condition contains **both** `Odd (orderOf ψ)` and `ψ ≠ 1`. Every character on an original host of target χ has order dividing a power of two times `orderOf χ`. Therefore Case III is empty whenever χ has power-of-two order. This includes the principal character and every quadratic target. This is a proof from the literal character conditions, not an expectation based on the name of a case.

The new KA5 proof establishes the fixed-target CountIII predicate with exponent zero. KA6 checks the quantifier order through all actual consumers: `sumOut`, `sumIn`, `point`, `thmHV`, `jointWin_of` and `vwinAt_of_joint`. Each uses its count, height or joint-window input only at the same target. Consequently, relative to the previously reconstructed local, two-primary, odd-minus and window components, the remaining **cohomological** sufficient cut for a fixed power-of-two-order target is:

1. `CorGK` at the single field `Kstar (pK χ)` (or the stronger specialized `PropGK`);
2. `PMExAlt`, to supply CountII through the already reconstructed YX2;
3. CountV at that same target.

These supply `PointHV` and then `VWinAt(χ,401)` under the original prime-pair and window hypotheses. The exponent 400 and the real continuum of window scales are preserved. No target-uniform threshold is invented. The universally quantified CountIII predicate remains open for general targets with nontrivial odd-order part.

This removes the **separate** SeedIVAlt/case-III chain from the selected RH route. It does not remove the common PMExAlt dependency, and it does not address the independent actual-family, gap, theta, denominator, metric or spectral conditions of the final theorem. The complete dependency graph must express these other branches as AND requirements rather than treating the host-window theorem as an isolated leaf.

## Genuine bounded closure: PropGK to CountI

`main.tex` supplies six claims. KA1–KA4 close the full human implication

`PropGK → CorGK → CountI`.

The remaining producer is explicit. There is no claim to have proved `PropGK`, `OneChar` or the rank-three congruence-number theorem.

| Claim | Exact contribution | Human classification |
|---|---|---|
| KA1 | The total weight of distinct cyclic character-kernel quotients is at most the size of the finite abelian group. | B, closed independently |
| KA2 | Every original Case-I host character satisfies all twelve fields of `GD`, including the inertia-based noncontainment condition. | B, closed independently |
| KA3 | Two uniform nonzero integers remove the exceptional coefficient prime and give the exact `CorGK` sum. | B, closed independently |
| KA4 | Finite kernel-orbit aggregation, with arbitrary coefficient rings and prime sets, yields literal `CountI`. | B, closed conditional on `CorGK` |
| KA5 | Case III is empty for every power-of-two-order target. | B, closed independently |
| KA6 | The specialized counts propagate to `PointHV` and `VWinAt(χ,401)`. | B, closed conditional in the stated inherited scope |

The aggregation has several useful checks. Complex characters are only a counting device; the original coefficient DVRs are not identified. A `GD` witness at each prime supplies finiteness and the full exact-kernel orbit bound in that coefficient ring. The nonzero integer in `PropGK` is selected before all later coefficient primes. The two auxiliary primes are selected before all hosts. Enlarging a host kernel fiber to the full orbit is legitimate because normalized lengths and logarithmic prime weights are nonnegative. The final bound is absorbed into one exponent independent of the host, coefficient family and finite prime set.

The field for a fixed target never varies after `Kstar (pK χ)` is selected. For ordinary RH this is the particular field isomorphic to Q(√−7). Supplying a theorem for all imaginary quadratic fields is sufficient but stronger than this selected route needs.

## Cases I, II and V survive principal specialization

For the principal target, `pK = 7`, `pOne = 3`, and the class number of Q(√−7) is one. The last assertion is justified in the proof by the elementary reduced-form check: a reduced primitive form of discriminant −7 has `3a² ≤ 7`, so the only reduced class is `[1,1,2]`. Thus the exceptional set is `{3,7}`.

CountV is confined to these two coefficient primes and twist one, but has arbitrarily large dyadic conductor. An explicit original host has auxiliary primes 11 and 23, cutoff 2 and exponent 12. Take a primitive even character modulo 2¹⁴, multiply it by the odd Legendre character modulo 11 and by the trivial character modulo 23, and use a 3-adic coefficient ring containing its roots of unity. Then `f0=2`, `n0=3`, `c2=14` and `R1=9216<2¹⁴`; this is in the actual large-conductor Case-V region. Its Big condition is also checked.

Case I is nonempty with twist one, coefficient prime five and the Legendre character modulo 11. Case II is nonempty with twist two, cutoff three, coefficient prime three and the product of the Legendre characters modulo 11 and 23. These examples establish nonemptiness, not a nonzero Selmer length. They prevent an unjustified vacuity shortcut. In particular, characteristic three remains on the principal route; a modular-support theorem requiring ℓ>3 cannot alone cover it.

## Remaining CountI producer

The exact source statement `UnitaryThreeGroups/OrbEquiv.lean:propGK` is

`CongruenceNumberRankThree → OneChar → PropGK`.

Its finite coefficient-orbit comparison, Frobenius normalization and valuation conversion are category B reconstruction work. They are not already supplied by KA1–KA4. The inputs have substantially deeper content:

| Obligation | Required original interface | Classification and scope |
|---|---|---|
| `OneChar` producer | `KatoQuadraticCharacters/OneChar.lean:oneChar` consumes `InpZ` and `AutomorphyUnramifiedCoefficients`. | C, open arithmetic producer |
| `InpZ` | Extends the exact `CohInp` with LemmaM, LemmaM′, LemmaP, RigII, AdVanishK and the rank-three number theorem. | B assembly after its actual deep inputs; not an independent closure |
| `KatoTwo`/RigII | The original `Used` record checks parity, conductor, class-number coprimality, ordinary flags, residual trace congruence and irreducibility on the infinite cyclotomic kernel before the two Selmer vanishings. | C for the arithmetic theorem; D for any unverified matching to a named published result |
| `AdVanishK` | Exact polarized adjoint, including the negative-transpose action of complex conjugation, on the prescribed imaginary quadratic field. | D until the exact published hypothesis match is recorded; inherited rank-four RX does not automatically give every rank-three instance |
| `AutomorphyUnramifiedCoefficients` | For the original datum with coefficient ramification index one and fixed embedding, choose one marked element giving weight-zero finiteness, all Type-I automorphy, and the Type-II modularity implication. | C, open actual automorphy and support producer |
| `CongruenceNumberRankThree` | Constants after the fixed quadratic field; then e,N,p,w and a Galois-stable roots-of-unity orbit; then one nonzero integer **before** every later coefficient prime, embedding and finite rank-three/rank-two collection. | C, open uniform arithmetic catalogue; D for an unproved rank-four-to-rank-three reuse |

The rank-three number theorem is not a pointwise separation statement. Its single integer must control every later coefficient specialization. The rank-four CX results are useful precedents but do not discharge this different predicate without a verified transport. Similarly, a classical adjoint theorem may cover a substantial mathematical leaf after matching, but it does not construct the original ordinary universal ring or the same marked element required by the automorphy package.

## Remaining CountII producer: actual ordinary support

The reconstructed YX2 reduces CountII to literal `PMExAlt`. The latter is quantified over each original Fit/Deep tower and a fixed complex embedding. It chooses a coefficient threshold **before** every later coefficient DVR and each actual source deformation space. It then asks for one ideal with all five fields `fin`, `p1`, `seed`, `pur`, `aut`.

QX10 reduces this to two actual rank-four source Links, each carrying `HidaPropsAlt` and `P1core` on the **same** ideal, above one common coefficient threshold. This is a smaller target than all-rank `ModUAlt`; it is still deep.

`HidaPropsAlt` literally has six fields: `ring`, `dense`, `pt`, `end1`, `end2`, `twist`. Its construction is category C. `P1core` is a characteristic-ℓ modular-support assertion and is also category C. A finite quotient, dense characteristic-zero point set, or an adjoint Selmer vanishing cannot replace the complete package.

Candidate published ordinary support theorems should be evaluated against the actual Links. Any mismatch in residual Schur hypotheses, distinctness/primitivity, local conditions or the range of coefficient primes is category D in the human audit until resolved. In particular, no ℓ>3 theorem can be declared sufficient without handling the actual ℓ=3 instances. The literature agent's primary-source review is the authority for which exact published statements have been checked; this count audit makes no new blanket A assignment.

## Remaining CountIII producer: needed for unrestricted targets

For general targets the existing JX1 count/length installation still requires the actual Case-III automorphy input. In the pinned source:

`ExistsTensorFactorTower ∧ ChainRankFour ∧ ChainDesc4 ∧ RankFourChainReductionDense`

implies `PromodularityCaseThreeDense`, and the final constructor is `DenseThresholdCases/CuFinal.lean:main4_alt`. The sufficient source dependencies include the following.

| Obligation | Quantifier or compatibility feature | Classification |
|---|---|---|
| `SeedIVAlt` | For fixed Ctx3/Four base tower, complex embedding and ambient coefficients, choose an auxiliary split prime and a residual seed **before every later Dies tower**; the later seed must lie above the earlier residual datum and retain specified support/root entries. | C, open; SeedIIAlt does not prove this different statement |
| `ExistsTensorFactorTower` | Exact factor tower, tame and residual character constraints. | B, substantial finite character construction still to reconstruct |
| `ChainDesc4` | Original residual descent and chain compatibility. | B, still to reconstruct |
| `ChainRankFour` | From SomeIn to AllIn on the original residual point and PM ideal under the source dimension bound. | C, substantial geometry/propagation reconstruction |
| `RankFourChainReductionDense` | Choose T1 before every later Deep tower and preserve the seed plus Chain4 for every original residual lift. | C for the complete seeded chain producer; finite steps may separately be B |
| Identification with existing rank-four modules | An exact map is needed before borrowing old RX/CX/UX statements. | D where no such map has been written |

KA5–KA6 remove this separate list from the selected power-of-two-target cohomological route. They do not render these statements unnecessary for unrestricted Dirichlet GRH, nor prove any universal Case-III wrapper.

## Remaining CountV producer

The exact endpoint `DenseThresholdCases/CountVOf.lean:countV_of_finiteness_duality_euler_host` consumes `ThmS6_s`, LemmaM/M′, local/global finiteness, duality and Euler characteristic, normalized Poitou–Tate, `HostVanE`, `HostXpp`, `HostRigid_s` and `HostNumber_s`.

Its final numerical estimate is elementary, but claiming the endpoint closed requires the actual original-host/frame construction, local-condition identifications and normalized-length comparison. It has not been silently closed here.

| Obligation | Exact scope | Classification |
|---|---|---|
| Host/frame construction and length comparison | Original `HostData`, frame, residue characteristic, local conditions and coefficient normalization. | B, still to reconstruct |
| `HostVanE` installation | `LevelCohomology/SoHostVanE.lean` uses the already supplied LemmaK and exact local/global duality/finiteness inputs. | B, not a new deep automorphy theorem |
| `HostXpp` installation | `LevelCohomology/Xpp.lean` consumes literal CorX; residual character and prime-to-ℓ kernel quotient must be tracked. | B, not automatically closed by citing BR7 |
| `ThmS6_s` | For the original host/frame and fixed embedding, choose a single marked element before every universal representation; obtain finite weight-zero ring and all Type-I `BPrime_s` points. | C, open support/automorphy producer |
| `BPrime_s` arithmetic | Irreducibility on every open subgroup of the quartic kernel, irreducibility on its intersection with the infinite cyclotomic kernel, and exact `AutOnAlt`. | C, part of the original producer |
| `HostRigid_s` | Rigidity on that original frame, marked element and eta-kernel. | D for literature/representation matching, with potentially C producer work remaining |
| `HostNumber_s` | One growth exponent before all closures, coefficient rings, levels, characters, frames, embeddings and marked elements; controls finite pairwise nonisomorphic collections. | C, open uniform rank-three catalogue |
| Final aggregation after the above | Apply actual abstract count and normalized length inequality. | B, bounded endpoint once all joins are reconstructed |

The source's `LinkedUnlE.lean:count_v_of_printed_bound_k_reduced_unitary_lift` provides an alternative producer from broad `HypothesesH′`, LemmaK and `ThmS6Core_s`. The intermediate `EHostRigidU.hostRigidUE_alt` and `EHostNumberU.hostNumberUE_alt` use the original UnlEndLogNorm package and rank-three number theorem. These are explicit source paths, not justification for importing broad all-rank hypotheses from the narrower completed rank-four modules.

## Published-theorem boundaries

The inherited RX/CX/QX/SX/UX registries contain useful theorem certificates, but their exact scope must stay attached. This report makes no new category-A declaration for an unmatched arithmetic producer.

- RX covers its exact polarized adjoint representation and the stated infinite-cyclotomic-kernel irreducibility; it does not by its name cover every rank-three `adRep` or Kato `Used` record.
- CX covers its actual rank-four catalogue and integer/conductor normalization. A rank-three/rank-two catalogue requires an explicit adaptation or a separate exact certificate.
- SX's ordinary-control certificate is for the rank-two seed construction. It is not the rank-four six-field `HidaPropsAlt` plus characteristic-ℓ `P1core` theorem.
- Semisimplified local–global compatibility is not a certificate for full monodromy at the coefficient prime. Only the exact needed consequence should be borrowed.
- QX's conditional reconstruction can turn a correctly supplied same-ideal arithmetic support package into PMExAlt; this does not construct that package.

The parent's broader certificate registry records inherited versus independently rechecked entries. Where a named theorem lacks a source/target/hypothesis certificate at this boundary, the honest state is D, “human matching unresolved”, not A and not a defect in the checked source.

## Recommended next work

For ordinary RH, finish the global dependency audit and compare the common actual family/gap/spectral frontiers with the three cohomological inputs in the reduced cut. The highest-return bounded arithmetic continuation is the CountV original-host/frame installation or the `OneChar + CongruenceNumberRankThree → PropGK` orbit/valuation installation: each gives a complete conditional endpoint with sharp residual deep inputs. Neither should be confused with finishing the theorem.

For substantial arithmetic reconstruction, compare the actual rank-three CountI/CountV producers with the rank-four ordinary support producer on the shared RH route. Work on SeedIVAlt should be prioritized for unrestricted Dirichlet GRH only after recognizing that it contributes nothing to the selected principal-target cohomological cut. Avoid automatically extending the most recently reconstructed PMEx branch when a different unresolved common producer has greater completion value.

## Validation and limitations

`provenance.json` binds every KA claim to the exact human proof range and source declaration ranges. Twenty-one source files and twenty-six declaration ranges were checked against the pinned Git blobs. `count_frontier.json` records source-level dependency edges, exact quantifier summaries, classifications and scope distinctions. No new Lean theorem or Lean build is claimed. The draft-mode TeX syntax check passed after selecting the working project format and explicit TeX package tree; no PDF was generated. Long monospaced source paths produce layout warnings in the standalone check, confined to the final source-record paragraph. The mathematical proof was manually inspected for its source contracts and quantifier order, and KA5–KA6 received an independent cross-agent review.
