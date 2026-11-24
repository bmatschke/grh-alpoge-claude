# Reading the Alpoge–Claude RH and Dirichlet-GRH proof

**Edition 0.72 closes two whole arithmetic obligations.** One Hida ideal supplies the marked theorem. On the original datum with unramified coefficients, a common marked element gives finiteness, rank-three automorphy, and the classical newform for every allowed rank-two corner. [Reading guide](../RH_reconstruction_progress_v0_72.md) · [Short TeX reader](../RH_new_proofs_v0_72.tex) · [Cumulative TeX manuscript](../RH_readable_reconstruction_v0_72.tex)

**Ten whole obligations remain**, shared by RH and unrestricted Dirichlet GRH. The partial human reconstruction contains 4,113 indexed claims. The arithmetic window and host are now supplied on both selected routes. [Current checkpoint](../CURRENT_CHECKPOINT_v0_72.json) · [Remaining contracts](../continuation_v72/obligations.json)

## Read and verify

| Argument | Source |
| --- | --- |
| Arithmetic inputs for the Hida ideal | [Local representations](../continuation_v72/local.tex) · [Crystalline comparison](../continuation_v72/crystal.tex) · [CM](../continuation_v72/cm.tex) · [Automorphy](../continuation_v72/aut.tex) · [Host hypotheses](../continuation_v72/outer.tex) |
| The marked theorem and Case V | [Hida ideal and marked conclusion](../continuation_v72/assembly.tex) |
| Unramified coefficients and the two hosts | [Common datum](../continuation_v72/datum.tex) · [Rank-two newform](../continuation_v72/corner.tex) · [Joint conclusion](../continuation_v72/return.tex) |
| Reproducibility | [Claim ledger](../continuation_v72/claims.json) · [Verification](../continuation_v72/validation.json) · [Previous edition](../RH_reconstruction_progress_v0_71.md) |

~~~sh
python3 continuation_v72/verify.py --formal-git formal_source
pdflatex RH_new_proofs_v0_72.tex
pdflatex RH_new_proofs_v0_72.tex
~~~

## Reproduce the portable v0.58 files

The release supplied the tracked original Lean source as a compressed archive with a file manifest. To recreate those two distribution files locally from the initialized submodule, use Python 3, Git and XZ. The exporter checks both results against the original byte counts and SHA-256 digests.

```sh
python3 continuation_v58/export_source_bundle.py
sha256sum -c SHA256SUMS_v0_58
```

The second command checks every entry in the original v0.58 checksum manifest. The [delivery record](../RH_reconstruction_v0_58_delivery.json) identifies the original ZIP. For an extracted copy of that ZIP, use the [offline restore instructions](../continuation_v58/SOURCE_ACCESS.txt).
