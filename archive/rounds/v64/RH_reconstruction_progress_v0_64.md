# Edition 0.64 · Frobenius traces, marked points and residual chains

This edition proves the uniform trace bound in the common Case V argument and two of the four outstanding Case III obligations for unrestricted Dirichlet GRH. The marked-point chapter connects a proposed arithmetic input to the remaining marked-point theorem. The manuscript now has **3,886 indexed claims**, including 21 in this edition, and **14 open whole obligations**. Twelve are shared by RH and Dirichlet GRH. Two more apply to unrestricted Dirichlet GRH. [New chapters](RH_new_proofs_v0_64.tex) · [Cumulative manuscript](RH_readable_reconstruction_v0_64.tex) · [Current checkpoint](CURRENT_CHECKPOINT_v0_64.json)

| Question | Result in this edition | Manuscript |
| --- | --- | --- |
| Can one trace separate all eligible points of a fixed Case V host? | A geometric Frobenius works for every point. One exponent bounds the valuation sum for every finite pairwise inequivalent family. | [VUN1–6](hostnumber_v64/main.tex) |
| What arithmetic input will prove the marked Case V theorem? | A common mark for the residual finiteness and characteristic-zero automorphy assertions suffices. Irreducibility on open subgroups and on the full cyclotomic kernel is proved. | [VMA1–6](markedaut_v64/main.tex) |
| Can the Case III tower be chosen with its prescribed label? | The construction gives an acceptable tame tower, one element separating four characters, and the required quadratic character. | [TFT1–5](tensortower_v64/main.tex) |
| How does the Case III lattice connect to the seed? | Four polynomial families connect their reductions after one preliminary tower extension, under the source seed, fitness and cohomology hypotheses. | [RFCR1–4](rankchain_v64/main.tex) |

## One prime for every eligible point

Fix the Gaussian field $K$ and the constants $a,b$ in the earlier rank-three congruence theorem. The theorem concerns Galois representations over $K$. To apply it to a host point, restrict the point to the positive-sign subgroup, identify that subgroup with the image of $G_K$, and check the ordinary flag at $\ell$ and the inertial basis everywhere else. At $\ell$ a single element with cyclotomic value one and three distinct residual eigenvalues rules out every equality between distinct diagonal characters after a cyclotomic twist. A finite extension of $\mathbb Q_\ell$ has nontrivial cyclotomic character, which deals with the equal-index case. These checks include $e=1$ and $\ell=3$. [Native level comparison](hostnumber_v64/main.tex) · [Earlier congruence theorem RNC16](rank_three_congruence_v46/main.tex) · [Local separator and eigenvalue comparison](host_rigidity_v42/main.tex)

Take an inert prime $p\equiv3\pmod4$ dividing $12\ell N-1$. It satisfies $7\le p\le12\ell N$ and $p\nmid\ell N$. Squaring an arithmetic Frobenius over $\mathbb Q$ and taking its inverse gives one element $\phi$ for both embeddings of $K$. For every eligible marked type-I point $r$, its trace at $\phi$ differs from that of the base point $r_0$. More precisely, if $v_\ell(\ell)=1$ and the matrices of the $r_i$ on the sign kernel are pairwise inequivalent, then

$$
 (\log\ell)\sum_i v_\ell\!\left(\operatorname{tr}r_i(\phi)-\operatorname{tr}r_0(\phi)\right)\le (\ell N e)^{2a+b+4}.
$$

The rank-three theorem bounds the norm of an integer using the traces in one Gaussian embedding at a time. Splitting the family between its two possible embeddings accounts for the factor of two in the estimate. The exponent depends only on $K$, and $\phi$ is chosen before the family. This proves **HOST_NUMBER_S** at its original quantifiers. [VUN4–6](hostnumber_v64/main.tex) · [Original host number statement](https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AutomorphicArithmetic/AutomorphicVarieties/ModularityArgument/ThresholdArguments/DenseThresholdCases/HostNumberS.lean#L18)

## What remains in Case V

A characteristic-zero type-I point stays irreducible on every open subgroup of the positive-sign group. A regular inertia element distinguishes three eigenlines. If an open restriction split into three lines permuted transitively, a three-cycle would force three distinct elements of the residue field to satisfy $X^2+X+1=0$. On the possibly infinite-index cyclotomic kernel, a failure of irreducibility would give a nonscalar matrix commuting with some open subgroup, contradicting the first part. [VMA3–4](markedaut_v64/main.tex)

This makes the reduced marked theorem equivalent to **THM_S6_S**. One route still has to produce an absolute mark for which both the residual finiteness end and the rank-three automorphy end hold. The subgroup in the finiteness end must work for every subsequent residual DVR point. The automorphy end must work at that same mark and yield the inverse-cyclotomic automorphy assertion for each eligible integral point. Of the direct inputs to the Case V count, this marked theorem is the sole remaining open one. [VMA1–2 and VMA5–6](markedaut_v64/main.tex) · [Case V count](hostjoin_v62/main.tex) · [Arithmetic end statement](https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AutomorphicArithmetic/AutomorphicVarieties/ModularityArgument/ThresholdArguments/DenseThresholdCases/AutEnd3AltAlt.lean#L20)

## The initial tower and four polynomial links in Case III

For either label allowed by the original datum, the tower construction produces four residual diagonal character ratios with values $1,-1,z,-z$ at one element, with $z$ of nontrivial odd order. They therefore separate all four coordinates. The construction also produces the specified quadratic character on the real tower and checks the ramification and inertia conditions at the original primes. This proves **TENSOR_FACTOR_TOWER**. [TFT1–5](tensortower_v64/main.tex)

Assume the original seed hypothesis in addition to cohomology and fitness. Start with its residual choice and the prescribed global lattice. Two compatible cup-product modifications produce intermediate residual pairs with matching matrix and local flag coordinates. One extension kills the required auxiliary inertia. On every later deep tower the seed hypothesis gives one integral seed; after restriction the four interpolations join the allowed lattice pairs to its reduction. The order of these choices supplies **RANK4_CHAIN_REDUCTION**. [RFCR1–4](rankchain_v64/main.tex) · [Downstream Case III argument](caseiii_v62/main.tex)

The two additional obligations for unrestricted Dirichlet GRH are the actual finite-coefficient seed (**SEED_IV_ALT**) and the propagation of ideal membership to every point on the original rank-four component (**CHAIN_RANK_FOUR**), with the specified bound $30(C+1)^2\le d$. The remaining common obligations and all fourteen source contracts appear in the register. [Dependency graph and remaining contracts](continuation_v64/obligations.json) · [Claim-level sources and reviews](continuation_v64/claims.json) · [Previous edition](RH_reconstruction_progress_v0_63.md)

For the component theorem, the next case to work out is the exceptional reducible support $Y$. Its matrices preserve two symplectic planes. Their ordinary characters and the traces of products give a direct way to bound the dimension of the corresponding trace fibre. The handoff identifies the exact local hypotheses, the two scalar coordinates needed for recovery, and the tangent estimate that would still remain. [Source statements and proof outline](tensortower_v64/next_source_handoff.txt)
