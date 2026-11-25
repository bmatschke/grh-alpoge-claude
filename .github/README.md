# Reading the Alpoge–Claude RH and Dirichlet-GRH proof

Start with [Why a chain of theta lifts can bound primes](../PROOF_IDEA.md). It follows the argument from an inert prime to the critical line. The [mathematical guide](../MATHEMATICAL_GUIDE.md) gives detailed matches to published theorems.

Edition 0.90 identifies the three remaining classical real-representation results needed to compare periods. It proves that the two coordinate descriptions agree on each sufficiently late selected bundle. The residual arithmetic question is whether three spaces of matrices have the required dimensions. Nine whole obligations remain, all shared by RH and unrestricted Dirichlet GRH. [Reading guide](../RH_reconstruction_progress_v0_90.md) · [New proofs (PDF)](../RH_new_proofs_v0_90.pdf) · [Cumulative manuscript](../RH_readable_reconstruction_v0_90.tex)

| Question | Where to read |
| --- | --- |
| How much period information does the slope estimate use? | [Images, quantitative spanning and the slope bound](../PERIOD_IMAGE_SPANNING.md) |
| What does the remaining Bessel comparison say? | [Three linear systems on the actual row space](../continuation_v90/intertwiners.tex) |
| Which classical results put the periods in the same spaces? | [Discrete series, compact types and smooth globalization](../RH_reconstruction_progress_v0_90.md#three-classical-inputs) · [The selected realization](../continuation_v90/join.tex) |
| Which growth and finiteness results can be cited? | [Rapid decay and finite dimensionality at fixed type](../continuation_v89/decay.tex) |
| Why does the denominator bound hold? | [Edition 0.87 guide](../RH_reconstruction_progress_v0_87.md) · [Denominator proof (PDF)](../RH_new_proofs_v0_87.pdf) |
| Where does the main term of the period error come from? | [The two distinguished prime fibres](../continuation_v87/periodnext.tex) · [Degree and level estimates](../continuation_v88/errors.tex) · [Inert-prime sums](../continuation_v88/inert.tex) |
| How are the row lattice and pairing identified on the actual family? | [Rational changes of tuple and the recorded period map](../continuation_v88/rows.tex) |
| Which period-height entries are proved? | [The corrected-height estimate](../continuation_v89/heights.tex) · [Status of all nine entries](../RH_reconstruction_progress_v0_89.md#status-of-the-nine-period-height-entries) |
| How is the edition checked? | [Checkpoint](../CURRENT_CHECKPOINT_v0_90.json) · [Claim ledger](../continuation_v90/claims.json) · [Original obligations](../continuation_v90/obligations.json) · [Validation record](../continuation_v90/validation.json) |

~~~sh
python3 continuation_v90/verify.py --upstream formal_source
pdflatex RH_new_proofs_v0_90.tex
pdflatex RH_new_proofs_v0_90.tex
~~~

## Reproduce the portable v0.58 files

The release supplied the tracked original Lean source as a compressed archive with a file manifest. To recreate those two distribution files locally from the initialized submodule, use Python 3, Git and XZ. The exporter checks both results against the original byte counts and SHA-256 digests.

```sh
python3 continuation_v58/export_source_bundle.py
sha256sum -c SHA256SUMS_v0_58
```

The second command checks every entry in the original v0.58 checksum manifest. The [delivery record](../RH_reconstruction_v0_58_delivery.json) identifies the original ZIP. For an extracted copy of that ZIP, use the [offline restore instructions](../continuation_v58/SOURCE_ACCESS.txt).
