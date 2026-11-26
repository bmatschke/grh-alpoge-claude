# Dependency audit for reconstruction v0.23

## Conclusion and scope

The useful milestone is now a set of **complete conditional chains with a small, explicit supplier frontier**, together with one substantial local representation-theoretic leaf whose proof is actually closed. It is not yet a human-readable proof of RH or Dirichlet GRH with every arithmetic hypothesis discharged.

HP1–HP4 prove the characteristic-zero canonical polynomial highest-vector, fixed-line and tensor-irreducibility inputs. HP5–HP6 connect these to the existing weight/form interfaces, preserving their supplied field, frame and row data. WB1–WB8 give a complete passage from the explicit same-object arithmetic contract to the positive character window and then the analytic zero-free conclusion. VW1–VW4 give a complete passage from the specified cohomological supplier statements to the literal `VWinAt` and the fixed-pair windows. The two latter achievements are conditional: their deep suppliers have precise mathematical content and remain visible.

This audit reads the v0.22 reconstruction and selected interfaces in the exact pinned Lean checkout, commit `7cbf7a0c32fca1badf05931879a37c3f8a2b03b4`. It does not extract all transitive Lean proof dependencies, replay the kernel, or assess prior verification claims. The user's report that the formal proof has been verified does not alter which arguments have been translated into readable mathematics. Sources and byte hashes for the interfaces discussed here are in `cut_interface_sources.json`; the independent WB/VW reviews are in `../reviews_v0_23/`.

## Why the inherited graph is not a completion certificate

The v0.22 recorded human graph has 1,168 vertices and 2,797 edges. References resolve and the graph is acyclic. It has 280 vertices without graph predecessors and 99 weak components. These figures are useful integrity checks, not measures of mathematical completion.

The reason is semantic. A recorded edge generally indicates a reference to another reconstructed claim. It does not necessarily represent an assumed source theorem, a required field identification, or an existence statement needed to instantiate a local theorem. For example:

| Historical claim | What the graph alone misses |
|---|---|
| AN2 | The prime-window hypothesis remains a premise, although there is no predecessor vertex. |
| AN3 | The analytic implication is proved from its window hypothesis; an empty `remaining_inputs` field does not construct that window. |
| SC2 | The scalar comparison retains the actual arithmetic/character input. |
| QP25 | Its graph predecessor QP22 supplies `PairEx`; the separately assumed `VWinAt` is not thereby supplied. |
| MR22 | Zero theta maps and an empty toric family are the stated initialization. They do not supply the later nonplaceholder theta/local family. |
| DC21 | The Core join is conditional on its exact other fields. Closing one of its fields does not construct the other fields. |

These are limitations of how the historical annotations encode premises. They are not contradictions in the mathematical implications and are not findings about Lean's kernel. Historical graph edges and claim records should be preserved; the new obligation map supplies a separate layer for current semantic status.

`historical_graph_audit.json` records the calculation and illustrative source records. It deliberately reports no completion percentage.

## The terminal chain is now explicit

For a fixed primitive target character ψ, first choose a finite constant Aψ and a positive allowed range for ε. For every sufficiently small positive ε, obtain arbitrarily late full real windows on which the same fixed positive character family satisfies

\[
H_\psi(x)\le x^{1/2+A_\psi\varepsilon}.
\]

The family of characters and Aψ must be fixed before ε and the moving window. A different host may be used at each x, but primitive character reading must identify every such host with that original fixed target family.

WB1–WB8 now prove all character and scalar steps from their explicit contract: ramified as well as unramified primitive reading, exact character balance, moving-cutoff bounds, subgroup averaging with coefficient bd₂/2, fixed quotient-family errors, and identification of the positive target ramp. The retained hypothesis is the actual arithmetic gain inequality and the common data satisfying the listed size and compatibility conditions. The passage from these windows to the zero-free half-plane is AN2–AN3; GH6 handles the full Dirichlet conclusion, including imprimitive Euler factors and the principal pole. Ordinary RH is the trivial-target specialization.

The pinned source takes eD=2 and eL=0 in its `shapeWin` application, giving the literal terminal coefficient eD+eL+7=9 if that whole application is supplied. The readable argument only needs some finite coefficient fixed before ε. A numerical simplification is useful only if it preserves that dependence order.

## The two cohomological routes form an OR, not a growing checklist

The coarse sufficient boundary for VW is

\[
\operatorname{JointWin}(C_t)\ \text{and}\ \operatorname{ThmBc}(C_t).
\]

An upstream sufficient route is

\[
\operatorname{ThmBab}(K,C_t),\quad \operatorname{PointHV},\quad
\operatorname{ThmBcFree},\qquad C_t\ge1.
\]

VW4 proves that the second route supplies the first with the exact finite prime set, cyclotomic reference layers, field models, local data, host conductor and dependence order. One need not independently supply both routes. The retained `ThmBab` contains simultaneous two-primary and reference-layer control, not merely an isolated two-primary estimate. `PointHV` contains the actual odd-plus counting/vanishing assertion; `ThmBcFree` contains the actual odd-minus assertion.

VW1 assembles odd plus/minus and two-primary pieces on the original cohomology, including the sign of the negative Tate twist. VW2 keeps the original host field, proves the CM and exact conductor identifications, and checks the scale restrictions. VW3 absorbs every coefficient uniformly on the same window to obtain literal `VWinAt`. VW4 then combines it with QP22, fixing q,d and the window before the continuum of scale parameters. Only the page/tower exponent varies. The final page-cutoff rescaling is checked explicitly.

QP22 is already a complete human implication from the named quadratic class-number formula CN and the precise density inputs BD and HD. These remain citation leaves. The cohomological leaves above are substantial project-specific suppliers. A matrix estimate such as OH8, field degree alone, or an unquantified statement that cohomology vanishes cannot replace them.

## The exact same-family bottleneck

The source's target predicate `GChi ψ` asks for both `EAtH(Level.cyc ψ,H,TT,x,ε,4)` and `VVle(E,t,√b)` on one host. Its family class also includes windows. `HostExW` further supplies the actual ranks and `HostGood` package on a scale family. Abstractly constructing a suitable number field, or proving the existence of q,d, supplies only part of this record.

The central source assembly `topDesWin` has a finite conjunction of closed conditions on the same design class:

| Obligation | Actual content that must remain attached to the family |
|---|---|
| `DesignExists` | For every threshold, one compatible family with `ChosenE`, `TuSize`, and `DGamSize`. |
| `LinkN` | Congruence-denominator cost bounded by the actual cohomological sum and polynomial budget. |
| `LinkEta` | Coverage of the original twisted local data. |
| `LinkIRR` | Nonnegative retained-row defect and the stated small upper bound. |
| `SmallLevelRankEq` | The actual dZ,0(j)=D0 equality for every used lift. |
| `LinkDIVt` | The same period target, integral and height data, yielding `LinkDIV` from `LinkEta` and `DIVinN`. |
| Fullness/rank | `ChosenE` yields the original lattice fullness and positive retained ranks. |
| `LinkG` | Actual local gain/divisibility with its served-orbit and lattice data. |
| `LinkS` | Actual normalized Gram, diagonal-error and dimension bounds. |
| `LinkGLOBAL` | The same-family slope comparison gives `ChainTied`. |

DA1 proves the quantifier join, not these suppliers. A `Closed` statement gives a threshold for every sufficiently small ε, then holds for every family above that threshold. Take the minimum of finitely many ε ranges and the supremum of their thresholds **before** using `DesignExists` to choose one family. This is why the source can join finitely many conditions without combining unrelated witnesses.

DA2 proves the subsequent logical chain. `VVle` gives summability and V≤√b≤b. The literal `NData.sha_eq` identifies these lengths with the stored lengths. `LinkN` and `SmallLevelRankEq` then give

\[
\eta_j\le D_0\{C(fmb\,y^2+\log^2x\,N_c)+V\}
\le D_0(|C|+1)y(B_0+N_c),
\quad y=x^\varepsilon,\quad B_0=fmb\,y,
\]

once log²x≤y and y≥1. Every eventual statement used here already holds uniformly in the family indices; a finite maximum of thresholds preserves that uniformity. No finiteness of the full index set is assumed.

This produces `DIVinN`; `LinkDIVt` then supplies `LinkDIV`. The separate actual lattice/metric comparison `NprimeMuR`, fullness, positive rank, and the two size bounds supply `LinkMu`. The five global links feed `LinkGLOBAL` and produce `FamilyClassConnected`, with eD,eL fixed before ε. The short wrapper `linkMu_of_linkDIV` is not a proof of the underlying metric identity from rank equalities alone.

## What remains after the new chains

The map groups the open work into four interacting branches. They are not four single lemmas of comparable difficulty.

1. **Actual cohomological windows:** the `ThmBab`, `PointHV`, and odd-minus suppliers, or a complete alternative satisfying the coarse boundary. The final assembly and all same-pair numerical bookkeeping are now closed.
2. **The actual geometric/arithmetic family:** Core, layouts, coefficient embeddings, `St`/`ColPin`/`R3.Read`, `NChoice`/`TupTied`/`ChoiceSide`, actual rational good-row data, and genuine theta/local realization. HP closes the representation-theoretic polynomial theorem inside this branch, not its geometric realization.
3. **The global theta/operators and normalized estimates:** toric ratios and `Choice.FieldOK`, convergence, separation, nonvanishing, tower and unfolding identities, chain norms, spectral words, normalized positive kernels and masses, and exceptional terms. Finite Weil formulas alone do not supply identities for the actual global operators.
4. **Integral, metric and congruence comparison:** original lattices, discarded directions, retained ranks, height and denominator costs, especially full `LinkN`. All of these must use the same maps and fields as the other branches.

There is a useful OR gate in the real-stage branch: the restricted actual large-gap route DC20, with its exact ties and named Harish–Chandra/Tamagawa inputs, is enough for the rows in its range. A universal `DiscreteSeriesExist`/`FormalDegreeFormula2` reconstruction is an alternative. It is not an additional requirement when every used row is already covered by DC20. Neither route supplies the other fields of Core.

The audit found no mathematical circularity in the reviewed implications. It does identify potential circular *closure accounting*: treating a downstream conditional theorem as the supplier of its own assumed window, treating a field record as its cohomological bound, treating a zero/empty initialization as genuine theta data, or counting rank agreement as the actual metric transport. The map prohibits these inferences explicitly.

## Recommended next closures

Only two targets are recommended as the next complete-chain milestones.

**1. Close one full cohomological supplier route into VW4.** The most concrete upstream route is `thmBab_of_lemmaK`, `pointHV_of_counts`, and `thmBcFree_of`. The first retains Poitou–Tate, local finiteness/duality, Ferrero–Washington and the project-specific `LemmaK`; the second additionally retains CountI/II/III/V/Z; the third retains the exact `PsiBound`. Classical duality statements may become precise citation leaves after their hypotheses match. Counts, layers, eigenspaces and `PsiBound` must be reconstructed or supplied by explicit established theorems. This milestone would yield actual `VWinAt` and fixed-pair windows rather than another conditional window wrapper.

**2. Close full `LinkN` on a single actual family, including the transport back to its original rows.** The source's direct family route `linkN_of_twGood_galoisPreconditions` requires `Hypotheses₂`, `CutGivesAlt`, `TwGood`, and rowwise `GaloisPreconditions`/`Tie4`. Its `linkN_of_gd` step transports the cut family back with explicit multiplicity and rank control. The alternate `linkN_of` interface requires actual `AdmF` and `KudlaFamilyStatement`; renaming these premises is not a closure. A completed supplier here would join directly to DA2 once the same host has its VW budget.

These are chosen because they end at already written downstream chains. They are work packages, not promises that the next iteration can discharge every leaf. Exact paths, declarations, source hashes and retained premises are recorded in `next_targets.json`.

## Reproduction and review

Run `python dependency_audit_v0_23/build_audit.py --repo PATH_TO_PINNED_SOURCE` from the archive root. The script computes the historical graph diagnostics, checks the finite obligation-map references and acyclicity, and extracts the recorded source ranges. It does not execute Lean.

The new TeX contains DA1 and DA2 with complete proofs and explicitly retained inputs. Independent review of VW1–VW4 and WB1–WB8 passed against their frozen final text hashes. Root review of DA1/DA2 required a clarification that finitely many uniform statements, not finitely many family indices, are being combined; that clarification is incorporated. Source and graph integrity checks support traceability. They do not silently discharge any remaining mathematical supplier.
