# Primitive densities for the generic scalar pairs

For either word of a row pair, a generic term with nonzero Gram invariant determines an integral joint frame at every finite place where it is represented. Its finite density enters the scalar-partner sum divided by the row's single-frame reference factors. The primitive representation formula gives this ratio explicitly, including at the auxiliary levels. At every dyadic place it is at most one. On the selected row, uniformly over represented joint frames,
$$
 1\le E_{\rm den}\le
 \exp\!\left(\tfrac52 f\,3^{-(k-m+1)}\right),
 \qquad m=2(r_S+1),\quad f=[F:\mathbb Q],\quad k\ge m+f+5.       \tag{1}
$$
Here $E_{\rm den}$ is the supremum of the normalized finite products enlarged to at least one. The adjoint-functor reconstruction obtains $\exp(12 f\,2^{-(k-m)})$ using separate bounds on the pair and reference. The improvement uses the marked last vector, cancellation between overlapping Euler factors, and splitting above two. It applies to equal and distinct words under the stated row hypotheses. [Adjoint-functor, primitive densities][reader] · [Row reference and supremum][data] · [Roadmap scalar-partner sum][partners]

## The local density and the marked frame

Fix a finite place of $F$, let $q$ be its residue field size, and write $\xi=1$ in the split case and $-1$ in the unramified quadratic case. Put
$$
 P(a,b)=\prod_{i=a}^{b}(1-\xi^i q^{-i}),
$$
with empty product one. Let $R=k+m-1$ be the ambient Hermitian rank. In an integral basis of the self-dual ambient lattice count primitive representations of an integral nonsingular $m$ by $m$ Hermitian matrix $S$. Write $c$ for its residual corank. A primitive representation has independent columns over the residue extension, in each component at a split place. The density is the number of solutions modulo $\varpi^n$ divided by $q^{n(2Rm-m^2)}$. At every depth $n\ge1$ it equals
$$
         P(R-m-c+1,R)=P(k-c,R).                                  \tag{2}
$$
The condition $R\ge m+c$ holds for all $0\le c\le m$ here. Hironaka's equation (3.1) and Corollary 3.3(i) give the unramified field formula. The following count covers both local algebras. [Hironaka, *Spherical functions and local densities on hermitian forms*, pp. 573, 577][hironaka] · [Reader's finite-field argument][reader]

At a split place write the residue equation as $U^{\mathsf T}V=S_0$ for $R$ by $m$ matrices. There are $q^{Rm}P(R-m+1,R)$ injective choices for $U$. With $U$ fixed, $U^{\mathsf T}$ is surjective and each column of $V$ has $q^{R-m}$ possible lifts. On $\ker S_0$ the lift must be injective into $\ker U^{\mathsf T}$. Its proportion is $\prod_{i=0}^{c-1}(1-q^{i-(R-m)})$. On a complement injectivity is automatic because $S_0$ is injective there. Multiplying gives $q^{2Rm-m^2}P(R-m-c+1,R)$.

At an inert place first embed the nonsingular block of dimension $d=m-c$ in the residual Hermitian space. Its ordered basis has $|U_R(q)|/|U_{R-d}(q)|$ images. For each of the $c$ radical columns, after choosing $i$ independent isotropic columns, take the orthogonal quotient by their span inside its perpendicular in the remaining space. This quotient has rank $N=R-d-2i$. Its nonzero isotropic vectors number $(q^N-(-1)^N)(q^{N-1}-(-1)^{N-1})$, with $q^{2i}$ lifts each. Indeed, for the norm on a Hermitian line, each nonzero value has $q+1$ inverse images. Writing $Z_N$ for the number of norm-zero vectors and $B_N$ for those of any fixed nonzero norm gives $Z_N=Z_{N-1}+(q^2-1)B_{N-1}$ and $Z_N+(q-1)B_N=q^{2N}$, starting with $Z_0=1$. The same recurrence gives $B_N=q^{N-1}(q^N-(-1)^N)$, so counting orthonormal bases gives $|U_R(q)|=q^{R^2}P(1,R)$. The nonsingular block contributes factors indexed $R-d+1$ through $R$. The radical steps contribute the successive adjacent index pairs $N-1,N$ down to $R-m-c+1$. The powers of $q$ give $2Rd-d^2+\sum_{i=0}^{c-1}(2(R-d)-2i-1)=2Rm-m^2$.

Finally the derivative of the Gram map at a primitive frame $X$ is $H\mapsto X^*JH+H^*JX$. Since $X^*J$ is surjective, an arbitrary off-diagonal can be assigned on one side. At an inert place each diagonal can be assigned by the surjective residue trace, also in characteristic two. In the split description one can fix the first component of the variation at zero and vary the second arbitrarily through $U^{\mathsf T}$. Each solution therefore has exactly $q^{2Rm-m^2}$ lifts to the next depth, proving (2).

For the actual row, take $S$ to be the Gram matrix after the two frame-line scalings. At a place above $g_0$ or $g_1$ of residue characteristic $g_i$, the integral joint basis uses the first frame $e$ and the divided difference $(e'-e)/g_i$ of the scaled frames. Thus the residual corank in (2) is taken **after** this basis change. At ordinary places use the scaled frames side by side. The pinned local comparison identifies this Gram matrix with the integral joint frame lattice and the ambient lattice with its self-dual local model. An unrepresented nonintegral joint lattice contributes zero. [Actual Gram matrix and divided difference][gram] · [Native identification and density formula][tied]

## Cancellation and the uniform product

For a word prime $T$ define $d(T)=k$ if the place divides $T$ and $d(T)=k+1$ otherwise. Its single-frame reference is $P(d(T),R)$. At an auxiliary place the two words share the single reference $P(k+1,R)$, and at ordinary places the reference is the product for the two words. The word primes are odd, coprime to $g_0g_1$, and split completely in $E$. With $a=\min(d(T_u),d(T_{u'}))$ and $b=\max(d(T_u),d(T_{u'}))$, the normalized local factors $h_v$ are consequently
$$
 h_v=\begin{cases}
       P(k-c,k),&v\mid g_0g_1,\\[2pt]
       P(k-c,a-1)/P(b,R),&v\nmid g_0g_1 .
      \end{cases}                                                \tag{3}
$$
The two intervals in the ordinary quotient are disjoint. In particular this is one density for a represented joint frame, even though it uses two words. [Single and double reference factors][data] · [Standing prime and congruence hypotheses][primes]

At an auxiliary place all factors are split, so $0<h_v\le1$. At an ordinary split place away from the word primes, the numerator contains the factor $1-q^{-k}$ and the other factors are at most one. On the denominator side,
$$
 P(k+1,R)\ge1-\sum_{i=k+1}^{R}q^{-i}
             \ge1-q^{-k}/(q-1)\ge1-q^{-k}.
$$
Hence $h_v\le1$ there too, for every residual corank. All dyadic places of this host split in $E/F$ and both word primes are odd, so no dyadic place increases the product. [Dyadic splitting for this host][dyadic]

Put $s=k-m+1\ge7$. At an inert place the first frame contains its last vector of norm $-T_u$, a unit since $T_u$ splits completely. Its last frame-line scaling is one. Thus $S\bmod\varpi$ has rank at least one, $c\le m-1$ and $k-c\ge s$. Both ordinary intervals in (3) lie in $[s,R]$. At an ordinary split place dividing either word prime the numerator is at most one, so only the denominator can increase $h_v$; its indices start at $b\ge k\ge s$. Both cases have $q\ge3$. Using $|\log(1\pm x)|\le x/(1-x)$ for $0\le x<1$, and disjointness of the intervals, gives
$$
 \max(0,\log h_v)
     \le \frac{q^{-s}}{(1-q^{-1})(1-q^{-s})}.
$$
[Marked vector's norm and both frame scalings][gram] · [Last flag multiplier][last]

There are at most $f$ places above each rational prime and $q$ is at least its residue characteristic. Summing over odd residue characteristics gives
$$
 \sum_v\max(0,\log h_v)
 \le\frac{3f}{2(1-3^{-s})}\sum_{n\ge3}n^{-s}
 \le\frac{3(1+3/(s-1))}{2(1-3^{-s})}\,f3^{-s}
 \le\tfrac52 f3^{-s}.
$$
The second inequality uses the first term and the integral from three to infinity. The products converge to positive values for represented integral frames: outside the finitely many places above two, (3) gives the same absolutely summable bound for $|\log h_v|$ with the universally valid starting exponent $k-m\ge6$. Every remaining local factor is positive. Taking the supremum gives (1), also if the set of represented frames is empty with the convention $E_{\rm den}\ge1$. This proves the finite density input. The global signed estimate also uses the scalar-partner fibre identities and the archimedean energy bound. [Local factors in the assembled scalar estimate][application]

[hironaka]: https://www.jstage.jst.go.jp/article/jmath1948/51/3/51_3_553/_pdf/-char/en#page=25
[reader]: https://github.com/adjoint-functor/theta-periods-to-rh-reader/blob/c0fe7c673cb8acaa328bebb2440ee3334c520b9a/tex/trace.tex#L665-L738
[application]: https://github.com/adjoint-functor/theta-periods-to-rh-reader/blob/c0fe7c673cb8acaa328bebb2440ee3334c520b9a/tex/trace.tex#L839-L855
[partners]: https://github.com/rh-lean-roadmap/rh-lean-roadmap/blob/94e6a98b4e74932a0298d6bd22d44cf60c62764b/docs/src/book/main.tex#L44472-L44497
[primes]: https://github.com/rh-lean-roadmap/rh-lean-roadmap/blob/94e6a98b4e74932a0298d6bd22d44cf60c62764b/docs/src/book/main.tex#L15552-L15560
[data]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Formalism/LocalToGlobal/SiegelLatticeTheory/CokernelGLCounts/DataInst.lean#L177-L205
[gram]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Formalism/LocalToGlobal/SiegelLatticeTheory/CokernelGLCounts/CntLocal.lean#L54-L92
[tied]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Formalism/LocalToGlobal/SiegelLatticeTheory/CokernelGLCounts/RankPointCounts/DualFamilyCounting/DensAtD.lean#L58-L88
[last]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Formalism/LocalToGlobal/SiegelLatticeTheory/CokernelGLCounts/RankPointCounts/MemOfBcPMem.lean#L70-L77
[dyadic]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Formalism/LocalToGlobal/IndefiniteReal/FinitePlaces/TwoSplit.lean#L41-L75
