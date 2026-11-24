# The denominator estimate at the two ramified primes

Edition 0.81 · 25 November 2026

The denominator family has fifteen fields, each of which must hold for the same family data. This edition proves the field called `ram`. It controls the congruence denominator at every twisted localization above either distinguished prime $p=q,d$ and every good point there. Together with edition 0.80 this gives **thirteen of the fifteen fields on the same hub**. The middle-range field `mid` and the small-prime correction `two` remain. The complete reconstruction of RH and unrestricted Dirichlet GRH still has ten open obligations, including the global denominator obligation. [New proofs (PDF)](RH_new_proofs_v0_81.pdf) · [Cumulative manuscript source](RH_readable_reconstruction_v0_81.tex) · [Exact open contracts](continuation_v81/obligations.json)

## What the estimate says

Write $v_{\rm cc}(i,\pi)$ for the congruence valuation at a point. Its main terms are the normalized Selmer length $s_\pi$, the positive-twist Tate–Shafarevich lengths $u_j$ for $1\le j<t$, the class-number valuation $v_p(h_E)$ and the auxiliary correction $p^{-2}$. For $u=\log b$ and $B=b/p+S_c+t+\eta+u$, the excess of the valuation over those terms is at most

$$
2080 f(rB+mb) + 181 f^2t^2(r+t)u .
$$

Here $r$ is the rank of the noncharacter block, $t$ counts the character blocks, and $m,f,b,S_c,\eta$ are the member parameters of the original bound. The polynomial has nonnegative coefficients, total degree five and coefficient sum 362. The uniform constant already chosen for the previous twelve fields absorbs this polynomial and the coefficient 2080. Increasing the common family cutoff imposes all the required size conditions at once. This is the source's `StarG` assertion. The proof uses the original family hypotheses $\mathrm{Hypotheses}_2$, $\mathrm{TwGood}$ and $\mathrm{FactsF}$, the bounds $C\ge0$ and $C_2\ge1$, and the stated late-member finiteness premise. [Member estimate](continuation_v81/assembly.tex) · [Comparison with the family inequality](continuation_v78/assembly.tex) · [Original definition of StarG](https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AbelianVarietyTheory/Definitions/NonGaloisDescent/BoundAtTwoThreeFamily.lean#L78-L80)

## Reading the ramified proof

| Step | Argument |
| --- | --- |
| Separate the character lines globally | At $q,d$ the cyclotomic character on inertia has residual order $(p-1)/2$. This exceeds $t$, so its values distinguish the character lines. The resulting integral projectors give a determinant bound on the original point ideal. A single graph lattice handles every finite list of rank classes. [Index and local restrictions](continuation_v81/index.tex) |
| Bound the characters | An integral estimate on a truncated Wach module controls the cocycle of a crystalline extension by the exact power prescribed in the source. This works for all rank-one twists tested here, including the trivial character. The sum of their errors costs at most $180 f^2t^2(r+t)\log b$. [Integral torsion](continuation_v81/torsion.tex) · [Kernel cocycles](continuation_v81/kernel.tex) · [Character sum](continuation_v81/assembly.tex) |
| Reduce the rank calculation to local lifts | Restrict the rank classes at all $w\mid p$ and quotient by the Bloch–Kato finite subgroups. The kernel is controlled by the Selmer term. The image is finite at each point by the integral elementary-divisor argument. A uniform bound also has to control its length as the point and member vary. [Pointwise finiteness](continuation_v81/smith.tex) · [Local length calculation](continuation_v81/row.tex) |
| Lift at every residue embedding | A coarse integral lift controls all target classes. A sharper lift uses the filtered Wach module at each embedding. The exceptional summand has rank at most $2m$, and its contribution requires at most $6m$ generators. At $q$ the two branches have the same sign. At $d$ they have opposite signs, and their endpoints can vary independently. Nearby endpoints give a valuation bound from a binomial coefficient. For separated endpoints, extracting a Taylor coefficient gives a lift in the required source filtration. [Coarse lifting](continuation_v81/bridge.tex) · [Comparison of the two models](continuation_v81/letters.tex) · [Pure signs](continuation_v81/slot.tex) · [Mixed signs](continuation_v81/mixed.tex) |
| Sum on the original family data | The integral argument yields the local row constant $160$ for every tested surjection and good coefficient extension. The length of the joint image under restriction is at most the sum of the local bounds. That sum costs at most $13\cdot160 f(rB+mb)+f$. The extra $f$ fits in the stated polynomial allowance. [Uniform local estimate](continuation_v81/lifting.tex) · [Assembly at both primes](continuation_v81/assembly.tex) |

## Character classes in the middle range

At the eligible unramified primes, the integral character calculation also holds at the exponent already stored on the hub. The extra issue here is that the Tate-dual character can have nonzero torsion invariants. They form a finite cyclic module. If $d_w=[K:\mathbf Q_p]$, the rational contribution to the local cohomology modulo its finite part has corank $d_w$. The cyclic contribution adds at most one generator. Hence the subgroup killed by $p^a$ has normalized length at most $(d_w+1)a$, including at $a=c_B$. This proves the character condition $\mathrm{admTB}$ on both middle-range branches. [Jump window, exact exponent and cyclic obstruction](continuation_v81/mid.tex)

## Lifting at the split primes

For the split middle-range primes the hub prescribes a single exponent $e_S$ for the column representations and the Tate-twisted duals on the conjugate rows. Put $h=\lfloor b+S_c+\eta+t+2\rfloor$. Working on the unramified base field gives the smaller bound

$$
 25h/p+3\ \le\ e_S
 =\left\lceil 23\left(2+2h/p+\log_p(2h+1)\right)\right\rceil .
$$

The saving comes from dividing the cyclotomic difference by an integral parameter $v$ with $v(\zeta-1)=-p$ at each primitive root. On the piece of degree $-j$ at a pole, the resulting operator has eigenvalue $(1-u^{-j})/p$, where $u$ is the cyclotomic value of the generator. A nonzero degree now costs $v_p(j)$. The integral correction therefore fits the prescribed exponent even when $h$ is much larger than $p$. On a row conjugate to column $u$, the resulting normalized cokernel length is at most $d_um e_S+r c_0(i,u)$, the precise row bound used by the split declaration. Here $d_u$ is the local degree. [Split lifting proof](continuation_v81/splitlift.tex) · [Conjugate row bound and global comparison](continuation_v81/splitrows.tex)

At small split primes, two character values at a point can coincide modulo $p$. Perturbing the character corner away from the chosen point separates the roots in characteristic zero and preserves the point evaluation. Passing from the resulting block cocycles to global cohomology costs at most $2(r+t-1)v_\delta(i)$ in normalized length. The same character calculation at a single place uses at most $d_u n_V$ possible jumps. Combining a column with its conjugate row shows that their two character costs fit within the allowance already assigned to the row. This leaves only the joint image of the rank classes at the columns to bound. [Projectors and the global comparison](continuation_v81/splitrows.tex) · [Paired character estimate](continuation_v81/splitcomp.tex)

## Where to resume

| Open field | What remains |
| --- | --- |
| `mid` | Bound the simultaneous image of the global rank classes at the split columns. At the inert primes, prove the sharp rank estimates for rows B, C and D. The guard includes eligible exceptional primes above the usual threshold. In the inert case row B requires the saving $(p-1)^{-(j+1)}$ for clustered Frobenius words. Rows C and D distinguish whether every letter is thick. Earlier work gives the coarse bound and split-column estimates. [Middle-range starting point](continuation_v81/mid.tex) · [Local row hypotheses](https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AbelianVarietyTheory/Proofs/InertiaEigenvalues/AdmissibleAtInert.lean) · [Earlier table and split columns](RH_reconstruction_progress_v0_79.md#where-to-resume) |
| `two` | Prove the bounds at 2 and 3 and the odd small-prime correction, with one family cutoff. The separate parameter inequalities for small primes already hold. [Original small-prime conclusion and reductions](https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AbelianVarietyTheory/Definitions/NonGaloisDescent/BoundAtTwoThreeFamily.lean#L50-L77) |

The original split-column comparison uses the dimension of a local finite-cohomology space on each point of the ordered-root cover. [Integral lifts](https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Formalism/AdmissibleDesigns/FiniteClassesLocalEq.lean#L461-L533) · [Dimension of the local space](https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Formalism/AdmissibleDesigns/CohomZeroEquivContinuous.lean#L464-L582) · [Column calculation](https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Formalism/AdmissibleDesigns/ColLx.lean#L32-L69)

The complete global denominator contract also requires the original family construction and the bound on its actual $\eta$-sum. The other nine open contracts are recorded individually in the ledger. [Checkpoint](CURRENT_CHECKPOINT_v0_81.json) · [Obligation ledger](continuation_v81/obligations.json) · [Earlier handoff on theta selections and readings](RH_reconstruction_progress_v0_78.md#next-source-obligations)

## Verification

The edition adds 66 proof blocks, bringing the inventory to 4,543. Their 485 cited ranges are in 147 distinct files of the pinned Lean source. The verifier checks the cited bytes, manuscript blocks and declared dependencies, compares all open contracts with the preceding commit, and checks the supplement digest. These are provenance and consistency checks on a human reconstruction. This edition involved no new Lean build. [Claim records](continuation_v81/claims.json) · [Validation](continuation_v81/validation.json) · [Previous edition](RH_reconstruction_progress_v0_80.md)

~~~sh
python3 continuation_v81/verify.py --formal-git formal_source
pdflatex RH_new_proofs_v0_81.tex
pdflatex RH_new_proofs_v0_81.tex
~~~
