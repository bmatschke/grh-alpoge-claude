#!/usr/bin/env python3
"""Append v0.27 actual symplectic chains and retain every historical proof."""
from pathlib import Path
import json
import re

ROOT = Path(__file__).resolve().parent
OLD = ROOT / 'history/version_0_26'
cfg = json.loads((ROOT / 'increment_v0_27.json').read_text())
prev = json.loads((OLD / 'increment_v0_26.json').read_text())
s = (OLD / 'RH_readable_reconstruction_v0_26.tex').read_text()
s = s.replace('working version 0.26', 'working version 0.27')
s = s.replace('Working version 0.26', 'Working version 0.27')
s = s.replace('Closing the rank-one and weighted-intersection suppliers',
              'Constructing the actual symplectic deformation model', 1)
s = s.replace('Original-field height comparison and the four-count frontier',
              'Integral points, torus orbits and the paired-count frontier', 1)
a = s.index(r'\textbf{What version 0.26 achieves.}')
b = s.index(r'\end{minipage}', a)
s = s[:a] + cfg['tex_front_summary'] + '\n' + s[b:]
heading = r'\paragraph{Version-0.26 scope of the historical conditional proofs.}'
assert s.count(heading) == 1
s = s.replace(heading, cfg['tex_scope_bridge'] + heading)

addition = '\n\n'.join((ROOT / c / 'main.tex').read_text()
                       for c in cfg['tex_component_order'])
addition += '\n\n' + cfg['tex_dependency_update']

def mono_breaks(match):
    body = re.sub(r'(?<=[a-z])(?=[A-Z])', lambda _: r'\allowbreak ', match[1])
    body = body.replace('.', r'.\allowbreak ')
    body = re.sub(r'\\_(?!\\allowbreak)', lambda _: r'\_\allowbreak ', body)
    return r'\texttt{' + body + '}'

addition = re.sub(r'\\texttt\{([^{}]*)\}', mono_breaks, addition)
marker = r'\section{Why simultaneous local exceptions have product size}'
assert s.count(marker) == 1
s = s.replace(marker, addition + marker)
for key in ['tex_remaining_local', 'tex_next_target', 'tex_reading_order']:
    old = prev[key].strip().replace('form/lattice/signature',
                                   r'form/\allowbreak lattice/\allowbreak signature')
    assert s.count(old) == 1, (key, s.count(old))
    replacement = cfg[key].strip().replace(
        r'\texttt{NormChoiceFacts}/\texttt{Tie4}',
        r'\texttt{Norm\allowbreak Choice\allowbreak Facts}/\allowbreak \texttt{Tie4}')
    s = s.replace(old, replacement)

start = s.index(r'\section{The arithmetic still to be written out}')
prefix, current = s[:start], s[start:]
a = current.index(r'\item[Actual local denominators and the four remaining count suppliers.]')
b = current.index(r'\item[', a + 1)
current = current[:a] + r'''\item[Actual local denominators and the four remaining count suppliers.]
LN supplies the conditional denominator/cut/restoration chain to the
original-family \texttt{LinkN}; its actual Galois inequalities and
type/theta/rank identities remain.  The shared cohomology, rank-one,
residual and universal algebra suppliers are available.  AX/DX/MX now
construct the actual symplectic datum and deformation model; PX supplies
its internal point/orbit/tangent/trace comparison.  The paired-count
route retains the literal image-density predicate, actual same-datum
irreducible rigidity and the exact uniform automorphic catalogue.
HV supplies \texttt{CountVs}, \texttt{CountIV} and the entire
original-field count-to-\texttt{PointHV} assembly.  The actual
\texttt{CountI/II/III/V} predicates remain.  The optional two-adic matrix
route retains its actual module identification, host descent and
strengthened prime selection.  Original \texttt{LinkV} and local
summability guards retain their roles where invoked.
\textsf{[AX1--AX10, DX1--DX8, MX1--MX10, PX1--PX10, SP9--SP10, HV10]}

''' + current[b:]
s = prefix + current
last = prev['tex_ledger_rows'][-1] + r'\\[3pt]'
assert s.count(last) == 1
s = s.replace(last, last + '\n' + '\n'.join(row + r'\\[3pt]'
                                              for row in cfg['tex_ledger_rows']))
s = s.replace('with version-0.26 updates where an input',
              'with version-0.27 updates where an input')
out = ROOT / 'RH_readable_reconstruction_v0_27.tex'
out.write_text(s)
print(out)
