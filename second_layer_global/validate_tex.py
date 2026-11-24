#!/usr/bin/env python3
"""Bounded offline draft-mode syntax check. Does not generate a PDF."""
from pathlib import Path
import hashlib, json, os, re, subprocess
ROOT=Path(__file__).resolve().parent
BASE=ROOT.parents[1]/'reconstruction_v030'
pre=(BASE/'RH_readable_reconstruction_v0_30.tex').read_text().split('\\begin{document}',1)[0]
(ROOT/'qa.tex').write_text(pre+'\\begin{document}\n\\input{main.tex}\n\\end{document}\n')
env=os.environ.copy()
env['TEXMF']='{/usr/share/texlive/texmf-dist,/usr/share/texmf,/etc/texmf}'
env['TEXFONTMAPS']=str(BASE/'build')+':'
passes=0
for i in range(2):
    r=subprocess.run(['pdflatex','-fmt='+str(BASE/'build/pdflatex.fmt'),'-draftmode','-no-shell-escape',
        '-interaction=nonstopmode','-halt-on-error','qa.tex'],cwd=ROOT,env=env,capture_output=True,text=True)
    (ROOT/'qa_console.txt').write_text(r.stdout+r.stderr)
    log=(ROOT/'qa.log').read_text() if (ROOT/'qa.log').exists() else r.stdout+r.stderr
    passes+=1
    if r.returncode or not any(s in log for s in ['Rerun to get','Label(s) may have changed','rerunfilecheck Warning']):break
result={'status':'PASS' if r.returncode==0 else 'FAIL',
    'main_sha256':hashlib.sha256((ROOT/'main.tex').read_bytes()).hexdigest(),
    'method':'Offline pdflatex -draftmode -no-shell-escape with inherited installed format; no PDF or visual layout review',
    'returncode':r.returncode,'passes':passes,
    'overfull_box_count':len(re.findall('Overfull',log)),
    'missing_characters':log.count('Missing character'),
    'warnings':[x for x in log.splitlines() if 'Warning' in x],
    'no_pdf_generated':not (ROOT/'qa.pdf').exists()}
(ROOT/'tex_validation.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
for m in re.finditer('Overfull',log): print(log[m.start():m.start()+360])
if r.returncode: print((r.stdout+r.stderr)[-2200:])
raise SystemExit(r.returncode)
