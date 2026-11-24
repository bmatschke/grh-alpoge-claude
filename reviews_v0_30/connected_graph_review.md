# Independent review of the connected v0.30 dependency graph

**Verdict: PASS for the selected sufficient-route dependency audit.** This is a review of logical accounting, target quantifiers and source-interface matching. It does not assert that the remaining human reconstruction is complete. The underlying Lean proof is assumed checked and correct throughout.

## Reviewed snapshot

- Graph: `reconstruction_v030/dependency_audit_v0_30/obligation_map.json`.
- SHA256: `80dfdc1c531497b7cb23de964250c10d124037caf62bde8fe1f8136064b9314b`.
- Pinned source commit and checked local HEAD: `7cbf7a0c32fca1badf05931879a37c3f8a2b03b4`.
- Reviewer: `audit_count_path`.
- Review time: `2026-11-22T10:15:26.485716+00:00`.

The final graph contains 90 selected logical nodes, 11 work refinements and eight optional routes. All 90 logical nodes are reachable from the union of the two final roots. Independent traversal found no duplicate IDs, dangling `requires` references or cycles. The RH route reaches 70 logical nodes; the unrestricted Dirichlet-GRH route reaches 79. Work-refinement and optional edges are explicitly separated from sufficient logical implications.

All five declared package input hashes match their actual files. I also rechecked all 704 embedded source-range occurrences: these comprise 596 distinct ranges in 207 source files, with no recorded file-hash, range-hash or line-bound failures. These are provenance checks, not a replacement for the substantive contract checks below.

## Arithmetic cut and fixed-target quantifiers

The RH route correctly needs the fixed-field CorGK endpoint, the joint ordinary support producer for Count II, and Count V. The general Dirichlet route additionally needs the complete Case-III producer. The shared contracts are instantiated at the target carried by the consuming root. RH uses the principal character; general GRH fixes an arbitrary primitive character first and takes the universal conclusion afterwards. No single coefficient or window threshold uniform over all target characters is introduced.

KA5 uses the literal Case-III hypothesis that the full host character has odd order and is nontrivial. A host character obtained from a target of 2-power order has 2-power order, so this case is empty. KA6 preserves that same fixed target through the actual sum, height, joint-window and VWinAt consumers. Consequently the graph excludes the complete Case-III chain from RH, including SeedIVAlt and Ctx3 promodularity, while preserving it for unrestricted targets. It does **not** remove Counts I, II or V from RH. The examples and source restrictions in the count audit preclude such an inference.

The narrower Count-I cut is CorGK only at the field Kchi selected by the target. PropGK followed by KA3 is one sufficient implementation, and KA4 supplies the actual CountI bound. The direct CorGK alternative is kept separate. The graph does not assert that a universal theorem over every quadratic field is necessary. Within the selected implementation, OneChar, InpZ, the original CNR3 scope and the relevant adjoint/coefficient obligations remain visible. RigII is deliberately opaque: the five source supplier arguments LitN, LemmaK, AdVanishQ, NewformAut and KatoTwo are recorded, but its partial navigation links are not a sufficient AND rule.

Count II remains one **joint** existence problem. On each original Link, the fixed embedding and common coefficient threshold precede the later coefficient DVR and universal data. One ideal must satisfy all six HidaPropsAlt fields and the original P1core. The graph does not combine an ideal satisfying Hida with an unrelated ideal satisfying P1. The original coefficient-prime range, including characteristic 3, remains intact; a published theorem restricted to primes greater than 3 is not promoted to the full producer.

For the unrestricted Case-III branch, the seed, tensor-factor tower, chain, descent and rank-four reduction producers remain separate. Their original conditional joins are either certified in their inherited scope or recorded as explicit open implication-reconstruction tasks. A seed alone does not supply the chain, promodularity or actual count consumer.

Count V correctly uses its own Gaussian/quartic-character field. This is distinct from the Count-I field Kstar(pK chi), which is Kstar7 for the principal target. At that target the Case-V constraints give e=1 and coefficient prime in {3,7}, while the dyadic conductors remain unbounded. The support, host/frame, local conditions, normalized length, marked element, rigidity and number bound are coupled on the original source data. The final helper contracts explicitly restrict to data arising from the fixed target. Fully universal source theorems are sufficient stronger implementations, not additional necessary universal target hypotheses. VanE, Xpp and the final installation retain their explicit B reconstruction tasks.

The possible reuse of a rank-four catalogue for the rank-three obligations remains an optional D matching route. It is neither a mandatory dependency nor a completed identification of the two source contracts.

## Global route and producer distinctions

The graph exposes the full ten-argument topDesWin interface. The common source classes and constants are fixed, and all nine Closed thresholds are joined before DesignExists selects one common family and character data. It does not combine unrelated families supplied by different individual estimates.

Host-window supply is an input to the open global design construction, rather than a sufficient producer by itself. Denominator, local coverage, retained defect, small rank, period/height, local gain and spectral bounds remain explicit obligations. Fullness/rank and global slope share the exact second-layer source match on the same class, with the hduty, tie, hU and hG arguments retained. Their broad theorem names cannot discharge those actual-instance hypotheses.

The completed metric transport, host/window transport, count aggregation and terminal numerical arguments retain all their arithmetic antecedents. An uncompleted conditional arrow is represented by its own open B or C task. This is essential to the graph's interpretation: its sufficient AND rules become complete implications only when every listed producer and proof-of-implication task is discharged. A completed implication is not being counted as a constructed arithmetic object.

## Two coverage findings resolved before acceptance

The first reviewed snapshot did not explicitly enumerate the M/Mprime/P algebra inputs within the native certificate. The final graph now includes the old exact LemmaMprime, LemmaM and framed-weighted-presentation nodes together with SP1–SP6 and FP8 proof provenance. This covers the literal InpZ and CountV antecedents in the recorded conditional scopes.

The Case-III certificate also originally named HFit without a literal proof anchor. The final graph now records NearSplit.Three0 and Fit, the CaseThree Four and HFit definitions, and Sp4In.hFit. The full human argument is included: Four.five, Four.sb and Four.psi are the three Three0 fields; with Ok and Ctx3 they select the right branch of the definition of Fit. Four.quad is unused in this dictionary step. This is an elementary interface closure, not a missing deep producer.

Both findings are resolved in the hash-bound snapshot above. No further review blocker remains.

## Limits of this review

The graph is a sufficient selected-route audit, not a proof of absolute mathematical minimality and not a listing of every transitive Lean dependency. Its open contracts still require the human work recorded by their B/C/D labels. No new Lean build was performed. I checked placement and exact scope of published-theorem certificates; this review does not independently repeat every inherited literature verification. The distinction between inherited and freshly rechecked certificates is preserved in the package.

The accompanying JSON records the individual checks, exact snapshot hash, structural results, input hashes and resolved findings in machine-readable form.
