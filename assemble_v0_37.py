#!/usr/bin/env python3
"""Add new proof chapters while preserving historical mathematics."""
from pathlib import Path
import json,re
ROOT=Path(__file__).resolve().parent;cfg=json.loads((ROOT/'increment_v0_37.json').read_text())
s=(ROOT/'RH_readable_reconstruction_v0_36.tex').read_text()
s=s.replace('working version 0.36','working version 0.37').replace('Working version 0.36','Working version 0.37')
s=s.replace('Simultaneous theta maps, exact analytic suppliers, and one-point arithmetic','Original pointwise theta maps, selected counts, and common-record assembly',1)
s=s.replace('with 71 new proof claims',f"with {cfg['expected_new_claims']} new proof claims",1)
a=s.index(r'\textbf{What version 0.36 achieves.}');b=s.index(r'\end{minipage}',a)
s=s[:a]+r'''\textbf{What version 0.37 achieves.}
The original smooth representatives, all derivative identities,
fixed-level Sobolev estimates and the full bounded-holomorphic
multiplicity map are now reconstructed. The analytic theta route
retains two initial suppliers: the extremal seed bound and the
target finite pair. Count II has its exact selected first-order
\texttt{B1} on the same witness already carrying
\texttt{Choice/B2}. The finite common-selected realization and
same-$R$ \texttt{Bundle/BWit/BunU} consumers are also proved.

'''+f"There are {cfg['expected_new_claims']} new claims and {1770+cfg['expected_new_claims']} cumulative claims. "+r'''
The selected register retains 34 open coupled leaves:
23 C, 9 B and 2 D. No additional whole selected leaf is closed.
Initial analytic production, common geometry/readings,
local/spectral estimates and original ordinary/automorphic
support remain. RH retains I/II/V; unrestricted Dirichlet GRH
also retains III.

Every historical mathematical proof, source array and dependency
edge is retained. The current audit governs older frontier statements.
The underlying Lean proof is accepted as fully checked and correct.
This remains \textbf{a partial human reconstruction}.
'''+s[b:]
def mono(m):
 b=re.sub(r'(?<=[a-z])(?=[A-Z])',lambda _:r'\allowbreak ',m[1])
 b=re.sub(r'\.(?!\\allowbreak)',lambda _:r'.\allowbreak ',b)
 b=re.sub(r'([/:])(?!\\allowbreak)',lambda m:m[1]+r'\allowbreak ',b)
 b=re.sub(r'\\_(?!\\allowbreak)',lambda _:r'\_\allowbreak ',b)
 return r'\texttt{'+b+'}'
def wraps(t):
 t=re.sub(r'\\texttt\{([^{}]*)\}',mono,t)
 t=re.sub(r'\\_(?!\\allowbreak)',lambda _:r'\_\allowbreak ',t)
 return re.sub(r',(?=[A-Za-z])',lambda _:r',\allowbreak{} ',t)
marker=r'\section{Current dependency audit: simultaneous theta maps and coupled one-point data}'
assert s.count(marker)==1
s=s.replace(marker,wraps((ROOT/'dependency_audit_v0_37/main.tex').read_text())+r'''

\paragraph{Historical version-0.36 audit.}
The next audit is preserved as a historical checkpoint.
Section~\ref{sec:dependency-audit-v37} and the version-0.37
scope updates state the current remaining obligations.
Historical conditional proofs retain their hypotheses.

'''+marker,1)
marker=r'\section{Why simultaneous local exceptions have product size}'
assert s.count(marker)==1
s=s.replace(marker,wraps('\n\n'.join((ROOT/c/'main.tex').read_text() for c in cfg['components']))+'\n\n'+marker,1)
a=s.index(r'\section{The arithmetic still to be written out}');b=s.index(r'\section{Claim ledger and reading order}',a)
s=s[:a]+r'''\section{The arithmetic still to be written out}\label{sec:remaining}

Section~\ref{sec:dependency-audit-v37} states all 34 remaining
selected contracts. The following priorities reflect the exact
remaining original producers.

\begin{description}[style=nextline]
\item[Initial theta boundedness and target volume.]
Supply the original target \texttt{FinPair} and the bound on
the initial extremal theta function. The same-quotient regular
representation, smooth representatives, every derivative,
fixed-level Sobolev growth/evaluation, complete original
\texttt{IsMultMap}, lowest-type restriction and linear theta
assembly are now proved after these inputs. Check any published
rapid-decay application against the source's exact smoothness,
cusp, center, level and uniform-derivative hypotheses.
\item[The actual common realization.]
The original finite columns, one common \texttt{ReadC}, exact
period/evaluation placement, scalar/error transports,
\texttt{RealIn/RealTB}, row-side and \texttt{Bundle/BWit/BunU}
consumers are complete. Construct their common geometry and
readings, host/frames, \texttt{MultEq} support, exact updated
\texttt{DivDef3}, eigensystem/parts and all-embedding
\texttt{logLam}, \texttt{HD/d3b}, and \texttt{NEb}.
Keep the actual rational tests, base rows and second-layer
selection; record assembly does not produce them.
\item[Local and global quantitative suppliers.]
Construct the original \texttt{NBuilt/NdSpec} installation
and projection square, denominator and retained-defect bounds,
period-height comparison, local gain and normalized spectral
estimates on the common family. The full global loss and
final assembly consumers remain reconstructed.
\item[Original arithmetic support.]
The same selected $h=0,a=n=4,g=0$ witness now has
\texttt{Choice/B1/B2}, with the exact $4[L^+:\mathbb Q]+4q$
first-order exponent. Retain the original ordinary/control
and arithmetic-fiber producer, type/neat level and
\texttt{TThetaEx}, four Hida endpoints, all-level same-$J$
\texttt{HasAut}, and the exact $h=0$ \texttt{Raw} propagation.
Complete \texttt{CohP/LocCFT} and all local guards remain.
Both rank-four Links use fixed $\iota$, $\ell=3$ and one
common coefficient threshold. RH retains I/II/V;
unrestricted Dirichlet GRH also retains III, SeedIV and chains.
\end{description}

The source-anchored continuation notes identify the next
smallest suppliers. They are work plans, not closure claims.
The optional AQ route and DEX11 correction of historical RF16
remain in their established scopes.

'''+s[b:]
start=s.index(r'\section{Claim ledger and reading order}');end=s.index(r'\end{longtable}',start)
rows=r'''
ASB1--ASB14 & Original adelic Sobolev producer & Actual chart, rational count, same-measure unfolding and one fixed-level exponent/list before all vectors.\\[3pt]
SPR1--SPR25 & Pointwise multiplicity and theta assembly & One smooth representative for all words; full IsMultMap; exact restriction and linear assembly after initial bound/volume.\\[3pt]
CFO1--CFO21 & Selected first-order arithmetic bound & Full selected dualN and ArSys/Counts; exact B1 on the same Choice/B2 witness.\\[3pt]
CSR1--CSR22 & Common selected realization & Original finite columns, periods, evaluations, row-side and same-R Bundle/BWit/BunU consumers.\\[3pt]
'''
s=s[:end]+rows+s[end:]
a=s.index('Start with the version-0.36 audit in',start);b=s.index('including the preserved RF16 correction.',a)+len('including the preserved RF16 correction.')
s=s[:a]+r'''Start with the version-0.37 audit in
Section~\ref{sec:dependency-audit-v37}. Read ASB and SPR together:
ASB3/4 feed SPR13, which feeds ASB14, and the later SPR claims
complete the pointwise map. Read CFO for selected first-order
counting, with its unchanged CCH/CAP/CIP/JSP inputs. Read CSR
for the finite common-realization and Bundle assembly, retaining
its exact geometric, reading, multiplicity, side and division
premises. Earlier CFB/JIO/RQC/HCU/TAE chapters give their
analytic and representation-theoretic inputs; LFS/GFI retain
the complete global consumers. Historical frontiers are governed
by the current audit and additive updates, including the preserved RF16 correction.'''+s[b:]
s=s.replace('with version-0.36 updates where an input','with version-0.37 updates where an input')
(ROOT/'RH_readable_reconstruction_v0_37.tex').write_text(s)
print('Assembled',len(s.encode()),'bytes; all historical proof chapters retained.')
