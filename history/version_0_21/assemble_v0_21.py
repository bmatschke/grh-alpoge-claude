#!/usr/bin/env python3
"""Append the v0.21 proofs and update only connective/current-scope prose."""
from pathlib import Path
import json,re
ROOT=Path(__file__).resolve().parent;OLD=ROOT/'history/version_0_20'
cfg=json.loads((ROOT/'increment_v0_21.json').read_text());prev=json.loads((OLD/'increment_v0_20.json').read_text())
s=(OLD/'RH_readable_reconstruction_v0_20.tex').read_text()
s=s.replace('working version 0.20','working version 0.21').replace('Working version 0.20','Working version 0.21')
s=s.replace('Normalized adic characters and finite Weil arithmetic','All-place coefficient families and full Weil actions')
s=s.replace('Exact mass ratios and uniform norm-prime supply','Geometric volume normalization and exact centered sums')
start=s.index(r'\textbf{What version 0.20 achieves.}');end=s.index(r'\end{minipage}',start)
s=s[:start]+cfg['tex_front_summary']+'\n'+s[end:]
bridge=r'''\paragraph{Version-0.21 scope of the historical conditional proofs.}
The historical proofs below retain their original text and hypotheses.
NR now constructs the actual all-prime coefficient family, inducing
readings and conditional bounded integral row representations. CW
constructs the full finite and real Weil action, with exact rational
pullback automorphy and bottom suppliers. GV proves the exact measure
normalizations and direct definite quotient-to-mass identity, and uses
the explicitly named classical unitary Tamagawa theorem for the
indefinite volume and true-volume stage consequences. CC proves the
Dirichlet analytic inputs, exact centered integrals and uniform
late-cutoff thinning under the original zero-exclusion and
\texttt{RealBox} hypotheses.
Older descriptions of those specific suppliers as future work are
historical. Genuine form/local realization, the remaining exact Core
and discrete-series/formal-degree inputs, quantitative theta and
critical-ratio joins, and the independent global branches remain
as stated in Section~\ref{sec:remaining}.

'''
heading=r'\paragraph{Version-0.20 scope of the historical conditional proofs.}'
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
last=prev['tex_ledger_rows'][-1]+r'\\[3pt]';assert s.count(last)==1
s=s.replace(last,last+'\n'+'\n'.join(x+r'\\[3pt]'for x in cfg['tex_ledger_rows']))
s=s.replace('with version-0.20 updates where an input','with version-0.21 updates where an input')
out=ROOT/'RH_readable_reconstruction_v0_21.tex';out.write_text(s);print(out)
