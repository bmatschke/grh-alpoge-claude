#!/usr/bin/env python3
"""Insert the current reviewed chapters while preserving historical proof chapters."""
from pathlib import Path
import json,re
ROOT=Path(__file__).resolve().parent
cfg=json.loads((ROOT/"increment_v0_40.json").read_text())
s=(ROOT/"RH_readable_reconstruction_v0_39.tex").read_text()
s=s.replace("working version 0.39","working version 0.40").replace("Working version 0.39","Working version 0.40")
s=s.replace("Exact row inputs, original readers, full limits and pro-ell descent",
 "Actual patching, selected support, and common comparisons",1)
s=s.replace("with 77 new proof claims",f"with {cfg['expected_new_claims']} new proof claims",1)
a=s.index(r"\textbf{What version 0.39 achieves.}");b=s.index(r"\end{minipage}",a)
s=s[:a]+r"""\textbf{What version 0.40 achieves.}
The selected original \texttt{Raw} support theorem is now
reconstructed at $h=0$, $a=n=4$, $k.g=0$, under its original
arithmetic antecedents. The actual universal ring and maps,
patched module and full \texttt{S5}, quotient pair and ordinary
point, coefficient normalization and pro-$\ell$ descent are all
supplied. The original comparison, row-package and fitting-stage
copy constructors are also reconstructed on their original inputs.

"""+f"There are {cfg['expected_new_claims']} new claims and {cfg['predecessor_claim_count']+cfg['expected_new_claims']} cumulative claims. "+r"""
No whole compound selected leaf closes: 33 remain open,
classified as 22 C, 9 B and 2 D. The next arithmetic work
is the original ordinary/control/type, four Hida endpoints and
all-level same-$J$ automorphic packet. Actual common geometry,
fitting/rational tests, exact $\eta$ agreement, and the shared
local/global quantitative suppliers also remain.

Every historical proof, source array and dependency edge is
preserved. The current audit governs older frontier statements.
The underlying Lean proof is accepted as fully checked and correct.
This remains \textbf{a partial human reconstruction}.
"""+s[b:]
def mono(m):
 b=re.sub(r"(?<=[a-z])(?=[A-Z])",lambda _:r"\allowbreak ",m[1])
 b=re.sub(r"\.(?!\\allowbreak)",lambda _:r".\allowbreak ",b)
 b=re.sub(r"([/:])(?!\\allowbreak)",lambda m:m[1]+r"\allowbreak ",b)
 b=re.sub(r"\\_(?!\\allowbreak)",lambda _:r"\_\allowbreak ",b)
 return r"\texttt{"+b+"}"
def wraps(t):
 t=t.replace(r"\subsection{Closed relations and nonsemisimplicity without an extra"+ "\nfinite-generation premise}",
             r"\subsection{Closed relations and semisimplicity descent}")
 t=re.sub(r"\\texttt\{([^{}]*)\}",mono,t)
 t=re.sub(r"\\_(?!\\allowbreak)",lambda _:r"\_\allowbreak ",t)
 return re.sub(r",(?=[A-Za-z])",lambda _:r",\allowbreak{} ",t)
old=(ROOT/"dependency_audit_v0_39/main.tex").read_text()
marker=re.search(r"^\\section\{[^\n]+",old,re.M)[0]
assert s.count(marker)==1
s=s.replace(marker,wraps((ROOT/"dependency_audit_v0_40/main.tex").read_text())+r"""

\paragraph{Historical version-0.39 audit.}
The following audit is retained as a historical checkpoint.
Section~\ref{sec:dependency-audit-v40} and the version-0.40
scope updates govern current remaining obligations.
Historical conditional proofs keep their original hypotheses.

"""+marker,1)
marker=r"\section{Why simultaneous local exceptions have product size}"
assert s.count(marker)==1
s=s.replace(marker,wraps("\n\n".join((ROOT/c/"main.tex").read_text() for c in cfg["components"]))+"\n\n"+marker,1)
a=s.index(r"\section{The arithmetic still to be written out}")
b=s.index(r"\section{Claim ledger and reading order}",a)
s=s[:a]+r"""\section{The arithmetic still to be written out}\label{sec:remaining}

Section~\ref{sec:dependency-audit-v40} gives all 33 current
selected contracts. The selected one-point \texttt{Raw} theorem
and the original given-data comparison constructors are now
available; their earlier arithmetic and geometric inputs remain.

\begin{description}[style=nextline]
\item[Original arithmetic and automorphic systems.]
Construct ordinary/control/separating arithmetic fibers,
type/neat levels and \texttt{TThetaEx}, the four Hida endpoints
and all-level same-$J$ \texttt{TWAut/HasAut}. Preserve full
\texttt{CohP/LocCFT/N4}, both rank-four Links, prime $3$,
fixed $\iota$ and one common coefficient threshold.
LIM/PRG/PMS/SCI with BCN/PQL now supply the selected
$h=0,a=n=4,k.g=0$ \texttt{Raw} consumer on those original
data. General \texttt{NonssT} or arbitrary-chain Core is not
needed to finish this selected patching branch.
\item[Actual common geometry and fitting tests.]
Construct one original recursive/geometric member with its
\texttt{Inputs/Pins/Holds/ExAt/InGeo} and required core duties.
PKT supplies \texttt{PkT}, \texttt{RowPk} and fitting-stage
\texttt{Moved/Copy/Coh} on given data, with one numerical record
before every later stage. Supply actual \texttt{Fits}, primitive
rational tests and exact $o.\eta=q.\eta$ for full
\texttt{ReadL}. RDR's side/reader algorithms are already
reconstructed on these same objects.
\item[Remaining rational and common fields.]
Construct original \texttt{RatG/LiftTestB}, actual base rows,
host/frames, \texttt{MultEq} support, the stored nonzero
chain and group tie, eigensystems/parts/all-embedding
\texttt{logLam}, \texttt{HD/d3b} and \texttt{NEb}.
RPI supplies exact \texttt{RowPairInt}; first
\texttt{DivDef3} follows from original premises.
The stronger second \texttt{DivRows3} square remains separate.
\item[Shared quantitative suppliers.]
Construct actual \texttt{NBuilt/NdSpec}, the original local
projection square and normalized spectra, then denominator,
retained-defect, period-height, local-gain and spectral estimates
on the common family. Complete compatible second-layer selection
with the original simultaneous eventual thresholds.
\end{description}

RH retains I/II/V; unrestricted Dirichlet GRH additionally
retains III, SeedIV and original rank-four chain propagation
and descent. The two D-class human source-interface questions
remain localized in the register. The optional AQ route remains
optional, and DEX11 continues to govern historical RF16.

"""+s[b:]
start=s.index(r"\section{Claim ledger and reading order}")
end=s.index(r"\end{longtable}",start)
rows=r"""
PRG1--PRG24 & Actual universal ring and maps & Full five-part tuple, coefficient ring, ordered splitting targets and every specialization identity.\\[3pt]
PMS1--PMS32 & Actual patched module and full S5 & All-level paired maps, six relation families, support/dimension/fiber/move and exact same-$J$ annihilator comparison.\\[3pt]
BCN1--BCN25 & Full coefficient normalization & Actual unramified extension, Unit parameter, closed ideals, same points and restricted Core consumer.\\[3pt]
SCI1--SCI13 & Selected Core and Raw & Actual quotient pair and point; one completion, vanishing support ideal and original $J$-containment.\\[3pt]
PKT1--PKT30 & Original common comparison constructors & Full PkT, RowPk and fitting-stage Moved/Copy/Coh; original initial geometry and exact eta guard retained.\\[3pt]
"""
s=s[:end]+rows+s[end:]
a=s.index("Start with the version-0.39 audit in",start)
b=s.index("including the preserved RF16 correction.",a)+len("including the preserved RF16 correction.")
s=s[:a]+r"""Start with the version-0.40 audit in
Section~\ref{sec:dependency-audit-v40}. For the arithmetic
support branch, read PRG and PMS with LIM, then SCI with
CRW and BCN/PQL. This gives the complete selected original
Raw producer under its original arithmetic antecedents.
For the common comparison branch, read PKT with RDR,
CSR and DI/RPI. This supplies the original comparison,
copy and reading algorithms while retaining actual initial
geometry, fitting/rational tests and exact eta agreement.
The current audit identifies the next original
ordinary/type/Hida/HasAut, common-family and quantitative
suppliers. Every historical chapter remains available,
including the preserved RF16 correction."""+s[b:]
s=s.replace("with version-0.39 updates where an input","with version-0.40 updates where an input")
a=s.index(r"\section{The arithmetic still to be written out}")
b=s.index(r"\section{Claim ledger and reading order}",a)
s=s[:a]+wraps(s[a:b])+s[b:]
(ROOT/"RH_readable_reconstruction_v0_40.tex").write_text(s)
print("Assembled",len(s.encode()),"bytes; historical proof chapters preserved.")
