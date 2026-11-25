# The CM polarization determines the theta line

On the interior of the moduli problem, the choice of a theta line has a canonical answer. Let $p:A\to S$ be an abelian scheme with an action $\iota$ of the CM order $\mathcal O_E$. Giving the polarization and line-bundle data in the source's proper object is equivalent, up to unique rigidified isomorphism over the given $A$, to giving a principal polarization $\lambda:A\to A^\vee$ for which complex conjugation is the adjoint of the CM action. The construction works in families and commutes with arbitrary base change. Its special ingredient is an element $w_0\in\mathcal O_E$ of trace one over the real subfield. Indeed $2w_0=1+\sqrt{-d}$ and complex conjugation negates $\sqrt{-d}$, so $w_0+\bar w_0=1$. The source proves that the group of every proper object here is an abelian scheme. [Host and theta data][sab] · [Abelian-scheme property][abelian]

## Recovering a line from a polarization

Let $\mathcal P$ be the Poincaré line on $A\times_S A^\vee$, normalized along both zero sections. Write $B_\lambda(x,y)=\mathcal P(x,\lambda y)$, and let $a=\iota(w_0)$. These expressions denote pullbacks of line bundles and can be evaluated on points over every test scheme. The bundle $B_\lambda$ is a symmetric biextension. This means that its two variables are additive under tensor product, and that interchanging the variables gives a canonical isomorphism. The Rosati condition $\iota(c)^\vee\lambda=\lambda\iota(\bar c)$ gives $B_\lambda(\iota(c)x,y)\simeq B_\lambda(x,\iota(\bar c)y)$. Define the rigidified line on $A$ by
$$
L_\lambda(x)=B_\lambda(x,ax).
$$

To calculate its polarization, take the second difference $D_2L(x,y)=L(x+y)\otimes L(x)^{-1}\otimes L(y)^{-1}\otimes L(0)$. The rigidification identifies the last factor with the trivial line. The two mixed terms give
$$
\begin{aligned}
D_2L_\lambda(x,y)
&\simeq B_\lambda(x,ay)\otimes B_\lambda(y,ax)\\
&\simeq B_\lambda(x,ay)\otimes B_\lambda(x,\iota(\bar w_0)y)\\
&\simeq B_\lambda(x,y).
\end{aligned}
$$
The universal property of the dual abelian scheme identifies $D_2 L$ with $(1\times\phi_L)^*\mathcal P$, where $\phi_L(y)$ is represented by $t_y^*L\otimes L^{-1}$. Thus $\phi_{L_\lambda}=\lambda$. The ordinary diagonal $x\mapsto(x,x)$ gives $2\lambda$ by the same calculation. The trace identity explains precisely why the source uses the graph of $w_0$. [Lan, Construction 1.3.2.7 and Lemma 1.3.2.13][lan] · [Sign of the source's second difference][cube]

The same calculation supplies the source's two line identities. Moving $\iota(c)$ between the variables gives `adj`. Restricting $D_2L_\lambda=B_\lambda$ to the graph of $a$ gives `prim`. Bimultiplicativity gives $L_\lambda(-x)\simeq L_\lambda(x)$ with its rigidification. Moret-Bailly’s theorem of the cube gives the unique normalized cubical structure on a rigidified line over an abelian scheme. The source's trivializations on the three zero faces, its two transpositions, and its cocycle are the normalization, symmetry and cocycle of this theorem. [Moret-Bailly, *Pinceaux de variétés abéliennes*, I.2.6][mb] · [Lan, Proposition 3.2.3.1][lan] · [Cubical structure][cube]

## Recovering the polarization and its morphisms

Conversely, for the source's line $L$ take $\lambda=\phi_L$. Its relative ampleness makes $\lambda$ a polarization, hence an isogeny. The kernel has a concrete test. For an affine $T\to S$, a point $x\in A(T)$ maps to zero precisely when $t_x^*L_T\otimes L_T^{-1}$ comes from a line on $T$. This follows by rigidifying the difference along zero and applying the defining property of $A^\vee$. Equivalently the difference is trivial on $A_V$ for an open cover of $T$ by $V$. Thus `KTriv` says exactly that the kernel group scheme is trivial, and $\lambda$ is principal. Affine tests include nonreduced rings and detect the whole kernel. In the forward direction $L_\lambda$ is ample on each geometric fiber since it induces the given polarization there. Relative ampleness follows by the fiber criterion for proper morphisms of finite presentation. Over each affine base open a sufficiently high power gives a closed immersion into projective space. Its coordinate sections and their ratios give the affine charts and ring generators in the source's `RelAmple`. [Definitions of ampleness and kernel][kernel] · [Lan, Proposition 1.3.2.15][lan]

Now $D_2L=B_\lambda$. By the universal property of $\mathcal P$, the identity `adj` of line bundles gives $\iota(c)^\vee\lambda=\lambda\iota(\bar c)$. The identity `prim` then identifies $L$ with $(1,a)^*B_\lambda=L_\lambda$. It asserts existence of an isomorphism. Normalize such an isomorphism at zero by multiplying by a unit from $S$. It is then unique because $p_*\mathcal O_A=\mathcal O_S$ universally, so every unit on $A$ comes from $S$. In particular, twisting $L$ by a rigidified algebraically trivial line preserves $D_2L$, and the graph identity forces that twist to be trivial. This explains how the moduli problem resolves the usual ambiguity in choosing a symmetric theta line. [Meaning of the line isomorphism][iso]

For an isomorphism of CM abelian schemes $A'\simeq A\times_S S'$ preserving the polarization, functoriality of $\mathcal P$ carries the pulled-back graph construction to $L_{\lambda'}$. Its unique rigidified isomorphism preserves the normalized cube. Conversely, pulling back the line and taking $D_2$ recovers compatibility of polarizations. In the source the map on triple products is forced by its three coordinate projections, and `lin` asks for existence of the compatible rigidified cubical isomorphism. There is no extra scalar automorphism. The remaining morphism conditions on the two marked sections are exactly their stated pullback equalities. [Cubical maps and rigidifications][map] · [Maps of polarized objects][objmap] · [Maps of marked objects][objects]

This settles the line-bundle comparison for families on the interior. On a complex period torus it recovers the line of PUN20 by uniqueness. The sign of the commutator pairing for the marked level uses the calculation in PUN21. The [fine moduli comparison](PEL_MODULI_COMPARISON.md) supplies the interior family with both markings and its tangent signatures. [Period torus and pairing](principal_uniformization_v48/main.tex#L930-L1086)

[lan]: https://www.kwlan.org/articles/cpt-PEL-type-thesis-revision-dense.pdf
[mb]: https://numdam.org/item/AST_1985__129__1_0/
[sab]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/ReciprocityTheory/ReductiveGroups/ArithmeticGeometry/BirationalGeometry/ToroidalCompactification/TwoWeightEqOneAddRoot.lean#L14-L82
[abelian]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AbelianVarietyTheory/Proofs/ModuliProofs/ObjIsAbelianSchemeDimRigidifiedSym.lean#L232-L240
[cube]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/ReciprocityTheory/ReductiveGroups/ArithmeticGeometry/SemiabelianSchemes/CubicalStructures/CubeSymmetricSwapFirst.lean#L144-L187
[kernel]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/ReciprocityTheory/ReductiveGroups/ArithmeticGeometry/ExtensionDescent/NonzeroLocus.lean#L33-L57
[iso]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/ReciprocityTheory/ReductiveGroups/ArithmeticGeometry/BirationalGeometry/ToroidalCompactification/IsGrpPullback.lean#L26-L42
[map]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/ReciprocityTheory/ReductiveGroups/ArithmeticGeometry/SemiabelianSchemes/CubicalStructures/CubicalPullBaseChangeSt.lean#L34-L99
[objmap]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/ReciprocityTheory/ReductiveGroups/ArithmeticGeometry/BirationalGeometry/ToroidalCompactification/TwoWeightEqOneAddRoot.lean#L86-L91
[objects]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/ReciprocityTheory/ReductiveGroups/ArithmeticGeometry/BirationalGeometry/ToroidalCompactification/TwoWeightEqOneAddRoot.lean#L144-L166
