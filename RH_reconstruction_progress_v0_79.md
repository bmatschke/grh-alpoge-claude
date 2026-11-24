# Edition 0.79 · The split columns and the two type primes

Two more fields of the original denominator conclusion now hold on one chosen family hub. The coarse field `bb` bounds the error in the middle range, including split primes with nonempty columns. The type-prime field `typ` bounds the weighted local index at each of the two type primes. Together with the nine fields from edition 0.78, this gives **11 of 15 family fields**. **Ten whole obligations remain open**, all shared by the RH and unrestricted Dirichlet-GRH routes. The count of fifteen concerns one part of one of those ten obligations. [New proofs (PDF)](RH_new_proofs_v0_79.pdf) · [Cumulative manuscript source](RH_readable_reconstruction_v0_79.tex) · [Checkpoint](CURRENT_CHECKPOINT_v0_79.json) · [Whole obligations](continuation_v79/obligations.json)

## What the two estimates say

For a good point $\pi$ and a declared split-column place $u$, take the original rank-$r$ lattice $T$ for the local representation $\chi_1^{-1}\rho_i(\pi)$. The comparison at $u$ fixes both the local field and the coefficient embedding. Removing the character block from the Hodge multiset leaves at most $r$ distinct jumps at any one embedding $\tau$, and none is zero. The crystalline comparison gives integral Wach height bounds for precisely this lattice and the compatible records chosen on this member. [The lattice and its jumps](continuation_v79/split.tex) · [The integral height bounds](continuation_v79/heights.tex)

Write $U_\tau$ for those distinct jumps and $m$ for the prescribed cyclotomic level. The local argument proves that the following power kills the invariant classes of $V/T$.

$$
\ell^{a_\tau}(V/T)^{G_{E_u}}=0,
\qquad a_\tau=2+\sum_{j\in U_\tau}(m+v_\ell(j)).
$$

The two extra powers pay for the integral change of basis and descent by trace. Each distinct nonzero jump contributes one factor in the characteristic-root polynomial on the finite level. The bound $a_\tau\le c_0(i,u)$ uses the exponent already stored on the hub. The normalized length is consequently at most $r c_0(i,u)$. Combining this with the scalar and inert estimates gives the native coarse invariant condition at 120 and $\mathrm{BBLe}(L,X,7200)$. The family constant already dominates 7200. [Local annihilator](continuation_v79/annihilator.tex) · [Coarse estimate on the family](continuation_v79/assembly.tex)

At each type prime $g_0,g_1$, the proof constructs the conjugate signs and jump sets for every point in the specified family and checks the wild-inertia and tame-generator conditions. The paired-character inequality supplied by the original family assumptions then bounds the local index. Summing good-point multiplicities uses the rank bound on the same hub. The place weights sum to at most $\log g_k$ by the local degree formula. Both occurrences of $1/g_k^2$ in the original bound are retained. The uniform constant can be chosen before the cutoff to dominate $2000(C+1)+5C_1$, where $C$ is the nonnegative paired-character constant and $C_1$ is the uniform parameter bound. [Type-prime witnesses](continuation_v79/typewitness.tex) · [Weighted bound and simultaneous conclusion](continuation_v79/type.tex)

## Scope of the family result

Assume the source's $\mathrm{Hypotheses}_2$, $\mathrm{TwGood}$ and $\mathrm{FactsF}$, with $C\ge0$ and $C_2\ge1$. One constant and one cutoff work for every subsequent member satisfying the original scale guard and the source’s `TwistedPlaces.ShaFinOdd` finiteness premise. In the pinned definition this ranges over every prime, including 2, for twists $0<e<t$. At each member, one hub with the prescribed arithmetic exceptional set satisfies all the following fields. Constructing families with the required hypotheses remains part of the global denominator proof. [The setup in edition 0.78](continuation_v78/family.tex) · [The original fifteen-field record](https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AbelianVarietyTheory/Definitions/NonGaloisDescent/BoundAtTwoThreeFamily.lean#L124-L143)

| Proved together | Outstanding |
| --- | --- |
| `pos`, `pass`, `mult`, `rank`, `kill`, `num`, `bb`, `exc`, `typ`, `par`, `small` | `mid`, `large`, `two`, `ram` |

## Where to resume

| Field | Current handoff |
| --- | --- |
| `large` | The numerical position data off the exceptional primes and the global count under the unit-root-difference and local cut-cocycle hypotheses are proved. The proof constructs the integral orthogonal decomposition with a unit root difference for the prescribed representation and complement, and descends the three required local conditions from a finite coefficient enlargement. The exact local Hodge data and the Bloch–Kato, coboundary and unramified conditions upstairs must be constructed for every guarded localization of every eligible member. D79G8 shows that proving those three assertions for all the guarded cut generators now suffices for the large-prime field. The original zero concerns the additional error parameter in the local inequality. [Global count and position tables](continuation_v79/large.tex) · [Integral decomposition](continuation_v79/decomposition.tex) · [Descent](continuation_v79/descent.tex) · [Local admissibility in Lean](https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AbelianVarietyTheory/Proofs/InertiaEigenvalues/AdmissibleOfLargeResidueChar.lean#L25) · [Family assembly in Lean](https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AbelianVarietyTheory/Proofs/InertiaEigenvalues/CongruenceBoundLarge.lean#L50) |
| `mid` | The coarse error and the five numerical table entries now hold. The pointwise middle-range inequality still needs the lifting estimate and the joint B/C/D row conditions on this representation. [Coarse error](continuation_v79/assembly.tex) · [Original row assembly](https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AbelianVarietyTheory/Proofs/InertiaEigenvalues/StarAndSizeBound.lean#L21-L39) |
| `two` | Supply the two/three local bound and the odd small-prime bound with their common family cutoff. These are separate from the already proved `small` parameter inequalities. [Original small-prime cases](https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AbelianVarietyTheory/Definitions/NonGaloisDescent/BoundAtTwoThreeFamily.lean) |
| `ram` | At $q,d$ the local completion, inertia, CM type, signed Hodge windows for all points, and row degrees are now determined. The original bound still needs the row-lifting estimate at 160 and the character-block bound $c_B\le60tf(r+t)\log b$ in the global index inequality. Its conversion to the common family constant is J78H2. [Ramified-prime inputs](continuation_v79/ramified.tex) [Polynomial conversion](continuation_v78/assembly.tex) · [Original family argument](https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AbelianVarietyTheory/Proofs/InertiaEigenvalues/ConclusionOfFamilyFacts.lean#L83-L126) |

The other nine whole obligations are listed with their original closure conditions in the obligation ledger. Edition 0.78 records the working handoff for the common theta bundle, including the kept preliminary datum and its eventual agreement with the localized reader. [Open contracts](continuation_v79/obligations.json) · [Theta handoff](RH_reconstruction_progress_v0_78.md#next-source-obligations)

## Verification

This edition adds 55 indexed proof claims, bringing the cumulative total to 4,433. Its 383 source ranges span 180 files at the original pinned revision. The claim ledger binds each new argument to byte ranges in the pinned original Lean tree and to its proof dependencies. The verifier compares the open contracts with the public predecessor and checks the supplement PDF. The validation record includes the full manuscript build, its page count and its inherited typesetting warnings. The original Lean development was not rebuilt for this edition. [Claims](continuation_v79/claims.json) · [Validation](continuation_v79/validation.json) · [Previous edition](RH_reconstruction_progress_v0_78.md)

~~~sh
python3 continuation_v79/verify.py --formal-git formal_source
pdflatex RH_new_proofs_v0_79.tex
pdflatex RH_new_proofs_v0_79.tex
~~~
