# A fixed-label arithmetic fibre in the diagonal zero-Gram cell

Fix a word, a row, a positive-rank minor label $(j,\delta)$ and one **embedded** definite datum of index $x$. This datum includes the other lattice and its congruence graph on the fixed row lattice. Its index or its abstract isometry class alone does not prescribe the fibre. Under the unramified CM and frame hypotheses of Roadmap B8.02b-fibre, the following argument recovers its weighted upper bound. It gives a different reduction of the perpendicular lattice, using projections at the nonzero leading minors and a shear on the dual of the common isotropic subspace. No global genus mass enters the single-datum calculation. [Source statement][statement] · [Definition of embedded data and relative isometry][data] · [Use in the diagonal estimate](SPECTRAL_DIAGONAL_ZERO_CELL.md)

Write $O=\mathcal O_E$, $[E:\mathbb Q]=2f$, $T=T_u$, $N_T=T^f$, $c=1+\log_2(2f)$, $\ell=c-1$, $t=r-j$, $d=2r+1$. Put $D=D_\delta$, let $D_b$ be the product of the normalized absolute ideal norms of the nonzero leading minors, and put $M=D_bDN_T$. For $1\le x\le D$, set $H=\sqrt{D/x}$ and
$$
 J_v(H)=\sum_{a,b\ge1,\ ab\le H} a^v.
$$
The relative inverse stabilizer weights of any finite family of inequivalent frames in this fibre have sum at most
$$
 \boxed{\quad
 8^{j+1} f^2 D^c N_T^2\,(D/x)^{k/2}
 (xH)^t J_\ell(H)\,
 M^{(48r+126)d^2+2d}.
 \quad}                                                     \tag{1}
$$
Here $k$ is the rank of the definite space. There are no terms for $x>D$. The constants in (1) are deliberately rounded up. For $H=1$ the index sum is exactly one. In general $J_\ell(H)\le\min(H^{\ell+2},\zeta(\ell+1)H^{\ell+1})$. The following proofs apply to projective lattices over $O$, including the nonfree case.

## The normal form and what the index measures

Use the adapted normal form of the two flags and its identification of integral frame classes with distinct lattice orbits. We spell out the structural information from these inputs. The fixed and moving flag spaces are $X,X'$, with common radical $I=X\cap X'$ of dimension $t$. The two last vectors are $z,z'=u z$, with $h(z,z)=-T$ and $u\bar u=1$. We take $h$ linear in its first variable. The first $j$ flag vectors on each side span the nondegenerate space $J=X_j+X'_j$. Their cross-pairing matrix is block antidiagonal. Within a block of consecutive indices the entries on the antidiagonal are the same nonzero field element up to signs. Blocks are mutually orthogonal. The last common flag grades coincide up to the common scalar $u$. There is an isotropic dual $I^*$ to $I$, perpendicular to $J+Ez$, and an orthogonal decomposition
$$
 V=W\perp\Pi,\qquad \Pi=J\perp Ez\perp(I\oplus I^*).
$$
Here $W$ is the fixed definite lift. Let $P_0$ be the reference lattice in $\Pi$. On each flag line of index $i<r$ its coefficient ideal is $\mathfrak d^{-(r-i)}$, on $Ez$ it is $O$, and its two lattices $I_0\subset I$, $Q_0\subset I^*$ are in perfect duality. Write $U_0=P_0\cap(J+Ez)$. These are direct-sum descriptions inside the rational spaces. [Native block matrix][block] · [Reference lattice and both frame filtrations][model]

A term is a unimodular row lattice $\Lambda$ in this normal form with both prescribed graded flag lattices and the level congruence. Normal-form changes in the common flag-unipotent group $R$ preserve its embedded datum, index and relative weight. On fixing a matrix and scalar, transport the row lattice back by each adapted isometry. An element of $R$ identifying two transported lattices conjugates to an integral fixed-frame equivalence of the original frames. Thus distinct frame classes give distinct lattice orbits, and their weights are bounded by the weights in the chosen models. The other inner lattice above its definite trace takes at most $N_T^2$ values. Its last-vector lift modulo its trace is specified by a class of the trace dual modulo the trace, of order $T^{2f}$. [Actual fixed finite family and weights][frame] · [Inner-lattice split][inner]

In the space $W+I$, let $D_+=(\Lambda+X)\cap(W+I)$, let $C_g$ be the diagonal fixed module of the congruence graph, and let $\Theta=(\Lambda\cap(W+I))+I$. The indices in the source are
$$
 x=[D_+:C_g],\qquad a=[C_g:\Theta],\qquad
 b=[\Lambda\cap X:(\Lambda\cap X_j)+(\Lambda\cap I)].
$$
We shall show $a,b\ge1$, $x a^2 b^2\le D$. For a split representative, $\Theta=A+I$ with $A=\Lambda\cap W$, and its discriminant order satisfies $|A^\#/A|\le(DN_T)^2$. The split condition also gives $[L_W:A]\le xa$, where $L_W=L\cap W$ for the fixed reference inner lattice $L=(X+X')^\perp\cap(\Lambda+X)$. Indeed the quotient injects into $D_+/\Theta$ by intersection with $W$. To achieve splitting, choose an integral section of the projection of $\Lambda\cap(W+I)$ along $I$. Its image spans a complement to $I$. A shear carrying this complement to $W$ lies in $R$: every linear map from this complement to $I$ is a sum of maps $w\mapsto h(w,v)y$ with $y\in I$, and each is the restriction of an Eichler isometry fixing both framed spaces pointwise. [Index and discriminant inputs][index] · [Split representative][split] · [Discriminant after splitting][disc]

Here is a lattice proof of the index and inner-lattice assertions. Reduce first by the saturated isotropic summand on $I$. The image $\bar\Lambda$ of $\Lambda\cap I^\perp$ in $I^\perp/I$ is self-dual. Indeed a vector of the dual defines an integral functional on the saturated submodule $\Lambda\cap I^\perp$. Extend it to $\Lambda$ by projectivity of the quotient and use unimodularity to represent it there. The representing vector differs from the original rational lift by a vector of $(I^\perp)^\perp=I$, proving self-duality. In the quotient identify $I^\perp/I=J\perp U$, with $U=W+Ez$. Put
$$
 P_J=\bar\Lambda\cap J,\quad Q=\bar\Lambda\cap U,\quad
 A_X=\bar\Lambda\cap X_j,\quad A_Y=\bar\Lambda\cap X'_j,\quad
 p=[P_J:A_X+A_Y].
$$
The first terminal index is $[A_X:\Lambda\cap X_j]=b$ by projection from $\Lambda\cap X$. It is also the index of $\Lambda\cap I$ in the projection of $\Lambda\cap X$ to $I$ along $X_j$. The opposite flag gives the same index: its projected tail lattice has the prescribed graded ideals times $u$ on the same ordered lines, and $|N_{E/\mathbb Q}(u)|=1$. Their additive covolumes are equal by the graded filtration. The cross determinant for $\Lambda\cap X_j$ and $\Lambda\cap X'_j$ has ideal norm $D$ by the graded coefficient ideals. Enlarging each lattice by index $b$ divides this norm by $b^2$. Thus the cross determinant for $A_X,A_Y$ has ideal norm $q=D/b^2$. In particular the discriminant group of $A_X+A_Y$ has order $q^2$, and that of $P_J$ has order $(q/p)^2$. These determinant formulas follow locally over a DVR and multiply over the rational primes. [Terminal determinant and equality of the two indices][terminal]

Write $L_X=(\bar\Lambda+X_j)\cap U$, $L_Y=(\bar\Lambda+X'_j)\cap U$. These are the images in $U$ of the native inner lattices after removing the common radical. Each is self-dual by the same isotropic reduction, applied this time to $A_X$ or $A_Y$ in $\bar\Lambda$. Unimodular gluing of $P_J$ and $Q$ identifies their discriminant modules. To see this, $\bar\Lambda/(P_J\oplus Q)$ injects into both discriminant modules by projection and its squared order equals the product of their orders. Thus both projections are isomorphisms and the graph reconstructs $\bar\Lambda$. In particular $[L_X:Q]=[L_Y:Q]=q/p$. In the discriminant module of $P_J$, the classes corresponding under gluing to $L_X/Q$ have representatives in $X_j$, and those for $L_Y/Q$ have representatives in $X'_j$. Their intersection injects into $P_J/(A_X+A_Y)$: choose pure representatives $\alpha,\beta$ of the same class and send it to $\alpha-\beta$ in the quotient. Changing representatives adds an element of $A_X+A_Y$. A zero image forces both pure representatives to belong to their respective intersections by $J=X_j\oplus X'_j$. Consequently
$$
 [(L_X\cap L_Y):Q]\le p.
$$
The definite index modules are $D_+/I=L_X\cap W$, $\Theta/I=Q\cap W$, and $\Theta/I\subset C_g/I\subset L_X\cap L_Y\cap W$. The lower inclusion follows by taking identical lattice lifts on the two sides of the graph. Therefore $xa=[D_+:\Theta]\le q/p$ and $a\le p$. Multiplying gives $xa^2b^2\le D$. This proves the previously used positivity and range, and also $xa\le D$. [Native definite index calculation][index]

The last grade says that $z$ spans a primitive line $Oz$ in $L_X$, and $uz$ a primitive line in $L_Y$. For example an element $vz$ of $L_X$ lifts to $vz+x$ in the original lattice, $x\in X$, so precisely the coefficients $v\in O$ occur. By gluing each last line to its perpendicular in its self-dual lattice, the definite trace in either case has discriminant group isomorphic to $O/(T)$, of order $N_T^2$. Once the opposite trace and $u$ are fixed, its choices of inner lattice are the graphs of isomorphisms from the discriminant of $Ouz$ to that of the trace. The first group is cyclic, so there are at most $N_T^2$ such graphs. Also $A=\Theta/I$ has index $xa$ in $L_X\cap W$, giving $|A^\#/A|=(xaN_T)^2$ by discriminant scaling. Finally the ideals of coefficients on the lines $z$ and $uz$ that land in $Q$ each have norm at most $q/p\le D$, by mapping the respective primitive lines into $L_X/Q,L_Y/Q$. Their ratio is $(u)$. This proves the bounded denominator assertion used below. [Inner trace and number of completions][traces] · [Norm bounds for the two coefficient ideals][scalar]

## Bounding the perpendicular lattice of an orbit

For a block endpoint $p$, put $q_p=\sum_{i<p}(r-i)$ and $\mathfrak m_p=(\delta_p)\mathfrak d^{-2q_p}$, with $\mathfrak m_0=O$. The nonzero leading minors occur at these endpoints. Write
$$
 \mathfrak c=(T)\prod_{p>0}\mathfrak m_p\overline{\mathfrak m_p},
 \qquad n=N\mathfrak c=(D_bN_T)^2 .
$$
The ideals $\mathfrak m_p$ are integral by pairing integral adapted flags and taking determinants. At an endpoint let $S_p=X_p+X'_p$ and $B_p=(\Lambda\cap X_p)+(\Lambda\cap X'_p)$. This is a full integral lattice in the nondegenerate $S_p$. Its discriminant module has zeroth Fitting ideal $\mathfrak m_p\overline{\mathfrak m_p}$: locally choose bases adapted to the two flags. Their cross determinant has ideal $\mathfrak m_p$, and the two diagonal blocks of the Hermitian matrix vanish. Therefore $\mathfrak c B_p^\#\subset B_p$. Orthogonal projection of every member of $\Lambda$ to $S_p$ lies in $B_p^\#$. Multiplication by $\mathfrak c$ brings this projection back into $\Lambda$. At $p=0$ the claim is empty. [Integral ideal and its norm][minor]

On a block of length $h$ between endpoints $p,q$, denote the two coordinate lattices from $P_0$ by $X_0^B,Y_0^B$. Each antidiagonal coefficient ideal for their pairing is the same fractional ideal $\mathfrak b_B$. Indeed the two paired indices sum to a constant, the line ideals are successive powers of the same star-stable ideal, and the scalar varies only by signs. Taking determinants gives $\mathfrak b_B^h=\mathfrak m_q/\mathfrak m_p$. At each prime the absolute value of its valuation is bounded by the larger of the two endpoint valuations, both of which are bounded by the valuation of $\mathfrak c$. The same calculation on conjugate ideals shows
$$
 \mathfrak c P_0^\#\subset P_0,\qquad
 h(P_0,P_0)\subset \mathfrak c^{-1}.
                                                               \tag{2}
$$
The last line uses $\mathfrak c\subset (T)$, and the two common-radical summands pair perfectly. Both inclusions hold for the orthogonal summand $U_0$ as well.

Project $\Lambda\cap X_q$ to the fixed side of the block along $X_p$. Its projected lattice has the same graded coefficient ideals as $X_0^B$. A section of each successive grade exists because its coefficient ideal is projective. Extending the sections to the field gives an upper unitriangular map carrying the projected lattice to $X_0^B$. Act on the opposite side by its inverse adjoint. Reversal of the order within the antidiagonal block makes this action upper unitriangular on that flag as well. These maps on the mutually orthogonal blocks, extended by the identity elsewhere, give one element of $R$ fixing $W$. We now use this representative. By the endpoint projection argument, $\mathfrak c X_0^B\subset\Lambda$. If $Y^B$ is the opposite projected lattice, then $\mathfrak c Y^B\subset\Lambda$ by the same projection. Pair a vector of $\mathfrak c X_0^B$ against an integral lift of a vector of $Y^B$. The earlier blocks are orthogonal to it, giving $h(X_0^B,Y^B)\subset\mathfrak c^{-1}$. By (2) this implies $Y^B\subset\mathfrak c^{-2}Y_0^B$. The two determinant lattices coincide because the graded ideals agree. Locally the elementary divisors of $Y^B$ against $Y_0^B$ consequently sum to zero and each is at least $-2v(\mathfrak c)$. Each is at most $2(h-1)v(\mathfrak c)$. This proves $\mathfrak c^{2h-1}Y_0^B\subset\Lambda$. [Comparison with the source block reduction][block]

Project $\Lambda\cap X$ away from $S_j$ onto $I$. Its image has the tail flag grades prescribed by $I_0$. A unitriangular change on $I$, extended by its inverse adjoint on $I^*$, puts that image equal to $I_0$. This operation fixes $J,Ez,W$ and respects both flags. Clearing the endpoint projection as above gives
$$
 \mathfrak c I_0\subset\Lambda\cap I\subset I_0.
$$
An integral lift of the fixed last-vector grade has the form $z+x_0$ with $x_0\in X$. Projecting away from $J$ gives $\mathfrak c(z+i)\subset\Lambda$ for some $i\in I$. There is a common unitary shear fixing $I,J,W$ and sending $z+i$ to $z$. Its formula is given in the congruence calculation below with displacement $-i$. Thus, with $s=2r+2$, we have arranged
$$
 \mathfrak c^s U_0\subset\Lambda,\qquad
 \mathfrak c I_0\subset\Lambda\cap I\subset I_0.             \tag{3}
$$

Put $P=\Lambda\cap\Pi$ and $\mathfrak a=\operatorname{Ann}(A^\#/A)$. Unimodularity identifies $A^\#/A$ with $P^\#/P$ by gluing. Indeed $\Lambda/(A\oplus P)$ injects into both discriminant groups by projection, since $A,P$ are the full intersections. Its order squared is the product of their orders, by unimodularity. Both projections are therefore bijective, and their graph recovers the lattice. In particular $\mathfrak a P^\#\subset P$, $N\mathfrak a\le|A^\#/A|\le(DN_T)^2$. This ideal is conjugation-stable by the perfect discriminant pairing, since an element annihilates the module precisely when its conjugate annihilates every value of the pairing. These statements include the trivial discriminant module, with annihilator $O$.

Unimodularity also gives $\operatorname{pr}_{I^*}\Lambda=(\Lambda\cap I)^\vee$. Restriction of integral functionals to the saturated summand $\Lambda\cap I$ is surjective by projectivity of the quotient. By (3) its dual contains $Q_0$. Choose a projective section over $Q_0$ and then project to $\Pi$. It is an $O$-linear map, extending over $E$, of the form
$$
 L(v)=v+y(v)+d_1(v)\in P^\#,\qquad
 y(v)\in J+Ez,\quad d_1(v)\in I.
$$
Here $\mathfrak a L(Q_0)\subset P$. Pairing against (3) and applying (2) give $y(Q_0)\subset\mathfrak c^{-(s+1)}U_0$. By pairing $L(v),L(w)$ we get
$$
 h(d_1(v),w)+h(v,d_1(w))=h(L(v),L(w))-h(y(v),y(w))
       \in \mathfrak a^{-1}+\mathfrak c^{-(2s+3)}
       \subset (\mathfrak a\mathfrak c^{2s+3})^{-1}
$$
for $v,w\in Q_0$. The first summand uses $\mathfrak a L(Q_0)\subset P$ and the second uses (2). Let $d_1^*$ be the adjoint for the perfect pairing of $I$ and $I^*$. Choose $\theta\in O$ with $\theta+\bar\theta=1$, using finite unramifiedness of $E/F$ and the surjectivity of the relative trace locally, also above two. The global trace ideal is therefore $\mathcal O_F$. The map
$$
 b_1=\theta(d_1+d_1^*)-d_1
$$
is skew-adjoint. The shear $v\mapsto v+b_1(v)$ on $I^*$, fixing $I,J,Ez,W$, lies in $R$. It replaces $d_1$ by $\theta(d_1+d_1^*)$, which sends $Q_0$ into $(\mathfrak a\mathfrak c^{2s+3})^{-1}I_0$. Let $P'$ be the transformed intersection. Multiply the corrected lifts by $\mathfrak l=\mathfrak a\mathfrak c^{2s+4}$. They lie in $P'$. Their two correction terms lie in $\mathfrak c^sU_0$ and $\mathfrak c I_0$, respectively. Subtract to obtain $\mathfrak l Q_0\subset P'$. Equation (3) now gives $\mathfrak l P_0\subset P'$. Since $P'$ is integral, pairing with $\mathfrak lP_0$ and using (2) gives the upper inclusion in
$$
 \mathfrak h P_0\subset P'\subset\mathfrak h^{-1}P_0,
 \qquad \mathfrak h=\mathfrak a\mathfrak c^{2s+5},
 \qquad N\mathfrak h\le M^{4s+12}.                           \tag{4}
$$
This is the alternative to the source's uniform exponent $12r+50$ on $\mathfrak c$. The ideal in (4) is fixed **after** $A$ is fixed, as required when counting the possible perpendicular lattices over $A$. All changes after the initial splitting fix $W$ pointwise. [Source comparison for the dual-radical correction][skew]

## Relative weights in the bounded set

From now on write $\Lambda,P$ for the representative in (4). Let $G_0,G_1$ be the stabilizers in $R$ of the reference completion and $\Lambda$, respectively. The source weight is $[G_0:G_0\cap G_1]/[G_1:G_0\cap G_1]$. The reference completion is $P_0+(L\cap(W+Ez))$. In particular its intersection with $\Pi$ is $P_0$ and its intersection with $V_0=J+Ez+I$ is $P_0\cap V_0$. Here the coefficient on the last line in $L$ permits no proper fractional enlargement of the pure line $Oz$, by its primitive graded normalization. The skew subgroup $Z$ fixes $V_0$ and $W$ pointwise, and the middle subgroup $R_1$ fixes $V_0$ pointwise. Factoring relative indices along $Z\triangleleft R_1\triangleleft R$ gives factors on $Z, R_1/Z, R/R_1$. The reference subgroup on the skew layer preserves $P_0$; on the top layer it preserves $P_0\cap V_0$. [Reference and three indices][weight] · [Source check on both reference intersections][outer]

Let $\mathfrak u=\mathfrak a\mathfrak h^2$. An isometry fixing $W$ pointwise and congruent to the identity modulo $\mathfrak u$ on $P_0$ preserves $\Lambda$. In fact the $\Pi$-projection of a lattice vector lies in $P^\#\subset\mathfrak a^{-1}P\subset\mathfrak a^{-1}\mathfrak h^{-1}P_0$. Its displacement thus belongs to $\mathfrak hP_0\subset P$. The inclusion of full lattices obtained this way is equality by unimodularity. It follows that the skew factor is at most $(N\mathfrak u)^{d^2}$, the cardinality of the endomorphism ring of a rank-$d$ projective lattice modulo $\mathfrak u$.

For the top layer, take a common flag isometry acting trivially on $P_0\cap V_0$ modulo $(T)\mathfrak u$. It preserves both leading flag spaces $X_j,X'_j$, hence preserves $J$, restricts to an automorphism $B$ on $I$, and sends $z$ to $z+w$ for $w\in I$. Extend its action on $J,I$ by the identity on $W,Ez$ and by the inverse adjoint of $B$ on $I^*$. This extension agrees with the given map on $J+I$. Its action on $Q_0$ is congruent to the identity modulo $(T)\mathfrak u$ by perfect duality. Here $B$ and its inverse preserve $I_0$ since the nilpotent displacement has a finite inverse series. Compose with the isometry which sends $z$ to $z+w$, fixes $J,I,W$, and acts on $I^*$ by
$$
 v\longmapsto v+\lambda(v)z+\theta\lambda(v)w,
 \qquad \lambda(v)=h(v,w)/T.
$$
Pairing the images with $z+w$ gives zero. Pairing two such images gives the additional coefficient $T(\theta+\bar\theta-1)=0$. All other pairings are preserved. Agreement on both flags, together with the identity on the transverse quotient by either flag inside its perpendicular, puts the composition in $R$. More explicitly the perpendicular to the first flag is $X+Ez+W$, and to the second it is $X'+Ez+W$. On these quotients the last vector and $W$ are fixed. Since $w\in(T)\mathfrak u I_0$, perfect duality gives $\lambda(Q_0)\subset\mathfrak u$. This lift acts trivially on $P_0$ modulo $\mathfrak u$, fixes $W$, and has the prescribed restriction to $V_0$. Hence it belongs to $G_1$; the original top-layer class belongs to the image of $G_1$. The top relative factor is at most $(N_T^2N\mathfrak u)^{d^2}$. The finite endomorphism counts used here follow locally from freeness and multiply over the finite support of the ideal. [Native integral lift][lift]

For the middle layer take the rows of the displacement of each dual tail vector modulo $I$, starting at the highest flag index. Their common kernel is $Z$. Let $C_i$ be the coefficient ideal of the $i$-th coordinate in $\Lambda\cap I$ after requiring higher coordinates to vanish. Let $\mathfrak b_i=\mathfrak d^{-(r-i)}$. In the filtration of $\Lambda\cap X$ the corresponding leading ideals are $\mathfrak b_i$. The sublattice $(\Lambda\cap X_j)+(\Lambda\cap I)$ has tail leading ideals $C_i$, so $\prod_{i\ge j}[\mathfrak b_i:C_i\cap\mathfrak b_i]\le b$. In the reference stabilizer the $i$-th row belongs to $\mathfrak b_i L_W$ modulo rows of the term stabilizer. To see the bound, multiply the dual vector by its coefficient ideal $\mathfrak b_i^{-1}$ in $P_0$. Displacements of these multiples belong to the reference completion; their definite components, after passage modulo $I$, are in $L_W$. Indeed in the middle group the displacement has no component on $J,Ez$ or $I^*$, by orthogonality to $V_0$. In the completion only $L\cap(W+Ez)$ can contribute a definite component. If its last component is canceled by a reference last-vector coefficient, that coefficient is integral and its multiple of $z$ already lies in $L$. Multiplication back by the invertible coefficient ideal gives the assertion. [Native row bound][rowbound]

For $y\in\Lambda\cap I$, $v\in A$, the transvection
$$
 p\longmapsto p+h(p,-v)y+h(p,y)v-\theta h(v,v)h(p,y)y
$$
is integral, isometric, and fixes $V_0$. Isometry follows by expanding pairings using $h(y,y)=h(y,v)=0$ and $\theta+\bar\theta=1$. Its definite row is $h(e_i^*,y)v$, with the higher rows zero whenever the higher coefficients of $y$ vanish. The term row group therefore contains $(C_i\cap\mathfrak b_i)A$ (the row coefficient may be conjugated under the first-linear convention; take conjugates of the coefficient ideals throughout, which preserves their indices and the reference ideal). The index in the sum of the two row groups is at most
$$
 [\mathfrak b_i L_W:(C_i\cap\mathfrak b_i)A]
   =[\mathfrak b_i:C_i\cap\mathfrak b_i]^k [L_W:A].
$$
The equality follows locally for free modules and then globally by multiplication. Taking successive row kernels gives a middle relative factor at most $b^k(xa)^t$. This also gives one when $t=0$. [Native middle group and Eichler rows][middle]

## Counting and the genus normalization

For a fixed $(a,b)$, the choices of $A$ are at most $a^{k+\ell}$. Indeed on the split representative $A+I=\Theta$ is a sublattice of index $a$ in the fixed rank-$k$ quotient $C_g/I$, and intersection with $W$ recovers $A$. For a rank-$k$ projective lattice, a chain with prescribed prime-ideal quotients of product norm $a$ has at most $a^k$ choices because each step consists of choosing a hyperplane over its residue field of order $q$, with at most $q^k$ choices. Every quotient is obtained for a fixed ordering of the primes in its Fitting ideal by the primary decomposition. The number of ideals of norm $m$ is at most $(2f)^{\Omega(m)}\le m^\ell$. Indeed at a rational prime $p$ their generating series is the product of $(1-z^{f_{\mathfrak p}})^{-1}$ over primes above $p$, bounded coefficientwise by $(1-z)^{-2f}$. The number of weak compositions of $v_p(m)$ in $2f$ parts is at most $(2f)^{v_p(m)}$ by counting strings. [Lattice chain count][chains]

Once $A$ is fixed, (4) bounds the number of $P$ by $(N\mathfrak h)^{2d^2}$. The interval quotient $\mathfrak h^{-1}P_0/\mathfrak hP_0$ has order $(N\mathfrak h)^{2d}$; each submodule is generated by at most $d$ elements. Locally this follows by lifting to a submodule of a free module over a DVR, and the generators combine by the Chinese remainder theorem. Similarly the finite module $P^\#/P$ needs at most $d$ generators. Every possible unimodular gluing is a graph of a map from it to $A^\#/A$, so the number of gluings is at most $(DN_T)^{2d}$. This is an upper bound even if the required anti-isometry or the term conditions exclude most graphs. The number of these representatives bounds the number of orbits. The weight is unchanged on each orbit. Powers of a fixed unipotent and of its inverse have a bounded common denominator by their binomial expansion; hence they take a given full lattice to finitely many lattices. Multiplicativity of relative indices along these powers gives relative change one. The inner datum of the transported lattice is the same, so the reference construction gives the equality $\Lambda_{\rm ref}(s\Lambda)=\Lambda_{\rm ref}(\Lambda)$. Multiplicativity thus compares the two term stabilizers against the identical reference lattice. [Original orbit count][orbit] · [Relative weight under transport][invariance]

Since $N\mathfrak u\le M^{8s+26}$ and $N_T^2\le M^2$, multiplying the count and the three weight factors gives, for fixed matrix, scalar, both inner lattices and $(a,b)$,
$$
 (ab)^k a^\ell (xa)^t M^{(24s+78)d^2+2d}.
$$
There are at most $8^j$ signed block matrices with the given leading minors. Record the ordered composition of $j$ into block lengths, one determinant root of degree at most the length per block, and the individual column signs. Each of the three counts is at most $2^j$. The scalar has at most $8f^2 D^c$ choices. Indeed the two integral ideals of norm at most $D$ with ratio $(u)$ obtained in the primitive last-line calculation above reduce to coprime numerator and denominator ideals. Since $u\bar u=1$, the numerator is the conjugate of the denominator. The reduced denominator still has norm at most $D$, and the preceding ideal count gives at most $\sum_{m\le D}m^\ell\le D^c$ possibilities. Two scalars for the same reduced denominator differ by a norm-one unit. All conjugates of that unit have modulus one, so its powers lie in a compact subset of the Minkowski lattice and the unit is a root of unity. If the group of roots of unity has order $w$, then $\varphi(w)\le2f$ and $\varphi(w)\ge\sqrt{w/2}$ by the prime-power formula. Thus $w\le8f^2$. [Finite normal-form parameters][frame] · [Two ideals for the actual scalar][scalar]

Multiply by the $N_T^2$ choices of the other inner lattice. Finally $ab\le H$ gives $(ab)^k\le H^k$ and $(xa)^t\le(xH)^t$. Summing $a^\ell$ gives $J_\ell(H)$. Its elementary estimate follows either by counting at most $H^2$ pairs, or by first fixing $b$ and bounding $\sum_{a\le H/b}a^\ell\le(H/b)^{\ell+1}$. This proves (1). In particular $xH\le D$, $J_\ell(H)\le D^{(\ell+2)/2}$, and
$$
 r+(48r+126)(2r+1)^2+2(2r+1)\le10000(r+1)^3 .
$$
Absorb $(xH)^t$ into $M^r$. Since $c+(\ell+2)/2\le3c+6$, (1) implies the exact right-hand side required in B8.02b-fibre,
$$
 F_\delta(x)= (D/x)^{k/2}8^{r+1}f^2 D^{3c+6}N_T^2
                 (D_b D N_T)^{10000(r+1)^3}.
$$

For two types on the same row, the [paired genus theorem](SPECTRAL_PAIRED_GENUS.md) counts triples $(K,\Gamma),(K',\Gamma'),\eta$ on the genus, with $\eta$ respecting the two level graphs. Its normalized bound has the factor $(xx')^{k/2}$. Above each triple the sum of products of nonnegative frame weights is bounded by $F_\delta(x)F_{\delta'}(x')$, since it is a subset of the product of the two frame fibres. The index powers give exactly
$$
 (xx')^{k/2}(D/x)^{k/2}(D'/x')^{k/2}=(DD')^{k/2}.
$$
The genus count is weighted by reciprocal *finite* row stabilizer orders and divided by the genus mass. Undoing that division restores the single genus mass in the same-row pair bound. The relative unipotent weight in the single-frame calculation has already been included. The [real orbital estimate](SPECTRAL_ORBITAL_AMPLITUDE.md) supplies the complementary fixed-label amplitude. The proof here replaces the weighted-frame-fibre estimate as a single imported assertion. Its structural inputs are the adapted frame normal form, its level data and the identification of its lattice orbits with the actual frame classes. The index and inner-lattice counts, bounded representative, three relative stabilizer factors and sum over the finite parameters have been derived above. The [paired mean](SPECTRAL_PAIRED_GENUS.md) supplies the other arithmetic factor. [Original exact pair-count hypotheses][pair] · [Genus triple bound][statement] · [Crossing the two arithmetic factors][assemble]

For a literature comparison, Terakado and Yu compute the mass of a unimodular Hermitian lattice over a CM field with a condition at two. Their mass is pertinent to the definite genus calculation. A congruence graph, two simultaneous frame filtrations, and the relative unipotent stabilizer are extra data in the fibre treated here. [Terakado–Yu, *Mass formulas and the basic locus of unitary Shimura varieties*](https://arxiv.org/abs/2210.04054)

[statement]: https://github.com/rh-lean-roadmap/rh-lean-roadmap/blob/94e6a98b4e74932a0298d6bd22d44cf60c62764b/docs/src/book/main.tex#L15773-L15806
[data]: https://github.com/rh-lean-roadmap/rh-lean-roadmap/blob/94e6a98b4e74932a0298d6bd22d44cf60c62764b/docs/src/book/main.tex#L15645-L15662
[model]: https://github.com/rh-lean-roadmap/rh-lean-roadmap/blob/94e6a98b4e74932a0298d6bd22d44cf60c62764b/docs/src/book/main.tex#L41869-L41901
[minor]: https://github.com/rh-lean-roadmap/rh-lean-roadmap/blob/94e6a98b4e74932a0298d6bd22d44cf60c62764b/docs/src/book/main.tex#L15717-L15737
[weight]: https://github.com/rh-lean-roadmap/rh-lean-roadmap/blob/94e6a98b4e74932a0298d6bd22d44cf60c62764b/docs/src/book/main.tex#L42032-L42065
[outer]: https://github.com/rh-lean-roadmap/rh-lean-roadmap/blob/94e6a98b4e74932a0298d6bd22d44cf60c62764b/docs/src/book/main.tex#L42085-L42100
[chains]: https://github.com/rh-lean-roadmap/rh-lean-roadmap/blob/94e6a98b4e74932a0298d6bd22d44cf60c62764b/docs/src/book/main.tex#L41239-L41247
[assemble]: https://github.com/rh-lean-roadmap/rh-lean-roadmap/blob/94e6a98b4e74932a0298d6bd22d44cf60c62764b/docs/src/book/main.tex#L41783-L41819
[rowbound]: https://github.com/rh-lean-roadmap/rh-lean-roadmap/blob/94e6a98b4e74932a0298d6bd22d44cf60c62764b/docs/src/book/main.tex#L42107-L42138
[block]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AbelianVarietyTheory/Proofs/FlagMeasures/NormalFormFlagLatticesNearUnderStabiliser.lean#L587-L640
[frame]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AbelianVarietyTheory/Proofs/FlagMeasures/FlagFrameVectorMemCommonSubspace.lean#L120-L270
[inner]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AbelianVarietyTheory/Proofs/FlagMeasures/SumWeightsInequivalentHermFrameTermsLe.lean#L44-L95
[index]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AbelianVarietyTheory/Proofs/FlagMeasures/FlagPairDefiniteThetaLatticeLeFixedIndexBound.lean#L117-L156
[split]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AbelianVarietyTheory/Proofs/FlagMeasures/HermFramePairExistsUnipotentSplitLattice.lean#L130-L186
[disc]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AbelianVarietyTheory/Proofs/FlagMeasures/HermFramePairOmSumSameDatumLe.lean#L188-L235
[skew]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AbelianVarietyTheory/Proofs/FlagMeasures/HermFramePairSplitTermNearReferenceBySkew.lean#L509-L582
[lift]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AbelianVarietyTheory/Proofs/FlagMeasures/HermFramePairNormalFormCongruenceLiftSmallGroup.lean#L782-L943
[middle]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AbelianVarietyTheory/Proofs/FlagMeasures/HaarInvVolumeMiddleLayerEichlerLe.lean#L1008-L1183
[orbit]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AbelianVarietyTheory/Proofs/FlagMeasures/HermFramePairOmSumSameDatumLe.lean#L237-L318
[invariance]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AbelianVarietyTheory/Proofs/FlagMeasures/RelIndexNeZero.lean#L169-L211
[scalar]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AbelianVarietyTheory/Proofs/FlagMeasures/HermFramePairScalarEqQuotIdealsNormLe.lean#L53-L77
[pair]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AbelianVarietyTheory/Proofs/FlagMeasures/TermPairCountBoundOfSiegelMassRatios.lean#L70-L161
[terminal]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AbelianVarietyTheory/Proofs/FlagMeasures/NormalFormTerminalDeterminant.lean#L274-L364
[traces]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AbelianVarietyTheory/Proofs/FlagMeasures/CardInnerLatticesWithDefiniteTraceLeNorm.lean#L12-L189
