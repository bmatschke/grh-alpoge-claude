#!/usr/bin/env python3
"""Append the v0.19 proofs and update only connective/current-scope prose."""
from pathlib import Path
import json,re
ROOT=Path(__file__).resolve().parent;OLD=ROOT/'history/version_0_18'
cfg=json.loads((ROOT/'increment_v0_19.json').read_text());prev=json.loads((OLD/'increment_v0_18.json').read_text())
s=(OLD/'RH_readable_reconstruction_v0_18.tex').read_text()
s=s.replace('working version 0.18','working version 0.19').replace('Working version 0.18','Working version 0.19')
s=s.replace('Arithmetic compatibility and actual period rings','Actual character frames and local arithmetic realization')
s=s.replace('Original sized geometry and rational theta targets','Primitive theta tests and quantitative mass windows')
start=s.index(r'\textbf{What version 0.18 achieves.}');end=s.index(r'\end{minipage}',start)
s=s[:start]+cfg['tex_front_summary']+'\n'+s[end:]
bridge=r'''\paragraph{Version-0.19 scope of the historical conditional proofs.}
The historical proofs below retain their original premises and text.
HF now constructs the actual host-character frame and continues the
same-base initial coefficient, jet and bare-stage joins. AR expands
actual local arithmetic level/character comparisons and conditional
coefficient-weight and installed series realizations. TT supplies
primitive finite/local theta-test calculations under their exact field
and analytic interfaces. QW proves the original quantitative mass window
from its stated mass law and the exact prime-count/scale transports
from their uniform analytic/arithmetic inputs. The bounded-modulus
real-zero margin is also proved. Older statements of those reductions
as future work are historical. Compatible nonempty realizations and
the full core, genuine global mass and weighted interval suppliers,
remaining theta identities and the four global branches remain as
stated in Section~\ref{sec:remaining}.

'''
heading=r'\paragraph{Version-0.18 scope of the historical conditional proofs.}'
assert s.count(heading)==1;s=s.replace(heading,bridge+heading)
addition='\n\n'.join((ROOT/c/'main.tex').read_text()for c in cfg['tex_component_order'])+'\n\n'
addition=addition.replace(r'\detId',r'\operatorname{detId}')
# Typesetting-only repair of a literal function argument in TT9. Keep
# the reviewed fragment bytes and mathematical expression unchanged.
addition=addition.replace(r'\texttt{formC}(j_Xx)',r'$\texttt{formC}(j_Xx)$')
addition=addition.replace('\\end{split}\nEvery displayed sum is finite',
                          '\\end{split}\n\\]\nEvery displayed sum is finite')
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
s=s.replace('with version-0.18 updates where an input','with version-0.19 updates where an input')
out=ROOT/'RH_readable_reconstruction_v0_19.tex';out.write_text(s);print(out)
