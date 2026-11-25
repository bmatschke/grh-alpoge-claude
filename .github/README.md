# Reading the Alpoge–Claude RH and Dirichlet-GRH proof

Edition 0.85 proves the quantitative type-prime lifting estimate on the original potentially crystalline Galois lattices, with absolute constant 40. It also proves four more of the original member hypotheses, bringing the total to ten of eighteen. The denominator bound on the uncut family follows under the remaining selected-member hypotheses and compatibility conditions. **Ten whole obligations remain open, all shared by RH and unrestricted Dirichlet GRH.** [Reading guide](../RH_reconstruction_progress_v0_85.md) · [New proofs (PDF)](../RH_new_proofs_v0_85.pdf) · [Cumulative manuscript source](../RH_readable_reconstruction_v0_85.tex)

## Read and verify

| Question | Source |
| --- | --- |
| What is the lifting bound and how does it enter the family? | [Cocycle exponent and family theorem](../continuation_v85/assembly.tex) |
| Where does integrality enter? | [Realized models](../continuation_v85/realization.tex) · [Cokernel on lattices](../continuation_v85/connection.tex) · [Kernel](../continuation_v85/kernel.tex) · [Monodromy correction](../continuation_v85/monodromy.tex) · [Return to finite cohomology](../continuation_v85/period.tex) |
| What has been proved on the original members? | [Infinity weights](../continuation_v85/memberfield.tex) · [Spherical inert base change](../continuation_v85/basechange.tex) · [Good finite types](../continuation_v85/member.tex) · [Wild inertia](../continuation_v85/depth.tex) · [Remaining fields and ties](../RH_reconstruction_progress_v0_85.md#where-to-resume) |
| Which outside sources help? | [External reconstructions](../continuation_v83/external_sources.md) · [Crystalline comparison](../RH_reconstruction_progress_v0_85.md#which-external-results-enter) |
| How do I verify this edition? | [Source ledger](../continuation_v85/claims.json) · [Checkpoint](../CURRENT_CHECKPOINT_v0_85.json) · [Original contracts](../continuation_v85/obligations.json) · [Validation](../continuation_v85/validation.json) |

~~~sh
python3 continuation_v85/verify.py --formal-git formal_source
pdflatex RH_new_proofs_v0_85.tex
pdflatex RH_new_proofs_v0_85.tex
~~~

## Reproduce the portable v0.58 files

The release supplied the tracked original Lean source as a compressed archive with a file manifest. To recreate those two distribution files locally from the initialized submodule, use Python 3, Git and XZ. The exporter checks both results against the original byte counts and SHA-256 digests.

```sh
python3 continuation_v58/export_source_bundle.py
sha256sum -c SHA256SUMS_v0_58
```

The second command checks every entry in the original v0.58 checksum manifest. The [delivery record](../RH_reconstruction_v0_58_delivery.json) identifies the original ZIP. For an extracted copy of that ZIP, use the [offline restore instructions](../continuation_v58/SOURCE_ACCESS.txt).
