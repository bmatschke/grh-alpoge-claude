# Reading the Alpoge–Claude RH and Dirichlet-GRH proof

Edition 0.83 completes the middle-range denominator estimate at every eligible prime. All fifteen denominator fields now hold on the same family data under their original hypotheses. The weighted denominator bound follows on a family carrying the stated arithmetic facts. Applying it to the selected design still requires identifying the data on that family, including their transport through the good cut on the route in the formal source. The human-readable reconstruction still has **ten open obligations shared by RH and unrestricted Dirichlet GRH**. [Reading guide](../RH_reconstruction_progress_v0_83.md) · [New proofs (PDF)](../RH_new_proofs_v0_83.pdf) · [Cumulative manuscript source](../RH_readable_reconstruction_v0_83.tex)

## Read and verify

| Question | Source |
| --- | --- |
| What finishes the two remaining inert rows? | [All-thick places](../continuation_v83/thick.tex) · [Mixed places and their length bounds](../continuation_v83/mixed.tex) · [All sign orders](../RH_reconstruction_progress_v0_83.md#the-last-middle-range-rows) |
| What does the bound on the original family require? | [Assembly and denominator sum](../continuation_v83/assembly.tex) · [Transport of the four ties](../continuation_v83/tiecut.tex) · [The next comparison](../RH_reconstruction_progress_v0_83.md#where-to-resume) · [Ten open contracts](../continuation_v83/obligations.json) |
| Which estimates were already available at the other primes? | [Split, small and row B estimates in edition 0.82](../RH_reconstruction_progress_v0_82.md) |
| Where do other public reconstructions supply relevant arguments? | [Comparison of six sources](../continuation_v83/external_sources.md) · [The counting argument](../continuation_v83/cylinder.tex) · [Arithmetic flags](../continuation_v83/nearflag.tex) |
| How can the checkpoint be checked? | [Claims and source ranges](../continuation_v83/claims.json) · [Checkpoint](../CURRENT_CHECKPOINT_v0_83.json) · [Validation](../continuation_v83/validation.json) |

~~~sh
python3 continuation_v83/verify.py --formal-git formal_source
pdflatex RH_new_proofs_v0_83.tex
pdflatex RH_new_proofs_v0_83.tex
~~~

## Reproduce the portable v0.58 files

The release supplied the tracked original Lean source as a compressed archive with a file manifest. To recreate those two distribution files locally from the initialized submodule, use Python 3, Git and XZ. The exporter checks both results against the original byte counts and SHA-256 digests.

```sh
python3 continuation_v58/export_source_bundle.py
sha256sum -c SHA256SUMS_v0_58
```

The second command checks every entry in the original v0.58 checksum manifest. The [delivery record](../RH_reconstruction_v0_58_delivery.json) identifies the original ZIP. For an extracted copy of that ZIP, use the [offline restore instructions](../continuation_v58/SOURCE_ACCESS.txt).
