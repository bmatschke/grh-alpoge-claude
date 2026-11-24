# The finite arithmetic supplier of PsiBound

## Outcome

The nine consolidated propositions OS1–OS9 reconstruct the complete finite arithmetic chain from Jacobi sums and finite reciprocity to the literal universal **UpperTheory.V.Odd.PsiBound** interface. The endpoint is OS9. The former bespoke special-value interface is now a proved output, relative to the explicitly identified classical arithmetic theorems and the LD finite-duality component.

The output retains the original abelian CM field \(E\), algebraic closure \(\Omega\), scalar towers, coefficient DVR \(O\), cyclotomic reading \(\rho\), and character \(\psi\). For every allowed odd prime \(p\nmid[E:\mathbb Q]\), every \(e\ge1\), and every supplied \(a\in O\) satisfying

\[
a=\operatorname{den}(N,e+1)B_{e+1,(\psi\circ\rho)_{\mathrm{prim}}},
\]

the proof gives

\[
\operatorname{psiLen}(\Omega,e,\psi)\le v_O(a).
\]

The exact coefficient character over \(\mathbb Q\) is \(\chi_p^{-e}\psi^{-1}\). The final eigenspace has character \(\psi\); OS9 explains the cancellation in the restriction action. The bound is on the original eigenspace, with the original local kernels, rather than a module selected only because its dimensions agree.

## Closed chain

| Stage | Proved content | Why it matters downstream |
|---|---|---|
| OS1 | Explicit Jacobi elements from finite-field power sums, ideal-class reduction, norm distribution and congruence at the new prime | Supplies actual arithmetic elements and both required identities |
| OS2 | Removal of roots-of-unity errors by the operator \(g_0-a\) and the power \(2N_0d\) | Makes both identities exact with exponents prime to \(p\) |
| OS3 | Kolyvagin derivatives, well-defined cocycles, weighted character averaging, the local transition formula, and initialization | Constructs the entire NuSys; it is not an assumed supplier |
| OS4 | Simultaneous Frobenius selection using a Kummer extension and an elementary three-subgroup argument | Proves compatibility of detection, cyclic-module generation, cyclotomic level, and admissibility at one prime |
| OS5 | The literal finite Rec consequence of LD2/LD4, commutator extension, and the local annihilator comparison | Converts the auxiliary inertia value into annihilation of Frobenius evaluation on a Selmer cocycle |
| OS6 | Length comparison and induction on the bounded valuation of auxiliary annihilators | Bounds the full module length without assuming finiteness in advance |
| OS7 | Finite Bernoulli expansion and exact valuation of the theta sum | Matches the source algebraic value and its actual denominator |
| OS8 | Normalized cocycle exhaustion and the residual cyclotomic exception | Covers every cohomology class and the branch excluded from the derivative construction |
| OS9 | Primitive-character reduction and tame global/local eigenspace descent | Supplies the original universal PsiBound interface |

The human dependency graph uses claim identifiers only:

- OS2 depends on OS1.
- OS3 depends on OS2.
- OS5 depends on LD2 and LD4.
- OS6 depends on OS3, OS4 and OS5.
- OS9 depends on OS6, OS7 and OS8.

OS1, OS4, OS7, and OS8 have their explicitly stated classical theorem inputs. These are recorded separately from reconstructed claim IDs. The graph is a human proof map, not a proof-term extraction from Lean.

## Substantive simplifications

The proof follows the source's finite route. It does not replace that route by an Iwasawa main theorem or by an unexpanded Euler-system theorem.

The Bernoulli congruence only needs a fixed integer that clears finitely many polynomial coefficients. OS7 proves this directly. The source's particular choice Stk.dk is therefore unnecessary at this intermediate step. The final source denominator den(N,k) is unchanged.

No analytic Bernoulli nonvanishing theorem is needed to prove PsiBound itself. If the supplied \(a\) is zero, the right side is the extended valuation \(\infty\), and the inequality is immediate. Otherwise the needed Bernoulli value is already nonzero. The subsequent quantitative odd-minus argument proves the additional integrality and nonvanishing required to obtain finite logarithmic bounds.

The residual cyclotomic branch is proved by the finite Kummer group of \(\mathbb Q\): a rational Kummer class unramified away from \(p\) and trivial at \(p\) has every rational prime valuation divisible by \(p\), hence is a \(p\)th power. The extension from residue-level vanishing to the whole torsion cohomology module is stated explicitly.

The length argument is a finite induction on \(v_O(p^m)-v_O(a_L)\). It establishes finiteness as part of its conclusion. It never cancels an infinite length, counts only a single element, or assumes a priori finite generation of the Selmer module.

## Classical inputs and exact remaining boundary

The following established finite theorems remain citation leaves:

- Finite cyclotomic theory, inertia/Frobenius descriptions, and local Hensel/tame-inertia facts.
- Chebotarev density for finite Galois extensions, with finite exclusions.
- The Hilbert class field and its Artin isomorphism. OS1 explains how Chebotarev then gives a degree-one prime in a specified ideal class.
- The Kummer exact sequence and Hilbert's theorem 90.
- The LD2–LD4 finite local/global reciprocity chain. Its local Tate duality and finite Poitou–Tate inputs are stated and matched in that component.

Primary textbook references checked in the author's editions are J. S. Milne, [Algebraic Number Theory, v3.08](https://www.jmilne.org/math/CourseNotes/ANT.pdf), §§6–7 and Theorem 8.31, and [Class Field Theory, v4.03](https://www.jmilne.org/math/CourseNotes/CFT.pdf), II Proposition 1.22 and V Theorem 3.6, Corollary 3.7, Example 3.9. These are general established theorems, not names for an unproved specialized special-value bound.

There is no retained bespoke Rec, NuSys, count, vChar, or PsiBound assumption in the endpoint. OS9 is the precise supplier for OB3 of odd_minus_bounds; the sibling component independently checks the value's integrality/nonzero property and conducts the same-field character summation and logarithmic estimates. The OS9-to-OB3 interface has been independently checked without a circular nonvanishing premise.

OS1 also supplies the Jacobi ideal annihilation needed in OB5. The sibling quantitative component uses its explicit theta-element identity to deduce Stickelberger annihilation, so a separate general Stickelberger theorem is unnecessary as a retained input on that path.

This component does not close the separate two-primary and odd-plus cohomological suppliers, the geometric common-family interfaces, or the full RH/GRH proof. Its milestone is one complete arithmetic dependency chain through the actual specialized endpoint.

## Source and artifact verification

The fixed source revision is 7cbf7a0c32fca1badf05931879a37c3f8a2b03b4 of the [source repository](https://github.com/CocoSgt/riemann-hypothesis-lean). The component ledger has 77 links on 47 source files, all verified byte-for-byte against the pinned git blobs. These numbers describe the index, not a completion metric.

The script build_component.py regenerates the source manifest, proof-block hashes, claim dependency graph, closure record, and verification record. It checks that every indexed declaration is unique in its file and that all recorded source bytes match the pin. It does not rebuild Lean or infer mathematical truth from matching hashes.

The script validate_tex.py runs the component in pdflatex draft mode with shell escape disabled. Validation succeeded with zero overfull boxes, zero missing-character warnings and no unresolved references. No PDF was produced. The validation is a syntax/font/reference check; mathematical review is separately recorded by the independent reviewers against the frozen TeX hash.

The frozen main.tex SHA-256 is d84beec71cba025a3303be52ab11e0f03ca95a533a3ed333ae401b20bdd47a84.

## Files

- main.tex: the complete readable proof, OS1–OS9.
- provenance.json: each claim's proof range, dependencies, classical inputs and source declarations.
- closure.json: endpoint, exact consumer join and retained scope boundaries.
- source_hashes.json: the pinned source file manifest.
- verification.json: source, range and graph verification results.
- tex_validation.json: draft-mode TeX validation result.
- build_component.py and validate_tex.py: reproducible indexing and validation.
