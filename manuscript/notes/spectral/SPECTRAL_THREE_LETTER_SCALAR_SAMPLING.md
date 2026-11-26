# Sharp scalar sampling with three letters

For distinct binary words in the selected tied family, the arithmetic sampling argument needs a third power of decay in each complex coordinate. It preserves the coefficient one in the principal term and the target relative error $b^{-7}$. This reduces the orders of the signed wave, lift, and cutoff word comparisons one must establish for the original real coefficients. There is also a stronger lower bound on the frequency threshold on the selected row. The lattice and numerical estimates below are unconditional under their stated size assumptions. For the selected compact coefficient the two boundary comparisons below verify the phase and section factor at both terminal and nonterminal levels, for every admitted signed word in the supplied local model. The final section matches the signed forms and arithmetic row measures in Jin’s account and obtains (5) on the common selected family.

## The arithmetic frequencies on a row

Write $n=r+1=m/2$, $f=[F:\mathbb Q]$, $E/F$ for the CM field, $g=g_0g_1$, $\rho=\operatorname{rd}(E)$, and $\mathfrak d$ for the absolute different of $E$. The two words differ at an interior index. For a block with start $i$, length $s$, and $i+s\le n+1$, put $\nu=2r+3-2i-s$. The period is
$$
 L=\{t\in g\mathfrak d^\nu:t-(-1)^s\bar t\in g^2\mathfrak d^\nu\}.
$$
For the source character $e^{2\pi i\sum_\tau 2\Re(\tau(\ell)c_\tau)/g}$, its dual lies in $J=g^{-1}\mathfrak d^{-\nu-1}$, by trace duality applied to $g^2\mathfrak d^\nu\subset L$. Inverse differences at the terminal step lie in $J'=g^{-1}\mathfrak d^{-\nu}$. The scales satisfy $\prod z_\tau/\sqrt{N(J)}\le\Theta^{-f}$ and $\prod z'_\tau/\sqrt{N(J')}\le\Theta^{-f}$. In ordinary embedding coordinates the period covolume is $\prod_\tau j_{is}$, where $j_{is}=\rho^{2\nu}(\rho/2)g^3$. Thus the lattice covolume cancels the section Jacobian exactly. [Period and character][period] · [Threshold definitions][cut] · [Section Jacobian and final period][volume]

**Threshold on the selected family.** Use the fifth-power spacing $\mathcal D\ge(kf\log b)^5$, $N=20n=10m$, $I=(\mathcal D-5)/2$, $4\le m\le f\le k$, $b\ge k^{3/2}$, and $T_u,T_v\ge b^{m/2}$. The ordinary and short-cut bounds at a place are $C\sqrt{k}\,t_\tau$ and $C\sqrt{kN^3/\mathcal D}\,t_\tau$, where $t_\tau^2=T_{\rm crit,\tau}(u)T_{\rm crit,\tau}(v)/(T_uT_v)$. The tied mass and dimension comparison gives $\prod t_\tau\le C_t^f$. The four local entries in the threshold table are bounded, in order, by $Ct_\tau\sqrt{kN^3/\mathcal D}$, $Ct_\tau\sqrt k(CN/I)^2$, $Ct_\tau\sqrt k(CN/I)$, and $C\sqrt{t_\tau}(k/(T_uT_v))^{1/4}$. Taking products at fixed block indices gives
$$
 \Theta\gg\min\!\left\{
 k^2f(\log b)^{5/2},\ b^{m/4}k^{-1/4}
 \right\}.                                                     \tag{1}
$$
Indeed the first term before substitution is $\sqrt{\mathcal D/(kN^3)}$. The other nonterminal lower estimate $I/(\sqrt{k}N)$ exceeds a fixed multiple of it when $\mathcal D\ge10$. The terminal lower estimate is $(T_uT_v/k)^{1/4}$. Its exponent in $k$ is at least $(3m/2-1)/4\ge5/4$. Thus $\Theta\ge k$ for sufficiently large selected ranks, with all cut constants fixed first. This strengthens the book's sufficient $k^{1/16}$ for these rows. Chen obtains the choice $\Theta=k$ with twelfth-power spacing. Here the fifth-power spacing suffices and is used with three insertions. No individual bound on $t_\tau$ is used. [Cut and rank inequalities][cut] · [Critical-product calculation](SPECTRAL_CRITICAL_PRODUCT_ON_ROWS.md) · [Chen's interpolation scales][chen]

## A third power controls all the lattice steps

For a nonzero fractional ideal $A\subset E$, write $D_A=\sqrt{N(A)}$, use one embedding from each conjugate pair, and put $M_z(x)=\prod_\tau\min\{1,(z_\tau/|\tau x|)^3\}$, with the zero-coordinate factor equal to one. For positive $z_\tau$,
$$
 \sum_{0\ne x\in A} M_z(x)
 \le C^f\left(\frac{\prod z_\tau}{D_A}\right)^{5/2}.          \tag{2}
$$
The constant is absolute even when $A$ is fractional and the coordinate scales differ arbitrarily. For distinct points the ideal $(x-y)A^{-1}$ is integral, so $\prod_\tau|\tau(x-y)|\ge D_A$. Take dyadic indices $j_\tau=\max(0,\lceil\log_2(|\tau x|/z_\tau)\rceil)$, $h=\sum j_\tau$, and $R_\tau=2^{j_\tau}z_\tau$. An occupied nonzero shell has $U=\prod R_\tau/D_A\ge1$. Subdivide the circumscribing squares into intervals of length at most $R_\tau/(2U^{1/f})$. Each resulting product of squares contains at most one ideal point, by the difference inequality. There are at most $25^fU^2\le25^fU^{5/2}$ such boxes. Multiplication by the shell weight $2^{3f-3h}$ leaves a factor $2^{-h/2}(\prod z_\tau/D_A)^{5/2}$. Summing the geometric series in all coordinates proves (2) with $C=200/(1-2^{-1/2})$. The borderline exponent two already gives a divergent absolute sum for $E=\mathbb Q(i)$, $A=\mathbb Z[i]$, $z=1$.

On the intermediate square lattices one also has $\sum_{w\in\mathbb Z[i]}\min(1,(t/|w|)^3)\le C(1+t^2)$, with the zero term one. Count the points in the disk of radius $\max(1,t)$, then sum the dyadic annuli outside it. Their areas grow by four and the weights decrease by eight. Tensoring, dividing by $R^{2f}$, and taking $R\to\infty$ with $t_\tau=Rz_\tau/g$ yields the same intermediate volume estimate as in the fifth-power argument. After restoring the section factors it is $C^f(\prod z_\tau)^2/N(J)\le C^f\Theta^{-2f}$. At the last period apply (2), including its zero mode separately. For inverse differences use $2z'$ at the terminal step and the injective map $t'\mapsto t^{-1}-(t')^{-1}$ at fixed $t$. The factor $2^{5f/2}$ affects only the nonzero error. [Boundary summation and intermediate volumes][volume]

## From three signed letters to a leading coefficient of one

Use the normalized local positive Gram kernels of the source, with the arithmetic coset majorants, singleton Fourier identity, and joint boundary kernels for the indicated prefixes. At a wave or lift apply the single-letter leading-coefficient identity in three successive interpolation variables. For degree $d$, choose $d+1$ distinct nodes in each variable, and sum over the $(d+1)^3$ tuples in the product grid. Each conditioned tuple inserts exactly three letters, one from each row of nodes, into each companion word. [Rectangular interpolation formula][grid] The signed extensions use $P(y)$ and $P(y+1)$, respectively. After division by the old word weight each letter costs exactly
$$
 \sqrt{|P(y)P(y+1)|/q_{\boldsymbol w}(y)}.
$$
The evaluation grids are the original separated grids inside the cut. In each variable the ordinary leading-coefficient Lagrange bound is $(28N/I)^d$ for degree $d$, with the original shorter interval for the first degree-zero singleton. Dividing each absolute interpolation weight by the sum of the absolute weights in its own variable gives a product probability measure. Cauchy–Schwarz for arbitrary finite linear combinations of prefixes gives the positive two-by-two block estimate. Its mixed multiplier is a unit phase times $\xi^3$ for the singleton and $(t^{-1}-(t')^{-1})^3$ for the lift. The diagonal blocks have scales $X^3$ and $\Lambda^3$, respectively, times the averaged companion kernels. The one-sided terminal calculation incurs $(|t|z')^2$ per letter on the squared norm, hence $(|t|z')^6$ after three. When the inverse difference is nonzero, one of $|t|,|t'|$ is at most $2/|t^{-1}-(t')^{-1}|$. Taking a square root on this side gives the required third power. The native block-polynomial statements allow a variable number of insertions. This is a human three-letter version of the final argument, which is specialized to five in the source. [Native wave][wave] · [Native lift][lift] · [Variable-length terminal vector interpolation][terminaldegree] · [Positive one-letter weights][terminalweight] · [Terminal Gram comparison][terminal] · [Signs, extension weights, and the squared comparison][weights]

For a singleton the zero Fourier mode is the preceding energy in its own arithmetic section. All changes of words and all applications of (2) are on the nonzero frequencies or on distinct inverse arguments. There are at most $2^f$ choices for the first and $3^f$ for the second. For a longer block of length $s\ge2$, the squared multiplier is at most $C^{fs}\Theta^{-2f(s-1)}$ after applying the intermediate volume estimate $s-1$ times. The arithmetic density factor is one below level $n$ and $e_1\ge1$ at level $n$. Normalize the square root of the energy at level $i$ by the product of square roots of these density factors through $i$. The norm triangle inequality over the last block length now gives, for the supremum $R_i$ over reachable words,
$$
 R_i\le(1+a)R_{i-1}+\sum_{s=2}^i q^{s-1}R_{i-s},
 \qquad a=(C_1\Theta^{-5/2})^f,\qquad q=(C_2/\Theta)^f.
$$
Here the constants absorb the singleton product $(1+3^fe)(1+2^fe)$, $e=(C\Theta^{-5/2})^f$, after taking its square root. The total number of insertions on any branch is at most $6n$, since a singleton uses at most six, a block of length $s\ge2$ uses at most $3(s+1)$, and the lengths sum to at most $n$. Keep the original $N=20n$ in the separation and cut estimates. An insertion is a coefficient operator, whose ordinary differential order can exceed one. [Arithmetic comparison and length recurrence][rec]

For completeness the equality majorant with $R_0=1$ has generating function $(1-qz)/(1-(1+a+q)z+aqz^2)$. Its coefficients are nonnegative by the original recurrence and satisfy $R_i\le(1+a+q)^i$. The resulting squared error is at most $\exp(2n(a+q))-1$. By (1), after a fixed increase of $C_*$, a sufficient condition for this error to be at most $b^{-7}$ is $8n(C_*/k)^f\le b^{-7}$. In particular it suffices that $k\ge C_*^2$ and $f\log k\ge14\log b+2\log(8n)$. In fact the source hypothesis $\mathrm{Cnt.Hyp0}$ gives $C_\ell\log b\le f\log k$, $C_\ell m^2\log b\le k$, and $m^4\le f\le k$. Take $C_\ell\ge20$, allowed before selection (the common cutoff in the book is at least 40). Since $n\le k/2$, $k\ge4$ and $b\ge k^{3/2}$, we have $2\log(8n)\le4\log k\le(8/3)\log b$. Thus $f\log k\ge16\log b+2\log(8n)$, and the same calculation gives the stronger sampling tolerance $b^{-8}$. [Original standing rank inequalities][sizesrc] · [Size conditions and order of thresholds][size] · [Common cutoff][threshold] With the source's level-zero limits equal to $I_N$, this proves the finite-row sampling inequality
$$
 \sum_{\rho\in S}\Big\|\sum_p c_{\rho p}V_p\Big\|^2
 \le (1+b^{-8})e_1 I_N.                                        \tag{3}
$$
The terminal empty word must agree with the represented tensor on each finite tower. Absolute convergence of each row's vector sum passes (3) to the full prefix set. With the original row-mass and measure isometries the right-hand side converts to $(1+b^{-8})e_1\Delta_{u,v}$ for the normalized scalar-partner contribution. The [finite-density calculation](SPECTRAL_SCALAR_DENSITIES.md) gives $e_1\le\exp((5/2)f3^{-(k-m+1)})$ on this host with $k\ge m+f+5$ and the stated split levels. At late rank $k-m+1\ge k/2$, $8\log b\le 8k/(20m^2)\le k/40$, and $\log((5/2)f)\le\log((5/2)k)=o(k)$. Hence $(5/2)f3^{-(k-m+1)}\le b^{-8}$. Because $(1+x)e^x\le1+3x$ for $0\le x\le1/4$, for $b\ge3$ the **full coefficient, including density**, is at most $1+3b^{-8}\le1+b^{-7}$. [Endpoint, row tails, and density][end] · [Mass cancellation][mass]

To apply the calculation to a real coefficient one needs positivity of its normalized prefix forms for the signed histories, the supplied local coefficient model, and the level-zero and terminal coordinate identifications as the cutoffs are removed. The following sections and the final row comparison identify these inputs on the common selected family. Equations (1) and (2) use none of these analytic identifications. The conditional step (3) shows exactly which lengths they must cover and avoids an unspecified multiplicative constant on the zero frequency. [Roadmap realization and limits][real] · [Chen's boundary proof][germ]

## A weak test for the boundary Gram limit

For one real place, a compact cutoff, a block of length $s\ge2$, and a finite prefix history $h$, let $Z$ be a Gram vector for the normalized kernel, with the inner product linear in its second argument. In the notation above the size-one fibre vector and the proposed boundary profile are
$$
 V_{h,x}(c)=j_{i+s-1,1}^{-1/2}
 Z\bigl(h(s-1,x^{-1})(1,c)\bigr),\qquad
 B_h(z)=\phi(z)j_{is}^{-1/2}Z\bigl(h(s,z)\bigr).
$$
Here $h(s,z)$ means appending the indicated block. The source phase $\phi$ has modulus one and is common to the histories. Write $W_{h,x}(D)=|x|^{s-1}V_{h,x}(x^{s-1}D)$, $J(z)=s|z|^{s-1}$, $\chi(z)=\exp(2\pi i\,2\Re z/g)$, and let $|\omega|=1$ account for the orientation of the determinant coordinate. Thus $B_h/J$ is the coefficient in the stationary-phase sum. The singleton integral identity and the preceding block's diagonal bound give $M_h=\sup_{|x|\ge1}\|W_{h,x}\|_2<\infty$, since the dilation preserves the norm. These formulas fix the power-map Jacobian and the embedding character on the selected row. [Original fibre and section normalizations][realgerm]

Define, in the common coefficient Hilbert space,
$$
 (T_x u)(D)=\sum_{z^s=\omega D}\frac{\chi(sxz)}{J(z)}u(z).
$$
To recover the two Gram limits it suffices to verify the following **weak scalar identity** for each history. For smooth finite-rank vector-valued $u$ supported in a compact disk off zero on which $z\mapsto z^s$ is injective, require
$$
 \lim_{|x|\to\infty}\langle W_{h,x},T_xu\rangle
 =\int_{\mathbb C}\langle B_h(z),u(z)\rangle\,d^2z.             \tag{4}
$$
Only local square integrability of the proposed $B_h$ is assumed here. In root coordinates the vector tested weakly on the left is precisely $J(z)\overline{\chi(sxz)}W_{h,x}(\omega^{-1}z^s)$. Consequently (4) can be checked on a scalar component against a smooth test supported on a single root sheet.

**Proof.** The real Jacobian is $J(z)^2$. Cauchy–Schwarz on each fibre and the area formula give $\|T_x\|\le\sqrt{s}$. For fixed $u,v\in L^2$, expanding $\langle T_xu,T_xv\rangle$ gives one term for each $\zeta^s=1$. The term for $\zeta=1$ is $\langle u,v\rangle$. The other integrands have phase $\chi(s(\zeta-1)xz)$ and the integrable amplitude $\langle u(z),v(\zeta z)\rangle$. Riemann–Lebesgue gives $\langle T_xu,T_xv\rangle\to\langle u,v\rangle$. By partitions of unity the test functions in (4) span a dense subspace. The bound $M_h$ and the limiting isometry give $|\int\langle B_h,u\rangle|\le M_h\|u\|_2$ there. By Riesz representation and local uniqueness, $B_h$ belongs to global $L^2$, with $\|B_h\|_2\le M_h$. The uniform bound on $T_x$ extends (4) to every fixed $L^2$ test.

Now put $x'=x+\sigma$ for fixed $\sigma$, and choose $\rho_x^s=(x/x')^{s-1}$ with $\rho_x\to1$. To take a Gram product, return both vectors to the same original $c$ coordinate, then rescale by $x$. The approximant belonging to $h',x'$ becomes exactly $T_x u_x$ with
$$
 u_x(z)=|\rho_x|\chi\bigl(s(\rho_xx'-x)z\bigr)B_{h'}(\rho_x z).
$$
Indeed the change of variable $z'=\rho_xz$ introduces the area-dilation factor $|\rho_x|^s$ while $J(\rho_xz)=|\rho_x|^{s-1}J(z)$, leaving $|\rho_x|$. Since $\rho_xx'=x(1+\sigma/x)^{1/s}$, the phase parameter tends to $\sigma$. Strong continuity of $L^2$ dilation and modulation gives $u_x\to\chi(\sigma z)B_{h'}$ in $L^2$. Apply (4) with this limit and use $\sup_x\|T_x\|\le\sqrt{s}$ for the difference. The pairing of the shorter vector with the shifted approximant therefore tends to
$$
 \int_{\mathbb C}\chi(\sigma z)\langle B_h(z),B_{h'}(z)\rangle\,d^2z
 =j_{is}^{-1}\int_{\mathbb C}\chi(\sigma z)
       \langle Z(h(s,z)),Z(h'(s,z))\rangle\,d^2z .
$$
The pairing of the two approximants has the same limit by the limiting isometry. Interchanging the histories gives the other mixed pairing. The joint matrices are Gram matrices in the common $c$ space. Taking a translation-invariant mean of the Gram kernel of the shorter vectors minus their approximants gives the positive-definite residual required for boundary summation. Indeed its quadratic form on any finite translated family is the mean of a squared norm; subtracting the two mixed limits and adding the approximant limit leaves exactly one copy of the displayed Fourier term to subtract from the mean of the shorter pairing. [Source boundary summation][volume]

Chen's annular $O(|x|^{-1})$ estimate implies (4). On the support of one test, pair the finite root expansion with the demodulating character. The intended sheet gives the prescribed integral, and every other sheet has a nonzero frequency tending to infinity. The error vanishes by Cauchy–Schwarz on compact support. Even convergence of the norm of that local error to zero **in measure** suffices: on each annulus the error is bounded in $L^2$ by the preceding diagonal bound and the local $L^2$ norms of the profiles, so its norm tends to zero in $L^1$ there. The bounded single-sheet tests then give (4). For each original signed word history, the required comparison is to evaluate these scalar pairings with the specified phase, coefficient projection, and section factor. Once this is done, the boundary step requires neither a rate in $x$ nor uniform constants across growing ranks. The earlier positivity, level-zero residue, and terminal identifications used in (3) are separate inputs. [Chen, power-map Gram proof][germ] · [Roadmap, actual compact coefficient and row character][realgerm]

### Verification at the compact terminal level

For the selected place's compact, positive-Gram cut coefficient, (4) holds whenever $i+s=r+2$, $s\ge2$, and the fixed prefix has size $i-1$. This includes the empty signed word. It also holds for every admitted signed word in the supplied terminal projected-coefficient model. Here $\omega=1$ and $\phi=1$ in the arithmetic coordinates of (4). The cut is kept fixed throughout this assertion.

To check the identification, set $a=s-1$, $q=g/(2\pi)$, $\lambda_1=q^s i_0^{s-2}$ and $\lambda_2=q^{s-1}i_0^{s-1}$, where $i_0=\sqrt{-1}$. The split and merged standard-coordinate block arguments are respectively $(\lambda_1/x,x^a D)$ and $\lambda_2z$. The change is independent of the preceding valid prefix. Chen's terminal matrix integral applies to the actual compact operator coefficient: the positive Gram cut makes the frame span nondegenerate, the common perpendicular has compact unitary stabilizer, and integration in the two frame fixers gives a smooth matrix test supported where its determinant is bounded away from zero. At fixed prefix, block elimination bounds the remaining integration variables and every fixed derivative on each determinant annulus. The same matrix test occurs in both entries. Its orbital expansion uses $\psi_\beta(w)=e^{i\Re(\beta w)}$ with self-dual measure $|\beta|\,d^2w/(2\pi)$. In the source Witt coordinates $\beta=2i_0$. Since $\lambda_2^s=(-1)^a\lambda_1^a$, the roots of the standard determinant equation are precisely $\lambda_2z$ with $z^s=D$. Since $\lambda_2/\lambda_1=2\pi i_0/g$, the standard phase is $\psi_{2i_0}((\lambda_2/\lambda_1)szx)=\overline{\chi(szx)}$. The concrete coefficient array has this conjugate phase. Its terminal Gram form puts the second point in the first inner-product slot, hence the abstract Gram vectors used in (4) have phase $\chi(szx)$. [Chen, compact prefix][prefix] · [Oriented terminal matrix fibre][fibre] · [Native real-place comparison][phase]

The two section weights can also be compared before taking the limit. Write $\kappa=2\pi/(g\rho)$ and $b_\ell=\prod_{d=1}^{\ell-1}(\kappa^{1-2d}/\pi)^{\ell-d}$. Then $b_s/b_a=\kappa^{-a^2}\pi^{-a}$ and $\sqrt{j_{is}/j_{r+1,1}}=\rho^a$. The split orbital integral has $a$ more complex integration variables than the merged one. Their self-dual measure factor is $\pi^{-a}$. After substituting the point weight $\sqrt{n}/b$, on both sides the resulting common multiplier is $K_h|D|^{k-1}$ for a single prefix constant $K_h$. More explicitly, after removing this common factor the split coefficient multiplying its standard integral is $|\lambda_1/x|^{a^2}\rho_N$, and at a root the merged coefficient multiplying its integral is $|\lambda_2z|^{a^2}/s$. Here $N$ is the signed word length and, on the nonzero split support,
$$
 \rho_N=\left(1-\frac{T_uT_v}{|x^aD|^2}\right)^{(k-1-N)/2}
        =1+O_{K,k,N,T_u,T_v}(|x|^{-2a})
$$
on any fixed compact annulus $K$ at large $|x|$. The exponent follows from the Gram weight $(|x^aD|^2-T_uT_v)^{(k-1)/2}$ and the signed-word factor $(|x^aD|^2/(|x^aD|^2-T_uT_v))^{N/2}$. The common-prefix cancellation uses $\kappa\rho q=1$ and $|D|=|z|^s$. These are the two identities of the source's section comparison, including the division by $s|z|^a\sqrt{j_{is}}$ on the merged side. [Point weight and section comparison][sectionmatch] · [Normalized orbital identity][orbitid]

Chen's stationary-phase formula gives an annular error $O_K(|x|^{-1})$ after these substitutions. The normalized split integral is bounded there, so the factor $\rho_N$ costs only $O_K(|x|^{-2a})$. For an admitted signed word, the terminal form is a finite sum of Gram forms of vectors $L_\alpha V(F_\alpha)$, with coefficients $c_\alpha\ge0$, compact positive-Gram tests $F_\alpha$, and fixed bounded projections $L_\alpha$. The error norm in the abstract Gram space is bounded by $|x|^{-1}\sum_\alpha\sqrt{c_\alpha}\|L_\alpha\|C_{\alpha,K}$, by expanding its squared norm in that finite Gram representation. This proves (4) for the compact terminal histories with the section and character stated above. The residual group calculation below uses a different continuity bound. [Unscaled matrix expansion][matrix] · [Terminal Gram decomposition][termgram] · [Application on the actual cut sequence][termcut]

### Verification with a residual group variable

At fixed cutoffs the same weak test holds on the supplied nonterminal coefficient model for $j=i+s-1\le r$, $s\ge2$, and every admitted signed word $w$. There is now a residual group variable $\gamma$. On a compact annulus of the standardized determinant, the block inverse formulas place $\gamma$, the two outer unipotent variables, and all prefix integration variables in a common compact set. The simple-root character splits with its adjacent corner entry. Fubini gives the two orbital integrals of the same residual-group-valued matrix test. Differentiation under the integral is valid at every fixed residual derivative order. Thus the stationary-phase estimate also applies in a norm controlling finitely many such derivatives. [Chen's residual-coordinate bounds][prefix] · [Factorization of the actual character][fibre]

For the positive form, use the source's finite-derivative Banach space $V$ of arrays of residual coefficients with all binary components of $w$. The form on $V$ agrees with the original word pairing on both sliced arrays. Its continuity estimate is
$$
  \operatorname{Re} B_w(u,u)\le C_p^2\|u\|_V^2 .
$$
Specifically, at a fixed sufficiently large decay exponent the word operator costs at most $(2(r-j)+k+1)|w|$ derivatives, followed by the five derivatives in the last continuous pairing. The finite sum over the binary indices gives the two-input bound $C_f c_u c_v$ in the weighted derivative norms. The coefficient model controls both by its Banach norm, so one may take $C_p=\sqrt{C_f}$. The cutoff slice identity represents the original word pairing by $B_w$ applied to the split and merged orbital values of this one $V$-valued test. It supplies a bound $C_{\rm st}|t|$ in $V$ for the standardized germ difference, including the determinant factors from the residual dimension. [Word operator and pairing bound][wordform] · [Identification on the coefficient space][vform] · [Compact slice and germ in that norm][germspace]

For the exact arithmetic scale, put $a=s-1$ and $\lambda_{\ell,d}=(g/(2\pi))^{\nu_{\ell d}} i_0^{d-1}$. The standardized arguments are $t=\lambda_{i,a}/x$, $c=\lambda_{j,1}x^aD$, and $\lambda_{i,s}z$. The identity $\lambda_{i,s}^{s}=(-1)^a\lambda_{j,1}\lambda_{i,a}^a$ gives $z^s=D$, and $\lambda_{i,s}/\lambda_{i,a}=2\pi i_0/g$ gives the same conjugate phase as at the terminal level. The point multiplier in the concrete form at $P$ is $\sqrt{n_j(P)}/(b(P)\sqrt{\Gamma_j^{\rm lev}n_\tau(w)})$. Substituting it on both paths in the finite root sum gives one common scalar $\mu_h$, independent of $x,D,z$. The section factors in that sum are exactly $|x|^a/\sqrt{j_{j,1}}$ on the split side and $1/(s|z|^a\sqrt{j_{is}})$ on the merged side. The common scalar occurs on the entire standardized difference. By the form bound, the norm of the arithmetic Gram-vector difference in (4) is therefore at most
$$
 C_p|\mu_h|\,C_{\rm st}|\lambda_{i,a}|\,|x|^{-1}.
$$
The signed companion word, prefix, compact annulus and both cutoffs are fixed here. An invalid prefix has zero Gram diagonal and gives zero throughout. This proves the annular comparison at every compact level of the supplied slice model. The limit to the untruncated coefficient and the level-zero residue used in (3) are treated in the companion calculation cited below. [Common scalar and word weight][lowerconst] · [Arithmetic difference and its norm][lowernorm]

## The signed scalar sum on the matched row

Fix an admitted selected Bessel family in the common arithmetic and real models above, with its two distinct words, original translated two-period coefficients, split levels, compact type projections, neat marked lattices and compatible Haar measures. Assume the standing rank and tie hypotheses of (1), the primitive density formula for this host, and the source's absolute orbital convergence. Write $\Sigma_{\rm sc,gen}(u,v)$ for the signed generic scalar-partner contribution before the common split index $\Gamma_1$. The preceding comparison on these data now gives
$$
             \Gamma_1\Sigma_{\rm sc,gen}(u,v)
              \le (1+b^{-7})\,\frac{d_ud_v}{D^\star}.           \tag{5}
$$

The signed residual form of an inserted word has triangular factorization $F_w^*D_wF_w$ with positive diagonal. For a negative insertion the shift is by one in the transposed auxiliary factor. Separation of the old nodes from these shifted arguments preserves the signs of both new pivots. Integration of the squared norm of $D_w^{1/2}F_wX$ proves positivity on arbitrary finite linear combinations of genuine compact slices. The terminal expression is the finite positive sum of the projected differentiated coefficient Grams used above. The alternating wave and reciprocal-label contractions use Cauchy–Schwarz in these very forms: each letter costs $\sqrt{|P(y)P(y+1)|/q_w(y)}$. Consequently the probabilities and three-variable estimates in (3) apply to the family’s own signed histories. The [level-zero and cutoff comparison](SPECTRAL_LEVEL_ZERO_AND_CUTOFFS.md) identifies their common starting energy and takes the two limits in order. [Jin, signed residual and terminal forms][jinsigned] · [Wave and reciprocal-label contractions][jinwave]

At a terminal block point the arithmetic and model orbital operators are related by $U_v(p)=E_v\,b_\kappa(p)^{-1}J_v^{\rm mod}(p)(E'_v)^{-1}$ in the pinned frames, with $E_v,E'_v$ independent of $p$. Indeed the root of height $d$ contributes $(\kappa^{1-2d}/\pi)\,d^2x$ to its section Haar. The point-dependent rotations are absorbed in the separately pinned arithmetic operators. The common identifications thus preserve cross inner products between different points of a class. On each occupied tuple the partner count gives the same rank-one arithmetic kernel multiplied by its represented density ratio, bounded by $e_1$. Taking the sum over occupied tuples bounds the coefficient Gram matrix, also for any finite subset of classes. Thus (3) applies to the exact class vectors. After exhaustion, the marked row weights and the factors from the two definite stabilizers give the [full column mass](SPECTRAL_SCALAR_ROW_MASS.md), with principal scale $d_ud_v/D^\star$. This gives $(1+b^{-8})e_1$ times that scale, and the density estimate above proves (5). The statement concerns this contribution on each family having the specified common data. The other pair classes, operator estimates and existence of families meeting all simultaneous requirements enter the global spectral obligation separately. [Actual terminal quotients][jinquot] · [Finite partner count and domination][jinpartner] · [Unfolding the class sum][jinunfold] · [Full column dimensions][jinmass]

[period]: https://github.com/rh-lean-roadmap/rh-lean-roadmap/blob/c535d69c2d028dd05547e05c4b0efde1225ce454/docs/src/book/main.tex#L46165-L46170
[cut]: https://github.com/rh-lean-roadmap/rh-lean-roadmap/blob/c535d69c2d028dd05547e05c4b0efde1225ce454/docs/src/book/main.tex#L46218-L46267
[volume]: https://github.com/rh-lean-roadmap/rh-lean-roadmap/blob/c535d69c2d028dd05547e05c4b0efde1225ce454/docs/src/book/main.tex#L46487-L46521
[chen]: https://github.com/yyyyychen/RH-Natural-Language-Proof/blob/d4dfb1a282dbf857288e73eb1f546dbfcc5899b8/tex/row-frequency-sizes.tex#L26-L195
[wave]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Formalism/HermitianCurvature/HermitianCurvatureProofs/BlockKWaveC.lean#L20-L176
[lift]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Formalism/HermitianCurvature/HermitianCurvatureProofs/LiftLocalPositiveCompactSupport.lean#L21-L183
[terminal]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Formalism/HermitianCurvature/HermitianCurvatureProofs/TopLocalBuiltPlaces.lean#L12-L154
[weights]: https://github.com/rh-lean-roadmap/rh-lean-roadmap/blob/c535d69c2d028dd05547e05c4b0efde1225ce454/docs/src/book/main.tex#L46389-L46437
[rec]: https://github.com/rh-lean-roadmap/rh-lean-roadmap/blob/c535d69c2d028dd05547e05c4b0efde1225ce454/docs/src/book/main.tex#L46534-L46565
[end]: https://github.com/rh-lean-roadmap/rh-lean-roadmap/blob/c535d69c2d028dd05547e05c4b0efde1225ce454/docs/src/book/main.tex#L46566-L46611
[mass]: https://github.com/rh-lean-roadmap/rh-lean-roadmap/blob/c535d69c2d028dd05547e05c4b0efde1225ce454/docs/src/book/main.tex#L46612-L46633
[real]: https://github.com/rh-lean-roadmap/rh-lean-roadmap/blob/c535d69c2d028dd05547e05c4b0efde1225ce454/docs/src/book/main.tex#L46269-L46305
[germ]: https://github.com/yyyyychen/RH-Natural-Language-Proof/blob/d4dfb1a282dbf857288e73eb1f546dbfcc5899b8/tex/orbital-germ.tex#L625-L758

[size]: https://github.com/rh-lean-roadmap/rh-lean-roadmap/blob/c535d69c2d028dd05547e05c4b0efde1225ce454/docs/src/book/main.tex#L15528-L15550
[threshold]: https://github.com/rh-lean-roadmap/rh-lean-roadmap/blob/c535d69c2d028dd05547e05c4b0efde1225ce454/docs/src/book/main.tex#L44536-L44540
[grid]: https://github.com/rh-lean-roadmap/rh-lean-roadmap/blob/c535d69c2d028dd05547e05c4b0efde1225ce454/docs/src/book/main.tex#L17447-L17473

[sizesrc]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Formalism/SharpRestriction/CuspSpanNormBounds/StandingNumericalData.lean#L106-L135
[terminaldegree]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Formalism/HermitianCurvature/HermitianCurvatureProofs/SecondDefectNonneg.lean#L146-L160
[terminalweight]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Formalism/HermitianCurvature/HermitianCurvatureProofs/SecondDefectPlusWordLe.lean#L48-L60

[realgerm]: https://github.com/rh-lean-roadmap/rh-lean-roadmap/blob/c535d69c2d028dd05547e05c4b0efde1225ce454/docs/src/book/main.tex#L46439-L46485

[prefix]: https://github.com/yyyyychen/RH-Natural-Language-Proof/blob/d4dfb1a282dbf857288e73eb1f546dbfcc5899b8/tex/orbital-germ.tex#L270-L309
[fibre]: https://github.com/yyyyychen/RH-Natural-Language-Proof/blob/d4dfb1a282dbf857288e73eb1f546dbfcc5899b8/tex/orbital-germ.tex#L405-L620
[phase]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Formalism/HermitianCurvature/HermitianCurvatureProofs/TopCore.lean#L60-L116
[sectionmatch]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Formalism/HermitianCurvature/HermitianCurvatureProofs/WeightProductGermIndep.lean#L158-L293
[orbitid]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Formalism/HermitianCurvature/HermitianCurvatureProofs/TopCore.lean#L124-L189
[matrix]: https://github.com/yyyyychen/RH-Natural-Language-Proof/blob/d4dfb1a282dbf857288e73eb1f546dbfcc5899b8/tex/orbital-germ.tex#L8-L40
[termgram]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Formalism/HermitianCurvature/HermitianCurvatureProofs/VecVNonloc.lean#L36-L78
[termcut]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Formalism/HermitianCurvature/HermitianCurvatureProofs/GermRateTopBound.lean#L45-L92

[wordform]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Formalism/HermitianCurvature/HermitianCurvatureProofs/PositiveDensityModerateGrowth.lean#L376-L405

[vform]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Formalism/HermitianCurvature/HermitianCurvatureProofs/BetaCongrRight.lean#L115-L170

[germspace]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Formalism/HermitianCurvature/HermitianCurvatureProofs/SliceAtApply.lean#L110-L185

[lowerconst]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Formalism/HermitianCurvature/HermitianCurvatureProofs/GermConstant.lean#L245-L341

[lowernorm]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Formalism/HermitianCurvature/HermitianCurvatureProofs/PbGermRateLowBOfParts.lean#L433-L478

[jinsigned]: https://github.com/yuiyuiui/Natural-Language-Proof-Generalized-Riemann-Hypothesis/blob/405237610e58ab9d4a9d5d54d9a0548a0c44227c/sections/g-real-restriction.tex#L7378-L7485

[jinwave]: https://github.com/yuiyuiui/Natural-Language-Proof-Generalized-Riemann-Hypothesis/blob/405237610e58ab9d4a9d5d54d9a0548a0c44227c/sections/g-real-restriction.tex#L8478-L8519

[jinquot]: https://github.com/yuiyuiui/Natural-Language-Proof-Generalized-Riemann-Hypothesis/blob/405237610e58ab9d4a9d5d54d9a0548a0c44227c/sections/g-real-restriction.tex#L5014-L5079

[jinpartner]: https://github.com/yuiyuiui/Natural-Language-Proof-Generalized-Riemann-Hypothesis/blob/405237610e58ab9d4a9d5d54d9a0548a0c44227c/sections/g-real-restriction.tex#L4479-L4539

[jinunfold]: https://github.com/yuiyuiui/Natural-Language-Proof-Generalized-Riemann-Hypothesis/blob/405237610e58ab9d4a9d5d54d9a0548a0c44227c/sections/g-real-restriction.tex#L5240-L5309

[jinmass]: https://github.com/yuiyuiui/Natural-Language-Proof-Generalized-Riemann-Hypothesis/blob/405237610e58ab9d4a9d5d54d9a0548a0c44227c/sections/g-real-restriction.tex#L5430-L5467
