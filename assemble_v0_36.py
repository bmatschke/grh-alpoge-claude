#!/usr/bin/env python3
"""Assemble the additive v0.36 manuscript, retaining historical proof chapters."""
from pathlib import Path
import json,re
ROOT=Path(__file__).resolve().parent
OLD=ROOT/'history/version_0_35'
cfg=json.loads((ROOT/'increment_v0_36.json').read_text())
s=(OLD/'RH_readable_reconstruction_v0_35.tex').read_text()
s=s.replace('working version 0.35','working version 0.36').replace('Working version 0.35','Working version 0.36')
s=s.replace('Completed global assembly, original lowest types, and auxiliary primes',
 'Simultaneous theta maps, exact analytic suppliers, and one-point arithmetic',1)
a=s.index(r'\textbf{What version 0.35 achieves.}');b=s.index(r'\end{minipage}',a)
s=s[:a]+r'''\textbf{What version 0.36 achieves.}
The original coefficient-to-polynomial bridge and the complete
simultaneous \texttt{ioP} are now reconstructed on the same original
datum. The actual regular representation, Hilbert smooth derivatives,
cusp-closure and central-scalar suppliers are proved on their exact
inputs. Count II has the full selected one-point \texttt{Choice}
together with literal \texttt{B2} for its same chosen zero-dimensional
\texttt{Kap}.

There are 71 new claims and 1770 cumulative claims. The selected
register retains 34 open coupled leaves: 23 C, 9 B and 2 D.
No additional whole selected leaf is closed in this version.
Common geometry and choices, initial target boundedness and volume,
pointwise smooth/Sobolev realization, local/spectral estimates,
ordinary/control and same-ideal automorphic support remain.
RH retains I/II/V; unrestricted Dirichlet GRH also retains III.

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
marker=r'\section{Current dependency audit: completed global assembly and original lowest types}'
assert s.count(marker)==1
s=s.replace(marker,wraps((ROOT/'dependency_audit_v0_36/main.tex').read_text())+r'''

\paragraph{Historical version-0.35 audit.}
The following audit is preserved as a historical checkpoint.
Section~\ref{sec:dependency-audit-v36} and the version-0.36 scope
updates give the current remaining obligations. The historical
conditional arguments retain their stated hypotheses.

'''+marker,1)
marker=r'\section{Why simultaneous local exceptions have product size}'
assert s.count(marker)==1
addition='\n\n'.join((ROOT/c/'main.tex').read_text() for c in cfg['components'])+'\n\n'
s=s.replace(marker,wraps(addition)+marker,1)
a=s.index(r'\section{The arithmetic still to be written out}')
b=s.index(r'\section{Claim ledger and reading order}',a)
remaining=r'''\section{The arithmetic still to be written out}\label{sec:remaining}

Section~\ref{sec:dependency-audit-v36} states every one of the 34
remaining selected contracts. The same-family global assembly
implication is complete, and this version closes substantial nested
theta and Count-II suppliers. The remaining producers are exact.

\begin{description}[style=nextline]
\item[The common original construction.]
Construct the recursive core, one compatible Bundle and its duties,
the original geometric readings, actual base rows and simultaneous
rational tests, and the literal local NBuilt/NdSpec projection square.
Begin the shared realization with \texttt{SelC.cols\_of\_witnesses}
and its one \texttt{ReadC} before later \texttt{TwArgs}, then the same
\texttt{R} package \texttt{BunU}/\texttt{BWit}, retaining geometric,
multiplicity and \texttt{NEb} inputs. Original fields, coefficient
embeddings, metrics and ties must agree.
\item[The original theta extension.]
The exact polynomial model and simultaneous
$\forall i\,\exists io_i\,\forall t$ producer are complete. The
same supplied \texttt{FinPair} now gives the original regular
representation; all Hilbert derivative words, cusp closure and
central-scalar suppliers are also proved. Supply initial boundedness
and target finite volume, then actual pointwise smooth representatives
and all derivative identities on that same quotient and finite level.
Prove one fixed-order Sobolev estimate with its exponent and derivative
list chosen before the point, representative and Hilbert vector.
These produce evaluation and uniform growth for the full original
\texttt{MMap}. Post-Hilbert central finiteness cannot justify earlier
boundedness.
\item[The remaining global producers.]
The eleven-field \texttt{FamGLmin} and exact
\texttt{ChainTied}/\texttt{Closed} consumers remain complete.
Construct their compatible second layer and duties, original
denominator and retained-defect bounds, period-height comparison,
local gain and normalized spectral estimates on that same family.
\item[The original arithmetic counts.]
RH and two-primary targets retain I/II/V. Count II now has the exact
reciprocity and universal \texttt{NiceI Norm}, full \texttt{ArPl}
under \texttt{CohP}, supplied-type residual values, and the full
$h=0,a=n=4$ \texttt{Choice}. Its same chosen $g=0$ \texttt{Kap}
satisfies \texttt{B2} with $C=0$ before every $m,N$.
Use these last two conclusions as one coupled existential witness;
no arbitrary-\texttt{Kap} obstruction theorem is asserted.
Ordinary/control/arithmetic fibers, type/\texttt{neatU}/
\texttt{TThetaEx}, four further Hida fields, same-$J$ all-level
\texttt{HasAut}, the precise \texttt{B1} bound
$4[L^+:\mathbf Q]+4q$, and the original \texttt{Raw} propagation
remain. The next bounded count target begins with full \texttt{dualN}
and the original local/global cardinality cancellation.
Both rank-four Links retain $\ell=3$, fixed $\iota$ and the common
coefficient threshold. Unrestricted Dirichlet targets additionally
retain III, SeedIV and chains.
\end{description}

Choose further work by its contribution to the final ten-input
interface. The current source-anchored continuation notes distinguish
the smooth/Sobolev, common-construction and selected first-order
count branches. These notes are plans, not further closure claims.
The optional AQ route and the DEX11 correction of historical RF16
remain in their established scopes.

'''
s=s[:a]+wraps(remaining)+s[b:]
start=s.index(r'\section{Claim ledger and reading order}')
end=s.index(r'\end{longtable}',start)
rows=r'''
CFB1--CFB13 & Original coefficient/Fock bridge & Exact polynomial range, covariance, cyclicity and all signed minor-weight and determinant identities.\\[3pt]
JIO1--JIO19 & Complete simultaneous theta map & One original io before every parameter, actual theta/Weil laws and exact unit-input normalization.\\[3pt]
RQC1--RQC22 & Regular quotient and analytic suppliers & Exact IsReg, smooth derivative words, cusp closure and central scalar action on their original inputs.\\[3pt]
CCH1--CCH17 & Coupled one-point Choice and B2 & Full polarized detector and finite coefficient transport; B2 for the same chosen zero-dimensional Kap.\\[3pt]
'''
s=s[:end]+rows+s[end:]
a=s.index('Start with the version-0.35 audit in',start)
b=s.index('including the preserved RF16 correction.',a)+len('including the preserved RF16 correction.')
s=s[:a]+r'''Start with the version-0.36 audit in
Section~\ref{sec:dependency-audit-v36}. Read CFB and JIO for the
complete original coefficient bridge and simultaneous theta map;
RQC for the exact regular representation, smooth Hilbert words,
cusp closure and central scalars; CCH for the coupled selected
one-point Choice and chosen-Kap B2. The exact upstream inputs and
downstream unfinished producers remain visible in those chapters.
Their immediate inputs include HCU/TAE/CW/BTH/FIA/CTC and
CIP/JSP/QX/CAP. The inherited LFS/GFI chapters retain the complete
global loss and final assembly consumers. Earlier chapters retain
the host, metric, counting and final zero-free arguments.
Historical frontiers are governed by the current audit and additive
scope updates, including the preserved RF16 correction.'''+s[b:]
s=s.replace('with version-0.35 updates where an input','with version-0.36 updates where an input')
(ROOT/'RH_readable_reconstruction_v0_36.tex').write_text(s)
print('Assembled',len(s.encode()),'bytes; historical mathematical chapters retained.')

