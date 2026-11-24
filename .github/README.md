# Human reconstruction of RH and Dirichlet GRH

Read the **[new chapters in edition 0.59 (PDF)](../RH_new_proofs_v0_59.pdf)** or start with the [mathematical reading guide](../RH_reconstruction_progress_v0_59.md). The [cumulative TeX manuscript](../RH_readable_reconstruction_v0_59.tex) includes the new chapters and the full earlier edition. The project develops a human-readable account of the pinned Alpöge–Claude Lean source.

Edition 0.59 adds the period Gram expansion on tied arithmetic data, the integral Cartier normal form and its two flag applications, the local Herr class maps, and the rank-three sharpness theorem. The checkpoint contains **3,783 claims and 24 open whole obligations**. Seventeen obligations are shared by RH and Dirichlet GRH. Seven more are specific to unrestricted Dirichlet GRH. [Current checkpoint](../CURRENT_CHECKPOINT_v0_59.json) · [Claim index](../continuation_v59/claims.json)

| To continue this argument | Next construction |
| --- | --- |
| [Automorphic periods](../period_range_v59/next_source_handoff.txt) | Choose compatible full data and comparison isometries throughout the family, then apply the diagonal and distinct-word estimates. |
| [Cartier rows](../cartier_v59/next_source_handoff.txt) | Join the odd, character and monomial blocks on the same geometric row data. |
| [Local Galois cohomology](../wach_v59/next_source_handoff.txt) | Construct crystalline evaluation and prove the quantitative comparison on the same Wach lattice. |
| [Rank-three deformation spaces](../exceptional_v59/next_source_handoff.txt) | Construct the rank-three corner ideal from rank-two support, then supply the seed for propagation. |

## Work from a checkout

From the repository root, fetch the formal source and check the edition against its pinned source ranges.

```sh
git submodule update --init --depth=1 -- formal_source
python3 continuation_v59/verify.py
```

The formal source commit is `7cbf7a0c32fca1badf05931879a37c3f8a2b03b4`. Source paths in chapter handoffs are relative to that submodule. To typeset only the new chapters locally, run `pdflatex RH_new_proofs_v0_59.tex` twice at the repository root with the packages in its preamble installed. The historical v0.57 manuscript and its v0.58 handoff remain available for earlier claims and the full dependency register. [Pinned formal source](https://github.com/CocoSgt/riemann-hypothesis-lean/tree/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4) · [Historical reading guide](../README.md) · [Dependency audit](../RH_dependency_audit_v0_57.txt)

## Reproduce the portable v0.58 files

The release supplied the tracked original Lean source as a compressed archive with a file manifest. To recreate those two distribution files locally from the initialized submodule, use Python 3, Git and XZ. The exporter checks both results against the original byte counts and SHA-256 digests.

```sh
python3 continuation_v58/export_source_bundle.py
sha256sum -c SHA256SUMS_v0_58
```

The second command checks every entry in the original v0.58 checksum manifest. The [delivery record](../RH_reconstruction_v0_58_delivery.json) identifies the original ZIP. For an extracted copy of that ZIP, use the [offline restore instructions](../continuation_v58/SOURCE_ACCESS.txt).
