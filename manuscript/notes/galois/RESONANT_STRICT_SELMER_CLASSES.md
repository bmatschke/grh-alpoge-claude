# Resonant primes in the strict Selmer sum

Fix a primitive Dirichlet character $\chi$ of conductor $f$ and order $o$. Put $M=M_\chi$, let $E_1$ be the conductor-one host at the same dyadic layer and auxiliary primes $q,d$, and set $E=E_1M$, $N=\operatorname{lcm}(2^a,f)qd$. Write $\Delta=\operatorname{Gal}(E/\mathbf Q)$, $G=\operatorname{Gal}(E/E_1)$ and $P_\chi$ for the fixed exceptional set of [ETS39][ets39]. The targets here are the quotients
$$
 Q_{\ell,e}=\mathcal S_\ell(E,e)^{c=(-1)^e}/
                  (\mathcal S_\ell(E,e)^{c=(-1)^e})^G
$$
at $\ell\notin P_\chi$ with $1\le e<t$ and $\ell-1\mid 2e$. Such primes satisfy $5\le\ell\le2e+1<q,d$ and $\ell\nmid N|\Delta|$. We may split $\Delta$ over the unramified coefficient ring $O=\mathbf Z_\ell[\mu_{\exp\Delta}]$. After tensoring with $O$ the target is the direct sum of the strict groups over $\mathbf Q$ for characters $\psi$ of $\Delta$ with $\psi(c)=(-1)^e$ and $\psi|_G\ne1$. Their coefficient is $D=(\operatorname{Frac}(O)/O)(\Psi^{-1})$ with $\Psi=\epsilon_\ell^e\psi$. Length over $O$ gives the original length over $\mathbf Z_\ell$ after summing all these characters. [Original host, parity and case split][cases] · [Integral character comparison][ets39]

## The local Frobenius at a resonant prime

<!--
% BEGIN RSC1
-->

<span id="claim:RSC1"></span>Let $2^b$ be the conductor of the dyadic component $\psi_2$. Set
$$
 k_\ell=1+v_2(o)+v_2(\ell^2-1).
$$
If $b>k_\ell$, the residual character $\bar\Psi$ has a separating element $x$ in the decomposition group at $\ell$ with $\eta_4(x)=\bar\epsilon_\ell(x)=1$ and $\bar\Psi(x)^2\ne1$. Here $\eta_4$ cuts out $K=\mathbf Q(i)$. The same data satisfy the three arithmetic hypotheses of the auxiliary-tower theorem (AT1), with modulus $\ell N$ and $F_b=\mathbf Q$. This criterion sharpens the sufficient dyadic conductor test in the original construction. [Original dyadic calculation][dyadic] · [Exact hypotheses of the auxiliary-field construction][tower]

Indeed the odd part of $\psi$ has exponent dividing $2o$. The four defining conditions for $E$ show this on units supported at each odd prime of $f$, where their $o$th powers fix $M$, and at $q,d$, where squares fix the quadratic subfields. Since $\ell$ is outside the modulus, $\psi$ is unramified there. Choose arithmetic Frobenius $s$ at $\ell$ with $\bar\epsilon_\ell(s)=1$ by adjusting it by inertia in the totally ramified extension $\mathbf Q_\ell(\mu_\ell)$. Its $\psi$-value is $\psi(\ell)$.

On $1+4\mathbf Z_2$, a character of exact conductor $2^b$ for $b\ge3$ has kernel $1+2^b\mathbf Z_2$. Indeed this subgroup of units modulo $2^b$ is cyclic, and primitivity excludes its unique subgroup of order two from the kernel. Factoring successive differences of squares, and observing that a final odd power preserves the valuation, gives
$$
 v_2(\ell^{4o}-1)=v_2(\ell^2-1)+1+v_2(o)=k_\ell.
$$
Thus $\psi_2(\ell)^{4o}\ne1$. All odd components disappear in the $4o$th power. Reduction is faithful on the prime-to-$\ell$ values, so $\bar\Psi(s)^4\ne1$. We may take $x=s^2$.

For the tower's remaining kernel test choose $u\in\mathbf Z_2^\times$ congruent to $-1$ modulo four with $\psi_2(u)=1$. Such a $u$ is $-v$, where $v\in1+4\mathbf Z_2$ maps to $\psi_2(-1)^{-1}$, since the image on $1+4\mathbf Z_2$ has order $2^{b-2}$. Inertia at two realizes $u$ on the dyadic roots and acts trivially on roots of odd order. This yields $\bar\epsilon_\ell=\bar\Psi=1$ and $\eta_4=-1$ there. Both residual characters factor through roots of unity of modulus dividing a power of $\ell N$, $\bar\Psi$ is even, its restriction at $\ell$ is $\bar\epsilon_\ell^e$, and $K$ is unramified there. Away from $\ell$ the inertia values of $\Psi$ have prime-to-$\ell$ order, so triviality after reduction implies integral triviality. This proves all three hypotheses directly, including when $2^b\le8o\ell^2$. [General fixed-order admission argument][admit] · [Original marked auxiliary field and seed condition][link]

<!--
% END RSC1
-->

## Integral length above the dyadic cutoff

<!--
% BEGIN RSC2
-->

<span id="claim:RSC2"></span>Use the external marked-frame arithmetic of the rank-three inertial comparison (DH2)–(DC9), including the auxiliary-field finite-point, automorphy, rigidity and Frobenius-spectrum results cited there. On this input, for the general host above and $b>k_\ell$, the original strict group satisfies
$$
  (\log\ell)\operatorname{length}_O\mathcal S(O,e,\psi)
          \le [N(e+1)]^{C_\chi}
$$
on all sufficiently late original windows. The transfer uses the proof of the inertial comparison at the actual character. Its stated conductor-one corollary has more restrictive hypotheses. Here are the arithmetic checks needed to run that proof. [Original inertial counting interface][count] · [External integral proof and the two types of points][dc]

1. On $\Gamma=G_{\mathbf Q,S}$ for $S=\{v:v\mid\ell N\}$, take $\eta=\eta_4$ and $N_v=I_v\cap\ker\eta\cap\ker\bar\Psi$ away from $\ell$. The set of places of nontrivial $\ell$-primary finite-character inertia is empty. The quotient $I_v/N_v$ has order prime to $\ell$ and $\Psi(N_v)=1$. At $\ell$ the element $x$ of RSC1 gives distinct residual diagonal characters $\bar\Psi(x),1,\bar\Psi(x)^{-1}$. On a nonzero adjoint weight $j=\pm1,\pm2$ its scalar $\bar\Psi(x)^j$ differs from one, also for the Tate dual because $\bar\epsilon_\ell(x)=1$. For weight zero, $K\cap\mathbf Q(\mu_\ell)=\mathbf Q$ gives the global Tate-dual vanishing. Thus the local lifting and Euler-characteristic calculation (DH4)–(DH5) has defects $0,-1,0,1,1$ in weights $-2,-1,0,1,2$. The Gaussian class group gives the unramified weight-zero rigidity and the class-one condition. For negative weights the rational strict vanishing applies on the finite field killing $\eta,\psi$, followed by restriction and corestriction. Finally $H^0(D_\ell,D)=H^0(\Gamma,D)=0$ by $x$. A strict class killed by $a_0\in O\setminus\{0\}$ therefore lifts uniquely at this coefficient modulus, is locally split at $\ell$, and is zero on $N_v$ elsewhere. This is the strict input to (DC9). [Cohomology of the frame][dh] · [Finite-modulus inclusion][dhmod]

2. Use the auxiliary tower, frame and seed with the hypotheses verified in RSC1. This supplies the same two marks for both ranks and the link on the same abelian CM field $L=L^+K$. The quotient kernel away from $\ell$ is killed by the inertial point since there $\Psi$ and $\bar\Psi$ have the same inertia kernel. Its ordered local flag has precisely the prescribed inertia characters. These are the conditions for its normalized lift (FE1). At a characteristic-$\ell$ DVR point the inertia characters on the residual kernel become trivial. Thus the finite-point and finite-end theorems used in (DU1) give the base characteristic polynomials on $G_L$, and the marked triangularity and integral finiteness argument applies to the weight-zero ring. At a two-sided characteristic-zero point the ordinary flag has exponents $(e,0,-e)$ and unramified finite factors at $\ell$. In both the rank-three irreducible case and the outer rank-two case, $x$ supplies the distinct residual eigenvalues in the strong irreducibility test. The two-sided classification uses the Gaussian class group to identify the unramified characters. The two normalized lifts receive the automorphic attachments, respectively over $K$ after descent and from the weight-$2e+1$ newform over $\mathbf Q$. For their tangents the positive Tate ratios and the unramified separation by $x$ give the crystalline local condition, and the finite inertia quotient gives the unramified condition elsewhere. These are the hypotheses of the type-I and type-II rigidity arguments. The integral count (DC5)–(DC9) treats both types and requires no residual vanishing in weight $-2$. [Two-rank frame and seed][admitend] · [Finite-point transfer][finite] · [Weight-zero finiteness and type I][du] · [Type II and its rigidity][dc2]

3. Choose two distinct fixed primes $p_1,p_2\ge7$ split in $K$ and prime to $30f$. Eventually both are below $q,d$. Use one different from $\ell$. Away from $\ell$ the rank-three inertia on $G_K$ factors through the finite character of modulus $N$. In rank two the extra factor is $\eta_4$, so modulus $4N$ suffices. At $\ell$ the prescribed ordinary exponents and the preceding crystalline comparison give the coefficient-place level condition. Consequently (SP3)–(SP6) bound the trace sum on the actual pairwise nonisomorphic points, using inverse Frobenius at the chosen split prime and the full orbit of $\psi(p)^{-1}$, of size at most $\varphi(N)$. The resulting bound for $(\log\ell)\sum v_\ell(\operatorname{tr}r_i-\operatorname{tr}r_0)$ is at most $C_K N[4N(e+1)]^{A_K}\max_j\log p_j$. The integral comparison (DC1), including the injection (DC9) at every modulus, multiplies this bound by at most $2e(O/\mathbf Z_\ell)=2$. The fixed constants can be absorbed into $C_\chi$. The allowed auxiliary fields and their class-rank bounds may vary with $\psi,\ell,e$ since neither enters this last exponent. [Spectrum and orbit bound][sp] · [Tangent, finite-modulus injection and normalization][dc9]

<!--
% END RSC2
-->

## The remaining field and its degree

<!--
% BEGIN RSC3
-->

<span id="claim:RSC3"></span>Write $N_{\rm odd}=N/2^{v_2(N)}$ and
$$
 F_\ell=E\cap\mathbf Q(\mu_{2^{\min(k_\ell,v_2(N))}N_{\rm odd}}).
$$
The low-dyadic part of $Q_{\ell,e}$ is canonically the parity-$(-1)^e$ strict group on $F_\ell$ modulo the invariants over $F_\ell\cap E_1$. Its order is bounded by the odd part of $|K_{2e}(\mathcal O_{F_\ell})|$. Moreover,
$$
 [F_\ell:\mathbf Q]\le4o\,2^{k_\ell-1},\qquad
 2^{k_\ell}\le4o(\ell+1).
$$
Indeed the dyadic conductor condition $b\le k_\ell$ is exactly factorization through $F_\ell$. The projector for $H=\operatorname{Gal}(E/F_\ell)$ is integral and commutes with those for parity and $G$. Restriction identifies the $H$-invariant strict group with the strict group on $F_\ell$ by local and global prime-to-degree descent. The image of $G$ there is $\operatorname{Gal}(F_\ell/(F_\ell\cap E_1))$. Duality followed by the number-ring comparison puts the dual strict group inside the indicated $K$-group at $\ell$. For the degree, write $\chi_{\rm odd}$ for the product of the character components of $\chi$ at odd primes. Its order divides $o$. By the Chinese remainder decomposition, every character of $F_\ell$ is a product of a character modulo $2^{k_\ell}$, a power of $\chi_{\rm odd}$ and characters of the two auxiliary quadratic fields. In fact the character group of a compositum is generated by the character groups of the factors. Restricting such a product to odd units gives the claimed odd components even if the dyadic factors cancel. This gives the degree bound. One of $\ell-1,\ell+1$ has 2-adic valuation one, so $2^{v_2(\ell^2-1)}\le2(\ell+1)$. [Descent through the strict local conditions][ets22] · [Strict dual and even $K$-group][ets15]

On the arithmetic input of RSC2, the total high-dyadic logarithmic order over all resonant $(\ell,e)$ is at most $(Nt)^{C'_\chi}$, since there are at most $t$ twists, $2t+1$ possible primes per twist, and $|\Delta|\le N$ characters. For the low-dyadic summands alone the following window estimate is independent of RSC2. For $e\le x^{\alpha\varepsilon}$, $2^{k_\ell}\le C_\chi x^{\beta\varepsilon}$ and $5\alpha+4\beta<4/5$, their **total** logarithmic order is $\le\exp(\delta x^\varepsilon)$ for every fixed $\delta>0$ on sufficiently late original windows. Apply [ETS36][ets36] with the degree above and $\log N=O_\chi(x^{\varepsilon/5}(1+\log^2x))$. Its exponent is $O_\chi(x^{(5\alpha+4\beta+1/5)\varepsilon}(1+\log^2x))=o(x^\varepsilon)$. Summing over $O(t^2)$ pairs adds $O(\log x)$ to this exponent. The high-dyadic polynomial bound also fits every such allowance. Hence on the stated arithmetic input **every** resonant quotient in the range $e\le x^{\alpha\varepsilon}$ is covered for $\alpha<4/45$, as $\ell\le2e+1$. If $\ell\equiv3,5\pmod8$, then $k_\ell=4+v_2(o)$ and the same conclusion holds for $\alpha<4/25$. At larger twists the residual estimate is needed only on the fields $F_\ell$ and with precisely the indicated invariant quotient. [Original cutoff and window size][ets37]

<!--
% END RSC3
-->

## A vanishing result at every twist in one resonant congruence class

<!--
% BEGIN RSC4
-->

<span id="claim:RSC4"></span>Suppose that $\psi$ factors through $M$, $\ell-1\mid e$ and $\psi(\ell)\ne1$. Then its strict group vanishes whenever $\ell\nmid h_M$, where $h_M$ is the ideal class number of $M$. For the finitely many possible remaining $\ell\mid h_M$ all these character contributions, summed through the full cutoff, fit $\exp(\delta x^\varepsilon)$ for every $\delta>0$ on a common choice of the original windows. In particular this treats the indicated Frobenius and twist conditions in original Case III: an odd-order character of $\Delta$ is trivial on $\operatorname{Gal}(E/M)$, a 2-group. This result is independent of the marked automorphic input.

Let $k$ be the residue field of $O$ and $\pi$ its uniformizer. The residual module $D[\pi]$ is $k(\bar\psi^{-1})$ because $\bar\epsilon_\ell^e=1$. The unramified residual character at $\ell$ takes a value different from one on Frobenius. This forces $H^0(\mathbf Q_\ell,D)=0$, since every nonzero invariant subgroup contains a nonzero element killed by $\pi$. It also forces $H^0(\mathbf Q,D)=0$. Thus a strict class killed by $\pi$ lifts uniquely to $H^1(\mathbf Q,D[\pi])$, and its lift vanishes locally at $\ell$. On restriction to $G_M$ the lift is a homomorphism to the additive group of $k$. Away from $\ell$, inertia over $M$ acts trivially even on $D$. The strict condition over $M$ makes the image of the cocycle there a coboundary in $D$, hence identically zero on inertia. It follows that the homomorphism factors through the ideal class group of $M$ (the odd prime also kills any issue at real places). Restriction on this residual $H^1$ is injective since $[M:\mathbf Q]=o$ is prime to $\ell$. We have embedded the $\pi$-torsion of the strict group into $\operatorname{Hom}(\operatorname{Cl}(M),k)$. If the latter vanishes, the entire torsion group vanishes. [Original inverse twist and strict kernel][strict] · [Prime-to-degree coefficient descent][ets39]

More generally, the same argument gives a class-number test for **every** host character in half of the resonant congruence classes. If $\ell-1\mid2e$ but $\ell-1\nmid e$, then $\bar\epsilon_\ell^e$ is the nontrivial quadratic character on inertia at $\ell$. The finite character $\psi$ is unramified there, so $H^0(\mathbf Q_\ell,D)=0$ automatically. Let $T$ be the fixed field of $\ker\bar\Psi$, and let $C$ be its ideal class group modulo the classes of the primes above $\ell$. Then
$$
 \mathcal S(O,e,\psi)[\pi]\ \hookrightarrow\
 \operatorname{Hom}_{\operatorname{Gal}(T/\mathbf Q)}
              (C,k(\bar\Psi^{-1})).
$$
Indeed $[T:\mathbf Q]$ divides $2\operatorname{ord}(\psi)$ and is prime to $\ell$. Over $T$ the residual cocycle is a homomorphism. On its inertia away from $\ell$, triviality of $\bar\Psi$ forces $\psi=1$ by faithful reduction and the cyclotomic character is unramified, so the integral cocycle condition still gives zero there. At the places over $\ell$ the lifted class was zero already. Global reciprocity therefore gives the indicated quotient of the class group, and restriction of a rational class is equivariant under the quotient Galois action. The same test holds in the other congruence class $\ell-1\mid e$ provided $\psi(\ell)\ne1$, with $T$ then the field of $\psi$. In the half-resonant case $T$ is contained in the compositum of that field with the quadratic subfield of $\mathbf Q(\mu_\ell)$. In particular the test at a given $(\ell,\psi)$ applies to all twists in the same residue class modulo $\ell-1$. The class numbers in this version can vary with $\ell$.

For the other primes, enlarge the fixed finite reference list of [TW8][tw8] **before** choosing $J,X_0$, by the primes $\ell\notin P_\chi$ dividing $h_M$, using the fixed datum $M(\mu_\ell)$ at each. The $\psi$-components in question are disjoint summands of the strict group over $M$ after extending scalars. For each $\ell$ on the enlarged list, restriction from $M$ to its TW8 reference layer has kernel of length at most the fixed constant $b_\ell$ of ETS22 per twist. Consequently the logarithmic order summed over all these primes and indices is at most
$$
 \sum_{\substack{\ell\mid h_M,\ \ell\notin P_\chi}}
 (\log\ell)\big[\exp(x^{4\varepsilon/5})+(t-1)b_\ell\big]
$$
with the sum restricted to odd primes. Its logarithm is $o(x^\varepsilon)$ whenever the sum is nonzero. At an overlapping prime include $M(\mu_\ell)$ and any previously needed fixed finite fields, including a previously specified finite layer, in the reference compositum. Restriction from any of these fields to the new reference layer has the same fixed-degree kernel bound. The vanishing assertion applies pointwise. The simultaneous estimate uses the enlarged list's choice of interval. [Fixed-degree kernel and reference-layer estimate][ets22] · [Window quantifiers and both conclusions][tw8]

<!--
% END RSC4
-->

[ets15]: EVEN_TWISTS_AND_RANK_THREE_AUTOMORPHY.md#claim:ETS15
[ets22]: EVEN_TWISTS_AND_RANK_THREE_AUTOMORPHY.md#claim:ETS22
[ets36]: EVEN_TWISTS_AND_RANK_THREE_AUTOMORPHY.md#claim:ETS36
[ets37]: EVEN_TWISTS_AND_RANK_THREE_AUTOMORPHY.md#claim:ETS37
[ets39]: EVEN_TWISTS_AND_RANK_THREE_AUTOMORPHY.md#claim:ETS39
[tw8]: ../../../research/modules/galois/simultaneous_cohomological_windows/main.tex#L825-L864
[cases]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AutomorphicArithmetic/AutomorphicVarieties/HeightAndVanishing/DirichletPrimeToLPartMulLPowerPart.lean#L164-L219
[dyadic]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AutomorphicArithmetic/AutomorphicVarieties/UnitaryThreeDeformations/DyadicCharacterPowerNeOne.lean#L50-L70
[link]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AutomorphicArithmetic/AutomorphicVarieties/CurveDVRSpecialization/HostFrameEx.lean#L22-L73
[count]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AutomorphicArithmetic/AutomorphicVarieties/UnitaryThreeDeformations/AbstractCount.lean#L25-L36
[strict]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AutomorphicArithmetic/AutomorphicVarieties/CharacterLevelBounds/ShaFamMono.lean#L15-L34
[tower]: https://github.com/JoseBrox/GRH_distillation/blob/cb86f1ca250903bd5930a3d2116c74344691e883/paper/shared/selmer-support-continuation-auxiliary-tower.tex#L22-L80
[admit]: https://github.com/JoseBrox/GRH_distillation/blob/cb86f1ca250903bd5930a3d2116c74344691e883/paper/shared/selmer-support-continuation-auxiliary-admission.tex#L10-L102
[admitend]: https://github.com/JoseBrox/GRH_distillation/blob/cb86f1ca250903bd5930a3d2116c74344691e883/paper/shared/selmer-support-continuation-auxiliary-admission.tex#L148-L164
[dh]: https://github.com/JoseBrox/GRH_distillation/blob/cb86f1ca250903bd5930a3d2116c74344691e883/paper/shared/rh-dyadic-host-frame.tex#L101-L214
[dhmod]: https://github.com/JoseBrox/GRH_distillation/blob/cb86f1ca250903bd5930a3d2116c74344691e883/paper/shared/rh-dyadic-host-frame.tex#L234-L256
[finite]: https://github.com/JoseBrox/GRH_distillation/blob/cb86f1ca250903bd5930a3d2116c74344691e883/paper/shared/selmer-support-continuation-finite-end.tex#L4-L33
[du]: https://github.com/JoseBrox/GRH_distillation/blob/cb86f1ca250903bd5930a3d2116c74344691e883/paper/shared/rh-dyadic-host-universal.tex#L35-L66
[dc]: https://github.com/JoseBrox/GRH_distillation/blob/cb86f1ca250903bd5930a3d2116c74344691e883/paper/shared/rh-dyadic-host-count.tex#L9-L36
[dc2]: https://github.com/JoseBrox/GRH_distillation/blob/cb86f1ca250903bd5930a3d2116c74344691e883/paper/shared/rh-dyadic-host-count.tex#L325-L485
[dc9]: https://github.com/JoseBrox/GRH_distillation/blob/cb86f1ca250903bd5930a3d2116c74344691e883/paper/shared/rh-dyadic-host-count.tex#L486-L600
[sp]: https://github.com/JoseBrox/GRH_distillation/blob/cb86f1ca250903bd5930a3d2116c74344691e883/paper/shared/selmer-support-continuation-spectrum.tex#L57-L99
