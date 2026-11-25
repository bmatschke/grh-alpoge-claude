# How many arithmetic row directions do the periods detect?

The slope comparison asks how much of the common row space the arithmetic period maps can reach after some of their source directions are discarded. This question has an answer in terms of subspaces alone. The answer gives a weaker sufficient target for this part of the proof. Establishing the required inequality on the actual family remains open. [Gram-to-slope argument](gram_frame/gram_frame_section.tex#L44-L111) · [The stronger Bessel identity](continuation_v90/intertwiners.tex#L74-L95)

## What survives a change of coordinates

Fix the complex embedding used in the comparison. Write $b_i:V_i\to C$ for the complexifications of the actual rational period maps into the common dual row space. On the automorphic side write $g_i=P_0A_iJ_i:W_i\to H_0$. Here $A_i$ is the normalized full period operator, $J_i$ includes the retained source isometrically, and $P_0$ is the orthogonal projection onto the retained target. The corresponding source dimensions are equal.

Suppose a single linear isomorphism $Y:C\to H_0$ sends $\operatorname{im} b_i$ onto $\operatorname{im} g_i$ for every label. Then there are linear isomorphisms $X_i:V_i\to W_i$ such that $Yb_i=g_iX_i$. Indeed the two kernels have equal dimensions. Choose an isomorphism between them, and choose complements to the kernels. On the complements, both maps identify their source with the same image, which determines the other part of $X_i$. Conversely, taking images of the displayed equality gives the common image identification. This proof includes zero maps. No norm estimate on $X_i$ or $Y$ is used. The height bounds on the arithmetic $b_i$, the metric restrictions $J_i,P_0$ on the analytic side, and the spectral estimates still have their original meanings. [Coordinate comparison in the pinned source](https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Formalism/SharpRestriction/GlobalSchurBounds/TopDensityNGeSixteen.lean#L1087-L1105)

## An inequality for the arithmetic maps themselves

Let $D$ be the full analytic target dimension and $M$ the sum of the full analytic source dimensions. Put $R=\sum_i\dim V_i$, with $M-R\le dM$. In the notation of the direct Gram-to-slope argument, the full frame error is $5\tau+4\sqrt{e_0}$. Under its spectral hypotheses the following bound transfers to the arithmetic maps whenever the image comparison above holds. For **every** choice of complex subspaces $E_i\subseteq V_i$,

$$
\operatorname{codim}_C\sum_i b_i(E_i)
 \le a+b\sum_i\operatorname{codim}_{V_i} E_i,
\qquad a=D(5\tau+4d+4\sqrt{e_0}),\quad b=4D/M.
$$

Indeed the corresponding subspaces of the full analytic sources have total codimension $M-R+\sum_i\operatorname{codim} E_i$. The full frame bound adds four times this fraction of $M$ to its error, and multiplies by $D$. Projection to $H_0$ can only decrease the absolute codimension. The factor $1/(1-\delta)$ enters when dividing by the retained target dimension $\dim C\ge(1-\delta)D$. [Derivation and constants](gram_frame/gram_frame_section.tex#L44-L111) · [Zhang, Lemma 4.2 and Proposition 4.3](https://hexagonmath.org/pdf/2611.00809v1#page=38)

A direct proof of this inequality for the arithmetic maps would suffice. It is equivalent to requiring, for every $W\subseteq C$,

$$
\operatorname{codim}_C W\le a+b\sum_i
  \left(\dim\operatorname{im} b_i-\dim(\operatorname{im} b_i\cap W)\right).
$$

For necessity, choose $E_i=b_i^{-1}(W)$, whose image sum lies in $W$. For sufficiency, take $W=\sum_i b_i(E_i)$ and use $E_i\subseteq b_i^{-1}(W)$. Taking annihilators gives an equivalent dual statement. For every $L\subseteq C^\vee$,

$$
\dim L\le a+b\sum_i\dim b_i^\vee(L).
$$

Each term on the right counts the independent functionals in $L$ seen by one label. A subspace of dimension greater than the allowed error must be detected in aggregate. In the slope proof the $E_i$ are specifically the Harder–Narasimhan subspaces above a height-adjusted threshold. The arithmetic height bound puts their images above the corresponding target threshold. The inequality bounds the proportion of slopes below it. Integrating in the threshold gives the mean-slope bound. The estimates for those particular subspaces already suffice. [Integration of the slope tails](gram_frame/gram_frame_section.tex#L84-L113)

For a two-dimensional example take two maps from lines to a plane and test the dual inequality with $a=0$, $b=1$. If the images are the two coordinate axes, every nonzero functional is detected by at least one map, and the entire dual plane contributes one dimension at each label. The inequality holds for all subspaces. If both lines map onto the first axis, the functional extracting the second coordinate vanishes on both, and its span violates the inequality. Every individual map has the same rank in both examples. The relative positions of their images determine the outcome.

There is a classical counterpart to the dual test. In the finiteness theorem for Brascamp–Lieb inequalities, one asks about linear maps $B_i$ from one real vector space and weights $p_i$. Finiteness is equivalent to a total-dimension scaling identity together with $\dim L\le\sum_i p_i\dim B_i(L)$ on every subspace. The proposed arithmetic test has this subspace form with an additive allowance $a$, complex subspaces and weights prescribed by the slope calculation. The classical theorem explains why this is a familiar geometric question. Verifying the dimension estimate for these particular periods is the arithmetic work. [Bennett–Carbery–Christ–Tao, conditions (7)–(8) and Theorem 1.15](https://webhomes.maths.ed.ac.uk/~carbery/analysis/papers/Carbery/bcctfinal.pdf#page=6)

## An exact certificate from noncommutative rank

The dimension test ranges over infinitely many subspaces of one finite-dimensional space. An existing theorem converts it to the rank of one matrix, provided one allows several copies of each space. The number of copies can depend on the datum. This identifies the precise finite problem for which a literature theorem is available.

Write $b=s/t$ with positive integers $s,t$, put $U=C^\vee$, and write $f_i=b_i^\vee:U\to V_i^\vee$. The largest possible deficit after clearing denominators is the integer

$$
h=\max_{L\subseteq U}\left(t\dim L-s\sum_i\dim f_i(L)\right).
$$

This quantity already has a name. View the maps $f_i$ as the arrows of a star-shaped quiver, all pointing from the central space $U$ to the various $V_i^\vee$. Give the center weight $t$ and every leaf weight $-s$. A subrepresentation consists of a subspace $L$ at the center and a subspace containing $f_i(L)$ at each leaf. For fixed $L$ its weight is largest when the leaf subspaces equal $f_i(L)$. Thus $h$ is exactly the **discrepancy of the quiver representation** in Cheng’s Definition 2.6, which allows arbitrary total weight. [Cheng, Definition 2.6](https://arxiv.org/pdf/2111.06428#page=7)

The desired inequality says $h\le\lfloor ta\rfloor$. **Equivalently**, for some positive integer $k$ there exist matrices $T_i:\mathbb C^{kt}\to\mathbb C^{ks}$ such that the block map

$$
\Phi_k=(f_i\otimes T_i)_i:
 U\otimes\mathbb C^{kt}\longrightarrow\bigoplus_i V_i^\vee\otimes\mathbb C^{ks}
$$

has nullity at most $k\lfloor ta\rfloor$. One direction is elementary. On $L\otimes\mathbb C^{kt}$ the domain has dimension $kt\dim L$ and the image has dimension at most $ks\sum_i\dim f_i(L)$. Thus every choice has nullity at least $kh$.

For the converse, let $\mathcal B$ be the matrix space consisting of all the maps $\Phi_1$ as the $T_i$ vary independently. For $X\subseteq U\otimes\mathbb C^t$, let $L\subseteq U$ be the span of its components in any basis of $\mathbb C^t$. Then $X\subseteq L\otimes\mathbb C^t$. The span $\mathcal B(X)$ of all images of $X$ is exactly $\bigoplus_i f_i(L)\otimes\mathbb C^s$. Indeed one can use a single matrix unit at a single label to extract any one component and place its image in any output coordinate. It follows that $\dim X-\dim\mathcal B(X)\le h$, with equality for $X=L\otimes\mathbb C^t$ when $L$ maximizes the deficit.

By the Fortin–Reutenauer characterization, the noncommutative rank of this rectangular matrix space is $r=t\dim U-h$. Ivanyos–Qiao–Subrahmanyam’s Theorem 7 gives a matrix of rank $kr$ after replacing its scalar coefficients by $k\times k$ matrices, for some $1\le k\le r+1$. One can apply their square-matrix statement by padding with zero rows or columns. Padding preserves rank before and after this replacement. Removing the padding and grouping the blocks gives precisely a map $\Phi_k$ with nullity $kh$. This proves the converse. [Fortin–Reutenauer, §2, Theorem 1](https://www.mat.univie.ac.at/~slc/wpapers/s52reut.pdf#page=4) · [Ivanyos–Qiao–Subrahmanyam, Theorem 7](https://drops.dagstuhl.de/storage/00lipics/lipics-vol067-itcs2017/LIPIcs.ITCS.2017.55/LIPIcs.ITCS.2017.55.pdf#page=7)

In arithmetic bases, a nonzero minor of the required size can be witnessed by rational choices of the auxiliary matrices. Its determinant is a nonzero polynomial in their entries, and rational points are Zariski dense. Thus a single explicit datum admits an exact check. The arithmetic question is to prove the prescribed rank bound throughout the selected family as the parameters grow. The three-rank criterion of edition 0.90 addresses the stronger question of simultaneous unitary equivalence. [The arithmetic periods in chosen bases](continuation_v90/base.tex#L4-L45)
