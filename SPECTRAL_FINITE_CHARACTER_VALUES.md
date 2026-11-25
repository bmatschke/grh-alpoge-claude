# The exact finite Gram coefficient on the nonsingular same-word cell

At a selected split marked place over $g_j$, put $q=g_j$. In the free orbit coordinates of B8.10f the normalized local Gram entry at relative displacement $x\in\mathrm{GL}_k(\mathbf F_q)$ is
$$
 c_q(x)=
 \begin{cases}
 0,& x\text{ is not unipotent},\\
 \displaystyle\frac{(-1)^h}{\prod_{a=k-h+1}^{k}(q^a-1)},&
 x\text{ is unipotent},\quad h=\operatorname{rank}(x-I).
 \end{cases}
$$
The rank-zero value is one. In particular a transvection has entry $-1/(q^k-1)$, and every nonidentity entry has absolute value at most $1/(q^k-1)$. The character formula is classical. Its application here gives the exact signs, support, and second moment in the finite coordinates of the row calculation. B8.10f gives an upper operator bound on that matrix. The source identifies its kernel with $\gamma/\gamma(1)$ or its conjugate, where $\gamma=\operatorname{Ind}_{U_k}^{\mathrm{GL}_k}\xi$ and $\xi$ is the chosen nondegenerate simple-root character. Both conventions give the displayed real number. [Roadmap's free orbit and normalization][gram] · [Thiem and Vinroot, Theorem 3.2, including attribution to Howlett and Zworestine][gg]

## Derivation for the specified character

Let $P_a$ be the stabilizer of the last covector and $T_a=\operatorname{Ind}_{U_a}^{P_a}\xi_a$, using the same additive character in each rank. For unipotent $y\in P_a$ with $D=\dim\ker(y-I)$,
$$
                  \operatorname{tr}T_a(y)=(-1)^{a-D}\prod_{b=1}^{D-1}(q^b-1).
$$
This holds at $a=1$. Write $y=(A,v)$ in $P_a=\mathrm{GL}_{a-1}\ltimes V$, $V=\mathbf F_q^{a-1}$, and let $d=\dim\ker(A-I)$. By induction in stages $T_a$ is induced from $P_{a-1}\ltimes V$ with representation $T_{a-1}$ twisted by $v\mapsto\psi(e_{a-1}^*v)$. Indeed this restricts on $U_{a-1}\ltimes V$ to the inducing character when one takes the original $U_{a-1}$-inducing line. The cosets index the nonzero covectors of $V$. Its trace at $y$ sums only over covectors $b\ne0$ satisfying $bA=b$. Each corresponding conjugate of $A$ has the same nullity $d$. The only varying factor is $\psi(bv)$. Its sum is $q^d-1$ if $v\in\operatorname{im}(A-I)$, and $-1$ otherwise, by character orthogonality including then removing the zero covector. Solving $(A-I)z+tv=0$ shows that $D=d+1$ in the first case and $D=d$ in the second. This proves the trace formula.

Now induce $T_k$ from $P_k$ to $\mathrm{GL}_k$. A unipotent $x$ fixes $q^D-1$ nonzero covectors and each summand has the same trace just computed. Thus $\gamma(x)=(-1)^{k-D}\prod_{a=1}^{D}(q^a-1)$. An element with nonzero induced character must be conjugate into $U_k$ and hence unipotent. Dividing by the value at the identity proves the displayed coefficient.

## Consequences on the project indices

Let $H=G_{\mathrm{fin}}/\Gamma_1$ in the finite-type coordinates. Entries between distinct free orbits vanish. Within a tensor orbit,
$$
 H_{ij}=\prod_{v\mid g_0g_1}c_{q_v}(x_{v,ij}).
$$
In particular the entry vanishes if one relative component has a nontrivial semisimple part. Otherwise its sign is $(-1)^{\sum_v h_{v,ij}}$, with $h_{v,ij}=\operatorname{rank}(x_{v,ij}-I)$; the preceding product supplies every denominator.

There is also an exact second-moment identity. On one place, the normalized row has
$$
 \sum_{x\ne1}|c_q(x)|^2
    =\prod_{a=2}^k(1-q^{-a})^{-1}-1
    \le \frac1{q(q-1)-1}.
$$
In fact $\sum_x|\gamma(x)|^2=|G|(q^k-q^{k-1})$, since the $q^k-q^{k-1}$ distinct generic constituents each have multiplicity one. Use $|G|=q^{k^2}\prod_{a=1}^k(1-q^{-a})$ and $\gamma(1)=|G|/q^{k(k-1)/2}$. The bound follows from $\prod_{a=2}^k(1-q^{-a})\ge1-\sum_{a=2}^{\infty}q^{-a}$. On each full tensor orbit the off-diagonal squared row mass is exactly
$$
 \sum_{j\ne i}|H_{ij}|^2=
 \prod_{\ell=0}^1\prod_{a=2}^k(1-g_\ell^{-a})^{-f}-1.
$$
For a principal restriction this formula supplies an upper bound. [Number of constituents and orbit tensor product][gram]

For the norm expansion on any absolutely summable nonsingular cell let $w_i$ be its orbital subtotal at finite index $i$, and put $S=\{i:w_i\ne0\}$. Define $d_S=\max_{i\in S}\sum_{j\in S,\ j\ne i}|H_{ij}|$. Applying $2|\langle w_i,w_j\rangle|\le\|w_i\|^2+\|w_j\|^2$ and the Hermitian symmetry gives
$$
 (1-d_S)\Gamma_1\sum_{i\in S}\|w_i\|^2
 \ \le\ \|\operatorname{part}\|_{\mathrm{HS}}^2
 \ \le\ (1+d_S)\Gamma_1\sum_{i\in S}\|w_i\|^2 .
$$
If, for each $i$, at most $M$ other active indices lie in its same orbit with unipotent relative elements at every component, then $d_S\le M/(\min(g_0,g_1)^k-1)$. In particular, strictly fewer than $\min(g_0,g_1)^k-1$ such neighbors guarantees that a nonzero subtotal survives in that cell. The exact formula allows the denominators at every moving component to be multiplied when counting these neighbors. This criterion measures the support in the **two type-prime** coordinates. An orbit of the diamond test at the word prime $T_u$ is indexed by a different group.

There is an unconditional improvement to this sparse criterion on the **actual rational stabilizer orbits** of a tied row. For the lattice pair $(\Lambda,\Lambda')$, B8.08oc identifies a subgroup $A_\Lambda\le\mathcal I$ from the rational stabilizer and proves the multiplication bijection
$$
 A_\Lambda\times\mathrm{Cl}_u(\Lambda)\times\mathcal U\longrightarrow\mathcal I,\qquad
 (a,\rho,v)\longmapsto a\,s_u(\rho)v,
$$
where $\mathcal U$ is the product of the marked upper unitriangular groups. Thus $A_\Lambda$ acts freely on $\mathcal I/\mathcal U$: writing a coset in the displayed unique form shows that $a$ fixing it forces $a=1$. Equivalently a nonidentity member of $A_\Lambda$ cannot be conjugate in $\mathcal I$ into $\mathcal U$. An element is conjugate into $\mathcal U$ precisely when **every** local component is unipotent, by choosing a flag in each finite vector space. It follows at once that
$$
 H_{a i,b i}=\mathbf1_{a=b}\quad(a,b\in A_\Lambda),\qquad
 H_{i a^{-1},i b^{-1}}=\mathbf1_{a=b}\quad(a,b\in A_{\Lambda'}).
$$
Indeed the relative index in each case is a conjugate of a stabilizer element, or that element itself. The native row transport actually sends a term with index $i$ to a term of index $ai$ or $ia^{-1}$ in the same lattice pair and preserves each nonsingular cell. Consequently **all cross terms between distinct finite indices in one such left or right orbit vanish exactly**. This conclusion holds for both generic and nongeneric nonzero-Gram cells. The fixed-lattice-pair subtotals $Z_{\Lambda,\Lambda'}(ai)$ are unitary transforms of $Z_{\Lambda,\Lambda'}(i)$, so the Gram sum restricted to that single left orbit is $\Gamma_1|A_\Lambda|\|Z_{\Lambda,\Lambda'}(i)\|_{\rm HS}^2$, before the lattice-pair weight; the right-orbit formula is identical. This uses the model's established neat action and requires no extra height bound on arbitrary rational isometries. [Actual stabilizer bijection and nonsingular row transport][stab] · [Norm expansion][expansion]

The same-index coefficients are exactly one. Multiple terms at the same index and orbital row can therefore cancel within $w_i$, and distinct cells can cancel in the full operator. The nonsingular-cell estimate in B8.08l still needs arithmetic control of the higher-corank and the two signed corank-one sums at these same indices. To use the sparse lower bound for a particular ramified Bessel test one must identify its finite-index expansion and show that its total orbital subtotals give a nonzero vector. The character calculation by itself establishes neither of those facts. [Same-row sums][rows] · [Ramified column criterion](PERIOD_FULL_REFERENCE_PAIRING.md)

[gram]: https://github.com/rh-lean-roadmap/rh-lean-roadmap/blob/02a95b4c62db610642af5f278ee5d0d6df87b348/docs/src/book/main.tex#L46579-L46613
[stab]: https://github.com/rh-lean-roadmap/rh-lean-roadmap/blob/02a95b4c62db610642af5f278ee5d0d6df87b348/docs/src/book/main.tex#L43983-L44007
[expansion]: https://github.com/rh-lean-roadmap/rh-lean-roadmap/blob/02a95b4c62db610642af5f278ee5d0d6df87b348/docs/src/book/main.tex#L16739-L16770
[gg]: https://www.math.wm.edu/~vinroot/UnitaryGGEJC.pdf
[rows]: https://github.com/rh-lean-roadmap/rh-lean-roadmap/blob/02a95b4c62db610642af5f278ee5d0d6df87b348/docs/src/book/main.tex#L16591-L16627
