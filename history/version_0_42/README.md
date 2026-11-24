# RH and Dirichlet-GRH reconstruction — v0.42

23 November 2026

Partial human reconstruction of RH and unrestricted Dirichlet GRH, assuming the pinned Alpoge–Claude Lean proof fully checked and correct. Version 0.42 supplies a complete conditional main argument, closes AdVanishK matching and full HostRigid_s, completes the original finite-level/ordinary/weight/control/Hecke-algebra/arithmetic-specialization entrance, and proves finite row estimates and sufficient quantitative simplifications. The full integral type, separating arithmetic fibers and same-ideal Hida/automorphy, common geometric/local construction, other arithmetic cases and global quantitative producers remain. No Lean build or kernel replay is claimed.

## Reading order

1. `RH_reconstruction_progress_v0_42.txt`: changes, roadmap milestones, mathematical ideas and next endpoints.
2. `RH_new_proofs_v0_42.tex`: current audit and all new proof chapters, without the historical accumulation.
3. `RH_readable_reconstruction_v0_42.tex`: cumulative manuscript, preserving all earlier proof chapters.
4. `RH_dependency_audit_v0_42.txt`: complete current selected obligation register, source references and compatibility constraints.
5. `continuation_checkpoint.json`, `next_source_targets.json`, `provenance.json` and `dependency_audit_v0_42/`: machine-readable continuation and exact contracts.

## Current boundary

154 new claims; 2363 cumulative claims. The selected graph remains 121 nodes and 161 edges. 31 whole obligations remain: 22 C and 9 B. Two former D matching obligations are closed, with no remaining D entry. This is not a percentage of proof completion.

Both rank-four Links, prime 3, fixed complex embeddings, original ideals, coefficient fields, actions, lattices, metrics, measures and uniform thresholds remain in scope. GRH means the unrestricted Dirichlet-L-function generalization in the source.

## Proof chapters

- `conditional_main_v42/main.tex`
- `host_rigidity_v42/main.tex`
- `finite_levels_v42/main.tex`
- `ordinary_structure_v42/main.tex`
- `weight_representation_v42/main.tex`
- `ordinary_control_v42/main.tex`
- `ordinary_hecke_algebra_v42/main.tex`
- `specialization_map_v42/main.tex`
- `arithmetic_specialization_v42/main.tex`
- `retained_rows_v42/main.tex`
- `global_quantitative_v42/main.tex`

Component provenance files give exact human proof ranges and pinned source ranges. The current mathematical dependency DAG is not represented as a Lean transitive dependency audit. The new `source_snapshot_v0_42/` contains the pinned source files cited by the increment; earlier snapshots are preserved.

## Verification and history

`validation_v0_42.json` records preservation, hashes, selected-graph and mathematical-DAG checks. `tex_validation.json` records draft-mode compilation and any limitations. Hash-bound mathematical reviews are in `reviews_v0_42/` and the component folders. No Lean build, kernel replay, PDF generation or visual PDF review is claimed.

All previous named files are preserved. Mutable root files from v0.41 are preserved byte-for-byte in `history/version_0_41/`. The current audit supersedes historical frontier prose; historical conditional theorems retain their hypotheses. `SHA256SUMS` covers the distributed files.

Source pin: `7cbf7a0c32fca1badf05931879a37c3f8a2b03b4`.

The integration, assembly, validation and packaging scripts are included for reproducibility. Re-running source checks requires the pinned source checkout at the path documented by those scripts.
