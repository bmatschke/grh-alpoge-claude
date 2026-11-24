# Congruence chain through the original family — v0.24

## Result and scope

LN1–LN10 close the integral-cut, congruence-module, multiplicity, weighted-prime-sum and uniform-family transport chain. The endpoint is the literal `LinkN` inequality on the **original actual family**, with the original cohomological series and its original finiteness and summability guards.

The chapter gives a complete supplier from explicit per-prime local denominator estimates. It does not replace those arithmetic estimates with an abstract assumption called `LinkN`, and it does not retain the numerical `KudlaFamilyStatement` as a black box. The numerical export is proved, including the sparse small-order inert primes and the exceptional tail. The source constant `2000(C+1)^3` is retained, with a possibly larger uniform threshold.

The deep local Galois bounds and the compatibility of the actual theta/type/local state are still inputs. `CutGivesAlt` has additional `NormChoiceFacts` and `Tie4` requirements beyond `CutD.Good`; the chapter does not assert that these stronger fields follow from making a lattice quotient.

## Two substantive simplifications

### Integral central coefficients without character classification

For a finite group G of order N and central idempotent e in C[G], left multiplication by g⁻¹e satisfies T^(N+1)=T. Its eigenvalues are zero or Nth roots of unity, so its trace belongs to Z[ζ_N]. In the group basis its trace is exactly N·e(g). This proves that N·e lifts centrally to the original coefficient DVR whenever that original ring contains ζ_N.

In the source, the good element e0 is a sum over **ordered root vectors**. Every summand is lifted separately, and the same multiplicities are preserved. No claim that this sum is idempotent is inferred from its formula. Its identity/zero action on the actual good/bad theta types remains the exact compatibility input used in constructing the selected Hecke set.

### Coordinate ideals control the congruence module directly

Let M be the actual finite free DVR module with rational decomposition V=⊕V_x. For a subset A, its congruence module is C_A=π_A(M)/(M∩V_A). If I_x(A) is the image at x of the Hecke operators supported on A, a filtration by the individual V_x gives

    length C_A ≤ Σ_(x∈A) dim(V_x) length(O/I_x(A)).

Each graded piece has at most dim(V_x) generators and is killed by I_x(A). This proves the estimate without changing the lattice or invoking an integral semisimplicity assertion.

For the actual cut M′=M/(M∩V_(Sᶜ)), the kernel of C_Y(M)→C_Y(M′) is killed by N_G. Its inverse image in π_Y(M) has at most Σ_Y dim(V_x) generators. Consequently

    η_i(original) ≤ η_i(cut) + Σ_good multiplicity · v_l(N_G).

Restriction of operators gives I_x(original Z)⊆I_x(cut Y). Combining this with the filtration yields the original-row `adm1` inequality with the **original** `vcc` ideals. No surjectivity of the map between congruence modules is assumed.

## Complete endpoint chain

| Claim | Mathematical work | Explicit boundary |
|---|---|---|
| LN1 | Trace proof of original-ring integral central lifts; literal ordered good-element sum | Original coefficient embedding/root-of-unity data |
| LN2 | All five `CutD.Good` fields, including every representative and every tame generator in `Nc` | Actual e0/type action, tame-label dictionary, same-point constituent permutation, eigen-action compatibility |
| LN3 | Original spectral quotient, free cut lattice, preserved eigenspaces/multiplicities, finite lengths | Rational eigenspaces actually span; separation alone is insufficient |
| LN4 | Direct coordinate-ideal filtration inequality | Data of LN3 |
| LN5 | Cut-kernel loss, exact normalized valuation, original `adm1` | Integral cut operator and exact selected/good/theta sets |
| LN6 | Disjoint localisation multiplicities and theta injectivity from nonzero row scalars | `ConclusionZ`, internal isotypic decomposition, localisation uniqueness; reference rank equality unless both theta injectivities are supplied |
| LN7 | Exact place weights, d_j·log N_G global cut loss, local-to-global denominator sum | Actual place/eta ties; local arithmetic inequalities and summability guard |
| LN8 | All numerical prime envelopes, progression sparsity, exceptional tail and uniform thresholds | Listed raw local bounds; actual parameter record and fixed polynomial parameter budget |
| LN9 | Exact same-data `gd` transport and original-family restoration | `LinkN` on the cut, original multiplicity/rank, uniform size parameters |
| LN10 | Complete original-family `LinkN` from explicit local inputs; actual table assembly | Deep local denominator suppliers and compatible state remain visible |

## Why the prime sum closes

The numerical budget is Q=f m b L², where L=x^epsilon and b=exp(L). Ordinary primes up to z=lStar split into the source's split, small inert with large order, medium inert, and small inert with small order cases.

For small-order odd primes, the least exponent o_l with l^o_l=±1 modulo 2^(e+2) is at most 4L_w. A valuation argument then forces l=±1 modulo

    M = 2^(e+2−floor(log_2(4L_w))).

The actual parameter inequalities give M≥n/L+1 and r≤2m(n/L)². Summing log(l)/l² along the two spaced progressions gives the required factor m, instead of losing the much larger factor r. This is the significant arithmetic sparsity step in the numerical export; the proof is included in full.

The band condition gives a pointwise bound r η_3 I(l)≤16mb/l outside a bounded small-prime range. Ordinary harmonic sums then bound all flat and ramification terms. The cost for the ordinary primes is at most 1000(C+1)^3Q.

For exceptional primes above z, their count is at most 388U^8 and each local envelope at most 10^4(C+1)^2U^9, where U=x^(C+2)exp(x^(epsilon/4)). Their logarithms are at most 3U, so their whole cost is O_C(U^18)=o(b). Generator-prime costs and the scalar logarithmic budgets are likewise o(b). The separate small and q,d prime bounds fit inside the remaining margin, yielding 2000(C+1)^3Q.

These are bounds for every finite prime set. No density theorem, Chebotarev theorem or unproved prime-counting statement is used in this numerical export.

## Exact preservation of the original object

The source `gd` family copies the original coefficient number field, place weights, theta spaces, size data, lift ranks, l-adic cohomology data and `vvTerm`. It changes the local Hecke sets/modules and their eta losses through the literal `ndCut` and `setRaw` constructors. Its norm choice is the transported original `nchTr`.

Consequently the global cut comparison is

    etaSum(original) ≤ etaSum(cut) + d_j log N_G.

The elementary bound |GL_r(F_g)|≤g^(r²) gives

    log N_G ≤ f r²(log g_0 + log g_1) ≤ C_N x^(C_N) L.

For fixed epsilon>0, x^(C_N)≤b eventually. Thus this extra term is absorbed into C_N times the original `LinkN` polynomial budget. The coefficient on the cohomological series remains **exactly d_j**, which is the coefficient required by DA2.

The threshold is the maximum of finitely many statements already uniform over every actual family index. No finite index set or maximum over family members is assumed. The final quantifiers are

    exists K,x0; for all x≥x0 and all i∈Fm.Ix(x):
      ShaFinOdd(D_xi) → for every allowed j:
        Summable(vvTerm(D_xi)) → original-family LinkN inequality.

## Dependency audit delta

`DA-next-02-b` is closed as a human proof of the full stated cut-to-original implication. LN1–LN7 supply its algebraic/multiplicity/weighted-loss content, and LN9 proves its same-object and threshold transport.

`DA-next-02-d` has a narrower frontier: the numerical `KudlaFamilyStatement` supplier is now proved in LN8–LN10, but the actual `AdmF`/local arithmetic table remains an input. `DA-next-02-a` and the linked-bundle `DA-next-02-c` are not marked globally closed: their deep Galois/transported-facts suppliers have not been proved merely by expanding the final predicate wrappers.

The remaining input ledger distinguishes the exact local denominator inequalities, spectral/theta/type identities, parameter budget, cohomological guards and stronger cut-facts transport. Algebraic and analytic elementary facts used in the new chain are proved in the text. Labels such as Fontaine, Bloch–Kato or Bhatt–Scholze in the source's `Hypotheses₂` are not automatically declared matched classical inputs; separately completed local-duality or other claims can be inserted in that ledger.

## Verification and files

The source is pinned to `7cbf7a0c32fca1badf05931879a37c3f8a2b03b4`. `provenance.json` records 155 declaration-range anchors in 39 source files, all checked byte-for-byte against the pinned Git objects, plus hashes of all ten written proof paragraphs. The builder is reproducible with `python congruence_chain/build_provenance.py --repo PATH_TO_CHECKOUT`.

The frozen `main.tex` SHA-256 is `033694f3a26f131b4ebb7b49557955e56478acd5be3ae4fbd1db32bfea0c0cac`. The root independently reviewed the mathematical algebraic and numerical arguments; its review is recorded separately. Draft-mode TeX compilation checks syntax and reports layout warnings, but is not a mathematical check or a PDF visual review. No Lean replay was run for these human alternatives.
