#!/usr/bin/env python3
"""Check UX in two draft-mode passes; no PDF is generated."""
from pathlib import Path
import hashlib
import json
import os
import re
import subprocess

here = Path(__file__).resolve().parent
build = here / 'build'
build.mkdir(exist_ok=True)
master = here.parent / 'RH_readable_reconstruction_v0_28.tex'
preamble = master.read_text().split(r'\begin{document}', 1)[0]
wrapper = build / 'promodular_realization_check.tex'
wrapper.write_text(preamble + '\\begin{document}\n\\input{../main.tex}\n\\end{document}\n')
env = os.environ.copy()
env['TEXMF'] = '{/usr/share/texlive/texmf-dist,/usr/share/texmf,/etc/texmf}'
env['TEXFONTMAPS'] = str(here.parent / 'build') + ':'
fmt = here.parent / 'build' / 'pdflatex.fmt'
for i in range(2):
    p = subprocess.run(['pdflatex','-fmt='+str(fmt),'-draftmode','-no-shell-escape',
                        '-interaction=nonstopmode','-halt-on-error',wrapper.name],
                       cwd=build,env=env,capture_output=True,text=True)
    (build/('pass_'+str(i+1)+'.txt')).write_text(p.stdout+p.stderr)
    if p.returncode:
        raise SystemExit((p.stdout+p.stderr)[-5000:])
log = (build/'promodular_realization_check.log').read_text()
result = {'schema':'rh-tex-validation/1','artifact_version':'0.29','component':'symplectic_promodular_realization',
 'main_tex_sha256':hashlib.sha256((here/'main.tex').read_bytes()).hexdigest(),
 'method':'pdflatex draftmode no-shell-escape, two passes, component wrapper with cumulative preamble',
 'syntax_compile_succeeded':True,'passes':2,'pdf_generated':False,'pdf_visual_review_performed':False,
 'undefined_references_or_citations':'undefined references' in log or 'undefined citations' in log,
 'missing_character_warnings':log.count('Missing character'),
 'overfull_box_warnings':len(re.findall(r'Overfull \\[hv]box',log)),
 'warnings':[line for line in log.splitlines() if 'Warning' in line],
 'log_sha256':hashlib.sha256(log.encode()).hexdigest(),
 'scope':'Syntax/reference validation only, not mathematical certification or visual review.'}
assert not (build/'promodular_realization_check.pdf').exists()
(here/'tex_validation.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
