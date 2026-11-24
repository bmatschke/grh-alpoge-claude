# Reading the Alpoge–Claude RH and Dirichlet-GRH proof

Edition 0.80 proves the large-prime denominator estimate under the original family hypotheses. The proof verifies each local condition on the actual cut generators and obtains the family bound with zero additional local error. **Twelve of the fifteen denominator family fields** now hold on one hub. Ten whole obligations remain, all shared by RH and unrestricted Dirichlet GRH. [Reading guide](../RH_reconstruction_progress_v0_80.md) · [New proofs in PDF](../RH_new_proofs_v0_80.pdf) · [Cumulative manuscript source](../RH_readable_reconstruction_v0_80.tex)

## Read and verify

| Question | Source |
| --- | --- |
| Which local representations enter the count? | [Shifted crystalline data](../continuation_v80/shift.tex) · [Integral Wach calculation](../continuation_v80/wach.tex) |
| How are the finite-coefficient classes determined? | [Residual presentation](../continuation_v80/res.tex) · [Model construction](../continuation_v80/model.tex) · [Local cohomology](../continuation_v80/top.tex) |
| How does this give the estimate on the original hub? | [Cut cocycles](../continuation_v80/cut.tex) · [Family assembly](../continuation_v80/assembly.tex) |
| What remains at the ramified primes? | [Row windows, common exponent and character cohomology](../continuation_v80/ramified.tex) |
| What remains in the full proof? | [Reading guide](../RH_reconstruction_progress_v0_80.md#where-to-resume) · [Open contracts](../continuation_v80/obligations.json) · [Checkpoint](../CURRENT_CHECKPOINT_v0_80.json) · [Verification](../continuation_v80/validation.json) |

~~~sh
python3 continuation_v80/verify.py --formal-git formal_source
pdflatex RH_new_proofs_v0_80.tex
pdflatex RH_new_proofs_v0_80.tex
~~~

## Reproduce the portable v0.58 files

The release supplied the tracked original Lean source as a compressed archive with a file manifest. To recreate those two distribution files locally from the initialized submodule, use Python 3, Git and XZ. The exporter checks both results against the original byte counts and SHA-256 digests.

```sh
python3 continuation_v58/export_source_bundle.py
sha256sum -c SHA256SUMS_v0_58
```

The second command checks every entry in the original v0.58 checksum manifest. The [delivery record](../RH_reconstruction_v0_58_delivery.json) identifies the original ZIP. For an extracted copy of that ZIP, use the [offline restore instructions](../continuation_v58/SOURCE_ACCESS.txt).
