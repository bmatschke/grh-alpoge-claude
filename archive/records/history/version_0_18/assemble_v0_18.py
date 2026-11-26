#!/usr/bin/env python3
"""Append the v0.18 proofs and update only connective/current-scope prose."""
from pathlib import Path
import json,re
ROOT=Path(__file__).resolve().parent;OLD=ROOT/'history/version_0_17'
cfg=json.loads((ROOT/'increment_v0_18.json').read_text());prev=json.loads((OLD/'increment_v0_17.json').read_text())
s=(OLD/'RH_readable_reconstruction_v0_17.tex').read_text()
s=s.replace('working version 0.17','working version 0.18').replace('Working version 0.17','Working version 0.18')
s=s.replace('Vacuum identities, covariance and arithmetic choices','Arithmetic compatibility and actual period rings')
s=s.replace('Restricted lattices and exact later-stage boundaries','Original sized geometry and rational theta targets')
start=s.index(r'\textbf{What version 0.17 achieves.}');end=s.index(r'\end{minipage}',start)
s=s[:start]+cfg['tex_front_summary']+'\n'+s[end:]
bridge=r'''\paragraph{Version-0.18 scope of the historical conditional proofs.}
The historical proofs below retain their original premises and text.
RC now expands actual rank, character and local-level mechanics.
LS constructs the actual local period rings and the bare Galois stage
on the same adapted rows. IG constructs an original sized preliminary
input and the exact chosen-volume empty-jet stage. TD supplies rational
theta cuts, common-image and metric deductions and common-test
normalization under explicit primitive inputs. Older statements of
these steps as future work are historical. Compatible nonempty
realizations, actual frame/core and quantitative windows, primitive
theta tests/operator identities, and the four global branches remain
as stated in Section~\ref{sec:remaining}.

'''
heading=r'\paragraph{Version-0.17 scope of the historical conditional proofs.}'
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
s=s.replace('with version-0.17 updates where an input','with version-0.18 updates where an input')
out=ROOT/'RH_readable_reconstruction_v0_18.tex';out.write_text(s);print(out)
