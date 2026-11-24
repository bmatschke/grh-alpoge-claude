# Reading the Alpoge–Claude RH and Dirichlet-GRH proof

Edition 0.75 proves the stable-range definite Siegel–Weil identity for the original admitted families. The proof counts split-prime neighbors and bounds the theta–Eisenstein difference uniformly over all twists and periods. It yields the differentiated arithmetic kernel for a supplied level system with the specified doubling laws. Edition 0.74 supplies the real reproducing integral and one normalization for the adelic and geometric theta lifts. **Ten whole obligations remain** in the human reconstruction, shared by RH and unrestricted Dirichlet GRH. [Current reading guide](../RH_reconstruction_progress_v0_75.md) · [New TeX manuscript](../RH_new_proofs_v0_75.tex) · [Cumulative TeX manuscript](../RH_readable_reconstruction_v0_75.tex)

## Read and verify

| Question | Source |
| --- | --- |
| Why are the two weighted series equal? | [Contraction at a split prime](../continuation_v75/definite.tex) · [Full Hecke calculation](../continuation_v75/hecke.tex) · [Induction and kernel](../continuation_v75/identity.tex) |
| What allows the infinite series, boundary limits and uniform bound? | [Absolute convergence](../continuation_v75/convergence.tex) · [Boundary limits](../continuation_v75/boundary.tex) · [Invariant norm](../continuation_v75/bounds.tex) |
| How does the argument preserve the finite tests? | [Finite Weil action from Poisson summation](../continuation_v75/weil.tex) · [Level and locality under Weil transport](../continuation_v75/admission.tex) |
| Why does an equality at zero suffice after differentiation? | [Invariant derivatives and the heat equations](../continuation_v75/heat.tex) |
| Where are the point comparison and the reproducing integral? | [Edition 0.74](../RH_reconstruction_progress_v0_74.md) |
| What is still open? | [Original contracts](../continuation_v75/obligations.json) · [Current checkpoint](../CURRENT_CHECKPOINT_v0_75.json) · [Verification](../continuation_v75/validation.json) |

~~~sh
python3 continuation_v75/verify.py --formal-git formal_source
pdflatex RH_new_proofs_v0_75.tex
pdflatex RH_new_proofs_v0_75.tex
~~~

## Reproduce the portable v0.58 files

The release supplied the tracked original Lean source as a compressed archive with a file manifest. To recreate those two distribution files locally from the initialized submodule, use Python 3, Git and XZ. The exporter checks both results against the original byte counts and SHA-256 digests.

```sh
python3 continuation_v58/export_source_bundle.py
sha256sum -c SHA256SUMS_v0_58
```

The second command checks every entry in the original v0.58 checksum manifest. The [delivery record](../RH_reconstruction_v0_58_delivery.json) identifies the original ZIP. For an extracted copy of that ZIP, use the [offline restore instructions](../continuation_v58/SOURCE_ACCESS.txt).
