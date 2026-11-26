#!/usr/bin/env python3
"""Assemble cumulative v0.15 TeX without producing a PDF."""
from pathlib import Path
import json
import re

ROOT=Path(__file__).resolve().parent
config=json.loads((ROOT/'increment_v0_15.json').read_text())
s=(ROOT/'history/version_0_14/RH_readable_reconstruction_v0_14.tex').read_text()
s=s.replace('working version 0.14','working version 0.15').replace('Working version 0.14','Working version 0.15')
s=s.replace('Explicit forms, values and adelic geometry','Column laws and the complete symmetric comparison')
s=s.replace('Canonical refill and quantitative block parameters','Complete numerical parameters and arithmetic constructors')
s=s.replace(r'Working notes for Benjamin Matschke\quad |\quad 21 November 2026',
            r'Working notes for Benjamin Matschke\quad |\quad 22 November 2026')
start=s.index(r'\textbf{What version 0.14 achieves.}')
end=s.index(r'\end{minipage}',start)
s=s[:start]+config['tex_front_summary']+'\n'+s[end:]

# The old proof fragments and their ledgers remain byte-for-byte preserved.
# Explicit bridges update their historical premise/status paragraphs in the
# cumulative note without silently rewriting a previously reviewed proof.
bridge=r'''\paragraph{Version-0.15 scope of the following conditional constructions.}
The following AD/DR/FC/CV/NB/VE/RF sections preserve their version-0.14
proofs and the hypotheses stated there. The additional law premise is now
supplied independently by TL13 in Section~\ref{sec:column-laws}, from
the literal \texttt{TC.Ok}. TG in Section~\ref{sec:terminal-geometry}
supplies the complete reference symmetric and terminal constructions.
PN and SZ complete every numerical parameter and size family, and AC
with SZ proves the three conditional arithmetic constructors isolated
by RF10. References below to those tasks as remaining describe their
historical stage; the current boundaries are stated in the new sections
and Section~\ref{sec:remaining}. Actual host, \texttt{Ok/Pins/Later},
analytic prime and geometric point suppliers are still retained where
specified.

'''
heading=r'\section{Explicit adelic base points and supported modifications}'
assert s.count(heading)==1
s=s.replace(heading,bridge+heading)

# Correct the previously current connective paragraph, not the LP proof.
start=s.index(r'\paragraph{Updated boundary of the point construction.}')
end=s.index(r'\paragraph{Version-0.15 scope of the following conditional constructions.}',start)
s=s[:start]+r'''\paragraph{Updated boundary of the point construction.}
LP patches the actual selected local lattices and installs their
ramification-normalized lengths. RF constructs canonical refill and
the conditional point installation. PN and SZ now complete the full
parameter/size package, while SZ constructs the initial size datum and
AC proves the coded-column and conditional level constructors. The
geometric \texttt{Lay/RecOK/LedOK/RecExP}, arithmetic host, top-window,
and analytic \texttt{LevelPrime} suppliers remain explicit. Thus neither
local patching nor one of the completed numerical records is an
additional open premise of the point construction.

'''+s[end:]

addition='\n\n'.join((ROOT/name/'main.tex').read_text() for name in config['tex_component_order'])+'\n\n'
def outer_split_tag(match):
    block=match.group()
    tags=re.findall(r'\\tag\{[^}]+\}',block)
    assert len(tags)<=1
    return block if not tags else block.replace(tags[0],'').rstrip()+'\n '+tags[0]
addition=re.sub(r'\\begin\{split\}[\s\S]*?\\end\{split\}',outer_split_tag,addition)
# A split environment accepts one alignment pair. Use aligned for the
# explanatory third columns in AC.9, preserving the reviewed proof bytes
# and changing only their presentation in the cumulative compilation.
def multi_column_alignment(match):
    block=match.group()
    if '&&' in block:
        block=block.replace(r'\begin{split}',r'\begin{aligned}',1)
        block=block.replace(r'\end{split}',r'\end{aligned}',1)
    return block
addition=re.sub(r'\\begin\{split\}[\s\S]*?\\end\{split\}',multi_column_alignment,addition)
def break_identifier(match):
    return r'\texttt{'+re.sub(r'\\_(?!\\allowbreak)',lambda _:r'\_\allowbreak ',match.group(1))+'}'
addition=re.sub(r'\\texttt\{([^{}]*)\}',break_identifier,addition)
marker=r'\section{Why simultaneous local exceptions have product size}'
assert s.count(marker)==1
s=s.replace(marker,addition+marker)

start=s.index('LI/SF/CR/CS prove the exact local identifications, common frame,',
              s.index(r'\section{The arithmetic still'))
end=s.index(r'\item[Theta identities',start)
s=s[:start]+config['tex_remaining_local']+'\n\n'+s[end:]
old_host_boundary=r'''assembly. Its remaining inputs are the actual \texttt{HostAx}/character
field and rank suppliers, \texttt{ShortNorm}, \texttt{SmallOne},
\texttt{ThinH}, \texttt{PairEx} and the cohomological window.
The predicate \texttt{HostParam.Seam.admitted} itself is constructed
from the supplied host fields; it is not an additional open interface.
The actual point constructor and its \texttt{NumAt} record also remain.'''
new_host_boundary=r'''assembly. Its remaining inputs are the actual \texttt{HostAx}/character
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
assert old_host_boundary in s
s=s.replace(old_host_boundary,new_host_boundary)
start=s.index(r'\paragraph{The next target: the remaining column and arithmetic suppliers.}')
end=s.index(r'\section{Claim ledger and reading order}',start)
s=s[:start]+config['tex_next_target']+'\n\n'+s[end:]

oldrow=r'RF1--16 & Refill, point and parameters & Canonical refill and conditional point installation; full ParamsT, seven parameter families and word count; fourteen families and SizesAt retained.\\[3pt]'
newrow=r'RF1--16 & Refill, point and parameters & Canonical refill, conditional point installation, full ParamsT and seven families; PN/SZ/AC now supply its remaining numerical and conditional constructor inputs.\\[3pt]'
assert oldrow in s
s=s.replace(oldrow,newrow+'\n'+'\n'.join(row+'\\\\[3pt]' for row in config['tex_ledger_rows']))
start=s.index('For the global spine, read Sections~',s.index(r'\section{Claim ledger'))
end=s.index('GJ4--GJ5 in Section~',start)
s=s[:start]+config['tex_reading_order']+'\n\n'+s[end:]
s=s.replace('with version-0.14 updates where an input','with version-0.15 updates where an input')
out=ROOT/'RH_readable_reconstruction_v0_15.tex'
out.write_text(s)
print(out)
