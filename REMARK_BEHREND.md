# What Behrend’s construction does in the cyclotomic tower

Items 11 and 19 of Alpöge’s remark combine two choices. The real dyadic cyclotomic layer has cyclic Galois group $(\mathbb Z/2^{e+2}\mathbb Z)^\times/\{\pm1\}$ of order $2^e$. In the Dirichlet construction this coordinate is combined with the fixed character data in a group $A$ with a cyclic subgroup $A_0$ of bounded index. A generator identifies $A_0$ with $\mathbb Z/n_0\mathbb Z$. Behrend’s construction selects **positions inside this cyclic group**. It marks the embeddings where the theta weights will be large. There must be enough marked embeddings for the prime estimate, yet a short string of successive Frobenius iterates should encounter very few of them. [Alpöge, items 11 and 19](https://alpo.ge/remark.pdf#page=4) · [The actual mixed Galois group](arithmetic_hosts/main.tex#L64-L98) · [Thick weights and their required density](conditional_main_v42/conditional_main.tex#L111-L139)

## A published theorem supplies the marked set

A set of integers is $k$-average-free if an average of at most $k$ of its members can equal another member only when all the terms are equal. Repetitions are allowed. Abboud, Bringmann, Hermelin and Shabtay give an absolute constant $c\ge1$ such that, for every integer $k\ge2$, integer $m\ge1$ and $0<\eta<1$, there are $m$ such integers in $[0,k^{c/\eta}m^{1+\eta}]$. This uniform dependence on $k$ matters because the Frobenius window grows with the scale. Behrend’s 1946 theorem directly treats ordinary three-term progressions. The more general statement also forbids, for example, $2s_1+s_3=3s_2$. The set $\{0,1,3\}$ illustrates the distinction. [Abboud–Bringmann–Hermelin–Shabtay, journal Lemma 3.3](https://doi.org/10.1145/3450524) · [Behrend’s original paper](https://doi.org/10.1073/pnas.32.12.331)

Take $k=2L$. If $0<|i|,|j|\le L$ and $i\ne j$, then a relation

$$
j(s_2-s_1)=i(s_3-s_1)
$$

has three nonzero coefficients $i-j,j,-i$ with sum zero. The coefficient whose sign occurs only once has absolute value at most $2L$. Dividing by it expresses one point as an average of repeated copies of the other two. Thus a $2L$-average-free set satisfies the full signed relation condition in the source. [The two native spacing requirements](https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Formalism/FrobeniusOrbits/HostThickExists.lean#L13-L32)

Here is the density calculation. For $X\ge1$ write $z=\log X$ and $u=\log k$. When $z\ge4cu$, put $\eta=\sqrt{cu/z}$ and choose

$$
m=\left\lfloor\exp\!\left(\frac{z-cu/\eta}{1+\eta}\right)\right\rfloor.
$$

The interval in the theorem ends at most at $X$. Since $(z-cu/\eta)/(1+\eta)\ge z-2\sqrt{cuz}$, the set has size at least $\tfrac12 X\exp(-2\sqrt{c\log X\log k})$. When $z<4cu$, a singleton already meets this bound.

For $n_0\ge16L$ take $X=n_0/(16L)$ and add one to every member. The resulting positive set $T_2$ satisfies $4Ls<n_0$ for every $s\in T_2$. Its cardinality is at least

$$
\frac{n_0}{32L}\exp\!\left(-2\sqrt{c\log n_0\log(2L)}\right).
$$

On the actual family $L=O_\varepsilon(\log x)$, $n_0\asymp x^{2+8\varepsilon}$ and $|A|/n_0$ is bounded for the fixed target. The loss relative to $n_0$ is therefore $x^{o(1)}$ in the denominator. In particular $|T_2|\ge x^{-\varepsilon}|A|$ eventually. This supplies the needed density with some absolute constant in the exponential. The direct proof in the reconstruction gives the explicit constant $64$ for the source’s form of the bound. [Host choice HC6](host_tops/main.tex#L174-L213)

## Why the same choice works for every Frobenius step

Fix a translate of $T_2$ and a step $h\in\mathbb Z/n_0\mathbb Z$. If $h$ has order greater than $4L$, the points at $L$ successive indices of $t+ih$ are distinct. Suppose three are marked. Subtract the first index from the other two, calling the resulting differences $i,j$. The three representatives $s_1,s_2,s_3\in T_2$ satisfy the displayed relation modulo $n_0$. Its two sides differ in absolute value by less than $2L\cdot n_0/(4L)<n_0$, so it holds over the integers, a contradiction. There are at most two marks in the window.

If $h$ has order $r\le4L$, distinct positions of its entire orbit differ by a nonzero multiple of $n_0/r$ modulo $n_0$. Two representatives from $T_2$ differ by less than $n_0/(4L)\le n_0/r$. The orbit therefore contains at most one marked position. Both arguments hold for every translate, which is precisely what the subsequent character averaging uses. Averaging a translated marked set kills the characters nontrivial on $A_0$. Each surviving character sees only its cardinality $|T_2|$. This explains how a set chosen for its spacing can still supply the intended prime sum. [Character averaging in CMP2](conditional_main_v42/conditional_main.tex#L279-L310)

The other set $T\subset A$ has a different job. It introduces a prescribed bias among cosets of $A_0$ and controls an average of bad primes. Its probabilistic construction and the common arithmetic realization of the theta and period data are separate steps. This literature substitution shortens the proof of the $T_2$ part of the host already reconstructed in HC6. The nine outstanding obligations concern additional data and comparisons. [The choice of the first set](host_tops/main.tex#L19-L72) · [Current obligations](continuation_v90/obligations.json)
