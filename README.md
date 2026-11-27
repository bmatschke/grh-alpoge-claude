# A human-readable version of the formal Alpöge–Claude proof of RH and Dirichlet GRH

This project reconstructs the argument in Levent Alpöge and Claude's Lean repository for the Riemann hypothesis and the generalized Riemann hypothesis for Dirichlet characters. It maintains two reading editions and the working materials used to test and extend the reconstruction.

| Reading edition | Contents |
| --- | --- |
| [Overview in the browser](manuscript/overview.md) · [Overview PDF, latest release](https://github.com/bmatschke/grh-alpoge-claude/releases/latest/download/overview.pdf) | The route from arithmetic divisibility and bounds on periods to the exclusion of zeros off the critical line. |
| [Detailed PDF, latest release](https://github.com/bmatschke/grh-alpoge-claude/releases/latest/download/full.pdf) · [Detailed contents and editable sources](publication/full/contents.json) | The argument with its local calculations, geometric and analytic estimates, and a record of the proof-specific inputs still to be derived here. |
| [Standalone TeX, latest release](https://github.com/bmatschke/grh-alpoge-claude/releases/latest/download/proof-source.zip) · [Versioned editions](https://github.com/bmatschke/grh-alpoge-claude/releases) | Sources for compiling either PDF and fixed editions for citation. |

**Coverage.** The manuscript derives RH and Dirichlet GRH from the inputs recorded in its coverage audit. For the height estimate it proves finiteness of the strict Selmer groups. It also proves the required bound for the full $c=(-1)^{e+1}$ contribution at odd primes on every abelian CM host, including at primes dividing the field degree. The simultaneous interval bounds the full dyadic contribution on the actual host. The remaining odd orders factor into a base term and ratios over cyclic subfields, with at most four subfields at each level of degree at least four. For general Dirichlet characters a uniform size bound for these factors is still needed. The generic case can be measured by the primitive part of an explicit even $K$-group. On each supplied self-dual host the manuscript proves the uniform indefinite counting estimate, including the flag-stabilizer measure and deep trace. The full Gram estimate, the integral models across windows and the arithmetic support argument retain the inputs detailed in the audit. [Coverage audit](publication/audit/completeness.md) · [Arithmetic claims](research/modules/galois/even_twist_selmer/claims.json) · [Two proofs of the odd-minus bound](research/modules/construction/odd_minus_bounds/) · [Spectral claims](research/modules/spectral/finite_flag_energy/claims.json) · [Geometric claims](research/modules/geometry/good_root_tower_comparison/claims.json)

In the classical RH specialization, choosing a larger gap between successive weights repairs the spacing issue identified by Adriazola. The resulting signed degree and inert-prime costs fit in the original error budget. [Weight calculation](manuscript/notes/arithmetic/WEIGHT_NODE_SPACING_ON_THE_CLASSICAL_HOST.md#claim:WNS3) · [Claims and hypotheses](research/modules/arithmetic/weight_node_spacing/)

At the original split rank-three representation the polarization bounds the central strict extension term through the odd-minus estimate. The adjacent entries can carry either sign. Their mixed cup obstruction lies in a group whose whole order is bounded independently of the auxiliary places. At level two, even cyclotomic classes admit explicit polarized families satisfying the prescribed mark, subject to one local splitting test. [Central estimate](manuscript/notes/galois/EVEN_TWISTS_AND_RANK_THREE_AUTOMORPHY.md#claim:ETS27) · [Marked extensions at level two](manuscript/notes/galois/EVEN_TWISTS_AND_RANK_THREE_AUTOMORPHY.md#claim:ETS29)

Brox's conductor-one product theorem bounds the **full unweighted** Selmer sum and each cyclic factor when combined with our window at the original cutoff 401. The argument extends to characters cut out by the real dyadic tower. For general Dirichlet characters, Roadmap B6.39 gives the exact bound conditional on the automorphic and counting inputs it develops. The comparison also identifies which finite level maps preserve integral section lattices and which signed pair bounds hold on a measured word row. [Three-issue comparison](manuscript/guides/EXTERNAL_PROOF_COMPARISON.md) · [Conductor-one transfer](manuscript/notes/galois/EVEN_TWISTS_AND_RANK_THREE_AUTOMORPHY.md#claim:ETS34) · [Integral models](manuscript/notes/periods/GOOD_ROOT_TOWER_COMPARISONS.md#claim:GRT112) · [Measured Gram operators](manuscript/notes/spectral/FLAG_BLOCK_ENERGY_AND_CUTOFF.md#claim:FBE69)

## Continue the research

Start with the [research guide](research/README.md) and the [current mathematical questions](research/register/NEXT_STEPS.md). The editable proof is in [manuscript](manuscript/). Research modules, machine-readable obligations and the verifier are in [research](research/). The previous rounds, proofs, source-span records and checkpoint files are in [archive](archive/). The [original project history](archive/project-history.md) and [old-to-current path map](archive/path-map.tsv) locate earlier work.

From the repository root, run the current dependency check with

```sh
python3 research/register/verify_selected_family.py
```

For a session using the original top-level layout, the research guide gives commands for making a writable workspace, running a historical round there, and reviewing and importing edits. The formal Lean proof remains a Git submodule at `formal_source`. To populate it at the recorded commit, run `git submodule update --init formal_source`.

## Build or cite the manuscripts

The [publication instructions](publication/README.md) cover the PDF and HTML builds, the portable TeX archive and numbered releases. Cite the edition and source revision printed on the cover. Each edition credits the formal source and the mathematical expositions it uses. The [comparison of independent reconstructions](manuscript/guides/EXTERNAL_PROOF_COMPARISON.md) describes their contributions to particular steps.
