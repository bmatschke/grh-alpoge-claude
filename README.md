Start with [Why a chain of theta lifts can bound primes](PROOF_IDEA.md) for the mathematical idea, its classical sources and the remaining period comparison.

**Current edition 0.90.** [Reading guide](RH_reconstruction_progress_v0_90.md) · [New proofs (PDF)](RH_new_proofs_v0_90.pdf) · [Current checkpoint](CURRENT_CHECKPOINT_v0_90.json) · [Mathematical guide](MATHEMATICAL_GUIDE.md)

# RH and unrestricted Dirichlet-GRH human reconstruction — v0.57

24 November 2026

Partial human reconstruction of RH and unrestricted Dirichlet GRH, accepting the pinned formal proof as correct. Version 0.57 continues the detailed proof-note approach with 101 independently reviewed numbered claims, bringing the inventory to 3746. It completes the original rank-two component theorem, the universal conditional period Gram expansion, the determinant-jet window and its actual integral row realization, the full section-growth input through explicit classical abelian-variety theorems, and the original faithful-invariant/fixed-basis/nonlinear-decompletion/etale-functor construction. No additional whole selected obligation is closed: 24 remain, comprising 17 class C and 7 class B, with 17 shared RH/GRH and 7 additional unrestricted Dirichlet-GRH obligations. The exact original retained producer hypotheses remain explicit. GLOBAL_LOCAL_GAIN remains fully closed from v0.49. Counts are inventories, not completion percentages. No Lean replay or PDF is claimed.

## Reading order

1. `RH_reconstruction_progress_v0_57.txt`: mathematical results, methods and current boundary.
2. `RH_new_proofs_v0_57.tex`: all new proofs and the current audit.
3. `RH_readable_reconstruction_v0_57.tex`: complete cumulative manuscript.
4. `RH_GRH_reconstruction_roadmap_v0_57.txt`: updated concrete research tasks.
5. `RH_GRH_parallel_execution_plan_v0_57.txt`: independent work packages and integration requirements.
6. `RH_dependency_audit_v0_57.txt`, `continuation_checkpoint.json`, `next_source_targets.json` and `provenance.json`: full contracts and exact continuation records.

## Current inventory

101 new claims; 3746 cumulative claims. The selected sufficient graph has 121 nodes and 161 edges. 24 whole obligations remain (17 C, 7 B), comprising 17 shared RH/GRH and 7 additional GRH obligations.
New whole selected closures: none. Complete subtheorems and their retained producer premises are recorded separately. Claim counts are not a completion percentage.

## New chapters

- `arithmetic_connectedness_v57/main.tex`
- `period_gram_v57/main.tex`
- `determinant_jet_v57/main.tex`
- `section_growth_v57/main.tex`
- `faithful_etale_v57/main.tex`

## Preservation and verification

Every predecessor claim record and the entire historical cumulative proof body are preserved. Mutable v0.56 root metadata and the two supplied v0.56 plans are frozen in `history/version_0_56`. All new cited source files were compared byte-for-byte with the exact pinned Git blobs and are included in `source_snapshot_v0_57`.

Every new claim has exact proof/source ranges and an independent mathematical review. The dependency graph records the human argument; it is not a mechanically extracted Lean dependency graph. Draft TeX compilation checks syntax and references. No Lean replay, PDF generation or PDF visual certification is asserted.

The archive includes integration, assembly, validation and packaging scripts. `SHA256SUMS` binds all distributed files.

Source pin: `7cbf7a0c32fca1badf05931879a37c3f8a2b03b4`.
