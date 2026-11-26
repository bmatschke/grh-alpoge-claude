#!/usr/bin/env python3
"""Compile current cumulative and increment TeX in draft mode; no PDF claim."""
from pathlib import Path
import hashlib
import json
import os
import re
import subprocess

ROOT=Path(__file__).resolve().parent
BUILD=ROOT/'build_v0_45'
BUILD.mkdir(exist_ok=True)
env=os.environ.copy()
trees=[Path('/usr/share/texlive/texmf-dist'),Path('/usr/share/texmf'),Path('/etc/texmf')]
env['TEXMF']='{'+','.join(str(p) for p in trees if p.is_dir())+'}'
env['TEXFONTMAPS']=str(BUILD)+':'
maps=[trees[1]/'fonts/map/dvips/lm/lm.map',trees[0]/'fonts/map/dvips/amsfonts/cm.map',
      trees[0]/'fonts/map/dvips/amsfonts/symbols.map',trees[0]/'fonts/map/dvips/amsfonts/euler.map',
      trees[0]/'fonts/map/dvips/amsfonts/latxfont.map',trees[0]/'fonts/map/dvips/amsfonts/cmextra.map']
(BUILD/'pdftex.map').write_text('\n'.join(p.read_text() for p in maps))
fmt=BUILD/'pdflatex.fmt'
if not fmt.is_file():
    p=subprocess.run(['pdftex','-ini','-etex','-no-shell-escape','-interaction=nonstopmode',
       '-halt-on-error','-jobname=pdflatex',f'-output-directory={BUILD}',r'\input pdflatex.ini'],
       cwd=BUILD,env=env,capture_output=True,text=True)
    (BUILD/'format_build.txt').write_text(p.stdout+p.stderr)
    if p.returncode:raise SystemExit((p.stdout+p.stderr)[-5000:])
results=[]
for name in ['RH_new_proofs_v0_45.tex','RH_readable_reconstruction_v0_45.tex']:
    tex=ROOT/name
    sub=BUILD/tex.stem
    sub.mkdir(exist_ok=True)
    for i in range(1,5):
        p=subprocess.run(['pdflatex',f'-fmt={fmt}','-draftmode','-no-shell-escape',
            '-interaction=nonstopmode','-halt-on-error',f'-output-directory={sub}',tex.name],
            cwd=ROOT,env=env,capture_output=True,text=True)
        (sub/f'tex_draft_pass_{i}.txt').write_text(p.stdout+p.stderr)
        if p.returncode:raise SystemExit(name+'\n'+(p.stdout+p.stderr)[-4000:])
        log=(sub/(tex.stem+'.log')).read_text()
        rerun=any(t in log for t in ['Rerun to get','Label(s) may have changed','Table widths have changed',
                                    'rerunfilecheck Warning','undefined references','Citation `'])
        if i>=2 and not rerun:break
    else:raise SystemExit(name+': TeX references remain unresolved after four draft passes.')
    assert not (sub/(tex.stem+'.pdf')).exists()
    warnings=[s.strip() for s in log.splitlines() if 'Warning' in s]
    result={'tex_filename':name,'tex_sha256':hashlib.sha256(tex.read_bytes()).hexdigest(),
       'syntax_compile_succeeded':True,'passes':i,'pdf_generated':False,
       'pdf_visual_review_performed':False,'page_count_asserted':False,
       'undefined_references_or_citations':any(t in log for t in ['undefined references','undefined citations','Citation `']),
       'missing_character_warnings':log.count('Missing character'),
       'overfull_box_warnings':len(re.findall(r'Overfull \\[hv]box',log)),
       'warnings':warnings,'log_sha256':hashlib.sha256(log.encode()).hexdigest()}
    results.append(result)
    print(json.dumps(result),flush=True)
out={'artifact_version':'0.45','method':'Offline pdflatex -draftmode -no-shell-escape; reference-driven reruns only.',
     'documents':results,'scope':'TeX syntax and cross-reference resolution only. No mathematical verification, Lean replay, PDF render or visual layout certification is inferred.'}
(ROOT/'tex_validation.json').write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n')
