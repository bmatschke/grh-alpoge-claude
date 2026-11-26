# Polarized Galois attachment on the cohomological window

The cohomological window uses proposition B9.38 and its ramified consequences in B9.02. The first two groups of claims below supply these results over every CM field. The third follows the Roadmap's construction for definite unitary data at split places.

| Claims | What they establish | Editable proof |
| --- | --- | --- |
| GSPH1–6 | The published attachment has the required weights and spherical Frobenius polynomials. Its crystalline properties hold for every admissible period comparison, and semisimplicity identifies every weak attachment with it. | [Spherical attachment](../../../../manuscript/notes/galois/SPHERICAL_GALOIS_ATTACHMENT.md) |
| GRLC1–5 | Cuspidal CM lifts give the toral comparison and, under the full tame test, equality of inertia polynomials with zero monodromy. Filtered descent and the common weight give B9.02. | [Ramified comparison](../../../../manuscript/notes/galois/RAMIFIED_LOCAL_COMPARISON.md) |
| GERK1–3 | Assuming the odd-rank attachment for the lifts and the stated stable-range inputs, two families of disjoint character lines can be removed in even rank. | [Even-rank subtraction](../../../../publication/full/even-rank-attachment.md) |

Claim GUA7 in the earlier unitary assembly takes the toral clause of the polarized attachment as input. GRLC5 supplies it. The formal construction of a weak local correspondence and the stable-range hypotheses of the alternative construction have their own scopes. [Consumer GUA7](../galois_assembly_v44/main.tex#L355-L383) · [Conclusions and retained inputs](closure.json)

The claim manifest uses the line and hash conventions of round 90. Each record points into the editable manuscript and cites inclusive line ranges in the pinned Lean files. The published-input register identifies the papers, theorem numbers and claims using them. The review records in the manifest name the manuscript revisions checked. [Claim manifest](claims.json) · [Published inputs](published_inputs.json) · [Round 90 schema example](../../../../archive/rounds/v90/continuation_v90/claims.json)

From the repository root, run the following command to check the claim dependencies, manuscript and review hashes, and the upstream source excerpts. It downloads only the referenced Lean files. The detailed edition runs the manuscript checks during its build.

```sh
python3 research/register/verify_claim_records.py --fetch-upstream
```
