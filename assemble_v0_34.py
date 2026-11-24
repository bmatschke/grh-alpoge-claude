#!/usr/bin/env python3
"""Append v0.34 chapters; retain every historical mathematical proof."""
from pathlib import Path
import json,re
ROOT=Path(__file__).resolve().parent;OLD=ROOT/'history/version_0_33'
cfg=json.loads((ROOT/'increment_v0_34.json').read_text())
s=(OLD/'RH_readable_reconstruction_v0_33.tex').read_text()
s=s.replace('working version 0.33','working version 0.34').replace('Working version 0.33','Working version 0.34')
s=s.replace('Original cuspidality, column slopes, and the same Hecke ideal','Original global consumers, theta derivatives, and Count-II normalization',1)
s=s.replace('A refined completion audit with 46 new proof claims',f"A refined completion audit with {cfg['expected_new_claims']} new proof claims",1)
a=s.index(r'\textbf{What version 0.33 achieves.}');b=s.index(r'\end{minipage}',a)
s=s[:a]+r'''\textbf{What version 0.34 achieves.}
The original global count, slopes, positive ranks, all-height frame,
node, window and character consumers now have explicit human proofs.
The theta integral has proved real derivatives, one growth exponent
for every derivative word, and exact lowering. Count II now has its
required every-map reciprocity dictionary and universal irreducible-point
normalization, including coefficient characteristic three.

The selected register still has 35 coupled open leaves: 23 C, 10 B
and 2 D. The global residual is the original loss estimate and
same-family tied-ledger/Closed installation. The analytic residual
keeps common ioP, lowest-type multiplicity one, boundedness and the
original Hilbert realization. Ordinary control and patched support,
common geometry, readings, rational tests and local/spectral producers
remain. RH retains I/II/V; unrestricted Dirichlet GRH also retains III.

Every historical proof, source array and claim dependency remains.
The current audit governs historical frontier statements. We accept
the underlying Lean proof as fully checked and correct. This remains
\textbf{a partial human reconstruction}; no new Lean replay is claimed.
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
marker=r'\section{Current dependency audit: original cuspidality, column slopes, and the same Hecke ideal}'
assert s.count(marker)==1
s=s.replace(marker,wraps((ROOT/'dependency_audit_v0_34/main.tex').read_text())+r'''

\paragraph{Historical version-0.33 audit.}
The following audit is preserved as a historical checkpoint.
Section~\ref{sec:dependency-audit-v34} and the version-0.34 scope
updates give the current remaining obligations. The historical
conditional mathematics retains its original hypotheses.

'''+marker,1)
marker=r'\section{Why simultaneous local exceptions have product size}'
assert s.count(marker)==1
addition='\n\n'.join((ROOT/c/'main.tex').read_text()for c in cfg['components'])+'\n\n'
s=s.replace(marker,wraps(addition)+marker,1)
a=s.index(r'\section{The arithmetic still to be written out}');b=s.index(r'\section{Claim ledger and reading order}',a)
remaining=r'''\section{The arithmetic still to be written out}\label{sec:remaining}

Section~\ref{sec:dependency-audit-v34} gives all 35 selected remaining
contracts. The completed global, analytic and Count-II consumers
keep their original common geometric and arithmetic premises.

\begin{description}[style=nextline]
\item[The common original construction.]
Construct the recursive core, one compatible Bundle and its duties.
The construction-class size and rank implications remain complete.
Supply the original readings, actual base rows and simultaneous
rational tests, then the literal local NBuilt/NdSpec and projection
square, all with the same fields and embeddings.
\item[The remaining theta producers.]
Smoothness, all-word uniform growth, exact lowering and genuine
cuspidality are now proved on the original kernels. Produce one
ioP valid at every parameter, prove LowSm/LowIrr for the entire
original lowest compact type, and reconstruct boundedness and the
exact Hilbert multiplicity realization with Sobolev continuity.
\item[The final global loss and ledger.]
The same-selector FamGLmin package now feeds the exact count,
source/quotient slopes, positive ranks, all-height frame, nodes,
windows and characters. Prove LossFS(Fm,0), assemble the literal
same-family linkCore/ChainTied, and carry its fields through Closed.
Keep $C_{\rm abs}=2,C_0=3,C_5=4,e_D=2,e_L=0$.
The compatible second layer, denominator, retained defect,
period-height, local-gain and spectral producers remain upstream.
\item[The original arithmetic counts.]
RH and two-primary targets retain I/II/V. CountII now has exact
reciprocity and its full required NiceI Norm, with old D0 and
characteristic three. Original ordinary/control data, four further
Hida endpoints, same-J all-level HasAut and the other single-point
support inputs remain. Both Links keep one threshold at fixed iota.
Unrestricted Dirichlet targets also retain III, SeedIV and chains.
\end{description}

Next prioritize the bounded loss/tied-ledger join and, in parallel,
common ioP/lowest-type/Hilbert realization and ordinary rank-four
arithmetic. The current audit preserves every compound scope, the
optional AQ route and the DEX11 correction of historical RF16.

'''
s=s[:a]+wraps(remaining)+s[b:]
start=s.index(r'\section{Claim ledger and reading order}');end=s.index(r'\end{longtable}',start)
rows=r'''
GVC1--GVC18 & Original global counts and source slopes & Exact degree/Vandermonde comparison, numerical and weight clauses, CountF and SlopesMF.\\[3pt]
GFA1--GFA12 & Original quotient and frame consumers & Type-prime cost, actual corrections and support, all-height frame, exact nodes/windows/characters.\\[3pt]
TAE1--TAE13 & Original real theta extension & Smooth generators, all-word growth, dominated differentiation, stored vacuum and exact lowering.\\[3pt]
CIP1--CIP12 & Count-II reciprocity and normalization & Every source local map at split CM places, cyclotomic sign and full required NiceI Norm.\\[3pt]
'''
s=s[:end]+rows+s[end:]
a=s.index('Start with the version-0.33 audit in',start);b=s.index('including the preserved RF16 correction.',a)+len('including the preserved RF16 correction.')
s=s[:a]+r'''Start with the version-0.34 audit in
Section~\ref{sec:dependency-audit-v34}. Read GVC and GFA for the
original global count, slope, frame, window and character consumers;
TAE for the real analytic and lowering block; CIP for exact
reciprocity and the required irreducible-point normalization.
Their immediate inputs are GLS/RSL/GLE, CW/BTH/FIA/CTC, and KX/JSP.
HX/MT/KA/ZW retain the host, metrics, count aggregation and final
numerical endpoint. Historical frontiers are governed by the current
audit and additive scope updates, including the preserved RF16 correction.'''+s[b:]
s=s.replace('with version-0.33 updates where an input','with version-0.34 updates where an input')
(ROOT/'RH_readable_reconstruction_v0_34.tex').write_text(s)
print('Assembled',len(s.encode()),'bytes; historical proof chapters retained.')
