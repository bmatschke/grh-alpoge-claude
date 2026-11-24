# The small-prime denominator field and the middle-range estimate

Edition 0.82 · 25 November 2026

The small-prime denominator estimate now holds at every prime dividing the small conductor $Q_S$ and also at 3. This includes 2. It gives the fourteenth of the fifteen fields required on the **same** family data. Of the remaining field, called `mid`, the estimate holds at every eligible split prime, every eligible inert prime classified as row B with the common row constant chosen below, and on the inert C and D ranges described here. The human-readable reconstruction of RH and unrestricted Dirichlet GRH has ten shared open obligations. [New proofs (PDF)](RH_new_proofs_v0_82.pdf) · [Cumulative manuscript source](RH_readable_reconstruction_v0_82.tex) · [Previous edition](RH_reconstruction_progress_v0_81.md)

## One estimate at all the small primes

Write $s=\max(1,v_p(Q_S))$, $y=h_B=b+S_c+\eta+t+2$, $\Lambda=s+\log_p(2y)+1$, and $n_V=r+t$. For a sufficiently late family member, each twisted localization $i$ at one of these primes and every good point $\pi$ there, the normalized congruence valuation satisfies

$$
 v_{\mathrm{cc}}(i,\pi)\ \le\
 s_\pi+\sum_{1\le j<t}u_j+v_p(h_E)+p^{-2}
       +6000 fmys+30000 f^2t^2n_V\Lambda .
$$

Here $s_\pi$ is the normalized Selmer length, $u_j$ is the cyclotomic length of twist $j$, and $h_E$ is the class number. The last two terms fit the original family allowance $C fmb\log x+C x^C(\log b)^2$. One chooses the common constant and cutoff before choosing the member. The auxiliary table can then put the allowance in its single non-place entry and take every place entry to be zero. This supplies the existential table of $\mathrm{StarF}$ on the representation already used for the other thirteen fields. The hypotheses are $\mathrm{Hypotheses}_2$, $\mathrm{TwGood}$, $\mathrm{FactsF}$ with its nonnegative constant, the original scale conditions, and the member's $\mathrm{TwistedPlaces.ShaFinOdd}$ premise. In the pinned definition that premise covers all primes for every $0<j<t$. [Small-prime calculation and family assembly, G82F1–G82F4](continuation_v82/smallglobal.tex) · [Original valuation, table and family conditions](https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AbelianVarietyTheory/Definitions/NonGaloisDescent/BoundAtTwoThreeFamily.lean)

Two integral arguments account for the prime 2. The local lifting estimate works over a cyclotomic field of every admitted level and descends by corestriction with the valuation of the actual extension degree. The character estimate uses inverse Frobenius on an integral Witt-vector equation. This moves the denominator to the second cyclotomic level, where its controlling degree is $p(p-1)$, at least two even at $p=2$. The resulting primitive converges. The additional term has trace zero on the next cyclotomic layer and can be removed. Computing the lattice of logarithmic coefficients then gives the original uniform character exponent. The host supplies $4\mid Q_S$, as needed for the dyadic generator and its valuation formula. [Cyclotomic lifting, L82K1–L82K5](continuation_v82/smalllift.tex) · [Integral character proof, T82K1–T82K6](continuation_v82/smallchar.tex)

## Why the split middle range closes

The obstacle in 0.81 was simultaneous localization. Local bounds at each column already held, but separate lifts need not come from a single global map. At a good point the rank and first-character evaluation maps now lift bases of the local finite cocycle spaces integrally. The proof adjoins generators for all the columns to one Hecke module and imposes their local equations on one homomorphism. Its determinant controls the evaluation ideal at the original point. Passing from integral cocycles to cohomology costs the valuations of the character-root differences, including when two roots agree in the residue field. The sum of the column costs and the costs on their conjugate rows fits the prescribed allowance on the selected family data. This proves $\mathrm{StarAD}$ throughout the split branch with its original guards. [Local evaluations, F82L1–F82L4](continuation_v82/fiber.tex) · [Simultaneous determinant, G82C1–G82C5](continuation_v82/column.tex)

## Why the inert row B closes

At an inert prime, Frobenius permutes the embeddings of the unramified completion $E_w$. Reading the Hodge weights in that cyclic order gives a word. A thick position is an embedding whose large weights reach the host's thick range. The formal row B condition forces the thick positions into clusters of at most two, separated by strings of thin positions. This holds for the tested representation and its good points. It permits a proof for one short arc at a time. [Frobenius order and word conditions, I82W1–I82W5](continuation_v82/inert.tex)

| Step | What is proved on the tested map |
| --- | --- |
| Split the target class into arcs | At each cut the source Wach lattice contains a preimage of the prescribed multiple of every target vector. Applying the same calculation to a crystalline extension and propagating its generators through the thin letters decomposes the target class, multiplied by $p^{R+2\sigma}$, into integral arc classes. [Cut exponent, R82W1–R82W4](continuation_v82/cutlift.tex) · [Class decomposition, I82B4–I82B5](continuation_v82/inertrow.tex) |
| Identify the integral and crystalline coordinates | Both the period frame and its inverse have integral representatives through the required Taylor orders after multiplication by $p^\sigma$. Testing all primitive roots detects membership in the actual Wach lattice. The true and rounded filtrations differ by at most $g$ grades. [Frame comparison, J82F1–J82F3](continuation_v82/frame.tex) · [Integral membership, D82P1–D82P3](continuation_v82/physical.tex) |
| Lift the constants in each sign order | The integral numerators have five normal forms, according to the order of up and down positions. In the down-before-up case the second constant must lift inside a filtered sublattice. A weighted valuation at the two different cyclotomic levels and a Smith-coordinate calculation give precisely $p^{2a_0}U_{2,u}\subseteq f_0(U_{1,u})$. [Normal forms, A82N1–A82N5](continuation_v82/arcforms.tex) · [Filtered lift, P82U1–P82U3](continuation_v82/filterarc.tex) |
| Lift the physical vector and return to finite cohomology | Two integral polynomials remove the finite sets of Taylor degrees where the target and source tests can fail. Their values at 1 have combined valuation at most $2\kappa$. Correcting the lifted numerator in the original Wach lattice gives the required cut-vector congruence. The source arc cocycles are crystalline-finite. Summing their lifts recovers the prescribed multiple of the original class. [Polynomial action, K82P1–K82P4](continuation_v82/killers.tex) · [Physical lift, B82R1–B82R3](continuation_v82/rowb.tex) · [Passage to cohomology, H82A1–H82A3](continuation_v82/arcclass.tex) |

The total exponent is $e_{\rm par}=2R+4\sigma+2a_0+2\kappa$. A target finite cohomology module over a completion of degree $d$ has at most $(d+1)r$ generators, including the integral torsion. Together with the explicit bound on $e_{\rm par}$, this proves the stored row length. The package chooses the free row constant $C_2\ge122$ before constructing the common family data. Earlier estimates then apply on that same choice. At each inert index the global determinant uses only rows, so their bounds yield the required inequality at every good point. [Exponent and rounding, I82B1–I82B3](continuation_v82/inertrow.tex) · [Global comparison, G82I1–G82I2](continuation_v82/inertglobal.tex) · [Original cohomological assembly](https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Formalism/DistinguishedUnitIdeals/StatementE.lean#L118-L148)

## Where to resume

The missing part of $\mathrm{mid}$ is at eligible inert indices outside row B, in the source's rows C and D. Every orbit without thick letters is covered. An orbit with thick letters is also covered whenever $25h_B/p+3\le2082F_w$, where $F_w$ is the source's flat allowance at the place, including its band term. In particular **all** places are covered for $h_B\le83p(S_c+\mathrm{large}_2)$. [Local C/D bounds, N82I1–N82I2](continuation_v82/thin.tex)

On a mixed orbit no three consecutive positions are thick. Cutting just before each nonthick position gives arcs of length at most three. If $g$ bounds the weights at the nonthick positions and the widths of the marked windows as in M82R1, the same local lifting argument at one thin step gives the exponent $32h/(p-1)^2+366g+14\log_p h$. A sufficient condition for this to fit the C/D row is $p^2g\le(8/9)h_B$. For each fixed exponent $A$, every mixed orbit with $p\le x^A$ meets this condition beyond a family cutoff depending on $A$. The source bounds the entire small-order row D by $p<x^6$. Consequently the full global inequality holds throughout row D whenever Frobenius differs from complex conjugation. The chapter also gives the full three-term test, available on every shape of word. [Mixed-word bound and comparison, M82R1–M82R3](continuation_v82/mixedrange.tex)

If even one orbit is all thick, Frobenius equals complex conjugation. Every completion then has degree two, and precisely $\#T_2$ of the $2n$ places are all thick. Pooling the available row lengths proves the global inequality, for example, whenever $\delta h_B\le162pF_{\min}$, where $\delta=\#T_2/n$ and $F_{\min}=(w_P+\eta_3)/p+S_c+\mathrm{large}_2$. The full inequality in the chapter is stronger. It also explains why the leading multiplicity term alone cannot pay the coarse thick-place bound uniformly on the original family. [All-thick places and the global sum, C82S1–C82S2](continuation_v82/ccsum.tex)

For the remaining places one can prove the sharp local length bound, or prove the weaker sufficient sum directly. If $b_w$ is the recorded row length, $B_w$ a valid upper bound on the normalized length of the tested cokernel, and $m_p$ the number of places above $p$, it suffices to show

$$
 \sum_{w\mid p} B_w\ \le\
 \sum_{w\mid p} b_w+t c_Bm_p+(2n_V+2)v_\delta(i).
$$

The known local bounds can contribute savings to this sum. In the local approach the unhandled words have either a mixture of thick and nonthick positions, or only thick positions with alternating signs. The source treats them by different estimates. Both must fit the *same* row table; the full pointwise hypothesis is sufficient but stronger than the displayed sum. [Available global allowance, G82I2](continuation_v82/inertglobal.tex) · [Original C/D row statement and case split](https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AbelianVarietyTheory/Proofs/InertiaEigenvalues/RowsCDRowConditionLocalBounds.lean#L62-L83) · [Mixed-word estimate](https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AbelianVarietyTheory/Proofs/InertiaEigenvalues/RowBoundsOfNonThickLetter.lean) · [All-thick estimate](https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AbelianVarietyTheory/Proofs/InertiaEigenvalues/RowBoundsOfAllLettersThick.lean)

Even after completing the fifteenth family field, the whole global denominator contract requires the specified family construction and the bound on its actual $\eta$-sum. The other nine shared obligations concern the common geometric and arithmetic data, theta readings and rational tests, base rows, period height, retained defect, spectral control, and compatible second-layer selection. Their complete hypotheses and quantifiers are preserved in the ledger. [Original open contracts](continuation_v82/obligations.json) · [Current checkpoint](CURRENT_CHECKPOINT_v0_82.json)

## Verification

This edition adds 71 proof blocks, giving 4,614 in the manuscript. The source concordance checks 469 ranges in 192 files against Git objects of the pinned Lean revision. The verifier checks the manuscript blocks, dependency paths, open contracts and supplement digest. The PDF validation checks that all the new headings appear in both readers. These are provenance and consistency checks for the human proofs. No new Lean build was run. [Claim ledger](continuation_v82/claims.json) · [Validation record](continuation_v82/validation.json)

~~~sh
python3 continuation_v82/verify.py --formal-git formal_source
pdflatex RH_new_proofs_v0_82.tex
pdflatex RH_new_proofs_v0_82.tex
~~~
