# Reading the Alpoge–Claude RH and Dirichlet-GRH proof

Edition 0.74 proves that one normalization compares the adelic theta lift with its geometric class sum at every pinned tuple. It also proves the real Gaussian reproducing integral and the finite lattice bound used to span the base cusp space. **Ten whole obligations remain** in the human reconstruction, all shared by RH and unrestricted Dirichlet GRH. [Current reading guide](../RH_reconstruction_progress_v0_74.md) · [New TeX manuscript](../RH_new_proofs_v0_74.tex) · [Cumulative TeX manuscript](../RH_readable_reconstruction_v0_74.tex)

## Read and verify

| Question | Source |
| --- | --- |
| Why does one normalization work over all the given coefficient records? | [The marked cover](../continuation_v74/dictionary.tex) · [The point comparison](../continuation_v74/point.tex) |
| Which short theta readings already lie in the class-sum span? | [Residues and split moves](../continuation_v74/span.tex) · [Point-kernel comparison](../continuation_v74/join.tex) · [Changing the vacuum](../continuation_v74/vacuum.tex) |
| Why does the analytic kernel reproduce a form? | [Finite overlap estimate](../continuation_v74/norm.tex) · [Real reproducing integral](../continuation_v74/reproduce.tex) |
| What remains of the doubled arithmetic identity? | [Isotropic orbits, coefficients and derivatives](../continuation_v74/orbit.tex) |
| Which base assertions hold on a single linked bundle? | [Readings, rational tests, rows and rank](../continuation_v74/bundle.tex) |
| Which obligations remain open? | [Original contracts](../continuation_v74/obligations.json) · [Checkpoint](../CURRENT_CHECKPOINT_v0_74.json) · [Verification](../continuation_v74/validation.json) |

~~~sh
python3 continuation_v74/verify.py --formal-git formal_source
pdflatex RH_new_proofs_v0_74.tex
pdflatex RH_new_proofs_v0_74.tex
~~~

## Reproduce the portable v0.58 files

The release supplied the tracked original Lean source as a compressed archive with a file manifest. To recreate those two distribution files locally from the initialized submodule, use Python 3, Git and XZ. The exporter checks both results against the original byte counts and SHA-256 digests.

```sh
python3 continuation_v58/export_source_bundle.py
sha256sum -c SHA256SUMS_v0_58
```

The second command checks every entry in the original v0.58 checksum manifest. The [delivery record](../RH_reconstruction_v0_58_delivery.json) identifies the original ZIP. For an extracted copy of that ZIP, use the [offline restore instructions](../continuation_v58/SOURCE_ACCESS.txt).
