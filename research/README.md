# Continuing the reconstruction

The [coverage register](../publication/audit/completeness.md) identifies proof-specific inputs that still need a human derivation or a verified reference to a peer-reviewed theorem. The [current questions](register/NEXT_STEPS.md) and [existing research modules](modules/) give the working statements and their supporting calculations. The [overview](../manuscript/overview.md) follows the route to RH and Dirichlet GRH. The [detailed contents](../publication/full/contents.json) give the precise reading order of the longer derivations.

## Working in the current layout

| Work | Where it goes |
| --- | --- |
| A derivation, counterexample to an intermediate formulation, or hypothesis check | Extend the corresponding [manuscript note](../manuscript/notes/) or [detailed chapter](../publication/full/). Add a new section to the [detailed contents](../publication/full/contents.json) if it belongs in the book. |
| Code, source ranges and a research module's supporting calculations | Use the appropriate subject in [research/modules](modules/). Keep the script and the data it checks together. |
| A change to the working obligations or dependency graph | Edit the [research register](register/), including its [selected-family checkpoint](register/SELECTED_FAMILY_CHECKPOINT.json). Run the [endpoint verifier](register/verify_selected_family.py). |
| A comparison or borrowed argument | Cite the author, theorem or section and a stable version in the chapter where it is used. Record edition-wide sources in [the bibliography and attribution notes](../publication/sources/scholarship.md). Update the [coverage register](../publication/audit/completeness.md) when the proof-specific derivation is in the manuscript. |

Four current modules record individual proofs, dependencies and original Lean line ranges. The geometric records include the marked group and its two section bases, the auxiliary-prime arc and its determinant, the four smooth intersection clauses, the two-cutoff comparison and the quantitative test for its regularized limits. The spectral records include the eighteen recursion clauses, the terminal row and the singleton Fourier calculation. Each closure file lists the family hypotheses still used. Run `python3 research/register/verify_claim_records.py --fetch-upstream` to check the excerpts against the pinned Lean source. [Galois attachment](modules/galois/polarized_galois_attachment/) · [Cyclotomic comparison](modules/galois/cyclotomic_wach_comparison/) · [Integral flags and heights](modules/geometry/good_root_tower_comparison/) · [Flag energy](modules/spectral/finite_flag_energy/)

From the repository root, run the following to check the selected-family graph and build both reading editions. The [publication guide](../publication/README.md) gives the typesetting prerequisites, output paths and release procedure.

```sh
python3 research/register/verify_selected_family.py
python3 publication/build.py --edition "$(cat publication/edition.txt)"
```

The verifier checks the registered statements, dependencies and evidence paths. Human review of the arguments and of a published theorem's hypotheses is a separate step. A historical round may report a different count because it checks the claims recorded in that round.

## Running an older round against the current sources

An older Python verifier may expect its continuation directory, source-span register and previous checkpoints as siblings at the project root. The [layout tool](../archive/legacy-layout.py) uses the [path map](../archive/path-map.tsv) to create a writable checkout with those names. It reads the current working files, including local edits. The workspace has separate files, a detached Git snapshot and access to the canonical clone's Git objects for historical lookups. Keep that clone available until edits are imported. The original source submodule is recorded as a Git link in the workspace.

With Python 3.10 or later and Git, choose a new directory outside the canonical checkout. The disk-saving option below skips the old `history/version_*` snapshot tree. Leave it off for a verifier that opens those snapshots directly.

```sh
python3 archive/legacy-layout.py export ../grh-legacy --omit-history
(
  cd ../grh-legacy
  python3 verify_selected_family.py
  python3 continuation_v80/verify.py
)
```

For the optional v80 Lean byte checks, use `python3 continuation_v80/verify.py --formal-git /path/to/alpoge-rh` inside that workspace. Supply a clone containing the formal commit named by the verifier. The v80 verification program also reads reconstruction commit `c7f1eff95ff8597171d10f1e209c41102b40a86a` through Git. Run this historical check from an export of a full clone whose history contains that public commit. A depth-one clone suffices for the export and current endpoint check. See the [v80 files](../archive/rounds/v80/continuation_v80/) for its dated register and validation program. For the exact historical files as originally committed, use a separate Git checkout of the historical commit identified by the round. The layout export uses the current working files.

For round v90, run `python3 continuation_v90/verify.py --upstream /path/to/alpoge-rh` inside the exported workspace. Both historical checks can use the public reconstruction history leading to commit [f6918db](https://github.com/bmatschke/grh-alpoge-claude/commit/f6918dbf16a8d5f4f86146fd9fa2c04efff4f8ad). Its ancestry includes the v90 baseline `4951ef2`. The [v90 register and source locators](../archive/rounds/v90/continuation_v90/) identify exactly which statements that round checks.

## Bringing edits back

Edit and run the old scripts in the exported workspace. From the **canonical repository root**, preview the import. Edited existing files already have mappings. For a new file or directory, explicitly supply both its historical name and the path where it will live. For example, a new Galois calculation could be imported with

```sh
python3 archive/legacy-layout.py import ../grh-legacy \
  --add continuation_v_next=research/modules/galois/continuation_v_next
```

Review the paths printed by the preview and run the same command with `--apply` to write them. An import that only edits existing files takes no `--add` argument.

```sh
python3 archive/legacy-layout.py import ../grh-legacy \
  --add continuation_v_next=research/modules/galois/continuation_v_next --apply
git status --short
git diff
python3 research/register/verify_selected_family.py
```

Review new files and their supplemental mapping in `archive/legacy-additions.tsv` when staging your changes. A later export reads these additions. The importer translates active Markdown links and register paths into the current layout. Archived evidence keeps its original bytes until explicitly edited. The preview reports unselected, nonignored additions left in the workspace. The importer flags a canonical file changed independently since the export if the two edits differ. Resolve that conflict in the canonical checkout and export a fresh workspace, keeping the earlier one until its edits have been recovered. Make requested deletions explicitly in the canonical checkout. The importer's file lock uses POSIX; run the import on Linux or macOS.
