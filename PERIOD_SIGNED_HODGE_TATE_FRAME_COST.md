# The signed cost of changing a record frame to a Hodge–Tate frame

The original mixed-valuation comparison in entry 7 charges the full absolute weight of a section in each direction. At an algebraic integral frame the transition has a definite direction on every one-dimensional flag quotient. This gives a sharper bound for the original mixed invariant if that invariant is wanted in addition to the [direct determinant argument](PERIOD_RECORD_TRACE_TO_CHOW.md).

Use a coefficient place $\lambda\mid p$ and normalize the additive valuation on the completed algebraic closure by $v_p(p)=1$. Let $r,s$ be the signature ranks and $n=r+s$. For the row weight $(u,0)$ define
$$
 W_+(u)=\sum_{\tau\in\Psi}\left(\sum_{i<r}(u_{\tau i})_+
                      +\sum_{r\le i<n}(-u_{\tau i})_+\right),
 \qquad W_-(u)=W_+(-u),\qquad x_+=\max(x,0).
$$
Thus $W_++W_-=\|u\|_1$. Write $\delta_p=v_p(|\operatorname{disc}E|)/[E:\mathbf Q]$ (the numerator here means the exponent of the rational prime), and $b_p=1/(p-1)+\delta_p$. For a Hodge–Tate test with underlying record frame, let $w$ and $v_0$ denote the two section valuations normalized to extend $\operatorname{ord}_\lambda$. A section $f$ with nonzero value satisfies
$$
 -\operatorname{ord}_\lambda(p)b_p W_+(u)
       \ \le\ w(f)-v_0(f)\ \le\
     \operatorname{ord}_\lambda(p)b_p W_-(u).                         \tag{1}
$$
If one reading is zero both are zero, and the separate inequalities between valuations still hold with $+\infty$. Here the tests are those of the original Hodge–Tate frame construction, with its integral Lie eigenbasis, compatible flag and comparison to the Tate and Lie pairings. This includes its comparisons on the semiabelian traits used to define the patched family. [Definition of the test and section valuations][mixed] · [Actual change of frames][diag]

## The lattice calculation

Write $b_i$ for the record basis vectors placed in the comparison space at an embedding, and $\Lambda_0=\sum_i\mathcal O_C b_i$. The corresponding Hodge–Tate eigenlattice $\Lambda$ contains $\Lambda_0$. In the original frame construction multiplication by $\kappa\delta_\tau$ takes $\Lambda$ into $\Lambda_0$, where $v_p(\kappa)=1/(p-1)$ and $v_p(\delta_\tau)=\delta_p$. These two factors have different origins.

* To clear the projection to an eigenspace, multiply the corresponding idempotent by a local generator from the different. In a basis of the integral order and its trace-dual basis the idempotent is written using the trace-dual coordinates; multiplication by the different makes those coordinates integral. The unprojected lattice is stable under the integral order. One can take an element of the global different with its exact local exponent at the given prime by choosing it outside the product of that prime and the different. Since $E/\mathbf Q$ is Galois, this exponent divided by the local ramification index is $\delta_p$. For an eigenspace defined by intersection with the original lattice the same multiplier is permitted. [Eigenspace projection and local different][diff]
* For the other factor use the cokernel bound for the integral Hodge–Tate map, with $\kappa^{p-1}=p$. To see how it estimates this lattice, choose coordinates on the integral Lie module. Each coordinate times $\kappa$ is the image of an integral Tate vector. Pairing with this vector reads the corresponding coordinate times $\kappa$ on the rational Lie image. Its pairing with an integral Tate-lattice vector is integral. Hence multiplying an integral vector in that image by $\kappa$ gives an integral Lie vector. After the preceding projection clearing it has the prescribed eigencharacter, so its coordinates in the supplied integral Lie eigenbasis are integral. This proves the asserted inclusion. The comparisons identifying the Raynaud point and its Lie pairing on degenerating tests are part of the stated frame hypotheses. [Fargues, §5.3.2, Theorem 2](https://www.numdam.org/item/10.24033/asens.2157.pdf) · [Source coefficient argument][coeff]

On the common flag the transition from the record basis to a basis of $\Lambda$ is triangular, with diagonal entries $t_i$. Because $\Lambda_0\subseteq\Lambda$, the inverse transition has integral entries. Because $\kappa\delta_\tau\Lambda\subseteq\Lambda_0$, the forward transition becomes integral after multiplication by $\kappa\delta_\tau$. Consequently $-b_p\le v_p(t_i)\le0$, including at $p=2$. On the additional scalar coordinate the change is a unit. The Borel transformation formula reads the new value as the old value times $\prod_i t_i^{e_i}$. In the first block $e_i=u_{\tau i}$ and in the conjugate block the exponents are the negatives of the last $s$ entries in reverse order. Thus positive exponents can only decrease the valuation and negative exponents can only increase it. Summing the intervals for the individual terms and restoring $\operatorname{ord}_\lambda(p)$ proves (1). [Triangular lattice proof][diag] · [Borel transformation][borel] · [Signs of the two weights][weights]

## The original mixed count

Let $S_B$ be the source's patched set of primes. Put
$$
 H_B^\sharp=\sum_{p\in S_B} b_p\log p
 =\sum_{p\in S_B}\frac{\log p}{p-1}+\log\operatorname{rd}(E).
$$
The equality uses the inclusion of every discriminant prime in $S_B$. The record-trace step on the supplied root origin costs $c_R=c_2(B)\|u\|_1$. Clearing each degree-$j$ trace coordinate also for the mixed family requires at most the further rational factor $\prod_{p\in S_B}p^{\lceil jb_pW_+(u)\rceil}$. Indeed each mixed test at such a prime comes with its algebraic integral record frame, to which (1) applies. The logarithmic cost per degree tends to $W_+(u)H_B^\sharp$. The same shifted-index limsup argument as in the [record trace count](PERIOD_RECORD_TRACE_TO_CHOW.md) gives the original invariant the lower bound
$$
               \nu_Z(u;B)\ge a_Z-c_R-W_+(u)H_B^\sharp .               \tag{2}
$$
In the other direction, wherever the lift of each algebraic integral record frame to a Hodge–Tate frame is supplied as in the carrying step, (1) shows that the cost of converting a mixed-integral section back to record integrality is at most $W_-(u)H_B^\sharp$ per degree. For $u=u'$ the anchored entry $u'_{\tau,k-2}=0$ and the entries decrease strictly across the row. The last $s$ entries are negative. Thus $W_-(u')$ is precisely the sum of $-u'_{\tau i}$ over $k-1\le i<r$ on each CM row; the first block has $r=k+j-1$, so there are only $j$ charged positions per row. Even in a proof retaining both changes of valuation, their combined allowance is $\|u'\|_1 H_B^\sharp$. Model-to-record trace costs are separate. [Original mixed comparison][native] · [Lifting a given record test](https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AbelianVarietyTheory/Proofs/DivisorProofs/SumAbsExOfLe.lean#L378-L387) · [Shifted weight and return to integral sections][return]

[mixed]: https://github.com/rh-lean-roadmap/rh-lean-roadmap/blob/dc5594a62bb2b94139788df817db693cd939a046/docs/src/book/main.tex#L19977-L19991
[diag]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AutomorphicSpectrum/Proofs/GeometryProofs/ExistsBLieEqSmul.lean#L312-L343
[diff]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AutomorphicSpectrum/Proofs/GeometryProofs/ExistsBLieEqSmul.lean#L344-L377
[coeff]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AutomorphicSpectrum/Proofs/GeometryProofs/ExistsBLieEqSmul.lean#L265-L311
[borel]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AbelianVarietyTheory/Proofs/DivisorProofs/TestValueEqConstMulReadingSecZ.lean#L71-L79
[weights]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AbelianVarietyTheory/Definitions/Foundations/IsProbabilityMeasureMuPart.lean#L208-L218
[native]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AutomorphicSpectrum/Proofs/GeometryProofs/UniformAllNormHeightBound.lean#L300-L372
[return]: https://github.com/rh-lean-roadmap/rh-lean-roadmap/blob/dc5594a62bb2b94139788df817db693cd939a046/docs/src/book/main.tex#L53738-L53773
