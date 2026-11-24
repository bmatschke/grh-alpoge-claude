# Reading the Alpoge–Claude RH and Dirichlet-GRH proof

Edition 0.81 proves the denominator estimate at both distinguished ramified primes. Thirteen of the fifteen denominator family fields now hold on the same family data. The middle-range and small-prime corrections remain open. The complete human-readable reconstruction has ten open obligations shared by RH and unrestricted Dirichlet GRH. [Reading guide](../RH_reconstruction_progress_v0_81.md) · [New proofs (PDF)](../RH_new_proofs_v0_81.pdf) · [Cumulative manuscript source](../RH_readable_reconstruction_v0_81.tex)

## Read and verify

| Question | Source |
| --- | --- |
| How are the contributions of the character lines controlled? | [Integral torsion](../continuation_v81/torsion.tex) · [Kernel cocycles](../continuation_v81/kernel.tex) · [Global index](../continuation_v81/index.tex) |
| Why does the local rank estimate cover both primes? | [Local row calculation](../continuation_v81/row.tex) · [Pure-sign branches](../continuation_v81/slot.tex) · [Mixed-sign branches](../continuation_v81/mixed.tex) |
| How do the local estimates yield one family inequality? | [Uniform lifting](../continuation_v81/lifting.tex) · [Ramified-prime conclusion](../continuation_v81/assembly.tex) |
| What remains? | [Middle range and small primes](../RH_reconstruction_progress_v0_81.md#where-to-resume) · [Open contracts](../continuation_v81/obligations.json) · [Checkpoint](../CURRENT_CHECKPOINT_v0_81.json) · [Validation](../continuation_v81/validation.json) |

~~~sh
python3 continuation_v81/verify.py --formal-git formal_source
pdflatex RH_new_proofs_v0_81.tex
pdflatex RH_new_proofs_v0_81.tex
~~~

## Reproduce the portable v0.58 files

The release supplied the tracked original Lean source as a compressed archive with a file manifest. To recreate those two distribution files locally from the initialized submodule, use Python 3, Git and XZ. The exporter checks both results against the original byte counts and SHA-256 digests.

```sh
python3 continuation_v58/export_source_bundle.py
sha256sum -c SHA256SUMS_v0_58
```

The second command checks every entry in the original v0.58 checksum manifest. The [delivery record](../RH_reconstruction_v0_58_delivery.json) identifies the original ZIP. For an extracted copy of that ZIP, use the [offline restore instructions](../continuation_v58/SOURCE_ACCESS.txt).
