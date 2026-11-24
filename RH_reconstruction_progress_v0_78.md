# Edition 0.78 · The theta readings and the common denominator setup

The global denominator argument needs one set of local comparison maps on each family member. Edition 0.78 constructs them under the original Bhatt–Scholze integral hypothesis, obtains the full family setup at a uniform threshold, and obtains nine of the fifteen fields of the family conclusion on one chosen hub. They include the five numerical table estimates, the exact exceptional set with both its bounds, and all eight uniform parameter inequalities. On the theta side it constructs the Hecke actions on the preliminary seed, identifies the two eta readings under explicit local hypotheses, and supplies the ambient lattices and divisors required in both passes through the fourth stage. **Ten whole obligations remain open**, all shared by RH and unrestricted Dirichlet GRH. [Current checkpoint](CURRENT_CHECKPOINT_v0_78.json) · [Original whole contracts](continuation_v78/obligations.json)

[Read the new proofs (PDF)](RH_new_proofs_v0_78.pdf) · [New TeX manuscript](RH_new_proofs_v0_78.tex) · [Cumulative TeX manuscript](RH_readable_reconstruction_v0_78.tex) · [Previous edition](RH_reconstruction_progress_v0_77.md)

## What is available now

| Starting data | Result in this edition | Proof |
| --- | --- | --- |
| The standard preliminary seed with its coefficient models, level and place identifications, and archimedean input | The prescribed split and inert Hecke operators and the finite flag action on its ordinary and lift rows. These give the seed bridge and both standard readings. | [H78K1–H78K6](continuation_v78/hecke.tex) |
| A pinned fourth-stage record with the specified row slots | Two ambient Hermitian lattices, with the required restrictions to the stored row readings. Both native passes also admit their prescribed divisor with those row lattices, constants, prime support and local integral values. | [P78C1–P78C14](continuation_v78/producer.tex) |
| A provisional state, its localization and the stated local comparison, Hecke, lattice and spectral data | The guarded equality of the two eta readings at every required row and place. With the original analytic inputs this gives a fitted localized reader. The last proof spells out sufficient geometric and good-point inputs for its spectral and lattice assumptions. | [E78R1–E78R6](continuation_v78/reading.tex) |
| An original arithmetic datum of type D7 and the source's Bhatt–Scholze integral hypothesis | A Wach system, its functor and its comparison at every prime, with the same lattices, functor maps and period maps in all three. | [L78W1–L78W13](continuation_v78/local.tex) |
| An original family under Hypotheses₂, TwGood and FactsF | One threshold before choosing a member and its finite exceptional set. On each qualifying member there is one hub satisfying Setup and carrying the five numerical table bounds at the stated constant. | [F78D1–F78D3](continuation_v78/family.tex) · [N78T1–N78T6](continuation_v78/table.tex) |
| The canonical size and parameter records of an original family member | The exact exceptional set with its cardinality and prime bounds, and one common exponent for all eight parameter inequalities. These give `exc` and `par` on the selected hub. | [Exceptional primes](continuation_v78/exceptional.tex) · [Uniform parameters](continuation_v78/parameters.tex) |
| That same setup, with the stated additional local estimates | The coarse non-place estimate at $7200$ and a conversion of the ramified-prime polynomial estimate at $q,d$ into the original family bound. | [Coarse estimate](continuation_v78/coarse.tex) · [Assembly and ramified primes](continuation_v78/assembly.tex) |

## The common hub in the denominator proof

The earlier family argument reached the prescribed exceptional set and Selmer killing condition if furnished with compatible Wach data. The missing comparison includes Laurent coefficients at the cyclotomic points and a filtration estimate for every allowed clearing witness. The new proof starts with integral lattices in both directions, constructs the Frobenius-invariant frame on a small disc and continues it and its inverse with a common power of the logarithm. Its Laurent coefficient maps give the filtration estimate with the error constant chosen before the truncation order. Functoriality is proved for these same maps. At each good layer we therefore choose a whole tuple of Wach data, functor and comparison before taking any of its projections. This is what allows the three records to be passed together to the family theorem. [Local comparison and assembly](continuation_v78/local.tex) · [Earlier conditional family argument, SSC17](selmer_signature_comparison_v52/main.tex)

The cutoff is the maximum of the parameter, small-prime and good-twist cutoffs. After fixing a member beyond it and assuming the prescribed odd Tate–Shafarevich finiteness, we can prescribe any finite exceptional set. The constructed hub has precisely that set. Its canonical table uses the actual finite sets of good points, including the case of an empty set, and its polynomial parameter bound supplies the last band estimate. For a row parameter $C_2\ge 1$, all five estimates hold there whenever

$$
C_s\ge \max(3C_2+1,22365).
$$

The fixed number comes from $K_3=3\cdot23\cdot320+12\cdot23+9$. Rows A through D and the band condition now give the whole numerical field of the family conclusion, on the same hub as the killing field. For the exceptional set, the argument puts every integer in the exclusion windows strictly between zero and $3b$, and proves $p_*^2>8b$. Each such integer can have at most one prime divisor above $p_*$. Counting windows bounds the size of the very set prescribed to the hub. A separate ideal-counting argument bounds the host class number, and a finite general linear group count bounds the row group. Together with the family parameters these give the eight uniform parameter inequalities. [Uniform construction](continuation_v78/family.tex) · [Five estimates](continuation_v78/table.tex) · [Exceptional primes](continuation_v78/exceptional.tex) · [Uniform parameters](continuation_v78/parameters.tex)

The original family conclusion has fifteen named fields. The following accounting is conditional on the same family hypotheses as the setup. The source's earlier requirement to produce a family satisfying those hypotheses is also part of the full denominator obligation.

| Now proved together on one hub | Still required on that hub |
| --- | --- |
| `pos`, `pass`, `mult`, `rank`, `kill`, `num`, `exc`, `par`, `small` | `mid`, `bb`, `large`, `two`, `ram`, `typ` |

Here `mid` and `bb` are middle-range and coarse length estimates. The remaining four concern large primes, the small-prime bounds including 2 and 3, the distinguished ramified primes, and the two type primes. The distinguished-prime polynomial in the source is $260f^2t^2(r+t)$. Its degree is five and its coefficient sum is 520, so the common table constant already covers the numerical conversion when the polynomial estimate is available on the selected representation. [Nine-field assembly](continuation_v78/assembly.tex) · [Final family record in Lean](https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AbelianVarietyTheory/Definitions/NonGaloisDescent/BoundAtTwoThreeFamily.lean#L124-L144)

## Where the theta comparisons now meet

At a split prime the defining operator uses the inverse adelic move on the component indexed by the neighbor. At an inert prime the two finite lattice quotients determine the positive and negative elementary divisors. An integral unitary double-coset argument then identifies the full operator on the framed row. At a marked flag the right-translation formula has the inverse of the specified level character. Together these formulas give the Hecke part of the same preliminary seed used to construct a fine geometric record in edition 0.77. [Hecke operators and seed bridge](continuation_v78/hecke.tex) · [Earlier construction of a fine record](continuation_v77/seed.tex)

For eta, fix a localized realization of a provisional state. Project the integral lattice to the rational kernel complement for the numerator. Intersect the cut lattice with that complement for the denominator. Interchanging projection and intersection would change the index. Integral Hecke projectors separate the residual classes, and the local module length gains a ramification factor under scalar extension, which cancels against the normalization of the local length. At an untwisted place the sum is empty. This proves the guarded equality before using the additional analytic hypotheses that construct the reader. The proof records both the theta-cut premise used in the spectral argument and the precise coefficient-built family used for lattice stability. [Cut, normalized lengths and reader](continuation_v78/reading.tex)

The fourth-stage construction keeps the original row lattices in the divisor. At a ramified selected prime it supplies the local spherical representation and a normalized type vector. For the first local doubling step it evaluates the integral as

$$
q^{-tr}\prod_{h=1}^{r}(1-q^{-h}).
$$

The later steps in this divisor call for existence of the values. The proof takes the actual normalized integrals there. The native geometric acceptance test for the two slots is the closure of the predicate accepting any geometry. Its base constructor admits the specified model, whose section maps are zero. This identifies the exact scope of the divisor result. A stronger moduli interpretation would require additional hypotheses. [Local integrals, geometry and both divisor passes](continuation_v78/producer.tex)

## Next source obligations

1. **Denominator.** The narrower middle-range target is `bb`. Its bound at 7200 now holds at every guarded inert prime and for each empty split column. At a nonempty split column, the precise remaining input is that the power $\ell^{c_0(u)}$ annihilates the local Galois invariants in $V_T/T$ for the recorded twist at each good point. The coarse chapter proves that this bounds their normalized length by $r c_0(u)$. The `mid` field also needs the quantitative Wach estimate and the joint row B/C/D conditions. For `large`, the exact exceptional-set identity is now in hand and the large-prime congruence estimate and vanishing remain. For the bounds at 2 and 3 the further inputs include the original local row estimates. [Coarse estimate](continuation_v78/coarse.tex) · [Original middle and size estimate](https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AbelianVarietyTheory/Proofs/InertiaEigenvalues/StarAndSizeBound.lean#L21-L39) · [Final assembly](https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AbelianVarietyTheory/Proofs/InertiaEigenvalues/ConclusionOfFamilyFacts.lean#L80-L126)
2. **Common theta bundle.** The next preliminary seed construction is `exists_realDat_keep`. Its decorated reading is now supplied, and its chain and Fock models, characters and marked-group comparisons still have to be put on that same record. Produce the input stages uniformly and supply the remaining theta, column, gauge, kernel, export and retwisting data in the two-pass construction. A fitted reader built from a supplied provisional state still needs to agree with the data of the eventually selected bundle. For the size-dependent step the reciprocity record is already prescribed before the requested lower bound. [Kept preliminary datum, lines 124–142](https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AbelianVarietyTheory/Proofs/IwasawaDecomposition/ExistsAnalyticDataKeptClausesColumnChoices.lean#L124-L142) · [Two-pass construction](continuation_v78/producer.tex) · [Localized reader](continuation_v78/reading.tex) · [Prescribed point and reciprocity record](continuation_v77/selection.tex)

## Verification

Edition 0.78 adds 61 indexed claims across ten proof chapters. The repository now contains 4,378 indexed claims. The ledger binds 531 source ranges in 213 files at the pinned original revision. The verifier checks the proof blocks, source excerpts and dependencies, and compares the ten complete open contracts with their copies at the parent commit. The new proofs are human-readable mathematical arguments. Verification of their source bindings and PDFs is separate from replaying the original Lean development. [Claim ledger](continuation_v78/claims.json) · [Validation results](continuation_v78/validation.json) · [Original pinned source](https://github.com/CocoSgt/riemann-hypothesis-lean/tree/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4)

~~~sh
python3 continuation_v78/verify.py --formal-git formal_source
pdflatex RH_new_proofs_v0_78.tex
pdflatex RH_new_proofs_v0_78.tex
~~~
