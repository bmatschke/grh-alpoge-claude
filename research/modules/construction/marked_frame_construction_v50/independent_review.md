# Independent review of marked-frame construction v0.50

**Verdict: PASS at the stated original premises.** No unresolved mathematical or quantifier defect was found.

Reviewer: `/root/geometry_alltest` (independent of the author).
Source pin: `7cbf7a0c32fca1badf05931879a37c3f8a2b03b4`.
Proof file SHA-256: `b35edcd7c974e078f227df139c80da08d0864e3ae240f140193b93eb3ada73c3`.

## Review scope

All fourteen numbered proof blocks were checked against the pinned source contracts and the relevant source bodies. The review checked the exact nineteen-field Gen entry, all twelve UFacts fields, the actual GalLink/Linked/FLink records, the strict-class cohomology arguments, and the literal Frame.Ok and cone definitions. The reviewer did not modify the proof file or author metadata.

All 30 source snapshots were independently compared byte-for-byte with `git show` at the pin. All 30 referenced source ranges, all fourteen proof-block hashes and all five inherited input file hashes were verified.

## Claim-by-claim findings

### MFC1

The CRT conditions are compatible because p does not divide 2DM. They give n>0, -n=1+4Mt and v_p(Dn)=1. The valuation contradiction at every place over M makes its full decomposition group fix sqrt(-n), so the exact local subgroup equality holds, including above 2. Eisenstein at the new odd p gives the required ramification outside M. The real quadratic fixed field has index exactly two and contains every complex conjugation. The source output has no requirement that n itself be prime.

Proof block SHA-256: `34f1aa0697e7c6e8004107ca375a9cfe83bf596236d6585d83931971c8c7caed`.

### MFC2

The shifted prime-power cyclotomic polynomial is Eisenstein, yielding full inertia surjectivity at every prolongation. The odd-prime unit decomposition gives index ell^m and the literal kernel intersection H_m intersect ker(epsilon_1)=ker(epsilon_(m+1)). Inertia away from ell kills the entire cyclotomic tower. The m=0 and r=0 cases are preserved.

Proof block SHA-256: `38be2c458aa5f71eb5f954e18921147a339cbf30014e4f3bba1d7d135cb647d5`.

### MFC3

All three tower factors have abelian ell-power quotients, so the single exponent ell^(1+b+m) works before the element is chosen. Residual units have no ell-power torsion. The inertia element outside H0 kills eta, alpha and omega by the exact conductor hypotheses, and the index-two coset argument proves all three source implications, including restriction to ker(eta).

Proof block SHA-256: `b6a7254537d46761db54ebff55eb6b4a0213e2c303731ea2c51f6e12e7da53e7`.

### MFC4

All twelve literal UFacts fields are supplied. The -1 inertia lift lies in every factor and has nontrivial mod-ell cyclotomic image. The degree lower bound uses actual relative indices. The g4 witness times complex conjugation forces all f2b/f2c/f5 failures, and conjugation plus an ell-power preserves the nonquadratic local g5 witness. Full Gen, including Hb and its exact local lifting clause, is retained.

Proof block SHA-256: `1b18c56fe42de4c19b33a1a2dba7fe13792a1b54cea8669eb1a53afcabbd03b2`.

### MFC5

The fixed subgroup V is open, abelian-quotient, and fixes mu_ell. The displayed tower equality is an equality in the original Galois group. Kum.XDual at modulus one has no added decomposition condition. Since the actual finite abelian field is totally complex, finite class-field reciprocity identifies exactly its unramified additive character space with ideal-class characters. TW1 applies to this fixed E at all levels, producing C0 before m. No twisted cone bound is inferred.

Proof block SHA-256: `134f89d9551c6a63748613682266e765ecfc3098f20488b69fe8d4dbe811fe8a`.

### MFC6

CAF8 applies using UFacts openness, commutator containment and all complex conjugations, yielding the embedded field L and literal equalities G_L=U intersect ker(eta), G_(L+)=U. The original B local witness lies in G_L by split. The choice m=3C0+7 occurs after the uniform bound and satisfies ell^m>3C0+7 for odd ell.

Proof block SHA-256: `3f82510323be1f4625b6842f947ca902aaa09f15ffa66bd07e19450926c17bb5`.

### MFC7

The chosen valuation representatives are actual primes of L+ above ell. Multiplying a conjugating element by complex conjugation corrects eta to one without changing its L+ place. The U-orbit uniqueness, decomposition/inertia intersections, local relative index, local degree sum, and all real-place conjugations have the exact linkage scope. Abelianity of L ensures the finite local Galois degree interpretation.

Proof block SHA-256: `504faabb24f1585ce8ad964a9719799c3bf40138902ea651f9dcf7531de74a55`.

### MFC8

The quotient uses the closed normal closure in the same U of exactly the inertia elements killing eta and alpha away from ell. It agrees with tameN under the fixed topological identification G_(L+)=U. K0 has prime-to-ell index and contains J; J also kills epsilon. All Frame, GalLink, GLink, LLink and FLink fields, including arbitrary valuation/trivial valuation cases, exact marked g1 image, local maps, kernel, degrees, inertia preimages and comparison equations, are supplied without changing field models.

Proof block SHA-256: `208a6c81dd7cc2324b070fe8b3ccefefeafb6ae107a4cd60bbc2abee6215354f`.

### MFC9

The proof uses fields of an arbitrary Linked record, not equality of its underlying quotient type. Quotient topology and character pullback prove continuity/open kernels; real-place equations, local degree sums, marking and residual reduction are literal. All seventeen ok_basic Ok fields plus Gen oddness/finiteness give nineteen. The additional relative degree and nonempty-place statements yield exactly Big(C0) with source constant 3C0+5+2.

Proof block SHA-256: `7272e28ce967d41fe2997ba7871b2b50ddc24334ca571c334f2f5b48f8ef64aa`.

### MFC10

The finite-module global and real invariants vanish by oddness, and the twisted dual vanishes since omega is prime-field valued and multiplication by kappa(s)-omega(s) is invertible. Local invariants vanish at every place other than w. At w, H0 and H2 have cardinality |k|, so local Euler gives |H1|=|k|^2. The exact Greenberg-Wiles identity then yields |Sel|=|k||Sel-dual| and a nonzero class. Inflation preserves noncoboundaries, and the displayed conjugation formula supplies local primitives at every prolongation. Original GC.Hypotheses2 remains an antecedent.

Proof block SHA-256: `5cde3fd963e124c63c238136db49c0bd7df3d4351d3b25614122eb898eb6eaaf`.

### MFC11

Subtracting a local coboundary and using normality of U proves restriction injectivity when kappa|U is nontrivial. At p different from ell, continuous ell-primary additive inertia characters have one-dimensional prime-field character space from tame inertia; the nonzero index-ell quotient character therefore annihilates every coordinate on its kernel. This proves the exact kernel vanishing needed at w.

Proof block SHA-256: `a460b840fd23345938fd0ef400303478d4d8487bea7ec2390e5da155e72bb8d3`.

### MFC12

Both characters alpha^(-a)eta are odd, noncyclotomic and locally nontrivial above ell. The finite set S consists only of ell, w and genuinely ramified primes of that character, so every other member has the local nontriviality needed by MFC10; no unramified dropped prime remains uncontrolled. The cocycle vanishes on inertia outside S and on inertia elements killing kappa within S except w. At w, tame inertia plus Htheta kills the required restriction. Nontriviality survives restriction to U, establishing all StrictCl clauses at every m for a=1 and a=2 on the same data.

Proof block SHA-256: `cf9a24e25c8cd7fb6cd726e268b12c3bd73bb02f4efe184da8ccc38c5f563645`.

### MFC13

The exact GalLink kernel generators are killed by the StrictCl inertia clause. The subgroup of kernel elements with cocycle value zero is closed and normal, so the cocycle vanishes on the whole closed normal closure. Descent through any continuous surjective linked map is locally constant. The actual j_v and loc_v identities give precisely Z1C with zero local subspaces. A zero cone class would imply one global coboundary and contradict strictness. Both original f4 and f4-prime are thereby obtained without changing any frame.

Proof block SHA-256: `f11004400e0de7f591d5543e7baee213f354845ee85371e3f0bd4693a8f43d10`.

### MFC14

Choice order is Q, H0, w, uniform C0, m, embedded L, marked g1, linked Phi, then both strict classes. All twenty-one supplied Ok fields lie on this one Phi; seven named fields remain. For the original coefficient DVR, full Gen implies CAF7 seed assumptions and its modulus is chosen first; the same L and g1 meet its square-witness condition. No complete HasFrameW, GdFrameEx, HostFrameEx, GdEnd, automorphic seed or selected whole obligation is claimed.

Proof block SHA-256: `eb8a3958ce28fde0c10b9633edfcc6375d88e52cb3a73bd6d41ee557f1b8ecda`.

## Premises and remaining boundary

The full original Gen is retained, including the actual Hb, its ell-power index, all local lifting conditions and the nonquadratic decomposition witness. The strict-class theorems retain the original GC.Hypotheses2. The uniform class-rank theorem uses the already reconstructed TW1 and its explicitly named classical foundations; finite class-field reciprocity is retained at the actual totally complex finite fields.

The chapter proves nineteen basic Ok fields and the two nontrivial strict cone fields on the same actual frame. The seven fields phi, gen, cl, ec, b1p, b1 and h1 remain. The uniform unramified class-character bound is not misrepresented as any of the three twisted cone bounds. Full gen_gd/gen_host entry producers and the complete HasFrameW, GdFrameEx, HostFrameEx and GdEnd exits remain open, as do the automorphic seeds and later common-family assembly.

The elementary CRT replacement of a prime-progression auxiliary choice is valid at the full original FrobeniusSplitPrimeDatum output scope. No hidden change to the field, marked element, local groups or order of choices is required.
