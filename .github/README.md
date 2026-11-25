# Reading the Alpoge–Claude RH and Dirichlet-GRH proof

Edition 0.86 proves six more of the original member preconditions in the denominator argument, bringing the total to sixteen of eighteen. All four compatibility conditions hold. The two remaining member fields are each equivalent to one question. Does the upward theta image exhaust every good upper Hecke eigenspace? Ten whole obligations remain open, all shared by RH and unrestricted Dirichlet GRH. [Reading guide](../RH_reconstruction_progress_v0_86.md) · [New proofs (PDF)](../RH_new_proofs_v0_86.pdf) · [Cumulative manuscript source](../RH_readable_reconstruction_v0_86.tex)

| Question | Where to read |
| --- | --- |
| How is a theta parameter recovered? | [Integral Hecke points](../continuation_v86/points.tex) · [Unique upper label and lower parameter](../continuation_v86/theta.tex) |
| Where is the integral residual representation constructed? | [Residual irreducibility and descent](../continuation_v86/residual.tex) · [Original residual occurrence](../continuation_v86/rowocc.tex) |
| How do the finite types span the lower row? | [Positive scalar and dimension](../continuation_v86/membernew.tex) · [Multiplicity on the two inner forms](../continuation_v86/packet.tex) |
| What still prevents closure? | [Remaining multiplicity inequality](../continuation_v86/assembly.tex) · [Pole and fixed-test hypotheses](../continuation_v86/pole.tex) · [Selection of the original family](../continuation_v86/design86.tex) |
| How is the edition verified? | [Checkpoint](../CURRENT_CHECKPOINT_v0_86.json) · [Claim ledger](../continuation_v86/claims.json) · [Original contracts](../continuation_v86/obligations.json) · [Validation](../continuation_v86/validation.json) |

~~~sh
python3 continuation_v86/verify.py --upstream formal_source
pdflatex RH_new_proofs_v0_86.tex
pdflatex RH_new_proofs_v0_86.tex
~~~

## Reproduce the portable v0.58 files

The release supplied the tracked original Lean source as a compressed archive with a file manifest. To recreate those two distribution files locally from the initialized submodule, use Python 3, Git and XZ. The exporter checks both results against the original byte counts and SHA-256 digests.

```sh
python3 continuation_v58/export_source_bundle.py
sha256sum -c SHA256SUMS_v0_58
```

The second command checks every entry in the original v0.58 checksum manifest. The [delivery record](../RH_reconstruction_v0_58_delivery.json) identifies the original ZIP. For an extracted copy of that ZIP, use the [offline restore instructions](../continuation_v58/SOURCE_ACCESS.txt).
