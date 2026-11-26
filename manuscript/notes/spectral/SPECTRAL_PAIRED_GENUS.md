# Two congruence data and their relative isometry in the definite genus

The arithmetic part of a fixed-label zero-Gram pair uses two counts. The [single-frame fibre](SPECTRAL_FRAME_FIBRE.md) counts flags over a prescribed embedded datum. Here we average the number of **pairs of such data together with an isometry respecting both congruence graphs**. We recover Roadmap B8.02b-mass from the definite Hermitian mass formula and lattice counts. At the actual level a compatible isometry is unique once the two data are fixed. This removes the finite-subgroup factorial from the estimate. At the smallest possible pair of indices the normalized mean is exactly one. [Roadmap statement][goal] · [Native genus and orbit-sum normalization][native]

## Statement on the actual row

Let $E/F$ be CM and unramified at every finite place, $O=\mathcal O_E$, $f=[F:\mathbb Q]$, $\rho=|\operatorname{disc}E|^{1/(2f)}=2v_E\ge2$. Let $V$ be the totally positive definite rank-$k$ row space, $k\ge3$, and $L_0$ its full integral lattice. For an integral lattice $N$ let $d(N)=|N^\#/N|$, taking the Hermitian dual in its span, and set $d(0)=1$. The row has $L_0^\#/L_0\simeq O/(T)$ for the rational prime $T=T_u$ split completely in $E$. Indeed the primitive last-vector line of norm $-T$ and its perpendicular in the self-dual isotropic reduction have isomorphic discriminant modules by unimodular gluing. Set $D=T^{2f}$, the common discriminant order on this genus. [Actual row-to-genus specialization][row] · [Primitive line and its complement](SPECTRAL_FRAME_FIBRE.md#the-normal-form-and-what-the-index-measures)

For each $L$ in the genus fix the rational integer level $g=g_0g_1$. An embedded datum is a full integral lattice $K\subset V$ with $d(K)=D$ and the inverse-image graph $\Gamma\subset K\oplus L$ of an isometry $\phi:K/gK\to L/gL$. Its diagonal lattice is $C=\{z:(z,z)\in\Gamma\}$. Require $[L:C]=x$ and at most $r$ generators for $L/C$ as an $O$-module. A second datum $(K',\Gamma')$ has index $x'$ and the same generator bound. Count the ordered triples with an $E$-linear isometry $\eta$ taking $K'$ to $K$ and carrying $\Gamma'$ to $\Gamma$ on their first factors. Define the normalized mean and parameters by
$$
 \mathcal T(x,x')=\frac1{m_0}\sum_{[L]\in\operatorname{gen}(L_0)}
       \frac{\#\{(K,\Gamma;K',\Gamma';\eta)\text{ over }L\}}
            {|\operatorname{Aut}L|},\qquad
 m_0=\sum_{[L]}|\operatorname{Aut}L|^{-1},
$$
$$
 \ell=\log_2(2f),\quad c=1+\ell,\quad
 M_*=(20 f\rho^2)^{2f(6+c)},\quad X=xx',\quad Y=XD^2,\quad
 A_s=(2/g)^{2sf}DX.
$$
Both graph indices are positive integers. The triple count over a fixed $L$ uses actual embedded data, before taking any quotient by its automorphisms. The displayed genus weights account for that action. [Definition of the graphs and triples][data] · [Native graph kernels][native-graph] · [Native ordered triples][native-trip]

The following bound holds for **every** integer $g\ge2$. Put $e_g=1$ for $g\ge3$ and $e_2=2$. On the original spectral row $e_g=1$. With $Z=X^{k/2}Y^{6r+10+4c}$,
$$
 \frac{\mathcal T(x,x')}{Z}\ \le \mathbf1_{x=x'}+ M_*\rho^f
 \sum_{\substack{1\le s<k\\ A_s\ge1}}
        \left(e_g(32/g)^{kf}Y^6\right)^s
 +\mathbf1_{A_k\ge1}\left(e_g(2/g)^{kf}\sqrt D\,X\right)^k .       \tag{1}
$$
The exact value at $x=x'=1$ and $g\ge3$ is $\mathcal T(1,1)=1$. Since $Y,D\ge1$ and $e_g\le(4kf)^{4f}$, (1) implies the source's bound
$$
 \mathcal T(x,x')\le Z\left[
 1+M_*\rho^f\sum_{s=1}^{k-1}
 \left((32/g)^{kf}(4kf)^{4f}Y^7\right)^s+
 \left((2/g)^{kf}(4kf)^{4f}DX\right)^k
 \right].                                                        \tag{2}
$$

## What the congruence implies about its fixed space

Fix $L$ and a triple. Let $U=\ker(1-\eta)$, $s=\operatorname{codim}_E U$, and $p$ be orthogonal projection onto $U$. Since $\eta$ fixes $U$ pointwise and preserves $U^\perp$, the two diagonal lattices satisfy $C\cap U=C'\cap U=P$. Put $a=d(L\cap U)$ and $y=[L\cap U:P]$. Then $y\mid\gcd(x,x')$ and $d(P)=ay^2$. Pairing the graph elements $(\eta z,z)$ and $(w,w)$ for $z\in C'$, $w\in C$, gives
$$
                (1-\eta)C'/g\subset C^\# .
$$
The determinant of $1-\eta$ on $U^\perp$ is nonzero. Use the map $S$ that is the identity on $U$ and equals $(1-\eta)/g$ on $U^\perp$. The lattice $B=P\oplus(1-p)C'$ has the same additive covolume as $C'$, by the projection sequence with kernel $P$. We have $SB\subset C^\#$ and $p(SB)=P$. Restricting integral functionals on $C$ to $P$ is surjective, since $C/P$ is torsion-free and projective. Thus $p(C^\#)=P^\#$. Projection followed by comparison of additive covolumes now gives
$$
 ay^2\le[C^\#:SB]=|N_{E/\mathbb Q}\det S|\,[C^\#:C']
             \le (2/g)^{2sf}Dx x'= A_s.                       \tag{3}
$$
Indeed $C'\subset L\subset C^\#$, with $[C^\#:L^\#]=x$ by duality. At every embedding the eigenvalues of $\eta$ on $U^\perp$ have modulus one by definiteness, hence $|\det(1-\eta)|\le2^s$. In particular $A_s<1$ excludes the entire codimension. [Native projected determinant inequality][det]

For prescribed data the graph relation determines the reduction of the isometry, namely $\bar\eta=\phi^{-1}\phi'$. Fix one solution $\eta_0$ in the same fixed-space fibre. Every other solution maps injectively via $\eta\mapsto\eta_0^{-1}\eta$ into the finite group of automorphisms of $K'$ acting trivially on $K'/gK'$ and fixing $U$ pointwise. Finiteness follows from definiteness and discreteness of the lattice. At level $g\ge3$ this kernel is trivial. Here is the integral argument. In a $\mathbb Z$-basis of the underlying additive lattice, an element of prime-order torsion in the kernel is $1+p^a B$ at an odd prime $p\mid g$, or at $p=2$ with $a\ge2$ when $4\mid g$, with some entry of $B$ a unit. Every $g\ge3$ satisfies one of these two conditions. Taking a power prime to $p$ preserves the exact valuation $a$ of the displacement. Raising to the $p$-th power increases that valuation by exactly one, by binomial expansion under these conditions. Thus no nonidentity element has finite order. If $g=2$, the square of an element congruent to the identity is the identity modulo four, hence equals the identity. The kernel has exponent two and is abelian. Its elements are commuting $E$-linear involutions and diagonalize simultaneously on $U^\perp$, where the action is faithful. Its order is at most $2^s$. This proves the factor $e_g^s$ in all cases; no estimate for general finite rational linear groups is needed.

For fixed $P$ and $s>0$, count $C$ by projecting to $V/U$. Its image has index $x/y$ in the image of $L$, a rank-$s$ projective lattice. A rank-$h$ projective lattice has at most $u^{h+\ell}$ sublattices of additive index $u$. To see this, the Fitting ideal of the quotient has norm $u$. Above a rational prime its possibilities are bounded coefficientwise by $(1-z)^{-2f}$, as each prime of residue degree $d_v$ contributes $(1-z^{d_v})^{-1}$. Thus the ideal count is at most $(2f)^{\Omega(u)}\le u^\ell$. For a fixed ideal, order its primes; a chain of successive residual hyperplanes reaches every such quotient in that order. Each prime factor of norm $q$ gives at most $q^h$ hyperplanes, proving the count. For a fixed projected lattice the lifts to $L/P$ are sections differing by a homomorphism into $(L\cap U)/P$ of order $y$. This gives at most $y^s$ lifts by local freeness. The number of possibilities for both $C,C'$ above the common $P$ is consequently at most $X^{s+\ell}y^{-2\ell}$. The possible $P$ of index $y$ in $L\cap U$ number at most $y^{k-s+\ell}$. [Projective lattice count](SPECTRAL_FRAME_FIBRE.md#counting-and-the-genus-normalization) · [Original fixed-space fibre][fibre]

Once $C$ is fixed, $C\subset K\subset C^\#$. The successive quotients in $C\subset L\subset L^\#\subset C^\#$ require at most $r,1,r$ generators, the last by finite-module duality. Every submodule of a finite $O$-module generated by $h$ elements is generated by at most $h$ elements, by elementary divisors locally and the Chinese remainder theorem. With $h=2r+1$, there are at most $(Dx^2)^h$ choices for $K/C\subset C^\#/C$. For at most $h$ generators $z$ of $K/C$, pair $(z,w)\in\Gamma$ with every $(v,v)$, $v\in C$. Then $(z-w)/g\in C^\#$. Its class modulo $L$ determines $w\bmod gL$, giving at most $[C^\#:L]=Dx$ choices per generator. The graph is already prescribed on $C$. The two lattices and graphs, once $C,C'$ are fixed, therefore give at most $(D^4X^3)^h$ possibilities.

Combining these facts gives the explicit fibre bound for $0<s<k$,
$$
 \#\{\text{triples with fixed space }U\}
 \le e_g^s(D^4X^3)^h X^{s+\ell}
       \sum_{\substack{y\mid\gcd(x,x')\\ay^2\le A_s}}
                 y^{k-s-\ell}.                                  \tag{4}
$$
For the mean below we can replace the sum by $X(A_s/a)^{k/2}$ on a nonempty fibre. In particular the index shared by the two graphs is counted once. If $x,x'$ are coprime only $y=1$ can occur.

## The primitive intersection average from the Hermitian mass formula

Let $M_h$ denote the mass of the standard positive definite unimodular genus of rank $h$. We use Gan, Hanke and Yu's **unitary** maximal-lattice formula. In a fixed rank-$h$ definite Hermitian space the mass of its maximal integral genus, divided by $M_h$, is
$$
              \prod_{v\text{ inert, odd determinant valuation}}
                    \frac{q_v^h-(-1)^h}{q_v+1}.                 \tag{5}
$$
Here $q_v$ is the residue field order in $F$. The unramified local models have discriminant order $q_v^2$ at each of these exceptional places and one elsewhere. In the odd-valuation case there is one elementary divisor of valuation one, in addition to a self-dual part. All maximal lattices are locally conjugate. The local condition in that paper is integrality of $h(x,x)$ at every vector. Testing $h(x+\alpha y,x+\alpha y)$ for every local integer $\alpha$ gives pairing integrality because the relative different is trivial. This also checks the convention at residual characteristic two. The fixed-rank global factors cancel in (5). [Gan–Hanke–Yu, §3, Tables 1–2 and Propositions 4.4–4.5][ghy]

If $b$ is the discriminant order of a maximal integral lattice $J$, (5) bounds its genus mass by $M_h b^{h/2}$. Enlarge any integral lattice $N$ of discriminant order $u$ into a maximal $J$, necessarily inside $N^\#$. Then $u=b[J:N]^2$. Count all inclusions with their inverse stabilizer weights. Over $N$ their total is at least $1/|\operatorname{Aut}N|$; over each $J$ it is bounded by the sublattice count at the fixed index, divided by $|\operatorname{Aut}J|$. This follows from $\sum_{[z]}1/|\operatorname{Stab}z|=|S|/|G|$ for a finite $G$-set $S$. In a fixed rational space all maximal lattices have the same $b$, so the index $i=[J:N]$ is fixed by $u$. The sublattice bound $i^{h+\ell}$ and (5) give $M_h b^{h/2} i^{h+\ell}\le M_h u^{(h+\ell)/2}$. Thus for rank $h\ge1$ in this space,
$$
        \sum_{[N]:d(N)=u}\frac1{|\operatorname{Aut}N|}
                \le M_h u^{(h+\ell)/2}.                          \tag{6}
$$

Fix $1\le s<k$, $j=k-s$. For a subspace $U$ of rank $j$ let $P_1=L\cap U$, $P_2=L\cap U^\perp$, and suppose $d(P_1)=a$. Possible rational isometry classes for $U$ number at most $a^{1+\ell}$. Indeed the inert places of odd determinant valuation determine its finite determinant classes. The corresponding product of primes of $E$ has norm equal to the maximal discriminant order of $U$, at most $a$ by enlargement. Sum the preceding ideal count up to $a$. At split places there is only one rational form of given rank. All signatures are positive. Landherr's local-global classification then determines $U$, and the determinant and signatures of the complement determine its isometry class as well. Taking the orthogonal sum identifies the embedded subspaces. [Gross, §3, Theorem 3.1, including the local determinant classes][gross]

Put $b=d(P_2)$, $H=L/(P_1\oplus P_2)$. Projection embeds $H$ in each discriminant module. Taking determinants gives $ab=D|H|^2$ and hence $b\le aD$. The module $P_2^\#/P_2$ needs at most $s$ generators, so its submodule $H$ does too. Restriction of functionals gives $p(L^\#)=P_1^\#$. In $P_1^\#/P_1$, the image $p(L)/P_1$ is isomorphic to $H$, and the quotient by that image is a quotient of the cyclic $L^\#/L$. Thus the two discriminant modules together require at most $2s+1$ generators. For fixed $P_1,P_2$ the possible lattices are determined by their gluing submodules in the direct sum, giving at most $(ab)^{2s+1}$ choices. This bound counts all compatible integral gluings even when extra genus restrictions discard most of them.

Write $N_{j,a}(L)=\#\{U:\dim U=j,d(L\cap U)=a\}$. Apply orbit–stabilizer first over $L$ and then over the two lattices with the rational space $U$ fixed. The latter weighting divides the number of admissible gluings by $|\operatorname{Aut}P_1||\operatorname{Aut}P_2|$. Using (6) on each side and summing over $1\le b\le aD$ gives
$$
 \sum_{[L]\in\operatorname{gen}(L_0)}
      \frac{N_{j,a}(L)}{|\operatorname{Aut}L|}
 \le M_j M_s\, a^{j/2}(aD)^{(9s+8+4\ell)/2}.                   \tag{7}
$$
For the exponents, put $B=aD$. The bound before collecting is $a^{1+\ell} M_j a^{(j+\ell)/2}\, B M_s B^{(s+\ell)/2}(aB)^{2s+1}$. Retain $a^{j/2}$ and bound every other occurrence of $a$ by $B$. [Primitive intersections and their stabilizers][primitive]

The level genus mass can be evaluated exactly. Choose one prime from each conjugate pair above $T$. For any $L$ in its genus add to $L$ the chosen components of $L^\#/L$. The discriminant pairing pairs the opposite components perfectly, so this gives a unique self-dual enlargement for this orientation. Conversely in such a $J$ choose one residual hyperplane in $J/\mathfrak pJ$ for each selected prime, keeping the opposite factors fixed, and take the inverse images. Every resulting lattice belongs to the original genus: at the selected places the split stabilizer acts by the full general linear group on the chosen component and transitively on the hyperplanes. Elsewhere take the corresponding self-dual components. Their local isometry classes are the standard ones by finite unramifiedness. The mass of the self-dual genus is therefore $M_k$ by (5). There are $f$ choices of hyperplane to make, each in a vector space of rank $k$ over $\mathbb F_T$. Counting these pairs by orbit–stabilizer gives
$$
             m_0=M_k\left(\frac{T^k-1}{T-1}\right)^f
                 \ge M_k D^{(k-1)/2}.                            \tag{8}
$$
Each conjugate pair contributes exactly one residual hyperplane factor. [Split-level mass and normalization][splitmass]

For completeness, the standard masses satisfy
$$
                \frac{M_s M_{k-s}}{M_k}\le M_*\rho^f16^{skf}.     \tag{9}
$$
Here are the constants. For $i\ge3$ the adjacent quotient $R_i=M_i/M_{i-1}$ from the standard case of Gan–Hanke–Yu and the functional equation is
$$
 R_i=\rho^{-f/2}\big((i-1)!(v_E/\pi)^i\big)^f
                   L_F(i,\eta_{E/F}^i).
$$
Here $\eta=\eta_{E/F}$ is the quadratic character, and $L_F(i,\eta^i)=\prod_{v<\infty}(1-\eta_v^i q_v^{-i})^{-1}$ with $\eta_v=1$ at split places and $-1$ at inert places. In particular even $i$ gives $\zeta_F(i)$. To see the power of $\rho$, the adjacent mass quotient from the standard-lattice formula is $2^{-f}|L_F(1-i,\eta^i)|$. The completed $L$-function has discriminant factor $|\operatorname{disc}F|^{s/2}$ since the finite conductor is trivial. At each real place its gamma factor is $\Gamma_{\mathbb R}(s+\epsilon)$ with $\epsilon=i\bmod 2$ and $\Gamma_{\mathbb R}(z)=\pi^{-z/2}\Gamma(z/2)$. The absolute gamma quotient at $i$ and $1-i$ is $2(i-1)!/(2\pi)^i$. The functional equation now gives the displayed $R_i$ using $|\operatorname{disc}F|=\rho^f$ and $v_E=\rho/2$. [Gan–Hanke–Yu, (4.2)–(4.3) and Proposition 4.4][ghy] · [Roadmap B8.48][adj]

The Euler product and its inverse are bounded by $\zeta_F(i)\le2^f$. Hence, with $B_0=16^f$, $R_i^{-1}\le\rho^{f/2}B_0^i$ and $R_i/R_{i+t}\le B_0^t$ for $t\ge1$. The constants follow from $v_E\ge1$, factorial monotonicity and $4\pi<16$.

For $h=1,2$, on a self-dual genus lattice use squared Euclidean norm $\operatorname{Tr}_{E/\mathbb Q}h_V(z,z)$. Its trace dual is $\mathfrak D_E^{-1}J$ for the absolute different $\mathfrak D_E$. At a nonzero point of that dual the integral ideal $\mathfrak D_E^2 h_V(z,z)$ has norm at least one. The arithmetic-geometric mean inequality implies that its squared trace length is at least $2f/\rho^2$. Banaszczyk’s transference inequality in dimension $2fh$ therefore supplies $2fh$ linearly independent vectors in $J$ with squared lengths at most $B=2fh^2\rho^2$. Choose $h$ spanning over $E$. Every embedding of each entry of their Gram matrix has modulus at most $B$. Integral entries are separated by sup-distance at least one by the absolute norm, so polydisc packing gives at most $(1+2B)^{2f}$ possibilities per entry. For the free sublattice generated by these vectors the determinant bounds the discriminant order by $(hB)^{2fh}$. Its discriminant quotient needs at most $h$ generators, giving at most $(hB)^{2fh^2}$ intermediate lattices. The Gram matrix and the intermediate lattice determine the class. Their count bounds $M_h$ by $(1+2B)^{2fh^2}(hB)^{2fh^2}\le(20f\rho^2)^{16f}\le M_*$. [Banaszczyk, Theorem 2.1][transference]

If $s,j\ge2$, divide $M_2$ by $R_{j+1}R_{j+2}$ and multiply by $\prod_{i=3}^sR_i/R_{j+i}$. This is exactly $M_sM_j/M_k$, and its upper bound is $M_*\rho^f B_0^{js+3}\le M_*\rho^f B_0^{sk}$. When either rank is one use $M_1/R_k$. This proves (9). Combining (7)–(9) gives
$$
 \frac1{m_0}\sum_{[L]}\frac{N_{k-s,a}(L)}{|\operatorname{Aut}L|}
 \le M_*\rho^f 16^{skf}
        (a/D)^{k/2}(aD)^{5s+5+2c}.                              \tag{10}
$$
In fact the comparison of the discriminant powers loses the factor $a^{s+3}D^{(s+5)/2}\ge1$. [Pinned primitive genus estimate][primitive-native]

## Summing the fixed spaces and applying the result

For $0<s<k$, multiply (10) by (4) summed with the bound following it. The rank-dependent factors combine as
$$
 16^{skf}(a/D)^{k/2}(A_s/a)^{k/2}=X^{k/2}(32/g)^{skf}.
$$
By (3) there are at most $DX\le Y$ discriminant orders $a$, and each satisfies $aD\le Y$. Use $(D^4X^3)^h\le Y^{3h}$ and $X\le Y$. The remaining exponent of $Y$ is at most
$$
 (5s+5+2c)+(s+\ell+1)+3(2r+1)+1
       =6s+6r+9+3c\le6s+6r+10+4c .
$$
This yields the middle sum of (1), including its cutoff. In particular the factor $16^{skf}$ comes from comparison of two ordinary definite masses. The factor $2^{skf}/g^{skf}$ comes from the determinant of the displacement on the complement of the fixed space.

If $s=0$, then $\eta=1$, which forces the same embedded lattice and the same graph, and in particular $x=x'$. When the indices agree, count just one datum. There are at most $x^{k+\ell}$ choices of $C$ and at most $(Dx^2)^h(Dx)^h$ completions. Dividing by $Z$ gives at most one since $X=x^2$. Thus the first indicator in (1) accounts for the entire identity contribution. If $x=x'=1$, both diagonal lattices are $L$ and $d(K)=d(L)$ forces $K=K'=L$. Both graphs are the identity graph, and every compatible isometry is an automorphism congruent to the identity modulo $g$. For $g\ge3$ only the identity survives on every lattice, proving the exact mean.

If $s=k$, then $U=0$, $a=y=1$. Count the two sublattices directly to get at most $X^{k+\ell}$ choices. Complete their data and choose the isometry as before, giving at most $e_g^k X^{k+\ell}Y^{3h}$ triples on each $L$. A nonempty fibre forces $A_k\ge1$ by (3); hence $(2/g)^{kf}\sqrt D\,X\ge\sqrt X$. Divide by $Z$ to obtain the last term in (1). The same bounds hold for the normalized averages since the normalized mass weights sum to one. This completes (1) and (2). [Native fixed-free endpoint][zero] · [Roadmap assembly and its two endpoints][assembly]

Finally, for two minor labels the disjoint frame fibres over each triple are bounded by $F_\delta(x)F_{\delta'}(x')$ from the [single-frame calculation](SPECTRAL_FRAME_FIBRE.md). Their leading index factors cancel the $X^{k/2}$ in (1)–(2) to give $(D_\delta D_{\delta'})^{k/2}$. The symbol $D=T^{2f}$ in the genus calculation is the row lattice discriminant, and each minor label has its own separate ideal norm. Undoing the normalization restores **one** factor of genus mass. Thus the paired arithmetic genus mean for the zero-Gram fixed-label estimate is supplied on the original row under the stated Hermitian mass, classification and transference theorems. The local orbital amplitude and the other spectral cells require their respective estimates. [Same-row fixed-label pair count][pairs] · [Operator estimate using this count](SPECTRAL_DIAGONAL_ZERO_CELL.md#from-the-fixed-type-estimate-to-the-operator)

## The exponents after summing the graph indices

On the actual row $g=g_0g_1\ge3$, equation (1) also saves two powers per $k$ in the minor-height allowance. To track them, put $S_1=S_\delta$, $S_2=S_{\delta'}$, $H(a)=b^{am^2f}$, $C_a=\max(1,2(C_H+1),C_T)$ and $U_i=H(C_a)S_i^2$. We have $D_\delta,N_T\le U_1$, the product of the nonzero minor norms is at most $U_1^r$, and $x\le D_\delta$, with the corresponding bounds on the second side. Since $D=N_T^2$, this gives
$$
                    Y=X D^2\le H(C_a)^6(S_1S_2)^2.
$$
The counting threshold in B8.02c gives $(32/g)^{kf}(4kf)^{4f}H(C_a)^{42}\le1/2$. Hence every middle summand of (1) is at most $2^{-s}(S_1S_2)^{12k}$. For the last one use $(2/g)^{kf}\sqrt D\,X\le(32/g)^{kf}Y^6$, so it has the same bound with $s=k$. This uses $e_g=1$. The sum of the geometric factors is at most one. Keeping the quantity $Y^6$ obtained for the graph pairs is what reduces the height exponent here.

For the remaining factors one may keep the original allowances. Indeed $c\le4r$, $M_*\rho^f$ has logarithm at most $O(fr\log(f\rho))$, and the source's size thresholds give $Y^{6r+10+4c}(2+2M_*\rho^f)\le (U_1U_2)^{96r+183}$. In the fixed-frame bound each side apart from its leading index factor costs at most $U_i^{250000r^4}$, by substituting $D_b\le U_i^r$ and $D_\delta,N_T\le U_i$ in its explicit formula. Summing the at most $D_\delta D_{\delta'}$ index pairs costs a further $U_1U_2$. Thus one needs at most $U_i^{251000r^4}S_i^{12k}$ on either side, since $96r+184\le1000r^4$ for $r\ge1$. For $k\ge300000r^4$ this is bounded by $H(C_h)^{C_hr^4} S_i^{14k}$ with $C_h=300000C_a$. Restoring the leading factor and the single genus mass proves B8.02b's same-row arithmetic pair estimate with
$$
          M(j,\delta)=D_\delta^{k/2} H(C_h)^{C_hr^4} S_\delta^{14k}.
$$
The Roadmap at this step uses $16k$. Either allowance suffices for the [operator summation](SPECTRAL_DIAGONAL_ZERO_CELL.md). [Original thresholds, counts and final assembly][collect]

[goal]: https://github.com/rh-lean-roadmap/rh-lean-roadmap/blob/94e6a98b4e74932a0298d6bd22d44cf60c62764b/docs/src/book/main.tex#L15789-L15803
[data]: https://github.com/rh-lean-roadmap/rh-lean-roadmap/blob/94e6a98b4e74932a0298d6bd22d44cf60c62764b/docs/src/book/main.tex#L15645-L15662
[fibre]: https://github.com/rh-lean-roadmap/rh-lean-roadmap/blob/94e6a98b4e74932a0298d6bd22d44cf60c62764b/docs/src/book/main.tex#L41344-L41372
[primitive]: https://github.com/rh-lean-roadmap/rh-lean-roadmap/blob/94e6a98b4e74932a0298d6bd22d44cf60c62764b/docs/src/book/main.tex#L41262-L41292
[splitmass]: https://github.com/rh-lean-roadmap/rh-lean-roadmap/blob/94e6a98b4e74932a0298d6bd22d44cf60c62764b/docs/src/book/main.tex#L41327-L41342
[adj]: https://github.com/rh-lean-roadmap/rh-lean-roadmap/blob/94e6a98b4e74932a0298d6bd22d44cf60c62764b/docs/src/book/main.tex#L23917-L23938
[assembly]: https://github.com/rh-lean-roadmap/rh-lean-roadmap/blob/94e6a98b4e74932a0298d6bd22d44cf60c62764b/docs/src/book/main.tex#L42162-L42185
[native]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AbelianVarietyTheory/Proofs/FlagMeasures/DiscNResNeZero.lean#L312-L428
[row]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AbelianVarietyTheory/Proofs/FlagMeasures/GenusMeanEmbeddedPairsLeMassMulPairBound.lean#L13-L36
[det]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AbelianVarietyTheory/Proofs/FlagMeasures/DiscriminantOrderCommonFixedLatticeEmbeddedData.lean#L372-L410
[primitive-native]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AbelianVarietyTheory/Proofs/FlagMeasures/MeanPrimitiveSublatticesGenusDefiniteLattice.lean#L158-L200
[zero]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AbelianVarietyTheory/Proofs/FlagMeasures/PairsIsometryNoFixedVectorCountBound.lean#L58-L103
[pairs]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AbelianVarietyTheory/Proofs/FlagMeasures/TermPairCountBoundOfSiegelMassRatios.lean#L70-L161
[ghy]: https://web.math.princeton.edu/~jonhanke/Web-02/Mass-Formula-of-Shimura/shimura-mass.pdf
[gross]: https://people.math.harvard.edu/~gross/preprints/incoherent.pdf#page=6
[transference]: https://doi.org/10.1007/BF01445125
[native-graph]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AbelianVarietyTheory/Definitions/SemilocalFrames/FlagPairDefinitePartLattice.lean#L115-L122
[native-trip]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AbelianVarietyTheory/Definitions/SemilocalFrames/NormalFormDualOrthogonalLast.lean#L127-L139

[collect]: https://github.com/rh-lean-roadmap/rh-lean-roadmap/blob/94e6a98b4e74932a0298d6bd22d44cf60c62764b/docs/src/book/main.tex#L41782-L41825
