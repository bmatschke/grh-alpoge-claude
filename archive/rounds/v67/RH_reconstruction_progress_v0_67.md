# Edition 0.67 · Finiteness on the marked rank-three space

The original rank-three propagation theorem is now proved in the human reconstruction. A rank-two good ideal on the same frame, and a rank-three finite-weight ideal satisfying the two prime conditions and the seed condition, give **both** conclusions of `PropagationTheoremGL3`. Every type-I prime contains the rank-three ideal after extension. One finite-weight ideal covers every off-triangular prime, including the exceptional ones. [Short TeX reader](RH_new_proofs_v0_67.tex) · [Cumulative TeX manuscript](RH_readable_reconstruction_v0_67.tex) · [Original theorem](https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AutomorphicArithmetic/AutomorphicVarieties/CurveDVRSpecialization/PropagationTheoremGL3.lean#L213-L231)

| Claims | Contribution |
| --- | --- |
| [C67E1–5](continuation_v67/corner.tex) | At an exceptional prime the outer two coordinates define a rank-two representation. The middle character and degree-zero coefficients give a single finite-weight ideal covering all such primes. |
| [G67T1–4](continuation_v67/geometry.tex) | Two explicit polynomial families connect the lower triangular locus and show that points outside the exceptional locus are dense in it. The specialization takes place on the original entry algebra. |
| [U67I1–5](continuation_v67/regular.tex) | A localized Laurent polynomial ring gives the seed prime over the required smaller coefficient prime. The seed, the connecting curves and the local component bounds prove the rank-three theorem. |
| [W67F1–4](continuation_v67/weights.tex) | Finiteness over the determinant weight algebra gives the precise radical containment on the matrix space. A good component returns a point of the original determinant ring with the prescribed characters. |

For the marked finiteness assertion, the rank-two and rank-three arithmetic setups still have to be realized on the prescribed frame. They must supply the comparison maps, finite determinant quotients, prime conditions and seed conditions used in W67F4. The upper automorphy and polarized descent assertions in the marked theorem are independent outstanding requirements. The register still counts **12 whole obligations, all shared**. The seed closed in edition 0.66 stays closed. [Marked arithmetic hypotheses](continuation_v65/marked.tex) · [Case III seed](continuation_v66/assembly.tex) · [Current contracts](continuation_v67/obligations.json)

A next step toward applying the theorem is to translate the determinant-ring hypotheses `ModIn` into the geometric hypotheses of W67F4. The original `AbsMain` proof makes this passage on the same two ideals. Its substantive inputs include a surjective comparison map in each rank, descent of local prime conditions, and passage from an arithmetic determinant point to the required seed prime. [Original consumer](https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AutomorphicArithmetic/AutomorphicVarieties/CurveDVRSpecialization/AbsMain.lean#L12-L30)

The 18 new claims bring the cumulative total to 3,958. Four chapter reviews and 124 original excerpts from 46 pinned Lean files accompany the proof. The short reader has 10 pages. The cumulative draft has 2,728 pages and retains the predecessor’s 53 overfull boxes and one duplicate hyperlink destination. The checks cover the manuscripts, graph and exact original excerpts. [Claim ledger](continuation_v67/claims.json) · [Validation](continuation_v67/validation.json) · [Previous edition](RH_reconstruction_progress_v0_66.md)

~~~sh
python3 continuation_v67/verify.py --formal-git formal_source
pdflatex RH_new_proofs_v0_67.tex
pdflatex RH_new_proofs_v0_67.tex
~~~
