# A human-readable version of the formal Alpöge–Claude proof of RH and Dirichlet GRH

*Overview*

For every Dirichlet character $\chi$, each zero of $L(s,\chi)$ in $0<\Re s<1$ has $\Re s=1/2$. For the character of conductor one this is the critical-strip assertion for $\zeta$. The proof also gives the usual formulation of RH excluding the trivial zeta zeros. The arithmetic part proves a bound on fluctuations in a weighted count of primes. The analytic part shows that a zero off the line would violate that bound on arbitrarily distant intervals.

For the zeta function one can see the objective before introducing a theta lift. Write $\Lambda(p^j)=\log p$ for $j\ge1$ and $\Lambda(n)=0$ otherwise. The quantity to be bounded is
$$
 G_1(x)=\sum_{n\le x}\Lambda(n)(x/n-1)-x\log x+(1+\gamma)x,
$$
where $\gamma$ is Euler's constant. The two centering terms remove the singularity at $s=1$ from the Mellin transform. A zero $\rho$ in the open strip then gives a pole of residue $1/[\rho(1-\rho)]$ for a simple zero, multiplied by its multiplicity in general. For $0<\delta<1/2$, if $\Re\rho>1/2+\delta$, that pole prevents $G_1(x)\le x^{1/2+\delta}$ from holding throughout arbitrarily late intervals $[Y,Y^{3/2}]$. For a Dirichlet character one uses a positive combination of the corresponding sums for its powers. A zero shared by several powers contributes with the same sign in the multiplicity numerator. The last part of this manuscript proves the implication from windows to zeros. [Jin's signed window criterion][analytic-jin]

How can geometry bound this sum over primes? For a nonzero integer, forced divisibility by $p^a$ puts $a\log p$ on the finite side of the product formula. The finite side here comes from derivatives of integral theta functions. The splitting of $p$ determines the derivative orders that contribute, and summing their contributions produces exactly the weight $(x/p^j-1)_+$. At infinity one estimates norms of period integrals of automorphic forms. The theta seesaw identity identifies these integrals with the arithmetic maps whose divisibility was counted. Their joint images must occupy enough independent directions for a determinant estimate to control the divisibility. Each successive lift increases the gain. The final error has competing terms of sizes $x/m$ and $m$, up to small powers of $x$, for a chain of $m$ lifts. Taking $m$ near $\sqrt{x}$ explains where the critical exponent enters the construction. The proof below tracks the additional costs of that choice. [Alpöge's explanation](https://alpo.ge/remark.pdf) · [Eto on the cost of a chain, §§2.4 and 6.3–6.4](https://hexagonmath.org/pdf/2611.01087v1#page=19) · [The four error terms][bridge-budget]

This manuscript gives the argument at the level of cited intermediate theorems. We work through the joint choice of arithmetic objects, the two estimates for the same integral period, and the deduction about zeros. The accompanying chapters develop the estimates. In particular the proof uses global Galois attachment, the local Langlands correspondence, integral PEL compactifications, theta identities and arithmetic volume theorems. Their precise versions and longer proofs are cited where they enter. The proof is due to Levent Alpöge and Claude. The reconstruction draws on the RH Lean Roadmap, Kaiwen Jin's translation and the other work credited below. The dependency checks in this project concern this exposition. [Formal source](https://github.com/CocoSgt/riemann-hypothesis-lean/tree/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4) · [Source comparisons](guides/EXTERNAL_PROOF_COMPARISON.md)

## Choosing the field, the forms and the levels together

Fix the primitive character whose zeros we wish to exclude. To probe primes, embed its cyclic group of characters in the character group of a larger abelian CM field $E$. The construction uses auxiliary odd primes $q,d$ and a power of two. For example, the host can be described inside a cyclotomic field using the kernel of the given character, the quadratic characters at $q,d$, and the classes congruent to $\pm1$ at the specified power of two. This supplies Frobenius labels. Weights assigned to selected labels will recover a positive combination of the powers of the original character. Every real scale in a long window must admit a compatible field and arithmetic data. A choice at a sparse set of unrelated scales would give no bound for the transform used at the end of the proof. [Fields, windows and rank range][read-host] · [The host theorem][read-supply]

The arithmetic constraint on the field concerns Galois cohomology. Let $S_p$ consist of the places of $E$ above $p$, and let $G_{E,S_p}$ be the Galois group allowing finite ramification only there. For each positive integer $k$ below the allowed rank define
$$
 \operatorname{Sha}_{p,k}(E)=\ker\!\left(H^1(G_{E,S_p},\mathbb Q_p/\mathbb Z_p(-k))
              \longrightarrow\prod_{v\mid p}H^1(E_v,\mathbb Q_p/\mathbb Z_p(-k))\right).
$$
These kernels measure a possible failure of local conditions to control a global class. Their lengths occur as errors when one projects an integral eigenspace lattice onto the desired summands. The window theorem supplies fields for which the lengths are finite and their sum, with each $p$ weighted by $\log p$, is at most $\sqrt b$, where $b=\exp(x^\varepsilon)$. At the completed scale $x$ this holds for all twists $1\le k<\lfloor x^{400}\rfloor$. Its proof uses arithmetic duality to separate signs of conjugation, Iwasawa-theoretic control of the small twists, and bounds from counting automorphic representations for the remaining terms. The global Galois inputs give Frobenius and inertia at primes away from $p$ and the required local information at $p$. These conditions connect the representations that are counted to the cohomology groups in the displayed formula. Theorem 2.1.1 of Barnet-Lamb, Gee, Geraghty and Taylor supplies one representation over the given CM field, with the prescribed Frobenius roots and crystalline filtration at spherical places. Comparing it after CM base change gives the required information at ramified places. The Roadmap builds the spherical representation by odd-rank approximation and subtraction of auxiliary characters in even rank. [Spherical attachment](notes/galois/SPHERICAL_GALOIS_ATTACHMENT.md) · [Ramified comparison](notes/galois/RAMIFIED_LOCAL_COMPARISON.md) · [Roadmap’s global statement][read-galois] · [The four counting inputs to the window][read-count] · [The window estimate][read-window] · [Integral comparison at the cyclotomic roots](notes/galois/CYCLOTOMIC_WACH_COMPARISON.md)

### Why the two estimates hold on the same interval

Fix the primitive target $\psi$ of conductor $M$ and $0<\varepsilon<1/52$. Write $P=2+8\varepsilon$ and $C=401$. Two estimates have to hold together. The first controls the prime sums belonging to the three nontrivial quadratic twists by $q,d$. The second controls the cohomology of the field cut out by those same primes and the power of two. The order of choice makes them compatible.

For the first estimate, the auxiliary-prime theorem works on every sufficiently late interval $[U,U^J]$ for fixed $J$. First select $q\equiv3\pmod 8$ so that all characters modulo $M$ twisted by $(\cdot/q)$ satisfy the required bounds. Then select $d\equiv7\pmod{16}$ in the prescribed progression for this $q$, simultaneously controlling the twists by $(\cdot/d)$ and by $(\cdot/q)(\cdot/d)$. The candidate-prime mean square controls the proportion whose finite sum is too large somewhere on the interval. The zero-density bound controls the candidates for which the primitive twist has a zero in $\Re s>399/400$ up to the required height. At each selection fewer than half of the candidates need be excluded once $U$ is sufficiently large. The resulting centered prime sums satisfy $|G_\chi(y)|\le y^{1/2+\varepsilon/2}$ on the entire interval. Every omitted character after translation averaging has one of these three nontrivial twists. Indeed, a character surviving that average restricts on the frame to a power of $\psi$, and the two remaining factors are the quadratic signs. Setting both signs to exponent zero gives a retained character. This square-root estimate is used for the omitted characters. At the thin positions one also uses a weaker prime-number-theorem estimate for every host character, including the retained ones, at much larger arguments. The signed square-root estimate for the retained powers of $\psi$ at $x$ will come from the theta periods. [Selection in two stages](https://github.com/rh-lean-roadmap/rh-lean-roadmap/blob/c7755c1086f05d0918ee8496d95912e4f35e22f9/docs/src/book/main.tex#L2997-L3057) · [Prime-sum conclusion](https://github.com/rh-lean-roadmap/rh-lean-roadmap/blob/c7755c1086f05d0918ee8496d95912e4f35e22f9/docs/src/book/main.tex#L3092-L3134) · [Which characters have this square-root bound](https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AutomorphicArithmetic/CharacterBoxes/BoundedTw.lean#L5-L56) · [Estimate for all characters at thin positions](https://github.com/rh-lean-roadmap/rh-lean-roadmap/blob/c7755c1086f05d0918ee8496d95912e4f35e22f9/docs/src/book/main.tex#L10931-L10939)

The cohomological estimate can require a smaller interval. Here is the underlying selection argument. At $2$ and a fixed finite set of odd primes, the cyclotomic-tower bounds give finitely many $\ell$-adic centres. Up to an integer cutoff $N$, a centre can be closer to at most one twist index than $\ell^{-\lfloor\log_\ell N\rfloor}$, since any two such indices are congruent modulo $\ell^{1+\lfloor\log_\ell N\rfloor}>N$. Taking the union across the relevant towers leaves at most $R$ exceptional indices, with $R$ independent of the outer scale $X$ and its chosen pair. At each of these indices one still has a bound from $H^2$ at a fixed layer, sufficient when the index is at most $v^\eta$ for a fixed $0<\eta\le C$. [Tower bounds and the residue argument](https://github.com/rh-lean-roadmap/rh-lean-roadmap/blob/c7755c1086f05d0918ee8496d95912e4f35e22f9/docs/src/book/main.tex#L12870-L12906) · [Small indices and the common window](https://github.com/rh-lean-roadmap/rh-lean-roadmap/blob/c7755c1086f05d0918ee8496d95912e4f35e22f9/docs/src/book/main.tex#L12911-L12970)

To see why a full interval survives, set $D=2C/\eta$ and $W_j=X^{1/(2D^j)}$ for $0\le j\le R$. The $R+1$ intervals of possible bad indices
$$
                 (W_j^\eta,W_j^{2C}]
$$
are pairwise disjoint, since $W_{j+1}^{2C}=W_j^\eta$. At least one contains no exceptional index. Put $W=W_j$ for that choice. If $W\le v\le W^2$, every exceptional $k\le v^C$ satisfies $k\le W^\eta\le v^\eta$. This bounds every exceptional index that still occurs, simultaneously for all real $v$ in the window, with $W^2\le X$ and $W\ge X^{1/(2D^R)}$. This pigeonhole proof gives the conclusion of the archive's window lemma. After the remaining odd-prime counts and the duality estimate are added, the cohomological theorem supplies its full weighted bound on a window $[W,W^2]$. [Formal window lemma](https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AutomorphicArithmetic/AutomorphicVarieties/LayeredIsomorphisms/Window1.lean#L6-L58) · [Assembly with the other prime classes](https://github.com/rh-lean-roadmap/rh-lean-roadmap/blob/c7755c1086f05d0918ee8496d95912e4f35e22f9/docs/src/book/main.tex#L12429-L12444)

Finally set $a(v)=\lceil\log_2(v^P)\rceil$ for $v\ge1$. The cohomological theorem for this function fixes $J$ first. Take $X$ arbitrarily large, put $U=X^{1/J}$, and choose $q,d$ analytically on $[U,X]$. The cohomological theorem applies to **every** pair with the prescribed congruences and sizes at $U$. For this pair it gives $W\ge U$, $W^2\le X$, and the bound through $\lfloor v^{401}\rfloor$ for every field with exponent $a(v)$ on $[W,W^2]$. The frame has size $c2^{a(v)}$ with $c\ge1$ fixed by $\psi$. Set $\lambda=c^{1/P}$, $Z=\lambda W$, and $v=x/\lambda$. For $Z\le x\le Z^{3/2}$ and $W\ge\max(\lambda^3,\lambda^{400})$ we have
$$
 W\le v\le x\le W^2,\qquad
 x^P\le c2^{a(v)}\le2x^P,\qquad
 x^{400}=\lambda^{400}v^{400}\le v^{401}.
$$
The nonnegative cohomology sum may be shortened to $1\le k<\lfloor x^{400}\rfloor$, and its budget $e^{v^\varepsilon/2}$ is at most $\sqrt b=e^{x^\varepsilon/2}$. The auxiliary rank satisfies $t\le\lfloor x^{400}\rfloor$, so every twist needed by the construction is covered. One can keep $q,d$ throughout this supply window. The exponent $a(v)$, and therefore the field supplied to the construction, can change with $x$. [Original rescaling and choice of the pair](https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AutomorphicArithmetic/CharacterBoxes/WinPairs.lean#L5-L81) · [Rank bound](https://github.com/rh-lean-roadmap/rh-lean-roadmap/blob/c7755c1086f05d0918ee8496d95912e4f35e22f9/docs/src/book/main.tex#L14618-L14669)

### Choosing a single family of theta maps

Over an eligible host the construction runs twice. The host determines the auxiliary split prime $q_0$ used for the functional grid by a least-prime condition. The completed-host estimate bounds its size, and the grid retains that same prime. [Exact dependence of the grid prime](guides/EXTERNAL_PROOF_COMPARISON.md#roadmap-v41-and-the-second-reading-of-the-condensed-proof) On the first pass it chooses a coefficient field, frames and an untwisted family of theta maps, with the initial localization set empty. Exporting its rational tests and norm choices specifies what must be kept in the second pass. That pass extends the same fields and levels, choosing characters that satisfy the required restrictions simultaneously for the relevant powers. Values of the additional field request that depend on the characters may be adjoined after those characters have been chosen. A linked bundle records the equalities that identify the complex realization, integral lattices and selected side with those of the constructed point. Identifying the actual objects lets a local division statement proved with the first description be applied to a complex period with the second. [Construction on one field and frame](notes/arithmetic/COMMON_DESIGN_WINDOW_TRANSFER.md) · [Selected objects and their identifications](notes/local/LOCAL_SELECTED_FAMILY.md)

A word is a string of $k-2$ bits. Its bits choose between separated values of the interior weight parameters. Two different words have a position at which their weights differ. The spectral calculation uses this differing position to distinguish their periods. Each word has a chain of $m$ theta lifts, and the same set of words is used at each prescribed translation of the host frame. [Choice of words, weights and translate](https://github.com/rh-lean-roadmap/rh-lean-roadmap/blob/c7755c1086f05d0918ee8496d95912e4f35e22f9/docs/src/book/main.tex#L42848-L42856) · [Use of the differing bit](https://github.com/rh-lean-roadmap/rh-lean-roadmap/blob/c7755c1086f05d0918ee8496d95912e4f35e22f9/docs/src/book/main.tex#L46246-L46251)

There is a logical issue even after individual points can be made. An estimate proved for one convenient point need not hold for the point that will satisfy a second estimate. The construction proves properties that hold for every linked bundle over a sufficiently late member satisfying a specified condition. Finitely many such conditions can be intersected at their respective stages, taking the maximum of numerical thresholds only after the arguments of those thresholds have been fixed. The functional estimate is an implication conditional on division, uniform in the subsequent selector. The geometric estimate is proved for every admissible reference realization, also before choosing a selector. The two-pass construction can therefore select one bundle satisfying both and retain it at each of the translates prescribed by the host. In the height theorem division is an antecedent. In the application to zeros the cohomological host bound proves it for this family, since the reference rank in the projection estimate is the actual rank of the selected row. [Functional bound](notes/construction/FUNCTIONAL_BEFORE_FAMILY_SELECTION.md) · [Joint family and height theorem](notes/geometry/COMMON_FAMILY_AND_PERIOD_HEIGHT.md) · [Denominator on the host](notes/periods/PERIOD_FINITE_ERRORS_ON_THE_DESIGN.md)

## How the theta tower turns prime splitting into divisibility

There are three questions to keep in view. How small are the images of integral forms at the complex embeddings, after dividing out their forced prime factors? How much of the row space do those images occupy? How small can their joint covolume be once their denominators are accounted for? The reading of Sernau and collaborators’ condensed proof, directed by Bartosz Naskręcki, organizes these questions into its Theorems A, B and C. In the original argument here, the second question must be answered again for every step of a slope filtration. [The three bounds in the condensed proof](https://github.com/nasqret/riemann-rev/blob/f30fe9229ab2a5acde1e6274f1887ffe994360a0/writeup/overview.tex#L286-L324)

The construction needs many integral maps into one space. Each map follows a chain of lifts indexed by a word $u$ in the chosen finite family. Its finite-prime divisibility will give a lower bound involving primes. Its complex realization will tell us how much of the target these maps see together. Both calculations concern the same maps, including their lattices, measures and norms. For a single nonzero integer this principle is the product formula $\sum_p v_p(n)\log p=\log|n|$. Here the determinant of a lattice replaces the integer, and the presence of many maps makes a bound on the target's *mean* slope possible. [Alpöge's description of the construction](https://alpo.ge/remark.pdf) · [The global comparison](../research/modules/construction/global_assembly/main.tex)

A theta lift between two unitary groups uses their commuting actions in the oscillator representation. A Schwartz function specifies the theta kernel. Summing it over rational lattice points produces an automorphic function of the two group variables. Pairing against a cusp form in the first variable gives a form in the second. At finite places the construction prescribes lattice functions and level characters. At infinite places the polynomial part of the Schwartz function realizes the required weights. Consecutive lifts vary the Hermitian spaces and weights while keeping the markings that will identify their rational structures. At the terminal step we take the indicated Fourier coefficient and evaluation. On integral sections this gives an arithmetic pairing. On the automorphic side the same operations give the Bessel period, an integral against the specified character of a unipotent subgroup and the form on its unitary stabilizer. [Fixed-stage theta realization](notes/theta/THETA_FIXED_STAGE_REALIZATION.md) · [The selected terminal Fourier coefficient](notes/periods/PERIOD_SELECTED_FOURIER_WORD.md)

### How the seesaw fixes the comparison scalar

Fix a word and a tuple of level characters. Write $P$ for its Bessel period operator, with the full Hilbert space of rows as target. At this point two facts are needed. A column in the required ramified source must have nonzero period. Its value must occur as the bottom row of the reference theta tower. The first fact is spectral and the second uses theta lifting.

For the first, put $K=\alpha^{-1}P^*P$ with the positive normalization of the diagonal Gram estimate. If the source has dimension $d$, that estimate gives $\|K-I\|_{\rm HS}^2\le ed$. Each unit vector in an orthonormal basis of $\ker P$ contributes exactly one to this squared norm. Hence $\dim\ker P\le ed$. The ramified column space has dimension at least $d/2$, and $e<1/2$ on the selected window. Choose there a column $\phi$ with $p=P\phi\ne0$. This is the kernel argument in Chen and Jin. [Chen's nonzero column][ed3-chen-column] · [Jin's diagonal estimate and ramified dimension][ed3-jin-column]

For the second, let $D$ denote descent from the full reference terminal rows to the bottom multiplicity space. The doubling formula at the prescribed local tests gives a nonzero adjoint lift for every nonzero vector of each reached bottom Hecke eigenspace. The finite character at a level cancels the character of its test. At a real place the local factor is a positive constant times the squared norm of the matched nonzero harmonic projection. Distinct unramified Hecke parameters stay distinct on ascent because one twists them by the same character and adjoins the same multiset of roots. Cancellation of multisets works with repetitions. The images of distinct eigenspaces are therefore independent, so $D^*$ is injective and $D$ is onto. Full translated evaluation at the distinguished character supplies a bottom row $y$ with value $p$. One possible terminal preimage is $D^*(DD^*)^{-1}y$ in the finite multiplicity spaces. Pairing the descended row with the column gives the reference value $b_*=\langle p,p\rangle>0$. This step takes place before projection to the arithmetic good rows. [Doubling at the prescribed tests and separation of the parameters](notes/periods/PERIOD_REFERENCE_ROW_DESCENT.md) · [Jin's evaluation and translation][ed3-jin-target]

Here is the linear algebra that turns this single value into an identity at every character tuple $t$ of the word. Write $A_t$ and $B_t$ for the arithmetic and automorphic pairings on corresponding tests. At each pair of consecutive lifts, unfolding the lower integral expresses it as an integral of upper evaluations of the matched theta kernels. The local test factors and the quotient measures give a prescribed nonzero scalar $c_t$. For example, in the finite level average the kernel translate belonging to $h$ carries weight $\chi(h)^{-1}$, and the level vector contributes $\chi(h)$. Their product is one throughout the sum. In passing two lifts at a time, the remaining real frames and their expansion coefficients are common to the two tuples. Thus a linear relation that vanishes in those frames still vanishes after the integrations. Denoting the normalized top value of the full reference test by $a_*$, this gives
$$
 \lambda a_*+\mu c_t A_t=0
 \quad\Longrightarrow\quad
 \lambda b_*+\mu B_t=0
 \qquad(\lambda,\mu\in\mathbb C).
$$
Taking $(\lambda,\mu)=(1,0)$ shows $a_*\ne0$. Taking $(c_t A_t,-a_*)$ then gives $a_* B_t=b_*c_t A_t$, including for tests with zero pairing. The same reference works throughout this word. Dividing $c_t$ by its value at the reference tuple isolates the relative tuple factor. The column similarity of each word splits into a positive scale and a unitary map. On the rows the construction uses a single finite central translation, fixed before choosing the word. Its action is unitary for the common Petersson measure. Two image vectors at different words therefore retain their mutual inner product under this target change, as required in the Gram estimate. [Chen's two-step recursion and two-tuple relation][ed3-chen-joint] · [Jin's measured scalar identity][ed3-jin-scalar] · [The original arithmetic row inputs and local factors](notes/periods/PERIOD_ARITHMETIC_ROWS_IN_THE_SEESAW.md)

[ed3-chen-column]: https://github.com/yyyyychen/RH-Natural-Language-Proof/blob/d4dfb1a282dbf857288e73eb1f546dbfcc5899b8/tex/period-transport.tex#L795-L817
[ed3-jin-column]: https://github.com/yuiyuiui/Natural-Language-Proof-Generalized-Riemann-Hypothesis/blob/405237610e58ab9d4a9d5d54d9a0548a0c44227c/sections/e-period-comparisons.tex#L1893-L1916
[ed3-jin-target]: https://github.com/yuiyuiui/Natural-Language-Proof-Generalized-Riemann-Hypothesis/blob/405237610e58ab9d4a9d5d54d9a0548a0c44227c/sections/e-period-comparisons.tex#L1935-L1973
[ed3-chen-joint]: https://github.com/yyyyychen/RH-Natural-Language-Proof/blob/d4dfb1a282dbf857288e73eb1f546dbfcc5899b8/tex/period-transport.tex#L626-L659
[ed3-jin-scalar]: https://github.com/yuiyuiui/Natural-Language-Proof-Generalized-Riemann-Hypothesis/blob/405237610e58ab9d4a9d5d54d9a0548a0c44227c/sections/e-period-comparisons.tex#L1975-L2021

### The weight contributed by a prime

The finite calculation takes derivatives of integral theta sections in prescribed flag directions. In a height-two local model, the factorial in a derivative and the allowed denominators of its Taylor coefficient give the difference of the geometric series $1/(p-1)$ and $1/(p^2-1)$. Their difference is $p/(p^2-1)=\sum_{j\ge1,\ j\text{ odd}}p^{-j}$. Chenxin Huang explains this model through supersingular reduction at primes inert in an imaginary quadratic field. Katz's divisibility theorem makes the coefficient precise for trace-zero functions on a height-two Lubin–Tate group. The tower requires the corresponding bounds on its actual multivariable determinant derivatives, with the weight order available at the Frobenius-translated flag. [Huang, §1.3.4](https://hexagonmath.org/pdf/2611.00833v1#page=3) · [Katz, Main Theorem 3.11](https://web.math.princeton.edu/~nmk/old/divcongCartier.pdf) · [Integral determinant derivatives](../research/modules/construction/determinant_jet_v57/main.tex)

Consider one order $a>0$, one allowance $w>0$, and the quadratic character $\chi_K$ of an imaginary quadratic field $K$. The surplus at odd exponent $j$ of an inert prime is $(a/p^j-w)_+$, where $z_+=\max(z,0)$. Put $y=a/w$. For unramified primes the identity
$$
 2\sum_{p\ {\mathrm{inert}}}\log p\!
   \sum_{j\ge1,\, j\ {\mathrm{odd}}}(a/p^j-w)_+
 =w\sum_{p\nmid\mathrm{disc}(K)}\sum_{j\ge1}
 (1-\chi_K(p^j))\log p\,(y/p^j-1)_+
$$
follows prime by prime. The factor on the right is two exactly on the terms counted on the left and zero on the other unramified powers. This explains the kernel $(y/n-1)_+$ against the von Mangoldt function. In the actual family the allowance depends on the step, word and CM embedding. Frobenius at $p$ determines the partner embedding at each exponent. At a ramified prime one averages over the inertia coset. Summing these local gains with the finite-place weights, then averaging over the selected translates, gives the corresponding character combination of smoothed prime sums. The exceptional ramified contribution is included with its own weight. [Local allowances and Frobenius partners, GLG.1–4](../research/modules/construction/global_local_gain_v46/main.tex) · [Inertia average and exact expansion, CMP.8–10](../research/modules/construction/conditional_main_v42/conditional_main.tex)

The top derivatives have a common degree constraint at an inert prime. At a top $s$ let $\alpha_s$ count its marked linear factors and let $w_{s+d}$ count the remaining minors at the position $d$ steps away. Extract all marked factors at once as the coefficient of $\prod_b t_{s,b}^{e(s,b)}$, with $\sum_b e(s,b)=\alpha_s$. A mixed kernel term at odd distance $d$ consumes $p^d$ units of this degree. A term joining two tops is assigned once to the endpoint with the larger Frobenius exponent. At that endpoint it consumes at least $p^d$ units, where $d$ is its first positive distance to the other endpoint. Thus the counts contributing to a single coefficient obey $\sum_d p^d n_d\le\alpha_s$. Except at these first distances to opposite-parity tops, one also has $n_d\le w_{s+d}$. Indeed, the translated matrix at $s+d$ changes by rank one. Two replacement columns of any minor are proportional, so each remaining minor accepts at most one such factor for fixed $s,d$. The ordinary local gain at $s$, before the digit error, is consequently at least $p\alpha_s/(p^2-1)-N_s$, where $N_s$ is the maximum number of occurrences allowed by these constraints. Filling the available slots in increasing $d$ computes $N_s$ and recovers the usual positive-part bound. [Coordinatewise inequality](https://github.com/rh-lean-roadmap/rh-lean-roadmap/blob/c7755c1086f05d0918ee8496d95912e4f35e22f9/docs/src/book/main.tex#L4656-L4679) · [Pure and mixed occurrences in the determinant expansion](https://github.com/jimjamzola/RH-Alpoge-Reconstruction/blob/9eefc08b0819728d4dd2ef0568b49a61251af111/manuscript/sec8_gain.tex#L230-L265) · [Full count and an example at five](notes/arithmetic/FINITE_DERIVATIVES_AT_AN_INERT_PRIME.md)

A related calculation measures the cost of a local test on the reference component. Over an odd unramified prime, the Hodge–Tate estimate bounds the determinant of character differentials on a full eigenspace. Choose columns of that matrix successively using pivots of least valuation. The product of the first $j$ pivots generates the ideal of the minors on the first $j$ rows. Thus one list of actual formal characters works at every step of the flag. For an inert prime and signature $(P,Q)$ the upper depth per derivative is $(Pp+Q)/(p^2-1)$, independent of the flag step. The proof of the lower divisibility estimate uses its own integral test. [The local arithmetic, simultaneous minors and Frobenius sum](notes/geometry/FROBENIUS_CHARACTER_FLAG.md)

### Passing the finite estimates through the lifts

An integral derivative gain reaches the terminal map only to the extent that the intermediate theta image occupies its prescribed lattice. At a coefficient place $v$ keep the integral cut in each stage, meaning the sublattice on which the required local division holds. The length of the quotient by the cut bounds how many powers of the local uniformizer may be lost in taking determinants. Rational surjectivity only determines the rank. The paired image indices at $v$ and its conjugate measure the remaining defect, and the index for the dual pairing records the actual Hermitian form. Their signs matter because the level-normalizing term from the two places cancels a term in the global main expression. The division and rank estimates bound the weighted sum of the cut lengths in every layer. The two auxiliary arithmetic runs handle exceptional residue characteristics with the same target rank. Their estimates, together with the reference covolume, bound the total error on the chosen lattice. [Finite indices on the chosen family](notes/periods/PERIOD_FINITE_ERRORS_ON_THE_DESIGN.md) · [Full measured operator and its signed determinant](notes/periods/PERIOD_JIN_FULL_THETA_TRANSFER.md)

Here is why a *Galois cohomology length* enters this lattice calculation. Over a discrete valuation ring $O$ with uniformizer $\varpi$, consider two systems of Hecke eigenvalues with integral algebra $\{(a,b)\in O^2:a-b\in\varpi^hO\}$. An operator killing the second system must act on the first by a multiple of $\varpi^h$. Thus even a rational projector of rank one can cost an arbitrarily large denominator. In the tower, take all integral operators that vanish off the theta locus. At a selected eigenpoint $\pi$ their values form an ideal $\mathfrak c_\pi$. Its length loss is $\operatorname{length}_O(O/\mathfrak c_\pi)$.

To bound this length, take a matrix of relations among generators and form its determinant with indeterminate coefficients. Every unwanted eigensystem has a nonzero solution of the relations, so the determinant vanishes there coefficient by coefficient. At $\pi$ it factors into block determinants. In each block one can choose relations in Smith normal form for which the valuation equals the length of the module of torsion solutions. The least coefficient valuation is additive under polynomial multiplication. This allows a different choice of relations for each block and bounds the congruence length by the *sum* of those solution lengths. The Galois action turns solutions into cocycles. After accounting for the allowed local images, the negative Tate twists contribute exactly the kind of strict local-to-global kernel bounded on the chosen window. The other blocks have their own terms. [The determinant argument, local conditions and normalizations](notes/galois/HECKE_CONGRUENCES_AND_SELMER_LENGTHS.md)

### Why a family of period maps controls the mean slope

Fix one translated point. Write $N'_u$ for its divided source lattice at word $u$, and $C=RR^\vee$ for the common dual row lattice. The integral map $B_u:N'_u\to C$ has height at most $h_u$ whenever it is nonzero. The height here is the average, over the complex places of the totally complex coefficient field $K$, one embedding per place, of the logarithm of the **squared** operator norm. At one specified complex place the maps have a second description. There is a normalized full period $A_u:V_u\to Z$ on every word. Restrict its source to the ramified subspace representing $N'_u$, project its target onto the row space representing $C$, and make the given invertible coordinate changes. The result is $B_u$. The target change of coordinates is the same for every word. This allows us to measure the dimension of the sum of their images. [Formal height and coordinate hypotheses][gram-native] · [Period realization on the selected row][gram-row]

A spanning statement alone says how many target directions the full family reaches. The arithmetic comparison also requires control after removing the directions of small slope, and the directions removed depend on the cutoff. The two moments of the Gram operator give this control.

Let $f_u=\dim V_u$, $M=\sum_u f_u$, and $D=\dim Z$. The spectral estimates control the overlaps between the full periods. Set $Q=\sum_u A_uA_u^*$ and $t=\operatorname{tr}Q$. The diagonal estimate gives $\sum_u\|A_u^*A_u-I\|_{\mathrm{HS}}^2\le eM$. Put $a=\sqrt e$. Cauchy–Schwarz, summed over the words, gives $t\ge(1-a)M$. The mixed estimates bound the off-diagonal terms of the identity $\operatorname{tr}(Q^2)=\sum_{u,v}\|A_u^*A_v\|_{\mathrm{HS}}^2$. On the design window these bounds give
$$
      D\operatorname{tr}(Q^2)\le(1+\eta)t^2,
      \qquad \eta=5\tau,\quad \tau=x^{-C_H}.
$$
Indeed $D\operatorname{tr}(Q^2)/t^2$ is at most $(1+\eta_1)[1+\eta_0+\tau(1+a)^2]/(1-a)^2$. Here the mixed bound has factor $1+\eta_0$, the full target dimension is at most $(1+\eta_1)D^\star$, and the supply of words gives $M\ge D^\star/\tau$. For $\eta_0,\eta_1,a\le\tau/2$ and $0<\tau\le1/4$ the ratio is at most $1+5\tau$. [Full Gram calculation and scalar inequality](../research/modules/spectral/gram_frame/gram_frame_section.tex#L22-L86) · [Original size and rank hypotheses][gram-size]

For two distinct words $u,v$, the identity orbit has zero local pairing and the remaining zero-Gram orbits give intertwiners between inequivalent compact types. Their contributions vanish. In the square of the other orbital sums the main contribution comes from generic pairs of corank one whose flag identifications satisfy the scalar quotient tests. Its leading coefficient is one. The zero Fourier frequency at each singleton flag step reproduces the previous energy, while a final block of $j\ge2$ steps costs at most $h^{j-1}$, with $h\le(C/k^{1/16})^f$. Summing these alternatives raises the normalized energy by at most $(1+2h)^{2(r+1)}$ through all the flag steps. The other orbital errors decay exponentially at the constructed ranks. The two distinguished split primes contribute the explicit finite operator factor $\prod_{i=0}^1\prod_{a=1}^{k-1}(1-g_i^{-a})^{-f}$. In particular, on the completed families the distinct-word squared overlap is at most $[1+(1+o(1))f(g_0^{-1}+g_1^{-1})]f_uf_v/D^\star$. For an equal word the identity gives $I$ and the other zero-Gram orbits require a separate estimate. [The two orbital sums, the finite factor and uniformity](notes/theta/MIXED_PERIODS_AT_THE_CONSTRUCTED_RANKS.md)

Take any subspace in each full source and let $E_u$ project onto its orthogonal complement. Suppose the total omitted dimension is $zM$. The span of the retained images is the image of the positive operator $Q'=\sum_u A_u(I-E_u)A_u^*$. The trace it loses is
$$
 \ell=t-\operatorname{tr}Q'
   =\sum_u\operatorname{tr}(E_u A_u^*A_u)
   \le M\bigl(z+\sqrt{ez}\bigr).
$$
The identity part contributes exactly $zM$. For the rest use Cauchy–Schwarz and $\sum_u\|E_u\|_{\mathrm{HS}}^2=zM$.

To measure the directions lost in the target, let $P$ project onto the complement of the retained images and $p=\operatorname{tr}(P)/D$. Since $PQ'=0$, we have $\operatorname{tr}(PQ)\le\ell$. Centering both matrices gives the argument of Subbarao's Theorem 19.1. Write $\eta_*=D\operatorname{tr}(Q^2)/t^2-1$. As $\|P-pI\|_{\rm HS}^2=Dp(1-p)$ and $\|Q-tI/D\|_{\rm HS}^2=\eta_*t^2/D$, Cauchy–Schwarz gives
$$
 p\le \frac{\ell}{t}+\sqrt{\eta_*p(1-p)}
   \le \frac{z+\sqrt{ez}}{1-a}+\frac p4+\eta_* .
$$
For example, in a perfectly uniform frame with $e=\eta_*=0$, removing a fraction $z$ of all source dimensions misses at most a fraction $z$ of the target. The general bound holds for *every* collection of removed directions. This allows a different choice at each slope threshold. [Subbarao, Theorem 19.1, pp. 38–39](https://github.com/muralisubbarao2/Refinements-and-Extensions-to-Alpoge-Claude-proof-of-Riemann-Hypotheisis/blob/4c3cb4f5e43212ec8c0ae759502291ae16e3df02/Ram-Calculus-Alpoge-RH-Nov24-v2.pdf#page=38) · [Exact rank bound and its integral](notes/theta/CENTERED_PERIOD_RANK_AND_SLOPE.md)

For a Hermitian lattice, its Harder–Narasimhan filtration groups the directions by decreasing slope. Use the archive's normalized slopes $2\lambda+c_K$, where $\lambda$ is the real covolume slope and $c_K=\log|\operatorname{disc}K|/[K:\mathbb Q]-\log2$. Each constituent of $K$-rank $r$ contributes $r$ copies when we count dimensions over $K$. The real-rank list repeats each copy $[K:\mathbb Q]$ times and gives the same fractions and means. In $N'_u$ subtract $h_u$ from each normalized slope. Let $s$ be the mean of all these adjusted slopes together, and let $s+U$ be their largest value. Take $H\ge0$ such that the minimum slope of $C$ is at least $s-H$. [Slope and height normalization][gram-normal] · [Weighted mean, spread and target floor][gram-mean]

At threshold $s-v$, retain the source filtration step of adjusted slopes at least $s-v$. Its image lies in the target filtration step of slopes at least $s-v$. Indeed, compose the map on the retained step with projection onto the quotient by this target step. A nonzero composite would have source minimum slope at least $s-v+h_u$, target maximum slope strictly below $s-v$, and height at most $h_u$. This contradicts the nonzero-map slope inequality. That inequality follows by dividing by the kernel and taking determinants on the saturated image. Integrality gives an inclusion of determinant lattices, and the operator norm on each exterior determinant is at most the original operator norm raised to the image rank. The quotient's mean slope is at least the source minimum, and the saturated image's mean slope is at most the target maximum. [Bost and Chen, Proposition 2.10(3)][gram-bost] · [The source and target filtration steps][gram-filter]

Let $q(v)$ be the fraction of the adjusted source slopes below $s-v$, and $p(v)$ the fraction of the target slopes below it. If $d$ is the fraction of full source dimensions initially lost on passing to the ramified subspaces, the omitted fraction in the full calculation is $z=d+(1-d)q(v)$. Write $1-\delta=\operatorname{rank}_K C/D$. Projection to the rows can only decrease the absolute codimension of the span of the images. The centered estimate, applied before this projection, therefore gives
$$
 (1-\delta)p(v)\le\frac43
 \left(\frac{d+(1-d)q(v)+a}{1-a}+\eta_*\right).
$$

The integral of $q(v)$ over $[0,H]$ is the average of $\min\{H,(s-\lambda)_+\}$ over all adjusted source slopes $\lambda$. For $U+H>0$ this quantity at each $\lambda\le s+U$ is at most $H(s+U-\lambda)/(H+U)$. The inequality follows on the three intervals cut out by $s-H$ and $s$. Its average is therefore at most $UH/(U+H)$. On the target, the lower bound $s-H$ ensures that integrating $p(v)$ gives the full average positive deficit, which dominates $s-\mu(C)$. Consequently, for $H>0$,
$$
 (1-\delta)(s-\mu(C))\le \frac43\left(
   \frac{(d+a)H+(1-d)UH/(U+H)}{1-a}+\eta_*H\right).
$$
For $H=0$ the target floor gives $s\le\mu(C)$. We can now use the ranks of the words actually constructed. Their number is $\lceil3\Gamma^2/\tau\rceil$, and each column has dimension at least $(1-k2^{-k})D^\star/\Gamma^2$. Thus the diagonal contribution $D^\star/M$ in the second moment is at most $\tau/[3(1-k2^{-k})]$. Since $a,\eta_0,\eta_1,d=o(\tau)$, we obtain $\eta_*\le(1/3+o(1))\tau$. Return to the centered inequality before its last estimate and use $\sqrt{\eta_*p}\le p/12+3\eta_*$. The integral of $3\eta_*$ over the cutoffs is at most $(1+o(1))b$, because $H\le b/\tau$. The contribution from $d+a$ is $o(b)$, the source contribution is at most $(1+o(1))U$, and $\delta=o(1)$. Hence for every $\xi>0$, beyond one common cutoff,
$$
 s\le \mu(RR^\vee)+(12/11+\xi)(U+b).
$$
In particular the coefficient $11/10$ suffices for the prime comparison. [Exact word count and integration of the centered bound](notes/theta/CENTERED_PERIOD_RANK_AND_SLOPE.md#the-factor-three-in-the-selected-code) · [Original family inequality][gram-native]

Finite divisibility gives the reverse comparison between $s$ and the prime gain. At each translate the gain plus $\mu(RR^\vee)$ is bounded above by $s$ plus the arithmetic main term and its specified errors. Combining the two inequalities cancels the dual row slope and leaves an upper bound for the prime gain. [Uniform frame parameters](../research/modules/spectral/gram_frame/gram_frame_section.tex#L115-L139) · [Signed lower bound for the mean][gram-gain]

[gram-native]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Formalism/HarderNarasimhan/StatementFrameF.lean#L64-L99
[gram-row]: https://github.com/rh-lean-roadmap/rh-lean-roadmap/blob/6c23d34a14a3ecf19504ed4182596217ca75006b/docs/src/book/main.tex#L10673-L10718
[gram-size]: https://github.com/rh-lean-roadmap/rh-lean-roadmap/blob/6c23d34a14a3ecf19504ed4182596217ca75006b/docs/src/book/main.tex#L10650-L10684
[gram-frame]: https://github.com/rh-lean-roadmap/rh-lean-roadmap/blob/6c23d34a14a3ecf19504ed4182596217ca75006b/docs/src/book/main.tex#L35546-L35591
[gram-normal]: https://github.com/rh-lean-roadmap/rh-lean-roadmap/blob/6c23d34a14a3ecf19504ed4182596217ca75006b/docs/src/book/main.tex#L10462-L10512
[gram-mean]: https://github.com/rh-lean-roadmap/rh-lean-roadmap/blob/6c23d34a14a3ecf19504ed4182596217ca75006b/docs/src/book/main.tex#L10682-L10699
[gram-bost]: https://webusers.imj-prg.fr/~huayi.chen/Recherche/bost_chen.pdf#page=26
[gram-filter]: https://github.com/rh-lean-roadmap/rh-lean-roadmap/blob/6c23d34a14a3ecf19504ed4182596217ca75006b/docs/src/book/main.tex#L35593-L35619
[gram-gain]: https://github.com/rh-lean-roadmap/rh-lean-roadmap/blob/6c23d34a14a3ecf19504ed4182596217ca75006b/docs/src/book/main.tex#L10993-L11010

## How arithmetic volume bounds a period lattice

A cusp form can be small for the Petersson norm at infinity and still have large denominators at finite places. The period estimate needs simultaneous control of both. Its geometric term is the logarithmic covolume of an integral lattice of cusp forms in a specified Hermitian space. The measure, the integral structure, and the component of the moduli space all come from the chosen arithmetic datum. A dimension formula alone says nothing about this covolume. The proof obtains the needed bound by counting sections satisfying norm bounds at every place. [The covolume on the original datum](notes/periods/PERIOD_JIN_FULL_THETA_TRANSFER.md)

A one-dimensional lattice already exhibits the positive part in the lower bound. Over $\operatorname{Spec}\mathbb Z$, fix a prime $p$ and integer $k\ge0$, take $p^k\mathbb Z$ as the integral line and give its rational coordinate the norm $e^{-a}|z|$. In degree $m$, the integral sections at threshold $e^{mt}$ number
$$
 1+2\left\lfloor e^{m(a+t-k\log p)}\right\rfloor .
$$
The logarithm of this number divided by $m$ tends to $(a+t-k\log p)_+$, also along $8\mid m$. Each unit of finite divisibility subtracts $\log p$ from the archimedean allowance. Strictly below that threshold only the zero section is counted. At equality there are three sections in every degree and their logarithmic growth rate is zero. On a flag component the dimension is $d$, the scale is $m^{d+1}/d!$, and a geometric degree multiplies the shifted component slope.

Fix a nonterminal layer, its marked covering space, and a component $Z$. Over that component take the complete flags in the Lie eigenspaces. Write $d$ for the dimension of the resulting flag space and $F$ for its field of definition. Two weights enter the argument. The cusp forms of weight $u$ give the projective coordinates used to measure the lattice. Subtracting a prescribed multiple of the Hodge weight gives a strictly decreasing weight $u'$, for which the intersections of the flag lines can be estimated. If $n_m(t)$ counts integral sections of weight $mu'$ with supremum norm at most $e^{mt}$, put
$$
 V_Z(t)=\limsup_{8\mid m,\ m\to\infty}
       \frac{d!\log n_m(t)}{[F:\mathbb Q]m^{d+1}} .
$$
At the specified bad and small primes the integrality condition uses the flag coming from the Hodge–Tate map. At the other primes it uses the ordinary integral flag. The factor of eight comes from the weight of the multiplier that will take these sections back to the original series. [The mixed lattice and arithmetic volume](notes/periods/PERIOD_VOLUME_BEFORE_SELECTION.md)

### Counting sections of the shifted weight

On a finite cover of the flag space the graded lines of these flags have integral models. Their arithmetic intersection yields a component slope $a_Z$. Smooth approximations to their metrics permit application of Moriwaki's lower bound for arithmetic volume. To count cusp forms, multiply the resulting sections by a fixed boundary section to the appropriate power. Its vanishing at the boundary controls the logarithmic growth of the metric; after division by the degree the smoothing loss tends to zero. The exponents in each approximation are chosen divisible by eight, so its volumes contribute to the limsup defining $V_Z$. [Boundary vanishing and the arithmetic intersection bound](notes/periods/PERIOD_VOLUME_BEFORE_SELECTION.md#the-volume-on-one-component) · [Comparison of the integral flag models](notes/periods/GOOD_ROOT_TOWER_COMPARISONS.md)

Suppose the covering function field has degree $h$ over the original flag field. Choose $h$ elements forming a field basis and clear their poles by one section of fixed weight. Multiplying a model section by these elements and taking all $h$ field traces determines the section, since the trace pairing is nondegenerate. The number of model sections is consequently at most the $h$th power of the corresponding count on the base. In the logarithmic count this factor cancels the covering degree in the arithmetic intersection. Comparing the integral flag lattices twice costs $2c_2\|u'\|_1$ per unit weight, where $c_2$ is the weighted sum of the local flag discrepancies. Thus, with $s_Z=a_Z-2c_2\|u'\|_1$ and $\delta'_Z$ the degree of the shifted line,
$$
 V_Z(t)\ge \delta'_Z(s_Z+t)_+,\qquad x_+=\max(x,0).
$$
The arithmetic intersection calculation bounds the mean of $s_Z$ over the components. Individual slopes may differ. [Trace, lattice discrepancies and mean slope](notes/periods/PERIOD_VOLUME_BEFORE_SELECTION.md#two-lattice-changes-and-one-field-trace)

### Transferring these sections to the original coordinates

On $Z$ choose a nonzero theta section $\Theta_Z$ of weight $8(u-u')$. At $m=8k$, multiplication by $\Theta_Z^k$ takes weight $mu'$ to $mu$. To read the product as a section on the projective image, one must check its order after dividing by a degree-$m$ chart frame. Let $s_i$ be an integral weight-$u$ generator whose projective coordinate defines the chart. The coordinates $s_j/s_i$ of the other generators are regular there. Hence on any integral trait in this chart $s_i$ has least order among the generators, in any common frame.

This test reaches possible vertical poles even though the estimates for theta derivatives use complete discrete valuation rings with finite residue field. If a rational chart coordinate has a pole along a vertical divisor, its reciprocal vanishes on an open of that divisor. Through a closed point there cut a horizontal arithmetic curve whose generic point lies in the marked flag interior. Normalizing and completing a branch gives a trait of finite residue field which still sees the pole. Its generic flag has an integral adapted frame after a triangular change. Both numerator and denominator have weight $mu$, so their quotient is unchanged. On this trait the reference-depth estimate bounds the least generator order above, and the theta estimate bounds the multiplier order below. The two inequalities contain the same degeneration term. Their difference leaves a finite correction absorbed by a single coefficient-field scalar $b_m$. This excludes a pole for $b_m\Theta_Z^k f/s_i^m$. Horizontal regularity follows from the complex chart estimate and vanishing at the cusp. Normality now gives a section on the normalization of the projective image. [Proof of the vertical test](notes/periods/PERIOD_VERTICAL_TRAIT_DETECTION.md) · [Kaiwen Jin, carrying section and chart calculation](https://github.com/yuiyuiui/Natural-Language-Proof-Generalized-Riemann-Hypothesis/blob/405237610e58ab9d4a9d5d54d9a0548a0c44227c/sections/j-arithmetic-covolume.tex#L5273-L5361)

At infinity let $G_y$ be the sum of squared point norms of a Petersson-orthonormal basis of the component cusp space. The bound on $\|\Theta_Z^k\|^2$ contains $G_y^m$. The Fubini–Study norm of a degree-$m$ section divides its squared point norm by exactly $G_y^m$. A redundant integral generating list can define the projective image; its complex norm is still induced by the Petersson space. The finite norms in the Chow height use that generating list, while its complex sphere integral uses the Petersson Gram at each embedding. Complex conjugation transports the norm to the other embedding of each pair. This identifies the metric in the upper volume bound with the metric in the determinant computation. [The metric and both frame dimensions](notes/periods/PERIOD_VERTICAL_TRAIT_DETECTION.md#the-metric-at-all-embeddings-and-the-dimension-of-the-chow-sphere)

On the normalized image the integral coordinate sections still generate the line. At the required metric shift they all have supremum norm at most one. To check nonnegative degree on a horizontal arithmetic curve, choose one of them nonzero at its generic point. Its finite divisor is effective and each archimedean contribution is a negative logarithm of a norm at most one. On a vertical curve global generation gives nonnegative degree, and the curvature at infinity is semipositive. The arithmetic Hilbert–Samuel formula therefore applies directly to the eighth tensor power on the normalization. Its generic degree-one projection preserves the arithmetic self-intersection. This proves the upper section count on precisely the multiples of eight used for the lower count. [The two volume theorems and the weighted slope calculation](notes/geometry/NORMALIZED_VOLUME_AND_COMPONENT_SLOPE.md)

### Recovering the covolume needed for divisibility

Write $\delta_Z$ and $h_Z$ for the degree and normalized Chow height of the original image, and $c_s$ for a common logarithmic norm bound for its integral generators. Above this bound the shifted image line is arithmetically nef. Its upper volume at threshold $t$ is $\delta_Z(h_Z+t)$. This holds on the normalization along multiples of eight by arithmetic birational invariance applied to the eighth tensor power. If $c_c$ is the total shift in the multiplication and scalar-balancing step, injectivity and the source lower bound give the principal comparison
$$
 \boxed{\delta'_Z(s_Z+c_s)_+\le \delta_Z(h_Z+c_s+c_c).}
$$
One first allows an arbitrary $\eta>0$ in the target threshold to absorb constants of fixed degree, then lets $\eta$ tend to zero. [Source and image bounds on the same degree progression](notes/periods/PERIOD_JIN_FULL_THETA_TRANSFER.md#the-small-section-estimate-on-the-fitted-component)

The projective degree satisfies $\delta'_Z\ge(1-\rho)\delta_Z$ for a controlled $\rho$. This turns the component comparison into a lower bound for the weighted mean of the $h_Z$, using the degree and rank bounds to pass from the mean of the $s_Z$. The fixed-degree determinant estimate for sections in the original lattice converts that height bound to a lower bound for its normalized Arakelov degree. With the squared-norm convention, changing its sign gives the upper bound needed for covolume. Descent to the prescribed character type and comparison with the retained lattice give, in each linked layer,
$$
 \frac{\operatorname{lcv}(X_{W,i},\Lambda_i)}{D_{\mathrm{norm}}}
        \le M_{p,i}+C E_p .
$$
Here $D_{\mathrm{norm}}$ is the reference rank, $M_{p,i}$ the prescribed principal term and $E_p$ the allowed geometric error. The terminal definite layer uses its own Gram calculation. The bound applies with a common cutoff to eligible linked members, so it can be imposed before the final family is selected. Combined with the signed indices of the two theta images and the pairing, it gives the geometric contribution to the upper bound on the period of each original word. [From the components to the core](notes/periods/PERIOD_VOLUME_BEFORE_SELECTION.md) · [RH Lean Roadmap, B8.34 and its application to the wordwise bound](https://github.com/rh-lean-roadmap/rh-lean-roadmap/blob/6c23d34a14a3ecf19504ed4182596217ca75006b/docs/src/book/main.tex#L21789-L21811)

Here is why a height computed from asymptotic section counts controls the lattice at the single degree $T$ needed in the tower. Intersect the component image with $d$ general hyperplanes. At each of the $\Delta_Z$ intersection points the Taylor monomials of order $a<T-d$ give independent columns, for a total of $B_Z=\binom{T-1}{d}\Delta_Z$. The last hyperplane vanishes at a cut point precisely on the Chow divisor. Filtering the section determinant by the order at these points therefore exhibits a power of the Chow form as a factor. The degree of the remaining factor is known exactly. The spherical polynomial height becomes nonnegative and remains additive after adding a fixed constant times the degree. Applying this to the factorization gives the finite-degree inequality
$$
 d_Z\ge B_Z(T h_Z-5b)
$$
beyond one uniform cutoff, with $d_Z$ the unsquared normalized degree of the original anchored cusp lattice. In particular the error is independent of the component height. Summing before dividing by the total rank and then doubling to the squared-norm convention gives $\mu_Y\ge-(5C_{\rm ht}+10)E_p$ on the cover. The changed character accounts for a small rank deficit. If the discarded proportion is $\theta\le b/K$ and its quotient has slope at least $-2K$, the mean is bounded by $(1-\theta)t-2\theta K$ from below, with $t$ the available slope after mapping. Keeping this signed expression charges the geometric error only once. [Cut determinant and passage to the retained lattice](notes/geometry/CHOW_DETERMINANT_AT_THE_TARGET_DEGREE.md) · [Jin's construction of the determinant](https://github.com/yuiyuiui/Natural-Language-Proof-Generalized-Riemann-Hypothesis/blob/405237610e58ab9d4a9d5d54d9a0548a0c44227c/sections/j-arithmetic-covolume.tex#L1835-L1895)

## The absolute height of every word on this family

Let $RR$ be the common integral row lattice, $N'_u$ the divided lattice at word $u$, and $B_u$ its rational period map into the dual row. Write $h_u$ for its squared-norm height allowance and $F_{\mathrm{ar}}$ for the signed arithmetic base contribution from all layers. Let $T_u$ be the level prime of the word, $TT$ the set of top positions, $a_t$ their jet orders and $\Omega$ the period normalization. The geometric estimate bounds the normalized logarithmic covolume from above at each stage. The finite estimate bounds the signed indices of the two conjugate theta images and their Hermitian pairing in the very same lattice. In the squared-norm convention their base term is $2F_*$. Sending each served place and each layer back to its arithmetic index gives $2F_*=F_{\mathrm{ar}}$. This equality fixes the coefficient that will be subtracted when the prime gains are counted. [Reference divisor](notes/periods/PERIOD_REFERENCE_WORD_COVOLUME.md) · [Signs and norm convention](notes/periods/PERIOD_FINITE_ERRORS_ON_THE_DESIGN.md)

At the two character levels the row spaces are projected subspaces of one finite-group representation. If the cut lattice has a denominator dividing the group order, its contribution to a logarithmic height is at most the logarithm of that order times its rank. The representations retained by the two projections have nearly proportional multiplicities. The small relative error times the size bound on the row is at most one on the host window. Together these give the comparison of the dual mean slopes before and after changing the level. The archimedean height of a theta lift contains a factorial contribution from its differential orders and a hook-length denominator from its highest weight. Interlacing determines which differential orders survive this comparison.

### The hook rows absorb all but the first large derivative order

Fix one word, one layer and one embedding position. Let $y_0,\ldots,y_{k-1}$ be the first $k$ differential orders and let $r_0,\ldots,r_{k-2}$ be the first $k-1$ row lengths of the corresponding Young diagram. All are nonnegative integers. After the rank shifts are removed, the weight formulas take the form
$$
 y_i=W+c_i,\qquad r_i=W+d_i+h,\qquad c_i\ge d_i\ge c_{i+1},
$$
with $W,h\ge0$. In particular $r_i\ge y_{i+1}$. Let $H$ be the hook product of the entire diagram. The hook of a box contains that box and every box to its right, so row $i$ contributes at least $r_i!$. All remaining hook lengths are at least one. This gives the single product inequality
$$
 H\ \ge\ \prod_{i=0}^{k-2}r_i!\ \ge\ \prod_{i=1}^{k-1}y_i!.
$$
It holds also for a zero row, with $0!=1$. Put $\varphi(z)=z\log z-z$ for $z>0$ and $\varphi(0)=0$. The exponential series gives $\varphi(v)\le\log(v!)$ for every nonnegative integer $v$. Thus every head term except $\varphi(y_0)$ is paid for by the hook product. The source interlacing and the identification of these as the actual rows are essential here. [Weight coordinates and hook identity, B5.08c](https://github.com/rh-lean-roadmap/rh-lean-roadmap/blob/c7755c1086f05d0918ee8496d95912e4f35e22f9/docs/src/book/main.tex#L32853-L32876)

For clarity, let $B_{\rm tail}$ bound the sum of the remaining differential orders and let $A_*>1$ be the upper bound on all orders, with $L_a=\log A_*$. The remaining orders cost at most $B_{\rm tail}L_a$. At an unmarked position $c_0\le S_w$, so the total excess of $\sum_i\varphi(\nu_i)$ over $\log H$ is at most $(W+S_w+B_{\rm tail})L_a$. At a mark of order $a_t$, the first degree is $W+a_t$. Integrating $\log z$ from $a_t$ to $a_t+W$ gives $\varphi(a_t+W)\le\varphi(a_t)+WL_a$, including $a_t=0$ by continuity. The excess there is at most $\varphi(a_t)+(W+B_{\rm tail})L_a$. Pairing each row with the following order gives these bounds directly and removes the accumulated row-shift allowance in the factorial estimate. [Endpoint orders and tail bounds](https://github.com/rh-lean-roadmap/rh-lean-roadmap/blob/c7755c1086f05d0918ee8496d95912e4f35e22f9/docs/src/book/main.tex#L32876-L32912)

The period normalization $\Omega$ requires a second calculation because $\log\Omega$ can have either sign. Let $I$ equal one at a mark and zero elsewhere, take $a_t=0$ off the marks, and put $\Delta=\sum_i\nu_i-Ia_t-kw$, where $w$ is the extension weight at this position. The term from the reference divisor is $\beta_j w\log\Omega$, with $\beta_j$ the reference coefficient of layer $j$. Subtracting $\sum_i\nu_i\log\Omega$ leaves
$$
 -Ia_t\log\Omega+\bigl((\beta_j-k)w-\Delta\bigr)\log\Omega .
$$
The degree-discrepancy estimate bounds the last term in absolute value after the subtraction. A marked position occurs in every layer, so its $\varphi(a_t)-a_t\log\Omega$ occurs $m$ times. The level factor occurs once, at the terminal evaluation. Summing the remaining bounds gives the wordwise inequality [B5.08, summation over positions](https://github.com/rh-lean-roadmap/rh-lean-roadmap/blob/c7755c1086f05d0918ee8496d95912e4f35e22f9/docs/src/book/main.tex#L32915-L32931)
$$
 \begin{aligned}
 \mu(RR^\vee)+h_u-F_{\mathrm{ar}}
 &\le m\sum_{t\in TT}\bigl(\varphi(a_t)-a_t\log\Omega\bigr)
       -\sum_{t\in TT}a_t\log T_u\\
 &\quad+C\bigl(n_TaL_a+m(B_0+N_c)x^{2\varepsilon}\bigr).
 \end{aligned}
$$
Here $n_T=\#TT$, $a=xb$, $L_a=\log(a\,\mathrm{rd}(E))$, $L=x^\varepsilon$, $B_0=fmbL$, and $N_c$ is the allowance for the thick set of labels. In particular the coefficient of $\log T_u$ is negative. The local base sum, the period normalization and this word-dependent term have prescribed partners in the finite division calculation. Bounding their absolute values separately would destroy that comparison. The original wordwise height bound, covariance of the periods, integral inclusion $B_u(N'_u)\subset RR^\vee$, control of the maximal slope, and uniformity in the selected words now hold on the same range. [Full height inequality and uniformity](notes/geometry/COMMON_FAMILY_AND_PERIOD_HEIGHT.md#the-absolute-height-on-this-class) · [Character-level comparison](notes/periods/PERIOD_CHARACTER_SLOPES.md) · [Identification of the rational and complex periods](notes/periods/PERIOD_ARITHMETIC_ROWS_IN_THE_SEESAW.md)

The spectral estimate supplies the other half of the comparison. For two different words of dimensions $d_u,d_v$ in a common space of reference dimension $D^\star$, the squared Hilbert–Schmidt norm of their mixed Gram operator is at most $(1+b^{-6})d_ud_v/D^\star$. On a single word the squared deviation of its Gram operator from the identity is at most $d_u(2e^{-kf\log k}+6/\Gamma)$, where $\Gamma$ is fixed by the family. These estimates hold simultaneously on the full columns. They follow by unfolding the period into orbital sums, estimating the nondegenerate terms and the contributions of smaller rank, and using the signed cancellation in the scalar term. Restriction to a ramified subspace of rank at least $d_u/2$ still gives a positive trace by Cauchy–Schwarz. This supplies a nonzero reference vector on every word for the comparison of the theta and period maps. The count in the corank-one contribution uses the rational block-cell labels of terms with nonzero weight. [Gram theorem and constants](notes/spectral/SPECTRAL_FULL_GRAM_ON_MATCHED_FAMILIES.md) · [v40 correction to the count](guides/EXTERNAL_PROOF_COMPARISON.md#roadmap-v40-and-the-two-final-height-comparisons) · [Uniform block bound and cutoff removal](notes/spectral/FLAG_BLOCK_ENERGY_AND_CUTOFF.md)

Apply the filtered dimension comparison to the finite and archimedean estimates together. Locally one has gained multiples of $\log p$ with prescribed Frobenius weights. Globally this gain is constrained by the integral maps and their mean slopes. After summing the stages and subtracting the matching base and archimedean terms, one obtains the upper bound for the translated prime sum. The selected-family theorem supplies it with division exponent two and common-weight loss exponent zero. At each window point one pair of integer weight functions serves every translation. This allows averaging over the translates while keeping the arithmetic error bound fixed. [Connected-family theorem][read-connected] · [One realization per window point][read-chain]

## What the arithmetic estimate must control

Fix a primitive Dirichlet character $\psi$ of order $o$. Take the powers of $\psi$ modulo its original modulus, and replace each by the primitive character inducing it. The resulting set $I_\psi$ has $o$ elements. Indeed, inducing any representative back to the original modulus recovers its power of $\psi$. The set contains the trivial character of conductor one, denoted $1$, and is closed under complex conjugation. Give $1$ weight $a_1=1$ and each other member weight $a_\chi=1/(3o+1)$. These coefficients will stay fixed as the arithmetic data vary. [Roadmap B1.21–22][analytic-level]

Write $\Lambda(p^j)=\log p$ for $j\ge1$ and $\Lambda(n)=0$ otherwise. The smoothed prime sum and its centered forms, for real $x\ge1$, are
$$
\begin{aligned}
 S_\chi(x)&=\sum_{n\le x}\Lambda(n)\chi(n)(x/n-1),\\
 G_\chi(x)&=S_\chi(x)+x(L'/L)(1,\chi) &&(\chi\ne1),\\
 G_1(x)&=S_1(x)-x\log x+(1+\gamma)x,\\
 H_\psi(x)&=\sum_{\chi\in I_\psi}a_\chi\Re G_\chi(x).
\end{aligned}
$$
Here $\gamma$ is Euler's constant. A prime power first enters with weight zero and thereafter contributes a linear function of $x$. This smoothing allows both the arithmetic comparison at nearby scales and the exact transform computed below. The analytic argument below proves the nonvanishing at $1$ needed for these constants.

The arithmetic result needed here is the following pointwise assertion on entire intervals. For each primitive $\psi$ and all sufficiently small $\varepsilon>0$, for every $Y_0$ there is $Y\ge\max(3,Y_0)$ such that
$$
             H_\psi(x)\le x^{1/2+9\varepsilon}
             \qquad(Y\le x\le Y^{3/2}).                 \tag{1}
$$
The constants and the family may depend on $\psi,\varepsilon$. The family has to work for arbitrarily late windows, and the estimate holds at every real point in each such window. The geometric model realizing the estimate may vary with the point. In the Roadmap, B2.61 supplies windows for the cyclic character request, B7.54 gives the division and loss exponents $(2,0)$, and B5.33 produces the chain with common weights for all required translations. B1.18–20 assemble these inputs. [Roadmap B1.17–20][analytic-supply] [Common chain realization B5.33][analytic-chain] [Family selection B7.54][analytic-selection]

### From the divisibility gain to the fixed character sum

Fix one scale $x$ in an arithmetic window. Three groups enter the calculation. The abelian group $A$ has order $n$. Its translation subgroup $A_0$ has index $o$, the order of the target character $\psi$. The host Galois group in the chosen coordinates is $G=(\mathbb Z/2\mathbb Z)^2\times A$. The half $\Phi=\{(0,j,s)\}$ has size $f=2n$. At a prime $p$ the data give an inertia subgroup $I_p$ and a Frobenius class $F_p$ modulo $I_p$. For $\alpha\in\widehat G$, let $\chi_\alpha$ be the primitive character obtained by pulling $\alpha$ back along the surjective Artin map and taking its primitive representative. Then for every $i\ge1$,
$$
 \chi_\alpha(p^i)=\frac1{|I_p|}\sum_{h\in I_p}\alpha(iF_p+h),
 \qquad
 \frac1f\sum_{\alpha\in\widehat G}\overline{\alpha(g)}\chi_\alpha(p^i)
 =\frac{2}{|I_p|}\mathbf1_{g\in iF_p+I_p}.
$$
Indeed the first average vanishes precisely when $\alpha$ is nontrivial on inertia, in which case $p$ divides the primitive conductor. Otherwise the character factors through the prime-to-$p$ part of the host modulus and the average equals its primitive value. The second identity follows by summing a character on $G$, whose order is $2f$. In particular the unramified coefficient is two, while at the auxiliary prime of inertia order two it is one on its coset. [Primitive values on this host][bridge-values] · [Inertia orthogonality][bridge-orth]

For a marked position $t$, an order $a>0$, and positive allowances $w$ on $\Phi$, let $J(a,t,w)$ be the prime-power gain. Truncating at any integer $N\ge\max_{\rho\in\Phi}a/w(\rho)$ includes every nonzero term. Its summand at $p^i$ is $\log p$ times the sum over $g\notin\Phi$ of $(a/p^i-w(r_t(g)))_+$ with the coefficient on the right above. Here $r_t(g)=(1,1,0)+g+(0,0,t)$ pairs the two halves of the host. Put $\ell_\alpha=(L'/L)(1,\chi_\alpha)$ for $\alpha\ne1$ and $\chi_d(i,j,s)=(-1)^i$. Replacing the coefficient by its character expansion gives the exact identity
$$
\begin{aligned}
 J(a,t,w)-M(a,w)
 &=\frac1f\sum_{g\notin\Phi}\sum_\alpha
  \overline{\alpha(g)}\,w(r_t(g))\,
       G_{\chi_\alpha}\!\left(\frac a{w(r_t(g))}\right),\\
 M(a,w)&=a\left(\log a-1-\gamma+\ell_{\chi_d}
             -\frac1f\sum_{\rho\in\Phi}\log w(\rho)\right).
\end{aligned}
$$
Use the same definitions of $G_\chi(y)$ for $0<y<1$, where the prime sum is empty. To check the sign of the linear term, subtracting $a\ell_\alpha$ converts each centered nonprincipal sum back to its prime sum. Its coefficient averaged over $G\setminus\Phi$ vanishes except at $\chi_d$, where it is $-1$. This gives $+a\ell_{\chi_d}$. The principal character gives the logarithms and Euler's constant. [One-layer balance in the formal proof][bridge-balance]

Write $T\subseteq A$ for the set of top positions, $T_2\subseteq A_0$ for the thick positions before translation, and $n_T=|T|$, $d_2=|T_2|/n$. For $u\in A_0$ and layer $j$, the thick positions in $\Phi$ are $(0,1,s+u)$ with $s\in T_2$. Write $\Gamma_u$ for the sum of $J(a_t,t,w_{u,j})-\Re M(a_t,w_{u,j})$ over $t\in T$ and the $m$ layers. The chain bounds $\Gamma_u$ above at every translate. We first replace each thick weight by its reference value $b$ and discard the thin terms. The total error per position $t$ and layer is at most $2b/x$. Here is how the cutoff pays for it. At a thick position, $b\le w\le b+\eta+1$ and $|a_t/b-x|\le1$. On any interval of differentiability the derivative of $vG_{\chi}(a_t/v)$ in $v$ has absolute value at most $3a_t/v$. For a nonprincipal $\chi$ this follows from $\sum_{r\le y}\Lambda(r)\le3y$. For $\chi=1$ the derivative is $a_t/v-\sum_{r\le a_t/v}\Lambda(r)$ and obeys the same bound. The function is continuous at the other points. Thus the thick replacement costs at most $3(x+1)(\eta+1)$ per term. At a thin position the window parameters $b'$, $X'$ satisfy $w\le2b'$, $b'X'\le xb$ and $x\ge3$. Consequently $a_t/w\ge (x-1)b/(2b')\ge X'/3$. In that range the host supplies $|G_{\chi_\alpha}(a_t/w)|\le (a_t/w)\theta_0$. There are $f$ positions and $2f$ characters with normalization $1/f$. The window inequalities $6f(x+1)(\eta+1)\le b/x$ and $2f(x+1)\theta_0\le1/x$ pay for the two errors separately. [Allowance bounds and their proof][bridge-weights]

Now average over $u\in A_0$. At a thick position the Fourier coefficient has become $\alpha(-(1,0,s+u-t))$. Its average vanishes unless $\alpha$ is trivial on $(0,0,A_0)$. For each surviving character it is $\alpha(1,0,t)$, independently of $s$. Write $P$ for these $4o$ characters, $Q=n_Tmb$ and $\bar\Gamma=|A_0|^{-1}\sum_u\Gamma_u$. Since $|T_2|/f=d_2/2$, the resulting inequality is
$$
 \frac{mbd_2}{2}\sum_{t\in T}\Re\sum_{\alpha\in P}
       \alpha(1,0,t)G_{\chi_\alpha}(a_t/b)
 \le\bar\Gamma+\frac{2Q}{x}.
$$
The arguments $a_t/b$ and the top set on the left are common to every translation, although the thick positions move. This is the point at which simultaneous realization of the weights is used. [Subgroup average][bridge-average] · [Common weights on the translated models][bridge-model]

Next average over $t\in T$. Among the $4o$ survivors write $K_\psi$ for those whose primitive character belongs to $I_\psi$. We call these the retained characters. For every retained $\alpha$, $\alpha(1,0,0)=1$. At the cyclic level the only retained character trivial on $A$ is the principal one. Indeed the possible second character is the auxiliary sign at $q$, and the cyclic host excludes it. On $A/A_0$ the prescribed coset shares are $(3+\mathbf1_{h=0})/(3o+1)$, with each actual share within $x^{-1+\varepsilon}$. Every nontrivial quotient character sums to zero on the constant part, so its average over $T$ differs from $1/(3o+1)$ by at most $ox^{-1+\varepsilon}$. For example, a quadratic target has shares $4/7$ and $3/7$. Their difference is $1/7$, the required coefficient of its nonprincipal character. Multiplying the share error in the character average by $|G_{\chi_\alpha}(x)|$ costs $O_{\psi}(x^\varepsilon(1+\log x))$ for a retained character. This uses $|G_\chi(x)|\le x(\log x+C+|\ell_\alpha|)$; the retained primitive characters are fixed. Moving every $a_t/b$ to $x$ costs $O_{\psi,\varepsilon}(1+\log x)$ per character, by the increment bounds and the host bound $|\ell_\alpha|=O_{\psi,\varepsilon}(\log x)$ for the others. For these increment bounds, differentiate the ramp between consecutive integers and use $\sum_{r\le y}\Lambda(r)/r=\log y+O(1)$. The latter follows by summing $\log n=\sum_{r\mid n}\Lambda(r)$ up to $\lfloor y\rfloor$ and bounding the rounding loss by $\sum_{r\le y}\Lambda(r)$. For fixed $o,\varepsilon$ the total error in these operations is at most $4x^{1/2+\varepsilon}$ past one common cutoff. The sum over omitted characters is bounded below by $-\Sigma(x)$, where $\Sigma(x)=\sum_{\alpha\in P,\,\chi_\alpha\notin I_\psi}|G_{\chi_\alpha}(x)|\le4o x^{1/2+\varepsilon}$ by the host window. The cyclic host theorem supplies a lift of every member of $I_\psi$, and surjectivity of the Artin map gives uniqueness. This identifies $K_\psi$ bijectively with $I_\psi$. Consequently
$$
 H_\psi(x)\le \frac{2\bar\Gamma}{Qd_2}
                +(4+4o)x^{1/2+\varepsilon}+\frac4{d_2x}.
$$
The positive coefficient $Qd_2/2$ preserves the direction of the chain bound. [Moving the top points][bridge-move] · [Cyclic-level shares and retained characters][bridge-target]

It remains to estimate the first term. The division exponent two and common-weight loss exponent zero give $\bar\Gamma\le x^{5\varepsilon}B$. With $d_1=n_T/n$, $k$ the starting rank and $a_E$ the top-weight scale, the four terms of the normalized budget are
$$
 \frac BQ=\frac{a_E}{mb}+\frac{a_Em}{bk}
     +\frac{2mx^\varepsilon}{d_1}
     +\frac{d_2 k x^{2\varepsilon}}{d_1 n^2}.
$$
The factor $m$ in $Q$ counts the layers that earn the prime gain. The first cost is paid once and contributes at most $2x/m$. The third cost recurs and contributes $2mx^\varepsilon/d_1$. This makes precise the balance that motivates a chain of length about $\sqrt{x}$, as emphasized in Eto's account for zeta. The coarse host bounds $d_1\ge x^{-\varepsilon/8}/2$, $d_2\ge x^{-\varepsilon}$, $x^{1/2-\varepsilon}\le m\le x^{1/2+\varepsilon/2}$ and $xm\le k\le n^2x^{1/2-\varepsilon}$ already give $B/Q\le10x^{1/2+13\varepsilon/8}$. Inserting the allowance $x^{5\varepsilon}$ and the loss $d_2^{-1}$ proves (1), including the formal exponent nine. The fixed constants can also be absorbed to give the exponent eight of the preceding edition. [Eto, §§6.3–6.4](https://hexagonmath.org/pdf/2611.01087v1#page=19) · [Four-term budget][bridge-budget] · [Formal exponent][bridge-core]

### The cost at the sizes used by the construction

The completed hosts used here have more precise sizes. At the very point where the maps are evaluated, the layer count and starting rank are the host's $m,k$. The map from integer thick labels $s$ to $sa_0$ is injective on the chosen range, so it also preserves their count. Write $o=[A:A_0]$, $n_0=n/o$ and $L_w=10\lceil405\log x\rceil+2\lceil30/\varepsilon\rceil+22$. The thick-set construction and rank constraints give
$$
\begin{gathered}
 d_2^{-1}\le o L_w\exp\!\left(C_{T_2}\sqrt{\log n_0\log L_w}\right),\qquad
 x^{2+8\varepsilon}\le n\le 2x^{2+8\varepsilon},\\
 x^{1/2-\varepsilon/16}\le m\le2x^{1/2-\varepsilon/16},\qquad
 x^{9/2+10\varepsilon}\le k\le2x^{9/2+10\varepsilon}.
\end{gathered}
$$
For fixed $\psi,\varepsilon$ the thickness constant is uniform, so $d_2^{-1}=\exp(O_{\psi,\varepsilon}(\sqrt{\log x\log\log x}))=x^{o(1)}$. Using $a_E\le2xb$ and $d_1\ge x^{-\varepsilon/8}/2$, the four summands of $B/Q$ are bounded, in order, by
$$
 2x^{1/2+\varepsilon/16},\quad
 4x^{-3-(161/16)\varepsilon},\quad
 8x^{1/2+(17/16)\varepsilon},\quad
 4d_2x^{1/2-(31/8)\varepsilon}.
$$
The third term dominates these upper bounds. Thus $2\bar\Gamma/(Qd_2)\le 36d_2^{-1} x^{1/2+(97/16)\varepsilon}$ for $x\ge1$. The remaining terms in the upper bound for $H_\psi(x)$ are smaller. Uniformly at these window points,
$$
 H_\psi(x)\le x^{1/2+(97/16)\varepsilon+o(1)}.
$$
Here $o(1)$ tends to zero at fixed $\psi,\varepsilon$. In particular the exponent $1/2+(49/8)\varepsilon$ holds throughout each sufficiently late window supplied by this construction. This refinement uses the concrete thick set and ranks of the completed hosts. [Rank ranges](https://github.com/rh-lean-roadmap/rh-lean-roadmap/blob/c7755c1086f05d0918ee8496d95912e4f35e22f9/docs/src/book/main.tex#L3144-L3157) · [Thickness and its scale](https://github.com/rh-lean-roadmap/rh-lean-roadmap/blob/c7755c1086f05d0918ee8496d95912e4f35e22f9/docs/src/book/main.tex#L3510-L3523) · [Completed-host constants](https://github.com/rh-lean-roadmap/rh-lean-roadmap/blob/c7755c1086f05d0918ee8496d95912e4f35e22f9/docs/src/book/main.tex#L3636-L3642) · [Ranks at the translated points](https://github.com/rh-lean-roadmap/rh-lean-roadmap/blob/c7755c1086f05d0918ee8496d95912e4f35e22f9/docs/src/book/main.tex#L15998-L16005) · [Cardinality of the common thick set](https://github.com/rh-lean-roadmap/rh-lean-roadmap/blob/c7755c1086f05d0918ee8496d95912e4f35e22f9/docs/src/book/main.tex#L10915-L10925)

For every lower threshold the construction supplies an entire interval beyond that threshold and all the fixed cutoffs. The character weights stay fixed on all these intervals.

[bridge-values]: https://github.com/rh-lean-roadmap/rh-lean-roadmap/blob/6c23d34a14a3ecf19504ed4182596217ca75006b/docs/src/book/main.tex#L26914-L26924
[bridge-orth]: https://github.com/rh-lean-roadmap/rh-lean-roadmap/blob/6c23d34a14a3ecf19504ed4182596217ca75006b/docs/src/book/main.tex#L2020-L2028
[bridge-balance]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AutomorphicArithmetic/DedekindLFunctions/LandauTheorems/ChBalance.lean#L200-L260
[bridge-weights]: https://github.com/rh-lean-roadmap/rh-lean-roadmap/blob/6c23d34a14a3ecf19504ed4182596217ca75006b/docs/src/book/main.tex#L26748-L26819
[bridge-average]: https://github.com/rh-lean-roadmap/rh-lean-roadmap/blob/6c23d34a14a3ecf19504ed4182596217ca75006b/docs/src/book/main.tex#L2080-L2114
[bridge-model]: https://github.com/rh-lean-roadmap/rh-lean-roadmap/blob/6c23d34a14a3ecf19504ed4182596217ca75006b/docs/src/book/main.tex#L10911-L10928
[bridge-move]: https://github.com/rh-lean-roadmap/rh-lean-roadmap/blob/6c23d34a14a3ecf19504ed4182596217ca75006b/docs/src/book/main.tex#L2213-L2264
[bridge-target]: https://github.com/rh-lean-roadmap/rh-lean-roadmap/blob/6c23d34a14a3ecf19504ed4182596217ca75006b/docs/src/book/main.tex#L26926-L26955
[bridge-budget]: https://github.com/bmatschke/grh-alpoge-claude/blob/f6918dbf16a8d5f4f86146fd9fa2c04efff4f8ad/conditional_main_v42/conditional_main.tex#L333-L369
[bridge-core]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AutomorphicArithmetic/PrimitiveCosets/CoreGm.lean#L12-L74

## Why one-sided windows detect a zero

Fix $0<\theta<1$ and $\lambda>1$. Suppose the real function $H_\psi(x)$ satisfies $H_\psi(x)\le x^\theta$ throughout $[Y,Y^\lambda]$ for arbitrarily large $Y$. We will see why a zero of any member of $I_\psi$ with real part greater than $\theta$ contradicts this one-sided estimate. We follow Kaiwen Jin in comparing two derivatives of the same order. [Jin, signed power-window criterion][analytic-jin] · [Formal power-window theorem][analytic-native]

### One product records all the zeros

First justify the constants $(L'/L)(1,\chi)$ used to center the prime sums. Give each power of $\psi$ its original modulus $Q$ for the moment, and set $B(s)=\prod_{j=0}^{o-1}L(s,\psi^j\bmod Q)$. At $p\nmid Q$ let $d$ be the order of $\psi(p)$. Its powers take each $d$th root of unity $o/d$ times. The local factor of $B$ is therefore $(1-p^{-ds})^{-o/d}$. At $p\mid Q$ it is $1$. In the Dirichlet series $B(s)=\sum b_n n^{-s}$ all $b_n$ are nonnegative, and $b_{m^o}\ge1$ if $(m,Q)=1$, since $d\mid o$ at every prime dividing $m$.

Every nonprincipal factor is holomorphic on $\Re s>0$ by summation by parts using bounded character partial sums. The principal factor is $\zeta(s)\prod_{p\mid Q}(1-p^{-s})$ and has a single simple pole there at $1$. A zero at $1$ of any nonprincipal factor would make $B$ holomorphic throughout this half-plane. Its Taylor series about $2$ would then converge at $v=1/o$. Termwise differentiation at $2$ and the nonnegativity of the terms give
$$
 B(v)=\sum_{k\ge0}\sum_{n\ge1} \frac{b_n}{n^2}
           \frac{((2-v)\log n)^k}{k!}
      =\sum_{n\ge1}\frac{b_n}{n^v}
      \ge\sum_{(m,Q)=1}\frac1m=\infty .
$$
This contradiction proves nonvanishing at $1$. The finite Euler factors removed in passing to primitive representatives are also nonzero there. This is the usual proof by positivity of Dirichlet coefficients, applied just to the powers of $\psi$. [Petrow, Theorem 4.13 and Lemma 4.14](https://metaphor.ethz.ch/x/2018/hs/401-3100-68L/IANTnotes2018.pdf#page=37)

Return to the primitive representatives and form
$$
 F_\psi(s)=\zeta(s)^{3o}\prod_{\chi\in I_\psi}L(s,\chi).
$$
The exponent of the zeta factor in the full product is $3o+1$. Thus $(F'_\psi/F_\psi)/(3o+1)=\sum_\chi a_\chi L'_\chi/L_\chi$. Conjugation permutes the characters and preserves their weights. Their weighted sum of centered prime sums is already real on the positive real axis. For example, when $o=2$ the product is $\zeta^7 L(s,\psi)$. The prime-power coefficient of $H_\psi$, before centering and apart from the ramp and $\log p$, is $1+\psi(p)^j/7$ at $p^j$. A split prime has coefficient $8/7$ in every degree. At an inert prime the odd degrees have $6/7$ and the even degrees $8/7$. At a ramified prime the coefficient is $1$. [Weights of the original cyclic level][analytic-level]

Write $D_\chi=L'_\chi/L_\chi$ and $D_1=\zeta'/\zeta$. For $\Re s>1$, the integral of $(x/n-1)x^{-s-1}$ from $n$ to infinity is $n^{-s}/[s(s-1)]$. Absolute convergence permits termwise integration of the smoothed sums. Their centered Mellin transforms are
$$
 P_\chi(s)=-\frac{D_\chi(s)}{s(s-1)}+\frac{D_\chi(1)}{s-1}
       \quad(\chi\ne1),\qquad
 P_1(s)=-\frac{D_1(s)}{s(s-1)}-\frac1{(s-1)^2}
                  +\frac{1+\gamma}{s-1}.
$$
Each is regular at $1$. The first has two canceling residues, and the second uses $D_1(s)=-1/(s-1)+\gamma+O(s-1)$. Set $g(u)=H_\psi(e^u)$. Its Laplace transform $\Phi(s)=\sum_\chi a_\chi P_\chi(s)$ is meromorphic for $\Re s>0$. At every family zero $\rho$ in this half-plane its residue is
$$
 \operatorname{res}_{s=\rho}\Phi(s)
 =\frac{\operatorname{ord}_\rho F_\psi}{(3o+1)\rho(1-\rho)}.       \tag{2}
$$
The numerator is a positive integer even when several family members vanish at $\rho$. The absolutely convergent Euler products exclude zeros for $\Re s>1$. Hence every real pole of $\Phi$ lies in $(0,1)$ and has positive residue. Equation (2) also applies to a hypothetical nonreal zero on $\Re s=1$.

### How the upper bound detects the pole

For $\sigma>2$ set $A_k(z)=(-1)^k\Phi^{(k)}(z)/k!$. The definition of the sums and $\Lambda(n)\le\log n$ give $|g(u)|\ll_\psi e^u(1+u^2)\le M e^{2u}$. Differentiate the Laplace integral. For real $t$, the triangle inequality and the reality of $g$ give
$$
 |A_k(\sigma+it)|+A_k(\sigma)
 \le 2\int_0^\infty \max(g(u),0)e^{-\sigma u}\frac{u^k}{k!}\,du .    \tag{3}
$$
The real derivative has kept its sign. This is where an upper bound on $H_\psi$ alone suffices.

Put $U=\log Y$, $h=(1+\lambda)/2$, $\mu=\sigma-2$, $n=\lfloor h\mu U\rfloor$ and $k=n-1$. On $[U,\lambda U]$ the right side of (3) is at most $2(\sigma-\theta)^{-n}$. Outside this interval it is at most $2M\mu^{-n}$ times the probability that a gamma variable $T$ with density $t^{n-1}e^{-t}/(n-1)!$ lies outside $[\mu U,\mu\lambda U]$. To bound this probability choose $1/h<r_-<1<r_+<\lambda/h$. For large $U$ the two tails lie in $T\le nr_-$ and $T\ge nr_+$ respectively. Applying exponential Markov with $v=1-1/r_\pm$ and $\mathbb E e^{vT}=(1-v)^{-n}$ bounds their sum by $2e^{-cn}$, where $c=\min_\pm(r_\pm-1-\log r_\pm)>0$. Consequently for **every** $\sigma$ large enough that $\log((\sigma-\theta)/(\sigma-2))<c$, there is an unbounded sequence of orders $k$ for which
$$
 |A_k(\sigma+it)|+A_k(\sigma)\le K_\sigma(\sigma-\theta)^{-k}
 \qquad(t\in\mathbb R).                                      \tag{4}
$$
The same orders work at every height $t$ for each such $\sigma$. [Jin’s gamma-kernel estimate and pole argument](https://github.com/yuiyuiui/Natural-Language-Proof-Generalized-Riemann-Hypothesis/blob/405237610e58ab9d4a9d5d54d9a0548a0c44227c/sections/signed-criterion.tex#L82-L99)

Suppose $\rho_0$ is a pole with $\Re\rho_0>\theta$. Choose $\sigma$ large enough for (4) and for
$$
 2\sigma(\Re\rho_0-\theta)>|\rho_0|^2-\theta^2 .
$$
The second inequality puts $\rho_0$ strictly inside the disk with center $\sigma$ and radius $a=\sigma-\theta$. This disk lies in the meromorphic half-plane. Let $d_0<a$ be the distance to the nearest pole. There are finitely many nearest poles, and conjugation preserves them. If they are all real, there is just one, $\beta=\sigma-d_0$, with residue $b>0$. Choose $d_0<r<a$ small enough that the disk of radius $r$ contains no other pole. Subtracting $b/(s-\beta)$ and applying Cauchy’s estimate gives $A_k(\sigma)=b d_0^{-k-1}+O(r^{-k})$. Inequality (4) at $t=0$ is impossible for arbitrarily large $k$.

Otherwise take a nearest pole $\rho_*$ with largest imaginary part. Its height is positive. Among the nearest poles this maximizer is unique, since two points of the same height and distance to $\sigma$, both to the left of $\sigma$, coincide. Moving the center to $\sigma+it$ changes the squared distance to a pole $\rho$ by $t^2-2t\Im\rho$. For all sufficiently small $t>0$ this makes $\rho_*$ the unique closest pole, at distance $d<d_0$. Indeed the original nearest poles are isolated from all others by a positive distance gap, and moving the center by $t$ changes every distance by at most $t$. Choose $d<r<d_0$ with just $\rho_*$ in the shifted closed disk. Subtract its simple principal part there. Cauchy’s estimate at the two centers gives $|A_k(\sigma+it)|\ge |\operatorname{res}_{\rho_*}\Phi| d^{-k-1}-O(r^{-k})$ and $|A_k(\sigma)|=O(r^{-k})$. Since $d<r<a$, their signed sum contradicts (4) along the same orders. Thus there is no pole with real part greater than $\theta$, and (2) excludes every family zero there.

## The five conclusions

For $\Re s>1/2$ choose $1/2<\theta<\min(\Re s,1)$, then choose $\varepsilon>0$ within the arithmetic range with $9\varepsilon<\theta-1/2$. Inequality (1) supplies the required windows with $\lambda=3/2$. Since $\psi\in I_\psi$, the criterion excludes a zero of $L(s,\psi)$. This works separately for every primitive character, including conductor one. At the classical pole $s=1$, all principal-character assertions below use their stated exception. The archive assigns a finite value $(\gamma-\log(4\pi))/2<0$ to its level-one function at $1$. [Roadmap, conventions and statements][analytic-five]

For an arbitrary character $\chi$ modulo $N\ge1$, let $\chi^*$ be its primitive representative of conductor $f$. Comparison of Euler products followed by meromorphic continuation gives
$$
  L(s,\chi)=L(s,\chi^*)\prod_{\substack{p\mid N\\p\nmid f}}
                         (1-\chi^*(p)p^{-s}).
$$
Each finite factor is nonzero when $\Re s>0$, since its subtracted term has modulus at most $p^{-\Re s}<1$. This proves **nonvanishing for every character in $\Re s>1/2$** whenever $\chi$ is nonprincipal or $s\ne1$. In the open strip $0<\Re s<1$, a primitive zero at $s$ reflects to a zero of the inverse character at $1-s$ by the primitive functional equation. Its gamma factors are finite and nonzero at both arguments. A zero with $\Re s<1/2$ would therefore contradict the nonvanishing just obtained. This proves **the critical-line assertion for primitive strip zeros** and, by the finite product, **the critical-line assertion for all character strip zeros**. [Roadmap B1.07–13][analytic-reflection]

Finally $L(s,1)=\zeta(s)$. If $\Re s<1/2$ and $\zeta(s)=0$, then $s\ne0$ since $\zeta(0)=-1/2$. Put $t=1-s$. The reflection identity
$$
  \zeta(1-t)=2(2\pi)^{-t}\Gamma(t)\cos(\pi t/2)\zeta(t)
$$
has $\Re t>1/2$ and $t\ne1$. All factors except the cosine are nonzero. Hence $t$ is an odd integer greater than 1, and $s$ is a negative even integer. Together with right-hand nonvanishing this gives **RH for all nontrivial zeta zeros**. Writing the excluded integers explicitly as $-2(n+1)$ for $n\ge0$ gives the archive's **explicit zeta implication**, its fifth formulation counted together with the preceding four. [Roadmap B1.01–05 and B1.11][analytic-five] [Zeta reflection][analytic-reflection]

[analytic-level]: https://github.com/rh-lean-roadmap/rh-lean-roadmap/blob/6c23d34a14a3ecf19504ed4182596217ca75006b/docs/src/book/main.tex#L972-L1015
[analytic-supply]: https://github.com/rh-lean-roadmap/rh-lean-roadmap/blob/6c23d34a14a3ecf19504ed4182596217ca75006b/docs/src/book/main.tex#L854-L968
[analytic-chain]: https://github.com/rh-lean-roadmap/rh-lean-roadmap/blob/6c23d34a14a3ecf19504ed4182596217ca75006b/docs/src/book/main.tex#L10888-L10930
[analytic-selection]: https://github.com/rh-lean-roadmap/rh-lean-roadmap/blob/6c23d34a14a3ecf19504ed4182596217ca75006b/docs/src/book/main.tex#L15234-L15238
[analytic-jin]: https://github.com/yuiyuiui/Natural-Language-Proof-Generalized-Riemann-Hypothesis/blob/405237610e58ab9d4a9d5d54d9a0548a0c44227c/sections/signed-criterion.tex#L54-L99
[analytic-five]: https://github.com/rh-lean-roadmap/rh-lean-roadmap/blob/6c23d34a14a3ecf19504ed4182596217ca75006b/docs/src/book/main.tex#L17-L80
[analytic-reflection]: https://github.com/rh-lean-roadmap/rh-lean-roadmap/blob/6c23d34a14a3ecf19504ed4182596217ca75006b/docs/src/book/main.tex#L89-L180
[analytic-native]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AutomorphicArithmetic/DedekindLFunctions/LandauTheorems/ZeroFreeOfRpowWindow.lean#L11-L14

## Sources and scope of the reconstruction

The [original Lean declarations](https://github.com/CocoSgt/riemann-hypothesis-lean/tree/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4) specify the mathematical statements and the common choices. [Alpöge's announcement](https://alpo.ge/remark.pdf) describes their motivation. The [RH Lean Roadmap, v41](https://github.com/rh-lean-roadmap/rh-lean-roadmap/tree/c7755c1086f05d0918ee8496d95912e4f35e22f9) gives a book-length account of the spectral, Galois and geometric inputs, with references back to the archive. [Kaiwen Jin's translation](https://github.com/yuiyuiui/Natural-Language-Proof-Generalized-Riemann-Hypothesis/tree/405237610e58ab9d4a9d5d54d9a0548a0c44227c) supplies the signed analytic criterion, arithmetic-volume comparison and paired finite estimates used here. [Chen's reconstruction](https://github.com/yyyyychen/RH-Natural-Language-Proof/tree/d4dfb1a282dbf857288e73eb1f546dbfcc5899b8) contributes the arithmetic seesaw and word-prime comparisons. [Nelson's workbook](https://github.com/ultronozm/grh-workbook/tree/954f94f32f6a3f7ce2d21c24598d8b9251e41729) gives complementary readings of the seesaw. Particular further contributions, including Huang's formal-group interpretation, are credited in the relevant chapters.

At each interior layer of an admissible marked member the rank inequalities give the required negative signature, and the chosen cover gives its level. The resolved Hodge flag supplies the smooth metrics, a section vanishing along the boundary and the degree-one reference for all its finite-prime covers. Both selected period operators map to the same measured automorphic space. A single isometry intertwines them on every word, so their Gram blocks have exactly the norms computed in that model. The rank and critical-level estimates give the word-frame inequality at one guarded family threshold. Applying the endpoint bounds uses the linked bundles on the required windows, the arithmetic volume and density formulas in their native measures, and the estimates for the other Gram strata. [All interior layers](../manuscript/notes/periods/GOOD_ROOT_TOWER_COMPARISONS.md#claim:GRT103) · [Reference and cutoff covers](../manuscript/notes/periods/GOOD_ROOT_TOWER_COMPARISONS.md#claim:GRT107) · [Full Gram transport](../manuscript/notes/spectral/FLAG_BLOCK_ENERGY_AND_CUTOFF.md#claim:FBE43) · [Word-frame threshold](../manuscript/notes/spectral/FLAG_BLOCK_ENERGY_AND_CUTOFF.md#claim:FBE44)

For review, the highest-dependency passage is the [assembly of the common family and the nine period-height clauses](notes/geometry/COMMON_FAMILY_AND_PERIOD_HEIGHT.md). It identifies the exact lemmas used, the actual objects on which they act and the cutoffs uniform in those objects. The [dependency register](../research/register/SELECTED_FAMILY_CHECKPOINT.json) records the endpoint uses and the [broader-work list](../research/register/NEXT_STEPS.md) records stronger questions inherited from earlier editions. This manuscript is a synthesis for mathematical review. The accompanying chapters and source references identify the premises of the deeper geometric and automorphic theorems. For each of the 63 Part VIII arguments that the Roadmap labels an outline, its book has a later proof subsection with links to the formal declarations. The [guide to all 63 longer passages](guides/ROADMAP_OUTLINE_CROSS_REFERENCES.md) groups them by their role in the proof.

[read-host]: https://github.com/rh-lean-roadmap/rh-lean-roadmap/blob/6c23d34a14a3ecf19504ed4182596217ca75006b/docs/src/book/main.tex#L11774-L11808
[read-supply]: https://github.com/rh-lean-roadmap/rh-lean-roadmap/blob/6c23d34a14a3ecf19504ed4182596217ca75006b/docs/src/book/main.tex#L3752-L3766
[read-galois]: https://github.com/rh-lean-roadmap/rh-lean-roadmap/blob/6c23d34a14a3ecf19504ed4182596217ca75006b/docs/src/book/main.tex#L24584-L24600
[read-count]: https://github.com/rh-lean-roadmap/rh-lean-roadmap/blob/6c23d34a14a3ecf19504ed4182596217ca75006b/docs/src/book/main.tex#L12429-L12442
[read-window]: https://github.com/rh-lean-roadmap/rh-lean-roadmap/blob/6c23d34a14a3ecf19504ed4182596217ca75006b/docs/src/book/main.tex#L11810-L11816
[read-connected]: https://github.com/rh-lean-roadmap/rh-lean-roadmap/blob/6c23d34a14a3ecf19504ed4182596217ca75006b/docs/src/book/main.tex#L15234-L15238
[read-chain]: https://github.com/rh-lean-roadmap/rh-lean-roadmap/blob/6c23d34a14a3ecf19504ed4182596217ca75006b/docs/src/book/main.tex#L10888-L10930
