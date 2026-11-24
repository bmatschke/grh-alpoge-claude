# Reading the Alpoge–Claude RH and Dirichlet-GRH proof

**Edition 0.67 proves the rank-three component propagation theorem.** It covers the ordinary and exceptional primes of the same matrix space and returns one finite-weight ideal for the off-triangular locus. This advances the finiteness side of the shared marked theorem. [Reading guide](../RH_reconstruction_progress_v0_67.md) · [Short TeX reader](../RH_new_proofs_v0_67.tex) · [Cumulative TeX manuscript](../RH_readable_reconstruction_v0_67.tex)

**Twelve whole obligations remain**, all shared by RH and unrestricted Dirichlet GRH. Edition 0.66 closed the separate Case III seed obligation. The partial reconstruction contains 3,958 indexed claims. [Current checkpoint](../CURRENT_CHECKPOINT_v0_67.json) · [Remaining contracts](../continuation_v67/obligations.json) · [Case III seed](../RH_reconstruction_progress_v0_66.md)

## Read and verify

| Argument | Source |
| --- | --- |
| Exceptional rank-three primes | [The outer rank-two block](../continuation_v67/corner.tex) |
| Ordinary primes and propagation | [Two connecting polynomial curves](../continuation_v67/geometry.tex) · [The seed and the component theorem](../continuation_v67/regular.tex) |
| Arithmetic finite points | [Weight and point transfer](../continuation_v67/weights.tex) |
| Earlier editions | [0.66](../RH_reconstruction_progress_v0_66.md) · [0.65](../RH_reconstruction_progress_v0_65.md) · [0.64](../RH_reconstruction_progress_v0_64.md) |

From the repository root, initialize the original source and verify the claim excerpts.

~~~sh
git submodule update --init --depth=1 -- formal_source
python3 continuation_v67/verify.py --formal-git formal_source
~~~

Run `pdflatex RH_new_proofs_v0_67.tex` twice for the short reader. [Original source pin](https://github.com/CocoSgt/riemann-hypothesis-lean/tree/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4) · [Earlier project overview](../README.md)

## Reproduce the portable v0.58 files

The release supplied the tracked original Lean source as a compressed archive with a file manifest. To recreate those two distribution files locally from the initialized submodule, use Python 3, Git and XZ. The exporter checks both results against the original byte counts and SHA-256 digests.

```sh
python3 continuation_v58/export_source_bundle.py
sha256sum -c SHA256SUMS_v0_58
```

The second command checks every entry in the original v0.58 checksum manifest. The [delivery record](../RH_reconstruction_v0_58_delivery.json) identifies the original ZIP. For an extracted copy of that ZIP, use the [offline restore instructions](../continuation_v58/SOURCE_ACCESS.txt).
