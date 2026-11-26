# Edition 0.71 · Closing the two-block patching argument

The marked theorem now follows from the original Hida ideal supplier, `HidaUAlt`. The new proof constructs the polarized universal matrices at a genuine two-block point, derives their local relations from the limiting Selmer conditions, and gives both prime tests for arbitrary finite chains. The cohomological hypotheses for the marked host and for patching have also been supplied. [Short TeX reader](RH_new_proofs_v0_71.tex) · [Cumulative TeX manuscript](RH_readable_reconstruction_v0_71.tex)

| Chapter | What is proved |
| --- | --- |
| [L71C1–5. Selmer conditions on the limit](continuation_v71/limits.tex) | Transfers both bounds on one normalized Taylor–Wiles system to its limiting group. Obtains the three integral Selmer tests and their Laurent-series versions, for two blocks of any permitted sizes. |
| [U71R1–6. Universal matrices](continuation_v71/urep.tex) | Constructs the source representation on the completed ring. Verifies its full determinant after extension of scalars, the test at a nonsemisimple specialization, and its continuity over the original coefficient ring. |
| [P71S1–6. Equations of the completed ring](continuation_v71/presentation.tex) | Derives the local generators, independent coefficient rows and quadratic relations. The off-diagonal generators remain present throughout the calculation. |
| [G71H1–4. Host and patching cohomology](continuation_v71/cohom.tex) | Installs the earlier local and global duality results in the original records. Checks the local invariant normalization and computes the tame symbol in its prescribed order, including for nonunit exponents. |
| [F71A1–3. Inputs for the Hida ideal](continuation_v71/hida.tex) | Gives the definite quaternion algebra with its finite-adelic splitting, weak descent to the definite unitary group with the specified spherical vectors, and the full cohomology part of the general-rank literature package, including the integral Bloch–Kato conditions. |
| [A71M1–2. Prime containment and the mark](continuation_v71/assembly.tex) | Proves `Core`, `Raw` and `PfromAut` in their original scope, then derives the entire marked conclusion from `HidaUAlt`. The mark is fixed before the universal ring and the type-I point. |

## Why the whole-obligation count is still twelve

The literal contract of `THM_S6_S` starts with host and frame data. Its conclusion gives one mark with finiteness at weight zero for every universal ring and the specified automorphy at every type-I point. The TeX proof reaches that conclusion given `HidaUAlt`. The outstanding task is to construct an ideal with all six Hida properties and its Taylor–Wiles automorphy system on **that same ideal** using the permitted original inputs. HIA2 supplies it from the larger package `Af.HypothesesH'`. [Marked contract](continuation_v71/obligations.json) · [Hida construction, HIA1–3](hida_installation_v45/main.tex)

The pinned source gives a shorter route to that package in `published_hypotheses_from_patching_alt`. Its two arguments are weak unitary descent and the four-part general-rank literature hypothesis. F71A2 supplies the first argument and F71A3 supplies the cohomology part of the second. The three other parts concern the local representation theory of general linear groups, global automorphic representations, and complex multiplication. Each contains several precise theorems. They and the intermediate suppliers in the source assembly still need to be matched to human proofs at their stated scope. [Original assembly, lines 98–103](https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AutomorphicArithmetic/AutomorphicVarieties/ModularityArgument/ThresholdArguments/DenseThresholdCases/PublishedHypothesesFromPatching.lean#L98-L103) · [Contents of the four-part hypothesis](https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AutomorphicArithmetic/AutomorphicVarieties/ModularityArgument/ThresholdArguments/DenseThresholdCases/LitAut.lean#L12-L63)

## Verification

The edition adds 26 indexed claims, bringing the total to 4,064. Each chapter has a mathematical review bound to its exact TeX. The verifier checks the manuscript, original source intervals, proof dependencies and obligation register. All 12 open whole obligations are shared by RH and unrestricted Dirichlet GRH. [Claim ledger](continuation_v71/claims.json) · [Validation and typesetting](continuation_v71/validation.json) · [Checkpoint](CURRENT_CHECKPOINT_v0_71.json)

~~~sh
python3 continuation_v71/verify.py --formal-git formal_source
pdflatex RH_new_proofs_v0_71.tex
pdflatex RH_new_proofs_v0_71.tex
~~~
