# Actual symplectic model construction — v0.27

Read `main.tex` for the complete proof and `report.md` for the result and scope.

The stable endpoint is **MX10**. It proves the exact intrinsic `exModel` implication and then uses **DX2/DX4/DX8** on the original good datum to obtain an actual `Model D`. The complete output field map is in `provenance.json` and `closure.json`. All previous reconstruction files are unchanged.

To regenerate exact pinned-source bindings from the shared checkout:

```sh
python work/symplectic_model_construction/build_provenance.py
```

To run the two-pass draft-only TeX check:

```sh
python work/symplectic_model_construction/validate_tex.py
```

These commands do not replay Lean or generate a PDF. Source paths are bound to commit `7cbf7a0c32fca1badf05931879a37c3f8a2b03b4`.
