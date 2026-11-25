# Twisted norm congruences in the nonsingular frame sum

This proves the finite norm-congruence estimate B8.10j on the lattices used in the positive-defect corank-one contribution. It also computes the full local Fourier phase on the nonsingular coordinates. The elementary move correspondence and its selected Haar normalizations are explicit hypotheses in passing to the relative orbital mass at the end. [Statement and application in the Roadmap][rm] · [Native move kernel][kernel]

## The transform of one Hermitian block

Let $F$ be a nonarchimedean local field of characteristic zero with integers $O$, uniformizer $\pi$ and residue cardinality $q$. Let $O_E$ be unramified quadratic over $O$ or $O\times O$ with exchange involution. Fix an additive character $\Psi$ of $F$ with conductor $O$ and put $e_i(z)=\Psi(\pi^{-i}z)$. On $U_0=O_E^\rho$ put $Q(x)=\sum x_j\bar x_j$ and $B(x,b)=\operatorname{Tr}_{E/F}(\sum x_j\bar b_j)$. Write $\epsilon=1$ in the split case and $\epsilon=-1$ in the unramified field case. All integrals use probability Haar measure.

Every linear character on the finite block of depth $N$ has the form $\chi(x)=e_c(B(x,b))$ for $0\le c\le N$, with a primitive vector in the dual $O$-lattice when $c>0$ and $b=0$ for $c=0$. This uses perfection of the trace pairing. For any unit $u$, and $1\le i\le N$,
$$
 \mathbb E_x e_i(uQ(x))\chi(x)=
 \begin{cases}
  0,&c>i,\\
  \epsilon^{i\rho}q^{-i\rho}
     e_i(-u^{-1}\pi^{2(i-c)}Q(b)),&c\le i .
 \end{cases}                                                       \tag{1}
$$
If $c>i$, translation by an element of $\pi^iU_0$ fixing the norm phase multiplies the summand by a nontrivial scalar. If $c\le i$, complete the square by translating by $u^{-1}\pi^{i-c}b$. The identity uses the trace for the polar form, so it holds without inverting two.

To evaluate the remaining untwisted transform, work in one coordinate and write $G_i(u)=\mathbb E_x e_i(u x\bar x)$. For split $O_E$, integration over the second coordinate in the product $x_1x_2$ gives $q^{-i}$. For the unramified field, at depth one the nonzero residue norms have $q+1$ preimages each and the zero norm has one. Orthogonality gives $G_1=-q^{-1}$. For $i\ge2$, averaging the norm phase over shifts by $\pi^{i-1}z$ kills the contribution unless $x\in\pi O_E$. Indeed the squared shift is divisible by $\pi^i$ and the residual trace pairing is perfect. On that surviving ball $x=\pi z$ and its measure is $q^{-2}$, hence $G_i=q^{-2}G_{i-2}$ with $G_0=1$. Taking the product over the independent coordinates proves (1), also for $q=2$.

As an example, for a pure nonsingular block, $0\le a<N$, and any $\lambda\in O$, character orthogonality gives
$$
 q^a\mathbb E_x{\bf1}_{Q(x)\equiv\lambda\bmod\pi^a}\chi(x)
 = {\bf1}_{c=0}+
 \sum_{i=\max(1,c)}^a\epsilon^{i\rho}q^{-i\rho}
 \sum_{u\in(O/\pi^i)^\times}
       e_i(-u\lambda-u^{-1}\pi^{2(i-c)}Q(b)).                      \tag{2}
$$
At $\lambda=0$ inversion permutes the units, so the innermost sum is $q^i{\bf1}_{\pi^i\mid t}-q^{i-1}{\bf1}_{\pi^{i-1}\mid t}$ with $t=\pi^{2(i-c)}Q(b)$. This gives an exact finite expression including its sign.

## Arbitrary complement and primitive moves

Suppose $W\subseteq U$ contains $\rho\ge4$ orthonormal vectors for an integral Hermitian form. Their span $U_0$ splits orthogonally over $O_E$, regardless of the degeneracy of the complement. The full linear character factors over this direct sum. For its restriction to $U_0$ of conductor exponent $c$ and $Z=\{Q_U(x)\equiv\lambda\bmod \pi^a\}$, (1) gives
$$
 \left|q^a\mathbb E({\bf1}_Z\chi)-{\bf1}_{\chi=1}\right|
 \le (1-q^{-1})\sum_{i=\max(1,c)}^a q^{-(\rho-1)i}
 \le \tfrac87 q^{1-\rho}.                                         \tag{3}
$$
The term at additive conductor zero uses the character on the *whole* lattice. Each complementary average has modulus at most one. In particular a positive block conductor $c>a$ forces the whole twisted expectation to vanish. This argument also works conditional on any fixed complement for the untwisted probability with a translated target.

If $h(x,W)$ is a proper ideal, every orthonormal coordinate belongs to the same maximal ideal of $O_E$, after exchanging the two possibilities in the split case if needed. Restricting the coordinates costs $q^{-j\rho}$, with $j=2$ for the inert maximal ideal and $j=1$ for either split maximal ideal. On writing the constrained coordinates as $\pi_E z$, their norm is $\pi^j Q(z)$ with the natural choice of generator. Fix the complementary coordinates. If $a\le j$, the normalized conditional congruence probability is at most $q^j$. If $a>j$, it is zero unless the residual target is divisible by $\pi^j$. Otherwise (3) applied at level $a-j$ bounds it by $q^j(1+(1-q^{-1})/(q^{\rho-1}-1))\le(8/7)q^j$. Thus
$$
 q^a\mathbb P(Z,\ h(x,W)\ne O_E)
 \le \begin{cases}
 (8/7)q^{2(1-\rho)},&E/F\text{ a field},\\
 (16/7)q^{1-\rho},&E\text{ split}.
 \end{cases}                                                       \tag{4}
$$

In the project the two frames have combined dimension at most $2r+2$ in a unimodular lattice of rank $k+2r+1$. The saturated perpendicular lattice $W$ consequently has residual codimension at most $2r+2$. In the nondegenerate residual ambient space its radical is contained in an orthogonal space of dimension at most $2r+2$. The induced nonsingular part therefore has rank at least $\rho=k-2r-3$, at least four at the threshold. In the split case the argument uses two mutually dual residual spaces and dual bases. In the unramified case choose an orthonormal residual basis of a nonsingular summand. Lift one unit vector at a time, rescale it by a unit norm and subtract its orthogonal projection. Unit norm surjectivity follows from finite-field norm surjectivity and successive lifting using the surjective residue trace at every positive depth. This works in residue characteristic two. These lifts give the block used in (3)–(4) on the actual $W$. [Frame complement and local orbit argument][moves]

For the full-image move kernel, retain the source identifications of the move fibres, their relative Haar factors, and the nontrivial character describing the phase on those fibres. Equations (3)–(4) then give normalized kernel row mass within $\delta=(24/7)q^{1-\rho}$ of one, and absolute normalized phase average at most $\delta$. Deleting nonprimitive moves costs at most the bad probability, since the phase has modulus one. If $\mu$ is the system of relative inverse stabilizer volumes and $m$ is the symmetric invariant kernel, orbit double counting gives
$$
 \sum_{[x]}\mu(x)\sum_y m(x,y)\omega(y)
   =\sum_{[x]}\mu(x)\omega(x)\sum_y m(x,y).
$$
Using the two row bounds shows $|\sum_{[x]}\mu(x)\omega(x)|\le2\delta\sum_{[x]}\mu(x)\le7q^{1-\rho}\sum_{[x]}\mu(x)$. Thus the local character cancellation follows on the identified move family. The other local mass comparisons, the global orbit-to-mass identification and the real spectral estimates remain distinct inputs. [Global squared-norm assembly][moves] · [Improved normal multiplicity](SPECTRAL_CORANK_NORMAL_LABELS.md)

[rm]: https://github.com/rh-lean-roadmap/rh-lean-roadmap/blob/02a95b4c62db610642af5f278ee5d0d6df87b348/docs/src/book/main.tex#L17676-L17703
[kernel]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AbelianVarietyTheory/Proofs/FlagMeasures/ExistsSymmInvariantKernelHermitianFrames.lean#L17-L31
[moves]: https://github.com/rh-lean-roadmap/rh-lean-roadmap/blob/02a95b4c62db610642af5f278ee5d0d6df87b348/docs/src/book/main.tex#L45675-L45700
