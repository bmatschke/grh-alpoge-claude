# Recovering the two compact contractions at equal weights

At a real place where the two compact parameters coincide, the wave proof replaces the coefficient by two coefficients with different right compact types. We prove the comparison for the actual positive Hermitian complement to the final flag vector. The bound below retains the width of the chosen gap and gives a factorial gain over the uniform estimate used in the [squared-amplitude argument](SPECTRAL_ORDINARY_SQUARED_AMPLITUDE.md). The wave estimates for the two shifted coefficients are separate inputs.

Let $V$ be the original compact $U(k)$-type on this complement $E$. Write its strictly decreasing shifted coordinates as $L_0,\ldots,L_{k-1}$ after removing a common scalar, so all differences are integral. Fix $i<k-1$, set $D=L_0-L_{k-1}$, $g_*=L_i-L_{i+1}$, and suppose $g_*\ge2d+1$ for a positive integer $d$. In the application $d=30s^2+6$, $s=m/2$, and $D\le2B$ on the selected equal-weight grid. Put
$$
 q_*=\lceil(g_*-1)/2\rceil,\qquad (q_*)_{d}=q_*(q_*-1)\cdots(q_*-d+1).
$$
The two types shift $L_{i+1}$ up by $d$ or $L_i$ down by $d$. There are equivariant degree-$d$ polynomial contractions $A_\pm(\omega):V_\pm\to V$ such that for $\omega\in E$,
$$
 \|A_\pm(\omega)\|\le\|\omega\|^d,\qquad
 \|\omega\|^{2d}\|v\|^2\le
 \frac{D^{2d}}{(q_*)_d}\sum_\pm\|A_\pm(\omega)^*v\|^2.                       \tag{1}
$$
In particular $(q_*)_d\ge d!$. This is uniform in the compact vector and the real point. [Selected cuts and real norm at the point][real] · [Roadmap compact contraction lemma][statement]

**Construction.** Fix a unit $e\in E$. Under $U(k-1)$ fixing $e$, the compact branching rule decomposes $V$ into interlacing spaces indexed by $L_{j+1}<M_j\le L_j$, $0\le j< k-1$, in these shifted integral coordinates. For a raising step in coordinate $h$, take the compact Pieri component in $V\otimes E$ of type $L+e_h$, with its inherited unitary metric. Contract the factor $E$ with $\omega$. For a lowering step use $V\otimes E^*$ and the evaluation by $\omega$. Each map intertwines the compact actions with the indicated transformation of $\omega$. Its norm is at most $\|\omega\|$. Composing $d$ successive maps at one coordinate gives the two maps in (1), polynomial in the real and imaginary coordinates of $\omega$.

Here is the scalar calculation for $A(e)A(e)^*$ at one step. If $X$ denotes the current top row, the last-coordinate entry of the spectral projector onto the chosen Pieri component is
$$
 w_+(X,M,h)=\frac{\prod_{j<k-1}(M_j-1-X_h)}{\prod_{a\ne h}(X_a-X_h)},\qquad
 w_-(X,M,h)=\frac{\prod_{j<k-1}(M_j-X_h)}{\prod_{a\ne h}(X_a-X_h)}.
$$
Indeed $A(e)^*$ is orthogonal projection after tensoring the input with $e$ or its dual. Use the last-coordinate resolvent of the compact split Casimir. Its denominator is the Capelli polynomial $\prod_a(t+X_a)$, with a common spectral shift suppressed. The last diagonal cofactor is the smaller Capelli polynomial on the $U(k-1)$-type, $\prod_j(t-1+M_j)$ in the defining tensor and $\prod_j(t+M_j)$ in the dual convention. The residue at $t=-X_h$ gives the displayed quotients. Each successive adjoint at $e$ intertwines $U(k-1)$, hence preserves the index $M$ when nonzero. Thus on that space the eigenvalue of the composed $AA^*$ is the product of the successive one-step eigenvalues. [Resolvent and chain computation][cofactor]

**Lower bound.** At the cut the two possible initial distances are
$$
 q_+=M_i-1-L_{i+1},\qquad q_-=L_i-M_i,\qquad q_++q_-=g_*-1.
$$
Choose the sign with the larger distance. At step $a$, $0\le a<d$, the distinguished numerator factor has magnitude at least $q_*-a$. In the raising chain $h=i+1$, $X_h=L_{i+1}+a$ and this is the factor at $j=h-1$. In the lowering chain $h=i$, $X_h=L_i-a$ and this is the factor at $j=h$. Since $q_*\ge d$, these factors stay nonzero and the same $M$ interlaces the successive top rows. All other gaps remain strict.

For completeness set $d_t=\max(1,|X_t-X_h|)$, so $d_h=1$. For $j<h$ the magnitude of each numerator is at least $d_{j+1}$, and for $j\ge h$ it is at least $d_j$. These inequalities follow from $X_{j+1}<M_j\le X_j$ and integrality, with the nonzero adjacent factor provided by the choice above. The distinguished factor had lower bound $d_h=1$ in this count, so we can include its full factor $q_*-a$. The product of the distance bounds times $d_0d_{k-1}$ equals the absolute denominator. Both coordinate moves are inward, hence $d_0,d_{k-1}\le D$. Each quotient is nonnegative as an eigenvalue of $A(e)A(e)^*$. The resulting lower bound at step $a$ is $(q_*-a)/D^2$. Multiplying over $a$ gives $(q_*)_d/D^{2d}$ for at least one chain on every $M$-space. Positivity of both chain operators gives (1) at $e$ after the orthogonal sum over $M$. Compact transitivity on the unit sphere and homogeneity give (1) throughout $E$. [Individual Wigner factors and gap dichotomy][dichotomy]

At a represented positive-Gram point, the source perpendicular vector has $\|\omega_\gamma\|^2=G(\gamma)/T'$. Insert $v=F(\gamma)^*e_a$ into (1) and sum over an orthonormal target basis. This gives the required Hilbert–Schmidt lower comparison from the two shifted readings $F(\gamma)A_\pm(\omega_\gamma)$ once the source's orbital covariance identifies them. On the integration section $\|A_\pm\|^2\le(G/T')^d$ gives the opposite comparison. The powers of $T'$ cancel, and $D^{2d}/(q_*)_d\le(2B)^{2d}/d!$ suffices in the equal-weight step. This computes the compact contraction constants on the original row. Constructing the shifted wave towers and controlling their terminal derivatives and cutoffs remains necessary to deduce the pointwise bound. [Pinning the flag vector and applying both contractions][real]

[statement]: https://github.com/rh-lean-roadmap/rh-lean-roadmap/blob/dc5594a62bb2b94139788df817db693cd939a046/docs/src/book/main.tex#L17330-L17357
[cofactor]: https://github.com/rh-lean-roadmap/rh-lean-roadmap/blob/dc5594a62bb2b94139788df817db693cd939a046/docs/src/book/main.tex#L44610-L44643
[dichotomy]: https://github.com/rh-lean-roadmap/rh-lean-roadmap/blob/dc5594a62bb2b94139788df817db693cd939a046/docs/src/book/main.tex#L44642-L44669
[real]: https://github.com/rh-lean-roadmap/rh-lean-roadmap/blob/dc5594a62bb2b94139788df817db693cd939a046/docs/src/book/main.tex#L45141-L45173
