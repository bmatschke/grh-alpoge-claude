# Reading the Alpoge–Claude RH and Dirichlet-GRH proof

Edition 0.79 proves two more denominator estimates on the same family hub. A prime-power annihilator on the original twisted lattice supplies the coarse bound at 7200. Local jump and inertia comparisons at the two type primes give the weighted type-prime bound. This brings the family conclusion to **11 of 15 fields** under the original family hypotheses. **Ten whole obligations remain**, all shared by RH and unrestricted Dirichlet GRH. [Reading guide](../RH_reconstruction_progress_v0_79.md) · [New proofs in PDF](../RH_new_proofs_v0_79.pdf) · [Cumulative manuscript source](../RH_readable_reconstruction_v0_79.tex)

## Read and verify

| Question | Source |
| --- | --- |
| What kills the split-column invariants? | [Chosen lattice and jumps](../continuation_v79/split.tex) · [Wach heights](../continuation_v79/heights.tex) · [Annihilator](../continuation_v79/annihilator.tex) |
| Which results hold on one family hub? | [Coarse error](../continuation_v79/assembly.tex) · [Type-prime witnesses](../continuation_v79/typewitness.tex) · [Eleven fields together](../continuation_v79/type.tex) |
| How far does the large-prime count go? | [Position tables and global congruence count](../continuation_v79/large.tex) · [Integral decomposition](../continuation_v79/decomposition.tex) · [Descent of local conditions](../continuation_v79/descent.tex) |
| What is known at $q,d$? | [Local fields and Hodge jumps](../continuation_v79/ramified.tex) |
| What remains open? | [Reading guide](../RH_reconstruction_progress_v0_79.md#where-to-resume) · [Whole contracts](../continuation_v79/obligations.json) · [Checkpoint](../CURRENT_CHECKPOINT_v0_79.json) · [Verification](../continuation_v79/validation.json) |

~~~sh
python3 continuation_v79/verify.py --formal-git formal_source
pdflatex RH_new_proofs_v0_79.tex
pdflatex RH_new_proofs_v0_79.tex
~~~

## Reproduce the portable v0.58 files

The release supplied the tracked original Lean source as a compressed archive with a file manifest. To recreate those two distribution files locally from the initialized submodule, use Python 3, Git and XZ. The exporter checks both results against the original byte counts and SHA-256 digests.

```sh
python3 continuation_v58/export_source_bundle.py
sha256sum -c SHA256SUMS_v0_58
```

The second command checks every entry in the original v0.58 checksum manifest. The [delivery record](../RH_reconstruction_v0_58_delivery.json) identifies the original ZIP. For an extracted copy of that ZIP, use the [offline restore instructions](../continuation_v58/SOURCE_ACCESS.txt).
