#!/usr/bin/env python3
"""Append frozen v0.24 proofs and update only current connective/scope prose."""
from pathlib import Path
import json,re

ROOT=Path(__file__).resolve().parent
OLD=ROOT/'history/version_0_23'
cfg=json.loads((ROOT/'increment_v0_24.json').read_text())
prev=json.loads((OLD/'increment_v0_23.json').read_text())
s=(OLD/'RH_readable_reconstruction_v0_23.tex').read_text()
s=s.replace('working version 0.23','working version 0.24').replace('Working version 0.23','Working version 0.24')
s=s.replace('Closing coefficient, cohomological and character chains','The complete odd-minus cohomological supplier')
s=s.replace('An explicit audit of the remaining arithmetic dependencies','Congruence transport and the remaining dependency chains')
a=s.index(r'\textbf{What version 0.23 achieves.}');b=s.index(r'\end{minipage}',a)
s=s[:a]+cfg['tex_front_summary']+'\n'+s[b:]
bridge=r'''\paragraph{Version-0.24 scope of the historical conditional proofs.}
Historical mathematical proofs and their original hypotheses are preserved.
LD1--LD4 now supply the stated finite-duality and unramified-reciprocity
interfaces relative to exact classical theorems. OS1--OS9 prove the
literal \texttt{PsiBound} supplier, and OB1--OB8 prove
\texttt{ThmBcFree} with constant $240$. Thus the odd-minus input
in VW3--VW4, QP25 and the earlier cohomological budget is now supplied;
older statements that it remains to be written are historical.
The remaining bespoke cohomological cut is \texttt{ThmBab} plus
\texttt{PointHV}, on the same original fields and simultaneous windows.
LN1--LN10 prove the conditional integral-cut, congruence-length,
prime-summation and original-family \texttt{LinkN} chain. Their
actual local Galois tables and type/theta/rank compatibility inputs
remain open; the stronger arithmetic cut is not inferred from a
good cut. The full arithmetic family/gap, genuine theta/local data,
global spectral estimates and exact metric transport remain required.
The current frontier is stated in Sections~\ref{sec:dependency-audit-v24}
and~\ref{sec:remaining}; the standalone version-0.24 audit records
the same-object and quantifier obligations explicitly.

'''
heading=r'\paragraph{Version-0.23 scope of the historical conditional proofs.}'
assert s.count(heading)==1
s=s.replace(heading,bridge+heading)
addition='\n\n'.join((ROOT/c/'main.tex').read_text() for c in cfg['tex_component_order'])+'\n\n'+cfg['tex_dependency_update']
# Typographic break opportunities only; the frozen component files retain
# exact proof-range hashes and remain the canonical claim locators.
def mono_breaks(m):
 body=re.sub(r'(?<=[a-z])(?=[A-Z])',lambda _:r'\allowbreak ',m[1])
 body=body.replace('.',r'.\allowbreak ')
 body=re.sub(r'\\_(?!\\allowbreak)',lambda _:r'\_\allowbreak ',body)
 return r'\texttt{'+body+'}'
addition=re.sub(r'\\texttt\{([^{}]*)\}',mono_breaks,addition)
marker=r'\section{Why simultaneous local exceptions have product size}'
assert s.count(marker)==1
s=s.replace(marker,addition+marker)
for k in ['tex_remaining_local','tex_next_target','tex_reading_order']:
 old=prev[k].strip();assert s.count(old)==1,(k,s.count(old))
 s=s.replace(old,cfg[k].strip())
start=s.index(r'\section{The arithmetic still to be written out}')
prefix,current=s[:start],s[start:]
old=r'''\item[Congruence denominators and cohomological windows.]
The integral comparisons \texttt{LinkN} and \texttt{LinkV} must still control the denominators introduced by rational projectors. The cohomological window has two-primary, odd-minus, and odd-plus parts. GH makes the general character field and the degree factor $c$ explicit, but does not prove these windows for its growing tower. The optional two-adic matrix lemma still lacks its actual module identification, host descent, and simultaneous strengthened prime selection. \textsf{[OH6--OH8, GH3, GH5, GH7]}'''
new=r'''\item[Actual local denominators and the two remaining cohomological suppliers.]
LN supplies the entire conditional denominator/cut/restoration chain
to original-family \texttt{LinkN}; its actual local Galois inequalities
and type/theta/rank identities must now be supplied. The exact
cohomological window retains \texttt{ThmBab} and \texttt{PointHV};
the odd-minus \texttt{ThmBcFree} branch is complete in LD/OS/OB.
The optional two-adic matrix route still needs its actual module
identification, host descent and simultaneous strengthened prime
selection. The original \texttt{LinkV} and local summability guards
remain separate obligations where invoked.
\textsf{[LD1--LD4, OS1--OS9, OB1--OB8, LN1--LN10, VW3--VW4]}'''
assert current.count(old)==1
current=current.replace(old,new)
old=r'''What remains
is the actual arithmetic gap and its size/error packages, the deep
cohomological estimates, and their installation on one compatible host.'''
new=r'''What remains
is the actual arithmetic gap and its size/error packages,
\texttt{ThmBab} and \texttt{PointHV}, and their installation on one
compatible host; the odd-minus supplier is now available from OB8.'''
assert current.count(old)==1
current=current.replace(old,new)
s=prefix+current
last=prev['tex_ledger_rows'][-1]+r'\\[3pt]'
assert s.count(last)==1
s=s.replace(last,last+'\n'+'\n'.join(x+r'\\[3pt]' for x in cfg['tex_ledger_rows']))
s=s.replace('with version-0.23 updates where an input','with version-0.24 updates where an input')
out=ROOT/'RH_readable_reconstruction_v0_24.tex';out.write_text(s)
print(out)
