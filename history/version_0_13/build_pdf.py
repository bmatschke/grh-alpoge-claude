#!/usr/bin/env python3
"""Offline PDF build using installed TeX; no package download is attempted."""
from pathlib import Path
import os, shutil, subprocess

ROOT=Path(__file__).resolve().parent
BUILD=ROOT/'build';BUILD.mkdir(exist_ok=True)
env=os.environ.copy()
trees=[Path('/usr/share/texlive/texmf-dist'),Path('/usr/share/texmf'),Path('/etc/texmf')]
env['TEXMF']='{'+','.join(str(p)for p in trees if p.is_dir())+'}'
env['TEXFONTMAPS']=str(BUILD)+':'
maps=[trees[1]/'fonts/map/dvips/lm/lm.map',
      trees[0]/'fonts/map/dvips/amsfonts/cm.map',
      trees[0]/'fonts/map/dvips/amsfonts/symbols.map',
      trees[0]/'fonts/map/dvips/amsfonts/euler.map',
      trees[0]/'fonts/map/dvips/amsfonts/latxfont.map',
      trees[0]/'fonts/map/dvips/amsfonts/cmextra.map']
(BUILD/'pdftex.map').write_text('\n'.join(p.read_text()for p in maps))
fmt=BUILD/'pdflatex.fmt'
if not fmt.exists():
    cmd=['pdftex','-ini','-etex','-no-shell-escape','-interaction=nonstopmode','-halt-on-error','-jobname=pdflatex',f'-output-directory={BUILD}',r'\input pdflatex.ini']
    p=subprocess.run(cmd,cwd=BUILD,env=env,capture_output=True,text=True)
    (BUILD/'format_build.txt').write_text(p.stdout+p.stderr)
    if p.returncode:raise SystemExit((p.stdout+p.stderr)[-5000:])
tex=ROOT/'RH_readable_reconstruction_v0_13.tex'
for i in range(1,5):
    cmd=['pdflatex',f'-fmt={fmt}','-no-shell-escape','-interaction=nonstopmode','-halt-on-error',f'-output-directory={BUILD}',tex.name]
    p=subprocess.run(cmd,cwd=ROOT,env=env,capture_output=True,text=True)
    (BUILD/f'compile_pass_{i}.txt').write_text(p.stdout+p.stderr)
    if p.returncode:raise SystemExit((p.stdout+p.stderr)[-6500:])
    print(f'Offline PDF pass {i} completed.',flush=True)
    log=(BUILD/(tex.stem+'.log')).read_text()
    rerun=any(t in log for t in ['Rerun to get','Label(s) may have changed','Table widths have changed','rerunfilecheck Warning','undefined references','Citation `'])
    if i>=2 and not rerun:break
else:raise SystemExit('Cross-references still require a further build pass; inspect log.')
pdf=BUILD/(tex.stem+'.pdf')
shutil.copy2(pdf,ROOT/pdf.name)
print(str(ROOT/pdf.name))
