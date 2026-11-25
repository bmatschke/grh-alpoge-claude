# Reading the Alpoge–Claude RH and Dirichlet-GRH proof

Start with the [mathematical guide](../MATHEMATICAL_GUIDE.md) for the role of theta periods and divisibility, the published theorems used in the argument, and the arithmetic comparisons that remain open.

Edition 0.89 proves the uniform comparison between any two level-corrected word heights on the original selected families. It proves fullness of the word lattices, exhibits the common kernel at the terminal two lifts, and reduces the remaining complex Bessel comparison to relative periods at the base tuple with the required compatible isometries. Entries 3, 5, 8 and 9 of the period-height estimate are proved. The global denominator bound was completed in edition 0.87. Nine whole obligations remain, all shared by RH and unrestricted Dirichlet GRH. [Reading guide](../RH_reconstruction_progress_v0_89.md) · [New proofs (PDF)](../RH_new_proofs_v0_89.pdf) · [Cumulative manuscript](../RH_readable_reconstruction_v0_89.tex)

| Question | Where to read |
| --- | --- |
| Which analytic inputs can be cited directly? | [Rapid decay and finite dimensionality at fixed type](../continuation_v89/decay.tex) |
| Why does the denominator bound hold? | [Edition 0.87 guide](../RH_reconstruction_progress_v0_87.md) · [Denominator proof (PDF)](../RH_new_proofs_v0_87.pdf) |
| Where does the main term of the period error come from? | [The two distinguished prime fibres](../continuation_v87/periodnext.tex) · [Degree and level estimates](../continuation_v88/errors.tex) · [Inert-prime sums](../continuation_v88/inert.tex) |
| How are the row lattice and pairing identified on the actual family? | [Rational changes of tuple and the recorded period map](../continuation_v88/rows.tex) |
| Which period-height entries are proved? | [The corrected-height estimate](../continuation_v89/heights.tex) · [Status of all nine entries](../RH_reconstruction_progress_v0_89.md#status-of-the-nine-period-height-entries) |
| How is the edition checked? | [Checkpoint](../CURRENT_CHECKPOINT_v0_89.json) · [Claim ledger](../continuation_v89/claims.json) · [Original obligations](../continuation_v89/obligations.json) · [Validation record](../continuation_v89/validation.json) |

~~~sh
python3 continuation_v89/verify.py --upstream formal_source
pdflatex RH_new_proofs_v0_89.tex
pdflatex RH_new_proofs_v0_89.tex
~~~

## Reproduce the portable v0.58 files

The release supplied the tracked original Lean source as a compressed archive with a file manifest. To recreate those two distribution files locally from the initialized submodule, use Python 3, Git and XZ. The exporter checks both results against the original byte counts and SHA-256 digests.

```sh
python3 continuation_v58/export_source_bundle.py
sha256sum -c SHA256SUMS_v0_58
```

The second command checks every entry in the original v0.58 checksum manifest. The [delivery record](../RH_reconstruction_v0_58_delivery.json) identifies the original ZIP. For an extracted copy of that ZIP, use the [offline restore instructions](../continuation_v58/SOURCE_ACCESS.txt).
