#!/usr/bin/env python3
"""Append v0.25 proof chapters and refresh current connective/scope prose."""
from pathlib import Path
import json,re

ROOT=Path(__file__).resolve().parent
OLD=ROOT/'history/version_0_24'
cfg=json.loads((ROOT/'increment_v0_25.json').read_text())
prev=json.loads((OLD/'increment_v0_24.json').read_text())
s=(OLD/'RH_readable_reconstruction_v0_24.tex').read_text()
s=s.replace('working version 0.24','working version 0.25').replace('Working version 0.24','Working version 0.25')
s=s.replace('The complete odd-minus cohomological supplier','The complete shared cohomology and simultaneous-window chains',1)
s=s.replace('Congruence transport and the remaining dependency chains','Arithmetic torsion, K-theory and exceptional vanishing',1)
a=s.index(r'\textbf{What version 0.24 achieves.}');b=s.index(r'\end{minipage}',a)
s=s[:a]+cfg['tex_front_summary']+'\n'+s[b:]
heading=r'\paragraph{Version-0.24 scope of the historical conditional proofs.}'
assert s.count(heading)==1
s=s.replace(heading,cfg['tex_scope_bridge']+heading)
addition='\n\n'.join((ROOT/c/'main.tex').read_text() for c in cfg['tex_component_order'])+'\n\n'+cfg['tex_dependency_update']
def mono_breaks(m):
 body=re.sub(r'(?<=[a-z])(?=[A-Z])',lambda _:r'\allowbreak ',m[1])
 body=body.replace('.',r'.\allowbreak ')
 body=re.sub(r'\\_(?!\\allowbreak)',lambda _:r'\_\allowbreak ',body)
 return r'\texttt{'+body+'}'
addition=re.sub(r'\\texttt\{([^{}]*)\}',mono_breaks,addition)
# The cumulative three-digit proposition numbers leave less header room than
# the standalone fragments. Start these two statements on their own line;
# the canonical proof files and their exact provenance ranges are unchanged.
for label,first in [('prop:lk-tate','Put'),('claim:KB1','Let')]:
 old='\\label{'+label+'}\n'+first
 assert addition.count(old)==1,(label,'statement-header layout marker')
 addition=addition.replace(old,'\\label{'+label+'}\n\\leavevmode\\par\n'+first)
marker=r'\section{Why simultaneous local exceptions have product size}'
assert s.count(marker)==1
s=s.replace(marker,addition+marker)
for k in ['tex_remaining_local','tex_next_target','tex_reading_order']:
 old=prev[k].strip();assert s.count(old)==1,(k,s.count(old))
 s=s.replace(old,cfg[k].strip())
start=s.index(r'\section{The arithmetic still to be written out}')
prefix,current=s[:start],s[start:]
a=current.index(r'\item[Actual local denominators and the two remaining cohomological suppliers.]')
b=current.index(r'\item[',a+1)
current=current[:a]+r'''\item[Actual local denominators and the remaining odd-plus supplier.]
LN supplies the conditional denominator/cut/restoration chain to the
original-family \texttt{LinkN}. Its actual local Galois inequalities
and type/theta/rank identities remain. LK/TB/KB now supply the
complete shared \texttt{LemmaK} chain, and TW supplies the full
simultaneous \texttt{ThmBab}. Alongside OB8 this leaves
\texttt{PointHV} at the major cohomological cut; CZ supplies its
exceptional \texttt{CountZ}, while the other counts and remaining
assembly are retained. The optional two-adic matrix route still
needs its actual module identification, host descent and strengthened
prime selection. The original \texttt{LinkV} and local summability
guards remain separate where invoked.
\textsf{[LK1--LK4, TB1--TB10, KB1--KB8, TW1--TW8, CZ1--CZ6, VW3--VW4]}

'''+current[b:]
old=r'''What remains
is the actual arithmetic gap and its size/error packages,
\texttt{ThmBab} and \texttt{PointHV}, and their installation on one
compatible host; the odd-minus supplier is now available from OB8.'''
new=r'''What remains
is the actual arithmetic gap and its size/error packages,
\texttt{PointHV}, and their installation on one compatible host.
The odd-minus supplier is OB8 and the simultaneous two-primary
and reference-layer supplier is now TW8.'''
assert current.count(old)==1
current=current.replace(old,new)
s=prefix+current
last=prev['tex_ledger_rows'][-1]+r'\\[3pt]'
assert s.count(last)==1
s=s.replace(last,last+'\n'+'\n'.join(x+r'\\[3pt]' for x in cfg['tex_ledger_rows']))
s=s.replace('with version-0.24 updates where an input','with version-0.25 updates where an input')
out=ROOT/'RH_readable_reconstruction_v0_25.tex';out.write_text(s)
print(out)
