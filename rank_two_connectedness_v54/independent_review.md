# Independent review of RTC1–RTC25

**Verdict: PASS.** I independently read all 25 human proofs and checked their stated endpoints against the pinned source. No unresolved mathematical or scope defect remains.

- Component: `rank_two_connectedness_v54`.
- Reviewer: `/root/bessel_nonvanishing`, independent of the author.
- Frozen main SHA-256: `847dc0b2d94dca7541ef6c34b93ecc7c43e8cfbf4207234a975f08dc0952d91c`.
- Source commit: `7cbf7a0c32fca1badf05931879a37c3f8a2b03b4`.
- Bindings independently verified: 25 proof blocks, 45 complete source snapshots, 55 exact source ranges, and 2 inherited human-proof blocks.
- The final standalone two-pass draft TeX record is PASS, with no errors, missing characters, undefined references or overfull boxes. No Lean replay was used.

## Weighted universal coordinates and topology

RTC1–RTC9 reconstruct the actual weighted presentation from the supplied universal space. The tangent-space argument selects finitely many actual centered entries. The decisive weight-separation step takes values in `(R/m^N)[[Z]]` and uses the injectivity of `D[Y,Y^-1] → D[[Z]]`, `Y ↦ 1+Z`. It therefore works with nilpotents and in residue characteristics dividing weight differences; it does not replace an integer grading by a grading modulo the characteristic.

The zero-weight monoid and each weight fiber have the required finite generators by the coordinatewise-minimal-elements argument. Their formal-series substitutions and regroupings are coefficientwise valid. The proof identifies the original closure B with R_0 and the original entry algebra A with the finite-sum graded algebra. In particular it proves the literal `wpres`, `co_B` and every `gr_A` field for both ranks two and three. The explicit `M=DN+L` argument supplies the whole fixed-weight topology comparison and hence every `cont_u` conclusion. No `FinA`, finite-point or automorphic result is imported upstream.

I checked these scopes directly against `ResMapBijective.lean`, `LeAdicClosure.lean`, `ContMap.lean:307–308`, `CoB.lean:8–9`, `IsInternalCongr.lean:81–82`, and `MemPowSmulLe.lean:14–15`.

## Strict cocycles and the actual rank-two core

RTC11 normalizes a strict cone representative using `X=-z(c)/2`. Its alternative formula in terms of `z(g)` and `z(gc)` proves local constancy without assuming continuity of the arbitrary character chi. The nonvanishing argument retains the local primitives, so a globally zero normalized cocycle really would represent zero in the strict cone. RTC12 checks the twist and the local minus sign explicitly.

The only scope clarification requested during review concerned the opening fixed coefficient ring. The final text states RTC11–RTC14 for a field k and Frame.Ok without choosing O or Space; it also correctly notes that Frame.Ok contains a finite-k field. The arguments were already valid at that original scope. Their exact source contracts are `SmoothVectorFixedByOpenSubgroup.lean:6–7`, `ExistsMemStrSNeZeroOfFrameOk.lean:12–13`, and `FramePointFiberNonempty.lean:6–7`.

The realization in RTC15 is sound for every prescribed k-algebra Q. It first uses the allowed coefficient algebra `k[[T_1,...,T_t]]`, where the universal residual representation is diagonal. The image of B is proved constant by continuity, and the image of A is then proved polynomial. Only this polynomial image is evaluated in Q. This avoids an unjustified formal-series evaluation and does not use the broader `point_loc` supplier or ACP's narrower finite-point shortcut.

RTC17 treats the actual field `Frac(A/p)` with its induced k-structure; it imposes no finiteness or algebraicity on this core-point field. RTC19 uses a single strict anchor chosen before all later points. The generic prime of the polynomial line is contained in both endpoint primes, and each of these three primes belongs to the original BB. The argument only needs this three-point subspace. It correctly avoids claiming that every other specialization of the line stays in BB. Thus the full original `preconnected_rank_two` is proved on the required space, without a Big, modularity or finite-point premise.

RTC20 installs only the Noetherian, preconnected-core, open-type-I and closed-good-locus fields it proves. Its remaining local chart, sharp dimension, incidence and seed inputs agree with the actual `ComponentsGoodRankTwo.lean` consumer.

## Exact finite-point descent

RTC21–RTC24 give a complete independent route to the original `finPtDown`. The q-power construction supplies the unique finite-residue coefficient section in an equal-characteristic complete test DVR. It respects every prescribed finite-field embedding. The compatible finite residue fields are then placed in one finite field L, and coefficientwise extension produces the required injective local map to `L[[T]]`, with the original maps on k preserved.

RTC23 checks the new IsCD structure, scalar tower, entry and character continuity, exact diagonal residues and the same ordinary inertia test. RTC24 applies the extended-frame FinPt to that actual point and cancels the injective polynomial map on the characteristic-polynomial identity. This works at every original rank and prime, including characteristic two, and does not assume Frame.Ok. I checked the literal `FinPtDown` contract and producer `FinPtDown.lean:113–155`, as well as the original IsCD fields.

The conditional RTC25 join keeps the extended and original coefficient frames distinct: ACP11 supplies the extended-frame FinPt only with its actual Space/OffFin inputs, RTC24 descends it, and AFE20 then applies on the original marking. Both inherited blocks and their parent bindings were independently verified.

## Boundaries and final binding

The packet does not supply the generic point_loc theorem or rank-three triangular realization, local completion/flatness dictionaries, full rank-two or rank-three propagation, AllGood/OffFin producers, automorphic seeds, original cohomological P, GdEnd/HostEnd, or the terminal Alt witnesses. These boundaries are consistent in the manuscript and contracts. No whole selected RH/GRH obligation is declared closed.

Besides the scope clarification above, one typographical correction changed `quad` to the intended TeX spacing command in RTC.34. Both corrections are included in the frozen main hash. The JSON review records a reasoned verdict and exact proof-block hash for every RTC claim. No author proof or author metadata was modified by this reviewer.
