# Version 0.25: the actual K-theory bridge and LemmaK

This component closes the shared `LemmaK` chain through a constructed `KBridge`. Its main endpoint is **KB8: `LemmaK 31`**, after joining the independently reconstructed **TB10: `TorsBoundPow 22`**. All arithmetic data in that conclusion remain the original prime, number field, algebraic closure, and `LData` record.

The main proof is in `main.tex`. `provenance.json` records each KB claim's exact proof range and hash and the corresponding pinned Lean definitions or proofs. `classical_inputs.json` gives the precise accepted classical statements and explains how their hypotheses are met. `closure.json` records the dependency graph, original-object bindings, simplifications, and scope exclusions. The pinned source is commit `7cbf7a0c32fca1badf05931879a37c3f8a2b03b4` of the CocoSgt mirror. No Lean kernel replay was performed.

## Closed mathematical chain

| Claim | Content | Mathematical role |
|---|---|---|
| KB1 | Original Galois quotient, cyclotomic character, finite étale/Galois comparison, compact continuous-cochain inverse limit, and direct mod-ell injection | Identifies the actual target and prevents a cohomology-model mismatch |
| KB2 | Finite positive even Quillen K-group and compatible Dwyer–Friedlander maps onto the actual integral H² | Constructs the finite source and its surjection, including degree two and prime two |
| KB3 | Dedekind stable range by CRT, integral finite-rank stabilization, and Arlettaz kernel control after flat base change | Constructs the homology map with the exact allowed prime-power kernel exponent |
| KB4 | Actual finite module and both maps satisfying every field of `KBridge` | Supplies the interface rather than retaining it as a premise |
| KB5 | Finite-module quotient bound and finite submodule bound in Z_ell tensor H | Gives the cardinality mechanism without assuming finite generation of homology |
| KB6 | Finite Poitou–Tate, native local-field matching, strict local kernels and class-group characters | Proves the original mod-ell quotient bound by classNumber times ell to the degree |
| KB7 | Minkowski and ideal counting, prime/degree bound, and exact logarithmic reduction | Matches the source inequality at homology rank 4e+4 and degree 2e |
| KB8 | Explicit constant absorption and TB10 join | Proves `LemmaK 31`, uniformly before all arithmetic choices |

Writing `n=[L:Q]`, `Delta=|disc L|`, and

```
X = H²_cts(G_{L,S}, Z_ell(e+1)),
T = tors H_{2e}(GL_{4e+4}(O_L), Z),
```

the complete numerical join is

```
|X/ell X| <= h_L ell^n,
|X| <= |X/ell X|^{cOne(2e)} |T|,
log |X| <= 4 n log(2 Delta) (2e)(2e+3) log(n+1) + log |T|,
TB10 => log |T| <= exp((2en)^22 log(2 Delta)),
log |X| <= exp((2en)^31 log(2 Delta)).
```

The proof constructs finite `X` before taking its logarithm. Group orders in these calculations are positive. The bound holds for every original `D`, not only for a convenient representative.

## What the KBridge construction actually uses

Take the canonical Quillen group `A=K_{2e}(O_L)` and its ell-primary completion `K=Z_ell tensor A`. Quillen finite generation and Borel's rank-zero result for positive even indices make this a finite group. The arithmetic surjection comes from Dwyer–Friedlander's finite-coefficient comparison followed by explicit inverse limits. The homology map is the canonical integral Hurewicz map followed by the inverse of the actual stable block-inclusion isomorphism at rank `4e+4`.

This existential construction avoids proving a more general statement about every record satisfying the source definition of a `Plus` model. At the pinned revision, the two `KBridgeOfKPublished` files specify interface structures. Their filenames are not used as evidence of a construction theorem; KB4 supplies the construction directly in human mathematics.

Arlettaz's Corollary 7.19(a) has the required **GL-infinity target**, rather than only an elementary subgroup target. Each factor in its annihilating integer is squarefree, so `v_ell(R_m)<=m-1<=cOne(m)`. Flatness of Z_ell carries the kernel bound through tensoring. This retains every prime, including the small primes. Van der Kallen's integral homology theorem already stabilizes at rank `2m+1` for this stable range; the actual source rank `2m+4` is within that range.

## Degree two, prime two, and inverse limits

The Dwyer–Friedlander input is recorded in finite coefficients: Proposition 8.1 removes the primes above ell, Theorem 8.5 supplies surjectivity, and Proposition 8.2 directly covers degree two. At ell=2 the source's primitive fourth root satisfies the needed hypothesis, and levels `r>=2` form a cofinal system. The proof does not rely on an uncertain OCR reading of the inequality in completed Theorem 8.7.

The finite-coefficient spectral sequence has only the relevant H² and H⁰ terms in positive even degree. The inverse limit of the positive-twist H⁰ term is zero because the cyclotomic image is infinite. The algebraic coefficient exact sequence has transition multiplication by ell on its torsion term; finite generation makes that inverse limit zero. Finiteness of each remaining level ensures the required Mittag–Leffler and compactness arguments.

For the target cohomology, the chapter explicitly identifies compact continuous cochains with the inverse limit of finite cochains and kills the derived limit using finite H¹. For the generator bound, a shorter argument suffices: the cochain exact sequence for multiplication by ell gives an injection `H²(Z_ell(j))/ell -> H²(F_ell(j))`. This avoids importing a separate integral H³ vanishing theorem or proving an unnecessary equality.

## Exact local comparison

LK1–LK3 are formulated on finite intermediate fields of the specified `PadicAlgCl`. KB6 now explicitly joins them to every original global decomposition group. It keeps the chosen valuation subring `D.A_v`, takes its selected henselization and completion `L_v`, embeds that finite extension of Q_ell into `PadicAlgCl`, and transports the absolute Galois group through the henselian finite-extension equivalence. This is a continuous group isomorphism in both directions. It preserves the action on all roots of unity and hence the exact cyclotomic character. Precomposition transports cochains, cup products, and the original local restriction map. The matching source transport theorems are included among the provenance anchors.

After this comparison, finite local duality bounds each local H² order by ell. Finite Poitou–Tate identifies the global strict H² kernel with the dual of the strict H¹ kernel for the inverse-and-twist dual coefficient. `HasMuQ` makes that residual coefficient trivial. Its strict H¹ classes are unramified class-group characters, so their number is at most `h_L`. There are at most `n` places above ell. No enlargement of the original field or change of local data occurs.

## Input boundary and noncircularity

The accepted classical leaves are stated individually in `classical_inputs.json`: Quillen, Borel, Dwyer–Friedlander, finite étale/Galois comparison, van der Kallen, Arlettaz, unramified global class field theory, Minkowski's bound, and the henselization/completion comparison. The human suppliers are **LD3**, **LK1–LK3**, and **TB10**. There is no remaining bespoke KBridge or LemmaK premise within this branch.

The finite-level cohomology inputs precede integral finiteness. Integral H² finiteness follows from the finite K-group surjection; it is not assumed to justify a limit. The Hurewicz bound and stability are independent of the torsion estimate. TB10 enters only at the final quantitative join. No `ThmBab`, tower bound, window bound, `LinkV`, or RH/GRH conclusion feeds back into these arguments.

The generic final constant is `max(C,0)+9`, for any supplier `TorsBoundPow C`. Thus TB10's value 22 gives the explicit value 31. It is fixed before ell, L, Omega, D, and e, exactly as required by `LemmaK`.

## Validation and scope

Run `python build_provenance.py --repo /path/to/pinned/lean-source` to regenerate the source/proof ledger and verify every cited source file against the pinned Git blob. `validate_tex.py` performs an offline draft-mode syntax check using the cumulative preamble and produces no PDF. Its results are in `tex_validation.json`; they are not mathematical verification or a visual layout certification.

This completes the shared LemmaK branch relative to the explicitly accepted classical theorems and the joined human TB/LK/LD components. It does not assert a full human-readable reconstruction of RH/GRH, prove the classical foundational theorems from first principles, or certify every arbitrary-model `KPublished` field.
