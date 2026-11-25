# The first moment on the ramified column of one word

For the height entries 1 and 4, [surjectivity of the original reference descent](PERIOD_REFERENCE_ROW_DESCENT.md) leaves the test $P\Pi\ne0$ on each word. Work on its tied equal-word realization, with the absolute convergence and normalization in B8.08oc. Write $K=\alpha^{-1}P^*P=I+Z+X$, where $Z$ is the nonidentity zero-Gram part and $X$ is the nonzero-Gram part. This note computes the **linear trace** from $X$, including both finite type primes and the diamond projection at the separate word prime $T$.

## Which lattice pairs contribute

Put $A=(\mathbf F_T^\times)^f$, $H=T-1$, $d=\dim C_u$, $\rho=(1-1/H)^f$, and write $R(a)$ for diamond translation. For $a\in A$ let $s(a)=\#\{v:a_v\ne1\}$. Expanding the product of the projections off the coordinatewise constant spaces gives
$$
       \Pi=\sum_{a\in A}c(a)R(a),\qquad
       c(a)=\rho\left(\frac{-1}{T-2}\right)^{s(a)}.                \tag{1}
$$
In particular $c(1)=\rho$. The variable $s(a)$ measures scalar changes of the marked vectors at $T$. The two type-prime level groups act on different coordinates. [Free vector markings][mark] · [Diamond translations and their metrics][diamond]

Let $\mathcal C$ denote the column classes, $V_\pi$ their coefficient fibre, and $n_\pi=\dim V_\pi$. Let $\Lambda_r$ be the coarse row class of $r\in\mathcal C$ obtained by forgetting the two type-prime frames and keeping the word-prime marking. In the definite model the coarse classes are self-dual genus lattices $L$ with a nonzero vector $v_w\in L_w/TL_w$ on the chosen split side at each $w\mid T$, up to rational isometry. Indeed the full class set is the adelic double quotient with the unitriangular levels at the two type primes and vector stabilizers at $T$. Enlarging just the two unitriangular levels to their full integral groups gives precisely this marked genus description. In the ambient flag model the enlarged subgroup preserves the row lattice, and the split-frame lift of B8.08oa is transitive on its type frames. Thus the resulting class partition is precisely $r\mapsto\Lambda_r$ of B8.08oc. [Definite cosets][genus] · [Coarse classes and type-frame lifts][coarse] · [The fibres of the forgetful map][fibre]

Choose the convention $R(a)\delta_r v=\delta_{ar}D_{a,r}v$ with $D_{a,r}$ unitary between the indicated coordinate fibres. For a cell $S$ equal to either of the nonzero-Gram cells, put $X_S=\sum_{t\in S}O_t$. Each term has a coarse lattice pair $q_t$, a type index $i_t$, and an amplitude $a_t\in\operatorname{End}V_\pi$, all in the B8.08oc normalization. Let $s_r$ denote the chosen type frame, $\psi_{\mathcal I}$ its product of Whittaker characters extended by zero off $\mathcal U$. Taking the diagonal of $R(a)O_t$ in the actual coefficient fibres gives
$$
 \operatorname{tr}(\Pi X_S)
 =\sum_{a\in A}c(a)\sum_{r\in\mathcal C}
    \sum_{\substack{t\in S:\ q_t=(\Lambda_r,\Lambda_{ar})}}
    \psi_{\mathcal I}(s_r^{-1} i_t s_{ar})\,
                      \operatorname{tr}(D_{a,r}a_t).                  \tag{2}
$$
Indeed the only block of $O_t$ which contributes in this coordinate is its $(r,ar)$ block. The block formula supplies both the support condition and its phase. Its trace composes the two maps between the same fibres and is independent of the fibre bases. The cell's absolute convergence justifies all rearrangements. Thus two coarse classes contribute only when their underlying lattices with the **projective lines** of their $T$-markings are isometric, including all other fixed levels. [Actual block formula][block]

## Averaging the type frames in this first moment

Let $\mathcal I=\prod_{v\mid g_0g_1}\mathrm{GL}_k(\mathbf F_{q_v})$, $\mathcal U$ its product of upper unitriangular subgroups, and $A_\Lambda$ the finite rational stabilizer of a coarse word-marked class. Write $h_\Lambda$ for its base representative. For each $a,\Lambda$ choose the rational change of representative transporting the diamond image of $h_\Lambda$ to the coarse representative $a\Lambda$. Denote the resulting type-frame displacement by $b_{a,\Lambda}\in\mathcal I$, and the coefficient transport by $D_{a,\Lambda}$ in the orientation of (2). They can be taken to be the identity for $a=1$. Then
$$
 \operatorname{tr}(R(a)X_S)
 =\sum_\Lambda\frac{1}{|A_\Lambda|}
    \sum_{\substack{t\in S:\ q_t=(\Lambda,a\Lambda)}}
       \gamma_{\rm fin}(i_t b_{a,\Lambda})\,
                 \operatorname{tr}(D_{a,\Lambda}a_t),               \tag{3}
$$
where $\gamma_{\rm fin}(y)=|\mathcal U|^{-1}\sum_{x\in\mathcal I}\psi_{\mathcal I}(x^{-1}yx)$. Different choices of rational transport in (3) give the same total by (2).

For the proof, first fix $a,\Lambda$. For every $x\in\mathcal I$ use the finite-adelic lift supported at the type places to give type frame $x$ over $h_\Lambda$. Use its diamond translate as the second representative, followed by the fixed rational change to $a\Lambda$. The diamond is supported at $T$ and commutes with the type-place lift. Its second type coordinate is therefore $b_{a,\Lambda}x$, and the coefficient transport is the same $D_{a,\Lambda}$ for all $x$. The two fibre bases may be chosen this way in the scalar trace of each composition. Changing them conjugates that composition. In particular, when the two classes coincide one can still use separate bases in the intermediate copy of the fibre. For this choice the block phase is $\psi_{\mathcal I}(x^{-1} i_t b_{a,\Lambda}x)$. The map from the complete type frames $x$ to actual fine classes above $\Lambda$ has fibres of size $|A_\Lambda||\mathcal U|$ by the free parametrization in B8.08oc. Summing over all $x$ and dividing by this fibre size proves (3). This use of representative independence applies to the whole retained cell, which rational stabilizer transport preserves. It does not assert such invariance of an individual orbital summand. [Type-frame parametrization and transport of cells][fibre] · [Finite character and normalization][type]

Consequently only indices for which $i_t b_{a,\Lambda}$ is unipotent at **every** type place survive the sum in (3). For $a=1$ these are precisely unipotent type indices in the diagonal coarse pair. For other diamonds the displaced index is essential. Its normalized weight is the product of the signed factors in the [finite character calculation](SPECTRAL_FINITE_CHARACTER_VALUES.md). In particular a nonidentity unipotent component of rank $h_v=\operatorname{rank}(i_tb_{a,\Lambda}-I)_v$ contributes $(-1)^{h_v}/\prod_{j=k-h_v+1}^k(q_v^j-1)$. The trace needs one amplitude at a time and the two strata of type and word-prime support in (2)–(3). Corank pairs of two orbital terms arise in estimates of *squared* Hilbert–Schmidt norms. [Character formula, Thiem–Vinroot, Theorem 3.2](https://www.math.wm.edu/~vinroot/UnitaryGGEJC.pdf)

## Cost of nonidentity diamonds for a fixed pair

For a fixed pair $\Lambda,\Lambda'$ in the same projectively marked genus class, the set $A(\Lambda,\Lambda')=\{a:a\Lambda=\Lambda'\}$ is one coset of the subgroup stabilizing $\Lambda$. Put $n=2fk$, the rational dimension of the definite column lattice. The image of that stabilizer in **each coordinate** of $A$ has order at most $M=2n^2$.

To see this, write $\Lambda$ as $(L,(v_w))$. A stabilizing diamond is realized by an element $u$ of the finite isometry group of the positive definite integral genus lattice $L$ taking $v_w$ to $a_w v_w$ (or the inverse, depending on the action convention) at each $w$. Its action on the rank-$n$ underlying integral lattice has a monic degree-$n$ characteristic polynomial made up of cyclotomic factors. Since $T-1>n$ at large selected members, $u$ has order prime to $T$, or some power would have order $T$ in rational dimension $n$. At a split place the scalar $a_w$ is a root modulo $T$ of this same polynomial. For each cyclotomic factor $\Phi_e$ the reduction of its roots has exact order $e$, since $T\nmid e$. It follows that the multiplicative order $m_w$ of $a_w$ has $\varphi(m_w)\le n$. Apply this to a generator of the coordinate image, which is a cyclic subgroup of $\mathbf F_T^\times$. Finally $\varphi(m)^2\ge m/2$ follows from the prime-power formula, with a factor smaller than one in $\varphi(m)^2/m$ only for $2^1$. This proves the bound independently of the order of the whole genus isometry group.

Every coordinate of an admissible $a$ now lies in a coset of size at most $M$. For a specified nonempty set of $j$ changed coordinates there are at most $M^j$ admissible tuples with exactly that set. Equation (1) therefore gives the uniform estimate, also valid when the coset is empty,
$$
 \frac{1}{\rho}\sum_{\substack{a\in A(\Lambda,\Lambda')\\a\ne1}}|c(a)|
 \le \left(1+\frac{M}{T-2}\right)^f-1
 \ll \frac{f^3 k^2}{T}.                                           \tag{4}
$$
Here $T-1\ge(g_0g_1)^2$ and $g_i\ge(kb)^8$, so $fM/(T-2)\to0$ on the original family. For this fixed pair, an immediate bound on the absolute value of the nonidentity part of (3) after weighting by (1) is
$$
 \frac{\rho\,\gamma_{\rm fin}(1)\sqrt{n_\pi}}{|A_\Lambda|}
 \left[\left(1+\frac M{T-2}\right)^f-1\right]
 \sum_{t\in S:\,q_t=(\Lambda,\Lambda')}\|a_t\|_{\rm HS}.
$$
This uses $|\gamma_{\rm fin}(y)|\le\gamma_{\rm fin}(1)$ and unitary coefficient transport. Retaining the exact type factors in (3) can reduce the bound. There can be many different pairs above one projectively marked class. A uniform summation estimate over them remains necessary. [Word-prime lower bound][large]

## Uniqueness when a type component is the identity

The choice of rational transports in (3) yields another restriction on each fixed orbital index. Suppose $a$ and $a'$ carry the same $\Lambda$ to the same $\Lambda'$. On the underlying unmarked definite lattices, the chosen rational changes of representative are isometries $\gamma_a,\gamma_{a'}:L\to L'$. The diamonds themselves preserve $L$ and have identity component at both type primes. Consequently at each type place $v$, the relative matrix $b_{a,\Lambda}^{-1}b_{a',\Lambda}$ is the reduction of $u=\gamma_a^{-1}\gamma_{a'}\in\operatorname{Aut}(L)$ in the chosen local basis. This is valid up to conjugation, which preserves order, rank and unipotence. The chosen split half is a faithful local representation of the definite unitary isometry. The finite order of $u$ is prime to both $g_j$, as $g_j-1>2fk$ would exclude an element of order $g_j$ in this rational lattice group.

Fix $i=i_t$. If $i b_{a,\Lambda}$ equals the identity at **one** type place and $\gamma_{\rm fin}(i b_{a,\Lambda})\ne0$, then every other diamond $a'$ for this coarse pair has $\gamma_{\rm fin}(i b_{a',\Lambda})=0$. Otherwise at that place the relative reduction of $u$ would be unipotent of order prime to the residue characteristic, hence the identity. The congruence kernel in the local integral general linear group is pro-$g_j$. Its finite prime-to-$g_j$ torsion is trivial. Thus $u=1$ on the split local space and hence on the rational lattice. The two rational changes of representative coincide. Comparing the nonzero word-prime vectors forces $a=a'$ in every coordinate. This argument works for any fixed choice of the rational transports.

In particular, if at least two diamonds survive for that pair and index, **every** local unipotent factor for every survivor is nonidentity. The exact character values then give
$$
 \frac{|\gamma_{\rm fin}(i b_{a,\Lambda})|}{\gamma_{\rm fin}(1)}
 \le \big((g_0^k-1)(g_1^k-1)\big)^{-f}.                          \tag{5}
$$
In the unique-survivor case the formula (3) gives its individual signed coefficient. In the other case (5) applies also to the identity diamond if it survives, and multiplies the cost (4) for all the other ones. These conclusions control the finite coefficient of an individual orbital index. The total still contains the archimedean traces and the number and size of the contributing indices.

## An alternative using only the ordinary trace and a coarse second moment

The [earlier moment test](PERIOD_FULL_REFERENCE_PAIRING.md) has the following centered form, with the same threshold for positivity. Let $m_K=\operatorname{tr}K/d\ge0$. Since $\operatorname{tr}(\Pi-\rho I)=0$ and $\|\Pi-\rho I\|_{\rm HS}^2=d\rho(1-\rho)$,
$$
 \alpha^{-1}\|P\Pi\|_{\rm HS}^2
 \ge \rho d m_K-\sqrt{d\rho(1-\rho)}\,\|K-m_K I\|_{\rm HS}.       \tag{6}
$$
For example, $m_K\ge1/2$ and $\|K-m_K I\|_{\rm HS}\le\tfrac14\sqrt{d(T-1)/f}$ already imply strict positivity on the selected range $\rho\ge3/4$, since $1-\rho\le f/(T-1)$. The ordinary first moment in this alternative uses only the $a=1$ case of (3). Formula (6) allows a substantially larger second moment than the final near-isometry assertion. Neither the signed lower bound for the surviving ordinary loops nor the total first-moment lower bound in (2)–(3) has been established here for the true orbital amplitudes. Thus the upstream Bessel nonvanishing and the normalized seesaw required by entries 1 and 4 remain open.

[mark]: https://github.com/rh-lean-roadmap/rh-lean-roadmap/blob/02a95b4c62db610642af5f278ee5d0d6df87b348/docs/src/book/main.tex#L43753-L43765
[diamond]: https://github.com/rh-lean-roadmap/rh-lean-roadmap/blob/02a95b4c62db610642af5f278ee5d0d6df87b348/docs/src/book/main.tex#L32023-L32037
[genus]: https://github.com/rh-lean-roadmap/rh-lean-roadmap/blob/02a95b4c62db610642af5f278ee5d0d6df87b348/docs/src/book/main.tex#L58779-L58794
[coarse]: https://github.com/rh-lean-roadmap/rh-lean-roadmap/blob/02a95b4c62db610642af5f278ee5d0d6df87b348/docs/src/book/main.tex#L43905-L43935
[fibre]: https://github.com/rh-lean-roadmap/rh-lean-roadmap/blob/02a95b4c62db610642af5f278ee5d0d6df87b348/docs/src/book/main.tex#L43983-L44003
[block]: https://github.com/rh-lean-roadmap/rh-lean-roadmap/blob/02a95b4c62db610642af5f278ee5d0d6df87b348/docs/src/book/main.tex#L43967-L43982
[type]: https://github.com/rh-lean-roadmap/rh-lean-roadmap/blob/02a95b4c62db610642af5f278ee5d0d6df87b348/docs/src/book/main.tex#L46579-L46601
[large]: https://github.com/rh-lean-roadmap/rh-lean-roadmap/blob/02a95b4c62db610642af5f278ee5d0d6df87b348/docs/src/book/main.tex#L44326-L44341
