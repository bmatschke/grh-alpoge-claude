# Independent review of KA5 and KA6

**Result: PASS**, in the stated fixed-target and conditional scope. This is an independent mathematical and source-quantifier review, not a new Lean declaration or compilation.

Reviewed file: `work_v030/audit_count_path/main.tex`

SHA-256: `39a8a5b5483fe5e59de6fb461e03317cf2b4934964da533402c3ea6863d61ea1`

Pinned source: `7cbf7a0c32fca1badf05931879a37c3f8a2b03b4`. Every source block recorded in the accompanying JSON was compared byte for byte with its pinned Git blob.

## Exact conclusions checked

### KA5-full-character

CaseIII requires Odd(orderOf psi) and psi != 1 for the full host character, not merely its prime-to-l or local part. HostComp bounds that full positive order by 2^(ex+1) ordC(chi). Thus a power-of-two target forces triviality whenever the order is odd.

### KA5-coefficients-and-constants

The original Coef l is a DVR subalgebra of a p-adic algebraic closure, hence a domain as required by HostComp. Membership in Host.X gives Host.IsChar. The CountShape implication is vacuous uniformly in the host, Big cutoff, algebraic closure, coefficient ring, prime and twist. Its natural exponent can be C=0 before all those quantifiers.

### KA6-outside

sumOut fixes chi at line53 and evaluates CountI, CountZ, CountII, CountIII only at that same chi in lines54-57. All later calls use the extracted target-specialized instances.

### KA6-inside

sumIn fixes chi,l,j at line89, evaluates CountII, CountV, CountVs at chi and CountIV at chi,l,j in lines95-98. No count at a changed Dirichlet target is required.

### KA6-point

point fixes chi and the entire layer function j before choosing its constants. Its finite exceptional-prime maximum and outside-prime threshold use only hin chi l (j l) and hout chi. This preserves the uniform host, field-model, coefficient and layer-function scope of PointHV at chi.

### KA6-height

thmHV evaluates PointHV only at psi with j(l)=Nat.log l(K.Rl l(Lchi psi l))+3. Thus its proof specializes without any uniformity over other targets.

### KA6-joint-and-VWinAt

jointWin_of invokes hV psi once. vwinAt_of_joint invokes hJ psi once. The remaining global ThmBab/ThmBc inputs may be specialized as written; they are not removed. Prime-pair guards, arbitrary page exponent functions, continuum scales and cutoff Ct=401 remain unchanged.

### principal-case-examples

For chi=1, source minima give pK=7 and pOne=3; the reduced-form calculation gives h(-7)=1, so Bchi={3,7}. q1=11,d=23,s=12 form an original host Big(2). The primitive even dyadic character times Legendre11 has odd parity, c2=14, f0(3)=2, n0(3)=3 and R1=16*9*64=9216<16384, so CountV still includes characteristic3. The displayed CaseI at l=5,e=1 and CaseII at l=3,e=2,t=3 also satisfy their literal predicates. These examples affect the priority claim by excluding false further vacuity; no cohomological nonvanishing is claimed.

### scope

The result removes the separate CaseIII seed/promodularity producer on the selected route for power-of-two targets, including ordinary RH. It neither gives universal CountIII for unrestricted Dirichlet GRH nor supplies the remaining CorGK/PropGK, PMExAlt, CountV or the common arithmetic-family/gap/theta/operator dependencies.

## Review boundary

KA5 and KA6 require no correction. The three surviving arithmetic premises remain `CorGK` at the one quadratic field (or the stronger `PropGK` at that field), `PMExAlt`, and `CountV` at the same target. Inherited closed inputs and unchanged TW/OB/VW guards remain explicit. This review does not relabel any one of those open arithmetic premises as a published theorem application.

The review is bound to the whole-file and claim-range hashes in `count_specialization_review.json`; future text edits require a new hash record.
