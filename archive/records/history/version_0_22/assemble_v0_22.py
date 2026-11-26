#!/usr/bin/env python3
"""Append the v0.22 proofs and update only connective/current-scope prose."""
from pathlib import Path
import json,re
ROOT=Path(__file__).resolve().parent;OLD=ROOT/'history/version_0_21'
cfg=json.loads((ROOT/'increment_v0_22.json').read_text());prev=json.loads((OLD/'increment_v0_21.json').read_text())
s=(OLD/'RH_readable_reconstruction_v0_21.tex').read_text()
s=s.replace('working version 0.21','working version 0.22').replace('Working version 0.21','Working version 0.22')
s=s.replace('All-place coefficient families and full Weil actions','Actual form lattices and quantitative Weil dictionaries')
s=s.replace('Geometric volume normalization and exact centered sums','Large-gap representations and simultaneous prime pairs')
start=s.index(r'\textbf{What version 0.21 achieves.}');end=s.index(r'\end{minipage}',start)
s=s[:start]+cfg['tex_front_summary']+'\n'+s[end:]
bridge=r'''\paragraph{Version-0.22 scope of the historical conditional proofs.}
The historical proofs retain their original text and hypotheses.
MR now supplies actual fixed-state form realization and original-DVR
lattices/signatures, but its initial SideB has zero theta/empty toric
fields and requires a supplied NTh. QD supplies the quantitative
moved-vacuum dictionary and common scalar units on the original choices.
DC supplies the sufficient large-gap discrete-series range and exact
formal degree using the named Harish--Chandra theorem, and restricted
RealTied under GV's Tamagawa input. QP supplies relative progressions
and full simultaneous PairEx under the named classical CN/BD/HD inputs;
RealBox/ThinH hold on a compatible supplied host, and winPairs retains
VWinAt. Older descriptions of these specific suppliers as future work
are historical. Genuine same-object theta/local installation, critical
ratios, remaining Core/layout and global/cohomological/spectral joins
remain as stated in Section~\ref{sec:remaining}.

'''
heading=r'\paragraph{Version-0.21 scope of the historical conditional proofs.}'
assert s.count(heading)==1;s=s.replace(heading,bridge+heading)
addition='\n\n'.join((ROOT/c/'main.tex').read_text()for c in cfg['tex_component_order'])+'\n\n'
addition=addition.replace(r'\detId',r'\operatorname{detId}')
def tags(m):
 block=m[0];ts=re.findall(r'\\tag\{[^}]+\}',block);assert len(ts)<=1
 return block if not ts else block.replace(ts[0],'').rstrip()+'\n '+ts[0]
addition=re.sub(r'\\begin\{split\}[\s\S]*?\\end\{split\}',tags,addition)
def multiline(m):
 b=m[0]
 # An aligned display permits multiple relation columns; split permits one.
 # Normalize layout only in the cumulative assembly, preserving the reviewed
 # mathematical text and exact component paragraph bytes.
 multi=any(len(re.findall(r'(?<!\\)&',row))>1 for row in b.split(r'\\'))
 return b.replace(r'\begin{split}',r'\begin{aligned}',1).replace(r'\end{split}',r'\end{aligned}',1)if multi else b
addition=re.sub(r'\\begin\{split\}[\s\S]*?\\end\{split\}',multiline,addition)
addition=re.sub(r'\\texttt\{([^{}]*)\}',lambda m:r'\texttt{'+re.sub(r'\\_(?!\\allowbreak)',lambda _:r'\_\allowbreak ',m[1])+'}',addition)
marker=r'\section{Why simultaneous local exceptions have product size}'
assert s.count(marker)==1;s=s.replace(marker,addition+marker)
for k in ['tex_remaining_local','tex_next_target','tex_reading_order']:
 old=prev[k].strip();assert s.count(old)==1,(k,s.count(old));s=s.replace(old,cfg[k].strip())
# Update only the current remaining-work section; historical proof paragraphs
# keep their original wording and are qualified by the version bridge above.
remaining_updates={
 r'''host field and its selected half-different. The remaining inputs include
the prime/splitting hypotheses in the required analytic windows,
\texttt{ShortNorm}, \texttt{SmallOne}, \texttt{ThinH}, \texttt{PairEx}
and the cohomological window. SZ13 supplies the prescribed and cyclic
rank constructions, with their original order-window antecedents.''':
 r'''host field and its selected half-different. QP now supplies full
\texttt{PairEx} under CN/BD/HD and \texttt{ThinH} on a compatible
supplied host. QR25 already supplies \texttt{ShortNorm}; its applications
retain their original \texttt{ModAt}, host, rank and endpoint hypotheses.
The remaining inputs include the prime/splitting compatibility on that
same host, \texttt{SmallOne} and the independent
\texttt{VWinAt}/cohomological window. SZ13 supplies the prescribed and
cyclic rank constructions, with their original order-window antecedents.''',
 r'''\item[Simultaneous prime selection and the centered target.]
The fixed-pair argument uses the whole \texttt{PairEx} input: congruences, zero-free boxes, logarithmic derivatives, and centered twisted ramps must hold together. The character/Fourier identities do not estimate the centered tail. The selected-set and uniform gain-to-prime-sum estimates in \texttt{ChBalance}, \texttt{ChCore}, and \texttt{TopWin} remain to be expanded. \textsf{[OH2--OH5, GH4--GH7, SC2]}''':
 r'''\item[Prime-pair installation and the centered target.]
QP supplies the whole \texttt{PairEx} input under CN/BD/HD: both primes satisfy the congruences, zero-free boxes, logarithmic-derivative bounds and centered twisted-ramp bounds simultaneously, including every required primitive inducer and the continuum of window parameters. Its use still requires installation on the same compatible host and the independent \texttt{VWinAt}/cohomological window. The selected-set and uniform gain-to-prime-sum estimates in \texttt{ChBalance}, \texttt{ChCore}, and \texttt{TopWin} remain to be expanded; the supplied fixed-pair estimates alone do not establish those global comparisons. \textsf{[QP22--QP25, OH2--OH5, GH4--GH7, SC2]}'''
}
remaining_start=s.index(r'\section{The arithmetic still to be written out}')
prefix,current=s[:remaining_start],s[remaining_start:]
for old,new in remaining_updates.items():
 assert current.count(old)==1,current.count(old)
 current=current.replace(old,new)
s=prefix+current
last=prev['tex_ledger_rows'][-1]+r'\\[3pt]';assert s.count(last)==1
s=s.replace(last,last+'\n'+'\n'.join(x+r'\\[3pt]'for x in cfg['tex_ledger_rows']))
s=s.replace('with version-0.21 updates where an input','with version-0.22 updates where an input')
out=ROOT/'RH_readable_reconstruction_v0_22.tex';out.write_text(s);print(out)
