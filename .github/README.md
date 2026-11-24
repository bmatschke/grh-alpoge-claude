# Human reconstruction of RH and Dirichlet GRH

Edition 0.62 closes four human-proof obligations. In rank four it constructs the Case III specialization from the given residual chain and carries it to the automorphy conclusion at one complex embedding. In rank three it proves the normalized Selmer length comparison and the Case V count on the original host. These are conditional theorems with their arithmetic hypotheses recorded. [Mathematical reading guide](../RH_reconstruction_progress_v0_62.md) · [New chapters in TeX](../RH_new_proofs_v0_62.tex) · [Cumulative manuscript in TeX](../RH_readable_reconstruction_v0_62.tex)

The reconstruction contains **3,858 indexed claims and 18 remaining whole obligations**. Fourteen are shared by RH and Dirichlet GRH. Four more concern unrestricted Dirichlet GRH. [Current checkpoint](../CURRENT_CHECKPOINT_v0_62.json) · [Original statements of the remaining obligations](../continuation_v62/obligations.json) · [New claims and source ranges](../continuation_v62/claims.json)

| Argument | Where to read |
| --- | --- |
| Case III residual chains and automorphy | [Transport between components and the common embedding](../caseiii_v62/main.tex) |
| Case V deformation ring and counting | [Marked ring](../marked_v62/main.tex), [Selmer coordinates](../countcoord_v62/main.tex), [shape classification](../shape_v62/main.tex) and [the type-I and length arguments](../hostjoin_v62/main.tex) |
| Spectral comparison of distinct words | [Prime and dimension ratios and the selected size estimates](../offdiag_v62/main.tex) |
| Previous edition | [Finite descent of the rank-four chain](../RH_reconstruction_progress_v0_61.md) |

## Verify or typeset the manuscript

From the repository root, initialize the pinned source and check the manuscript proofs, reviewed files, dependencies and register.

~~~sh
git submodule update --init --depth=1 -- formal_source
python3 continuation_v62/verify.py --formal-git formal_source
~~~

Run <code>pdflatex RH_new_proofs_v0_62.tex</code> twice for the new chapters. The original source is pinned at <code>7cbf7a0c32fca1badf05931879a37c3f8a2b03b4</code>. [Pinned formal source](https://github.com/CocoSgt/riemann-hypothesis-lean/tree/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4) · [Earlier reading guide](../README.md) · [Historical dependency audit](../RH_dependency_audit_v0_57.txt)

## Reproduce the portable v0.58 files

The release supplied the tracked original Lean source as a compressed archive with a file manifest. To recreate those two distribution files locally from the initialized submodule, use Python 3, Git and XZ. The exporter checks both results against the original byte counts and SHA-256 digests.

```sh
python3 continuation_v58/export_source_bundle.py
sha256sum -c SHA256SUMS_v0_58
```

The second command checks every entry in the original v0.58 checksum manifest. The [delivery record](../RH_reconstruction_v0_58_delivery.json) identifies the original ZIP. For an extracted copy of that ZIP, use the [offline restore instructions](../continuation_v58/SOURCE_ACCESS.txt).
