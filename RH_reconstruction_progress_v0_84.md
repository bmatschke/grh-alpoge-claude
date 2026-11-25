# A good cut for the denominator estimate

**Edition 0.84 · 25 November 2026**

The human reconstruction now proves the full good-cut theorem `CutGivesAlt`. Given the Galois preconditions and the four compatibility conditions on a datum with its specified norm choice, it constructs one cut, proves all the norm-choice facts there, and transports all four compatibilities to it. On each original selected member, six Galois preconditions and the first and third of the four compatibilities now have direct proofs. The class-wide denominator estimate still has two substantive requirements, supplying the remaining member data and proving the uniform integral lifting estimate used at the type primes. The reconstruction has ten open obligations, all shared by RH and Dirichlet GRH. [New proofs (PDF)](RH_new_proofs_v0_84.pdf) · [Cumulative TeX](RH_readable_reconstruction_v0_84.tex) · [Unabridged obligation contracts](continuation_v84/obligations.json)

## What the cut keeps

For each localization the finite central operator splits the type space by a tuple of monic residue-field polynomials. Its indices are **coefficients**. For instance the vector $(2,0)$ indexes $X^2+2$ over the field with five elements, although this polynomial has no roots there. This corrects the description of the indices as ordered roots in LN1. Restricting the sum to good tuples acts on every type vector above a theta point by its good-point indicator. Multiplication by the order of the finite group gives the integral endomorphism. Its support can also contain points outside theta, and these points account for a congruence loss. P84C3 proves all the goodness clauses even for other automorphic representatives of a retained point. [Selector and good cut](continuation_v84/goodcut.tex)

The new arithmetic argument on the cut includes the two signed local inertia calculations (G5) and the converse assertion that a distinguished character line forces the required good parameter (G6). The latter uses the strict cuspidal Satake bound and a residual dimension count. Every rank-one residual dimension is used up by a single character string of length $t$. The remaining single constituent has rank $r$. These arguments supply the facts required on the same cut chosen by the operator. [Cut arithmetic](continuation_v84/cutfacts.tex) · [CutGivesAlt](continuation_v84/binding.tex)

## Which assertions hold on original members?

| Native datum | Result at a supplied original member |
| --- | --- |
| Rank-one character, the first tie | The member’s Hecke character determines the local de Rham Galois character. A single unit gives the two conjugate labels $X-u$ and $X-u^{-1}$. |
| Crystalline inertia, the third tie | The specified inertia polynomial annihilates every tested potentially crystalline period in the member's own coefficient embedding. |
| `large`, `nct`, `same` | The chosen coefficient extension is large enough in the native sense, the member carries its norm-choice tie, and both readings of the twist have the same relation kernel. |
| `block`, `muUnr` | The character tie gives the two signed infinity exponents and the unramifiedness test for the original twist. |
| `c2` | Two localizations on the tested fibre sharing a good row induce identical residual values on every Hecke generator. Their residual maximal ideals agree, hence they are the same localization. |
| Depth-zero and local series data | The member supplies its localized Hecke sections, the coefficient-field and central-operator comparisons, and both tame inertia-polynomial laws. The local type-occurrence test in M84T8 has its own representation-theoretic premise. |

The class statement quantifies over all eligible indices of the original family. The member proofs apply to the norm, character, coefficient embeddings and Hecke action already specified at such an index. Constructing the common geometric family and its remaining row data is a separate obligation. [Member compatibilities](continuation_v84/member.tex) · [Localization uniqueness](continuation_v84/localisation.tex) · [Pinned original member assembly](https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AutomorphicArithmetic/ThetaCorrespondence/ThetaPairLifts/ThirdPlaceSeries/PreAtMem.lean#L86-L103)

## What is actually measured at a type prime?

Let $T_U$ be the image of the integral Hecke algebra on a finite set $U$ of points. For a fixed good point $\pi$, let $B$ consist of the non-theta points in its selected support. With coefficient ring $O$, ramification index $e$ and module length $\ell_O$, the congruence length is exactly

$$
 c_\pi = \frac{\ell_O(O^{B\cup\{\pi\}}/T_{B\cup\{\pi\}})
                 -\ell_O(O^B/T_B)}{e}.
$$

This formula uses two integral restriction images of the *same* algebra. It becomes a difference of Smith valuations when generator matrices are available. It gives zero when the unwanted set is empty. The proof also treats the case in which a different tuple of local types is chosen at each point. The associated endomorphism can cost the valuation of the finite group order, at most $2fr^2$. The original paired inequality already budgets this amount. The point estimates therefore suffice with the same constant $C=C_T$ as the lattice lifting estimate. [Congruence ideals and point-dependent supports](continuation_v84/typeideal.tex)

For these supports the cut representations become crystalline over one finite normal extension at each tested place. The direct and dual local lifting arguments give costs $2r e_{\max}$ and $2 e_{\max}$ for the rank and character blocks. The global Selmer argument converts them into a bound on the displayed length. It includes the class group, all the cyclotomic Tate–Shafarevich lengths and the loss from a possibly nonunit root difference. The alternate denominator argument then proves the fifteen conditions on one hub. Returning to the original family costs at most $d_j\log N_G$, absorbed at a cutoff fixed before the member and lift. The original rank, finiteness condition and summability test survive this comparison. [Potentially crystalline families](continuation_v84/potential.tex) · [Local lifting](continuation_v84/typeplace.tex) · [Global Selmer estimate](continuation_v84/selmer.tex) · [The simultaneous estimate](continuation_v84/alternate.tex) · [Return to the original family](continuation_v84/binding.tex)

## Where to resume

1. **Integral lifting at the type primes.** The formal route uses the absolute constant $C_T=40$. The remaining mathematical estimate concerns finite integral cocycles through surjective lattice maps among potentially crystalline representations with specified jumps and tame inertia. P84B3 shows exactly where this uniform estimate would complete the bound for families satisfying the original Galois preconditions and four ties. Q84T1–Q84T4 descend the field and coefficients and prove exactness in the middle with a finite terminal cokernel. F84R1–F84R3 give the uniform Frobenius bound on a power of the variable modulo $p^b$ and transport a sharp cokernel bound to the tame invariant lattices. Q84T5 proves the interpolation denominator bound $(N-1)R$ and, from explicit Euler-connection estimates, the sharp $p^{2(N-1)R}$ cokernel bound. A complete proof of those connection estimates is still needed. The remaining integral work is the construction of a bounded representative, the lift across the monodromy obstruction, and the return of the lifted vector to an integral finite cocycle. [Quantitative reduction](continuation_v84/quantitative.tex) · [Frobenius and invariant lattices](continuation_v84/power.tex) [Family implication](continuation_v84/binding.tex) · [Previous source comparison](continuation_v83/external_sources.md)
2. **The selected-member hypotheses.** In the source's eighteen-field Galois record, the other fields to assemble at their native quantifiers are `what₂`, `adm`, `Conclusion1`, `z`, `rhoBar`, `g3p`, `weight`, `depthG`, `bc`, `lam`, `trip`, and `good`. Several have earlier conditional ingredients. Of the four original ties, the first and third are proved. For the second, the remaining work includes the compact depth-zero type comparison. For the fourth, M84T8 isolates the local type-occurrence comparison and a compatible finite series system. [Original field definitions](https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AutomorphicArithmetic/ThetaCorrespondence/ThetaPairLifts/ThirdPlaceSeries/GaloisPreconditions.lean#L13-L31) · [Member proofs](continuation_v84/member.tex)

## What the external roadmap contributes

The corresponding roadmap argument B8.42bs1d isolates the tame-field reduction and the integral lifting calculation, and points to the model estimates used by the formal proof. Two details matter in using it here. The Kisin realization is exact in the middle and may have a finite terminal cokernel. Also, for the Eisenstein polynomial $E=u^e+p$, the initial decomposition is $p^b y_2=y'_2+m_2$. It follows that $y'_2+\varphi m_2=p^b y_2+(\varphi-1)m_2$. The latter difference disappears in the class comparison. Q84T3–Q84T4 give the arguments and track which of the monodromy estimates still needs proof. [Roadmap at the inspected revision](https://github.com/rh-lean-roadmap/rh-lean-roadmap/blob/e481c74135c4f0c20980f2371badbd0276ae8829/docs/src/book/main.tex#L55800-L55867) · [Integral comparison](continuation_v84/quantitative.tex) · [Earlier survey of the other sources](continuation_v83/external_sources.md)

## Verification

The verifier compares each marked manuscript argument and its cited Lean byte ranges with the pinned Git tree, and checks the dependency graph, predecessor totals and typeset supplement. The new arguments are human proofs. This edition did not rebuild the Lean development. [Checkpoint](CURRENT_CHECKPOINT_v0_84.json) · [Claim and source ledger](continuation_v84/claims.json) · [Validation](continuation_v84/validation.json)

~~~sh
python3 continuation_v84/verify.py --formal-git formal_source
~~~
