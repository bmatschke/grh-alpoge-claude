# Human reconstruction of RH and Dirichlet GRH

Edition 0.65 proves that the potential modularity ideal vanishes on every rank-four component through a good residual point as soon as it vanishes on one, at the original bound $d\ge 30(C+1)^2$. The new chapters also reduce the integral seed construction to three arithmetic inputs and establish the local ordinary comparison at the marked rank-three host. [Read the mathematical guide](../RH_reconstruction_progress_v0_65.md) · [New chapters in TeX](../RH_new_proofs_v0_65.tex) · [Cumulative manuscript in TeX](../RH_readable_reconstruction_v0_65.tex)

**Thirteen whole obligations remain**, twelve shared by RH and unrestricted Dirichlet GRH and one additional integral seed for unrestricted Dirichlet GRH. The reconstruction remains incomplete. [Current checkpoint](../CURRENT_CHECKPOINT_v0_65.json) · [All remaining contracts](../continuation_v65/obligations.json) · [New claim ledger](../continuation_v65/claims.json)

## Read and verify

| Argument | Source |
| --- | --- |
| Rank-four component propagation | [Two symplectic planes](../continuation_v65/planes.tex) · [Dimension bounds and propagation](../continuation_v65/component.tex) |
| Integral tensor seed | [Conditional seed theorem](../continuation_v65/seedassembly.tex) · [Source inputs still needed](../RH_reconstruction_progress_v0_65.md) |
| Marked theorem used by both routes | [Local comparison and remaining global hypotheses](../continuation_v65/marked.tex) |
| Earlier proofs | [0.64](../RH_reconstruction_progress_v0_64.md) · [0.63](../RH_reconstruction_progress_v0_63.md) · [0.62](../RH_reconstruction_progress_v0_62.md) |

From the repository root, initialize the formal source to verify the original excerpts.

~~~sh
git submodule update --init --depth=1 -- formal_source
python3 continuation_v65/verify.py --formal-git formal_source
~~~

Run `pdflatex RH_new_proofs_v0_65.tex` twice for the new reader. [Original source pin](https://github.com/CocoSgt/riemann-hypothesis-lean/tree/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4) · [Earlier project overview](../README.md)

## Reproduce the portable v0.58 files

The release supplied the tracked original Lean source as a compressed archive with a file manifest. To recreate those two distribution files locally from the initialized submodule, use Python 3, Git and XZ. The exporter checks both results against the original byte counts and SHA-256 digests.

```sh
python3 continuation_v58/export_source_bundle.py
sha256sum -c SHA256SUMS_v0_58
```

The second command checks every entry in the original v0.58 checksum manifest. The [delivery record](../RH_reconstruction_v0_58_delivery.json) identifies the original ZIP. For an extracted copy of that ZIP, use the [offline restore instructions](../continuation_v58/SOURCE_ACCESS.txt).
