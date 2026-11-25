# The definite pairing on the marked fibres of period entry 7

Fix a fitted base-level definite layer, a serving tuple at a conjugate pair of places, and the actual full level lattice of coefficient-valued forms. Write $N$ for this lattice, $H$ for its class-sum pairing including $1/|P|$, $s$ for the selected inclusion, $p$ for its orthogonal coordinate projection, $T=pN$, and $D=\dim T_K$. Write $C=s^{-1}N$ for the selected dual Weyl cut, $C_\Delta$ for its Weyl cut, $a_w=[T:C]_w$, and $q_w=[T:T^\sharp]_w$. Work over the semilocal Dedekind ring at $w,\bar w$ before taking a length at $w$. Use the fitted geometric coefficient pairing on the unimodular class lattices. In particular the Hermitian dual of the dual Weyl lattice of each coefficient fibre is its Weyl lattice.

On this layer there is a module $U_w$, annihilated by the common stabilizer denominator, and an **exact equality**
$$
 q_w=a_w+[C:C_\Delta]_w+\operatorname{length}(U_w).
 \tag{1}
$$
The correction $U_w$ vanishes for every residue characteristic $l>2f(r+t)+1$. Moreover, if $l>\max_\tau(\lambda_{\tau,0}-\lambda_{\tau,r+t-1}+r+t-1)$, the two Weyl lattices coincide at $w$. On the sufficiently large prescribed weights both inequalities hold at $g_0,g_1$. It follows on **every layer, including the terminal one**, that
$$
                  q_w=a_w\qquad (w\mid g_0g_1).
 \tag{2}
$$
The marked-prime class form itself is unimodular even though $g_i\mid |P|$. There may still be a nonzero congruence length $a_w$ after the spectral projection.

## Mass weights on the rank-$r+t$ source

Let $K_P$ be the level whose first block reduces into $P$, and $K_1$ the kernel of the first-block reduction on that level. In the geometric marked realization the deck action on principal classes is through $K_P/K_1=P$. Surjectivity of reduction on this subgroup follows by lifting each upper unipotent matrix at the selected split prime as an integral upper unipotent matrix in the first block, using the identity in the complementary block and the inverse adjoint at the conjugate place. These local lifts define an adelic level element. The determinant character on the other blocks is incorporated in the coefficient transition. On a $K_P$-class write $\Gamma$ for its finite rational stabilizer. The stabilizer in $P$ of any principal class over it is the image of $\Gamma$, with kernel the principal class stabilizer. Indeed a right translation fixes the principal class precisely when it can be undone on the left by a rational isometry and on the right by $K_1$.

The group $\Gamma$ has a faithful rational representation of dimension $b_*=2f(r+t)$ by restriction of scalars. If an element has prime order $l$, its minimal polynomial contains $\Phi_l$, so $l-1\le b_*$. The base group $P$ is a product of upper unipotent groups at $g_0,g_1$. Both primes eventually exceed $b_*+1$. Thus the image of $\Gamma$ in $P$ is trivial and all its deck orbits are free. The complementary rank-$t$ Levi can retain rational stabilizers. Freeness concerns the finite deck action, so it does not require that Levi to have trivial stabilizers.

Each orbit in the full class sum now has $|P|$ terms of the same pairing value and the same stabilizer order $h_c$. Unitarity of the transport and of the character gives the first assertion. It is valid at every place because the original identity is algebraic. The level factor $1/|P|$ cancels exactly. Thus evaluation at one class in each orbit identifies the full level lattice and form with
$$
       N=\bigoplus_c A_c^{\Gamma_c},
       \qquad H=\bigoplus_c h_c^{-1}H_c ,
$$
where the action includes the level character, $A_c$ is the full dual Weyl fibre, $B_c=A_c^{\sharp,H_c}\subset A_c$ its Weyl fibre, and $h_c=|\Gamma_c|$. All transitions act by lattice isomorphisms. More generally the same class-sum formula follows without freeness from orbit–stabilizer, since summing $|P|/|\operatorname{im}\Gamma_c|$ terms weighted by $1/|\ker(\Gamma_c\to P)|$ also gives $1/|\Gamma_c|$ after division by $|P|$.

## The integral norm and the cut

Let $A=A_c$, $B=B_c$, $h=h_c$, and $e=h^{-1}\sum_{\gamma\in\Gamma_c}\gamma$, using the twisted action. The rational average is self-adjoint. Its use does not require $h$ to be invertible at $w$. The fixed lattice $A^\Gamma$ is saturated in $A$, so it is a direct summand over the semilocal ring. Every integral linear functional on it extends to $A$, including after conjugating the first variable. The ambient dual lattice $B$ represents all those extensions. Restriction to the invariant space with the unscaled form is represented by $eB$. Rescaling by $1/h$ therefore gives the exact dual lattice
$$
       (A^\Gamma)^{\sharp,H_c/h}=(he)B
       =\operatorname{Nm}_{\Gamma_c} B.
$$
In particular $h_c B_c^{\Gamma_c}\subset\operatorname{Nm}_{\Gamma_c}B_c\subset B_c^{\Gamma_c}$. Orthogonality of $s,p$ gives $T^\sharp=s^{-1}N^\sharp$: pairing with all $pn$ tests exactly pairing of the lift with all $n\in N$. Hence $T^\sharp\subset C_\Delta\subset C\subset T$. Define $U_w=(C_\Delta/T^\sharp)_w$. Evaluation injects this module into the direct sum of $B_c^{\Gamma_c}/\operatorname{Nm}_{\Gamma_c} B_c$ at $w$. Each summand is killed by $h_c$. Additivity of DVR lengths proves (1), with $0\le\operatorname{length}U_w\le D v_w(d_*)$ for any common stabilizer multiple $d_*$. This statement retains the positive sign of every term.

For $l>b_*+1$, Cauchy's theorem and the cyclotomic-degree argument give $l\nmid h_c$ for each class, so integral averaging kills $U_w$. The coarse Weyl inclusion at each embedding bounds the inclusion exponent by $\binom{r+t}{2}\lfloor\log_l(\lambda_{\tau,0}-\lambda_{\tau,r+t-1}+r+t-1)\rfloor$ before multiplying by the ramification index. Consequently both cuts coincide for $l$ above the displayed shifted spreads. On the design the relevant weight coordinates and shifts are bounded by a fixed polynomial in $x$ times $b^2$, whereas $b=\exp(x^\epsilon)$ and $g_i\ge(kb)^8$. This proves (2) without a prime-to-level assumption.

## An unconditional range for the Weyl correction

Set $L=x^\epsilon$, $b=\exp L$, $X'=\exp(L^{1/3})$, and $P_b=b/\sqrt{X'}$. Let $J_{\tau j}(l)$ be the single-factor Weyl inclusion exponent before multiplying by the ramification index. The full exponent is at most the sum over embeddings, by scaling each factor of the tensor product on each class. Cutting to a subspace preserves the same inclusion. With $N_*=r+t$ and shifted spread $H_{\tau j}=\max(1,\lambda_{\tau,0}-\lambda_{\tau,N_*-1}+N_*-1)$, the coarse bound is
$$
 J_{\tau j}(l)\log l\le \binom{N_*}{2}\log H_{\tau j},
 \qquad J_{\tau j}(l)=0\quad(l>H_{\tau j}).
$$
The design gives $\log H_{\tau j}=O(L+\log x)$, polynomially many labels and layers, and a polynomial bound on rank. Every twisted partial fibre has $\sum_{w\mid l,w\in{\rm Tw}}\ell_w e_w\le \log l$. Summing this coarse estimate over all $l\le P_b$ therefore costs at most $P_b$ times a fixed polynomial in $x$, which is $o(b)$. At any fixed bounded number of additional distinguished primes per layer the same estimate costs only a polynomial in $x$, regardless of the sizes of those primes. For non-thick labels the actual width bounds imply $J_{\tau j}(l)=0$ for $l>2b'=2xb/X'$. A larger cutoff can be used with an explicit cost. Write $R_b=\sum_{j,\tau}\binom{N_*}{2}\log H_{\tau j}$ and $P_b^+=b/[x(1+R_b)]$. The contribution from characteristics at most $P_b^+$ is at most $P_b^+R_b\le b/x$. Since $R_b$ is polynomially bounded, eventually $2b'<P_b<P_b^+$. Thus the whole Weyl correction at all small primes, all non-thick factors, and the at most four individual primes $q,d,p_{\rm de},p'_{\rm de}$ per layer costs $o(b)$ without a Hida-model comparison. Equivalently the exact length $[C:C_\Delta]_w$ at the remaining primes is supported solely on thick factors at $P_b^+<l\le\max_{\tau\ {\rm thick}} H_{\tau j}$. This statement bounds $q_w-a_w$ in the indicated range. A large congruence length $a_w$ would still enter $q_w$ with coefficient one.

## Using the denominator budgets

The exact identification with the original first-pass and exponent quantities is
$$
 a_w=\mathrm{etaW}(w),\quad
 J_w=\exp_w(C/C_\Delta)=e_wJ_0(t_w,w,j).
$$
Thus (1) gives $a_w\le q_w\le a_w+D(J_w+v_w(d_*))$. The common $d_*$ can be taken independent of the serving tuple: every stabilizer of every layer embeds in $\mathrm{GL}_{b_*}(\mathbb Q)$. It preserves an integral lattice and injects modulo 3. For the last assertion a finite-order matrix in the level-3 kernel would have an element of prime order; if $X=1+3^aY$ with $Y\not\equiv0\pmod3$, then $X^l-1$ has 3-adic matrix valuation $a$ for $l\ne3$, and $a+1$ for $l=3$, by expansion. Hence $d_*=|\mathrm{GL}_{b_*}(\mathbb F_3)|$ suffices, and $m\log d_*=O(m b_*^2)=o(b)$ on the polynomial-rank family. This witness is only needed for the global upper bound. For local vanishing use the individual stabilizer orders, since $d_*$ can contain needless large primes.

The normalized sum of $q_w$ at all serving twisted places is absorbed by the original two allowances whenever the fitted first-pass division estimate and the short-weight exponent bounds of B8.38b apply to this member:
$$
 \sum_j\sum_{w\in\mathrm{Tw}}\ell_w q_w/D
 \ \le\ \sum_j\sum_{w\in\mathrm{Tw}}\ell_w(a_w/D+e_wJ_{0,j,w})+o(b).
$$
With the cited allowances this is $O(mL(B_0+N_c))$. On the two marked fibres only the actual first-pass lengths are needed, and their twisted partial sum is bounded by the full nonnegative first-pass sum. This is a transfer onto the same definite row and a genuine marked-fibre equality. The coarse global inequality itself is already present in the roadmap, with an extra level-order denominator. An application of the sharp exponent outside the marked fibres still needs the selected member's Hida-model covering and exponent input. The formula gives no bound for the raw archimedean theta determinant or its change between the two selection primes. In particular the identity cover used to construct the preliminary top datum is replaced at every active layer by a cover with the run's own prime, a prescribed character, and a nontrivial character witness at full weight.

[Class forms and stabilizer weights](https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Formalism/LocalToGlobal/Divisibility/ClassSum.lean#L47-L101). [The first-block unipotent subgroup, the level map, and the complementary Levi](https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Formalism/LocalToGlobal/Divisibility/DefGroup.lean#L600-L698). [Lift-level subgroup at rank (r+t)](https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Formalism/LocalToGlobal/Divisibility/DefGroup.lean#L791-L817). [Mutual duality with the dual base lattice](https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Formalism/LocalToGlobal/Divisibility/CoefModLemmas.lean#L142-L148). [Orthogonal coordinates and both cuts](https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Formalism/LocalToGlobal/Divisibility/LiftLat.lean#L192-L216). [Serving tuple for the short exponent](https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AbelianVarietyTheory/Proofs/DivisorProofs/ExpansionOfNumericsModel.lean#L45-L76). [The earlier coarse pairing estimate](https://github.com/rh-lean-roadmap/rh-lean-roadmap/blob/02a95b4c62db610642af5f278ee5d0d6df87b348/docs/src/book/main.tex#L32958-L32978). [The selected exponent model and prime sum](https://github.com/rh-lean-roadmap/rh-lean-roadmap/blob/02a95b4c62db610642af5f278ee5d0d6df87b348/docs/src/book/main.tex#L54203-L54217). [Own-prime covers in the two completed runs](https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AbelianVarietyTheory/Proofs/HeightProofs/ExistsFullDataExtension.lean#L18-L54).
