# Reading the Alpoge–Claude RH and Dirichlet-GRH proof

Edition 0.84 proves the good-cut theorem for the denominator estimate, including all the norm-choice facts and the four compatibility conditions on the same cut. Six Galois preconditions and two of the four original compatibility conditions are proved on each original member. The remaining type-prime estimate is reduced to uniform integral lifting on the indicated potentially crystalline lattices. **Ten whole obligations remain open, all shared by RH and unrestricted Dirichlet GRH.** [Reading guide](../RH_reconstruction_progress_v0_84.md) · [New proofs (PDF)](../RH_new_proofs_v0_84.pdf) · [Cumulative manuscript source](../RH_readable_reconstruction_v0_84.tex)

## Read and verify

| Question | Source |
| --- | --- |
| How is the good cut constructed and what does it preserve? | [Selector and indexing correction](../continuation_v84/goodcut.tex) · [Arithmetic facts on the cut](../continuation_v84/cutfacts.tex) |
| Which hypotheses already hold on original members? | [Member data](../continuation_v84/member.tex) · [Localization uniqueness](../continuation_v84/localisation.tex) |
| How are local type-prime losses measured? | [Exact Hecke restriction indices](../continuation_v84/typeideal.tex) · [Finite local cocycles](../continuation_v84/typeplace.tex) · [Global Selmer bound](../continuation_v84/selmer.tex) |
| Where does the argument return to the uncut family? | [Family comparison](../continuation_v84/binding.tex) · [What remains](../RH_reconstruction_progress_v0_84.md#where-to-resume) |
| Which independent sources were compared? | [Source-by-source comparison](../continuation_v83/external_sources.md) · [Previous edition](../RH_reconstruction_progress_v0_83.md) |
| How is this checkpoint verified? | [Claim ledger](../continuation_v84/claims.json) · [Checkpoint](../CURRENT_CHECKPOINT_v0_84.json) · [Open contracts](../continuation_v84/obligations.json) · [Validation](../continuation_v84/validation.json) |

~~~sh
python3 continuation_v84/verify.py --formal-git formal_source
pdflatex RH_new_proofs_v0_84.tex
pdflatex RH_new_proofs_v0_84.tex
~~~

## Reproduce the portable v0.58 files

The release supplied the tracked original Lean source as a compressed archive with a file manifest. To recreate those two distribution files locally from the initialized submodule, use Python 3, Git and XZ. The exporter checks both results against the original byte counts and SHA-256 digests.

```sh
python3 continuation_v58/export_source_bundle.py
sha256sum -c SHA256SUMS_v0_58
```

The second command checks every entry in the original v0.58 checksum manifest. The [delivery record](../RH_reconstruction_v0_58_delivery.json) identifies the original ZIP. For an extracted copy of that ZIP, use the [offline restore instructions](../continuation_v58/SOURCE_ACCESS.txt).
