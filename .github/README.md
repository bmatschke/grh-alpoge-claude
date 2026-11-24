# Reading the Alpoge–Claude RH and Dirichlet-GRH proof

**Ten whole obligations remain in the human reconstruction**, shared by RH and unrestricted Dirichlet GRH. Edition 0.72 closed the marked theorem and unramified-coefficient automorphy. Edition 0.73 continues the theta argument on the prescribed coefficient field. It constructs the higher moduli scheme on the original lower model, supplies the pinned class sum, recovers a theta kernel at any finite point of the definite group, and proves the support required on a supplied weighted point. [Current reading guide](../RH_reconstruction_progress_v0_73.md) · [New TeX chapters](../RH_new_proofs_v0_73.tex) · [Cumulative TeX manuscript](../RH_readable_reconstruction_v0_73.tex)

## Read and verify

| Question | Source |
| --- | --- |
| How does the original level acquire an upper marking? | [Higher moduli and its fibers](../continuation_v73/cover.tex) · [Framed lifts and level data](../continuation_v73/level.tex) |
| How does the higher character descend to the required coefficient field? | [Determinant and character section](../continuation_v73/tests.tex) |
| Which geometric section represents the class sum? | [Existence, uniqueness and cusp condition](../continuation_v73/compare.tex) |
| How can an integrated lift recover one given kernel value? | [Finite double-coset calculation and descent](../continuation_v73/kernel.tex) |
| Which vector supplies the support of the selected reading? | [A rational column at the distinguished place](../continuation_v73/reading.tex) |
| Where are the two most recent whole closures? | [Arithmetic proof and reading guide, edition 0.72](../RH_reconstruction_progress_v0_72.md) |
| Which obligations are still open? | [Checkpoint](../CURRENT_CHECKPOINT_v0_73.json) · [Original contracts](../continuation_v73/obligations.json) · [Validation](../continuation_v73/validation.json) |

~~~sh
python3 continuation_v73/verify.py --formal-git formal_source
pdflatex RH_new_proofs_v0_73.tex
pdflatex RH_new_proofs_v0_73.tex
~~~

## Reproduce the portable v0.58 files

The release supplied the tracked original Lean source as a compressed archive with a file manifest. To recreate those two distribution files locally from the initialized submodule, use Python 3, Git and XZ. The exporter checks both results against the original byte counts and SHA-256 digests.

```sh
python3 continuation_v58/export_source_bundle.py
sha256sum -c SHA256SUMS_v0_58
```

The second command checks every entry in the original v0.58 checksum manifest. The [delivery record](../RH_reconstruction_v0_58_delivery.json) identifies the original ZIP. For an extracted copy of that ZIP, use the [offline restore instructions](../continuation_v58/SOURCE_ACCESS.txt).
