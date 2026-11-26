# The normalized theta vacuum on a self-dual lattice

At a fixed step of the tower, let $S,T$ have the prescribed self-dual Hermitian lattices and real Cartan involutions. Fix the source's standard additive character $\psi$ and its real embeddings. On the adelic Hom space, there exists a theta function $f_0$ which satisfies the real Fock vacuum equations, has the required finite lattice symmetries, and has mean square one on the rational quotient. The construction works at each stage independently, before any choice of a reference lift or finite test. [Vacuum and its normalization][vac]

## A characteristic function at the finite places

Write $W=\operatorname{Res}_{E/F}\operatorname{Hom}_E(S,T)$, $B=\operatorname{Tr}_{E/F}(\xi_0 h_O)$ for its alternating form, and $\Lambda_v$ for the source's completed Hom lattice at a finite place $v$ of $F$. Its dual for the character $\psi_v(B(\cdot,\cdot))$ is itself. The lattice includes the coefficient ideal $\mathfrak A$ in its rank-one Hom generators. In the Hermitian pairing on two such generators, the two lattice pairings are integral, and their coefficients contribute $\mathfrak A\overline{\mathfrak A}$. The host identity $\xi_0\mathfrak A\overline{\mathfrak A}=\mathfrak D_{E/\mathbb Q}^{-1}$ makes the absolute trace pairing integral. Conversely, testing against all such generators, using the inverse different and the self-duality of the two Hermitian lattices, recovers exactly the Hom lattice. This calculation localizes, since these full lattices are finitely generated and trace duality commutes with localization. It identifies the annihilator for the actual character, also at primes dividing the different. [Rank-one duality and proof][ratdual] · [Completed lattice and conductor calculation][dual]

Choose transverse $F_v$-Lagrangians $X_v,Y_v$ with $\Lambda_v=L_X\oplus L_Y$, where $L_X=\Lambda_v\cap X_v$ and $L_Y=\Lambda_v\cap Y_v$. One can obtain these by splitting the alternating form on the lattice into planes over the valuation ring. Choose a pair of basis vectors whose nonzero pairing has least valuation among the entries of its matrix. Integral row and column operations make every remaining vector orthogonal to this pair. Induction gives the desired planes. Their first vectors span one Lagrangian and their second vectors span the other. At a split place one can instead take the two halves of $E_v=F_v\times F_v$. Each half is isotropic and its idempotent preserves the lattice. In both constructions $L_Y$ is the exact character annihilator of $L_X$ by self-duality.

In the Schrödinger model on $X_v$ put $\phi_v=\mathbf1_{L_X}$. For $u=x+y$ the Heisenberg operator is
$$
 (\rho_v(x+y)\phi)(s)=
 \psi_v\!\left(B(s,y)+\tfrac12 B(x,y)\right)\phi(s+x).
$$
For $x\in L_X$ and $y\in L_Y$, translation preserves $L_X$ and $\psi_v(B(s,y))=1$ on it. On replacing $u$ by $2u$ the remaining scalar is $\psi_v(2B(x,y))=1$. At a split place a vector in **either** half-lattice has $x=0$ or $y=0$ in the split polarization, so already $\rho_v(u)\phi_v=\phi_v$. This verifies the undoubled condition on each half even in residue characteristic two. At odd places $2\Lambda_v=\Lambda_v$. [The lattice and split-half conditions][vac] · [A split-place idempotent and its conjugate][split]

These choices give a restricted tensor of Schwartz–Bruhat vectors. Indeed, fix a rational symplectic basis and its polarization. Away from finitely many places the basis is integral, the lattice is standard in that basis, the character has its standard conductor and the residue characteristic is odd. At those places use the integral characteristic function, which is fixed by the entire lattice, including both halves whenever the place splits. At the finitely many exceptional places transfer the chosen local vectors to the rational polarization. Changes of Schrödinger model by Fourier transform and linear changes of variables preserve the Schwartz–Bruhat space and intertwine the Heisenberg operators. [Weil, *Sur certains groupes d’opérateurs unitaires*](https://doi.org/10.1007/BF02391012)

## The Gaussian and its rational translates

At a real place the prescribed Cartans give a complex structure $J$ and an alternating form $\Omega$ such that $\psi_v(B(z,w)/2)=\exp(-\pi i\Omega(z,w))$ and $\Omega(z,Jz)>0$ for $z\ne0$. This sign follows by diagonalizing the two Hermitian forms in their Cartan frames. The sign on each matrix line is the product of the signs of its row and column, and the same product occurs in $J$. The remaining factor in the positive quadratic form is a positive multiple of the absolute value of the chosen imaginary generator $\xi_0$. In symplectic coordinates $(q,p)$ adapted to $J$, take $J(q,p)=(-p,q)$ and $\Omega((q,p),(q',p'))=q\cdot p'-p\cdot q'$. For a coordinate direction in $q$, the vacuum equation is $(\partial_{s_j}+2\pi s_j)\phi_v=0$, since the $p$ direction acts by $-2\pi i s_j$. Thus $\phi_v(s)=\exp(-\pi\|s\|^2)$ satisfies all the equations, including the $p$ directions by $J^2=-1$. Transfer it to the real part of the rational polarization. [Complex structure, sign and positivity][positive] · [Source annihilation operator][annih]

Write $W=X\oplus Y$ for the rational polarization and take the product $\Phi$ of these local vectors. Define
$$
 f(w)=\sum_{a\in X(F)}(\rho(w)\Phi)(a).
$$
For $\gamma\in W(F)$, rational translations permute $X(F)$ and rational modulations have value one there. The Heisenberg product law therefore gives
$$
 f(\gamma+w)=\psi(-B(\gamma,w)/2)\, f(w).
$$
The same product law intertwines right Heisenberg translation with $\rho$ on the Schwartz vector. Consequently $f$ has the finite symmetries proved above and satisfies every real annihilation equation. The sums and all their real derivatives converge locally uniformly. On compact sets of translates the contributing rational points lie in a fixed fractional lattice in the real vector space, and every real derivative has Schwartz decay. In particular the finite open level $2\prod_v\Lambda_v$ and the required real smoothness belong to this very function. [Theta transform and the rational sign](WEIL_AUTOMORPHIC_MODEL.md#how-a-sum-over-a-lattice-gives-the-theta-kernel)

This transform is injective on Schwartz functions. For fixed $x\in X(\mathbb A_F)$ multiply $f(x+y)$ by $\psi(-B(x,y)/2)$ and vary $y$ on $Y(F)\backslash Y(\mathbb A_F)$. Its Fourier coefficient at $a\in X(F)$ is $\Phi(a+x)$ by character orthogonality. In particular $f=0$ would force $\Phi(x)=0$ for all $x$. The nonzero continuous function $|f|^2$ descends to the compact additive quotient $W(F)\backslash W(\mathbb A_F)$ and has a finite strictly positive integral there. Divide $f$ by the square root of this integral for quotient probability measure. Every additive Haar measure and fundamental domain with covolume one induces that same probability measure. This produces a single $f_0$ with every normalization in the source. In dimension zero the constant function one has these properties. [Normalization on all fundamental domains][normal]

## The marked finite tests

At a marked split place the two undoubled invariances pick out the local line spanned by the lattice indicator. In a polarization by the two halves, modulations force support on the chosen half-lattice and translations make the vector constant there. The tower and row can therefore replace that indicator by their respective finite matrix functions, starting from any vacuum satisfying the same symmetries. [The two finite tests and their formulas](THETA_FINITE_LATTICE_TESTS.md)

[vac]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Formalism/LocalToGlobal/IndefiniteReal/LocalNewformFunction.lean#L197-L227
[ratdual]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AbelianVarietyTheory/Proofs/AdelicLatticeProofs/RationalHermitianRankOneLatticeSelfDual.lean#L130-L161
[dual]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AbelianVarietyTheory/Proofs/AdelicLatticeProofs/SelfDualLatticePairingDual.lean#L89-L123
[split]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Formalism/LocalToGlobal/BesselHermitianTheta/TiedWeil.lean#L68-L75
[positive]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AbelianVarietyTheory/Proofs/AdelicLatticeProofs/ExistsRealPlaceSymplecticFormPositiveComplexStruStatement.lean#L8-L10
[annih]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Formalism/LocalToGlobal/IndefiniteReal/LocalNewformFunction.lean#L121-L145
[normal]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AbelianVarietyTheory/Proofs/AdelicLatticeProofs/MapFinNeg.lean#L182-L197
