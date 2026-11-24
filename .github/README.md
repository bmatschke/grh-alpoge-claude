# Reading the Alpoge–Claude RH and Dirichlet-GRH proof

Edition 0.76 proves that the integral cusp forms on a pinned geometric row give a full lattice. For each eligible geometric column it derives the rational theta-lift tests at both prescribed levels from the original existence and geometric comparison data and the rank bound. One finite request for Weber values supplies the higher cover fields across the allowed tuples. **Ten whole obligations remain**, all shared by RH and unrestricted Dirichlet GRH. [Current reading guide](../RH_reconstruction_progress_v0_76.md) · [New TeX manuscript](../RH_new_proofs_v0_76.tex) · [Cumulative TeX manuscript](../RH_readable_reconstruction_v0_76.tex)

## Read and verify

| Question | Source |
| --- | --- |
| How do the analytic theta series become algebraic sections over the given number field? | [Short-section comparison](../continuation_v76/short.tex) · [Algebraic span](../continuation_v76/span.tex) |
| Why does the integral cusp lattice span in every positive weight? | [One denominator across all frames](../continuation_v76/integral.tex) · [Full lattice](../continuation_v76/full.tex) |
| Where do the rational coordinates of a theta lift come from? | [Base class-sum span](../continuation_v76/base.tex) · [Rationality and separating tests](../continuation_v76/ties.tex) · [Exact column hypotheses](../continuation_v76/column.tex) |
| Which field works for all higher levels on a column? | [Geometric components](../continuation_v76/field.tex) · [Finite Weber request](../continuation_v76/weber.tex) |
| Which analytic identity underlies the span? | [Edition 0.75, definite Siegel–Weil and the arithmetic kernel](../RH_reconstruction_progress_v0_75.md) |
| What remains open? | [Whole contracts](../continuation_v76/obligations.json) · [Current checkpoint](../CURRENT_CHECKPOINT_v0_76.json) · [Verification](../continuation_v76/validation.json) |

~~~sh
python3 continuation_v76/verify.py --formal-git formal_source
pdflatex RH_new_proofs_v0_76.tex
pdflatex RH_new_proofs_v0_76.tex
~~~

## Reproduce the portable v0.58 files

The release supplied the tracked original Lean source as a compressed archive with a file manifest. To recreate those two distribution files locally from the initialized submodule, use Python 3, Git and XZ. The exporter checks both results against the original byte counts and SHA-256 digests.

```sh
python3 continuation_v58/export_source_bundle.py
sha256sum -c SHA256SUMS_v0_58
```

The second command checks every entry in the original v0.58 checksum manifest. The [delivery record](../RH_reconstruction_v0_58_delivery.json) identifies the original ZIP. For an extracted copy of that ZIP, use the [offline restore instructions](../continuation_v58/SOURCE_ACCESS.txt).
