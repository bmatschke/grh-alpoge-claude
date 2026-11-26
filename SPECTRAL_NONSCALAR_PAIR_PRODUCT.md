# The product of the two orbital bounds at generic corank one

Fix a represented nonscalar generic pair of corank one on a tied row for the ordered words $u,u'$. Use $r=r_S$, $\ell=r+1$, $m=2\ell$, $T=T_u$, $T'=T_{u'}$, $g=g_0g_1$, and let $f$ be the number of CM-type embeddings. Both terms have the same incoming and outgoing words. We prove a bound for their product using both angular factors at once. This also retains the norm of a nonzero algebraic integer attached to the pair.

## The integral entry on the two-dimensional quotient

Let $\begin{pmatrix}a&b_1\\ c_1&d_1\end{pmatrix}$ be the transfer on the two normal coordinates furnished by the integral flag comparison at generic corank one. It preserves $T|u_1|^2-T'|u_2|^2$ at every complex embedding, carries

$$
  \mathcal L_g=\{(x,y)\in\mathcal O_E^2:x+y\in g\mathcal O_E\}
   \quad\text{into itself},
$$

and has $c_1/T,(a-1)/T$ integral locally at primes over $T$, and $b_1/T',(d_1-1)/T'$ integral locally over $T'$. These assertions use generic saturation for both flags, the common definite hyperplane and the prescribed level congruences. In the flag comparison the normal lines agree modulo the fixed isotropic spaces. Expressing each pair of lifts in its two coefficient coordinates gives the transfer. The integral gluing gives the lattice and the local conditions above, and taking Hermitian norms gives preservation of the form. [Normal-coordinate construction][normal] · [Local gluing and global level congruences][glue] · [Transfer and Hermitian form][form]

The image of $(g,0)$ gives $gc_1\in\mathcal O_E$. Consequently $\xi=gc_1/T$ is integral at every prime. Away from $T$ the denominator is a unit, and at primes dividing $T$ we use $c_1/T$ directly. On this pair $\xi\ne0$. Indeed preservation of the form gives $T|b_1|=T'|c_1|$ at each place. If $c_1=0$, the matrix would be diagonal with both diagonal entries of absolute value one everywhere. Its action on $(1,-1)$ makes them integral. The local congruences then give $(a-1)/T,(d_1-1)/T'\in\mathcal O_E$. Each has all conjugates of modulus at most $2/3$ because $T,T'\ge3$. Its absolute algebraic norm is therefore less than one, forcing it to vanish. The identity transfer gives a scalar pair by the defining normal-line comparison. Write $D_p=|\mathrm N_{E/\mathbf Q}\xi|\ge1$. [Integral conditions][int] · [Identity transfer gives a scalar pair][identity]

For term $i=1,2$ at a place $\tau$ with nonzero penultimate minor use the positive hyperbolic sine $x_{i\tau}$ from the [angular calculation](SPECTRAL_ANGULAR_FROM_ORDINARY_AMPLITUDE.md), and put

$$
 B_{i\tau}=1/x_{i\tau},\quad
 A_{i\tau}=\sqrt{1+x_{i\tau}^2}/x_{i\tau},\quad
 z_{i\tau}=\min(1,x_{i\tau}).
$$

At a zero minor put $B=0$, $A=z=1$, as in the arithmetic place formula. With $X_\tau=A_{1\tau}B_{2\tau}+B_{1\tau}A_{2\tau}$ the transfer satisfies $\sqrt{T'/T}\,|\tau c_1|\le X_\tau$. This follows by expressing the lower-left transfer entry in the two orthogonal normal frames, bounding the two summands by the products of their normalized diagonal and off-diagonal entries. Taking products and using the norm of $\xi$ gives

$$
  (\sqrt{TT'}/g)^f\sqrt{D_p}\le\prod_\tau X_\tau,\qquad
  \prod_\tau z_{1\tau}z_{2\tau}
     \le (2\sqrt2\,g/\sqrt{TT'})^f D_p^{-1/2}.                 \tag{1}
$$

Indeed $zB\le1$ and $zA\le\sqrt2$ in every case, so $z_1z_2X\le2\sqrt2$ locally. With one vanishing penultimate minor this bound is $1$ at every place, since the minor is an algebraic number and the corresponding $X$ is the other $B$. Two zero minors would give $X=0$ and are excluded by (1). [Lower-left entry estimate][entry] · [Original zero-minor conventions][zero]

## The two angular factors

Use the hypotheses and the first angular bound (4) of the [local orbital estimate](SPECTRAL_ANGULAR_FROM_ORDINARY_AMPLITUDE.md). Put $\lambda=(C/k)^{2r(1-\delta)}$, where $1\le C\le k^{1/3}$ and $0\le\delta\le1/4$. Then $k^{-2r}\le\lambda\le k^{-r}$. At place $\tau$ put $a_\tau=T_{\rm crit,\tau}(u')/T'$. The critical-scale lower bound is $a_\tau T'g^{-m}\ge k^{3r}$. If the minor is nonzero the minimum in the angular bound is $U_{i\tau}=\min(1,a_\tau T'g^{-m}\lambda x_{i\tau}^2)$. It is $1$ at a zero minor. In both cases,

$$
              a_\tau^{-1}U_{i\tau}\le T'g^{-m}\lambda z_{i\tau}^2 .
                                                                  \tag{2}
$$

For $x<1$ use the second argument of the minimum. For $x\ge1$ and the zero-minor branch use $1\le a_\tau T'g^{-m}\lambda$. The same comparison with $1$ is valid on each side independently.

Let $h_i,\sigma_i,n_i$ be its arithmetic height, size and Gram normalizer. Put $A_i^{\rm orb}=a_{t_i}/\sqrt{d_\infty}$, the amplitude divided by the square root of the incoming compact dimension. Apply the local squared estimate to each term, take both square roots, and use (2) at every place. In the product the square roots of the two factors $z_i^{2k}$ give $(z_1z_2)^k$. By (1) and the [arithmetic orbit-volume estimate](SPECTRAL_ARITHMETIC_ORBIT_VOLUME.md),

$$
 \sqrt{n_1n_2}\,A_1^{\rm orb} A_2^{\rm orb}
 \le (h_1h_2)^{c r^2}\,\Gamma e^{2C_2m^6 f\log b}
   (\sigma_1\sigma_2)^{a_2/2-q/\ell}
   [2\sqrt2\,\sqrt{T'/T}\,g^{1-m}\lambda]^{kf}D_p^{-k/2},       \tag{3}
$$

where $a_2=C_2(m^2+2m^4)$. Take $c$ large enough for the individual volume and count constants. The compact dimensions and the local Haar units in (3) are the same as in the [higher-corank sum](SPECTRAL_HIGHER_CORANK_PAIR_SUM.md). The per-place critical factors $a_\tau$ have cancelled before the sums over the labels. Both words share the same finite prime ratio throughout. With one zero minor $2\sqrt2$ in (3) may be replaced by one. In particular (3) applies even if the smaller of the two nonzero hyperbolic sines belongs to a different term at different embeddings.

One can keep the critical scale of each place in the constant. Write $B_\tau^*=a_\tau T'g^{-m}\lambda\ge k^r$ and $w_i=\sqrt{U_{i\tau}}$. At a nonzero minor $w_i B_i\le\sqrt{B_\tau^*}$ and $w_i A_i\le\sqrt{1+B_\tau^*}$, by separating $x_i^2\le1/B_\tau^*$ from $x_i^2\ge1/B_\tau^*$. Hence $w_1w_2 X_\tau\le2\sqrt{B_\tau^*(1+B_\tau^*)}$. If one minor vanishes, its $w=A=1$ and $B=0$, so $w_1w_2 X_\tau\le\sqrt{B_\tau^*}$. Multiply over the places, divide by the lower bound on $\prod X_\tau$ and by $\prod a_\tau$, then raise to the power $k$. This replaces $(2\sqrt2)^{kf}$ in (3) by

$$
 \prod_\tau [2\sqrt{1+1/B_\tau^*}]^k
 \quad\text{or, with one zero minor,}\quad
 \prod_\tau (B_\tau^*)^{-k/2}\le k^{-rkf/2}.
$$

These constants apply to the two respective classes before summation.

## Summation on the arithmetic row

The [two ordered frame counts](SPECTRAL_CORANK_ONE_FRAME_COUNTS.md) and symmetry give the weighted number of pairs with fixed labels, per unit row mass, at most $c^f(h_1h_2)^{3cr^2/2}\sqrt{n_1n_2}$. Take the geometric mean of the bounds obtained by fixing a first or second frame. Cauchy–Schwarz, as in the higher-corank sum, now cancels both Gram normalizers in (3). Restricting to pairs with $D_p\ge D_0\ge1$ retains the factor $D_0^{-k/2}$. With $h_i\le P\sigma_i^4$ take

$$
 q=\left\lceil\ell\left(10cr^2+a_2/2+12\ell^2\right)\right\rceil .
$$

Indeed the total exponent on $h_1h_2$ is $5cr^2/2$, leaving $-12\ell^2$ on each label after conversion. This moment is below the source's choice with $12cr^2$ in place of $10cr^2$ and hence within the allowed eventual range. The two packing sums cost at most $(27^f P^3)^{2\ell^2}$. Using $\Gamma_1 M d_\infty\le d_u^S$, $\log P=O(m^3 f\log b)$, $m\le f$ and the rank threshold in the higher-corank note gives, for a fixed constant $K$,

$$
 \Gamma_1\sum_{\substack{p\ {\rm nonscalar,\ generic}\\s(p)=1,\ D_p\ge D_0}}
       |\langle v_{t_1},v_{t_2}\rangle|
 \le d_u^S e^{Kkf}
     [2\sqrt2\,\sqrt{T'/T}\,g^{1-m}\lambda]^{kf}D_0^{-k/2}.     \tag{4}
$$

Taking the supremum over finite subsets proves absolute summability on this class. On the tied dimension window $1/R'\le C_0\Gamma^2$, $\Gamma^2\le e^{O(kf)}$, $T'/T$ is bounded, $g\ge k^8$ and $\lambda\le k^{-r}$. Thus (4) at $D_0=1$ fits the $d_u^SR'e^{-kf\log k}$ allowance eventually. The hypotheses for (4) include the matched local wave, one-step period, cofactor, Haar and size data. The scalar and nongeneric corank-one pairs have their own signed estimates. The integral entry and the suppression by $D_p$ concern the generic nonscalar class. [Original small-side estimate][comparison] · [Its role in the mixed operator][role]

[normal]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Formalism/SharpRestriction/CuspSpanNormBounds/LatticeGluingRadicals.lean#L3353-L3434
[glue]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Formalism/SharpRestriction/CuspSpanNormBounds/LatticeGluingRadicals.lean#L4348-L4460
[form]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Formalism/SharpRestriction/CuspSpanNormBounds/LatticeGluingRadicals.lean#L3177-L3226
[int]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Formalism/FlagUnipotentLattices/DetIndexProductHyperbolicInequality.lean#L126-L148
[identity]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Formalism/SharpRestriction/CuspSpanNormBounds/LatticeGluingRadicals.lean#L3160-L3175
[entry]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Formalism/SharpRestriction/CuspSpanNormBounds/LatticeGluingRadicals.lean#L3132-L3158
[zero]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Formalism/SharpRestriction/CuspSpanNormBounds/CayleyDegreeNondegeneracy/RowsTrm.lean#L945-L1029
[comparison]: https://github.com/rh-lean-roadmap/rh-lean-roadmap/blob/dc5594a62bb2b94139788df817db693cd939a046/docs/src/book/main.tex#L17884-L17909
[role]: https://github.com/rh-lean-roadmap/rh-lean-roadmap/blob/dc5594a62bb2b94139788df817db693cd939a046/docs/src/book/main.tex#L46022-L46048
