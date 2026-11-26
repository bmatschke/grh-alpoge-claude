# Edition 0.62 · Four obligations in the human reconstruction

The new chapters prove two implications for Case III of the Dirichlet-GRH argument and two for the Case V count shared by RH and Dirichlet GRH. Each is proved under its original hypotheses. The register now has **18 open whole obligations**, down from 22 in edition 0.61. Fourteen are shared and four are additional for unrestricted Dirichlet GRH. The edition contains 38 new claims, bringing the cumulative total to 3,858. [New chapters in TeX](RH_new_proofs_v0_62.tex) · [Cumulative manuscript in TeX](RH_readable_reconstruction_v0_62.tex)

| Original obligation | Result in this edition | Proof |
| --- | --- | --- |
| TASK_CASE3_PROMOD_JOIN | From the rank-four tower, seed, component and chain hypotheses, construct the specialization into the valuation ring of the given Case III star point. | [CJP1–3](caseiii_v62/main.tex) |
| TASK_CASE3_AUT_JOIN | Use that specialization at a single fixed complex embedding to prove the three conclusions about the original rank-four datum. | [CJA1–2](caseiii_v62/main.tex) |
| HOST_FRAME_LENGTH | Identify the original strict Selmer group and bound its normalized length using the original marked deformation ring on the same host. | [HVJ1](hostjoin_v62/main.tex) |
| TASK_COUNT_V_INSTALL | Derive the guarded CountV inequality, including equality at the cutoff, with an exponent uniform over the required host instances. | [HVJ2](hostjoin_v62/main.tex) |

## Why support reaches the given rank-four point

The two endpoints of a residual polynomial deformation may each lie on several components. The support of an ideal on one component at the seed initially says little about the other endpoint. The source's rank-four component hypothesis supplies the missing implication at a good residual point: support on one component forces support on all components through it.

A map into a polynomial ring has prime kernel. A minimal prime contained in that kernel lies below both endpoint kernels. Hence support on every component at one endpoint implies support on at least one at the next. Apply the component implication again, and travel backwards along the finite chain. The seed and the eventual integral lift use the same finite coefficient ring, chosen after all three coefficient thresholds. At the original point the integral specialization has prime kernel contained in the residual kernel. A minimal prime below it now contains the ideal. This proves the required vanishing in the actual valuation ring. CJP3 also recovers the symplectic multiplier, global conjugacy, restriction to the tower field, and all the prescribed inertial characters. [CJP1–3](caseiii_v62/main.tex) · [Finite coefficient descent in edition 0.61](chain_v61/main.tex)

CJA1 fixes the complex embedding before the ambient field and its points vary. CJA2 uses the characteristic-polynomial and commutator obstruction in characteristic $\ell$, the weak Frobenius root inequalities in characteristic zero, and automorphic attachment on the irreducible points. Together they prove finiteness of the weight-zero algebra, exclusion of the specified block endpoint, and automorphy of every irreducible algebraic point. The arithmetic existence of the rank-four towers and seeds, and the shared potential-modularity inputs, keep their own entries in the argument. [CJA1–2](caseiii_v62/main.tex) · [Obligation register](continuation_v62/obligations.json)

## Why the rank-three count is now on the original frame

NMD1–7 construct the universal marked deformation ring, its origin, weighted variables and equations on the frame from the Case V host. VSCM1–11 give the map from finite Selmer classes to relation coordinates and identify the points, trace, torus orbits and tangent directions used by the count. The arithmetic and algebraic length arguments now concern the same representation and the same coefficient ring. [Marked ring](marked_v62/main.tex) · [Selmer coordinates and point comparisons](countcoord_v62/main.tex)

One reducible shape still has entries of both weight signs. Its outer two-dimensional block would have to be irreducible. Choose a nonzero lower-left entry of smallest valuation, divide the other lower-left entries by it, reduce modulo the maximal ideal and twist by the inverse residual character. The result is a weight $-2$ cocycle. Its local conditions come from the original flags. The weight $-2$ vanishing theorem and normalization at the distinguished involution force the cocycle to vanish, contradicting the unit obtained at the chosen entry. The outer block would therefore preserve a proper line. This excludes it and proves that a two-sided point has type I. [Shape classification](shape_v62/main.tex) · [TSI1–3](hostjoin_v62/main.tex) · [The earlier host weight −2 calculation](host_xpp_v60/main.tex)

For the finite-level comparison, the $b$-torsion of the strict group lies in the image of the finite Selmer module. This inclusion suffices for the length bound. Exhaustion gives the bound on the divisible-coefficient group; division by the ramification index gives the original normalization. Under the stated host inputs, the trace bound then gives $\mathrm{Vn}\log\ell\le 2(\ell N e)^C\le(\ell N e)^{C+1}$. The exponent is chosen before the varying host instances. At the boundary the guard is $R_1\le 2^{c_2(\psi)}$. [HVJ1–2](hostjoin_v62/main.tex) · [Guard and exponent in edition 0.61](count_v61/main.tex) · [Strict Selmer length](count_v61/length.tex)

## The spectral estimate

For two words in the same family, the linear term in the logarithm of the interior Vandermonde has harmonic-number coefficients. Their total absolute size is linear in the word length. Controlling the quadratic remainder and the two fixed endpoints gives $A=\exp(3/4)$ for both the prime ratio and the archimedean dimension comparison. The common factors in the two prime windows cancel. On a family with the specified compatible selections the remaining size estimates also follow, including the threshold at the least differing letter, both ranks, the masses and the row normalization. The off-diagonal operator bound still requires the pointwise spectral estimate and the selected row-loop estimate. [ODW1–8](offdiag_v62/main.tex) · [Precise next estimates and source lines](offdiag_v62/next_source_handoff.txt)

## Next shared obligation

The next arithmetic calculation is the host vanishing hypothesis used by the count. For a negative weight, the current global argument needs a primitive for the cocycle on inertia at each prime away from the coefficient prime. At the special host primes the original line conditions do not supply that primitive. The pinned proof obtains it from the local cohomology of the inverse cyclotomic twist, then treats weight zero by the Gaussian class-one argument and combines the scalar components into a single integral matrix coboundary. [Original negative-weight argument](https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AutomorphicArithmetic/AutomorphicVarieties/LevelCohomology/SoLineNeg.lean) · [Original host theorem](https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AutomorphicArithmetic/AutomorphicVarieties/LevelCohomology/SoHostVanE.lean)

## Verification and continuation

The six chapters are bound to the original pinned Lean tree through 259 source ranges in 107 files. To repeat the manuscript, dependency and graph checks, initialize the formal source submodule and run the verifier from the repository root.

~~~sh
git submodule update --init --depth=1 -- formal_source
python3 continuation_v62/verify.py --formal-git formal_source
pdflatex RH_new_proofs_v0_62.tex
pdflatex RH_new_proofs_v0_62.tex
~~~

The verification record distinguishes the source and manuscript checks from a rebuild of Lean. The two Case III producers and the full Case V producer still have outstanding arithmetic inputs. [Checkpoint](CURRENT_CHECKPOINT_v0_62.json) · [Source ranges by claim](continuation_v62/claims.json) · [Proof and typesetting checks](continuation_v62/validation.json) · [Remaining statements](continuation_v62/obligations.json)
