# Reading the Alpoge–Claude RH and Dirichlet-GRH proof

Edition 0.82 proves the small-prime denominator estimate, including at 2 and 3. Fourteen of the fifteen denominator family conditions now hold for the same data. The middle-range estimate holds at every eligible split prime and every eligible inert prime in row B. The guide identifies the remaining C and D cases. The complete human-readable reconstruction has ten open obligations shared by RH and unrestricted Dirichlet GRH. [Reading guide](../RH_reconstruction_progress_v0_82.md) · [New proofs (PDF)](../RH_new_proofs_v0_82.pdf) · [Cumulative manuscript source](../RH_readable_reconstruction_v0_82.tex)

## Read and verify

| Question | Source |
| --- | --- |
| How are all places above a split prime treated at once? | [Local evaluation maps](../continuation_v82/fiber.tex) · [The common Hecke module and its determinant](../continuation_v82/column.tex) |
| Why does the small-prime estimate include 2? | [Local lifts](../continuation_v82/smalllift.tex) · [Cyclotomic character calculation](../continuation_v82/smallchar.tex) · [Uniform family bound](../continuation_v82/smallglobal.tex) |
| Which inert places are covered? | [Frobenius words](../continuation_v82/inert.tex) · [Row B](../continuation_v82/inertrow.tex) · [Rows C and D](../continuation_v82/thin.tex) · [Global comparison](../continuation_v82/inertglobal.tex) |
| How do the marked row B arcs lift? | [Cut-vector congruence](../continuation_v82/arcclass.tex) · [Integral normal forms](../continuation_v82/arcforms.tex) · [Comparison with crystalline periods](../continuation_v82/frame.tex) · [Full row B proof](../continuation_v82/rowb.tex) |
| What remains for the whole proof? | [Where to resume](../RH_reconstruction_progress_v0_82.md#where-to-resume) · [Ten open contracts](../continuation_v82/obligations.json) · [Checkpoint](../CURRENT_CHECKPOINT_v0_82.json) · [Validation](../continuation_v82/validation.json) |

~~~sh
python3 continuation_v82/verify.py --formal-git formal_source
pdflatex RH_new_proofs_v0_82.tex
pdflatex RH_new_proofs_v0_82.tex
~~~


## Reproduce the portable v0.58 files

The release supplied the tracked original Lean source as a compressed archive with a file manifest. To recreate those two distribution files locally from the initialized submodule, use Python 3, Git and XZ. The exporter checks both results against the original byte counts and SHA-256 digests.

```sh
python3 continuation_v58/export_source_bundle.py
sha256sum -c SHA256SUMS_v0_58
```

The second command checks every entry in the original v0.58 checksum manifest. The [delivery record](../RH_reconstruction_v0_58_delivery.json) identifies the original ZIP. For an extracted copy of that ZIP, use the [offline restore instructions](../continuation_v58/SOURCE_ACCESS.txt).
