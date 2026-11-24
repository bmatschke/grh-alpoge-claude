# Reading the Alpoge–Claude RH and Dirichlet-GRH proof

**Edition 0.70 proves both Taylor–Wiles bounds needed for a chain of marked arithmetic points and returns the polarized representation to the original CM field.** The patching argument covers every full-block chain. At a two-block point it identifies which local construction is still needed. The descent argument preserves the strict local bounds, including at eligible places over the coefficient prime. [Reading guide](../RH_reconstruction_progress_v0_70.md) · [Short TeX reader](../RH_new_proofs_v0_70.tex) · [Cumulative TeX manuscript](../RH_readable_reconstruction_v0_70.tex)

**Twelve whole obligations remain**, all shared by RH and unrestricted Dirichlet GRH. The partial human reconstruction contains 4,038 indexed claims. [Current checkpoint](../CURRENT_CHECKPOINT_v0_70.json) · [Remaining contracts](../continuation_v70/obligations.json)

## Read and verify

| Argument | Source |
| --- | --- |
| Simultaneous detection and both arithmetic bounds | [Choosing the primes](../continuation_v70/choice.tex) · [First-order bound](../continuation_v70/bounds.tex) · [Obstruction bound](../continuation_v70/obstruction.tex) |
| General chains and the remaining two-block local input | [Prime containment](../continuation_v70/raw.tex) |
| Descent and the marked conclusion | [Polarized solvable descent](../continuation_v70/descent.tex) · [Marked theorem](../continuation_v70/return.tex) |
| Earlier editions | [0.69](../RH_reconstruction_progress_v0_69.md) · [0.68](../RH_reconstruction_progress_v0_68.md) · [0.67](../RH_reconstruction_progress_v0_67.md) |

From the repository root, initialize the original source and verify the claim excerpts.

~~~sh
git submodule update --init --depth=1 -- formal_source
python3 continuation_v70/verify.py --formal-git formal_source
~~~

Run `pdflatex RH_new_proofs_v0_70.tex` twice to build the short reader. [Original source pin](https://github.com/CocoSgt/riemann-hypothesis-lean/tree/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4) · [Earlier project overview](../README.md)

## Reproduce the portable v0.58 files

The release supplied the tracked original Lean source as a compressed archive with a file manifest. To recreate those two distribution files locally from the initialized submodule, use Python 3, Git and XZ. The exporter checks both results against the original byte counts and SHA-256 digests.

```sh
python3 continuation_v58/export_source_bundle.py
sha256sum -c SHA256SUMS_v0_58
```

The second command checks every entry in the original v0.58 checksum manifest. The [delivery record](../RH_reconstruction_v0_58_delivery.json) identifies the original ZIP. For an extracted copy of that ZIP, use the [offline restore instructions](../continuation_v58/SOURCE_ACCESS.txt).
