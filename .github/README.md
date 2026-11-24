# Reading the Alpoge–Claude RH and Dirichlet-GRH proof

**Edition 0.69 constructs the two automorphic seeds and puts their arithmetic points on the prescribed Hida ideals.** Given the unitary modularity-ideal theorem, the argument now gives both upper-field automorphy statements and weight-zero finiteness on the original linked frame. The exceptional two-block normalization needed in patching is also proved. [Reading guide](../RH_reconstruction_progress_v0_69.md) · [Short TeX reader](../RH_new_proofs_v0_69.tex) · [Cumulative TeX manuscript](../RH_readable_reconstruction_v0_69.tex)

**Twelve whole obligations remain**, all shared by RH and unrestricted Dirichlet GRH. The partial human reconstruction contains 4,006 indexed claims. [Current checkpoint](../CURRENT_CHECKPOINT_v0_69.json) · [Remaining contracts](../continuation_v69/obligations.json)

## Read and verify

| Argument | Source |
| --- | --- |
| The two seed representations and their local conditions | [Constructing the seeds](../continuation_v69/seeds.tex) |
| The two auxiliary runs on one frame | [Coefficient field and realizations](../continuation_v69/setup.tex) · [Arithmetic points on the ideals](../continuation_v69/point.tex) |
| Exceptional patching and the result on the linked field | [Normalizing both blocks](../continuation_v69/patching.tex) · [Linked-field conclusion](../continuation_v69/linked.tex) |
| Earlier editions | [0.68](../RH_reconstruction_progress_v0_68.md) · [0.67](../RH_reconstruction_progress_v0_67.md) · [0.66](../RH_reconstruction_progress_v0_66.md) |

From the repository root, initialize the original source and verify the claim excerpts.

~~~sh
git submodule update --init --depth=1 -- formal_source
python3 continuation_v69/verify.py --formal-git formal_source
~~~

Run `pdflatex RH_new_proofs_v0_69.tex` twice to build the short reader. [Original source pin](https://github.com/CocoSgt/riemann-hypothesis-lean/tree/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4) · [Earlier project overview](../README.md)

## Reproduce the portable v0.58 files

The release supplied the tracked original Lean source as a compressed archive with a file manifest. To recreate those two distribution files locally from the initialized submodule, use Python 3, Git and XZ. The exporter checks both results against the original byte counts and SHA-256 digests.

```sh
python3 continuation_v58/export_source_bundle.py
sha256sum -c SHA256SUMS_v0_58
```

The second command checks every entry in the original v0.58 checksum manifest. The [delivery record](../RH_reconstruction_v0_58_delivery.json) identifies the original ZIP. For an extracted copy of that ZIP, use the [offline restore instructions](../continuation_v58/SOURCE_ACCESS.txt).
