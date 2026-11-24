# Human reconstruction of RH and Dirichlet GRH

Edition 0.60 proves the weight −2 Selmer vanishing theorem on the rank-three frame used by the counting argument. This closes one whole obligation shared by RH and unrestricted Dirichlet GRH. The new chapters also carry the period expansion to concrete spectral data for a family under the stated selector and frame hypotheses. [New chapters (PDF)](../RH_new_proofs_v0_60.pdf) · [Mathematical reading guide](../RH_reconstruction_progress_v0_60.md) · [Cumulative TeX manuscript](../RH_readable_reconstruction_v0_60.tex)

The checkpoint contains **3,801 claims and 23 open whole obligations**. Sixteen are shared by RH and Dirichlet GRH. Seven more concern unrestricted Dirichlet GRH. [Current checkpoint](../CURRENT_CHECKPOINT_v0_60.json) · [Whole obligations and their statements](../continuation_v60/obligations.json) · [New claim index](../continuation_v60/claims.json)

| Argument | Where to read or continue |
| --- | --- |
| Vanishing on the rank-three host | [The Dirichlet pair](../host_xpp_v60/input.tex) feeds [the proof on the chosen frame](../host_xpp_v60/main.tex). |
| Automorphic periods | [Arithmetic terms](../arf_v60/main.tex) and [the spectral family](../spectral_v60/main.tex) lead to [the numerical frame bound on a common family window](../spectral_v60/next_source_handoff.txt). |
| Cartier rows, local Galois cohomology and rank-three deformation spaces | The [edition 0.59 guide](../RH_reconstruction_progress_v0_59.md) describes the completed results and their next source endpoints. |

## Verify or typeset this edition

From the repository root, initialize the pinned source and check the new claims, source excerpts, review hashes and obligation register.

```sh
git submodule update --init --depth=1 -- formal_source
python3 continuation_v60/verify.py --formal-git formal_source
```

Run `pdflatex RH_new_proofs_v0_60.tex` twice for the new chapters. The original proof is pinned at `7cbf7a0c32fca1badf05931879a37c3f8a2b03b4`. The historical dependency audit gives the definitions and prior evidence for the selected graph. [Pinned formal source](https://github.com/CocoSgt/riemann-hypothesis-lean/tree/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4) · [Historical reading guide](../README.md) · [Historical dependency audit](../RH_dependency_audit_v0_57.txt)

## Reproduce the portable v0.58 files

The release supplied the tracked original Lean source as a compressed archive with a file manifest. To recreate those two distribution files locally from the initialized submodule, use Python 3, Git and XZ. The exporter checks both results against the original byte counts and SHA-256 digests.

```sh
python3 continuation_v58/export_source_bundle.py
sha256sum -c SHA256SUMS_v0_58
```

The second command checks every entry in the original v0.58 checksum manifest. The [delivery record](../RH_reconstruction_v0_58_delivery.json) identifies the original ZIP. For an extracted copy of that ZIP, use the [offline restore instructions](../continuation_v58/SOURCE_ACCESS.txt).
