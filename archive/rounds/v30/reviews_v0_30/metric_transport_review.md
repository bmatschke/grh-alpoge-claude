# Independent review of MT1–MT7

**Result: PASS.** No corrections required.

Reviewed text: `metric_transport/main.tex`

SHA-256: `55ac8034b4312f450ceb7be32320e2039cc6a063c89db454159b2fa5bb4142a3`

Source pin: `7cbf7a0c32fca1badf05931879a37c3f8a2b03b4`.

The review independently checked the same-metric identity, the ideal-index normalization, the sign and factor two of the floor error, the complete exceptional-prime support, the scale estimates and the uniform same-family installation. The argument closes the metric-transport implication under its original arithmetic inputs. It does not construct those remaining inputs.

## MT1 — PASS

NuH changes only L, hence space, basis and matrices are literally identical. Iu uses negative integer floors. NprimeDef is an eventual FamP field; ram_idx and place labels match.

Claim SHA-256: `baaaa61445246ab971d4e6d05165469e81baee60f48ebf1c0433b8a03c7d81c8`.

## MT2 — PASS

[M:aM]=Norm(a)^r by local length, with rank measured over K. Source mu= -2 log(covol)/(degree*rank) plus the fixed field term. Fractional ideal reduction and deriving finite generation/nonzero M from N=IM are valid.

Claim SHA-256: `3c7acdf5cb1a2d43ac0d6e9058dd82f65924387647546e137a14a9e28ef3ceb0`.

## MT3 — PASS

Negative ideal exponents give positive 2 sum(lw floor(e*s)) in mu(N)-mu(M). Subtracting sz leaves floor(e*s)-e*s, including s<0. The error is zero at s=0 and nonpositive.

Claim SHA-256: `939c272fc0cca7f903f3f3913714980069b8130892e5bd821276f88393fd46dc`.

## MT4 — PASS

sum e_w f_w=degree yields sum e_w lw=log p; no Galois assumption is needed. ZeroAbove plus F_above gives all support alternatives T,g0,g1,d,prime divisors Delta. Prime logarithm induction and product-of-distinct-primes bound are correct.

Claim SHA-256: `d810d82c6113e825fbd87bb9a741951141adb8ba7a0f5a27dde6cc5182a94aa8`.

## MT5 — PASS

Xpp=Xp*x*n, f=2n, m<=2n, epsilon bounds, N<=eta<=Xp, n<=x^3 and log(fN)<=4x prove fN log(fN)<=8Xpp, hence the stated 10Xpp. Sign of C_Delta is handled with absolute value. Constant 2(log4+5+10|C_Delta|) counts all five unit support costs correctly.

Claim SHA-256: `aba061f95f32606ba7d2b337b8ec881d85a4a2a5feb7689bc0010c99b34abfb0`.

## MT6 — PASS

Uniform thresholds are extracted before x,i,u and joined finitely. TuSize is converted by CTu<=x^(epsilon/100), using FamP L_x,L_eps. Fullness gives finite generation and retained-rank positivity gives nonzero. No union over all words/index sets is assumed finite.

Claim SHA-256: `b05f1842f9c82203b3ecee493a8e41667ecaeb30b6b1223f661167fe986bcab2`.

## MT7 — PASS

topDesWin chooses a single family after the finite Closed threshold join. ChosenE, TuSize, DGamSize and all nine closed conditions attach to that family. Source LinkMu is built from the same LinkDIV, rank and size data. Arithmetic family/link/rank producers remain explicit.

Claim SHA-256: `a696abe927fb77765afea72faed2240e7b24bc94400d1326721f863ce07beab6`.

The review additionally verified 53 cited source ranges in 11 source files directly against the pinned Git objects and the local checkout. No new Lean compilation is claimed.
