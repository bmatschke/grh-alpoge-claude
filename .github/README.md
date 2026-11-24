# Reading the Alpoge–Claude RH and Dirichlet-GRH proof

**Edition 0.71 completes the patching argument at points with two residual blocks.** The prime-containment tests now hold along arbitrary finite chains. The human-readable marked theorem consequently follows from the original Hida ideal construction. The remaining premise and the parts already supplied are identified in the reading guide. [Reading guide](../RH_reconstruction_progress_v0_71.md) · [Short TeX reader](../RH_new_proofs_v0_71.tex) · [Cumulative TeX manuscript](../RH_readable_reconstruction_v0_71.tex)

**Twelve whole obligations remain**, all shared by RH and unrestricted Dirichlet GRH. The partial human reconstruction contains 4,064 indexed claims. [Current checkpoint](../CURRENT_CHECKPOINT_v0_71.json) · [Remaining contracts](../continuation_v71/obligations.json)

## Read and verify

| Argument | Source |
| --- | --- |
| The two-block patching calculation | [Selmer limits](../continuation_v71/limits.tex) · [Universal matrices](../continuation_v71/urep.tex) · [Equations](../continuation_v71/presentation.tex) |
| The arithmetic inputs | [Cohomology of the host and patching](../continuation_v71/cohom.tex) · [Three Hida inputs](../continuation_v71/hida.tex) |
| The remaining premise of the marked theorem | [Prime tests and marked conclusion](../continuation_v71/assembly.tex) |
| Earlier editions | [0.70](../RH_reconstruction_progress_v0_70.md) · [0.69](../RH_reconstruction_progress_v0_69.md) · [0.68](../RH_reconstruction_progress_v0_68.md) |

From the repository root, initialize the original source and verify the claim excerpts.

~~~sh
git submodule update --init --depth=1 -- formal_source
python3 continuation_v71/verify.py --formal-git formal_source
~~~

Run `pdflatex RH_new_proofs_v0_71.tex` twice to build the short reader. [Original source pin](https://github.com/CocoSgt/riemann-hypothesis-lean/tree/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4) · [Earlier project overview](../README.md)

## Reproduce the portable v0.58 files

The release supplied the tracked original Lean source as a compressed archive with a file manifest. To recreate those two distribution files locally from the initialized submodule, use Python 3, Git and XZ. The exporter checks both results against the original byte counts and SHA-256 digests.

```sh
python3 continuation_v58/export_source_bundle.py
sha256sum -c SHA256SUMS_v0_58
```

The second command checks every entry in the original v0.58 checksum manifest. The [delivery record](../RH_reconstruction_v0_58_delivery.json) identifies the original ZIP. For an extracted copy of that ZIP, use the [offline restore instructions](../continuation_v58/SOURCE_ACCESS.txt).
