# v0.27: the actual symplectic Model constructor

## Result

MX1–MX10 reconstruct every field of the literal source `Model D`. The intrinsic endpoint is the exact implication

\[
\operatorname{Good}(D)\land\operatorname{PhiCond}(D.\mathrm{Gam})
\land D.\mathrm{Nums}\land\operatorname{Nonempty}(\mathrm{LocBase}\,D)
\Longrightarrow\operatorname{Nonempty}(\mathrm{Model}\,D).
\]

The universal `LemmaP` premise is already supplied by FP8. The separate arithmetic suppliers DX2, DX4, and DX8 install the other three interfaces on the same original good datum, yielding the displayed MX10 consequence `Good D -> Nonempty (Model D)`. This component neither assumes nor promotes the whole `CohomologyHyp` package.

The construction preserves the original algebraic closure, coefficient DVR, all four diagonal characters, residual representation, decomposition and inertia groups, global quotient, and local restriction maps. It uses no auxiliary coefficient extension.

## Complete chain

| Claims | Completed mathematical work |
|---|---|
| MX1–MX2 | Exact global quotient descent and all five axioms of the kill-inertia local condition. The small-extension lifting axiom is proved using the actual finite residual adjoint module. |
| MX3 | The actual universal framed ring, origin, centered-entry variables, and exact relation multiplicities from the literal framed `Nums` equality. |
| MX4–MX5 | Complete relative cover, graded/complete finite-jet comparison, homogeneous formal cuts, an actual domain quotient, and preservation of every integral point derivation killing the cuts. |
| MX6–MX7 | The six root cuts with their exact signs, independent tangent directions, normalization, all three equation lists, exact dimensions, and actual local-component witnesses on the same domain. |
| MX8 | Literal `Lift.Generates`, for every complete Noetherian local target. |
| MX9 | Literal `Model.der`, including both entry formulas for every preimage and all nonzero moduli. |
| MX10 | Assembly of every record field and the exact arithmetic installation. |

## Main simplifications and why they preserve the endpoint

The local kill-inertia condition has finite residual inertia of order prime to the coefficient prime. Averaging over that finite subgroup reduces its second cohomology to that of the procyclic unramified quotient. An explicit cyclic-inflation calculation kills every finite continuous class. The resulting correction of a matrix-lifting defect proves the full local lifting axiom, including continuity over complete rings that need not be Artinian.

The given local base already has an augmentation whose tuple is the original diagonal representation. Mapping its equations by this augmentation proves the base-point local equations. No additional local existence assertion is necessary at this step.

The source smooth-point notion is a rational cotangent chart. The proof does not replace it by integral formal smoothness. Finite Taylor jets compare the completed ring with its finite-sum homogeneous subalgebra. After independent homogeneous equations are cut out over the fraction field, the kernel of the resulting chart gives an actual domain quotient. A point derivation with values in the integral DVR annihilates that kernel because its cotangent class is torsion and the DVR is a domain. This proves the integral descent required later, without claiming integral regularity of the local deformation problem.

Two universal properties prove generation: equality of final representations first identifies the local-base maps, then identifies the framed maps, and finally identifies the quotient maps. The proof therefore establishes the source's exact uniqueness predicate directly.

For the cocycle derivation, each local coboundary parameter is lifted to the integral ring without dividing by a character difference. A torus-character separation argument proves the full homogeneous weight assertion on the local base. The final quotient is handled modulo the chosen modulus, with an explicit proof that the formulas are independent of every possible entry preimage.

## Exact inputs

The direct previously reconstructed inputs are FP1, FP4, FP8, and the original-place comparison in KB6. AX6 supplies the full literal `facts` consequences of `Good`, including original continuity, residual openness, unramified behavior, and residual separation at `ph`.

The intrinsic constructor retains `PhiCond D.Gam`, `D.Nums`, and the actual `LocBase D` as explicit theorem hypotheses. The final installed consequence cites only the separate exact suppliers DX2, DX4, and DX8. Their arithmetic proofs belong to the DX component and must be reviewed there. In particular, an input named `LocBase` is required to have the actual universal property over all `IsCO` targets, the original equations and groups, and the literal source chart dimensions.

New classical leaves are limited to finite unramified local Galois theory, the finite Hochschild–Serre cochain filtration, and basic complete Noetherian algebra. `classical_inputs.json` gives precise primary statements, URLs, and the matching conditions. The continuous-cochain passage, cyclic vanishing, formal implicit substitution, finite-jet comparison, and domain/derivation arguments are proved in the chapter.

## Audit and validation

`provenance.json` binds 166 claim-source links across 29 exact pinned Lean files and all ten human proof ranges. The source files are checked byte-for-byte against commit `7cbf7a0c32fca1badf05931879a37c3f8a2b03b4`. The ledger includes a complete `Model` field-to-proof mapping and separates stable claim dependencies from named classical inputs and theorem hypotheses.

Two draft-mode TeX passes succeeded, with no undefined references, missing characters, or overfull boxes. No PDF was produced. This is a syntax/reference check; independent proof reviews are recorded separately by the integration process. No Lean kernel replay is performed or claimed.

## Scope after this closure

The internal `Fr`, `Cover`, smooth quotient, normalization, generation, and cocycle-derivation chain is complete. The first-weight-zero algebra and point/orbit/trace comparison are supplied by the separate PX reconstruction. Model existence alone does not establish image density, automorphy, rigidity, the finite trace catalogue, an unconditional count, or the full RH/Dirichlet-GRH reconstruction.

## Files

- `main.tex`: complete readable proof, MX1–MX10.
- `provenance.json`: exact source and human proof hashes, dependency graph, and field coverage.
- `closure.json`: exact endpoints, original-object bindings, simplifications, and nonclaims.
- `input_registry.json`: exact arithmetic theorem hypotheses and human suppliers.
- `classical_inputs.json`: matched classical leaves.
- `source_locators.txt`: review-friendly pinned declaration links and hashes.
- `build_provenance.py`: reproducible source binding generator.
- `validate_tex.py` and `tex_validation.json`: reproducible draft-only TeX validation.

