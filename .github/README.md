# Reading the Alpoge–Claude RH and Dirichlet-GRH proof

Edition 0.77 constructs the rational theta tests on each eligible pinned geometric record from its analytic map-existence condition. The rank bound follows from the context and all seven geometric comparisons follow on that record. Starting from a preliminary seed and lawful core, the manuscript also constructs the geometric record, its target coordinates and its rational base lift under the stated analytic and arithmetic hypotheses. **Ten whole obligations remain**, all shared by RH and unrestricted Dirichlet GRH. [Current reading guide](../RH_reconstruction_progress_v0_77.md) · [New TeX manuscript](../RH_new_proofs_v0_77.tex) · [Cumulative TeX manuscript](../RH_readable_reconstruction_v0_77.tex)

## Read and verify

| Question | Source |
| --- | --- |
| What gives both levels of tests on the stored theta map? | [Column theorems](../continuation_v77/column.tex) · [Rational base vector](../continuation_v77/seed.tex) |
| Where are the geometric comparisons and integral lattices proved? | [The seven fields of InGeo](../continuation_v77/geometry.tex) · [Full integral lattice, edition 0.76](../continuation_v76/full.tex) |
| Which analytic hypotheses still enter? | [Eight existence clauses](../continuation_v77/existence.tex) · [Inner theta arrows](../continuation_v77/interior.tex) |
| What does a prescribed good point supply? | [Division lattice, kernel and reciprocity](../continuation_v77/selection.tex) |
| What remains open? | [Reading guide](../RH_reconstruction_progress_v0_77.md) · [Whole contracts](../continuation_v77/obligations.json) · [Current checkpoint](../CURRENT_CHECKPOINT_v0_77.json) · [Verification](../continuation_v77/validation.json) |

~~~sh
python3 continuation_v77/verify.py --formal-git formal_source
pdflatex RH_new_proofs_v0_77.tex
pdflatex RH_new_proofs_v0_77.tex
~~~

## Reproduce the portable v0.58 files

The release supplied the tracked original Lean source as a compressed archive with a file manifest. To recreate those two distribution files locally from the initialized submodule, use Python 3, Git and XZ. The exporter checks both results against the original byte counts and SHA-256 digests.

```sh
python3 continuation_v58/export_source_bundle.py
sha256sum -c SHA256SUMS_v0_58
```

The second command checks every entry in the original v0.58 checksum manifest. The [delivery record](../RH_reconstruction_v0_58_delivery.json) identifies the original ZIP. For an extracted copy of that ZIP, use the [offline restore instructions](../continuation_v58/SOURCE_ACCESS.txt).
