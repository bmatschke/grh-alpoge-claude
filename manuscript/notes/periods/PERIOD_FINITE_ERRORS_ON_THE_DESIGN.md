# The finite part of the seventh height estimate

The period implication and the final application use the local denominator estimate at different stages. In the original implication, the family already satisfies the division bound. In the application to zeros, the host request and the previously proved denominator theorem give that bound on the chosen family. Neither argument requires a division bound on every preliminary host. The signed theta-index estimate, in contrast, must be available as an implication for *every eligible choice* before choosing the family. We check the order of these assertions and the size of the finite error. The index estimates themselves are due to the Alpöge–Claude construction. We use the RH Lean Roadmap's proof of B8.38b and Kaiwen Jin's integral division argument. [Original period and division conditions][native] · [Two-run proof][runs] · [Jin's signed lattice conventions](PERIOD_JIN_PAIRED_REFERENCE.md)

## The division bound on the family used for zeros

For each primitive character (including the character of conductor one), the actual host request includes the bound on the indicated Tate–Shafarevich lengths up to the host rank, with budget $\sqrt b$. The host-supply theorem B2.61 applies at window ratio $3/2$ on the window theorem B6.04. Each translated point uses the very same host field and host rank as the test of the request. Thus, for every indexed point above the initial cutoff of a family in this target class, every finite set of primes satisfies
$$
 \sum_{p\in S}\log p\sum_{1\le k<t}\operatorname{length}_{\mathbb Z_p}
              \Sha_{p,k}(E)\le\sqrt b.
$$
Take the local data of the point itself, which are covered by the universal host requirement. The lengths are finite also at $2$. Nonnegativity makes the supremum of the finite sums the full sum. This yields the exact finiteness and summability guards in the denominator theorem. For an arbitrary request in the abstract connection theorem the corresponding host bound is an explicit premise. [Host condition and local data][host] · [Supply for primitive characters][supply] · [Native projection on the target family][window] · [One host across translates](../arithmetic/COMMON_DESIGN_WINDOW_TRANSFER.md)

The denominator theorem G87D2 establishes the row for any compatible selector at the required level, using its eighteen member inputs and four ties. X87S4 inserts its member condition in the conjunction *before* class selection. Restricting to the host-request subclass only projects the family membership and retains the same selected points and their norm data. On the selected family the base-level rank theorem identifies the dimension $d_{j,0}$ in this row with the actual reference dimension $D_0$ in every layer. This follows by taking the image of the surjective base projection with the selected primitive and division rows, at the maximum of their cutoffs. [Denominator and its guards](../../../archive/rounds/v87/continuation_v87/denominator.tex#L36-L84) · [Insertion in the joint selection](../../../archive/rounds/v87/continuation_v87/selection.tex#L133-L205) · [Selected base-rank theorem](../construction/SELECTED_BASE_ROWS.md#the-square-used-by-both-endpoints) · [Original rank comparison][rank]

Put $L=x^\varepsilon$, $b=e^L$, $B_0=fmbL$ and let $N_c\ge0$ be the thick-set budget. Let $C_N$ be the family denominator constant. Take the maximum of the window, denominator and rank cutoffs, the family's initial cutoff plus one, and the cutoff for $(\log x)^2\le L$. For every later index the denominator inequality gives, in every permitted layer,
$$
 \eta_j\le D_0\{C_N(fmbL^2+(\log x)^2 N_c)+\sqrt b\}
       \le D_0 (|C_N|+1)L(B_0+N_c).
$$
Indeed $f,m,L\ge1$ and $\sqrt b\le b\le B_0$. The constant is chosen once for the family before any layer. Under the place and type identifications, each twisted place is supported and has nonreference type. If $a_{jv}$ is the length of the lift modulo its cut, the ordinary length at the matching place is its normalized length times $e_v$. After reindexing the nonnegative sum, $\sum_{v\in\mathrm{Tw}}\ell_v a_{jv}\le\eta_{a(j)}$, where $a(j)$ numbers the same layer on the arithmetic side. This last implication uses only the given division bound, and therefore works also in the period theorem on the full design class. [Native derivation of the common cutoff][div] · [Identification of the cut lengths][sum]

## One signed estimate for every eligible reference point

Fix an eligible family in the covolume class and a height parameter satisfying its ordered thresholds. The arithmetic producer first proves a closed implication with the family division bound as antecedent. Its conclusion has the following order: a constant $C_0\ge0$, a cutoff $x_0$, all $x>x_1$ with $x\ge x_0$, all indices, all eligible points with the extra reference ties, and all $C\ge C_0$. The reference relation fixes the two recursion primes, the marked tuple, the two determinant characters and both coefficient readings. The producer uses the original representations, Galois, crystalline and local Langlands inputs. Its proof obtains the actual two runs, rationality, geometric and rank estimates and the size conditions together with the separate twist, share, exceptional-place and exponent estimates. The latter exponent estimate is where definite base change and the crystalline lattice theorem enter. The point predicate and the auxiliary ties in B8.38 are supplied by the linked primitive, divisor, goodness, geometric and reference rows. This gives the arithmetic inequality on the point chosen by the common selector. [Native domain of the two runs][domain] · [Construction of the arithmetic inputs][producer] · [Two-run and rank installation][install] · [Transport on the given points][transport]

Here is the normalization of its estimated terms. Write $D>0$ for the common reference rank, $M_j$ for its integral lattice, $T_{j,t}$ for the upper lattice of type $t$ and $A_{j,t}=\theta_{j,t}T_{j,t}$. Let $i_{jw}$ be the sum of the signed indices of $A_{j,t(w)}$ in $M_j$ at $w,\bar w$, and let $q_{jw}$ be the index of the Hermitian dual in $T_{j,t(w)}$ at $w$. The type at $\bar w$ is the same as at $w$. For each run in layer $j$ the nonnegative subspace remainder has weighted sum at most $n_j fmb$, where $n_j$ is the full dimension. Using one run at its distinguished residue characteristic and the other elsewhere costs at most $2 n_j fmb$. Counting both places costs at most $4 n_j fmb$, even for a conjugation-stable place, since the formula for $i_{jw}$ counts both readings there. The mirabolic index $s_j$ is the divisor in the projection estimate. With $y=1/(4(fk)^3)\le1/4$ and $\delta_j\le1/4$, the rank and group inequalities give
$$
 \frac{n_j}{s_jD}\le\frac{1}{(1-y)^2(1-\delta_j)}
                      \le\frac{64}{27}<3 .
$$
Thus the normalized two-run remainder is at most $12 fmb$ per layer. At a type prime the depth contains the negative order of the level-normalizing factor. Its orders at $w,\bar w$, in units of $e_w$, add to $-2F_{0,j,w}$. Subtracting them gives **$+2F_{0,j,w}$** in the upper bound. Replacing this signed contribution by its absolute value would lose the later cancellation with the archimedean term. The remaining twist errors contribute at most $2e_w/p_w^2$ after the sum over layers. [Mirabolic projection and rank][runs] · [Exceptional prime depths and their signs][depths] · [Summation over the ordinary primes][excess]

For clarity, put $\ell_w=\log Nw/[K:\mathbb Q]$ and $F_*=\sum_{j,w\in\mathrm{Tw}}\ell_w e_w F_{0,j,w}$. Remove the signed main term and the inverse-square error from $D^{-1}\sum_j i_{jw}$ and take the positive part. Distributing this positive part equally over the $m$ layers gives nonnegative errors $e'_{jw}$. B8.38b gives a single family constant bounding $\sum_w\ell_w(e'_{jw}+e_wJ_{0,j,w})$ by $C L(B_0+N_c)$ in every layer, where $J_{0,j,w}$ bounds the normalized exponent carrying the cut into the integral pairing lattice. If $s_0$ is the common stabilizer denominator and $d_{j,t(w)}\mid d_g$ the local denominator, the integral containment on the cut gives
$$
 q_{jw}\le a_{jw}+D\big(e_wJ_{0,j,w}+v_w(d_{j,t(w)})+v_w(s_0)\big).
$$
Sum with weights $\ell_w$. The cut lengths cost at most $D(|C_N|+1)L(B_0+N_c)$ on the host family, or the supplied division allowance on the general family. The two integer denominators cost at most $D(\log d_g+\log s_0)$ per layer by the norm identity. The inverse-square contribution over all places and all layers is bounded by $2\sum_p\log(p)/p^2<1$. Consequently
$$
 \frac1D\sum_{w\in\mathrm{Tw}}\ell_w\sum_j(i_{jw}+q_{jw})
 \le 2F_*+O\big(mL(B_0+N_c)\big)
$$
with the original denominator-size bounds. The quotient Gram's additional global term $L_G$ costs at most $\log |G|+\log s_0$ on the same row. Together these give the finite part of B5.08x. The negative-lattice covolume is its distinct geometric summand. [Signed error assertion][on] · [Cut, denominator and Gram estimates][cut] · [Elementary bound for the inverse-square prime sum](PERIOD_JIN_PAIRED_REFERENCE.md#the-finite-estimate-in-the-original-units) · [Signed base and sharp levels](PERIOD_SIGNED_LEVEL_TRANSFER.md)

[native]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Formalism/SharpRestriction/GlobalTheoremInputs.lean#L59-L95
[window]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AutomorphicArithmetic/CharacterBoxes/ZeroFreeAllOfTopG.lean#L12-L23
[rank]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AbelianVarietyTheory/Proofs/GlobalInterpolation/SmallLevelRankEqClosedOfLevelProjectionSurjective.lean#L13-L47
[div]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AutomorphicArithmetic/CharacterBoxes/DivinNOfHypV.lean#L117-L130
[sum]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Formalism/LocalToGlobal/Divisibility/SumLeEtaSumNum.lean#L28-L64
[domain]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AutomorphicArithmetic/ThetaCorrespondence/ThetaPairLifts/ThirdPlaceSeries/ExportSt.lean#L22-L48
[producer]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AutomorphicArithmetic/ThetaCorrespondence/ThetaPairLifts/ThirdPlaceSeries/OntoXOfPrints.lean#L28-L45
[install]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AutomorphicArithmetic/ThetaCorrespondence/ThetaPairLifts/ThirdPlaceSeries/OntoXOfTwistSharesExp.lean#L20-L25
[host]: https://github.com/rh-lean-roadmap/rh-lean-roadmap/blob/6c23d34a14a3ecf19504ed4182596217ca75006b/docs/src/book/main.tex#L11774-L11786
[supply]: https://github.com/rh-lean-roadmap/rh-lean-roadmap/blob/6c23d34a14a3ecf19504ed4182596217ca75006b/docs/src/book/main.tex#L26421-L26431
[runs]: https://github.com/rh-lean-roadmap/rh-lean-roadmap/blob/6c23d34a14a3ecf19504ed4182596217ca75006b/docs/src/book/main.tex#L54360-L54378
[transport]: https://github.com/rh-lean-roadmap/rh-lean-roadmap/blob/6c23d34a14a3ecf19504ed4182596217ca75006b/docs/src/book/main.tex#L54318-L54354
[depths]: https://github.com/rh-lean-roadmap/rh-lean-roadmap/blob/6c23d34a14a3ecf19504ed4182596217ca75006b/docs/src/book/main.tex#L54380-L54405
[excess]: https://github.com/rh-lean-roadmap/rh-lean-roadmap/blob/6c23d34a14a3ecf19504ed4182596217ca75006b/docs/src/book/main.tex#L54407-L54434
[on]: https://github.com/rh-lean-roadmap/rh-lean-roadmap/blob/6c23d34a14a3ecf19504ed4182596217ca75006b/docs/src/book/main.tex#L21988-L22005
[cut]: https://github.com/rh-lean-roadmap/rh-lean-roadmap/blob/6c23d34a14a3ecf19504ed4182596217ca75006b/docs/src/book/main.tex#L32981-L32995
