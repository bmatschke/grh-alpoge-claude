# Human reconstruction of RH and Dirichlet GRH

Edition 0.64 constructs a single Frobenius element whose trace separates every eligible rank-three point of a Case V host from its base point. The Case III chapters construct a tame tower at a prescribed label and four polynomial families connecting the restricted lattice to a seed under the source hypotheses. The marked-point chapter proves the two irreducibility upgrades and describes the remaining automorphy input. [Mathematical reading guide](../RH_reconstruction_progress_v0_64.md) · [New chapters in TeX](../RH_new_proofs_v0_64.tex) · [Cumulative manuscript in TeX](../RH_readable_reconstruction_v0_64.tex)

The manuscript has **3,886 indexed claims and 14 open whole obligations**. Twelve are common to RH and Dirichlet GRH. Two additional obligations concern unrestricted Dirichlet GRH. [Current checkpoint](../CURRENT_CHECKPOINT_v0_64.json) · [All remaining source statements](../continuation_v64/obligations.json) · [New claim ledger](../continuation_v64/claims.json)

| Argument | Chapters |
| --- | --- |
| Case V trace bound | [Host points, an inert prime and the valuation estimate](../hostnumber_v64/main.tex) |
| Case V marked theorem | [Open subgroups, the cyclotomic kernel and the joint arithmetic end](../markedaut_v64/main.tex) |
| Case III initial tower | [The four characters, local constraints and prescribed label](../tensortower_v64/main.tex) |
| Case III seeded reduction | [Cup modifications, restriction and four polynomial links](../rankchain_v64/main.tex) |
| Earlier connected arguments | [Host vanishing](../RH_reconstruction_progress_v0_63.md) and [the rank-three count and Case III automorphy](../RH_reconstruction_progress_v0_62.md) |

## Verify or typeset the manuscript

From the repository root, the following commands initialize the pinned formal source and check the new source excerpts, proof dependencies, reviews and obligation register.

~~~sh
git submodule update --init --depth=1 -- formal_source
python3 continuation_v64/verify.py --formal-git formal_source
~~~

Run `pdflatex RH_new_proofs_v0_64.tex` twice to typeset the four new chapters. [Pinned formal source](https://github.com/CocoSgt/riemann-hypothesis-lean/tree/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4) · [Earlier reading guide](../README.md) · [Dependency audit at v0.57](../RH_dependency_audit_v0_57.txt)

## Reproduce the portable v0.58 files

The release supplied the tracked original Lean source as a compressed archive with a file manifest. To recreate those two distribution files locally from the initialized submodule, use Python 3, Git and XZ. The exporter checks both results against the original byte counts and SHA-256 digests.

```sh
python3 continuation_v58/export_source_bundle.py
sha256sum -c SHA256SUMS_v0_58
```

The second command checks every entry in the original v0.58 checksum manifest. The [delivery record](../RH_reconstruction_v0_58_delivery.json) identifies the original ZIP. For an extracted copy of that ZIP, use the [offline restore instructions](../continuation_v58/SOURCE_ACCESS.txt).
