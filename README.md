# A human-readable version of the formal Alpöge–Claude proof of RH and Dirichlet GRH

This project reconstructs the argument in Levent Alpöge and Claude's Lean repository for the Riemann hypothesis and the generalized Riemann hypothesis for Dirichlet characters. It maintains two reading editions and the working materials used to test and extend the reconstruction.

| Reading edition | Contents |
| --- | --- |
| [Overview in the browser](manuscript/overview.md) · [Overview PDF, latest release](https://github.com/bmatschke/grh-alpoge-claude/releases/latest/download/overview.pdf) | The route from arithmetic divisibility and bounds on periods to the exclusion of zeros off the critical line. |
| [Detailed PDF, latest release](https://github.com/bmatschke/grh-alpoge-claude/releases/latest/download/full.pdf) · [Detailed contents and editable sources](publication/full/contents.json) | The argument with its local calculations, geometric and analytic estimates, and a record of the proof-specific inputs still to be derived here. |
| [Standalone TeX, latest release](https://github.com/bmatschke/grh-alpoge-claude/releases/latest/download/proof-source.zip) · [Versioned editions](https://github.com/bmatschke/grh-alpoge-claude/releases) | Sources for compiling either PDF and fixed editions for citation. |

**Coverage.** On a selected member the manuscript constructs the marked root tower and compares the two measured period operators on a common family. It derives the convergent Siegel–Weil average and the exact hyperplane volume ratio with the prescribed local measures. The preselection volume proof accounts for its Hilbert–Samuel and trace errors before the family threshold is chosen. The remaining review includes the arithmetic models and level maps across all required windows and the uniform cuspidal trace estimates used for indefinite unitary groups. [Coverage audit](publication/audit/completeness.md) · [Geometric claim records](research/modules/geometry/good_root_tower_comparison/claims.json) · [Spectral claim records](research/modules/spectral/finite_flag_energy/claims.json)

## Continue the research

Start with the [research guide](research/README.md) and the [current mathematical questions](research/register/NEXT_STEPS.md). The editable proof is in [manuscript](manuscript/). Research modules, machine-readable obligations and the verifier are in [research](research/). The previous rounds, proofs, source-span records and checkpoint files are in [archive](archive/). The [original project history](archive/project-history.md) and [old-to-current path map](archive/path-map.tsv) locate earlier work.

From the repository root, run the current dependency check with

```sh
python3 research/register/verify_selected_family.py
```

For a session using the original top-level layout, the research guide gives commands for making a writable workspace, running a historical round there, and reviewing and importing edits. The formal Lean proof remains a Git submodule at `formal_source`. To populate it at the recorded commit, run `git submodule update --init formal_source`.

## Build or cite the manuscripts

The [publication instructions](publication/README.md) cover the PDF and HTML builds, the portable TeX archive and numbered releases. Cite the edition and source revision printed on the cover. Each edition credits the formal source and the mathematical expositions it uses. The [comparison of independent reconstructions](manuscript/guides/EXTERNAL_PROOF_COMPARISON.md) describes their contributions to particular steps.
