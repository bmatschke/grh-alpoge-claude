#!/usr/bin/env python3
"""Assemble the cumulative v0.16 note, retaining prior proof fragments."""
from pathlib import Path
import json
import re

ROOT=Path(__file__).resolve().parent
OLD=ROOT/'history/version_0_15'
config=json.loads((ROOT/'increment_v0_16.json').read_text())
oldconfig=json.loads((OLD/'increment_v0_15.json').read_text())
s=(OLD/'RH_readable_reconstruction_v0_15.tex').read_text()
s=s.replace('working version 0.15','working version 0.16').replace('Working version 0.15','Working version 0.16')
s=s.replace('Column laws and the complete symmetric comparison','Arithmetic hosts, periods and normalized theta')
s=s.replace('Complete numerical parameters and arithmetic constructors','Canonical local indices and the complete twisted comparison')
start=s.index(r'\textbf{What version 0.15 achieves.}')
end=s.index(r'\end{minipage}',start)
s=s[:start]+config['tex_front_summary']+'\n'+s[end:]

bridge=r'''\paragraph{Version-0.16 scope of the historical conditional proofs.}
The following previously reconstructed proofs retain their stated inputs
and their original text. AH in Section~\ref{sec:arithmetic-hosts} now
constructs the conditional arithmetic host and character field; PA in
Section~\ref{sec:period-arithmetic} supplies its periods and trace
isometries; TA in Section~\ref{sec:theta-arithmetic} supplies the
one-dimensional normalized theta arithmetic; CI in
Section~\ref{sec:canonical-indices} supplies the local-index and
nonvanishing theorems; and TX in Section~\ref{sec:twisted-comparison}
supplies the standard all-twist comparison. References below to those
tasks as future work describe the historical stage, not the present
boundary. The current remaining hypotheses are stated in the new
sections and Section~\ref{sec:remaining}. In particular the actual
multivariable vacuum/indicator/covariance, normalized arithmetic
\texttt{NChoice}/\texttt{TupTied}, \texttt{Pins.iX}, \texttt{Later},
and the analytic/geometric/global branches are still distinguished.

'''
heading=r'\paragraph{Version-0.15 scope of the following conditional constructions.}'
assert s.count(heading)==1
s=s.replace(heading,bridge+heading)
start=s.index(r'\paragraph{Updated boundary of the point construction.}')
end=s.index(r'\paragraph{Version-0.16 scope of the historical conditional proofs.}',start)
s=s[:start]+r'''\paragraph{Updated boundary of the point construction.}
LP patches the actual selected local lattices and installs their
ramification-normalized lengths. RF constructs canonical refill and
conditional point installation. PN/SZ complete the numerical package;
SZ constructs initial size and rank data; AC gives coded columns and
the conditional level datum. AH now constructs the actual field/host
under its literal $q,d$ and splitting hypotheses. The remaining
existence inputs include the analytic prime and top/logarithmic windows
and the geometric \texttt{Lay/RecOK/LedOK/RecExP} with its mass/window
estimates. The new local period/theta/index/comparison arguments do
not themselves construct those geometric points.

'''+s[end:]

addition='\n\n'.join((ROOT/c/'main.tex').read_text()for c in config['tex_component_order'])+'\n\n'
def outer_split_tag(match):
 block=match.group();tags=re.findall(r'\\tag\{[^}]+\}',block)
 assert len(tags)<=1
 return block if not tags else block.replace(tags[0],'').rstrip()+'\n '+tags[0]
addition=re.sub(r'\\begin\{split\}[\s\S]*?\\end\{split\}',outer_split_tag,addition)
def multi_column(match):
 block=match.group()
 return block.replace(r'\begin{split}',r'\begin{aligned}',1).replace(r'\end{split}',r'\end{aligned}',1)if'&&'in block else block
addition=re.sub(r'\\begin\{split\}[\s\S]*?\\end\{split\}',multi_column,addition)
def break_identifier(match):
 return r'\texttt{'+re.sub(r'\\_(?!\\allowbreak)',lambda _:r'\_\allowbreak ',match.group(1))+'}'
addition=re.sub(r'\\texttt\{([^{}]*)\}',break_identifier,addition)
marker=r'\section{Why simultaneous local exceptions have product size}'
assert s.count(marker)==1
s=s.replace(marker,addition+marker)

old=oldconfig['tex_remaining_local'].strip()
assert s.count(old)==1
s=s.replace(old,config['tex_remaining_local'].strip())
old_host=r'''assembly. Its remaining inputs are the actual \texttt{HostAx}/character
field, \texttt{ShortNorm}, \texttt{SmallOne}, \texttt{ThinH},
\texttt{PairEx} and the cohomological window. SZ13 now constructs the
required ranks over prescribed and cyclic frames; the number field with
those labels remains an arithmetic input. AC2--AC3 also prove the
root-of-unity norm component of \texttt{HostDer}; its other arithmetic
fields remain to be supplied.
The predicate \texttt{HostParam.Seam.admitted} itself is constructed
from the supplied host fields. Actual geometric point supply remains;
the conditional \texttt{NumAt} construction is now complete by PN16
and SZ9, on the initial size datum supplied by SZ10--SZ12.'''
new_host=r'''assembly. AH17--AH18 now supply the actual conditional
\texttt{HostAx}/character-field arithmetic, including every derived
host field and its selected half-different. The remaining inputs include
the prime/splitting hypotheses in the required analytic windows,
\texttt{ShortNorm}, \texttt{SmallOne}, \texttt{ThinH}, \texttt{PairEx}
and the cohomological window. SZ13 supplies the prescribed and cyclic
rank constructions, with their original order-window antecedents.
The predicate \texttt{HostParam.Seam.admitted} is constructed from
the supplied fields. Actual geometric point supply remains; PN16/SZ9
give the conditional \texttt{NumAt} on SZ10--SZ12's initial size datum.'''
assert old_host in s
s=s.replace(old_host,new_host)
for k in ['tex_next_target','tex_reading_order']:
 old=oldconfig[k].strip();assert s.count(old)==1,(k,s.count(old))
 s=s.replace(old,config[k].strip())
last=oldconfig['tex_ledger_rows'][-1]+r'\\[3pt]'
assert s.count(last)==1
s=s.replace(last,last+'\n'+'\n'.join(row+r'\\[3pt]'for row in config['tex_ledger_rows']))
s=s.replace('with version-0.15 updates where an input','with version-0.16 updates where an input')
out=ROOT/'RH_readable_reconstruction_v0_16.tex'
out.write_text(s)
print(out)
