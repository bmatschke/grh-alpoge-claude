# The squared real-place amplitude at the required counting moment

Let the original local datum satisfy the supplied eventual family hypotheses, including the Haar tie, and require the original discrete series to have arithmetic formal degree as in `ForAmp`. Write $n=k+m-1$, $s=m/2$, $B=b^{C_\beta}$ for a fixed envelope, and $H=b^{C_Hm^2}$. Distinguish the fixed exponent bounding the input terminal sizes, $T_{p,1},T_{q,1}\le B^{2|C_{\rm in}|m}$, from the output constant $C_H$. Set $\sigma=\prod_{l=1}^s\max(1,d_l/H)$, where the omitted zeroth minor equals one. Then, from the wave-shortening and terminal-moment inputs in the [unweighted proof](SPECTRAL_ORDINARY_SQUARED_AMPLITUDE.md) and the signed one-step expansion for all leading minors, one obtains
$$
   \frac{\eta G^k\|J_\gamma\|_{\rm HS}^2}{d}
     \le L_\tau(t')^{-k}\sigma^{-2q/s},
   \qquad 0\le q\le C_{\rm pr}km^2.                                    \tag{6}
$$
The constants in $L_\tau$ and $C_H$ can be chosen before $C_{\rm pr}$. As in the original eventual statement, the rank threshold may depend on $C_{\rm pr}$. This includes cells with vanishing proper minors. It proves the first inequality in the source's `stDEC`, subject to the named analytic inputs. [Target and quantifiers][qtarget]

References to (3) and (5) refer to the section mass and the unweighted point bound in the [normalization calculation](SPECTRAL_ORDINARY_SQUARED_AMPLITUDE.md).

**A uniform shifted estimate.** Keep the grid centered at the supplied unshifted parameter $\lambda$. For fixed $C_{\rm pr}\ge0$ take $E=\lfloor C_{\rm pr}km^2\rfloor$ and a shifted representation of parameter $\lambda+\nu$, with integral $\|\nu\|_1\le sE$. The coefficient attached to this shifted representation is detected at the same two compact types and with the same physical frames. Since the shifted representation is a supplied good child, the squared mass $M_\nu$ is finite and strictly positive. For its actual physical amplitude define $U_\nu=J_\nu/\sqrt{M_\nu}$. The unweighted point-to-section estimate (5) holds uniformly for these $U_\nu$ in the form
$$
 p\|U_\nu(\gamma)\|_{\rm HS}^2
       \le b^{C_3m^4}\max(1,G^{-1})^{40s^2}.                            \tag{7}
$$
The original arithmetic degree identity is used for the starting representation at the last step (3) only. Each child uses its own actual mass in (7). [Shifted physical detector, positive mass and root comparison][qdet]

Here are the shift checks needed to obtain (7). The Roadmap endpoint construction begins explicitly with a coefficient at $\lambda+\nu$ and includes the possible compact-type contractions. Its polynomial degree loss is $d_{\max}=mp_0+(30s^2+6)s\le5m^3$. Use
$$
      c=sE+5m^3+1,\qquad Q=sE+40s^3+s(s+1).
$$
The eigenvalues of every endpoint summand have coordinate displacement at most $c$ from $\lambda$. The grid lemma only needs adjacent upper gaps at least $1+c$, $B\ge c+2$, half-integral interlacing at the **anchor**, and the fixed cut between compact weights. Its actual progression and cardinality are independent of $E$. The shifted compact contractions in the equal-type case use the same one-exception grid as in the zero-exponent proof. Their compact shift size remains $30s^2+6$. [Grid statement][qgrid] · [Starting at a shifted representation][qstart]

For completeness, the original lower bound on every gap exceeds $C_lkm^4+nm^{10}$, the opposite-sign gap exceeds or equals $C_l n^{19}f^5\log b$, and the splitting scale $b_v$ obeys $k^8\le b_v\le B$. Here $8m^2\le k$ and $k\le n\le2k$. For fixed $C_{\rm pr}$ one has $c,Q=O((1+C_{\rm pr})km^3)$, hence eventually $2c$ and $100(Q+1)$ fit in both gap lower bounds. Also $c+2\le k^8\le B$ and $10^6 n^7\le b_v$ eventually. To check endpoint decay, put $X=s^4(3sn^2+n^3)$. Then $C_tn^3+C_AX+3d_{\max}+1+2sE$ is below the opposite-sign gap for the fixed constants $C_t,C_A$. The same opposite-sign gap satisfies the period quarter-gap threshold used in the zero-exponent proof. Only the anchor is required to lie in the two specified ranges for the coordinates. The numerical family lemma requires the anchored shape, interlacing and parity, the gap quarter-condition, the two inequalities $100(Q+1)\le g_{\rm all},g_{\pm}$, and $10^6n^7\le b_v$. The independent gap parameters $g_{\rm all}$ and $g_{\pm}$ can be taken to be the source lower bounds just given. Thus it admits this $Q$. In particular all descendants needed in the **terminal** expansion fit because $\|\nu\|_1+sh+s(s+1)\le Q$ for $h\le40s^2$. The bound for that expansion is $B^{(|C_{\rm in}|+6)m^2h}$ regardless of the initial shift. The unweighted cutoff removal, contraction, terminal expansion and torus transfer proving (5) now give (7). The joint physical coefficient and section comparison applies at the shifted parameter too, with the prescribed root measure factor. No critical arithmetic degree is substituted for any shifted child. [Native gap and splitting inputs][qgap] · [Native numerical family lemma with independent gaps][qnum] · [Uniform terminal moment][qterm]

The original pointwise estimate also distinguishes the unshifted parameter that fixes the grid from the actual parameter of the representation. Its hypotheses put the cluster boxes, interlacing and compact cut at the anchor and allow a separate displacement bounded by one two-hundredth of the anchor gaps. The reserve above gives this stronger factor 200 eventually as well. [Pointwise theorem at a displaced parameter](https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AbelianVarietyTheory/Proofs/FlagMeasures/BesselPointwiseBoundAtLargeGaps.lean#L18-L61) · [Anchor conditions](https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Formalism/SharpRestriction/CuspSpanNormBounds/LeadMinorK.lean#L65-L78)

**Multiplication by the physical minor.** For $0\le l\le s$, the native signed exterior-power identity expands $D_l U_\nu$ as a finite sum of shifted normalized amplitudes. Every child with nonzero coefficient has parameter $\lambda+\nu\pm\mathbf1_I$ for $|I|=l$. Vanishing branches have coefficient zero. The sum of absolute coefficients costs at most $b^{C_Dm^2}$, with $C_D$ chosen before the permitted displacement coefficient $C_n$. This bound includes the projected period scalars on both sides, the formal-degree ratio, and the sum over subsets. The section normalization in this identity is precisely the physical $M_\nu$ used in (7). The theorem applies for all $l$ at once on the eventual window $\|\nu\|_1\le C_nkm^3$. Its analytic inputs are the signed exterior tensor projection, the large-gap period bounds and the orbital convergence identification. [Signed one-step identity and cost][qminor] · [Physical section normalization][qunit]

Choose $C_n=1+C_{\rm pr}$, which covers every index reached in $q$ steps because $sq\le C_{\rm pr}km^3/2$. Induction on the number of multiplications gives
$$
 D_l^q U_0=\sum_P a_P U_{\nu_P},\qquad
 \sum_P|a_P|\le b^{C_Dm^2q},\qquad \|\nu_P\|_1\le lq.
$$
Indeed each path coefficient is its parent's coefficient times one outgoing coefficient; summing absolute values multiplies the preceding bound by at most the one-step cost. Taking the Hilbert–Schmidt norm, applying (7) to each surviving leaf and squaring once gives
$$
 d_l^{2q}p\|U_0(\gamma)\|_{\rm HS}^2
   \le b^{2C_Dm^2q+C_3m^4}\max(1,G^{-1})^{40s^2}.
$$
If some $d_l>H$, choose the largest. With $C_H\ge\max(C_D,0)$, division gives a factor at most $(d_l/H)^{-2q}\le\sigma^{-2q/s}$. If all $d_l\le H$, (5) suffices. Multiply by the original mass and use (3) and the same block-end conversion to obtain (6). This uses the physical minor identity only after transporting the **unweighted** shifted estimate, so transport costs a fixed $b^{O(m^4)}$ with no $q$-dependence.

There is a shorter check for $q\le m^3$. Use the printed Roadmap bound with fixed exterior exponent $e_*=m^3$. Then its physical $b^{C_*m^5}$ factor (including torus transport) is covered by $H^{2e_*}$ if $2C_H\ge C_*$. Above $H$, the resulting power $-2e_*/s$ implies $-2q/s$, and below $H$ (5) applies. The full range in (6) uses the larger original gaps and the separate normalized one-step identity.

### Cost of one exterior-power step in the physical frame

Here is the coefficient bound for the original period normalization used in the iteration. Write $n=k+2r+1$. At a parameter $\mu$, denote its formal degree by $d_0$ and the degree at $\mu+\mathbf1_I$ by $d_I$, for $|I|=l\le r+1$. These degrees refer to representations of the noncompact group with the same Haar measure. Use the supplied signed exterior decomposition of the discrete-series tensor product, the multiplicity-one period maps, the cofactor bounds for their two projections and the common big-cell mass comparison. The physical-frame proof permits the plus shift in every nonzero branch. The coefficient of the $I$-branch in the section-normalized orbital vector satisfies
$$
 |a_I|\le \sqrt{d_0/d_I}\,|\kappa_I\kappa'_I|.
$$
Indeed the leading minor is the matrix coefficient between the two exterior frame vectors. Tensor it with the original coefficient, insert the signed projections, and apply the two period maps. Each becomes a scalar multiple, $\kappa_I$ or $\kappa'_I$, of the old period. The signs have modulus one. The common section mass has inverse-degree dependence with the same constant for all those data; passing to unit section mass gives the displayed square root. If either period projection vanishes the term contributes zero. This is where using precisely the same section in each normalization matters. [Tensor identity and scalar](https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AbelianVarietyTheory/Proofs/FlagMeasures/LeadingMinorLineUnitAmplitudesLargeGaps.lean#L112-L175) · [Identical section and plus-shift choice](https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AbelianVarietyTheory/Proofs/FlagMeasures/LeadingMinorLineUnitAmplitudesLargeGaps.lean#L359-L371)

Let $S_l$ be the modulus of the product of the $l$ diagonal frame-transport entries. The two cofactor estimates take the form $|\kappa_I|^2 d_0/d_I\le S_l^2 H(T)^l$ and $|\kappa'_I|^2 d_0/d_I\le S_l^2 H(T')^l$ with the transported scales of the source. Multiplying, taking a square root, and using the preceding coefficient bound gives
$$
 |a_I|\le S_l^2\{H(T)H(T')\}^{l/2}\sqrt{d_I/d_0}.
$$
The compact-dual degree formula gives $d_I/d_0\le n^l$. For example, in the Vandermonde ratio add the selected coordinates one at a time while keeping the gap reserve. Terms from larger coordinates can only decrease, and the factors from smaller coordinates telescope against $\prod_{a=1}^{n-i}(1+1/a)\le n$ for coordinate $i$. There are at most $n^l$ choices of $I$. The source bounds $S_l\le b^{(2C_g+2)m^2}$, both terminal-norm factors by its $b^{(|C_T|+20U)m^2}$ allowance each, and each occurrence of $n^l$ by $b^{Um^2}$, with $U=\max(2,C_u)$. In particular
$$
 \sum_I|a_I|\le b^{C_Dm^2},\qquad
 C_D=2(2C_g+2)+2(|C_T|+20U)+2U .
$$
The constants in this one-step bound precede the depth of the iteration. Its explicit inputs include the normalized exterior period estimates on the shifted discrete-series family and the positive common-section comparison. Taking only an abstract decomposition of an exterior power would leave $\kappa_I,\kappa'_I$ uncontrolled. [Cofactor scale](https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AbelianVarietyTheory/Proofs/FlagMeasures/LeadingMinorLineUnitAmplitudesLargeGaps.lean#L256-L266) · [Frame cost, degree ratio and sum](https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AbelianVarietyTheory/Proofs/FlagMeasures/LeadingMinorLineUnitAmplitudesLargeGaps.lean#L501-L548)

[qtarget]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Formalism/SharpRestriction/CuspSpanNormBounds/AmplitudeAndVolumeBounds.lean#L342-L355
[qdet]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AbelianVarietyTheory/Proofs/FlagMeasures/AmplitudeEqBesselFunctionLargeGaps.lean#L140-L193
[qgrid]: https://github.com/rh-lean-roadmap/rh-lean-roadmap/blob/dc5594a62bb2b94139788df817db693cd939a046/docs/src/book/main.tex#L17077-L17100
[qstart]: https://github.com/rh-lean-roadmap/rh-lean-roadmap/blob/dc5594a62bb2b94139788df817db693cd939a046/docs/src/book/main.tex#L44885-L44917
[qgap]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Formalism/SharpRestriction/CuspSpanNormBounds/BruhatCellsKronecker/StandardHypothesesOfScaleHyp.lean#L88-L101
[qnum]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/CompanionTheory/AutomorphicTheory/BesselWaveGrids/PowFourLeRpowNineHalves.lean#L41-L56
[qterm]: https://github.com/rh-lean-roadmap/rh-lean-roadmap/blob/dc5594a62bb2b94139788df817db693cd939a046/docs/src/book/main.tex#L45175-L45279
[qminor]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AbelianVarietyTheory/Proofs/FlagMeasures/LeadingMinorLineUnitAmplitudesLargeGaps.lean#L359-L551
[qunit]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Formalism/SharpRestriction/CuspSpanNormBounds/NormalizedLocalScale.lean#L183-L215
