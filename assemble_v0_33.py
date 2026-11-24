#!/usr/bin/env python3
"""Append reviewed v0.33 chapters without changing historical mathematical proofs."""
from pathlib import Path
import json,re
ROOT=Path(__file__).resolve().parent;OLD=ROOT/'history/version_0_32'
cfg=json.loads((ROOT/'increment_v0_33.json').read_text())
s=(OLD/'RH_readable_reconstruction_v0_32.tex').read_text()
s=s.replace('working version 0.32','working version 0.33').replace('Working version 0.32','Working version 0.33')
s=s.replace('Actual size and rank, local operators, and the theta frontier','Original cuspidality, column slopes, and the same Hecke ideal',1)
s=s.replace('A refined completion audit with 48 new proof claims',f"A refined completion audit with {cfg['expected_new_claims']} new proof claims",1)
a=s.index(r'\textbf{What version 0.32 achieves.}');b=s.index(r'\end{minipage}',a)
s=s[:a]+r'''\textbf{What version 0.33 achieves.}
The original finite isotropic average and the full constant-term
argument now prove genuine cuspidality of the original base theta
integral. The three GL4 implications and all eleven FamGLmin fields
are written on the same supplied second layer. The original
Hecke-kernel ideal and the one-point characteristic-prime support
transports also have explicit human proofs.

The selected register has 35 open leaves: 23 C, 10 B and 2 D.
The common geometric/analytic/arithmetic producers remain, including
the smooth multiplicity extension, its separate simultaneous ioP
identification, actual readings and rational tests, ordinary control
and patched support. The final global numerical/lattice join remains.
RH retains I/II/V; unrestricted Dirichlet GRH additionally retains III.

All historical mathematical chapters, source arrays and claim
dependencies remain. The current audit governs superseded frontier
statements. We accept the underlying Lean proof as fully checked
and correct. This remains \textbf{a partial human reconstruction};
no new Lean build or kernel replay is claimed.
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
marker=r'\section{Current dependency audit: actual size and rank, local operators, and the base theta frontier}'
assert s.count(marker)==1
s=s.replace(marker,wraps((ROOT/'dependency_audit_v0_33/main.tex').read_text())+r'''

\paragraph{Historical version-0.32 audit.}
The following audit is retained as a historical checkpoint.
Section~\ref{sec:dependency-audit-v33} and the version-0.33 additive
scope updates specify the current open obligations. The historical
conditional arguments retain their original hypotheses.

'''+marker,1)
marker=r'\section{Why simultaneous local exceptions have product size}'
assert s.count(marker)==1
addition='\n\n'.join((ROOT/c/'main.tex').read_text()for c in cfg['components'])+'\n\n'
addition=addition.replace('and its\nwrapper\n', 'and its wrapper:\\par\n\\noindent\n')
s=s.replace(marker,wraps(addition)+marker,1)
a=s.index(r'\section{The arithmetic still to be written out}');b=s.index(r'\section{Claim ledger and reading order}',a)
remaining=r'''\section{The arithmetic still to be written out}\label{sec:remaining}

Section~\ref{sec:dependency-audit-v33} is the current complete selected
audit. Its 35 open contracts keep the exact original final interface:
one compatible design and nine closed predicates. The finite-average,
cuspidality, GL4 and Hecke/support transports proved in this version
do not create their shared geometric or arithmetic producers.

\begin{description}[style=nextline]
\item[The common original construction.]
Construct the recursive core, one compatible Bundle and its duties.
The exact construction-class size and rank implications from DSZ/RMP
remain complete. Supply original readings, actual base rows and
simultaneous rational tests, with the same fields and embeddings.
Produce the actual local NBuilt/NdSpec and projection square.
\item[The residual theta extension.]
FIA and CTC prove literal finite cancellation and genuine cuspidality.
Complete smoothness, uniform derivative growth, lowering/type,
finite-level/equivariance installation and the bounded holomorphic
realization into the original Hilbert multiplicity model. Separately
supply the source's common ioP with every parameter condition.
\item[The final global assembly and local estimates.]
The eleven FamGLmin fields are now proved on the same supplied
second layer. Construct that compatible second layer and complete
the original linkGLOBAL7\_min/items/link8 numerical/lattice join,
with $C_{\rm abs}=2,C_0=3,C_5=4,e_D=2,e_L=0$.
The denominator, retained defect, period-height, local-gain and
spectral producers remain on the common family.
\item[The original arithmetic counts.]
RH and two-primary targets still need I/II/V. CountII keeps the
kernel ideal of JSP5: construct its original ordinary/control
arithmetic data, exact reciprocity dictionary, four remaining Hida
fields, all-level automorphic modules and single-point support
inputs. Both rank-four Links must use one coefficient threshold at
fixed iota, before later DVRs and universal data. Unrestricted
Dirichlet targets additionally need III, SeedIV and original chains.
\end{description}

Next prioritize the bounded final global join and, in parallel,
the shared analytic extension and original ordinary arithmetic
producer. Do not repeat the now completed finite averages, cusp,
GL4 or kernel transport. The current audit retains every original
compound scope, the alternative AQ route and the DEX11 correction
of historical RF16.

'''
s=s[:a]+wraps(remaining)+s[b:]
start=s.index(r'\section{Claim ledger and reading order}');end=s.index(r'\end{longtable}',start)
rows=r'''
FIA1--FIA8 & Actual finite isotropic average & Original split/residue chart, half-datum guards, phase and uniform polynomial annihilation.\\[3pt]
CTC1--CTC13 & Original theta cuspidality & Compact quotients, orbit bounds, coinvariants, Fourier constant terms and genuine unipotent cuspidality.\\[3pt]
GLS1--GLS13 & Original column slopes & Actual ColVal, exact column slope, hook/Fock and constant-four bounds, same-selector FamGLmin.\\[3pt]
JSP1--JSP12 & Joint Hecke ideal and support & Kernel and annihilator, conditional RingProps/Dense, same-ideal TWBase and single-point P1 transport.\\[3pt]
'''
s=s[:end]+rows+s[end:]
a=s.index('Start with the version-0.32 audit in',start);b=s.index('including the preserved RF16 correction.',a)+len('including the preserved RF16 correction.')
s=s[:a]+r'''Start with the version-0.33 audit in
Section~\ref{sec:dependency-audit-v33}. Read FIA and CTC for the
original finite average and genuine cuspidality; GLS for the exact
column dictionary and slope bounds; JSP for the same-ideal Hecke
and one-point support transport. BTH/RSL/GLE give their immediate
earlier interfaces, and DSZ/RMP the construction-class size/rank
proofs. HX/MT/KA/ZW retain the host, metrics, count aggregation and
numerical endpoint; QX/YX retain the original Case-II chain.
Historical frontiers are governed by the current audit and additive
scope updates, including the preserved RF16 correction.'''+s[b:]
s=s.replace('with version-0.32 updates where an input','with version-0.33 updates where an input')
(ROOT/'RH_readable_reconstruction_v0_33.tex').write_text(s)
print('Assembled',len(s.encode()),'bytes; historical proof chapters retained.')
