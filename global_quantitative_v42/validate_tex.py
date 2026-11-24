#!/usr/bin/env python3
"""Draft-mode syntax and reference check; no PDF or visual-layout claim."""
from pathlib import Path
import hashlib
import json
import os
import re
import subprocess

here=Path(__file__).resolve().parent
out=here/'validation'
out.mkdir(exist_ok=True)
env=os.environ.copy()
trees=[Path('/usr/share/texlive/texmf-dist'),Path('/usr/share/texmf'),Path('/etc/texmf')]
env['TEXMF']='{'+','.join(str(p) for p in trees if p.is_dir())+'}'
env['TEXFONTMAPS']=str(out)+':'
maps=[trees[1]/'fonts/map/dvips/lm/lm.map',trees[0]/'fonts/map/dvips/amsfonts/cm.map',
      trees[0]/'fonts/map/dvips/amsfonts/symbols.map',trees[0]/'fonts/map/dvips/amsfonts/euler.map',
      trees[0]/'fonts/map/dvips/amsfonts/latxfont.map',trees[0]/'fonts/map/dvips/amsfonts/cmextra.map']
(out/'pdftex.map').write_text('\n'.join(p.read_text() for p in maps if p.is_file()))
fmt=out/'pdflatex.fmt'
if not fmt.is_file():
    p=subprocess.run(['pdftex','-ini','-etex','-no-shell-escape','-interaction=nonstopmode',
        '-halt-on-error','-jobname=pdflatex',f'-output-directory={out}',r'\input pdflatex.ini'],
        cwd=out,env=env,capture_output=True,text=True)
    (out/'format_build.txt').write_text(p.stdout+p.stderr)
    if p.returncode:
        raise SystemExit((p.stdout+p.stderr)[-4000:])
(out/'check.tex').write_text(r'''\documentclass[11pt]{article}
\usepackage[margin=1in]{geometry}
\usepackage{amsmath,amssymb,amsthm,hyperref}
\newcommand{\status}[1]{\par\noindent\textbf{Status.} #1\par}
\begin{document}
\input{../main.tex}
\end{document}
''')
for i in range(1,5):
    p=subprocess.run(['pdflatex',f'-fmt={fmt}','-draftmode','-no-shell-escape',
        '-interaction=nonstopmode','-halt-on-error','check.tex'],cwd=out,env=env,capture_output=True,text=True)
    (out/f'pass_{i}.txt').write_text(p.stdout+p.stderr)
    if p.returncode:
        raise SystemExit((p.stdout+p.stderr)[-3000:])
    log=(out/'check.log').read_text()
    rerun=any(w in log for w in ('Rerun to get','Label(s) may have changed','rerunfilecheck Warning','undefined references'))
    if i>=2 and not rerun:
        break
else:
    raise SystemExit('Unresolved TeX references after four passes.')
result=dict(artifact_version='0.42',component='global_quantitative_v42',
    method='offline pdflatex -draftmode -no-shell-escape',
    main_tex_sha256=hashlib.sha256((here/'main.tex').read_bytes()).hexdigest(),
    syntax_compile_succeeded=True,passes=i,pdf_generated=False,
    visual_layout_review_performed=False,mathematical_verification_claimed=False,
    undefined_references=False,overfull_box_warnings=len(re.findall(r'Overfull \\[hv]box',log)),
    missing_characters=log.count('Missing character'),
    warnings=[s.strip() for s in log.splitlines() if 'Warning' in s])
assert not (out/'check.pdf').exists()
(here/'tex_validation.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
