# Independent review of the dependency join and audit scope

**Result: PASS.**

Reviewed `dependency_audit_v0_23/main.tex` at SHA-256
`a6270d8d26f72556adac64b800c74b94f7541cfd09975fbc44ac1136aab6ed85` against the pinned Lean source commit
`7cbf7a0c32fca1badf05931879a37c3f8a2b03b4`.
Reviewer: `/root/core_closure`, independent of the audit author.

The scope is the mathematics of DA1–DA2, the literal source interfaces at
`DesWin` and `DivinNOfHypV`, and the audit's distinction between closed
implications and retained suppliers. This is not a Lean replay or an
exhaustive extraction of the source graph.

## DA1: choices occur in the required order

The stated definition of `Closed` matches the source: a positive epsilon
range is fixed first; for each epsilon in it, the threshold is chosen
before the family and its height parameter. `TransportedAlt.sup` takes
pointwise maxima, and `FamP.large_sup` is an equivalence. Thus the same
joined threshold works even though later threshold components depend on
lists of parameters selected earlier.

`DesignExists` accepts every such threshold before supplying the actual
family and height parameter. Intersecting the finitely many epsilon
ranges, joining the thresholds, and then selecting the family is valid.
The stated class-inclusion transport is essential and is present. The
empty finite conjunction is harmless. No independent family witnesses
are being combined.

## DA2: the cohomological budget is converted correctly

The nine closed conditions are exactly those used by `topDesWin`.
Conditions depending on `TuSize`, `DGamSize`, and `ChosenE` retain those
antecedents on the selected family. The final constants eD and eL are
fixed before epsilon, whereas the remaining constants and eventual
threshold may depend on the selected family. This is precisely the
quantifier order in `FamilyClassConnected`.

For the scalar subchain, `VVle` can be instantiated at the actual
algebraic closure and local-data system stored in D. Its finiteness
clause and `NData.sha_eq` identify the stored lengths with finite natural
cohomological lengths. The nonnegative prime-weighted summands have
uniformly bounded finite subsums. Consequently their series converges
and its sum V satisfies 0 <= V <= sqrt(b) <= b. `ShaFinOdd` holds on the
same D, so the conditional `LinkN_at` inequality is applicable.

The remaining estimate is correct with no sign hypothesis on C. At late
scales let y = x^epsilon >= 1, B0 = f m b y, and Nc >= 0. For an actual
used lift, its interval membership supplies m >= 1; the frame gives
f >= 1. Thus b <= B0. Once log(x)^2 <= y,

- A = f m b y^2 + log(x)^2 Nc is nonnegative and at most y(B0 + Nc);
- C A <= |C| A <= |C| y(B0 + Nc);
- V <= b <= B0 <= y(B0 + Nc).

Multiplying the resulting bound by the nonnegative rank D0 gives
exactly `DIVinN_at` with constant |C| + 1. The family-level statement
uses one C and finitely many thresholds already uniform in every
moving index and used lift. Taking their maximum preserves uniformity;
no finite-index assumption is introduced.

## The metric premise remains a real premise

The source's `J.linkMu_of_linkDIV` extracts zero-above and finite
generation from the actual `LinkDIV` and fullness data, and joins these
with positive rank and the two size estimates. Its substantive comparison
then uses `nprimeMuR_at`, the family's actual `nprimeDef`, stored good
metrics, and size bounds. The audit explicitly retains this lattice and
metric transport. It does not claim that dimensions or an abstract
isometry on other spaces imply the needed slope identity.

With that retained premise, the assembly is complete: `LinkDIVt` gives
`LinkDIV`; the metric arrow gives `LinkMu`; the five stated conjuncts give
`GlobalTheoremInputs`; and `LinkGLOBAL` applied with `ChosenE` supplies
`ChainTied` on the same family's eventual windows. The wording 'one
family' is correctly understood for each permitted epsilon, as the
preceding definition and following proof make explicit.

## Audit scope

The same-host `EAtH` and `VVle` clauses of `GChi` are correctly retained,
as is the family's window condition. The document identifies the
representation leaf HP1–HP4 separately from the field/frame/row
identifications of HP5–HP6 and from full geometric `Core`. It distinguishes
the two newly completed conditional window interfaces from the open
arithmetic and cohomological suppliers. The real-stage alternative is
correctly stated as an OR gate only for the actual rows covered by that
route; it does not erase unrelated `Core` fields.

No completion percentage is inferred from claim counts, graph acyclicity,
or empty historical dependency arrays. Named classical leaves are
accepted only after exact statement matching. These are appropriate
limitations of this milestone.

No unresolved mathematical finding remains. The accompanying JSON lists
the exact source symbols checked and the hashes of DA1 and DA2.
