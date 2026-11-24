# The large-prime denominator estimate

Edition 0.80 · 25 November 2026

The large-prime field of the denominator family conclusion now holds on the same hub as the eleven fields proved through edition 0.79. For every sufficiently late qualifying family member, every twisted localization with residue prime $\ell>p_*$ outside the arithmetic exceptional set and the two type primes, and every good point $\pi$, the normalized congruence valuation satisfies

$$
v_{\rm cc}(i,\pi)\ \le\ s_\pi(\rho_i)+\sum_{1\le j<t}u_j+v_\ell(h_E)+\ell^{-2}.
$$

Here $s_\pi$ is the normalized Selmer term, $u_j$ are the prescribed Tate–Shafarevich lengths for the positive twists, and $h_E$ is the host class number. The additional local error in the source's bound is zero. The auxiliary-prime correction $\ell^{-2}$ is included in the displayed inequality. [Large-prime assembly](continuation_v80/assembly.tex) · [Normalization and the original inequality](continuation_v79/large.tex)

The statement retains the original hypotheses $\mathrm{Hypotheses}_2$, $\mathrm{TwGood}$ and $\mathrm{FactsF}$, with $C\ge0$ and $C_2\ge1$, the eventual scale guard, and the original finiteness premise. In this source revision, the premise named `ShaFinOdd` covers every prime, including 2, for $0<e<t$. The choice of uniform constant precedes selection of a member. The cutoff can be increased while keeping the same constant and the prescribed exceptional set. The complete global denominator obligation also requires the original family construction and the final bound on the actual $\eta$-sum. **Ten whole obligations remain**, all shared by RH and unrestricted Dirichlet GRH. [Family checkpoint](CURRENT_CHECKPOINT_v0_80.json) · [Whole contracts](continuation_v80/obligations.json)

## Reading the proof

| Step | Mathematical content |
| --- | --- |
| Shift every local representation | A labelled crystalline character realizes the chosen integer shifts. After twisting, every point in the good family has the exact jump multiset and congruence of characteristic polynomials required by the local criterion. This holds for the full range of families, points and continuous complements in the congruence theorem. [Shift construction](continuation_v80/shift.tex) |
| Pass from characteristic zero to the residue field | On the chosen level-one Wach module an invariant basis and integral divisibility at the primitive roots give the signed Frobenius shifts and the two polynomial identities for the divided cyclotomic action. The residual tensor presentation identifies the integral kernels and the actual reduction maps. These maps give the standard and character models and all admitted residual quotients. [Integral calculation](continuation_v80/wach.tex) · [Tensor presentation](continuation_v80/res.tex) · [Residual models](continuation_v80/model.tex) |
| Bound local classes | At embedding $i$ put $d_i=\#\{u\in U_i:u<w_i\}$, counted with multiplicity. A cocycle is represented by the Frobenius and cyclotomic differences of a lift. Their negative-power coefficients give an injective record on independent classes. At a boundary embedding the relevant kernel has dimension at most $r$, and its integral part has dimension $r-d_i$. Summing the resulting local bounds gives at most $\sum_i d_i$ independent classes on the rank block. The rational Bloch–Kato subspace attains this dimension. [Local cohomology proof](continuation_v80/top.tex) |
| Test the original cocycles | Each cut cocycle produces a triangular finite extension. Two full stable lattices give exactly that extension as their quotient, at every exponent that kills its coefficient module. On the rank block it gives a Bloch–Kato finite class. On each higher character ratio it gives a coboundary. On the first character it gives an unramified class. These conditions descend from the enlarged coefficient field. [Cut construction](continuation_v80/cut.tex) · [Descent](continuation_v79/descent.tex) |
| Apply the global count | The three local conditions are exactly those required by D79G8 for every eligible localization. The previously constructed integral decomposition, determinant count and global Artin reciprocity now give the member bound. Specialization to the selected hub proves the large-prime field. [Family conclusion](continuation_v80/assembly.tex) |

The full new text is available as [a PDF](RH_new_proofs_v0_80.pdf) and in [the cumulative manuscript source](RH_readable_reconstruction_v0_80.tex).

## Where to resume

Twelve fields now hold together: `pos`, `pass`, `mult`, `rank`, `kill`, `num`, `bb`, `exc`, `typ`, `par`, `small`, and `large`.

| Open field | Exact remaining work |
| --- | --- |
| `ram` | At $q,d$ the filtered subrepresentations, integral row windows, explicit common tame exponent and three rank-one cohomology clauses are established. The next local assertion concerns an integral lift $e_0$ of 1 in a crystalline extension, with kernel $Y$. After an allowed equivariant map from its kernel lattice to the torsion character line, one must place the image of $g e_0-e_0$ in the finite part after multiplication by the prescribed prime power. The row-lifting estimate at 160 and application of the global index inequality to these rows are also needed. Under these inputs H80M5 gives the coefficient $13\cdot160=2080$. [Ramified-prime calculations](continuation_v80/ramified.tex) |
| `mid` | Prove the lifting estimate and the joint B/C/D row conditions for the actual middle-range representation. The coarse bound and five numerical table entries are available. [Earlier handoff](RH_reconstruction_progress_v0_79.md#where-to-resume) |
| `two` | Prove the bounds at 2 and 3 and the odd small-prime correction with one family cutoff. The separate small-prime parameter inequalities already hold. [Original family record](https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AbelianVarietyTheory/Definitions/NonGaloisDescent/BoundAtTwoThreeFamily.lean) |

The pinned [kernel-cocycle proof](https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AbelianVarietyTheory/Proofs/InertiaEigenvalues/CrystallineExtensionClassBound.lean#L359-L390) identifies the next step at the ramified primes. It combines a Wach-module torsion estimate with descent of the resulting finite class.

The [obligation ledger](continuation_v80/obligations.json) gives the nine other entire contracts. The earlier [theta handoff](RH_reconstruction_progress_v0_78.md#next-source-obligations) records their common selection and reading requirements.

## Verification

The edition adds 44 claims, bringing the inventory to 4,477. Their 380 source ranges cover 165 distinct files in the pinned original Lean tree. The verifier checks the source excerpts, manuscript blocks, declared proof dependencies, checkpoint and supplement digest. The ten open contracts retain the wording recorded on the preceding public commit. The new arguments are human mathematical proofs. This edition involved no new Lean build. [Claim ledger](continuation_v80/claims.json) · [Validation](continuation_v80/validation.json) · [Previous edition](RH_reconstruction_progress_v0_79.md)

~~~sh
python3 continuation_v80/verify.py --formal-git formal_source
pdflatex RH_new_proofs_v0_80.tex
pdflatex RH_new_proofs_v0_80.tex
~~~
