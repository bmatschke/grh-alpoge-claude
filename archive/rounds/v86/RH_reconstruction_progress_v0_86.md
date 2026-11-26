# Recovering a theta row from its upper Hecke point

**Edition 0.86 · 25 November 2026**

Sixteen of the eighteen original Galois preconditions and all four compatibility conditions now have human proofs on the selected members. The two remaining member fields, **what₂** and **z**, are each equivalent to the same upper multiplicity inequality. The proof also identifies the family-level choice that must be matched to the original design. **Ten whole obligations remain open**, all shared by RH and unrestricted Dirichlet GRH. [New proofs (PDF)](RH_new_proofs_v0_86.pdf) · [Cumulative manuscript source](RH_readable_reconstruction_v0_86.tex) · [Original open contracts](continuation_v86/obligations.json)

## Why the upper label determines the lower row

Let a nonzero lower row of rank $r$ pair with an upper label of rank $r+t$, where $r<t$. At a split place $w$, the local theta correspondence says that the upper parameter consists of the lower parameter and a string of $t$ twists of the character $\mu_i$, all twisted by $\eta^{-1}$. If two upper labels pair with the row, their split parameters agree. The Galois representations of their base-change lists therefore agree on a dense set of split Frobenius elements. This recovers the global lists. At a nonsplit place the unramified base-change multiset recovers the spherical representation up to its relative Weyl group. Thus all finite components agree and the upper labels coincide. Positivity of the down-up scalar then puts the entire lower image inside this one upper type. [Point representations](continuation_v86/points.tex) · [Positive scalar and ranks](continuation_v86/membernew.tex) · [Uniqueness of the lift](continuation_v86/theta.tex)

At almost every split place, the string supplies a unique root of absolute value $q^{(t-1)/2}$, where $q=\mathrm Nw$. All lower roots are smaller. A cuspidal block of length less than $t$ cannot supply the extreme root. Because $r+t<2t$, exactly one block can have length at least $t$, and its base has rank one. Its extreme root forces its length to equal $t$ and identifies its character locally. Rank-one uniqueness over the split places gives the global character. Deleting the string recovers the lower parameter even at ramified split places. The polynomial conditions on a good row then force every candidate lower list to be a single rank-$r$ cusp. This proves the missing row assertion in the original **Conclusion1**. [U86T1–4](continuation_v86/theta.tex) · [S86A1–4](continuation_v86/rows.tex)

## What was proved at the original member

| Newly completed field | Mathematical content |
| --- | --- |
| **Conclusion1** | The original upper Hecke points have integral Galois families with the prescribed weights, residual polynomials and distinct constituents. A nonzero theta row has a unique upper type and the required lower parameter. [H86P1–4](continuation_v86/points.tex) · [U86T1–4](continuation_v86/theta.tex) |
| **rhoBar** and **g3p** | At the two type primes, both the matrix eigenvalues and the character are compared at the specified tame generators after reduction. The resulting missing-divisor argument gives absolute irreducibility and exclusion of the distinguished character. [R86G1–7](continuation_v86/residual.tex) |
| **lam** | Averaging at the original level gives the same metric factor on the two sides. The restricted adjoint has the named positive scalar on every nonzero lower type. [L86M1–4](continuation_v86/membernew.tex) |
| **trip** | A simultaneous eigenvector descends with the stated level character and good projector. Its signature has the required Frobenius reading at the original row and coefficient place. [J86S1–3](continuation_v86/trip.tex) |
| **adm** | At every $1\le j\le m$, the named isotypic components span the lower level space. The good reference type has simple cuspidal base change. Comparing its multiplicity on the two unitary inner forms yields the exact dimension of each lower summand. [F86I1–2](continuation_v86/packet.tex) · [Assembly](continuation_v86/assembly.tex) |

The second compatibility condition now has a single depth-zero witness whose eigenspaces satisfy the original spanning test. The fourth identifies the finite series seen in the actual local parameter. With the character comparison M84T10 and crystalline inertia comparison M84T2, these give all four ties on the same original member. [T86C1–6](continuation_v86/ties.tex) · [Ramified local parameters](continuation_v86/inertiatype.tex)

Two coefficient-field details matter for the residual result. At a type prime outside its bad set, a proper invariant subspace or its quotient of dimension $d\le r/2$ would select a Frobenius-stable set of $d$ eigenvalues at every designated place above that prime. The original label requires some place to lack a divisor of degree $d$. The two bad sets are disjoint, so a suitable prime exists for each coefficient characteristic. For integral descent, absolute irreducibility supplies $r^2$ group matrices whose reductions span the matrix algebra. Their trace Gram matrix is invertible over the original ring $O_i$. A lifted primitive idempotent in their integral span produces the required free column module of rank $r$ over $O_i$. [Reduction and integral descent](continuation_v86/residual.tex)

## Where the denominator proof resumes

For a localization $i$, let $T$ be its upward theta map, $E_x$ the upper eigenspace at a good point $x$, and $A_x$ the sum of lower rows with the corresponding parameter. F86D1 proves that different choices of a parameter list for $x$ give the same $A_x$. The map $T$ is injective, $TA_x\subseteq E_x$, and the good lower space is the sum of the $A_x$. The $E_x$ for different points are mutually orthogonal. It follows that

$$
\sum_{x\ \mathrm{good}}\operatorname{mult}(i,x)-d_M(i)
=\sum_{x\ \mathrm{good}}\dim(E_x/TA_x)\ \ge 0.
$$

**The upper multiplicity question is whether this difference vanishes at every localization.** The remaining condition asks for the reverse inequality. The proof shows exactly how it gives the two outstanding member fields and how each of those fields implies it. With the lower spanning result, all six entries of the third block of point conditions hold. The remaining separate injectivity test asks whether the prescribed downward lift kills any nonzero good upper vector. [Point and row comparisons](continuation_v86/rowocc.tex) · [Dimensions and the downward kernel](continuation_v86/rowend.tex) · [Equivalence with the original conditions](continuation_v86/assembly.tex)

There is an analytic route to this injectivity. The partial standard $L$-function of a good upper point has a simple pole at $(t+1)/2$ with nonzero residue. This is $t/2$ in the variable of the doubling integral. At the finite type primes the good projector annihilates both families of weighted mirabolic averages. Passing from a nonzero integral with a varying Schwartz test to the member's prescribed test still requires the doubling and residue comparison for its form, archimedean approximation and finite-place generation. The manuscript gives the precise hypotheses under which that implication works. [Simple pole and fixed Schwartz test](continuation_v86/pole.tex) · [Finite projector](continuation_v86/miravg.tex)

At family level, one cutoff per family suffices if it works for every member index. Raising the initial scale preserves the member, coefficient data, norm choice and twists. To apply the resulting bound to the original design class, its late members and their full objects must be identified with the actual layer witnesses, including the selected norms. The specialization and the order of these choices are given in X86B1–2. [Family and selector comparison](continuation_v86/design86.tex)

## Verification and sources

The ledger binds every new proof to exact manuscript bytes and excerpts of the original Lean source. The two readers were typeset, and all 50 new proof headings were recovered from each PDF. The supplement has 34 pages and the cumulative reader has 3,263. The source check covers 427 ranges in 216 pinned Lean files. Verification checks the 18-field partition, all prior claim IDs, the original open contracts, and the 121 nodes and 161 edges in the selected graph. This edition takes the pinned formal proof as its reference. There is no new Lean replay. [Checkpoint](CURRENT_CHECKPOINT_v0_86.json) · [Claim ledger](continuation_v86/claims.json) · [Validation](continuation_v86/validation.json)

~~~sh
python3 continuation_v86/verify.py --upstream formal_source
~~~

The split lift uses Mínguez's explicit type-II correspondence. The multiplicity argument uses Labesse's base change at all split places and the generic pure-inner-form case of the Kaletha–Mínguez–Shin–White formula. The local comparison of the residual attachment away from the coefficient prime uses Varma's Theorem 1. The relevant hypotheses are checked in the corresponding proofs. [Mínguez](https://doi.org/10.24033/asens.2080) · [Labesse, Corollary 5.3](https://webusers.imj-prg.fr/~michael.harris/CBCM.pdf) · [Kaletha–Mínguez–Shin–White](https://arxiv.org/abs/1409.3731) · [Varma](https://doi.org/10.1017/fms.2024.7)
