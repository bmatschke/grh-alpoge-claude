# A degree-weighted intersection bound suffices on the nonterminal rows

Use the fitted cover of period entry 7, its nonterminal components $Z$, the weight $v=u'=u_1-3n\eta_H$, and its cutoff $N=\lfloor B(v,g)\rfloor$. The arithmetic target can retain the geometric weights on its components throughout. This removes the separate proof of equality of all component volumes from this particular path to the endpoint. It also removes one loss from comparing the two geometric degrees. The argument assumes the individual geometric degree identification, the model-to-record comparison, and the height and determinant inequalities specified below.

## The intersection measured by the model

Let $P_{N,Z}$ be the component arithmetic intersection functional, including the division by the field degree and by the generic degree of the model over the flag function field. Write $V_Z>0$ for the geometric factor normalized in the same way. For the actual weight put $H_v=(d+1)\delta_{\rm fl}(v)>0$, $d=d_{\rm fl}$, $F=L_v^{d+1}$ and $V=\sum_ZV_Z$. The model slope is $a_Z=P_{N,Z}(F)/(V_Z H_v)$. Therefore
$$
 \frac{\sum_Z V_Za_Z}{V}
   =\frac{P_N(F)}{V H_v},\qquad P_N=\sum_ZP_{N,Z}.                 \tag{1}
$$
This uses only positivity and the definitions. Roadmap B8.26c obtains its lower bound on the right side by applying the cutoff decomposition B8.26b to $F$, including the error from higher power sums. Its last use of equal volumes rewrites (1) as an unweighted mean. For the following argument it suffices to establish this total intersection estimate directly at the single indicated weight and cutoff. The first part of the geometric proportionality comparison gives $\Delta'_Z=\deg_Z(v)$ as the same positive multiple of $V_Z$ for every $Z$. Indeed it evaluates the geometric top intersection at $L_v^d$ after the individual generic-degree normalization, giving $V_ZD(L_v^d)$ in the tower's common convention. The arithmetic root-line extensions at the finite places still matter for the numerator of (1). [Definition of the component slope](https://github.com/rh-lean-roadmap/rh-lean-roadmap/blob/dc5594a62bb2b94139788df817db693cd939a046/docs/src/book/main.tex#L20053-L20066) · [Geometric proportionality before the volume equality](https://github.com/rh-lean-roadmap/rh-lean-roadmap/blob/dc5594a62bb2b94139788df817db693cd939a046/docs/src/book/main.tex#L49964-L49976) · [Cutoff estimate and final averaging](https://github.com/rh-lean-roadmap/rh-lean-roadmap/blob/dc5594a62bb2b94139788df817db693cd939a046/docs/src/book/main.tex#L50917-L50950)

On a smooth toroidal compactification of a supplied marked component with its canonical Hodge bundles, this geometric proportionality can also be checked directly. Take the full flags in the two Hodge blocks at each embedding. Successive projective bundle pushforwards send the top power of the root line on this flag bundle to a top-degree polynomial in the Chern classes of its Hodge bundles. The polynomial is universal for the specified block ranks and weight. The two Hodge factors are representations of the Levi of the compact-dual parabolic, so its unipotent radical acts trivially, as Mumford requires. His proportionality theorem computes its integral on the base as the invariant volume of that component times its compact-dual integral, with the same curvature convention on every component. For mixed Chern products the same proof applies term by term because the canonical invariant Chern forms are good and their top-degree product is an invariant density. Thus the ratio of these geometric degrees for two components is exactly the ratio of their volumes. The regular positive degree fixes the normalization by testing one component. This verifies the geometric assertion on canonical extensions. For other extensions across the boundary the root-model comparison must still identify their degrees with these, including the normalization by the generic degree of a finite cover. [Mumford, *Hirzebruch's Proportionality Theorem in the Non-Compact Case*, Theorems 3.1 and 3.2](https://www.dam.brown.edu/people/mumford/alg_geom/papers/1977b--HirzProp-GT.pdf#page=25)

Suppose the right side of (1) is at least $-X_0$ and the individual model comparison gives $\nu_Z(v;B)\ge a_Z-c$ at all $Z$. In B8.26d the common cost is $c=2c_2(B)\|v\|_1$. Then $s_Z=a_Z-c$ satisfies
$$
 s_Z\le\nu_Z(v;B),\qquad
 \frac{\sum_Z\Delta'_Zs_Z}{\sum_Z\Delta'_Z}\ge-X,\qquad X=X_0+c .
                                                                    \tag{2}
$$
One can also use (2) directly, for example with a degree-weighted bound on unequal comparison costs. The source's cost estimate for $v$ has $T\mathcal E_{\ell(D)}(v,g)=O(E_p)$. [Trace transfer and local cost](https://github.com/rh-lean-roadmap/rh-lean-roadmap/blob/dc5594a62bb2b94139788df817db693cd939a046/docs/src/book/main.tex#L50607-L50627) · [The actual shifted weight and size budget](https://github.com/rh-lean-roadmap/rh-lean-roadmap/blob/dc5594a62bb2b94139788df817db693cd939a046/docs/src/book/main.tex#L53741-L53759)

## The comparison with the period height

Write $\Delta_Z$ for the degree of the image at $u_1$. The individual moving-degree comparison is $(1-\rho)\Delta_Z\le\Delta'_Z\le\Delta_Z$. Write $h_Z$ for the normalized Petersson Chow height, $c_s\ge0$ for the coarse generator cost and $c_c\ge0$ for the multiplication and local comparison costs. The componentwise small-section injection, nef arithmetic Hilbert–Samuel formula and Chow-height comparison give equation (8.28f) of the Roadmap, hence
$$
 \Delta_Z(h_Z+c_s+c_c)\ge\Delta'_Z(s_Z+c_s)
$$
after letting its arbitrarily small slack tend to zero. Sum before dividing. With $\sigma=(\sum_Z\Delta'_Z)/(\sum_Z\Delta_Z)\in[1-\rho,1]$, (2) gives
$$
 \frac{\sum_Z\Delta_Z(h_Z+c_s)}{\sum_Z\Delta_Z}
 \ge\sigma(c_s-X)-c_c
 \ge(1-\rho)c_s-X-c_c ,                                         \tag{3}
$$
taking $X\ge0$. The inequality remains valid for either sign of $c_s-X$. In particular the possible negativity of some $s_Z$ does not cost a factor involving the largest or smallest component. [Moving degrees](https://github.com/rh-lean-roadmap/rh-lean-roadmap/blob/dc5594a62bb2b94139788df817db693cd939a046/docs/src/book/main.tex#L20243-L20254) · [Component height comparison](https://github.com/rh-lean-roadmap/rh-lean-roadmap/blob/dc5594a62bb2b94139788df817db693cd939a046/docs/src/book/main.tex#L53770-L53782)

The weight $w_Z$ in the arithmetic determinant lower bound is $\mathcal B\Delta_Z$ with common $\mathcal B>0$. In B8.29 let $a=T-3d-4\ge0$ and retain its common $N_0$. Then $d_Z\ge w_Z[a(h_Z+c_s)-N_0]$ implies directly
$$
 \frac{\sum_Z d_Z}{\sum_Zw_Z}
 \ge a[(1-\rho)c_s-X-c_c]-N_0 .
$$
If useful the square bracket can be replaced by its nonnegative part, since $h_Z+c_s\ge0$ separately. The corresponding original calculation allows $(1-2\rho)c_s-X-c_c$. Thus (3) preserves its full error budget. The rank comparison and the remaining slope descent apply with the same constants whenever their hypotheses are supplied. [Arithmetic degree and subsequent slope descent](https://github.com/rh-lean-roadmap/rh-lean-roadmap/blob/dc5594a62bb2b94139788df817db693cd939a046/docs/src/book/main.tex#L53786-L53813)

For this route the next arithmetic test is to exhibit the limiting functional for the selected normalized flag models and prove $P_N(L_{u'}^{d+1})/(V H_{u'})\ge-X_0$ with $T X_0=O(E_p)$, together with the model-to-record estimate in (2) at that cutoff. B8.26b gives one sufficient identity for that value, in terms of two first-derivative coefficients and the Frobenius correction for higher power sums. The geometric proportionality and $V_Z>0$ alone give no lower bound for $P_N$. [Precise cutoff identity and its coefficient bounds](https://github.com/rh-lean-roadmap/rh-lean-roadmap/blob/dc5594a62bb2b94139788df817db693cd939a046/docs/src/book/main.tex#L20158-L20177)

A metric normalization matters even when all these geometric degrees are known. For example, on the arithmetic line under test replace its norm at every embedding by $e^{-t}$ times that norm. This leaves the geometric degree fixed. By multilinearity the normalized arithmetic top intersection gains $(d+1)t$ times the geometric degree. Indeed the constant metric on the trivial factor contributes $t$ when it occurs once, and the product of two such factors vanishes. Since the geometric degree on component $Z$ is $V_Z\delta_{\rm fl}(v)$, the right side of (1) gains exactly $t$ in the unsquared norm convention. Thus calibrating the actual metric and its comparison with the cusp count is essential for a numerical lower bound.
