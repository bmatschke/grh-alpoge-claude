# Independent review of ZW1–ZW4

**Result: PASS after clarifying edits.** The weighted-slope proof, all six uniform table estimates, the replacement threshold $200R^3\le x^\epsilon$, and the exact terminal exponent are correct. No additional arithmetic-existence premise is needed after the literal common-family `ChainTied` record is supplied. The eleven geometric ledger fields remain inputs to its producer.

## Reviewed text and scope

The reviewed chapter is `reconstruction_v030/tied_window_completion/main.tex`. Its final whole-file SHA-256 is **3e102f1a3e4ddced78b5cd3e92378a3ebdfa68a52b7de5fb69e2ac997eddc7b1**. The accompanying JSON also records separate ZW1–ZW4 range hashes, the inherited WB consumer hash and 24 pinned source blocks. Every recorded source file was compared byte for byte with its Git blob at `7cbf7a0c32fca1badf05931879a37c3f8a2b03b4`.

The edits remove an unwarranted comparison with the source numerical constant, distinguish the ledger exponent $\alpha=C.\texttt{cHH}$ from its fixed global upper bound, state the $0\log0=0$ convention, and make the eventual quantifiers and finite-cardinality conditions explicit. The statement and final exponent are unchanged. The detailed edit log is `zw_review_edits.json`.

## Finite weighted-slope calculation

Positive weights and a nonempty finite word set justify all averages and show $u\ge0$. The sign in the height comparison is correct:

\[
(-E_v-h_v)-(-E_w-h_w)
\le 2mc_EB_0+c_H(n_TaL_a+mB_0)+A(t_v-t_w)
\le V.
\]

Combining the upper slope at $v$ with the lower slope at $w$, then averaging over $w$, yields $u\le K_3+\langle L_w\rangle\le U$. The loss hypotheses are pointwise in the translate, exactly as required. No averaging over translates or selection of a favorable word has been substituted.

The divisibility inequality has the displayed rearrangement $F-h_w\ge\mu_C-S_D+At_w-E_D$. Positivity of $A$ permits the lower count bound; the exponent comparison supplies the upper bound on $E_w$. In the resulting finite identity, the $mA\,\mathrm{lg}$ terms cancel, as do the $v/\pi$ logarithms. The remaining expression is exactly the source Main term and its $Ac_C L_a(1+m^2/k)$ error. The positive $w,v$ and $f>0$ hypotheses are present in `HidaSetting`; the continuous convention handles a zero $a_t$.

The logarithm step is valid. For $u>0$, Jensen's inequality with weights $u/(u+b)$ and $b/(u+b)$ and arguments $1+H/u$ and $1$ gives

\[
u\log(1+H/u)\le (u+b)\log(1+H/(u+b))
\le (U+b)\log(1+X).
\]

At $u=0$ both relevant expressions are zero after extension. `FParams`, `HHBound` and `HidaSetting` supply all antecedents of `SlopeIneq`. Its nonnegative error terms permit the reciprocal and square-root increases. With the local exponent written as $\alpha=C.\texttt{cHH}$, (ZW.8) is literally `ErrX5at`.

## Every uniform bound checked

Put $z=x^\epsilon$ and use $R,z\ge1$. The original windows give $m/k\le1$, $mb\le a$, $A\le2n_Ta$, $E\ge n_Ta$, $E\ge mB_0$, $L,L_a\le2z$ and $\log k\le e_K\log x\le Rz$.

| Quantity | Independent bound and accounting |
|---|---|
| $L_P$ | $REz^{e_L}$, using $mb\le a$. |
| $V$ | The first two groups cost at most $5REz$; the logarithmic group costs $2R^2Ez$, totaling at most $7R^2Ez$. |
| $K_3$ | $B_1\le4REz$, $B_2\le2REz$, $P\le REz$, plus $V$ give $14R^2Ez$. |
| $M_L$ | The three groups cost $R^2Ez^{e_L}$, $4R^2Ez$, and $2RE$, giving $7R^2Ez^{e_L+1}$. |
| $U$ | Adding $K_3$ and $M_L$ gives $21R^2Ez^{e_L+1}$. |
| $K_0$ | The linear-$z$ groups cost $(4+2+1+4)REz$; the remaining divisibility term costs $REz^{e_D}$. |

The only mixed term uses $b'\le a/k$ and equals at most $4R^2n_Ta(m^2/k)z$, which is bounded by $4R^2Ez$. No factor depending on a growing field or on the word count has been lost.

The nonlinear line of (ZW.8) is at most $178R^3Ez^{e_L+2}$. Its first line is at most $21R^3Ez^{e_D+e_L+2}$. As $e_D,e_L\ge0$ whenever a ledger exists, their sum is at most $199R^3Ez^{e_D+e_L+2}$, hence at most $Ez^{e_D+e_L+3}$ once $200R^3\le z$. All thresholds depend only on the fixed exponents, constants and $\epsilon$.

## Original data and final quantifiers

The `TieArith`/`TT_eq` combination identifies the actual top sets by injectivity of their integer labels. The original host, its word sets and weights, the identity coverage map, actual logarithmic derivatives and all source identifications are retained. `IdentU` supplies the exact Main/ASK/gap identities; `BNBoundsU` enlarges only nonnegative bracket terms. `RestSize` and `ErrWindows` supply all WB6 scalar inequalities, including the lower bounds ensuring positive $m,n_T,n_2$.

The retained character family stays fixed by the cyclic level. `EFamC` supplies one character constant and one threshold before $x$; if necessary replace that constant by its maximum with zero. `ChainTied` supplies its constants and threshold before $x$. The finite maximum is therefore fixed before the original index $i_0(x)$ is chosen, while that index and its host may vary with $x$.

Finally `FamilyClassConnected` fixes $e_D,e_L$ before choosing $\epsilon$. The actual `GChi.cls` provides `EFamC` with constant $4$ and full intervals of the fixed stretch $3/2$ at arbitrarily late locations. The absorption exponent $e_D+e_L+3$ and WB's subsequent $+4$ give exactly $e_D+e_L+7$, hence $1/2+9\epsilon$ on the selected $(e_D,e_L)=(2,0)$ route. Choosing $\epsilon$ after the proposed zero's margin and before its family and window is valid.

## Validation

Standalone draft-mode TeX compilation passed with exit code zero and no fatal errors, undefined controls or overfull boxes. This checks syntax and basic text fitting only; it is not a visual PDF review or a new Lean replay. The JSON records the compiled source hash.
