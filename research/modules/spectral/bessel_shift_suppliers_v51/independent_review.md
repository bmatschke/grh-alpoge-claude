# Independent review: bessel shift suppliers, version 0.51

**Verdict: PASS for BST1–BST11 at their stated original scope.**

Reviewer: `/root/geometry_alltest`, independent of the author.  
Accepted source pin: `7cbf7a0c32fca1badf05931879a37c3f8a2b03b4`.  
Reviewed proof: `bessel_shift_suppliers_v51/main.tex`.  
Reviewed whole-file SHA-256: `068e98c63dcb9f8049befda3611983af6a76d19cf90f3e76f5907b921bc10cc3`.

## Mathematical assessment

The proof supplies the full decay-under-derivatives statement, both complete tensor-map statements, the noncommutative complementary-minor expansions, the complete eigenspace statement and both tensor Casimir formulas. Its final join correctly retains the four exact period-evaluation and shifted-quotient suppliers. No unresolved mathematical defect was found.

The compact convolution argument uses the entire unique lowest-type isotypic subspace; one averaged kernel therefore reproduces all vector pairs. Differentiation transfers to compactly supported kernels by left-Haar invariance, and compact inverse-norm bounds preserve the exact decay exponent for every word. The subsequent L2 argument checks the source exponent inequality and actual square integrability.

The row–column minor proof is valid in a noncommutative complex algebra. It compares the two N-fold expansion sums and cancels the complete commutator sum; it does not commute individual factors. The replacement-index signs, shifts and N−1 multiplicities agree with the source identities. Both complementary contractions then give the exact source eigenvalues and Casimir shifts.

The final StepStatement reduction keeps the original representation, Bessel coefficient, conjugation, characters, Haar measures and period. It uses EvalP/M for the nonzero complementary periods and QuotP/M for the actual shifted spaces, their image relations and period injectivity. These are not inferred from an eigenvalue or Casimir calculation. The separate BSE packet was not used to change the conditional statement under review.

## Claim-by-claim findings

### BST1 — One compact smooth convolution fixing the entire lowest type

The compact conjugation average preserves left Haar measure because the modulus of a compact group is trivial. The averaged integrated operator commutes with K and maps j(T) into the entire unique T-isotypic subspace supplied by DC9–DC10. Schur gives one scalar, and strong continuity on the finite-dimensional unit sphere makes that scalar nonzero. Dividing the kernel therefore reproduces all lowest-type matrix coefficients simultaneously. The compact smooth ambient extension uses ordinary embedded-submanifold charts and retains arbitrary Haar normalization. No irreducibility of an arbitrary later datum is assumed.

Proof-block SHA-256: `c5d0875a3305777f050097ffa7dd4f4cf33dad683d67180d887ede8a56b9de2a`.

### BST2 — Whole original DecDerivStatement

The elementary inequality min(s^2,s/R) >= (s-1)/R, with R=sqrt(2q0), gives the exact exponent a=h/(8 sqrt(2q0)). Right differentiation in g is transferred by a left-Haar change of variables to -D_X on the compact kernel; the sign and side are correct. Iterating in the actual word order produces compact smooth kernels. The comparison rho(g) <= rho(gy) rho(y^{-1}) on each fixed compact support proves the unchanged exponent -a for every word, including the empty word. Complexified E_ab derivatives and local ambient extensions match the original DecDeriv scope.

Proof-block SHA-256: `1c0d2a002ce6a88e60a8283ce74c8208f745ca98ebacdbe23839d341d4878845`.

### BST3 — All generated-module coefficient words and free left translates

The generated stable submodule is the finite linear span of words in E applied to the lowest type. The original coefficient identity and the conjugate-first, linear-second inner-product convention identify right E_ab derivatives with E_ab applied to the second vector. Fixed left translation by arbitrary x0 commutes with right differentiation, and rho(g) <= rho(x0) rho(x0^{-1}g) changes only the constant. Thus every original generated-module vector has all the required coefficient derivatives; no new ambient irreducibility or complete-model identification is introduced.

Proof-block SHA-256: `45e0478e722d88e48e5719bb46e59f2df6052f1851e0784caee57eee21720689`.

### BST4 — Both literal tensor maps and exact first-derivative intertwining

Direct differentiation gives E_ab q_j = delta_jb q_a and E_ab r_j = -delta_ja r_b. These signs and index placements produce exactly the source standard and dual tuple actions. The product rule then proves the literal scalar intertwining maps for arbitrary original x1. In the dual formula the standard basis is real, so the stated transpose/conjugate convention agrees with the source. No Bessel-specific replacement of x1 is used.

Proof-block SHA-256: `d07d093650067f69f52f9f4535fd92268f7c66d04278edb7bacdbc970acf925d`.

### BST5 — Whole original TMapStatement and TMapDStatement

All tuple components remain in the generated module after every word. Standard and dual matrix coordinate factors are bounded by a constant times rho(g), with rho(g^{-1})=rho(g) in the actual unitary matrix group. The exact derivative exponent is therefore 1-a for every word. The original StepGap gives 2(a-1)>2nq0; BSP6 applies to the actual Haar measure and proves genuine square integrability of all derivatives. Smoothness supplies measurability, so both full IsSmoothL2 fields and all TMap/TMapD quantifiers are proved, not merely a formal L2-class assignment.

Proof-block SHA-256: `2a778c26727b65380094671cd2f4f8881bb12b8162f7e26861d9ba6514478ade`.

### BST6 — Shifted-minor alternation and exact commutator

The Grassmann calculations give the decreasing-shift column relation and increasing-shift row relation with the stated signs. Their top coefficients supply both alternating index laws and repeated-index vanishing over a complex algebra. The commutator formula follows from the ordered Leibniz rule; scalar correction terms cancel with the indicated shifts. These calculations use no commutation of the algebra-valued entries and remain valid for arbitrary lists and every associative unital complex algebra.

Proof-block SHA-256: `39b3761a6e05fc2ee830b1122956ee5e5fc0e2dff5a2b942a5ced13e72694b08`.

### BST7 — Equality of shifted row and column minors

Summing first-column expansions over every column gives N times the column minor; summing last-row expansions and applying the induction hypothesis gives N times the row minor. Their difference is the entire signed commutator double sum. For each selected pair, the replacement-row and replacement-column terms have exactly the displayed signs; in the full sum every T_sj occurs N-1 times in each direction. Cancellation is consequently valid without any individual-factor commutation. Division by N is legitimate over C for N>0, and the empty minor is treated separately. The first-row expansion has the exact x-p shift.

Proof-block SHA-256: `eae34291291e57bc9523df874218a7ca585a9e5e50d5bdf859e9829c813fda3e`.

### BST8 — Whole original CapelliExpandStatement

The complementary minors U and V have the correct deleted-row/deleted-column order and shifts x-1 and x. Expanding the list formed by the selected first column, or selected first row, makes every off-diagonal case vanish by alternation and gives the diagonal full minor with the stated sign. The order of multiplication is preserved. The empty complementary minor at m=0 is included. This proves the full original pair of Capelli expansion identities.

Proof-block SHA-256: `05d7e264c6c6f364b1fcd1bec0b571be23e52451a1b3620e7fc092b3429b5dd6`.

### BST9 — Whole original EigStatement

Stable-module membership of each complementary-minor vector follows by finite products and sums in S. Applying the two identities from BST8 at the common parameter omega gives eigenvalues -omega and omega-m with the exact source standard/dual contractions. The argument retains the independently arbitrary coefficient vectors, arbitrary stable complex module, and capfull(omega) annihilation hypothesis. It does not infer nonvanishing or add Hilbert-space assumptions.

Proof-block SHA-256: `9efba6046c132661745b387be340a835b6644cef4ee3861e952d3c472ff3d2a1`.

### BST10 — Whole CapelliTensorStatement and exact positive/negative Casimir shifts

The standard/dual index actions satisfy the required matrix-unit bracket and commute with the component E action. Expanding the tensor Casimir gives component Casimir plus n times identity plus twice the stated contraction, with the dual minus sign correctly included. Centrality propagates the original scalar Casimir from the lowest type to S. At omega=-theta_s the two scalar formulas equal exactly c(lambda+e_s) and c(lambda-e_s). The conclusion supplies tensor/Casimir data and does not claim a shifted quotient or a nonzero period.

Proof-block SHA-256: `842a0fa6b45a02be0ed0a7d306c711eb0ff70b46dde77ad7a0fb8ab338b65404`.

### BST11 — Exact conditional reduction of whole StepStatement to four suppliers

The join preserves the original Bessel witness, conjugating matrix P, characters, Haar measures, representation, and period functional. The displayed coefficient identity identifies the old nonzero Bessel integral with the exact original per on the original datum. EvalP and EvalM remain explicit hypotheses for the same complementary vectors and exclusions u_j != lambda_s +/- 1/2. QuotP and QuotM remain explicit hypotheses supplying the actual Wf and W-prime, image relation, shifted lowest type and Casimir, K stability, and period injectivity. BST5 applies to every element of those supplied images, and BSP10 then yields each shifted BesselNZ. Thus the whole original StepStatement follows only after all four retained suppliers are joined. No eigenvalue, nonzero vector, or Casimir coincidence is substituted for the quotient and period requirements; BesselNVGap and the setting retain their original supplied-Forms0 scope.

Proof-block SHA-256: `a41ddc28886282df2e1db49dfda6c10d44ee843b41507746368725a4a89b74b6`.

## Independent evidence checks

All 11 numbered proof blocks match their exact line ranges and SHA-256 digests. All 32 source snapshots, totaling 278,646 bytes, were compared byte for byte with the accepted pinned git blobs. All 38 distinct cited source ranges were hashed independently and match the provenance. The three inherited proof files also match their declared whole-file digests, and their used interfaces were checked at the stated scope. The JSON review records every proof-block and source-range hash.

These are human mathematical and source-binding checks. No Lean replay was performed, and no author proof or metadata was changed.

## Scope retained

The component alone retains the complete original EvalP, EvalM, QuotP and QuotM statements. It does not independently close StepStatement, BesselNVGap, ConcreteSettingExists, the original Forms0 supply, any selected whole obligation, RH or unrestricted Dirichlet GRH. The declared inherited and classical inputs remain exactly those of the packet.

**Unresolved findings: none.**
