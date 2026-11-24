# Symplectic image-density reduction — v0.28

This component proves the complete lower reduction from the three literal arithmetic assertions `Con`, `PurityAtPoints` and `AutmAlt` to the original datum's `Fin0`, `NoEnd` and `AllIrr(IsAut4Alt iota)`. The embedding `iota` is fixed before every point quantifier. It also proves the complete finite-weight-module → finite special fibre → residual trace → star obstruction chain, and the exact characteristic-zero transport from `ProModAlt`.

**It does not supply the actual `ProModAlt` witnesses, `PMExAlt`, `SeedIIAlt`, `SeedIVAlt`, or unconditional `SymplecticFourImageDense`.** The missing arithmetic realization is stated explicitly in IX.35 and in the closure ledger. The existing cohomological and model constructors do not silently fill that gap.

## Files

- `main.tex`: ten consolidated readable proofs, IX1–IX10, with the exact fixed datum, valued ambient, local flags, block directions, smallness, weak-purity normalization and quantifier order.
- `provenance.json`: exact source declarations, ranges, SHA256 hashes, pinned Git-blob comparison, human proof ranges and dependency graph.
- `closure.json`: closed implications, explicit retained arithmetic hypotheses, same-object bindings and noncircularity checks.
- `input_registry.json` and `classical_inputs.json`: supplied earlier human claims, matched primary classical statements and retained source interfaces.
- `source_locators.txt`: readable exact source links and hashes.
- `report.md`: the mathematical milestone and precise next arithmetic frontier.
- `build_provenance.py`: reproducibly regenerates the ledgers from the pinned source and current proof bytes.
- `validate_tex.py` and `tex_validation.json`: two-pass draft-mode TeX check, without producing a PDF.

## Reproduction

Run `python work/symplectic_image_density/build_provenance.py` from the project workspace. The optional `--repo` argument identifies a checkout of commit `7cbf7a0c32fca1badf05931879a37c3f8a2b03b4`. A mismatched source file fails the build.

Run `python work/symplectic_image_density/validate_tex.py` to check the chapter against the v0.27 cumulative preamble and the existing project TeX runtime. This validates syntax and references; it is not a mathematical certification or kernel replay.

No file from v0.27 or earlier is modified by this component.
