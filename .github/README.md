# Human reconstruction of RH and Dirichlet GRH

Edition 0.61 proves that a finite chain of rank-four residual representations, including its polynomial links and local data, descends to one finite coefficient field and to every later enlargement. This closes **CHAIN_DESC4**, an obligation for unrestricted Dirichlet GRH. The new chapters also prove the spectral frame inequality at every sufficiently late word of a selected family and the Selmer length comparison on the original rank-three host. [New chapters (TeX)](../RH_new_proofs_v0_61.tex) · [Mathematical reading guide](../RH_reconstruction_progress_v0_61.md) · [Cumulative TeX manuscript](../RH_readable_reconstruction_v0_61.tex)

The checkpoint contains **3,820 claims and 22 open whole obligations**. Sixteen are shared by RH and Dirichlet GRH. Six more concern unrestricted Dirichlet GRH. [Current checkpoint](../CURRENT_CHECKPOINT_v0_61.json) · [Whole obligations and statements](../continuation_v61/obligations.json) · [New claims and source ranges](../continuation_v61/claims.json)

| Argument | Where to read or continue |
| --- | --- |
| Rank-four residual descent | [Complete descent proof](../chain_v61/main.tex) and the [Case-III obligations](../continuation_v61/obligations.json) |
| Spectral estimates | [Frame inequality](../frame_v61/main.tex), [kernel expansion](../expansion_v61/main.tex) and [the distinct-word bound](../frame_v61/next_source_handoff.txt) |
| Rank-three counting | [Original Selmer length](../count_v61/length.tex), [the arithmetic count](../count_v61/main.tex) and [the remaining deformation-ring comparisons](../count_v61/next_source_handoff.txt) |
| Previous edition | [The weight −2 host vanishing theorem and the spectral family hypotheses](../RH_reconstruction_progress_v0_60.md) |

## Verify or typeset this edition

From the repository root, initialize the pinned source and check the new claims, source excerpts, review hashes and obligation register.

```sh
git submodule update --init --depth=1 -- formal_source
python3 continuation_v61/verify.py --formal-git formal_source
```

Run `pdflatex RH_new_proofs_v0_61.tex` twice for the new chapters. The original proof is pinned at `7cbf7a0c32fca1badf05931879a37c3f8a2b03b4`. The historical dependency audit gives the definitions and prior evidence for the selected graph. [Pinned formal source](https://github.com/CocoSgt/riemann-hypothesis-lean/tree/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4) · [Historical reading guide](../README.md) · [Historical dependency audit](../RH_dependency_audit_v0_57.txt)

## Reproduce the portable v0.58 files

The release supplied the tracked original Lean source as a compressed archive with a file manifest. To recreate those two distribution files locally from the initialized submodule, use Python 3, Git and XZ. The exporter checks both results against the original byte counts and SHA-256 digests.

```sh
python3 continuation_v58/export_source_bundle.py
sha256sum -c SHA256SUMS_v0_58
```

The second command checks every entry in the original v0.58 checksum manifest. The [delivery record](../RH_reconstruction_v0_58_delivery.json) identifies the original ZIP. For an extracted copy of that ZIP, use the [offline restore instructions](../continuation_v58/SOURCE_ACCESS.txt).
