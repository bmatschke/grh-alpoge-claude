# Edition 0.66 · The Case III seed

The Case III seed now has a human-readable proof. Fix a base tower, its marked element, its complex comparison and its ambient residue field. The construction chooses one split auxiliary prime and one residual representation. Every acceptable later tower that kills the auxiliary character then carries a compatible integral seed. This order of choices is the content of `SEED_IV_ALT`. [Short TeX reader](RH_new_proofs_v0_66.tex) · [Cumulative TeX manuscript](RH_readable_reconstruction_v0_66.tex) · [Exact original statement](https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AutomorphicArithmetic/AutomorphicVarieties/ModularityArgument/ThresholdArguments/DenseThresholdCases/PromodularityCaseThree.lean#L19-L25)

## Reading the proof

| Claims | What the argument supplies |
| --- | --- |
| [P66E1–5](continuation_v66/eisenstein.tex) | A cuspidal eigenform in every sufficiently large weight of the prescribed parity. At the auxiliary prime the Eisenstein constant reduces to zero. The ordinary quotient at the coefficient prime fixes the order of the two characters. |
| [R66P1–6](continuation_v66/ranktwo.tex) | A split auxiliary prime, the rank-two factor in a basis diagonal at the specified mark, and a single finite coefficient ring containing all its ordinary slopes. |
| [D66T1–8](continuation_v66/dihedral.tex) | A character of the specified imaginary quadratic field. All its positive powers give dihedral lattices over subsequent coefficient rings. The exact reciprocity map was constructed in CIP1. |
| [F66A1–4](continuation_v66/transfer.tex) | One of nine exponents avoids every archimedean collision. Quadratic induction produces the rank-four cusp, and the required strict bounds hold at every finite place for every attached cusp. |
| [S66C1–2](continuation_v66/assembly.tex) | The original pair, its residual support, compatibility, type A and both root entries on every allowed later tower. |

Two normalizations matter. At a prime of good reduction the ordinary newform representation has its usual arithmetic Frobenius eigenvalues. The source tests geometric Frobenius, so the cusp used for attachment is the dual of the unitary cusp twisted by the determinant norm to the power `k/2`. In quadratic induction, the geometric Satake factors change from rank two to rank four, and the resulting cusp is twisted once by the determinant norm. [Rational attachment](continuation_v66/eisenstein.tex) · [Rank-four attachment](continuation_v66/transfer.tex)

## State of the reconstruction

The count is **12 open whole obligations**, down from 13. All twelve are shared by RH and unrestricted Dirichlet GRH. The separate GRH-only leaf list is now empty. The downstream Case III modularity conclusion also uses the conditional potential-modularity input `PMEX_ALT`. This edition changes the status of the seed alone. The historical graph contains 121 nodes and 161 edges. [Original contracts and graph](continuation_v66/obligations.json) · [Checkpoint](CURRENT_CHECKPOINT_v0_66.json)

The next shared target is `THM_S6_S`. The 0.65 marked comparison requires weight-zero finiteness and automorphy over the same upper field, followed by polarized descent. For the finite part ACP11 already converts finite control of the off-triangular locus to finite-point control. The remaining arithmetic work is to construct that control on the marked space. [Marked comparison](continuation_v65/marked.tex) · [Finite-point implication](arithmetic_component_propagation_v53/main.tex) · [Descent back to the original coefficients](rank_two_connectedness_v54/main.tex)

## Verification

There are 25 new claims and 3,940 cumulative claims. Five independent chapter reviews are bound to the manuscript text. The verifier checks the new dependencies, the exact seed closure, and 184 original excerpts from 83 files at the pinned revision. This is a source and manuscript verification. The run does not rebuild Lean or certify the mathematical arguments by machine. [Claim and review ledger](continuation_v66/claims.json) · [Validation](continuation_v66/validation.json) · [Predecessor](RH_reconstruction_progress_v0_65.md)

From the repository root with the original source submodule initialized, run

~~~sh
python3 continuation_v66/verify.py --formal-git formal_source
pdflatex RH_new_proofs_v0_66.tex
pdflatex RH_new_proofs_v0_66.tex
~~~

The rational modular-form inputs include Deligne and Ribet on attachment and irreducibility, the ordinary local description for a tame newform, and Langlands–Carayol compatibility away from the coefficient prime. The rank-four argument uses the previously stated cyclic base change, automorphic induction and polarized rank-two CM compatibility. [Ribet, §2](https://doi.org/10.1007/BFb0063941) · [Skinner and Wiles](https://doi.org/10.1073/pnas.94.20.10520) · [Carayol](https://doi.org/10.24033/asens.1512) · [Previously stated transfer inputs](symplectic_automorphic_seeds/main.tex)
