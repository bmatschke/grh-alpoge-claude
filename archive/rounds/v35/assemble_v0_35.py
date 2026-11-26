#!/usr/bin/env python3
"""Assemble the complete additive manuscript; retain historical mathematical chapters."""
from pathlib import Path
import json,re
ROOT=Path(__file__).resolve().parent;OLD=ROOT/'history/version_0_34'
cfg=json.loads((ROOT/'increment_v0_35.json').read_text())
s=(OLD/'RH_readable_reconstruction_v0_34.tex').read_text()
s=s.replace('working version 0.34','working version 0.35').replace('Working version 0.34','Working version 0.35')
s=s.replace('Original global consumers, theta derivatives, and Count-II normalization','Completed global assembly, original lowest types, and auxiliary primes',1)
s=s.replace('A refined completion audit with 55 new proof claims',f"A refined completion audit with {cfg['expected_new_claims']} new proof claims",1)
a=s.index(r'\textbf{What version 0.34 achieves.}');b=s.index(r'\end{minipage}',a)
s=s[:a]+r'''\textbf{What version 0.35 achieves.}
Both original losses and the exact same-family tied-ledger and final
\texttt{Closed} assembly are now reconstructed. The selected global
assembly leaf is proved on its original inputs. The original full
lowest compact type is smooth and irreducible with multiplicity one;
the exact extremal coefficient and Hilbert-map stages are supplied.
Count II has its complete original auxiliary-prime supplier under
unchanged \texttt{CohP}, and residual Hecke values for every supplied
integral type.

The selected register has 34 open coupled leaves: 23 C, 9 B and 2 D.
Common geometry, compatible choices, local/spectral estimates,
simultaneous ioP and global Sobolev completion, ordinary/control and
same-ideal automorphic support remain. RH retains I/II/V;
unrestricted Dirichlet GRH also retains III.

Every historical mathematical proof, source array and dependency edge
is retained. The current audit governs older frontier statements.
We accept the underlying Lean proof as fully checked and correct.
This remains \textbf{a partial human reconstruction}; no new Lean
replay is claimed.
'''+s[b:]
def mono_breaks(m):
    body=re.sub(r'(?<=[a-z])(?=[A-Z])',lambda _:r'\allowbreak ',m[1])
    body=re.sub(r'\.(?!\\allowbreak)',lambda _:r'.\allowbreak ',body)
    body=re.sub(r'([/:])(?!\\allowbreak)',lambda m:m[1]+r'\allowbreak ',body)
    body=re.sub(r'\\_(?!\\allowbreak)',lambda _:r'\_\allowbreak ',body)
    return r'\texttt{'+body+'}'
def wraps(t):
    for phrase in ['orbit/Frobenius/valuation','host/cohomology']:
        t=t.replace(phrase,phrase.replace('/',r'/\allowbreak '))
    t=re.sub(r'\\texttt\{([^{}]*)\}',mono_breaks,t)
    t=re.sub(r'\\_(?!\\allowbreak)',lambda _:r'\_\allowbreak ',t)
    return re.sub(r',(?=[A-Za-z])',lambda _:r',\allowbreak{} ',t)
marker=r'\section{Current dependency audit: original global consumers, theta derivatives, and Count-II normalization}'
assert s.count(marker)==1
s=s.replace(marker,wraps((ROOT/'dependency_audit_v0_35/main.tex').read_text())+r'''

\paragraph{Historical version-0.34 audit.}
The following audit is preserved as a historical checkpoint.
Section~\ref{sec:dependency-audit-v35} and the version-0.35 scope
updates give the current remaining obligations. The historical
conditional arguments retain their stated hypotheses.

'''+marker,1)
marker=r'\section{Why simultaneous local exceptions have product size}'
assert s.count(marker)==1
addition='\n\n'.join((ROOT/c/'main.tex').read_text()for c in cfg['components'])+'\n\n'
s=s.replace(marker,wraps(addition)+marker,1)
a=s.index(r'\section{The arithmetic still to be written out}');b=s.index(r'\section{Claim ledger and reading order}',a)
remaining=r'''\section{The arithmetic still to be written out}\label{sec:remaining}

Section~\ref{sec:dependency-audit-v35} gives every one of the 34
remaining selected contracts. The global assembly implication is
complete; the shared producer hypotheses remain exact.

\begin{description}[style=nextline]
\item[The common original construction.]
Construct the recursive core, one compatible Bundle and its duties,
the original geometric readings, actual base rows and simultaneous
rational tests, and the literal local NBuilt/NdSpec projection square.
The original fields, embeddings and coefficient maps must agree.
The construction-class size and rank implications remain complete.
\item[The original theta extension.]
Produce one ioP valid for every parameter on the same original datum.
Full LowSm/LowIrr and multiplicity one on the actual ordered base model
are now proved. The extremal coefficient identity and Hilbert map are
also proved under boundedness and the same finite-volume regular target.
Supply those target inputs, then the pointwise smooth representatives,
all derivative identities, Sobolev evaluation and uniform growth,
central finiteness and cusp closure needed for the full original MMap.
\item[The remaining global producers.]
The eleven-field FamGLmin package and all its numerical, lattice and
loss consumers now give the exact same-family ChainTied and Closed
assembly. Construct the compatible second layer and duties, together
with the original denominator, retained-defect, period-height,
local-gain and spectral estimates. Their hypotheses have not been
discharged by completing the consumer.
\item[The original arithmetic counts.]
RH and two-primary targets still need I/II/V. CountII now has exact
reciprocity, required universal NiceI normalization, full original ArPl
under CohP, and residual values for any supplied integral type.
Its ordinary/control, type/neatU/TThetaEx, four further Hida endpoints,
same-J all-level HasAut, Choice, first-order/obstruction bounds and Raw
remain. Both original Links retain the threshold at fixed iota.
Unrestricted Dirichlet targets also retain III, SeedIV and chains.
\end{description}

The next work should be selected from these producer contracts by its
contribution to the final ten-input interface. The bounded global
assembly need not be revisited. The precise next source locations and
couplings are recorded in the version-0.35 continuation notes. The
optional AQ route and the DEX11 correction of historical RF16 remain.

'''
s=s[:a]+wraps(remaining)+s[b:]
start=s.index(r'\section{Claim ledger and reading order}');end=s.index(r'\end{longtable}',start)
rows=r'''
LFS1--LFS17 & Original simultaneous losses & Exact prime classes, eleven terms, every-reading dictionary and the same realized degree pair.\\[3pt]
GFI1--GFI17 & Complete original global assembly & Every tied-ledger field, original chosen-data conversion and final Closed quantifiers.\\[3pt]
HCU1--HCU20 & Original lowest type and Hilbert coefficient & Full multiplicity one, holomorphic uniqueness, exact base model and conditional Hilbert realization.\\[3pt]
CAP1--CAP17 & Original auxiliary primes and residual values & Full ArPl under CohP, all lists/levels and uniform bound; supplied-type IsRes.\\[3pt]
'''
s=s[:end]+rows+s[end:]
a=s.index('Start with the version-0.34 audit in',start)
b=s.index('including the preserved RF16 correction.',a)+len('including the preserved RF16 correction.')
s=s[:a]+r'''Start with the version-0.35 audit in
Section~\ref{sec:dependency-audit-v35}. Read LFS and GFI for the
complete original loss and final-global assembly consumer; HCU for
the full original lowest type, coefficient uniqueness and Hilbert
map; CAP for the original auxiliary-prime supplier and residual
Hecke values. Their immediate inputs are GVC/GFA/GLS/RSL/GLE,
TAE/CW/BTH/FIA/CTC, and CIP/JSP/QX. Earlier chapters retain the
host, metric, counting and final zero-free arguments. Historical
frontiers are governed by the current audit and additive scope
updates, including the preserved RF16 correction.'''+s[b:]
s=s.replace('with version-0.34 updates where an input','with version-0.35 updates where an input')
(ROOT/'RH_readable_reconstruction_v0_35.tex').write_text(s)
print('Assembled',len(s.encode()),'bytes; historical mathematical chapters retained.')
