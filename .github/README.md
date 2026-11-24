# Human reconstruction of RH and Dirichlet GRH

This repository develops a detailed mathematical account of the Alpöge–Claude formal proof of RH and unrestricted Dirichlet GRH. The [v0.57 manuscript](../RH_readable_reconstruction_v0_57.tex) contains the partial reconstruction. The [v0.58 continuation guide](../RH_START_HERE_v0_58.txt) identifies the next missing arguments. The mathematical checkpoint records 3,746 claims and 24 open obligations, of which 17 are shared by RH and GRH and seven are additional obligations for unrestricted Dirichlet GRH. [Checkpoint and obligation IDs](../CURRENT_CHECKPOINT_v0_58.json)

## Continue from a Git checkout

The reconstruction files are already expanded in a clone. From the repository root, fetch the original Lean source at the commit used for the reconstruction.

```sh
git submodule update --init --depth=1 -- formal_source
git -C formal_source rev-parse HEAD
```

The expected commit is `7cbf7a0c32fca1badf05931879a37c3f8a2b03b4`. Paths beginning with `src/` in the handoff are relative to `formal_source/`. You can also browse the [pinned source on GitHub](https://github.com/CocoSgt/riemann-hypothesis-lean/tree/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4).

Start with the [progress report](../RH_reconstruction_progress_v0_57.txt), then read the [source index for the next tasks](../continuation_v58/next_tasks_source_index.txt). For each task, the index identifies the original Lean statement and the human proof to build on.

| Next construction | Existing chapter |
| --- | --- |
| Construct the local Wach data, then the Herr class maps and quantitative comparison. | [Faithful étale constructions](../faithful_etale_v57/next_source_handoff.txt) |
| Prove the rank-three exceptional presentation and follow it through the corner and propagation arguments. | [Arithmetic connectedness](../arithmetic_connectedness_v57/next_source_handoff.txt) |
| Construct the Cartier normal form required by the determinant-window theorem. | [Determinant jets](../determinant_jet_v57/next_source_handoff.txt) |
| Identify the Hilbert convolution with its scalar representative to obtain the `InHHC` range equation, then assemble the analytic identities on the same data. | [Period Gram expansion](../period_gram_v57/next_source_handoff.txt) |

For a new chat, use the [continuation prompt](../RH_NEW_CHAT_PROMPT_v0_58.txt) and specify that the project is a Git checkout. Use the submodule command above in place of the ZIP extraction instructions. The [v0.57 reading guide](../README.md) and [dependency audit](../RH_dependency_audit_v0_57.txt) give the mathematical statements and remaining hypotheses.

## Reproduce the portable v0.58 files

The release supplied the tracked original Lean source as a compressed archive with a file manifest. To recreate those two distribution files locally from the initialized submodule, use Python 3, Git and XZ. The exporter checks both results against the original byte counts and SHA-256 digests.

```sh
python3 continuation_v58/export_source_bundle.py
sha256sum -c SHA256SUMS_v0_58
```

The second command checks every entry in the original v0.58 checksum manifest. The [delivery record](../RH_reconstruction_v0_58_delivery.json) identifies the original ZIP. For an extracted copy of that ZIP, use the [offline restore instructions](../continuation_v58/SOURCE_ACCESS.txt).
