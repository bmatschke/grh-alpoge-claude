#!/usr/bin/env python3
"""Append the v0.20 proofs and update only connective/current-scope prose."""
from pathlib import Path
import json,re
ROOT=Path(__file__).resolve().parent;OLD=ROOT/'history/version_0_19'
cfg=json.loads((ROOT/'increment_v0_20.json').read_text());prev=json.loads((OLD/'increment_v0_19.json').read_text())
s=(OLD/'RH_readable_reconstruction_v0_19.tex').read_text()
s=s.replace('working version 0.19','working version 0.20').replace('Working version 0.19','Working version 0.20')
s=s.replace('Actual character frames and local arithmetic realization','Normalized adic characters and finite Weil arithmetic')
s=s.replace('Primitive theta tests and quantitative mass windows','Exact mass ratios and uniform norm-prime supply')
start=s.index(r'\textbf{What version 0.19 achieves.}');end=s.index(r'\end{minipage}',start)
s=s[:start]+cfg['tex_front_summary']+'\n'+s[end:]
bridge=r'''\paragraph{Version-0.20 scope of the historical conditional proofs.}
The historical proofs below retain their original premises and text.
GA now constructs normalized adic characters from the stipulated global
Artin map and supplies exact local character laws and conditional
installed-character identifications. WA proves qualitative finite Weil
arithmetic, the normalized jet field and period fields for supplied
bottom triangles. MF proves the exact unramified CM mass ratio, with
classical Hasse--Minkowski stated explicitly. QR constructs the actual
ray-class family and proves its uniform weighted interval estimate;
the earlier reductions therefore supply the required norm primes.
Older descriptions of these particular suppliers as future work are
historical. Compatible nonempty arithmetic realizations and the full
geometric core, new full bottom-Weil existence, critical ratio fields,
quantitative dictionaries and exact embedding joins, and the four
global branches remain as stated in Section~\ref{sec:remaining}.

'''
heading=r'\paragraph{Version-0.19 scope of the historical conditional proofs.}'
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
s=s.replace('with version-0.19 updates where an input','with version-0.20 updates where an input')
out=ROOT/'RH_readable_reconstruction_v0_20.tex';out.write_text(s);print(out)
