#!/usr/bin/env python3
"""Bounded offline draft-mode syntax check; no PDF is generated."""
from pathlib import Path
import hashlib,json,os,re,subprocess
HERE=Path(__file__).resolve().parent
BASE=HERE.parents[1]/'reconstruction_v032'
FMT=HERE.parents[1]/'reconstruction_v030/build/pdflatex.fmt'
pre=(BASE/'RH_readable_reconstruction_v0_32.tex').read_text().split('\\begin{document}',1)[0]
(HERE/'qa.tex').write_text(pre+'\\begin{document}\n\\input{main.tex}\n\\end{document}\n')
env=os.environ.copy();env['TEXMF']='{/usr/share/texlive/texmf-dist,/usr/share/texmf,/etc/texmf}'
env['TEXFONTMAPS']=str(FMT.parent)+':'
passes=0
for i in range(2):
    r=subprocess.run(['pdflatex','-fmt='+str(FMT),'-draftmode','-no-shell-escape','-interaction=nonstopmode','-halt-on-error','qa.tex'],cwd=HERE,env=env,capture_output=True,text=True)
    (HERE/'qa_console.txt').write_text(r.stdout+r.stderr)
    log=(HERE/'qa.log').read_text() if (HERE/'qa.log').exists() else r.stdout+r.stderr
    passes+=1
    if r.returncode or not any(x in log for x in ['Rerun to get','Label(s) may have changed','rerunfilecheck Warning']):break
result={'status':'PASS' if r.returncode==0 else 'FAIL','main_sha256':hashlib.sha256((HERE/'main.tex').read_bytes()).hexdigest(),'method':'Offline pdflatex draftmode no-shell-escape; syntax and overflow check, no PDF/visual review','returncode':r.returncode,'passes':passes,'overfull_box_count':log.count('Overfull'),'missing_characters':log.count('Missing character'),'warnings':[x for x in log.splitlines() if 'Warning' in x],'no_pdf_generated':not (HERE/'qa.pdf').exists()}
(HERE/'tex_validation.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
for m in re.finditer('Overfull',log):print(log[m.start():m.start()+400])
if r.returncode:print((r.stdout+r.stderr)[-2200:])
raise SystemExit(r.returncode)
