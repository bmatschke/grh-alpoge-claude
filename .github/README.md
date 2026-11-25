# Reading the Alpoge–Claude RH and Dirichlet-GRH proof

Start with the [mathematical guide](../MATHEMATICAL_GUIDE.md) for the role of theta periods and divisibility, the published theorems used in the argument, and the arithmetic comparisons that remain open.

Edition 0.88 completes the weighted period-error estimate and proves full rank for the sharp and base row lattices on the original selected family. Its Bessel pairing agrees with the recorded map on rational vectors. Entries 3, 5 and 8 of the period-height estimate are proved. The original global denominator bound was completed in edition 0.87. Nine whole obligations remain, all shared by RH and unrestricted Dirichlet GRH. [Reading guide](../RH_reconstruction_progress_v0_88.md) · [New proofs (PDF)](../RH_new_proofs_v0_88.pdf) · [Cumulative manuscript source](../RH_readable_reconstruction_v0_88.tex)

| Question | Where to read |
| --- | --- |
| Why does the denominator bound hold? | [Edition 0.87 guide](../RH_reconstruction_progress_v0_87.md) · [Denominator proof (PDF)](../RH_new_proofs_v0_87.pdf) |
| Where does the main term of the period error come from? | [The two distinguished prime fibres](../continuation_v87/periodnext.tex) · [Degree and level estimates](../continuation_v88/errors.tex) · [Inert-prime sums](../continuation_v88/inert.tex) |
| How are the row lattice and pairing identified on the actual family? | [Rational changes of tuple and the recorded period map](../continuation_v88/rows.tex) |
| Which period-height entries are proved? | [One family constant and threshold](../continuation_v88/period.tex) · [The nine entries](../RH_reconstruction_progress_v0_88.md#what-remains-in-global_period_height) |
| How is the edition checked? | [Checkpoint](../CURRENT_CHECKPOINT_v0_88.json) · [Claim ledger](../continuation_v88/claims.json) · [Original obligations](../continuation_v88/obligations.json) · [Validation record](../continuation_v88/validation.json) |

~~~sh
python3 continuation_v88/verify.py --upstream formal_source
pdflatex RH_new_proofs_v0_88.tex
pdflatex RH_new_proofs_v0_88.tex
~~~

## Reproduce the portable v0.58 files

The release supplied the tracked original Lean source as a compressed archive with a file manifest. To recreate those two distribution files locally from the initialized submodule, use Python 3, Git and XZ. The exporter checks both results against the original byte counts and SHA-256 digests.

```sh
python3 continuation_v58/export_source_bundle.py
sha256sum -c SHA256SUMS_v0_58
```

The second command checks every entry in the original v0.58 checksum manifest. The [delivery record](../RH_reconstruction_v0_58_delivery.json) identifies the original ZIP. For an extracted copy of that ZIP, use the [offline restore instructions](../continuation_v58/SOURCE_ACCESS.txt).
