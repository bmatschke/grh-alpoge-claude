# Reading the Alpoge–Claude RH and Dirichlet-GRH proof

Edition 0.87 completes the original global denominator bound. The prescribed theta lift detects every nonzero vector at a good upper Hecke point. This proves the last two member conditions, and the common bundle selection transports the estimate to its original family. Nine whole obligations remain open, all shared by RH and unrestricted Dirichlet GRH. [Reading guide](../RH_reconstruction_progress_v0_87.md) · [New proofs (PDF)](../RH_new_proofs_v0_87.pdf) · [Cumulative manuscript source](../RH_readable_reconstruction_v0_87.tex)

| Question | Where to read |
| --- | --- |
| What forces a nonzero downward integral? | [Real matrix coefficient](../continuation_v87/definite.tex) · [Weil actions](../continuation_v87/normalization.tex) · [Doubling residue](../continuation_v87/residue.tex) |
| Why does the prescribed test detect every nonzero vector? | [Fixed Schwartz test](../continuation_v87/fixedtest.tex) · [Adjointness on the original eigenspace](../continuation_v87/return.tex) |
| Which family and which denominator are bounded? | [Joint selector](../continuation_v87/selection.tex) · [Original inequality and quantifiers](../continuation_v87/denominator.tex) |
| What has been proved on the period and height obligation? | [Support and prime contributions](../continuation_v87/periodnext.tex) · [Row lattice and Bessel identity](../continuation_v87/periodbessel.tex) |
| How is the edition checked? | [Checkpoint](../CURRENT_CHECKPOINT_v0_87.json) · [Claim ledger](../continuation_v87/claims.json) · [Original obligations](../continuation_v87/obligations.json) · [Validation](../continuation_v87/validation.json) |

~~~sh
python3 continuation_v87/verify.py --upstream formal_source
pdflatex RH_new_proofs_v0_87.tex
pdflatex RH_new_proofs_v0_87.tex
~~~

## Reproduce the portable v0.58 files

The release supplied the tracked original Lean source as a compressed archive with a file manifest. To recreate those two distribution files locally from the initialized submodule, use Python 3, Git and XZ. The exporter checks both results against the original byte counts and SHA-256 digests.

```sh
python3 continuation_v58/export_source_bundle.py
sha256sum -c SHA256SUMS_v0_58
```

The second command checks every entry in the original v0.58 checksum manifest. The [delivery record](../RH_reconstruction_v0_58_delivery.json) identifies the original ZIP. For an extracted copy of that ZIP, use the [offline restore instructions](../continuation_v58/SOURCE_ACCESS.txt).
