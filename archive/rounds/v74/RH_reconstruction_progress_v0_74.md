# Edition 0.74 · One normalization for the theta lift

A theta lift in the original proof has two descriptions. One integrates a theta kernel against an automorphic form on a definite unitary group. The other evaluates an algebraic section built from a finite sum over lattice classes. Comparing the two is a prerequisite for transferring rationality between different tuples. Edition 0.74 proves their pointwise comparison with **one nowhere-zero function chosen before the tuple and the pinned coefficient record vary**. It also proves the real reproducing integral for cusp spanning. **Ten whole obligations remain**, shared by RH and unrestricted Dirichlet GRH. [New TeX manuscript](RH_new_proofs_v0_74.tex) · [Cumulative TeX manuscript](RH_readable_reconstruction_v0_74.tex) · [Whole contracts](continuation_v74/obligations.json)

## The pointwise equality

For an automorphic quotient point $q$, a tuple $t$, a rational input $x$, a pinned record $O$ and the section $f$ specified by the comparison, the result is

$$
c\,O.\mathrm{thAd}(t,x,q)=\lambda(q)\,\mathrm{rdQ}(O,1,f,q).
$$

Here $c$ is the scalar in the geometric character section's prescribed value. On the right the level element is the identity. The auxiliary root of unity for every tuple is also one. Changing the coefficient field, the tuple or the allowed phase of the character section preserves the same function $\lambda$. The proof works even when the geometric class sum vanishes. [P74I1–7](continuation_v74/point.tex)

To see how the normalization survives those changes, evaluate both expressions at the same marked point. Unfolding the integral gives finitely many classes weighted by their subgroup volume divided by the order of their stabilizer. On the geometric side the corresponding finite average projects the theta vector onto the chosen lattice's vacuum line. Its norm is the inverse square root of a lattice index. The coefficient pin and the number of terms in the geometric average restore exactly the same square-root factor as on the adelic side. The harmonic degree and component comparison then give $\lambda(q)=K_d C_{k(q)}$ with every factor nonzero. The proof compares the finite sums term by term. [Point comparison](continuation_v74/point.tex) · [Index cancellation for arbitrary split moves](continuation_v74/join.tex)

## From a class sum to the whole base cusp space

On the pinned base data the point kernel for any permitted split move is in the complex span of integrated lifts of rational source vectors. The comparison above uses the same multiplier on both sides of this span. It expresses the corresponding short theta reading as a linear combination of geometric class-sum readings. When a rational unitary matrix changes the source lattice, the normalized vacuum acquires one unit phase on all marked points in the base dictionary. The residue roots can be chosen compatibly, even when the two short levels differ. Applying this twice moves the original short readings to the split ones. Descent of the resulting class-sum span to the original coefficient field is K73G4. [Finite kernel recovery](continuation_v73/kernel.tex) · [Residues and split moves](continuation_v74/span.tex) · [Comparison on the dictionary](continuation_v74/vacuum.tex)

This leaves a specific question on these data. Do the short theta sections on the identity cover generate every bounded cusp section at the specified weight? The earlier reduction ICL14–16 explains how to deduce this from a reproducing integral, a doubled arithmetic identity and a simultaneous dictionary between its analytic generators and the algebraic short sections. The following results supply inputs to that argument. [ICL12–16 and equations (ICL.6), (ICL.7) and (ICL.12)](integral_cusp_lattices_v46/main.tex)

| Ingredient | What the new chapter proves |
| --- | --- |
| Marked higher cover | The theta-section bases commute with arbitrary affine base change. Under the original level, character-value and component-field hypotheses, the construction gives a higher marked model and character section on the prescribed field for every tuple. [D74U1–5](continuation_v74/dictionary.tex) |
| Finite lattice estimate | For $d=[E:\mathbb Q]r$ and $n\ge 4d+4$, the normalized off-diagonal row sum is at most $\pi^2/6-1<0.65$. This supplies the norm field of the required finite-level system and gives strict diagonal dominance. [F74N1–3](continuation_v74/norm.tex) |
| Real reproducing integral | For the actual harmonic Gaussian kernel $K$, at each sufficiently small positive slab width $\delta$, integration against $K$ gives $\rho_\delta F(x)$ for every bounded holomorphic form of the prescribed weight. The integral converges absolutely, and $\rho_\delta>0$ is independent of the form and frame. [K74A1–4](continuation_v74/reproduce.tex) |
| Doubled arithmetic kernel | Rational isotropic spaces split into graphs and singular orbits. Cuspidality kills the singular terms. Every surviving coefficient carries the original stabilizer weight and conjugated vacuum multiplier. The weighted graph series can be differentiated in the elliptic variables. Termwise differentiation of the original theta and Eisenstein series gives the heat equations for their weighted difference, including holomorphy in the period variables. [Arithmetic kernel](continuation_v74/orbit.tex) |
| A bundle already selected by a linked family | For every permitted index of every such selection, one witness gives the base theta square, the separating rational tests, the primitive rows and the base-rank conclusion on that same bundle. Its proof uses the rational tests contained in the witness. Construction of those tests upstream remains essential. [B74R1–4](continuation_v74/bundle.tex) |

## Where the remaining proof enters

For the doubled identity, the unresolved arithmetic comparison is for the class average of the difference of the theta and Eisenstein functions. At zero elliptic argument it needs the definite Siegel–Weil identity for the admitted family. After passage to the doubled coordinates, the invariant harmonic differential operator must annihilate that difference. The statement uses the original finite tests, group multipliers and class weights. These enter (ICL.6), which identifies the resulting periodized kernel with a finite sum of theta products. [Doubled identity and its remaining inputs](continuation_v74/orbit.tex)

For the geometric part, the same principal charts must carry the finite-level system with its covariance, support, cusp and admission conditions. The theta functions on all chart components must then be readings of the actual algebraic short sections, with the normalization in (ICL.12). Finally the outer construction must produce these data and the rational and integral comparisons on a single admissible family. A witness extracted from an already linked bundle supplies the downstream rank implication and cannot serve as its own existence proof. These are reasons the base rational-test, reading and row obligations remain open. [Stable short-section generation](integral_cusp_lattices_v46/main.tex) · [Linked selection](continuation_v74/bundle.tex) · [Checkpoint](CURRENT_CHECKPOINT_v0_74.json)

## Verification

The edition adds 38 indexed claims, bringing the cumulative total to 4,172. The ledger records their dependencies and original Lean source ranges. The corresponding manuscript paragraphs give the hypotheses of each result. Each review identifies the exact TeX bytes examined. The verifier checks those bytes, their source anchors, the claim graph and the open contracts against the public predecessor. The validation record also gives the rendered supplement's page count and the cumulative manuscript's typesetting results. This edition adds human proofs in TeX. [Claim ledger](continuation_v74/claims.json) · [Verification results](continuation_v74/validation.json)

~~~sh
python3 continuation_v74/verify.py --formal-git formal_source
pdflatex RH_new_proofs_v0_74.tex
pdflatex RH_new_proofs_v0_74.tex
~~~
