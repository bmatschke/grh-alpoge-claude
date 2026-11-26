# Edition 0.73 · The theta kernel and class sums on the given data

The rational theta argument asks for a finite family of tests on the image of the selected theta map. Each test must take values in the fixed embedded coefficient field on two sets of vectors, the images of all original rational inputs and the stored target basis. This edition constructs the higher moduli scheme on the given lower model, supplies a geometric class sum and proves a finite-point spanning result used to build those tests. The whole rational-test and reading obligations remain open. The manuscript has **4,134 indexed claims and ten open whole obligations**, all shared by the two routes. [New TeX chapters](RH_new_proofs_v0_73.tex) · [Cumulative TeX manuscript](RH_readable_reconstruction_v0_73.tex)

## From a point kernel to integrated lifts

Fix a tuple, a finite adelic point on the definite group, a coefficient vector, and the lowest-type tensor. Average the vector over the rational elements carrying the given point to a variable finite point at the required level. This constructs a form supported on one double coset. Its level character cancels the inverse character in the theta kernel. On the unique contributing class the sum has as many terms as there are elements of the rational stabilizer. The normalized volume of that class is the reciprocal of the same cardinality. The integral is therefore **exactly the original point kernel** for every target argument. Linearity puts this function in the complex span of the lifts of the original rational source vectors. The same chapter proves when a complex span of geometric readings descends to the required coefficient field. [K73G1–4](continuation_v73/kernel.tex)

## The higher cover and the class sum

| Result | Hypotheses and conclusion |
| --- | --- |
| Higher moduli at the prescribed level | The cover parametrizes the isomorphisms on the newly added half of the torsion. It is finite étale and surjective over the original lower scheme. The proof checks the full compatible Tate marking, uniqueness on reduced schemes and the infinitesimal test. [A73H1–2](continuation_v73/cover.tex) |
| Framed points and level datum | The pullback of the same polarized abelian scheme lifts every original framed point, including the generator of its theta sections. With the canonical connection and unit section this satisfies all fields of the original level record. [L73D1–2](continuation_v73/level.tex) |
| Determinant character | The construction on norm-one finite ideles gives the prescribed value on each unitary determinant. It is trivial on rational determinants and on the required ray subgroup. Its determinant values lie in the original embedded field. [T73K1](continuation_v73/tests.tex) |
| Algebraic character section | On this higher model with a marked dictionary and component-field condition, indicator functions of the components give a weight-zero section over that same field. It has the required value for every marking, with common scalar one. [T73K2–3](continuation_v73/tests.tex) |
| Class-sum section | For each tuple of a supplied pinned record, the finite short-series formula descends through the level cover and gives a cusp section. Its point values determine it among all sections of the prescribed weight. The construction also applies after the permitted rescaling of the cover character section. [T73C1–5](continuation_v73/compare.tex) |
| Support of the reading | On a supplied weighted point, a nonzero row part contains a base-level row. Each corresponding base W-part contains the lift of a rational column. One such column works at every other infinite place because the original quotient metric is positive definite there. An audit of every use in the original bundle-witness construction eliminates its eventual global multiplicity premise once the point and the remaining inputs have been supplied. Initial constructions that require multiplicity to produce the point’s data still retain it. [R73P1–5](continuation_v73/reading.tex) |

The next comparison needs a single nonvanishing function and group element chosen before the tuple record varies. The equality must connect each geometric class sum to its adelic lift, including the records obtained by rescaling the character section. The kernel computation above addresses a distinct issue, the span by rational-input lifts at a fixed point. Full generation of the base cusp space still needs the short-series comparison. The higher moduli scheme and framed level datum now follow from the given lower model. Its normalized marked upper dictionary and the comparison with the original selected bundle still require their own constructions. [Original rational-test route, RTG16–25](rational_theta/main.tex) · [Exact remaining contracts](continuation_v73/obligations.json)

## Verification

Twenty-one new claims are indexed against the original Lean revision. The checker verifies the source excerpts, manuscript and review digests, dependencies and the ten continuing whole obligations. The two arithmetic closures and their consequences are recorded in edition 0.72. This edition adds mathematical arguments in TeX. The verification record distinguishes source checks, typesetting and mathematical review, and includes the scope of each. [Claim ledger](continuation_v73/claims.json) · [Verification record](continuation_v73/validation.json) · [Arithmetic closures](RH_reconstruction_progress_v0_72.md)

~~~sh
python3 continuation_v73/verify.py --formal-git formal_source
pdflatex RH_new_proofs_v0_73.tex
pdflatex RH_new_proofs_v0_73.tex
~~~
