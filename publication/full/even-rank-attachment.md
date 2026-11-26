# Removing the auxiliary characters in even rank

The Roadmap constructs spherical attachment using definite unitary groups. In even rank it extracts the desired representation from two odd-rank theta lifts. This section follows that construction at split places. The general linear attachment used on the cohomological window also follows directly from the published theorem over CM fields. [Spherical Galois attachment](../../manuscript/notes/galois/SPHERICAL_GALOIS_ATTACHMENT.md)

Consider a definite unitary form $U$ of positive even rank $n$ on the CM field of the stable-range construction. The prescribed set $Q$ consists of split places. After omitting any finite subset of $Q$, the conjugacy classes of the inverse Frobenius elements there are dense in the absolute Galois group $G_E$. Fix a comparison of coefficient fields and the inverse-arithmetic-Frobenius convention. If $B$ is a spherical Satake multiset at $w$, write $A_a(w,B)=q_w^{(a-1)/2}B$ for the roots in rank $a$. The normalization depends on the rank and must be applied before comparing the two lifts. We derive the two families of characters in RH Lean Roadmap B9.41 and prove the descent step B9.42–45. [Arithmetic conventions and the global statement](https://github.com/rh-lean-roadmap/rh-lean-roadmap/blob/c7755c1086f05d0918ee8496d95912e4f35e22f9/docs/src/book/main.tex#L24580-L24600) · [The two-lift hypothesis and the subtraction statements](https://github.com/rh-lean-roadmap/rh-lean-roadmap/blob/c7755c1086f05d0918ee8496d95912e4f35e22f9/docs/src/book/main.tex#L25238-L25282)

<!--
% BEGIN GERK1
-->

<span id="claim:GERK1"></span>**Two lifts with disjoint auxiliary characters.** Fix a spherical target place $w_0$. Assume the field conditions and admissible self-dual lattices of B9.39 and B9.41, the stable-range lift and its split local pairing, the split Satake formula B9.40a, and the unitary-character existence lemma B9.36c. We derive the arithmetic and archimedean parameters of both lifts. If $d_0$ is the stable-range bound, take $t=2(d_0+n)+1$ and $d=n+t$. Thus $d$ is odd, $d\ge d_0$ and $t>n$. Choose a lower bound $b$ for all the source weights at the chosen complex embeddings. B9.36c supplies a unitary Hecke character $\chi$, unramified at $w_0$, restricting to the quadratic character of $E/F$, whose archimedean value at each chosen embedding is $(z/|z|)^{-1}$. Take a positive odd integer $K$ with $K\ge d-2b$. For $u=0,1$ use the pair $\chi_{X,u}=\chi^{2u}$, $\chi_{W,u}=\chi^{K+2u}$. Their restrictions have the parity of $n$ and $d$, respectively. The target exponent is $-K-2u$, and $d-K-2u\le 2b$ verifies the stable-range weight inequality for both pairs. [Character existence](https://github.com/rh-lean-roadmap/rh-lean-roadmap/blob/c7755c1086f05d0918ee8496d95912e4f35e22f9/docs/src/book/main.tex#L25074-L25084) · [Stable-range hypotheses and local pairing](https://github.com/rh-lean-roadmap/rh-lean-roadmap/blob/c7755c1086f05d0918ee8496d95912e4f35e22f9/docs/src/book/main.tex#L25201-L25219)

Let $N$ denote the idèlic norm, with $N(\varpi_w)=q_w^{-1}$ at a finite place and $N(z)=z\bar z$ at a complex place. Using the same $K$ in both pairs, define
$$
 \kappa=\chi^K N^{t/2},\qquad
 a_j=-\frac{n+2t-2}{2}+j,\qquad
 \psi_{u+1,j}=\chi^{2u}N^{a_j}\quad(0\le j<t).
$$
At a chosen complex embedding the exponent pair of $\kappa$ on $(z,\bar z)$ is $(m,t-m)$, where $m=(t-K)/2$. The pair for $\psi_{u+1,j}$ is $(a_j-u,a_j+u)$. All these exponents are integers. The difference of the two exponents is zero in the first family and $-2$ in the second, so equality of characters across the families is impossible. All the finite local characters just defined are unramified at $w_0$. [Construction in the pinned source](https://github.com/rh-lean-roadmap/rh-lean-roadmap/blob/c7755c1086f05d0918ee8496d95912e4f35e22f9/docs/src/book/main.tex#L61203-L61213)

At a split place where $\kappa$ and the $u$-family are unramified, $\chi^{2u}$ and $\chi^K$ are unramified because powers of the norm are unramified. Put $x=\chi^{2u}(\varpi_w)$, $y=\chi^{K+2u}(\varpi_w)$ and $q=q_w$. B9.40a gives the Satake roots of the lift as $(xy^{-1})B$ and $xq^{(t-1)/2-j}$ for $0\le j<t$. Multiplication by $q^{(d-1)/2}$ turns the contributing source roots into $\kappa(w)^{-1}A_n(w,B)$, since $xy^{-1}q^{t/2}=\chi^{-K}(\varpi_w)q^{t/2}$. The remaining roots become $xq^{-a_j}=\psi_{u+1,j}(w)$. This accounts for every root with its multiplicity. [Split Satake multiset](https://github.com/rh-lean-roadmap/rh-lean-roadmap/blob/c7755c1086f05d0918ee8496d95912e4f35e22f9/docs/src/book/main.tex#L25227-L25245)

The jump calculation uses $J(\lambda)=\{k-\lambda_k:0\le k<n\}$. At the chosen embedding the weight formula in B9.39 gives $\lambda'_k=\lambda_k-m$ for $k<n$ and $\lambda'_k=n/2-u$ for $n\le k<d$. The first $n$ jumps are $J(\lambda)+m$. The other $t$ jumps are $n/2+i+u$ for $k=n+i$, $0\le i<t$. On writing $j=t-1-i$ these become $-(a_j-u)$, the negatives of the first exponents of the added characters. At the conjugate embedding a dual weight in rank $h$ replaces a jump $x$ by $h-1-x$, since its $k$th component is minus the $(h-1-k)$th original component. Accordingly the common jumps at this embedding are $J(\lambda_{\bar\tau})+(t-m)$, and the added jumps are the negatives of $a_j+u$ with multiplicity. This proves the jump assertion in B9.41 at both embeddings. [Jump convention](https://github.com/rh-lean-roadmap/rh-lean-roadmap/blob/c7755c1086f05d0918ee8496d95912e4f35e22f9/docs/src/book/main.tex#L24645-L24647) · [Weights of a stable-range lift](https://github.com/rh-lean-roadmap/rh-lean-roadmap/blob/c7755c1086f05d0918ee8496d95912e4f35e22f9/docs/src/book/main.tex#L25201-L25215)

<!--
% END GERK1
-->

<!--
% BEGIN GERK2
-->

<span id="claim:GERK2"></span>**Odd-rank attachment.** Suppose the odd-rank attachment has been proved on these lifts. Let $r_i$ be the attached semisimple representations, and let $L_i$ be the direct sum of the $t$ one-dimensional Galois realizations for lift $i$. Injectivity of the realization on the chosen characters keeps the sets of isomorphism classes in $L_1$ and $L_2$ disjoint. Repetition within either set is allowed. At a cofinite set of $w\in Q$ away from $\ell$, the inverse-Frobenius roots of $r_i$ consist of the common multiset $\kappa(w)^{-1}A_n(w,B)$ together with the roots of $L_i$. At $w_0$ the local comparisons hold for the first lift and its lines. These are precisely the hypotheses that the construction of the lifts and odd-rank compatibility must supply. [Odd-rank application at the selected place](https://github.com/rh-lean-roadmap/rh-lean-roadmap/blob/c7755c1086f05d0918ee8496d95912e4f35e22f9/docs/src/book/main.tex#L61215-L61219)

**The global summand.** Compare $V=r_1\oplus L_2$ and $W=r_2\oplus L_1$. At every one of the good inverse Frobenius elements their characteristic polynomials are the common polynomial multiplied by both auxiliary polynomials. Their trace characters therefore agree on a dense conjugacy-invariant subset, hence on $G_E$ by continuity.

Here is the multiplicity argument over $\overline{\mathbb Q}_\ell$. Let $A$ be the image of the group algebra on $V\oplus W$. It is finite dimensional. Its submodules are the $G_E$-stable subspaces, so $V\oplus W$ is a faithful semisimple $A$-module. The Jacobson radical annihilates this module and must be zero. The structure theorem for finite-dimensional semisimple algebras identifies $A$ with a product of matrix algebras. Equality of the two traces on group elements extends by linearity to equality on $A$. A diagonal matrix unit in one factor has trace one on the corresponding simple module and zero on the others. Its trace on $V$ or $W$ is therefore exactly that module's multiplicity. Since the coefficient field has characteristic zero, equality of traces gives equality of all the integer multiplicities.

Write $m_i(S)$ for the multiplicity of a simple representation $S$ in $r_i$ and $a_i(S)$ for its multiplicity in $L_i$. Thus $m_1(S)+a_2(S)=m_2(S)+a_1(S)$. If $a_1(S)>0$, then $a_2(S)=0$ and $m_1(S)=m_2(S)+a_1(S)\ge a_1(S)$. All differences $m_1(S)-a_1(S)$ are consequently nonnegative and equal $m_2(S)-a_2(S)$. The representation $s$ with these multiplicities has dimension $n$, and $r_i\simeq s\oplus L_i$ for both $i$. This recovers an actual Galois representation with the desired constituents.

<!--
% END GERK2
-->

<!--
% BEGIN GERK3
-->

<span id="claim:GERK3"></span>**Local comparison.** Put $r=s\otimes\kappa_\ell$. If $w_0\nmid\ell$, inertia acts trivially on $r_1$ and on $\kappa_\ell$ at this place by the spherical comparison. It acts trivially on the summand $s$ and on $r$. For any prescribed Satake multiset $B$ of $U$ at $w_0$, cancel the monic characteristic polynomial of $L_1$ in that of $r_1$. Twisting multiplies each remaining inverse-Frobenius root by $\kappa(w_0)$, giving exactly $A_n(w_0,B)$. The same computation away from a finite exceptional set is weak attachment on $Q$.

If $w_0\mid\ell$, the first lift and its lines have the crystalline comparison of the odd-rank theorem. The functor $D_{\rm cris}$ preserves direct sums. The crystalline dimension of any representation is at most its dimension, and the first lift attains equality, so equality also holds on each summand. Thus $s$ is crystalline. In a de Rham direct sum, every graded piece of the filtered module is the direct sum of its two graded pieces. At each induced embedding, remove the multiplicities of the jumps of $L_1$ from those of $r_1$. Write $m_\tau=m$ at the chosen embedding and $m_{\bar\tau}=t-m$ at its conjugate. B9.41 gives the remaining jumps at each embedding as $J(\lambda_\tau)+m_\tau$. The twisting line has jump $-m_\tau$, giving $J(\lambda_\tau)$ for $r$. For any compatible period datum the Weil operator respects the same direct sum. Its characteristic polynomial on $s$ is obtained by cancelling that of $L_1$. For $g$ of Weil degree $j$, twisting therefore gives
$$
 \det(X-\mathrm{WD}(r)(g))
       =\prod_{\alpha\in A_n(w_0,B)}(X-\alpha^{-j}).
$$
This uses the spherical crystalline assertion at $w_0$ and the character realization with its specified local normalization. Semisimplicity alone would give no filtration or crystalline dimension. [Precise local hypotheses and polynomial convention](https://github.com/rh-lean-roadmap/rh-lean-roadmap/blob/c7755c1086f05d0918ee8496d95912e4f35e22f9/docs/src/book/main.tex#L25261-L25274)

**Changing the target place.** For another spherical place $v\in Q$, apply the two-lift construction with target $v$, obtaining $r^{(v)}$. Remove from $Q$ the finite exceptional sets of both constructions, the places above $\ell$ and the places where $U$ is nonspherical. At each remaining place use the same Satake multiset of $U$ for $r$ and $r^{(v)}$. Their traces coincide there. Density and the trace calculation above give $r\simeq r^{(v)}$, so the local comparison established at $v$ holds for $r$ as well. This proves the split spherical assertion for every such $v$. [Passage from one target to all spherical places](https://github.com/rh-lean-roadmap/rh-lean-roadmap/blob/c7755c1086f05d0918ee8496d95912e4f35e22f9/docs/src/book/main.tex#L25275-L25281)

<!--
% END GERK3
-->
