# Reading the Alpoge–Claude RH and Dirichlet-GRH proof

Edition 0.78 constructs the Wach functor and its comparison at every prime under the original Bhatt–Scholze integral hypothesis. It obtains the common denominator setup throughout the specified family and proves nine of the fifteen fields on one chosen hub, including all five numerical bounds, the bounds on its exact exceptional set, and all eight uniform parameter inequalities. On the theta side the edition supplies the seed's two Hecke readings, both fourth-stage ambient lattices and divisors, and the agreement of the two localized eta formulas under explicit hypotheses. **Ten whole obligations remain**, all shared by RH and unrestricted Dirichlet GRH. [Reading guide](../RH_reconstruction_progress_v0_78.md) · [New proofs in PDF](../RH_new_proofs_v0_78.pdf) · [Cumulative manuscript source](../RH_readable_reconstruction_v0_78.tex)

## Read and verify

| Question | Source |
| --- | --- |
| What does the denominator argument now give on one family member? | [Uniform family setup](../continuation_v78/family.tex) · [Nine fields on the same hub](../continuation_v78/assembly.tex) |
| Where does its local comparison come from? | [Wach lattices, Laurent coefficients and the original comparison](../continuation_v78/local.tex) |
| How are the theta operators and the local index read? | [Hecke operators on the chosen rows](../continuation_v78/hecke.tex) · [Eta and the fitted reader](../continuation_v78/reading.tex) |
| Which fourth-stage data are now constructed? | [Ambient lattices and both divisor passes](../continuation_v78/producer.tex) |
| What remains open? | [Original whole contracts](../continuation_v78/obligations.json) · [Checkpoint](../CURRENT_CHECKPOINT_v0_78.json) · [Verification](../continuation_v78/validation.json) |

~~~sh
python3 continuation_v78/verify.py --formal-git formal_source
pdflatex RH_new_proofs_v0_78.tex
pdflatex RH_new_proofs_v0_78.tex
~~~

## Reproduce the portable v0.58 files

The release supplied the tracked original Lean source as a compressed archive with a file manifest. To recreate those two distribution files locally from the initialized submodule, use Python 3, Git and XZ. The exporter checks both results against the original byte counts and SHA-256 digests.

```sh
python3 continuation_v58/export_source_bundle.py
sha256sum -c SHA256SUMS_v0_58
```

The second command checks every entry in the original v0.58 checksum manifest. The [delivery record](../RH_reconstruction_v0_58_delivery.json) identifies the original ZIP. For an extracted copy of that ZIP, use the [offline restore instructions](../continuation_v58/SOURCE_ACCESS.txt).
