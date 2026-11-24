#!/usr/bin/env python3
"""Add the v0.39 proofs and governing current audit to the cumulative TeX."""
from pathlib import Path
import json,re
ROOT=Path(__file__).resolve().parent;cfg=json.loads((ROOT/'increment_v0_39.json').read_text())
s=(ROOT/'RH_readable_reconstruction_v0_38.tex').read_text()
s=s.replace('working version 0.38','working version 0.39').replace('Working version 0.38','Working version 0.39')
s=s.replace('Initial theta bounds, completed-point arithmetic, and exact row identities','Exact row inputs, original readers, full limits and pro-ell descent',1)
s=s.replace('with 69 new proof claims',f"with {cfg['expected_new_claims']} new proof claims",1)
a=s.index(r'\textbf{What version 0.38 achieves.}');b=s.index(r'\end{minipage}',a)
s=s[:a]+r'''\textbf{What version 0.39 achieves.}
The entire original \texttt{S4} limit-system construction and
full \texttt{CoreBC}-to-\texttt{Raw} pro-$\ell$ descent are
now reconstructed. Exact integrability of the actual row pairs
removes the extra \texttt{RowPairInt} premise of the first
division identity. The original level-zero side and moved-reader
constructors are reconstructed on their given data, with the
precise $\eta$ guard retained for full \texttt{ReadL}.

'''+f"There are {cfg['expected_new_claims']} new claims and {cfg['predecessor_claim_count']+cfg['expected_new_claims']} cumulative claims. "+r'''
No additional whole selected leaf closes: 33 remain open,
classified as 22 C, 9 B and 2 D. Their nested dependencies
are smaller. The next arithmetic producers are normalized
limiting patching/S5 and coefficient normalization/Unit.
Actual common geometry/comparisons/tests, local/spectral and
ordinary/automorphic producers also remain.

Every historical proof, source array and dependency edge is
preserved. The current audit governs older frontier statements.
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
old=(ROOT/'dependency_audit_v0_38/main.tex').read_text()
marker=re.search(r'^\\section\{[^\n]+',old,re.M)[0]
assert s.count(marker)==1
s=s.replace(marker,wraps((ROOT/'dependency_audit_v0_39/main.tex').read_text())+r'''

\paragraph{Historical version-0.38 audit.}
The following audit is retained as a historical checkpoint.
Section~\ref{sec:dependency-audit-v39} and the version-0.39
scope updates govern current remaining obligations.
Historical conditional proofs keep their original hypotheses.

'''+marker,1)
marker=r'\section{Why simultaneous local exceptions have product size}'
assert s.count(marker)==1
s=s.replace(marker,wraps('\n\n'.join((ROOT/c/'main.tex').read_text() for c in cfg['components']))+'\n\n'+marker,1)
a=s.index(r'\section{The arithmetic still to be written out}');b=s.index(r'\section{Claim ledger and reading order}',a)
s=s[:a]+r'''\section{The arithmetic still to be written out}\label{sec:remaining}

Section~\ref{sec:dependency-audit-v39} gives every one of the
33 current selected contracts. Four nested branches advance
without closing their whole coupled obligations.

\begin{description}[style=nextline]
\item[Normalized limiting patching and support.]
Construct the actual normalized Core \texttt{RRObj/RMaps}
and compatible patched modules, then the original \texttt{S5}
dimension, fiber and annihilator support theorem. The selected
completed-point/cotangent/\texttt{ChainAbs} comparison is
already available. LIM now constructs the entire original
\texttt{S4}; PQL supplies full \texttt{TWQuot} and
\texttt{CoreBC}-to-\texttt{Raw} pro-$\ell$ descent.
These completed producers should be reused on the same
point, Kap, $B,J,K,f$ and supplied automorphic system.
\item[Coefficient normalization.]
Supply the original Core-to-CoreBC coefficient normalization
and the added \texttt{Unit} parameter. The old coefficient
ring need not already surject onto the point residue field.
This remains adjacent to normalized Core patching, separate
from the completed group and determinant descent.
\item[Actual common geometry and comparison inputs.]
Construct one original \texttt{q/o/Moved/Fits} realization,
\texttt{ChT/LfT/Reps}, primitive \texttt{Holds} and exact
$o.\eta=q.\eta$ at every required row/place. RDR supplies
the original level-zero side and moved-reader constructors,
their common pins and guarded full \texttt{ReadL}; these
algorithms are no longer open subproducers. The outer
family/eventual/same-Bundle duties remain.
\item[Rational tests, rows and common remaining fields.]
Construct actual \texttt{RatG/LiftTestB} values and base rows,
host/frames, \texttt{MultEq} support, the original nonzero
chain and group tie, eigensystems/parts/all-embedding
\texttt{logLam}, \texttt{HD/d3b} and \texttt{NEb}.
RPI supplies exact \texttt{RowPairInt}; first \texttt{DivDef3}
now follows from original premises alone. The stronger second
\texttt{DivRows3} theta square remains separate.
\item[Local and global quantitative suppliers.]
Construct original \texttt{NBuilt/NdSpec}, the same-row
projection square and normalized spectra, then denominator,
retained-defect, period-height, local-gain and spectral estimates
on the common family. Complete the compatible second-layer
selection. The final quantitative and ten-input consumers
keep their reconstructed scopes.
\item[Original arithmetic and automorphic production.]
CountII still requires ordinary/control/separating arithmetic
fibers, type/neat levels, \texttt{TThetaEx}, four Hida
endpoints and all-level same-$J$ \texttt{HasAut}. Preserve
full \texttt{CohP/LocCFT/N4}, both rank-four Links,
fixed $\iota$, $\ell=3$ and one common coefficient threshold.
Neither transported supplied modules nor a one-point
comparison construct these actual systems.
\end{description}

RH retains I/II/V; unrestricted Dirichlet GRH also retains
III, SeedIV and original chains. The optional AQ route and
DEX11 correction of historical RF16 retain their scopes.
Continuation notes identify next source endpoints; they are
work plans rather than additional closure claims.

'''+s[b:]
start=s.index(r'\section{Claim ledger and reading order}');end=s.index(r'\end{longtable}',start)
rows=r'''
RPI1--RPI15 & Exact original row integrability & Uniform derivative growth, literal cusp radicals and compact contraction; first division's extra analytic premise discharged.\\[3pt]
RDR1--RDR22 & Original side and reader constructors & Actual given-data lattice, all reader ties and common pins; full ReadL retains exact eta agreement.\\[3pt]
LIM1--LIM19 & Entire original S4 & One common cover, quotient and ultrafilter; all uniform local limits and complete Lim record.\\[3pt]
PQL1--PQL21 & Full quotient and pro-ell descent & Full laws and closed ideals; same point, B1/B2, modules and J; normalized patching remains.\\[3pt]
'''
s=s[:end]+rows+s[end:]
a=s.index('Start with the version-0.38 audit in',start);b=s.index('including the preserved RF16 correction.',a)+len('including the preserved RF16 correction.')
s=s[:a]+r'''Start with the version-0.39 audit in
Section~\ref{sec:dependency-audit-v39}. Read RPI with FV and
DI for exact row integrability and first division from original
premises. Read RDR with CSR for the original given-data
side/reader constructors and full ReadL's exact guard.
Read LIM and PQL with CRW/CCH/CFO for the full original
limit and matched pro-$\ell$ descent, retaining normalized
limiting patching/S5 and coefficient normalization/Unit.
FV/SBD and HCU/RQC/ASB/SPR retain the complete initial
theta-extension branch. LFS/GFI retain the global consumers.
The current audit and additive scope updates govern historical
frontiers, including the preserved RF16 correction.'''+s[b:]
s=s.replace('with version-0.38 updates where an input','with version-0.39 updates where an input')
(ROOT/'RH_readable_reconstruction_v0_39.tex').write_text(s)
print('Assembled',len(s.encode()),'bytes; historical proof chapters preserved.')
