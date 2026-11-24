#!/usr/bin/env python3
"""Append the v0.17 proofs and update only connective/current-scope prose."""
from pathlib import Path
import json,re
ROOT=Path(__file__).resolve().parent;OLD=ROOT/'history/version_0_16'
cfg=json.loads((ROOT/'increment_v0_17.json').read_text());prev=json.loads((OLD/'increment_v0_16.json').read_text())
s=(OLD/'RH_readable_reconstruction_v0_16.tex').read_text()
s=s.replace('working version 0.16','working version 0.17').replace('Working version 0.16','Working version 0.17')
s=s.replace('Arithmetic hosts, periods and normalized theta','Vacuum identities, covariance and arithmetic choices')
s=s.replace('Canonical local indices and the complete twisted comparison','Restricted lattices and exact later-stage boundaries')
start=s.index(r'\textbf{What version 0.16 achieves.}');end=s.index(r'\end{minipage}',start)
s=s[:start]+cfg['tex_front_summary']+'\n'+s[end:]
bridge=r'''\paragraph{Version-0.17 scope of the historical conditional proofs.}
The historical proofs below retain their original premises and text.
VI and CA now construct the actual vacuum, normalized indicator,
covariance and conditional canonical analytic join. NC constructs the
choice/tuple records under their exact rank, character and support ties.
SE supplies restricted lattices, several bare stage records and the pins
normal form. Older references to these steps as future work are historical;
the current boundary is stated in Section~\ref{sec:remaining} and the
new sections. Full \texttt{NStage}/\texttt{LocStage}, arithmetic ties,
initial geometric and analytic-window suppliers, and the four independent
global branches remain distinct.

'''
heading=r'\paragraph{Version-0.16 scope of the historical conditional proofs.}'
assert s.count(heading)==1;s=s.replace(heading,bridge+heading)
addition='\n\n'.join((ROOT/c/'main.tex').read_text()for c in cfg['tex_component_order'])+'\n\n'
addition=addition.replace(r'\detId',r'\operatorname{detId}')
def tags(m):
 block=m[0];ts=re.findall(r'\\tag\{[^}]+\}',block);assert len(ts)<=1
 return block if not ts else block.replace(ts[0],'').rstrip()+'\n '+ts[0]
addition=re.sub(r'\\begin\{split\}[\s\S]*?\\end\{split\}',tags,addition)
def multiline(m):
 b=m[0];return b.replace(r'\begin{split}',r'\begin{aligned}',1).replace(r'\end{split}',r'\end{aligned}',1)if'&&'in b else b
addition=re.sub(r'\\begin\{split\}[\s\S]*?\\end\{split\}',multiline,addition)
addition=re.sub(r'\\texttt\{([^{}]*)\}',lambda m:r'\texttt{'+re.sub(r'\\_(?!\\allowbreak)',lambda _:r'\_\allowbreak ',m[1])+'}',addition)
marker=r'\section{Why simultaneous local exceptions have product size}'
assert s.count(marker)==1;s=s.replace(marker,addition+marker)
for k in ['tex_remaining_local','tex_next_target','tex_reading_order']:
 old=prev[k].strip();assert s.count(old)==1,(k,s.count(old));s=s.replace(old,cfg[k].strip())
last=prev['tex_ledger_rows'][-1]+r'\\[3pt]';assert s.count(last)==1
s=s.replace(last,last+'\n'+'\n'.join(x+r'\\[3pt]'for x in cfg['tex_ledger_rows']))
s=s.replace('with version-0.16 updates where an input','with version-0.17 updates where an input')
out=ROOT/'RH_readable_reconstruction_v0_17.tex';out.write_text(s);print(out)
