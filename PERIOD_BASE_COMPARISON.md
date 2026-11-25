# A reference period from the diagonal estimate

Entry 4 of the period-height comparison needs a single change of row coordinates for all words. The RH Lean Roadmap obtains it from a central translation and a seesaw argument that carries linear relations between periods down two lifts at a time. On the tied marked model, the following argument supplies its nonzero reference pairing from a quantitative part of the diagonal estimate. It identifies which additional geometric and automorphic assertions a proof on the selected family must supply. [Base-tuple criterion](continuation_v89/comparison.tex#L34-L98) · [Roadmap's reference argument][anchor]

## How much of the diagonal bound is needed?

Fix a word, write $C$ for its full column space, $d=\dim C$, and let $P:C\to H$ be its spectral period operator before the good-type projection. Write $K=\alpha^{-1}P^*P$, where $\alpha=\operatorname{vol}(N_u)\operatorname{vol}(H_u)/\dim\pi_u>0$ is the identity-cell normalization for this word. Let $U\subseteq C$ be the simultaneous kernel of the level norms at the $f$ places above $T=T_u$. The marked model gives
$$
 \dim U=\rho d,\qquad \rho=\left(1-\frac1{T-1}\right)^f.
$$
Indeed the marking group is the product of $f$ copies of $\mathbb F_T^\times$. A diamond fixing a class can be represented by a rational isometry $\gamma$ whose power belongs to the finite class stabilizer, since the diamonds normalize the level. Thus $\gamma$ has finite order. At both type primes the locally conjugated element belongs to a subgroup with unipotent reduction and pro-prime congruence kernel. Its order must be a power of both distinct residue characteristics. This forces $\gamma=1$ and all the marked multipliers to be one. On each free orbit transport a coefficient basis from one fibre. In that basis the action is a sum of regular representations. The norm in one factor kills exactly the nontrivial characters of that factor. Requiring this at every factor retains $(T-2)^f$ characters out of $(T-1)^f$. In particular $\rho>1/2$ if $T-1>2f$, by Bernoulli's inequality. [Definition of the normalized Gram operator][gram] · [Freeness on the specified markings][diamond] · [Coefficient fibres and their norms][fibres]

Put $\delta=\|K-I\|_{\rm HS}$. On $U\cap\ker P$ the operator $K-I$ equals $-I$. Taking an orthonormal basis of this kernel, extended to the whole domain, gives
$$
 \operatorname{rank}(P|_U)\ \ge\ \dim U-\delta^2 .
$$
One also gets a reference vector of controlled size when $h=\dim U>0$. Let $\Pi$ be the orthogonal projection onto $U$. By Cauchy–Schwarz in the Hilbert–Schmidt inner product,
$$
 \alpha^{-1}\operatorname{tr}\bigl((P|_U)^*P|_U\bigr)
   =h+\operatorname{tr}\bigl(\Pi(K-I)\bigr)
   \ge h-\sqrt h\,\delta .
$$
The largest eigenvalue is at least the average. Some unit $\phi\in U$ therefore satisfies $\|P\phi\|^2\ge\alpha(1-\delta/\sqrt h)$. In particular $\delta^2<\rho d$ suffices when $d>0$. On any range where the native diagonal bound actually applies, $\delta^2\le e_0 d$ and $e_0<\rho$ eventually suffices. The native spectral assertion is an implication with a comparability premise on the word dimensions. The [marked class count and prime window](PERIOD_FULL_REFERENCE_PAIRING.md) prove this premise with $C_0=3$ on the original linked members. For construction before final selection one still needs the diagonal estimate or a descended nonzero pairing on that earlier domain. The estimate on the singular cell alone does not bound $\delta$. [Native spectral implication][linkS] · [Singular-cell bound](SPECTRAL_DIAGONAL_ZERO_CELL.md)

Use the translated evaluation $J_z$ of a **full** reference multiplicity map at the unit lowest-type vector, in the convention identifying its range with $H$. This includes the conjugation required for row functions. The finite central translation $z$ commutes with the level projector and acts unitarily by Haar invariance. On the linked model full-level surjectivity is obtained from formal-degree orthogonality and cyclicity of the lowest-type vector, with cuspidality of the projected image. Explicitly the compressed translate acts by the matrix coefficient of that vector, so the orbit of any value in $H$ determines an intertwiner with that value. Thus there is a full reference row $T_0$ with $J_zT_0=P\phi$, and its reference pairing is $b_0=\|P\phi\|^2>0$. No lower bound on the projection of this vector to a good type is needed. If the permitted column is zero the comparison on that column is vacuous. [Translated evaluation before projection][eval] · [Reference choice][anchor]

## Carrying one pair down the same tower

Here the hypotheses are the matched row and column frames, the defining row lifts and finite charts at each stage, full reference descent onto the bottom multiplicity space, and the identified normalizations of the terminal pairing and bottom translation. These are the geometric and automorphic inputs of B8.08i. In particular, surjectivity of *bottom evaluation* above does not by itself lift $T_0$ through the theta tower. The latter follows under doubling nonvanishing on each reference eigenspace and separation of their lifted Hecke systems. Adjoining the same list of parameters preserves that separation by cancellation of multisets. [Full reference descent and normalization][desc]

In the two-step seesaw, an upper relation that vanishes at every frame and real argument yields a lower relation after multiplying by the two row-lift constants. To see why the coefficients work for both entries of the relation, expand the compact polynomial average in frame evaluations before inserting a class form. Invertible frames determine every polynomial in the finite-dimensional coefficient space. The weights fix their determinant factors, so the expansion coefficients are common to both entries. Refine the two levels to their intersection, sum the finite averages there, and integrate the identically zero sum. Cuspidal decay controls the interchange with the quotient integrals. Real translates of the prescribed polynomial tests generate the irreducible compact-finite module and continuity extends the relation to smooth vectors. At the terminal pair there is a single branching map by multiplicity one. At the bottom there is one finite translation. Iterating the two-step implication and unfolding the bottom pairing therefore gives, in the Roadmap's normalizations,
$$
 \lambda p+\lambda' c_t A_t(\phi',F)=0
 \quad\Longrightarrow\quad
 \lambda b_0+\lambda' B_t(\phi',F)=0 .
$$
Here $p$ is the normalized top reference period, $A_t$ the arithmetic evaluation, $B_t$ the bottom model pairing and $c_t\ne0$ the quotient of lift constants, with the fixed column normalization absorbed. The same $p,b_0$ apply to every input for this word. The choice $(\lambda,\lambda')=(1,0)$ rules out $p=0$. The choice $(c_t A_t,-p)$ then gives $c_t A_t b_0=p B_t$, including at every zero of either form. [Double-step and terminal relations][seesaw]

On the good rows let $V$ be right translation by the same central $z$ for every word. This preserves the good idempotent and the norm. For this word write $S^{-1}$ for the column change in descent, $r_u>0$ for its norm multiplier, and $R$ for the bottom column isometry. The composite $r_u^{-1}RS^{-1}$ gives the required column unitary in the common coordinates. On writing the reference identity in the joined Petersson metrics, denote the adjusted reference scalars by $p_u,b_u$. Both are nonzero. In conjugate row coordinates one conjugates all three scalars and the entries of the column matrix together. At the base tuple $t_0$ it gives exactly the base criterion with $a_u=p_u/(c_{u,t_0}b_u)$ and these unitaries. No other tuple enters that criterion. The selected rational-coordinate statement and bilinearity then give every complex argument, hence the three-rank equality of the normalized Gram families. This is a conditional derivation of entry 4. The actual level-by-level comparison on the chosen arithmetic rows, full reference descent and an applicable nonsingular diagonal estimate are outstanding for a self-contained proof on the uniform range. [Joined comparison][desc] · [Three ranks](continuation_v90/intertwiners.tex#L62-L95)

[diamond]: https://github.com/rh-lean-roadmap/rh-lean-roadmap/blob/94e6a98b4e74932a0298d6bd22d44cf60c62764b/docs/src/book/main.tex#L32020-L32030
[fibres]: https://github.com/rh-lean-roadmap/rh-lean-roadmap/blob/94e6a98b4e74932a0298d6bd22d44cf60c62764b/docs/src/book/main.tex#L43686-L43692
[eval]: https://github.com/rh-lean-roadmap/rh-lean-roadmap/blob/94e6a98b4e74932a0298d6bd22d44cf60c62764b/docs/src/book/main.tex#L43629-L43652
[anchor]: https://github.com/rh-lean-roadmap/rh-lean-roadmap/blob/94e6a98b4e74932a0298d6bd22d44cf60c62764b/docs/src/book/main.tex#L44270-L44284
[seesaw]: https://github.com/rh-lean-roadmap/rh-lean-roadmap/blob/94e6a98b4e74932a0298d6bd22d44cf60c62764b/docs/src/book/main.tex#L44285-L44342
[desc]: https://github.com/rh-lean-roadmap/rh-lean-roadmap/blob/94e6a98b4e74932a0298d6bd22d44cf60c62764b/docs/src/book/main.tex#L44345-L44366
[linkS]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Formalism/SharpRestriction/GlobalTheoremInputs.lean#L142-L157

[gram]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Formalism/SharpRestriction/CuspSpanNormBounds/RelevantZeroGramTerms.lean#L332-L345
