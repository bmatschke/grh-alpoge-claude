# Integral descent at primes added for a common marking

Fix an exported arithmetic member with its two marked levels, the imaginary quadratic field $K$, fixed modulus $m_*$ and squarefree auxiliary modulus $N$. Every prime of $N$ splits in $K$, and $N$ avoids $m_*$ and all active primes. Write $H_d$ for the ray class field of $d\mathcal O_K$. Let $B$ be any specified coefficient field on one side containing $H_{m_*}$, and put $L=BH_{m_*N}$. This section examines the integral lattice of the **rational space of lower-level sections** in the marked cover, with its original evaluation tests. It uses the rational pullback, identification of invariant sections and detection of lower-coefficient integrality by lifted frames established in the [common marked-level comparison](SECOND_PASS_COMMON_MARKED_LEVELS.md).

## Removing the unramified part

Set $B_c=B(\zeta_N)$. The cyclotomic field lies in $L$ by Artin reciprocity. For instance the norm to $\mathbf Q$ of a principal generator congruent to one modulo $N\mathcal O_K$ is congruent to one modulo $N$, so the cyclotomic Artin map factors through the ray group. With $N=1$ this is the trivial character condition. Then $L/B_c$ is unramified at **every** finite prime. Away from $N$ this follows from the [relative ray calculation](SECOND_PASS_RAY_DIFFERENT.md). At a place of $K$ over $p\mid N$, the completed base is $\mathbf Q_p$, the old ray field is unramified, and inertia on the new field has order $p-1$. Restriction to $\mathbf Q_p(\zeta_p)$ already has order $p-1$. Inertia on the extension over $H_{m_*}(\zeta_N)$ is therefore trivial. Base change by $B$ proves the assertion. Restriction embeds the Galois group of $L/B$ into the abelian ray class group over $K$, since $L$ is a compositum with that ray field. In particular
$$
 \mathfrak D_{L/B}=\mathfrak D_{B_c/B}\mathcal O_L.
$$
Any stable integral pullback lattice over $L$ is the scalar extension of its intersection with the $B_c$-rational space, by unramified descent. Thus all finite lattice loss from adjoining this ray field occurs already over $B_c/B$. If the specified field $B$ contains $\zeta_N$, the original invariant lattice extends exactly at every prime, including all $p\mid N$. When those roots are adjoined as a preliminary step its own determinant cost must be included. [Trace comparison for the actual integral tests](../geometry/PEL_GOOD_FRAMES_AT_ALL_PRIMES.md) · [Cyclotomic tower and integral descent](../periods/PERIOD_CYCLOTOMIC_DESCENT.md)

## The index at a tame coefficient prime

Fix $\lambda\mid p\mid N$ of $B$ and $w\mid\lambda$ of $L$. In this paragraph $K_0=B_\lambda$, $K_1=L_w$, $U$ is the maximal unramified intermediate field, and $t=e(K_1/K_0)$ divides $p-1$. Write $V$ for the lower $K_0$-vector space. Let $T\subset K_1\otimes V$ be the upper integral lattice with its semilinear decomposition-group action, and let $T_0=T\cap V$. In the application the lower lattice of integral frame tests is $T_0$ by the marked pullback comparison. Put $V_U=U\otimes V$ and $T_U=T\cap V_U$. The unramified descent of $T_U$ gives $T_U=\mathcal O_U T_0$. If $t=1$ the upper lattice is already $\mathcal O_{K_1}T_0$.

For $t>1$ choose a uniformizer $\varpi$ of $K_1$ which is a tame inertia eigenvector. Indeed, the action on its cotangent line gives the faithful tame character of inertia $I$ into the residue field of $U$. Lift this character to $\mu_t\subset U$. Project any uniformizer to its character using $t^{-1}\sum_{\sigma\in I}\chi(\sigma)^{-1}\sigma$. The projection agrees with that uniformizer modulo the square of the maximal ideal, so has valuation one. Its $t$-th power is a uniformizer of $U$, up to a unit. Let $\pi_U$ be any uniformizer of $U$ and $k_U$ its residue field. Define a filtration in the **single** lower lattice by
$$
 W_a=\{v\in V_U:\ \varpi^{-a}v\in T\},\qquad 0\le a<t.
$$
Its zeroth term is $W_0=T_U$. For $1\le a<t$ the terms decrease and $\pi_U T_U\subseteq W_a\subseteq T_U$. Integral character idempotents on $T$ now give
$$
 T=T_U\oplus\bigoplus_{a=1}^{t-1}\varpi^{-a}W_a,\qquad
 \mathcal O_{K_1}T_0=T_U\oplus\bigoplus_{a=1}^{t-1}\varpi^{-a}\pi_U T_U .
$$
These are decompositions as $\mathcal O_U$-modules. For the first, each eigenspace of inertia in $K_1\otimes V$ is $\varpi^{-a}V_U$. For the second, $1,\varpi,\ldots,\varpi^{t-1}$ is an integral basis in this totally ramified tame extension over $U$, and $\varpi^{t-a}$ differs from $\varpi^{-a}\pi_U$ by a unit in $U$. Since $U$ and $K_1$ have the same residue field, the quotient length equals
$$
 \operatorname{length}_{\mathcal O_{K_1}}(T/\mathcal O_{K_1}T_0)
   =\sum_{a=1}^{t-1}\dim_{k_U}(W_a/\pi_U T_U).
$$
In particular its maximum is $(t-1)\dim V$ and equality of the two integral lattices is equivalent to $W_1=\pi_U T_U$. The filtration can detect a smaller index than the different alone. For example, in rank one $T=\varpi^{-b}\mathcal O_{K_1}$ with $0\le b<t$ has $T_0=\mathcal O_{K_0}$ and the first $b$ residue terms have dimension one. The formula gives length $b$.

**A test in the original finite evaluations.** For vector-valued tests, a reading means a coordinate in an integral frame. Normalize the extended valuation by $v(\pi_U)=1$. For $v_0\in T_U$ the condition $v_0\in W_a$ says that all its upper integral frame readings have valuation at least $a/t$, using the same integral trivializations as for $T$. Thus $W_1=\pi_U T_U$ precisely when each nonzero class of $T_U/\pi_U T_U$ has a reading of valuation strictly below $1/t$. Changing a representative by $\pi_U T_U$ does not affect this test. This gives an exact finite-dimensional criterion at newly marked tame primes on an exported member. Existence of common members with the required divisibility, heights and scale bounds is the remaining arithmetic construction problem.
