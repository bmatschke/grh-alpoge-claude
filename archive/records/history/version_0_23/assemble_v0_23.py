#!/usr/bin/env python3
"""Append reviewed v0.23 chains; replace only current connective/scope prose."""
from pathlib import Path
import json,re

ROOT=Path(__file__).resolve().parent
OLD=ROOT/'history/version_0_22'
cfg=json.loads((ROOT/'increment_v0_23.json').read_text())
prev=json.loads((OLD/'increment_v0_22.json').read_text())
s=(OLD/'RH_readable_reconstruction_v0_22.tex').read_text()
s=s.replace('working version 0.22','working version 0.23').replace('Working version 0.22','Working version 0.23')
s=s.replace('Actual form lattices and quantitative Weil dictionaries','Closing coefficient, cohomological and character chains')
s=s.replace('Large-gap representations and simultaneous prime pairs','An explicit audit of the remaining arithmetic dependencies')
a=s.index(r'\textbf{What version 0.22 achieves.}');b=s.index(r'\end{minipage}',a)
s=s[:a]+cfg['tex_front_summary']+'\n'+s[b:]
bridge=r'''\paragraph{Version-0.23 scope of the historical conditional proofs.}
Historical proof paragraphs and their original hypotheses are preserved.
HP1--HP6 now supply the literal characteristic-zero highest-weight,
irreducibility, classification and descent premises of MR5/MR19 and
AR13--AR14, including the full original-field weight endpoint.
VW1--VW4 give the complete cohomological-window assembly, conditional
on the exact deep suppliers \texttt{ThmBab}, \texttt{PointHV} and
\texttt{ThmBcFree}. WB1--WB8 give the full arithmetic-gap-to-character-window
implication, including ramification and uniform moving cutoffs, and
join the already complete AN2--AN3/GH6 analytic endpoint. DA1--DA2
make the common-family quantifiers and conditional global-link assembly
explicit. Thus older statements that these particular downstream
assemblies are still future work are historical. The actual arithmetic
gap/family, deep cohomological estimates, genuine theta/local data and
global metric/spectral comparisons remain open in this reconstruction.
The current frontier is in Section~\ref{sec:remaining} and the semantic
audit in Section~\ref{sec:dependency-audit}.

'''
heading=r'\paragraph{Version-0.22 scope of the historical conditional proofs.}'
assert s.count(heading)==1
s=s.replace(heading,bridge+heading)
addition='\n\n'.join((ROOT/c/'main.tex').read_text() for c in cfg['tex_component_order'])+'\n\n'
# Only line-breaking affordances in monospaced identifiers; original component
# files and paragraph hashes are untouched by this cumulative layout step.
addition=re.sub(r'\\texttt\{([^{}]*)\}',lambda m:r'\texttt{'+re.sub(r'\\_(?!\\allowbreak)',lambda _:r'\_\allowbreak ',m[1])+'}',addition)
marker=r'\section{Why simultaneous local exceptions have product size}'
assert s.count(marker)==1
s=s.replace(marker,addition+marker)
for k in ['tex_remaining_local','tex_next_target','tex_reading_order']:
 old=prev[k].strip()
 assert s.count(old)==1,(k,s.count(old))
 s=s.replace(old,cfg[k].strip())
start=s.index(r'\section{The arithmetic still to be written out}')
prefix,current=s[:start],s[start:]
old=r'''\item[Prime-pair installation and the centered target.]
QP supplies the whole \texttt{PairEx} input under CN/BD/HD: both primes satisfy the congruences, zero-free boxes, logarithmic-derivative bounds and centered twisted-ramp bounds simultaneously, including every required primitive inducer and the continuum of window parameters. Its use still requires installation on the same compatible host and the independent \texttt{VWinAt}/cohomological window. The selected-set and uniform gain-to-prime-sum estimates in \texttt{ChBalance}, \texttt{ChCore}, and \texttt{TopWin} remain to be expanded; the supplied fixed-pair estimates alone do not establish those global comparisons. \textsf{[QP22--QP25, OH2--OH5, GH4--GH7, SC2]}'''
new=r'''\item[Actual arithmetic gap and the cohomological suppliers.]
QP supplies full \texttt{PairEx} under CN/BD/HD. VW closes the exact
\texttt{VWinAt}/fixed-pair assembly from the explicitly named deep
cohomological cut. WB closes \texttt{ChBalance}, the subgroup/bias and
moving-cutoff deductions, the scalar exponent and the final positive
character window under its complete common-datum contract. What remains
is the actual arithmetic gap and its size/error packages, the deep
cohomological estimates, and their installation on one compatible host.
These are substantive arithmetic suppliers, not additional missing
Fourier or analytic manipulations. \textsf{[VW1--VW4, WB1--WB8, DA1--DA2]}'''
assert current.count(old)==1
current=current.replace(old,new)
s=prefix+current
last=prev['tex_ledger_rows'][-1]+r'\\[3pt]'
assert s.count(last)==1
s=s.replace(last,last+'\n'+'\n'.join(x+r'\\[3pt]' for x in cfg['tex_ledger_rows']))
s=s.replace('with version-0.22 updates where an input','with version-0.23 updates where an input')
out=ROOT/'RH_readable_reconstruction_v0_23.tex'
out.write_text(s)
print(out)
