#!/usr/bin/env python3
"""Insert reviewed current chapters, preserving all historical proof chapters."""
from pathlib import Path
import json,re
ROOT=Path(__file__).resolve().parent;cfg=json.loads((ROOT/'increment_v0_41.json').read_text())
s=(ROOT/'RH_readable_reconstruction_v0_40.tex').read_text()
s=s.replace('working version 0.40','working version 0.41').replace('Working version 0.40','Working version 0.41')
s=s.replace('Actual patching, selected support, and common comparisons','Neat levels, ordinary weights, and exact local tests',1)
s=s.replace('with 124 new proof claims',f"with {cfg['expected_new_claims']} new proof claims",1)
a=s.index(r'\textbf{What version 0.40 achieves.}');b=s.index(r'\end{minipage}',a)
s=s[:a]+r'''\textbf{What version 0.41 achieves.}
The full original \texttt{neatU} and \texttt{TThetaEx} are now
reconstructed. One theta character is fixed before every original
compact-open level, for arbitrary integral \(\tau_0\). The exact
\texttt{HdEx} record can be assembled after its original complete
integral type is supplied. The prescribed-field rational theta
transfers and both-level tests, and the original local Hecke
projection, faithful action and full \texttt{nonempty\_spec}
constructor, are reconstructed on their explicit original inputs.

'''+f"There are {cfg['expected_new_claims']} new claims and {cfg['predecessor_claim_count']+cfg['expected_new_claims']} cumulative claims. "+r'''
The selected \texttt{Raw} support theorem remains complete from
v0.40. No whole compound leaf closes in this version: 33 remain,
classified as 22 C, 9 B and 2 D. Original integral type and
ordinary/control, geometric class-sum and point-identity suppliers,
compatible arithmetic coefficient data, and shared quantitative
estimates remain. The next bounded arithmetic route is finite
level classes, ordinary freeness and base change.

Every historical proof, source array and dependency edge is
preserved. The current audit governs older frontier statements.
The underlying Lean proof is accepted as fully checked and correct.
This remains \textbf{a partial human reconstruction}.
'''+s[b:]
def mono(m):
 b=re.sub(r'(?<=[a-z])(?=[A-Z])',lambda _:r'\allowbreak ',m[1]);b=re.sub(r'\.(?!\\allowbreak)',lambda _:r'.\allowbreak ',b)
 b=re.sub(r'([/:])(?!\\allowbreak)',lambda m:m[1]+r'\allowbreak ',b);b=re.sub(r'\\_(?!\\allowbreak)',lambda _:r'\_\allowbreak ',b)
 return r'\texttt{'+b+'}'
def wraps(t):
 t=re.sub(r'\\texttt\{([^{}]*)\}',mono,t);t=re.sub(r'\\_(?!\\allowbreak)',lambda _:r'\_\allowbreak ',t)
 return re.sub(r',(?=[A-Za-z])',lambda _:r',\allowbreak{} ',t)
old=(ROOT/'dependency_audit_v0_40/main.tex').read_text();marker=re.search(r'^\\section\{[^\n]+',old,re.M)[0];assert s.count(marker)==1
s=s.replace(marker,'\\begingroup\\emergencystretch=3em\n'+wraps((ROOT/'dependency_audit_v0_41/main.tex').read_text())+'\n\\endgroup\n'+r'''

\paragraph{Historical version-0.40 audit.}
The following audit is retained as a historical checkpoint.
Section~\ref{sec:dependency-audit-v41} and the version-0.41
scope updates govern current remaining obligations.
Historical conditional proofs retain their original hypotheses.

'''+marker,1)
marker=r'\section{Why simultaneous local exceptions have product size}';assert s.count(marker)==1
new=wraps('\n\n'.join((ROOT/c/'main.tex').read_text() for c in cfg['components']))
s=s.replace(marker,'\\begingroup\\emergencystretch=3em\n'+new+'\n\\endgroup\n\n'+marker,1)
a=s.index(r'\section{The arithmetic still to be written out}');b=s.index(r'\section{Claim ledger and reading order}',a)
s=s[:a]+r'''\section{The arithmetic still to be written out}\label{sec:remaining}

Section~\ref{sec:dependency-audit-v41} gives every current selected
contract. The full original neatness and theta/weight producers are
now available, alongside the selected original Raw theorem and the
new exact rational and local finite constructors.

\begin{description}[style=nextline]
\item[Finite-level and ordinary entrance.]
Reconstruct the original \texttt{FuCmpMem.finU}, then
\texttt{OrdFree.ordStruct/ordFree} and \texttt{OrdBCMapOrd.ordBC}.
They now have the original neatness, full-ring character and
all-level \texttt{Frame.Free} stabilizer identity supplied by NTL/OTW. Continue into the actual
ordinary control, commutation and algebra statements. These are
the original Hida Frame/glIwa operators, distinct from HLP's
ambient local Hecke operators.
\item[Integral type and the same ideal.]
Construct the full original \texttt{TypeForAlt}, retaining every
required Teichmuller lift and \texttt{IsRecT}. OTW13 then assembles
the entire original \texttt{HdEx} record. Supply the four Hida
endpoints, separating arithmetic fibers and all-level
\texttt{TWAut/HasAut} on the same original \(J\), on both rank-four
Links. Preserve prime \(3\), fixed \(\iota\), full
\texttt{CohP/LocCFT} and one common coefficient threshold.
The selected \(h=0,a=n=4,k.g=0\) Raw proof is already reconstructed;
general multi-point Core is not needed for that selected consumer.
\item[Actual geometric rationality.]
Construct the original higher \texttt{CoversAt}, class-sum cusp
membership and uniqueness for all records and phase rescalings,
one \texttt{PointIdentCore} with common \(\lambda,z\) before
records, and base \texttt{ClassSumsSpan}. Retain its exact
\(8fr+4\le n_V\) condition. RTG now supplies the finite prescribed-field,
phase, original good-projector and both-level \texttt{LiftTestB}
calculations. Its \texttt{MLat} consumes the original
\texttt{LatFull}; the geometric fullness producer remains if that
field has not yet been constructed. Actual common geometry,
\texttt{Fits}, exact eta agreement, base rows and outer common-family
duties remain coupled.
\item[Compatible local arithmetic.]
Supply the actual common \texttt{MtInput} and choice data,
complex Hecke standard and no-Jordan facts, the original
\(F_3\) bridges with exact norm/\texttt{GoodCoef}/\(\operatorname{iq}\),
and \(F_4\) full common-overfield reading. Retain the original
arithmetic character and reciprocity inputs. HLP supplies literal
\texttt{MtSub}, \(\Psi\), projection/spans, faithful action and the
full \texttt{nonempty\_spec} constructor on those inputs.
Full \texttt{ndSpec\_exists}, \texttt{AutSpec} and the remaining
\texttt{NBuilt} fields still have to be installed together.
\item[Other shared and character-dependent producers.]
Complete the original host/frame, nonzero chain/group tie,
\texttt{MultEq}, parts/all-embedding \texttt{logLam},
\texttt{HD/d3b}, \texttt{NEb} and second \texttt{DivRows3}
duties. Supply denominator, retained-defect, period-height,
local-gain and normalized-spectrum estimates on the one original
family, and the compatible second-layer selector. RH retains
Cases I/II/V; unrestricted Dirichlet GRH additionally retains III,
Seed IV and original rank-four propagation/descent. The two
D-class human source-interface questions remain explicit.
\end{description}

The optional AQ route remains optional. Historical RF16 is still
governed by DEX11. No formal-source correctness question is reopened.

'''+s[b:]
start=s.index(r'\section{Claim ledger and reading order}');end=s.index(r'\end{longtable}',start)
rows=r'''
NTL1--NTL17 & Full original neat levels & All QData, arbitrary integral type representation, every compact-open level, original odd auxiliary prime.\\[3pt]
OTW1--OTW13 & Full theta/weight and conditional HdEx & One full-ring theta before every level; actual Artin convention; complete integral type antecedent retained.\\[3pt]
RTG1--RTG25 & Exact rational theta and tests & Prescribed coefficient record, phase transfer, original good projector and both-level LiftTestB; geometric suppliers explicit.\\[3pt]
HLP1--HLP32 & Exact local Hecke and projection & All maximal ideals, literal lattice/Psi, faithful action and full nonempty\_spec on original arithmetic inputs.\\[3pt]
'''
s=s[:end]+rows+s[end:]
a=s.index('Start with the version-0.40 audit in',start);b=s.index('including the preserved RF16 correction.',a)+len('including the preserved RF16 correction.')
s=s[:a]+r'''Start with the version-0.41 audit in
Section~\ref{sec:dependency-audit-v41}. For the next arithmetic
entrance read NTL and OTW with CIP/CAP, then reconstruct the actual
finite-level and ordinary/control suppliers. The earlier
PRG/PMS/SCI with BCN/PQL already give selected Raw.
For rational theta read RTG with CFB/BTH and the original common
reading chapters; its geometric cover, class-sum and point-identity
inputs are stated before the finite transfer. For the local
construction read HLP with LTD3 and MR23--MR26, retaining every
arithmetic coefficient and character input. The current audit
separates these completed consumers from their actual producers.
All historical chapters remain available, including the preserved
RF16 correction.'''+s[b:]
s=s.replace('with version-0.40 updates where an input','with version-0.41 updates where an input')
a=s.index(r'\section{The arithmetic still to be written out}');b=s.index(r'\section{Claim ledger and reading order}',a);s=s[:a]+wraps(s[a:b])+s[b:]
(ROOT/'RH_readable_reconstruction_v0_41.tex').write_text(s)
print('Assembled',len(s.encode()),'bytes; all historical chapters retained.')
