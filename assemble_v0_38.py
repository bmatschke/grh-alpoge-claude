#!/usr/bin/env python3
"""Add the reviewed v0.38 proof chapters and current audit to the cumulative TeX."""
from pathlib import Path
import json,re
ROOT=Path(__file__).resolve().parent;cfg=json.loads((ROOT/'increment_v0_38.json').read_text())
s=(ROOT/'RH_readable_reconstruction_v0_37.tex').read_text()
s=s.replace('working version 0.37','working version 0.38').replace('Working version 0.37','Working version 0.38')
s=s.replace('Original pointwise theta maps, selected counts, and common-record assembly','Initial theta bounds, completed-point arithmetic, and exact row identities',1)
s=s.replace('with 82 new proof claims',f"with {cfg['expected_new_claims']} new proof claims",1)
a=s.index(r'\textbf{What version 0.37 achieves.}');b=s.index(r'\end{minipage}',a)
s=s[:a]+r'''\textbf{What version 0.38 achieves.}
The original target finite volume and initial extremal theta bound
are now proved. With the inherited pointwise multiplicity map and
linear assembly, this closes the complete selected cuspidal
theta-extension obligation on its original common-data premises.
The selected rank-four route now has its actual completed
representation, cotangent presentation and one-point dimension
comparison. The first exact division identity is reconstructed
on the common selected realization, its retained inputs and
the additional \texttt{RowPairInt} supplier.

'''+f"There are {cfg['expected_new_claims']} new claims and {cfg['predecessor_claim_count']+cfg['expected_new_claims']} cumulative claims. "+r'''
Exactly one whole selected leaf closes; 33 remain open:
22 C, 9 B and 2 D. Original common geometry/readings,
rational tests, generic row-pair integrability, local/spectral
estimates, patching and ordinary/automorphic production remain.
RH retains I/II/V; unrestricted Dirichlet GRH also retains III.

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
marker=r'\section{Current dependency audit: original pointwise maps and selected first-order bounds}'
assert s.count(marker)==1
s=s.replace(marker,wraps((ROOT/'dependency_audit_v0_38/main.tex').read_text())+r'''

\paragraph{Historical version-0.37 audit.}
The following audit is retained as a historical checkpoint.
Section~\ref{sec:dependency-audit-v38} and the version-0.38
scope updates govern the current remaining obligations.
Historical conditional proofs keep their original hypotheses.

'''+marker,1)
marker=r'\section{Why simultaneous local exceptions have product size}'
assert s.count(marker)==1
s=s.replace(marker,wraps('\n\n'.join((ROOT/c/'main.tex').read_text() for c in cfg['components']))+'\n\n'+marker,1)
a=s.index(r'\section{The arithmetic still to be written out}');b=s.index(r'\section{Claim ledger and reading order}',a)
s=s[:a]+r'''\section{The arithmetic still to be written out}\label{sec:remaining}

Section~\ref{sec:dependency-audit-v38} states all 33 remaining
selected contracts. The initial analytic finite-volume and seed-bound
gates are closed; the following tasks now have priority.

\begin{description}[style=nextline]
\item[Actual common readings and rational theta values.]
Construct the original level-zero rational side and
\texttt{read\_of\_moved}, then the actual \texttt{RatG}
and base \texttt{LiftTestB} values. The selected theta extension
is complete, but its geometric reading, rational test and actual
base row remain separate. Keep the same $R$, maps, metrics and
thresholds. The source-anchored continuation note identifies
the exact original endpoints.
\item[The remaining common realization.]
Supply host/frames, \texttt{MultEq} nonzero-part support,
eigensystem/carrier/parts and all-embedding \texttt{logLam},
\texttt{HD/d3b} and \texttt{NEb}. First \texttt{DivDef3}
is complete on its original readings, \texttt{Pins/Holds},
nonzero stored chain, real-group and group-tie inputs.
The additional \texttt{RowPairInt} supplier is still required;
the initial highest-weight seed bound is not a universal
\texttt{CuspRapidDecay} theorem. Inspect the smaller exact
pairing contract before undertaking that stronger statement.
The second \texttt{DivRows3} theta square stays separate.
\item[Local and global quantitative suppliers.]
Construct original \texttt{NBuilt/NdSpec}, the same-row
projection square and normalized spectra, then denominator,
retained-defect, period-height, local-gain and spectral estimates
on the common family. Their final quantitative consumers and
the ten-input global assembly remain reconstructed.
\item[Original arithmetic support and descent.]
The same selected $h=0,a=n=4,g=0$ point has its coupled
\texttt{Choice/B1/B2}, completed full-block representation,
actual coefficient DVR, cotangent presentation and
\texttt{ChainAbs} comparison. Produce original \texttt{S4},
patched rings/maps/modules with \texttt{S5} support, and
coefficient/pro-$\ell$ descent for \texttt{Raw} on that
same point, \texttt{Kap}, $T$, \texttt{TWAut} and paired $J$.
Ordinary/control/arithmetic fibers, type/neat levels,
\texttt{TThetaEx}, four Hida endpoints and all-level same-$J$
\texttt{HasAut} remain major producers. Preserve full
\texttt{CohP/LocCFT/N4}, both Links, fixed $\iota$,
$\ell=3$ and the common coefficient threshold.
\end{description}

RH retains I/II/V; unrestricted Dirichlet GRH also retains
III, SeedIV and the original chains. The optional AQ route
and the DEX11 correction of historical RF16 retain their scopes.
Continuation notes are work plans, not extra closure claims.

'''+s[b:]
start=s.index(r'\section{Claim ledger and reading order}');end=s.index(r'\end{longtable}',start)
rows=r'''
FV1--FV11 & Original finite volume and arithmetic components & Every Haar and fundamental domain; target FinPair before parameters; exact finite classes and real groups.\\[3pt]
SBD1--SBD16 & Initial seed boundedness and complete theta extension & Pre-Hilbert full center, exact cusp descent, checked rapid decay; whole selected analytic leaf closed.\\[3pt]
CRW1--CRW21 & Selected completion and one-point comparison & Actual full-block representation and coefficient DVR; cotangent/presentation and ChainAbs; patching/support/descent remain.\\[3pt]
DI1--DI21 & First division identity on common realization & Exact level, row metric, composite and theta li/span/lat; original common and generic pairing inputs retained.\\[3pt]
'''
s=s[:end]+rows+s[end:]
a=s.index('Start with the version-0.37 audit in',start);b=s.index('including the preserved RF16 correction.',a)+len('including the preserved RF16 correction.')
s=s[:a]+r'''Start with the version-0.38 audit in
Section~\ref{sec:dependency-audit-v38}. Read FV and SBD for
the two completed initial analytic gates; inherited HCU/RQC/ASB/SPR
then provide the full original pointwise theta extension. Read
CRW with CCH/CFO for the selected completed-point and first-order
comparison, retaining actual patching and descent. Read DI with
CSR for first division compatibility on the same updated packet,
with its original geometry, chain, pairing and group-tie inputs.
LFS/GFI retain the global consumers. The current audit and additive
scope updates govern historical frontiers, including the preserved RF16 correction.'''+s[b:]
s=s.replace('with version-0.37 updates where an input','with version-0.38 updates where an input')
(ROOT/'RH_readable_reconstruction_v0_38.tex').write_text(s)
print('Assembled',len(s.encode()),'bytes; historical proof chapters preserved.')
