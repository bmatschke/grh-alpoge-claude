#!/usr/bin/env python3
"""Append v0.28 complete supplier/count chains and retain every historical proof."""
from pathlib import Path
import json
import re

ROOT = Path(__file__).resolve().parent
OLD = ROOT / 'history/version_0_27'
cfg = json.loads((ROOT / 'increment_v0_28.json').read_text())
prev = json.loads((OLD / 'increment_v0_27.json').read_text())
s = (OLD / 'RH_readable_reconstruction_v0_27.tex').read_text()
s = s.replace('working version 0.27', 'working version 0.28')
s = s.replace('Working version 0.27', 'Working version 0.28')
s = s.replace('Constructing the actual symplectic deformation model',
              'Closing actual rigidity and the automorphic catalogue', 1)
s = s.replace('Integral points, torus orbits and the paired-count frontier',
              'Complete cohomology and the reduced count frontier', 1)
a = s.index(r'\textbf{What version 0.27 achieves.}')
b = s.index(r'\end{minipage}', a)
s = s[:a] + cfg['tex_front_summary'] + '\n' + s[b:]
heading = r'\paragraph{Version-0.27 scope of the historical conditional proofs.}'
assert s.count(heading) == 1
s = s.replace(heading, cfg['tex_scope_bridge'] + heading)

addition = '\n\n'.join((ROOT / c / 'main.tex').read_text()
                       for c in cfg['tex_component_order'])
addition += '\n\n' + cfg['tex_dependency_update']

def mono_breaks(match):
    body = re.sub(r'(?<=[a-z])(?=[A-Z])', lambda _: r'\allowbreak ', match[1])
    body = re.sub(r'\.(?!\\allowbreak)', lambda _: r'.\allowbreak ', body)
    body = re.sub(r'\\_(?!\\allowbreak)', lambda _: r'\_\allowbreak ', body)
    return r'\texttt{' + body + '}'

addition = re.sub(r'\\texttt\{([^{}]*)\}', mono_breaks, addition)
addition = addition.replace('metric/global/spectral',
                            r'metric/\allowbreak global/\allowbreak spectral')
marker = r'\section{Why simultaneous local exceptions have product size}'
assert s.count(marker) == 1
s = s.replace(marker, addition + marker)
for key in ['tex_remaining_local', 'tex_next_target', 'tex_reading_order']:
    old = prev[key].strip().replace('form/lattice/signature',
                                   r'form/\allowbreak lattice/\allowbreak signature')
    old = old.replace(r'\texttt{NormChoiceFacts}/\texttt{Tie4}',
                      r'\texttt{Norm\allowbreak Choice\allowbreak Facts}/\allowbreak \texttt{Tie4}')
    assert s.count(old) == 1, (key, s.count(old))
    replacement = cfg[key].strip().replace(
        r'\texttt{NormChoiceFacts}/\texttt{Tie4}',
        r'\texttt{Norm\allowbreak Choice\allowbreak Facts}/\allowbreak \texttt{Tie4}')
    s = s.replace(old, replacement)

start = s.index(r'\section{The arithmetic still to be written out}')
prefix, current = s[:start], s[start:]
a = current.index(r'\item[Actual local denominators and the four remaining count suppliers.]')
b = current.index(r'\item[', a + 1)
current = current[:a] + r'''\item[Actual local denominators and the reduced count input.]
LN supplies the conditional denominator/cut/restoration chain to the
original-family \texttt{LinkN}; its actual Galois inequalities and
type/theta/rank identities remain.  BX supplies complete actual
cohomology records.  AX/DX/MX/PX supply the actual symplectic datum,
model and comparison; RX supplies its actual irreducible rigidity
and CX the exact uniform catalogue.  JX1 therefore reduces the paired
counts to the literal image-density predicate.  IX closes its internal
actual-point and promodular transports, retaining their modular
quotient/link/support and arithmetic seed producers.
The selected height/window input is now \texttt{CountI},
\texttt{CountV}, and image density.  JX2, HV, TW, OB and VW supply
the entire downstream original-field assembly with its stated
prime-pair inputs.  The optional two-adic matrix route retains its
actual module identification, host descent and strengthened prime
selection.  Original \texttt{LinkV} and local summability guards
retain their roles where invoked.
\textsf{[BX1--BX8, RX1--RX7, CX1--CX9, IX1--IX10, JX1--JX2]}

''' + current[b:]
s = prefix + current
last = prev['tex_ledger_rows'][-1] + r'\\[3pt]'
assert s.count(last) == 1
s = s.replace(last, last + '\n' + '\n'.join(row + r'\\[3pt]'
                                              for row in cfg['tex_ledger_rows']))
s = s.replace('with version-0.27 updates where an input',
              'with version-0.28 updates where an input')
out = ROOT / 'RH_readable_reconstruction_v0_28.tex'
out.write_text(s)
print(out)
