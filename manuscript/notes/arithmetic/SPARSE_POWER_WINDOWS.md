# Testing the arithmetic estimate on powers in a window

Fix a primitive Dirichlet character $\psi$. For the RH and Dirichlet GRH endpoints it suffices to produce the arithmetic data on a sparse set of scales. At each tested scale the **signed average** of the discrepancies over the translates suffices. All translates at that scale must use compatible data. The analytic function being bounded uses only the fixed primitive target.

The fixed-power argument and the signed translate mean come from *From theta lifts to the critical line*. We give their transfer to (WB.12)–(WB.25), including a short proof for exceptional powers using a smaller power window. We use the existing one-sided window theorem. This proof works on windows of fixed positive logarithmic stretch. The external paper also treats intervals of fixed multiplicative ratio under further inputs. [Signed mean](https://github.com/Sidler4Hare/alpoge-claude-rh-reconstruction/blob/7d17bb991581172cebd554c33a205b1b0f3a2fb3/sections/arithmetic.tex#L172-L231) · [Fixed powers and the explicit formula](https://github.com/Sidler4Hare/alpoge-claude-rh-reconstruction/blob/7d17bb991581172cebd554c33a205b1b0f3a2fb3/sections/reselected-realization.tex#L334-L418) · [External sparse-exception result](https://github.com/Sidler4Hare/alpoge-claude-rh-reconstruction/blob/7d17bb991581172cebd554c33a205b1b0f3a2fb3/sections/sparse-window-mean.tex#L166-L193)

## A sufficient geometric input for both endpoints

**Theorem.** For a sequence of positive $\varepsilon$ tending to zero, fix an integer $r\ge 1$ and $c>0$, which may depend on $\psi,\varepsilon$. Suppose that on arbitrarily late windows $[Y,Z]$, $Z=Y^{3/2}$, all except at most
$$
 K Z^{-c}\#\{j\in\mathbb N:Y\le j^r\le Z\}
$$
of these powers $x=j^r$ have the following data. Supply the reciprocity, retained-character, thick and thin weight, omitted-character and scalar size conditions of [WB7](../../../research/modules/arithmetic/window_bridge/main.tex#L501-L524) on one common datum at $x$. Replace the arithmetic gap required in (WB.13) by
$$
 \frac1{|A_0|}\sum_{u\in A_0}D_u(x)\ \le\ x^{C\varepsilon}\mathcal B(x),
 \qquad D_u(x)=\sum_{t,j}
  \bigl(\mathcal A(a_t,t,w_{u,j})-\Re\mathcal M(a_t,w_{u,j})\bigr).
$$
Here $\mathcal B$ is exactly the four-term bracket (WB.22), and $C\ge0$ is bounded independently of $\varepsilon$. At fixed $\psi,\varepsilon$ the constants and thresholds are uniform over the windows and tested scales. Then the primitive inducers of all powers of $\psi$ are zero-free in $\Re s>1/2$. The trivial target gives RH. Taking each primitive target gives unrestricted Dirichlet GRH by functional equation and the finite Euler factors.

**Translation average at a good scale.** Write $Q=|T|mb$ as in WB4. Before using the individual discrepancy bound, (WB.8) and the thick and thin errors give
$$
 \sum_{t,j}\Re\mathcal T_u(t,a_t/b)\ \le\ D_u(x)+2Q/x .
$$
Average this inequality over $u$, then apply the exact character orthogonality (WB.15). The result is (WB.16) with $E$ equal to the arithmetic mean of the $D_u$. All later uses of $E$ are upper bounds, so we can use the nonnegative majorant $x^{C\varepsilon}\mathcal B(x)$. WB5–WB6 give
$$
 H_\psi(x)\le x^\alpha,\qquad \alpha=\tfrac12+(C+4)\varepsilon
$$
at every sufficiently large good power. Here $H_\psi=G+(3o+1)^{-1}\sum_{\chi\ne1}\Re G_\chi$ uses the distinct primitive inducers of the powers of $\psi$, with $o$ its order and $G$ the principal ramp. In particular the family and its coefficients are fixed across all samples. With $e_D=2,e_L=0$ the existing arithmetic exponent is $C=5$. [Discrepancy and orthogonality](../../../research/modules/arithmetic/window_bridge/main.tex#L283-L339) · [Fourier extraction and the original exponent](../../../research/modules/arithmetic/window_bridge/main.tex#L424-L497)

**Variation between samples.** Let $\Theta$ be the supremum of the real parts of the nontrivial zeros in this fixed family and its conjugates, counted here as a union. Thus $1/2\le\Theta\le1$. We use the unconditional bound
$$
 |H_\psi(t(1+v))-H_\psi(t)|\ll_\psi t^\Theta |v|^{1/2}
 \qquad(t\ge4,\ |v|\le1/2).
$$
For an individual primitive character set $f(s)=(s-1)^{\mathbf1_{\chi=1}}L(s,\chi)$ and $p=f'/f$. The order-one Hadamard product, with $m_0$ the multiplicity at zero, gives
$$
 \frac{p(1)-p(s)}{s(s-1)}
  =\frac{m_0}{s^2}+
    \sum_{\rho\ne0}\frac{1}{(1-\rho)s(s-\rho)}.
$$
Here $f(1)\ne0$, and the sum includes the trivial zeros with multiplicity. The left side is the Mellin transform on $[1,\infty)$ of the project's centered $G_\chi(t)-G_\chi(1)$. Indeed each ramp contributes $n^{-s}/[s(s-1)]$, and the centering terms cancel the removed pole for the principal character. By uniqueness of Mellin transforms,
$$
 G_\chi(t)-G_\chi(1)=m_0\log t+
           \sum_{\rho\ne0}\frac{t^\rho-1}{\rho(1-\rho)}.
$$
The order-one product gives $\sum_{|\rho|>1}|\rho|^{-3/2}<\infty$; in particular absolute convergence permits transforming this expression termwise for $\Re s>1$. For $0<\Re\rho<1$, the mean-value integral and the trivial bound together give
$$
 |(1+v)^\rho-1|\ll\min(1,|\rho|\,|v|)
                  \ll(1+|\rho|)^{1/2}|v|^{1/2}.
$$
Summing after division by $|\rho(1-\rho)|$ bounds the nontrivial-zero contribution by the claimed modulus. The negative trivial zeros cost $O_\psi(|v|)$ by the mean-value bound $2|\rho|(t/2)^{\Re\rho}|v|$, and the logarithm costs $O_\psi(|v|)$. Take the fixed linear combination. [Ramp definitions](../../../research/modules/arithmetic/window_bridge/main.tex#L85-L104) · [Classical analytic inputs, Koukoulopoulos, Chapters 8 and 11](https://dms.umontreal.ca/~koukoulo/documents/publications/primes.pdf)

**Exceptional powers and a smaller window.** Fix $a$ with $\max(2/3,1-rc)<a<1$, and let
$$
 d=\min\{a/r,\ c-(1-a)/r\}>0 .
$$
There are $O(Z^{1/r-c})$ bad integer indices on the original window. For every real $t\in[Z^a,Z]$, choose a nearest good index to $t^{1/r}$ among the tested indices. Its distance is $O(1+Z^{1/r-c})$, even at the endpoints, since at most that many consecutive indices can be missing and the number of available indices is asymptotic to $Z^{1/r}$. Dividing by $t^{1/r}\ge Z^{a/r}$ and raising to the fixed power $r$ produces a good $s$ with $|s/t-1|\ll Z^{-d}\le t^{-d}$. Thus throughout the smaller window
$$
 H_\psi(t)\ \ll_{\psi,\varepsilon,r,c,K}\ t^\alpha+t^{\Theta-d/2}.
$$
If $\Theta>\alpha$, choose $\gamma$ strictly between $\max(\alpha,\Theta-d/2)$ and $\Theta$. The displayed bound implies $H_\psi(t)\ll t^\gamma$ on arbitrarily late windows with lower endpoint $Z^a$ and fixed stretch $1/a>1$. The [positive window theorem AQ3–AQ4](../../../research/modules/arithmetic/analytic_envelope/analytic_envelope.tex#L97-L105) excludes all family zeros with real part greater than $\gamma$, contrary to the definition of the supremum. Hence $\Theta\le\alpha$. Taking $\varepsilon$ to zero proves the theorem. The argument applies if the supremum is unattained, if it equals one, or if there is a real zero.

For example, taking $\varepsilon=1/q$ along large integers $q$ and $r=2q$ permits testing $x=j^{2q}$, so $x^{1/2}=j^q$ and $x^\varepsilon=j^2$ are exact integers. The field, the rank constraints, all local normalizations and the signed arithmetic estimate must still be realized at the good scales. Between good scales the argument compares only values of the same $H_\psi$. The theorem proves a weaker sufficient route to the endpoints; it leaves the full selected-family assertions separately recorded in the [endpoint inventory](../../../research/register/SELECTED_FAMILY_CHECKPOINT.json).
