# Integral lifting at the type primes

**Edition 0.85 · 25 November 2026**

The potentially crystalline lifting estimate required by the denominator argument now has a human proof on the original integral Galois lattices. The absolute constant is 40. This discharges the local hypothesis left in P84B3. On a family with the original Galois preconditions, four compatibility conditions and the other hypotheses of P84B3, the proof gives the denominator estimate on the uncut family. Four further preconditions now hold on the actual selected members. They give the two archimedean weights, spherical inert base change, goodness of every finite-type row label and the wild inertia polynomial at the two type places. **Ten whole obligations remain open**, all shared by RH and unrestricted Dirichlet GRH. [New proofs (PDF)](RH_new_proofs_v0_85.pdf) · [Cumulative manuscript](RH_readable_reconstruction_v0_85.tex) · [Open contracts](continuation_v85/obligations.json)

## The estimate on an arbitrary test

Take a surjection of Galois-stable lattices $g:T_1\to T_2$ of any ranks allowed by the original potentially crystalline test. Let $N$ bound its inertia support, $R$ be the largest Frobenius period of a ratio of inertia characters and $[-b,H]$ contain its labelled jumps. Use the original hypotheses, including $1\le b<H$, the cardinality bounds on characters and jumps, and $40(HN^2+N^3)<p$. For every integral Bloch–Kato finite cocycle $c$ of $T_2$ there are a finite integral cocycle $\widetilde c$ of $T_1$ and $t\in T_2$ satisfying

$$
p^d c(\gamma)=g(\widetilde c(\gamma))+(\gamma-1)t,\qquad
d=6(N-1)R+(N+5+2R)b .
$$

The equality holds on the whole local Galois group. Thus multiplication by $p^d$ kills the cokernel on finite cohomology. We have $4R\le N^2$ and $d\le 7\{NR+b(N+R)\}$. This proves both conclusions of the local admissibility test with constant 40. [Local theorem and family consequence](continuation_v85/assembly.tex)

| Step | Mathematical content | Proof |
| --- | --- | --- |
| Realize the original test | The kernel, source, target and the cocycle extension have compatible tame models. The period maps agree on their common integral coordinates. The de Rham filtration gives the physical lattice at each root of the Eisenstein polynomial. | [R85P1–3](continuation_v85/realization.tex) |
| Bound the cokernel | A first-order crystal calculation supplies an integral ordinary derivative on the Frobenius columns. Two successive reductions in the variable degree give a cokernel killed by $p^w$, $w=2(N-1)R$, including on the invariant lattices. | [E85C1–4](continuation_v85/connection.tex) |
| Lift across the kernel | The obstruction is a principal part. Its rational Euler operator has distinct eigenvalues indexed by shifted jumps. Its integral inversion and a convergent correction remove the entire obstruction. | [K85F1–4](continuation_v85/kernel.tex) · [M85N1–6](continuation_v85/monodromy.tex) |
| Return to an integral cocycle | The corrected vector has an actual crystalline primitive. Its Galois differences lie in the original lattice after the stated power of $p$. Two representatives differ by the coboundary of an integral vector. | [P85C1–6](continuation_v85/period.tex) |

The initial representative costs $w$ powers of $p$. The shift into $u^eY$ costs $b$. The middle lift costs $c_1+2w+b+h_L$, with $c_1=b(R+1)$ and $h_L=(N+1)b$. The return to a finite cocycle costs $c_1$. Their sum gives the displayed exponent. No term depends on the ranks of the test lattices. [Assembly](continuation_v85/assembly.tex) · [Coefficient descent and prime guard](continuation_v84/quantitative.tex)

## Which external results enter

Bhatt and Scholze provide the equivalence for integral crystalline lattices in Theorem 5.6, the common crystalline period comparison in Proposition 5.3, and the filtered modification and its recovery in Construction 6.5 and the proof of Theorem 7.9. R85P1–3 use these specific comparisons to identify the original period and filtration conventions. The estimates for the integral cokernel and the monodromy correction are proved in the supplement. The earlier comparison with Rubinstein, Zhang, the two GitHub reconstructions and the declaration-indexed roadmap remains available. [Bhatt–Scholze, *Prismatic F-crystals and crystalline Galois representations*](https://arxiv.org/abs/2106.14735) · [Source-by-source review](continuation_v83/external_sources.md) · [Roadmap comparison in edition 0.84](RH_reconstruction_progress_v0_84.md#what-the-external-roadmap-contributes)

## Where to resume

Ten of the eighteen original Galois preconditions now have human proofs at each selected member. This edition adds four.

| Field | Result on the original member |
| --- | --- |
| `weight` | The two conjugate infinity multisets are the prescribed shifted multiset and its negative. The proof reads the shift $1/2$ at the original coefficient representation. [W85M1](continuation_v85/memberfield.tex) |
| `bc` | Each definite row spherical at the nonsplit places has one base-change list satisfying positivity of the ranks, distinctness, all split and inert comparisons and its infinity weight. [B85U1–2](continuation_v85/basechange.tex) |
| `good` | A single row vector produces a simultaneous finite type. Comparison with inertia at the chosen tame generators gives both polynomial goodness tests, also for the conjugated row. [G85M1–3](continuation_v85/member.tex) |
| `depthG` | Every unitary representative at a tested type place has wild inertia polynomial $(X-1)^{n_V}$, including representatives outside the image of a Hecke-point choice. [D85G1](continuation_v85/depth.tex) |

The earlier six fields are `large`, `nct`, `same`, `block`, `muUnr` and `c2`. The eight still to be supplied in the original design ranges are **`what₂`, `adm`, `Conclusion1`, `z`, `rhoBar`, `g3p`, `lam` and `trip`**. The second and fourth of the four ties also remain. The next comparison concerns `g3p`, which asks for the residual tame eigenvalue condition. The new wild-inertia identity and the row-label calculation supply local information at the type places. The residual comparison must match the characteristic polynomials on the specified tame generators after reduction, including the prime-to-$\ell$ parts of the label roots and the rank-one character. The general family assertion A85D3 becomes the selected whole obligation only once the remaining hypotheses are supplied at that scope. [Original field definitions](https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AutomorphicArithmetic/ThetaCorrespondence/ThetaPairLifts/ThirdPlaceSeries/GaloisPreconditions.lean#L13-L31) · [Earlier member proofs](continuation_v84/member.tex) · [Exact remaining contracts](continuation_v85/obligations.json)

## Verification

The ten new proof sections contain 33 numbered claims with 385 cited ranges in 169 pinned Lean files. The verifier checks those ranges against the original Git tree, the manuscript hashes, the dependency graph, the original obligation contracts and the typeset supplement. The cumulative inventory is 4,753 claims. This edition did not rebuild Lean. [Checkpoint](CURRENT_CHECKPOINT_v0_85.json) · [Source ledger](continuation_v85/claims.json) · [Validation](continuation_v85/validation.json)

~~~sh
python3 continuation_v85/verify.py --formal-git formal_source
~~~
