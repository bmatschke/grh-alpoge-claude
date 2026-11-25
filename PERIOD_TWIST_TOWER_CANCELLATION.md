# An upper bound for the twisted Fourier denominators by cancelling the tower factors

For the glued base row in frame entry 2, the local square-tower calculation needs only upper bounds for a particular list of positive critical Hecke ratios. Its negative-valuation estimates for the varying twists, including the separate partial-zeta denominator at the residue prime, drop out. This follows by combining the definite bottom norm with the entire tower identity before estimating their valuations. The result below applies on a fitted grid and also specifies weaker sufficient input on a selected row for which the full grid comparison has yet to be established. [Base evaluation and the remaining lattice comparison](PERIOD_REFERENCE_EVALUATION.md) · [Original square estimate][square]

## Exactly which critical values survive

Fix a layer pair $(i,j)$ and a finite coefficient place $w$ at which the serving tuple $\tau$ differs from the reference tuple $0$. Write $v=v_w$, normalized to have value one on a uniformizer. Use the source's ranks
$$
 y=m-1-j,\quad p=\lfloor y/2\rfloor,\quad q=y-p,\quad
 e_0=e+q-p,\quad h_0=h-y,\quad h=h_{ij}.
$$
Here $e$ is half the difference of the two upper row ranks; $0\le e\le e_0<h_0$ and $e+q\le h$. Let $\rho_s=\Lambda_\tau(s)/\Lambda_0(s)$ in its algebraic reading for $1-e_0\le s\le h$. The factors in the tower are nonzero. At the places in use the twist conductor is a unit, so the Hecke functional equation gives $v(\rho_s)=v(\rho_{1-s})$ for $1-e_0\le s\le0$. [Rank comparison and index ranges][rank] · [Reflection with its unit factor][reflect]

Let $A,A'$ be the norms of the two reference definite theta pairs on this square, $d(w)\ge0$ the coordinate denominator allowance, $\gamma$ the relative definite bottom constant, and $r_{ij,\tau}$ the relative upper square constant. The norm identity on the large definite bottom and the bottom-constant comparison give
$$
 v(\gamma)\le v(AA')+\sum_{s=1-e_0}^{h_0} v(\rho_s)+6d(w).
$$
The same reference normalization, period and two-torsion point occur on each side. They are essential here since the comparison is between the actual values of the two norms. Write $C_w=\sum_{a\in S_0}c_a v(N\mathfrak q_a)$ for the conductor contribution of the fixed evaluation grid. Each normalized step factor $t_k$ is a unit times a product of quotients of two integral divisors of $(N\mathfrak q_a)^{c_a}$. Their valuations both lie in the interval $[0,c_a v(N\mathfrak q_a)]$, so $|v(t_k)|\le C_w$. With $X_s=v(\rho_s)$ the tower identity therefore gives
$$
 v(r_{ij,\tau})\le v(\gamma)+yC_w+
      \sum_{s=e_0+1}^{e+q}X_s-\sum_{s=e+1}^{e+q}X_s .
$$
The positive numerator interval has length $p$; when $p=0$ it is empty. The reference tuple has $r_{ij,0}=1$. [Norm identity and bottom constant][bottom] · [Actual normalized tower and its step divisors][tower] · [Original statements for both comparisons][native]

Reflection rewrites the bottom sum as $\sum_{s=1}^{h_0}X_s+\sum_{s=1}^{e_0}X_s$. The difference of the two tower intervals equals $\sum_{s=1}^{e}X_s-\sum_{s=1}^{e_0}X_s$. Hence
$$
 \boxed{\displaystyle
 v(r_{ij,\tau})\le v(AA')+6d(w)+yC_w+
       \sum_{s=1}^{h_0}v(\rho_s)+\sum_{s=1}^{e}v(\rho_s).}
 \tag{1}
$$
This includes $y=0$ and $q=p+1$. Every surviving Hecke valuation has positive coefficient. In particular the estimates for $-v(\rho_s)$ and their counts $N_0(i,j,s,\ell)$ used in the general absolute-value estimate are unnecessary for (1). Nonvanishing and the exact tower and norm identities remain hypotheses. As an independent check on endpoint conventions, direct integer multiplicity counts agree for all 7,635 choices with $0\le e<15$, $0\le y<30$ and $\max(2,e_0+1)\le h_0\le e_0+17$. The interval calculation proves the formula for every admissible rank. The absolute height of each fixed prime-twist comparison can still use arithmetic denominator estimates in its own proof. [Earlier cancellation of the top ratios on an untwisted tower](ROW_GRID_PRODUCT.md)

## Sum on the original serving places

Put $\ell_w=\log Nw/[K:\mathbf Q]$. Suppose the reference numbers obey $v_w(A),v_w(A')\ge-3d(w)$, $\sum_w\ell_wd(w)\le D_0$ and the means of $\log^+|\sigma A|,\log^+|\sigma A'|$ are at most $A_0$. B8.21l supplies these estimates on its prescribed data. The function $v_w(AA')+6d(w)$ is nonnegative **at every place**. Summing it on the changed subset costs at most its full sum, at most $2A_0+6D_0$ by the product formula. This keeps its signed valuations. [Bottom number and denominator allowances][budgets]

For each surviving $s$, put $z_c=\Lambda_{\delta_c}(s)/\Lambda_0(s)$ for the two fixed prime twists. Take from the twisting comparison just the upper half
$$
  v_w(\rho_s)\le v_w(z_{c(w)})+v_w(\ell)/\ell^2,\qquad \ell=\operatorname{char} k(w).
 \tag{2}
$$
It suffices on the changed places. On the fitted data the source picks $\delta_{c(w)}$ so its conductor is a unit there. When applying (2) using the selected point's twisting tests, the local character and abelian layer labels for these $(i,j,s)$ must be those of the actual grid. The coprime-power tests then control the choice of primitive root. More generally (1) permits the bound for the signed *sum* of the surviving terms even without a bound for each term. [Choice and matching at the changed places][fitting] · [Source of (2)][upper]

For the reference value $1$ and each $z_c$, B8.21a supplies the same shift $g(w)$ with each of $\sum\ell_w|g(w)|,\sum\ell_w|v_w(z_c)+g(w)|$ at most $B_0$. At each changed place use $v_w(z_{c(w)})\le|v_w(z_{c(w)})+g(w)|+|g(w)|$. Partition the first sum into the two possible fixed prime twists, and sum the second just once. The resulting bound is $3B_0$ regardless of how many different serving tuples occur. The degree formula gives $\sum_{w\mid\ell}\ell_wv_w(\ell)=\log\ell$ and $\sum_{\ell\ {\rm prime}}(\log\ell)/\ell^2<1$, as follows by splitting off the terms $2,3,4$ in the sum over integers and integrating from $4$. Also $\sum_w\ell_w C_w=\sum_{a\in S_0}c_a\log N\mathfrak q_a\le\Sigma_0$. With $r_{\mu(w)}=\prod_{i,j}r_{ij,\mu(w)}$ this gives the family bound
$$
 \sum_w\ell_w v_w(r_{\mu(w)})\le
 G^+ :=\sum_{i,j}\left(2A_0+6D_0+(h_0+e)(3B_0+1)+y\Sigma_0\right).
 \tag{3}
$$
In (3) $h_0,e,y$ take the values for the summand's square. A coarser uniform upper bound is $m^2[2A_0+6D_0+2N_*(3B_0+1)+m\Sigma_0]$. [Height of the two fixed prime-twist ratios][probes] · [Prime-degree estimate][primes] · [Definitions of $A_0,D_0$ and $B_0$][budgets]

## Applying the bound to the glued row

Let $\Psi$ be the injection constructed on the reference row, with ordinary evaluation matrices $V_t$ on each used tuple. Suppose the Fourier and square identities identify $\Psi\iota_tP_t=r_t^{-1}V_t$ up to valuation units, and the finite sum estimate gives $V_{\mu(w)}(M_{\mu(w),w})\subseteq\mathfrak p_w^{-d_F(w)}M_w$, with $2\sum_w\ell_w d_F(w)\le B_F$. These comparisons are at the same places and in the same target as the reference evaluation. Since $RR_w=\iota_{\mu(w)}P_{\mu(w)}M_{\mu(w),w}$, (3) gives
$$
 \mu_{\max}(RR)+\langle\log\kappa\rangle_\infty
       \le \mu_{\max}(M)+H_I+B_F+2G^+ .
$$
Here $H_I$ is the squared-norm archimedean height bound for $\Psi$ with the row metric divided by $\kappa$. One applies the determinant bound to every rational subspace. Negative local exponents are permissible in the fractional target ideal. This route controls the image of the actual glued row under the fixed injection. It does not require a bound on the relative elementary divisors of the *preimage* lattices. On the B8.22 size range the right side is $O(x^A b)$: $h_0+e\le2N_*$, and (3) is dominated by the source's existing budget with $B=\max(A_0+6D_0,B_0)$. Indeed $2A_0+6D_0\le2B$ and $6N_*B_0\le 6N_*B$. Use its ordering of thresholds: first the allowed $C_F$ and $\varepsilon$ and outer size thresholds, then the eligible family, then $C_1$ exceeding its joint constant, then a common $x_0$ before the member, word, tuple and place. The [sharp-row transfer](PERIOD_SHARP_ROW_TRANSFER.md) and [divided-column estimate](PERIOD_DIVIDED_COLUMN_UPPER.md) then complete the frame at a sufficiently large permitted middle exponent. [Fourier identities and lattice inclusions][maps] · [Numerical bounds and order][order]

For a further field relaxation, suppose the upper and bottom numbers are available in a finite extension $L/K$. Keep the original $K$-linear $\Psi,\iota_tP_t,V_t$. For a used tuple mapping onto a positive-dimensional row, $V_t=z_t\Psi\iota_tP_t$ over $\mathbf C$ determines $z_t\in K^\times$ once both maps over $K$ are identified and $z_t\ne0$: divide any pair of corresponding entries with nonzero denominator. The individual square factors can be read in $L$. If the bottom comparison, reflection, step-unit and upper estimates (2) hold at the places of $L$ above the original serving places, for the pullbacks of those same choices, perform (1)–(3) over $L$. For a rational scalar $z_t$ and each original $w$ one has
$$
 \sum_{w'\mid w}\frac{\log Nw'}{[L:\mathbf Q]}\,v_{w'}(z_t)
           =\ell_w v_w(z_t).
$$
This proves (3) for the original lattice without constructing a new selected arithmetic point over $L$. Only the auxiliary numbers were adjoined. This field relaxation requires control of the stated inequalities at the prolonged places used in the normalized sum; a bound at one arbitrary prolongation does not in general control the sum. Algebraicity of the auxiliary ratios and reference CM norms on a fixed permitted grid follows from the CM theorem and definite-coordinate calculation. It does not identify the abelian list, the evaluation field, or the serving comparisons on every selected member. The [selected-family proof](PERIOD_SELECTED_BASE_FUNCTIONAL.md) identifies the common grid and the serving comparisons on the original selector under its stated inputs. [Algebraicity on a given grid][algebraic] · [Selected row conditions](PERIOD_REFERENCE_EVALUATION.md)

There is also a single-prolongation version. Suppose $z_t$, both reference bottom numbers $A,A'$, and both fixed probes $z_c(s)$ lie in $K$, and the coordinate allowance at the chosen $w'\mid w$ is at most $e(w'/w)d(w)$. The conductor and rational-prime allowances already scale by $e(w'/w)$. Then it suffices to prove the bottom, tower, and upper comparisons for **one** prolongation of each changed $w$, chosen jointly for these identities. Substitute (2) in (1), divide the entire inequality by $e(w'/w)$, and sum it on the original $K$-places using the $K$-budgets. The unit phase in the total scalar comparison must have zero valuation at the chosen prolongations. Only the fully varying ratios and the factors of the tower have been adjoined here. In particular no bound on their extension degree is needed. If the fixed probes and bottom numbers also require a larger field and one prolongation per place suffices for the local identities, there is an explicit fallback: after dividing by $e(w'/w)$, a selected nonnegative summand with weight $\ell_w$ is at most $[L:K]$ times its weight in the normalized full $L$-sum, since $e(w'/w)f(w'/w)\ge1$. Apply this to the nonnegative bottom majorant and to the shifted probe absolute values. Only $2A_0+6D_0$ and $3B_0$ in (3) pick up this degree factor. An eligible family-uniform polynomial bound on this degree therefore still gives a polynomial row-height estimate with a correspondingly larger permitted exponent. No such degree bound is assumed for the selected points in this note.

## Common bottom witnesses and rational comparison of their integrals

For a fixed admissible grid, the two source pairs in every reference square can use one CM period and one two-torsion point. Choose a discriminant twelfth-root period $\delta$ for $\mathcal O_{K_d}$ and an unkilled two-torsion point $t_0$ for its period lattice before choosing the square. Fix $(i,j)$, with bottom ranks $a_+,a_-$ and even target rank $a_++a_-$. The grid supplies unitary Hecke characters with finite components $\beta^{-1}$ on the larger source, $\alpha$ on the smaller source, and $\nu_0^{-1}$ on the common target. The target infinity exponents are at least $a_++a_-$. The two split auxiliary primes are prime to $Q_S q$. The grid conductor $\mathfrak m_E$ and its conjugate are consequently prime to the relevant half-different, using also the coprimalities in the grid definition. These are precisely the two coprimalities needed to form the standard pairs. [Joint witness and conductor checks][pair-joint]

On each side use the vacuum for $(\delta,t_0)$ and these characters to define the finite Weil action. The even target rank gives the parity condition for both vacua. On the larger side form the sum of the integral compact translates of the standard coset vector over representatives modulo its principal congruence group. Use modulus $\mathfrak m_E$ and block offset zero. On the smaller side use the conjugate modulus and offset $a_+$. The principal congruence fixes the respective vector, so the translate sums are independent of the representatives. The level character of the target is trivial on the prescribed congruence units. The block stabilizer thus acts by its prescribed unit scalar, and both vectors give pairs at the grid level $Q_{\rm lev}$. Their characters and ranks give the required reference pair. Repeating this construction with the already fixed $(\delta,t_0)$ works on every square. The norm nonvanishing and valuation estimates are the separate definite-integral comparisons used in (1). The further claim that the resulting norms can be chosen in the *selected* field uses B8.20's square-field condition. [Larger-side pair][pair-large] · [Smaller-side pair][pair-small] · [Where v36 uses the field condition][pair-field]

There is a finite-dimensional descent argument for the comparison of the bottom constants, even when the full polynomial test spaces are infinite-dimensional. Suppose the common-quotient identity in B8.21n holds on the chosen square. Write $p,p'$ for the maps of the two polynomial test spaces into a common complex quotient, with $p$ surjective and $p'\ne0$, and write $J_t$ for its injective realization as functions at tuple $t$. Suppose the two sides have periods $\Omega,\Omega'\ne0$ independent of $t$, with all monomial evaluations at finite adelic target points in $\Omega K$ and $\Omega'K$, respectively. The precise separation requirement is that these finite evaluations distinguish the functions in the finite span used below. In the definite model this follows from continuity, automorphic invariance and density of rational unitary points at infinity. Indeed one may vary the finite argument freely when left-translating a rational element, then pass to a limit in the real argument. The original definite-evaluation lemma gives exactly this implication. [Simultaneous factorization][factor] · [Finite-point determination on the definite model][finite-determination]

Choose a primed monomial $P'$ with $p'P'\ne0$. By surjectivity and the monomial spanning property there are unprimed monomials $P_1,\ldots,P_d$ with independent $pP_j$ and coefficients $a_j$ for which $p'P'=\sum_j a_jpP_j$. Define $f_{t,j}=I_t(P_j)/\Omega$ and $g_t=I'_t(P')/\Omega'$. The factorization $I_t(P)=\lambda_t J_t(pP)$ and $I'_t(P')=J_t(p'P')$ with $\lambda_t\ne0$ gives
$$
g_t=\sum_{j=1}^d b_{t,j} f_{t,j},
\qquad b_{t,j}=\frac{\Omega}{\Omega'\lambda_t}a_j.
$$
The evaluations of $(f_{t,j})_{j=1}^d$ at finite target points span the dual of this $d$-dimensional space. Otherwise a nonzero linear combination would vanish at every finite point, contradicting separation and injectivity. Select $d$ target points whose evaluation rows are independent. The resulting system for $b_{t,j}$ has an invertible matrix over $K$ and right side over $K$. Hence all $b_{t,j}$ lie in $K$. For any one $j$ with $a_j\ne0$, the same $j$ works at every tuple and
$$
\lambda_t/\lambda_0=b_{0,j}/b_{t,j}\in K^\times .
$$
This derives the arithmetic ratio from the actual monomial evaluations on both sides. It does not supply the original two rational period models. [Original arithmetic-ratio lemma][ratio-proof]

[pair-joint]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AbelianVarietyTheory/Proofs/DivisorProofs/ExistsIsBottomOfIsCoprime.lean#L23-L43
[pair-large]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AbelianVarietyTheory/Proofs/DivisorProofs/ExistsBottomPairBigMemberReferenceTuple.lean#L43
[pair-small]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AbelianVarietyTheory/Proofs/DivisorProofs/ExistsBottomPairSmallMemberReferenceTuple.lean#L28
[pair-field]: https://github.com/rh-lean-roadmap/rh-lean-roadmap/blob/02a95b4c62db610642af5f278ee5d0d6df87b348/docs/src/book/main.tex#L48865-L48872
[factor]: https://github.com/rh-lean-roadmap/rh-lean-roadmap/blob/02a95b4c62db610642af5f278ee5d0d6df87b348/docs/src/book/main.tex#L48825-L48837
[finite-determination]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AbelianVarietyTheory/Proofs/TwistedOperators/ContinuousAutomorphicEqZeroOfVanishOnFiniteAdeliStatement.lean#L11-L12
[ratio-proof]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AbelianVarietyTheory/Proofs/TwistedOperators/RatInOfDefinite.lean#L93-L170

[square]: https://github.com/rh-lean-roadmap/rh-lean-roadmap/blob/02a95b4c62db610642af5f278ee5d0d6df87b348/docs/src/book/main.tex#L19297-L19320
[rank]: https://github.com/rh-lean-roadmap/rh-lean-roadmap/blob/02a95b4c62db610642af5f278ee5d0d6df87b348/docs/src/book/main.tex#L48306-L48318
[reflect]: https://github.com/rh-lean-roadmap/rh-lean-roadmap/blob/02a95b4c62db610642af5f278ee5d0d6df87b348/docs/src/book/main.tex#L48347-L48367
[bottom]: https://github.com/rh-lean-roadmap/rh-lean-roadmap/blob/02a95b4c62db610642af5f278ee5d0d6df87b348/docs/src/book/main.tex#L48376-L48395
[tower]: https://github.com/rh-lean-roadmap/rh-lean-roadmap/blob/02a95b4c62db610642af5f278ee5d0d6df87b348/docs/src/book/main.tex#L48397-L48429
[budgets]: https://github.com/rh-lean-roadmap/rh-lean-roadmap/blob/02a95b4c62db610642af5f278ee5d0d6df87b348/docs/src/book/main.tex#L19505-L19516
[fitting]: https://github.com/rh-lean-roadmap/rh-lean-roadmap/blob/02a95b4c62db610642af5f278ee5d0d6df87b348/docs/src/book/main.tex#L19092-L19102
[upper]: https://github.com/rh-lean-roadmap/rh-lean-roadmap/blob/02a95b4c62db610642af5f278ee5d0d6df87b348/docs/src/book/main.tex#L48332-L48346
[probes]: https://github.com/rh-lean-roadmap/rh-lean-roadmap/blob/02a95b4c62db610642af5f278ee5d0d6df87b348/docs/src/book/main.tex#L18929-L18942
[primes]: https://github.com/rh-lean-roadmap/rh-lean-roadmap/blob/02a95b4c62db610642af5f278ee5d0d6df87b348/docs/src/book/main.tex#L49026-L49035
[maps]: https://github.com/rh-lean-roadmap/rh-lean-roadmap/blob/02a95b4c62db610642af5f278ee5d0d6df87b348/docs/src/book/main.tex#L19470-L19485
[order]: https://github.com/rh-lean-roadmap/rh-lean-roadmap/blob/02a95b4c62db610642af5f278ee5d0d6df87b348/docs/src/book/main.tex#L49048-L49087
[algebraic]: https://github.com/rh-lean-roadmap/rh-lean-roadmap/blob/02a95b4c62db610642af5f278ee5d0d6df87b348/docs/src/book/main.tex#L47959-L47976
[native]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AbelianVarietyTheory/Statements/PlaceShiftStatements/NormSmall.lean#L114-L151
