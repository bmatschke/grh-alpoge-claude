# Published inputs and the terminal analytic obligation — v0.30 audit

This audit accepts the correctness of the pinned formal proof. “D” below always concerns an unproved identification or implication in the human reconstruction, never a claimed defect in Lean. The source commit is `7cbf7a0c32fca1badf05931879a37c3f8a2b03b4` of `CocoSgt/riemann-hypothesis-lean`.

## 1. The material reduction found in this audit

The exact final analytic source needs **a bound on the weighted positive part on late windows**, not necessarily the stronger pointwise estimate used in the v0.29 sufficient map. For a fixed primitive target and its fixed positive character family, put $H=H_\psi$. For each $1/2<\theta<1$, it is enough to have some fixed $\delta>0$ such that

\[
 \forall\eta>0\ \forall Y_0\ \exists Y\ge\max(2,Y_0):
 \quad \int_Y^{Y^{1+\delta}}\max(H(x),0)x^{-\theta-1}\,dx\le Y^\eta.
\]

The stretch $\delta$ may depend on the target and on $\theta$, but must be chosen before $\eta$ and the window. It even suffices to use a sequence $\theta\downarrow1/2$. The old pointwise bound implies this condition because its integral is at most $C_\theta\delta\log Y$. The converse is false in general: the integral condition permits short positive spikes. A bound on the **signed** integral is insufficient, since the localization inequality requires the positive part.

The exact native source definitions are `CharFamily.lean:WindowHyp` and `LandauZeroFreeCriterion.lean:WindowHypU`. The source's `landau_window` proves the logarithmic pole criterion, `lemmaL` proves the character-family consequence, and `zeroFree_of_rpow_window` is the pointwise special case. In particular the source already permits any fixed positive stretch; the exponent $3/2$ was a convenient choice in the reconstruction, not an analytic necessity.

`analytic_envelope.tex` gives a complete independent human proof as **AQ1–AQ5**:

| Claim | Complete conclusion | Classification |
|---|---|---|
| AQ1 | Equivalence of the source envelope interface with the positive-part integral above | B, now closed |
| AQ2 | Explicit gamma localization for every fixed positive stretch, with ceiling errors included | B, now closed |
| AQ3 | The integral condition excludes every constituent zero to the right of θ | B, now closed, using the already reconstructed Mellin continuation |
| AQ4 | The resulting fixed-target contract gives RH/Dirichlet GRH | B, now closed, using GH6 |
| AQ5 | Integer-to-real interpolation for the original centered ramps, with error at most $1/(8n)$ on $[n,n+1]$ | B, now closed |

AQ2 takes $d=\min(\delta,1)$, $m=1+d/2$, $h=8m/d$, $\sigma=(h+2)^2+3$, and $k=\lceil m\sigma U\rceil$. Exponential tilting bounds both tails by $C_\delta\sigma^{-k}e^{-mU}$. AQ3 then bounds the relevant derivatives by

\[
 |A_k(\sigma+it)|+A_k(\sigma)
 \le 2e^{\eta U}(\sigma-\theta)^{-k}+O(\sigma^{-k}).
\]

After locating a putative nearest pole, one chooses η sufficiently small **before** using the arbitrarily late-window assertion. The resulting exponential rate contradicts either the unique nonreal pole contribution or the positive residue of a real pole. Positivity of the character weights prevents coincident-zero cancellation. The proof does not use zero density, automorphy or cohomology after the window input.

AQ5 observes that between integers the nonprincipal ramps and the von Mangoldt ramp sums are affine, while the principal term contributes exactly $H''(x)=-1/x$. Thus the concavity gap above the chord is between zero and $(x-n)(n+1-x)/(2n)$. Integer window bounds on $[Y,Y^\lambda]$ imply real bounds on a slightly shorter fixed stretch $[Z,Z^\mu]$, $Z=\lceil Y\rceil$, $1<\mu<\lambda$. This is a second reduction of the terminal contract, not a construction of those integer bounds.

**Strategy consequence.** Add the integral-envelope supplier as an explicit alternative leaf. It is potentially worth investigating whether the arithmetic height/gap argument can give it with less uniform work. At present no such saving has been proved; the existing pointwise source route and all its actual-family obligations remain. It would be incorrect to count the weaker analytic contract itself as closing any arithmetic supplier.

## 2. Strict A certificates checked from primary sources in this round

These are certifications of applications, not reconstructions of the deep published proofs. Each applies only in the scope stated below. Primary PDFs were read at the theorem; Bombieri's relevant scanned pages were visually inspected because the extracted formulas lose exponents.

### CN: quadratic class-number normalization — A

Primary source: Andrew V. Sutherland, MIT 18.785, Lecture 19 (15 November 2021), the analytic class-number formula on page 1: [PDF](https://math.mit.edu/classes/18.785/2021fa/LectureNotes19.pdf).

The required hypothesis is a number field. For a real primitive nonprincipal Dirichlet character, the associated field is quadratic with fundamental discriminant $D$ and conductor $f=|D|$. Factoring its zeta function as $\zeta(s)L(s,\chi_D)$ and using the residue $1$ of zeta yields the exact normalization in QP1. For $D<0$, $R=1$, $h\ge1$, and $w\le6$; for $D>0$, $w=2$, $R=\log\epsilon_D\ge\log((1+\sqrt5)/2)$. Hence $L(1,\chi_D)\gg f^{-1/2}$ with an absolute positive constant. No effective uniform Siegel theorem is being imported.

### BD: the exceptional-factor density theorem — A

Primary source: Enrico Bombieri, *Le grand crible dans la théorie analytique des nombres*, Astérisque 18, §6, Theorem 14, printed pp. 38–39, [scanned primary text](https://www.numdam.org/item/AST_1987__18__1_0.pdf).

The theorem sums over primitive characters of modulus at most the common parameter $T$, and counts zeros with α at most the real part at most $1$, and absolute imaginary part at most $T$. Set $T=R$, α=σ. Its exceptional zero is the real, simple Landau–Page zero in the stated $c_1/\log T$ neighborhood. With that zero removed, the theorem gives the extra factor $(1-\beta_1)\log R$ as required by QP's BD premise. In the unconditional estimate, adding the omitted zero costs at most one, absorbed into the absolute constant because $R^{A(1-\sigma)}\ge1$. The choice of absolute exponent is existential; no explicit large source numerical constant is asserted.

### HD: the hybrid density specialization — A

Primary source: D. R. Heath-Brown, *The Density of Zeros of Dirichlet's L-Functions*, Canadian Journal of Mathematics 31 (1979), 231–240, Theorem 1 on p. 231, [publisher PDF](https://www.cambridge.org/core/services/aop-cambridge-core/content/view/7BEA17255131BE21F20DED8223306040/S0008414X00014942a.pdf/div-class-title-the-density-of-zeros-of-dirichlet-s-span-class-italic-l-span-functions-div.pdf).

The theorem is uniform for $T\ge1$, $Q\ge1$, and $11/14\le\sigma\le1$, counts both signs of the imaginary part and multiplicities, and sums only primitive characters. Its exponent is $2(1-\sigma)+h$, with any fixed $h>0$. QP16 sets $T=Q\ge2$, σ=$399/400$, $h=1/100$, giving $3(2/400+1/100)=9/200<1/4$. A bad primitive character contributes at least one zero; counting characters by zeros is therefore valid. An omitted or totalized principal character costs at most one character. No hypothesis remains unmatched for this substitution.

### QX1: polarized adjoint vanishing — A plus the written B transport

Primary source: Jack A. Thorne, *On the vanishing of adjoint Bloch–Kato Selmer groups of irreducible automorphic Galois representations*, Theorem 6.1 on printed p. 24 and §6.3 on p. 25, [primary PDF](https://arxiv.org/pdf/2207.04925).

The theorem requires a CM field, $n\ge2$, an actual regular algebraic cuspidal polarized pair, an isomorphism $\overline{\mathbb Q}_\ell\simeq\mathbb C$, and irreducibility on the full cyclotomic extension. It has no residual adequacy hypothesis and no lower bound on ℓ. QX1 checks these against the literal definitions: `IsAutCsdA` supplies the cusp and attachment; `TypeI` is irreducibility on the cyclotomic kernel; surjectivity of the original quotient identifies this with the required absolute Galois subgroup. The form and action comparison proves the same polarized adjoint, including minus transpose at complex conjugation; the source `Af.IsBK` condition is transported through the already reconstructed period-ring and local-group comparisons. This supplies the stated adjoint theorem. It supplies no characteristic-ℓ support assertion and no automorphic point where none was already given.

### Caraiani local compatibility and temperedness — A in the CSD scope

Primary source: Ana Caraiani, *Local-global compatibility and the action of monodromy on nearby cycles*, Duke Mathematical Journal 161 (2012), Theorems 1.1 and 1.2 on p. 2312, [primary PDF](https://www.ma.imperial.ac.uk/~acaraian/papers/lgc1.pdf).

Theorems 1.1–1.2 apply to an actual cuspidal conjugate-self-dual representation over a CM field that is cohomological for an irreducible algebraic coefficient. They give full Frobenius-semisimplified compatibility away from ℓ and temperedness at every finite place. QX9 applies them after its actual CSD and cohomological match. The restriction ℓ different from the local residue characteristic belongs to Theorem 1.1's compatibility conclusion; it is not a restriction on Theorem 1.2's temperedness conclusion. The generic polarized statement or compatibility at ℓ needs the separately named theorem and normalizations already recorded in QX; it is not obtained by erasing this distinction.

### Hida rank-two ordinary control — A only for the specific SX3 module

Primary source: Haruzo Hida, *Control of nearly ordinary Hecke algebras* (Luminy lecture, July 2007), Theorem 1.2, Lemmas 2.1–2.2, Theorem 2.4, Corollary 2.5, Theorem 3.1 and Remark 3.1, [author PDF](https://www.math.ucla.edu/~hida/Lum07.pdf).

Theorem 1.2 assumes the module system A0–A4. SX3 uses the definite quaternion algebra over a real quadratic field, ramified at both real places and no finite places, fixed central character, and the specified level system. Lemmas 2.1–2.2 identify this actual cuspidal Hecke system and verify the axioms; Theorem 1.2 yields finiteness and torsion-freeness over the fixed-central weight algebra. Classical specialization uses the control theorem. Theorem 3.1 supplies the ordinary line/quotient formula over characteristic-zero points; residual absolute irreducibility is only the additional integral realization in Remark 3.1, not a premise of that characteristic-zero statement. This check supports SX3's scoped use. It does not identify a general rank-four unitary module or supply `HidaPropsAlt`.

### Complete-local connectedness — A after the component's dimension bounds

Primary source: Stacks Project, [Lemma 52.14.1, tag 0ECR](https://stacks.math.columbia.edu/tag/0ECR).

The hypotheses are a complete Noetherian local ring $A$, a proper ideal $I$, and a closed bad set $Z\subset V(I)$. The bound uses the least component dimension, the connectedness dimension of $\operatorname{Spec}A$, and the cohomological dimension of $I$. UX10 applies it to a regular formal power-series domain with its actual proper relation ideal. An ideal generated by $b$ elements has cohomological dimension at most $b$. The theorem converts the explicit lower component dimension and upper bad-locus dimension into connectedness. Those dimensions, the properness and the actual universal-ring identification are proof obligations in UX, not supplied by the citation itself.

## 3. A concrete rejected shortcut: characteristic-ℓ support

The original remaining producer asks for **one ideal** in the actual universal ordinary ring carrying all six fields of `HidaPropsAlt`: `ring`, `dense`, `pt`, `end1`, `end2`, `twist`. The selected QX route also asks for `P1core` on that same ideal and on its two actual links, after one coefficient threshold that precedes all later coefficient and ring choices.

The exact `P1core` assertion says that for each original `NiceI` point lying on the ideal, every prime below that point's kernel also contains the ideal. This is a characteristic-ℓ support theorem. Characteristic-zero tangent vanishing does not establish it.

Allen–Newton–Thorne, *Automorphy lifting for residually reducible ℓ-adic Galois representations, II*, [arXiv:1912.11269v2](https://arxiv.org/pdf/1912.11269), Theorem 4.1, gives a closely related support theorem, but its input also includes the setup of §4.2. This requires that the residual constituents be individually conjugate self-dual with the specified multiplier and pairwise distinct, equivalently the stated residually Schur condition. Its theorem then adds genericity, exact auxiliary local conditions, primitivity, a cyclotomic Schur restriction, absence of a quotient of order ℓ, and $\ell>3$ with ℓ not dividing $n$.

The human reconstruction has not shown that this full list holds on the two QX links. Polarization of the total sum alone does not imply individual polarization of each constituent: it may pair different constituents. Rank four makes ℓ not dividing $n$ easy only after excluding $\ell=2$, and does not remove the theorem's $\ell>3$ premise. Consequently:

| Obligation | Class | Completion test |
|---|---|---|
| Actual rank-four ordinary Hecke module and its six-field ideal | C | Construct the exact module/map and prove all six fields on the same kernel |
| Actual characteristic-ℓ support at the source `NiceI` points | C | Reconstruct the original patching producer, or give an entirely matched published replacement |
| Claim that Allen–Newton–Thorne 4.1 already applies to the two QX links | D | Prove every missing hypothesis and identify its rings/ideals/points with the source objects |
| Rank-two Hida control as a substitute for the rank-four six-field package | D | A module/theorem identification is absent; shared terminology is not evidence |
| Generic automorphy or an unrelated finite quotient as a substitute for the source ideal | D | Establish the exact universal maps, all point clauses, twist property and common threshold |

These are failures of proposed shortcuts in the current human argument. They are not counterexamples to, or criticism of, the assumed verified formal proof.

## 4. Audit policy for the inherited classical frontier

The v0.29 map contains 29 leaf nodes whose status names a classical input, including CN/BD/HD. There are also 101 entries in 22 `classical_inputs.json` registries; these counts include overlap and are not 101 independent unresolved theorems. An audit should identify the exact leaves consumed on the selected complete route and retain their existing theorem/hypothesis certificates.

The seven applications above were checked afresh in this round. The remaining inherited certificates were inventoried, not all independently reproved or rechecked from every original publication. This distinction should survive in the machine-readable map: `closed_by_published_theorem` and `primary_source_rechecked_this_round` are different fields. A theorem's proof can be extremely deep while its exact matched use is class A. Conversely, a file or record named “Literature…” is not automatically class A; its individual fields and their hypotheses must be exposed.

The fixed-target analytic endpoint is class B, now fully written at the weaker actual interface. Its sole substantive open arithmetic input is the positive-envelope window supplier (or one of the stronger suppliers implying it). The prime-density theorems are A leaves of pair selection, not leaves of the final analytic implication. The rank-four ordinary Hecke/support producer remains class C. This is the clearest priority distinction supplied by the present review.

## Evidence and validation

The adjacent `audit.json` records the scoped classifications, primary URLs, inherited inventory and claim/source hashes. `analytic_envelope.tex` is new text only. No predecessor component was changed. The source files were inspected at the pinned checkout and their byte hashes were bound to the provenance. Draft-mode TeX compilation checks syntax only; it is not a fresh formal proof check or a visual review. The new arithmetic window or an unconditional RH/GRH proof is not claimed.

## Additional independent peer review

`count_specialization_review.md` and its JSON companion record a passing, hash-bound independent review of KA5–KA6. The original Case III uses the order of the full host character, so it is empty for targets of power-of-two order. Every height/window consumer retains the same fixed target. This removes that separate producer on the selected principal-target route while preserving the surviving Case I, II and V obligations, including characteristic three.
