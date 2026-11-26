#!/usr/bin/env python3
"""Append the reviewed v0.26 proof chapters without changing historical proofs."""
from pathlib import Path
import json,re

ROOT=Path(__file__).resolve().parent
OLD=ROOT/'history/version_0_25'
cfg=json.loads((ROOT/'increment_v0_26.json').read_text())
prev=json.loads((OLD/'increment_v0_25.json').read_text())
s=(OLD/'RH_readable_reconstruction_v0_25.tex').read_text()
s=s.replace('working version 0.25','working version 0.26').replace('Working version 0.25','Working version 0.26')
s=s.replace('The complete shared cohomology and simultaneous-window chains',
            'Closing the rank-one and weighted-intersection suppliers',1)
s=s.replace('Arithmetic torsion, K-theory and exceptional vanishing',
            'Original-field height comparison and the four-count frontier',1)
a=s.index(r'\textbf{What version 0.25 achieves.}'); b=s.index(r'\end{minipage}',a)
s=s[:a]+cfg['tex_front_summary']+'\n'+s[b:]
heading=r'\paragraph{Version-0.25 scope of the historical conditional proofs.}'
assert s.count(heading)==1
s=s.replace(heading,cfg['tex_scope_bridge']+heading)
addition='\n\n'.join((ROOT/c/'main.tex').read_text()for c in cfg['tex_component_order'])+'\n\n'+cfg['tex_dependency_update']
def mono_breaks(m):
    body=re.sub(r'(?<=[a-z])(?=[A-Z])',lambda _:r'\allowbreak ',m[1])
    body=body.replace('.',r'.\allowbreak ')
    body=re.sub(r'\\_(?!\\allowbreak)',lambda _:r'\_\allowbreak ',body)
    return r'\texttt{'+body+'}'
addition=re.sub(r'\\texttt\{([^{}]*)\}',mono_breaks,addition)
addition=addition.replace(
    r'\section{Original-field character comparison and the complete PointHV assembly}',
    r'\section{Original-field comparison and the complete PointHV assembly}',1)
marker=r'\section{Why simultaneous local exceptions have product size}'
assert s.count(marker)==1
s=s.replace(marker,addition+marker)
for key in ['tex_remaining_local','tex_next_target','tex_reading_order']:
    old=prev[key].strip(); assert s.count(old)==1,(key,s.count(old))
    replacement=cfg[key].strip().replace('form/lattice/signature',
        r'form/\allowbreak lattice/\allowbreak signature')
    s=s.replace(old,replacement)
start=s.index(r'\section{The arithmetic still to be written out}')
prefix,current=s[:start],s[start:]
a=current.index(r'\item[Actual local denominators and the remaining odd-plus supplier.]')
b=current.index(r'\item[',a+1)
current=current[:a]+r'''\item[Actual local denominators and the four remaining count suppliers.]
LN supplies the conditional denominator/cut/restoration chain to the
original-family \texttt{LinkN}.  Its actual Galois inequalities and
type/theta/rank identities remain.  The LK/\allowbreak TB/\allowbreak KB/\allowbreak TW/\allowbreak OB/\allowbreak CZ cohomological
suppliers are available.  RV, BR, SP and FP now supply the exact
rank-one, residual and universal algebra theorems.  HV supplies
\texttt{CountVs}, \texttt{CountIV} and the entire original-field
count-to-\texttt{PointHV} assembly.  The actual four predicates
\texttt{CountI/II/III/V}, including their compatible arithmetic model,
automorphy, catalogue and rigidity requirements, remain.  The optional
two-adic matrix route still needs its actual module identification,
host descent and strengthened prime selection.  The original
\texttt{LinkV} and local summability guards remain where invoked.
\textsf{[RV1--RV7, BR1--BR7, SP1--SP10, FP, HV1--HV10]}

'''+current[b:]
old=r'''What remains
is the actual arithmetic gap and its size/error packages,
\texttt{PointHV}, and their installation on one compatible host.
The odd-minus supplier is OB8 and the simultaneous two-primary
and reference-layer supplier is now TW8.'''
new=r'''What remains
is the actual arithmetic gap and its size/error packages, the four
actual \texttt{CountI/II/III/V} suppliers, and their installation
on one compatible host.  HV10 supplies the entire passage from
these counts to \texttt{PointHV}; OB8 and TW8 supply the odd-minus
and simultaneous two-primary/reference-layer branches.'''
assert current.count(old)==1
current=current.replace(old,new)
s=prefix+current
last=prev['tex_ledger_rows'][-1]+r'\\[3pt]'
assert s.count(last)==1
s=s.replace(last,last+'\n'+'\n'.join(row+r'\\[3pt]'for row in cfg['tex_ledger_rows']))
s=s.replace('with version-0.25 updates where an input','with version-0.26 updates where an input')
out=ROOT/'RH_readable_reconstruction_v0_26.tex'
out.write_text(s)
print(out)
