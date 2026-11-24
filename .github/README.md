# Reading the Alpoge–Claude RH and Dirichlet-GRH proof

**Edition 0.66 constructs the Case III seed.** The proof chooses a single auxiliary prime and residual representation before any later tower is given. It supplies compatible integral lifts with the required automorphic weights and both root entries. [Guide to the proof](../RH_reconstruction_progress_v0_66.md) · [Short reader in TeX](../RH_new_proofs_v0_66.tex) · [Cumulative manuscript in TeX](../RH_readable_reconstruction_v0_66.tex)

**Twelve whole obligations remain**, all shared by RH and unrestricted Dirichlet GRH. The partial reconstruction has 3,940 indexed claims. [Current checkpoint](../CURRENT_CHECKPOINT_v0_66.json) · [Remaining contracts](../continuation_v66/obligations.json) · [New claim ledger](../continuation_v66/claims.json)

## Read and verify

| Argument | Source |
| --- | --- |
| Rational Eisenstein congruence and marked lattice | [Classical eigenform](../continuation_v66/eisenstein.tex) · [Integral lattice](../continuation_v66/ranktwo.tex) |
| Dihedral factor and rank-four transfer | [Hecke character](../continuation_v66/dihedral.tex) · [Automorphic induction](../continuation_v66/transfer.tex) |
| Seed on all later towers | [Final assembly](../continuation_v66/assembly.tex) |
| Earlier proofs | [0.65](../RH_reconstruction_progress_v0_65.md) · [0.64](../RH_reconstruction_progress_v0_64.md) · [0.63](../RH_reconstruction_progress_v0_63.md) |

From the repository root, initialize the original source and verify the claim excerpts.

~~~sh
git submodule update --init --depth=1 -- formal_source
python3 continuation_v66/verify.py --formal-git formal_source
~~~

Run `pdflatex RH_new_proofs_v0_66.tex` twice to build the short reader. [Original source pin](https://github.com/CocoSgt/riemann-hypothesis-lean/tree/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4) · [Earlier project overview](../README.md)

## Reproduce the portable v0.58 files

The release supplied the tracked original Lean source as a compressed archive with a file manifest. To recreate those two distribution files locally from the initialized submodule, use Python 3, Git and XZ. The exporter checks both results against the original byte counts and SHA-256 digests.

```sh
python3 continuation_v58/export_source_bundle.py
sha256sum -c SHA256SUMS_v0_58
```

The second command checks every entry in the original v0.58 checksum manifest. The [delivery record](../RH_reconstruction_v0_58_delivery.json) identifies the original ZIP. For an extracted copy of that ZIP, use the [offline restore instructions](../continuation_v58/SOURCE_ACCESS.txt).
