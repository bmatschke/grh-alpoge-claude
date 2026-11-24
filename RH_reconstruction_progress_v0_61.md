# Descending a rank-four residual chain

Edition 0.61 closes the whole obligation **CHAIN_DESC4**. The new proof is on pages 1–2. Pages 3–7 prove the numerical spectral bound and transfer the kernel expansion to the original spectral spaces. Pages 7–13 establish the strict Selmer length comparison and identify the arithmetic and deformation-theoretic inputs to the rank-three count. [Typeset the 13-page supplement](RH_new_proofs_v0_61.tex) · [Cumulative TeX](RH_readable_reconstruction_v0_61.tex)

## Why a whole chain descends

In Case III, one residual representation is connected to the reduction of a seed by a finite sequence of polynomial deformations. The vertices are matrices over the ambient residue field. Each edge carries an entire representation over its polynomial ring and matrices specifying its local flags. Later steps choose a coefficient ring large enough for the seed and several other constructions. Descent must work over **every sufficiently large coefficient ring**, whichever one those later choices require. [Statement of ChainDesc4](https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AutomorphicArithmetic/AutomorphicVarieties/ModularityArgument/CuspidalTwists/PromodularityCaseThree.lean#L101-L105) · [Place where the ring is enlarged](https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AutomorphicArithmetic/AutomorphicVarieties/ModularityArgument/ThresholdArguments/DenseThresholdCases/PromodularityCaseThreeOfLemmas.lean#L49-L66)

The proof has three steps.

1. A locally constant matrix entry on the compact group has finite image. For a polynomial link, this means finitely many polynomials actually occur as values. Across finitely many matrix entries, local flags and links, there are only finitely many coefficients to capture. The ambient residue-field hypothesis captures each in a coefficient ring. Taking the ring of integers of a finite compositum captures them all, and they remain available at every larger coefficient ring.
2. The residue-field inclusion is injective, as is its extension to polynomials. The multiplication laws, similitude, diagonal characters, local flag identities and required zero entries therefore descend. Each required nonzero root entry retains its original witness. This verifies the source’s complete residual and goodness conditions.
3. Evaluation at zero and one commutes with the inclusion. Consecutive lifted links therefore share the very same endpoint, entry by entry, including the local matrices. Keeping the original order gives the required chain. A chain of length zero descends by lifting its initial vertex once.

The result provides one premise of Case-III promodularity. Its sibling obligation CHAIN_RANK_FOUR concerns propagation between components of a deformation space along such a chain. That geometric argument is still required. [RCD1–3](chain_v61/main.tex) · [Source and proof review](chain_v61/review.md)

## The frame bound on every sufficiently late word

Let $v$ be half the host root discriminant, $g_0,g_1$ its two level primes, and $T_u$ the prime already chosen for word $u$. In the earlier lower bound (QW.17) for the logarithm of the window centre, retaining the two terms $m\log(g_0g_1)$ and $m\log(v/\pi)$ gives the host factors needed here. The $m$ middle weights contribute at least another $m$, which absorbs the window error since $m\ge x^{1/4}$ and $L=x^\epsilon$ with $\epsilon<1/52$. After one family threshold the result is

$$
T_u\ge(vg_0g_1/\pi)^m,\qquad
T_u\left(\frac{\pi}{vg_0g_1}\right)^{2r_S}
\ge(vg_0g_1/\pi)^2\ge1 .
$$

The second inequality uses $2r_S=m-2$. It holds for **all** late indices and words of a family with the stated base-volume identity. A supplied tied selector gives that identity on the same members. With its compatible spectral selector, this proves the original concrete family selection, including indices outside the admissibility guard. TFR4 also proves the frame bound on linked construction data before a family is chosen. [TFR1–4](frame_v61/main.tex)

The kernel expansion now holds on the original column spaces at every late index of a family with a spectral selector. The compact Weyl dimension formula identifies the normalization. The unitary comparison carries both the period maps and their adjoints, and a bijection reindexes the absolutely convergent operator series. This proves the family assertion PX.ExpF. The existence of the common selector and the off-diagonal and diagonal estimates retain their own requirements. [KXE1–3](expansion_v61/main.tex) · [Next spectral estimates](frame_v61/next_source_handoff.txt)

## The rank-three count and its remaining comparison

VLT1–3 prove a uniform comparison on the particular host frame. If its finite-coefficient lengths are bounded by $V$ for every nonzero coefficient $a$, then the original arithmetic Selmer length is at most $V$. The proof identifies the strict Selmer classes, lifts each torsion class with the prescribed local conditions, and exhausts the full group by increasing torsion submodules. Their bounded integer lengths force stabilization. [Length comparison](count_v61/length.tex)

CVI1–4 construct the Galois frame under the original Case V guard, including its equality endpoint. They compute the local vanishing and the Euler defect on that frame. CVI5–6 carry this to the required exponent $C+1$ **assuming the listed comparisons on the marked deformation ring**. The remaining work is to construct and identify the native marked universal pair, its weighted presentation, the point and tangent comparisons and the integral map from the finite Selmer group into the relation coordinates. The separate one-character model in earlier chapters has different inputs. The obligation TASK_COUNT_V_INSTALL therefore remains open. [Count proof and remaining hypotheses](count_v61/main.tex) · [Exact source handoff](count_v61/next_source_handoff.txt)

There are **3,820 indexed claims and 22 open whole obligations** in the human reconstruction. Sixteen are shared by RH and unrestricted Dirichlet GRH, and six are additional for unrestricted Dirichlet GRH. The verifier checks the single change against the previous edition and the original graph contracts. [Checkpoint](CURRENT_CHECKPOINT_v0_61.json) · [Whole obligation register](continuation_v61/obligations.json) · [Claim index](continuation_v61/claims.json) · [Verification record](continuation_v61/validation.json)
