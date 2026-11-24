#!/usr/bin/env python3
"""Validate the component in pdflatex draft mode; never produce a PDF."""
from pathlib import Path
import hashlib
import json
import os
import re
import subprocess

HERE=Path(__file__).resolve().parent
BUILD=HERE/'validation'
BUILD.mkdir(exist_ok=True)
env=os.environ.copy()
trees=[Path('/usr/share/texlive/texmf-dist'),Path('/usr/share/texmf'),Path('/etc/texmf')]
env['TEXMF']='{'+','.join(str(p)for p in trees if p.is_dir())+'}'
env['TEXFONTMAPS']=str(BUILD)+':'
maps=[trees[1]/'fonts/map/dvips/lm/lm.map',trees[0]/'fonts/map/dvips/amsfonts/cm.map',
      trees[0]/'fonts/map/dvips/amsfonts/symbols.map',trees[0]/'fonts/map/dvips/amsfonts/euler.map',
      trees[0]/'fonts/map/dvips/amsfonts/latxfont.map',trees[0]/'fonts/map/dvips/amsfonts/cmextra.map']
(BUILD/'pdftex.map').write_text('\n'.join(p.read_text()for p in maps))
fmt=HERE.parent/'build/pdflatex.fmt'
if not fmt.is_file():
    fmt=BUILD/'pdflatex.fmt'
    if not fmt.is_file():
        p=subprocess.run(['pdftex','-ini','-etex','-no-shell-escape','-interaction=nonstopmode',
            '-halt-on-error','-jobname=pdflatex',f'-output-directory={BUILD}',r'\input pdflatex.ini'],
            cwd=BUILD,env=env,capture_output=True,text=True)
        (BUILD/'format_build.txt').write_text(p.stdout+p.stderr)
        if p.returncode: raise SystemExit((p.stdout+p.stderr)[-4000:])

preamble=r'''\documentclass[11pt,a4paper]{article}
\usepackage[T1]{fontenc}
\usepackage[utf8]{inputenc}
\usepackage{lmodern,amsmath,amssymb,amsthm,mathtools,microtype,mathrsfs}
\usepackage[margin=25mm,top=23mm,bottom=25mm]{geometry}
\usepackage[colorlinks=true]{hyperref}
\setlength{\parindent}{0pt}
\setlength{\parskip}{5pt plus 1pt}
\newtheorem{theorem}{Theorem}[section]
\newtheorem{proposition}[theorem]{Proposition}
\newcommand{\status}[1]{\textbf{Status:} #1}
\begin{document}
\input{../main.tex}
\end{document}
'''
(BUILD/'check.tex').write_text(preamble)
for i in range(1,4):
    p=subprocess.run(['pdflatex',f'-fmt={fmt}','-draftmode','-no-shell-escape',
        '-interaction=nonstopmode','-halt-on-error','check.tex'],
        cwd=BUILD,env=env,capture_output=True,text=True)
    (BUILD/f'pass_{i}.txt').write_text(p.stdout+p.stderr)
    if p.returncode:raise SystemExit((p.stdout+p.stderr)[-4500:])
    log=(BUILD/'check.log').read_text()
    if i>=2 and not any(t in log for t in ['Rerun to get','Label(s) may have changed','rerunfilecheck Warning']):break
assert not (BUILD/'check.pdf').exists()
report={
 'artifact_version':'0.27','component':'symplectic_arithmetic_data',
 'main_tex_sha256':hashlib.sha256((HERE/'main.tex').read_bytes()).hexdigest(),
 'syntax_compile_succeeded':True,'passes':i,'pdf_generated':False,
 'undefined_references_or_citations':any(t in log for t in ['undefined references','undefined citations','Citation `']),
 'missing_character_warnings':log.count('Missing character'),
 'overfull_box_warnings':len(re.findall(r'Overfull \\[hv]box',log)),
 'warnings':[s.strip()for s in log.splitlines()if 'Warning' in s],
 'scope':'Draft-mode syntax/font/reference check only; no PDF rendering or mathematical verification.',
 'log_sha256':hashlib.sha256(log.encode()).hexdigest()
}
(HERE/'tex_validation.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(report,indent=2))
