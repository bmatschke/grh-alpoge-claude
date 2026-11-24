# Independent mathematical review of the odd-minus supplier

**Result: PASS for OS3–OS9 in their stated scope and the exact OS1 -> OB5 join.**

Reviewed `odd_minus_supplier/main.tex` at SHA-256 `d84beec71cba025a3303be52ab11e0f03ca95a533a3ed333ae401b20bdd47a84`. This review is independent of its author and covers OS3–OS9, with the OS1 principal-ideal consequence additionally checked for its join to OB5. The full OS1 distribution proof is outside this review scope.

## OS3

- The derivative identity (tau_q-1)D_q=(q-1)-N_q gives an Mth-power quotient for every generator of the actual relative cyclotomic group, and the induction closes under products and inverses.
- The corrected Kummer quotient in OS.18 is independent of both choices; P kills mu_M, commutation is only used on the finite cyclotomic field, and U fixes mu_M. This proves actual additivity and continuity.
- Coset reindexing of OS.19 gives beta-equivariance with the stated positive beta weight.
- Expanded OS.20: its third factor contributes (phi^-1(PY'))^(s(q-1)), reducing the expression to the direct ratio of the two Kummer quotients. Every factor is a q-adic unit, all residues equal one, and reduction on mu_M is injective.
- The recurrence is kappa_(qL)(tau)=-s kappa_L(phi); after conjugating the actual place it sums to the same unit recurrence for nu.
- Initialization contains P twice and therefore gives 2 N_0 (alpha(g_0)-a)^2 z w. This coefficient is a unit, so the exact annihilator of z w is retained.

## OS4

- Each noncontainment in the Kummer subgroup H uses the correct conjugation scalar: alpha versus chi for c, beta(j)=1 versus chi(j)=-1 for nu, and inversion versus trivial action for the next cyclotomic layer.
- The three-subgroup avoidance proof is valid: x^2 and x^M in the middle subgroup imply x lies there because M is odd.
- A single open Frobenius condition simultaneously controls c, generation of nu(U), splitting modulo F, failure to split modulo Fp, and the prime-to-p order of r modulo q. No independent incompatible prime choices occur.

## OS5

- Matched the literal Rec declaration, including its nonzero annihilator, open reduction-kernel hypothesis, bounded local witnesses, and simultaneous local conditions.
- The cup cocycle lambda(n(g) alpha(g)c(h)) has cyclotomic target. For c=delta(m), the displayed cochain -lambda(n(g)alpha(g)m) has exactly that coboundary.
- At q the class is N cup x_0; the trivial cyclic module R has every unramified class a multiple of x_0. LD4 and LD2 therefore force N to be unramified, hence zero on actual inertia values.
- All additive Z/p^h-linear maps from O/(a') separate points. This avoids any unjustified perfect trace pairing in a possibly ramified coefficient ring.
- The commutator formula OS.26 extends nu to a beta-cocycle with precisely the same annihilator bound. The final DVR valuation argument proves d c(phi_q)=0, including the unit-annihilator case.

## OS6

- Initialization uses M=k_0 z and ann(w)=(M), giving ann(z w)=(k_0); a_0 divides k_0 as required by reciprocity.
- Evaluation on T_n has kernel exactly T_(nq), including all conjugate places, and image contained in A[d]. Thus the quotient-length bound is stronger than a merely elementwise annihilation statement.
- A nonzero normalized cocycle remains nonzero on U: factoring through the abelian quotient and comparing jg with gj forces it to vanish because -2 is a unit.
- OS4 selects one prime with c(phi_q) nonzero and nu_L(phi_q) generating the image; OS3 then identifies the inertia annihilator at the next stage.
- Each nonzero stage strictly increases v(a_L), bounded above by v(M). Induction on v(M)-v(a_L) proves the extended-length bound and finiteness together.
- Only the finite integer v(k_0) is cancelled at the end; no subtraction of infinite lengths or prior finiteness assumption is used.

## OS7

- Recomputed the leading Bernoulli expansion in OS.35: twice the difference equals -b^(k-1) theta(t) t^(k-1) modulo F after a fixed denominator. No level-dependent denominator is needed.
- Multiplication by eta(bt) and reindexing gives exactly b^e eta(b) S - 2(eta(b)b^k-1) B_(k,eta_F)/k, with the stated sign and factor 2.
- Raising the p-power level preserves the primitive Bernoulli value except for the single factor 1-eta(p)p^(k-1) when p does not divide the primitive conductor; this factor is a unit because k>=2.
- The nonresidual hypothesis makes eta(b)b^k-1 a unit. The strict p-adic error bound then gives v(z)=v(Y), and z lies in the original O.
- The same choice of level implies a_0 z divides p^m. Also z divides den(N,k)B_(k,eta) because that scalar is k den(N,k)Y.
- All lifts and character values remain in the original coefficient ring and algebraic closure; no auxiliary field comparison is substituted.

## OS8

- Normalization at complex conjugation is unique and O-linear because alpha(j)-1=-2 is a unit.
- Primitivity and prime-to-p order give a unit alpha(tau)-1 at every non-p conductor prime. This both bounds the inertia witness and promotes its coboundary identity to the decomposition group.
- One finite torsion bound kills the cocycle image and all conjugate local witnesses, so the normalized strict Selmer module is exactly the increasing union of the displayed finite-exponent stages.
- The finite-chain argument bounds the length of the union without noetherianity.
- In the residual case alpha modulo varpi equals chi_p. Away from p, prime-to-p character values force actual unramifiedness; global and p-local invariants vanish by unit character differences.
- The varpi-torsion lifting sequence preserves strict local conditions and identifies the residual coefficient with k(1). Componentwise rational Kummer classes have every prime valuation divisible by p; the sign is a pth power since p is odd.
- No residual varpi-torsion remains, and every class has finite varpi-power order, proving the entire module is zero.

## OS9

- Matched PsiOf.psiOf and the universal PsiBound declaration in ZeroMemUnrHom. Primitive induction preserves the actual O-values, parity and prime-to-p character order.
- The a=0 case is handled by the extended valuation; no Bernoulli nonvanishing assumption is imported from OB2, so the OS9 -> OB3 dependency is acyclic.
- The varying levels have identical prime support fp, so they bound the same normalized module before the increasing-union passage.
- IsCycAct identifies the Galois character with psi composed with actual restriction to E, not merely an isomorphic representation.
- Averaging over Delta of order prime to p gives restriction onto invariants. The coefficient alpha=chi_p^(-e) psi^(-1) converts those invariants into the positive psi-eigenspace for the negative twist.
- At every actual decomposition and inertia group, the quotient has order dividing |Delta|, so local restriction is injective. Thus all strict local kernels and original choices are preserved.
- The resulting length is literally psiLen(Omega,e,psi), with the scalar den(N,e+1) Bprim and all source quantifiers unchanged.

## Exact quantitative join

OS9 supplies the literal `PsiBound` consumed by OB3. Its zero-Bernoulli case is covered by extended valuation, so it does not depend on the nonvanishing later supplied by OB2. OS1 also supplies OB5 through the displayed factor-2 reindexing identity; cancellation takes place only in the odd-primary target. The direct classical Stickelberger input is therefore unnecessary.

## Verification and limits

The independent byte check verified 9 human proof ranges, 77 declaration links, and 47 distinct source files against pinned commit `7cbf7a0c32fca1badf05931879a37c3f8a2b03b4`. These are provenance checks, not a new Lean build. There are no unresolved mathematical findings in the reviewed scope. LD2–LD4 and the named classical arithmetic theorems remain the explicit inputs. This review does not assert that the whole RH/GRH reconstruction is complete.
