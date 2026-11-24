# Independent review: denominator export v0.50

**Verdict: PASS.** DNE1–DNE14 prove the stated original implications `ConclF → AdmF → LinkN`, with the unchanged uniform constant and the original field, host, rank, and summability/finiteness guards. The common arithmetic supplier remains a premise; this review does not close `GLOBAL_DENOMINATOR`.

Reviewer: `/root/geometry_alltest`. Reviewed proof SHA-256: `bcaae1d8952f75c04b0661af770150853929f62cc1f274807b081c75df1f68c3`. Source commit: `7cbf7a0c32fca1badf05931879a37c3f8a2b03b4`.

## Exact source and proof checks

Independently compared all 24 supplied source files with their pinned Git blobs and recomputed all 32 source-range hashes. Recomputed every DNE claim-block hash against the current proof. All match. The companion JSON contains exact line ranges and hashes. No Lean replay was performed.

## Corrections resolved before acceptance

- **DNE7:** the draft must prove that the dyadic exponent lies in the range of LFS2. The current proof derives `2^e/Lw ≥ 2R0 ≥ 6`, hence `4Lw < 2^e` and `v < e`; this is sufficient. This issue had already been identified by the author and was independently checked in review.
- **DNE5:** the original `lenB` has no explicit inert predicate in its second branch. The current proof removes that extra condition and explains why ordinary primes are split or inert. The scalar table now matches the source literally; no estimate changed.

## Claim-by-claim mathematical review

### DNE1

PASS: the coefficient-place normalization uses the actual coefficient field K, whereas n_lambda and degree 2f use the host E. The degree formula, nonnegative weights and actual etaJ_tie give the stated inequality even if dZ0 or the support is zero. No division by a row rank is used.

Proof block SHA-256: `eed11168abd30abf04e5a88fd3ba6061789f417a94adbd919c0a14e69c6f92e0`.

### DNE2

PASS: use the identity residue exponent modulo M, finite-precision cyclotomic approximation on the actual algebraic closure, and extension of an automorphism fixing E. For odd p not dividing M, odd tr makes -1 give valuation zero. For p dividing M, the binomial valuation is v_p(M)+v_p(tr), including p=2 because 4 divides M and tr is odd. Existence of a finite valuation identifies the source nuOf with the displayed minimum. The weaker log M budget is sufficient for the unchanged endpoint.

Proof block SHA-256: `26105d2e4a5522795954c04e2a57f885fc12fd18f9bf720920b0f279ffe7e864`.

### DNE3

PASS: each branch of the original tab matches, including the shared StarF witness and the equal distribution at 3 outside small. The local length maximum and error maximum use precisely supZ/lenR on the actual good-point set with its empty-set zero convention. The four prime cases exhaust RangeAD and its complement.

Proof block SHA-256: `c6f049d7c5ed3043fa6c086e291bc50e7c794811e1e34ab77e85d67f2a795902`.

### DNE4

PASS: all seventeen AdmT fields are preserved. The original not-InertK-at-3 clause is used exactly for the inert rows, and the split row excludes 3 through p>=5. Small controls the exceptional zero branches; q,d are outside small and differ from 3. The separate starF_of constructor retains both 2 and 3 cases.

Proof block SHA-256: `48f4c0092e8d0f5c4fb6d5bf2cccfa70466457ed9357a4172d8a9d997b8621ce`.

### DNE5

PASS after correction of the literal lenB branch: the second branch now has exactly p<A and high order, without an additional inert predicate. Ordinary primes are split or inert by the original host classification. Summation retains both the C inside e_p and the outer C in the inert row. The local v_p(J) cost is retained; all added budgets are nonnegative. The original same-host vvTerm is identified before passing from its finite sum to the summable series.

Proof block SHA-256: `54a7263ae62fae9d6a618f5829dc5767446bf737974d31a769874490507e574d`.

### DNE6

PASS: original logeta, logDel (with its factor 1/2), Sc_eq, bT_le/rho_le, teta/kS_le, Neta, delta bounds, o_tie, Lw_le and radius/k_ge_mx yield the displayed uniform inequalities. The only varying analytic quantities have bounds K*x^a*exp(B*z^(1/4)). Both this scale and its product with bprime are o(b) because eps>0 and 1/4<1/3<1. Thresholds depend only on eps,C and finitely many fixed comparisons, not the family or indices.

Proof block SHA-256: `a9e79c9ba39a3b8d6f40e8dcb87ce0fbc3241356c53ec582be8a729685ec6c46`.

### DNE7

PASS after the pre-review correction: n=R0*z<=o*2^e and 2*o*Lw<=z imply 2^e/Lw>=2R0. With R0>=3 this gives 4Lw<2^e and v<e, justifying the untruncated inherited LFS2 residue calculation. The arithmetic-progression tail bound, r<=2mR0^2 and n<=o*M0*Lw give the announced 4m*z^2 bound uniformly for finite sets of odd integers.

Proof block SHA-256: `2472f812cd8a17453a0d9b17525bbbe90010b7752fc09c1c2a10c80fd97db3b2`.

### DNE8

PASS: Den first term cancels B0*pstar*z to at most C*f*m*b*z. The three e_p sums are bounded by b,8*b*z^2,2*b. The total e_p coefficient is at most (3+2C)*f*m. No prime density estimate is hidden.

Proof block SHA-256: `50ea695164733d2e3244205a638894c4e4532a3b17b5c2bfb1c598feebcf0307`.

### DNE9

PASS: (p-1)^j>=A and j+1<=3+log A yield the split of R(p). The H contribution is at most 8m*b*(1+log A)^2/z<=8m*b eventually; all remaining terms are polynomial times bprime or polynomial, hence <=m*b. Thus 36C*f*m*b is valid and implies the advertised 40C*f*m*b*z^2.

Proof block SHA-256: `086aaafed61b853feab96f5ca0ab54b21dcc5f5b69d0f72b7f72cfaece199637`.

### DNE10

PASS: the ordinary integer tail above A gives 64C*f*m*b, and DNE7 gives 32C*f*m*b*z^2 below A at low order. Their combination is bounded by 96C*f*m*b*z^2.

Proof block SHA-256: `c36d393d7d292218465d9c0aa09c5ea4dbf8d4f4df7e4a71488d67445a4b1333`.

### DNE11

PASS: the flat non-band terms contribute 36+2 units before 4fC. The actual band implication, C*(eta3+S+z)<=wpp/4 and p>=2C yield p*s<=6b and hence at most 6b/wpp integers. Neta gives r*eta3<=4m*wpp, producing 24 units. The small p remainder contributes 4(2C+1)^2 units. The resulting 248C+16C(2C+1)^2 is correct.

Proof block SHA-256: `5602910f22bc70d05469098abc7f5626a032d5483acbb940110819382b44751e`.

### DNE12

PASS: log pstar>=z/2 eventually because Den has the common subexponential bound, and pstar>A. Exception cardinalities, all local costs and log p are controlled by the same bound. Generator costs use g_Y and CYL<=C. QS<=n^2 gives log QS<=2C log x for the small-prime class. The original M^36*t^150<=b^(1/2) bounds q,d. The four totals 1,1,2,4C units are valid.

Proof block SHA-256: `f630e8b85d321c9f806dc7b8f5595eb04d0f03f6f7c55e5d96b679af6e7ca1e0`.

### DNE13

PASS: the ordinary coefficient expands to 434C+86C^2+64C^3. Adding the four special classes and non-prime budget gives 5+438C+86C^2+64C^3<=2000(C+1)^3. The actual Nc is nonnegative, so adding its term yields the literal LinkN_at. Same dZ0 and same-host vvTerm are preserved.

Proof block SHA-256: `14918af5060f55c19d842ff2f4bc04d61315f3b10b1108e42b05c19d82cb84e3`.

### DNE14

PASS: the exported constant 2000*(abs(Ca)+1)^3 is chosen before the family. Ix_zero and L_eps give the scale epsilon restriction; L_x identifies later scale coordinates. The cutoff is the maximum of the admissibility cutoff, F.x1+1 and a uniform analytic cutoff. An actual table is chosen only after ShaFinOdd; it forces Ca>0. For Ca<=0 the guarded claim is vacuous. The summability premise and universal original lift quantifier are preserved, and the exact ConclF witness gives AdmFC member by member.

Proof block SHA-256: `7c2157e93cd24c5e593c743cf38aa06f0d908beb8d6e3a30b68803478265587e`.

## Retained premises and limits

The existence of the original common `HubData` satisfying `Concl`, its numerical local row bounds, killing facts, small-prime and type-prime bounds, and the common-family supplier remain upstream. The proof reconstructs table assembly and its global export, including the exact quantifier order. It intentionally changes only the auxiliary sufficient asymptotic cutoff and the intermediate cyclotomic budget; it does not claim the source’s particular pointwise `Large` predicate or its sharper intermediate `nuBudget` as new human theorems. Both simplifications preserve the full original export.
