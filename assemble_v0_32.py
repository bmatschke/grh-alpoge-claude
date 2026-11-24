#!/usr/bin/env python3
"""Append the v0.32 proof chapters; keep historical mathematical text unchanged."""
from pathlib import Path
import json,re
ROOT=Path(__file__).resolve().parent;OLD=ROOT/'history/version_0_31'
cfg=json.loads((ROOT/'increment_v0_32.json').read_text());count=cfg['expected_new_claims']
s=(OLD/'RH_readable_reconstruction_v0_31.tex').read_text()
s=s.replace('working version 0.31','working version 0.32').replace('Working version 0.31','Working version 0.32')
s=s.replace('Compatible producers and completed finite arguments','Actual size and rank, local operators, and the theta frontier',1)
s=s.replace('A refined completion audit with 41 new proof claims',f'A refined completion audit with {count} new proof claims',1)
a=s.index(r'\textbf{What version 0.31 achieves.}');b=s.index(r'\end{minipage}',a)
s=s[:a]+r'''\textbf{What version 0.32 achieves.}
This version proves the original construction-class \texttt{TuSize}
and \texttt{RankM} inputs, the exact row-degree installation, and the
specified local Hecke and congruence-length calculations. It also
reduces the base theta square to a smaller, precisely stated
common-bundle producer, including a proof of integral convergence.

The design cut now retains the actual common-family construction.
The global-slope cut retains the three original GL4 slots and the
final assembly, with compatible second-layer forms still upstream.
The actual base readings, smooth cuspidal extensions, rational tests
and base rows remain explicit. RH retains I/II/V; unrestricted
Dirichlet targets additionally retain III.

All historical mathematical chapters, source arrays and claim
dependencies remain. The current audit determines which old frontier
statements have been superseded in their exact scopes.
We accept the underlying Lean proof as fully checked and correct.
This remains \textbf{a partial human reconstruction}; no new Lean
build or kernel replay is claimed.
''' +s[b:]
def mono_breaks(m):
 body=re.sub(r'(?<=[a-z])(?=[A-Z])',lambda _:r'\allowbreak ',m[1])
 body=re.sub(r'\.(?!\\allowbreak)',lambda _:r'.\allowbreak ',body)
 body=re.sub(r'([/:])(?!\\allowbreak)',lambda m:m[1]+r'\allowbreak ',body)
 body=re.sub(r'\\_(?!\\allowbreak)',lambda _:r'\_\allowbreak ',body)
 return r'\texttt{'+body+'}'
def wraps(t):
 t=re.sub(r'\\texttt\{([^{}]*)\}',mono_breaks,t)
 # Formatting only: the current register contains long source identifiers
 # outside monospace too. These break points change no mathematical text.
 t=re.sub(r'\\_(?!\\allowbreak)',lambda _:r'\_\allowbreak ',t)
 return re.sub(r',(?=[A-Za-z])',lambda _:r',\allowbreak{} ',t)
marker=r'\section{Current dependency audit: compatible producers and completed consumers}'
assert s.count(marker)==1
s=s.replace(marker,wraps((ROOT/'dependency_audit_v0_32/main.tex').read_text())+r'''

\paragraph{Historical version-0.31 audit.}
The following audit is retained as a historical checkpoint.
Section~\ref{sec:dependency-audit-v32} and the version-0.32 additive
scope updates specify the current remaining producer obligations.
Its previous conditional proofs retain their original hypotheses.

'''+marker,1)
marker=r'\section{Why simultaneous local exceptions have product size}'
assert s.count(marker)==1
addition='\n\n'.join((ROOT/c/'main.tex').read_text() for c in cfg['components'])+'\n\n'
old_display=r''' X_u=\frac1{fk}\log\frac{D_*}{d_*(u)},\quad
 \ell=\log(v/\pi),\quad G=\log(g_0g_1),\quad
 A_m=(m-1)k+\frac{m(m-1)}2,\quad
 B_m=\frac{m(2k+m-1)}2.'''
new_display=r''' \begin{gathered}
 X_u=\frac1{fk}\log\frac{D_*}{d_*(u)},\quad
 \ell=\log(v/\pi),\quad G=\log(g_0g_1),\\
 A_m=(m-1)k+\frac{m(m-1)}2,\quad
 B_m=\frac{m(2k+m-1)}2.
 \end{gathered}'''
assert addition.count(old_display)==1
addition=addition.replace(old_display,new_display)
inline=r'd\pi(X)\pi(g)=\pi(g)d\pi(\operatorname{Ad}(g^{-1})X)'
assert addition.count(r'\('+inline+r'\)')==1
addition=addition.replace(r'\('+inline+r'\);',r'\['+inline+r';\]')
s=s.replace(marker,wraps(addition)+marker,1)
a=s.index(r'\section{The arithmetic still to be written out}');b=s.index(r'\section{Claim ledger and reading order}',a)
remaining=r'''\section{The arithmetic still to be written out}\label{sec:remaining}

Section~\ref{sec:dependency-audit-v32} is the current complete
selected audit. The original final theorem interface remains one
compatible design and nine closed predicates. The construction-class
size and rank proofs, original $h_3$, and the specified GL6 local
calculations are now available on their exact original inputs.

\begin{description}[style=nextline]
\item[The common construction and its actual readings.]
Construct the original recursive core and one compatible family with
its Bundle and duties. Supply its actual base rows, geometric theta
reading, smooth cuspidal base extension, simultaneous rational tests,
and local \texttt{NBuilt}/\texttt{NdSpec}. The finite rank, coverage,
and base-theta consequences do not create those producer data.
BTH13--BTH15 prove the actual finite Weil normalization, including
the comparison with the canonical action on the original theta space.
\item[The local arithmetic and spectral estimates.]
Complete original \texttt{LinkN}, retained defect, period height,
local gain and spectral bounds, including their prescribed
coefficient-field readings, on the same selected family.
\item[The remaining global branch.]
Construct the common original second-layer selector and class duties.
The new local calculations then supply the actual ramified inclusion
and length. Reconstruct the three original GL4 slots---the
\texttt{ColVal} dictionary, lower slope and class-map upper slope---
and the final numerical/lattice assembly. The full global theorem
has not been inferred just from the completed local slots.
\item[The original arithmetic counts.]
RH and power-of-two-order targets retain I, II and V. CountII requires
all six \texttt{HidaPropsAlt} fields and \texttt{P1core} on the
same ideal of both original Links after one threshold. CountI and
CountV retain their distinct fields and prime scopes. Unrestricted
Dirichlet targets additionally require Case III, SeedIV and the
original chain construction.
\end{description}

The next substantial priority is the actual common row/theta
producer; the next bounded global branch is GL4 followed by final
assembly. The same-ideal ordinary support branch should proceed in
parallel. AQ remains an alternative conditional endpoint requiring
its own arithmetic envelope. The historical RF16 correction in DEX11
remains in force; no historical proof bytes have been changed.

'''
s=s[:a]+wraps(remaining)+s[b:]
start=s.index(r'\section{Claim ledger and reading order}');end=s.index(r'\end{longtable}',start)
rows=r'''
DSZ1--DSZ10 & Actual degree and prime size & Exact original h3, harmonic upper comparison and construction-class TuSize.\\[3pt]
RMP1--RMP11 & Original class number and rank & Self-dual enlargement, actual local indices, mass, Mu0Tie and construction-class RankM.\\[3pt]
BTH1--BTH15 & Original base theta reduction & Integral convergence, actual Weil normalization and exact Hilbert/finite/rational consumer, with common producer inputs explicit.\\[3pt]
GLE1--GLE12 & Original local Hecke and length & Late setting, actual integral and ramified maps, exact second branch and composite bound.\\[3pt]
'''
s=s[:end]+rows+s[end:]
a=s.index('Start with the version-0.31 audit in',start)
b=s.index('including the explicit RF16 correction.',a)+len('including the explicit RF16 correction.')
s=s[:a]+r'''Start with the version-0.32 audit in
Section~\ref{sec:dependency-audit-v32}. Read DSZ and RMP for the
newly completed construction-class size and rank arguments; GLE for
the original local calculations; and BTH for the smaller actual base
theta producer. DEX, SLR, LTD and RSL give their earlier finite
interfaces. HX/MT/KA/ZW give the host, metrics, count aggregation and
numerical endpoint; QX/YX retain the exact conditional Case-II chain.
Historical frontier statements are governed by the current audit and
additive scope updates, including the preserved RF16 correction.''' +s[b:]
s=s.replace('with version-0.31 updates where an input','with version-0.32 updates where an input')
out=ROOT/'RH_readable_reconstruction_v0_32.tex';out.write_text(s)
print(out.name,len(s.encode()),'bytes; historical mathematical chapters retained.')
