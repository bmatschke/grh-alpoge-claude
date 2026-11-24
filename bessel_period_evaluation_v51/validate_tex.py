#!/usr/bin/env python3
"""Validate the original bessel_period_evaluation_v51 chapter as two-pass draft TeX; produces no PDF."""
from pathlib import Path
import argparse
import hashlib
import json
import os
import re
import subprocess

HERE = Path(__file__).resolve().parent
parser = argparse.ArgumentParser()
parser.add_argument('--format', type=Path)
args = parser.parse_args()
work = HERE / 'validation'
work.mkdir(exist_ok=True)
(work / 'check.tex').write_text(r'''\documentclass[11pt]{article}
\usepackage[a4paper,margin=25mm]{geometry}
\usepackage{amsmath,amssymb,amsthm,mathtools}
\usepackage[T1]{fontenc}
\usepackage{lmodern}
\usepackage[unicode]{hyperref}
\newcommand{\status}[1]{\par\noindent\textbf{Status.} #1\par}
\setlength{\emergencystretch}{3em}
\begin{document}
\input{../main.tex}
\end{document}
''')
cmd = ['pdflatex', '-no-shell-escape', '-interaction=nonstopmode',
       '-halt-on-error', '-draftmode', 'check.tex']
if args.format:
    cmd.insert(1, '-fmt=' + str(args.format.resolve()))
env = os.environ.copy()
env['TEXMF'] = '{/usr/share/texlive/texmf-dist,/usr/share/texmf,/etc/texmf}'
passes = []
for n in [1, 2]:
    r = subprocess.run(cmd, cwd=work, env=env, text=True,
                       stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    (work / f'pass_{n}.txt').write_text(r.stdout)
    passes.append({'pass': n, 'returncode': r.returncode})
    if r.returncode:
        raise SystemExit(r.stdout[-8000:])
log = (work / 'check.log').read_text()
diagnostics = {
    'overfull_boxes': len(re.findall(r'Overfull \\[hv]box', log)),
    'missing_characters': len(re.findall('Missing character:', log)),
    'undefined_references': len(re.findall(r'(?:Reference|Citation).*undefined|There were undefined references', log)),
    'latex_errors': len(re.findall(r'^!', log, re.M)),
}
record = {
    'schema': 'rh-standalone-tex-validation/1',
    'component': 'bessel_period_evaluation_v51', 'artifact_version': '0.51',
    'proof_file_sha256': hashlib.sha256((HERE / 'main.tex').read_bytes()).hexdigest(),
    'status': 'PASS' if not any(diagnostics.values()) else 'REVIEW',
    'mode': 'two-pass draft TeX; no PDF; no Lean replay',
    'passes': passes, 'diagnostics': diagnostics,
}
(HERE / 'tex_validation.json').write_text(json.dumps(record, indent=2) + '\n')
print(json.dumps(record, indent=2))
if record['status'] != 'PASS':
    print('\n'.join(l for l in log.splitlines() if 'Overfull' in l))
    raise SystemExit(1)
