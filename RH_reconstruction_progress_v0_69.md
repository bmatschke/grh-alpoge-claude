# Edition 0.69 · The arithmetic seeds on the marked frame

Given the unitary modularity-ideal theorem `ModUAlt`, the manuscript now derives the full linked-field conclusion `LinkedEndEAlt`. On the original link it gives weight-zero finiteness over the original coefficient DVR, upper-field automorphy for the rank-three inverse-cyclotomic twist, and one algebraic twist giving upper-field automorphy in rank two. The constructions retain the same comparison with the complex numbers and the same mark through both auxiliary runs. [Short TeX reader](RH_new_proofs_v0_69.tex) · [Cumulative TeX manuscript](RH_readable_reconstruction_v0_69.tex)

| Chapter | What it supplies |
| --- | --- |
| [S69B1–5. Automorphic seeds](continuation_v69/seeds.tex) | Builds the two representations from ordinary rational eigenforms. In rank three the traceless adjoint stays irreducible on every open subgroup and its automorphic lift has the required local window even at ramified places. The classical inputs include Deligne's bound, cyclic base change and the Gelbart–Jacquet lift. |
| [C69C1–7. Arithmetic setups](continuation_v69/setup.tex) | Chooses one finite coefficient field for both twists. In each rank and for every nonzero avoidance integer it constructs a realization whose distinguished prime avoids that integer, on the given extension of the frame. |
| [P69A1–5. Points on the prescribed ideal](continuation_v69/point.tex) | Builds the determinant point from the seed, recovers its ordered local characters and proves the point satisfies the Hida ideal's own point condition. This supplies the arithmetic input to the geometric specialization proved in edition 0.68. |
| [N69E1–5. Normalization and patching](continuation_v69/patching.tex) | Proves the full normalization theorem for nice points, including the exceptional two-block case. Constructs the prime-condition argument for arbitrary finite chains from four explicit patching inputs. |
| [L69D1–4. The linked-field conclusion](continuation_v69/linked.tex) | Proves the quadratic twist and algebraic-character inputs, combines the two seeds with the prescribed points and setups, then returns the conclusion to the original coefficient ring. |

## What remains for the marked theorem

The register has **12 open whole obligations**, all shared by RH and unrestricted Dirichlet GRH. This edition settles named subtheorems inside `THM_S6_S`. Its terminal contract still requires one mark on each original host that gives weight-zero finiteness for every universal ring and the specified automorphy conclusion at every type-I point. [Marked comparison](continuation_v65/marked.tex) · [Whole contracts](continuation_v69/obligations.json)

On the patching side, the four inputs remaining in the chain argument are the simultaneous choice of detecting elements and coefficient extensions, the first-order dual bound, the Taylor–Wiles obstruction bound, and the general patched-support implication `Raw`. They must apply to the same family, including arbitrary chains of exceptional points. The Hida and cohomological hypotheses for constructing the ideal itself also have to be met in their original scope. A separate solvable descent must return the automorphy and its local window to the marked Gaussian field. A concrete next step is the simultaneous detecting choice for a finite chain, including odd directions in the two-block case. [Native patching argument](https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AutomorphicArithmetic/AutomorphicVarieties/PatchingModules/ChebotarevFamilies/PFromAutOf.lean#L30-L131) · [Hida construction](hida_installation_v45/main.tex)

## Verification

The edition adds 26 indexed claims, bringing the cumulative total to 4,006. Five mathematical reviews identify the exact TeX they cover. The verifier checks the new claims against 259 original-source intervals in 109 distinct files, the dependencies of the linked conclusion, and the obligation register against its public predecessor. These are source and manuscript checks. [Claim ledger](continuation_v69/claims.json) · [Validation and typesetting](continuation_v69/validation.json) · [Checkpoint](CURRENT_CHECKPOINT_v0_69.json)

~~~sh
python3 continuation_v69/verify.py --formal-git formal_source
pdflatex RH_new_proofs_v0_69.tex
pdflatex RH_new_proofs_v0_69.tex
~~~
