# Edition 0.68 · From arithmetic ideals to marked points

The proof now passes from the two original arithmetic determinant ideals to the three outputs of `AbsMain`. Given rank-two and rank-three setups on the same frame, each with its own ideal satisfying `ModIn`, the result gives a good determinant point for each original ideal under its universal tests and the required finiteness statement for every rank-three weight-zero test. The subsequent two-run argument supplies the corresponding upper-field automorphy statements under its stated arithmetic hypotheses. [Short TeX reader](RH_new_proofs_v0_68.tex) · [Cumulative TeX manuscript](RH_readable_reconstruction_v0_68.tex) · [Original AbsMain proof](https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AutomorphicArithmetic/AutomorphicVarieties/CurveDVRSpecialization/AbsMain.lean#L12-L30)

| Claims | Contribution |
| --- | --- |
| [V68M1–4](continuation_v68/comparison.tex) | The twisted determinant descends as a polynomial law under arbitrary coefficient extension. Traces and local character values recover the degree-zero subring, giving the surjective comparison required in both ranks. |
| [P68K1–7](continuation_v68/primes.tex) | Points on local curves give the required original arithmetic tests. This transports the first prime condition and the rank-three exceptional-chain condition, including a chain of length zero. |
| [S68D1–6](continuation_v68/seed.tex) | An actual irreducible determinant specialization on the given ideal produces a type-I matrix prime. Its contraction contains the mapped ideal and its quotient has the exact prescribed dimension. This part works for every original comparison map satisfying `IsPhi`. |
| [A68M1–5](continuation_v68/linked.tex) | Assemble `AbsMain`, construct the seven fields of `ModIn` from the linked Hida inputs, and apply the two auxiliary runs to the same representation in each rank. |

## What the marked theorem still needs

The two-run result uses the source's modularity-ideal theorem `ModUAlt`, its weight-algebra existence theorem `LamEx`, sufficiently large coefficients, and the appropriate twists. In each rank it also uses arithmetic realizations with an auxiliary prime avoiding any specified nonzero integer. For each realization, an ideal satisfying the Hida point condition must have an actual irreducible determinant specialization. Once these are supplied, the two runs give `FinPt` on the extended frame and `AutPtAlt` in both ranks on the given link. The earlier coefficient descent returns finiteness on the original frame. The polarized descent required to finish `THM_S6_S` on its marked host still has its own hypotheses. [Exact two-run premises](https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AutomorphicArithmetic/AutomorphicVarieties/ModularityArgument/ThresholdArguments/DenseThresholdCases/TwoRuns.lean#L79-L110) · [Original marked comparison](continuation_v65/marked.tex)

A concrete next target is `seedPtOf_alt` on the chosen rank-three realization. Here the direction matters. The current chapter starts with an irreducible determinant specialization and constructs a geometric seed prime. The preceding arithmetic step must start with the prescribed ordinary automorphic seed, realize it as a point of that same Hida determinant ring, and show that this particular point kills the Hida ideal. The source names the character, twist, congruence and local inertia hypotheses for doing so. Supplying that point would remove one input to the marked argument while leaving the other named inputs visible. [Arithmetic point construction](https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AutomorphicArithmetic/AutomorphicVarieties/ModularityArgument/ThresholdArguments/DenseThresholdCases/PrSeedPtOf.lean#L157-L258) · [Geometric specialization proved here](continuation_v68/seed.tex)

The register contains **12 open whole obligations**, all shared by RH and unrestricted Dirichlet GRH. Edition 0.66 closed the additional Case III seed. Edition 0.67 proved the component theorem used in this edition. [Case III seed](RH_reconstruction_progress_v0_66.md) · [Rank-three propagation](RH_reconstruction_progress_v0_67.md) · [All open contracts](continuation_v68/obligations.json)

## Verification

The 22 new claims bring the cumulative total to 3,980. Four reviews are bound to the respective manuscripts. The verifier checks the source-range ledger, dependence of the final conclusion on the component proofs, and the obligation graph against the public predecessor. All 205 indexed excerpts in 61 original files can be verified using the pinned submodule. These checks validate source correspondence and bookkeeping. Mathematical review is recorded separately from these checks. [Claim ledger and reviews](continuation_v68/claims.json) · [Typesetting and source validation](continuation_v68/validation.json) · [Checkpoint](CURRENT_CHECKPOINT_v0_68.json)

~~~sh
python3 continuation_v68/verify.py --formal-git formal_source
pdflatex RH_new_proofs_v0_68.tex
pdflatex RH_new_proofs_v0_68.tex
~~~
