# Edition 0.70 · Patching a chain and descending to the marked field

The marked theorem asks for one element chosen before all universal rings and ordinary points. This edition resolves two issues in that argument. It proves both Taylor–Wiles estimates for the simultaneous auxiliary choices of an arbitrary finite chain. It also descends a polarized automorphic representation to the original CM field with its prescribed local bounds. [Short TeX reader](RH_new_proofs_v0_70.tex) · [Cumulative TeX reader](RH_readable_reconstruction_v0_70.tex)

| Chapter | Result |
| --- | --- |
| [Q70C1–7. Detecting the Selmer classes](continuation_v70/choice.tex) | Constructs the auxiliary detecting tuple for the entire chain, including the independent odd directions at an exceptional two-block point. |
| [T70B1–4. First-order deformations](continuation_v70/bounds.tex) | Counts the paired first-order deformations for the actual auxiliary primes. The constant works across truncations and sufficiently high levels. |
| [U70O1–8. Obstruction classes](continuation_v70/obstruction.tex) | Obtains the second bound with one constant chosen before the truncation. Produces a coefficient vector with a unit entry even for several odd directions. |
| [R70P1–6. Moving primes along the chain](continuation_v70/raw.tex) | Proves the local dimension comparison for arbitrarily many odd generators, transports containment through each edge, and gives the complete comparison when all vertices have one block. It identifies the outstanding inputs at a genuine two-block vertex. |
| [D70W1–5. Polarized solvable descent](continuation_v70/descent.tex) | Corrects the finite character ambiguity of cyclic descent to recover the specified representation. Tracks the common center of the strict local bounds through residue degrees, including at eligible places above the coefficient prime. |
| [H70M1–2. Return to the marked theorem](continuation_v70/return.tex) | Applies both bounds and the descent theorem on the same marked host. Identifies the remaining local patching, Hida and cohomological inputs. |

## What remains open

The register still has **12 open whole obligations**, all shared by RH and unrestricted Dirichlet GRH. For the marked theorem, an arbitrary chain may contain genuine two-block vertices. There the source still needs the universal matrix algebra on the normalized completion and the presentation obtained from its limiting Selmer conditions. A count at each finite level alone does not construct either object. The original Hida and cohomological packages also occur in the marked argument. [Whole contracts](continuation_v70/obligations.json) · [Hida inputs](hida_installation_v45/main.tex) · [Preceding seed constructions](RH_reconstruction_progress_v0_69.md)

## Verification

This edition adds 32 claims to the preceding 4,006. The verifier checks the original source excerpts, the reviewed manuscript bytes, the proof dependencies and the original whole-obligation contracts. The short reader was built and the full reader typeset for comparison with the previous edition. [Claim ledger](continuation_v70/claims.json) · [Typesetting and validation](continuation_v70/validation.json) · [Checkpoint](CURRENT_CHECKPOINT_v0_70.json)

~~~sh
python3 continuation_v70/verify.py --formal-git formal_source
pdflatex RH_new_proofs_v0_70.tex
pdflatex RH_new_proofs_v0_70.tex
~~~
