# Finite derivative valuations at one inert prime

Fix the ordinary branch at an inert prime in the range of the integral theta-kernel theorem, write $v(p)=1$, and index the embedding positions by $s$ modulo $2\nu$. At a marked position (a top) let $\alpha_s$ be the number of marked one-box columns. At each position let $w_s$ count the remaining determinant minors, and let $\lambda_s$ be their total number of boxes. The ordinary valuation bound admits a finite calculation which keeps track of the fact that different odd powers of Frobenius use degrees of the same derivative.

In a fixed integral frame the derivative has symbol
$$
 E=\prod_{s,b}\Big(\sum_a\xi_{s,a}X_{s,a,b}\Big)^{e(s,b)}Q(X),
 \qquad \alpha_s=\sum_b e(s,b),
$$
where $Q$ is the product of the remaining minors. Take $\varpi^{p^2-1}=p$. Write $y$ for the variables describing the integral frame. The local input is Adriazola's rescaled kernel condition $\Theta(\varpi X)=\sum_{j\ge0}p^{-j}h_\upsilon^j U_j$, with the specified kernel $h_\upsilon$ and integral $U_j$. The pairing with $E$ evaluates $E(\partial)\Theta$ at the origin. Write $\gamma_p=p/(p^2-1)$. For $\operatorname{lg}_p(k)$ the base-$p$ digit count, with value zero at $k=0$, the published factorial error is
$$
 \Delta=\sum_s\{r_1\operatorname{lg}_p(\alpha_s)+r_0r_1\operatorname{lg}_p(\lambda_s)\}
       +\sum_{s\text{ a top}}\operatorname{lg}_p(\alpha_s)^2,
$$
where $r_0,r_1$ count the row and column labels of $X_s$. [Integral kernel and valuation theorem](https://github.com/jimjamzola/RH-Alpoge-Reconstruction/blob/9eefc08b0819728d4dd2ef0568b49a61251af111/manuscript/sec8_gain.tex#L137-L193)

## A common degree bound for the marked derivatives

 For each top $s$, let $D_s$ be the set of least positive residues of $s'-s$ for tops $s'$ of opposite parity. For positive odd $d$ put $c_{s,d}=+\infty$ if $d\in D_s$, and $c_{s,d}=w_{s+d}$ otherwise. Only the position subscript $s+d$ is read cyclically in the second rule. Define
$$
 N_s=\max\left\{\sum_{d\text{ odd}} n_d:\ n_d\in\mathbf Z_{\ge0},\quad
 n_d\le c_{s,d},\quad\sum_{d\text{ odd}} p^d n_d\le\alpha_s\right\}.
$$
Every frame coefficient of the unscaled pairing satisfies
$$
 v\bigl([y^\mu]\langle E,\Theta\rangle\bigr)
 \ \ge\ \sum_{s\text{ a top}}(\gamma_p\alpha_s-N_s)-\Delta.
$$
Here the frame variables may equivalently be regarded as the generic integral coordinates used to prove Adriazola's coefficient estimate.

Make the substitutions $X_{s,a,b}\mapsto X_{s,a,b}+\xi_{s,a}t_{s,b}$ at the tops. The coefficient of $t^e$ extracts the marked derivatives after multiplication by $e!$. In the integral kernel expansion the terms that still cost one unit of valuation after the factorial estimate come in two forms. A mixed term uses $t_{s,b}^{p^d}$ and a linear form at $s+d$. A pure term joins two opposite-parity tops. Charge each such term once to the endpoint bearing the larger Frobenius exponent. If the shifts at its endpoints are $a>a'\ge0$, the larger endpoint plus $a$ equals the other endpoint plus $a'$ in the cycle. The least positive distance $d$ from the chosen endpoint to the other therefore satisfies $d\le a-a'\le a$. This occurrence consumes at least $p^d$ units of $t$-degree at the chosen endpoint. The charged mixed and pure occurrences are disjoint. If $n_{s,d}$ counts those charged at a top and distance, then in the *same* nonzero summand
$$
 \sum_d p^d n_{s,d}\le\sum_b e(s,b)=\alpha_s.
$$
Indeed the entire product of these $t$-monomials divides $t^e$. This is the coordinatewise inequality in Roadmap Theorem B3.21, summed over labels $b$ after each pure occurrence has been assigned once. [Common valuation and coordinatewise degree inequality](https://github.com/rh-lean-roadmap/rh-lean-roadmap/blob/c7755c1086f05d0918ee8496d95912e4f35e22f9/docs/src/book/main.tex#L4635-L4679) · [Assignment of the pure factors](https://github.com/rh-lean-roadmap/rh-lean-roadmap/blob/c7755c1086f05d0918ee8496d95912e4f35e22f9/docs/src/book/main.tex#L29314-L29357)

If $d\notin D_s$, only mixed factors are charged. At fixed $s,d$ their directions translate the matrix at $s+d$ by $\eta(\tau_b)_b^{\mathsf T}$, where $\eta_a=\xi_{s,a}^{p^d}$ is independent of $b$. Any determinant has total degree at most one in the $\tau_b$, since the term obtained by replacing two columns has proportional columns. This remains true in the presence of the other translation parameters by taking their polynomial ring as the ground ring. Hence the product of the $w_{s+d}$ partner minors has degree at most $w_{s+d}$. A nonzero coefficient satisfies $n_{s,d}\le w_{s+d}$. This explains why the allowance counts minors irrespective of their heights. Legendre's factorial estimate, after undoing the rescaling by $\varpi$, gives $\sum_s\gamma_p\alpha_s-\sum_{s,d}n_{s,d}-\Delta$. Applying the joint degree bound to that expression proves the displayed inequality. [Kernel expansion, digit error, and determinant argument](https://github.com/jimjamzola/RH-Alpoge-Reconstruction/blob/9eefc08b0819728d4dd2ef0568b49a61251af111/manuscript/sec8_gain.tex#L210-L265)

One computes $N_s$ by filling capacities in increasing odd $d$, stopping when the next occurrence exceeds the remaining degree. Among all choices of $k$ occurrences, the $k$ cheapest have the smallest total cost. In particular $N_s\le\lfloor\alpha_s/p\rfloor$, so the gross gain at a top is at least $\alpha_s/[p(p^2-1)]$. Also $N_s\le\sum_d\min(c_{s,d},\alpha_s/p^d)$. Using $\sum_{d\text{ odd}}p^{-d}=\gamma_p$ recovers the usual positive-part formula. For example, take $p=5,\alpha_s=250,D_s=\varnothing$ and $w_{s+d}=48$ at every odd translate. The ordinary positive-part sum is $2$. The first 48 occurrences cost 240 in the joint count. A further occurrence costs at least 125, so $N_s=48$ and the gross bound is $625/12-48=49/12$. Both bounds are before the same digit loss. The joint calculation is an arithmetic consequence of the coordinatewise source inequality. The determinant and factorial arguments belong to the cited reconstructions. The following calculation treats the marked-column case. To reach the global gain one must also use the division lattice and sum over the selected primes.

## A marked column and its cost

The same degree count can be retained in the two parity-weighted versions of the local theorem. For an *odd* top $s$ use the maximum $M_s$ computed as for $N_s$, with the finite caps $w_{s+d}$ at **every** odd distance. Write $a$ for the total number of pure factors, $b_{\rm ev}$ and $b_{\rm odd}$ for the mixed counts according to their source. Only mixed counts enter $M_s$. They consume $p^d$ units at $s$ and act through the rank-one substitution even when $s+d$ is another top. Consequently $b_{\rm odd}\le\sum_{s\ {\rm odd}}M_s$. Set
$$
 G_B=\gamma_p\sum_{s\ {\rm top}}\alpha_s-\sum_{s\ {\rm odd\ top}}M_s-\Delta .
$$
For a given subset $J$ of the target column labels, let $N_J$ count the marked boxes at even tops with label outside $J$, the marked boxes at odd tops with label in $J$, and, in each remaining minor at an odd position, the number of distinct column labels belonging to $J$. Then every unscaled entry coefficient $c$ satisfies
$$
 v(c)\ge G_B-\sum_{s\ {\rm even\ top}}\alpha_s,\qquad
 v(p^{N_J}c)\ge G_B .
$$
Indeed each pure term uses a top degree at an even endpoint, and each even-source mixed term uses one there. This bounds $a+b_{\rm ev}$ by the total even top degree. For the second bound, the two endpoints of each pure term have the same label and opposite parity, so exactly one is among the counted marked coordinates. Even-source mixed terms with label outside $J$ also use one of them. The remaining even-source terms act at odd targets in labels from $J$, for which a determinant is linear in each actual column. Repeated labels already give a zero determinant. Its allowable number of such derivatives is at most the number of its distinct column labels in $J$. Thus $a+b_{\rm ev}\le N_J$. Combine either payment with the bound on $b_{\rm odd}$ in the common factorial valuation. The argument retains the original marked-column normalization. [Parity and marked-column payments](https://github.com/rh-lean-roadmap/rh-lean-roadmap/blob/c7755c1086f05d0918ee8496d95912e4f35e22f9/docs/src/book/main.tex#L29366-L29443)

## A coefficientwise error bound for an imbalanced jet

Here is a consequence of the exact integral kernel used in the ordinary finite-prime argument. Suppose two rescaled series have expansions
$$
 \Theta(\varpi X)=\sum_{j\ge0}p^{-j}h_\upsilon^jU_j(X),\qquad
 \widetilde\Theta(\varpi X)=\sum_{j\ge0}p^{-j}h_\upsilon^j\widetilde U_j(X),
 \qquad \varpi^{p^2-1}=p.
$$
Use the same integral $h_\upsilon$. Assume the coefficients of $U_j-\widetilde U_j$ through the tested total degree have valuation at least $Q$, with $v(p)=1$. For each pair of matrix-entry labels $(a,b)$, let $A_{ab}$ and $B_{ab}$ be the sums of the exponents of $X_{s,a,b}$ in $X^\kappa$ over the even and odd positions, respectively. Set
$$
 T_p(A,B)=\max\{u+v:u,v\in\mathbb Z_{\ge0},\;pu+v\le A,\;u+pv\le B\}.
$$
Then the error in the individual derivative $P_\kappa\partial^\kappa$ at the origin satisfies
$$
 v\bigl(P_\kappa\kappa![X^\kappa]\bigl(\Theta-\widetilde\Theta\bigr)\bigr)
 \ge Q+v(P_\kappa)+v_p(\kappa!)-\frac{|\kappa|}{p^2-1}
           -\sum_{a,b}T_p(A_{ab},B_{ab}).
$$
For a polynomial test use the minimum over its monomials with nonzero coefficient.

Indeed, the integral series $\mathsf S_{s,a,b}$ has terms $(-1)^\ell X_{s-2\ell,a,b}^{p^{2\ell}}$. Every position occurring in it has the parity of $s$. Each term of $h_\upsilon=\sum_{s,a,b}\upsilon_s \mathsf S_{s,a,b}^{p}\mathsf S_{s+1,a,b}$ therefore consumes at least $(p,1)$ or $(1,p)$ units of degree in the two parities at its own pair $(a,b)$. This support statement holds in characteristic zero, including the mixed terms inside the $p$th power. Any product of $j$ kernel factors contributing to $X^\kappa$ allocates $u_{ab},v_{ab}$ factors of the two types at each matrix entry. Its degree constraints give $j\le\sum T_p(A_{ab},B_{ab})$. The corresponding contribution has valuation at least $Q-j$. Undoing $\varpi$ and multiplying by $P_\kappa\kappa!$ proves the inequality. Since $T_p(A,B)\le\lfloor(A+B)/(p+1)\rfloor$, this includes the total-degree precision estimate and specializes to zero kernel factors for a test supported on one parity at each matrix entry. The support argument uses Adriazola's kernel and refines the denominator-counting step in Subbarao's Theorem 17.2. [Exact integral kernel](https://github.com/jimjamzola/RH-Alpoge-Reconstruction/blob/9eefc08b0819728d4dd2ef0568b49a61251af111/manuscript/sec8_gain.tex#L101-L115) · [Rescaled theta-kernel membership](https://github.com/jimjamzola/RH-Alpoge-Reconstruction/blob/9eefc08b0819728d4dd2ef0568b49a61251af111/manuscript/sec8_gain.tex#L137-L163) · [Subbarao, v2, Theorem 17.2](https://github.com/muralisubbarao2/Refinements-and-Extensions-to-Alpoge-Claude-proof-of-Riemann-Hypotheisis/blob/4c3cb4f5e43212ec8c0ae759502291ae16e3df02/Ram-Calculus-Alpoge-RH-Nov24-v2.pdf#page=34)

For $p=5$ and a single entry with monomial $X^{25}Y$, the total-degree bound allows four denominator factors. The single odd exponent forces $T_5(25,1)=1$. Since $v_5(25!)=6$, the resulting precision is $Q+47/12$ for $P_\kappa=1$, compared with $Q+11/12$ from total degree. This value is attained in the integral kernel class. Take two positions, one matrix entry, $\upsilon_0=1,\upsilon_1=0$, $Q=0$, $\widetilde\Theta=0$, and $\Theta(\varpi X,\varpi Y)=p^{-1}h_\upsilon X^{20}$. The coefficient of $X^5Y$ in $h_\upsilon$ equals $1$, giving equality for the displayed derivative. The equality example concerns the integral kernel class. Obtaining a bound for a particular theta test requires its actual series and test polynomial.
