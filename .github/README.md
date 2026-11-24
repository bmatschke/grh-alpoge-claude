# Reading the Alpoge–Claude RH and Dirichlet-GRH proof

**Edition 0.68 proves the original two-rank arithmetic reduction.** Two determinant ideals on the same frame, each satisfying the source's modularity conditions, give both good-point assertions and rank-three finite-point control. The new chapters also give the upper-field automorphy conclusion from two arithmetic runs with distinct auxiliary places. [Reading guide](../RH_reconstruction_progress_v0_68.md) · [Short TeX reader](../RH_new_proofs_v0_68.tex) · [Cumulative TeX manuscript](../RH_readable_reconstruction_v0_68.tex)

**Twelve whole obligations remain**, all shared by RH and unrestricted Dirichlet GRH. The separate Case III seed was closed in edition 0.66. The partial human reconstruction contains 3,980 indexed claims. [Current checkpoint](../CURRENT_CHECKPOINT_v0_68.json) · [Remaining contracts](../continuation_v68/obligations.json) · [Proof of the Case III seed](../RH_reconstruction_progress_v0_66.md)

## Read and verify

| Argument | Source |
| --- | --- |
| From determinant rings to matrix entries | [Comparison maps in both ranks](../continuation_v68/comparison.tex) |
| From points to primes on the right space | [Local prime conditions](../continuation_v68/primes.tex) · [Specializing the seed](../continuation_v68/seed.tex) |
| Applying the two ideals on the marked frame | [Arithmetic assembly and two runs](../continuation_v68/linked.tex) |
| Earlier editions | [0.67](../RH_reconstruction_progress_v0_67.md) · [0.66](../RH_reconstruction_progress_v0_66.md) · [0.65](../RH_reconstruction_progress_v0_65.md) |

From the repository root, initialize the original source and verify the new claim excerpts.

~~~sh
git submodule update --init --depth=1 -- formal_source
python3 continuation_v68/verify.py --formal-git formal_source
~~~

Run `pdflatex RH_new_proofs_v0_68.tex` twice to build the short reader. [Original source pin](https://github.com/CocoSgt/riemann-hypothesis-lean/tree/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4) · [Earlier project overview](../README.md)

## Reproduce the portable v0.58 files

The release supplied the tracked original Lean source as a compressed archive with a file manifest. To recreate those two distribution files locally from the initialized submodule, use Python 3, Git and XZ. The exporter checks both results against the original byte counts and SHA-256 digests.

```sh
python3 continuation_v58/export_source_bundle.py
sha256sum -c SHA256SUMS_v0_58
```

The second command checks every entry in the original v0.58 checksum manifest. The [delivery record](../RH_reconstruction_v0_58_delivery.json) identifies the original ZIP. For an extracted copy of that ZIP, use the [offline restore instructions](../continuation_v58/SOURCE_ACCESS.txt).
