#!/usr/bin/env python3
"""Append v0.29 complete supplier/count chains and retain every historical proof."""
from pathlib import Path
import json
import re

ROOT = Path(__file__).resolve().parent
OLD = ROOT / 'history/version_0_28'
cfg = json.loads((ROOT / 'increment_v0_29.json').read_text())
prev = json.loads((OLD / 'increment_v0_28.json').read_text())
s = (OLD / 'RH_readable_reconstruction_v0_28.tex').read_text()
s = s.replace('working version 0.28', 'working version 0.29')
s = s.replace('Working version 0.28', 'Working version 0.29')
s = s.replace('Closing actual rigidity and the automorphic catalogue',
              'Closing the complete case-II count chain', 1)
s = s.replace('Complete cohomology and the reduced count frontier',
              'Actual seeds, promodularity and the remaining Hecke producer', 1)
a = s.index(r'\textbf{What version 0.28 achieves.}')
b = s.index(r'\end{minipage}', a)
s = s[:a] + cfg['tex_front_summary'] + '\n' + s[b:]
heading = r'\paragraph{Version-0.28 scope of the historical conditional proofs.}'
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
    old = old.replace('BX/IX/AX/DX/MX/PX/RX/CX/SP',
                      r'BX/IX/AX/DX/\allowbreak MX/PX/RX/CX/SP')
    assert s.count(old) == 1, (key, s.count(old))
    replacement = cfg[key].strip().replace(
        r'\texttt{NormChoiceFacts}/\texttt{Tie4}',
        r'\texttt{Norm\allowbreak Choice\allowbreak Facts}/\allowbreak \texttt{Tie4}')
    replacement = replacement.replace('BX/IX/AX/DX/MX/PX/RX/CX/SP',
                                      r'BX/IX/AX/DX/\allowbreak MX/PX/RX/CX/SP')
    s = s.replace(old, replacement)

start = s.index(r'\section{The arithmetic still to be written out}')
prefix, current = s[:start], s[start:]
a = current.index(r'\item[Actual local denominators and the reduced count input.]')
b = current.index(r'\item[', a + 1)
current = current[:a] + r'''\item[Actual local denominators and the case-II support producer.]
LN supplies the conditional denominator/cut/restoration chain to the
original-family \texttt{LinkN}; its actual Galois inequalities and
type/theta/rank identities remain.  SX supplies the actual case-II
seed; UX supplies its complete original-point promodular witness.
Together with BX/IX/AX/DX/MX/PX/RX/CX/SP, YX closes
\texttt{PMExAlt}$\Rightarrow$\texttt{CountII}.
KX supplies the universal arithmetic objects, and QX supplies the
adjoint theorem and five-clause tower join from the exact actual
rank-four ordinary Hecke/support input.  That producer remains.
The case-IV seed and case-III promodularity remain separate.
The added height/window sufficient input is \texttt{CountI},
\texttt{CountIII}, \texttt{CountV} and \texttt{PMExAlt}, with
the previously stated prime-pair hypotheses.  The optional two-adic
matrix route retains its actual module identification, host descent
and strengthened prime selection.  Original \texttt{LinkV} and
local summability guards retain their roles where invoked.
\textsf{[KX1--KX9, QX1--QX10, SX1--SX8, UX1--UX12, YX1--YX2]}

''' + current[b:]
s = prefix + current
old_current_gap = r'''is the actual arithmetic gap and its size/error packages, the four
actual \texttt{CountI/II/III/V} suppliers, and their installation
on one compatible host.  HV10 supplies the entire passage from
these counts to \texttt{PointHV}; OB8 and TW8 supply the odd-minus
and simultaneous two-primary/reference-layer branches.'''
new_current_gap = r'''is the actual arithmetic gap and its size/error packages,
\texttt{CountI}, \texttt{CountIII}, \texttt{CountV}, and
\texttt{PMExAlt}, with their installation on one compatible host.
YX2 supplies the entire \texttt{CountII} chain from \texttt{PMExAlt};
QX retains the actual rank-four ordinary Hecke/support producer.
HV10 supplies the passage from the four counts to \texttt{PointHV};
OB8 and TW8 supply the odd-minus and simultaneous
two-primary/reference-layer branches.'''
assert s.count(old_current_gap) == 1
s = s.replace(old_current_gap, new_current_gap)
last = prev['tex_ledger_rows'][-1] + r'\\[3pt]'
assert s.count(last) == 1
s = s.replace(last, last + '\n' + '\n'.join(row + r'\\[3pt]'
                                              for row in cfg['tex_ledger_rows']))
s = s.replace('with version-0.28 updates where an input',
              'with version-0.29 updates where an input')
out = ROOT / 'RH_readable_reconstruction_v0_29.tex'
out.write_text(s)
print(out)
